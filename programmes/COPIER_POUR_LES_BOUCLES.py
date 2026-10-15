#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COPIER_POUR_LES_BOUCLES — copie dans le dossier du projet les fichiers dont les boucles Cowork ont besoin.

① RÔLE — Copier, depuis le clone du dépôt, la liste COPIE_DES_BOUCLES écrite UNE fois dans
  programmes/CONTRATS_DES_FICHIERS.py, vers le dossier du projet où les boucles Cowork de
  07h05, 08h35 et 21h05 font tourner leurs étapes 3 (signaux) et 5bis (positions). Les
  boucles appellent ce programme au lieu d'épeler la liste dans leur texte.
② CONTEXTE D'APPEL — L'étape 5bis des trois boucles, une fois par passage, juste après le
  clone : python3 -B /tmp/depot/programmes/COPIER_POUR_LES_BOUCLES.py /tmp/depot <dossier_du_projet>.
  Aussi les épreuves tests/EPREUVES_DE_LA_COPIE_DES_BOUCLES_Jeu_01-10-2026.py (E2 à E5),
  pour que le témoin emprunte le même chemin que la boucle.
③ ENTRÉE — `sys.argv[1]` : la racine du clone · `sys.argv[2]` : le dossier du projet.
④ CONDITIONS D'ENTRÉE — Le dossier du projet existe. La racine porte
  programmes/CONTRATS_DES_FICHIERS.py avec COPIE_DES_BOUCLES, et chaque fichier de la liste.
  Si l'une manque, RIEN n'est copié (voir ⑤).
⑤ SORTIE — Sur la sortie standard, une ligne par fichier copié (« nom · N octets ·
  empreinte XXXXXXXXXXXXXXXX », les seize premiers caractères du sha256 de la copie), puis
  « COPIE DES BOUCLES : N fichier(s) copié(s) ». Code de sortie : 0 si tout est copié ;
  1 si un argument, le dossier, la liste ou un fichier manque — RIEN n'est copié alors,
  et la ligne commence par « COPIE DES BOUCLES IMPOSSIBLE » (R-734 : ce qui n'a pas pu se
  faire ne rend jamais 0).
⑥ TRAITEMENT — ① lire la liste dans le module des contrats DU CLONE, chargé par son
  chemin · ② vérifier que chaque fichier existe, AVANT d'en copier un seul · ③ copier
  chacun à plat dans le dossier du projet (son seul nom, comme le faisait `cp`) · ④
  relire chaque copie pour en donner la taille et l'empreinte.
⑦ UNITÉ — Des octets ; l'empreinte est un sha256 tronqué à seize caractères.
⑧ POURQUOI — Décision de Jean-Luc du 01-10-2026 à 16h31 (« Fait ce qu'il faut pour réparer
  professionnellement »), puis à 18h19 (« Trouve une solution pour ne pas attendre
  demain »). La fusion du 01-10-2026 à 14h08 a donné deux imports à
  TENIR_LES_POSITIONS.py ; la ligne `cp` des boucles, écrite à la main dans leur texte, ne
  les copiait pas, et les étapes 3 et 5bis tombaient (relecture de Cowork `aff6d33`).
  Deux listes d'une même chose divergent toujours (R-708) : la liste ne vit plus que dans
  le contrat, et ce programme est le seul à la lire pour copier. Tout vérifier avant de
  copier évite un dossier du projet à moitié mis à jour.
⑨ CE QUI CLOCHE — ① La copie écrase les fichiers de même nom du dossier du projet : c'est
  voulu (le dépôt fait foi, R-736), comme le faisait `cp`. ② Charger le module des
  contrats exécute son code de tête : il ne fait que définir des noms aujourd'hui ; s'il
  se mettait à écrire, ce programme écrirait aussi. ③ La liste copie des fichiers ; un
  dossier entier n'y aurait pas sa place. ④ Les copies sont à plat : deux fichiers de même
  nom dans deux dossiers s'écraseraient — le programme refuse alors de copier.
  ⑤ Une écriture qui échoue en route (disque plein, cible protégée) laisse une copie partielle :
  tout est vérifié avant, mais la copie elle-même n'est pas atomique. Le programme lève alors,
  avec un code non nul, et la boucle s'arrête comme pour « COPIE DES BOUCLES IMPOSSIBLE ».
⑩ EFFET — Lit le clone ; écrit dans le dossier du projet les seuls fichiers de la liste.
  N'écrit rien dans le clone (pas de cache Python : `sys.dont_write_bytecode`).
