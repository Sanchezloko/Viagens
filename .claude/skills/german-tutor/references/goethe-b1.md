# Goethe-Zertifikat B1 — format, timings, scoring

Reference for `exam-drill` mode and for rubric-based correction of Schreiben and
Sprechen. Used by `agents/session.md`, `agents/tracker.md` and
`agents/immersion.md`.

**Verify before the learner books.** Exam formats are revised periodically. The
structure below reflects the modular Goethe-Zertifikat B1 as commonly examined;
confirm current details at `goethe.de` and against the official *Modellsatz*
before treating any timing as exact. Do not present these numbers to the learner
as freshly verified when they have not been.

## Overall

- Four modules: **Lesen, Hören, Schreiben, Sprechen**.
- Modules are **individually bookable and individually retakeable**. This matters
  for planning: a learner strong in Lesen and weak in Hören does not have to
  re-sit everything.
- **Pass mark: 60 % per module**, scored on a 100-point scale per module.
- Grade bands: 100–90 *sehr gut*, 89–80 *gut*, 79–70 *befriedigend*, 69–60
  *ausreichend*, below 60 *nicht bestanden*.
- Total exam time roughly 3 hours plus the speaking appointment.

---

## Lesen — 65 minutes, 5 parts, 30 items

| Teil | Text type | Task | Items |
|---|---|---|---|
| 1 | Blog entry or personal email | richtig/falsch plus multiple choice | 6 |
| 2 | Two short press texts | multiple choice, 3 per text | 6 |
| 3 | Ten short adverts | match each situation to an advert; some have no match | 7 |
| 4 | Readers' opinions on one topic | decide *dafür* or *dagegen* for each writer | 7 |
| 5 | Rules text — Hausordnung, Benutzerordnung, terms of use | multiple choice | 4 |

Drill focus for this learner: **Teil 3 is a trap for Brazilians**, because the
distractor adverts share vocabulary with the target situation and the match hangs
on a small preposition or a negation. Teil 5 is dense formal register — passive,
genitive prepositions, nominal style. That is exactly the `Nominalstil` and
`Praepositionen_Genitiv` material in `curriculum-b1.md`.

## Hören — approx. 40 minutes, 4 parts, 30 items

| Teil | Audio | Heard | Task | Items |
|---|---|---|---|---|
| 1 | Five short announcements, voicemails, radio spots | twice | richtig/falsch plus multiple choice | 10 |
| 2 | A monologue — guided tour, presentation | once | multiple choice | 5 |
| 3 | An everyday conversation | once | richtig/falsch | 7 |
| 4 | A discussion with several speakers | twice | match statements to speakers | 8 |

The parts heard **once** are where the exam is won or lost. Practising with
pause-and-replay builds a false sense of readiness.

Because this system cannot play audio, Hören preparation is: the learner listens
to an assigned external source, then writes in German what they understood, and
that summary is corrected. See "The six skills" in `SKILL.md`.

## Schreiben — 60 minutes, 3 tasks

| Teil | Task | Register | Length | Suggested time |
|---|---|---|---|---|
| 1 | Email to a friend — invite, cancel, react to news | informal, du | ~80 words | 20 min |
| 2 | Forum post giving an opinion on a topic | neutral to informal | ~80 words | 25 min |
| 3 | Formal email — apology, cancellation, request to an institution | formal, Sie | ~40 words | 15 min |

**Rubric — four criteria, weighted equally.** Correct against these and name the
criterion; do not give an undifferentiated "good".

| Criterion | What is judged |
|---|---|
| **Erfüllung** | Are all bullet points from the task addressed, at the required length, in the right text type? |
| **Kohärenz** | Connectors, paragraphing, logical order, appropriate opening and closing formulas. |
| **Wortschatz** | Range and precision. Repetition of the same three verbs costs points even when correct. |
| **Strukturen** | Range and accuracy of grammar. Subordinate clauses, tense control, case. |

Recurring failure modes to check first in this learner's writing:

- Teil 3 written in du-form or with an informal sign-off. Register failure is an
  *Erfüllung* problem, not a politeness quibble, and it is heavily penalised.
- All four bullet points mentioned but one only in a half-sentence. Each point
  needs development, not acknowledgement.
- Wrong closing formula: `Mit freundlichen Grüßen` for Teil 3, `Liebe Grüße` or
  `Viele Grüße` for Teil 1. Brazilians often transfer *Atenciosamente* register
  inconsistently.
- Word count far over. Over-length costs time and adds errors; it earns nothing.

## Sprechen — approx. 15 minutes, in pairs, with 15 minutes' preparation

| Teil | Task | Time |
|---|---|---|
| 1 | Plan something together with the partner — a trip, a party, a farewell gift | ~3 min |
| 2 | Present a topic, roughly 5 structured points | ~3 min each |
| 3 | Give feedback on the partner's presentation and ask a question about it | ~2 min |

The standard **Teil 2 five-point structure**, which is what to drill:

1. Introduce the topic and say how you will structure it.
2. Your own experience with it.
3. The situation in your home country — for this learner, Brazil, and this is a
   built-in advantage worth exploiting deliberately.
4. Advantages and disadvantages, plus your own opinion.
5. Close and thank the audience.

**Rubric — five criteria.**

| Criterion | What is judged |
|---|---|
| **Erfüllung** | Task completed, all points covered, appropriate length. |
| **Interaktion** | Reacting to the partner, taking turns, asking back. Teil 1 and 3 live here. |
| **Aussprache** | Pronunciation and intonation; comprehensibility over accent. |
| **Wortschatz** | Range and precision. |
| **Strukturen** | Grammatical range and accuracy. |

**Aussprache cannot be assessed by this system.** It is delegated to the human
tutor — record it in `profile.json.humanTutor.delegatedToTutor` and do not
silently score it. The specific Brazilian issues to hand over: `ü`/`ö`, final
devoicing, `h` (aspirated in German, silent in PT), `r`, and syllable-timed
rhythm against German stress-timing.

Interaktion is partly practisable here through voice-input role-play; a learner
who prepares only monologue Teil 2 typically fails on Teil 1.

---

## Using this file in `exam-drill` mode

- Always drill **one module under its real timing**. A Lesen Teil 3 done leisurely
  is not exam practice.
- Report the result as raw module points out of 100 with the date and the fact
  that it was one mock. Never average mock results, never turn them into a
  running score, and never present a mock as a prediction.
- Write the per-criterion breakdown into the session's `rubric` field so the
  tracker can compare module to module over time.
- Items in a mock are still graded 0–5 and still update the schedule. A mock is a
  session, not a separate universe.
