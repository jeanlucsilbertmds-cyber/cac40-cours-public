#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_SORTIE_AU_CALENDRIER_Ven_27-11-2026.py — Ven 27-11-2026 19h51 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Ce programme éprouve le lot L2 du plan R505 (« LA SORTIE », R-505 v2 étape 3) : l'horizon d'une
position se compte en SÉANCES DU CALENDRIER (R-112, défaut A-950), une échéance sans cours vend à l'ouverture de la
reprise (R-112 ②), une position « sans délai » encore ouverte à la fin des cours est mise À PART (A-1100), la liste
des durées à essayer contient « aucune » (A-645, A-1099), et la taxe de Peugeot s'arrête le 15-01-2021 (n°92). Il
repose sur des cours fabriqués à prix ronds ET sur de vraies lignes : le témoin du golden
(temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv, où TotalEnergies n'a pas de cours le 29-10-2024 alors que
la Bourse a coté), le fichier maître donnees/cours_maitre.csv, le journal des trades vécus
donnees/claude_journal_trades.csv et donnees/VALEURS_TTF.csv.

① RÔLE — Dire, propriété par propriété, si la sortie suit la loi ; avec --saboter, prouver que chaque épreuve
  ROUGIT quand on retire ce qu'elle teste.
② CONTEXTE D'APPEL — À la main ou par la certification : python3 -B tests/EPREUVES_DE_LA_SORTIE_AU_CALENDRIER_Ven_27-11-2026.py
  <racine> [--saboter]. Avec --saboter, il se relance lui-même sur des copies sabotées (« --racine-sabotee »).
③ ENTRÉE — <racine> : la racine d'une copie du dépôt (programmes/, donnees/, temoins/), jamais modifiée.
④ CONDITIONS D'ENTRÉE — Les fichiers cités au sens en tête existent dans la racine.
⑤ SORTIE — Un tableau « Ennn VERT/ROUGE motif » puis « VERDICT ». UNE valeur : le code — 0 tout vert (et, avec
  --saboter, chaque sabotage a fait rougir SON épreuve) · 1 au moins un rouge ou un sabotage resté vert · 2 la
  racine ne se lit pas (R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0).
⑥ TRAITEMENT — `epreuves` joue E1 à E9 ; `saboter` copie programmes/ et les fichiers lus dans un dossier
  temporaire, y change UN texte (présent une seule fois, sinon le sabotage est rouge), relance, exige le rouge nommé.
