# Quim Pérez / Pol Moyano

from excepcions.errors import ObjecteNoTrobat
from objectes.objecte import Objecte


class Calaix(Objecte):
    def __init__(self, contingut=None):
        super().__init__("calaix", "Un calaix d'un escriptori.", portable=False)
        self.obert = False
        self.contingut = contingut if contingut is not None else []

    def obrir(self):
        if self.obert:
            return "El calaix ja està obert."
        self.obert = True
        if self.contingut:
            noms = ", ".join(objecte.nom for objecte in self.contingut)
            return f"Obres el calaix. Hi ha: {noms}"
        return "Obres el calaix. Està buit."

    def tancar(self):
        if not self.obert:
            return "El calaix ja està tancat."
        self.obert = False
        return "Tanques el calaix."

    def treure(self, nom):
        if self.obert:
            for objecte in self.contingut:
                if objecte.nom.lower() == nom.lower():
                    self.contingut.remove(objecte)
                    return objecte
        raise ObjecteNoTrobat(nom)

    def usar(self, objectiu=None):
        return self.tancar() if self.obert else self.obrir()
