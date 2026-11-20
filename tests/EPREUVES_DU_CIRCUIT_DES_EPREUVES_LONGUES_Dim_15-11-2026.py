#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES — Dim 15-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Étape GHUB ② (décisions de Jean-Luc A-809, A-811, A-816 du 15-11-2026, « GitHub en priorité ») : le
circuit .github/workflows/epreuves_longues.yml du dépôt public joue sur GitHub, une machine par épreuve, au plus
PARTS_EN_MEME_TEMPS à la fois, les épreuves longues d'un tenant nommées par une demande. Cette épreuve garde, au dépôt,
les cinq propriétés de l'étape : ① une demande ne porte que des CODES, la commande est figée dans la table ; ② même
groupe de concurrence et même budget de machines que les séries ; ③ la table recense les épreuves longues connues ;
④ rien de privé ne sort (contrôle des fichiers écrits au public, confronté au registre de provenance) ; ⑤ le
rapatriement rend, pour chaque épreuve, le code de sortie et la sortie capturée, dans le dépôt privé. Le relais
(« circuit=epreuve ») est éprouvé par tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py (cas X0 à X13).

① RÔLE — Éprouver la table des épreuves longues (`epreuves_du_circuit` du fabricant), le gabarit EPREUVES, le joueur
  tests/outils/jouer_une_epreuve_longue.py, le rapatrieur tests/outils/rapatrier_les_epreuves_longues.py et le contrôle
  `refus_selon_la_provenance` du fabricant.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine, puis avec --saboter) ;
  à la main avant toute livraison qui touche ces programmes (R-731) :
  python3 tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py <racine> [--saboter | --saboter=SE01,…]
③ ENTRÉE — La racine d'un dépôt : programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, programmes/CERTIFIER_LA_VERSION.py,
  tests/LANCEMENT_DES_EPREUVES.json, tests/outils/jouer_une_part.py, tests/outils/jouer_une_epreuve_longue.py,
  tests/outils/rapatrier_les_epreuves_longues.py, donnees/PROVENANCE_DES_FICHIERS.csv et le plus petit fichier qu'il
  enregistre, les fichiers des épreuves de la table.
④ CONDITIONS D'ENTRÉE — bash, git et jq installés ; aucun réseau (dépôts nus locaux).
⑤ SORTIE — Le code de sortie : 0 si chaque cas ci-dessous donne la réponse attendue et, avec --saboter, si chaque
  sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus ; 3 (CODE_D_OUTILLAGE) sur
  une erreur d'outillage (ErreurDOutillage : place insuffisante pour la copie de P3, copie ou git en échec dans
  celle-ci, JOUENT_P3 incohérente, écart du contrôle d'après P3 dans un tour de sabotage, liste des variables
  locales de git illisible) — l'épreuve n'a pas pu se jouer, aucun verdict n'est rendu. Un P3 non joué (clone
  superficiel) ne change pas le code : la ligne Z0 dit « P1, P2 conformes · P3 NON JOUÉ ».
  [rend: 1]
