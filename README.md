# P000 · Història Conversacional: la nau PiaXXII

Aventura conversacional de text feta en Python, amb orientació a objectes.
Any 2120: la nau PiaXXII ha xocat amb un aeròlit i els propulsors s'han danyat. El capità Bond
s'ha de despertar, reparar-los i tornar a la sala de comandament... mentre un Malien s'ha colat a la nau.

Autors: Quim Pérez / Pol Moyano

## Instal·lació i execució

Només cal Python 3.8 o superior. No hi ha cap dependència externa.

```bash
git clone https://github.com/Quim21/projecte-Historia-Conversacional.git
cd projecte-Historia-Conversacional
python src/main.py
```

A Windows, si `python` no funciona, prova amb `py src/main.py`.

## Com es juga

En iniciar, el joc demana el teu nom i ofereix un menú (`1. Jugar`, `2. Sortir`).
Cada torn escrius una ordre (verb + objecte) i el joc t'explica què passa.
Es poden escriure en majúscules o minúscules.

| Ordre | Què fa |
|---|---|
| `anar <zona>` | Et mous a una zona veïna (`anar banys`) |
| `agafar <objecte>` | Agafes un objecte de la zona o d'un calaix obert |
| `deixar <objecte>` | Deixes un objecte de l'inventari a la zona |
| `usar <objecte> [objectiu]` | Fas servir un objecte, sol o sobre alguna cosa (`usar eina propulsors`) |
| `encendre <objecte>` / `apagar <objecte>` | Encens o apagues (`encendre llanterna`) |
| `obrir <objecte>` / `tancar <objecte>` | Obres o tanques (`obrir calaix`) |
| `parlar` | Fas una pregunta a iHall (tries un número entre 3 preguntes) |
| `parlar company` | Despertes el teu company |
| `inventari` | Mostra el que portes a sobre |
| `ajuda` | Llista les ordres |
| `sortir` | Abandones la partida |

Les ordres `inventari`, `ajuda` i `sortir`, i qualsevol ordre que doni error, no compten com a torn.

### Regles del joc

- **Portes automàtiques.** Gairebé totes les portes de la nau s'obren amb la tarja. Amb la teva tarja s'obren soles;
  amb la d'un company, iHall t'ho retreu; sense tarja, depèn de iHall, que només fa cas la meitat de les vegades.
- **iHall.** Respon a tres preguntes (on és la llanterna, on és en Malien, com estan els propulsors).
  Diu la veritat el 50 % de les vegades; l'altre 50 % et dona una pista falsa.
- **Taller a les fosques.** No es pot agafar l'eina si no portes la llanterna encesa.
- **Exterior.** Per sortir als propulsors cal portar el vestit d'astronauta posat (`usar vestit`).
- **Malien.** Es mou cada dos torns per la nau. Si coincideix amb tu, tens un torn per distreure'l
  amb els dònuts (`usar donuts malien`) o per fugir; si no, perds. Un cop distret, es queda entretingut tota la partida.
  Si l'ataques amb l'eina, se't cola per la gola i mors set moviments després.
- **El company.** Dorm al dormitori. Si el despertes deixa la seva tarja i es posa a caminar per la nau
  una zona per torn: si troba en Malien, la partida s'acaba, i si arriba a la cuina es menja els dònuts.
- **Final.** Guanyes quan els propulsors estan reparats i arribes a la sala de comandament.
  Perds si en Malien t'atrapa, si mors per l'atac de l'eina o si en Malien troba el teu company.
  En acabar, el joc et deixa jugar una altra partida (la llanterna canvia de lloc cada vegada).

## Estructura del projecte

```
src/
├── main.py            punt d'entrada: menú d'inici, bucle de la partida i "tornar a jugar"
├── joc.py             classeJoc: estat de la partida, torns, Malien, company i final
├── ihall.py           iHall: respon preguntes i obre portes (amb 50 % de sort)
├── mapa/              Zona i Sortida (les 10 zones i les seves connexions)
├── objectes/          Objecte i els seus fills: Tarja, Llanterna, Eina, Donut, Vestit, Calaix, Propulsor, Estri
├── personatges/       Personatge i els seus fills: Jugador, Company, Malien
├── ordres/            un fitxer per ordre, l'intèrpret (interpret.py) i el despatxador (despatx.py)
└── excepcions/        errors del joc (tots hereten de JocError)
docs/                  diagrama de classes
```

Les errades de l'usuari (ordre desconeguda, objecte que no hi és, acció impossible...) es gestionen amb excepcions
pròpies que hereten de `JocError`; `main.py` les captura i mostra el missatge sense aturar la partida.

## Documentació

- [Diagrama de classes](docs/diagrama-classes.md)
