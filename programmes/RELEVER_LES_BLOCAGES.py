#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relève les BLOCAGES écrits par le pilote dans ses derniers rapports au BACKLOG.

① RÔLE — Faire apparaître, en tête de toute réponse sur l'avancement, chaque
  blocage que le pilote a déjà écrit. Le 25-11-2026, le pilote a écrit
  « BLOCAGE » à 16h50 (A-1004) et à 18h16 (A-1009) ; le Chat a répondu à 18h21
  et 18h28 sur l'avancement sans les lire, et Jean-Luc l'a découvert seul à 20h09.
② CONTEXTE D'APPEL — Par le Chat, avant toute réponse sur l'avancement ; par le
  pilote, à la fin de chaque passage (règle 11 du MODE_EMPLOI §13.1quater, A-1011).
③ ENTRÉE — Ligne de commande : le chemin du BACKLOG (« - » = entrée standard),
  puis, facultatif, le nombre N de derniers rapports du pilote à lire (défaut 3).
④ CONDITIONS D'ENTRÉE — Le fichier est le tableau du BACKLOG : une ligne par
  action, commençant par « | A-<nombre> | », dont la 4e case nomme le responsable.
  Un rapport du pilote est une ligne dont cette case contient « Pilote ».
⑤ SORTIE — Un affichage, et un code de sortie, UNE valeur : 0 aucun blocage ·
  3 au moins un blocage · 2 lecture impossible ou aucun rapport du pilote trouvé.
⑥ TRAITEMENT — Lire les lignes ; garder les rapports du pilote dans l'ordre du
  fichier ; prendre les N derniers ; dans chacun, chaque occurrence du mot
  « blocage » (majuscules ou non) est affichée avec 300 caractères autour.
⑦ UNITÉ — Caractères (extraits), nombre de rapports.
⑧ POURQUOI — Un blocage écrit mais non lu équivaut à un blocage caché ; c'est
  un programme qui le relève, pas la vigilance (directive 2 de Jean-Luc).
