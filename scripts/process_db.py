import json
import os
from zoneinfo import ZoneInfo
from datetime import datetime, timezone


def process_data(filename):
    """
    This function will read the given filename.
    It will parse the prayer time and convert into epoch timestamp
    """
    # extract month and year from filename
    target_file_name = filename.split(".")[0]
    month, year = target_file_name.split("-")

    # read json content in response.json file
    with open(f'outputs/{filename}') as f:
        raw_data = json.load(f)

    data = {}
    data['processed'] = []

    print('Processing data starting...')

    # iterate the zones
    for zone in raw_data["jakim"]:
        prayer_times_zone = []

        # iterate the prayerTime
        for item in zone["prayerTime"]:

            date = item["date"]
            day = date.split("-")[0]
            month = date.split("-")[1]
            year = date.split("-")[2]

            prayer_times_day = {
                "fajr": item["fajr"],
                "syuruk": item["syuruk"],
                "dhuhr": item["dhuhr"],
                "asr": item["asr"],
                "maghrib": item["maghrib"],
                "isha": item["isha"]
            }

            # parse prayer_times to datetime
            # TODO: Beware of JAKIM's month name convention
            # refer: https://github.com/mptwaktusolat/app_waktu_solat_malaysia/issues/103#issuecomment-1059596883
            for key, value in prayer_times_day.items():
                prayer_times_day[key] = datetime.strptime(
                    f"{year}-{month}-{day} {value}", "%Y-%b-%d %H:%M:%S")

            # convert datetime to epoch timestamp in Malaysia's timezone
            for key, value in prayer_times_day.items():
                prayer_times_day[key] = int(
                    value.replace(
                        tzinfo=ZoneInfo('Asia/Kuala_Lumpur')).timestamp())

            # Add day to prayer_times
            prayer_times_day["day"] = int(day)

            # Add back hijri date
            prayer_times_day["hijri"] = item["hijri"]

            # add the zone's prayer time to the list
            prayer_times_zone.append(prayer_times_day)

        # solat data
        solat_data = {"zone": zone["zone"], "prayerTime": prayer_times_zone}

        data['processed'].append(solat_data)
        print(f"Processed {zone['zone']}")

    # bring forward the last_fetched time
    data['last_fetched'] = raw_data['last_fetched']

    process_finish = datetime.now(ZoneInfo('Asia/Kuala_Lumpur'))
    process_finish = int(process_finish.timestamp())
    print(f'\n:white_check_mark: Process finish at {process_finish}')
    data['last_processed'] = process_finish

    # write to json file
    filename = f'outputs/{month}-{year}.processed.json'
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=2)
        print(f':white_check_mark: Finish writing to {filename}')

    print('\n')  # spare a new line


# iterate all files in outputs folder and process them
for file in os.listdir("../outputs"):
    if file.endswith(".json") and not file.endswith("processed.json"):
        process_data(file)
