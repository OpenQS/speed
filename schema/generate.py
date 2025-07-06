import argparse
import json
from .schema import DataModel

def generate_scheme():
    p = argparse.ArgumentParser(description="Dump DataModel JSON schema")
    p.add_argument(
        "-o","--output",
        help="Where to write schema.json",
        default="schema.json"
    )
    args = p.parse_args()

    schema = DataModel.model_json_schema()  # Pydantic v2
    with open(args.output, "w") as f:
        json.dump(schema, f, indent=2)
