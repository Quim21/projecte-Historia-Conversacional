# Quim Pérez / Pol Moyano

class Objecte:
    def __init__(self, nom, descripcio, portable=True):
        self.nom = nom
        self.descripcio = descripcio
        self.portable = portable

    def usar(self, objectiu=None):
        return f"No pots fer servir {self.nom} així."
