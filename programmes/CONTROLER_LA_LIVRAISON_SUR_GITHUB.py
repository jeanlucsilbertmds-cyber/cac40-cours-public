#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Joue le contrôle final d'une livraison (programmes/CONTROLER_MA_LIVRAISON.py) sur une machine de GitHub, et juge
son résultat. Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Décision de Jean-Luc du 25-11-2026 à 15h21 (BACKLOG A-995, réponse « 1 » à « Jouer le contrôle
final sur GitHub (recommandé) ») : le contrôle final des livraisons se joue SUR GITHUB, plus sur la machine du Chat.
Les faits : le contrôle exige tout donnees/ sur le disque (le « témoin du parcours » de l'étage A lit les chemins du
registre de provenance donnees/PROVENANCE_DES_FICHIERS.csv) et un dépôt git qui connaît origin/main ; les agents
travaillent sur des copies partielles, et la plateforme refuse d'y ajouter donnees/. Sur GitHub, le circuit des
épreuves longues (.github/workflows/epreuves_longues.yml, fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py) a
le clone ENTIER du dépôt privé à la pointe demandée, données comprises (traiter des données privées sur GitHub sans
rien publier est permis : A-543, A-600, erratum d'A-812) ; mais il joue chaque épreuve sur une COPIE SANS .git
(comme la nuit). Ce programme rend à cette copie le dépôt git qui lui manque, puis lance le contrôle.

① RÔLE — Deux usages. (a) `<copie>` : jouer le contrôle final sur la note echanges/A_RELIRE.md de la copie, avec
  les options de l'usage local du Chat (« --attendu=livraison », écriture de la ligne de contrôle dans la copie
  jetable), et rendre le verdict, la pointe et l'empreinte. (b) `--juger <RESULTAT.json> <pointe>` : dire si un
  résultat rapatrié est un contrôle VERT de CETTE pointe — c'est le geste du relecteur avant « DÉPLOYABLE ».
② CONTEXTE D'APPEL — (a) Le code « Livraison » de la table « epreuves_longues » de tests/LANCEMENT_DES_EPREUVES.json,
  lancé par tests/outils/jouer_une_epreuve_longue.py au pas « Jouer l epreuve » du circuit des épreuves longues, sous
  « unshare -rn » (réseau coupé). (b) Le relecteur, à la main, sur le RESULTAT.json rapatrié par
  tests/outils/rapatrier_les_epreuves_longues.py. Aussi l'épreuve tests/EPREUVES_DU_CONTROLE_DE_LIVRAISON_SUR_GITHUB_Mer_25-11-2026.py.
③ ENTRÉE — (a) la ligne de commande : la copie jouée ; l'environnement : GITHUB_WORKSPACE (le clone du dépôt privé
  fait par le circuit, avec son .git), POINTE_JOUEE (le commit que « preparer » a cloné et vérifié, 40 caractères
  hexadécimaux), RESULTAT_DE_L_EPREUVE (facultatif : le fichier où écrire le détail, posé par le joueur).
  (b) le chemin d'un RESULTAT.json, et la pointe relue (40 caractères hexadécimaux).
④ CONDITIONS D'ENTRÉE — (a) la copie porte echanges/A_RELIRE.md et programmes/CONTROLER_MA_LIVRAISON.py, et PAS de
  .git ; GITHUB_WORKSPACE est un dépôt git dont HEAD est POINTE_JOUEE et qui connaît refs/remotes/origin/main.
⑤ SORTIE — Le code de sortie. (a) 0 : contrôle VERT (le contrôle a rendu 0 et posé sa ligne de contrôle) ; 1 : le
  contrôle a refusé la livraison (ROUGE) ; 2 : le contrôle n'a pas pu être joué (R-734 : un contrôle qui n'a pas pu
  tourner rend un code non nul). (b) 0 : résultat VERT de cette pointe ; 1 : non (la raison est affichée) ; 2 :
  résultat illisible ou arguments refusés.
  [rend: 1]
