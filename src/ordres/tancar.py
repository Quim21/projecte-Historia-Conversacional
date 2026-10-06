from excepcions.errors import AccioImpossible
from ordres.cerca import buscar_objecte


def tancar(jugador, zona, nom_objecte):
    objecte = buscar_objecte(jugador, zona, nom_objecte)
    if not hasattr(objecte, "tancar"):
        raise AccioImpossible(f"No pots tancar '{objecte.nom}'.")
    return objecte.tancar()
