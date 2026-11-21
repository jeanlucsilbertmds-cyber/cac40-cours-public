#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVE_DE_L_ECART_DE_GAIN_C5 — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Épreuve COURTE de programmes/EXPLIQUER_L_ECART_DE_GAIN_C5.py : sur trois VRAIES lignes du tableau des
100 trades du golden (R-732), l'hypothèse « forfait de 300 € contre barème réel » doit être confirmée ; un gain du
golden déplacé de 1,00 € doit la faire réfuter et nommer l'opération ; la décomposition courtage + taxe doit
retomber sur l'écart forfait − réel ; le rapport écrit doit porter le verdict. Elle ne lit aucun cours.

① RÔLE — Prouver que `mesurer` et `ecrire_le_rapport` disent ce qu'ils doivent dire ; avec --saboter, prouver que
  l'épreuve rougit quand on retire ce qu'elle teste (S1 : `pnl_net` sourd au barème, le forfait n'est plus appliqué ;
  S2 : tolérance infinie, plus rien n'est hors tolérance).
② CONTEXTE D'APPEL — Le lancement des épreuves de GitHub (tests/LANCEMENT_DES_EPREUVES.json, « EcartDeGain ») ; à la
  main.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ou d'une copie (lue, jamais écrite) ; « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte programmes/EXPLIQUER_L_ECART_DE_GAIN_C5.py, programmes/MODULE_POSITIONS.py,
  programmes/COMPARER_LE_CALIBRAGE_C5.py, programmes/JUGE_DES_STRATEGIES.py et donnees/TABLEAU_100_TRADES_C5E10_*.csv
  avec au moins trois lignes.
⑤ SORTIE — Le code de sortie : 0 tout vert (et sabotages qui mordent) ; 1 un cas rouge ou un sabotage qui ne mord
  pas ; 2 l'épreuve n'a pas pu tourner (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① charger le programme, le module, le comparateur, le juge · ② lire trois vraies lignes · ③ jouer E1
  à E4 · ④ sous --saboter, remplacer une fonction, rejouer, remettre.
⑦ UNITÉ — EUROS.
⑧ POURQUOI — Relecture Cowork du 21-11-2026, défaut I-1 : la preuve doit tourner depuis un clone, avec une épreuve
  (R-731 : sabotages qui mordent).
⑨ CE QUI CLOCHE — ① N'éprouve pas `main` (ni la garde de la fenêtre du regard unique) : la note de livraison la joue
  sur une copie.
⑩ EFFET — Crée puis efface un dossier temporaire pour le rapport ; n'écrit rien dans la racine.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Non : trois lignes, aucune boucle
  ouverte.
  [sort: oui]
"""
import copy
import importlib.util
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True


def charger(chemin, nom):
    """Charge un programme comme un module.

    ① RÔLE — Atteindre le programme éprouvé sans le recopier.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
    [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut du fichier.
    ⑪ TERMINAISON — Lève ce que lève l'import.
    [sort: non]
    """
    d = os.path.dirname(os.path.abspath(chemin))
    if d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


def cas(P, M, ops):
    """Joue E1 à E4.

    ① RÔLE — Les cas de l'épreuve.
    ② CONTEXTE D'APPEL — `main`, sans et sous sabotage.
    ③ ENTRÉE — `P` le programme chargé, `M` le module des positions, `ops` trois vraies opérations.
    ④ CONDITIONS D'ENTRÉE — len(ops) ≥ 3.
    ⑤ SORTIE — UNE valeur : la liste des cas rouges.
    [rend: 1]
    ⑥ TRAITEMENT — E1 vraies lignes confirmées · E2 un gain du golden déplacé de 1,00 € réfute et nomme l'opération ·
    E3 courtage + taxe = forfait − réel, et la somme des groupes aussi, et l'écart est non nul · E4 le rapport écrit
    porte CONFIRMÉE, puis RÉFUTÉE avec la valeur déplacée.
    ⑦ UNITÉ — EUROS.
    ⑧ POURQUOI — Chaque affirmation du rapport a son cas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Un dossier temporaire, effacé.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    rouges = []
    vrai = P.mesurer(ops, M)
    if not vrai["confirmee"] or vrai["hors_tolerance"]:
        rouges.append("E1 vraies lignes non confirmées au forfait")
    faux_ops = copy.deepcopy(ops)
    faux_ops[1]["ref"] += 1.00
    faux = P.mesurer(faux_ops, M)
    if faux["confirmee"] or [o["date_entree"] for o in faux["hors_tolerance"]] != [ops[1]["date_entree"]]:
        rouges.append("E2 gain déplacé de 1,00 € non vu")
    somme_groupes = round(sum(e for _n, e in vrai["par_groupe"].values()), 2)
    if abs(vrai["part_courtage"] + vrai["part_taxe"] - vrai["ecart_forfait_reel"]) > 0.011 \
            or abs(somme_groupes - vrai["ecart_forfait_reel"]) > 0.011 or vrai["ecart_forfait_reel"] == 0:
        rouges.append("E3 décomposition incohérente ou écart nul")
    d = tempfile.mkdtemp(prefix="epreuve_ecart_de_gain_")
    try:
        t1 = P.ecrire_le_rapport(os.path.join(d, "a.md"), vrai, ["épreuve"])
        t2 = P.ecrire_le_rapport(os.path.join(d, "b.md"), faux, ["épreuve"])
        hors = t2.split("## OPÉRATIONS HORS TOLÉRANCE", 1)[-1].split("## VERDICT", 1)[0]
        if "CONFIRMÉE" not in t1 or "RÉFUTÉE" not in t2 or ops[1]["valeur"] not in hors:
            rouges.append("E4 verdict ou opération hors tolérance absent du rapport écrit")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return rouges


def main():
    """Point d'entrée.

    ① RÔLE — Voir fiche en tête.
    ② CONTEXTE D'APPEL — Le lancement.
    ③ ENTRÉE — fiche en tête, ③.
    ④ CONDITIONS D'ENTRÉE — fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
    [rend: 1]
    ⑥ TRAITEMENT — fiche en tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — fiche en tête, ⑩.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) != 1 or any(o != "--saboter" for o in options):
        print("usage : EPREUVE_DE_L_ECART_DE_GAIN_C5_Sam_21-11-2026.py <racine> [--saboter]")
        return 2
    racine = os.path.abspath(args[0])
    p = os.path.join(racine, "programmes")
    try:
        J = charger(os.path.join(p, "JUGE_DES_STRATEGIES.py"), "JUGE_DES_STRATEGIES")
        K = charger(os.path.join(p, "COMPARER_LE_CALIBRAGE_C5.py"), "COMPARER_LE_CALIBRAGE_C5")
        M = charger(os.path.join(p, "MODULE_POSITIONS.py"), "MODULE_POSITIONS")
        P = charger(os.path.join(p, "EXPLIQUER_L_ECART_DE_GAIN_C5.py"), "EXPLIQUER_L_ECART_DE_GAIN_C5")
        ops = P.lire_le_tableau(J.trouver(racine, "TABLEAU_100_TRADES_C5E10"), K.gain)[:3]
        if len(ops) < 3:
            raise ValueError("moins de trois lignes dans le tableau")
    except Exception as e:  # l'épreuve n'a pas pu tourner (R-734)
        print("ARRÊT : %s: %s" % (type(e).__name__, e))
        return 2
    rouges = cas(P, M, ops)
    for r in rouges:
        print("ROUGE — " + r)
    if rouges:
        return 1
    print("E1 à E4 verts.")
    if "--saboter" not in options:
        return 0
    vrai_pnl, vraie_tol = M.pnl_net, P.tolerance

    def sourd(*a, **k):
        """S1.

        ① RÔLE — `pnl_net` qui ignore le barème demandé.
        ② CONTEXTE D'APPEL — sabotage.
        ③ ENTRÉE — les arguments de `pnl_net`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le gain au barème réel.
        [rend: 1]
        ⑥ TRAITEMENT — retire `bareme`.
        ⑦ UNITÉ — EUROS.
        ⑧ POURQUOI — E1 doit rougir : sans forfait, le golden ne se retrouve plus.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]
        """
        k.pop("bareme", None)
        return vrai_pnl(*a, **k)
    sabotages = [("S1 barème ignoré", M, "pnl_net", sourd),
                 ("S2 tolérance infinie", P, "tolerance", lambda *a: float("inf"))]
    ne_mord_pas = []
    for nom, cible, attr, faux in sabotages:
        setattr(cible, attr, faux)
        try:
            rouge = bool(cas(P, M, ops))
        finally:
            M.pnl_net, P.tolerance = vrai_pnl, vraie_tol
        print("%s : %s (attendu ROUGE)" % (nom, "ROUGE" if rouge else "VERT"))
        if not rouge:
            ne_mord_pas.append(nom)
    print("SABOTAGES JOUÉS %d sur %d" % (len(sabotages), len(sabotages)))
    if ne_mord_pas:
        print("SABOTAGES QUI NE MORDENT PAS : %s" % ne_mord_pas)
        return 1
    print("Sabotages S1, S2 : conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
