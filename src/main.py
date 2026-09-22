# Quim Pérez / Pol Moyano

from joc import classeJoc

def main():
    joc = classeJoc()
    joc.iniciar()

    while not joc.comprovarFinal():
        ordre = input("Què vols fer? ")
        joc.jugarTorn(ordre)

if __name__ == "__main__":
    main()