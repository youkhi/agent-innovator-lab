---
layout: home
title: Basic of Agent - LangGraph
nav_order: 2.2
---

# LangGraph

---

LangGraph is a robust framework for developing stateful, multi-actor applications leveraging Large Language Models (LLMs). It provides a graph-based execution model that enables structured, dynamic, and scalable workflows, making it a powerful tool for building multi-agent systems and conversational AI applications. LangGraph is designed to overcome the stateless nature of traditional LLM pipelines, allowing developers to persist state, control execution flow, and integrate human feedback seamlessly. Its flexibility makes it suitable for a variety of use cases, from chatbot orchestration to complex decision-making systems.

### Core Features of LangGraph

- **Graph-Based Execution Model**: LangGraph structures workflows as a directed graph, where nodes represent functions (or agents) and edges define the flow of execution. This allows for parallel execution, conditional branching, and dynamic state updates. It provides a structured alternative to unstructured LLM chaining, making debugging and monitoring more intuitive.

- **Stateful Processing with Persistence**: Unlike traditional LLM applications that process inputs independently, LangGraph maintains state across multiple interactions. It supports long-running tasks, memory retention, and interruption-resumption workflows, ensuring continuity in interactions and decision-making processes.

- **Multi-Agent Collaboration**: LangGraph makes it easy to design multi-agent environments, where multiple autonomous agents communicate and collaborate to complete complex tasks. It supports event-driven execution, allowing agents to operate asynchronously, respond to real-time events, and coordinate decisions dynamically.

- **Human-in-the-Loop Support**:One of LangGraph’s key strengths is its built-in support for human intervention. Workflows can pause execution at critical decision points, request human validation or input, and then resume execution, making it ideal for applications requiring human oversight, such as legal document review, customer service escalation, or AI-assisted research.

### [Hands-On](1_building-graph-practice.ipynb)