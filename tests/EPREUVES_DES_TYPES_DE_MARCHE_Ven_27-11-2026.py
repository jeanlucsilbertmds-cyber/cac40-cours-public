#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DES TYPES DE MARCHÉ — programmes/DATER_LES_TYPES_DE_MARCHE.py et ses contrats dans
programmes/CONTRATS_DES_FICHIERS.py (REGLAGES_DES_TYPES_DE_MARCHE, PARAMETRES_DES_TYPES_DE_MARCHE,
PAS_DE_TEMPS_DES_TYPES_DE_MARCHE, TYPES_DE_MARCHE, FIGEAGE_DES_TYPES_DE_MARCHE). Ven 27-11-2026 (Paris), lot L5 du
plan R505, refait par le lot L5-CORR d'après la relecture V1. Simulation uniquement.

① RÔLE — Éprouver chaque propriété du découpage par une épreuve, puis SABOTER le programme (une copie modifiée) et
  montrer que l'épreuve visée ROUGIT : une épreuve qui reste verte quand on retire ce qu'elle teste est une
  décoration.
② CONTEXTE D'APPEL — À la main : `python3 -B tests/EPREUVES_DES_TYPES_DE_MARCHE_Ven_27-11-2026.py <racine>`.
③ ENTRÉE — argv[1] : la racine du dépôt (porte donnees/, programmes/ et temoins/).
④ CONDITIONS D'ENTRÉE — Les fichiers de données lus par le programme existent sous la racine, et le témoin des
  20 ans (temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv) pour l'épreuve e14.
