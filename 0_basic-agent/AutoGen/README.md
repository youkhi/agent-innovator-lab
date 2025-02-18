---
layout: default
title: Basic of Agent - AutoGen
permalink: /0_basic-agent_AutoGen/
parent: Lab 0. Building a Basic Agent
nav_order: 2.1
---


# AutoGen

---

Microsoft AutoGen is an open-source toolkit for building autonomous multi-agent systems. It provides a flexible and scalable framework for creating agent-based applications that can interact, collaborate, and learn from each other. AutoGen simplifies the development of complex agent architectures by offering high-level abstractions, predefined agent types, and communication patterns, enabling developers to focus on agent behaviors and interactions.

Microsoft AutoGen offers two primary APIs: **AgentChat** and **Core**. Each serves distinct purposes and caters to different levels of application complexity and control. Below is a comparison of their key features:

| Aspect               | AgentChat                                                                                                                                                 | Core                                                                                                                                                       |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Purpose**          | Provides a high-level framework for building interactive agent applications with preset agents, facilitating quick development.                           | Offers a foundational, unopinionated, and flexible API for creating scalable, event-driven agent workflows, granting developers full control over agent behaviors and interactions. |
| **Complexity**       | Simplifies development by offering predefined agents and configurations, making it suitable for straightforward applications.                            | Requires more detailed setup and configuration, ideal for complex applications needing customized agent behaviors and interactions.                        |
| **Customization**    | Allows for some customization through preset agents and configurations but is primarily designed for rapid application development.                      | Enables extensive customization, allowing developers to define unique agent types, message handlers, and communication patterns tailored to specific application needs. |
| **Scalability**      | Suitable for applications with a limited number of agents and simpler interaction patterns.                                                              | Designed to support scalable applications, capable of managing numerous agents with complex interaction patterns, including distributed deployments.         |
| **Use Cases**        | Ideal for quickly setting up applications that require basic agent interactions, such as simple chatbots or assistants.                                 | Best suited for applications that demand intricate agent workflows, advanced message routing, and fine-grained control over agent lifecycles, such as large-scale multi-agent systems. |
| **Learning Curve**   | Lower learning curve due to high-level abstractions and preset configurations, enabling faster development.                                              | Steeper learning curve owing to its foundational nature, requiring a deeper understanding of agent-based architectures and event-driven programming.         |
| **Integration**      | Integrates with the Core API, utilizing its runtime environment for message handling and agent management, but abstracts many complexities.              | Serves as the underlying framework upon which AgentChat is built, providing the essential components for agent communication, lifecycle management, and message routing. |
| **Examples**         | Creating a simple assistant agent that can perform tasks using predefined tools.                                                                         | Implementing a distributed multi-agent system where agents have specialized roles and communicate through custom message types and handlers.                |

### [Hands-On](1_basic-concept-with-autogen-studio.ipynb)