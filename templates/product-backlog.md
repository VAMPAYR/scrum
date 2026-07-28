<!--
  TEMPLATE: product-backlog.md
  Instantiate to .scrum/product/backlog.md at stage 1 VISION; refined at stage 2.
  The Product Backlog is the ordered, emergent list of everything the product
  needs to fulfil the Product Goal. The Product Owner owns it and its order.
  The PBI record format below is FIXED by SKILL.md. Do not
  change field names or order. Keep it plain markdown, committed to the repo.
-->

# Product Backlog

<!--
  Ordering: the top of the list is the most valuable, most ready work. The PO
  orders by value, risk, dependency, and size (core/roles/product-owner.md).
  Each item's "Order rationale" explains why it sits where it does.

  Status legend:
  - draft       captured, not yet refined
  - ready       refined, sized, acceptance criteria written; eligible to forecast
  - forecast    pulled into the current Sprint's forecast
  - in-progress a Developer is building it this Sprint
  - done        passed the Definition of Done gate with recorded evidence
  - dropped     removed from scope by the PO (keep the record; do not delete)

  Keep the backlog bounded. Dropping stale items is healthy (health check S1.4);
  a monotonically growing backlog is a process-decay sign.

  Size: XS | S | M | L. An L must be split into smaller releasable items before
  it can move to forecast.
-->

## Ordered items

### PBI-001: <title>
- Status: draft | ready | forecast | in-progress | done | dropped
- Value: <stakeholder-facing outcome, one sentence>
- Order rationale: <why it sits here in the backlog>
- Size: XS | S | M | L (L must be split before forecast)
- Acceptance criteria:
  - [ ] <observable behavior>
- DoD evidence: <links/paths filled at completion>

### PBI-002: <title>
- Status: draft | ready | forecast | in-progress | done | dropped
- Value: <stakeholder-facing outcome, one sentence>
- Order rationale: <why it sits here in the backlog>
- Size: XS | S | M | L (L must be split before forecast)
- Acceptance criteria:
  - [ ] <observable behavior>
- DoD evidence: <links/paths filled at completion>

<!--
  Add PBIs in order, numbered PBI-NNN. Every field is required. "Value" must name
  a stakeholder-facing outcome, not restate the task (health check S1.2). Write
  acceptance criteria as observable behaviors the DoD gate and the stakeholder can
  check. Fill "DoD evidence" only at completion, from the gate
  (core/dod/definition-of-done.md).

  Example of a well-formed item (delete before use):

  ### PBI-042: Export a session as a shareable link
  - Status: ready
  - Value: A user can hand a colleague a link that reopens their exact session.
  - Order rationale: Highest-value ask from the last Review; unblocks sharing.
  - Size: M
  - Acceptance criteria:
    - [ ] A "Share" control produces a URL that reopens the session read-only.
    - [ ] The link works for a signed-out viewer.
    - [ ] An expired link shows a clear message, not an error page.
  - DoD evidence: <links/paths filled at completion>
-->

## Dropped items
<!-- Keep dropped PBIs here with the reason and the Sprint that dropped them. -->
- <PBI-NNN: title> dropped <YYYY-MM-DD, sprint-NNN>: <reason>
