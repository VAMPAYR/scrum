# Daily Scrum (checkpoint sync)

## Purpose

The Daily Scrum is the Developers' checkpoint to review how far the Sprint Goal has
advanced and to re-plan the Sprint Backlog for the next stretch of work. It is a short
event owned by the Developers.

## Participants

- **Developers** own the event. It is by and for the Developers. In AI terms, the
  Developer agents' work state and the Orchestrator running on their behalf drive the
  inspection.
- **Scrum Master (SM)** ensures the event happens and stays in its timebox, and coaches
  the team on its purpose. The SM does not run it for the team.
- **Product Owner (PO)** and stakeholders may observe but must not interfere or turn it
  into a status report. The Daily Scrum is not a status meeting.

## Inputs

- `sprints/sprint-NNN/sprint.md`: the Sprint Goal and the task log with each PBI's state.
- The delegation results returned since the last checkpoint: pass or fail on the DoD
  gate, evidence, and any blockers reported verbatim.
- `impediments.md`: the open impediment list.

## AI-adapted procedure

**Adaptation: the checkpoint sync.** A Sprint here runs in hours, not weeks, and the
Developers are agents working in task batches rather than people working across a day.
The Daily Scrum becomes a checkpoint the Developers run between task batches. The purpose
is unchanged: inspect progress toward the Sprint Goal, adapt the Sprint Backlog, and
surface impediments. The cadence is compressed from once a day to once per batch
boundary. The intent is preserved because the event stays the Developers' focused chance
to inspect and re-plan toward the Sprint Goal, only timed to the work rhythm of agents.

Run the checkpoint at each batch boundary in the Orchestrator's execution loop
(`core/orchestrator.md`, section 7). At each checkpoint, work these steps about the
Sprint as a whole, not about individual agents:

1. **Progress toward the Sprint Goal.** How many forecast PBIs have passed the DoD gate,
   how many are in progress, how many are untouched? Is the Sprint Goal still reachable in
   the remaining timebox?
2. **Knowledge sweep.** Before adapting the plan, collect the durable discoveries the
   completed briefs returned, an interface decision, a gotcha, an environment quirk, and
   append each to `.scrum/decisions.md` as a dated one-line entry. Transient status stays
   in the task log. Only knowledge the next brief would otherwise rediscover at cost
   belongs in `decisions.md`.
3. **Adaptation of the plan.** Given what the last batch showed, what changes? Reorder the
   remaining PBIs, resize an item that proved larger than estimated, or drop a
   nice-to-have that does not serve the Sprint Goal. Update the task log.
4. **Impediments.** What is blocking or slowing the work that the Developers cannot
   self-resolve? Record each in `impediments.md` with an owner. Blockers reported verbatim
   by an agent are logged, not smoothed over.

The Daily Scrum has no mandatory format beyond serving its purpose. The steps above are a
useful shape, not a required script.

Decision rules for the checkpoint:

- **The checkpoint is not a status report to the PO or stakeholder.** If the PO wants
  status, point them to the task log and the metrics, and keep the checkpoint by and for
  the Developers.
- **Do not skip the checkpoint because agents "collaborate continuously".** Continuous
  work does not replace the one focused chance to inspect the Sprint Backlog and re-plan
  toward the Sprint Goal. Self-managing means working within boundaries, not skipping
  inspection.
- **When the Sprint Goal looks unreachable,** raise it now, not at the Review. The
  Developers renegotiate scope with the PO; the Sprint length does not change. If the
  Sprint Goal has become obsolete, only the PO may cancel the Sprint.
- **Mid-Sprint scope pressure** goes to the PO. If an outside request or an urgent
  non-goal item appears, the Developers decide whether to take it only if the Sprint Goal
  is not endangered, and inform the PO who owns backlog scope.

## Outputs (`.scrum/` file changes)

- `sprints/sprint-NNN/sprint.md`: task log updated with each PBI's current state and any
  re-plan of the remaining work; a Checkpoint entry appended.
- `impediments.md`: new impediments appended with an owner; resolved ones closed.
- `decisions.md`: the batch's durable discoveries appended as dated one-line entries.
- No new artifact is produced. The checkpoint adapts existing state.

## SM facilitation notes

- **Keep it short and on purpose.** The value is inspect-and-adapt toward the Sprint Goal,
  not a recital of what each agent did. If the checkpoint drifts into status reporting,
  redirect it.
- **Protect the Developers' ownership.** Ensure the checkpoint happens and stays inside
  its timebox, but do not run it or answer for the Developers.
- **Watch for a checkpoint that never changes anything.** A checkpoint that only reports
  and never adapts the plan is a symptom to raise at the Retrospective. Inspection without
  adaptation is wasted.
- **Escalate organizational impediments; coach the team to clear the rest.** The SM
  removes what the team cannot, and does not become the team's impediment triage queue.

## Timebox

Official Scrum bounds the Daily Scrum at fifteen minutes for a Sprint of standard length.

**Adaptation.** The checkpoint sync is proportional to the compressed Sprint and runs
once per task batch rather than once per calendar day. It stays brief, a few exchanges,
so it inspects and adapts without becoming overhead. The fifteen-minute bound maps to
"short enough that it does not slow the batch it sits between". The event's frequency
follows the work rhythm of agent batches, and its purpose, inspect progress toward the
Sprint Goal and adapt the plan, is unchanged.
