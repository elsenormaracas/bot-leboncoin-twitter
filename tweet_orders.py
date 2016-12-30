import tweepy
import time, schedule
import re
from tweet import *
from bdd import *

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

def record_tweet(id,text,action,sender,mention,object):
    """ Adds a sale in the db """
    cur.execute("""INSERT INTO tweets (id,text,action,sender,mention,object) VALUES (?,?,?,?,?,?)""",
                (id,text,action,sender,mention,str(object),))
    bdd.commit()

def extract_numbers(str):
    """ extracts all numbers in the tweet and return tuples """
    return [int(s) for s in str.split() if s.isdigit()]



def listen_orders():
    """ This is the main function, it reads the tweets sent to the timeline and executes orders """
    last = get_last_tweet()
    timeline = api.home_timeline(since_id=last, count=10)
    for status in timeline:
        if status.user.screen_name != "botleboncoin":
            print(status.text)
            tweet_id = status.id
            text = status.text
            sender = status.user.screen_name
            owner = ''
            action = ''
            object = extract_numbers(text)
            answer = ''

            for entity in status.entities['user_mentions']:
                if entity['screen_name'] not in ('botleboncoin'):
                    owner = "@" + entity['screen_name']
            if owner == '':
                if "pour moi" in text:
                    owner = "@" + sender
                else:
                    owner = "@" + admin
            answer += "@" + owner + "\n"

            if 'recherche' in text:
                if 'liste' in text or 'quel' in text:
                    action = "lister recherche"
                    request = get_active_searches()
                    if request == []:
                        answer += "Pas de recherche en cours"
                    else:
                        answer +="Recherches en cours :"
                        for s in request:
                            answer += "\n" + str(s[0]) + " : " + s[2]
                    send_tweet(answer)
                if 'arret' in text or 'stop' in text or 'supprime' in text or 'efface' in text:
                    action = "arreter recherche"
                    if object != []:
                        answer = "Recherches arrêtées : \n"
                        for o in object:
                            if search_exists(o) == True:
                                if is_owner(o,owner) == True:
                                    stop_search(o)
                                    answer += str(o) + " : Ok"
                                else:
                                    answer += str(o) + " : Non (Pas votre recherche)"
                    else:
                        answer = "Je ne connais pas cette recherche, il me faut le numéro pas le nom"
                    send_tweet(answer)
                if 'cree' in text or 'crée' in text or 'demarr' in text or 'démarr' in text or 'nouvel' in text:
                    action = "creer recherche"
                    url=''
                    name=''
                    try:
                        url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                    except:
                        send_tweet(owner + " Il faut renseigner une URL")
                    else:
                        print(url)
                    try :
                        name = re.search(r'"([^"]*)"', text).group(0)[1:-1]
                    except:
                        send_tweet(owner + " Il faut mettre le nom de la recherche entre guillemets")
                    else:
                        print(name)
                    if url != '' and name != '':
                        create_search(url,name,owner)
                        send_tweet("Je crée la recherche \"" + name + "\" pour " + owner)
            print("\n")
            #record_tweet(tweet_id,text,action,sender,owner,object)

if __name__ == '__main__':

    api = connect_twitter()
    listen_orders()
    """
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
"""