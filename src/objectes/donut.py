# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Donut(Objecte):
    """Dònut que el jugador es pot menjar."""

    def __init__(self):
        super().__init__("donut", "Un dònut de xocolata acabat de fer.")
        self.menjat = False

    def usar(self, objectiu=None):
        if self.menjat:
            return "Ja te l'has menjat."
        self.menjat = True
        return "Et menges el dònut. Boníssim!"
