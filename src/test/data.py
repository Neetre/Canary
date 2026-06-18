'''
Module that handles requests to external APIs
'''

import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

WAQI_TOKEN = os.getenv("WAQI_KEY")

TS_stations = ["A77473", "@10046", "A374836", "A478045", "A359995", "A459208", "A497281"]

base_url="https://api.waqi.info/search/?keyword={}&token={}"
city = "trieste"
url = "https://api.waqi.info/feed/A77473/?token=8a45fdca4da4c360c409c7db4a53158428913441"

req = requests.get(url.format(city, WAQI_TOKEN))
if req.status_code == 200:
    data = req.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))
else:
    print(f"Request failed with status: {req.status_code}")