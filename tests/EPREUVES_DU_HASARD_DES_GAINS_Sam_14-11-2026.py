"""ÉPREUVES DU HASARD DES GAINS (A-782, A-786) — `probabilite_que_le_gain_soit_du_hasard` et `minimum_d_observations`.
Simulation uniquement. Samedi 14-11-2026.

LE SENS EN TÊTE — Deux fonctions de `programmes/MODULE_JUGEMENT.py` remplacent, dans les contrôles ④ et ⑤ de R-505, le
plancher fixe de 30 observations et la loi de Student (décisions de Jean-Luc du 14-11-2026, A-782 à 16h56 et A-786 à
17h08). Ces épreuves vérifient, vite, sur des cas dont on connaît la réponse : que le p de la vraie série des 100
opérations de C5 est celui mesuré le jour de la livraison (valeur figée, R-732) ; que le calcul est rejouable à
l'identique (graine fixe) ; que des stratégies sans talent ne passent presque jamais le seuil le plus strict là où
Student les fait passer ; que le nombre de tirages suffit au seuil ; que la grille appelle bien ces deux
fonctions ; que la grille ne valide ni une stratégie sans aucune perte (④ INCONNU, H8d) ni une période de moins de
5 blocs (⑤ INCONNU, H8e) ; que la limite des 5 blocs de 28 jours est tenue aux deux bords (H9) ; que les deux
branches de prudence d'un tirage comptent « aussi bien » (H10) ; qu'un gain nul n'est pas une perte (H7f) — ces
ajouts du tour 3 répondent à la relecture de Cowork du 14-11-2026 à 19h33 (C-1, C-2, m-1, m-2). Une
épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731) : `--saboter` casse le code de
chacune des façons de la table SABOTAGES (retour à Student, blocs d'un jour, pas de recentrage, graine variable,
tirages trop peu nombreux, plancher fixe de 30…) et chacune doit faire rougir au moins un cas. L'épreuve LONGUE de
calibrage (des milliers de mondes) est `programmes/CALIBRER_LE_HASARD_DES_GAINS.py`, lancée à la main.

USAGE : python3 -B tests/EPREUVES_DU_HASARD_DES_GAINS_Sam_14-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de sabotage
est introuvable, si le nom est inconnu ou si une donnée manque (R-734).

① RÔLE — Prouver que les deux fonctions font ce que dit leur texte, et que chaque garde a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque fichier
  de tests/ avec la racine, puis avec « --saboter ». Ce programme se relance en « --cas <copie> <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/MODULE_JUGEMENT.py`, `programmes/CONTRATS_DES_FICHIERS.py`,
  `programmes/COMMUN.py`, `gouvernance/REGISTRE_REGLES.md`, `donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv`.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier les trois programmes dans un dossier temporaire, appliquer le
  sabotage (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie · ③ Z0 doit être vert ; un
  sabotage doit faire rougir au moins un cas.
⑦ UNITÉ — Gains en EUROS ; durées en JOURS DE CALENDRIER ; probabilités sans unité.
⑧ POURQUOI — R-731 (sabotages), R-732 (un cas tiré d'une vraie ligne : H1, H8), R-734 (code non nul si un contrôle
  n'a pas pu tourner). Les valeurs figées de H1 ont été mesurées le 14-11-2026 sur la livraison : elles ne prouvent pas
  que le p est JUSTE (c'est le rôle de H3 et de l'épreuve de calibrage), elles prouvent qu'il n'a pas CHANGÉ ; un
  changement voulu du calcul se fait en changeant ces valeurs, et le dit.
⑨ CE QUI CLOCHE — ① H3 n'est qu'un calibrage éclair (1 000 mondes, une forme stylisée) : il attrape Student (dont
  le taux mesuré à 30 observations, au seuil 0,05 ÷ 69, est 15 fois le promis) mais pas un écart fin. ② Aucun cas
  n'atteint « p = seuil » exactement : le p dépend du seuil reçu (sa précision), l'égalité n'est pas atteignable ;
  « < » contre « ≤ » n'est donc pas éprouvé ici.
⑩ EFFET — Écrit et efface des dossiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 600 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""
import csv, datetime, importlib.util, json, os, random, shutil, subprocess, sys, tempfile

ICI = os.path.abspath(__file__)
MODULE = "programmes/MODULE_JUGEMENT.py"
VOISINS = ("programmes/CONTRATS_DES_FICHIERS.py", "programmes/COMMUN.py")
TABLEAU_C5 = "donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv"
# VALEURS FIGÉES le 14-11-2026 sur la livraison (vraie série des 100 opérations de C5) : voir l'en-tête, ⑧.
P_C5_SEUIL_DE_LA_LOI = 0.012791813239526703      # 40 tirages « aussi bien » sur 3 127, au seuil 0,05 ÷ 69
P_C5_SEUIL_005 = 0.012                           # 40 sur 3 333, au seuil 0,05
MINIMUM_C5_SEUIL_DE_LA_LOI = 15                  # q = 39 perdantes / 100 → ln(0,05 ÷ 69) ÷ ln(0,61) = 14,63 → 15 (A-782)

# LES SABOTAGES : (fichier, texte présent UNE fois, remplacement). Chacun retire ce qu'un cas teste.
SABOTAGES = {
    "H01_retour_a_student": [(MODULE, "    hasard = random.Random(graine)\n    au_hasard = hasard.random\n",
                              "    return 1.0 - loi_de_student_inferieure(m / (statistics.stdev(gains) / math.sqrt(n)), n - 1)\n"
                              "    hasard = random.Random(graine)\n    au_hasard = hasard.random\n")],
    "H02_blocs_d_un_jour": [(MODULE, "    longueur = longueur_des_blocs_jours or max(LONGUEUR_MINIMALE_DES_BLOCS_JOURS, max(tenues))",
                             "    longueur = 1")],
    "H03_pas_de_recentrage": [(MODULE, "        somme[j - j0] += g - m\n", "        somme[j - j0] += g\n")],
    "H04_graine_variable": [(MODULE, "    hasard = random.Random(graine)\n    au_hasard = hasard.random\n",
                             "    hasard = random.Random()\n    au_hasard = hasard.random\n")],
    "H05_tirages_trop_peu": [(MODULE, "math.ceil(DEPASSEMENTS_POUR_CONCLURE / seuil))", "math.ceil(1 / seuil))")],
    "H06_arret_au_premier": [(MODULE, "DEPASSEMENTS_POUR_CONCLURE = 40 ", "DEPASSEMENTS_POUR_CONCLURE = 1 ")],
    "H07_aussi_bien_a_l_envers": [(MODULE, "elif m_t / (math.sqrt(v_t) / n_t) >= t_observe:",
                                   "elif m_t / (math.sqrt(v_t) / n_t) <= t_observe:")],
    "H08_studentisation_naive": [(MODULE, "    t_observe = m / (math.sqrt(e2) / n)\n",
                                  "    t_observe = m / (statistics.stdev(gains) / math.sqrt(n))\n")],
    "H09_minimum_fixe_30": [(MODULE, "    return max(1, math.ceil(math.log(seuil) / math.log(1.0 - q)))", "    return 30")],
    # H10 : retour au q du tour 1 (« sous la moyenne »), moins strict que A-782 (relecteur neuf du 14-11, D2)
    "H10_q_sous_la_moyenne": [(MODULE, "    q = sum(1 for g in gains if g < 0.0) / len(gains)",
                               "    q = sum(1 for g in gains if g < math.fsum(gains) / len(gains)) / len(gains)")],
    "H11_grille_revient_a_student": [(MODULE, "            p_gain = probabilite_que_le_gain_soit_du_hasard(ops, s_preuve)",
                                      "            p_gain = probabilite_epoque_perdante([-x for x in gains], n_obs)"
                                      "[\"p_perdante\"]")],
    "H12_grille_plancher_fixe": [(MODULE, "plancher, r_plancher = minimum_d_observations([o[\"net\"] for o in ops], s_preuve), \"\"",
                                  "plancher, r_plancher = 30.0, \"\"")],
    "H13_periode_trop_courte_admise": [(MODULE, "    if D < BLOCS_MINIMUM * longueur:\n", "    if False:\n")],
    # H14 à H21 : tour 3, relecture Cowork du 14-11-2026 à 19h33 (C-1, C-2, m-1, m-2) — chacun retire ce qu'un cas
    # NOUVEAU tient, et chacun survivait aux 135 cas du tour 2 (sabotages R2, R3, R4, R7, R8, R9, R10 de Cowork)
    # C-1 : le refus du ④ (aucune perte → minimum infini) est avalé en « plancher 0 » ; tenu par H8d
    "H14_refus_du_4_avale": [(MODULE, "            except ValueError as ex:\n                r_plancher = str(ex)\n",
                              "            except ValueError as ex:\n                plancher, r_plancher = 0, \"\"\n")],
    # C-2 : la période trop courte devient un ⑤ PASSE à p = 0 au lieu d'INCONNU ; tenu par H8e
    "H15_5_inconnu_devient_passe": [(MODULE, "            c[\"gain_bat_zero\"] = _controle(\"INCONNU\", raison=\"p du gain "
                                     "non calculable : %s\" % ex)",
                                     "            p_gain = 0.0\n"
                                     "            c[\"gain_bat_zero\"] = _controle(\"PASSE\", valeur=0.0, seuil=s_preuve)")],
    # m-1 : la limite des 5 blocs et la longueur de 28 jours, dans les deux sens ; tenus par H9
    "H16_quatre_blocs_suffisent": [(MODULE, "BLOCS_MINIMUM = 5 ", "BLOCS_MINIMUM = 4 ")],
    "H17_six_blocs_exiges": [(MODULE, "BLOCS_MINIMUM = 5 ", "BLOCS_MINIMUM = 6 ")],
    "H18_blocs_de_21_jours": [(MODULE, "LONGUEUR_MINIMALE_DES_BLOCS_JOURS = 28 ", "LONGUEUR_MINIMALE_DES_BLOCS_JOURS = 21 ")],
    "H19_blocs_de_35_jours": [(MODULE, "LONGUEUR_MINIMALE_DES_BLOCS_JOURS = 28 ", "LONGUEUR_MINIMALE_DES_BLOCS_JOURS = 35 ")],
    # m-2 : les deux branches de prudence des tirages ne comptent plus « aussi bien » ; tenues par H10 et H10b
    "H20_moins_de_2_operations_non_compte": [(MODULE, "        if n_t < 2:\n            aussi_bien += 1\n",
                                              "        if n_t < 2:\n            aussi_bien += 0\n")],
    "H21_erreur_nulle_non_comptee": [(MODULE, "aussi_bien += m_t >= 0.0", "aussi_bien += 0")],
    # m-2, voisin : un gain net exactement nul compté comme une perte ; tenu par H7f
    "H22_gain_nul_compte_perdant": [(MODULE, "    q = sum(1 for g in gains if g < 0.0) / len(gains)",
                                     "    q = sum(1 for g in gains if g <= 0.0) / len(gains)")],
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


def ops_c5(racine):
    """Lit les 100 vraies opérations de C5 (tableau du 01-08-2026).
    ① RÔLE — Le cas tiré d'une vraie ligne (R-732). ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — la racine.
    ④ CONDITIONS D'ENTRÉE — le tableau existe. ⑤ SORTIE — UNE valeur : la liste des opérations. [rend: 1]
    ⑥ TRAITEMENT — lire `net_eur` (virgule décimale), `date_entree`, `date_sortie`. ⑦ UNITÉ — euros.
    ⑧ POURQUOI — la série sur laquelle A-781 et A-782 ont été mesurés. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit un fichier.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    with open(os.path.join(racine, TABLEAU_C5), encoding="utf-8") as f:
        return [{"net": float(r["net_eur"].replace(",", ".")), "date_entree": r["date_entree"],
                 "date_sortie": r["date_sortie"], "valeur": r["valeur"]} for r in csv.DictReader(f, delimiter=";")]


