class OrdreInvalida(Exception):
    def __init__(self, text):
        super().__init__(f"Ordre no reconeguda: {text}")
        self.text = text