⑤ SORTIE — UN code de sortie : 0 si toutes les épreuves passent sur le programme ET si chaque sabotage fait
  rougir son épreuve ; 1 sinon (R-734 : un contrôle qui n'a pas pu tourner ne se tait pas).
⑥ TRAITEMENT — ① charger le programme · ② jouer les épreuves · ③ pour chaque sabotage : copier le programme et ses
  trois voisins dans un dossier temporaire, remplacer un fragment du code (le fragment DOIT exister une fois,
  sinon échec), rejouer l'épreuve visée, exiger qu'elle échoue.
⑦ UNITÉ — Séances, mois, points d'indice, logarithmes, fractions.
⑧ POURQUOI — R-731, R-732 (un cas au moins tiré d'une vraie ligne : 2000-09-04, 2003, 2008, 2018-2020, le
  2016-03-28 du témoin, les mesures du Chat du 27-11) ; défauts D1 à D9 de la relecture V1 du 27-11-2026 (les quatre
  sabotages qui restaient verts — égalités, levée en logarithme, `jusqu_au` exclusif, bord gauche — ont chacun
  ici une épreuve qui rougit).
⑨ CE QUI CLOCHE — Les épreuves sur données réelles s'arrêtent au 2026-10-02 (`FIN`) : un indice prolongé ne les
  change pas, mais elles ne disent rien des séances d'après. L'étalonnage e13 compare au portage du relecteur V1,
  pas au tableau de l'article (non lu).
⑩ EFFET — Écrit dans des dossiers temporaires, effacés à la fin ; ne touche pas la racine.
⑪ TERMINAISON — Rend la main ; chaque épreuve est bornée.
"""
import contextlib, csv, importlib.util, io, json, math, os, shutil, sys, tempfile, traceback

PROG = "DATER_LES_TYPES_DE_MARCHE"
VOISINS = ("CONTRATS_DES_FICHIERS", "CALENDRIER_DE_LA_BOURSE", "METEO_DU_MARCHE")
TEMPORAIRES = []
FIN = "2026-10-02"
TEMOIN = os.path.join("temoins", "TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv")
# Retournements rendus par le PORTAGE INDÉPENDANT du relecteur V1 (bbstkjae.prg en Python, V1_RELU_L5_outils/
# commun.py, sortie_port.txt du 27-11-2026), sur l'indice jusqu'au 2026-10-02 : au jour (8/4/16 mois en séances)…
PORTAGE_JOUR = [("2003-03-12", "CREUX"), ("2007-06-01", "SOMMET"), ("2009-03-09", "CREUX"), ("2011-02-18", "SOMMET"),
                ("2011-09-22", "CREUX"), ("2015-04-27", "SOMMET"), ("2016-02-11", "CREUX"), ("2020-02-19", "SOMMET"),
                ("2020-03-18", "CREUX"), ("2022-01-05", "SOMMET"), ("2022-09-29", "CREUX"), ("2024-05-15", "SOMMET"),
                ("2025-04-09", "CREUX")]
# … et au mois (cours de fin de mois, 8/4/16 mois tels quels).
PORTAGE_MOIS = [("2003-03", "CREUX"), ("2007-05", "SOMMET"), ("2009-02", "CREUX"), ("2011-02", "SOMMET"),
                ("2011-09", "CREUX"), ("2015-07", "SOMMET"), ("2016-06", "CREUX"), ("2019-12", "SOMMET"),
                ("2020-03", "CREUX"), ("2021-12", "SOMMET"), ("2022-09", "CREUX"), ("2024-03", "SOMMET"),
                ("2024-11", "CREUX"), ("2026-02", "SOMMET")]


def charger(dossier):
    """Charge le programme depuis un dossier.

    ① RÔLE — Avoir le programme original ou saboté sous la main.
    ② CONTEXTE D'APPEL — `main`, `saboter`.
    ③ ENTRÉE — `dossier` : le dossier qui porte le programme et ses trois voisins.
    ④ CONDITIONS D'ENTRÉE — Les quatre fichiers y sont.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, par chemin, sous un nom propre au dossier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le programme charge ses voisins depuis son propre dossier : la copie sabotée les trouve à côté.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut du module.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("epreuve_" + str(abs(hash(dossier))), os.path.join(dossier, PROG + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m



def racine_avec_reglages(racine, transformer):
    """Fabrique une fausse racine dont seul le fichier des réglages diffère.

    ① RÔLE — Éprouver la lecture des réglages sans toucher au dépôt.
    ② CONTEXTE D'APPEL — `e01_reglages`.
    ③ ENTRÉE — `racine` : la vraie racine · `transformer` : fonction qui reçoit les lignes du CSV et rend les lignes
      à écrire.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de la fausse racine (dossier temporaire).
      [rend: 1]
    ⑥ TRAITEMENT — copier donnees/sources_indice/INDICE_CAC40.csv, donnees/CALENDRIER_EURONEXT.csv et le fichier des
      réglages transformé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un réglage faux doit être refusé, pas deviné.
    ⑨ CE QUI CLOCHE — Le dossier est effacé par `main` à la fin ; une interruption brutale le laisse.
    ⑩ EFFET — Écrit un dossier temporaire.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    t = tempfile.mkdtemp(prefix="types_reglages_"); TEMPORAIRES.append(t)
    os.makedirs(os.path.join(t, "donnees", "sources_indice"))
    for rel in (os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv"), os.path.join("donnees", "CALENDRIER_EURONEXT.csv")):
        shutil.copy(os.path.join(racine, rel), os.path.join(t, rel))
    with open(os.path.join(racine, "donnees", "REGLAGES_DES_TYPES_DE_MARCHE.csv"), encoding="utf-8") as f:
        lignes = list(csv.reader(f))
    with open(os.path.join(t, "donnees", "REGLAGES_DES_TYPES_DE_MARCHE.csv"), "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(transformer(lignes))
    return t



def racine_avec_indice(racine, transformer):
    """Fabrique une fausse racine dont seul le fichier de l'indice diffère.

    ① RÔLE — Éprouver la lecture d'un découpage figé quand une séance de sa période a été révisée.
    ② CONTEXTE D'APPEL — `e15_periode_et_figeage`.
    ③ ENTRÉE — `racine` : la vraie racine · `transformer` : fonction qui reçoit les lignes du CSV de l'indice (listes)
      et rend les lignes à écrire.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de la fausse racine (dossier temporaire).
      [rend: 1]
    ⑥ TRAITEMENT — copier le calendrier et les réglages, écrire l'indice transformé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Les révisions du passé se détectent, elles ne se devinent pas. »
    ⑨ CE QUI CLOCHE — Le dossier est effacé par `main` à la fin ; une interruption brutale le laisse.
    ⑩ EFFET — Écrit un dossier temporaire.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    t = tempfile.mkdtemp(prefix="types_indice_"); TEMPORAIRES.append(t)
    os.makedirs(os.path.join(t, "donnees", "sources_indice"))
    for rel in (os.path.join("donnees", "CALENDRIER_EURONEXT.csv"), os.path.join("donnees", "REGLAGES_DES_TYPES_DE_MARCHE.csv")):
        shutil.copy(os.path.join(racine, rel), os.path.join(t, rel))
    rel = os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv")
    with open(os.path.join(racine, rel), encoding="utf-8") as f:
        lignes = list(csv.reader(f))
    with open(os.path.join(t, rel), "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(transformer(lignes))
    return t


def dates_brutes(racine):
    """Les dates du fichier de l'indice, relues ici sans le programme.

    ① RÔLE — Avoir une vérité lue à part pour confronter le programme.
    ② CONTEXTE D'APPEL — `e13_etalonnage`, `e14_dates_sans_type`, `e15_periode_et_figeage`.
    ③ ENTRÉE — `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des dates, dans l'ordre du fichier.
      [rend: 1]
    ⑥ TRAITEMENT — lecture CSV.
    ⑦ UNITÉ — Dates.
    ⑧ POURQUOI — R-732 : de vraies lignes.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(os.path.join(racine, "donnees", "sources_indice", "INDICE_CAC40.csv"), encoding="utf-8") as f:
        return [r["date"] for r in csv.DictReader(f)]


def doit_lever(f, *a):
    """Vérifie qu'un appel lève ValueError.

    ① RÔLE — Dire qu'un refus a bien eu lieu.
    ② CONTEXTE D'APPEL — Les épreuves de refus.
    ③ ENTRÉE — `f` : la fonction · `*a` : ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien : lève AssertionError si `f` ne lève pas ValueError.
      [rend: rien]
    ⑥ TRAITEMENT — appel.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    try:
        f(*a)
    except ValueError:
        return
    raise AssertionError(f"{f.__name__} n'a pas refusé")



def e01_reglages(m, racine):
    """Le fichier se lit, porte les valeurs de la règle publiée, et un fichier faux est refusé.

    ① RÔLE — Propriétés : les réglages viennent du fichier ; la censure est celle du CODE des auteurs (4 mois,
      défaut D5) ; la levée est en logarithme (unité « logarithme », défaut D4) ; le pas est déclaré (défaut D6) ;
      le paramètre inventé `retrait_dans_un_cycle` n'existe plus (défaut D1) ; un paramètre inconnu, manquant,
      doublé, dans une autre unité, ou un pas hors liste est refusé.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — lecture du vrai fichier, puis six fichiers faussés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un réglage mal écrit qui passerait en silence changerait tout le découpage.
    ⑨ CE QUI CLOCHE — Les valeurs du fichier sont des données : un sabotage du programme ne peut pas les fausser ;
      l'épreuve les fixe telles que décidées (A-1102) et corrigées (D5).
    ⑩ EFFET — Écrit des dossiers temporaires.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    r = m.lire_les_reglages(racine)
    # pas MENSUEL : décision de Jean-Luc du 28-11-2026 à 12h04 (A-1112, « par mois ») ; le quotidien n'est qu'affiché
    attendu = {"methode": "PS", "pas_de_temps": "mensuel", "fenetre_des_sommets": 8.0, "censure": 4.0,
               "phase_minimale": 4.0, "cycle_minimal": 16.0, "seuil_de_levee": 0.20, "durees_minimales": "oui"}
    assert all(r[k] == v for k, v in attendu.items()), r
    assert "retrait_dans_un_cycle" not in r, r
    assert dict(charger_contrats(m).PARAMETRES_DES_TYPES_DE_MARCHE)["seuil_de_levee"] == "logarithme"
    doit_lever(m.lire_les_reglages, racine_avec_reglages(racine, lambda l: l + [["inconnu", "1", "—", "", ""]]))
    doit_lever(m.lire_les_reglages, racine_avec_reglages(racine, lambda l: [x for x in l if x[0] != "censure"]))
    doit_lever(m.lire_les_reglages, racine_avec_reglages(racine, lambda l: l + [l[2]]))
    doit_lever(m.lire_les_reglages, racine_avec_reglages(
        racine, lambda l: [x if x[0] != "phase_minimale" else [x[0], x[1], "semaines"] + x[3:] for x in l]))
    doit_lever(m.lire_les_reglages, racine_avec_reglages(
        racine, lambda l: [x if x[0] != "pas_de_temps" else [x[0], "hebdomadaire"] + x[2:] for x in l]))
    doit_lever(m.lire_les_reglages, racine_avec_reglages(
        racine, lambda l: l + [["retrait_dans_un_cycle", "plus_faible_variation", "—", "", ""]]))


def e02_conversion(m, racine):
    """Les mois de l'article deviennent des séances au nombre MESURÉ de séances par mois.

    ① RÔLE — Propriété : aucune conversion écrite à la main.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — recompter les séances par mois depuis le fichier de l'indice, ligne à ligne, sans le programme.
    ⑦ UNITÉ — Séances par mois.
    ⑧ POURQUOI — R-728.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    with open(os.path.join(racine, "donnees", "sources_indice", "INDICE_CAC40.csv"), encoding="utf-8") as f:
        mois = [r["date"][:7] for r in csv.DictReader(f)]
    distincts = sorted(set(mois))[1:-1]
    attendu = sum(mois.count(x) for x in distincts) / len(distincts)
    dates, prix, _ = m.lire_l_indice(racine)
    # (28-11-2026, A-1112) le fichier porte le pas mensuel ; la conversion éprouvée ici est celle du pas quotidien, affiché
    d = m.durees_en_pas(dict(m.lire_les_reglages(racine), pas_de_temps="quotidien"), dates)
    assert abs(d["seances_par_mois"] - attendu) < 1e-9, (d, attendu)
    assert d["fenetre_des_sommets"] == round(8 * attendu) and d["cycle_minimal"] == round(16 * attendu), d



def e03_fenetre_entiere_et_censure(m, racine):
    """Un candidat est le plus haut (bas) de sa fenêtre ENTIÈRE ; la censure retire le premier et le dernier point
    trop près des bouts, aux bornes exactes du code des auteurs.

    ① RÔLE — Propriétés des étapes `dates1` (défaut D2 : jamais de fenêtre coupée) et `enfvbp` (défaut D5 : rang
      compté de 0, premier retiré si < c, dernier si ≥ n − c), sur des séries fabriquées.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : non lu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — ① série 1..10, 9..1, 2..10 : sommet au rang 9, creux au rang 18, rien d'autre (le 10 final est au
      bord) · ② série dont le maximum est au rang 1 : avec une fenêtre de 3, il n'est PAS candidat · ③ censure de 4
      sur 100 rangs : sommet au rang 3 et creux au rang 96 retirés, sommet au rang 4 et creux au rang 95 gardés.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.499 (`i=9; do while i <= nd-8`) et l.414-416 (`.<= 4`, `.> rows(x)-4`, rangs de 1).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    p = list(range(1, 11)) + list(range(9, 0, -1)) + list(range(2, 11))
    assert m.extremes_locaux(p, 3) == ([9], [18]), m.extremes_locaux(p, 3)
    q = [5, 9, 1, 2, 3, 4, 5, 6, 3, 2]
    assert 1 not in m.extremes_locaux(q, 3)[0], m.extremes_locaux(q, 3)
    x = [0.0] * 100
    for i in (3, 4, 50):
        x[i] = 1.0
    for i in (30, 95, 96):
        x[i] = -1.0
    assert m.censurer(x, [3, 50], [30, 96], 4) == ([50], [30]), m.censurer(x, [3, 50], [30, 96], 4)
    assert m.censurer(x, [4, 50], [30, 95], 4) == ([4, 50], [30, 95]), m.censurer(x, [4, 50], [30, 95], 4)


def e04_alternance_et_egalites(m, racine):
    """Deux sommets de suite : le plus haut reste ; deux creux : le plus bas ; À ÉGALITÉ, le premier sommet et le
    second creux restent, comme dans le code des auteurs.

    ① RÔLE — Propriétés de `alter2` (défaut D9-N1 : les égalités n'étaient gardées par aucune épreuve).
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : non lu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — listes fabriquées, avec et sans égalité.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.373 (`if x[d1,1] .>= x[d2,1]; s[j+1,1]=1` : second sommet retiré à égalité) et
      l.384 (`if x[d1,1] .>= x[d2,1]; s[j,1]=1` : premier creux retiré à égalité).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    p = [5, 9, 4, 12, 3, 1]
    assert m.alterner(p, [1, 3], [4, 5]) == ([3], [5]), m.alterner(p, [1, 3], [4, 5])
    e = [0, 7, 0, 7, 0, 0]
    assert m.alterner(e, [1, 3], [4, 5]) == ([1], [5]), m.alterner(e, [1, 3], [4, 5])


def e05_levee_en_logarithme(m, racine):
    """Une phase trop courte est retirée sauf si le LOGARITHME du cours a bougé de plus de la levée.

    ① RÔLE — Propriété de `enfve_2` (défaut D4) : +21 % en 5 séances (logarithme 0,191) est RETIRÉ ; −19 % en 5
      séances (logarithme −0,211) est GARDÉ — l'inverse de ce que donnerait une variation simple.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : non lu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — deux séries fabriquées passées par `dater_pagan_sossounov` entier (fenêtre 2, cycle 0, phase 8,
      censure 0, levée 0,20) : la conversion en logarithme est donc éprouvée dans la chaîne, pas seulement l'étape.
    ⑦ UNITÉ — Séances ; écart de logarithme.
    ⑧ POURQUOI — bbstkjae.prg l.241-242, `abs(x[nind]-x[cind]) .> .2` sur le logarithme des cours.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    monte = [110, 108, 106, 104, 102, 100, 104, 108, 112, 116, 121] + [121 - 3.1 * k for k in range(1, 11)] + \
            [90 + 4 * k for k in range(1, 11)] + [130 - 3.5 * k for k in range(1, 11)]
    got = m.dater_pagan_sossounov(monte, 2, 0, 8, 0, 0.20)
    assert got == [(20, m.CREUX), (30, m.SOMMET)], got
    baisse = [90, 92, 94, 96, 98, 100, 96, 92, 88, 84, 81] + [81 + 3 * k for k in range(1, 11)] + \
             [111 - 2 * k for k in range(1, 11)] + [91 + 2 * k for k in range(1, 11)]
    got = m.dater_pagan_sossounov(baisse, 2, 0, 8, 0, 0.20)
    assert (5, m.SOMMET) in got and (10, m.CREUX) in got, got


def e06_cycles_regle_des_auteurs(m, racine):
    """D'un cycle trop court, on garde le PLUS HAUT sommet et le PLUS BAS creux ; à égalité, le second.

    ① RÔLE — Propriété de `enf1p` (défaut D1 : remplace le paramètre inventé `retrait_dans_un_cycle`).
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : non lu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — ① sommets aux rangs 10 et 30 (cycle 20 < 40) : le plus haut reste, quel que soit son rang ; à
      égalité, celui du rang 30 ; l'alternance qui suit garde le plus bas des deux creux restés côte à côte ·
      ② sommets 5, 45, 85 (cycles de 40, pas < 40 : intacts) et creux 20 et 50 (30 < 40) : le plus bas creux reste ;
      à égalité, celui du rang 50.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.277-278, « If Violated, choose highest peak and lowest trough », et l.285 / l.296
      (`if x[d1,1] .> x[d2,1]` : à égalité, le premier part).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    x = [0.0] * 80
    x[10], x[30], x[20], x[60] = 5.0, 6.0, 1.0, 1.0
    assert m.cycles_minimaux(x, [10, 30], [20, 60], 40) == ([30], [20, 60]), m.cycles_minimaux(x, [10, 30], [20, 60], 40)
    x[10], x[30] = 7.0, 6.0
    assert m.cycles_minimaux(x, [10, 30], [20, 60], 40) == ([10], [60]), m.cycles_minimaux(x, [10, 30], [20, 60], 40)
    x[10] = 6.0
    assert m.cycles_minimaux(x, [10, 30], [20, 60], 40) == ([30], [20, 60]), "égalité de sommets"
    y = [0.0] * 90
    y[5], y[45], y[85], y[20], y[50] = 5.0, 6.0, 5.0, 1.0, 2.0
    assert m.cycles_minimaux(y, [5, 45, 85], [20, 50], 40) == ([5, 45], [20]), m.cycles_minimaux(y, [5, 45, 85], [20, 50], 40)
    y[20], y[50] = 2.0, 1.0
    assert m.cycles_minimaux(y, [5, 45, 85], [20, 50], 40) == ([45, 85], [50]), m.cycles_minimaux(y, [5, 45, 85], [20, 50], 40)
    y[20] = 1.0
    assert m.cycles_minimaux(y, [5, 45, 85], [20, 50], 40) == ([45, 85], [50]), "égalité de creux"


def e07_cas_reels(m, racine):
    """Cas réels lus dans les données : le haut de 2000, le bas de 2003, 2008, 2018-2020.

    ① RÔLE — R-732 et défauts D1, D2 : ① aucun point à moins d'une demi-fenêtre des bouts ; la plus haute clôture
      de 2000 (2000-09-04, rang 170, sous la demi-fenêtre de 171) n'est PAS un sommet, comme chez les auteurs ; la
      plus basse de 2003 est le premier point, un creux, et tout ce qui le précède est en BAISSE · ② la plus haute
      clôture de 2007 est un sommet, la plus basse de 2008-2009 un creux, tout entre les deux en BAISSE · ③ la plus
      basse de 2018 (2018-12-27) N'EST PAS un creux : son cycle avec le creux de 2020 dure moins de 16 mois et la
      règle des auteurs garde le plus bas, celui de 2020 ; la plus haute de janvier-février 2020 est un sommet.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — Les données couvrent 2000-2020.
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — dates des extrêmes calculées sur les clôtures, jamais écrites ; découpage jusqu'au `FIN`.
    ⑦ UNITÉ — Dates, rangs.
    ⑧ POURQUOI — Relecture V1 : le portage du programme des auteurs ne date pas le 2000-09-04 ; l'ancien L5 le
      datait (fenêtre coupée), et ~170 séances de 2000 changeaient de sens.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les données.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    # (28-11-2026, A-1112) cas réels relevés au pas QUOTIDIEN, désormais seulement affiché : le pas est donné ici ; le
    # pas mensuel décidé est éprouvé par l'étalonnage (e13, les 14 points des auteurs)
    lignes, ctx = m.dater(racine, {"pas_de_temps": "quotidien"}, jusqu_au=FIN)
    ext = lambda debut, fin, f: f([l for l in lignes if debut <= l["date"] <= fin], key=lambda l: l["cloture"])["date"]
    pts = dict(ctx["points"]); rang = {l["date"]: k for k, l in enumerate(lignes)}
    f, n = ctx["durees"]["fenetre_des_sommets"], len(lignes)
    assert all(f <= rang[d] <= n - 1 - f for d in pts), (f, ctx["points"])
    s00 = ext("2000-01-01", "2000-12-31", max)
    assert s00 == "2000-09-04" and rang[s00] < f and s00 not in pts, (s00, rang[s00], f)
    c03 = ext("2003-01-01", "2003-12-31", min)
    assert ctx["points"][0] == (c03, m.CREUX), (c03, ctx["points"][:2])
    assert all(l["sens"] == m.BAISSE for l in lignes if l["date"] <= c03)
    s07, c09 = ext("2007-01-01", "2007-12-31", max), ext("2008-01-01", "2009-12-31", min)
    assert pts.get(s07) == m.SOMMET and pts.get(c09) == m.CREUX, (s07, c09, ctx["points"])
    assert all(l["sens"] == m.BAISSE for l in lignes if s07 < l["date"] <= c09)
    c18 = ext("2018-01-01", "2018-12-31", min)
    c20, s20 = ext("2020-01-01", "2020-12-31", min), ext("2020-01-01", "2020-02-29", max)
    assert c18 not in pts and pts.get(c20) == m.CREUX and pts.get(s20) == m.SOMMET, (c18, c20, s20, ctx["points"])


def e08_agitation(m, racine):
    """La séance de plus forte variation de 2020 est AGITÉE ; la part d'agité vaut 1 − centile.

    ① RÔLE — Propriété du calme/agité, sur un cas réel lu dans les données.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — la séance de plus grande |variation| en 2020 est cherchée sur les clôtures.
    ⑦ UNITÉ — Fraction.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les données.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    lignes, ctx = m.dater(racine)
    i = max((k for k in range(1, len(lignes)) if lignes[k]["date"][:4] == "2020"),
            key=lambda k: abs(lignes[k]["cloture"] / lignes[k - 1]["cloture"] - 1))
    assert lignes[i]["agitation"] == m.AGITE, lignes[i]
    connues = [l for l in lignes if l["agitation"] != m.INCONNUE]
    part = sum(1 for l in connues if l["agitation"] == m.AGITE) / len(connues)
    assert abs(part - (1 - ctx["reglages"]["centile_d_agitation"])) < 2 / len(connues), part



def e09_mesures_du_chat(m, racine):
    """Le programme reproduit les mesures du Chat du 27-11-2026 (étalonnage de l'instrument).

    ① RÔLE — Avec la méthode LT, seuils égaux, sans durées minimales : cycles 17, 8, 6 et baisses médianes 84, 152,
      152 séances aux seuils 15, 20, 25 % ; hausses médianes, phase ouverte de la fin comprise, 482,5 et 709 à 20 et
      25 % ; épisodes agités/calmes médians 7,5/20 sur 20 séances et 18,5/58 sur 60. L'écart connu (hausse médiane
      à 15 % : 167 ici, 130 chez le Chat) est vérifié tel quel, pour qu'un changement se voie.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — six découpages.
    ⑦ UNITÉ — Séances.
    ⑧ POURQUOI — Mandat L5 point 4 : calibrer l'instrument sur un cas connu.
    ⑨ CE QUI CLOCHE — Le Chat arrondissait (7,5 → 8 ; 18,5 → 18 ; 482,5 → 482) : arrondi au pair de Python.
    ⑩ EFFET — Lit les données.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    attendu = {0.15: (17, 84, 167), 0.20: (8, 152, 482.5), 0.25: (6, 152, 709)}
    for seuil, (cy, ba, ha) in attendu.items():
        mm = m.mesurer(m.dater(racine, {"methode": "LT", "durees_minimales": "non", "seuil_de_hausse": seuil,
                                        "seuil_de_baisse": seuil})[0])
        assert (mm["cycles_sommet_a_sommet"], mm["baisse_mediane"], mm["hausse_mediane_avec_fin"]) == (cy, ba, ha), (seuil, mm)
    for fen, (a, c) in {20: (7.5, 20), 60: (18.5, 58)}.items():
        mm = m.mesurer(m.dater(racine, {"fenetre_de_volatilite": fen})[0])
        assert (mm["agite_median"], mm["calme_median"]) == (a, c), (fen, mm)



def e10_forme_de_la_sortie(m, racine):
    """Une ligne par séance, types admis, époques qui se suivent, seules les phases des bords sont ouvertes.

    ① RÔLE — Propriétés de la sortie, que liront les autres programmes.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — comptes et parcours ; le nombre de lignes est celui du fichier de l'indice, relu ici.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les données.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    c = charger_contrats(m)
    lignes, ctx = m.dater(racine)
    with open(os.path.join(racine, "donnees", "sources_indice", "INDICE_CAC40.csv"), encoding="utf-8") as f:
        brut = list(csv.DictReader(f))
    assert len(lignes) == len(brut), (len(lignes), len(brut))
    assert ctx["seances_bnains"] == sum(1 for r in brut if not r["yahoo"]), ctx["seances_bnains"]
    assert all(l["type"] in c.TYPES_DE_MARCHE_ADMIS for l in lignes)
    assert all(set(l) == set(c.TYPES_DE_MARCHE) for l in lignes)
    ep = [l["epoque"] for l in lignes]
    assert ep[0] == 1 and all(b - a in (0, 1) for a, b in zip(ep, ep[1:])), "époques"
    ouvertes = {l["epoque"] for l in lignes if l["phase_terminee"] == 0}
    assert ouvertes == {1, ep[-1]}, ouvertes
    assert all(l["type"].startswith(l["sens"]) or l["type"] == "INCONNU" for l in lignes)



def charger_contrats(m):
    """Charge les contrats comme le programme les charge.

    ① RÔLE — Lire le contrat sans le recopier.
    ② CONTEXTE D'APPEL — `e10_forme_de_la_sortie`, `e11_ecriture`.
    ③ ENTRÉE — `m` : le module du programme.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module des contrats.
      [rend: 1]
    ⑥ TRAITEMENT — appel de `_module` du programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    return m._module("CONTRATS_DES_FICHIERS")



def e11_ecriture_et_code_de_sortie(m, racine):
    """`ecrire` écrit l'en-tête du contrat ; une racine sans données rend 2.

    ① RÔLE — R-734 et contrat de sortie.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — `main` vers un fichier temporaire, puis sur un dossier vide, affichage capturé (il porte des
      chemins temporaires qui changent à chaque passage).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier temporaire.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    TEMPORAIRES.extend([tempfile.mkdtemp(prefix="types_sortie_"), tempfile.mkdtemp(prefix="types_vide_")])
    sortie = os.path.join(TEMPORAIRES[-2], "types.csv")
    with contextlib.redirect_stdout(io.StringIO()):
        code_ecrit, code_vide = m.main(["x", racine, "ecrire", sortie]), m.main(["x", TEMPORAIRES[-1]])
    assert code_ecrit == 0 and code_vide == 2, (code_ecrit, code_vide)
    with open(sortie, encoding="utf-8") as f:
        assert next(csv.reader(f)) == list(charger_contrats(m).TYPES_DE_MARCHE)



def e12_bords(m, racine):
    """Un premier (dernier) sommet plus bas que le premier (dernier) cours n'est pas un sommet ; de même un creux.

    ① RÔLE — Propriété de `enfvcp` (défaut D3, L5-1 de Cowork), sur la fonction ET dans la chaîne entière.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : non lu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — ① premier point sommet (9) sous le premier cours (10) : retiré · ② dernier point creux (2)
      au-dessus du dernier cours (1) : retiré · ③ une série dont le premier candidat est un sommet à 120 après un
      départ à 200 : `dater_pagan_sossounov` ne le garde pas · ④ premier point creux (1,0) au-dessus du premier cours
      (0,5) : retiré (SN1 de la relecture V1 du 28-11-2026).
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.434-480, appelé l.587.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    x = [0.0] * 25
    x[0], x[5], x[8], x[15], x[20], x[24] = 10.0, 9.0, 1.0, 8.0, 2.0, 3.0
    assert m.bords(x, [5, 15], [8, 20]) == ([15], [8, 20]), m.bords(x, [5, 15], [8, 20])
    x[24] = 1.0
    assert m.bords(x, [5, 15], [8, 20]) == ([15], [8]), m.bords(x, [5, 15], [8, 20])
    p = [200, 100, 110, 120, 110, 100, 90, 100, 130, 150, 140, 120, 100, 110, 120]
    got = m.dater_pagan_sossounov(p, 2, 0, 0, 0, 0.20, durees_minimales=False)
    assert got == [(6, m.CREUX), (9, m.SOMMET), (12, m.CREUX)], got
    # ④ (28-11-2026, SN1 de la relecture V1 : sabotage « premier creux jamais retiré » resté vert) : le premier point
    # est un CREUX (1,0) au-dessus du premier cours (0,5) : retiré ; le dernier creux (0,2), sous le dernier cours, reste
    y = [0.0] * 15
    y[0], y[3], y[6], y[10], y[14] = 0.5, 1.0, 9.0, 0.2, 0.5
    assert m.bords(y, [6], [3, 10]) == ([6], [10]), m.bords(y, [6], [3, 10])


def e13_etalonnage(m, racine):
    """Le programme rend les mêmes retournements que le portage indépendant du relecteur V1, au jour et au mois.

    ① RÔLE — Étalonnage obligatoire (mandat L5-CORR) : au pas quotidien, les 13 points du portage ; au pas mensuel
      (`pas_de_temps` = mensuel), ses 14 points, chacun reporté sur la DERNIÈRE séance de son mois.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — L'indice couvre 2000-01-03 → `FIN`.
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — ① une série fabriquée de 20 cours (fenêtre 1, cycle 4, sans phase ni censure), dont le
      résultat attendu a été rendu par le portage du relecteur (commun.findates, 27-11-2026) : elle n'est juste que
      si les cycles sont appliqués DEUX fois, comme chez les auteurs (l.572 et l.589) — sur l'indice, sauter le
      second passage ne change rien · ② deux découpages jusqu'au `FIN`, comparés aux listes `PORTAGE_JOUR` et
      `PORTAGE_MOIS` ; la dernière séance de chaque mois est relue dans le fichier, sans le programme.
    ⑦ UNITÉ — Dates.
    ⑧ POURQUOI — Défaut D6 : le pas est un choix ; le mensuel des auteurs doit être programmé juste pour que la
      sensibilité affichée soit vraie.
    ⑨ CE QUI CLOCHE — Le portage du relecteur n'a pas été relu par un tiers (V1, §4).
    ⑩ EFFET — Lit les données.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    serie = [23, 26, 30, 14, 13, 24, 26, 19, 15, 30, 5, 29, 12, 4, 2, 5, 16, 7, 9, 22]
    got = m.dater_pagan_sossounov(serie, 1, 4, 0, 0, 0.20)
    assert got == [(2, m.SOMMET), (4, m.CREUX), (9, m.SOMMET), (14, m.CREUX)], got
    _, ctx = m.dater(racine, {"pas_de_temps": "quotidien"}, jusqu_au=FIN)
    assert ctx["points"] == PORTAGE_JOUR, ctx["points"]
    # (28-11-2026, A-1112) le pas MENSUEL est celui du fichier des réglages : la datation SANS surcharge doit rendre
    # les 14 points des auteurs
    _, ctx = m.dater(racine, jusqu_au=FIN)
    assert [(d[:7], s) for d, s in ctx["points"]] == PORTAGE_MOIS, ctx["points"]
    brut = [d for d in dates_brutes(racine) if d <= FIN]
    fins = {d[:7]: d for d in brut}
    assert all(fins[d[:7]] == d for d, _ in ctx["points"]), ctx["points"]


def e14_dates_sans_type(m, racine):
    """Une date sans séance de l'indice rend le type INCONNU, avec son motif ; jamais rangée d'office.

    ① RÔLE — Défaut D7 (bloquant pour le branchement au juge) : les 28 dates du témoin des 20 ans après la dernière
      séance de l'indice, et le 2016-03-28 (lundi de Pâques, une seule ligne au témoin), sont INCONNUES.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — Le témoin des 20 ans existe (`TEMOIN`).
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — ① dates fabriquées (veille de l'indice, dernière séance, après) · ② toutes les dates du témoin
      relues : celles que l'indice n'a pas sont INCONNUES, avec « après la dernière séance datée » ou « pas une
      séance de l'indice » ; celles qu'il a gardent leur type.
    ⑦ UNITÉ — Dates.
    ⑧ POURQUOI — R-505 v2, étape 3 : « un jour sans type de marché n'est jamais rangé d'office dans un type ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les données et le témoin (23 Mo).
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    lignes, _ = m.dater(racine)
    t, mo = m.types_aux_dates(lignes, ["1999-12-31", lignes[0]["date"], lignes[-1]["date"], "2026-11-11"])
    assert t["1999-12-31"] == "INCONNU" and mo["1999-12-31"] == "avant la première séance datée", (t, mo)
    assert t[lignes[0]["date"]] == "INCONNU" and mo[lignes[0]["date"]] == "volatilité pas encore connue", (t, mo)
    assert t[lignes[-1]["date"]] == lignes[-1]["type"] != "INCONNU", (t, mo)
    assert t["2026-11-11"] == "INCONNU" and mo["2026-11-11"] == "après la dernière séance datée", (t, mo)
    with open(os.path.join(racine, TEMOIN), encoding="utf-8") as f:
        temoin = sorted({r["date"] for r in csv.DictReader(f)})
    indice = set(dates_brutes(racine))
    sans = [d for d in temoin if d not in indice]
    assert "2016-03-28" in sans and "2026-11-11" in sans, sans[:3]
    t, mo = m.types_aux_dates(lignes, temoin)
    assert all(t[d] == "INCONNU" for d in sans), [(d, t[d]) for d in sans if t[d] != "INCONNU"][:3]
    assert mo["2016-03-28"] == "pas une séance de l'indice", mo["2016-03-28"]
    par_date = {l["date"]: l["type"] for l in lignes}
    assert all(t[d] == par_date[d] for d in temoin if d in indice)


def e15_periode_et_figeage(m, racine):
    """`jusqu_au` est INCLUS ; `figer` écrit un découpage figé avec ses empreintes, refuse d'écraser et de dater
    au-delà de l'indice ; `lire_le_fige` refuse un CSV modifié et une séance révisée dans la période.

    ① RÔLE — Défaut D8 : la datation dépend de la fin des données ; elle se fige sur une période déclarée (A-1063,
      A-1064 ⑤). Défaut D9-N5 : `jusqu_au` n'était éprouvé par rien.
    ② CONTEXTE D'APPEL — `EPREUVES`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; lève si la propriété est fausse.
      [rend: rien]
    ⑥ TRAITEMENT — ① `jusqu_au` = une vraie séance (rang 4 790 du fichier) : la dernière ligne rendue est elle, et le
      nombre de lignes celui du fichier jusqu'à elle · ② figer jusqu'à cette séance dans un dossier temporaire :
      fiche aux clés du contrat, CSV identique au découpage, relu sans erreur, y compris contre la racine ·
      ③ refiger au même chemin : refusé · ④ figer au 2026-11-11 (après l'indice) : refusé · ⑤ une séance de la
      période révisée dans une fausse racine : refusé ; une séance APRÈS la période : accepté · ⑥ une ligne du CSV
      modifiée : refusé.
    ⑦ UNITÉ — Dates.
    ⑧ POURQUOI — Relecture V1 : dater les seuls 70 % change le type de 214 des 4 790 séances.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit des dossiers temporaires.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    brut = dates_brutes(racine)
    j = brut[4790]
    lignes, ctx = m.dater(racine, jusqu_au=j)
    assert lignes[-1]["date"] == j and len(lignes) == sum(1 for d in brut if d <= j), (lignes[-1]["date"], j)
    t = tempfile.mkdtemp(prefix="types_fige_"); TEMPORAIRES.append(t)
    chemin = os.path.join(t, "types.csv")
    fiche = m.figer(racine, j, chemin)
    assert tuple(fiche) == tuple(charger_contrats(m).FIGEAGE_DES_TYPES_DE_MARCHE), tuple(fiche)
    relu, f2 = m.lire_le_fige(chemin, racine)
    assert f2["empreinte_entree"] == ctx["empreinte_entree"] and len(relu) == len(lignes)
    assert all(a["type"] == b["type"] and a["date"] == b["date"] for a, b in zip(relu, lignes))
    doit_lever(m.figer, racine, j, chemin)
    doit_lever(m.figer, racine, "2026-11-11", os.path.join(t, "apres.csv"))
    rang_dans = 1 + 100
    revise = racine_avec_indice(racine, lambda l: [x if k != rang_dans else [x[0], x[1], str(float(x[2] or x[1]) + 1)]
                                                    for k, x in enumerate(l)])
    doit_lever(m.lire_le_fige, chemin, revise)
    apres = racine_avec_indice(racine, lambda l: l[:-1] + [[l[-1][0], l[-1][1], str(float(l[-1][2]) + 1)]])
    m.lire_le_fige(chemin, apres)
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte.replace("HAUSSE_CALME", "BAISSE_CALME", 1))
    doit_lever(m.lire_le_fige, chemin)


EPREUVES = [e01_reglages, e02_conversion, e03_fenetre_entiere_et_censure, e04_alternance_et_egalites,
            e05_levee_en_logarithme, e06_cycles_regle_des_auteurs, e07_cas_reels, e08_agitation, e09_mesures_du_chat,
            e10_forme_de_la_sortie, e11_ecriture_et_code_de_sortie, e12_bords, e13_etalonnage, e14_dates_sans_type,
            e15_periode_et_figeage]

# (nom, fragment du code, remplacement, épreuve qui doit rougir)
SABOTAGES = [
    ("réglage : unité non contrôlée", "if unite != attendus[nom]:", "if False:", e01_reglages),
    ("réglage : doublon accepté (V1 N6)", "if nom in lu:", "if False:", e01_reglages),
    ("réglage : pas hors liste accepté", "if valeur not in c.PAS_DE_TEMPS_DES_TYPES_DE_MARCHE:", "if False:", e01_reglages),
    ("conversion : 21 séances par mois écrites à la main", "return sum(par_mois[m] for m in pleins) / len(pleins)",
     "return 21.0", e02_conversion),
    ("conversion : troncature au lieu d'arrondi (V1 N2)", "out = {k: int(round(reglages[k] * spm)) for k in noms}",
     "out = {k: int(reglages[k] * spm) for k in noms}", e02_conversion),
    ("fenêtre coupée aux bords (V1 N7, D2)",
     "for i in range(fenetre, n - fenetre):\n        fen = x[i - fenetre:i + fenetre + 1]",
     "for i in range(n):\n        fen = x[max(0, i - fenetre):i + fenetre + 1]", e03_fenetre_entiere_et_censure),
    ("fenêtre coupée aux bords, sur le cas réel du 2000-09-04 (D2)",
     "for i in range(fenetre, n - fenetre):\n        fen = x[i - fenetre:i + fenetre + 1]",
     "for i in range(n):\n        fen = x[max(0, i - fenetre):i + fenetre + 1]", e07_cas_reels),
    ("censure retirée", "return alterner(x, _bouts(sommets, n, censure), _bouts(creux, n, censure))", "return alterner(x, sommets, creux)",
     e03_fenetre_entiere_et_censure),
    ("censure : borne du début décalée (D5)", "if garde and garde[0] < censure:", "if garde and garde[0] <= censure:",
     e03_fenetre_entiere_et_censure),
    ("censure seulement au début (V1 N10)", "    if garde and garde[-1] >= n - censure:\n        garde.pop()\n", "",
     e03_fenetre_entiere_et_censure),
    ("alternance : garde le plus bas des sommets", "del an[j + 1 if x[d1] >= x[d2] else j]",
     "del an[j if x[d1] >= x[d2] else j + 1]", e04_alternance_et_egalites),
    ("égalité de sommets : le second gardé (V1 N1)", "del an[j + 1 if x[d1] >= x[d2] else j]",
     "del an[j + 1 if x[d1] > x[d2] else j]", e04_alternance_et_egalites),
    ("égalité de creux : le premier gardé (V1 N1)", "del an[j if x[d1] >= x[d2] else j + 1]",
     "del an[j if x[d1] > x[d2] else j + 1]", e04_alternance_et_egalites),
    ("levée en variation simple (V1 N3, D4)", "if s - c < phase_min and not abs(x[s] - x[c]) > levee:",
     "if s - c < phase_min and not abs(math.exp(x[s] - x[c]) - 1) > levee:", e05_levee_en_logarithme),
    ("cours sans logarithme (D4)", "    x = [math.log(p) for p in prix]\n    sommets, creux = extremes_locaux(x, fenetre)",
     "    x = list(prix)\n    sommets, creux = extremes_locaux(x, fenetre)", e05_levee_en_logarithme),
    ("levée ignorée", "if s - c < phase_min and not abs(x[s] - x[c]) > levee:", "if s - c < phase_min:",
     e05_levee_en_logarithme),
    ("cycle : garde le plus bas des sommets (D1)", "del sommets[i if x[sommets[i - 1]] > x[sommets[i]] else i - 1]",
     "del sommets[i if x[sommets[i - 1]] < x[sommets[i]] else i - 1]", e06_cycles_regle_des_auteurs),
    ("cycle : garde le plus haut des creux (D1)", "del creux[i if x[creux[i - 1]] < x[creux[i]] else i - 1]",
     "del creux[i if x[creux[i - 1]] > x[creux[i]] else i - 1]", e06_cycles_regle_des_auteurs),
    ("cycle : garde le plus haut des creux, sur le cas réel 2018-2020 (D1)",
     "del creux[i if x[creux[i - 1]] < x[creux[i]] else i - 1]",
     "del creux[i if x[creux[i - 1]] > x[creux[i]] else i - 1]", e07_cas_reels),
    ("cycle : égalité de sommets, le second retiré", "del sommets[i if x[sommets[i - 1]] > x[sommets[i]] else i - 1]",
     "del sommets[i if x[sommets[i - 1]] >= x[sommets[i]] else i - 1]", e06_cycles_regle_des_auteurs),
    ("cycle : égalité de creux, le second retiré", "del creux[i if x[creux[i - 1]] < x[creux[i]] else i - 1]",
     "del creux[i if x[creux[i - 1]] <= x[creux[i]] else i - 1]", e06_cycles_regle_des_auteurs),
    ("cycle minimal ignoré", "if sommets[i] - sommets[i - 1] < cycle_min:", "if False:", e06_cycles_regle_des_auteurs),
    ("sens de la première phase inversé (V1 N4)", "sens_phases = [HAUSSE if pts[0][1] == SOMMET else BAISSE]",
     "sens_phases = [BAISSE if pts[0][1] == SOMMET else HAUSSE]", e07_cas_reels),
    ("séance du sommet rattachée à la baisse (V1 N12)", "        for i in range(bornes[e] + 1, bornes[e + 1] + 1):",
     "        for i in range(max(0, bornes[e]), bornes[e + 1] + (1 if e == len(bornes) - 2 else 0)):", e07_cas_reels),
    ("agitation inversée", "(AGITE if v > seuil else CALME)", "(AGITE if v < seuil else CALME)", e08_agitation),
    ("seuil d'agitation : centile 0,75 écrit (V1 N11)", "return connues[min(len(connues) - 1, int(centile * len(connues)))]",
     "return connues[min(len(connues) - 1, int(0.75 * len(connues)))]", e08_agitation),
    ("volatilité : écart-type remplacé par la moyenne des écarts absolus",
     "out[i] = math.sqrt(sum((a - m) ** 2 for a in x) / fenetre)", "out[i] = sum(abs(a - m) for a in x) / fenetre",
     e09_mesures_du_chat),
    ("bnains oublié", "prix.append(bnains[d]); de_bnains += 1", "continue", e10_forme_de_la_sortie),
    ("phases des bords déclarées terminées", "terminee = 0 if e in (0, len(bornes) - 2) else 1", "terminee = 1",
     e10_forme_de_la_sortie),
    ("échec rendu 0", "        return 2\n\n\nif __name__", "        return 0\n\n\nif __name__",
     e11_ecriture_et_code_de_sortie),
    ("étape des bords sautée (D3)", "    sommets, creux = bords(x, sommets, creux)\n", "", e12_bords),
    ("bords : premier sommet jamais retiré (D3)", "            if x[0] > x[sommets[0]]:", "            if False:", e12_bords),
    ("bords : dernier creux jamais retiré (D3)", "        elif x[-1] < x[creux[-1]]:", "        elif False:", e12_bords),
    ("bords : premier creux jamais retiré (SN1 de V1, 28-11-2026)", "        elif x[0] < x[creux[0]]:", "        elif False:",
     e12_bords),
    ("pas mensuel : point non reporté sur la fin de mois", "        pts = [(rangs[i], s) for i, s in pts]",
     "        pts = [(i, s) for i, s in pts]", e13_etalonnage),
    ("second passage des cycles sauté",
     "    if durees_minimales:\n        sommets, creux = cycles_minimaux(x, sommets, creux, cycle_min)\n        sommets, creux = phases_minimales",
     "    if durees_minimales:\n        sommets, creux = phases_minimales", e13_etalonnage),
    ("date sans séance rangée dans le type de la veille (D7)", "        t = par_date.get(d, \"INCONNU\")",
     "        t = par_date.get(d) or next((par_date[x] for x in sorted(par_date, reverse=True) if x < d), \"INCONNU\")",
     e14_dates_sans_type),
    ("jusqu_au exclusif (V1 N5, D8)", "jours = [d for d in jours if d <= jusqu_au]",
     "jours = [d for d in jours if d < jusqu_au]", e15_periode_et_figeage),
    ("figé : écrasement accepté (D8)", "        if os.path.exists(x):\n            raise", "        if False:\n            raise",
     e15_periode_et_figeage),
    ("figé : fin après l'indice acceptée (D7, D8)", "    if jusqu_au > tous[-1]:", "    if False:", e15_periode_et_figeage),
    ("figé : CSV modifié accepté (D8)", "    if _sha(chemin) != fiche[\"empreinte_sortie\"]:", "    if False:",
     e15_periode_et_figeage),
    ("figé : séance révisée acceptée (D8)", "        if empreinte_de_l_entree(dates, prix) != fiche[\"empreinte_entree\"]:",
     "        if False:", e15_periode_et_figeage),
]


def jouer(m, racine, epreuve):
    """Joue une épreuve et dit si elle passe.

    ① RÔLE — Rendre un verdict sans arrêter le reste.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : le module · `racine` : la racine · `epreuve` : la fonction d'épreuve.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : vrai si elle passe, et le texte de l'erreur (vide si elle passe).
      [rend: 2]
    ⑥ TRAITEMENT — appel sous try.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ceux de l'épreuve.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        epreuve(m, racine)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:160]}"



def saboter(racine, fragment, remplacement):
    """Fabrique une copie sabotée du programme et la charge.

    ① RÔLE — Retirer ou fausser ce qu'une épreuve teste.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : la racine (porte programmes/) · `fragment` : le texte à remplacer · `remplacement` : le
      texte qui le remplace.
    ④ CONDITIONS D'ENTRÉE — Le fragment existe exactement une fois dans le programme ; sinon le sabotage lui-même est
      périmé, et c'est un échec.
    ⑤ SORTIE — UNE valeur : le module saboté.
      [rend: 1]
    ⑥ TRAITEMENT — copier les quatre fichiers dans un dossier temporaire, remplacer, charger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un dossier temporaire.
    ⑪ TERMINAISON — Rend la main ou lève AssertionError.
      [sort: non]
    """
    t = tempfile.mkdtemp(prefix="types_sabotage_"); TEMPORAIRES.append(t)
    for nom in VOISINS:
        shutil.copy(os.path.join(racine, "programmes", nom + ".py"), t)
    with open(os.path.join(racine, "programmes", PROG + ".py"), encoding="utf-8") as f:
        code = f.read()
    assert code.count(fragment) == 1, f"fragment absent ou multiple : {fragment!r}"
    with open(os.path.join(t, PROG + ".py"), "w", encoding="utf-8") as f:
        f.write(code.replace(fragment, remplacement))
    return charger(t)



def main(argv):
    """Joue les épreuves puis les sabotages.

    ① RÔLE — Le verdict d'ensemble.
    ② CONTEXTE D'APPEL — Ligne de commande.
    ③ ENTRÉE — `argv` : [programme, racine].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0 si tout est vert et chaque sabotage rougit, 1 sinon.
      [rend: 1]
    ⑥ TRAITEMENT — voir le haut du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731, R-734.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche ; efface les dossiers temporaires créés par les épreuves.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(argv) < 2:
        print("usage : EPREUVES_DES_TYPES_DE_MARCHE <racine>"); return 1
    racine = os.path.abspath(argv[1])
    echecs = 0
    try:
        m = charger(os.path.join(racine, "programmes"))
    except Exception:
        traceback.print_exc(); return 1
    for e in EPREUVES:
        ok, err = jouer(m, racine, e)
        print(f"{'VERT ' if ok else 'ROUGE'} {e.__name__} {err}")
        echecs += not ok
    for nom, frag, rempl, e in SABOTAGES:
        try:
            ms = saboter(racine, frag, rempl)
            ok, err = jouer(ms, racine, e)
        except Exception as x:
            ok, err = None, f"SABOTAGE IMPOSSIBLE : {x}"
        bon = ok is False
        print(f"{'ROUGIT  ' if bon else 'NE ROUGIT PAS'} sabotage « {nom} » → {e.__name__} {err}")
        echecs += not bon
    for t in TEMPORAIRES:
        shutil.rmtree(t, ignore_errors=True)
    print(f"BILAN : {len(EPREUVES)} épreuves, {len(SABOTAGES)} sabotages, {echecs} échec(s)")
    return 0 if echecs == 0 else 1



if __name__ == "__main__":
    sys.exit(main(sys.argv))
