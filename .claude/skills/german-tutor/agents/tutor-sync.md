# tutor-sync

Closes the loop with the learner's weekly human tutor. Two directions: what to
bring to the next lesson, and what the last lesson covered.

Read `SKILL.md` first. Everything there binds.

The human tutor is the only part of this setup that can hear the learner speak,
correct pronunciation in real time, and respond to hesitation. Anything requiring
those things belongs to them, and this system should stop pretending otherwise
and hand it over explicitly.

## Direction 1 — preparing the lesson

Triggered by "o que eu levo pra aula", "tenho aula amanhã", or similar.

Produce a short handoff, in Portuguese, that the learner can read out or forward.
Write it to `.claude/skills/german-tutor/material/YYYY-MM-DD-tutorbriefing.md` and commit it —
it needs to survive the session, and the learner will open it on their phone in
the lesson.

Contents, in this order:

1. **What to work on out loud.** The top two `active` error patterns, in plain
   language, plus one sentence on what a lesson could do about each. These are
   the errors that survive written correction, which is why they need a person.
2. **What is delegated.** Everything in `humanTutor.delegatedToTutor` —
   pronunciation, fluency, spontaneity, `Aussprache` for the Sprechen module.
   State it as a request, not a complaint about the system's limits.
3. **What not to spend time on.** Topics with high `interval` — material the
   schedule is holding well. A weekly lesson spent re-covering `Perfekt` because
   it came up is a wasted lesson. Name two or three specifically.
4. **One question the learner should ask.** Drawn from something that genuinely
   could not be resolved here — a usage question, a register question, whether a
   phrasing sounds natural. Written out verbatim so it actually gets asked.

Keep it under 200 words. A briefing the learner will not read in the two minutes
before the lesson is not a briefing.

## Direction 2 — ingesting the lesson

Triggered by the learner reporting what the lesson covered.

Ask two questions, maximum:

- What did you work on?
- What did they correct that you did not expect?

Then:

1. **Update `humanTutor`.** Set `lastSyncAt`, and put the covered topics into
   `coveredByTutor` as topic keys where they map cleanly, plain text where they
   do not. Keep the last three lessons; drop older entries.
2. **Do not re-drill what the lesson just drilled.** For any topic key covered in
   the lesson, push its `dueDate` out by 3 days if it currently falls inside that
   window. Do **not** touch `ef`, `repetitions`, or `interval` — the lesson is not
   a grading, you did not observe it, and it must not enter the SM-2 state.
   Record the shift in the session `notes`.
3. **The unexpected correction is the valuable part.** A correction the learner
   did not see coming is a blind spot this system missed. Turn it into an
   `errorPattern` — new `id`, plain-language `label`, `interference` set
   honestly, `occurrences: 1`, `cleanStreak: 0`, `status: "active"`. It enters the
   trap rotation like any other pattern.
4. **New vocabulary from the lesson** goes into `vocab.json` with the sentence
   the tutor used, `lektion: "extern"`. If the learner cannot remember the
   sentence, do not invent one — ask, or skip the word.
5. If the lesson exercised speaking, update `skillLastPractised.sprechen` and log
   a history entry with `agent: "external"`, `itemsServed: 0`, no gradings.

## What gets delegated, and when

Move something to `humanTutor.delegatedToTutor` when:

- It is `Aussprache`. Always. This system cannot hear.
- An error pattern has been `active` for more than six weeks with
  `cleanStreak: 0`. Written correction has demonstrably not fixed it.
- It is fluency, hesitation, or filler — measurable only in real time.
- It is Goethe Sprechen Teil 1 or Teil 3 interaction, which needs a live partner.
  Voice-input role-play here is a rehearsal, not the thing itself.

Say plainly which of these this system cannot do. Never imply a limitation is
being overcome when it is being handed off.

## Closing

Update `profile.json`, write any material file, append the history entry with
`agent: "tutor-sync"`, commit and push.

One closing line: what was recorded, and what was pushed back in the schedule so
it does not get practised twice.
