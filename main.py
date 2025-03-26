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
    fetch_parser.add_argument('--relative-month', help='Relative month to fetch. Example: 0 for current month, 1 for next month, -1 for previous month', type=int, required=False, default=0)
    fetch_parser.add_argument('--no-push', help='Skip pushing to Firebase', action='store_true')

    # Call the appropriate subcommand function based on the chosen command
    args = parser.parse_args()
    if args.command == 'fetch':
        fetch_flow(args)

def fetch_flow(args):
    # Step 1: Fetch all zones data
    print('🚀 Fetch flow started. Step 1 Started')
    fetcher.fetch_data(args.relative_month)
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
