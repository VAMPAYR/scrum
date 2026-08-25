# Artifact and communication standard

This standard governs stakeholder messages, `.scrum/` artifacts, delegation
briefs, technical documentation, reviews, decisions, findings, and reports. It
integrates the `research-clinical-writing` skill into Scrum while keeping this
package usable in runtimes that do not have that separate skill installed.

## Load the writing standard

1. If the runtime can discover a skill named `research-clinical-writing`, read
   its `SKILL.md` and the canonical style guide that file names.
2. If that skill is unavailable, apply this file as the complete fallback.
3. An explicit stakeholder or organization style may add constraints. It may not
   weaken factual accuracy, source integrity, uncertainty calibration, privacy,
   or the Definition of Done.

This is a behavioral integration, not a copy of a private style source.

## Core prose rules

- **Lead with the outcome.** State the finding, decision, status, or request before
  process detail.
- **Use clear actors and actions.** Prefer subject-verb-object sentences when they
  fit naturally. Use active voice unless the actor is unknown or genuinely
  irrelevant. Do not force awkward syntax merely to preserve SVO order.
- **Be concise and sufficiently detailed.** Keep only information that changes
  understanding, action, or verification. Detailed means the reader can see the
  evidence, rationale, owner, and next action. It does not mean repetitive.
- **Use conventional words.** Prefer the precise familiar term. Define a needed
  technical or Scrum term on first use. Remove jargon, novelty wording, and
  acronyms that add no precision.
- **Calibrate certainty.** Distinguish observed facts, source claims, inferences,
  decisions, estimates, and unknowns. State the concrete reason for uncertainty.
  Do not use vague hedges such as "may possibly," "it seems," or "arguably" when
  a scope condition or evidence limit can be named.
- **Keep claims traceable.** Preserve exact quantities, dates, thresholds, error
  text, and scope. Put in-text citations or links next to the supported claim when
  sources are available. Cite project evidence by path or command. Never invent a
  citation or expose a private local source path in a distributable artifact.
- **Separate evidence from judgment.** Show what was observed, then explain what
  it supports. Name conflicting evidence and material assumptions.
- **Write original prose.** Synthesize sources. Do not reproduce long passages or
  mimic a source's distinctive wording.

## Remove AI slop

Delete generic openings, canned transitions, inflated importance, repeated
conclusions, false balance, decorative adjectives, empty reassurance, and
restatements of the prompt. Avoid phrases that announce writing instead of doing
it, such as "it is important to note," "delve into," "in today's landscape," or
"this highlights the significance of." Do not label ordinary details as
"critical," "robust," "seamless," or "comprehensive" without evidence.

Do not smooth failures. Quote only the minimum error text needed, then state its
effect. Do not turn an unknown into "should work" or a failed check into "mostly
complete."

## Artifact rules

- **Product Goal and Sprint Goal:** one outcome, named beneficiary, and observable
  change. Avoid task lists.
- **PBI and acceptance criteria:** observable behavior and scope. Use examples for
  risky edge cases. Avoid implementation detail unless it is a real constraint.
- **Delegation brief:** one outcome, exact authority and scope, material context,
  chosen risk and test routes, and evidence required.
- **Decision:** decision first, then context, alternatives, rationale, assumptions,
  consequences, owner, and review trigger.
- **Status or review:** outcome first, then evidence, deviations, residual risk,
  and the next decision or action.
- **Risk or incident:** condition or event, consequence, evidence, treatment,
  owner, and review point. Avoid euphemism.
- **Technical documentation:** explain why the behavior exists, the contract,
  failure modes, examples, and operating limits. Keep it synchronized with code.

Templates define minimum fields, not filler quotas. Remove empty prose. Mark a
field `n/a` with a reason when the format requires it but the concept does not
apply.

## Final artifact audit

Before saving or sending prose, check:

1. Does the first sentence state the outcome or purpose?
2. Does each material claim have evidence, a citation, or an explicit basis?
3. Are observed facts, inferences, decisions, and unknowns distinguishable?
4. Does each sentence have a clear actor and action where one exists?
5. Can any jargon, hedge, transition, repetition, or adjective be removed without
   losing meaning?
6. Are the owner, next action, and residual risk clear where action is required?
7. Does the text protect private paths, personal data, secrets, and unpublished
   source material?

Revise until the artifact passes. The audit checks communication quality; it does
not replace technical verification.
