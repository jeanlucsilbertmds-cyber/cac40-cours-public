#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit le tableau du planning pour Jean-Luc à partir de la SORTIE du contrôle, jamais à la main.

① RÔLE — Lancer CONTROLER_UN_PLANNING.py, relever ses lignes « CALCUL étape »,
  et en faire un tableau Markdown : étape · ce qu'elle livre · fenêtre ·
  début et fin au mieux · début et fin réalistes · jalon.
② CONTEXTE D APPEL — `python3 programmes/ECRIRE_LE_TABLEAU.py <dossier> <sortie.md> --maintenant=AAAA-MM-JJTHH:MM`.
③ ENTRÉE — Le dossier du planning, le fichier à écrire, l'heure.
④ CONDITIONS D ENTRÉE — Le contrôle tourne (code 0 ou 1).
⑤ SORTIE — UNE valeur : le code du contrôle (0 accepté, 1 refusé), 2 si impossible.
  [rend: 1]
⑥ TRAITEMENT — Sous-processus du contrôle ; chaque ligne « CALCUL étape X »
  donne fenêtres et heures ; « livre » vient d'etapes.csv (60 caractères au
  plus), le jalon de jalons.csv ; ordre : celui des lignes du contrôle (début
  au mieux, puis début réaliste). Les lignes CALCUL de fin réelle et de
  forfait et le verdict sont recopiés tels quels.
⑦ UNITÉ — heures de Paris.
⑧ POURQUOI — Ce qui se calcule ne s'écrit jamais à la main (R-728).
⑨ CE QUI CLOCHE — Les étapes tenues n'ont pas de ligne CALCUL étape : absentes. Installé dans programmes/
  le 18-11-2026 avec le contrôle qu'il lance (étape PANNES) ; la copie d'étude reste sous etudes/.
⑩ EFFET — Écrit le fichier de sortie.
⑪ TERMINAISON — Un sous-processus local ; revient toujours.
  [sort: non]
"""
import csv
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
R = re.compile(r"^CALCUL étape (\S+) : fenêtre au mieux (\S+) · réaliste (\S+) · au mieux (.+?) → (.+?) · réaliste (.+?) → (.+)$")


def main(argv):
    """Lance le contrôle, relève ses lignes « CALCUL étape » et écrit le tableau Markdown.

    ① RÔLE — Tout le programme (voir la fiche en tête).
    ② CONTEXTE D APPEL — Par la ligne de commande ; par tests/EPREUVES_DU_TUNNEL_DE_PLANIFICATION_Mer_18-11-2026.py (k10).
    ③ ENTRÉE — `argv` : <dossier> <sortie.md> --maintenant=AAAA-MM-JJTHH:MM.
    ④ CONDITIONS D ENTRÉE — Le contrôle à côté ; etapes.csv et jalons.csv lisibles.
    ⑤ SORTIE — UNE valeur : le code du contrôle (0 ou 1), ou 2 si arguments faux ou contrôle impossible.
      [rend: 1]
    ⑥ TRAITEMENT — sous-processus du contrôle ; lignes « CALCUL étape » relevées par l'expression R ; « livre » et
      jalon lus dans les fichiers du planning ; lignes de fin réelle, de forfait et verdict recopiées telles quelles.
    ⑦ UNITÉ — heures de Paris.
    ⑧ POURQUOI — Ce qui se calcule ne s'écrit jamais à la main (R-728).
    ⑨ CE QUI CLOCHE — Les étapes tenues n'ont pas de ligne CALCUL étape : absentes du tableau.
    ⑩ EFFET — Écrit le fichier de sortie.
    ⑪ TERMINAISON — Un sous-processus local, sans délai borné ; revient quand le contrôle revient.
      [sort: non]
    """
    pos = [a for a in argv if not a.startswith("--")]
    opt = [a for a in argv if a.startswith("--maintenant=")]
    if len(pos) != 2 or len(opt) != 1:
        print("ARRET usage : ECRIRE_LE_TABLEAU.py <dossier> <sortie.md> --maintenant=AAAA-MM-JJTHH:MM")
        return 2
    dossier, cible = pos
    p = subprocess.run([sys.executable, os.path.join(ICI, "CONTROLER_UN_PLANNING.py"), dossier, opt[0]],
                       capture_output=True, text=True)
    if p.returncode not in (0, 1):
        print(p.stdout + p.stderr)
        return 2
    lignes = p.stdout.splitlines()
    livre = {e["etape"]: e["livre"] for e in csv.DictReader(open(os.path.join(dossier, "etapes.csv"), encoding="utf-8-sig"), delimiter=";")}
    jalon = {j["jalon"].strip(): j["echeance"] for j in csv.DictReader(open(os.path.join(dossier, "jalons.csv"), encoding="utf-8-sig"), delimiter=";")}
    court = lambda t: (t if len(t) <= 60 else t[:59] + "…").replace("|", "/")
    out = [f"# Planning réel — tiré de la sortie du contrôle", "",
           lignes[0], "",
           "| Étape | Livre | Fenêtre (remise à zéro) | Début au mieux | Fin au mieux | Début réaliste | Fin réaliste | Jalon |",
           "|---|---|---|---|---|---|---|---|"]
    n = 0
    for l in lignes:
        m = R.match(l)
        if not m:
            continue
        i, fm, fr, dm, fmn, dr, frn = m.groups()
        fen = fm if fm == fr else f"au mieux {fm} · réaliste {fr}"
        out.append(f"| {i} | {court(livre.get(i, '?'))} | {fen} | {dm} | {fmn} | {dr} | {frn} | {jalon.get(i, '—')} |")
        n += 1
    out += ["", "Lignes du contrôle, recopiées telles quelles :", ""]
    for l in lignes:
        if (l.startswith("CALCUL fin réelle") or l.startswith("CALCUL forfait") or l.startswith("CALCUL au mieux —")
                or l.startswith("CALCUL réaliste —") or l.startswith("CALCUL limite de concurrence")
                or l.startswith("PLANNING ")):
            out.append(f"- {l}")
    open(cible, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"{n} étapes écrites dans {cible} ; contrôle : {lignes[-1]}")
    return p.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
