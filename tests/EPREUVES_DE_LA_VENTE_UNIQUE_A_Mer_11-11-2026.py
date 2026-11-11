#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_VENTE_UNIQUE (agent A) — Mer 11-11-2026 (Paris) — plan V7, bloc 4 : « le juge vend de toutes les façons ».
Simulation uniquement — aucun ordre réel, jamais.

LE SENS EN TÊTE. Le 11-11-2026, la décision « quand et à quel prix vendre » vit à UN endroit,
`programmes/MODULE_POSITIONS.vendre` : le juge des stratégies (`jouer_une_entree`), le circuit du soir
(`TENIR_LES_POSITIONS.cloturer`) l'appellent — le radar garde son recalcul indépendant (A-208 ⑤) ; les deux seuils se
posent par `seuils_de_vente` (arrondis à cinq décimales, décision de Jean-Luc du 07-11-2026 à 15h49, n°311) et le prix
de convention par `prix_de_convention`. Deux implémentations d'une même chose divergent toujours (R-708). Une durée
« aucune » (contrat du lot 0, `programmes/COMMUN.py`) devient jouable par le juge et tenable par le soir. Le soir ne
donne plus de signal à une fiche que le juge refuse (BACKLOG A-706 ④), et continue de tenir les positions quand
aucune fiche n'est VIVANTE (message du Chat du 11-11-2026 à 02h35). Ce fichier prouve ces propriétés, et que chaque
épreuve a des dents : chaque sabotage retire une protection et au moins une épreuve doit rougir (R-731).

