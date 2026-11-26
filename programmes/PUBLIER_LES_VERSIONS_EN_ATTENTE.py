#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUBLIER_LES_VERSIONS_EN_ATTENTE.py — Mer 25-11-2026 (Paris), version SIMPLE. Simulation uniquement : aucun ordre
réel, jamais.

LE SENS EN TÊTE. « Ce programme publie au dépôt public, sans geste humain, chaque version en attente (branche
travail-*) qui attend ses épreuves longues, avec le SEUL fabricant de main, puis dépose UNE demande au relais de main ;
il compte les échecs de chaque pointe et s'arrête au deuxième, avec une ligne rouge. Il sert à ce qu'aucune pièce du
chemin critique ne reste bloquée faute de publication. »
Décision de Jean-Luc A-1012, 25-11-2026 à 20h10 : « 1. GitHub, automatiquement ». La première version (archivée sous
archives/PUBLIER_LES_VERSIONS_EN_ATTENTE_V1_REMPLACE_PAR_LA_VERSION_SIMPLE_DU_SUPERVISEUR_R759_Mer_25-11-2026.py) a
été jugée « ARRÊTER ET SIMPLIFIER » par le superviseur R-759 du 25-11-2026 à 21h48 (echanges/
SUPERVISEUR_R759_DU_PILOTE.md) : elle exécutait le fabricant de la branche (code non relu) avec le jeton, devinait
le refus du relais à sa phrase, relançait un échec sans plafond et ouvrait une branche privée par passage.
Cette version applique la version simple du superviseur :
  ① seul le code de MAIN tourne : le fabricant et le module du jeton qu'il charge sont les octets posés à côté de ce
    fichier (main du public) ; une branche qui modifie l'un des deux « ATTEND L'INSTALLATION » ;
  ①bis (superviseur R-759, tour 2, Q2) le fabricant de main est lancé depuis un DOSSIER COMPOSÉ : programmes/ (ses
    octets de main) + tests/LANCEMENT_DES_EPREUVES.json DE LA BRANCHE. PROPRIÉTÉ : tout ce que le fabricant EXÉCUTE
    est l'octet de main ; tout ce qu'il LIT à côté de lui vient de la branche, comme une publication à la main. Ainsi
    le relais publié connaît les épreuves que la branche ajoute (défaut N-42 du RELU de Cowork du 25-11-2026 à 22h34 :
    6 branches sur 15 demandaient un code que le relais de main ne connaissait pas). Une table que le fabricant de
    main refuse → filet (Q1) : la table de main, et seuls les codes qu'elle connaît sont demandés ; s'il n'en reste
    aucun, « ATTEND L'INSTALLATION », jamais un échec compté ;
  ② au plus une demande en vol par pointe, au format du relais de main ; au plus UNE demande déposée par passage ;
  ③ mémoire des échecs par pointe : tout échec compte (publication refusée, demande refusée par le relais, passage
    terminé sans résultat) ; au deuxième, plus de tentative et une ligne rouge, une seule fois ;
  ④ un seul journal privé (branche fixe publication-auto/journal, rangée par le circuit) ; l'écran public ne porte
    que les branches déjà présentes au dépôt public, au vocabulaire fixe ;
  ⑤ seules comptent les branches dont la base contient le commit FILE-2 (le relais qui met en file, jamais ne refuse
    pour la charge).

① RÔLE — Pour chaque branche travail-* que programmes/ETAT_DES_TRAVAUX.py range « À ÉPROUVER » : constater l'issue
  de la tentative précédente (`constater`), décider (`decider`), et si oui publier et demander (`publier_la_branche`).
② CONTEXTE D'APPEL — Le circuit public circuits_publics_a_installer/publication_automatique.yml (NON INSTALLÉ :
  accord de Jean-Luc nécessaire), toutes les 30 minutes ; ou à la main :
    python3 -B programmes/PUBLIER_LES_VERSIONS_EN_ATTENTE.py --prive=<clone privé COMPLET> --travail=<dossier vide>
        --memoire-sortie=<fichier> [--public=<propriétaire/nom>] [--depot-public=<adresse de clonage>]
        [--gh=<programme gh>] [--seulement=<branche>[,<branche>…]] [--journal=<fichier>] [--a-blanc]
        [--commit-file-2=<commit>]
  Sans --a-blanc il POUSSE au dépôt public ; avec --a-blanc il ne pousse rien et ne change pas la mémoire.
