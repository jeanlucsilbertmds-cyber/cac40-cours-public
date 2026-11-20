#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_CORRECTION_UN_JETON_Mer_18-11-2026.py — éprouve la correction des comptes un jeton (A-801) et sa
lecture par la mesure, puis, avec `--saboter`, éprouve les épreuves elles-mêmes.

Simulation uniquement : aucun ordre réel n'est jamais passé.

① RÔLE — Prouver, sur les VRAIES lignes du journal des trades (R-732), que `programmes/CORRIGER_LES_COMPTES_UN_JETON.py`
  retrouve par la règle l'achat EIFFAGE du 21-10-2026 à la place de l'achat ENGIE, que le fichier déposé est son calcul
  à l'octet, que la mesure de la performance compte le remplacement et met de côté la ligne retirée en un jeton, et
  qu'elle ne touche jamais aux jetons illimités ; puis que chaque épreuve rougit quand on retire ce qu'elle garde.
② CONTEXTE D'APPEL — À la main : `python3 tests/EPREUVES_DE_LA_CORRECTION_UN_JETON_Mer_18-11-2026.py <racine>` et
  `... <racine> --saboter`. Aucune tâche ne la lance.
③ ENTRÉE — La racine d'un clone du dépôt (« . » par défaut) ; l'option `--saboter`.
④ CONDITIONS D'ENTRÉE — Le clone porte le commit des signaux du 20-10-2026 (553c2fd2) et le fichier des corrections.
⑤ SORTIE — Un code : 0 si tout est conforme (et, en `--saboter`, si chaque sabotage est mordu), 1 sinon, 2 si
  l'épreuve n'a pas pu tourner (CalculImpossible).
⑥ TRAITEMENT — Lancer les épreuves E1 à E19 sur le dépôt tel quel ; en `--saboter`, pour chaque sabotage S1 à S19,
  appliquer une modification en mémoire du code éprouvé (jamais des fichiers), relancer toutes les épreuves, et exiger
  qu'au moins l'épreuve attendue tombe ; puis rejouer le témoin intact.
