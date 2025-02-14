
from src.utilities.DataBaseUtility import DataBaseUtility

class Del:
    def __init__(self):
        self.text = DataBaseUtility().extract_web_content()

    def get_text(self):
        return self.text

text = Del().get_text()
# Convert each tuple to a list
list_of_lists = [list(tup) for tup in text]
flattened_list = [item for sublist in list_of_lists for item in sublist]
print(list_of_lists)
print(flattened_list)
print(len(flattened_list))



