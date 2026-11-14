#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RELEVER_LES_REFUS_DE_LA_VENTE_REGLABLE — Mer 11-11-2026 (Paris) — mission « VENTE » du plan V7. Simulation uniquement.

USAGE
    python3 tests/outils/RELEVER_LES_REFUS_DE_LA_VENTE_REGLABLE_Mer_11-11-2026.py <dossier des programmes>
    python3 tests/outils/RELEVER_LES_REFUS_DE_LA_VENTE_REGLABLE_Mer_11-11-2026.py --calibrer

① RÔLE — Relever, par l'arbre syntaxique, les endroits du code qui REFUSENT encore la durée « aucune » ou le stop
  « sans stop » : le BACKLOG A-611 (ajout du 31-10-2026) et A-645 disent la durée « aucune » « impossible à 7 endroits
  du code ». Le relevé remplace la liste écrite à la main, dont les numéros de ligne vieillissent.
② CONTEXTE D'APPEL — À la main, par l'auteur ou le relecteur d'un travail sur la vente (passe ② de R-740).
③ ENTRÉE — Un argument : le dossier des programmes, ou « --calibrer ».
④ CONDITIONS D'ENTRÉE — Des fichiers Python lisibles par `ast`.
⑤ SORTIE — Le code de sortie : 0 (relevé affiché, ou calibrage bon) · 1 (calibrage faux, ou un fichier illisible) ·
  2 (arguments absents).
  [rend: 1]
⑥ TRAITEMENT — Cinq motifs, chacun une PROPRIÉTÉ du code et non une liste de noms de fichiers : R1 un appel à la
  lecture STRICTE `lire_horizon` (elle rend None pour « aucune ») · R2 une conversion `int`, `float`, `range` ou
  `round` dont l'argument nomme un horizon · R3 une lecture stricte du stop (`seuil_de_la_fiche(…, "sl")`,
  `pourcent`/`pourcents_de` d'un sl) · R4 une forme numérique exigée (`FORME_NOMBRE.match`, `FORME_POURCENT.match`) ·
  R5 le calcul du prix du stop (`constante - sl`). Un relevé est dit GARDÉ quand sa fonction reconnaît la sentinelle
  de SA famille (HORIZON_AUCUNE pour R1-R2, STOP_AUCUN ou le mot du stop pour R3 et R5, l'une ou l'autre pour R4).
⑦ UNITÉ — Des numéros de ligne.
⑧ POURQUOI — « Un motif de recherche se calibre sur un cas connu avant de servir — et sur un cas qui doit échouer »
  (instructions du projet, geste « mesurer avant de conclure ») : `--calibrer` joue un cas connu qui doit être relevé
  (le refus de `JOUER_LES_VERSIONS.controler_fusion` de main 15f2c5eb, recopié) et un cas qui ne doit pas l'être (la
  lecture `lire_horizon_ou_aucune`).
⑨ CE QUI CLOCHE — Un refus écrit autrement (une comparaison de texte, un dictionnaire de valeurs permises) n'est pas
  vu : un relevé vide ne prouve pas l'absence de refus. La preuve que la chaîne accepte « aucune » et « sans stop »
  est l'épreuve de bout en bout W13 de `tests/EPREUVES_DE_LA_VENTE_REGLABLE_Mer_11-11-2026.py`, pas ce relevé.
  « GARDÉ » ne dit pas que la garde est juste, seulement qu'elle existe dans la fonction.
⑩ EFFET — Affiche ; n'écrit rien.
⑪ TERMINAISON — Sort avec son code. Aucun appel qui puisse ne pas revenir.
  [sort: oui]
