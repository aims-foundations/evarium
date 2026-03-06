import os
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

load_dotenv(Path(__file__).parent.parent / ".env")

token = os.environ.get("HF_TOKEN")
if not token:
    raise ValueError("HF_TOKEN not found in .env")

snapshot_download(
    repo_id="aims-foundation/ecosystem",
    repo_type="dataset",
    local_dir=Path(__file__).parent.parent / "hf_data",
    token=token,
    max_workers=4,  # reduce parallel requests to avoid rate limiting
)

print("Done.")
