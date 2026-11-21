#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CERTIFIER_LA_VERSION — rejoue toutes les épreuves du dépôt, mesure ce qu'elles examinent, refuse une version qui recule.

① RÔLE — Dire, pour une version du dépôt, si elle est certifiée : chaque épreuve de `tests/`
  (et celles de `programmes/` déclarées dans `tests/LANCEMENT_DES_EPREUVES.json`) est rejouée, avec ses sabotages quand elle en a ;
  pendant ce temps, chaque instruction et chaque embranchement des programmes de
  `programmes/` (sous-dossiers compris) exécutés par au moins une épreuve sont relevés ;
  le résultat est comparé à une référence écrite au dépôt. Une épreuve rouge, une épreuve
  disparue, une ligne, un embranchement ou une fonction qui deviennent non examinés : la
  version n'est pas certifiée.
② CONTEXTE D'APPEL — `.github/workflows/certifier.yml`, à chaque dépôt sur la version
  officielle et sur une version en attente, et chaque soir de bourse. Le Chat le lance
  aussi avant de fusionner une version en attente. À la main :
  python3 programmes/CERTIFIER_LA_VERSION.py <racine du dépôt>
  [--ecrire-la-reference [--accord "<décision de Jean-Luc, datée>"]].
  LA NUIT, DEPUIS LE 30-10-2026, EN TRANCHES (décision de Jean-Luc du 30-10-2026 à 19h02) : le circuit public
  `.github/workflows/certifier_la_version.yml` lance « --tranche i/n » sur n machines en même temps, puis
  « --reunir n » dans une tâche finale qui réunit leurs certificats partiels (voir `main`, ⑥).
③ ENTRÉE — `sys.argv[1]` : la racine d'un clone du dépôt. `--ecrire-la-reference` : écrire
  la référence à partir de la mesure de ce passage. `--accord "…"` : la décision de
  Jean-Luc qui autorise une référence moins bonne que l'actuelle, recopiée dedans.
④ CONDITIONS D'ENTRÉE — Le module `coverage` est installé pour `python3` (version inscrite
  dans le workflow). La racine porte `programmes/`, `tests/`,
  `tests/LANCEMENT_DES_EPREUVES.json`, et, hors écriture de
  la référence, `gouvernance/CERTIFICAT_REFERENCE.json`.
⑤ SORTIE — Un rapport `rapports/CERTIFICAT_DE_LA_VERSION.md` écrit dans la racine, une ligne
  de verdict sur la sortie standard, et un code de sortie : 0 = version certifiée ;
  1 = version qui recule ; 2 = la certification n'a pas pu se faire (mesure aveugle ou
  trompée, référence absente, table de lancement illisible, épreuve non déclarée, programme
  présent que la mesure ne sait pas lire, outil manquant) — R-734 : un contrôle
  qui n'a pas pu conclure ne rend jamais 0. Avec `--ecrire-la-reference`, aussi
  `gouvernance/CERTIFICAT_REFERENCE.json`.
⑥ TRAITEMENT — ① copier la racine dans un dossier jetable (les épreuves écrivent) ·
  ② armer la mesure : un Python jetable qui mesure chaque processus, y compris ceux lancés
  avec `python3 -E`, et qui note, à la fin de chaque processus, l'empreinte de chaque
  fichier mesuré · ③ calibrer sur une sonde lancée à deux niveaux de sous-processus, et sur
  un leurre de même nom mais de contenu différent, qui ne doit RIEN faire créditer ·
  ④ lister les épreuves · ⑤ les jouer · ⑥ ne créditer à un programme que les lignes
  exécutées dans une copie identique à l'octet (même empreinte) · ⑦ comparer à la
  référence, ligne par ligne (par le texte de la ligne, pour ne pas dépendre des numéros) ·
  ⑧ écrire le rapport (et la référence si demandé).
⑦ UNITÉ — Des nombres d'instructions, d'embranchements et de fonctions ; des secondes.
⑧ POURQUOI — Décision de Jean-Luc du 01-10-2026, 20h38 : « Chaque ligne, chaque calcul,
  chaque fonction, chaque sous-fonction, chaque traitement, chaque élément de tout le
  circuit d'écosystème doit être vérifié. Tout. Tous les cas. […] toute la mécanique
  interne doit être vérifiée et certifiée à chaque nouvelle version. » ; puis 23h32 « 1 »
  (la règle et ce contrôle automatique) et 23h33 « 1 » (compléter R-731). Mesure du même
  soir : 61,3 % des instructions et 260 fonctions sur 394 exécutées par une épreuve ; le
  détecteur des signaux, à 0 %. Ce programme réalise aussi A-500 (« un jeu de test complet
  qui sera joué tous les jours », Jean-Luc, 29-09-2026) et A-457 (les contrôles à chaque
  dépôt). La relecture indépendante du 01-10-2026 a prouvé cinq façons de reculer sans être
  vu dans la première version — un leurre de même nom, un sous-dossier, un échange de
  lignes à nombres égaux, une épreuve classée « outil » parce qu'un texte la nommait, une
  épreuve disparue : chacune est fermée ici, et éprouvée.
