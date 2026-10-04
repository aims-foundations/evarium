"""Within-family benchmark correlations from Epoch AI Benchmarking Hub data.

Grounds the paper's cos(theta) = 0.85 anchor: Pearson correlation, across models
scored on both, between a public benchmark and its harder or held-out sibling.

Data: external-validation/data/benchmarks/ (Epoch AI, CC-BY-4.0). A model scored more than
once on a benchmark contributes its best score.

Usage: python external-validation/scripts/epoch_within_family_correlations.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / 'data' / 'benchmarks'

PAIRS = [
    ('SWE-Bench-Verified vs SWE-Bench-Bash', 'swe_bench_verified.csv', 'mean_score', 'swe_bench_bash.csv', '% Resolved'),
    ('FrontierMath T1-3 vs T4', 'frontiermath.csv', 'mean_score', 'frontiermath_tier_4.csv', 'mean_score'),
    ('ARC-AGI-1 vs ARC-AGI-2', 'arc_agi_external.csv', 'Score', 'arc_agi_2_external.csv', 'Score'),
]


def best_scores(name, col):
    d = pd.read_csv(DATA / name)[['Model version', col]].dropna()
    return d.groupby('Model version')[col].max()


def main():
    rs = []
    for label, fa, ca, fb, cb in PAIRS:
        both = pd.concat([best_scores(fa, ca), best_scores(fb, cb)], axis=1, join='inner').dropna()
        r = np.corrcoef(both.iloc[:, 0], both.iloc[:, 1])[0, 1]
        rs.append(r)
        print(f'{label}: n={len(both)} models, Pearson r={r:.3f}')
    print(f'range {min(rs):.3f}-{max(rs):.3f}, median {np.median(rs):.3f}')


if __name__ == '__main__':
    main()
