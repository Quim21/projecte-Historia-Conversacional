# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Tarja(Objecte):
    """Tarja d'accés: obre les portes automàtiques de la nau."""

    def __init__(self):
        super().__init__("tarja", "Una tarja d'accés de la tripulació.")

    def usar(self, objectiu=None):
        return "No cal fer-la servir: les portes automàtiques s'obren si portes la tarja."