⑪ TERMINAISON — Sort par sys.exit, en 0 ou 1. Aucun appel ne peut ne pas revenir : il
  lit et copie des fichiers locaux.
  [sort: oui]
"""
import hashlib
import importlib.util
import os
import shutil
import sys

sys.dont_write_bytecode = True


def lire_la_liste(depot):
    """Rend la liste COPIE_DES_BOUCLES lue dans le module des contrats du clone donné.

    ① RÔLE — Prendre la liste là où elle est écrite, jamais la recopier (R-708).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `depot` : la racine du clone.
    ④ CONDITIONS D'ENTRÉE — programmes/CONTRATS_DES_FICHIERS.py existe sous la racine.
    ⑤ SORTIE — UNE valeur : la liste des chemins, relatifs à la racine.
      [rend: 1]
    ⑥ TRAITEMENT — charger le module par son chemin, lire le nom COPIE_DES_BOUCLES.
    ⑦ UNITÉ — Des chemins sous la racine.
    ⑧ POURQUOI — Charger par le chemin, et non par `sys.path`, garantit que c'est le
      contrat DU CLONE qui est lu, et pas un fichier de même nom laissé dans le dossier
      du projet.
    ⑨ CE QUI CLOCHE — Un module des contrats sans COPIE_DES_BOUCLES lève AttributeError :
      `main` le transforme en « COPIE DES BOUCLES IMPOSSIBLE ».
    ⑩ EFFET — Exécute le code de tête du module des contrats.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location(
        "contrats_du_clone", os.path.join(depot, "programmes", "CONTRATS_DES_FICHIERS.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return list(m.COPIE_DES_BOUCLES)


def empreinte(chemin):
    """Rend les seize premiers caractères du sha256 d'un fichier.

    ① RÔLE — Dire ce qui a été copié, au caractère près.
    ② CONTEXTE D'APPEL — `main`, une fois par fichier copié.
    ③ ENTRÉE — `chemin` : un fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — lire les octets, hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les boucles relèvent déjà la taille et l'empreinte du programme des
      positions avant de le lancer (le 01-09-2026, une tâche avait réécrit son script de
      mémoire) : la ligne est donnée ici pour chaque fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:16]


def main():
    """Copie la liste, ou ne copie rien et dit pourquoi.

    ① RÔLE — Le programme entier (voir la fiche en tête).
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv[1]` : la racine du clone · `sys.argv[2]` : le dossier du projet.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête.
    ⑤ SORTIE — Le code de sortie, 0 ou 1, passé à sys.exit.
      [rend: 1]
    ⑥ TRAITEMENT — lire la liste · vérifier chaque fichier · copier · relever.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit les fichiers de la liste dans le dossier du projet.
    ⑪ TERMINAISON — Rend la main au bloc de lancement.
      [sort: non]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print("COPIE DES BOUCLES IMPOSSIBLE — usage : COPIER_POUR_LES_BOUCLES.py <racine du clone> <dossier du projet>")
        return 1
    depot, dossier = (os.path.abspath(a) for a in args)
    if not os.path.isdir(dossier):
        print(f"COPIE DES BOUCLES IMPOSSIBLE — le dossier du projet n'existe pas : {dossier}. Rien n'est copié.")
        return 1
    try:
        liste = lire_la_liste(depot)
    except Exception as e:
        print(f"COPIE DES BOUCLES IMPOSSIBLE — la liste ne se lit pas dans {depot}/programmes/CONTRATS_DES_FICHIERS.py : "
              f"{type(e).__name__}: {e}. Rien n'est copié.")
        return 1
    manquants = [f for f in liste if not os.path.isfile(os.path.join(depot, f))]
    noms = [os.path.basename(f) for f in liste]
    doubles = sorted({n for n in noms if noms.count(n) > 1})
    if not liste or manquants or doubles:
        print("COPIE DES BOUCLES IMPOSSIBLE — " + ("la liste est vide" if not liste else
              "absents du clone : " + ", ".join(manquants) if manquants else
              "deux fichiers de la liste portent le même nom et s'écraseraient : " + ", ".join(doubles))
              + ". Rien n'est copié.")
        return 1
    for f in liste:
        cible = os.path.join(dossier, os.path.basename(f))
        shutil.copyfile(os.path.join(depot, f), cible)
        print(f"{os.path.basename(f)} · {os.path.getsize(cible)} octets · empreinte {empreinte(cible)}")
    print(f"COPIE DES BOUCLES : {len(liste)} fichier(s) copié(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
