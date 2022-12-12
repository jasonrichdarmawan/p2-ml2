import json

with open('./model/kinds_dict.txt', 'rt') as file_1:
    kinds_dict = json.load(file_1)
    kinds_dict = {int(k):v for k,v in kinds_dict.items()}

int_to_kinds = lambda items: [kinds_dict[item] for item in items]