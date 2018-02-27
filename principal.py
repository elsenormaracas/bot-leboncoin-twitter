import time, schedule
from annonces import chercher_nouvelles_annonces
from twitter import ecouter_ordres


schedule.every(1).minutes.do(ecouter_ordres)
schedule.every(1).minutes.do(chercher_nouvelles_annonces)

while True:
    schedule.run_pending()
    time.sleep(1)
