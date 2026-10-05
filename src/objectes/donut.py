# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Donut(Objecte):
    """Dònuts de la cuina: serveixen per despistar en Malien o en Gonzalin (el company).
    Si en Gonzalin els troba, se'ls menja i ja no es poden fer servir."""

    # Personatges que es poden despistar amb els dònuts
    DESPISTABLES = ("malien", "gonzalin")

    def __init__(self):
        super().__init__("donuts", "Uns dònuts.")
        self.menjat = False

    def menjar(self):
        # El crida en Gonzalin quan troba els dònuts
        self.menjat = True

    def usar(self, objectiu=None):
        if self.menjat:
            return "Ja no queden dònuts."
        if objectiu is None or objectiu.lower() not in self.DESPISTABLES:
            return f"No pots fer servir {self.nom} així."
        self.menjat = True
        return f"En {objectiu.capitalize()} es llança sobre els dònuts. Quedarà entretingut durant la resta de la partida."
