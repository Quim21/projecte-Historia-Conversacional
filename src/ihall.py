import random

EXCUSES_PORTA = [
    "iHall: «Perdoni, capità, no l'he sentit bé. Torni-ho a provar.»",
    "iHall: «Aquesta porta està en manteniment.» (No sembla gaire cert.)",
    "iHall: «Primer digui 'si us plau', capità.»",
    "iHall: «Ara no puc, estic ocupat comptant estrelles.»",
]


class iHall:
    def respondre(self, pregunta, resposta_correcta=None, resposta_falsa=None):
        if resposta_correcta is None:
            return "No ho sé, no tinc informació sobre això."
        if random.random() < 0.5:
            return resposta_correcta
        if resposta_falsa is not None:
            return resposta_falsa
        return "No ho sé, prova-ho a un altre lloc."

    def obrir_porta(self):
        if random.random() < 0.5:
            return True, "iHall: «Aquesta vegada li obro la porta, capità.»"
        return False, random.choice(EXCUSES_PORTA)
