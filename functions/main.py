import config
import datetime
import json
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage

#===== common =====
class MyException(Exception):
    pass

# https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search
def search_tweets(token, env_label, query, from_jst=None, to_jst=None):
    url = f"https://api.twitter.com/1.1/tweets/search/30day/{env_label}.json"
    time_diff = datetime.timedelta(hours=9)
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "query": query,
        "maxResults": 100,
    }
    if from_jst is not None:
        from_jst_parsed = datetime.datetime.strptime(from_jst, "%Y%m%d%H%M")
        from_utc = (from_jst_parsed - time_diff).strftime("%Y%m%d%H%M")
    else:
        from_utc = (datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y%m%d%H%M")
    payload["fromDate"] = from_utc
    if to_jst is not None:
        to_jst_parsed = datetime.datetime.strptime(to_jst, "%Y%m%d%H%M")
        to_utc = (to_jst_parsed - time_diff).strftime("%Y%m%d%H%M")
        payload["toDate"] = to_utc
    res = requests.get(url, headers=headers, params=payload)
    res_json = json.loads(res.text)
    try:
        tweet_id = res_json["results"][0]["id_str"]
        # results is automatically sorted in reverse chronological order
        tweet_url = f"https://twitter.com/aichan_nel/status/{tweet_id}"
    except (IndexError, KeyError) as e:
        raise MyException(f"couldn't find any tweets\n{res.text}")
    return tweet_url

def send_message(message):
    line_bot_api = LineBotApi(config.LINE_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text=message))

def morning_ai_bot(request):
    tweet_url = search_tweets(
        config.TWITTER_TOKEN,
        "myenv",
        '#モーニングアイちゃん from:aichan_nel has:videos',
        #"202006140600",
        #"202006140900",
    )
    send_message(tweet_url)

