# Curriculum A1–A2 — canonical topic key registry

Schritte International Neu, Bände 1–4 (Hueber). This file is the **registry of
permanent identifiers**, not teaching material. See `SKILL.md` → "Topic keys are
permanent identifiers" before touching anything here.

Rules for this file:

- The `Key` column is an identity. It is never renamed, re-cased, or
  re-prefixed. The `Topic` and `Lektion` columns are editable metadata.
- Keys in Bände 1–3 are **inherited verbatim** from the previous version of this
  system, including the inconsistency where A1 keys carry an `A1_` prefix and
  A2.1 keys do not. That inconsistency stays: renaming would orphan the
  schedules attached to those strings.
- Grammar keys go in `grammar.json`. Thematic keys never go in `grammar.json` —
  they appear only as `topicKey` metadata on words in `vocab.json`. The two
  namespaces must not collide.
- Adding a key here and seeding it in `grammar.json` happens in the same turn.

---

## Band 1 — A1.1 (Lektionen 1–7)

### Grammar

| Key | Topic | Lektion |
|-----|-------|---------|
| `A1_Personalpronomen` | Personal pronouns: ich, du, er, sie, es, wir, ihr, sie, Sie | B1/L1 |
| `A1_Praesens_Regelmaessig` | Present tense, regular verbs | B1/L1 |
| `A1_Praep_aus_in` | Prepositions aus / in for origin and location | B1/L1–2 |
| `A1_W_Fragen` | W-questions: wer, was, wie, wo, woher, wohin, wann, warum | B1/L1 |
| `A1_Ja_Nein_Fragen` | Yes/no questions and basic word order | B1/L1 |
| `A1_Sein_Haben` | Present tense of sein and haben | B1/L2 |
| `A1_Possessivpronomen_Nom` | Possessives in the nominative | B1/L2 |
| `A1_Zahlen` | Numbers 0–1 000 000 | B1/L2–3 |
| `A1_Nullartikel` | Zero article | B1/L3 |
| `A1_Artikel_Indef` | Indefinite article ein/eine | B1/L3 |
| `A1_Artikel_Neg` | Negative article kein/keine | B1/L3 |
| `A1_Plural` | Noun plurals | B1/L3 |
| `A1_Verb_Essen` | Strong verbs with vowel change (essen, nehmen, sprechen) | B1/L3 |
| `A1_Artikel_Def` | Definite articles der/die/das | B1/L4 |
| `A1_Negation` | Negation with nicht | B1/L4 |
| `A1_Adverbien_Ort` | Adverbs of place: hier, dort, da | B1/L4 |
| `A1_Trennbare_Verben_Basis` | Separable verbs, basic | B1/L5 |
| `A1_Satzstellung` | Verb-second (V2) | B1/L5 |
| `A1_Praep_Uhrzeit` | Time prepositions: am, um, von…bis | B1/L5 |
| `A1_Uhrzeit` | Telling the time | B1/L5 |

### Thematic

| Key | Area | Lektion |
|-----|------|---------|
| `A1_Begruessung` | Greetings, introductions, farewells | B1/L1 |
| `A1_Laender_Sprachen` | Countries, nationalities, languages | B1/L1 |
| `A1_Alphabet` | Alphabet and spelling aloud | B1/L1 |
| `A1_Familie` | Family and relationships | B1/L2 |
| `A1_Telefon` | Phone numbers and personal data | B1/L2 |
| `A1_Lebensmittel` | Food, drink, the market | B1/L3 |
| `A1_Preise` | Prices and quantities | B1/L3 |
| `A1_Wohnung` | Home, rooms, furniture | B1/L4 |
| `A1_Farben` | Colours | B1/L4 |
| `A1_Tagesablauf` | Daily routine | B1/L5 |
| `A1_Wochentage` | Days of the week, opening hours | B1/L5 |

## Band 2 — A1.2 (Lektionen 8–14)

### Grammar

