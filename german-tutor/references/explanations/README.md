# Explanation cards

One card per grammar topic key, written in Portuguese, contrasting German with
Brazilian Portuguese. This is the depth layer: `SKILL.md` forbids long theory in
a session, and these cards are how the depth exists anyway.

## How a card is used

- In a session, quote **only the `Kurzfassung`** — three lines, no more. That is
  the whole point of the field.
- Expand to the full card when the learner asks: "explica melhor", "mais
  detalhe", "por quê", "não entendi".
- The `Erros previsíveis` section is not decoration. It is the source of
  `errorPatterns` in `profile.json` and of the trap items every session must
  include. When the learner makes one of these errors, name it by its card.

## The corpus is seeded, not complete

Cards exist for the highest-interference topics. Many keys in
`curriculum-a2.md` and `curriculum-b1.md` have none yet.

**If a session teaches a topic with no card, write the card in the same turn and
commit it.** Do not teach from memory when a card exists. Do not refuse to teach
because one does not. The corpus grows by use, which means it grows in the order
this particular learner actually needs.

## Card format

Copy this exactly. The heading is the topic key, verbatim, so a card can be found
by key.

```markdown
## <TopicKey>

**Kurzfassung** (3 linhas — é isto que a sessão cita)
> Linha 1: a regra em uma frase.
> Linha 2: o contraste com o português.
> Linha 3: um exemplo mínimo.

**Regra completa.** …

**Contraste com o português.** …

**Erros previsíveis.**
1. …
2. …

**Exemplos.**
- Alemão — tradução
```

## Files

| File | Covers |
|---|---|
| `faelle-und-praepositionen.md` | Cases, two-way prepositions, verbs with fixed prepositions, genitive prepositions |
| `verbsystem.md` | Tenses, modals, reflexives, passive, Konjunktiv II |
| `satzbau.md` | Word order, subordinate clauses, connectors, relative clauses, infinitive clauses |
| `nomen-und-adjektive.md` | Adjective endings, weak nouns, genitive |
