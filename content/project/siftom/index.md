---
title: "Pragmatic Embodied Spoken Instruction Following in Human-Robot Collaboration with Theory of Mind"
date: 2026-01-31
summary: ICRA 2026 paper on spoken instruction following for embodied agents using theory-of-mind inference over speech, human perception, and robot goals.
aliases:
  - /projects/siftom/
tags:
  - Embodied AI
  - Theory of Mind
  - Robotics
  - Bayesian Inference
links:
  - name: Paper
    url: /publication/ying-2024-siftom/
  - name: arXiv
    url: https://arxiv.org/abs/2409.10849
---

**Publication:** ICRA 2026. The [arXiv record](https://arxiv.org/abs/2409.10849) provides the paper, full author list, and version history; the [first author's publication list](https://www.lanceying.com/) also records the conference venue.

## Research question

How can a robot infer a speaker's intended goal when spoken instructions are noisy or ambiguous?

## Method

SIFToM combines a vision-language model's symbolic descriptions of scenes, human actions, and speech with probabilistic theory-of-mind inference over collaborative goals and plans. It uses the task context to interpret ambiguous instructions.

## Evaluation and scope

Experiments use UnclearInstruct in VirtualHome and a Stretch robot in meal-preparation tasks, comparing instruction interpretation and collaboration against VLM and ablation baselines. The reported results concern these household settings; visual-to-symbolic grounding remains a source of failure.

The earlier preprint was titled **SIFToM: Robust Spoken Instruction Following through Theory of Mind**. The [publication page](/publication/ying-2024-siftom/) includes the revised arXiv v2 abstract and author list alongside the ICRA 2026 venue.
