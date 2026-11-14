#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_VENTE_REGLABLE — Mer 11-11-2026 (Paris) — mission « VENTE » du plan V7 (bloc 4, bloc 5l geste ④).
Simulation uniquement — aucun ordre réel, jamais.

LE SENS EN TÊTE. La vente se décide à UN endroit, `programmes/MODULE_POSITIONS.vendre` (R-708 : deux implémentations
d'une même chose divergent toujours). Le 11-11-2026, elle accepte de plus un stop « sans stop » (décision de Jean-Luc
du 19-10-2026 à 20h22, « et bien sûr, ajoutez le sans stop », BACKLOG A-541), et la moulinette (PREPARER → DECLINER →
JOUER_LES_VERSIONS) sait essayer une LISTE de valeurs écrite telle quelle dans `donnees/combinatoires/VOISINAGE.csv`
(colonne `liste`, modification 1 d'A-541 du 19-10-2026 à 21h46), « sans stop » et la durée « aucune » compris
(A-645, « LA SORTIE RÉGLABLE »). Le programme du soir et le juge à 8 critères, eux, continuent de REFUSER « sans
stop » (garde-fou d'A-645 : aucune fiche VIVANTE ne reçoit une sortie que le soir ne sait pas tenir), et `juger`
refuse de rendre un point mort pour une version sans stop (A-541 ④). Ce fichier prouve ces propriétés, et que chaque
épreuve a des dents : chaque sabotage retire une protection et au moins une épreuve doit rougir (R-731).

CE QUI EST ÉPROUVÉ :
  W0 le contrat de COMMUN : STOP_AUCUN refuse tout calcul (1 − sl, float, comparaison) ; le mot exact « sans stop »
     est reconnu (casse et blancs de bord), « sans_stop », « aucun », « » ne le sont pas.
  W1 `vendre` sans stop, valeurs connues écrites à la main : une série qui plonge à −50 % puis touche +4 % est vendue
     à l'objectif (avec un stop de 2,5 % : au stop, le jour même) ; la vente rendue porte la sentinelle, jamais −inf.
  W2 sans stop et durée « aucune » : sans objectif touché, « garder » rend None, « vendre » la dernière clôture, sous
     le motif FIN_DES_DONNEES depuis le 13-11-2026 (décision de Jean-Luc du 12-11-2026 à 09h18).
  W3 sans stop, durée 3 : vendue à la clôture de la 3e séance après l'achat (HORIZON).
  W4 VRAIE LIGNE (R-732), témoin du golden : VINCI acheté le 07-06-2024 à 113,60, plus bas 110,75 sous le stop
     110,76 → vendu au stop le jour même ; sans stop : pas de motif SL, une autre sortie.
  W5 `seuils_de_vente` sans stop : l'objectif est celui du cas chiffré (ENGIE 13,25 → 13,78), le stop la sentinelle.
  W6 propriété : sur toute la série ENGIE du témoin, sans stop, aucune vente ne porte un motif SL ; avec stop, si.
  W7 le juge : `seuil_de_la_fiche` REFUSE « sans stop » (le soir, le juge à 8 critères) ; `seuil_de_la_fiche_ou_aucun`
     l'accepte pour sl et le refuse pour tp ; `porte_0` accepte la vraie fiche C5E10-QA-V1 mise « sans stop » ;
     `juger` la refuse par MOTIF_SANS_STOP_NON_JUGEABLE.
  W8 `jouer` sur la vraie fiche C5E10-QA-V1 mise « sans stop » : autant d'opérations qu'avec le stop (jetons
     illimités : les mêmes signaux), aucune sortie SL, au moins une sortie différente.
  W9 PREPARER : la vraie ligne `sl` de VOISINAGE.csv donne les 15 valeurs de la grille du 19-10-2026, « sans stop » en
     dernier ; liste vide → le pas régulier d'avant ; valeur de la fiche absente de la liste → ajoutée ; « aucune »
     dans une liste d'horizon → en dernier ; fiche « sans stop » sans liste → refus ; élément illisible → refus.
  W10 PREPARER `main` sur le vrai registre et le vrai VOISINAGE.csv : 7 × 15 × 5 × 11 = 5 775 versions annoncées.
  W11 DECLINER : « sans stop » et « aucune » normalisés en mots, la version de la fiche repérée une fois ; « sans stop »
     refusé pour tp ; « sans_stop » et « aucun » refusés.
  W12 JOUER_LES_VERSIONS `controler_fusion` : mot contre mot → aucun écart ; mot contre nombre → un écart.
  W13 DE BOUT EN BOUT, `JOUER_LES_VERSIONS.py` sur une combinatoire de 4 versions de C5E10-OBS-V1 (stop 2,5 % ou sans
      stop × durée 20 ou aucune) : code 0, le juge seul calibré, 4 lignes écrites, la durée « aucune » DITE à l'écran ;
      PUIS `TRIER_LES_VARIANTES.py` sur ce fichier (phase 2 d'E1F, M-1) : code 0, 4 versions essayées, les deux
      « aucune » écartées comme non mesurables avec leur raison, aucune « aucune » dans le fichier trié.
  W15 (12-11-2026, défaut D1) PROPRIÉTÉ du soir : pour toute fiche du registre et cinq mutantes de C5E10-QA-V1 qui
      passent la porte du laboratoire, `fiche_suivie` la refuse à la lecture du soir ⇔ `reglages_du_registre` ne la
      règle pas ; « sans stop » et « aucune » (réglage du soir par défaut : refuser) sont refusées par les deux.
  W17 (12-11-2026) le réglage du soir `donnees/REGLAGES_DU_SOIR.csv` : « refuser » au dépôt, À DÉCIDER ; seul
      « accepter » ouvre ; un autre mot, une ligne ou un fichier absents ferment (la valeur la plus stricte).
  W16 (12-11-2026, défaut D3) : `JUGER_SUR_8_CRITERES.py` refuse « sans stop » par son motif nommé avant de jouer.
  W14 propriété R-708 par l'arbre syntaxique : dans PREPARER, DECLINER et JOUER_LES_VERSIONS, tout appel à la lecture
      STRICTE `lire_horizon` vit dans une fonction qui reconnaît HORIZON_AUCUNE.

USAGE : python3 -B tests/EPREUVES_DE_LA_VENTE_REGLABLE_Mer_11-11-2026.py <racine du dépôt> [--saboter | nom]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si une cible de
sabotage est introuvable.

① RÔLE — Prouver la vente réglable (« sans stop », liste de VOISINAGE.csv, « aucune » dans la moulinette).
② CONTEXTE D'APPEL — À la main ; par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque
  fichier de tests/ avec la racine, puis avec « --saboter ».
③ ENTRÉE — la racine, et facultativement « --saboter » ou un nom de sabotage.
④ CONDITIONS D'ENTRÉE — le témoin du golden sous temoins/, le registre des stratégies avec C5E10-QA-V1 et
  C5E10-OBS-V1, `donnees/combinatoires/VOISINAGE.csv` avec sa colonne `liste`, le golden sous gouvernance/.
⑤ SORTIE — le code de sortie ; une ligne par épreuve rouge.
  [rend: 1]
⑥ TRAITEMENT — pour Z0 puis chaque sabotage : copier `programmes/` (saboté), lier `donnees/`, `temoins/`,
  `gouvernance/` par liens physiques, jouer W0-W12, W14, W15 et W17 dans un sous-processus de la copie, puis W13
  et W16.
⑦ UNITÉ — seuils en FRACTIONS dans `vendre`, en POURCENTS dans les tableaux de la moulinette ; prix en euros ;
  durées en séances.
⑧ POURQUOI — voir le sens en tête ; R-731 (toute modification de code passe épreuves et sabotages).
⑨ CE QUI CLOCHE — Les liens PHYSIQUES (`os.link`) partagent l'octet avec le dépôt : un programme qui RÉÉCRIRAIT un
  fichier de `donnees/` en place l'abîmerait dans le dépôt. Les programmes joués ici n'écrivent que dans des
  dossiers temporaires créés par l'épreuve (vérifié par lecture le 11-11-2026 : PREPARER et DECLINER écrivent dans
  leur dossier de sortie, JOUER_LES_VERSIONS dans son fichier de résultats, le juge n'écrit rien). Des liens
  symboliques ne suffisent pas : le juge cherche ses fichiers par `os.walk`, qui ne les suit pas. W13 dure environ
  30 secondes par passage (le juge seul se calibre) : la série complète des sabotages prend environ 12 minutes.
⑩ EFFET — dossiers temporaires, effacés.
⑪ TERMINAISON — chaque sous-processus est borné à 900 s ; un délai dépassé compte comme rouge.
  [sort: oui — code]
"""
import json, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MODP, BAN, COM = "programmes/MODULE_POSITIONS.py", "programmes/JUGE_DES_STRATEGIES.py", "programmes/COMMUN.py"
PREP = "programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py"
DECL, JOUE = "programmes/DECLINER_LES_STRATEGIES.py", "programmes/JOUER_LES_VERSIONS.py"
LIES = ("donnees", "temoins", "gouvernance")

SABOTAGES = {
    "Z0": [],
    # N-3 (relecture Cowork du 14-11-2026) : le tri écarte toute version chiffrée — W13 rougit.
    "T_N3_tri_ecarte_les_chiffrees": [("programmes/TRIER_LES_VARIANTES.py",
                                       "    ops70 = (ligne.get(\"operations_70\") or \"\").strip()\n    if ops70.isdigit()",
                                       "    return False, True, RAISON_CASE_VIDE\n    ops70 = (ligne.get(\"operations_70\") or \"\").strip()\n    if ops70.isdigit()")],
    "T1_vendre_passe_la_sentinelle_au_test": [(MODP, '    if stop is _stop_aucun():\n        stop = float("-inf")\n', '')],
    "T2_vendre_rend_moins_l_infini": [(MODP, '    stop_rendu = stop\n    if stop is _stop_aucun():\n        stop = float("-inf")\n',
                                       '    if stop is _stop_aucun():\n        stop = float("-inf")\n    stop_rendu = stop\n')],
    "T3_sans_stop_ecrit_comme_un_grand_stop": [(MODP, '        return seuils_de_vente(prix_entree, tp, 0.0)[0], sl',
                                                '        return seuils_de_vente(prix_entree, tp, 0.99)')],
    "T4_juge_ne_lit_plus_sans_stop": [(BAN, '    if champ == "sl" and est_le_mot_du_stop_aucun(fiche.get("sl")):\n        return STOP_AUCUN',
                                       '    if False:\n        return STOP_AUCUN')],
    "T5_juger_sans_refus_nomme": [(BAN, '    if seuil_de_la_fiche_ou_aucun(fiche, "sl") is STOP_AUCUN:\n        raise ValueError(MOTIF_SANS_STOP_NON_JUGEABLE)',
                                   '    if False:\n        raise ValueError(MOTIF_SANS_STOP_NON_JUGEABLE)')],
    "T6_le_soir_lit_sans_stop": [(BAN, '    texte = fiche.get(champ)\n    v = pourcent(texte)\n',
                                  '    texte = fiche.get(champ)\n    if champ == "sl" and est_le_mot_du_stop_aucun(texte):\n        return STOP_AUCUN\n    v = pourcent(texte)\n')],
    "T7_liste_ignoree": [(PREP, '        liste = (voisinage[p].get("liste") or "").strip()', '        liste = ""')],
    "T8_valeur_de_la_fiche_oubliee": [(PREP, '    lues.append(valeur_fiche)\n', '')],
    "T9_liste_dans_l_ordre_ecrit": [(PREP, '    return [ecrire_nombre(x) for x in nombres] + mots',
                                     '    return [x if isinstance(x, str) else ecrire_nombre(x) for x in dict.fromkeys(lues)]')],
    "T10_decliner_sans_stop_illisible": [(DECL, '    if parametre == "sl" and COMMUN.est_le_mot_du_stop_aucun(t):\n        return COMMUN.STOP_AUCUN, COMMUN.MOT_DU_STOP_AUCUN\n', '')],
    "T11_decliner_aucune_illisible": [(DECL, '    if parametre == "horizon" and COMMUN.lire_horizon_ou_aucune(t) is COMMUN.HORIZON_AUCUNE:\n        return COMMUN.HORIZON_AUCUNE, COMMUN.MOT_DE_L_HORIZON_AUCUNE\n', '')],
    "T12_fusion_mot_contre_nombre_acceptee": [(JOUE, '            ecart = not all(mots)', '            ecart = False')],
    "T13_marge_compte_aucune": [(JOUE, '    _chiffrees = [d for d in _durees if d is not COMMUN.HORIZON_AUCUNE and d is not None]',
                                 '    _chiffrees = [d for d in _durees if d is not None]')],
    "T14_mot_devine": [(COM, '    return str(x).strip().lower() == MOT_DU_STOP_AUCUN', '    return str(x).strip().lower().startswith("sans")')],
    # T15 : la sentinelle se laisse convertir en un grand stop (0,99), ce qu'A-541 ⑤ interdit. (Retirer seulement
    # `__sub__` ne mord pas : Python lève déjà TypeError sur `1 - objet` sans opération définie — essayé le 11-11-2026.)
    "T15_sentinelle_convertible": [(COM, '    __int__ = __index__ = __float__ = _refuser_le_calcul_du_stop\n    __lt__ = __le__ = __gt__ = __ge__ = _refuser_le_calcul_du_stop\n    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _refuser_le_calcul_du_stop\n    __truediv__',
                                    '    __int__ = __index__ = _refuser_le_calcul_du_stop\n    __float__ = lambda self: 0.99\n    __lt__ = __le__ = __gt__ = __ge__ = _refuser_le_calcul_du_stop\n    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _refuser_le_calcul_du_stop\n    __truediv__')],
    # Tour 2 (12-11-2026) : D1 et D3 du relecteur neuf.
    "T17_porte_du_soir_sans_lecture_du_soir": [(BAN, '        lecture_du_soir(racine, fiche)\n    except ValueError as e:\n        return None, None, "lecture du soir : " + str(e)',
                                                 '        pass\n    except ValueError as e:\n        return None, None, "lecture du soir : " + str(e)')],
    "T18_soir_relit_a_sa_facon": [("programmes/TENIR_LES_POSITIONS.py", '                tp, sl, _h = juge.lecture_du_soir(base, x)\n',
                                   '                tp, sl = juge.seuil_de_la_fiche(x, "tp"), juge.seuil_de_la_fiche(x, "sl")\n'
                                   '                _h = lire_horizon_ou_aucune(x.get("horizon", ""))\n')],
    "T19_aucune_acceptee_par_defaut": [(BAN, '    return any((l.get("reglage") or "").strip() == REGLAGE_HORIZON_AUCUNE_AU_SOIR',
                                        '    return True or any((l.get("reglage") or "").strip() == REGLAGE_HORIZON_AUCUNE_AU_SOIR')],
    "T21_reglage_absent_ouvre_le_soir": [(BAN, '    if not isinstance(lignes, list):\n        return False\n    return any(',
                                          '    if not isinstance(lignes, list):\n        return True\n    return any(')],
    "T20_juge_a_8_joue_avant_de_refuser": [("programmes/JUGER_SUR_8_CRITERES.py", '        if banc.seuil_de_la_fiche_ou_aucun(fiche, "sl") is banc.STOP_AUCUN:\n            raise',
                                            '        if False:\n            raise')],
    "T16_preparer_relit_l_horizon_strictement": [(PREP, '        h = COMMUN.lire_horizon_ou_aucune(texte)\n        if h is COMMUN.HORIZON_AUCUNE:',
                                                  '        h = COMMUN.lire_horizon(texte)\n        if h is COMMUN.HORIZON_AUCUNE:')],
}

CODE = r'''
import sys, os, json, glob, ast, csv, tempfile, io, contextlib
sys.path.insert(0, "programmes")
import MODULE_POSITIONS as P, JUGE_DES_STRATEGIES as B, COMMUN
import PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES as PR, DECLINER_LES_STRATEGIES as DE, JOUER_LES_VERSIONS as JV
S = COMMUN.STOP_AUCUN
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
from CONTRATS_DES_FICHIERS import fiches_du_registre, chemin_du_registre
FICHES = fiches_du_registre(chemin_du_registre("."))

def w0():
    leves = []
    for f in (lambda: 1 - S, lambda: float(S), lambda: 3 <= S, lambda: S * 2, lambda: 1.0 - S):
        try:
            f(); leves.append(False)
        except TypeError:
            leves.append(True)
    mots = [COMMUN.est_le_mot_du_stop_aucun(x) for x in ("sans stop", "  Sans Stop ", "sans_stop", "aucun", "", None, "-2.5%")]
    note("W0 contrat : STOP_AUCUN refuse tout calcul ; seul le mot exact est reconnu",
         all(leves) and mots == [True, True, False, False, False, False, False] and str(S) == "sans stop", (leves, mots))
essai("W0", w0)

def w1():
    s = [b(1, 100, 100, 99, 99.5)] + [b(2 + i, 60, 61, 50, 55) for i in range(4)] + [b(6, 99, 104.5, 98, 104)]
    r = P.vendre(s, 0, {"tp": 0.04, "sl": S, "horizon": 20}, "vendre")
    q = P.vendre(s[:1] + [b(2, 99, 99.5, 97, 98)] + s[1:], 0, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre")
    o = ((r["motif"], r["date_sortie"], r["px"], r["stop"] is S), (q["motif"], q["date_sortie"], q["px"]))
    note("W1 sans stop : -50 % traverse, vendue a l'objectif ; la vente porte la sentinelle ; avec stop : au stop",
         o == (("TP", "2026-01-06", 104.0, True), ("SL", "2026-01-02", 97.5)), o)
essai("W1", w1)

def w2():
    s = [b(1, 100, 100, 99, 100)] + [b(2 + i, 90, 91, 40, 50) for i in range(30)]
    g = P.vendre(s, 0, {"tp": 0.04, "sl": S, "horizon": A}, "garder")
    v = P.vendre(s, 0, {"tp": 0.04, "sl": S, "horizon": A}, "vendre")
    o = (g, (v["motif"], v["date_sortie"], v["px"], v["stop"] is S))
    # depuis le 13-11-2026 : motif FIN_DES_DONNEES (décision de Jean-Luc du 12-11-2026 à 09h18), HORIZON avant
    note("W2 sans stop et aucune : garder None ; vendre a la derniere cloture, motif FIN_DES_DONNEES", o == (None, ("FIN_DES_DONNEES", "2026-01-31", 50, True)), o)
essai("W2", w2)

def w3():
    s = [b(1, 100, 100, 99, 100)] + [b(2 + i, 90, 91, 40, 50 + i) for i in range(10)]
    v = P.vendre(s, 0, {"tp": 0.04, "sl": S, "horizon": 3}, "vendre")
    o = (v["motif"], v["date_sortie"], v["px"])
    note("W3 sans stop, duree 3 : vendue a la cloture de la 3e seance apres l'achat", o == ("HORIZON", "2026-01-04", 52), o)
essai("W3", w3)

def w4():
    s = cours["VINCI"]; j = [k for k, x in enumerate(s) if x["date"] == "2024-06-07"][0]
    a = P.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre")
    z = P.vendre(s, j, {"tp": 0.04, "sl": S, "horizon": 20}, "vendre")
    o = (s[j]["open"], s[j]["low"], (a["motif"], a["date_sortie"], a["px"]), (z["motif"], z["date_sortie"]))
    note("W4 vraie ligne VINCI 07-06-2024 : au stop 110,76 le jour meme ; sans stop, ni SL ni ce jour",
         o[:3] == (113.6, 110.75, ("SL", "2024-06-07", 110.76)) and not z["motif"].startswith("SL") and z["date_sortie"] != "2024-06-07", o)
essai("W4", w4)

def w5():
    o = (P.seuils_de_vente(13.25, 0.04, S), P.seuils_de_vente(13.25, 0.04, 0.025))
    note("W5 seuils_de_vente sans stop : meme objectif 13,78, stop = la sentinelle", o[0][0] == o[1][0] == 13.78 and o[0][1] is S, o)
essai("W5", w5)

def w6():
    s = cours["ENGIE"]
    sans = [P.vendre(s, j, {"tp": 0.04, "sl": S, "horizon": 20}, "vendre") for j in range(len(s) - 1)]
    avec = [P.vendre(s, j, {"tp": 0.04, "sl": 0.025, "horizon": 20}, "vendre") for j in range(len(s) - 1)]
    m_s = {r["motif"] for r in sans if r}; m_a = {r["motif"] for r in avec if r}
    note("W6 ENGIE entiere : sans stop aucun motif SL ; avec stop, des SL", not any(m.startswith("SL") for m in m_s) and "SL" in m_a, (sorted(m_s), sorted(m_a)))
essai("W6", w6)

def w7():
    f = dict(FICHES["C5E10-QA-V1"], sl="sans stop")
    o = []
    try:
        B.seuil_de_la_fiche(f, "sl"); o.append("strict accepte")
    except ValueError:
        o.append("strict refuse")
    o.append(B.seuil_de_la_fiche_ou_aucun(f, "sl") is S)
    try:
        B.seuil_de_la_fiche_ou_aucun(dict(f, tp="sans stop"), "tp"); o.append("tp accepte")
    except ValueError:
        o.append("tp refuse")
    o.append(B.porte_0(f)[0])   # porte_0 = la porte du LABORATOIRE (la moulinette la passe) ; le soir : W15
    try:
        B.juger(f, [], cours, [], None, None, P); o.append("juger rend")
    except ValueError as e:
        o.append(str(e) == B.MOTIF_SANS_STOP_NON_JUGEABLE)
    note("W7 juge (laboratoire) : lecture stricte refuse, lecture ou_aucun accepte (sl seul), porte 0 du laboratoire passe, juger refuse par son motif",
         o == ["strict refuse", True, "tp refuse", True, True], o)
essai("W7", w7)

def w8():
    mn = B.table_mnemoniques(B.trouver(".", "REFERENTIEL_VALEURS"))
    c, lec = B.lire_par_le_lecteur(".", os.path.relpath(B.fichiers_de_cours(".")[0], "."), mn)
    mod_pos = B.charger_module(B.trouver(".", "MODULE_POSITIONS.py"), "pos")
    f = dict(FICHES["C5E10-QA-V1"])
    sig = B.signal_de_la_fiche(".", f)
    bornes = B.porte_0(f)[2]
    with contextlib.redirect_stdout(io.StringIO()):
        o1, _ = B.jouer(f, c, mn, sig, mod_pos, periode=bornes, lecture=lec)
        o2, _ = B.jouer(dict(f, sl="sans stop"), c, mn, sig, mod_pos, periode=bornes, lecture=lec)
    cle = lambda o: (o["valeur"], o["date_signal"])
    diff = sum(1 for x, y in zip(o1, o2) if (x["motif"], x["date_sortie"]) != (y["motif"], y["date_sortie"]))
    o = (len(o1), len(o2), [cle(x) for x in o1] == [cle(y) for y in o2], sorted({x["motif"] for x in o2}), diff)
    note("W8 jouer C5E10-QA-V1 sans stop : memes signaux, aucune sortie SL, des sorties changees",
         o[0] == o[1] > 0 and o[2] and not any(m.startswith("SL") for m in o[3]) and diff > 0, o)
essai("W8", w8)

def w9():
    vois = {r["parametre"]: r for r in csv.DictReader(open("donnees/combinatoires/VOISINAGE.csv", encoding="utf-8"))}
    grille = PR.valeurs_de_la_liste("sl", vois["sl"]["liste"], 2.5)
    pas = PR.voisins(2.5, dict(vois["sl"], liste=""))
    ajout = PR.valeurs_de_la_liste("sl", "2;5", 2.5)
    hor = PR.valeurs_de_la_liste("horizon", "aucune;20;5", 20.0)
    fiche = dict(FICHES["C5E10-OBS-V1"], sl="sans stop")
    codes = {c.strip() for c in fiche["univers"].split(",")}
    _, m1 = PR.preparer(fiche, dict(vois, sl=dict(vois["sl"], liste="")), "E01", "2026-11-11 22h00 Paris", codes)
    _, m2 = PR.preparer(FICHES["C5E10-OBS-V1"], dict(vois, sl=dict(vois["sl"], liste="2;abc")), "E01", "2026-11-11 22h00 Paris", codes)
    l3, m3 = PR.preparer(fiche, vois, "E01", "2026-11-11 22h00 Paris", codes)
    sl3 = [l for l in l3 if l["parametre"] == "sl"]
    o = (grille, pas, ajout, hor, len(m1), len(m2), m3, sl3[0]["valeur_fiche"] if sl3 else None)
    note("W9 PREPARER : la grille du 19-10, le pas d'avant, la fiche ajoutee, aucune en dernier, deux refus, fiche sans stop + liste",
         o == (["1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "6", "7", "8", "10", "12", "15", "sans stop"],
               [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5], ["2", "2.5", "5"], ["5", "20", "aucune"], 1, 1, [], "sans stop"), o)
essai("W9", w9)

def w10():
    d = tempfile.mkdtemp()
    with contextlib.redirect_stdout(io.StringIO()) as sortie:
        c = PR.main([chemin_du_registre("."), "C5E10-OBS-V1", "donnees/combinatoires/VOISINAGE.csv", "E98", d])
    t = sortie.getvalue()
    import shutil; shutil.rmtree(d, ignore_errors=True)
    note("W10 PREPARER main sur le vrai registre et le vrai voisinage : 5775 versions annoncees", c == 0 and "FABRIQUERA : 5775" in t, (c, t[-200:]))
essai("W10", w10)

def w11():
    n = [DE.normaliser("sl", "Sans Stop"), DE.normaliser("horizon", "aucune"), DE.normaliser("tp", "sans stop"),
         DE.normaliser("sl", "sans_stop"), DE.normaliser("horizon", "aucun"), DE.normaliser("sl", "2.5")]
    ok = (n[0] == (S, "sans stop") and n[1] == (A, "aucune") and n[2] is None and n[3] is None and n[4] is None
          and n[5] == (2.5, "0.025"))
    fiche = dict(FICHES["C5E10-OBS-V1"], sl="sans stop", horizon="aucune")
    j = "Jean-Luc le 11-11-2026"
    lignes = [dict(strategie="C5E10-OBS-V1", essai="E01", parametre=p, valeur_fiche=vf, valeurs_a_essayer=va, unite="",
                   jouable="OUI", raison="", valide_par=j, prepare_le="2026-11-11 22h00 Paris")
              for p, vf, va in (("tp", "4", "4"), ("sl", "sans stop", "2.5;sans stop"), ("horizon", "aucune", "20;aucune"),
                                ("univers", fiche["univers"], fiche["univers"]))]
    codes = {c.strip() for c in fiche["univers"].split(",")}
    motifs = DE.verifier(lignes, fiche, codes)
    cols, vers = DE.decliner(lignes)
    marque = [(v["sl"], v["horizon"]) for v in vers if v["version_de_la_fiche"] == "OUI"]
    note("W11 DECLINER : mots normalises, tp sans stop refuse, mots devines refuses, la version de la fiche reperee",
         ok and motifs == [] and len(vers) == 4 and marque == [("sans stop", "aucune")], (n, motifs, marque))
essai("W11", w11)

def w12():
    class J: pass
    J.pourcent = B.pourcent; J.lire_horizon = B.lire_horizon
    base = {"tp": "0.04", "sl": "sans stop", "horizon": "aucune", "univers": "TTE"}
    e0 = JV.controler_fusion(J, base, dict(base))
    e1 = JV.controler_fusion(J, base, dict(base, sl="0.025"))
    e2 = JV.controler_fusion(J, dict(base, sl="0.025"), dict(base))
    e3 = JV.controler_fusion(J, base, dict(base, horizon="20"))
    e4 = JV.controler_fusion(J, dict(base, sl="0.025", horizon="20"), dict(base, sl="0.025", horizon="20"))
    o = [len(e) for e in (e0, e1, e2, e3, e4)]
    note("W12 controler_fusion : mot contre mot sans ecart, mot contre nombre un ecart", o == [0, 1, 1, 1, 0], (o, e1, e3))
essai("W12", w12)

def w14():
    fautes = []
    for f in ("PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py", "DECLINER_LES_STRATEGIES.py", "JOUER_LES_VERSIONS.py"):
        src = open(os.path.join("programmes", f), encoding="utf-8").read()
        for fn in ast.walk(ast.parse(src)):
            if not isinstance(fn, ast.FunctionDef):
                continue
            seg = ast.get_source_segment(src, fn)
            for n in ast.walk(fn):
                if isinstance(n, ast.Call) and getattr(n.func, "attr", getattr(n.func, "id", "")) == "lire_horizon" \
                        and "HORIZON_AUCUNE" not in seg:
                    fautes.append((f, fn.name, n.lineno))
    note("W14 R-708 : aucune lecture stricte de l'horizon hors d'une fonction qui reconnait HORIZON_AUCUNE", not fautes, fautes)
essai("W14", w14)
def w15():
    # PROPRIÉTÉ « SUIVIE ⇔ RÉGLÉE » (défaut D1, marche du superviseur R-759 du 12-11-2026, point 4) : pour toute fiche
    # du registre et ses mutantes qui passent la porte du laboratoire, le soir la refuse à la lecture (`fiche_suivie`,
    # motif « lecture du soir ») si et seulement si `reglages_du_registre` ne la règle pas. Non vide : les mutantes
    # « sans stop » et « aucune » doivent être refusées, C5E10-QA-V1 réglée.
    import TENIR_LES_POSITIONS as T
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "donnees"))
    src = chemin_du_registre(".")
    lignes = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    champs = list(lignes[0].keys())
    qa = FICHES["C5E10-QA-V1"]
    mutantes = [dict(qa, id="MUT-SANS-STOP", nom="MUT1", sl="sans stop"), dict(qa, id="MUT-AUCUNE", nom="MUT2", horizon="aucune"),
                dict(qa, id="MUT-LES-DEUX", nom="MUT3", sl="Sans Stop", horizon="aucune"),
                dict(qa, id="MUT-SL-ILLISIBLE", nom="MUT4", sl="abc"), dict(qa, id="MUT-TP-SANS-STOP", nom="MUT5", tp="sans stop")]
    w = csv.DictWriter(open(os.path.join(d, "donnees", "cac40_strategies.csv"), "w", encoding="utf-8", newline=""), fieldnames=champs)
    w.writeheader(); w.writerows(lignes + mutantes)
    fiches = fiches_du_registre(os.path.join(d, "donnees", "cac40_strategies.csv"))
    r = T.reglages_du_registre(d)
    mn = B.table_mnemoniques(B.trouver(".", "REFERENTIEL_VALEURS"))
    ecarts, vus = [], {}
    for k, f in fiches.items():
        if not B.porte_0(f)[0]:
            continue
        motif = B.fiche_suivie(d, f, mn)[2] or ""
        refusee = motif.startswith("lecture du soir")
        vus[k] = (refusee, k in r)
        if refusee == (k in r):
            ecarts.append((k, motif[:60], k in r))
    import shutil; shutil.rmtree(d, ignore_errors=True)
    attendu = {"MUT-SANS-STOP": (True, False), "MUT-AUCUNE": (True, False), "MUT-LES-DEUX": (True, False), "C5E10-QA-V1": (False, True)}
    ok = not ecarts and all(vus.get(k) == v for k, v in attendu.items()) and "MUT-TP-SANS-STOP" not in vus and "MUT-SL-ILLISIBLE" not in vus
    note("W15 soir : suivie <=> reglee (porte du laboratoire passee) ; sans stop et aucune refuses par les deux, C5 reglee",
         ok, (ecarts, {k: vus.get(k) for k in attendu}))
essai("W15", w15)

def w17():
    # LE RÉGLAGE DU SOIR (« aucune » au soir, À DÉCIDER) : le fichier du dépôt dit « refuser » ; seul « accepter »
    # ouvre ; un autre mot, une ligne absente, un fichier absent ferment (la valeur la plus stricte).
    o = [B.soir_accepte_aucune(".")]
    for contenu in ("reglage,valeur\nhorizon_aucune_au_soir, Accepter \n", "reglage,valeur\nhorizon_aucune_au_soir,oui\n",
                    "reglage,valeur\nautre,accepter\n", None):
        d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, "donnees"))
        if contenu is not None:
            open(os.path.join(d, "donnees", "REGLAGES_DU_SOIR.csv"), "w", encoding="utf-8").write(contenu)
        o.append(B.soir_accepte_aucune(d))
        import shutil; shutil.rmtree(d, ignore_errors=True)
    lu = [l for l in B.lire_csv("donnees/REGLAGES_DU_SOIR.csv") if l["reglage"] == "horizon_aucune_au_soir"]
    note("W17 reglage du soir : depot « refuser » (A DECIDER) ; seul « accepter » ouvre ; autre mot, ligne ou fichier absents ferment",
         o == [False, True, False, False, False] and len(lu) == 1 and lu[0]["etat"] == "À DÉCIDER", (o, lu))
essai("W17", w17)
print("RESULTATS " + json.dumps(res))
'''


def copie(sab):
    """Fabrique une copie de travail du dépôt, sabotée selon `sab`, et rend son chemin.

    ① RÔLE — Isoler chaque passage : le dépôt n'est jamais modifié.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par sabotage.
    ③ ENTRÉE — `sab` : le nom d'un sabotage de SABOTAGES.
    ④ CONDITIONS D'ENTRÉE — chaque texte « avant » du sabotage figure EXACTEMENT une fois dans son fichier.
    ⑤ SORTIE — UNE valeur : le chemin du dossier temporaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① copier `programmes/` · ② lier `donnees/`, `temoins/`, `gouvernance/` par liens physiques ·
      ③ appliquer chaque remplacement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge cherche ses fichiers par `os.walk`, qui ne suit pas les liens symboliques ; les liens
      physiques ne coûtent aucune place (disque presque plein, cadre commun du 11-11-2026).
    ⑨ CE QUI CLOCHE — voir ⑨ de l'en-tête (liens physiques).
    ⑩ EFFET — crée un dossier temporaire.
    ⑪ TERMINAISON — Rend la main, ou lève LookupError si une cible de sabotage est introuvable ou multiple.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix="vente_reglable_")
    shutil.copytree(os.path.join(DEPOT, "programmes"), os.path.join(d, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    for x in LIES:
        shutil.copytree(os.path.join(DEPOT, x), os.path.join(d, x), copy_function=os.link)
    for f, avant, apres in SABOTAGES[sab]:
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(avant) != 1:
            shutil.rmtree(d, ignore_errors=True)
            raise LookupError("cible du sabotage %s trouvée %d fois dans %s" % (sab, t.count(avant), f))
        os.remove(p)   # jamais réécrire en place : `programmes/` est une vraie copie, mais la règle vaut partout
        open(p, "w", encoding="utf-8").write(t.replace(avant, apres))
    return d


def run(d, *args):
    """Lance Python dans la copie et rend son code et sa sortie.

    ① RÔLE — Un seul chemin de lancement, borné.
    ② CONTEXTE D'APPEL — `epreuves` et `bout_en_bout`.
    ③ ENTRÉE — `d` : la copie · `args` : les arguments de Python.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé), la sortie et l'erreur réunies.
      [rend: 2]
    ⑥ TRAITEMENT — `subprocess.run` avec `-B`, dans `d`, borné à 900 s.
    ⑦ UNITÉ — Des secondes pour le délai.
    ⑧ POURQUOI — Chaque passage voit les modules de SA copie, et rien n'écrit de fichier compilé.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lance un processus.
    ⑪ TERMINAISON — Rend la main ; le processus est borné.
      [sort: non]
    """
    try:
        p = subprocess.run([sys.executable, "-B"] + list(args), cwd=d, capture_output=True, text=True, timeout=900)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, "délai de 900 s dépassé"


def bout_en_bout(d):
    """W13 : JOUER_LES_VERSIONS.py, de bout en bout, sur 4 versions de C5E10-OBS-V1 (stop 2,5 % ou sans stop × 20 ou aucune).

    ① RÔLE — Prouver que la moulinette joue « sans stop » et « aucune » jusqu'au fichier de résultats.
    ② CONTEXTE D'APPEL — `epreuves`, après le sous-processus des autres épreuves.
    ③ ENTRÉE — `d` : la copie.
    ④ CONDITIONS D'ENTRÉE — le registre de la copie porte C5E10-OBS-V1.
    ⑤ SORTIE — UNE valeur : un dictionnaire d'une épreuve, {nom: [vert, détail]}.
      [rend: 1]
    ⑥ TRAITEMENT — ① écrire une combinatoire de 4 versions (la version de la fiche marquée) dans un dossier
      temporaire · ② lancer le programme · ③ exiger le code 0, le calibrage, 4 lignes de résultats et la phrase qui
      DIT la durée « aucune » · ④ lancer le TRI sur ces résultats et exiger le code 0, « VERSIONS ESSAYÉES : 4 », la
      raison « durée « aucune » : embargo non tranché » pour 2 versions, et aucune version « aucune » retenue
      (relecteur neuf E1F phase 2, M-1 : le tri arrêtait tout le fichier sur une version « aucune ») ; exiger que
      les versions chiffrées soient RETENUES, leur nombre et leurs identifiants calculés depuis l'entrée (N-3).
    ⑦ UNITÉ — Gains en euros.
    ⑧ POURQUOI — Les épreuves par import ne prouvent pas que la chaîne réelle tient (le juge lancé seul, la porte 0
      de chaque version, la marge).
    ⑨ CE QUI CLOCHE — Aucun témoin de résultats : les chiffres ne sont pas comparés à une référence, seulement
      produits ; le chiffre de la fiche, lui, est confronté au juge seul par le programme.
    ⑩ EFFET — écrit dans un dossier temporaire, effacé.
    ⑪ TERMINAISON — Rend la main ; le lancement est borné par `run`.
      [sort: non]
    """
    import csv
    t = tempfile.mkdtemp(prefix="vente_reglable_w13_")
    try:
        univers = None
        for l in csv.DictReader(open(os.path.join(d, "donnees", "cac40_strategies.csv"), encoding="utf-8-sig")):
            if l.get("id") == "C5E10-OBS-V1":
                univers = l["univers"]   # la DERNIÈRE ligne fait foi (n°83)
        f_c = os.path.join(t, "COMBINATOIRE_C5E10-OBS-V1_E97.csv")
        cols = ["id_version", "strategie", "essai", "tp", "sl", "horizon", "univers", "versions_dans_l_essai", "version_de_la_fiche"]
        with open(f_c, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            entree = {"C5E10-OBS-V1-E97-%04d" % i: (sl, h) for i, (sl, h) in enumerate(
                (("0.025", "20"), ("0.025", "aucune"), ("sans stop", "20"), ("sans stop", "aucune")), 1)}
            for i, (sl, h) in enumerate(entree.values(), 1):
                w.writerow({"id_version": "C5E10-OBS-V1-E97-%04d" % i, "strategie": "C5E10-OBS-V1", "essai": "E97",
                            "tp": "0.04", "sl": sl, "horizon": h, "univers": univers, "versions_dans_l_essai": "4",
                            "version_de_la_fiche": "OUI" if i == 1 else ""})
        f_r = os.path.join(t, "RESULTATS.csv")
        c, o = run(d, "programmes/JOUER_LES_VERSIONS.py", d, f_c, f_r)
        lignes = list(csv.DictReader(open(f_r, encoding="utf-8"))) if os.path.exists(f_r) else []
        ok = (c == 0 and "CALIBRAGE PAR LE JUGE SEUL : OK" in o and len(lignes) == 4
              and "DURÉE « AUCUNE » : 2 version(s)" in o
              and [(x["sl"], x["horizon"]) for x in lignes][2:] == [("sans stop", "20"), ("sans stop", "aucune")])
        # ④ LE TRI À LA SUITE (M-1) : le fichier de JOUER, tel quel
        f_t = os.path.join(t, "TRI.csv")
        c_t, o_t = run(d, "programmes/TRIER_LES_VARIANTES.py", d, f_t, f_r) if os.path.exists(f_r) else (None, "")
        triees = list(csv.DictReader(open(f_t, encoding="utf-8"))) if os.path.exists(f_t) else []
        # N-3 (relecture Cowork du 14-11-2026, superviseur R-759 E1F) : les versions CHIFFRÉES passent le tri ; leur
        # nombre est CALCULÉ depuis l'entrée de W13 (`entree`), jamais écrit en dur.
        chiffrees = {i for i, (_, h) in entree.items() if h != "aucune"}
        ok_t = (c_t == 0 and "VERSIONS ESSAYÉES : %d (" % len(entree) in o_t
                and "NON MESURABLE — durée « aucune » : embargo non tranché : %d version(s)" % (len(entree) - len(chiffrees)) in o_t
                and "RETENUES : %d " % len(chiffrees) in o_t and {x["id_version"] for x in triees} == chiffrees)
        return {"W13 JOUER_LES_VERSIONS puis TRIER de bout en bout : 4 versions (2,5 % / sans stop x 20 / aucune), "
                "les « aucune » non mesurables": [ok and ok_t, "jouer code %d · %d ligne(s) · tri code %s · %d triee(s) · %s"
                                                  % (c, len(lignes), c_t, len(triees), (o_t or o).strip()[-260:])]}
    finally:
        shutil.rmtree(t, ignore_errors=True)


def juge_a_8(d):
    """W16 : le juge à 8 critères refuse une fiche « sans stop » par son motif nommé, AVANT de la jouer (défaut D3).

    ① RÔLE — Prouver la réparation de D3 sur le vrai programme `programmes/JUGER_SUR_8_CRITERES.py`.
    ② CONTEXTE D'APPEL — `epreuves`, après W13.
    ③ ENTRÉE — `d` : la copie.
    ④ CONDITIONS D'ENTRÉE — la copie porte le registre (lien physique) avec C5E10-QA-V1.
    ⑤ SORTIE — UNE valeur : {nom: [vert, détail]}.
      [rend: 1]
    ⑥ TRAITEMENT — ① REMPLACER le lien physique du registre de la copie par un vrai fichier, où C5E10-QA-V1 porte
      « sans stop » (le registre du dépôt n'est jamais réécrit) · ② lancer le programme sur cette fiche · ③ exiger le
      motif MOTIF_SANS_STOP_NON_JUGEABLE, aucune opération jouée, aucune trace d'erreur.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecteur neuf du 11-11-2026, D3 : la branche jouait 67 opérations sans stop puis tombait sur une
      trace d'erreur ; marche du superviseur R-759 du 12-11-2026, point 5.
    ⑨ CE QUI CLOCHE — Le registre de la copie est modifié en dernier : rien ne le relit ensuite.
    ⑩ EFFET — écrit le registre de la copie (après en avoir retiré le lien).
    ⑪ TERMINAISON — Rend la main ; le lancement est borné par `run`.
      [sort: non]
    """
    import csv
    f_reg = os.path.join(d, "donnees", "cac40_strategies.csv")
    lignes = list(csv.DictReader(open(f_reg, encoding="utf-8-sig")))
    champs = list(lignes[0].keys())
    os.remove(f_reg)   # LE LIEN EST RETIRÉ AVANT L'ÉCRITURE : le registre du dépôt n'est jamais touché
    with open(f_reg, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        w.writerows([dict(l, sl="sans stop") if l.get("id") == "C5E10-QA-V1" else l for l in lignes])
    c, o = run(d, "programmes/JUGER_SUR_8_CRITERES.py", d, "--strategie", "C5E10-QA-V1")
    ok = "NON JUGEABLE — stop « sans stop »" in o and "Traceback" not in o and "opération(s)" not in o
    return {"W16 juge a 8 criteres : sans stop refuse par son motif, avant de jouer, sans trace d'erreur":
            [ok, "code %d · %s" % (c, o.strip()[-220:])]}


def epreuves(sab):
    """Joue toutes les épreuves sur une copie sabotée selon `sab` et rend leurs verdicts.

    ① RÔLE — Un passage complet : W0-W12, W14, W15, W17 dans un sous-processus, puis W13 et W16.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `sab` : le nom du sabotage.
    ④ CONDITIONS D'ENTRÉE — celles de `copie`.
    ⑤ SORTIE — UNE valeur : {nom de l'épreuve: [vert, détail]}.
      [rend: 1]
    ⑥ TRAITEMENT — copier, lancer CODE, lire la ligne « RESULTATS », ajouter W13, effacer la copie.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sous-processus par passage : les modules sabotés ne se mélangent pas aux autres.
    ⑨ CE QUI CLOCHE — Un sous-processus qui tombe avant d'écrire « RESULTATS » rend une seule épreuve rouge, « CODE ».
    ⑩ EFFET — dossiers temporaires, effacés.
    ⑪ TERMINAISON — Rend la main ; lève LookupError par `copie`.
      [sort: non]
    """
    d = copie(sab)
    try:
        c, o = run(d, "-c", CODE)
        ligne = [l for l in o.splitlines() if l.startswith("RESULTATS ")]
        res = json.loads(ligne[-1][10:]) if ligne else {"CODE": [False, o[-400:]]}
        res.update(bout_en_bout(d))
        res.update(juge_a_8(d))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return res


def main():
    """Joue Z0, ou un sabotage nommé, ou tous les sabotages, et rend le code de sortie.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — Le bas de ce fichier.
    ③ ENTRÉE — `sys.argv` (voir USAGE).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque passage : ses rouges ; Z0 doit être tout vert, un sabotage doit faire rougir au moins
      une épreuve.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — affiche une ligne par passage et une par rouge.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
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
                                                 "  <-- ATTENDU : 0 rouge" if sab == "Z0" and rouges else ""), flush=True)
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
