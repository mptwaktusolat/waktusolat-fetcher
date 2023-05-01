# Waktu Solat fetcher (Malaysia)

Simple CLI utility to fetch prayer time data from JAKIM.

:construction: This is still **work-in-progress** :construction: Related to https://github.com/mptwaktusolat/mpt-server/issues/3

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

### `fetch`

**Step 1**: This command will fetch the prayer time data for all states for the 
upcoming month. For example, now you are on May 2023, it will fetch
the data for June 2023. A file `month-year.json` will be produced.

**Step 2**: Next, the date time will be parsed and save as UNIX timestamp (seconds). Another 
output file will be produced (`month-year.processed.json`).

> **Note** All produced files will be saved in the `output` directory. 

**Step 3**: Then, the processed data will be pushed to the Firebase Firestore. You can skip
this step by passing the argument `--no-push`.



