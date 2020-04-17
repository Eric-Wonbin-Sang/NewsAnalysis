import datetime
import json

import Guardian

from General import Functions


def get_day_list(article_folder_path):

    for json_path in Functions.get_path_list_from_directory(article_folder_path):
        print(json_path)
        # with open(json_path) as json_file:
        #     data = json.load(json_file)
        #     print(data[:100])


def main():

    article_folder_path = "Day JSON Folder"

    do_download = False
    if do_download:
        Guardian.get_articles(
            folder_path=article_folder_path,
            start_date=datetime.date(2019, 10, 1),
            end_date=datetime.date(2020, 4, 10)
        )

    day_list = get_day_list(article_folder_path=article_folder_path)


main()
