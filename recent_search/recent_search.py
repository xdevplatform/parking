import pandas as pd
import yaml
import json
import requests

from twilio_connect import twilio_connect, send_message

handle = "NYCASP"
url = "https://api.twitter.com/labs/2/tweets/search?query=from:{}".format(handle)
print(url)

with open("secret_demo.yaml") as file:
    data = yaml.safe_load(file)

bearer_token = data["search_tweets_api"]["bearer_token"]

headers = {"Authorization": "Bearer {}".format(bearer_token)}

response = requests.request("GET", url, headers=headers)
print(response.text)

if response.encoding is None:
    response.encoding = "utf-8"
for d in response.iter_lines(decode_unicode=True):
    if d:
        jdata = json.loads(d)

print(jdata)

data_jd = jdata["data"]
print(data_jd)

df = pd.DataFrame(data_jd)

client = twilio_connect()

if "suspended" in df["text"].values[0]:
    if "tomorrow" in df["text"].values[0]:
        send_message(client=client)
        print("text sent")
    else:
        print("not today, friend")
else:
    print("not today, friend")
