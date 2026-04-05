---
title: "Learning Nonlinear Systems Using Linear Operators and Machine Learning"
date: 2026-03-09
author: Wenjian Hao
blog_group: "Learning Complex Dynamical Systems"
math: true
summary: "A concise introduction to learning nonlinear systems using linear operators and machine learning for prediction and control."
---

This post introduces a practical view of learning nonlinear dynamics using Koopman-inspired deep linear operators, with a focus on prediction and control.

<!--more-->

## Why care about learning nonlinear systems?

### Problem setup

Consider the discrete-time dynamical system

\begin{equation}
\boldsymbol{x}(t+1) = \boldsymbol{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))
\label{eq:dynamics}
\end{equation}

where $t=0,1,2,\cdots$ denotes the discrete-time index, $\boldsymbol{x}(t) \in \mathbb{R}^n$ is the system state, $\boldsymbol{u}(t) \in \mathbb{R}^m$ is the control input, and $\boldsymbol{f}:\mathbb{R}^n\times\mathbb{R}^m\rightarrow\mathbb{R}^n$ is the system dynamics mapping funciton. 

Suppose we are given a dataset 

<div>
\begin{equation}
\mathcal{D} = \{(\boldsymbol{x}_i, \boldsymbol{u}_i, \boldsymbol{x}_i^+)\}_{i=1}^{N}
\label{eq:dataset}
\end{equation}
</div>

where $\boldsymbol{x}_i^+$ denotes the successor state obtained by applying the input $\boldsymbol{u}_i$ to $\boldsymbol{f}$ at $\boldsymbol{x}_i$. Here, the subscript is used to index data samples in the dataset, rather than the time-varying system variables. The problem of interest is to learn an approximation of $\boldsymbol{f}$ from the dataset $\mathcal{D}$.

## What is linear operator and state-of-the-art methods

### State-of-the-art methods

Popular baseline methods:

<ul>
<li>

Linear Regression (works well if $\boldsymbol{f}$ is linear): 
- Ordinary Least Squares (OLS) for basic modeling
- Regularized least squares (e.g., Ridge regression)
 
</li>
</ul>

<ul>
<li>
Multilayer Perceptron (MLP) in machine learning: MLP assumes that the unknown dynamics $\boldsymbol{f}$ in \eqref{eq:dynamics} can be represented by a parameterized function class, denoted as $\boldsymbol{f}(\boldsymbol{x}(t), \boldsymbol{u}(t))=\boldsymbol{\phi}(\boldsymbol{x}(t), \boldsymbol{u}(t), \boldsymbol{w}^*)$, where $\boldsymbol{\phi}:\mathbb{R}^n\times\mathbb{R}^m\rightarrow\mathbb{R}^n$. The dynamics learning problem is then formulated as estimating the optimal parameters $\boldsymbol{w}^*$ that best fit the dataset $\mathcal{D}$ in \eqref{eq:dataset} by minimizing the prediction error:

\begin{equation}
\boldsymbol{\hat w}^* = \arg\min_{\boldsymbol{w}\in\mathbb{R}^p} \mathbf{L}(\boldsymbol{w}) = \frac{1}{N}\sum_{i=1}^{N}\parallel \boldsymbol{x}_i^+ - \boldsymbol{\phi}(\boldsymbol{x}_i, \boldsymbol{u}_i, \boldsymbol{w})\parallel^2
\label{eq:mlp-loss}
\end{equation}

One can typically use gradient descent to solve \eqref{eq:mlp-loss}

\begin{equation}
\boldsymbol{w}(k+1) = \boldsymbol{w}(k) - \alpha_w(k) \nabla_{\boldsymbol{w}}\mathbf{L}(\boldsymbol{w}(k))
\label{eq:gd-update}
\end{equation}

where $k=0,1,2,\cdots$ denotes the iteration index, $\alpha_w(k)$ is the learning rate, and $\nabla_{\boldsymbol{w}}\mathbf{L}(\boldsymbol{w}_k)$ denotes the gradient of $\mathbf{L}$ with respect to $\boldsymbol{w}$ evaluated at $\boldsymbol{w}(k)$.


Some notes:
- The assumption that $\boldsymbol{f}$ can be represented by $\boldsymbol{\phi}$ (i.e., the existence of $\boldsymbol{w}^*$) is generally unclear in practice and depends on the expressive power of the chosen function class.
- $\boldsymbol{\hat w}^*$ denotes the optimal parameters with respect to the training dataset, while $\boldsymbol{w}^*$ denotes the optimal parameters defined over the entire state–input space of the dynamical system. In general, $\boldsymbol{\hat w}^*$ and $\boldsymbol{w}^*$ are not equal. The gap between $\boldsymbol{w}^*$ and $\boldsymbol{\hat w}^*$ may lead to poor deployment performance of $\boldsymbol{\hat w}^*$ for state–input pairs that are not contained in the training dataset.
- One useful existing result for \eqref{eq:gd-update} is that, to achieve $\lim_{k\rightarrow\infty} \parallel \boldsymbol{w}(k) - \boldsymbol{\hat w}^*\parallel^2 = 0$, the learning rate $\alpha_w(k)$ should be diminishing. Furthermore, for a constant $\alpha_w$, $\lim_{k\rightarrow\infty} \parallel \boldsymbol{w}(k) - \boldsymbol{\hat w}^*\parallel^2$ typically converges to a small constant.
</li>
</ul>

### Linear operator viewpoint

The Koopman operator provides a way to study nonlinear dynamics through a linear evolution of observables. Instead of evolving the state directly, it evolves carefully chosen functions of the state, which can make prediction and control design more structured.

The Koopman-operator-based methods include:
<ul>
<li>
- Dynamic Mode Decomposition (DMD)
- Extended Dynamic Mode Decomposition (EDMD)
- Deep Koopman Operator
</li>
</ul>

## The Proposed Method

### Main ideas
<div>
\begin{equation}
\mathcal{L} = 
\label{eq:training-objective}
\end{equation}
</div>

### Algorithm

1. Learn an encoder $\phi_\theta$ that maps original states to latent observables.
2. Fit linear operators $(A, B)$ in latent space from data.
3. Learn a decoder $\psi_\eta$ to reconstruct physical states from latent variables.
4. Train end-to-end with losses on one-step prediction, multi-step rollout, and reconstruction.

A typical training objective is:


### Applications

Deep linear-operator models support multiple downstream tasks:

- Long-horizon forecasting in nonlinear physical systems.
- System identification when first-principles models are unavailable or expensive.
- Controller synthesis in latent space using linear optimal control methods.
- Safety filtering and constrained control by combining latent predictions with CBF/MPC layers.
- Model-based reinforcement learning with improved planning and sample efficiency.

### Extensions

Current research directions include:

- Time-varying and input-dependent operators $(A_t, B_t)$.
- Stochastic and uncertainty-aware Koopman models for noisy environments.
- Physics-informed lifting functions that embed invariants or conservation structure.
- Distributed and partial-observation formulations for multi-agent systems.
- Online adaptation for nonstationary dynamics and domain shifts.

These extensions aim to close the gap between elegant operator theory and robust real-world deployment.
