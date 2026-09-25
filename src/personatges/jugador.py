from personatges.personatge import Personatge


class Jugador(Personatge):
    def __init__(self, zona_actual, inventari=None):
        super().__init__(zona_actual)
        self.inventari = inventari if inventari is not None else []
