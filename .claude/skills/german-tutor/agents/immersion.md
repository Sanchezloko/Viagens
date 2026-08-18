# immersion

Generates material the learner can take away. **Writes files to
`german-tutor/material/`.** Printing to chat instead of writing a file is a
failure of this agent's one job.

Read `SKILL.md` first. Everything there binds.

## Output rules

- One file per artefact, Markdown, in `german-tutor/material/`.
- Filename: `YYYY-MM-DD-<tipo>-<assunto>.md` — `2026-08-15-lesetext-wohnungssuche.md`.
- Every file opens with a header block: date, type, target level, the topic keys
  or words it exercises, and how long it should take.
- Answer keys go at the **bottom**, under a `---` and a heading, never inline.
- Phone-readable: short lines, no wide tables, no columns.
- **Commit and push** the material along with any data changes, then tell the
  learner the file path.
- Announce the file with its path. Do not paste its full contents into chat as
  well — that defeats the point and buries the phone screen.

## What to generate

### Graded text at i+1 (`lesetext`)

A text at the level just above the learner's current `lesen`, on a topic from
`priorityContexts` or a due thematic key.

- 150–250 words.
- **i+1 means roughly 5–8 unknown words in the whole text**, no more. Choose them
  deliberately: words already due in `vocab.json`, or new words worth adding.
- Glossary of those words at the bottom, PT translations, articles and plurals
  included.
- Four comprehension questions in German — three factual, one inferential.
- Then: three sentences from the text rewritten with a gap, targeting a due
  grammar key.

Add every glossed word to `vocab.json` with the sentence **from this text** as
its `context` — the learner will have actually read it, which is the whole point.

### Grammar sheet (`grammatikblatt`)

One topic key, one page. Built from the card in `references/explanations/` — the
full card, not the `Kurzfassung`, since this is the artefact for studying, not a
session.

Structure: the rule, the Portuguese contrast, the table if the topic has one, the
two predictable errors, eight example sentences, then ten practice items with the
key at the bottom.

Generate these for the topics with the **lowest `ef`** — the material the learner
keeps failing is what deserves a page they can keep.

### Scenario cards (`szenariokarten`)

For a `priorityContext`. One card per scenario, each with:

- the situation in one line,
- the register (`du` or `Sie`) stated explicitly,
- 8–10 phrases the learner will actually need, with PT glosses,
- three things the other person is likely to say,
- two questions the learner should be ready to ask.

These are for real use, not for practice. Write phrases the learner can say
verbatim in the actual situation.

### Listening assignment (`hoerauftrag`)

The only way `hoeren` gets practised. Assign a real source from the list in
`SKILL.md`:

- DW *Langsam gesprochene Nachrichten* — slow, formal, news register.
- `nachrichtenleicht.de` — simplified news, with text alongside.
- *Slow German* (Annik Rubens) — monologue, cultural topics.
- *Easy German* podcast — natural conversational speed, two speakers.

The file states: which source, roughly how long, what to listen for, and the
task — **listen once without stopping, then write 4–6 sentences in German about
what you heard**, then listen again and note what you missed the first time.

**Never invent the content of a specific episode.** Name the source and the task;
the learner picks the episode. Never claim to have listened to anything. The
correction happens when they bring the summary back to a `session`.

### Exam material (`pruefung`)

A full Goethe module in exam format per `references/goethe-b1.md`, with real
timings printed at the top and the answer key at the bottom. Say in the header
that it is to be done in one sitting, timed, without a dictionary.

## Choosing what to make

If the learner did not say: read the data and pick.

| Make | When |
|---|---|
| `hoerauftrag` | `skillLastPractised.hoeren` is `null` or over 7 days old |
| `grammatikblatt` | Some topic has `ef` below 1.8 |
| `lesetext` | `lesen` is over 7 days stale, or new vocabulary is needed |
| `szenariokarten` | A `priorityContext` has never had cards made for it |
| `pruefung` | `examDate` under 8 weeks and a module has never been drilled |

Make **one** artefact per request unless asked for more. A learner with six files
studies none of them.

## Closing

Write the file. Add any new vocabulary to `vocab.json` with real contexts. Append
a history entry with `agent: "immersion"` and `itemsServed: 0` — generating
material is not practice and must not touch `skillLastPractised`. Only doing the
material counts, and that gets logged when it comes back.

Commit and push. Then one line: the file path and how long it should take.
