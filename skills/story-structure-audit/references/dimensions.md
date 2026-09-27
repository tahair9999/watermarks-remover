# The ten dimensions

StoryScope organizes 304 induced features across ten dimensions, adapted from the
NarraBench taxonomy. Feature counts are from the released implementation and sum to
304.

Use this file when the twelve core checkpoints are not enough resolution — when a
writer asks specifically about, say, their social structures, or when an audit needs
to say something more precise than "the plot is thin".

| Dimension | Features | Covers |
|---|---|---|
| Agents | 54 | Character complexity, emotional arcs, moral position, interiority |
| Social networks | 39 | Relationship dynamics, hierarchies, who is connected to whom |
| Style | 39 | Language devices, sentence structure, register |
| Plot | 28 | Conflict, resolution pattern, track count, causal density |
| Setting | 27 | Spatial detail, atmosphere, tonal register of place |
| Events | 26 | Causality, escalation shape, event granularity |
| Revelation | 25 | Suspense mechanism, reveal placement, recontextualization |
| Situatedness | 25 | Genre awareness, intertextuality, thematic explicitness |
| Temporal structure | 24 | Pacing, chronology, discontinuity |
| Perspective | 17 | Viewpoint consistency, narrative distance, frame breaking |

Note that Style is included in the taxonomy but the paper's headline result
deliberately *excludes* stylistic cues: narrative features alone retained over 97%
of the performance of models that also saw style. For this skill's purposes, treat
Style as out of scope — prose-level work belongs in a separate pass, and mixing the
two produces an audit where the structural findings get lost among comma notes.

## What the paper found, by dimension

**Agents.** Human protagonists are morally ambivalent far more often (59% vs 38%).
The emotion-channel gap is the widest single finding in the paper: AI conveys emotion
through physical sensation 81% of the time against 38% for humans, while humans use
explicit emotion labels 29% of the time against 8%.

**Social networks.** AI produces simpler structures — fewer characters standing in
consequential relation to one another, flatter hierarchies, less of the incidental
social texture that published fiction carries.

**Plot.** Tighter causal chains in AI: events connect more cleanly, with less
material that exists for its own sake. Protagonist-driven resolutions at 69% against
46%. Single-track preference, fewer loose ends, tidier and longer denouements.

**Setting.** Tonal register differs by generator more than it does between AI and
human in aggregate; the notable finding is per-model rather than class-wide.

**Events.** Smoother escalation. The most distinctive per-model trait in the paper is
flat event intensity, where escalation barely rises across a whole story.

**Revelation.** AI reveals tend to add information; human reveals more often force
reinterpretation of earlier scenes. Scored as depth of recontextualization.

**Situatedness.** The densest cluster of AI tells. Thematic explicitness runs about
20% higher; narrators explain the theme 77% of the time against 52%; dialogue serves
philosophical debate 59% against 34%. Intertextually, AI reaches for vague allusion
(72% vs 50%) where humans name specific texts and authors (47% vs 24%).

**Temporal structure.** Humans jump across time substantially more — flashback,
flash-forward, nonlinear arrangement. Highlighted in the abstract as one of two
headline differences alongside character agency.

**Perspective.** Humans break the fourth wall at 67% against 39%, and address the
reader directly at 28% against 7%.

## Why the aggregate picture matters more than any one dimension

The paper's most useful structural observation is about distribution rather than
means: AI-generated stories cluster in a shared, narrow region of narrative space,
while human-authored stories are rarer and far more dispersed. Five different
generators from different labs converge on similar narrative architecture.

Two consequences for how you audit:

1. A story is not improved by being pushed toward some human-typical target profile.
   There is no such profile — dispersion is the human trait. An audit that prescribes
   "add a flashback, make the ending ambiguous, name a book" produces exactly the
   kind of convergent, formula-following text the measurements describe.
2. The useful question is always *what does this story need*, with the feature space
   as a diagnostic for what the draft has stopped noticing. The scorecard finds
   places where a choice was made by default rather than on purpose. Whether the
   default was wrong is a craft judgment, and it belongs to the author.
