#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait tourner un pas du circuit du soir sans rien en laisser lire au public.

① RÔLE — Exécuter le texte d'un pas du circuit (les commandes écrites sous
  « run: » dans le fichier du circuit) en envoyant TOUT ce qu'il affiche — sa
  sortie et ses erreurs — dans un journal du dépôt privé, et n'afficher dans le
  journal public de GitHub qu'une ligne : « étape … : OK » ou « étape … : ÉCHEC ».
② CONTEXTE D'APPEL — Le circuit du soir qui tourne sur le dépôt PUBLIC
  `cac40-cours-public` (A-543). Il est déclaré comme interpréteur de tous les pas
  (`defaults: run: shell: python3 _code/programmes/ETAPE_MUETTE.py {0}`) : GitHub
  écrit le texte du pas dans un fichier temporaire et en passe le chemin à la
  place de `{0}`. Jamais lancé à la main, sauf par ses épreuves.
③ ENTRÉE — La ligne de commande : UN argument, le chemin du fichier qui porte le
  texte du pas. L'environnement : `GITHUB_WORKSPACE`, le dossier du dépôt privé
  cloné, où le journal est écrit ; `GITHUB_ACTION`, le nom du pas (son `id`) ;
  `GITHUB_RUN_ID` et `GITHUB_RUN_ATTEMPT`, le numéro du passage et de sa
  tentative (une relance garde le même numéro de passage).
④ CONDITIONS D'ENTRÉE — Le fichier du pas existe. `GITHUB_WORKSPACE` est posé et
  on peut y écrire : sinon le pas est déclaré en échec, jamais exécuté en
  silence ailleurs.
⑤ SORTIE — UNE valeur : le code de sortie du pas, rendu tel quel (0 = réussi,
  autre = échec), ou 1 si le journal n'a pas pu être ouvert. Sur l'écran : UNE
  ligne. [rend: 1]
⑥ TRAITEMENT — ① ouvrir, en ajout, `rapports/journal_du_circuit/circuit_<numéro
  du passage>_<tentative>.log` dans le dépôt privé · ② y écrire un en-tête
  « étape, heure de Paris » · ③ lancer `bash -e <fichier>` — la commande même
  que GitHub emploie pour un pas qui ne déclare pas d'interpréteur, comme tous
  les pas du circuit privé (relecture du 08-10-2026 : `-o pipefail` n'en fait
  pas partie) — sortie et erreurs vers le journal · ④ écrire le code de sortie dans le journal · ⑤ afficher une ligne ·
  ⑥ rendre le code.
⑦ UNITÉ — —
⑧ POURQUOI — Le journal d'un dépôt public est lisible par toute personne
  connectée à GitHub. Mesuré par Cowork le 06-10-2026 : il afficherait
  « C5E10-OBS-V1 · jetons illimites : 2 operation(s) · cumul 897.75 EUR »
  (A-543, action ①). Un enrobage UNIQUE pour tous les pas évite de modifier
  chaque pas un par un : deux façons de faire la même chose divergent toujours
  (R-708).
⑨ CE QUI CLOCHE — Les annonces que GitHub lit dans la sortie d'un pas (lignes
  « ::error:: ») partent au journal privé : la page publique ne montre plus
  l'annotation rouge, seulement « ÉCHEC ». Le détail se lit au dépôt privé. Le
  journal n'est enregistré au dépôt privé que par le dernier pas du circuit :
  si la machine tombe avant, le détail est perdu.
⑩ EFFET — ÉCRIT un fichier du dépôt cloné (le journal). Lance un interpréteur
  bash, qui fait ce que le pas demande.
⑪ TERMINAISON — Rend la main quand le pas se termine. Un de mes appels peut ne
  pas revenir : le pas lui-même, qui peut tourner sans fin ; c'est la limite de
  durée de GitHub qui l'arrête alors. [sort: oui]
⑫ DÉFINITIONS
  le circuit du soir : la suite de programmes lancés chaque soir de bourse par
    GitHub Actions — collecte des cours, versement, signaux, positions, mesure,
    pilote, radar.
  un pas : une étape du circuit, avec son nom et ses commandes.
  le dépôt public : `jeanlucsilbertmds-cyber/cac40-cours-public`.
  le dépôt privé : `jeanlucsilbertmds-cyber/Cac-40-signals-sur-git-hub-pour-Claude-`.
"""
import datetime
import os
import subprocess
import sys
from zoneinfo import ZoneInfo

DOSSIER_DU_JOURNAL = os.path.join("rapports", "journal_du_circuit")


def chemin_du_journal(base, passage):
    """Dit où écrire le journal d'un passage.

    ① RÔLE — Fabriquer le chemin du journal du passage dans le dépôt privé.
    ② CONTEXTE D'APPEL — `main`, une fois par pas ; les épreuves.
    ③ ENTRÉE — `base` : le dossier du dépôt privé cloné ; `passage` : le numéro
      du passage et de sa tentative (texte).
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le chemin, texte. [rend: 1]
    ⑥ TRAITEMENT — Joindre la base, le dossier du journal et
      `circuit_<passage>.log`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un fichier par passage et par tentative : tous les pas d'un
      même soir au même endroit, le soir suivant n'écrase rien, et une relance
      n'ajoute rien à un journal déjà enregistré au dépôt — sinon le premier pas
      de commit s'arrêterait sur un fichier suivi modifié (relecture du 08-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return os.path.join(base, DOSSIER_DU_JOURNAL, f"circuit_{passage}.log")


def main():
    """Exécute un pas, journal privé, une ligne publique.

    ① RÔLE — Voir l'en-tête du programme.
    ② CONTEXTE D'APPEL — La ligne de commande, posée par GitHub pour chaque pas.
    ③ ENTRÉE — `sys.argv[1]` : le fichier du pas ; l'environnement de GitHub.
    ④ CONDITIONS D'ENTRÉE — Un argument.
    ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — ÉCRIT le journal ; lance bash.
    ⑪ TERMINAISON — Rend la main quand le pas se termine. [sort: oui]
    """
    pas = os.environ.get("GITHUB_ACTION", "pas-sans-nom")
    if len(sys.argv) != 2:
        print(f"étape {pas} : ÉCHEC — l'enrobage attend un seul argument, il en a reçu {len(sys.argv) - 1}")
        return 1
    base = os.environ.get("GITHUB_WORKSPACE", "")
    if not base or not os.path.isdir(base):
        print(f"étape {pas} : ÉCHEC — GITHUB_WORKSPACE absent : pas exécuté, faute de journal")
        return 1
    chemin = chemin_du_journal(base, os.environ.get("GITHUB_RUN_ID", "sans-numero") + "_"
                               + os.environ.get("GITHUB_RUN_ATTEMPT", "1"))
    heure = datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%d-%m-%Y %Hh%M:%S")
    try:
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        journal = open(chemin, "a", encoding="utf-8")
    except OSError as e:
        print(f"étape {pas} : ÉCHEC — journal impossible à ouvrir ({type(e).__name__}) : pas exécuté")
        return 1
    with journal:
        journal.write(f"\n===== étape {pas} — {heure} (Paris) =====\n")
        journal.flush()
        code = subprocess.run(["bash", "-e", sys.argv[1]],
                              stdout=journal, stderr=subprocess.STDOUT).returncode
        journal.write(f"===== fin de l'étape {pas} : code {code} =====\n")
    if code == 0:
        print(f"étape {pas} : OK")
    else:
        print(f"étape {pas} : ÉCHEC (code {code}) — le détail est au dépôt privé, "
              f"{os.path.relpath(chemin, base)}")
    return code


if __name__ == "__main__":
    sys.exit(main())
