from objectes.objecte import Objecte


class Estri(Objecte):
    def __init__(self, nom, descripcio, missatge, portable=True):
        super().__init__(nom, descripcio, portable)
        self.missatge = missatge

    def usar(self, objectiu=None):
        return self.missatge
