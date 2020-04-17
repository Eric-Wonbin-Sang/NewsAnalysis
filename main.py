import os
import requests
import json
import datetime

from General import Constants


ARTICLES_DIR = os.path.join('Day JSON Folder')
os.makedirs(ARTICLES_DIR, exist_ok=True)

API_ENDPOINT = 'http://content.guardianapis.com/search'
api_params = {
    'from-date': None,      # will be added during for loop
    'to-date': None,        # will be added during for loop
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'api-key': Constants.guardian_api_key_path
}

start_date = datetime.date(2019, 10, 1)
end_date = datetime.date(2020, 4, 15)

for day_count in range((end_date - start_date).days + 1):

    curr_datetime = start_date + datetime.timedelta(days=day_count)
    curr_date_str = curr_datetime.strftime('%Y-%m-%d')
    json_path = os.path.join(ARTICLES_DIR, curr_date_str + '.json')

    if not os.path.exists(json_path):

        print("{} - Downloading {}".format(day_count, curr_date_str))

        all_results = []
        api_params['from-date'] = curr_date_str
        api_params['to-date'] = curr_date_str

        current_page = 1
        total_pages = 1
        while current_page <= total_pages:

            print("\t\tpage", current_page)
            api_params['page'] = current_page
            resp = requests.get(API_ENDPOINT, api_params)
            data = resp.json()
            all_results.extend(data['response']['results'])

            current_page += 1
            total_pages = data['response']['pages']

        with open(json_path, 'w') as f:
            print("\tWriting to", json_path)
            f.write(json.dumps(all_results, indent=2))
