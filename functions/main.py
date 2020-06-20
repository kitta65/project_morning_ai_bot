from requests_oauthlib import OAuth1Session
import config
import datetime
import json
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage

#===== common =====
class MyException(Exception):
    pass

def make_sess():
    ck=config.CONSUMER_KEY
    cs=config.CONSUMER_SECCRET
    at=config.ACCESS_TOKEN
    ats=config.ACCESS_TOKEN_SECRET
    sess=OAuth1Session(ck, cs, at, ats)
    return sess

# https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search
def search_tweets(sess, env_label, query, from_jst=None, to_jst=None):
    url = f"https://api.twitter.com/1.1/tweets/search/30day/{env_label}.json"
    time_diff = datetime.timedelta(hours=9)
    if from_jst is not None:
        from_jst_parsed = datetime.datetime.strptime(from_jst, "%Y%m%d%H%M")
        from_utc = (from_jst_parsed - time_diff).strftime("%Y%m%d%H%M")
    else:
        from_utc = (datetime.datetime.now() - datetime.timedelta(hours=10)).strftime("%Y%m%d%H%M")
    if to_jst is not None:
        to_jst_parsed = datetime.datetime.strptime(to_jst, "%Y%m%d%H%M")
        to_utc = (to_jst_parsed - time_diff).strftime("%Y%m%d%H%M")
    else:
        to_utc = datetime.datetime.now().strftime("%Y%m%d%H%M")
    params = {
        "query": query,
        "maxResults": 100,
        "fromDate": from_utc, # UTC
        "toDate": to_utc, # UTC
    }
    res = sess.get(url, params=params)
    res_json = json.loads(res.text)
    try:
        tweet_id = res_json["results"][0]["id_str"]
        # results is automatically sorted in reverse chronological order
        tweet_url = f"https://twitter.com/aichan_nel/status/{tweet_id}"
    except (IndexError, KeyError) as e:
        raise MyException("couldn't find any tweets\n{}".format(res.text))
    return tweet_url

def send_message(message):
    line_bot_api = LineBotApi(config.LINE_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text=message))

def morning_ai_bot(request):
    sess = make_sess()
    tweet_url = search_tweets(
        sess,
        "myenv",
        '#モーニングアイちゃん from:aichan_nel has:videos',
        #"202006140600",
        #"202006140900",
    )
    send_message(tweet_url)

#res = search_tweets(
#    make_sess(), "myenv", "#モーニングアイちゃん from:aichan_nel has:videos",
#    "202006200000",
#    "202006200900"
#)
