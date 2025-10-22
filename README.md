# AbbVie Share Outstanding Data Viewer

This project fetches and displays annual common stock shares outstanding data for AbbVie (CIK 0001551152) from the SEC EDGAR API. It processes the data to find the highest and lowest reported shares outstanding for fiscal years after 2020, and renders the results in a clean, responsive HTML page.

## Features

- Fetches data from the SEC's official XBRL company concept endpoint with a descriptive User-Agent header respecting SEC guidelines.
- Processes JSON to find the maximum and minimum shares outstanding (`val`) and their associated fiscal year (`fy`) for years after 2020.
- Saves the processed results in `data.json`, including the entity name.
- Displays results in an elegant and accessible `index.html` page.
- Dynamically updates display when loaded with a `?CIK=xxxxxxxxxx` query parameter by fetching data of the specified CIK (via a proxy to bypass CORS restrictions).

## Files

- `README.md` - This documentation.
- `index.html` - Main web page that displays the shares outstanding data.
- `fetch_data.py` - Python script to fetch, process, and save the processed data for AbbVie.
- `data.json` - Processed data JSON for AbbVie.
- `uid.txt` - Provided UID as-is.
- `LICENSE` - MIT License text.

## How to Use

### Viewing the Data

Simply open `index.html` in a modern web browser. The page will fetch the AbbVie data and display:
- Entity Name (in title and header)
- Maximum and minimum shares outstanding values and their fiscal years

### Viewing Other Companies

Append `?CIK=xxxxxxxxxx` (ten-digit CIK number) to the URL of the page:

```
index.html?CIK=0001018724
```

The page will dynamically fetch and display data for that CIK (using a free proxy to bypass CORS restrictions), updating the title, header, and values without reloading the page.

### Generating/Updating AbbVie Data

To re-fetch and update the `data.json` for AbbVie:

1. Ensure Python 3 is installed.
2. Run:

```bash
python fetch_data.py
```

This will download fresh data from the SEC and output the processed JSON to `data.json`.

## Technical Details

- The Python script sets a descriptive User-Agent as per SEC guidelines.
- Data is filtered to include fiscal years (`fy`) strictly greater than "2020".
- The SEC endpoint:/api/xbrl/companyconcept/CIK{CIK}/dei/EntityCommonStockSharesOutstanding.json
- The JavaScript in `index.html` handles fetching, parsing, and updating the DOM.
- A publicly available proxy (https://api.allorigins.win/get?url=) is used to avoid CORS issues when fetching SEC data for other CIKs.

## Dependencies

- Python 3 standard libraries only (no external packages).
- Modern web browser with ES6 JavaScript support.

## Notes

- The SEC API may occasionally have downtime or rate limits.
- The proxy used is public and may have usage limitations; for production usage, consider deploying your own proxy.


## License

MIT License