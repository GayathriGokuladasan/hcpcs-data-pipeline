import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.hcpcsdata.com"
CODES_URL = f"{BASE_URL}/Codes"

OUTPUT_FILE = Path("data/raw/hcpcs_all.json")


HEADERS = {
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


def get_page(session, url):
    response = session.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def get_hcpcs_groups(session):
    soup = get_page(
        session,
        CODES_URL
    )

    groups = []

    for link in soup.find_all("a", href=True):
        href = link["href"]

        if href.startswith("/Codes/") and len(href) == len("/Codes/A"):
            group_code = href.split("/")[-1]

            if group_code.isalpha() and group_code.isupper():
                row = link.find_parent("tr")

                if row is None:
                    continue

                cells = row.find_all("td")

                if len(cells) < 3:
                    continue

                category_name = cells[2].get_text(
                    " ",
                    strip=True
                )

                groups.append(
                    {
                        "group_code": group_code,
                        "category_name": category_name,
                        "url": urljoin(BASE_URL, href),
                    }
                )

    return groups


def extract_group(session, group):
    soup = get_page(
        session,
        group["url"]
    )

    rows = soup.select(
        "tr.clickable-row"
    )

    records = []

    for row in rows:
        cells = row.find_all("td")

        if len(cells) < 2:
            continue

        code = cells[0].get_text(
            strip=True
        )

        description = cells[1].get_text(
            " ",
            strip=True
        )

        records.append(
            {
                "hcpcs_code": code,
                "group_code": group["group_code"],
                "category_name": group["category_name"],
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


def main():
    session = requests.Session()

    print("Finding HCPCS groups...")

    groups = get_hcpcs_groups(session)

    print(
        f"Found {len(groups)} HCPCS groups."
    )

    all_records = []

    for group in groups:
        print(
            f"Extracting group {group['group_code']}..."
        )

        records = extract_group(
            session,
            group
        )

        print(
            f"  Extracted {len(records)} records."
        )

        all_records.extend(records)

    save_raw_data(
        all_records
    )

    print()
    print(
        f"Total records extracted: {len(all_records)}"
    )
    print(
        f"Raw data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
