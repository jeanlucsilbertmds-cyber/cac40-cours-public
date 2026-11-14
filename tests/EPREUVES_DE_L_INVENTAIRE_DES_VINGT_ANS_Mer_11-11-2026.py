#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_INVENTAIRE_DES_VINGT_ANS_Mer_11-11-2026.py — Mer 11-11-2026 (Paris). Simulation uniquement.

① RÔLE — Éprouver (tour 2 : six sabotages internes et deux externes) etudes/VINGT_ANS_A_PART_Mer_11-11-2026/INVENTORIER_LES_VINGT_ANS.py : sans sabotage, ses cinq
  calibrages passent (code 0) ; chacun des six sabotages internes et des deux sabotages externes (texte du programme changé dans une copie) fait échouer LE calibrage qu'il vise (code 1) ; une
  racine absente ou un sabotage inconnu rendent 2 (R-734).
② CONTEXTE D'APPEL — À la main, ou par le relais des séries :
  python3 -I tests/EPREUVES_DE_L_INVENTAIRE_DES_VINGT_ANS_Mer_11-11-2026.py <racine d'une COPIE du dépôt>
③ ENTRÉE — La racine d'une copie du dépôt (le programme éprouvé ne l'écrit pas, mais la règle du cadre V7 veut une
  copie).
④ CONDITIONS D'ENTRÉE — La copie porte le programme éprouvé et ses entrées (④ de son en-tête).
⑤ SORTIE — UNE valeur : le code de sortie, 0 si tous les cas tiennent, 1 sinon, 2 si l'épreuve n'a pas pu tourner.
  À l'écran : une ligne par cas, puis « CAS : n / m tenus ». [rend: 1]
⑥ TRAITEMENT — Pour chaque cas, lancer le programme dans un processus à part, lire son code et ses lignes « Kn
  PASSE/ÉCHOUE », comparer à l'attendu.
⑦ UNITÉ — —
⑧ POURQUOI — R-731 : un jeu d'épreuves se sabote contre sa propre correction ; chaque sabotage doit mordre.
⑨ CE QUI CLOCHE — Les sabotages sont dans le programme éprouvé (option --saboter) : un sabotage retiré du
  programme rend 2 ici (« sabotage inconnu »), ce qui se voit. · Environ 10 s par cas sur la machine du Chat.