⑦ UNITÉ — Euros (textes du journal), dates AAAA-MM-JJ.
⑧ POURQUOI — R-731 et R-732 : un jeu d'épreuves se sabote contre sa propre correction, et un cas au moins vient d'une
  vraie ligne. Les chiffres attendus (3 294,00 € ; cumul un jeton d'OBS 995,50 €) sont des TÉMOINS relevés le
  18-11-2026, non des valeurs que le code lit : E3 recalcule aussi le cumul par la relation « brut − retirée +
  ajoutée ».
⑨ CE QUI CLOCHE — Les sabotages agissent en mémoire, dans ce processus : un sabotage qui ne passerait que par un
  sous-processus ne serait pas vu. E4 lance donc la mesure EN MÉMOIRE (son `main`), pas en sous-processus.
⑩ EFFET — Écrit seulement dans un dossier jetable (`tempfile`), effacé à la fin ; affiche.
⑪ TERMINAISON — Rend un code ; aucun appel qui ne revienne pas (le rejeu s'arrête à la dernière séance).
"""
import contextlib
import csv
import importlib.util
import io
import os
import shutil
import sys
import tempfile

RACINE = os.path.realpath(next((a for a in sys.argv[1:] if not a.startswith("--")), "."))
sys.path.insert(0, os.path.join(RACINE, "programmes"))

import CONTRATS_DES_FICHIERS as C  # noqa: E402
import CORRIGER_LES_COMPTES_UN_JETON as K  # noqa: E402
import TENIR_LES_POSITIONS as T  # noqa: E402
import PUBLIER_LE_SITE as P  # noqa: E402
import glob  # noqa: E402
import subprocess  # noqa: E402

_sp = importlib.util.spec_from_file_location(
    "MESURE_EPREUVE", os.path.join(RACINE, "programmes", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py"))
M = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(M)

JOURNAL = os.path.join(RACINE, "donnees", "claude_journal_trades.csv")
CORR = os.path.join(RACINE, C.CORRECTIONS_UN_JETON)
DECISION = C.CORRECTIONS_UN_JETON_DECIDEES[0]
OBS = DECISION["strategie"]


def _journal():
    """Rend les lignes du VRAI journal, en dictionnaires.

    ① RÔLE — La source des cas réels (R-732). ② CONTEXTE D'APPEL — Les épreuves. ③ ENTRÉE — — ④ CONDITIONS
    D'ENTRÉE — Le journal existe. ⑤ SORTIE — UNE valeur : la liste. [rend: 1] ⑥ TRAITEMENT — `csv.DictReader`.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit un fichier. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    with open(JOURNAL, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _cumul(ops, carte_id, compta):
    """Rend (nombre, cumul) d'une stratégie dans une comptabilité, par le chemin même de la mesure.

    ① RÔLE — Compter comme la mesure. ② CONTEXTE D'APPEL — E3, E5. ③ ENTRÉE — `ops` : des lignes du journal ·
    `carte_id` : l'identifiant de la fiche · `compta` : la comptabilité. ④ CONDITIONS D'ENTRÉE — La fiche existe.
    ⑤ SORTIE — DEUX valeurs : le nombre d'opérations et le cumul arrondi au centime. [rend: 2]
    ⑥ TRAITEMENT — `mesurer_une_strategie` de la mesure, sur la fiche lue au registre. ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — R-708 : ne pas recompter à part. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit le registre.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    carte = C.fiches_du_registre(os.path.join(RACINE, C.REGISTRE_DES_STRATEGIES))[carte_id]
    for _lib, c, s in M.mesurer_une_strategie(ops, carte):
        if c == compta:
            return s["n"], round(s["cumul"], 2)
    raise KeyError(compta)


def e1_rejeu_sur_les_vraies_lignes():
    """E1 — le calcul sur le dépôt réel retire la ligne ENGIE réelle et ajoute EIFFAGE, sans faute.

    ① RÔLE — Le cas réel de R-732. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — Celles du
    programme éprouvé. ⑤ SORTIE — UNE valeur : la liste des écarts (vide = conforme). [rend: 1]
    ⑥ TRAITEMENT — `calculer` ; la retirée égale la ligne du journal ENGIE un jeton du 21-10 champ pour champ ; l'ajoutée
    égale, sur les colonnes chiffrées, la ligne EIFFAGE jetons illimités du journal écrite par le circuit le 02-11.
    ⑦ UNITÉ — — ⑧ POURQUOI — Deux chemins, un résultat. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la
    main. [sort: non]
    """
    ec = []
    lignes, fautes = K.calculer(RACINE)
    if fautes:
        return ["calculer : " + f for f in fautes]
    if [l["geste"] for l in lignes] != [C.GESTE_RETIREE, C.GESTE_AJOUTEE]:
        return ["gestes %r" % [l["geste"] for l in lignes]]
    r, a = lignes
    j = _journal()
    vraie = [l for l in j if l["strategie"] == OBS and l["valeur"] == "ENGIE" and l["comptabilite"] == C.UN_JETON]
    if len(vraie) != 1 or any(vraie[0][c] != r[c] for c in C.TRADE):
        ec.append("la ligne retirée n'est pas la ligne ENGIE un jeton du journal")
    jum = [l for l in j if l["strategie"] == OBS and l["valeur"] == "EIFFAGE" and l["comptabilite"] == C.JETONS_ILLIMITES]
    cols = [c for c in C.TRADE if c not in ("comptabilite", "explication", "regles_pre_trade", "strategie")]
    if len(jum) != 1 or any(jum[0][c] != a[c] for c in cols):
        ec.append("l'ajoutée diffère de la ligne EIFFAGE jetons illimités du journal")
    if (a["valeur"], a["pnl_net_eur"], a["bareme_reel"], a["comptabilite"]) != ("EIFFAGE", "3294.00", "REEL", C.UN_JETON):
        ec.append("témoin du 18-11-2026 : %r" % ((a["valeur"], a["pnl_net_eur"], a["bareme_reel"], a["comptabilite"]),))
    return ec


def e2_le_fichier_depose_est_le_calcul():
    """E2 — `--verifier` rend 0 sur le dépôt, et 1 sur une copie du fichier modifiée d'un centime.

    ① RÔLE — Le fichier déposé n'est pas écrit à la main (R-728). ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Le fichier existe. ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — `main`
    avec `--verifier` ; puis le même sur une copie jetable où « 3294.00 » devient « 3294.01 », le chemin du fichier
    étant détourné vers la copie. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit une copie jetable.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    ec = []
    with contextlib.redirect_stdout(io.StringIO()):
        rc = K.main([RACINE, "--verifier"])
    if rc != 0:
        ec.append("--verifier rend %d sur le dépôt" % rc)
    d = tempfile.mkdtemp(prefix="corr_e2_")
    try:
        faux = os.path.join(d, "corr.csv")
        with open(CORR, encoding="utf-8") as f:
            texte = f.read()
        with open(faux, "w", encoding="utf-8") as f:
            f.write(texte.replace("3294.00", "3294.01", 1))
        ancien = C.CORRECTIONS_UN_JETON
        C.CORRECTIONS_UN_JETON = faux          # os.path.join(racine, chemin absolu) rend le chemin absolu
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc2 = K.main([RACINE, "--verifier"])
                rc3 = K.main([RACINE])           # sans --verifier : un fichier qui diffère n'est jamais écrasé
            with open(faux, encoding="utf-8") as f:
                garde = f.read()
        finally:
            C.CORRECTIONS_UN_JETON = ancien
        if rc2 != 1:
            ec.append("--verifier rend %d sur un fichier modifié d'un centime (attendu 1)" % rc2)
        if rc3 != 1 or garde == texte:
            ec.append("l'écriture a écrasé un fichier qui différait (code %d)" % rc3)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return ec


def e3_la_mesure_compte_le_remplacement():
    """E3 — après correction : OBS un jeton = brut − retirée + ajoutée (témoin 995,50 €) ; jetons illimités et QA intacts.

    ① RÔLE — La propriété comptable. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — `appliquer_les_corrections_un_jeton` sur le vrai
    journal ; compter par `mesurer_une_strategie`. ⑦ UNITÉ — Euros. ⑧ POURQUOI — Deux comptabilités, jamais mêlées.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    ec = []
    brut = _journal()
    corr, ret, aj, so = C.appliquer_les_corrections_un_jeton(brut, CORR, True)
    if so:
        ec.append("sans objet sur le vrai journal : %r" % so)
    if len(corr) != len(brut):
        ec.append("le nombre d'opérations change : %d → %d" % (len(brut), len(corr)))
    nb, cb = _cumul(brut, OBS, C.UN_JETON)
    nc, cc = _cumul(corr, OBS, C.UN_JETON)
    attendu = round(cb - float(ret[0]["pnl_net_eur"]) + float(aj[0]["pnl_net_eur"]), 2) if ret and aj else None
    if (nc, cc) != (nb, attendu) or cc != 995.50:
        ec.append("OBS un jeton : %d · %.2f ; attendu %d · %r (témoin 995.50)" % (nc, cc, nb, attendu))
    for sid, compta in ((OBS, C.JETONS_ILLIMITES), ("C5E10-QA-V1", C.UN_JETON), ("C5E10-QA-V1", C.JETONS_ILLIMITES)):
        if _cumul(brut, sid, compta) != _cumul(corr, sid, compta):
            ec.append("%s %s a changé" % (sid, compta))
    if [o for o in corr if o.get("comptabilite") == C.JETONS_ILLIMITES] != \
       [o for o in brut if o.get("comptabilite") == C.JETONS_ILLIMITES]:
        ec.append("une ligne des jetons illimités a changé")
    return ec


def e4_la_mesure_du_soir_l_ecrit():
    """E4 — le `main` de la mesure, en mémoire, écrit « OBS · un jeton : 4 operation(s) · cumul 995.50 » et la correction.

    ① RÔLE — Le chemin du soir, pas une fonction isolée. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — `M.main` avec un dossier de sortie jetable ; lire ce
    qu'il affiche. ⑦ UNITÉ — — ⑧ POURQUOI — Un appel oublié dans `main` laisserait E3 vert. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit l'historique dans un dossier jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="corr_e4_")
    os.makedirs(os.path.join(d, "donnees"))
    argv = sys.argv
    sys.argv = ["mesure", RACINE, d]
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rc = M.main()
    finally:
        sys.argv = argv
        shutil.rmtree(d, ignore_errors=True)
    t = out.getvalue()
    ec = []
    if rc != 0:
        ec.append("la mesure rend %d : %s" % (rc, t[-300:]))
    if "%s · un jeton : 4 operation(s) · cumul 995.50 EUR" % OBS not in t:
        ec.append("ligne OBS un jeton absente ou fausse")
    if "%s · jetons illimites : 7 operation(s) · cumul 11677.50 EUR" % OBS not in t:
        ec.append("ligne OBS jetons illimités absente ou changée")
    if "CORRECTION A-801 (un jeton)" not in t:
        ec.append("la correction n'est pas dite")
    if "SANS OBJET" in t:
        ec.append("la correction est dite sans objet sur le vrai journal")
    return ec


def _journal_modifie(transforme):
    """Écrit une copie jetable du VRAI journal, ses lignes de texte transformées ; rend (opérations, chemin, dossier).

    ① RÔLE — Éprouver la correction sur un journal réel retouché, octets compris (le début du journal est haché).
    ② CONTEXTE D'APPEL — E5, E10, E11, E12. ③ ENTRÉE — `transforme` : fonction liste de lignes (octets) → liste.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — TROIS valeurs : les opérations lues, le chemin, le dossier à effacer.
    [rend: 3] ⑥ TRAITEMENT — Lire, transformer, écrire, relire en dictionnaires. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans un dossier jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="corr_j_")
    ch = os.path.join(d, "claude_journal_trades.csv")
    with open(JOURNAL, "rb") as f:
        lignes = f.read().splitlines(keepends=True)
    with open(ch, "wb") as f:
        f.write(b"".join(transforme(lignes)))
    with open(ch, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f)), ch, d


def _est_engie_un_jeton(l):
    """Dit si une ligne de texte du journal est l'achat ENGIE un jeton d'OBS. [rend: 1] [sort: non]"""
    return l.startswith((OBS + ",ENGIE,").encode()) and b",un_jeton," in l


def _essayer(transforme, vrai=True):
    """Applique la correction sur un journal retouché (`vrai` : le vrai journal de la racine) ; rend (levée ?, rendu
    ou None). [rend: 2] [sort: non]"""
    ops, ch, d = _journal_modifie(transforme)
    try:
        return False, C.appliquer_les_corrections_un_jeton(ops, CORR, vrai)
    except C.CorrectionUnJetonImpossible:
        return True, None
    finally:
        shutil.rmtree(d, ignore_errors=True)


def e5_un_journal_change_arrete():
    """E5 — si la ligne ENGIE du vrai journal change d'un centime, la correction lève au lieu de corriger de travers.

    ① RÔLE — La comparaison champ pour champ. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Copie jetable du vrai journal, prix d'entrée d'ENGIE
    un jeton changé (le début du journal reste le même) ; appliquer. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, _r = _essayer(lambda ls: [l.replace(b"22.90000", b"22.90001", 1) if _est_engie_un_jeton(l) else l for l in ls])
    return [] if leve else ["un journal changé sous la correction est corrigé quand même"]


def e6_fichier_absent_arrete():
    """E6 — une décision déclarée sans fichier de corrections lève ; la mesure s'arrêterait.

    ① RÔLE — Pas de saut silencieux. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Appliquer avec un chemin None. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        C.appliquer_les_corrections_un_jeton(_journal(), None, True)
    except C.CorrectionUnJetonImpossible:
        return []
    return ["fichier absent : aucune levée"]


def e7_jamais_les_jetons_illimites():
    """E7 — une ligne de correction en jetons illimités est refusée.

    ① RÔLE — Les jetons illimités ne se corrigent jamais. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Copie jetable du fichier,
    « un_jeton » de la ligne retirée remplacé par « jetons_illimites ». ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE —
    — ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="corr_e7_")
    try:
        faux = os.path.join(d, "c.csv")
        with open(CORR, encoding="utf-8") as f:
            texte = f.read()
        with open(faux, "w", encoding="utf-8") as f:
            f.write(texte.replace(",un_jeton,", ",jetons_illimites,", 1))
        try:
            C.appliquer_les_corrections_un_jeton(_journal(), faux, True)
        except C.CorrectionUnJetonImpossible:
            return []
        return ["une correction en jetons illimités est acceptée"]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def e8_la_suite_des_comptes_est_gardee():
    """E8 — un achat un jeton d'OBS pendant la position de remplacement fait refuser la correction.

    ① RÔLE — L'effet en chaîne d'A-801, recalculé. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Rejeu réel ; journal en
    mémoire augmenté d'un achat un jeton OBS le 2026-10-30 ; `confronter`. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI
    CLOCHE — — ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    trades, _inc, _ouv = K.rejouer_la_decision(RACINE, DECISION)
    j = _journal()
    _r, _a, f0 = K.confronter(DECISION, j, [], trades)
    if f0:
        return ["le vrai journal est refusé : %r" % f0]
    ajout = dict(j[-1], valeur="AIRBUS", date_entree="2026-10-30", comptabilite=C.UN_JETON, strategie=OBS)
    _r, _a, f = K.confronter(DECISION, j + [ajout], [], trades)
    return [] if any("pendant la position de remplacement" in x for x in f) else ["achat pendant le remplacement accepté"]


def e9_la_decision_doit_etre_la_regle():
    """E9 — une décision qui nommerait ENGIE est refusée : la règle donne EIFFAGE.

    ① RÔLE — Une décision mal recopiée ne s'applique jamais. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Rejeu réel ; décision copiée
    avec `valeur_nommee_par_la_decision` = ENGIE ; `confronter`. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    trades, _inc, _ouv = K.rejouer_la_decision(RACINE, DECISION)
    d = dict(DECISION, valeur_nommee_par_la_decision="ENGIE")
    _r, _a, f = K.confronter(d, _journal(), [], trades)
    return [] if any("la règle donne EIFFAGE" in x for x in f) else ["décision contraire à la règle acceptée : %r" % f]


