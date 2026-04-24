# Sonnet vs Opus Appendix (Appendix K) — Analysis Playbook

Reproducible steps for the model-robustness appendix in `overleaf/appendix/K_sonnet_opus.tex`. Use this playbook to re-run the analysis whenever the Tier 1 `_core_privacy` batch expands — e.g., after batch 3a / 3b completes and new Opus-Sonnet pairs are available.

## What this produces

Four artifacts populate the appendix:
1. `output/paper/sonnet_vs_opus_ladder.{png,pdf}` — two-panel privacy-ladder forest (K.2, Fig K.1)
2. `output/paper/sonnet_vs_opus_forest.{png,pdf}` — paired per-benchmark dots at seed 42 (K.2, Fig K.2)
3. `output/paper/sonnet_vs_opus_endpoints.csv` — share-weighted endpoint metrics per (condition, seed, model) (K.2, Table K.1)
4. `output/paper/sonnet_vs_opus_frames.{png,pdf}` — stacked reasoning-frame distribution per (provider, model) (K.3, Fig K.3)

Plus supporting:
- `sonnet_vs_opus_frames_detail.csv` — one row per tagged planning entry; used to compose K.3 excerpts
- `sonnet_vs_opus_frames_audit.md` — hand-audit sample (3 tagged excerpts per frame per model)

## Inputs / prerequisites

- Runs under `sandbox/experiments/_core_privacy/llm/<condition>_s<seed>_<model>/` with full 40-round `rounds.jsonl`. The discovery filter skips partial runs; no manual cleanup needed.
- Naming convention must be `<condition>_s<seed>_<model>` with `model ∈ {sonnet, opus}`. This is what `scripts/run_experiment.py` emits by default; keep it.
- Each run directory needs the standard payload: `rounds.jsonl`, `summary.json`, `metadata.json`, `providers/<name>/memory.json`. These are all auto-written.

No Sonnet or Opus runs outside `_core_privacy/` are folded in — the appendix is deliberately scoped to Tier 1.

## Step 1: Endpoint table + ladder + paired-s42 forest

```bash
cd evaluation-ecosystem-simulation
python -m scripts.plots.paper.sonnet_vs_opus
```

Reads every `_core_privacy/llm/*_s*_{sonnet,opus}/seeds/seed_*/rounds.jsonl` with `n_rounds ≥ 40`. Partial runs are skipped with a log line. Outputs to `output/paper/`.

Side effects:
- Prints the endpoint table to stdout (handy for eyeballing)
- Ladder panel titles include per-condition seed counts so you can tell at a glance how unbalanced the panels are
- Paired-s42 forest only draws conditions where BOTH sonnet and opus have full seed-42 runs. Missing pairs are silently dropped.

## Step 2: Reasoning-frame tagging

```bash
python -m scripts.tag_reasoning_frames
```

Scans `providers/<name>/memory.json` for every matched (condition, seed) pair, pulls `type=='planning'` entries, runs keyword+regex tagging, writes:
- `sonnet_vs_opus_frames_detail.csv` — per-entry long form (1872 rows as of 4 paired runs)
- `sonnet_vs_opus_frames.csv` — aggregated (model, provider, frame, count)
- `sonnet_vs_opus_frames_audit.md` — sample excerpts

**Hand-audit (always do this when frame ratios shift):** open the audit markdown and skim ~3 excerpts per frame per model. The two frames that matter for the story are `privacy` and `incident` — confirm that matched excerpts are *substantive* reasoning about the mechanism, not incidental keyword hits.

The frame patterns are in `scripts/tag_reasoning_frames.py:FRAME_PATTERNS`. Modify them if a new round of prompt changes introduces new vocabulary (e.g., if prompt audit adds new phrasing for the holdout mechanism, update the `privacy` regex).

## Step 3: Regenerate ladder + frames figure

The first run of Step 1 will emit the frames figure as a `SKIP` because the frames CSV doesn't exist yet. After Step 2 writes the CSV, re-run Step 1:

```bash
python -m scripts.plots.paper.sonnet_vs_opus
```

Now all four figures + CSV are current.

## Step 4: Compose K.3 excerpts

