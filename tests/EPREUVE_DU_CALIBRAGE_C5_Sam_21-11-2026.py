#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVE_DU_CALIBRAGE_C5 — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Épreuve COURTE de programmes/COMPARER_LE_CALIBRAGE_C5.py : une opération retirée doit apparaître
parmi les DISPARUES, une opération ajoutée parmi les NOUVELLES, un motif changé parmi les CHANGÉES, un gain seul
changé ailleurs que parmi les CHANGÉES, et le rapport écrit doit porter l'opération disparue. Les opérations viennent
de VRAIES lignes du tableau de référence (R-732). Elle ne lit ni le témoin des cours ni aucun cours.

① RÔLE — Prouver que `comparer` et `ecrire_le_rapport` voient ce qu'ils doivent voir ; avec --saboter, prouver que
  l'épreuve rougit quand on retire à `comparer` ce qu'elle teste (S1 : les disparues ne sont plus rendues ; S2 : la
  famille du motif ne distingue plus rien).
② CONTEXTE D'APPEL — Le lancement des épreuves de GitHub (tests/LANCEMENT_DES_EPREUVES.json, « Calibrage ») ; à la main.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ou d'une copie (lue, jamais écrite) ; « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte programmes/COMPARER_LE_CALIBRAGE_C5.py, programmes/JUGE_DES_STRATEGIES.py et
  donnees/TABLEAU_100_TRADES_C5E10_*.csv avec au moins trois lignes.
⑤ SORTIE — Le code de sortie : 0 tout vert (et sabotages qui mordent) ; 1 un cas rouge ou un sabotage qui ne mord
  pas ; 2 l'épreuve n'a pas pu tourner (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① charger le programme et le juge · ② lire trois vraies lignes · ③ jouer E1 à E6 · ④ sous --saboter,
  remplacer une fonction du programme chargé, rejouer, remettre.
⑦ UNITÉ — —
⑧ POURQUOI — Demande du Chat du 21-11-2026 (décision de Jean-Luc 15h11, « 1 », A-967) : un sabotage qui mord.
⑨ CE QUI CLOCHE — ① N'éprouve pas `operations_d_aujourd_hui` ni `main` (ils lisent le témoin des cours).
⑩ EFFET — Crée puis efface un dossier temporaire pour le rapport ; n'écrit rien dans la racine.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Non : rien n'y boucle sur des données.
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
    spec.loader.exec_module(m)
    return m


def cas(P, ref):
    """Joue E1 à E6.
        ① RÔLE — Les cas de l'épreuve.
        ② CONTEXTE D'APPEL — `main`, sans et sous sabotage.

    ③ ENTRÉE — `P` le programme chargé, `ref` trois vraies opérations.
    ④ CONDITIONS D'ENTRÉE — len(ref) ≥ 3.

    ⑤ SORTIE — UNE valeur : la liste des cas rouges.
    [rend: 1]
    ⑥ TRAITEMENT — six comparaisons fabriquées.

    ⑦ UNITÉ — EUROS.
    ⑧ POURQUOI — Chaque catégorie du rapport a son cas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Un
    dossier temporaire, effacé.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    rouges = []
    r = P.comparer(ref, copy.deepcopy(ref))
    if any(r[k] for k in ("disparues", "nouvelles", "changees", "gain_seul", "doublons")):
        rouges.append("E1 identité : un écart sur deux listes identiques")
    auj = copy.deepcopy(ref[1:])
    r = P.comparer(ref, auj)
    if [o["date_signal"] for o in r["disparues"]] != [ref[0]["date_signal"]]:
        rouges.append("E2 opération retirée absente des DISPARUES")
    auj = copy.deepcopy(ref)
    auj[1]["motif"] = "SL" if P.famille(ref[1]["motif"]) != "SL" else "TP"
    r = P.comparer(ref, auj)
    if len(r["changees"]) != 1:
        rouges.append("E3 motif changé absent des CHANGÉES")
    auj = copy.deepcopy(ref)
    auj[2]["gain"] += 12.34
    r = P.comparer(ref, auj)
    if r["changees"] or len(r["gain_seul"]) != 1:
        rouges.append("E4 gain seul mal rangé")
    r = P.comparer(ref[:2], ref)
    if len(r["nouvelles"]) != 1:
        rouges.append("E5 opération ajoutée absente des NOUVELLES")
    d = tempfile.mkdtemp(prefix="epreuve_calibrage_")
    try:
        res = P.comparer(ref, copy.deepcopy(ref[1:]))
        texte = P.ecrire_le_rapport(os.path.join(d, "r.md"), res, ref, ref[1:], ["épreuve"])
        bloc = texte.split("## DISPARUES", 1)[-1].split("## NOUVELLES", 1)[0]
        if ref[0]["date_signal"] not in bloc or ref[0]["valeur"] not in bloc:
            rouges.append("E6 opération disparue absente du rapport écrit")
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
    ⑥ TRAITEMENT — fiche en
    tête, ⑥.
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
        print("usage : EPREUVE_DU_CALIBRAGE_C5_Sam_21-11-2026.py <racine> [--saboter]")
        return 2
    racine = os.path.abspath(args[0])
    try:
        P = charger(os.path.join(racine, "programmes", "COMPARER_LE_CALIBRAGE_C5.py"), "COMPARER_LE_CALIBRAGE_C5")
        J = charger(os.path.join(racine, "programmes", "JUGE_DES_STRATEGIES.py"), "JUGE_DES_STRATEGIES")
        ref = P.operations_de_reference(J.trouver(racine, "TABLEAU_100_TRADES_C5E10"), J.cle_valeur)[:3]
        if len(ref) < 3:
            raise ValueError("moins de trois lignes dans le tableau de référence")
    except Exception as e:  # l'épreuve n'a pas pu tourner (R-734)
        print("ARRÊT : %s: %s" % (type(e).__name__, e))
        return 2
    rouges = cas(P, ref)
    for r in rouges:
        print("ROUGE — " + r)
    if rouges:
        return 1
    print("E1 à E6 verts.")
    if "--saboter" not in options:
        return 0
    vrai_comparer, vraie_famille = P.comparer, P.famille

    def sans_disparues(a, b):
        """S1.
            ① RÔLE — `comparer` qui tait les disparues.
            ② CONTEXTE D'APPEL — sabotage.
            ③ ENTRÉE — deux listes.

        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le dictionnaire faussé.
        [rend: 1]
        ⑥ TRAITEMENT — vide
        « disparues ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — E2 et E6 doivent rougir.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]
        """
        r = vrai_comparer(a, b)
        r["disparues"] = []
        return r
    sabotages = [("S1 disparues tues", "comparer", sans_disparues),
                 ("S2 famille aveugle", "famille", lambda m: "")]
    ne_mord_pas = []
    for nom, attr, faux in sabotages:
        setattr(P, attr, faux)
        try:
            rouge = bool(cas(P, ref))
        finally:
            P.comparer, P.famille = vrai_comparer, vraie_famille
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
