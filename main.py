import tweepy
import time
import logging
import requests
import json

all_keys = open('API Keys', 'r').read().splitlines()
api_key = all_keys[0]
api_key_secret = all_keys[1]
access_token = all_keys[2]
access_token_secret = all_keys[3]
bearer_token = all_keys[4]

client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)

api = tweepy.API(authenticator)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


def get_bit():
    url = " https://cryptingup.com/api/exchanges/BINANCE/markets"
    response = requests.get(url).json()

    with open('crypto.json', 'w') as json_file:
        json.dump(response, json_file, indent=4, sort_keys=True)


def open_bit(base):
    price = ''
    f = open('crypto.json')
    data = json.load(f)

    for i in data['markets']:
        if i['base_asset'] == base:
            price = str(i['base_asset']), "Price: " + str(i['price']), \
                    "Updated at: " + str(i['updated_at']), "Change in 24hrs: " + str(i['change_24h']),\
                    str(i['exchange_id'])

            message = "Your search resulted in " + str(price) + " @{}"
            return message
    f.close()
    print(price)


def respond_to_tweet():
    mention_id = 1
    while True:
        mentions = api.mentions_timeline(since_id=mention_id)
        for mention in mentions:
            print("Mention Tweet Found")
            print(f"{mention.author.screen_name} - {mention.text}")
            mention_id = mention.id
            get_bit()
            value = mention.text.upper().split()
            if len(value) > 1:
                string = open_bit(value[1])
            else:
                string = "not valid search was inputted @{}"
            if mention.in_reply_to_status_id is None:
                try:
                    print("Liking tweet")
                    api.create_favorite(mention.id)
                    print("Tweet has been liked!")
                    print("Retweeting..")
                    api.retweet(mention.id)
                    print("Retweeted")
                    print("Trying to reply...")
                    api.update_status(string.format(mention.author.screen_name),
                                      in_reply_to_status_id=mention.id_str)
                    print("Successfully replied :)")
                except Exception as exc:
                    print(exc)
        time.sleep(15)


if __name__ == "__main__":  # pulls api info to get bitcoin information.
    respond_to_tweet()