⑨ CE QUI CLOCHE — ① Une instruction exécutée par une épreuve n'est pas pour autant vérifiée :
  seule l'épreuve dit si le résultat est juste. Une épreuve dont on retire les contrôles
  reste verte et continue d'exécuter les mêmes lignes : ce programme ne le voit pas (action
  au BACKLOG : éprouver les épreuves en injectant des pannes dans les programmes). ② Les cas
  de données (valeurs extrêmes, jour férié) ne se mesurent pas en lignes. ③ Les chiffres de
  référence figés (R-701, le golden) ne sont pas rejoués ici. ④ Des épreuves lisent les
  données du jour ou l'horloge : la part examinée peut bouger sans que le code change.
  C'est pourquoi un recul de mesure SANS changement du code (programmes/ et tests/
  identiques à la référence) est dit « dérive de mesure » et ne rougit pas ; les épreuves
  rouges, elles, rougissent toujours. ⑤ La référence est écrite là où le certificateur
  tourne quand on la demande ; GitHub et la machine du Chat peuvent mesurer différemment :
  la dérive ④ couvre le cas où le code est identique, pas les suivants. ⑥ Deux lignes de
  même texte dans un même programme se comptent ensemble : déplacer l'examen de l'une à
  l'autre n'est pas vu. ⑦ Les lectures d'une épreuve sont notées par l'événement d'audit
  « open », qui ne porte pas le dossier ouvert (dir_fd) : un fichier ouvert par
  `os.open(nom, dir_fd=…)` est noté au mauvais endroit (superviseur R-759 du 25-10-2026 ;
  shutil.rmtree n'ouvre ainsi que des dossiers, que la liste des lus écarte). ⑧ « La
  mesure ne fait aucun geste que le processus mesuré peut voir » vaut pour un processus
  qui REMPLACE des fonctions (open, os.open…) ; un crochet d'audit du processus mesuré
  (sys.addaudithook) voit encore l'ouverture du manifeste et les lectures d'empreinte :
  un événement d'audit ne se contourne pas (relecture de Cowork du 26-10-2026, P1 ; seul
  programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py pose un tel crochet, et il ne
  réagit qu'au code exécuté et aux .pyc).
⑩ EFFET — Écrit dans un dossier jetable, puis `rapports/CERTIFICAT_DE_LA_VERSION.md` dans la
  racine, et `gouvernance/CERTIFICAT_REFERENCE.json` sur demande. Ne modifie aucun autre
  fichier de la racine.
⑪ TERMINAISON — Sort par sys.exit, en 0, 1 ou 2. Chaque épreuve est bornée à
  `DUREE_MAX_EPREUVE` secondes, ou au délai que la table de lancement lui déclare
  (« delais », depuis le 16-10-2026) : une épreuve qui ne revient pas est arrêtée et comptée
  rouge. Une série de sabotages déclarée « series_hors_de_la_nuit » n'est pas jouée : son
  relevé est vérifié (`verifier_une_serie`, décision de Jean-Luc du 16-10-2026 à 14h30).
  [sort: oui]
⑫ DÉFINITIONS
  une épreuve : un programme qui fait tourner un programme du système sur un cas dont la
    bonne réponse est connue, sur une copie, et rend 0 s'il la retrouve.
  un sabotage : une panne provoquée exprès dans une copie, que l'épreuve doit dénoncer.
  examiné : exécuté au moins une fois pendant les épreuves, dans une copie identique au
    programme à l'octet.
  la référence : `gouvernance/CERTIFICAT_REFERENCE.json`.
  l'empreinte du code : le sha256 de tous les fichiers de `programmes/` et de `tests/`.
"""
import ast
import collections
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import tokenize
from datetime import datetime
from zoneinfo import ZoneInfo

DUREE_MAX_EPREUVE = 1500       # secondes, par lancement d'épreuve
# LES ÉPREUVES TOURNENT SANS LA CONFIGURATION GIT DE LA MACHINE (signature des commits, identité, …) : une épreuve ne
# dépend que du dépôt. Défini ici, une fois, et lu par `jouer` ET par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py
# (R-708 : deux définitions d'une même chose divergent toujours). Cassure N de Cowork, 17-10-2026 : le joueur de séries
# ne le faisait pas, et 14 sabotages de la boucle de check ont « mordu » parce qu'un `git commit` du montage était
# refusé — un plantage compté comme une morsure. Les fichiers de configuration (GLOBAL, NOSYSTEM) ET les réglages passés
# par l'environnement (COUNT, PARAMETERS) : relecture indépendante du même jour, tour 11 — « GIT_CONFIG_COUNT=1
# GIT_CONFIG_KEY_0=commit.gpgsign » faisait encore refuser un commit, et cette machine en porte trois.
SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                                           "GIT_CONFIG_COUNT": "0", "GIT_CONFIG_PARAMETERS": ""}
REFERENCE = "gouvernance/CERTIFICAT_REFERENCE.json"
RAPPORT = "rapports/CERTIFICAT_DE_LA_VERSION.md"
LANCEMENT = "tests/LANCEMENT_DES_EPREUVES.json"   # comment lancer les épreuves rangées dans programmes/
SEP = os.sep + "programmes" + os.sep

# LE MODULE CHARGÉ AU DÉMARRAGE DE CHAQUE PROCESSUS DU PYTHON JETABLE. Il démarre la mesure si la variable
# COVERAGE_PROCESS_START existe, et, à la fin du processus — AVANT que l'épreuve qui l'a lancé n'efface sa copie —
# note l'empreinte de chaque fichier de programmes/ qu'il a mesuré. Sans ces empreintes, un fichier de même nom mais de
# contenu différent ferait créditer le vrai programme (relecture du 01-10-2026, attaque « leurre »).
MODULE_DE_MESURE = '''import os, sys
sys.path.append({ici!r})
if os.environ.get("COVERAGE_PROCESS_START"):
    try:
        import coverage, atexit, hashlib, io, json, stat
        coverage.process_startup()
        _avant = {{}}
        # LA MESURE NE FAIT AUCUN GESTE QUE LE PROCESSUS MESURÉ PEUT VOIR (superviseur R-759 du 25-10-2026). ① Elle ouvre
        # ses fichiers par sa propre fonction, prise ICI, avant que l'épreuve ne démarre : une épreuve qui remplace
        # builtins.open pour compter ses écritures comptait celle du manifeste (E17k5 de l'épreuve du cours propre, rouge
        # sous la certification seulement, le 25-10-2026). ② Ses propres lectures ne sont jamais notées comme celles de
        # l'épreuve (`_dans_la_mesure`) : l'empreinte prise avant un effacement, et celle du manifeste, passaient pour
        # des lectures (« 100 fichier(s) lu(s) par l'épreuve sans empreinte » pour l'historique long, le même jour).
        _ouvrir = io.open
        _dans_la_mesure = [False]

        def _noter(chemin, dir_fd=None, une_entree=False):
            # Un fichier mesuré que le processus efface lui-même (shutil.rmtree, os.remove) ne serait plus là à la
            # fin : l'empreinte de chaque programme (.py sous un dossier programmes/) est prise juste AVANT
            # l'effacement (16-10-2026 : l'épreuve de la lecture des cours efface sa copie avant de finir, et
            # LIRE_LES_COURS.py paraissait « jamais examiné »). Aucun appel à coverage ici : appelée pendant
            # qu'il range ses propres fichiers, son API casse sa base (« no such table: meta », mesuré le
            # 16-10-2026).
            # ③ Un chemin relatif à un dossier ouvert (dir_fd : shutil.rmtree efface ainsi chaque entrée) se résout par
            # ce dossier, jamais par le dossier courant ; un LIEN effacé n'efface pas sa cible : rien à noter ; et
            # « os.remove » efface une seule entrée, jamais un dossier (25-10-2026 : le cas H61 de l'historique long
            # efface un lien « etudes », et le vrai dossier etudes/ était parcouru).
            _dans_la_mesure[0] = True
            try:
                nom = os.fsdecode(chemin)
                if dir_fd is not None and not os.path.isabs(nom):
                    nom = os.path.join(os.readlink("/proc/self/fd/%d" % dir_fd), nom)
                if stat.S_ISLNK(os.lstat(nom).st_mode):
                    return
                cible = os.path.realpath(nom)   # coverage nomme ses fichiers par leur chemin réel
                if os.path.isfile(cible):
                    fichiers = [cible]
                elif une_entree:
                    return
                else:
                    fichiers = [os.path.join(r, n) for r, _, ns in os.walk(cible) for n in ns]
                for f in fichiers:
                    if f.endswith(".py") and {sep!r} in f and os.path.isfile(f) and not os.path.islink(f):
                        with _ouvrir(f, "rb") as h:
                            _avant[f] = hashlib.sha256(h.read()).hexdigest()
            except Exception:
                pass
            finally:
                _dans_la_mesure[0] = False

        def _ecoute(evenement, arguments):
            if evenement in ("shutil.rmtree", "os.remove") and arguments and isinstance(arguments[0], (str, bytes, os.PathLike)):
                fd = arguments[1] if len(arguments) > 1 and isinstance(arguments[1], int) and arguments[1] >= 0 else None
                _noter(arguments[0], fd, evenement == "os.remove")

        sys.addaudithook(_ecoute)
        _lectures = os.environ.get("CERTIF_LECTURES")
        if _lectures:
            # Les fichiers OUVERTS EN LECTURE par une épreuve dont la série de sabotages est jouée hors de la nuit
            # (relecture de Cowork du 16-10-2026, cassure M1 : le relevé ne doit pas choisir ce qu'il surveille).
            _lus = _ouvrir(os.path.join(_lectures, "lus.%d.%s" % (os.getpid(), os.urandom(4).hex())), "a", encoding="utf-8")

            def _lu(evenement, arguments):
                if evenement != "open" or not arguments or not isinstance(arguments[0], (str, bytes)) or _dans_la_mesure[0]:
                    return
                mode = arguments[1] if len(arguments) > 1 else "r"
                drapeaux = arguments[2] if len(arguments) > 2 and isinstance(arguments[2], int) else 0
                if (mode is None and drapeaux & 3) or (mode is not None and any(c in str(mode) for c in "wax+")):
                    return
                try:
                    _lus.write(os.path.realpath(os.fsdecode(arguments[0])) + "\\n")
                    _lus.flush()
                except Exception:
                    pass

            sys.addaudithook(_lu)

        def _manifeste():
            _dans_la_mesure[0] = True
            try:
                c = coverage.Coverage.current()
                d = os.environ.get("CERTIF_MANIFESTES")
                if c is None or not d:
                    return
                vus = {{}}
                for f in c.get_data().measured_files():
                    # seuls les fichiers que CE processus a mesurés : un processus qui efface une copie qu'un autre a
                    # exécutée ne doit pas en donner l'empreinte (relecture du 16-10-2026, cassure 2 : un leurre
                    # remis en état puis effacé par le parent était crédité trois fois sur quatre)
                    if {sep!r} in f and os.path.isfile(f):
                        with _ouvrir(f, "rb") as h:
                            vus[f] = hashlib.sha256(h.read()).hexdigest()
                    elif {sep!r} in f and f in _avant:
                        vus[f] = _avant[f]
                with _ouvrir(os.path.join(d, "manifeste.%d.%s.json" % (os.getpid(), os.urandom(4).hex())), "w") as s:
                    json.dump(vus, s)
            except Exception:
                pass
            finally:
                _dans_la_mesure[0] = False

        atexit.register(_manifeste)
    except Exception:
        pass
'''


def empreinte_fichier(chemin):
    """Rend le sha256 d'un fichier.

    ① RÔLE — Dire si deux fichiers sont identiques à l'octet.
    ② CONTEXTE D'APPEL — `lire_la_mesure`, `empreinte_du_code`.
    ③ ENTRÉE — `chemin` : un fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — lire les octets, hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le module de mesure, qui tourne dans un autre processus, fait le même calcul
      dans `MODULE_DE_MESURE` ; s'ils divergeaient, plus rien ne serait crédité et le
      calibrage le dirait (« la mesure est aveugle »).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return hashlib.sha256(open(chemin, "rb").read()).hexdigest()


def programmes_de(racine):
    """Rend « chemin relatif → chemin absolu » pour chaque `.py` de `programmes/`, sous-dossiers compris.

    ① RÔLE — Ne laisser aucun programme hors de la mesure.
    ② CONTEXTE D'APPEL — `lire_la_mesure`, `lister_les_epreuves`.
    ③ ENTRÉE — `racine` : une racine de dépôt.
    ④ CONDITIONS D'ENTRÉE — `programmes/` existe.
    ⑤ SORTIE — UNE valeur : le dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — parcours récursif, caches Python exclus.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un programme rangé dans un sous-dossier échappait à la première version
      (relecture du 01-10-2026, attaque « sous-dossier »).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des dossiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    trouves = {}
    for d, sous, fichiers in os.walk(os.path.join(racine, "programmes")):
        sous[:] = sorted(x for x in sous if x != "__pycache__")
        for f in sorted(fichiers):
            if f.endswith(".py"):
                a = os.path.join(d, f)
                trouves[os.path.relpath(a, racine)] = a
    return trouves


def empreinte_du_code(racine):
    """Rend l'empreinte de tous les fichiers de `programmes/` et de `tests/`.

    ① RÔLE — Dire si le code est le même que celui de la référence.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque fichier (chemin relatif trié), son chemin et son sha256, hachés
      ensemble ; caches Python exclus.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Distinguer un recul du code d'une dérive de la mesure (fiche ⑨ ④).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    h = hashlib.sha256()
    for dossier in ("programmes", "tests"):
        for d, sous, fichiers in os.walk(os.path.join(racine, dossier)):
            sous[:] = sorted(x for x in sous if x != "__pycache__")
            for f in sorted(fichiers):
                if f.endswith(".pyc"):
                    continue
                a = os.path.join(d, f)
                h.update(os.path.relpath(a, racine).encode() + b"\0" + empreinte_fichier(a).encode() + b"\n")
    return h.hexdigest()[:16]


def copier(racine, dossier):
    """Copie la racine dans un dossier jetable et rend le chemin de la copie.

    ① RÔLE — Protéger la racine : les épreuves et les programmes écrivent.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : le dépôt · `dossier` : un dossier jetable existant.
    ④ CONDITIONS D'ENTRÉE — La racine est lisible.
    ⑤ SORTIE — UNE valeur : le chemin de la copie (`<dossier>/depot`).
      [rend: 1]
    ⑥ TRAITEMENT — copie récursive, `.git` compris (des épreuves lisent l'historique),
      caches Python exclus, liens gardés comme liens.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui écrirait dans la racine modifierait la version qu'on
      certifie.
    ⑨ CE QUI CLOCHE — Le dépôt pèse une centaine de mégaoctets : la copie demande cette place.
    ⑩ EFFET — Écrit la copie.
    ⑪ TERMINAISON — Rend la main, ou lève si la place manque.
      [sort: non]
    """
    copie = os.path.join(dossier, "depot")
    shutil.copytree(racine, copie, symlinks=True, ignore=shutil.ignore_patterns("__pycache__"))
    return copie


def armer_la_mesure(dossier):
    """Prépare le Python jetable qui mesure chaque processus, et rend son chemin, ses réglages et le dossier des empreintes.

    ① RÔLE — Faire mesurer chaque processus Python lancé pendant les épreuves, y compris
      ceux lancés avec `python3 -E`, et noter l'empreinte de ce qu'ils ont mesuré.
    ② CONTEXTE D'APPEL — `main`, une fois ; `calibrer_la_mesure` réutilise le Python.
    ③ ENTRÉE — `dossier` : le dossier jetable.
    ④ CONDITIONS D'ENTRÉE — `coverage` est importable par ce Python.
    ⑤ SORTIE — TROIS valeurs : le chemin de l'exécutable Python jetable, le fichier de
      réglages de la mesure, le dossier où chaque processus dépose les empreintes.
      [rend: 3]
    ⑥ TRAITEMENT — ① un environnement `venv` qui voit les paquets du système · ② dans son
      dossier de paquets, `MODULE_DE_MESURE` et un `.pth` qui le charge au démarrage ·
      ③ les réglages : mesure par processus, embranchements comptés, seuls les fichiers
      `*/programmes/*` mesurés, AUCUN rapprochement de chemins (le crédit se fait par
      empreinte, dans `lire_la_mesure`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves lancent les programmes dans leurs propres copies, par
      `sys.executable -E` : une mesure qui ne suit pas ces processus voit 1,9 % du code au
      lieu de 61,3 % (mesure du Chat, 01-10-2026, premier essai).
    ⑨ CE QUI CLOCHE — ① Un programme lancé par un autre Python que `sys.executable` peut
      échapper à la mesure : la part non examinée l'affichera. ② `coverage` (7.10 et
      après) pose aussi son propre `a1_coverage.pth`, qui démarre la mesure dès que la
      variable existe ; la mesure ne démarre qu'une fois. Ce qui l'arme vraiment est la
      variable : `calibrer_la_mesure` le vérifie à chaque passage.
    ⑩ EFFET — Écrit l'environnement jetable et les réglages.
    ⑪ TERMINAISON — Rend la main, ou lève si `venv` échoue.
      [sort: non]
    """
    import coverage
    env = os.path.join(dossier, "python_mesure")
    subprocess.run([sys.executable, "-m", "venv", "--system-site-packages", env], check=True,
                   capture_output=True, text=True)
    py = os.path.join(env, "bin", "python")
    paquets = subprocess.run([py, "-c", "import site; print(site.getsitepackages()[0])"], check=True,
                             capture_output=True, text=True).stdout.strip()
    ici = os.path.dirname(os.path.dirname(coverage.__file__))
    with open(os.path.join(paquets, "certif_mesure.py"), "w", encoding="utf-8") as f:
        f.write(MODULE_DE_MESURE.format(ici=ici, sep=SEP))
    with open(os.path.join(paquets, "zz_certif_mesure.pth"), "w", encoding="utf-8") as f:
        f.write("import certif_mesure\n")
    mesure = os.path.join(dossier, "mesure")
    manifestes = os.path.join(dossier, "manifestes")
    os.makedirs(mesure, exist_ok=True)
    os.makedirs(manifestes, exist_ok=True)
    reglages = os.path.join(dossier, "mesure.rc")
    with open(reglages, "w", encoding="utf-8") as f:
        f.write(f"[run]\nparallel = True\nbranch = True\ndata_file = {os.path.join(mesure, 'donnees')}\n"
                "include = */programmes/*\n")
    return py, reglages, manifestes


def texte(lignes, n):
    """Rend le texte, débarrassé de ses espaces de bord, de la ligne `n` (comptée à partir de 1), ou « <sortie> ».

    ① RÔLE — Désigner une ligne par ce qu'elle dit, et non par son numéro.
    ② CONTEXTE D'APPEL — `lire_la_mesure`.
    ③ ENTRÉE — `lignes` : les lignes du fichier · `n` : un numéro, négatif pour une sortie de
      fonction (convention de `coverage`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un ajout de ligne décale tous les numéros qui suivent ; le texte, non.
    ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨ ⑥.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return lignes[n - 1].strip() if 0 < n <= len(lignes) else "<sortie>"


def mesure_brute(dossier, reglages, manifestes, racine):
    """Réunit les relevés, ne crédite que les copies identiques, et rend, par programme, ce qui n'est pas examiné, par numéros.

    ① RÔLE — Transformer les relevés bruts en ce qui a été examiné, programme par programme.
    ② CONTEXTE D'APPEL — `lire_la_mesure` ; `main`, pour le certificat partiel d'une tranche de la nuit.
    ③ ENTRÉE — `dossier` : où écrire les fichiers de travail · `reglages` · `manifestes` :
      le dossier des empreintes · `racine` : la copie dont on mesure les programmes.
    ④ CONDITIONS D'ENTRÉE — Les épreuves ont tourné.
    ⑤ SORTIE — UNE valeur : « chemin relatif → {empreinte, instructions, embranchements, fonctions,
      fonctions_non_examinees, lignes, branches} » ; `lignes` : les numéros des lignes non examinées ;
      `branches` : les couples [départ, arrivée] non examinés ; `empreinte` : le sha256 du programme mesuré.
      [rend: 1]
    ⑥ TRAITEMENT — ① réunir les relevés · ② lire les empreintes notées par chaque processus ·
      ③ pour chaque fichier mesuré, retrouver le programme de même chemin relatif sous
      `programmes/`, et ne créditer ses lignes et embranchements QUE si l'empreinte est la
      même · ④ faire calculer par `coverage` le rapport de chaque programme sur les seuls
      crédits · ⑤ garder les numéros (la traduction en textes est faite par `tableau_de`).
    ⑦ UNITÉ — Des numéros de lignes.
    ⑧ POURQUOI — Voir la fiche en tête, ⑧ (le leurre) et ⑨ ⑥. Les numéros, et non les textes : deux tranches de
      la nuit se réunissent ligne à ligne (`reunir_les_mesures`), et deux lignes de même texte se confondraient.
    ⑨ CE QUI CLOCHE — Une copie modifiée par un sabotage n'est pas créditée : ce qu'elle
      exécute ne compte pas, et c'est voulu.
    ⑩ EFFET — Écrit des fichiers de travail dans `dossier`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import coverage
    from coverage.data import CoverageData
    subprocess.run([sys.executable, "-m", "coverage", "combine", "--rcfile", reglages, "-q", "--keep"],
                   cwd=dossier, capture_output=True, text=True)
    brut = CoverageData(basename=os.path.join(os.path.dirname(reglages), "mesure", "donnees"))
    if os.path.exists(brut.data_filename()):
        brut.read()
    toutes = collections.defaultdict(set)
    for f in os.listdir(manifestes):
        try:
            for chemin, e in json.load(open(os.path.join(manifestes, f), encoding="utf-8")).items():
                toutes[chemin].add(e)
        except (ValueError, OSError, AttributeError):
            pass
    # Un chemin qui a porté deux contenus différents (une copie sabotée puis remise en état au même endroit) n'est
    # crédité à rien : la mesure réunit les lignes de tous les processus par chemin, et ne sait plus lesquelles
    # viennent de quel contenu (relecture du 16-10-2026, cassure 2 ; le défaut existait avant le crochet).
    vus = {chemin: next(iter(e)) for chemin, e in toutes.items() if len(e) == 1}
    reels = programmes_de(racine)
    empreintes = {rel: empreinte_fichier(a) for rel, a in reels.items()}
    arcs, lignes = collections.defaultdict(set), collections.defaultdict(set)
    for f in brut.measured_files():
        i = f.rfind(SEP)
        rel = f[i + 1:] if i >= 0 else None
        if rel not in reels or vus.get(f) != empreintes[rel]:
            continue
        if brut.has_arcs():
            arcs[reels[rel]] |= set(brut.arcs(f) or [])
        else:
            lignes[reels[rel]] |= set(brut.lines(f) or [])
    credit = CoverageData(basename=os.path.join(dossier, "credit"))
    if lignes:
        credit.add_lines({k: list(v) for k, v in lignes.items()})
    else:
        credit.add_arcs({k: list(v) for k, v in arcs.items()})
    credit.write()
    cov = coverage.Coverage(data_file=os.path.join(dossier, "credit"), branch=True)
    cov.load()
    sortie = os.path.join(dossier, "mesure.json")
    cov.json_report(morfs=list(reels.values()), outfile=sortie, ignore_errors=True)
    rapport = json.load(open(sortie, encoding="utf-8"))["files"]
    par_chemin = {os.path.abspath(k): v for k, v in rapport.items()}
    brute = {}
    for rel, a in reels.items():
        v = par_chemin.get(os.path.abspath(a))
        if v is None:
            continue
        s = v["summary"]
        fonctions = {k: x for k, x in v.get("functions", {}).items() if k}
        brute[rel] = {"empreinte": empreintes[rel], "instructions": s["num_statements"],
                      "embranchements": s.get("num_branches", 0), "fonctions": len(fonctions),
                      "fonctions_non_examinees": sorted(k for k, x in fonctions.items()
                                                        if x["summary"]["covered_lines"] == 0),
                      "lignes": sorted(v.get("missing_lines", [])),
                      "branches": sorted([d, b] for d, b in v.get("missing_branches", []))}
    return brute


def tableau_de(brute, racine):
    """Traduit une mesure brute (numéros de lignes) en tableau par programme (textes de lignes), celui que la référence garde.

    ① RÔLE — Désigner ce qui n'est pas examiné par le TEXTE des lignes, pas par leur numéro.
    ② CONTEXTE D'APPEL — `lire_la_mesure` (une tranche, ou la certification entière) ; `main`, après `reunir_les_tranches`.
    ③ ENTRÉE — `brute` : « chemin relatif → mesure brute » (`mesure_brute`) · `racine` : où lire le texte des programmes.
    ④ CONDITIONS D'ENTRÉE — Chaque programme de `brute` existe sous `racine`, avec le contenu mesuré.
    ⑤ SORTIE — UNE valeur : le tableau décrit en ⑤ de `lire_la_mesure`.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque programme : les comptes, et le compte par texte des lignes et des embranchements non examinés.
    ⑦ UNITÉ — Des nombres d'instructions et d'embranchements.
    ⑧ POURQUOI — La nuit découpée en tranches (décision de Jean-Luc du 30-10-2026 à 19h02, « 1 ») réunit des mesures
      faites sur plusieurs machines : la réunion se fait sur les NUMÉROS (un même programme, à l'octet), puis la
      traduction en textes se fait ici, une fois, pour une tranche comme pour la nuit entière (R-708).
    ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨ ⑥.
    ⑩ EFFET — Lit les programmes.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    tableau = {}
    for rel, v in brute.items():
        src = open(os.path.join(racine, rel), encoding="utf-8", errors="replace").read().splitlines()
        tableau[rel] = {
            "instructions": v["instructions"], "instructions_non_examinees": len(v["lignes"]),
            "embranchements": v["embranchements"], "embranchements_non_examines": len(v["branches"]),
            "fonctions": v["fonctions"], "fonctions_non_examinees": sorted(v["fonctions_non_examinees"]),
            "lignes_non_examinees": dict(collections.Counter(texte(src, n) for n in v["lignes"])),
            "branches_non_examinees": dict(collections.Counter(f"{texte(src, d)} → {texte(src, b)}"
                                                               for d, b in v["branches"]))}
    return tableau


def lire_la_mesure(dossier, reglages, manifestes, racine):
    """Rend le tableau par programme de la mesure : `mesure_brute` puis `tableau_de`.

    ① RÔLE — La mesure d'un passage, telle que la référence la garde.
    ② CONTEXTE D'APPEL — `calibrer_la_mesure` et `main`.
    ③ ENTRÉE — `dossier` : où écrire les fichiers de travail · `reglages` · `manifestes` : le dossier des
      empreintes · `racine` : la copie dont on mesure les programmes (les quatre sont passés tels quels à
      `mesure_brute`).
    ④ CONDITIONS D'ENTRÉE — Les épreuves ont tourné.
    ⑤ SORTIE — UNE valeur : « chemin relatif → {instructions, instructions_non_examinees, embranchements,
      embranchements_non_examines, fonctions, fonctions_non_examinees, lignes_non_examinees, branches_non_examinees} ».
      [rend: 1]
    ⑥ TRAITEMENT — les deux appels.
    ⑦ UNITÉ — Des nombres d'instructions et d'embranchements.
    ⑧ POURQUOI — Garder l'appel d'avant le découpage de la nuit (30-10-2026) pour la sonde du calibrage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir `mesure_brute`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return tableau_de(mesure_brute(dossier, reglages, manifestes, racine), racine)


def calibrer_la_mesure(dossier, py):
    """Vérifie que la mesure voit un programme lancé à deux niveaux de `-E`, ou chargé d'une copie effacée avant la fin
    du processus, et qu'un leurre ne fait rien créditer, même effacé.

    ① RÔLE — Prouver, avant de conclure quoi que ce soit, que la mesure n'est ni aveugle ni
      trompée.
    ② CONTEXTE D'APPEL — `main`, avant les épreuves.
    ③ ENTRÉE — `dossier` : le dossier jetable · `py` : le Python jetable.
    ④ CONDITIONS D'ENTRÉE — `armer_la_mesure` a tourné.
    ⑤ SORTIE — DEUX valeurs : vrai si la mesure est juste, et la raison sinon.
      [rend: 2]
    ⑥ TRAITEMENT — ① une sonde `sonde/depot/programmes/SONDE_DE_MESURE.py` à trois
      fonctions ; `appelee` est appelée par un processus `python -E` lancé par un autre ·
      ② une copie identique `sonde/copie/programmes/SONDE_DE_MESURE.py`, d'où un processus
      appelle `appelee_dans_une_copie_effacee` puis efface la copie (shutil.rmtree) avant de
      finir — comme les épreuves qui effacent leur dossier jetable (16-10-2026) · ③ un leurre
      `sonde/leurre/programmes/SONDE_DE_MESURE.py`, de même nom mais au contenu différent, qui
      appelle `jamais_appelee` et s'efface de même · ④ la mesure de la sonde doit dire
      `appelee` et `appelee_dans_une_copie_effacee` examinées, `jamais_appelee` non
      examinée — si le leurre était crédité, `jamais_appelee` le serait.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un motif se calibre sur un cas qui doit sortir et sur un cas qui ne doit pas
      sortir (instructions du projet, § 4) ; une mesure aussi.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit puis efface la sonde, le leurre et leur mesure.
    ⑪ TERMINAISON — Rend la main ; chaque processus est borné à 120 secondes.
      [sort: non]
    """
    sonde = os.path.join(dossier, "sonde")
    for d in ("depot/programmes", "copie/programmes", "leurre/programmes", "mesure", "manifestes"):
        os.makedirs(os.path.join(sonde, d))
    vrai = ("def appelee():\n    return 1\n\n\ndef jamais_appelee():\n    return 2\n\n\n"
            "def appelee_dans_une_copie_effacee():\n    return 3\n")
    open(os.path.join(sonde, "depot", "programmes", "SONDE_DE_MESURE.py"), "w").write(vrai)
    open(os.path.join(sonde, "copie", "programmes", "SONDE_DE_MESURE.py"), "w").write(vrai)
    open(os.path.join(sonde, "leurre", "programmes", "SONDE_DE_MESURE.py"), "w").write(
        vrai + "\n\njamais_appelee()\nappelee()\n")
    reg = os.path.join(sonde, "sonde.rc")
    open(reg, "w").write(f"[run]\nparallel = True\nbranch = True\n"
                         f"data_file = {os.path.join(sonde, 'mesure', 'donnees')}\ninclude = */programmes/*\n")
    env = dict(os.environ, COVERAGE_PROCESS_START=reg, CERTIF_MANIFESTES=os.path.join(sonde, "manifestes"))
    effacer = "; import shutil; shutil.rmtree('programmes')"
    for ou, appel in (("depot", "S.appelee()"), ("copie", "S.appelee_dans_une_copie_effacee()" + effacer),
                      ("leurre", "pass" + effacer)):
        interieur = f"import sys; sys.path.insert(0, 'programmes'); import SONDE_DE_MESURE as S; {appel}"
        exterieur = (f"import subprocess, sys; subprocess.run([sys.executable, '-E', '-c', {interieur!r}], "
                     "check=True, timeout=120)")
        subprocess.run([py, "-E", "-c", exterieur], cwd=os.path.join(sonde, ou), env=env, capture_output=True,
                       text=True, timeout=120)
    vu = lire_la_mesure(sonde, reg, os.path.join(sonde, "manifestes"),
                        os.path.join(sonde, "depot")).get(os.path.join("programmes", "SONDE_DE_MESURE.py"), {})
    shutil.rmtree(sonde, ignore_errors=True)
    if vu.get("fonctions") != 3 or "appelee" in vu.get("fonctions_non_examinees", ["appelee"]):
        return False, "la mesure est aveugle : la sonde lancée par deux sous-processus n'a pas été vue"
    if "appelee_dans_une_copie_effacee" in vu.get("fonctions_non_examinees", []):
        return False, "la mesure est aveugle : une copie identique effacée avant la fin du processus n'a pas été vue"
    if vu.get("fonctions_non_examinees") != ["jamais_appelee"]:
        return False, "la mesure est trompée : un leurre de même nom a fait créditer la sonde"
    return True, ""


MODES_D_EPREUVE = ("epreuves", "--calibrage")


def modes_d_epreuve(chemin):
    """Rend les modes d'épreuve qu'un programme lit sur sa ligne de commande (« epreuves », « --calibrage »).

    ① RÔLE — Reconnaître une épreuve à ce qu'elle fait, et non à son nom : un programme qui
      porte son propre jeu d'épreuves ou son calibrage, lancé par un mot de sa ligne de
      commande, est une épreuve du dépôt.
    ② CONTEXTE D'APPEL — `lister_les_epreuves`, une fois par programme de `programmes/`.
    ③ ENTRÉE — `chemin` : un programme.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des modes trouvés parmi `MODES_D_EPREUVE` (vide si aucun,
      ou si le programme ne se lit pas).
      [rend: 1]
    ⑥ TRAITEMENT — parcourir l'arbre syntaxique ; retenir chaque comparaison (« == » ou « in »)
      dont un côté est l'un des mots de `MODES_D_EPREUVE` et l'autre côté nomme `argv`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 ① écrit qu'un jeu d'épreuves se lance par « python3 LE_PROGRAMME.py
      epreuves ». Le 02-10-2026, quatre programmes portaient un tel mode
      (`CONTROLER_LES_COURS.py` et `PROUVER_L_EXECUTION.py` : `epreuves` ;
      `JUGER_SUR_8_CRITERES.py` et `TENIR_LES_POSITIONS.py` : `--calibrage`), et aucun n'était
      nommé `EPREUVES_*` : un certificateur qui ne cherchait que les noms annonçait « toutes
      les épreuves » sans les jouer — une phrase qui promet plus que le code.
    ⑨ CE QUI CLOCHE — Un mode écrit autrement (un autre mot, un dictionnaire de modes, une
      bibliothèque de lecture des arguments) n'est pas reconnu : la liste des mots est à
      allonger quand un tel mode apparaît.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        arbre = ast.parse(open(chemin, encoding="utf-8").read())
    except (SyntaxError, UnicodeDecodeError, OSError):
        return set()
    trouves = set()
    for n in ast.walk(arbre):
        if not isinstance(n, ast.Compare) or len(n.ops) != 1 or not isinstance(n.ops[0], (ast.Eq, ast.In)):
            continue
        cotes = [n.left, n.comparators[0]]
        mots = {c.value for c in cotes if isinstance(c, ast.Constant) and c.value in MODES_D_EPREUVE}
        if mots and any(isinstance(x, (ast.Name, ast.Attribute)) and getattr(x, "id", getattr(x, "attr", "")) == "argv"
                        for c in cotes for x in ast.walk(c)):
            trouves |= mots
    return trouves


def programmes_illisibles(racine):
    """Rend les programmes de `programmes/` que Python ne sait pas lire, chacun avec sa raison.

    ① RÔLE — Refuser une version dont un programme ne se lit pas comme le circuit le lance : une
      erreur de syntaxe, un octet qui n'est pas de l'UTF-8.
    ② CONTEXTE D'APPEL — `main`, une fois, après la mesure.
    ③ ENTRÉE — `racine` : la copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des « chemin (raison) », vide si tout se lit.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque programme, le lire comme Python lit un script lancé en ligne de
      commande (`tokenize.open` : l'encodage déclaré, sinon de l'UTF-8 strict), puis `compile`.
      Mesuré le 02-10-2026 : un octet non UTF-8 dans un commentaire passe `compile` sur les
      octets et même l'import, mais `python3 programmes/X.py` le refuse — c'est ainsi que le
      circuit lance les programmes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un octet non UTF-8 dans un programme faisait tomber le certificateur sur une
      trace, code 1, sans rapport (relecture de Cowork du 02-10-2026, cas K7). Lire comme Python
      lit un script donne la même réponse à K1 et à K7, avec un rapport.
    ⑨ CE QUI CLOCHE — Un programme lisible mais faux à l'exécution n'est pas vu ici : c'est la
      comparaison à la référence qui le refuse (`comparer`, ③).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    illisibles = []
    for rel, a in programmes_de(racine).items():
        try:
            with tokenize.open(a) as f:     # la lecture d'un script par Python : encodage déclaré, sinon UTF-8 strict
                compile(f.read(), a, "exec", dont_inherit=True)
        except (SyntaxError, ValueError) as e:
            illisibles.append(f"{rel} ({type(e).__name__}: {e})")
    return illisibles


# LES MORCEAUX DE LA NUIT (A-961, décision de Jean-Luc du 21-11-2026 à 13h34, réponse « 1 » à la question N-10 :
# « Faire les deux tout de suite (18 morceaux et grosse épreuve découpée), puis étudier la relance sélective »).
# LE PROBLÈME, MESURÉ : une tranche de la nuit ne doit pas prévoir plus du tiers de ses 330 minutes, soit 6 600 s (N5 de
# tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py). Or `repartir` range une épreuve ENTIÈRE dans une seule tranche,
# et le seul lancement « tests/EPREUVES_DE_LA_LECTURE_DES_COURS_Sam_10-10-2026.py --saboter » a duré 7 663 s à la
# certification de nuit 44852703801 (21-11-2026) : aucun nombre de tranches ne pouvait le faire tenir.
# LA RÉPONSE : une épreuve déclarée dans la table « morceaux_de_la_nuit » de tests/LANCEMENT_DES_EPREUVES.json est
# jouée, pour ses sabotages, en N lancements au lieu d'un. Le morceau i sur N porte « --saboter --morceau=i/N
# --seulement=<codes> » : il rejoue Z0 (le jeu sans sabotage, nécessaire pour dire qu'un sabotage « mord ») puis les
# sabotages dont le RANG, dans l'ordre du dictionnaire SABOTAGES de l'épreuve, vaut i − 1 modulo N. Chaque sabotage
# travaille déjà dans sa propre copie des programmes : les groupes sont indépendants par construction.
# CE QUI PROTÈGE : aucun sabotage n'est perdu ni joué deux fois — N14 de l'épreuve de la nuit découpée recompte, par une
# autre rédaction, les sabotages du fichier et ceux des morceaux, et rougit si les comptes diffèrent. La charge d'un
# morceau n'est jamais écrite à la main (R-728) : `repartir` prend sa durée relevée, sinon la calcule depuis la durée
# relevée du lancement entier (`charge_estimee_du_morceau`). Ce qu'on paie : Z0 est rejoué une fois par morceau.
# LIMITE : le nombre de morceaux est déclaré, pas calculé ; si un morceau dépasse un jour le tiers, N5 rougit, et l'on
# augmente ce nombre dans la table.
MORCEAUX_DE_LA_NUIT = "morceaux_de_la_nuit"       # le nom de la table, dans tests/LANCEMENT_DES_EPREUVES.json
ARGUMENT_DU_MORCEAU = "--morceau="                # « --morceau=i/N » : le nom stable du morceau (clé des durées)
ARGUMENT_DES_SABOTAGES = "--seulement="           # l'option que l'épreuve lit déjà pour ne jouer que ces sabotages


def morceaux_declares(table):
    """Lit, dans la table de lancement, le nombre de morceaux de chaque épreuve jouée en morceaux la nuit.

    ① RÔLE — Dire quelles épreuves voient leurs sabotages découpés, et en combien de morceaux.
    ② CONTEXTE D'APPEL — `lister_les_epreuves` et `options_de_lancement`, une fois chacune.
    ③ ENTRÉE — `table` : le contenu entier de tests/LANCEMENT_DES_EPREUVES.json, déjà lu.
    ④ CONDITIONS D'ENTRÉE — La clé MORCEAUX_DE_LA_NUIT est facultative ; chaque entrée porte « morceaux », un entier
      de 2 à 50, et « pourquoi » ; une épreuve déclarée aussi dans « series_hors_de_la_nuit » est refusée. Sinon
      ValueError (et `main` rend 2).
    ⑤ SORTIE — UNE valeur : {chemin de l'épreuve : nombre de morceaux}, vide si la table n'en déclare aucun.
      [rend: 1]
    ⑥ TRAITEMENT — lecture et contrôle de forme.
    ⑦ UNITÉ — Un nombre de morceaux.
    ⑧ POURQUOI — Commentaire de MORCEAUX_DE_LA_NUIT (A-961). Une série jouée hors de la nuit ne se découpe pas : sa
      vérification lit les fichiers lus par SON lancement normal, dans le même processus (`jouer_les_lancements`).
    ⑨ CE QUI CLOCHE — 50 est une borne de forme, pas une mesure.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    brut = table.get(MORCEAUX_DE_LA_NUIT) or {}
    if not isinstance(brut, dict):
        raise ValueError(f"« {MORCEAUX_DE_LA_NUIT} » n'est pas une table chemin → valeur")
    rendu = {}
    for chemin, e in brut.items():
        n = e.get("morceaux") if isinstance(e, dict) else None
        if not isinstance(n, int) or isinstance(n, bool) or not 2 <= n <= 50 or not (e.get("pourquoi") or "").strip():
            raise ValueError(f"morceaux illisibles pour « {chemin} » : il faut un entier de 2 à 50 et un pourquoi")
        if chemin in (table.get("series_hors_de_la_nuit") or {}):
            raise ValueError(f"« {chemin} » est une série jouée hors de la nuit : elle ne se découpe pas")
        rendu[chemin] = n
    return rendu


def sabotages_declares(texte, chemin):
    """Rend les noms des sabotages d'une épreuve, dans l'ordre de son dictionnaire SABOTAGES, sans Z0.

    ① RÔLE — Connaître les sabotages d'une épreuve sans l'exécuter.
    ② CONTEXTE D'APPEL — `lancements_des_morceaux`, une fois par épreuve déclarée en morceaux.
    ③ ENTRÉE — `texte` : le code de l'épreuve · `chemin` : son chemin, pour le message d'erreur.
    ④ CONDITIONS D'ENTRÉE — Le fichier assigne, au premier niveau, « SABOTAGES = { … } » dont chaque clé est un texte
      écrit tel quel. Sinon ValueError.
    ⑤ SORTIE — UNE valeur : la liste des noms, Z0 exclu.
      [rend: 1]
    ⑥ TRAITEMENT — lecture de l'arbre syntaxique (`ast`), sans rien exécuter.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Importer l'épreuve l'exécuterait : celle de la lecture des cours copie environ 70 Mo à l'import
      (`depot_fige`). Une clé calculée ne se lit pas sans exécuter : elle est refusée, jamais devinée (R-734).
    ⑨ CE QUI CLOCHE — Un sabotage ajouté au dictionnaire après coup (« SABOTAGES[...] = ») n'est pas vu ; N14 de
      l'épreuve de la nuit découpée compte les sabotages par une autre rédaction et le verrait.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    for n in ast.parse(texte, filename=chemin).body:
        if (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id == "SABOTAGES" and isinstance(n.value, ast.Dict)):
            if not all(isinstance(k, ast.Constant) and isinstance(k.value, str) for k in n.value.keys):
                raise ValueError(f"{chemin} : une clé de SABOTAGES n'est pas un texte écrit tel quel")
            return [k.value for k in n.value.keys if k.value != "Z0"]
    raise ValueError(f"{chemin} : aucun dictionnaire « SABOTAGES = {{…}} » au premier niveau")


def lancements_des_morceaux(chemin, texte, nombre):
    """Rend les lancements d'une épreuve dont les sabotages sont joués en `nombre` morceaux.

    ① RÔLE — Couper le lancement « --saboter » d'une épreuve en morceaux qui tiennent chacun dans une tranche.
    ② CONTEXTE D'APPEL — `lister_les_epreuves`, une fois par épreuve déclarée dans MORCEAUX_DE_LA_NUIT.
    ③ ENTRÉE — `chemin` : « tests/<fichier> » · `texte` : son code · `nombre` : de `morceaux_declares`.
    ④ CONDITIONS D'ENTRÉE — Celles de `sabotages_declares` ; chaque code court (le nom jusqu'au premier « _ ») désigne
      exactement un sabotage, et il y a au moins `nombre` sabotages. Sinon ValueError.
    ⑤ SORTIE — UNE valeur : la liste de `nombre` lancements [chemin, « . », [« {copie} », « --saboter »,
      « --morceau=i/N », « --seulement=<codes> »]], i de 1 à N.
      [rend: 1]
    ⑥ TRAITEMENT — le sabotage de rang r (0 pour le premier après Z0) va au morceau (r modulo N) + 1.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de MORCEAUX_DE_LA_NUIT. L'alternance (et non des blocs qui se suivent) mélange les
      sabotages anciens et récents dans chaque morceau : leurs durées s'équilibrent sans mesure. L'épreuve exige déjà
      qu'un code court désigne EXACTEMENT un sabotage (m-a du relecteur du 13-11-2026) : on le vérifie ici, avant la
      nuit, plutôt que de laisser l'épreuve rendre 2.
    ⑨ CE QUI CLOCHE — Ajouter un sabotage au milieu du dictionnaire déplace les suivants d'un morceau à l'autre : sans
      effet sur ce qui est joué, mais les durées relevées d'un morceau changent un peu la nuit suivante.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    noms = sabotages_declares(texte, chemin)
    codes = [n.split("_", 1)[0] for n in noms]
    doubles = sorted({c for c in codes if codes.count(c) != 1})
    if doubles or len(noms) < nombre:
        raise ValueError(f"{chemin} : codes courts en double {doubles} ou moins de {nombre} sabotages ({len(noms)})")
    return [[chemin, ".", ["{copie}", "--saboter", f"{ARGUMENT_DU_MORCEAU}{i}/{nombre}",
                           ARGUMENT_DES_SABOTAGES + ",".join(codes[i - 1::nombre])]]
            for i in range(1, nombre + 1)]


def lister_les_epreuves(copie):
    """Rend la liste des épreuves à jouer, chacune avec son dossier et ses arguments, et les épreuves non déclarées.

    ① RÔLE — Trouver toutes les épreuves sans en oublier une.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `copie` : la copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — `tests/LANCEMENT_DES_EPREUVES.json` existe et se lit, et chaque
      `tests/*.py` est du Python lisible ; une épreuve déclarée en morceaux porte un dictionnaire SABOTAGES
      littéral ; sinon la fonction lève, et `main` rend 2.
    ⑤ SORTIE — DEUX valeurs : la liste des lancements [chemin, dossier, arguments] ; la liste
      des fichiers de `programmes/` qui sont des épreuves — par leur nom, ou par un mode
      d'épreuve lu sur leur ligne de commande (`modes_d_epreuve`) — sans être déclarés.
      [rend: 2]
    ⑥ TRAITEMENT — ① chaque fichier `tests/*.py` qu'aucun autre fichier de `tests/` n'IMPORTE
      (un fichier importé par d'autres est un outil d'épreuve, comme `HORLOGE_D_EPREUVE.py`)
      se lance depuis la racine avec la racine en argument, puis une seconde fois avec
      `--saboter` si son texte l'accepte — ou, si la table la déclare dans « morceaux_de_la_nuit », une fois PAR
      MORCEAU (`lancements_des_morceaux`, commentaire de MORCEAUX_DE_LA_NUIT) · ② les épreuves rangées dans `programmes/` se
      lancent comme la table `tests/LANCEMENT_DES_EPREUVES.json` les déclare · ③ un fichier de `programmes/` nommé
      `EPREUVES_*` ou `TESTS_*`, ou qui lit un mode d'épreuve sur sa ligne de commande, et
      que la table ne déclare pas, est rendu à part.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve oubliée est une partie du système qu'on croit vérifiée. La
      première version classait « outil » un fichier simplement NOMMÉ dans une chaîne d'une
      autre épreuve : un `print` suffisait à en faire disparaître une (relecture du
      01-10-2026). Seul un import compte désormais ; et la référence garde la liste des
      lancements, pour qu'une épreuve disparue soit un recul.
    ⑨ CE QUI CLOCHE — Une épreuve rangée hors de `tests/` sous un autre nom n'est pas trouvée
      ici ; si elle était à la référence, elle compte comme disparue.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    complete = json.load(open(os.path.join(copie, LANCEMENT), encoding="utf-8"))
    table = complete["epreuves"]
    declarees = {chemin: (e["dossier"], tuple(e["arguments"])) for chemin, e in table.items()}
    morceaux = morceaux_declares(complete)
    tests = sorted(f for f in os.listdir(os.path.join(copie, "tests")) if f.endswith(".py"))
    textes = {f: open(os.path.join(copie, "tests", f), encoding="utf-8").read() for f in tests}
    importes = set()
    for f, t in textes.items():
        for n in ast.walk(ast.parse(t, filename="tests/" + f)):
            if isinstance(n, ast.Import):
                importes |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
                importes.add(n.module.split(".")[0])
    lancements = []
    for f in tests:
        if f[:-3] in importes:
            continue
        lancements.append(["tests/" + f, ".", ["{copie}"]])
        if "--saboter" in textes[f] and "tests/" + f in morceaux:
            lancements += lancements_des_morceaux("tests/" + f, textes[f], morceaux["tests/" + f])
        elif "--saboter" in textes[f]:
            lancements.append(["tests/" + f, ".", ["{copie}", "--saboter"]])
    for chemin, (dossier, arguments) in declarees.items():
        lancements.append([chemin, dossier, list(arguments)])
    non_declarees = sorted(rel for rel, a in programmes_de(copie).items() if rel not in declarees
                           and (os.path.basename(rel).startswith(("EPREUVES_", "TESTS_")) or modes_d_epreuve(a)))
    return lancements, non_declarees


def options_de_lancement(copie):
    """Lit, dans la table de lancement, les délais propres à certains lancements et les séries jouées hors de la nuit.

    ① RÔLE — Dire quels lancements ont un délai à eux, et quelles séries de sabotages ne se rejouent pas la nuit.
    ② CONTEXTE D'APPEL — `main`, une fois, après `lister_les_epreuves`.
    ③ ENTRÉE — `copie` : la copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — `tests/LANCEMENT_DES_EPREUVES.json` se lit ; « delais » et « series_hors_de_la_nuit »
      sont facultatifs. Un délai qui n'est pas un entier de 1 à 21 600 secondes, ou une série sans « releve », lève
      ValueError (et `main` rend 2).
    ⑤ SORTIE — DEUX valeurs : {« chemin arguments » : secondes} (les arguments sans « {copie} », séparés par une
      espace) ; {chemin de l'épreuve : {« releve » : motif du relevé, relatif à la racine, « essais » : nombre
      d'essais de la série refaits chaque nuit, « portee » : la portée du relevé écrite à la table
      (« portee_du_releve »), ou None si elle n'y est pas}}.
      [rend: 2]
    ⑥ TRAITEMENT — json ; contrôle de forme ; chaque morceau d'une épreuve déclarée dans MORCEAUX_DE_LA_NUIT reçoit
      le délai déclaré de son lancement entier (« <chemin> --saboter »), s'il n'en a pas à lui. La VALEUR de la portée n'est pas contrôlée ici : programmes/
      SERIES_DE_SABOTAGES.py, qui seul connaît les portées (`PORTEES`), refuse une portée inconnue (code 2, la nuit
      même).
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 14h30 : la série des 167 sabotages de l'épreuve des 20 ans
      (environ 6 heures) se rejoue quand son code change, et la nuit vérifie seulement que rien n'a changé ; la
      série de la lecture des cours (62 minutes mesurées le 16-10-2026) reçoit un délai à elle. Les deux rougissaient
      au certificat du 16-10-2026 (f5aac6b), arrêtées à 1 500 s. 21 600 s : les six heures d'un passage de GitHub.
      La portée : décision de Jean-Luc du 01-11-2026 à 11h41 (n°71) — la série de l'épreuve d'arrivée des signaux sort
      du soir et ne se rejoue que quand le code de l'épreuve change.
    ⑨ CE QUI CLOCHE — Un délai déclaré pour un lancement qui n'existe plus n'est pas signalé. · Une portée qui n'est
      pas un texte (un nombre…) n'est refusée qu'à la vérification de la série, pas ici.
    ⑩ EFFET — Lit la table.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    table = json.load(open(os.path.join(copie, LANCEMENT), encoding="utf-8"))
    for nom in ("delais", "series_hors_de_la_nuit"):
        if not isinstance(table.get(nom) or {}, dict):
            raise ValueError(f"« {nom} » n'est pas une table nom → valeur")   # relecture du 16-10-2026, cassure 6
    delais = {}
    for cle, e in (table.get("delais") or {}).items():
        sec = e.get("secondes") if isinstance(e, dict) else None
        if not isinstance(sec, int) or isinstance(sec, bool) or not 1 <= sec <= 21600:
            raise ValueError(f"délai illisible pour « {cle} » : {sec!r}")
        delais[cle] = sec
    for chemin, n in morceaux_declares(table).items():
        entier = cle_de(chemin, ["--saboter"])
        for i in range(1, n + 1):
            if entier in delais:
                delais.setdefault(cle_de(chemin, ["--saboter", f"{ARGUMENT_DU_MORCEAU}{i}/{n}"]), delais[entier])
    series = {}
    for chemin, e in (table.get("series_hors_de_la_nuit") or {}).items():
        motif = e.get("releve") if isinstance(e, dict) else None
        if not isinstance(motif, str) or not motif:
            raise ValueError(f"série hors de la nuit sans relevé : {chemin}")
        essais = e.get("essais_refaits_chaque_nuit")
        if not isinstance(essais, int) or isinstance(essais, bool) or not 0 <= essais <= 50:
            raise ValueError(f"série hors de la nuit sans nombre d'essais refaits (0 à 50) : {chemin}")
        series[chemin] = {"releve": motif, "essais": essais, "portee": e.get("portee_du_releve")}
    return delais, series


# LA NUIT DÉCOUPÉE EN TRANCHES (décision de Jean-Luc du 30-10-2026 à 19h02, réponse « 1 » : « Couper la nuit en
# plusieurs tâches qui tournent en même temps, chacune avec ses propres 6 heures, plus une tâche finale qui réunit les
# résultats et dit rouge s'il en manque un »). La nuit du 29 au 30-10-2026, la certification, lancée à 01h30:33, a été
# coupée par sa limite de 330 minutes : les lancements de tests/ relevés au journal y totalisent 19 663 s (328 min), et
# les épreuves de programmes/ n'ont pas commencé. Le nombre de tranches est écrit UNE fois, dans
# programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (TRANCHES_DE_LA_NUIT), qui le passe sur la ligne de commande.
JOURNAUX = os.path.join("rapports", "journal_du_circuit")
JOURNAL_DE_CERTIFICATION = r"^circuit_(\d+)_\d+_certifier(?:_tranche_\d+)?\.log$"   # nom écrit par programmes/ETAPE_MUETTE.py
PASSAGES_RETENUS = 3            # les trois derniers passages qui ont joué un lancement : on garde la plus longue durée
PARTIELS = "rapports/certificats_partiels"   # où chaque tranche dépose son certificat partiel (noms fixes)
# LES DURÉES PUBLIÉES (A-968, décision de Jean-Luc du 21-11-2026 à 15h34, réponse « 1 » : « Publier au dépôt public les
# seules durées des épreuves (des chiffres de temps, aucun cours) pour que GitHub juge pour de vrai »). La copie jouée
# sur GitHub exclut rapports/journal_du_circuit (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, SERIES_COPIE) : sans
# journaux, `durees_relevees` rendait {}, chaque lancement comptait pour son délai, et N5 de la nuit découpée voyait
# 20 400 s par tranche (passage GitHub 44906050466). Ce fichier, DÉRIVÉ des journaux par `publier_les_durees`, porte la
# clé de chaque lancement et ses secondes, rien d'autre : `garder_les_durees` refuse tout le reste, à l'écriture comme
# à la lecture. L'unité est dans le nom du fichier et dans celui de la colonne.
DUREES_PUBLIEES = os.path.join("rapports", "durees_des_epreuves_en_secondes.csv")
COLONNES_DES_DUREES = ["cle_du_lancement", "secondes"]
# une clé publiable : un chemin d'épreuve, puis des mots sans espace ni virgule (calibré le 21-11-2026 sur les 216 clés
# des journaux : toutes passent ; « tests/x.py ; cat /etc/passwd » et une ligne de cours ne passent pas)
CLE_PUBLIABLE = r"^(?:tests|programmes)/[A-Za-z0-9_.-]+\.py(?: [A-Za-z0-9_./=-]+)*$"


def ligne_du_journal(chemin, arguments, code, duree):
    """Rend la ligne que la certification écrit pour un lancement, et que `durees_relevees` relit.

    ① RÔLE — Écrire une fois la forme de la ligne d'un lancement (R-708 : l'écrivain et le lecteur ne divergent pas).
    ② CONTEXTE D'APPEL — `main`, une fois par lancement ; `durees_relevees` lit sa forme par `LIGNE_DU_JOURNAL`.
    ③ ENTRÉE — `chemin` : l'épreuve · `arguments` : ses arguments, « {copie} » compris · `code` : son code ·
      `duree` : en secondes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la ligne, sans fin de ligne.
      [rend: 1]
    ⑥ TRAITEMENT — « ␣␣vert␣␣<clé> · code <code> · <durée> s » ou « ␣␣ROUGE␣<clé> · … », la clé étant celle de `cle_de`.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — La durée de chaque lancement se relève dans les journaux des nuits passées pour répartir les
      tranches (`repartir`) : la forme de la ligne est un contrat entre ce programme et lui-même.
    ⑨ CE QUI CLOCHE — Une clé qui contiendrait « · code » se relirait mal ; aucune ne le fait (relevé le 30-10-2026).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return f"  {'vert ' if code == 0 else 'ROUGE'} {cle_de(chemin, arguments)} · code {code} · {duree} s"


