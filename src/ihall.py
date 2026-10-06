import random


class iHall:
    def respondre(self, pregunta, resposta_correcta=None):
        if resposta_correcta is None:
            return "No ho sé, no tinc informació sobre això."
        if random.random() < 0.5:
            return resposta_correcta
        return "No ho sé, prova-ho a un altre lloc."
