"""Analyze VC-VC correlation and funder reasoning pre/post session-49d identity rewrite."""
import json
from pathlib import Path
from statistics import mean, stdev
import math

PRE = Path("C:/Users/yashd/Desktop/evaluation-ecosytem-project/evaluation-ecosystem-simulation/sandbox/experiments/_llm_apr23_v1/llm/baseline_seed2/seeds/seed_2/rounds.jsonl")
POST = Path("C:/Users/yashd/Desktop/evaluation-ecosytem-project/evaluation-ecosystem-simulation/sandbox/experiments/_llm_apr23_v1/llm/baseline_seed2_postid/seeds/seed_2/rounds.jsonl")

VCS = ["TechVentures", "Horizon_Capital"]
FUNDERS = ["TechVentures", "Horizon_Capital", "StratCorp_AI", "IndustryPartners_AI", "AISI_Fund", "OpenResearch_Foundation"]

def load_rounds(path):
    rounds = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rounds.append(json.loads(line))
    return rounds

def pearson(x, y):
    n = len(x)
    if n < 2:
        return None
    mx, my = mean(x), mean(y)
    num = sum((a-mx)*(b-my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a-mx)**2 for a in x))
    dy = math.sqrt(sum((b-my)**2 for b in y))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)

def get_round_number(r):
    # try common keys
    for k in ("round", "round_number", "t", "step"):
        if k in r:
            return r[k]
    return None

def extract_allocations(r):
    """Return {funder: {provider: amount}} or {} if not present."""
    # Look for funder_data
    fd = r.get("funder_data") or r.get("funders") or {}
    # Structure could be: funder_data['allocations'][funder][provider] OR {funder: {provider: x}}
    if isinstance(fd, dict):
        if "allocations" in fd and isinstance(fd["allocations"], dict):
            return fd["allocations"]
    return {}

def extract_traces(r):
    return r.get("actor_traces") or {}

pre = load_rounds(PRE)
post = load_rounds(POST)
print(f"pre rounds: {len(pre)}, post rounds: {len(post)}")

# Inspect first round structure
r0 = pre[0]
print("\nTop-level keys in pre[0]:", list(r0.keys())[:30])
