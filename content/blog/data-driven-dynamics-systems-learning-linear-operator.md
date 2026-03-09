---
title: "Learning Nonlinear Dynamics with Deep Linear Operators"
date: 2026-03-09
author: Wenjian Hao
math: true
---

Goal of this post: This post introduces data-driven dynamical systems learning using a combination of deep neural networks and linear-operator-based methods. In particular, it focuses on Koopman-inspired representations for prediction, system identification, and feedback control design in complex nonlinear systems. The discussion is intended for readers with minimal background knowledge.

## Problem Setup

Consider the discrete-time dynamical system

$$
\boldsymbol{x}(t+1) = \boldsymbol{f}(\boldsymbol{x}(t), \boldsymbol{u}(t)),
$$

where $t=0,1,2,\cdots$ denotes the discrete-time index, $\boldsymbol{x}(t) \in \mathbb{R}^n$ is the system state, $\boldsymbol{u}(t) \in \mathbb{R}^m$ is the control input, and $\boldsymbol{f}:\mathbb{R}^n\times\mathbb{R}^m\rightarrow\mathbb{R}^n$ is the system dynamics mapping funciton. 

Suppose we are given a dataset 

$$\mathcal{D} = \{(\boldsymbol{x}_i, \boldsymbol{u}_i, \boldsymbol{x}_i^+)\}_{t=1}^{N},
$$ 

where $\boldsymbol{x}_i^+$ denotes the successor state obtained by applying the input $\boldsymbol{u}_i$ to $\boldsymbol{f}$ at $\boldsymbol{x}_i$. Here, the subscript is used to index data samples in the dataset, rather than the time-varying system variables. The problem of interest is to learn an approximation of $\boldsymbol{f}$ from the dataset $\mathcal{D}$.

## Baseline Methods and Preliminaries

Popular baseline methods:

- A Multilayer Perceptron (MLP) in machine learning: MLP assumes that the unknown dynamics $\boldsymbol{f}$ can be approximated by a parameterized function class, denoted as $\boldsymbol{\phi}(\boldsymbol{x}(t), \boldsymbol{u}(t), \boldsymbol{w}^*)$, where $\boldsymbol{\phi}:\mathbb{R}^n\times\mathbb{R}^m\rightarrow\mathbb{R}^n$. The dynamics learning problem is then formulated as estimating the optimal parameters $\boldsymbol{w}^*$ that best fit the dataset $\mathcal{D}$ by minimizing the prediction error:

$$
\min_{\boldsymbol{w}\in\mathbb{R}^p} \mathbf{L}(\boldsymbol{w}) = \frac{1}{N}\sum_{i=1}^{N}\parallel \boldsymbol{x}_i^+ - \boldsymbol{\phi}(\boldsymbol{x}_i, \boldsymbol{u}_i, \boldsymbol{w})\parallel^2 
$$

One can typically use gradient descent to solve this optimization problem:

$$
\boldsymbol{w}(k+1) = \boldsymbol{w}(k) - \alpha_w(k) \nabla_{\boldsymbol{w}}\mathbf{L}(\boldsymbol{w}_k),
$$

where $k=0,1,2,\cdots$ denotes the iteration index, $\alpha_w(k)$ is the learning rate, and $\nabla_{\boldsymbol{w}}\mathbf{L}(\boldsymbol{w}_k)$ denotes the gradient of $\mathbf{L}$ with respect to $\boldsymbol{w}$ evaluated at $\boldsymbol{w}(k)$.

The Koopman operator:

Common evaluation metrics include one-step error, multi-step rollout error, long-horizon stability, and control cost when integrated with MPC/LQR-style controllers.

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
