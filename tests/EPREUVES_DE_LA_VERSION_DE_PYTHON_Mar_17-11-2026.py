#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_VERSION_DE_PYTHON — Mar 17-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Décision de Jean-Luc A-874 du 17-11-2026 à 07h48 (réponse « 1 ») : fixer la version de Python des
circuits qui n'en imposaient aucune — le circuit du soir et les autres, qui prenaient celle de la machine GitHub du
moment —, comme le fait déjà la certification (.github/workflows/certifier.yml du dépôt privé, ligne 48 au
17-11-2026 : `python-version: "3.11"`). Le code est certifié sous UNE version ; un circuit qui le joue sous une autre
joue du code non certifié. Les circuits du dépôt public sont FABRIQUÉS par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py ;
la version y est écrite UNE fois, dans la constante VERSION_DE_PYTHON (deux écritures d'une même chose divergent
toujours, R-708). Cette épreuve garde trois propriétés : ① chaque job d'un circuit fabriqué qui lance Python pose
actions/setup-python ; ② chaque pose porte la version de la constante ; ③ la constante est la version de la fiche de
certification du dépôt privé ; ④ (relecteur neuf du 17-11-2026, D1 et D2) chaque module hors bibliothèque standard
qu'exécute un pas du circuit du soir est installé par un pas PLUS TÔT du même job — le Python posé n'a que pip, et
la certification installe plus de paquets que le soir (coverage, numpy, pyflakes, cryptography, pyyaml contre le seul
cryptography) : un `import yaml` neuf dans un programme du soir serait certifié vert et tomberait le soir.

① RÔLE — Fabriquer les circuits publics dans la racine donnée (sans rien écrire : `ce_que_la_publication_ecrit`, la
  liste même que la publication écrit), les relever job par job, et rougir si une propriété ci-dessus tombe.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine) ; à la main avant
  toute livraison qui touche la pose de Python dans le fabricant (R-731) :
  python3 -B tests/EPREUVES_DE_LA_VERSION_DE_PYTHON_Mar_17-11-2026.py <racine> [--saboter | --saboter=SV1,…]
③ ENTRÉE — La racine d'un dépôt : programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, programmes/FORME_D_UN_JETON.py,
  tests/LANCEMENT_DES_EPREUVES.json, .github/workflows/collecte_abc.yml (la source du circuit du soir) et
  .github/workflows/certifier.yml (la certification du privé, référence de la version). Pour la propriété ④ : tous
  les programmes de programmes/ et de la racine (les programmes du soir et ce qu'ils lancent), le relevé des fichiers
  dont un programme dépend (`dependances`, programmes/COPIER_POUR_LES_BOUCLES.py, écrit pour CERT-3) et la lecture
  de ce qu'installe un pas (`paquets_installes`, tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py, écrite pour
  E6 bis) — IMPORTÉS, jamais recopiés (deux écritures d'une même chose divergent toujours, R-708). Le fabricant
  lui-même TOURNE au soir : le pas « Le circuit public est-il celui que fabrique le depot prive ? » (gabarit DECISION
  du fabricant, jobs faut_il_tourner et collecte) lance `python3 programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py` ; ce qu'il
  importe ou charge par chemin compte donc pour le soir (superviseur R-759 du 17-11-2026, N1).
④ CONDITIONS D'ENTRÉE — Le module yaml (PyYAML) est installé : la certification l'installe (INSTALLER_LA_MESURE du
  fabricant). Absent : code 1 et le dire (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0). Avec --saboter :
  l'entrée simple de cette épreuve dans la table des délais (tests/LANCEMENT_DES_EPREUVES.json, « delais »,
  « secondes ») se lit et vaut un nombre positif — c'est le délai de chaque copie sabotée ; sinon code 1, dit.
⑤ SORTIE — Le code de sortie : 0 si chaque cas donne la réponse attendue et, avec --saboter, si chaque sabotage fait
  rougir au moins un cas POUR SA RAISON ; 1 sinon ; 2 si un sabotage ne s'applique plus. À l'écran : le relevé, une
  ligne par job de chaque circuit fabriqué (lance Python ? version posée ?).
  [rend: 1]
