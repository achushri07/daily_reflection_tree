# Write-up: Design Rationale — Daily Reflection Tree

## Why These Questions

Every question in this tree is trying to do one thing: make the implicit explicit, without the employee feeling interrogated. The hard part of designing questions for end-of-day reflection is that tired people answer quickly and honestly — they don't have the energy to perform. That's an asset. The questions had to be concrete enough to catch real behaviour, and non-obvious enough to not telegraph the "right" answer.

**Axis 1 — Locus:** The car-seat metaphor was a deliberate choice over a direct question like "did you feel in control today?" Direct questions about control are too psychologically loaded — people answer the question they want to answer rather than the one being asked. The car metaphor is defamiliarising; it pulls the employee out of defensive mode and into image-mode. The follow-up questions (what made it work / what was your instinct) then excavate the mechanism behind the metaphor.

The lucky-answer branch (A1_Q_CHOICE_LUCKY) was added because many high-agency people attribute their successes to luck out of modesty. Crediting luck is not the same as having an external locus — and conflating them would produce a bad tree. The follow-up question ("did you do anything to make luck more likely?") separates genuine external attribution from false modesty.

**Axis 2 — Orientation:** The entitlement axis is the hardest to surface without shame. The approach here was to ask the employee to locate the feeling in time ("when did you first notice it?") rather than asking whether they have it. Locating it in time makes it observable rather than accusatory. The follow-up question ("was there a moment where someone needed you and you weren't fully there?") is the pivot — it doesn't tell the employee they were wrong; it asks them to look. The employee's answer to that question is what the tree routes on.

**Axis 3 — Radius:** The frame question ("who is in the picture?") uses visual metaphor intentionally. "Who do you think about" is answerable in the abstract; "who is in the frame of a specific moment" forces the employee to recall a concrete scene, which makes the self/other ratio visible.

---

## Branching Design — Trade-offs

The tree has two architecturally significant choices worth explaining.

**1. Axis 1 has the most branching depth.** This is intentional: locus of control is the foundation of the whole session. Someone who leaves Axis 1 without being genuinely met — either validated in their agency or genuinely accompanied in their external locus — won't be emotionally available for Axes 2 and 3. The extra depth (the lucky-branch, the "one small thing" question) exists to make sure no one falls through the cracks feeling judged.

**2. The Axis 2 entitlement path goes deeper than the contribution path.** Contributing employees need acknowledgement, not re-education. The tree does that in one reflection and moves on. Employees on the entitlement path need more scaffolding — a chance to locate the feeling, then a harder question, then a non-shaming reflection. This asymmetry is intentional: the tree spends time where it's needed.

**Trade-off I would revisit:** The Axis 3 "team" branch (A3_Q_TEAM) currently terminates after two questions. With more time, I'd add a follow-up that bridges from team-awareness to user/external-awareness — to give team-oriented employees a path toward the transcendent level without forcing it.

---

## Psychological Sources

**Locus of Control — Julian Rotter (1954):** The internal/external spectrum informed every Axis 1 branch target. Crucially, Rotter's original scale is a continuum, not a binary — the tree reflects this by having intermediate states (co-pilot, latent agency) rather than forcing a victim/victor dichotomy.

**Growth Mindset — Carol Dweck (2006):** The "lucky" follow-up question draws directly from Dweck's observation that fixed-mindset individuals tend to attribute success to natural talent or luck rather than process. The question does not correct this; it asks the employee to look for process beneath the luck.

**Organizational Citizenship Behavior — Organ (1988):** OCB's defining characteristic — discretionary effort beyond formal role requirements — informed the Axis 2 contribution questions. The options (helping without being asked, unglamorous tasks, patient moments) are all OCB behaviours that have no job-description home.

**Psychological Entitlement — Campbell et al. (2004):** Entitlement is invisible to its holder. The design implication was to avoid yes/no entitlement questions and instead ask employees to locate and describe their experience. The tree never uses the word "entitlement."

**Self-Transcendence — Maslow (1969):** The late-career Maslow (Theory Z, the Journal of Transpersonal Psychology paper) argued that the highest human motivation is not self-actualisation but transcendence — the orientation toward something larger than oneself. The Axis 3 progression (self → team → outside circle) maps this directly, with the reflection for the transcend path naming Maslow explicitly, because employees at that level benefit from having the concept named.

---

## What I'd Improve With More Time

**Richer summary personalisation.** Currently the summary node interpolates three axis-level summaries. With more time, I'd add cross-axis synthesis — for example, flagging when someone shows internal locus (Axis 1) but entitlement (Axis 2), which is a specific and interesting pattern (capable people who feel underrecognised). The current state tallies support this; the summary templates don't yet use it.

**Temporal comparison.** The tree resets each session. A real product would track axis signals over time and surface patterns: "This is the third week running where your Axis 3 frame has been mostly self." That's when the tool becomes genuinely useful.

**More question variety per axis.** Currently the entry point into each axis is fixed. Rotating the opening question (drawing from a pool) would reduce the fatigue effect for long-term users.

**Mobile-first interface.** The CLI agent is functional and readable, but a web-based version with thoughtful typography — slow text reveal, no button chrome, dark mode by default — would close the gap between the tree's tone and its container. The reflection text is designed to be read carefully; the interface should enforce that pace.
