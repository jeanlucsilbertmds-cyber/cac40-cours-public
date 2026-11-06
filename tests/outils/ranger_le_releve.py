#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ranger_le_releve — Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Ranger dans tests/resultats/ d'un clone de la version éprouvée le relevé d'une série jouée ailleurs (GitHub),
  SEULEMENT s'il a été joué sur la pointe de cette version.
② CONTEXTE D'APPEL — Le Chat, après un passage du circuit des séries, sur un clone de la version (sa branche
  « travail-… », ou main), avant de commiter :
  python3 -B tests/outils/ranger_le_releve.py <clone de la version> <relevé lu sur la branche series-longues/…>
③ ENTRÉE — Le clone (un dépôt git sur une branche, avec son « origin ») ; le chemin du relevé à ranger.
④ CONDITIONS D'ENTRÉE — Le relevé porte une ligne « # joué par : … ; commit <sha> ; … » (le joueur l'écrit depuis
  le 05-11-2026, `ligne_joue_par`).
⑤ SORTIE — UNE valeur : le code de sortie. 0 rangé ; 1 refusé (rien n'est écrit) : pas de ligne « joué par », commit
  « inconnu », commit suivi de « MODIFIÉ » (arbre modifié au moment du jeu), clone sur aucune branche, HEAD du clone différente du commit du relevé, ou pointe de la branche à
  « origin » différente (lue par « git ls-remote »), ou relevé dont le nom ne porte pas de date.
⑥ TRAITEMENT — ① lire le commit dans la ligne « joué par » ; refuser « inconnu » et « MODIFIÉ », chacun avec sa
  raison · ② exiger HEAD du clone = ce commit = la pointe distante
  de sa branche · ③ ranger les anciens relevés de la même série dans archives/ (`ranger_les_anciens_releves` du
  joueur, R-708) · ④ copier le relevé dans tests/resultats/ sous son nom.
⑦ UNITÉ — —
⑧ POURQUOI — Superviseur R-759 du 05-11-2026, N2 : « Le rangement est fait par un programme qui exige que le commit
  du relevé soit la pointe de la version » ; ranger à la main permettait de ranger le relevé d'un autre commit
  (R-754 : ce qu'un programme peut faire, un programme le fait). « MODIFIÉ » et « inconnu » : superviseur R-759 du
  05-11-2026, tour 3, M-4 (« le rangeur refuse « MODIFIÉ » et « inconnu » ») — la relecture du tour 2 a rangé un
  relevé joué sur un arbre modifié non commité, que la ligne disait joué sur la pointe.
⑨ CE QUI CLOCHE — Ne commite pas (le Chat commite, avec sa livraison). La pointe distante est lue sur le réseau :
  hors réseau, refus. Ne relit pas les EMPREINTE du relevé (la certification de nuit le fait).
⑩ EFFET — Écrit dans tests/resultats/ et archives/ du clone.
⑪ TERMINAISON — Rend la main ; chaque appel git est borné à 120 s ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys

JOUEUR = os.path.join("tests", "outils", "JOUER_UNE_SERIE_DE_SABOTAGES.py")


def git(clone, *args):
    """Lance git dans le clone ; rend (code, sortie).

    ① RÔLE — Un appel git borné.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `clone`, les arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (code, texte de la sortie, sans blancs autour). [rend: 1]
    ⑥ TRAITEMENT — subprocess.run.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépassement de 120 s lève (code non nul par la trace).
    ⑩ EFFET — Ce que fait git (lecture seulement ici).
    ⑪ TERMINAISON — Rend la main ; 120 s au plus. [sort: non]
    """
    r = subprocess.run(["git", "-C", clone] + list(args), capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout.strip()


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête.
    ⑤ SORTIE — UNE valeur : 0 ou 1. [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Fiche en tête.
    ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if len(sys.argv) != 3:
        print("usage : ranger_le_releve.py <clone de la version> <relevé>")
        return 1
    clone, releve = os.path.realpath(sys.argv[1]), sys.argv[2]
    texte = open(releve, encoding="utf-8").read()
    d = re.search(r"^# joué par : .* ; commit (\S+)( MODIFIÉ)? ; ", texte, re.M)
    if d and d.group(2):
        print(f"REFUS : le relevé a été joué sur un arbre MODIFIÉ (commit {d.group(1)[:12]} plus des changements non "
              "commités) : il ne dit pas le code de la pointe")
        return 1
    if d and d.group(1) == "inconnu":
        print("REFUS : le relevé dit « commit inconnu » (copie sans .git jouée hors du circuit de GitHub)")
        return 1
    # « MODIFIÉ » est admis par cette lecture : seul le refus explicite ci-dessus le juge (une garde, une place)
    m = re.search(r"^# joué par : .* ; commit ([0-9a-f]{40})(?: MODIFIÉ)? ; ", texte, re.M)
    if not m:
        print("REFUS : le relevé ne dit pas sur quel commit il a été joué (ligne « # joué par : … ; commit <sha> »)")
        return 1
    code, branche = git(clone, "symbolic-ref", "-q", "--short", "HEAD")
    _, tete = git(clone, "rev-parse", "HEAD")
    code2, distante = git(clone, "ls-remote", "origin", "refs/heads/" + branche)
    pointe = distante.split()[0] if code == 0 and code2 == 0 and distante else ""
    if not (code == 0 and branche and tete == m.group(1) == pointe):
        print(f"REFUS : relevé joué sur {m.group(1)[:12]}, clone sur {branche or 'aucune branche'} à {tete[:12]}, "
              f"pointe distante {pointe[:12] or 'illisible'} : ce n'est pas la pointe de la version")
        return 1
    spec = importlib.util.spec_from_file_location("JOUEUR", os.path.join(clone, JOUEUR))
    joueur = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(joueur)
    cible = os.path.join("tests", "resultats", os.path.basename(releve))
    if joueur.prefixe_de_la_serie(cible) == os.path.basename(cible):
        print("REFUS : le nom du relevé ne porte pas de date (une seule version vivante se range à la date près)")
        return 1
    for ancien in joueur.ranger_les_anciens_releves(clone, cible):
        print(f"ancien relevé rangé dans archives/ : {ancien}")
    os.makedirs(os.path.join(clone, "tests", "resultats"), exist_ok=True)
    shutil.copyfile(releve, os.path.join(clone, cible))
    print(f"RANGÉ : {cible} (commit {tete[:12]}, pointe de {branche})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
