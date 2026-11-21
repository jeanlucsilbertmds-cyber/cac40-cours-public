#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVE_DE_L_ECART_DE_GAIN_C5 — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Épreuve COURTE de programmes/EXPLIQUER_L_ECART_DE_GAIN_C5.py : sur de VRAIES lignes du tableau des
100 trades du golden (R-732) — les trois premières, la moins chère, une valeur taxée et une non taxée —, l'hypothèse
« forfait de 300 € contre barème réel » doit être confirmée ; un gain du golden déplacé de 1,00 € sur une ligne chère
ET sur la moins chère doit la faire réfuter et nommer ces deux opérations ; sur une valeur non taxée la part de la taxe
vaut 0 et le courtage porte tout l'écart, sur une valeur taxée la part de la taxe est non nulle ; le tableau entier
rend le golden, un tableau falsifié de façon cohérente ne le rend plus ; le rapport écrit porte le verdict. Elle ne
lit aucun cours. Corrections du RELU Cowork (pointe fbb5debeb) : D-1 (E6, S6), D-2 (E5, S3, S4), m-1 (E2, S5).

① RÔLE — Prouver que `confronter_au_golden`, `mesurer`, `tolerance` et `ecrire_le_rapport` disent ce qu'ils doivent
  dire ; avec --saboter, prouver que l'épreuve rougit quand on retire ce qu'elle teste (S1 : `pnl_net` sourd au barème ;
  S2 : tolérance infinie ; S3 : barème « sans taxe » remplacé par le forfait, toute la part passe à la taxe ; S4 :
  barème « sans taxe » remplacé par le réel, toute la part passe au courtage ; S5 : tolérance décuplée ; S6 :
  confrontation au golden aveugle).
② CONTEXTE D'APPEL — Le lancement des épreuves de GitHub (tests/LANCEMENT_DES_EPREUVES.json, « EcartDeGain ») ; à la
  main.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ou d'une copie (lue, jamais écrite) ; « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte programmes/EXPLIQUER_L_ECART_DE_GAIN_C5.py, programmes/MODULE_POSITIONS.py,
  programmes/COMPARER_LE_CALIBRAGE_C5.py, programmes/JUGE_DES_STRATEGIES.py, le golden (gouvernance/golden_tests_*.json)
  et donnees/TABLEAU_100_TRADES_C5E10_*.csv avec au moins trois lignes, au moins une valeur taxée et une non taxée.
