"""Check which rows are visible when querying with only the Supabase anon key.

Run with:
    python scripts/test_anon_rls.py

Run from the conference-rag folder, or pass this script's path from elsewhere.
"""

import json
from pathlib import Path

from supabase import create_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config.public.json"


def main():
    with CONFIG_PATH.open(encoding="utf-8-sig") as config_file:
        public_config = json.load(config_file)

    client = create_client(
        public_config["SUPABASE_URL"],
        public_config["SUPABASE_ANON_KEY"],
    )

    for table in ("page_views", "sentence_embeddings"):
        try:
            result = client.table(table).select("*").limit(5).execute()
            row_count = len(result.data)
            print(f"{table}: query succeeded; {row_count} visible rows")

            if table == "sentence_embeddings" and row_count == 0:
                print(
                    "  Zero visible rows only demonstrates RLS filtering if "
                    "the table contains rows."
                )
        except Exception as exc:
            print(f"{table}: query failed: {exc}")


if __name__ == "__main__":
    main()
