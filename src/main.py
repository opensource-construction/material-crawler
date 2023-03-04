import json
from pathlib import Path

import requests as requests


def main(p: Path):
    urls = json.loads(p.read_text())

    data = []
    for url in urls:
        data.append(crawl(url))

    out = Path("../index.json")
    out.write_text(json.dumps(data, indent=2))


def crawl(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    keys = list(data.keys())
    data.update({"@id": url})

    if "@context" in keys:
        return data
    else:
        data.update({"@context": {
            "@version": 1.1,
            "schema": "https://schema.org/",
            "name": "schema:Product",
            "isAccessoryOrSparePartFor": {
                "@id": "schema:isAccessoryOrSparePartFor",
                "@container": "@type"
            },
        }})
        return data


if __name__ == "__main__":
    p = Path("input.json")
    main(p)
