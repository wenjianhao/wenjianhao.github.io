#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
OUTFILE = ROOT / "static" / "data" / "visitors.json"

DEFAULT_OUTPUT = {
    "source": "preview",
    "views": 12438,
    "visitors": 3184,
    "countries": 42,
    "updated_at": None,
    "locations": [
        {"code": "US", "name": "United States", "views": 4200},
        {"code": "CA", "name": "Canada", "views": 780},
        {"code": "GB", "name": "United Kingdom", "views": 960},
        {"code": "DE", "name": "Germany", "views": 620},
        {"code": "IN", "name": "India", "views": 1320},
        {"code": "CN", "name": "China", "views": 880},
        {"code": "AU", "name": "Australia", "views": 530},
        {"code": "BR", "name": "Brazil", "views": 460},
    ],
}


def resolve_base():
    endpoint = os.getenv("GOATCOUNTER_ENDPOINT", "").strip()
    site = os.getenv("GOATCOUNTER_CODE", "").strip()
    if endpoint:
        return endpoint.rstrip("/") + "/api/v0"
    if site:
        if site.startswith("http://") or site.startswith("https://"):
            return site.rstrip("/") + "/api/v0"
        return f"https://{site}.goatcounter.com/api/v0"
    return ""


def fetch_json(base, path, token, params=None):
    url = f"{base}{path}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "wenjianhao-site-visitors-fetcher/1.0",
    })
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_items(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("hits", "stats", "locations", "results", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def read_number(item, *keys):
    for key in keys:
        value = item.get(key)
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return 0


def normalize_location(item):
    code = str(item.get("id") or item.get("code") or item.get("country_code") or "").strip().upper()
    name = str(item.get("name") or item.get("label") or item.get("country") or code).strip()
    views = read_number(item, "count", "views", "total", "visitors")
    visitors = read_number(item, "visitors", "count", "total")
    return {
        "code": code,
        "name": name or code,
        "views": views,
        "visitors": visitors,
    }


def main():
    token = os.getenv("GOATCOUNTER_API_KEY", "").strip()
    base = resolve_base()
    if not token or not base:
        print("Missing GoatCounter config; writing preview data.", file=sys.stderr)
        OUTFILE.parent.mkdir(parents=True, exist_ok=True)
        OUTFILE.write_text(json.dumps(DEFAULT_OUTPUT, indent=2) + "\n", encoding="utf-8")
        return 0

    total = fetch_json(base, "/stats/total", token)
    hits = fetch_json(base, "/stats/hits", token, {"limit": 200})
    locations = fetch_json(base, "/stats/locations", token, {"limit": 60})

    hit_items = list_items(hits)
    location_items = [normalize_location(item) for item in list_items(locations)]
    location_items = [item for item in location_items if item["code"] or item["name"]]
    location_items.sort(key=lambda item: item["views"], reverse=True)

    views = sum(read_number(item, "count", "views", "total") for item in hit_items)
    visitors = read_number(total, "total", "count", "visitors")
    countries = len({item["code"] or item["name"] for item in location_items})

    output = {
        "source": "goatcounter",
        "views": views,
        "visitors": visitors,
        "countries": countries,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "locations": location_items,
    }

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    OUTFILE.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
