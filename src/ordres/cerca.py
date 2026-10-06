from excepcions.errors import ObjecteNoTrobat


def buscar_objecte(jugador, zona, nom_objecte):
    for objecte in jugador.inventari + zona.objectes:
        if objecte.nom.lower() == nom_objecte.lower():
            return objecte
    raise ObjecteNoTrobat(nom_objecte)
