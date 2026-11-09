"""ÉPREUVES DES ÉPOQUES — lot S_per (R-505 ⑦ et ⑪, n°58, n°79, n°80, n°197), jeudi 05-11-2026. Simulation uniquement.

LE SENS EN TÊTE — Cette épreuve dit si les six fonctions du lot S_per (`programmes/MODULE_JUGEMENT.py`) tiennent la
loi : ① le minimum d'époques gagnantes se calcule à la déclaration, sans aucun gain, et une stratégie dont l'avantage est
le même dans chaque époque et qui passe ⑤ n'est refusée par lui qu'au plus 5 fois sur 100 (propriété de n°58, E2) ;
② ce minimum n'est jamais un chiffre fixe (n°80, E1) ; ③ une époque est « perdante à coup sûr » par un test de Student
sur le nombre d'observations RETENU, à n retenu − 1 degrés (n°197, E4, E5, E12, E17) ; ④ le découpage vient de la déclaration et de nulle part
ailleurs (E6, E7) ; ⑤ le groupe témoin informe et ne décide jamais, quelle que soit la mesure où il est meilleur (n°79, E8,
E13) ; ⑥ ce qui ne se mesure pas rend INCONNU, ce qui sort du découpage rend NON JUGEABLE (E9, E10), et BLOQUE passe
avant INCONNU quand le refus est déjà certain (E15) ; ⑥bis une époque sans opération n'est jamais gagnante, et une
époque n'est gagnante que si son gain moyen est strictement positif (E14, E16) ; ⑦ une vraie ligne : les opérations de C5E10-QA-V1
rejouées par le juge, sur 2024-2026 SEULEMENT (E11, R-732). INTERDIT ici : jouer ⑦ sur C5 en 2000-2023 (ce serait le
regard unique de R-505 ③).

USAGE : python3 -B tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py <racine> [--saboter | nom]
  sans option : Z0, le dépôt tel quel ; --saboter : Z0 puis chaque sabotage ; un nom : Z0 puis celui-là.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage n'est pas trouvée exactement une fois, si le nom demandé n'existe pas ou si la préparation (rejeu de
C5E10-QA-V1 par le juge, calendrier) n'a pas pu tourner (R-734).

① RÔLE — Éprouver les six fonctions des époques à vérité connue et sur de vraies opérations, et prouver que chaque
  épreuve rougit quand on retire ce qu'elle teste (R-731).
② CONTEXTE D'APPEL — À la main. Ce programme se relance lui-même en mode « --cas » sur chaque copie du module.
③ ENTRÉE — La racine du dépôt ; `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/MODULE_JUGEMENT.py`, `programmes/JUGE_DES_STRATEGIES.py` et ce
  qu'il lit pour jouer une fiche, `programmes/CALENDRIER_DE_LA_BOURSE.py` et ses deux fichiers.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage. [rend: 1]
⑥ TRAITEMENT — ① préparer UNE fois, sur la racine intacte : les opérations de C5E10-QA-V1 que rend le juge (sa
  fonction `juger` est remplacée par une prise qui garde les opérations et arrête) et les séances du calendrier de
  2024-01-02 à 2026-07-10 ; les écrire dans un JSON temporaire · ② pour Z0 puis chaque sabotage : copier le module dans
  un dossier temporaire, appliquer le sabotage (un texte qui doit y être une fois), relancer ce programme en « --cas »
  · ③ Z0 doit être vert, chaque sabotage doit faire rougir un cas.
⑦ UNITÉ — Des époques, des opérations, des observations, des probabilités, des euros.
⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731). Les vérités
  d'E1 et E2 viennent de l'étalonnage du superviseur R-759 du 05-11-2026 (lot S_per, §2), fait par un autre programme
  (numpy, scipy) avant cette épreuve ; E4 vient des tables de Student.
⑨ CE QUI CLOCHE — ① E1 attend 3 pour « 5 époques égales, k = 69 » et non 4 comme le §4 du superviseur : son essai
  prenait le quantile de Student à 399 degrés, la consigne dit z (loi normale) ; z donne un minimum plus petit ou
  égal, donc du côté où la propriété tient (déclaré au RAPPORT). ② Les sabotages ne portent que sur le module copié ;
  le rejeu de QA-V1 est fait une fois sur le dépôt intact. ③ E2 simule ⑤ avec l'écart-type connu (σ = 1), pas estimé.
⑩ EFFET — Écrit et efface des dossiers temporaires ; ne touche pas au dépôt.
⑪ TERMINAISON — Chaque relance a un délai de 600 s. [sort: oui — code de sortie]
"""
import ast
import contextlib
import datetime
import importlib.util
import io
import json
import math
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import tempfile

ICI = os.path.abspath(__file__)
MODULE = "programmes/MODULE_JUGEMENT.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
CALENDRIER = "programmes/CALENDRIER_DE_LA_BOURSE.py"
FICHE_REELLE, PERIODE_REELLE = "C5E10-QA-V1", ("2024-01-02", "2026-07-10")
K_ILLUSTRATIF = 69            # k du relevé n°192, repris par le superviseur (§2) : illustratif, pas le k de C5
SEUIL_EPOQUE = 0.05           # la clé epoque_perdante de la table de R-505, recopiée pour l'épreuve seulement
NOUVELLES = ("lire_les_epoques", "loi_de_student_inferieure", "probabilite_epoque_perdante",
             "minimum_d_epoques_gagnantes", "controle_des_epoques", "afficher_le_groupe_temoin")
LITTERAUX_PERMIS = {0, 1, 2, 0.5, 100}   # constantes des formules et plafond d'itérations, nommés dans les fonctions
PROPOSEES = "2000-01-03..2007-12-31 ; 2008-01-02..2012-12-31 ; 2013-01-02..2019-12-31 ; 2020-01-02..2023-12-29"

