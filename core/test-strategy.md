# Adaptive test strategy

Testing starts with the claim and the failure cost. The team chooses the smallest
set of methods that can expose the important defects. It does not force every
task through the same ceremony.

## Select the route before implementation

Record the selected route and reason in the Sprint plan and every build brief.
Several routes may apply to one PBI.

| Situation | Primary route | Required evidence |
|---|---|---|
| Deterministic new behavior with a clear contract | Test-driven development (TDD) | A failing test observed before implementation, then the passing test and refactor result |
| Reported defect or reproducible security flaw | Regression-first TDD | A test that reproduces the failure before the fix and passes after it |
| Legacy or poorly understood behavior that must be preserved | Characterization tests, then change | Tests that capture current behavior, with intentional behavior changes identified separately |
| Invariants, parsers, serializers, protocols, or numerical logic | Example tests plus property-based tests | Named invariants, generated-case results, and minimized counterexamples when found |
| Untrusted binary, text, or protocol input | Boundary tests plus fuzzing | Corpus or seed strategy, run duration or case count, crash/hang findings, and retained regressions |
| API, service, database, queue, or third-party boundary | Contract and integration tests | Provider/consumer contract result, realistic boundary run, timeout and failure-path result |
| Critical user journey | A small end-to-end suite | Runnable journey evidence across the integrated system; do not duplicate every lower-level branch |
| Refactor with behavior intended to remain stable | Existing tests plus characterization or differential checks | Before-and-after behavior comparison and a scoped diff |
| Concurrency, state machines, memory safety, or high-assurance logic | Static analysis, model checking, formal methods, stress or race tests as appropriate | Tool result, property checked, assumptions, and unresolved findings |
| Visual, interaction, accessibility, or usability change | Component checks plus hands-on and visual review | State coverage, keyboard and assistive-tech evidence, viewport evidence, and screenshots where useful |
| Probabilistic model behavior | Evaluation-driven development | Versioned eval set, rubric, thresholds, repeated results, failure analysis, and model/prompt version |
| Feasibility is unknown | Timeboxed spike | Question, timebox, result, and an explicit discard-or-harden decision |

## TDD route

Use TDD when the expected behavior can be stated before the implementation.

1. Write one small test for one behavior or risk.
2. Run it and observe the expected failure. A test that passes before the change
   does not prove that it guards the new behavior.
3. Write the smallest implementation that makes the test pass.
4. Run the focused test and the relevant surrounding suite.
5. Refactor while the tests stay green.
6. Repeat, then run the full project gates before review.

TDD does not require mocking every collaborator. Prefer real values and narrow
fakes. Use integration tests where the boundary behavior is the claim.

## Legacy and uncertain systems

Do not assert an idealized behavior and call it preserved behavior. First add
characterization tests around the paths the change can affect. Identify surprising
behavior as observed, then ask the Product Owner whether to preserve or change it.
For a broad unknown, run a scout or spike before forecasting implementation.

## Security and misuse testing

Map each material threat or abuse case to at least one preventive, detective, or
recovery check. Test authorization before effects, invalid and oversized input,
timeouts, partial failure, replay or duplication, unsafe defaults, and resource
exhaustion where relevant. Fuzz parsers and complex trust boundaries when the
input space makes examples inadequate.

Penetration and exploratory testing supplement these checks. They do not replace
requirements, threat modeling, code review, or automated mitigation tests.

## Evidence rules

- Map every acceptance criterion to a test, analysis, inspection, or hands-on
  check. State why a non-automated method is the right method.
- Record the exact command, environment, result, and test or property name. Keep
  screenshots only when they show evidence that text output cannot.
- Run focused checks during development and the full relevant suite at the gate.
- Treat skipped, flaky, quarantined, or nondeterministic tests as findings. Name
  the reason, owner, and remediation. Do not rerun until green without diagnosis.
- Review the test itself. A tautological assertion, an over-mocked path, or a test
  that never exercises the changed behavior does not count.
- Keep tests fast and local at lower layers. Reserve slower end-to-end tests for
  integrated risks that lower layers cannot answer.

## Refuse test theater

Do not chase a coverage number without a decision it supports. Do not write tests
only after implementation and claim they drove the design. Do not weaken an
assertion, delete a test, add a broad exclusion, or hide a failure to make a gate
green. When a test method cannot answer the important question, choose another
method and record why.
