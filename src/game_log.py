"""
Game Log Generator for Evaluation Ecosystem Simulation

Generates natural language summaries of simulation rounds in markdown format.
Captures strategy decisions, score changes, rank changes, consumer switches,
regulations, and LLM reasoning when available.

Design:
- Template-based core for fast, deterministic output
- LLM reasoning inclusion from provider.private_state.recent_insights when llm_mode=True
"""
from typing import Optional


def _mean_capability(record: dict, name: str) -> float:
    """Return mean of a provider's 6-dim capability vector, or 0 if missing."""
    vec = record.get("capability_vectors", {}).get(name)
    if not vec:
        return 0.0
    return sum(vec.values()) / len(vec)


class GameLogGenerator:
    """
    Generates a readable markdown log of the simulation.

    Usage:
        generator = GameLogGenerator(experiment_name="baseline", experiment_id="exp_001")
        generator.record_round(round_data, providers, consumers, regulators)
        ...
        markdown_content = generator.generate_markdown()
    """

    def __init__(
        self,
        experiment_name: str = "Simulation",
        experiment_id: str = "",
        llm_mode: bool = False,
        benchmarks: list = None,
    ):
        self.experiment_name = experiment_name
        self.experiment_id = experiment_id
        self.llm_mode = llm_mode
        self.benchmarks = benchmarks or []

        self.rounds_data: list[dict] = []
        self.events: list[dict] = []

    def record_round(self, round_data: dict, providers: list):
        round_num = round_data.get("round", len(self.rounds_data))

        # Extract provider states including LLM reasoning
        provider_states = {}
        for provider in providers:
            provider_states[provider.name] = {
                "true_capability": _mean_capability(round_data, provider.name),
                "score": round_data["scores"].get(provider.name),
                "strategy": round_data["strategies"].get(provider.name, {}),
                "reasoning": self._extract_latest_reasoning(provider, round_num),
            }

        # Store round data
        record = {
            "round": round_num,
            "scores": round_data.get("scores", {}),
            "capability_vectors": round_data.get("capability_vectors", {}),
            "strategies": round_data.get("strategies", {}),
            "leaderboard": sorted(round_data.get("scores", {}).items(), key=lambda x: x[1], reverse=True),
            "consumer_data": round_data.get("consumer_data", {}),
            "regulator_data": round_data.get("regulator_data", {}),
            "provider_states": provider_states,
            "actor_traces": round_data.get("actor_traces", {}),
            "new_benchmark": round_data.get("new_benchmark"),
            "per_benchmark_scores": round_data.get("per_benchmark_scores", {}),
            "benchmark_names": list(round_data.get("benchmark_params", {}).keys()),
            "media_data": round_data.get("media_data", {}),
        }

        self.rounds_data.append(record)

        # Detect events
        self._detect_events(round_num, record)

    def _extract_latest_reasoning(self, provider, round_num: int) -> Optional[str]:
        """
        Extract LLM reasoning from provider state for the given round.

        Args:
            provider: ModelProvider instance
            round_num: Round number to extract reasoning for

        Returns:
            Reasoning string if available, None otherwise
        """
        if not self.llm_mode:
            return None

        # Check recent_insights in private_state
        if hasattr(provider, 'private_state') and provider.private_state.recent_insights:
            for insight in reversed(provider.private_state.recent_insights):
                if isinstance(insight, dict) and insight.get("round") == round_num:
                    return insight.get("reasoning")

        # Check memory for planning entries
        if hasattr(provider, 'memory'):
            for entry in reversed(provider.memory):
                if (entry.get("type") == "planning" and
                    entry.get("round") == round_num and
                    entry.get("reasoning")):
                    return entry.get("reasoning")

        return None

    def _detect_events(self, round_num: int, record: dict):
        """
        Detect notable events for this round.

        Events include:
        - Rank changes
        - Strategy shifts
        - Regulatory actions
        - Consumer switches
        """
        if round_num == 0:
            return

        prev_record = self.rounds_data[-2] if len(self.rounds_data) >= 2 else None
        if not prev_record:
            return

        # Detect rank changes
        curr_leaderboard = record.get("leaderboard", [])
        prev_leaderboard = prev_record.get("leaderboard", [])

        if curr_leaderboard and prev_leaderboard:
            curr_ranks = {name: i for i, (name, _) in enumerate(curr_leaderboard)}
            prev_ranks = {name: i for i, (name, _) in enumerate(prev_leaderboard)}

            for name in curr_ranks:
                if name in prev_ranks:
                    curr_rank = curr_ranks[name]
                    prev_rank = prev_ranks[name]
                    if curr_rank != prev_rank:
                        direction = "up" if curr_rank < prev_rank else "down"
                        change = abs(curr_rank - prev_rank)
                        self.events.append({
                            "round": round_num,
                            "type": "rank_change",
                            "provider": name,
                            "direction": direction,
                            "change": change,
                            "from_rank": prev_rank + 1,
                            "to_rank": curr_rank + 1,
                        })

        # Detect strategy shifts (>15% change in any lever)
        for name, strategy in record.get("strategies", {}).items():
            prev_strategy = prev_record.get("strategies", {}).get(name, {})
            if prev_strategy:
                for lever in ("rd", "safety", "product"):
                    change = abs(strategy.get(lever, 0) - prev_strategy.get(lever, 0))
                    if change > 0.15:
                        curr_val = strategy.get(lever, 0)
                        prev_val = prev_strategy.get(lever, 0)
                        direction = f"more {lever}" if curr_val > prev_val else f"less {lever}"
                        self.events.append({
                            "round": round_num,
                            "type": "strategy_shift",
                            "provider": name,
                            "direction": direction,
                            "change": change,
                        })
                        break  # report only the largest shift per provider per round

        # Detect regulatory actions
        regulator_data = record.get("regulator_data", {})
        if regulator_data.get("interventions"):
            for intervention in regulator_data["interventions"]:
                self.events.append({
                    "round": round_num,
                    "type": "regulation",
                    "regulator": intervention.get("regulator"),
                    "regulation_type": intervention.get("type"),
                    "details": intervention.get("details"),
                })

        # Detect significant consumer switching
        consumer_data = record.get("consumer_data", {})
        switching_rate = consumer_data.get("switching_rate", 0)
        if switching_rate >= 0.05:  # 5%+ of market switching is notable
            self.events.append({
                "round": round_num,
                "type": "consumer_movement",
                "switching_rate": switching_rate,
            })

    def generate_markdown(self) -> str:
        """
        Generate the complete markdown game log.

        Returns:
            Markdown formatted string
        """
        lines = []

        # Header
        lines.append(f"# Game Log: {self.experiment_name}")
        lines.append("")
        if self.experiment_id:
            lines.append(f"**Experiment ID:** {self.experiment_id}")
        lines.append(f"**Mode:** {'LLM-assisted' if self.llm_mode else 'Heuristic'}")
        lines.append(f"**Total Rounds:** {len(self.rounds_data)}")

        # Benchmark params
        if self.benchmarks:
            lines.append("")
            lines.append(f"**Benchmarks ({len(self.benchmarks)}):**")
            for bm in self.benchmarks:
                lines.append(f"- **{bm.get('name', 'Unknown')}**: weight={bm.get('weight', 1.0)}")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Round-by-round summaries
        for record in self.rounds_data:
            lines.extend(self._format_round(record))
            lines.append("")

        # Final summary
        lines.extend(self._generate_final_summary())

        return "\n".join(lines)

    def _format_round(self, record: dict) -> list[str]:
        """Format a single round's data."""
        lines = []
        round_num = record.get("round", 0)

        lines.append(f"## Round {round_num}")
        lines.append("")

        # Leaderboard table
        lines.append("### Leaderboard")
        leaderboard = record.get("leaderboard", [])
        if leaderboard:
            lines.append("| Rank | Provider | Score | True Cap | R&D | Safety | Product |")
            lines.append("|------|----------|-------|----------|-----|--------|---------|")

            for rank, (name, score) in enumerate(leaderboard, 1):
                true_cap = _mean_capability(record, name)
                strategy = record["strategies"].get(name, {})
                rd = strategy.get("rd", 0) * 100
                safety = strategy.get("safety", 0) * 100
                product = strategy.get("product", 0) * 100

                lines.append(
                    f"| {rank} | {name} | {score:.3f} | {true_cap:.3f} | "
                    f"{rd:.0f}% | {safety:.0f}% | {product:.0f}% |"
                )
        lines.append("")

        # Per-benchmark scores (if multi-benchmark)
        per_benchmark = record.get("per_benchmark_scores", {})
        if per_benchmark:
            lines.append("### Per-Benchmark Scores")
            bm_names = record.get("benchmark_names", list(per_benchmark.keys()))
            header = "| Provider | " + " | ".join(bm_names) + " |"
            separator = "|----------|" + "|".join(["-------" for _ in bm_names]) + "|"
            lines.append(header)
            lines.append(separator)

            for name, _ in leaderboard:
                scores_str = " | ".join(
                    f"{per_benchmark.get(bm, {}).get(name, 0):.3f}"
                    for bm in bm_names
                )
                lines.append(f"| {name} | {scores_str} |")
            lines.append("")

        # Score changes (if not first round)
        if round_num > 0 and len(self.rounds_data) > 1:
            prev_record = self.rounds_data[round_num - 1] if round_num <= len(self.rounds_data) - 1 else None
            if prev_record:
                lines.append("### Score Changes")
                for name, score in record.get("scores", {}).items():
                    prev_score = prev_record.get("scores", {}).get(name, score)
                    change = score - prev_score
                    sign = "+" if change >= 0 else ""
                    lines.append(f"- **{name}**: {prev_score:.3f} -> {score:.3f} ({sign}{change:.3f})")
                lines.append("")

        # Events for this round
        round_events = [e for e in self.events if e.get("round") == round_num]
        if round_events:
            lines.append("### Events")
            for event in round_events:
                if event["type"] == "rank_change":
                    lines.append(
                        f"- **{event['provider']}** moved {event['direction']} "
                        f"from #{event['from_rank']} to #{event['to_rank']}"
                    )
                elif event["type"] == "strategy_shift":
                    lines.append(
                        f"- **{event['provider']}** shifted strategy toward {event['direction']} "
                        f"({event['change']:.0%} change)"
                    )
                elif event["type"] == "regulation":
                    lines.append(
                        f"- **Regulation** by {event['regulator']}: {event['regulation_type']}"
                    )
                elif event["type"] == "consumer_movement":
                    rate = event.get('switching_rate', 0)
                    lines.append(
                        f"- **Consumer movement**: {rate:.1%} of market switched providers"
                    )
            lines.append("")

        # New benchmark introduction
        new_bm = record.get("new_benchmark")
        if new_bm:
            lines.append("### New Benchmark Introduced")
            noise_str = f"noise={new_bm['noise']:.2f}" if "noise" in new_bm else ""
            weight_str = f"weight={new_bm['weight']:.2f}" if "weight" in new_bm else ""
            params_str = ", ".join(p for p in [noise_str, weight_str] if p)
            lines.append(f"- **{new_bm['name']}** introduced ({params_str})")
            lines.append(f"  - Trigger: {new_bm.get('trigger', 'N/A')}")
            lines.append("")

        # Actor reasoning traces (all actor types, both LLM and heuristic)
        actor_traces = record.get("actor_traces", {})

        # Provider reasoning — from provider_states (LLM) or actor_traces (heuristic)
        provider_states = record.get("provider_states", {})
        provider_traces = {}
        for name, state in provider_states.items():
            reasoning = state.get("reasoning")
            if reasoning:
                provider_traces[name] = reasoning
        # Fallback to actor_traces for providers
        for name in record.get("scores", {}).keys():
            if name not in provider_traces and name in actor_traces:
                provider_traces[name] = actor_traces[name]

        if provider_traces:
            lines.append("### Provider Reasoning")
            for name, reasoning in provider_traces.items():
                lines.append(f"**{name}:** {reasoning}")
            lines.append("")

        # Non-provider actor reasoning (filter out routine "stay" / "no_action")
        non_provider_traces = {
            k: v for k, v in actor_traces.items()
            if k not in record.get("scores", {})
        }
        # Only show non-trivial decisions to keep the log readable
        notable_traces = {
            k: v for k, v in non_provider_traces.items()
            if not v.startswith("stay:") and not v.startswith("no_action:")
        }
        if notable_traces:
            lines.append("### Other Actor Reasoning")
            for name, reasoning in notable_traces.items():
                lines.append(f"- **{name}:** {reasoning}")
            lines.append("")

        # Media coverage
        media_data = record.get("media_data", {})
        if media_data:
            headlines = media_data.get("headlines", [])
            if headlines:
                lines.append("### Media Coverage")
                sentiment = media_data.get("sentiment", 0)
                sentiment_label = "positive" if sentiment > 0.1 else "negative" if sentiment < -0.1 else "neutral"
                lines.append(f"- Sentiment: {sentiment:.2f} ({sentiment_label})")
                for headline in headlines:
                    lines.append(f"- {headline}")
                risk_signals = media_data.get("risk_signals", [])
                if risk_signals:
                    lines.append(f"- Risk signals: {', '.join(risk_signals)}")
                lines.append("")

        # Consumer data
        consumer_data = record.get("consumer_data", {})
        if consumer_data:
            lines.append("### Consumer Market")
            avg_satisfaction = consumer_data.get("avg_satisfaction")
            switching_rate = consumer_data.get("switching_rate", 0)
            if avg_satisfaction is not None:
                lines.append(f"- Avg Satisfaction: {avg_satisfaction:.3f}")
            lines.append(f"- Switching Rate: {switching_rate:.1%}")

            # Market shares
            market_shares = consumer_data.get("market_shares", {})
            if market_shares:
                shares_str = ", ".join(
                    f"{p}: {s:.1%}" for p, s in
                    sorted(market_shares.items(), key=lambda x: x[1], reverse=True)
                )
                lines.append(f"- Market Shares: {shares_str}")

            # Org LLM reasoning traces (only when consumer_llm_organizations=True)
            org_llm_decisions = consumer_data.get("org_llm_decisions", {})
            if org_llm_decisions:
                lines.append("")
                lines.append("**Organizational Consumer Reasoning (LLM):**")
                for seg_name, decision in org_llm_decisions.items():
                    provider = decision.get("provider", "?")
                    should_switch = decision.get("should_switch", False)
                    target = decision.get("target_provider")
                    confidence = decision.get("confidence", 0.0)
                    reasoning = decision.get("reasoning", "")
                    use_case = decision.get("use_case", "")
                    archetype = decision.get("archetype", "")
                    action = f"SWITCH -> {target}" if should_switch and target else "STAY"
                    lines.append(
                        f"- **{seg_name}** ({use_case}, {archetype}) "
                        f"[{provider}] -> **{action}** (confidence {confidence:.0%})"
                    )
                    if reasoning:
                        lines.append(f"  > {reasoning}")

            lines.append("")

        # Regulatory activity
        regulator_data = record.get("regulator_data", {})
        if regulator_data.get("interventions"):
            lines.append("### Regulatory Activity")
            actor_traces = record.get("actor_traces", {})
            for intervention in regulator_data["interventions"]:
                reg_name = intervention.get("regulator", "")
                target = intervention.get("provider")
                target_text = f" targeting {target}" if target else ""
                lines.append(f"- **{intervention.get('type')}** by {reg_name}{target_text}")
                # Include LLM reasoning inline if available
                reg_reasoning = actor_traces.get(reg_name, "")
                if reg_reasoning and not reg_reasoning.startswith("no_action"):
                    # Strip the "type: " prefix if present to avoid duplication
                    colon_idx = reg_reasoning.find(": ")
                    reasoning_text = reg_reasoning[colon_idx + 2:] if colon_idx != -1 else reg_reasoning
                    lines.append(f"  > {reasoning_text}")
            lines.append("")

        lines.append("---")
        return lines

    def _generate_final_summary(self) -> list[str]:
        """Generate the final summary section."""
        lines = []

        lines.append("## Final Summary")
        lines.append("")

        if not self.rounds_data:
            lines.append("No simulation data recorded.")
            return lines

        final_round = self.rounds_data[-1]
        first_round = self.rounds_data[0]

        # Final standings
        lines.append("### Final Standings")
        leaderboard = final_round.get("leaderboard", [])
        if leaderboard:
            lines.append("| Rank | Provider | Final Score | Cap Growth | Avg R&D | Avg Safety |")
            lines.append("|------|----------|-------------|------------|---------|------------|")

            for rank, (name, score) in enumerate(leaderboard, 1):
                initial_cap = _mean_capability(first_round, name)
                final_cap = _mean_capability(final_round, name)
                cap_growth = final_cap - initial_cap

                total_rd = 0
                total_safety = 0
                count = 0
                for record in self.rounds_data:
                    strategy = record.get("strategies", {}).get(name, {})
                    if strategy:
                        total_rd += strategy.get("rd", 0)
                        total_safety += strategy.get("safety", 0)
                        count += 1

                if count > 0:
                    avg_rd = (total_rd / count) * 100
                    avg_safety = (total_safety / count) * 100
                else:
                    avg_rd = 0
                    avg_safety = 0

                lines.append(
                    f"| {rank} | {name} | {score:.3f} | {cap_growth:+.3f} | {avg_rd:.0f}% | {avg_safety:.0f}% |"
                )
        lines.append("")

        # Event summary
        if self.events:
            lines.append("### Event Summary")

            rank_changes = [e for e in self.events if e["type"] == "rank_change"]
            strategy_shifts = [e for e in self.events if e["type"] == "strategy_shift"]
            regulations = [e for e in self.events if e["type"] == "regulation"]
            consumer_movements = [e for e in self.events if e["type"] == "consumer_movement"]

            lines.append(f"- **Rank changes:** {len(rank_changes)}")
            lines.append(f"- **Strategy shifts:** {len(strategy_shifts)}")
            lines.append(f"- **Regulatory actions:** {len(regulations)}")
            lines.append(f"- **Consumer movement events:** {len(consumer_movements)}")
            lines.append("")

        # Key insights
        lines.append("### Key Insights")

        # Check for Goodhart's Law effects
        if leaderboard and len(leaderboard) >= 2:
            # Find provider with highest score vs highest true capability
            score_leader = leaderboard[0][0]
            cap_leader = max(
                final_round.get("capability_vectors", {}).keys(),
                key=lambda k: _mean_capability(final_round, k)
            )

            if score_leader != cap_leader:
                lines.append(
                    f"- **Goodhart's Law effect detected:** {score_leader} leads on benchmark scores, "
                    f"but {cap_leader} has the highest true capability."
                )
            else:
                lines.append(
                    f"- **Benchmark aligned:** {score_leader} leads on both benchmark scores "
                    f"and true capability."
                )

        # Investment strategy analysis
        for name in final_round.get("strategies", {}).keys():
            total_rd = sum(
                r.get("strategies", {}).get(name, {}).get("rd", 0)
                for r in self.rounds_data
            )
            total_safety = sum(
                r.get("strategies", {}).get(name, {}).get("safety", 0)
                for r in self.rounds_data
            )
            n = len(self.rounds_data) if self.rounds_data else 1

            avg_rd = total_rd / n
            avg_safety = total_safety / n

            if avg_safety > 0.35:
                lines.append(
                    f"- **{name}** prioritized safety investment (avg {avg_safety:.0%})"
                )
            elif avg_rd > 0.6:
                lines.append(
                    f"- **{name}** prioritized R&D (avg {avg_rd:.0%})"
                )

        lines.append("")

        return lines


def generate_game_log_from_history(
    history: list,
    providers: list,
    experiment_name: str = "Simulation",
    experiment_id: str = "",
    llm_mode: bool = False,
    benchmarks: list = None,
) -> str:
    generator = GameLogGenerator(
        experiment_name=experiment_name,
        experiment_id=experiment_id,
        llm_mode=llm_mode,
        benchmarks=benchmarks,
    )

    for round_data in history:
        generator.record_round(round_data=round_data, providers=providers)

    return generator.generate_markdown()