def e10_un_autre_journal_est_sans_objet():
    """E10 — un journal fabriqué qui ne commence pas comme le vrai (cas E20 du barème des frais) : sans objet.

    ① RÔLE — Ne pas arrêter les épreuves qui fabriquent leur journal. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Comme E20 : l'en-tête, la
    ligne Bureau Veritas, puis une ligne fabriquée (Unibail changée en Airbus) ; appliquer. ⑦ UNITÉ — —
    ⑧ POURQUOI — Un autre journal n'est pas un journal changé (superviseur R-759, D1, D2 (a) : seulement hors du
    vrai journal de la racine). ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, r = _essayer(lambda ls: ls[:2] + [ls[2].replace(b"UNIBAIL_RODAMCO", b"AIRBUS")], vrai=False)
    if leve:
        return ["un autre journal arrête la mesure"]
    corr, ret, aj, so = r
    if ret or aj or so != ["A-801"]:
        return ["sans objet mal rendu : %d retirée(s), %d ajoutée(s), sans objet %r" % (len(ret), len(aj), so)]
    return []


def e11_un_trade_en_double_arrete():
    """E11 — la ligne ENGIE un jeton écrite une seconde fois en fin de journal arrête la correction.

    ① RÔLE — Une seule ligne par trade. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Copie jetable, ligne recopiée à la fin. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, _r = _essayer(lambda ls: ls + [l for l in ls if _est_engie_un_jeton(l)])
    return [] if leve else ["trade en double accepté"]


