# UI and UX specialist integration

Keep product-specific UI and UX design as a standalone specialist capability.
Scrum routes relevant work to it and consumes its evidence; Scrum does not copy a
full design method into its core. This separation lets the design skill evolve
without turning every backend Sprint into a design exercise.

## Trigger the route

Use this route when a PBI changes a user-facing flow, information hierarchy,
navigation, interaction pattern, visual system, responsive behavior, form,
content hierarchy, or loading, empty, error, success, and permission states. A
pure implementation repair with no design decision can use the Web UI Definition
of Done profile without a specialist pass. Backend, infrastructure, and internal
refactors skip this route unless they change a user experience contract.

## Route when `ux-fit` is available

1. Read the existing product Design Brief and design-system evidence before
   proposing a UI change.
2. Load the standalone `ux-fit` skill during refinement or planning. Ask it to
   diagnose the product, domain, users, constraints, and current interface, then
   return the product-specific design direction and review criteria.
3. Keep the Product Owner accountable for value and ordering. Keep Developers
   accountable for implementation. Treat `ux-fit` as specialist evidence, not as
   a new Scrum role and not as authority to change scope.
4. Put the accepted design direction, states, accessibility expectations, and
   evidence paths in the PBI criteria, Sprint plan, or delegation brief.
5. Run a design review against the implemented result before the Definition of
   Done gate. Record screenshots or hands-on evidence only when they materially
   support the review.

## Fallback when `ux-fit` is unavailable

The Product Owner and Developers write a compact design intent before build:

- target user and task;
- information and action priority;
- required states and recovery paths;
- supported viewport and input modes;
- accessibility and content requirements;
- existing components or patterns to preserve;
- observable review evidence.

Apply the Web UI profile in `core/dod/profiles.md` and test the interaction under
`core/test-strategy.md`. Do not invent a new visual language without an explicit
product decision.

## Record the route

Add `UX route: ux-fit | fallback | n/a, with reason` to the Sprint plan and to each
affected build brief. Link the Design Brief or design evidence. The fixed PBI
record does not need a new field; acceptance criteria and DoD evidence carry the
observable contract.
