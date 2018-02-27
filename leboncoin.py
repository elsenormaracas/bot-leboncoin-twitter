""" This script store new sales from leboncoin.fr.
Its arguments are the proximity and keyword and last search"""

import time, schedule
from bdd import *
from tweet import *
from bs4 import BeautifulSoup

def get_all_links(id,search_url):
    """ Parse the URL given in query and returns an array containing the last sale's info"""
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text,"html5lib")
    bloc = soup.select('a.list_item')
    link = []
    for b in bloc:
        try:
            save_id = b.select_one('div.saveAd').get('data-savead-id')
        except:
            save_id = '0'
        if save_id != '0' and sale_exists(save_id) == True:
            url = "https:"+b.get('href')
            if b.select_one('span.lazyload') is None:#This span doesn't exist if no image
                img = "no-image"
            else:
                img = "https:"+b.select_one('span.lazyload').get('data-imgsrc')
            title = b.get('title')
            try:
                price = b.select_one('h3.item_price').get('content')
            except:
                price = '0'

            date = time.strftime("%d/%m/%Y %H:%M:%S")
            link.append({'save_id':save_id, 'title':title, 'price':price, 'date':date,
                         'url':url, 'img':img, 'search_id':id})
    return link

def main():
    """executes when the script launches directly"""

    loop = True
    interval = 60
    # If loop == true this will execute itself every interval
    while loop == True:

        #1 Gets all active searches
        active_searches = get_active_searches()

        #2 Gets all new links in active searches and stores them in the sales table
        for search in active_searches:
            search_links = get_all_links(search[0],search[1])
            if search_links != []:
                for link in search_links:
                    create_sale(link['save_id'],link['title'],link['price'],link['date'],link['url'],link['img'],link['search_id'])
                    print("Créé : " + link['title'])
            else:
                print(time.strftime("%d/%m/%Y %H:%M:%S") + ' : Rien pour la recherche : ' + str(search[2]))

        #3 Gets all unpublished sales
        unpublished_sales = get_unpublished_sales()

        #4 Tweets all the unpublished sales and marks them as published
        for unpub in unpublished_sales:
            tweet = create_tweet(unpub)
            tweet_img = unpub[5]
            send_img_tweet(tweet_img, tweet)
            publish_sale(unpub[0])
            print('Envoyé tweet : '+ unpub[1])

        #5 Sleeps for a fixed period of time
        time.sleep(interval)

if __name__ == '__main__':
    sys.exit(main())