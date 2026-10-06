# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Llanterna(Objecte):
    def __init__(self):
        super().__init__("llanterna", "Una llanterna.")
        self.encesa = False

    def encendre(self):
        if self.encesa:
            return "La llanterna ja està encesa."
        self.encesa = True
        return "Encens la llanterna."

    def apagar(self):
        if not self.encesa:
            return "La llanterna ja està apagada."
        self.encesa = False
        return "Apagues la llanterna."

    def usar(self, objectiu=None):
        return self.apagar() if self.encesa else self.encendre()
