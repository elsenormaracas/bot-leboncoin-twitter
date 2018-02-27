""" This file groups everything related to database """
import sqlite3, sys


bdd = sqlite3.connect("base.sq3")
cur = bdd.cursor()

def create_sale(id,title,price,date,url,img,search_id):
    """ Adds a sale in the db """
    cur.execute("""INSERT INTO sales (id,title,price,date,url,img,search_id) VALUES (?,?,?,?,?,?,?)""",
                (id,title,price,date,url,img,search_id,))
    bdd.commit()

def create_search(url="",name="",owner=""):
    """ Adds a sale in the db """
    cur.execute("""INSERT INTO search (url,name,owner) VALUES (?,?,?)""",
                (url,name,owner))
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

def sale_exists(id):
    """ returns yes if the sale exists or no if not """
    cur.execute("""SELECT id FROM sales WHERE id=?""",(id,))
    if len(cur.fetchall()) == 0:
        response = True
    else:
        response = False
    return response

def search_exists(id):
    """ returns yes if the search exists or no if not """
    cur.execute("""SELECT id FROM search WHERE id=?""",(id,))
    if len(cur.fetchall()) == 0:
        response = True
    else:
        response = False
    return response

def is_owner(id,owner):
    """ returns yes if owner is the owner of the search """
    cur.execute("""SELECT id,owner FROM search WHERE id=? and owner=?""",(id,owner,))
    if len(cur.fetchall()) == 0:
        response = False
    else:
        response = True
    return response

def update_last_id(search_id,last_id):
    """ For each active search, update last_id """
    cur.execute("""UPDATE search SET last_save_id=? WHERE id=?""",(last_id, search_id,))
    bdd.commit()

def stop_search(search_id):
    """ Stop search"""
    cur.execute("""UPDATE search SET active=0 WHERE id=?""",(search_id,))
    bdd.commit()

def main():
    """ For local testing """

if __name__ == '__main__':
    sys.exit(main())