"""
import ast, glob, os, sys

GARDES = {"horizon": ("HORIZON_AUCUNE", "_horizon_aucune()", "MOT_DE_L_HORIZON_AUCUNE"),
          "stop": ("STOP_AUCUN", "_stop_aucun()", "MOT_DU_STOP_AUCUN", "est_le_mot_du_stop_aucun")}


def relever(source, nom):
    """Rend les relevés d'un texte Python : une ligne par endroit qui refuse « aucune » ou « sans stop ».

    ① RÔLE — Le cœur du relevé, sur un seul fichier.
    ② CONTEXTE D'APPEL — `main` (une fois par fichier) et `calibrer`.
    ③ ENTRÉE — `source` : le texte Python · `nom` : le nom affiché.
    ④ CONDITIONS D'ENTRÉE — `source` se lit par `ast.parse`.
    ⑤ SORTIE — UNE valeur : la liste des relevés, chacun un tuple (nom, ligne, motif, extrait, fonction, gardé).
      [rend: 1]
    ⑥ TRAITEMENT — ① noter, pour chaque nœud, sa fonction englobante la plus proche et les gardes que contient son
      CODE (sa fiche, la chaîne de tête, est écartée) ·
      ② tester les cinq motifs sur chaque appel et chaque soustraction.
    ⑦ UNITÉ — Des numéros de ligne.
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève SyntaxError sur un texte illisible.
      [sort: non]
    """
    arbre = ast.parse(source)
    # `ast.get_source_segment` relit tout le texte à chaque appel (des minutes sur le juge) : `ast.unparse`.
    seg = ast.unparse
    fonc = {}
    for d in ast.walk(arbre):
        if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # LE CODE SEUL, sans la fiche de la fonction : une fiche qui NOMME la sentinelle n'est pas une garde
            # (MODULE_JUGEMENT.coupure_70_30 la nomme dans sa fiche et la refuse dans son code).
            corps = d.body[1:] if d.body and isinstance(d.body[0], ast.Expr) and \
                isinstance(getattr(d.body[0], "value", None), ast.Constant) else d.body
            texte = "\n".join(ast.unparse(x) for x in corps)
            for n in ast.walk(d):
                fonc[id(n)] = (d.name, texte)
    sortie = []
    for n in ast.walk(arbre):
        motif, famille = None, None
        if isinstance(n, ast.Call):
            appel = n.func.attr if isinstance(n.func, ast.Attribute) else (n.func.id if isinstance(n.func, ast.Name) else "")
            args = " ".join(seg(x) for x in n.args)
            tete = seg(n.func).split(".")[0]
            if appel == "lire_horizon":
                motif, famille = "R1 lecture stricte de l'horizon", "horizon"
            elif appel in ("int", "float", "range", "round") and "horizon" in args:
                motif, famille = "R2 conversion numérique d'un horizon", "horizon"
            elif appel == "seuil_de_la_fiche" and "sl" in [x.value for x in n.args if isinstance(x, ast.Constant)]:
                motif, famille = "R3 lecture stricte du stop", "stop"
            elif appel in ("pourcent", "pourcents_de") and "sl" in args:
                motif, famille = "R3 lecture stricte du stop", "stop"
            elif appel == "match" and tete in ("FORME_NOMBRE", "FORME_POURCENT"):
                motif, famille = "R4 forme numérique exigée", None
        elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Sub) and isinstance(n.left, ast.Constant) \
                and seg(n.right) == "sl":
            motif, famille = "R5 calcul du prix du stop", "stop"
        if not motif:
            continue
        nf, texte = fonc.get(id(n), ("-", ""))
        gardes = GARDES[famille] if famille else GARDES["horizon"] + GARDES["stop"]
        sortie.append((nom, n.lineno, motif, seg(n)[:60], nf, any(g in texte for g in gardes)))
    return sortie


def calibrer():
    """Joue le relevé sur un cas connu qui doit sortir et sur un cas qui ne doit pas sortir.

    ① RÔLE — Prouver que le motif voit ce qu'il doit voir, et ne voit pas ce qu'il ne doit pas voir.
    ② CONTEXTE D'APPEL — `main`, avec « --calibrer ».
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : vrai si le calibrage est bon.
      [rend: 1]
    ⑥ TRAITEMENT — ① le contrôle de la fusion de JOUER_LES_VERSIONS tel qu'il était sur main 15f2c5eb (deux refus de
      « aucune », non gardés) et la lecture du stop de `reglages_du_registre` du soir doivent rendre R1, R2 et R3
      non gardés · ② une lecture `lire_horizon_ou_aucune` et une lecture
      gardée ne doivent rien rendre de non gardé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Deux cas seulement.
    ⑩ EFFET — Affiche le résultat.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    connu = ("def controler_fusion(J, fusion, version):\n"
             "    ecarts = []\n"
             "    if J.lire_horizon(fusion[\"horizon\"]) != int(version[\"horizon\"]):\n"
             "        ecarts.append(1)\n"
             "    return ecarts\n"
             "def reglages(x):\n"
             "    return juge.seuil_de_la_fiche(x, \"sl\")\n")
    muet = ("def lire(fiche):\n"
            "    return COMMUN.lire_horizon_ou_aucune(fiche[\"horizon\"])\n"
            "def lire2(x):\n"
            "    if COMMUN.lire_horizon_ou_aucune(x) is COMMUN.HORIZON_AUCUNE:\n"
            "        return x\n"
            "    return COMMUN.lire_horizon(x)\n")
    a = sorted((r[2][:2], r[5]) for r in relever(connu, "connu"))
    b = [r for r in relever(muet, "muet") if not r[5]]
    ok = a == [("R1", False), ("R2", False), ("R3", False)] and b == []
    print("calibrage : cas connu %s · cas muet %s → %s" % (a, b, "BON" if ok else "FAUX"))
    return ok


def main():
    """Point d'entrée : calibrer, ou relever un dossier.

    ① RÔLE — Lire la ligne de commande et afficher le relevé.
    ② CONTEXTE D'APPEL — Le bas de ce fichier.
    ③ ENTRÉE — `sys.argv`.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① « --calibrer » : calibrer · ② sinon relever chaque fichier Python du dossier, trié par nom,
      et compter les non gardés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(sys.argv) != 2:
        print(__doc__.split("①")[0])
        return 2
    if sys.argv[1] == "--calibrer":
        return 0 if calibrer() else 1
    tout, illisibles = [], []
    for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.py"))):
        try:
            tout += relever(open(f, encoding="utf-8").read(), os.path.basename(f))
        except (SyntaxError, UnicodeDecodeError):
            illisibles.append(os.path.basename(f))
    for nom, ligne, motif, extrait, nf, garde in tout:
        print("%s:%d  %s  %s  [%s]%s" % (nom, ligne, motif, extrait, nf, "  GARDÉ" if garde else ""))
    print("relevés : %d · non gardés : %d · illisibles : %s" % (len(tout), sum(1 for r in tout if not r[5]),
                                                                ", ".join(illisibles) or "aucun"))
    return 1 if illisibles else 0


if __name__ == "__main__":
    sys.exit(main())
