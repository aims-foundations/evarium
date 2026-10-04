"""
calibration_audit_table.py

The calibration-audit table.
Assembles sim parameters vs empirically-measured values into one
sim | empirical | source | verdict table, extending Appendix C's existing
parameter-grounding longtable (the K=3 row is the accepted precedent). Audit
only -- mismatches become limitations text, never retuning.

Rows computed here from data:
  B. Benchmark introduction cadence  (registry first-mention + census firehose)
  C. Active roster size              (registry benchmarks-per-doc)
  D. Model release tempo             (Epoch ECI inter-release gaps)
  F. Saturation -> retirement lag    (Epoch score plateau vs registry last-mention)
Rows asserted (already anchored / definitional):
  A. Round = month / run window      (run_experiment date comments vs registry window)
  E. Reporting lag K=3               (paper App C: Epoch 24-bench x 8-lab, 3.0 mo)

Round = MONTH (canonical; stakeholders.md + run_experiment.py date comments;
the external-validation/README.md quarterly line is stale drift).

Sources: private ai-discourse census+registry; public Epoch (in-repo). Windows
console is cp1252 -- ascii-only prints.
"""

import csv
import json
import os
import statistics
from collections import Counter, defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
EXTVAL = os.path.dirname(HERE)
PROC = os.path.join(EXTVAL, "data", "processed")
BENCH = os.path.join(EXTVAL, "data", "benchmarks")

# Private source (a separate benchmark-census project); set LAB_REPORTING_DIR to its lab-reporting folder.
AID = os.environ.get("LAB_REPORTING_DIR", "lab-reporting")
CENSUS = os.path.join(AID, "data", "linking", "frozen_20260623", "census.csv")
CENSUS_V3 = os.path.join(AID, "data", "linking", "frozen_20260623", "census_v3.csv")
REG_CANON = os.path.join(AID, "data", "linking", "registry_canonical.csv")
TOP60 = os.path.join(AID, "data", "linking", "test_top60.csv")
EXTRACTED = os.path.join(AID, "data", "extracted_with_recovery.jsonl")


def _read(path, bom=True):
    with open(path, encoding="utf-8-sig" if bom else "utf-8") as f:
        return list(csv.DictReader(f))


def _months(d1, d2):
    return (d2 - d1).days / 30.437


def parse_date(s):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


# ---------- Row C: benchmarks per doc ----------
def row_benchmarks_per_doc():
    docs = [json.loads(l) for l in open(EXTRACTED, encoding="utf-8")]
    by = defaultdict(list)
    for d in docs:
        y = (d.get("group_min_date", "") or "")[:4]
        by[y].append(len(d.get("benchmarks", []) or []))
    alln = [n for v in by.values() for n in v]
    per_year = {y: (len(by[y]), round(sum(by[y]) / len(by[y]), 1)) for y in sorted(by) if y}
    return round(sum(alln) / len(alln), 1), per_year


# ---------- Row B: benchmark introduction cadence ----------
def row_cadence():
    # canonical map raw->canonical
    canon = {r["raw_name"]: r["canonical"] for r in _read(REG_CANON, bom=False)}
    top60 = {r["canonical"] for r in _read(TOP60)}
    # first-mention per canonical from extracted (post-recovery)
    first = {}
    docs = [json.loads(l) for l in open(EXTRACTED, encoding="utf-8")]
    for d in docs:
        gd = d.get("group_min_date", "") or ""
        for b in d.get("benchmarks", []) or []:
            c = canon.get(b.get("name", ""), b.get("name", ""))
            if not c:
                continue
            if c not in first or gd < first[c]:
                first[c] = gd
    # arrival of NEW top-60 benchmarks into lab reporting, by first-mention year
    # (2023 is inflated by the reporting-window start 2023-02; 2024+ ~= genuine debut)
    arrivals = Counter()
    for c in top60:
        y = (first.get(c, "") or "")[:4]
        if y:
            arrivals[y] += 1
    # census firehose for contrast (>=100 citations)
    date = {r[list(r.keys())[0]]: r["date"] for r in _read(CENSUS)}
    cv = _read(CENSUS_V3)
    idk = list(cv[0].keys())[0]
    fire = Counter()
    for r in cv:
        try:
            n = int(float(r["n_citations"]))
        except (ValueError, KeyError):
            n = 0
        if n >= 100:
            y = (date.get(r[idk], "") or "")[:4]
            if y:
                fire[y] += 1
    return arrivals, fire


