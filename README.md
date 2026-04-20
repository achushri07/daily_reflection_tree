# Daily Reflection Tree

A deterministic end-of-day reflection tool built for the DT Fellowship assignment.

**No LLM at runtime.** The tree is a structured JSON file. The agent is a Python script that walks it. Same answers → same conversation → same reflection. Every time.

---

## Repository Structure

```
/tree/
  reflection-tree.json    ← The tree (Part A: primary deliverable)
  tree-diagram.md         ← Mermaid visual diagram of all paths

/agent/
  agent.py                ← CLI agent that walks the tree (Part B)

/transcripts/
  persona-1-transcript.md ← Victor / Contributing / Altrocentric path
  persona-2-transcript.md ← Victim / Entitlement / Self-centric path

write-up.md               ← Design rationale (2 pages)
README.md                 ← This file
```

---

## Part A — Reading the Tree

Open `tree/reflection-tree.json`. Each node has:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier |
| `parentId` | Structural parent (builds tree hierarchy) |
| `type` | `start` / `question` / `decision` / `reflection` / `bridge` / `summary` / `end` |
| `text` | What the employee sees. `{NODE_ID.answer}` and `{axis.summary}` are interpolated at runtime. |
| `options` | For `question` nodes: list of fixed choices. For `decision` nodes: list of `{match, target}` routing rules. |
| `target` | Explicit next node (used by bridges and linear nodes). |
| `signal` | Tag written to state when this node is visited. Format: `axis:pole` e.g. `axis1:internal`. |

**Decision nodes** route based on the previous question's answer:
```json
{
  "type": "decision",
  "options": [
    { "match": ["Option A", "Option B"], "target": "NODE_HIGH" },
    { "match": ["Option C", "Option D"], "target": "NODE_LOW" }
  ]
}
```

**Reflection and summary nodes** interpolate stored state:
```
"You said \"{A1_OPEN.answer}\" — and by end of Axis 1, {axis1.summary}."
```

The `state_templates` section at the bottom of the JSON defines what each axis dominant pole resolves to in prose.

---

## Part B — Running the Agent

**Requirements:** Python 3.10+. No external dependencies.

```bash
# From repo root
python3 agent/agent.py

# Or with explicit path
python3 agent/agent.py tree/reflection-tree.json
```

The agent:
1. Loads the tree from the JSON file
2. Walks nodes in order, branching deterministically
3. Renders `question` nodes with numbered options
4. Auto-advances `start`, `bridge`, and `decision` nodes
5. Pauses at `reflection` and `summary` nodes for the employee to read
6. Accumulates signals in state
7. Interpolates `{placeholder}` variables in reflection and summary text
8. Prints a compact session snapshot at the end

---

## The Three Axes

| Axis | Spectrum | Psychology |
|------|----------|-----------|
| **1 — Locus** | Victim ↔ Victor | Rotter's Locus of Control (1954); Dweck's Growth Mindset (2006) |
| **2 — Orientation** | Entitlement ↔ Contribution | Campbell et al. on Psychological Entitlement (2004); Organ's OCB (1988) |
| **3 — Radius** | Self-centric ↔ Altrocentric | Maslow's Self-Transcendence (1969); Batson's Perspective-Taking (2011) |

The axes run in sequence. Agency (Axis 1) enables giving (Axis 2). Consistent giving widens the self's radius of concern (Axis 3). The progression is designed — not arbitrary.

---

## Tree Stats

| Metric | Count |
|--------|-------|
| Total nodes | 42 |
| Question nodes | 14 |
| Decision nodes | 9 |
| Reflection nodes | 11 |
| Bridge nodes | 2 |
| Summary nodes | 1 |
| Start / End nodes | 1 each |
| Options per question | 4 (all questions) |
| Axes covered | 3 (in sequence) |

---

## Design Principles

1. **No moralising.** The tree never tells an employee they were wrong. It asks them to look. The reflection for the "victim / entitlement / self-centric" path is gentler, not harsher.
2. **Fixed options, not free text.** Every question has exactly 4 predefined choices. This forces design — the options must genuinely capture the spectrum.
3. **Interpolation, not generation.** Reflection text uses `{placeholders}` for personalisation. The actual text was written by a human (with AI assistance in drafting and critique). No LLM runs at session time.
4. **The tree is the product.** Another developer can load `reflection-tree.json` and build a completely different interface — web, mobile, voice — without touching the tree structure.
