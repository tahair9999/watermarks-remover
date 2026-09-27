# Per-model fingerprints

StoryScope attempted six-way authorship attribution (human plus five generators) and
reached 68.4% macro-F1, against 93.2% for the binary human/AI task.

**Read that gap before using anything on this page.** Binary separation is strong;
telling one generator from another is weak. The paper explicitly notes that several
of the models overlap heavily in narrative space, and that one sits at the generic
centre of the AI distribution with no distinctive choices at all. So these are
tendencies observed across thousands of ~5,000-word stories, not identifying marks.
On a single story they support a guess at best, and an audit should not lead with
one.

Only reach for this file if someone directly asks which system likely drafted
something — and when you answer, give the 68.4% figure alongside it.

## Tendencies the paper reports

**Claude** — event intensity escalates less than in any other source; narrative voice
the most uniform across a story.

**GPT** — over-indexes on dream sequences (named in the abstract). The paper's
analysis also reports gossip and rumour used as a plot mechanism at 64%, against
44–55% for other sources.

**Gemini** — defaults to external character description over interiority (named in
the abstract). The analysis further reports the tidiest endings, the most extended
denouements, and the bleakest settings, with 88% of its settings tagged bleak.

**DeepSeek** — front-loads crucial context that other sources hold back until later.

**Kimi** — sits at the generic centre of the AI distribution, without distinctive
narrative choices. Worth stating plainly: the absence of a fingerprint is itself why
attribution accuracy is limited.

## What not to do with this

Do not run the fingerprints backwards as a checklist for making text look like it
came from a different system, or from a person. Beyond the fact that 68.4% accuracy
cannot support that kind of inference, the exercise mistakes what the features are:
descriptions of how these systems tend to build stories, not switches to flip.

If the underlying question is "will this be spotted", the honest answer is in the
robustness result — surface edits moved detection by 1.6 points, so the only thing
that changes a story's structural profile is genuinely rebuilding its structure. At
which point the writer has done the work, and the question answers itself.
