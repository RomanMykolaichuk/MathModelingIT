# MathModelingIT Lab — architecture and expansion contract

## Purpose

The web layer reduces environment/setup friction and gives the learner an immediate experiment in the browser. It does **not** replace the Python lesson package, notebook, tests or research-grade experiment.

The contract is:

> **browser intuition → explicit explanation → Python reproduction → research transfer**

## Source-of-truth rule

For every mathematical idea implemented twice:

1. Python lesson code remains the computational source of truth.
2. Browser JavaScript may implement only a transparent teaching subset.
3. A shared control case must be stored in `web/control-cases.json`.
4. CI must verify the case independently with Node and Python.
5. A browser result must not claim more precision or scope than the Python model supports.

## Lab Engine

`web/lab-engine.js` contains pure functions with no DOM dependency. This is deliberate:

- the browser UI can call them;
- Node can test them without a browser;
- UI refactoring cannot silently change the mathematics;
- future labs can add small testable functions instead of embedding equations in event handlers.

`web/app.js` is responsible only for:

- reading UI parameters;
- rendering results;
- saving local progress/reflections;
- exporting JSON;
- Student/Instructor mode.

## One learning pattern

Every full browser laboratory must implement:

1. **Predict** — learner commits to an expectation before seeing the result.
2. **Run** — learner changes at least one meaningful model parameter.
3. **Explain** — learner explains the observed mechanism.
4. **Break** — learner finds a counterexample, invalid assumption or boundary.
5. **Transfer** — learner maps the method to a research problem.

A slider plus a chart is therefore **not** sufficient to count as a completed interactive lab.

## Mandatory pre-lab resources

Every full interactive laboratory must begin with a visible **pre-lab resource bar** placed before the Predict → Run → Explain → Break → Transfer cycle.

It must contain exactly these learner-facing resources:

1. **Theory** — a button that opens the lesson theoretical material in a **new browser tab**. The theoretical source is the lesson `README.md` (or a future versioned theory page derived from it).
2. **Lab instruction (PDF)** — a button that opens a versioned PDF instruction in a **new browser tab**. PDF files live under `web/instructions/`.

This is a release requirement, not an optional UX enhancement. A lesson cannot be marked `interactive` unless both resources exist and are linked.

PDF instructions must:
- be derived from the lesson `README.md` and `assignment.md`;
- describe the browser workflow and its control cases;
- explicitly separate the browser teaching subset from the full Python assignment when the scopes differ;
- include completion criteria and research-transfer expectations;
- be visually QA-checked before commit.

Course CI must verify that every PDF referenced by the current interactive labs exists and is non-empty.

## Admission criteria for a new interactive lab

A lesson may move from `python` to `interactive` in `web/course-catalog.js` only when all of the following exist:

- a baseline control case with known output;
- at least one meaningful parameter to manipulate;
- an explicit “break the model” scenario;
- a research-transfer prompt;
- a pure function in the Lab Engine or an explicitly precomputed scenario;
- Node verification;
- Python verification;
- an instructor checkpoint;
- a theory link that opens in a new tab;
- a versioned PDF lab instruction under `web/instructions/`.

## Proposed expansion order

### Wave 1 — high visual payoff

- **T2.L1 optimization:** feasible region, active constraints, objective movement.
- **T2.L2 transport:** route matrix/flow diagram and forbidden-route experiment.
- **T2.L3 nonlinear optimization:** contour surface, start point and optimizer path.

### Wave 2 — reproducibility and uncertainty

- **T1.L2 model classification:** deterministic trajectory vs stochastic ensemble.
- **T1.L3 modeling organization:** seed/config/metadata reproducibility experiment.
- **T2.L6 computer mathematics:** symbolic vs numerical solution comparison.

### Wave 3 — meta-modeling

- **T1.L4 method selection:** problem features → method selection with counterexamples.
- **T2.L7 research workflow:** calibration, residuals, uncertainty and alternative-model challenge.

This order intentionally prioritizes labs where browser interaction adds information that is difficult to see in a notebook listing alone.

## Data and security

The first version:

- uses no accounts;
- sends no learner data to a backend;
- stores progress and reflections in `localStorage`;
- exports learner-owned JSON files;
- uses synthetic/non-sensitive teaching data.

If server-side functions are added later, they should be treated as a separate architecture decision rather than hidden inside the GitHub Pages layer.

## Definition of Done for the web layer

A release candidate requires:

- all web files pass syntax checks;
- shared Node/Python control cases pass;
- existing full course smoke check passes;
- three current interactive labs reproduce their baseline Python results;
- Student and Instructor modes remain progressive enhancement, not separate codebases;
- the site remains functional as a static GitHub Pages deployment;
- every interactive lab exposes its theory and PDF instruction before the interactive cycle.