LIGNE_DU_JOURNAL = r"^  (?:vert |ROUGE) (.+?) · code -?\d+ · (\d+) s$"


def cle_de(chemin, arguments):
    """Rend la clé d'un lancement : son chemin, puis ses arguments sans « {copie} » ni « --seulement=… », séparés par une espace.

    ① RÔLE — Nommer un lancement de la même façon partout : délais déclarés, journal, répartition.
    ② CONTEXTE D'APPEL — `main`, `ligne_du_journal`, `repartir`.
    ③ ENTRÉE — `chemin` · `arguments`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — joindre, en écartant les arguments qui commencent par ARGUMENT_DES_SABOTAGES.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La forme des clés de « delais » (tests/LANCEMENT_DES_EPREUVES.json, « format_des_options »). La liste
      des sabotages d'un morceau change dès qu'un sabotage est ajouté : dans la clé, elle ferait perdre la durée relevée
      du morceau à chaque ajout. Le morceau se nomme par « --morceau=i/N », stable (A-961).
    ⑨ CE QUI CLOCHE — Deux lancements d'une même épreuve qui ne différeraient QUE par « --seulement=… » auraient la
      même clé ; seuls les morceaux en portent, et chacun a son « --morceau=i/N ».
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return " ".join([chemin] + [a for a in arguments if a != "{copie}" and not a.startswith(ARGUMENT_DES_SABOTAGES)])


def durees_relevees(racine, passage_exclu=""):
    """Rend, pour chaque lancement déjà joué une nuit, sa durée relevée dans les journaux de la certification.

    ① RÔLE — Donner à `repartir` la durée de chaque lancement, MESURÉE et non écrite à la main (R-728).
    ② CONTEXTE D'APPEL — `main`, dans les deux modes qui jouent (entier et tranche : la coupure de `coupure` la lit
      aussi) ; tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py.
    ③ ENTRÉE — `racine` : le dépôt · `passage_exclu` : le numéro du passage en cours (GITHUB_RUN_ID), dont les
      journaux sont écartés.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {clé du lancement : secondes} ; vide si aucun journal ni fichier de durées publiées.
      [rend: 1]
    ⑥ TRAITEMENT — ① s'il n'existe AUCUN journal de certification (aucun fichier de `JOURNAUX` dont le nom répond à
      `JOURNAL_DE_CERTIFICATION`, quel que soit son passage) : rendre `lire_les_durees_publiees` (A-968) · ② sinon,
      chaque fichier de `JOURNAUX` dont le nom répond à `JOURNAL_DE_CERTIFICATION` ; chaque ligne qui
      répond à `LIGNE_DU_JOURNAL` ; par clé, la plus longue durée des `PASSAGES_RETENUS` derniers passages (numéros
      de passage croissants) qui l'ont jouée.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Une propriété, pas une liste : une épreuve nouvelle ou ralentie est prise avec sa vraie durée dès
      qu'une nuit l'a jouée. La plus longue des trois dernières : les durées ont varié du simple au double d'une nuit
      à l'autre (la série de la lecture des cours : 2 730 s, 4 379 s, 5 028 s aux nuits du 23, 24 et 30-10-2026).
      Les journaux du passage en cours sont écartés : une tranche qui démarre après qu'une autre a déposé son
      journal, ou relancée seule, ferait sinon une autre répartition que ses sœurs.
    ⑨ CE QUI CLOCHE — Un lancement ROUGE tombé vite (0 s) est compté pour sa durée réelle, donc trop court : la
      plus longue des trois nuits l'atténue sans l'effacer. Un lancement jamais joué n'a pas de durée ici : `repartir`
      prend alors son délai. Le repli sur les durées publiées (①) rend des durées PÉRIMÉES si le fichier n'a pas été
      refait depuis les dernières nuits : la prévision l'est alors autant (A-968). Le repli se décide sur la présence
      d'un journal, tous passages compris, et non sur ce qui reste après l'exclusion du passage en cours : sinon deux
      tranches sœurs, l'une partie avant et l'autre après le dépôt d'un journal, liraient deux sources différentes.
      Un fichier de durées publiées malformé lève ValueError (`garder_les_durees`) : la certification tombe, en rouge.
    ⑩ EFFET — Lit les journaux, ou le fichier des durées publiées.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import re
    par_cle = collections.defaultdict(list)
    dossier = os.path.join(racine, JOURNAUX)
    noms = sorted(os.listdir(dossier)) if os.path.isdir(dossier) else []
    if not any(re.match(JOURNAL_DE_CERTIFICATION, f) for f in noms):
        return lire_les_durees_publiees(racine)
    for f in noms:
        m = re.match(JOURNAL_DE_CERTIFICATION, f)
        if not m or (passage_exclu and m.group(1) == passage_exclu):
            continue
        t = open(os.path.join(dossier, f), encoding="utf-8", errors="replace").read()
        for l in re.finditer(LIGNE_DU_JOURNAL, t, re.M):
            par_cle[l.group(1).strip()].append((int(m.group(1)), int(l.group(2))))
    rendu = {}
    for cle, v in par_cle.items():
        derniers = sorted({p for p, _ in v})[-PASSAGES_RETENUS:]
        rendu[cle] = max(d for p, d in v if p in derniers)
    return rendu


