---
title: "Learning Nonlinear Systems Using Linear Operators and Machine Learning"
date: 2026-03-09
author: Wenjian Hao
math: true
summary: "A concise introduction to learning nonlinear systems using linear operators and machine learning for prediction and control."
---

Learning a dynamical model from data can support prediction, planning, and feedback control when first-principles models are unavailable or difficult to use. This post explains two approaches: learning the nonlinear state-transition map directly and learning observables whose evolution is approximately linear. The central distinction is that the Koopman operator is linear on a space of functions, but a practical finite-dimensional model is generally only an approximation.

<!--more-->

## Learning a dynamical system from data

### Problem setup

Consider a deterministic, discrete-time, time-invariant controlled system:

$$
\boldsymbol{x}_{t+1}=\boldsymbol{f}(\boldsymbol{x}_t,\boldsymbol{u}_t).
\label{eq:dynamics}
$$

Here $t=0,1,2,\ldots$ indexes time, $\boldsymbol{x}_t\in\mathbb{R}^n$ is the state, and $\boldsymbol{u}_t\in\mathbb{R}^m$ is the input. The unknown transition map is $\boldsymbol{f}:\mathbb{R}^n\times\mathbb{R}^m\to\mathbb{R}^n$. For this initial setup, assume the full state and applied inputs are measured without noise.

Suppose we collect transition samples:

$$
\mathcal{D}=\{(\boldsymbol{x}_i,\boldsymbol{u}_i,\boldsymbol{x}_i^+)\}_{i=1}^{N},
\qquad \boldsymbol{x}_i^+=\boldsymbol{f}(\boldsymbol{x}_i,\boldsymbol{u}_i).
\label{eq:dataset}
$$

The index $i$ identifies a data sample, not necessarily its time index; samples may come from multiple trajectories. The learning goal is to predict successor states accurately over the operating region and input range relevant to deployment. Good training fit alone does not establish accuracy outside that region.

With disturbances or measurement noise, observed transitions need not satisfy the deterministic relation exactly. At the population level, the optimal unrestricted squared-error predictor is the conditional mean when the relevant second moments exist, not every random realization. A restricted model class may only approximate that mean. Measurement noise in the regressors can also bias identification. Partial observations may require an observer, a history of measurements, or a recurrent model instead of a memoryless state-transition model.

### Direct prediction models

A linear baseline predicts the next state using $A\boldsymbol{x}+B\boldsymbol{u}$; an affine baseline also includes an offset. Ordinary least squares fits these coefficients, while ridge regression adds a quadratic penalty. These are useful baselines, but generally cannot represent nonlinear dynamics exactly over a large operating region.

A multilayer perceptron (MLP) instead uses a nonlinear predictor $\boldsymbol{f}_{\boldsymbol{w}}:\mathbb{R}^n\times\mathbb{R}^m\to\mathbb{R}^n$, parameterized by $\boldsymbol{w}\in\mathbb{R}^p$. Define its empirical prediction loss separately from its minimizers:

$$
\mathcal{L}_N(\boldsymbol{w})=
\frac{1}{N}\sum_{i=1}^{N}
\left\|\boldsymbol{x}_i^+-\boldsymbol{f}_{\boldsymbol{w}}(\boldsymbol{x}_i,\boldsymbol{u}_i)\right\|_2^2.
\label{eq:mlp-loss}
$$

$$
\widehat{\boldsymbol{w}}\in
\operatorname*{arg\,min}_{\boldsymbol{w}\in\mathbb{R}^p}
\mathcal{L}_N(\boldsymbol{w}).
\label{eq:empirical-minimizer}
$$

The latter notation assumes a minimizer exists and allows it to be nonunique. An optimizer used in practice may return only an approximate or local solution. No assumption that some network parameters reproduce the true dynamics exactly is needed to define this learning problem.

Generalization concerns prediction error on unseen data, not simply the distance between two parameter vectors. Different network parameters can represent the same function. To define a population objective, one must specify a distribution $\rho$ over state-input pairs; for example:

