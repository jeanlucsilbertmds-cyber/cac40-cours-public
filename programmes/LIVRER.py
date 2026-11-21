#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LIVRER.py — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Demande de Jean-Luc du 20-11-2026 à 19h38 : le Chat arrête de piloter de mémoire les gestes
opérationnels ; un PROGRAMME les enchaîne, toujours dans le même ordre (R-754 : ce qu'un programme peut faire, un
programme le fait). Ce qui avait raté ce jour-là : une installation sur main à 15h29 sans republication au public
(le circuit du soir est tombé) ; des épreuves longues jamais envoyées sur GitHub ; Cowork lancé avant GitHub, qui a
donc rejoué lui-même les épreuves longues ; deux demandes refusées par le relais, faute de file d'attente ; une
mauvaise consigne de branche donnée à la publication (worktree détaché, refusé par `refus_de_branche`).
Ajout du 20-11-2026 à 19h40 (question de Jean-Luc : « comment piloter un graphe d'actions parallèles si tu ne sais
pas qui fait quoi ? ») : chaque lancement s'écrit dans UN registre, le dossier etudes/REGISTRE_DES_TRAVAUX/ (un
fichier JSON par entrée), relu par programmes/QUI_FAIT_QUOI.py contre les sources vivantes.
Réparation du 20-11-2026 au soir (relecteur neuf : « NON DÉPLOYABLE » ; superviseur R-759 : « RUSTINE, À REPRENDRE,
AVEC SIMPLIFICATION ») : un PLANTAGE (exception imprévue) sort en code 5, jamais lu comme un verdict ; la poussée
privée refait « pull --rebase » puis retente ; le registre ne s'écrit qu'en fichiers neufs ; un résultat d'épreuve
n'est cru que si son RESULTAT.json porte la pointe jouée ; une demande qui voit deux passages s'arrête.

① RÔLE — Après chaque livraison poussée sur une branche travail-*, enchaîner : ① la note de la branche est acceptée
  (CONTROLER_MA_LIVRAISON.py --verifier) · ② le code de la branche est publié sur la branche publique du même nom ·
  ③ les épreuves longues de la note sont relevées et confrontées à tests/LANCEMENT_DES_EPREUVES.json · ④ leur demande
  est déposée au relais, avec attente quand un passage occupe la file · ⑤ le passage est suivi jusqu'au bout, ses
  résultats lus au dépôt privé et résumés dans la note (section « RÉSULTATS GITHUB »), poussée · ⑥ le code de sortie
  dit au Chat s'il peut lancer Cowork.
② CONTEXTE D'APPEL — À la main par le Chat, depuis la racine de son clone privé :
  python3 -B programmes/LIVRER.py <branche travail-…> [--plafond=<minutes>]
  Jamais par un circuit. Le programme NE LANCE PAS Cowork : il n'en a pas l'outil ; le Chat le lance sur le code 0.
