---
title: "Learning Nonlinear Dynamics with Deep Linear Operators"
date: 2026-03-09
author: Wenjian Hao
math: true
---

Goal of this post: This post introduces data-driven dynamical systems learning using a combination of deep neural networks and linear-operator-based methods. In particular, it focuses on Koopman-inspired representations for prediction, system identification, and feedback control design in complex nonlinear systems. The discussion is intended for readers with minimal background knowledge.

## Problem Setup

We observe a nonlinear discrete-time system

$$
x_{t+1} = f(x_t, u_t),
$$

where $x_t \in \mathbb{R}^n$ is the state and $u_t \in \mathbb{R}^m$ is the control input. The goal is to learn a predictive model from trajectory data $\{(x_t, u_t, x_{t+1})\}$ that is accurate, stable, and useful for downstream control.

Instead of modeling $f(\cdot)$ directly, we seek a lifted representation $z_t = \phi_\theta(x_t)$ in which dynamics are approximately linear:

$$
z_{t+1} \approx A z_t + B u_t.
$$

If successful, this lets us use linear-system tools for prediction and control while still handling nonlinear behavior through the learned lifting map $\phi_\theta$.

## Main Ideas and Algorithm

The core idea is to combine neural representation learning with linear operator identification:

1. Learn an encoder $\phi_\theta$ that maps original states to latent observables.
2. Fit linear operators $(A, B)$ in latent space from data.
3. Learn a decoder $\psi_\eta$ to reconstruct physical states from latent variables.
4. Train end-to-end with losses on one-step prediction, multi-step rollout, and reconstruction.

A typical training objective is:

$$
\mathcal{L} = \lambda_{\mathrm{pred}} \mathcal{L}_{\mathrm{pred}} + \lambda_{\mathrm{roll}} \mathcal{L}_{\mathrm{roll}} + \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}.
$$

Regularization can include spectral penalties on $A$, sparsity structure, or constraints motivated by stability and controllability.

After training, we can roll out trajectories with the linear latent dynamics and decode predictions back to the original state space.

## Benchmark Algorithm Comparison

This framework is typically evaluated on several classes of systems:

- Low-dimensional canonical systems (e.g., pendulum, Duffing oscillator, Lorenz-type dynamics) to inspect interpretability and long-horizon behavior.
- Robotics and control benchmarks (e.g., cart-pole, quadrotor variants, soft robotic systems) where control relevance matters.
- PDE-inspired or spatiotemporal datasets where latent linear evolution can improve sample efficiency and forecasting speed.

Common evaluation metrics include one-step error, multi-step rollout error, long-horizon stability, and control cost when integrated with MPC/LQR-style controllers.

## Applications

Deep linear-operator models support multiple downstream tasks:

- Long-horizon forecasting in nonlinear physical systems.
- System identification when first-principles models are unavailable or expensive.
- Controller synthesis in latent space using linear optimal control methods.
- Safety filtering and constrained control by combining latent predictions with CBF/MPC layers.
- Model-based reinforcement learning with improved planning and sample efficiency.

## Extensions

Current research directions include:

- Time-varying and input-dependent operators $(A_t, B_t)$.
- Stochastic and uncertainty-aware Koopman models for noisy environments.
- Physics-informed lifting functions that embed invariants or conservation structure.
- Distributed and partial-observation formulations for multi-agent systems.
- Online adaptation for nonstationary dynamics and domain shifts.

These extensions aim to close the gap between elegant operator theory and robust real-world deployment.