⑥ TRAITEMENT —
  T (la table, `epreuves_du_circuit`) : T0 le TÉMOIN — les six épreuves exigées par la consigne de l'étape (circuit des
  séries, circuit public, relais, nuit découpée, certification, vente unique) sont dans la table avec leur commande
  « {copie} --saboter » ; T1 chaque épreuve de la table existe dans la racine et le joueur ne la refuse pas (ni lien,
  ni programme interdit nommé) ; T2 une table piégée est refusée pour SA raison : code avec une espace, argument avec
  un point-virgule, arguments sans « {copie} », le « --saboter » d'une série, deux codes égaux à la casse près, un
  chemin qui remonte (« .. »).
  G (le gabarit fabriqué) : G1 EPREUVES est fabriqué sans repère de format non rempli (« %( »), porte le MÊME groupe de
  concurrence que SERIES (GROUPE_DES_MACHINES_LONGUES) et « max-parallel » = PARTS_EN_MEME_TEMPS, sa largeur CALCULÉE
  vaut PARTS_EN_MEME_TEMPS, et la largeur calculée des circuits fabriqués tient dans TACHES_EN_MEME_TEMPS_DU_COMPTE
  (`refus_de_la_largeur`, A-884, 17-11-2026 ; avant : la part plus une marge écrite à la main) ; G2 le filet des gabarits l'accepte, et
  le refuse privé de « persist-credentials: false », poussant vers main, ou signant de l'identité des séries ; G3 le pas
  « Fabriquer la matrice », extrait du gabarit et joué par bash sur une version minuscule, rend la matrice des codes
  demandés, et refuse un code inconnu ; G4 le pas « Jouer l epreuve », joué avec un faux « unshare » qui note sa ligne
  de commande, lance le joueur, réseau coupé, avec la copie, le code et la sortie attendus ; G5 le pas « deposer »,
  joué par bash contre un dépôt privé nu local (l'adresse du privé écrite dans le pas remplacée par lui), pousse la
  sortie et le journal renommé sur epreuves-longues/<passage>/<code>.
  J (le joueur, sur une version minuscule dont la table nomme des épreuves d'essai) : J1 une épreuve qui affiche sa
  ligne de commande et son environnement et rend 3 → code 3, RESULTAT.json au code 3, SORTIE.txt porte la sortie ET
  les erreurs, « --saboter » et la copie, aucune variable des fichiers de commandes de GitHub (posées toutes avant),
  GIT_CONFIG_GLOBAL vide de la machine ; J2 code inconnu → 2, « refus » écrit ; J3 une épreuve qui nomme un programme
  interdit → 2 ; J4 un fichier absent → 2 ; J5 une épreuve qui dort au-delà du délai (DELAI ramené à 2 s) → 124,
  « ARRÊTÉE » ; J6 « --matrice » : l'ordre demandé gardé, un double, une interdite, une absente, et « toutes »
  sur cette table qui porte une interdite, refusés (code 2) ; « toutes » sur la vraie table est éprouvé par le relais (X2).
  R (le rapatrieur, sur le dépôt nu de G5) : R1 deux épreuves déposées (codes 3 et 0) → code 1, BILAN.txt dit les
  deux codes, SORTIE.txt rangée à l'octet ; R2 une branche sans RESULTAT.json → code 2, « RIEN DE SUR » ; R3 un
  passage qui n'est pas un nombre → 2.
  P (la provenance) : P1 sur le VRAI registre de la racine (R-732) : la copie octet pour octet d'un vrai fichier
  enregistré, sous un autre nom, est refusée ; un fichier sous donnees/ aussi ; un lien aussi ; un programme ordinaire
  et un fichier vide passent ; P2 registre absent avec un dossier donnees/ → OSError ; sans l'un ni l'autre → aucun
  refus ; P3 le fabricant en ligne de commande sur une COPIE de la racine que P3 place lui-même sur la branche
  « epreuve-p3 » (`copie_sur_une_branche` : copie ordinaire des fichiers, historique en miroir sans origine), vers
  un clone public neuf de la même branche : code 0 et « 0 refus », et la racine inchangée (tête, références,
  inventaire du disque hors .git). P3 ne dépend donc plus de la branche de la racine : sur la tête détachée de la
  machine de certification (17-11-2026, cause C6), il rougissait sans que rien ne soit cassé. Joué seulement si la
  racine est un clone git non superficiel qui porte tout le dépôt ; avec --saboter, joué aussi dans le tour de
  SE40, qui fait refuser toute branche par le fabricant — SE40 ne mord que si la ligne « P3 fabricant » porte
  « garde sabotée », le texte qu'il injecte (JOUENT_P3). Avant tout git, les variables locales de git (GIT_DIR…)
  sont retirées de l'environnement : P3 n'écrit jamais dans un autre dépôt que sa copie.
  A (l'étage A, `etage_a`) : détaillé dans la fiche de `etage_a` ; depuis le 16-11-2026, A8 (A-857) : le refus
  nomme le blob entier et le remède unique « changer une ligne du fichier publié (comme 32aa88d0) », sans jamais
  proposer de retirer la copie (superviseur R-759 SUPERVISEUR_COPIE_CTL_Lun_16-11-2026.md, M1).
⑦ UNITÉ — Des codes de sortie ; des secondes (J5).
⑧ POURQUOI — R-731 : tout code écrit a ses épreuves au dépôt, avec des sabotages qui mordent chacun pour sa raison.
⑨ CE QUI CLOCHE — Rien n'est joué sur GitHub : actions/checkout et ETAPE_MUETTE sont imités (bash) ; le jeton est
  vide, le dépôt privé est un dépôt nu local ; la vraie identification de github.com reste celle des séries
  (THÉORIQUE ici). Aucune vraie épreuve longue n'est jouée (elles durent de 10 à 90 minutes). Les fonctions
  `pas_du_gabarit` et `resoudre` sont recopiées de l'épreuve du relais : une épreuve importée par une autre
  deviendrait un outil et sortirait de la certification (`lister_les_epreuves`).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 secondes ; sort par sys.exit.
  [sort: oui]
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
CERTIFICATEUR = "programmes/CERTIFIER_LA_VERSION.py"
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
JOUEUR_DES_PARTS = "tests/outils/jouer_une_part.py"
JOUEUR = "tests/outils/jouer_une_epreuve_longue.py"
RAPATRIEUR = "tests/outils/rapatrier_les_epreuves_longues.py"
REGISTRE = "donnees/PROVENANCE_DES_FICHIERS.csv"
JETON = "programmes/FORME_D_UN_JETON.py"     # chargé par `refus_avant_publication` (cas A4), à côté du fabricant
CIRCUIT_PRIVE = ".github/workflows/collecte_abc.yml"   # G1 (A-884) : le circuit du soir est fabriqué de lui
LUS = (FABRICANT, CERTIFICATEUR, TABLE, JOUEUR_DES_PARTS, JOUEUR, RAPATRIEUR, REGISTRE, JETON, CIRCUIT_PRIVE)
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="essai",
               GIT_AUTHOR_EMAIL="essai@essai", GIT_COMMITTER_NAME="essai", GIT_COMMITTER_EMAIL="essai@essai",
               GIT_TERMINAL_PROMPT="0")
# LE TÉMOIN (T0) : les six épreuves exigées par la consigne de l'étape GHUB ② (15-11-2026), recopiées VOLONTAIREMENT :
# c'est la référence fixe qui fait rougir une table d'où l'une aurait disparu ou dont la commande aurait changé.
TEMOIN = {"CircuitSeries": "tests/EPREUVES_DU_CIRCUIT_DES_SERIES_Jeu_05-11-2026.py",
          "CircuitPublic": "tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py",
          "Relais": "tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py",
          "NuitDecoupee": "tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py",
          "Certification": "tests/EPREUVES_DE_LA_CERTIFICATION_Jeu_01-10-2026.py",
          "VenteUnique": "tests/EPREUVES_DE_LA_VENTE_UNIQUE_A_Mer_11-11-2026.py"}
# L'épreuve d'essai de J1 : elle affiche sa ligne de commande, les variables gardées et une ligne d'erreur, rend 3.
MINI = '''import os, sys
print("ARGV", sys.argv[1:])
print("CWD", os.getcwd())
for v in ("GITHUB_ENV", "GITHUB_PATH", "GITHUB_OUTPUT", "GITHUB_STATE", "GITHUB_STEP_SUMMARY", "BASH_ENV", "GIT_CONFIG_GLOBAL", "TEMOIN_ORDINAIRE"):
    print(v + "=" + str(os.environ.get(v)))
print("ERREUR_VUE", file=sys.stderr)
sys.exit(3)
'''
FAUX_UNSHARE = '''#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAUX_UNSHARE_JOURNAL"], "a", encoding="utf-8") as f:
    f.write(json.dumps(sys.argv[1:]) + "\\n")
'''


def lancer(args, env=None, cwd=None):
    """Lance une commande ; rend (code, sortie et erreurs réunies).

    ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — `args`, `env` (GIT_ENV par défaut), `cwd`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, le texte. [rend: 2] ⑥ TRAITEMENT — subprocess, 300 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : rangé parmi les cas faux.
    ⑩ EFFET — Ce que fait la commande. ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, env=env or GIT_ENV, cwd=cwd, timeout=300, errors="replace")
    return p.returncode, p.stdout + p.stderr


def charger(chemin, nom):
    """Charge un programme comme un module, par son chemin.

    ① RÔLE — Appeler les fonctions de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Le code de tête du programme s'exécute. ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pas_du_gabarit(texte, ident):
    """Rend (environnement brut, script) du pas d'identifiant `ident` d'un circuit fabriqué ; (None, "") s'il manque.

    ① RÔLE — Jouer le pas tel que le circuit le porte. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — le texte, l'identifiant.
    ④ CONDITIONS D'ENTRÉE — Le pas porte « id: », éventuellement « env: », puis « run: | ».
    ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — lecture par indentation (recopiée de l'épreuve du relais, fiche
    en tête ⑨). ⑦ UNITÉ — — ⑧ POURQUOI — Ne jamais recopier le script éprouvé. ⑨ CE QUI CLOCHE — Pas un lecteur YAML.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = texte.split("\n")
    debut = [i for i, l in enumerate(lignes) if l.strip() == "id: " + ident]
    if not debut:
        return None, ""
    i = debut[0]
    marge = len(lignes[i]) - len(lignes[i].lstrip())
    env = {}
    while i < len(lignes) and lignes[i].strip() != "run: |":
        if lignes[i].strip() == "env:" and len(lignes[i]) - len(lignes[i].lstrip()) == marge:
            k = i + 1
            while k < len(lignes) and len(lignes[k]) - len(lignes[k].lstrip()) > marge:
                nom, _, valeur = lignes[k].strip().partition(": ")
                env[nom] = valeur
                k += 1
            i = k
            continue
        i += 1
    if i == len(lignes):
        return None, ""
    corps = []
    for l in lignes[i + 1:]:
        if l.strip() and len(l) - len(l.lstrip()) <= marge:
            break
        corps.append(l[marge + 2:])
    return env, "\n".join(corps) + "\n"


def resoudre(env, contexte):
    """Remplace chaque valeur « ${{ x }} » d'un bloc « env: » par contexte[x] (KeyError si absente).

    ① RÔLE — Imiter GitHub. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `env`, `contexte`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {nom : texte}. [rend: 1] ⑥ TRAITEMENT — motif exact « ${{ x }} ». ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Une expression composée lève KeyError. ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    sortie = {}
    for nom, valeur in env.items():
        m = re.fullmatch(r"\$\{\{ ([^}]+) \}\}", valeur)
        sortie[nom] = str(contexte[m.group(1)]) if m else valeur
    return sortie


def plus_petit_enregistre(racine):
    """Rend le chemin relatif du plus petit fichier non vide du registre de provenance présent dans la racine.

    ① RÔLE — Choisir la VRAIE donnée de P1 (R-732). ② CONTEXTE D'APPEL — `tour`, `main`. ③ ENTRÉE — la racine.
    ④ CONDITIONS D'ENTRÉE — Le registre existe. ⑤ SORTIE — UNE valeur : le chemin, ou None. [rend: 1]
    ⑥ TRAITEMENT — csv, taille. ⑦ UNITÉ — — ⑧ POURQUOI — Un petit fichier se recopie vite dans chaque copie sabotée.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit le registre. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import csv
    with open(os.path.join(racine, REGISTRE), encoding="utf-8", newline="") as f:
        chemins = [l["fichier"] for l in csv.DictReader(f)]
    presents = [c for c in chemins if os.path.isfile(os.path.join(racine, c)) and os.path.getsize(os.path.join(racine, c))]
    return min(presents, key=lambda c: os.path.getsize(os.path.join(racine, c))) if presents else None


# La branche nommée sur laquelle P3 place SA copie de la racine, et celle du clone public neuf qu'il fabrique : le
# fabricant n'écrit que dans un clone public de la branche du dépôt privé (`refus_de_branche`). Un nom fixe, propre à
# l'épreuve : il ne doit rien à la branche de la racine, qui peut ne pas en avoir (tête détachée).
BRANCHE_DE_P3 = "epreuve-p3"
# Les sabotages dont le tour joue AUSSI P3 (sur une copie de la vraie racine, `copie_sur_une_branche`), chacun avec
# son FRAGMENT ATTENDU. P3 coûte une fabrication entière (9 s mesurées le 17-11-2026) ; le jouer dans chaque tour de
# sabotage ajouterait cette durée autant de fois qu'il y a de sabotages. Il n'est donc joué que là où un sabotage le
# vise. Un tel sabotage ne « mord » que si une ligne « P3 fabricant » de son tour porte son fragment, cherché dans la
# sortie ENTIÈRE du fabricant : c'est le texte que le sabotage injecte lui-même (pour SE40, « garde sabotée », que le
# fabricant affiche dans « ARRÊT — garde sabotée ; RIEN n'est écrit au dépôt public »). Raison : relecture du
# 17-11-2026, tour 3, MAJEUR 1 — SE40 mordait sur n'importe quel cas faux de son tour, y compris un écart du contrôle
# d'après causé par un autre programme qui écrivait dans la racine ; superviseur R-759, R1. Liste DÉCLARÉE : `main`
# vérifie, avant tout tour, que chaque nom existe dans SABOTAGES, que chaque fichier qu'il vise fait partie de LUS
# (seuls les fichiers LUS passent dans la copie de P3) et que le fragment est un texte non vide, injecté par le
# sabotage et absent du fichier visé tel quel ; sinon, erreur d'outillage.
JOUENT_P3 = {"SE40_garde_d_entree_refuse_tout": "garde sabotée"}
# La garde de place de `copie_sur_une_branche` : la place libre exigée, en multiple de la taille de la source hors .git.
FACTEUR_DE_PLACE = 2
# Le code de sortie de `main` sur une erreur d'outillage : distinct de 0 (conforme), 1 (non conforme), 2 (sabotage
# qui ne s'applique plus).
CODE_D_OUTILLAGE = 3


class ErreurDOutillage(Exception):
    """L'épreuve n'a pas pu se jouer : son outillage a échoué, rien n'est jugé.

    ① RÔLE — Distinguer un échec de l'outillage de l'épreuve (copie de P3, git dans cette copie, place, liste
    JOUENT_P3 incohérente) d'un cas faux du programme éprouvé. ② CONTEXTE D'APPEL — Levée par `copie_sur_une_branche`,
    par le cas P3 de `tour` et par `main` ; relancée par `tour` avant son rangement des erreurs imprévues ; attrapée
    par `main`. ③ ENTRÉE — Le message. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — ⑥ TRAITEMENT — —
    ⑦ UNITÉ — — ⑧ POURQUOI — Relecture de travail-c2-p3 (RELU du 17-11-2026, m4) : une copie de P3 en échec tombait
    dans « erreur imprévue », donc parmi les cas faux, et faisait « mordre » SE40 sans que la garde sabotée ait été
    jugée ; superviseur R-759 du 17-11-2026, Q5. ⑨ CE QUI CLOCHE — — ⑩ EFFET — `main` sort avec CODE_D_OUTILLAGE et
    le message, jamais avec un verdict. ⑪ TERMINAISON — —
    """


def retirer_les_variables_locales_de_git():
    """Retire de os.environ et de GIT_ENV les variables qui désignent un dépôt à git ; rend la liste des noms retirés.

    ① RÔLE — Qu'aucun git de l'épreuve, P3 compris, ne vise un autre dépôt que celui que nomme sa ligne de commande.
    ② CONTEXTE D'APPEL — `main`, une fois, en tête, avant tout git (donc avant tout git de P3).
    ③ ENTRÉE — — (lit os.environ et la liste que donne git lui-même).
    ④ CONDITIONS D'ENTRÉE — git installé.
    ⑤ SORTIE — UNE valeur : la liste des noms effectivement présents et retirés (vide le plus souvent). [rend: 1]
    ⑥ TRAITEMENT — « git rev-parse --local-env-vars » lancé hors de tout dépôt (dossier « / ») et avec un
      environnement qui ne porte que PATH et les deux réglages qui écartent la configuration de la machine (donc déjà
      sans GIT_DIR) : git y nomme LUI-MÊME les variables propres à un dépôt (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE,
      GIT_COMMON_DIR, GIT_OBJECT_DIRECTORY…, quinze avec git 2.43.0, compté le 17-11-2026) ; chacune est retirée de os.environ (lu par les
      fonctions du fabricant appelées ici même) et de GIT_ENV (environnement par défaut de `lancer`). C'est une
      PROPRIÉTÉ demandée à git, pas une liste recopiée ni un motif « GIT_ » : GIT_CONFIG_GLOBAL, posé par GIT_ENV,
      n'en fait pas partie et reste.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du 17-11-2026, tour 3, MINEUR 3 : avec GIT_DIR hérité (crochet git, « rebase -x »), P3
      écrivait dans la racine — tête sur epreuve-p3, « core.bare=false », section « remote.origin » retirée,
      « user.name » posé, « refs/heads/autre » créé ; le contrôle d'après ne le voyait qu'après coup. Superviseur
      R-759, R4 : retirer, avant tout git de P3, les variables que donne « git rev-parse --local-env-vars ». Fait en
      tête de `main` et pour toute l'épreuve, pas pour P3 seul : les autres cas (étage A, G5, R) lancent aussi git,
      et l'épreuve exigée — même verdict avec et sans GIT_DIR — ne tient que si aucun git n'hérite de GIT_DIR.
    ⑨ CE QUI CLOCHE — Si la commande échoue ou ne nomme aucune variable, l'épreuve s'arrête (ErreurDOutillage) au
      lieu de jouer avec un environnement non nettoyé. Une variable qu'une version future de git ajouterait à cette
      liste est retirée sans changer ce code ; une variable qui viserait un dépôt sans figurer dans la liste ne l'est
      pas.
    ⑩ EFFET — Modifie os.environ et GIT_ENV du processus de l'épreuve (jamais l'environnement de l'appelant).
    ⑪ TERMINAISON — Rend la main, ou lève ErreurDOutillage ; le git est borné à 300 s. [sort: non]
    """
    try:
        p = subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True, text=True, cwd="/",
                           timeout=300, env={"PATH": os.environ.get("PATH", ""), "GIT_CONFIG_NOSYSTEM": "1",
                                             "GIT_CONFIG_GLOBAL": os.devnull})
    except (OSError, subprocess.SubprocessError) as e:
        raise ErreurDOutillage(f"git rev-parse --local-env-vars : {type(e).__name__} : {e}")
    noms = p.stdout.split()
    if p.returncode != 0 or not noms:
        raise ErreurDOutillage(f"git rev-parse --local-env-vars : code {p.returncode}, {len(noms)} nom(s) : "
                               f"{(p.stdout + p.stderr)[-200:]}")
    retires = [n for n in noms if n in os.environ or n in GIT_ENV]
    for n in noms:
        os.environ.pop(n, None)
        GIT_ENV.pop(n, None)
    return retires


def inventaire_hors_git(source):
    """Rend l'inventaire du disque de `source`, son « .git » de tête exclu : chemin, taille, date de modification.

    ① RÔLE — Photographier le disque de la racine sans en lire le contenu. ② CONTEXTE D'APPEL — `copie_sur_une_branche`
    (taille, pour la garde de place) ; `tour`, cas P3, avant et après (la racine inchangée).
    ③ ENTRÉE — `source` : le dossier d'un dépôt. ④ CONDITIONS D'ENTRÉE — `source` existe.
    ⑤ SORTIE — UNE valeur : la liste triée des triplets (chemin relatif, taille, mtime_ns), un par dossier, fichier ou
      lien, lus par lstat (un lien n'est pas suivi). [rend: 1]
    ⑥ TRAITEMENT — os.walk de `source` ; le « .git » de tête retiré du parcours (dossier, ou fichier d'une copie de
      travail liée) ; lstat de chaque entrée. ⑦ UNITÉ — octets ; nanosecondes.
    ⑧ POURQUOI — Superviseur R-759 du 17-11-2026, Q3 : le contrôle d'après P3 ne relisait que HEAD ; une écriture dans
      la racine ne se voyait pas (RELU du 17-11-2026, m1). Pas d'empreinte de contenu (lire ~630 Mo à chaque tour), pas
      de « git status » (il réécrit l'index de la racine).
    ⑨ CE QUI CLOCHE — Une écriture qui garde la taille et remet la date de modification ne se voit pas ; un autre
      programme qui écrit dans la racine PENDANT l'épreuve la fait rougir à tort. La taille d'un dossier compte dans
      la somme de la garde de place (quelques Ko par dossier : la garde est un peu plus exigeante).
    ⑩ EFFET — Lit les métadonnées, jamais le contenu. ⑪ TERMINAISON — Rend la main ; une erreur de lecture d'un
      dossier lève OSError (`onerror`). [sort: non]
    """
    entrees = []

    def remonter(e):
        """Relève l'erreur d'un dossier illisible. ① RÔLE — Ne pas taire un dossier que os.walk ne peut pas lire.
        ② CONTEXTE D'APPEL — `os.walk`, `onerror`, dans `inventaire_hors_git`. ③ ENTRÉE — `e`, l'OSError de os.walk.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — AUCUNE valeur : elle lève. [rend: 0] ⑥ TRAITEMENT — raise.
        ⑦ UNITÉ — — ⑧ POURQUOI — Par défaut os.walk saute un dossier illisible en silence : l'inventaire serait
        incomplet sans le dire. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lève `e`. ⑪ TERMINAISON — Lève toujours. [sort: non]"""
        raise e

    for d, dossiers, fichiers in os.walk(source, onerror=remonter):
        if os.path.abspath(d) == os.path.abspath(source):
            dossiers[:] = [x for x in dossiers if x != ".git"]
            fichiers = [x for x in fichiers if x != ".git"]
        for nom in dossiers + fichiers:
            chemin = os.path.join(d, nom)
            s = os.lstat(chemin)
            entrees.append((os.path.relpath(chemin, source), s.st_size, s.st_mtime_ns))
    return sorted(entrees)


def etat_de_la_source(source):
    """Rend l'état de la racine que P3 doit laisser intact : tête, branche de la tête, références, disque hors .git.

    ① RÔLE — Le contrôle d'avant et d'après P3. ② CONTEXTE D'APPEL — `tour`, cas P3, avant la copie et après le
    fabricant. ③ ENTRÉE — `source` : le dépôt copié par P3. ④ CONDITIONS D'ENTRÉE — `source` est un dépôt Git.
    ⑤ SORTIE — UNE valeur : un quadruplet — (code, sortie) de « git rev-parse HEAD », (code, sortie) de « git
      symbolic-ref -q HEAD », (code, sortie) de « git for-each-ref », la liste de `inventaire_hors_git`. [rend: 1]
    ⑥ TRAITEMENT — Trois git en lecture, un inventaire. ⑦ UNITÉ — octets et nanosecondes (inventaire).
    ⑧ POURQUOI — Superviseur R-759 du 17-11-2026, Q3 : comparer HEAD, les références et l'inventaire du disque ; pas
      d'empreinte de contenu (coût), pas de « git status » (il réécrit l'index de la racine).
    ⑨ CE QUI CLOCHE — Voir `inventaire_hors_git`, ⑨. Ni l'index ni la configuration de la racine ne sont comparés.
    ⑩ EFFET — Lit, n'écrit rien. ⑪ TERMINAISON — Rend la main ; chaque git est borné à 300 s (`lancer`). [sort: non]
    """
    return (lancer(["git", "-C", source, "rev-parse", "HEAD"]),
            lancer(["git", "-C", source, "symbolic-ref", "-q", "HEAD"]),
            lancer(["git", "-C", source, "for-each-ref"]),
            inventaire_hors_git(source))


def copie_sur_une_branche(source, racine, dossier):
    """Fabrique la copie de travail de P3, placée sur la branche BRANCHE_DE_P3 ; rend son chemin.

    ① RÔLE — Donner à P3 un dépôt privé complet, SUR UNE BRANCHE NOMMÉE, quelle que soit la branche de la racine.
    ② CONTEXTE D'APPEL — `tour`, cas P3, une fois par tour où P3 est joué.
    ③ ENTRÉE — `source` : le dépôt Git copié (historique, données, disque) · `racine` : où lire les programmes
      éprouvés ; si elle diffère de `source` (tour de sabotage), ses fichiers LUS remplacent ceux de la copie ·
      `dossier` : le dossier jetable du tour.
    ④ CONDITIONS D'ENTRÉE — `source` est un dépôt Git non superficiel (vérifié par `tour` avant l'appel) ; `dossier`
      existe et n'a pas de sous-dossier « prive3 ».
    ⑤ SORTIE — UNE valeur : le chemin de la copie, `dossier`/prive3. [rend: 1]
    ⑥ TRAITEMENT — ① LA GARDE DE PLACE : si la place libre sous `dossier` est inférieure à FACTEUR_DE_PLACE fois la
      taille du disque de `source` hors .git (`inventaire_hors_git`), ErreurDOutillage « place insuffisante » ·
      ② les fichiers de `source`, sauf son « .git », COPIÉS sous `dossier`/prive3 (octets recopiés, chaque fichier a
      son propre inode ; les liens symboliques restent des liens) · ③ son historique cloné dans prive3/.git par
      « git clone --mirror --shared » (toutes les références, branches distantes comprises, puisque l'étage A lit
      l'historique entier par « git log --all » ; les objets lus chez la source, rien de recopié), rendu non nu, puis
      la section « remote.origin » retirée de sa configuration (« git config --remove-section », qui garde les
      références) ; « git remote » doit alors rendre vide · ④ la branche BRANCHE_DE_P3 créée sur le commit de la tête
      de `source`, et HEAD placé dessus · ⑤ si `racine` n'est pas `source` : chaque fichier LUS de la racine remplace
      celui de la copie (l'ancien retiré d'abord : un lien symbolique ne mène pas l'écriture hors de la copie).
    ⑦ UNITÉ — octets (place, taille).
    ⑧ POURQUOI — Certification de la nuit du 17-11-2026 (passage 44009228039), cause C6 : P3 lisait la branche de la
      racine par « git rev-parse --abbrev-ref HEAD », qui rend « HEAD » sur la tête détachée de la machine de
      certification ; le fabricant refusait alors (« le clone public est sur la branche « HEAD », le dépôt privé sur
      « aucune branche » »), et P3 rougissait sans que rien ne soit cassé. Réparation jugée DE FOND par le superviseur
      R-759 le 17-11-2026 : P3 crée et se place sur une branche nommée dans SA PROPRE copie, au lieu de dépendre de
      la branche du dépôt où il tourne. « Ne pas jouer P3 et le dire dans une NOTE » a été écarté : une rustine.
      Le clone en miroir sert aussi une racine dont le « .git » est un fichier (copie de travail liée) : rien de la
      racine n'est écrit, alors qu'une copie de ce fichier pointerait sur l'historique de la racine elle-même.
      COPIE ORDINAIRE et non plus liens physiques (relecture du 17-11-2026, M1 et m1 ; superviseur R-759, Q1) : avec
      des liens, chaque fichier de la copie avait deux noms, le fabricant refusait les fichiers « lien dur » (un
      sabotage qui publie le disque mordait à cause de la copie, et ne mordait plus sur un autre disque où le lien
      est refusé), et une écriture sur place dans la copie écrivait dans la racine. SECTION « remote.origin » RETIRÉE
      (m2, Q2) : la copie en miroir avait la racine pour origine, et un « git push » nu y aurait créé epreuve-p3 et
      supprimé les références de la racine absentes de la copie ; « git remote remove » n'est pas employé, il
      efface refs/remotes/origin/*, que l'étage A lit. GARDE DE PLACE (Q1) : une copie qui manque de place échoue au
      milieu ; elle s'arrête avant, en le disant, jamais par un saut silencieux de P3.
    ⑨ CE QUI CLOCHE — « --shared » : la copie lit les objets de la racine ; un « git gc » ou « git prune » de la racine
      PENDANT P3 pourrait retirer un objet qu'elle lit et la corrompre — l'effet est bruyant (git en échec, P3 rouge),
      jamais muet ; non éprouvé (gc et prune interdits ici). Une racine en copie de travail liée (« .git » fichier)
      n'a pas été éprouvée après cette correction (le relecteur l'a éprouvée sur la version à liens physiques). La
      copie ordinaire coûte une recopie du disque (~630 Mo) à chaque tour où P3 est joué : Z0 et SE40, soit quelques
      secondes de plus dans la tranche 10 de la certification, qui portait déjà ~40 s de plus pour le tour de SE40.
      Une racine portant un FIFO ou une socket ferait échouer la copie (erreur d'outillage). Les modifications non
      commitées de la source sont sur le disque de la copie (comme sur la racine), mais ne sont pas dans son
      historique (comme sur la racine). La copie n'a pas d'index : le fabricant n'en lit pas (il lit HEAD,
      l'historique et le disque). La copie prend le disque ENTIER de `source`, non suivi et ignoré compris, et
      l'étage A du fabricant parcourt volontairement ce disque (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, fiche de
      `refus_selon_l_historique`, l. 3064-3083 : « dans l'historique entier, toutes branches, ou sur le disque » ;
      le parcours lui-même, `os.walk`, l. 3153) : une copie de travail ou un fichier non suivi IMBRIQUÉ dans la racine,
      qui reprend le contenu d'un fichier publié, fait donc rougir P3, comme il ferait rougir le fabricant en
      production sur ce disque (relecture du 17-11-2026, tour 3, MINEUR 2 : « git worktree add --detach » dans la
      racine → « FAUX P3 fabricant … étage A »). Ce n'est pas un défaut du code éprouvé ; remède : jouer l'épreuve
      depuis un clone neuf. Copie inchangée (superviseur R-759, R3). À VALIDER PAR JEAN-LUC : sur une machine qui manque de place (celle du Chat en
      particulier), la suite s'arrête en erreur d'outillage au lieu de jouer P3 sans place.
    ⑩ EFFET — Écrit sous `dossier` ; lance git (clone en lecture de la source, puis écritures dans la copie seule) ;
      lit les fichiers de la source sans les modifier.
    ⑪ TERMINAISON — Rend la main, ou lève ErreurDOutillage si la place manque, si la copie des fichiers échoue ou si
      un git échoue (`tour` la relance, `main` sort avec CODE_D_OUTILLAGE) ; chaque git est borné à 300 s (`lancer`).
      [sort: non]
    """
    copie = os.path.join(dossier, "prive3")
    taille = sum(e[1] for e in inventaire_hors_git(source))
    libre = shutil.disk_usage(dossier).free
    if libre < FACTEUR_DE_PLACE * taille:
        raise ErreurDOutillage(f"place insuffisante pour la copie de P3 : {libre} octets libres sous {dossier}, "
                               f"il en faut au moins {FACTEUR_DE_PLACE} × {taille} (le disque de {source} hors .git)")
    try:
        shutil.copytree(source, copie, symlinks=True,
                        ignore=lambda d, noms: [".git"] if os.path.abspath(d) == os.path.abspath(source) else [])
    except (OSError, shutil.Error) as e:
        raise ErreurDOutillage(f"copie des fichiers de {source} vers {copie} : {type(e).__name__} : {str(e)[:300]}")
    for args in (["clone", "-q", "--mirror", "--shared", source, os.path.join(copie, ".git")],
                 ["-C", copie, "config", "core.bare", "false"],
                 ["-C", copie, "config", "--remove-section", "remote.origin"]):
        c, o = lancer(["git"] + args)
        if c != 0:
            raise ErreurDOutillage(f"git {' '.join(args[:3])} : code {c} : {o[-200:]}")
    c, o = lancer(["git", "-C", copie, "remote"])
    if c != 0 or o.strip():
        raise ErreurDOutillage(f"la copie de P3 garde une origine (git remote : code {c} : {o[-200:]})")
    c, tete = lancer(["git", "-C", source, "rev-parse", "--verify", "HEAD"])
    for args in (["update-ref", "refs/heads/" + BRANCHE_DE_P3, tete.strip()],
                 ["symbolic-ref", "HEAD", "refs/heads/" + BRANCHE_DE_P3]):
        c2, o = lancer(["git", "-C", copie] + args)
        if c != 0 or c2 != 0:
            raise ErreurDOutillage(f"git {args[0]} : code {c}/{c2} : {(tete + o)[-200:]}")
    if os.path.abspath(racine) != os.path.abspath(source):
        for rel in LUS:
            if os.path.isfile(os.path.join(racine, rel)):
                cible = os.path.join(copie, rel)
                if os.path.lexists(cible):
                    os.remove(cible)
                shutil.copyfile(os.path.join(racine, rel), cible)
    return copie


NOTES = []
P3_JOUES = []   # une entrée par tour où P3 a été joué (lu par `main` pour les sabotages de JOUENT_P3)


def etage_a(F, d):
    """Joue les cas A (étage A, témoin, extraction du commit, publication du commit extrait) ; rend les cas faux.

    ① RÔLE — Éprouver la livraison 1 du superviseur R-759 du 15-11-2026 sur un petit dépôt git fabriqué ici.
    ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `F` : le fabricant éprouvé ; `d` : le dossier jetable du tour.
    ④ CONDITIONS D'ENTRÉE — git installé. ⑤ SORTIE — UNE valeur : la liste des cas faux. [rend: 1]
    ⑥ TRAITEMENT — Un dépôt « prive_a » : main porte programmes/OK.py, sa copie etudes/copie_ok.py, donnees/d.csv et
      le registre ; une branche « autre » porte donnees/sur_branche.csv ; travail-a porte, puis retire,
      donnees/ancien.csv, et porte etudes/proto.py et tests/outils/VOLE.py (= donnees/d.csv, COMMITÉ) ; sur le disque,
      un fichier non suivi nonsuivi/x.txt. Au public : VOLE (copie d'une donnée du commit), HIST (= une donnée
      retirée, dans l'historique seulement), BRANCHE (= une donnée d'une autre branche), DISQUE (= le fichier non
      suivi), NEUF (= etudes/proto.py, un « .py » d'une étude, jamais publié) et OK (sur main à un chemin publié, mais
      identique à sa copie etudes/copie_ok.py : aucune exemption « déjà public » depuis F1, 15-11-2026) doivent être
      refusés ; PROPRE (sur main, sans copie) et VIDE passent. X2 (la donnée fusionnée dans main et poussée, publication
      de main), X3 (main local avancé non poussé, publication d'une autre branche) et X4 (la fuite déjà présente au
      dépôt public) : refusés (F1 du RELU de Cowork d21df83c). A2 le témoin ; A3 un clone superficiel ; A7 une copie sans git (étage A sans objet) ;
      A4 l'extraction du commit ; A5 la publication refusée si HEAD a bougé ; A6 la garde des lignes ne se tait plus ;
      A8 (A-857) le refus de OK.py nomme le blob entier et le remède unique « changer une ligne du fichier publié
      (comme 32aa88d0) », sans « retirer » (M1 du superviseur R-759 du 16-11-2026) (sabotages SE37, SE38, SE39).
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731 : chaque défaut a son cas, chaque garde son sabotage.
    ⑨ CE QUI CLOCHE — Un dépôt minuscule : le coût sur le vrai dépôt est mesuré par P3, et seulement sur un clone entier.
    ⑩ EFFET — Écrit dans `d`. ⑪ TERMINAISON — Rend la main ; chaque git est borné (`lancer`). [sort: non]
    """
    faux = []
    p = os.path.join(d, "prive_a")
    def ecrire(rel, contenu):
        """Écrit un fichier du dépôt d'essai. ① RÔLE — —. ② CONTEXTE D'APPEL — `etage_a`. ③ ENTRÉE — chemin, octets.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune valeur. [rend: rien] ⑥ TRAITEMENT — —. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Écrit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        os.makedirs(os.path.dirname(os.path.join(p, rel)), exist_ok=True)
        open(os.path.join(p, rel), "wb").write(contenu)
    def git(*a):
        """git dans le dépôt d'essai. ① RÔLE — —. ② CONTEXTE D'APPEL — `etage_a`. ③ ENTRÉE — arguments.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — `lancer`. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — git. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        return lancer(["git", "-C", p] + list(a))
    lancer(["git", "init", "-q", "-b", "main", p])
    donnee = b"date,valeur\n2001-02-03,12.34\n2001-02-04,12.56\n"
    ecrire("programmes/OK.py", b"VALEUR = 1\n")
    ecrire("etudes/copie_ok.py", b"VALEUR = 1\n")
    ecrire("programmes/PROPRE.py", b"PROPRE = 5\n")
    ecrire("donnees/d.csv", donnee)
    ecrire("donnees/PROVENANCE_DES_FICHIERS.csv", b"fichier,sha256\ndonnees/d.csv,x\n")
    git("add", "-A"); git("commit", "-qm", "main")
    git("checkout", "-q", "-b", "autre")
    ecrire("donnees/sur_branche.csv", b"branche,1\n")
    git("add", "-A"); git("commit", "-qm", "autre")
    git("checkout", "-q", "-b", "travail-a", "main")
    ecrire("donnees/ancien.csv", b"ancien,2\n")
    git("add", "-A"); git("commit", "-qm", "ancien")
    git("rm", "-q", "donnees/ancien.csv")
    ecrire("etudes/proto.py", b"PROTO = 3\n")
    ecrire("tests/outils/VOLE.py", donnee)
    git("add", "-A"); git("commit", "-qm", "travail")
    ecrire("nonsuivi/x.txt", b"non suivi, 4\n")
    pub = os.path.join(d, "public_a")
    contenus = {"tests/outils/VOLE.py": donnee, "programmes/HIST.py": b"ancien,2\n",
                "programmes/BRANCHE.py": b"branche,1\n", "programmes/DISQUE.py": b"non suivi, 4\n",
                "programmes/NEUF.py": b"PROTO = 3\n", "programmes/OK.py": b"VALEUR = 1\n", "programmes/VIDE.py": b"",
                "programmes/PROPRE.py": b"PROPRE = 5\n"}
    for rel, c in contenus.items():
        os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True)
        open(os.path.join(pub, rel), "wb").write(c)
    try:
        refus, note = F.refus_selon_l_historique(p, pub, list(contenus))
        vus = sorted(r.split(" : ")[0] for r in refus)
        attendus = sorted(["tests/outils/VOLE.py", "programmes/HIST.py", "programmes/BRANCHE.py", "programmes/DISQUE.py",
                           "programmes/NEUF.py", "programmes/OK.py"])
        if vus != attendus or "témoin : les 1 chemins" not in note:
            faux.append(f"A1 étage A : refusés {vus} au lieu de {attendus} ; {note[-160:]}")
        # A8 (A-857, 16-11-2026) : le refus nomme le blob ENTIER et le remède prouvé par 32aa88d0 — le texte est écrit
        # ici en toutes lettres, jamais lu dans le fabricant (sinon un remède vidé passerait)
        ok = [r for r in refus if r.startswith("programmes/OK.py : ")]
        blob_ok = hashlib.sha1(b"blob %d\0" % len(b"VALEUR = 1\n") + b"VALEUR = 1\n").hexdigest()
        if (len(ok) != 1 or f"blob {blob_ok}" not in ok[0] or f"--find-object={blob_ok}" not in ok[0]
                or "remède : changer une ligne du fichier publié (comme 32aa88d0)" not in ok[0] or "retir" in ok[0]):
            faux.append(f"A8 (A-857) le refus ne nomme pas le blob {blob_ok} et le remède : {ok}")
    except (OSError, ValueError) as e:
        faux.append(f"A1 étage A n'a pas tourné : {e}")
    # X2, X3, X4 (F1 du RELU de Cowork d21df83c, 15-11-2026) : aucune exemption « déjà public », ni lue au privé ni au
    # public ; la donnée VOLE (= donnees/d.csv) doit être refusée dans les trois cas.
    vole = {"tests/outils/VOLE.py": donnee}
    ident = ["-c", "user.name=e", "-c", "user.email=e@e"]
    distant = os.path.join(d, "distant_x")
    lancer(["git", "clone", "-q", "--bare", p, distant])
    x3 = os.path.join(d, "prive_x3")
    lancer(["git", "clone", "-q", "-b", "main", distant, x3])
    lancer(["git", "-C", x3] + ident + ["merge", "-q", "--no-edit", "origin/travail-a"])
    lancer(["git", "-C", x3, "checkout", "-q", "-b", "travail-y", "origin/travail-a"])
    x2 = os.path.join(d, "prive_x2")
    lancer(["git", "clone", "-q", "-b", "main", distant, x2])
    lancer(["git", "-C", x2] + ident + ["merge", "-q", "--no-edit", "origin/travail-a"])
    lancer(["git", "-C", x2, "push", "-q", "origin", "main"])
    lancer(["git", "-C", x2, "fetch", "-q", "origin"])
    pub4 = os.path.join(d, "public_x4")
    os.makedirs(os.path.join(pub4, "tests", "outils"))
    lancer(["git", "init", "-q", "-b", "main", pub4])
    open(os.path.join(pub4, "tests", "outils", "VOLE.py"), "wb").write(donnee)
    lancer(["git", "-C", pub4, "add", "-A"])
    lancer(["git", "-C", pub4] + ident + ["commit", "-qm", "fuite deja publiee"])
    pubx = os.path.join(d, "public_x")
    os.makedirs(os.path.join(pubx, "tests", "outils"))
    open(os.path.join(pubx, "tests", "outils", "VOLE.py"), "wb").write(donnee)
    for cas, prive_x, public_x in (("X2 la donnée fusionnée dans main et poussée, publication de main", x2, pubx),
                                   ("X3 main local avancé non poussé, publication d'une autre branche", x3, pubx),
                                   ("X4 la fuite déjà présente au dépôt public", p, pub4)):
        try:
            refus_x, note_x = F.refus_selon_l_historique(prive_x, public_x, list(vole))
            if [r.split(" : ")[0] for r in refus_x] != ["tests/outils/VOLE.py"]:
                faux.append(f"{cas} : refus {refus_x} ; {note_x[-120:]}")
        except (OSError, ValueError) as e:
            faux.append(f"{cas} : n'a pas tourné : {e}")
    # A2 : le témoin — un chemin du registre absent du disque, puis remplacé par un dossier : le contrôle s'arrête
    os.remove(os.path.join(p, "donnees", "d.csv"))
    for nom, geste in (("absent", None), ("dossier", lambda: os.makedirs(os.path.join(p, "donnees", "d.csv")))):
        if geste:
            geste()
        try:
            F.refus_selon_l_historique(p, pub, list(contenus))
            faux.append(f"A2 témoin : un chemin du registre {nom} n'arrête pas le contrôle")
        except OSError as e:
            if "témoin du parcours" not in str(e):
                faux.append(f"A2 témoin ({nom}) : arrêté pour une autre raison : {e}")
    os.rmdir(os.path.join(p, "donnees", "d.csv"))
    # un lien vers un fichier lisible : le parcours ne le suit pas, donc ne l'a pas vu (le témoin seul le dit)
    open(os.path.join(d, "d_hors.csv"), "wb").write(donnee)
    os.symlink(os.path.join(d, "d_hors.csv"), os.path.join(p, "donnees", "d.csv"))
    try:
        F.refus_selon_l_historique(p, pub, list(contenus))
        faux.append("A2 témoin : un chemin du registre que le parcours n'a pas vu (un lien) n'arrête pas le contrôle")
    except OSError as e:
        if "non vus par le parcours" not in str(e):
            faux.append(f"A2 témoin (lien) : arrêté pour une autre raison : {e}")
    os.remove(os.path.join(p, "donnees", "d.csv"))
    open(os.path.join(p, "donnees", "d.csv"), "wb").write(donnee)
    registre = os.path.join(p, "donnees", "PROVENANCE_DES_FICHIERS.csv")
    os.rename(registre, registre + ".cache")
    try:
        F.refus_selon_l_historique(p, pub, list(contenus))
        faux.append("A2 témoin : le registre au commit mais absent du disque n'arrête pas le contrôle")
    except OSError as e:
        if "témoin du parcours" not in str(e):
            faux.append(f"A2 témoin (registre absent) : arrêté pour une autre raison : {e}")
    os.rename(registre + ".cache", registre)
    # A7 : une copie SANS git (copie d'épreuve) : l'étage A est sans objet (rien n'en peut être poussé), le témoin tourne
    sans_git = os.path.join(d, "prive_sans_git")
    shutil.copytree(p, sans_git, ignore=shutil.ignore_patterns(".git"))
    try:
        refus7, note7 = F.refus_selon_l_historique(sans_git, pub, list(contenus))
        if refus7 or "sans objet" not in note7 or "témoin : les 1 chemins" not in note7:
            faux.append(f"A7 copie sans git : refus {refus7} ; {note7[-120:]}")
    except (OSError, ValueError) as e:
        faux.append(f"A7 copie sans git : {e}")
    # A3 : un clone superficiel s'arrête
    sup = os.path.join(d, "prive_superficiel")
    lancer(["git", "clone", "-q", "--depth", "1", "-b", "travail-a", "file://" + p, sup])
    try:
        F.refus_selon_l_historique(sup, pub, list(contenus))
        faux.append("A3 un clone superficiel n'arrête pas l'étage A")
    except OSError as e:
        if "SUPERFICIEL" not in str(e):
            faux.append(f"A3 clone superficiel : arrêté pour une autre raison : {e}")
    # A4 : l'extraction du commit — le disque modifié ou non suivi n'est pas publié ; un lien du commit reste un lien
    ecrire("programmes/OK.py", b"VALEUR = 2  # modifie sur le disque, non commite\n")
    ecrire("programmes/NONSUIVI.py", b"X = 1\n")
    os.symlink("../donnees/d.csv", os.path.join(p, "programmes", "LIEN.py"))
    git("add", "programmes/LIEN.py"); git("commit", "-qm", "lien")
    x = os.path.join(d, "extrait_a")
    os.makedirs(x)
    try:
        sha, publies = F.extraire_le_commit(p, x)
        lu = open(os.path.join(x, "programmes", "OK.py"), "rb").read()
        refus = F.refus_avant_publication(p, ["programmes/LIEN.py"], source=x)
        if (lu != b"VALEUR = 1\n" or "programmes/NONSUIVI.py" in publies or os.path.exists(os.path.join(x, "programmes", "NONSUIVI.py"))
                or sha != git("rev-parse", "HEAD")[1].strip() or not refus or "lien symbolique" not in refus[0]):
            faux.append(f"A4 extraction du commit : OK.py {lu!r}, publiés {publies}, refus du lien {refus}")
    except (OSError, ValueError) as e:
        faux.append(f"A4 extraction du commit n'a pas tourné : {e}")
    # A5 : HEAD a bougé entre l'extraction et la publication → refus, rien de commité
    c5 = os.path.join(d, "public_a5")
    lancer(["git", "init", "-q", "-b", "travail-a", c5])
    old = os.environ.copy()
    os.environ.update({k: v for k, v in GIT_ENV.items() if k.startswith("GIT_")})
    try:
        k5, m5 = F.publier(p, c5, ["p.txt"], "0" * 40)
    finally:
        os.environ.clear()
        os.environ.update(old)
    if k5 != 1 or "HEAD a bougé" not in m5:
        faux.append(f"A5 publication d'un commit qui n'est plus HEAD : code {k5} : {m5[:120]}")
    # A6 (C-D2) : la garde des lignes ne se tait plus sur un dossier de données illisible
    p6 = os.path.join(d, "prive_a6")
    os.makedirs(p6)
    open(os.path.join(p6, "donnees"), "w").write("pas un dossier\n")
    try:
        F.lignes_de_donnees(p6)
        faux.append("A6 (C-D2) un dossier de données illisible donne un index vide, en silence")
    except OSError:
        pass
    if F.lignes_de_donnees(os.path.join(d, "prive_sans_rien")) != {}:
        faux.append("A6 un dépôt d'essai sans donnees/ ne donne pas un index vide")
    return faux


def tour(racine, source_git=None, fragment_p3=None):
    """Joue tous les cas sur une racine ; rend la liste des cas faux (vide : tout est conforme).

    ① RÔLE — Le corps de l'épreuve (fiche en tête, ⑥). ② CONTEXTE D'APPEL — `main`, sur la racine puis sur chaque
    copie sabotée. ③ ENTRÉE — `racine` : où lire les programmes éprouvés · `source_git` : le dépôt Git dont P3 fait
    sa copie (None : la racine elle-même ; `main` donne la vraie racine aux seuls sabotages de JOUENT_P3, car une
    copie sabotée n'a pas de .git) · `fragment_p3` : None hors des tours de sabotage de JOUENT_P3 ; sinon le
    fragment attendu de ce sabotage (JOUENT_P3[nom]) — sa présence fait de ce tour un tour de sabotage de P3.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des cas faux. [rend: 1] ⑥ TRAITEMENT — Fiche en tête, ⑥. P3 : une copie de
    `source_git` (ou de la racine) sur la branche BRANCHE_DE_P3, où les fichiers LUS de la racine remplacent les siens
    (`copie_sur_une_branche`) ; la source est relue avant et après : sa tête (HEAD et sa branche), ses références
    (« git for-each-ref ») et l'inventaire de son disque hors .git (`inventaire_hors_git` : chemin, taille, mtime_ns) ;
    un écart est un cas faux au tour tel quel (Z0), et une ErreurDOutillage dans un tour de sabotage (`fragment_p3`
    donné). Avec `fragment_p3`, la ligne « P3 fabricant » d'un fabricant en échec porte en plus l'extrait de sa sortie
    ENTIÈRE autour du fragment s'il y est, ou « fragment attendu ABSENT » (sans le citer) ; `main` n'y voit une
    morsure que si le fragment est dans cette ligne. ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête. Contrôle d'après élargi aux références et au disque (relecture du 17-11-2026, m1 et
    m2 ; superviseur R-759, Q3) : HEAD seul ne voyait ni une écriture dans la racine ni une référence poussée.
    Fragment cherché dans la sortie entière et écart du contrôle d'après rangé en erreur d'outillage dans un tour de
    sabotage : relecture du 17-11-2026, tour 3, MAJEUR 1 — avec la garde neutralisée et un écrivain dans la racine,
    SE40 « mordait » par le seul écart du contrôle d'après, et le verdict sortait vert ; superviseur R-759, R1.
    ⑨ CE QUI CLOCHE — Une erreur imprévue d'un cas est rangée parmi les cas faux (au tour d'un sabotage de JOUENT_P3,
    elle n'est pas une morsure : seule la ligne « P3 fabricant » portant le fragment l'est) ; une ErreurDOutillage
    (copie de P3, git dans cette copie, création du clone public de P3, écart du contrôle d'après dans un tour de
    sabotage) est RELANCÉE avant ce rangement : elle n'est jamais un cas faux, donc jamais une morsure. Le contrôle
    d'après ne lit pas le contenu (voir `inventaire_hors_git`, ⑨) ; au tour tel quel, une écriture concurrente dans la
    racine le fait rougir à tort (code 1).
    ⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin ; P3 y COPIE les fichiers de la source (lus, jamais
    modifiés). ⑪ TERMINAISON — Rend la main, ou lève ErreurDOutillage.
    [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="epreuves_longues_")
    try:
        try:
            F = charger(os.path.join(racine, FABRICANT), "FABRICANT_EPROUVE_EL")
            J = charger(os.path.join(racine, JOUEUR), "JOUEUR_EPROUVE_EL")
            R = charger(os.path.join(racine, RAPATRIEUR), "RAPATRIEUR_EPROUVE_EL")
        except Exception as e:   # noqa: BLE001 — tout échec de chargement est un cas faux
            return [f"chargement : {type(e).__name__} : {e}"]
        # T : la table
        table = json.load(open(os.path.join(racine, TABLE), encoding="utf-8"))
        try:
            lues = {c: (ch, a) for c, ch, a in F.epreuves_du_circuit(racine)}
        except ValueError as e:
            return [f"T la table de la racine est refusée : {e}"]
        for code, chemin in TEMOIN.items():
            if lues.get(code) != (chemin, ["{copie}", "--saboter"]):
                faux.append(f"T0 {code} : {lues.get(code)} au lieu de {chemin} {{copie}} --saboter")
        for code, (chemin, _) in lues.items():
            refus = J.refus_du_fichier(racine, chemin)
            if refus:
                faux.append(f"T1 {code} : {refus}")
        serie = next(iter(table.get("series_hors_de_la_nuit") or {}), "tests/X.py")
        for nom, entrees, fragment in (
                ("T2a code avec une espace", {"A b": {"chemin": "tests/X.py", "arguments": ["{copie}"], "pourquoi": "p"}},
                 "code d'épreuve longue refusé"),
                ("T2b argument avec un point-virgule",
                 {"A": {"chemin": "tests/X.py", "arguments": ["{copie}", "x;id"], "pourquoi": "p"}}, "arguments refusés"),
                ("T2c arguments sans {copie}", {"A": {"chemin": "tests/X.py", "arguments": ["--saboter"], "pourquoi": "p"}},
                 "arguments refusés"),
                ("T2d le --saboter d'une série",
                 {"A": {"chemin": serie, "arguments": ["{copie}", "--saboter"], "pourquoi": "p"}}, "série de sabotages"),
                ("T2e deux codes égaux à la casse près",
                 {"Relais": {"chemin": "tests/X.py", "arguments": ["{copie}"], "pourquoi": "p"},
                  "relais": {"chemin": "tests/Y.py", "arguments": ["{copie}"], "pourquoi": "p"}}, "en double"),
                ("T2f chemin qui remonte",
                 {"A": {"chemin": "tests/../x.py", "arguments": ["{copie}"], "pourquoi": "p"}}, "chemin refusé")):
            t = os.path.join(d, "t2", nom[:3])
            os.makedirs(os.path.join(t, "tests"))
            json.dump(dict(table, epreuves_longues=entrees), open(os.path.join(t, TABLE), "w", encoding="utf-8"),
                      ensure_ascii=False)
            try:
                F.epreuves_du_circuit(t)
                faux.append(f"{nom} : acceptée")
            except ValueError as e:
                if fragment not in str(e):
                    faux.append(f"{nom} : refusée pour une autre raison : {e}")
        # G : le gabarit
        E = F.EPREUVES
        if E is None:
            return faux + [f"G1 gabarit des épreuves non fabriqué : {F.ERREUR_DE_LA_TABLE}"]
        if "%(" in E:
            faux.append("G1 un repère de format non rempli dans le gabarit des épreuves")
        groupes = [re.findall(r"^  group: (.+)$", g, re.M) for g in (E, F.SERIES)]
        if groupes != [[F.GROUPE_DES_MACHINES_LONGUES]] * 2:
            faux.append(f"G1 groupes de concurrence épreuves / séries : {groupes}")
        if E.count("max-parallel: %d\n" % F.PARTS_EN_MEME_TEMPS) != 1 or len(re.findall("max-parallel", E)) != 1:
            faux.append("G1 « max-parallel » du gabarit des épreuves n'est pas PARTS_EN_MEME_TEMPS")
        # A-884 (17-11-2026) : la largeur se CALCULE sur les fiches fabriquées ; avant, G1 comparait la part à une marge
        # écrite à la main (10), restée verte à 16 + 10 = 26 > 20
        soir_g1 = F.fabriquer_le_circuit(open(os.path.join(racine, CIRCUIT_PRIVE), encoding="utf-8").read())
        fiches_g1 = {c.split("/")[-1]: o.decode("utf-8") for c, o in F.ce_que_la_publication_ecrit(racine, [], [], soir_g1)
                     if c.startswith(".github/workflows/")}
        refus_g1, _ = F.refus_de_la_largeur(fiches_g1)
        if refus_g1:
            faux.append(f"G1 la largeur calculée des circuits fabriqués dépasse les tâches du compte : {refus_g1}")
        if F.largeur_d_une_fiche(E) != (F.GROUPE_DES_MACHINES_LONGUES, F.PARTS_EN_MEME_TEMPS):
            faux.append(f"G1 largeur calculée du gabarit des épreuves {F.largeur_d_une_fiche(E)} au lieu de "
                        f"{(F.GROUPE_DES_MACHINES_LONGUES, F.PARTS_EN_MEME_TEMPS)}")

        def filet(nom, texte, fragment):
            """Juge un cas G2 (fragment None : accepté). ① RÔLE — Un cas du filet. ② CONTEXTE D'APPEL — `tour`.
            ③ ENTRÉE — le nom, le gabarit, le fragment attendu. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur.
            [rend: rien] ⑥ TRAITEMENT — `verifier_les_gabarits_publics` avec les séries. ⑦ UNITÉ — — ⑧ POURQUOI — Un
            refus pour sa raison. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Ajoute à `faux`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            try:
                F.verifier_les_gabarits_publics({"series": F.SERIES, "epreuves": texte}, "")
                vu = "accepté"
            except ValueError as e:
                vu = str(e)
            if (fragment is None and vu != "accepté") or (fragment is not None and fragment not in vu):
                faux.append(f"{nom} : {vu[:160]}")
        filet("G2 gabarit fabriqué", E, None)
        filet("G2 sans persist-credentials", E.replace("          persist-credentials: false\n", "", 1), "garde le jeton")
        filet("G2 poussée vers main", E.replace('"HEAD:refs/heads/' + F.EPREUVES_BRANCHES, '"HEAD:refs/heads/main/', 1),
              "hors de la forme permise")
        filet("G2 identité des séries", E.replace(F.EPREUVES_IDENTITE, F.SERIES_IDENTITE), "identité partagée")
        # C-D3 : la forme de la ligne 1211 de 9691517a, remise dans le gabarit, est refusée ; aucun gabarit ne la porte
        filet("G2 valeur refusée citée (C-D3)", E.replace("{ echo \"::error::code d epreuve refuse\"; exit 1; }",
                                                         "{ echo \"::error::code d epreuve refuse : $CODE\"; exit 1; }", 1),
              "cite la valeur contrôlée")
        for nom_g, texte_g in (("certification", F.CERTIFICATION), ("series", F.SERIES), ("relais", F.RELAIS), ("epreuves", E)):
            if F.valeur_citee_apres_un_motif(texte_g):
                faux.append(f"E10a (C-D3) gabarit {nom_g} : {F.valeur_citee_apres_un_motif(texte_g)[:100]}")
        if not F.valeur_citee_apres_un_motif('  [[ "$VERSION" =~ ^x$ ]] || { echo "::error::version refusee : $VERSION"; exit 1; }'):
            faux.append("E10a (C-D3) la forme de la ligne 1211 de 9691517a n'est pas vue")
        # R-D3 : le relais écrit sans le circuit des épreuves
        rel = ".github/workflows/demande_de_serie.yml"
        tous = [rel] + [".github/workflows/" + f for f in ("series_longues.yml", "epreuves_longues.yml",
                                                           "certifier_la_version.yml")]
        if F.circuits_du_relais_non_ecrits(tous) or F.circuits_du_relais_non_ecrits([x for x in tous if "epreuves" not in x]) \
                != ["epreuves_longues.yml"]:
            faux.append("E3a (R-D3) le relais publié sans un circuit qu'il compte n'est pas vu")
        # la version minuscule : fabricant, certificateur, joueurs, table d'essai, épreuves d'essai
        v = os.path.join(d, "version")
        for f in (FABRICANT, CERTIFICATEUR, JOUEUR_DES_PARTS, JOUEUR, RAPATRIEUR):
            os.makedirs(os.path.dirname(os.path.join(v, f)), exist_ok=True)
            shutil.copyfile(os.path.join(racine, f), os.path.join(v, f))
        essai = {"Mini": "tests/EPREUVE_MINI.py", "Ok": "tests/EPREUVE_OK.py", "Lente": "tests/EPREUVE_LENTE.py",
                 "Interdite": "tests/EPREUVE_INTERDITE.py", "Absente": "tests/EPREUVE_ABSENTE.py"}
        table_essai = dict(table, epreuves_longues={c: {"chemin": ch, "arguments": ["{copie}", "--saboter"],
                                                        "pourquoi": "essai"} for c, ch in essai.items()})
        json.dump(table_essai, open(os.path.join(v, TABLE), "w", encoding="utf-8"), ensure_ascii=False)
        open(os.path.join(v, essai["Mini"]), "w").write(MINI)
        open(os.path.join(v, essai["Ok"]), "w").write("print('tout va bien')\n")
        open(os.path.join(v, essai["Lente"]), "w").write("import time\ntime.sleep(60)\n")
        open(os.path.join(v, essai["Interdite"]), "w").write("# lance MESURER_LES_AJUSTEMENTS_DE_YAHOO\nprint(1)\n")
        outils = os.path.join(d, "outils")
        os.makedirs(outils)
        open(os.path.join(outils, "unshare"), "w").write(FAUX_UNSHARE)
        os.chmod(os.path.join(outils, "unshare"), 0o755)
        # G3 : le pas « Fabriquer la matrice »
        env_m, script_m = pas_du_gabarit(E, "matrice")
        if env_m is None:
            faux.append("G3 pas « matrice » introuvable")
        else:
            for nom, liste, attendu in (("G3 deux codes", "Ok,Mini", ["Ok", "Mini"]), ("G3 code inconnu", "Nul", None)):
                rt = tempfile.mkdtemp(prefix="g3_", dir=d)
                sortie = os.path.join(rt, "sortie")
                env = dict(GIT_ENV, GITHUB_OUTPUT=sortie, RUNNER_TEMP=rt, **resoudre(env_m, {"inputs.epreuves": liste}))
                c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-c", script_m], env=env, cwd=v)
                lu = dict(l.split("=", 1) for l in open(sortie).read().split("\n") if "=" in l) \
                    if os.path.exists(sortie) else {}
                vus = [x["code"] for x in json.loads(lu["matrice"])] if "matrice" in lu else None
                if (attendu is None and (c == 0 or vus is not None)) or (attendu is not None and (c != 0 or vus != attendu)):
                    faux.append(f"{nom} : code {c}, matrice {vus} : {o[-200:]}")
        # G4 : le pas « Jouer l epreuve »
        env_j, script_j = pas_du_gabarit(E, "jouer_l_epreuve")
        if env_j is None:
            faux.append("G4 pas « jouer_l_epreuve » introuvable")
        else:
            rt = tempfile.mkdtemp(prefix="g4_", dir=d)
            journal = os.path.join(rt, "unshare.jsonl")
            espace4 = os.path.join(rt, "espace")
            matrice4 = '[{"code":"Mini"},{"code":"Ok"}]'
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt, GITHUB_WORKSPACE=espace4,
                       GITHUB_RUN_ID="77", FAUX_UNSHARE_JOURNAL=journal,
                       **resoudre(env_j, {"matrix.code": "Mini", "runner.temp": rt,
                                          "needs.preparer.outputs.matrice": matrice4,
                                          "needs.preparer.outputs.sha": "a" * 40,
                                          "steps.depart.outputs.t": "1700000000"}))
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-c", script_j], env=env, cwd=rt)
            vus = [json.loads(l) for l in open(journal)] if os.path.exists(journal) else []
            attendu = [["-rn", "python3", "-B", "-u", JOUEUR, rt + "/depot", "Mini",
                        "--sortie=" + espace4 + "/rapports/epreuves_longues/77/Mini"]]
            if c != 0 or vus != attendu:
                faux.append(f"G4 « Jouer l epreuve » : code {c}, lancé {vus} au lieu de {attendu} : {o[-200:]}")
            ecrite = os.path.join(espace4, "rapports", "epreuves_longues", "77", "Mini", "DEMANDE.json")
            if not os.path.exists(ecrite) or open(ecrite).read().strip() != matrice4 or env.get("DEPART_DU_JOB") != "1700000000":
                faux.append("G4bis (R-D2, R-D7) le pas « Jouer l epreuve » n'écrit pas la matrice entière dans DEMANDE.json, "
                            "ou ne reçoit pas l'heure de départ du job")
            # R-D7 : la durée du job écrite une fois, le pas « depart » en tête du job « jouer »
            job_jouer = E[E.index("\n  jouer:\n"):]
            if ("    timeout-minutes: %d\n" % F.DUREE_D_UNE_EPREUVE_LONGUE) not in job_jouer \
                    or job_jouer.index("id: depart\n") > job_jouer.index("actions/checkout"):
                faux.append("E7b le job « jouer » ne porte pas DUREE_D_UNE_EPREUVE_LONGUE, ou le pas « depart » n'est pas "
                            "avant le clonage")
            if env.get("POINTE_JOUEE") != "a" * 40:
                faux.append("G4ter (réparation du 20-11-2026 au soir, point A) le pas « Jouer l epreuve » ne reçoit pas la "
                            "pointe préparée (POINTE_JOUEE) : RESULTAT.json ne pourrait pas dire quel code a été joué")
            env["CODE"] = "Mini;id"
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-c", script_j], env=env, cwd=rt)
            if c == 0:
                faux.append("G4 un code d'épreuve « Mini;id » est accepté par le pas « Jouer l epreuve »")
        # J : le joueur
        copie = v
        espace = os.path.join(d, "espace")
        sorties = os.path.join(espace, "rapports", "epreuves_longues", "77")
        env = dict(GIT_ENV, TEMOIN_ORDINAIRE="vu", **{n: "/tmp/piege_" + n for n in F.FICHIERS_DE_COMMANDES_DE_GITHUB})
        env["GIT_CONFIG_GLOBAL"] = "/tmp/config_de_la_machine"
        env["POINTE_JOUEE"] = "b" * 40
        c, o = lancer([sys.executable, "-B", os.path.join(racine, JOUEUR), copie, "Mini",
                       "--sortie=" + os.path.join(sorties, "Mini")], env=env)
        try:
            s = open(os.path.join(sorties, "Mini", "SORTIE.txt"), encoding="utf-8").read()
            r = json.load(open(os.path.join(sorties, "Mini", "RESULTAT.json"), encoding="utf-8"))
        except (OSError, ValueError) as e:
            s, r = "", {}
            faux.append(f"J1 sortie ou résultat illisible : {e} ; {o[-200:]}")
        manques = [m for m in (f"ARGV ['{copie}', '--saboter']", "ERREUR_VUE", "TEMOIN_ORDINAIRE=vu",
                               f"GIT_CONFIG_GLOBAL={os.devnull}") if m not in s]
        fuites = [n for n in F.FICHIERS_DE_COMMANDES_DE_GITHUB if f"{n}=None" not in s]
        if r.get("pointe_jouee") != "b" * 40:
            faux.append(f"J1bis (20-11-2026 au soir, point A) RESULTAT.json ne porte pas la pointe jouée : "
                        f"{r.get('pointe_jouee')!r}")
        if c != 3 or r.get("code_de_sortie") != 3 or r.get("chemin") != essai["Mini"] or manques or fuites:
            faux.append(f"J1 épreuve d'essai : code {c}, résultat {r.get('code_de_sortie')}, manques {manques}, "
                        f"variables transmises {fuites} : {o[-200:]}")
        for nom, code, fragment in (("J2 code inconnu", "Nul", "inconnue"), ("J3 programme interdit nommé", "Interdite",
                                                                           "interdit"), ("J4 fichier absent", "Absente", "absent")):
            c, o = lancer([sys.executable, "-B", os.path.join(racine, JOUEUR), copie, code,
                           "--sortie=" + os.path.join(sorties, code)])
            try:
                refus = json.load(open(os.path.join(sorties, code, "RESULTAT.json"), encoding="utf-8")).get("refus", "")
            except (OSError, ValueError):
                refus = ""
            if c != 2 or fragment not in refus:
                faux.append(f"{nom} : code {c}, refus {refus!r} : {o[-200:]}")
        Jm = charger(os.path.join(racine, JOUEUR), "JOUEUR_EPROUVE_EL_DELAI")
        Jm.DELAI = 2
        t0 = time.time()
        c = Jm.jouer(copie, "Lente", os.path.join(sorties, "Lente"))
        s = open(os.path.join(sorties, "Lente", "SORTIE.txt"), encoding="utf-8").read() \
            if os.path.exists(os.path.join(sorties, "Lente", "SORTIE.txt")) else ""
        if c != 124 or "ARRÊTÉE" not in s or time.time() - t0 > 30:
            faux.append(f"J5 épreuve au-delà du délai : code {c}, {round(time.time() - t0)} s, sortie {s[-80:]!r}")
        maintenant = 1_800_000_000
        d_sans = J.delai_restant(F, None, maintenant)
        d_30 = J.delai_restant(F, str(maintenant - 1800), maintenant)
        d_fin = J.delai_restant(F, str(maintenant - 10 ** 6), maintenant)
        if (d_sans, d_30, d_fin) != (J.DELAI, (F.DUREE_D_UNE_EPREUVE_LONGUE - F.MARGE_D_ECRITURE) * 60 - 1800, 1):
            faux.append(f"E7 (R-D7) délai : sans départ {d_sans}, départ il y a 30 min {d_30}, départ très ancien {d_fin}")
        for nom, liste, attendu in (("J6 ordre demandé", "Ok,Mini", '[{"code":"Ok"},{"code":"Mini"}]'),
                                    ("J6 toutes, la table d'essai portant une interdite", "toutes", None),
                                    ("J6 double", "Ok,Ok", None), ("J6 interdite", "Interdite", None),
                                    ("J6 absente", "Absente", None)):
            c, o = lancer([sys.executable, "-B", os.path.join(racine, JOUEUR), "--matrice", copie, liste])
            if (attendu is None and c != 2) or (attendu is not None and (c != 0 or o.strip() != attendu)):
                faux.append(f"{nom} : code {c}, {o.strip()[-160:]}")
        # G5 : le pas « deposer », contre un dépôt privé nu local ; puis R : le rapatrieur
        nu = os.path.join(d, "prive.git")
        lancer(["git", "init", "-q", "--bare", nu])
        env_d, script_d = pas_du_gabarit(E, "deposer")
        if env_d is None or F.DEPOT_PRIVE_ADRESSE not in script_d:
            return faux + ["G5 pas « deposer » introuvable, ou sans l'adresse du dépôt privé"]
        script_d = script_d.replace(F.DEPOT_PRIVE_ADRESSE, nu)
        os.makedirs(os.path.join(sorties, "Ok"), exist_ok=True)
        lancer([sys.executable, "-B", os.path.join(racine, JOUEUR), copie, "Ok", "--sortie=" + os.path.join(sorties, "Ok")])
        os.makedirs(os.path.join(sorties, "Vide"), exist_ok=True)
        open(os.path.join(sorties, "Vide", "SORTIE.txt"), "w").write("rien\n")
        def deposer(passage, code, demande):
            """Dépose une épreuve d'essai comme le job « jouer » (DEMANDE.json compris) ; rend (code, sortie, fichiers).
            ① RÔLE — G5 et les cas R. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — le passage, le code, la liste demandée
            (None : pas de DEMANDE.json). ④ CONDITIONS D'ENTRÉE — La sortie du code est dans `sorties`.
            ⑤ SORTIE — TROIS valeurs. [rend: 3] ⑥ TRAITEMENT — un dossier de travail neuf, le pas « deposer ».
            ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au dépôt nu. ⑪ TERMINAISON — Rend la main.
            [sort: non]"""
            ws = os.path.join(d, f"ws_{passage}_{code}")
            ici = os.path.join(ws, "rapports", "epreuves_longues", passage, code)
            shutil.copytree(os.path.join(sorties, code), ici)
            if demande is not None:
                open(os.path.join(ici, "DEMANDE.json"), "w").write(json.dumps([{"code": x} for x in demande]) + "\n")
            os.makedirs(os.path.join(ws, "rapports", "journal_du_circuit"))
            open(os.path.join(ws, "rapports", "journal_du_circuit", f"circuit_{passage}_1_jouer.log"), "w").write(
                f"journal {code}\n")
            env = dict(GIT_ENV, GITHUB_WORKSPACE=ws, GITHUB_RUN_ID=passage, GITHUB_RUN_ATTEMPT="1", GITHUB_JOB="jouer",
                       **resoudre(env_d, {"secrets.JETON_DEPOTS": "", "matrix.code": code}))
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-c", script_d], env=env, cwd=ws)
            return (c, o) + (lancer(["git", "-C", nu, "ls-tree", "-r", "--name-only", f"epreuves-longues/{passage}/{code}"])[1],)
        for code in ("Mini", "Ok", "Vide"):
            c, o, fichiers = deposer("77", code, ["Mini", "Ok", "Vide"])
            if code == "Mini" and (c != 0 or "rapports/epreuves_longues/77/Mini/SORTIE.txt" not in fichiers
                                   or "rapports/journal_du_circuit/circuit_77_1_jouer_Mini.log" not in fichiers):
                faux.append(f"G5 dépôt de Mini : code {c}, branche {fichiers.split()} : {o[-200:]}")
        racine_r = os.path.join(d, "clone_prive")
        shutil.copytree(v, racine_r)
        lancer(["git", "init", "-q", racine_r])
        c, bilan = R.rapatrier(racine_r, "77", depuis=nu)
        texte = "\n".join(bilan)
        rangee = os.path.join(racine_r, "tests", "resultats", "epreuves_longues", "77", "Mini", "SORTIE.txt")
        identique = os.path.exists(rangee) and open(rangee, "rb").read() == open(os.path.join(sorties, "Mini", "SORTIE.txt"), "rb").read()
        identique = identique and os.path.exists(os.path.join(os.path.dirname(rangee), "circuit_77_1_jouer_Mini.log"))
        if c != 2 or "Mini : code 3" not in texte or "Ok : code 0" not in texte or not identique \
                or "Vide : RIEN DE SUR" not in texte or "demandées 3 · rapatriées 3" not in texte:
            faux.append(f"R1/R2 rapatriement : code {c} (2 attendu : Vide sans résultat), rangée identique {identique} : "
                        f"{texte[-300:]}")
        lancer(["git", "-C", nu, "branch", "-D", "epreuves-longues/77/Vide"])
        lancer(["git", "-C", racine_r, "update-ref", "-d", "refs/epreuves_lues/77/Vide"])
        c, bilan = R.rapatrier(racine_r, "77", depuis=nu)
        if c != 2 or not any(l.startswith("Vide : ABSENTE") for l in bilan) or "demandées 3 · rapatriées 2" not in bilan[0]:
            faux.append(f"R4 (R-D2) une épreuve demandée sans branche : code {c} (2 attendu, « Vide : ABSENTE ») : {bilan}")
        # R1 : un passage complet (78), Mini au code 3 → 1
        for code in ("Mini", "Ok"):
            deposer("78", code, ["Mini", "Ok"])
        c, bilan = R.rapatrier(racine_r, "78", depuis=nu)
        if c != 1 or not any(l.startswith("Mini : code 3") for l in bilan):
            faux.append(f"R1 passage complet : code {c} (1 attendu : Mini au code 3) : {bilan}")
        # R5 (R-D5) : la branche de Mini remplacée par un commit sans son dossier ; l'ancien résultat rangé reste
        rangee78 = os.path.join(racine_r, "tests", "resultats", "epreuves_longues", "78", "Mini", "RESULTAT.json")
        ok78 = lancer(["git", "-C", nu, "rev-parse", "epreuves-longues/78/Ok"])[1].strip()
        lancer(["git", "-C", nu, "update-ref", "refs/heads/epreuves-longues/78/Mini", ok78])
        c, bilan = R.rapatrier(racine_r, "78", depuis=nu)
        try:
            garde = json.load(open(rangee78, encoding="utf-8")).get("code_de_sortie") == 3
        except (OSError, ValueError):
            garde = False
        if c != 2 or not garde or not any("ancien résultat gardé" in l for l in bilan):
            faux.append(f"R5 (R-D5) branche sans son dossier : code {c}, ancien résultat gardé {garde} : {bilan}")
        # R6 : une branche que le passage ne demande pas ; R7 : aucune DEMANDE.json
        deposer("79", "Ok", ["Ok"])
        deposer("79", "Mini", ["Ok"])
        c, bilan = R.rapatrier(racine_r, "79", depuis=nu)
        if c != 2 or not any("NON DEMANDÉE" in l for l in bilan):
            faux.append(f"R6 branche non demandée : code {c} : {bilan}")
        deposer("80", "Ok", None)
        c, bilan = R.rapatrier(racine_r, "80", depuis=nu)
        if c != 2 or not any("INCONNUE" in l for l in bilan):
            faux.append(f"R7 sans DEMANDE.json : code {c} : {bilan}")
        c, bilan = R.rapatrier(racine_r, "7a", depuis=nu)
        if c != 2:
            faux.append(f"R3 passage « 7a » : code {c}")
        # P : la provenance
        vraie = plus_petit_enregistre(racine)
        pub = os.path.join(d, "public")
        for rel, contenu in (("tests/outils/VOLE.py", open(os.path.join(racine, vraie), "rb").read() if vraie else b""),
                             ("donnees/x.csv", b"a,b\n"), ("programmes/OK.py", b"x = 1\n"), ("tests/VIDE.py", b"")):
            os.makedirs(os.path.dirname(os.path.join(pub, rel)), exist_ok=True)
            open(os.path.join(pub, rel), "wb").write(contenu)
        os.symlink(os.path.join(racine, FABRICANT), os.path.join(pub, "programmes", "LIEN.py"))
        ecrits = ["tests/outils/VOLE.py", "donnees/x.csv", "programmes/OK.py", "tests/VIDE.py", "programmes/LIEN.py",
                  "programmes/RETIRE.py"]
        try:
            refus, note = F.refus_selon_la_provenance(racine, pub, ecrits)
            refuses = sorted(r.split(" : ")[0] for r in refus)
            if vraie is None or refuses != ["donnees/x.csv", "programmes/LIEN.py", "tests/outils/VOLE.py"]:
                faux.append(f"P1 vraie donnée {vraie} : refus {refus}")
        except (OSError, ValueError) as e:
            faux.append(f"P1 le contrôle n'a pas tourné : {e}")
        sans = os.path.join(d, "prive_sans_registre")
        os.makedirs(os.path.join(sans, "donnees"))
        try:
            F.refus_selon_la_provenance(sans, pub, ecrits)
            faux.append("P2 registre absent avec un dossier donnees/ : accepté")
        except OSError:
            pass
        os.rmdir(os.path.join(sans, "donnees"))
        try:
            if F.refus_selon_la_provenance(sans, pub, ecrits)[0]:
                faux.append("P2 dépôt sans registre ni données : des refus")
        except OSError as e:
            faux.append(f"P2 dépôt sans registre ni données : {e}")
        faux += etage_a(F, d)
        # P3 : le fabricant en ligne de commande sur une COPIE de la VRAIE racine, placée sur la branche BRANCHE_DE_P3
        # (`copie_sur_une_branche`), vers un clone public neuf de la même branche. La copie porte sa propre branche :
        # P3 ne dépend plus de la branche de la racine (certification du 17-11-2026, cause C6 : sur la tête détachée
        # de la machine de certification, la racine n'a pas de branche et le fabricant refusait). Joué seulement si
        # la source porte tout le dépôt, historique entier : sur un clone superficiel, l'étage A s'arrête, voulu.
        source = source_git or racine
        cb = lancer(["git", "-C", source, "rev-parse", "--verify", "HEAD"])[0]
        superficiel = lancer(["git", "-C", source, "rev-parse", "--is-shallow-repository"])[1].strip() == "true"
        if superficiel:
            NOTES.append("P3 non joué : la racine est un clone superficiel (shallow)")
        if os.path.isfile(os.path.join(source, ".github", "workflows", "collecte_abc.yml")) and cb == 0 and not superficiel:
            etat_avant = etat_de_la_source(source)
            prive3 = copie_sur_une_branche(source, racine, d)
            P3_JOUES.append(source)
            pub3 = os.path.join(d, "public3")
            ci, oi = lancer(["git", "init", "-q", "-b", BRANCHE_DE_P3, pub3])
            if ci != 0:
                raise ErreurDOutillage(f"git init du clone public de P3 : code {ci} : {oi[-200:]}")
            c, o = lancer([sys.executable, "-B", os.path.join(prive3, FABRICANT), prive3, pub3])
            if c != 0 or not re.search(r"provenance : \d+ fichier\(s\) écrit\(s\) .* ; 0 refus", o) \
                    or not re.search(r"étage A : \d+ fichier\(s\) .* ; 0 refus · témoin : les \d+ chemins", o):
                ligne = f"P3 fabricant sur la copie de la racine : code {c} : {o[-300:]}"
                if fragment_p3 is not None:
                    # le fragment cherché dans la sortie ENTIÈRE (R1) : il peut être avant les 300 derniers caractères
                    i = o.find(fragment_p3)
                    ligne += (f" · fragment attendu vu dans la sortie entière : …{o[max(0, i - 80):i + len(fragment_p3) + 80]}…"
                              if i >= 0 else " · fragment attendu ABSENT de la sortie entière du fabricant")
                faux.append(ligne)
            etat_apres = etat_de_la_source(source)
            ecarts = []
            for i, quoi in enumerate(("la tête", "la branche de la tête", "les références", "le disque hors .git")):
                if etat_apres[i] != etat_avant[i]:
                    ecart = (sorted(set(etat_avant[i]) ^ set(etat_apres[i]))[:3] if i == 3
                             else (etat_avant[i], etat_apres[i]))
                    ecarts.append(f"P3 a changé {quoi} de la racine : {str(ecart)[:300]}")
            if ecarts and fragment_p3 is not None:
                # dans un tour de sabotage, un écart du contrôle d'après n'est jamais une morsure (R1)
                raise ErreurDOutillage("contrôle d'après P3 dans un tour de sabotage (un autre programme écrit-il dans "
                                       "la racine ?) : " + " | ".join(ecarts))
            faux += ecarts
    except ErreurDOutillage:
        raise
    except Exception as e:   # noqa: BLE001 — une erreur imprévue est un cas faux, jamais un passage
        faux.append(f"erreur imprévue : {type(e).__name__} : {e}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


SABOTAGES = {
    "SE01_joueur_transmet_les_fichiers_de_commandes": [
        (JOUEUR, "        for v in F.FICHIERS_DE_COMMANDES_DE_GITHUB:\n", "        for v in ():\n")],
    "SE02_joueur_ignore_les_interdits_nommes": [(JOUEUR, "    nommes = [n for n in interdits if n[:-3] in texte]\n",
                                                 "    nommes = []\n")],
    "SE03_joueur_delai_rendu_vert": [(JOUEUR, "            code_de_sortie = 124\n", "            code_de_sortie = 0\n")],
    "SE04_joueur_perd_les_arguments": [(JOUEUR, '+ [a.replace("{copie}", copie) for a in arguments]', "+ [copie]")],
    "SE05_joueur_perd_les_erreurs": [(JOUEUR, "stdout=f, stderr=subprocess.STDOUT", "stdout=f, stderr=subprocess.DEVNULL")],
    "SE06_table_arguments_libres": [(FABRICANT, 'ARGUMENT_FIGE = r"\\{copie\\}|[A-Za-z0-9_.=,-]{1,40}"',
                                     'ARGUMENT_FIGE = r"\\{copie\\}|.+"')],
    "SE07_table_admet_le_saboter_d_une_serie": [(FABRICANT, '        if chemin in series and "--saboter" in arguments:\n',
                                                 "        if False:\n")],
    "SE08_epreuves_hors_du_budget": [(FABRICANT, '"en_meme_temps": PARTS_EN_MEME_TEMPS, "branches": EPREUVES_BRANCHES,',
                                      '"en_meme_temps": 16, "branches": EPREUVES_BRANCHES,')],
    "SE09_epreuves_dans_un_autre_groupe": [(FABRICANT, '"groupe": GROUPE_DES_MACHINES_LONGUES,\n    "entrees": EPREUVES_ENTREES,',
                                            '"groupe": "epreuves-longues",\n    "entrees": EPREUVES_ENTREES,')],
    "SE10_provenance_sans_empreintes": [(FABRICANT, 'hashlib.sha256(open(p, "rb").read()).hexdigest() in empreintes:',
                                         'False:')],
    "SE11_provenance_sans_les_dossiers": [(FABRICANT, '        elif rel in chemins or rel.split("/")[0] in dossiers:\n',
                                           "        elif rel in chemins:\n")],
    "SE12_provenance_registre_absent_tolere": [
        (FABRICANT, '            raise OSError(f"{REGISTRE_DE_PROVENANCE} absent alors que le dépôt privé a un dossier '
                    '{DOSSIER_DES_DONNEES}/")\n', '            return [], "registre absent"\n')],
    "SE13_rapatrieur_ne_lit_pas_le_code": [(RAPATRIEUR, "            codes.append(0 if cs == 0 else 1)\n",
                                            "            codes.append(0)\n")],
    "SE14_rapatrieur_tolere_un_resultat_absent": [(RAPATRIEUR, "            codes.append(2)\n        finally:\n",
                                                   "            codes.append(0)\n        finally:\n")],
    "SE15_matrice_ignore_la_demande": [(FABRICANT, '--matrice . "$EPREUVES")', "--matrice . toutes)")],
    "SE17_filet_sans_les_branches_des_epreuves": [
        (FABRICANT, 'BRANCHES_DES_GABARITS = {"series": SERIES_BRANCHES, "epreuves": EPREUVES_BRANCHES}',
         'BRANCHES_DES_GABARITS = {"series": SERIES_BRANCHES}')],
    "SE18_etage_a_sans_l_historique": [(FABRICANT, '                if blob in voulus:\n                    lieux.setdefault(blob, set())',
                                         '                if False:\n                    lieux.setdefault(blob, set())')],
    "SE19_etage_a_sans_le_disque": [(FABRICANT, '                if b in voulus:\n                    lieux.setdefault(b, set()).add(rel)',
                                     '                if False:\n                    lieux.setdefault(b, set()).add(rel)')],
    "SE20_etage_a_exempte_les_py": [(FABRICANT, "        prives = sorted(c for c in lieux.get(b, ()) if not est_un_chemin_publie(c))",
                                     "        prives = sorted(c for c in lieux.get(b, ()) if not est_un_chemin_publie(c) and not c.endswith('.py'))")],
    # SE21 (la clause « déjà public » retirée) n'a plus d'objet depuis F1 (15-11-2026) : la clause n'existe plus.
    # SE35 et SE36 la REMETTENT, lue au privé puis au public : X2 et X3, puis X4, doivent rougir.
    "SE35_etage_a_exempte_main_du_prive": [(FABRICANT, "    refus = []\n    for rel, b in publies.items():\n", '    deja = set()\n    for depot_lu in (prive,):\n        for ref in ("refs/remotes/origin/main", "refs/heads/main"):\n            try:\n                arbre = _git_prive(depot_lu, "ls-tree", "-r", "-z", "--full-tree", ref)\n            except OSError:\n                continue\n            for e in arbre.split(b"\\0"):\n                if e:\n                    meta, chemin = e.split(b"\\t", 1)\n                    if est_un_chemin_publie(chemin.decode("utf-8", "surrogateescape")):\n                        deja.add(meta.decode().split()[2])\n' + "    refus = []\n    for rel, b in publies.items():\n"),
                                           (FABRICANT, "        if avec_git and prives:\n", "        if avec_git and prives and b not in deja:\n")],
    "SE36_etage_a_exempte_ce_qui_est_au_public": [(FABRICANT, "    refus = []\n    for rel, b in publies.items():\n", '    deja = set()\n    for depot_lu in (public,):\n        for ref in ("refs/remotes/origin/main", "refs/heads/main"):\n            try:\n                arbre = _git_prive(depot_lu, "ls-tree", "-r", "-z", "--full-tree", ref)\n            except OSError:\n                continue\n            for e in arbre.split(b"\\0"):\n                if e:\n                    meta, chemin = e.split(b"\\t", 1)\n                    if est_un_chemin_publie(chemin.decode("utf-8", "surrogateescape")):\n                        deja.add(meta.decode().split()[2])\n' + "    refus = []\n    for rel, b in publies.items():\n"),
                                                  (FABRICANT, "        if avec_git and prives:\n", "        if avec_git and prives and b not in deja:\n")],
    "SE37_refus_sans_le_remede": [(FABRICANT, ' — étage A ; remède : {REMEDE_DE_L_ETAGE_A}")', ' — étage A")')],
    "SE39_remede_qui_propose_de_retirer": [(FABRICANT, 'REMEDE_DE_L_ETAGE_A = "changer une ligne du fichier publié (comme 32aa88d0)"',
                                            'REMEDE_DE_L_ETAGE_A = "changer une ligne du fichier publié (comme 32aa88d0) ou retirer la copie"')],
    "SE38_refus_sans_le_blob_entier": [(FABRICANT, '(blob {b}), qu\'un fichier du dépôt privé', '(blob {b[:12]}), qu\'un fichier du dépôt privé')],
    "SE22_temoin_retire": [(FABRICANT, "        if manquants:\n            raise OSError(f\"témoin du parcours : {len(manquants)}",
                            "        if False:\n            raise OSError(f\"témoin du parcours : {len(manquants)}")],
    "SE23_superficiel_admis": [(FABRICANT, '"--is-shallow-repository").strip() != b"false":', '"--is-shallow-repository").strip() == b"jamais":')],
    "SE24_publie_le_disque": [(FABRICANT, "        with open(cible, \"wb\") as f:\n            f.write(octets)",
                               "        with open(cible, \"wb\") as f:\n            f.write(open(os.path.join(prive, *chemin.split(\"/\")), \"rb\").read())")],
    "SE25_lien_du_commit_ecrit_en_fichier": [(FABRICANT, '        if mode == "120000":\n', '        if False:\n')],
    "SE26_rapatrieur_sans_liste_demandee": [(RAPATRIEUR, "            if c not in vus:\n", "            if False:\n")],
    "SE27_rapatrieur_efface_avant_de_copier": [(RAPATRIEUR, "            voisin = cible + \".neuf\"\n",
                                                "            voisin = cible + \".neuf\"\n            shutil.rmtree(cible, ignore_errors=True)\n")],
    "SE28_delai_constant": [(JOUEUR, "    delai = delai_restant(F, os.environ.get(\"DEPART_DU_JOB\"), time.time())\n",
                             "    delai = DELAI\n"), (JOUEUR, "    try:\n        debut = int(depart)\n", "    return DELAI\n    try:\n        debut = int(depart)\n")],
    "SE29_valeur_refusee_citee_admise": [(FABRICANT, "        citee = valeur_citee_apres_un_motif(texte)\n", "        citee = None\n")],
    "SE30_relais_sans_ses_circuits_admis": [(FABRICANT, "    if CIRCUIT_RELAIS.replace(os.sep, \"/\") not in ecrits:\n        return []\n",
                                             "    return []\n")],
    "SE31_jouer_sans_la_matrice": [(FABRICANT, "          printf '%%s\\\\n' \"$MATRICE\" > ", "          true \"$MATRICE\" > ")],
    "SE32_publier_sans_le_commit_extrait": [(FABRICANT, "    if sha_publie is not None and sha != sha_publie:\n", "    if False:\n")],
    "SE33_lignes_muettes_sur_un_dossier_illisible": [(FABRICANT, "os.walk(os.path.join(prive, DOSSIER_DES_DONNEES), onerror=_ne_pas_taire)",
                                                      "os.walk(os.path.join(prive, DOSSIER_DES_DONNEES))")],
    "SE34_etage_a_juge_une_copie_sans_git": [(FABRICANT, "        if avec_git and prives:\n",
                                              "        if prives:\n")],
    "SE16_jouer_sans_couper_le_reseau": [(FABRICANT, '          unshare -rn python3 -B -u tests/outils/jouer_une_epreuve_longue.py',
                                          '          python3 -B -u tests/outils/jouer_une_epreuve_longue.py')],
    # SE40 (cause C6 du 17-11-2026) : la garde d'entrée du fabricant en ligne de commande (`fabriquer_et_publier`)
    # refuse tout clone public, quelle que soit la branche. Seul P3 lance le fabricant en ligne de commande sur un vrai
    # dépôt et un clone public qui a un .git : il doit rougir, et ce tour le joue (JOUENT_P3). La garde de `publier`
    # n'est pas touchée : A5 la juge, et SE40 ne doit mordre que par P3 — par la ligne « P3 fabricant » qui porte
    # « garde sabotée », le fragment attendu que JOUENT_P3 lui associe.
    "SE40_garde_d_entree_refuse_tout": [(FABRICANT, "        refus = refus_de_branche(prive, public)\n",
                                         "        refus = refus_de_branche(prive, public) or \"garde sabotée\"\n")],
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1, 2 ou CODE_D_OUTILLAGE (3). [rend: 1]
    ⑥ TRAITEMENT — ⓪ les variables locales de git retirées de l'environnement (`retirer_les_variables_locales_de_git`),
      avant tout git ; celles qui étaient posées sont dites dans une NOTE · ① la cohérence de JOUENT_P3 : chaque nom
      existe dans SABOTAGES, chaque fichier que ce sabotage vise fait partie de LUS, et son fragment attendu est un
      texte non vide, présent dans un texte que le sabotage injecte et absent du fichier visé de la racine tel quel ;
      sinon ErreurDOutillage · ② un tour tel quel ; si P3 n'y a pas été joué (clone superficiel, sans .git, sans
      .github/workflows/collecte_abc.yml), la ligne Z0 dit « P1, P2 conformes · P3 NON JOUÉ » au lieu de compter P3
      parmi les conformes (code de sortie inchangé) ; avec --saboter (ou --saboter=SE01,…),
      une copie de la racine par sabotage (les fichiers que l'épreuve lit, LUS, la plus petite donnée enregistrée,
      les épreuves de la table), le fichier visé écrit saboté, un tour par copie · ③ une ErreurDOutillage, d'où
      qu'elle vienne, arrête tout : « ERREUR D'OUTILLAGE : <message> » est affiché et le code est CODE_D_OUTILLAGE,
      sans verdict.
      Les sabotages de JOUENT_P3 donnent aussi la vraie racine à `tour` (`source_git`) : P3 y est joué sur une copie
      de la racine où les fichiers sabotés remplacent les vrais ; si P3 ne peut pas s'y jouer (racine superficielle,
      sans .git), le sabotage est dit NON JOUÉ et ne compte pas, comme P3 lui-même dans Z0. Un sabotage de JOUENT_P3
      ne « mord » que si une ligne de son tour commence par « P3 fabricant » et porte son fragment attendu (`tour`
      l'y recopie depuis la sortie ENTIÈRE du fabricant) ; tout autre cas faux de ce tour ne compte pas, et un écart
      du contrôle d'après y est une ErreurDOutillage (levée par `tour`). Les autres sabotages mordent dès qu'un cas
      est faux.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. L'assertion ① : superviseur R-759 du 17-11-2026, Q4 (relecture m3 :
      JOUENT_P3 est une énumération à tenir à la main, et un sabotage de JOUENT_P3 qui viserait un fichier hors de LUS
      jouerait P3 sur des fichiers non sabotés). Le code distinct ③ : Q5 (relecture m4). Le fragment attendu, la
      morsure par la seule ligne « P3 fabricant » : relecture du 17-11-2026, tour 3, MAJEUR 1 ; superviseur R-759, R1.
      « P3 NON JOUÉ » dans Z0 : même relecture, MINEUR 1 ; R2. L'étape ⓪ : MINEUR 3 ; R4.
    ⑨ CE QUI CLOCHE — La copie sabotée n'a pas le dépôt entier : hors des sabotages de JOUENT_P3, P3 n'y est pas joué
      (il exige .github/workflows/collecte_abc.yml et un .git). JOUENT_P3 reste une liste déclarée, vérifiée par ①, et
      non une propriété calculée du sabotage — À VALIDER PAR JEAN-LUC (simplification acceptée par le superviseur).
      ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        retires = retirer_les_variables_locales_de_git()
        if retires:
            NOTES.append("variables locales de git retirées de l'environnement de l'épreuve : " + ", ".join(retires))
        for nom, fragment in JOUENT_P3.items():
            if nom not in SABOTAGES:
                raise ErreurDOutillage(f"JOUENT_P3 nomme {nom}, absent de SABOTAGES")
            hors = [fichier for fichier, _, _ in SABOTAGES[nom] if fichier not in LUS]
            if hors:
                raise ErreurDOutillage(f"JOUENT_P3 : {nom} vise {hors}, hors de LUS (P3 ne les reporte pas dans sa copie)")
            if not isinstance(fragment, str) or not fragment or not any(fragment in b for _, _, b in SABOTAGES[nom]):
                raise ErreurDOutillage(f"JOUENT_P3 : le fragment attendu de {nom} ({fragment!r}) est vide ou n'est pas "
                                       "dans le texte que ce sabotage injecte")
            try:
                tels_quels = [open(os.path.join(DEPOT, fichier), encoding="utf-8").read() for fichier, _, _ in SABOTAGES[nom]]
            except OSError as e:
                raise ErreurDOutillage(f"JOUENT_P3 : fichier visé par {nom} illisible : {e}")
            if any(fragment in x for x in tels_quels):
                raise ErreurDOutillage(f"JOUENT_P3 : le fragment attendu de {nom} est déjà dans le fichier visé tel quel")
        joues_avant_z0 = len(P3_JOUES)
        faux = tour(DEPOT)
        p3 = "P1 à P3, " if len(P3_JOUES) > joues_avant_z0 else ""
        print("Z0 programmes tels quels : " + (f"T0 à T2, G1 à G5, J1 à J6, E3a, E7, E10a, R1 à R7, {p3}A1 à A8, X2 à X4"
                                                + (" conformes" if p3 else ", P1, P2 conformes · P3 NON JOUÉ")
                                                if not faux else "FAUX " + " | ".join(faux)))
        for n in dict.fromkeys(NOTES):
            print("NOTE " + n)
        code = 1 if faux else 0
        choix = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
        if "--saboter" in sys.argv or choix:
            table = json.load(open(os.path.join(DEPOT, TABLE), encoding="utf-8"))
            a_copier = list(LUS) + [plus_petit_enregistre(DEPOT)] + [e["chemin"] for e in table["epreuves_longues"].values()]
            for nom in [n for n in SABOTAGES if not choix or n in choix[0] or n.split("_")[0] in choix[0]]:
                d = tempfile.mkdtemp(prefix="epreuves_longues_sab_")
                try:
                    for f in a_copier:
                        os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
                        shutil.copyfile(os.path.join(DEPOT, f), os.path.join(d, f))
                    for fichier, a, b in SABOTAGES[nom]:
                        t = open(os.path.join(d, fichier), encoding="utf-8").read()
                        if t.count(a) != 1:
                            print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                            return 2
                        open(os.path.join(d, fichier), "w", encoding="utf-8").write(t.replace(a, b))
                    joues_avant = len(P3_JOUES)
                    f = tour(d, source_git=DEPOT if nom in JOUENT_P3 else None, fragment_p3=JOUENT_P3.get(nom))
                finally:
                    shutil.rmtree(d, ignore_errors=True)
                if nom in JOUENT_P3 and len(P3_JOUES) == joues_avant:
                    print(f"{nom} NON JOUÉ : P3 ne se joue pas sur cette racine (voir la NOTE de Z0, ou : sans .git, "
                          "sans .github/workflows/collecte_abc.yml)")
                    continue
                if nom in JOUENT_P3:
                    # R1 : seule la ligne « P3 fabricant » qui porte le fragment attendu est une morsure
                    morsures = [l for l in f if l.startswith("P3 fabricant") and JOUENT_P3[nom] in l]
                    print(f"{nom} {'mord' if morsures else 'NE MORD PAS'} : {(morsures or f)[:3]}")
                    code |= 0 if morsures else 1
                    continue
                print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f[:3]}")
                code |= 0 if f else 1
    except ErreurDOutillage as e:
        print(f"ERREUR D'OUTILLAGE : {e}")
        print(f"VERDICT : aucun — l'épreuve n'a pas pu se jouer (code {CODE_D_OUTILLAGE})")
        return CODE_D_OUTILLAGE
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