$$
\mathcal{R}(\boldsymbol{w})=
\mathbb{E}_{(\boldsymbol{x},\boldsymbol{u})\sim\rho}
\left\|\boldsymbol{f}(\boldsymbol{x},\boldsymbol{u})-\boldsymbol{f}_{\boldsymbol{w}}(\boldsymbol{x},\boldsymbol{u})\right\|_2^2.
\label{eq:population-risk}
$$

A shift in this distribution can change deployment performance even when training error is small.

### What gradient descent does and does not guarantee

For a differentiable loss, full-batch gradient descent uses

$$
\boldsymbol{w}_{k+1}=\boldsymbol{w}_k-\alpha_k\nabla\mathcal{L}_N(\boldsymbol{w}_k),
\label{eq:gd-update}
$$

where $k$ indexes optimization iterations and $\alpha_k>0$ is the step size. This is distinct from the physical time index $t$.

A diminishing step size is **not universally necessary** for convergence. For a differentiable, strongly convex objective with an $L$-Lipschitz gradient, full-batch gradient descent with a constant step size $0<\alpha\leq 1/L$ converges to the unique minimizer. Neural-network objectives are generally nonconvex, so this guarantee does not automatically apply.

Stochastic gradient descent uses noisy gradient estimates. Under suitable smoothness, strong-convexity, unbiasedness, and bounded-variance assumptions, a sufficiently small fixed step size gives an expected-error bound with a noise-dependent floor. Suitable diminishing step sizes can remove that floor; classical conditions include $\sum_k\alpha_k=\infty$ and $\sum_k\alpha_k^2<\infty$. Neither statement is a universal guarantee for neural networks. See [Bottou, Curtis, and Nocedal (2018)](https://arxiv.org/abs/1606.04838) for precise assumptions and results.

## The Koopman operator viewpoint

### Linear evolution of observables

First consider an autonomous system $\boldsymbol{x}_{t+1}=\boldsymbol{F}(\boldsymbol{x}_t)$, without an independently chosen input. An observable is a scalar function $g$ of the state. On a linear function space closed under composition with $\boldsymbol{F}$, the Koopman operator is defined by

$$
(\mathcal{K}g)(\boldsymbol{x})=g(\boldsymbol{F}(\boldsymbol{x})).
\label{eq:koopman}
$$

It advances observables by one time step. For observables $g,h$ and scalars $a,b$,

$$
\mathcal{K}(ag+bh)=a\mathcal{K}g+b\mathcal{K}h.
\label{eq:linearity}
$$

This linearity follows from composition and does not require $\boldsymbol{F}$ to be linear. The trade-off is that the observable space is usually infinite-dimensional.

For a finite vector of observables $\boldsymbol{\psi}(\boldsymbol{x})\in\mathbb{R}^{d}$, an exact matrix representation requires its components to span a Koopman-invariant subspace:

$$
\boldsymbol{\psi}(\boldsymbol{F}(\boldsymbol{x}))=K\boldsymbol{\psi}(\boldsymbol{x}).
\label{eq:closure}
$$

Otherwise, a fitted matrix only approximates this relation. Recovering the original state also requires that the observables retain sufficient information. An exact finite-dimensional invariant representation with state recovery is a restrictive property, not a generic consequence of lifting into more dimensions. [Brunton et al. (2016)](https://doi.org/10.1371/journal.pone.0150171) discuss these limitations.

### DMD, EDMD, and learned observables

- **Dynamic mode decomposition (DMD)** fits a linear map between successive measured snapshots, possibly in reduced coordinates. Its connection to Koopman spectral quantities depends on the observables, data, and approximation assumptions.
- **Extended DMD (EDMD)** fits evolution in a prescribed dictionary of observables, such as polynomials or radial basis functions. Dictionary choice and data coverage affect the approximation. See [Williams, Kevrekidis, and Rowley (2015)](https://arxiv.org/abs/1408.4408).
- **Deep Koopman models** learn observables using neural networks rather than prescribing the entire dictionary. Encoder-decoder models are one approach; learning features does not by itself guarantee exact invariant coordinates. [Lusch, Kutz, and Brunton (2018)](https://arxiv.org/abs/1712.09707) provide an example of learning representations from trajectory data.

### Including control inputs

An independently selected input changes the state transition, so the autonomous definition alone is not a complete controlled-system model. One can define a family of operators indexed by a fixed input, or augment the state with an input sequence and its shift. A common practical predictor instead takes the form

$$
\begin{aligned}
\boldsymbol{z}_t&=\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_t),\\
\widehat{\boldsymbol{z}}_{t+1}&=A\boldsymbol{z}_t+B\boldsymbol{u}_t,\\
\widehat{\boldsymbol{x}}_{t+1}&=C\widehat{\boldsymbol{z}}_{t+1}.
\end{aligned}
\label{eq:controlled-predictor}
$$

Here $A\in\mathbb{R}^{d\times d}$, $B\in\mathbb{R}^{d\times m}$, and $C\in\mathbb{R}^{n\times d}$. This model is linear in the lifted state and input but generally approximates the nonlinear controlled dynamics. Some systems need input-dependent, bilinear, or richer lifted models. A nonlinear decoder is another option, but its use can make state constraints and costs nonlinear in the lifted variables. [Korda and Mezic (2018)](https://arxiv.org/abs/1611.03537) develop lifted linear predictors for model predictive control.

## A practical learning workflow

The following is an illustrative workflow, not a claim of a new algorithm or a guarantee that every nonlinear system admits this model.

### Preserve the state and fit lifted dynamics

One useful architecture includes the state explicitly:

$$
\boldsymbol{\psi}_{\theta}(\boldsymbol{x})=
\begin{bmatrix}\boldsymbol{x}\\\boldsymbol{h}_{\theta}(\boldsymbol{x})\end{bmatrix},
\qquad C=\begin{bmatrix}I_n&0\end{bmatrix}.
\label{eq:state-inclusive-lift}
$$

The learned features $\boldsymbol{h}_{\theta}$ augment the state, so $d\geq n$ and $C\boldsymbol{\psi}_{\theta}(\boldsymbol{x})=\boldsymbol{x}$ by construction. A separate decoder and reconstruction loss are unnecessary for this architecture. Including a constant feature allows an affine offset in the lifted predictor.

For a fixed encoder, form matrices with samples as columns:

$$
\begin{aligned}
Z&=[\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_1),\ldots,\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_N)],\\
Z^+&=[\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_1^+),\ldots,\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_N^+)],\\
U&=[\boldsymbol{u}_1,\ldots,\boldsymbol{u}_N].
\end{aligned}
\label{eq:lifted-data}
$$