def e12_ligne_engie_effacee_arrete():
    """E12 — la ligne ENGIE un jeton EFFACÉE du vrai journal, son jumeau en jetons illimités restant : ARRÊT.

    ① RÔLE — Le cas que la première forme de D1 laissait passer en « sans objet » (superviseur R-759, 18-11-2026).
    ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts.
    [rend: 1] ⑥ TRAITEMENT — Copie jetable sans la ligne ENGIE un jeton ; appliquer. ⑦ UNITÉ — —
    ⑧ POURQUOI — Sinon la mesure ne compterait ni ENGIE ni EIFFAGE, dans un pas vert. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, _r = _essayer(lambda ls: [l for l in ls if not _est_engie_un_jeton(l)])
    return [] if leve else ["ligne ENGIE effacée du vrai journal : aucun arrêt"]


def e13_le_cockpit_dit_la_ligne_retiree():
    """E13 — le cockpit, fabriqué comme la publication le fabrique, dit sous ENGIE qu'elle est retirée et ce qui compte.

    ① RÔLE — Le point 1 du superviseur R-759 (18-11-2026) : la liste ne doit pas contredire la synthèse en silence.
    ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts.
    [rend: 1] ⑥ TRAITEMENT — Copier les entrées de `PUBLIER_LE_SITE.ENTREES` (et le golden, les signaux) dans un
    dossier jetable, lancer le générateur du cockpit en sous-processus, lire la page. ⑦ UNITÉ — —
    ⑧ POURQUOI — La publication copie une liste FIXE de fichiers : un fichier oublié dans cette liste ne serait
    jamais vu du cockpit. ⑨ CE QUI CLOCHE — Le générateur tourne en sous-processus : un sabotage en mémoire du
    générateur ne serait pas vu (seul celui de la liste des entrées l'est). ⑩ EFFET — Écrit dans un dossier jetable.
    ⑪ TERMINAISON — Rend la main ; délai de 600 s pour le générateur. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="corr_e13_")
    try:
        for src, dst in P.ENTREES:
            if os.path.isfile(os.path.join(RACINE, src)):
                shutil.copy(os.path.join(RACINE, src), os.path.join(d, dst))
        for g in glob.glob(os.path.join(RACINE, "gouvernance", "golden_tests_*.json")):
            shutil.copy(g, d)
        shutil.copy(os.path.join(RACINE, "donnees", "signaux_du_jour.json"), d)
        gen = os.path.join(RACINE, "programmes", P.GENERATEUR)
        r = subprocess.run([sys.executable, gen, d, d], capture_output=True, text=True, timeout=600)
        pages = sorted(glob.glob(os.path.join(d, "cockpit_*.html")))
        if r.returncode != 0 or not pages:
            return ["cockpit non fabriqué (code %d) : %s" % (r.returncode, r.stdout[-200:] + r.stderr[-200:])]
        with open(pages[-1], encoding="utf-8") as f:
            page = f.read()
        mot = "RETIREE DES COMPTES UN JETON (A-801), ligne gardee au journal — comptee a sa place : EIFFAGE"
        return [] if page.count(mot) == 1 else ["la page dit %d fois la ligne retirée (attendu 1)" % page.count(mot)]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def e14_vrai_journal_sans_les_deux_lignes_arrete():
    """E14 — le vrai journal (il couvre le 21-10) privé des DEUX lignes ENGIE d'OBS : ARRÊT, jamais « sans objet ».

    ① RÔLE — Le cas (a) du superviseur R-759 du 18-11-2026 (D2). ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Copie jetable sans les
    deux lignes ; appliquer comme vrai journal. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit une
    copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, _r = _essayer(lambda ls: [l for l in ls if not l.startswith((OBS + ",ENGIE,").encode())])
    return [] if leve else ["vrai journal sans aucune des deux lignes ENGIE : aucun arrêt"]


def e15_explication_annotee_correction_appliquee():
    """E15 — une note ajoutée à l'explication de la ligne ENGIE un jeton : la correction s'applique toujours.

    ① RÔLE — Le cas (b) du superviseur : seuls les champs de la décision se comparent. ② CONTEXTE D'APPEL —
    `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1]
    ⑥ TRAITEMENT — Copie jetable, explication vide de la ligne ENGIE un jeton remplacée par une note. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, r = _essayer(lambda ls: [l.replace(b",un_jeton,,,", b",un_jeton,,note de relecture,", 1)
                                   if _est_engie_un_jeton(l) else l for l in ls])
    if leve:
        return ["une note dans l'explication arrête la correction"]
    corr, ret, aj, so = r
    if len(ret) != 1 or so or not any(o.get("valeur") == "EIFFAGE" and o.get("comptabilite") == C.UN_JETON
                                      and o.get("strategie") == OBS for o in corr):
        return ["correction non appliquée : %d retirée(s), sans objet %r" % (len(ret), so)]
    return []


def e16_note_a_la_ligne_8_rien_ne_change():
    """E16 — une note ajoutée à la ligne 8 du vrai journal (une AUTRE ligne) : la correction est la même.

    ① RÔLE — Le défaut D2 de la relecture du 18-11-2026 : l'empreinte des 8 premières lignes changeait, la correction
    devenait « sans objet » et ENGIE était recomptée. ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1] ⑥ TRAITEMENT — Copie jetable, explication de la ligne 8
    annotée ; comparer cumuls et lignes retirées au vrai journal. ⑦ UNITÉ — Euros. ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    def annoter(ls):
        ls = list(ls)
        ls[7] = ls[7].replace(b",HIST_COURTAGE_SANS_TTF,HIST_COURTAGE_SANS_TTF", b"note,HIST_COURTAGE_SANS_TTF,HIST_COURTAGE_SANS_TTF", 1)
        return ls
    ops, ch, d = _journal_modifie(annoter)
    try:
        if ops[6] == _journal()[6]:
            return ["la ligne 8 n'a pas été annotée"]
        r1 = C.appliquer_les_corrections_un_jeton(ops, CORR, True)
    except C.CorrectionUnJetonImpossible as e:
        return ["note à la ligne 8 : arrêt %s" % e]
    finally:
        shutil.rmtree(d, ignore_errors=True)
    r0 = C.appliquer_les_corrections_un_jeton(_journal(), CORR, True)
    if (len(r1[1]), r1[3]) != (len(r0[1]), r0[3]) or _cumul(r1[0], OBS, C.UN_JETON) != _cumul(r0[0], OBS, C.UN_JETON):
        return ["note à la ligne 8 : correction changée (%d retirée(s), sans objet %r, %r)"
                % (len(r1[1]), r1[3], _cumul(r1[0], OBS, C.UN_JETON))]
    return []


def e17_deux_journaux_arretent():
    """E17 — un journal parasite à plat à la racine d'une copie, le vrai restant dans donnees/ : la mesure ARRÊTE.

    ① RÔLE — La garde « deux journaux » du superviseur R-759 (18-11-2026, arbitrage d'E20). ② CONTEXTE D'APPEL —
    `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1]
    ⑥ TRAITEMENT — Copie par liens durs de donnees/, programmes/, gouvernance/, temoins/ ; `journal_trades.csv` écrit
    à la racine (le vrai journal recopié) ; `main` de la mesure, en mémoire, sur cette racine. ⑦ UNITÉ — —
    ⑧ POURQUOI — `_p` cherche d'abord à plat : le parasite serait lu à la place du vrai, `vrai_journal` vaudrait
    faux, et ENGIE serait recomptée. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans un dossier jetable (fichiers liés,
    jamais réécrits). ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="corr_e17_")
    argv = sys.argv
    try:
        for rep_ in ("donnees", "programmes", "gouvernance", "temoins"):
            shutil.copytree(os.path.join(RACINE, rep_), os.path.join(d, rep_), copy_function=os.link,
                            ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(JOURNAL, os.path.join(d, "journal_trades.csv"))
        sortie = os.path.join(d, "_sortie")
        os.makedirs(os.path.join(sortie, "donnees"))
        sys.argv = ["mesure", d, sortie]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = M.main()
    finally:
        sys.argv = argv
        shutil.rmtree(d, ignore_errors=True)
    return [] if rc == 1 and "deux journaux" in out.getvalue() else [
        "journal parasite à la racine : code %r, pas d'arrêt « deux journaux »" % rc]


def e18_journal_anterieur_sans_objet():
    """E18 — le vrai journal ARRÊTÉ au 20-10-2026 (huit premières lignes, sans ENGIE) : la correction est sans objet.

    ① RÔLE — Le cas du témoin figé du 27-09-2026 d'EPREUVES_DES_COMPTABILITES (superviseur R-759, option B).
    ② CONTEXTE D'APPEL — `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts.
    [rend: 1] ⑥ TRAITEMENT — Copie jetable réduite à l'en-tête et aux sept premiers trades (dernière date 2026-10-20) ;
    appliquer comme vrai journal. ⑦ UNITÉ — — ⑧ POURQUOI — Un journal qui s'arrête avant le trade corrigé ne peut
    pas le porter. ⑨ CE QUI CLOCHE — Ce que cette épreuve fige est une LIMITE ADMISE, pas un vœu (superviseur R-759 du
    18-11-2026 à 16h22, sur N1 du relecteur du tour 5) : le même « sans objet » vaut pour le VRAI journal du jour
    tronqué avant le 21-10 ou vidé — code 0, simple ALERTE, une perte de lignes passe sans arrêt. Le remède n'est pas
    dans la correction : action BACKLOG « garde : le journal des trades ne perd aucune ligne » (A-908, consignée le 18-11-2026).
    ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    leve, r = _essayer(lambda ls: ls[:8])
    if leve:
        return ["journal arrêté avant le 21-10 : arrêt"]
    corr, ret, aj, so = r
    return [] if (not ret and so == ["A-801"]) else ["sans objet mal rendu : %d retirée(s), %r" % (len(ret), so)]


def e19_date_illisible_arrete():
    """E19 — sans les deux lignes ENGIE, une date de vente VIDE au journal fait arrêter (la couverture ne se calcule pas).

    ① RÔLE — La condition ① du superviseur : « une date illisible ou vide fait ARRÊTER ». ② CONTEXTE D'APPEL —
    `epreuves`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les écarts. [rend: 1]
    ⑥ TRAITEMENT — Copie jetable : journal arrêté au 20-10 (huit lignes), date de vente de Bureau Veritas vidée.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit une copie jetable. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    leve, _r = _essayer(lambda ls: [ls[0], ls[1].replace(b",2026-07-29,", b",,", 1)] + ls[2:8])
    return [] if leve else ["date vide acceptée"]


EPREUVES = [e1_rejeu_sur_les_vraies_lignes, e2_le_fichier_depose_est_le_calcul, e3_la_mesure_compte_le_remplacement,
            e4_la_mesure_du_soir_l_ecrit, e5_un_journal_change_arrete, e6_fichier_absent_arrete,
            e7_jamais_les_jetons_illimites, e8_la_suite_des_comptes_est_gardee, e9_la_decision_doit_etre_la_regle,
            e10_un_autre_journal_est_sans_objet, e11_un_trade_en_double_arrete, e12_ligne_engie_effacee_arrete,
            e13_le_cockpit_dit_la_ligne_retiree, e14_vrai_journal_sans_les_deux_lignes_arrete,
            e15_explication_annotee_correction_appliquee, e16_note_a_la_ligne_8_rien_ne_change,
            e17_deux_journaux_arretent, e18_journal_anterieur_sans_objet, e19_date_illisible_arrete]


def epreuves():
    """Lance toutes les épreuves ; rend {nom: écarts}.

    ① RÔLE — Un passage complet. ② CONTEXTE D'APPEL — `main`, et chaque sabotage. ③ ENTRÉE — — ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le dictionnaire. [rend: 1] ⑥ TRAITEMENT — Chaque épreuve ; une exception
    est un écart. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — `CalculImpossible` est un écart ici, pas un code 2 :
    `main` le relance avant pour le distinguer. ⑩ EFFET — Celui des épreuves. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    rendu = {}
    for e in EPREUVES:
        try:
            rendu[e.__name__] = e()
        except Exception as x:  # un sabotage peut faire lever : c'est une morsure, dite
            rendu[e.__name__] = ["%s : %s" % (type(x).__name__, x)]
    return rendu


@contextlib.contextmanager
def _remplace(objet, nom, valeur):
    """Remplace un attribut le temps d'un bloc, puis le remet.

    ① RÔLE — Saboter en mémoire. ② CONTEXTE D'APPEL — Les sabotages. ③ ENTRÉE — `objet`, `nom`, `valeur`.
    ④ CONDITIONS D'ENTRÉE — L'attribut existe. ⑤ SORTIE — — ⑥ TRAITEMENT — setattr, puis remise dans `finally`.
    ⑦ UNITÉ — — ⑧ POURQUOI — Aucun fichier du dépôt n'est modifié. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Modifie un module
    le temps du bloc. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    ancien = getattr(objet, nom)
    setattr(objet, nom, valeur)
    try:
        yield
    finally:
        setattr(objet, nom, ancien)


def _ne_corrige_rien(ops, chemin, vrai):
    """Sabotage S1 : la correction rend le journal tel quel. [rend: 4] [sort: non]"""
    return list(ops), [], [], []


def _corrige_par_valeur_et_date(ops, chemin, vrai):
    """Sabotage S4 : la ligne retirée se retrouve par valeur et date seulement. [rend: 4] [sort: non]"""
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    r = [l for l in lignes if l["geste"] == C.GESTE_RETIREE][0]
    a = [l for l in lignes if l["geste"] == C.GESTE_AJOUTEE][0]
    out = list(ops)
    for i, o in enumerate(out):
        if (o["valeur"], o["date_entree"], o["comptabilite"]) == (r["valeur"], r["date_entree"], r["comptabilite"]):
            out[i] = {c: a[c] for c in C.TRADE}
    return out, [r], [a], []


def _corrige_les_deux_comptabilites(ops, chemin, vrai):
    """Sabotage S5 : la correction s'applique aussi aux jetons illimités. [rend: 4] [sort: non]"""
    out, r, a, so = _ORIGINAL_APPLIQUER(ops, chemin, vrai)
    for i, o in enumerate(out):
        if o["valeur"] == "ENGIE" and o["strategie"] == OBS and o["comptabilite"] == C.JETONS_ILLIMITES:
            out[i] = dict(a[0], comptabilite=C.JETONS_ILLIMITES)
            out[i] = {c: out[i][c] for c in C.TRADE}
    return out, r, a, so


def _change_dit_sans_objet(ops, chemin, vrai):
    """Sabotage S9 : un trade présent mais différent est dit « sans objet » au lieu d'arrêter. [rend: 4] [sort: non]"""
    try:
        return _ORIGINAL_APPLIQUER(ops, chemin, vrai)
    except C.CorrectionUnJetonImpossible:
        return list(ops), [], [], ["A-801"]


def _absent_arrete(ops, chemin, vrai):
    """Sabotage S10 : un trade absent arrête, comme avant le 18-11-2026 à 15h. [rend: 4] [sort: non]"""
    r = _ORIGINAL_APPLIQUER(ops, chemin, vrai)
    if r[3]:
        raise C.CorrectionUnJetonImpossible("absent : %r" % r[3])
    return r


def _absence_dit_sans_objet(ops, chemin, vrai):
    """Sabotage S11 : la première forme de D1 — trade absent = sans objet, sans regarder le début. [rend: 4] [sort: non]"""
    if not any(o.get("strategie") == OBS and o.get("valeur") == "ENGIE" and o.get("comptabilite") == C.UN_JETON
               for o in ops):
        return list(ops), [], [], ["A-801"]
    return _ORIGINAL_APPLIQUER(ops, chemin, vrai)


def _vrai_journal_ignore(ops, chemin, vrai):
    """Sabotage S13 : le vrai journal traité comme un autre (les deux lignes manquent → sans objet). [rend: 4]
    [sort: non]"""
    return _ORIGINAL_APPLIQUER(ops, chemin, False)


@contextlib.contextmanager
def _compare_tout():
    """Sabotage S14 : la comparaison porte sur toutes les colonnes TRADE, explication comprise. [sort: non]"""
    ancien = DECISION["champs_compares"]
    DECISION["champs_compares"] = tuple(C.TRADE)
    try:
        yield
    finally:
        DECISION["champs_compares"] = ancien


def _debut_hache(ops, chemin, vrai):
    """Sabotage S15 : la forme du tour 2 — un début de journal différent du vrai rend la correction sans objet.
    [rend: 4] [sort: non]"""
    vrais = _journal()
    if any(a != b for a, b in zip(ops[:7], vrais[:7])):
        return list(ops), [], [], ["A-801"]
    return _ORIGINAL_APPLIQUER(ops, chemin, vrai)


def _module_au_bareme_historique(chemin):
    """Sabotage S6 : le moteur des positions chiffre au barème historique sans taxe. [rend: 1] [sort: non]"""
    m = _ORIGINAL_CHARGER(chemin)
    m.BAREME_PAR_DEFAUT = "HIST_COURTAGE_SANS_TTF"
    return m


def _confronter_sans_la_suite(decision, journal, positions_ouvertes, trades):
    """Sabotage S3 : la confrontation oublie l'effet en chaîne (journal réduit à la retirée). [rend: 3] [sort: non]"""
    garde = [l for l in journal if l.get("valeur") == decision["valeur_retiree"] or l.get("comptabilite") != C.UN_JETON]
    return _ORIGINAL_CONFRONTER(decision, garde, [], trades)


_ORIGINAL_APPLIQUER = C.appliquer_les_corrections_un_jeton
_ORIGINAL_COUVRE = C.journal_couvre
_ORIGINAL_CHARGER = T.charger_module_positions
_ORIGINAL_CONFRONTER = K.confronter

# (nom, ce qu'il retire, la fabrique du bloc, l'épreuve qui doit tomber au moins)
SABOTAGES = [
    ("S1_la_mesure_ne_corrige_rien", lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _ne_corrige_rien),
     "e3_la_mesure_compte_le_remplacement"),
    ("S2_plus_de_departage_R207bis", lambda: _remplace(T, "departager_r207bis", lambda s: list(s)),
     "e1_rejeu_sur_les_vraies_lignes"),
    ("S3_confronter_oublie_la_suite", lambda: _remplace(K, "confronter", _confronter_sans_la_suite),
     "e8_la_suite_des_comptes_est_gardee"),
    ("S4_ligne_retrouvee_par_valeur_et_date",
     lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _corrige_par_valeur_et_date),
     "e5_un_journal_change_arrete"),
    ("S5_corrige_aussi_les_jetons_illimites",
     lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _corrige_les_deux_comptabilites),
     "e3_la_mesure_compte_le_remplacement"),
    ("S6_frais_au_bareme_historique", lambda: _remplace(T, "charger_module_positions", _module_au_bareme_historique),
     "e1_rejeu_sur_les_vraies_lignes"),
    ("S7_verifier_toujours_vert",
     lambda: _remplace(K, "en_texte", lambda lignes: open(os.path.join(RACINE, C.CORRECTIONS_UN_JETON),
                                                          encoding="utf-8").read()),
     "e2_le_fichier_depose_est_le_calcul"),
    ("S9_un_journal_change_dit_sans_objet",
     lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _change_dit_sans_objet),
     "e5_un_journal_change_arrete"),
    ("S10_un_autre_journal_arrete",
     lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _absent_arrete),
     "e10_un_autre_journal_est_sans_objet"),
    ("S11_ligne_engie_effacee_dite_sans_objet",
     lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _absence_dit_sans_objet),
     "e12_ligne_engie_effacee_arrete"),
    ("S13_vrai_journal_traite_comme_un_autre",
     lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _vrai_journal_ignore),
     "e14_vrai_journal_sans_les_deux_lignes_arrete"),
    ("S14_explication_comparee", _compare_tout, "e15_explication_annotee_correction_appliquee"),
    ("S15_debut_du_journal_hache", lambda: _remplace(C, "appliquer_les_corrections_un_jeton", _debut_hache),
     "e16_note_a_la_ligne_8_rien_ne_change"),
    ("S16_plus_de_garde_deux_journaux",
     lambda: _remplace(sys.modules[__name__], "M", _mesure_modifiee(
         "if os.path.isfile(_vrai) and os.path.realpath(ch) != os.path.realpath(_vrai):", "if False:")),
     "e17_deux_journaux_arretent"),
    ("S17_couverture_toujours_fausse", lambda: _remplace(C, "journal_couvre", lambda ops, d: False),
     "e14_vrai_journal_sans_les_deux_lignes_arrete"),
    ("S18_couverture_toujours_vraie", lambda: _remplace(C, "journal_couvre", lambda ops, d: True),
     "e18_journal_anterieur_sans_objet"),
    ("S19_date_illisible_toleree", lambda: _remplace(C, "journal_couvre", _couvre_en_tolerant),
     "e19_date_illisible_arrete"),
    ("S12_la_publication_oublie_les_corrections",
     lambda: _remplace(P, "ENTREES", [e for e in P.ENTREES if e[0] != C.CORRECTIONS_UN_JETON]),
     "e13_le_cockpit_dit_la_ligne_retiree"),
    ("S8_la_mesure_n_appelle_plus_la_correction",
     lambda: _remplace(sys.modules[__name__], "M", _mesure_sans_correction()),
     "e4_la_mesure_du_soir_l_ecrit"),
]


