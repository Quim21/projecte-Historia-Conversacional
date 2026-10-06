import contextlib
import io
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from joc import classeJoc


def nova_partida():
    joc = classeJoc()
    with contextlib.redirect_stdout(io.StringIO()):
        joc.iniciar()
    return joc


def executa(joc, ordre):
    sortida = io.StringIO()
    with contextlib.redirect_stdout(sortida):
        joc.jugarTorn(ordre)
    return sortida.getvalue()


def torn_inofensiu(joc):
    with patch("builtins.input", return_value="9"):
        return executa(joc, "parlar")


def finalitza(joc, atacAbans=False):
    sortida = io.StringIO()
    with contextlib.redirect_stdout(sortida):
        joc.finalitzarTorn(atacAbans)
    return sortida.getvalue()


def primera_opcio(llista):
    return llista[0]


def zona_anomenada(nom):
    def triar(llista):
        return next(zona for zona in llista if zona.nom == nom)
    return triar