SABOTAGES = [
    ("S1_minimum_fixe_a_2", "E1",
     "        minimum = m\n    return {\"minimum\": minimum,",
     "        minimum = m\n    minimum = 2\n    return {\"minimum\": minimum,"),
    ("S2_minimum_fixe_a_3", "E1",
     "        minimum = m\n    return {\"minimum\": minimum,",
     "        minimum = m\n    minimum = 3\n    return {\"minimum\": minimum,"),
    ("S3_minimum_egal_au_nombre_d_epoques", "E2",
     "        minimum = m\n    return {\"minimum\": minimum,",
     "        minimum = m\n    minimum = len(parts)\n    return {\"minimum\": minimum,"),
    ("S4_minimum_sur_le_gain_regarde", "E3",
     "    minimum = minimum_d_epoques_gagnantes(parts, seuil_de_preuve, seuil_epoque)[\"minimum\"]",
     "    _g = [o[\"net\"] for o in ops]\n"
     "    _p = 1 - __import__(\"statistics\").NormalDist().cdf(__import__(\"statistics\").mean(_g) / "
     "__import__(\"statistics\").stdev(_g) * len(_g) ** 0.5)\n"
     "    minimum = minimum_d_epoques_gagnantes(parts, min(0.5, max(1e-12, _p)), seuil_epoque)[\"minimum\"]"),
    ("S5_loi_normale_au_lieu_de_Student", "E4",
     "    return 0.5 * i_x if t < 0 else 1 - 0.5 * i_x",
     "    return __import__(\"statistics\").NormalDist().cdf(t)"),
    ("S6_n_operations_au_lieu_du_nombre_retenu", "E5",
     "                proba = probabilite_epoque_perdante(gains, n_retenu)",
     "                proba = probabilite_epoque_perdante(gains, len(gains))"),
    ("S7_epoques_en_repli_dans_le_code", "E6 E7",
     "    if not isinstance(texte, str) or not texte.strip():\n        rendu[\"motif\"]",
     "    if not isinstance(texte, str) or not texte.strip():\n        texte = \"" + PROPOSEES + "\"\n"
     "    if False:\n        rendu[\"motif\"]"),
    ("S8_seuil_en_defaut", "E7",
     "def controle_des_epoques(ops, epoques, parts_des_seances, seuil_de_preuve, seuil_epoque):",
     "def controle_des_epoques(ops, epoques, parts_des_seances, seuil_de_preuve, seuil_epoque=0.05):"),
    ("S9_le_temoin_decide", "E8",
     "    rendu[\"valeur\"] = resumes[(\"groupe_temoin\", \"tout\")][\"gain_moyen_eur\"]\n    rendu[\"etat\"] = \"PASSE\"",
     "    rendu[\"valeur\"] = resumes[(\"groupe_temoin\", \"tout\")][\"gain_moyen_eur\"]\n"
     "    rendu[\"etat\"] = (\"BLOQUE\" if rendu[\"valeur\"] is not None and rendu[\"valeur\"] > "
     "(resumes[(\"strategie\", \"tout\")][\"gain_moyen_eur\"] or 0) else \"PASSE\")"),
    ("S10_PASSE_au_lieu_d_INCONNU", "E9",
     "        rendu[\"etat\"] = \"INCONNU\"\n        rendu[\"raison\"] = \"MESURE MANQUANTE — \"",
     "        rendu[\"etat\"] = \"PASSE\"\n        rendu[\"raison\"] = \"MESURE MANQUANTE — \""),
    ("S11_operation_hors_epoque_ecartee", "E10",
     "            hors.append(\"operation n°%d (%s, achat %s)\" % (i, o.get(\"valeur\", \"?\"), d))\n            continue",
     "            continue"),
    ("S12_perdante_jamais_vue", "E12",
     "                    if proba[\"p_perdante\"] < seuil_epoque:",
     "                    if proba[\"p_perdante\"] < 0:"),
    ("S13_chevauchement_accepte", "E6",
     "        if suivante[0] <= precedente[1]:",
     "        if False:"),
    ("S14_le_temoin_decide_par_la_part_gagnante_d_une_epoque", "E13",
     "    rendu[\"valeur\"] = resumes[(\"groupe_temoin\", \"tout\")][\"gain_moyen_eur\"]\n    rendu[\"etat\"] = \"PASSE\"",
     "    rendu[\"valeur\"] = resumes[(\"groupe_temoin\", \"tout\")][\"gain_moyen_eur\"]\n"
     "    rendu[\"etat\"] = \"BLOQUE\" if any((e[\"groupe_temoin\"][\"part_gagnante\"] or 0) > "
     "(e[\"strategie\"][\"part_gagnante\"] or 0) for e in rendu[\"detail\"][\"par_epoque\"]) else \"PASSE\""),
    ("S15_epoque_vide_comptee_gagnante", "E14",
     "        lignes.append(ligne)\n    gagnantes",
     "        ligne[\"gagnante\"] = ligne[\"gagnante\"] or not ops_e\n        lignes.append(ligne)\n    gagnantes"),
    ("S16_INCONNU_avant_BLOQUE", "E15",
     "    if raisons:\n        rendu[\"etat\"] = \"BLOQUE\"",
     "    if raisons and not inconnues:\n        rendu[\"etat\"] = \"BLOQUE\""),
    ("S17_gagnante_si_gain_nul", "E16",
     "            ligne[\"gagnante\"] = ligne[\"gain_moyen_eur\"] > 0",
     "            ligne[\"gagnante\"] = ligne[\"gain_moyen_eur\"] >= 0"),
    ("S18_ddl_egal_n_retenu", "E17",
     "    ddl = n_retenu - 1\n",
     "    ddl = n_retenu\n"),
]


