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

`core/engineering-standards.md` was generalized from the author's own private
production standards and rewritten to be stack-agnostic. The AI and LLM profile
in `core/dod/profiles.md` draws on published industry practice in
evaluation-driven development of foundation-model applications, stated here in
general terms.

## Licensing

This package is released under the MIT license; see `LICENSE`. That grant covers
this package's own text and structure. The frameworks and standards credited
above belong to their respective authors and stay under their own licenses and
terms. Scrum itself is a framework anyone may implement: the rules are free to
use, and only a given author's expression of them is protected. Trademarks named
on this page belong to their owners.
