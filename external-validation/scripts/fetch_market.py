"""
fetch_market.py — Collect market share proxy data from public sources.

Sources:
  1. SimilarWeb public pages — monthly visit estimates (scraped HTML)
  2. Stack Overflow Developer Survey CSV — AI tool usage percentages

Writes:
  validation/data/raw/market/web_traffic.csv
  validation/data/raw/market/so_survey.csv

Usage:
    python validation/scripts/fetch_market.py [--skip-similarweb] [--skip-so]

Notes:
  - SimilarWeb scraping uses only the publicly visible stats page (no login).
    It is inherently fragile; if scraping fails, the script writes a stub CSV
    with a note so downstream steps don't break.
  - SO survey CSVs must be downloaded manually from:
      https://insights.stackoverflow.com/survey
    Place the CSV in validation/data/raw/market/ and re-run.
"""

import argparse
import csv
import io
import re
import time
from datetime import datetime
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "market"

# ---------------------------------------------------------------------------
# SimilarWeb config
# ---------------------------------------------------------------------------
SW_TARGETS = {
    "chat.openai.com": "Orion Labs",
    "claude.ai": "Apex AI",
    "gemini.google.com": "Genesis Systems",
    "character.ai": "Other",
    "mistral.ai": "Spark AI",
}

SW_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def parse_similarweb_visits(html: str) -> str | None:
    """
    Extract the monthly visit count from a SimilarWeb website overview page.
    The count appears in a span near 'Total Visits' or as a data attribute.
    Returns a string like '1.2B' or '345.6M', or None if not found.
    """
    # Try JSON-LD or data attributes first
    m = re.search(r'"totalVisits"\s*:\s*"?([0-9.,]+[BMK]?)"?', html, re.I)
    if m:
        return m.group(1)
    # Fallback: look for text patterns like "1.2B" near "Total Visits"
    m = re.search(
        r'Total Visits[^<]{0,200}?([0-9]+\.?[0-9]*\s*[BMK])',
        html, re.I | re.S
    )
    if m:
        return m.group(1).strip()
    return None


def visits_to_float(visits_str: str | None) -> float | None:
    """Convert '1.2B' / '345.6M' / '12.3K' to a float (raw count)."""
    if not visits_str:
        return None
    s = visits_str.strip().upper().replace(",", "")
    multipliers = {"B": 1e9, "M": 1e6, "K": 1e3}
    for suffix, mult in multipliers.items():
        if s.endswith(suffix):
            try:
                return float(s[:-1]) * mult
            except ValueError:
                return None
    try:
        return float(s)
    except ValueError:
        return None


def fetch_similarweb() -> list[dict]:
    rows = []
    scrape_date = datetime.today().strftime("%Y-%m")

    for domain, sim_provider in SW_TARGETS.items():
        url = f"https://www.similarweb.com/website/{domain}/"
        print(f"  Fetching SimilarWeb for {domain} ...")
        try:
            resp = requests.get(url, headers=SW_HEADERS, timeout=30)
            if resp.status_code == 200:
                visits_str = parse_similarweb_visits(resp.text)
                visits = visits_to_float(visits_str)
                rows.append({
                    "domain": domain,
                    "provider_raw": domain,
                    "sim_provider": sim_provider,
                    "date": scrape_date,
                    "monthly_visits": visits,
                    "visits_label": visits_str or "N/A",
                    "source": "similarweb",
                })
                print(f"    -> {visits_str}")
            else:
                print(f"    [WARN] HTTP {resp.status_code}")
                rows.append({
                    "domain": domain,
                    "provider_raw": domain,
                    "sim_provider": sim_provider,
                    "date": scrape_date,
                    "monthly_visits": None,
                    "visits_label": f"HTTP_{resp.status_code}",
                    "source": "similarweb",
                })
        except Exception as exc:
            print(f"    [ERROR] {exc}")
            rows.append({
                "domain": domain,
                "provider_raw": domain,
                "sim_provider": sim_provider,
                "date": scrape_date,
                "monthly_visits": None,
                "visits_label": f"ERROR:{exc}",
                "source": "similarweb",
            })
        time.sleep(2)

    return rows


