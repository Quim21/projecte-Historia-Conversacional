# Quim Pérez / Pol Moyano

class Zona:
    def __init__(self, nom, descripcio, objectes=None, sortides=None):
        self.nom = nom
        self.descripcio = descripcio
        self.objectes = objectes if objectes is not None else []
        self.sortides = sortides if sortides is not None else []

    def descriure(self, ocults=None):
        text = f"{self.nom}\n{self.descripcio}"
        visibles = [objecte for objecte in self.objectes if ocults is None or objecte not in ocults]
        if visibles:
            noms = ", ".join(objecte.nom for objecte in visibles)
            text += f"\nObjectes: {noms}"
        return text