| Key | Topic | Lektion |
|-----|-------|---------|
| `A1_Wortstruktur` | Compound nouns and common suffixes | B2/L8 |
| `A1_Praeteritum_Sein_Haben` | Präteritum of sein and haben | B2/L8 |
| `A1_Temp_Praepositionen` | vor, nach, seit, in, an, um | B2/L8 |
| `A1_Modalverben_Intro` | können, möchten, müssen | B2/L9 |
| `A1_Pronomen_Man` | The pronoun man | B2/L9 |
| `A1_Imperativ_Basis` | Imperative, du and Sie | B2/L9 |
| `A1_Possessivpronomen_Akk` | Possessives in the accusative | B2/L10 |
| `A1_Praepositionen_Ort` | Dative prepositions of place | B2/L10–11 |
| `A1_Konjunktiv2_Intro` | könnte, würde, hätte | B2/L11 |
| `A1_Praep_Richtung` | durch, über, entlang | B2/L11 |
| `A1_Vergleich` | Comparison: größer als, genauso … wie | B2/L12 |
| `A1_Verben_Dativ` | gefallen, gehören, passen, schmecken | B2/L12 |
| `A1_Akkusativ` | Accusative articles and pronouns | B2/L13 |
| `A1_Ordinalzahlen` | Ordinals | B2/L13 |
| `A1_Personalpron_Akk` | mich, dich, ihn, sie, uns, euch | B2/L13 |
| `A1_Konjunktionen_Basis` | und, aber, oder, denn | B2/L14 |

### Thematic

| Key | Area | Lektion |
|-----|------|---------|
| `A1_Berufe` | Professions and workplaces | B2/L8 |
| `A1_Stadt_Orientierung` | City, hotel, tourism | B2/L9 |
| `A1_Koerper_Gesundheit` | Body, health, at the doctor | B2/L10 |
| `A1_Verkehr` | Transport and timetables | B2/L11 |
| `A1_Kundenservice` | Customer service and complaints | B2/L12 |
| `A1_Kleidung` | Clothing and shopping | B2/L12–13 |
| `A1_Feste` | Celebrations and invitations | B2/L13–14 |
| `A1_Zukunft` | Future plans | B2/L14 |

## Band 3 — A2.1 (Lektionen 1–7)

### Grammar

| Key | Topic | Lektion |
|-----|-------|---------|
| `Perfekt` | Perfekt with haben and sein | B3/L1–2 |
| `Praeteritum` | Präteritum of haben, sein, modals | B3/L2 |
| `Modalverben` | Full modal system | B3/L3 |
| `Imperativ` | Imperative, du / ihr / Sie | B3/L3 |
| `Trennbare_Verben` | Separable verbs, incl. in the Perfekt | B3/L1–3 |
| `Reflexive_Verben` | sich waschen, sich freuen, sich ärgern | B3/L4 |
| `Akkusativ` | Accusative: articles, pronouns, adjective endings | B3/L1–4 |
| `Dativ` | Dative: articles, pronouns, dative prepositions | B3/L4–5 |
| `Wechselpraepositionen` | Two-way prepositions, Akk vs. Dat | B3/L5 |
| `Possessivpronomen` | Possessives across cases | B3/L5 |
| `Komparation` | Comparative and superlative | B3/L6 |
| `Konjunktionen` | weil, dass, wenn, ob — verb-final | B3/L6–7 |
| `Indefinitpronomen` | man, jemand, niemand, etwas, nichts | B3/L7 |
| `Konjunktiv2_A2` | würde, könnte, hätte for requests and wishes | B3/L6–7 |

### Thematic

| Key | Area | Lektion |
|-----|------|---------|
| `Alltag` | Routine, appointments, schedules | B3/L1 |
| `Wohnen` | Housing, rooms, neighbours | B3/L2 |
| `Essen` | Food, cooking, restaurants | B3/L3 |
| `Einkaufen` | Shopping, clothing, prices | B3/L4 |
| `Gesundheit` | Body, health, pharmacy | B3/L5 |
| `Reisen` | Travel, transport, directions | B3/L6 |
| `Freizeit` | Hobbies, leisure, sport | B3/L7 |
| `Arbeit` | Work and workplace communication | B3/L1–2 |
| `Kommunikation` | Calls, messages, written appointments | B3/L3–4 |