⑤ SORTIE — Le code de sortie : 0 tout vert (et sabotages qui mordent) ; 1 un cas rouge ou un sabotage qui ne mord
  pas ; 2 l'épreuve n'a pas pu tourner (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① charger le programme, le module, le comparateur, le juge, lire le golden · ② choisir les vraies lignes
  (`choisir`) · ③ jouer E1 à E6 · ④ sous --saboter, remplacer une fonction ou une constante, rejouer, tout remettre.
⑦ UNITÉ — EUROS.
⑧ POURQUOI — Relecture Cowork du 21-11-2026, défaut I-1 : la preuve doit tourner depuis un clone, avec une épreuve
  (R-731 : sabotages qui mordent) ; puis D-1, D-2, m-1 : trois sabotages restaient verts.
⑨ CE QUI CLOCHE — ① N'éprouve pas `main` (ni la garde de la fenêtre du regard unique) : la note de livraison la joue
  sur une copie.
⑩ EFFET — Crée puis efface un dossier temporaire pour le rapport ; n'écrit rien dans la racine.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Non : au plus six lignes mesurées, le
  tableau entier lu une fois, aucune boucle ouverte.
  [sort: oui]
"""
import copy
import json
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


def choisir(tout, M):
    """Choisit les vraies lignes de l'épreuve dans le tableau entier.

    ① RÔLE — Rendre les lignes qui donnent des dents à chaque cas.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `tout` le tableau lu par `lire_le_tableau`, `M` le module des positions.
    ④ CONDITIONS D'ENTRÉE — Au moins trois lignes, une valeur taxée et une non taxée à leur date d'entrée.
    ⑤ SORTIE — UNE valeur : (ops, i_cher, i_bon_marche, i_non_taxee, i_taxee), indices dans `ops`.
    [rend: 1]
    ⑥ TRAITEMENT — les trois premières lignes, la ligne au prix d'entrée le plus bas, la première non taxée, la première
    taxée (par `valeur_taxee`), sans doublon.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — m-1 : la tolérance d'une valeur chère (≈ 100 €) cache une tolérance décuplée, celle de la moins chère
    (ENGIE à 14,79 € le 21-11-2026) non ; D-2 : seule une valeur non taxée montre une taxe nulle.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit la liste des valeurs taxées (par le module).
    ⑪ TERMINAISON — Lève ValueError s'il manque une valeur taxée ou non taxée.
    [sort: non]
    """
    taxe = [bool(M.valeur_taxee(o["valeur"], o["date_entree"])) for o in tout]
    idx = [0, 1, 2, min(range(len(tout)), key=lambda i: tout[i]["prix_entree"]), taxe.index(False), taxe.index(True)]
    garde = sorted(set(idx))
    ops = [tout[i] for i in garde]
    return (ops, garde.index(1), garde.index(idx[3]), garde.index(idx[4]), garde.index(idx[5]))


def cas(P, M, choix, tout, golden):
    """Joue E1 à E6.

    ① RÔLE — Les cas de l'épreuve.
    ② CONTEXTE D'APPEL — `main`, sans et sous sabotage.
    ③ ENTRÉE — `P` le programme chargé, `M` le module des positions, `choix` le rendu de `choisir`, `tout` le tableau
    entier, `golden` le dictionnaire du golden.
    ④ CONDITIONS D'ENTRÉE — Celles de `choisir`.
    ⑤ SORTIE — UNE valeur : la liste des cas rouges.
    [rend: 1]
    ⑥ TRAITEMENT — E1 vraies lignes confirmées · E2 un gain du golden déplacé de 1,00 € sur une ligne chère et sur la
    moins chère réfute et nomme exactement ces deux opérations · E3 courtage + taxe = forfait − réel, la somme des
    groupes aussi, l'écart non nul · E4 le rapport écrit porte CONFIRMÉE SUR LE TABLEAU, puis RÉFUTÉE avec la valeur
    déplacée · E5 valeur non taxée : taxe 0,00 et courtage = tout l'écart, non nul ; valeur taxée : taxe non nulle ·
    E6 le tableau entier rend le golden ; une ligne au gain baissé de 1 000,00 € rend un écart « net » ; une ligne
    retirée rend un écart « n » ; un motif TP changé en SL rend un écart « motifs ».
    ⑦ UNITÉ — EUROS.
    ⑧ POURQUOI — Chaque affirmation du rapport a son cas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Un dossier temporaire, effacé.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    ops, i_cher, i_bon, i_libre, i_taxee = choix
    rouges = []
    vrai = P.mesurer(ops, M)
    if not vrai["confirmee"] or vrai["hors_tolerance"]:
        rouges.append("E1 vraies lignes non confirmées au forfait")
    faux_ops = copy.deepcopy(ops)
    faux_ops[i_cher]["ref"] += 1.00
    faux_ops[i_bon]["ref"] += 1.00
    faux = P.mesurer(faux_ops, M)
    vus = sorted((o["valeur"], o["date_entree"]) for o in faux["hors_tolerance"])
    if faux["confirmee"] or vus != sorted((ops[i]["valeur"], ops[i]["date_entree"]) for i in (i_cher, i_bon)):
        rouges.append("E2 gain déplacé de 1,00 € non vu (ligne chère ou moins chère)")
    somme_groupes = round(sum(e for _n, e in vrai["par_groupe"].values()), 2)
    if abs(vrai["part_courtage"] + vrai["part_taxe"] - vrai["ecart_forfait_reel"]) > 0.011 \
            or abs(somme_groupes - vrai["ecart_forfait_reel"]) > 0.011 or vrai["ecart_forfait_reel"] == 0:
        rouges.append("E3 décomposition incohérente ou écart nul")
    d = tempfile.mkdtemp(prefix="epreuve_ecart_de_gain_")
    try:
        t1 = P.ecrire_le_rapport(os.path.join(d, "a.md"), vrai, ["épreuve"])
        t2 = P.ecrire_le_rapport(os.path.join(d, "b.md"), faux, ["épreuve"])
        hors = t2.split("## OPÉRATIONS HORS TOLÉRANCE", 1)[-1].split("## VERDICT", 1)[0]
        if "CONFIRMÉE SUR LE TABLEAU" not in t1 or "RÉFUTÉE" not in t2 or ops[i_cher]["valeur"] not in hors:
            rouges.append("E4 verdict ou opération hors tolérance absent du rapport écrit")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    libre, taxee = P.mesurer([ops[i_libre]], M), P.mesurer([ops[i_taxee]], M)
    if libre["part_taxe"] != 0 or libre["part_courtage"] == 0 \
            or abs(libre["part_courtage"] - libre["ecart_forfait_reel"]) > 0.011 or taxee["part_taxe"] <= 0:
        rouges.append("E5 décomposition courtage/taxe fausse (non taxée : taxe %.2f, courtage %.2f ; taxée : taxe %.2f)"
                      % (libre["part_taxe"], libre["part_courtage"], taxee["part_taxe"]))
    if P.confronter_au_golden(tout, golden):
        rouges.append("E6 le tableau entier ne rend pas le golden")
    net_faux = copy.deepcopy(tout)
    net_faux[1]["ref"] -= 1000.00
    motif_faux = copy.deepcopy(tout)
    i_tp = next(i for i, o in enumerate(motif_faux) if o["motif"] == "TP")
    motif_faux[i_tp]["motif"] = "SL"
    attendus = (("net", net_faux), ("n", tout[:-1]), ("motifs", motif_faux))
    for mot, tableau in attendus:
        if not any(e.startswith(mot + " ") for e in P.confronter_au_golden(tableau, golden)):
            rouges.append("E6 tableau falsifié (%s) non vu" % mot)
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
        tout = P.lire_le_tableau(J.trouver(racine, "TABLEAU_100_TRADES_C5E10"), K.gain)
        if len(tout) < 3:
            raise ValueError("moins de trois lignes dans le tableau")
        with open(J.trouver(racine, "golden_tests_"), encoding="utf-8") as f:
            golden = json.load(f)
        choix = choisir(tout, M)
    except Exception as e:  # l'épreuve n'a pas pu tourner (R-734)
        print("ARRÊT : %s: %s" % (type(e).__name__, e))
        return 2
    rouges = cas(P, M, choix, tout, golden)
    for r in rouges:
        print("ROUGE — " + r)
    if rouges:
        return 1
    print("E1 à E6 verts.")
    if "--saboter" not in options:
        return 0
    origine = [(M, "pnl_net", M.pnl_net), (P, "tolerance", P.tolerance), (P, "SANS_TAXE", P.SANS_TAXE),
               (P, "DEMI_PAS_DE_PRIX", P.DEMI_PAS_DE_PRIX), (P, "confronter_au_golden", P.confronter_au_golden)]
    vrai_pnl = M.pnl_net

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
                 ("S2 tolérance infinie", P, "tolerance", lambda *a: float("inf")),
                 ("S3 sans taxe = forfait", P, "SANS_TAXE", P.FORFAIT),
                 ("S4 sans taxe = réel", P, "SANS_TAXE", None),
                 ("S5 tolérance décuplée", P, "DEMI_PAS_DE_PRIX", P.DEMI_PAS_DE_PRIX * 10),
                 ("S6 golden aveugle", P, "confronter_au_golden", lambda *a: [])]
    ne_mord_pas = []
    for nom, cible, attr, faux in sabotages:
        setattr(cible, attr, faux)
        try:
            rouge = bool(cas(P, M, choix, tout, golden))
        finally:
            for c, a, v in origine:
                setattr(c, a, v)
        print("%s : %s (attendu ROUGE)" % (nom, "ROUGE" if rouge else "VERT"))
        if not rouge:
            ne_mord_pas.append(nom)
    print("SABOTAGES JOUÉS %d sur %d" % (len(sabotages), len(sabotages)))
    if ne_mord_pas:
        print("SABOTAGES QUI NE MORDENT PAS : %s" % ne_mord_pas)
        return 1
    print("Sabotages S1 à S%d : conformes." % len(sabotages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
