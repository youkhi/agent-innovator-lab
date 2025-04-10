---
layout: default
title: Major Agentic Design Patterns - Multi-Agent
permalink: /1_agentic-design-ptn_03_multi-agent/
parent: Lab 1. Major Agentic Design Patterns 
nav_order: 5.3
---

# Major Agentic Design Patterns - Multi-Agent
---

Multi-Agent is an advanced AI framework where **multiple specialized agents collaborate** to improve retrieval and generation processes. Instead of a single model handling all tasks, different agents are assigned specific roles, such as retrieval, planning, reasoning, verification, and generation. These agents **communicate and refine outputs iteratively**, leading to more accurate, context-aware, and explainable responses. Multi-Agent RAG is particularly useful for complex problem-solving, knowledge-intensive tasks, and long-context reasoning, enhancing the reliability and efficiency of AI-generated content.

## [Semantic Kernel Hands-On](./SK)

## [AutoGen Hands-On](./AutoGen)

## [LangGraph Hands-On](./LangGraph)

## Representative patterns

### Multi-Agent Supervisor

A Multi-Agent Supervisor is a control mechanism that oversees and coordinates multiple autonomous agents operating within a system. It ensures that agents work collaboratively and efficiently by managing tasks, resolving conflicts, optimizing resource allocation, and enforcing system constraints. The supervisor can be centralized, decentralized, or distributed, depending on the system architecture. It is commonly used in multi-robot systems, industrial automation, and AI-driven applications to enhance coordination, adaptability, and decision-making.

As the number of agents increases, the branching logic also becomes more complex. The Supervisor agent gathers various specialized agents together and operates them as a single team. The Supervisor agent observes the progress of the team and performs logic such as calling the appropriate agent for each step or terminating the task.

### Mult-Agent Collaboration

Multi-Agent Collaboration refers to the process where multiple autonomous agents—each capable of independent decision-making—work together to achieve common or complementary objectives. This concept is widely used in fields like artificial intelligence, robotics, distributed computing, and simulation, and it involves several key aspects:

- **Effective Communication and Coordination**:
Agents exchange information and align their actions to collectively achieve a goal, ensuring that tasks are organized and synchronized.

- **Autonomous, Distributed Decision-Making**:
Each agent operates independently, making local decisions while contributing to a broader strategy, which enhances flexibility and fault tolerance.

- **Adaptive Task Specialization**:
Agents focus on specific roles or subtasks based on their capabilities, and they adjust their strategies through iterative feedback, leading to improved overall performance.


**Reference**
- [Multi-Agent Supervisor Concept](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#supervisor)  
- [Multi-Agent Collabration Concept](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#network) 
- [LangChain `create_react_agent` built-in function](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)