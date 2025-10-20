# Waktu Solat fetcher (Malaysia)

Simple CLI utility to fetch (read: scrape) prayer time data from JAKIM.

## Get Started (Development)

1. Clone this repository
2. Install dependencies
   ```pwsh
   pip install -r requirements.txt
   ```
3. Run the script
   ```pwsh
   py main.py
   ```

## Usage

To view all available commands, run:

```pwsh
py main.py -h
```

To view help for specific command, run:

```pwsh
py main.py <command> -h
```

### `fetch`

**Step 1**: This command will fetch the prayer time data for all zones from the API.
You must specify the `--year` argument. Optionally, you can specify `--month` (1-12) to fetch
a specific month. If `--month` is not provided, it will fetch all months (Jan-Dec) for the given year.
A file `month-year.json` will be produced for each month.

Examples:

```pwsh
# Fetch all months for 2025
py main.py fetch --year 2025

# Fetch only June 2025
py main.py fetch --year 2025 --month 6

# Fetch all months for 2026 without pushing to Firebase
py main.py fetch --year 2026 --no-push
```

**Step 2**: Next, the date time will be parsed and saved as UNIX timestamp (seconds). Another
output file will be produced (`month-year.processed.json`).

> **Note** All produced files will be saved in the `outputs` directory.

**Step 3**: Then, the processed data will be pushed to the Firebase Firestore. You can skip
this step by passing the argument `--no-push`. (You may need to have Firebase admin credential JSON file)
