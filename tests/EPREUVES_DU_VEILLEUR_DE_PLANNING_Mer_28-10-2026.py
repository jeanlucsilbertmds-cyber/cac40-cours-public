#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU VEILLEUR DE PLANNING — lance les épreuves de programmes/TENIR_UN_PLANNING.py et leurs mutations.

Simulation uniquement — aucun ordre réel.

① RÔLE — Faire tourner, depuis tests/, les deux jeux qui éprouvent le veilleur de planning
  (`programmes/TENIR_UN_PLANNING.py`) : `programmes/EPREUVES_TENIR_UN_PLANNING.py`, puis le même avec
  `--mutations`, qui rejoue les épreuves contre des copies du veilleur abîmées chacune d'UNE façon précise.
② CONTEXTE D APPEL — Comme toute épreuve de tests/ : depuis la racine, la racine en argument, par le
  certificateur (`programmes/CERTIFIER_LA_VERSION.py`) et à la main.
③ ENTRÉE — `sys.argv[1]` : la racine du dépôt.
④ CONDITIONS D ENTRÉE — La racine porte `programmes/TENIR_UN_PLANNING.py` et
  `programmes/EPREUVES_TENIR_UN_PLANNING.py`. Sinon : code 2.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si les épreuves passent et si toutes les mutations sont tuées,
  1 sinon, 2 si l'un des deux jeux n'a pas pu tourner. [rend: 1] À l'écran, la dernière ligne de chaque jeu.
⑥ TRAITEMENT — ① vérifier les deux fichiers · ② lancer les épreuves · ③ lancer les mutations · ④ rendre le
  plus grave des deux codes.
⑦ UNITÉ — —
⑧ POURQUOI — Le 28-10-2026, le veilleur a oublié le rendez-vous P1 dès son annonce (BACKLOG A-632 ⑤). Ses
  épreuves vivent dans programmes/ depuis le 25-10-2026 ; la règle R-755 ② veut qu'une épreuve de tests/
  désigne chaque programme modifié. Ce fichier la donne sans déplacer ni recopier les épreuves (R-708).
⑨ CE QUI CLOCHE — Les épreuves de programmes/ sont aussi lancées par le certificateur
  (`tests/LANCEMENT_DES_EPREUVES.json`) : elles tournent deux fois.
⑩ EFFET — Lance deux sous-processus ; chacun écrit et efface ses dossiers temporaires.
⑪ TERMINAISON — Rend la main ; chaque sous-processus est borné à 600 secondes.
  [sort: oui]
"""
import os
import subprocess
import sys


def lancer(racine, options):
    """Lance le jeu d'épreuves du veilleur avec des options et rend son code.

    ① RÔLE — Lancer un des deux jeux.
    ② CONTEXTE D APPEL — `main`, deux fois.
    ③ ENTRÉE — `racine` : la racine du dépôt · `options` : la liste des options (vide, ou `--mutations`).
    ④ CONDITIONS D ENTRÉE — Le jeu d'épreuves existe (vérifié par `main`).
    ⑤ SORTIE — UNE valeur : le code de sortie du jeu, ou 2 s'il n'a pas pu tourner ou a dépassé 600 secondes.
      [rend: 1]
    ⑥ TRAITEMENT — `subprocess.run` avec `-I`, puis afficher la dernière ligne de la sortie.
    ⑦ UNITÉ — secondes pour la borne.
    ⑧ POURQUOI — Un contrôle qui n'a pas pu tourner rend un code non nul (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un sous-processus ; affiche une ligne.
    ⑪ TERMINAISON — Bornée à 600 secondes.
      [sort: non]
    """
    jeu = os.path.join(racine, "programmes", "EPREUVES_TENIR_UN_PLANNING.py")
    try:
        r = subprocess.run([sys.executable, "-B", "-I", jeu] + options, capture_output=True, text=True, timeout=600)
    except Exception as e:
        print(f"IMPOSSIBLE {' '.join(options) or 'épreuves'} : {type(e).__name__} {e}")
        return 2
    lignes = (r.stdout or "").strip().splitlines()
    print(f"{' '.join(options) or 'épreuves'} : code {r.returncode} · {lignes[-1] if lignes else '(rien affiché)'}")
    for l in lignes:
        if l.startswith(("ÉCHEC", "SURVIT", "INTROUVABLE")):
            print("  " + l)
    return r.returncode


def main(argv):
    """Lance les deux jeux et rend le plus grave des deux codes.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D ENTRÉE — Voir le ④ du programme.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2, comme le ⑤ du programme. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — vérifier ; lancer les épreuves ; lancer les mutations ; rendre le plus grave.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les mutations prouvent que les épreuves ont des dents (R-731) : sans elles, un jeu vert ne dit rien.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(argv) < 1:
        print("IMPOSSIBLE : il faut la racine du dépôt en argument")
        return 2
    racine = os.path.realpath(argv[0])
    for f in ("TENIR_UN_PLANNING.py", "EPREUVES_TENIR_UN_PLANNING.py"):
        if not os.path.isfile(os.path.join(racine, "programmes", f)):
            print(f"IMPOSSIBLE : programmes/{f} absent de {racine}")
            return 2
    codes = [lancer(racine, []), lancer(racine, ["--mutations"])]
    return 2 if 2 in codes else (1 if any(codes) else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