Set $V=[Z^\top\;U^\top]^\top$ and $M=[A\;B]$. A regularized least-squares fit is

$$
\min_M\ \|Z^+-MV\|_F^2+\lambda\|M\|_F^2,
\label{eq:ridge-objective}
$$

$$
M=Z^+V^\top(VV^\top+\lambda I)^{-1},\qquad\lambda>0.
\label{eq:ridge-fit}
$$

The norm is the Frobenius norm. With no regularization, a minimum-norm solution is $M=Z^+V^\dagger$, where the dagger denotes the Moore-Penrose pseudoinverse; the superscript $+$ on $Z^+$ denotes successor data, not a pseudoinverse. Numerically, solve the regularized linear system rather than forming an explicit inverse. Jointly optimizing the encoder and matrices is generally nonconvex even though fitting the matrices for a fixed encoder is a convex problem.

### Train and validate for the intended use

1. **Split data by trajectory or experiment.** Keep training, validation, and test trajectories separate; randomly splitting highly correlated neighboring transitions can give an overly optimistic estimate of generalization. Fit normalization statistics on training data only.
2. **Fit the lifting map and dynamics.** A latent consistency loss compares $\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_i^+)$ with $A\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_i)+B\boldsymbol{u}_i$. State-prediction losses measure errors after applying $C$. Feature scaling and regularization matter because latent loss depends on the chosen coordinates.
3. **Use multi-step losses when trajectories are available.** Initialize $\widehat{\boldsymbol{z}}_0=\boldsymbol{\psi}_{\theta}(\boldsymbol{x}_0)$, roll out $\widehat{\boldsymbol{z}}_{j+1}=A\widehat{\boldsymbol{z}}_j+B\boldsymbol{u}_j$, and compare $C\widehat{\boldsymbol{z}}_j$ with measured states. Arbitrary unconnected transition samples do not provide multi-step targets.
4. **Evaluate beyond training loss.** Compare held-out one-step and multi-step errors against linear and nonlinear baselines, and measure computation time. For control, also evaluate tracking, constraint violations, and sensitivity to disturbances and model mismatch.

