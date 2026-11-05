#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_REGISTRE_DES_STRATEGIES — Jeu 05-11-2026 (Paris)
EN ESSAI · Rôle : prouver que le registre des stratégies se NOMME et se LIT à un seul endroit, le contrat des fichiers
(programmes/CONTRATS_DES_FICHIERS.py), que la lecture y rend, pour chaque identifiant, sa DERNIÈRE ligne, et qu'aucun
autre programme ne nomme ce fichier ni n'en lit l'historique. Et que ces épreuves ont des dents. SIMULATION
UNIQUEMENT.
Quand l'appeler : à toute livraison qui touche le registre des stratégies, sa lecture, ou un programme qui le lit ;
la vérification de version la lance d'elle-même chaque nuit.

À QUOI ÇA SERT, EN FRANÇAIS SIMPLE. Décision de Jean-Luc n°83, du 01-11-2026 à 12h33, réponse « 1 » : « Quand une
stratégie a deux lignes au registre […] 1. La dernière ligne ajoutée fait foi. Les précédentes restent comme
historique. » On n'efface jamais une ligne du registre, on en ajoute une (R-727). Le 05-11-2026, une stratégie
(C5-EI-PARAMS) y avait deux lignes depuis la décision n°53, et les programmes n'en retenaient pas la même : le teneur
de positions gardait la dernière, JOUER_LES_VERSIONS refusait la fiche, le juge à 8 critères prenait la première, le
juge des stratégies jugeait les deux. Deux lectures d'une même chose divergent toujours (R-708). Depuis le tour de
n°83 (05-11-2026), le NOM du fichier et sa LECTURE vivent une fois, au contrat, et tous les programmes qui le lisaient
passent par là. Mais « tous les programmes passent par là » ne se prouve pas par une liste : un lecteur écrit demain
à sa façon ne serait vu par personne (superviseur R-759 du 05-11-2026, défaut 3 : « une énumération »). D'où le
GARDE-FOU PAR PROPRIÉTÉ de G1 : aucune constante du code, hors du contrat, ne nomme le fichier du registre. Et,
depuis le tour court du 05-11-2026 (superviseur R-759 de 09h05, propriété P1), celui de G4 : aucun programme hors du
contrat n'appelle la lecture de l'HISTORIQUE (`lignes_du_registre`, toutes les lignes, doublons compris). Mesuré ce
matin-là : un juge à 8 critères ou un teneur de positions ramenés à toutes les lignes EN PASSANT PAR LE CONTRAT
laissaient G1 vert, et le teneur aurait ouvert les positions simulées de C5E10-QA-V1 avec l'ANCIEN objectif.

LES CAS, DANS UNE COPIE DU DÉPÔT (sans .git, etudes, caches) :
  G1 le garde-fou : dans chaque fichier `.py` de la copie, hors des dossiers de traces (etudes, archives) et hors du
     module du contrat, aucune constante de texte du CODE (les textes explicatifs des modules, classes et fonctions
     exclus ; les commentaires ne sont pas du code) ne nomme le fichier du registre. Le motif se TIRE du contrat : le
     nom du fichier sans son extension, soulignés ou espaces, sans lettre, chiffre ni souligné collé avant ou après —
     « donnees/cac40_strategies.csv », « cac40 strategies.csv » et « cac40_strategies » le nomment ;
     « TEMOIN_cac40_strategies_DU_10-10-2026_JEU_DES_COMPTABILITES.csv » (un autre fichier, le témoin figé d'une
     épreuve) ne le nomme pas.
  G2 la lecture : sur le VRAI registre de la copie (R-732), chaque identifiant écrit plusieurs fois rend sa dernière
     ligne, et chaque fiche est rangée À LA PLACE DE SA DERNIÈRE LIGNE (superviseur R-759 du 05-11-2026 à 09h05, D1 :
     le cockpit lit cette place comme une date ; au 05-11-2026, C5-EI-PARAMS, 64e et 69e lignes, vient après
     C5E10-TP5-SL5, 68e) ; sur un registre fabriqué (X écrit trois fois, Y une fois entre la 1re et la 2e ligne de
     X), X rend sa troisième ligne et l'ordre est Y puis X ; `chemin_du_registre` trouve le fichier sous `donnees/`
     puis à plat.
  G3 le motif de G1, calibré sur un arbre fabriqué (« un motif de recherche se calibre sur un cas connu, et sur un cas
     qui doit échouer ») : une constante, une f-chaîne, un nom à espaces et un morceau de nom sont vus ; un texte
     explicatif, le nom du témoin, un nom plus long et un fichier rangé sous etudes/ ne le sont pas.
  G4 l'historique réservé (P1) : dans chaque fichier `.py` sous `programmes/` de la copie, hors des dossiers de traces
     et hors du module du contrat, aucun appel, import ni mention de code de `lignes_du_registre` (le nom est pris au
     contrat de la copie, `lignes_du_registre.__name__`) ; puis le même relevé, CALIBRÉ sur un arbre fabriqué : un
     appel par le module, un import du nom, une référence sans appel et un `getattr` par le nom en texte, sous un
     sous-dossier, sont vus ; un texte explicatif, un commentaire, un appel depuis tests/, un nom plus long, une autre
     fonction du contrat et le contrat lui-même ne le sont pas.

