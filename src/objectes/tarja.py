# Quim Pérez / Pol Moyano

from objectes.objecte import Objecte


class Tarja(Objecte):

    def __init__(self, del_company=False):
        if del_company:
            super().__init__("tarja", "La tarja identificadora d'un company.")
        else:
            super().__init__("tarja", "La teva tarja identificadora.")
        self.del_company = del_company

    def usar(self, objectiu=None):
        if self.del_company:
            return "L'iHall obre la porta, però et recorda que aquesta no és la teva tarja."
        return "La porta s'obre automàticament."
