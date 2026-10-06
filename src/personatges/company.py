from personatges.personatge import Personatge


class Company(Personatge):
    def __init__(self, zona_actual, despert=False):
        super().__init__(zona_actual)
        self.despert = despert
