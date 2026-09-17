---
title: Learning to Defer with an Uncertain Rejector via Conformal Prediction
summary: NeurIPS 2024 workshop paper on conformal uncertainty sets for learning-to-defer rejectors, with abstention and human-model consensus on object and hate-speech detection tasks.
abstract: |
  Learning to defer (L2D) allows prediction tasks to be allocated to a human or machine decision maker, thus getting the best of both’s abilities. Yet this allocation decision depends on a ‘rejector’ function, which could be poorly fit or otherwise misspecified. In this work, we perform uncertainty quantification for the rejector sub-component of the L2D framework. We use conformal prediction to allow the reject to output sets, instead of just the binary outcome of ‘defer’ or not. On tasks ranging from object to hate speech detection, we demonstrate that the uncertainty in the rejector translates to safer decisions via two forms of selective prediction.
abstract_source: https://openreview.net/pdf?id=TWb9y4PNSW
abstract_source_label: NeurIPS 2024 Workshop on Bayesian Decision-making and Uncertainty paper, page 1
publication_date: '2024'
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
date: '2024-12-01'
publishDate: '2024-10-21T05:54:14.768200Z'
publication_types:
- paper-conference
publication: '*NeurIPS 2024 Workshop on Bayesian Decision-making and Uncertainty*'
url_pdf: https://openreview.net/pdf?id=TWb9y4PNSW
links:
- name: Workshop
  url: https://openreview.net/forum?id=TWb9y4PNSW
---

## Research question

Can uncertainty about the rejector improve decision making in learning-to-defer systems, where each input is assigned to either a model or a human expert?

## Approach and evidence

This workshop paper uses conformal prediction to make the rejector return sets rather than a single defer-or-predict decision. It evaluates two responses to ambiguous routing: withholding the prediction and checking agreement between the human and model. The reported experiments cover tasks ranging from object to hate-speech detection. The [workshop PDF](https://openreview.net/pdf?id=TWb9y4PNSW) contains the original method and results.

## Scope and versions

The paper focuses on multiclass learning to defer with one expert. Its selective workflows can abstain or consult both decision makers, so their behavior includes decisions that are withheld as well as those returned. This is the NeurIPS 2024 Workshop on Bayesian Decision-making and Uncertainty version. The subsequent [TMLR 2026 article](/publication/fang-2026-learning-tmlr/) has a separate abstract, review record, and citation.
