# betalab 

A research-first Python library for glucose–insulin system modeling, simulation, and structured experimentation.

## Vision

This project is not just another simulator.
It is not an RL environment.
It is not a single-model implementation.

The long-term goal is to build a research-oriented abstraction layer for physiological dynamical systems — similar in spirit to what scikit-learn did for classical machine learning.

The focus is on reducing infrastructure overhead so researchers can spend more time on ideas and less time rewriting setup code.

---

## Motivation

In current glucose–insulin modeling research, there is a recurring pattern:

Researchers repeatedly:

* Rewrite simulation setup code
* Manually manage parameters and state vectors
* Build custom loops for experiments
* Re-implement wrappers for each model
* Spend more time on infrastructure than on research

This library aims to solve those problems first.

---

## Core Philosophy

### 1) Research-first, not product-first

This library should feel like a personal research engine that evolves naturally into a community tool.

Priorities:

* Flexibility
* Transparency
* Extensibility

Not priorities (yet):

* Polish
* Enterprise structure
* Over-engineering

---

### 2) Model-agnostic design

The system should not be tied to a single physiological model.

Long-term vision includes support for:

* Dalla Man
* Hovorka
* Bergman
* Other mechanistic and hybrid models

Version 1 will start with a clean and structured Dalla Man implementation.

---

### 3) Remove repetition in research workflows

The library should simplify common repetitive tasks:

* Running simulations
* Modifying physiological parameters
* Running batches of experiments
* Comparing outcomes

---

### 4) Simple and consistent API

User interaction should be clean, predictable, and minimal.

Inspired by scikit-learn:

* Consistent method naming
* Low boilerplate
* Easy to learn
* Structured experimentation

Conceptual example:

model = DallaMan()
model.set_params(SI=0.8)

sim = model.simulate(
duration=300,
meal=60,
insulin=6
)

sim.plot("glucose")

This level of simplicity is a central design goal.

---

### 5) Transparency over black-box abstraction

This library should not hide physiology.

Researchers must be able to:

* Access parameters
* Inspect state variables
* Modify internal components
* Plug in custom logic

The goal is to structure physiological modeling, not obscure it.

---

## Version 1 Scope (Strictly Limited)

Version 1 focuses on solving three core problems:

A) Rewriting simulation setup repeatedly
B) Manually managing parameters and states
C) Running many experiments using custom loops

### Version 1 will include:

* A clean Dalla Man model class

* A standard `simulate()` interface

* Parameter handling:

  * `set_params()`
  * `get_params()`

* Basic experiment utilities:

  * `batch_simulate()`
  * Parameter sweep functionality

### Version 1 will NOT include:

* RL environments
* Multiple physiological models
* GUI or web apps
* C++ optimization
* Full ML integration
* Population simulators
* Heavy packaging complexity

---

## Long-Term Direction

Over time, this library may expand into a broader physiological research framework supporting:

* Multiple models
* Control algorithm testing
* Data-driven identification
* Koopman / eDMD modeling
* Hybrid mechanistic + ML systems
* Synthetic data generation

These are future directions, not immediate goals.

---

## Core Abstraction Idea

At the heart of the system is the idea of a physiological dynamical system defined by:

* States
* Parameters
* Inputs (meal, insulin, etc.)
* Dynamics
* Simulation capability

All models will eventually conform to a common interface built around this concept.

---

## Primary User

The primary user is the researcher building and testing models.

The first priority is to support the creator’s own research workflow.

If it works well for that, it will naturally become useful to others.

---

## Design Principles

The system should remain:

* Clean
* Minimal
* Extensible
* Consistent

Avoid:

* Premature generalization
* Feature overload
* Rigid workflows

The goal is to build a strong foundation that can grow organically into a serious scientific framework.

