# Quim Pérez / Pol Moyano

import random

from ihall import iHall
from mapa.sortida import Sortida
from mapa.zona import Zona
from objectes.calaix import Calaix
from objectes.donut import Donut
from objectes.eina import Eina
from objectes.llanterna import Llanterna
from objectes.propulsor import Propulsor
from objectes.tarja import Tarja
from objectes.vestit import Vestit
from ordres.anar import anar
from ordres.despatx import VERBS_OBJECTE, executar
from ordres.interpret import interpretar
from personatges.jugador import Jugador


class classeJoc:
    def __init__(self):
        self.zones = []
        self.jugador = None
        self.ihall = iHall()
        self.torn = 0
        self.acabat = False

    def iniciar(self):
        self.crearMapa()
        self.jugador = Jugador(self.buscarZona("dormitori"))
        self.mostrarIntroduccio()
        print(self.descriureZona(self.jugador.zona_actual))

    def crearMapa(self):
        tallers = Zona("tallers", "Els tallers de la nau. Un fallo de llum ho ha deixat tot a les fosques.")
        oficines = Zona("oficines", "L'oficina principal. Hi ha escriptoris plens de papers.")
        vestuari = Zona("vestuari", "El vestuari de la tripulació. Hi ha taquilles i vestits penjats.")
        banys = Zona("banys", "Els banys de la nau. Una aixeta goteja sense parar.")
        comandament = Zona("comandament", "La sala de comandament. Des d'aquí es posen en marxa els motors.")
        cuina = Zona("cuina", "La cuina de la nau. Fa olor de dònuts acabats de fer.")
        dormitori = Zona("dormitori", "El dormitori. Les càpsules d'hivernació brillen amb llum blava.")
        menjador = Zona("menjador", "El menjador. Taules metàl·liques i cadires desordenades.")
        exterior = Zona("exterior", "La sala de sortida exterior. Una comporta dona a l'espai.")
        propulsors = Zona("propulsors", "L'exterior de la nau, al costat dels propulsors danyats.")

        # Portes automàtiques: necessiten tarja
        self.connectar(tallers, oficines, True)
        self.connectar(oficines, comandament, True)
        self.connectar(oficines, vestuari, True)
        self.connectar(oficines, banys, True)
        self.connectar(vestuari, cuina, True)
        self.connectar(banys, dormitori, True)
        self.connectar(comandament, menjador, True)
        self.connectar(menjador, cuina, True)
        self.connectar(menjador, dormitori, True)
        self.connectar(menjador, exterior, True)
        # La comporta a l'espai no necessita tarja
        self.connectar(exterior, propulsors, False)

        oficines.objectes.append(Calaix(contingut=[Tarja()]))
        vestuari.objectes.append(Vestit())
        cuina.objectes.append(Donut())
        tallers.objectes.append(Eina())
        propulsors.objectes.append(Propulsor())

        self.zones = [tallers, oficines, vestuari, banys, comandament,
                      cuina, dormitori, menjador, exterior, propulsors]

        zonesLlanterna = [zona for zona in self.zones if zona not in (exterior, propulsors)]
        random.choice(zonesLlanterna).objectes.append(Llanterna())

    def connectar(self, zonaA, zonaB, necessitaTarja):
        zonaA.sortides.append(Sortida(zonaB.nom, necessitaTarja))
        zonaB.sortides.append(Sortida(zonaA.nom, necessitaTarja))

    def buscarZona(self, nom):
        for zona in self.zones:
            if zona.nom == nom:
                return zona
        return None

    def mostrarIntroduccio(self):
        print("=" * 70)
        print("  Any 2120 D.C. La nau PiaXXII viatja cap al planeta SUMMEM.")
        print("  Un aeròlit ha danyat els propulsors. Repara'ls i torna a la sala")
        print("  de comandament per posar en marxa els motors.")
        print("  (Escriu 'ajuda' per veure les ordres)")
        print("=" * 70)

    def mostrarAjuda(self):
        print("Ordres disponibles:")
        print("  anar <zona>     Et mous a una zona del costat (ex: anar banys)")
        print("  agafar <obj>    Agafes un objecte de la zona")
        print("  encendre <obj>  Encens un objecte (ex: encendre llanterna)")
        print("  apagar <obj>    Apagues un objecte")
        print("  obrir <obj>     Obres un objecte (ex: obrir calaix)")
        print("  tancar <obj>    Tanques un objecte")
        print("  parlar          Fas una pregunta a iHall")
        print("  inventari       Mostra el que portes a sobre")
        print("  ajuda           Mostra aquesta ajuda")
        print("  sortir          Abandona la partida")

    def mostrarInventari(self):
        if not self.jugador.inventari:
            print("No portes res a sobre.")
            return
        print("Portes: " + ", ".join(objecte.nom for objecte in self.jugador.inventari))

    def descriureZona(self, zona):
        text = "\n" + zona.descriure()
        text += "\nSortides: " + ", ".join(s.zonaDesti for s in zona.sortides)
        return text

    def jugarTorn(self, ordre):
        # Ordres de control de la partida, no són accions del joc
        control = ordre.strip().lower()
        if control == "ajuda":
            self.mostrarAjuda()
            return
        if control == "inventari":
            self.mostrarInventari()
            return
        if control == "sortir":
            print(f"Abandones la partida després de {self.torn} torns.")
            self.acabat = True
            return

        # Si l'ordre no és vàlida, l'excepció la recull el main i no es compta el torn
        verb, objectiu = interpretar(ordre)

        if verb == "ANAR":
            if not self.moureJugador(objectiu):
                return
        elif verb == "PARLAR":
            print(self.parlar())
        elif verb in VERBS_OBJECTE:
            print(executar(verb, self.jugador, objectiu))
        else:
            print(f"Encara no sé fer l'acció {verb}.")
            return

        self.torn += 1

    def moureJugador(self, nomDesti):
        if nomDesti is None:
            print("On vols anar?")
            return False

        zonaDesti = anar(self.jugador, self.zones, nomDesti)
        print(self.descriureZona(zonaDesti))
        return True

    def trobarZonaObjecte(self, nomObjecte):
        for zona in self.zones:
            for objecte in zona.objectes:
                if objecte.nom.lower() == nomObjecte.lower():
                    return zona
        return None

    def trobarObjecte(self, nomObjecte):
        for zona in self.zones:
            for objecte in zona.objectes:
                if objecte.nom.lower() == nomObjecte.lower():
                    return objecte
        return None

    def preguntesIhall(self):
        return [
            "On és la llanterna?",
            "On és en Malien?",
            "Com estan els propulsors?",
        ]

    def respostaPregunta(self, index):
        if index == 0:
            zona = self.trobarZonaObjecte("llanterna")
            return zona.nom if zona is not None else None

        if index == 1:
            malien = getattr(self, "malien", None)
            return malien.zona_actual.nom if malien is not None else None

        if index == 2:
            propulsor = self.trobarObjecte("propulsors")
            if propulsor is None:
                return None
            return "reparats" if propulsor.reparats else "encara trencats"

        return None

    def parlar(self):
        preguntes = self.preguntesIhall()
        print("Què vols preguntar a iHall?")
        for i, pregunta in enumerate(preguntes, start=1):
            print(f"{i}. {pregunta}")

        opcio = input("Tria un número: ").strip()
        if not opcio.isdigit() or not (1 <= int(opcio) <= len(preguntes)):
            return "Això no és una pregunta vàlida."

        index = int(opcio) - 1
        pregunta = preguntes[index]
        respostaCorrecta = self.respostaPregunta(index)
        return self.ihall.respondre(pregunta, respostaCorrecta)

    def comprovarFinal(self):
        return self.acabat

    def reiniciar(self):
        # El main torna a cridar iniciar() després de reiniciar
        self.__init__()
