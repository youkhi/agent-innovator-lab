import os
import json
import requests
import asyncio
import httpx
import logging
from typing import List, Tuple, Dict, Any, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import scrapy
from dotenv import load_dotenv
load_dotenv(override=True) 

# Optional Azure imports - only used for Bing grounding search
try:
    from azure.ai.projects.models import MessageRole, BingGroundingTool
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    AZURE_IMPORTS_AVAILABLE = True
except ImportError:
    AZURE_IMPORTS_AVAILABLE = False

# Set up logging
logger = logging.getLogger(__name__)


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
    
def bing_grounding_search(query, num=5, search_type="web"):
    """
    Perform a web search using Azure AI Project's Bing Grounding feature.
    
    Args:
        query: The search query
        num: Number of results to return
        search_type: Type of search (web or image)
        
    Returns:
        List of search results
    """
    if not AZURE_IMPORTS_AVAILABLE:
        logger.warning("Azure AI Projects SDK not installed. Using fallback to Google search.")
        return google_search(query, num, search_type)
        
    # Get credentials from environment variables
    BING_GROUNDING_PROJECT_CONNECTION_STRING = os.getenv("BING_GROUNDING_PROJECT_CONNECTION_STRING")
    BING_GROUNDING_AGENT_ID = os.getenv("BING_GROUNDING_AGENT_ID")
    BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME = os.getenv("BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME")
    BING_GROUNDING_CONNECTION_NAME = os.getenv("BING_GROUNDING_CONNECTION_NAME")
    
    if not BING_GROUNDING_PROJECT_CONNECTION_STRING:
        logger.warning("Bing Grounding connection string not set. Using fallback to Google search.")
        return google_search(query, num, search_type)
        
    try:
        creds = DefaultAzureCredential()
        
        project_client = AIProjectClient.from_connection_string(
            credential=creds,
            conn_str=BING_GROUNDING_PROJECT_CONNECTION_STRING,
        )
        
        agent_id = BING_GROUNDING_AGENT_ID
        
        if not agent_id:
            logger.info("BING_GROUNDING_AGENT_ID not set. Creating new agent...")
            connection_name = BING_GROUNDING_CONNECTION_NAME
            
            bing_connection = project_client.connections.get(
                connection_name=connection_name,
            )
            conn_id = bing_connection.id
            
            bing = BingGroundingTool(connection_id=conn_id)
            
            agent = project_client.agents.create_agent(
                model=BING_GROUNDING_AGENT_MODEL_DEPLOYMENT_NAME,
                name="temporary-bing-agent",
                instructions="""
                    Search for product information and provide comprehensive results. 
                    Return only relevant information from trusted sources.
                    Prioritize official websites whenever available to ensure accuracy and reliability.
                """,
                tools=bing.definitions,
                headers={"x-ms-enable-preview": "true"}
            )
            agent_id = agent.id
            logger.info(f"New agent created. Agent ID: {agent_id}")
        else:
            logger.info(f"Using existing agent ID: {agent_id}")
            try:
                agent = project_client.agents.get_agent(agent_id)
            except Exception as agent_error:
                logger.error(f"Failed to retrieve agent: {agent_error}")
                return []

        thread = project_client.agents.create_thread()
        
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"Search the web for: {query}. Return only the top {num} most relevant results as a list.",
        )
        
        run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
        
        if run.status == "failed":
            logger.error(f"Bing Grounding execution failed: {run.last_error}")
            return []
        
        results = []
        response_message = project_client.agents.list_messages(thread_id=thread.id).get_last_message_by_role(
            MessageRole.AGENT
        )
        
        # Extract content text and annotations
        if response_message.content:
            for content_item in response_message["content"]:
                if content_item["type"] == "text":
                    text_content = content_item["text"]["value"]
                    results.append({"content": text_content})
            
        if response_message.url_citation_annotations:
            for annotation in response_message.url_citation_annotations:
                if annotation["type"] == "url_citation":
                    url_citation = annotation["url_citation"]
                    url = url_citation["url"]
                    title = url_citation["title"]
                    results.append({"url_citation":{"link": url, "title": title}})

        # Clean up temporary agent if needed
        if not BING_GROUNDING_AGENT_ID and hasattr(agent, 'id'):
            try:
                logger.info(f"Deleting temporary agent with ID: {agent.id}")
                project_client.agents.delete_agent(agent.id)
            except Exception as delete_error:
                logger.error(f"Error deleting agent: {delete_error}")

        return results if results else []
    except Exception as e:
        logger.error(f"Bing Grounding error: {e}")
        return google_search(query, num, search_type)  # Fallback to Google search

