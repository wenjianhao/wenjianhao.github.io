---
title: "Koopman Model-Based Reinforcement Learning"
date: 2026-11-10
author: "W Hao, PC Heredia, S Mou"
paper_group: "Learning-Based Control for Robotics"
paper_order: 5
summary_from_abstract: true
media: "/papers/media/koopman-mbrl-outdoor-preview.gif"
media_natural: true
media_alt: "Front and rear views of a quadruped walking outdoors on its hind feet"
---

- [Paper](https://arxiv.org/pdf/2611.14186)
- [arXiv record](https://arxiv.org/abs/2611.14186)

---

##### Abstract

We propose a Koopman model-based reinforcement learning (K-MBRL) algorithm for controlling nonlinear robotic systems with unknown dynamics. The K-MBRL learns a control policy by minimizing an approximate policy objective that combines the analytical immediate cost with an estimate of the future cost evaluated at the one-step predicted state. To this end, we develop a stochastic Koopman operator-based learning method to approximate the unknown nonlinear dynamics in a linear representation, while a critic function estimates the remaining future cost. This formulation offers two key advantages. First, the linear Koopman dynamics simplify the model-dependent policy gradient computation to a constant matrix product, enabling computationally efficient policy improvement. Second, one-step model propagation mitigates the accumulation of prediction errors associated with long-horizon rollouts while retaining long-term cost information through the critic. The learned policy enables real-time control through feedforward evaluation without online optimization. We establish policy learning convergence guarantees under standard stochastic approximation assumptions. Simulations on HalfCheetah and quadruped four-legged locomotion tasks demonstrate strong sample efficiency and improved performance compared with classical model-free and model-based reinforcement learning baselines. A pendulum swing-up task is used to assess policy gradient approximation accuracy and conduct ablation studies on the learning mechanism and key hyperparameters. The proposed K-MBRL is further validated on a physical quadruped robot performing a challenging sequence of maneuvers: rising to an upright posture supported by two rounded rear feet, maintaining balance during bipedal walking, and safely returning to the ground, as shown in Fig.1.

---

##### Demo

<video controls playsinline preload="none" poster="/papers/media/koopman-mbrl-outdoor-sdr-first-frame.png" width="864" height="1080" aria-label="Outdoor bipedal walking demonstration" style="display:block; width:100%; max-width:480px; height:auto; margin:18px auto;">
  <source src="/papers/media/koopman-mbrl-outdoor-demo-sdr.mp4" type="video/mp4">
  <a href="/papers/media/koopman-mbrl-outdoor-demo-sdr.mp4">Watch the outdoor walking demo (MP4)</a>
</video>

---

##### Citation

```bibtex
@misc{hao2026koopman,
  title = {Koopman Model-Based Reinforcement Learning},
  author = {Wenjian Hao and Paulo C. Heredia and Shaoshuai Mou},
  year = {2026},
  eprint = {2611.14186},
  archivePrefix = {arXiv},
  primaryClass = {cs.RO},
  url = {https://arxiv.org/abs/2611.14186}
}
```
