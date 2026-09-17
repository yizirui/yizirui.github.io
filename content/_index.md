---
# Leave the homepage title empty to use the site title
title: ""
date: 2026-09-16
lastmod: 2026-09-17
summary: "Yizirui (Easey) Fang: Amazon SDE and applied ML researcher working on reliable LLM agents, embodied AI, conformal prediction, and human-AI collaboration. Explore projects, papers, and public evidence."
seo:
  title: 'Yizirui Fang | LLM Agents, Embodied AI & Uncertainty'
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Archived Academic CV
        url: uploads/Yizirui_Fang_PhD_CV_EmbodiedAI.pdf
    design:
      css_class: dark
      background:
        color: black
        image:
          # Add your image background to `assets/media/`.
          filename: stacked-peaks.svg
          filters:
            brightness: 1.0
          size: cover
          position: center
          parallax: false
  - block: collection
    id: projects
    content:
      title: Selected Machine Learning Projects
      text: "Research in uncertainty-aware decisions, embodied AI, and human–AI collaboration, with related papers and code."
      filters:
        folders:
          - project
    design:
      view: article-grid
      fill_image: false
      columns: 3
  - block: collection
    id: papers
    content:
      title: Papers and Abstracts
      text: "Papers on learning to defer, conformal prediction, embodied instruction following, and human-centered AI. Explore the [research themes](/research/)."
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      view: citation
  # - block: collection
  #   id: talks
  #   content:
  #     title: Recent & Upcoming Talks
  #     filters:
  #       folders:
  #         - event
  #   design:
  #     view: article-grid
  #     columns: 1
  # - block: collection
  #   id: news
  #   content:
  #     title: Recent News
  #     subtitle: ''
  #     text: ''
  #     # Page type to display. E.g. post, talk, publication...
  #     page_type: post
  #     # Choose how many pages you would like to display (0 = all pages)
  #     count: 5
  #     # Filter on criteria
  #     filters:
  #       author: ""
  #       category: ""
  #       tag: ""
  #       exclude_featured: false
  #       exclude_future: false
  #       exclude_past: false
  #       publication_type: ""
  #     # Choose how many pages you would like to offset by
  #     offset: 0
  #     # Page order: descending (desc) or ascending (asc) date.
  #     order: desc
  #   design:
  #     # Choose a layout view
  #     view: date-title-summary
  #     # Reduce spacing
  #     spacing:
  #       padding: [0, 0, 0, 0]
---
