#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BOUCLE_DE_CHECK — Ven 16-10-2026 (Paris) — la partie mécanique de la boucle de check, la même des deux côtés. Simulation uniquement.

① RÔLE — Faire, pour le Chat comme pour Cowork, ce qu'un programme sait faire dans la boucle de check : guetter au dépôt
  la note de l'autre côté, la vérifier par le garde-fou, compter les allers-retours, reconnaître les arrêts, et écrire la
  ligne du journal dans une forme fixe. Il ne relit rien, ne répare rien, ne décide rien : il dit à la conversation qui
  le lance s'il y a quelque chose à faire, en UNE ligne qui commence par un mot fixe — « GUETTE », « TOUR À FAIRE »,
  « NOTE REFUSÉE », « MA NOTE REFUSÉE », « ARRÊT », « ERREUR » —, par exemple
  « TOUR À FAIRE · travail-filet · a714f09 · la note de l'autre côté passe le garde-fou · 3 allers-retours sur 10 ».
② CONTEXTE D'APPEL — Lancé à la main par chacune des deux conversations, dans son outil de surveillance (Monitor), qui
  réveille la conversation à chaque ligne écrite :
  python3 programmes/BOUCLE_DE_CHECK.py <clone> --cote chat|cowork
  et, à la fin de chaque tour, pour la ligne du journal :
  python3 programmes/BOUCLE_DE_CHECK.py <clone> --noter --cote chat|cowork --commit <commit> --texte "<texte>"
  Aucune tâche planifiée ne l'appelle. tests/EPREUVES_DE_LA_BOUCLE_DE_CHECK_Ven_16-10-2026.py l'éprouve.
③ ENTRÉE — Le chemin d'un clone du dépôt privé dont le distant s'appelle « origin » ; le côté qui lance ; pour guetter,
  l'intervalle entre deux regards (60 secondes par défaut) et le dossier de sa propre copie (par défaut sous le dossier
  temporaire du système, un par clone guetté) ; pour noter, le commit et le texte. L'accès au dépôt privé vient de la
  configuration du clone (http.extraheader, credential.helper, recopiés dans la copie à chaque démarrage) ou de
  l'environnement du programme (GIT_CONFIG_COUNT, GIT_CONFIG_KEY_0, GIT_CONFIG_VALUE_0), que chaque git lancé hérite.
④ CONDITIONS D'ENTRÉE — git sur la machine ; le clone sait joindre « origin ». Le programme ne travaille JAMAIS dans ce
  clone pour guetter : il s'en fait une copie à lui, qu'il met à jour seul ; la note est lue dans une copie de travail
  jetable de cette copie. Une seule surveillance à la fois par copie : un verrou de fichier l'impose.
⑤ SORTIE — Pour guetter : des lignes, la dernière dit l'événement ; code 0 sur un événement, code 2 si le programme n'a
  pas pu faire son travail (R-734). Pour noter : la ligne écrite ; code 0, ou 2 sur un argument manquant.
⑥ TRAITEMENT — Voir `un_regard`, `guetter` et `noter`.
⑦ UNITÉ — Les heures sont celles de Paris ; les durées en secondes ; un aller-retour = un commit qui touche
  echanges/RELU.md après la dernière ligne de lancement du journal.
⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 19h28 (« 1 » : « fais-en un programme ») : la boucle de check, décidée
  le même jour de 18h43 à 19h21, n'était qu'un texte suivi par deux conversations ; ce qu'un programme peut faire, un
  programme le fait (R-754), et un seul programme pour les deux côtés garde les mêmes règles des deux côtés (R-708).
  Le mode d'emploi complet est la section « LA BOUCLE DE CHECK » de echanges/MODE_EMPLOI_DES_ECHANGES.md. Relu le
  16-10-2026 vers 20h, puis vers 20h40, par un relecteur indépendant, qui a cassé les deux premières versions (relance
  muette, branche supprimée encore vue, journal hérité, notes concurrentes muettes, accès non transmis, refus qui
  tournaient en rond, faux arrêts, surveillances qui se cassaient l'une l'autre) : cette version les répare.
⑨ CE QUI CLOCHE — « Tourne en rond » n'est pas reconnu par le programme : il faut juger que deux réparations se
  contredisent ; c'est le relecteur qui l'écrit en tête de sa note (« ARRÊT — TOURNE EN ROND »), et le programme lit
  cette ligne. · La note est vérifiée par le garde-fou de la version relue : une version qui affaiblit le garde-fou
  serait vérifiée par le garde-fou affaibli ; le programme le SIGNALE sur la ligne du tour (« le garde-fou a changé
  sur cette version ») quand le garde-fou, un module qu'il importe ou nomme dans son code, ou une des deux sections du
  registre qu'il lit, a changé ; un fichier qu'il lirait par un nom construit morceau par morceau n'est pas vu. · Les
  arrêts et les refus ne sont annoncés qu'une fois chacun (mémoire dans la copie) ; « TOUR À FAIRE » est redit à
  chaque relance tant que le tour n'est pas joué.
⑩ EFFET — Crée et met à jour sa propre copie du dépôt (git fetch --prune) et y garde un petit fichier de mémoire ; y
  crée puis retire des copies de travail jetables ; pour noter, ajoute une ligne à echanges/JOURNAL_DE_LA_BOUCLE.md du
  clone (sans commit : la conversation pousse). Le clone guetté n'est jamais écrit pour guetter.
⑪ TERMINAISON — Guetter boucle jusqu'à un événement ; l'outil de surveillance l'arrête au bout de 30 minutes (SIGTERM
  passe par le nettoyage ; une copie laissée par un autre signal est retirée au regard suivant), et la conversation le
  relance. Chaque appel à git ou au garde-fou est borné par une limite de temps.
  [sort: oui]