③ ENTRÉE — La ligne de commande : la branche (forme travail-…, MOTIF_DE_VERSION du fabricant) ; « --plafond » : le
  temps d'attente permis à CHAQUE attente (file du relais, passage), en minutes, 240 par défaut. Variables
  d'environnement facultatives, pour les épreuves (tests/EPREUVES_DE_LIVRER_ET_INSTALLER_Ven_20-11-2026.py) :
  LIVRER_GH (le programme gh), LIVRER_DEPOT_PUBLIC (l'adresse de clonage du public), LIVRER_REPO_PUBLIC et
  LIVRER_REPO_PRIVE (« propriétaire/nom » pour gh), LIVRER_FABRICANT, LIVRER_GARDE_FOU, LIVRER_RAPATRIEUR (les
  programmes lancés), LIVRER_PAS (secondes entre deux regards, 30 par défaut).
④ CONDITIONS D'ENTRÉE — Lancé dans un clone git du dépôt privé dont « origin » est le privé ; git et gh installés et
  autorisés ; la branche existe sur origin ; sa note echanges/A_RELIRE.md porte une section dont le titre contient
  « À JOUER SUR GITHUB » (une liste de codes ou de chemins d'épreuves, ou la ligne « aucune »).
⑤ SORTIE — Le code de sortie : 0 PRÊT POUR COWORK · 1 ÉPREUVE ROUGE (au moins une épreuve longue rend un code non
  nul) · 2 LA NOTE NE DIT PAS QUOI JOUER (section absente, ou un nom sans code dans la table) · 3 ÉTAPE TOMBÉE (note
  refusée, branche locale en avance, publication refusée, relais qui refuse pour une autre raison, plafond dépassé,
  deux passages pour une demande, résultat absent ou d'une autre pointe, poussée privée refusée après
  ESSAIS_DE_POUSSEE essais) · 5 PLANTAGE (une exception imprévue : ni un verdict, ni un refus ; le registre et la note
  sont quand même poussés). Chaque étape affiche une ligne « ÉTAPE n … ».
⑥ TRAITEMENT — Les six étapes ci-dessus, dans l'ordre, arrêt au premier échec ; le registre reçoit une ligne au
  lancement de chaque travail et une à sa fin, et il est commité et poussé sur la branche à la sortie, même en échec.
⑦ UNITÉ — Des minutes (le plafond), des secondes (le pas), des heures de Paris (le registre).
⑧ POURQUOI — Voir le sens en tête. Chaque geste RÉUTILISE ce qui existe (R-708) : le garde-fou pour la note, le
  fabricant pour la publication (avec sa garde `refus_de_branche`), le format de demande et les noms des circuits lus
  dans le fabricant, la table des épreuves longues, le rapatrieur tests/outils/rapatrier_les_epreuves_longues.py
  pour les résultats.
⑨ CE QUI CLOCHE — Les variables d'environnement LIVRER_* peuvent rediriger les programmes lancés : elles servent aux
  épreuves, et la sortie affiche ce qui est lancé. Les lignes de registre écrites entre la demande et la fin du
  passage ne vivent que dans le worktree jusqu'à la sortie : pousser la branche pendant le passage changerait sa
  pointe, que la porte « preparer » du circuit compare à la demande. Un arrêt brutal (machine éteinte) les perd ;
  QUI_FAIT_QUOI.py lit aussi les worktrees locaux. Un tiers qui pousse sur la branche pendant le passage fait
  échouer ce passage côté GitHub (la porte compare la pointe) : LIVRER ne le voit qu'au résultat ; sa propre poussée
  finale se rebase sur le tiers et ne perd rien. La réécriture de la note à l'étape ⑤ relance le garde-fou en mode
  écriture (nouvelle ligne de contrôle) : s'il refuse, la sortie est 3 et la note n'est pas poussée.
⑩ EFFET — Crée et retire des worktrees du dépôt privé, clone le public sous /tmp (jamais /home/claude/pub), pousse
  sur la branche publique du même nom (par le fabricant, puis la demande) et sur la branche privée (note, registre),
  jamais sur main, jamais en force.
⑪ TERMINAISON — Sort du programme par sys.exit. Chaque commande lancée est bornée ; les attentes sont bornées par le
  plafond.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import unicodedata
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
PRET, ROUGE, NOMS, TOMBE, PLANTAGE = 0, 1, 2, 3, 5
ESSAIS_DE_POUSSEE = 3   # poussées privées tentées au plus, chacune après un « pull --rebase » (sauf la première)
REGISTRE = None   # lu au contrat (CONTRATS_DES_FICHIERS.REGISTRE_DES_TRAVAUX, un dossier), juste après `charger`
NOTE = "echanges/A_RELIRE.md"
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
GARDE_FOU = "programmes/CONTROLER_MA_LIVRAISON.py"
RAPATRIEUR = "tests/outils/rapatrier_les_epreuves_longues.py"
TITRE_DES_EPREUVES = "A JOUER SUR GITHUB"
TITRE_DES_RESULTATS = "## RÉSULTATS GITHUB"
DEPOT_PUBLIC = "https://github.com/jeanlucsilbertmds-cyber/cac40-cours-public.git"
REPO_PUBLIC = "jeanlucsilbertmds-cyber/cac40-cours-public"
INTERDIT_POUR_LE_CLONE_PUBLIC = "/home/claude/pub"


class Arret(Exception):
    """Un échec d'étape : porte le code de sortie et le message.

    ① RÔLE — Remonter un échec jusqu'à `main` avec son code (1, 2 ou 3).
    ② CONTEXTE D'APPEL — Levée par les étapes, attrapée par `main` de LIVRER et d'INSTALLER.
    ③ ENTRÉE — Celle d'Exception : le code, puis le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un seul chemin de sortie pour tous les échecs : le registre est écrit et poussé dans tous les cas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """


def maintenant():
    """Rend l'heure de Paris, « AAAA-MM-JJ HH:MM:SS ».

    ① RÔLE — L'horodatage du registre et des notes.
    ② CONTEXTE D'APPEL — Partout où une heure s'écrit.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — datetime.now(Europe/Paris).
    ⑦ UNITÉ — Heure de Paris, à la seconde.
    ⑧ POURQUOI — Horodatage Europe/Paris exigé par les instructions du projet.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit l'horloge.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return datetime.now(PARIS).strftime("%Y-%m-%d %H:%M:%S")


def dire(texte):
    """Affiche une ligne tout de suite.

    ① RÔLE — Le compte rendu du programme, ligne à ligne.
    ② CONTEXTE D'APPEL — Partout.
    ③ ENTRÉE — `texte` : la ligne.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — print avec vidage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le Chat suit un programme long par sa sortie ; une ligne gardée en mémoire tampon ne se voit pas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sur la sortie.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    print(texte, flush=True)


def lancer(commande, dossier=None, borne=900, entree=None):
    """Lance une commande, sortie capturée en texte ; rend le résultat.

    ① RÔLE — Le seul endroit où ce programme lance un autre programme.
    ② CONTEXTE D'APPEL — `git`, `gh`, les étapes.
    ③ ENTRÉE — `commande` : la liste des mots · `dossier` : où la lancer · `borne` : secondes au plus · `entree` :
      le texte donné sur l'entrée, ou None.
    ④ CONDITIONS D'ENTRÉE — Le premier mot désigne un programme installé.
    ⑤ SORTIE — UNE valeur : un subprocess.CompletedProcess ; une commande absente ou trop longue rend un résultat de
      code 127 ou 124, jamais une exception.
      [rend: 1]
    ⑥ TRAITEMENT — subprocess.run, sortie et erreur capturées.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Une commande qui ne revient pas ne doit pas figer le programme ; une commande absente doit se dire.
    ⑨ CE QUI CLOCHE — La sortie entière est gardée en mémoire.
    ⑩ EFFET — Ce que fait la commande.
    ⑪ TERMINAISON — Rend la main après `borne` secondes au plus.
      [sort: non]
    """
    try:
        return subprocess.run(commande, cwd=dossier, capture_output=True, text=True, timeout=borne, input=entree)
    except FileNotFoundError as e:
        return subprocess.CompletedProcess(commande, 127, "", f"commande introuvable : {e}")
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(commande, 124, "", f"commande arrêtée après {borne} s")


def git(racine, *args, borne=600):
    """Lance git dans un dépôt ; rend le résultat.

    ① RÔLE — Un appel git borné.
    ② CONTEXTE D'APPEL — Partout.
    ③ ENTRÉE — `racine` : le dépôt · `args` : les arguments · `borne` : secondes au plus.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le résultat de `lancer`.
      [rend: 1]
    ⑥ TRAITEMENT — « git -C racine args ».
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — R-708 : une seule écriture de l'appel.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ce que fait git.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return lancer(["git", "-C", racine] + list(args), borne=borne)


def gh(*args, borne=300):
    """Lance gh ; rend le résultat.

    ① RÔLE — Un appel gh borné, par le programme désigné par LIVRER_GH (le vrai gh par défaut).
    ② CONTEXTE D'APPEL — Les étapes qui lisent GitHub.
    ③ ENTRÉE — `args` : les arguments · `borne` : secondes au plus.
    ④ CONDITIONS D'ENTRÉE — gh est autorisé (jeton jamais affiché, jamais lu ici).
    ⑤ SORTIE — UNE valeur : le résultat de `lancer`.
      [rend: 1]
    ⑥ TRAITEMENT — [LIVRER_GH ou « gh »] + args.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Les épreuves remplacent gh par un faux, sans réseau.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ce que fait gh.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return lancer([os.environ.get("LIVRER_GH", "gh")] + list(args), borne=borne)


def gh_json(*args):
    """Lance gh et lit sa sortie JSON ; lève Arret(3) si gh échoue ou rend autre chose que du JSON.

    ① RÔLE — Lire une réponse de gh en données.
    ② CONTEXTE D'APPEL — Les regards sur les passages.
    ③ ENTRÉE — `args` : les arguments de gh (avec --json).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'objet lu.
      [rend: 1]
    ⑥ TRAITEMENT — `gh`, puis json.loads.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une réponse illisible n'est jamais lue comme « rien ne tourne » (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `gh`.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    r = gh(*args)
    if r.returncode != 0:
        raise Arret(TOMBE, f"gh {' '.join(args[:3])} : code {r.returncode} : {(r.stderr or r.stdout).strip()[:200]}")
    try:
        return json.loads(r.stdout or "null")
    except ValueError:
        raise Arret(TOMBE, f"gh {' '.join(args[:3])} : réponse illisible")


def repo_public():
    """Rend « propriétaire/nom » du dépôt public pour gh.

    ① RÔLE — Nommer le dépôt public à un endroit.
    ② CONTEXTE D'APPEL — Les regards gh.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom.
      [rend: 1]
    ⑥ TRAITEMENT — LIVRER_REPO_PUBLIC, sinon REPO_PUBLIC.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves le remplacent.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return os.environ.get("LIVRER_REPO_PUBLIC", REPO_PUBLIC)


def repo_prive(racine):
    """Rend « propriétaire/nom » du dépôt privé, lu dans l'adresse d'origin.

    ① RÔLE — Nommer le dépôt privé pour gh sans le recopier (il est écrit dans le clone).
    ② CONTEXTE D'APPEL — INSTALLER (A-818) et QUI_FAIT_QUOI.
    ③ ENTRÉE — `racine` : le clone privé.
    ④ CONDITIONS D'ENTRÉE — origin est une adresse GitHub, sauf LIVRER_REPO_PRIVE donné.
    ⑤ SORTIE — UNE valeur : le nom, ou lève Arret(3).
      [rend: 1]
    ⑥ TRAITEMENT — LIVRER_REPO_PRIVE, sinon ce qui suit le dernier « github.com » de « git remote get-url origin » :
      deux morceaux séparés par « / », sans « .git » (lecture par partition, sans expression régulière : un motif qui
      reconnaît une adresse GitHub est pris pour un motif de jeton par l'épreuve E8 du circuit public, et il n'en faut
      qu'un, dans programmes/FORME_D_UN_JETON.py).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — L'adresse n'est jamais affichée (elle pourrait porter un jeton).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    if os.environ.get("LIVRER_REPO_PRIVE"):
        return os.environ["LIVRER_REPO_PRIVE"]
    adresse = git(racine, "remote", "get-url", "origin").stdout.strip()
    _, trouve, reste = adresse.rpartition("github.com")
    morceaux = [x for x in reste.lstrip(":/").rstrip("/").removesuffix(".git").partition("/")[::2] if x]
    if not trouve or len(morceaux) != 2 or "/" in morceaux[1]:
        raise Arret(TOMBE, "le dépôt privé n'est pas lisible dans l'adresse d'origin (adresse non affichée)")
    return f"{morceaux[0]}/{morceaux[1]}"


def charger(chemin, nom):
    """Charge un programme Python comme module, par son chemin.

    ① RÔLE — Lire les constantes du fabricant et les fonctions de LIVRER là où elles sont écrites (R-708).
    ② CONTEXTE D'APPEL — `constantes_du_fabricant`, INSTALLER, QUI_FAIT_QUOI.
    ③ ENTRÉE — `chemin` : le fichier · `nom` : le nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et s'importe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une valeur recopiée finit par différer.
    ⑨ CE QUI CLOCHE — Le code de tête du module s'exécute (le fabricant lit sa table).
    ⑩ EFFET — Exécute le module.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REGISTRE = charger(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CONTRATS_DES_FICHIERS.py"),
                   "CONTRATS_DE_LIVRER").REGISTRE_DES_TRAVAUX


def constantes_du_fabricant(racine):
    """Rend les noms de circuits et motifs lus dans le fabricant de la racine.

    ① RÔLE — Les noms du relais, du circuit des épreuves, du groupe long, et le motif de version, d'un tenant.
    ② CONTEXTE D'APPEL — `main` et INSTALLER.
    ③ ENTRÉE — `racine` : la racine où lire programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py.
    ④ CONDITIONS D'ENTRÉE — Le fabricant s'importe.
    ⑤ SORTIE — UNE valeur : un dict (relais, epreuves, groupe_long, motif_version, nom_de_demande).
      [rend: 1]
    ⑥ TRAITEMENT — `charger`, puis lecture de CIRCUIT_RELAIS, CIRCUIT_EPREUVES, CIRCUITS_DU_GROUPE_LONG,
      MOTIF_DE_VERSION, NOM_DE_DEMANDE.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : ces noms sont écrits une fois, dans le fabricant.
    ⑨ CE QUI CLOCHE — Un fabricant qui ne s'importe pas fait lever Arret(3).
    ⑩ EFFET — Exécute le fabricant comme module (lecture de sa table).
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    try:
        f = charger(os.path.join(racine, FABRICANT), "FABRICANT_POUR_LIVRER")
        return {"relais": os.path.basename(f.CIRCUIT_RELAIS), "epreuves": os.path.basename(f.CIRCUIT_EPREUVES),
                "groupe_long": tuple(f.CIRCUITS_DU_GROUPE_LONG), "motif_version": f.MOTIF_DE_VERSION,
                "nom_de_demande": f.NOM_DE_DEMANDE}
    except Exception as e:
        raise Arret(TOMBE, f"fabricant illisible : {type(e).__name__} : {e}")


def commande_de_republication(racine):
    """Rend la commande qui amène le public à main, lue dans le fabricant de `racine`.

    ① RÔLE — Nommer la commande de republication sans la recopier (R-708).
    ② CONTEXTE D'APPEL — INSTALLER (message du code 4, public en retard), REPUBLIER (ligne « ::error:: » du mode --verifier).
    ③ ENTRÉE — `racine` : la racine d'un dépôt privé (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la commande, ou un texte qui dit qu'elle est illisible.
      [rend: 1]
    ⑥ TRAITEMENT — `charger` le fabricant, lire COMMANDE_DE_REPUBLICATION.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La même commande est nommée par le pas « Poser les programmes publics » du circuit du soir
      (relecture de Cowork du 20-11-2026 à 21h23, D-3) : une seule écriture, dans le fabricant.
    ⑨ CE QUI CLOCHE — Le fabricant s'exécute comme module (lecture de sa table).
    ⑩ EFFET — Exécute le fabricant comme module.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        return charger(os.path.join(racine, FABRICANT), "FABRICANT_POUR_LA_COMMANDE").COMMANDE_DE_REPUBLICATION
    except Exception as e:   # noqa: BLE001 — un message, jamais un plantage
        return f"programmes/REPUBLIER.py (commande illisible dans le fabricant : {type(e).__name__})"


# ── LE REGISTRE DES TRAVAUX ─────────────────────────────────────────────────────────────────────────────────────────
def contrat_des_travaux(racine):
    """Rend la liste des colonnes du registre, lue au contrat, et le module des contrats.

    ① RÔLE — Les colonnes du registre, écrites une fois dans programmes/CONTRATS_DES_FICHIERS.py (TRAVAUX).
    ② CONTEXTE D'APPEL — `noter` et `lire_le_registre`.
    ③ ENTRÉE — `racine` : où lire le module des contrats ; à défaut, à côté de ce programme.
    ④ CONDITIONS D'ENTRÉE — Le module s'importe et déclare TRAVAUX.
    ⑤ SORTIE — DEUX valeurs : la liste des colonnes, le module.
      [rend: 2]
    ⑥ TRAITEMENT — `charger` le module de la racine s'il existe, sinon celui d'à côté.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Ce qui se partage se déclare » : écrivain et lecteur se confrontent au contrat.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le module des contrats.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    chemin = os.path.join(racine, "programmes", "CONTRATS_DES_FICHIERS.py")
    if not os.path.isfile(chemin):
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CONTRATS_DES_FICHIERS.py")
    c = charger(chemin, "CONTRATS_POUR_LE_REGISTRE")
    return list(c.TRAVAUX), c


def noter(racine, etape, branche, executant, identifiant, lance_le, fini_le="", resultat=""):
    """Écrit UNE entrée du registre des travaux : un fichier JSON NEUF dans le dossier du registre (jamais un ajout).

    ① RÔLE — Écrire qui fait quoi, au moment même du geste.
    ② CONTEXTE D'APPEL — Les étapes de LIVRER et d'INSTALLER, et QUI_FAIT_QUOI.py « noter ».
    ③ ENTRÉE — `racine` : le worktree · `etape` (« note », « publication », « demande », « epreuve:<CODE> »,
      « relecture », « installation ») · `branche` · `executant` (github, cowork ou chat) · `identifiant` (numéro de
      passage, pointe) · `lance_le` · `fini_le` · `resultat`.
    ④ CONDITIONS D'ENTRÉE — `executant` est l'un des EXECUTANTS_DES_TRAVAUX du contrat.
    ⑤ SORTIE — UNE valeur : le chemin relatif du fichier écrit ; lève ValueError si le contrat refuse.
      [rend: 1]
    ⑥ TRAITEMENT — Champs confrontés au contrat (sens ECRIT) ; nom « AAAA-MM-JJ_HHhMMmSS_<6 octets au hasard en
      hexadécimal>.json » ; création exclusive (un nom déjà pris est refusé par le système, jamais écrasé).
    ⑦ UNITÉ — Heures de Paris.
    ⑧ POURQUOI — Une entrée au lancement et une à la fin : la plus avancée fait foi. Un fichier par entrée : deux
      poussées concurrentes n'écrivent jamais le même fichier, donc un « pull --rebase » ne peut pas entrer en conflit
      sur le registre (consigne du 20-11-2026 au soir, point C).
    ⑨ CE QUI CLOCHE — Le dossier grandit d'un fichier par entrée ; aucun programme ne l'élague.
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    _colonnes, c = contrat_des_travaux(racine)
    if executant not in c.EXECUTANTS_DES_TRAVAUX:
        raise ValueError(f"exécutant hors contrat : {executant!r}")
    ligne = {"etape": etape, "branche": branche, "executant": executant, "identifiant": str(identifiant),
             "lance_le": lance_le, "fini_le": fini_le, "resultat": resultat}
    ecarts = c.verifier("TRAVAUX", list(ligne), "ECRIT")
    if ecarts:
        raise ValueError("registre hors contrat : " + " ; ".join(ecarts))
    dossier = os.path.join(racine, REGISTRE)
    os.makedirs(dossier, exist_ok=True)
    nom = datetime.now(PARIS).strftime("%Y-%m-%d_%Hh%Mm%S") + "_" + os.urandom(6).hex() + ".json"
    with open(os.path.join(dossier, nom), "x", encoding="utf-8") as f:
        json.dump(ligne, f, ensure_ascii=False)
        f.write("\n")
    return REGISTRE + nom


def entrees_du_registre(racine, ref=None):
    """Rend les entrées du registre, lues sur le disque de `racine` ou à la référence git `ref`.

    ① RÔLE — Le SEUL lecteur du registre (R-708) : QUI_FAIT_QUOI et les épreuves le lisent ici.
    ② CONTEXTE D'APPEL — QUI_FAIT_QUOI.lignes_du_registre ; les épreuves.
    ③ ENTRÉE — `racine` : un dépôt git · `ref` : None pour le disque, sinon une référence.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des (nom du fichier, dict) ; lève ValueError sur une entrée illisible ou hors
      contrat (sens LU : colonnes, et exécutant dans EXECUTANTS_DES_TRAVAUX — relecture de Cowork, D-6).
      [rend: 1]
    ⑥ TRAITEMENT — Disque : les *.json du dossier, triés. Référence : « git ls-tree » du dossier, puis
      « git cat-file --batch » en un appel ; une référence sans dossier rend [].
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Ce qui se partage se déclare » : le lecteur se confronte au contrat, comme l'écrivain.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le disque ou git.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    colonnes, c = contrat_des_travaux(racine)
    textes = []
    if ref is None:
        dossier = os.path.join(racine, REGISTRE)
        if os.path.isdir(dossier):
            for n in sorted(os.listdir(dossier)):
                if n.endswith(".json"):
                    with open(os.path.join(dossier, n), encoding="utf-8") as f:
                        textes.append((n, f.read()))
    else:
        noms = [n for n in git(racine, "ls-tree", "--name-only", ref, "--", REGISTRE).stdout.splitlines()
                if n.endswith(".json")]
        if noms:
            r = subprocess.run(["git", "-C", racine, "cat-file", "--batch"], capture_output=True, timeout=600,
                               input="".join(f"{ref}:{n}\n" for n in noms).encode("utf-8"))
            flux, i = r.stdout, 0
            for n in noms:
                fin = flux.index(b"\n", i)
                tete = flux[i:fin].split()
                if len(tete) != 3:
                    raise ValueError(f"entrée illisible : {n}")
                taille = int(tete[2])
                textes.append((os.path.basename(n), flux[fin + 1:fin + 1 + taille].decode("utf-8")))
                i = fin + 1 + taille + 1
    rendu = []
    for n, texte in textes:
        try:
            d = json.loads(texte)
        except ValueError:
            raise ValueError(f"entrée illisible : {n}")
        ecarts = c.verifier("TRAVAUX", list(d) if isinstance(d, dict) else [], "LU")
        if ecarts or not isinstance(d, dict) or list(d) != colonnes:
            raise ValueError(f"entrée hors contrat : {n} : " + " ; ".join(ecarts or ["colonnes"]))
        if d["executant"] not in c.EXECUTANTS_DES_TRAVAUX:
            raise ValueError(f"entrée hors contrat : {n} : exécutant {d['executant']!r}")
        rendu.append((n, d))
    return rendu


# ── LES WORKTREES ───────────────────────────────────────────────────────────────────────────────────────────────────
def worktree_de(racine, branche):
    """Rend le worktree où une branche locale est déjà extraite, ou None.

    ① RÔLE — Savoir si la branche nommée est déjà sur un disque (git refuse de l'extraire deux fois).
    ② CONTEXTE D'APPEL — `worktree_nomme`.
    ③ ENTRÉE — `racine` : le clone privé · `branche` : le nom court.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — « git worktree list --porcelain », ligne « branch refs/heads/<branche> ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le worktree du Chat porte souvent la branche ; en créer un autre échouerait.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin = None
    for l in git(racine, "worktree", "list", "--porcelain").stdout.splitlines():
        if l.startswith("worktree "):
            chemin = l[len("worktree "):]
        elif l == "branch refs/heads/" + branche:
            return chemin
    return None


def worktree_nomme(racine, branche):
    """Rend un worktree où la branche est extraite SOUS SON NOM, à la pointe d'origin ; et s'il est jetable.

    ① RÔLE — Donner au fabricant un dépôt privé sur une branche NOMMÉE (sinon `refus_de_branche` refuse).
    ② CONTEXTE D'APPEL — `main` de LIVRER (la branche travail-…) et d'INSTALLER (main).
    ③ ENTRÉE — `racine` : le clone privé · `branche` : le nom court.
    ④ CONDITIONS D'ENTRÉE — « git fetch origin » fait juste avant.
    ⑤ SORTIE — DEUX valeurs : le chemin du worktree, vrai s'il a été créé ici (à retirer à la fin).
      [rend: 2]
    ⑥ TRAITEMENT — Refus (Arret 3) si la branche locale porte un commit absent d'origin. Branche déjà extraite dans
      un worktree : il doit être propre et à la pointe d'origin (sinon refus), et il est pris tel quel. Sinon :
      « git worktree add -B <branche> <dossier neuf> origin/<branche> ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026 : jamais de worktree détaché pour publier ; « -B » ne doit pas effacer un
      commit local non poussé.
    ⑨ CE QUI CLOCHE — Le worktree pris tel quel est celui du Chat : le programme y commite la note et le registre.
    ⑩ EFFET — Peut créer un worktree et déplacer la branche locale sur la pointe d'origin.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    distante = git(racine, "rev-parse", "--verify", "-q", f"refs/remotes/origin/{branche}").stdout.strip()
    if not distante:
        raise Arret(TOMBE, f"origin/{branche} introuvable")
    locale = git(racine, "rev-parse", "--verify", "-q", f"refs/heads/{branche}").stdout.strip()
    if locale:
        en_avance = git(racine, "rev-list", f"refs/remotes/origin/{branche}..refs/heads/{branche}").stdout.split()
        if en_avance:
            raise Arret(TOMBE, f"la branche locale {branche} porte {len(en_avance)} commit(s) absent(s) d'origin "
                               f"({en_avance[0][:12]}…) : la pousser d'abord, rien n'est effacé")
    deja = worktree_de(racine, branche)
    if deja:
        sale = git(deja, "status", "--porcelain").stdout.strip()
        tete = git(deja, "rev-parse", "HEAD").stdout.strip()
        if sale or tete != distante:
            raise Arret(TOMBE, f"{branche} est extraite dans {deja}, qui n'est pas propre ou pas à la pointe d'origin")
        return deja, False
    dossier = tempfile.mkdtemp(prefix="livrer_wt_", dir="/tmp")
    os.rmdir(dossier)
    r = git(racine, "worktree", "add", "-q", "-B", branche, dossier, f"origin/{branche}")
    if r.returncode != 0:
        raise Arret(TOMBE, f"worktree de {branche} refusé : {r.stderr.strip()[:200]}")
    return dossier, True


def worktree_jetable(racine, reference):
    """Crée un worktree détaché à une référence ; rend son chemin.

    ① RÔLE — Lire une version sans rien écrire sur une branche (vérification de la note, rapatriement).
    ② CONTEXTE D'APPEL — `verifier_la_note`, `lire_les_resultats`.
    ③ ENTRÉE — `racine` : le clone privé · `reference` : ce qu'on extrait.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin.
      [rend: 1]
    ⑥ TRAITEMENT — « git worktree add --detach ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ce qui ne publie pas peut être détaché.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée un worktree.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    dossier = tempfile.mkdtemp(prefix="livrer_lu_", dir="/tmp")
    os.rmdir(dossier)
    r = git(racine, "worktree", "add", "-q", "--detach", dossier, reference)
    if r.returncode != 0:
        raise Arret(TOMBE, f"worktree de lecture refusé : {r.stderr.strip()[:200]}")
    return dossier


def retirer_worktree(racine, dossier):
    """Retire un worktree créé par ce programme.

    ① RÔLE — Ne rien laisser derrière soi.
    ② CONTEXTE D'APPEL — Les blocs finally.
    ③ ENTRÉE — `racine` : le clone privé · `dossier` : le chemin absolu du worktree.
    ④ CONDITIONS D'ENTRÉE — `dossier` a été créé par ce programme sous /tmp.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — « git worktree remove --force <dossier> », puis « git worktree prune ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un worktree oublié garde une branche extraite et bloque le suivant.
    ⑨ CE QUI CLOCHE — Un dossier hors de /tmp n'est jamais retiré.
    ⑩ EFFET — Efface le worktree.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if dossier and os.path.isabs(dossier) and dossier.startswith("/tmp/livrer_"):
        git(racine, "worktree", "remove", "--force", dossier)
        git(racine, "worktree", "prune")


# ── ÉTAPE ① : LA NOTE ───────────────────────────────────────────────────────────────────────────────────────────────
def verifier_la_note(racine, branche):
    """Étape ① : la note de la branche est-elle acceptée par le garde-fou, en mode relecture ? Lève Arret(3) sinon.

    ① RÔLE — Ne rien publier ni lancer pour une note qui n'a pas été contrôlée ou qui a bougé depuis.
    ② CONTEXTE D'APPEL — `main`, en premier.
    ③ ENTRÉE — `racine` : le clone privé · `branche` : la branche.
    ④ CONDITIONS D'ENTRÉE — origin/<branche> lu.
    ⑤ SORTIE — UNE valeur : la dernière ligne du garde-fou.
      [rend: 1]
    ⑥ TRAITEMENT — worktree détaché jetable à origin/<branche> ; « CONTROLER_MA_LIVRAISON.py
      echanges/A_RELIRE.md --verifier » depuis ce worktree ; retrait.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026, étape ① ; la relecture n'écrit rien (Q5 de Cowork).
    ⑨ CE QUI CLOCHE — Le garde-fou relance les commandes citées par la note (bornées à 120 s chacune).
    ⑩ EFFET — Crée et retire un worktree ; lance le garde-fou.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    wt = worktree_jetable(racine, f"origin/{branche}")
    try:
        if not os.path.isfile(os.path.join(wt, NOTE)):
            raise Arret(TOMBE, f"{NOTE} absent de origin/{branche}")
        garde = os.environ.get("LIVRER_GARDE_FOU", os.path.join(wt, GARDE_FOU))
        r = lancer([sys.executable, "-B", garde, NOTE, "--verifier"], dossier=wt, borne=3600)
        fin = (r.stdout.strip().splitlines() or [""])[-1]
        if r.returncode != 0:
            raise Arret(TOMBE, f"note refusée par le garde-fou (code {r.returncode}) : {fin[:200]}")
        return fin
    finally:
        retirer_worktree(racine, wt)


# ── ÉTAPE ② : LA PUBLICATION ────────────────────────────────────────────────────────────────────────────────────────
def cloner_le_public(branche):
    """Clone le dépôt public NEUF sous /tmp, sur la branche du même nom ; rend le chemin.

    ① RÔLE — Un clone public neuf à chaque publication, jamais /home/claude/pub.
    ② CONTEXTE D'APPEL — `publier_au_public`, deux fois (publier, puis vérifier).
    ③ ENTRÉE — `branche` : la branche publique voulue.
    ④ CONDITIONS D'ENTRÉE — LIVRER_DEPOT_PUBLIC ou DEPOT_PUBLIC joignable.
    ⑤ SORTIE — UNE valeur : le chemin du clone, sur une branche NOMMÉE `branche`.
      [rend: 1]
    ⑥ TRAITEMENT — « git ls-remote » : branche publique existante → « git clone --branch » ; absente → clone de la
      branche par défaut, puis « git checkout -b <branche> » (la publication la crée).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026 : « Clone public NEUF dans /tmp, jamais /home/claude/pub ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Clone le public ; crée un dossier sous /tmp.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    url = os.environ.get("LIVRER_DEPOT_PUBLIC", DEPOT_PUBLIC)
    dossier = tempfile.mkdtemp(prefix="livrer_pub_", dir="/tmp")
    if os.path.realpath(dossier).startswith(INTERDIT_POUR_LE_CLONE_PUBLIC):
        raise Arret(TOMBE, "clone public refusé sous /home/claude/pub")
    existe = lancer(["git", "ls-remote", "--heads", url, f"refs/heads/{branche}"], borne=300)
    if existe.returncode != 0:
        shutil.rmtree(dossier, ignore_errors=True)
        raise Arret(TOMBE, "dépôt public illisible : " + existe.stderr.strip()[:200])
    if existe.stdout.strip():
        r = lancer(["git", "clone", "-q", "--branch", branche, url, dossier], borne=900)
    else:
        r = lancer(["git", "clone", "-q", url, dossier], borne=900)
        if r.returncode == 0:
            r = git(dossier, "checkout", "-q", "-b", branche)
    if r.returncode != 0:
        shutil.rmtree(dossier, ignore_errors=True)
        raise Arret(TOMBE, "clone public refusé : " + r.stderr.strip()[:200])
    return dossier


def pointe_publique(branche):
    """Rend la pointe de la branche publique, ou « » si elle n'existe pas.

    ① RÔLE — Voir si la publication a bougé la branche publique.
    ② CONTEXTE D'APPEL — `publier_au_public`.
    ③ ENTRÉE — `branche`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le commit, ou « ».
      [rend: 1]
    ⑥ TRAITEMENT — « git ls-remote ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — INSTALLER exige de voir la pointe publique bouger (consigne ④).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le dépôt public.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = lancer(["git", "ls-remote", "--heads", os.environ.get("LIVRER_DEPOT_PUBLIC", DEPOT_PUBLIC),
                f"refs/heads/{branche}"], borne=300)
    return (r.stdout.split() or [""])[0]


def fabriquer(prive, public, publier):
    """Lance le fabricant du circuit public ; rend le résultat.

    ① RÔLE — Un seul appel du fabricant, à blanc ou avec --publier.
    ② CONTEXTE D'APPEL — `publier_au_public`, trois fois.
    ③ ENTRÉE — `prive` : le worktree nommé · `public` : le clone public · `publier` : vrai pour --publier.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le résultat de `lancer`.
      [rend: 1]
    ⑥ TRAITEMENT — « python3 -B <fabricant> <prive> <public> [--publier] », TMPDIR propre sous /tmp.
    ⑦ UNITÉ — Secondes (borne 3 600).
    ⑧ POURQUOI — MODE_EMPLOI_DEPOT.md §13.2 : le fabricant est la seule poussée vers le public.
    ⑨ CE QUI CLOCHE — LIVRER_FABRICANT le remplace dans les épreuves.
    ⑩ EFFET — Celui du fabricant.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return lancer([sys.executable, "-B", fabricant_de(prive), prive, public] + (["--publier"] if publier else []),
                  dossier=prive, borne=3600)


def fabricant_de(prive):
    """Rend le chemin du fabricant d'un dépôt privé : LIVRER_FABRICANT, sinon celui que porte ce dépôt.

    ① RÔLE — Le seul choix du fabricant pour publier depuis main ET pour vérifier ce qui a été publié.
    ② CONTEXTE D'APPEL — `fabriquer` ; REPUBLIER (`publier_si_different`, et `verifier` avec --fabricant-du-prive,
      que lance INSTALLER à l'étape ⑤).
    ③ ENTRÉE — `prive` : un dépôt privé (worktree de main).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un chemin (il peut ne pas exister ; le lancement le dira, code non nul).
      [rend: 1]
    ⑥ TRAITEMENT — os.environ, sinon <prive>/FABRICANT.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-21 du RELU de Cowork sur 4e4dc386f : INSTALLER publiait avec le fabricant de main et vérifiait avec
      celui du clone du Chat ; deux fabricants pour une même comparaison (R-708).
    ⑨ CE QUI CLOCHE — LIVRER_FABRICANT le remplace dans les épreuves.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return os.environ.get("LIVRER_FABRICANT", os.path.join(prive, FABRICANT))


def est_cowork(auteur):
    """Rend vrai si un nom d'auteur git est EXACTEMENT « cowork » (casse et blancs aux bords ignorés).

    ① RÔLE — La seule écriture de la règle « ce commit est-il de Cowork ? ».
    ② CONTEXTE D'APPEL — INSTALLER (`juger_le_relu`, auteur du dernier commit du RELU) ; QUI_FAIT_QUOI (commits de
      Cowork depuis le lancement d'une relecture).
    ③ ENTRÉE — `auteur` : un nom d'auteur git (%an), éventuellement vide.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — strip, lower, égalité avec « cowork ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-26 du RELU de Cowork sur 13988dfbd : la règle était écrite deux fois (INSTALLER et QUI_FAIT_QUOI) ;
      deux implémentations d'une même chose divergent toujours (R-708). D-5 : « --author=cowork » de git est un
      motif, « Claude (pas cowork) » y répond ; seul le nom entier compte.
    ⑨ CE QUI CLOCHE — L'auteur git se déclare : n'importe qui peut écrire « cowork » ; filet contre l'oubli, pas preuve.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return auteur.strip().lower() == "cowork"


# LA DATE FIGÉE DES FICHIERS AVANT UNE FABRICATION À BLANC (N-4 du RELU de Cowork sur 0f18a8d2a, 21-11-2026) : une
# date que nul fichier écrit aujourd'hui ne porte (09-09-2001), en secondes depuis 1970.
DATE_FIGEE = 1_000_000_000


def ecart_apres_fabrication(clone, lancer_le_fabricant):
    """Fige les dates du clone, lance le fabricant, rend (résultat, écart, nombre de fichiers réécrits).

    ① RÔLE — La propriété unique « une fabrication à blanc ne change rien », sans ses deux angles morts : un
      fabricant MUET (il sort en 0 sans rien écrire, et rien ne change) et un fichier écrit mais IGNORÉ par le
      .gitignore du clone (git ne le montre pas).
    ② CONTEXTE D'APPEL — `_publier_dans` (clone de contrôle) et REPUBLIER.ecart_avec_le_public (copie du public).
    ③ ENTRÉE — `clone` : un dépôt git · `lancer_le_fabricant` : une fonction sans argument qui lance le fabricant
      sur ce clone et rend son CompletedProcess.
    ④ CONDITIONS D'ENTRÉE — Le clone peut être écrit (ses dates sont changées).
    ⑤ SORTIE — TROIS valeurs : le CompletedProcess du fabricant ; l'écart, texte de « git status --porcelain
      --untracked-files=all » suivi d'une ligne « !! <chemin> » par fichier ignoré que la fabrication a écrit (vide =
      égal) ; le nombre de fichiers que la fabrication a écrits : suivis réécrits ou supprimés, nouveaux, ignorés.
      [rend: 3]
    ⑥ TRAITEMENT — Chaque fichier suivi (« git ls-files ») et chaque fichier ignoré déjà présent (« git status
      --ignored=matching ») reçoit la date DATE_FIGEE (lien symbolique : sa propre date) ; le fabricant tourne ; un
      fichier suivi absent ou de date différente est réécrit ; un fichier ignoré de date différente est écrit par
      la fabrication et compte dans l'écart.
    ⑦ UNITÉ — Secondes depuis 1970 pour les dates ; un NOMBRE DE FICHIERS.
    ⑧ POURQUOI — RELU de Cowork sur 0f18a8d2a, N-4 : avec le seul « git status », un fabricant qui sort en 0 sans
      rien écrire, ou qui écrit un fichier listé au .gitignore du public, rendait « égal ». Mesuré le 21-11-2026
      sur le vrai fabricant et un clone public : après les dates figées, 250 des 285 fichiers suivis sont réécrits
      (les 250 qu'il publie), et l'écart est vide.
    ⑨ CE QUI CLOCHE — Un fabricant qui réécrit un fichier en lui remettant la date DATE_FIGEE passerait pour muet sur
      ce fichier. Un fabricant qui n'écrit qu'une partie de ce qu'il publie n'est pas vu, s'il écrit au moins un
      fichier suivi.
    ⑩ EFFET — Change les dates des fichiers du clone ; lance le fabricant.
    ⑪ TERMINAISON — Rend la main ; la durée est celle du fabricant, que l'appelant borne.
      [sort: non]
    """
    def chemins_ignores():
        """Rend les fichiers ignorés présents dans le clone (les dossiers ignorés sont parcourus).

        ① RÔLE — Voir ce que « git status » ordinaire cache.
        ② CONTEXTE D'APPEL — `ecart_apres_fabrication`, avant et après le fabricant.
        ③ ENTRÉE — — (le clone de la fonction englobante).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la liste des chemins relatifs.
          [rend: 1]
        ⑥ TRAITEMENT — « git status --porcelain --ignored=matching --untracked-files=all », lignes « !! ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-4 du RELU de Cowork sur 0f18a8d2a : un fichier écrit mais ignoré était invisible.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lance git en lecture.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        rel = []
        for ligne in git(clone, "status", "--porcelain", "--ignored=matching", "--untracked-files=all").stdout.splitlines():
            if not ligne.startswith("!! "):
                continue
            chemin = os.path.join(clone, ligne[3:].rstrip("/"))
            if os.path.isdir(chemin) and not os.path.islink(chemin):
                for d, _sous, fichiers in os.walk(chemin):
                    rel += [os.path.relpath(os.path.join(d, f), clone) for f in fichiers]
            else:
                rel.append(ligne[3:])
        return rel

    suivis = [x for x in git(clone, "ls-files", "-z").stdout.split("\0") if x]
    for rel in suivis + chemins_ignores():
        chemin = os.path.join(clone, rel)
        if os.path.lexists(chemin):
            os.utime(chemin, (DATE_FIGEE, DATE_FIGEE), follow_symlinks=False)
    resultat = lancer_le_fabricant()
    reecrits = sum(1 for rel in suivis if not os.path.lexists(os.path.join(clone, rel))
                   or os.lstat(os.path.join(clone, rel)).st_mtime != DATE_FIGEE)
    ecrits_ignores = [rel for rel in chemins_ignores()
                      if os.lstat(os.path.join(clone, rel)).st_mtime != DATE_FIGEE]
    reste = git(clone, "status", "--porcelain", "--untracked-files=all").stdout.strip()
    nouveaux = [x for x in reste.splitlines() if x.startswith("?? ")]
    reste = "\n".join([x for x in [reste] if x] + ["!! " + x for x in ecrits_ignores])
    return resultat, reste, reecrits + len(nouveaux) + len(ecrits_ignores)


def publier_au_public(prive, branche):
    """Étape ② (et ④ d'INSTALLER) : publie le code de `prive` sur la branche publique du même nom ; rend le clone.

    ① RÔLE — La publication complète : clone neuf, essai à blanc, --publier, puis preuve par un SECOND clone neuf
      qu'une fabrication à blanc n'y change plus rien.
    ② CONTEXTE D'APPEL — `main` de LIVRER, `main` d'INSTALLER.
    ③ ENTRÉE — `prive` : le worktree nommé · `branche` : sa branche.
    ④ CONDITIONS D'ENTRÉE — `prive` est sur la branche nommée `branche`.
    ⑤ SORTIE — DEUX valeurs : le chemin du clone public de publication (gardé pour la demande), et un dict (avant,
      apres : pointes publiques ; message du fabricant).
      [rend: 2]
    ⑥ TRAITEMENT — `cloner_le_public` ; puis `_publier_dans` : `fabriquer` à blanc (code 0 exigé) ; `fabriquer`
      --publier (code 0 exigé) ; second clone neuf, `fabriquer` à blanc par `ecart_apres_fabrication` : au moins un
      fichier réécrit et un écart vide exigés (N-4 : ni fabricant muet, ni fichier ignoré écrit) ; ce
      second clone est effacé. Si quoi que ce soit lève, le clone de publication est effacé avant de relever.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — 20-11-2026 : une installation non republiée a fait tomber le circuit du soir. La preuve porte sur
      une PROPRIÉTÉ (le public porte exactement ce que fabrique la version), pas sur un message.
    ⑨ CE QUI CLOCHE — Une publication qui ne change rien ne bouge pas la pointe ; la preuve du second clone le dit.
    ⑩ EFFET — Pousse au public (par le fabricant) ; crée des dossiers sous /tmp ; ne laisse que le clone rendu.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    if git(prive, "symbolic-ref", "-q", "--short", "HEAD").stdout.strip() != branche:
        raise Arret(TOMBE, f"le dépôt privé {prive} n'est pas sur la branche nommée {branche}")
    avant = pointe_publique(branche)
    public = cloner_le_public(branche)
    try:
        return public, _publier_dans(prive, branche, public, avant)
    except BaseException:
        shutil.rmtree(public, ignore_errors=True)
        raise


def _publier_dans(prive, branche, public, avant):
    """Le corps de `publier_au_public`, une fois le clone public fait ; rend le dict (avant, apres, message).

    ① RÔLE — Séparer le travail du nettoyage : `publier_au_public` efface le clone si ceci lève.
    ② CONTEXTE D'APPEL — `publier_au_public`, une fois.
    ③ ENTRÉE — `prive` : le worktree nommé · `branche` · `public` : le clone public neuf · `avant` : la pointe
      publique d'avant.
    ④ CONDITIONS D'ENTRÉE — Celles de `publier_au_public`.
    ⑤ SORTIE — UNE valeur : le dict.
      [rend: 1]
    ⑥ TRAITEMENT — Voir `publier_au_public`, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Mesuré le 20-11-2026 : 18 clones publics laissés sous /tmp par les cas qui refusent (publication
      refusée, branche détachée) ; l'épreuve R0 les compte désormais.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir `publier_au_public`, ⑩.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    blanc = fabriquer(prive, public, False)
    if blanc.returncode != 0:
        raise Arret(TOMBE, f"essai à blanc du fabricant refusé (code {blanc.returncode}) : "
                           + (blanc.stdout + blanc.stderr).strip()[-300:])
    pub = fabriquer(prive, public, True)
    if pub.returncode != 0:
        raise Arret(TOMBE, f"publication refusée (code {pub.returncode}) : " + (pub.stdout + pub.stderr).strip()[-300:])
    apres = pointe_publique(branche)
    controle = cloner_le_public(branche)
    try:
        if git(controle, "rev-parse", "HEAD").stdout.strip() != apres:
            raise Arret(TOMBE, "le clone de contrôle n'est pas à la pointe publique annoncée")
        refait, reste, reecrits = ecart_apres_fabrication(controle, lambda: fabriquer(prive, controle, False))
        if refait.returncode == 0 and not reecrits:
            raise Arret(TOMBE, "après publication, le fabricant n'a réécrit aucun fichier du clone de contrôle : "
                               "un fabricant muet ne prouve rien (N-4)")
        if refait.returncode != 0 or reste:
            raise Arret(TOMBE, "après publication, le public ne porte pas exactement le code de la version : "
                               + (reste or refait.stdout.strip()[-200:])[:300])
    finally:
        shutil.rmtree(controle, ignore_errors=True)
    return {"avant": avant, "apres": apres, "message": (pub.stdout.strip().splitlines() or [""])[-1]}


# ── ÉTAPE ③ : LES CODES ─────────────────────────────────────────────────────────────────────────────────────────────
def sans_accents(texte):
    """Rend le texte en majuscules, sans accents.

    ① RÔLE — Reconnaître « À JOUER SUR GITHUB » quelle que soit l'écriture.
    ② CONTEXTE D'APPEL — `codes_a_jouer`.
    ③ ENTRÉE — `texte`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte normalisé.
      [rend: 1]
    ⑥ TRAITEMENT — NFD, retrait des marques, majuscules.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les notes écrivent « À JOUER SUR GITHUB » ou « à jouer sur GitHub ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return "".join(c for c in unicodedata.normalize("NFD", texte) if not unicodedata.combining(c)).upper()


def codes_a_jouer(note, table):
    """Étape ③ : relève les épreuves de la section « à jouer sur GitHub » et les confronte à la table.

    ① RÔLE — Dire QUOI demander à GitHub, sans que le Chat le recopie de mémoire.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `note` : le texte de echanges/A_RELIRE.md · `table` : le dict epreuves_longues de
      tests/LANCEMENT_DES_EPREUVES.json (code → chemin, arguments).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la liste des codes (ordre de la note, sans doublon) ; la liste des noms sans code ;
      un état, « absente », « vide » (section sans élément), « aucune » ou « liste ».
      [rend: 3]
    ⑥ TRAITEMENT — Section = titre « # … » contenant A JOUER SUR GITHUB, jusqu'au titre suivant de même niveau ou
      plus haut. Chaque élément de liste (« - », « * », « 1. ») : son premier `texte entre accents graves`, sinon son
      premier mot. « aucune » en tête d'élément → état « aucune », SAUF s'il nomme quelque chose entre accents graves
      (« aucune autre que `X` ») : l'élément entier va aux noms sans code (N-3). Un nom est un code de la table, ou le chemin d'UNE
      seule entrée ; sinon il est sans code (un chemin porté par deux entrées est ambigu, donc sans code).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026, étape ③ : « Un nom sans code fait sortir en code 2 ».
    ⑨ CE QUI CLOCHE — Un élément sur deux lignes n'est lu que par sa première.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = note.splitlines()
    debut, niveau = None, 0
    for i, l in enumerate(lignes):
        m = re.match(r"^(#+)\s+(.*)$", l)
        if m and TITRE_DES_EPREUVES in sans_accents(m.group(2)):
            debut, niveau = i + 1, len(m.group(1))
            break
    if debut is None:
        return [], [], "absente"
    par_chemin = {}
    for code, e in table.items():
        par_chemin.setdefault(e.get("chemin"), []).append(code)
    codes, sans, aucune = [], [], False
    for l in lignes[debut:]:
        m = re.match(r"^(#+)\s", l)
        if m and len(m.group(1)) <= niveau:
            break
        e = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$", l)
        if not e:
            continue
        texte = e.group(1).strip()
        if sans_accents(texte).startswith("AUCUNE"):
            nomme = re.search(r"`([^`]+)`", texte)
            if nomme:   # « aucune autre que `X` » nomme X : ce n'est pas « aucune » (N-3), et rien ne se devine
                sans.append(f"« {texte[:60]} » (« aucune » qui nomme {nomme.group(1)})")
                continue
            aucune = True
            continue
        b = re.search(r"`([^`]+)`", texte)
        nom = (b.group(1) if b else (texte.split() or [""])[0]).strip()
        if not nom:
            continue
        code = nom if nom in table else (par_chemin.get(nom, [None, None])[0]
                                         if len(par_chemin.get(nom, [])) == 1 else None)
        if code is None:
            sans.append(nom)
        elif code not in codes:
            codes.append(code)
    return codes, sans, ("liste" if codes or sans else "aucune" if aucune else "vide")


# CE QUI NE CHANGE PAS LE CODE (N-14 du RELU de Cowork sur e7b230083, 21-11-2026). Une PROPRIÉTÉ, pas une énumération
# de ce qui s'exécute : l'ancienne liste de trois dossiers ne voyait ni tests/LANCEMENT_DES_EPREUVES.json, qui fabrique
# les circuits du public, ni les *.py de la racine, de tests/ et de etudes/outils/, que le fabricant publie. Tout
# chemin HORS de ces préfixes compte comme du code. Une seule écriture (R-708 : deux implémentations d'une même chose
# divergent toujours) : `changes_hors_permis` la lit, pour INSTALLER (même code avant et après la relecture) et pour
# `code_change_par` (« aucune » épreuve longue n'est crue que sans code changé).
CHANGEMENTS_SANS_CODE = ("echanges/", "archives/")   # plus le registre des travaux, ajouté après `charger` (REGISTRE)


def changes_hors_permis(racine, avant, apres):
    """Rend les fichiers changés entre deux commits hors de CHANGEMENTS_SANS_CODE.

    ① RÔLE — Dire si deux commits portent le MÊME CODE (seuls les échanges, les archives et le registre diffèrent).
    ② CONTEXTE D'APPEL — `code_change_par` ; INSTALLER (`juger_le_relu`, `meme_code`), sous le même nom.
    ③ ENTRÉE — `racine` : un dépôt · `avant`, `apres` : deux commits.
    ④ CONDITIONS D'ENTRÉE — Les deux commits sont connus du dépôt.
    ⑤ SORTIE — UNE valeur : la liste des chemins hors permis (vide : même code).
      [rend: 1]
    ⑥ TRAITEMENT — « git diff --no-renames --name-only -z avant apres », filtré par les préfixes permis. Sans
      « --no-renames », un programme rangé en archives/ n'apparaît que sous son nouveau chemin, permis (relecture de
      Cowork du 20-11-2026 à 21h23, D-2). Sans « -z », git met entre guillemets un chemin non ASCII
      (« "archives/\\303\\251.md" ») qui ne commence plus par son préfixe (N-15 du RELU de Cowork sur e7b230083).
      Différence illisible → lève Arret(TOMBE) : une liste vide dirait « même code » à tort.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : une seule écriture de la propriété « même code » (N-14).
    ⑨ CE QUI CLOCHE — Tout changement hors des préfixes compte, même une donnée ou un document : un travail qui ne
      touche que le BACKLOG doit nommer une épreuve. Refus du bon côté, voulu.
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    d = git(racine, "diff", "--no-renames", "--name-only", "-z", avant, apres)
    if d.returncode != 0:
        raise Arret(TOMBE, f"différence de {avant[:12]} à {apres[:12]} illisible")
    return [c for c in d.stdout.split("\0")
            if c and not any(c == p or c.startswith(p) for p in CHANGEMENTS_SANS_CODE + (REGISTRE,))]


def code_change_par(racine, pointe):
    """Rend les fichiers changés par `pointe` hors de CHANGEMENTS_SANS_CODE depuis sa base commune avec origin/main.

    ① RÔLE — Dire, sans la note, si un travail change du code : « aucune » épreuve longue n'est crue que sinon.
    ② CONTEXTE D'APPEL — `main` (étape ③) et INSTALLER.prouver_les_epreuves.
    ③ ENTRÉE — `racine` : un dépôt privé où origin/main est connue (fetch fait) · `pointe` : un commit.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des chemins (vide : aucun code changé).
      [rend: 1]
    ⑥ TRAITEMENT — « git merge-base origin/main <pointe> » ; `changes_hors_permis(base, pointe)` (N-14 : la même
      propriété qu'INSTALLER, plus une énumération). Base introuvable → lève Arret(TOMBE).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — RELU de Cowork sur 0f18a8d2a, N-3 : « aucune » dans la note faisait installer sans aucune preuve
      GitHub, alors que la réparation du soir pose que « la note du Chat ne fait JAMAIS foi ».
    ⑨ CE QUI CLOCHE — L'épreuve d'un code changé n'est pas déduite (la note la nomme toujours, et Cowork juge si elle
      suffit).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    base = git(racine, "merge-base", "origin/main", pointe)
    if base.returncode != 0:
        raise Arret(TOMBE, f"base commune de {pointe[:12]} et origin/main introuvable")
    return changes_hors_permis(racine, base.stdout.strip(), pointe)


# ── ÉTAPE ④ : LA DEMANDE ────────────────────────────────────────────────────────────────────────────────────────────
def passages_occupes(circuits):
    """Rend les passages du dépôt public en cours ou en attente parmi des circuits.

    ① RÔLE — Voir la file du groupe long avant de déposer, comme le relais la voit.
    ② CONTEXTE D'APPEL — `deposer_et_suivre_le_relais`.
    ③ ENTRÉE — `circuits` : les noms de fichiers des circuits.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des (circuit, numéro, état).
      [rend: 1]
    ⑥ TRAITEMENT — « gh run list --workflow <f> --json databaseId,status », état différent de completed.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relais refuse tant qu'un passage du groupe long est en cours ou en attente (« deux demandes
      refusées par le relais, faute de file d'attente », 20-11-2026).
    ⑨ CE QUI CLOCHE — 100 derniers passages par circuit seulement.
    ⑩ EFFET — Lit GitHub.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    occupes = []
    for f in circuits:
        for p in gh_json("run", "list", "--repo", repo_public(), "--workflow", f, "--limit", "100",
                         "--json", "databaseId,status") or []:
            if p.get("status") != "completed":
                occupes.append((f, p.get("databaseId"), p.get("status")))
    return occupes


def attendre_la_file(circuits, plafond, pas):
    """Attend qu'aucun passage du groupe long ne soit en cours ni en attente ; lève Arret(3) au plafond.

    ① RÔLE — La file d'attente qui manquait au relais.
    ② CONTEXTE D'APPEL — `deposer_et_suivre_le_relais`, avant chaque dépôt.
    ③ ENTRÉE — `circuits` · `plafond` : secondes au plus · `pas` : secondes entre deux regards.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — `passages_occupes` jusqu'à liste vide, un regard par `pas`.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Voir `passages_occupes`.
    ⑨ CE QUI CLOCHE — Un autre déposant peut prendre la place entre ce regard et le dépôt : le relais refuse alors,
      et `deposer_et_suivre_le_relais` revient ici.
    ⑩ EFFET — Lit GitHub, attend.
    ⑪ TERMINAISON — Rend la main, ou lève Arret au plafond.
      [sort: non]
    """
    fin = time.monotonic() + plafond
    while True:
        occ = passages_occupes(circuits)
        if not occ:
            return
        if time.monotonic() >= fin:
            raise Arret(TOMBE, f"plafond atteint : {len(occ)} passage(s) occupent encore la file ({occ[0][0]} {occ[0][1]})")
        dire(f"  file occupée : {', '.join(f'{c} {n} ({e})' for c, n, e in occ)} — nouveau regard dans {pas} s")
        time.sleep(pas)


def deposer_la_demande(public, branche, codes, pointe, motif_du_nom):
    """Dépose UN fichier demandes/DEMANDE_<horodatage>.txt, seul dans un commit, et le pousse ; rend le commit.

    ① RÔLE — La demande au format du relais (MODE_EMPLOI_DEPOT.md §13.2).
    ② CONTEXTE D'APPEL — `deposer_et_suivre_le_relais`.
    ③ ENTRÉE — `public` : le clone public de la publication, sur `branche` · `branche` · `codes` · `pointe` : le
      commit privé exact (40 caractères) · `motif_du_nom` : NOM_DE_DEMANDE du fabricant.
    ④ CONDITIONS D'ENTRÉE — Le clone est propre et à jour.
    ⑤ SORTIE — UNE valeur : le commit poussé.
      [rend: 1]
    ⑥ TRAITEMENT — « git pull --ff-only » ; nom à la minute de Paris, en attendant la minute suivante si le nom
      existe ; contenu « circuit=epreuve / epreuves=… / pointe=… » en ASCII ; commit seul ; « git push origin
      HEAD:refs/heads/<branche> » sans force ; la pointe distante relue.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relais refuse toute autre poussée (un commit, un fichier ajouté, parent = pointe d'avant).
    ⑨ CE QUI CLOCHE — Le commit prend l'identité git de la machine. LIVRER_SANS_ATTENTE_DE_MINUTE (épreuves
      seulement) prend la minute suivante au lieu de l'attendre : le nom porte alors une minute à venir.
    ⑩ EFFET — Pousse un commit sur la branche publique.
    ⑪ TERMINAISON — Rend la main, ou lève Arret ; attend au plus 61 s une minute libre.
      [sort: non]
    """
    if git(public, "pull", "-q", "--ff-only", "origin", branche).returncode != 0:
        raise Arret(TOMBE, "le clone public n'a pas pu se mettre à jour avant la demande")
    decale = 0
    for _ in range(3):
        nom = "demandes/DEMANDE_" + (datetime.now(PARIS) + timedelta(minutes=decale)).strftime("%Y-%m-%d_%Hh%M") + ".txt"
        if not os.path.lexists(os.path.join(public, nom)):
            break
        if os.environ.get("LIVRER_SANS_ATTENTE_DE_MINUTE"):
            decale += 1
        else:
            time.sleep(61 - datetime.now(PARIS).second)
    if not re.match(motif_du_nom, nom) or os.path.lexists(os.path.join(public, nom)):
        raise Arret(TOMBE, f"nom de demande impossible : {nom}")
    os.makedirs(os.path.join(public, "demandes"), exist_ok=True)
    texte = f"circuit=epreuve\nepreuves={','.join(codes)}\npointe={pointe}\n"
    with open(os.path.join(public, nom), "w", encoding="ascii", newline="\n") as f:
        f.write(texte)
    for etape in (git(public, "add", "--", nom),
                  git(public, "commit", "-q", "-m", f"demande d'épreuves longues pour {branche} ({len(codes)})", "--", nom),
                  git(public, "push", "-q", "origin", f"HEAD:refs/heads/{branche}")):
        if etape.returncode != 0:
            raise Arret(TOMBE, "demande non déposée : " + (etape.stderr or etape.stdout).strip()[:200])
    sha = git(public, "rev-parse", "HEAD").stdout.strip()
    if pointe_publique(branche) != sha:
        raise Arret(TOMBE, "la pointe publique n'est pas le commit de la demande")
    return sha


def attendre(regarder, plafond, pas, quoi):
    """Appelle `regarder` jusqu'à ce qu'il rende autre chose que None ; lève Arret(3) au plafond.

    ① RÔLE — Une seule boucle d'attente bornée.
    ② CONTEXTE D'APPEL — Le suivi du relais et du passage.
    ③ ENTRÉE — `regarder` : une fonction sans argument · `plafond`, `pas` : secondes · `quoi` : ce qu'on attend.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : ce que `regarder` a rendu.
      [rend: 1]
    ⑥ TRAITEMENT — Un regard par `pas` jusqu'au plafond.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Aucune attente sans borne.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `regarder`.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    fin = time.monotonic() + plafond
    while True:
        v = regarder()
        if v is not None:
            return v
        if time.monotonic() >= fin:
            raise Arret(TOMBE, f"plafond atteint en attendant {quoi}")
        time.sleep(pas)


def deposer_et_suivre_le_relais(racine, public, branche, codes, pointe, k, plafond, pas):
    """Étape ④ : dépose la demande, suit le relais, redépose après un refus « passage en cours » ; rend le passage.

    ① RÔLE — Obtenir le numéro du passage des épreuves longues lancé par le relais pour CETTE demande.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le worktree nommé (registre) · `public` : le clone public · `branche` · `codes` ·
      `pointe` · `k` : les constantes du fabricant · `plafond`, `pas` : secondes.
    ④ CONDITIONS D'ENTRÉE — Le code de la branche est publié (étape ②).
    ⑤ SORTIE — UNE valeur : le numéro du passage des épreuves.
      [rend: 1]
    ⑥ TRAITEMENT — Jusqu'au plafond : `attendre_la_file` ; `deposer_la_demande` ; le passage du relais dont le
      commit est celui de la demande, suivi jusqu'à sa fin ; succès → le passage des épreuves de la branche créé
      après lui ; échec dont le journal dit « en cours ou en attente » → on recommence ; autre échec → Arret(3).
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — 20-11-2026 : deux demandes refusées, faute de file d'attente.
    ⑨ CE QUI CLOCHE — Le passage des épreuves est reconnu par sa branche et son heure de création (le relais ne
      rend pas son numéro). Plus d'un passage de la branche créé à partir du relais — vivant ou fini — est une
      AMBIGUÏTÉ et arrête tout (code 3), au lieu d'en choisir un. Un second passage qui apparaîtrait APRÈS le premier
      regard n'est pas vu.
    ⑩ EFFET — Pousse des demandes, lit GitHub, écrit le registre.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    fin = time.monotonic() + plafond
    while True:
        attendre_la_file(k["groupe_long"], max(1, fin - time.monotonic()), pas)
        sha = deposer_la_demande(public, branche, codes, pointe, k["nom_de_demande"])
        depose_le = maintenant()
        dire(f"  demande déposée : commit public {sha[:12]}")

        def relais():
            """Rend le passage du relais de cette demande s'il est fini, sinon None.

            ① RÔLE — Un regard sur le relais.
            ② CONTEXTE D'APPEL — `attendre`.
            ③ ENTRÉE — —
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : le dict du passage fini, ou None.
              [rend: 1]
            ⑥ TRAITEMENT — « gh run list --workflow <relais> --branch <branche> », commit = la demande.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Le relais est le seul à savoir s'il a lancé.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Lit GitHub.
            ⑪ TERMINAISON — Rend la main, ou lève Arret.
              [sort: non]
            """
            for p in gh_json("run", "list", "--repo", repo_public(), "--workflow", k["relais"], "--branch", branche,
                             "--limit", "20", "--json", "databaseId,headSha,status,conclusion,createdAt") or []:
                if p.get("headSha") == sha and p.get("status") == "completed":
                    return p
            return None

        p = attendre(relais, max(1, fin - time.monotonic()), pas, "le relais")
        noter(racine, "demande", branche, "github", p["databaseId"], depose_le, maintenant(),
              p.get("conclusion", ""))
        if p.get("conclusion") == "success":
            def lance():
                """Rend le numéro du passage des épreuves lancé par ce relais, sinon None.

                ① RÔLE — Trouver le passage lancé.
                ② CONTEXTE D'APPEL — `attendre`.
                ③ ENTRÉE — —
                ④ CONDITIONS D'ENTRÉE — —
                ⑤ SORTIE — UNE valeur : le numéro, ou None ; lève Arret(3) si plus d'un passage répond.
                  [rend: 1]
                ⑥ TRAITEMENT — Passages workflow_dispatch du circuit des épreuves sur la branche, créés à partir du
                  relais (createdAt ≥ celui du relais), QUEL QUE SOIT leur état : aucun → None ; un → son numéro ;
                  plus d'un → Arret (sabotages M3 et M4 du relecteur du 20-11-2026 : deux passages vivants, ou un fini
                  et un vivant de la même branche, étaient départagés en silence par le plus ancien).
                ⑦ UNITÉ — —
                ⑧ POURQUOI — Voir ⑨ de la fonction englobante.
                ⑨ CE QUI CLOCHE — Les heures de GitHub sont comparées en texte ISO (même forme).
                ⑩ EFFET — Lit GitHub.
                ⑪ TERMINAISON — Rend la main, ou lève Arret.
                  [sort: non]
                """
                vus = [q for q in gh_json("run", "list", "--repo", repo_public(), "--workflow", k["epreuves"],
                                          "--branch", branche, "--event", "workflow_dispatch", "--limit", "20",
                                          "--json", "databaseId,createdAt,status") or []
                       if q.get("createdAt", "") >= p.get("createdAt", "")]
                if len(vus) > 1:
                    raise Arret(TOMBE, f"{len(vus)} passages des épreuves sur {branche} depuis le relais "
                                       f"{p['databaseId']} : " + ", ".join(f"{q.get('databaseId')} ({q.get('status')})"
                                                                         for q in vus) + " — lequel est le nôtre ?")
                return vus[0]["databaseId"] if vus else None

            return attendre(lance, max(60, fin - time.monotonic()), pas, "le passage lancé par le relais")
        journal = gh("run", "view", str(p["databaseId"]), "--repo", repo_public(), "--log-failed")
        if "en cours ou en attente" in journal.stdout:
            dire("  relais : REFUS, un passage occupe la file — attente, puis nouvelle demande")
            continue
        raise Arret(TOMBE, f"le relais {p['databaseId']} a refusé la demande : "
                           + next((l for l in journal.stdout.splitlines() if "REFUSEE" in l), "raison non lue")[-200:])


# ── ÉTAPE ⑤ : LE PASSAGE ET SES RÉSULTATS ───────────────────────────────────────────────────────────────────────────
def suivre_le_passage(passage, plafond, pas):
    """Attend la fin d'un passage ; rend sa conclusion.

    ① RÔLE — Ne rien conclure avant la fin réelle du passage.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `passage` : le numéro · `plafond`, `pas` : secondes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la conclusion de GitHub.
      [rend: 1]
    ⑥ TRAITEMENT — « gh run view <n> --json status,conclusion » jusqu'à completed.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — 20-11-2026 : Cowork lancé avant GitHub a rejoué lui-même les épreuves.
    ⑨ CE QUI CLOCHE — La couleur du passage n'est pas le verdict : il vient des RESULTAT.json.
    ⑩ EFFET — Lit GitHub.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    def regard():
        """Rend la conclusion si le passage est fini, sinon None.

        ① RÔLE — Un regard.
        ② CONTEXTE D'APPEL — `attendre`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la conclusion, ou None.
          [rend: 1]
        ⑥ TRAITEMENT — `gh_json`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit GitHub.
        ⑪ TERMINAISON — Rend la main, ou lève Arret.
          [sort: non]
        """
        v = gh_json("run", "view", str(passage), "--repo", repo_public(), "--json", "status,conclusion") or {}
        return (v.get("conclusion") or "?") if v.get("status") == "completed" else None
    return attendre(regard, plafond, pas, f"la fin du passage {passage}")


def lire_les_resultats(racine, branche, passage, codes, pointe):
    """Rapatrie les résultats d'un passage par le rapatrieur, dans un worktree jetable ; rend code et lignes.

    ① RÔLE — Lire le code de sortie de chaque épreuve au dépôt privé (origin/epreuves-longues/<passage>/<CODE>).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le clone privé · `branche` · `passage` · `codes` : les codes demandés · `pointe` : le
      commit demandé (40 caractères).
    ④ CONDITIONS D'ENTRÉE — Le passage est fini.
    ⑤ SORTIE — DEUX valeurs : le code (0 toutes vertes, 1 au moins une rouge, 2 rien de sûr) ; la liste des
      (code, code de sortie ou « ABSENTE » ou « AUTRE POINTE », durée en secondes, pointe jouée lue).
      [rend: 2]
    ⑥ TRAITEMENT — worktree détaché à origin/<branche> ; tests/outils/rapatrier_les_epreuves_longues.py <wt>
      <passage> ; lecture de chaque RESULTAT.json rangé ; un code demandé sans résultat est ABSENT (code 2, jamais
      vert : sabotage M1) ; un résultat dont « pointe_jouee » n'est pas `pointe` est d'une AUTRE POINTE (code 2) ;
      retrait du worktree.
    ⑦ UNITÉ — Secondes (durées).
    ⑧ POURQUOI — R-708 : le rapatrieur sait déjà confronter la liste demandée aux branches (R-D2, R-D5).
    ⑨ CE QUI CLOCHE — Les sorties rangées ne sont pas commitées : elles restent sur les branches du passage.
    ⑩ EFFET — Crée et retire un worktree ; le rapatrieur écrit des références refs/epreuves_lues/….
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    wt = worktree_jetable(racine, f"origin/{branche}")
    try:
        rap = os.environ.get("LIVRER_RAPATRIEUR", os.path.join(wt, RAPATRIEUR))
        r = lancer([sys.executable, "-B", rap, wt, str(passage)], dossier=wt, borne=1800)
        dire("  rapatriement : " + ((r.stdout.strip().splitlines() or ["(rien)"])[-1])[:200])
        lignes, code = [], (r.returncode if r.returncode in (0, 1, 2) else 2)
        for c in codes:
            chemin = os.path.join(wt, "tests", "resultats", "epreuves_longues", str(passage), c, "RESULTAT.json")
            try:
                with open(chemin, encoding="utf-8") as f:
                    res = json.load(f)
                sortie, jouee = res["code_de_sortie"], res.get("pointe_jouee", "")
                if jouee != pointe:
                    lignes.append((c, "AUTRE POINTE", res.get("duree_secondes", "?"), jouee or "(aucune)"))
                    code = 2
                    continue
                lignes.append((c, sortie, res.get("duree_secondes", "?"), jouee))
                if sortie != 0 and code == 0:
                    code = 1
            except (OSError, ValueError, KeyError):
                lignes.append((c, "ABSENTE", "?", ""))
                code = 2
        return code, lignes
    finally:
        retirer_worktree(racine, wt)


def ecrire_les_resultats(wt, passage, pointe, lignes):
    """Écrit la section « RÉSULTATS GITHUB » dans la note, avant la demande de relecture, et la refait contrôler.

    ① RÔLE — Mettre les résultats de GitHub sous les yeux de Cowork, dans la note qu'il relit.
    ② CONTEXTE D'APPEL — `main`, étape ⑤.
    ③ ENTRÉE — `wt` : le worktree nommé · `passage` · `pointe` : le commit demandé · `lignes` : (code, sortie,
      durée, pointe jouée LUE dans RESULTAT.json).
    ④ CONDITIONS D'ENTRÉE — La note existe.
    ⑤ SORTIE — Rien ; lève Arret(3) si le garde-fou refuse la note réécrite (elle est alors remise en l'état).
      [rend: rien]
    ⑥ TRAITEMENT — Retire une section « ## RÉSULTATS GITHUB » précédente et la ligne de contrôle ; insère la section
      neuve avant le titre « DEMANDE DE RELECTURE PAR COWORK » (sinon à la fin) ; relance le garde-fou en écriture.
    ⑦ UNITÉ — Secondes (durées).
    ⑧ POURQUOI — Consigne du 20-11-2026, étape ⑤ ; une note modifiée sans nouvelle ligne de contrôle serait refusée
      par la relecture (« EMPREINTE DIFFÉRENTE »).
    ⑨ CE QUI CLOCHE — Le garde-fou relance les commandes citées par la note.
    ⑩ EFFET — Réécrit la note.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    chemin = os.path.join(wt, NOTE)
    with open(chemin, encoding="utf-8") as f:
        avant = f.read()
    texte = re.sub(r"\n<!-- CONTROLE [0-9a-f]{16} · [^>]*-->\s*$", "\n", avant)
    texte = re.sub(r"(?ms)^## RÉSULTATS GITHUB\b.*?(?=^#{1,2} |\Z)", "", texte)
    section = [TITRE_DES_RESULTATS,
               f"Écrit par programmes/LIVRER.py le {maintenant()} (Paris). Passage {passage} du circuit des épreuves "
               f"longues, pointe demandée {pointe}. Codes et pointe jouée lus dans les RESULTAT.json de "
               f"origin/epreuves-longues/{passage}/<CODE>, pas dans la couleur du passage. Ne pas les rejouer. Cette "
               f"section ne fait pas foi pour l'installation : INSTALLER relit les RESULTAT.json eux-mêmes.", ""]
    section += [f"- {c} : code {s} · {d} s · pointe jouée {j or '(aucune)'}" for c, s, d, j in lignes] + [""]
    m = re.search(r"(?m)^#+ .*DEMANDE DE RELECTURE PAR COWORK", texte)
    i = m.start() if m else len(texte.rstrip("\n")) + 1
    neuf = texte[:i].rstrip("\n") + "\n\n" + "\n".join(section) + "\n" + texte[i:].lstrip("\n")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(neuf.rstrip("\n") + "\n")
    garde = os.environ.get("LIVRER_GARDE_FOU", os.path.join(wt, GARDE_FOU))
    r = lancer([sys.executable, "-B", garde, NOTE], dossier=wt, borne=3600)
    if r.returncode != 0:
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(avant)
        raise Arret(TOMBE, "la note réécrite est refusée par le garde-fou : "
                           + ((r.stdout.strip().splitlines() or [""])[-1])[:200])


def pousser(wt, branche, message, chemins):
    """Commite des chemins s'ils ont changé et pousse sur la branche, sans force, en se rebasant sur un tiers ; rend
    vrai si poussé ou rien à pousser.

    ① RÔLE — La seule poussée privée de LIVRER et de QUI_FAIT_QUOI « noter » (INSTALLER pousse main lui-même).
    ② CONTEXTE D'APPEL — `main` (bloc finally) et QUI_FAIT_QUOI « noter ». PAS INSTALLER : il pousse main lui-même,
      une seule fois et sans rebase (`INSTALLER.fusionner`) — N-6 du RELU de Cowork sur 0f18a8d2a.
    ③ ENTRÉE — `wt` : le worktree nommé · `branche` · `message` · `chemins` : relatifs (fichiers ou dossiers).
    ④ CONDITIONS D'ENTRÉE — `wt` est sur `branche`, sans autre changement que `chemins`.
    ⑤ SORTIE — UNE valeur : vrai, ou faux si le commit est refusé ou si ESSAIS_DE_POUSSEE poussées ont échoué.
      [rend: 1]
    ⑥ TRAITEMENT — « git add » des chemins présents ; commit s'il y a une différence indexée ; puis au plus
      ESSAIS_DE_POUSSEE fois : « git push origin HEAD:refs/heads/<branche> » ; refusée → « git pull --rebase origin
      <branche> » (un rebase en conflit est abandonné, « git rebase --abort », et la poussée rend faux) et nouvel
      essai.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Jamais main par erreur : la cible est écrite en clair. Le rebase : consigne du 20-11-2026 au soir,
      point C — un tiers qui pousse pendant un passage ne doit faire perdre ni la note ni le registre (le registre ne
      peut pas entrer en conflit : un fichier neuf par entrée, `noter`).
    ⑨ CE QUI CLOCHE — Un tiers qui modifie la NOTE elle-même produit un vrai conflit : rien n'est poussé, faux.
    ⑩ EFFET — Commit, rebase et poussée privés.
    ⑪ TERMINAISON — Rend la main ; chaque appel git est borné.
      [sort: non]
    """
    presents = [c for c in chemins if os.path.exists(os.path.join(wt, c))]
    if presents:
        git(wt, "add", "--", *presents)
    if git(wt, "diff", "--cached", "--quiet").returncode != 0:
        if git(wt, "commit", "-q", "-m", message).returncode != 0:
            return False
    for essai in range(ESSAIS_DE_POUSSEE):
        git(wt, "fetch", "-q", "origin", branche)
        if git(wt, "rev-list", f"refs/remotes/origin/{branche}..HEAD").stdout.strip() == "":
            return True
        if git(wt, "push", "-q", "origin", f"HEAD:refs/heads/{branche}").returncode == 0:
            return True
        dire(f"  poussée de {branche} refusée (essai {essai + 1}/{ESSAIS_DE_POUSSEE}) : pull --rebase, puis nouvel essai")
        if git(wt, "pull", "-q", "--rebase", "origin", branche).returncode != 0:
            git(wt, "rebase", "--abort")
            return False
    return False


def main():
    """Enchaîne les six étapes ; sort avec le code qui dit au Chat s'il peut lancer Cowork.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv : la branche, « --plafond=<minutes> ».
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — Rien : sort du programme (codes 0 à 3, ou 5, voir l'en-tête).
      [rend: rien]
    ⑥ TRAITEMENT — fetch ; ① note ; worktree nommé ; ② publication ; ③ codes ; ④ demande ; ⑤ suivi, résultats,
      note ; ⑥ verdict ; à la sortie, registre et note commités et poussés, worktrees retirés, clone public effacé.
    ⑦ UNITÉ — Minutes (plafond).
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Sort du programme par sys.exit.
      [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    plafond = 240
    for a in sys.argv[1:]:
        if a.startswith("--plafond="):
            plafond = int(a.split("=", 1)[1])
    if len(args) != 1:
        dire("usage : LIVRER.py <branche travail-…> [--plafond=<minutes>]")
        sys.exit(TOMBE)
    branche, racine = args[0], os.getcwd()
    pas = int(os.environ.get("LIVRER_PAS", "30"))
    wt, jetable, public, code = None, False, None, TOMBE
    try:
        k = constantes_du_fabricant(racine)
        if not re.match(k["motif_version"], branche) or branche == "main":
            raise Arret(TOMBE, f"branche refusée : {branche!r} (une version en attente travail-…)")
        if git(racine, "fetch", "-q", "origin").returncode != 0:
            raise Arret(TOMBE, "fetch du dépôt privé refusé")
        dire(f"ÉTAPE 1 — note de {branche} : " + verifier_la_note(racine, branche))
        wt, jetable = worktree_nomme(racine, branche)
        pointe = git(wt, "rev-parse", "HEAD").stdout.strip()
        noter(wt, "note", branche, "chat", pointe, maintenant(), maintenant(), "acceptée")
        debut = maintenant()
        public, pub = publier_au_public(wt, branche)
        noter(wt, "publication", branche, "chat", pub["apres"], debut, maintenant(),
              f"publiée (pointe publique {pub['avant'][:12] or 'neuve'} -> {pub['apres'][:12]})")
        dire(f"ÉTAPE 2 — publié : {pub['message']} · pointe publique {pub['avant'][:12] or '(neuve)'} → {pub['apres'][:12]}")
        with open(os.path.join(wt, TABLE), encoding="utf-8") as f:
            table = json.load(f).get("epreuves_longues", {})
        with open(os.path.join(wt, NOTE), encoding="utf-8") as f:
            codes, sans, etat = codes_a_jouer(f.read(), table)
        if etat in ("absente", "vide"):
            raise Arret(NOMS, f"section « À JOUER SUR GITHUB » {etat} dans la note (une liste de codes, ou « aucune »)")
        if sans:
            raise Arret(NOMS, "nom(s) sans code dans tests/LANCEMENT_DES_EPREUVES.json : " + ", ".join(sans))
        change = code_change_par(wt, pointe) if not codes else []
        if change:
            raise Arret(NOMS, "la note déclare « aucune » épreuve longue, mais ce travail change du code qui s'exécute : "
                              + ", ".join(change[:5]) + " (N-3)")
        dire(f"ÉTAPE 3 — épreuves longues : {', '.join(codes) or 'aucune'}")
        if not codes:
            dire("ÉTAPES 4 et 5 — sans objet : la note déclare « aucune » épreuve longue")
            code = PRET
        else:
            passage = deposer_et_suivre_le_relais(wt, public, branche, codes, pointe, k, plafond * 60, pas)
            lance_le = maintenant()
            for c in codes:
                noter(wt, f"epreuve:{c}", branche, "github", passage, lance_le, "", "EN COURS")
            dire(f"ÉTAPE 4 — passage {passage} lancé par le relais")
            conclusion = suivre_le_passage(passage, plafond * 60, pas)
            verdict, lignes = lire_les_resultats(racine, branche, passage, codes, pointe)
            for c, s, _, _ in lignes:
                noter(wt, f"epreuve:{c}", branche, "github", passage, lance_le, maintenant(), f"code {s}")
            ecrire_les_resultats(wt, passage, pointe, lignes)
            dire(f"ÉTAPE 5 — passage {passage} fini ({conclusion}) : "
                 + " · ".join(f"{c} {s}" for c, s, _, _ in lignes))
            code = {0: PRET, 1: ROUGE}.get(verdict, TOMBE)
    except Arret as e:
        code = e.args[0]
        dire(f"ARRÊT (code {code}) — {e.args[1]}")
    except Exception as e:   # noqa: BLE001 — un plantage n'est jamais lu comme un verdict ni comme un refus
        code = PLANTAGE
        dire(f"PLANTAGE (code {PLANTAGE}) — {type(e).__name__} : {e}")
        dire(traceback.format_exc().rstrip())
    finally:
        try:
            if wt:
                if not pousser(wt, branche, f"LIVRER : note et registre des travaux de {branche}", [NOTE, REGISTRE]):
                    dire("ARRÊT — la note ou le registre n'ont pas pu être poussés")
                    code = code if code != PRET else TOMBE
                if jetable:
                    retirer_worktree(racine, wt)
            if public:
                shutil.rmtree(public, ignore_errors=True)
        except Exception as e:   # noqa: BLE001 — même règle pendant le rangement
            code = PLANTAGE
            dire(f"PLANTAGE (code {PLANTAGE}) pendant le rangement — {type(e).__name__} : {e}")
    dire({PRET: "ÉTAPE 6 — PRÊT POUR COWORK (code 0) : le Chat lance la relecture",
          ROUGE: "ÉTAPE 6 — ÉPREUVE ROUGE (code 1) : Cowork n'est pas lancé",
          NOMS: "ÉTAPE 6 — LA NOTE NE DIT PAS QUOI JOUER (code 2)",
          TOMBE: "ÉTAPE 6 — ÉTAPE TOMBÉE (code 3)",
          PLANTAGE: "ÉTAPE 6 — PLANTAGE (code 5) : ni verdict ni refus, l'état est à relire"}[code])
    sys.exit(code)


if __name__ == "__main__":
    main()