③ ENTRÉE — Le clone privé, avec toutes ses branches en refs/remotes/origin/* (dont publication-auto/journal, qui
  porte memoire.json) ; le dépôt public (cloné sous --travail) ; gh (lu par ETAT_DES_TRAVAUX seulement).
④ CONDITIONS D'ENTRÉE — git sans invite ; les droits de lecture du privé et d'écriture du public donnés à git par
  l'environnement (dans le circuit : l'en-tête du secret JETON_DEPOTS) ; FABRIQUER_LE_CIRCUIT_PUBLIC.py et
  ETAT_DES_TRAVAUX.py à côté de ce fichier.
⑤ SORTIE — Le code de sortie : 0 rien de rouge · 1 au moins une ligne ROUGE (ÉCHEC, ARRÊT) · 2 IMPOSSIBLE (une source
  COMMUNE illisible — toute source qui ne dépend d'aucune branche, lue avant la boucle ; par exemple la mémoire, la
  lecture du public ou la poussée à blanc vers lui — ou --seulement qui nomme une branche inconnue : rien n'est
  décidé, R-734 ; une source d'UNE branche illisible n'est qu'un ÉCHEC de cette branche, N-46) · 5 PLANTAGE
  (exception imprévue).
  À l'écran (journal PUBLIC de GitHub) : une ligne par branche DÉJÀ PUBLIQUE examinée, au vocabulaire fixe, puis une
  ligne de bilan ; jamais un message d'exception ni une trace. Le détail va au fichier --journal (privé) ; la
  mémoire mise à jour va au fichier --memoire-sortie, que le circuit range au dépôt privé.
⑥ TRAITEMENT — `main` : mémoire (`lire_la_memoire`) · état des travaux (sans fetch) · clone ou fetch du public ·
  sources communes, dont la poussée à blanc vers le public (N-89) · pour chaque
  branche « À ÉPROUVER » (ou de --seulement) : faits (`relever_les_faits`), `constater`, `decider`, agir, mémoire
  écrite · une ligne par branche publique · bilan.
⑦ UNITÉ — Secondes (durées, heures Unix) ; heure de Paris dans le nom des demandes.
⑧ POURQUOI — R-754 : ce qu'un programme peut faire, un programme le fait. A-543 (décision de Jean-Luc du 08-10-2026,
  « Non pas question de prendre ces risques ») : aucun code non relu ne tourne au dépôt public avec le jeton — d'où ①.
  Le relais de main ne refuse plus pour la charge depuis FILE-2 (951c16361, 21-11-2026 à 01h36) : aucun refus n'est
  donc à deviner, tout échec se compte — d'où ③.
⑨ CE QUI CLOCHE — (a) Une branche qui modifie le fabricant ou le module du jeton ne s'éprouve plus
  automatiquement : elle attend son installation, ou un envoi à la main (QUESTION à Jean-Luc). Ce que le fabricant
  lit à côté de lui a été relevé à la main le 25-11-2026 (« grep __file__ » sur le fabricant de main, blob 86877e4b :
  lignes 335, 1911, 1986 — le module du jeton et la table, rien d'autre) ; si un fabricant futur lit un autre
  voisin, le dossier composé ne le porte pas et le fabricant échoue (échec compté) : aucun programme ne le garde.
  En mode filet (table de la branche refusée), le circuit publié est celui de la table de MAIN : l'auto-vérification
  publiée (refabrication avec la table de la branche) rougira, et la version jouée lit une table refusée : l'épreuve
  demandée échoue à coup sûr (N-47 du RELU de Cowork du 25-11-2026 à 23h33). Retrait du filet jugé par le
  superviseur R-759 de 23h37 ; il attend l'accord de Jean-Luc. (b) Une demande se juge échouée quand la
  branche est encore « À ÉPROUVER » GARDE_S après son dépôt : un relais ou un passage que GitHub ferait attendre
  plus longtemps sans le montrer serait compté échoué à tort (au plus deux fois, puis arrêt rouge). (c) La mémoire
  vit au dépôt privé : si le circuit ne peut pas la ranger, le passage suivant repart de l'ancienne (au pire une
  tentative de plus). (d) La mémoire est par POINTE (N-44 du RELU de Cowork) : tout commit neuf (un RELU, une note)
  remet le compteur d'échecs à zéro, et une branche condamnée peut rougir deux fois par commit ; la clé pourrait être
  l'empreinte du code (ETAT_DES_TRAVAUX.meme_code). La mémoire n'est jamais élaguée. Consigné, non corrigé. (e) Deux
  endroits du circuit n'ont pas d'épreuve parce que retirés ils ne changent rien d'observable (N-43, X10, X11 du RELU) :
  « persist-credentials: false » (aucun pas après le clonage ne pousse avec les droits de GitHub) et le masque de
  l'en-tête entier (le masque du base64, qu'il contient, suffit à l'écran).
⑩ EFFET — Crée sous --travail des clones et des worktrees, puis les retire ; crée et retire des worktrees du clone
  privé ; sans --a-blanc, POUSSE au dépôt public (publication par le fabricant, puis demande), jamais en force ;
  écrit --journal et --memoire-sortie.
⑪ TERMINAISON — Sort par sys.exit. Chaque commande est bornée (DELAI_S ; le fabricant, DELAI_FABRICANT_S). Aucune
  attente active : une branche qui doit attendre est revue au passage suivant.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
PARIS = ZoneInfo("Europe/Paris")
OK, ROUGE, IMPOSSIBLE, PLANTAGE = 0, 1, 2, 5
DELAI_S = 300                 # secondes, toute commande git
DELAI_FABRICANT_S = 1800      # secondes, une publication (le fabricant lit le dépôt privé)
FRAICHEUR_S = 3 * 86400       # une pointe plus vieille n'est plus publiée seule : quelqu'un a laissé la branche
GARDE_S = 30 * 60             # une demande plus jeune est encore en vol (relais, départ du passage)
ECHECS_MAX = 2                # au deuxième échec d'une pointe : plus de tentative, une ligne rouge
COMMIT_FILE_2 = "951c16361d430a0df31b6c602d21093cac79e440"   # relais qui met en file (installé le 21-11-2026)
BRANCHE_DU_JOURNAL = "publication-auto/journal"
SONDE_D_ECRITURE = "publication-auto/sonde-d-ecriture"   # visée par la poussée À BLANC de `main` ; jamais créée
FICHIER_MEMOIRE = "memoire.json"
MARQUE_EN_COURS = "echanges/EN_COURS.md"
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
MODULE_DU_JETON = "programmes/FORME_D_UN_JETON.py"     # le seul module que le fabricant charge à côté de lui (l. 335)
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"           # la seule donnée qu'il lit à côté de lui (l. 1911, 1986)
# Ce que le fabricant composé dit de la table qu'il lit : 0 et les codes de son relais en JSON, ou 3 (table refusée).
# Il est EXÉCUTÉ dans un processus à part (« python3 -I ») : le module de main est chargé depuis le dossier composé,
# ses définitions s'exécutent, sa fonction main ne tourne pas.
LECTEUR_DE_LA_TABLE = ("import importlib.util, json, sys\n"
                       "s = importlib.util.spec_from_file_location('fabricant_compose', sys.argv[1])\n"
                       "m = importlib.util.module_from_spec(s)\n"
                       "s.loader.exec_module(m)\n"
                       "if m.ERREUR_DE_LA_TABLE:\n"
                       "    sys.exit(3)\n"
                       "print(json.dumps([e[0] for e in m.EPREUVES_DU_CIRCUIT]))\n")
PUBLIC_PAR_DEFAUT = "jeanlucsilbertmds-cyber/cac40-cours-public"
MOTIF_BRANCHE = re.compile(r"^travail-[A-Za-z0-9._-]+$")
# Le vocabulaire fixe : les seuls mots que l'écran PUBLIC porte sur une branche.
RIEN, ATTENTE, PUBLIER, ATTEND_INSTALLATION = "RIEN", "ATTENTE", "PUBLIER", "ATTEND L'INSTALLATION"
FAITE, A_BLANC, ECHEC, ARRET = "PUBLIÉE ET DEMANDÉE", "À BLANC", "ÉCHEC", "ARRÊT APRÈS 2 ÉCHECS"
ROUGES = (ECHEC, ARRET)


class Impossible(Exception):
    """Une source n'a pas pu être lue.

    ① RÔLE — Porter jusqu'à `main` qu'une source (git, mémoire, état) est illisible.
    ② CONTEXTE D'APPEL — Levée par `lancer` et les lecteurs ; attrapée par `main`.
    ③ ENTRÉE — Le message (il ne va qu'au journal privé).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """


class Journal:
    """Le fichier du détail (privé) ; l'écran ne reçoit que les lignes publiques.

    ① RÔLE — Séparer ce que lit le monde (écran du circuit public) de ce que lit Jean-Luc (journal privé).
    ② CONTEXTE D'APPEL — Créé par `main`, passé à tout ce qui lance une commande.
    ③ ENTRÉE — `chemin` : le fichier, ou None (rien n'est gardé).
    ④ CONDITIONS D'ENTRÉE — Le dossier du fichier existe.
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — `ecrire` ajoute une ligne horodatée.
    ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Le journal d'un dépôt public est lisible de tous (A-543).
    ⑨ CE QUI CLOCHE — Le fichier est ouvert à chaque ligne (simple, lent : quelques centaines de lignes).
    ⑩ EFFET — Écrit le fichier.
    ⑪ TERMINAISON — Rend la main.
    """

    def __init__(self, chemin):
        """Retient le chemin.

        ① RÔLE — Constructeur.
        ② CONTEXTE D'APPEL — `main`.
        ③ ENTRÉE — `self` : le journal · `chemin` : le fichier du journal, ou None.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — Retenir le chemin.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        self.chemin = chemin

    def ecrire(self, texte):
        """Ajoute `texte` au journal privé.

        ① RÔLE — Garder le détail.
        ② CONTEXTE D'APPEL — Partout où une commande est lancée ou une décision prise.
        ③ ENTRÉE — `self` : le journal · `texte` : la ligne à garder.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — Ajouter « [heure] texte » au fichier.
        ⑦ UNITÉ — Heure de Paris.
        ⑧ POURQUOI — Voir la classe.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit le fichier si un chemin est donné.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if self.chemin:
            with open(self.chemin, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now(PARIS):%Y-%m-%d %H:%M:%S}] {texte}\n")


def lancer(arguments, journal, dossier=None, tolere=False, delai=DELAI_S):
    """Lance une commande, garde sa sortie au journal privé, et la rend.

    ① RÔLE — Le seul endroit où ce programme lance git ou le fabricant.
    ② CONTEXTE D'APPEL — Toutes les fonctions qui agissent ou lisent.
    ③ ENTRÉE — `arguments` : les mots · `journal` : un Journal · `dossier` : dossier courant ou None · `tolere` : un
      code non nul est une réponse · `delai` : secondes.
    ④ CONDITIONS D'ENTRÉE — Le premier mot est un programme trouvable.
    ⑤ SORTIE — DEUX valeurs : le code de sortie et la sortie standard (texte).
      [rend: 2]
    ⑥ TRAITEMENT — Lancer, borné ; écrire au journal la commande (sans l'environnement), le code, la sortie et
      l'erreur ; sans `tolere`, un code non nul lève Impossible.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — R-734 ; et rien de ce qu'une commande écrit ne doit atteindre l'écran public.
    ⑨ CE QUI CLOCHE — Une commande qui écrirait un secret sur sa sortie l'écrirait au journal PRIVÉ (git ne le fait
      pas ; le fabricant masque les jetons).
    ⑩ EFFET — Lance un processus ; écrit le journal.
    ⑪ TERMINAISON — Rend la main ou lève ; un appel ne dépasse pas `delai`.
      [sort: non]
    """
    try:
        r = subprocess.run(arguments, cwd=dossier, capture_output=True, text=True, errors="replace", timeout=delai)
    except (OSError, subprocess.TimeoutExpired) as e:
        journal.ecrire(f"$ {' '.join(arguments)}\n  {type(e).__name__}")
        if tolere:
            return 124, ""
        raise Impossible(f"{os.path.basename(arguments[0])} : {type(e).__name__}")
    journal.ecrire(f"$ {' '.join(arguments)}\n  code {r.returncode}\n{r.stdout[-4000:]}{r.stderr[-4000:]}")
    if r.returncode != 0 and not tolere:
        raise Impossible(f"{os.path.basename(arguments[0])} {arguments[1] if len(arguments) > 1 else ''} : "
                         f"code {r.returncode}")
    return r.returncode, r.stdout


def charger_l_etat():
    """Importe programmes/ETAT_DES_TRAVAUX.py, voisin de ce fichier.

    ① RÔLE — Réutiliser l'observateur des branches au lieu de le recopier (R-708).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — ETAT_DES_TRAVAUX.py est à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, depuis le chemin voisin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le circuit lance le code de main du public : le voisin est celui de main.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le module (définitions seulement).
    ⑪ TERMINAISON — Rend la main ou lève (fichier absent).
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("etat_des_travaux_publication", os.path.join(ICI, "ETAT_DES_TRAVAUX.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lire_la_memoire(prive, journal):
    """Lit la mémoire des tentatives, rangée au dépôt privé sur la branche fixe du journal.

    ① RÔLE — Savoir, pour chaque pointe, combien d'échecs et si une demande est en vol.
    ② CONTEXTE D'APPEL — `main`, une fois, avant toute décision.
    ③ ENTRÉE — `prive` : le clone privé · `journal` : le Journal.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dict {pointe: {"branche", "echecs", "demande" (heure Unix ou None), "signalee"}} ;
      vide si la branche du journal n'existe pas encore (premier passage).
      [rend: 1]
    ⑥ TRAITEMENT — « rev-parse » de refs/remotes/origin/publication-auto/journal ; absente → {} ; présente →
      « git show …:memoire.json » (absent → {}), JSON qui doit être un dict de dicts.
    ⑦ UNITÉ — Secondes Unix.
    ⑧ POURQUOI — Défauts 2 et 13 de la relecture du 25-11-2026 : sans mémoire, un échec se relançait 48 fois par jour.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible (mémoire illisible : rien n'est décidé sans elle).
      [sort: non]
    """
    ref = "refs/remotes/origin/" + BRANCHE_DU_JOURNAL
    if lancer(["git", "-C", prive, "rev-parse", "-q", "--verify", ref], journal, tolere=True)[0] != 0:
        return {}
    code, texte = lancer(["git", "-C", prive, "show", f"{ref}:{FICHIER_MEMOIRE}"], journal, tolere=True)
    if code != 0:
        return {}
    try:
        memoire = json.loads(texte)
    except ValueError:
        raise Impossible("mémoire : pas du JSON")
    if not isinstance(memoire, dict) or not all(isinstance(v, dict) for v in memoire.values()):
        raise Impossible("mémoire : forme inattendue")
    return memoire


def ecrire_la_memoire(chemin, memoire):
    """Écrit la mémoire dans le fichier que le circuit range au dépôt privé.

    ① RÔLE — Garder la mémoire d'un passage au suivant.
    ② CONTEXTE D'APPEL — `main`, au départ puis après chaque branche.
    ③ ENTRÉE — `chemin` : le fichier · `memoire` : le dict.
    ④ CONDITIONS D'ENTRÉE — Le dossier existe.
    ⑤ SORTIE — Aucune valeur.
      [rend: rien]
    ⑥ TRAITEMENT — JSON trié, écrit dans un fichier voisin puis renommé (jamais à moitié écrit).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Écrite après chaque branche : un plantage plus loin ne perd pas ce qui a été fait.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin + ".neuf", "w", encoding="utf-8") as f:
        json.dump(memoire, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(chemin + ".neuf", chemin)


def constater(souvenir, maintenant):
    """Constate l'issue d'une demande déposée à un passage précédent, pour une branche encore « À ÉPROUVER ».

    ① RÔLE — Compter comme échec une demande qui n'a pas abouti (refusée par le relais, passage sans résultat).
    ② CONTEXTE D'APPEL — `main`, pour une branche « À ÉPROUVER », avant `decider` ; les épreuves.
    ③ ENTRÉE — `souvenir` : le dict de la pointe dans la mémoire (vide si jamais vue) · `maintenant` : secondes Unix.
    ④ CONDITIONS D'ENTRÉE — La branche est « À ÉPROUVER » : ETAT_DES_TRAVAUX ne la range ainsi que si aucun passage
      n'y est vivant et qu'un code demandé n'a pas de résultat.
    ⑤ SORTIE — UNE valeur : le souvenir mis à jour (un dict neuf).
      [rend: 1]
    ⑥ TRAITEMENT — Une demande en vol plus vieille que GARDE_S : la branche n'a pas quitté « À ÉPROUVER », c'est un
      échec (echecs + 1, plus de demande en vol). Sinon, rien ne change.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Version simple du superviseur (P7) : après FILE-2, le relais de main ne refuse plus pour la charge ;
      un refus, une annulation ou un passage sans résultat se traitent pareil : un échec compté.
    ⑨ CE QUI CLOCHE — Voir ⑨ (b) du module.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s = {"echecs": 0, "demande": None, "signalee": False}
    s.update(souvenir)
    if s["demande"] is not None and maintenant - s["demande"] >= GARDE_S:
        s["echecs"] += 1
        s["demande"] = None
    return s


def decider(faits, souvenir, maintenant, demande_deja_ce_passage):
    """Décide, pour une branche, sans rien lire : publier et demander, attendre, ou s'arrêter.

    ① RÔLE — Le cœur du programme : des faits et du souvenir à l'action.
    ② CONTEXTE D'APPEL — `main`, une fois par branche, après `constater` ; les épreuves.
    ③ ENTRÉE — `faits` : dict {etat, pointe_heure, codes, resultats, en_cours (marque EN_COURS), base_file_2 (bool),
      code_de_main (bool : le fabricant ET le module du jeton de la pointe sont ceux qui tournent)} · `souvenir` : le dict rendu par
      `constater` · `maintenant` : secondes Unix · `demande_deja_ce_passage` : bool.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : l'action (RIEN, ATTENTE, ATTEND_INSTALLATION, ARRET, PUBLIER) · le motif court (journal
      privé seulement).
      [rend: 2]
    ⑥ TRAITEMENT — Le premier qui s'applique : état autre que « À ÉPROUVER » → RIEN · base sans FILE-2 → RIEN · marque
      EN_COURS → ATTENTE · pointe plus vieille que FRAICHEUR_S → RIEN · aucun code manquant → RIEN · ECHECS_MAX
      échecs : pas encore signalé → ARRET (rouge, une fois), sinon RIEN · demande en vol → ATTENTE · une demande déjà
      déposée ce passage → ATTENTE (frein) · fabricant ou module du jeton différent de main → ATTEND_INSTALLATION ·
      sinon PUBLIER.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Version simple du superviseur R-759 du 25-11-2026 (voir le module).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if faits["etat"] != "À ÉPROUVER":
        return RIEN, f"état {faits['etat']}"
    if not faits["base_file_2"]:
        return RIEN, "base sans FILE-2 (relais qui met en file)"
    if faits["en_cours"]:
        return ATTENTE, "marque EN_COURS sur la branche"
    if maintenant - faits["pointe_heure"] > FRAICHEUR_S:
        return RIEN, f"pointe de plus de {FRAICHEUR_S // 86400} jours"
    if not [c for c in faits["codes"] if c not in faits["resultats"]]:
        return RIEN, "aucune épreuve manquante"
    if souvenir["echecs"] >= ECHECS_MAX:
        if not souvenir["signalee"]:
            return ARRET, f"{souvenir['echecs']} échecs pour cette pointe : plus de tentative"
        return RIEN, "arrêtée après échecs (déjà signalée)"
    if souvenir["demande"] is not None:
        return ATTENTE, f"demande en vol depuis {(maintenant - souvenir['demande']) // 60} min"
    if demande_deja_ce_passage:
        return ATTENTE, "une demande déjà déposée à ce passage (frein de débit)"
    if not faits["code_de_main"]:
        return ATTEND_INSTALLATION, "le fabricant ou le module du jeton de la branche n'est pas celui de main"
    return PUBLIER, "échec(s) déjà comptés : " + str(souvenir["echecs"])


def relever_les_faits(prive, branche_etat, fabricant_main, commit_file_2, journal):
    """Relève, au dépôt privé, ce que `decider` attend en plus de l'état des travaux.

    ① RÔLE — Les trois faits privés : marque EN_COURS, base qui contient FILE-2, code exécuté identique à main.
    ② CONTEXTE D'APPEL — `main`, une fois par branche examinée.
    ③ ENTRÉE — `prive` : le clone privé · `branche_etat` : le dict d'ETAT_DES_TRAVAUX pour la branche ·
      `fabricant_main` : le chemin du fabricant de main (le module du jeton est à côté) · `commit_file_2` · `journal`.
    ④ CONDITIONS D'ENTRÉE — La pointe est un commit du clone privé.
    ⑤ SORTIE — UNE valeur : le dict des faits (celui de l'état, plus en_cours, base_file_2, code_de_main).
      [rend: 1]
    ⑥ TRAITEMENT — « cat-file -e pointe:echanges/EN_COURS.md » · « merge-base --is-ancestor FILE-2 pointe » (code 0
      oui, 1 non, autre : Impossible) · pour le fabricant ET le module du jeton : empreinte git du fichier de la pointe
      comparée à « hash-object » du fichier de main ; un fichier absent de la pointe n'est pas celui de main.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — PROPRIÉTÉS, jamais des listes de branches : une branche neuve se range seule.
    ⑨ CE QUI CLOCHE — Voir ⑨ (a) du module. Un commit FILE-2 absent du clone est vu par `main` avant la boucle
      (source commune) ; ici, un merge-base illisible vient de la pointe : Impossible pour cette branche seule.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    faits = dict(branche_etat)
    pointe = faits["pointe"]
    faits["en_cours"] = lancer(["git", "-C", prive, "cat-file", "-e", f"{pointe}:{MARQUE_EN_COURS}"],
                               journal, tolere=True)[0] == 0
    code, _ = lancer(["git", "-C", prive, "merge-base", "--is-ancestor", commit_file_2, pointe], journal, tolere=True)
    if code not in (0, 1):
        raise Impossible("merge-base FILE-2 illisible")
    faits["base_file_2"] = code == 0
    faits["code_de_main"] = True
    for chemin in (FABRICANT, MODULE_DU_JETON):
        _, a_main = lancer(["git", "hash-object", os.path.join(os.path.dirname(fabricant_main),
                                                                os.path.basename(chemin))], journal)
        code, a_branche = lancer(["git", "-C", prive, "rev-parse", f"{pointe}:{chemin}"], journal, tolere=True)
        faits["code_de_main"] = faits["code_de_main"] and code == 0 and a_branche.strip() == a_main.strip()
    return faits


def composer_le_fabricant(prive, pointe, fabricant_main, dossier, table_de_main, journal):
    """Compose le dossier d'où le fabricant de main est lancé : son code de main, la table de la branche.

    ① RÔLE — Réaliser la propriété ①bis du module : ce qui s'exécute est l'octet de main, ce qui se lit à côté vient
      de la branche.
    ② CONTEXTE D'APPEL — `publier_la_branche`, une ou deux fois (la seconde : le filet, avec la table de main).
    ③ ENTRÉE — `prive` : le clone privé · `pointe` : la pointe de la branche · `fabricant_main` : le fabricant de main
      (le module du jeton est à côté, la table de main dans ../tests/) · `dossier` : dossier à créer (absent) ·
      `table_de_main` : vrai pour le filet · `journal`.
    ④ CONDITIONS D'ENTRÉE — `dossier` n'existe pas.
    ⑤ SORTIE — DEUX valeurs : le chemin du fabricant composé · vrai si la table est bien posée (la pointe en porte une).
      [rend: 2]
    ⑥ TRAITEMENT — Copier les octets du fabricant et du module du jeton de main sous <dossier>/programmes/ ; poser
      sous <dossier>/tests/ la table : celle de main si `table_de_main`, sinon « git cat-file blob <pointe>:<table> »,
      écrite octet pour octet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fabricant lit la table à côté de lui (« dirname(__file__)/.. », lignes 1911 et 1986 du fabricant
      de main) : la composer est le seul moyen de lui faire lire celle de la branche SANS le modifier (superviseur
      R-759, tour 2 : « si Q2 est impossible sans modifier le fabricant, ARRÊTER »).
    ⑨ CE QUI CLOCHE — Voir ⑨ (a) du module.
    ⑩ EFFET — Crée des fichiers sous `dossier`.
    ⑪ TERMINAISON — Rend la main ou lève Impossible (git illisible) ; borné à DELAI_S.
      [sort: non]
    """
    ici = os.path.dirname(fabricant_main)
    os.makedirs(os.path.join(dossier, "programmes"))
    os.makedirs(os.path.join(dossier, "tests"))
    for chemin in (FABRICANT, MODULE_DU_JETON):
        shutil.copyfile(os.path.join(ici, os.path.basename(chemin)), os.path.join(dossier, chemin))
    cible = os.path.join(dossier, TABLE)
    if table_de_main:
        source = os.path.join(ici, "..", TABLE)
        if not os.path.isfile(source):
            return os.path.join(dossier, FABRICANT), False
        shutil.copyfile(source, cible)
        return os.path.join(dossier, FABRICANT), True
    arguments = ["git", "-C", prive, "cat-file", "blob", f"{pointe}:{TABLE}"]
    try:
        with open(cible, "wb") as f:
            r = subprocess.run(arguments, stdout=f, stderr=subprocess.PIPE, timeout=DELAI_S)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Impossible(f"table de la branche : {type(e).__name__}")
    journal.ecrire(f"$ {' '.join(arguments)} > {cible}\n  code {r.returncode}")
    if r.returncode != 0:
        os.remove(cible)
        return os.path.join(dossier, FABRICANT), False
    return os.path.join(dossier, FABRICANT), True


def codes_du_relais(fabricant_compose, journal):
    """Demande au fabricant composé s'il admet sa table, et quels codes son relais connaîtra.

    ① RÔLE — Juger la table AVANT toute poussée, avec le code de main lui-même (pas une copie de ses règles, R-708).
    ② CONTEXTE D'APPEL — `publier_la_branche`, après `composer_le_fabricant`.
    ③ ENTRÉE — `fabricant_compose` : le chemin rendu par `composer_le_fabricant` · `journal`.
    ④ CONDITIONS D'ENTRÉE — Le dossier composé est complet.
    ⑤ SORTIE — UNE valeur : la liste des codes du relais, ou None si le fabricant ne l'admet pas.
      [rend: 1]
    ⑥ TRAITEMENT — LECTEUR_DE_LA_TABLE dans un Python isolé (« -I -B ») : code 0 et une liste JSON de textes → la
      liste ; TOUT AUTRE CAS → None : code 3 (le fabricant garde l'erreur dans ERREUR_DE_LA_TABLE), mais aussi un
      fabricant qui ne se CHARGE pas avec cette table (code 1 : AttributeError sur « series_hors_de_la_nuit » en
      liste, N-46 du RELU de Cowork du 25-11-2026 à 23h33), un délai dépassé (124) ou une sortie hors forme. Que
      le code de main se charge, `controler_le_fabricant_de_main` l'a établi au départ, sur la table de main : un
      refus ici vient donc de la table lue, pas du code.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fabricant de main vérifie déjà la forme des codes et des arguments (epreuves_du_circuit, motif
      CODE_DE_SERIE, ARGUMENT_FIGE) et garde l'erreur dans ERREUR_DE_LA_TABLE : il suffit de la lire. Superviseur
      R-759, tour 3 (25-11-2026, 23h37), N-46 ② : « code du lecteur ≠ 0 sur la table de la branche = table refusée,
      comme le code 3 ». « -I » : ni le dossier courant ni PYTHONPATH ne fournissent un module au lecteur (N-48).
    ⑨ CE QUI CLOCHE — Les définitions du fabricant de main s'exécutent deux fois (ici, puis à la fabrication). Le
      motif exact du refus (3, 1, 124…) ne va qu'au journal privé.
    ⑩ EFFET — Lance un processus Python.
    ⑪ TERMINAISON — Rend la main ; borné à DELAI_S (un délai dépassé rend None).
      [sort: non]
    """
    code, sortie = lancer([sys.executable, "-I", "-B", "-c", LECTEUR_DE_LA_TABLE, fabricant_compose], journal,
                          tolere=True)
    try:
        codes = json.loads(sortie) if code == 0 else None
    except ValueError:
        codes = None
    if not isinstance(codes, list) or not all(isinstance(c, str) for c in codes):
        journal.ecrire(f"table refusée par le fabricant composé (code du lecteur {code})")
        return None
    return codes


def controler_le_fabricant_de_main(fabricant_main, travail, journal):
    """Vérifie, une fois par passage, que le fabricant de main se charge et admet la table de MAIN.

    ① RÔLE — Séparer la source COMMUNE (le code de main et sa table) des données d'UNE branche.
    ② CONTEXTE D'APPEL — `main`, une fois, avant la boucle des branches, s'il y a au moins une branche à examiner.
    ③ ENTRÉE — `fabricant_main` : le fabricant de main (la table de main dans ../tests/) · `travail` : le dossier de
      travail · `journal`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur.
      [rend: rien]
    ⑥ TRAITEMENT — Dossier composé avec la table de main (`composer_le_fabricant`, table_de_main vrai), puis
      `codes_du_relais` ; table de main absente ou refusée → Impossible ; le dossier est retiré dans tous les cas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759, tour 3, N-46 ③ : « restent IMPOSSIBLE pour tout le passage les seules sources
      communes (…) contrôle initial : le fabricant de main lit la table de main ». Sans lui, un code de main qui ne se
      charge plus rendrait chaque table « refusée » : ATTEND L'INSTALLATION partout, sans une ligne rouge.
    ⑨ CE QUI CLOCHE — Un lancement de Python de plus par passage.
    ⑩ EFFET — Crée et retire un dossier sous `travail` ; lance un processus Python.
    ⑪ TERMINAISON — Rend la main ou lève Impossible ; borné à DELAI_S.
      [sort: non]
    """
    dossier = os.path.join(travail, "fabricant_de_main")
    shutil.rmtree(dossier, ignore_errors=True)
    try:
        fabricant, posee = composer_le_fabricant("", "", fabricant_main, dossier, True, journal)
        if not posee or codes_du_relais(fabricant, journal) is None:
            raise Impossible("le fabricant de main n'admet pas la table de main")
    finally:
        shutil.rmtree(dossier, ignore_errors=True)


def texte_de_la_demande(codes, pointe):
    """Fabrique le texte de la demande, au format du relais de main.

    ① RÔLE — Une seule écriture du format.
    ② CONTEXTE D'APPEL — `deposer_la_demande` ; les épreuves.
    ③ ENTRÉE — `codes` (liste non vide) · `pointe` (40 hex).
    ④ CONDITIONS D'ENTRÉE — Codes non vides.
    ⑤ SORTIE — UNE valeur : le texte, ASCII, fini par une fin de ligne.
      [rend: 1]
    ⑥ TRAITEMENT — « circuit=epreuve », « epreuves=a,b », « pointe=… ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relais de main (FABRIQUER_LE_CIRCUIT_PUBLIC.py, pas « Lire la demande ») admet pour le circuit
      epreuve les seules clés circuit, epreuves, pointe et a_blanc, et refuse une clé inconnue (« version »).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return f"circuit=epreuve\nepreuves={','.join(codes)}\npointe={pointe}\n"


def deposer_la_demande(public_wt, branche, codes, pointe, journal):
    """Commite la demande seule dans un commit à elle et la pousse sur la branche publique, sans force.

    ① RÔLE — Le dernier geste : appuyer sur le relais.
    ② CONTEXTE D'APPEL — `publier_la_branche`, après une publication réussie.
    ③ ENTRÉE — `public_wt` : le clone public sur la branche, à la pointe publiée · `branche` · `codes` · `pointe` ·
      `journal`.
    ④ CONDITIONS D'ENTRÉE — La branche publique existe déjà (le relais refuse une demande qui crée la branche).
    ⑤ SORTIE — DEUX valeurs : l'action (FAITE, ATTENTE si le nom de la minute est pris, ECHEC si la poussée est
      refusée) · le motif court.
      [rend: 2]
    ⑥ TRAITEMENT — Nom à la minute de Paris ; s'il existe : ATTENTE (revu au passage suivant) ; écrire ; « git add »
      de ce seul fichier ; commit de ce seul fichier ; « git push origin HEAD:refs/heads/<branche> », sans force.
    ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Le relais exige : un commit, un fichier ajouté sous demandes/, nom DEMANDE_AAAA-MM-JJ_HHhMM.txt.
      Mineur 8 de la relecture : une minute prise n'est pas un échec.
    ⑨ CE QUI CLOCHE — L'identité du commit est imposée ici (« publication-automatique »).
    ⑩ EFFET — Écrit un fichier, commite, pousse au dépôt public.
    ⑪ TERMINAISON — Rend la main ou lève Impossible (git illisible).
      [sort: non]
    """
    nom = "demandes/DEMANDE_" + datetime.now(PARIS).strftime("%Y-%m-%d_%Hh%M") + ".txt"
    chemin = os.path.join(public_wt, nom)
    if os.path.lexists(chemin):
        return ATTENTE, "une demande porte déjà le nom de cette minute"
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="ascii", newline="\n") as f:
        f.write(texte_de_la_demande(codes, pointe))
    identite = ["-c", "user.name=publication-automatique",
                "-c", "user.email=publication-automatique@users.noreply.github.com"]
    lancer(["git", "-C", public_wt, "add", "--", nom], journal)
    lancer(["git", "-C", public_wt] + identite + ["commit", "-q", "-m",
            f"demande : {','.join(codes)} sur {branche} ({pointe[:9]}), publication automatique", "--", nom], journal)
    code, _ = lancer(["git", "-C", public_wt, "push", "-q", "origin", f"HEAD:refs/heads/{branche}"], journal, tolere=True)
    if code != 0:
        return ECHEC, "poussée de la demande refusée"
    return FAITE, "demande déposée : " + ",".join(codes)


def publier_la_branche(prive, base_publique, travail, branche, pointe, codes, fabricant_main, a_blanc, journal,
                       tentative=None):
    """Publie une branche au dépôt public avec le fabricant de main, puis y dépose sa demande.

    ① RÔLE — L'action PUBLIER de `decider`.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `prive` : le clone privé complet · `base_publique` : un clone du public, mis à jour par `main` avant la
      boucle (clone ou fetch) · `travail` : dossier de travail · `branche`, `pointe` · `codes` : à demander ·
      `fabricant_main` : le fabricant qui tourne (celui de main) · `a_blanc` : ne rien pousser · `journal` : le
      Journal · `tentative` : un dict de `main` ou None ; sa clé « poussee » passe à vrai dès qu'une poussée au
      dépôt public peut avoir lieu (N-89 ④).
    ④ CONDITIONS D'ENTRÉE — `branche` a la forme travail-… ; aucun worktree du privé n'est déjà sur `branche`.
    ⑤ SORTIE — DEUX valeurs : l'action faite (FAITE, A_BLANC, ATTENTE, ATTEND_INSTALLATION, ECHEC) · le motif court.
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ dossier composé (`composer_le_fabricant`, table de la branche) et `codes_du_relais` ; table
      refusée → filet : dossier composé avec la table de main ; codes demandés = codes manquants que le relais
      connaîtra ; aucun → ATTEND_INSTALLATION, rien n'est lancé ni poussé · ① worktree privé, branche locale <branche> sur <pointe> (le fabricant exige que le privé soit SUR
      la branche) · ② clone public partagé (« --shared ») de la base, lien refs/remotes/origin/HEAD du clone
      retiré (« update-ref -d --no-deref »), puis fetch LOCAL depuis la base qui recopie ses branches distantes
      (refs/remotes/origin/* → refs/remotes/origin/*, sans refspec négative), puis l'adresse GitHub remise ; sur
      <branche> : sa branche publique, ou main du public si elle n'existe pas · ③ « tentative » marquée,
      puis le fabricant DE MAIN, lancé depuis le dossier composé, fabrique et (sans à blanc) publie · ④ la demande ·
      ⑤ tout est retiré.
      À blanc : ③ sans --publier (le fabricant écrit le clone, ne pousse rien), « tentative » non marquée, pas de
      demande.
    ⑦ UNITÉ — Secondes (bornes).
    ⑧ POURQUOI — A-543 : seul le code de main, déjà relu et public, tourne avec le jeton.
    ⑨ CE QUI CLOCHE — Le FILET (table refusée → table de main) est le défaut N-47 du RELU de Cowork du 25-11-2026 à
      23h33 : sur GitHub, le joueur relit la table de la VERSION JOUÉE, refusée, et l'épreuve demandée échoue à coup
      sûr (deux publications et une ligne rouge pour rien). Le superviseur R-759 (23h37) juge « ARRÊTER ET
      SIMPLIFIER » par son RETRAIT ; un retrait demande l'accord de Jean-Luc (directive ⑩ de R-751) : le filet est
      GARDÉ en attendant. Depuis N-46 ②, il couvre aussi une table qui fait PLANTER le fabricant de main.
      PROPRIÉTÉ VOULUE (N-89 du RELU de Cowork du 26-11-2026 à 00h13, superviseur R-759 de 00h16) : ici, ne restent
      que des opérations LOCALES et les poussées de CETTE branche ; tout ce qui touche le réseau sans dépendre de la
      branche est fait une fois par `main`, avant la boucle. Ce qui la garde : les épreuves C1 et C1bis (fetch du
      public en panne), pas une liste ; une opération réseau ajoutée ici plus tard redeviendrait une source commune
      déguisée en échec de branche, et aucun programme ne relève les commandes réseau de cette fonction.
      Limite : une poussée qui tombe ici pour une cause commune (jeton retiré, GitHub en panne) APRÈS la sonde
      d'écriture de `main` reste un ÉCHEC de cette branche ; le frein (« tentative ») borne ce cas à une branche
      par passage.
      N-92 (RELU de Cowork du 26-11-2026 à 01h07 ; superviseur R-759 de 01h1x) : la refspec négative
      « ^refs/remotes/origin/HEAD » (tour 5) faisait dépendre la boucle d'un git 2.29 ou plus ; un git plus ancien
      aurait compté un échec à CHAQUE branche, puis les aurait toutes ARRÊTÉES. Remplacée par le retrait du lien
      avant le fetch, accepté par toute version de git. LA PROTECTION DE HEAD ELLE-MÊME N'A AUCUNE ÉPREUVE QUI
      ROUGISSE SUR GIT 2.43 : le défaut qu'elle devait parer (origin/main écrit par le lien origin/HEAD) n'est pas
      reproduit par le superviseur (trois montages, git 2.43 : git n'écrit pas origin/HEAD), ni par l'agent de
      correction au tour 6 (essai du tour 5 rejoué : origin/main juste, lien intact), et le sabotage K1 de Cowork ne
      rougit aucun cas. Ce qui la garde : rien. L'épreuve GV garde seulement l'ABSENCE de refspec
      négative. La version de git du runner (ubuntu-latest) est écrite au journal en tête de chaque passage ;
      elle n'est pas encore lue (THÉORIQUE jusqu'au premier passage réel).
    ⑩ EFFET — Crée et retire des worktrees et un clone ; sans a_blanc, pousse au dépôt public ; écrit « tentative ».
    ⑪ TERMINAISON — Rend la main ou lève Impossible ; le fabricant borné à DELAI_FABRICANT_S.
      [sort: non]
    """
    if not MOTIF_BRANCHE.match(branche):
        return ECHEC, "nom de branche hors de la forme travail-…"
    prive_wt = os.path.join(travail, "prive_" + branche)
    public_wt = os.path.join(travail, "public_" + branche)
    compose = os.path.join(travail, "fabricant_" + branche)
    shutil.rmtree(public_wt, ignore_errors=True)
    shutil.rmtree(compose, ignore_errors=True)
    try:
        fabricant, posee = composer_le_fabricant(prive, pointe, fabricant_main, compose, False, journal)
        connus = codes_du_relais(fabricant, journal) if posee else None
        filet = connus is None
        if filet:   # Q1 en filet : la table de la branche est refusée par le fabricant de main
            shutil.rmtree(compose, ignore_errors=True)
            fabricant, posee = composer_le_fabricant(prive, pointe, fabricant_main, compose, True, journal)
            connus = codes_du_relais(fabricant, journal) if posee else None
        a_demander = [c for c in codes if c in (connus or [])]
        if not a_demander:
            shutil.rmtree(compose, ignore_errors=True)
            return ATTEND_INSTALLATION, ("table de la branche refusée par le fabricant de main" if filet else
                                         "aucun code demandé n'est dans la table de la branche")
    except BaseException:
        shutil.rmtree(compose, ignore_errors=True)
        raise
    lancer(["git", "-C", prive, "worktree", "add", "-q", "-f", "-B", branche, prive_wt, pointe], journal)
    try:
        _, url = lancer(["git", "-C", base_publique, "remote", "get-url", "origin"], journal)
        lancer(["git", "clone", "-q", "--shared", "--no-checkout", base_publique, public_wt], journal)
        # N-89 ② : fetch LOCAL depuis la base (aucun réseau) ; un clone --shared ne porte pas les branches distantes
        # de la base (mesuré par le superviseur R-759 du 26-11-2026 à 00h16) : la refspec les recopie.
        # N-92 : le lien origin/HEAD du clone est retiré AVANT le fetch (rien ne peut écrire par lui), au lieu d'une
        # refspec négative que refuse un git antérieur à 2.29 ; une réf absente rend 0 (mesuré sur git 2.43).
        lancer(["git", "-C", public_wt, "update-ref", "-d", "--no-deref", "refs/remotes/origin/HEAD"], journal)
        lancer(["git", "-C", public_wt, "fetch", "-q", base_publique, "+refs/remotes/origin/*:refs/remotes/origin/*"],
               journal)
        lancer(["git", "-C", public_wt, "remote", "set-url", "origin", url.strip()], journal)
        existe = lancer(["git", "-C", public_wt, "rev-parse", "-q", "--verify", f"refs/remotes/origin/{branche}"],
                        journal, tolere=True)[0] == 0
        lancer(["git", "-C", public_wt, "checkout", "-q", "-B", branche,
                f"origin/{branche}" if existe else "origin/main"], journal)
        option = [] if a_blanc else ["--publier"]
        if not a_blanc and tentative is not None:
            tentative["poussee"] = True   # N-89 ④ : à partir d'ici, le fabricant peut pousser au dépôt public
        code, _ = lancer([sys.executable, "-B", fabricant, prive_wt, public_wt] + option, journal,
                         dossier=public_wt, tolere=True, delai=DELAI_FABRICANT_S)
        if code != 0:
            return ECHEC, f"le fabricant de main refuse la publication (code {code})"
        mode = " (filet : table de main)" if filet else ""
        if a_blanc:
            return A_BLANC, f"publierait avec le fabricant de main{mode} ; demanderait : " + ",".join(a_demander)
        return deposer_la_demande(public_wt, branche, a_demander, pointe, journal)
    finally:
        lancer(["git", "-C", prive, "worktree", "remove", "--force", prive_wt], journal, tolere=True)
        shutil.rmtree(public_wt, ignore_errors=True)
        shutil.rmtree(compose, ignore_errors=True)


def noter(souvenir, action, maintenant):
    """Reporte dans le souvenir d'une pointe ce que le passage vient de faire.

    ① RÔLE — La seule écriture de la mémoire après une action.
    ② CONTEXTE D'APPEL — `main`, après l'action d'une branche.
    ③ ENTRÉE — `souvenir` : le dict de `constater` · `action` : l'action faite · `maintenant` : secondes Unix.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le souvenir mis à jour (dict neuf) · l'action à afficher (ECHEC devient ARRET au
      deuxième échec).
      [rend: 2]
    ⑥ TRAITEMENT — FAITE → demande en vol depuis maintenant · ECHEC → echecs + 1, et au ECHECS_MAX-ième : ARRET,
      signalée · ARRET → signalée · autres : rien.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Au plus deux lignes rouges par pointe, jamais 48 par jour.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s = dict(souvenir)
    if action == FAITE:
        s["demande"] = maintenant
    elif action == ECHEC:
        s["echecs"] += 1
        if s["echecs"] >= ECHECS_MAX:
            s["signalee"] = True
            return s, ARRET
    elif action == ARRET:
        s["signalee"] = True
    return s, action


def main():
    """Lit la ligne de commande, examine les branches, agit, sort.

    ① RÔLE — Le programme en ligne de commande.
    ② CONTEXTE D'APPEL — Voir ② du module.
    ③ ENTRÉE — Voir ② du module.
    ④ CONDITIONS D'ENTRÉE — Voir ④ du module.
    ⑤ SORTIE — Le code de sortie (⑤ du module).
      [rend: rien]
    ⑥ TRAITEMENT — Options · « git --version » au journal (N-92) · mémoire (recopiée tout de suite en sortie) · ETAT_DES_TRAVAUX (sans fetch) · --seulement
      inconnue → IMPOSSIBLE · base du public : clonée si absente, sinon fetch réseau (N-89 ①) · s'il y a une branche
      à examiner : commit FILE-2 présent, `controler_le_fabricant_de_main`, et (sans --a-blanc) une poussée À BLANC
      vers le public (« push --dry-run » visant SONDE_D_ECRITURE, N-89 ③) · par branche, dans UN périmètre
      d'erreur : `constater`, faits, `decider`, action, `noter`, mémoire écrite (sauf à blanc) ; le frein s'arme
      dès qu'une poussée a été TENTÉE, réussie ou non (N-89 ④) · une ligne par branche DÉJÀ publique · bilan.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — LA PROPRIÉTÉ (superviseur R-759 du 26-11-2026 à 00h16, N-89) : « tout ce qui touche le RÉSEAU
      sans dépendre du contenu d'une branche se fait UNE fois, avant la boucle ; illisible → IMPOSSIBLE, rien
      compté. Dans la boucle, seules restent des opérations locales et les poussées de la branche. » Plus
      largement : une source qui ne dépend d'aucune branche se lit avant la boucle, et sa panne rend IMPOSSIBLE
      (code 2) sans rien compter ; une Impossible née DANS la boucle est un ÉCHEC compté pour cette seule pointe
      (au plus deux lignes rouges, puis ARRÊT) et la boucle passe à la suivante (N-46 ①) ; une table refusée
      n'en est pas une : ATTEND L'INSTALLATION (N-46 ②). Les sources communes ne sont PAS énumérées ici : au
      tour 3, une liste a oublié le fetch du public (N-89). Ce que la propriété ne garantit pas :
      (a) la sonde d'écriture suppose que GitHub refuse un « push --dry-run » à un jeton expiré ou sans droit
      d'écriture — THÉORIQUE, à tester une fois sur GitHub avec un jeton révoqué ; (b) une panne qui survient
      APRÈS la sonde, pendant la boucle, frappe la première branche qui pousse : un ÉCHEC compté pour elle, et le
      frein (N-89 ④) épargne les suivantes de ce passage ; une panne qui durerait deux passages ARRÊTERAIT donc
      cette pointe ; (c) rien ne relève, dans le code, une opération réseau ajoutée plus tard dans la boucle : la
      garde est l'épreuve (C1, C1bis, C1ter), pas un relevé. Choix de l'auteur (tour 3), toujours ouvert : le
      superviseur disait « ATTEND L'INSTALLATION, jamais un échec compté » ; l'auteur ne l'applique qu'à la
      TABLE, car une poussée ou un clone de branche qui tombe ne doit pas se taire.
    ⑩ EFFET — Voir ⑩ du module.
    ⑪ TERMINAISON — Sort par sys.exit.
      [sort: oui]
    """
    p = argparse.ArgumentParser(description="Publication automatique des versions en attente (A-1012).")
    p.add_argument("--prive", required=True)
    p.add_argument("--travail", required=True)
    p.add_argument("--memoire-sortie", required=True)
    p.add_argument("--public", default=PUBLIC_PAR_DEFAUT)
    p.add_argument("--depot-public", default=None)
    p.add_argument("--gh", default="gh")
    p.add_argument("--seulement", default="")
    p.add_argument("--journal", default=None)
    p.add_argument("--a-blanc", action="store_true")
    p.add_argument("--commit-file-2", default=COMMIT_FILE_2)
    a = p.parse_args()
    journal = Journal(a.journal)
    rouge = False
    try:
        lancer(["git", "--version"], journal, tolere=True)   # N-92 : la version de git du runner, au journal privé
        memoire = lire_la_memoire(a.prive, journal)
        ecrire_la_memoire(a.memoire_sortie, memoire)
        etat_mod = charger_l_etat()
        try:
            etat = etat_mod.etat_des_travaux(a.prive, a.gh, a.public, fetch=False)
        except etat_mod.Impossible as e:
            raise Impossible(f"ETAT_DES_TRAVAUX : {e}")
        seulement = [b for b in a.seulement.split(",") if b]
        connues = {b["branche"] for b in etat["branches"]}
        if [b for b in seulement if b not in connues]:
            raise Impossible("--seulement nomme une branche inconnue")
        base = os.path.join(a.travail, "public_base")
        if not os.path.isdir(os.path.join(base, ".git")):
            lancer(["git", "clone", "-q", "--no-checkout", a.depot_public or f"https://github.com/{a.public}.git",
                    base], journal)
        else:   # N-89 ① : la lecture RÉSEAU du public, commune, une fois avant la boucle ; illisible → IMPOSSIBLE
            lancer(["git", "-C", base, "fetch", "-q", "--prune", "origin"], journal)
        _, publiques = lancer(["git", "-C", base, "for-each-ref", "--format=%(refname:lstrip=3)",
                               "refs/remotes/origin/"], journal)
        publiques = set(publiques.split())
        fabricant_main = os.path.join(ICI, os.path.basename(FABRICANT))
        maintenant = int(time.time())
        examinees, demande_deja = 0, False
        a_examiner = [b for b in etat["branches"]
                      if not ((b["branche"] not in seulement) if seulement else (b["etat"] != "À ÉPROUVER"))]
        if a_examiner:   # sources COMMUNES (N-46 ③) : illisibles → IMPOSSIBLE pour tout le passage
            lancer(["git", "-C", a.prive, "cat-file", "-e", a.commit_file_2 + "^{commit}"], journal)
            controler_le_fabricant_de_main(fabricant_main, a.travail, journal)
            if not a.a_blanc:   # N-89 ③ : le droit d'ÉCRIRE au public, commun : sonde à blanc, refusée → IMPOSSIBLE
                lancer(["git", "-C", base, "push", "--dry-run", "-q", "origin",
                        "refs/remotes/origin/main:refs/heads/" + SONDE_D_ECRITURE], journal)
        for b in a_examiner:
            examinees += 1
            branche, pointe = b["branche"], b["pointe"]
            souvenir = constater(memoire.get(pointe, {}), maintenant)
            tentative = {"poussee": False}
            try:   # N-46 ① : une erreur née d'une branche ne touche que cette branche
                faits = relever_les_faits(a.prive, b, fabricant_main, a.commit_file_2, journal)
                action, motif = decider(faits, souvenir, maintenant, demande_deja)
                if action == PUBLIER:
                    codes = [c for c in faits["codes"] if c not in faits["resultats"]]
                    action, motif = publier_la_branche(a.prive, base, a.travail, branche, pointe, codes,
                                                       fabricant_main, a.a_blanc, journal, tentative)
                    demande_deja = demande_deja or action == FAITE
            except Impossible as e:
                action, motif = ECHEC, "source de CETTE branche illisible : " + str(e)
            demande_deja = demande_deja or tentative["poussee"]   # N-89 ④ : le frein compte une TENTATIVE
            souvenir, action = noter(souvenir, action, maintenant)
            souvenir["branche"] = branche
            if not a.a_blanc:
                memoire[pointe] = souvenir
                ecrire_la_memoire(a.memoire_sortie, memoire)
            rouge = rouge or action in ROUGES
            journal.ecrire(f"BRANCHE {branche} {pointe[:9]} : {action} — {motif}")
            if branche in publiques:
                print(f"{branche} {pointe[:9]} : {action}", flush=True)
        if examinees == 0:
            print("publication automatique : aucune branche examinée")
        print(f"publication automatique : {'ROUGE' if rouge else 'rien de rouge'}{' (à blanc)' if a.a_blanc else ''}")
    except Impossible as e:
        journal.ecrire("IMPOSSIBLE : " + str(e))
        print("IMPOSSIBLE — une source n'a pas pu être lue ; rien n'est décidé pour la suite (détail au journal privé)")
        sys.exit(IMPOSSIBLE)
    except Exception:  # PLANTAGE : jamais un verdict ; le détail ne va qu'au journal privé
        journal.ecrire("PLANTAGE :\n" + traceback.format_exc())
        print("PLANTAGE — exception imprévue (détail au journal privé)")
        sys.exit(PLANTAGE)
    sys.exit(ROUGE if rouge else OK)


if __name__ == "__main__":
    main()
