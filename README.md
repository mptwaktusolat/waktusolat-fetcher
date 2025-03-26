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

**Step 1**: This command will fetch the prayer time data for all states for the
current month (default). If you want to fetch for other month, you can pass the
`--relative-month` arguments (accepts integer input). A file `month-year.json` will be produced.

**Step 2**: Next, the date time will be parsed and save as UNIX timestamp (seconds). Another
output file will be produced (`month-year.processed.json`).

> **Note** All produced files will be saved in the `output` directory.

**Step 3**: Then, the processed data will be pushed to the Firebase Firestore. You can skip
this step by passing the argument `--no-push`. (You may need to have Firebase admin credential JSON file)
