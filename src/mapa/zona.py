# Quim Pérez / Pol Moyano

class Zona:
    def __init__(self, nom, descripcio, objectes=None, sortides=None):
        self.nom = nom
        self.descripcio = descripcio
        self.objectes = objectes if objectes is not None else []
        self.sortides = sortides if sortides is not None else []

