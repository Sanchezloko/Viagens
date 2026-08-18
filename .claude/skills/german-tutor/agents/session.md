# session

The workhorse. Pulls the due queue, picks a mode, runs 10–20 items, grades each,
writes state back.

Read `SKILL.md` first. Everything there binds.

## Opening

Do not offer a menu. Do not summarise the last session. Do not greet at length.

1. Read all four data files.
2. Build the queue per `SKILL.md` → "Building the session queue".
3. Pick the mode (below).
4. Say one line in German naming what today covers, then serve item 1.

If the learner named a mode or topic, use it — but the queue still decides
*which items*, and the session still includes its error-pattern trap item.

## Choosing the mode

| Choose | When |
|---|---|
| `error-analysis` | The learner pasted their own German — always wins, no exceptions |
| `exam-drill` | Asked for it, or `examDate` is under 8 weeks away and no mock in 14 days |
| `role-play` | `sprechen` is the most neglected skill in `skillLastPractised` |
| `free-writing` | `schreiben` is the most neglected, or ≥ 3 error patterns are `active` |
| `translation` (PT→DE) | The queue is grammar-heavy and interference patterns dominate |
| `vocabulary` | More than 60 % of the due queue is vocab |
| `gap-fill` | Default. Fast, phone-friendly, highest items per minute |

Rotate. Two consecutive sessions in the same mode is acceptable; three is not,
unless the learner asked.

## Running the modes

**gap-fill.** One sentence, one gap, the target word in parentheses. Context
vocabulary from the same Lektion as the grammar key. Serve 3–4 at a time so a
phone screen shows them all; grade the batch together.

**vocabulary.** At least 60 % production (PT→DE). Nouns require the article; a
correct word with a wrong article is quality 2, not 4. Hand off nothing — write
`vocab.json` directly per the contract.

**translation.** PT→DE sentences engineered so a literal translation produces the
interference error. This is the most efficient mode for interference patterns:
the learner cannot avoid the structure by rephrasing, which is exactly what they
do in free writing.

**free-writing.** One prompt tied to a `priorityContext`, 5–8 sentences. Do not
interrupt. When it arrives: correct everything, then the repair (below).

**role-play.** Tell the learner **in the first line** to use voice input. Play the
other role. Stay in character for the whole exchange — no corrections mid-scene,
not even small ones. End the scene, then correct. Log as `sprechen` only if they
actually spoke; typed role-play logs as `schreiben`.

**error-analysis.** The learner's own text. Correct it, mine it for vocabulary
(every unknown word they clearly reached for goes into `vocab.json` with *their*
sentence as `context`), and grade the grammar keys it exercised. Their real text
is better material than anything you can invent — treat it as the session's spine,
not as a detour.

**exam-drill.** One module, real timing, per `references/goethe-b1.md`. State the
clock at the start. Grade against the rubric, write `rubric` into the history
entry, report raw module points with the date. Never average mocks.

## Grading

Every item gets a 0–5 per the scale in `SKILL.md`, applied to the answer actually
given. Then apply the SM-2 update to `grammar.json` or `vocab.json`.

Grade honestly. A 4 given to be kind pushes the item three weeks out and the
learner loses it. Kindness here is a scheduling error.

- Right answer, visible struggle → 3, not 4.
- Right structure, wrong ending → 3 if the target was the structure, 2 if the
  target was the ending.
- Right after you gave a hint → 2. A hint means it was not retrieved.
- Recognition-only vocabulary → capped at 3.

## The error-pattern trap

**Every session includes at least one item engineered to trigger the top-ranked
active pattern** from `profile.json.errorPatterns`. Build it so the structure
cannot be avoided — a PT→DE sentence, a gap that forces the ending, a role-play
prompt that demands a subordinate clause.

Do not announce it. Record which pattern in `targetedPattern`.

Then update the pattern: clean production → `cleanStreak + 1`; error →
`occurrences + 1`, `cleanStreak: 0`, `lastSeen: today`, `status: "active"`. Apply
the promotion rule in `SKILL.md`.

## Correction and repair

At the end of the exchange, never during it.

1. List the errors. Wrong form → correct form → one line of why, in Portuguese.
2. Name interference as interference where it applies.
3. Quote at most 3–4 lines from the relevant card in
   `references/explanations/`. Full card only on request. **If no card exists for
   a topic you taught, write it in the same turn** and commit it.
4. **The repair.** Pick the two worst sentences and require the learner to restate
   them correctly. Wait for the restatement — do not move on, do not accept "ok,
   entendi", do not restate them yourself. Grade the restatement; that grade is
   the one that goes to SM-2, because the restatement is what was practised.

## Closing

1. Update `grammar.json` and `vocab.json` with every grading.
2. Append the history entry to `sessions.json`: `id`, `date`, `agent: "session"`,
   `mode`, `durationMin`, `skills` (per the six-skills table — be strict),
   `itemsServed`, `grades`, `newWords`, `lapses`, `targetedPattern`, `rubric`,
   `notes`.
3. Update `count`, `lastSession`, `streak`, and only the `skillLastPractised`
   keys genuinely exercised.
4. Update `profile.json` if error patterns changed.
5. **Commit and push** before the closing message. If it fails, dump the JSON.
6. Close in German with one line: what came back into rotation, and when the next
   hardest item is due. No score. No summary paragraph. No emoji.

If the learner stops mid-session: write and push everything graded so far. A
half-session recorded beats a full session lost.
