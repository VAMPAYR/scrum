# Threat modeling

Threat modeling makes security design explicit before defects become expensive.
Use it to connect the system as built, plausible misuse, mitigations, and tests.
The model is a living engineering artifact, not a one-time compliance diagram.

## Trigger

Run or update a threat model when a PBI adds or changes any of these:

- a trust boundary, entry point, external integration, or data flow;
- authentication, authorization, identity, privilege, secrets, or cryptography;
- sensitive, regulated, safety-relevant, or customer-controlled data;
- deployment, infrastructure, build, update, or dependency trust;
- a parser, file upload, public endpoint, privileged tool, autonomous action, or
  destructive capability;
- a model, retrieval source, memory store, agent, tool call, or inter-agent path;
- an architecture assumption whose failure would have material impact.

A small implementation inside an already modeled boundary may update an existing
threat record instead of creating a new model. Mark the route and reason. Do not
mark the whole security tier `n/a` merely because a change has no HTTP endpoint.

## Ask four questions

### 1. What are we building?

Draw or describe the minimum system model needed to reason about the change.
Name components, actors, data stores, entry points, data flows, trust boundaries,
privileged operations, dependencies, and deployment boundaries. Distinguish the
intended design from the observed implementation.

### 2. What can go wrong?

Work breadth first. Examine each entry point, flow, store, boundary, dependency,
and privileged action before exploring one threat deeply. Consider unauthorized
access, tampering, disclosure, loss, denial of service, privilege expansion,
unsafe failure, repudiation, supply-chain compromise, privacy harm, and misuse of
legitimate capability.

For AI agents and model-backed products, also consider instruction or goal
hijacking, tool misuse, identity and privilege abuse, poisoned memory or context,
insecure inter-agent communication, unexpected code execution, data leakage,
uncontrolled cost, and cascading failure.

### 3. What will we do about it?

Choose one treatment for each material risk: avoid, reduce, transfer, or accept.
Prefer design changes that remove the path or privilege. Add preventive,
detective, and recovery controls where removal is not practical. Assign an owner
and map every mitigation to verification under `core/test-strategy.md`.

### 4. Did we do a sound job?

Check that the model covers every material boundary and asset, that the code and
deployment still match it, and that each mitigation has evidence. Search for
variants and second-order effects. Record assumptions, unresolved questions, and
residual risk. A named risk owner, not an implementer acting alone, accepts
material residual risk.

## Threat record

Keep the record in the Sprint directory, an existing project threat-model system,
or an architecture decision record. Link it from the PBI evidence.

```markdown
### TM-<id>: <short threat>
- Scope and asset: <component, data, capability, or user outcome>
- Boundary or entry point: <where trust changes>
- Condition or event: <how the threat becomes possible>
- Consequence: <technical and stakeholder impact>
- Assumptions: <facts the analysis depends on>
- Treatment: avoid | reduce | transfer | accept
- Mitigation: <design or operational control>
- Verification: <test, analysis, review, monitoring, or recovery exercise>
- Owner: <role or named risk owner>
- Residual risk and review point: <what remains and when to revisit>
- Status: open | mitigated | accepted | invalidated
```

Use stable IDs so a mitigation, test, defect, and operational alert can point to
the same threat. Convert implementation work into a PBI or task; do not leave it
buried in a diagram.

## Depth and timing

- **Low-risk change inside a stable boundary:** record the trigger decision,
  inspect the existing model, and update affected records.
- **New feature or integration:** model it during refinement or planning, before
  implementation fixes the design.
- **High-impact architecture:** use a fuller data-flow model, independent security
  review, misuse scenarios, and an assurance case.
- **Before release and after incidents:** compare the model with the deployed
  system, close verified mitigations, and reopen assumptions that changed.

Threat modeling starts the security conversation. Code review, static analysis,
fuzzing, dependency review, penetration testing, monitoring, and incident learning
provide different evidence and remain necessary where risk warrants them.
