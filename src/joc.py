# Quim Pérez / Pol Moyano

import random

from excepcions.errors import AccioImpossible
from ihall import iHall
from mapa.sortida import Sortida
from mapa.zona import Zona
from objectes.calaix import Calaix
from objectes.donut import Donut
from objectes.eina import Eina
from objectes.estri import Estri
from objectes.llanterna import Llanterna
from objectes.propulsor import Propulsor
from objectes.tarja import Tarja
from objectes.vestit import Vestit
from ordres.anar import anar
from ordres.despatx import VERBS_OBJECTE, executar
from ordres.interpret import interpretar
from ordres.usar import usar
from personatges.company import Company
from personatges.jugador import Jugador
from personatges.malien import Malien


class classeJoc:
    def __init__(self):
        self.zones = []
        self.jugador = None
        self.company = None
        self.malien = None
        self.ihall = iHall()
        self.torn = 0
        self.acabat = False
        self.contaAtac = None
        self.alertaMalien = False

    def iniciar(self):
        self.crearMapa()
        dormitori = self.buscarZona("dormitori")
        self.jugador = Jugador(dormitori)
        self.company = Company(dormitori)
        self.malien = Malien(self.zonaInicialMalien(dormitori))
        self.mostrarIntroduccio()
        print(self.descriureZona(dormitori))

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
        # La comporta a l'espai no necessita tarja, però sí el vestit
        self.connectar(exterior, propulsors, False, True)

        oficines.objectes.append(Calaix(contingut=[Tarja()]))
        vestuari.objectes.append(Vestit())
        cuina.objectes.append(Donut())
        tallers.objectes.append(Eina())
        propulsors.objectes.append(Propulsor())
        banys.objectes.append(Estri("tovallola", "Una tovallola humida.",
                                    "Et eixugues les mans amb la tovallola."))
        menjador.objectes.append(Estri("tassa", "Una tassa de cafè fred.",
                                       "Beus un glop de cafè fred. Quin fàstic."))
        comandament.objectes.append(Estri("consola", "La consola de comandament.",
                                          "La consola no respon: els motors no s'engegaran fins que es reparin els propulsors.",
                                          portable=False))
        exterior.objectes.append(Estri("comporta", "La comporta que dona a l'espai.",
                                       "La comporta dona a l'espai. Sense el vestit posat no sobreviuràs allà fora.",
                                       portable=False))

        self.zones = [tallers, oficines, vestuari, banys, comandament,
                      cuina, dormitori, menjador, exterior, propulsors]

        zonesLlanterna = [zona for zona in self.zones if zona not in (exterior, propulsors)]
        random.choice(zonesLlanterna).objectes.append(Llanterna())

    def connectar(self, zonaA, zonaB, necessitaTarja, necessitaVestit=False):
        zonaA.sortides.append(Sortida(zonaB.nom, necessitaTarja, necessitaVestit))
        zonaB.sortides.append(Sortida(zonaA.nom, necessitaTarja))

    def buscarZona(self, nom):
        for zona in self.zones:
            if zona.nom == nom:
                return zona
        return None

    def zonaInicialMalien(self, dormitori):
        veines = {sortida.zonaDesti for sortida in dormitori.sortides}
        candidates = [zona for zona in self.zones
                      if zona is not dormitori and zona.nom not in veines and zona.nom != "propulsors"]
        return random.choice(candidates)

    def mostrarIntroduccio(self):
        print("=" * 70)
        print("  Any 2120 D.C. La nau PiaXXII viatja cap al planeta SUMMEM.")
        print("  Un aeròlit ha danyat els propulsors. Repara'ls i torna a la sala")
        print("  de comandament per posar en marxa els motors.")
        print("  Compte: un Malien s'ha colat a la nau.")
        print("  (Escriu 'ajuda' per veure les ordres)")
        print("=" * 70)

    def mostrarAjuda(self):
        ordres = [
            ("anar <zona>", "Et mous a una zona del costat (ex: anar banys)"),
            ("agafar <obj>", "Agafes un objecte de la zona"),
            ("deixar <obj>", "Deixes un objecte a la zona"),
            ("usar <obj> [objectiu]", "Fas servir un objecte (ex: usar eina propulsors)"),
            ("encendre <obj>", "Encens un objecte (ex: encendre llanterna)"),
            ("apagar <obj>", "Apagues un objecte"),
            ("obrir <obj>", "Obres un objecte (ex: obrir calaix)"),
            ("tancar <obj>", "Tanques un objecte"),
            ("parlar [company]", "Preguntes a iHall, o despertes el teu company"),
            ("inventari", "Mostra el que portes a sobre"),
            ("mapa", "Dibuixa el mapa de la nau i on ets"),
            ("ajuda", "Mostra aquesta ajuda"),
            ("sortir", "Abandona la partida"),
        ]
        print("Ordres disponibles:")
        for ordre, descripcio in ordres:
            print(f"  {ordre.ljust(24)}{descripcio}")

    def mostrarMapa(self):
        actual = self.jugador.zona_actual.nom

        def caixa(nom):
            marca = "*" if nom == actual else " "
            return f"[{marca}{nom.center(11)}{marca}]"

        centre = " " * 28 + "|"
        laterals = " " * 9 + "|" + " " * 18 + "|" + " " * 18 + "|"

        print()
        print(" " * 21 + caixa("tallers"))
        print(centre)
        print("  " + caixa("vestuari") + "----" + caixa("oficines") + "----" + caixa("banys"))
        print(laterals)
        print("  " + caixa("cuina") + "    " + caixa("comandament") + "    " + caixa("dormitori"))
        print(laterals)
        print(" " * 9 + "+" + "-" * 11 + caixa("menjador") + "-" * 11 + "+")
        print(centre)
        print(" " * 21 + caixa("exterior"))
        print(centre)
        print(" " * 21 + caixa("propulsors"))
        print("\n  [*nom*] = tu ets aquí")

    def mostrarInventari(self):
        if not self.jugador.inventari:
            print("No portes res a sobre.")
            return
        print("Portes: " + ", ".join(objecte.nom for objecte in self.jugador.inventari))

    def descriureZona(self, zona):
        text = "\n" + zona.descriure(self.objectesOcults(zona))
        if self.company is not None and self.company.zona_actual is zona and not self.company.despert:
            text += "\nUn company teu dorm profundament en una càpsula. (Prova: parlar company)"
        return text

    def mostrarSituacio(self):
        zona = self.jugador.zona_actual
        print(f"[{zona.nom}] Sortides: " + ", ".join(s.zonaDesti for s in zona.sortides))

    def objectesOcults(self, zona):
        if zona.nom == "tallers" and not self.llanternaEncesa():
            return [objecte for objecte in zona.objectes if objecte.nom == "eina"]
        return []

    def llanternaEncesa(self):
        return any(objecte.nom == "llanterna" and objecte.encesa for objecte in self.jugador.inventari)

    def jugarTorn(self, ordre):
        # Ordres de control de la partida, no són accions del joc
        control = ordre.strip().lower()
        if control == "ajuda":
            self.mostrarAjuda()
            return
        if control == "inventari":
            self.mostrarInventari()
            return
        if control == "mapa":
            self.mostrarMapa()
            return
        if control == "sortir":
            print(f"Abandones la partida després de {self.torn} torns.")
            self.acabat = True
            return

        # Si l'ordre no és vàlida, l'excepció la recull el main i no es compta el torn
        verb, objectiu = interpretar(ordre)
        atacAbans = self.contaAtac is not None

        if verb == "ANAR":
            if not self.moureJugador(objectiu):
                return
        elif verb == "PARLAR":
            print(self.parlar(objectiu))
        elif verb == "USAR":
            print(usar(self, objectiu))
        elif verb in VERBS_OBJECTE:
            print(executar(verb, self.jugador, objectiu))

        self.torn += 1
        self.finalitzarTorn(atacAbans)

    def moureJugador(self, nomDesti):
        if nomDesti is None:
            print("On vols anar?")
            return False

        zonaDesti, missatge = anar(self.jugador, self.zones, nomDesti, self.ihall)
        if missatge:
            print(missatge)
        if zonaDesti is not None:
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

    def zonaFalsa(self, zonaReal):
        alternatives = [zona for zona in self.zones if zona is not zonaReal]
        return random.choice(alternatives)

    def preguntesIhall(self):
        return [
            "On és la llanterna?",
            "On és en Malien?",
            "Com estan els propulsors?",
        ]

    def respostaPregunta(self, index):
        if index == 0:
            if any(objecte.nom == "llanterna" for objecte in self.jugador.inventari):
                return "La llanterna la portes tu a sobre.", "La llanterna és al menjador."
            zona = self.trobarZonaObjecte("llanterna")
            if zona is None:
                return None, None
            return (f"La llanterna és a {zona.nom}.",
                    f"La llanterna és a {self.zonaFalsa(zona).nom}.")

        if index == 1:
            if self.malien is None:
                return None, None
            zona = self.malien.zona_actual
            return (f"En Malien és a {zona.nom}.",
                    f"En Malien és a {self.zonaFalsa(zona).nom}.")

        if index == 2:
            propulsor = self.trobarObjecte("propulsors")
            if propulsor is None:
                return None, None
            estan = "Els propulsors estan reparats."
            encara = "Els propulsors encara estan trencats."
            return (estan, encara) if propulsor.reparats else (encara, estan)

        return None, None

    def parlar(self, objectiu=None):
        if objectiu is None or objectiu.strip().lower() == "ihall":
            return self.preguntarIhall()
        if objectiu.strip().lower() == "company":
            return self.despertarCompany()
        raise AccioImpossible(f"No hi ha ningú anomenat '{objectiu}' per parlar-hi.")

    def preguntarIhall(self):
        preguntes = self.preguntesIhall()
        print("Què vols preguntar a iHall?")
        for i, pregunta in enumerate(preguntes, start=1):
            print(f"{i}. {pregunta}")

        opcio = input("Tria un número: ").strip()
        if not opcio.isdigit() or not (1 <= int(opcio) <= len(preguntes)):
            return "Això no és una pregunta vàlida."

        index = int(opcio) - 1
        respostaCorrecta, respostaFalsa = self.respostaPregunta(index)
        return self.ihall.respondre(preguntes[index], respostaCorrecta, respostaFalsa)

    def despertarCompany(self):
        if self.company.zona_actual is not self.jugador.zona_actual:
            raise AccioImpossible("El teu company no és aquí.")
        if self.company.despert:
            return "El teu company ja està despert."
        self.company.despert = True
        self.jugador.zona_actual.objectes.append(Tarja(del_company=True))
        return ("Despertes el teu company. Desorientat, deixa la seva tarja identificadora "
                "a la càpsula i se'n va caminant per la nau.")

    def iniciarAtac(self):
        if self.contaAtac is None:
            self.contaAtac = 7

    def finalitzarTorn(self, atacAbans):
        if self.comprovarVictoria():
            return
        if atacAbans and self.comptarAtac():
            return

        self.moureCompany()
        if self.acabat:
            return

        if self.torn % 2 == 0:
            self.moureMalien()
            if self.acabat:
                return

        self.comprovarMalien()

    def comprovarVictoria(self):
        propulsors = self.trobarObjecte("propulsors")
        if propulsors is None or not propulsors.reparats:
            return False
        if self.jugador.zona_actual.nom != "comandament":
            return False
        print("\nPoses en marxa els motors a la sala de comandament. La PiaXXII reprèn el rumb cap a SUMMEM.")
        print(f"Has guanyat la partida en {self.torn} torns!")
        self.acabat = True
        return True

    def comptarAtac(self):
        self.contaAtac -= 1
        if self.contaAtac <= 0:
            self.derrota("Un Malien petit t'esclata de l'estómac. Has mort.")
            return True
        print(f"(Sents moviments a l'estómac... et queden {self.contaAtac} moviments.)")
        return False

    def zonaVeinaAleatoria(self, zona):
        veines = [self.buscarZona(s.zonaDesti) for s in zona.sortides if s.zonaDesti != "propulsors"]
        return random.choice(veines)

    def moureCompany(self):
        if not self.company.despert:
            return
        self.company.moure(self.zonaVeinaAleatoria(self.company.zona_actual))
        if self.company.zona_actual.nom == "cuina":
            self.menjarDonuts()
        self.comprovarCompanyMalien()

    def menjarDonuts(self):
        zona = self.company.zona_actual
        for objecte in zona.objectes:
            if objecte.nom == "donuts" and not objecte.menjat:
                objecte.menjar()
                zona.objectes.remove(objecte)
                print("iHall: «El teu company s'ha menjat els dònuts de la cuina.»")
                return

    def moureMalien(self):
        if self.malien.distret:
            return
        self.malien.moure(self.zonaVeinaAleatoria(self.malien.zona_actual))
        self.comprovarCompanyMalien()

    def comprovarCompanyMalien(self):
        if (self.company.despert and not self.malien.distret
                and self.company.zona_actual is self.malien.zona_actual):
            self.derrota("En Malien ha trobat el teu company. La missió ha fracassat.")

    def comprovarMalien(self):
        mateixaZona = self.malien.zona_actual is self.jugador.zona_actual
        if not mateixaZona or self.malien.distret:
            self.alertaMalien = False
            return
        if self.alertaMalien:
            self.derrota("En Malien se't llança a sobre. La missió ha fracassat.")
            return
        self.alertaMalien = True
        print("En Malien és aquí! Distreu-lo amb els dònuts o fuig d'aquesta zona ara mateix!")

    def derrota(self, missatge):
        print("\n" + missatge)
        print("Has perdut la partida.")
        self.acabat = True

    def comprovarFinal(self):
        return self.acabat

    def reiniciar(self):
        # El main torna a cridar iniciar() després de reiniciar
        self.__init__()