⑨ CE QUI CLOCHE — Un blocage écrit sans le mot « blocage » n'est pas vu ; un
  « déblocage » ne déclenche pas (mot entier exigé), mais « bloquant » non plus.
  Relevés du 26-11-2026 (pilote V8, textes seuls, NON corrigés — voir les ⑨ de
  `rapports_du_pilote` et de `main`) : un rapport dont le texte porte un « | »
  est ignoré (A-1035, A-1038) ; N = 0 lit tous les rapports, N négatif retire
  les premiers ; un blocage LEVÉ OU ABSENT compte comme un blocage
  (« **BLOCAGE LEVÉ** », A-1020 ; « **Aucun blocage nouveau.** », A-1024, qui
  n'est pas un blocage levé mais une absence).
⑩ EFFET — Aucun : lecture seule.
⑪ TERMINAISON — Toujours ; aucun appel externe.
"""
import re, sys

MOT = re.compile(r"\bblocages?\b", re.I)


def rapports_du_pilote(lignes):
    """Rend les lignes du tableau du BACKLOG dont le responsable est le pilote.

    ① RÔLE — Garder, dans l'ordre du fichier, les lignes d'action écrites par le
      pilote : ce sont ses rapports de passage.
    ② CONTEXTE D'APPEL — `main`, une fois, sur toutes les lignes du BACKLOG.
    ③ ENTRÉE — `lignes` : la liste des lignes du BACKLOG (chaînes, sans leur fin
      de ligne).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des couples (identifiant « A-<n> », ligne
      entière), dans l'ordre des lignes ; vide si aucune ne convient.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne : ① ne garder que celles qui commencent par
      « | A-<nombre> | » · ② la découper en cases sur « | », chaque case sans ses
      blancs · ③ garder la ligne si la case de rang 4 (la colonne responsable,
      après le bord, l'identifiant, le texte et le statut) contient « Pilote ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le tableau du BACKLOG porte le responsable de chaque action dans
      sa quatrième colonne ; un rapport du pilote se reconnaît à elle seule.
    ⑨ CE QUI CLOCHE — Une ligne mal formée est ignorée sans le dire. Un « | » dans
      le texte de l'action décale les cases : la colonne responsable n'est plus en
      rang 4 et le rapport est ignoré ; mesuré le 26-11-2026 sur BACKLOG_DECISIONS.md
      (travail-carte, 4526f7283) : A-1035 et A-1038, rapports du « Pilote V8 », ne
      sont pas relevés (aucun ne porte le mot « blocage » ce jour-là). « Pilote »
      est cherché comme sous-chaîne : « Copilote » serait pris. Consigné, NON
      corrigé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main à tous les coups ; aucun appel externe.
      [sort: non]
    """
    sortie = []
    for l in lignes:
        if not re.match(r"^\| A-\d+ \|", l):
            continue
        cases = [c.strip() for c in l.split("|")]
        if len(cases) > 4 and "Pilote" in cases[4]:
            sortie.append((cases[1], l))
    return sortie


def main(argv):
    """Lit le BACKLOG, relève les mentions de blocage des N derniers rapports du pilote, rend le code.

    ① RÔLE — Faire le travail du programme en entier : lire, relever, afficher,
      rendre le code de sortie.
    ② CONTEXTE D'APPEL — Le bloc `if __name__ == "__main__"`, qui passe
      `sys.argv` et sort avec le code rendu ; une épreuve peut l'appeler aussi.
    ③ ENTRÉE — `argv` : la ligne de commande entière ; argv[0] le nom du
      programme, argv[1] le chemin du BACKLOG ou « - » (entrée standard),
      argv[2], facultatif, le nombre N de derniers rapports à lire (défaut 3).
    ④ CONDITIONS D'ENTRÉE — Deux ou trois éléments dans `argv`, sinon USAGE et
      code 2 ; N doit s'écrire comme un entier, sinon code 2.
    ⑤ SORTIE — UNE valeur : le code, 0 aucune mention de blocage · 3 au moins une ·
      2 arguments faux, lecture impossible ou aucun rapport du pilote trouvé.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier le nombre d'arguments · ② lire N et le texte (fichier
      en UTF-8, ou entrée standard) · ③ `rapports_du_pilote` sur les lignes, garder
      les N derniers · ④ aucun → code 2 · ⑤ pour chaque rapport, chaque mot
      « blocage » ou « blocages » (mot entier, majuscules ou non) est affiché avec
      150 caractères de part et d'autre · ⑥ un bilan, puis 3 s'il y a au moins une
      mention, 0 sinon.
    ⑦ UNITÉ — Caractères pour les extraits ; nombre de rapports pour N.
    ⑧ POURQUOI — Un blocage écrit mais non lu équivaut à un blocage caché (A-1011) ;
      un code de sortie non nul permet à un appelant de s'arrêter sans lire.
    ⑨ CE QUI CLOCHE — N n'est pas borné : « 0 » lit TOUS les rapports (la tranche
      [-0:] est la liste entière) et un nombre négatif retire les premiers au lieu
      de garder les derniers ; mesuré le 26-11-2026 sur le BACKLOG de travail-carte :
      N = 0 → 38 rapports, N = -2 → 36. Le mot est compté même quand le texte dit
      le blocage levé ou absent (« **BLOCAGE LEVÉ** » dans A-1020, « **Aucun
      blocage nouveau.** » dans A-1024, rapports du pilote) : le code 3 dit « le
      mot est écrit », pas « un blocage est en cours ». À l'inverse, un blocage qui
      tient sans que le mot soit réécrit disparaît du relevé (déjà consigné en
      A-1040). Un N illisible est annoncé « LECTURE IMPOSSIBLE », comme un fichier
      absent. Consigné, NON corrigé.
    ⑩ EFFET — Écrit sur la sortie standard ; lit le fichier ou l'entrée standard.
      N'écrit aucun fichier.
    ⑪ TERMINAISON — Rend la main à tous les coups ; la lecture de l'entrée standard
      (« - ») attend la fin de l'entrée : un appel peut ne pas revenir si
      l'entrée standard n'est jamais fermée.
      [sort: non]
    """
    if len(argv) not in (2, 3):
        print("USAGE : RELEVER_LES_BLOCAGES.py <BACKLOG|-> [N]")
        return 2
    try:
        n = int(argv[2]) if len(argv) == 3 else 3
        texte = sys.stdin.read() if argv[1] == "-" else open(argv[1], encoding="utf-8").read()
    except Exception as e:
        print("LECTURE IMPOSSIBLE : %s" % e)
        return 2
    rapports = rapports_du_pilote(texte.split("\n"))[-n:]
    if not rapports:
        print("AUCUN RAPPORT DU PILOTE TROUVÉ — relevé impossible")
        return 2
    vus = 0
    for ident, l in rapports:
        for m in MOT.finditer(l):
            vus += 1
            print("BLOCAGE %s : …%s…" % (ident, l[max(0, m.start() - 150):m.end() + 150]))
    noms = ", ".join(i for i, _ in rapports)
    if vus:
        print("%d MENTION(S) DE BLOCAGE dans les %d derniers rapports du pilote (%s)" % (vus, len(rapports), noms))
        return 3
    print("AUCUN BLOCAGE dans les %d derniers rapports du pilote (%s)" % (len(rapports), noms))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
