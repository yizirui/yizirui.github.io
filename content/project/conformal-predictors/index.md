---
title: Investigating Data Usage for Inductive Conformal Predictors
date: 2024-06-18
summary: Studying how data allocation choices affect inductive conformal prediction, calibration behavior, and uncertainty guarantees.
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

**Publication status:** arXiv preprint, first submitted June 18, 2024. [Read the source and version history](https://arxiv.org/abs/2406.12262).

## Research question

How should limited development data be allocated between training and calibration, and what happens when those sets overlap?

## Method

The experiments use an inductive conformal predictor around a neural-network classifier on Covtype. They vary training/calibration allocation, development-set size, and overlap, using repeated randomized splits to examine coverage and prediction-set size.

## Results and scope

Small calibration sets can increase variability. Overlapping training and calibration data can produce smaller prediction sets at the cost of undercoverage. These empirical findings concern one classification dataset; they do not establish a universally optimal split or validate overlapping calibration data in general.
