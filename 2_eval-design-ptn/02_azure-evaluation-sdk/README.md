---
layout: default
title: Azure Evaluation SDK
permalink: /2_eval-design-ptn_02_azure-evaluation-sdk/
parent: Lab 2. Evaluation Driven Design Patterns
nav_order: 6.2
---

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