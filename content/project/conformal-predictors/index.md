---
title: Investigating Data Usage for Inductive Conformal Predictors
date: 2024-06-01
summary: Studying how data allocation choices affect inductive conformal prediction, calibration behavior, and uncertainty guarantees.
external_link: https://arxiv.org/abs/2406.12262
tags:
  - Conformal Prediction
  - Uncertainty Quantification
  - Calibration
  - Robust ML
links:
  - name: Paper
    url: /publication/fang-2024-investigating/
  - name: arXiv
    url: https://arxiv.org/abs/2406.12262
---

## Hiring-manager view

This paper is a direct uncertainty-quantification signal: it studies the data and calibration choices behind conformal prediction rather than treating uncertainty estimates as a black box.

## Scientific problem

Inductive conformal predictors rely on data splits and calibration sets to produce uncertainty-aware prediction sets. The practical question is how data usage decisions affect validity, efficiency, and downstream model behavior.

## Method

- Investigated how data allocation choices influence inductive conformal prediction.
- Focused on calibration behavior, data efficiency, and prediction-set quality.
- Connected empirical model behavior to uncertainty guarantees relevant to safety-sensitive ML systems.

## Evaluation signal

The evaluation centers on how calibration and data usage choices change uncertainty quality and reliability, especially when model outputs must support downstream decisions.