def web_search(query, num=5, search_type="web", web_search_mode=None):
    """
    Unified search function that uses either Google Search or Bing Grounding based on environment variables.
    
    Args:
        query: The search query (string or dict with 'web_search' and 'llm_query' keys)
        num: Number of results to return
        search_type: Type of search (web or image)
        
    Returns:
        List of search results
    """
    # Get web search mode from environment variables
    WEB_SEARCH_MODE = os.getenv("WEB_SEARCH_MODE", "bing").lower()
    # Override with function argument if provided
    if web_search_mode:
        WEB_SEARCH_MODE = web_search_mode
    print(f"Using web search mode: {WEB_SEARCH_MODE}")
    # Check if query is a dictionary with separate search queries
    query_for_search = query
    if isinstance(query, dict):
        if WEB_SEARCH_MODE == "bing" and "llm_query" in query:
            query_for_search = query["llm_query"]
        elif "web_search" in query:
            query_for_search = query["web_search"]
    
    # Use appropriate search engine based on environment variable
    if WEB_SEARCH_MODE == "bing":
        try:
            logger.info(f"Using Bing Grounding search for query: {query_for_search}")
            return bing_grounding_search(query_for_search, num, search_type)
        except Exception as e:
            logger.error(f"Bing Grounding search failed: {e}")
    else:
        logger.info(f"Using Google search for query: {query_for_search}")
        return google_search(query_for_search, num, search_type)

async def extract_contexts_async(url_snippet_tuples: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
    """
    Asynchronously extract content from a list of URLs with their snippets.
    
    Args:
        url_snippet_tuples: List of (url, snippet) pairs to process
        
    Returns:
        List of extracted contents with URL citations
    """
    async def fetch(url: str, snippet: str) -> Dict[str, Any]:
        # Add user agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                try:
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    # Handle redirects manually if needed
                    if e.response.status_code == 302 and "location" in e.response.headers:
                        redirect_url = e.response.headers["location"]
                        if not redirect_url.startswith("http"):
                            redirect_url = urljoin(url, redirect_url)
                        try:
                            response = await client.get(redirect_url, headers=headers)
                            response.raise_for_status()
                        except Exception as e2:
                            logger.error(f"Redirect request failed: {e2}")
                            return {"content": f"{snippet} ", "url_citation": {"link": url, "title": snippet}}
                    else:
                        logger.error(f"Request failed: {e}")
                        return {"content": f"{snippet} ", "url_citation": {"link": url, "title": snippet}}
                except httpx.HTTPError as e:
                    logger.error(f"Request failed: {e}")
                    return {"content": f"{snippet} ", "url_citation": {"link": url, "title": snippet}}
                
                # Parse the content
                selector = scrapy.Selector(text=response.text)
                
                # Extract paragraphs
                paragraphs = [p.strip() for p in selector.css('p::text, p *::text').getall() if p.strip()]
                
                # Remove duplicate and very short paragraphs
                filtered_paragraphs = []
                seen_content = set()
                for p in paragraphs:
                    # Skip very short paragraphs that are likely UI elements
                    if len(p) < 5:
                        continue
                    # Avoid duplicate content
                    if p in seen_content:
                        continue
                    seen_content.add(p)
                    filtered_paragraphs.append(p)
                
                # Join the filtered paragraphs
                text = "\n".join(filtered_paragraphs)
                
                # If no paragraphs were found, try to get other text content
                if not text:
                    content_texts = [t.strip() for t in selector.css(
                        'article::text, article *::text, .content::text, .content *::text, '
                        'main::text, main *::text'
                    ).getall() if t.strip()]
                    
                    if content_texts:
                        text = "\n".join(content_texts)
                
                # Combine snippet with extracted text
                snippet_text = f"{snippet}: {text}"
                
                return {"content": snippet_text, "url_citation": {"link": url, "title": snippet}}
                
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            return {"content": f"{snippet} [Error: {str(e)}]", "url_citation": {"link": url, "title": snippet}}
    
    # Create tasks for all URLs
    tasks = [asyncio.create_task(fetch(url, snippet)) 
            for url, snippet in url_snippet_tuples]
    
    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Error processing URL {url_snippet_tuples[i][0]}: {str(result)}")
            processed_results.append({
                "content": f"{url_snippet_tuples[i][1]} [Processing Error]", 
                "url_citation": {"link": url_snippet_tuples[i][0], "title": url_snippet_tuples[i][1]}
            })
        else:
            processed_results.append(result)

    return processed_results

