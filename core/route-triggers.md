# Conditional route triggers

Keep this index active with the compact writing contract. Load a triggered module
before the related decision or mutation; triggers are additive.

- **State:** load `core/state-protocol.md` when `.scrum/state.md` is absent,
  unreadable, incompatible, or being reconstructed after interruption.
- **Stall:** load `core/stall-recovery.md` when a worker reports `BLOCKED`,
  repeats a materially similar failure, consumes its mutating-attempt budget, or
  reaches a checkpoint without evidence-defined progress.
- **Threat:** load `core/threat-modeling.md` when work changes a material trust,
  data, identity, dependency, deployment, tool-authority, or agent boundary.
- **UI/UX:** load `core/ux-integration.md` when work changes a user journey,
  interaction, information architecture, accessibility behavior, visual system,
  or interface whose quality needs design judgment.
- **Full writing:** use the standalone `research-clinical-writing` skill for a
  substantial stakeholder-facing or analytical artifact. When it is unavailable,
  load `core/artifact-writing-full.md`.
- **Cancel:** load the `cancel` route before a `[PO]` decision to cancel an
  obsolete Sprint Goal and return unfinished PBIs to the backlog.

If Python is available, add the corresponding `--trigger` option to
`scripts/context_router.py`. If it is unavailable, read the named module directly.
Never omit a triggered module to fit context. Split the operation at a safe
boundary instead.
