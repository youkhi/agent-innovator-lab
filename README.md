# Agent Innovator Lab

The Agent Innovator Lab is designed to provide a structured learning experience for AI agent development by leveraging Microsoft Azure's core services (Data & AI, App, and Infra). Each lab focuses on a specific topic, covering areas such as search algorithm optimization, agentic design patterns, and evaluation frameworks. Through this hands-on workshop, participants will gain practical experience in building, optimizing, and evaluating Azure-based AI agents, ultimately driving innovation and enhancing real-world AI system deployment.
This repository includes RAG best practices, along with tools and techniques for innovating current architecture. 


This hands-on lab is suitable for the following purposes:

1. 1-day workshop (4-7 hours depending on customer)
2. Hackathon starter code
3. Reference guide for Evaluation-driven Multi-Agent design patterns


[**Hands-on guide**](https://azure.github.io/agent-innovator-lab/) | [**Requirements**](#requirements) | [**Get started**](#get-started) 

----------------------------------------------------------------------------------------

## List of workshops

Provided below is a list of currently published modules:

| Title  | Description and Link  |
|-------|-----|
| Lab 0. Basic RAG | [Create RAG application with Azure AI Search](0_basic-rag)  |
| Lab 0. Basic Agent | [Basic Concepts of Agent and Agent toolkits (AutoGen and LangGraph)](0_basic-agent) |
| Lab 1. Agentic Design Pattern | [Practice representative patterns of Agentic RAG](1_agentic-design-ptn) |
| Lab 2. Evaluation Design Pattern | [Practice the Evaluation-Driven RAG patterns](2_eval-design-ptn) |
| Lab 3. Optimization Design Pattern | [(In development) Practice the Optimization Design patterns](3_optimization-design-ptn)   |
| Lab Intermission. Agentic Workflow Design Lab | [Design Agentic Workflow before each hands-on session ](lab_intermission) |
 

## Requirements
Before starting, you should meet the following requirements:

- [Access to Azure OpenAI Service](https://go.microsoft.com/fwlink/?linkid=2222006)
- [Azure AI Foundry getting started](https://int.ai.azure.com/explore/gettingstarted): Need to create a project
- [Access to Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [Access to Azure Bing Search](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource)

- ***[Evaluation driven design pattern]*** Need to grant ***Storage Blob Data Contributor*** at the storage of AI Foundry role to user, group, service principle and managed Identity which you are trying to access the data executing evaluators in cloud.

- ***[Evaluation driven design pattern - custom evaluator]*** Need to access ***Azure ML*** and ***Storage Account*** to upload your custom evaluators and data.

- In order to run ***azure.ai.evaluation.evaluate***, ***Azure CLI*** installed and you are logged into your Azure account by running ***az login***.


**Please do not forget to modify the `.env` file to match your account. Rename `sample.env` to `.env` or copy and use it**

## Get started

### If you are using your own local 
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Set up your environment
git clone https://github.com/Azure/agent-innovator-lab.git

cd agent-innovator-lab 

pip install -r requirements.txt


```

### If you are using Azure ML Compute Instance
```bash
conda create -n venv_agentlab python=3.11

# Set up your environment
git clone https://github.com/Azure/agent-innovator-lab.git

cd agent-innovator-lab 

pip install -r requirements.txt
```

## 🔥 New Feature (10-Apr-2025)

### Prompt Optimization using PromptWizard<br>
- This hands-on demonstrates how to optimize prompts using PromptWizard. PromptWizard, released as open source and paper by Microsoft, is a prompt optimization tool for maximizing the performance of LLM. It is a prompt optimization framework that employs a self-evolving mechanism in which LLM generates, critiques, refines, and continuously improves prompts and examples through feedback and synthesis
- <a href="https://github.com/Azure/agent-innovator-lab/tree/main/3_optimization-design-ptn/03_prompt-optimization">Go to notebook</a>

### Semantic Kernel hands-on lab<br>
- This hands-on demonstrates how to use Semantic Kernel (SK) to build a simple agentic application.
- The lab covers the following topics:
    - Core concepts and architecture of Semantic Kernel (SK)
- Agent implementation examples:
    - Azure AI Agent, Azure Assistant Agent, Chat Completion Agent, Azure Responses Agent
- Tool and connector integration:
    - Azure AI Search, File Tool, Bing Search API via Bing Search Connector, Bing Grounding Tool, Azure Evaluation SDK 
- How to build a simple agentic application using SK, leveraging various agentic design patterns (e.g. Corrective / Adaptive RAG)
- You can also leverage existing evaluation design patterns and optimization design patterns to evaluate and optimize your Semantic Kernel application.
  <a href="https://github.com/Azure/agent-innovator-lab/blob/main/0_basic-agent/SK/1_basic-concept-with-sk.ipynb">Go to notebook</a>


## Trouble Shooting

### EvaluationException: (UserError) Failed to connect to your Azure AI project. Please check if the project scope is configured correctly, and make sure you have the necessary access permissions. Status code: 401.
- run `az login`. To set up your tenant scope, try the option `--scope https://graph.microsoft.com//.default`
- For example, `az login --scope https://graph.microsoft.com//.default`

### azure_ai_project evaluationexception: (internalerror) azure ml managed identity configuration not found in environment. invalid_scope
- Check the managed identity role that your compute instance has. You can create a **compute instance on Azure AI Foundry (not on Azure ML)** to avoid the complex identity setup. 

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
