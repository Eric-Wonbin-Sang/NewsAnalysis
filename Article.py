
class Article:

    def __init__(self, data_dict):

        self.data_dict = data_dict

        self.date = self.get_date
        self.title = self.get_title
        self.text = self.get_text()

    def get_date(self):
        return None

    def get_title(self):
        return None

    def get_text(self):
        return None

    def __str__(self):
        ret_str = "Date: {} \tTitle: {}".format(self.date, self.title) + "\n\t"
        ret_str += "Text: {}{}".format(self.text[:20], "...") + "\t"
        return ret_str
