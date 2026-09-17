---
title: 'Pragmatic Embodied Spoken Instruction Following in Human-Robot Collaboration with Theory of Mind'
summary: SIFToM combines vision-language models with probabilistic theory-of-mind inference for noisy spoken instruction following in human-robot collaboration.
abstract: |
  Spoken language instructions are ubiquitous in agent collaboration. However, in real-world human-robot collaboration, following human spoken instructions can be challenging due to various speaker and environmental factors, such as background noise or mispronunciation. When faced with noisy auditory inputs, humans can leverage the collaborative context in the embodied environment to interpret noisy spoken instructions and take pragmatic assistive actions. In this paper, we present a cognitively inspired neurosymbolic model, Spoken Instruction Following through Theory of Mind (SIFToM), which leverages a Vision-Language Model with model-based mental inference to enable robots to pragmatically follow human instructions under diverse speech conditions. We test SIFToM in both simulated environments (VirtualHome) and real-world human-robot collaborative settings with human evaluations. Results show that SIFToM can significantly improve the performance of a lightweight base VLM (Gemini 2.5 Flash), outperforming state-of-the-art VLMs (Gemini 2.5 Pro) and approaching human-level accuracy on challenging spoken instruction following tasks.
abstract_source: https://arxiv.org/abs/2409.10849v2
abstract_source_label: arXiv preprint 2409.10849v2, October 6, 2025
abstract_license: CC BY 4.0
abstract_license_url: https://creativecommons.org/licenses/by/4.0/
tags:
- Spoken instruction following
- Theory of mind
- Human-robot collaboration
- Neurosymbolic AI
- Vision-language models
- Pragmatic goal inference
research_topics:
- embodied-instruction-following
authors:
- Lance Ying
- Xinyi Li
- Shivam Aarya
- Yizirui Fang
- Yifan Yin
- Jason Xinyu Liu
- Stefanie Tellex
- Joshua B. Tenenbaum
- Tianmin Shu
date: '2026-01-31'
publishDate: '2024-10-21T05:54:14.774525Z'
publication_types:
- paper-conference
publication: '*IEEE International Conference on Robotics and Automation (ICRA 2026)*'
url_pdf: /publication/ying-2024-siftom/paper.pdf
pdf_source: https://arxiv.org/pdf/2409.10849v2
links:
- name: Project
  url: /project/siftom/
- name: arXiv
  url: https://arxiv.org/abs/2409.10849
---

How can a robot infer the intended action when a spoken instruction is corrupted by noise? SIFToM combines a vision-language model's symbolic descriptions of scenes, human actions, and speech with probabilistic theory-of-mind inference over collaborative goals and plans. This grounds ambiguous language in the task context.

Experiments use UnclearInstruct in VirtualHome and a Stretch robot in meal-preparation tasks, comparing instruction interpretation and collaboration against VLM and ablation baselines. The reported results concern these household settings; visual-to-symbolic grounding remains a source of failure. The paper connects embodied instruction following, pragmatic language understanding, and human-robot collaboration. Its earlier title, [SIFToM: Robust Spoken Instruction Following through Theory of Mind](https://arxiv.org/abs/2409.10849v1), refers to the September 2024 preprint; this page uses the revised v2 abstract and author list.

The [first author's publication list](https://www.lanceying.com/) records ICRA 2026; this page provides the arXiv v2 abstract and PDF.
