#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DE L'ÉTALON DANS L'INDICE — Mer 28-10-2026 (Paris)

Simulation uniquement — aucun ordre réel.

① RÔLE — Prouver que l'étalon de hasard (`programmes/MODULE_JUGEMENT.py`, `etalon_hasard`) ne tire que des achats que
  la stratégie aurait pu faire — dans le CAC 40 le jour de l'achat, dans la période de la fiche — et qu'il les joue
  avec la mécanique même de la stratégie (`programmes/JUGE_DES_STRATEGIES.py`, `jouer_une_entree` et `achat_admis`).
② CONTEXTE D APPEL — Depuis la racine, la racine en argument : par le certificateur et à la main, avant toute
  livraison qui touche `etalon_hasard`, `jouer`, `jouer_une_entree` ou `achat_admis`. Avec `--saboter`, chaque
  sabotage doit faire rougir au moins une épreuve.
③ ENTRÉE — `sys.argv[1]` : la racine du dépôt ; `--saboter`, facultatif.
④ CONDITIONS D ENTRÉE — La racine porte les deux programmes, `donnees/cours_maitre.csv`, le référentiel et le registre
  des stratégies avec la fiche C5E10-QA-V1. Sinon l'épreuve E2 rougit.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si Z0 est vert et, avec `--saboter`, si chaque sabotage rougit ; 1 sinon.
  [rend: 1] Une ligne « == » par jeu, puis une ligne par épreuve rouge.
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : copier le dépôt, appliquer le sabotage, lancer les épreuves E1 à E6 dans un
  sous-processus, compter les rouges.
  E1 cas fabriqué : deux valeurs, B hors de l'indice tout le temps ; aucun achat tiré sur B, en mode « valeur ».
  E2 cas réel C5E10-QA-V1 sur le maître : l'ancienne règle de candidature retrouve le cas connu du relecteur du 27-10-2026
     (306 achats possibles, dont 42 hors de l'indice) ; le nouvel étalon en tire 0 hors de l'indice, 0 hors de la période.
  E3 un trou juste après le signal : avec un seul achat possible, le gain du hasard est EXACTEMENT celui de la stratégie.
  E4 mode « date » sur une période bornée : aucun signal tiré hors de la période.
  E5 mode « date » : la valeur réelle est gardée.
  E6 sans la mécanique de la stratégie, l'étalon refuse (il ne garde pas de copie).
  E7 et E7b le nombre joué par tirage dit vrai · E11 le branchement de production, par le vrai `juger` · E8 une lecture sans composition ne filtre pas · E9 les dernières séances
  restent tirables · E10 sans lecture, mode « valeur » : mêmes chiffres que l'ancien étalon, figés une fois.
  Le cas connu de E2 (306 achats, dont 42 hors de l'indice) est RECALCULÉ à chaque lancement par l'ancienne règle de
  candidature, réécrite dans l'épreuve pour la seule mesure.
⑦ UNITÉ — —
⑧ POURQUOI — Le 27-10-2026, le relecteur a mesuré que l'étalon tirait hors de l'indice (42 achats sur 306) ; décision de
  Jean-Luc du 28-10-2026 à 23h03 : réparer tout de suite ; le superviseur R-759 a exigé une seule mécanique (R-708).
⑨ CE QUI CLOCHE — E2 dépend du fichier maître : s'il grandit, le compte du cas connu peut changer ; il est donc lu sur la
  période de la fiche, figée.
⑩ EFFET — Des copies temporaires du dépôt, effacées à la fin.
⑪ TERMINAISON — Chaque sous-processus est borné à 600 secondes.
  [sort: oui]
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
JUG = "programmes/MODULE_JUGEMENT.py"
BAN = "programmes/JUGE_DES_STRATEGIES.py"
SABOTAGES = {
    "Z0": [],
    "S1_l_etalon_ignore_l_indice": [(JUG, "            if not admis(v, j):\n                continue\n", "            pass\n")],
    "S2_l_etalon_ignore_la_periode": [(JUG, "            if periode and not (periode[0] <= d_sig <= periode[1]):\n                continue\n            if not admis",
                                       "            if False:\n                continue\n            if not admis")],
    "S3_l_etalon_achete_un_jour_trop_tard": [(JUG, "            op = entree(v, j)\n", "            op = entree(v, j + 1) if j + 1 < len(cours[v]) else None\n")],
    "S4_le_mode_date_tire_la_valeur": [(JUG, "                v = o[\"valeur\"]\n", "                v = dispo[r.randrange(len(dispo))]\n")],
    "S5_la_regle_d_achat_ignore_l_indice": [(BAN, "    if lecture is None or not lecture.get(\"composition\"):\n        return True",
                                             "    if True:\n        return True")],
    "S6_l_etalon_garde_une_copie": [(JUG, "    if entree is None or admis is None:\n        raise ValueError(",
                                     "    if False:\n        raise ValueError(")],
    # S7 à S9 (29-10-2026, relecture et superviseur R-759 du 28-10-2026) : les exigences que rien ne gardait
    "S7_l_effectif_joue_ment": [(JUG, "            joues.append(n)\n", "            joues.append(len(ops))\n")],
    "S8_les_dernieres_seances_jamais_tirees": [(JUG, "        for j in range(1, len(s)):\n", "        for j in range(1, len(s) - horizon - 2):\n")],
    "S9_une_composition_fausse_filtre_quand_meme": [(BAN, '    if lecture is None or not lecture.get("composition"):', '    if lecture is None:')],
    # S10 et S11 (29-10-2026, relecture du tour 2, N1 ; superviseur R-759) : le branchement de PRODUCTION, dans `juger`
    "S10_juger_n_envoie_plus_la_periode": [(BAN, "                                 periode=_bornes)", "                                 periode=None)")],
    "S11_juger_lit_l_indice_sans_la_lecture": [(BAN, "                                 admis=lambda v, j: achat_admis(v, cours[v], j, lecture),",
                                                "                                 admis=lambda v, j: achat_admis(v, cours[v], j, None),")],
}
CODE = r'''
import sys, os, csv
sys.path.insert(0, "programmes")
import MODULE_JUGEMENT as J, MODULE_POSITIONS as P, JUGE_DES_STRATEGIES as B
rouges = []
def dire(nom, ok, det=""):
    if not ok:
        rouges.append(nom + " · " + str(det))
def jour(k):
    return "2025-%02d-%02d" % (1 + k // 28, 1 + k % 28)
def barre(k, o=100.0, hi=101.0, lo=99.0, c=100.0):
    return dict(date=jour(k), open=o, high=hi, low=lo, close=c, volume=1.0)
# E1
A = [barre(k) for k in range(80)]
Bv = [barre(k, 50.0, 60.0, 49.0, 55.0) for k in range(80)]
lec = {"passages": {"A": [(jour(0), None)], "B": []}, "trous": {}, "composition": True}
cours = {"A": A, "B": Bv}
tires = []
def ent(v, j):
    tires.append(v)
    return B.jouer_une_entree(v, cours[v], j, 0.04, 0.025, 20, P, lec)
ops = [{"valeur": "A", "date_signal": jour(k)} for k in range(0, 40, 4)]
J.etalon_hasard(ops, cours, ["A", "B"], 0.04, 0.025, 20, P, mode="valeur", n_tirages=20, entree=ent,
                admis=lambda v, j: B.achat_admis(v, cours[v], j, lec))
dire("E1 aucun achat hors de l'indice (cas fabriqué)", tires and "B" not in tires, "%d tirés, %d sur B" % (len(tires), tires.count("B")))
# E2
R = "."
mnemo = B.table_mnemoniques(B.trouver(R, "REFERENTIEL_VALEURS"))
sig = B.charger_module(B.trouver(R, "MODULE_C5_ETENDU_10"), "sig")
f = next(x for x in csv.DictReader(open("donnees/cac40_strategies.csv", encoding="utf-8-sig")) if x["id"] == "C5E10-QA-V1")
ok0, _m, bornes = B.porte_0(f); f.setdefault("_fonction_signal", "signaux_c5etendu10")
cr, lr = B.lire_par_le_lecteur(R, "donnees/cours_maitre.csv", mnemo)
o2, _ = B.jouer(f, cr, mnemo, sig, P, periode=bornes, lecture=lr)
tp, sl, h = B.pourcent(f["tp"]), B.pourcent(f["sl"]), B.lire_horizon(f["horizon"])
univ = [v for v in (mnemo.get(x.strip().upper(), B.cle_valeur(x)) for x in f["univers"].split(",") if x.strip()) if v in cr]
hors = lambda v, j: not B.dans_l_indice(lr["passages"].get(v, []), cr[v][j]["date"])
cal = {}
for v in [v for v in univ if len(cr[v]) > h + 3]:
    for i, b in enumerate(cr[v]):
        cal.setdefault(b["date"], []).append((v, i))
anc = [(v, i + 1) for o in o2 for (v, i) in cal.get(o["date_signal"], []) if i + 1 < len(cr[v])]
dire("E2a calibrage : le cas connu du relecteur (306 achats, dont 42 hors de l'indice)",
     (len(anc), sum(hors(v, j) for v, j in anc)) == (306, 42), (len(anc), sum(hors(v, j) for v, j in anc)))
for mode in ("valeur", "date"):
    t2 = []
    def e2(v, j):
        t2.append((v, j))
        return B.jouer_une_entree(v, cr[v], j, tp, sl, h, P, lr)
    J.etalon_hasard(o2, cr, univ, tp, sl, h, P, mode=mode, n_tirages=30, entree=e2,
                    admis=lambda v, j: B.achat_admis(v, cr[v], j, lr), periode=bornes)
    nh = sum(hors(v, j) for v, j in t2)
    npd = sum(1 for v, j in t2 if not (bornes[0] <= cr[v][j - 1]["date"] <= bornes[1]))
    dire("E2b mode %s : 0 hors de l'indice, 0 hors de la période (cas réel)" % mode, t2 and nh == 0 and npd == 0, (len(t2), nh, npd))
# E3 : un trou juste après le signal ; un seul achat possible -> le hasard rend exactement la stratégie
S = [barre(k) for k in range(30)] + [barre(k, 100.0, 105.0, 99.0, 104.0) for k in range(32, 60)]   # trou : jours 30 et 31
lec3 = {"passages": {"X": [(jour(0), None)]}, "trous": {"X": [jour(30), jour(31)]}, "composition": True}
cours3 = {"X": S}
d_sig = jour(29)
j = [b["date"] for b in S].index(d_sig) + 1
op = B.jouer_une_entree("X", S, j, 0.04, 0.025, 20, P, lec3)
hz = J.etalon_hasard([{"valeur": "X", "date_signal": d_sig}], cours3, ["X"], 0.04, 0.025, 20, P, mode="valeur", n_tirages=5,
                     entree=lambda v, k: B.jouer_une_entree(v, cours3[v], k, 0.04, 0.025, 20, P, lec3),
                     admis=lambda v, k: B.achat_admis(v, cours3[v], k, lec3))
dire("E3 trou après le signal : le hasard, seul achat possible, rend la stratégie au centime",
     op is not None and round(hz.get("gain_median", 0), 0) == round(op["net"], 0) and op["date_sortie"] > jour(31), (op, hz.get("gain_median")))
# E4 et E5 : mode date, période bornée, valeur gardée
per = (jour(10), jour(30))
t4 = []
def e4(v, k):
    t4.append((v, k))
    return B.jouer_une_entree(v, cours[v], k, 0.04, 0.025, 20, P, None)
lec4 = {"passages": {"A": [(jour(0), None)], "B": [(jour(0), None)]}, "trous": {}, "composition": True}
J.etalon_hasard([{"valeur": "A", "date_signal": jour(12)}] * 5, cours, ["A", "B"], 0.04, 0.025, 20, P, mode="date", n_tirages=40,
                entree=e4, admis=lambda v, k: B.achat_admis(v, cours[v], k, lec4), periode=per)
dire("E4 mode date : aucun signal hors de la période", t4 and all(per[0] <= cours[v][k - 1]["date"] <= per[1] for v, k in t4), len(t4))
dire("E5 mode date : la valeur réelle est gardée", t4 and all(v == "A" for v, k in t4), sorted(set(v for v, k in t4)))
# E7 : le nombre joué par tirage dit vrai — le second achat tombe sur la dernière séance, sans seuil touché : non joué
D = [barre(k) for k in range(30)]
cours7 = {"X": D}
hz7 = J.etalon_hasard([{"valeur": "X", "date_signal": jour(5)}, {"valeur": "X", "date_signal": jour(28)}], cours7, ["X"],
                      0.04, 0.025, 20, P, mode="valeur", n_tirages=5,
                      entree=lambda v, k: B.jouer_une_entree(v, cours7[v], k, 0.04, 0.025, 20, P, None),
                      admis=lambda v, k: B.achat_admis(v, cours7[v], k, None))
dire("E7 le nombre joué par tirage dit vrai (1 sur 2)", (hz7.get("operations_reelles"), hz7.get("jouees_par_tirage_min"),
     hz7.get("jouees_par_tirage_max")) == (2, 1, 1), hz7)
# E7b : le plus petit et le plus grand diffèrent — deux valeurs, l'une finit à la séance tirée, l'autre non
cours7b = {"X": [barre(k) for k in range(30)], "Y": [barre(k) for k in range(29)]}
hz7b = J.etalon_hasard([{"valeur": "X", "date_signal": jour(27)}] * 3, cours7b, ["X", "Y"], 0.04, 0.025, 20, P, mode="valeur",
                       n_tirages=60,
                       entree=lambda v, k: B.jouer_une_entree(v, cours7b[v], k, 0.04, 0.025, 20, P, None),
                       admis=lambda v, k: B.achat_admis(v, cours7b[v], k, None))
dire("E7b le plus petit et le plus grand nombre joué sont rendus chacun", hz7b.get("jouees_par_tirage_min", 9) < hz7b.get("jouees_par_tirage_max", -1),
     (hz7b.get("jouees_par_tirage_min"), hz7b.get("jouees_par_tirage_max")))
# E8 : une lecture qui ne demande pas la composition ne filtre pas (B est tirable)
lec8 = {"passages": {"A": [(jour(0), None)], "B": []}, "trous": {}, "composition": False}
t8 = []
def e8(v, k):
    t8.append(v)
    return B.jouer_une_entree(v, cours[v], k, 0.04, 0.025, 20, P, lec8)
J.etalon_hasard(ops, cours, ["A", "B"], 0.04, 0.025, 20, P, mode="valeur", n_tirages=20, entree=e8,
                admis=lambda v, k: B.achat_admis(v, cours[v], k, lec8))
dire("E8 composition non demandée : aucun filtre", "B" in t8, sorted(set(t8)))
# E9 : les dernières séances restent tirables, comme dans `jouer` (mode date)
t9 = []
def e9(v, k):
    t9.append(k)
    return B.jouer_une_entree(v, cours7[v], k, 0.04, 0.025, 20, P, None)
J.etalon_hasard([{"valeur": "X", "date_signal": jour(5)}], cours7, ["X"], 0.04, 0.025, 20, P, mode="date", n_tirages=200,
                entree=e9, admis=lambda v, k: B.achat_admis(v, cours7[v], k, None))
dire("E9 les dernières séances sont tirables", t9 and max(t9) == len(D) - 1, max(t9) if t9 else None)
# E10 : sans lecture, en mode valeur, le nouvel étalon rend EXACTEMENT ce que rendait l'ancien sur un cas fabriqué.
# Chiffres FIGÉS, sortis une fois de l'ancien code (version officielle 2a3c597, 28-10-2026) — l'ancien code n'est
# jamais recopié ici (superviseur R-759 du 29-10-2026).
import math
cours10 = {}
for n, (a, fq) in {"A": (100.0, 0.31), "B": (50.0, 0.17), "C": (20.0, 0.53)}.items():
    s10 = []
    for k in range(120):
        o = a * (1 + 0.06 * math.sin(fq * k)); c = a * (1 + 0.06 * math.sin(fq * k + 0.7))
        s10.append(dict(date=jour(k), open=round(o, 4), high=round(max(o, c) * 1.02, 4), low=round(min(o, c) * 0.985, 4),
                        close=round(c, 4), volume=1.0))
    cours10[n] = s10
ops10 = [{"valeur": "ABC"[k % 3], "date_signal": jour(k)} for k in range(2, 90, 7)]
r10 = J.etalon_hasard(ops10, cours10, ["A", "B", "C"], 0.04, 0.025, 20, P, mode="valeur", n_tirages=25,
                      entree=lambda v, k: B.jouer_une_entree(v, cours10[v], k, 0.04, 0.025, 20, P, None),
                      admis=lambda v, k: B.achat_admis(v, cours10[v], k, None))
fige = {"n_tirages": 25, "taux_median": 38.5, "taux_95pct": 46.2, "taux_max": 61.5, "gain_median": -3900.0, "gain_95pct": 2590.0, "gain_max": 15571.0}
dire("E10 sans lecture, l'ancien et le nouvel étalon rendent la même chose (chiffres figés)",
     {k: r10.get(k) for k in fige} == fige, {k: r10.get(k) for k in fige})
# E11 : le branchement de PRODUCTION — le vrai `juger`, sur C5E10-QA-V1 et le maître, reçoit un mandataire du module de
# jugement qui enregistre ce que `juger` passe à l'étalon et chaque achat tiré (relecture du tour 2, N1)
import types, importlib.util as _iu
recus, tires11 = [], []
def _etalon(*a, **k):
    recus.append(k)
    e0 = k["entree"]
    def e(v, j):
        tires11.append((v, j))
        return e0(v, j)
    k = dict(k, entree=e)
    return J.etalon_hasard(*a, **k)
mand = types.SimpleNamespace(**{n: getattr(J, n) for n in dir(J) if not n.startswith("__")})
mand.etalon_hasard = _etalon
_fs = B.trouver(R, "MODULE_STATISTIQUES")
_sp = _iu.spec_from_file_location("sta", _fs); S_ = _iu.module_from_spec(_sp); _sp.loader.exec_module(S_)
seances = {b["date"] for s_ in cr.values() for b in s_}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    B.juger(f, o2, cr, seances, mand, S_, P, mnemo, bornes, (sig,), lecture=lr)
modes = sorted(k.get("mode") for k in recus)
dire("E11a juger appelle l'étalon dans les deux modes, avec la période de la fiche",
     modes == ["date", "valeur"] and all(tuple(k.get("periode") or ()) == tuple(bornes) for k in recus), (modes, [k.get("periode") for k in recus]))
nh11 = sum(hors(v, j) for v, j in tires11)
np11 = sum(1 for v, j in tires11 if not (bornes[0] <= cr[v][j - 1]["date"] <= bornes[1]))
dire("E11b par juger : 0 achat hors de l'indice, 0 hors de la période", tires11 and nh11 == 0 and np11 == 0, (len(tires11), nh11, np11))
# E6
try:
    J.etalon_hasard(ops, cours, ["A"], 0.04, 0.025, 20, P, mode="valeur", n_tirages=2)
    dire("E6 sans la mécanique de la stratégie, l'étalon refuse", False, "il a joué")
except ValueError:
    pass
except Exception as e:
    dire("E6 sans la mécanique de la stratégie, l'étalon refuse", False, "il a planté autrement : %s" % type(e).__name__)
print("ROUGES %d" % len(rouges))
for x in rouges:
    print("  " + x)
'''


def jeu(sab):
    """Joue les épreuves sur une copie du dépôt, sabotée ou non, et rend le nombre de rouges et leur détail.

    ① RÔLE — Un jeu complet d'épreuves.
    ② CONTEXTE D APPEL — Le programme principal, une fois pour Z0 et une fois par sabotage.
    ③ ENTRÉE — `sab` : le nom du sabotage, une clé de SABOTAGES.
    ④ CONDITIONS D ENTRÉE — Chaque texte visé par le sabotage existe une seule fois.
    ⑤ SORTIE — DEUX valeurs : le nombre de rouges (−1 si le jeu n'a pas pu tourner), et le détail. [rend: 2]
    ⑥ TRAITEMENT — copier sans .git, saboter, lancer CODE, lire « ROUGES n ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Une copie temporaire, effacée.
    ⑪ TERMINAISON — Bornée à 600 secondes.
    """
    d = tempfile.mkdtemp(prefix="etalon_indice_")
    try:
        r = os.path.join(d, "r")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "__pycache__", "archives"))
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            if t.count(a) != 1:
                return -1, "texte du sabotage introuvable (%d fois) : %s" % (t.count(a), a[:60])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))
        x = subprocess.run([sys.executable, "-B", "-c", CODE], cwd=r, capture_output=True, text=True, timeout=600)
        lignes = x.stdout.strip().splitlines()
        tete = next((l for l in lignes if l.startswith("ROUGES ")), None)
        if x.returncode != 0 or tete is None:
            return 99, "plantage : " + (x.stderr.strip().splitlines() or ["?"])[-1][:160]
        return int(tete.split()[1]), "\n".join(lignes[lignes.index(tete) + 1:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    n, det = jeu(sab)
    if sab == "Z0":
        bon = n == 0
        print(f"== {sab} : {'vert' if n == 0 else str(n) + ' rouge(s)'} {'(attendu)' if bon else '<-- ATTENDU VERT'}")
    else:
        # un plantage (99) ou un sabotage inapplicable (-1) ne prouve rien : il ne compte JAMAIS comme sabotage vu
        # (relecture du 28-10-2026, m8)
        bon = 0 < n < 99
        etat = "PLANTAGE" if n == 99 else "INAPPLICABLE" if n < 0 else "vert" if n == 0 else str(n) + " rouge(s)"
        print(f"== {sab} : {etat} {'(attendu)' if bon else '<-- SABOTAGE NON VU OU INVALIDE'}")
    if det and (not bon or sab == "Z0"):
        print(det)
    _faute = _faute or not bon
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