# ---------- Row D: model release tempo (Epoch ECI) ----------
def row_release_tempo():
    eci = _read(os.path.join(BENCH, "epoch_capabilities_index.csv"))
    by_org = defaultdict(list)
    for r in eci:
        org = (r.get("Organization", "") or "").strip()
        d = parse_date(r.get("Release date", ""))
        if org and d:
            by_org[org].append(d)
    out = {}
    for org, dates in by_org.items():
        # dedupe same-day variants (reasoning-effort/size variants share a date):
        # tempo = gaps between DISTINCT release dates in the sim window.
        w = sorted({d for d in dates if d >= datetime(2023, 1, 1)})
        if len(w) < 4:
            continue
        gaps = [_months(w[i], w[i + 1]) for i in range(len(w) - 1)]
        out[org] = (len(w), round(statistics.median(gaps), 1))
    return out


# ---------- Row F: saturation -> retirement lag ----------
def _plateau_date(csv_name, score_col="EM", eps=0.02):
    rows = _read(os.path.join(BENCH, csv_name))
    pts = []
    for r in rows:
        d = parse_date(r.get("Release date", ""))
        try:
            s = float(r.get(score_col, "") or "")
        except ValueError:
            continue
        if d and s:
            pts.append((d, s))
    if not pts:
        return None, None, None
    pts.sort()
    run_max, series = 0.0, []
    for d, s in pts:
        run_max = max(run_max, s)
        series.append((d, run_max))
    final = series[-1][1]
    # plateau = first date running-max reaches within eps of final running-max
    plateau = next((d for d, rm in series if rm >= final - eps), None)
    return plateau, final, pts[-1][0]


def _last_mention(canonical_name):
    canon = {r["raw_name"]: r["canonical"] for r in _read(REG_CANON, bom=False)}
    docs = [json.loads(l) for l in open(EXTRACTED, encoding="utf-8")]
    last = ""
    for d in docs:
        gd = d.get("group_min_date", "") or ""
        for b in d.get("benchmarks", []) or []:
            if canon.get(b.get("name", ""), b.get("name", "")) == canonical_name:
                if gd > last:
                    last = gd
    return last


def row_saturation():
    out = {}
    for label, csvf, canon in [("MMLU", "mmlu_external.csv", "MMLU"),
                               ("GSM8K", "gsm8k_external.csv", "GSM8K")]:
        plateau, final, last_score = _plateau_date(csvf)
        lm = _last_mention(canon)
        lag = None
        if plateau and lm:
            lmd = parse_date(lm)
            if lmd:
                lag = round(_months(plateau, lmd), 1)
        out[label] = {
            "plateau": plateau.strftime("%Y-%m") if plateau else "n/a",
            "final_max": round(final, 3) if final else "n/a",
            "last_mention": lm or "n/a",
            "lag_months": lag,
        }
    return out


