import datetime
import json

from Article import Article

from General import Functions


class Day:

    def __init__(self, json_path):

        self.json_path = json_path

        self.date = self.get_date()
        self.article_list = self.get_article_list()
        self.article_count = len(self.article_list)

    def get_date(self):
        date_str = self.json_path.split("\\")[-1].split(".")[0]
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    def get_date_to_str(self):
        return self.date.strftime('%Y-%m-%d')

    def get_article_list(self):
        with open(self.json_path) as json_file:
            return [Article(self, data_dict) for data_dict in json.load(json_file)]

    def __str__(self):
        ret_str = "Date: {}".format(self.get_date_to_str()) + "\t"
        ret_str += "JSON Path: {}".format(self.json_path) + "\t"
        ret_str += "Article Count: {}".format(self.article_count)
        for i, article in enumerate(self.article_list):
            ret_str += "\n"
            ret_str += Functions.tab_str("Article {}: {}".format(i, str(article)))
        return ret_str
