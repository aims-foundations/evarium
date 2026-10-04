"""Fetch the exact webfont faces evaluarium currently requests from Google,
and rewrite them as self-hosted @font-face rules.

Keeps only the latin and latin-ext subsets. The site is English prose with
European author names in the literature strip, so latin-ext is the floor;
cyrillic/greek/vietnamese subsets are dropped.
"""
import re, os, sys, urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# Exactly the families/axes the five pages ask for today.
CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Google+Sans+Flex:slnt,wght@-10,300..700;0,300..700"
    "&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400"
    "&family=Roboto+Mono:wght@400;500;700"
    "&display=swap"
)

KEEP = {"latin", "latin-ext"}
OUT_DIR = sys.argv[1]

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if binary else r.read().decode("utf-8")

css = get(CSS_URL)

# Blocks look like:  /* latin */\n@font-face {\n ... \n}
blocks = re.findall(r"/\*\s*([a-z0-9-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
print(f"parsed {len(blocks)} @font-face blocks; subsets present: "
      f"{sorted(set(s for s, _ in blocks))}")

os.makedirs(OUT_DIR, exist_ok=True)
kept, seen = [], {}

for subset, block in blocks:
    if subset not in KEEP:
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
    style = re.search(r"font-style:\s*([^;]+);", block)
    style = style.group(1).strip() if style else "normal"

    slug = fam.lower().replace(" ", "-")
    stylish = style.replace(" ", "").replace("oblique10deg", "oblique")
    name = f"{slug}-{stylish}-{subset}.woff2"
    name = re.sub(r"[^a-z0-9.-]", "", name)

    path = os.path.join(OUT_DIR, name)
    if name not in seen:
        data = get(url, binary=True)
        with open(path, "wb") as fh:
            fh.write(data)
        seen[name] = len(data)
        print(f"  {name:52s} {len(data):>8,} bytes   ({fam} / {style} / {subset})")

    kept.append(block.replace(url, f"../fonts/{name}"))

print(f"\nkept {len(kept)} faces, {len(seen)} files, "
      f"{sum(seen.values()):,} bytes total")

with open(os.path.join(OUT_DIR, "_faces.css"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(kept) + "\n")
print(f"css written to {os.path.join(OUT_DIR, '_faces.css')}")
