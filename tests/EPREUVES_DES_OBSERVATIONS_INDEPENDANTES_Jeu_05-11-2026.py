"""ÉPREUVES DES OBSERVATIONS INDÉPENDANTES — lot S_ep (A-304, n°106), jeudi 05-11-2026, tours 2 et 3. Simulation uniquement.

LE SENS EN TÊTE — Cette épreuve dit si `observations_independantes(ops)` (`programmes/MODULE_JUGEMENT.py`) mesure bien
combien d'occasions distinctes portent le gain moyen d'une stratégie, PAR LE CHEVAUCHEMENT RÉEL DES POSITIONS (les
paires d'opérations ouvertes en même temps) : des positions qui ne se chevauchent jamais valent exactement autant
d'observations que d'opérations ; des blocs de 5 copies ouvertes ensemble, exactement le cinquième ; une dépendance
négative n'est jamais créditée ; les 100 opérations du tableau de C5 valent 68,8 observations MESURÉES sur 143 paires (cas
connu : mesure du superviseur R-759 du 05-11-2026, faite par un autre programme que celui-ci) ; une date absente ou
mal écrite rend INCONNU avec un motif. DEPUIS LE TOUR 3 (avis du superviseur R-759 « DE FOND », 05-11-2026) : le nombre
RETENU est le plus petit des observations mesurées et de K, le nombre de positions deux à deux jamais ouvertes en même
temps (périodes distinctes) — C5 rejouée par le juge : mesurées 70,585, K = 52, retenu 52 ; deux paquets de 50
positions ouvertes ensemble : au plus 2 ; trente positions toutes ensemble : 1 ; un jeton : K = N. Le juge lui-même
(`juger`) est EXÉCUTÉ jusqu'à sa ligne OBSERVATIONS, et le nombre qu'il affiche est comparé au calcul de la fonction
sur les mêmes opérations (relecture du tour 2, R-2 : le juge pouvait mesurer la moitié des opérations, ou afficher les
opérations à la place des observations, sans qu'aucun cas ne rougisse). Elle vérifie aussi que l'ancien comptage par épisodes à 5 séances et le
réglage du tour 1 (deux règles, troncature de Geyer, test de Ljung et Box, `_khi2_au_dela`) ont disparu, et que la
fonction ne prend que les opérations, sans valeur par défaut.
CE QUI EST RETIRÉ DE L'ÉPREUVE DU TOUR 1, DIT ICI POUR NE RIEN SUPPRIMER EN SILENCE : le contrôle « C5 retrouve 96 à
100 observations (A-304) », fixé par le superviseur avant D, est RETIRÉ — le superviseur R-759 du 05-11-2026 l'a jugé
faux (cible d'une autre mesure, défaut D2) ; les cas du khi-deux, de la règle inconnue, du seuil, du centrage exact de
Geyer et de la ressemblance au voisin sont retirés avec les fonctions qu'ils éprouvaient.

USAGE : python3 -B tests/EPREUVES_DES_OBSERVATIONS_INDEPENDANTES_Jeu_05-11-2026.py <racine> [--saboter | nom]
  sans option : Z0, le dépôt tel quel ; --saboter : Z0 puis chaque sabotage ; un nom de sabotage : Z0 puis celui-là.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable, si le nom demandé n'existe pas ou si le rejeu de C5 par le juge n'a pas pu tourner (R-734 :
un contrôle qui n'a pas pu tourner ne rend pas 0).

① RÔLE — Éprouver `observations_independantes` à vérité connue et sur de vraies opérations, et prouver que chaque
  épreuve rougit quand on retire ce qu'elle teste (R-731).
② CONTEXTE D'APPEL — À la main, ou par le lanceur des épreuves (`tests/LANCEMENT_DES_EPREUVES.json` n'a pas d'entrée
  pour elle : la racine en seul argument est le lancement par défaut). Ce programme se relance lui-même en mode
  « --cas » sur chaque copie.
③ ENTRÉE — La racine du dépôt ; `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/MODULE_JUGEMENT.py`, `programmes/JUGE_DES_STRATEGIES.py`, le
  témoin du golden, le golden, le référentiel des valeurs, `programmes/MODULE_POSITIONS.py` et
  `donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv`.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage. [rend: 1]
⑥ TRAITEMENT — ① rejouer C5 UNE fois par le calibrage du juge (`calibrer`, sur le témoin du golden, sortie par sortie
  contre le tableau des 100) et garder ses opérations (dates d'entrée et de sortie, gain) dans un fichier temporaire ·
  ① bis garder aussi la fiche, le barème et les opérations COMPLÈTES que `jouer` rend, pour exécuter `juger` (E11) ·
  ② pour Z0 puis chaque sabotage : copier les DEUX programmes éprouvés dans un dossier temporaire, appliquer le
  sabotage (un texte qui doit y être une fois), relancer ce programme en « --cas » sur la copie · ③ Z0 doit être
  vert, un sabotage doit faire rougir un cas.
⑦ UNITÉ — Des opérations et des observations (nombres) ; des paires (entiers) ; des probabilités.
⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731). Le rejeu
  passe par `calibrer`, le chemin du juge lui-même, pour que les opérations soient celles que le juge produit.
⑨ CE QUI CLOCHE — ① Le rejeu de C5 n'est fait que sur le dépôt intact : les sabotages ne portent que sur les deux
  programmes copiés, pas sur le jeu des opérations. ② Le 68,8 et les 143 paires du tableau sont un CAS CONNU, mesuré
  par le superviseur avant l'écriture de cette épreuve. Les chiffres de C5 REJOUÉE PAR LE JUGE (barème réel) et la
  probabilités (tableau 0,0305 ; juge 0,0475) sont des TÉMOINS DE RÉGRESSION relevés APRÈS l'écriture de l'épreuve, le
  05-11-2026 (PROGRES du tour 2) : ce ne sont pas des vérités. Le 70,585 a depuis été recalculé à l'identique, en
  fractions exactes, par le relecteur du tour 2 ; K = 52 vient du programme du superviseur (sortie_disjointes.txt).
  ③ E1, E2, E4, E10, E13, E14 et E15 sont des vérités EXACTES (calcul à la main au ⑧ de `cas`), sans tirage ; E12 tire
  des gains, mais sa vérité (au plus 2) ne dépend pas des gains. ④ E11 exécute `juger` jusqu'à sa ligne OBSERVATIONS
  et l'ARRÊTE au pas suivant (la coupure 70/30) par un module de jugement mandataire : le reste du juge n'est pas
  exécuté ici.
⑩ EFFET — Écrit et efface des dossiers temporaires ; ne touche pas au dépôt.
⑪ TERMINAISON — Chaque relance a un délai de 600 s. [sort: oui — code de sortie]
"""
import ast
import csv
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import importlib.util

