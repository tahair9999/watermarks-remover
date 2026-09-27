---
name: story-structure-audit
description: >
  Audit fiction at the level of narrative structure rather than prose style — plot
  tracks, theme explicitness, moral ambiguity, event escalation, temporal complexity,
  revelation depth, perspective — using the feature space from StoryScope (arXiv
  2604.03136). Use this whenever someone asks why a story feels flat, generic, tidy,
  formulaic, or "AI-ish"; wants a structural or developmental edit of a short story,
  chapter, or manuscript; is revising a draft an LLM helped write; or asks what makes
  machine-written fiction recognizable beyond word choice. Also use for developmental
  feedback that goes past line edits — pacing, subplot structure, ending tidiness,
  character agency, flashback use. Produces a per-dimension scorecard and specific
  revision moves tied to the weakest dimensions. Not for copyediting, prose polish,
  or invisible-character cleanup, and never a verdict that a particular text was
  machine-written.
license: MIT
metadata:
  source: "Russell, Rajendhran, Pham, Iyyer, Wieting. StoryScope: Investigating idiosyncrasies in AI fiction. arXiv:2604.03136v6"
  source_code: "https://github.com/jenna-russell/storyscope (MIT)"
---

# Story structure audit

Most feedback on AI-assisted fiction attacks the prose: the tricolons, the "not just
X but Y", the em-dashes. StoryScope shows that the deeper signal is *architectural*.
A classifier using only discourse-level narrative features — no stylistic cues at all
— separated human from AI fiction at 93.2% macro-F1 across 61,608 stories. More
telling: when the researchers used span-level artifact removal to strip surface
prose tells from 278 machine-written stories, detection fell by only 1.6 points
(95.5% to 93.9% macro-F1).

That finding is the reason this skill exists. **Rewriting sentences does not change
the shape of a story.** If a draft reads as machine-made, the cause is usually
structural, and structure is where the revision has to happen. Which is simply to
say: the fix is craft work, not disguise.

Use this skill to locate which structural choices are doing the damage, and to
propose revisions that change them.

## Scope and honesty constraints

These matter, and getting them wrong makes the audit worse than useless:

- **Report tendencies, never verdicts.** 93.2% macro-F1 is a corpus-level number. On
  a single story it means nothing. Never tell someone their text "is AI-generated",
  "reads as human", or "will pass" any detector. Say which structural choices are
  common in machine-written fiction and which are rarer, and stop there.
- **Every feature is a tendency, not a rule.** Plenty of excellent human fiction is
  linear, single-track, and states its theme outright. A story scoring "AI-leaning"
  across the board may just be a tidy, sincere, conventional story — which is a
  legitimate thing to write. Flag the pattern; let the author decide.
- **Know the distribution you are comparing against.** The paper's human baseline is
  published novels (from Books3), and the stories on both sides run roughly 5,000
  words. So the implicit comparison is *published literary fiction*. Applying these
  features to flash fiction, genre-formula work, or a first draft is a stretch;
  applying them to nonfiction — essays, personal statements, applications, reports —
  is outside what the paper measured. Say so when the input is out of distribution
  rather than scoring it anyway.
- **This is a craft tool.** It tells a writer what is thin in their story. It is not
  an evasion aid, and it cannot certify authorship in either direction. If someone
  wants it to launder machine-written work as their own for a context that requires
  original authorship, the audit does not help them and the framing should not
  pretend otherwise.

## Workflow

### 1. Check the input fits

Confirm the text is fiction and long enough to have structure — a scene or two at
minimum, ideally a complete story or chapter. For anything under ~1,000 words, say
that several dimensions (subplot structure, event escalation, revelation depth)
cannot be assessed on that length, and audit only what is present.

If the text is nonfiction, say plainly that the feature space was induced on and
validated against fiction, and offer ordinary developmental feedback instead.

### 2. Read for structure, not sentences

