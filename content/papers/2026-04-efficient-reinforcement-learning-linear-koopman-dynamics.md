---
title: "Efficient Reinforcement Learning using Linear Koopman Dynamics for Nonlinear Robotic Systems"
date: 2026-04-01
author: "W Hao, Y Fang, Z Lu, S Mou"
paper_group: "Learning-Based Control for Robotics"
summary: "This paper presents an online model-based reinforcement learning framework that combines learned linear Koopman dynamics with actor-critic policy optimization for efficient control of nonlinear robotic systems."
---

---

- [Paper](https://arxiv.org/pdf/2604.19980)

---

##### Abstract

This paper presents an online model-based reinforcement learning framework for optimal closed-loop control of nonlinear robotic systems with unknown dynamics. The method learns linear lifted dynamics using Koopman operator theory and integrates the resulting model into an actor-critic architecture, where policy gradients are estimated using one-step predictions rather than multi-step model rollouts. This design improves sample efficiency, reduces computational cost, and mitigates model rollout error accumulation. The framework is evaluated on multiple simulated nonlinear control benchmarks and real-world robotic platforms, including a Kinova Gen3 robotic arm and a Unitree Go1 quadruped.

---

##### Demo

Demo coming soon.

---

##### Citation

Hao, Wenjian, Yuxuan Fang, Zehui Lu, and Shaoshuai Mou. 2026. "Efficient Reinforcement Learning using Linear Koopman Dynamics for Nonlinear Robotic Systems." arXiv preprint arXiv:2604.19980.

```latex
@techreport{WHao2026efficient,
  author = {W Hao, Y Fang, Z Lu, S Mou},
  year = {2026},
  title = {Efficient Reinforcement Learning using Linear Koopman Dynamics for Nonlinear Robotic Systems},
  number = {arXiv:2604.19980},
  url = {https://arxiv.org/pdf/2604.19980}
}
```
