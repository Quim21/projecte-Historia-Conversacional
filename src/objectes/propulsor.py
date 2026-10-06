# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Propulsor(Objecte):

    def __init__(self):
        super().__init__("propulsors", "Els propulsors danyats per l'aeròlit.", portable=False)
        self.reparats = False

    def reparar(self):
        if self.reparats:
            return "Els propulsors ja estan reparats."
        self.reparats = True
        return "Els propulsors estan reparats. Torna a la sala de comandament per posar en marxa els motors."
