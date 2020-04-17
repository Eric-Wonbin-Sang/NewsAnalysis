import os
import requests
import json
import datetime

from General import Constants


def get_articles(folder_path, start_date, end_date):
    folder_path = create_json_folder_directory(folder_path)
    download_articles_to_path(
        folder_path=folder_path,
        start_date=start_date,
        end_date=end_date
    )


def create_json_folder_directory(folder_path):
    os.makedirs(os.path.join(folder_path), exist_ok=True)
    return folder_path


def download_articles_to_path(folder_path, start_date, end_date):

    api_endpoint = 'http://content.guardianapis.com/search'
    api_params = {
        'from-date': None,  # will be added during for loop
        'to-date': None,  # will be added during for loop
        'order-by': "newest",
        'show-fields': 'all',
        'page-size': 200,
        'api-key': Constants.guardian_api_key_path
    }

    for day_count in range((end_date - start_date).days + 1):

        curr_datetime = start_date + datetime.timedelta(days=day_count)
        curr_date_str = curr_datetime.strftime('%Y-%m-%d')
        json_path = os.path.join(folder_path, curr_date_str + '.json')

        if not os.path.exists(json_path):

            try:
                print("{} - Downloading {}".format(day_count, curr_date_str))

                all_results = []
                api_params['from-date'] = curr_date_str
                api_params['to-date'] = curr_date_str

                current_page = 1
                total_pages = 1
                while current_page <= total_pages:
                    print("\tpage", current_page)
                    api_params['page'] = current_page
                    resp = requests.get(api_endpoint, api_params)
                    data = resp.json()
                    all_results.extend(data['response']['results'])

                    current_page += 1
                    total_pages = data['response']['pages']

                with open(json_path, 'w') as f:
                    print("\tWriting to", json_path)
                    f.write(json.dumps(all_results, indent=2))
            except KeyError:
                print("\tDate: {} - No response given, Guardian API may be exhausted".format(curr_date_str))