def _couvre_en_tolerant(operations, date_de_reference):
    """Sabotage S19 : la couverture saute les dates vides ou illisibles au lieu d'arrêter. [rend: 1] [sort: non]"""
    ok = [o for o in operations if len(o.get("date_entree") or "") == 10 and len(o.get("date_sortie") or "") == 10]
    return _ORIGINAL_COUVRE(ok, date_de_reference)


def _mesure_modifiee(avant, apres):
    """Rend la mesure du soir chargée depuis son texte où `avant` (présent une fois) devient `apres`.

    ① RÔLE — Saboter le code même de la mesure sans toucher au fichier. ② CONTEXTE D'APPEL — S16.
    ③ ENTRÉE — `avant`, `apres` : deux textes. ④ CONDITIONS D'ENTRÉE — `avant` est présent une fois. ⑤ SORTIE — UNE
    valeur : un module. [rend: 1] ⑥ TRAITEMENT — Lire, remplacer, exécuter comme module. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun fichier écrit. ⑪ TERMINAISON — Rend la main ; lève ValueError sinon.
    [sort: non]
    """
    import types
    chemin = os.path.join(RACINE, "programmes", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py")
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    if texte.count(avant) != 1:
        raise ValueError("texte à saboter introuvable dans la mesure : %r" % avant)
    m = types.ModuleType("MESURE_MODIFIEE")
    m.__file__ = chemin
    exec(compile(texte.replace(avant, apres), chemin, "exec"), m.__dict__)
    return m


def _mesure_sans_correction():
    """Sabotage S8 : la mesure du soir, son appel à la correction remplacé par « rien ».

    ① RÔLE — Retirer l'appel dans le code même de la mesure, sans toucher au fichier. ② CONTEXTE D'APPEL — S8.
    ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — La ligne de l'appel est présente une fois. ⑤ SORTIE — UNE valeur : un module
    chargé depuis le texte modifié. [rend: 1] ⑥ TRAITEMENT — Lire le texte, remplacer l'appel, l'exécuter comme module.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un appel oublié dans `main` ne se voit que par E4. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun
    fichier écrit. ⑪ TERMINAISON — Rend la main ; lève ValueError si l'appel n'est pas trouvé une fois. [sort: non]
    """
    import types
    chemin = os.path.join(RACINE, "programmes", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py")
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    appel = ("operations, _retirees, _ajoutees, _sans_objet = appliquer_les_corrections_un_jeton(\n"
             "            operations, _p(base, NOM_DES_CORRECTIONS_UN_JETON), vrai_journal)")
    if texte.count(appel) != 1:
        raise ValueError("S8 : appel de la correction introuvable dans la mesure")
    m = types.ModuleType("MESURE_SANS_CORRECTION")
    m.__file__ = chemin
    exec(compile(texte.replace(appel, "operations, _retirees, _ajoutees, _sans_objet = operations, [], [], []"), chemin, "exec"),
         m.__dict__)
    return m


def main():
    """Lance les épreuves, puis les sabotages ; rend le code.

    ① RÔLE — Le point d'entrée. ② CONTEXTE D'APPEL — Ligne de commande. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — ① un calcul d'essai : `CalculImpossible` →
    code 2 · ② les épreuves sur le dépôt tel quel · ③ en `--saboter` : chaque sabotage, l'épreuve attendue doit tomber ;
    puis le témoin intact. ⑦ UNITÉ — — ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        K.rejouer_la_decision(RACINE, DECISION)
    except K.CalculImpossible as e:
        print("CODE 2 — l'épreuve n'a pas pu tourner : %s" % e)
        return 2
    ok = True
    r = epreuves()
    for n, ec in r.items():
        print(("%s conforme" % n) if not ec else ("%s NON CONFORME : %s" % (n, " | ".join(ec))))
        ok = ok and not ec
    if "--saboter" in sys.argv:
        for nom, bloc, attendue in SABOTAGES:
            with bloc():
                rs = epreuves()
            tombees = [n for n, ec in rs.items() if ec]
            mord = attendue in tombees
            print("%s %s (attendu : %s ; tombées : %s)" % (nom, "mord" if mord else "NE MORD PAS", attendue,
                                                           ", ".join(tombees) or "aucune"))
            ok = ok and mord
        r2 = epreuves()
        intact = not any(r2.values())
        print("TÉMOIN après les sabotages : %s" % ("conforme" if intact else "NON CONFORME %r" % r2))
        ok = ok and intact
    print("VERDICT : %s" % ("tout est conforme" if ok else "NON CONFORME"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
