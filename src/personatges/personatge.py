class Personatge:
    def __init__(self, zona_actual):
        self.zona_actual = zona_actual

    def moure(self, nova_zona):
        self.zona_actual = nova_zona
