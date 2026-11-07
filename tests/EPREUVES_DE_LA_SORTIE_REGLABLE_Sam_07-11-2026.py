#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_SORTIE_REGLABLE — Sam 07-11-2026 (Paris) — lot ①a de J1 : UNE SEULE FONCTION DE VENTE POUR LE JUGE.
Simulation uniquement — aucun ordre réel, jamais.

À QUOI ÇA SERT. Le 07-11-2026, la boucle qui décide une vente dans le juge des stratégies
(`programmes/JUGE_DES_STRATEGIES.py`, `jouer_une_entree`) est partie, sans changement, dans
`programmes/MODULE_POSITIONS.py`, fonction `vendre`. Raison : deux implémentations d'une même chose divergent
toujours (R-708) ; la conception J1 du 07-11-2026 a relevé quatre boucles de vente, qui divergent déjà. Le
superviseur R-759 du même jour a jugé la conception « de fond, à découper », et le premier lot (①a) « sans rien
de neuf » : il se prouve entièrement par une égalité. Ce fichier garde cette égalité au dépôt, et prouve que
chaque épreuve a des dents (R-731) : chaque sabotage retire ou décale une protection, et au moins une épreuve
doit rougir.

CE QUI EST ÉPROUVÉ (E1 à E12) :
  E1 les quatre cas fabriqués de la conception (§1.4), joués par le juge ET par `vendre` : les mêmes sorties
     qu'avant le lot, mesurées sur `main` 95666ac3 le 07-11-2026.
  E2 TOUTES les entrées possibles du témoin du golden (chaque valeur, chaque séance, quatre réglages
     objectif/stop/échéance), jouées par le juge : empreinte figée, mesurée sur `main` 95666ac3.
  E3 les 100 opérations de l'étalon (fiche de calibrage de C5, barème réel et forfait de 300 €) : empreintes
     complètes figées `788dc3a04cddc988` et `484bfe7935a44017` (valeur, dates, motif, prix, net).
  E4 vraies lignes : VINCI acheté le 07-06-2024 (vendu au stop le jour même), AIRBUS le 21-02-2024 (objectif),
     VEOLIA le 17-01-2025 (échéance), lues dans le tableau des 100 trades ; ENGIE acheté le 17-06-2024 à 13,25
     (témoin, l. 8490 : plus haut 13,78 le 21-06, objectif brut 13,780000000000001, vendu le 24-06).
  E5 refus : `fin_des_donnees` autre que "vendre" lève ValueError ; un module des positions sans `vendre`
     arrête le juge (RuntimeError), sans copie de repli.
  E6 une séance qui touche stop et objectif sans saut : le stop (R-602) ; qui ouvre au-dessus de l'objectif
     puis passe sous le stop : l'objectif à l'ouverture (R-607 ③) ; un plus bas ÉGAL au stop, un plus haut ÉGAL à
     l'objectif : vendu (la comparaison inclut l'égalité).
  E7 fin des données : achat sur la dernière séance sans seuil touché → rien ; trois séances après l'achat
     et rien touché → vendu à la dernière clôture, motif HORIZON (comportement gardé tel quel au lot ①a).
  E8 propriété R-708, par l'arbre syntaxique : `jouer_une_entree` ne contient aucune boucle (une vente se
     déroule séance par séance : sans boucle, elle ne peut pas y vivre).
  E9 propriété R-708, par le comportement : avec un `vendre` qui rend une vente sentinelle et un
     `tester_seance` qui lève, le juge rend la sentinelle, pour chaque séance d'achat d'ENGIE.
  E10 une clé absente de la pièce `vente` lève KeyError (jamais de valeur par défaut).
  E11 une séance sans l'un de ses prix lève KeyError, par `vendre` et par le juge.
  E12 propriété R-708, par l'arbre syntaxique : aucune fonction du juge n'appelle `tester_seance`.
  (E8 à E11 depuis le tour 2, après la relecture du 07-11-2026 : l'ancienne E8 cherchait le NOM `tester_seance`,
  et trois sabotages, N1, N4 et N12, restaient verts. E12 depuis le tour 3 : le tour 2 avait retiré l'ancienne
  E8 au lieu de lui ajouter la nouvelle, et deux sabotages de la seconde relecture, R1 et R2, restaient verts.)