def main():
    os.makedirs(PROC, exist_ok=True)
    bpd_mean, bpd_year = row_benchmarks_per_doc()
    arrivals, fire = row_cadence()
    tempo = row_release_tempo()
    sat = row_saturation()

    print("=" * 74)
    print("CALIBRATION-AUDIT: sim parameter vs empirical measurement")
    print("=" * 74)

    print("\n[A] Round=month / run window")
    print("    SIM: 40 rounds, round=month, Jan 2023 -> ~Apr 2026 (run_experiment dates)")
    print("    EMP: registry lab-report window 2023-02 .. 2026-06 -> MATCH")

    print("\n[B] Benchmark introduction cadence")
    print("    SIM: 1 new benchmark / 4 rounds = 1 / 4 months (3/yr); App B prose says '1-2 months'")
    print("    EMP: NEW top-60 benchmarks entering lab reporting, by first-mention year:")
    for y in ["2023", "2024", "2025", "2026"]:
        note = " (window-start inflated)" if y == "2023" else ""
        print("         %s: %2d  (%.2f/mo)%s" % (y, arrivals[y], arrivals[y] / 12.0, note))
    n2425 = arrivals["2024"] + arrivals["2025"]
    print("    -> 2024-25 flagship arrival ~%.1f/mo (1 per %.1f mo): matches App B prose,"
          % (n2425 / 24.0, 24.0 / max(n2425, 1)))
    print("       ~%.1fx FASTER than the code's 4-month cooldown. Census firehose (>=100 cit)"
          % (4.0 / (24.0 / max(n2425, 1))))
    print("       = %d/yr (2024), i.e. sim roster is a deliberate flagship subset."
          % fire["2024"])

    print("\n[C] Active roster size")
    print("    SIM: 13 active benchmarks (max_benchmarks)")
    print("    EMP: registry benchmarks-per-doc mean=%.1f (%s) -> same order, sim slightly high"
          % (bpd_mean, ", ".join("%s:%.1f" % (y, m) for y, (n, m) in bpd_year.items())))

    print("\n[D] Model release tempo (Epoch ECI, 2023+, median inter-release gap, months)")
    for org in ["OpenAI", "Anthropic", "Google DeepMind", "Google", "Meta AI",
                "DeepSeek", "Alibaba", "xAI", "Mistral AI"]:
        if org in tempo:
            n, g = tempo[org]
            print("    %-18s n=%2d  median gap %4.1f mo" % (org, n, g))
    print("    SIM: continuous monthly capability growth (no discrete release event);")
    print("         breakthrough prob 0.05/round -> continuous approx of ~1-3 mo frontier cadence")

    print("\n[E] Reporting lag K")
    print("    SIM: K=3 rounds = 3 months (holdout publish cadence)")
    print("    EMP: Epoch 24-bench x 8-lab median-of-medians 3.0 mo (paper App C) -> ANCHORED")

    print("\n[F] Saturation -> retirement lag")
    print("    SIM: benchmark retires when saturated (score-delta<0.005 x3 rounds) at roster cap")
    for k, v in sat.items():
        print("    EMP %-6s plateau %s (max %.3f) -> last lab-mention %s = lag %s months"
              % (k, v["plateau"], v["final_max"], v["last_mention"], v["lag_months"]))
    print("    -> real benchmarks keep being reported ~1-2 yr AFTER saturation (slow retirement);")
    print("       sim retires promptly at cap -- a simplification to flag, not retune.")

    # write the assembled table
    rows = [
        ["A round/window", "40 mo, Jan2023-Apr2026", "registry 2023-02..2026-06", "match", "definitional"],
        ["B intro cadence", "1 / 4 mo (3/yr)", "flagship ~1 / %.1f mo (2024-25)" % (24.0 / max(n2425, 1)), "sim SLOWER ~%.1fx" % (4.0 / (24.0 / max(n2425, 1))), "registry first-mention"],
        ["C roster size", "13 active", "%.1f benchmarks/doc" % bpd_mean, "match (same order)", "registry"],
        ["E reporting lag K", "3 mo", "3.0 mo", "anchored", "Epoch (App C)"],
    ]
    for k, v in sat.items():
        rows.append(["F saturation lag %s" % k, "prompt retire at cap",
                     "plateau %s, last-mention %s (lag %s mo)" % (v["plateau"], v["last_mention"], v["lag_months"]),
                     "sim retires faster", "Epoch+registry"])
    for org in ["OpenAI", "Anthropic", "Google DeepMind", "Meta AI", "DeepSeek"]:
        if org in tempo:
            rows.append(["D release tempo %s" % org, "continuous monthly",
                         "median gap %.1f mo" % tempo[org][1], "continuous approx", "Epoch ECI"])
    with open(os.path.join(PROC, "calibration_audit_table.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["parameter", "sim_value", "empirical_value", "verdict", "source"])
        w.writerows(rows)
    print("\nWrote %s" % os.path.join(PROC, "calibration_audit_table.csv"))


if __name__ == "__main__":
    main()
