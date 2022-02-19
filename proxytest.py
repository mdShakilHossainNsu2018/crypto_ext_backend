import requests

import random

res = requests.get("https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc")

res_json = res.json()["data"]

ren_obj = res_json[random.randint(0, len(res_json))]

proxy = ren_obj["ip"] + ":" + ren_obj["port"]

api_key = "59ee27c6-decc-43d6-9927-cde5d99a58b7"
api_endpoint = "https://api.blocknative.com/gasprices/blockprices?confidenceLevels=10&confidenceLevels=30" \
                   "&confidenceLevels=50&confidenceLevels=70&confidenceLevels=90 "
r = requests.get(api_endpoint, headers={'Authorization': api_key})

print(r.json())

