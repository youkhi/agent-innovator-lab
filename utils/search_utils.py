import os
import json
import requests
import asyncio
import httpx
import logging
from typing import List, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import scrapy
from dotenv import load_dotenv
load_dotenv(override=True) 
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    BingGroundingTool,
    MessageRole,
)
from datetime import datetime
import pytz 
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import AgentStreamEvent, RunStepDeltaChunk, RunStatus
from azure.ai.projects import AIProjectClient
from langchain_core.prompts import load_prompt, PromptTemplate


# Set up logging
logger = logging.getLogger(__name__)

SEARCH_GENERATE_PROMPT_TEMPLATE = """
You are an intelligent chatbot that provides guidance on {product_name} in **Markdown** format based on real-time web search results.

🎯 Objective:
- Provide users with accurate and reliable answers based on the latest web information.
- Actively utilize web search results to generate rich and specific answers.
- Respond in Markdown format, including 1-2 emojis to increase readability and friendliness.

📌 Guidelines:  
1. Always generate answers based on search results and avoid making unfounded assumptions.  
2. Always include reference links and format them using the Markdown `[text](URL)` format.  
3. When providing product price information, base it on the official website's prices and links.
4. don't response with greeting messages, just response with the answer to the user's question.
"""




def google_search(query, num=5, search_type="web"):
    """
    Perform a web search using Google Custom Search API.
    
    Args:
        query: The search query
        num: Number of results to return
        search_type: Type of search (web or image)
        
    Returns:
        List of search results
    """
    # Get API credentials from environment variables
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    
        
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query + " -filetype:pdf",  # Exclude PDF files which are harder to parse
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "num": num,
        "filter": "1"  # Filter duplicate content
    }
    
    if search_type == "image":
        params["searchType"] = "image"
        
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for non-200 status codes
        results = response.json()
        return results.get("items", [])
    except Exception as e:
        logger.error(f"Error performing Google search: {e}")
        return []
    
def bing_grounding_search(query, product_name=None):
    """
    Perform a web search using Azure AI Project's Bing Grounding feature.
    
    Args:
        query: The search query
        product_name: Optional product name to include in the search prompt
        
    Returns:
        List of search resultss
    """   
    # Get credentials from environment variables
    BING_GROUNDING_PROJECT_ENDPOINT = os.getenv("BING_GROUNDING_PROJECT_ENDPOINT")
    BING_GROUNDING_CONNECTION_ID = os.getenv("BING_GROUNDING_CONNECTION_ID")
    BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME = os.getenv("BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME")
    BING_GROUNDING_MAX_RESULTS = int(os.getenv("BING_GROUNDING_MAX_RESULTS", 3))
    BING_GROUNDING_MARKET = os.getenv("BING_GROUNDING_MARKET", "ko-KR")
    BING_GROUNDING_SET_LANG = os.getenv("BING_GROUNDING_SET_LANG", "ko-KR")

    creds = DefaultAzureCredential()
    
    project_client = AIProjectClient(
        endpoint=BING_GROUNDING_PROJECT_ENDPOINT,
        credential=creds,
    )
    
    SEARCH_GEN_PROMPT = PromptTemplate(
        template=SEARCH_GENERATE_PROMPT_TEMPLATE,
        input_variables=["product_name"]
    )

    bing = BingGroundingTool(connection_id=BING_GROUNDING_CONNECTION_ID, market=BING_GROUNDING_MARKET, set_lang=BING_GROUNDING_SET_LANG, count=int(BING_GROUNDING_MAX_RESULTS))

    search_gen_agent = project_client.agents.create_agent(
                model=BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME,
                name="temp-grounding-agent",
                instructions=SEARCH_GEN_PROMPT.format(product_name=product_name),
                tools=bing.definitions,
            )
    
    
    SEARCH_GEN_USER_PROMPT_TEMPLATE = """
            please provide as rich and specific an answer and reference links as possible for `{query}`.
            Today is {current_date}. Results should be based on the recent information available.
        """

    # Create a LangChain PromptTemplate
    SEARCH_GEN_USER_PROMPT = PromptTemplate(
        template=SEARCH_GEN_USER_PROMPT_TEMPLATE,
        input_variables=["query","current_date"]
    )
    current_date = datetime.now(tz=pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

    search_gen_instruction = SEARCH_GEN_USER_PROMPT.format(
        query=query,
        current_date=current_date
    )
    
    thread = project_client.agents.threads.create()
    logger.info(f"Created thread, ID: {thread.id}")

    # Create message to thread
    logger.info(f"final user_instruction on Azure AI Agent: {search_gen_instruction}")
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=search_gen_instruction,
    )
    logger.info(f"Created message, ID: {message.id}")


    logger.info("Creating and processing agent run in thread with tools")
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=search_gen_agent.id)
    logger.info(f"Run finished with status: {run.status}")

    # Print the Agent's response message with optional citation
    try:
        text_content = []
        last_message = project_client.agents.messages.get_last_message_by_role(
                    thread_id=thread.id, 
                    role=MessageRole.AGENT,
                )
        if last_message is None or not getattr(last_message, "content", None):
            logger.error("Agent response message not found after retries.")
            return "No response from agent."

        if last_message:
            for text_message in last_message.text_messages:
                text_content.append(text_message.text.value)

        # add for testing, delete thread and agent
        # for production, you need to manage the thread and agent lifecycle properly
        project_client.agents.threads.delete(thread.id)
        logger.info(f"Deleted thread with ID: {thread.id}")
        
        project_client.agents.delete_agent(search_gen_agent.id)
        logger.info(f"Deleted agent with ID: {search_gen_agent.id}")
        
        
        return text_content
    except Exception as e:
        logger.error(f"Error retrieving agent response: {str(e)}")
        return "Error retrieving agent response."
        