⑩ EFFET — Lance des processus ; affiche.
⑪ TERMINAISON — Rend la main ; chaque processus a une limite de 600 s. [sort: non]
"""
import os, re, subprocess, sys

PROGRAMME = os.path.join("etudes", "VINGT_ANS_A_PART_Mer_11-11-2026", "INVENTORIER_LES_VINGT_ANS.py")
# SABOTAGES EXTERNES (relecteur E2a, D1) : le TEXTE du programme est changé dans une copie, sans option prévue par
# lui ; (nom, texte d'origine, texte saboté, calibrage qui doit tomber). Les deux cas du relecteur, refaits.
EXTERNES = [
    ("X1 division retirée dans le texte", "abs(c / q / b[0] - 1)", "abs(c / b[0] - 1)", "K6"),
    ("X2 borne de période fausse dans le texte", 'fin_bnains = "2012-01-01" if sabotage == "S6" else R.FIN_BNAINS',
     'fin_bnains = "2012-01-01"', "K7"),
]
# (nom du cas, arguments après la racine, code attendu, calibrage qui doit échouer ou None)
CAS = [
    ("normal", [], 0, None),
    ("S1 facteurs lus comme 1", ["--saboter", "S1"], 1, "K1"),
    ("S2 frais jamais demandés", ["--saboter", "S2"], 1, "K3"),
    ("S3 toutes les sociétés numérotées", ["--saboter", "S3"], 1, "K4"),
    ("S4 noms de A_VERSER au référentiel", ["--saboter", "S4"], 1, "K5"),
    ("S5 division par le facteur retirée", ["--saboter", "S5"], 1, "K6"),
    ("S6 borne de période fausse", ["--saboter", "S6"], 1, "K7"),
    ("sabotage inconnu", ["--saboter", "S9"], 2, None),
]


def lancer(racine, args):
    """Lance le programme éprouvé ; rend son code et sa sortie.

    ① RÔLE — Un lancement isolé. ② CONTEXTE D'APPEL — `principal`, pour chaque cas.
    ③ ENTRÉE — `racine` : la copie ; `args` : les arguments après la racine.
    ④ CONDITIONS D'ENTRÉE — Le programme existe sous la racine.
    ⑤ SORTIE — DEUX valeurs : le code de sortie et le texte affiché. [rend: 2]
    ⑥ TRAITEMENT — `python3 -I <programme> <racine> <args>`, sortie capturée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un processus neuf par cas : le programme change de dossier et importe des modules.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus.
    ⑪ TERMINAISON — Rend la main ; lève `subprocess.TimeoutExpired` au-delà de 600 s. [sort: non]
    """
    p = subprocess.run([sys.executable, "-I", os.path.join(racine, PROGRAMME), racine] + args,
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout + p.stderr


def principal(argv):
    """Déroule les cas ; rend le code de sortie.

    ① RÔLE — Le corps de l'épreuve. ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `argv` : la racine. ④ CONDITIONS D'ENTRÉE — Un dossier.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — Pour chaque cas : lancer ; tenu si le code est l'attendu ET, sans sabotage, aucun « ÉCHOUE »,
      ou, sous sabotage, le calibrage visé échoue et lui seul.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sabotage qui ferait tout échouer ne prouverait pas qu'il vise le bon calibrage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        print("USAGE : EPREUVES_DE_L_INVENTAIRE_DES_VINGT_ANS_Mer_11-11-2026.py <racine d'une copie>")
        return 2
    racine = os.path.abspath(argv[0])
    tenus = 0
    cas = CAS + [("racine absente", None, 2, None)]
    for nom, args, attendu, vise in cas:
        if args is None:
            p = subprocess.run([sys.executable, "-I", os.path.join(racine, PROGRAMME), "/nexiste/pas"],
                               capture_output=True, text=True, timeout=60)
            code, sortie = p.returncode, p.stdout + p.stderr
        else:
            code, sortie = lancer(racine, args)
        echecs = re.findall(r"^(K\d) ÉCHOUE", sortie, re.M)
        if vise is None:
            ok = code == attendu and not echecs
        else:
            ok = code == attendu and echecs == [vise]
        tenus += ok
        print(f"  {'TENU ' if ok else 'ÉCHEC'}  {nom} — code {code} (attendu {attendu}) ; calibrages en échec {echecs}"
              + (f" (attendu [{vise}])" if vise else ""))
    import tempfile
    with tempfile.TemporaryDirectory(prefix="E2_externe_") as tmp:
        texte = open(os.path.join(racine, PROGRAMME), encoding="utf-8").read()
        for nom, avant, apres, vise in EXTERNES:
            copie = os.path.join(tmp, "INVENTORIER_SABOTE.py")
            present = texte.count(avant) == 1
            open(copie, "w", encoding="utf-8").write(texte.replace(avant, apres))
            p = subprocess.run([sys.executable, "-I", copie, racine], capture_output=True, text=True, timeout=600)
            echecs = re.findall(r"^(K\d) ÉCHOUE", p.stdout + p.stderr, re.M)
            ok = present and p.returncode == 1 and echecs == [vise]
            tenus += ok
            print(f"  {'TENU ' if ok else 'ÉCHEC'}  {nom} — texte trouvé {present} ; code {p.returncode} (attendu 1) ; "
                  f"calibrages en échec {echecs} (attendu [{vise}])")
    total = len(cas) + len(EXTERNES)
    print(f"CAS : {tenus} / {total} tenus")
    return 0 if tenus == total else 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