⑥ TRAITEMENT —
  C (le relevé, calibré avant de servir) : C1 sur la VRAIE fiche fabriquée certifier_la_version.yml (R-732), le relevé
  trouve une pose dans le job « certifier » et le job « preparer » (un clonage et un pas bash) ne lance pas Python ;
  C2 sur un circuit d'essai qui ÉCRIT « actions/setup-python » et « python-version » dans un commentaire, dans un
  texte « echo » et dans un nom de pas, sans les poser, le relevé ne trouve AUCUNE pose (il ne sur-détecte pas) ;
  C3 sur ce même circuit, le job dont le shell par défaut est python3 et le job qui lance « python3 -B x.py »
  lancent Python, le job « bash echo python » non.
  V (les circuits fabriqués) : V0 le TÉMOIN — les cinq circuits que la publication écrit sont relevés (sinon le
  relevé ne prouverait rien) ; V1 la constante VERSION_DE_PYTHON existe et a la forme « 3.N » (version mineure,
  sans numéro de correctif) ; V2 chaque job qui lance Python pose actions/setup-python ; V3 chaque pose porte la
  version de la constante ; V4 la pose précède, dans le circuit du soir, tout pas du job (le circuit du soir est tout
  entier joué sous la version : ses jobs passent chaque pas par python3).
  P (la certification du privé) : P1 .github/workflows/certifier.yml pose actions/setup-python, à la version de la
  constante.
  M (les modules qu'exécute le soir, propriété ④ ; `besoins_d_un_pas`) : M0 le relevé, calibré sur un dépôt d'essai
  (un programme qui écrit « import numpy » dans un texte explicatif et « import yaml » dans une chaîne, importe os et
  json, essaie `import requests` sous « except ImportError » et importe d'un second programme qui fait
  `importlib.import_module("pandas")` ; un pas qui écrit _piege.py puis lance « python3 -c "import os, _piege;
  import toml" », puis « python3 -m pip install x », « python3 -m json.tool f.json » et « python3 -B -m black ») rend
  exactement {requests, pandas, toml, black} — ni le texte, ni la bibliothèque standard, ni le fichier que le pas
  écrit lui-même, ni pip ; M1 sur la VRAIE fiche du soir (R-732), le relevé retrouve le cas connu : `cryptography`,
  importé par programmes/PROTEGER_LA_PAGE.py, que programmes/PUBLIER_LE_SITE.py lance au pas du cockpit (sinon le
  relevé ne prouverait rien) ; M2 chaque module relevé pour un pas d'un job du soir est installé par un pas
  « pip install » placé AVANT lui dans le même job, et ce pas ne porte pas de clé « if: » (un pas sous « if: » peut
  être sauté sans rien dire : il n'installe rien aux yeux de M2 ; superviseur R-759 du 17-11-2026, N2). La clé
  « continue-on-error » reste PERMISE : CHIFFREMENT_DU_SOIR la porte à dessein (une installation tombée n'empêche
  pas la collecte, et le pas du cockpit rougit en le disant) — un échec qui se dit est permis, un saut qui se tait ne
  l'est pas. Ce n'est PAS la règle d'E6 bis (tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py), qui refuse aussi
  « continue-on-error » sur le pas qui installe la certification : la sémantique diffère, E6 bis n'est pas réutilisée.
  SABOTAGES (--saboter), chacun sur une copie des fichiers lus : SV1 la pose retirée du circuit du soir → V2 ;
  SV2 la constante changée du seul côté du fabricant → P1 ; SV3 la version changée du seul côté de la fiche de
  certification du privé → P1 ; SV4 la pose écrite en dur dans le départ de la certification, à une autre version
  que la constante → V3 ; SV5 le relevé qui prend une pose écrite dans un texte pour une vraie → C2 ; SV6 la pose
  du job de décision du soir placée après les clonages → V4 ; SV7 le pas qui installe cryptography retiré du soir →
  M2 (D1) ; SV8 un « import yaml » ajouté à programmes/TENIR_L_HISTORIQUE.py, que le soir lance, sans l'installer →
  M2 (D2) ; SV9 le relevé privé de son filtre de la bibliothèque standard → M0 ; SV10 la coupe du fabricant retirée →
  M2 (le faux positif `coverage` revient : la coupe porte le vert, elle n'est pas une décoration) ; SV11 un
  `import CERTIFIER_LA_VERSION` ajouté au fabricant → M2 avec coverage (un vrai import n'est pas coupé, N1) ; SV12
  `subprocess.run([sys.executable, "programmes/CERTIFIER_LA_VERSION.py"])` ajouté au fabricant → le garde tombe, la
  coupe disparaît, M2 avec coverage (N1) ; SV13 le relevé privé de « python3 -m » → M0 (black, N4) ; SV14
  `if: ${{ false }}` sur le pas qui installe cryptography → M2 (N2) ; SV15 ce pas déplacé dans le job de décision →
  M2 au job collecte (« même job », N3) ; SV16 ce pas placé juste après le pas du cockpit → M2 (« plus tôt », N3).
  Quand un sabotage déclare des textes attendus, ils doivent figurer dans la sortie de la copie : il mord alors
  POUR SA RAISON, pas seulement par le bon cas.
⑦ UNITÉ — Des codes de sortie ; une version de Python, « majeure.mineure » (texte).
⑧ POURQUOI — R-731 : tout code écrit a ses épreuves au dépôt, avec des sabotages qui mordent chacun pour sa raison.
  A-874 : la version se fixe à un seul endroit et se vérifie, elle ne se suppose pas.
⑨ CE QUI CLOCHE — Rien n'est joué sur GitHub : que actions/setup-python@v5 mette bien python3 3.11 devant le
  python3 de la machine, pour un shell « python3 programmes/ETAPE_MUETTE.py {0} », est THÉORIQUE ici (documentation de
  l'action : elle ajoute l'interpréteur en tête du PATH). Dans la certification, les séries et les épreuves longues,
  la pose vient APRÈS les pas de départ (pose du code, contrôle du circuit), qui tournent donc encore sous le Python
  de la machine : V4 ne le vérifie que pour le circuit du soir (à consigner au BACKLOG). « Lancer Python » est relevé
  sur le texte des pas (shell par défaut, shell du pas, commande « python » ou « python3 » en tête de mot) : un
  programme lancé par un autre nom (un « #! » exécuté directement) échapperait au relevé.
  Propriété ④ — relevé statique, sur-approximé à dessein : tout nom « X.py » écrit dans une chaîne d'un programme
  atteint est suivi (`dependances`), qu'il soit lancé ou seulement cité dans un message ; un module importé dans une
  branche jamais jouée compte. UNE SEULE COUPE, sur le SEUL programme qui écrit les circuits, le fabricant
  (`coupe_du_fabricant`, superviseur R-759 du 17-11-2026, N1) : coupe = les programmes que nomment les commandes des
  circuits fabriqués, MOINS ceux que le fabricant importe (`import`, `from`), MOINS ceux qu'il charge par chemin
  (FORME_D_UN_JETON.py par `spec_from_file_location`, constante MODULE_DU_JETON). Le fabricant TOURNE au soir ; ce
  qu'il importe ou charge compte, ce qu'il seulement nomme dans une commande qu'il écrit ne tourne pas chez lui. Sans
  la coupe, programmes/CERTIFIER_LA_VERSION.py, nommé dans le gabarit de la certification, ferait exiger `coverage` au
  soir (relecteur neuf du 17-11-2026, §1a : faux positif ; SV10). LA COUPE N'EST JUSTE QUE TANT QUE LE GARDE TIENT :
  le fabricant ne lance aucun interpréteur (pas de `sys.executable`, `runpy`, `exec`, `os.system` — plus, ajoutés par
  l'auteur, `eval`, `os.popen`, `os.exec*`, `os.spawn*` et tout import de noms de subprocess — et chaque appel
  subprocess lance un programme littéral qui n'est pas « python* » : aujourd'hui `git` seulement). Si le garde tombe,
  la coupe est supprimée et le faux positif `coverage` rougit (SV12). LIMITE ÉCRITE : le garde est une liste de
  formes interdites : neuf formes ordinaires le contournent sans le faire tomber (relecteur du 17-11-2026, R1 :
  import subprocess as sp, getattr(subprocess,"run"), ["env","python3",…], ["bash","-c","python3 …"], from os
  import execv, import os as o; o.system, os.posix_spawn, pty.spawn, functools.partial(subprocess.run)) ; un
  chargeur par chemin écrit en deux fonctions échappe à la coupe (R2) ; seuls SV12 et le garde entier ont un
  sabotage (R3). Aujourd'hui le fabricant ne lance que git (mesuré : 18 commandes, M0 à M2 conformes) : le relevé
  est juste ; le trou ne s'ouvre que si le fabricant change. Réparation de fond prévue (BACKLOG) : garde en LISTE
  POSITIVE. Ce que la coupe ne voit
  pas : un chargement par un nom COMPOSÉ à l'exécution (`import_module(nom)`, un chemin bâti hors littéral et hors
  constante) — le fichier ainsi chargé, s'il est aussi nommé dans une commande, serait coupé à tort. Ce principe
  (« un nom dans une chaîne n'est jamais un import ») ne vaut QUE pour le fabricant : programmes/PUBLIER_LE_SITE.py
  lance programmes/PROTEGER_LA_PAGE.py par subprocess, d'une chaîne (c'est le cas M1). À VALIDER PAR JEAN-LUC : la
  coupe comme exception propre au fabricant, gardée par une propriété ; et, pour M2, « continue-on-error » permis,
  « if: » interdit sur un pas d'installation du soir. « python3 -m X » est relevé comme un import de X, sauf pip
  (N4) ; un « -m » suivi d'un nom composé par le shell ne se voit pas. Un nom de module composé à l'exécution, un
  programme lancé par un nom composé, un paquet installé autrement que par « pip install » au début d'une ligne ne se
  voient pas. ④ lit le texte du pas, pas l'effet de pip (--dry-run, --target, install puis uninstall,
  -r requirements non compris ; relecteur du 17-11-2026, R4). Le nom d'import se rapproche du nom pip par les métadonnées des paquets
  installés là où l'épreuve tourne (`importlib.metadata.packages_distributions`) : un module absent d'ici n'est
  reconnu que si son nom pip est le sien. Ce qui est installé n'est pas épinglé (m1 du relecteur, consigné, pas
  corrigé ici).
⑩ EFFET — Écrit dans des dossiers jetables (sabotages), effacés à la fin.
⑪ TERMINAISON — Rend la main ; sort par sys.exit.
  [sort: oui]
"""
import ast
import importlib.util
import os
import re
import shutil
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
JETON = "programmes/FORME_D_UN_JETON.py"     # chargé par le fabricant, à côté de lui
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"   # lue par le fabricant à l'import (séries, épreuves longues)
SOURCE_DU_SOIR = ".github/workflows/collecte_abc.yml"
CERTIFICATION_PRIVEE = ".github/workflows/certifier.yml"
COPIEUR = "programmes/COPIER_POUR_LES_BOUCLES.py"           # `dependances` : de quels fichiers un programme dépend
EPREUVE_DU_PUBLIC = "tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py"   # `paquets_installes` : ce qu'un pas installe
LUS = (FABRICANT, JETON, TABLE, SOURCE_DU_SOIR, CERTIFICATION_PRIVEE, COPIEUR, EPREUVE_DU_PUBLIC)
# Un nom de programme dans un texte de pas : le motif même de `dependances` (lettres, chiffres, « _ », « - », « .py »).
NOM_DE_PROGRAMME = re.compile(r"[A-Za-z0-9_\-]+\.py\b")
# « python3 -c "code" » (ou 'code') dans un texte de pas : le code en ligne, relevé comme un programme.
CODE_EN_LIGNE = re.compile(r"""(?:^|[\s;&|(`])python3?(?:\.\d+)?\s+(?:-[A-Za-z]+\s+)*-c\s+(["'])(.*?)\1""", re.S)
ACTION = "actions/setup-python@"
# « python » ou « python3 » (ou « python3.11 ») EN TÊTE DE MOT de commande : début de ligne, après une espace, « ; »,
# « & », « | », « ( », « $( » ou « ` » ; suivi d'une espace ou de la fin. « setup-python » ne répond pas (« - » devant).
MOTIF_PYTHON = re.compile(r"(?:^|[\s;&|(`])python3?(?:\.\d+)?(?=\s|$)", re.M)
# « python3 -m X » ou « python -m X » (options avant « -m » permises) dans un texte de pas : le module X est EXÉCUTÉ
# (relecteur neuf du 17-11-2026 à 21h03, N4 : `python3 -m yaml` échappait au relevé).
MODULE_LANCE = re.compile(r"(?:^|[\s;&|(`])python3?(?:\.\d+)?\s+(?:-[A-Za-z]+\s+)*-m\s*([A-Za-z_][\w.]*)")
# LE GARDE DE LA COUPE (superviseur R-759 du 17-11-2026, N1) : ce par quoi un programme Python lance un autre
# interpréteur. Les appels de subprocess dont le programme doit être un littéral qui n'est pas « python* ».
APPELS_DE_SUBPROCESS = {"run", "Popen", "call", "check_call", "check_output", "getoutput", "getstatusoutput"}
# Ce par quoi un programme charge un fichier Python par son CHEMIN (FORME_D_UN_JETON.py dans le fabricant).
CHARGEURS_PAR_CHEMIN = {"spec_from_file_location", "SourceFileLoader"}
FORME_DE_VERSION = re.compile(r"3\.\d+")
# LE CIRCUIT D'ESSAI DE C2 et C3 : il écrit l'action et la version partout SAUF dans une pose réelle.
ESSAI = '''name: essai
on:
  workflow_dispatch:
jobs:
  defaut_python:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: python3 programmes/ETAPE_MUETTE.py {0}
    steps:
      # - uses: actions/setup-python@v5
      #   with:
      #     python-version: "3.11"
      - name: actions/setup-python@v5 python-version 3.11
        run: |
          echo "uses: actions/setup-python@v5"
          echo "python-version: 3.11"
  commande_python:
    runs-on: ubuntu-latest
    steps:
      - name: Lancer
        shell: bash
        run: |
          python3 -B x.py
  sans_python:
    runs-on: ubuntu-latest
    steps:
      - name: Dire python sans le lancer
        shell: bash
        run: echo "le mot setup-python et monpython3 ne lancent rien"
'''


def charger(chemin, nom):
    """Charge un programme comme un module, par son chemin.

    ① RÔLE — Appeler les fonctions du fabricant de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `chemin` (absolu), `nom` (nom du module). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fabricant n'est pas un paquet. ⑨ CE QUI CLOCHE — Le code de tête du fabricant s'exécute (il lit la
    table des épreuves, à côté de lui). ⑩ EFFET — Aucun hors du processus. ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relever(texte):
    """Relève, job par job, si le job lance Python et quelles versions il pose par actions/setup-python.

    ① RÔLE — LE relevé de cette épreuve, calibré par C1 à C3 avant de servir.
    ② CONTEXTE D'APPEL — `tour`, sur chaque circuit fabriqué, sur la fiche de certification du privé et sur ESSAI.
    ③ ENTRÉE — `texte` : le contenu d'un fichier de circuit GitHub (YAML).
    ④ CONDITIONS D'ENTRÉE — Le texte se lit en YAML et porte « jobs: ».
    ⑤ SORTIE — UNE valeur : un dictionnaire job → (lance_python, poses, indice_de_la_premiere_pose) ; `poses` est la
      liste des versions posées (texte, ou None si la pose n'en donne pas) ; l'indice est celui du pas dans le job
      (None sans pose). Lève ValueError si le texte n'a pas de jobs.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le YAML (les commentaires disparaissent : un « # uses: » n'est pas une pose) ; pour chaque job :
      il lance Python si son shell par défaut, le shell d'un pas, ou la commande d'un pas porte « python »/« python3 »
      en tête de mot (MOTIF_PYTHON) ; une pose est un pas dont la clé « uses » commence par actions/setup-python@ (une
      VALEUR de clé, jamais un texte de commande ou un nom), sa version est la clé « python-version » de son « with ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un relevé par motif sur le texte brut prendrait un commentaire ou un « echo » pour une pose (C2) ; le
      YAML ne donne la clé « uses » que des vrais pas.
    ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨ : un programme lancé sans le mot « python » échappe au relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    import yaml
    donnees = yaml.safe_load(texte)
    jobs = donnees.get("jobs") if isinstance(donnees, dict) else None
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("aucun job lu")
    rendu = {}
    for nom, job in jobs.items():
        shells = [str((((job.get("defaults") or {}).get("run") or {}).get("shell")) or "")]
        commandes, poses, premiere = [], [], None
        for i, pas in enumerate(job.get("steps") or []):
            shells.append(str(pas.get("shell") or ""))
            commandes.append(str(pas.get("run") or ""))
            if str(pas.get("uses") or "").startswith(ACTION):
                v = (pas.get("with") or {}).get("python-version")
                poses.append(None if v is None else str(v))
                premiere = i if premiere is None else premiere
        lance = any(MOTIF_PYTHON.search(s) for s in shells + commandes)
        rendu[nom] = (lance, poses, premiere)
    return rendu


def modules_externes(depot, code, dossier):
    """Rend les modules hors bibliothèque standard et hors dépôt qu'un code importe.

    ① RÔLE — La brique du relevé de la propriété ④ : ce qu'un programme (ou un code « python3 -c ») exige d'installé.
    ② CONTEXTE D'APPEL — `besoins_d_un_pas`, une fois par fichier atteint et par code en ligne.
    ③ ENTRÉE — `depot` : la racine · `code` : le texte Python · `dossier` : le dossier du programme (la racine pour un
      code en ligne).
    ④ CONDITIONS D'ENTRÉE — `code` se lit en Python (sinon ast lève SyntaxError, qui remonte).
    ⑤ SORTIE — UNE valeur : l'ensemble des noms de premier niveau (« cryptography » pour
      « from cryptography.hazmat… import AESGCM ») — par exemple {"cryptography"} pour programmes/PROTEGER_LA_PAGE.py.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir l'arbre syntaxique : `import X`, `from X import …` (absolu), et l'appel
      `import_module("X")` ou `__import__("X")` écrit avec un texte littéral ; écarter la bibliothèque standard
      (`sys.stdlib_module_names`) et tout nom dont un fichier « X.py » existe dans le dossier du programme ou à la
      racine (les deux dossiers où `dependances` cherche, pour la même raison : c'est là que l'import le trouve).
    ⑦ UNITÉ — Des noms de modules.
    ⑧ POURQUOI — Un texte explicatif ou une chaîne qui écrit « import yaml » n'importe rien : seul l'arbre dit ce qui
      s'exécute. La bibliothèque standard vient avec Python ; le reste doit être installé.
    ⑨ CE QUI CLOCHE — Un nom composé à l'exécution (`import_module(nom)`) ne se voit pas ; un import dans une branche
      jamais jouée compte (sur-approximation). `sys.stdlib_module_names` est celui du Python qui fait tourner
      l'épreuve, pas celui du soir (3.11) : un module retiré de la bibliothèque standard entre les deux n'est pas vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    noms = set()
    for n in ast.walk(ast.parse(code)):
        if isinstance(n, ast.Import):
            noms |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
            noms.add(n.module.split(".")[0])
        elif (isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant)
              and isinstance(n.args[0].value, str)
              and (getattr(n.func, "attr", None) or getattr(n.func, "id", None)) in ("import_module", "__import__")):
            noms.add(n.args[0].value.split(".")[0])
    return {m for m in noms if m
            and m not in sys.stdlib_module_names
            and not any(os.path.isfile(os.path.join(d, m + ".py")) for d in (dossier, depot))}


def programmes_nommes(depot, texte):
    """Rend les programmes du dépôt qu'un texte de pas nomme (« X.py »), cherchés dans programmes/ puis à la racine.

    ① RÔLE — Les graines du relevé : ce qu'un pas de circuit lance. ② CONTEXTE D'APPEL — `besoins_d_un_pas` ; `tour`,
    pour les commandes de tous les circuits fabriqués. ③ ENTRÉE — `depot`, `texte` (commande et shell d'un pas).
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : un ensemble de chemins relatifs à la racine — par exemple
    {"programmes/ETAPE_MUETTE.py"} pour « python3 _code/programmes/ETAPE_MUETTE.py {0} ». [rend: 1]
    ⑥ TRAITEMENT — Le motif NOM_DE_PROGRAMME ; le premier fichier existant de ce nom, dans programmes/ puis à la racine.
    ⑦ UNITÉ — — ⑧ POURQUOI — Les pas nomment les programmes sous _code/ (le code public posé) ou programmes/ : seul le
    nom compte, c'est le même fichier. ⑨ CE QUI CLOCHE — Un nom composé par le shell (« $n ») ne se voit pas.
    ⑩ EFFET — Lit l'existence de fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    trouves = set()
    for nom in NOM_DE_PROGRAMME.findall(texte):
        for d in ("programmes", ""):
            if os.path.isfile(os.path.join(depot, d, nom)):
                trouves.add(os.path.join(d, nom).replace(os.sep, "/"))
                break
    return trouves


def modules_lances(depot, texte):
    """Rend ce qu'un texte de pas lance par « python3 -m X » : les programmes du dépôt, et les modules à installer.

    ① RÔLE — Relever la forme « -m » (N4 du relecteur neuf du 17-11-2026) pour `besoins_d_un_pas`.
    ② CONTEXTE D'APPEL — `besoins_d_un_pas`, une fois par pas.
    ③ ENTRÉE — `depot` : la racine · `texte` : la commande du pas et son shell effectif.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : l'ensemble des programmes du dépôt lancés (chemins relatifs, à suivre comme des
      graines) ; l'ensemble des modules hors dépôt et hors bibliothèque standard lancés — par exemple, pour
      « python3 -B -m black x » : (set(), {"black"}) ; pour « python3 -m pip install cryptography » : (set(), set()).
      [rend: 2]
    ⑥ TRAITEMENT — Le motif MODULE_LANCE ; pour chaque nom : « pip » est écarté (le Python que pose
      actions/setup-python n'a que pip : décision du superviseur R-759 du 17-11-2026, N4) ; un nom dont le fichier
      existe au dépôt (à la racine ou sous programmes/, « a.b » cherché comme « a/b.py ») est une graine ; sinon sa
      tête (« yaml » pour « yaml.tool ») compte, sauf si elle est de la bibliothèque standard ou un dossier du dépôt.
    ⑦ UNITÉ — Des chemins ; des noms de modules.
    ⑧ POURQUOI — « python3 -m X » exécute X comme « import X » : il doit être installé avant le pas.
    ⑨ CE QUI CLOCHE — Un nom de module composé par le shell (« -m $m ») ne se voit pas. Un nom de paquet du dépôt
      lancé par « -m » (un dossier) est écarté sans être suivi.
    ⑩ EFFET — Lit l'existence de fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    graines, externes = set(), set()
    for nom in MODULE_LANCE.findall(texte):
        tete = nom.split(".")[0]
        if tete == "pip":
            continue
        chemin = nom.replace(".", "/") + ".py"
        fichier = next((c for c in ("programmes/" + chemin, chemin) if os.path.isfile(os.path.join(depot, c))), None)
        if fichier:
            graines.add(fichier)
        elif not (tete in sys.stdlib_module_names
                  or any(os.path.exists(os.path.join(depot, d, tete)) for d in ("programmes", ""))):
            externes.add(tete)
    return graines, externes


def programme_litteral(argument):
    """Rend le programme qu'un appel de subprocess lance, s'il est écrit en littéral ; None sinon.

    ① RÔLE — Brique du garde de `coupe_du_fabricant`. ② CONTEXTE D'APPEL — `coupe_du_fabricant`, une fois par appel
    de subprocess du fabricant. ③ ENTRÉE — le premier argument de l'appel (nœud de l'arbre syntaxique, ou None).
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte du programme, ou None — par exemple « git » pour
    `["git", "-C", public] + list(args)` (fabricant, `pousser`). [rend: 1] ⑥ TRAITEMENT — Descendre à gauche des
    « + » ; une liste ou un tuple dont le premier élément est un texte littéral rend ce texte. ⑦ UNITÉ — —
    ⑧ POURQUOI — Seul un littéral se juge sans exécuter le code. ⑨ CE QUI CLOCHE — Une chaîne seule (shell=True)
    rend None : le garde tombe, à dessein. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    while isinstance(argument, ast.BinOp) and isinstance(argument.op, ast.Add):
        argument = argument.left
    if (isinstance(argument, (ast.List, ast.Tuple)) and argument.elts and isinstance(argument.elts[0], ast.Constant)
            and isinstance(argument.elts[0].value, str)):
        return argument.elts[0].value
    return None


def coupe_du_fabricant(racine, commandes):
    """Rend la coupe du fabricant (ce qui n'est pas suivi depuis lui), et ce qui l'a réduite ou supprimée.

    ① RÔLE — Écarter du relevé de la propriété ④ les programmes que le fabricant NOMME dans les commandes qu'il écrit
      sans les exécuter lui-même, et rien d'autre (superviseur R-759 du 17-11-2026, « RUSTINE, À REPRENDRE », N1).
    ② CONTEXTE D'APPEL — `tour`, une fois par racine, avant le relevé du soir.
    ③ ENTRÉE — `racine` · `commandes` : les programmes que nomment les pas de tous les circuits fabriqués.
    ④ CONDITIONS D'ENTRÉE — programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py se lit en Python (sinon SyntaxError remonte).
    ⑤ SORTIE — QUATRE valeurs : la coupe (ensemble de chemins, vide si le garde tombe) ; la liste des raisons du
      garde tombé (vide s'il tient) ; les commandes que le fabricant importe ; celles qu'il charge par chemin.
      [rend: 4]
    ⑥ TRAITEMENT — ① Le GARDE : le fabricant ne lance aucun interpréteur — pas de `sys.executable`, pas de `runpy`,
      pas d'appel `exec` ou `eval`, pas de `os.system`, `os.popen`, `os.exec*`, `os.spawn*`, aucun import de noms de
      `subprocess` ou de `runpy`, et chaque appel `subprocess.run`/`Popen`/`call`/`check_call`/`check_output`/
      `getoutput`/`getstatusoutput` a pour programme un littéral (`programme_litteral`) qui n'est pas « python* »
      ni d'argument `executable=` ; ② les fichiers qu'il IMPORTE (`import`, `from`, `import_module("…")`,
      `__import__("…")`, chaque composant d'un nom pointé cherché comme « X.py ») ; ③ ceux qu'il CHARGE PAR CHEMIN :
      dans chaque fonction qui appelle `spec_from_file_location` ou `SourceFileLoader`, chaque nom « X.py » écrit en
      littéral ou porté par une constante de premier niveau du fabricant (MODULE_DU_JETON = "FORME_D_UN_JETON.py"),
      texte explicatif exclu ; ④ coupe = commandes − importés − chargés, ou vide si le garde est tombé.
    ⑦ UNITÉ — Des chemins relatifs à la racine.
    ⑧ POURQUOI — Le fabricant TOURNE au soir (pas « Le circuit public est-il celui que fabrique le depot prive ? »,
      jobs faut_il_tourner et collecte) : ce qu'il importe ou charge compte pour le soir. Ce qu'il seulement nomme dans
      une commande qu'il écrit ne tourne pas chez lui ; le suivre ferait exiger `coverage` au soir (CERTIFIER_LA_VERSION.py,
      nommé dans le gabarit de la certification). Le garde rend la coupe vérifiable : s'il tombe, la coupe disparaît,
      le faux positif revient et M2 rougit — bruyant. Limite : le garde ne tombe pas sous toutes les formes qui
      lancent un interpréteur (R1, R2 et R3 du relecteur du 17-11-2026, écrits au ⑨ de la fiche de tête) ; quand il ne
      tombe pas alors qu'il le devrait, l'erreur est muette. Réparation de fond prévue : garde en liste positive.
    ⑨ CE QUI CLOCHE — Les ajouts au garde au-delà de la liste du superviseur (`eval`, `os.popen`, `os.exec*`,
      `os.spawn*`, import de noms de subprocess) sont de l'auteur : ils ne peuvent que supprimer la coupe, jamais
      l'élargir. Un chargement par un nom composé à l'exécution (`import_module(nom)`, un chemin bâti hors littéral
      et hors constante) ne se voit pas : la coupe serait alors trop large. Exception propre au fabricant, à valider
      par Jean-Luc.
    ⑩ EFFET — Lit le fabricant et l'existence de fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    with open(os.path.join(racine, FABRICANT), encoding="utf-8") as f:
        arbre = ast.parse(f.read())
    garde, importes, charges = [], set(), set()

    def fichiers(nom):
        return programmes_nommes(racine, " ".join(p + ".py" for p in (nom or "").split(".") if p))

    constantes = {c.id: n.value.value for n in arbre.body if isinstance(n, ast.Assign)
                  and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
                  for c in n.targets if isinstance(c, ast.Name)}
    for n in ast.walk(arbre):
        if isinstance(n, ast.Import):
            for a in n.names:
                importes |= fichiers(a.name)
                if a.name.split(".")[0] == "runpy":
                    garde.append(f"import runpy, ligne {n.lineno}")
        elif isinstance(n, ast.ImportFrom):
            importes |= fichiers(n.module) | set().union(*(fichiers(a.name) for a in n.names))
            if (n.module or "").split(".")[0] in ("runpy", "subprocess"):
                garde.append(f"from {n.module} import …, ligne {n.lineno}")
        elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
            if (n.value.id, n.attr) == ("sys", "executable") or (
                    n.value.id == "os" and (n.attr in ("system", "popen") or n.attr.startswith(("exec", "spawn")))):
                garde.append(f"{n.value.id}.{n.attr}, ligne {n.lineno}")
        elif isinstance(n, ast.Name) and n.id == "runpy":
            garde.append(f"runpy, ligne {n.lineno}")
        elif isinstance(n, ast.Call):
            nom = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if isinstance(n.func, ast.Name) and n.func.id in ("exec", "eval"):
                garde.append(f"{n.func.id}(…), ligne {n.lineno}")
            if (nom in ("import_module", "__import__") and n.args and isinstance(n.args[0], ast.Constant)
                    and isinstance(n.args[0].value, str)):
                importes |= fichiers(n.args[0].value)
            if (isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
                    and n.func.value.id == "subprocess" and n.func.attr in APPELS_DE_SUBPROCESS):
                prog = programme_litteral(n.args[0] if n.args else None)
                if (prog is None or os.path.basename(prog).lower().startswith("python")
                        or any(k.arg == "executable" for k in n.keywords)):
                    garde.append(f"subprocess.{n.func.attr} lance {prog!r}, ligne {n.lineno}")
    for portee in [arbre] + [n for n in ast.walk(arbre) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        corps = ([s for s in portee.body if not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                 if isinstance(portee, ast.Module) else [portee])
        noeuds = [x for c in corps for x in ast.walk(c)]
        if not any(isinstance(x, ast.Call) and (getattr(x.func, "attr", None) or getattr(x.func, "id", None))
                   in CHARGEURS_PAR_CHEMIN for x in noeuds):
            continue
        textes_explicatifs = {id(s.body[0].value) for s in noeuds if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))
                              and s.body and isinstance(s.body[0], ast.Expr) and isinstance(s.body[0].value, ast.Constant)}
        noms = [x.value for x in noeuds if isinstance(x, ast.Constant) and isinstance(x.value, str)
                and id(x) not in textes_explicatifs]
        noms += [constantes[x.id] for x in noeuds if isinstance(x, ast.Name) and x.id in constantes]
        charges |= programmes_nommes(racine, " ".join(noms))
    coupe = set() if garde else set(commandes) - importes - charges
    return coupe, garde, importes & set(commandes), charges & set(commandes)


def besoins_d_un_pas(depot, texte, dependances, coupes):
    """Rend les modules hors bibliothèque standard qu'exécute un pas de circuit, et d'où vient chacun.

    ① RÔLE — Le relevé de la propriété ④, pour UN pas. ② CONTEXTE D'APPEL — `tour` : M0 (dépôt d'essai), M1 et M2
      (chaque pas de chaque job du circuit du soir fabriqué).
    ③ ENTRÉE — `depot` · `texte` : la commande du pas et son shell effectif (celui du pas, sinon celui du job) ·
      `dependances` : la fonction de programmes/COPIER_POUR_LES_BOUCLES.py (chemin → fichiers dont il dépend) ·
      `coupes` : dictionnaire chemin → fichiers à ne pas suivre depuis lui (la coupe du fabricant, ⑨ de la fiche).
    ④ CONDITIONS D'ENTRÉE — Chaque programme atteint et chaque code en ligne se lit en Python (sinon SyntaxError).
    ⑤ SORTIE — UNE valeur : dictionnaire module → ensemble des origines (« programmes/X.py », « python3 -c » ou
      « python3 -m ») — par exemple {"cryptography": {"programmes/PROTEGER_LA_PAGE.py"}} pour le pas du cockpit.
      [rend: 1]
    ⑥ TRAITEMENT — ① graines : les programmes que le texte nomme (`programmes_nommes`) et ceux qu'il lance par
      « python3 -m » (`modules_lances`, qui rend aussi les modules hors dépôt ainsi lancés, origine « python3 -m » ;
      pip écarté) ; ② fermeture : ajouter ce dont
      chaque programme atteint dépend (`dependances`, moins sa coupe) jusqu'à ce que rien ne s'ajoute (le geste de
      `deriver`, qui n'a pas de coupe) ; ③ les modules externes de chaque fichier atteint ; ④ ceux de chaque code
      « python3 -c », moins les noms dont le texte du pas écrit lui-même le fichier « X.py » (le pas « Le garde du code
      mord-il ? » écrit _piege_du_garde.py puis l'importe).
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, propriété ④ : ce qu'un pas exécute doit être installé avant lui.
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨. ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main : chaque fichier n'est lu qu'une fois, le dépôt est fini. [sort: non]
    """
    besoins = {}
    graines, lances = modules_lances(depot, texte)
    for m in lances:
        besoins.setdefault(m, set()).add("python3 -m")
    a_lire, vus = sorted(programmes_nommes(depot, texte) | graines), set()
    while a_lire:
        p = a_lire.pop()
        if p in vus:
            continue
        vus.add(p)
        a_lire.extend(sorted(set(dependances(depot, p)) - set(coupes.get(p, ())) - vus))
        with open(os.path.join(depot, p), encoding="utf-8") as f:
            code = f.read()
        for m in modules_externes(depot, code, os.path.dirname(os.path.join(depot, p))):
            besoins.setdefault(m, set()).add(p)
    for _, code in CODE_EN_LIGNE.findall(texte):
        for m in modules_externes(depot, code, depot):
            if (m + ".py") not in NOM_DE_PROGRAMME.findall(texte):
                besoins.setdefault(m, set()).add("python3 -c")
    return besoins


def normaliser(paquet):
    """Rend le nom pip d'un mot « pip install » sans version ni extra, en minuscules, « _ » et « . » changés en « - ».

    ① RÔLE — Comparer un nom pip à un nom de distribution. ② CONTEXTE D'APPEL — `tour`, M2. ③ ENTRÉE — un mot
    (« numpy==2.2.6 », « PyYAML »). ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le nom (« numpy », « pyyaml »).
    [rend: 1] ⑥ TRAITEMENT — couper au premier « < > = ! ~ [ ; @ » ou espace. ⑦ UNITÉ — — ⑧ POURQUOI — pip compare
    les noms ainsi (PEP 503). ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return re.sub(r"[-_.]+", "-", re.split(r"[<>=!~\[;@\s]", paquet.strip(), maxsplit=1)[0]).lower()


def tour(racine):
    """Joue les cas C, V et P sur une racine ; rend la liste des cas faux, et le relevé.

    ① RÔLE — Un tour complet de l'épreuve. ② CONTEXTE D'APPEL — `main` : la racine telle quelle, puis chaque copie
    sabotée. ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — Les fichiers LUS existent sous `racine`.
    ⑤ SORTIE — DEUX valeurs : la liste des cas faux (textes commençant par le code du cas), les lignes du relevé.
    [rend: 2] ⑥ TRAITEMENT — Fiche en tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Une exception du fabricant est rangée en cas faux « V0 », pas propagée.
    ⑩ EFFET — Aucun hors du processus. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux, lignes = [], []
    # C — le relevé, calibré
    essai = relever(ESSAI)
    if any(poses for _, poses, _ in essai.values()):
        faux.append("C2 le relevé prend pour une pose un commentaire, un nom ou un echo : "
                    + str({k: v[1] for k, v in essai.items()}))
    attendu = {"defaut_python": True, "commande_python": True, "sans_python": False}
    vu = {k: v[0] for k, v in essai.items()}
    if vu != attendu:
        faux.append(f"C3 lance-t-il Python : {vu} au lieu de {attendu}")
    # V — les circuits fabriqués
    try:
        F = charger(os.path.join(racine, FABRICANT), "fabricant_version_python")
        with open(os.path.join(racine, SOURCE_DU_SOIR), encoding="utf-8") as f:
            circuits = F.ce_que_la_publication_ecrit(racine, [], [], F.fabriquer_le_circuit(f.read()))
    except Exception as e:      # noqa: BLE001 — tout échec du fabricant est un cas faux, jamais un silence
        return [f"V0 les circuits n'ont pas pu être fabriqués : {type(e).__name__} : {e}"], lignes
    attendus = {p.replace(os.sep, "/") for p in (F.CIRCUIT_PUBLIC, F.CIRCUIT_CERTIFICATION, F.CIRCUIT_SERIES,
                                                  F.CIRCUIT_RELAIS, F.CIRCUIT_EPREUVES)}
    if {c for c, _ in circuits} != attendus:
        faux.append(f"V0 circuits relevés {sorted(c for c, _ in circuits)} au lieu de {sorted(attendus)}")
    version = getattr(F, "VERSION_DE_PYTHON", None)
    if not isinstance(version, str) or not FORME_DE_VERSION.fullmatch(version):
        faux.append(f"V1 constante VERSION_DE_PYTHON absente ou mal formée : {version!r}")
    for chemin, octets in circuits:
        releve = relever(octets.decode("utf-8"))
        for job, (lance, poses, premiere) in releve.items():
            lignes.append(f"{chemin} · job {job} : " + ("lance Python" if lance else "ne lance pas Python")
                          + " · pose : " + (", ".join(repr(p) for p in poses) if poses else "aucune"))
            if lance and not poses:
                faux.append(f"V2 {chemin} job {job} lance Python sans poser actions/setup-python")
            for p in poses:
                if p != version:
                    faux.append(f"V3 {chemin} job {job} pose {p!r} au lieu de la constante {version!r}")
            if chemin == F.CIRCUIT_PUBLIC.replace(os.sep, "/") and lance and premiere not in (0, None):
                faux.append(f"V4 {chemin} job {job} : la pose est au pas {premiere}, pas en tête")
        if chemin == F.CIRCUIT_CERTIFICATION.replace(os.sep, "/"):
            c = releve.get("certifier")
            if not c or not c[1] or (releve.get("preparer") or (True,))[0]:
                faux.append(f"C1 relevé de la vraie certification : certifier={c}, preparer={releve.get('preparer')}")
    # P — la certification du privé
    with open(os.path.join(racine, CERTIFICATION_PRIVEE), encoding="utf-8") as f:
        prive = relever(f.read())
    poses_privees = [p for _, poses, _ in prive.values() for p in poses]
    lignes.append(f"{CERTIFICATION_PRIVEE} (privé) · poses : {poses_privees}")
    if not poses_privees or any(p != version for p in poses_privees):
        faux.append(f"P1 la certification du privé pose {poses_privees}, la constante vaut {version!r}")
    # M — les modules qu'exécute le soir (propriété ④)
    try:
        _dependances = charger(os.path.join(racine, COPIEUR), "copieur_version_python").dependances
        _lus = {}
        def dependances(depot, chemin):      # la même, retenue : chaque programme n'est lu qu'une fois par dépôt
            if (depot, chemin) not in _lus:
                _lus[(depot, chemin)] = _dependances(depot, chemin)
            return _lus[(depot, chemin)]
        paquets_installes = charger(os.path.join(racine, EPREUVE_DU_PUBLIC), "epreuve_du_public_version_python").paquets_installes
    except Exception as e:      # noqa: BLE001 — un relevé qui n'a pas pu se charger est un cas faux, jamais un silence
        return faux + [f"M0 le relevé des imports n'a pas pu se charger : {type(e).__name__} : {e}"], lignes
    essai = tempfile.mkdtemp(prefix="version_python_m0_")
    try:
        os.makedirs(os.path.join(essai, "programmes"))
        with open(os.path.join(essai, "programmes", "A.py"), "w", encoding="utf-8") as f:
            f.write('"""Exemple : import numpy."""\nimport os, json\nx = "import yaml"\ntry:\n    import requests\n'
                    'except ImportError:\n    requests = None\nfrom B import f\n')
        with open(os.path.join(essai, "programmes", "B.py"), "w", encoding="utf-8") as f:
            f.write('import importlib\n\ndef f():\n    return importlib.import_module("pandas")\n')
        vu = besoins_d_un_pas(essai, 'python3 programmes/A.py\nprintf "" > _piege.py\n'
                                     'python3 -c "import os, _piege; import toml"\n'
                                     'python3 -m pip install --quiet x\npython3 -m json.tool f.json\n'
                                     'python3 -B -m black --check .\n', dependances, {})
    finally:
        shutil.rmtree(essai, ignore_errors=True)
    if set(vu) != {"requests", "pandas", "toml", "black"}:
        faux.append(f"M0 relevé du dépôt d'essai : {sorted(vu)} au lieu de ['black', 'pandas', 'requests', 'toml']")
    soir = dict(circuits).get(F.CIRCUIT_PUBLIC.replace(os.sep, "/"))
    if soir is None:
        return faux + ["M1 le circuit du soir n'est pas parmi les circuits fabriqués"], lignes
    import yaml
    commandes = set()     # tout ce que les circuits fabriqués lancent : le fabricant l'écrit, il ne le lance pas
    for _, octets in circuits:
        for job in (yaml.safe_load(octets.decode("utf-8")).get("jobs") or {}).values():
            for pas in job.get("steps") or []:
                commandes |= programmes_nommes(racine, str(pas.get("run") or "") + " " + str(pas.get("shell") or ""))
    coupe, garde, importes, charges = coupe_du_fabricant(racine, commandes)
    if garde:
        lignes.append(f"GARDE DU FABRICANT TOMBÉ — il peut lancer un interpréteur ({'; '.join(garde)}) : coupe supprimée")
    else:
        lignes.append(f"COUPE DU FABRICANT (garde tenu) : {len(commandes)} commandes − importées {sorted(importes)} − "
                      f"chargées par chemin {sorted(charges)} = {len(coupe)} fichiers non suivis depuis lui")
    coupes = {FABRICANT: coupe}
    import importlib.metadata
    distributions = importlib.metadata.packages_distributions()
    connu = False
    for nom_job, job in (yaml.safe_load(soir.decode("utf-8")).get("jobs") or {}).items():
        defaut = str(((job.get("defaults") or {}).get("run") or {}).get("shell") or "")
        installes = []      # (indice du pas, noms pip normalisés) — un pas sous « if: » n'installe rien (N2)
        ecartes = []        # les pas d'installation disqualifiés par un « if: »
        for i, pas in enumerate(job.get("steps") or []):
            run = str(pas.get("run") or "")
            paquets = {normaliser(p) for p in paquets_installes(run)}
            if paquets and "if" in pas:
                ecartes.append(i)
                paquets = set()
            installes.append((i, paquets))
            if not run:
                continue
            besoins = besoins_d_un_pas(racine, run + "\n" + str(pas.get("shell") or defaut), dependances, coupes)
            for m, origines in sorted(besoins.items()):
                noms_pip = {normaliser(m)} | {normaliser(d) for d in distributions.get(m, ())}
                avant = [j for j, paquets in installes[:-1] if paquets & noms_pip]
                lignes.append(f"BESOIN {F.CIRCUIT_PUBLIC} · job {nom_job} · pas {i} ({pas.get('name')}) : {m} "
                              f"← {', '.join(sorted(origines))} · installé au pas {avant or 'AUCUN'}")
                connu |= m == "cryptography" and "programmes/PROTEGER_LA_PAGE.py" in origines
                if not avant:
                    faux.append(f"M2 {F.CIRCUIT_PUBLIC} job {nom_job} pas {i} ({pas.get('name')}) exécute {m} "
                                f"({', '.join(sorted(origines))}) sans qu'un pas plus tôt du job l'installe"
                                + (f" (pas d'installation sous « if: » écartés : {ecartes})" if ecartes else ""))
    if not connu:
        faux.append("M1 le relevé du soir ne retrouve pas le cas connu : cryptography, importé par "
                    "programmes/PROTEGER_LA_PAGE.py au pas du cockpit")
    return faux, lignes


# Chaque sabotage : la liste des (fichier, texte cible, remplacement), le cas qui DOIT rougir (sa raison), et
# facultativement les textes qui doivent figurer dans la sortie de la copie (ce qui prouve la raison).
SABOTAGES = {
    "SV1_pose_retiree_du_circuit_du_soir": ([(FABRICANT, "lambda m: POSE_DE_PYTHON + CHIFFREMENT_DU_SOIR + CLONAGES",
                                              "lambda m: CHIFFREMENT_DU_SOIR + CLONAGES")], "V2"),
    "SV2_constante_changee_cote_fabricant": ([(FABRICANT, 'VERSION_DE_PYTHON = "3.11"\n', 'VERSION_DE_PYTHON = "3.12"\n')],
                                             "P1"),
    "SV3_version_changee_cote_certification_privee": ([(CERTIFICATION_PRIVEE, 'python-version: "3.11"',
                                                        'python-version: "3.12"')], "P1"),
    "SV4_pose_en_dur_dans_le_depart": ([(FABRICANT, '""" + POSE_DE_PYTHON\n',
                                         '""" + POSE_DE_PYTHON.replace(VERSION_DE_PYTHON, "3.10")\n')], "V3"),
    "SV6_pose_apres_les_clonages_au_soir": ([(FABRICANT, "DECISION_ENTETE + POSE_DE_PYTHON + CLONAGES",
                                              "DECISION_ENTETE + CLONAGES + POSE_DE_PYTHON")], "V4"),
    "SV7_installation_du_chiffrement_retiree_du_soir": ([(FABRICANT,
                                                          "lambda m: POSE_DE_PYTHON + CHIFFREMENT_DU_SOIR + CLONAGES",
                                                          "lambda m: POSE_DE_PYTHON + CLONAGES")], "M2"),
    "SV8_import_yaml_ajoute_a_un_programme_du_soir": ([("programmes/TENIR_L_HISTORIQUE.py",
                                                        "import csv, math, os, sys\n",
                                                        "import csv, math, os, sys\nimport yaml\n")], "M2"),
    "SV9_releve_sans_filtre_de_la_bibliotheque_standard": ([("@SOI", "            and m not in sys.stdlib_module_names\n",
                                                             "            and True\n")], "M0"),
    "SV10_coupe_du_fabricant_retiree": ([("@SOI", "    coupes = {FABRICANT: coupe}\n", "    coupes = {}\n")], "M2",
                                        ("coverage",)),
    # Superviseur R-759 du 17-11-2026, N1 : ce que le fabricant IMPORTE compte pour le soir, la coupe ne l'efface pas.
    "SV11_fabricant_importe_CERTIFIER_LA_VERSION": ([(FABRICANT, '\nif __name__ == "__main__":',
                                                      '\ndef _sabotage_sv11():\n    import CERTIFIER_LA_VERSION  # noqa: F401\n'
                                                      '\n\nif __name__ == "__main__":')], "M2", ("coverage",)),
    # N1, le garde : un fabricant qui lance un interpréteur perd sa coupe (le faux positif coverage revient).
    "SV12_fabricant_lance_un_interpreteur": ([(FABRICANT, '\nif __name__ == "__main__":',
                                               '\ndef _sabotage_sv12():\n    subprocess.run([sys.executable, '
                                               '"programmes/CERTIFIER_LA_VERSION.py"])\n\n\nif __name__ == "__main__":')],
                                             "M2", ("GARDE DU FABRICANT TOMBÉ", "sys.executable", "coverage")),
    # N4 : « python3 -m X » relevé ; sans lui, le module « black » du dépôt d'essai n'est plus vu.
    "SV13_releve_sans_python_m": ([("@SOI", "    graines, lances = modules_lances(depot, texte)\n",
                                    "    graines, lances = set(), set()\n")], "M0", ("black",)),
    # N2 : un pas d'installation sous « if: » n'installe rien.
    "SV14_installation_sous_if_false": ([(FABRICANT, "        id: chiffrement\n        shell: bash\n",
                                          "        id: chiffrement\n        if: ${{ false }}\n        shell: bash\n")],
                                        "M2", ("cryptography", "« if: »")),
    # N3, « même job » : l'installation déplacée dans le job de décision (TS1 de l'épreuve sabotée la laisse verte).
    "SV15_chiffrement_dans_un_autre_job": ([(FABRICANT, "lambda m: POSE_DE_PYTHON + CHIFFREMENT_DU_SOIR + CLONAGES",
                                             "lambda m: POSE_DE_PYTHON + CLONAGES"),
                                            (FABRICANT, "DECISION_ENTETE + POSE_DE_PYTHON + CLONAGES",
                                             "DECISION_ENTETE + POSE_DE_PYTHON + CHIFFREMENT_DU_SOIR + CLONAGES")],
                                           "M2", ("job collecte", "cryptography")),
    # N3, « plus tôt » : l'installation placée juste APRÈS le pas du cockpit (TS2 la laisse verte).
    "SV16_chiffrement_apres_le_cockpit": ([(FABRICANT, "lambda m: POSE_DE_PYTHON + CHIFFREMENT_DU_SOIR + CLONAGES",
                                            "lambda m: POSE_DE_PYTHON + CLONAGES"),
                                           (FABRICANT, '    corps = corps.replace("${{ secrets.TOKEN_PUBLIC }}", '
                                                       '"${{ secrets.JETON_DEPOTS }}")\n',
                                            '    corps = corps.replace("${{ secrets.TOKEN_PUBLIC }}", '
                                            '"${{ secrets.JETON_DEPOTS }}")\n'
                                            '    _i = corps.index("\\n      - ", corps.index("- name: Fabriquer et publier '
                                            'le cockpit en page web")) + 1\n'
                                            '    corps = corps[:_i] + CHIFFREMENT_DU_SOIR + corps[_i:]\n')],
                                          "M2", ("job collecte", "cryptography")),
    "SV5_releve_qui_lit_le_texte": ([("@SOI", '            if str(pas.get("uses") or "").startswith(ACTION):\n',
                                      '            if ACTION in str(pas):\n')], "C2"),
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel (relevé affiché) ; avec --saboter (ou --saboter=SV1,…), un tour sur une copie
      intacte des fichiers lus (elle doit être conforme : sinon un sabotage mordrait pour une autre raison), puis une
      copie par sabotage, le fichier visé écrit saboté. « @SOI » désigne cette épreuve : elle est recopiée sabotée et
      relancée dans un processus neuf sur la copie, borné au délai du lancement SIMPLE de cette épreuve dans
      tests/LANCEMENT_DES_EPREUVES.json (superviseur R-759 du 17-11-2026, P5 ; illisible → code 1). Un sabotage mord
      si la copie rend 1, si sa ligne Z0 porte le cas attendu, et si chacun de ses textes attendus (troisième élément
      facultatif de SABOTAGES) figure dans la sortie de la copie.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête. ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("NON CONFORME — le module yaml (PyYAML) est absent : le relevé n'a pas pu tourner (R-734)")
        return 1
    faux, lignes = tour(DEPOT)
    for ligne in lignes:
        print("RELEVÉ " + ligne)
    print("Z0 fichiers tels quels : " + ("C1 à C3, V0 à V4, P1, M0 à M2 conformes" if not faux else "FAUX " + " | ".join(faux)))
    code = 1 if faux else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        import json
        import subprocess
        # Le délai de chaque copie sabotée est celui du lancement SIMPLE de cette épreuve dans la table des délais
        # (superviseur R-759 du 17-11-2026, P5 : il était écrit en dur, 300 s, sans lien avec la table).
        try:
            with open(os.path.join(DEPOT, TABLE), encoding="utf-8") as f:
                delai = json.load(f)["delais"]["tests/" + os.path.basename(__file__)]["secondes"]
            if isinstance(delai, bool) or not isinstance(delai, (int, float)) or delai <= 0:
                raise ValueError(f"secondes = {delai!r}")
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(f"NON CONFORME — délai des copies sabotées illisible dans {TABLE} ({type(e).__name__} : {e}) : "
                  "les sabotages n'ont pas pu tourner (R-734)")
            return 1
        for nom in ["TEMOIN"] + [n for n in SABOTAGES if not choix or n in choix[0] or n.split("_")[0] in choix[0]]:
            d = tempfile.mkdtemp(prefix="version_python_sab_")
            try:
                # les fichiers lus, plus tous les programmes (programmes/ et la racine) : la propriété ④ les suit
                tous = [f"programmes/{n}" for n in os.listdir(os.path.join(DEPOT, "programmes")) if n.endswith(".py")]
                tous += [n for n in os.listdir(DEPOT) if n.endswith(".py") and os.path.isfile(os.path.join(DEPOT, n))]
                for f in sorted(set(LUS) | set(tous)):
                    os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
                    shutil.copyfile(os.path.join(DEPOT, f), os.path.join(d, f))
                soi = os.path.join(d, "tests", os.path.basename(__file__))
                shutil.copyfile(os.path.abspath(__file__), soi)
                for fichier, a, b in ([] if nom == "TEMOIN" else SABOTAGES[nom][0]):
                    cible = soi if fichier == "@SOI" else os.path.join(d, fichier)
                    t = open(cible, encoding="utf-8").read()
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                        return 2
                    open(cible, "w", encoding="utf-8").write(t.replace(a, b))
                p = subprocess.run([sys.executable, "-B", soi, d], capture_output=True, text=True, timeout=delai)
                ligne = next((l for l in p.stdout.splitlines() if l.startswith("Z0 ")), p.stdout[-300:] + p.stderr[-300:])
            finally:
                shutil.rmtree(d, ignore_errors=True)
            if nom == "TEMOIN":
                ok = p.returncode == 0
                print(f"TÉMOIN copie intacte : {'conforme' if ok else 'NON CONFORME — ' + ligne}")
            else:
                raison, requis = SABOTAGES[nom][1], (SABOTAGES[nom][2] if len(SABOTAGES[nom]) > 2 else ())
                manque = [t for t in requis if t not in p.stdout]
                ok = (p.returncode == 1 and re.search(r"(?:FAUX |\| )" + raison + r" ", ligne) is not None
                      and not manque)
                print(f"{nom} {'mord' if ok else 'NE MORD PAS'} (attendu : {raison}"
                      + (f", avec {list(requis)}" if requis else "") + ")"
                      + (f" — absent de la sortie : {manque}" if manque else "") + f" : {ligne[:400]}")
            code |= 0 if ok else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
