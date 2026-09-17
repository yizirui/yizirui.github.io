---
title: Learning to Defer with an Uncertain Rejector via Conformal Prediction
summary: Conformal prediction quantifies uncertainty in learning-to-defer rejectors, enabling abstention and human-model consensus workflows for image and hate-speech classification.
abstract: |
  Learning to defer (L2D) aims to optimize human-AI collaboration by allocating prediction tasks to either a machine learning model or a human expert, depending on which is most likely to be correct. This allocation decision is governed by a rejector: a meta-model that routes inputs based on estimated success probabilities. In practice, a poorly fit or otherwise misspecified rejector can jeopardize the entire L2D workflow due to its crucial role in allocating prediction tasks. In this work, we perform uncertainty quantification for the rejector. We use conformal prediction to allow the rejector to output prediction sets or intervals instead of just the binary outcome of ‘defer’ or not. On tasks ranging from image to hate speech classification, we demonstrate that the uncertainty in the rejector translates to safer decisions via two forms of selective prediction.
abstract_source: https://openreview.net/pdf?id=SZQJ8K2DUe
abstract_source_label: TMLR published article, February 2026, page 1
publication_date: '2026-02'
tags:
  - Learning to Defer
  - Conformal Prediction
  - Uncertainty Quantification
  - Human-AI Collaboration
  - Selective Prediction
  - Abstention
research_topics:
  - human-ai-decision-making
authors:
- Yizirui Fang
- Eric Nalisnick
date: '2026-02-01'
publishDate: '2026-02-01T00:00:00Z'
publication_types:
- article-journal
publication: '*Transactions on Machine Learning Research (TMLR)*'
url_pdf: https://openreview.net/pdf?id=SZQJ8K2DUe
links:
- name: Project
  url: /project/uncertain-defer/
- name: TMLR
  url: https://openreview.net/forum?id=SZQJ8K2DUe
- name: Code
  url: https://github.com/yizirui/conformal_L2D
---

## Research question

How should a human-AI system act when its learned routing function is itself uncertain about whether the model or human should make a prediction?

## Approach and evidence

The paper applies conformal prediction to the rejector, replacing a forced binary decision with prediction sets or intervals. It studies two selective workflows: abstaining when the allocation is uncertain, and querying both decision makers to check agreement. Experiments span image and hate-speech classification. The [published paper](https://openreview.net/pdf?id=SZQJ8K2DUe) and [research code](https://github.com/yizirui/conformal_L2D) document the methods and evaluation.

## Scope and versions

The uncertainty estimate concerns assignment of responsibility between a model and an expert. Abstention withholds a prediction; consensus checking requires both predictions, so these workflows change which decisions are made and when the expert is consulted. This is the February 2026 TMLR article; the [NeurIPS 2024 workshop paper](/publication/fang-2024-learning-workshop/) is an earlier version of the same research.
