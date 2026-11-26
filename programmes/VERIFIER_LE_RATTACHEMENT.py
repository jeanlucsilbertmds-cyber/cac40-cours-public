#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie que chaque travail en cours sert une décision prise par Jean-Luc.

① RÔLE — Rendre impossible, en silence, de construire ce que Jean-Luc n'a pas
  demandé. Chaque note de livraison (echanges/A_RELIRE.md d'une branche) doit
  porter une ligne « SERT : A-<nombre> » ; l'action citée doit exister au BACKLOG
  et y être une décision (statut DÉCIDÉ ou TRANCHÉ). Le 25-11-2026, le chemin
  critique a été construit pendant des heures sur une traversée unique, alors
  que Jean-Luc avait décidé le 19-11 (A-923) de faire passer toutes les
  stratégies ; il l'a relevé seul à 20h14.
② CONTEXTE D'APPEL — Par le pilote à chaque passage ; par le maréchal ; par le
  Chat avant toute réponse sur l'avancement (règle 12 du MODE_EMPLOI §13.1quater).
③ ENTRÉE — Ligne de commande : le chemin du BACKLOG, puis une ou plusieurs
  paires ÉTIQUETTE=CHEMIN, chaque CHEMIN étant une note A_RELIRE.md lue sur disque
  (le pilote l'extrait de chaque branche par `git show`).
④ CONDITIONS D'ENTRÉE — Le BACKLOG est le tableau « | A-<n> | … ». Au moins une
  paire.
⑤ SORTIE — Un affichage, une ligne par note, et UN code : 0 toutes rattachées ·
  3 au moins une non rattachée · 2 lecture impossible ou arguments faux.
⑥ TRAITEMENT — Indexer les lignes du BACKLOG par identifiant ; pour chaque note,
  chercher toutes les lignes « SERT : A-n » ; chaque A-n doit exister et porter
  DÉCIDÉ ou TRANCHÉ dans sa ligne ; une note sans ligne SERT est non rattachée.
⑦ UNITÉ — —
⑧ POURQUOI — Un programme qui refuse vaut mieux qu'une promesse de vigilance.
⑨ CE QUI CLOCHE — Le programme vérifie que la décision existe, pas que le travail
  la sert vraiment : ce jugement reste au relecteur et au maréchal.
  Relevés du 26-11-2026 (pilote V8, textes seuls, NON corrigés — voir les ⑨ de
  `index_du_backlog` et de `main`) : seule la PREMIÈRE action d'une ligne
  « SERT : A-…, A-… » est vérifiée ; DÉCIDÉ ou TRANCHÉ est cherché dans TOUTE la
  ligne du BACKLOG, pas dans sa colonne statut (« NON TRANCHÉ » suffit) ; une
  action au statut FAIT n'est pas une décision pour ce programme.
⑩ EFFET — Aucun : lecture seule.
⑪ TERMINAISON — Toujours ; aucun appel externe.
"""
import re, sys

SERT = re.compile(r"^\s*SERT\s*:\s*(A-\d+)", re.M)
DECISION = re.compile(r"DÉCIDÉ|TRANCHÉ")


def index_du_backlog(texte):
    """Rend la ligne du BACKLOG de chaque identifiant d'action.

    ① RÔLE — Indexer le tableau du BACKLOG : pour chaque « A-<n> », sa ligne.
    ② CONTEXTE D'APPEL — `main`, une fois, sur le texte entier du BACKLOG.
    ③ ENTRÉE — `texte` : le contenu entier du BACKLOG (une chaîne).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire identifiant « A-<n> » → ligne entière
      (sans sa fin de ligne) ; vide si aucune ligne ne convient.
      [rend: 1]
    ⑥ TRAITEMENT — Découper le texte en lignes ; garder celles qui commencent par
      « | A-<nombre> | » ; noter chaque identifiant à sa PREMIÈRE ligne, ignorer
      les suivantes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `main` doit retrouver vite la ligne de chaque action citée par
      une note, pour y chercher DÉCIDÉ ou TRANCHÉ.
    ⑨ CE QUI CLOCHE — Un identifiant en double ne garde que sa première ligne ;
      une ligne dont l'identifiant est mal espacé (« |A-12 | ») est ignorée et
      l'action passe pour absente. Consigné, NON corrigé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main à tous les coups ; aucun appel externe.
      [sort: non]
    """
    idx = {}
    for l in texte.split("\n"):
        m = re.match(r"^\| (A-\d+) \|", l)
        if m and m.group(1) not in idx:
            idx[m.group(1)] = l
    return idx


def main(argv):
    """Lit le BACKLOG et chaque note, dit pour chacune si elle sert une décision, rend le code.

    ① RÔLE — Faire le travail du programme en entier : lire, vérifier chaque note,
      afficher une ligne par note et un bilan, rendre le code de sortie.
    ② CONTEXTE D'APPEL — Le bloc `if __name__ == "__main__"`, qui passe
      `sys.argv` et sort avec le code rendu ; une épreuve peut l'appeler aussi.
    ③ ENTRÉE — `argv` : la ligne de commande entière ; argv[0] le nom du
      programme, argv[1] le chemin du BACKLOG, puis une ou plusieurs paires
      ÉTIQUETTE=CHEMIN, chaque CHEMIN une note A_RELIRE.md sur disque.
    ④ CONDITIONS D'ENTRÉE — Au moins trois éléments dans `argv`, et un « = » dans
      chaque paire ; sinon USAGE et code 2.
    ⑤ SORTIE — UNE valeur : le code, 0 toutes les notes rattachées · 3 au moins
      une non rattachée (ou illisible) · 2 arguments faux ou BACKLOG illisible.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier les arguments · ② lire le BACKLOG en UTF-8 et
      l'indexer (`index_du_backlog`) · ③ pour chaque paire : lire la note (illisible
      → non rattachée) · ④ relever, par le motif SERT, l'action qui suit
      « SERT : » en tête de chaque ligne · ⑤ aucune → non rattachée · ⑥ une action
      absente de l'index, ou dont la ligne ne contient ni DÉCIDÉ ni TRANCHÉ → non
      rattachée · ⑦ un bilan, puis 3 s'il y a au moins une note non rattachée,
      0 sinon.
    ⑦ UNITÉ — Nombre de notes.
    ⑧ POURQUOI — Un programme qui refuse vaut mieux qu'une promesse de vigilance
      (A-1014, règle 12 de l'outil de planning) : rien ne se construit en silence
      hors d'une décision de Jean-Luc.
    ⑨ CE QUI CLOCHE — ① Le motif SERT ne capture que la PREMIÈRE action d'une
      ligne : « SERT : A-1011, A-1014, A-1055 » ne vérifie qu'A-1011 ; mesuré le
      26-11-2026 sur le BACKLOG de travail-carte : cette ligne → « NON RATTACHÉ …
      A-1011 », A-1014 et A-1055 jamais regardées. ② DÉCIDÉ ou TRANCHÉ est cherché
      dans TOUTE la ligne, pas dans la colonne statut : A-1055 (statut CONSTAT)
      passe parce que son texte écrit « NON TRANCHÉ » ; A-1011 (statut FAIT, une
      demande de Jean-Luc exécutée) ne passe pas. ③ Une ligne « SERT : » placée
      n'importe où dans la note compte, même citée en exemple. Consigné, NON
      corrigé.
    ⑩ EFFET — Écrit sur la sortie standard ; lit les fichiers nommés. N'écrit
      aucun fichier.
    ⑪ TERMINAISON — Rend la main à tous les coups ; aucun appel externe ; une
      lecture de fichier peut attendre si un CHEMIN désigne un tube nommé.
      [sort: non]
    """
    if len(argv) < 3 or any("=" not in a for a in argv[2:]):
        print("USAGE : VERIFIER_LE_RATTACHEMENT.py <BACKLOG> ETIQUETTE=A_RELIRE.md [...]")
        return 2
    try:
        idx = index_du_backlog(open(argv[1], encoding="utf-8").read())
    except Exception as e:
        print("LECTURE IMPOSSIBLE DU BACKLOG : %s" % e)
        return 2
    mauvais = 0
    for paire in argv[2:]:
        nom, chemin = paire.split("=", 1)
        try:
            note = open(chemin, encoding="utf-8").read()
        except Exception as e:
            print("NON RATTACHÉ %s : note illisible (%s)" % (nom, e))
            mauvais += 1
            continue
        cites = SERT.findall(note)
        if not cites:
            print("NON RATTACHÉ %s : aucune ligne « SERT : A-… » dans la note" % nom)
            mauvais += 1
            continue
        fautes = [a for a in cites if a not in idx or not DECISION.search(idx[a])]
        if fautes:
            print("NON RATTACHÉ %s : %s absente(s) du BACKLOG ou non décidée(s)" % (nom, ", ".join(fautes)))
            mauvais += 1
        else:
            print("RATTACHÉ %s : sert %s" % (nom, ", ".join(cites)))
    print("%d NOTE(S) NON RATTACHÉE(S) SUR %d" % (mauvais, len(argv) - 2))
    return 3 if mauvais else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
