class OrdreInvalida(Exception):
    def __init__(self, text):
        super().__init__(f"Ordre no reconeguda: {text}")
        self.text = text


class MovimentInvalid(Exception):
    def __init__(self, nom_desti):
        super().__init__(f"No es pot anar a '{nom_desti}' des d'aquí")
        self.nom_desti = nom_desti
