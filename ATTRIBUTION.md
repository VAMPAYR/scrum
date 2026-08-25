# Attribution

This package is an independent work that builds on published frameworks and
standards written by other people. It states in its own wording every rule it
takes from those sources. No organization or author named on this page endorses,
sponsors, or is affiliated with this package, and none has reviewed it. Any
error here belongs to this package, not to the work it credits.

## The Scrum Guide (2020)

The definition of Scrum this package follows is the Scrum Guide (2020) by Ken
Schwaber and Jeff Sutherland, published at https://scrumguides.org under the
Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0).

The accountabilities, the events, the artifacts and their commitments, the three
pillars, and the five values described across `core/` come from that definition.
This package restates those rules in its own wording rather than reproducing the
Guide's text. It is not a copy, an edition, or a replacement of the Scrum Guide;
read the Guide at the address above for the definition itself. Where this
package adapts Scrum for AI teams, the file carries an explicit "Adaptation:"
note that names what changed and why the original intent survives.

## The four value measures

The value dimensions the Product Owner records in `metrics.md` (current value,
unrealized value, time-to-market, ability-to-innovate) are the Key Value Areas of
Evidence-Based Management, published by Scrum.org. This package uses them as
plain prompts for judgment rather than as a scored measurement program.

## Delivery orchestration

Several delivery-orchestration concepts were adapted from an existing
open-source multi-agent supervision tool: investigation-only "scout" tasks kept
distinct from build tasks, explicit delivery modes, and isolated per-agent
working copies. That tool is acknowledged here generically and is not named.

## Engineering standards

The secure-development lifecycle, evidence, supply-chain, and AI-specific
controls in `core/engineering-standards.md`, `core/threat-modeling.md`, and the
Definition of Done draw on these public sources:

- NIST Special Publication 800-218, *Secure Software Development Framework
  (SSDF) Version 1.1*, at https://csrc.nist.gov/pubs/sp/800/218/final, and NIST
  SP 800-218A, *Secure Software Development Practices for Generative AI and
  Dual-Use Foundation Models*, at
  https://csrc.nist.gov/pubs/sp/800/218/a/final. The package uses their
  risk-based, outcome-oriented secure-development approach and lifecycle scope.
- The NCSC, CISA, and international-partner *Guidelines for Secure AI System
  Development*, at
  https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development.
  The package carries security across design, development, deployment, and
  operation.
- The OWASP GenAI Security Project's *Top 10 for Agentic Applications 2026*, at
  https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/.
  The package addresses agent goal hijacking, tool misuse, privilege abuse,
  agentic supply-chain risk, and related runtime failures in original wording.
- The Supply-chain Levels for Software Artifacts (SLSA) specification 1.2, at
  https://slsa.dev/spec/v1.2/. The package uses provenance and verifiable-build
  concepts without claiming conformance to a SLSA level.

The adaptive test strategy and compact assurance-case format are this package's
own synthesis of established testing and systems-assurance practice. They select
methods by claim and risk instead of prescribing one method for every task.

## Accessibility

The Web UI profile uses the W3C *Web Content Accessibility Guidelines (WCAG)
2.2*, at https://www.w3.org/TR/WCAG22/. It distinguishes the Level AA target-size
minimum in success criterion 2.5.8 from the larger Level AAA target in criterion
2.5.5. The package does not claim that this checklist alone establishes WCAG
conformance.

## Writing and UI/UX integrations

`core/artifact-writing-standard.md` defines a portable Scrum writing floor and,
when available, delegates the fuller prose method to the separately installed
`research-clinical-writing` skill. `core/ux-integration.md` keeps the separately
installed `ux-fit` design method modular and routes only design-relevant work to
it. Neither external skill's text or private supporting material is copied into
this package.

## Licensing

This package is released under the MIT license; see `LICENSE`. That grant covers
this package's own text and structure. The frameworks and standards credited
above belong to their respective authors and stay under their own licenses and
terms. Scrum itself is a framework anyone may implement: the rules are free to
use, and only a given author's expression of them is protected. Trademarks named
on this page belong to their owners.