⑥ TRAITEMENT — (a) `jouer_le_controle` : vérifier les conditions d'entrée ; `rendre_le_depot_git` (un .git neuf dans
  la copie, qui EMPRUNTE les objets du clone, « alternates », sans les recopier ; les références
  refs/remotes/origin/* du clone ; HEAD détachée sur la pointe ; l'index lu de HEAD) ; empreinte sha256 de la note
  AVANT le contrôle ; lancer le contrôle ; lire la ligne de contrôle qu'il a posée par la fonction du contrôle
  lui-même (`_marqueur_de_queue`) ; écrire le détail. (b) `juger_un_resultat`, qui lit `contenu_vert`.
⑦ UNITÉ — Des empreintes : sha256 entier (64 caractères) de la note, et l'empreinte du contrôle (16 caractères).
⑧ POURQUOI — Décision A-995 ci-dessus. La table des épreuves longues n'admet que des arguments figés sans « / »
  (ARGUMENT_FIGE du fabricant) : le chemin de la note ne peut pas y être écrit, d'où ce programme, qui le connaît.
  Le .git est EMPRUNTÉ et non copié : le dépôt privé pèse plus d'un gigaoctet (1,2 Go mesurés le 25-11-2026 sur la
  machine du Chat) ; le clone du circuit n'est pas modifié. Le résultat porte la pointe et l'empreinte pour qu'un
  vert ne puisse pas servir pour une autre version que celle relue (consigne du 25-11-2026 : « le relecteur ne rend
  pas DÉPLOYABLE sans son résultat vert sur la pointe relue »).
⑨ CE QUI CLOCHE — Que actions/checkout, avec « fetch-depth: 0 » et « ref: <commit> », pose bien
  refs/remotes/origin/main dans le clone n'est PAS VU sur GitHub au 25-11-2026 (THÉORIQUE — à tester : premier essai
  réel, la livraison de la branche travail-controle-github) ; s'il manque, ce programme rend 2 et le dit. Les
  commandes que la note cite et que le contrôle relance tournent réseau coupé, dans la copie : une commande qui
  exige le réseau ou un chemin de la machine de l'auteur y est refusée, comme sur toute autre machine. La copie ne
  porte pas les programmes INTERDITS du circuit (tests/outils/jouer_une_part.py) : une note qui les cite est refusée.
⑩ EFFET — (a) écrit un .git dans la copie, la ligne de contrôle en queue de la note DE LA COPIE (jamais celle de la
  branche : la copie est jetable et rien n'est poussé), et le fichier de détail ; lance git et le contrôle. (b) lit.
⑪ TERMINAISON — Rend la main à `main`, qui sort. Un de mes appels peut-il ne pas revenir ? Le contrôle, sans délai
  ici : le joueur (tests/outils/jouer_une_epreuve_longue.py) l'arrête au temps qui reste au job ; chaque appel à git
  est borné à 600 secondes.
  [sort: oui]
⑫ DÉFINITIONS
  la copie : le dossier que le circuit fabrique depuis le clone du privé, sans .git, et où il joue l'épreuve
  la pointe : le commit exact de la branche relue au dépôt privé (40 caractères hexadécimaux)
  le détail : l'objet JSON que ce programme écrit, que le joueur range dans RESULTAT.json sous
    « detail_de_l_epreuve »
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

NOTE = os.path.join("echanges", "A_RELIRE.md")
CONTROLE = os.path.join("programmes", "CONTROLER_MA_LIVRAISON.py")
CERTIFICATEUR = os.path.join("programmes", "CERTIFIER_LA_VERSION.py")
# Les options de l'usage local du Chat avant tout dépôt (fiche du contrôle, ③) : le rôle attendu, sans « --verifier »
# (la note de la branche ne porte pas encore de ligne de contrôle : l'auteur n'a pas pu jouer le contrôle chez lui).
OPTIONS = ("--attendu=livraison",)
POINTE = r"[0-9a-f]{40}"
VERT, ROUGE, IMPOSSIBLE = "VERT", "ROUGE", "IMPOSSIBLE"
DELAI_GIT = 600


def code_de_sortie_nul(valeur):
    """Dit si un « code_de_sortie » lu dans un RESULTAT.json est un succès : strictement l'entier 0.

    ① RÔLE — L'UNIQUE définition, pour tout le dépôt, d'un code de sortie de succès lu dans un RESULTAT.json du circuit
      des épreuves longues (RELU de Cowork du 25-11-2026, N-44 ; superviseur R-759 : « UNE seule fonction, écrite à un
      endroit, lue par --juger et par INSTALLER », R-708 : deux écritures d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `contenu_vert` (ici) ; programmes/INSTALLER.py, `prouver_les_epreuves`, qui charge ce
      fichier par le chemin LIVRER.JUGE.
    ③ ENTRÉE — `valeur` : ce que le fichier JSON porte sous « code_de_sortie », tel que json.load l'a lu (entier,
      booléen, texte, None, ou autre).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si `valeur` est un entier (et pas un booléen) égal à 0, faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — `type(valeur) is int and valeur == 0`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — En Python, `False == 0` est vrai : le test « != 0 » prenait un « code_de_sortie »: false pour un
      succès (essai J2 de Cowork, 25-11-2026 : « --juger » a répondu « OUI — VERT »). `type(...) is int` refuse le
      booléen, qui est une sous-classe d'int ; 0.0 et "0" sont refusés aussi.
    ⑨ CE QUI CLOCHE — tests/outils/rapatrier_les_epreuves_longues.py porte sa propre règle (« int et pas bool »), et
      programmes/ETAT_DES_TRAVAUX.py compare encore par « != 0 » : deux autres écritures, consignées au BACKLOG.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return type(valeur) is int and valeur == 0


def charger(racine, chemin, nom):
    """Charge un programme de la racine comme un module, par son chemin.

    ① RÔLE — Lire chez la version jouée la fonction qui lit la ligne de contrôle (le contrôle) et l'environnement git
      nettoyé (le certificateur), sans les recopier (R-708 : deux écritures d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `jouer_le_controle`, `environnement_git`.
    ③ ENTRÉE — `racine`, `chemin` relatif, `nom` du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, sans passer par sys.path.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Toujours le voisin de la version jouée, jamais un module de même nom venu d'ailleurs.
    ⑨ CE QUI CLOCHE — Le code de tête du module s'exécute (imports et constantes).
    ⑩ EFFET — Lit et exécute un fichier de la racine.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, os.path.join(racine, chemin))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def environnement_git(copie):
    """Rend l'environnement des appels à git : celui du processus, sans la configuration git de la machine.

    ① RÔLE — Que git ne lise ni la configuration globale ni celle du système (aucun jeton, aucun réglage étranger).
    ② CONTEXTE D'APPEL — `git`.
    ③ ENTRÉE — `copie` : la racine jouée, où vit le certificateur.
    ④ CONDITIONS D'ENTRÉE — programmes/CERTIFIER_LA_VERSION.py existe dans la copie.
    ⑤ SORTIE — UNE valeur : le dictionnaire de l'environnement.
      [rend: 1]
    ⑥ TRAITEMENT — l'environnement du processus, plus SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE du certificateur.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le même nettoyage que la nuit et que le joueur des épreuves longues, lu chez eux (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le code de tête du certificateur.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    c = charger(copie, CERTIFICATEUR, "CERTIFICATEUR_DU_CONTROLE_SUR_GITHUB")
    return dict(os.environ, **c.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)


def git(env, racine, *arguments, entree=None):
    """Lance git en lecture ou en écriture dans une racine, et rend sa sortie ; lève si git échoue.

    ① RÔLE — Le seul endroit où ce programme appelle git.
    ② CONTEXTE D'APPEL — `rendre_le_depot_git`.
    ③ ENTRÉE — `env` : l'environnement (`environnement_git`) ; `racine` ; `arguments` : les arguments de git, sans le
      mot git ; `entree` :
      un texte envoyé à git sur son entrée standard, ou None.
    ④ CONDITIONS D'ENTRÉE — git est installé.
    ⑤ SORTIE — UNE valeur : la sortie standard, sans espaces de fin.
      [rend: 1]
    ⑥ TRAITEMENT — `git -C <racine> <arguments>`, sorties capturées ; code non nul → OSError avec l'erreur.
    ⑦ UNITÉ — DELAI_GIT secondes au plus.
    ⑧ POURQUOI — Un échec de git est un contrôle qui n'a pas pu tourner : il doit se dire (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus git.
    ⑪ TERMINAISON — Rend la main, ou lève ; borné à DELAI_GIT secondes.
      [sort: non]
    """
    r = subprocess.run(["git", "-C", racine, *arguments], env=env, input=entree, capture_output=True, text=True,
                       timeout=DELAI_GIT)
    if r.returncode != 0:
        raise OSError(f"git {' '.join(arguments[:3])} : code {r.returncode} : {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def rendre_le_depot_git(env, source, copie, pointe):
    """Pose dans la copie un dépôt git qui emprunte les objets du clone, ses références origin/*, HEAD sur la pointe.

    ① RÔLE — Donner au contrôle, dans la copie, ce qu'il exige : un .git avec HEAD, refs/remotes/origin/main et
      l'historique entier (l'étage A lit « git log --all »).
    ② CONTEXTE D'APPEL — `jouer_le_controle`, une fois.
    ③ ENTRÉE — `env` ; `source` : le clone du circuit ; `copie` : la copie jouée ; `pointe` : le commit attendu.
    ④ CONDITIONS D'ENTRÉE — la copie n'a pas de .git (vérifié par l'appelant) ; la source est un dépôt git.
    ⑤ SORTIE — UNE valeur : le nombre de références origin/* posées.
      [rend: 1]
    ⑥ TRAITEMENT — ① HEAD de la source = la pointe, sinon refus · ② « git init » de la copie · ③ le fichier
      objects/info/alternates nomme les objets de la source · ④ chaque référence refs/remotes/origin/* de la source
      (sauf origin/HEAD, symbolique) recréée dans la copie · ⑤ HEAD détachée sur la pointe · ⑥ index lu de HEAD
      (« read-tree » : le disque de la copie n'est pas touché) · ⑦ HEAD et origin/main relus dans la copie · ⑧ le
      disque de la copie égale HEAD dans programmes/ et echanges/ (« git diff --quiet HEAD »), sinon refus.
    ⑦ UNITÉ — Un nombre de références.
    ⑧ POURQUOI — Fiche en tête, ⑧ (emprunter, pas recopier) ; ⑦ relit ce qui a été écrit, pour qu'un dépôt mal posé
      soit vu ici et non pris pour un refus du contrôle.
    ⑨ CE QUI CLOCHE — Le dépôt emprunté dépend du clone : si le clone disparaît pendant le contrôle, git échoue (et le
      contrôle refuse, R-734).
    ⑩ EFFET — Écrit copie/.git ; lance git.
    ⑪ TERMINAISON — Rend la main, ou lève OSError (dit par l'appelant).
      [sort: non]
    """
    tete = git(env, source, "rev-parse", "--verify", "HEAD^{commit}")
    if tete != pointe:
        raise OSError(f"le clone n'est pas à la pointe jouée : HEAD {tete[:12]}, POINTE_JOUEE {pointe[:12]}")
    objets = git(env, source, "rev-parse", "--path-format=absolute", "--git-path", "objects")
    refs = [l.split(" ", 1) for l in git(env, source, "for-each-ref", "--format=%(objectname) %(refname)",
                                            "refs/remotes/origin/").splitlines() if l.strip()]
    refs = [(sha, nom) for sha, nom in refs if nom != "refs/remotes/origin/HEAD"]
    git(env, copie, "init", "-q")
    with open(os.path.join(copie, ".git", "objects", "info", "alternates"), "w", encoding="utf-8") as f:
        f.write(objets + "\n")
    git(env, copie, "update-ref", "--stdin", entree="".join(f"create {nom} {sha}\n" for sha, nom in refs))
    git(env, copie, "update-ref", "--no-deref", "HEAD", pointe)
    git(env, copie, "read-tree", "HEAD")
    if git(env, copie, "rev-parse", "--verify", "HEAD^{commit}") != pointe:
        raise OSError("la copie ne porte pas la pointe jouée après la pose du dépôt")
    git(env, copie, "rev-parse", "--verify", "refs/remotes/origin/main^{commit}")
    # Le disque de la copie est-il la pointe ? (superviseur R-759 du 25-11-2026, point 3) : le contrôle juge le DISQUE
    # (la note, les programmes) ; une copie qui différerait de HEAD ferait juger une autre version que la pointe.
    ecart = subprocess.run(["git", "-C", copie, "diff", "--quiet", "HEAD", "--", "programmes/", "echanges/"], env=env,
                           capture_output=True, text=True, timeout=DELAI_GIT)
    if ecart.returncode != 0:
        raise OSError("le disque de la copie diffère de la pointe dans programmes/ ou echanges/ "
                      f"(git diff code {ecart.returncode}) : ce ne serait pas la version demandée qui est jugée")
    return len(refs)


def jouer_le_controle(copie, environ):
    """Joue le contrôle final sur la note de la copie ; rend le code de sortie et le détail.

    ① RÔLE — Usage (a) de la fiche en tête.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `copie` : chemin absolu de la copie ; `environ` : l'environnement (GITHUB_WORKSPACE, POINTE_JOUEE).
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④ ; chacune est vérifiée ici et son absence rend IMPOSSIBLE.
    ⑤ SORTIE — DEUX valeurs : le code (0, 1 ou 2, fiche en tête ⑤) et le détail (dictionnaire : verdict, note,
      sha256_de_la_note, empreinte, pointe, code_du_controle, raison).
      [rend: 2]
    ⑥ TRAITEMENT — Fiche en tête, ⑥ (a). Le contrôle hérite de la sortie standard : son compte rendu entier va dans
      SORTIE.txt du joueur.
    ⑦ UNITÉ — Fiche en tête, ⑦.
    ⑧ POURQUOI — Fiche en tête, ⑧. Le verdict n'est VERT que si le contrôle a rendu 0 ET que sa ligne de contrôle
      se relit : un 0 sans ligne n'est pas une livraison contrôlée.
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨.
    ⑩ EFFET — Fiche en tête, ⑩ (a).
    ⑪ TERMINAISON — Rend la main ; le contrôle n'a pas de délai ici (fiche en tête, ⑪).
      [sort: non]
    """
    pointe = environ.get("POINTE_JOUEE", "")
    detail = {"verdict": IMPOSSIBLE, "note": NOTE.replace(os.sep, "/"), "sha256_de_la_note": "", "empreinte": "",
              "pointe": pointe if re.fullmatch(POINTE, pointe) else "", "code_du_controle": None, "raison": ""}
    source = environ.get("GITHUB_WORKSPACE", "")
    note = os.path.join(copie, NOTE)
    if not re.fullmatch(POINTE, pointe):
        detail["raison"] = "POINTE_JOUEE absente ou mal formée : le circuit la donne (40 caractères hexadécimaux)"
    elif not source or not os.path.isdir(os.path.join(source, ".git")):
        detail["raison"] = "GITHUB_WORKSPACE n'est pas un clone git : ce programme se joue dans le circuit"
    elif os.path.lexists(os.path.join(copie, ".git")):
        detail["raison"] = "la copie porte déjà un .git : ce n'est pas la copie du circuit"
    elif not os.path.isfile(note) or os.path.islink(note):
        detail["raison"] = f"{NOTE} absente de la version jouée (ou lien)"
    elif not os.path.isfile(os.path.join(copie, CONTROLE)):
        detail["raison"] = f"{CONTROLE} absent de la version jouée"
    if detail["raison"]:
        return 2, detail
    try:
        with open(note, "rb") as f:
            detail["sha256_de_la_note"] = hashlib.sha256(f.read()).hexdigest()
        env = environnement_git(copie)
        n = rendre_le_depot_git(env, os.path.realpath(source), copie, pointe)
        print(f"dépôt git rendu à la copie : HEAD {pointe[:12]}, {n} référence(s) origin/*", flush=True)
        lecteur = charger(copie, CONTROLE, "CONTROLE_LU_SUR_GITHUB")._marqueur_de_queue
    except (OSError, subprocess.SubprocessError, AttributeError, SyntaxError) as e:
        detail["raison"] = f"{type(e).__name__} : {e}"
        return 2, detail
    commande = [sys.executable, "-B", os.path.join(copie, CONTROLE), note, *OPTIONS]
    print("contrôle : " + " ".join([CONTROLE, NOTE, *OPTIONS]), flush=True)
    code = subprocess.run(commande, cwd=copie, env=env, stdin=subprocess.DEVNULL).returncode
    detail["code_du_controle"] = code
    with open(note, encoding="utf-8", errors="replace") as f:
        ligne = lecteur(f.read())
    if code == 0 and ligne:
        detail.update(verdict=VERT, empreinte=ligne.group(1))
        return 0, detail
    if code == 0:
        detail["raison"] = "le contrôle a rendu 0 sans poser de ligne de contrôle"
        return 2, detail
    detail.update(verdict=ROUGE, raison=f"le contrôle a refusé la livraison (code {code})")
    return 1, detail


def contenu_vert(r):
    """Dit si le CONTENU d'un RESULTAT.json est un contrôle « Livraison » VERT ; rend le code et la raison.

    ① RÔLE — L'UNIQUE définition, pour tout le dépôt, d'un « Livraison » vert lu dans un RESULTAT.json, quelle que soit
      la pointe (superviseur R-759 du 25-11-2026 à 17h20, forme recommandée, point 1 : « il n'y a ainsi qu'UNE
      définition de Livraison verte, comme pour code_de_sortie_nul » ; R-708 : deux écritures d'une même chose
      divergent toujours). Le lien à la pointe relue n'est PAS jugé ici : `juger_un_resultat` exige l'égalité,
      programmes/INSTALLER.py admet un ancêtre de même code.
    ② CONTEXTE D'APPEL — `juger_un_resultat` (ici) ; programmes/INSTALLER.py, `prouver_les_epreuves`, qui charge ce
      fichier par le chemin LIVRER.JUGE.
    ③ ENTRÉE — `r` : le RESULTAT.json lu par json.load.
    ④ CONDITIONS D'ENTRÉE — `r` est un dictionnaire (chaque appelant refuse avant ce qui n'en est pas un).
    ⑤ SORTIE — DEUX valeurs : le code (0 oui, 1 non) et la raison (texte).
      [rend: 2]
    ⑥ TRAITEMENT — « code_epreuve » vaut « Livraison » ; « code_de_sortie » est l'entier 0 (`code_de_sortie_nul` :
      un booléen false est refusé, N-44) ; « detail_de_l_epreuve.verdict » vaut VERT ; son « empreinte » est faite
      d'exactement 16 caractères hexadécimaux (re.fullmatch : un suffixe est refusé).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — RELU de Cowork du 25-11-2026, N-48 : INSTALLER ne vérifiait ni l'empreinte ni « code_epreuve » ;
      deux jugements du même fichier. Avec cette fonction, INSTALLER et « --juger » lisent la même règle.
    ⑨ CE QUI CLOCHE — Le détail est écrit par le code de la version jouée : une branche qui affaiblit ce programme se
      fait juger par lui (point 13 du superviseur, au BACKLOG). « sha256_de_la_note » n'est pas jugé ici (il ne sert
      qu'au lien d'INSTALLER).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    d = r.get("detail_de_l_epreuve") if isinstance(r.get("detail_de_l_epreuve"), dict) else {}
    if r.get("code_epreuve") != "Livraison":
        return 1, f"ce résultat est celui de l'épreuve {r.get('code_epreuve')!r}, pas de « Livraison »"
    if not code_de_sortie_nul(r.get("code_de_sortie")) or d.get("verdict") != VERT:
        return 1, f"contrôle non vert : code {r.get('code_de_sortie')!r}, verdict {d.get('verdict')!r}, {d.get('raison', '')}"
    if not re.fullmatch(r"[0-9a-f]{16}", str(d.get("empreinte", ""))):
        return 1, "contrôle vert sans empreinte lisible"
    return 0, f"VERT · empreinte {d['empreinte']} · note sha256 {str(d.get('sha256_de_la_note'))[:16]}"


def juger_un_resultat(chemin, pointe):
    """Dit si un RESULTAT.json rapatrié est un contrôle VERT de la pointe relue ; rend le code et la raison.

    ① RÔLE — Usage (b) de la fiche en tête : le geste du relecteur, fait par un programme (R-754 : ce qu'un
      programme peut faire, un programme le fait).
    ② CONTEXTE D'APPEL — `main`, avec « --juger ».
    ③ ENTRÉE — `chemin` : un RESULTAT.json du circuit ; `pointe` : la pointe relue.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code (0 oui, 1 non, 2 illisible) et la raison (texte).
      [rend: 2]
    ⑥ TRAITEMENT — la pointe est bien formée ; le fichier est un objet JSON ; « pointe_jouee » (écrite par le joueur,
      d'après le circuit) vaut la pointe relue (« detail_de_l_epreuve.pointe » n'est pas comparée : elle vient de la
      même variable, la comparer serait une tautologie — superviseur R-759 du 25-11-2026, point 4) ; puis le contenu,
      par `contenu_vert` (la seule définition d'un « Livraison » vert, superviseur R-759 de 17h20, point 1).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un vert d'une autre pointe, ou d'une autre épreuve, ne dit rien de la version relue.
    ⑨ CE QUI CLOCHE — Le code « Livraison » est écrit dans `contenu_vert` ET dans la table : si la table le renomme,
      ce jugement refuse tout (sur-refus visible, jamais un faux vert). Le refus de `contenu_vert` est rendu par un
      `if` dont le corps rend `code` (une variable) : la fabrication des sabotages de l'épreuve ne le voit pas comme une
      garde (fiche de `corps_qui_refuse`, ⑨) ; ses gardes sont sabotées dans `contenu_vert` même.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not re.fullmatch(POINTE, pointe or ""):
        return 2, "pointe relue mal formée (40 caractères hexadécimaux)"
    try:
        with open(chemin, encoding="utf-8") as f:
            r = json.load(f)
    except (OSError, ValueError) as e:
        return 2, f"résultat illisible : {type(e).__name__} : {e}"
    if not isinstance(r, dict):
        return 2, "résultat illisible : pas un objet JSON"
    if r.get("pointe_jouee") != pointe:
        return 1, f"résultat d'une autre pointe : joué sur {str(r.get('pointe_jouee'))[:12]!r}, relu {pointe[:12]}"
    code, raison = contenu_vert(r)
    if code != 0:
        return code, raison
    return 0, f"sur la pointe {pointe[:12]} · {raison}"


def main():
    """La ligne de commande (fiche en tête).

    ① RÔLE — Aiguiller vers l'usage (a) ou (b), afficher le résultat, écrire le détail.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv, os.environ.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — `--juger <RESULTAT.json> <pointe>` → `juger_un_resultat` ; `<copie>` → `jouer_le_controle`, puis
      le détail écrit dans RESULTAT_DE_L_EPREUVE s'il est donné (un détail qui ne s'écrit pas rend 2) ; toute autre
      forme : usage, code 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Fiche en tête, ⑩.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "--juger":
        code, raison = juger_un_resultat(a[1], a[2])
        print(("OUI — " if code == 0 else "NON — ") + raison)
        return code
    if len(a) != 1 or a[0].startswith("--"):
        print("usage : CONTROLER_LA_LIVRAISON_SUR_GITHUB.py <copie> | --juger <RESULTAT.json> <pointe>", file=sys.stderr)
        return 2
    code, detail = jouer_le_controle(os.path.abspath(a[0]), os.environ)
    print(f"VERDICT {detail['verdict']} · pointe {detail['pointe'] or '?'} · empreinte {detail['empreinte'] or '—'}"
          + (f" · {detail['raison']}" if detail["raison"] else ""), flush=True)
    sortie = os.environ.get("RESULTAT_DE_L_EPREUVE", "")
    if sortie:
        try:
            with open(sortie, "w", encoding="utf-8") as f:
                json.dump(detail, f, ensure_ascii=False, indent=1)
        except OSError as e:
            print(f"ARRET détail non écrit : {e}", file=sys.stderr)
            return 2
    return code


if __name__ == "__main__":
    sys.exit(main())
