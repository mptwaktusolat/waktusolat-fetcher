import json
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil.relativedelta import relativedelta

import requests
import urllib3


def fetch_data(relative_month: int):
    """
    Fetch data from the given relative month
    """
    urllib3.disable_warnings()  # disable certificate error warning

    reqUrl = "https://www.e-solat.gov.my/index.php"

    jakim_code = [
        "JHR01", "JHR02", "JHR03", "JHR04", "KDH01", "KDH02", "KDH03", "KDH04", "KDH05", "KDH06", "KDH07",
        "KTN01", "KTN02", "MLK01", "NGS01", "NGS02", "NGS03", "PHG01", "PHG02", "PHG03", "PHG04", "PHG05",
        "PHG06", "PHG07", "PRK01", "PRK02", "PRK03", "PRK04", "PRK05", "PRK06", "PRK07", "PLS01", "PNG01",
        "SBH01", "SBH02", "SBH03", "SBH04", "SBH05", "SBH06", "SBH07", "SBH08", "SBH09", "SGR01", "SGR02",
        "SGR03", "SWK01", "SWK02", "SWK03", "SWK04", "SWK05", "SWK06", "SWK07", "SWK08", "SWK09", "TRG01",
        "TRG02", "TRG03", "TRG04", "WLY01", "WLY02"
    ]  # Total 60

    # for testing
    # jakim_code = ["JHR01", "JHR02"]
    # jakim_code = ["KDH01", "KDH02"]

    data = {}
    data['jakim'] = []

    # Get next month
    fetch_date_target = datetime.now() + relativedelta(months=relative_month)
    fetch_month = fetch_date_target.month
    fetch_year = fetch_date_target.year

    # Get last day of next month (For whatever given month, it will limit to the last day of the month)
    last_day_of_next_month = (fetch_date_target +
                              relativedelta(day=31)).day

    print(f'Total of {len(jakim_code)}')

    print(f'ℹ️ Fetching for {fetch_date_target.strftime("%B")} {fetch_year}')

    print('\nStarting\n')

    attempt_count = 0

    # Retry the failed request until all filled up
    while len(jakim_code) != 0:
        if (attempt_count > 0):
            failed = '", "'.join(x for x in jakim_code)
            print(f'\n💔 Failed to fetch: "{failed}"')
            print(f'\n🔄 Retrying failed requests. Attempt #{attempt_count}\n')

        # Iterate each of the JAKIM code
        for zone in jakim_code:

            params = {
                'r': 'esolatApi/takwimsolat',
                'period': 'duration',
                'zone': zone,
            }

            payload = f"datestart={fetch_year}-{fetch_month}-01&dateend={fetch_year}-{fetch_month}-{last_day_of_next_month}"
            headers = {
                "User-Agent": "iqfareez",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.post(
                reqUrl, params=params, data=payload, headers=headers, verify=False, timeout=5)

            json_response = response.json()

            # Only put into json if everything's fine
            if (response.status_code == 200):
                response_code = json_response['status']
                if response_code == 'OK!':
                    print(f"{zone} : {response_code}")
                    data['jakim'].append(json_response)
                else:
                    print(f'{zone} : Failed ({response_code}). Skipping for now')

                jakim_code.remove(zone)
            else:
                print(f'{zone} : Failed ({response.status_code})')

            # Adding artificial delay to prevent 'ddosing' their server
            time.sleep(2.0)

        attempt_count += 1

    # Don't be scared, this block of code just for logging time
    fetch_finish = datetime.now(ZoneInfo('Asia/Kuala_Lumpur'))
    # number of seconds since epoch
    fetch_finish = int(fetch_finish.timestamp())
    print(f'\nFetching finish at {fetch_finish}')
    data['last_fetched'] = fetch_finish

    # writing all location data to file
    os.makedirs('outputs', exist_ok=True)

    # ImportantL The filename format is "Month-Year.json", do not
    # simply change the implementation because some function preceeding
    # will need to determine date etc based on the filename
    filename = f'outputs/{fetch_date_target.strftime("%b-%Y")}.json'

    with open(filename, 'w+') as outfile:
        json.dump(data, outfile, indent=2)
        print(f'\n✅Finish writing to {filename}')


if __name__ == "__main__":
    print("This script is not meant to invoke by itself. So use this to debugging only")
    fetch_data(8)
