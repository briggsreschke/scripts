# read csv with header and write to array of dicts 
import csv
import json

with open('read.csv') as f:
    a = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

with open('write.json', 'w') as fout:
    json.dump(a, fout)
