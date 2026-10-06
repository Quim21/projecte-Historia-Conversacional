class JocError(Exception):
    pass


class OrdreInvalida(JocError):
    def __init__(self, text):
        super().__init__(f"Ordre no reconeguda: {text}")
        self.text = text


class MovimentInvalid(JocError):
    def __init__(self, nom_desti):
        super().__init__(f"No es pot anar a '{nom_desti}' des d'aquí")
        self.nom_desti = nom_desti


class ObjecteNoTrobat(JocError):
    def __init__(self, nom):
        super().__init__(f"No hi ha cap '{nom}' aquí")
        self.nom = nom


class ObjecteNoPortable(JocError):
    def __init__(self, nom):
        super().__init__(f"No pots agafar '{nom}'")
        self.nom = nom


class AccioImpossible(JocError):
    def __init__(self, missatge):
        super().__init__(missatge)
        self.missatge = missatge
