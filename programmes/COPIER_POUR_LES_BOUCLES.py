#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COPIER_POUR_LES_BOUCLES — copie dans le dossier du projet les fichiers dont les boucles Cowork ont besoin.

① RÔLE — Copier, depuis le clone du dépôt, vers le dossier du projet où les boucles Cowork de
  07h05, 08h35 et 21h05 font tourner leurs étapes 3 (signaux) et 5bis (positions), la liste des
  fichiers dont elles ont besoin. Cette liste n'est écrite nulle part : ce programme la DÉRIVE
  des racines RACINES_DE_LA_COPIE_DES_BOUCLES, écrites une fois dans
  programmes/CONTRATS_DES_FICHIERS.py, en suivant les imports réels de chaque programme copié
  (depuis le 16-11-2026, CERT-3 tour 2). Les boucles appellent ce programme au lieu d'épeler
  la liste dans leur texte.
② CONTEXTE D'APPEL — L'étape 5bis des trois boucles, une fois par passage, juste après le
  clone : python3 -B /tmp/depot/programmes/COPIER_POUR_LES_BOUCLES.py /tmp/depot <dossier_du_projet>.
  Aussi les épreuves tests/EPREUVES_DE_LA_COPIE_DES_BOUCLES_Jeu_01-10-2026.py (E2, E5 et E6 le
  lancent, E3 et E4 font tourner ce qu'il a copié ; E1 et E2 lisent la liste que rend sa
  `lire_la_liste`),
  pour que le témoin emprunte le même chemin que la boucle.
③ ENTRÉE — `sys.argv[1]` : la racine du clone · `sys.argv[2]` : le dossier du projet.
④ CONDITIONS D'ENTRÉE — Le dossier du projet existe. La racine porte
  programmes/CONTRATS_DES_FICHIERS.py avec RACINES_DE_LA_COPIE_DES_BOUCLES, et chaque racine.
  Si l'une manque, ou si un programme à suivre ne se lit pas en Python, RIEN n'est copié
  (voir ⑤).
⑤ SORTIE — Sur la sortie standard, une ligne par fichier copié (« nom · N octets ·
  empreinte XXXXXXXXXXXXXXXX », les seize premiers caractères du sha256 de la copie), puis
  « COPIE DES BOUCLES : N fichier(s) copié(s) ». Code de sortie : 0 si tout est copié ;
  1 si un argument, le dossier, la liste ou un fichier manque — RIEN n'est copié alors,
  et la ligne commence par « COPIE DES BOUCLES IMPOSSIBLE » (R-734 : ce qui n'a pas pu se
  faire ne rend jamais 0).
⑥ TRAITEMENT — ① lire les racines dans le module des contrats DU CLONE, chargé par son
  chemin, et en dériver la liste (`deriver`) · ② vérifier que chaque fichier existe, AVANT
  d'en copier un seul · ③ copier
  chacun à plat dans le dossier du projet (son seul nom, comme le faisait `cp`) · ④
  relire chaque copie pour en donner la taille et l'empreinte.
⑦ UNITÉ — Des octets ; l'empreinte est un sha256 tronqué à seize caractères.
⑧ POURQUOI — Décision de Jean-Luc du 01-10-2026 à 16h31 (« Fait ce qu'il faut pour réparer
  professionnellement »), puis à 18h19 (« Trouve une solution pour ne pas attendre
  demain »). La fusion du 01-10-2026 à 14h08 a donné deux imports à
  TENIR_LES_POSITIONS.py ; la ligne `cp` des boucles, écrite à la main dans leur texte, ne
  les copiait pas, et les étapes 3 et 5bis tombaient (relecture de Cowork `aff6d33`).
  Deux listes d'une même chose divergent toujours (R-708) : la liste a d'abord vécu dans le
  contrat seul, écrite à la main ; elle se rouvrait à chaque programme gagnant un import, et
  le superviseur R-759 du 15-11-2026 l'a jugée RUSTINE (« Le fond : une liste dérivée des
  imports »). Le code des programmes est désormais la seule source de la liste. Tout
  vérifier avant de copier évite un dossier du projet à moitié mis à jour.
