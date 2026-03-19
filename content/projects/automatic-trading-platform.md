---
title: "Automatic Trading Platform"
date: 2026-03-09
author: Wenjian Hao
project_group: "Personal Projects"
---

Project goal: Designed and developed an automatic trading platform for quantitative strategy research and execution. The platform integrates data ingestion, signal generation, portfolio construction, risk control, and performance evaluation in a reproducible workflow.

Platform structure: The platform is organized as a modular pipeline that connects market data collection, preprocessing, feature generation, strategy logic, portfolio construction, execution, and post-trade evaluation. This structure makes it easier to test quantitative ideas in a reproducible manner while keeping research, simulation, and execution components clearly separated.

<figure style="text-align: center;">
  <img src="/projects/pics/trading_flow_chart.png" alt="Automatic trading platform flow chart" style="max-width: 100%; height: auto;">
  <figcaption><em>Fig. 1: Automatic trading platform architecture.</em></figcaption>
</figure>

The architecture highlights how raw market data flows through the research and execution stack. Historical and live data first enter the data management layer, where they are cleaned and transformed into features for signal generation. The strategy layer then produces trading decisions, which are filtered by portfolio and risk modules before being sent to execution components.

The final stage of the platform focuses on monitoring and evaluation. Orders, positions, and performance metrics are tracked continuously so that strategies can be diagnosed, compared, and refined over time. This design supports both rapid prototyping of new trading ideas and disciplined deployment with clear risk-control checkpoints.