ICI = os.path.abspath(__file__)
MODULE = "programmes/MODULE_JUGEMENT.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
TABLEAU = "donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv"
# CAS CONNU (superviseur R-759, 05-11-2026, mesuré par son propre programme avant cette épreuve) : tableau des 100.
CONNU_TABLEAU_OBSERVATIONS, CONNU_TABLEAU_PAIRES = 68.82, 143
# CAS CONNUS DU TOUR 3 : K = 52 périodes distinctes pour les 100 opérations de C5, tableau et juge (mêmes dates) —
# superviseur R-759, superviseur_nuit/sep_t3/sortie_disjointes.txt ; 70,585 mesurées sur les opérations du juge —
# relecteur du tour 2, recalcul en fractions exactes (lot_Sep_relecture_t2/sorties/recalcul.txt).
CONNU_C5_PERIODES = 52
CONNU_JUGE_MESUREES = 70.585
# TÉMOINS DE RÉGRESSION, relevés APRÈS l'écriture de l'épreuve (05-11-2026, PROGRES du tour 2) — pas des vérités.
TEMOIN_TABLEAU_P = 0.0305
# C5 rejouée par le juge (barème réel), relevé à 15h37 au premier Z0 (sorties/z0_essai1.txt du tour 2) :
TEMOIN_JUGE_OBSERVATIONS = 70.58527047235057
TEMOIN_JUGE_PAIRES = 143
TEMOIN_JUGE_P = 0.0475

# LES SABOTAGES : (fichier, texte qui doit y être UNE fois, remplacement). Les six premiers sont la liste du
# superviseur R-759 du 05-11-2026 ; les suivants retirent chacun ce qu'un autre cas teste.
SABOTAGES = {
    "S1_rendre_N": [(MODULE, "    taille = max(facteur, 1.0)\n", "    taille = 1.0\n")],
    "S2_toutes_les_paires": [(MODULE, "              if not (lues[i][1] < lues[j][0] or lues[j][1] < lues[i][0])]",
                              "              if True]")],
    "S3_bornes_exclues": [(MODULE, "              if not (lues[i][1] < lues[j][0] or lues[j][1] < lues[i][0])]",
                           "              if not (lues[i][1] <= lues[j][0] or lues[j][1] <= lues[i][0])]")],
    "S4_negatif_credite": [(MODULE, "    taille = max(facteur, 1.0)\n", "    taille = facteur\n")],
    "S5_date_absente_ignoree": [(MODULE, "    if illisibles:\n        rendu[\"motif\"]", "    if False:\n        rendu[\"motif\"]")],
    "S6_centre_sur_zero": [(MODULE, "    ecart = [g - moyenne for g in gains]", "    ecart = [g for g in gains]")],
    "S7_variance_nulle": [(MODULE, "    if somme_carres == 0.0:\n        rendu[\"motif\"]", "    if False:\n        rendu[\"motif\"]")],
    # S8 s'ancre sur le tri de observations_independantes, AVEC la ligne qui le précède : depuis le lot S_per, le
    # lecteur des époques porte aussi « lues.sort() », et l'ancre seule était trouvée 2 fois (bloc 3, 08-11-2026).
    "S8_sans_tri": [(MODULE, "        return rendu\n    lues.sort()\n", "        return rendu\n    pass\n")],
    "S9_sans_hasard": [(MODULE, "            hasard.shuffle(melange)\n", "            pass\n")],
    "S10_argument_par_defaut": [(MODULE, "def observations_independantes(ops):", "def observations_independantes(ops=()):")],
    "S11_ancien_appel": [(JUGE, "e = J.observations_independantes(ops)", "e = J.episodes(ops, seances)")],
    "S12_sortie_avant_entree_acceptee": [(MODULE, "            if bornes[1] < bornes[0]:", "            if False:")],
    "S13_date_mal_ecrite_acceptee": [(MODULE, 'if not isinstance(t, str) or len(t) != 10 or t[4] != "-" or t[7] != "-":',
                                      "if not isinstance(t, str):")],
    # Tour 3 : R3 et R4 du relecteur du tour 2 (le juge), puis la borne K (liste du superviseur R-759 avant le tour 3).
    "S14_juge_moitie_des_ops": [(JUGE, "e = J.observations_independantes(ops)",
                                 "e = J.observations_independantes(ops[:50])")],
    "S15_juge_affiche_les_operations": [(JUGE, '.format(e["n_operations"], e["n_observations"], e["taille_des_groupes"],',
                                         '.format(e["n_operations"], e["n_operations"], e["taille_des_groupes"],')],
    "S16_K_oublie": [(MODULE, "    retenu = min(observations_mesurees, float(periodes))\n",
                      "    retenu = observations_mesurees\n")],
    "S17_K_sans_bornes_comprises": [(MODULE, "        if fin is None or debut > fin:\n",
                                     "        if fin is None or debut >= fin:\n")],
    "S18_K_compte_les_paquets": [(MODULE, "    for debut, sortie, _ in sorted(lues, key=lambda x: x[1]):\n"
                                          "        if fin is None or debut > fin:\n"
                                          "            periodes += 1\n"
                                          "            fin = sortie\n",
                                  "    for debut, sortie, _ in sorted(lues):\n"
                                  "        if fin is None or debut > fin:\n"
                                  "            periodes += 1\n"
                                  "            fin = sortie\n"
                                  "        else:\n"
                                  "            fin = max(fin, sortie)\n")],
    "S19_taille_laissee_au_facteur": [(MODULE, "                 taille_des_groupes=n / retenu)",
                                       "                 taille_des_groupes=taille)")],
    "S20_rendre_K": [(MODULE, "    retenu = min(observations_mesurees, float(periodes))\n",
                      "    retenu = float(periodes)\n")],
}


