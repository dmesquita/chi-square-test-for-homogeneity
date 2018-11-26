import en_core_web_sm
import glob
import csv
import logging
from extraction_rules import InformationExtractor
import json
import urllib.request
import zipfile
from tqdm import tqdm

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', 
                    level=logging.INFO)

nlp = en_core_web_sm.load()
tsv_files = glob.glob("gitter-history-dfa9f2287cf20e04640646edab14e5a83a5fb0f1/archives/*.tsv")
data = []

if len(tsv_files) == 0:
    print('Beginning file download with urllib2...')
    url = 'https://github.com/freeCodeCamp/gitter-history/archive/dfa9f2287cf20e04640646edab14e5a83a5fb0f1.zip'  
    urllib.request.urlretrieve(url, 'data.zip')
    print('Unziping data...')
    zip_ref = zipfile.ZipFile('data.zip', 'r')
    zip_ref.extractall('./')
    zip_ref.close()
    tsv_files = glob.glob("gitter-history-dfa9f2287cf20e04640646edab14e5a83a5fb0f1/archives/*.tsv")

extractor = InformationExtractor(nlp)

for tsv in tqdm(tsv_files):
    with open(tsv, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        #logging.info("Reading: %s", tsv)
        for row in tqdm(reader):
            city = tsv.split("/")[-1]
            text_raw = row[6]
            text = nlp(text_raw)

            mentions = extractor.extract_mention(text, city)
            if len(mentions) == 0:
                mentions = [{"city":city, "rule":"MENTION","text":"Not found",
                            "message":text_raw, "sent_at": row[2]}]
            else:
                for item in mentions:
                    item.update({"message":text_raw})
                    item.update({"sent_at": row[2]})

            data.append(mentions)

with open('raw_data.json', 'w') as f:
    flat_list = [item for sublist in data for item in sublist]
    json.dump(flat_list, f)
