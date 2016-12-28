import tweepy
import time, schedule
from twitter_connect import *

import sqlite3

bdd = sqlite3.connect("base.sq3")
cur = bdd.cursor()

admin = "ElSenorMaracas"



def get_last_tweet():
    """ gets last tweet recorded """

    cur.execute("""SELECT id FROM tweets ORDER BY id DESC LIMIT 1""")
    id = cur.fetchone()
    bdd.commit()
    return id[0]

def record_tweet(id,text,action,sender,mention):
    """ Adds a sale in the db """
    cur.execute("""INSERT INTO tweets (id,text,action,sender,mention) VALUES (?,?,?,?,?)""",
                (id,text,action,sender,mention,))
    bdd.commit()

def extract_numbers(str):
    """ extracts all numbers in the tweet and return tuples """
    return [int(s) for s in str.split() if s.isdigit()]

def listen_orders():
    """ This is the main function, it reads the tweets sent to the timeline and executes orders """
    last = get_last_tweet()
    timeline = api.home_timeline(since_id=last, count=10)
    for status in timeline:

        tweet_id = status.id
        text = status.text
        sender = status.user.screen_name
        mention = ''
        action = ''
        object = extract_numbers(text)

        for entity in status.entities['user_mentions']:
            if entity['screen_name'] not in ('ElSenorMaracas', 'botleboncoin'):
                mention = entity['screen_name']

        if 'recherche' in text and 'autoris' not in text:
            if 'quel' in text:
                action = "lister recherche"
                pass
            if 'efface' in text:
                action = "effacer recherche"
                pass
            if 'arret' in text:
                action = "arreter recherche"
                pass
            if 'repr' in text:
                action = "reprendre recherche"
                pass
            if 'cree' in text:
                action = "creer recherche"
                pass

        if 'autoris' in text:
            action = "autoriser"
            pass
        #record_tweet(tweet_id,text,action,sender,mention,object)
        print("fait")

if __name__ == '__main__':

    print(extract_numbers("roger 4    59"))
    api = connect_twitter()
    """
    listen_orders()
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
"""