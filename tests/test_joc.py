import contextlib
import io
import unittest
from unittest.mock import patch

import helpers
from excepcions.errors import AccioImpossible, MovimentInvalid, OrdreInvalida
from objectes.donut import Donut
from objectes.eina import Eina
from objectes.llanterna import Llanterna
from objectes.tarja import Tarja
from objectes.vestit import Vestit


def objectes_de(joc):
    return [objecte for zona in joc.zones for objecte in zona.objectes]


class TestMapa(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()

    def test_hi_ha_deu_zones(self):
        self.assertEqual(len(self.joc.zones), 10)

    def test_no_totes_les_zones_tenen_les_mateixes_sortides(self):
        self.assertGreater(len({len(zona.sortides) for zona in self.joc.zones}), 1)

    def test_totes_les_zones_menys_el_dormitori_tenen_objectes(self):
        for zona in self.joc.zones:
            if zona.nom != "dormitori":
                self.assertTrue(zona.objectes, zona.nom)

    def test_hi_ha_almenys_sis_objectes_portables(self):
        portables = [objecte for objecte in objectes_de(self.joc) if objecte.portable]
        contingut = [objecte for objecte in objectes_de(self.joc) if hasattr(objecte, "contingut")]
        total = len(portables) + sum(len(calaix.contingut) for calaix in contingut)
        self.assertGreaterEqual(total, 6)

    def test_la_llanterna_canvia_de_lloc(self):
        llocs = set()
        for _ in range(60):
            joc = helpers.nova_partida()
            llocs.add(joc.trobarZonaObjecte("llanterna").nom)
        self.assertGreater(len(llocs), 1)
        self.assertFalse(llocs & {"exterior", "propulsors"})

    def test_malien_no_comença_a_prop_del_jugador(self):
        for _ in range(60):
            joc = helpers.nova_partida()
            proximes = {s.zonaDesti for s in joc.jugador.zona_actual.sortides} | {"dormitori", "propulsors"}
            self.assertNotIn(joc.malien.zona_actual.nom, proximes)

    def test_el_joc_comença_al_dormitori_amb_el_company_dormint(self):
        self.assertEqual(self.joc.jugador.zona_actual.nom, "dormitori")
        self.assertEqual(self.joc.company.zona_actual.nom, "dormitori")
        self.assertFalse(self.joc.company.despert)


class TestPortes(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.distret = True

    def test_sense_tarja_ihall_pot_obrir(self):
        with patch("ihall.random.random", return_value=0.1):
            sortida = helpers.executa(self.joc, "anar banys")
        self.assertEqual(self.joc.jugador.zona_actual.nom, "banys")
        self.assertIn("iHall", sortida)

    def test_sense_tarja_ihall_pot_negar_la_porta(self):
        with patch("ihall.random.random", return_value=0.9):
            sortida = helpers.executa(self.joc, "anar banys")
        self.assertEqual(self.joc.jugador.zona_actual.nom, "dormitori")
        self.assertEqual(self.joc.torn, 1)
        self.assertIn("busca la teva tarja", sortida)

    def test_la_pista_nomes_surt_quan_ihall_nega_la_porta(self):
        with patch("ihall.random.random", return_value=0.1):
            sortida = helpers.executa(self.joc, "anar banys")
        self.assertNotIn("busca la teva tarja", sortida)

    def test_amb_la_tarja_propia_la_porta_s_obre_sola(self):
        self.joc.jugador.inventari.append(Tarja())
        with patch("ihall.random.random", return_value=0.9):
            sortida = helpers.executa(self.joc, "anar banys")
        self.assertEqual(self.joc.jugador.zona_actual.nom, "banys")
        self.assertIn("automàticament", sortida)

    def test_amb_la_tarja_del_company_ihall_ho_recorda(self):
        self.joc.jugador.inventari.append(Tarja(del_company=True))
        with patch("ihall.random.random", return_value=0.9):
            sortida = helpers.executa(self.joc, "anar banys")
        self.assertEqual(self.joc.jugador.zona_actual.nom, "banys")
        self.assertIn("no és la teva", sortida)

    def test_si_es_porten_les_dues_targes_es_fa_servir_la_propia(self):
        self.joc.jugador.inventari.extend([Tarja(del_company=True), Tarja()])
        sortida = helpers.executa(self.joc, "anar banys")
        self.assertIn("automàticament", sortida)

    def test_sortida_inexistent(self):
        with self.assertRaises(MovimentInvalid):
            helpers.executa(self.joc, "anar cuina")

    def test_un_error_no_compta_torn(self):
        with self.assertRaises(MovimentInvalid):
            helpers.executa(self.joc, "anar cuina")
        with self.assertRaises(OrdreInvalida):
            helpers.executa(self.joc, "volar")
        self.assertEqual(self.joc.torn, 0)


class TestVestit(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.distret = True
        self.joc.jugador.moure(self.joc.buscarZona("exterior"))

    def test_sense_vestit_no_es_pot_sortir(self):
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "anar propulsors")

    def test_amb_el_vestit_a_l_inventari_pero_sense_posar_tampoc(self):
        self.joc.jugador.inventari.append(Vestit())
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "anar propulsors")

    def test_amb_el_vestit_posat_es_pot_sortir(self):
        self.joc.jugador.inventari.append(Vestit())
        helpers.executa(self.joc, "usar vestit")
        helpers.executa(self.joc, "anar propulsors")
        self.assertEqual(self.joc.jugador.zona_actual.nom, "propulsors")


class TestTaller(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.distret = True
        self.joc.jugador.moure(self.joc.buscarZona("tallers"))

    def test_la_eina_no_es_veu_a_les_fosques(self):
        self.assertNotIn("eina", self.joc.descriureZona(self.joc.jugador.zona_actual))

    def test_la_eina_es_veu_amb_la_llanterna_encesa(self):
        llanterna = Llanterna()
        llanterna.encesa = True
        self.joc.jugador.inventari.append(llanterna)
        self.assertIn("eina", self.joc.descriureZona(self.joc.jugador.zona_actual))

    def test_no_es_pot_agafar_la_eina_a_les_fosques(self):
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "agafar eina")


class TestUsar(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.distret = True

    def test_cal_agafar_abans_d_usar(self):
        self.joc.jugador.zona_actual.objectes.append(Eina())
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "usar eina")

    def test_usar_sense_dir_que(self):
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "usar")

    def test_objectiu_inexistent(self):
        self.joc.jugador.inventari.append(Eina())
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "usar eina pizza")

    def test_eina_sense_objectiu_pregunta_amb_que(self):
        self.joc.jugador.inventari.append(Eina())
        self.assertIn("Amb què", helpers.executa(self.joc, "usar eina"))

    def test_el_vestit_s_alterna_amb_usar(self):
        vestit = Vestit()
        self.joc.jugador.inventari.append(vestit)
        helpers.executa(self.joc, "usar vestit")
        self.assertTrue(vestit.equipat)
        helpers.executa(self.joc, "usar vestit")
        self.assertFalse(vestit.equipat)

    def test_usar_un_objecte_fix_de_la_zona(self):
        self.joc.jugador.moure(self.joc.buscarZona("comandament"))
        self.assertIn("no respon", helpers.executa(self.joc, "usar consola"))

    def test_la_eina_repara_els_propulsors(self):
        self.joc.jugador.inventari.append(Eina())
        self.joc.jugador.moure(self.joc.buscarZona("propulsors"))
        sortida = helpers.executa(self.joc, "usar eina amb propulsors")
        self.assertTrue(self.joc.trobarObjecte("propulsors").reparats)
        self.assertIn("reparats", sortida)


