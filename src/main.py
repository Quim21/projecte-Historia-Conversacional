# Quim Pérez / Pol Moyano

from joc import classeJoc
from excepcions.errors import JocError

def main():
    if not menu_inici():
        return

    joc = classeJoc()
    jugar_partida(joc)

    while vol_tornar_a_jugar():
        joc.reiniciar()
        jugar_partida(joc)

def menu_inici():
    nom = input("Com et dius, capità? ")
    print(f"Benvingut a bord, {nom}.")

    while True:
        opcio = input("1. Jugar\n2. Sortir\nTria una opció: ").strip()
        if opcio == "1":
            return True
        if opcio == "2":
            return False
        print("Opció no vàlida.")

def jugar_partida(joc):
    joc.iniciar()

    while not joc.comprovarFinal():
        joc.mostrarSituacio()
        ordre = input("Què vols fer? ")
        try:
            joc.jugarTorn(ordre)
        except JocError as error:
            print(error)

def vol_tornar_a_jugar():
    resposta = input("Vols tornar a jugar? (s/n) ") 
    return resposta.strip().lower() == "s"

if __name__ == "__main__":
    main()