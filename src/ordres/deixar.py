from excepcions.errors import AccioImpossible


def deixar(jugador, zona, nom_objecte):
    for objecte in jugador.inventari:
        if objecte.nom.lower() == nom_objecte.lower():
            if getattr(objecte, "equipat", False):
                raise AccioImpossible("Primer t'has de treure el vestit.")
            jugador.inventari.remove(objecte)
            zona.objectes.append(objecte)
            return f"Deixes {objecte.nom}."
    raise AccioImpossible(f"No portes cap '{nom_objecte}'.")
