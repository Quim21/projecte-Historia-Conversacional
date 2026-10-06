from excepcions.errors import AccioImpossible
from ordres.cerca import buscar_objecte


def encendre(jugador, zona, nom_objecte):
    objecte = buscar_objecte(jugador, zona, nom_objecte)
    if not hasattr(objecte, "encendre"):
        raise AccioImpossible(f"No pots encendre '{objecte.nom}'.")
    return objecte.encendre()
