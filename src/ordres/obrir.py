from excepcions.errors import AccioImpossible
from ordres.cerca import buscar_objecte


def obrir(jugador, zona, nom_objecte):
    objecte = buscar_objecte(jugador, zona, nom_objecte)
    if not hasattr(objecte, "obrir"):
        raise AccioImpossible(f"No pots obrir '{objecte.nom}'.")
    return objecte.obrir()