def ops_espacees(gains, pas=5, debut="2030-01-01", duree=2):
    """Fabrique des opérations qui ne se chevauchent pas, une tous les `pas` jours.
    ① RÔLE — Une série synthétique de vérité connue. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — gains, écart, départ, durée.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : les opérations. [rend: 1] ⑥ TRAITEMENT — entrée au jour i × pas.
    ⑦ UNITÉ — euros, jours. ⑧ POURQUOI — pas = 5 : 40 opérations couvrent 200 jours, au moins 5 blocs de 28 jours.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    d0 = datetime.date.fromisoformat(debut)
    return [{"net": float(g), "date_entree": (d0 + datetime.timedelta(days=i * pas)).isoformat(),
             "date_sortie": (d0 + datetime.timedelta(days=i * pas + duree - 1)).isoformat()} for i, g in enumerate(gains)]


def cas(copie, racine):
    """Joue tous les cas sur le module de la copie et rend leurs résultats.
    ① RÔLE — Les épreuves elles-mêmes. ② CONTEXTE D'APPEL — `main`, en « --cas ». ③ ENTRÉE — la copie, la racine.
    ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur : liste de [nom, vert, détail]. [rend: 1]
    ⑥ TRAITEMENT — H1 à H10, chacun enveloppé (une erreur = rouge). ⑦ UNITÉ — voir l'en-tête.
    ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    sys.path.insert(0, os.path.join(copie, "programmes"))
    J = charger(os.path.join(copie, MODULE), "MODULE_JUGEMENT")
    mots_du_verdict = charger(os.path.join(copie, VOISINS[0]), "CONTRATS_DES_FICHIERS").MOTS_DU_VERDICT
    res = []

    def ok(nom, cond, det=""):
        res.append([nom, bool(cond), str(det)[:300]])

    def essai(nom, f):
        try:
            f()
        except Exception as ex:      # une erreur est un rouge, jamais un silence
            res.append([nom, False, "%s: %s" % (type(ex).__name__, str(ex)[:200])])

    c5 = ops_c5(racine)
    loi = 0.05 / 69
    P = J.probabilite_que_le_gain_soit_du_hasard

    def h1():   # R-732 : la vraie série, valeurs figées
        p = P(c5, loi)
        ok("H1 vraie série de C5 (100 opérations), seuil 0,05 ÷ 69 : p = %r (figé le 14-11-2026)" % P_C5_SEUIL_DE_LA_LOI,
           p == P_C5_SEUIL_DE_LA_LOI, repr(p))
        p = P(c5, 0.05)
        ok("H1b même série, seuil 0,05 : p = %r" % P_C5_SEUIL_005, p == P_C5_SEUIL_005, repr(p))
        n = J.minimum_d_observations([o["net"] for o in c5], loi)
        ok("H1c minimum d'observations de C5 au seuil 0,05 ÷ 69 : 15 (A-782)", n == MINIMUM_C5_SEUIL_DE_LA_LOI, repr(n))
    essai("H1", h1)

    def h2():   # rejouable : même entrée, même p ; la graine sert
        a, b = P(c5, loi), P(c5, loi)
        autre = P(c5, loi, graine=7)
        ok("H2 deux appels identiques rendent le même p (graine fixe déclarée)", a == b, "%r %r" % (a, b))
        ok("H2b une autre graine rend un autre p (la graine est bien celle des tirages)", autre != a, "%r %r" % (a, autre))
    essai("H2", h2)

    def h3():   # calibrage éclair : sans talent, forme +1/-3 (gains autour de +1 000 €, pertes autour de −3 000 €),
        #         30 opérations (au-dessus du minimum de 26 que A-782 exige pour cette forme), seuil de la loi
        hasard = random.Random(20261114)
        faux = calcules = 0
        for k in range(1000):
            gains = [(1000.0 + hasard.uniform(-150, 150)) if hasard.random() < 0.75 else
                     (-3000.0 + hasard.uniform(-300, 300)) for _ in range(30)]      # moyenne vraie : 0 (symétries)
            jours = sorted(hasard.sample(range(900), 30))
            ops = [{"net": g, "date_entree": (datetime.date(2030, 1, 1) + datetime.timedelta(days=j)).isoformat(),
                    "date_sortie": (datetime.date(2030, 1, 1) + datetime.timedelta(days=j + 9)).isoformat()}
                   for g, j in zip(gains, jours)]
            try:
                p = P(ops, loi, graine=k)
            except ValueError:
                continue
            calcules += 1
            faux += p < loi
        # promis : 0,000725 × 1 000 = 0,7 ; Student à 30 observations : 1,09 % mesuré sur la vraie forme (TERMINER B.2),
        # soit environ 11 sur 1 000
        ok("H3 1 000 stratégies sans talent (+1/−3, 30 opérations) au seuil 0,05 ÷ 69 : au plus 4 faux gagnants "
           "(Student en ferait environ 11)", faux <= 4 and calcules >= 900, "%d faux sur %d calculés" % (faux, calcules))
    essai("H3", h3)

    def h4():   # le nombre de tirages suffit au seuil : sans aucun tirage « aussi bien », p = 1 ÷ (M + 1) ≤ seuil ÷ 40
        fort = [dict(o, net=o["net"] + 3000.0) for o in c5]
        for s in (0.05, 0.01, loi):
            p = P(fort, s)
            ok("H4 série écrasante, seuil %.6f : p = %.3g ≤ seuil ÷ 40 (au moins 40 ÷ seuil tirages)" % (s, p),
               p <= s / 40 * 1.0001, repr(p))
    essai("H4", h4)

    def h5():   # recentrage : une série au gain net franc a un p petit ; une série au gain moyen nul, un p grand
        g = [900] * 30 + [-300] * 10
        random.Random(3).shuffle(g)                  # gains mêlés, dates dans l'ordre
        franc = ops_espacees(g)
        p = P(franc, 0.05)
        # 40 opérations sur 200 jours, 7 blocs : le calcul est prudent à peu de blocs (fonction, ⑨ ③) ; mesuré 0,016
        ok("H5 gain franc (30 × +900, 10 × −300, 7 blocs) : p < 0,05", p < 0.05, repr(p))
        nul = ops_espacees([900, -900] * 20)
        p = P(nul, 0.05)
        ok("H5b gain moyen nul exactement : p > 0,2", p > 0.2, repr(p))
    essai("H5", h5)

    def h6():   # les blocs : 8 paquets de 5 opérations sur 5 jours voisins, de même signe — UN hasard par paquet
        gains, jours = [], []
        signe = [1, 1, 1, 1, 1, -1, 1, -1]
        for k, s in enumerate(signe):
            for i in range(5):
                gains.append(800.0 * s + 10 * i)
                jours.append(k * 30 + i)
        ops = [{"net": g, "date_entree": (datetime.date(2030, 1, 1) + datetime.timedelta(days=j)).isoformat(),
                "date_sortie": (datetime.date(2030, 1, 1) + datetime.timedelta(days=j)).isoformat()}
               for g, j in zip(gains, jours)]
        p_blocs, p_un_jour = P(ops, 0.05), P(ops, 0.05, longueur_des_blocs_jours=1)
        ok("H6 paquets liés : les blocs de 28 jours rendent un p au moins 3 fois plus grand que des blocs d'un jour",
           p_blocs >= 3 * p_un_jour, "%r contre %r" % (p_blocs, p_un_jour))
    essai("H6", h6)

    def h7():   # entrées refusées, période trop courte, minimum : q sous la MOYENNE
        refus = []
        for nom, args in (("1 opération", ([{"net": 1.0, "date_entree": "2030-01-01", "date_sortie": "2030-01-02"}], 0.05)),
                          ("seuil 0", (c5, 0.0)), ("seuil 1", (c5, 1.0)), ("seuil booléen", (c5, True)),
                          ("gain NaN", ([dict(c5[0], net=float("nan"))] + c5[1:], 0.05)),
                          ("date illisible", ([dict(c5[0], date_entree="01/02/2024")] + c5[1:], 0.05)),
                          ("sortie avant entrée", ([dict(c5[0], date_sortie="2020-01-01")] + c5[1:], 0.05)),
                          ("gains tous égaux", (ops_espacees([500] * 40), 0.05)),
                          ("période de 39 jours (moins de 5 blocs)", (ops_espacees([900, -300, 900] * 13, pas=1), 0.05)),
                          ("seuil 1e-6 (trop de tirages)", (c5, 1e-6))):
            try:
                P(*args)
                refus.append(nom)
            except ValueError:
                pass
        ok("H7 entrées hors de leur forme : ValueError, jamais un p", not refus, "acceptées : %s" % refus)
        # A-782 : q = part des opérations PERDANTES ; « sous la moyenne » (tour 1) donnerait q = 1/2 → 5
        n = J.minimum_d_observations([-50.0, 100.0, 200.0, 300.0], 0.05)
        ok("H7b minimum : 1 perdante sur 4 (q = 1/4, A-782) → ln(0,05) ÷ ln(0,75) = 10,41 → 11 (sous la moyenne : 5)",
           n == 11, repr(n))
        n = J.minimum_d_observations([o["net"] for o in c5], loi)
        ok("H7d C5 : 39 perdantes sur 100 → 15 ; et +1/−3 exact (q = 0,25) au seuil de la loi → 26, pas 25 (erratum)",
           n == 15 and J.minimum_d_observations([-3000.0] + [1000.0] * 3, loi) == 26, repr(n))
        try:
            J.minimum_d_observations([100.0, 200.0, 300.0], 0.05)
            ok("H7e minimum sans aucune opération perdante : refusé (infini)", False, "accepté")
        except ValueError:
            ok("H7e minimum sans aucune opération perdante : refusé (infini)", True)
        try:
            J.minimum_d_observations([7.0, 7.0, 7.0], 0.05)
            ok("H7c minimum sur des gains égaux : refusé", False, "accepté")
        except ValueError:
            ok("H7c minimum sur des gains égaux : refusé", True)
        # A-782 dit « perdantes » : un gain net exactement nul n'est pas une perte (q = 1/4 → 11) ; compté comme
        # perte, q = 2/4 → ln(0,05) ÷ ln(0,5) = 4,32 → 5 (relecture Cowork du 14-11-2026, m-2)
        n = J.minimum_d_observations([0.0, -50.0, 100.0, 200.0], 0.05)
        ok("H7f minimum : un gain exactement nul n'est pas une perte (q = 1/4 → 11 ; compté perdant : 5)",
           n == 11, repr(n))
    essai("H7", h7)

    def h8():   # la grille appelle les deux fonctions (vraie table de R-505, vraie série, k = 69)
        t = J.table_de_la_loi(open(os.path.join(racine, "gouvernance/REGISTRE_REGLES.md"), encoding="utf-8").read())
        r = J.grille_de_validation(t, "1", 69, ops=c5, point_mort_pct=43.1, declaration_manquants=[],
                                   seances_hors_examen=0, regards_anterieurs=[])
        c4, c5_ = r["controles"]["observations_independantes"], r["controles"]["gain_bat_zero"]
        ok("H8 grille, ⑤ : le p est celui de la fonction (%r), comparé au seuil 0,05 ÷ 69 → BLOQUE" % P_C5_SEUIL_DE_LA_LOI,
           c5_["valeur"] == P_C5_SEUIL_DE_LA_LOI and c5_["etat"] == "BLOQUE", "%r %s" % (c5_["valeur"], c5_["etat"]))
        ok("H8b grille, ④ : le minimum est calculé (15), pas 30 ; 52 observations retenues → PASSE",
           c4["seuil"] == MINIMUM_C5_SEUIL_DE_LA_LOI and c4["etat"] == "PASSE", "%r %r %s" % (c4["seuil"], c4["valeur"],
                                                                                         c4["etat"]))
        vingt = ops_espacees([900, 900, 900, -300] * 5)
        r = J.grille_de_validation(t, "1", 1, ops=vingt, point_mort_pct=40.0, declaration_manquants=[],
                                   seances_hors_examen=0, regards_anterieurs=[])
        c4 = r["controles"]["observations_independantes"]
        ok("H8c grille, ④ : 20 observations, q = 1/4, seuil 0,05 → minimum 11 → PASSE (le « 30 » aurait bloqué)",
           c4["seuil"] == 11 and c4["etat"] == "PASSE", "%r %s" % (c4["seuil"], c4["etat"]))
        # C-1 (relecture Cowork du 14-11-2026) : 40 opérations TOUTES gagnantes sur un an, k = 69. Le ⑤ PASSE (p minuscule,
        # 0,000018 mesuré par Cowork sur une série de cette forme) : seul le ④ empêche la validation, c'est le cas pour
        # lequel A-782 a créé le minimum. Le ④ doit être INCONNU (minimum infini) et être le premier contrôle qui bloque.
        gagnantes = ops_espacees([500.0 + (37 * i) % 400 for i in range(40)], pas=9)
        r = J.grille_de_validation(t, "1", 69, ops=gagnantes, point_mort_pct=40.0, declaration_manquants=[],
                                   seances_hors_examen=0, regards_anterieurs=[])
        c4, c5_ = r["controles"]["observations_independantes"], r["controles"]["gain_bat_zero"]
        ok("H8d grille, toutes gagnantes (40 sur un an, k = 69) : ⑤ PASSE mais ④ INCONNU (minimum infini), premier "
           "contrôle bloquant ④, jamais Validée",
           c5_["etat"] == "PASSE" and c4["etat"] == "INCONNU" and "aucune des 40" in c4["raison"]
           and r["premier_controle_bloquant"] == "observations_independantes" and r["verdict"] != mots_du_verdict[0],
           "⑤ %s %r · ④ %s %r · premier %r · %r" % (c5_["etat"], c5_["valeur"], c4["etat"], c4["raison"][:60],
                                                   r["premier_controle_bloquant"], r["verdict"]))
        # C-2 (relecture Cowork du 14-11-2026) : 39 opérations sur 39 jours, moins de 5 blocs de 28 jours, à travers la
        # GRILLE (H7 et H13 n'éprouvent que la fonction) : ⑤ INCONNU, jamais validée.
        courte = ops_espacees([900, -300, 900] * 13, pas=1)
        r = J.grille_de_validation(t, "1", 1, ops=courte, point_mort_pct=40.0, declaration_manquants=[],
                                   seances_hors_examen=0, regards_anterieurs=[])
        c5_ = r["controles"]["gain_bat_zero"]
        ok("H8e grille, période de 39 jours (moins de 5 blocs) : ⑤ INCONNU, jamais Validée",
           c5_["etat"] == "INCONNU" and "moins de 5 blocs" in c5_["raison"] and r["verdict"] != mots_du_verdict[0],
           "%s %r %r · %r" % (c5_["etat"], c5_.get("valeur"), c5_["raison"][:80], r["verdict"]))
    essai("H8", h8)

    def h9():   # m-1 : la limite des 5 blocs de 28 jours, aux deux bords. Détentions de 2 jours : la longueur des blocs est
        #         28 jours (la plus grande de 28 et de la plus longue détention). Période = dernier jour d'entrée − premier
        #         + 1. 140 jours = 5 × 28 : calculé ; 139 jours : refusé. Avec 4 blocs ou des blocs de 21 jours, 139 passe ;
        #         avec 6 blocs ou des blocs de 35 jours, 140 est refusé.
        # cinq gains qui se répètent sur 4 entrées par bloc : les sommes des blocs diffèrent (un motif de 4 les rendrait
        # toutes égales, incertitude nulle — vu au premier essai du 14-11-2026)
        gains = [900.0, -300.0, 750.0, 600.0, -200.0] * 4
        def periode(dernier):
            jours = list(range(0, 133, 7)) + [dernier]       # 19 entrées tous les 7 jours, puis la dernière
            d0 = datetime.date(2030, 1, 1)
            return [{"net": g, "date_entree": (d0 + datetime.timedelta(days=j)).isoformat(),
                     "date_sortie": (d0 + datetime.timedelta(days=j + 1)).isoformat()} for g, j in zip(gains, jours)]
        try:
            p = P(periode(139), 0.05)
            ok("H9 période de 140 jours, blocs de 28 jours (5 blocs tout juste) : p calculé", 0.0 < p <= 1.0, repr(p))
        except ValueError as ex:
            ok("H9 période de 140 jours, blocs de 28 jours (5 blocs tout juste) : p calculé", False, str(ex))
        try:
            p = P(periode(138), 0.05)
            ok("H9b période de 139 jours (moins de 5 blocs de 28 jours) : refusée", False, "accepté, p = %r" % p)
        except ValueError as ex:
            ok("H9b période de 139 jours (moins de 5 blocs de 28 jours) : refusée", "139 jours" in str(ex)
               and "blocs de 28 jours" in str(ex) and "moins de 5 blocs" in str(ex), str(ex))
    essai("H9", h9)

    def h10():  # m-2 : les deux branches de prudence d'un tirage (fonction, ⑥ ⑥) comptent comme « aussi bien ».
        d0 = datetime.date(2030, 1, 1)
        def ops_jours(gains, jours):
            return [{"net": float(g), "date_entree": (d0 + datetime.timedelta(days=j)).isoformat(),
                     "date_sortie": (d0 + datetime.timedelta(days=j + 1)).isoformat()} for g, j in zip(gains, jours)]
        # ① tirage de moins de 2 opérations : 3 opérations aux jours 0, 300, 600 ; période 601 jours, 22 blocs de 28.
        #   Un bloc contient une opération avec la probabilité 84 ÷ 601 (28 débuts par opération, aucune partagée).
        #   P(moins de 2 opérations tirées) = (517/601)^22 + 22 × (84/601) × (517/601)^21 = 0,167 : le p doit être au
        #   moins de cet ordre. Mesuré le 14-11-2026 : 0,296 ; sans la branche : 0,113.
        p = P(ops_jours([1000.0, 1100.0, -10.0], [0, 300, 600]), 0.05)
        ok("H10 3 opérations éparses : les tirages de moins de 2 opérations comptent « aussi bien » → p ≥ 0,15 "
           "(borne calculée 0,167)", p >= 0.15, repr(p))
        # ② erreur nulle : 40 opérations de +100 € tous les 5 jours (jours 0 à 195), une de −5 000 € au jour 400 ;
        #   période 401 jours, 15 blocs. Un tirage qui évite les 28 blocs contenant la perte ne voit que des +100 :
        #   erreur nulle, et gain recentré 100 − (−24,4) > 0 → « aussi bien ». P(l'éviter) = (373/401)^15 = 0,338.
        #   Mesuré le 14-11-2026 : 0,625 ; sans la branche : 0,268.
        p = P(ops_jours([100.0] * 40 + [-5000.0], list(range(0, 200, 5)) + [400]), 0.05)
        ok("H10b 40 gains identiques et une perte isolée : les tirages d'erreur nulle et de gain positif comptent "
           "« aussi bien » → p ≥ 0,33 (borne calculée 0,338)", p >= 0.33, repr(p))
    essai("H10", h10)
    return res


