import datetime

import Guardian
from Day import Day

from General import Functions


def get_day_list(article_folder_path):
    day_list = []
    for json_path in Functions.get_path_list_from_directory(article_folder_path):
        day_list.append(Day(json_path))
        print(day_list[-1])
    return day_list


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