CE QUI EST ÉPROUVÉ :
  V1 « garder » : une série qui s'arrête avant l'échéance rend None ; « vendre » vend à la dernière clôture.
  V2 « aucune » : `vendre` ne vend que sur un seuil ; sans seuil, « garder » rend None, « vendre » la dernière clôture.
  V3 VRAIE LIGNE (R-732), témoin du golden : ENGIE achetée le 17-06-2024 à 13,25 ; plus haut du 21-06 = 13,78 =
     l'objectif arrondi : vendue le 21-06 à 13,78 (n°311 ; avant, le juge vendait le 24-06).
  V4 refus : horizon 0, True, 20.0, « 20 », None ; fin des données inconnue ; seuils ambigus → ValueError.
  V5 LA MÊME VENTE PARTOUT, sur les vraies séries du témoin (ENGIE, VINCI, AIRBUS), chaque séance d'achat dont
     l'échéance est connue : le juge, le soir (une position fabriquée comme `entrer` la fabrique) et le radar rendent
     le même motif, la même date, le même prix réel (le juge et le soir).
  V6 le soir et « aucune » : `reglages_du_registre` → `horizon_connu` rend HORIZON_AUCUNE (jamais 20),
     `completer_echeances` écrit « aucune », `cloturer` garde la position sans seuil touché et la vend à l'objectif.
  V7 `fiche_suivie` (juge) : une fiche à l'achat « CLOSE » est refusée ; la vraie fiche C5E10-OBS-V1 est acceptée.
  V8 VALEURS CONNUES écrites à la main, motif par motif (TP, TP_GAP, SL, SL_GAP, HORIZON, garder, fin des données) :
     `vendre` et `prix_de_convention`. Le radar garde son recalcul INDÉPENDANT (A-208 ⑤) : il n'est plus éprouvé ici.
  V14 `juger` refuse tout horizon illisible (N2 du relecteur, tour 2).
  V12 `juger` refuse une fiche « aucune » avec son motif nommé ; V13 l'embargo proposé exclut les 30 % et la fin des données.
  V9 propriété R-708 par l'arbre syntaxique : le soir n'appelle pas `tester_seance`.
  V11 le juge joue une fiche « aucune » (ENGIE du témoin) : aucune vente à l'échéance avant la fin des données.
  V10 DE BOUT EN BOUT, `TENIR_LES_POSITIONS.py` sur une copie : (a) aucune fiche VIVANTE, une position en attente
      d'entrée (Vinci, signal du 06-06-2024) → code 0, vendue au stop le 07-06 à 110,76 ; (b) la fiche
      C5E10-OBS-V1 refusée (achat « CLOSE ») et un signal VINCI (univers d'elle seule), avec un champ
      « garde_du_soir » dans le fichier des signaux → code 0, refus dit, aucune position ouverte ; (c) JONCTION :
      le détecteur puis le teneur, univers « TTE,ZZZ » : aucune position pour la fiche refusée (LC-1).

USAGE : python3 -B tests/EPREUVES_DE_LA_VENTE_UNIQUE_A_Mer_11-11-2026.py <racine du dépôt> [--saboter | nom]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si une cible de
sabotage est introuvable.
Chaque épreuve travaille sur une COPIE temporaire : `programmes/` copié, `donnees/` et `temoins/` en liens
symboliques, sauf les fichiers que l'épreuve écrit (registre, positions, journal, signaux), copiés.

① RÔLE — Prouver la vente unique du bloc 4 et la garde du soir côté positions. ② CONTEXTE D'APPEL — À la main ; par
la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque fichier de tests/ avec la racine, puis avec
« --saboter ». ③ ENTRÉE — la racine, et facultativement « --saboter » ou un nom. ④ CONDITIONS D'ENTRÉE — le témoin du
golden sous temoins/, `donnees/cours_maitre.csv`, le registre des stratégies avec C5E10-OBS-V1. ⑤ SORTIE — le code de
sortie, une ligne par épreuve rouge. [rend: 1] ⑥ TRAITEMENT — pour Z0 puis chaque sabotage : copier, saboter, jouer
V1-V9 dans un sous-processus de la copie, puis V10 par deux lancements du programme du soir. ⑦ UNITÉ — seuils en
FRACTIONS, prix en euros, horizon en séances. ⑧ POURQUOI — voir le sens en tête. ⑨ CE QUI CLOCHE — V5 ne compare
que les séances d'achat dont l'échéance est dans la série (le soir garde, le juge vend : la différence voulue) ; la
copie en liens symboliques suppose que le programme du soir n'écrit, sous donnees/, que les positions et le journal
(vérifié par lecture de `tenir_pour_de_vrai` le 11-11-2026 ; un autre fichier écrit le serait dans le dépôt).
⑩ EFFET — dossiers temporaires, effacés. ⑪ TERMINAISON — chaque sous-processus est borné à 900 s. [sort: oui — code]
"""
import csv, json, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MODP, BAN = "programmes/MODULE_POSITIONS.py", "programmes/JUGE_DES_STRATEGIES.py"
TEN, C5 = "programmes/TENIR_LES_POSITIONS.py", "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"
ECRITS = ("cac40_strategies.csv", "claude_positions_ouvertes.csv", "claude_journal_trades.csv", "signaux_du_jour.json",
          "cours_maitre.csv")   # le maître est copié : V10c en retire la séance du 10-11-2026

SABOTAGES = {
    "Z0": [],
    "S1_garder_vend_quand_meme": [(MODP, '    if fin_des_donnees == "garder" or not apres:', '    if not apres:')],
    "S2_aucune_lue_comme_vingt": [(MODP, '    if aucune:\n        suite = serie[j:]\n', '    if aucune:\n        suite = serie[j:j + 21]\n')],
    "S3_seuils_bruts": [(MODP, '    return float("%.5f" % (prix_entree * (1.0 + tp))), float("%.5f" % (prix_entree * (1.0 - sl)))',
                         '    return prix_entree * (1.0 + tp), prix_entree * (1.0 - sl)')],
    "S4_horizon_flottant_accepte": [(MODP, '    if not aucune and (type(h) is not int or h <= 0):', '    if not aucune and h <= 0:')],
    "S5_seuils_ambigus_acceptes": [(MODP, '    if en_euros and en_fractions:\n        raise', '    if False:\n        raise')],
    "S6_soir_vend_a_la_fin_des_donnees": [(TEN, '{"objectif": tp, "stop": sl, "horizon": h}, "garder")', '{"objectif": tp, "stop": sl, "horizon": h}, "vendre")')],
    "S7_horizon_connu_filtre_aucune": [(TEN, '    if h is HORIZON_AUCUNE:\n        return h\n    return h if', '    return h if')],
    "S8_reglages_relit_par_lire_horizon": [(TEN, '"horizon": lire_horizon_ou_aucune(x.get("horizon", ""))}', '"horizon": lire_horizon(x.get("horizon", ""))}')],
    # S9 = M9 du relecteur neuf du 11-11-2026 : le prix de convention d'une échéance devient l'objectif.
    "S9_convention_horizon_a_l_objectif": [(MODP, '    if motif.startswith("TP"):\n        return objectif\n    return prix_sortie',
                                            '    if motif.startswith("TP"):\n        return objectif\n    return objectif')],
    "S10_juger_ne_refuse_plus_aucune": [(BAN, '    if h is HORIZON_AUCUNE:\n        raise ValueError(MOTIF_AUCUNE_NON_TRANCHEE)',
                                          '    if False:\n        raise ValueError(MOTIF_AUCUNE_NON_TRANCHEE)')],
    "S15_embargo_mesure_sur_les_30_et_la_fin_des_donnees": [(BAN, '        if o["date_signal"] > frontiere or o["motif"] == "HORIZON":\n            continue',
                                                             '        if False:\n            continue')],
    "S17_juger_juge_un_horizon_illisible": [(BAN, '    if h is None:\n        raise ValueError("fiche %s non jugeable : horizon illisible %r"',
                                             '    if False:\n        raise ValueError("fiche %s non jugeable : horizon illisible %r"')],
    "S16_convention_gap_au_prix_reel": [(MODP, '    if motif.startswith("SL"):\n        return stop', '    if motif.startswith("SL"):\n        return prix_sortie')],
    "S11_refus_du_juge_muet": [(BAN, '    if not porte[0]:\n        return None, None,', '    if False:\n        return None, None,')],
    # S18 (LC-1, RELU Cowork ab8fc49f) : le contrôle du référentiel retiré de `fiche_suivie` — la jonction V10c rougit.
    "S18_referentiel_non_controle": [(BAN, '    if inconnus:\n        return None, None,', '    if False:\n        return None, None,')],
    # S19 : le teneur ne demande plus au juge (`fiche_suivie`) : il donne les signaux à toute fiche VIVANTE.
    "S19_teneur_sans_la_garde": [(TEN, '            _refus = juge.fiche_suivie(base, ligne, _mnemo_du_juge)[2]', '            _refus = None')],
    "S12_aucune_vivante_arrete_tout": [(TEN, "les positions deja ouvertes sont tenues.\")\n", "les positions deja ouvertes sont tenues.\")\n        return 1\n")],
    "S13_completer_sans_aucune": [(TEN, '        if h is HORIZON_AUCUNE:\n            if ancienne not in', '        if False:\n            if ancienne not in')],
    "S14_juge_relit_par_lire_horizon": [(BAN, '    h = lire_horizon_ou_aucune(fiche["horizon"])\n    if h is None:', '    h = lire_horizon(fiche["horizon"])\n    if h is None:')],
}

CODE = r'''
import sys, os, json, glob, ast, csv
sys.path.insert(0, "programmes")
import MODULE_POSITIONS as P, JUGE_DES_STRATEGIES as B, TENIR_LES_POSITIONS as T, COMMUN
import importlib.util
sp = importlib.util.spec_from_file_location("c5", glob.glob("programmes/MODULE_C5_ETENDU_10_*.py")[0])
C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
A = COMMUN.HORIZON_AUCUNE
res = {}
def note(nom, ok, det):
    res[nom] = [bool(ok), str(det)[:300]]
def essai(nom, f):
    try:
        f()
    except Exception as e:
        note(nom, False, "leve %s : %s" % (type(e).__name__, e))
def b(d, o, h, l, c):
    return {"date": "2026-01-%02d" % d, "open": o, "high": h, "low": l, "close": c, "volume": 1000}
cours = B.charger_cours(glob.glob("temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN*.csv")[0])
F = {"tp": 0.04, "sl": 0.025}

def v1():
    s = [b(1, 100, 100, 100, 100)] + [b(2 + i, 100, 101, 99, 100 + i / 10) for i in range(5)]
    g = P.vendre(s, 1, dict(F, horizon=20), "garder")
    v = P.vendre(s, 1, dict(F, horizon=20), "vendre")
    e = P.vendre(s, 1, dict(F, horizon=3), "garder")
    o = (g, (v["motif"], v["date_sortie"]), (e["motif"], e["date_sortie"], e["px"]))
    note("V1 garder : None avant l'echeance ; vendre : derniere cloture ; echeance dans la serie : vendue", o == (None, ("HORIZON", "2026-01-06"), ("HORIZON", "2026-01-05", 100.3)), o)
essai("V1", v1)

def v2():
    s = [b(1, 100, 100, 100, 100)] + [b(2 + i, 100, 101, 99, 100) for i in range(30)] + [b(32, 100, 104.5, 99.5, 104)]
    t = P.vendre(s, 1, dict(F, horizon=A), "garder")
    s2 = s[:-1]
    g = P.vendre(s2, 1, dict(F, horizon=A), "garder")
    v = P.vendre(s2, 1, dict(F, horizon=A), "vendre")
    o = ((t["motif"], t["date_sortie"], t["px"]), g, (v["motif"], v["date_sortie"]))
    note("V2 aucune : vendue a l'objectif a la 31e seance ; sans seuil, garder None, vendre derniere cloture",
         o == (("TP", "2026-01-32", 104.0), None, ("HORIZON", "2026-01-31")), o)
essai("V2", v2)

def v3():
    s = cours["ENGIE"]; j = [k for k, x in enumerate(s) if x["date"] == "2024-06-17"][0]
    r = P.vendre(s, j, dict(F, horizon=20), "vendre")
    o = (s[j]["open"], r["motif"], r["date_sortie"], r["px"], P.seuils_de_vente(13.25, 0.04, 0.025))
    note("V3 vraie ligne ENGIE 17-06-2024 : vendue le 21-06 a 13,78 (seuils a 5 decimales, n°311)",
         o == (13.25, "TP", "2024-06-21", 13.78, (13.78, 12.91875)), o)
essai("V3", v3)

def v4():
    s = [b(1, 100, 100, 100, 100)] + [b(2 + i, 100, 101, 99, 100) for i in range(5)]
    o = []
    for nom, vente, fin in (("h0", dict(F, horizon=0), "vendre"), ("vrai", dict(F, horizon=True), "vendre"),
                            ("flottant", dict(F, horizon=20.0), "vendre"), ("texte", dict(F, horizon="20"), "vendre"),
                            ("None", dict(F, horizon=None), "vendre"), ("fin", dict(F, horizon=5), "attendre"),
                            ("ambigu", dict(F, horizon=5, objectif=104.0, stop=97.5), "garder")):
        try:
            P.vendre(s, 1, vente, fin); o.append((nom, "rien leve"))
        except ValueError:
            o.append((nom, "ValueError"))
    note("V4 refus : horizon 0, True, 20.0, texte, None ; fin inconnue ; seuils ambigus", all(x[1] == "ValueError" for x in o), o)
essai("V4", v4)

def v5():
    ecarts, n = [], 0
    for val in ("ENGIE", "VINCI", "AIRBUS"):
        s = cours[val]
        for j in range(1, len(s) - 21):
            juge = B.jouer_une_entree(val, s, j, 0.04, 0.025, 20, P, None, "HIST_FORFAIT_300")
            o, st = P.seuils_de_vente(s[j]["open"], 0.04, 0.025)
            pos = dict(strategie="X", valeur=val, date_signal=s[j - 1]["date"], date_entree=s[j]["date"],
                       prix_entree="%.5f" % s[j]["open"], tp="%.5f" % o, sl="%.5f" % st,
                       horizon_fin=T.echeance(s, s[j]["date"], 20), statut="OUVERTE", comptabilite="un_jeton",
                       regles_pre_trade="", explication="", frais_non_chiffrables="")
            tr, _r, _i = T.cloturer([pos], {val: s}, P, bareme="HIST_FORFAIT_300")
            n += 1
            if not tr:
                ecarts.append((val, j, "absent")); continue
            t0 = tr[0]
            a = (juge["motif"], juge["date_sortie"], "%.5f" % juge["px"])
            bb = (t0["motif_sortie"], t0["date_sortie"], t0["prix_sortie"])
            if a != bb:
                ecarts.append((val, s[j]["date"], a, bb))
    # le radar garde son recalcul INDEPENDANT (A-208 ⑤, decision de Jean-Luc du 14-08-2026) : il n'est pas compare ici.
    note("V5 la meme vente : juge et soir sur trois vraies series", n > 1500 and not ecarts, "%d achats, %d ecarts : %s" % (n, len(ecarts), ecarts[:2]))
essai("V5", v5)

def v6():
    import tempfile
    d = tempfile.mkdtemp()
    reg = os.path.join(d, "donnees"); os.makedirs(reg)
    src = "donnees/cac40_strategies.csv"
    lignes = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    champs = list(lignes[0].keys())
    for l in lignes:
        if l["id"] == "C5E10-OBS-V1":
            l["horizon"] = "aucune"
    w = csv.DictWriter(open(os.path.join(reg, "cac40_strategies.csv"), "w", encoding="utf-8", newline=""), fieldnames=champs)
    w.writeheader(); w.writerows(lignes)
    sys.modules.pop("JUGE_DES_STRATEGIES", None)
    r = T.reglages_du_registre(d)
    p = dict(strategie="C5E10-OBS-V1", valeur="AIRBUS", date_signal="2026-01-01", date_entree="2026-01-02",
             prix_entree="100.00000", tp="104.00000", sl="97.50000", horizon_fin="EN_ATTENTE", statut="OUVERTE",
             comptabilite="un_jeton", regles_pre_trade="", explication="", frais_non_chiffrables="")
    s = [b(1, 100, 100, 100, 100)] + [b(2 + i, 100, 101, 99, 100) for i in range(28)]
    hc, hd = T.horizon_connu(p, r), T.horizon_de(p, r, 20)
    T.completer_echeances([p], {"AIRBUS": s}, r)
    fin = p["horizon_fin"]
    tr1, rest1, _ = T.cloturer([p], {"AIRBUS": s}, P, bareme="HIST_FORFAIT_300")
    s2 = s + [b(30, 100, 104.2, 99.5, 104)]
    tr2, rest2, _ = T.cloturer([p], {"AIRBUS": s2}, P, bareme="HIST_FORFAIT_300")
    o = (hc is A, hd is A, fin, len(tr1), len(rest1), [(x["motif_sortie"], x["date_sortie"]) for x in tr2])
    note("V6 le soir et aucune : jamais 20, echeance « aucune », gardee 28 seances, vendue a l'objectif",
         o == (True, True, "aucune", 0, 1, [("TP", "2026-01-30")]), o)
essai("V6", v6)

def v7():
    from CONTRATS_DES_FICHIERS import fiches_du_registre, chemin_du_registre
    f = fiches_du_registre(chemin_du_registre("."))["C5E10-OBS-V1"]
    mn = B.table_mnemoniques(B.trouver(".", "REFERENTIEL_VALEURS"))
    a = B.fiche_suivie(".", f, mn)[2]
    r = B.fiche_suivie(".", dict(f, entree="CLOSE"), mn)[2]
    note("V7 refus du juge : C5E10-OBS-V1 acceptee, la meme a l'achat CLOSE refusee", a is None and bool(r), (a, r))
essai("V7", v7)

def v8():
    # VALEURS CONNUES, ECRITES A LA MAIN (demande du Chat du 11-11-2026) : achat 100, objectif +4 % = 104, stop -2,5 % = 97,5.
    def serie(*jours):
        return [b(1, 100, 100, 100, 100)] + [b(2 + i, *x) for i, x in enumerate(jours)]
    plat = (100, 101, 99, 100)
    cas = {
        "TP": (serie((100, 104.5, 99.5, 104.2), plat, plat), 3, "garder", ("TP", "2026-01-02", 104.0, 104.0)),
        "TP_GAP": (serie(plat, (105, 106, 104.5, 105.5), plat), 3, "garder", ("TP_GAP", "2026-01-03", 105.0, 104.0)),
        "SL": (serie((100, 100.5, 97.0, 97.2), plat, plat), 3, "garder", ("SL", "2026-01-02", 97.5, 97.5)),
        "SL_GAP": (serie(plat, (96.0, 96.5, 95.0, 95.5), plat), 3, "garder", ("SL_GAP", "2026-01-03", 96.0, 97.5)),
        "HORIZON": (serie(plat, plat, plat, (100, 101, 99, 100.7), plat), 3, "garder", ("HORIZON", "2026-01-05", 100.7, 100.7)),
        "garder": (serie(plat, plat), 3, "garder", None),
        "vendre_fin": (serie(plat, (100, 101, 99, 100.3)), 3, "vendre", ("HORIZON", "2026-01-03", 100.3, 100.3)),
    }
    obt, ok = {}, True
    for k, (s, h, fin, att) in cas.items():
        r = P.vendre(s, 1, dict(F, horizon=h), fin)
        o = None if r is None else (r["motif"], r["date_sortie"], r["px"],
                                    P.prix_de_convention(r["motif"], r["px"], r["objectif"], r["stop"]))
        obt[k] = o
        ok = ok and o == att
    d = (P.prix_de_convention("TP_GAP", 105.0, 104.0, 97.5), P.prix_de_convention("SL_GAP", 96.0, 104.0, 97.5),
         P.prix_de_convention("HORIZON", 100.7, 104.0, 97.5), P.prix_de_convention("TP", 104.0, 104.0, 97.5),
         P.prix_de_convention("SL", 97.5, 104.0, 97.5))
    ok = ok and d == (104.0, 97.5, 100.7, 104.0, 97.5)
    note("V8 valeurs connues, motif par motif : vendre et prix_de_convention (TP, TP_GAP, SL, SL_GAP, HORIZON, garder)", ok, (obt, d))
essai("V8", v8)

def v9():
    trouve = []
    for f in ("programmes/TENIR_LES_POSITIONS.py",):
        arbre = ast.parse(open(f, encoding="utf-8").read())
        for fn in ast.walk(arbre):
            if isinstance(fn, ast.FunctionDef) and not fn.name.startswith("_calibrage") and fn.name != "_tests":
                for n in ast.walk(fn):
                    if isinstance(n, ast.Call) and ((isinstance(n.func, ast.Attribute) and n.func.attr == "tester_seance")
                                                    or (isinstance(n.func, ast.Name) and n.func.id == "tester_seance")):
                        trouve.append((os.path.basename(f), fn.name, n.lineno))
    note("V9 R-708 : le soir n'appelle pas tester_seance", not trouve, trouve)
essai("V9", v9)
def v11():
    # le juge joue une fiche « aucune » : chaque opération sort sur un seuil ou à la fin des données, jamais à 20
    s = cours["ENGIE"]
    sig = B.SignalNomme(lambda x: [{"i": k} for k in range(0, len(x) - 1, 40)], {}, "epreuve A, V11")
    fiche = {"id": "A-V11", "tp": "+4%", "sl": "-3%", "horizon": "aucune", "univers": "ENGI", "entree": "DÉFAUT",
             "donnees_demandees": "cours", "periode": ""}
    mnemo = B.table_mnemoniques(glob.glob("donnees/REFERENTIEL_VALEURS_*.csv")[0])
    ops, _ = B.jouer(fiche, {"ENGIE": s}, mnemo, sig, P, bareme="HIST_FORFAIT_300")
    fins = sorted({o["motif"] for o in ops})
    derniere = s[-1]["date"]
    longs = [o for o in ops if o["motif"] == "HORIZON" and o["date_sortie"] != derniere]
    note("V11 le juge joue « aucune » : sorties sur seuil, ou HORIZON seulement a la fin des donnees",
         len(ops) > 10 and not longs and set(fins) <= {"TP", "SL", "TP_GAP", "SL_GAP", "HORIZON"},
         "%d op, motifs %s, HORIZON avant la fin %d" % (len(ops), fins, len(longs)))
essai("V11", v11)
def v12():
    s = cours["ENGIE"]
    sig = B.SignalNomme(lambda x: [{"i": k} for k in range(0, len(x) - 1, 40)], {}, "epreuve A, V12")
    fiche = {"id": "A-V12", "tp": "+4%", "sl": "-3%", "horizon": "aucune", "univers": "ENGI", "entree": "DÉFAUT",
             "donnees_demandees": "cours", "periode": ""}
    mnemo = B.table_mnemoniques(glob.glob("donnees/REFERENTIEL_VALEURS_*.csv")[0])
    ops, _ = B.jouer(fiche, {"ENGIE": s}, mnemo, sig, P, bareme="HIST_FORFAIT_300")
    import MODULE_JUGEMENT as J, io, contextlib
    S = importlib.util.module_from_spec(importlib.util.spec_from_file_location("st", sorted(glob.glob("programmes/MODULE_STATISTIQUES_*.py"))[-1]))
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            B.juger(fiche, ops, {"ENGIE": s}, {x["date"] for x in s}, J, S, P, mnemo, None, (sig,), None, "HIST_FORFAIT_300")
        o = "juge sans refus"
    except ValueError as e:
        o = "refus nomme" if str(e) == B.MOTIF_AUCUNE_NON_TRANCHEE else "autre refus : %s" % e
    note("V12 juger refuse une fiche « aucune » avec son motif nomme (embargo non tranche)", o == "refus nomme", o)
essai("V12", v12)

def v13():
    cal = ["2026-01-%02d" % d for d in range(1, 31)]
    op = lambda sig, ent, sor, m: {"date_signal": sig, "date_entree": ent, "date_sortie": sor, "motif": m}
    ops = [op("2026-01-01", "2026-01-02", "2026-01-05", "TP"),      # 3 seances, apprentissage : compte
           op("2026-01-02", "2026-01-03", "2026-01-30", "HORIZON"), # fin des donnees : exclue
           op("2026-01-21", "2026-01-22", "2026-01-29", "SL")]      # apres la frontiere (30 %) : exclue
    d = B.duree_d_embargo_sans_horizon(ops, cal, "2026-01-20")
    note("V13 embargo de « aucune » : ni les 30 %, ni la fin des donnees (3 seances attendues)", d == 3, d)
essai("V13", v13)
def v14():
    # N2 du relecteur neuf (tour 2) : un horizon illisible n'obtient pas de verdict de `juger`.
    s = cours["ENGIE"]
    sig = B.SignalNomme(lambda x: [{"i": k} for k in range(0, len(x) - 1, 40)], {}, "epreuve A, V14")
    base = {"id": "A-V14", "tp": "+4%", "sl": "-3%", "horizon": "20", "univers": "ENGI", "entree": "DÉFAUT",
            "donnees_demandees": "cours", "periode": ""}
    mnemo = B.table_mnemoniques(glob.glob("donnees/REFERENTIEL_VALEURS_*.csv")[0])
    ops, _ = B.jouer(base, {"ENGIE": s}, mnemo, sig, P, bareme="HIST_FORFAIT_300")
    import MODULE_JUGEMENT as J, io, contextlib
    S = importlib.util.module_from_spec(importlib.util.spec_from_file_location("st", sorted(glob.glob("programmes/MODULE_STATISTIQUES_*.py"))[-1]))
    o = []
    for hz in ("", None, 0, "0", "aucun", "sans", "-5", "inf"):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                B.juger(dict(base, horizon=hz), ops, {"ENGIE": s}, {x["date"] for x in s}, J, S, P, mnemo, None, (sig,), None, "HIST_FORFAIT_300")
            o.append((hz, "verdict rendu"))
        except ValueError as e:
            o.append((hz, "refus" if "horizon illisible" in str(e) else "autre : %s" % e))
    note("V14 juger refuse tout horizon illisible (\"\", None, 0, \"0\", aucun, sans, -5, inf)", len(ops) >= 5 and all(x[1] == "refus" for x in o), o)
essai("V14", v14)
print("RESULTATS " + json.dumps(res, ensure_ascii=False))
'''


def copie(sab):
    """Fabrique une copie sabotée : programmes copiés, donnees/temoins en liens sauf les fichiers écrits.

    ① RÔLE — isoler chaque épreuve. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — le nom du sabotage. ④ CONDITIONS
    D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — le dossier. [rend: 1] ⑥ TRAITEMENT — copier
    programmes/, lier les fichiers de donnees/ et temoins/ (copier ceux de ECRITS), appliquer le sabotage.
    ⑦ UNITÉ — — ⑧ POURQUOI — le dépôt fait 564 Mo ; une copie entière par sabotage coûterait des minutes. ⑨ CE QUI
    CLOCHE — voir ⑨ de l'en-tête. ⑩ EFFET — crée un dossier temporaire. ⑪ TERMINAISON — rend la main ou lève
    LookupError. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="vente_unique_")
    shutil.copytree(os.path.join(DEPOT, "programmes"), os.path.join(d, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    for rep in ("donnees", "temoins", "gouvernance"):
        os.makedirs(os.path.join(d, rep))
        for f in os.listdir(os.path.join(DEPOT, rep)):
            src = os.path.join(DEPOT, rep, f)
            if rep == "donnees" and f in ECRITS:
                shutil.copy(src, os.path.join(d, rep, f))
            else:
                os.symlink(src, os.path.join(d, rep, f))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            shutil.rmtree(d)
            raise LookupError("sabotage %s : texte visé présent %d fois dans %s" % (sab, t.count(a), f))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d


def run(d, *args):
    r = subprocess.run([sys.executable, "-B", *args], cwd=d, capture_output=True, text=True, timeout=900)
    return r.returncode, r.stdout + r.stderr


def bout_en_bout(d):
    """V10 : deux lancements du programme du soir sur la copie. Rend {nom: [vert, détail]}.

    ① RÔLE — éprouver le vrai chemin du soir. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — la copie. ④ CONDITIONS
    D'ENTRÉE — le registre de la copie est un fichier (ECRITS). ⑤ SORTIE — un dictionnaire de deux épreuves.
    [rend: 1] ⑥ TRAITEMENT — (a) registre sans VIVANTE, position Vinci en attente, séance du 07-06-2024 ; (b) registre
    où C5E10-OBS-V1 achète « CLOSE », signal VINCI, champ garde_du_soir. ⑦ UNITÉ — — ⑧ POURQUOI — voir l'en-tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — réécrit quatre fichiers de la copie. ⑪ TERMINAISON — borné à 900 s par lancement.
    [sort: non]
    """
    sys.path.insert(0, os.path.join(DEPOT, "programmes"))
    import CONTRATS_DES_FICHIERS as K
    sys.path.pop(0)
    res = {}
    f_reg = os.path.join(d, "donnees", "cac40_strategies.csv")
    origine = list(csv.DictReader(open(os.path.join(DEPOT, "donnees", "cac40_strategies.csv"), encoding="utf-8-sig")))
    champs = list(origine[0].keys())

    def ecrire(lignes, signaux, positions):
        with open(f_reg, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=champs); w.writeheader(); w.writerows(lignes)
        with open(os.path.join(d, "donnees", "signaux_du_jour.json"), "w", encoding="utf-8") as fh:
            json.dump(signaux, fh)
        with open(os.path.join(d, "donnees", "claude_positions_ouvertes.csv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(K.POSITION)); w.writeheader(); w.writerows(positions)
        with open(os.path.join(d, "donnees", "claude_journal_trades.csv"), "w", encoding="utf-8", newline="") as fh:
            csv.DictWriter(fh, fieldnames=list(K.TRADE)).writeheader()

    def lire(f):
        return list(csv.DictReader(open(os.path.join(d, "donnees", f), encoding="utf-8-sig")))

    attente = dict(strategie="C5E10-OBS-V1", valeur="VINCI", date_signal="2024-06-06", date_entree="",
                   prix_entree="EN_ATTENTE", tp="EN_ATTENTE", sl="EN_ATTENTE", horizon_fin="EN_ATTENTE",
                   statut="EN_ATTENTE_ENTREE", comptabilite="jetons_illimites", regles_pre_trade="", explication="epreuve")
    # (a) AUCUNE FICHE VIVANTE
    lignes = [dict(l, statut=(l.get("statut") or "").replace("VIVANTE", "FERMEE_EPREUVE")) for l in origine]
    ecrire(lignes, {"seance": "2024-06-07", "signaux": []}, [attente])
    c, o = run(d, TEN, d)
    j = lire("claude_journal_trades.csv")
    ok = c == 0 and [(x["valeur"], x["date_sortie"], x["motif_sortie"], x["prix_sortie"]) for x in j] == [
        ("VINCI", "2024-06-07", "SL", "110.76000")]
    res["V10a aucune fiche VIVANTE : code 0, la position Vinci est tenue et vendue au stop"] = [ok, "code %d · %s · %s" % (
        c, [(x["valeur"], x["date_sortie"], x["motif_sortie"], x["prix_sortie"]) for x in j], o.strip()[-160:])]
    # (b) FICHE REFUSÉE PAR LE JUGE, champ garde_du_soir
    lignes = [dict(l, entree="CLOSE") if l["id"] == "C5E10-OBS-V1" else l for l in origine]
    sig = {"seance": "2024-06-07", "garde_du_soir": {"refusees": ["C5E10-OBS-V1"]},
           "signaux": [{"valeur": "VINCI", "date_signal": "2024-06-07", "cmf": 0.01, "cci": -120.0, "close": 113.0}]}
    ecrire(lignes, sig, [])
    c, o = run(d, TEN, d)
    pos = lire("claude_positions_ouvertes.csv")
    ok = c == 0 and not pos and "FICHE C5E10-OBS-V1 REFUSEE PAR LE JUGE" in o
    res["V10b fiche refusee par le juge : aucun signal attribue, refus dit, code 0 (garde_du_soir ignore)"] = [
        ok, "code %d · %d position(s) · %s" % (c, len(pos), o.strip()[-200:])]
    # (c) JONCTION (RELU Cowork ab8fc49f, LC-1) : le DÉTECTEUR puis le TENEUR sur le même registre — l'univers de
    # C5E10-QA-V1 devient « TTE,ZZZ » (ZZZ absent du référentiel), le maître perd la séance du 10-11-2026 (signal
    # TOTALENERGIES du 09-11, mesuré par Cowork). Les fiches qui reçoivent un signal ⊆ les fiches suivies.
    f_m = os.path.join(d, "donnees", "cours_maitre.csv")
    lignes_m = open(os.path.join(DEPOT, "donnees", "cours_maitre.csv"), encoding="utf-8").read().splitlines(True)
    open(f_m, "w", encoding="utf-8").write("".join(l for l in lignes_m if ",2026-11-10," not in l))
    lignes = [dict(l, univers="TTE,ZZZ") if l["id"] == "C5E10-QA-V1" else l for l in origine]
    ecrire(lignes, {"seance": "2026-11-09", "signaux": []}, [])
    cd, od = run(d, "programmes/DETECTER_LES_SIGNAUX_GITHUB.py", ".")
    sj = json.load(open(os.path.join(d, "donnees", "signaux_du_jour.json"), encoding="utf-8"))
    c, o = run(d, TEN, d)
    pos = lire("claude_positions_ouvertes.csv")
    # un refus PARTIEL n'est pas écrit dans le fichier (garde_du_soir seulement quand la garde mord) : il se lit dans ce
    # que le détecteur affiche, « ⛔ GARDE DU SOIR — la fiche X n'est PAS suivie ».
    import re
    refusees = set(re.findall(r"⛔ GARDE DU SOIR — la fiche (\S+) n'est PAS suivie", od))
    vivantes = {l["id"] for l in lignes if "VIVANTE" in (l.get("statut") or "")}
    suivies = vivantes - refusees
    recoivent = {p["strategie"] for p in pos}
    ok = (cd == 0 and c == 0 and "C5E10-QA-V1" in refusees and bool(recoivent) and recoivent <= suivies
          and "C5E10-QA-V1" not in recoivent)
    res["V10c jonction detecteur puis teneur : les fiches qui recoivent un signal sont parmi les fiches suivies (TTE,ZZZ)"] = [
        ok, "detecteur %d, teneur %d, refusees %s, recoivent %s, %d position(s) · %s" % (
            cd, c, sorted(refusees), sorted(recoivent), len(pos), (od + o).strip()[-200:])]
    open(f_m, "w", encoding="utf-8").write("".join(lignes_m))
    return res


def epreuves(sab):
    d = copie(sab)
    try:
        c, o = run(d, "-c", CODE)
        ligne = [l for l in o.splitlines() if l.startswith("RESULTATS ")]
        res = json.loads(ligne[-1][10:]) if ligne else {"CODE": [False, o[-400:]]}
        res.update(bout_en_bout(d))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return res


def main():
    choix = list(SABOTAGES) if "--saboter" in sys.argv else (["Z0"] + _args[1:2] if len(_args) > 1 else ["Z0"])
    code = 0
    for sab in choix:
        try:
            res = epreuves(sab)
        except LookupError as e:
            print("ARRET : %s" % e)
            return 2
        rouges = [k for k, v in res.items() if not v[0]]
        print("== %s : %d vertes, %d rouges%s" % (sab, len(res) - len(rouges), len(rouges),
                                                 "  <-- ATTENDU : 0 rouge" if sab == "Z0" and rouges else ""))
        for k in rouges:
            print("     ROUGE %s · %s" % (k, res[k][1]))
        if (sab == "Z0") == bool(rouges):
            code = 1
            if sab != "Z0":
                print("     NE MORD PAS")
    print("CODE %d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())
