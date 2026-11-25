#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DE LA MÉTHODE DES 30 % (ARBITRAGE du 14-11-2026, corrections C1 à C6 et C13) — Simulation uniquement.
Mercredi 25-11-2026.

LE SENS EN TÊTE — Au regard unique sur les 30 % (cas 2 de R-505), m versions d'une famille sont jugées ensemble.
L'arbitrage du 14-11-2026 a classé sept corrections DE FOND, programmées le 25-11-2026 dans
`programmes/MODULE_JUGEMENT.py` (`romano_wolf_du_gain`, `holm_du_hasard`, `tirages_exiges_par_holm`,
`SEUIL_PAR_FAMILLE_DEFAUT`, `PORTEE_DU_VERDICT_DES_30`) et `programmes/CALIBRER_LA_METHODE_DES_30.py`. Ces épreuves
vérifient, vite et sur des données FABRIQUÉES (dates de 2024 et après ; aucun cours lu), que chaque correction fait ce
qu'elle dit, et `--saboter` retire chacune d'elles pour vérifier qu'un cas rougit (R-731).
  C5 — la statistique est celle du juge : E1. C4 — mêmes tirages pour toutes les versions : E2 ; calendrier = période
  déclarée : E3. C13 — seuil par famille paramétrable, 2,5 % par défaut : E4 ; Holm pas à pas pour ⑥ : E5 ; tirages
  exigés (N2) : E5b. Pas à pas de Romano et Wolf : E6. C1, C2, C3 — ce que prouve le verdict : E7. C6 — le calibrage a
  des dents : E8 ; mode « --famille » (⑤ et ⑥ ensemble) : E9.

USAGE : python3 -B tests/EPREUVES_DE_LA_METHODE_DES_30_Mer_25-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de sabotage
est introuvable, si un nom ou une option est inconnu ou si un fichier manque (R-734).

