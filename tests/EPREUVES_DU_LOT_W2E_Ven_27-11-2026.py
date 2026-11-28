#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_LOT_W2E — Ven 27-11-2026 (Paris). SIMULATION UNIQUEMENT : aucun ordre réel.

① RÔLE — Éprouver les quatre pièces du lot W2e du plan R505 (loi R-505 v2) : le GLISSEMENT MESURÉ (A-1068), l'ÉPREUVE
  ANTI-AVENIR SUR LES 20 ANS (A-674, A-692), la CASE RAISON OBLIGATOIRE (A-1090) et le réglage « QUAND JOUER » (A-1079),
  et montrer que chaque épreuve a des dents (sabotages). LOT W2e-FIX (27-11-2026, A-1105) : l'estimateur EDGE
  calibré sur les chiffres publiés des auteurs (E1), l'achat à l'enchère sans fourchette (G4), la sensibilité (E3),
  la raison « inconnue » acceptée (R1), « quand jouer » dans l'empreinte et la moulinette (Q5, M1), le découpage du
  jour même par défaut, ses calculs importés (Q4, Q6, Q7).
② CONTEXTE D'APPEL — À la main ou par le circuit des épreuves, après toute modification de programmes/MODULE_GLISSEMENT.py,
  programmes/MODULE_QUAND_JOUER.py, de `jouer`, `jouer_une_entree` ou `resumer` (JUGE_DES_STRATEGIES) ou du contrat de la
  déclaration (CONTRATS_DES_FICHIERS).
③ ENTRÉE — argv[1] : la racine d'un dépôt (une COPIE : rien n'y est écrit, mais la règle du projet est de ne jamais éprouver
  sur le dépôt) · facultatif : `--saboter` (Z0 puis chaque sabotage) · `--cas=A,B` (ces cas seuls, sans sabotage).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/, donnees/sources_indice/INDICE_CAC40.csv, donnees/REFERENTIEL_VALEURS*,
  et le témoin des 20 ans (temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv, nommé par
  PREPARER_LA_MOULINETTE_D_ESSAI.COURS_DES_VINGT_ANS, lu par cette constante : R-708).
⑤ SORTIE — UN code de sortie : 0 si tous les cas sont verts (et, avec --saboter, si chaque sabotage fait rougir au moins un
  de ses cas) ; 1 sinon ; 2 si un cas n'a pas pu tourner (exception) ou un argument est inconnu (R-734). [rend: 1]
⑥ TRAITEMENT — ① lire une fois les 20 ans par le lecteur du juge et l'indice · ② jouer chaque cas · ③ avec --saboter :
  pour chaque sabotage, une copie temporaire dont programmes/ est copié (le reste en liens), une phrase du code remplacée
  (la phrase doit exister une fois, sinon code 2), puis les cas visés relancés dans un processus neuf, qui doit rendre 1.
