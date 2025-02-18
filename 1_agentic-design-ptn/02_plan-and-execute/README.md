---
layout: default
title: Major Agentic Design Patterns - Plan and Execute 
permalink: /1_agentic-design-ptn_02_plan-and-execute/
parent: Lab 1. Major Agentic Design Patterns 
nav_order: 5.2
---


# Plan and Execute 
---

## [AutoGen Hands-On](./AutoGen)

## [LangGraph Hands-On](./LangGraph)

## Representative patterns

### Plan-and-Execute Basics

The Plan-and-Execute framework is a strategy for retrieval-augmented generation (RAG) that divides complex reasoning tasks into two distinct phases: planning and execution. While traditional ReAct agents think one step at a time, plan-and-execute emphasizes explicit, long-term planning.

- **Planning Phase**: The model generates a high-level plan or structured outline that serves as a roadmap for solving the task. This phase ensures that the execution is systematic and adheres to the task's requirements.

- **Execution Phase**: Based on the generated plan, the model retrieves relevant information and executes the outlined steps to provide a detailed and coherent response.

This separation aims to address limitations in RAG systems that attempt to perform reasoning and generation in a single step, often leading to logical errors or inefficiency in handling complex tasks.


**Reference**
- [ReAct paper](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve paper](https://arxiv.org/abs/2305.04091)
- [Baby-AGI project](https://github.com/yoheinakajima/babyagi)  