① RÔLE — Prouver que les corrections font ce que dit leur texte, et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque fichier
  de tests/ avec la racine, puis avec « --saboter » ; sur GitHub, code `MethodeDes30` de
  `tests/LANCEMENT_DES_EPREUVES.json`. Ce programme se relance en « --cas <copie> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : les fichiers de `FICHIERS`. Sinon code 2.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier les programmes dans un dossier temporaire, appliquer le sabotage
  (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie · ③ Z0 doit être vert ; un sabotage
  doit faire rougir au moins un cas.
⑦ UNITÉ — Gains en EUROS ; durées en JOURS DE CALENDRIER ; probabilités sans unité.
⑧ POURQUOI — R-731 (une épreuve et un sabotage qui mord par correction), R-734 (code non nul si un contrôle n'a pas pu
  tourner), R-708 (E1 confronte les deux écritures du t par blocs).
⑨ CE QUI CLOCHE — ① Aucun cas ne vient d'une vraie ligne (R-732) : la consigne du 25-11-2026 n'admet que des données
  fabriquées. ② E1 ne compare que des séries fortes (moins de 40 tirages « aussi bien ») : au-delà,
  `probabilite_que_le_gain_soit_du_hasard` s'arrête tôt (Besag et Clifford) et les deux p diffèrent par construction.
  ③ Le calibrage lui-même (des milliers de mondes) n'est pas joué ici : E8 n'éprouve que ses dents.
⑩ EFFET — Écrit et efface des dossiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 600 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""
import datetime, importlib.util, json, os, random, shutil, subprocess, sys, tempfile

sys.dont_write_bytecode = True
ICI = os.path.abspath(__file__)
MODULE = "programmes/MODULE_JUGEMENT.py"
CALIBRAGE = "programmes/CALIBRER_LA_METHODE_DES_30.py"
FICHIERS = (MODULE, CALIBRAGE, "programmes/CALIBRER_LE_HASARD_DES_GAINS.py", "programmes/CONTRATS_DES_FICHIERS.py",
            "programmes/COMMUN.py")
D0 = datetime.date(2024, 1, 2)

# LES SABOTAGES : nom → (fichier, texte présent UNE fois, remplacement). Chacun retire une correction.
SABOTAGES = {
    # C5 : la statistique n'est plus celle du juge (n du juge glissé dans le t, comme l'ancien Student) ; tenu par E1
    "S1_C5_t_qui_n_est_pas_celui_du_juge": [(MODULE, "        t_vrais.append(moyenne / (math.sqrt(carre) / effectif))\n",
                                             "        t_vrais.append(moyenne / (math.sqrt(carre) / effectif) * 0.9)\n")],
    # C4 : des tirages propres à chaque version ; tenu par E2
    "S2_C4_tirages_par_version": [(MODULE, "        for f_n, f_s, f_ss, f_sc, f_cc in sommes:\n            n_tir = sum(choix(f_n))\n",
                                   "        for f_n, f_s, f_ss, f_sc, f_cc in sommes:\n"
                                   "            choix = itemgetter(*[int(tireur() * nb_jours) for _ in range(nb_blocs)])\n"
                                   "            n_tir = sum(choix(f_n))\n")],
    # C4 : le calendrier pris aux entrées des versions, pas à la période déclarée ; tenu par E3
    "S3_C4_calendrier_des_entrees": [(MODULE, "    lues = [(nom, _operations_d_une_version(nom, ops, premier, dernier)) for nom, ops in versions.items()]\n",
                                      "    lues = [(nom, _operations_d_une_version(nom, ops, premier, dernier)) for nom, ops in versions.items()]\n"
                                      "    premier = min(min(e) for _, (_, e, _) in lues)\n"
                                      "    nb_jours = max(max(e) for _, (_, e, _) in lues) - premier + 1\n")],
    # C13 : retour à 5 % par famille ; tenu par E4
    "S4_C13_seuil_par_defaut_5": [(MODULE, "SEUIL_PAR_FAMILLE_DEFAUT = 0.025\n", "SEUIL_PAR_FAMILLE_DEFAUT = 0.05\n")],
    # C13 : Holm devient Bonferroni (barre fixe) ; tenu par E5
    "S5_C13_holm_sans_pas": [(MODULE, "        barres[nom] = seuil / (m - rang)\n", "        barres[nom] = seuil / m\n")],
    # N2 : trop peu de tirages accepté ; tenu par E5b
    "S6_N2_tirages_non_exiges": [(MODULE, "        elif tirages < exiges:\n", "        elif False:\n")],
    # pas à pas retiré (un seul pas) ; tenu par E6
    "S7_un_seul_pas": [(MODULE, "        en_lice = [i for i in en_lice if i not in du_pas]\n", "        break\n")],
    # C1, C2, C3 : la portée du verdict effacée ; tenu par E7
    "S8_C1_C3_portee_effacee": [(MODULE, "PORTEE_DU_VERDICT_DES_30 = (\n", "PORTEE_DU_VERDICT_DES_30 = \"\" and (\n")],
    # C6 : le calibrage ne voit plus rien ; tenu par E8
    "S9_C6_calibrage_aveugle": [(CALIBRAGE, "    if binomiale(mesure[\"faux\"], calcules, seuil) < NIVEAU_DE_L_ALERTE:\n",
                                 "    if False:\n")],
    # mode « --famille » (décision de Jean-Luc du 25-11-2026, 15h36) : ⑥ oublié dans le jugement ; tenu par E9
    "S10_famille_sans_le_controle_6": [(CALIBRAGE, "            if etats[v] == \"PASSE\"]\n", "            if etats[v] or True]\n")],
    # mode « --famille » : les 10 versions « gain sûr » n'ont plus de gain ; tenu par E9
    "S11_famille_sans_gain_sur": [(CALIBRAGE, "dict(o, net=o[\"net\"] + FAMILLE_DECALAGE_EUR)", "dict(o, net=o[\"net\"] + 0.0)")],
    # mode « --famille » : nombre de mondes qui n'atteint plus « strictement moins de ±1 point » ; tenu par E9
    # mode « --famille » : ⑥ des « gain sûr » rendu impossible à passer (le taux mesuré tomberait à tort) ; tenu par E9c
    "S13_famille_hasard_toujours_battu": [(CALIBRAGE, "        net = math.sqrt(ressemblance) * commun",
                                           "        net = -1e9 + math.sqrt(ressemblance) * commun")],
    "S12_famille_precision_au_bord": [(CALIBRAGE, "demi_largeur), 9)) + 1\n", "demi_largeur), 9))\n")],
}


def charger(chemin, nom):
    """Charge un programme par son chemin.
    ① RÔLE — Prendre le module éprouvé dans la copie. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — chemin, nom.
    ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — spec_from_file_location, exécution, rangé dans sys.modules sous son nom. ⑦ UNITÉ — —.
    ⑧ POURQUOI — le module importe ses voisins par leur nom : il doit trouver la copie.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — charge du code. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


def serie(decalage, graine, n=80, jours=700):
    """Fabrique une version : n opérations +1 000 / −2 500 € (70 % / 30 %), plus un décalage, sur `jours` jours.
    ① RÔLE — Une série de vérité connue. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — décalage (euros), graine, n, jours.
    ④ CONDITIONS D'ENTRÉE — n ≤ jours. ⑤ SORTIE — UNE valeur : la liste d'opérations. [rend: 1]
    ⑥ TRAITEMENT — jours d'entrée tirés sans remise et triés, détention de 7 jours. ⑦ UNITÉ — euros, jours.
    ⑧ POURQUOI — dates à partir du 2024-01-02 : données fabriquées, 2024 et après (consigne du 25-11-2026).
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    h = random.Random(graine)
    entrees = sorted(h.sample(range(jours), n))
    return [{"net": (1000.0 if h.random() < 0.7 else -2500.0) + decalage + h.uniform(-100.0, 100.0),
             "date_entree": (D0 + datetime.timedelta(days=j)).isoformat(),
             "date_sortie": (D0 + datetime.timedelta(days=j + 6)).isoformat()} for j in entrees]


def bornes(ops):
    """Rend la période des entrées d'une version.
    ① RÔLE — La période propre d'une version (E1). ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — ops.
    ④ CONDITIONS D'ENTRÉE — au moins une opération. ⑤ SORTIE — DEUX valeurs : première et dernière entrée. [rend: 2]
    ⑥ TRAITEMENT — min et max. ⑦ UNITÉ — dates. ⑧ POURQUOI — comparer à `probabilite_que_le_gain_soit_du_hasard`, qui
    prend cette période. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    return min(o["date_entree"] for o in ops), max(o["date_entree"] for o in ops)


def cas(copie):
    """Joue tous les cas sur les programmes de la copie et rend leurs résultats.
    ① RÔLE — Les épreuves elles-mêmes. ② CONTEXTE D'APPEL — `main`, en « --cas ». ③ ENTRÉE — la copie.
    ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur : liste de [nom, vert, détail]. [rend: 1]
    ⑥ TRAITEMENT — E1 à E8, chacun enveloppé (une erreur = rouge). ⑦ UNITÉ — voir l'en-tête.
    ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    sys.path.insert(0, os.path.join(copie, "programmes"))
    J = charger(os.path.join(copie, MODULE), "MODULE_JUGEMENT")
    res = []

    def ok(nom, cond, det=""):
        res.append([nom, bool(cond), str(det)[:300]])

    def essai(nom, f):
        try:
            f()
        except Exception as ex:      # une erreur est un rouge, jamais un silence
            res.append([nom, False, "%s: %s" % (type(ex).__name__, str(ex)[:200])])

    RW, P = J.romano_wolf_du_gain, J.probabilite_que_le_gain_soit_du_hasard

    def e1():   # C5 : une version seule, sa propre période → le p du juge, à l'octet
        for dec in (800.0, 650.0, 500.0):
            s = serie(dec, graine=1)
            a, b = bornes(s)
            p_juge = P(s, J.SEUIL_PAR_FAMILLE_DEFAUT)
            p_rw = RW({"A": s}, a, b)["p_au_pas"]["A"]
            ok("E1 C5 : version seule (décalage %+.0f €), sa période : p de Romano-Wolf = p du juge (%r)" % (dec, p_juge),
               p_rw == p_juge and p_juge * 2000 <= 40, "%r contre %r" % (p_rw, p_juge))
    essai("E1", e1)

    def e2():   # C4 : deux copies d'une même version ne paient pas deux fois (mêmes tirages)
        s = serie(650.0, graine=1)
        a, b = bornes(s)
        seule = RW({"A": s}, a, b)["p_au_pas"]["A"]
        r = RW({"A": s, "B": [dict(o) for o in s]}, a, b)
        ok("E2 C4 : deux versions identiques → même p que la version seule (%r), toutes deux validées ensemble" % seule,
           r["p_au_pas"]["A"] == seule == r["p_au_pas"]["B"] and r["etapes"][0]["validees"] == ["A", "B"],
           "%r %r %r" % (r["p_au_pas"], seule, r["etapes"]))
    essai("E2", e2)

    def e3():   # C4 : le calendrier est la période déclarée ; une entrée hors période est refusée
        s = serie(650.0, graine=1)                                  # entrées dans les 700 premiers jours
        r = RW({"A": s, "B": serie(0.0, graine=2)}, "2024-01-02", "2026-12-31")
        attendu = (datetime.date(2026, 12, 31) - D0).days + 1
        ok("E3 C4 : période déclarée de %d jours → calendrier de %d jours (pas celui des entrées)" % (attendu, attendu),
           r["periode_jours"] == attendu, repr(r["periode_jours"]))
        try:
            RW({"A": s}, "2024-03-01", "2026-12-31")
            ok("E3b C4 : une entrée avant la période déclarée → refusée", False, "acceptée")
        except ValueError as ex:
            ok("E3b C4 : une entrée avant la période déclarée → refusée", "hors de la période" in str(ex), str(ex))
    essai("E3", e3)

    def e4():   # C13 : 2,5 % par défaut, paramétrable
        trouve = None
        for k in range(60):                                         # recherche déterministe d'un p entre 2,5 et 5 %
            s = serie(300.0 + 10.0 * k, graine=7)
            a, b = bornes(s)
            r = RW({"A": s}, a, b, seuil=0.05)
            if 0.025 < r["p_au_pas"]["A"] <= 0.05:
                trouve = (s, a, b, r)
                break
        ok("E4 C13 : une version de p entre 2,5 % et 5 % existe dans la recherche", trouve is not None, "")
        if trouve:
            s, a, b, r5 = trouve
            defaut = RW({"A": s}, a, b)
            ok("E4b C13 : SEUIL_PAR_FAMILLE_DEFAUT vaut 0,025 ; validée à 5 %% (paramètre), pas au défaut (p = %r)"
               % r5["p_au_pas"]["A"], J.SEUIL_PAR_FAMILLE_DEFAUT == 0.025 and r5["validees"] == ["A"]
               and defaut["validees"] == [] and defaut["seuil"] == 0.025, "%r %r" % (r5["validees"], defaut["validees"]))
            h = J.holm_du_hasard({"A": (0.03, 10000)})
            ok("E4c C13 : Holm au défaut : p = 0,03 seul → BLOQUE (2,5 %)", h["etats"]["A"] == "BLOQUE" and h["seuil"] == 0.025,
               repr(h))
    essai("E4", e4)

    def e5():   # Holm pas à pas, exemple de la méthode (§A.4)
        p = {"a": (0.001, 10000), "b": (0.010, 10000), "c": (0.020, 10000), "d": (0.300, 10000)}
        h5 = J.holm_du_hasard(p, seuil=0.05)
        h25 = J.holm_du_hasard(p)
        ok("E5 Holm : 0,001 ; 0,010 ; 0,020 ; 0,300 → 3 passent à 5 % (Bonferroni : 2), 1 à 2,5 %",
           [h5["etats"][k] for k in "abcd"] == ["PASSE", "PASSE", "PASSE", "BLOQUE"]
           and [h25["etats"][k] for k in "abcd"] == ["PASSE", "BLOQUE", "BLOQUE", "BLOQUE"], "%r %r" % (h5, h25))
    essai("E5", e5)

    def e5b():  # N2 : 40 × m + 1 tirages à 2,5 %
        ok("E5b N2 : 15 versions à 2,5 % → 601 tirages exigés", J.tirages_exiges_par_holm(15) == 601,
           repr(J.tirages_exiges_par_holm(15)))
        p = {("v%d" % i): (0.0001, 600) for i in range(15)}
        h = J.holm_du_hasard(p)
        ok("E5c N2 : 600 tirages pour 15 versions → INCONNU, jamais PASSE", set(h["etats"].values()) == {"INCONNU"},
           repr(set(h["etats"].values())))
        p = {("v%d" % i): (0.0001, 601) for i in range(15)}
        ok("E5d N2 : 601 tirages → PASSE", set(J.holm_du_hasard(p)["etats"].values()) == {"PASSE"}, "")
    essai("E5b", e5b)

    def e6():   # le pas à pas valide au second pas une version que le premier ne valide pas : huit versions fortes
        #         (+1 200 €) partent au 1er pas ; la barre baisse (mesuré le 25-11-2026 : t 3,63 → 2,04) ; M (+900 €,
        #         t 2,77) passe au 2e pas
        fam = {("F%d" % i): serie(1200.0, graine=10 + i) for i in range(8)}
        fam["M"] = serie(900.0, graine=3)
        r = RW(fam, "2024-01-02", "2025-12-31")
        e = r["etapes"]
        ok("E6 pas à pas : M validée au 2e pas, après le retrait des 8 fortes, barre qui baisse",
           len(e) >= 2 and "M" not in e[0]["validees"] and len(e[0]["validees"]) == 8 and "M" in e[1]["validees"]
           and e[1]["barre_t"] < e[0]["barre_t"] and "M" in r["validees"], repr([(x["barre_t"], x["validees"]) for x in e]))
    essai("E6", e6)

    def e7():   # C1, C2, C3 : ce que prouve le verdict, rendu avec chaque famille
        s = serie(650.0, graine=1)
        a, b = bornes(s)
        txt = RW({"A": s}, a, b)["ce_que_prouve"]
        ok("E7 C1/C2/C3 : le verdict dit ce qu'il ne prouve pas (la durée), la seule preuve de durée (marche en avant "
           "réelle) et la limite de ⑥ (prime propre au signal)",
           "ne prouve pas" in txt.lower() and "durera" in txt and "marche en avant réelle" in txt
           and "prime propre au signal" in txt and txt == J.PORTEE_DU_VERDICT_DES_30, txt[:120])
    essai("E7", e7)

    def e8():   # C6 : le calibrage voit une méthode trop indulgente, et laisse passer une méthode prudente
        C = charger(os.path.join(copie, CALIBRAGE), "CALIBRER_LA_METHODE_DES_30")
        H = charger(os.path.join(copie, "programmes/CALIBRER_LE_HASARD_DES_GAINS.py"), "CALIBRER_LE_HASARD_DES_GAINS")
        formes = C.fabriquer_les_formes()
        forme = formes["+1/-3 (10 jours)"]
        moyenne = sum(g for g, _ in forme) / len(forme)
        hasard = random.Random(1)
        liaison = C.LIAISONS["paquets de 10 liés (0,36)"]

        def fabriquer(k):
            return C.fabriquer_une_famille(hasard, forme, 50, 3, liaison, 0.96)
        laxiste = C.mesurer_le_risque(lambda v, a, b, s: list(v)[:1],
                                      fabriquer, 60, 0.025)
        prudente = C.mesurer_le_risque(lambda v, a, b, s: [], fabriquer, 60, 0.025)
        famille = fabriquer(0)
        ok("E8 C6 : formes fabriquées de moyenne nulle (%.2e €), familles de 3 versions × 50 opérations, 2024 et après"
           % moyenne, abs(moyenne) < 1e-6 and len(famille) == 3 and all(len(o) == 50 for o in famille.values())
           and min(o["date_entree"] for ops in famille.values() for o in ops) >= "2024-01-01", "")
        ok("E8b C6 : une méthode qui valide toujours → DÉPASSE ; une qui ne valide jamais → TIENT",
           C.verdict_d_une_case(laxiste, 0.025, H.binomiale_au_dessus) == "DÉPASSE"
           and C.verdict_d_une_case(prudente, 0.025, H.binomiale_au_dessus) == "TIENT", "%r %r" % (laxiste, prudente))
        r = C.mesurer_le_risque(lambda v, a, b, s: J.romano_wolf_du_gain(v, a, b, seuil=s)["validees"], fabriquer, 8, 0.025)
        ok("E8c C6 : la vraie méthode passe dans le calibrage (8 mondes, aucun non calculable)",
           r["non_calculables"] == 0 and r["mondes"] == 8, repr(r))
    essai("E8", e8)

    def e9():   # mode « --famille » : ⑤ ET ⑥ ensemble, au pire cas de l'arbitre (décision de Jean-Luc du 25-11-2026)
        C = charger(os.path.join(copie, CALIBRAGE), "CALIBRER_LA_METHODE_DES_30")
        forme = C.fabriquer_les_formes()["+1/-3 (10 jours)"]
        hasard = random.Random(7)
        tirages = J.tirages_exiges_par_holm(20, 0.05)
        debut, fin = C.DEBUT.isoformat(), (C.DEBUT + datetime.timedelta(days=C.PERIODE_JOURS - 1)).isoformat()
        sures5 = sures6 = juste = 0
        p_h = []
        for k in range(3):
            versions, p6 = C.fabriquer_la_famille_mixte(hasard, J, forme, C.LIAISONS["indépendantes"], 0.0, tirages)
            rw = J.romano_wolf_du_gain(versions, debut, fin, seuil=0.05, graine=20 + k)["validees"]
            etats = J.holm_du_hasard(p6, 0.05)["etats"]
            sures5 += all(v in rw for v in versions if v[0] == "h")
            p_h += [p6[v][0] for v in versions if v[0] == "h"]
            sures6 += all(etats[v] == "PASSE" for v in versions if v[0] == "z")
            juste += C.juger_les_deux(J, versions, p6, debut, fin, 0.05, 20 + k) == [v for v in rw if etats[v] == "PASSE"]
        ok("E9 famille : sur 3 mondes, ⑤ valide les 10 « gain sûr », ⑥ passe les 10 « gain nul », et le jugement est "
           "l'INTERSECTION des deux", (sures5, sures6, juste) == (3, 3, 3), "%r" % ((sures5, sures6, juste),))
        ok("E9b famille : nombre de mondes pour moins de ±1 point à 95 % quel que soit le taux = 9 605 (à 15 % : 4 899)",
           (C.mondes_pour_la_precision(), C.mondes_pour_la_precision(0.15)) == (9605, 4899),
           "%r" % ((C.mondes_pour_la_precision(), C.mondes_pour_la_precision(0.15)),))
        moyenne_h = sum(p_h) / len(p_h)
        ok("E9c famille : les 30 p de ⑥ des « gain sûr » sont ceux d'un tirage de plus (moyenne %.3f, attendue 0,5 ; "
           "acceptée entre 0,3 et 0,7)" % moyenne_h, len(p_h) == 30 and 0.3 < moyenne_h < 0.7, "%r" % p_h[:5])
    essai("E9", e9)
    return res


def preparer(racine, sab):
    """Copie les programmes et applique un sabotage.
    ① RÔLE — Donner à chaque sabotage sa copie. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — la racine, le nom ou « Z0 ».
    ④ CONDITIONS D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — UNE valeur : le dossier. [rend: 1]
    ⑥ TRAITEMENT — copier, remplacer. ⑦ UNITÉ — —. ⑧ POURQUOI — une cible introuvable ne sabote rien : elle lève.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — crée un dossier temporaire. ⑪ TERMINAISON — rend la main ou lève LookupError.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="methode30_%s_" % sab[:12])
    os.makedirs(os.path.join(d, "programmes"))
    for f in FICHIERS:
        shutil.copy(os.path.join(racine, f), os.path.join(d, f))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            shutil.rmtree(d)
            raise LookupError("sabotage %s : le texte visé est présent %d fois dans %s" % (sab, t.count(a), f))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d


def jouer(racine, sab):
    """Relance ce programme en « --cas » sur la copie d'un sabotage et rend ses lignes.
    ① RÔLE — Isoler chaque copie dans son processus. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — racine, sabotage.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : liste de (nom, vert, détail). [rend: 1]
    ⑥ TRAITEMENT — préparer, relancer (borné à 600 s), lire le JSON, effacer la copie. ⑦ UNITÉ — —.
    ⑧ POURQUOI — les modules ont les mêmes noms d'une copie à l'autre. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — dossiers
    temporaires. ⑪ TERMINAISON — rend la main ; un dépassement ou une sortie illisible rend un cas rouge. [sort: non]"""
    d = preparer(racine, sab)
    try:
        r = subprocess.run([sys.executable, "-B", ICI, "--cas", d], capture_output=True, text=True, timeout=600)
        try:
            return [tuple(x) for x in json.loads(r.stdout.strip().splitlines()[-1])]
        except (ValueError, IndexError):
            return [("relance illisible", False, (r.stdout + r.stderr)[-300:])]
    except subprocess.TimeoutExpired:
        return [("relance au-delà de 600 s", False, "")]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    """Joue Z0 puis les sabotages demandés, affiche, rend le code.
    ① RÔLE — Le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — argv.
    ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — « --cas » : jouer les cas et écrire leur JSON ; sinon Z0, puis chaque sabotage demandé.
    ⑦ UNITÉ — —. ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if len(argv) == 3 and argv[1] == "--cas":
        print(json.dumps(cas(argv[2]), ensure_ascii=False))
        return 0
    if len(argv) < 2 or len(argv) > 3 or argv[1].startswith("--"):
        print(__doc__.split("USAGE")[1].split("①")[0].strip())
        return 2
    racine = os.path.abspath(argv[1])
    for f in FICHIERS:
        if not os.path.exists(os.path.join(racine, f)):
            print("FICHIER MANQUANT : %s" % f)
            return 2
    demandes = []
    if len(argv) == 3:
        demandes = list(SABOTAGES) if argv[2] == "--saboter" else [argv[2]]
        if any(s not in SABOTAGES for s in demandes):
            print("SABOTAGE OU OPTION INCONNU : %s · connus : --saboter %s" % (argv[2], " ".join(SABOTAGES)))
            return 2
    print("ÉPREUVES DE LA MÉTHODE DES 30 %% — racine : %s" % racine)
    try:
        z0 = jouer(racine, "Z0")
    except LookupError as ex:
        print(str(ex))
        return 2
    for nom, vert, det in z0:
        print("  %s  %s%s" % ("VERT " if vert else "ROUGE", nom, ("  — " + det) if (det and not vert) else ""))
    rouges = sum(1 for _, v, _ in z0 if not v)
    print("== Z0 : %d cas, %d rouge(s)" % (len(z0), rouges))
    survivants = []
    for s in demandes:
        try:
            lignes = jouer(racine, s)
        except LookupError as ex:
            print(str(ex))
            return 2
        mordus = [n for n, v, _ in lignes if not v]
        print("  %s %s : %d cas rouges — %s" % ("mord" if mordus else "SURVIT", s, len(mordus),
                                               " | ".join(x.split(" ")[0] for x in mordus)))
        if not mordus:
            survivants.append(s)
    if rouges or survivants:
        print("VERDICT : NON CONFORME%s" % ((" — sabotages qui survivent : %s" % survivants) if survivants else ""))
        return 1
    print("VERDICT : conforme")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
