"""Validate claim-level sources and write outputs/tables/claim_provenance.csv."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rsimodel.provenance import write_claim_provenance_csv  # noqa: E402


if __name__ == "__main__":
    path = write_claim_provenance_csv()
    print(f"wrote {path.relative_to(ROOT)}")