Reconstruction losses are useful when a learned encoder-decoder does not include an exact state readout. They should not be treated as mandatory for every Koopman model. Similarly, a learned feature vector can collapse to an uninformative representation unless the architecture or losses preserve the information needed for the task.

## Prediction and control: benefits and limitations

Small one-step error does not guarantee small long-horizon error. To see why, suppose the true lifted evolution satisfies $\boldsymbol{z}_{t+1}=A\boldsymbol{z}_t+B\boldsymbol{u}_t+\boldsymbol{r}_t$, while the predictor omits the residual $\boldsymbol{r}_t$. With the same initial lifted state and the same input sequence, define $\boldsymbol{e}_t=\boldsymbol{z}_t-\widehat{\boldsymbol{z}}_t$. Direct substitution gives

$$
\begin{aligned}
\boldsymbol{e}_H&=\sum_{j=0}^{H-1}A^{H-1-j}\boldsymbol{r}_j,\\
\|\boldsymbol{e}_H\|_2&\leq\sum_{j=0}^{H-1}\|A^{H-1-j}\|_2\|\boldsymbol{r}_j\|_2.
\end{aligned}
\label{eq:error-propagation}
$$

Thus, both approximation residuals and the growth of matrix powers influence rollout accuracy. With the exact linear readout above, state error is bounded by $\|C\|_2\|\boldsymbol{e}_H\|_2$. This calculation compares predictions under an identical input sequence; closed-loop stability requires a separate analysis.

A lifted linear predictor can simplify model predictive control when the costs are convex quadratic and the constraints are linear in the decision variables. Nonlinear decoding or nonconvex constraints can remove that advantage. Good empirical prediction alone does not establish stability, recursive feasibility, or safety of the physical system. Those claims require additional assumptions, analysis, and an appropriate treatment of model error.

Likewise, using a learned model in reinforcement learning may reduce planning cost or improve data efficiency on a particular task, but neither improvement follows automatically from a linear latent representation. The appropriate model depends on data quality, coverage, prediction horizon, and the control objective.

## Extensions

Time-varying systems require models that account for time or changing parameters; a single fixed operator is not generally sufficient. Stochastic systems can be described using conditional-expectation operators on observables, but predicting expectations is different from predicting individual sample paths. Partial-observation and multi-agent problems introduce additional questions about state estimation, available information, and communication.

**Takeaway:** Koopman-based learning provides a useful structure for approximating nonlinear dynamics, not a universal exact finite-dimensional linearization. Its value should be established through clearly stated assumptions, held-out prediction tests, and task-specific control evaluation.

## References

- Bottou, L., Curtis, F. E., and Nocedal, J. (2018). [Optimization Methods for Large-Scale Machine Learning](https://arxiv.org/abs/1606.04838).
- Williams, M. O., Kevrekidis, I. G., and Rowley, C. W. (2015). [A Data-Driven Approximation of the Koopman Operator: Extending Dynamic Mode Decomposition](https://arxiv.org/abs/1408.4408).
- Brunton, S. L., Brunton, B. W., Proctor, J. L., and Kutz, J. N. (2016). [Koopman Invariant Subspaces and Finite Linear Representations of Nonlinear Dynamical Systems for Control](https://doi.org/10.1371/journal.pone.0150171).
- Korda, M., and Mezic, I. (2018). [Linear Predictors for Nonlinear Dynamical Systems: Koopman Operator Meets Model Predictive Control](https://arxiv.org/abs/1611.03537).
- Lusch, B., Kutz, J. N., and Brunton, S. L. (2018). [Deep Learning for Universal Linear Embeddings of Nonlinear Dynamics](https://arxiv.org/abs/1712.09707).