# ---------------------------------------------------------------------------
# Stack Overflow Developer Survey
# ---------------------------------------------------------------------------
# Column name patterns that indicate AI tool usage (vary across survey years)
SO_AI_COLUMNS = [
    "AIToolCurrently",
    "AISearchHave",
    "AISelect",
    "ai_tools",
]

# Map SO response values → sim providers
SO_PROVIDER_MAP = {
    "ChatGPT": "Orion Labs",
    "OpenAI": "Orion Labs",
    "Bing AI": "Orion Labs",
    "Claude": "Apex AI",
    "Anthropic": "Apex AI",
    "Google Bard": "Genesis Systems",
    "Gemini": "Genesis Systems",
    "GitHub Copilot": "Orion Labs",
    "Meta AI": "Mirage AI",
    "Llama": "Mirage AI",
    "Mistral": "Spark AI",
    "DeepSeek": "OpenCore",
}

SO_SURVEY_FILES = sorted(RAW_DIR.glob("so_survey*.csv")) if RAW_DIR.exists() else []


def parse_so_survey(csv_path: Path) -> list[dict]:
    """
    Parse a Stack Overflow survey CSV and count AI tool mentions per provider.
    Returns normalized usage fractions.
    """
    rows = []
    # Infer year from filename (e.g. so_survey_2024.csv)
    m = re.search(r"(\d{4})", csv_path.name)
    year = m.group(1) if m else "unknown"

    try:
        with csv_path.open(encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []

            # Find the AI tool column
            ai_col = None
            for col in fieldnames:
                if any(pat.lower() in col.lower() for pat in SO_AI_COLUMNS):
                    ai_col = col
                    break

            if not ai_col:
                print(f"    [WARN] No AI tool column found in {csv_path.name}")
                return []

            counts: dict[str, int] = {}
            total_respondents = 0

            for record in reader:
                total_respondents += 1
                cell = record.get(ai_col, "")
                # Multiple tools separated by ";" in SO surveys
                for tool in cell.split(";"):
                    tool = tool.strip()
                    for keyword, sim_prov in SO_PROVIDER_MAP.items():
                        if keyword.lower() in tool.lower():
                            counts[sim_prov] = counts.get(sim_prov, 0) + 1
                            break  # count each respondent once per sim_prov

            for sim_prov, count in counts.items():
                rows.append({
                    "sim_provider": sim_prov,
                    "provider_raw": sim_prov,
                    "date": f"{year}-01",
                    "usage_fraction": count / total_respondents if total_respondents else 0,
                    "respondent_count": count,
                    "total_respondents": total_respondents,
                    "source": f"so_survey_{year}",
                })

    except Exception as exc:
        print(f"    [ERROR] Parsing {csv_path}: {exc}")

    return rows


def write_csv(rows: list[dict], out_path: Path) -> None:
    if not rows:
        out_path.write_text("# No data collected\n")
        return
    fieldnames = list(rows[0].keys())
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(skip_similarweb: bool, skip_so: bool) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # --- SimilarWeb ---
    if not skip_similarweb:
        print("Fetching SimilarWeb web traffic estimates ...")
        sw_rows = fetch_similarweb()
        out = RAW_DIR / "web_traffic.csv"
        write_csv(sw_rows, out)
        print(f"  -> {len(sw_rows)} rows written to {out}")
    else:
        print("Skipping SimilarWeb.")

    # --- Stack Overflow ---
    if not skip_so:
        survey_files = sorted(RAW_DIR.glob("so_survey*.csv"))
        if not survey_files:
            print(
                "[INFO] No SO survey CSVs found in data/raw/market/.\n"
                "  Download from https://insights.stackoverflow.com/survey\n"
                "  and save as so_survey_<year>.csv"
            )
            (RAW_DIR / "so_survey.csv").write_text(
                "# Place so_survey_<year>.csv files in this directory and re-run fetch_market.py\n"
            )
        else:
            all_so_rows = []
            for sf in survey_files:
                print(f"Parsing SO survey: {sf.name} ...")
                all_so_rows.extend(parse_so_survey(sf))
            out = RAW_DIR / "so_survey.csv"
            write_csv(all_so_rows, out)
            print(f"  -> {len(all_so_rows)} rows written to {out}")
    else:
        print("Skipping SO survey.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-similarweb", action="store_true")
    parser.add_argument("--skip-so", action="store_true")
    args = parser.parse_args()
    main(args.skip_similarweb, args.skip_so)