def bing_url_search(query, max_result=5, product_name=None):
    """
    Perform a web search using Azure AI Project's Bing Grounding feature.
    
    Args:
        query: The search query
        num: Number of results to return
        
    Returns:
        List of search results
    """
    # Get credentials from environment variables
    BING_GROUNDING_PROJECT_ENDPOINT = os.getenv("BING_GROUNDING_PROJECT_ENDPOINT")
    BING_GROUNDING_CONNECTION_ID = os.getenv("BING_GROUNDING_CONNECTION_ID")
    BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME = os.getenv("BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME")
    BING_GROUNDING_MAX_RESULTS = int(os.getenv("BING_GROUNDING_MAX_RESULTS", 3))
    BING_GROUNDING_MARKET = os.getenv("BING_GROUNDING_MARKET", "ko-KR")
    BING_GROUNDING_SET_LANG = os.getenv("BING_GROUNDING_SET_LANG", "ko-KR")

    
    creds = DefaultAzureCredential()
    
    project_client = AIProjectClient(
        endpoint=BING_GROUNDING_PROJECT_ENDPOINT,
        credential=creds,
    )
    
    SEARCH_SYSTEM_PROMPT_TEMPLATE = """
    You are an intelligent chatbot that can perform real-time web searches for {product_name}.
    """

    SEARCH_SYSTEM_PROMPT = PromptTemplate(
        template=SEARCH_SYSTEM_PROMPT_TEMPLATE,
        input_variables=["product_name"]
    )
    
    SEARCH_USER_PROMPT_TEMPLATE = """
        Search the web for: {query}. Return only the top {max_results} most relevant results as a list.
        Today is {current_date}. Results should be based on the recent information available.
    """

    # Create a LangChain PromptTemplate
    SEARCH_USER_PROMPT = PromptTemplate(
        template=SEARCH_USER_PROMPT_TEMPLATE,
        input_variables=["query","current_date", "max_results"]
    )
    
    bing = BingGroundingTool(connection_id=BING_GROUNDING_CONNECTION_ID, market=BING_GROUNDING_MARKET, set_lang=BING_GROUNDING_SET_LANG, count=int(BING_GROUNDING_MAX_RESULTS))

    search_agent = project_client.agents.create_agent(
        model=BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME,
        name="temp-search-agent",
        instructions=SEARCH_SYSTEM_PROMPT.format(product_name=product_name),
        tools=bing.definitions,
    )

    thread = project_client.agents.threads.create()
    logger.info(f"Created thread, ID: {thread.id}")

    # Create message to thread
    
    current_date = datetime.now(tz=pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=SEARCH_USER_PROMPT.format(query=query, current_date=current_date, max_results=max_result),
    )
    logger.info(f"Created message, ID: {message.id}")


    logger.info("Creating and processing agent run in thread with tools")
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=search_agent.id)
    logger.info(f"Run finished with status: {run.status}")

    # Print the Agent's response message with optional citation
    try:
        url_content = []
        last_message = project_client.agents.messages.get_last_message_by_role(
                    thread_id=thread.id, 
                    role=MessageRole.AGENT,
                )
        logger.info(f"response_message: {last_message}")
            
        if last_message.url_citation_annotations:
            for annotation in last_message.url_citation_annotations:
                url = annotation.url_citation.url
                title = annotation.url_citation.title
                url_content.append({"link": url, "snippet": title})

        # add for testing, delete thread and agent
        # for production, you need to manage the thread and agent lifecycle properly
        project_client.agents.threads.delete(thread.id)
        logger.info(f"Deleted thread with ID: {thread.id}")

        project_client.agents.delete_agent(search_agent.id)
        logger.info(f"Deleted agent with ID: {search_agent.id}")


        return url_content
    except Exception as e:
        logger.error(f"Error retrieving agent response: {str(e)}")
        return "Error retrieving agent response."        