⑨ CE QUI CLOCHE — ① La copie écrase les fichiers de même nom du dossier du projet : c'est
  voulu (le dépôt fait foi, R-736), comme le faisait `cp`. ② Charger le module des
  contrats exécute son code de tête : il ne fait que définir des noms aujourd'hui ; s'il
  se mettait à écrire, ce programme écrirait aussi. ③ La liste copie des fichiers ; un
  dossier entier n'y aurait pas sa place. ④ Les copies sont à plat : deux fichiers de même
  nom dans deux dossiers s'écraseraient — le programme refuse alors de copier.
  ⑤ Une écriture qui échoue en route (disque plein, cible protégée) laisse une copie partielle :
  tout est vérifié avant, mais la copie elle-même n'est pas atomique. Le programme lève alors,
  avec un code non nul, et la boucle s'arrête comme pour « COPIE DES BOUCLES IMPOSSIBLE ».
  ⑥ La dérivation ne voit pas un nom de programme composé à l'exécution, ni un programme que
  le code nomme mais qui manque au clone (elle ne suit que les fichiers qui existent) : c'est
  l'épreuve E6 de tests/EPREUVES_DE_LA_COPIE_DES_BOUCLES_Jeu_01-10-2026.py, l'import de chaque
  programme copié à plat, qui le prend — à l'import seulement, pas dans les fonctions.
⑩ EFFET — Lit le clone ; écrit dans le dossier du projet les seuls fichiers de la liste.
  N'écrit rien dans le clone (pas de cache Python : `sys.dont_write_bytecode`).
⑪ TERMINAISON — Sort par sys.exit, en 0 ou 1. Aucun appel ne peut ne pas revenir : il
  lit et copie des fichiers locaux.
  [sort: oui]