class TestMalien(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.moure(self.joc.jugador.zona_actual)

    def test_primer_avis_i_despres_derrota(self):
        self.joc.torn = 1
        sortida = helpers.finalitza(self.joc)
        self.assertIn("En Malien és aquí", sortida)
        self.assertFalse(self.joc.acabat)
        sortida = helpers.finalitza(self.joc)
        self.assertTrue(self.joc.acabat)
        self.assertIn("Has perdut", sortida)

    def test_fugir_a_temps_salva_la_partida(self):
        self.joc.torn = 1
        helpers.finalitza(self.joc)
        self.joc.jugador.moure(self.joc.buscarZona("banys"))
        helpers.finalitza(self.joc)
        self.assertFalse(self.joc.acabat)
        self.assertFalse(self.joc.alertaMalien)

    def test_els_donuts_el_distreuen(self):
        donuts = Donut()
        self.joc.jugador.inventari.append(donuts)
        self.joc.torn = 1
        helpers.finalitza(self.joc)
        sortida = helpers.executa(self.joc, "usar donuts malien")
        self.assertTrue(self.joc.malien.distret)
        self.assertIn("es llança sobre els dònuts", sortida)
        self.assertFalse(self.joc.acabat)
        helpers.finalitza(self.joc)
        self.assertFalse(self.joc.acabat)

    def test_gonzalin_es_un_altre_nom_de_malien(self):
        self.joc.jugador.inventari.append(Donut())
        helpers.executa(self.joc, "usar donuts gonzalin")
        self.assertTrue(self.joc.malien.distret)

    def test_els_donuts_no_serveixen_si_malien_no_hi_es(self):
        self.joc.jugador.inventari.append(Donut())
        self.joc.malien.moure(self.joc.buscarZona("cuina"))
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "usar donuts malien")

    def test_uns_donuts_gastats_no_distreuen(self):
        donuts = Donut()
        donuts.menjat = True
        self.joc.jugador.inventari.append(donuts)
        helpers.executa(self.joc, "usar donuts malien")
        self.assertFalse(self.joc.malien.distret)

    def test_es_mou_cada_dos_torns(self):
        self.joc.malien.moure(self.joc.buscarZona("oficines"))
        self.joc.jugador.moure(self.joc.buscarZona("dormitori"))
        with patch("joc.random.choice", side_effect=helpers.primera_opcio):
            helpers.torn_inofensiu(self.joc)
            self.assertEqual(self.joc.malien.zona_actual.nom, "oficines")
            helpers.torn_inofensiu(self.joc)
        self.assertNotEqual(self.joc.malien.zona_actual.nom, "oficines")

    def test_si_esta_distret_no_es_mou(self):
        self.joc.malien.moure(self.joc.buscarZona("oficines"))
        self.joc.malien.distret = True
        self.joc.jugador.moure(self.joc.buscarZona("dormitori"))
        for _ in range(4):
            helpers.torn_inofensiu(self.joc)
        self.assertEqual(self.joc.malien.zona_actual.nom, "oficines")

    def test_mai_entra_a_l_exterior_de_la_nau(self):
        self.joc.malien.moure(self.joc.buscarZona("exterior"))
        self.joc.jugador.moure(self.joc.buscarZona("dormitori"))
        self.joc.torn = 1
        for _ in range(40):
            helpers.torn_inofensiu(self.joc)
            self.assertNotEqual(self.joc.malien.zona_actual.nom, "propulsors")
            if self.joc.acabat:
                break
            self.joc.malien.moure(self.joc.buscarZona("exterior"))
            self.joc.jugador.moure(self.joc.buscarZona("dormitori"))


