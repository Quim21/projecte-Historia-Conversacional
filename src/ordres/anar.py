from excepcions.errors import AccioImpossible, MovimentInvalid


def anar(jugador, zones, nom_desti, ihall=None):
    sortida = _buscar_sortida(jugador.zona_actual, nom_desti)
    zona_desti = _buscar_zona(zones, sortida.zonaDesti, nom_desti)

    if sortida.necessitaVestit and not _porta_vestit(jugador):
        raise AccioImpossible("Sense el vestit espacial posat no sobreviuràs a l'exterior de la nau.")

    missatge = None
    if sortida.necessitaTarja:
        obre, missatge = _obrir_porta(jugador, ihall)
        if not obre:
            return None, missatge

    jugador.moure(zona_desti)
    return zona_desti, missatge


def _buscar_sortida(zona, nom_desti):
    for sortida in zona.sortides:
        if sortida.zonaDesti.lower() == nom_desti.lower():
            return sortida
    raise MovimentInvalid(nom_desti)


def _buscar_zona(zones, nom, nom_desti):
    for zona in zones:
        if zona.nom.lower() == nom.lower():
            return zona
    raise MovimentInvalid(nom_desti)


def _porta_vestit(jugador):
    return any(objecte.nom == "vestit" and objecte.equipat for objecte in jugador.inventari)


def _obrir_porta(jugador, ihall):
    targes = [objecte for objecte in jugador.inventari if hasattr(objecte, "del_company")]
    targes.sort(key=lambda tarja: tarja.del_company)
    if targes:
        return True, targes[0].usar()
    if ihall is None:
        return False, "La porta no s'obre sense la tarja."
    obre, missatge = ihall.obrir_porta()
    if not obre:
        missatge += "\n(Torna-ho a provar o busca la teva tarja.)"
    return obre, missatge
