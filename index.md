---
layout: home
title: Agent Innovator Lab (Korean)
nav_order: 1
permalink: /
---
# Agent Innovator Lab
{: .no_toc }

[Requirements](#requirements){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub](https://github.com/Azure/agent-innovator-lab){: .btn .fs-5 .mb-4 .mb-md-0 }

# Agent Innovoator Lab

Agent Innovator Lab은 화이트보딩과 핸즈온을 통해 프로덕션 런칭에 필요한 에이전트 설계 패턴, 평가 중심 방법론을 같이 고민하고 체험하는 1-day 워크숍입니다. 기존 핸즈온과 달리 코드베이스 일방향 진행이 아니라 (고객마다 적용할 에이전트 패턴이 다르고 목표도 다르고 에이전트 프레임워크도 다르기 때문입니다.) 브레인스토밍 및 화이트보딩 세션을 진행하게 됩니다.


1. 1-day workshop (4-7 hours depending on customer)
2. Hackathon starter code
3. Reference guide for RAG/Multi-Agent design patterns

[**Requirements**](#requirements) | [**Get started**](#get-started) 

----------------------------------------------------------------------------------------

## List of workshops

Agent Innovator Lab은 현재 5개의 핸즈온을 제공하고 있습니다. 각 핸즈온은 아래와 같은 주제를 다루고 있습니다.:

| Title  | Description and Link  |
|-------|-----|
| Lab 0. Basic RAG | [Azure AI Search기반 기본 RAG 환경 설정](https://github.com/Azure/agent-innovator-lab/tree/main/0_basic-rag)  |
| Lab 0. Basic Agent | [기본 에이전트 체험 (SK, AutoGen, LangGraph)](https://github.com/Azure/agent-innovator-lab/tree/main/0_basic-agent) |
| Lab 1. Agentic Design Pattern | [4가지 주요 에이전틱 패턴인 Reflection, Tool Usage, Planning, and Multi-Agent Systems을  톺아보기](https://github.com/Azure/agent-innovator-lab/tree/main/1_agentic-design-ptn) |
| Lab 2. Evaluation Design Pattern | [Evaluation-driven 핸즈온을 통해 1회성 개발이 아닌 평가 파이프라인을 구축](https://github.com/Azure/agent-innovator-lab/tree/main/2_eval-design-ptn)  |
| Lab 3. Optimization Design Pattern | [cache, prompt, 메모리 관리 등 특정 영역 최적화 실험](https://github.com/Azure/agent-innovator-lab/tree/main/2_eval-design-ptn)  |
| Lab Intermission. Agentic Workflow Design Lab | [에이전틱 패턴 화이트보딩](lab_intermission) |


## 사전 준비 사항
시작하기 전 아래의 요구 사항을 충족해야 합니다.:

### 접근 및 테스트해야 할 URL
1. Azure OpenAI Service 액세스: https://go.microsoft.com/fwlink/?linkid=2222006
2. Azure AI Foundry Getting Started (AI Foundry 프로젝트 생성): https://int.ai.azure.com/explore/gettingstarted
3. 필수 설정 및 권한 부여 필요 사항
- 환경 변수 수정 (.env 파일 적용 필요)
4. Agent Innovator Lab 기본 코드 수행
- https://github.com/Azure/agent-innovator-lab/blob/main/0_basic-agent/SK/1_basic-concept-with-sk.ipynb
- https://github.com/Azure/agent-innovator-lab/blob/main/2_eval-design-ptn/02_azure-evaluation-sdk/01.2_batch-eval-with-your-data.ipynb
 
## Agentic Architecture 고도화 필수 원칙
- 처음부터 전체 데이터를 넣지 않고 소규모(50~100건) 데이터로 실험
- 점진적으로 200건 → 전체 데이터로 확장
- 단계별 실험 후 확장
- 튜닝 방식:
    - RAG 구성
    - Evaluation-Driven Design Pattern 적용 (Human-in-the-loop 활용)
    - Intent classification포함한 Agentic Design Pattern 적용
    - 핵심 Task별 개발/고도화
    - Tracing, cache를 활용한 구간별 최적화
    - content safety 및 cost control
    - 답변 품질과 응답속도 사이 의 trade-off 고려

### 로컬환경
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

### Azure ML Compute Instance
```bash
conda create -n venv_agentlab python=3.11

# Set up your environment
git clone https://github.com/Azure/agent-innovator-lab.git

cd agent-innovator-lab 

pip install -r requirements.txt
```


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
