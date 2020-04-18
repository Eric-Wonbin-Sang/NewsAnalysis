from General import Functions


class Topic:

    def __init__(self, name, keyword_list):

        self.name = name
        self.keyword_list = keyword_list
        self.day_freq_dict = {}
        self.article_list = []
        self.article_count = 0

    def update_day_freq_dict(self, day_list):
        for day in day_list:
            freq = 0
            for article in day.article_list:
                curr_freq = article.get_freq_of_keywords(self.keyword_list)
                if curr_freq != 0:
                    freq += curr_freq
                    self.article_list.append(article)
            self.day_freq_dict[day] = freq
        self.article_count = len(self.article_list)

    def __str__(self):
        ret_str = "name: {}".format(self.name) + "\t"
        ret_str += "article_count: {}".format(self.article_count) + "\t"
        ret_str += "keyword_list: {}".format(self.keyword_list)
        for i, article in enumerate(self.article_list):
            ret_str += "\n"
            ret_str += Functions.tab_str("Article {}: {}".format(i, str(article)))
        return ret_str
