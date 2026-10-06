from excepcions.errors import AccioImpossible, ObjecteNoPortable, ObjecteNoTrobat


def agafar(jugador, zona, nom_objecte):
    objecte = _buscar_a_la_zona(zona, nom_objecte)

    if objecte is None:
        objecte = _treure_d_un_calaix(zona, nom_objecte)
        if objecte is None:
            raise ObjecteNoTrobat(nom_objecte)
    else:
        if not objecte.portable:
            raise ObjecteNoPortable(objecte.nom)
        _comprovar_llum(jugador, objecte)
        zona.objectes.remove(objecte)

    jugador.inventari.append(objecte)
    return f"Agafes {objecte.nom}."


def _buscar_a_la_zona(zona, nom_objecte):
    for objecte in zona.objectes:
        if objecte.nom.lower() == nom_objecte.lower():
            return objecte
    return None


def _treure_d_un_calaix(zona, nom_objecte):
    for objecte in zona.objectes:
        if hasattr(objecte, "treure") and hasattr(objecte, "contingut"):
            try:
                return objecte.treure(nom_objecte)
            except ObjecteNoTrobat:
                continue
    return None


def _comprovar_llum(jugador, objecte):
    if objecte.nom.lower() != "eina":
        return
    for item in jugador.inventari:
        if item.nom.lower() == "llanterna" and item.encesa:
            return
    raise AccioImpossible("Està massa fosc per trobar l'eina. Necessites la llanterna encesa.")
