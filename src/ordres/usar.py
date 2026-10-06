from excepcions.errors import AccioImpossible
from ordres.cerca import buscar_objecte

ALIES_MALIEN = ("malien", "gonzalin")
CONNECTORS = ("amb", "a", "al", "en", "sobre", "contra")


def separar(text):
    parts = text.split()
    if not parts:
        return None, None
    nom_objecte = parts[0]
    resta = parts[1:]
    while resta and resta[0].lower() in CONNECTORS:
        resta.pop(0)
    nom_objectiu = " ".join(resta) if resta else None
    return nom_objecte, nom_objectiu


def usar(joc, text):
    if text is None or not text.strip():
        raise AccioImpossible("Què vols fer servir?")

    nom_objecte, nom_objectiu = separar(text)
    jugador = joc.jugador
    zona = jugador.zona_actual

    objecte = buscar_objecte(jugador, zona, nom_objecte)
    if objecte.portable and objecte not in jugador.inventari:
        raise AccioImpossible(f"Primer has d'agafar '{objecte.nom}'.")

    if nom_objectiu is None:
        return objecte.usar(None)

    clau, objectiu = _resoldre_objectiu(joc, zona, nom_objectiu)
    menjat_abans = getattr(objecte, "menjat", None)
    missatge = objecte.usar(clau)
    return missatge + _efectes(joc, objecte, clau, objectiu, menjat_abans)


def _resoldre_objectiu(joc, zona, nom):
    nom = nom.lower()

    if nom in ALIES_MALIEN:
        if joc.malien.zona_actual is zona:
            return "malien", joc.malien
        raise AccioImpossible("En Malien no és aquí.")

    if nom == "company":
        if joc.company.zona_actual is zona:
            return "company", joc.company
        raise AccioImpossible("El teu company no és aquí.")

    for objecte in zona.objectes + joc.jugador.inventari:
        if objecte.nom.lower() == nom:
            return nom, objecte

    raise AccioImpossible(f"Aquí no hi ha cap '{nom}'.")


def _efectes(joc, objecte, clau, objectiu, menjat_abans):
    tipus = type(objecte).__name__

    if tipus == "Eina" and clau == "propulsors":
        return "\n" + objectiu.reparar()

    if tipus == "Eina" and clau == "malien":
        joc.iniciarAtac()

    if tipus == "Donut" and clau == "malien" and menjat_abans is False and objecte.menjat:
        joc.malien.distret = True

    return ""
