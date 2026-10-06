import unittest

import helpers
from excepcions.errors import AccioImpossible, JocError, ObjecteNoPortable, ObjecteNoTrobat
from mapa.zona import Zona
from objectes.calaix import Calaix
from objectes.eina import Eina
from objectes.llanterna import Llanterna
from objectes.propulsor import Propulsor
from objectes.tarja import Tarja
from objectes.vestit import Vestit
from ordres.despatx import executar
from ordres.usar import separar
from personatges.jugador import Jugador


class TestVerbs(unittest.TestCase):
    def setUp(self):
        self.oficines = Zona("oficines", "x", objectes=[Calaix(contingut=[Tarja()]), Vestit()])
        self.tallers = Zona("tallers", "x", objectes=[Eina(), Propulsor()])
        self.jugador = Jugador(self.oficines)

    def test_tarja_invisible_amb_el_calaix_tancat(self):
        with self.assertRaises(ObjecteNoTrobat):
            executar("AGAFAR", self.jugador, "tarja")

    def test_obrir_el_calaix_i_agafar_la_tarja(self):
        self.assertIn("Hi ha: tarja", executar("OBRIR", self.jugador, "calaix"))
        self.assertEqual(executar("AGAFAR", self.jugador, "tarja"), "Agafes tarja.")
        self.assertEqual([objecte.nom for objecte in self.jugador.inventari], ["tarja"])
        self.assertEqual(self.oficines.objectes[0].contingut, [])

    def test_la_tarja_no_es_pot_agafar_dues_vegades(self):
        executar("OBRIR", self.jugador, "calaix")
        executar("AGAFAR", self.jugador, "tarja")
        with self.assertRaises(ObjecteNoTrobat):
            executar("AGAFAR", self.jugador, "tarja")

    def test_tancar_el_calaix(self):
        executar("OBRIR", self.jugador, "calaix")
        self.assertEqual(executar("TANCAR", self.jugador, "calaix"), "Tanques el calaix.")

    def test_objectes_fixos_no_es_poden_agafar(self):
        with self.assertRaises(ObjecteNoPortable):
            executar("AGAFAR", self.jugador, "calaix")

    def test_agafar_no_distingeix_majuscules(self):
        self.assertEqual(executar("AGAFAR", self.jugador, "VESTIT"), "Agafes vestit.")
        self.assertNotIn("vestit", [objecte.nom for objecte in self.oficines.objectes])

    def test_la_eina_necessita_la_llanterna_encesa(self):
        llanterna = Llanterna()
        self.jugador.inventari.append(llanterna)
        self.jugador.moure(self.tallers)
        with self.assertRaises(AccioImpossible):
            executar("AGAFAR", self.jugador, "eina")
        executar("ENCENDRE", self.jugador, "llanterna")
        self.assertEqual(executar("AGAFAR", self.jugador, "eina"), "Agafes eina.")

    def test_la_eina_no_es_pot_agafar_sense_llanterna(self):
        self.jugador.moure(self.tallers)
        with self.assertRaises(AccioImpossible):
            executar("AGAFAR", self.jugador, "eina")

    def test_encendre_i_apagar_la_llanterna(self):
        self.jugador.inventari.append(Llanterna())
        self.assertEqual(executar("ENCENDRE", self.jugador, "llanterna"), "Encens la llanterna.")
        self.assertIn("ja està encesa", executar("ENCENDRE", self.jugador, "llanterna"))
        self.assertEqual(executar("APAGAR", self.jugador, "llanterna"), "Apagues la llanterna.")
        self.assertIn("ja està apagada", executar("APAGAR", self.jugador, "llanterna"))

    def test_accions_que_un_objecte_no_suporta(self):
        self.jugador.inventari.append(Eina())
        with self.assertRaises(AccioImpossible):
            executar("ENCENDRE", self.jugador, "eina")
        with self.assertRaises(AccioImpossible):
            executar("OBRIR", self.jugador, "eina")

    def test_objecte_inexistent(self):
        with self.assertRaises(ObjecteNoTrobat):
            executar("APAGAR", self.jugador, "pizza")

    def test_verb_sense_objectiu(self):
        with self.assertRaises(AccioImpossible) as context:
            executar("ENCENDRE", self.jugador, None)
        self.assertIn("Què vols encendre?", str(context.exception))

    def test_deixar_un_objecte(self):
        executar("AGAFAR", self.jugador, "vestit")
        self.assertEqual(executar("DEIXAR", self.jugador, "vestit"), "Deixes vestit.")
        self.assertEqual(self.jugador.inventari, [])
        self.assertIn("vestit", [objecte.nom for objecte in self.oficines.objectes])

    def test_no_es_pot_deixar_el_vestit_posat(self):
        executar("AGAFAR", self.jugador, "vestit")
        self.jugador.inventari[0].equipat = True
        with self.assertRaises(AccioImpossible):
            executar("DEIXAR", self.jugador, "vestit")

    def test_deixar_el_que_no_es_porta(self):
        with self.assertRaises(AccioImpossible):
            executar("DEIXAR", self.jugador, "vestit")

    def test_totes_les_excepcions_son_del_joc(self):
        for excepcio in (AccioImpossible("x"), ObjecteNoTrobat("x"), ObjecteNoPortable("x")):
            self.assertIsInstance(excepcio, JocError)

    def test_separar_objecte_i_objectiu(self):
        self.assertEqual(separar("eina propulsors"), ("eina", "propulsors"))
        self.assertEqual(separar("eina amb propulsors"), ("eina", "propulsors"))
        self.assertEqual(separar("donuts a en malien"), ("donuts", "malien"))
        self.assertEqual(separar("vestit"), ("vestit", None))


if __name__ == "__main__":
    unittest.main()