def preparer(racine, sab):
    """Copie le module et ses voisins, et applique un sabotage.
    ① RÔLE — Donner à chaque sabotage sa copie. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — la racine, le nom ou « Z0 ».
    ④ CONDITIONS D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — UNE valeur : le dossier. [rend: 1]
    ⑥ TRAITEMENT — copier, remplacer. ⑦ UNITÉ — —. ⑧ POURQUOI — une cible introuvable ne sabote rien : elle lève.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — crée un dossier temporaire. ⑪ TERMINAISON — rend la main ou lève LookupError.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="hasard_%s_" % sab)
    os.makedirs(os.path.join(d, "programmes"))
    for f in (MODULE,) + VOISINS:
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
        r = subprocess.run([sys.executable, "-B", ICI, "--cas", d, racine], capture_output=True, text=True, timeout=600)
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
    if len(argv) >= 4 and argv[1] == "--cas":
        print(json.dumps(cas(argv[2], argv[3]), ensure_ascii=False))
        return 0
    if len(argv) < 2:
        print(__doc__.split("USAGE")[1].split("①")[0].strip())
        return 2
    racine = os.path.abspath(argv[1])
    for f in (MODULE, TABLEAU_C5, "gouvernance/REGISTRE_REGLES.md") + VOISINS:
        if not os.path.exists(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            return 2
    demandes = []
    if len(argv) > 2:
        demandes = list(SABOTAGES) if argv[2] == "--saboter" else [argv[2]]
        if any(s not in SABOTAGES for s in demandes):
            print("SABOTAGE INCONNU : %s" % argv[2])
            return 2
    print("ÉPREUVES DU HASARD DES GAINS — racine : %s" % racine)
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
