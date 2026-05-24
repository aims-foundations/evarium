#!/usr/bin/env python3
"""
Phase 2a: Build explorer data directory from a runs directory.

Walks source_dir for any folder containing rounds.jsonl, writes:
  output/explorer/data/<relative_path>/frames.json   -- full payload per run
  output/explorer/runs.json                           -- lightweight index

Incremental by default: skips runs whose frames.json is newer than rounds.jsonl.

Usage:
    python scripts/animation/generate_explorer.py
    python scripts/animation/generate_explorer.py --source hf_data_staging
    python scripts/animation/generate_explorer.py --output output/explorer
    python scripts/animation/generate_explorer.py --force
"""

import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_demo import (
    load_rounds, parse_game_log, aggregate_segments,
    build_dot_definitions, assign_dot_providers, extract_frame,
    PROVIDER_COLORS, FALLBACK_COLORS, N_DOTS,
)


def discover_runs(source_dir: Path) -> list:
    return sorted(p.parent for p in source_dir.rglob("rounds.jsonl"))


def build_payload(run_dir: Path) -> dict:
    rounds   = load_rounds(run_dir / "rounds.jsonl")
    game_log = parse_game_log(run_dir / "game_log.md")

    first_rd   = rounds[0]
    providers  = list(first_rd["consumer_data"]["market_shares"].keys())
    colors     = [PROVIDER_COLORS.get(p, FALLBACK_COLORS[i % len(FALLBACK_COLORS)])
                  for i, p in enumerate(providers)]
    prov_idx   = {p: i for i, p in enumerate(providers)}

    first_segs     = aggregate_segments(first_rd)
    dot_defs       = build_dot_definitions(first_segs, N_DOTS)
    dot_cats       = [d["cat"] for d in dot_defs]
    dot_enterprise = [d["enterprise"] for d in dot_defs]

    frames          = []
    prev_penalties  = {}
    cum_funding     = {}

    for rd in rounds:
        frame = extract_frame(rd, game_log, dot_defs, prov_idx)

        curr_penalties = {
            p: v["incident_penalty"]
            for p, v in rd["consumer_data"]["penalty_breakdown"].items()
        }
        frame["incidents"] = {
            p: round(curr, 4)
            for p, curr in curr_penalties.items()
            if curr > 0.025 and curr > prev_penalties.get(p, 0.0)
        }
        for p in frame["incidents"]:
            frame["events"].append({"kind": "incident", "text": f"Incident: {p}"})
        prev_penalties = curr_penalties

        for p, amt in rd.get("funder_data", {}).get("provider_funding_totals", {}).items():
            cum_funding[p] = cum_funding.get(p, 0.0) + amt
        frame["cum_funding"] = dict(cum_funding)

        frames.append(frame)

    return {
        "providers":       providers,
        "colors":          colors,
        "n":               len(frames),
        "dot_cats":        dot_cats,
        "dot_enterprise":  dot_enterprise,
        "frames":          frames,
    }


def run_metadata(run_dir: Path, source_dir: Path, payload: dict) -> dict:
    rel   = run_dir.relative_to(source_dir)
    parts = rel.parts

    bucket    = parts[0] if len(parts) > 0 else "unknown"
    mode      = parts[1] if len(parts) > 1 else "unknown"
    # llm layout: bucket/llm/model/condition/seed
    # heuristic layout: bucket/heuristic/condition/seed
    if mode == "llm" and len(parts) >= 5:
        model     = parts[2]
        condition = parts[3]
        seed      = parts[4]
    elif mode == "heuristic" and len(parts) >= 4:
        model     = None
        condition = parts[2]
        seed      = parts[3]
    else:
        model     = None
        condition = parts[-2] if len(parts) >= 2 else "unknown"
        seed      = parts[-1]

    # Try metadata.json for model field if not in path
    if model is None:
        meta_path = run_dir / "metadata.json"
        if meta_path.exists():
            try:
                meta  = json.loads(meta_path.read_text(encoding="utf-8"))
                model = meta.get("llm_model") or meta.get("model")
            except Exception:
                pass

    frames    = payload["frames"]
    providers = payload["providers"]
    last      = frames[-1]

    peak_gap = round(max(
        abs((f["scores"].get(p, 0.0) - f["sat"].get(p, 0.0)))
        for f in frames for p in providers
    ), 4)

    leader_traj = [
        round(max(f["shares"].values()), 3) if f["shares"] else 0.0
        for f in frames
    ]

    return {
        "path":          str(rel).replace("\\", "/"),
        "bucket":        bucket,
        "mode":          mode,
        "model":         model,
        "condition":     condition,
        "seed":          seed,
        "n_rounds":      len(frames),
        "providers":     providers,
        "final_shares":  {p: round(v, 4) for p, v in last["shares"].items()},
        "final_scores":  {p: round(v, 4) for p, v in last["scores"].items()},
        "peak_gap":      peak_gap,
        "leader_traj":   leader_traj,
    }