def charger(chemin, nom):
    """Charge un programme Python par son chemin.

    ① RÔLE — Donner le module éprouvé, pris dans la copie (sabotée ou non). ② CONTEXTE D'APPEL — `cas` et
    `rejouer_c5`. ③ ENTRÉE — `chemin` du fichier, `nom` du module. ④ CONDITIONS D'ENTRÉE — le fichier existe.
    ⑤ SORTIE — le module chargé. [rend: 1] ⑥ TRAITEMENT — `spec_from_file_location`, puis exécution. ⑦ UNITÉ — —
    ⑧ POURQUOI — Charger par chemin garantit que c'est la copie qui est éprouvée, jamais un module déjà importé.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — exécute le haut du fichier. ⑪ TERMINAISON — rend la main ou lève ce que le
    fichier lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rejouer_c5(racine, sortie):
    """Rejoue C5 par le calibrage du juge et écrit ses opérations dans `sortie` (JSON).

    ① RÔLE — Obtenir les 100 opérations étalons de C5 PRODUITES PAR LE JUGE, sur le témoin du golden.
    ② CONTEXTE D'APPEL — Le programme principal, une fois, avant Z0. ③ ENTRÉE — la racine, le fichier de sortie.
    ④ CONDITIONS D'ENTRÉE — celles du ④ du programme. ⑤ SORTIE — un couple (vrai si le calibrage du juge est
    vert, ses lignes). [rend: 2] ⑥ TRAITEMENT — ① charger le juge, les cours du témoin, les mnémoniques, le module
    de positions, le golden · ② envelopper `jouer` pour garder ce qu'il rend, avec la fiche et le barème reçus ·
    ③ appeler `calibrer` avec le témoin
    et le tableau des 100, qui compare les sorties une à une · ④ écrire date de signal, dates d'entrée et de sortie,
    valeur et gain net de chaque opération, et les clés (date, valeur) du juge et du tableau ; et, pour exécuter
    `juger` (E11), la fiche, le barème et les opérations COMPLÈTES telles que `jouer` les rend. ⑦ UNITÉ — le gain net
    en euros ; les dates en AAAA-MM-JJ. ⑧ POURQUOI — passer par `calibrer` reprend la fiche, la période et le barème
    du juge sans les recopier (R-708) ; les dates d'entrée et de sortie sont celles que le juge passe à la mesure.
    ⑨ CE QUI CLOCHE — ① l'enveloppe remplace `jouer` dans le module chargé pendant l'appel : si `calibrer` cessait
    d'appeler `jouer` par ce nom, rien ne serait gardé, et le cas E3 le dirait (zéro opération). ⑩ EFFET — écrit
    `sortie`. ⑪ TERMINAISON — rend la main ou lève. [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    B = charger(os.path.join(racine, JUGE), "juge_epreuve_obs")
    f_tem = B.trouver(racine, "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN")
    cours = B.charger_cours(f_tem)
    mnemo = B.table_mnemoniques(B.trouver(racine, "REFERENTIEL_VALEURS"))
    pos = B.charger_module(B.trouver(racine, "MODULE_POSITIONS.py"), "pos")
    golden = json.load(open(B.trouver(racine, "golden_tests_"), encoding="utf-8"))
    gardees = []
    vrai_jouer = B.jouer

    def jouer_garde(*a, **k):
        """Appelle le vrai `jouer` et garde ce qu'il rend.

        ① RÔLE — Garder les opérations rejouées, la fiche et le barème. ② CONTEXTE D'APPEL — `calibrer`, à la place
        de `jouer`. ③ ENTRÉE — les arguments de `jouer`, transmis tels quels. ④ CONDITIONS D'ENTRÉE — celles de
        `jouer`. ⑤ SORTIE — ce que rend `jouer`. [rend: 1] ⑥ TRAITEMENT — appeler, garder le premier élément rendu, la
        fiche (premier argument) et le barème (argument nommé `bareme`, ou `None`), rendre. ⑦ UNITÉ — — ⑧ POURQUOI —
        `calibrer` ne rend pas les opérations ; `juger` a besoin de la fiche et du barème que le calibrage a joués.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — ajoute à `gardees`. ⑪ TERMINAISON — rend la main ou lève ce que `jouer` lève.
        [sort: non]
        """
        r = vrai_jouer(*a, **k)
        gardees.append((r[0], a[0], k.get("bareme")))
        return r
    B.jouer = jouer_garde
    try:
        ok, lignes = B.calibrer(cours, mnemo, racine, pos, golden, f_tem, os.path.join(racine, TABLEAU))
    finally:
        B.jouer = vrai_jouer
    ops = [{"date_signal": o["date_signal"], "date_entree": o["date_entree"], "date_sortie": o["date_sortie"],
            "valeur": o["valeur"], "net": o["net"]} for o in (gardees[-1][0] if gardees else [])]
    T = list(csv.DictReader(open(os.path.join(racine, TABLEAU), encoding="utf-8"), delimiter=";"))
    cles = {"juge": sorted([o["date_signal"], B.cle_valeur(o["valeur"])] for o in ops),
            "tableau": sorted([t["date_signal"], B.cle_valeur(t["valeur"])] for t in T)}
    json.dump({"ops": ops, "cles": cles, "ops_completes": gardees[-1][0] if gardees else [],
               "fiche": gardees[-1][1] if gardees else None, "bareme": gardees[-1][2] if gardees else None},
              open(sortie, "w", encoding="utf-8"))
    return ok, lignes


def jour(k):
    """Le k-ième jour à partir du 01-01-2024, écrit AAAA-MM-JJ.

    ① RÔLE — Fabriquer des dates valides pour les cas à vérité connue. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — `k`,
    un entier positif ou nul. ④ CONDITIONS D'ENTRÉE — `k` entier. ⑤ SORTIE — un texte AAAA-MM-JJ. [rend: 1]
    ⑥ TRAITEMENT — 01-01-2024 plus `k` jours. ⑦ UNITÉ — des jours du calendrier. ⑧ POURQUOI — l'ancienne épreuve
    écrivait des dates à la main (« %02d ») ; un calendrier vrai évite un jour impossible. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    import datetime
    return (datetime.date(2024, 1, 1) + datetime.timedelta(days=k)).isoformat()


def cas(copie, f_ops, racine):
    """Joue les cas sur une copie et rend la liste (nom, vert, détail).

    ① RÔLE — Les cas E1 à E15. ② CONTEXTE D'APPEL — Le mode « --cas », une fois par copie. ③ ENTRÉE — la copie
    (dossier qui contient `programmes/`), le JSON des opérations rejouées, la racine (pour le tableau des 100, et pour
    les cours du témoin, les mnémoniques et le module de positions dont `juger` a besoin en E11).
    ④ CONDITIONS D'ENTRÉE — les deux programmes sont dans la copie. ⑤ SORTIE — une liste de triplets. [rend: 1]
    ⑥ TRAITEMENT — un cas par fonction locale ; une exception rend le cas ROUGE avec son message. ⑦ UNITÉ — des
    observations ; des paires ; des probabilités. ⑧ POURQUOI — chaque cas porte sa raison dans son nom ; les vérités
    exactes : E1, aucune paire, facteur 1, donc N, et K = N ; E2, vingt blocs de cinq copies, dans chaque bloc 10
    paires de produit e², somme des carrés 5 e², facteur 1 + 2 × 10 ÷ 5 = 5, donc N ÷ 5 = 20 mesurées, K = 20 ; E4,
    des paires (+a, −a) de moyenne nulle, facteur 1 − 1 = 0, ramené à 1, donc N = 100 mesurées, mais chaque paire est
    ouverte ensemble : K = 50, retenu 50 ; E10, deux paires qui ne se touchent qu'un jour, écarts ±100, facteur
    1 + 2 × 20 000 ÷ 40 000 = 2, donc 4 ÷ 2 = 2 mesurées, K = 2 ; E13, vingt chaînes de cinq positions de même gain,
    chacune touchant la suivante un jour : 4 paires par chaîne, facteur 1 + 2 × 4 ÷ 5 = 2,6, mesurées 100 ÷ 2,6 =
    38,46, K = 3 par chaîne (1re, 3e, 5e), 60 en tout, retenu 38,46 (la MESURE mord, pas K) ; E14, trente positions
    toutes ensemble : K = 1, retenu 1 ; trente isolées : 30 ; E15, cinquante positions dont chaque entrée suit d'un
    jour la sortie précédente : aucune paire, K = 50. E12, deux paquets de 50 ouverts ensemble : K = 2, donc au plus 2,
    quels que soient les gains (vérité du relecteur du tour 2 : 3,9 ; le plancher de 30 doit dire TROP PETIT). ⑨ CE QUI CLOCHE — ① le seuil « p < 0,01 » de E2 est une
    borne d'épreuve, pas un seuil de la loi : sous des blocs de copies, le hasard n'atteint presque jamais un facteur
    de 5. ② E11 arrête `juger` après sa ligne OBSERVATIONS (voir ⑨④ du programme). ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    J = charger(os.path.join(copie, MODULE), "jugement_epreuve_obs")
    texte_juge = open(os.path.join(copie, JUGE), encoding="utf-8").read()
    res = []

    def un(nom, f):
        """Joue un cas et range son résultat.

        ① RÔLE — Une exception rend le cas ROUGE, jamais muet. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — le nom, la
        fonction du cas. ④ CONDITIONS D'ENTRÉE — la fonction rend (vert, détail). ⑤ SORTIE — rien. [rend: rien]
        ⑥ TRAITEMENT — appeler, attraper, ranger. ⑦ UNITÉ — — ⑧ POURQUOI — R-734. ⑨ CE QUI CLOCHE — — ⑩ EFFET —
        ajoute à `res`. ⑪ TERMINAISON — rend la main. [sort: non]
        """
        try:
            v, d = f()
        except Exception as ex:   # une épreuve qui lève est ROUGE, jamais muette
            v, d = False, "LEVE %s: %s" % (type(ex).__name__, ex)
        res.append((nom, bool(v), d))

    O = J.observations_independantes
    rng = random.Random(20261105)
    T = list(csv.DictReader(open(os.path.join(racine, TABLEAU), encoding="utf-8"), delimiter=";"))
    tableau = [{"date_entree": t["date_entree"], "date_sortie": t["date_sortie"], "valeur": t["valeur"],
                "net": float(t["net_eur"].replace(",", "."))} for t in T]

    def e1():
        o = [{"date_entree": jour(3 * k), "date_sortie": jour(3 * k + 1), "valeur": "V", "net": rng.gauss(0, 1000)}
             for k in range(100)]
        r = O(o)
        return (r["n_observations"] == 100.0 and r["paires_qui_se_chevauchent"] == 0 and r["p_hasard"] is None
                and r["periodes_distinctes"] == 100,
                "observations %r · paires %r · p %r · K %r (vérité 100, 0, None, 100)"
                % (r["n_observations"], r["paires_qui_se_chevauchent"], r["p_hasard"], r["periodes_distinctes"]))
    un("E1 positions qui ne se chevauchent jamais : exactement N (100), et K = N", e1)

    def e2():
        o = []
        for b in range(20):
            g = rng.gauss(0, 1000)
            o += [{"date_entree": jour(10 * b), "date_sortie": jour(10 * b + 4), "valeur": "V%d" % c, "net": g}
                  for c in range(5)]
        r = O(o)
        return (abs(r["n_observations"] - 20.0) < 1e-9 and abs(r["observations_mesurees"] - 20.0) < 1e-9
                and r["periodes_distinctes"] == 20 and r["paires_qui_se_chevauchent"] == 200
                and r["p_hasard"] is not None and r["p_hasard"] < 0.01,
                "retenu %.6f · mesurées %.6f · K %r · paires %r · p %r (vérité 20, 20, 20, 200, p < 0,01)"
                % (r["n_observations"], r["observations_mesurees"], r["periodes_distinctes"],
                   r["paires_qui_se_chevauchent"], r["p_hasard"]))
    un("E2 blocs de 5 copies ouvertes ensemble : exactement N ÷ 5 (20), et le hasard ne l'atteint pas", e2)

    def e3():
        lu = json.load(open(f_ops, encoding="utf-8"))
        ops = lu["ops"]
        rt = O(tableau)
        rj = O(ops)
        vu = {"tableau mesurées 68,82 (±0,01)": abs(rt["observations_mesurees"] - CONNU_TABLEAU_OBSERVATIONS) < 0.01,
              "tableau K 52": rt["periodes_distinctes"] == CONNU_C5_PERIODES,
              "tableau retenu 52": rt["n_observations"] == float(CONNU_C5_PERIODES),
              "tableau 143 paires": rt["paires_qui_se_chevauchent"] == CONNU_TABLEAU_PAIRES,
              "tableau p = témoin": rt["p_hasard"] == TEMOIN_TABLEAU_P,
              "100 opérations rejouées": len(ops) == 100,
              "mêmes (date, valeur) que le tableau": lu["cles"]["juge"] == lu["cles"]["tableau"],
              "juge mesurées 70,585 (±0,01)": abs(rj["observations_mesurees"] - CONNU_JUGE_MESUREES) < 0.01,
              "juge mesurées = témoin": abs(rj["observations_mesurees"] - TEMOIN_JUGE_OBSERVATIONS) < 1e-9,
              "juge K 52": rj["periodes_distinctes"] == CONNU_C5_PERIODES,
              "juge retenu 52": rj["n_observations"] == float(CONNU_C5_PERIODES),
              "juge groupes 100 ÷ 52": abs(rj["taille_des_groupes"] - 100.0 / CONNU_C5_PERIODES) < 1e-9,
              "juge paires = témoin": rj["paires_qui_se_chevauchent"] == TEMOIN_JUGE_PAIRES,
              "juge p = témoin": rj["p_hasard"] == TEMOIN_JUGE_P}
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + \
            " · tableau mesurées %r, K %r, retenu %r, %r paires, p %r · juge mesurées %r, K %r, retenu %r, groupes %r, " \
            "%r paires, p %r" % (
                rt["observations_mesurees"], rt["periodes_distinctes"], rt["n_observations"],
                rt["paires_qui_se_chevauchent"], rt["p_hasard"], rj["observations_mesurees"], rj["periodes_distinctes"],
                rj["n_observations"], rj["taille_des_groupes"], rj["paires_qui_se_chevauchent"], rj["p_hasard"])
    un("E3 C5 : tableau des 100 et opérations rejouées par le juge — mesurées 68,82 / 70,585, K = 52, retenu 52", e3)

    def e4():
        o = []
        for b in range(50):
            a = rng.gauss(0, 1000)
            o += [{"date_entree": jour(10 * b), "date_sortie": jour(10 * b + 3), "valeur": "A", "net": a},
                  {"date_entree": jour(10 * b + 1), "date_sortie": jour(10 * b + 5), "valeur": "B", "net": -a}]
        r = O(o)
        return (r["observations_mesurees"] == 100.0 and r["periodes_distinctes"] == 50 and r["n_observations"] == 50.0
                and r["taille_des_groupes"] == 2.0,
                "mesurées %r · K %r · retenu %r · groupes %r (vérité 100, 50, 50, 2,0)"
                % (r["observations_mesurees"], r["periodes_distinctes"], r["n_observations"], r["taille_des_groupes"]))
    un("E4 dépendance négative : jamais créditée (mesurées exactement N, 100) ; K = 50 paires ouvertes ensemble", e4)

    def e5():
        bon = [{"date_entree": jour(3 * k), "date_sortie": jour(3 * k + 2), "valeur": "V", "net": float(k % 3)}
               for k in range(6)]
        mauvais = {"entrée absente": {"date_sortie": jour(40), "valeur": "X", "net": 1.0},
                   "entrée vide": {"date_entree": "", "date_sortie": jour(40), "valeur": "X", "net": 1.0},
                   "entrée None": {"date_entree": None, "date_sortie": jour(40), "valeur": "X", "net": 1.0},
                   "entrée JJ/MM/AAAA": {"date_entree": "05/11/2024", "date_sortie": jour(40), "valeur": "X", "net": 1.0},
                   "entrée AAAAMMJJ": {"date_entree": "20240105", "date_sortie": jour(40), "valeur": "X", "net": 1.0},
                   "entrée jour impossible": {"date_entree": "2024-13-01", "date_sortie": jour(40), "valeur": "X", "net": 1.0},
                   "sortie absente": {"date_entree": jour(38), "valeur": "X", "net": 1.0}}
        vu = {}
        for k, m in mauvais.items():
            r = O(bon + [m])
            vu[k] = r["n_observations"] is None and bool(r["motif"]) and "n°6" in r["motif"]
        refus = {"sortie avant entrée": {"date_entree": jour(40), "date_sortie": jour(38), "valeur": "X", "net": 1.0},
                 "gain absent": {"date_entree": jour(38), "date_sortie": jour(40), "valeur": "X"},
                 "gain non fini": {"date_entree": jour(38), "date_sortie": jour(40), "valeur": "X", "net": float("nan")}}
        for k, m in refus.items():
            try:
                O(bon + [m])
                vu[k] = False
            except ValueError:
                vu[k] = True
        motif = O(bon + [mauvais["entrée vide"]])["motif"]
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + \
            " · motif type : %r" % motif
    un("E5 date absente ou mal écrite : INCONNU avec motif qui nomme l'opération ; sortie avant entrée refusée", e5)

    def e6():
        appels = [n for n in ast.walk(ast.parse(texte_juge)) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute)]
        noms = [n.func.attr for n in appels]
        obs = [n for n in appels if n.func.attr == "observations_independantes"]
        mod = ast.parse(open(os.path.join(copie, MODULE), encoding="utf-8").read())
        defs = {n.name for n in ast.walk(mod) if isinstance(n, ast.FunctionDef)}
        affectes = {c.id for n in ast.walk(mod) if isinstance(n, ast.Assign) for c in n.targets
                    if isinstance(c, ast.Name)}
        vu = {"aucun appel episodes": "episodes" not in noms,
              "un appel observations_independantes(ops), un seul argument": len(obs) == 1
              and len(obs[0].args) == 1 and not obs[0].keywords,
              "aucune définition episodes ni _khi2_au_dela": not ({"episodes", "_khi2_au_dela"} & defs),
              "aucune constante REGLES_DE_DEPENDANCE": "REGLES_DE_DEPENDANCE" not in affectes,
              "le juge n'écrit plus « prudente » ni Q-Sep1 dans son affichage": all(
                  "prudente" not in n.value and "Q-Sep1" not in n.value for n in ast.walk(ast.parse(texte_juge))
                  if isinstance(n, ast.Constant) and isinstance(n.value, str) and "OBSERVATIONS" in n.value)}
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E6 l'ancien comptage à 5 séances et le réglage du tour 1 ont disparu ; le juge appelle (ops)", e6)

    def e7():
        mod = ast.parse(open(os.path.join(copie, MODULE), encoding="utf-8").read())
        f = [n for n in ast.walk(mod) if isinstance(n, ast.FunctionDef) and n.name == "observations_independantes"]
        if len(f) != 1:
            return False, "%d définition(s)" % len(f)
        a = f[0].args
        vu = {"arguments": [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs],
              "défauts": len(a.defaults) + sum(d is not None for d in a.kw_defaults),
              "*args/**kw": (a.vararg is not None) or (a.kwarg is not None)}
        return vu["arguments"] == ["ops"] and vu["défauts"] == 0 and not vu["*args/**kw"], repr(vu)
    un("E7 la fonction ne prend que les opérations, sans valeur par défaut", e7)

    def e8():
        r = O([{"date_entree": jour(k), "date_sortie": jour(k + 3), "valeur": "V", "net": 300.0} for k in range(7)])
        return r["n_observations"] is None and bool(r["motif"]), "rendu %r · motif %r" % (r["n_observations"], r["motif"])
    un("E8 gains tous égaux : INCONNU avec motif, jamais un nombre", e8)

    def e9():
        m = list(tableau)
        random.Random(5).shuffle(m)
        a, b = O(tableau), O(m)
        return (a["n_observations"] == b["n_observations"] and a["p_hasard"] == b["p_hasard"]
                and a["observations_mesurees"] == b["observations_mesurees"]
                and a["periodes_distinctes"] == b["periodes_distinctes"],
                "retenu %r contre %r · mesurées %r contre %r · K %r contre %r · p %r contre %r"
                % (a["n_observations"], b["n_observations"], a["observations_mesurees"], b["observations_mesurees"],
                   a["periodes_distinctes"], b["periodes_distinctes"], a["p_hasard"], b["p_hasard"]))
    un("E9 le résultat, probabilité comprise, ne dépend pas de l'ordre donné par l'appelant", e9)

    def e10():
        o = [{"date_entree": "2024-01-02", "date_sortie": "2024-01-05", "valeur": "A", "net": 100.0},
             {"date_entree": "2024-01-05", "date_sortie": "2024-01-08", "valeur": "B", "net": 100.0},
             {"date_entree": "2024-02-01", "date_sortie": "2024-02-03", "valeur": "C", "net": -100.0},
             {"date_entree": "2024-02-03", "date_sortie": "2024-02-05", "valeur": "D", "net": -100.0}]
        r = O(o)
        return (r["paires_qui_se_chevauchent"] == 2 and abs(r["n_observations"] - 2.0) < 1e-12
                and abs(r["observations_mesurees"] - 2.0) < 1e-12 and r["periodes_distinctes"] == 2,
                "paires %r · retenu %r · mesurées %r · K %r (vérité 2, 2, 2, 2)"
                % (r["paires_qui_se_chevauchent"], r["n_observations"], r["observations_mesurees"],
                   r["periodes_distinctes"]))
    un("E10 bornes comprises : une sortie le jour d'une entrée est un chevauchement, pour les paires ET pour K", e10)

    def e11():
        import contextlib
        import io
        import re
        lu = json.load(open(f_ops, encoding="utf-8"))
        ops = lu["ops_completes"]
        sys.path.insert(0, os.path.join(racine, "programmes"))
        B = charger(os.path.join(copie, JUGE), "juge_cas_obs")
        cours = B.charger_cours(B.trouver(racine, "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN"))
        mnemo = B.table_mnemoniques(B.trouver(racine, "REFERENTIEL_VALEURS"))
        pos = B.charger_module(B.trouver(racine, "MODULE_POSITIONS.py"), "pos_cas_obs")

        class Arret(BaseException):
            """Arrête `juger` au pas qui suit OBSERVATIONS.

            ① RÔLE — Signal d'arrêt. ② CONTEXTE D'APPEL — levé par le mandataire à la coupure 70/30. ③ ENTRÉE — —
            ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — [rend: rien] ⑥ TRAITEMENT — — ⑦ UNITÉ — — ⑧ POURQUOI — une
            `BaseException` traverse les `except Exception` du juge : seul cet arrêt la rattrape. ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — — ⑪ TERMINAISON — — [sort: non]
            """

        class Mandataire:
            """Le module de jugement de la copie, sauf la coupure 70/30, qui arrête `juger`.

            ① RÔLE — Laisser `juger` appeler la vraie fonction de la copie, puis l'arrêter. ② CONTEXTE D'APPEL —
            passé à `juger` à la place du module. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — l'attribut
            demandé. [rend: 1] ⑥ TRAITEMENT — `coupure_70_30` lève `Arret` ; tout autre nom est lu dans le module de
            la copie. ⑦ UNITÉ — — ⑧ POURQUOI — le reste du juge (hasard, voisinage) coûte des minutes et n'éprouve
            rien ici. ⑨ CE QUI CLOCHE — si `juger` cessait d'appeler la coupure juste après OBSERVATIONS, l'arrêt
            viendrait plus tard ou jamais : le cas exige qu'il soit venu. ⑩ EFFET — — ⑪ TERMINAISON — rend la main
            ou lève `Arret`. [sort: non]
            """
            def __getattr__(self, nom):
                if nom == "coupure_70_30":
                    def arreter(*a, **k):
                        raise Arret()
                    return arreter
                return getattr(J, nom)
        sortie = io.StringIO()
        arrete = False
        try:
            with contextlib.redirect_stdout(sortie):
                B.juger(lu["fiche"], ops, cours, set(), Mandataire(), None, pos, mnemo, bareme=lu["bareme"])
        except Arret:
            arrete = True
        lignes = [l for l in sortie.getvalue().splitlines() if l.strip().startswith("OBSERVATIONS")]
        r = O(ops)
        attendu = ("OBSERVATIONS         %d operations . %.1f observations independantes retenues . groupes de %.2f "
                   "operation(s) . le plus petit de %.1f mesurees et %d periodes distinctes . %d paires de positions "
                   "ouvertes en meme temps" % (len(ops), r["n_observations"], r["taille_des_groupes"],
                                               r["observations_mesurees"], r["periodes_distinctes"],
                                               r["paires_qui_se_chevauchent"]))
        vu = {"juger arrêté APRÈS la ligne OBSERVATIONS": arrete,
              "une seule ligne OBSERVATIONS": len(lignes) == 1,
              "la ligne affiche le calcul de la fonction sur TOUTES les opérations": len(lignes) == 1
              and lignes[0].strip().startswith(attendu),
              "100 opérations": len(ops) == 100 and re.search(r"OBSERVATIONS +100 operations", lignes[0] if lignes
                                                                 else "") is not None}
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + \
            " · ligne du juge %r · attendu %r" % (lignes[0].strip() if lignes else None, attendu)
    un("E11 le juge (`juger` exécuté) affiche le nombre de la fonction sur toutes les opérations de C5", e11)

    def e12():
        vus = []
        for _ in range(2):
            o = []
            for b in range(2):
                choc = rng.gauss(0, 1000)
                o += [{"date_entree": jour(100 * b), "date_sortie": jour(100 * b + 5), "valeur": "V%d" % k,
                       "net": choc + rng.gauss(0, 1000)} for k in range(50)]
            r = O(o)
            vus.append((r["n_observations"], r["observations_mesurees"], r["periodes_distinctes"]))
        return (all(v[0] is not None and v[0] <= 2.0 and v[2] == 2 for v in vus),
                "(retenu, mesurées, K) par tirage : %r (vérité du relecteur 3,9 ; attendu : au plus 2, K = 2)" % vus)
    un("E12 deux paquets de 50 positions ouvertes ensemble, forte ressemblance : au plus 2 (K = 2)", e12)

    def e13():
        o = []
        for b in range(20):
            g = rng.gauss(0, 1000)
            o += [{"date_entree": jour(20 * b + 2 * c), "date_sortie": jour(20 * b + 2 * c + 2), "valeur": "V%d" % c,
                   "net": g} for c in range(5)]
        r = O(o)
        return (abs(r["n_observations"] - 100 / 2.6) < 1e-9 and abs(r["observations_mesurees"] - 100 / 2.6) < 1e-9
                and r["periodes_distinctes"] == 60 and r["paires_qui_se_chevauchent"] == 80,
                "retenu %r · mesurées %r · K %r · paires %r (vérité 38,46, 38,46, 60, 80)"
                % (r["n_observations"], r["observations_mesurees"], r["periodes_distinctes"],
                   r["paires_qui_se_chevauchent"]))
    un("E13 vingt chaînes de cinq positions qui se touchent : la MESURE mord (38,46), K = 60 et non 20 paquets", e13)

    def e14():
        ens = O([{"date_entree": jour(0), "date_sortie": jour(5), "valeur": "V%d" % k, "net": rng.gauss(0, 1000)}
                 for k in range(30)])
        iso = O([{"date_entree": jour(10 * k), "date_sortie": jour(10 * k + 5), "valeur": "V", "net": rng.gauss(0, 1000)}
                 for k in range(30)])
        return (ens["n_observations"] == 1.0 and ens["periodes_distinctes"] == 1 and iso["n_observations"] == 30.0
                and iso["periodes_distinctes"] == 30,
                "ensemble : retenu %r, mesurées %r, K %r (vérité 1, 30, 1) · isolées : retenu %r, K %r (vérité 30, 30)"
                % (ens["n_observations"], ens["observations_mesurees"], ens["periodes_distinctes"],
                   iso["n_observations"], iso["periodes_distinctes"]))
    un("E14 trente positions toutes ouvertes ensemble : 1 ; trente isolées : 30", e14)

    def e15():
        r = O([{"date_entree": jour(4 * k), "date_sortie": jour(4 * k + 3), "valeur": "V", "net": rng.gauss(0, 1000)}
               for k in range(50)])
        return (r["periodes_distinctes"] == 50 and r["n_observations"] == 50.0 and r["paires_qui_se_chevauchent"] == 0,
                "K %r · retenu %r · paires %r (vérité 50, 50, 0)"
                % (r["periodes_distinctes"], r["n_observations"], r["paires_qui_se_chevauchent"]))
    un("E15 un jeton (chaque entrée le lendemain de la sortie précédente) : K = N, la borne ne mord pas", e15)
    return res


