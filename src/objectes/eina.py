# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Eina(Objecte):
    def __init__(self):
        super().__init__("eina", "Una eina especial per reparar els motors.")
        self.utilitzat = False

    def usar(self, objectiu=None):
        if objectiu is None:
            return "Amb què vols fer servir l'eina?"
        if objectiu.lower() == "propulsors":
            self.utilitzat = True
            return "Repares els propulsors amb l'eina."
        if objectiu.lower() == "malien":
            # El joc ha de comptar 7 moviments i acabar la partida
            return ("Ataques en Malien amb l'eina, però se't cola per la gola! "
                    "D'aquí a 7 moviments un nou Malien petit sortirà del teu estómac.")
        return f"No pots fer servir {self.nom} així."