def url_search(query, max_result=5, web_search_mode=None, product_name="whatever"):
    """
    Unified search function that uses either Google Search or Bing Grounding based on environment variables.
    
    Args:
        query: The search query (string or dict with 'web_search' and 'llm_query' keys)
        max_result: Number of results to return
        web_search_mode: Optional search mode, defaults to environment variable WEB_SEARCH_MODE
        
    Returns:
        List of search results
    """
    if web_search_mode is None:
        web_search_mode = os.getenv("WEB_SEARCH_MODE", "bing").lower()
    # Check if query is a dictionary with separate search queries
    
    # Use appropriate search engine based on environment variable
    if web_search_mode == "bing":
        try:
            logger.info(f"Using Bing Grounding search for query: {query}")
            return bing_url_search(query, product_name=product_name)
        except Exception as e:
            logger.error(f"Bing Grounding search failed: {e}")     
            
    elif web_search_mode == "google":
        try:
            logger.info(f"Using Google search for query: {query}")
            return google_search(query, max_result, "web")
        

        except Exception as e:
            logger.error(f"Google search failed: {e}")

    
            

async def web_search(query, max_result=5, web_search_mode=None, product_name="whatever"):
    """
    Unified search function that uses either Google Search or Bing Grounding based on environment variables.
    
    Args:
        query: The search query (string or dict with 'web_search' and 'llm_query' keys)
        num: Number of results to return
        
    Returns:
        List of search results
    """
    if web_search_mode is None:
        web_search_mode = os.getenv("WEB_SEARCH_MODE", "bing").lower()
    
    # Check if query is a dictionary with separate search queries
    query_for_search = query
    if isinstance(query, dict):
        if web_search_mode == "bing" and "llm_query" in query:
            query_for_search = query["llm_query"]
        elif "web_search" in query:
            query_for_search = query["web_search"]
    
    # Use appropriate search engine based on environment variable
    if web_search_mode == "bing":
        try:
            logger.info(f"Using Bing Grounding search for query: {query_for_search}")
            return bing_grounding_search(query_for_search, product_name=product_name)
        except Exception as e:
            logger.error(f"Bing Grounding search failed: {e}")
    else:
        logger.info(f"Using Google search for query: {query_for_search}")
        results = google_search(query_for_search, max_result, "web") # default to web search
        url_snippet_tuples = [(r["link"], r["snippet"]) for r in results]
        contexts = await extract_contexts_async(url_snippet_tuples)
        return contexts

async def extract_contexts_async(url_snippet_tuples: List[Tuple[str, str]]) -> List[str]:
        """
        Asynchronously extract content from a list of URLs with their snippets.
        
        Args:
            url_snippet_tuples: List of (url, snippet) pairs to process
            
        Returns:
            List of extracted contents
        """
        async def fetch_and_cache(url: str, snippet: str) -> str:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            try:
                async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                    try:
                        response = await client.get(url, headers=headers)
                        response.raise_for_status()
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 302 and "location" in e.response.headers:
                            redirect_url = e.response.headers["location"]
                            if not redirect_url.startswith("http"):
                                redirect_url = urljoin(url, redirect_url)
                            try:
                                response = await client.get(redirect_url, headers=headers)
                                response.raise_for_status()
                            except Exception as e2:
                                logger.error(f"Redirect request failed: {e2}")
                                return f"{snippet} "
                        else:
                            logger.error(f"Request failed: {e}")
                            return f"{snippet} "
                    except httpx.HTTPError as e:
                        logger.error(f"Request failed: {e}")
                        return f"{snippet} "
                    
                    selector = scrapy.Selector(text=response.text)
                    
                    paragraphs = [p.strip() for p in selector.css('p::text, p *::text').getall() if p.strip()]
                    
                    filtered_paragraphs = []
                    seen_content = set()
                    for p in paragraphs:
                        if len(p) < 5:
                            continue
                        if p in seen_content:
                            continue
                        seen_content.add(p)
                        filtered_paragraphs.append(p)
                    
                    text = "\n".join(filtered_paragraphs)
                    
                    if not text:
                        content_texts = [t.strip() for t in selector.css(
                            'article::text, article *::text, .content::text, .content *::text, '
                            'main::text, main *::text'
                        ).getall() if t.strip()]
                        
                        if content_texts:
                            text = "\n".join(content_texts)
                    
                    snippet_text = f"{snippet}: {text}"
                    
                    
                    return snippet_text
                    
            except Exception as e:
                logger.error(f"Error processing URL {url}: {str(e)}")
                return f"{snippet} [Error: {str(e)}]"
        
        tasks = [asyncio.create_task(fetch_and_cache(url, snippet)) 
                for url, snippet in url_snippet_tuples]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing URL {url_snippet_tuples[i][0]}: {str(result)}")
                processed_results.append(f"{url_snippet_tuples[i][1]} [Processing Error]")
            else:
                processed_results.append(result)
                
        return processed_results

