# Quim Pérez / Pol Moyano

from excepcions.errors import MovimentInvalid
from mapa.sortida import Sortida
from mapa.zona import Zona
from ordres.interpret import interpretar
from personatges.jugador import Jugador


class classeJoc:
    """Controla l'estat de la partida: mapa, jugador i torns."""

    def __init__(self):
        self.zones = []
        self.jugador = None
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

        self.zones = [tallers, oficines, vestuari, banys, comandament,
                      cuina, dormitori, menjador, exterior, propulsors]

    def connectar(self, zonaA, zonaB, necessitaTarja):
        """Crea una sortida en cada sentit entre dues zones."""
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
        print("  anar <zona>   Et mous a una zona del costat (ex: anar banys)")
        print("  ajuda         Mostra aquesta ajuda")
        print("  sortir        Abandona la partida")

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
        if control == "sortir":
            print(f"Abandones la partida després de {self.torn} torns.")
            self.acabat = True
            return

        # Si l'ordre no és vàlida, l'excepció la recull el main i no es compta el torn
        verb, objectiu = interpretar(ordre)

        if verb == "ANAR":
            if not self.moureJugador(objectiu):
                return
        else:
            print(f"Encara no sé fer l'acció {verb}.")
            return

        self.torn += 1

    def moureJugador(self, nomDesti):
        if nomDesti is None:
            print("On vols anar?")
            return False

        nomDesti = nomDesti.lower()
        for sortida in self.jugador.zona_actual.sortides:
            if sortida.zonaDesti == nomDesti:
                self.jugador.moure(self.buscarZona(nomDesti))
                print(self.descriureZona(self.jugador.zona_actual))
                return True

        raise MovimentInvalid(nomDesti)

    def comprovarFinal(self):
        return self.acabat

    def reiniciar(self):
        # El main torna a cridar iniciar() després de reiniciar
        self.__init__()
