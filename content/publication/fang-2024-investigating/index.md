---
title: Investigating Data Usage for Inductive Conformal Predictors
summary: How training/calibration splits and overlap affect coverage validity and prediction-set size in inductive conformal classification.
abstract: |
  Inductive conformal predictors (ICPs) are algorithms that are able to generate prediction sets, instead of point predictions, which are valid at a user-defined confidence level, only assuming exchangeability. These algorithms are useful for reliable machine learning and are increasing in popularity. The ICP development process involves dividing development data into three parts: training, calibration and test. With access to limited or expensive development data, it is an open question regarding the most efficient way to divide the data. This study provides several experiments to explore this question and consider the case for allowing overlap of examples between training and calibration sets. Conclusions are drawn that will be of value to academics and practitioners planning to use ICPs.
abstract_source: https://arxiv.org/abs/2406.12262v1
abstract_source_label: arXiv preprint 2406.12262v1, June 18, 2024
abstract_license: CC BY-NC-ND 4.0
abstract_license_url: https://creativecommons.org/licenses/by-nc-nd/4.0/
tags:
- Inductive conformal prediction
- Calibration sets
- Data splitting
- Marginal coverage
- Uncertainty quantification
- Neural networks
research_topics:
- conformal-prediction
authors:
- Yizirui Fang
- Anthony Bellotti
date: '2024-06-18'
publishDate: '2024-09-03T06:08:44.694714Z'
publication_types:
- manuscript
publication: '*arXiv preprint arXiv:2406.12262*'
url_pdf: /publication/fang-2024-investigating/paper.pdf
pdf_source: https://arxiv.org/pdf/2406.12262v1
doi: 10.48550/arXiv.2406.12262
links:
- name: arXiv
  url: https://arxiv.org/abs/2406.12262
---

How should limited development data be divided between training and calibration for inductive conformal prediction? This study examines the tradeoff between coverage validity and predictive efficiency, measured through prediction-set size, when calibration data are scarce or overlap with training data.

The experiments wrap an artificial neural network with an inductive conformal predictor on the multiclass Covtype dataset. They vary training/calibration allocation, development-set size, and overlap, repeating randomized splits to examine variability. Small calibration sets can increase variability, while training/calibration overlap can produce smaller prediction sets at the cost of undercoverage. These are empirical findings from one classification dataset; they do not establish a universally optimal split or validate overlapping calibration data in general.