"""
import argparse
import ast
import fcntl
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
NOTE_DU_CHAT = "echanges/A_RELIRE.md"
NOTE_DE_COWORK = "echanges/RELU.md"
JOURNAL = "echanges/JOURNAL_DE_LA_BOUCLE.md"
GARDE_FOU = "programmes/CONTROLER_MA_LIVRAISON.py"
REGISTRE = "gouvernance/REGISTRE_REGLES.md"
BUDGET = 10                      # allers-retours avant de redemander à Jean-Luc (décision du 16-10-2026, 18h43 et 19h12)
SILENCE = 3 * 3600               # secondes sans réponse de l'autre côté (texte de la boucle validé le 16-10-2026)
LANCEMENT = re.compile(r"^BOUCLE (LANCÉE|CONTINUÉE)\b")
LIGNE_DU_JOURNAL = re.compile(r"^- (\d{4}-\d\d-\d\d) (\d\dh\d\d) Paris · (Chat|Cowork) · (\S+) · (.*)$")
TETE = 15                        # lignes de tête où se lisent les arrêts écrits par l'autre côté
PREFIXE_DES_COPIES = "boucle_de_check_copie_"
ATTENTE_DU_VERROU = 300         # secondes : au-delà, la vérification rend « contrôle impossible » au lieu d'attendre
COTES = {"chat": ("Chat", NOTE_DU_CHAT, NOTE_DE_COWORK),       # nom, ma note, la note de l'autre
         "cowork": ("Cowork", NOTE_DE_COWORK, NOTE_DU_CHAT)}
ATTENDU = {NOTE_DU_CHAT: "livraison", NOTE_DE_COWORK: "relecture"}   # le rôle que le garde-fou exige de chaque note
ARRET_MARQUE = re.compile(r"(RIEN DE (NEUF|NOUVEAU)(\s*[-:.,!»].*)?|ARRET\s*[-:.]?\s*(DECISION( DE JEAN[- ]?LUC)?|TOURNE EN ROND|SILENCE)\b.*)$")
RESERVE = re.compile(r"\b(SAUF|MAIS|EXCEPTE|HORMIS)\b")   # « RIEN DE NEUF » suivi d'une réserve n'arrête pas la boucle
RECU_DU_ROLE = "rôle attendu : "   # le début de la ligne par laquelle le garde-fou prouve qu'il a contrôlé le rôle


def git(depot, *args, limite=120):
    """Lance une commande git sur un dépôt et rend son code et sa sortie.

    ① RÔLE — Un seul endroit pour appeler git, avec une limite de temps.
    ② CONTEXTE D'APPEL — Toutes les fonctions de ce programme qui lisent un dépôt.
    ③ ENTRÉE — `depot` : le dossier · `args` : les mots de la commande après « git » · `limite` : secondes.
    ④ CONDITIONS D'ENTRÉE — git installé.
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si la limite est dépassée), puis la sortie standard sans le saut de
      ligne final.
      [rend: 2]
    ⑥ TRAITEMENT — subprocess.run avec capture ; le dépassement de limite devient le code 124. L'environnement du
      programme passe à git tel quel : c'est par là qu'arrive l'accès au dépôt privé quand le clone ne le garde pas.
    ⑦ UNITÉ — Secondes pour la limite.
    ⑧ POURQUOI — Un fetch qui pend ne doit pas bloquer la surveillance sans rien dire (R-734).
    ⑨ CE QUI CLOCHE — La sortie d'erreur est jetée : l'appelant ne voit que le code.
    ⑩ EFFET — Celui de la commande git lancée.
    ⑪ TERMINAISON — Rend la main au plus tard après `limite` secondes.
      [sort: non]
    """
    try:
        r = subprocess.run(["git", "-C", depot, *args], capture_output=True, text=True, errors="replace",
                           timeout=limite)
    except subprocess.TimeoutExpired:
        return 124, ""
    return r.returncode, r.stdout.rstrip("\n")


def copie_du_programme(clone, dossier=None):
    """Rend la copie du dépôt propre au programme, la crée si elle n'existe pas, et y recopie l'accès du clone.

    ① RÔLE — Ne jamais travailler dans le clone guetté : il porte souvent du travail non commité, et ses propres
      « git fetch » entreraient en collision avec ceux du programme.
    ② CONTEXTE D'APPEL — `guetter`, une fois au départ ; les épreuves.
    ③ ENTRÉE — `clone` : le clone guetté · `dossier` : où mettre la copie (None : sous le dossier temporaire du système,
      un nom tiré du chemin du clone, pour que deux clones n'aient jamais la même copie).
    ④ CONDITIONS D'ENTRÉE — Le clone a un distant « origin ».
    ⑤ SORTIE — DEUX valeurs : le chemin de la copie, ou None, puis le motif d'échec en une ligne (vide si réussi).
      [rend: 2]
    ⑥ TRAITEMENT — ① lire l'adresse du distant du clone · ② si la copie n'est pas un dépôt, git clone --no-checkout du
      clone (local, rapide) · ③ À CHAQUE APPEL, y recopier l'adresse du distant et, s'ils existent, l'en-tête d'accès
      http.extraheader et l'aide aux identifiants credential.helper de la configuration PROPRE au clone (« --local »),
      sans jamais les écrire à l'écran ; ce qui vient de l'environnement n'est pas recopié : chaque git le reçoit.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026 : sans copie à lui, le programme gardait les branches supprimées,
      laissait des copies de travail inscrites dans le clone du Chat, et ses fetch échouaient quand le Chat faisait le
      sien ; puis, au second tour, une copie qui gardait l'adresse vue à sa création, et une copie interrompue entre sa
      création et sa configuration : la recopie se fait donc à chaque démarrage.
    ⑨ CE QUI CLOCHE — La valeur de l'en-tête d'accès passe par la ligne de commande de git pendant la recopie, et elle
      est écrite dans la configuration de la copie, sous le dossier temporaire : comme dans le clone, d'où elle vient.
      Relecture indépendante du 16-10-2026, troisième tour : un jeton venu de l'environnement était écrit sur le disque ;
      la recopie se limite donc à la configuration propre au clone.
    ⑩ EFFET — Crée un dossier et un dépôt ; écrit sa configuration.
    ⑪ TERMINAISON — Rend la main au plus tard après les limites des commandes git.
      [sort: non]
    """
    clone = os.path.abspath(clone)
    if dossier is None:
        dossier = os.path.join(tempfile.gettempdir(),
                               "boucle_de_check_" + hashlib.sha1(clone.encode("utf-8")).hexdigest()[:12])
    code, adresse = git(clone, "remote", "get-url", "origin")
    if code != 0 or not adresse:
        return None, "le clone n'a pas de distant « origin »"
    if not os.path.isdir(os.path.join(dossier, ".git")):
        shutil.rmtree(dossier, ignore_errors=True)
        try:
            r = subprocess.run(["git", "clone", "-q", "--no-checkout", clone, dossier], capture_output=True,
                               timeout=600)
        except subprocess.TimeoutExpired:
            return None, "la copie du clone n'a pas fini en 600 secondes"
        if r.returncode != 0:
            return None, "la copie du clone a échoué"
    git(dossier, "remote", "set-url", "origin", adresse)
    for cle in ("http.extraheader", "credential.helper"):
        code, valeur = git(clone, "config", "--local", "--get", cle)
        if code == 0 and valeur:
            git(dossier, "config", cle, valeur)
    return dossier, ""


def memoire(depot, cote, ecrire=None):
    """Lit, ou écrit, la mémoire du programme pour un côté : les annonces déjà faites et les notes déjà vérifiées.

    ① RÔLE — Ne dire qu'une fois un arrêt ou un refus, et ne vérifier qu'une fois sa propre note.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `depot` : la copie du programme · `cote` · `ecrire` : None pour lire, ou le dictionnaire à écrire.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire {"annonces": [clés], "verifiees": {"<note>@<commit>": [code, motif]}} ;
      vide s'il n'existe pas ou ne se lit pas.
      [rend: 1]
    ⑥ TRAITEMENT — Un fichier JSON dans le dossier .git de la copie, un par côté.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, second tour, points 3 et 6 : un refus ou un arrêt redit à chaque
      relance réveillait la conversation toutes les minutes, et faisait tourner les deux côtés en rond ; quatrième
      tour, point 1 : une note refusée faisait relancer le garde-fou, une demi-minute, à chaque regard.
    ⑨ CE QUI CLOCHE — Une mémoire illisible est prise pour vide : un arrêt peut alors être redit une fois.
    ⑩ EFFET — Écrit un fichier dans la copie quand `ecrire` est donné.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin = os.path.join(depot, ".git", f"boucle_de_check_{cote}.json")
    if ecrire is not None:
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(ecrire, f, ensure_ascii=False)
        return ecrire
    try:
        with open(chemin, encoding="utf-8") as f:
            m = json.load(f)
        return {"annonces": list(m.get("annonces", [])), "verifiees": dict(m.get("verifiees", {}))}
    except (OSError, ValueError, AttributeError):
        return {"annonces": [], "verifiees": {}}


def versions_en_attente(depot):
    """Rend les noms des versions en attente connues du distant, sans le préfixe « origin/ ».

    ① RÔLE — Trouver où vit le travail relu, sans qu'on le nomme (règle de nom du 23-09-2026, A-448).
    ② CONTEXTE D'APPEL — `un_regard`, après le fetch.
    ③ ENTRÉE — `depot` : la copie du programme.
    ④ CONDITIONS D'ENTRÉE — Un fetch avec --prune juste avant : sinon une branche supprimée au distant reste vue.
    ⑤ SORTIE — UNE valeur : la liste triée des noms qui commencent par « travail- », par exemple ["travail-filet"].
      [rend: 1]
    ⑥ TRAITEMENT — git branch -r --list 'origin/travail-*'.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Il n'y en a jamais plus d'une à la fois : c'est ce qui permet de la trouver seul.
    ⑨ CE QUI CLOCHE — Un échec de git rend une liste vide ; le fetch qui précède a déjà dit son échec.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    _, sortie = git(depot, "branch", "-r", "--list", "origin/travail-*")
    return sorted(x.strip()[len("origin/"):] for x in sortie.split("\n") if x.strip().startswith("origin/travail-"))


def dernier_commit(depot, branche, fichier, base):
    """Rend le dernier commit de la version en attente, après son départ de la version officielle, qui a touché un fichier.

    ① RÔLE — Savoir qui a écrit sa note en dernier dans CETTE boucle, et quand.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `depot` · `branche` · `fichier` : chemin relatif au dépôt · `base` : le commit où la version a quitté
      origin/main (None : toute l'histoire).
    ④ CONDITIONS D'ENTRÉE — Un fetch récent.
    ⑤ SORTIE — DEUX valeurs : l'identifiant complet du commit et son heure en secondes depuis 1970, ou (None, None)
      si le fichier n'a pas été touché sur cette version depuis `base`.
      [rend: 2]
    ⑥ TRAITEMENT — git log -1 --format='%H %ct' <base>..origin/<branche> -- <fichier>.
    ⑦ UNITÉ — Secondes depuis 1970 (heure du commit).
    ⑧ POURQUOI — Le commit qui touche la note, et non le dernier de la version : un commit de l'autre côté qui ne touche
      pas sa note n'est pas une réponse. Depuis `base` : relecture indépendante du 16-10-2026, second tour, point 5 —
      les notes héritées d'une boucle déjà fusionnée faisaient annoncer un silence de 120 heures.
    ⑨ CE QUI CLOCHE — L'heure est celle que le commit déclare : une horloge fausse chez l'un fausse le silence.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    plage = f"{base}..origin/{branche}" if base else "origin/" + branche
    _, sortie = git(depot, "log", "-1", "--format=%H %ct", plage, "--", fichier)
    if not sortie.strip():
        return None, None
    h, ct = sortie.split()
    return h, int(ct)


def est_ancetre(depot, a, b):
    """Dit si le commit `a` est un ancêtre strict du commit `b`.

    ① RÔLE — Dire quelle note a été écrite après l'autre, par l'histoire et non par l'horloge.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `depot` · `a` et `b` : deux identifiants de commit.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : True si a ≠ b et a est ancêtre de b.
      [rend: 1]
    ⑥ TRAITEMENT — git merge-base --is-ancestor.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, points 2, 7 et 8 : comparer à un commit de départ rendait la
      surveillance muette après une relance, et un rebase faisait relire deux fois. L'ordre des deux notes dans
      l'histoire survit à une relance et à un rebase.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return a != b and git(depot, "merge-base", "--is-ancestor", a, b)[0] == 0


def lire_au_commit(depot, commit, fichier):
    """Rend le texte d'un fichier tel qu'il est dans un commit, ou None s'il n'y est pas.

    ① RÔLE — Lire la note, le journal et le garde-fou sans copie de travail.
    ② CONTEXTE D'APPEL — `un_regard`, `modules_du_garde_fou`, `garde_fou_change`, `lignes_de_la_version`.
    ③ ENTRÉE — `depot` · `commit` : un identifiant ou une référence (« origin/travail-filet ») · `fichier`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — git show <commit>:<fichier>.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    code, sortie = git(depot, "show", f"{commit}:{fichier}")
    return sortie if code == 0 else None


def lignes_de_la_version(depot, branche, base):
    """Rend les lignes du journal ajoutées sur la version en attente, dans leur ordre, sous leur forme fixe.

    ① RÔLE — Ne compter que la boucle de CE travail : le journal de la boucle précédente arrive avec la version
      officielle.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `depot` · `branche` · `base` : le commit où la version a quitté origin/main, ou None.
    ④ CONDITIONS D'ENTRÉE — Un fetch récent.
    ⑤ SORTIE — UNE valeur : la liste des lignes du journal de la pointe de la version qui ne figurent pas dans le
      journal de `base`, et qui ont la forme fixe de `noter`.
      [rend: 1]
    ⑥ TRAITEMENT — Le journal à `base` et à la pointe ; les lignes de la pointe absentes du premier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, point 4 : la ligne « BOUCLE LANCÉE » d'une boucle déjà fusionnée
      lançait la suivante sans Jean-Luc, avec un compteur déjà à 3.
    ⑨ CE QUI CLOCHE — Une ligne recopiée à l'identique d'une ancienne boucle ne serait pas comptée ; chaque ligne porte
      l'heure à la minute et un commit, ce qui la rend unique en pratique.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    avant = set((lire_au_commit(depot, base, JOURNAL) or "").split("\n")) if base else set()
    pointe = (lire_au_commit(depot, "origin/" + branche, JOURNAL) or "").split("\n")
    return [x for x in pointe if x not in avant and LIGNE_DU_JOURNAL.match(x)]


def derniere_ligne_de_lancement(lignes):
    """Rend la dernière ligne « BOUCLE LANCÉE » ou « BOUCLE CONTINUÉE » écrite par le Chat, ou None.

    ① RÔLE — Trouver le point d'où se compte le budget.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `lignes` : les lignes du journal de la version, sous leur forme fixe.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la ligne, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — Parcours des lignes ; la dernière qui est du Chat et dont le texte commence par la marque.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « BOUCLE CONTINUÉE » remet le compte à zéro : c'est ainsi que « 10 tours de plus » (décision de
      Jean-Luc du 16-10-2026 à 19h12) se compte sans autre règle. Sans ligne de lancement, la boucle n'a pas été lancée
      par Jean-Luc.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    derniere = None
    for x in lignes:
        m = LIGNE_DU_JOURNAL.match(x)
        if m and m.group(3) == "Chat" and LANCEMENT.match(m.group(5)):
            derniere = x
    return derniere


def allers_retours(depot, branche, ligne):
    """Compte les réponses de Cowork écrites depuis le commit qui a ajouté la ligne de lancement.

    ① RÔLE — Le compteur du budget, lu dans l'histoire et non recopié.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `depot` · `branche` · `ligne` : la ligne de lancement.
    ④ CONDITIONS D'ENTRÉE — La ligne figure au journal de la version.
    ⑤ SORTIE — UNE valeur : le nombre de commits qui touchent echanges/RELU.md après ce commit, ou None si le commit
      qui a ajouté la ligne n'est pas retrouvé.
      [rend: 1]
    ⑥ TRAITEMENT — ① git log --reverse -S<ligne> : le premier commit qui l'a ajoutée · ② git rev-list --count
      <ce commit>..origin/<branche> -- echanges/RELU.md.
    ⑦ UNITÉ — Un aller-retour = un commit de la note de Cowork.
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, point 9 : compté sur les lignes du journal, le 10e tour passait
      quand la note était poussée avant sa ligne — ce qui est l'ordre naturel. Les commits de la note ne dépendent pas
      de l'ordre des poussées.
    ⑨ CE QUI CLOCHE — Deux commits de la note de Cowork pour un seul tour (une correction de sa note) comptent pour deux.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    _, sortie = git(depot, "log", "--reverse", "--format=%H", "-S" + ligne, "origin/" + branche, "--", JOURNAL)
    commits = [x for x in sortie.split("\n") if x.strip()]
    if not commits:
        return None
    code, n = git(depot, "rev-list", "--count", f"{commits[0]}..origin/{branche}", "--", NOTE_DE_COWORK)
    return int(n) if code == 0 and n.isdigit() else None


def normaliser(texte):
    """Rend le texte en capitales, sans accents, tous les tirets ramenés à « - », les espaces resserrés.

    ① RÔLE — Reconnaître une ligne d'arrêt quelle que soit sa graphie.
    ② CONTEXTE D'APPEL — `arret_ecrit`.
    ③ ENTRÉE — `texte`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte normalisé, par exemple « ARRET - DECISION DE JEAN-LUC ».
      [rend: 1]
    ⑥ TRAITEMENT — décomposition Unicode, accents retirés, capitales, tirets « — – ‐ ‑ − » en « - ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, point 5 : « ARRÊT - TOURNE EN ROND » ou « Arrêt — décision »
      faisaient relire une fois de trop après que l'autre avait dit stop.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    t = "".join(c for c in unicodedata.normalize("NFKD", texte) if not unicodedata.combining(c)).upper()
    for tiret in "—–‐‑−":
        t = t.replace(tiret, "-")
    return " ".join(t.split())


def arret_ecrit(note):
    """Rend la ligne d'arrêt que l'autre côté a écrite en tête de sa note, ou None.

    ① RÔLE — Reconnaître les arrêts qu'un programme ne sait pas juger, et que la conversation a écrits.
    ② CONTEXTE D'APPEL — `un_regard`, sur la note de l'autre côté quand c'est mon tour.
    ③ ENTRÉE — `note` : le texte de la note.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la première des 15 premières lignes qui COMMENCE par une marque d'arrêt — rendue sans ses
      doubles étoiles ni ses dièses de titre ; sinon None. Les marques forment une liste fermée (`ARRET_MARQUE`), lue
      une fois la ligne normalisée et un éventuel « RELU — » ou « À RELIRE — » de titre retiré : « RIEN DE NEUF » ou
      « RIEN DE NOUVEAU », seuls ou suivis d'un signe de ponctuation (tiret, deux-points, point, virgule, point
      d'exclamation, guillemet fermant), jamais d'un mot ; « ARRÊT » suivi, après un tiret, deux-points, point ou rien,
      de « DÉCISION » (avec ou sans « DE JEAN-LUC »), « TOURNE EN ROND » ou « SILENCE ». Un guillemet ouvrant en tête
      est retiré. Une ligne « RIEN DE NEUF » ou « RIEN DE NOUVEAU » qui porte une réserve (« sauf », « mais »,
      « excepté », « hormis ») n'arrête pas : relecture indépendante du 16-10-2026, cinquième tour — « RIEN DE NOUVEAU,
      sauf une cassure M » arrêtait la boucle. La réserve ne vaut pas pour « ARRÊT — … » (sixième tour) : la question
      posée à Jean-Luc contient librement « mais » ou « sauf ».
      [rend: 1]
    ⑥ TRAITEMENT — Lecture des lignes de tête, chacune normalisée par `normaliser`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « RIEN DE NEUF — je propose de clore » est la fin de la boucle ; « RIEN DE NOUVEAU » est le mot de la
      maison (registre, ligne 37) ; « ARRÊT — DÉCISION DE JEAN-LUC », « ARRÊT — TOURNE EN ROND » et « ARRÊT — SILENCE »
      sont les arrêts que l'autre côté a reconnus. Au DÉBUT de la ligne seulement : relecture indépendante du
      16-10-2026, second tour, point 4 — une livraison qui déclare « le dernier tour du relecteur : RIEN DE NOUVEAU »
      arrêtait la boucle avant toute relecture. Une liste FERMÉE : troisième tour, point 4 — « Arrêt du circuit du
      soir… » ou « ## Rien de nouveau dans la passe ②, mais M casse » arrêtaient la boucle.
    ⑨ CE QUI CLOCHE — Une marque écrite autrement que la liste n'arrête rien : un arrêt manqué se voit au tour suivant.
      · Le guillemet ouvrant retiré en tête fait qu'une ligne des 15 premières qui EXPLIQUE un arrêt en commençant
      par sa citation (« ARRÊT — TOURNE EN ROND » s'écrit quand…) arrête la boucle (relecture de Cowork du
      17-10-2026, point 5 : jamais survenu dans les 597 versions des deux notes). L'effet est un arrêt annoncé à
      Jean-Luc, pas un silence.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for ligne in note.split("\n")[:TETE]:
        nue = ligne.replace("**", "").strip().strip("# ").strip()
        n = re.sub(r"^(A RELIRE|RELU)\s*-\s*", "", normaliser(nue).lstrip("«“\" "))
        if ARRET_MARQUE.match(n) and not (n.startswith("RIEN DE") and RESERVE.search(n)):
            return nue
    return None


def modules_du_garde_fou(depot, commit):
    """Rend le garde-fou et les fichiers de code qu'il importe ou nomme dans son code, de proche en proche.

    ① RÔLE — Savoir quels programmes comparer pour dire « le garde-fou a changé ».
    ② CONTEXTE D'APPEL — `garde_fou_change`.
    ③ ENTRÉE — `depot` · `commit`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des chemins existants au commit : le garde-fou, puis chaque programmes/NOM.py
      ou NOM.py de la racine dont le nom est importé (« import NOM ») ou écrit en clair dans une chaîne du code
      (« "NOM.py" », hors des textes explicatifs), et de même pour chacun de ceux-là.
      [rend: 1]
    ⑥ TRAITEMENT — Arbre syntaxique de chaque fichier ; les commentaires et les textes explicatifs ne comptent pas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, second tour, point 9 : cherchés dans le texte entier, des noms
      cités en commentaire faisaient sonner l'avertissement à presque chaque tour, et il ne voulait plus rien dire.
      Le garde-fou importe LIRE_LE_CODE, qui importe emp : d'où le « de proche en proche ».
    ⑨ CE QUI CLOCHE — Un fichier dont le nom serait construit morceau par morceau n'est pas vu.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : chaque fichier n'est lu qu'une fois.
      [sort: non]
    """
    vus, a_lire = set(), [GARDE_FOU]
    while a_lire:
        chemin = a_lire.pop()
        if chemin in vus:
            continue
        vus.add(chemin)
        try:
            arbre = ast.parse(lire_au_commit(depot, commit, chemin) or "")
        except SyntaxError:
            continue
        textes = {id(n.body[0].value) for n in ast.walk(arbre)
                  if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body
                  and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
        noms = set()
        for n in ast.walk(arbre):
            if isinstance(n, ast.Import):
                noms |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module:
                noms.add(n.module.split(".")[0])
            elif isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in textes:
                m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\.py", n.value)
                if m:
                    noms.add(m.group(1))
        for nom in noms:
            for c in (f"programmes/{nom}.py", f"{nom}.py"):
                if c not in vus and git(depot, "cat-file", "-e", f"{commit}:{c}")[0] == 0:
                    a_lire.append(c)
    return sorted(vus)


def sections_lues_du_registre(texte):
    """Rend les deux sections du registre que le garde-fou lit : le protocole de livraison et R-755.

    ① RÔLE — Comparer du registre ce qui change ce que le garde-fou exige, et rien d'autre.
    ② CONTEXTE D'APPEL — `garde_fou_change`.
    ③ ENTRÉE — `texte` : le registre, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte de la section « # LE PROTOCOLE DE LIVRAISON » jusqu'au séparateur « --- », suivi
      de celui de la section « ### R-755 » jusqu'à la section suivante ; une chaîne vide pour ce qui manque.
      [rend: 1]
    ⑥ TRAITEMENT — Les mêmes bornes que `gestes_du_protocole`, `gestes_du_relecteur` et `pieges_r755` du garde-fou.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, second tour, point 9 : le registre change dans presque chaque
      livraison ; seules ces deux sections changent ce que le garde-fou exige.
    ⑨ CE QUI CLOCHE — Les bornes sont recopiées du garde-fou : si le garde-fou change les siennes, celles-ci ne suivent
      pas, et l'avertissement peut se taire sur ce changement-là.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    t = texte or ""
    i = t.find("\n# LE PROTOCOLE DE LIVRAISON")
    protocole = t[i:t.find("\n---", i + 5)] if i >= 0 else ""
    j = t.find("\n### R-755")
    r755 = t[j:t.find("\n### ", j + 5)] if j >= 0 else ""
    return protocole + "\n" + r755


def garde_fou_change(depot, commit):
    """Dit si le garde-fou de la version relue, un module qu'il emploie, ou une section du registre qu'il lit, a changé.

    ① RÔLE — Signaler qu'une note est vérifiée par un garde-fou modifié (⑨ du programme).
    ② CONTEXTE D'APPEL — `un_regard`, avant de rendre un tour ou un refus.
    ③ ENTRÉE — `depot` · `commit`.
    ④ CONDITIONS D'ENTRÉE — origin/main connu.
    ⑤ SORTIE — UNE valeur : True si un des fichiers de `modules_du_garde_fou` (au commit ou à origin/main) diffère de la
      version officielle, ou si les sections lues du registre diffèrent.
      [rend: 1]
    ⑥ TRAITEMENT — git diff --quiet origin/main <commit> -- <fichiers> ; puis comparaison des sections du registre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ne pas laisser croire qu'une vérification par un garde-fou modifié vaut une vérification ordinaire.
    ⑨ CE QUI CLOCHE — Un échec de git est compté comme un changement : on signale de trop.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fichiers = sorted(set(modules_du_garde_fou(depot, commit)) | set(modules_du_garde_fou(depot, "origin/main")))
    code, _ = git(depot, "diff", "--quiet", "origin/main", commit, "--", *fichiers)
    if code != 0:
        return True
    return (sections_lues_du_registre(lire_au_commit(depot, "origin/main", REGISTRE))
            != sections_lues_du_registre(lire_au_commit(depot, commit, REGISTRE)))


def prendre_le_verrou_des_copies(depot, attente=ATTENTE_DU_VERROU):
    """Attend puis prend le verrou qui sépare, sur un même dépôt, les créations et retraits de copies de travail.

    ① RÔLE — Que deux programmes travaillant sur le même dépôt ne créent, retirent ou nettoient jamais des copies de
      travail au même instant.
    ② CONTEXTE D'APPEL — `verifier_la_note`, autour du nettoyage et de la création, puis autour du retrait.
    ③ ENTRÉE — `depot` : un dépôt git · `attente` : le temps d'attente maximal, en secondes (300 par défaut).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le fichier du verrou, ouvert et verrouillé — le fermer libère le verrou ; ou None si le
      verrou est resté tenu par un autre pendant toute l'attente.
      [rend: 1]
    ⑥ TRAITEMENT — Trouver le dossier git commun (git rev-parse --git-common-dir) ; ouvrir
      boucle_de_check_copies.verrou dedans ; tenter fcntl.flock exclusif sans attendre, toutes les 50 millisecondes,
      jusqu'à la fin de l'attente ; toute interruption (un signal d'arrêt) referme le fichier, donc libère le verrou,
      avant de remonter.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026 vers 23h40 : git ne supporte pas deux « worktree add »,
      « remove » ou « prune » en même temps sur un même dépôt — 4 processus × 50 vérifications sans verrou : 18
      échecs « copie du commit impossible » ; avec ce verrou : 0 sur 200, et 0 sur 240 avec 8 processus. Le numéro
      dans le nom de la copie (`proprietaire_vivant`) ne suffisait pas : il protège la copie pendant que le garde-fou
      tourne, pas l'inscription que git est en train d'écrire. L'attente bornée et la fermeture sur interruption :
      tour suivant de la même relecture — un signal d'arrêt reçu juste après la prise du verrou laissait le fichier
      ouvert ; le nettoyage redemandait alors le verrou que le programme tenait lui-même, et attendait pour toujours,
      bloquant avec lui toute autre vérification du dépôt.
    ⑨ CE QUI CLOCHE — Le verrou ne protège que contre les autres programmes qui le prennent : un « git worktree »
      lancé à la main sur le même dépôt au même instant peut encore entrer en collision.
    ⑩ EFFET — Crée le fichier du verrou s'il manque.
    ⑪ TERMINAISON — Rend la main au plus tard après `attente` secondes, plus 120 secondes pour le rev-parse (`git`) ;
      il n'est jamais tenu pendant le garde-fou.
      [sort: non]
    """
    _, commun = git(depot, "rev-parse", "--git-common-dir")
    chemin = os.path.join(depot, commun.strip() or ".git", "boucle_de_check_copies.verrou")
    f = open(chemin, "a")
    try:
        fin = time.monotonic() + attente
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return f
            except BlockingIOError:
                if time.monotonic() >= fin:
                    f.close()
                    return None
                time.sleep(0.05)
    except BaseException:
        f.close()
        raise


def proprietaire_vivant(nom):
    """Dit si le programme qui a créé une copie jetable est encore en marche.

    ① RÔLE — Empêcher le ménage d'un programme d'effacer la copie qu'un autre programme est en train d'utiliser.
    ② CONTEXTE D'APPEL — `nettoyer_les_copies`, pour chaque copie au préfixe du programme.
    ③ ENTRÉE — `nom` : le nom du dossier parent de la copie, « boucle_de_check_copie_<numéro du programme>_<hasard> ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : True si le numéro du programme créateur existe encore (un programme terminé mais pas encore
      ramassé par son parent compte) et n'est pas celui-ci ; False s'il n'existe plus, s'il est celui-ci, ou si le nom
      ne porte pas un numéro d'au plus 9 chiffres valant plus de 1 (copie d'avant ce correctif, dont le suffixe au
      hasard peut commencer par des chiffres : 0 viserait tout le groupe de programmes, 1 le premier programme du
      système, qui ne s'arrête jamais).
      [rend: 1]
    ⑥ TRAITEMENT — Lire le numéro dans le nom ; l'écarter s'il vaut 0 ou 1 ; le comparer au numéro de ce programme ;
      demander au système si ce numéro existe encore (signal 0, qui ne fait rien au programme visé) ; un refus du
      système (PermissionError : le programme existe mais appartient à un autre utilisateur) compte comme vivant.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le 16-10-2026 à 23h17, la série des sabotages jouait deux paquets en même temps sur un même clone :
      le ménage de l'un a effacé la copie de l'autre, et le programme intact a échoué (« le garde-fou n'existe pas
      dans cette version »). Reproduit le même soir : 4 vérifications simultanées sur un clone, 1 échec. La consigne « une seule
      surveillance par clone » et le verrou de `guetter` ne couvraient pas ce cas. Le numéro protège la copie pendant
      que le garde-fou tourne ; les commandes git qui créent et retirent les copies sont, elles, séparées par
      `prendre_le_verrou_des_copies` (relecture indépendante du même soir : le numéro seul laissait 18 échecs sur
      200). Une copie de ce programme-ci est forcément périmée : il ne fait qu'une vérification à la fois.
    ⑨ CE QUI CLOCHE — Un numéro de programme peut être réattribué par le système à un autre programme : la copie
      périmée reste alors en place jusqu'à l'arrêt de ce dernier. Elle encombre, elle ne fausse rien. · THÉORIQUE,
      non éprouvé : deux machines ou deux conteneurs qui partageraient un même clone ne voient pas les numéros l'un de
      l'autre — une copie de l'autre côté paraîtrait abandonnée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = re.match(re.escape(PREFIXE_DES_COPIES) + r"(\d{1,9})_", nom)
    if not m or int(m.group(1)) <= 1 or int(m.group(1)) == os.getpid():
        return False
    try:
        os.kill(int(m.group(1)), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def nettoyer_les_copies(depot):
    """Retire les copies de travail jetables qu'un arrêt brutal aurait laissées dans la copie du programme.

    ① RÔLE — Qu'un signal d'arrêt pendant une vérification ne laisse rien derrière lui.
    ② CONTEXTE D'APPEL — `verifier_la_note`, avant chaque copie.
    ③ ENTRÉE — `depot`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de copies que git a retirées (code 0).
      [rend: 1]
    ⑥ TRAITEMENT — git worktree list --porcelain ; chaque copie dont le dossier parent porte le préfixe du programme, et
      dont le programme créateur ne tourne plus (`proprietaire_vivant`), est retirée (git worktree remove --force
      --force : une copie dont la création a été tuée reste verrouillée « initializing », et un seul --force ne la
      retire pas), son dossier effacé ; puis git worktree prune ; puis, dans le dossier temporaire du système, les
      dossiers VIDES au préfixe d'un autre programme arrêté sont effacés — vides seulement : relecture indépendante,
      tour 11 — un dossier plein peut être la copie en usage d'un programme d'un autre espace de processus, dont le
      numéro paraît arrêté d'ici.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, point 10 : un arrêt pendant la vérification laissait une copie
      inscrite que « prune » ne retirait pas. Le verrou de `guetter` vient du second tour, point 7 : sans lui, une
      seconde surveillance retirait la copie en cours d'usage par la première. Le verrou ne couvre pas deux
      vérifications lancées hors surveillance (16-10-2026, 23h17) : la copie d'un programme vivant est épargnée.
      Le double --force, le compte juste et les dossiers vides : relecture indépendante, tour 10 (17-10-2026) — une
      copie tuée pendant sa création restait inscrite pour toujours, et était pourtant comptée comme retirée.
    ⑨ CE QUI CLOCHE — Les dossiers vides de ce programme-ci (verrou resté tenu) attendent son arrêt.
    ⑩ EFFET — Retire des copies de travail et leurs dossiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    _, sortie = git(depot, "worktree", "list", "--porcelain")
    n = 0
    for x in sortie.split("\n"):
        if x.startswith("worktree "):
            chemin = x[len("worktree "):]
            nom = os.path.basename(os.path.dirname(chemin))
            if nom.startswith(PREFIXE_DES_COPIES) and not proprietaire_vivant(nom):
                code, _ = git(depot, "worktree", "remove", "--force", "--force", chemin)
                shutil.rmtree(os.path.dirname(chemin), ignore_errors=True)
                n += code == 0
    git(depot, "worktree", "prune")
    # les dossiers jetables créés avant leur copie (arrêt avant « worktree add », ou verrou resté tenu) : git ne les
    # connaît pas ; ceux d'un programme arrêté sont effacés, jamais ceux de ce programme-ci (sa copie en cours)
    dossier = tempfile.gettempdir()
    for nom in os.listdir(dossier):
        m = re.match(re.escape(PREFIXE_DES_COPIES) + r"(\d{1,9})_", nom)
        if (m and int(m.group(1)) != os.getpid() and os.path.isdir(os.path.join(dossier, nom))
                and not proprietaire_vivant(nom)):
            try:
                os.rmdir(os.path.join(dossier, nom))     # VIDE seulement : un dossier plein n'est pas à ce balayage
            except OSError:
                pass
    return n


def verifier_la_note(depot, commit, fichier):
    """Fait passer une note par le garde-fou, en mode vérification, dans une copie jetable du commit.

    ① RÔLE — Dire si la note a vraiment passé le contrôle : la ligne « <!-- CONTROLE … --> » n'est que du texte, la
      vérification refait le contrôle (décision de Jean-Luc du 16-10-2026 à 19h21).
    ② CONTEXTE D'APPEL — `controler` ; les épreuves, sur la vraie relecture du 16-10-2026.
    ③ ENTRÉE — `depot` : un dépôt qui connaît le commit et origin/main · `commit` · `fichier` : la note.
    ④ CONDITIONS D'ENTRÉE — Le commit porte le garde-fou.
    ⑤ SORTIE — DEUX valeurs : le code du garde-fou (0 acceptée, autre refusée ; 2 s'il n'a pas pu tourner, si le
      verrou des copies est resté tenu par un autre, ou s'il
      n'a pas écrit le reçu du rôle — une version qui ignore « --attendu »), puis le motif en une ligne (les lignes
      « · » du refus, la ligne ❌, ou la ligne ✅).
      [rend: 2]
    ⑥ TRAITEMENT — ① sous le verrou des copies : nettoyer les copies laissées, puis git worktree add --detach dans un
      dossier temporaire au préfixe du programme suivi de son numéro · ③ python3 <garde-fou> <note> --verifier --attendu=<livraison pour la note du Chat, relecture pour
      celle de Cowork>, depuis cette copie, limité à 600 secondes, hors du verrou · ④ sous le verrou : retirer la copie, quoi qu'il arrive ;
      un verrou encore tenu par cette fonction est d'abord libéré ; s'il ne peut être repris dans l'attente, la copie
      reste, et le prochain nettoyage de ce programme la retire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une copie du commit : le garde-fou lit la note et ses voisins tels qu'ils ont été poussés. Le rôle
      attendu passe au garde-fou, qui le lit lui-même : relecture indépendante du 16-10-2026, troisième tour — une
      seconde lecture du rôle, ici, divergeait de la sienne, et une relecture sans gestes passait les deux.
    ⑨ CE QUI CLOCHE — Le garde-fou utilisé est celui du commit relu (voir ⑨ du programme).
    ⑩ EFFET — Crée et retire une copie de travail ; crée le fichier du verrou des copies s'il manque.
    ⑪ TERMINAISON — Rend la main au plus tard après 600 secondes de garde-fou, deux attentes du verrou de 300
      secondes chacune, et 120 secondes par commande git (`git` : rev-parse, worktree list, add, remove, prune, et un
      remove par copie laissée).
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix=f"{PREFIXE_DES_COPIES}{os.getpid()}_")
    copie = os.path.join(d, "depot")
    verrou = None
    try:
        verrou = prendre_le_verrou_des_copies(depot)
        if verrou is None:
            return 2, f"le verrou des copies est tenu par un autre programme depuis plus de {ATTENTE_DU_VERROU} secondes"
        try:
            nettoyer_les_copies(depot)
            code, _ = git(depot, "worktree", "add", "--detach", copie, commit)
        finally:
            verrou.close()
            verrou = None
        if code != 0:
            return 2, "copie du commit impossible (git worktree)"
        if not os.path.isfile(os.path.join(copie, GARDE_FOU)):
            return 2, "le garde-fou n'existe pas dans cette version"
        try:
            r = subprocess.run([sys.executable, GARDE_FOU, fichier, "--verifier", f"--attendu={ATTENDU[fichier]}"],
                               cwd=copie, capture_output=True,
                               text=True, errors="replace", timeout=600)
        except subprocess.TimeoutExpired:
            return 2, "le garde-fou n'a pas rendu sa réponse en 600 secondes"
        lignes = [x.strip() for x in r.stdout.split("\n")]
        if not any(x.startswith(RECU_DU_ROLE) for x in lignes):
            return 2, ("ce garde-fou ne sait pas contrôler le rôle (aucune ligne « rôle attendu : … ») : une version "
                       "antérieure au 16-10-2026 ne peut pas vérifier une note de la boucle")
        if r.returncode == 0:
            return 0, next((x for x in lignes if x.startswith("✅")), "acceptée")
        motifs = [x.lstrip("· ").strip() for x in lignes if x.startswith("·")]
        return r.returncode, " | ".join(motifs) or next((x for x in lignes if x.startswith("❌")), "refusée")
    finally:
        if verrou is not None:          # interrompu entre la prise et la libération : libérer avant de reprendre
            verrou.close()
        verrou = prendre_le_verrou_des_copies(depot)
        if verrou is not None:
            try:
                git(depot, "worktree", "remove", "--force", "--force", copie)
                shutil.rmtree(d, ignore_errors=True)
                git(depot, "worktree", "prune")
            finally:
                verrou.close()


def controler(depot, commit, fichier):
    """Contrôle une note par le garde-fou et rend un code ramené à trois valeurs, avec le motif.

    ① RÔLE — Un seul contrôle pour la note de l'autre et pour la mienne.
    ② CONTEXTE D'APPEL — `un_regard`.
    ③ ENTRÉE — `depot` · `commit` · `fichier`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : 0 acceptée, 1 refusée, 2 contrôle impossible ; puis le motif.
      [rend: 2]
    ⑥ TRAITEMENT — `verifier_la_note`, dont le code est ramené à 0, 1 ou 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le garde-fou rend 1 pour un refus ; tout autre code non nul que 2 est aussi un refus.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `verifier_la_note`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    code, motif = verifier_la_note(depot, commit, fichier)
    return (code if code in (0, 2) else 1), motif


def un_regard(depot, cote, maintenant):
    """Regarde une fois le dépôt et rend l'événement, ou None s'il n'y a rien à dire.

    ① RÔLE — Le cœur de la surveillance : un seul regard, sans attente, pour que les épreuves le jouent sans horloge.
    ② CONTEXTE D'APPEL — `guetter`, toutes les `intervalle` secondes ; les épreuves, directement.
    ③ ENTRÉE — `depot` : la copie du programme · `cote` : « chat » ou « cowork » · `maintenant` : l'heure en secondes
      depuis 1970.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None (rien à dire), ou un couple (code, ligne) : code 0 pour un événement, 2 pour une
      erreur ; la ligne commence par « TOUR À FAIRE », « NOTE REFUSÉE », « MA NOTE REFUSÉE », « ARRÊT » ou « ERREUR ».
      [rend: 1 ou 2]
    ⑥ TRAITEMENT — ① git fetch --prune ; un échec rend une erreur · ② versions en attente : aucune ou plusieurs → arrêt ·
      ③ les dernières notes des deux côtés écrites depuis que la version a quitté origin/main · ④ à qui le tour : à moi
      si la note de l'autre existe et que la mienne est absente, en est un ancêtre, ou — quand aucune n'est l'ancêtre de
      l'autre (une fusion) — est plus ancienne à l'horloge ; même commit, ou même heure sans ordre → arrêt « notes
      concurrentes » · ⑤ pas mon tour : ma note est contrôlée une fois — refusée → « MA NOTE REFUSÉE » ; acceptée et
      plus vieille que 3 heures, refusée ou non → arrêt (silence) ; sinon None · ⑥ mon tour : la note de l'autre a disparu → arrêt ; un
      arrêt écrit en tête → arrêt ; pas de ligne de lancement sur cette version → arrêt ; 10 allers-retours ou plus →
      arrêt · ⑦ contrôle de la note de l'autre : refusée → « NOTE REFUSÉE », puis, si elle n'est pas corrigée en 3
      heures, arrêt (silence) ; acceptée → « TOUR À FAIRE » · ⑧ un arrêt ou un refus déjà annoncé (mémoire) n'est pas
      redit : None. La fin d'une boucle (« aucune version ») est annoncée une fois par état de origin/main.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Le tour se lit à l'ordre des deux notes et non à un commit de départ : après une relance, une réponse
      arrivée pendant l'arrêt de la surveillance est vue. Ma propre note contrôlée : relecture indépendante du 16-10-2026,
      second tour, point 3 — sans cela, un refus du garde-fou faisait échanger des refus aux deux côtés jusqu'au budget,
      sans que la note fautive soit jamais réparée. Les notes concurrentes : même relecture, point 1 — une fusion rendait
      la boucle muette des deux côtés, pour toujours.
    ⑨ CE QUI CLOCHE — Le silence se mesure à l'heure du commit de la note attendue. · Le verdict sur ma propre note est
      gardé par commit : si origin/main avance et change ce verdict, il n'est pas recalculé. · Un lancement à la main
      consomme les annonces comme la vraie surveillance : le texte de la boucle dit de ne pas en lancer pendant qu'une
      surveillance tourne.
    ⑩ EFFET — git fetch dans la copie du programme ; des copies jetables pendant les contrôles ; la mémoire écrite.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    nom, ma_note, sa_note = COTES[cote]
    mem = memoire(depot, cote)

    def annoncer(cle, ligne):
        """Rend un événement la première fois qu'il se produit, et rien les fois suivantes.

        ① RÔLE — Qu'un arrêt ou un refus ne soit annoncé qu'une fois, même si la surveillance est relancée.
        ② CONTEXTE D'APPEL — `un_regard`, pour chaque arrêt et chaque refus.
        ③ ENTRÉE — `cle` : ce qui identifie l'événement — sa nature, suivie du ou des commits concernés, ou des noms
          des versions en attente pour l'arrêt « plusieurs versions » · `ligne` : la ligne à écrire.
        ④ CONDITIONS D'ENTRÉE — `mem` et `depot`, `cote`, de `un_regard`.
        ⑤ SORTIE — UNE valeur : None si la clé a déjà été annoncée ; sinon le couple (0, ligne).
          [rend: 1 ou 2]
        ⑥ TRAITEMENT — Chercher la clé dans la mémoire ; absente : l'ajouter et écrire la mémoire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Chaque relance de la surveillance referait voir le même arrêt : sans mémoire, Jean-Luc
          recevrait la même alerte toutes les 30 minutes.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit la mémoire du côté.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if cle in mem["annonces"]:
            return None
        mem["annonces"].append(cle)
        memoire(depot, cote, mem)
        return 0, ligne

    code, _ = git(depot, "fetch", "-q", "--prune", "origin", "+refs/heads/*:refs/remotes/origin/*", limite=180)
    if code != 0:
        return 2, f"ERREUR · le fetch a échoué (code {code})"
    versions = versions_en_attente(depot)
    if not versions:
        return annoncer("aucune version après " + (git(depot, "rev-parse", "origin/main")[1] or "?"),
                        "ARRÊT · aucune version en attente travail-* : rien à relire (fusionnée, ou pas encore poussée)")
    if len(versions) > 1:
        return annoncer("plusieurs " + " ".join(versions), "ARRÊT · plusieurs versions en attente : "
                        + " ".join(versions) + " — Jean-Luc tranche (A-448)")
    branche = versions[0]
    base = git(depot, "merge-base", "origin/main", "origin/" + branche)[1] or None
    sien, son_heure = dernier_commit(depot, branche, sa_note, base)
    mien, mon_heure = dernier_commit(depot, branche, ma_note, base)
    if sien and mien and (sien == mien or (not est_ancetre(depot, mien, sien) and not est_ancetre(depot, sien, mien)
                                           and son_heure == mon_heure)):
        return annoncer("concurrentes " + sien + " " + mien,
                        f"ARRÊT · NOTES CONCURRENTES · {branche} · {sien[:7]} et {mien[:7]} : aucune n'est écrite après "
                        "l'autre — Jean-Luc tranche qui joue")
    mon_tour = sien is not None and (mien is None or est_ancetre(depot, mien, sien)
                                     or (not est_ancetre(depot, sien, mien) and son_heure > mon_heure))
    if not mon_tour:
        if mien is None:
            return None
        cle = ma_note + "@" + mien
        if cle not in mem["verifiees"]:
            mem["verifiees"][cle] = list(controler(depot, mien, ma_note))
            memoire(depot, cote, mem)
        code, motif = mem["verifiees"][cle]
        if code == 2:
            del mem["verifiees"][cle]
            memoire(depot, cote, mem)
            return 2, f"ERREUR · {branche} · {mien[:7]} · le garde-fou n'a pas pu tourner sur ma note : {motif}"
        if code != 0:
            r = annoncer("ma note refusée " + mien, f"MA NOTE REFUSÉE · {branche} · {mien[:7]} · {motif}")
            if r:
                return r
        if maintenant - mon_heure > SILENCE:
            heures = (maintenant - mon_heure) / 3600
            return annoncer("silence " + mien,
                            f"ARRÊT · SILENCE · {branche} · aucune note de l'autre côté depuis ma note {mien[:7]}, "
                            f"il y a {heures:.1f} h (limite {SILENCE // 3600} h)")
        return None
    note = lire_au_commit(depot, "origin/" + branche, sa_note)
    if note is None:
        return annoncer("supprimée " + sien,
                        f"ARRÊT · NOTE SUPPRIMÉE · {branche} · {sien[:7]} · {sa_note} n'existe plus sur la version")
    ecrit = arret_ecrit(note)
    if ecrit:
        return annoncer("écrit " + sien, f"ARRÊT · ÉCRIT PAR L'AUTRE CÔTÉ · {branche} · {sien[:7]} · {ecrit}")
    ligne = derniere_ligne_de_lancement(lignes_de_la_version(depot, branche, base))
    if ligne is None:
        return annoncer("non lancée " + sien,
                        f"ARRÊT · BOUCLE NON LANCÉE · {branche} · {sien[:7]} · le journal {JOURNAL} de cette version ne "
                        "porte aucune ligne « BOUCLE LANCÉE » du Chat : seule la réponse de Jean-Luc lance la boucle")
    n = allers_retours(depot, branche, ligne)
    if n is None:
        return 2, f"ERREUR · {branche} · le commit de la ligne de lancement est introuvable"
    if n >= BUDGET:
        return annoncer("budget " + sien,
                        f"ARRÊT · BUDGET · {branche} · {sien[:7]} · {n} allers-retours depuis le dernier lancement "
                        f"(limite {BUDGET}) : Jean-Luc dit s'il continue")
    cle = sa_note + "@" + sien
    if cle not in mem["verifiees"]:
        code, motif = controler(depot, sien, sa_note)
        if code != 2:                                   # une erreur se retente au regard suivant
            mem["verifiees"][cle] = [code, motif]
            memoire(depot, cote, mem)
    else:
        code, motif = mem["verifiees"][cle]
    signal_ = " · ATTENTION : le garde-fou a changé sur cette version" if garde_fou_change(depot, sien) else ""
    if code == 2:
        return 2, f"ERREUR · {branche} · {sien[:7]} · le garde-fou n'a pas pu tourner : {motif}"
    if code != 0:
        r = annoncer("refusée " + sien, f"NOTE REFUSÉE · {branche} · {sien[:7]} · {motif}{signal_}")
        if r is None and maintenant - son_heure > SILENCE:
            r = annoncer("silence après refus " + sien,
                         f"ARRÊT · SILENCE · {branche} · la note refusée {sien[:7]} n'a pas été corrigée depuis "
                         f"{(maintenant - son_heure) / 3600:.1f} h (limite {SILENCE // 3600} h)")
        return r
    return 0, (f"TOUR À FAIRE · {branche} · {sien[:7]} · la note de l'autre côté passe le garde-fou · "
               f"{n} allers-retours sur {BUDGET}{signal_}")


def _arret_propre(signum, cadre):
    """Change un signal d'arrêt en sortie ordinaire, pour que le nettoyage des blocs « finally » se fasse.

    ① RÔLE — Qu'un arrêt demandé (SIGTERM, celui de l'outil Monitor) ne laisse pas de copie de travail derrière lui.
    ② CONTEXTE D'APPEL — Installé par `guetter` pour SIGTERM ; appelé par le système à la réception du signal.
    ③ ENTRÉE — `signum` : le numéro du signal · `cadre` : le cadre d'exécution interrompu (inutilisé).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur : lève SystemExit(2).
      [rend: rien]
    ⑥ TRAITEMENT — Lever SystemExit(2), que les blocs « finally » laissent passer après avoir fait leur nettoyage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 16-10-2026, point 10 : sans ce changement, SIGTERM tuait le programme
      sans exécuter les « finally », et la copie de travail restait inscrite dans le clone.
    ⑨ CE QUI CLOCHE — SIGKILL ne se rattrape pas, et un SIGTERM reçu pendant un « finally » en saute la fin :
      dans les deux cas, `nettoyer_les_copies` retire la copie au regard suivant, son programme étant arrêté.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Lève toujours.
      [sort: oui]
    """
    raise SystemExit(2)


def guetter(clone, cote, intervalle, dossier=None, regard=None):
    """Regarde le dépôt toutes les `intervalle` secondes jusqu'à un événement, et l'écrit.

    ① RÔLE — La surveillance elle-même, telle que l'outil Monitor la lance.
    ② CONTEXTE D'APPEL — `main`, sans « --noter » ; les épreuves.
    ③ ENTRÉE — `clone` : le clone guetté · `cote` · `intervalle` en secondes · `dossier` : la copie du programme (None :
      par défaut) · `regard` : la fonction de regard (None : `un_regard` ; les épreuves en passent une autre).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie (0 événement, 2 erreur) ; les lignes sont écrites au fil de l'eau.
      [rend: 1]
    ⑥ TRAITEMENT — ① SIGTERM devient une sortie propre · ② préparer la copie du programme · ③ prendre son verrou, sans
      attendre : déjà pris → erreur · ④ écrire « GUETTE … » · ⑤ un regard ; None → attendre et recommencer, et le
      compte d'erreurs repart de zéro · ⑥ un événement → l'écrire et rendre son code · ⑦ trois erreurs de suite →
      rendre 2.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Une erreur passagère du réseau ne doit pas arrêter la boucle ; trois de suite, si (R-734). Le verrou :
      relecture indépendante du 16-10-2026, second tour, point 7.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `copie_du_programme` et de `un_regard` ; le verrou tombe avec le processus.
    ⑪ TERMINAISON — Tourne jusqu'à un événement ou trois erreurs ; arrêté de l'extérieur sinon.
      [sort: non]
    """
    signal.signal(signal.SIGTERM, _arret_propre)
    nom, ma_note, sa_note = COTES[cote]
    depot, motif = copie_du_programme(clone, dossier)
    if depot is None:
        print(f"ERREUR · {motif}", flush=True)
        return 2
    verrou = open(os.path.join(depot, ".git", "boucle_de_check.verrou"), "w")
    try:
        fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print(f"ERREUR · une surveillance tourne déjà sur la copie {depot}", flush=True)
        return 2
    regard = regard or un_regard
    print(f"GUETTE · {nom} · note attendue : {sa_note} · copie du programme : {depot}", flush=True)
    erreurs = 0
    while True:
        r = regard(depot, cote, time.time())
        if r is not None:
            code, ligne = r
            print(ligne, flush=True)
            if code != 2:
                return 0
            erreurs += 1
            if erreurs >= 3:
                print("ERREUR · trois erreurs de suite : la surveillance s'arrête (R-734)", flush=True)
                return 2
        else:
            erreurs = 0
        time.sleep(intervalle)


def noter(clone, cote, commit, texte, maintenant=None):
    """Ajoute au journal de la boucle une ligne dans la forme fixe, et la rend.

    ① RÔLE — Écrire la ligne du journal toujours de la même façon, pour que le programme la retrouve.
    ② CONTEXTE D'APPEL — `main`, avec « --noter » ; chaque conversation, à la fin de chaque tour ; le Chat, au
      lancement (« BOUCLE LANCÉE · <sujet> ») et quand Jean-Luc dit de continuer (« BOUCLE CONTINUÉE · accord de
      Jean-Luc de HHhMM »).
    ③ ENTRÉE — `clone` · `cote` · `commit` : le commit de la note du tour · `texte` : ce qui a été trouvé ou réparé ·
      `maintenant` : un datetime, pour les épreuves.
    ④ CONDITIONS D'ENTRÉE — Le texte tient sur une ligne ; ses sauts de ligne sont remplacés par des espaces.
    ⑤ SORTIE — UNE valeur : la ligne écrite, par exemple
      « - 2026-10-16 19h40 Paris · Chat · 655103c · BOUCLE LANCÉE · le filet de la nuit ».
      [rend: 1]
    ⑥ TRAITEMENT — ① former la ligne à l'heure de Paris · ② créer le journal avec son en-tête s'il n'existe pas ·
      ③ ajouter la ligne en fin de fichier.
    ⑦ UNITÉ — Heure de Paris, à la minute.
    ⑧ POURQUOI — Ce qui se calcule ne s'écrit pas à la main (R-728) : la forme de la ligne vit ici, une fois.
    ⑨ CE QUI CLOCHE — Le programme écrit dans le clone sans commit ; c'est la conversation qui pousse.
    ⑩ EFFET — Écrit echanges/JOURNAL_DE_LA_BOUCLE.md dans le clone.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    nom = COTES[cote][0]
    quand = (maintenant or datetime.now(PARIS)).astimezone(PARIS)
    ligne = (f"- {quand.strftime('%Y-%m-%d %Hh%M')} Paris · {nom} · {commit[:7]} · "
             + " ".join(texte.split()))
    chemin = os.path.join(clone, JOURNAL)
    if not os.path.isfile(chemin):
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("FABRIQUÉ · Rôle : le journal de la boucle de check, une ligne par tour, écrite par "
                    "programmes/BOUCLE_DE_CHECK.py --noter.\nQuand l'appeler : pour savoir où en est la boucle.\n\n"
                    "# JOURNAL DE LA BOUCLE DE CHECK\n\n")
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")
    return ligne


def main():
    """Lit la ligne de commande et lance la surveillance ou la ligne du journal.

    ① RÔLE — Point d'entrée.
    ② CONTEXTE D'APPEL — Lancé seul (voir ② du programme).
    ③ ENTRÉE — Les arguments de la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Le clone existe.
    ⑤ SORTIE — Aucune valeur rendue : sort par sys.exit (0 événement ou ligne écrite, 2 sinon).
      [rend: rien]
    ⑥ TRAITEMENT — argparse ; « --noter » exige « --commit » et « --texte ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un argument manquant est une erreur dite, jamais un comportement par défaut (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `guetter` ou de `noter`.
    ⑪ TERMINAISON — Sort par sys.exit.
      [sort: oui]
    """
    p = argparse.ArgumentParser(description="La partie mécanique de la boucle de check.")
    p.add_argument("clone")
    p.add_argument("--cote", required=True, choices=sorted(COTES))
    p.add_argument("--intervalle", type=int, default=60)
    p.add_argument("--copie")
    p.add_argument("--noter", action="store_true")
    p.add_argument("--commit")
    p.add_argument("--texte")
    a = p.parse_args()
    if not os.path.isdir(a.clone):
        print(f"ERREUR · le clone {a.clone} n'existe pas", flush=True)
        sys.exit(2)
    if a.noter:
        if not a.commit or not a.texte:
            print("ERREUR · --noter exige --commit et --texte", flush=True)
            sys.exit(2)
        print(noter(a.clone, a.cote, a.commit, a.texte), flush=True)
        sys.exit(0)
    sys.exit(guetter(a.clone, a.cote, a.intervalle, a.copie))


if __name__ == "__main__":
    main()