"""
import ast
import hashlib
import importlib.util
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True


def dependances(depot, chemin):
    """Rend les fichiers Python du dépôt dont un fichier dépend par son code.

    ① RÔLE — Dire, pour un programme, ce qu'il faut copier avec lui : la brique de la
      dérivation.
    ② CONTEXTE D'APPEL — `deriver`, une fois par programme atteint.
    ③ ENTRÉE — `depot` : la racine du clone · `chemin` : le programme, relatif à la racine.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et se lit en Python.
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins, relatifs à la racine, des fichiers « X.py »
      que le programme importe (`import X`, `from X import …`, à tous les niveaux du code, une
      fonction comprise) ou dont il écrit le nom « X.py » dans une chaîne de son code (un
      argument, une constante, un tuple parcouru par une boucle) — cherchés dans le dossier
      du programme, puis à la racine du dépôt ; le programme lui-même n'y est pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir l'arbre syntaxique · ② écarter les chaînes posées seules
      comme une instruction (les textes explicatifs : elles ne font rien) · ③ pour chaque nom,
      garder le premier fichier existant, dans le dossier du programme puis à la racine.
    ⑦ UNITÉ — Des chemins sous la racine.
    ⑧ POURQUOI — Deux dossiers, parce que ce sont ceux où l'import d'un programme copié
      trouve un fichier du dépôt : le sien, que Python place en tête de `sys.path`, et la
      racine, que des programmes y ajoutent (programmes/LIRE_LE_CODE.py le fait pour importer
      emp.py ; la liste écrite à la main l'ignorait, relecteur du 16-11-2026, D2). Une
      propriété du code, et non une énumération : un programme renommé, ajouté ou retiré
      change la liste sans que personne l'écrive.
    ⑨ CE QUI CLOCHE — Un nom composé à l'exécution n'est pas vu ; un import relatif est
      ignoré (les programmes ne forment pas un paquet). Un nom de programme cité dans un
      message compte comme une dépendance : la liste s'élargit à tort plutôt que de se taire.
      Un nom qui existe à la fois dans le dossier du programme et à la racine est pris dans le
      dossier du programme, comme le ferait Python.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève sur un fichier illisible.
      [sort: non]
    """
    source = os.path.join(depot, chemin)
    dossiers = (os.path.dirname(source), depot)
    arbre = ast.parse(open(source, encoding="utf-8").read())
    seules = {id(n.value) for n in ast.walk(arbre) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)}
    noms = set()
    for n in ast.walk(arbre):
        if isinstance(n, ast.Import):
            noms |= {a.name.split(".")[0] + ".py" for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
            noms.add(n.module.split(".")[0] + ".py")
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in seules:
            noms |= set(re.findall(r"[A-Za-z0-9_\-]+\.py\b", n.value))
    trouves = set()
    for nom in noms:
        for d in dossiers:
            if os.path.isfile(os.path.join(d, nom)):
                trouves.add(os.path.relpath(os.path.join(d, nom), depot).replace(os.sep, "/"))
                break
    trouves.discard(chemin)
    return trouves


def deriver(depot, racines):
    """Rend la liste des fichiers à copier : les racines et tout ce dont leurs programmes dépendent.

    ① RÔLE — Fabriquer la liste des boucles depuis le code, au lieu de la lire écrite à la main.
    ② CONTEXTE D'APPEL — `lire_la_liste`, une fois.
    ③ ENTRÉE — `depot` : la racine du clone · `racines` : des chemins sous la racine.
    ④ CONDITIONS D'ENTRÉE — Chaque racine qui finit par « .py » existe et se lit en Python ;
      une racine absente est laissée dans la liste, et `main` la refuse.
    ⑤ SORTIE — UNE valeur : la liste des chemins, les programmes d'abord, triés, puis les
      autres racines dans l'ordre où le contrat les écrit.
      [rend: 1]
    ⑥ TRAITEMENT — fermeture : partir des racines programmes, ajouter les dépendances de chaque
      programme atteint (`dependances`) jusqu'à ce que rien ne s'ajoute.
    ⑦ UNITÉ — Des chemins sous la racine.
    ⑧ POURQUOI — Les programmes d'abord et triés : un ordre qui ne dépend que du code. Les
      racines de données à la fin : l'épreuve E5 retire le DERNIER fichier de la liste, et seul
      un fichier déclaré peut manquer de façon visible (un programme absent n'est simplement
      pas atteint, ⑥ de la fiche en tête).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main : chaque programme n'est lu qu'une fois et le dépôt est fini.
      [sort: non]
    """
    a_lire = [r for r in racines if r.endswith(".py") and os.path.isfile(os.path.join(depot, r))]
    vus = set()
    while a_lire:
        p = a_lire.pop()
        if p not in vus:
            vus.add(p)
            a_lire.extend(sorted(dependances(depot, p) - vus))
    absents = [r for r in racines if r.endswith(".py") and r not in vus]
    return sorted(vus) + absents + [r for r in racines if not r.endswith(".py")]


def lire_la_liste(depot):
    """Rend la liste des fichiers que copient les boucles, dérivée des racines du contrat du clone donné.

    ① RÔLE — Prendre les racines là où elles sont écrites, jamais les recopier (R-708), et en
      dériver la liste.
    ② CONTEXTE D'APPEL — `main`, une fois ; l'épreuve de la copie des boucles, pour lire la
      liste de la copie qu'elle éprouve.
    ③ ENTRÉE — `depot` : la racine du clone.
    ④ CONDITIONS D'ENTRÉE — programmes/CONTRATS_DES_FICHIERS.py existe sous la racine.
    ⑤ SORTIE — UNE valeur : la liste des chemins, relatifs à la racine.
      [rend: 1]
    ⑥ TRAITEMENT — charger le module par son chemin, lire RACINES_DE_LA_COPIE_DES_BOUCLES,
      dériver.
    ⑦ UNITÉ — Des chemins sous la racine.
    ⑧ POURQUOI — Charger par le chemin, et non par `sys.path`, garantit que c'est le
      contrat DU CLONE qui est lu, et pas un fichier de même nom laissé dans le dossier
      du projet.
    ⑨ CE QUI CLOCHE — Un module des contrats sans les racines lève AttributeError, un
      programme illisible lève SyntaxError : `main` les transforme en « COPIE DES BOUCLES
      IMPOSSIBLE ».
    ⑩ EFFET — Exécute le code de tête du module des contrats ; lit les programmes suivis.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location(
        "contrats_du_clone", os.path.join(depot, "programmes", "CONTRATS_DES_FICHIERS.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return deriver(depot, list(m.RACINES_DE_LA_COPIE_DES_BOUCLES))


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
        print(f"COPIE DES BOUCLES IMPOSSIBLE — la liste ne se dérive pas de {depot}/programmes/CONTRATS_DES_FICHIERS.py : "
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