def charger(chemin, nom):
    """Charge un fichier Python comme module.

    ① RÔLE — Importer un programme par son chemin. ② CONTEXTE D'APPEL — `preparer`, `cas`. ③ ENTRÉE — le chemin, un nom.
    ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — le module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — —
    ⑧ POURQUOI — les noms de fichiers ne sont pas des noms de modules. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — exécute le code du fichier. ⑪ TERMINAISON — rend la main ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def preparer(racine, sortie):
    """Rejoue C5E10-QA-V1 par le juge et lit les séances du calendrier ; écrit le tout en JSON.

    ① RÔLE — Fournir à E11 une VRAIE ligne (R-732) : les opérations que le juge produit pour la fiche, et les séances de
    sa période. ② CONTEXTE D'APPEL — `main`, une fois. ③ ENTRÉE — la racine, le chemin du JSON. ④ CONDITIONS D'ENTRÉE —
    le juge et le calendrier se chargent. ⑤ SORTIE — le nombre d'opérations prises. [rend: 1] ⑥ TRAITEMENT — remplacer
    `juger` du juge chargé par une prise qui garde les opérations puis lève ; lancer `main` du juge sur la fiche, sortie
    écran avalée ; lire les séances par `lire_les_seances` et `seances_entre`. ⑦ UNITÉ — opérations, séances.
    ⑧ POURQUOI — les opérations doivent être celles du juge, pas une recopie. ⑨ CE QUI CLOCHE — `main` du juge fait aussi
    son calibrage (quelques secondes). ⑩ EFFET — écrit le JSON. ⑪ TERMINAISON — rend la main ou lève. [sort: non]
    """
    juge = charger(os.path.join(racine, JUGE), "juge_epoques")
    pris = {}

    class Prise(Exception):
        """Arrête le juge après la prise.

        ① RÔLE — signal d'arrêt. ② CONTEXTE D'APPEL — `prise`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — —
        ⑥ TRAITEMENT — — ⑦ UNITÉ — — ⑧ POURQUOI — ne pas juger : seules les opérations servent. ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — — ⑪ TERMINAISON — —
        """

    def prise(fiche, ops, *a, **k):
        """Garde les opérations de la fiche et arrête.

        ① RÔLE — remplacer `juger`. ② CONTEXTE D'APPEL — `main` du juge. ③ ENTRÉE — la fiche, les opérations.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — aucune : lève. [rend: 0] ⑥ TRAITEMENT — copier les cases lues.
        ⑦ UNITÉ — euros. ⑧ POURQUOI — éviter le reste du jugement. ⑨ CE QUI CLOCHE — — ⑩ EFFET — remplit `pris`.
        ⑪ TERMINAISON — lève Prise. [sort: non]
        """
        pris["ops"] = [{c: o.get(c) for c in ("valeur", "date_signal", "date_entree", "date_sortie", "net")}
                       for o in ops]
        raise Prise()
    juge.juger = prise
    argv = sys.argv
    sys.argv = [JUGE, racine, FICHE_REELLE]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                juge.main()
            except SystemExit:
                pass
    finally:
        sys.argv = argv
    if not pris.get("ops"):
        raise RuntimeError("le juge n'a rendu aucune opération pour %s" % FICHE_REELLE)
    cal = charger(os.path.join(racine, CALENDRIER), "calendrier_epoques")
    sc = cal.lire_les_seances(racine)
    seances = [d.isoformat() for d, _ in cal.seances_entre(datetime.date.fromisoformat(PERIODE_REELLE[0]),
                                                           datetime.date.fromisoformat(PERIODE_REELLE[1]), sc)]
    json.dump({"ops": pris["ops"], "seances": seances}, open(sortie, "w", encoding="utf-8"))
    return len(pris["ops"])


def fabriquer(epoques, gains_par_epoque, pas=2):
    """Fabrique des opérations d'un jour, disjointes, dans chaque époque.

    ① RÔLE — Construire des cas à vérité connue. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — les époques ({debut, fin}),
    une liste de gains par époque, l'écart en jours entre deux opérations. ④ CONDITIONS D'ENTRÉE — l'époque est assez
    longue. ⑤ SORTIE — la liste des opérations. [rend: 1] ⑥ TRAITEMENT — l'opération j de l'époque e est achetée et
    revendue le jour début + pas × j. ⑦ UNITÉ — euros, jours. ⑧ POURQUOI — positions jamais simultanées : K = n, la
    mesure ne mord pas. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
    """
    ops = []
    for ep, gains in zip(epoques, gains_par_epoque):
        d0 = datetime.date.fromisoformat(ep["debut"])
        for j, g in enumerate(gains):
            d = (d0 + datetime.timedelta(days=pas * j)).isoformat()
            assert d <= ep["fin"], (ep, j)
            ops.append({"valeur": "V%d" % j, "date_entree": d, "date_sortie": d, "net": float(g)})
    return ops


def jours_ouvres(debut, fin):
    """Rend les jours du lundi au vendredi entre deux dates, 1er janvier exclu.

    ① RÔLE — Un calendrier synthétique pour E6. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — deux textes AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — une liste de dates. [rend: 1] ⑥ TRAITEMENT — jour par jour. ⑦ UNITÉ — séances.
    ⑧ POURQUOI — le 1er janvier fermé prouve qu'un trou se compte en séances. ⑨ CE QUI CLOCHE — les autres fériés sont
    ignorés : sans effet sur les cas. ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
    """
    d, fin_d, out = datetime.date.fromisoformat(debut), datetime.date.fromisoformat(fin), []
    while d <= fin_d:
        if d.weekday() < 5 and not (d.month == 1 and d.day == 1):
            out.append(d)
        d += datetime.timedelta(days=1)
    return out


def cas(chemin_module, chemin_donnees):
    """Joue les cas E1 à E17 sur une copie du module et rend la liste (nom, vert, détail).

    ① RÔLE — Les cas (E13 à E17 ajoutés au tour 2, relecture S_per t1). ② CONTEXTE D'APPEL — le mode « --cas », une fois par copie. ③ ENTRÉE — le module copié, le JSON
    de `preparer`. ④ CONDITIONS D'ENTRÉE — le module se charge. ⑤ SORTIE — une liste de triplets. [rend: 1]
    ⑥ TRAITEMENT — un bloc par cas ; une exception rend le cas ROUGE avec son message. ⑦ UNITÉ — voir chaque cas.
    ⑧ POURQUOI — VÉRITÉS : E1, étalonnage du superviseur (§2 ; 5 égales : 3, voir ⑨ ① du programme) ; E2, la propriété de
    n°58 par 4 000 mondes simulés à μ = μ* (graine 20261105), refus ≤ 0,05 ; E4, tables de Student (t 0,95 à 10 ddl
    1,812 ; à 1 ddl 6,314 ; loi normale 1,645) ; E5, 20 opérations en 4 paquets de 5 ouverts ensemble : K = 4, donc
    n retenu 4 ; E12, une époque de 30 pertes certaines. ⑨ CE QUI CLOCHE — les bornes d'épreuve (10⁻³ en E4, 0,05 en
    E2) sont des bornes d'épreuve, pas des seuils de la loi. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    m = charger(chemin_module, "module_jugement_epoques")
    donnees = json.load(open(chemin_donnees, encoding="utf-8"))
    res = []
    s69 = 0.05 / K_ILLUSTRATIF
    quatre = [{"debut": a, "fin": b} for a, b in (p.strip().split("..") for p in PROPOSEES.split(";"))]
    parts_ans = [8 / 24, 5 / 24, 7 / 24, 4 / 24]
    blocs = []

    # E1 — le minimum n'est pas un chiffre fixe
    def e1():
        """① RÔLE — E1. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — comparer aux valeurs du superviseur. ⑦ UNITÉ — époques. ⑧ POURQUOI — n°80.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        attendus = [(parts_ans, 69, 3), ([0.2] * 5, 69, 3), ([1 / 3] * 3, 69, 2), ([1 / 3] * 3, 1, 1),
                    ([0.1] * 10, 69, 6), ([0.1] * 10, 500, 7)]
        rendus = [m.minimum_d_epoques_gagnantes(p, 0.05 / k, SEUIL_EPOQUE)["minimum"] for p, k, _ in attendus]
        return (rendus == [a for _, _, a in attendus],
                "rendus %s, attendus %s (8/5/7/4 k=69 ; 5 égales ; 3 égales ; 3 égales k=1 ; 10 égales ; 10 égales "
                "k=500)" % (rendus, [a for _, _, a in attendus]))
    blocs.append(("E1 minimum calculé (n°80), jamais fixe", e1))

    def e2():
        """① RÔLE — E2, la propriété de n°58. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — (vert, détail). [rend: 2] ⑥ TRAITEMENT — 4 000 mondes : moyenne de chaque époque ~ N(μ*, 1/√n_e),
        ⑤ = z-test global unilatéral à 0,05/69 ; refus = passe ⑤ et gagnantes < minimum. ⑦ UNITÉ — écart-type d'une
        opération. ⑧ POURQUOI — n°58. ⑨ CE QUI CLOCHE — σ connu. ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        n_e = (148, 92, 130, 74)
        total = sum(n_e)
        minimum = m.minimum_d_epoques_gagnantes([n / total for n in n_e], s69, SEUIL_EPOQUE)["minimum"]
        z5 = statistics.NormalDist().inv_cdf(1 - s69)
        mu = z5 / math.sqrt(total)
        hasard = random.Random(20261105)
        passent = refuses = 0
        for _ in range(4000):
            moy = [mu + hasard.gauss(0, 1) / math.sqrt(n) for n in n_e]
            globale = sum(a * n for a, n in zip(moy, n_e)) / total
            if globale * math.sqrt(total) > z5:
                passent += 1
                if sum(1 for a in moy if a > 0) < minimum:
                    refuses += 1
        taux = refuses / passent
        return (taux <= 0.05 and passent > 1000,
                "minimum %d ; %d mondes passent ⑤ sur 4000 ; refusés par le minimum : %d, soit %.4f (borne 0,05)"
                % (minimum, passent, refuses, taux))
    blocs.append(("E2 propriété n°58 (homogène, passe ⑤ → refus ≤ 5 %)", e2))

    def e3():
        """① RÔLE — E3. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — signature ; deux jeux de gains, mêmes dates, même minimum. ⑦ UNITÉ — époques.
        ⑧ POURQUOI — avant le regard. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        import inspect
        params = list(inspect.signature(m.minimum_d_epoques_gagnantes).parameters)
        fort = fabriquer(quatre, [[3000 + 37 * j for j in range(12)]] * 4)
        faible = fabriquer(quatre, [[(-1) ** j * 2000 + 40 for j in range(12)]] * 4)
        r1 = m.controle_des_epoques(fort, quatre, parts_ans, s69, SEUIL_EPOQUE)
        r2 = m.controle_des_epoques(faible, quatre, parts_ans, s69, SEUIL_EPOQUE)
        attendu = m.minimum_d_epoques_gagnantes(parts_ans, s69, SEUIL_EPOQUE)["minimum"]
        return (params == ["parts_des_seances", "seuil_de_preuve", "seuil_epoque"] and r1["seuil"] == r2["seuil"]
                == attendu, "paramètres %s ; minimum gains forts %s, gains faibles %s, attendu %s"
                % (params, r1["seuil"], r2["seuil"], attendu))
    blocs.append(("E3 le minimum ne lit aucun gain", e3))

    def e4():
        """① RÔLE — E4. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — trois valeurs de table et une symétrie. ⑦ UNITÉ — probabilités. ⑧ POURQUOI — Student.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        f = m.loi_de_student_inferieure
        v = [f(-1.812, 10), f(-6.314, 1), f(-1.645, 10 ** 6)]
        sym = f(2.0, 3.5) + f(-2.0, 3.5)
        return (all(abs(x - 0.05) < 1e-3 for x in v) and abs(sym - 1) < 1e-12,
                "F(-1,812;10)=%.5f F(-6,314;1)=%.5f F(-1,645;10^6)=%.5f ; F(2)+F(-2) à 3,5 ddl = %.12f" % (*v, sym))
    blocs.append(("E4 loi de Student (tables)", e4))

    def e5():
        """① RÔLE — E5, n°197. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert,
        détail). [rend: 2] ⑥ TRAITEMENT — 4 paquets de 5 positions ouvertes ensemble. ⑦ UNITÉ — observations.
        ⑧ POURQUOI — compter les opérations ferait une époque perdante. ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
        ⑪ TERMINAISON — rend la main. [sort: non]
        """
        ecarts = [-900, -300, 100, 500, 900]
        ops = []
        for p in range(4):
            d_in = datetime.date(2020, 3, 2) + datetime.timedelta(days=10 * p)
            for j, e in enumerate(ecarts):
                ops.append({"valeur": "P%dV%d" % (p, j), "date_entree": d_in.isoformat(),
                            "date_sortie": (d_in + datetime.timedelta(days=3)).isoformat(),
                            "net": -420.0 + e + 37 * p})
        une = [{"debut": "2020-01-02", "fin": "2020-12-31"}]
        r = m.controle_des_epoques(ops, une, [1.0], s69, SEUIL_EPOQUE)
        ep = r["detail"]["epoques"][0]
        p20 = m.probabilite_epoque_perdante([o["net"] for o in ops], 20)["p_perdante"]
        return (ep["observations_retenues"] == 4 and ep["p_perdante"] >= SEUIL_EPOQUE and p20 < SEUIL_EPOQUE
                and "perdante à coup sûr" not in r["raison"],
                "observations retenues %s ; p à n retenu %.4f ; p si l'on comptait 20 opérations %.4f ; raison : %s"
                % (ep["observations_retenues"], ep["p_perdante"], p20, r["raison"]))
    blocs.append(("E5 n°197 : n retenu, pas le nombre d'opérations", e5))

    def e6():
        """① RÔLE — E6. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — vide, chevauchement, trou, débordement, illisible, années illisibles, et le bon cas.
        ⑦ UNITÉ — séances. ⑧ POURQUOI — R-505 ⑦, découpage déclaré. ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
        ⑪ TERMINAISON — rend la main. [sort: non]
        """
        sc = jours_ouvres("2000-01-03", "2023-12-29")
        ex = "2000-01-03..2023-12-29"
        mauvais = {"vide": "", "blancs": "   ",
                   "chevauchement": "2000-01-03..2010-12-31 ; 2008-01-02..2023-12-29",
                   "trou": "2000-01-03..2007-12-31 ; 2009-01-02..2023-12-29",
                   "debordement": "1999-01-04..2007-12-31 ; 2008-01-02..2023-12-29",
                   "illisible": "2000-01-03-2007-12-31 ; 2008-01-02..2023-12-29"}
        motifs = {k: m.lire_les_epoques(v, ex, sc)["motif"] for k, v in mauvais.items()}
        mots = {"chevauchement": "chevauchement", "trou": "trou", "debordement": "débordement", "vide": "vide",
                "blancs": "vide", "illisible": "illisible"}
        bons_motifs = all(mt and mt.startswith("NON JUGEABLE — epoques :") and mots[k] in mt
                          for k, mt in motifs.items())
        annees = m.lire_les_epoques(PROPOSEES, "2000-01-03", sc)["motif"]
        bon = m.lire_les_epoques(PROPOSEES, ex, sc)
        sans = m.controle_des_epoques([], None, [], s69, SEUIL_EPOQUE)
        ok = (bons_motifs and annees and annees.startswith("NON JUGEABLE — annees_d_examen") and bon["motif"] is None
              and len(bon["epoques"]) == 4 and abs(sum(bon["parts_des_seances"]) - 1) < 1e-12
              and sans["etat"] == "INCONNU" and sans["raison"].startswith("NON JUGEABLE — epoques"))
        return ok, "motifs %s ; années illisibles : %s ; bon cas : %s époques, séances %s ; sans époque : %s, %s" % (
            {k: (v or "")[:40] for k, v in motifs.items()}, (annees or "")[:40],
            len(bon["epoques"] or []), [e["seances"] for e in bon["epoques"] or []], sans["etat"], sans["raison"][:40])
    blocs.append(("E6 époques déclarées : défauts → NON JUGEABLE", e6))

    def e7():
        """① RÔLE — E7. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — arbre syntaxique des six fonctions, textes d'explication retirés : aucun texte à quatre
        chiffres, aucun nombre hors LITTERAUX_PERMIS, aucun argument par défaut. ⑦ UNITÉ — — ⑧ POURQUOI — aucun seuil ni
        date dans le code. ⑨ CE QUI CLOCHE — un seuil passé par un calcul détourné (0.1 / 2) échapperait ; la relecture
        le voit. ⑩ EFFET — lit le module. ⑪ TERMINAISON — rend la main. [sort: non]
        """
        arbre = ast.parse(open(chemin_module, encoding="utf-8").read())
        fautes, vues = [], set()
        for n in arbre.body:
            if isinstance(n, ast.FunctionDef) and n.name in NOUVELLES:
                vues.add(n.name)
                if n.args.defaults or any(d is not None for d in n.args.kw_defaults):
                    fautes.append("%s : argument par défaut" % n.name)
                corps = n.body[1:] if (n.body and isinstance(n.body[0], ast.Expr)
                                      and isinstance(n.body[0].value, ast.Constant)) else n.body
                for noeud in ast.walk(ast.Module(body=corps, type_ignores=[])):
                    if isinstance(noeud, ast.Constant):
                        v = noeud.value
                        if isinstance(v, str) and re.search(r"\d{4}", v):
                            fautes.append("%s : texte daté %r" % (n.name, v[:30]))
                        elif isinstance(v, (int, float)) and not isinstance(v, bool) and v not in LITTERAUX_PERMIS:
                            fautes.append("%s : nombre %r" % (n.name, v))
        manquent = set(NOUVELLES) - vues
        return (not fautes and not manquent, "fautes %s ; fonctions absentes %s" % (fautes[:4], sorted(manquent)))
    blocs.append(("E7 ni date, ni seuil, ni défaut dans le code", e7))

    def e8():
        """① RÔLE — E8, n°79. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert,
        détail). [rend: 2] ⑥ TRAITEMENT — témoin bien meilleur, puis bien pire, puis absent. ⑦ UNITÉ — euros.
        ⑧ POURQUOI — le témoin informe. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        import inspect
        strat = fabriquer(quatre, [[800 + 11 * j for j in range(10)]] * 4)
        mieux = fabriquer(quatre, [[5000 + j for j in range(10)]] * 4)
        pire = fabriquer(quatre, [[-5000 - j for j in range(10)]] * 4)
        r1 = m.afficher_le_groupe_temoin(strat, mieux, quatre)
        r2 = m.afficher_le_groupe_temoin(strat, pire, quatre)
        r0 = m.afficher_le_groupe_temoin(strat, None, quatre)
        c = m.controle_des_epoques(strat, quatre, parts_ans, s69, SEUIL_EPOQUE)
        sans_temoin = not any("temoin" in p for p in inspect.signature(m.controle_des_epoques).parameters)
        ok = (r1["role"] == r2["role"] == r0["role"] == "AFFICHAGE" and r1["etat"] == r2["etat"] == "PASSE"
              and r0["etat"] == "INCONNU" and "I-8" in r0["raison"] and sans_temoin
              and len(r1["detail"]["par_epoque"]) == 4 and r1["valeur"] > 0 > r2["valeur"])
        return ok, "meilleur : %s %s ; pire : %s %s ; absent : %s « %s » ; ⑦ : %s (le témoin n'entre pas) ; " \
                   "signature de ⑦ sans témoin : %s" % (r1["etat"], r1["role"], r2["etat"], r2["role"], r0["etat"],
                                                         r0["raison"][:45], c["etat"], sans_temoin)
    blocs.append(("E8 le groupe témoin informe, ne décide pas", e8))

    def e9():
        """① RÔLE — E9. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — trois époques ; la première a un défaut de mesure. ⑦ UNITÉ — — ⑧ POURQUOI — R-734.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        trois = [{"debut": "2010-01-04", "fin": "2010-12-31"}, {"debut": "2011-01-03", "fin": "2011-12-30"},
                 {"debut": "2012-01-02", "fin": "2012-12-31"}]
        bons = [[900 + 13 * j for j in range(8)]] * 2
        variantes = {"une_operation": fabriquer(trois, [[700]] + bons),
                     "ecart_type_nul": fabriquer(trois, [[700] * 5] + bons),
                     "mesure_inconnue": fabriquer(trois, [[700 + j for j in range(5)]] + bons)}
        variantes["mesure_inconnue"][0]["date_sortie"] = "2010-13-45"
        etats = {}
        for nom, ops in variantes.items():
            r = m.controle_des_epoques(ops, trois, [1 / 3] * 3, 0.05, SEUIL_EPOQUE)
            etats[nom] = (r["etat"], "2010-01-04" in r["raison"])
        directs = [m.probabilite_epoque_perdante([1.0, 2.0], None)["motif"],
                   m.probabilite_epoque_perdante([1.0, 2.0], 1.5)["motif"],
                   m.probabilite_epoque_perdante([5.0, 5.0, 5.0], 3)["motif"]]
        ok = all(e == ("INCONNU", True) for e in etats.values()) and all(directs)
        return ok, "contrôle %s ; directs %s" % (etats, [d[:30] for d in directs])
    blocs.append(("E9 mesure impossible → INCONNU qui nomme l'époque", e9))

    def e10():
        """① RÔLE — E10. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — une opération achetée hors des époques. ⑦ UNITÉ — — ⑧ POURQUOI — rien en silence.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        ops = fabriquer(quatre, [[900 + 7 * j for j in range(10)]] * 4)
        ops.append({"valeur": "HORS", "date_entree": "2024-03-01", "date_sortie": "2024-03-05", "net": 50.0})
        r = m.controle_des_epoques(ops, quatre, parts_ans, s69, SEUIL_EPOQUE)
        return (r["etat"] == "INCONNU" and r["raison"].startswith("NON JUGEABLE — epoques") and "HORS" in r["raison"],
                "%s : %s" % (r["etat"], r["raison"][:110]))
    blocs.append(("E10 opération hors de toute époque → NON JUGEABLE", e10))

    def e11():
        """① RÔLE — E11, une VRAIE ligne (R-732). ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — le JSON de `preparer`.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail). [rend: 2] ⑥ TRAITEMENT — trois époques civiles déclarées
        pour l'épreuve sur la période de la fiche ; la répartition et les observations retenues sont recomptées ici.
        ⑦ UNITÉ — euros, observations. ⑧ POURQUOI — sortie capturée, sans vérité attendue : seule la cohérence est
        exigée. ⑨ CE QUI CLOCHE — k = 69 illustratif ; 2024-2026 a servi à régler C5 : ceci n'est PAS un jugement.
        ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        ops = donnees["ops"]
        texte = "2024-01-02..2024-12-31 ; 2025-01-02..2025-12-31 ; 2026-01-02..2026-07-10"
        lu = m.lire_les_epoques(texte, "%s..%s" % PERIODE_REELLE, donnees["seances"])
        if lu["motif"]:
            return False, lu["motif"]
        r = m.controle_des_epoques(ops, lu["epoques"], lu["parts_des_seances"], s69, SEUIL_EPOQUE)
        coherent = True
        for ep, ligne in zip(lu["epoques"], r["detail"]["epoques"]):
            dedans = [o for o in ops if ep["debut"] <= o["date_entree"] <= ep["fin"]]
            n_ret = m.observations_independantes(dedans)["n_observations"] if dedans else 0
            coherent &= (ligne["n_operations"] == len(dedans) and ligne["observations_retenues"] == n_ret)
        lignes = " | ".join("%s..%s n=%d retenues=%s gain=%.0f p=%s gagnante=%s" % (
            e["debut"], e["fin"], e["n_operations"], e["observations_retenues"] if e["observations_retenues"] is None
            else round(e["observations_retenues"], 2), e["gain_moyen_eur"] or 0,
            None if e["p_perdante"] is None else round(e["p_perdante"], 4), e["gagnante"])
            for e in r["detail"]["epoques"])
        total = sum(e["n_operations"] for e in r["detail"]["epoques"])
        return (coherent and total == len(ops) and r["etat"] in ("PASSE", "BLOQUE"),
                "%s : %d opérations, parts %s, %s ; minimum %s ; état %s %s" % (
                    FICHE_REELLE, total, [round(p, 3) for p in lu["parts_des_seances"]], lignes, r["seuil"],
                    r["etat"], r["raison"]))
    blocs.append(("E11 vraie ligne : C5E10-QA-V1, 2024-2026 seulement", e11))

    def e12():
        """① RÔLE — E12. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — une époque de pertes certaines, une gagnante ; puis deux gagnantes. ⑦ UNITÉ — euros.
        ⑧ POURQUOI — la première moitié de ⑦. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        deux = [{"debut": "2015-01-02", "fin": "2015-12-31"}, {"debut": "2016-01-04", "fin": "2016-12-30"}]
        perd = m.controle_des_epoques(fabriquer(deux, [[1500 + 9 * j for j in range(30)],
                                                       [-1500 - 9 * j for j in range(30)]], pas=3),
                                      deux, [0.5, 0.5], 0.05, SEUIL_EPOQUE)
        gagne = m.controle_des_epoques(fabriquer(deux, [[1500 + 9 * j for j in range(30)]] * 2, pas=3),
                                       deux, [0.5, 0.5], 0.05, SEUIL_EPOQUE)
        return (perd["etat"] == "BLOQUE" and "2016-01-04" in perd["raison"] and "perdante" in perd["raison"]
                and perd["valeur"] == 1 and perd["seuil"] == 1 and gagne["etat"] == "PASSE",
                "pertes : %s, %s gagnante(s), minimum %s, « %s » ; deux gagnantes : %s"
                % (perd["etat"], perd["valeur"], perd["seuil"], perd["raison"][:70], gagne["etat"]))
    blocs.append(("E12 époque perdante à coup sûr → BLOQUE", e12))

    def e13():
        """① RÔLE — E13, n°79 par une PROPRIÉTÉ : le groupe témoin ne décide jamais, quelle que soit la mesure où il
        est meilleur. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail).
        [rend: 2] ⑥ TRAITEMENT — 400 paires (stratégie, témoin) tirées au hasard (graine 20261105) : 0 à 8 opérations
        par époque, gains ~ N(moyenne tirée, écart tiré) ; chaque rendu doit être « PASSE », rôle AFFICHAGE ; et chacun
        des quatre critères (gain moyen sur le tout, part gagnante sur le tout, gain moyen d'une époque, part gagnante
        d'une époque) doit avoir été vu au moins 20 fois avec le témoin meilleur que la stratégie. ⑦ UNITÉ — euros,
        fractions. ⑧ POURQUOI — E8 ne compare que des groupes qui gagnent tous 100 % de leurs opérations : un témoin
        qui déciderait par la part gagnante d'une époque restait VERT (relecture S_per t1, R4). Une propriété ne
        dépend pas du critère qu'un sabotage choisirait. ⑨ CE QUI CLOCHE — un critère hors des quatre (le nombre
        d'opérations, par exemple) n'est couvert que si le hasard le fait varier, ce qu'il fait ici sans que ce soit
        compté. ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        hasard = random.Random(20261105)
        vus = {"gain_tout": 0, "part_tout": 0, "gain_epoque": 0, "part_epoque": 0}
        mauvais = []

        def tirer():
            """① RÔLE — Tirer un groupe d'opérations. ② CONTEXTE D'APPEL — `e13`. ③ ENTRÉE — — ④ CONDITIONS
            D'ENTRÉE — — ⑤ SORTIE — une liste d'opérations. [rend: 1] ⑥ TRAITEMENT — moyenne et écart tirés, puis 0 à 8
            gains par époque. ⑦ UNITÉ — euros. ⑧ POURQUOI — varier tous les critères à la fois. ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — avance le hasard d'`e13`. ⑪ TERMINAISON — rend la main. [sort: non]
            """
            moy, ecart = hasard.uniform(-1500, 1500), hasard.uniform(10, 3000)
            return fabriquer(quatre, [[hasard.gauss(moy, ecart) for _ in range(hasard.randint(0, 8))]
                                      for _ in quatre])

        def plus(a, b):
            """① RÔLE — Dire si le témoin est meilleur sur une mesure. ② CONTEXTE D'APPEL — `e13`. ③ ENTRÉE — la
            mesure du témoin, celle de la stratégie (ou None). ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — un booléen.
            [rend: 1] ⑥ TRAITEMENT — a présent et (b absent ou a > b). ⑦ UNITÉ — celle de la mesure. ⑧ POURQUOI — un
            groupe vide n'a pas de mesure. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
            """
            return a is not None and (b is None or a > b)
        for i in range(400):
            strat, temoin = tirer(), tirer()
            r = m.afficher_le_groupe_temoin(strat, temoin, quatre)
            if r["etat"] != "PASSE" or r["role"] != "AFFICHAGE":
                mauvais.append((i, r["etat"], r["role"]))
                continue
            d = r["detail"]
            vus["gain_tout"] += plus(d["groupe_temoin"]["gain_moyen_eur"], d["strategie"]["gain_moyen_eur"])
            vus["part_tout"] += plus(d["groupe_temoin"]["part_gagnante"], d["strategie"]["part_gagnante"])
            vus["gain_epoque"] += any(plus(e["groupe_temoin"]["gain_moyen_eur"], e["strategie"]["gain_moyen_eur"])
                                      for e in d["par_epoque"])
            vus["part_epoque"] += any(plus(e["groupe_temoin"]["part_gagnante"], e["strategie"]["part_gagnante"])
                                      for e in d["par_epoque"])
        return (not mauvais and all(v >= 20 for v in vus.values()),
                "400 paires ; états autres que PASSE/AFFICHAGE : %s ; témoin meilleur vu (par critère) : %s"
                % (mauvais[:3] or "aucun", vus))
    blocs.append(("E13 le témoin ne décide jamais, quel que soit le critère (n°79)", e13))

    def e14():
        """① RÔLE — E14 : une époque sans aucune opération n'est ni gagnante ni perdante. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail). [rend: 2] ⑥ TRAITEMENT — ① quatre époques,
        des gains seulement dans la première : 1 gagnante, minimum 3 → BLOQUE, et les trois vides portent 0 opération,
        `gagnante` faux, `p_perdante` None · ② trois époques gagnantes et la dernière vide : 3 gagnantes, pas 4.
        ⑦ UNITÉ — époques. ⑧ POURQUOI — compter une époque vide comme gagnante ouvrirait la porte à une stratégie qui
        ne joue que dans un seul climat (relecture S_per t1, R10) ; le ⑥ de `controle_des_epoques` le promet.
        ⑨ CE QUI CLOCHE — la raison du BLOQUE ne nomme pas les époques vides : elles ne se voient que dans le détail
        (BACKLOG). ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        gains = [1200 + 13 * j for j in range(12)]
        seule = m.controle_des_epoques(fabriquer(quatre, [gains, [], [], []]), quatre, parts_ans, s69, SEUIL_EPOQUE)
        vides = seule["detail"]["epoques"][1:]
        trois = m.controle_des_epoques(fabriquer(quatre, [gains, gains, gains, []]), quatre, parts_ans, s69,
                                       SEUIL_EPOQUE)
        ok = (seule["valeur"] == 1 and seule["etat"] == "BLOQUE" and seule["seuil"] == 3
              and all(e["n_operations"] == 0 and e["gagnante"] is False and e["p_perdante"] is None for e in vides)
              and trois["valeur"] == 3 and trois["detail"]["epoques"][3]["gagnante"] is False)
        return ok, "une seule époque jouée : %s gagnante(s), %s, « %s » ; trois jouées + une vide : %s gagnante(s), %s" \
            % (seule["valeur"], seule["etat"], seule["raison"][:60], trois["valeur"], trois["etat"])
    blocs.append(("E14 une époque vide n'est jamais gagnante", e14))

    def e15():
        """① RÔLE — E15 : BLOQUE passe avant INCONNU quand le refus est déjà certain. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail). [rend: 2] ⑥ TRAITEMENT — trois époques :
        une seule opération (non mesurable), 30 pertes certaines, 30 gains → BLOQUE, la raison nomme la perdante et
        les non mesurées. ⑦ UNITÉ — — ⑧ POURQUOI — le ⑧ de `controle_des_epoques` le promet (relecture S_per t1, R8).
        ⑨ CE QUI CLOCHE — sans effet sur le verdict final aujourd'hui (les deux mènent à NON TRANCHÉE) ; la raison
        rendue, elle, change. ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        trois = [{"debut": "2010-01-04", "fin": "2010-12-31"}, {"debut": "2011-01-03", "fin": "2011-12-30"},
                 {"debut": "2012-01-02", "fin": "2012-12-31"}]
        ops = fabriquer(trois, [[700], [-1500 - 9 * j for j in range(30)], [1500 + 9 * j for j in range(30)]], pas=3)
        r = m.controle_des_epoques(ops, trois, [1 / 3] * 3, 0.05, SEUIL_EPOQUE)
        return (r["etat"] == "BLOQUE" and "2011-01-03" in r["raison"] and "perdante" in r["raison"]
                and "non mesurées" in r["raison"], "%s : %s" % (r["etat"], r["raison"][:110]))
    blocs.append(("E15 BLOQUE avant INCONNU", e15))

    def e16():
        """① RÔLE — E16 : « gagnante » veut dire gain moyen STRICTEMENT positif. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail). [rend: 2] ⑥ TRAITEMENT — deux époques : la
        première a un gain moyen exactement nul (±500 € alternés), la seconde gagne → 1 gagnante. ⑦ UNITÉ — euros.
        ⑧ POURQUOI — une époque qui ne gagne rien n'est pas gagnante (⑥ de `controle_des_epoques`, « > 0 » ; relecture
        S_per t1, R9). ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        deux = [{"debut": "2015-01-02", "fin": "2015-12-31"}, {"debut": "2016-01-04", "fin": "2016-12-30"}]
        r = m.controle_des_epoques(fabriquer(deux, [[(-1) ** j * 500 for j in range(12)],
                                                    [900 + 7 * j for j in range(12)]]),
                                   deux, [0.5, 0.5], 0.05, SEUIL_EPOQUE)
        nulle = r["detail"]["epoques"][0]
        return (nulle["gain_moyen_eur"] == 0 and nulle["gagnante"] is False and r["valeur"] == 1,
                "gain moyen de l'époque nulle %s, gagnante %s ; gagnantes %s" % (nulle["gain_moyen_eur"],
                                                                                nulle["gagnante"], r["valeur"]))
    blocs.append(("E16 gain moyen nul : pas gagnante", e16))

    def e17():
        """① RÔLE — E17 : les degrés de liberté de Student valent n retenu − 1. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — (vert, détail). [rend: 2] ⑥ TRAITEMENT — trois gains
        100 × (μ − 1, μ, μ + 1), écart-type 100, n retenu 3 : t = μ√3 ; μ choisi pour t = −2,919986, le quantile 5 %
        de Student à 2 ddl (table) → p = 0,05 et ddl = 2. ⑦ UNITÉ — euros, probabilité. ⑧ POURQUOI — ⑥ ④ de
        `probabilite_epoque_perdante` (relecture S_per t1, R7 : ddl = n retenu passait VERT ; à 3 ddl, p ≈ 0,031).
        ⑨ CE QUI CLOCHE — la borne 10⁻³ est une borne d'épreuve. ⑩ EFFET — — ⑪ TERMINAISON — rend la main. [sort: non]
        """
        mu = -2.919986 / math.sqrt(3)
        r = m.probabilite_epoque_perdante([100 * (mu + d) for d in (-1, 0, 1)], 3)
        return (r["ddl"] == 2 and abs(r["p_perdante"] - 0.05) < 1e-3,
                "t %.6f ; ddl %s ; p %.5f (table : 0,05 à 2 ddl)" % (r["t"], r["ddl"], r["p_perdante"]))
    blocs.append(("E17 Student à n retenu − 1 ddl (table)", e17))

    for nom, f in blocs:
        try:
            vert, detail = f()
        except Exception as e:  # un cas qui lève est ROUGE, avec son message
            vert, detail = False, "%s: %s" % (type(e).__name__, e)
        res.append((nom, bool(vert), detail))
    return res


def lancer_copie(racine, donnees, sabotage):
    """Copie le module, applique un sabotage, joue les cas dans un sous-processus.

    ① RÔLE — Une passe. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine, le JSON, un sabotage ou None.
    ④ CONDITIONS D'ENTRÉE — la cible du sabotage est dans le module exactement une fois, sinon code 2.
    ⑤ SORTIE — (code du sous-processus, sa sortie). [rend: 2] ⑥ TRAITEMENT — copier, remplacer, relancer en « --cas ».
    ⑦ UNITÉ — — ⑧ POURQUOI — le dépôt n'est jamais modifié. ⑨ CE QUI CLOCHE — — ⑩ EFFET — dossier temporaire, effacé.
    ⑪ TERMINAISON — rend la main, ou SORT DU PROGRAMME en 2 sur cible introuvable. [sort: oui — 2]
    """
    tmp = tempfile.mkdtemp(prefix="epoques_")
    try:
        copie = os.path.join(tmp, "MODULE_JUGEMENT.py")
        texte = open(os.path.join(racine, MODULE), encoding="utf-8").read()
        if sabotage:
            nom, _, avant, apres = sabotage
            if texte.count(avant) != 1:
                print("ARRET : cible du sabotage %s trouvée %d fois (attendu 1)" % (nom, texte.count(avant)))
                sys.exit(2)
            texte = texte.replace(avant, apres)
        open(copie, "w", encoding="utf-8").write(texte)
        p = subprocess.run([sys.executable, "-I", "-B", ICI, "--cas", copie, donnees], capture_output=True,
                           text=True, timeout=600)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    """Prépare, joue Z0, puis les sabotages demandés.

    ① RÔLE — Le point d'entrée. ② CONTEXTE D'APPEL — le lancement. ③ ENTRÉE — la ligne de commande. ④ CONDITIONS
    D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — le code. [rend: 1] ⑥ TRAITEMENT — mode « --cas » : jouer `cas` et rendre 0 si
    tout est vert ; sinon préparer, Z0, sabotages. ⑦ UNITÉ — — ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — — ⑩ EFFET —
    affiche ; fichiers temporaires effacés. ⑪ TERMINAISON — rend le code. [sort: non]
    """
    if len(sys.argv) >= 4 and sys.argv[1] == "--cas":
        res = cas(sys.argv[2], sys.argv[3])
        for nom, vert, detail in res:
            print("%s  %s — %s" % ("VERT " if vert else "ROUGE", nom, detail))
        return 0 if all(v for _, v, _ in res) else 1
    if len(sys.argv) < 2:
        print(__doc__.split("①")[0])
        return 2
    racine = os.path.abspath(sys.argv[1])
    option = sys.argv[2] if len(sys.argv) > 2 else None
    noms = [s[0] for s in SABOTAGES]
    if option and option != "--saboter" and option not in noms:
        print("ARRET : sabotage inconnu %r (connus : %s)" % (option, ", ".join(noms)))
        return 2
    tmp = tempfile.mkdtemp(prefix="epoques_donnees_")
    try:
        donnees = os.path.join(tmp, "donnees.json")
        try:
            n = preparer(racine, donnees)
        except Exception as e:
            print("ARRET : préparation impossible (%s: %s)" % (type(e).__name__, e))
            return 2
        print("préparation : %d opérations de %s rejouées par le juge ; séances %s..%s lues au calendrier"
              % (n, FICHE_REELLE, *PERIODE_REELLE))
        code, sortie = lancer_copie(racine, donnees, None)
        print("== Z0 (le dépôt tel quel) : code %d" % code)
        print(sortie.rstrip())
        ok = code == 0
        a_jouer = SABOTAGES if option == "--saboter" else [s for s in SABOTAGES if s[0] == option]
        for sab in a_jouer:
            code_s, sortie_s = lancer_copie(racine, donnees, sab)
            rouges = [ligne.split(" — ")[0].replace("ROUGE  ", "") for ligne in sortie_s.splitlines()
                      if ligne.startswith("ROUGE")]
            mord = code_s != 0 and bool(rouges)
            ok &= mord
            print("== %s (vise %s) : code %d, %s — rouges : %s" % (sab[0], sab[1], code_s,
                                                                   "MORD" if mord else "NE MORD PAS",
                                                                   "; ".join(rouges) or "aucun"))
        print("VERDICT : %s" % ("VERT" if ok else "ROUGE"))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
