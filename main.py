import argparse

import sys

sys.path.append('scripts')

import scripts.fetcher as fetcher
import scripts.process_db as processor
import scripts.push_db as pusher


def main():
    # Parsing arguments https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Fetch and process Waktu Solat data from JAKIM')
    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    fetch_parser = subparsers.add_parser('fetch', help='Fetch data from JAKIM')
    fetch_parser.add_argument('--year', help='Year to fetch (required). Will fetch all months (Jan-Dec) if --month is not specified', type=int, required=True)
    fetch_parser.add_argument('--month', help='Specific month to fetch (1-12). If not specified, fetches all months for the year', type=int, choices=range(1, 13), metavar='1-12')
    fetch_parser.add_argument('--no-push', help='Skip pushing to Firebase', action='store_true')

    # Call the appropriate subcommand function based on the chosen command
    args = parser.parse_args()
    if args.command == 'fetch':
        fetch_flow(args)

def fetch_flow(args):
    # Step 1: Fetch all zones data
    print('🚀 Fetch flow started. Step 1 Started')
    
    if args.month:
        # Fetch specific month
        print(f'📅 Fetching data for {args.year}-{args.month:02d}')
        fetcher.fetch_data(args.year, args.month)
    else:
        # Fetch all months (Jan-Dec)
        print(f'📅 Fetching data for all months in {args.year}')
        for month in range(1, 13):
            print(f'\n--- Fetching month {month}/12 ---')
            fetcher.fetch_data(args.year, month)
    
    print('🆗 Step 1 Finished')

    # Step 2: Process the data
    print('🚀 Step 2 Started')
    processor.process_db()
    print('🆗 Step 2 Finished')

    # Step 3: Push to Firebase
    if args.no_push:
        print('🚫 Skipping Step 3')
        return

    print('🚀 Step 3 started')
    pusher.push_to_firebase()
    print('🆗 Step 3 Finished')


if __name__ == '__main__':
    main()
