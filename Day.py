import datetime


class Day:

    def __init__(self, json_path):

        self.json_path = json_path

        self.date = self.get_date()
        self.article_list = self.get_article_list()

    def get_date(self):
        date_str = self.json_path.split("\\")[-1].split(".")[0]
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    def get_article_list(self):
        article_list = []

        return article_list

    def __str__(self):
        ret_str = "Date: " + self.date.strftime('%Y-%m-%d') + "\t"
        ret_str += "JSON Path: " + self.json_path
        return ret_str