def preparer(racine, sab):
    """Copie les deux programmes éprouvés et y applique un sabotage.

    ① RÔLE — Donner à chaque sabotage sa copie. ② CONTEXTE D'APPEL — le programme principal. ③ ENTRÉE — la racine,
    le nom du sabotage ou « Z0 ». ④ CONDITIONS D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — le
    dossier de la copie. [rend: 1] ⑥ TRAITEMENT — copier, remplacer. ⑦ UNITÉ — — ⑧ POURQUOI — une cible
    introuvable ne sabote rien : elle lève au lieu de passer pour un sabotage qui mord. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — crée un dossier temporaire. ⑪ TERMINAISON — rend la main ou lève `LookupError`. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="obs_%s_" % sab)
    os.makedirs(os.path.join(d, "programmes"))
    for f in (MODULE, JUGE):
        shutil.copy(os.path.join(racine, f), os.path.join(d, f))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            shutil.rmtree(d)
            raise LookupError("sabotage %s : le texte visé est présent %d fois dans %s" % (sab, t.count(a), f))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d


def main():
    """Programme principal : rejeu de C5, Z0, puis les sabotages demandés.

    ① RÔLE — Enchaîner l'épreuve. ② CONTEXTE D'APPEL — le lancement. ③ ENTRÉE — la ligne de commande (voir USAGE).
    ④ CONDITIONS D'ENTRÉE — voir le ④ du programme. ⑤ SORTIE — le code de sortie. [rend: 1] ⑥ TRAITEMENT — voir le ⑥
    du programme. ⑦ UNITÉ — — ⑧ POURQUOI — voir le ⑧ du programme. ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — dossiers temporaires, effacés. ⑪ TERMINAISON — chaque relance a un délai de 600 s ; elle rend la
    main, et c'est le bas du fichier qui sort du processus. [sort: non]
    """
    if len(sys.argv) > 4 and sys.argv[1] == "--cas":
        r = cas(sys.argv[2], sys.argv[3], sys.argv[4])
        for nom, v, d in r:
            print("  %s  %s — %s" % ("VERT " if v else "ROUGE", nom, d))
        return 0 if all(v for _, v, _ in r) else 1
    if len(sys.argv) < 2:
        print(__doc__.split("\n\n")[1])
        return 2
    racine = os.path.abspath(sys.argv[1])
    choix = sys.argv[2] if len(sys.argv) > 2 else None
    if choix not in (None, "--saboter") and choix not in SABOTAGES:
        print("ARRET : sabotage inconnu %r (connus : %s)" % (choix, ", ".join(SABOTAGES)))
        return 2
    travail = tempfile.mkdtemp(prefix="obs_ops_")
    f_ops = os.path.join(travail, "c5.json")
    try:
        try:
            ok, lignes = rejouer_c5(racine, f_ops)
        except Exception as ex:
            print("ARRET : le rejeu de C5 par le juge n'a pas pu tourner : %s: %s" % (type(ex).__name__, ex))
            return 2
        print("REJEU DE C5 PAR LE CALIBRAGE DU JUGE : %s" % ("VERT" if ok else "ROUGE"))
        for l in lignes:
            if "identiques" in l or "operations" in l.lower():
                print("  " + l.strip())
        if not ok:
            print("ARRET : le calibrage du juge est rouge, les opérations rejouées ne sont pas les étalons.")
            return 2
        a_jouer = ["Z0"] + (list(SABOTAGES) if choix == "--saboter" else ([choix] if choix else []))
        code = 0
        for sab in a_jouer:
            try:
                d = preparer(racine, sab)
            except LookupError as ex:
                print("ARRET : %s" % ex)
                return 2
            try:
                p = subprocess.run([sys.executable, "-B", ICI, "--cas", d, f_ops, racine], capture_output=True,
                                   text=True, timeout=600)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            rouges = [l for l in p.stdout.splitlines() if l.strip().startswith("ROUGE")]
            if sab == "Z0":
                print("Z0 — le dépôt tel quel : %s" % ("VERT" if p.returncode == 0 else "ROUGE"))
                print(p.stdout.rstrip())
                if p.stderr.strip():
                    print(p.stderr.rstrip())
                if p.returncode != 0:
                    code = 1
            else:
                mord = p.returncode != 0 and bool(rouges)
                print("%s %s — %s" % ("MORD   " if mord else "NE MORD PAS", sab,
                                       " | ".join(l.strip()[6:].split(" — ")[0] for l in rouges) or p.stderr.strip()[-200:]))
                if not mord:
                    code = 1
        print("CODE %d" % code)
        return code
    finally:
        shutil.rmtree(travail, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