## Band 4 — A2.2 (Lektionen 8–14) — NEW KEYS, NOT YET IN USE

The previous system stopped at Band 3, so none of these keys carry history and
all of them are still safe to rename. **This is the last moment that is true.**
Once `grammar.json` holds them, they are frozen.

Lektion numbers below are marked `B4/L?` where I could not confirm the mapping
against the book. The keys do not depend on those numbers — filling them in
later is metadata editing, not renaming.

### Grammar

| Key | Topic | Lektion |
|-----|-------|---------|
| `Adjektivdeklination_Def` | Adjective endings after der/die/das | B4/L? |
| `Adjektivdeklination_Indef` | Adjective endings after ein/kein/mein | B4/L? |
| `Adjektivdeklination_Null` | Adjective endings with no article | B4/L? |
| `Superlativ_Attributiv` | der beste, am besten in attributive use | B4/L? |
| `Relativsatz_Nom_Akk` | Relative clauses, nominative and accusative | B4/L? |
| `Genitiv` | Genitive, incl. von + Dativ as the spoken alternative | B4/L? |
| `N_Deklination` | Weak masculine nouns: der Student → den Studenten | B4/L? |
| `Praeteritum_Vollverben` | Präteritum of full verbs, written narrative | B4/L? |
| `Plusquamperfekt` | Plusquamperfekt with nachdem | B4/L? |
| `Passiv_Praesens` | Present passive: werden + Partizip II | B4/L? |
| `Infinitiv_mit_zu` | Infinitive with zu after verbs and expressions | B4/L? |
| `Finalsatz_um_zu_damit` | Purpose: um … zu vs. damit | B4/L? |
| `Konzessiv_obwohl_trotzdem` | Concession: obwohl vs. trotzdem | B4/L? |
| `Temporalsatz_als_wenn` | als vs. wenn for past time | B4/L? |
| `Temporalsatz_bevor_nachdem` | bevor, nachdem, während | B4/L? |
| `Indirekte_Fragen` | Indirect questions with ob and W-words | B4/L? |
| `Konnektoren_Hauptsatz` | deshalb, deswegen, trotzdem, dann — position 1 inversion | B4/L? |
| `Verben_mit_Praeposition` | Verbs with fixed prepositions: warten auf, sich freuen über | B4/L? |
| `Praepositionaladverbien` | worauf / darauf, worüber / darüber | B4/L? |
| `Reflexive_Verben_Praeposition` | Reflexives with fixed prepositions | B4/L? |
| `Verben_Dativ_Akkusativ` | Two-object verbs and pronoun order | B4/L? |
| `Wortstellung_TeKaMoLo` | Middle-field order: temporal, kausal, modal, lokal | B4/L? |
| `Konjunktiv2_Rat` | Advice and hypotheticals: sollte, an deiner Stelle würde ich | B4/L? |

### Thematic

| Key | Area | Lektion |
|-----|------|---------|
| `Zusammenleben` | Living together, flatshares, neighbours, conflict | B4/L? |
| `Wohnungssuche` | Flat hunting, contracts, viewings | B4/L? |
| `Bildung` | School, courses, qualifications, further training | B4/L? |
| `Berufsleben` | Applications, interviews, workplace roles | B4/L? |
| `Behoerden` | Authorities, forms, appointments, Anmeldung | B4/L? |
| `Geld_Finanzen` | Bank, contracts, bills, insurance | B4/L? |
| `Natur_Umwelt` | Nature, weather, environment, recycling | B4/L? |
| `Medien_Technik` | Internet, devices, media habits | B4/L? |
| `Beziehungen` | Friendship, relationships, feelings | B4/L? |
| `Feste_Traditionen` | Festivals, customs, German vs. Brazilian | B4/L? |
