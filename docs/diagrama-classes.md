# Diagrama de classes

Estat final de la implementació (la versió lliurada el 20 de setembre és `Diagrama de classes.drawio.pdf`, a l'arrel del repositori).

```mermaid
classDiagram
    class classeJoc {
        -zones: Zona[]
        -jugador: Jugador
        -company: Company
        -malien: Malien
        -ihall: iHall
        -torn: int
        -acabat: bool
        -contaAtac: int
        -alertaMalien: bool
        +iniciar()
        +jugarTorn(ordre: str)
        +comprovarFinal() bool
        +reiniciar()
    }
    class Zona {
        -nom: str
        -descripcio: str
        -objectes: Objecte[]
        -sortides: Sortida[]
        +descriure(ocults) str
    }
    class Sortida {
        -zonaDesti: str
        -necessitaTarja: bool
        -necessitaVestit: bool
    }
    class Objecte {
        -nom: str
        -descripcio: str
        -portable: bool
        +usar(objectiu) str
    }
    class Tarja {
        -del_company: bool
    }
    class Llanterna {
        -encesa: bool
        +encendre() str
        +apagar() str
    }
    class Eina {
        -utilitzat: bool
    }
    class Donut {
        -menjat: bool
        +menjar()
    }
    class Vestit {
        -equipat: bool
        +posar() str
        +treure() str
    }
    class Calaix {
        -obert: bool
        -contingut: Objecte[]
        +obrir() str
        +tancar() str
        +treure(nom) Objecte
    }
    class Propulsor {
        -reparats: bool
        +reparar() str
    }
    class Estri {
        -missatge: str
    }
    class Personatge {
        -zona_actual: Zona
        +moure(nova_zona)
    }
    class Jugador {
        -inventari: Objecte[]
    }
    class Company {
        -despert: bool
    }
    class Malien {
        -distret: bool
    }
    class iHall {
        +respondre(pregunta, correcta, falsa) str
        +obrir_porta() bool, str
    }
    class JocError
    class OrdreInvalida
    class MovimentInvalid
    class ObjecteNoTrobat
    class ObjecteNoPortable
    class AccioImpossible

    Objecte <|-- Tarja
    Objecte <|-- Llanterna
    Objecte <|-- Eina
    Objecte <|-- Donut
    Objecte <|-- Vestit
    Objecte <|-- Calaix
    Objecte <|-- Propulsor
    Objecte <|-- Estri
    Personatge <|-- Jugador
    Personatge <|-- Company
    Personatge <|-- Malien
    JocError <|-- OrdreInvalida
    JocError <|-- MovimentInvalid
    JocError <|-- ObjecteNoTrobat
    JocError <|-- ObjecteNoPortable
    JocError <|-- AccioImpossible

    classeJoc "1" o-- "10" Zona
    classeJoc "1" *-- "1" Jugador
    classeJoc "1" *-- "1" Company
    classeJoc "1" *-- "1" Malien
    classeJoc "1" *-- "1" iHall
    Zona "1" *-- "0..*" Sortida
    Zona "1" o-- "0..*" Objecte
    Calaix "1" o-- "0..*" Objecte
    Jugador "1" o-- "0..*" Objecte : inventari
    Personatge "*" --> "1" Zona : zona_actual
    Sortida ..> Zona : zonaDesti
    Jugador ..> iHall : consulta
```

## Ordres

Cada ordre és una funció a `src/ordres/`. `interpret.py` separa el verb de l'objectiu i `despatx.py` crida la funció de l'objecte (`agafar`, `deixar`, `encendre`, `apagar`, `obrir`, `tancar`). `anar` i `usar` necessiten l'estat de la partida i els crida directament `classeJoc`; `parlar` viu a `classeJoc` perquè depèn de l'estat del joc (iHall, company).
