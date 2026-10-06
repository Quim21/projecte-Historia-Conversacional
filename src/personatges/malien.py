from personatges.personatge import Personatge


class Malien(Personatge):
    def __init__(self, zona_actual, distret=False):
        super().__init__(zona_actual)
        self.distret = distret
