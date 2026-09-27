from excepcions.errors import MovimentInvalid


def anar(jugador, zones, nom_desti):
    sortida = None
    for s in jugador.zona_actual.sortides:
        if s.zonaDesti.lower() == nom_desti.lower():
            sortida = s
            break

    if sortida is None:
        raise MovimentInvalid(nom_desti)

    zona_desti = None
    for zona in zones:
        if zona.nom.lower() == sortida.zonaDesti.lower():
            zona_desti = zona
            break

    if zona_desti is None:
        raise MovimentInvalid(nom_desti)

    jugador.moure(zona_desti)
    return zona_desti
