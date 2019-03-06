import datetime
import pandas as pd
from searchtweets import ResultStream, gen_rule_payload, load_credentials
from twilio_connect_demo import twilio_connect, send_message


premium_search_args = load_credentials(
    filename="secret_demo.yaml", yaml_key="search_tweets_api", env_overwrite=False
)

today = datetime.date.today()
print(today)

start_date = today + datetime.timedelta(-30)
print(start_date)

rule = gen_rule_payload(
    "from:NYCASP", from_date=str(start_date), to_date=str(today), results_per_call=500
)

print(rule)

rs = ResultStream(rule_payload=rule, max_results=500, **premium_search_args)

print(rs)

tweets = rs.stream()
list_tweets = list(tweets)
[print(tweet.all_text, end="\n\n") for tweet in list_tweets[0:100]]


tweet_text = []
tweet_date = []


for tweet in list_tweets:
    tweet_text.append(tweet["text"])
    tweet_date.append(tweet["created_at"])

df = pd.DataFrame({"tweet": tweet_text, "date": tweet_date})
df.head()

client = twilio_connect()

if "suspended" in df["tweet"].values[0]:
    if "tomorrow" in df["tweet"].values[0]:
        send_message(client=client)
        print("text sent")
    else:
        print("not today, friend")
else:
    print("not today, friend")
