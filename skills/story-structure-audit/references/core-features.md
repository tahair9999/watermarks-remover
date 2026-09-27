# Core feature rubric

The twelve checkpoints, with scoring scales and the measured split from StoryScope
(arXiv:2604.03136v6). Percentages are the share of stories in each corpus showing
the trait; "AI" pools the five generators the paper tested.

Two cautions before you use these numbers. First, they describe corpora, not
individual stories — a single story landing on the AI side of a split tells you
almost nothing on its own, and the audit's value is in the *pattern* across all
twelve. Second, the human corpus is published novels, so "human-typical" here means
"typical of published literary fiction", which is a high and specific bar.

---

## 1. Thematic explicitness and moralizing

**Dimension:** Situatedness
**Prompt:** How explicitly does the story articulate its themes or morals?
**Scale:** 1 (theme wholly implicit) to 5 (theme stated outright and underlined)
**Split:** AI averages roughly 20% higher on the 1–5 scale.

The single most reliable item in the set. Machine drafts tend to distrust the
reader — they arrive at meaning and then explain it, often in the final beat.

## 2. Narratorial thematic commentary

**Dimension:** Situatedness
**Prompt:** Does the narrator explicitly comment on themes beyond the characters'
perspectives?
**Scale:** binary (yes / no)
**Split:** AI 77%, human 52%.

Distinct from #1: this is specifically the narrator stepping outside the characters
to gloss the story's significance, as opposed to a character voicing the theme.

## 3. Agency in resolution

**Dimension:** Plot
**Prompt:** Is the resolution driven by the protagonist's choices or by external
events?
**Scale:** `protagonist_choice` / `mixed` / `external_fate`
**Split:** protagonist-driven resolutions — AI 69%, human 46%.

Machine drafts reliably deliver the satisfying arc where the protagonist decides and
the decision settles the story. Published fiction lets accident, other people, and
circumstance carry more of the ending.

## 4. Plot track count

**Dimension:** Plot
**Prompt:** How many distinct plot lines remain active, and how many threads are
left unresolved?
**Scale:** 1 (single track, nothing loose) to 5 (multiple live tracks, threads left
open)
**Split:** AI favors single-track narratives with fewer loose ends; human stories
carry more subplots.

## 5. Ending tidiness

**Dimension:** Plot
**Prompt:** How completely does the ending resolve what the story raised?
**Scale:** 1 (abrupt or openly unresolved) to 5 (everything resolved, extended
denouement)
**Split:** AI produces markedly tidier endings; humans use ambiguous endings more
often. Gemini was the most extreme on extended denouements.

## 6. Protagonist moral position

**Dimension:** Agents
**Prompt:** Is the protagonist morally ambivalent, or clearly sympathetic?
**Scale:** `ambivalent` / `mixed` / `sympathetic`
**Split:** morally ambivalent protagonists — human 59%, AI 38%.

The gap is not about likability. It is about whether the story lets the protagonist
be *implicated* — whether their choices cost someone else something the story
declines to excuse.

## 7. Event escalation curve

**Dimension:** Events
**Prompt:** How does event intensity move across the story?
**Scale:** `flat` / `even_steps` / `uneven` / `spiked`
**Split:** the paper singles out flat escalation as the most distinctive trait of
one generator, and finds AI event structure generally smoother.

Human-typical curves have lulls, false peaks, and scenes whose intensity does not
serve the next rung up.

## 8. Degree of chronological discontinuity

**Dimension:** Temporal structure
**Prompt:** How often does the narrative jump across time?
**Scale:** 1 (strict forward sequence) to 5 (heavily discontinuous)
**Split:** humans employ substantially more flashback, flash-forward, and nonlinear
arrangement. Called out in the abstract as a headline difference.

Note the direction of the causal claim: this is not "add a flashback and the story
improves". Discontinuity in published fiction is usually a *consequence* of the
story needing two time frames to mean what it means.

## 9. Depth of recontextualization after surprise

**Dimension:** Revelation
**Prompt:** How extensively does a revelation force reinterpretation of earlier
scenes?
**Scale:** 1 (none — the reveal only adds information) to 5 (complete re-reading of
what came before)
**Split:** human stories score higher.

A machine-typical reveal answers a question. A human-typical reveal changes what
earlier scenes *were*.

## 10. Emotion conveyed how

**Dimension:** Agents
**Prompt:** Through what channel is character emotion primarily conveyed?
**Scale:** `physical` / `mixed` / `named`
**Split:** the widest single gap in the paper. Emotion via physical sensation — AI
81%, human 38%. Explicit emotion labels — human 29%, AI 8%. AI also used
smell-based imagery at 82% versus 57%.

This is the "show don't tell" rule metabolized into a tic. Machine drafts route
nearly every feeling through the body — tightening chests, clenching jaws, a smell
that brings it all back. Published fiction names feelings far more often than
workshop advice implies.

## 11. Intertextual strategy

**Dimension:** Situatedness
**Prompt:** What kind of intertextual engagement does the story employ?
**Scale:** multi-select — `explicit_named` / `retelling` / `pastiche` /
`myth_religion` / `self_referential` / `vague_allusion` / `none`
**Split:** named references to specific texts and authors — human 47%, AI 24%. Vague
allusion — AI 72%, human 50%.

Machine drafts gesture at a literary register without naming anything. Human
stories name the book, the song, the painter.

## 12. Reader address and frame breaking

**Dimension:** Perspective
**Prompt:** Does the narration acknowledge the reader or its own status as a telling?
**Scale:** binary (yes / no), scored separately for direct address
**Split:** frame breaking — human 67%, AI 39%. Direct reader address — human 28%,
AI 7%.

---

## Beyond the twelve

The full space is 304 features across ten dimensions; these twelve compress the
30-feature core set, which itself retains about 91% of the full model's
discriminative power (84.8% macro-F1 against 93.2%). When an audit needs more
resolution in one area, `dimensions.md` describes what each dimension covers.

A few further differences worth knowing, from the paper's analysis:

- Dialogue serving philosophical debate: AI 59%, human 34%.
- Social structures: AI produces simpler networks with fewer characters in
  meaningful relation to each other.
- AI stories cluster in a shared, narrow region of narrative space; human stories
  occupy a rarer and far more dispersed region. The practical reading is that there
  is no single "human structure" to aim for — the diversity *is* the signal, which
  is also why prescribing a target profile would be self-defeating.

## Method caveats from the source

- Features were extracted by LLM annotation (Gemini 3 Flash), validated at Cohen's
  kappa 0.84 against human annotators. Good agreement, not perfect.
- Human stories come from Books3; AI stories were generated from prompts
  reverse-engineered from those human stories.
- The paper reports no testing on contemporaneous human fiction or on models
  released after the study.
