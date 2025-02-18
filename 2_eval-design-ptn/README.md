---
layout: default
title: Lab 2. Evaluation Driven Design Patterns
permalink: /2_eval-design-ptn/
has_children: true
nav_order: 6
---


# Evaluation Driven Design Patterns
Delve into evaluation-driven design for agentic AI, featuring human-in-the-loop architecture, batch evaluation with your data, tracing-based scheduling, safety evaluators, and adversarial simulator usage. Key Skills is testing and benchmarking AI agents, integrating human feedback loops, ensuring ethical and safe AI operation.


## Human-in-the-loop in agentic architecture
---

### What is multi-Agent Collaboration?
Human-in-the-loop (HITL) in agentic architecture refers to a system design approach where human oversight, intervention, or collaboration is integrated into the AI-driven process. This ensures that AI agents operate within ethical, safe, and effective boundaries, particularly in complex or high-stakes scenarios.

- **Human Oversight & Control**:
Ensures that AI decisions are reviewed, validated, or overridden by humans before execution.
Example: AI suggests business strategies, but executives make the final call.

- **Continuous Learning & Adaptation**:
AI improves over time by learning from human feedback, refining its decision-making process.
Example: Reinforcement Learning with Human Feedback (RLHF) in AI chatbots.

- **Intervention for Critical Decisions**:
In high-risk or complex situations, humans intervene to ensure accuracy and compliance.
Example: In medical AI, doctors approve diagnoses before prescribing treatments.

- **Hybrid Decision-Making**:
AI handles repetitive or high-speed tasks, while humans provide strategic oversight.
Example: AI filters job applications, but recruiters make final hiring decisions.


### Key Advantages
- **Increases Reliability & Trust**:
Reduces AI errors and builds confidence in AI-driven processes.
Ensures decisions are ethical, fair, and compliant with regulations.

- **Enhances Adaptability & Learning**:
AI continuously evolves based on human feedback, improving accuracy and performance.
Avoids rigid automation, allowing AI to adjust to new scenarios.

- **Reduces Risks & Prevents Biases**:
Human intervention helps correct AI biases and prevent unintended consequences.
Especially crucial in AI-driven hiring, medical diagnosis, and financial services.

- **Optimizes Efficiency & Productivity**:
AI accelerates routine tasks, while humans focus on higher-level strategic decisions.
Balances automation with human expertise, leading to better outcomes.


# Azure Evaluation SDK
To thoroughly assess the performance of your generative AI application when applied to a substantial dataset, you can evaluate a Generative AI application in your development environment with the Azure AI evaluation SDK. 


| Category                                | Evaluator class                                                                                                                           |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Performance and quality (AI-assisted)   | GroundednessEvaluator, GroundednessProEvaluator, RetrievalEvaluator, RelevanceEvaluator, CoherenceEvaluator, FluencyEvaluator, SimilarityEvaluator |
| Performance and quality (NLP)           | F1ScoreEvaluator, RougeScoreEvaluator, GleuScoreEvaluator, BleuScoreEvaluator, MeteorScoreEvaluator                                       |
| Risk and safety (AI-assisted)           | ViolenceEvaluator, SexualEvaluator, SelfHarmEvaluator, HateUnfairnessEvaluator, IndirectAttackEvaluator, ProtectedMaterialEvaluator        |
| Composite                               | QAEvaluator, ContentSafetyEvaluator                                                                                                       |

### Performance and Quality Evaluators

#### AI-assisted Evaluators:
GroundednessEvaluator: Assesses the accuracy of responses based on provided context.
GroundednessProEvaluator: Similar to GroundednessEvaluator but uses Azure AI Content Safety.
RetrievalEvaluator: Evaluates the effectiveness of retrieval-augmented generation.
RelevanceEvaluator: Measures how relevant the response is to the query.
CoherenceEvaluator: Checks the logical flow and consistency of the response.
FluencyEvaluator: Evaluates the grammatical correctness and naturalness of the response.
SimilarityEvaluator: Measures the similarity between generated responses and ground truth.

#### NLP Evaluators:
F1ScoreEvaluator: Calculates the F1 score for precision and recall.
RougeScoreEvaluator: Measures overlap with reference texts using ROUGE metrics.
GleuScoreEvaluator: Evaluates using GLEU score.
BleuScoreEvaluator: Uses BLEU score for evaluating machine translations.
MeteorScoreEvaluator: Measures using METEOR score.


### Risk and Safety Evaluators
#### AI-assisted Evaluators:
ViolenceEvaluator: Detects violent content.
SexualEvaluator: Identifies sexually explicit content.
SelfHarmEvaluator: Detects content related to self-harm.
HateUnfairnessEvaluator: Identifies hate speech and unfair content.
IndirectAttackEvaluator: Evaluates vulnerability to indirect attack jailbreaks.
ProtectedMaterialEvaluator: Detects protected material.

#### Composite Evaluators:
QAEvaluator: Combines multiple quality evaluators for comprehensive assessment.
ContentSafetyEvaluator: Combines multiple safety evaluators for overall safety assessment.