⑦ UNITÉ — Euros, fractions du prix, séances, dates AAAA-MM-JJ.
⑧ POURQUOI — R-731 : épreuves avec sabotages, cas réels (R-732), un contrôle qui ne tourne pas ne rend pas 0 (R-734).
  L'ÉPREUVE ANTI-AVENIR : la fiche d'essai ESSAI-C5-2000-2026 (A-853 ; une stratégie fictive est REFUSÉE sur 2000-2023
  par la garde du regard unique, mesuré le 27-11-2026, et seule cette fiche reçoit le jeton d'essai, A-863), jouée sur
  les 20 ans, coupée à des dates réparties, sans qu'aucun gain soit affiché : aucune décision prise avant la coupure ne
  change quand on cache ce qui la suit (A-674 : « calculer […] avec tous les cours, puis en lui CACHANT tout ce qui suit
  ce jour ; si la décision change, le programme utilise l'avenir »).
⑨ CE QUI CLOCHE — ① L'épreuve anti-avenir de la chaîne (A3) joue SANS la lecture du lecteur (`lecture=None` : ni
  composition de l'indice, ni trous) et sur les 6 valeurs de la fiche d'essai, 8 dates : la voie « avec lecture » n'est pas éprouvée ici. ② Le
  signal du programme de signal lui-même relève de tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py, pas d'ici.
  ③ Les sabotages remplacent du texte : renommer une phrase du code rend le sabotage introuvable (code 2), jamais vert.
⑩ EFFET — Lit des fichiers ; avec --saboter, écrit puis efface des copies temporaires sous le dossier temporaire.
⑪ TERMINAISON — Rend la main ; chaque sabotage a un délai de 900 s (dépassé : compté comme non mordu, code 1).
  [sort: oui]
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile

RACINE = None
_CACHE = {}
CAS = {}


def cas(nom):
    """Inscrit un cas. ① RÔLE — Ranger une épreuve sous son nom. ② CONTEXTE D'APPEL — à la définition de chaque cas.
    ③ ENTRÉE — `nom`. ④ CONDITIONS D'ENTRÉE — nom unique. ⑤ SORTIE — UNE valeur, le décorateur. [rend: 1]
    ⑥ TRAITEMENT — ranger. ⑦ UNITÉ — —. ⑧ POURQUOI — un sabotage vise des cas par leur nom. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — remplit CAS. ⑪ TERMINAISON — rend la main. [sort: non]"""
    def deco(f):
        CAS[nom] = f
        return f
    return deco


def modules():
    """Importe les modules de la racine. ① RÔLE — Charger les programmes éprouvés depuis RACINE/programmes.
    ② CONTEXTE D'APPEL — chaque cas. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — RACINE posée. ⑤ SORTIE — UNE valeur, un
    dictionnaire de modules. [rend: 1] ⑥ TRAITEMENT — sys.path, import. ⑦ UNITÉ — —. ⑧ POURQUOI — éprouver la copie,
    jamais le dossier de ce fichier. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie sys.path. ⑪ TERMINAISON — rend la main ou
    lève ImportError. [sort: non]"""
    p = os.path.join(RACINE, "programmes")
    if p not in sys.path:
        sys.path.insert(0, p)
    import MODULE_GLISSEMENT as G, MODULE_QUAND_JOUER as Q, JUGE_DES_STRATEGIES as J, MODULE_POSITIONS as P
    import CONTRATS_DES_FICHIERS as C, DECLARER_UNE_STRATEGIE as D, METEO_DU_MARCHE as M
    import PREPARER_LA_MOULINETTE_D_ESSAI as PM
    import DATER_LES_TYPES_DE_MARCHE as L5
    import PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES as PV, DECLINER_LES_STRATEGIES as DL
    import JOUER_LES_VERSIONS as JV
    return {"G": G, "Q": Q, "J": J, "P": P, "C": C, "D": D, "M": M, "PM": PM, "L5": L5, "PV": PV, "DL": DL, "JV": JV}


def vingt_ans():
    """Lit les 20 ans une fois. ① RÔLE — Rendre (cours, lecture, mnemo) du témoin des 20 ans. ② CONTEXTE D'APPEL — les
    cas réels. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — le témoin existe. ⑤ SORTIE — UNE valeur, un triplet. [rend: 1]
    ⑥ TRAITEMENT — `lire_par_le_lecteur`, le lecteur du juge. ⑦ UNITÉ — euros. ⑧ POURQUOI — lu comme la moulinette le
    lit (R-708). ⑨ CE QUI CLOCHE — 17 à 26 s. ⑩ EFFET — lit un fichier. ⑪ TERMINAISON — rend la main. [sort: non]"""
    if "20" not in _CACHE:
        m = modules()
        J = m["J"]
        mnemo = J.table_mnemoniques(J.trouver(RACINE, "REFERENTIEL_VALEURS"))
        cours, lecture = J.lire_par_le_lecteur(RACINE, m["PM"].COURS_DES_VINGT_ANS, mnemo)
        _CACHE["20"] = (cours, lecture, mnemo)
    return _CACHE["20"]


def indice():
    """Lit l'indice. ① RÔLE — {date : clôture} du CAC 40 par `METEO_DU_MARCHE.lire_serie` (R-708). ② CONTEXTE D'APPEL —
    cas Q et A. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur. [rend: 1]
    ⑥ TRAITEMENT — lecture, colonne yahoo. ⑦ UNITÉ — points. ⑧ POURQUOI — la météo lit cette colonne.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
    if "ind" not in _CACHE:
        M = modules()["M"]
        _CACHE["ind"] = M.lire_serie(M.chemins(RACINE)["historique"], "yahoo")
    return _CACHE["ind"]


def oracle_cs(h1, l1, c1, h2, l2):
    """L'oracle : la formule de Corwin et Schultz (2012) recopiée DE L'ARTICLE ici, à la main, pour juger le module.
    ① RÔLE — Donner la valeur attendue. ② CONTEXTE D'APPEL — G1, G2. ③ ENTRÉE — prix de deux séances. ④ CONDITIONS
    D'ENTRÉE — prix > 0. ⑤ SORTIE — UNE valeur, S en fraction. [rend: 1] ⑥ TRAITEMENT — ajustement de la nuit, β, γ, α,
    S, négatif → 0. ⑦ UNITÉ — fraction. ⑧ POURQUOI — une épreuve juge contre une référence écrite à part.
    ⑨ CE QUI CLOCHE — c'est une seconde écriture de la formule, voulue : elle ne vit que dans l'épreuve.
    ⑩ EFFET — —. ⑪ TERMINAISON — rend la main. [sort: non]"""
    if l2 > c1:
        d = l2 - c1
        h2, l2 = h2 - d, l2 - d
    elif h2 < c1:
        d = c1 - h2
        h2, l2 = h2 + d, l2 + d
    b = math.log(h1 / l1) ** 2 + math.log(h2 / l2) ** 2
    g = math.log(max(h1, h2) / min(l1, l2)) ** 2
    k = 3 - 2 * math.sqrt(2)
    a = (math.sqrt(2 * b) - math.sqrt(b)) / k - math.sqrt(g / k)
    return max(0.0, 2 * (math.exp(a) - 1) / (1 + math.exp(a)))


def seance(d, o, h, l, c):
    """Une séance construite. ① RÔLE — fabriquer un dictionnaire de séance. ② CONTEXTE D'APPEL — cas construits.
    ③ ENTRÉE — date et prix. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT — —. ⑦ UNITÉ —
    euros. ⑧ POURQUOI — lisibilité. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — —. ⑪ TERMINAISON — rend la main. [sort: non]"""
    return {"date": d, "open": o, "high": h, "low": l, "close": c, "volume": 1}


# ───────────────────────── PIÈCE 1 — LE GLISSEMENT MESURÉ (A-1068) ─────────────────────────

@cas("G1")
def g1():
    """G1 — la formule sur trois paires construites : ordinaire, montée de nuit, écart négatif ramené à 0.
    ①-⑪ : voir l'en-tête ; rend (vrai/faux, détail). [rend: 1] [sort: non]"""
    G = modules()["G"]
    paires = [((101, 99, 100), (101.5, 99.5)),        # ordinaire
              ((101, 99, 100), (104.0, 102.0)),       # le plus bas du jour au-dessus de la clôture de la veille
              ((102, 98, 100), (99.0, 97.0)),         # le plus haut du jour sous la clôture : sans l'ajustement, 0
              ((101, 100, 101), (102.0, 101.0))]      # deux séances en escalier : α < 0 (S brut −1,40 %), ramené à 0
    det = []
    ok = True
    for (h1, l1, c1), (h2, l2) in paires:
        v = G.ecart_de_deux_seances({"high": h1, "low": l1, "close": c1}, {"high": h2, "low": l2, "close": 0})
        e = oracle_cs(h1, l1, c1, h2, l2)
        det.append("%.6f/%.6f" % (v, e))
        ok = ok and abs(v - e) < 1e-12
    ok = ok and det[3].startswith("0.000000") and float(det[0].split("/")[0]) > 0 and float(det[2].split("/")[0]) > 0
    # un prix manquant : None, jamais un chiffre
    ok = ok and G.ecart_de_deux_seances({"high": 1, "low": 1}, {"high": 1, "low": 1, "close": 1}) is None
    return ok, "obtenu/attendu : " + " · ".join(det)


@cas("G2")
def g2():
    """G2 — CAS RÉEL (R-732) : la première paire de séances d'une vraie valeur du témoin des 20 ans, contre l'oracle.
    [rend: 1] [sort: non]"""
    G = modules()["G"]
    cours, _, _ = vingt_ans()
    v = sorted(cours)[0]
    s = cours[v]
    a, b = s[0], s[1]
    x = G.ecart_de_deux_seances(a, b)
    e = oracle_cs(a["high"], a["low"], a["close"], b["high"], b["low"])
    return x is not None and abs(x - e) < 1e-12, "%s %s→%s : %.6f, oracle %.6f" % (v, a["date"], b["date"], x or -1, e)


@cas("G3")
def g3():
    """G3 — `ecart_estime_avant` ne lit RIEN de la séance de l'ordre ni d'après : séances ≥ j faussées, même chiffre.
    [rend: 1] [sort: non]"""
    G = modules()["G"]
    cours, _, _ = vingt_ans()
    v = sorted(cours)[1]
    s = cours[v]
    ecarts = {e: 0 for e in G.ESTIMATEURS}
    for j in range(30, len(s), max(1, len(s) // 400)):
        faux = s[:j] + [dict(b, open=b["open"] * 1.2, high=b["high"] * 1.5, low=b["low"] * 0.5) for b in s[j:]]
        for e in G.ESTIMATEURS:
            if G.ecart_estime_avant(s, j, estimateur=e) != G.ecart_estime_avant(faux, j, estimateur=e):
                ecarts[e] += 1
    return not any(ecarts.values()), "%s : rangs où l'avenir faussé change l'estimation %s" % (v, ecarts)


@cas("G4")
def g4():
    """G4 — QUI PAIE (R-601, lot W2e-FIX) : par défaut (« enchere_gratuite ») l'achat ne paie rien ; une vente à
    l'objectif ou au stop EN SÉANCE paie quantité × prix × demi-écart ; un saut d'ouverture (SL_GAP, TP_GAP) et une
    échéance (HORIZON) ne paient rien ; « les_deux » fait payer achat et vente ; un réglage inconnu lève ; les deux
    estimateurs passent par la même formule. [rend: 1] [sort: non]"""
    m = modules()
    G, P = m["G"], m["P"]
    s = [seance("2025-01-%02d" % (k + 1), 100 + (k % 4) * 0.3, 101 + k % 3, 99 - k % 2, 100 + (k % 5) * 0.2)
         for k in range(30)]
    base = {"pe": 100.0, "px": 104.0, "date_sortie": s[28]["date"]}
    q = P.CAPITAL / 100.0
    det, ok = [], True
    for est in G.ESTIMATEURS:
        da, dv = G.ecart_estime_avant(s, 25, estimateur=est) / 2, G.ecart_estime_avant(s, 28, estimateur=est) / 2
        c = {mo: G.cout_du_glissement(s, 25, dict(base, motif=mo), estimateur=est)["glissement_eur"]
             for mo in ("TP", "SL", "SL_GAP", "TP_GAP", "HORIZON")}
        deux = G.cout_du_glissement(s, 25, dict(base, motif="HORIZON"), "les_deux", estimateur=est)["glissement_eur"]
        ok = ok and da > 0 and dv > 0 and abs(c["TP"] - q * 104.0 * dv) < 1e-9 and abs(c["SL"] - q * 104.0 * dv) < 1e-9
        ok = ok and c["SL_GAP"] == 0.0 and c["TP_GAP"] == 0.0 and c["HORIZON"] == 0.0
        ok = ok and abs(deux - (P.CAPITAL * da + q * 104.0 * dv)) < 1e-9
        det.append("%s : TP %.2f · SL_GAP %.2f · HORIZON %.2f · les_deux %.2f €" % (est, c["TP"], c["SL_GAP"],
                                                                                 c["HORIZON"], deux))
    try:
        G.cout_du_glissement(s, 25, dict(base, motif="TP"), "au_hasard")
        leve = False
    except ValueError:
        leve = True
    ok = ok and leve and G.ORDRES_QUI_PAIENT_PAR_DEFAUT == "enchere_gratuite"
    return ok, " | ".join(det) + " · inconnu lève : %s" % leve


@cas("G5")
def g5():
    """G5 — BRANCHEMENT, sur de VRAIES séances : `jouer_une_entree` rend `net` comme avant (prix et frais) et
    `net_glissement_paye` = `net` − le coût de `cout_du_glissement`, calculé à ce seul endroit. [rend: 1] [sort: non]"""
    m = modules()
    J, P, G = m["J"], m["P"], m["G"]
    cours, _, _ = vingt_ans()
    _f, jeton = fiche_d_essai()
    if isinstance(jeton, str):
        raise RuntimeError("jeton d'essai refusé : %s" % jeton)
    v = sorted(cours, key=lambda k: -len(cours[k]))[0]
    s = cours[v]
    vues, faux, payes = 0, [], 0
    for j in range(300, len(s) - 30, 499):
        op = J.jouer_une_entree(v, s, j, 0.04, 0.025, 10, P, recu=jeton)
        if op is None:
            continue
        vues += 1
        q = P.CAPITAL / op["pe"]
        g = G.cout_du_glissement(s, j, op)["glissement_eur"]
        if not (abs(op["net"] - (q * (op["px"] - op["pe"]) - op["frais"])) < 1e-6
                and abs(op["glissement"] - g) < 1e-9 and abs(op["net_glissement_paye"] - (op["net"] - g)) < 1e-9
                and g >= 0):
            faux.append(s[j]["date"])
        payes += g > 0
    return vues >= 5 and not faux and payes >= 1, "%s : %d entrées (%d paient), %d fausses %s" % (
        v, vues, payes, len(faux), faux[:3])


@cas("G6")
def g6():
    """G6 — `resumer` rend la somme du glissement et du gain glissement payé À CÔTÉ de `net`, jamais à sa place ; une
    liste sans glissement rend la forme d'avant. [rend: 1] [sort: non]"""
    J = modules()["J"]
    # (28-11-2026, lot I1FIX) chaque opération porte sa date de sortie : depuis la réunion I1 (règle UNIQUE
    # `MODULE_JUGEMENT.est_non_terminee`, motif FIN_DES_DONNEES OU sortie absente, A-1100), une opération sans sortie est
    # NON TERMINÉE et `resumer` la met à part — ces opérations-ci, sans sortie, n'étaient plus résumées (KeyError 'net')
    ops = [{"net": 100.0, "motif": "TP", "date_sortie": "2026-01-05", "glissement": 30.0, "net_glissement_paye": 70.0},
           {"net": -50.0, "motif": "SL", "date_sortie": "2026-01-06", "glissement": 20.0, "net_glissement_paye": -70.0}]
    r = J.resumer(ops)
    r0 = J.resumer([{"net": 1.0, "motif": "TP", "date_sortie": "2026-01-05"}])
    ok = r["net"] == 50.0 and r.get("glissement") == 50.0 and r.get("net_glissement_paye") == 0.0 and \
        "glissement" not in r0
    return ok, str({k: r.get(k) for k in ("net", "glissement", "net_glissement_paye")})


@cas("G7")
def g7():
    """G7 — la mesure des ventes sur stop : un saut sous le stop compte son écart, une vente au stop compte 0, un
    objectif n'entre pas ; « déjà compté dans le gain » (R-607 ②). [rend: 1] [sort: non]"""
    G = modules()["G"]
    ops = [{"pe": 100.0, "px": 96.0, "motif": "SL_GAP"}, {"pe": 100.0, "px": 97.5, "motif": "SL"},
           {"pe": 100.0, "px": 104.0, "motif": "TP"}]
    r = G.glissement_des_ventes_sur_stop(ops, 0.025)
    ok = (r["ventes_sur_stop"] == 2 and r["dont_en_trou"] == 1 and abs(r["ecart_total_eur"] - 1000 * 1.5) < 1e-6
          and r["deja_compte_dans_le_gain"] is True)
    return ok, str(r)


def _ohlc_des_auteurs(nom):
    """Les données d'essai publiées par les auteurs d'EDGE. ① RÔLE — lire temoins/TEMOIN_EDGE_DES_AUTEURS_<nom>.csv,
    copie de pseudocode/<nom>.csv du dépôt github.com/eguidotti/bidask (licence MIT), prise le 27-11-2026.
    ② CONTEXTE D'APPEL — E1. ③ ENTRÉE — `nom`. ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — QUATRE listes.
    [rend: 4] ⑥ TRAITEMENT — case vide = NaN. ⑦ UNITÉ — prix. ⑧ POURQUOI — le calibrage se fait sur LEURS données.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
    import csv
    with open(os.path.join(RACINE, "temoins", "TEMOIN_EDGE_DES_AUTEURS_%s.csv" % nom), encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    lire = (lambda k: [float(x[k]) if x[k] else float("nan") for x in r])
    return lire("Open"), lire("High"), lire("Low"), lire("Close")


@cas("E1")
def e1():
    """E1 — CALIBRAGE OBLIGATOIRE D'EDGE : les chiffres PUBLIÉS par les auteurs dans leurs épreuves (python/tests/
    test_edge.py, tests/testthat/test-edge.R) sont reproduits : 0.0101849034905478 (ohlc.csv), −0.016889917516422
    (dix premières lignes, signé), 0.01013284969780197 (ohlc-miss.csv), NaN sur trois séances figées.
    [rend: 1] [sort: non]"""
    G = modules()["G"]
    o, h, l, c = _ohlc_des_auteurs("ohlc")
    a = G.edge(o, h, l, c)
    b = G.edge(o[:10], h[:10], l[:10], c[:10], True)
    o2, h2, l2, c2 = _ohlc_des_auteurs("ohlc-miss")
    d = G.edge(o2, h2, l2, c2)
    n = G.edge([18.21, 17.61, 17.61], [18.21, 17.61, 17.61], [17.61, 17.61, 17.61], [17.61, 17.61, 17.61])
    ok = (abs(a - 0.0101849034905478) < 1e-12 and abs(b - (-0.016889917516422)) < 1e-12
          and abs(d - 0.01013284969780197) < 1e-12 and math.isnan(n))
    return ok, "obtenu %r · %r · %r · %r" % (a, b, d, n)


@cas("E3")
def e3():
    """E3 — LA SENSIBILITÉ, sur de VRAIES séances : quatre combinaisons ; « EDGE|enchere_gratuite » est le coût retiré
    du gain (l'estimateur principal, la lecture par défaut) ; « CS|les_deux » est le calcul du lot W2e (Corwin-Schultz,
    deux ordres) ; `jouer` porte la sensibilité de chaque opération et `resumer` la somme. [rend: 1] [sort: non]"""
    m = modules()
    J, P, G = m["J"], m["P"], m["G"]
    cours, _, _ = vingt_ans()
    _f, jeton = fiche_d_essai()
    if isinstance(jeton, str):
        raise RuntimeError("jeton d'essai refusé : %s" % jeton)
    v = sorted(cours, key=lambda k: -len(cours[k]))[0]
    s = cours[v]
    faux, vues = [], 0
    for j in range(300, len(s) - 30, 499):
        op = J.jouer_une_entree(v, s, j, 0.04, 0.025, 10, P, recu=jeton)
        if op is None:
            continue
        vues += 1
        sb = G.sensibilite_du_glissement(s, j, op)
        ref = G.cout_du_glissement(s, j, op, "les_deux", estimateur="CS")["glissement_eur"]
        if not (len(sb) == 4 and abs(sb["EDGE|enchere_gratuite"] - op["glissement"]) < 1e-9
                and abs(sb["CS|les_deux"] - ref) < 1e-9 and G.ESTIMATEUR_PRINCIPAL == "EDGE"):
            faux.append(s[j]["date"])
    # (28-11-2026, lot I1FIX) la date de sortie, comme en G6 : sans elle l'opération est NON TERMINÉE (règle unique)
    ops = [{"net": 1.0, "motif": "TP", "date_sortie": "2026-01-05", "glissement": 1.0, "net_glissement_paye": 0.0,
            "glissement_sensibilite": {"A|x": 2.0, "B|y": 3.0}}] * 2
    r = J.resumer(ops)
    ok = vues >= 5 and not faux and r.get("glissement_sensibilite") == {"A|x": 4.0, "B|y": 6.0}
    return ok, "%s : %d entrées, %d fausses · résumé %s" % (v, vues, len(faux), r.get("glissement_sensibilite"))


# ───────────────────────── PIÈCE 3 — LA RAISON OBLIGATOIRE (A-1090) ─────────────────────────

@cas("R1")
def r1():
    """R1 — LA RAISON (A-1090, lot W2e-FIX) : une case VIDE ou ABSENTE est refusée par programme, par le contrat
    (`champs_de_la_declaration_manquants`) et par l'écrivain (`DECLARER_UNE_STRATEGIE.defauts_d_une_declaration`) ;
    « inconnue » et « aucune » écrits sont ACCEPTÉS (la loi : une stratégie sans explication connue n'est pas refusée) ;
    la vraie raison d'IND-001-RETEST passe ; le vrai fichier porte la case. [rend: 1] [sort: non]"""
    import csv
    m = modules()
    C, D = m["C"], m["D"]
    base = {c: "épreuve W2e" for c in C.DECLARATION_DATEE}
    base.update(cas="1", regard_sans_decision="")
    vraie = "après une forte baisse, le rebond prend du temps et secoue d'abord ; un stop serré coupe la position " \
            "avant le rebond"
    a = C.champs_de_la_declaration_manquants(dict(base, raison=vraie))
    b = C.champs_de_la_declaration_manquants(dict(base, raison="  "))
    c = C.champs_de_la_declaration_manquants(dict(base, raison=" Inconnue "))
    c2 = C.champs_de_la_declaration_manquants(dict(base, raison="aucune"))
    sans = dict(base)
    sans.pop("raison", None)
    d = C.champs_de_la_declaration_manquants(sans)
    ecrivain = D.defauts_d_une_declaration(dict(base, raison=""))
    ecrivain_inconnue = D.defauts_d_une_declaration(dict(base, raison="inconnue"))
    with open(os.path.join(RACINE, C.DECLARATIONS_DATEES), encoding="utf-8-sig") as f:
        entete = next(csv.reader(f))
    ok = (a == [] and b == ["raison"] and c == [] and c2 == [] and d == ["raison"]
          and any("raison" in x for x in ecrivain) and not any("raison" in x for x in ecrivain_inconnue)
          and "raison" in entete and entete == C.DECLARATION_DATEE)
    return ok, "vraie %s · vide %s · inconnue %s · aucune %s · absente %s · écrivain %s" % (a, b, c, c2, d, ecrivain[:2])


# ───────────────────────── PIÈCE 4 — LE RÉGLAGE « QUAND JOUER » (A-1079) ─────────────────────────

@cas("Q1")
def q1():
    """Q1 — la lecture du réglage. [rend: 1] [sort: non]"""
    Q = modules()["Q"]
    ok = Q.lire_quand_jouer("toujours") is None and Q.lire_quand_jouer("AGITE") == {"HAUSSE_AGITEE", "BAISSE_AGITEE"}
    ok = ok and Q.lire_quand_jouer("hausse + calme") == {"HAUSSE_CALME", "HAUSSE_AGITEE", "BAISSE_CALME"}
    try:
        Q.lire_quand_jouer("TEMPÊTE")
        ok = False
    except ValueError:
        pass
    return ok, "toujours, AGITE, hausse+calme, mot inconnu"


@cas("Q2")
def q2():
    """Q2 — AUCUN DÉCOUPAGE PAR DÉFAUT : un réglage autre que « toujours » sans découpage lève ; « toujours » n'en
    demande pas ; une date INCONNUE n'est pas jouée. [rend: 1] [sort: non]"""
    Q = modules()["Q"]
    try:
        Q.admis("AGITE", None, "2020-03-12")
        leve = False
    except ValueError:
        leve = True
    dec = Q.Decoupage("essai", {"2020-03-12": "BAISSE_AGITEE", "2020-03-13": "INCONNU"}, True)
    ok = leve and Q.admis("toujours", None, "x") and Q.admis("AGITE", dec, "2020-03-12") and \
        not Q.admis("AGITE", dec, "2020-03-13") and not Q.admis("CALME", dec, "2020-03-12")
    return ok, "sans découpage lève : %s" % leve


def fiche_d_essai(quand_jouer=None):
    """La fiche d'essai ESSAI-C5-2000-2026 et son jeton (A-853, A-863), bâties EN MÉMOIRE par les fonctions de
    PREPARER_LA_MOULINETTE_D_ESSAI (R-708), sans rien écrire.
    ① RÔLE — Jouer les 20 ans sans regard : la garde du regard unique (R-505 ③) refuse toute autre fiche sur
      2000-2023, une stratégie fictive comprise (mesuré le 27-11-2026 : RegardNonInscrit) ; le jeton d'essai n'est
      accordé qu'à cette fiche, hors d'un dépôt (racine sans .git). ② CONTEXTE D'APPEL — G5, Q3, A3.
    ③ ENTRÉE — `quand_jouer` : None, ou un réglage posé sur la fiche. ④ CONDITIONS D'ENTRÉE — RACINE sans .git.
    ⑤ SORTIE — DEUX valeurs : la fiche (dictionnaire) et le jeton (ou None et le motif du refus). [rend: 2]
    ⑥ TRAITEMENT — lire le registre, `ligne_source`, `periode_d_essai`, `ligne_d_essai`, `jeton_d_essai`.
    ⑦ UNITÉ — —. ⑧ POURQUOI — consigne du plan R505 : aucun regard sur une vraie stratégie 2000-2023 ; A-853 : la
    famille C5 est déjà jouée. ⑨ CE QUI CLOCHE — les GAINS de cette fiche ne sont jamais affichés ici, seules les
    décisions sont comparées. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
    import csv
    import io
    m = modules()
    PM, J = m["PM"], m["J"]
    octets = open(os.path.join(RACINE, PM.REGISTRE), "rb").read()
    lignes = list(csv.reader(io.StringIO(octets.decode("utf-8-sig"), newline="")))
    debut, fin = PM.periode_d_essai(PM.seances_du_fichier(os.path.join(RACINE, PM.COURS_DES_VINGT_ANS)))
    _ident, source = PM.ligne_source(lignes)
    fiche = dict(zip(lignes[0], PM.ligne_d_essai(lignes[0], source, debut, fin)))
    # LE JETON SE DEMANDE POUR LA FICHE D'ESSAI TELLE QU'AUTORISÉE (« toujours ») : depuis le lot W2e-FIX, « quand
    # jouer » entre dans l'empreinte, et la fiche portant un autre réglage est REFUSÉE (Q5). Le réglage est posé après :
    # `jouer` ne confronte que l'identifiant du jeton (limite écrite dans la note du lot W2e-FIX).
    jeton, motif = J.jeton_d_essai(RACINE, fiche, 1)
    if quand_jouer is not None:
        fiche["quand_jouer"] = quand_jouer
    return fiche, (jeton if jeton is not None else motif)


def univers_de_la_fiche(fiche):
    """Les valeurs de la fiche, par la lecture du juge (`mnemoniques_de_l_univers`, la clé par le mnémonique, R-708),
    présentes dans les 20 ans. ① RÔLE — l'univers joué. ② CONTEXTE D'APPEL — Q3, A3. ③ ENTRÉE — la fiche.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur, la liste des clés de cours. [rend: 1] ⑥ TRAITEMENT — comme `jouer`.
    ⑦ UNITÉ — —. ⑧ POURQUOI — jouer les valeurs que la fiche nomme. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — —.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    J = modules()["J"]
    cours, _, mnemo = vingt_ans()
    return [v for v in (mnemo.get(m, J.cle_valeur(m)) for m in J.mnemoniques_de_l_univers(fiche["univers"]))
            if v in cours]


@cas("Q3")
def q3():
    """Q3 — BRANCHEMENT dans `jouer`, VRAIE fiche d'essai et vraies séances (2 valeurs, 2019-2026) : sans découpage, un
    réglage « AGITE » est refusé AVANT calcul ; un découpage tout calme rend 0 opération ; tout agité, les mêmes
    opérations que « toujours ». [rend: 1] [sort: non]"""
    m = modules()
    J, P, Q = m["J"], m["P"], m["Q"]
    cours, _, mnemo = vingt_ans()
    fiche, jeton = fiche_d_essai()
    if isinstance(jeton, str):
        raise RuntimeError("jeton d'essai refusé : %s" % jeton)
    sig = J.signal_de_la_fiche(RACINE, fiche)
    u = univers_de_la_fiche(fiche)[:2]
    c2 = {v: [b for b in cours[v] if b["date"] >= "2019-01-01"] for v in u}
    dates = sorted({b["date"] for v in u for b in c2[v]})
    calme = Q.Decoupage("tout calme", {d: "HAUSSE_CALME" for d in dates}, True)
    agite = Q.Decoupage("tout agité", {d: "BAISSE_AGITEE" for d in dates}, True)
    f_ag = dict(fiche, quand_jouer="AGITE")
    try:
        J.jouer(f_ag, c2, mnemo, sig, P, recu=jeton)
        leve = False
    except ValueError:
        leve = True
    o_t, _ = J.jouer(fiche, c2, mnemo, sig, P, recu=jeton)
    o_c, _ = J.jouer(f_ag, c2, mnemo, sig, P, recu=jeton, types_de_marche=calme)
    o_a, _ = J.jouer(f_ag, c2, mnemo, sig, P, recu=jeton, types_de_marche=agite)
    ok = leve and len(o_t) > 5 and o_c == [] and o_a == o_t
    return ok, "refus sans découpage %s · toujours %d · calme %d · agité %d" % (leve, len(o_t), len(o_c), len(o_a))


@cas("Q4")
def q4():
    """Q4 — le SENS du découpage du jour même est celui de `METEO_DU_MARCHE.voyant` (R-708), à 6 vraies dates
    réparties ; avant 252 séances, INCONNU. [rend: 1] [sort: non]"""
    m = modules()
    Q, M = m["Q"], m["M"]
    ind = indice()
    dec = Q.decoupage_du_jour_meme(ind, 20, 0.80)
    dates = sorted(ind)
    faux = []
    for d in dates[300::1100]:
        vy = M.voyant({k: ind[k] for k in dates if k <= d})
        sens = "HAUSSE" if vy["couleur"] == "🟢" else "BAISSE"
        # l'ORACLE écrit à part : la moyenne des 200 dernières clôtures, sommées ici
        i = dates.index(d)
        moy = sum(ind[k] for k in dates[i - 199:i + 1]) / 200.0
        sens_oracle = "HAUSSE" if ind[d] > moy else "BAISSE"
        if not dec.types[d].startswith(sens) or sens != sens_oracle or abs(vy["moyenne_200"] - moy) > 1e-6:
            faux.append(d)
    ok = not faux and dec.types[dates[100]] == Q.INCONNU and dec.jour_meme
    return ok, "%d dates confrontées, désaccords %s" % (len(dates[300::1100]), faux)


@cas("Q5")
def q5():
    """Q5 — « QUAND JOUER » DANS L'EMPREINTE DES RÉGLAGES (lot W2e-FIX ; défaut D1 du lot W2e : le jeton d'essai était
    accordé à la fiche portant quand_jouer=BAISSE) : absent, vide et « toujours » gardent l'empreinte d'avant (la valeur
    figée du contrat) ; « BAISSE » la change et le jeton est REFUSÉ ; « HAUSSE+BAISSE » et « CALME+AGITE » (mêmes jours)
    ont la même empreinte. [rend: 1] [sort: non]"""
    import csv
    import io
    m = modules()
    J, PM, C = m["J"], m["PM"], m["C"]
    octets = open(os.path.join(RACINE, PM.REGISTRE), "rb").read()
    lignes = list(csv.reader(io.StringIO(octets.decode("utf-8-sig"), newline="")))
    debut, fin = PM.periode_d_essai(PM.seances_du_fichier(os.path.join(RACINE, PM.COURS_DES_VINGT_ANS)))
    _ident, source = PM.ligne_source(lignes)
    fiche = dict(zip(lignes[0], PM.ligne_d_essai(lignes[0], source, debut, fin)))
    lire = J.lire_module_du_jour(RACINE)
    emp = {k: J.empreinte_des_reglages(dict(fiche, **({} if k is None else {"quand_jouer": k})), lire)[0]
           for k in (None, "", "toujours", "BAISSE", "HAUSSE+BAISSE", "CALME+AGITE")}
    figee = {v[1] for v in C.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE.values() if isinstance(v, tuple)}
    j_plain, _ = J.jeton_d_essai(RACINE, fiche, 1)
    j_baisse, motif = J.jeton_d_essai(RACINE, dict(fiche, quand_jouer="BAISSE"), 1)
    ok = (emp[None] == emp[""] == emp["toujours"] and emp[None] in figee and emp["BAISSE"] != emp[None]
          and emp["HAUSSE+BAISSE"] == emp["CALME+AGITE"] != emp[None] and j_plain is not None and j_baisse is None)
    return ok, "toujours %s (figée : %s) · BAISSE %s · jeton BAISSE refusé : %s" % (
        emp[None], emp[None] in figee, emp["BAISSE"], j_baisse is None)


@cas("Q6")
def q6():
    """Q6 — LE DÉCOUPAGE PAR DÉFAUT EST CELUI DU JOUR MÊME (A-1105) : `decoupage_par_defaut` rend, sur l'indice lu par
    L5 (`lire_l_indice`) et les réglages du fichier de L5 (`lire_les_reglages`), le découpage `decoupage_du_jour_meme` ;
    le juge (`decoupage_pour_la_fiche`) ne lit rien pour « toujours » et le rend pour « AGITE ». [rend: 1] [sort: non]"""
    m = modules()
    Q, J, L5 = m["Q"], m["J"], m["L5"]
    reg = L5.lire_les_reglages(RACINE)
    dates, prix, _b = L5.lire_l_indice(RACINE)
    attendu = Q.decoupage_du_jour_meme(dict(zip(dates, prix)), reg["fenetre_de_volatilite"],
                                       reg["centile_d_agitation"]).types
    d = Q.decoupage_par_defaut(RACINE)
    ok = (d.jour_meme and d.types == attendu and J.decoupage_pour_la_fiche(RACINE, {"id": "x"}) is None
          and J.decoupage_pour_la_fiche(RACINE, {"id": "x", "quand_jouer": "AGITE"}) is d)
    return ok, "%d séances, réglages fenêtre %s centile %s" % (len(d.types), reg["fenetre_de_volatilite"],
                                                              reg["centile_d_agitation"])


@cas("Q7")
def q7():
    """Q7 — LA VOLATILITÉ EST CELLE DE L5 (R-708) : l'agitation de chaque séance se retrouve avec
    `DATER_LES_TYPES_DE_MARCHE.volatilites` et un seuil sur le seul passé, recalculé ici. [rend: 1] [sort: non]"""
    m = modules()
    Q, L5 = m["Q"], m["L5"]
    ind = indice()
    dates = sorted(ind)
    dec = Q.decoupage_du_jour_meme(ind, 20, 0.80).types
    vols = L5.volatilites([ind[d] for d in dates], 20)
    import bisect
    faux, passe, vues = [], [], 0
    for i, d in enumerate(dates):
        if vols[i] is not None:
            bisect.insort(passe, vols[i])
        if dec[d] == Q.INCONNU:
            continue
        vues += 1
        agite = vols[i] > passe[min(len(passe) - 1, int(0.80 * len(passe)))]
        if dec[d].endswith("_AGITEE") != agite:
            faux.append(d)
    return not faux and vues > 6000, "%d séances confrontées, désaccords %d %s" % (vues, len(faux), faux[:3])


@cas("M1")
def m1():
    """M1 — « QUAND JOUER » EST UNE VARIABLE DE LA MOULINETTE : avec une ligne au voisinage, PREPARER écrit une ligne
    jouable (la valeur de la fiche comprise, les doublons d'ensemble retirés) ; DECLINER la croise APRÈS les
    obligatoires (deux fois plus de versions, colonne `quand_jouer`) ; JOUER_LES_VERSIONS la porte dans la fiche
    fusionnée et `controler_fusion` la confronte ; sans ligne, colonnes et numéros d'avant. Le VRAI voisinage du dépôt
    porte la ligne, avec « toujours » seul. [rend: 1] [sort: non]"""
    import csv
    m = modules()
    PV, DL, JV, J = m["PV"], m["DL"], m["JV"], m["J"]
    fiche = {"id": "F", "tp": "4", "sl": "2.5", "horizon": "20", "univers": "AI,MC"}
    lig, manq = PV.ligne_quand_jouer("F", "E01", "h", fiche, {"liste": "toujours;AGITE;HAUSSE_AGITEE+BAISSE_AGITEE",
                                                              "raison": "r"})
    base = [{"parametre": p, "valeurs_a_essayer": v, "valeur_fiche": f, "jouable": "OUI", "strategie": "F",
             "essai": "E01"} for p, v, f in (("tp", "4;5", "4"), ("sl", "2.5", "2.5"), ("horizon", "20", "20"),
                                            ("univers", "AI,MC", "AI,MC"))]
    col0, ver0 = DL.decliner(base)
    col1, ver1 = DL.decliner(base + [dict(lig[0], strategie="F", essai="E01")])
    fus = JV.fusionner(dict(fiche, quand_jouer="toujours"), ver1[-1])
    pareil = JV.controler_fusion(J, dict(ver1[-1]), dict(ver1[-1]))
    ecart = JV.controler_fusion(J, dict(ver1[-1], quand_jouer="toujours"), dict(ver1[-1]))
    with open(os.path.join(RACINE, "donnees", "combinatoires", "VOISINAGE.csv"), encoding="utf-8") as f:
        vrai = {r["parametre"]: r for r in csv.DictReader(f)}
    ok = (not manq and lig[0]["valeurs_a_essayer"] == "toujours;AGITE" and "quand_jouer" not in col0
          and col1[-3] == "quand_jouer" and len(ver1) == 2 * len(ver0) and fus["quand_jouer"] == "AGITE"
          and pareil == [] and len(ecart) == 1 and ecart[0].startswith("quand_jouer")
          and vrai.get("quand_jouer", {}).get("liste") == "toujours")
    return ok, "valeurs %s · versions %d → %d · colonnes %s · même version %s · écart %s" % (
        lig[0]["valeurs_a_essayer"] if lig else manq, len(ver0), len(ver1), col1[3:-2], pareil, ecart)


# ───────────────────────── PIÈCE 2 — L'ÉPREUVE ANTI-AVENIR SUR LES 20 ANS (A-674, A-692) ─────────────────────────

@cas("A1")
def a1():
    """A1 — le découpage du jour même ne lit pas l'avenir : à 400 dates réparties sur les 20 ans, le type calculé sur
    l'indice COUPÉ à la date est celui calculé sur l'indice entier. [rend: 1] [sort: non]"""
    Q = modules()["Q"]
    ind = indice()
    plein = Q.decoupage_du_jour_meme(ind, 20, 0.80).types
    dates = sorted(ind)
    pas = max(1, len(dates) // 400)
    diff = []
    for d in dates[::pas]:
        coupe = Q.decoupage_du_jour_meme({k: ind[k] for k in dates if k <= d}, 20, 0.80).types
        if coupe[d] != plein[d]:
            diff.append(d)
    return not diff, "%d dates, %d changent quand l'avenir est caché %s" % (len(dates[::pas]), len(diff), diff[:3])


@cas("A2")
def a2():
    """A2 — TÉMOIN QUI DOIT ÉCHOUER (le motif se calibre sur un cas qui échoue) : un découpage « après coup » — le seuil
    d'agitation pris sur TOUTE la période, comme celui de l'étape 2 (`seuil_d_agitation` du lot L5, son ⑨) — CHANGE
    à des dates coupées : la même mesure que A1 le voit. Il documente la question R5-2. [rend: 1] [sort: non]"""
    Q = modules()["Q"]
    ind = indice()
    dates = sorted(ind)

    def apres_coup(serie):
        """Le découpage d'après coup, construit ici pour l'épreuve. [rend: 1] [sort: non]"""
        jm = Q.decoupage_du_jour_meme(serie, 20, 0.80).types
        ds = sorted(serie)
        p = [serie[d] for d in ds]
        r = [None] + [math.log(p[i] / p[i - 1]) for i in range(1, len(p))]
        vols = {}
        for i in range(20, len(p)):
            x = r[i - 19:i + 1]
            mu = sum(x) / 20
            vols[ds[i]] = math.sqrt(sum((a - mu) ** 2 for a in x) / 20)
        tri = sorted(vols.values())
        seuil = tri[min(len(tri) - 1, int(0.80 * len(tri)))]
        return {d: (t if t == Q.INCONNU else t.split("_")[0] + ("_AGITEE" if vols[d] > seuil else "_CALME"))
                for d, t in jm.items()}
    plein = apres_coup(ind)
    diff = 0
    echantillon = dates[300::40]
    for d in echantillon:
        if apres_coup({k: ind[k] for k in dates if k <= d})[d] != plein[d]:
            diff += 1
    return diff > 0, "%d dates sur %d changent : la mesure voit la lecture de l'avenir" % (diff, len(echantillon))


@cas("A3")
def a3():
    """A3 — LA CHAÎNE ENTIÈRE SUR LES 20 ANS, fiche d'essai ESSAI-C5-2000-2026 (A-853 ; jamais une vraie stratégie,
    jamais un gain affiché) : `jouer` avec le réglage « BAISSE » sur le découpage du jour même ; à 8 dates de coupure
    réparties, les cours ET l'indice coupés à la date D : chaque décision d'avant D (valeur, jour du signal, jour et prix
    d'achat, demi-écart estimé à l'achat) est la même qu'avec tout l'historique, sur les valeurs de la fiche.
    [rend: 1] [sort: non]"""
    m = modules()
    J, P, Q, G = m["J"], m["P"], m["Q"], m["G"]
    cours, _, mnemo = vingt_ans()
    fiche, jeton = fiche_d_essai("BAISSE")
    if isinstance(jeton, str):
        raise RuntimeError("jeton d'essai refusé : %s" % jeton)
    sig = J.signal_de_la_fiche(RACINE, fiche)
    u = univers_de_la_fiche(fiche)
    c6 = {v: cours[v] for v in u}
    ind = indice()

    def decisions(cs, ops, avant):
        """Les décisions d'avant une date, avec le demi-écart d'achat. [rend: 1] [sort: non]"""
        out = []
        for o in ops:
            if o["date_entree"] >= avant:   # un achat à la séance D elle-même, dernière séance coupée, n'a pas de vente
                continue
            s = cs[o["valeur"]]
            j = next(k for k, b in enumerate(s) if b["date"] == o["date_entree"])
            out.append((o["valeur"], o["date_signal"], o["date_entree"], o["pe"], G.ecart_estime_avant(s, j)))
        return sorted(out)
    ops_plein, _ = J.jouer(fiche, c6, mnemo, sig, P, recu=jeton,
                           types_de_marche=Q.decoupage_du_jour_meme(ind, 20, 0.80))
    dates = sorted(ind)
    coupures = [dates[int(len(dates) * k / 9)] for k in range(1, 9)]
    rates, vues = [], 0
    for D in coupures:
        cs = {v: [b for b in c6[v] if b["date"] <= D] for v in u}
        dec = Q.decoupage_du_jour_meme({k: ind[k] for k in dates if k <= D}, 20, 0.80)
        ops_c, _ = J.jouer(fiche, cs, mnemo, sig, P, recu=jeton, types_de_marche=dec)
        a, b = decisions(cs, ops_c, D), decisions(c6, ops_plein, D)
        vues += len(b)
        if a != b:
            rates.append(D)
    return not rates and vues > 20, "%d coupures, %d décisions comparées, coupures en écart %s (valeurs jouées : %s)" % (
        len(coupures), vues, rates[:3], ",".join(sorted({o["valeur"] for o in ops_plein})))


# ───────────────────────── SABOTAGES ─────────────────────────
# nom : (fichier, phrase exacte, remplacement, cas qui doivent rougir) ou (fichier, [(phrase, remplacement)…], cas)
SABOTAGES = {
    "S_formule_sans_nuit": ("programmes/MODULE_GLISSEMENT.py",
                            [("    if l2 > c1:                       # montée pendant la nuit", "    if False:"),
                             ("    elif h2 < c1:                     # baisse pendant la nuit", "    elif False:")],
                            ["G1"]),
    "S_negatif_garde": ("programmes/MODULE_GLISSEMENT.py", "    return max(0.0, s)", "    return s", ["G1"]),
    "S_ecart_lit_le_jour": ("programmes/MODULE_GLISSEMENT.py", "    for k in range(max(1, j - fenetre), j):",
                            "    for k in range(max(1, j - fenetre), min(j + 1, len(serie))):", ["G3"]),
    # lot W2e-FIX
    "S_edge_lit_le_jour": ("programmes/MODULE_GLISSEMENT.py", "    b = serie[max(0, j - fenetre - 1):j]",
                           "    b = serie[max(0, j - fenetre - 1):j + 1]", ["G3"]),
    "S_edge_formule": ("programmes/MODULE_GLISSEMENT.py", "    x2 = [-4.0 / po * d1[i] * r5[i]",
                       "    x2 = [-4.0 / po * d1[i] * r2[i]", ["E1"]),
    "S_edge_sans_demoyenne": ("programmes/MODULE_GLISSEMENT.py", "    d3 = [r3[i] - mr3 / pt * tau[i] for i in k]",
                              "    d3 = list(r3)", ["E1"]),
    # l'achat payant aux DEUX endroits qui le décident (le coût, et le calcul évité d'un écart non payé)
    "S_enchere_paie_l_achat": ("programmes/MODULE_GLISSEMENT.py",
                               [('    paie_achat = ordres_qui_paient == "les_deux"\n    paie_vente = ordres_qui_paient == '
                                 '"les_deux" or vente["motif"] in MOTIFS_VENDUS_EN_SEANCE\n    cap',
                                 '    paie_achat = True\n    paie_vente = ordres_qui_paient == '
                                 '"les_deux" or vente["motif"] in MOTIFS_VENDUS_EN_SEANCE\n    cap'),
                                ('    paie_achat = ordres_qui_paient == "les_deux"\n    paie_vente = paie_achat or',
                                 '    paie_achat = True\n    paie_vente = paie_achat or')], ["G4"]),
    # le seul `_cout` faussé : la sensibilité ne dit plus le coût retiré du gain
    "S_cout_paie_l_achat": ("programmes/MODULE_GLISSEMENT.py",
                            '    paie_achat = ordres_qui_paient == "les_deux"\n    paie_vente = ordres_qui_paient == '
                            '"les_deux" or vente["motif"] in MOTIFS_VENDUS_EN_SEANCE\n    cap',
                            '    paie_achat = True\n    paie_vente = ordres_qui_paient == '
                            '"les_deux" or vente["motif"] in MOTIFS_VENDUS_EN_SEANCE\n    cap', ["E3"]),
    "S_le_trou_paie": ("programmes/MODULE_GLISSEMENT.py", 'MOTIFS_VENDUS_EN_SEANCE = ("TP", "SL")',
                       'MOTIFS_VENDUS_EN_SEANCE = ("TP", "SL", "SL_GAP", "TP_GAP", "HORIZON")', ["G4"]),
    "S_principal_cs": ("programmes/MODULE_GLISSEMENT.py", 'ESTIMATEUR_PRINCIPAL = "EDGE"',
                       'ESTIMATEUR_PRINCIPAL = "CS"', ["E3"]),
    "S_glissement_non_retire": ("programmes/JUGE_DES_STRATEGIES.py",
                                '"net_glissement_paye": net - _g["glissement_eur"],', '"net_glissement_paye": net,',
                                ["G5"]),
    "S_resumer_sans_glissement": ("programmes/JUGE_DES_STRATEGIES.py",
                                  '           if all("net_glissement_paye" in o for o in ops) else {})',
                                  "           if False else {})", ["G6"]),
    "S_raison_inconnue_refusee": ("programmes/CONTRATS_DES_FICHIERS.py",
                                  '    manquants = [c for c in exiges if not (declaration.get(c) or "").strip()]\n',
                                  '    manquants = [c for c in exiges if not (declaration.get(c) or "").strip() or '
                                  '(declaration.get(c) or "").strip().lower() == "inconnue"]\n', ["R1"]),
    "S_raison_hors_contrat": ("programmes/CONTRATS_DES_FICHIERS.py", '    "raison",                 # POURQUOI',
                              "                              # POURQUOI", ["R1"]),
    "S_decoupage_par_defaut": ("programmes/MODULE_QUAND_JOUER.py", "    if decoupage is None:\n        raise",
                               "    if decoupage is None:\n        return True\n        raise", ["Q2"]),
    "S_filtre_retire": ("programmes/JUGE_DES_STRATEGIES.py",
                        "                if not MODULE_QUAND_JOUER.admis(_qj, types_de_marche, d_sig):",
                        "                if False:", ["Q3"]),
    "S_empreinte_sans_quand_jouer": ("programmes/JUGE_DES_STRATEGIES.py",
                                     '    _fin = () if _qj is None else (("quand_jouer", _qj),)', "    _fin = ()", ["Q5"]),
    "S_defaut_autre_centile": ("programmes/MODULE_QUAND_JOUER.py", '                                                  reg["centile_d_agitation"])',
                               "                                                  0.5)", ["Q6"]),
    "S_volatilite_decalee": ("programmes/MODULE_QUAND_JOUER.py",
                             "    vols = D.volatilites([float(indice[d]) for d in dates], f)",
                             "    vols = D.volatilites([float(indice[d]) for d in dates], f + 1)", ["Q7"]),
    "S_moyenne_faussee": ("programmes/METEO_DU_MARCHE.py",
                          "        moy = somme / SEANCES_MOYENNE if k >= SEANCES_MOYENNE - 1 else None",
                          "        moy = somme / (SEANCES_MOYENNE - 1) if k >= SEANCES_MOYENNE - 1 else None", ["Q4"]),
    "S_sens_du_lendemain": ("programmes/MODULE_QUAND_JOUER.py",
                            '        sens = "HAUSSE" if dessus[i] else "BAISSE"',
                            '        sens = "HAUSSE" if dessus[min(i + 1, len(dessus) - 1)] else "BAISSE"', ["A1"]),
    "S_seuil_sur_toute_la_periode": ("programmes/MODULE_QUAND_JOUER.py",
                                     [("    connues, types = [], {}",
                                       "    connues, types = sorted(v for v in vols if v is not None), {}"),
                                      ("            bisect.insort(connues, vol)", "            pass")], ["A1"]),
    "S_moulinette_ignore_quand_jouer": ("programmes/JOUER_LES_VERSIONS.py",
                                        "        if k in version:\n            f[k] = version[k]",
                                        "        if False:\n            f[k] = version[k]", ["M1"]),
    "S_decliner_sans_facultatif": ("programmes/DECLINER_LES_STRATEGIES.py",
                                   '    return OBLIGATOIRES + tuple(p for p in FACULTATIFS if p in par and '
                                   'par[p].get("jouable") == "OUI")', "    return OBLIGATOIRES", ["M1"]),
}


def jouer_les_cas(noms):
    """Joue des cas et rend le code. ① RÔLE — exécuter et afficher. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — noms.
    ④ CONDITIONS D'ENTRÉE — noms connus. ⑤ SORTIE — UNE valeur : 0 tout vert, 1 un rouge, 2 une exception. [rend: 1]
    ⑥ TRAITEMENT — chaque cas, sa ligne. ⑦ UNITÉ — —. ⑧ POURQUOI — R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    code = 0
    for n in noms:
        try:
            ok, det = CAS[n]()
        except Exception as e:
            print("  EXCEPTION %s — %s: %s" % (n, type(e).__name__, e), flush=True)
            code = 2
            continue
        print("  %s %s — %s" % ("VERT " if ok else "ROUGE", n, det), flush=True)
        if not ok and code == 0:
            code = 1
    return code


def saboter(nom):
    """Joue un sabotage dans une copie et dit s'il mord. ① RÔLE — R-731 : la dent de chaque épreuve. ② CONTEXTE
    D'APPEL — `main --saboter`. ③ ENTRÉE — le nom. ④ CONDITIONS D'ENTRÉE — la phrase visée existe UNE fois.
    ⑤ SORTIE — UNE valeur : (mord : vrai/faux/None si introuvable, détail). [rend: 1] ⑥ TRAITEMENT — copie de
    programmes/, liens pour le reste, remplacement, processus neuf sur les cas visés, code attendu 1.
    ⑦ UNITÉ — —. ⑧ POURQUOI — une épreuve qui reste verte sans ce qu'elle teste est une décoration.
    ⑨ CE QUI CLOCHE — un sabotage qui fait LEVER (code 2) n'est pas compté comme mordu. ⑩ EFFET — écrit et efface une
    copie temporaire. ⑪ TERMINAISON — délai de 900 s. [sort: oui]"""
    sab = SABOTAGES[nom]
    fichier, cibles = sab[0], sab[-1]
    paires = sab[1] if len(sab) == 3 else [(sab[1], sab[2])]
    tmp = tempfile.mkdtemp(prefix="w2e_sabot_")
    try:
        for e in os.listdir(RACINE):
            if e == "programmes":
                shutil.copytree(os.path.join(RACINE, e), os.path.join(tmp, e))
            else:
                os.symlink(os.path.join(RACINE, e), os.path.join(tmp, e))
        ch = os.path.join(tmp, fichier)
        texte = open(ch, encoding="utf-8").read()
        for avant, apres in paires:
            if texte.count(avant) != 1:
                return None, "phrase visée trouvée %d fois : %r" % (texte.count(avant), avant[:60])
            texte = texte.replace(avant, apres)
        open(ch, "w", encoding="utf-8").write(texte)
        p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), tmp, "--cas=" + ",".join(cibles)],
                           capture_output=True, text=True, timeout=900)
        rouges = [l.split()[1] for l in p.stdout.splitlines() if l.strip().startswith("ROUGE")]
        return p.returncode == 1 and bool(rouges), "code %d, rougis %s" % (p.returncode, rouges)
    except subprocess.TimeoutExpired:
        return False, "délai dépassé"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv):
    """Point d'entrée. ① RÔLE — lire les arguments, jouer Z0 et les sabotages. ② CONTEXTE D'APPEL — la ligne de
    commande. ③ ENTRÉE — argv. ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur, le code. [rend: 1]
    ⑥ TRAITEMENT — voir l'en-tête. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    global RACINE
    if len(argv) < 2:
        print("USAGE : python3 -B %s <racine> [--saboter | --cas=A,B]" % os.path.basename(__file__))
        return 2
    RACINE = os.path.abspath(argv[1])
    opts = argv[2:]
    inconnus = [o for o in opts if o != "--saboter" and not o.startswith("--cas=")]
    if inconnus or len(opts) > 1:
        print("ARGUMENT INCONNU OU EN TROP : %s" % opts)
        return 2
    if opts and opts[0].startswith("--cas="):
        noms = [n for n in opts[0][6:].split(",") if n]
        if any(n not in CAS for n in noms) or not noms:
            print("CAS INCONNU : %s" % noms)
            return 2
        return jouer_les_cas(noms)
    print("== Z0 : %d cas, racine %s" % (len(CAS), RACINE), flush=True)
    code = jouer_les_cas(list(CAS))
    print("== Z0 : code %d" % code, flush=True)
    if opts == ["--saboter"]:
        for nom in SABOTAGES:
            mord, det = saboter(nom)
            print("%s %s : %s" % (nom, "mord" if mord else ("INTROUVABLE" if mord is None else "NE MORD PAS"), det),
                  flush=True)
            if mord is None:
                code = 2
            elif not mord and code == 0:
                code = 1
    print("CODE %d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
