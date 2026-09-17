---
title: Research
summary: Research by Yizirui Fang on uncertainty-aware human–AI decisions, conformal prediction, embodied instruction following, and AI-assisted education.
date: 2026-09-17
---

My research examines uncertainty in human–AI decisions, conformal calibration, embodied instruction following, and AI-assisted education.

## Human–AI decision making: uncertain rejectors in learning to defer

**Research question:** What should a learning-to-defer system do when the component deciding between a model and a human expert is itself uncertain?

[Learning to Defer with an Uncertain Rejector via Conformal Prediction — TMLR 2026](/publication/fang-2026-learning-tmlr/) applies conformal prediction to the rejector that assigns inputs to a model or a human expert. Its uncertainty sets support selective workflows, including abstention and checking agreement between both decision makers. The evaluation concerns classification tasks with model and expert outputs.

The [NeurIPS 2024 workshop paper](/publication/fang-2024-learning-workshop/) is an earlier version of the same research, studying abstention and human-model consensus.

## Conformal prediction: training and calibration data allocation

**Research question:** Can training and calibration sets share data, and how does their allocation affect an inductive conformal predictor?

[Investigating Data Usage for Inductive Conformal Predictors](/publication/fang-2024-investigating/) studies training/calibration splits, data reuse through overlapping sets, and their effects on coverage and prediction-set size. Its experiments use a neural-network classifier on Covtype. Smaller prediction sets from overlapping data can come at the cost of undercoverage. The findings in this arXiv preprint concern one classification dataset and do not establish a universally optimal split.

## Embodied instruction following: noisy speech and theory of mind

**Research question:** How can a robot infer an intended goal when spoken instructions are noisy or ambiguous?

[Pragmatic Embodied Spoken Instruction Following in Human-Robot Collaboration with Theory of Mind](/publication/ying-2024-siftom/) combines vision-language models with theory-of-mind inference to interpret speech in a collaborative task context. Experiments examine instruction following in VirtualHome and real-world human–robot collaboration. The earlier preprint was titled **SIFToM: Robust Spoken Instruction Following through Theory of Mind**; the linked record includes the revised arXiv v2 abstract and lists the ICRA 2026 venue.

## Human-centered AI: transparent instructional design

**Research question:** How can AI support instructional design while keeping educators involved in the decisions?

[ARCHED: A Human-Centered Framework for Transparent, Responsible, and Collaborative AI-Assisted Instructional Design](/publication/li-2024-arched/) separates learning-objective generation from analysis while retaining educator control. Its evaluation examines objective quality, alignment with Bloom's taxonomy, and preliminary expert feedback. The evidence concerns instructional-design support; classroom learning gains and broad adoption outcomes were not established.

## Papers and projects

- [All publication records](/publication/)
- [Structured paper catalog with complete abstracts](/papers.json)
- [Project explanations and public artifacts](/projects/)
