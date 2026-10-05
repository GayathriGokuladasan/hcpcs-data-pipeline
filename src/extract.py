import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL = "https://www.hcpcsdata.com/Codes/A"

OUTPUT_FILE = Path("data/raw/hcpcs_A.json")


def extract_hcpcs():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.hcpcsdata.com/",
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("tr.clickable-row")

    records = []

    for row in rows:
        cells = row.find_all("td")

        if len(cells) < 2:
            continue

        code = cells[0].get_text(strip=True)

        description = cells[1].get_text(
            " ",
            strip=True
        )

        records.append(
            {
                "hcpcs_code": code,
                "group_code": "A",
                "category_name": (
                    "Transportation Services Including Ambulance, "
                    "Medical & Surgical Supplies"
                ),
                "long_description": description,
            }
        )

    return records


def save_raw_data(records):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False
        )


if __name__ == "__main__":
    records = extract_hcpcs()

    save_raw_data(records)

    print(f"Extracted {len(records)} HCPCS records.")
    print(f"Raw data saved to: {OUTPUT_FILE}")