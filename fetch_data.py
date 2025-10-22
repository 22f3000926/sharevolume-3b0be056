#!/usr/bin/env python3
"""
fetch_data.py

Fetches common stock shares outstanding data for AbbVie (CIK 0001551152) from SEC API,
filters for fiscal years > 2020, extracts max and min `val`, and saves to data.json.

SEC requires a descriptive User-Agent in HTTP requests.
"""

import json
import urllib.request

CIK = '0001551152'
URL = f'https://data.sec.gov/api/xbrl/companyconcept/CIK{CIK}/dei/EntityCommonStockSharesOutstanding.json'
USER_AGENT = 'MyApp/1.0 (example@example.com) AbbVieSharesOutstandingFetcher'


def fetch_data(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Accept-Encoding', 'gzip, deflate')
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.getheader('Content-Encoding') == 'gzip':
                import gzip
                data = gzip.decompress(resp.read())
            else:
                data = resp.read()
            return data.decode('utf-8')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def process_data(raw_json):
    obj = json.loads(raw_json)

    entity_name = obj.get('entityName', '').strip()
    units = obj.get('units', {})
    shares_list = units.get('shares', [])

    filtered = []
    for entry in shares_list:
        fy = entry.get('fy')
        val = entry.get('val')
        if fy and val is not None:
            # Ensure fy is a string representing year-like
            if fy > '2020':  # string compare works here because FY is YYYY format
                try:
                    number_val = float(val)
                    filtered.append({'fy': fy, 'val': number_val})
                except Exception:
                    continue

    if not filtered:
        raise ValueError('No shares outstanding data found for fiscal years > 2020.')

    max_entry = max(filtered, key=lambda x: x['val'])
    min_entry = min(filtered, key=lambda x: x['val'])

    result = {
        'entityName': entity_name,
        'max': {'val': max_entry['val'], 'fy': max_entry['fy']},
        'min': {'val': min_entry['val'], 'fy': min_entry['fy']}
    }

    return result


def main():
    print(f"Fetching data for CIK {CIK} from SEC API...")
    raw_data = fetch_data(URL)
    if raw_data is None:
        print("Failed to fetch data; exiting.")
        return

    try:
        processed = process_data(raw_data)
    except Exception as e:
        print(f"Error processing data: {e}")
        return

    out_filename = 'data.json'
    with open(out_filename, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2)

    print(f"Processed data saved to {out_filename}. Entity Name: {processed['entityName']}")


if __name__ == '__main__':
    main()