For a fresh appendix pass, pick ~4 excerpts to quote: matched-pair privacy-frame (one Sonnet, one Opus, ideally same condition & a round with similar observation) + an incident-frame pair.

Helper snippet — pulls the longest-reasoning entries per frame:

```python
import pandas as pd
d = pd.read_csv('output/paper/sonnet_vs_opus_frames_detail.csv')
for model in ('sonnet', 'opus'):
    sub = d[(d.model == model) & d.frames.str.contains('privacy', regex=False)]
    print(sub.sort_values('reasoning_len', ascending=False).head(4)[
        ['provider','condition','seed','round','reasoning_excerpt']])
```

Then fetch the full reasoning by reading `providers/<prov>/memory.json`, scanning for `type=='planning'` and matching `round`.

The current K.3 quotes matched excerpts from `Genesis Systems / private_dominant@s42 r31 (Sonnet)` and `Mirage AI / private_dominant@s42 r25 (Opus)` — both open with "universal +0.000… K=3 lag". If these runs are replaced, find a new matched pair with the same pattern.

## Step 5: Copy PDFs into Overleaf

```bash
cp output/paper/sonnet_vs_opus_ladder.pdf ../overleaf/figures/
cp output/paper/sonnet_vs_opus_forest.pdf ../overleaf/figures/
cp output/paper/sonnet_vs_opus_frames.pdf ../overleaf/figures/
```

User compiles on Overleaf — do not run pdflatex locally.

## Step 6: Update numbers in K.2 / K.3 / K.4

Three spots need manual number updates when the data changes:

1. **Table K.1** (`overleaf/appendix/K_sonnet_opus.tex`) — the paired-pair endpoint rows. Copy from `sonnet_vs_opus_endpoints.csv`, keeping only (condition, seed) pairs with both models present.
2. **K.3 frame counts** — the Sonnet/Opus incident and privacy percentages. Recompute from the aggregated frames CSV: `share = count / total_planning_entries_per_model`. The total is roughly `n_paired_runs × 6 providers × 40 rounds` but exact planning-entry count varies; use `df_detail[df_detail.model==m].shape[0]` for the denominator.
3. **K.4 runtime** — recompute wall-clock per-run from `metadata.json` → `summary.json` file-mtime deltas. Snippet:
   ```python
   import os, glob, re, statistics
   pairs = []
   for d in glob.glob('sandbox/experiments/_core_privacy/llm/*'):
       m = re.match(r'.+?_s(\d+)_(sonnet|opus)$', os.path.basename(d))
       if not m: continue
       seed = m.group(1)
       meta = f'{d}/seeds/seed_{seed}/metadata.json'
       summ = f'{d}/seeds/seed_{seed}/summary.json'
       if os.path.exists(meta) and os.path.exists(summ):
           pairs.append((os.path.basename(d),
                         (os.path.getmtime(summ)-os.path.getmtime(meta))/60))
   ```

Wall-clock is the firmest quantity; token counts are not currently logged, so cost is an estimate from published per-token pricing (5× per-token for Opus).

## Decision gates / what to flag

- **Ladder ordering**: if privacy-condition ordering flips between models on any high-gap benchmark, that's a real breakage of the main claim — write it up, don't paper over.
- **Frame divergence > 2×**: if any frame's Sonnet/Opus ratio exceeds 2× (current: incident ~1.8×), hand-audit 20+ excerpts before trusting it. Keyword tagging has blind spots.
- **Privacy-frame share differs by > 10pp between models**: means the two planners are reasoning about the mechanism at meaningfully different rates — not necessarily a failure but deserves its own paragraph rather than being buried.

## Known limitations of the playbook

- Tagging is keyword+regex, not LLM-judged. It is deterministic and reproducible but can miss paraphrased mentions. If a future prompt audit changes the vocabulary providers use, update `FRAME_PATTERNS` in `tag_reasoning_frames.py`.
- Wall-clock uses file-mtime deltas as a proxy, which is accurate to within a few seconds but depends on summary.json being written at run completion (which `run_experiment.py` guarantees).
- Token and per-call cost are not logged — if you need exact cost, you'll have to add token telemetry to `src/llm.py` and regenerate runs.
