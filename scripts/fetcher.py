import json
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil.relativedelta import relativedelta

import requests
import urllib3


def fetch_data():
    urllib3.disable_warnings()  # disable certificate error warning

    reqUrl = "https://www.e-solat.gov.my/index.php"

    jakim_code = [
        "JHR01", "JHR02", "JHR03", "JHR04", "KDH01", "KDH02", "KDH03", "KDH04",
        "KDH05", "KDH06", "KDH07", "KTN01", "KTN02", "MLK01", "NGS01", "NGS02", "NGS03",
        "PHG01", "PHG02", "PHG03", "PHG04", "PHG05", "PHG06", "PRK01", "PRK02",
        "PRK03", "PRK04", "PRK05", "PRK06", "PRK07", "PLS01", "PNG01", "SBH01",
        "SBH02", "SBH03", "SBH04", "SBH05", "SBH06", "SBH07", "SBH08", "SBH09",
        "SGR01", "SGR02", "SGR03", "SWK01", "SWK02", "SWK03", "SWK04", "SWK05",
        "SWK06", "SWK07", "SWK08", "SWK09", "TRG01", "TRG02", "TRG03", "TRG04",
        "WLY01", "WLY02"
    ]  # Total 59

    # for testing
    # jakim_code = ["SWK08"]

    data = {}
    data['jakim'] = []

    # Get next month
    fetch_date_target = datetime.now() + relativedelta(months=1)
    fetch_month = fetch_date_target.month
    fetch_year = fetch_date_target.year

    last_day_of_next_month = (fetch_date_target.replace(day=1) +
                              relativedelta(months=1) - relativedelta(days=1)).day

    print(f'Total of {len(jakim_code)}')

    print(f'Fetching for {fetch_date_target.strftime("%B")} {fetch_year}')
    print('\nStarting\n')

    attempt_count = 0

    # Retry the failed request until all filled up
    while len(jakim_code) != 0:
        if (attempt_count > 0):
            failed = '", "'.join(x for x in jakim_code)
            print(f'\nFailed to fetch: "{failed}"')
            print(f'\nRetrying failed requests. Attempt #{attempt_count}\n')

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

            response = requests.post(reqUrl,
                                     params=params,
                                     data=payload,
                                     headers=headers,
                                     verify=False)

            json_response = response.json()

            # Only put into json if everything's fine
            if (response.status_code == 200) and json_response['status'] == 'OK!':
                print(f"{zone} : {json_response['status']}")
                data['jakim'].append(json_response)
                jakim_code.remove(zone)
            else:
                print(f'{zone} : Failed ({response.status_code})')

            # Pause 1.7 secs before the next api call
            # to prevent 'ddos' to their server
            time.sleep(1.7)

        attempt_count += 1

    # Don't be scared, this block of code just for logging time
    fetch_finish = datetime.now(ZoneInfo('Asia/Kuala_Lumpur'))
    fetch_finish = int(fetch_finish.timestamp())  # number of seconds since epoch
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