USAGE : python3 -B tests/EPREUVES_DU_REGISTRE_DES_STRATEGIES_Jeu_05-11-2026.py <racine> [--saboter | nom]
  sans option : Z0, le dépôt tel quel ; --saboter : Z0 puis chaque sabotage ; un nom de sabotage : celui-là seul.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable ou si le nom demandé n'existe pas (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; et par la vérification de version (`programmes/CERTIFIER_LA_VERSION.py`), qui lance
  chaque épreuve de tests/ depuis la racine avec la racine en argument, et avec `--saboter`. Ce programme se relance
  lui-même avec « --cas <copie> » pour jouer les cas dans une copie : ce mode n'est pas fait pour la main.
③ ENTRÉE — La racine du dépôt ; `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : le contrat des fichiers (programmes/CONTRATS_DES_FICHIERS.py) avec
  REGISTRE_DES_STRATEGIES, NOM_DU_REGISTRE_DES_STRATEGIES, `chemin_du_registre`, `lignes_du_registre`,
  `fiches_du_registre`, `lire_les_fiches` ; le registre des stratégies.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage. [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① copier la racine dans un dossier temporaire (sans .git, etudes,
  caches) · ② appliquer le sabotage à la copie (remplacer un texte qui doit y être une fois, ou déposer un fichier
  neuf) · ③ relancer la copie de ce programme en mode « --cas » · ④ Z0 doit être vert, un sabotage doit faire échouer
  au moins un cas.
⑦ UNITÉ — Des fichiers, des lignes du registre, des fiches.
⑧ POURQUOI — Superviseur R-759 du 05-11-2026 (défaut 3) : « Le NOM du fichier du registre et sa LECTURE vivent une
  fois, dans programmes/CONTRATS_DES_FICHIERS.py » ; « Garde-fou par propriété : aucune constante de CODE hors de ce
  module ne nomme le fichier du registre (lecture par l'arbre syntaxique, docstrings exclues). Un lecteur neuf qui le
  lit à sa façon rougit sans que personne pense à lui. » Le critère, en une question : si je renomme un fichier, ce
  contrôle change-t-il d'avis ? Non : il ne nomme aucun programme, et son motif vient du contrat. Un jeu d'épreuves se
  sabote contre sa propre correction (R-731).
⑨ CE QUI CLOCHE — ① G1 voit le NOM, pas la LECTURE ; G4 voit l'appel de l'HISTORIQUE du contrat. Ne sont pas vus :
  un programme qui prend le nom au contrat puis lit le fichier à sa façon (`csv.DictReader` sur toutes les lignes,
  `COMMUN.lire_csv` comme PREPARER et DECLINER), un nom concaténé, un `glob`, un nom en `bytes` ; ni une NOUVELLE
  fonction de lecture ajoutée AU CONTRAT lui-même (il est exempté par construction : cela relève de la relecture du
  contrat, R-731). La propriété dynamique P2 (« le fichier du registre n'est OUVERT que depuis le contrat », mesurée
  par l'évènement d'audit `open`) est au BACKLOG ; la lecture « dernière ligne » de ces cas repose sur la relecture.
  ② Un nom FABRIQUÉ à l'exécution (« cac40_" + "strategies », un nom lu dans un fichier de données ou
  sur la ligne de commande) n'est pas vu. Cas réel au 05-11-2026 : tests/LANCEMENT_DES_EPREUVES.json passe
  « donnees/cac40_strategies.csv » en argument à programmes/EPREUVES_DE_LA_DECLINAISON.py ; ce fichier de données
  n'est pas du code et n'est pas lu par G1 (au BACKLOG). ③ Les dossiers de traces sont reconnus à leur NOM (etudes,
  archives) : un programme vivant rangé sous un tel dossier échapperait à G1 et à G4. ④ Les fichiers que Python ne
  sait pas lire (syntaxe) sont DITS, et font rougir G1 et G4 (R-734) : un garde-fou qui n'a pas pu lire ne rend pas
  vert. ⑤ G4 ne regarde que `programmes/` : une épreuve rangée sous `programmes/` (comme
  programmes/EPREUVES_DE_LA_DECLINAISON.py) ne pourrait pas appeler `lignes_du_registre` sans le faire rougir ;
  aucune ne le fait au 05-11-2026. ⑥ L'ORDRE gardé par G2 ne dit rien des lecteurs qui RANGENT eux-mêmes (le repli
  du radar range à la première apparition, ⑨ ③ de `fiches_des_lignes`, au BACKLOG avec X7).
⑩ EFFET — Écrit seulement dans des dossiers temporaires, effacés à la fin normale ; `-B` partout, aucun fichier
  compilé.
⑪ TERMINAISON — Sort lui-même. Chaque sous-processus a un délai ; un délai dépassé compte comme un échec.
  [sort: oui]
"""
import ast
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

SOI = "tests/EPREUVES_DU_REGISTRE_DES_STRATEGIES_Jeu_05-11-2026.py"
CON = "programmes/CONTRATS_DES_FICHIERS.py"
# Les dossiers de TRACES (études datées, versions tombées) et les caches : jamais lus par G1 (⑨ ③).
DOSSIERS_ECARTES = {".git", "__pycache__", "_site_travail", "etudes", "archives"}
DELAI = 600   # secondes, pour un lancement « --cas » (mesuré le 05-11-2026 : quelques secondes)

# Le contrat du dépôt de CE fichier, chargé sous un autre nom de module, pour écrire le sabotage S2 sans écrire le nom
# du registre dans ce fichier (G1 le verrait).
_sp = importlib.util.spec_from_file_location(
    "contrat_du_depot_du_garde_fou", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), CON))
_contrat_du_depot = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_contrat_du_depot)

# LES SABOTAGES : (fichier, texte qui doit y être UNE fois, remplacement) ; texte None = déposer un fichier NEUF.
SABOTAGES = {
    # S1 : la lecture rend la PREMIÈRE ligne d'un identifiant écrit deux fois (G2 doit rougir)
    "S1_premiere_ligne_fait_foi": [(CON, "        fiches.pop(cle, None)        # la place de la fiche est celle de sa "
                                         "DERNIÈRE ligne (⑧)\n        fiches[cle] = ligne\n",
                                    "        fiches.setdefault(cle, ligne)\n")],
    # S6 : la valeur reste la dernière ligne, mais la fiche garde la place de sa PREMIÈRE apparition (l'ordre du tour
    # de n°83, D1 du superviseur R-759 du 05-11-2026 à 09h05) — G2 doit rougir par l'ordre seul
    "S6_ordre_de_premiere_apparition": [(CON, "        fiches.pop(cle, None)        # la place de la fiche est celle "
                                              "de sa DERNIÈRE ligne (⑧)\n", "")],
    # S7 : un programme NEUF qui lit l'historique EN PASSANT PAR LE CONTRAT, sans nommer le registre (G1 reste vert,
    # G4 doit rougir) — la forme des sabotages X1 et X5 de la relecture du 05-11-2026, sans nommer aucun programme
    "S7_un_programme_neuf_lit_l_historique": [
        ("programmes/LECTEUR_NEUF_DE_L_HISTORIQUE.py", None,
         '"""Un lecteur écrit demain : il passe par le contrat, mais prend TOUTES les lignes."""\n'
         'from CONTRATS_DES_FICHIERS import REGISTRE_DES_STRATEGIES, lignes_du_registre\n'
         'def premiere(ident):\n'
         '    return next(x for x in lignes_du_registre(REGISTRE_DES_STRATEGIES) if x["id"] == ident)\n')],
    # S8 : le relevé de G4 ne regarde plus les attributs (« C.lignes_du_registre(…) ») — G4 doit rougir par sa
    # calibration (le cas « appel par le module » n'est plus vu)
    "S8_attributs_ignores": [(SOI, "                    or (isinstance(n, ast.Attribute) and n.attr == fonction)\n",
                              "                    or False\n")],
    # S2 : un programme NEUF qui nomme le registre et le lit à sa façon (G1 doit rougir, sans que rien ne le nomme)
    "S2_un_lecteur_neuf_nomme_le_registre": [
        ("programmes/LECTEUR_NEUF_DE_L_EPREUVE.py", None,
         '"""Un lecteur écrit demain, à sa façon."""\nimport csv\nREGISTRE = "%s"\n'
         'def fiches():\n    return list(csv.DictReader(open(REGISTRE, encoding="utf-8-sig")))\n'
         % _contrat_du_depot.REGISTRE_DES_STRATEGIES)],
    # S3 : les textes explicatifs ne sont plus écartés (G3 doit rougir : un texte explicatif serait vu)
    "S3_textes_explicatifs_comptes": [(SOI, "            if id(n) not in explicatifs:\n", "            if True:\n")],
    # S4 : les dossiers de traces ne sont plus écartés (G3 doit rougir : un fichier sous etudes/ serait vu)
    "S4_traces_comptees": [(SOI, "        sd[:] = [x for x in sd if x not in DOSSIERS_ECARTES]\n",
                            "        sd[:] = [x for x in sd if x in (\".git\",)]\n")],
    # S5 : le motif ne regarde plus ce qui suit le nom (G3 doit rougir : le nom du témoin serait vu)
    "S5_motif_sans_bord_droit": [(SOI, "    return re.compile(r\"(?<![A-Za-z0-9])\" + coeur + r\"(?![A-Za-z0-9_])\")\n",
                                  "    return re.compile(r\"(?<![A-Za-z0-9])\" + coeur)\n")],
}


def motif_du_nom(nom_du_fichier):
    """Rend le motif qui reconnaît le nom du registre dans un texte, tiré du nom que le contrat déclare.

    ① RÔLE — Dire, sans écrire le nom ici, ce qui « nomme le fichier du registre ».
    ② CONTEXTE D'APPEL — `constantes_qui_nomment`, une fois par appel.
    ③ ENTRÉE — `nom_du_fichier` : NOM_DU_REGISTRE_DES_STRATEGIES du contrat (par exemple « cac40_strategies.csv »).
    ④ CONDITIONS D'ENTRÉE — Un nom de fichier avec une extension.
    ⑤ SORTIE — UNE valeur : une expression rationnelle compilée. [rend: 1]
    ⑥ TRAITEMENT — ① ôter l'extension · ② accepter un souligné OU une espace à la place de chaque souligné · ③ exiger
      qu'aucune lettre ni aucun chiffre ne précède, et qu'aucune lettre, chiffre ni souligné ne suive.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les graphies que les programmes employaient avant n°83 : « donnees/cac40_strategies.csv »,
      « cac40_strategies.csv », « cac40 strategies.csv », le morceau « cac40_strategies » (le radar, le contrôle des
      valeurs). Le bord droit écarte les autres fichiers dont le nom COMMENCE pareil (le témoin figé des
      comptabilités, « …_DU_10-10-2026… »).
    ⑨ CE QUI CLOCHE — Un nom découpé (« cac40_" + "strategies ») n'est pas reconnu (⑨ ② de l'en-tête).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    coeur = "[_ ]".join(re.escape(x) for x in os.path.splitext(nom_du_fichier)[0].split("_"))
    return re.compile(r"(?<![A-Za-z0-9])" + coeur + r"(?![A-Za-z0-9_])")


def constantes_qui_nomment(racine, nom_du_fichier, module_du_contrat):
    """Relève, dans le code de la racine, chaque constante de texte qui nomme le fichier du registre (G1, G3).

    ① RÔLE — Le garde-fou par propriété de n°83 : trouver un programme qui nomme le registre ailleurs qu'au contrat.
    ② CONTEXTE D'APPEL — `cas`, pour G1 (la copie du dépôt) et pour G3 (un arbre fabriqué).
    ③ ENTRÉE — `racine` : le dossier fouillé · `nom_du_fichier` : NOM_DU_REGISTRE_DES_STRATEGIES · `module_du_contrat` :
      le chemin du fichier du contrat chargé, seul fichier exempté (None : aucun).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des (chemin relatif, ligne, début du texte) trouvés ; la liste des fichiers que
      Python n'a pas su lire, (chemin relatif, erreur). [rend: 2]
    ⑥ TRAITEMENT — ① descendre la racine, hors des DOSSIERS_ECARTES · ② lire chaque `.py` par l'arbre syntaxique ·
      ③ écarter les textes explicatifs (la première expression texte d'un module, d'une classe, d'une fonction) ·
      ④ garder chaque autre constante de texte, morceaux de f-chaînes compris, que `motif_du_nom` reconnaît.
    ⑦ UNITÉ — Des lignes de fichier.
    ⑧ POURQUOI — Voir ⑧ de l'en-tête. L'arbre syntaxique, et non une recherche de texte : un commentaire ou un texte
      explicatif qui CITE le registre ne le lit pas (au 05-11-2026, des dizaines de textes explicatifs le citent).
    ⑨ CE QUI CLOCHE — Voir ⑨ de l'en-tête.
    ⑩ EFFET — Lit les fichiers ; n'en exécute aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    motif = motif_du_nom(nom_du_fichier)
    trouves, illisibles = [], []
    for d, sd, fs in os.walk(racine):
        sd[:] = [x for x in sd if x not in DOSSIERS_ECARTES]
        for f in sorted(fs):
            if not f.endswith(".py"):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, racine)
            if module_du_contrat and os.path.exists(module_du_contrat) and os.path.samefile(p, module_du_contrat):
                continue
            try:
                arbre = ast.parse(open(p, encoding="utf-8").read())
            except (SyntaxError, UnicodeDecodeError, ValueError) as e:
                illisibles.append((rel, type(e).__name__))
                continue
            explicatifs = set()
            for n in ast.walk(arbre):
                if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
                    e0 = n.body[0]
                    if isinstance(e0, ast.Expr) and isinstance(e0.value, ast.Constant) and isinstance(e0.value.value, str):
                        explicatifs.add(id(e0.value))
            for n in ast.walk(arbre):
                if not (isinstance(n, ast.Constant) and isinstance(n.value, str) and motif.search(n.value)):
                    continue
                if id(n) not in explicatifs:
                    trouves.append((rel, n.lineno, n.value[:80].replace("\n", "⏎")))
    return trouves, illisibles


def appels_de_l_historique(racine, fonction, module_du_contrat):
    """Relève, sous `programmes/` de la racine, chaque mention de code de la lecture de l'historique (G4, P1).

    ① RÔLE — La propriété P1 : la lecture de TOUTES les lignes du registre est réservée au contrat et aux épreuves.
    ② CONTEXTE D'APPEL — `cas`, pour G4 : une fois sur la copie du dépôt, une fois sur l'arbre fabriqué.
    ③ ENTRÉE — `racine` : le dossier fouillé (seul son sous-dossier `programmes/` est lu) · `fonction` : le nom de la
      fonction d'historique, pris au contrat (`lignes_du_registre.__name__`) · `module_du_contrat` : le chemin du
      fichier du contrat, seul fichier exempté (None : aucun).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des (chemin relatif à la racine, ligne, forme) trouvés ; la liste des fichiers
      que Python n'a pas su lire, (chemin relatif, erreur). [rend: 2]
    ⑥ TRAITEMENT — ① descendre `<racine>/programmes`, hors des DOSSIERS_ECARTES · ② lire chaque `.py` par l'arbre
      syntaxique · ③ garder chaque nœud qui porte le nom : un nom (`lignes_du_registre(…)`, une référence), un
      attribut (`C.lignes_du_registre`), un import (`from … import lignes_du_registre`), une constante de texte
      ÉGALE au nom (`getattr(C, "lignes_du_registre")`).
    ⑦ UNITÉ — Des lignes de fichier.
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026 à 09h05 : « P1 (statique, peu coûteuse) : aucun fichier de
      `programmes/` autre que le contrat n'appelle `lignes_du_registre`. Cette lecture de l'historique est réservée aux
      épreuves. » Un programme qui lit toutes les lignes juge une ligne que n°83 a remplacée ; mesuré le même matin
      (relecture, X1 et X5) : le juge à 8 critères ramené à la première ligne, le teneur à toutes les lignes, par le
      contrat, laissaient tout vert. L'arbre syntaxique et non une recherche de texte : un texte explicatif ou un
      commentaire qui CITE la fonction ne l'appelle pas (des textes explicatifs la citent).
    ⑨ CE QUI CLOCHE — Voir ⑨ ①, ③ et ⑤ de l'en-tête : une lecture faite sans cette fonction n'est pas vue (P2, au
      BACKLOG) ; un nom fabriqué (`getattr(C, "lignes_" + "du_registre")`) non plus.
    ⑩ EFFET — Lit les fichiers ; n'en exécute aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    trouves, illisibles = [], []
    for d, sd, fs in os.walk(os.path.join(racine, "programmes")):
        sd[:] = [x for x in sd if x not in DOSSIERS_ECARTES]      # traces et caches, comme G1 (⑨ ③)
        for f in sorted(fs):
            if not f.endswith(".py"):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, racine)
            if module_du_contrat and os.path.exists(module_du_contrat) and os.path.samefile(p, module_du_contrat):
                continue
            try:
                arbre = ast.parse(open(p, encoding="utf-8").read())
            except (SyntaxError, UnicodeDecodeError, ValueError) as e:
                illisibles.append((rel, type(e).__name__))
                continue
            for n in ast.walk(arbre):
                if ((isinstance(n, ast.Name) and n.id == fonction)
                    or (isinstance(n, ast.Attribute) and n.attr == fonction)
                    or (isinstance(n, ast.Constant) and n.value == fonction)):
                    trouves.append((rel, n.lineno, type(n).__name__))
                elif isinstance(n, ast.ImportFrom) and any(a.name == fonction for a in n.names):
                    trouves.append((rel, n.lineno, "ImportFrom"))
    return trouves, illisibles


def cas(copie):
    """Joue G1, G2, G3 et G4 dans une copie, et rend leurs verdicts.

    ① RÔLE — Chaque cas dit vert ou rouge, avec ce qu'il a vu.
    ② CONTEXTE D'APPEL — Le mode « --cas » de ce programme, une fois par copie (Z0 ou un sabotage).
    ③ ENTRÉE — `copie` : la racine d'une copie du dépôt, éventuellement sabotée.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des (nom, réussi, détail). [rend: 1]
    ⑥ TRAITEMENT — ① charger le contrat de la copie · ② G1 sur la copie · ③ G2 sur le vrai registre de la copie, puis
      sur un registre fabriqué et deux dossiers fabriqués · ④ G3 sur un arbre fabriqué · ⑤ G4 sur la copie, puis sur
      un arbre fabriqué ; un cas qui lève compte comme échoué.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Écrit dans des dossiers temporaires, effacés.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    res = []

    def un(nom, f):
        """Joue un cas et range son verdict.

        ① RÔLE — Un seul geste pour tous les cas. ② CONTEXTE D'APPEL — `cas`, une fois par cas. ③ ENTRÉE — `nom` ; `f` :
        la fonction du cas, qui rend (réussi, détail). ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune valeur ; ajoute un
        (nom, réussi, détail) à `res`. [rend: 0] ⑥ TRAITEMENT — Appeler `f` ; une erreur levée compte comme un échec,
        avec son type et son texte. ⑦ UNITÉ — —. ⑧ POURQUOI — Un cas qui plante n'est pas un cas réussi. ⑨ CE QUI
        CLOCHE — —. ⑩ EFFET — Celui de `f`. ⑪ TERMINAISON — Rend la main. [sort: non]
        """
        try:
            ok, detail = f()
        except (Exception, SystemExit) as e:
            ok, detail = False, "%s : %s" % (type(e).__name__, str(e)[:220])
        res.append((nom, bool(ok), detail))

    sys.path.insert(0, os.path.join(copie, "programmes"))
    import CONTRATS_DES_FICHIERS as C
    nom = C.NOM_DU_REGISTRE_DES_STRATEGIES

    def g1():
        """Le cas G1 : aucune constante du code ne nomme le registre hors du contrat.

        ① RÔLE — Voir l'en-tête, G1. ② CONTEXTE D'APPEL — `un`, dans `cas`, une fois. ③ ENTRÉE — Par fermeture :
        `copie`, `nom`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs : réussi, détail. [rend: 2] ⑥ TRAITEMENT —
        `constantes_qui_nomment` sur la copie, le contrat exempté ; vert si rien n'est trouvé et tout s'est lu. ⑦ UNITÉ
        — Des constantes. ⑧ POURQUOI — Voir l'en-tête, ⑧. ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨. ⑩ EFFET — Lit les
        fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
        """
        trouves, illisibles = constantes_qui_nomment(copie, nom, os.path.join(copie, CON))
        return not trouves and not illisibles, "%d constante(s) du code nomment le registre hors du contrat%s%s" % (
            len(trouves), (" : " + " · ".join("%s l.%d %r" % x for x in trouves[:8])) if trouves else "",
            (" ; ILLISIBLES : %s" % illisibles) if illisibles else "")
    un("G1 aucune constante du code ne nomme le registre hors du contrat", g1)

    def g2():
        """Le cas G2 : la lecture rend la dernière ligne de chaque identifiant (n°83).

        ① RÔLE — Voir l'en-tête, G2. ② CONTEXTE D'APPEL — `un`, dans `cas`, une fois. ③ ENTRÉE — Par fermeture :
        `copie`, `nom`, le contrat `C` de la copie. ④ CONDITIONS D'ENTRÉE — Le registre de la copie existe. ⑤ SORTIE —
        DEUX valeurs : réussi, détail. [rend: 2] ⑥ TRAITEMENT — ① sur le vrai registre, comparer les fiches du contrat à
        la dernière ligne de chaque identifiant, relevée ici ligne à ligne, et l'ordre à celui des DERNIÈRES lignes
        (D1 du superviseur R-759 du 05-11-2026 à 09h05) · ② un registre fabriqué (X trois fois, Y une fois entre la
        1re et la 2e ligne de X : l'ordre attendu est Y puis X) · ③ `chemin_du_registre` sous `donnees/` puis à
        plat. ⑦ UNITÉ — Des lignes, des fiches. ⑧ POURQUOI — Décision n°83 et D1 ; un cas réel (R-732) et un cas fabriqué
        qui ne dépend pas de l'état du registre (au 05-11-2026, un seul identifiant y est écrit deux fois). ⑨ CE QUI
        CLOCHE — Si le vrai registre n'a plus aucun identifiant écrit deux fois, la première ligne est vraie sans rien
        prouver ; le registre fabriqué garde la dent. ⑩ EFFET — Écrit un dossier temporaire, effacé. ⑪ TERMINAISON —
        Rend la main. [sort: non]
        """
        vu = {}
        lignes = C.lignes_du_registre(os.path.join(copie, C.REGISTRE_DES_STRATEGIES))
        fiches = C.lire_les_fiches(copie)
        derniere = {}
        for x in lignes:
            derniere[x.get("id") or ""] = x
        doubles = sorted({k for k in derniere if sum(1 for x in lignes if (x.get("id") or "") == k) > 1})
        vu["vrai registre : %d lignes, %d fiches, identifiants écrits plusieurs fois %s, chacun rend sa dernière ligne"
           % (len(lignes), len(fiches), doubles)] = all(fiches[k] is derniere[k] or fiches[k] == derniere[k] for k in doubles)
        place = {}
        for i, x in enumerate(lignes):
            place[x.get("id") or ""] = i          # la place de la DERNIÈRE ligne de chaque identifiant
        attendu = sorted(place, key=place.get)
        vu["vrai registre : chaque fiche est à la place de sa dernière ligne (fin : %s)" % list(fiches)[-3:]] = (
            list(fiches) == attendu)
        d = tempfile.mkdtemp(prefix="registre_epreuve_")
        try:
            os.makedirs(os.path.join(d, "donnees"))
            p = os.path.join(d, C.REGISTRE_DES_STRATEGIES)
            with open(p, "w", encoding="utf-8", newline="") as h:
                h.write("id,v\r\nX,premiere\r\nY,seule\r\nX,deuxieme\r\nX,troisieme\r\n")
            f = C.lire_les_fiches(d)
            vu["registre fabriqué : X rend sa troisième ligne, Y la sienne, ordre Y puis X (%s)"
               % [(k, v["v"]) for k, v in f.items()]] = [(k, v["v"]) for k, v in f.items()] == [("Y", "seule"), ("X", "troisieme")]
            vu["registre fabriqué : l'historique garde les 4 lignes"] = len(C.lignes_du_registre(p)) == 4
            vu["chemin_du_registre trouve donnees/ d'abord"] = C.chemin_du_registre(d) == p
            os.remove(p)
            plat = os.path.join(d, nom)
            open(plat, "w", encoding="utf-8").write("id\r\n")
            vu["chemin_du_registre trouve la copie à plat"] = C.chemin_du_registre(d) == plat
        finally:
            shutil.rmtree(d, ignore_errors=True)
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("G2 la lecture rend la dernière ligne de chaque identifiant (n°83)", g2)

    def g3():
        """Le cas G3 : le motif de G1, calibré sur un arbre fabriqué.

        ① RÔLE — Voir l'en-tête, G3. ② CONTEXTE D'APPEL — `un`, dans `cas`, une fois. ③ ENTRÉE — Par fermeture : `nom`.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs : réussi, détail. [rend: 2] ⑥ TRAITEMENT — Écrire huit
        petits fichiers (quatre « VU_ », quatre « PAS_VU_ », dont un sous etudes/), passer `constantes_qui_nomment`,
        exiger exactement les quatre « VU_ ». ⑦ UNITÉ — Des fichiers. ⑧ POURQUOI — « Un motif de recherche se calibre
        sur un cas connu avant de servir — et sur un cas qui doit échouer, sinon il sur-détecte » (instructions du
        projet, § 4). ⑨ CE QUI CLOCHE — Les cas sont fabriqués : un cas réel de nom découpé n'existe pas (⑨ ② de
        l'en-tête). ⑩ EFFET — Écrit un dossier temporaire, effacé. ⑪ TERMINAISON — Rend la main. [sort: non]
        """
        d = tempfile.mkdtemp(prefix="registre_motif_")
        racine = os.path.splitext(nom)[0]
        fichiers = {
            "programmes/VU_CONSTANTE.py": 'X = "donnees/%s"\n' % nom,
            "programmes/VU_F_CHAINE.py": 'import os\nX = f"{os.sep}%s"\n' % nom,
            "programmes/VU_ESPACES.py": 'X = "%s"\n' % nom.replace("_", " "),
            "programmes/VU_MORCEAU.py": 'X = ["%s"]\n' % racine,
            "programmes/PAS_VU_EXPLICATIF.py": '"""Lit donnees/%s."""\ndef f():\n    """Lit %s."""\n    return 1\n' % (nom, nom),
            "programmes/PAS_VU_TEMOIN.py": 'X = "temoins/TEMOIN_%s_DU_10-10-2026_JEU.csv"\n' % racine,
            "programmes/PAS_VU_PLUS_LONG.py": 'X = "%s_validees.csv"\n' % racine,
            "etudes/PAS_VU_TRACE.py": 'X = "donnees/%s"\n' % nom,
        }
        try:
            for rel, texte in fichiers.items():
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                open(os.path.join(d, rel), "w", encoding="utf-8").write(texte)
            trouves, illisibles = constantes_qui_nomment(d, nom, None)
            vus = sorted({os.path.basename(x[0]) for x in trouves})
        finally:
            shutil.rmtree(d, ignore_errors=True)
        attendus = sorted(os.path.basename(r) for r in fichiers if os.path.basename(r).startswith("VU_"))
        return vus == attendus and not illisibles, "vus %s (attendus %s)%s" % (
            vus, attendus, (" ; illisibles %s" % illisibles) if illisibles else "")
    un("G3 le motif, calibré : quatre cas vus, quatre cas qui doivent échouer", g3)

    def g4():
        """Le cas G4 : aucun programme hors du contrat ne lit l'historique du registre (P1), relevé calibré.

        ① RÔLE — Voir l'en-tête, G4. ② CONTEXTE D'APPEL — `un`, dans `cas`, une fois. ③ ENTRÉE — Par fermeture :
        `copie`, le contrat `C` de la copie. ④ CONDITIONS D'ENTRÉE — Le contrat de la copie déclare `lignes_du_registre`.
        ⑤ SORTIE — DEUX valeurs : réussi, détail. [rend: 2] ⑥ TRAITEMENT — ① `appels_de_l_historique` sur la copie, le
        contrat exempté : rien trouvé, tout lu · ② dix petits fichiers fabriqués (quatre « VU_ », six autres, dont un
        sous tests/ et un contrat exempté), le même relevé, exactement les quatre « VU_ ». ⑦ UNITÉ — Des fichiers.
        ⑧ POURQUOI — P1 (voir `appels_de_l_historique`, ⑧) ; un relevé se calibre sur un cas connu et sur un cas qui
        doit échouer (instructions du projet, § 4). ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨ ① et ⑤. ⑩ EFFET — Écrit un
        dossier temporaire, effacé. ⑪ TERMINAISON — Rend la main. [sort: non]
        """
        fonction = C.lignes_du_registre.__name__
        trouves, illisibles = appels_de_l_historique(copie, fonction, os.path.join(copie, CON))
        reel = not trouves and not illisibles
        d = tempfile.mkdtemp(prefix="registre_historique_")
        explicatif = '"""Ne lit jamais %s."""\ndef f():\n    """Ni %s."""\n    return 1\n' % (fonction, fonction)
        fichiers = {
            "programmes/VU_PAR_LE_MODULE.py": "import CONTRATS_DES_FICHIERS as C\nL = C.%s(C.REGISTRE)\n" % fonction,
            "programmes/VU_IMPORT.py": "from CONTRATS_DES_FICHIERS import %s\n" % fonction,
            "programmes/VU_SANS_APPEL.py": "import CONTRATS_DES_FICHIERS as C\nlire = C.%s\n" % fonction,
            "programmes/sous/VU_GETATTR.py": "import CONTRATS_DES_FICHIERS as C\nL = getattr(C, %r)(1)\n" % fonction,
            "programmes/PAS_VU_EXPLICATIF.py": explicatif,
            "programmes/PAS_VU_COMMENTAIRE.py": "# L = C.%s(p)\nX = 1\n" % fonction,
            "programmes/PAS_VU_PLUS_LONG.py": "import CONTRATS_DES_FICHIERS as C\nL = C.%s_bis(1)\n" % fonction,
            "programmes/PAS_VU_FICHES.py": "import CONTRATS_DES_FICHIERS as C\nL = C.fiches_du_registre(1)\n",
            "programmes/CONTRAT_EXEMPTE.py": "def %s(chemin):\n    return []\n" % fonction,
            "tests/PAS_VU_EPREUVE.py": "import CONTRATS_DES_FICHIERS as C\nL = C.%s(1)\n" % fonction,
        }
        try:
            for rel, texte in fichiers.items():
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                open(os.path.join(d, rel), "w", encoding="utf-8").write(texte)
            t2, i2 = appels_de_l_historique(d, fonction, os.path.join(d, "programmes", "CONTRAT_EXEMPTE.py"))
            vus = sorted({os.path.basename(x[0]) for x in t2})
        finally:
            shutil.rmtree(d, ignore_errors=True)
        attendus = sorted(os.path.basename(r) for r in fichiers if os.path.basename(r).startswith("VU_"))
        calibre = vus == attendus and not i2
        return reel and calibre, "copie : %d mention(s) de %s hors du contrat%s%s %s · calibrage : vus %s (attendus %s) %s" % (
            len(trouves), fonction, (" : " + " · ".join("%s l.%d %s" % x for x in trouves[:8])) if trouves else "",
            (" ; ILLISIBLES : %s" % illisibles) if illisibles else "", "oui" if reel else "NON",
            vus, attendus, "oui" if calibre else "NON")
    un("G4 aucun programme hors du contrat ne lit l'historique du registre (P1)", g4)
    return res


def preparer(depot, sab):
    """Copie le dépôt et y applique un sabotage.

    ① RÔLE — Donner à chaque sabotage sa copie, pour que rien ne touche au dépôt.
    ② CONTEXTE D'APPEL — Le programme principal, une fois par lancement (Z0 ou un sabotage).
    ③ ENTRÉE — `depot` : la racine · `sab` : le nom du sabotage, ou « Z0 ».
    ④ CONDITIONS D'ENTRÉE — Chaque texte visé existe UNE fois dans son fichier ; un fichier neuf n'existe pas encore.
    ⑤ SORTIE — DEUX valeurs : le dossier temporaire et la racine de la copie. [rend: 2]
    ⑥ TRAITEMENT — ① copier sans .git, etudes, caches · ② remplacer chaque texte visé, ou déposer le fichier neuf.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une cible introuvable ne sabote rien : elle lève au lieu de passer pour un sabotage qui mord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un dossier temporaire (dans TMPDIR s'il est posé).
    ⑪ TERMINAISON — Rend la main, ou lève AssertionError. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="registre_strategies_")
    r = os.path.join(d, "r")
    shutil.copytree(depot, r, ignore=shutil.ignore_patterns(".git", "etudes", "__pycache__", "_site_travail"))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(r, f)
        if a is None:
            assert not os.path.exists(p), "%s : le fichier neuf existe déjà : %s" % (sab, f)
            open(p, "w", encoding="utf-8").write(b)
            continue
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, "%s : cible trouvée %d fois dans %s : %r" % (sab, t.count(a), f, a[:60])
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d, r


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--cas":
        resultats = cas(os.path.abspath(sys.argv[2]))
        for nom_du_cas, ok, detail in resultats:
            print(("  ok    " if ok else "  ÉCHEC ") + nom_du_cas + " — " + detail)
        # LE MARQUEUR DE FIN : sans lui, une épreuve interrompue ne passe ni pour verte ni pour mordue
        print("FIN DES CAS : %d" % len(resultats))
        sys.exit(0 if all(ok for _, ok, _ in resultats) else 1)
    _args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not _args:
        print(__doc__.split("① RÔLE")[0])
        sys.exit(2)
    DEPOT = os.path.abspath(_args[0])
    if "--saboter" in sys.argv:
        _choix = ["Z0"] + list(SABOTAGES)
    else:
        _choix = [_args[1]] if len(_args) > 1 else ["Z0"]
        if _choix[0] != "Z0" and _choix[0] not in SABOTAGES:
            print("%s N'EXISTE PAS dans SABOTAGES" % _choix[0])
            sys.exit(2)
    _faute = False
    for sab in _choix:
        t0 = time.time()
        try:
            d, r = preparer(DEPOT, sab)
        except AssertionError as e:
            print("%s NE S'APPLIQUE PLUS : CIBLE INTROUVABLE — %s" % (sab, e))
            sys.exit(2)
        try:
            p = subprocess.run([sys.executable, "-B", os.path.join(r, SOI), "--cas", r], cwd=r, capture_output=True,
                               text=True, timeout=DELAI)
            code, out = p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            code, out = 124, "délai de %d s dépassé" % DELAI
        finally:
            shutil.rmtree(d, ignore_errors=True)
        echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
        fin = "FIN DES CAS : 4" in out
        if sab == "Z0":
            bon = code == 0 and not echecs and fin
            print("Z0 dépôt tel quel : %s" % ("tout vert" if bon else "ROUGE (code %d)" % code))
            print("\n".join(l for l in out.splitlines() if l.strip()))
        else:
            bon = code == 1 and bool(echecs) and fin
            print(("%s mord : %r" % (sab, echecs)) if bon else "%s NE MORD PAS : code %d · %s" % (sab, code, out.strip()[-600:]))
        print("   durée : %d s" % (time.time() - t0))
        sys.stdout.flush()
        _faute = _faute or not bon
    print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
    sys.exit(1 if _faute else 0)
