#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JOUER_UNE_SERIE_DE_SABOTAGES — Ven 16-10-2026 (Paris). Simulation uniquement.

① RÔLE — Jouer en entier la série de sabotages d'une épreuve trop longue pour la nuit, par lots repris là où ils se
  sont arrêtés, sur plusieurs processeurs, et en écrire le RELEVÉ avec l'empreinte de chaque fichier du dépôt lu
  pendant la série (programmes/SERIES_DE_SABOTAGES.py). La certification de nuit vérifie ensuite ces empreintes.
② CONTEXTE D'APPEL — À la main, à chaque livraison qui change l'épreuve ou un fichier qu'elle lit (R-731), sous
  l'outil de surveillance du Chat (méthode du 10-10-2026, projet de section 12 du mode d'emploi, A-562) :
  python3 -u tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py <racine> <épreuve> <relevé> [--parts=2] [--lot=21]
  [--travail=<dossier>] [--raisons-acceptees=S1,S2,…] — `épreuve` et `relevé` relatifs à la racine.
③ ENTRÉE — La racine d'un dépôt (un clone, jamais le dépôt où l'on travaille : l'épreuve y écrit des dossiers
  jetables) ; l'épreuve, qui doit accepter « --saboter=S1,S2,… » et porter un dictionnaire SABOTAGES ; le relevé.
④ CONDITIONS D'ENTRÉE — Le dossier de travail est propre à cette racine : il garde les lots faits et l'état du dépôt
  au départ ; si le dépôt a changé depuis, le travail est refusé (ARRET) et il faut un dossier neuf.
⑤ SORTIE — Le code de sortie : 0 relevé écrit et série conforme ; 1 relevé écrit, série NON conforme (un sabotage ne
  mord pas, un lot a rendu autre chose que 0) ; 2 rien d'écrit (dépôt changé, épreuve illisible, sortie d'un lot
  introuvable, table de lancement illisible, portée inconnue, écoute SOURDE — un lot dont un flux d'écoute ne nomme
  pas l'épreuve, ou des fichiers couverts qui ne comptent pas l'épreuve). Une sortie de lot qui porte une trace
  d'erreur système (`TRACE_SYSTEME`) rend la série NON CONFORME (1), et les sabotages de ce lot ne comptent pas
  « mord ». Un sabotage dont la RAISON (les épreuves qu'il fait tomber) n'est pas celle du dernier relevé retenu, un
  sabotage nouveau ou disparu, non acceptés par --raisons-acceptees, ou une place libre minimale sous le plancher
  rendent aussi la série NON CONFORME (1), relevé « à examiner ». L'ancien relevé de la même série (même nom, à la date
  près) est rangé dans archives/ avant l'écriture.
  [rend: 1]
⑥ TRAITEMENT — ① lire les noms des sabotages dans l'épreuve (arbre syntaxique, clé du dictionnaire SABOTAGES) ·
  ② prendre l'empreinte de chaque fichier du dépôt (sans .git ni le relevé), ou relire celle du départ et refuser si
  un fichier présent au départ a changé ou disparu ·
  ③ découper en lots ; jouer chaque lot non fait, `--parts` à la fois, l'épreuve écoutée par un module de démarrage
  qui note chaque fichier ouvert en lecture · ④ chaque lot écrit sa sortie et son code, d'abord dans un fichier
  « .part », renommé une fois fini ; le code n'est écrit que si CHAQUE flux d'écoute du processus de l'épreuve
  (FLUX_D_ECOUTE) nomme l'épreuve, sinon le lot est SOURD : pas de code, et la série s'arrête (2) · ④bis l'épreuve
  doit être parmi les fichiers couverts (lus ou exécutés selon la portée), sinon aucune écoute n'a rien entendu (2),
  y compris quand tous les lots sont repris · ④ter une sortie de lot qui porte une trace d'erreur système
  (`trace_d_erreur_systeme`) : le lot est « en erreur système », ses sabotages ne comptent pas « mord », la série
  est NON CONFORME, et une ligne d'en-tête le dit (absente quand il n'y en a pas : le relevé d'une série saine ne
  change pas d'un octet) · ④quater LES DEUX TÉMOINS DE LA RAISON (superviseur R-759 du 05-11-2026, M1 ; commentaire
  de PLANCHER_MO) : (1) la raison de chaque sabotage comparée à celle du dernier relevé retenu de la même série
  (`raisons_a_examiner`) — toute différence non acceptée fait perdre son « mord » au sabotage et une ligne
  d'en-tête la dit ; (2) la place libre mesurée pendant les lots (`surveiller_la_place`), son minimum jugé contre
  le plancher · la dernière ligne d'en-tête dit où la série a été jouée (`ligne_joue_par`) · ⑤ quand tous sont faits : chaque sabotage doit apparaître une fois, « mord » ;
  les fichiers lus = ceux notés ET présents au départ (les dossiers jetables de l'épreuve n'y sont pas) ; leur
  empreinte doit être celle du départ · ⑥ écrire le relevé. Avec la portée « lectures » (la règle d'origine, prise
  quand la table n'en déclare pas), le relevé porte les fichiers LUS. Avec la portée « epreuve » (décision de Jean-Luc
  n°71 du 01-11-2026 à 11h41 : la série de l'épreuve d'arrivée des signaux ne se rejoue que quand le code de l'essai
  change) ou « code_execute » (05-11-2026, CHOIX D43 DU CHAT, À CONFIRMER PAR JEAN-LUC : le code de l'essai lu comme
  le code que la série exécute), le relevé porte les fichiers du dépôt dont le code a été EXÉCUTÉ pendant la série —
  l'écoute note aussi l'évènement d'audit « exec », et `SERIE.fichiers_executes` ramène chaque code exécuté, même
  dans une copie jetable, au fichier du dépôt qu'il représente ; les données n'y entrent pas, elles ne sont jamais
  exécutées. Le relevé porte les mêmes empreintes pour ces deux portées : la nuit ne compare que l'épreuve
  (« epreuve ») ou tout le code exécuté (« code_execute »), et passer de l'une à l'autre se fait d'un mot dans la
  table, sans rejouer la série. La portée vient de la table, lue par `CERTIF.options_de_lancement` (R-708), et ses
  valeurs de `SERIE.PORTEES`.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 14h30 : la série des 167 sabotages de l'épreuve des 20 ans se rejoue
  quand son code change, avec une alarme la nuit si on oublie. Elle dure environ 6 heures sur la machine du Chat
  (27 sabotages en 62 minutes mesurés le 16-10-2026) : les lots permettent la reprise si la machine redémarre, et
  plusieurs lots en même temps divisent la durée. Repères en tête de ligne pour la surveillance : ETAPE, ERREUR,
  FINI, ARRET.
  Le dossier de travail est préparé par UNE fonction, `preparer_le_travail`, appelée aussi par tests/outils/
  jouer_une_part.py et tests/outils/rassembler_les_parts.py (étude du 05-11-2026, github_series/RAPPORT.md §1.3 :
  la part recopiait cette préparation et ne créait pas le dossier « execution » ajouté ici le 05-11-2026 ; le module
  d'écoute plantait au démarrage, l'écoute était SOURDE — 0 ligne lue, code 0 —, mesuré). Deux rédactions d'une
  même chose divergent toujours (R-708). Une écoute vide n'est jamais un succès : chaque flux doit nommer l'épreuve,
  le seul fichier que tout lot lit et exécute à coup sûr (vérifié le 05-11-2026 sous Python 3.11, 3.12 et 3.13 :
  « lus » et « executes » nomment le programme lancé). Trace d'erreur système : un disque plein a déjà donné un faux
  « mord » (series_A, essai 1 du 04-11-2026 : « OSError : [Errno 28] No space left on device », puis « T5 mord »).
  Les deux témoins de la raison (05-11-2026) : une recherche de trace ne voit pas une erreur AVALÉE par l'épreuve ou
  par un de ses enfants (relecture du 05-11-2026, M1 : `lancer` de l'épreuve Yahoo jette la sortie d'erreur ; 55
  « except Exception: » muets dans l'épreuve HL) ; la liste des épreuves tombées, elle, change.
⑨ CE QUI CLOCHE — Le module d'écoute passe par PYTHONPATH : l'épreuve est lancée sans « -I », et un programme qu'elle
  lance avec « -I », « -E » ou « -S », ou avec un environnement remplacé (`env=` sans PYTHONPATH), n'est pas écouté
  — ni ses lectures ni son code exécuté ne sont notés —, et du code exécuté par `exec` d'une chaîne lue dans un fichier
  ne porte pas le nom de ce fichier (relecteur du 05-11-2026, défaut 2 : les cinq mécanismes, détaillés au ⑨ ③ de
  programmes/SERIES_DE_SABOTAGES.py) ; la vérification de
  nuit ne le rattrape pas non plus : ce qui n'est pas lu sous l'écoute n'a pas d'empreinte (la règle « chaque
  programme nommé », qui le rattrapait par hasard de nommage, est retirée le 17-10-2026). · Avec la portée
  « lectures », seules les ouvertures SOUS LA RACINE comptent : un programme exécuté dans une copie faite ailleurs
  n'est pas couvert (la mesure « exec » ne leur est pas appliquée : changer leur mesure pourrait rendre « SÉRIE À
  REJOUER » à la nuit suivante, environ 6 heures pour les 20 ans ; décision séparée, BACKLOG). · Les limites de la
  mesure « exec » : programmes/SERIES_DE_SABOTAGES.py, ⑨. · Un fichier compilé
  (__pycache__) lu à la place d'un .py est ramené à son .py. · Un lot coupé recommence en entier. · Le contrôle
  d'un lot lit les flux « *.<pid> » du processus de l'épreuve : un processus d'un lot PRÉCÉDENT qui aurait reçu le
  même numéro et nommé l'épreuve masquerait un lot sourd (pas ④bis, qui porte sur l'ensemble) ; les numéros de
  processus ne reviennent qu'après des millions de lancements. · Une écoute qui nomme l'épreuve peut ne pas avoir
  tout entendu (programme lancé en « -I », ci-dessus). · `TRACE_SYSTEME` sur-détecte par construction : une épreuve
  qui imprimerait une trace Python ou un « [Errno n] » attendus rendrait sa série NON CONFORME ; calibré le
  05-11-2026 sur 434 sorties de lots réelles de la machine : il ne reconnaît que les 18 sorties du disque plein (2
  sorties distinctes, copiées), 0 des 416 autres ; « MemoryError » n'en fait pas partie (plantage SIMULÉ par une
  épreuve, n83). · Le témoin de la raison exige un relevé retenu : la première série d'une épreuve rend tous ses
  sabotages « nouveaux », donc « à examiner », jusqu'à --raisons-acceptees (voulu : rien n'a été comparé). Une
  épreuve qui change légitimement ses raisons passe aussi par là ; la reprise sur le même dossier de travail ne rejoue
  aucun lot, seulement le compte.
