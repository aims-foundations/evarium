"""Quick analysis of a running/completed experiment from rounds.jsonl."""
import json, statistics, sys, os

path = sys.argv[1] if len(sys.argv) > 1 else "sandbox/experiments/_apr7_full_ecosystem_balanced_llm_20260407_092700"

with open(os.path.join(path, "rounds.jsonl")) as f:
    rounds = [json.loads(l) for l in f]

providers = ["Orion Labs", "Apex AI", "Genesis Systems", "Mirage AI", "OpenCore", "Spark AI"]
dims = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

print(f"Total rounds: {len(rounds)} (R0-R{rounds[-1]['round']})")
print()

# Final state
last = rounds[-1]
r = last["round"]
scores = last["scores"]
cvs = last["capability_vectors"]
cd = last.get("consumer_data", {})
shares = cd.get("market_shares", {})
es = last.get("effective_strategies", last.get("strategies", {}))

hdr = f"{'Provider':<18} {'Score':>7} {'CapMean':>8} {'Gap':>7} {'Share':>7} {'rd/sf/pr':>10}"
print(f"=== Final State (R{r}) ===")
print(hdr)
print("-" * 62)
for p in providers:
    s = scores.get(p, 0)
    cv = cvs.get(p, {})
    c = statistics.mean(cv.values()) if cv else 0
    sh = shares.get(p, 0) * 100
    st = es.get(p, {})
    port = f"{st.get('rd',0)*100:.0f}/{st.get('safety',0)*100:.0f}/{st.get('product',0)*100:.0f}"
    print(f"{p:<18} {s:>7.3f} {c:>8.3f} {s-c:>+7.3f} {sh:>6.1f}% {port:>10}")

print()

# Trajectory summary
print("=== Trajectory Summary ===")
checkpoints = [0, 10, 20, len(rounds)-1]
for idx in checkpoints:
    if idx >= len(rounds):
        continue
    rd = rounds[idx]
    r2 = rd["round"]
    cd2 = rd.get("consumer_data", {})
    sat = cd2.get("avg_satisfaction", 0)
    switch = cd2.get("switching_rate", 0)
    s2 = rd["scores"]
    cv2 = rd["capability_vectors"]
    avg_score = statistics.mean(s2.get(p, 0) for p in providers)
    avg_cap = statistics.mean(
        statistics.mean(cv2.get(p, {}).values()) for p in providers if cv2.get(p)
    )
    shares2 = cd2.get("market_shares", {})
    top_share = max(shares2.values()) * 100 if shares2 else 0
    hhi = sum((v * 100) ** 2 for v in shares2.values()) if shares2 else 0
    print(f"  R{r2:>2}: sat={sat:.3f}  avg_score={avg_score:.3f}  avg_cap={avg_cap:.3f}  top_share={top_share:.1f}%  HHI={hhi:.0f}  switch={switch:.3f}")

print()

# Capability vectors
print("=== Final Capability Vectors ===")
print(f"{'Provider':<18}", "  ".join(f"{d[:5]:>7}" for d in dims))
print("-" * 65)
for p in providers:
    cv = cvs.get(p, {})
    print(f"{p:<18}", "  ".join(f"{cv.get(d,0):>7.3f}" for d in dims))

print()

# All incidents
print("=== All Incidents ===")
for rd in rounds:
    inc = rd.get("incidents", [])
    for i in inc:
        sev = i.get("severity", "?")
        prov = i.get("provider", "?")
        desc = i.get("description", "?")[:65]
        print(f"  R{rd['round']:>2} [{sev:>8}] {prov:<18} {desc}")

print()

# Funding totals
fd = last.get("funder_data", {})
totals = fd.get("provider_funding_totals", {})
if totals:
    print("=== Cumulative Funding ===")
    for p in sorted(totals, key=totals.get, reverse=True):
        print(f"  {p:<18} ${totals[p]:>15,.0f}")
    print(f"  {'TOTAL':<18} ${sum(totals.values()):>15,.0f}")
    print()

# Benchmarks
bms = list(last.get("per_benchmark_scores", {}).keys())
print(f"=== Active Benchmarks ({len(bms)}) ===")
for bm in bms:
    print(f"  {bm}")