def garder_les_durees(lignes):
    """Vérifie un tableau de durées publiables et le rend en {clé : secondes} ; lève ValueError sinon.

    ① RÔLE — La garde des durées publiées (A-968) : ne laisser passer que la clé d'un lancement et ses secondes.
    ② CONTEXTE D'APPEL — `publier_les_durees`, AVANT d'écrire ; `lire_les_durees_publiees`, après avoir lu. Une seule
      garde pour l'écrivain et le lecteur (R-708 : deux rédactions d'une même règle divergent toujours).
    ③ ENTRÉE — `lignes` : liste de listes de textes, la première étant l'en-tête.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {clé du lancement : secondes (entier)}.
      [rend: 1]
    ⑥ TRAITEMENT — ① l'en-tête doit valoir exactement `COLONNES_DES_DUREES` · ② chaque ligne suivante a exactement deux
      champs · ③ la clé répond à `CLE_PUBLIABLE` · ④ les secondes ne sont faites que de chiffres (0 à 9) · ⑤ une
      clé ne paraît qu'une fois. Le premier manquement lève ValueError, qui le nomme.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Les journaux de la certification portent aussi les sorties des épreuves, qui peuvent citer des cours ;
      le dépôt public ne doit recevoir que des chiffres de temps (décision de Jean-Luc du 21-11-2026 à 15h34 : « les
      seules durées des épreuves (des chiffres de temps, aucun cours) »). Une garde par PROPRIÉTÉ (deux colonnes, une
      forme de clé, un nombre), jamais par liste de clés connues.
    ⑨ CE QUI CLOCHE — Une clé de la bonne forme peut nommer une épreuve qui n'existe plus : elle est publiée et lue
      sans dommage (`repartir` ne cherche que les clés de ses lancements).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    import re
    if not lignes or list(lignes[0]) != COLONNES_DES_DUREES:
        raise ValueError(f"durées publiées : en-tête {list(lignes[0]) if lignes else None}, attendu {COLONNES_DES_DUREES}")
    rendu = {}
    for n, l in enumerate(lignes[1:], 2):
        if len(l) != 2:
            raise ValueError(f"durées publiées, ligne {n} : {len(l)} champ(s), attendu 2")
        cle, secondes = l
        if not re.match(CLE_PUBLIABLE, cle):
            raise ValueError(f"durées publiées, ligne {n} : clé hors de la forme d'un lancement")
        if not re.fullmatch(r"[0-9]+", secondes):
            raise ValueError(f"durées publiées, ligne {n} : secondes non numériques")
        if cle in rendu:
            raise ValueError(f"durées publiées, ligne {n} : clé en double")
        rendu[cle] = int(secondes)
    return rendu


def lire_les_durees_publiees(racine):
    """Rend les durées publiées du dépôt, {clé : secondes}, vérifiées par `garder_les_durees` ; {} si le fichier manque.

    ① RÔLE — Donner à `durees_relevees` les durées quand les journaux ne sont pas là (la copie jouée sur GitHub).
    ② CONTEXTE D'APPEL — `durees_relevees`, quand aucun journal de certification n'existe ; les épreuves
      tests/EPREUVES_DES_DUREES_PUBLIEES_Sam_21-11-2026.py.
    ③ ENTRÉE — `racine` : le dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {clé du lancement : secondes} ; {} si `DUREES_PUBLIEES` n'existe pas.
      [rend: 1]
    ⑥ TRAITEMENT — lire le CSV (module csv), le passer à `garder_les_durees`.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 15h34 (A-968) : que GitHub juge N5 sur de vraies durées.
      Fichier absent : {} et non une erreur — c'est l'état d'avant A-968, où chaque lancement compte pour son délai.
    ⑨ CE QUI CLOCHE — Des durées périmées font une prévision périmée : rien ici ne dit de quand elles datent.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError (fichier malformé).
      [sort: non]
    """
    import csv
    chemin = os.path.join(racine, DUREES_PUBLIEES)
    if not os.path.isfile(chemin):
        return {}
    with open(chemin, encoding="utf-8", newline="") as f:
        return garder_les_durees([l for l in csv.reader(f)])


def publier_les_durees(racine):
    """Écrit `DUREES_PUBLIEES` à partir des journaux, par `durees_relevees`, et rend le nombre de clés écrites.

    ① RÔLE — Fabriquer le fichier des durées publiables (A-968).
    ② CONTEXTE D'APPEL — `main`, sur « --publier-les-durees », au dépôt privé où vivent les journaux ; les épreuves
      tests/EPREUVES_DES_DUREES_PUBLIEES_Sam_21-11-2026.py.
    ③ ENTRÉE — `racine` : le dépôt.
    ④ CONDITIONS D'ENTRÉE — Au moins un journal de certification sous `JOURNAUX` ; sinon ValueError (refaire le fichier
      à partir de lui-même ne publierait rien de neuf, et le ferait croire).
    ⑤ SORTIE — UNE valeur : le nombre de clés écrites.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier qu'un journal existe · ② `durees_relevees(racine)` (aucune durée recopiée : R-708) ·
      ③ en faire un tableau en-tête + lignes triées par clé · ④ `garder_les_durees` sur ce tableau AVANT d'écrire ·
      ⑤ écrire dans un fichier voisin puis le renommer (jamais de fichier à moitié écrit).
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 15h34, réponse « 1 » : « Publier au dépôt public les seules
      durées des épreuves (des chiffres de temps, aucun cours) pour que GitHub juge pour de vrai ». Jamais les
      journaux eux-mêmes : ils portent aussi les sorties des épreuves.
    ⑨ CE QUI CLOCHE — Rien ne refait ce fichier chaque nuit tant que le circuit ne l'appelle pas (A-968, reste
      ouvert) : entre deux publications, ses durées vieillissent.
    ⑩ EFFET — Écrit `DUREES_PUBLIEES`.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    import csv
    import re
    dossier = os.path.join(racine, JOURNAUX)
    if not any(re.match(JOURNAL_DE_CERTIFICATION, f) for f in (os.listdir(dossier) if os.path.isdir(dossier) else [])):
        raise ValueError(f"aucun journal de certification sous {JOURNAUX} : rien à publier")
    durees = durees_relevees(racine)
    lignes = [list(COLONNES_DES_DUREES)] + [[c, str(durees[c])] for c in sorted(durees)]
    garder_les_durees(lignes)
    chemin = os.path.join(racine, DUREES_PUBLIEES)
    with open(chemin + ".en_cours", "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(lignes)
    os.replace(chemin + ".en_cours", chemin)
    return len(lignes) - 1


def repartir(lancements, durees, delais, nombre):
    """Répartit les lancements en `nombre` tranches de charges voisines, chaque épreuve entière dans une seule.

    ① RÔLE — Dire quelle tranche de la nuit joue quoi.
    ② CONTEXTE D'APPEL — `main`, en mode tranche ; tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py.
    ③ ENTRÉE — `lancements` : de `lister_les_epreuves` · `durees` : de `durees_relevees` · `delais` : de
      `options_de_lancement` · `nombre` : le nombre de tranches.
    ④ CONDITIONS D'ENTRÉE — `nombre` ≥ 1.
    ⑤ SORTIE — DEUX valeurs : la liste des `nombre` tranches (chacune : ses lancements, dans l'ordre de
      `lancements`) ; la liste de leurs charges prévues, en secondes.
      [rend: 2]
    ⑥ TRAITEMENT — ① grouper les lancements par épreuve (son chemin), chaque morceau à part (`unite_de`) · ② la durée
      prévue d'un lancement : sa durée relevée, sinon (morceau) sa part calculée, sinon son délai déclaré, sinon
      `DUREE_MAX_EPREUVE` · ③ ranger les épreuves de la plus longue à la plus
      courte (à égalité : par chemin), chacune dans la tranche la moins chargée (à égalité : la première).
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Une PROPRIÉTÉ, jamais une liste de noms : une épreuve ajoutée est rangée sans qu'on y pense. Une
      épreuve entière dans une seule tranche : la vérification d'une série jouée hors de la nuit lit les fichiers que
      son lancement normal a lus (`fichiers_lus`), dans le même processus ; et une épreuve et sa série se jouent dans
      l'ordre. La plus longue d'abord, dans la moins chargée : la règle de Graham (1969), dont la charge la plus
      forte ne dépasse pas 4/3 de la meilleure possible.
    ⑨ CE QUI CLOCHE — Une épreuve dont la durée dépasse à elle seule la limite d'une tranche ne peut pas être
      coupée : sa série doit passer hors de la nuit (« series_hors_de_la_nuit »), et l'épreuve de la nuit découpée
      le dit en rouge. Des épreuves qui se gênaient en se suivant dans une même copie ne se suivent plus.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    groupes = collections.OrderedDict()
    for l in lancements:
        groupes.setdefault(unite_de(l), []).append(l)

    def prevue(l):
        """Rend la durée prévue d'un lancement d'épreuve, en secondes.

        ① RÔLE — Donner à `repartir` le poids d'un lancement pour équilibrer les tranches.
        ② CONTEXTE D'APPEL — `repartir`, dans le tri des épreuves et dans le cumul des charges.
        ③ ENTRÉE — `l` : un lancement de `lister_les_epreuves` (l[0] : le chemin de l'épreuve, l[2] : ses arguments).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la durée relevée de ce lancement, sinon — pour un morceau dont le lancement entier a
          une durée relevée — sa part calculée (`charge_estimee_du_morceau`), sinon son délai déclaré, sinon
          `DUREE_MAX_EPREUVE`.
          [rend: 1]
        ⑥ TRAITEMENT — ① la clé du lancement (`cle_de`) · ② la chercher dans `durees`, puis dans `delais`.
        ⑦ UNITÉ — Des secondes.
        ⑧ POURQUOI — Voir le ⑥ ② de `repartir` : une durée inconnue compte pour la plus longue permise, jamais pour zéro.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        cle = cle_de(l[0], l[2])
        if cle not in durees and cle_de(l[0], ["--saboter"]) in durees and morceau_de(l):
            return charge_estimee_du_morceau(l, lancements, durees[cle_de(l[0], ["--saboter"])])
        return durees.get(cle, delais.get(cle, DUREE_MAX_EPREUVE))

    unites = sorted(groupes, key=lambda c: (-sum(prevue(l) for l in groupes[c]), c))
    charges, choisies = [0] * nombre, [set() for _ in range(nombre)]
    for c in unites:
        i = min(range(nombre), key=lambda k: (charges[k], k))
        charges[i] += sum(prevue(l) for l in groupes[c])
        choisies[i].add(c)
    return [[l for l in lancements if unite_de(l) in choisies[i]] for i in range(nombre)], charges


def morceau_de(l):
    """Rend « i/N » si le lancement est un morceau (MORCEAUX_DE_LA_NUIT), sinon le texte vide.

    ① RÔLE — Reconnaître un morceau à ses arguments.
    ② CONTEXTE D'APPEL — `unite_de`, `repartir`, `charge_estimee_du_morceau`, `comparer`.
    ③ ENTRÉE — `l` : un lancement [chemin, dossier, arguments].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte après ARGUMENT_DU_MORCEAU, ou « ».
      [rend: 1]
    ⑥ TRAITEMENT — le premier argument qui commence par ARGUMENT_DU_MORCEAU.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule rédaction de la reconnaissance (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return next((a[len(ARGUMENT_DU_MORCEAU):] for a in l[2] if a.startswith(ARGUMENT_DU_MORCEAU)), "")


def unite_de(l):
    """Rend l'unité de rangement d'un lancement dans les tranches : son épreuve, ou son épreuve et son morceau.

    ① RÔLE — Dire ce que `repartir` garde ensemble dans une même tranche.
    ② CONTEXTE D'APPEL — `repartir`, deux fois par lancement.
    ③ ENTRÉE — `l` : un lancement.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de l'épreuve, suivi de « --morceau=i/N » pour un morceau.
      [rend: 1]
    ⑥ TRAITEMENT — joindre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve reste entière dans une tranche (fiche de `repartir`, ⑧), SAUF ses morceaux : chacun est
      rangé à part, c'est tout l'objet de la découpe (A-961). Le lancement normal de l'épreuve reste rangé à part
      lui aussi, sous le seul chemin : aucune série jouée hors de la nuit n'est en morceaux (`morceaux_declares`).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = morceau_de(l)
    return l[0] + (" " + ARGUMENT_DU_MORCEAU + m if m else "")


def charge_estimee_du_morceau(l, lancements, duree_entiere):
    """Rend la charge prévue d'un morceau jamais joué, calculée depuis la durée relevée du lancement entier.

    ① RÔLE — Donner à `repartir` le poids d'un morceau la première nuit, sans l'écrire à la main (R-728).
    ② CONTEXTE D'APPEL — `repartir` (fonction `prevue`), pour un morceau sans durée relevée.
    ③ ENTRÉE — `l` : le morceau · `lancements` : tous, pour compter les sabotages de ses frères · `duree_entiere` :
      la durée relevée de « <chemin> --saboter », en secondes.
    ④ CONDITIONS D'ENTRÉE — `l` est un morceau, et porte ARGUMENT_DES_SABOTAGES.
    ⑤ SORTIE — UNE valeur : un nombre entier de secondes.
      [rend: 1]
    ⑥ TRAITEMENT — k = sabotages du morceau, K = sabotages de tous les morceaux de la même épreuve ; le lancement entier
      jouait Z0 puis K sabotages, le morceau joue Z0 puis k : durée entière × (k + 1) ÷ (K + 1), arrondie au-dessus.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Sans elle, un morceau jamais joué compterait pour son délai (10 800 s, hérité du lancement entier) et
      N5 rougirait à tort la première nuit. Compter Z0 dans chaque morceau rend la somme des morceaux PLUS grande que la
      durée entière : l'estimation pèche par excès, jamais par défaut.
    ⑨ CE QUI CLOCHE — Elle suppose des sabotages de durée égale ; l'alternance des rangs (`lancements_des_morceaux`) le
      rend vraisemblable, rien ne le garantit. Dès qu'une nuit a joué le morceau, sa durée relevée la remplace.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def compte(x):
        """Rend le nombre de sabotages qu'un morceau joue (Z0 non compté).

        ① RÔLE — Compter les codes de « --seulement=… ».
        ② CONTEXTE D'APPEL — `charge_estimee_du_morceau`, pour le morceau et pour chacun de ses frères.
        ③ ENTRÉE — `x` : un lancement.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : un entier, 0 si le lancement ne porte pas ARGUMENT_DES_SABOTAGES.
          [rend: 1]
        ⑥ TRAITEMENT — découper le texte après « = » sur les virgules.
        ⑦ UNITÉ — Des sabotages.
        ⑧ POURQUOI — La part d'un morceau se calcule sur ce qu'il joue vraiment (R-728).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return sum(len(a[len(ARGUMENT_DES_SABOTAGES):].split(",")) for a in x[2] if a.startswith(ARGUMENT_DES_SABOTAGES))
    k = compte(l)
    tous = sum(compte(x) for x in lancements if x[0] == l[0] and morceau_de(x))
    return -(-duree_entiere * (k + 1) // (tous + 1))


def empreinte_de_la_repartition(tranches):
    """Rend l'empreinte d'une répartition, pour que les tranches d'une même nuit prouvent qu'elles ont la même.

    ① RÔLE — Comparer deux répartitions en une chaîne.
    ② CONTEXTE D'APPEL — `main`, en mode tranche et en mode réunion.
    ③ ENTRÉE — `tranches` : la première sortie de `repartir`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — sha256 du JSON trié.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux tranches qui auraient réparti différemment joueraient une épreuve deux fois et en oublieraient
      une autre ; la réunion le refuse (`reunir_les_tranches`).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return hashlib.sha256(json.dumps(tranches, sort_keys=True).encode()).hexdigest()[:16]


def reunir_les_mesures(brutes):
    """Réunit les mesures brutes de plusieurs tranches en une seule, comme si une seule machine avait tout joué.

    ① RÔLE — Une ligne est examinée la nuit si une tranche au moins l'a examinée.
    ② CONTEXTE D'APPEL — `reunir_les_tranches`, une fois.
    ③ ENTRÉE — `brutes` : la liste des mesures brutes (`mesure_brute`), une par tranche.
    ④ CONDITIONS D'ENTRÉE — Toutes viennent du même code (vérifié par `reunir_les_tranches`).
    ⑤ SORTIE — DEUX valeurs : la mesure brute réunie ; la liste des programmes écartés (absents d'une tranche, ou
      mesurés avec deux empreintes différentes).
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque programme présent dans TOUTES les tranches avec la même empreinte : les lignes,
      embranchements et fonctions non examinés sont l'INTERSECTION de ceux des tranches ; les comptes totaux sont ceux
      de la première tranche.
    ⑦ UNITÉ — Des numéros de lignes.
    ⑧ POURQUOI — Ce qui n'est examiné par aucune tranche n'est examiné par personne : l'intersection des non-examinés
      est le complément de l'union des examinés, ce que fait la mesure quand une seule machine joue tout.
    ⑨ CE QUI CLOCHE — Un programme écarté devient « présent sans rapport de mesure » : la certification est
      impossible, jamais devinée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not brutes:
        return {}, []
    reunie, ecartes = {}, []
    for rel in sorted(set().union(*brutes)):
        v = [b.get(rel) for b in brutes]
        if any(x is None for x in v) or len({x["empreinte"] for x in v}) != 1:
            ecartes.append(rel)
            continue
        r = dict(v[0])
        r["lignes"] = sorted(set.intersection(*(set(x["lignes"]) for x in v)))
        r["branches"] = sorted(list(p) for p in set.intersection(*({tuple(p) for p in x["branches"]} for x in v)))
        r["fonctions_non_examinees"] = sorted(set.intersection(*(set(x["fonctions_non_examinees"]) for x in v)))
        reunie[rel] = r
    return reunie, ecartes


def reunir_les_tranches(racine, nombre, passage, empreinte, lancements):
    """Lit les certificats partiels des tranches de la nuit et dit ce qui manque, ou rend leur réunion.

    ① RÔLE — La tâche finale de la nuit : rouge s'il manque une tranche, si une tranche est rouge, ou si les tranches
      n'ont pas joué, à elles toutes, chaque lancement une fois et une seule.
    ② CONTEXTE D'APPEL — `main`, en mode réunion (« --reunir N »), dans le job `reunir` du circuit de certification.
    ③ ENTRÉE — `racine` : le dépôt, où les tranches ont déposé leurs certificats partiels (`PARTIELS`) · `nombre` :
      le nombre de tranches attendu · `passage` : le numéro du passage en cours · `empreinte` : celle du code de
      `racine` · `lancements` : ceux que `lister_les_epreuves` trouve dans `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — QUATRE valeurs : la raison qui rend la certification impossible (texte vide sinon) ; les résultats
      réunis, dans l'ordre de `lancements` ; la mesure brute réunie ; une remarque par tranche (lancements, durée
      mesurée, charge prévue), pour le certificat.
      [rend: 4]
    ⑥ TRAITEMENT — pour chaque tranche de 1 à `nombre` : le fichier existe, se lit, porte ce passage, ce nombre,
      ce numéro de tranche, l'empreinte du code et la même empreinte de répartition que les autres, et ne se dit pas
      impossible · chaque lancement de `lancements` est joué par exactement une tranche, et aucune tranche ne joue un
      lancement inconnu · les mesures sont réunies (`reunir_les_mesures`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 30-10-2026 à 19h02 (voir `JOURNAUX`, plus haut) : « une tâche finale qui
      réunit les résultats et dit rouge s'il en manque un ». Le numéro du passage : un certificat partiel d'une nuit
      précédente reste au dépôt sous le même nom, et ne doit pas passer pour celui de la nuit.
    ⑨ CE QUI CLOCHE — Hors de GitHub, le passage s'appelle « local » : deux certifications locales successives ne se
      distinguent pas par lui (seulement par l'empreinte du code).
    ⑩ EFFET — Lit les certificats partiels.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lus, fautes = [], []
    for i in range(1, nombre + 1):
        f = os.path.join(racine, PARTIELS, f"TRANCHE_{i}.json")
        try:
            p = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError) as e:
            fautes.append(f"tranche {i} : certificat partiel absent ou illisible ({type(e).__name__})")
            continue
        attendu = {"passage": passage, "nombre": nombre, "tranche": i, "empreinte_du_code": empreinte}
        ecarts = [f"{k} {p.get(k)!r} au lieu de {v!r}" for k, v in attendu.items() if p.get(k) != v]
        if ecarts:
            fautes.append(f"tranche {i} : certificat partiel d'un autre passage ou d'un autre code ({'; '.join(ecarts)})")
        elif p.get("impossible"):
            fautes.append(f"tranche {i} : {p['impossible']}")
        else:
            lus.append(p)
    if not fautes and len({p.get("repartition") for p in lus}) != 1:
        fautes.append("les tranches n'ont pas fait la même répartition : " + ", ".join(
            f"tranche {p['tranche']} {p.get('repartition')}" for p in lus))
    if fautes:
        return " · ".join(fautes), [], {}, []
    joues = collections.Counter(json.dumps(l) for p in lus for l in p.get("joues", []))
    attendus = {json.dumps(l) for l in lancements}
    oublies = [json.loads(l) for l in sorted(attendus) if joues[l] == 0]
    doubles = [json.loads(l) for l in sorted(joues) if joues[l] > 1]
    inconnus = [json.loads(l) for l in sorted(joues) if l not in attendus]
    for quoi, liste in (("jamais joué(s)", oublies), ("joué(s) par plusieurs tranches", doubles),
                        ("inconnu(s) du dépôt", inconnus)):
        if liste:
            fautes.append(f"lancement(s) {quoi} : " + ", ".join(cle_de(l[0], l[2]) for l in liste[:5]))
    if fautes:
        return " · ".join(fautes), [], {}, []
    # un résultat partiel : [chemin, dossier, arguments, code, durée, lignes] (écrit par `main`, mode tranche)
    par_lancement = {json.dumps(r[:3]): r for p in lus for r in p.get("resultats", [])}
    resultats = []
    for l in lancements:
        r = par_lancement.get(json.dumps(l))
        if r is None:
            return f"résultat absent pour {cle_de(l[0], l[2])}", [], {}, []
        resultats.append((r[0], r[2], r[3], r[4], r[5]))
    reunie, ecartes = reunir_les_mesures([p.get("mesure", {}) for p in lus])
    notes = [f"tranche {p['tranche']}/{nombre} : {len(p.get('joues', []))} lancement(s), "
             f"{sum(r[4] for r in p.get('resultats', []))} s mesurées, "
             f"{(p.get('charges_prevues_secondes') or [0] * nombre)[p['tranche'] - 1]} s prévues" for p in lus]
    return "", resultats, reunie, notes


def verifier_une_serie(copie, chemin, entree_de_la_serie, lus=None):
    """Remplace, pour une série jouée hors de la nuit, le lancement « --saboter » par la vérification de son relevé.

    ① RÔLE — L'alarme décidée par Jean-Luc le 16-10-2026 : la série n'est pas rejouée ; son relevé doit valoir pour
      les fichiers du jour.
    ② CONTEXTE D'APPEL — `main`, à la place de `jouer`, pour le lancement « --saboter » d'une épreuve déclarée dans
      « series_hors_de_la_nuit ».
    ③ ENTRÉE — `copie` · `chemin` : l'épreuve, relative · `entree_de_la_serie` : son entrée rendue par
      `options_de_lancement`, {« releve » : le motif du relevé (glob), relatif ; « portee » : la portée du relevé ou
      None} · `lus` : l'ensemble des fichiers du dépôt que l'épreuve a lus cette nuit en mode normal (`fichiers_lus`),
      ou None.
    ④ CONDITIONS D'ENTRÉE — `entree_de_la_serie` porte « releve » (contrôlé par `options_de_lancement`).
    ⑤ SORTIE — TROIS valeurs, comme `jouer` : le code (0 le relevé vaut ; 1 un fichier a changé ou la série n'était
      pas conforme ; 2 aucun relevé, plusieurs relevés, relevé illisible, ou portée inconnue), la durée (0), une ligne
      de raison.
      [rend: 3]
    ⑥ TRAITEMENT — un seul fichier doit répondre au motif (une seule version vivante) ;
      programmes/SERIES_DE_SABOTAGES.py, `verifier_la_serie`, avec la portée de la série (décision n°71 du
      01-11-2026 pour la portée « epreuve »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir `options_de_lancement`, ⑧. Le relevé et sa vérification sont écrits une fois (R-708).
    ⑨ CE QUI CLOCHE — Voir programmes/SERIES_DE_SABOTAGES.py, ⑨.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import glob
    motif = entree_de_la_serie["releve"]
    trouves = sorted(glob.glob(os.path.join(copie, motif)))
    if len(trouves) != 1:
        return 2, 0, [f"série hors de la nuit : {len(trouves)} relevé(s) pour {motif}, il en faut un seul"]
    sp = importlib.util.spec_from_file_location("SERIES_DE_SABOTAGES",
                                                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                             "SERIES_DE_SABOTAGES.py"))
    serie = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(serie)
    code, raison = serie.verifier_la_serie(copie, chemin, os.path.relpath(trouves[0], copie).replace(os.sep, "/"), lus,
                                           entree_de_la_serie.get("portee"))
    return code, 0, [raison]


def fichiers_lus(lectures, copie, racine):
    """Rend les fichiers du dépôt qu'une épreuve a ouverts en lecture, d'après les notes de ses processus.

    ① RÔLE — Dire, par la mesure et non par le relevé, ce que l'épreuve d'une série hors de la nuit lit.
    ② CONTEXTE D'APPEL — `main`, après le lancement normal d'une épreuve déclarée « series_hors_de_la_nuit ».
    ③ ENTRÉE — `lectures` : le dossier des notes · `copie` : la copie du dépôt où l'épreuve a tourné · `racine` : le
      dépôt certifié.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins relatifs (« / ») des fichiers ouverts sous la copie, qui existent
      aussi dans le dépôt certifié, hors de .git ; un fichier compilé (__pycache__) est ramené à son .py.
      [rend: 1]
    ⑥ TRAITEMENT — lire chaque note ; garder les chemins sous la copie ; ramener les .pyc ; écarter ce qui n'existe
      pas dans le dépôt certifié (les dossiers jetables de l'épreuve, les fichiers écrits par d'autres épreuves).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture de Cowork du 16-10-2026, cassure M1 : un relevé qui ne porte que trois empreintes passait,
      et une clôture changée dans l'historique long n'imposait plus de rejouer la série. La liste vient désormais de
      ce que l'épreuve lit, chaque nuit.
    ⑨ CE QUI CLOCHE — Un programme lancé hors du Python jetable (un autre interpréteur) n'est pas noté.
    ⑩ EFFET — Lit les notes.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import re
    racine_copie = os.path.realpath(copie) + os.sep
    lus = set()
    for f in os.listdir(lectures):
        try:
            texte = open(os.path.join(lectures, f), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for p in texte.splitlines():
            if not p.startswith(racine_copie):
                continue
            rel = p[len(racine_copie):].replace(os.sep, "/")
            m = re.match(r"^(.*/)?__pycache__/([^/.]+)\.[^/]+\.pyc$", rel)
            if m:
                rel = (m.group(1) or "") + m.group(2) + ".py"
            if not rel.startswith(".git/") and os.path.isfile(os.path.join(racine, rel)):
                lus.add(rel)
    return lus


def refaire_des_essais(copie, py, reglages, manifestes, chemin, motif, nombre, delai):
    """Refait, chaque nuit, quelques essais d'une série jouée hors de la nuit, et les confronte à son relevé.

    ① RÔLE — Prouver que la série a vraiment tourné : un relevé écrit sans la jouer ne peut pas deviner, essai par
      essai, la liste exacte des épreuves qui tombent.
    ② CONTEXTE D'APPEL — `main`, après `verifier_une_serie`, quand le relevé vaut et que la table de lancement
      demande au moins un essai refait (« essais_refaits_chaque_nuit »).
    ③ ENTRÉE — `copie`, `py`, `reglages`, `manifestes` : comme `jouer` · `chemin` : l'épreuve, relative · `motif` : le
      motif de son relevé · `nombre` : combien d'essais refaire · `delai` : en secondes.
    ④ CONDITIONS D'ENTRÉE — Un seul relevé répond au motif (vérifié par `verifier_une_serie`) ; l'épreuve accepte
      « --saboter=S1,S2,… » et écrit pour chaque sabotage une ligne « <nom> mord : [...] ».
    ⑤ SORTIE — TROIS valeurs, comme `jouer` : le code (0 chaque essai refait rend, mot pour mot, la ligne du relevé,
      et l'épreuve rend 0 ; 1 sinon), la durée en secondes, et les lignes qui le disent.
      [rend: 3]
    ⑥ TRAITEMENT — lire les lignes du relevé ; tirer `nombre` sabotages au hasard (`random.SystemRandom`) ; jouer
      l'épreuve avec ces seuls sabotages, sous la mesure ; comparer chaque ligne rendue à celle du relevé.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Relecture de Cowork du 16-10-2026, cassure M2 : « rien ne prouve que la série a été jouée ». Décision
      de Jean-Luc du 16-10-2026 à 18h53 : trois essais par nuit (« 1 » à « 3 essais par nuit (Recommandé) »).
    ⑨ CE QUI CLOCHE — L'épreuve rejoue d'abord ses épreuves normales avant les sabotages choisis : le coût d'une nuit
      est donc ce passage normal plus les essais. · Une sortie qui changerait d'une machine à l'autre pour une raison
      sans rapport (un chemin, une heure) ferait rougir à tort : la ligne fautive est donnée.
    ⑩ EFFET — Lance l'épreuve ; lit le relevé.
    ⑪ TERMINAISON — Rend la main ; l'épreuve est arrêtée à `delai` secondes.
      [sort: non]
    """
    import glob
    import random
    import re
    releve = sorted(glob.glob(os.path.join(copie, motif)))[0]
    attendues = {}
    for l in open(releve, encoding="utf-8", errors="replace").read().splitlines():
        m = re.match(r"^(\S+) (mord|NE MORD PAS|NE S'APPLIQUE PLUS)\b", l)
        if m:
            attendues[m.group(1)] = l
    if not attendues:
        return 1, 0, [f"série de {chemin} : aucun essai lisible au relevé, rien à refaire"]
    choix = random.SystemRandom().sample(sorted(attendues), min(nombre, len(attendues)))
    code, duree, sortie = jouer(copie, py, reglages, manifestes, chemin, ".", ["{copie}", "--saboter=" + ",".join(choix)],
                                delai, None, None)
    rendues = {l.split(" ", 1)[0]: l for l in sortie if re.match(r"^\S+ (mord|NE MORD PAS|NE S'APPLIQUE PLUS)\b", l)}
    ecarts = [n for n in choix if rendues.get(n) != attendues[n]]
    if code != 0 or ecarts:
        return 1, duree, [f"ESSAIS REFAITS NON CONFORMES AU RELEVÉ ({', '.join(choix)}) : code {code}"] + [
            f"{n} relevé « {attendues[n][:80]} » · refait « {(rendues.get(n) or 'absent')[:80]} »" for n in ecarts[:2]]
    return 0, duree, [f"{len(choix)} essai(s) refait(s) cette nuit, identiques au relevé : {', '.join(choix)}"]


def fichiers_de_commandes_de_github():
    """Rend les noms des variables qui désignent les fichiers de commandes de GitHub, lus chez le fabricant.

    ① RÔLE — Donner à `jouer` la liste des variables à retirer de l'environnement d'une épreuve.
    ② CONTEXTE D'APPEL — `jouer`, une fois par lancement.
    ③ ENTRÉE — — (le fabricant est programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, à côté de ce fichier).
    ④ CONDITIONS D'ENTRÉE — Le fabricant est à côté de ce fichier et se charge ; sinon l'exception remonte et la
      certification s'arrête : un lancement ne part jamais avec ces variables par défaut de liste.
    ⑤ SORTIE — UNE valeur : le n-uplet FICHIERS_DE_COMMANDES_DE_GITHUB du fabricant.
      [rend: 1]
    ⑥ TRAITEMENT — charger le fabricant par son chemin (une fois, gardé dans `_COMMANDES_DE_GITHUB`), lire le n-uplet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La liste vit UNE fois, chez le fabricant ; le joueur des séries la lit déjà
      (tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py) : deux écritures d'une même chose divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — Charger le fabricant exécute son module (lecture de la table des séries) : environ un dixième
      de seconde, une fois par passage.
    ⑩ EFFET — Lit et exécute un fichier Python du dépôt.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    global _COMMANDES_DE_GITHUB
    if _COMMANDES_DE_GITHUB is None:
        sp = importlib.util.spec_from_file_location("FABRICANT_DE_LA_CERTIFICATION",
                                                    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                 "FABRIQUER_LE_CIRCUIT_PUBLIC.py"))
        fabricant = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(fabricant)
        _COMMANDES_DE_GITHUB = tuple(fabricant.FICHIERS_DE_COMMANDES_DE_GITHUB)
    return _COMMANDES_DE_GITHUB


_COMMANDES_DE_GITHUB = None


def jouer(copie, py, reglages, manifestes, chemin, dossier, arguments, delai=DUREE_MAX_EPREUVE, lectures=None,
          garder=None):
    """Joue une épreuve sous la mesure et rend son code, sa durée et les lignes de sa sortie.

    ① RÔLE — Un lancement d'épreuve.
    ② CONTEXTE D'APPEL — `main`, une fois par lancement.
    ③ ENTRÉE — `copie` · `py` : le Python jetable · `reglages` · `manifestes` · `chemin` :
      l'épreuve, relative à la copie · `dossier` : le dossier de lancement, relatif à la
      copie · `arguments` : où `{copie}` est remplacé par le chemin de la copie · `delai` : en
      secondes, la coupure rendue par `coupure` (délai déclaré à la table de lancement, « delais », sinon
      `DUREE_MAX_EPREUVE` ; porté à 3 × la durée relevée si c'est plus, ce triple plafonné à
      3 × `DUREE_MAX_EPREUVE`) · `lectures` : un dossier où chaque processus note les fichiers
      qu'il ouvre en lecture, ou None · `garder` : le nombre de dernières lignes de sortie rendues (None, le défaut
      depuis le 15-11-2026 : toutes ; la coupe d'une épreuve VERTE est faite par `lignes_gardees`).
    ④ CONDITIONS D'ENTRÉE — La mesure est armée.
    ⑤ SORTIE — TROIS valeurs : le code de sortie (124 si l'épreuve a dépassé son délai), la
      durée en secondes, les lignes non vides de sa sortie (toutes, ou les `garder` dernières). Une épreuve coupée
      rend ce qu'elle a écrit avant la coupure (stdout puis stderr), puis « ARRÊTÉE : plus de N s » en dernière ligne.
      [rend: 3]
    ⑥ TRAITEMENT — lancer `py <épreuve> <arguments>` dans le dossier, avec les variables qui
      arment la mesure et désignent le dossier des empreintes, sans la configuration Git de
      la machine (`SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE`), et sans aucune des variables des fichiers de
      commandes de GitHub (`fichiers_de_commandes_de_github`).
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Le même Python pour toutes les épreuves : la mesure les suit toutes. Sans la
      configuration Git de la machine : le 02-10-2026 à 19h37, la machine du Chat signait ses
      commits par un programme apparu dans la journée, et une épreuve qui fabrique des dépôts
      Git (`SABOTER_LES_CORRECTIONS_DU_GARDE_FOU`) rougissait ici et pas ailleurs ; lancée sans
      cette configuration, elle est verte. Une épreuve ne doit dépendre que du dépôt. Sans les fichiers de commandes
      de GitHub (superviseur R-759 du 15-11-2026, SUPERVISEUR_GHUB_Dim_15-11-2026.md, 2.1) : sur une machine du
      dépôt PUBLIC, ce qu'une épreuve écrirait dans GITHUB_STEP_SUMMARY s'afficherait à tout visiteur, et ce qu'elle
      écrirait dans GITHUB_ENV ou GITHUB_OUTPUT changerait les pas suivants ; le joueur des séries les retirait
      déjà, la nuit non (aucun programme n'y écrivait le 15-11-2026, recherche du superviseur : un trou fermé avant
      d'être emprunté).
      Garder la sortie d'une épreuve coupée : superviseur R-759 du 15-11-2026 (etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/
      SUPERVISEUR_CERT3_Dim_15-11-2026.md, §2, A2, « DE FOND ») — une coupure est justement un rouge à diagnostiquer,
      et la donnée était déjà portée par l'exception ; elle était jetée.
    ⑨ CE QUI CLOCHE — Une épreuve qui écrit dans la copie peut gêner la suivante ; toutes
      sont écrites pour travailler sur leurs propres copies. La sortie entière est tenue en mémoire : une épreuve
      bavarde (des centaines de milliers de lignes) pèserait d'autant ; aucune n'a été mesurée ainsi. Une épreuve
      coupée : stdout et stderr sont mis bout à bout, sans leur entrelacement réel ; une épreuve dont des
      petits-processus tiennent encore les tuyaux après la coupure n'a pas été essayée (THÉORIQUE : sous POSIX,
      `subprocess.run` ne fait que `wait()` après `kill()`).
    ⑩ EFFET — Lance un processus.
    ⑪ TERMINAISON — Rend la main ; l'épreuve est arrêtée à `delai` secondes.
      [sort: non]
    """
    env = dict(os.environ, COVERAGE_PROCESS_START=reglages, CERTIF_MANIFESTES=manifestes)
    env.update(SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)
    for v in fichiers_de_commandes_de_github():
        env.pop(v, None)
    if lectures:
        env["CERTIF_LECTURES"] = lectures
    args = [a.replace("{copie}", copie) for a in arguments]
    debut = time.time()
    try:
        r = subprocess.run([py, os.path.join(copie, chemin)] + args, cwd=os.path.join(copie, dossier), env=env,
                           capture_output=True, text=True, errors="replace", timeout=delai)
        code, sortie = r.returncode, (r.stdout + r.stderr)
    except subprocess.TimeoutExpired as e:
        # ce que l'épreuve coupée a écrit : sous text=True, l'exception le rend en OCTETS, et None si rien n'a été
        # écrit (mesuré, Python 3.13) — décodé ou ignoré, sinon TypeError ici et la tranche tomberait sans partiel
        lu = "".join(x.decode("utf-8", "replace") if isinstance(x, bytes) else x for x in (e.stdout, e.stderr) if x)
        code, sortie = 124, lu + f"\nARRÊTÉE : plus de {delai} s"
    lignes = [l for l in sortie.strip().splitlines() if l.strip()]
    return code, round(time.time() - debut), (lignes if garder is None else lignes[-garder:])


def comparer(tableau, lancements, reference, sources):
    """Rend les reculs de la mesure et les épreuves disparues, par rapport à la référence.

    ① RÔLE — Dire en quoi cette version examine moins que la référence.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `tableau` : la mesure · `lancements` : les épreuves jouées · `reference` ·
      `sources` : pour chaque programme présent, le compte de ses lignes par texte (débarrassé
      des espaces de bord), lu sur le disque.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : les reculs de mesure (lignes, embranchements, fonctions, lignes
      non examinées supprimées ou modifiées) et les épreuves disparues, en phrases.
      [rend: 2]
    ⑥ TRAITEMENT — ① chaque lancement de la référence doit être encore joué, comparé sans « --seulement=… » ; le
      lancement entier « --saboter » d'une épreuve est joué si TOUS ses morceaux 1/N … N/N le sont (A-961) · ② pour chaque
      programme, et pour chaque texte de ligne ou couple d'embranchement, le nombre de
      non-examinés ne doit pas augmenter ; une fonction non examinée doit être déjà dans la
      liste de la référence ; un programme absent de la référence doit tout avoir examiné ;
      ③ une ligne non examinée à la référence ne disparaît pas du programme : si son texte y
      figure moins de fois qu'il n'était non examiné, elle a été supprimée ou modifiée sans
      qu'aucune épreuve l'exécute — c'est un recul ; et un programme de la référence qui
      portait des lignes non examinées ne disparaît pas du disque non plus (relecture de
      Cowork du 02-10-2026, troisième tour, cas K19 : le supprimer était certifié, alors que
      le vider ne l'était pas). Ranger un programme aux archives passe donc par l'accord de
      Jean-Luc (`--accord`) : rien ne se supprime sans validation.
    ⑦ UNITÉ — Des nombres de lignes et d'embranchements.
    ⑧ POURQUOI — Comparer des NOMBRES par programme laissait passer un échange : examiner une
      autre ligne que celle de la référence, à total égal (relecture du 01-10-2026). Par
      texte, la ligne qui cesse d'être examinée se voit, même si une autre l'est devenue.
      Le ③ : retirer une ligne non examinée faisait BAISSER le compte des non-examinés, ce
      qui n'était jamais un recul ; un programme qu'aucune épreuve n'exécute pouvait être
      vidé ou amputé d'une ligne et la version restait certifiée (relecture de Cowork du
      02-10-2026, cas K9 et K13 ; le détecteur des signaux était dans ce cas). Ce qu'aucune
      épreuve n'exécute ne change donc pas sans refus : l'éprouver d'abord, ou l'accord de
      Jean-Luc pour écrire la référence (`--accord`).
    ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨ ⑥ : un même texte présent ailleurs dans le
      programme, sur une ligne examinée, peut masquer la suppression d'une ligne non
      examinée de même texte. Un programme disparu n'est pas un recul
      de mesure (son code n'existe plus) : `main` le dit en remarque.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    mesure, epreuves = [], []
    for nom, r in reference.get("programmes", {}).items():
        if nom not in sources and r.get("lignes_non_examinees"):
            mesure.append(f"{nom} : programme supprimé alors que {sum(r['lignes_non_examinees'].values())} ligne(s) n'y "
                          "étaient exécutées par aucune épreuve — l'éprouver d'abord, ou l'accord de Jean-Luc")
    def forme(l):
        """Rend la forme comparable d'un lancement : le lancement sans ses arguments « --seulement=… », en JSON.

        ① RÔLE — Comparer un lancement de la référence à ceux de la version sans dépendre de la liste des sabotages.
        ② CONTEXTE D'APPEL — `comparer`, une fois par lancement de la version et de la référence.
        ③ ENTRÉE — `l` : un lancement [chemin, dossier, arguments].
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : un texte JSON.
          [rend: 1]
        ⑥ TRAITEMENT — filtrer les arguments, puis json.dumps.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un sabotage ajouté à une épreuve en morceaux change les codes d'un morceau : sans ce filtre, la
          référence verrait le morceau « disparu » à chaque ajout (A-961).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return json.dumps([l[0], l[1], [a for a in l[2] if not a.startswith(ARGUMENT_DES_SABOTAGES)]])
    joues = {forme(l) for l in lancements}
    morceaux_joues = collections.defaultdict(set)
    for l in lancements:
        if morceau_de(l):
            morceaux_joues[(l[0], l[1])].add(morceau_de(l))
    for (chemin, dossier), vus in morceaux_joues.items():
        n = {m.split("/")[1] for m in vus}
        if len(n) == 1 and vus == {f"{i}/{next(iter(n))}" for i in range(1, int(next(iter(n))) + 1)}:
            joues.add(json.dumps([chemin, dossier, ["{copie}", "--saboter"]]))
    for l in reference.get("epreuves", []):
        if forme(l) not in joues:
            epreuves.append(f"épreuve disparue : {l[0]} {' '.join(a for a in l[2] if a != '{copie}')}")
    ref = reference.get("programmes", {})
    for nom, m in tableau.items():
        r = ref.get(nom)
        if r is None:
            if m["instructions_non_examinees"]:
                mesure.append(f"{nom} : programme nouveau, {m['instructions_non_examinees']} instruction(s) non examinée(s)")
            continue
        for cle, quoi in (("lignes_non_examinees", "ligne"), ("branches_non_examinees", "embranchement")):
            pires = [t for t, n in m[cle].items() if n > r.get(cle, {}).get(t, 0)]
            if pires:
                mesure.append(f"{nom} : {len(pires)} {quoi}(s) de plus non examiné(s) — "
                              + " | ".join(p[:70] for p in pires[:3]))
        src = sources.get(nom, collections.Counter())
        otees = [t for t, n in r.get("lignes_non_examinees", {}).items() if t != "<sortie>" and src[t] < n]
        if otees:
            mesure.append(f"{nom} : {len(otees)} ligne(s) qu'aucune épreuve n'exécute supprimée(s) ou modifiée(s) — "
                          "l'éprouver d'abord — " + " | ".join(o[:70] for o in otees[:3]))
        nouvelles = sorted(set(m["fonctions_non_examinees"]) - set(r["fonctions_non_examinees"]))
        if nouvelles:
            mesure.append(f"{nom} : fonction(s) non examinée(s) hors référence — " + ", ".join(nouvelles))
    return mesure, epreuves


def ecrire_le_rapport(racine, horodatage, resultats, tableau, reculs, verdict, calibration, non_declarees, notes):
    """Écrit `rapports/CERTIFICAT_DE_LA_VERSION.md` dans la racine.

    ① RÔLE — Laisser une trace lisible de la certification.
    ② CONTEXTE D'APPEL — `main`, à la fin, quel que soit le verdict.
    ③ ENTRÉE — `racine` · `horodatage` (Paris) · `resultats` : (épreuve, arguments, code,
      durée, lignes) · `tableau` : la mesure (peut être vide) · `reculs` · `verdict` ·
      `calibration` : la phrase du calibrage · `non_declarees` · `notes` : remarques sans
      effet sur le verdict (dérive de mesure, programme disparu).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — verdict, totaux, reculs, remarques, épreuves, programmes du moins examiné
      au plus examiné, fonctions non examinées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Jean-Luc et Cowork lisent le dépôt, pas les journaux de GitHub.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    t = ["FABRIQUÉ · Rôle : dire si la version du dépôt est certifiée.\nQuand l'appeler : après chaque certification.\n",
         f"# CERTIFICAT DE LA VERSION — {horodatage} (Paris)\n", f"**{verdict}**\n"]
    if tableau:
        ins = sum(m["instructions"] for m in tableau.values())
        ins_n = sum(m["instructions_non_examinees"] for m in tableau.values())
        br = sum(m["embranchements"] for m in tableau.values())
        br_n = sum(m["embranchements_non_examines"] for m in tableau.values())
        fon = sum(m["fonctions"] for m in tableau.values())
        fon_n = sum(len(m["fonctions_non_examinees"]) for m in tableau.values())
        t.append(f"Instructions examinées : {ins - ins_n} sur {ins} ({100 * (ins - ins_n) / max(ins, 1):.1f} %) · "
                 f"embranchements examinés : {br - br_n} sur {br} · fonctions examinées : {fon - fon_n} sur {fon} · "
                 f"fonctions qu'aucune épreuve n'examine : {fon_n}.\n")
    t.append(f"Calibrage de la mesure : {calibration}.\n")
    if non_declarees:
        t.append("Épreuves non déclarées dans " + LANCEMENT + " : " + ", ".join(non_declarees) + "\n")
    if reculs:
        t.append("## RECULS\n" + "\n".join("- " + r for r in reculs) + "\n")
    if notes:
        t.append("## REMARQUES\n" + "\n".join("- " + r for r in notes) + "\n")
    if resultats:
        t.append("## ÉPREUVES\n| épreuve | arguments | code | durée (s) |\n|---|---|---|---|")
        for chemin, args, code, duree, _ in resultats:
            t.append(f"| {chemin} | {' '.join(a for a in args if a != '{copie}')} | {code} | {duree} |")
        for c, a, code, _, lignes in resultats:
            if code != 0:
                t.append(f"\n**ROUGE : {c} {' '.join(x for x in a if x != '{copie}')}**\n```\n" + "\n".join(lignes) + "\n```")
    if tableau:
        t.append("\n## PROGRAMMES, DU MOINS EXAMINÉ AU PLUS EXAMINÉ\n"
                 "| programme | instructions examinées | embranchements examinés | fonctions examinées |\n|---|---|---|---|")
        for nom, m in sorted(tableau.items(), key=lambda kv: (kv[1]["instructions"] - kv[1]["instructions_non_examinees"])
                             / max(kv[1]["instructions"], 1)):
            t.append(f"| {nom} | {m['instructions'] - m['instructions_non_examinees']}/{m['instructions']} | "
                     f"{m['embranchements'] - m['embranchements_non_examines']}/{m['embranchements']} | "
                     f"{m['fonctions'] - len(m['fonctions_non_examinees'])}/{m['fonctions']} |")
        t.append("\n## FONCTIONS QU'AUCUNE ÉPREUVE N'EXAMINE\n")
        for nom, m in sorted(tableau.items()):
            if m["fonctions_non_examinees"]:
                t.append(f"- **{nom}** : " + ", ".join(m["fonctions_non_examinees"]))
    os.makedirs(os.path.join(racine, "rapports"), exist_ok=True)
    with open(os.path.join(racine, RAPPORT), "w", encoding="utf-8") as f:
        f.write("\n".join(t) + "\n")


FACTEUR_DE_COUPURE = 3          # la coupure d'un lancement déjà joué une nuit : au moins 3 fois sa durée relevée


def coupure(cle, delais, durees):
    """Rend le délai au-delà duquel un lancement est coupé (code 124) : le plus grand du délai et de 3 × sa durée relevée,
    ce triple plafonné à 3 × `DUREE_MAX_EPREUVE`.

    ① RÔLE — Donner à `jouer` et à `refaire_des_essais` la coupure d'un lancement, qui suit sa durée MESURÉE au lieu de
      rester pour toujours au chiffre déclaré.
    ② CONTEXTE D'APPEL — `jouer_les_lancements`, une fois par lancement joué ou par série dont les essais sont refaits ;
      tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py, cas N9.
    ③ ENTRÉE — `cle` : la clé du lancement (`cle_de`) · `delais` : {clé : secondes} de `options_de_lancement` ·
      `durees` : {clé : secondes} de `durees_relevees`.
    ④ CONDITIONS D'ENTRÉE — Les valeurs des deux dictionnaires sont des nombres de secondes.
    ⑤ SORTIE — UNE valeur : la coupure, en secondes. Délai = le délai déclaré, sinon `DUREE_MAX_EPREUVE` ; coupure =
      max(délai, min(`FACTEUR_DE_COUPURE` × durée relevée, `FACTEUR_DE_COUPURE` × `DUREE_MAX_EPREUVE`)) quand une
      durée est relevée, sinon le délai.
      [rend: 1]
    ⑥ TRAITEMENT — ① le délai : `delais`, sinon `DUREE_MAX_EPREUVE` · ② si `durees` porte la clé, le plus grand du
      délai et de 3 fois la durée relevée, ce triple ramené au plus à 3 × `DUREE_MAX_EPREUVE`.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Relecture de Cowork du 09-11-2026, B3-2 : la note du bloc 3 disait « la première nuit remplace ces
      délais par la durée relevée » ; c'était vrai pour la répartition (`repartir`), faux pour la coupure, qui lisait
      le seul délai déclaré. Les délais des onze lancements nouveaux du bloc 3 (300 s au moins) viennent de mesures
      faites SANS la mesure de couverture, que la certification multiplie par environ 2,2 (tests/LANCEMENT_DES_EPREUVES
      .json, l'épreuve d'arrivée des signaux) : un lancement de 950 s coupé à 900 s rougissait chaque nuit, et la
      durée relevée valait 900. Décision du Chat, sous la délégation de Jean-Luc n°129, du 09-11-2026 : coupure =
      max(délai déclaré, 3 × durée relevée). Le max : un délai déclaré n'est jamais raccourci par une nuit rapide.
      Le facteur 3 : les durées relevées ont varié du simple au double d'une nuit à l'autre (le ⑧ de
      `durees_relevees`), et la répartition vise une tranche au tiers de sa limite.
      LE PLAFOND (relecture de Cowork du 09-11-2026, 4dcffa32, point 1 : sans lui, un lancement qui ne finit jamais
      voyait sa coupure tripler à chaque nuit, 1 500 s, 4 500 s, 13 500 s, jusqu'à faire tomber la tranche entière
      sur la limite de GitHub) : décision du Chat sous la délégation n°129, du 09-11-2026, À CONFIRMER PAR JEAN-LUC.
      Le plafond borne la croissance par la durée relevée, jamais le délai déclaré : la formule demandée,
      min(max(délai, 3 × durée), 3 × `DUREE_MAX_EPREUVE`), aurait coupé à 4 500 s les cinq lancements déclarés à plus
      de 4 500 s, dont la série de la lecture des cours (délai 10 800 s, durée relevée 5 097 s) : rouge sûr chaque
      nuit. Mesure du 09-11-2026 sur les journaux du dépôt (etudes/BLOC3_SORTIES/11c_plafond_sur_les_vraies_durees.log).
    ⑨ CE QUI CLOCHE — Un lancement non déclaré dont la durée vraie dépasse 3 × `DUREE_MAX_EPREUVE` est coupé chaque
      nuit : son rouge reste visible, et le remède est de lui déclarer un délai (« delais »). Le plafond n'est confirmé par personne
      d'autre que le Chat (BACKLOG, à consigner).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    delai = delais.get(cle, DUREE_MAX_EPREUVE)
    if cle in durees:
        return max(delai, min(FACTEUR_DE_COUPURE * durees[cle], FACTEUR_DE_COUPURE * DUREE_MAX_EPREUVE))
    return delai


def jouer_les_lancements(copie, jetable, racine, py, reglages, manifestes, lancements, delais, series, durees):
    """Joue des lancements dans l'ordre donné, sous la mesure, et rend leurs résultats.

    ① RÔLE — La boucle des épreuves, la même pour la certification entière et pour une tranche de la nuit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `copie` · `jetable` : le dossier jetable · `racine` : le dépôt certifié · `py`, `reglages`,
      `manifestes` : la mesure armée · `lancements` : ceux à jouer · `delais`, `series` : de `options_de_lancement` ·
      `durees` : de `durees_relevees`, obligatoire (un appelant qui l'oublierait tombe, il ne coupe pas en silence).
    ④ CONDITIONS D'ENTRÉE — La mesure est armée et calibrée.
    ⑤ SORTIE — UNE valeur : la liste des [chemin, dossier, arguments, code, durée, lignes], dans l'ordre joué.
      [rend: 1]
    ⑥ TRAITEMENT — une série déclarée « series_hors_de_la_nuit » n'est pas rejouée : son relevé est vérifié
      (`verifier_une_serie`), puis des essais refaits (`refaire_des_essais`) ; tout autre lancement est joué
      (`jouer`) ; chacun est coupé à `coupure` (délai déclaré, ou 3 × la durée relevée plafonné, s'il est plus grand) ;
      sa sortie est gardée par `lignes_gardees` (entière s'il est rouge, depuis le 15-11-2026) ; une ligne par
      lancement à l'écran (`ligne_du_journal`).
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Une seule rédaction de la boucle (R-708) pour les deux modes.
    ⑨ CE QUI CLOCHE — La vérification d'une série lit ce que le lancement normal de la même épreuve a lu : il doit
      être joué AVANT, dans le même appel (`repartir` garde une épreuve entière dans une tranche).
    ⑩ EFFET — Lance les épreuves ; écrit à l'écran.
    ⑪ TERMINAISON — Rend la main ; chaque épreuve est bornée par sa coupure (`coupure`).
      [sort: non]
    """
    resultats, lus_par_epreuve = [], {}
    for chemin, dossier, arguments in lancements:
        cle = cle_de(chemin, arguments)
        if chemin in series and "--saboter" in arguments:
            code, duree, lignes = verifier_une_serie(copie, chemin, series[chemin],
                                                     lus_par_epreuve.get(chemin, set()))
            if code == 0 and series[chemin]["essais"]:
                code, duree, autres = refaire_des_essais(copie, py, reglages, manifestes, chemin,
                                                         series[chemin]["releve"], series[chemin]["essais"],
                                                         coupure(cle, delais, durees))
                lignes = lignes + autres
        else:
            lectures = None
            if chemin in series:
                lectures = os.path.join(jetable, "lectures", os.path.basename(chemin))
                os.makedirs(lectures, exist_ok=True)
            code, duree, lignes = jouer(copie, py, reglages, manifestes, chemin, dossier, arguments,
                                        coupure(cle, delais, durees), lectures)
            if lectures:
                lus_par_epreuve[chemin] = fichiers_lus(lectures, copie, racine)
        resultats.append([chemin, dossier, arguments, code, duree, lignes_gardees(code, lignes)])
        print(ligne_du_journal(chemin, arguments, code, duree), flush=True)
    return resultats


# Le nombre de dernières lignes gardées de la sortie d'une épreuve VERTE (une épreuve rouge garde tout, `lignes_gardees`).
LIGNES_D_UNE_EPREUVE_VERTE = 3


def lignes_gardees(code, lignes):
    """Rend ce qui est gardé de la sortie d'un lancement : tout s'il est rouge, les dernières lignes s'il est vert.

    ① RÔLE — La seule règle de coupe de la sortie d'un lancement, pour le certificat partiel et le certificat.
    ② CONTEXTE D'APPEL — `jouer_les_lancements`, une fois par lancement ;
      tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py, cas N11.
    ③ ENTRÉE — `code` : le code de sortie du lancement · `lignes` : les lignes de sa sortie, toutes.
    ④ CONDITIONS D'ENTRÉE — `lignes` est une liste.
    ⑤ SORTIE — UNE valeur : `lignes` entière si `code` n'est pas 0 ; ses `LIGNES_D_UNE_EPREUVE_VERTE` dernières sinon.
      [rend: 1]
    ⑥ TRAITEMENT — un test sur le code.
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — Enquête du 15-11-2026 (etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/ENQUETE_CERTIFICATION_
      ROUGE_Dim_15-11-2026.md, C6) : VENTE_UNIQUE_A rougit chaque nuit sur GitHub et reste verte sur la machine ; la
      sortie gardée ne portait que 3 lignes, et le cas fautif est resté inconnu. Le superviseur R-759 du 15-11-2026
      (même dossier, réparation 8, « DE FOND ») : garder la sortie entière d'une épreuve rouge, préalable au diagnostic
      de C6, C2 et C12. La sortie va au dépôt privé (certificats partiels, certificat), jamais au journal public, qui ne
      porte qu'une ligne par lancement (`ligne_du_journal`). Une épreuve verte garde 3 lignes, comme avant : rien à
      diagnostiquer, et les certificats partiels ne grossissent pas.
    ⑨ CE QUI CLOCHE — Une épreuve rouge très bavarde grossit d'autant le certificat partiel poussé au privé et le
      certificat ; aucune borne n'est posée (une borne écrite ici serait un chiffre sans mesure).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return list(lignes) if code != 0 else list(lignes)[-LIGNES_D_UNE_EPREUVE_VERTE:]


def conclure(racine, ou, horodatage, resultats, lancements, tableau, reference, empreinte, ecrire, accord,
             non_declarees, notes):
    """Compare la mesure à la référence, écrit le certificat (et la référence si demandé), et rend le code de sortie.

    ① RÔLE — La fin d'une certification, entière ou réunie depuis les tranches de la nuit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : le dépôt certifié, où écrire · `ou` : où lire les programmes (la copie, ou la racine en
      réunion) · `horodatage` · `resultats` : (épreuve, arguments, code, durée, lignes) · `lancements` : tous ·
      `tableau` : la mesure (`tableau_de`) · `reference` : la référence lue, ou None · `empreinte` : celle du code ·
      `ecrire`, `accord` : l'écriture de la référence · `non_declarees` · `notes` : remarques déjà faites.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0 certifiée (ou référence écrite), 1 recul (ou référence refusée), 2 impossible.
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑦ et ⑧, et la fiche de `main`, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule rédaction de la conclusion (R-708) pour la certification entière et pour la réunion
      des tranches (décision de Jean-Luc du 30-10-2026 à 19h02).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit `rapports/CERTIFICAT_DE_LA_VERSION.md` ; et la référence sur demande.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin_ref = os.path.join(racine, REFERENCE)
    # UN SEUL REFUS POUR « NE SE LIT PAS », APRÈS LA MESURE (troisième tour, 02-10-2026) : un programme
    # que Python ne lit pas comme un script (K1, K7 de Cowork), et un programme présent dont la mesure
    # n'a aucun rapport. Placés avant les épreuves, ces refus laissaient la garde de la mesure sans
    # aucun cas qui l'atteigne : le certificateur se refusait lui-même, et il avait raison.
    presents = programmes_de(ou)
    illisibles = programmes_illisibles(ou)
    non_mesures = sorted(rel for rel in presents if rel not in tableau
                         and not any(i.startswith(rel + " (") for i in illisibles))
    if illisibles or non_mesures:
        raison = " · ".join(p for p in (
            "programme(s) que Python ne sait pas lire : " + " · ".join(illisibles) if illisibles else "",
            "programme(s) présent(s) sans rapport de mesure : " + ", ".join(non_mesures) if non_mesures else "")
            if p)
        ecrire_le_rapport(racine, horodatage, resultats, tableau, [], "CERTIFICATION IMPOSSIBLE — " + raison,
                          "réussie (sonde vue, leurre écarté)", non_declarees, notes)
        print("CERTIFICATION IMPOSSIBLE — " + raison)
        return 2
    rouges = [f"épreuve rouge : {c} {' '.join(a for a in ar if a != '{copie}')} (code {code})"
              for c, ar, code, _, _ in resultats if code != 0]
    notes, reculs_mesure, disparues = list(notes), [], []
    if reference is not None:
        sources = {rel: collections.Counter(l.strip() for l in
                                            open(a, encoding="utf-8", errors="replace").read().splitlines())
                   for rel, a in presents.items()}
        reculs_mesure, disparues = comparer(tableau, lancements, reference, sources)
        notes += [f"programme disparu depuis la référence : {n}" for n in reference.get("programmes", {})
                  if n not in presents]
        if reculs_mesure and not rouges and not disparues and reference.get("empreinte_du_code") == empreinte:
            notes += ["DÉRIVE DE MESURE, code identique à la référence (" + empreinte + ") : " + r
                      for r in reculs_mesure]
            reculs_mesure = []
    reculs = rouges + disparues + reculs_mesure
    if ecrire:
        if rouges:
            verdict, code_final = "RÉFÉRENCE NON ÉCRITE — une épreuve est rouge", 1
        elif reference is not None and reculs and not accord:
            verdict, code_final = "RÉFÉRENCE NON ÉCRITE — elle reculerait ; il faut l'accord de Jean-Luc (--accord)", 1
        else:
            with open(chemin_ref, "w", encoding="utf-8") as f:
                json.dump({"ecrite_le": horodatage, "empreinte_du_code": empreinte,
                           "accord": accord or "première référence, ou aucun recul",
                           "epreuves": lancements, "programmes": tableau},
                          f, ensure_ascii=False, indent=1, sort_keys=True)
            verdict, code_final = "RÉFÉRENCE ÉCRITE — " + REFERENCE, 0
    else:
        verdict = ("VERSION CERTIFIÉE — toutes les épreuves sont vertes et rien ne recule"
                   if not reculs else f"VERSION NON CERTIFIÉE — {len(reculs)} recul(s)")
        code_final = 0 if not reculs else 1
    ecrire_le_rapport(racine, horodatage, resultats, tableau, reculs, verdict, "réussie (sonde vue, leurre écarté)",
                      non_declarees, notes)
    print(verdict)
    return code_final


def ecrire_le_partiel(racine, contenu):
    """Écrit le certificat partiel d'une tranche de la nuit, `PARTIELS`/TRANCHE_<i>.json, dans la racine.

    ① RÔLE — Laisser à la tâche finale ce que la tranche a joué et mesuré.
    ② CONTEXTE D'APPEL — `main`, en mode tranche, une fois (qu'elle ait pu jouer ou non).
    ③ ENTRÉE — `racine` · `contenu` : le dictionnaire (« tranche » y est).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — JSON, dans un fichier temporaire renommé (un fichier à moitié écrit ne se lit pas comme entier).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le pas « deposer » de la tranche pousse ce fichier au dépôt privé, où la tâche finale le lit. Pas
      d'archive de GitHub : celles d'un dépôt public sont téléchargeables par tous (fiche de
      programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, ⑥ ③).
    ⑨ CE QUI CLOCHE — Le fichier porte les numéros des lignes et des embranchements non examinés de chaque programme,
      réécrit chaque nuit au dépôt privé : sa taille sur le vrai dépôt n'est pas mesurée (estimée à quelques centaines
      de kilooctets par tranche le 30-10-2026, d'après la référence, 338 450 octets en textes de lignes).
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(os.path.join(racine, PARTIELS), exist_ok=True)
    f = os.path.join(racine, PARTIELS, f"TRANCHE_{contenu['tranche']}.json")
    with open(f + ".part", "w", encoding="utf-8") as s:
        json.dump(contenu, s, ensure_ascii=False, sort_keys=True)
    os.replace(f + ".part", f)


def lire_la_ligne_de_commande(argv):
    """Lit la ligne de commande du certificateur.

    ① RÔLE — Dire quel mode est demandé : la certification entière, une tranche de la nuit, ou la réunion.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `argv` : sys.argv.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — SIX valeurs : la racine (ou None si la ligne est fausse), `ecrire` (booléen), `accord` (texte),
      `tranche` ((i, n) ou None), `reunir` (n ou None), la raison du refus (texte vide si la ligne est bonne).
      [rend: 6]
    ⑥ TRAITEMENT — « --ecrire-la-reference », « --accord <texte> », « --tranche i/n » (1 ≤ i ≤ n), « --reunir n »
      (n ≥ 1) ; « --tranche » et « --reunir » ne vont ni ensemble ni avec « --ecrire-la-reference ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La référence s'écrit d'un passage entier, sur une seule machine : jamais d'une tranche.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def valeur(nom):
        """Rend le mot qui suit une option de la ligne de commande, ou None.

        ① RÔLE — Lire la valeur d'une option à valeur (« --accord », « --tranche », « --reunir »).
        ② CONTEXTE D'APPEL — `lire_la_ligne_de_commande`, une fois par option à valeur.
        ③ ENTRÉE — `nom` : le nom de l'option, par exemple « --tranche ».
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le mot qui suit la première occurrence de `nom` dans `argv`, ou None si `nom` est
          absent ou en dernière position.
          [rend: 1]
        ⑥ TRAITEMENT — chercher `nom` dans `argv` sans son dernier mot, puis prendre le mot suivant.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une option écrite sans sa valeur rend None : l'appelant la refuse alors avec sa raison.
        ⑨ CE QUI CLOCHE — Une option écrite deux fois : seule la première est lue, sans rien dire.
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return argv[argv.index(nom) + 1] if nom in argv[:-1] else None

    ecrire = "--ecrire-la-reference" in argv
    accord, t, r = valeur("--accord") or "", valeur("--tranche"), valeur("--reunir")
    args = [a for a in argv[1:] if not a.startswith("--") and a not in {accord, t, r}]
    tranche = reunir = None
    try:
        if t is not None:
            i, n = (int(x) for x in t.split("/"))
            if not 1 <= i <= n:
                raise ValueError
            tranche = (i, n)
        if r is not None:
            reunir = int(r)
            if reunir < 1:
                raise ValueError
    except ValueError:
        return None, ecrire, accord, None, None, "« --tranche i/n » ou « --reunir n » illisible"
    if ("--tranche" in argv and tranche is None) or ("--reunir" in argv and reunir is None):
        return None, ecrire, accord, None, None, "« --tranche » ou « --reunir » sans valeur"
    if sum(x is not None for x in (tranche, reunir)) + ecrire > 1:
        return None, ecrire, accord, None, None, "« --tranche », « --reunir » et « --ecrire-la-reference » s'excluent"
    if len(args) < 1 or not os.path.isdir(os.path.join(args[0], "programmes")):
        return None, ecrire, accord, None, None, "racine absente"
    return os.path.abspath(args[0]), ecrire, accord, tranche, reunir, ""


def main():
    """Certifie la version, ou une tranche de la nuit, ou réunit les tranches, ou dit pourquoi ce n'est pas possible.

    ① RÔLE — Le programme entier (voir la fiche en tête).
    ② CONTEXTE D'APPEL — La ligne de commande. La nuit, au dépôt public (.github/workflows/certifier_la_version.yml,
      fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py) : « --tranche i/n » dans chaque tranche, puis
      « --reunir n » dans la tâche finale.
    ③ ENTRÉE — Voir la fiche en tête, et `lire_la_ligne_de_commande`. L'environnement : GITHUB_RUN_ID, le numéro du
      passage (« local » hors de GitHub).
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête.
    ⑤ SORTIE — Le code de sortie, 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ① à ⑧. Un programme présent sous `programmes/` que la
      mesure n'a pas pu lire (une erreur de syntaxe, par exemple) rend 2 : il n'a pas été
      mesuré, ce n'est pas un programme disparu — « disparu » veut dire absent du disque
      (relecture de Cowork du 02-10-2026, cassure K1 : un programme jamais éprouvé, cassé,
      laissait la version « certifiée »). Un recul de mesure, sans épreuve rouge ni
      disparue, alors que l'empreinte du code est celle de la référence, est une dérive de
      mesure : dit en remarque, sans rougir (fiche ⑨ ④).
      MODE TRANCHE (« --tranche i/n ») : les lancements sont répartis (`repartir`, durées de `durees_relevees`) ;
      seuls ceux de la tranche i sont joués ; le certificat partiel est écrit (`ecrire_le_partiel`), et non le
      certificat ; rend 2 si la tranche n'a pas pu jouer, 1 si une épreuve est rouge, 0 sinon.
      MODE PUBLICATION (« --publier-les-durees », seul) : rien n'est joué ; `publier_les_durees` écrit
      `DUREES_PUBLIEES` ; 0 si écrit, 2 sinon (A-968, décision de Jean-Luc du 21-11-2026 à 15h34).
      MODE RÉUNION (« --reunir n ») : rien n'est joué ; les certificats partiels sont lus et vérifiés
      (`reunir_les_tranches`) ; une tranche absente, rouge d'impossibilité, d'un autre passage ou d'un autre code, ou
      un lancement joué zéro ou deux fois : CERTIFICATION IMPOSSIBLE, code 2 ; sinon la conclusion est celle de la
      certification entière (`conclure`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête. Les tranches : décision de Jean-Luc du 30-10-2026 à 19h02 (voir `JOURNAUX`).
    ⑨ CE QUI CLOCHE — Une épreuve rouge d'une tranche fait rougir la tranche ET la réunion : la réunion le dit dans
      le certificat, la tranche dans son job.
    ⑩ EFFET — Voir la fiche en tête ; en mode tranche, écrit `PARTIELS`/TRANCHE_<i>.json au lieu du certificat ; en
      mode publication, écrit `DUREES_PUBLIEES` et rien d'autre.
    ⑪ TERMINAISON — Rend la main au bloc de lancement ; le dossier jetable est effacé.
      [sort: non]
    """
    racine, ecrire, accord, tranche, reunir, refus = lire_la_ligne_de_commande(sys.argv)
    if racine is None:
        print("CERTIFICATION IMPOSSIBLE — " + refus + " — usage : CERTIFIER_LA_VERSION.py <racine du dépôt> "
              "[--ecrire-la-reference [--accord \"…\"]] [--tranche i/n | --reunir n | --publier-les-durees]")
        return 2
    if "--publier-les-durees" in sys.argv:
        if ecrire or tranche or reunir:
            print("PUBLICATION IMPOSSIBLE — « --publier-les-durees » se lance seul")
            return 2
        try:
            print(f"DURÉES PUBLIÉES — {publier_les_durees(racine)} clé(s) dans {DUREES_PUBLIEES}")
            return 0
        except (OSError, ValueError) as e:
            print(f"PUBLICATION IMPOSSIBLE — {e}")
            return 2
    maintenant = datetime.now(ZoneInfo("Europe/Paris"))
    horodatage = ("Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim")[maintenant.weekday()] + maintenant.strftime(" %d-%m-%Y %Hh%M")
    passage = os.environ.get("GITHUB_RUN_ID") or "local"
    empreinte = empreinte_du_code(racine)
    partiel = {"passage": passage, "nombre": tranche[1], "tranche": tranche[0], "empreinte_du_code": empreinte,
               "ecrit_le": horodatage, "impossible": ""} if tranche else None

    def impossible(raison, calibration="non faite", non_declarees=()):
        """Écrit que la certification est impossible, dit pourquoi, et rend le code 2.

        ① RÔLE — Terminer `main` proprement quand la certification ne peut pas se faire.
        ② CONTEXTE D'APPEL — `main`, à chaque cas où la certification ne peut pas aller au bout.
        ③ ENTRÉE — `raison` : la phrase qui dit pourquoi · `calibration` : l'état de la calibration de la mesure ·
          `non_declarees` : les épreuves non déclarées, s'il y en a.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : 2, le code de sortie « impossible ».
          [rend: 1]
        ⑥ TRAITEMENT — ① en mode tranche, noter la raison dans le certificat partiel et l'écrire
          (`ecrire_le_partiel`) · ② sinon, écrire le rapport « CERTIFICATION IMPOSSIBLE » (`ecrire_le_rapport`) ·
          ③ afficher la raison.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un contrôle qui n'a pas pu tourner rend un code de sortie non nul et le dit (R-734).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit le certificat partiel de la tranche, ou le rapport ; affiche une ligne.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if partiel is not None:
            partiel["impossible"] = raison
            ecrire_le_partiel(racine, partiel)
        else:
            ecrire_le_rapport(racine, horodatage, [], {}, [], "CERTIFICATION IMPOSSIBLE — " + raison, calibration,
                              list(non_declarees), [])
        print("CERTIFICATION IMPOSSIBLE — " + raison)
        return 2

    if reunir is None:
        try:
            import coverage  # noqa: F401
        except ImportError:
            print("CERTIFICATION IMPOSSIBLE — le module coverage n'est pas installé")
            return 2
    chemin_ref = os.path.join(racine, REFERENCE)
    reference = json.load(open(chemin_ref, encoding="utf-8")) if os.path.exists(chemin_ref) else None
    if reference is None and not ecrire:
        if tranche is None:     # une tranche n'a pas besoin de la référence : la réunion la lit
            return impossible("référence absente : " + REFERENCE)
    if reunir is not None:
        try:
            lancements, non_declarees = lister_les_epreuves(racine)
        except (OSError, ValueError, KeyError, TypeError, SyntaxError) as erreur:
            return impossible(f"épreuves illisibles ({type(erreur).__name__}: {erreur})")
        if non_declarees:
            return impossible("épreuve(s) non déclarée(s) : " + ", ".join(non_declarees), non_declarees=non_declarees)
        raison, resultats, brute, notes = reunir_les_tranches(racine, reunir, passage, empreinte, lancements)
        if raison:
            return impossible(raison)
        return conclure(racine, racine, horodatage, resultats, lancements, tableau_de(brute, racine), reference,
                        empreinte, False, "", non_declarees, notes)
    jetable = tempfile.mkdtemp(prefix="certification_")
    try:
        copie = copier(racine, jetable)
        py, reglages, manifestes = armer_la_mesure(jetable)
        calibree, raison = calibrer_la_mesure(jetable, py)
        try:
            lancements, non_declarees = lister_les_epreuves(copie)
            delais, series = options_de_lancement(copie)
        except (OSError, ValueError, KeyError, TypeError, SyntaxError) as e:
            # SyntaxError : une épreuve de tests/ qui ne se lit pas ; sans cette prise, le certificateur
            # tombait sur une trace et rendait 1, sans rapport (passe ② du 02-10-2026, cas S21).
            lancements, non_declarees = [], [f"épreuves illisibles ({type(e).__name__}: {e})"]
            delais, series = {}, {}
        if not calibree or non_declarees:
            raison = raison if not calibree else "épreuve(s) non déclarée(s) : " + ", ".join(non_declarees)
            return impossible(raison, "échouée" if not calibree else "réussie", non_declarees)
        if tranche is None:
            resultats = jouer_les_lancements(copie, jetable, racine, py, reglages, manifestes, lancements, delais,
                                             series, durees_relevees(racine, passage))
            return conclure(racine, copie, horodatage, [(r[0], r[2], r[3], r[4], r[5]) for r in resultats],
                            lancements, lire_la_mesure(jetable, reglages, manifestes, copie), reference, empreinte,
                            ecrire, accord, non_declarees, [])
        durees = durees_relevees(racine, passage)
        tranches, charges = repartir(lancements, durees, delais, tranche[1])
        a_jouer = tranches[tranche[0] - 1]
        resultats = jouer_les_lancements(copie, jetable, racine, py, reglages, manifestes, a_jouer, delais, series,
                                         durees)
        partiel.update({"repartition": empreinte_de_la_repartition(tranches), "charges_prevues_secondes": charges,
                        "joues": a_jouer, "resultats": resultats,
                        "mesure": mesure_brute(jetable, reglages, manifestes, copie)})
        ecrire_le_partiel(racine, partiel)
        rouges = sum(1 for r in resultats if r[3] != 0)
        print(f"TRANCHE {tranche[0]}/{tranche[1]} — {len(a_jouer)} lancement(s), {rouges} rouge(s) — "
              f"certificat partiel : {PARTIELS}/TRANCHE_{tranche[0]}.json")
        return 1 if rouges else 0
    finally:
        shutil.rmtree(jetable, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
