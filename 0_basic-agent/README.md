---
layout: default
title: Lab 0. Building a Basic Agent
permalink: /0_basic_agent/
has_children: true
nav_order: 4
---

# Building a Basic Agent
---

## Overview

Agents are the core building blocks of AI systems, responsible for executing specific tasks, making decisions, and interacting with users or other agents. A well-designed agent architecture is crucial for achieving optimal performance, scalability, and maintainability in AI applications. This hands-on guide demonstrates how to create a basic agent using [Microsoft AutoGen](https://github.com/microsoft/autogen) or [LangGraph](https://langchain-ai.github.io/langgraph/), powerful AI toolkits that simplifies agent development and deployment.

**AutoGen focuses on autonomous multi-agent interactions, while LangGraph emphasizes structured, graph-based execution with deterministic workflows**. You should be able to determine the right agent pattern and toolkit for your use case and use the right toolkit for AI production 

#### Architecture & Design Philosophy
- AutoGen: Designed as an agent-based framework, where multiple AI agents communicate and collaborate autonomously to solve tasks. It focuses on multi-agent coordination and self-improving workflows.
- LangGraph: Based on a graph-based execution model, allowing for flexible, deterministic flow control in multi-step AI pipelines. It is optimized for directed acyclic graphs (DAGs) to structure agent interactions 
explicitly.

#### Execution & Workflow Control
- AutoGen: Uses dynamic interactions between agents, where agents decide their next steps based on the context, making the workflow more flexible but less predictable.
- LangGraph: Employs predefined execution flows using a graph structure, ensuring better control over the sequence of operations while still allowing for dynamic logic.

#### Use Cases & Flexibility
- AutoGen: Best suited for autonomous multi-agent collaboration, such as AI-driven dialogue, problem-solving, and self-learning agents.
- LangGraph: More suitable for structured, deterministic AI pipelines, such as workflow automation, task-specific retrieval-augmented generation (RAG), and multi-step reasoning.


## Step-by-Step Guide

### Step 1. Construct and Visualize Agents
Visualizing abstract agents through sketches or diagrams is essential for several reasons:

- **Improved Comprehension** – Abstract agents and their interactions can be difficult to grasp in purely textual or code-based formats. Visual representations make it easier to understand complex relationships and data flows at a glance.
- **Debugging and Troubleshooting** – Visualizing agents helps identify inconsistencies, missing connections, or unexpected interactions in a multi-agent system. This proactive approach can reduce debugging time and prevent potential issues.
- **Efficient System Design** – By mapping out interactions between agents, designers can optimize workflows, remove redundancies, and ensure that the architecture is well-structured before implementation.

AutoGen does not support visualization in a form similar to langgraph. Thus, the author created a custom toolkit (`azure_genai_utils`), which can also help in building AutoGen-based agents.

### Step 2. Implement Agents in AutoGen or LangGraph

If you are not familiar with AutoGen/LangGraph, you can start with the [AutoGen Hands-On](./AutoGen) or [LangGraph Hands-On](./LangGraph) to get a better understanding of the concepts.

### [AutoGen Hands-On](./AutoGen)

### [LangGraph Hands-On](./LangGraph)