def write_viewer_shell(output_dir: Path) -> None:
    from generate_demo import HTML_TEMPLATE as T

    shell = T

    # Title
    shell = shell.replace(
        "<title>Eval Ecosystem — %%RUN_NAME%%</title>",
        "<title>AI Evaluation Ecosystem Explorer</title>",
    )

    # Header: back link + empty run label (filled by JS)
    shell = shell.replace(
        '<div id="hdr-run">%%RUN_NAME%%</div>',
        '<a id="hdr-back" href="index.html">← Explorer</a>'
        '<div id="hdr-run"></div>',
    )

    # Back-button + loading-overlay CSS
    shell = shell.replace(
        "</style>",
        '#hdr-back{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;'
        'color:#a08868;text-decoration:none;border:1px solid #c8b498;border-radius:4px;'
        'padding:3px 10px;margin-right:4px;white-space:nowrap}'
        '#hdr-back:hover{color:#2a1a0e;border-color:#a08868}'
        '#viewer-loading{position:fixed;inset:0;background:#f0e6d3;display:flex;'
        'align-items:center;justify-content:center;z-index:200;'
        'font-size:12px;color:#a08868;font-family:inherit;letter-spacing:.04em}'
        '</style>',
        1,
    )

    # Loading overlay in HTML (inserted before the guide overlay div)
    shell = shell.replace(
        '\n<div id="spotlight-overlay"></div>',
        '\n<div id="viewer-loading">Loading run…</div>'
        '\n<div id="spotlight-overlay"></div>',
    )

    # <script> → <script type="module"> (top-level await)
    shell = shell.replace("<script>\n", '<script type="module">\n', 1)

    # Replace SIM data block with URL-param fetch
    old_sim = (
        "const SIM       = %%DATA%%;\n"
        "const providers = SIM.providers;\n"
        "const colors    = SIM.colors;\n"
        "const frames    = SIM.frames;\n"
        "const N         = SIM.n;\n"
        "const DOT_CATS       = SIM.dot_cats;\n"
        "const DOT_ENTERPRISE = SIM.dot_enterprise;\n"
        "const N_DOTS         = DOT_CATS.length;"
    )
    new_sim = (
        "const _p   = new URLSearchParams(location.search);\n"
        "const _run = _p.get('run') || '';\n"
        "if (!_run) {\n"
        "  document.getElementById('viewer-loading').innerHTML =\n"
        "    'No run specified. <a href=\"index.html\">← Back to explorer</a>';\n"
        "  throw new Error('no run param');\n"
        "}\n"
        "document.getElementById('hdr-run').textContent =\n"
        "  _run.split('/').slice(-2).join(' / ');\n"
        "const _resp = await fetch('data/' + _run + '/frames.json');\n"
        "if (!_resp.ok) {\n"
        "  document.getElementById('viewer-loading').innerHTML =\n"
        "    'Could not load <b>' + _run + '</b> (HTTP ' + _resp.status + ')."
        " <a href=\"index.html\">← Back</a>';\n"
        "  throw new Error('fetch ' + _resp.status);\n"
        "}\n"
        "const SIM = await _resp.json();\n"
        "document.getElementById('viewer-loading').style.display = 'none';\n"
        "const providers = SIM.providers;\n"
        "const colors    = SIM.colors;\n"
        "const frames    = SIM.frames;\n"
        "const N         = SIM.n;\n"
        "const DOT_CATS       = SIM.dot_cats;\n"
        "const DOT_ENTERPRISE = SIM.dot_enterprise;\n"
        "const N_DOTS         = DOT_CATS.length;"
    )
    shell = shell.replace(old_sim, new_sim)

    # window.addEventListener("load", ...) → direct execution (module is deferred)
    shell = shell.replace(
        'window.addEventListener("load", () => {',
        "/* module is deferred — DOM ready, run directly */ {",
    )
    # Remove the matching closing }); at the very end of the script
    shell = shell.replace(
        "});\n</script>\n</body>\n</html>",
        "}\n</script>\n</body>\n</html>",
    )

    out = output_dir / "viewer.html"
    out.write_text(shell, encoding="utf-8")
    print(f"Viewer:  {out}")


def generate_explorer(source_dir: Path, output_dir: Path, force: bool = False) -> None:
    runs = discover_runs(source_dir)
    if not runs:
        print(f"No runs found under {source_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(runs)} runs under {source_dir}")

    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    index   = []
    built   = 0
    skipped = 0
    errors  = 0

    for i, run_dir in enumerate(runs, 1):
        rel      = run_dir.relative_to(source_dir)
        out_path = data_dir / rel / "frames.json"

        if not force and out_path.exists():
            src_mtime = (run_dir / "rounds.jsonl").stat().st_mtime
            if out_path.stat().st_mtime >= src_mtime:
                try:
                    payload = json.loads(out_path.read_text(encoding="utf-8"))
                    index.append(run_metadata(run_dir, source_dir, payload))
                    skipped += 1
                    continue
                except Exception:
                    pass

        print(f"  [{i:3d}/{len(runs)}] {rel}")
        try:
            payload = build_payload(run_dir)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                json.dumps(payload, separators=(",", ":")),
                encoding="utf-8",
            )
            index.append(run_metadata(run_dir, source_dir, payload))
            built += 1
        except Exception as e:
            print(f"             SKIP ({e})")
            errors += 1

    runs_path = output_dir / "runs.json"
    runs_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

    write_viewer_shell(output_dir)

    print(f"\nDone.  built={built}  up-to-date={skipped}  errors={errors}")
    print(f"Data:  {data_dir}")
    print(f"Index: {runs_path}  ({len(index)} entries)")


def main():
    ap = argparse.ArgumentParser(
        description="Build explorer data directory from a runs directory"
    )
    ap.add_argument("--source", "-s", default="hf_data_staging",
                    help="Source runs directory (default: hf_data_staging)")
    ap.add_argument("--output", "-o", default="../web-explorer",
                    help="Output directory (default: ../web-explorer)")
    ap.add_argument("--force", "-f", action="store_true",
                    help="Re-generate all frames.json even if up-to-date")
    args = ap.parse_args()
    generate_explorer(Path(args.source), Path(args.output), force=args.force)


if __name__ == "__main__":
    main()
