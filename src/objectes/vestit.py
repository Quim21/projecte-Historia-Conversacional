# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Vestit(Objecte):
    def __init__(self):
        super().__init__("vestit", "El vestit d'astronauta.")
        self.equipat = False

    def posar(self):
        if self.equipat:
            return "Ja portes el vestit posat."
        self.equipat = True
        return "Et poses el vestit d'astronauta."

    def treure(self):
        if not self.equipat:
            return "No portes el vestit posat."
        self.equipat = False
        return "Et treus el vestit d'astronauta."

    def usar(self, objectiu=None):
        return self.treure() if self.equipat else self.posar()