⑦ UNITÉ — Euros, séances du calendrier, dates AAAA-MM-JJ.
⑧ POURQUOI — R-731 (toute épreuve se sabote contre sa propre correction), R-732 (un cas au moins vient d'une vraie
  ligne), mandat L2 du 27-11-2026 (montrer que la C5 en service se comporte comme avant, sauf l'effet voulu).
⑨ CE QUI CLOCHE — La règle d'une échéance tombée sur un TROU DE DONNÉES (et non une suspension) est celle de la
  suspension (R-112 ②) : à confirmer par Jean-Luc ; E2 la fige. Le témoin indépendant du radar
  (`MODULE_C5_ETENDU_10._c5e10_sortie`, A-208 ⑤) compte encore en lignes : non éprouvé ici.
⑩ EFFET — Lit la racine ; avec --saboter, écrit puis efface des copies sous le dossier temporaire du système.
⑪ TERMINAISON — Sort par sys.exit ; chaque relance est bornée à 300 s.
  [sort: oui]
"""
import csv
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.abspath(__file__)
FICHIERS_LUS = ("donnees/BAREME_FRAIS.csv", "donnees/VALEURS_TTF.csv", "donnees/combinatoires/VOISINAGE.csv",
                "donnees/cours_maitre.csv", "donnees/claude_journal_trades.csv",
                "temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv")
JAN24 = ("2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08", "2024-01-09", "2024-01-10",
         "2024-01-11", "2024-01-12", "2024-01-15", "2024-01-16")
# LES DIX VALEURS DE LA C5 EN SERVICE (univers de C5E10-OBS-V1 au registre : TTE, ENGI, VIE, EN, FGR, AIR, RNO, URW,
# BVI, DG), sous la clé que rend le lecteur unique.
C5_VALEURS = ("TOTALENERGIES", "ENGIE", "VEOLIA", "BOUYGUES", "EIFFAGE", "AIRBUS", "RENAULT", "UNIBAIL_RODAMCO",
              "BUREAU_VERITAS", "VINCI")


def lire_le_maitre(racine):
    """Lit donnees/cours_maitre.csv par le lecteur unique du juge ; rend (cours, calendrier).
    ① RÔLE — le chemin réel du juge et du soir (R-111). ② CONTEXTE D'APPEL — E3, E4. ③ ENTRÉE — la racine.
    ④ CONDITIONS D'ENTRÉE — le référentiel des valeurs et les fichiers du lecteur. ⑤ SORTIE — DEUX valeurs : les
    séries par clé de valeur, le calendrier officiel des séances. [rend: 2] ⑥ TRAITEMENT —
    `JUGE_DES_STRATEGIES.lire_par_le_lecteur`, puis `MODULE_POSITIONS.calendrier_des_seances` avec la lecture.
    ⑦ UNITÉ — euros, dates. ⑧ POURQUOI — le maître écrit une même valeur sous deux graphies ; le lecteur les réunit.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main ou lève. [sort: non]"""
    J = charger(racine, "JUGE_DES_STRATEGIES")
    MP = charger(racine, "MODULE_POSITIONS")
    mnemo = J.table_mnemoniques(J.trouver(racine, "REFERENTIEL_VALEURS"))
    cours, lecture = J.lire_par_le_lecteur(racine, "donnees/cours_maitre.csv", mnemo)
    return cours, MP.calendrier_des_seances(cours, lecture)


def charger(racine, nom):
    """Charge programmes/<nom>.py de la racine, sous son propre nom.
    ① RÔLE — donner aux épreuves le code de la racine éprouvée, jamais un autre. ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — la racine, le nom du programme. ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : le
    module. [rend: 1] ⑥ TRAITEMENT — mettre programmes/ en tête du chemin d'import, puis importer par le nom (COMMUN
    et MODULE_POSITIONS doivent être LES mêmes objets que ceux que chargent les programmes : la sentinelle
    HORIZON_AUCUNE se reconnaît par `is`). ⑦ UNITÉ — —. ⑧ POURQUOI — une copie sabotée doit être celle qui tourne.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie sys.path. ⑪ TERMINAISON — rend la main ou lève ImportError. [sort: non]"""
    p = os.path.join(racine, "programmes")
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module(nom)


def lire_cours(chemin, valeurs):
    """Lit un fichier de cours (valeur, date, open, high, low, close, …) pour quelques valeurs.
    ① RÔLE — rendre les vraies séries. ② CONTEXTE D'APPEL — E1, E3, E4. ③ ENTRÉE — le chemin, les valeurs voulues.
    ④ CONDITIONS D'ENTRÉE — en-tête en première ligne. ⑤ SORTIE — UNE valeur : {valeur: séances triées, prix en
    nombres}. [rend: 1] ⑥ TRAITEMENT — DictReader, filtre, tri. ⑦ UNITÉ — euros. ⑧ POURQUOI — R-732. ⑨ CE QUI
    CLOCHE — ne passe pas par le lecteur unique (programmes/LIRE_LES_COURS.py) : aucune ligne n'est mise à part ici.
    ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main ; lève OSError. [sort: non]"""
    cours = {}
    with open(chemin, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if valeurs is None or r["valeur"] in valeurs:
                cours.setdefault(r["valeur"], []).append(
                    {"date": r["date"], "open": float(r["open"]), "high": float(r["high"]), "low": float(r["low"]),
                     "close": float(r["close"])})
    for v in cours:
        cours[v].sort(key=lambda b: b["date"])
    return cours


def serie_fabriquee(trous=(), barres=None):
    """Rend une série de janvier 2024 à prix ronds, moins les trous.
    ① RÔLE — cas connus écrits à la main. ② CONTEXTE D'APPEL — E1, E2, E5. ③ ENTRÉE — les dates sans cours, les
    séances particulières {date: (o, h, l, c)}. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la série. [rend: 1]
    ⑥ TRAITEMENT — séance calme (100,5 / 101 / 99,5 / 100,5) sauf `barres`. ⑦ UNITÉ — euros. ⑧ POURQUOI — prix ronds :
    l'attendu se calcule de tête (objectif 104,00, stop 97,50 pour un achat à 100,00). ⑨ CE QUI CLOCHE — —. ⑩ EFFET —
    aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    barres = barres or {}
    s = []
    for d in JAN24:
        if d in trous:
            continue
        o, h, l, c = barres.get(d, (100.5, 101.0, 99.5, 100.5))
        s.append({"date": d, "open": o, "high": h, "low": l, "close": c})
    return s


