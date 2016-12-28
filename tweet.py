""" This file groups everything related to Twitter """
import tweepy, requests, os, sys
from bdd import get_search_contents
from twitter_connect import *

def create_tweet(link):
    """ Format the final tweet message using an array """
    search = get_search_contents(link[6])
    url = link[4][:-7]
    tweet = (link[1]
             + "\n" + link[2] + "€\n" + url
             + "\n@" + str(search[5])
             +"\nRecherche: " + str(search[2]))
    return (tweet[:140])

def send_tweet(img,message):
    """ Send a tweet with an image """
    api = connect_twitter()
    if img == "no-image": #If no image we send the no-picture.png
        api.update_with_media('no-picture.png', status=message)
    else: #Tweepy needs the image to be local and doesn't use the url.
        filename = 'temp.jpg'
        request = requests.get(img, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            api.update_with_media(filename, status=message)
            os.remove(filename)
        else:
            api.update_with_media('no-picture.png', status=message)

def get_orders(user):
    """ Listens to a stream of tweets adressed to an user """

    pass

def main():
    """ For local testing """


if __name__ == '__main__':
    sys.exit(main())