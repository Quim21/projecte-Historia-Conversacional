from excepcions.errors import AccioImpossible
from ordres.agafar import agafar
from ordres.apagar import apagar
from ordres.deixar import deixar
from ordres.encendre import encendre
from ordres.obrir import obrir
from ordres.tancar import tancar

VERBS_OBJECTE = {
    "AGAFAR": agafar,
    "DEIXAR": deixar,
    "ENCENDRE": encendre,
    "APAGAR": apagar,
    "OBRIR": obrir,
    "TANCAR": tancar,
}


def executar(verb, jugador, objectiu):
    if objectiu is None:
        raise AccioImpossible(f"Què vols {verb.lower()}?")
    return VERBS_OBJECTE[verb](jugador, jugador.zona_actual, objectiu)