def epreuves(racine):
    """Joue E1 à E9 sur la racine ; rend la liste (code, vert, motif).
    ① RÔLE — les propriétés du lot L2. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE —
    celles du programme. ⑤ SORTIE — UNE valeur : la liste des résultats. [rend: 1] ⑥ TRAITEMENT — voir chaque bloc ;
    une exception dans un bloc le rend ROUGE avec son message (jamais vert). ⑦ UNITÉ — euros, séances. ⑧ POURQUOI —
    voir l'en-tête. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
    MP = charger(racine, "MODULE_POSITIONS")
    COMMUN = charger(racine, "COMMUN")
    res = []

    def bloc(code, fn):
        """Joue un bloc ; une exception le rend rouge. ① RÔLE — isoler chaque épreuve. ② CONTEXTE D'APPEL —
        `epreuves`. ③ ENTRÉE — le code, la fonction qui rend (vert, motif). ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE —
        aucune ; ajoute à `res`. [rend: 0] ⑥ TRAITEMENT — appeler, attraper. ⑦ UNITÉ — —. ⑧ POURQUOI — une épreuve qui
        lève n'est jamais verte (R-734). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit `res`. ⑪ TERMINAISON — rend la main.
        [sort: non]"""
        try:
            ok, motif = fn()
        except Exception as e:  # noqa: BLE001
            ok, motif = False, "lève %s: %s" % (type(e).__name__, str(e)[:200])
        res.append((code, ok, motif))

    def e1():
        """E1 — R-112 ① : une séance manquante fait avancer l'horizon (K07 fabriqué ; vraie ligne TotalEnergies).
        ① RÔLE — l'échéance au calendrier. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — le
        témoin du golden. ⑤ SORTIE — DEUX valeurs : vert, motif. [rend: 2] ⑥ TRAITEMENT — K07 : cours du 10-01-2024
        absent, achat le 09-01 à 100,00, horizon 3 → échéance le 12-01 (10, 11, 12), clôture 101,00 (le compte en
        lignes vendait le 15-01). Vraie ligne : TotalEnergies, achat à l'ouverture du 25-10-2024 (59,86), objectif
        62,2544, stop 58,3635, horizon 3 ; séances du calendrier 28, 29, 30-10 (le 29 manque pour TTE) → HORIZON le
        30-10 à la clôture 59,14 ; en lignes (28, 30, 31-10) le 31-10 ouvrait à 58,10 sous le stop : SL_GAP à 58,10.
        ⑦ UNITÉ — euros. ⑧ POURQUOI — A-950, K07 ; R-732. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend
        la main. [sort: non]"""
        s = serie_fabriquee(trous=("2024-01-10",), barres={"2024-01-09": (100.0, 101.0, 99.5, 100.5),
                                                            "2024-01-12": (100.5, 101.0, 99.5, 101.0),
                                                            "2024-01-15": (100.5, 102.5, 99.5, 102.0)})
        j = [b["date"] for b in s].index("2024-01-09")
        v = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 3}, "vendre", seances=list(JAN24))
        if (v["motif"], v["date_sortie"], v["px"]) != ("HORIZON", "2024-01-12", 101.0):
            return False, "K07 : %s %s %s, attendu HORIZON 2024-01-12 101.0" % (v["motif"], v["date_sortie"], v["px"])
        c = lire_cours(os.path.join(racine, FICHIERS_LUS[5]), ("TOTALENERGIES", "ENGIE"))
        cal = MP.calendrier_des_seances(c)
        if "2024-10-29" not in cal or "2024-10-29" in [b["date"] for b in c["TOTALENERGIES"]]:
            return False, "vraie ligne : le trou du 29-10-2024 de TotalEnergies n'est plus dans le témoin"
        tte = c["TOTALENERGIES"]
        j = [b["date"] for b in tte].index("2024-10-25")
        v = MP.vendre(tte, j, {"tp": 0.04, "sl": 0.025, "horizon": 3}, "vendre", seances=cal)
        if (v["motif"], v["date_sortie"], v["px"], v["objectif"], v["stop"]) != (
                "HORIZON", "2024-10-30", 59.14, 62.2544, 58.3635):
            return False, "TTE 25-10-2024 : %r" % (v,)
        return True, "K07 vendu le 12-01 à 101,00 ; TTE acheté le 25-10-2024 vendu HORIZON le 30-10 à 59,14"

    def e2():
        """E2 — R-112 ② : une échéance sans cours vend à l'OUVERTURE de la séance cotée suivante.
        ① RÔLE — la reprise. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX
        valeurs. [rend: 2] ⑥ TRAITEMENT — fabriqué (K07B) : achat le 09-01, horizon 3, échéance le 12-01 sans cours →
        vente le 15-01 à l'ouverture 100,50 ; vraie ligne : TotalEnergies acheté le 25-10-2024, horizon 2, échéance
        le 29-10 (pas de cours) → vente le 30-10 à l'ouverture 59,28 ; même vente quand le soir passe la DATE
        d'échéance (« echeance », fin des données « garder »). ⑦ UNITÉ — euros. ⑧ POURQUOI — R-112 ② ; le choix pour un
        trou de données est à confirmer (en-tête, ⑨). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la
        main. [sort: non]"""
        s = serie_fabriquee(trous=("2024-01-12",), barres={"2024-01-09": (100.0, 101.0, 99.5, 100.5),
                                                            "2024-01-15": (100.5, 102.5, 99.5, 102.0)})
        j = [b["date"] for b in s].index("2024-01-09")
        v = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 3}, "vendre", seances=list(JAN24))
        if (v["motif"], v["date_sortie"], v["px"]) != ("HORIZON", "2024-01-15", 100.5):
            return False, "K07B : %s %s %s, attendu HORIZON 2024-01-15 100.5" % (v["motif"], v["date_sortie"], v["px"])
        c = lire_cours(os.path.join(racine, FICHIERS_LUS[5]), ("TOTALENERGIES", "ENGIE"))
        cal = MP.calendrier_des_seances(c)
        tte = c["TOTALENERGIES"]
        j = [b["date"] for b in tte].index("2024-10-25")
        v = MP.vendre(tte, j, {"tp": 0.04, "sl": 0.025, "horizon": 2}, "vendre", seances=cal)
        w = MP.vendre(tte, j, {"objectif": 62.2544, "stop": 58.3635, "echeance": "2024-10-29"}, "garder")
        for x, qui in ((v, "juge"), (w, "soir")):
            if (x["motif"], x["date_sortie"], x["px"]) != ("HORIZON", "2024-10-30", 59.28):
                return False, "TTE 25-10-2024, horizon 2 (%s) : %r" % (qui, x)
        return True, "échéance sans cours : ouverture de la reprise (15-01 à 100,50 ; TTE 30-10-2024 à 59,28)"

    def e3():
        """E3 — LA C5 EN SERVICE NE CHANGE PAS sur le fichier maître : avec ou sans calendrier, même vente.
        ① RÔLE — montrer que seul l'effet voulu change (mandat L2, point 6). ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE —
        —. ④ CONDITIONS D'ENTRÉE — le maître. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — pour chaque séance
        des valeurs de C5 dans le maître prise comme achat (+4 % / −2,5 % / 20 séances, A-492), comparer la vente au
        calendrier (`calendrier_des_seances`) à la vente sans calendrier — l'ANCIEN compte en lignes, à l'identique
        du code d'avant le lot (mêmes séances testées, même échéance quand aucune séance ne manque) ; exiger au moins
        une vente HORIZON parmi elles (sinon l'épreuve ne dirait rien de l'horizon). ⑦ UNITÉ — séances. ⑧ POURQUOI —
        A-492, A-655 : la C5 en service garde sa vente à 20 séances. ⑨ CE QUI CLOCHE — le maître n'a aucun trou
        (mesuré le 27-11-2026 : 743 séances du calendrier, aucune manquante) : l'égalité y est attendue partout.
        ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
        c, cal = lire_le_maitre(racine)
        n, horizons, ecarts = 0, 0, []
        for v in C5_VALEURS:
            s = c.get(v, [])
            for j in range(len(s) - 1):
                a = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre", seances=cal)
                b = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre")
                n += 1
                horizons += bool(a and a["motif"] == "HORIZON")
                if a != b:
                    ecarts.append("%s %s" % (v, s[j]["date"]))
        if n < 1000 or not horizons:
            return False, "%d achats, %d ventes HORIZON : rien n'est éprouvé" % (n, horizons)
        if ecarts:
            return False, "%d écart(s) avec l'ancien compte, dont %s" % (len(ecarts), ", ".join(ecarts[:3]))
        return True, "%d achats possibles de la C5 sur le maître, dont %d vendus à 20 séances : vente inchangée" % (
            n, horizons)

    def e4():
        """E4 — LES TRADES VÉCUS DE C5 se rejouent à l'identique (journal des trades, vraies lignes).
        ① RÔLE — R-732 sur la C5 en service. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — le
        journal et le maître. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — pour chaque ligne du journal, le prix
        d'entrée et la date du journal, seuils +4 % / −2,5 %, horizon 20, calendrier du maître : motif, date et prix de
        sortie égaux à ceux du journal (à 1e-4 € près). ⑦ UNITÉ — euros. ⑧ POURQUOI — le soir a vendu ces trades avant
        le lot ; ils ne doivent pas bouger. ⑨ CE QUI CLOCHE — le soir vend avec les seuils écrits dans la position ;
        ici ils sont recalculés par `seuils_de_vente` (le même arrondi à cinq décimales, n°311). ⑩ EFFET — lit.
        ⑪ TERMINAISON — rend la main. [sort: non]"""
        c, cal = lire_le_maitre(racine)
        J = charger(racine, "JUGE_DES_STRATEGIES")
        vus, fautes = set(), []
        with open(os.path.join(racine, FICHIERS_LUS[4]), encoding="utf-8", newline="") as fh:
            for t in csv.DictReader(fh):
                cle = (t["valeur"], t["date_entree"])
                if cle in vus:
                    continue
                vus.add(cle)
                s = c[J.cle_valeur(t["valeur"])]
                j = [b["date"] for b in s].index(t["date_entree"])
                v = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre", seances=cal)
                if (v["motif"], v["date_sortie"]) != (t["motif_sortie"], t["date_sortie"]) or \
                        abs(v["px"] - float(t["prix_sortie"])) > 1e-4:
                    fautes.append("%s %s : %s %s %s, journal %s %s %s" % (
                        t["valeur"], t["date_entree"], v["motif"], v["date_sortie"], v["px"], t["motif_sortie"],
                        t["date_sortie"], t["prix_sortie"]))
        if len(vus) < 5:
            return False, "%d trade(s) seulement au journal" % len(vus)
        return (not fautes), ("%d trades vécus rejoués à l'identique" % len(vus)) if not fautes else "; ".join(fautes)

    def e5():
        """E5 — A-1100 : une position SANS DÉLAI encore ouverte à la fin des cours est NON TERMINÉE, comptée à part.
        ① RÔLE — la marque et la mise à part. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — achat le 09-01 sans seuil touché, horizon « aucune » :
        `vendre` (« vendre ») rend le motif COMMUN.MOTIF_FIN_DES_DONNEES, jamais HORIZON, au dernier cours ; en
        « garder », rien ; `JUGE_DES_STRATEGIES.resumer` l'exclut du compte et la rend dans « fin_des_donnees » ; une
        durée chiffrée au même endroit garde HORIZON. ⑦ UNITÉ — euros. ⑧ POURQUOI — décision de Jean-Luc du
        12-11-2026 à 09h18 et A-1100 (27-11-2026, 19h29). ⑨ CE QUI CLOCHE — le mot écrit est « FIN_DES_DONNEES », pas
        « NON TERMINÉE » (COMMUN, hors du lot). ⑩ EFFET — charge le juge. ⑪ TERMINAISON — rend la main. [sort: non]"""
        s = serie_fabriquee(barres={"2024-01-09": (100.0, 101.0, 99.5, 100.5)})
        j = [b["date"] for b in s].index("2024-01-09")
        a = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": COMMUN.HORIZON_AUCUNE}, "vendre", seances=list(JAN24))
        g = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": COMMUN.HORIZON_AUCUNE}, "garder", seances=list(JAN24))
        h = MP.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 30}, "vendre", seances=list(JAN24))
        if a["motif"] != COMMUN.MOTIF_FIN_DES_DONNEES or a["motif"] == "HORIZON" or g is not None or \
                h["motif"] != "HORIZON":
            return False, "aucune : %r ; garder : %r ; 30 séances : %r" % (a and a["motif"], g, h and h["motif"])
        J = charger(racine, "JUGE_DES_STRATEGIES")
        ops = [{"motif": a["motif"], "net": 500.0}, {"motif": "TP", "net": 3694.0}]
        r = J.resumer(ops)
        if r.get("n") != 1 or r.get("fin_des_donnees") != {"n": 1, "net": 500.0} or r.get("net") != 3694.0:
            return False, "resumer : %r" % (r,)
        return True, "sans délai, ouverte à la fin : FIN_DES_DONNEES, hors du total, comptée à part"

    def e6():
        """E6 — n°92 : Peugeot (UG) taxée du 04-01 au 15-01-2021 seulement ; Stellantis (STLAP) non taxée en 2021.
        ① RÔLE — la date de fin propre à une valeur. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE
        — donnees/VALEURS_TTF.csv avec la colonne `taxee_jusqu_au`. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT —
        `valeur_taxee` sur six cas réels, puis la taxe d'un achat de 100 000 € (0,3 % en 2021 : 300,00 €, puis 0,00 €
        le 18-01-2021) ; refus d'une fin posée sur une ligne NON. ⑦ UNITÉ — euros. ⑧ POURQUOI — décision n°92 du
        01-11-2026, rapportée par A-1100. ⑨ CE QUI CLOCHE — la dernière séance de Peugeot (15-01-2021) n'est pas lue
        dans les cours : la date vient de la décision. ⑩ EFFET — lit ; remplit puis vide le cache du module.
        ⑪ TERMINAISON — rend la main. [sort: non]"""
        attendus = {("UG", "2021-01-04"): True, ("UG", "2021-01-15"): True, ("UG", "2021-01-18"): False,
                    ("STLAP", "2021-01-18"): False, ("UG", "2020-06-01"): True, ("UG", "2022-01-10"): False}
        vus = {k: MP.valeur_taxee(*k) for k in attendus}
        if vus != attendus:
            return False, "valeur_taxee : %r" % ({k: v for k, v in vus.items() if attendus[k] != v},)
        t1 = round(MP.cout_d_un_ordre("UG", "2021-01-15", "achat", 100000.0)["taxe"], 2)
        t2 = round(MP.cout_d_un_ordre("UG", "2021-01-18", "achat", 100000.0)["taxe"], 2)
        if (t1, t2) != (300.0, 0.0):
            return False, "taxe UG : %s le 15-01, %s le 18-01 (300,00 puis 0,00 attendus)" % (t1, t2)
        cle = ("tableau", "VALEURS_TTF.csv")
        garde = MP._CACHE[cle]
        try:
            MP._CACHE[cle] = [dict(l, taxee_jusqu_au="2021-06-30") if (l["annee"], l["mnemonique"]) == ("2021", "STLAP")
                              else l for l in garde]
            try:
                MP.valeur_taxee("STLAP", "2021-03-01")
                return False, "une fin sur une ligne NON est acceptée"
            except ValueError:
                pass
        finally:
            MP._CACHE[cle] = garde
        return True, "UG taxée jusqu'au 15-01-2021 (300,00 €), plus le 18-01 ; STLAP non taxée ; fin sur NON refusée"

    def e7():
        """E7 — A-645, A-1099 : la liste des durées à essayer contient « aucune ».
        ① RÔLE — la version « sans délai » est déclarée. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS
        D'ENTRÉE — donnees/combinatoires/VOISINAGE.csv. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — lire la
        ligne horizon ; `PREPARER.valeurs_de_la_liste("horizon", liste, 20)` doit rendre 5, 10, 15, 20, 25, aucune
        (les cinq durées d'avant le lot, plus « aucune »). ⑦ UNITÉ — séances. ⑧ POURQUOI — décision de Jean-Luc du
        27-11-2026 à 19h27 (A-1099). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
        with open(os.path.join(racine, FICHIERS_LUS[2]), encoding="utf-8-sig", newline="") as fh:
            ligne = [r for r in csv.DictReader(fh) if r["parametre"] == "horizon"]
        if len(ligne) != 1:
            return False, "%d ligne(s) horizon" % len(ligne)
        P = charger(racine, "PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES")
        vals = P.valeurs_de_la_liste("horizon", ligne[0]["liste"] or "", 20)
        if vals != ["5", "10", "15", "20", "25", COMMUN.MOT_DE_L_HORIZON_AUCUNE]:
            return False, "durées à essayer : %r" % (vals,)
        return True, "durées à essayer : %s" % " · ".join(vals)

    def e8():
        """E8 — LE SOIR compte l'échéance au calendrier (`TENIR_LES_POSITIONS.echeance`), comme le juge.
        ① RÔLE — R-708 entre le juge et le soir. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE —
        —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — K07 : avec le calendrier, échéance le 12-01 ; sans,
        l'ancien compte en lignes (15-01) ; `seance_d_echeance` rend None quand le calendrier ne porte pas encore h
        séances (une échéance pas encore publiée ne se devine pas, défaut 2 de A-491). ⑦ UNITÉ — séances. ⑧ POURQUOI —
        A-950. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — charge le soir. ⑪ TERMINAISON — rend la main. [sort: non]"""
        T = charger(racine, "TENIR_LES_POSITIONS")
        s = serie_fabriquee(trous=("2024-01-10",))
        a, b = T.echeance(s, "2024-01-09", 3, list(JAN24)), T.echeance(s, "2024-01-09", 3)
        n = MP.seance_d_echeance(list(JAN24), "2024-01-12", 3)
        if (a, b, n) != ("2024-01-12", "2024-01-15", None):
            return False, "échéance au calendrier %s, sans calendrier %s, calendrier trop court %r" % (a, b, n)
        return True, "soir : échéance le 12-01 au calendrier (15-01 en lignes) ; inconnue si le calendrier s'arrête"

    def e9():
        """E9 — LE JUGE PASSE LE CALENDRIER : `jouer_une_entree` vend au calendrier de la lecture ou reçu.
        ① RÔLE — le chemin réel du juge et de la moulinette. ② CONTEXTE D'APPEL — `bloc`. ③ ENTRÉE — —. ④ CONDITIONS
        D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — K07 joué par `jouer_une_entree` : avec
        `seances` → 12-01 ; avec une lecture qui porte « seances » → 12-01 ; `calendrier_pour_la_vente` sans lecture
        rend la réunion des dates des cours. ⑦ UNITÉ — euros. ⑧ POURQUOI — A-950 : la vente du juge comptait en lignes.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — charge le juge. ⑪ TERMINAISON — rend la main. [sort: non]"""
        J = charger(racine, "JUGE_DES_STRATEGIES")
        s = serie_fabriquee(trous=("2024-01-10",), barres={"2024-01-09": (100.0, 101.0, 99.5, 100.5),
                                                            "2024-01-12": (100.5, 101.0, 99.5, 101.0)})
        j = [b["date"] for b in s].index("2024-01-09")
        a = J.jouer_une_entree("FABC", s, j, 0.04, 0.025, 3, MP, None, "HIST_COURTAGE_SANS_TTF", seances=list(JAN24))
        lec = {"composition": False, "seances": list(JAN24), "passages": {}, "trous": {}}
        b = J.jouer_une_entree("FABC", s, j, 0.04, 0.025, 3, MP, lec, "HIST_COURTAGE_SANS_TTF")
        cal = J.calendrier_pour_la_vente({"A": s, "B": [{"date": "2024-01-10"}]}, None, MP)
        if (a["date_sortie"], b["date_sortie"]) != ("2024-01-12", "2024-01-12") or "2024-01-10" not in cal:
            return False, "juge : %s, %s ; calendrier %r" % (a["date_sortie"], b["date_sortie"], cal[:6])
        return True, "le juge vend K07 le 12-01, calendrier reçu ou lu"

    for code, fn in (("E1", e1), ("E2", e2), ("E3", e3), ("E4", e4), ("E5", e5), ("E6", e6), ("E7", e7),
                     ("E8", e8), ("E9", e9)):
        bloc(code, fn)
    return res


# LES SABOTAGES — (nom, épreuve qui DOIT rougir, fichier, texte avant, texte après). Le texte avant doit être présent
# UNE fois exactement ; sinon le sabotage n'est pas joué et compte ROUGE.
SABOTAGES = (
    ("S1 l'échéance comptée en lignes", "E1", "programmes/MODULE_POSITIONS.py",
     "            echeance = seance_d_echeance(seances, serie[j][\"date\"], h)\n",
     "            echeance = serie[j + h][\"date\"] if j + h < len(serie) else None\n"),
    ("S2 la reprise retirée (l'échéance sans cours n'est plus vue)", "E2", "programmes/MODULE_POSITIONS.py",
     "        if echeance is not None and b[\"date\"] > echeance:\n", "        if False:\n"),
    ("S3 la reprise à la clôture au lieu de l'ouverture", "E2", "programmes/MODULE_POSITIONS.py",
     "            return {\"pe\": pe, \"px\": b[\"open\"], \"motif\": \"HORIZON\", \"date_sortie\": b[\"date\"],",
     "            return {\"pe\": pe, \"px\": b[\"close\"], \"motif\": \"HORIZON\", \"date_sortie\": b[\"date\"],"),
    ("S4 l'échéance un cran trop tôt", "E3", "programmes/MODULE_POSITIONS.py",
     "    k = bisect.bisect_right(seances, date_achat) + h - 1\n",
     "    k = bisect.bisect_right(seances, date_achat) + h - 2\n"),
    ("S5 le stop sans saut n'est plus vu", "E4", "programmes/MODULE_POSITIONS.py",
     "    if bar[\"low\"] <= sl:\n", "    if bar[\"low\"] < sl - 1.0:\n"),
    ("S6 sans délai vendu HORIZON au dernier cours", "E5", "programmes/MODULE_POSITIONS.py",
     "    motif = _motif_fin_des_donnees() if aucune else \"HORIZON\"\n", "    motif = \"HORIZON\"\n"),
    ("S7 la fin propre de la taxe ignorée", "E6", "programmes/MODULE_POSITIONS.py",
     "    if jusqu_au:\n        _date_du_calendrier(", "    if False:\n        _date_du_calendrier("),
    ("S8 la fin posée sur une ligne NON acceptée", "E6", "programmes/MODULE_POSITIONS.py",
     "        if drapeau != \"OUI\" or jusqu_au[:4] != annee:\n", "        if jusqu_au[:4] != annee:\n"),
    ("S9 la colonne retirée du contrat", "E6", "programmes/CONTRATS_DES_FICHIERS.py",
     "    \"releve_le\", \"taxee_jusqu_au\",\n", "    \"releve_le\",\n"),
    ("S10 « aucune » retirée de la liste des durées", "E7", "donnees/combinatoires/VOISINAGE.csv",
     ";25;aucune\r\n", ";25\r\n"),
    ("S11 le soir compte encore en lignes", "E8", "programmes/TENIR_LES_POSITIONS.py",
     "    return _moteur().seance_d_echeance(seances if seances is not None else dates, date_entree, h)\n",
     "    return _moteur().seance_d_echeance(dates, date_entree, h)\n"),
    ("S12 le juge ne passe pas le calendrier", "E9", "programmes/JUGE_DES_STRATEGIES.py",
     "    _cal = seances if seances is not None else (lecture or {}).get(\"seances\")\n", "    _cal = None\n"),
)


def saboter(racine):
    """Joue chaque sabotage sur une copie et exige le rouge de SON épreuve ; rend la liste (nom, mord, motif).
    ① RÔLE — R-731 : une épreuve verte quand on retire ce qu'elle teste est une décoration. ② CONTEXTE D'APPEL —
    `main`, avec --saboter. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — celles du programme. ⑤ SORTIE — UNE valeur :
    la liste. [rend: 1] ⑥ TRAITEMENT — pour chaque sabotage : copier la racine (sans .git) dans un dossier
    temporaire, remplacer le texte (présent une fois), relancer ce programme avec --racine-sabotee, lire la ligne de
    l'épreuve visée. ⑦ UNITÉ — —. ⑧ POURQUOI — voir ①. ⑨ CE QUI CLOCHE — seule l'épreuve visée est exigée rouge ;
    les autres peuvent rougir aussi. ⑩ EFFET — écrit puis efface des dossiers temporaires. ⑪ TERMINAISON — chaque
    relance est bornée à 300 s. [sort: non]"""
    out = []
    for nom, cible, fichier, avant, apres in SABOTAGES:
        tmp = tempfile.mkdtemp(prefix="sortie_cal_sab_")
        try:
            tmp = os.path.join(tmp, "racine")
            shutil.copytree(racine, tmp, symlinks=True, ignore=shutil.ignore_patterns("__pycache__", ".git"))
            p = os.path.join(tmp, fichier)
            t = open(p, "rb").read().decode("utf-8")
            if t.count(avant) != 1:
                out.append((nom, False, "NON JOUÉ — texte à saboter présent %d fois" % t.count(avant)))
                continue
            open(p, "wb").write(t.replace(avant, apres).encode("utf-8"))
            r = subprocess.run([sys.executable, "-B", ICI, tmp, "--racine-sabotee"], capture_output=True, text=True,
                               timeout=300)
            ligne = [l for l in r.stdout.splitlines() if l.startswith(cible + " ")]
            mord = bool(ligne) and " ROUGE " in ligne[0]
            out.append((nom, mord, ligne[0] if ligne else "épreuve %s absente de la sortie (code %d)" % (
                cible, r.returncode)))
        finally:
            shutil.rmtree(os.path.dirname(tmp) if tmp.endswith("racine") else tmp, ignore_errors=True)
    return out


def main(argv):
    """Lance les épreuves, et les sabotages si demandé ; rend le code de sortie.
    ① RÔLE — le point d'entrée. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — argv. ④ CONDITIONS D'ENTRÉE —
    une racine. ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir l'en-tête). [rend: 1] ⑥ TRAITEMENT — vérifier la racine ;
    jouer ; afficher ; saboter. ⑦ UNITÉ — —. ⑧ POURQUOI — R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    racine = os.path.abspath(args[0])
    manque = [f for f in ("programmes/MODULE_POSITIONS.py",) + FICHIERS_LUS if not os.path.isfile(
        os.path.join(racine, f))]
    if manque:
        print("ARRÊT : la racine ne porte pas %s — rien n'est éprouvé" % ", ".join(manque))
        return 2
    res = epreuves(racine)
    print("ÉPREUVES DE LA SORTIE AU CALENDRIER (lot L2, A-950 · A-645 · A-1100 · n°92) — racine %s" % racine)
    for code, ok, motif in res:
        print("%s %s %s" % (code, "VERT " if ok else "ROUGE", motif))
    bon = all(ok for _c, ok, _m in res)
    if "--saboter" in argv and "--racine-sabotee" not in argv:
        print("— SABOTAGES —")
        for nom, mord, motif in saboter(racine):
            print("  %s %s — %s" % ("MORD " if mord else "RESTE VERT/NON JOUÉ", nom, motif))
            bon = bon and mord
    print("VERDICT : %s" % ("TOUT TIENT" if bon else "NON CONFORME"))
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
