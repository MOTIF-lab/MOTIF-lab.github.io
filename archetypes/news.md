---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
date_precision: day            # day | month (month when only the month is known)
draft: true
category: "Accepted paper"     # Accepted paper | Preprint | Award | Media | Milestone  (data/news_categories.yaml)
description: ""
external: []                   # - {label: "…", outlet: "arXiv", url: "https://…", date: 2026-01-01}
links: []                      # - {label: "Project page", url: "/projects/…/"}
image: ""                      # assets path, e.g. img/news/…jpg (processed by partials/img.html)
---