Read the whole text before scoring. Resist noting prose issues — they are a
different job, and attention spent on them is attention not spent on architecture.
Build a rough map as you read: who wants what, what happens in what order, when
the reader learns each thing, where time moves.

### 3. Score the twelve checkpoints

Score each checkpoint below. These are the highest-signal items from the paper's
30-feature core set, which retains about 91% of the full model's discriminative
power. Read `references/core-features.md` for the full rubric, the exact scoring
scales, and the measured human/AI split on each.

Score 1–5 where noted, or pick the stated category. Record a line of evidence from
the text for each — a scorecard without evidence is not auditable, and forces you
to actually locate the thing rather than form an impression.

| # | Checkpoint | Dimension | AI-leaning looks like |
|---|---|---|---|
| 1 | Thematic explicitness | Situatedness | 4–5: theme stated outright, often in closing lines |
| 2 | Narratorial thematic commentary | Situatedness | Narrator steps out to gloss the meaning |
| 3 | Agency in resolution | Plot | `protagonist_choice` — the ending turns on a decision |
| 4 | Plot track count | Plot | Single track, no live subplots, few loose ends |
| 5 | Ending tidiness | Plot | Everything resolved; extended denouement |
| 6 | Protagonist moral position | Agents | Clearly sympathetic, choices not compromising |
| 7 | Event escalation curve | Events | Flat or evenly-stepped intensity, no lulls or spikes |
| 8 | Chronological discontinuity | Temporal | 1–2: strict forward sequence |
| 9 | Recontextualization depth | Revelation | 1–2: reveals add information, don't reframe |
| 10 | Emotion conveyed how | Agents | Physical sensation; rarely a named emotion |
| 11 | Intertextual strategy | Situatedness | Vague allusion rather than named work/author |
| 12 | Reader address / frame breaking | Perspective | Sealed frame, narrator never acknowledges reader |

### 4. Compute the profile

Run the scorer to turn the twelve scores into a profile and a ranked priority list:

```bash
python3 scripts/score.py --interactive
# or: python3 scripts/score.py --scores 5,yes,protagonist_choice,1,4,sympathetic,flat,1,2,physical,vague,no
```

It reports an AI-lean index, which dimensions are most extreme, and which are
already in human-typical range so you leave them alone. The arithmetic is trivial
but doing it by hand invites drift toward whatever impression you formed while
reading, which defeats the point of scoring.

### 5. Write the audit

Use this structure:

```
## Structural profile
[2-3 sentences: overall shape, and the honest caveat that this describes
tendencies in a corpus, not a verdict on this story]

## Scorecard
[table: checkpoint, score, evidence from the text]

## The three things costing the most
[For each: what the text does now, why it flattens the story — in craft terms,
not detection terms — and a concrete revision move]

## Dimensions already working
[What not to touch. Writers need this; without it they over-revise.]
```

Lead with craft, not detection. "Your ending resolves every thread, which drains
the last page of tension" is useful. "Your ending scores AI-leaning on tidiness"
is not — it tells the writer about a classifier instead of about their story.

### 6. Propose revisions that change structure

Each recommendation must alter the story's architecture, not its wording. See
`references/revision-moves.md` for worked moves per dimension. The test for a good
recommendation: could the author apply it by editing sentences? If yes, it is not a
structural fix and belongs in a different pass.

Weak: "make the theme less explicit."
Strong: "Cut the final two paragraphs where Mara names what she learned. End on the
unreturned phone call. The theme survives in the gesture; the reader does it."

## Reference files

- `references/core-features.md` — full rubric for all twelve checkpoints, scoring
  scales, and measured human/AI rates. Read before scoring.
- `references/dimensions.md` — the ten dimensions, their feature counts, and what
  the paper found in each. Read when you need to go beyond the core twelve.
- `references/revision-moves.md` — concrete structural revisions per dimension.
  Read when writing recommendations.
- `references/model-fingerprints.md` — per-model tendencies the paper identified.
  Read only if asked which system likely drafted something, and note that six-way
  attribution ran at 68.4% macro-F1, so these are weak signals at best.