USAGE : python3 -B tests/EPREUVES_DE_LA_SORTIE_REGLABLE_Sam_07-11-2026.py <racine du dépôt> [--saboter | nom]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Chaque épreuve travaille sur une COPIE temporaire ; le dépôt n'est jamais touché.
Sous `--saboter`, chaque ligne dit aussi si l'empreinte des 100 opérations (E3) a rougi : un sabotage qui ne
touche aucune des 100 la laisse verte, et c'est E2 ou un cas fabriqué qui le voit.
"""
import json, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MODP, BAN = "programmes/MODULE_POSITIONS.py", "programmes/JUGE_DES_STRATEGIES.py"

# Les valeurs figées, mesurées sur `main` 95666ac3 le 07-11-2026 (sorties du lot ①a, J1a/sorties/) AVANT le lot.
FIGE_E2 = "96049b1558e218a3"   # 100 444 entrées (4 réglages × 25 111 séances du témoin)
FIGE_E3 = {"REEL": "788dc3a04cddc988", "HIST_FORFAIT_300": "484bfe7935a44017"}
FIGE_E1 = {"A": ["TP_GAP", "2026-01-03", 105], "B": ["SL", "2026-01-02", 97.5],
           "C": ["HORIZON", "2026-01-07", 100], "D": ["HORIZON", "2026-01-22", 100.5]}

SABOTAGES = {
    "Z0": [],
    # dans `vendre`
    "S1_echeance_un_cran_trop_tot": [(MODP, "    suite = serie[j:j + 1 + h]", "    suite = serie[j:j + h]")],
    "S2_seance_d_achat_sautee": [(MODP, "    suite = serie[j:j + 1 + h]", "    suite = serie[j + 1:j + 1 + h]")],
    "S3_achat_a_l_ouverture_de_la_veille": [(MODP, '    pe = serie[j]["open"]\n    tp_abs', '    pe = serie[j - 1]["open"]\n    tp_abs')],
    "S4_echeance_vendue_a_l_ouverture": [(MODP, 'px, motif, d_sortie = apres[-1]["close"], "HORIZON"',
                                          'px, motif, d_sortie = apres[-1]["open"], "HORIZON"')],
    "S5_vendu_au_seuil_meme_sur_un_saut": [(MODP, "            px, motif = r\n            d_sortie = b[\"date\"]",
                                            "            px, motif = (tp_abs if r[1].startswith(\"TP\") else sl_abs), r[1]\n"
                                            "            d_sortie = b[\"date\"]")],
    "S6_seuils_arrondis": [(MODP, "    tp_abs, sl_abs = pe * (1 + tp), pe * (1 - sl)\n    # LA SEANCE",
                            "    tp_abs, sl_abs = round(pe * (1 + tp), 5), round(pe * (1 - sl), 5)\n    # LA SEANCE")],
    "S7_fin_des_donnees_vendue_le_jour_d_achat": [(MODP, "        if not apres:\n            return None\n        px, motif, d_sortie",
                                                   "        apres = apres or suite\n        px, motif, d_sortie")],
    "S8_garder_accepte_en_silence": [(MODP, '    if fin_des_donnees != "vendre":\n        raise',
                                      '    if fin_des_donnees not in ("vendre", "garder"):\n        raise')],
    # dans `tester_seance`, qu'elle emploie (ordre et comparaisons)
    "S9_stop_compare_un_cran_trop_strict": [(MODP, '    if bar["low"] <= sl:\n        return sl, "SL"',
                                             '    if bar["low"] < sl:\n        return sl, "SL"')],
    "S10_objectif_compare_un_cran_trop_strict": [(MODP, '    if bar["high"] >= tp:\n        return tp, "TP"',
                                                  '    if bar["high"] > tp:\n        return tp, "TP"')],
    "S11_objectif_teste_avant_le_stop": [(MODP, '    if bar["low"] <= sl:\n        return sl, "SL"\n    if bar["high"] >= tp:\n        return tp, "TP"',
                                          '    if bar["high"] >= tp:\n        return tp, "TP"\n    if bar["low"] <= sl:\n        return sl, "SL"')],
    # dans le juge, qui l'appelle
    "S12_juge_passe_une_echeance_decalee": [(BAN, '{"tp": tp, "sl": sl, "horizon": h}, "vendre")', '{"tp": tp, "sl": sl, "horizon": h + 1}, "vendre")')],
    "S13_juge_inverse_objectif_et_stop": [(BAN, '{"tp": tp, "sl": sl, "horizon": h}, "vendre")', '{"tp": sl, "sl": tp, "horizon": h}, "vendre")')],
    "S14_juge_recopie_la_boucle": [(BAN, '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n',
                                    '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n'
                                    '    for _b in serie[j:j + 1 + h]:\n'
                                    '        if mod_positions.tester_seance(_b, serie[j]["open"] * (1 + tp), serie[j]["open"] * (1 - sl)):\n'
                                    '            break\n')],
    "S15_juge_repli_sans_vendre": [(BAN, '    if not callable(_vendre):\n        raise RuntimeError(',
                                    '    if not callable(_vendre):\n        _vendre = lambda *a: None\n    if False:\n        raise RuntimeError(')],
    # les trois sabotages de la relecture du 07-11-2026 (tour 1) que les épreuves du tour 1 ne voyaient pas
    "N1_juge_recopie_vendre_sans_nommer_tester_seance": [(BAN,
        '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n',
        '    _t = getattr(mod_positions, "tester_seance")\n'
        '    def _vendre_local(serie, j, vente, fin):\n'
        '        pe = serie[j]["open"]\n'
        '        ta, sa = pe * (1 + vente["tp"]), pe * (1 - vente["sl"])\n'
        '        suite = serie[j:j + 1 + vente["horizon"]]\n'
        '        for b in suite:\n'
        '            r = _t(b, ta, sa)\n'
        '            if r:\n'
        '                return {"pe": pe, "px": r[0], "motif": r[1], "date_sortie": b["date"]}\n'
        '        apres = suite[1:]\n'
        '        if not apres:\n'
        '            return None\n'
        '        return {"pe": pe, "px": apres[-1]["close"], "motif": "HORIZON", "date_sortie": apres[-1]["date"]}\n'
        '    _vente = _vendre_local(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n')],
    "N4_vendre_remplace_une_cle_absente_par_un_defaut": [(MODP,
        '    tp, sl, h = vente["tp"], vente["sl"], vente["horizon"]',
        '    tp, sl, h = vente.get("tp", 0.04), vente.get("sl", 0.025), vente.get("horizon", 20)')],
    "N12_vendre_avale_une_seance_incomplete": [(MODP,
        '        r = tester_seance(b, tp_abs, sl_abs)\n',
        '        try:\n            r = tester_seance(b, tp_abs, sl_abs)\n        except KeyError:\n            r = None\n')],
    # les deux sabotages de la seconde relecture du 07-11-2026 (tour 2) que E8 et E9 laissaient passer
    'R1_boucle_dans_une_fonction_du_module_filtre_sur_le_motif': [(BAN, 'def jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture=None, bareme=None):', 'def _r1_vente_du_juge(serie, j, tp, sl, h, mp):\n    pe = serie[j]["open"]\n    ta, sa = pe * (1 + tp), pe * (1 - sl)\n    suite = serie[j:j + 1 + h]\n    for b in suite:\n        r = mp.tester_seance(b, ta, sa)\n        if r:\n            return {"pe": pe, "px": r[0], "motif": r[1], "date_sortie": b["date"]}\n    apres = suite[1:]\n    if not apres:\n        return None\n    return {"pe": pe, "px": apres[-1]["close"], "motif": "HORIZON", "date_sortie": apres[-1]["date"]}\n\n\ndef jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture=None, bareme=None):'), (BAN, '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n', '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n    if _vente is not None and _vente["motif"] in ("TP", "SL", "TP_GAP", "SL_GAP", "HORIZON"):\n        _vente = _r1_vente_du_juge(serie, j, tp, sl, h, mod_positions)\n')],
    'R2_next_filter_dans_le_juge_filtre_sur_le_motif': [(BAN, '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n', '    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")\n    if _vente is not None and _vente["motif"] in ("TP", "SL", "TP_GAP", "SL_GAP", "HORIZON"):\n        _pe = serie[j]["open"]; _ta, _sa = _pe * (1 + tp), _pe * (1 - sl)\n        _b = next(filter(lambda x: mod_positions.tester_seance(x, _ta, _sa), serie[j:j + 1 + h]), None)\n        if _b is not None:\n            _r = mod_positions.tester_seance(_b, _ta, _sa)\n            _vente = {"pe": _pe, "px": _r[0], "motif": _r[1], "date_sortie": _b["date"]}\n')],
}

# Le code joué DANS la copie, en sous-processus (modules de la copie, jamais ceux du dépôt). Il imprime un
# dictionnaire JSON : épreuve -> [vert ?, détail].
CODE = r'''
import sys, os, json, glob, hashlib, types, ast, csv
sys.path.insert(0, "programmes")
import MODULE_POSITIONS as P, JUGE_DES_STRATEGIES as B
FIGE_E1, FIGE_E2, FIGE_E3 = json.loads(sys.argv[1]), sys.argv[2], json.loads(sys.argv[3])
res = {}
def note(nom, ok, det):
    res[nom] = [bool(ok), str(det)[:300]]
def essai(nom, f):
    try:
        f()
    except Exception as e:
        note(nom, False, "leve %s : %s" % (type(e).__name__, e))
HIST = "HIST_FORFAIT_300"
f_tem = glob.glob("temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN*.csv")[0]
cours = B.charger_cours(f_tem)

def b(d, o, h, l, c):
    return {"date": "2026-01-%02d" % d, "open": o, "high": h, "low": l, "close": c, "volume": 1000}
CAS = {
    "A": [b(1, 100, 100, 100, 100), b(2, 100, 101, 99, 100), b(3, 105, 105, 96, 97)] + [b(4 + i, 100, 101, 99, 100) for i in range(25)],
    "B": [b(1, 100, 100, 100, 100), b(2, 100, 101, 97, 99)] + [b(3 + i, 100, 101, 99, 100) for i in range(25)],
    "C": [b(1, 100, 100, 100, 100)] + [b(2 + i, 100, 101, 99, 100) for i in range(6)],
    "D": [b(1, 100, 100, 100, 100)] + [b(2 + i, 100, 101, 99, 100.5) for i in range(26)],
}
def e1():
    obt, ok = {}, True
    for k, s in CAS.items():
        op = B.jouer_une_entree("AIRBUS", s, 1, 0.04, 0.025, 20, P, None, HIST)
        vd = P.vendre(s, 1, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre")
        a = [op["motif"], op["date_sortie"], round(op["px"], 4)]
        w = [vd["motif"], vd["date_sortie"], round(vd["px"], 4)]
        obt[k] = (a, w)
        ok = ok and a == FIGE_E1[k] and w == FIGE_E1[k] and vd["pe"] == op["pe"]
    note("E1 cas A a D : le juge et vendre rendent les sorties d'avant", ok, obt)
essai("E1 cas A a D : le juge et vendre rendent les sorties d'avant", e1)

def e2():
    t = []
    for reg in ((0.04, 0.025, 20), (0.02, 0.01, 5), (0.10, 0.05, 1), (0.03, 0.03, 40)):
        for v in sorted(cours):
            s = cours[v]
            for j in range(len(s)):
                o = B.jouer_une_entree(v, s, j, reg[0], reg[1], reg[2], P, None, HIST)
                t.append((reg, v, j) + ((None,) if o is None else
                         (repr(o["pe"]), repr(o["px"]), o["motif"], o["date_sortie"], repr(o["net"]), repr(o["frais"]), o["date_entree"])))
    e = hashlib.sha256(repr(t).encode()).hexdigest()[:16]
    note("E2 toutes les entrees du temoin, quatre reglages : empreinte d'avant", e == FIGE_E2, "%d entrees, empreinte %s, figee %s" % (len(t), e, FIGE_E2))
essai("E2 toutes les entrees du temoin, quatre reglages : empreinte d'avant", e2)

def e3():
    mnemo = B.table_mnemoniques(glob.glob("donnees/REFERENTIEL_VALEURS_*.csv")[0])
    sig = B.signal_de_la_fiche(".", dict(B.SIGNAL_DU_CALIBRAGE, id="calibrage"))
    fiche = {"tp": "+4.0%", "sl": "-2.5%", "horizon": "20", "entree": "Open J+1", "donnees_demandees": "cours",
             "univers": ",".join(getattr(sig.module, "C5E10_UNIVERS", [])), "indicateurs": "calibrage",
             "periode": min(min(x["date"] for x in s) for s in cours.values()) + " -> 2026-07-10"}
    fiche.update(B.SIGNAL_DU_CALIBRAGE)
    ok0, manq, bornes = B.porte_0(fiche)
    det, ok = {}, ok0
    for bar in ("REEL", "HIST_FORFAIT_300"):
        ops, _ = B.jouer(fiche, cours, mnemo, sig, P, periode=bornes, bareme=bar)
        t = sorted((o["valeur"], o["date_signal"], o["date_entree"], o["date_sortie"], o["motif"], "%.6f" % o["pe"], "%.6f" % o["px"], "%.2f" % o["net"]) for o in ops)
        e = hashlib.sha256(repr(t).encode()).hexdigest()[:16]
        det[bar] = (len(t), e)
        ok = ok and len(t) == 100 and e == FIGE_E3[bar]
    note("E3 les 100 operations de l'etalon : empreintes completes d'avant", ok, det)
essai("E3 les 100 operations de l'etalon : empreintes completes d'avant", e3)

def e4():
    f_tab = glob.glob("donnees/TABLEAU_100_TRADES_C5E10_*.csv")[0]
    lignes = list(csv.DictReader(open(f_tab, encoding="utf-8-sig"), delimiter=";"))
    det, ok = [], True
    for v, d_ent in (("VINCI", "2024-06-07"), ("AIRBUS", "2024-02-21"), ("VEOLIA", "2025-01-17")):
        r = [x for x in lignes if x["valeur"] == v and x["date_entree"] == d_ent]
        s = cours[v]; j = [k for k, x in enumerate(s) if x["date"] == d_ent]
        if len(r) != 1 or len(j) != 1:
            ok = False; det.append((v, d_ent, "ligne ou seance introuvable", len(r), len(j))); continue
        op = B.jouer_une_entree(v, s, j[0], 0.04, 0.025, 20, P, None, HIST)
        attendu = (r[0]["motif"], r[0]["date_sortie"], round(float(r[0]["prix_sortie"].replace(",", ".")), 4))
        obtenu = (op["motif"], op["date_sortie"], round(op["px"], 4))
        ok = ok and attendu == obtenu; det.append((v, d_ent, obtenu, attendu))
    s = cours["ENGIE"]; j = [k for k, x in enumerate(s) if x["date"] == "2024-06-17"][0]
    op = B.jouer_une_entree("ENGIE", s, j, 0.04, 0.025, 20, P, None, HIST)
    obtenu = (op["pe"], op["motif"], op["date_sortie"], repr(op["px"]))
    ok = ok and obtenu == (13.25, "TP", "2024-06-24", "13.780000000000001"); det.append(("ENGIE", obtenu))
    note("E4 vraies lignes : Vinci, Airbus, Veolia du tableau ; Engie du temoin", ok, det)
essai("E4 vraies lignes : Vinci, Airbus, Veolia du tableau ; Engie du temoin", e4)

def e5():
    s = CAS["D"]
    try:
        P.vendre(s, 1, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "garder"); a = "rien leve"
    except ValueError:
        a = "ValueError"
    faux = types.SimpleNamespace(**{n: getattr(P, n) for n in dir(P) if not n.startswith("__") and n != "vendre"})
    try:
        B.jouer_une_entree("AIRBUS", s, 1, 0.04, 0.025, 20, faux, None, HIST); c = "rien leve"
    except RuntimeError as e:
        c = "RuntimeError" if "vendre" in str(e) else "RuntimeError sans le mot vendre"
    note("E5 refus : garder leve, module sans vendre arrete le juge", (a, c) == ("ValueError", "RuntimeError"), (a, c))
essai("E5 refus : garder leve, module sans vendre arrete le juge", e5)

def e6():
    s1 = [b(1, 100, 100, 100, 100), b(2, 100, 104.5, 97.0, 100)] + [b(3 + i, 100, 101, 99, 100) for i in range(25)]
    s2 = [b(1, 100, 100, 100, 100), b(2, 100, 101, 99, 100), b(3, 104.2, 104.5, 97.0, 98)] + [b(4 + i, 100, 101, 99, 100) for i in range(25)]
    v = {"tp": 0.04, "sl": 0.025, "horizon": 20}
    # un seuil touché TOUT JUSTE compte (« plus bas <= stop », « plus haut >= objectif ») : le plus bas égal au stop,
    # puis le plus haut égal à l'objectif, chacun calculé comme le juge le calcule (prix × (1 ∓ seuil))
    s3 = [b(1, 100, 100, 100, 100), b(2, 100, 101, 100 * (1 - 0.025), 100)] + [b(3 + i, 100, 101, 99, 100) for i in range(25)]
    s4 = [b(1, 100, 100, 100, 100), b(2, 100, 100 * (1 + 0.04), 99, 100)] + [b(3 + i, 100, 101, 99, 100) for i in range(25)]
    r1, r2, r3, r4 = (P.vendre(x, 1, v, "vendre") for x in (s1, s2, s3, s4))
    o = tuple((r["motif"], r["date_sortie"]) for r in (r1, r2, r3, r4)) + ((r1["px"], r2["px"]),)
    note("E6 les deux seuils dans la meme seance : stop sans saut, objectif a l'ouverture sur un saut ; seuil tout juste touche",
         o == (("SL", "2026-01-02"), ("TP_GAP", "2026-01-03"), ("SL", "2026-01-02"), ("TP", "2026-01-02"), (97.5, 104.2)), o)
essai("E6 les deux seuils dans la meme seance : stop sans saut, objectif a l'ouverture sur un saut", e6)

def e7():
    v = {"tp": 0.04, "sl": 0.025, "horizon": 20}
    s = [b(1, 100, 100, 100, 100), b(2, 100, 101, 99, 100), b(3, 100, 101, 99, 100), b(4, 100, 101, 99, 100.25), b(5, 100, 101, 99, 100.75)]
    r_der = P.vendre(s, 4, v, "vendre")
    r_3 = P.vendre(s, 1, v, "vendre")
    o = (r_der, None if r_3 is None else (r_3["motif"], r_3["date_sortie"], r_3["px"]))
    note("E7 fin des donnees : rien sur la derniere seance, HORIZON a la derniere cloture sinon",
         o == (None, ("HORIZON", "2026-01-05", 100.75)), o)
essai("E7 fin des donnees : rien sur la derniere seance, HORIZON a la derniere cloture sinon", e7)

# E8 et E9 : LA VENTE DU JUGE VIENT DE `vendre`, ET DE RIEN D'AUTRE (R-708). Une PROPRIÉTÉ, pas un nom : la
# relecture du 07-11-2026 (tour 1, N1) a recopié la boucle dans le juge en appelant `tester_seance` sous un autre
# nom, et l'ancienne E8, qui cherchait ce nom, est restée verte.
def e8():
    # E8 — par l'arbre syntaxique : `jouer_une_entree`, fonctions imbriquées comprises, ne contient AUCUNE boucle
    # (for, while, compréhension). Elle ne suffit pas seule : une vente recopiée peut se passer de boucle
    # syntaxique (`next(filter(...))`, R2) ou vivre dans une autre fonction du module (R1) — relecture du
    # 07-11-2026, tour 2. E12 (aucun appel à `tester_seance` dans le juge) et E9 la complètent.
    arbre = ast.parse(open("programmes/JUGE_DES_STRATEGIES.py", encoding="utf-8").read())
    fns = [fn for fn in ast.walk(arbre) if isinstance(fn, ast.FunctionDef) and fn.name == "jouer_une_entree"]
    boucles = sorted({(type(n).__name__, n.lineno) for fn in fns for n in ast.walk(fn)
                      if isinstance(n, (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp))})
    note("E8 R-708 : jouer_une_entree ne contient aucune boucle (arbre syntaxique)", len(fns) == 1 and not boucles,
         "%d fonction(s) trouvee(s) · boucles : %s" % (len(fns), boucles))
essai("E8 R-708 : jouer_une_entree ne contient aucune boucle (arbre syntaxique)", e8)

def e9():
    # E9 — par le comportement : un module des positions dont `vendre` rend une vente SENTINELLE et dont
    # `tester_seance` lève. Le juge doit rendre exactement la sentinelle, pour chaque séance d'achat d'une vraie
    # série (ENGIE, témoin) : s'il décidait la vente ailleurs, il rendrait autre chose ou lèverait.
    def sentinelle(serie, j, vente, fin):
        return {"pe": serie[j]["open"], "px": round(serie[j]["open"] * 1.01234, 4), "motif": "SENTINELLE",
                "date_sortie": serie[min(j + 2, len(serie) - 1)]["date"]}
    def interdit(*a, **k):
        raise AssertionError("le juge a appele tester_seance")
    faux = types.SimpleNamespace(**{n: getattr(P, n) for n in dir(P) if not n.startswith("__")})
    faux.vendre, faux.tester_seance = sentinelle, interdit
    s = cours["ENGIE"]; ecarts = []
    for j in range(len(s)):
        op = B.jouer_une_entree("ENGIE", s, j, 0.04, 0.025, 20, faux, None, HIST)
        att = sentinelle(s, j, None, None)
        if op is None or (op["pe"], op["px"], op["motif"], op["date_sortie"]) != (att["pe"], att["px"], att["motif"], att["date_sortie"]):
            ecarts.append((j, None if op is None else op["motif"]))
    note("E9 R-708 : la vente du juge est celle que rend vendre, tester_seance interdit", not ecarts,
         "%d seances d'achat · ecarts %s" % (len(s), ecarts[:5]))
essai("E9 R-708 : la vente du juge est celle que rend vendre, tester_seance interdit", e9)

def e10():
    # E10 — une clé absente de `vente` lève KeyError (fiche de `vendre`, ⑪) : jamais de valeur par défaut, qui
    # jouerait en silence « +4 % / −2,5 % / 20 » pour une fiche qui dit autre chose (relecture, tour 1, N4).
    s = CAS["D"]; obt = []
    for cle in ("tp", "sl", "horizon"):
        v = {"tp": 0.04, "sl": 0.025, "horizon": 20}; del v[cle]
        try:
            P.vendre(s, 1, v, "vendre"); obt.append((cle, "rien leve"))
        except KeyError:
            obt.append((cle, "KeyError"))
    note("E10 une cle absente de vente leve KeyError", all(x[1] == "KeyError" for x in obt), obt)
essai("E10 une cle absente de vente leve KeyError", e10)

def e11():
    # E11 — une séance incomplète lève KeyError, par `vendre` et par le juge (fiche de `vendre`, ⑪) : une séance
    # sans plus bas avalée serait une séance où le stop n'est jamais testé (relecture, tour 1, N12).
    s = [dict(x) for x in CAS["D"]]; del s[3]["low"]
    obt = []
    for nom, f in (("vendre", lambda: P.vendre(s, 1, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre")),
                   ("juge", lambda: B.jouer_une_entree("AIRBUS", s, 1, 0.04, 0.025, 20, P, None, HIST))):
        try:
            f(); obt.append((nom, "rien leve"))
        except KeyError:
            obt.append((nom, "KeyError"))
    note("E11 une seance incomplete leve KeyError, par vendre et par le juge", obt == [("vendre", "KeyError"), ("juge", "KeyError")], obt)
essai("E11 une seance incomplete leve KeyError, par vendre et par le juge", e11)

def e12():
    # E12 — l'ancienne E8 du tour 1, remise : AUCUNE fonction du module du juge n'appelle `tester_seance`, ni
    # par son nom, ni comme attribut. Elle voit R1 et R2 (relecture du 07-11-2026, tour 2), que E8 et E9
    # laissent passer ; elle ne voit pas N1 (appel sous un autre nom), que E8 et E9 voient.
    arbre = ast.parse(open("programmes/JUGE_DES_STRATEGIES.py", encoding="utf-8").read())
    appels = sorted({(fn.name, n.lineno) for fn in ast.walk(arbre) if isinstance(fn, ast.FunctionDef)
                     for n in ast.walk(fn) if isinstance(n, ast.Call)
                     and ((isinstance(n.func, ast.Attribute) and n.func.attr == "tester_seance")
                          or (isinstance(n.func, ast.Name) and n.func.id == "tester_seance"))})
    note("E12 R-708 : aucune fonction du juge n'appelle tester_seance", not appels, appels)
essai("E12 R-708 : aucune fonction du juge n'appelle tester_seance", e12)
print("RESULTATS " + json.dumps(res, ensure_ascii=False))
'''


def copie(sab):
    """Copie le dépôt (sans .git) dans un dossier temporaire et y pose le sabotage `sab`.

    ① RÔLE — Donner à chaque jeu d'épreuves sa copie jetable, sabotée ou non.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par sabotage.
    ③ ENTRÉE — `sab` : un nom de `SABOTAGES`.
    ④ CONDITIONS D'ENTRÉE — Chaque texte visé figure UNE fois dans son fichier (sinon le sabotage ne saboterait rien).
    ⑤ SORTIE — UNE valeur : le chemin de la copie.
    ⑥ TRAITEMENT — copier, puis remplacer chaque texte visé, après avoir exigé qu'il y soit une seule fois.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sabotage dont la cible a disparu laisserait l'épreuve verte sans rien saboter.
    ⑨ CE QUI CLOCHE — La copie pèse le dépôt entier sans .git (environ 530 Mo le 07-11-2026) : une à la fois.
    ⑩ EFFET — Écrit un dossier temporaire.
    ⑪ TERMINAISON — Rend la main ; lève AssertionError si une cible n'est pas unique.
    """
    d = tempfile.mkdtemp(prefix="j1a_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, (sab, f, a[:60], t.count(a))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d


def epreuves(sab):
    """Joue E1 à E12 sur une copie sabotée par `sab`, et rend la liste (nom, vert, détail).

    ① RÔLE — Un jeu complet d'épreuves pour un sabotage.
    ② CONTEXTE D'APPEL — La partie principale, une fois par sabotage choisi.
    ③ ENTRÉE — `sab` : un nom de `SABOTAGES`.
    ④ CONDITIONS D'ENTRÉE — La copie porte le témoin du golden, le tableau des 100 trades et le référentiel.
    ⑤ SORTIE — UNE valeur : une liste de triplets (nom, vert, détail) ; un sous-processus qui n'imprime pas ses
      résultats donne UNE épreuve rouge « le code n'a pas tourné » (R-734).
    ⑥ TRAITEMENT — copier, lancer `CODE` dans la copie en sous-processus, lire la ligne RESULTATS, effacer la copie.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les modules de la COPIE sont chargés neufs dans un processus à part : un sabotage ne peut pas
      être masqué par un module déjà chargé.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit puis efface un dossier temporaire.
    ⑪ TERMINAISON — Rend la main.
    """
    d = copie(sab)
    try:
        r = subprocess.run([sys.executable, "-B", "-c", CODE, json.dumps(FIGE_E1), FIGE_E2, json.dumps(FIGE_E3)],
                           cwd=d, capture_output=True, text=True)
        ligne = [x for x in r.stdout.splitlines() if x.startswith("RESULTATS ")]
        if not ligne:
            return [("le code des epreuves n'a pas tourne", False, (r.stdout + r.stderr)[-400:])]
        return [(k, v[0], v[1]) for k, v in json.loads(ligne[-1][len("RESULTATS "):]).items()]
    finally:
        shutil.rmtree(d, ignore_errors=True)


_choix = (list(SABOTAGES) if "--saboter" in sys.argv else [_args[1]] if len(_args) > 1 else ["Z0"])
_faute = False
for sab in _choix:
    r = epreuves(sab)
    rouges = [x for x in r if not x[1]]
    vert = sab == "Z0"
    e3 = [x for x in r if x[0].startswith("E3")]
    print(f"== {sab} : {len(r) - len(rouges)} vertes, {len(rouges)} rouges · empreinte des 100 (E3) : "
          + ("rouge" if e3 and not e3[0][1] else "verte" if e3 else "absente")
          + ("  <-- ATTENDU : 0 rouge" if vert and rouges else "  <-- SABOTAGE NON VU" if not vert and not rouges else ""))
    for nom, ok, det in r:
        if not ok:
            print(f"     ROUGE {nom} · {det}")
    _faute = _faute or (vert and bool(rouges)) or (not vert and not rouges)
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
