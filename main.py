import datetime

import Guardian


def main():

    article_folder_path = "Day JSON Folder"

    Guardian.get_articles(
        folder_path=article_folder_path,
        start_date=datetime.date(2019, 10, 1),
        end_date=datetime.date(2020, 4, 10)
    )


main()
