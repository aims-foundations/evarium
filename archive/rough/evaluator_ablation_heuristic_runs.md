- Evaluator ablation heuristic baseline

8 core conditions x 30 seeds (balanced policy only), 8 shells in parallel (one per condition).
Output: sandbox/experiments/heuristic/<condition>/seeds/seed_<N>/

Seeds (fixed, reproducible): 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859

Generated with:
  import random; random.seed(42); sorted(random.sample(range(100, 1000), 30))

Conditions:
  full_ecosystem     — baseline (expanding benchmarks, all public)
  fixed_public       — 4 initial benchmarks only, no new introductions, all public
  fixed_partial      — fixed set, Safety Eval partial holdout (h=0.30)
  fixed_private      — fixed set, Safety+Coding Eval private holdout (h=0.50)
  expanding_partial  — expanding set + partial holdout (Safety h=0.30, 4 seq benchmarks h=0.30-1.00)
  expanding_private  — expanding set + private holdout (Safety+Coding h=0.50, all 6 seq h=0.50-1.00)
  dynamic_evaluator  — time-triggered heuristic, introduces from pool every 4 rounds
  eval_as_company    — evaluator has commercial interests, best-of-N trials

Shell 1 — full_ecosystem:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition full_ecosystem --mode heuristic --policy balanced --seed $seed; done

Shell 2 — fixed_public:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition fixed_public --mode heuristic --policy balanced --seed $seed; done

Shell 3 — fixed_partial:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition fixed_partial --mode heuristic --policy balanced --seed $seed; done

Shell 4 — fixed_private:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition fixed_private --mode heuristic --policy balanced --seed $seed; done

Shell 5 — expanding_partial:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition expanding_partial --mode heuristic --policy balanced --seed $seed; done

Shell 6 — expanding_private:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition expanding_private --mode heuristic --policy balanced --seed $seed; done

Shell 7 — dynamic_evaluator:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition dynamic_evaluator --mode heuristic --policy balanced --seed $seed; done

Shell 8 — eval_as_company:
for seed in 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859; do python scripts/run_experiment.py --condition eval_as_company --mode heuristic --policy balanced --seed $seed; done

After all runs complete:
Check for failures: any seed directory missing rounds.jsonl is a failed run.
Then run aggregation: python scripts/aggregate_heuristic.py (add new conditions to condition list first).
