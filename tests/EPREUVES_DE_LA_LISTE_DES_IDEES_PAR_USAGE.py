#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Épreuves de programmes/FABRIQUER_LA_LISTE_DES_IDEES_PAR_USAGE.py (R-731).

① RÔLE — Prouver que le rangement par usage fait ce qu'il dit, et que chaque
  épreuve rougit quand on retire ce qu'elle teste (sabotages).
② CONTEXTE D'APPEL — À la main : python3 tests/EPREUVES_DE_LA_LISTE_DES_IDEES_PAR_USAGE.py
③ ENTRÉE — —
④ CONDITIONS D'ENTRÉE — Lancé depuis la racine d'un clone du dépôt.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si toutes les épreuves et tous les
  sabotages se comportent comme attendu, 1 sinon.
⑥ TRAITEMENT — ① épreuves sur `classer`, dont des cases réelles du tableau
  (R-732) · ② fabrication sur un tableau fabriqué dans un dossier temporaire ·
  ③ sabotages : on remplace une pièce par une version cassée et on exige
  qu'au moins une épreuve rougisse.
⑦ UNITÉ — —
⑧ POURQUOI — « une épreuve qui reste verte quand on retire ce qu'elle teste
  n'est pas une preuve, c'est une décoration » (instructions du projet, § 7).
⑨ CE QUI CLOCHE — Les sabotages ne couvrent que trois pièces.
⑩ EFFET — Écrit dans un dossier temporaire, effacé ensuite.
⑪ TERMINAISON — Rend toujours la main.
"""
import importlib.util, os, sys, tempfile, shutil, re

spec = importlib.util.spec_from_file_location("L", "programmes/FABRIQUER_LA_LISTE_DES_IDEES_PAR_USAGE.py")
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)

def epreuves(classer, fabriquer):
    """Rend la liste des épreuves échouées (vide = tout vert)."""
    ko = []
    cas = [  # cases RÉELLES du tableau au 20-11-2026 (R-732), puis cas limites
        ("2 protection + 3 paramètre (objectif réaliste)", ["2", "3"]),        # I09
        ("1 stratégie (③) + 2 protection (①)", ["1", "2"]),                    # I46
        ("5 plus tard (à la minute)", ["5"]),                                    # I44
        ("4 taille de la mise + 2 méthode", ["4"]),                              # I26 : « 2 méthode » n'est pas un usage reconnu
        ("—", ["0"]), ("voir I07, I11, I12", ["D"]), ("", ["X"]),
        ("sur 2 939 croisements", ["X"]),
    ]
    for case, attendu in cas:
        if classer(case) != attendu:
            ko.append(f"classer({case!r}) = {classer(case)} au lieu de {attendu}")
    d = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(d, "etudes", "IDEES_VIDEOS_INSTAGRAM"))
        t = os.path.join(d, "etudes", "IDEES_VIDEOS_INSTAGRAM", "idees_videos.csv")
        with open(t, "w", encoding="utf-8") as f:
            f.write("id;video;producteur;idee_en_clair;case;testable;action_backlog\n")
            f.write("I01;V01 · reel;Kara Tools (k);LA FAUSSE BAISSE : texte;1 stratégie;\"maintenant ; détail\";A-744\n")
            f.write("I02;V02;P;IDÉE B : x;illisible;—;\n")
        with open(os.path.join(d, "BACKLOG_DECISIONS.md"), "w", encoding="utf-8") as f:
            f.write("| A-837 | idées plus tard : I02 |\n")
        code = fabriquer(d)
        out = open(os.path.join(d, "etudes", "IDEES_VIDEOS_INSTAGRAM", "LISTE_PAR_USAGE.md"), encoding="utf-8").read()
        if code != 1: ko.append(f"code {code} au lieu de 1 avec une idée non classée")
        if "**I01** — LA FAUSSE BAISSE · testable : maintenant · action : A-744 · source : V01, Kara Tools" not in out:
            ko.append("ligne de I01 incorrecte")
        if "## NON CLASSÉES" not in out or "**I02**" not in out.split("## NON CLASSÉES")[1]:
            ko.append("I02 illisible absente des NON CLASSÉES")
        if "A-837 (liste des idées « plus tard »)" not in out:
            ko.append("renvoi à A-837 absent pour une idée sans action citée par A-837")
        os.remove(t)
        if fabriquer(d) != 2: ko.append("tableau absent : code différent de 2")
    finally:
        shutil.rmtree(d)
    return ko

ko = epreuves(L.classer, L.fabriquer)
print("ÉPREUVES :", "VERT" if not ko else "ROUGE"); [print("  ", k) for k in ko]
# Sabotages : chacun DOIT rougir.
sab = {
    "classer ignore le mot d'usage": lambda c: [m for m in re.findall(r"([1-5])", c)][:1] or ["X"],
    "classer ne garde que le premier usage": lambda c: L.classer(c)[:1],
    "classer range tout en X": lambda c: ["X"],
}
sab_ok = True
for nom, f in sab.items():
    r = epreuves(f, L.fabriquer)
    print("SABOTAGE", nom, ":", "rougit" if r else "RESTE VERT")
    sab_ok &= bool(r)
orig = L.ligne
L.ligne = lambda i, a, p=frozenset(): orig(i, a)   # sabotage : oubli du renvoi à A-837
r = epreuves(L.classer, L.fabriquer); print("SABOTAGE ligne sans A-837 :", "rougit" if r else "RESTE VERT"); sab_ok &= bool(r)
L.ligne = orig
sys.exit(0 if (not ko and sab_ok) else 1)
