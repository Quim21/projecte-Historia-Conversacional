# Quim Pérez / Pol Moyano

from excepcions.errors import OrdreInvalida
from mapa.sortida import Sortida
from mapa.zona import Zona
from ordres.interpret import interpretar
from personatges.personatge import Personatge


class classeJoc:
    """Controla l'estat de la partida: mapa, jugador i torns."""

    def __init__(self):
        self.zones = []
        self.jugador = None
        self.torn = 0
        self.acabat = False

    def iniciar(self):
        self.crearMapa()
        # De moment el jugador és un Personatge; quan hi hagi la classe Jugador es canviarà
        self.jugador = Personatge(self.buscarZona("dormitori"))
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
        print("=" * 70)

    def descriureZona(self, zona):
        text = f"\n[{zona.nom.upper()}]\n{zona.descripcio}"
        text += "\nSortides: " + ", ".join(s.zonaDesti for s in zona.sortides)
        return text

    def jugarTorn(self, ordre):
        try:
            verb, objectiu = interpretar(ordre)
        except OrdreInvalida as e:
            print(e)
            return
        # Encara no hi ha cap verb implementat
        print(f"Has dit {verb} {objectiu or ''}, però encara no sé fer-ho.")

    def comprovarFinal(self):
        return self.acabat
