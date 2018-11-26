import en_core_web_sm
import logging
import time
import json
from pprint import pprint
from tqdm import tqdm

nlp = en_core_web_sm.load()
metadata = "raw_data.json"
data = []
seen_messages = []

with open(metadata, "r") as f:
    json_data = json.load(f)
    for item in tqdm(json_data):
        if item["message"] not in seen_messages:
            seen_messages.append(item["message"])
            new_item = {}
            new_item["message"] = item["message"]
            new_item["city"] = item["city"]
            new_item["sent_at"] = item["sent_at"]
            new_item["city"] = item["city"].split(".tsv")[0]

        if item["text"] == "Not found":
            new_item["mention"] = "NO"
        else:
            new_item["mention"] = "YES"

        data.append(new_item)

with open('mentions_data.json', 'w') as f:
    pprint(data)
    json.dump(data, f)
