from excepcions.errors import AccioImpossible
from ordres.cerca import buscar_objecte


def apagar(jugador, zona, nom_objecte):
    objecte = buscar_objecte(jugador, zona, nom_objecte)
    if not hasattr(objecte, "apagar"):
        raise AccioImpossible(f"No pots apagar '{objecte.nom}'.")
    return objecte.apagar()