class TestAtacDeLaEina(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.moure(self.joc.jugador.zona_actual)
        self.joc.malien.distret = True
        self.joc.jugador.inventari.append(Eina())

    def test_ataca_a_malien_i_mor_set_moviments_despres(self):
        sortida = helpers.executa(self.joc, "usar eina malien")
        self.assertIn("7 moviments", sortida)
        self.assertEqual(self.joc.contaAtac, 7)
        for _ in range(6):
            helpers.torn_inofensiu(self.joc)
            self.assertFalse(self.joc.acabat)
        sortida = helpers.torn_inofensiu(self.joc)
        self.assertTrue(self.joc.acabat)
        self.assertIn("Has perdut", sortida)

    def test_un_segon_atac_no_reinicia_el_comptador(self):
        helpers.executa(self.joc, "usar eina malien")
        helpers.torn_inofensiu(self.joc)
        helpers.executa(self.joc, "usar eina malien")
        self.assertLess(self.joc.contaAtac, 7)


class TestCompany(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.distret = True

    def test_despertar_el_company_deixa_la_seva_tarja(self):
        helpers.executa(self.joc, "parlar company")
        self.assertTrue(self.joc.company.despert)
        targes = [o for o in self.joc.jugador.zona_actual.objectes if isinstance(o, Tarja)]
        self.assertEqual(len(targes), 1)
        self.assertTrue(targes[0].del_company)

    def test_no_es_pot_despertar_dues_vegades(self):
        helpers.executa(self.joc, "parlar company")
        self.joc.company.moure(self.joc.jugador.zona_actual)
        self.assertIn("ja està despert", helpers.executa(self.joc, "parlar company"))

    def test_el_company_se_va_en_despertar(self):
        helpers.executa(self.joc, "parlar company")
        self.assertIsNot(self.joc.company.zona_actual, self.joc.jugador.zona_actual)

    def test_no_es_pot_parlar_amb_un_company_que_no_hi_es(self):
        self.joc.jugador.moure(self.joc.buscarZona("banys"))
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "parlar company")

    def test_no_es_pot_parlar_amb_qualsevol_cosa(self):
        with self.assertRaises(AccioImpossible):
            helpers.executa(self.joc, "parlar pizza")

    def test_el_company_dorm_i_no_es_mou(self):
        for _ in range(4):
            helpers.torn_inofensiu(self.joc)
        self.assertEqual(self.joc.company.zona_actual.nom, "dormitori")

    def test_el_company_desperta_es_mou_cada_torn(self):
        helpers.executa(self.joc, "parlar company")
        with patch("joc.random.choice", side_effect=helpers.primera_opcio):
            helpers.torn_inofensiu(self.joc)
        self.assertNotEqual(self.joc.company.zona_actual.nom, "dormitori")

    def test_el_company_menja_els_donuts_de_la_cuina(self):
        self.joc.company.despert = True
        self.joc.company.moure(self.joc.buscarZona("menjador"))
        with patch("joc.random.choice", side_effect=helpers.zona_anomenada("cuina")):
            sortida = helpers.finalitza(self.joc)
        self.assertIn("s'ha menjat els dònuts", sortida)
        self.assertIsNone(self.joc.trobarObjecte("donuts"))

    def test_el_company_no_menja_els_donuts_que_porta_el_jugador(self):
        donuts = Donut()
        self.joc.jugador.inventari.append(donuts)
        self.joc.buscarZona("cuina").objectes.remove(self.joc.trobarObjecte("donuts"))
        self.joc.company.despert = True
        self.joc.company.moure(self.joc.buscarZona("menjador"))
        with patch("joc.random.choice", side_effect=helpers.zona_anomenada("cuina")):
            helpers.finalitza(self.joc)
        self.assertFalse(donuts.menjat)

    def test_si_el_company_troba_malien_es_perd(self):
        self.joc.malien.distret = False
        self.joc.malien.moure(self.joc.buscarZona("cuina"))
        self.joc.company.despert = True
        self.joc.company.moure(self.joc.buscarZona("menjador"))
        with patch("joc.random.choice", side_effect=helpers.zona_anomenada("cuina")):
            sortida = helpers.finalitza(self.joc)
        self.assertTrue(self.joc.acabat)
        self.assertIn("ha trobat el teu company", sortida)

    def test_si_malien_esta_distret_no_fa_mal_al_company(self):
        self.joc.malien.moure(self.joc.buscarZona("cuina"))
        self.joc.company.despert = True
        self.joc.company.moure(self.joc.buscarZona("menjador"))
        with patch("joc.random.choice", side_effect=helpers.zona_anomenada("cuina")):
            helpers.finalitza(self.joc)
        self.assertFalse(self.joc.acabat)


class TestParlarAmbIhall(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()

    def pregunta(self, opcio, aleatori):
        sortida = io.StringIO()
        with patch("builtins.input", return_value=opcio), \
                patch("ihall.random.random", return_value=aleatori), \
                contextlib.redirect_stdout(sortida):
            resposta = self.joc.parlar()
        return resposta, sortida.getvalue()

    def test_el_menu_te_tres_preguntes(self):
        resposta, menu = self.pregunta("1", 0.1)
        numerades = [linia for linia in menu.splitlines() if linia[:2] in ("1.", "2.", "3.")]
        self.assertEqual(len(numerades), 3)
        self.assertNotIn("4.", menu)

    def test_diu_la_veritat_sobre_la_llanterna(self):
        zona = self.joc.trobarZonaObjecte("llanterna")
        resposta, _ = self.pregunta("1", 0.1)
        self.assertEqual(resposta, f"La llanterna és a {zona.nom}.")

    def test_menteix_sobre_la_llanterna(self):
        zona = self.joc.trobarZonaObjecte("llanterna")
        resposta, _ = self.pregunta("1", 0.9)
        self.assertTrue(resposta.startswith("La llanterna és a "))
        self.assertNotEqual(resposta, f"La llanterna és a {zona.nom}.")

    def test_si_portes_la_llanterna_ho_sap(self):
        self.joc.trobarZonaObjecte("llanterna").objectes[:] = []
        self.joc.jugador.inventari.append(Llanterna())
        resposta, _ = self.pregunta("1", 0.1)
        self.assertIn("la portes tu", resposta)

    def test_diu_on_es_malien(self):
        resposta, _ = self.pregunta("2", 0.1)
        self.assertEqual(resposta, f"En Malien és a {self.joc.malien.zona_actual.nom}.")

    def test_estat_dels_propulsors(self):
        resposta, _ = self.pregunta("3", 0.1)
        self.assertEqual(resposta, "Els propulsors encara estan trencats.")
        self.joc.trobarObjecte("propulsors").reparats = True
        resposta, _ = self.pregunta("3", 0.1)
        self.assertEqual(resposta, "Els propulsors estan reparats.")

    def test_opcio_no_valida(self):
        for opcio in ("0", "4", "x", ""):
            resposta, _ = self.pregunta(opcio, 0.1)
            self.assertEqual(resposta, "Això no és una pregunta vàlida.")


class TestFinalDeLaPartida(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()
        self.joc.malien.distret = True
        self.joc.jugador.inventari.extend([Tarja(), Eina(), Vestit()])
        self.joc.jugador.moure(self.joc.buscarZona("exterior"))

    def reparar(self):
        helpers.executa(self.joc, "usar vestit")
        helpers.executa(self.joc, "anar propulsors")
        helpers.executa(self.joc, "usar eina propulsors")

    def test_victoria_en_tornar_a_comandament_amb_els_propulsors_reparats(self):
        self.reparar()
        helpers.executa(self.joc, "usar vestit")
        helpers.executa(self.joc, "anar exterior")
        helpers.executa(self.joc, "anar menjador")
        self.assertFalse(self.joc.comprovarFinal())
        sortida = helpers.executa(self.joc, "anar comandament")
        self.assertTrue(self.joc.comprovarFinal())
        self.assertIn("Has guanyat", sortida)

    def test_no_hi_ha_victoria_si_els_propulsors_no_estan_reparats(self):
        self.joc.jugador.moure(self.joc.buscarZona("menjador"))
        helpers.executa(self.joc, "anar comandament")
        self.assertFalse(self.joc.comprovarFinal())

    def test_sortir_acaba_la_partida(self):
        helpers.executa(self.joc, "sortir")
        self.assertTrue(self.joc.comprovarFinal())

    def test_es_pot_jugar_una_altra_partida(self):
        self.reparar()
        with contextlib.redirect_stdout(io.StringIO()):
            self.joc.derrota("x")
        self.assertTrue(self.joc.comprovarFinal())
        self.joc.reiniciar()
        with contextlib.redirect_stdout(io.StringIO()):
            self.joc.iniciar()
        self.assertFalse(self.joc.comprovarFinal())
        self.assertEqual(self.joc.torn, 0)
        self.assertIsNone(self.joc.contaAtac)
        self.assertEqual(len(self.joc.zones), 10)
        self.assertEqual(self.joc.jugador.inventari, [])
        self.assertFalse(self.joc.trobarObjecte("propulsors").reparats)


class TestOrdresDeControl(unittest.TestCase):
    def setUp(self):
        self.joc = helpers.nova_partida()

    def test_la_situacio_diu_on_ets_i_les_sortides(self):
        sortida = io.StringIO()
        with contextlib.redirect_stdout(sortida):
            self.joc.mostrarSituacio()
        self.assertEqual(sortida.getvalue().strip(), "[dormitori] Sortides: banys, menjador")

    def test_la_situacio_surt_abans_de_cada_ordre(self):
        import main
        sortida = io.StringIO()
        with patch("builtins.input", side_effect=["ajuda", "inventari", "sortir"]), \
                contextlib.redirect_stdout(sortida):
            main.jugar_partida(helpers.classeJoc())
        self.assertEqual(sortida.getvalue().count("[dormitori] Sortides: banys, menjador"), 3)

    def test_la_situacio_canvia_quan_et_mous(self):
        self.joc.malien.distret = True
        with patch("ihall.random.random", return_value=0.1):
            helpers.executa(self.joc, "anar banys")
        sortida = io.StringIO()
        with contextlib.redirect_stdout(sortida):
            self.joc.mostrarSituacio()
        self.assertEqual(sortida.getvalue().strip(), "[banys] Sortides: oficines, dormitori")

    def test_les_sortides_no_es_repeteixen_en_entrar_a_una_zona(self):
        self.joc.malien.distret = True
        with patch("ihall.random.random", return_value=0.1):
            sortida = helpers.executa(self.joc, "anar banys")
        self.assertNotIn("Sortides", sortida)

    def test_ajuda_i_inventari_no_compten_torn(self):
        helpers.executa(self.joc, "ajuda")
        self.assertIn("No portes res", helpers.executa(self.joc, "inventari"))
        self.assertEqual(self.joc.torn, 0)

    def test_l_inventari_llista_el_que_es_porta(self):
        self.joc.jugador.inventari.append(Donut())
        self.assertIn("donuts", helpers.executa(self.joc, "inventari"))

    def test_la_ajuda_menciona_tots_els_verbs(self):
        text = helpers.executa(self.joc, "ajuda")
        for verb in ("anar", "agafar", "deixar", "usar", "encendre", "apagar", "obrir", "tancar", "parlar"):
            self.assertIn(verb, text)


if __name__ == "__main__":
    unittest.main()
