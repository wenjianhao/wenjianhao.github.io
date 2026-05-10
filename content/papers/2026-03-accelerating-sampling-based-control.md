---
title: "Accelerating Sampling-Based Control via Learned Linear Koopman Dynamics"
date: 2026-03-01
author: "W Hao, Y Fang, Z Lu, S Mou"
paper_group: "Learning-Based Control for Robotics"
paper_order: 20
summary: "This paper presents an efficient MPPI control framework using learned linear Koopman dynamics to reduce rollout cost while maintaining control performance."
media: "/papers/media/accelerating-sampling-based-control.gif"
media_alt: "Accelerating sampling-based control robot motion animation"
---

---

- [Paper](https://arxiv.org/pdf/2603.05385)
- [Code and data](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=SQ2BSVsAAAAJ&citation_for_view=SQ2BSVsAAAAJ:kNdYIx-mwKoC)

---

##### Abstract

This paper presents an efficient model predictive path integral (MPPI) control framework for systems with complex nonlinear dynamics. To improve the computational efficiency of classic MPPI while preserving control performance, we replace nonlinear trajectory propagation with a learned linear deep Koopman operator model. The resulting controller is validated in simulation and hardware experiments, showing near-MPPI performance with substantially lower computational cost for real-time robotic control.

---

##### Demo

<video controls muted loop playsinline preload="metadata" style="display: block; width: 100%; max-width: 760px; height: auto; border-radius: 8px; margin: 18px auto;">
  <source src="/papers/media/mppi-dk.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

##### Citation

Hao, Wenjian, Yuxuan Fang, Zehui Lu, and Shaoshuai Mou. 2026. "Accelerating Sampling-Based Control via Learned Linear Koopman Dynamics." arXiv preprint arXiv:2603.05385.

```latex
@techreport{WHao2026accelera,
  author = {W Hao, Y Fang, Z Lu, S Mou},
  year = {2026},
  title = {Accelerating Sampling-Based Control via Learned Linear Koopman Dynamics},
  number = {arXiv:2603.05385},
  url = {https://arxiv.org/pdf/2603.05385}
}
```
