class annonce:

    def __init__(self, id, titre, prix, date, lien, img, recherche_id):
        self.id = id
        self.titre = titre
        self.prix = prix
        self.date = date
        self.lien = lien
        self.img = img
        self.recherche_id = recherche_id

    def get_id(self):
        return self.id
    def get_titre(self):
        return self.titre
    def get_prix(self):
        return self.prix
    def get_date(self):
        return self.date
    def get_lien(self):
        return self.lien
    def get_img(self):
        return self.img
    def get_recherche_id(self):
        return self.recherche_id