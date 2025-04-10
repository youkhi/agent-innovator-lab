---
layout: default
title: Major Agentic Design Patterns - Reflection 
permalink: /1_agentic-design-ptn_01_reflection/
parent: Lab 1. Major Agentic Design Patterns 
nav_order: 5.1
---

# Major Agentic Design Patterns - Reflection 

## Reflection
---

The Reflection Pattern in Retrieval-Augmented Generation (RAG) refers to a method where the system iteratively refines its responses by incorporating feedback from previous generations. Instead of generating an answer in a single pass, the model evaluates its own output, identifies potential errors or gaps, and retrieves additional relevant information to improve accuracy and coherence. This approach enhances the quality of responses by enabling self-correction and iterative learning, making it particularly useful for complex queries requiring deep reasoning or factual accuracy.

## [Semantic Kernel Hands-On](./SK)

## [AutoGen Hands-On](./AutoGen)

## [LangGraph Hands-On](./LangGraph)

## Representative patterns

### Self-RAG

Self-RAG reflects on the retrieved documents and generated responses, and includes a self-evaluation process to improve the quality of the generated answers.

Original paper says Self-RAG generates special tokens, termed "reflection tokens," to determine if retrieval would enhance the response, allowing for on-demand retrieval integration. 
But in practice, we can ignore reflection tokens and let LLM decides if each document is relevant or not.

Corrective RAG (CRAG) is similar to Self-RAG, but Self-RAG focuses on self-reflection and self-evaluation, while CRAG focuses on refining the entire retrieval process including web search.

- **Self-RAG**: Trains the LLM to be self-sufficient in managing retrieval and generation processes. By generating reflection tokens, the model controls its behavior during inference, deciding when to retrieve information and how to critique and improve its own responses, leading to more accurate and contextually appropriate outputs. 
- **CRAG**: Focuses on refining the retrieval process by evaluating and correcting the retrieved documents before they are used in generation. It integrates additional retrievals, such as web searches, when initial retrievals are insufficient, ensuring that the generation is based on the most relevant and accurate information available.

### Corrective RAG

Corrective RAG (CRAG) is a methodology that adds a step to the RAG (Retrieval Augmented Generation) strategy to evaluate the documents found during the search process and refine the knowledge. This includes a series of processes to check the search results before generation and, if necessary, perform auxiliary searches to generate high-quality answers.

- Retrieval Grader: Evaluates the relevance of retrieved documents and assigns a score to each document.
- Web Search Integration: If quality of retrieved documents is low, CRAG uses web searches to augment retrieval results. It optimizes search results through query rewriting.

### Adaptive RAG
Adaptive RAG predicts the **complexity of the input question** using a SLM/LLM and selects an appropriate processing workflow accordingly.

- **Very simple question (No Retrieval)**: Generates answers without RAG.
- **Simple question (Single-shot RAG)**: Efficiently generates answers through a single-step search and generation.
- **Complex question (Iterative RAG)**: Provides accurate answers to complex questions through repeated multi-step search and generation.

Adaptive-RAG, Self-RAG, and Corrective RAG are similar approach, but they have different focuses.

- **Adaptive-RAG**: Dynamically selects appropriate retrieval and generation strategies based on the complexity of the question.
- **Self-RAG**: The model determines the need for retrieval on its own, performs retrieval when necessary, and improves the quality through self-reflection on the generated answers.
- **Corrective RAG**: Evaluates the quality of retrieved documents, and performs additional retrievals such as web searches to supplement the information if the reliability is low.

**Reference**
- [ReAct paper](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve paper](https://arxiv.org/abs/2305.04091)
- [Baby-AGI project](https://github.com/yoheinakajima/babyagi)  
- [Corrective RAG paper](https://arxiv.org/pdf/2401.15884)  
- [Adaptive-RAG paper](https://arxiv.org/abs/2403.14403)  
