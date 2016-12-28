""" This file groups everything related to database """
import sqlite3, sys


bdd = sqlite3.connect("base.sq3")
cur = bdd.cursor()

def create_sale(id,title,price,date,url,img,search_id):
    """ Adds a sale in the db """
    cur.execute("""INSERT INTO sales (id,title,price,date,url,img,search_id) VALUES (?,?,?,?,?,?,?)""",
                (id,title,price,date,url,img,search_id,))
    bdd.commit()

def create_search(url="",name="",interval=0,last_save_id=0,owner=""):
    """ Adds a sale in the db """
    cur.execute("""INSERT INTO search (url,name,interval,last_save_id,owner) VALUES (?,?,?,?,?)""",
                (url,name,interval,last_save_id,owner))
    print('Nouvelle recherche active :  ' + name + " pour " + owner)
    bdd.commit()

def get_search_contents(id):
    """ gets search contents """
    cur.execute("""SELECT * FROM search WHERE id=?""", (id,))
    search = cur.fetchone()
    bdd.commit()
    return search

def get_active_searches():
    """ returns all active searches """
    cur.execute("""SELECT id, url, name FROM search WHERE active='1'""")
    request = cur.fetchall()
    bdd.commit()
    return request

def delete_sale(id):
    """ Delete the sale corresponding to this id """
    cur.execute("""DELETE FROM sales WHERE id=?""",(id,))
    print('Annonce ' + str(id) + ' supprimée')
    bdd.commit()

def delete_search(id):
    """ Delete the sale corresponding to this id """
    cur.execute("""SELECT id,search_id FROM sales WHERE search_id=?""", (id,))
    sales = cur.fetchall()
    for sale in sales:
        delete_sale(sale[0])
    #cur.execute("""DELETE FROM search WHERE id=?""",(id,))
    print('Recherche ' + str(id) + ' supprimée')
    bdd.commit()

def edit_search(id,url="",name="",interval=0,last_save_id=0,owner=""):
    """ Modify a preexisting search """
    cur.execute("""SELECT * FROM search WHERE id=?""", (id,))
    search = cur.fetchone()
    request = ({'url': search[1], 'name': search[2], 'interval': search[3], 'last_save_id': search[4],
                'owner': search[5]})

    if url != "":
        request['url'] = url
    if name != "":
        request['name'] = name
    if interval != 0:
        request['interval'] = interval
    if last_save_id != 0:
        request['last_save_id'] = last_save_id
    if owner != "":
        request['owner'] = owner

    cur.execute("""UPDATE search SET url=?, name=?, interval=?, last_save_id=?, owner=? WHERE id=?""",
                (request['url'], request['name'], request['interval'], request['last_save_id'],
                 request['owner'], id,))
    bdd.commit()

def publish_sale(id):
    """ Marks a sale as published """
    cur.execute("""UPDATE sales SET published='1' WHERE id=?""", (id,))
    bdd.commit()

def get_unpublished_sales():
    """ Get all the unpublished sales and return their ids """
    cur.execute("""SELECT * FROM sales WHERE published='0'""")
    request = cur.fetchall()
    bdd.commit()
    return request

def exists(id):
    """ returns yes if the sale exists or no if not """
    cur.execute("""SELECT id FROM sales WHERE id=?""",(id,))
    if len(cur.fetchall()) == 0:
        response = "yes"
    else:
        response = "no"
    return response

def update_last_id(search_id,last_id):
    """ For each active search, update last_id """
    cur.execute("""UPDATE search SET last_save_id=? WHERE id=?""",(last_id, search_id,))
    bdd.commit()
    pass

def main():
    """ For local testing """

if __name__ == '__main__':
    sys.exit(main())