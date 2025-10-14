---
layout: default
title: Basic of Agent - Microsoft Agent Framework
permalink: /0_basic-agent_AgentFramework/
parent: Lab 0. Building a Basic Agent
nav_order: 2.1
---

# Microsoft Agent Framework

---

## Overview

Microsoft Agent Framework is the **open-source engine for building production-ready agentic AI applications**. It represents the evolution and unification of **Semantic Kernel** and **AutoGen**, bringing together the enterprise-ready foundations with innovative orchestration patterns in a single framework for both experimentation and production deployment.

![Microsoft Agent Framework Architecture](https://devblogs.microsoft.com/foundry/wp-content/uploads/sites/89/2025/09/AgentStack.png)

---

## Core Components of Microsoft Agent Framework

Microsoft Agent Framework consists of four main components that work together to enable sophisticated agentic AI applications:

### 1. **Chat Agents**
Core agents that handle conversational interactions using any compatible chat client:
- **Azure OpenAI**: Enterprise-grade OpenAI models hosted on Azure
- **Azure AI Agent Service**: Managed agent service with built-in observability
- **OpenAI**: Direct integration with OpenAI API
- **Azure Responses API**: Structured response generation

### 2. **Tools & Functions**
Extensible capabilities that agents can use to interact with external systems:
- **Built-in Hosted Tools**: Code Interpreter, File Search, Web Search (Bing Grounding)
- **Custom Function Tools**: User-defined functions with `@ai_function` decorator
- **MCP Integration**: Model Context Protocol for standardized tool interfaces
- **OpenAPI Support**: Automatic API integration from OpenAPI specifications

### 3. **Multi-Agent Orchestration**
Patterns for coordinating multiple agents to solve complex tasks:
- **Sequential**: Step-by-step execution with dependencies
- **Concurrent**: Parallel execution for independent tasks
- **Group Chat**: Turn-based collaborative dialogue
- **Handoff**: Dynamic task delegation between agents
- **Magentic**: Intelligent orchestration with planning and adaptation

### 4. **Open Standards**
Native support for interoperability and integration:
- **MCP (Model Context Protocol)**: Standardized protocol for tool and context sharing
- **A2A (Agent-to-Agent)**: Inter-agent communication protocol
- **OpenAPI**: REST API integration and tool discovery

---

## Key Design Principles

### 1. **Open Standards First**
Built on MCP, A2A, and OpenAPI for maximum interoperability with existing tools and services, ensuring your agents can integrate with any system.

### 2. **Research to Production Pipeline**
Cutting-edge orchestration patterns from Microsoft Research, production-ready out of the box with built-in durability, observability, and security features.

### 3. **Extensible by Design**
Modular architecture with pluggable components allows you to customize every aspect of your agent system while maintaining compatibility.

### 4. **Enterprise Ready**
Built-in support for:
- **Observability**: OpenTelemetry integration for monitoring and debugging
- **Security**: Azure AD integration and managed identities
- **Durability**: Workflow checkpointing and state management
- **Human-in-the-loop**: Approval workflows and intervention points

---

## Comparison with Other Frameworks

### **vs. Semantic Kernel**

| Feature | Semantic Kernel | Agent Framework |
|---------|----------------|-----------------|
| **Agent Creation** | Requires Kernel coupling | Direct agent creation |
| **Thread Management** | Manual management | Built-in automatic management |
| **Tool Registration** | Attribute decorators required | Inline registration |
| **Azure AI Integration** | Plugin-based | Native service integration |
| **Workflow API** | Plugin orchestration | Graph-based with checkpointing |

**Key Benefits:**
- ✅ Simplified agent creation without Kernel complexity
- ✅ Native thread management reduces boilerplate code
- ✅ Inline tool registration is more intuitive
- ✅ Direct integration with Azure AI Foundry Agent Service

### **vs. AutoGen**

| Feature | AutoGen | Agent Framework |
|---------|---------|-----------------|
| **Message Types** | Multiple message formats | Unified ChatMessage |
| **Workflow API** | Conversation-based | Graph-based with composability |
| **Observability** | Custom implementation | Built-in OpenTelemetry |
| **Durability** | Limited checkpointing | Full workflow state management |
| **Multi-Agent** | Group chat focused | Multiple orchestration patterns |

**Key Benefits:**
- ✅ Unified message types simplify agent communication
- ✅ Graph-based workflows enable complex orchestration
- ✅ Built-in observability for production monitoring
- ✅ Stronger composability for multi-agent systems

---

## Core Features

### **Flexible Chat Client Support**
Work with multiple AI service providers through a unified interface:
- Azure OpenAI (enterprise-grade with managed identity)
- Azure AI Agent Service (fully managed with observability)
- OpenAI (direct API access)
- Azure Responses API (structured output generation)

### **Powerful Tool Integration**
Extend agent capabilities with diverse tools:
- **Hosted Tools**: Enterprise-grade tools running on Azure (Code Interpreter, File Search, Web Search)
- **Custom Functions**: Define your own tools with simple decorators
- **MCP Servers**: Connect to local or hosted Model Context Protocol servers
- **OpenAPI Integration**: Automatically integrate REST APIs

### **Advanced Multi-Agent Patterns**
Build sophisticated multi-agent systems:
- **Reflection Pattern**: Quality-driven workflows with review cycles
- **Plan-and-Execute**: Intelligent task decomposition and execution
- **Multi-Agent Collaboration**: Concurrent, sequential, and orchestrated patterns

### **Enterprise-Grade Features**
Production-ready capabilities:
- **Native Observability**: OpenTelemetry integration for monitoring and tracing
- **State Management**: Automatic thread persistence and checkpointing
- **Human-in-the-Loop**: Built-in approval workflows
- **Secure Integration**: Azure AD, managed identities, and role-based access

### **Workflow Orchestration**
Compose complex agent systems:
- **Graph-Based Workflows**: Define execution flows with dependencies
- **Checkpointing**: Resume workflows from any point
- **Error Handling**: Built-in retry and error recovery
- **Streaming Support**: Real-time output for better user experience

### **Future-Proof Architecture**
Microsoft Agent Framework is designed to adapt to advancements in AI technology. Its flexible architecture allows developers to integrate new models, tools, and orchestration patterns without extensive codebase modifications, ensuring that applications remain up-to-date with minimal effort.

---

## Getting Started

### Installation

```bash
# Install core framework
pip install agent-framework

# Install Azure integrations
pip install agent-framework[azure]

# Install OpenAI integration
pip install agent-framework[openai]

# Install all components
pip install agent-framework[all]
```

### Quick Start Example

```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

# Create chat client
chat_client = AzureOpenAIChatClient(
    model_id="gpt-4",
    endpoint="https://your-endpoint.openai.azure.com",
    api_key="your-api-key"
)

# Create agent
agent = ChatAgent(
    chat_client=chat_client,
    instructions="You are a helpful assistant.",
    name="MyAssistant"
)

# Run the agent
result = await agent.run("Hello! Tell me about agentic AI.")
print(result.text)
```

---

## Use Cases Covered in Hands-On Lab

### **Case 1: Basic Agent Creation**
- Simple agent with Azure OpenAI
- Streaming responses
- Multi-turn conversations with thread management

### **Case 2: Agents with Custom Tools**
- Custom function tools with `@ai_function` decorator
- Integration with different chat clients (Azure OpenAI, Azure AI, Responses)
- Code execution capabilities

### **Case 3: Understanding Chat Clients**
- Comparison of AzureOpenAIChatClient, AzureAIAgentClient, and AzureOpenAIResponsesClient
- Local vs. hosted code execution
- When to use each client type

### **Case 4: Enterprise Tools**
- Azure AI Search integration (HostedFileSearchTool)
- Bing Grounding for web search (HostedWebSearchTool)
- Local MCP server integration
- Hosted MCP servers with human-in-the-loop

---

## Advanced Design Patterns

The framework supports sophisticated agentic design patterns covered in detail in the design pattern labs:

### **Reflection Pattern (Adaptive RAG)**
- Worker-Reviewer cycles for quality assurance
- Intent classification and routing
- Retrieval grading and query rewriting
- Automatic quality evaluation and retry

### **Plan-and-Execute Pattern**
- Intelligent task decomposition
- Sequential and parallel workflow orchestration
- Dynamic planning with feedback adaptation
- Multi-step complex operations

### **Multi-Agent Collaboration**
- **Group Chat**: Turn-based refinement workflows
- **Concurrent Execution**: Parallel independent analysis
- **Magentic Orchestration**: Intelligent coordination for complex tasks

---

## Resources

### Official Documentation
- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry](https://ai.azure.com/)
- [API Reference](https://learn.microsoft.com/en-us/python/api/overview/azure/agent-framework)

### Learning Resources
- [Introduction Blog Post](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)
- [Code Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples)
- [Community Forum](https://github.com/microsoft/agent-framework/discussions)

---

## Hands-On Labs

Explore the complete capabilities of Microsoft Agent Framework through our comprehensive hands-on labs:

### [Basic Concepts - Getting Started](./1_basic-concept-with-msaf.ipynb)
Learn the fundamentals of Microsoft Agent Framework including:
- Core components and architecture
- Agent creation with different chat clients
- Tool integration (custom functions, hosted tools, MCP)
- Multi-turn conversations and thread management
- Enterprise features (Azure AI Search, Bing Grounding)

### [Advanced Design Patterns](../../1_agentic-design-ptn/)
Implement production-ready agentic design patterns:
- **Reflection Pattern**: Quality-driven workflows with Adaptive RAG
- **Plan-and-Execute**: Intelligent task decomposition and orchestration
- **Multi-Agent Collaboration**: Group chat, concurrent execution, and Magentic orchestration

---

## Why Choose Microsoft Agent Framework?

✅ **Unified Framework**: Best of Semantic Kernel and AutoGen in one framework  
✅ **Production-Ready**: Built-in observability, security, and durability  
✅ **Open Standards**: MCP, A2A, and OpenAPI for maximum interoperability  
✅ **Enterprise Support**: Backed by Microsoft with Azure integration  
✅ **Flexible Deployment**: Local development to cloud-scale production  
✅ **Active Development**: Regular updates with cutting-edge research  
✅ **Rich Ecosystem**: Growing community and extensive documentation  

---

## Next Steps

1. **Try the Basic Concepts Notebook**: Start with [1_basic-concept-with-msaf.ipynb](./1_basic-concept-with-msaf.ipynb)
2. **Explore Design Patterns**: Check out [Agentic Design Patterns](../../1_agentic-design-ptn/)
3. **Build Your First Agent**: Follow the quick start guide above
4. **Join the Community**: Contribute on [GitHub](https://github.com/microsoft/agent-framework)

---

*Last updated: October 14, 2025*