⑩ EFFET — Écrit dans le dossier de travail (lots, empreintes du départ, écoutes) et le relevé ; l'épreuve écrit ses
  dossiers jetables.
⑪ TERMINAISON — Rend la main quand tous les lots ont fini ; un lot n'a pas de délai (il en faut plus de deux heures) ;
  sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import ast
import concurrent.futures
import contextlib
import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import zoneinfo

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "programmes"))
import SERIES_DE_SABOTAGES as SERIE   # noqa: E402  (le relevé : écrit une fois, lu par la certification, R-708)
import CERTIFIER_LA_VERSION as CERTIF  # noqa: E402  (l'environnement de la nuit : défini une fois, R-708)
import FABRIQUER_LE_CIRCUIT_PUBLIC as FABRICANT  # noqa: E402  (les fichiers de commandes de GitHub : une liste, R-708)

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
# L'ÉCOUTE : chaque processus note les fichiers qu'il ouvre en lecture (dossier SERIE_ECOUTE) et, depuis le
# 05-11-2026, le fichier de chaque code qu'il EXÉCUTE (évènement d'audit « exec », dossier SERIE_EXECUTION, à part :
# la lecture des notes « lus » de la portée « lectures » reste inchangée).
ECOUTE = '''import os, sys
_d = os.environ.get("SERIE_ECOUTE")
_x = os.environ.get("SERIE_EXECUTION")
if _d:
    _f = open(os.path.join(_d, "lus.%d" % os.getpid()), "a", encoding="utf-8")
    _g = open(os.path.join(_x, "executes.%d" % os.getpid()), "a", encoding="utf-8") if _x else None
    def _h(ev, a):
        if ev == "open" and a and isinstance(a[0], (str, bytes)) and "w" not in str(a[1] or "r") and "a" not in str(a[1] or "r"):
            _f.write(os.path.realpath(os.fsdecode(a[0])) + "\\n"); _f.flush()
        elif _g is not None and ev == "exec" and a and hasattr(a[0], "co_filename"):
            _g.write(a[0].co_filename + "\\n"); _g.flush()
    sys.addaudithook(_h)
'''
LIGNE = SERIE.LIGNE
# LES FLUX DE L'ÉCOUTE, écrits UNE fois (R-708) : la variable d'environnement que lit le module ECOUTE → le nom de son
# dossier dans le dossier de travail. `preparer_le_travail` les crée tous, `jouer_un_lot` exige que chacun nomme
# l'épreuve, tests/outils/rassembler_les_parts.py les réunit tous.
FLUX_D_ECOUTE = {"SERIE_ECOUTE": "ecoute", "SERIE_EXECUTION": "execution"}
MODULE_D_ECOUTE = "module"      # le dossier du module ECOUTE (PYTHONPATH), qui n'est pas un flux
# UNE TRACE D'ERREUR SYSTÈME dans la sortie d'un lot (étude du 05-11-2026, §2 : un disque plein a donné un faux
# « mord »). Calibrée sur les sorties réelles (fiche en tête, ⑨).
TRACE_SYSTEME = re.compile(r"Traceback \(most recent call last\)|\[Errno \d+\]|No space left on device|\bOSError\b")
# LES DEUX TÉMOINS DE LA RAISON (superviseur R-759 du 05-11-2026, 14h47-14h55, M1 : « un sabotage ne compte « mord » que
# si l'épreuve a rougi POUR SA RAISON, jamais sur une erreur système » ; une épreuve peut avaler l'erreur — 55
# « except Exception: » muets dans l'épreuve HL —, donc aucune recherche de trace ne suffit).
# (1) LA RAISON d'un sabotage est la liste des épreuves qu'il fait tomber ; elle est déterministe (213 sur 213 identiques
#     à une semaine d'écart, mesuré par le superviseur). Elle est comparée à celle du DERNIER RELEVÉ RETENU de la même
#     série : un disque plein fait tomber des épreuves EN PLUS, la liste change, où que l'erreur ait été avalée.
# (2) LE MILIEU : la place libre est mesurée PENDANT la série (un fil, toutes les PAS_DE_SURVEILLANCE_S secondes) et
#     son minimum jugé contre PLANCHER_MO. Pourquoi 1024 Mo : le disque plein (0 Mo) a été vu ; un lot HL écrit environ
#     2,4 Go (mesuré le 04-11-2026) ; sous 1 Go, la marge entre deux mesures n'est plus sûre. Le plancher ne se baisse
#     jamais : la variable SERIE_PLANCHER_MO ne peut que le RELEVER (les épreuves s'en servent pour simuler un disque
#     presque plein sans le remplir).
PLANCHER_MO = 1024
PAS_DE_SURVEILLANCE_S = 0.5
# UN LOT COMPTÉ PORTE SA PLACE (superviseur R-759 du 05-11-2026, 17h13, tour 3, B-2 : « `lot_NN.place` (le minimum
# pendant ce lot) est écrit AVANT `lot_NN.code`, qui sert de marque de fin. Le minimum de la série = le minimum sur
# tous les lots. Un `.code` sans `.place` = NON CONFORME. Cela REMPLACE la note unique du `finally` »). Raison : la
# relecture du tour 2 (B-2) a coupé une série par SIGKILL — ce que fait un garde-disque — après un lot joué disque
# plein ; le `finally` qui notait le minimum n'a pas tourné, la reprise a mesuré une place redevenue normale, et le
# faux « mord » est sorti CONFORME. Un fichier par lot, écrit avant la marque de fin, ne peut pas manquer à un lot fini.
SUFFIXE_DE_LA_PLACE = "place"
# Les mesures en cours, par dossier de travail : le fil de `surveiller_la_place` y ajoute, `jouer_un_lot` y lit le
# minimum de SON lot. Une seule implémentation pour la machine et pour les parts de GitHub (R-708).
_MESURES_EN_COURS = {}
# LES FICHIERS TEMPORAIRES D'UN LOT VIVENT SUR LE DISQUE MESURÉ (superviseur R-759 du 05-11-2026, tour 3, M-1 :
# « TMPDIR, TMP et TEMP sont forcés DANS le dossier de travail pour chaque lot. Au départ, refus si
# st_dev(gettempdir()) ≠ st_dev(travail) »). Raison : la relecture du tour 2 (M-1) a mis TMPDIR sur un petit disque
# plein ; le témoin de la place mesurait le dossier de travail, sur un autre disque, et le faux « mord » est sorti
# CONFORME. Une propriété plutôt qu'une liste de disques à mesurer : tout ce qu'un enfant écrit en temporaire tombe
# sur le disque que le fil mesure.
VARIABLES_DU_TEMPORAIRE = ("TMPDIR", "TMP", "TEMP")
LIGNE_JOUE_PAR = "joué par : "   # la ligne d'en-tête qui dit où la série a été jouée (N2) ; le comparateur l'écarte


