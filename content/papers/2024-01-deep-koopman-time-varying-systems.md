---
title: "Deep Koopman learning of nonlinear time-varying systems"
date: 2024-01-01
author: "W Hao, B Huang, W Pan, D Wu, S Mou"
paper_group: "Dynamics Learning for Complex Systems"
paper_order: 50
summary: "This paper proposes deep Koopman learning for nonlinear time-varying systems with error analysis and computationally efficient prediction."
venue: "Automatica 2024"
media: "/papers/media/deep-koopman-time-varying-systems.gif"
media_alt: "Deep Koopman learning time-varying systems gamma comparison animation"
home_media: "/papers/media/time-varying-koopman-tracking-white.gif"
home_media_alt: "Recorded one-step Deep Koopman predictions (circles) against the true states (line) as the fast-varying system evolves, gamma = 6."
---

---

- [Paper](https://www.sciencedirect.com/science/article/pii/S0005109823005381)
- [Code and data](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=SQ2BSVsAAAAJ&citation_for_view=SQ2BSVsAAAAJ:2osOgNQ5qMEC)

---

##### Abstract

This paper presents a data-driven approach that approximates nonlinear time-varying dynamics by linear time-varying Koopman models learned with deep neural networks. It provides approximation-error analysis between original and lifted dynamics and demonstrates small prediction errors even under rapid system changes. Quadcopter simulations further show strong computational efficiency for control-oriented modeling.

---

##### Demo

For the fast-varying case (γ = 6), the circles show the model's one-step predictions. The solid line shows the observed state at the same simulation step.

<video controls muted loop playsinline preload="none" width="720" height="520" poster="/papers/media/time-varying-koopman-tracking.jpg" aria-label="Recorded state and one-step prediction for both state variables" style="display:block; width:100%; max-width:720px; height:auto; margin:18px auto;">
  <source src="/papers/media/time-varying-koopman-tracking.mp4" type="video/mp4">
</video>

Full comparison across both rates of change, including prediction errors:

<video controls muted loop playsinline preload="none" poster="/papers/media/gamma-comparison-web.jpg" style="display: block; width: 100%; max-width: 760px; height: auto; border-radius: 8px; margin: 18px auto;">
  <source src="/papers/media/gamma-comparison-web.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

##### Citation

Hao, Wenjian, Bowen Huang, Wei Pan, Di Wu, and Shaoshuai Mou. 2024. "Deep Koopman learning of nonlinear time-varying systems." Automatica 159:111372.

```latex
@article{WHao2024deepkoop,
  author = {W Hao, B Huang, W Pan, D Wu, S Mou},
  year = {2024},
  title = {Deep Koopman learning of nonlinear time-varying systems},
  journal = {Automatica 159:111372},
  url = {https://www.sciencedirect.com/science/article/pii/S0005109823005381}
}
```