def heure():
    """Rend l'heure de Paris, « HHhMM ».

    ① RÔLE — Dater les repères. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte. [rend: 1] ⑥ TRAITEMENT — datetime. ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Les repères sont lus pendant des heures. ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return datetime.datetime.now(PARIS).strftime("%Hh%M")


def dossiers_d_ecoute(travail):
    """Rend {variable d'environnement : dossier} des flux de l'écoute et du module, pour un dossier de travail.

    ① RÔLE — Dire, en un seul endroit, où l'écoute écrit. ② CONTEXTE D'APPEL — `preparer_le_travail`, `jouer_un_lot`,
    `main` ; tests/outils/jouer_une_part.py et tests/outils/rassembler_les_parts.py (par `preparer_le_travail`).
    ③ ENTRÉE — `travail` : le dossier de travail. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire, PYTHONPATH (le module) puis chaque flux de FLUX_D_ECOUTE. [rend: 1]
    ⑥ TRAITEMENT — chemins joints. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, ⑧ (préparation recopiée qui a divergé).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = {"PYTHONPATH": os.path.join(travail, MODULE_D_ECOUTE)}
    d.update({v: os.path.join(travail, n) for v, n in FLUX_D_ECOUTE.items()})
    return d


def preparer_le_travail(travail):
    """Crée le module d'écoute et le dossier de chaque flux dans un dossier de travail.

    ① RÔLE — La seule préparation du dossier de travail. ② CONTEXTE D'APPEL — `main` ; tests/outils/jouer_une_part.py
    (avant ses lots) ; tests/outils/rassembler_les_parts.py (dossier réuni). ③ ENTRÉE — `travail`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur. [rend: 0] ⑥ TRAITEMENT — chaque dossier de
    `dossiers_d_ecoute` créé ; ECOUTE écrit en sitecustomize.py dans celui du module. ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ⑧ : le module ouvre un fichier dans chaque flux au démarrage ; un dossier absent le
    fait planter, et l'écoute devient sourde. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans `travail`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    for dossier in dossiers_d_ecoute(travail).values():
        os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossiers_d_ecoute(travail)["PYTHONPATH"], "sitecustomize.py"), "w") as s:
        s.write(ECOUTE)


def decouper(noms, taille):
    """Découpe la liste des sabotages en lots.

    ① RÔLE — Le seul découpage : même numéro et même contenu de lot partout. ② CONTEXTE D'APPEL — `main` ;
    tests/outils/jouer_une_part.py, tests/outils/rassembler_les_parts.py. ③ ENTRÉE — `noms` : les sabotages dans
    l'ordre du dictionnaire ; `taille` : lot maximal. ④ CONDITIONS D'ENTRÉE — taille >= 1. ⑤ SORTIE — UNE valeur :
    la liste des lots, le lot k à l'indice k-1. [rend: 1] ⑥ TRAITEMENT — tranches successives. ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relevé range les lignes par numéro de lot ; la part le recopiait (R-708). ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return [noms[i:i + taille] for i in range(0, len(noms), taille)]


def trace_d_erreur_systeme(texte):
    """Rend la première ligne d'un texte qui porte une trace d'erreur système, ou None.

    ① RÔLE — Dire si la sortie d'un lot montre que la MACHINE a failli (disque plein, fichier refusé…), pas l'épreuve.
    ② CONTEXTE D'APPEL — `main`, pour chaque lot ; tests/outils/jouer_une_part.py (à l'écran, fin de part).
    ③ ENTRÉE — `texte` : la sortie d'un lot. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la ligne (coupée à 160 caractères), ou None. [rend: 1]
    ⑥ TRAITEMENT — TRACE_SYSTEME cherché ligne à ligne. ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ⑧ : un disque plein a donné un faux « mord ». ⑨ CE QUI CLOCHE — Fiche en tête, ⑨
    (sur-détection voulue). ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    for l in texte.splitlines():
        if TRACE_SYSTEME.search(l):
            return l.strip()[:160]
    return None


def plancher_mo():
    """Rend le plancher de place libre, en Mo.

    ① RÔLE — Dire, en un seul endroit, sous quelle place libre une série n'est plus sûre.
    ② CONTEXTE D'APPEL — `main` (jugement) ; `ligne_joue_par`.
    ③ ENTRÉE — La variable d'environnement SERIE_PLANCHER_MO, facultative.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un entier, jamais sous PLANCHER_MO. [rend: 1]
    ⑥ TRAITEMENT — le plus grand de PLANCHER_MO et de la variable (ignorée si elle n'est pas un entier).
    ⑦ UNITÉ — Mo (2**20 octets).
    ⑧ POURQUOI — Commentaire de PLANCHER_MO : la variable sert aux épreuves à simuler un disque presque plein ; elle ne
      peut pas baisser le plancher, donc pas éteindre le témoin.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        return max(PLANCHER_MO, int(os.environ.get("SERIE_PLANCHER_MO", "0")))
    except ValueError:
        return PLANCHER_MO


def place_libre_mo(dossier):
    """Rend la place libre du disque qui porte `dossier`, en Mo.

    ① RÔLE — La seule mesure de la place libre (R-708 : la part la mesurait à part, elle appelle désormais celle-ci).
    ② CONTEXTE D'APPEL — `surveiller_la_place` ; tests/outils/jouer_une_part.py (début et fin de part).
    ③ ENTRÉE — `dossier` : un dossier existant.
    ④ CONDITIONS D'ENTRÉE — Il existe.
    ⑤ SORTIE — UNE valeur : un entier. [rend: 1]
    ⑥ TRAITEMENT — shutil.disk_usage.
    ⑦ UNITÉ — Mo (2**20 octets).
    ⑧ POURQUOI — Commentaire de PLANCHER_MO, témoin (2).
    ⑨ CE QUI CLOCHE — Mesure le disque entier : un autre programme qui écrit sur le même disque compte aussi (voulu :
      c'est la place que l'épreuve avait).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return shutil.disk_usage(dossier).free // 2**20


def lire_la_place(travail):
    """Rend le minimum de place libre sur TOUS les lots comptés d'un dossier de travail, ou None.

    ① RÔLE — Relire le témoin du milieu : la place la plus basse vue pendant un lot compté.
    ② CONTEXTE D'APPEL — `main` (jugement contre le plancher) ; tests/outils/jouer_une_part.py (part.json) et
      tests/outils/rassembler_les_parts.py (chaque part doit avoir la sienne).
    ③ ENTRÉE — `travail` : un dossier de travail ou d'une part.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un entier, ou None si aucun lot n'est compté, ou si UN lot compté (« lot_NN.code ») n'a
      pas son « lot_NN.place » lisible comme un entier. [rend: 1]
    ⑥ TRAITEMENT — pour chaque « lot_NN.code » du dossier, lire « lot_NN.place » ; rendre le minimum.
    ⑦ UNITÉ — Mo.
    ⑧ POURQUOI — Commentaire de SUFFIXE_DE_LA_PLACE (B-2 du tour 2) : « Un `.code` sans `.place` = NON CONFORME. »
      None se distingue d'une valeur : `main` juge None sous le plancher, le rassembleur refuse la part (2).
    ⑨ CE QUI CLOCHE — La place d'un lot repris est celle de son passage d'origine, pas une nouvelle mesure (voulu : c'est
      la place que ses épreuves ont eue).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        fins = sorted(f for f in os.listdir(travail) if re.fullmatch(r"lot_\d+\.code", f))
    except OSError:
        return None
    places = []
    for f in fins:
        try:
            places.append(int(open(os.path.join(travail, f[:-len("code")] + SUFFIXE_DE_LA_PLACE),
                                   encoding="utf-8").read().strip()))
        except (OSError, ValueError):
            return None
    return min(places) if places else None


def refus_du_disque_temporaire(travail):
    """Rend la raison de refuser une série dont le temporaire n'est pas sur le disque du dossier de travail, ou None.

    ① RÔLE — La garde de départ de M-1 : le fil ne mesure qu'un disque, celui du dossier de travail.
    ② CONTEXTE D'APPEL — `main` et tests/outils/jouer_une_part.py, avant tout lot (R-708 : une seule écriture).
    ③ ENTRÉE — `travail` : le dossier de travail, existant.
    ④ CONDITIONS D'ENTRÉE — `travail` existe.
    ⑤ SORTIE — UNE valeur : None si `tempfile.gettempdir()` et `travail` sont sur le même système de fichiers
      (st_dev) ; sinon le texte de la raison. [rend: 1]
    ⑥ TRAITEMENT — os.stat des deux, comparaison de st_dev.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de VARIABLES_DU_TEMPORAIRE (M-1 du tour 2).
    ⑨ CE QUI CLOCHE — Ne voit pas un programme qui écrit dans un chemin écrit en dur (« /tmp », /dev/shm) ; les inodes
      ne sont pas mesurés (BACKLOG, superviseur du tour 3).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    temporaire = tempfile.gettempdir()
    if os.stat(temporaire).st_dev != os.stat(travail).st_dev:
        return (f"le dossier temporaire {temporaire} n'est pas sur le disque du dossier de travail {travail} : la place "
                "libre mesurée ne serait pas celle où les épreuves écrivent (poser TMPDIR sur ce disque)")
    return None


@contextlib.contextmanager
def surveiller_la_place(travail):
    """Mesure la place libre PENDANT ce que l'on fait sous ce bloc, et en garde le minimum.

    ① RÔLE — Le témoin du milieu (2) : le creux de place libre pendant les lots, pas seulement au début et à la fin.
    ② CONTEXTE D'APPEL — `main` (autour des lots et du compte) ; tests/outils/jouer_une_part.py (autour de ses lots).
      Une seule implémentation pour la machine locale et pour GitHub (R-708).
    ③ ENTRÉE — `travail` : le dossier de travail (la mesure porte sur son disque).
    ④ CONDITIONS D'ENTRÉE — `travail` existe.
    ⑤ SORTIE — Aucune valeur (bloc « with »). [rend: 0]
    ⑥ TRAITEMENT — une mesure au départ ; un fil qui mesure toutes les PAS_DE_SURVEILLANCE_S secondes, dans la liste
      _MESURES_EN_COURS[travail] que `jouer_un_lot` lit pour écrire la place de SON lot ; à la sortie du bloc, le fil
      s'arrête et la liste est retirée. Rien n'est noté ici (tour 3, B-2 : la note unique de la sortie du bloc ne
      tournait pas sous SIGKILL ; chaque lot écrit désormais sa place avant sa marque de fin).
    ⑦ UNITÉ — Mo ; secondes (le pas).
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026, M1 (2) : « On mesure le MINIMUM de place libre au fil de la part
      (fil de surveillance), et on le juge contre un plancher. » Commentaire de SUFFIXE_DE_LA_PLACE.
    ⑨ CE QUI CLOCHE — Un creux plus court que le pas n'est pas vu : c'est le témoin (1), la raison, qui le rattrape s'il
      a fait tomber une épreuve. Une erreur de mesure dans le fil (disque démonté) arrête le fil ; les lots suivants
      n'ont alors que leurs mesures de début et de fin. Un seul bloc à la fois par dossier de travail.
    ⑩ EFFET — Un fil de plus pendant le bloc ; une entrée de _MESURES_EN_COURS.
    ⑪ TERMINAISON — Le fil s'arrête à la sortie du bloc (attendu au plus un pas). [sort: non]
    """
    cle = os.path.realpath(travail)
    mesures = [place_libre_mo(travail)]
    _MESURES_EN_COURS[cle] = mesures
    fin = threading.Event()

    def guetter():
        while not fin.wait(PAS_DE_SURVEILLANCE_S):
            try:
                mesures.append(place_libre_mo(travail))
            except OSError:
                return

    fil = threading.Thread(target=guetter, daemon=True)
    fil.start()
    try:
        yield
    finally:
        fin.set()
        fil.join()
        _MESURES_EN_COURS.pop(cle, None)


def raison_d_une_ligne(ligne):
    """Rend (nom du sabotage, raison) pour une ligne de résultat, ou None si ce n'en est pas une.

    ① RÔLE — Lire la RAISON d'un sabotage : son verdict et les épreuves qu'il fait tomber.
    ② CONTEXTE D'APPEL — `raisons_des_lignes`.
    ③ ENTRÉE — `ligne` : une ligne de sortie d'épreuve ou de relevé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None, ou (nom, (verdict, épreuves)) ; « épreuves » est la suite triée des premiers mots des
      éléments de la liste écrite après le verdict (« ['H8', 'H31'] » → H31, H8 ; « ["E2 (code 0, …)"] » → E2) ; si la
      liste n'est pas lisible, la suite d'un seul élément « texte : <reste de la ligne> ». [rend: 1]
    ⑥ TRAITEMENT — LIGNE (le format du relevé, R-708) ; le reste, depuis le premier « [ », lu par ast.literal_eval.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de PLANCHER_MO, témoin (1). Les quatre formats des relevés du dépôt (HL « mord : ['H8'] »,
      Yahoo « mord ["E2 (…)"] », boucle de check, arrivée des signaux) portent tous la liste après le verdict ; le
      premier mot d'un élément est le nom de l'épreuve tombée (le reste — l'écran, un compte d'octets — n'est pas la
      raison).
    ⑨ CE QUI CLOCHE — Une épreuve qui écrirait autre chose qu'une liste a une raison « texte » : comparée au mot près,
      elle sur-détecte (le relevé passe « à examiner »), jamais l'inverse.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    m = LIGNE.match(ligne)
    if not m:
        return None
    reste = ligne[m.end():]
    i = reste.find("[")
    try:
        liste = ast.literal_eval(reste[i:].strip()) if i >= 0 else None
    except (ValueError, SyntaxError):
        liste = None
    if isinstance(liste, list):
        tombees = tuple(sorted({(str(e).split() or [""])[0] for e in liste}))
    else:
        tombees = ("texte : " + reste.strip(),)
    return m.group(1), (m.group(2), tombees)


def raisons_des_lignes(lignes):
    """Rend {nom du sabotage : raison} pour des lignes de résultat.

    ① RÔLE — Les raisons d'une série entière.
    ② CONTEXTE D'APPEL — `main` : les lignes des lots joués, et celles du relevé retenu.
    ③ ENTRÉE — `lignes` : des lignes de texte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire ; un nom vu deux fois garde sa dernière raison (les doubles sont jugés
      ailleurs, dans `main`). [rend: 1]
    ⑥ TRAITEMENT — `raison_d_une_ligne` sur chaque ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de PLANCHER_MO, témoin (1).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    raisons = {}
    for l in lignes:
        r = raison_d_une_ligne(l)
        if r:
            raisons[r[0]] = r[1]
    return raisons


def prefixe_de_la_serie(releve):
    """Rend le début commun des noms des relevés d'une même série : le nom sans sa date, ou le nom entier.

    ① RÔLE — Dire, en un seul endroit, quels fichiers sont les relevés d'une même série (R-708).
    ② CONTEXTE D'APPEL — `anciens_releves`, `etat_du_depart`.
    ③ ENTRÉE — `releve` : un chemin de relevé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte ; égal au nom du fichier s'il ne porte pas de date. [rend: 1]
    ⑥ TRAITEMENT — retire « _Jjj_JJ-MM-AAAA_HHhMM.txt » de la fin du nom, en gardant le « _ ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule version vivante d'un relevé, à la date près.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return re.sub(r"_[A-Z][a-z]{2}_\d{2}-\d{2}-\d{4}_\d{2}h\d{2}\.txt$", "_", os.path.basename(releve))


def etat_du_depart(racine, releve):
    """Rend l'empreinte du dépôt au départ d'une série, sans les relevés de cette série ni leurs archives.

    ① RÔLE — L'état que la reprise et la fin de série comparent.
    ② CONTEXTE D'APPEL — `main` ; tests/outils/jouer_une_part.py (le départ de chaque part, comparé au rassemblement).
    ③ ENTRÉE — `racine` ; `releve` : le chemin relatif du relevé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {chemin relatif : sha256}. [rend: 1]
    ⑥ TRAITEMENT — `etat_du_depot`, sans le relevé et sans tout fichier dont le nom commence par le préfixe de la
      série (`prefixe_de_la_serie`) quand le relevé porte une date : le relevé retenu, les relevés « à examiner », leurs
      archives (« <nom>_REMPLACE_PAR_<nouveau> »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relevé change à chaque série (règle d'origine) ; depuis le témoin de la raison (05-11-2026), la
      reprise d'une série « à examiner » avec --raisons-acceptees doit trouver le dépôt « inchangé » alors que
      l'écriture du premier relevé a rangé le relevé retenu dans archives/ (mesuré : ARRET, code 2, sans cela).
    ⑨ CE QUI CLOCHE — Une épreuve qui LIRAIT un relevé de sa propre série n'en verrait pas le changement ici (aucune
      ne le fait au 05-11-2026).
    ⑩ EFFET — Lit tout le dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    etat = etat_du_depot(racine)
    etat.pop(releve, None)
    prefixe = prefixe_de_la_serie(releve)
    if prefixe != os.path.basename(releve):
        etat = {c: e for c, e in etat.items() if not c.rsplit("/", 1)[-1].startswith(prefixe)}
    return etat


def anciens_releves(racine, releve):
    """Rend les relevés de la même série que `releve` (même nom à la date près), autres que lui, triés.

    ① RÔLE — Trouver, en un seul endroit, les relevés de la même série (R-708).
    ② CONTEXTE D'APPEL — `main` (le relevé retenu ; le rangement des anciens) ; tests/outils/ranger_le_releve.py.
    ③ ENTRÉE — `racine` ; `releve` : chemin relatif du nouveau relevé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms de fichiers (dans le dossier du relevé), triée ; vide si le nom ne porte
      pas de date ou si le dossier manque. [rend: 1]
    ⑥ TRAITEMENT — le préfixe = le nom sans « _Jjj_JJ-MM-AAAA_HHhMM.txt » ; les fichiers du dossier qui commencent par
      lui. Le DERNIER RELEVÉ RETENU est le seul (une seule version vivante) ou, à défaut, le dernier par ordre de nom.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le code d'origine vivait dans `main` (rangement dans archives/) ; le rangeur et le témoin de la raison
      en ont besoin aussi.
    ⑨ CE QUI CLOCHE — L'ordre des noms n'est pas l'ordre des dates (jour de la semaine en tête) : s'il y en a plusieurs,
      ce qui contredit « une seule version vivante », le choix est arbitraire ; `main` le dit.
    ⑩ EFFET — Lit un dossier.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    prefixe = prefixe_de_la_serie(releve)
    dossier = os.path.join(racine, os.path.dirname(releve))
    if prefixe == os.path.basename(releve) or not os.path.isdir(dossier):
        return []
    return sorted(a for a in os.listdir(dossier) if a.startswith(prefixe) and a != os.path.basename(releve))


def ranger_les_anciens_releves(racine, releve):
    """Range dans archives/ les relevés de la même série que `releve`, sous un nom qui dit pourquoi.

    ① RÔLE — Une seule version vivante d'un relevé.
    ② CONTEXTE D'APPEL — `main`, avant d'écrire le relevé ; tests/outils/ranger_le_releve.py.
    ③ ENTRÉE — `racine` ; `releve` : chemin relatif du nouveau relevé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms rangés. [rend: 1]
    ⑥ TRAITEMENT — chaque nom de `anciens_releves` déplacé en archives/<nom sans .txt>_REMPLACE_PAR_<nouveau>.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Règle du dépôt : l'ancienne version va en archives/, sous un nom qui dit pourquoi.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Déplace des fichiers ; crée archives/ s'il manque.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    ranges = []
    for ancien in anciens_releves(racine, releve):
        os.makedirs(os.path.join(racine, "archives"), exist_ok=True)
        os.replace(os.path.join(racine, os.path.dirname(releve), ancien), os.path.join(
            racine, "archives", ancien[:-4] + "_REMPLACE_PAR_" + os.path.basename(releve)))
        ranges.append(ancien)
    return ranges


def raisons_a_examiner(retenues, nouvelles, acceptees):
    """Rend les différences de raison entre le relevé retenu et la série jouée, hors celles acceptées.

    ① RÔLE — Le témoin de la raison (1).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `retenues` : {nom : raison} du dernier relevé retenu ({} s'il n'y en a pas) · `nouvelles` : celles de la
      série jouée · `acceptees` : les noms dont la nouvelle raison a été acceptée (option --raisons-acceptees).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (changés, nouveaux, disparus) ; changés : {nom : (raison retenue, raison jouée)} ;
      nouveaux et disparus : listes triées de noms. [rend: 1]
    ⑥ TRAITEMENT — comparaison nom à nom ; un nom accepté sort des trois.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026, M1 (1) : « Toute différence, toute épreuve tombée en plus, tout
      sabotage nouveau ou modifié est listé. Le relevé reste « à examiner » tant que ces différences ne sont pas
      tranchées. » Trancher appartient à Jean-Luc ; la décision s'écrit par --raisons-acceptees, et le relevé la porte.
    ⑨ CE QUI CLOCHE — Un sabotage dont le CODE change sans changer sa raison n'est pas vu ici (l'empreinte de l'épreuve,
      au relevé, le dit).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    changes = {n: (retenues[n], r) for n, r in nouvelles.items()
               if n in retenues and retenues[n] != r and n not in acceptees}
    nouveaux = sorted(n for n in nouvelles if n not in retenues and n not in acceptees)
    disparus = sorted(n for n in retenues if n not in nouvelles and n not in acceptees)
    return changes, nouveaux, disparus


def ligne_joue_par(racine, place):
    """Rend la ligne d'en-tête « joué par : … » d'un relevé.

    ① RÔLE — Dire où, avec quoi et sur quel commit une série a été jouée (relecture du 05-11-2026, N2).
    ② CONTEXTE D'APPEL — `main`, à l'écriture du relevé.
    ③ ENTRÉE — `racine` ; `place` : le minimum de place libre, en Mo. Variables d'environnement : GITHUB_ACTIONS,
      GITHUB_RUN_ID, GITHUB_RUN_ATTEMPT, SERIE_COMMIT (le commit éprouvé, posé par le circuit, lu SEULEMENT si
      GITHUB_ACTIONS vaut « true »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, sans le « # ». [rend: 1]
    ⑥ TRAITEMENT — machine (« GitHub » ou « machine locale ») ; version de Python ; commit : sur GitHub,
      SERIE_COMMIT ; sinon `git rev-parse HEAD` de la racine si elle est un dépôt git, suivi de « MODIFIÉ » si
      `git status --porcelain` n'est pas vide ou n'a pas pu être lu ; sinon « inconnu » ; passage ; place minimale
      et plancher.
    ⑦ UNITÉ — Mo.
    ⑧ POURQUOI — Le rangeur (tests/outils/ranger_le_releve.py) exige que ce commit soit la pointe de la version
      éprouvée ; GitHub joue en 3.11, la machine en 3.13 : la ligne le dit. Le comparateur l'écarte, comme la ligne 3.
      « Le relevé dit sur quel arbre il a été joué, et il le MESURE » (superviseur R-759 du 05-11-2026, tour 3,
      M-4) : la relecture du tour 2 a rangé un relevé joué sur un arbre modifié non commité, et un relevé dont le
      commit venait de SERIE_COMMIT posé à la main sur la machine. Sur GitHub, le circuit compare déjà le commit
      cloné à celui de la préparation (pas « meme_depot »), et la copie jouée n'a pas de .git.
    ⑨ CE QUI CLOCHE — Une copie sans .git jouée hors du circuit dit « commit inconnu » : le rangeur la refuse. Le
      dossier de travail de la série, s'il est DANS la racine, rend l'arbre « MODIFIÉ » (voulu : il doit être hors du
      dépôt, fiche en tête ③). GITHUB_ACTIONS posé à la main sur la machine contourne encore la mesure (la ligne
      dirait alors « GitHub », que `--calibrage` du comparateur confronte à la machine).
    ⑩ EFFET — Lance git deux fois au plus.
    ⑪ TERMINAISON — Rend la main ; chaque git est borné à 30 s. [sort: non]
    """
    sur_github = os.environ.get("GITHUB_ACTIONS") == "true"
    commit = os.environ.get("SERIE_COMMIT", "").strip() if sur_github else ""
    if not commit and os.path.lexists(os.path.join(racine, ".git")):
        try:
            r = subprocess.run(["git", "-C", racine, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=30)
            commit = r.stdout.strip() if r.returncode == 0 else ""
            s = subprocess.run(["git", "-C", racine, "status", "--porcelain"], capture_output=True, text=True, timeout=30)
            if commit and (s.returncode != 0 or s.stdout.strip()):
                commit += " MODIFIÉ"
        except (OSError, subprocess.SubprocessError):
            commit = ""
    machine = "GitHub" if sur_github else "machine locale"
    passage = (os.environ.get("GITHUB_RUN_ID", "") + "." + os.environ.get("GITHUB_RUN_ATTEMPT", "")).strip(".") or "—"
    return (f"{LIGNE_JOUE_PAR}{machine} ; Python {platform.python_version()} ; commit {commit or 'inconnu'} ; "
            f"passage {passage} ; place libre minimale {place} Mo (plancher {plancher_mo()} Mo)")


def etat_du_depot(racine):
    """Rend l'empreinte de chaque fichier du dépôt, sans .git ni __pycache__.

    ① RÔLE — Fixer l'état de départ, pour la reprise et pour la vérification de fin. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le dépôt. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : {chemin relatif : sha256}.
    [rend: 1] ⑥ TRAITEMENT — os.walk. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête, ⑥ ②.
    ⑨ CE QUI CLOCHE — Les liens symboliques sont suivis comme des fichiers. ⑩ EFFET — Lit tout le dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    etat = {}
    for r, ds, fs in os.walk(racine):
        ds[:] = [d for d in ds if d not in (".git", "__pycache__")]
        for f in fs:
            p = os.path.join(r, f)
            if os.path.isfile(p):
                etat[os.path.relpath(p, racine).replace(os.sep, "/")] = SERIE.empreinte(p)
    return etat


def jouer_un_lot(racine, epreuve, travail, k, lot):
    """Joue un lot de sabotages ; rend (k, code).

    ① RÔLE — Un morceau de la série, repris s'il est déjà fait. ② CONTEXTE D'APPEL — `main`, en parallèle.
    ③ ENTRÉE — `racine`, `epreuve` (relative), `travail` : le dossier de travail · `k` : le numéro du lot · `lot` : ses
      noms. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (k, code de l'épreuve), ou (k, None) si le lot est SOURD (un flux d'écoute du processus de
      l'épreuve ne nomme pas l'épreuve : aucun code écrit). [rend: 1]
    ⑥ TRAITEMENT — si lot_k.code existe, le relire ; sinon lancer l'épreuve écoutée (`dossiers_d_ecoute`), sans la
      configuration git de la machine (`CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE`), avec TMPDIR, TMP et TEMP
      dans « tmp_lot_NN » du dossier de travail (M-1), sortie dans lot_k.out.part puis renommée ; si chaque flux
      « <flux>/*.<pid de l'épreuve> » nomme l'épreuve : d'abord lot_k.place (le minimum des mesures du fil pendant le
      lot, et des mesures de début et de fin du lot), PUIS lot_k.code, la marque de fin (B-2). L'épreuve jouée ne
      reçoit AUCUNE variable de FABRICANT.FICHIERS_DE_COMMANDES_DE_GITHUB (GITHUB_ENV, GITHUB_PATH, GITHUB_OUTPUT,
      GITHUB_STATE, GITHUB_STEP_SUMMARY, BASH_ENV : la liste est lue là, pas recopiée).
      ⑦ UNITÉ — Mo (la place). ⑧ POURQUOI — Voir la fiche en tête (⑥ ④, ⑧). Sans la configuration git : cassure N de
      Cowork, 17-10-2026 — le relevé était écrit dans un autre environnement que celui où la nuit le rejoue. La place
      avant la marque : commentaire de SUFFIXE_DE_LA_PLACE. Le temporaire : commentaire de VARIABLES_DU_TEMPORAIRE.
      Les fichiers de commandes de GitHub retirés (tour 6, relecture neuve du tour 5, R5-4 ; mesure jugée par le
      superviseur R-759 du 06-11-2026 « suffisante contre l'accident, peu coûteuse ») : sur GitHub, une épreuve jouée
      (ou un programme saboté qu'elle lance) qui écrirait par mégarde dans le vrai $GITHUB_ENV agirait sur le pas
      « deposer » suivant, celui qui tient le jeton.
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨ (numéro de processus repris). Hors d'un bloc `surveiller_la_place`, la place du
      lot n'a que ses deux mesures, de début et de fin. Le dossier « tmp_lot_NN » n'est pas effacé (il sert à la
      lecture d'un lot raté). Le retrait des fichiers de commandes de GitHub protège de l'ACCIDENT, pas d'un code
      écrit pour nuire : celui-ci retrouve le fichier par son dossier (« _runner_file_commands », même utilisateur).
      ⑩ EFFET — Écrit dans `travail` ; lance l'épreuve.
    ⑪ TERMINAISON — Attend la fin de l'épreuve, sans délai. [sort: non]
    """
    fin = os.path.join(travail, f"lot_{k:02d}.code")
    if os.path.exists(fin):
        return k, int(open(fin).read().strip())
    mesures = _MESURES_EN_COURS.get(os.path.realpath(travail), [])
    debut_des_mesures = len(mesures)
    place_au_debut = place_libre_mo(travail)
    sortie = os.path.join(travail, f"lot_{k:02d}.out")
    temporaire = os.path.join(travail, f"tmp_lot_{k:02d}")
    os.makedirs(temporaire, exist_ok=True)
    env = dict(os.environ, PYTHONUNBUFFERED="1", **dossiers_d_ecoute(travail))
    env.update({v: temporaire for v in VARIABLES_DU_TEMPORAIRE})
    env.update(CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)   # l'environnement où la nuit refait les essais
    for v in FABRICANT.FICHIERS_DE_COMMANDES_DE_GITHUB:          # tour 6, R5-4 : contre l'ACCIDENT seulement
        env.pop(v, None)
    programme = os.path.join(racine, epreuve)
    with open(sortie + ".part", "w", encoding="utf-8") as s:
        p = subprocess.Popen([sys.executable, "-u", programme, racine, "--saboter=" + ",".join(lot)],
                             cwd=racine, env=env, stdout=s, stderr=subprocess.STDOUT)
        code = p.wait()
    os.replace(sortie + ".part", sortie)
    # Chaque flux de l'écoute de CE processus doit nommer l'épreuve : sinon le lot n'a rien entendu (fiche en tête, ⑧).
    noms_de_l_epreuve = {programme, os.path.realpath(programme)}
    for v, n in FLUX_D_ECOUTE.items():
        dossier = env[v]
        lignes = set()
        for f in os.listdir(dossier) if os.path.isdir(dossier) else []:
            if f.endswith(f".{p.pid}"):
                lignes.update(open(os.path.join(dossier, f), encoding="utf-8", errors="replace").read().splitlines())
        if not lignes & noms_de_l_epreuve:
            print(f"ERREUR {heure()} lot {k} SOURD : le flux « {n} » de l'écoute ne nomme pas l'épreuve "
                  f"(code {code} non écrit)", flush=True)
            return k, None
    place = min(mesures[debut_des_mesures:] + [place_au_debut, place_libre_mo(travail)])
    with open(os.path.join(travail, f"lot_{k:02d}.{SUFFIXE_DE_LA_PLACE}"), "w", encoding="utf-8") as f:
        f.write(str(place))
    open(fin, "w").write(str(code))
    print(f"ETAPE {heure()} lot {k} fini, code {code} ({len(lot)} sabotages)", flush=True)
    return k, code


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — Voir la fiche en tête. ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(pos) != 3:
        print("ARRET usage : JOUER_UNE_SERIE_DE_SABOTAGES.py <racine> <épreuve> <relevé> [--parts=2] [--lot=21] [--travail=…]")
        return 2
    racine, epreuve, releve = os.path.realpath(pos[0]), pos[1], pos[2]
    parts, taille = int(opt.get("parts", 2)), int(opt.get("lot", 21))
    travail = os.path.realpath(opt.get("travail", os.path.join(racine, "..", "serie_" + os.path.basename(epreuve)[:-3])))
    # les raisons nouvelles acceptées par Jean-Luc (témoin de la raison) : des noms de sabotages, séparés par des virgules
    acceptees = sorted({n for n in opt.get("raisons-acceptees", "").split(",") if n})
    try:
        noms = SERIE.noms_des_sabotages(os.path.join(racine, epreuve))
    except (OSError, SyntaxError, ValueError) as e:
        print(f"ARRET épreuve {epreuve} illisible : {type(e).__name__} : {e}")
        return 2
    if not noms:
        print(f"ARRET aucun dictionnaire SABOTAGES lisible dans {epreuve}")
        return 2
    # LA PORTÉE DU RELEVÉ, lue à la table de lancement par le certificateur (R-708) ; une racine sans table (un dépôt
    # d'essai) garde la portée d'origine, « lectures ».
    try:
        portee = (CERTIF.options_de_lancement(racine)[1].get(epreuve) or {}).get("portee")
    except FileNotFoundError:
        portee = None
    except ValueError as e:
        print(f"ARRET table de lancement illisible : {e}")
        return 2
    portee = SERIE.PORTEE_LECTURES if portee is None else portee
    if portee not in SERIE.PORTEES:
        print(f"ARRET portée du relevé inconnue pour {epreuve} : {portee!r}")
        return 2
    preparer_le_travail(travail)
    refus = refus_du_disque_temporaire(travail)
    if refus:
        print("ARRET " + refus)
        return 2
    flux = dossiers_d_ecoute(travail)
    depart = os.path.join(travail, "etat_du_depart.json")
    etat = etat_du_depart(racine, releve)        # le relevé lui-même change à chaque série
    if os.path.exists(depart):
        avant = json.load(open(depart, encoding="utf-8"))
        # Seuls les fichiers présents au départ comptent : un dossier jetable laissé par un lot coupé n'empêche pas
        # la reprise (mesuré le 16-10-2026 sur un dépôt d'essai : le relevé écrit dans la racine la refusait).
        differents = [c for c, e in avant.items() if etat.get(c) != e]
        if differents:
            print(f"ARRET le dépôt a changé depuis le départ de cette série ({travail}) : {', '.join(differents[:5])} "
                  "— prendre un dossier de travail neuf")
            return 2
        etat = avant
        print(f"ETAPE {heure()} reprise : dépôt identique au départ, lots déjà faits gardés", flush=True)
    else:
        json.dump(etat, open(depart, "w", encoding="utf-8"))
        open(os.path.join(travail, "debut.txt"), "w").write(datetime.datetime.now(PARIS).strftime("%d-%m-%Y %Hh%M"))
    lots = decouper(noms, taille)
    print(f"ETAPE {heure()} {len(noms)} sabotages en {len(lots)} lots, {parts} à la fois", flush=True)
    # le témoin du milieu (2) : la place libre mesurée PENDANT les lots ; son minimum est jugé plus bas
    with surveiller_la_place(travail):
        with concurrent.futures.ThreadPoolExecutor(max_workers=parts) as g:
            codes = dict(g.map(lambda kl: jouer_un_lot(racine, epreuve, travail, *kl), enumerate(lots, 1)))
    sourds = sorted(k for k, c in codes.items() if c is None)
    if sourds:
        print(f"ARRET écoute sourde pour le(s) lot(s) {sourds} : impossible de dire ce qu'ils ont lu — relancer "
              "(ces lots seront rejoués)")
        return 2
    # ⑤ le compte : chaque sabotage une fois, « mord » ; ④ter un lot en erreur système ne compte aucun « mord »
    vus, lignes, z0, en_erreur = {}, [], [], {}
    for k in range(1, len(lots) + 1):
        try:
            sortie_du_lot = open(os.path.join(travail, f"lot_{k:02d}.out"), encoding="utf-8", errors="replace").read()
        except OSError:
            print(f"ARRET la sortie du lot {k} manque alors que son code est écrit : effacer lot_{k:02d}.code et relancer")
            return 2
        trace = trace_d_erreur_systeme(sortie_du_lot)
        if trace is not None:
            en_erreur[k] = trace
        for l in sortie_du_lot.splitlines():
            m = LIGNE.match(l)
            if m:
                vus.setdefault(m.group(1), []).append("ERREUR SYSTÈME" if trace is not None else m.group(2))
                lignes.append(l)
            elif l.startswith("Z0 "):
                z0.append(f"lot {k} : {l}")
    # ④quater le témoin de la raison (1) : chaque sabotage doit faire tomber les MÊMES épreuves que dans le dernier
    # relevé retenu de la même série ; sinon il ne compte pas « mord » et le relevé est « à examiner »
    # Seul un relevé CONFORME est « retenu » : les lignes d'un relevé « à examiner » portent les raisons NON tranchées
    # (rejouer sous un autre nom les ferait passer pour retenues).
    retenus = []
    for a in anciens_releves(racine, releve):
        with open(os.path.join(racine, os.path.dirname(releve), a), encoding="utf-8", errors="replace") as f:
            texte_retenu = f.read().splitlines()
        if texte_retenu and texte_retenu[-1] == SERIE.VERDICT_CONFORME:
            retenus.append((a, texte_retenu))
    retenues = raisons_des_lignes(retenus[-1][1]) if retenus else {}
    retenus = [a for a, _ in retenus]
    changes, nouveaux, disparus = raisons_a_examiner(retenues, raisons_des_lignes(lignes), set(acceptees))
    for n in list(changes) + nouveaux:
        vus[n] = ["RAISON À EXAMINER" if v == "mord" else v for v in vus[n]]
    place = lire_la_place(travail)
    sous_le_plancher = place is None or place < plancher_mo()
    manquent = [n for n in noms if n not in vus]
    doubles = [n for n, v in vus.items() if len(v) != 1]
    ne_mordent_pas = [n for n, v in vus.items() if v != ["mord"]]
    lots_rouges = [k for k, c in codes.items() if c != 0]
    if manquent:
        print(f"ERREUR {len(manquent)} sabotage(s) sans résultat : {', '.join(manquent[:8])}")
    # les fichiers lus : notés par l'écoute ET présents au départ (pas les dossiers jetables)
    lus = set()
    for f in os.listdir(flux["SERIE_ECOUTE"]):
        for p in open(os.path.join(flux["SERIE_ECOUTE"], f), encoding="utf-8", errors="replace").read().splitlines():
            if p.startswith(racine + os.sep):
                rel = os.path.relpath(p, racine).replace(os.sep, "/")
                m = re.match(r"^(.*/)?__pycache__/([^/.]+)\.[^/]+\.pyc$", rel)
                if m:
                    rel = (m.group(1) or "") + m.group(2) + ".py"
                if rel in etat:
                    lus.add(rel)
    # le code exécuté (portées « epreuve » et « code_execute ») : une propriété mesurée, ramenée au dépôt (R-708)
    executes = SERIE.fichiers_executes(flux["SERIE_EXECUTION"], etat)
    couverts = lus if portee == SERIE.PORTEE_LECTURES else executes
    # ④bis l'épreuve doit être couverte : sinon aucune écoute n'a rien entendu, même si tous les lots sont repris.
    if epreuve not in couverts:
        print(f"ARRET aucune écoute ne nomme l'épreuve {epreuve} (portée {portee}) : impossible de dire ce que la série "
              "a lu ou exécuté")
        return 2
    # Un fichier disparu pendant la série est un changement, pas un plantage (relecture indépendante, 17-10-2026, tour
    # 15 : un fichier lu, effacé par l'épreuve, faisait sortir le joueur sur une trace, code 1, au lieu d'ARRET).
    change = [c for c in sorted(couverts | {epreuve}) if not os.path.isfile(os.path.join(racine, c))
              or SERIE.empreinte(os.path.join(racine, c)) != etat.get(c)]
    if change:
        print(f"ARRET {len(change)} fichier(s) lu(s) ont changé pendant la série : {', '.join(change[:5])}")
        return 2
    conforme = not (manquent or doubles or ne_mordent_pas or lots_rouges or en_erreur or changes or nouveaux or disparus
                    or sous_le_plancher)
    examen = []
    if changes or nouveaux or disparus:
        examen.append(f"raisons à examiner, contre le relevé retenu {retenus[-1] if retenus else '(aucun)'} : "
                      f"{len(changes)} changée(s) {sorted(changes)[:20]} ; {len(nouveaux)} sabotage(s) nouveau(x) "
                      f"{nouveaux[:20]} ; {len(disparus)} disparu(s) {disparus[:20]} — ils ne comptent pas « mord » tant "
                      "que Jean-Luc n'a pas tranché (--raisons-acceptees=…)")
        for n, (avant, apres) in sorted(changes.items())[:20]:
            examen.append(f"raison changée {n} : retenue {avant[0]} {list(avant[1])} ; jouée {apres[0]} {list(apres[1])}")
    if len(retenus) > 1:
        examen.append(f"{len(retenus)} relevés retenus de la même série au lieu d'un : comparé au dernier par ordre de nom")
    if acceptees:
        examen.append(f"raisons nouvelles acceptées (--raisons-acceptees) : {acceptees}")
    if sous_le_plancher:
        examen.append(f"place libre minimale {place} Mo, sous le plancher de {plancher_mo()} Mo : série NON CONFORME "
                      "(un disque presque plein fait tomber des épreuves pour une autre raison que le sabotage)")
    entete = [f"série jouée du {open(os.path.join(travail, 'debut.txt')).read()} au "
              f"{datetime.datetime.now(PARIS):%d-%m-%Y %Hh%M} (Paris), {len(lots)} lots de {taille} au plus, {parts} à la fois,",
              f"par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py ; {len(noms)} sabotages attendus, {len(vus)} joués, "
              f"{sum(v == ['mord'] for v in vus.values())} mordent ; lots rouges : {lots_rouges or 'aucun'}",
              f"portée du relevé : {portee}" + ("" if portee == SERIE.PORTEE_LECTURES else
                                                 " — empreintes du code EXÉCUTÉ par la série (évènement « exec »), sans "
                                                 "les données ; la nuit compare " + ("le seul code de l'épreuve (décision "
                                                 "n°71 du 01-11-2026, lue au mot)" if portee == SERIE.PORTEE_EPREUVE else
                                                 "tout ce code (choix D43 du Chat du 05-11-2026, à confirmer par "
                                                 "Jean-Luc)"))] + ([
        f"lots en erreur système : {sorted(en_erreur)} — leurs sabotages ne comptent pas « mord » ; première trace : "
        f"{en_erreur[min(en_erreur)]}"] if en_erreur else []) + z0 + examen + [ligne_joue_par(racine, place)]
    # Une seule version vivante : l'ancien relevé de la même série va dans archives/, sous un nom qui dit pourquoi.
    for ancien in ranger_les_anciens_releves(racine, releve):
        print(f"ETAPE {heure()} ancien relevé rangé dans archives/ : {ancien}")
    n = SERIE.ecrire_le_releve(racine, releve, epreuve, sorted(couverts), lignes, conforme, entete)
    print(f"FINI {heure()} relevé {releve} : {len(vus)} sabotages, {n} empreintes, "
          f"{'conforme' if conforme else 'NON CONFORME'} ; place libre minimale {place} Mo (plancher {plancher_mo()} Mo)"
          + (f" ; raisons à examiner : {len(changes)} changée(s), {len(nouveaux)} nouveau(x), {len(disparus)} disparu(s)"
             if changes or nouveaux or disparus else ""), flush=True)
    return 0 if conforme else 1


if __name__ == "__main__":
    sys.exit(main())
