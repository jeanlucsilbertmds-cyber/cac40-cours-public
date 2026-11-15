#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique, à partir du dépôt privé, ce que le dépôt public doit porter pour faire tourner le circuit du soir.

① RÔLE — Recopier dans un clone du dépôt PUBLIC `cac40-cours-public` : ① TOUS
  les programmes du dépôt privé (`programmes/*.py`), ses outils d'études
  (`etudes/outils/*.py`), ses outils d'épreuves (`tests/outils/*.py`, depuis le
  01-11-2026) et le code de sa racine (`*.py`, `emp.py` le 15-10-2026),
  tels qu'ils y sont ; ② le
  CODE des épreuves (`tests/*.py` et `tests/LANCEMENT_DES_EPREUVES.json`), sans
  leurs fichiers de données, qui restent au privé ; ③ le fichier du circuit du
  soir, `.github/workflows/circuit_du_soir.yml`, FABRIQUÉ à partir de celui du
  dépôt privé (`.github/workflows/collecte_abc.yml`), pour qu'il n'existe qu'une
  seule rédaction des pas ; ④ le fichier du circuit de la certification,
  `.github/workflows/certifier_la_version.yml`, écrit ICI et nulle part ailleurs ;
  ④bis le fichier du circuit des séries longues de sabotages, `.github/workflows/series_longues.yml`, écrit ICI
  et nulle part ailleurs, avec les pas de départ et de dépôt de la certification (patch du 04-11-2026) ; ses
  dépôts vont sur des branches à lui du dépôt privé, jamais sur main ; ④ter avant toute écriture, la
  post-condition `verifier_les_gabarits_publics` (actions permises, permissions en lecture, identités distinctes,
  résultat des parts lu, branches à soi) ; ④quater (08-11-2026) le relais des demandes de série,
  `.github/workflows/demande_de_serie.yml` (RELAIS), écrit ICI, fabriqué comme le circuit des séries depuis la table
  des séries de `tests/LANCEMENT_DES_EPREUVES.json` (`series_du_circuit`) ;
  ⑤ les fiches de circuit du privé (`.github/workflows/*.yml`), sous
  `circuits_du_prive/`, où GitHub ne les met pas en service.
② CONTEXTE D'APPEL — Lancé à la main par le Chat, chaque fois qu'un des
  programmes publiés ou le fichier du circuit change au dépôt privé ; puis le
  Chat pousse le clone public. Jamais par une tâche automatique.
③ ENTRÉE — La ligne de commande : DEUX arguments, la racine du dépôt privé et
  celle du clone du dépôt public.
④ CONDITIONS D'ENTRÉE — Les deux dossiers existent ; le dépôt privé porte au
  moins un programme et `tests/LANCEMENT_DES_EPREUVES.json` ; le fichier du
  circuit privé a la forme attendue (voir ⑥) ; aucun fichier à publier (code ou
  fiche de circuit) n'est un lien symbolique, n'a un chemin réel hors de sa place
  dans le dépôt privé, n'est un lien dur, n'est hors du texte UTF-8 strict, ni ne porte une
  chaîne de la forme d'un jeton (`refus_avant_publication`, défaut M5 du
  04-11-2026 ; le motif vit dans programmes/FORME_D_UN_JETON.py, à côté de ce
  fichier) ; si le clone public porte un « .git », il est sur la MÊME branche que le dépôt privé
  (`refus_de_branche`, décision de Jean-Luc du 05-11-2026 à 13h36 : une branche publique ne porte que le
  code de la version du même nom). Sinon : arrêt, code 1, RIEN n'est écrit.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si tout est écrit, 1 sinon ; à
  l'écran, ce qui a été copié, retiré et fabriqué. [rend: 1]
⑥ TRAITEMENT — ① vérifier que chaque programme à publier existe · ② fabriquer
  le fichier du circuit : en-tête public, horaire, `defaults` qui fait passer
  chaque pas par `ETAPE_MUETTE.py`, les deux clonages (le privé à la racine,
  le public dans `_code/`) et le pas qui vérifie que les programmes publics
  sont ceux du privé puis les pose et efface `_code/` (sinon les programmes qui
  fouillent l'arborescence y trouveraient des fichiers en double), un pas qui
  refabrique le circuit et le compare à celui qui tourne, tous les pas du privé SANS leurs
  commentaires, le jeton du dépôt public remplacé par le secret `JETON_DEPOTS`
  (un commit fait avec le jeton de GitHub ne reconstruit pas la page publique du
  cockpit, relecture du 08-10-2026), et un
  dernier pas qui enregistre le journal au dépôt privé ; DEVANT ce job, un premier job
  `faut_il_tourner` (mêmes clonages, même journal) qui lance programmes/FAUT_IL_TOURNER.py,
  et dont la réponse conditionne le job du circuit ; la case « rattrapage » des pas du
  privé est remplacée par la réponse de ce premier job ; quatre réveils planifiés
  (décision de Jean-Luc du 13-10-2026, voir la fiche de FAUT_IL_TOURNER.py) · ③ refuser un pas privé
  qui rendrait quelque chose lisible au public (voir le code) · ④ écrire : programmes, code
  des épreuves, les deux fichiers de circuit ; retirer du clone public tout programme
  ou tout code d'épreuve qui n'est plus au dépôt privé. LES DEUX CIRCUITS REFUSENT DE
  TOURNER si un seul fichier de code diffère entre les deux dépôts, ou n'existe que d'un
  côté : ce que la machine exécute est donc, octet pour octet, ce que le dépôt public
  montre. · DEPUIS LE 15-11-2026 (livraison 1 du superviseur R-759, SUPERVISEUR_GHUB2_Dim_15-11-2026.md) : avec un
  « .git » au dépôt privé, ce qui se publie est LU DANS LE COMMIT HEAD (`extraire_le_commit`), jamais sur le disque ;
  après l'écriture, l'ÉTAGE A refuse un fichier écrit identique à un fichier du dépôt privé qui ne se publie pas
  (historique entier, toutes branches, disque ; un dépôt superficiel s'arrête), et le TÉMOIN DU PARCOURS exige chaque
  chemin du registre de provenance présent et lisible (`refus_selon_l_historique`).
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 (A-543) : le quota gratuit des
  machines GitHub du dépôt privé est épuisé ; un dépôt public ne consomme rien ;
  Jean-Luc a écarté de faire tourner depuis le public le code du privé (« Non
  pas question de prendre ces risques », zone grise des conditions d'usage de
  GitHub) et retenu de publier le circuit ET les programmes qu'il lance ; puis,
  le même soir à 22h29, de les publier avec leurs chiffres de stratégie pour le
  moment (A-556). Deux rédactions d'un même circuit divergent toujours (R-708) :
  celle du public est donc FABRIQUÉE depuis celle du privé, jamais écrite à la main.
  Décision de Jean-Luc du 12-10-2026 à 16h46 (« Oui, construire », après la liste des
  fichiers et le point « il publierait tous les programmes au lieu d'une liste tenue à
  la main ») : la certification passe elle aussi au dépôt public, en y PUBLIANT le code
  qu'elle exécute, au lieu d'y exécuter le code du privé, qu'il avait écarté le
  08-10-2026 ; ordre confirmé le 15-10-2026 à 08h36 (A-580, A-576). Publier TOUS les
  programmes, et non une liste, répare le défaut que cette fiche consignait : un
  programme oublié dans la liste s'exécutait depuis le clone du dépôt privé, sans
  alarme.
  LES SÉRIES AVANT LA FUSION — décision de Jean-Luc du 05-11-2026 à 13h36. La question : « Comment veut-on
  utiliser GitHub pour les séries ? » ; options : 1. après la fusion (circuit tel quel, retour arrière par
  « git revert » si la série est NON CONFORME) ; 2. avant la fusion (le circuit reçoit une entrée « version en
  attente », le dépôt public reçoit le code de cette version sur une branche du même nom, le contrôle d'identité
  compare à cette branche au lieu de main) ; 3. réponse libre. Réponse : « 2 ». Raison : avec 1, une version non
  éprouvée par ses séries serait la version officielle pendant environ une heure, une baisse de contrôle ; avec 2,
  la barrière « séries conformes avant fusion » est gardée, et « publier ce qui tourne » reste le cadre du
  08-10-2026. D'où l'entrée « version » du circuit des séries (SERIES_VERSION) et `refus_de_branche`.
⑨ CE QUI CLOCHE — Le contrôle d'identité porte sur `programmes/*.py`, `tests/*.py`
  et `tests/LANCEMENT_DES_EPREUVES.json`. Un pas qui lancerait du code rangé ailleurs
  (`etudes/outils/`, `tests/outils/`…) l'exécuterait depuis le clone du dépôt privé :
  relevé le 15-10-2026 par une relecture indépendante, des épreuves en lançaient
  (`emp.py`, cinq outils de `etudes/outils/` ; puis, relevé le 01-11-2026, l'épreuve du
  joueur de séries lance `tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py`) : ils sont
  désormais publiés (`tests/outils/` depuis le 01-11-2026), et le pas
  « poser le code » de la certification EFFACE de la machine tout autre `*.py` privé, et
  tout code compilé (les suffixes que Python importe, calculés par Python lui-même :
  un paquet `.pyc` ou une extension `.so` passeraient avant le `.py` publié), avant de
  rien lancer ; il refuse les liens symboliques et voit les fichiers cachés. Un pas qui
  tourne après un échec (une condition qui appelle always(), failure(), cancelled() ou success()) ne tourne que si
  le code public est posé : propriété écrite UNE fois (`condition_exige_le_code_pose`), appliquée par
  `proteger_les_pas`, relue par la post-condition `verifier_les_pas` (superviseur R-759 du 30-10-2026, défaut E3 : la
  chaîne exacte « if: always() » remplacée laissait passer « always() && … »). Le circuit du soir, lui, n'efface rien : ses pas lisent tout le
  dépôt (le pilote, le radar) et son contrôle porte sur `programmes/*.py` seulement ;
  relevé le 08-10-2026, il ne lance aucun programme hors de `programmes/`. Le pas « Poser » du soir
  refuse tout fichier compilé (.pyc, .so, .pyd) OÙ QU'IL SOIT dans le clone, même hors de
  `programmes/` : plus large que nécessaire, laissé tel quel (relecteur du 21-10-2026, mineur 1). Il les
  reconnaît à leur SUFFIXE : une archive `.zip` ou un code compilé sous un autre nom n'est pas vu (voir ⑨ du garde). Le circuit de la certification est
  écrit dans ce programme, et non fabriqué depuis un fichier du privé :
  `.github/workflows/certifier.yml`, au privé, ne tourne plus (quota épuisé) et n'est
  pas la source de celui-ci.
  LA CERTIFICATION EN TRANCHES (30-10-2026, voir TRANCHES_DE_LA_NUIT) : la tâche finale
  (job « reunir ») ne porte pas de limite écrite ; GitHub lui donne ses 6 heures par défaut.
  programmes/MESSAGE_DU_SOIR.py lit UNE limite dans le gabarit (celle des tranches) pour dire
  quand le passage a eu le temps de finir : la durée de la tâche finale n'y est pas comptée
  (quelques minutes attendues, jamais mesurées sur GitHub).
  Le job du circuit ne tourne que si le premier job a répondu « tourner » : si ce
  premier job tombe avant de répondre (clonage refusé, réseau), le passage ne fait
  rien et rougit ; le réveil suivant (secours du soir, rattrapage du matin) reprend.
⑩ EFFET — ÉCRIT dans le clone public : les `*.py` de la racine, de `programmes/`,
  de `tests/`, de `etudes/outils/` et de `tests/outils/`, `tests/LANCEMENT_DES_EPREUVES.json`,
  `.github/workflows/circuit_du_soir.yml`, `.github/workflows/certifier_la_version.yml` et
  `.github/workflows/series_longues.yml` ; et `circuits_du_prive/*.yml` ; RETIRE du clone public, à ces emplacements, ce qui
  est absent du dépôt privé. Ne pousse rien. Lance git en lecture (la branche des deux dépôts).
⑪ TERMINAISON — Rend la main. Aucun appel qui puisse ne pas revenir. [sort: oui]
⑫ DÉFINITIONS
  le circuit du soir : la suite de programmes lancés chaque soir de bourse par
    GitHub Actions — collecte des cours, versement, signaux, positions, mesure,
    pilote, radar.
  le dépôt privé : `jeanlucsilbertmds-cyber/Cac-40-signals-sur-git-hub-pour-Claude-`.
  le dépôt public : `jeanlucsilbertmds-cyber/cac40-cours-public`.
"""
import csv
import hashlib
import importlib.util
import json
import os
import posixpath
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unicodedata

DEPOT_PRIVE = "jeanlucsilbertmds-cyber/Cac-40-signals-sur-git-hub-pour-Claude-"
CIRCUIT_PRIVE = os.path.join(".github", "workflows", "collecte_abc.yml")
CIRCUIT_PUBLIC = os.path.join(".github", "workflows", "circuit_du_soir.yml")

# LES CINQ EMPLACEMENTS DU CODE PUBLIÉ, chacun sans ses sous-dossiers : la racine du dépôt (""), programmes/,
# tests/, etudes/outils/ et tests/outils/. Décision de Jean-Luc du 15-10-2026 à 15h29 (« 1 ») : publier aussi les
# outils d'études et le code de la racine (emp.py), que des épreuves exécutent, et effacer tout autre code privé de la
# machine de la certification avant de rien lancer (relecture indépendante du 15-10-2026, cassures B1 et B2).
# Décision de Jean-Luc du 01-11-2026 à 13h39 (« 1 » à « publier tests/outils/ au dépôt public ») : l'épreuve du joueur
# de séries (tests/EPREUVES_DU_JOUEUR_DE_SERIES_Sam_17-10-2026.py) lance tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py ;
# le pas « poser le code » l'effaçait, et elle rougissait à chaque passage public depuis le 21-10-2026 (« FAUX J1
# (code 2), J3 (code 2) »). CETTE LISTE EST LA SEULE : la boucle et le motif d'effacement du pas « poser le code » en
# sont tirés (`pour_le_pas_poser`), jamais recopiés (R-708 : deux implémentations d'une même chose divergent toujours).
DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils", "tests/outils")


def pour_le_pas_poser(dossiers):
    """Rend la liste des emplacements et le motif d'un fichier publié, écrits pour le pas « poser le code ».

    ① RÔLE — Traduire DOSSIERS_DE_CODE dans la langue du pas « poser le code » de la certification (bash et grep -E).
    ② CONTEXTE D'APPEL — Une fois, au chargement du module, pour fabriquer DEPART_DE_LA_CERTIFICATION ; les épreuves du
      circuit public (tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py) et la simulation de l'effacement.
    ③ ENTRÉE — `dossiers` : les emplacements, chemins relatifs à la racine, « » pour la racine elle-même.
    ④ CONDITIONS D'ENTRÉE — Les noms ne portent ni espace ni caractère spécial de grep -E autre que le point (vrai pour
      les cinq emplacements du 01-11-2026) : seul le point est protégé.
    ⑤ SORTIE — DEUX valeurs : la liste pour la boucle shell, séparée par des espaces, « . » pour la racine (au
      01-11-2026 : « . programmes tests etudes/outils tests/outils ») ; le motif grep -E d'un fichier `.py` publié, chemin
      commençant par « ./ » comme les rend `find .` (au 01-11-2026 :
      « ^[.]/[^/]+[.]py$|^[.]/(programmes|tests|etudes/outils|tests/outils)/[^/]+[.]py$ »).
      [rend: 2]
    ⑥ TRAITEMENT — La racine donne « . » dans la boucle et « ^[.]/[^/]+[.]py$ » dans le motif ; chaque autre emplacement
      est ajouté à la boucle et à une alternative « ^[.]/(…)/[^/]+[.]py$ », son point écrit « [.] ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Jusqu'au 01-11-2026, le pas épelait la liste à quatre endroits (deux boucles, deux motifs) : publier
      un emplacement demandait cinq écritures, et une boucle sans le motif aurait effacé ce que l'autre recopie, ou
      l'inverse. Décision de Jean-Luc du 01-11-2026 à 13h39 (voir DOSSIERS_DE_CODE).
    ⑨ CE QUI CLOCHE — Un emplacement dont le nom porterait un autre caractère spécial (« + », « ( », une espace)
      fausserait le motif ou la boucle sans erreur : aucun aujourd'hui. · Un emplacement qui en contient un autre
      (« tests » et « tests/outils ») est sans effet sur le motif : « [^/]+ » ne traverse pas de « / ».
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    boucle, sous = [], []
    for d in dossiers:
        if d:
            boucle.append(d)
            sous.append(d.replace(".", "[.]"))
        else:
            boucle.append(".")
    racine = ["^[.]/[^/]+[.]py$"] if "" in dossiers else []
    return " ".join(boucle), "|".join(racine + ["^[.]/(" + "|".join(sous) + ")/[^/]+[.]py$"])


BOUCLE_DU_CODE, MOTIF_DU_CODE = pour_le_pas_poser(DOSSIERS_DE_CODE)


def _chemin(dossier, fichier):
    """Rend le chemin d'un fichier d'un emplacement de code, relatif à la racine.

    ① RÔLE — Écrire « emp.py » pour la racine et « programmes/X.py » ailleurs.
    ② CONTEXTE D'APPEL — `code_a_publier`, `main`.
    ③ ENTRÉE — `dossier` : un emplacement de DOSSIERS_DE_CODE (« » pour la racine) · `fichier` : un nom.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin.
      [rend: 1]
    ⑥ TRAITEMENT — joindre par « / », sauf pour la racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un seul endroit qui écrit ces chemins : le contrôle et la copie parlent la même langue.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return fichier if not dossier else dossier + "/" + fichier
LANCEMENT = "tests/LANCEMENT_DES_EPREUVES.json"
CIRCUIT_CERTIFICATION = os.path.join(".github", "workflows", "certifier_la_version.yml")
# LE CIRCUIT DES SÉRIES LONGUES DE SABOTAGES (patch du 04-11-2026) : lancé à la main seulement ; ses pas de départ et
# de dépôt sont ceux de la certification (`depart_pour`, `pas_de_depot`), jamais recopiés.
CIRCUIT_SERIES = os.path.join(".github", "workflows", "series_longues.yml")
# LE CIRCUIT DES ÉPREUVES LONGUES D'UN TENANT (étape GHUB ②, 15-11-2026 ; A-809, A-811, A-816 de Jean-Luc, « GitHub en
# priorité ») : une demande nomme des CODES d'épreuves ; chaque code renvoie, dans la table « epreuves_longues » de
# tests/LANCEMENT_DES_EPREUVES.json, à une commande FIGÉE. Ses pas de départ et de dépôt sont ceux des séries.
CIRCUIT_EPREUVES = os.path.join(".github", "workflows", "epreuves_longues.yml")
# LES FICHES DE CIRCUIT DU PRIVÉ, PUBLIÉES À PART (décision de Jean-Luc du 15-10-2026 à 20h32, « 1 ») : une épreuve
# publiée (celle du rattrapage) EXÉCUTE un pas écrit dans une fiche `.github/workflows/*.yml` du dépôt qu'on lui donne
# (relecture de Cowork 5855cd4, cassure L). Les fiches du privé sont donc publiées, et comparées comme le code, mais
# dans ce dossier-ci et jamais dans `.github/workflows/` du public, où GitHub les mettrait en service.
FICHES_PRIVEES = os.path.join(".github", "workflows")
FICHES_PUBLIEES = "circuits_du_prive"


def fiches_a_publier(prive):
    """Rend les noms des fiches de circuit du dépôt privé (`.github/workflows/*.yml` et `*.yaml`).

    ① RÔLE — Dire quelles fiches de circuit vont au public, sous `circuits_du_prive/`.
    ② CONTEXTE D'APPEL — `main` ; les épreuves du circuit public.
    ③ ENTRÉE — `prive` : la racine du dépôt privé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des noms de fichiers (vide si aucun).
      [rend: 1]
    ⑥ TRAITEMENT — lister le dossier des fiches, garder les fichiers `.yml` et `.yaml`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une fiche de circuit est du code : ses pas s'exécutent (cassure L, 15-10-2026). Une propriété, pas
      une liste : une fiche ajoutée au privé est publiée sans qu'on y pense.
    ⑨ CE QUI CLOCHE — Les sous-dossiers ne sont pas parcourus : GitHub n'y lit aucune fiche.
    ⑩ EFFET — Lit un dossier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    d = os.path.join(prive, FICHES_PRIVEES)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.endswith((".yml", ".yaml")) and os.path.isfile(os.path.join(d, f)))


def code_a_publier(prive):
    """Rend la liste des fichiers de code du dépôt privé qui vont au public.

    ① RÔLE — Dire quels fichiers publier : tout `*.py` de chaque emplacement de
      DOSSIERS_DE_CODE (la racine, `programmes/`, `tests/`, `etudes/outils/`,
      `tests/outils/` au 01-11-2026), et `tests/LANCEMENT_DES_EPREUVES.json`, en
      chemins relatifs à la racine.
    ② CONTEXTE D'APPEL — `main` ; les épreuves du circuit public.
    ③ ENTRÉE — `prive` : la racine du dépôt privé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des chemins (vide si rien).
      [rend: 1]
    ⑥ TRAITEMENT — lister chaque emplacement, garder les fichiers `.py`, ajouter
      le fichier de lancement s'il existe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une propriété, jamais une énumération : renommer ou ajouter un
      programme ne doit pas le faire sortir de la publication (voir la fiche du
      fichier, ⑧).
    ⑨ CE QUI CLOCHE — Les sous-dossiers ne sont pas parcourus : relevé le 15-10-2026,
      `programmes/` n'en a pas ; ceux de `tests/` portent des données (`resultats/`,
      `temoins_*`) et un programme, `tests/outils/`, publié comme son propre emplacement
      depuis le 01-11-2026 (décision de Jean-Luc de 13h39). Le code qui n'est pas publié est
      EFFACÉ de la machine de la certification avant qu'elle ne lance rien (son pas
      « poser le code ») : une épreuve qui en aurait besoin rougit, elle ne l'exécute pas.
      · Un sous-dossier ajouté un jour à `tests/outils/` ne serait pas publié non plus.
    ⑩ EFFET — Lit les dossiers de DOSSIERS_DE_CODE.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rendu = []
    for dossier in DOSSIERS_DE_CODE:
        d = os.path.join(prive, dossier)
        if os.path.isdir(d):
            rendu += [_chemin(dossier, f) for f in os.listdir(d)
                      if f.endswith(".py") and os.path.isfile(os.path.join(d, f))]
    if os.path.isfile(os.path.join(prive, LANCEMENT)):
        rendu.append(LANCEMENT)
    return sorted(rendu)


# LA FORME D'UN JETON vit dans UN module, voisin de ce programme (superviseur R-759 du 05-11-2026 à 00h52, D1 : deux
# implémentations d'une même chose divergent toujours, R-708). Il est chargé PAR SON CHEMIN, à côté de ce fichier,
# jamais par son nom : c'est toujours le voisin qui juge, jamais un module de même nom déjà chargé d'ailleurs. Et
# seulement au moment de refuser : les programmes qui lisent ce fichier comme une donnée (MESSAGE_DU_SOIR.py,
# CERTIFIER_LA_VERSION.py, des épreuves qui le copient seul) n'en dépendent pas.
MODULE_DU_JETON = "FORME_D_UN_JETON.py"


def forme_d_un_jeton():
    """Rend le module de la forme d'un jeton, chargé depuis le dossier de ce programme.

    ① RÔLE — Donner à `refus_avant_publication` le seul motif de jeton du dépôt (programmes/FORME_D_UN_JETON.py).
    ② CONTEXTE D'APPEL — `refus_avant_publication`, une fois par appel.
    ③ ENTRÉE — — (le nom du module est MODULE_DU_JETON).
    ④ CONDITIONS D'ENTRÉE — Le module existe à côté de ce fichier. Sinon l'exception de lecture remonte : `main`
      l'arrête (code 1, rien n'est écrit).
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — Construire le chemin à partir de celui de ce fichier, charger et exécuter le module.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un chargement par le nom prendrait le premier module de ce nom sur les chemins de Python, ou celui
      déjà chargé : une épreuve qui lance le fabricant d'une copie sabotée doit être jugée par le module de la copie.
    ⑨ CE QUI CLOCHE — Le module est exécuté à chaque appel (une fois par fabrication) : sans coût mesurable. · Il est
      EXÉCUTÉ avant d'être contrôlé (s'il est un lien hors du dépôt, sa cible tourne, puis le lien est refusé :
      relecture du tour 2, D5) ; c'est la même confiance que pour ce fabricant, que Python exécute avant tout.
    ⑩ EFFET — Lit et exécute un fichier Python du dépôt.
    ⑪ TERMINAISON — Rend la main ; le module ne fait que compiler un motif.
      [sort: non]
    """
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODULE_DU_JETON)
    spec = importlib.util.spec_from_file_location("forme_d_un_jeton_du_fabricant", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# LA GARDE DES LIGNES ENTIÈRES — SA VRAIE PORTÉE (réécrite le 15-11-2026, livraison 1 du superviseur R-759,
# SUPERVISEUR_GHUB2_Dim_15-11-2026.md, § 3 : « l'ancienne garde des lignes entières reste en place, avec sa phrase de
# tête réduite à ce qu'elle fait vraiment ») : elle refuse un fichier publié qui recopie TELLE QUELLE une LIGNE ENTIÈRE
# d'un fichier texte UTF-8 de `donnees/`, commençant à un début reconnu (DEBUT_POSSIBLE_D_UNE_LIGNE). ELLE NE GARDE PAS
# « les données du dépôt privé » : une ligne entre « », entre accents graves, après « : », découpée en champs, avec un
# autre séparateur, ou un fichier de données hors de `donnees/`, passent (Cowork, 15-11-2026, G03 à G10) ; vingt barres
# réelles sont déjà dans le code publié (A-825). La garde de la FORME (aucune ligne publiée ne porte une date et des
# prix) est la livraison 2 ; le fichier entier recopié est gardé par l'étage A (`refus_selon_l_historique`).
# Son origine (superviseur R-759 du 15-11-2026, SUPERVISEUR_GHUB_Dim_15-11-2026.md,
# 2.1, « voie élargie par A-811 : la branche publiée ») : publier le code de chaque version en attente, c'est publier
# ses épreuves, qui portent des cas tirés de vraies lignes de fichier (R-732), alors que les cours des 20 ans ne
# doivent jamais entrer au public (A-555) et que les cours d'ABC en sortent (A-662). Un fichier de données ajouté
# demain à `donnees/` est couvert, pour ses lignes entières seulement. Une « ligne chiffrée » : une ligne d'un fichier texte UTF-8 de
# DOSSIER_DES_DONNEES, sans ses blancs de bord, d'au moins LONGUEUR_D_UNE_LIGNE_DE_DONNEES caractères, dont au moins
# CHIFFRES_D_UNE_LIGNE_DE_DONNEES chiffres. Mesure du 15-11-2026 (travail-ghub sur main 7d8024de) : 0 de ces lignes
# dans les 196 fichiers que publie le fabricant ; la vraie ligne d'Accor du 03-01-2000 de bnains_cac40.csv, posée dans
# un texte d'épreuve, est trouvée.
DOSSIER_DES_DONNEES = "donnees"
LONGUEUR_D_UNE_LIGNE_DE_DONNEES = 25      # caractères, celle que le superviseur a mesurée (0 sur 160 522 lignes de bnains)
CHIFFRES_D_UNE_LIGNE_DE_DONNEES = 6       # chiffres au moins : une ligne d'en-tête ou un chemin sans date n'en est pas
# Où une ligne de données peut commencer dans un fichier publié : en début de ligne (après les blancs, et après un
# « # » de commentaire suivi de blancs), après un guillemet, une parenthèse ou un crochet ouvrants, ou après la
# séquence « \n » écrite dans une chaîne.
DEBUT_POSSIBLE_D_UNE_LIGNE = re.compile(r"(?m)^[ \t]*(?:#+[ \t]*)?|[\"'(\[]|\\n")


def _ne_pas_taire(erreur):
    """Fait échouer un parcours `os.walk` qui n'a pas pu lire un dossier, sauf le dossier de tête absent.

    ① RÔLE — Le `onerror` des parcours de ce programme (R-734 : un contrôle qui n'a pas pu tourner rend un code non nul).
    ② CONTEXTE D'APPEL — `os.walk` de `lignes_de_donnees` et de `refus_selon_l_historique`.
    ③ ENTRÉE — `erreur` : l'OSError que `os.walk` a rencontrée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur ; lève l'erreur, sauf « fichier absent » (ENOENT), que le témoin du parcours juge.
      [rend: rien]
    ⑥ TRAITEMENT — Laisser passer ENOENT (le `donnees/` absent d'un dépôt d'essai ; un fichier effacé pendant le
      parcours), lever tout le reste (droit de lecture refusé, dossier illisible).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — C-D2 de Cowork (15-11-2026) : « dépôt sans donnees/ : index 0 lignes ; refus : [] » ; un `os.walk` sans
      `onerror` saute en silence un dossier illisible. Le dossier ABSENT est jugé par le témoin du parcours (chaque
      chemin du registre de provenance doit être présent et lisible, `refus_selon_l_historique`).
    ⑨ CE QUI CLOCHE — Un dossier absent sans registre (dépôt d'essai) n'est pas une erreur : c'est voulu.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    import errno
    if getattr(erreur, "errno", None) != errno.ENOENT:
        raise erreur


def lignes_de_donnees(prive):
    """Rend l'index des lignes chiffrées des fichiers de données du dépôt privé.

    ① RÔLE — Lire, une fois par publication, les lignes que le public ne doit jamais porter telles quelles.
    ② CONTEXTE D'APPEL — `refus_avant_publication`, une fois par appel.
    ③ ENTRÉE — `prive` : la racine du dépôt privé.
    ④ CONDITIONS D'ENTRÉE — — (un dossier `donnees/` absent donne un index vide : un dépôt d'essai n'en a pas ; un
      vrai dépôt sans `donnees/` est arrêté par le témoin du parcours, `refus_selon_l_historique`). Un dossier
      illisible lève OSError (`_ne_pas_taire`), que `main` arrête (code 1).
    ⑤ SORTIE — UNE valeur : un dictionnaire {les LONGUEUR_D_UNE_LIGNE_DE_DONNEES premiers caractères : la ligne, ou
      l'ensemble des lignes qui commencent ainsi}.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir `prive/donnees` sans suivre les liens ; pour chaque fichier ordinaire (pas un lien) qui
      se décode en UTF-8, chaque ligne sans ses blancs de bord, longue d'au moins LONGUEUR_D_UNE_LIGNE_DE_DONNEES
      caractères, est rangée sous son début. Les chiffres ne sont pas comptés ici, mais à la rencontre
      (`refus_avant_publication`) : compter un million de lignes coûtait 8 s, ranger les débuts en coûte 2 (mesuré le
      15-11-2026 sur la machine du Chat).
    ⑦ UNITÉ — Des caractères.
    ⑧ POURQUOI — Commentaire de DOSSIER_DES_DONNEES.
    ⑨ CE QUI CLOCHE — Les fichiers qui ne se décodent pas en UTF-8 ne sont pas lus, et les archives ZIP ne sont pas
      ouvertes : une ligne des archives de bnains (2000-2017, dans `donnees/sources_bnains/archives_bnains/*.ZIP`)
      publiée telle quelle n'est pas vue (leurs noms sont en Latin-1, `zipfile` refuse de les lire : mesuré le
      15-11-2026) → BACKLOG. Les données rangées hors de `donnees/` (témoins, études) ne sont pas lues → BACKLOG.
    ⑩ EFFET — Lit des fichiers. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; des lectures de fichiers locaux.
      [sort: non]
    """
    index = {}
    for dossier, sous, fichiers in os.walk(os.path.join(prive, DOSSIER_DES_DONNEES), onerror=_ne_pas_taire):
        sous[:] = [s for s in sous if not os.path.islink(os.path.join(dossier, s))]
        for f in fichiers:
            p = os.path.join(dossier, f)
            if os.path.islink(p) or not os.path.isfile(p):
                continue
            try:
                with open(p, "rb") as e:
                    texte = e.read().decode("utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for ligne in texte.splitlines():
                if len(ligne) < LONGUEUR_D_UNE_LIGNE_DE_DONNEES:
                    continue
                ligne = ligne.strip()
                if len(ligne) < LONGUEUR_D_UNE_LIGNE_DE_DONNEES:
                    continue
                cle = ligne[:LONGUEUR_D_UNE_LIGNE_DE_DONNEES]
                deja = index.get(cle)
                if deja is None:
                    index[cle] = ligne
                elif isinstance(deja, str):
                    if deja != ligne:
                        index[cle] = {deja, ligne}
                else:
                    deja.add(ligne)
    return index


def ligne_de_donnees_publiee(texte, index):
    """Rend la première ligne chiffrée de l'index que `texte` porte telle quelle, ou None.

    ① RÔLE — Dire si un fichier à publier recopie une ligne de données du dépôt privé.
    ② CONTEXTE D'APPEL — `refus_avant_publication`, une fois par fichier dont le texte est strict et sans jeton.
    ③ ENTRÉE — `texte` : le contenu du fichier · `index` : celui de `lignes_de_donnees`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la ligne trouvée, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — À chaque début possible (DEBUT_POSSIBLE_D_UNE_LIGNE), les LONGUEUR_D_UNE_LIGNE_DE_DONNEES
      caractères suivants sont cherchés dans l'index ; une ligne de l'index qui commence là, en entier, et porte au
      moins CHIFFRES_D_UNE_LIGNE_DE_DONNEES chiffres, est rendue.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de DOSSIER_DES_DONNEES. La ligne ENTIÈRE est comparée : un début seul faisait 239 faux
      rouges sur le code publié (des chemins de fichiers du registre de provenance), mesuré le 15-11-2026.
    ⑨ CE QUI CLOCHE — Une ligne recopiée après d'autres caractères sur la même ligne du fichier publié (« x = 1;
      ACCOR,2000-… ») ou coupée en deux chaînes n'est pas vue ; une ligne de données plus courte que
      LONGUEUR_D_UNE_LIGNE_DE_DONNEES non plus → BACKLOG.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for m in DEBUT_POSSIBLE_D_UNE_LIGNE.finditer(texte):
        i = m.end()
        lignes = index.get(texte[i:i + LONGUEUR_D_UNE_LIGNE_DE_DONNEES])
        if lignes is None:
            continue
        for ligne in ([lignes] if isinstance(lignes, str) else sorted(lignes)):
            if texte.startswith(ligne, i) and sum(c.isdigit() for c in ligne) >= CHIFFRES_D_UNE_LIGNE_DE_DONNEES:
                return ligne
    return None


def refus_avant_publication(prive, chemins, source=None):
    """Rend les raisons de refuser la publication : liens, chemins réels hors du dépôt, liens durs, texte non strict,
    jetons, lignes de données.

    ① RÔLE — Dire, AVANT que rien ne soit écrit au dépôt public, si un des fichiers que le fabricant s'apprête à
      publier est un lien symbolique, a un chemin réel qui n'est pas son chemin dans le dépôt privé (un dossier lié,
      une cible hors du dépôt), est un lien dur (le même fichier porte un autre nom, peut-être hors du dépôt), n'est
      pas du TEXTE UTF-8 STRICT (de l'UTF-8 valide sans aucun caractère de contrôle, catégorie Unicode Cc, hors
      tabulation et sauts de ligne), porte une chaîne de la forme d'un jeton (programmes/FORME_D_UN_JETON.py), ou porte
      telle quelle une ligne chiffrée d'un fichier de `donnees/` (`ligne_de_donnees_publiee`, 15-11-2026). Un seul
      contrôle pour les deux familles publiées : le code (`code_a_publier`) et les fiches de circuit
      (`fiches_a_publier`).
    ② CONTEXTE D'APPEL — `main`, une fois, juste après avoir dressé les deux listes et avant de fabriquer ou d'écrire
      quoi que ce soit ; les épreuves du circuit public (E8 de tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py).
    ③ ENTRÉE — `prive` : la racine du dépôt privé (ses `donnees/` sont lues) · `chemins` : les chemins des fichiers à
      publier, relatifs à la source, séparés par « / » (« programmes/X.py », « .github/workflows/collecte_abc.yml ») ·
      `source` (15-11-2026, livraison 1 du superviseur R-759 GHUB2) : le dossier où les fichiers à publier sont LUS —
      le commit du dépôt privé extrait par `extraire_le_commit` ; None : le dépôt privé lui-même (un dépôt sans git).
    ④ CONDITIONS D'ENTRÉE — Chaque chemin désigne une entrée existante (les deux listes ne rendent que des fichiers
      vus par `os.path.isfile`, qui suit les liens) ; programmes/FORME_D_UN_JETON.py est à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : la liste des refus, une phrase par fichier refusé (la première raison trouvée), dans
      l'ordre de `chemins` ; vide si tout peut être publié. La phrase nomme le fichier et la raison, JAMAIS le contenu
      trouvé ni la cible d'un lien. TOUS les fichiers sont examinés, pas seulement le premier fautif.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque chemin : ① un lien symbolique est refusé, en disant s'il mène hors du dépôt ; ② sinon,
      si le chemin réel (tous liens résolus, `os.path.realpath`) n'est pas exactement la racine réelle du dépôt
      suivie du chemin, le fichier est refusé : hors du dépôt, ou atteint par un dossier lié ; ③ sinon, un fichier qui
      a plus d'un nom (`st_nlink > 1`) est refusé ; ④ sinon seulement, le contenu est lu EN ENTIER, en octets : refusé
      s'il ne se décode pas en UTF-8 (clause UTF-8), puis s'il porte un caractère de catégorie Cc autre que la
      tabulation, le saut de ligne et le retour chariot (clause des contrôles ; le refus nomme le premier, U+XXXX),
      puis s'il porte la forme d'un jeton, puis s'il porte une ligne chiffrée de `donnees/` (clause des données ; le
      refus nomme le fichier, jamais la ligne : le message s'affiche et pourrait être lu). Le contenu d'un fichier refusé en ①, ② ou ③ n'est jamais lu : on ne lit pas, même en mémoire, un fichier qui peut être hors du dépôt.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Défaut M5, mesuré par Cowork le 04-11-2026 à 21h17 (echanges/RELU.md, I1) : `shutil.copyfile` suit
      les liens, et `os.path.isfile` aussi ; un lien `etudes/outils/HORS.py` ou `.github/workflows/hors.yml` vers un
      fichier secret posé sur la machine hors du dépôt a été publié avec le contenu de sa cible, et un `.py` portant
      une chaîne de forme jeton a été publié tel quel, fabricant au code 0. Le pas « poser le code » de la
      certification refuse les liens `*.py`, mais au passage suivant, donc APRÈS la poussée publique : trop tard pour
      un secret. Relecture neuve du 04-11-2026 et superviseur R-759 du 05-11-2026 à 00h52 : un lien dur vers un
      fichier hors du dépôt était publié (D4, cas A1), et un fichier en UTF-16 portant un jeton aussi (D5, cas A5).
      Relecture neuve du tour 2 (05-11-2026, D1) : un octet nul est de l'UTF-8 valide, et un jeton en UTF-16 ou
      UTF-32 SANS BOM était publié, fabricant au code 0 ; le superviseur R-759 du 05-11-2026 à 03h10 a jugé « DE
      FOND » le texte strict (0 refus mesuré sur les 144 fichiers que publie le fabricant). Clause des données :
      commentaire de DOSSIER_DES_DONNEES (superviseur R-759 du 15-11-2026, 2.1).
      Réparé par des PROPRIÉTÉS (le chemin réel égale le chemin logique ; un seul nom ; tout ce qui est publié est du
      texte UTF-8 strict ; aucune forme de jeton), jamais par une liste de noms ni d'encodages ; et à UN seul endroit, appelé
      pour le code ET pour les fiches (R-708 : deux implémentations d'une même chose divergent toujours).
    ⑨ CE QUI CLOCHE — Le motif a les limites de tout motif (voir la fiche de programmes/FORME_D_UN_JETON.py) : un
      jeton coupé en deux littéraux, une valeur base64 écrite sans « Authorization: » devant (relecture du
      04-11-2026, A4 et A7), une clé d'un autre service, un mot de passe en clair passent. · Faux rouges possibles :
      un exemple d'adresse à identifiant et secret, ou d'en-tête « Authorization: Basic » suivi d'un mot de 8 lettres,
      écrit d'un bloc dans un commentaire ; un fichier du dépôt qui porterait deux noms DANS le dépôt (git n'en crée pas) ; le message le
      dit, rien n'est publié. · Les deux circuits FABRIQUÉS (soir, certification) ne sont pas passés au motif : ils
      sont faits du texte de `collecte_abc.yml` (une fiche contrôlée ici) et de textes de ce programme (publié, donc
      contrôlé ici). · Le texte strict ne ferme pas les transformations qui restent du texte (UTF-7, base64, jeton
      coupé) : limite du motif. Une fiche portant U+0085 est arrêtée ici, avant le sous-ensemble YAML (code 1, le
      refus nomme U+0085). · ENTRE LE CONTRÔLE ET LA COPIE, le fichier est rouvert PAR SON NOM par `shutil.copyfile`, qui
      suit les liens : si un acteur local le change, ou le remplace par un lien, pendant que le fabricant tourne,
      c'est le fichier changé qui est publié (relecture du 04-11-2026, D3, cas T1 et T2) ; de même un dossier échangé
      entre `os.path.realpath` et l'ouverture n'est pas vu. Le remède jugé de fond (publier les blobs commités) est en place
      depuis le 15-11-2026 quand le dépôt privé porte un « .git » : `main` lit alors les fichiers dans le commit extrait
      (`source`), un dossier neuf qu'il a lui-même écrit ; sans « .git » (une copie d'épreuve), rien ne peut être
      poussé (`refus_de_branche`). · CÔTÉ PUBLIC, rien n'est contrôlé :
      si `circuits_du_prive/` du clone public est un lien vers `.github/workflows/`, les fiches du privé y sont
      écrites et GitHub les MET EN SERVICE au dépôt public, avec ses secrets (relecture du 04-11-2026, D6, cas P1 :
      les sept fiches du privé arrivées dans `.github/workflows/` du public, fabricant au code 0) ; il faut pour cela
      un lien commité au dépôt public, que seul ce circuit écrit. La propriété « tout chemin écrit ou effacé au public
      a pour chemin réel la racine réelle du public suivie du chemin » est proposée au BACKLOG.
    ⑩ EFFET — Lit les fichiers non refusés en ①, ② et ③, les fichiers texte de `donnees/` (`lignes_de_donnees`, environ
      2 s sur le vrai dépôt), et charge programmes/FORME_D_UN_JETON.py. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; des lectures de fichiers locaux, aucun appel qui puisse ne pas revenir.
      [sort: non]
    """
    forme = forme_d_un_jeton()
    donnees = lignes_de_donnees(prive)
    prive = prive if source is None else source   # les fichiers à publier sont lus dans la source (le commit extrait)
    racine = os.path.realpath(prive)
    refus = []
    for rel in chemins:
        p = os.path.join(prive, rel)
        reel = os.path.realpath(p)
        dehors = os.path.commonpath([racine, reel]) != racine
        if os.path.islink(p):
            refus.append(f"{rel} : lien symbolique" + (" vers un fichier HORS du dépôt privé" if dehors else ""))
        elif reel != os.path.normpath(os.path.join(racine, rel)):
            refus.append(f"{rel} : chemin réel HORS du dépôt privé" if dehors
                         else f"{rel} : atteint par un dossier lié (son chemin réel n'est pas le sien)")
        elif os.stat(p).st_nlink > 1:
            refus.append(f"{rel} : lien dur (le même fichier porte un autre nom, peut-être hors du dépôt privé)")
        else:
            with open(p, "rb") as e:
                octets = e.read()
            # ④ LE TEXTE STRICT (superviseur R-759 du 05-11-2026 à 03h10, D1) : deux clauses, chacune avec son refus.
            try:
                texte = octets.decode("utf-8")
            except UnicodeDecodeError:
                refus.append(f"{rel} : n'est pas du texte UTF-8 strict (clause UTF-8 : ne se décode pas en UTF-8 ; "
                             "un autre encodage échapperait au motif de jeton)")
                continue
            controle = next((c for c in texte if unicodedata.category(c) == "Cc" and c not in "\t\n\r"), None)
            if controle is not None:
                refus.append(f"{rel} : n'est pas du texte UTF-8 strict (clause des contrôles : caractère "
                             f"U+{ord(controle):04X}, catégorie Cc, hors tabulation et sauts de ligne ; un texte "
                             "entrelacé d'octets nuls, comme l'UTF-16 ou l'UTF-32 sans BOM, échapperait au motif de jeton)")
                continue
            if forme.porte_une_forme_de_jeton(octets):
                refus.append(f"{rel} : porte une chaîne de la forme d'un jeton")
                continue
            if ligne_de_donnees_publiee(texte, donnees) is not None:
                refus.append(f"{rel} : porte telle quelle une ligne chiffrée d'un fichier de {DOSSIER_DES_DONNEES}/ "
                             "(les données du dépôt privé ne se publient pas, A-555, A-662)")
    return refus


ENTETE = """# CIRCUIT DU SOIR — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py à partir du fichier du circuit
# du dépôt privé (A-543). Il fait tourner les programmes de ce dépôt sur les données
# du dépôt privé. Chaque pas passe par programmes/ETAPE_MUETTE.py : le journal public
# ne dit que « étape … : OK » ou « étape … : ÉCHEC » ; le détail est au dépôt privé.
name: Circuit du soir
on:
  workflow_dispatch:
    inputs:
      rattrapage:
        description: "Passage sans mesure de la performance"
        type: boolean
        default: false
  # QUATRE REVEILS, ET C'EST L'HORLOGE DE PARIS QUI DECIDE (decision de Jean-Luc du
  # 13-10-2026 : 18h07, secours 21h23, rattrapage 7h41). GitHub compte en heure
  # universelle, qui ne suit pas l'heure d'ete ; programmes/FAUT_IL_TOURNER.py lit
  # l'heure de Paris au demarrage reel : il tourne seulement si la derniere seance
  # close n'est pas finie (celle du jour apres 18h, la veille avant). Aucun reveil a l'heure pile : GitHub les
  # retarde en forte charge (passages de 23h25, 00h17, 02h10 avec 18h00 pile).
  schedule:
    - cron: "7 16 * * 1-5"     # 18h07 l'ete · 17h07 l'hiver (s'arrete si la veille est faite)
    - cron: "7 17 * * 1-5"     # 19h07 l'ete (travail deja fait) · 18h07 l'hiver
    - cron: "23 19 * * 1-5"    # secours : 21h23 l'ete · 20h23 l'hiver
    - cron: "41 5 * * 2-6"     # rattrapage : 7h41 l'ete · 6h41 l'hiver
concurrency:
  group: circuit-du-soir
  cancel-in-progress: false
permissions:
  contents: write
jobs:
"""

DEFAULTS = """    defaults:
      run:
        shell: python3 programmes/ETAPE_MUETTE.py {0}
"""

CLONAGES = """      - uses: actions/checkout@v5
        with:
          repository: %s
          token: ${{ secrets.JETON_DEPOTS }}
          fetch-depth: 0
      - uses: actions/checkout@v5
        with:
          path: _code
      - name: Poser les programmes publics, s'ils sont ceux du depot prive
        id: poser_les_programmes
        shell: python3 _code/programmes/ETAPE_MUETTE.py {0}
        run: |
          D=""
          for f in _code/programmes/*.py; do
            n=$(basename "$f")
            if [ -f "programmes/$n" ] && ! cmp -s "$f" "programmes/$n"; then D="$D $n"; fi
          done
          for f in programmes/*.py; do
            n=$(basename "$f")
            [ -f "_code/programmes/$n" ] || D="$D $n(absent-du-public)"
          done
          for x in programmes/*; do [ -d "$x" ] && D="$D $x(dossier)"; done
          for x in $(find . -path ./_code -prune -o -path ./.git -prune -o \\( -name '*.pyc' -o -name '*.so' -o -name '*.pyd' \\) -print); do D="$D $x(compile)"; done
          if [ -n "$D" ]; then echo "::error::PROGRAMMES PUBLICS DIFFERENTS DU DEPOT PRIVE :$D"; exit 1; fi
          cp _code/programmes/*.py programmes/
          mkdir -p "$RUNNER_TEMP/circuit_public" "$RUNNER_TEMP/garde"
          cp _code/.github/workflows/circuit_du_soir.yml "$RUNNER_TEMP/circuit_public/"
          cp _code/programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py "$RUNNER_TEMP/garde/sitecustomize.py"
          rm -rf "$RUNNER_TEMP/code" && mv _code "$RUNNER_TEMP/code"
          { echo "PYTHONPATH=$RUNNER_TEMP/garde"; echo "PYTHONDONTWRITEBYTECODE=1"; echo "GARDE_DONNEES=$GITHUB_WORKSPACE"; echo "GARDE_CODE=$RUNNER_TEMP/code"; } >> "$GITHUB_ENV"
      - name: Le garde du code mord-il ?
        id: garde_du_code
        run: |
          printf 'print("piege du garde")\\n' > _piege_du_garde.py
          c=0; python3 -c "import sys; sys.path.insert(0, '.'); import _piege_du_garde" || c=$?
          rm -rf _piege_du_garde.py __pycache__/_piege_du_garde.*
          [ "$c" -eq 97 ] || { echo "::error::LE GARDE DU CODE NE MORD PAS (code $c au lieu de 97) — du code du depot prive pourrait tourner"; exit 1; }
          echo "garde du code : en place"
      - name: Le circuit public est-il celui que fabrique le depot prive ?
        id: circuit_a_jour
        continue-on-error: true
        run: |
          rm -rf "$RUNNER_TEMP/refait" && mkdir -p "$RUNNER_TEMP/refait"
          python3 programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py . "$RUNNER_TEMP/refait"
          cmp "$RUNNER_TEMP/refait/.github/workflows/circuit_du_soir.yml" "$RUNNER_TEMP/circuit_public/circuit_du_soir.yml" \
            || { echo "::error::LE CIRCUIT PUBLIC N EST PLUS CELUI DU DEPOT PRIVE — refabriquer et pousser"; exit 1; }
""" % DEPOT_PRIVE

JOURNAL = """      - name: Enregistrer le journal du passage au depot prive
        id: journal
        if: always()
        shell: bash
        run: |
          git rebase --abort 2>/dev/null || true
          git add rapports/journal_du_circuit/ || { echo "journal introuvable"; exit 1; }
          if git diff --cached --quiet; then echo "journal : rien a enregistrer"; exit 0; fi
          git -c user.name=circuit-public -c user.email=circuit-public@users.noreply.github.com commit -q -m "journal du circuit public, passage ${GITHUB_RUN_ID} [skip ci]"
          for i in 1 2 3; do
            if git pull -q --rebase --autostash origin main && git push -q; then echo "journal : enregistre"; exit 0; fi
            sleep 5
          done
          echo "journal : POUSSEE REFUSEE 3 FOIS"; exit 1
"""

DECISION_ENTETE = """  faut_il_tourner:
    runs-on: ubuntu-latest
    outputs:
      tourner: ${{ steps.decision.outputs.tourner }}
      rattrapage: ${{ steps.decision.outputs.rattrapage }}
""" + DEFAULTS + "    steps:\n"

DECISION_PAS = """      - name: Faut-il tourner ?
        id: decision
        run: |
          set +e
          python3 programmes/FAUT_IL_TOURNER.py . "${{ github.event_name }}" "${{ inputs.rattrapage }}"
          echo "code=$?" >> "$GITHUB_OUTPUT"
      - name: Rougir si la decision n a pas pu se prendre
        if: steps.decision.outputs.code != '0'
        run: |
          echo "::error::DECISION IMPOSSIBLE OU PAR PRECAUTION — voir le journal du passage au depot prive"
          exit 1
"""

JOB_PRIVE = "  collecte:\n"
JOB_CONDITION = """  collecte:
    needs: faut_il_tourner
    if: ${{ !cancelled() && needs.faut_il_tourner.outputs.tourner == 'true' }}
"""
RATTRAPAGE_PRIVE = "${{ inputs.rattrapage }}"
RATTRAPAGE_PUBLIC = "${{ needs.faut_il_tourner.outputs.rattrapage }}"

# LA NUIT DÉCOUPÉE EN TRANCHES (décision de Jean-Luc du 30-10-2026 à 19h02, réponse « 1 » : « Couper la nuit en plusieurs
# tâches qui tournent en même temps, chacune avec ses propres 6 heures, plus une tâche finale qui réunit les résultats et
# dit rouge s'il en manque un »). La nuit du 29 au 30-10-2026, la certification, d'un seul tenant, lancée à 01h30:33, a été
# coupée par sa limite de 330 minutes après 328 minutes d'épreuves relevées au journal (19 663 s), avant les épreuves de
# programmes/. Le NOMBRE de tranches est écrit ICI et nulle part ailleurs (R-708) : le circuit le passe sur la ligne de
# commande de programmes/CERTIFIER_LA_VERSION.py, qui répartit les épreuves par leurs durées relevées (`repartir`).
# Six : le plus petit nombre pour lequel la tranche la plus chargée tenait sous le TIERS de sa limite au 30-10-2026,
# les durées ayant varié du simple au double d'une nuit à l'autre ; en quatre et en cinq, non. Les charges ne sont pas
# recopiées ici (R-728 : ce qui se calcule ne s'écrit pas à la main) : `repartir` les calcule à chaque nuit, chaque
# certificat partiel les porte (« charges_prevues_secondes »), et tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py
# (N5) les recalcule et rougit quand une tranche dépasse ce tiers : il faut alors augmenter ce nombre.
TRANCHES_DE_LA_NUIT = 6
# LES ESSAIS DE POUSSÉE D'UNE TÂCHE DE LA CERTIFICATION : le nombre de tranches PLUS TROIS. Choix technique du Chat
# (31-10-2026), pas une décision de Jean-Luc. Sa raison est une loi, mesurée par le superviseur R-759 du 31-10-2026
# (simulation `sup_N/course.sh` : six clones poussent vers un même dépôt à la même seconde) : un essai d'une tranche ne
# peut échouer que si un AUTRE écrivain a réussi entre sa lecture et sa poussée ; une tranche échoue donc au plus
# (tranches − 1) + (poussées étrangères pendant la fenêtre) fois. Mesuré : 6 tranches, 6 essais à pas fixe → 6 partiels
# sur 6 à chaque passage ; 5 essais → 5 sur 6, trois fois sur trois ; 3 essais (le lot du 30-10) → 3 sur 6. Les trois de
# plus couvrent les autres écrivains du dépôt privé pendant la fenêtre (le circuit du soir retardé par GitHub, Cowork,
# le Chat) : leur nombre n'est pas mesuré. tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py rougit si le circuit
# fabriqué fait moins d'essais qu'il n'y a de tranches.
ESSAIS_DE_POUSSEE = TRANCHES_DE_LA_NUIT + 3

# LES PAS DU DÉBUT, LES MÊMES POUR CHAQUE TRANCHE ET POUR LA TÂCHE FINALE : les deux clonages, la pose du code public
# s'il est celui du dépôt privé, la vérification que ce circuit est celui que fabrique le dépôt privé, Python.
DEPART_DE_LA_CERTIFICATION = """      - uses: actions/checkout@v5
        with:
          repository: """ + DEPOT_PRIVE + """
          token: ${{ secrets.JETON_DEPOTS }}
          fetch-depth: 0
      - uses: actions/checkout@v5
        with:
          path: _code
      - name: Poser le code public, s'il est celui du depot prive
        id: poser_le_code
        shell: python3 _code/programmes/ETAPE_MUETTE.py {0}
        run: |
          D=""
          L=$(find . -name '*.py' -type l -print | head -5 | paste -sd ' ' -)
          [ -z "$L" ] || D="$D liens-symboliques:$L"
          for d in """ + BOUCLE_DU_CODE + """; do
            while IFS= read -r -d '' f; do
              n=${f##*/}
              if [ ! -f "$d/$n" ]; then D="$D $d/$n(absent-du-prive)"; elif ! cmp -s "$f" "$d/$n"; then D="$D $d/$n"; fi
            done < <(find "_code/$d" -maxdepth 1 -name '*.py' -type f -print0 2>/dev/null)
            while IFS= read -r -d '' f; do
              n=${f##*/}
              [ -f "_code/$d/$n" ] || D="$D $d/$n(absent-du-public)"
            done < <(find "$d" -maxdepth 1 -name '*.py' -type f -print0)
          done
          cmp -s _code/tests/LANCEMENT_DES_EPREUVES.json tests/LANCEMENT_DES_EPREUVES.json || D="$D tests/LANCEMENT_DES_EPREUVES.json"
          while IFS= read -r -d '' f; do
            n=${f##*/}
            if [ ! -f ".github/workflows/$n" ]; then D="$D fiche:$n(absent-du-prive)"; elif ! cmp -s "$f" ".github/workflows/$n"; then D="$D fiche:$n"; fi
          done < <(find _code/circuits_du_prive -maxdepth 1 \\( -name '*.yml' -o -name '*.yaml' \\) -type f -print0 2>/dev/null)
          while IFS= read -r -d '' f; do
            n=${f##*/}
            [ -f "_code/circuits_du_prive/$n" ] || D="$D fiche:$n(absent-du-public)"
          done < <(find .github/workflows -maxdepth 1 \\( -name '*.yml' -o -name '*.yaml' \\) -type f -print0)
          if [ -n "$D" ]; then echo "::error::CODE PUBLIC DIFFERENT DU DEPOT PRIVE :$D"; exit 1; fi
          find . -path ./_code -prune -o -path ./.git -prune -o -name __pycache__ -type d -prune -exec rm -rf {} +
          find . -path ./_code -prune -o -path ./.git -prune -o -name '*.py' -type f -print0 | grep -zvE '""" + MOTIF_DU_CODE + """' | xargs -0 -r rm -f
          X=$(python3 -c "import importlib.machinery as m; print('|'.join(s.replace('.', '[.]') for s in m.all_suffixes() if s != '.py'))")
          find . -path ./_code -prune -o -path ./.git -prune -o -type f -print0 | grep -zE "($X)$" | xargs -0 -r rm -f
          R=$(find . -path ./_code -prune -o -path ./.git -prune -o -name '*.py' -print | grep -cvE '""" + MOTIF_DU_CODE + """' || true)
          C=$(find . -path ./_code -prune -o -path ./.git -prune -o -type f -print | grep -cE "($X)$" || true)
          [ "$R" = "0" ] && [ "$C" = "0" ] || { echo "::error::CODE PRIVE NON PUBLIE ENCORE PRESENT : $R source(s), $C compile(s)"; exit 1; }
          for d in """ + BOUCLE_DU_CODE + """; do
            for f in _code/$d/*.py; do [ -e "$f" ] && cp "$f" "$d/"; done
          done
          cp _code/tests/LANCEMENT_DES_EPREUVES.json tests/
          mkdir -p "$RUNNER_TEMP/circuit_public"
          cp _code/.github/workflows/certifier_la_version.yml "$RUNNER_TEMP/circuit_public/"
          rm -rf _code
      - name: Le circuit de certification est-il celui que fabrique le depot prive ?
        id: circuit_a_jour
        run: |
          rm -rf "$RUNNER_TEMP/refait" && mkdir -p "$RUNNER_TEMP/refait"
          python3 programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py . "$RUNNER_TEMP/refait"
          cmp "$RUNNER_TEMP/refait/.github/workflows/certifier_la_version.yml" "$RUNNER_TEMP/circuit_public/certifier_la_version.yml" \\
            || { echo "::error::LE CIRCUIT DE CERTIFICATION N EST PLUS CELUI DU DEPOT PRIVE — refabriquer et pousser"; exit 1; }
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
"""

LOGICIELS_DE_LA_CERTIFICATION = """      # Les logiciels que les programmes cherchent par shutil.which : pdftotext (les PDF) et soffice
      # (les .doc). Absents de la machine de GitHub, ils ont fait rougir trois epreuves au premier
      # certificat public (16-10-2026, f5aac6b). continue-on-error : si l'installation tombe, la
      # certification tourne quand meme, et les epreuves qui en ont besoin rougissent en le disant.
      - name: Installer les logiciels que lisent les programmes
        id: logiciels
        continue-on-error: true
        run: |
          command -v pdftotext >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils; }
          command -v soffice >/dev/null || command -v libreoffice >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq --no-install-recommends libreoffice-writer-nogui; }
          pdftotext -v
          soffice --version || libreoffice --version
"""

# Les paquets que la certification installe : les mêmes que la certification privée (.github/workflows/certifier.yml).
# pyflakes : l'épreuve E12 des frais (A-550, 29-10-2026) cherche les noms lus jamais définis ; absent, elle rougit. Il
# manquait ici : E12 a rougi au certificat public du 31-10-2026 (7980a86, « pyflakes absent »), relecture de Cowork du
# 31-10-2026 à 18h49. L'épreuve E6 bis du circuit public rougit si un paquet du privé manque ici.
# numpy : le cas E7 de EPREUVES_DE_LA_LECTURE_DE_LA_FICHE éprouve des rangs numpy et rougit sans lui (R-734) ; il
# manquait, d'où le rouge du certificat du 08-11-2026 à 22h57 (82c92ace). 2.2.6 : la dernière version pour Python 3.11.
INSTALLER_LA_MESURE = """      - name: Installer la mesure et les dependances des programmes
        id: installer
        run: python3 -m pip install --quiet "coverage==7.16.2" "numpy==2.2.6" "pyflakes==4.1.0" cryptography pyyaml
"""

VERDICT_DE_LA_CERTIFICATION = """      - name: Rougir si la version n'est pas certifiee
        id: verdict
        if: ${{ !cancelled() && steps.poser_le_code.outcome == 'success' && steps.certifier.outcome != 'success' }}
        run: |
          echo "::error::VERSION NON CERTIFIEE — lire rapports/CERTIFICAT_DE_LA_VERSION.md au depot prive"
          exit 1
"""


def pas_de_depot(apres_echec, chemins, avant, auteur="certification-publique", message="certificat de la version",
                 reste="le certificat", branche=None, valeurs=()):
    """Rend le pas qui pousse au dépôt privé ce qu'une tâche de la certification a écrit.

    ① RÔLE — Écrire une fois le dépôt au privé (R-708), pour les tranches et pour la tâche finale.
    ② CONTEXTE D'APPEL — Le gabarit CERTIFICATION, deux fois ; le gabarit SERIES, deux fois (patch du 04-11-2026).
    ③ ENTRÉE — `apres_echec` : le message d'erreur si rien n'est à ajouter · `chemins` : les chemins à ajouter,
      séparés par une espace · `avant` : des lignes de commande jouées avant l'ajout (indentées de dix espaces) ·
      `auteur` : l'identité git du commit · `message` : le début du message du commit · `reste` : ce qui reste sur
      la machine si la poussée est refusée · `branche` : None (pousser sur main, avec les essais ci-dessous), ou le
      nom d'une branche À SOI du dépôt privé (une seule poussée, voir ⑥) · `valeurs` (tour 5, seulement avec
      `branche`) : des couples (NOM, expression de GitHub), posés dans le bloc « env: » du pas et vérifiés en tête du
      script ; `avant`, `chemins` et `branche` les lisent alors par « ${NOM} », jamais par « ${{ … }} ». Les valeurs
      par défaut sont celles de la certification : son texte fabriqué ne change pas d'un octet.
    ④ CONDITIONS D'ENTRÉE — Avec `branche` : `avant`, `chemins` et `branche` ne portent aucune expression « ${{ » (le
      filet des gabarits, propriété ⑩, refuse sinon le gabarit entier).
    ⑤ SORTIE — UNE valeur : le texte du pas, au format du fichier de circuit.
      [rend: 1]
    ⑥ TRAITEMENT — SANS `branche` (la certification) : identité `certification-publique` (programmes/MESSAGE_DU_SOIR.py
      la cherche dans l'historique), `avant`, ajout, commit, puis `ESSAIS_DE_POUSSEE` essais : chacun abandonne
      d'abord un rebasage resté en plan par l'essai précédent, reprend le dépôt et pousse ; après chaque essai
      refusé, le dernier compris, une attente tirée au hasard de 1 à 15 s (jusqu'à 15 s perdues avant le message
      d'erreur). AVEC `branche` (patch du 04-11-2026, superviseur R-759, R1 ; tour 5, superviseur R-759 du
      06-11-2026, §4 ①) : SANS_RIEN_DE_LA_VERSION ; chaque valeur de `valeurs` vérifiée (lettres, chiffres, « _ »,
      « - » : ni « : », qui ferait écrire une autre référence, ni « / » ni « .. ») ; `avant` ; les chemins de
      `chemins` qui existent recopiés comme de SIMPLES FICHIERS (tar) du dossier de travail vers le dossier neuf $T
      (aucun : message d'erreur) ; dans $T SEULEMENT : un dépôt git neuf, les exclusions du dépôt (tour 6 : le
      .gitignore du dossier de travail recopié dans .git/info/exclude de $T, refusé s'il est un lien symbolique),
      l'identité, l'ajout, un commit SANS PARENT
      (la branche ne porte que les résultats, pas la version), l'adresse du privé, AUTORISATION, l'aide aux
      identifiants écrite dans la configuration de $T, puis UNE poussée « HEAD:refs/heads/<branche> », sans reprise
      ni nouvel essai — une référence que nul autre n'écrit n'a pas de concurrent. JAMAIS « --force » (superviseur
      R-759 du 04-11-2026, tour 4, R1 ; MODE_EMPLOI_DEPOT.md : « jamais push --force », le seul geste qui puisse
      détruire le travail d'un autre) : une nouvelle tentative du MÊME job (« Re-run ») vise la même branche, déjà
      poussée, et sa poussée est REFUSÉE (mesuré : « [rejected] … (non-fast-forward) », code 1). Un passage rouge
      ne se relance donc pas : ménage des branches, puis nouveau passage (en-tête du circuit des séries). La forme
      de cette ligne est la SEULE que permet `verifier_les_gabarits_publics` : la changer ici, c'est la changer là.
    ⑦ UNITÉ — Des secondes (l'attente entre deux essais).
    ⑧ POURQUOI — Les tranches poussent leur certificat partiel au dépôt privé, où la tâche finale le lit : les
      archives jointes d'un passage public sont téléchargeables par tous (fiche du programme, ⑥ ③). AVEC `branche` :
      c'est le seul pas à jeton qui vient APRÈS du code de la version (il dépose ce que ce code a produit) ; ce code a
      pu écrire .git/config du dossier de travail (« core.fsmonitor », « filter.<x>.clean » : un programme que git
      lance, avec l'environnement du pas, donc le jeton ; mesuré par le superviseur R-759 du 06-11-2026, §4 ①, malgré
      « core.hooksPath=/dev/null ») : git ne tourne donc plus du tout dans ce dossier, et un fichier recopié par tar
      n'est que lu, jamais exécuté. Le commit sans parent remplace la recopie par « git fetch "$GITHUB_WORKSPACE" »
      du tour 3, qui lançait git dans le dossier de travail. LES EXCLUSIONS (tour 6, relecture neuve du tour 5, R5-1) :
      git ne tournant plus dans le dossier de travail, le .gitignore du dépôt ne s'appliquait plus, et un
      « __pycache__/*.pyc » laissé dans un « tmp_lot_NN » partait au privé (mesuré par le relecteur) ; le FICHIER est
      recopié, pas sa liste de motifs (deux implémentations d'une même chose divergent toujours, R-708). Un lien
      symbolique est refusé : git lirait alors, avec le jeton dans son environnement, le fichier que le lien vise,
      choisi par le code de la version (par exemple /proc/self/environ du pas, qui porte le jeton).
    ⑨ CE QUI CLOCHE — Les tranches qui finissent à la même seconde se disputent la poussée. Un essai d'une tranche ne
      peut échouer que si un autre écrivain a réussi entre sa lecture et sa poussée : une tranche échoue au plus
      (tranches − 1) + (poussées étrangères pendant la fenêtre) fois — c'est ce que couvre `ESSAIS_DE_POUSSEE`, et non
      le hasard. L'attente au hasard ne fait qu'accélérer : à pas fixe, les essais restent synchronisés et il n'y a
      qu'un gagnant par tour (mesuré par le superviseur R-759 du 31-10-2026). Plus de poussées étrangères que la marge
      pendant la fenêtre : une tranche peut encore échouer, et la réunion rougit (« certificat partiel absent »).
      L'abandon du rebasage dans la boucle n'a pas été vu servir : les fichiers des tranches sont distincts, aucun
      conflit n'a été observé (THÉORIQUE). La loi ne compte que les échecs dus à la concurrence : une erreur passagère
      du réseau ou de GitHub consomme aussi un essai. AVEC `branche` : un code ÉCRIT POUR NUIRE, qui a tourné avant ce
      pas dans le même job, peut encore lui prendre le jeton (BASH_ENV ou LD_PRELOAD par $GITHUB_ENV, un « bash » posé
      par $GITHUB_PATH, un processus laissé en fond, sudo) : hors du modèle de menace retenu le 05-11-2026 (l'accident),
      et sans réparation de fond dans un job où ce code a tourné (superviseur R-759 du 06-11-2026, §3) — décision de
      Jean-Luc en attente : (a) consigner, ou (b) une « boîte de dépôt » à jeton réduit. Un dépôt git imbriqué (un
      dossier « .git ») dans les résultats est recopié tel quel et ajouté comme tel par git : non éprouvé. Le refus du
      lien symbolique est un test puis une copie : un lien posé ENTRE les deux passerait (hors du modèle de l'accident).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      · AUTRE IDENTITÉ POUR TOUT AUTRE CIRCUIT (patch du 04-11-2026) : programmes/MESSAGE_DU_SOIR.py juge la
      certification sur le DERNIER commit d'auteur `certification-publique`, quel que soit le fichier ; un autre
      circuit qui signerait ainsi ferait passer son dépôt pour un certificat (la post-condition
      `verifier_les_gabarits_publics` l'interdit).
      · Le défaut M-a de la relecture du 04-11-2026 (après un conflit d'« autostash », les essais suivants échouent
      tous) reste dans la branche « main » de ce pas, celle de la certification : non réparé ici, à consigner.
      [sort: non]
    """
    if branche is None:
        return ("""      - name: Deposer au depot prive
        id: deposer
        if: always()
        shell: bash
        run: |
          git config user.name """ + auteur + """
          git config user.email """ + auteur + """@users.noreply.github.com
""" + avant + "          git add " + chemins + """ \\
            || { echo \"::error::""" + apres_echec + """\"; exit 1; }
          if git diff --cached --quiet; then echo "rien a deposer"; exit 0; fi
          git commit -q -m \"""" + message + """, passage public ${GITHUB_RUN_ID} [skip ci]"
          for i in $(seq 1 """ + str(ESSAIS_DE_POUSSEE) + """); do
            git rebase --abort 2>/dev/null || true
            if git pull -q --rebase --autostash origin main && git push -q; then echo "depose"; exit 0; fi
            sleep $((RANDOM % 15 + 1))
          done
          echo "::error::POUSSEE REFUSEE """ + str(ESSAIS_DE_POUSSEE) + """ FOIS — """ + reste + """ reste sur la machine jetable"; exit 1
""")
    # tour 5 : le jeton n'est lu que par AUTORISATION ; git ne tourne que dans le dossier neuf $T, où les résultats
    # arrivent comme de simples fichiers ; aucune expression de GitHub dans le script (les valeurs passent par env:)
    return ("""      - name: Deposer au depot prive
        id: deposer
        if: always()
        shell: bash
        env:
""" + JETON_DU_PAS + "".join("          " + nom + ": " + expression + "\n" for nom, expression in valeurs) + """        run: |
""" + SANS_RIEN_DE_LA_VERSION + "".join(
        """          [[ "$""" + nom + """" =~ ^[A-Za-z0-9_-]+$ ]] || { echo "::error::valeur refusee pour """ + nom
        + """ (lettres, chiffres, _ et - seulement)"; exit 1; }\n""" for nom, _ in valeurs) + avant + """          L=( )
          for c in """ + chemins + """; do if [ -e "$c" ]; then L+=( "$c" ); fi; done
          [ "${#L[@]}" -gt 0 ] || { echo "::error::""" + apres_echec + """"; exit 1; }
          tar -C "$GITHUB_WORKSPACE" -cf - -- "${L[@]}" | tar -C "$T" -xf - \\
            || { echo "::error::POUSSEE REFUSEE — """ + reste + """ reste sur la machine jetable (copie vers un dossier neuf)"; exit 1; }
          cd "$T" && git init -q . || { echo "::error::POUSSEE REFUSEE — dossier neuf impossible"; exit 1; }
          if [ -L "$GITHUB_WORKSPACE/.gitignore" ]; then echo "::error::POUSSEE REFUSEE — le .gitignore du depot est un lien symbolique"; exit 1; fi
          if [ -f "$GITHUB_WORKSPACE/.gitignore" ]; then mkdir -p .git/info && cp -- "$GITHUB_WORKSPACE/.gitignore" .git/info/exclude \\
            || { echo "::error::POUSSEE REFUSEE — exclusions du depot illisibles"; exit 1; }; fi
          git config user.name """ + auteur + """
          git config user.email """ + auteur + """@users.noreply.github.com
          git add -- "${L[@]}" || { echo "::error::""" + apres_echec + """"; exit 1; }
          if git diff --cached --quiet; then echo "rien a deposer"; exit 0; fi
          git commit -q -m \"""" + message + """, passage public ${GITHUB_RUN_ID} [skip ci]"
          git remote add origin "$PRIVE"
""" + AUTORISATION + """          git config --local credential.helper "$AIDE"
          git push -q origin "HEAD:refs/heads/""" + branche + """" \\
            || { echo "::error::POUSSEE REFUSEE — """ + reste + """ reste sur la machine jetable"; exit 1; }
          echo "depose sur sa branche"
""")


CERTIFICATION = """# CERTIFIER LA VERSION — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (décision de Jean-Luc du 12-10-2026 à
# 16h46, ordre confirmé le 15-10-2026 à 08h36). La certification rejoue toutes les épreuves et
# dit si la version du dépôt privé est certifiée. Elle n'exécute QUE le code de ce dépôt public :
# le pas « poser le code public » refuse de continuer si un seul fichier de programmes/ ou de
# tests/ diffère du dépôt privé ou n'existe que d'un côté. Les données des épreuves sont lues au
# dépôt privé, jamais publiées. Chaque pas passe par programmes/ETAPE_MUETTE.py : le journal
# public ne dit que « OK » ou « ÉCHEC » ; le détail est au dépôt privé.
# Depuis le 30-10-2026 (décision de Jean-Luc à 19h02) : les épreuves sont réparties en tranches
# jouées en même temps sur des machines distinctes (job « certifier »), puis une tâche finale
# (job « reunir ») réunit leurs certificats partiels et rougit s'il en manque un.
name: Certifier la version
on:
  workflow_dispatch:
  # 21h00 en heure universelle : 23h00 à Paris l'été, 22h00 l'hiver, après le circuit du soir
  # (dont des épreuves lisent les données). GitHub peut retarder un réveil de plusieurs heures.
  schedule:
    - cron: "0 21 * * 1-5"
concurrency:
  group: certifier-la-version
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  certifier:
    runs-on: ubuntu-latest
    # 330 minutes PAR TRANCHE : GitHub coupe toute tâche à 6 heures ; chaque tranche a les siennes.
    timeout-minutes: 330
    strategy:
      # une tranche rouge n'arrête pas les autres : la tâche finale doit voir chacune
      fail-fast: false
      matrix:
        tranche:
%(tranches)s%(defaults)s    steps:
%(depart)s%(logiciels)s%(installer)s      - name: Certifier une tranche
        id: certifier
        continue-on-error: true
        run: python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --tranche ${{ matrix.tranche }}/%(nombre)d
%(deposer_tranche)s%(verdict)s  reunir:
    # LA TÂCHE FINALE : après toutes les tranches, MÊME si l'une a échoué, a été coupée ou annulée.
    needs: certifier
    if: ${{ always() }}
    runs-on: ubuntu-latest
%(defaults)s    steps:
%(depart)s%(installer)s      - name: Reunir les tranches
        id: certifier
        continue-on-error: true
        run: python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --reunir %(nombre)d
%(deposer_final)s%(verdict)s""" % {
    # la matrice en liste « à tirets » : le sous-ensemble YAML que lit ce fabricant (SCALAIRE_DE_LISTE) refuse la liste
    # entre crochets, qui commence par un indicateur YAML ; c'est le producteur qui parle la langue du lecteur
    # (superviseur R-759 du 31-10-2026, B1, « DE FOND »)
    "tranches": "".join("          - %d\n" % i for i in range(1, TRANCHES_DE_LA_NUIT + 1)), "nombre": TRANCHES_DE_LA_NUIT,
    "defaults": DEFAULTS, "depart": DEPART_DE_LA_CERTIFICATION, "logiciels": LOGICIELS_DE_LA_CERTIFICATION,
    "installer": INSTALLER_LA_MESURE, "verdict": VERDICT_DE_LA_CERTIFICATION,
    # chaque tranche renomme son journal (ETAPE_MUETTE le nomme par le job, le même pour toutes) et pousse son partiel
    "deposer_tranche": pas_de_depot(
        "certificat partiel ou journal introuvable", "rapports/certificats_partiels/ rapports/journal_du_circuit/",
        "          mkdir -p rapports/certificats_partiels\n"
        "          for f in rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}.log; do\n"
        "            [ -f \"$f\" ] && mv \"$f\" \"${f%.log}_tranche_${{ matrix.tranche }}.log\"\n"
        "          done\n"),
    "deposer_final": pas_de_depot("certificat ou journal introuvable",
                                  "rapports/CERTIFICAT_DE_LA_VERSION.md rapports/journal_du_circuit/", "")}

# LE CIRCUIT DES SÉRIES LONGUES DE SABOTAGES, AU DÉPÔT PUBLIC (patch du 04-11-2026, tour 3 après l'avis du superviseur
# R-759 du 04-11-2026 à 19h59 ; à valider par Jean-Luc ; NON appliqué).
# Pourquoi au public : le quota gratuit des machines du dépôt privé est épuisé (A-543) ; décision de Jean-Luc du
# 08-10-2026, « atelier au privé, machines au public » : le public n'exécute que du code publié, les données sont lues au
# privé avec le secret JETON_DEPOTS. Ce circuit reprend les pas de la certification publique sans les recopier : mêmes
# pas de départ (`depart_pour`, tirés de DEPART_DE_LA_CERTIFICATION), même enrobage muet (DEFAULTS), mêmes paquets
# (INSTALLER_LA_MESURE), même pas de dépôt au privé (`pas_de_depot`), avec SA PROPRE identité et SES PROPRES BRANCHES.
# Le nombre de parts jouées en même temps : SOUS la limite des tâches simultanées d'un compte gratuit chez GitHub
# (« 20 total concurrent jobs », docs.github.com/en/actions/reference/limits, lue le 05-11-2026 par la relecture et le
# superviseur R-759). 16 et non 20 (superviseur R-759 du 05-11-2026, N3) : à 20, une série prend tout le quota, et un
# circuit du soir lancé pendant ce temps attend ; une séance non lue le jour même perd ses signaux pour toujours. La
# page ne dit pas si le total couvre le compte entier (dépôts privé et public) : je ne sais pas. Il ne règle que la
# matrice (« max-parallel ») : une part pousse UNE fois, sur une branche à elle.
# 10 ET NON PLUS 16 (superviseur R-759 du 15-11-2026, SUPERVISEUR_GHUB_Dim_15-11-2026.md, 2.6, étape GHUB ①) : la
# largeur simultanée des AUTRES circuits du dépôt public, lue dans leurs fiches par le superviseur, est 10 — le soir 1
# (« collecte » attend « faut_il_tourner », un seul groupe), la certification 6 tranches, le relais 1, la fiche du
# consensus 1, l'essai des archives 1. 16 + 6 + 1 = 23 dépassait déjà les 20 du compte : c'est le soir qui attendait
# dans la file. Mesure du gain gardé : les 28 lancements longs passent de 776 min un à un à 83,5 min sur 10 machines
# (le plancher, la lecture des cours `--saboter`, 5 007 s), comme sur 16. Le budget est la différence de deux nombres
# écrits UNE fois ici ; le calcul de la marge à partir des fiches elles-mêmes reste à faire (BACKLOG, étape GHUB ②).
TACHES_EN_MEME_TEMPS_DU_COMPTE = 20     # « 20 total concurrent jobs », offre gratuite, docs.github.com lu le 15-11-2026
MARGE_DES_AUTRES_CIRCUITS = 10          # largeur simultanée des autres fiches publiques, relevée le 15-11-2026
PARTS_EN_MEME_TEMPS = TACHES_EN_MEME_TEMPS_DU_COMPTE - MARGE_DES_AUTRES_CIRCUITS
SERIES_IDENTITE = "series-longues-publiques"
# LE GROUPE DE CONCURRENCE DES MACHINES LONGUES (étape GHUB ②, 15-11-2026) : le circuit des séries ET celui des
# épreuves longues portent CE groupe. GitHub ne fait tourner qu'un passage d'un groupe à la fois ; les deux circuits se
# partagent donc le même budget de PARTS_EN_MEME_TEMPS machines, et la marge des autres circuits reste entière.
GROUPE_DES_MACHINES_LONGUES = "series-longues"
# LES BRANCHES DES SÉRIES (superviseur R-759 du 04-11-2026, R1, « RUSTINE, À REPRENDRE » de l'archive jointe et de la
# garde d'horaire). Chaque job pousse UNE fois sur SA branche neuve du dépôt privé, jamais sur main :
#   series-longues/<passage>/<série>/part_<n>  (une part)   et   series-longues/<passage>/<série>/releve  (le relevé).
# Pourquoi : (1) une archive jointe d'un dépôt public est téléchargeable par tout compte GitHub connecté (documentation
# GitHub citée par le superviseur), or une part porte les écoutes (les chemins lus) et etat_du_depart.json (les noms de
# tous les fichiers du privé) ; (2) 20 parts qui poussaient sur main ont fait refuser 3 fois la collecte du soir, une
# fois sur trois (relecture du 04-11-2026, I1, course locale) ; une référence neuve n'a aucun concurrent : mesuré par
# le superviseur, 20 parts sur 20 et la collecte au premier essai, cinq fois sur cinq (course_branches.log), contre 1 à
# 2 parts sur 20 au premier essai sur main (course_contre_epreuve_main.log). Le préfixe ne commence JAMAIS par
# « travail- » : ce nom est réservé aux versions en attente que cherche le « check » (A-448, élargi par A-735).
# LE MÉNAGE : les branches restent au privé jusqu'à ce que le Chat ait lu le relevé et l'ait rangé dans tests/resultats/
# de la version éprouvée (sa branche « travail-… », ou main) ; il les supprime alors TOUTES. Tant qu'il en reste une, « preparer » refuse un nouveau passage : jamais plus
# d'un passage en attente, et un oubli se voit au lancement suivant.
# PAS DE RELANCE (superviseur R-759 du 04-11-2026, tour 4, R1 et R3) : la poussée est sans « --force », donc un passage
# rouge ne se relance pas (voir l'en-tête du circuit fabriqué, « PAS DE RELANCE ») ; ménage, puis nouveau passage.
SERIES_BRANCHES = "series-longues/"


def depart_pour(fiche, nom, ref=None, apres_le_clonage="", aussi=()):
    """Rend les pas de départ de la certification, adaptés à une autre fiche de circuit public.

    ① RÔLE — Donner au circuit des séries EXACTEMENT les pas de départ de la certification (clonage du privé avec
      JETON_DEPOTS, clonage du public, pose du code public s'il est celui du privé et effacement de tout autre code,
      contrôle que le circuit qui tourne est celui que fabrique le privé, Python), sans en recopier une ligne (R-708).
    ② CONTEXTE D'APPEL — Le gabarit SERIES, trois fois (une par job : « preparer » à la version demandée, les deux
      autres au commit de la préparation) ; « preparer » et « rassembler » y glissent leurs pas de lecture à jeton.
    ③ ENTRÉE — `aussi` (08-11-2026) : d'autres fichiers de circuit public, comparés eux aussi à ce que fabrique le
      privé (le relais demande_de_serie.yml, pour « preparer ») · `fiche` : le nom du fichier de circuit public (« series_longues.yml ») · `nom` : le circuit en
      minuscules, pour le nom du pas et le message (« des series longues ») · `ref` : None, ou la version à cloner
      au privé (une expression de GitHub : l'entrée « version », ou le commit de la préparation), ajoutée au clonage
      du privé sous « ref: » · `apres_le_clonage` (tour 5) : des pas, au format du fichier de circuit, placés JUSTE
      APRÈS le clonage du privé, avant le clonage du public et tout pas qui exécute du code de la version.
    ④ CONDITIONS D'ENTRÉE — DEPART_DE_LA_CERTIFICATION nomme sa fiche 3 fois, le circuit 2 fois (casse comprise),
      porte « fetch-depth: 0 » une fois (le clonage du privé) et le clonage du public (« path: _code ») une fois.
    ⑤ SORTIE — UNE valeur : le texte des pas. Lève ValueError si un ancrage n'a pas le compte attendu.
      [rend: 1]
    ⑥ TRAITEMENT — trois remplacements, quatre avec `ref`, cinq avec `apres_le_clonage` (inséré devant le clonage
      du public), chacun compté avant d'être fait.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le pas « poser le code » porte la loi d'A-600 (aucun code privé ne tourne au public) : une seconde
      rédaction finirait par diverger. DEPART_DE_LA_CERTIFICATION n'est pas modifié (élément validé) : il est LU.
      Avec `ref`, le clonage du privé porte aussi « persist-credentials: false » (superviseur R-759 du 05-11-2026,
      N1) : sans lui, actions/checkout laisse le jeton dans .git/config pendant tout le job, à portée du code de la
      version en attente, non validé ; seuls les pas qui lisent ou poussent au privé le reçoivent (JETON_DU_PAS).
      `ref` (tour 3, piste du superviseur R-759 du 04-11-2026) : les parts et le rassemblement jouent le commit FIGÉ
      de la préparation, quoi que reçoive main pendant le passage (collecte du soir, Chat, Cowork). « preparer »
      clone l'entrée « version » (décision de Jean-Luc du 05-11-2026 à 13h36, « 2 » : la version en attente
      s'éprouve AVANT sa fusion ; voir SERIES_VERSION) : le pas « poser le code » compare alors la branche publique
      lancée à cette version, et non à main. `apres_le_clonage` (tour 5, superviseur R-759 du 06-11-2026, §3) : le
      shell par défaut de chaque job est programmes/ETAPE_MUETTE.py, du code de la version ; un pas de lecture à jeton
      placé avant ce code ne peut rien lire que ce code ait écrit (fichiers de commandes de GitHub, .git/config).
    ⑨ CE QUI CLOCHE — Dépend du texte de DEPART_DE_LA_CERTIFICATION : s'il renomme sa fiche une quatrième fois ou change
      le nom de son pas, le fabricant lève à l'import (aucun circuit fabriqué) au lieu de produire un circuit faux.
      Que actions/checkout clone bien un commit donné par « ref: » avec « fetch-depth: 0 » n'est pas vu chez GitHub
      (documentation : « The branch, tag or SHA to checkout ») : le pas `meme_depot` le vérifie à chaque job.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    texte = DEPART_DE_LA_CERTIFICATION
    remplacements = [(os.path.basename(CIRCUIT_CERTIFICATION), fiche, 3),
                     ("Le circuit de certification", "Le circuit " + nom, 1),
                     ("LE CIRCUIT DE CERTIFICATION", "LE CIRCUIT " + nom.upper(), 1)]
    if ref is not None:
        remplacements.append(("          fetch-depth: 0\n", "          fetch-depth: 0\n          ref: " + ref + "\n"
                              "          persist-credentials: false\n", 1))
    for autre in aussi:   # 08-11-2026 (méthode du bloc 2, §5 R7) : un autre circuit fabriqué, comparé lui aussi
        remplacements.append(("          rm -rf _code\n", "          cp _code/.github/workflows/" + autre
                              + ' "$RUNNER_TEMP/circuit_public/"\n          rm -rf _code\n', 1))
        fin = ' N EST PLUS CELUI DU DEPOT PRIVE — refabriquer et pousser"; exit 1; }\n'
        remplacements.append((fin, fin + '          cmp "$RUNNER_TEMP/refait/.github/workflows/' + autre
                              + '" "$RUNNER_TEMP/circuit_public/' + autre + '" \\\n            || { echo "::error::LE CIRCUIT '
                              + autre + ' N EST PLUS CELUI DU DEPOT PRIVE — refabriquer et publier"; exit 1; }\n', 1))
    if apres_le_clonage:
        public = "      - uses: actions/checkout@v5\n        with:\n          path: _code\n"
        remplacements.append((public, apres_le_clonage + public, 1))
    for ancien, nouveau, fois in remplacements:
        if texte.count(ancien) != fois:
            raise ValueError(f"pas de départ de la certification : « {ancien} » trouvé {texte.count(ancien)} fois, "
                             f"{fois} attendu(s)")
        texte = texte.replace(ancien, nouveau)
    return texte


# LE JETON, PAS PAR PAS (superviseur R-759 du 05-11-2026, N1 : « Le jeton seulement dans les pas qui poussent ou lisent
# les parts »). Avec l'option 2 (05-11-2026), du code NON VALIDÉ tourne dans ce circuit (ETAPE_MUETTE de la version, ses
# parts, son rassembleur). Les clonages du privé ne gardent donc pas le jeton (`depart_pour`, « persist-credentials:
# false ») ; un pas qui lit ou pousse au privé le reçoit par son environnement (JETON_DU_PAS), tourne sous « bash »
# (jamais sous ETAPE_MUETTE, qui est du code de la version) et ne lance que des commandes du système : le filet des
# gabarits le vérifie (propriété ⑧). L'identification passe par une aide aux identifiants de git (AUTORISATION).
# LE MODÈLE DE MENACE (décision de Jean-Luc du 05-11-2026 à 17h36, ses mots : « on protège la clé, on ne veut pas que la
# clé soit visible à l'extérieur par rapport à des actes malveillants […] qui pourraient faire des modifications de nos
# programmes, des espionnages total du programme » ; lecture retenue, option 1 du superviseur R-759 du tour 3) :
# empêcher toute FUITE du jeton vers l'extérieur (journaux, dépôt public, branches, artefacts, relevés) par un défaut
# de NOTRE code. Un code écrit pour nuire, déjà dans le dépôt privé, est HORS de cette protection (BACKLOG) : il peut
# écrire $GITHUB_ENV ou $GITHUB_PATH pour les pas suivants, laisser un processus en fond qui lit /proc, ou se servir
# de sudo pour remplacer une commande du système.
# CONTRE L'ACCIDENT (superviseur R-759 du 05-11-2026, tour 3, M-3 : « Un pas qui tient le jeton ne lit rien que le
# code de la version a pu écrire ») : chaque pas à jeton commence par SANS_RIEN_DE_LA_VERSION — PATH fixe (une commande
# posée par une épreuve dans un dossier du PATH n'est pas prise), ni configuration git du système ni globale, l'adresse
# du privé écrite ici (jamais lue dans .git/config du dossier de travail), et un dossier NEUF pris hors du dépôt joué
# (`mktemp`), où se font les lectures et la poussée : les crochets git qu'une épreuve pose dans .git/hooks du dépôt
# cloné (les épreuves du circuit en posent elles-mêmes) ne sont pas dans ce dossier. Mesuré par la relecture du tour 2
# (M-3) : sans cela, des crochets posés au pas 1 ont vu le jeton (fictif) aux pas 2 et 3.
# TOUR 5 (superviseur R-759 du 06-11-2026, après la relecture de Cowork de 12h59) : ① les pas de LECTURE à jeton
# (« version », « rien_en_attente » — retirée le 08-11-2026 —, « lire_les_parts ») tournent juste après le clonage du privé, AVANT tout pas qui
# exécute du code de la version (`depart_pour`, `apres_le_clonage`) : ce code n'a encore rien pu écrire, ni dans
# .git/config du dossier de travail, ni dans les fichiers de commandes de GitHub ; le filet le vérifie (propriété ⑨) ;
# ② la poussée, seul pas à jeton qui vient après ce code (elle dépose ce qu'il a produit), recopie les résultats comme
# de SIMPLES FICHIERS (tar) dans le dossier neuf et n'y lance git que là : plus aucun git dans le dossier de travail,
# dont le .git/config a pu recevoir « core.fsmonitor » ou « filter.<x>.clean » (mesuré par le superviseur : le jeton
# fictif vu 6 fois et 2 fois, malgré « core.hooksPath=/dev/null ») ; ③ aucune expression « ${{ … }} » dans le script
# d'un pas à jeton (propriété ⑩) : GitHub la remplace AVANT bash, et une valeur de la matrice vient d'un pas qui a
# exécuté du code de la version ; les valeurs passent par « env: » et sont vérifiées par une expression régulière.
# « GIT_TRACE_REDACT=1 » : git caviarde l'en-tête « Authorization » de ses traces HTTP (GIT_TRACE_CURL,
# GIT_CURL_VERBOSE) ; posé à 0 au circuit, il les écrit en clair (mesuré le 06-11-2026 par l'auteur du tour 5, serveur
# local qui exige une identification : le base64 du jeton fictif écrit 2 fois sous GIT_TRACE_CURL).
JETON_DU_PAS = "          JETON: ${{ secrets.JETON_DEPOTS }}\n"
DEPOT_PRIVE_ADRESSE = "https://github.com/" + DEPOT_PRIVE + ".git"
SANS_RIEN_DE_LA_VERSION = ("          export PATH=/usr/bin:/bin GIT_TRACE_REDACT=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null\n"
                           "          PRIVE=" + DEPOT_PRIVE_ADRESSE + "\n"
                           "          T=$(mktemp -d)\n")
# L'IDENTIFICATION, SEULE LECTURE DU JETON DANS UN PAS (superviseur R-759 du 05-11-2026, tour 4, M-a : « $JETON n'est lu
# qu'à un seul endroit » ; tour 5, superviseur R-759 du 06-11-2026, §2 : « plus de base64 du tout »). Le journal d'un
# circuit du dépôt public est public. Jusqu'au tour 4, ce texte CALCULAIT le base64 de « x-access-token:<jeton> » dans
# une variable du shell, puis le déclarait masqué (« ::add-mask:: », masquage de GitHub THÉORIQUE) : une trace rallumée
# (« set -x »), un « echo » de mise au point ou GIT_TRACE écrivaient alors cette valeur au journal (relecture de Cowork
# du 06-11-2026, D2 et D3 ; le superviseur l'a mesuré aussi sous GIT_TRACE2). Désormais AUCUNE valeur tirée du jeton
# n'existe dans le shell : AIDE est le TEXTE d'une aide aux identifiants de git (« credential.helper »), entre
# apostrophes, où « $JETON » reste écrit tel quel ; git lance cette aide au moment où le serveur demande une
# identification, et c'est l'aide, un petit shell à part, qui lit $JETON et le donne à git par un tube. « A=(…) »
# l'emploie pour une commande (lecture) ; la poussée l'écrit dans la configuration du dossier neuf (`pas_de_depot`),
# car la seule forme de poussée permise par le filet n'a pas de « -c ». Une trace ou un « echo » n'écrivent que le
# texte « $JETON », jamais sa valeur. « credential.helper= » vide d'abord la liste des aides. Mesuré le 06-11-2026
# (superviseur, puis auteur du tour 5) contre un serveur local qui exige une identification, sous GIT_TRACE,
# GIT_TRACE2, GIT_TRACE_CURL, GIT_CURL_VERBOSE, GIT_TRACE_PACKET et « set -x » : 0 occurrence du jeton fictif ni de son
# base64. Que github.com accepte cette forme : THÉORIQUE (c'est la manière ordinaire d'identifier git). Le filet ⑧
# refuse tout pas à jeton qui nomme JETON hors d'une copie mot pour mot de ce texte.
AUTORISATION = ("          AIDE='!f() { echo username=x-access-token; echo \"password=$JETON\"; }; f'\n"
                "          A=(-c credential.helper= -c \"credential.helper=$AIDE\")\n")

# Le commit que jouent les parts et le rassemblement : celui de la préparation (clonage à « ref: », `depart_pour`). Ce
# pas vérifie que le clonage l'a bien posé : sinon les parts ne joueraient pas la même version (le rassemblement s'en
# apercevrait par les empreintes du départ, mais plus tard et moins clairement). Depuis le tour 3 il compare HEAD au
# commit, sans exclusion : plus rien de ce circuit n'est poussé sur main.
SERIES_MEME_DEPOT = """      - name: Le depot prive est-il celui de la preparation ?
        id: meme_depot
        env:
          SHA: ${{ needs.preparer.outputs.sha }}
        run: |
          [ "$(git rev-parse HEAD)" = "$SHA" ] || { echo "::error::LE COMMIT CLONE N EST PAS CELUI DE LA PREPARATION"; exit 1; }
"""

# LA VERSION ÉPROUVÉE, VÉRIFIÉE AVANT TOUT (décision de Jean-Luc du 05-11-2026 à 13h36, « 2 » : les séries tournent sur
# GitHub AVANT la fusion ; la question, les options et la raison sont dans l'en-tête du gabarit SERIES). Le pas de
# « preparer » placé juste après le clonage du privé (tour 5 : avant tout code de la version, `depart_pour`). Trois
# propriétés, chacune avec sa raison :
#   ① la version demandée est « main » ou un nom « travail-… » sans « / » ni espace, et c'est le nom de la branche
#     publique LANCÉE (github.ref_name) : le code exécuté est celui de cette branche publique, que le pas « poser le
#     code » compare au clone du privé ; une version demandée depuis une autre branche publique ferait comparer deux
#     versions différentes (refus certain, mais pour une raison obscure) ou, pire, deux versions qui coïncident par
#     hasard sous deux noms ;
#   ② (A-811, décision de Jean-Luc du 15-11-2026 à 14h18, « 1 mais tu le note en autoportant maximum ») la branche
#     EXISTE au dépôt privé, et la POINTE DONNÉE par la demande (entrée « pointe », 40 caractères hexadécimaux) est
#     EXACTEMENT sa pointe actuelle ; pour main, une pointe vide vaut « la pointe actuelle ». Elle remplace l'ancienne
#     ② (« la SEULE branche travail-… du dépôt privé », A-448) : depuis A-735 (12-11-2026) Cowork relit plusieurs
#     versions à la fois, il y en avait 18 le 15-11-2026, et l'ancienne ② ne laissait passer que main ; elle écrivait
#     de plus au journal PUBLIC les noms des branches du privé (superviseur R-759 du 15-11-2026, 2.1). Pourquoi la
#     pointe exacte : on éprouve ce qui sera installé, pas une version plus ancienne ni une autre ; si la branche
#     avance entre la demande et ce pas (un RELU.md déposé par Cowork), le passage est refusé et l'on redépose ;
#   ③ le clone du privé est la POINTE actuelle de cette branche au dépôt privé : le sha noté ensuite par « Fabriquer la
#     matrice », que clonent les parts, est donc celui de la version demandée.
# Les valeurs viennent de l'environnement du pas, jamais recopiées dans le script : une entrée « inputs. » écrite en
# clair dans un script de shell y serait exécutée. Les messages d'erreur ne nomment que des valeurs déjà validées par
# motif (version, pointe), jamais une branche lue au privé.
# La forme d'une version : la version officielle ou la version en attente (A-448). Écrite UNE fois, lue par la porte du
# circuit des séries (SERIES_VERSION) et par le relais (RELAIS) : deux écritures d'une même chose divergent (R-708).
MOTIF_DE_VERSION = "^(main|travail-[A-Za-z0-9._-]+)$"
# La forme d'une pointe : un commit écrit en entier (A-811). Écrite UNE fois, lue par la porte (SERIES_VERSION) et par
# le relais (RELAIS), qui la valide par CE motif et non par celui des autres valeurs (au plus 20 caractères).
MOTIF_DE_POINTE = "^[0-9a-f]{40}$"
SERIES_VERSION = """      - name: La version demandee est-elle celle de cette branche publique ?
        id: version
        shell: bash
        env:
""" + JETON_DU_PAS + """          VERSION: ${{ inputs.version }}
          POINTE: ${{ inputs.pointe }}
          BRANCHE_PUBLIQUE: ${{ github.ref_name }}
        run: |
          set -o pipefail
""" + SANS_RIEN_DE_LA_VERSION + AUTORISATION + """          cd "$T"
          [[ "$VERSION" =~ """ + MOTIF_DE_VERSION + """ ]] || { echo "::error::version refusee : ${#VERSION} caractere(s), hors de la forme permise (main, ou une version en attente travail-...)"; exit 1; }
          [ "$VERSION" = "$BRANCHE_PUBLIQUE" ] || { echo "::error::la version $VERSION n'est pas la branche publique lancee ($BRANCHE_PUBLIQUE) : lancer ce circuit depuis la branche publique $VERSION"; exit 1; }
          if [ "$VERSION" != "main" ] || [ -n "$POINTE" ]; then
            [[ "$POINTE" =~ """ + MOTIF_DE_POINTE + """ ]] || { echo "::error::pointe refusee : une version en attente se demande avec sa pointe, 40 caracteres hexadecimaux (A-811)"; exit 1; }
          fi
          tetes=$(git "${A[@]}" ls-remote --heads "$PRIVE") || { echo "::error::branches du depot prive illisibles"; exit 1; }
          pointe=$(printf '%s\\n' "$tetes" | awk -v r="refs/heads/$VERSION" '$2 == r { print $1 }')
          [ -n "$pointe" ] || { echo "::error::la version $VERSION n'existe pas au depot prive"; exit 1; }
          [ -z "$POINTE" ] || [ "$POINTE" = "$pointe" ] || { echo "::error::la pointe demandee $POINTE n'est pas la pointe actuelle de $VERSION au depot prive : redeposer la demande avec la pointe actuelle"; exit 1; }
          [ -n "$pointe" ] && [ "$(git -C "$GITHUB_WORKSPACE" -c core.hooksPath=/dev/null rev-parse HEAD)" = "$pointe" ] || { echo "::error::le clone du depot prive n'est pas la pointe de $VERSION"; exit 1; }
"""

# La copie jouée : sans .git (comme la machine du Chat), sans les journaux et les dépôts de ce circuit (ils changent
# d'un job à l'autre : les empreintes du départ différeraient), sans les programmes interdits (ainsi ils ne peuvent pas
# être lancés, même en « -I », que l'écoute ne voit pas : relecture du 04-11-2026, D4). Leur liste est lue dans
# tests/outils/jouer_une_part.py (INTERDITS), jamais épelée ici.
SERIES_COPIE = """      - name: Copie jouee, sans .git, sans journaux ni depots de ce circuit, sans programmes interdits
        id: copie
        run: |
          set -o pipefail
          X=(--exclude=./.git --exclude=./rapports/journal_du_circuit --exclude=./rapports/series_longues)
          while IFS= read -r n; do [ -z "$n" ] || X+=("--exclude=$n"); done < <(python3 -B tests/outils/jouer_une_part.py --interdits)
          [ "${#X[@]}" -gt 3 ] || { echo "::error::liste des programmes interdits vide ou illisible"; exit 1; }
          rm -rf "$RUNNER_TEMP/depot" && mkdir -p "$RUNNER_TEMP/depot"
          tar -C "$GITHUB_WORKSPACE" "${X[@]}" -cf - . | tar -C "$RUNNER_TEMP/depot" -xf -
"""

# Couper le réseau des programmes de la version : jouer une part, et rassembler (superviseur R-759 du 05-11-2026, N1 :
# « unshare -rn au rassemblement »). Écrit une fois, posé dans les deux jobs (R-708).
SERIES_RESEAU = """      - name: Couper le reseau des epreuves
        id: reseau
        run: |
          sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 || true
          # Propriété vérifiée : dans l'espace isolé, /proc/net/dev ne compte qu'une interface, « lo » (calibré le
          # 04-11-2026 sur la machine du Chat : 4 hors de l'espace, 1 dedans).
          n=$(unshare -rn cat /proc/net/dev | tail -n +3 | wc -l)
          [ "$n" = "1" ] || { echo "::error::le reseau n'est pas coupe ($n interfaces)"; exit 1; }
"""

# LES PAS DE LECTURE À JETON, JUSTE APRÈS LE CLONAGE DU PRIVÉ (tour 5, superviseur R-759 du 06-11-2026, §3 : « dans un
# job, aucun pas à jeton ne vient après un pas qui exécute du code de la version, sauf la poussée finale ») ; posés par
# `depart_pour(…, apres_le_clonage=…)`. Ils n'emploient que bash, git et des dossiers neufs ou vides.
# LA GARDE « rien_en_attente » EST RETIRÉE (relevé du Chat n°347, Q4 = 3 : option « retirer la garde
# rien_en_attente », choisie par le Chat le 08-11-2026 sous la délégation de Jean-Luc ; ces mots sont ceux de l'option,
# pas ceux de Jean-Luc) : elle refusait un passage tant qu'une branche series-longues/* restait au
# privé, et la session du Chat ne peut supprimer aucune branche (n°331, trois voies essayées, refusées) ; le second
# passage aurait donc toujours été refusé. Elle n'était pas nécessaire à la sécurité : chaque nom de branche porte le
# numéro du passage, deux passages ne se touchent pas. Son texte reste dans l'historique du dépôt (commit 791d317d).
# La garde des parts vient AVANT la lecture des parts (rien n'est lu si une part n'est pas verte) : sous « bash » et
# sans programme de la version, elle peut précéder le clonage du public ; elle lit « needs.jouer.result » (propriété ⑤
# du filet des gabarits).
SERIES_PARTS_VERTES = """      - name: Toutes les parts sont-elles vertes ?
        id: parts_vertes
        shell: bash
        env:
          JOUER: ${{ needs.jouer.result }}
        run: |
          [ "$JOUER" = "success" ] || { echo "::error::une part au moins n'est pas verte ($JOUER) : rien n'est rassemble, aucun releve"; exit 1; }
"""
SERIES_LIRE_LES_PARTS = """      - name: Lire les parts sur leurs branches
        id: lire_les_parts
        shell: bash
        env:
""" + JETON_DU_PAS + """          SERIE: ${{ matrix.serie }}
        run: |
          set -o pipefail
""" + SANS_RIEN_DE_LA_VERSION + AUTORISATION + """          [[ "$SERIE" =~ ^[A-Za-z0-9_-]+$ ]] || { echo "::error::valeur refusee pour SERIE (lettres, chiffres, _ et - seulement)"; exit 1; }
          B=\"""" + SERIES_BRANCHES + """$GITHUB_RUN_ID/$SERIE"
          rm -rf "$RUNNER_TEMP/parts" && mkdir -p "$RUNNER_TEMP/parts"
          cd "$T" && git init -q . || { echo "::error::dossier neuf impossible"; exit 1; }
          git "${A[@]}" fetch -q --no-tags "$PRIVE" "+refs/heads/$B/*:refs/series_lues/$SERIE/*" || { echo "::error::branches des parts illisibles"; exit 1; }
          n=0
          while IFS= read -r r; do
            p=${r##*/}
            mkdir -p "$RUNNER_TEMP/parts/$p"
            git archive "$r" "rapports/series_longues/$GITHUB_RUN_ID/$SERIE/$p" | tar -x -C "$RUNNER_TEMP/parts/$p"
            n=$((n + 1))
          done < <(git for-each-ref --format='%(refname)' "refs/series_lues/$SERIE/part_*")
          [ "$n" -gt 0 ] || { echo "::error::aucune branche de part pour $B"; exit 1; }
          echo "$n part(s) lue(s)"
"""

# LA TABLE DES SÉRIES DU CIRCUIT (décision de Jean-Luc n°309 du 07-11-2026, « 1 » : « une seule table qui dit, pour
# chaque série, quelle épreuve jouer et avec quels réglages ; tout le circuit est fabriqué depuis cette table »). Elle
# vit dans tests/LANCEMENT_DES_EPREUVES.json (LANCEMENT) : une entrée de « series_hors_de_la_nuit » qui porte
# « serie_du_circuit » est une série du circuit. Avant le 08-11-2026, le lien série → épreuve était tapé deux fois à la
# main dans le pas « Fabriquer la matrice » (motif "HISTORIQUE_LONG" / "COURS_PROPRE_DE_YAHOO", défaut NV-1 : une
# demande « HL » pouvait jouer l'épreuve Yahoo sans qu'aucune épreuve ne rougisse, relevé n°298).
TOUTES = "toutes"                   # le choix du bouton et d'une demande qui joue chaque série de la table
CODE_DE_SERIE = r"[A-Za-z][A-Za-z0-9]{0,19}"
SERIES_AU_PLUS = 4                  # 3 + 2 × 4 = 11 entrées du bouton (version, pointe, serie, puis parts et lot par
                                    # série) : la limite de GitHub est 25 depuis le 04-12-2025 (« You can now use up to
                                    # 25 inputs », github.blog/changelog, lu le 15-11-2026 ; le 05-11-2026 on avait lu 10)


def series_du_circuit(racine=None):
    """Rend les séries du circuit lues dans la table : [(code, épreuve, machines, lot), …], dans l'ordre de la table.

    ① RÔLE — Lire UNE fois la table des séries, pour que le bouton du circuit des séries, sa matrice et le relais des
      demandes en soient fabriqués (décision n°309).
    ② CONTEXTE D'APPEL — Le haut de ce programme, une fois, pour SERIES_DU_CIRCUIT (lu par les gabarits SERIES et
      RELAIS) ; l'épreuve tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py, pour sa table de référence.
    ③ ENTRÉE — `racine` : la racine du dépôt ; None = le dossier parent de celui de ce programme.
    ④ CONDITIONS D'ENTRÉE — `racine`/tests/LANCEMENT_DES_EPREUVES.json existe et se lit en UTF-8.
    ⑤ SORTIE — UNE valeur : la liste des quadruplets (code : texte ; épreuve : chemin relatif ; machines, lot :
      entiers). Lève ValueError si la table ne convient pas.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque entrée de « series_hors_de_la_nuit » qui porte « serie_du_circuit » : le chemin de
      l'épreuve a la forme tests/<lettres, chiffres, « _ . - »>.py ; le code répond à CODE_DE_SERIE et n'est pas
      TOUTES ; machines et lot sont des entiers (pas des booléens) de 1 à 99 ; deux codes ne se ressemblent pas à la
      casse près (les entrées du bouton sont nommées en minuscules, les variables en majuscules) ; au moins une série,
      au plus SERIES_AU_PLUS.
    ⑦ UNITÉ — machines : des machines de GitHub ; lot : des sabotages par lot.
    ⑧ POURQUOI — Décision n°309 ; un réglage écrit à deux endroits finit par différer (R-708). Les formes sont
      vérifiées ICI parce que les valeurs deviennent du texte du circuit (noms d'entrées, de variables, choix du
      bouton) : un code avec une espace ou un guillemet casserait le fichier fabriqué.
    ⑨ CE QUI CLOCHE — La limite de 10 entrées du bouton est celle lue dans la documentation de GitHub le 05-11-2026
      (relevé du 05-11-2026), pas mesurée par un passage. L'existence du fichier de l'épreuve n'est pas vérifiée ici :
      le pas « Fabriquer la matrice » la vérifie sur la version jouée.
    ⑩ EFFET — Lit la table.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    racine = racine or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    with open(os.path.join(racine, LANCEMENT), encoding="utf-8") as f:
        table = json.load(f)
    series, vus = [], set()
    for epreuve, e in (table.get("series_hors_de_la_nuit") or {}).items():
        s = e.get("serie_du_circuit") if isinstance(e, dict) else None
        if s is None:
            continue
        if not isinstance(s, dict) or not re.fullmatch(r"tests/[A-Za-z0-9_.-]+\.py", epreuve):
            raise ValueError(f"série du circuit illisible pour {epreuve!r}")
        code, machines, lot = s.get("code"), s.get("machines"), s.get("lot")
        if not isinstance(code, str) or not re.fullmatch(CODE_DE_SERIE, code) or code.lower() == TOUTES:
            raise ValueError(f"code de série refusé pour {epreuve} : {code!r}")
        for nom, v in (("machines", machines), ("lot", lot)):
            if not isinstance(v, int) or isinstance(v, bool) or not 1 <= v <= 99:
                raise ValueError(f"{nom} refusé pour la série {code} : {v!r} (entier de 1 à 99)")
        if code.lower() in vus:
            raise ValueError(f"code de série en double (à la casse près) : {code}")
        vus.add(code.lower())
        series.append((code, epreuve, machines, lot))
    if not 1 <= len(series) <= SERIES_AU_PLUS:
        raise ValueError(f"{len(series)} série(s) du circuit dans la table (1 à {SERIES_AU_PLUS})")
    return series


# Une table illisible n'empêche pas d'IMPORTER ce programme (tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py en lit
# FICHIERS_DE_COMMANDES_DE_GITHUB, sur des dépôts d'essai sans séries) : SERIES et RELAIS valent alors None, et `main`
# refuse de fabriquer (ERREUR_DE_LA_TABLE).
try:
    SERIES_DU_CIRCUIT, ERREUR_DE_LA_TABLE = series_du_circuit(), None
except (OSError, ValueError) as _e:
    SERIES_DU_CIRCUIT, ERREUR_DE_LA_TABLE = [], f"{type(_e).__name__} : {_e}"


# LA TABLE DES ÉPREUVES LONGUES D'UN TENANT (étape GHUB ②, 15-11-2026). Elle vit dans tests/LANCEMENT_DES_EPREUVES.json,
# clé « epreuves_longues » : code → {« chemin », « arguments », « pourquoi »}. Une demande ne porte QUE des codes ; la
# commande jouée est celle de la table de la version éprouvée, jamais un argument venu de la demande. La forme d'un
# code est celle d'un code de série (CODE_DE_SERIE) : elle devient du texte du circuit et du relais.
EPREUVES_AU_PLUS = 64                 # codes au plus dans la table : une demande « toutes » reste sous 1 000 octets
# Un argument figé : la racine de la copie jouée, ou un mot sans espace, sans guillemet ni caractère du shell.
ARGUMENT_FIGE = r"\{copie\}|[A-Za-z0-9_.=,-]{1,40}"


def epreuves_du_circuit(racine=None):
    """Rend les épreuves longues de la table : [(code, chemin, arguments), …], dans l'ordre de la table.

    ① RÔLE — Lire UNE fois la table des épreuves longues d'un tenant, pour que le circuit des épreuves, son pas
      « Fabriquer la matrice », le relais et le joueur d'une épreuve en soient tous tirés (R-708).
    ② CONTEXTE D'APPEL — Le haut de ce programme, une fois, pour EPREUVES_DU_CIRCUIT (lu par les gabarits EPREUVES et
      RELAIS) ; tests/outils/jouer_une_epreuve_longue.py, sur la copie jouée (la table de la version éprouvée) ;
      l'épreuve tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py.
    ③ ENTRÉE — `racine` : la racine du dépôt ; None = le dossier parent de celui de ce programme.
    ④ CONDITIONS D'ENTRÉE — `racine`/tests/LANCEMENT_DES_EPREUVES.json existe et se lit en UTF-8. La clé
      « epreuves_longues » est facultative (absente : aucune épreuve, liste vide).
    ⑤ SORTIE — UNE valeur : la liste des triplets (code : texte ; chemin : chemin relatif ; arguments : liste de
      textes). Lève ValueError si la table ne convient pas, en nommant le code fautif.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque entrée : le code répond à CODE_DE_SERIE et n'est pas TOUTES ; deux codes ne se
      ressemblent pas à la casse près ; le chemin a la forme tests/<nom>.py ou programmes/<nom>.py (lettres, chiffres,
      « _ . - ») ; « arguments » est une liste non vide de textes qui répondent chacun à ARGUMENT_FIGE et contient
      « {copie} » ; « pourquoi » est un texte non vide ; une épreuve de « series_hors_de_la_nuit » n'est pas admise
      avec « --saboter » (sa série a son propre circuit, et son « --saboter » joue la série entière : des heures) ;
      au plus EPREUVES_AU_PLUS entrées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Point 1 de l'étape GHUB ② (« chaque code renvoie, dans la table, à une commande FIGÉE : aucun
      argument libre ne vient de la demande ») ; les formes sont vérifiées ICI parce que les codes deviennent du texte
      du circuit (noms de jobs, motifs du relais) et les arguments une ligne de commande.
    ⑨ CE QUI CLOCHE — L'existence du fichier n'est pas vérifiée ici (une table de main peut nommer une épreuve d'une
      version en attente) : le joueur la vérifie sur la version jouée, le pas « Fabriquer la matrice » aussi. Qu'une
      épreuve ne nomme pas un programme interdit est vérifié par le joueur (tests/outils/jouer_une_epreuve_longue.py),
      qui connaît INTERDITS, pas ici.
    ⑩ EFFET — Lit la table.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    racine = racine or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    with open(os.path.join(racine, LANCEMENT), encoding="utf-8") as f:
        table = json.load(f)
    entrees = table.get("epreuves_longues")
    if entrees is None:
        return []
    if not isinstance(entrees, dict):
        raise ValueError("« epreuves_longues » n'est pas une table code → épreuve")
    series = table.get("series_hors_de_la_nuit") or {}
    rendu, vus = [], set()
    for code, e in entrees.items():
        if not re.fullmatch(CODE_DE_SERIE, code) or code.lower() == TOUTES:
            raise ValueError(f"code d'épreuve longue refusé : {code!r}")
        if code.lower() in vus:
            raise ValueError(f"code d'épreuve longue en double (à la casse près) : {code}")
        vus.add(code.lower())
        if not isinstance(e, dict):
            raise ValueError(f"épreuve longue {code} : entrée illisible")
        chemin, arguments, pourquoi = e.get("chemin"), e.get("arguments"), e.get("pourquoi")
        if not isinstance(chemin, str) or not re.fullmatch(r"(?:tests|programmes)/[A-Za-z0-9_.-]+\.py", chemin):
            raise ValueError(f"épreuve longue {code} : chemin refusé {chemin!r} (tests/<nom>.py ou programmes/<nom>.py)")
        if (not isinstance(arguments, list) or not arguments or "{copie}" not in arguments
                or not all(isinstance(a, str) and re.fullmatch(ARGUMENT_FIGE, a) for a in arguments)):
            raise ValueError(f"épreuve longue {code} : arguments refusés {arguments!r} (liste de mots figés, "
                             "« {copie} » compris)")
        if not isinstance(pourquoi, str) or not pourquoi.strip():
            raise ValueError(f"épreuve longue {code} : « pourquoi » manque")
        if chemin in series and "--saboter" in arguments:
            raise ValueError(f"épreuve longue {code} : {chemin} --saboter est une série de sabotages, qui a son "
                             "propre circuit (series_longues.yml)")
        rendu.append((code, chemin, list(arguments)))
    if len(rendu) > EPREUVES_AU_PLUS:
        raise ValueError(f"{len(rendu)} épreuves longues dans la table (au plus {EPREUVES_AU_PLUS})")
    return rendu


try:
    EPREUVES_DU_CIRCUIT = epreuves_du_circuit()
except (OSError, ValueError) as _e:
    EPREUVES_DU_CIRCUIT = []
    ERREUR_DE_LA_TABLE = ERREUR_DE_LA_TABLE or f"{type(_e).__name__} : {_e}"
# Les morceaux du circuit des séries tirés de la table (une boucle chacun, sur la même liste) :
# les entrées du bouton, et l'environnement du pas « Fabriquer la matrice ».
SERIES_ENTREES = ("""      serie:
        description: "Serie a jouer (""" + TOUTES + """ : chaque serie de la table)"
        required: true
        type: choice
        options: [""" + ", ".join('"%s"' % c for c in [TOUTES] + [s[0] for s in SERIES_DU_CIRCUIT]) + """]
        default: \"""" + TOUTES + """\"
""" + "".join("""      parts_%s:
        description: "Nombre de machines pour la serie %s (1 a 99)"
        type: number
        default: %d
      lot_%s:
        description: "Sabotages par lot pour la serie %s (1 a 99 ; le changer change les lignes lot k du releve)"
        type: number
        default: %d
""" % (c.lower(), c, n, c.lower(), c, l) for c, _, n, l in SERIES_DU_CIRCUIT))
SERIES_ENV_MATRICE = "".join("          PARTS_%s: ${{ inputs.parts_%s }}\n          LOT_%s: ${{ inputs.lot_%s }}\n"
                             % (c.upper(), c.lower(), c.upper(), c.lower()) for c, _, _, _ in SERIES_DU_CIRCUIT)


SERIES = """# SERIES LONGUES DE SABOTAGES, EN PARALLELE — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py. Simulation uniquement. Lancé par le bouton « Run workflow »,
# ou par le relais .github/workflows/demande_de_serie.yml, qui appuie sur ce même bouton (une seule porte d'entrée).
# LA TABLE (décision de Jean-Luc n°309 du 07-11-2026) : les séries, leurs épreuves, leurs nombres de machines et leurs
# tailles de lot par défaut viennent de tests/LANCEMENT_DES_EPREUVES.json (« serie_du_circuit » d'une entrée de
# « series_hors_de_la_nuit ») ; les entrées du bouton, leurs valeurs par défaut et la matrice en sont fabriquées.
# À QUOI IL SERT. Rejouer les séries de sabotages trop longues pour la machine du Chat (historique long « HL », cours
# propre de Yahoo) sur des machines de ce dépôt public, puis réunir les parts en UN relevé écrit par
# tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py lui-même. « parts_<série> » = 1 joue la série d'un seul tenant.
# LE DÉCOUPAGE (05-11-2026) : les lots par défaut sont ceux des relevés de la machine (la table) ; changer « lot_<série> »
# change les lignes « lot k » du relevé. LE DISQUE :
# 14 Go par machine (documentation GitHub lue le 05-11-2026) et environ 2,4 Go par lot HL joué (mesuré le 04-11-2026) ;
# avec « parts_hl » = 18, une machine joue 2 lots, soit environ 4,8 Go. Un disque plein ne donne jamais « mord » : le
# joueur déclare NON CONFORME tout lot dont la sortie porte une trace d'erreur système.
# CE QU'IL FAIT. ① « preparer » clone la version demandée, vérifie aussitôt, avant tout code de la version, qu'elle est
# la branche publique lancée (voir « LA VERSION ÉPROUVÉE » plus bas) ; puis il lit l'épreuve de chaque série par son
# code dans tests/LANCEMENT_DES_EPREUVES.json (« serie_du_circuit »), date le relevé à l'heure de Paris, note le
# commit du dépôt privé, fabrique la matrice. ② « jouer » : une machine par part, sur CE commit, réseau coupé
# (tests/outils/jouer_une_part.py). ③ « rassembler » : une machine par série, et SEULEMENT si toutes les parts sont
# vertes (tests/outils/rassembler_les_parts.py), sur ce même commit.
# COMME LA CERTIFICATION : chaque job clone le dépôt privé, pose le code de ce dépôt s'il est celui du privé et efface
# tout autre code ; chaque pas passe par programmes/ETAPE_MUETTE.py (le journal public ne dit que OK ou ÉCHEC).
# OÙ VONT LES RÉSULTATS : AU DÉPÔT PRIVÉ, jamais sur main, jamais en archive jointe (lisible par tous ici). Chaque job
# pousse UNE fois sur SA branche : %(branches)s<passage>/<série>/part_<n> pour une part,
# %(branches)s<passage>/<série>/releve pour le relevé (dans rapports/series_longues/<passage>/<série>/sortie/).
# LE MÉNAGE : le Chat lit le relevé et le range dans tests/resultats/ de la version éprouvée. Les branches
# %(branches)s* restent au dépôt privé et se rangent plus tard (choix n°347, Q4 = 3 : la garde qui refusait un passage
# tant qu'il en restait une est retirée, la session du Chat ne pouvant supprimer aucune branche).
# PAS DE RELANCE. Un passage rouge NE SE RELANCE PAS, ni par « Re-run failed jobs », ni par « Re-run all jobs ».
# Pourquoi : chaque job a déjà poussé sa branche (le dépôt tourne même après un échec) ; une nouvelle tentative du même
# job vise la même branche, et sa poussée est refusée, car elle n'est jamais forcée (MODE_EMPLOI_DEPOT.md, règle
# absolue : jamais de poussée forcée, le seul geste qui puisse détruire le travail d'un autre). Le message affiché alors
# (« POUSSEE REFUSEE ») ne dit pas cette cause.
# LA MARCHE À SUIVRE : le Chat lit les branches du passage rouge (journaux) ; il vérifie qu'aucun passage ne tourne ;
# puis un NOUVEAU passage est lancé (bouton, ou nouvelle demande au relais) : son numéro est neuf, ses branches aussi.
# LA VERSION ÉPROUVÉE (décision de Jean-Luc du 05-11-2026 à 13h36, « 2 ») : l'entrée « version » nomme la version du
# dépôt privé à éprouver, « main » (la version officielle) ou la version en attente « travail-… », AVANT sa fusion. Le
# circuit se lance depuis la branche de CE dépôt public qui porte le même nom, où le Chat a publié le code de cette
# version (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py refuse d'écrire dans un clone public d'une autre branche que
# celle du privé) : « publier ce qui tourne », cadre du 08-10-2026. « preparer » refuse de partir si la version n'est
# pas la branche publique lancée, si elle n'existe pas au dépôt privé, si la pointe demandée (entrée « pointe »,
# obligatoire pour une version en attente, A-811 du 15-11-2026) n'est pas exactement sa pointe actuelle, ou si le clone
# n'est pas sa pointe ; chaque job compare ensuite le code publié de cette branche à celui de la version, octet pour
# octet. Plusieurs versions en attente peuvent coexister (A-735) : ce n'est plus un refus.
# La question posée le 05-11-2026 : « Comment veut-on utiliser GitHub pour les séries ? » — 1. après la fusion, retour
# arrière si la série est NON CONFORME ; 2. avant la fusion, par cette entrée ; 3. réponse libre. Réponse : « 2 ».
# Raison : avec 1, une version non éprouvée par ses séries serait la version officielle pendant environ une heure,
# une baisse de contrôle ; avec 2, la barrière « séries conformes avant fusion » est gardée.
# INTERDITS ICI : etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py et
# tests/EPREUVES_DES_AJUSTEMENTS_DE_YAHOO_Jeu_08-10-2026.py (liste : INTERDITS de tests/outils/jouer_une_part.py) —
# retirés de la copie jouée, refusés comme épreuve, cherchés dans l'écoute de chaque part.
name: Series longues de sabotages
on:
  workflow_dispatch:
    inputs:
      version:
        description: "Version du depot prive a eprouver : main, ou la version en attente travail-... (lancer ce circuit depuis la branche publique du meme nom)"
        required: true
        type: string
        default: "main"
      pointe:
        description: "Pointe exacte de la version au depot prive, 40 caracteres hexadecimaux (obligatoire pour travail-... ; vide sur main : la pointe actuelle)"
        required: false
        type: string
        default: ""
%(entrees)sconcurrency:
  group: %(groupe)s
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  preparer:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    outputs:
      sha: ${{ steps.matrice.outputs.sha }}
      series: ${{ steps.matrice.outputs.series }}
      matrice: ${{ steps.matrice.outputs.matrice }}
%(defaults)s    steps:
%(depart_version)s      - name: Fabriquer la matrice
        id: matrice
        env:
          SERIE: ${{ inputs.serie }}
%(env_matrice)s        run: |
          set -u -o pipefail
          echec () { echo "::error::$1"; exit 1; }
          codes="%(codes)s"
          choix=""
          for c in $codes; do
            if [ "$SERIE" = "%(toutes)s" ] || [ "$SERIE" = "$c" ]; then choix="$choix $c"; fi
            vp="PARTS_${c^^}"; vl="LOT_${c^^}"
            [[ "${!vp}" =~ ^[1-9][0-9]?$ ]] || echec "nombre refuse pour $vp (1 a 99)"
            [[ "${!vl}" =~ ^[1-9][0-9]?$ ]] || echec "nombre refuse pour $vl (1 a 99)"
          done
          [ -n "$choix" ] || echec "serie inconnue : $SERIE"
          interdits=$(python3 -B tests/outils/jouer_une_part.py --interdits) || echec "liste des programmes interdits illisible"
          [ -n "$interdits" ] || echec "liste des programmes interdits vide"
          table=tests/LANCEMENT_DES_EPREUVES.json
          [ -f "$table" ] || echec "$table absent"
          jours=(x Lun Mar Mer Jeu Ven Sam Dim)
          read -r u jour_heure < <(TZ=Europe/Paris date '+%%u %%d-%%m-%%Y_%%Hh%%M')
          horodatage="${jours[$u]}_${jour_heure}"
          series='[]'; matrice='[]'
          for s in $choix; do
            vp="PARTS_${s^^}"; vl="LOT_${s^^}"; n="${!vp}"; l="${!vl}"
            cles=$(jq -r --arg c "$s" '.series_hors_de_la_nuit | to_entries[] | select((.value | type) == "object" and (.value.serie_du_circuit | type) == "object" and .value.serie_du_circuit.code == $c) | .key' "$table") || echec "table illisible"
            [ "$(printf '%%s\\n' "$cles" | grep -c .)" = "1" ] || echec "serie $s : il faut exactement une epreuve de code $s dans la table, trouve : ${cles:-aucune}"
            epreuve="$cles"
            if grep -qxF -- "${epreuve##*/}" <<<"$interdits"; then echec "epreuve interdite dans ce circuit : $epreuve"; fi
            [ -f "$epreuve" ] || echec "epreuve absente : $epreuve"
            modele=$(jq -r --arg e "$epreuve" '.series_hors_de_la_nuit[$e].releve' "$table")
            [[ "$modele" == *"*"* ]] || echec "modele de releve sans etoile : $modele"
            releve="${modele/\\*/$horodatage}"
            series=$(jq -c --arg s "$s" --arg e "$epreuve" --arg r "$releve" '. + [{serie: $s, epreuve: $e, releve: $r}]' <<<"$series")
            matrice=$(jq -c --arg s "$s" --arg e "$epreuve" --arg r "$releve" --argjson n "$n" --argjson l "$l" \\
              '. + [range(0; $n) as $i | {serie: $s, epreuve: $e, releve: $r, part: $i, nb_parts: $n, lot: $l}]' <<<"$matrice")
            echo "serie $s : $epreuve -> $releve, $n part(s), lots de $l"
          done
          [ "$(jq length <<<"$matrice")" -le 256 ] || echec "plus de 256 jobs : limite d'une matrice chez GitHub"
          echo "sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"
          echo "series=$series" >> "$GITHUB_OUTPUT"
          echo "matrice=$matrice" >> "$GITHUB_OUTPUT"
  jouer:
    needs: preparer
    runs-on: ubuntu-latest
    # 330 minutes : sous les 6 heures d'une tâche chez GitHub, comme une tranche de la certification
    timeout-minutes: 330
    strategy:
      # une part rouge n'arrête pas les autres ; le rassemblement, lui, refuse dès qu'une seule n'est pas verte
      fail-fast: false
      max-parallel: %(en_meme_temps)d
      matrix:
        include: ${{ fromJSON(needs.preparer.outputs.matrice) }}
    name: jouer ${{ matrix.serie }} ${{ matrix.part }}/${{ matrix.nb_parts }}
%(defaults)s    steps:
%(depart_fige)s%(installer)s%(meme_depot)s%(copie)s%(reseau)s      - name: Jouer la part
        id: jouer_la_part
        env:
          EPREUVE: ${{ matrix.epreuve }}
          RELEVE: ${{ matrix.releve }}
          PART: ${{ matrix.part }}
          NB: ${{ matrix.nb_parts }}
          LOT: ${{ matrix.lot }}
          TMPDIR: ${{ runner.temp }}
        run: |
          unshare -rn python3 -B -u tests/outils/jouer_une_part.py "$RUNNER_TEMP/depot" "$EPREUVE" "$RELEVE" \\
            --part="$PART" --nb-parts="$NB" --lot="$LOT" --parallele="$(nproc)" --travail="$RUNNER_TEMP/travail"
%(deposer_part)s  rassembler:
    needs: [preparer, jouer]
    if: ${{ !cancelled() && needs.preparer.result == 'success' }}
    runs-on: ubuntu-latest
    timeout-minutes: 90
    strategy:
      fail-fast: false
      matrix:
        include: ${{ fromJSON(needs.preparer.outputs.series) }}
    name: rassembler ${{ matrix.serie }}
%(defaults)s    steps:
%(depart_rassembler)s%(installer)s%(meme_depot)s%(copie)s%(reseau)s      - name: Rassembler et ecrire le releve
        id: rassembler
        env:
          EPREUVE: ${{ matrix.epreuve }}
          RELEVE: ${{ matrix.releve }}
          SERIE: ${{ matrix.serie }}
          SERIE_COMMIT: ${{ needs.preparer.outputs.sha }}
          TMPDIR: ${{ runner.temp }}
        run: |
          S="rapports/series_longues/$GITHUB_RUN_ID/$SERIE/sortie"
          rm -rf "$S" && mkdir -p "$S"
          set +e
          unshare -rn python3 -B -u tests/outils/rassembler_les_parts.py "$RUNNER_TEMP/depot" "$EPREUVE" "$RELEVE" \\
            --depuis="$RUNNER_TEMP/parts" --travail="$RUNNER_TEMP/rassemble" > "$S/journal_du_rassemblement.txt" 2>&1
          code=$?
          set -e
          cat "$S/journal_du_rassemblement.txt"
          # 0 conforme, 1 NON conforme : le relevé est écrit par le joueur et déposé ; 2 rien de sûr : aucun relevé déposé
          if [ "$code" = "0" ] || [ "$code" = "1" ]; then
            cp "$RUNNER_TEMP/depot/$RELEVE" "$S/"
            for f in "$RUNNER_TEMP"/depot/archives/*_REMPLACE_PAR_"${RELEVE##*/}"; do
              if [ -f "$f" ]; then cp "$f" "$S/"; fi
            done
          fi
          echo "serie $SERIE : code $code (0 conforme, 1 NON conforme, 2 rien de sur)"
          exit "$code"
%(deposer_final)s""" % {
    "defaults": DEFAULTS, "installer": INSTALLER_LA_MESURE, "en_meme_temps": PARTS_EN_MEME_TEMPS,
    "branches": SERIES_BRANCHES, "groupe": GROUPE_DES_MACHINES_LONGUES,
    "entrees": SERIES_ENTREES, "env_matrice": SERIES_ENV_MATRICE, "toutes": TOUTES,
    "codes": " ".join(s[0] for s in SERIES_DU_CIRCUIT),
    "depart_version": depart_pour(os.path.basename(CIRCUIT_SERIES), "des series longues",
                                  apres_le_clonage=SERIES_VERSION, ref="${{ inputs.version }}",
                                  aussi=("demande_de_serie.yml",)),
    "depart_fige": depart_pour(os.path.basename(CIRCUIT_SERIES), "des series longues",
                               ref="${{ needs.preparer.outputs.sha }}"),
    "depart_rassembler": depart_pour(os.path.basename(CIRCUIT_SERIES), "des series longues",
                                     apres_le_clonage=SERIES_PARTS_VERTES + SERIES_LIRE_LES_PARTS,
                                     ref="${{ needs.preparer.outputs.sha }}"),
    "meme_depot": SERIES_MEME_DEPOT, "copie": SERIES_COPIE, "reseau": SERIES_RESEAU,
    # chaque part dépose son dossier de travail (sans le module d'écoute : un .py hors des emplacements du code, que
    # le rassemblement réécrit depuis le joueur) et renomme son journal (ETAPE_MUETTE le nomme par le job, le même
    # pour toutes les parts), comme une tranche de la certification ; sur SA branche
    "deposer_part": pas_de_depot(
        "depot de la part ou journal introuvable",
        "rapports/series_longues rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}"
        "_${SERIE}_part_${PART}.log",
        "          P=rapports/series_longues/${GITHUB_RUN_ID}/${SERIE}/part_${PART}\n"
        "          mkdir -p rapports/series_longues\n"
        "          if [ -d \"$RUNNER_TEMP/travail\" ]; then rm -rf \"$P\" && mkdir -p \"$P\" && cp -r \"$RUNNER_TEMP/travail/.\" \"$P/\" && rm -rf \"$P/module\"; fi\n"
        "          for f in rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}.log; do\n"
        "            [ -f \"$f\" ] && mv \"$f\" \"${f%.log}_${SERIE}_part_${PART}.log\"\n"
        "          done\n",
        auteur=SERIES_IDENTITE, message="series longues de sabotages, une part", reste="la part",
        branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}",
        valeurs=(("SERIE", "${{ matrix.serie }}"), ("PART", "${{ matrix.part }}"))),
    "deposer_final": pas_de_depot(
        "releve ou journal introuvable",
        "rapports/series_longues rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}"
        "_${SERIE}.log",
        "          mkdir -p rapports/series_longues\n"
        "          for f in rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}.log; do\n"
        "            [ -f \"$f\" ] && mv \"$f\" \"${f%.log}_${SERIE}.log\"\n"
        "          done\n",
        auteur=SERIES_IDENTITE, message="series longues de sabotages, le releve", reste="le releve",
        branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/releve", valeurs=(("SERIE", "${{ matrix.serie }}"),))}


# LE CIRCUIT DES ÉPREUVES LONGUES D'UN TENANT (étape GHUB ②, 15-11-2026 ; décisions de Jean-Luc A-809 du 15-11 à 14h01,
# « Il faut absolument que tu l'utilises […] ça traite 10 fois plus vite », A-811 à 14h18 et A-816 à 15h32, « GitHub en
# priorité »). Les 28 épreuves longues relevées le 15-11-2026 prennent 776 min l'une après l'autre sur une machine,
# environ 83 min sur 10 machines en parallèle (le plancher : la plus longue, la lecture des cours, 5 007 s ; capture
# etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/preuves/V7_GHUB/gain_parallele_et_decoupage.log). Ce gabarit reprend TELS QUELS
# les pas des séries — la porte de la version (SERIES_VERSION, pointe exacte), le départ figé, la copie sans .git ni
# programmes interdits, le réseau coupé, le dépôt sur une branche à soi du privé — et n'ajoute que deux pas : la
# matrice et le jeu d'une épreuve, tous deux confiés à tests/outils/jouer_une_epreuve_longue.py.
EPREUVES_BRANCHES = "epreuves-longues/"
EPREUVES_IDENTITE = "epreuves-longues-publiques"
# LA DURÉE DU JOB « jouer » (R-D7 du relecteur du 15-11-2026, jugé DE FOND) : écrite UNE fois, ici ; le joueur
# (tests/outils/jouer_une_epreuve_longue.py, `delai_restant`) la LIT et coupe l'épreuve sur le temps qui RESTE au job,
# compté depuis le pas « depart » (première chose du job), moins MARGE_D_ECRITURE pour écrire et pousser le résultat.
DUREE_D_UNE_EPREUVE_LONGUE = 330          # minutes, sous les 6 heures d'une tâche chez GitHub
MARGE_D_ECRITURE = 10                     # minutes laissées, après la coupure, au dépôt du résultat
EPREUVES_ENTREES = """      epreuves:
        description: "Codes des epreuves a jouer, separes par des virgules, ou """ + TOUTES + """ (table epreuves_longues de tests/LANCEMENT_DES_EPREUVES.json)"
        required: true
        type: string
"""
EPREUVES = ("""# EPREUVES LONGUES D'UN TENANT, EN PARALLELE — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py. Simulation uniquement. Lancé par le bouton « Run workflow »,
# ou par le relais .github/workflows/demande_de_serie.yml (demande « circuit=epreuve »), qui appuie sur ce même bouton.
# À QUOI IL SERT (étape GHUB ②, décisions de Jean-Luc A-809, A-811, A-816 du 15-11-2026) : jouer sur les machines de ce
# dépôt les épreuves trop longues pour la machine du Chat (plus de 10 minutes), une machine par épreuve, au plus
# %(en_meme_temps)d à la fois, et rendre au DÉPÔT PRIVÉ, pour chacune, sa sortie entière et son code de sortie.
# LA TABLE : l'entrée « epreuves » ne porte que des CODES ; la commande de chaque code est FIGÉE dans la table
# « epreuves_longues » de tests/LANCEMENT_DES_EPREUVES.json de la version éprouvée (lue par
# tests/outils/jouer_une_epreuve_longue.py) ; aucun argument ne vient de la demande.
# LE GROUPE : le même que le circuit des séries (%(groupe)s) : GitHub ne fait tourner qu'un passage du groupe à la fois,
# les deux circuits ne dépassent donc jamais ensemble %(en_meme_temps)d machines, et la marge des autres circuits
# (MARGE_DES_AUTRES_CIRCUITS du fabricant) reste entière.
# CE QU'IL FAIT. ① « preparer » clone la version demandée, vérifie aussitôt, avant tout code de la version, qu'elle est
# la branche publique lancée, qu'elle existe au privé et que la pointe demandée est exactement sa pointe (A-811 ; la
# porte est celle du circuit des séries) ; puis il valide la liste contre la table de la version et fabrique la
# matrice. ② « jouer » : une machine par épreuve, sur CE commit, réseau coupé, comme une tranche de la certification
# (mêmes logiciels, mêmes paquets).
# COMME LA CERTIFICATION : chaque job clone le dépôt privé, pose le code de ce dépôt s'il est celui du privé et efface
# tout autre code ; chaque pas passe par programmes/ETAPE_MUETTE.py (le journal public ne dit que OK ou ÉCHEC).
# OÙ VONT LES RÉSULTATS : AU DÉPÔT PRIVÉ, jamais sur main, jamais en archive jointe. Chaque épreuve pousse UNE fois sur
# SA branche : %(branches)s<passage>/<code>, dossier rapports/epreuves_longues/<passage>/<code>/ (SORTIE.txt,
# RESULTAT.json, et DEMANDE.json : la matrice ENTIÈRE du passage, pour que le rapatrieur sache quelles épreuves
# manquent, R-D2), plus le journal du job. Le Chat les rapatrie par tests/outils/rapatrier_les_epreuves_longues.py.
# PAS DE RELANCE : comme le circuit des séries (sa poussée n'est jamais forcée) ; un passage rouge se lit, puis un
# NOUVEAU passage est demandé.
# INTERDITS ICI : les programmes d'INTERDITS de tests/outils/jouer_une_part.py — retirés de la copie jouée ; une épreuve
# qui les nomme est refusée par le joueur.
name: Epreuves longues d'un tenant
on:
  workflow_dispatch:
    inputs:
      version:
        description: "Version du depot prive a eprouver : main, ou la version en attente travail-... (lancer ce circuit depuis la branche publique du meme nom)"
        required: true
        type: string
        default: "main"
      pointe:
        description: "Pointe exacte de la version au depot prive, 40 caracteres hexadecimaux (obligatoire pour travail-... ; vide sur main : la pointe actuelle)"
        required: false
        type: string
        default: ""
%(entrees)sconcurrency:
  group: %(groupe)s
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  preparer:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    outputs:
      sha: ${{ steps.matrice.outputs.sha }}
      matrice: ${{ steps.matrice.outputs.matrice }}
%(defaults)s    steps:
%(depart_version)s      - name: Fabriquer la matrice
        id: matrice
        env:
          EPREUVES: ${{ inputs.epreuves }}
        run: |
          set -u -o pipefail
          matrice=$(python3 -B tests/outils/jouer_une_epreuve_longue.py --matrice . "$EPREUVES") || { echo "::error::liste d epreuves refusee"; exit 1; }
          n=$(jq length <<<"$matrice") || { echo "::error::matrice illisible"; exit 1; }
          [ "$n" -ge 1 ] && [ "$n" -le 256 ] || { echo "::error::matrice de $n epreuve(s) : de 1 a 256"; exit 1; }
          echo "$n epreuve(s) : $(jq -r '[.[].code] | join(" ")' <<<"$matrice")"
          echo "sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"
          echo "matrice=$matrice" >> "$GITHUB_OUTPUT"
  jouer:
    needs: preparer
    runs-on: ubuntu-latest
    # DUREE_D_UNE_EPREUVE_LONGUE minutes : sous les 6 heures d'une tâche chez GitHub ; le joueur coupe l'épreuve sur le
    # temps qui reste au job, compté depuis le pas « depart », moins MARGE_D_ECRITURE
    timeout-minutes: %(duree)d
    strategy:
      # une épreuve rouge n'arrête pas les autres
      fail-fast: false
      max-parallel: %(en_meme_temps)d
      matrix:
        include: ${{ fromJSON(needs.preparer.outputs.matrice) }}
    name: jouer ${{ matrix.code }}
%(defaults)s    steps:
      - name: Noter le depart du job
        id: depart
        shell: bash
        run: |
          echo "t=$EPOCHSECONDS" >> "$GITHUB_OUTPUT"
%(depart_fige)s%(logiciels)s%(installer)s%(meme_depot)s%(copie)s%(reseau)s      - name: Jouer l epreuve
        id: jouer_l_epreuve
        env:
          CODE: ${{ matrix.code }}
          TMPDIR: ${{ runner.temp }}
          MATRICE: ${{ needs.preparer.outputs.matrice }}
          DEPART_DU_JOB: ${{ steps.depart.outputs.t }}
        run: |
          [[ "$CODE" =~ ^""" + CODE_DE_SERIE + """$ ]] || { echo "::error::code d epreuve refuse"; exit 1; }
          mkdir -p "$GITHUB_WORKSPACE/rapports/epreuves_longues/$GITHUB_RUN_ID/$CODE"
          printf '%%s\\n' "$MATRICE" > "$GITHUB_WORKSPACE/rapports/epreuves_longues/$GITHUB_RUN_ID/$CODE/DEMANDE.json"
          unshare -rn python3 -B -u tests/outils/jouer_une_epreuve_longue.py "$RUNNER_TEMP/depot" "$CODE" \\
            --sortie="$GITHUB_WORKSPACE/rapports/epreuves_longues/$GITHUB_RUN_ID/$CODE"
%(deposer)s""") % {
    "defaults": DEFAULTS, "installer": INSTALLER_LA_MESURE, "logiciels": LOGICIELS_DE_LA_CERTIFICATION,
    "en_meme_temps": PARTS_EN_MEME_TEMPS, "branches": EPREUVES_BRANCHES, "groupe": GROUPE_DES_MACHINES_LONGUES,
    "entrees": EPREUVES_ENTREES, "duree": DUREE_D_UNE_EPREUVE_LONGUE,
    "depart_version": depart_pour(os.path.basename(CIRCUIT_EPREUVES), "des epreuves longues",
                                  apres_le_clonage=SERIES_VERSION, ref="${{ inputs.version }}",
                                  aussi=("demande_de_serie.yml",)),
    "depart_fige": depart_pour(os.path.basename(CIRCUIT_EPREUVES), "des epreuves longues",
                               ref="${{ needs.preparer.outputs.sha }}"),
    "meme_depot": SERIES_MEME_DEPOT, "copie": SERIES_COPIE, "reseau": SERIES_RESEAU,
    # chaque épreuve dépose son dossier de sortie et son journal renommé par son code (ETAPE_MUETTE le nomme par le
    # job, le même pour toutes les épreuves), sur SA branche, comme une part des séries
    "deposer": pas_de_depot(
        "sortie de l epreuve ou journal introuvable",
        "rapports/epreuves_longues rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}"
        "_${CODE}.log",
        "          mkdir -p rapports/epreuves_longues\n"
        "          for f in rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}.log; do\n"
        "            [ -f \"$f\" ] && mv \"$f\" \"${f%.log}_${CODE}.log\"\n"
        "          done\n",
        auteur=EPREUVES_IDENTITE, message="epreuves longues, une epreuve", reste="la sortie de l epreuve",
        branche=EPREUVES_BRANCHES + "${GITHUB_RUN_ID}/${CODE}", valeurs=(("CODE", "${{ matrix.code }}"),))}

# LE RELAIS DES DEMANDES DE SÉRIE (méthode du bloc 2 du 08-11-2026, action 4 ; options choisies par le Chat sous la
# délégation de Jean-Luc, relevé du Chat n°347 — les mots cités sont ceux des options : Q1 = 1 « le relais », Q2 = 1 « la version est le nom de la branche », Q5 = 1 « actions: write pour le
# seul relais, sans secret ni clone du privé, vérifié par le filet », Q7 = 1 « séries seulement »). Le Chat dépose un
# fichier demandes/DEMANDE_<AAAA-MM-JJ_HHhMM>.txt, seul, dans un commit à lui, sur la branche publique de la version
# (main ou travail-…), APRÈS la publication du code ; le relais le lit, le valide et appuie sur le bouton du circuit
# des séries à la place de Jean-Luc (`gh workflow run`), avec le jeton propre du passage (geste prouvé par le passage
# 42384101504 du 07-11-2026, lancé par github-actions[bot] : relevé n°324). Le circuit des séries garde UNE porte.
# LE FICHIER DE DEMANDE, ASCII, une clé par ligne, « cle=valeur » sans espace ; lignes vides et lignes « # … »
# ignorées ; chaque clé au plus une fois ; « serie » obligatoire (TOUTES ou un code de la table) ; « parts_<code> » et
# « lot_<code> » (1 à 99) facultatifs, sinon la valeur de la table ; « a_blanc » (oui/non, non par défaut) : « oui »
# écrit au journal ce qui aurait été lancé, et ne lance rien ; « pointe » (A-811, 15-11-2026) : le commit exact de la
# version au dépôt privé, 40 caractères hexadécimaux, validé par MOTIF_DE_POINTE et non par le motif commun des
# valeurs (au plus 20 caractères), OBLIGATOIRE pour le circuit des séries depuis une branche travail-…, facultatif
# depuis main ; le relais ne peut pas lire le privé : c'est « preparer » qui la compare à la pointe actuelle. Exemple :
#   serie=Yahoo
#   pointe=1c5302a94959b9702e41bb49b13c7a5220a6da43
#   parts_yahoo=2
#   a_blanc=oui
CIRCUIT_RELAIS = os.path.join(".github", "workflows", "demande_de_serie.yml")
NOM_DE_DEMANDE = r"^demandes/DEMANDE_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}h[0-9]{2}[.]txt$"
# LES CIRCUITS QUE LE RELAIS PEUT LANCER — une ligne par circuit : (son nom dans la demande, « circuit=… » ; son fichier ;
# le motif des branches d'où il se lance). Ajout du 08-11-2026 à 18h06, décision de Jean-Luc (« Ok vas y ») : le
# relais lance aussi l'examen de certification à la demande, parce que, prévu à 22h, GitHub le démarre entre 1h et
# 3h45 (2 à 5 h d'attente par nuit), alors qu'un lancement à la main du 07-11-2026 a démarré aussitôt. L'examen n'a
# pas d'entrée : il clone la version officielle du dépôt privé (son clonage ne porte pas « ref: »), il ne se lance
# donc que depuis main. Seul le circuit des séries reçoit des réglages (serie, parts_<code>, lot_<code>).
# Ajout du 15-11-2026 (étape GHUB ②, A-809, A-811, A-816) : « epreuve », le circuit des épreuves longues d'un tenant,
# depuis main ou une version en attente, comme les séries ; il reçoit la liste des codes (« epreuves= ») et la pointe.
CIRCUITS_DU_RELAIS = (("series", os.path.basename(CIRCUIT_SERIES), MOTIF_DE_VERSION),
                      ("examen", os.path.basename(CIRCUIT_CERTIFICATION), "^main$"),
                      ("epreuve", os.path.basename(CIRCUIT_EPREUVES), MOTIF_DE_VERSION))
# Les circuits qui partagent GROUPE_DES_MACHINES_LONGUES : avant de lancer l'un, le relais compte les passages en cours
# ou en attente de TOUS (GitHub ne garde qu'un passage en attente par groupe, quel que soit le circuit : une demande
# d'épreuves ferait disparaître sans message une série en attente, et l'inverse).
CIRCUITS_DU_GROUPE_LONG = (os.path.basename(CIRCUIT_SERIES), os.path.basename(CIRCUIT_EPREUVES))
TAILLE_DE_DEMANDE = 1000          # octets au plus


def _relais_par_serie(modele):
    """Rend `modele` répété pour chaque série de la table, %(c)s = le code, %(m)s = minuscules, %(M)s = majuscules,
    %(n)s et %(l)s = machines et lot par défaut, %(t)s = TOUTES.

    ① RÔLE — Fabriquer une ligne du relais par série, toutes depuis la même boucle.
    ② CONTEXTE D'APPEL — La construction de RELAIS, quatre fois.
    ③ ENTRÉE — `modele` : un texte à clés %(…)s.
    ④ CONDITIONS D'ENTRÉE — SERIES_DU_CIRCUIT est lue.
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — une copie de `modele` par série, dans l'ordre de la table, mises bout à bout.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision n°309 (tout est fabriqué depuis la table) ; un même modèle pour les quatre usages : un code
      ne peut pas recevoir la valeur d'un autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return "".join(modele % {"c": c, "m": c.lower(), "M": c.upper(), "n": n, "l": l, "t": TOUTES}
                   for c, _, n, l in SERIES_DU_CIRCUIT)


RELAIS = """# DEMANDE DE SERIE — LE RELAIS — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py. Simulation uniquement.
# À QUOI IL SERT. Lancer le circuit des séries longues (series_longues.yml), ou l'examen de certification
# (certifier_la_version.yml, depuis main, ajout du 08-11-2026 décidé par Jean-Luc à 18h06), sans que Jean-Luc clique
# sur « Run workflow » : le Chat dépose un fichier de demande (« circuit=series » ou « circuit=examen »), ce relais le
# lit, le valide et appuie sur le bouton du circuit demandé à sa place (table CIRCUITS_DU_RELAIS du fabricant).
# CE QU'IL FAIT, DANS L'ORDRE : ① la poussée doit porter UN commit, dont le parent est la pointe d'avant, qui AJOUTE UN
# seul fichier, demandes/DEMANDE_<AAAA-MM-JJ_HHhMM>.txt (une publication de code ne lance donc jamais rien) ; ② le fichier
# est lu en ASCII strict, une clé par ligne, clés connues seulement, valeurs validées par des motifs tirés de la table
# des séries (tests/LANCEMENT_DES_EPREUVES.json) ; ③ aucun passage du circuit des séries ne doit être en cours ou en
# attente (GitHub n'en garde qu'un en attente par groupe : un troisième ferait disparaître le deuxième sans message) ;
# ④ « a_blanc=oui » : il écrit au journal ce qu'il aurait lancé et s'arrête ; sinon il lance le circuit des séries
# sur CETTE branche, version = nom de la branche, pointe = la pointe demandée (obligatoire depuis travail-…, A-811),
# chaque valeur passée explicitement (celles absentes de la demande prennent la valeur de la table).
# « circuit=epreuve » (étape GHUB ②, 15-11-2026) : « epreuves=<code>,<code>… » ou « epreuves=""" + TOUTES + """ » (codes
# de la table epreuves_longues), « pointe » obligatoire depuis travail-… ; il lance epreuves_longues.yml. Les séries et
# les épreuves partagent un groupe de concurrence : le compte des passages en cours porte sur les DEUX circuits.
# CE QU'IL N'A PAS : aucune clé du dépôt privé, aucun clonage du privé, aucun programme de la version lancé (seulement
# des commandes du système et gh) ; permissions : lire le dépôt, lancer un circuit. Ce texte a été relu ; le
# fabricant refuse de publier un relais qui n'est pas ce texte, octet pour octet (empreinte), et tout autre circuit
# qui porterait la permission de lancer.
name: Demande de serie (relais)
on:
  push:
    paths:
      - "demandes/**"
concurrency:
  group: demande-de-serie
  cancel-in-progress: false
permissions:
  contents: read
  actions: write
jobs:
  relayer:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 2
          persist-credentials: false
      - name: Lire la demande, la valider, appuyer sur le bouton
        id: relayer
        shell: bash
        env:
          AVANT: ${{ github.event.before }}
          APRES: ${{ github.sha }}
          BRANCHE: ${{ github.ref_name }}
          GH_REPO: ${{ github.repository }}
          GH_TOKEN: ${{ github.token }}
        run: |
          set -u -o pipefail
          export LC_ALL=C
          [[ "$BRANCHE" =~ """ + MOTIF_DE_VERSION + """ ]] || { echo "::error::DEMANDE REFUSEE : branche hors de la forme permise (main, ou une version en attente travail-...)"; exit 1; }
          [[ "$AVANT" =~ ^[0-9a-f]{40}$ ]] && [[ "$AVANT" =~ [1-9a-f] ]] || { echo "::error::DEMANDE REFUSEE : pas de pointe d'avant (branche creee par cette poussee ?) : publier le code d'abord, puis la demande seule"; exit 1; }
          parent=$(git rev-parse -q --verify "$APRES^1") || { echo "::error::DEMANDE REFUSEE : commit sans parent lisible"; exit 1; }
          [ "$parent" = "$AVANT" ] || { echo "::error::DEMANDE REFUSEE : la poussee porte plus d'un commit ; la demande se depose seule, dans un commit a elle"; exit 1; }
          [ -z "$(git rev-parse -q --verify "$APRES^2" || true)" ] || { echo "::error::DEMANDE REFUSEE : commit de fusion"; exit 1; }
          changes=$(git diff-tree --no-commit-id --no-renames -r --name-status "$AVANT" "$APRES") || { echo "::error::DEMANDE REFUSEE : changements illisibles"; exit 1; }
          [ "$(printf '%s\\n' "$changes" | grep -c .)" = "1" ] || { echo "::error::DEMANDE REFUSEE : la poussee doit ajouter UN seul fichier, sous demandes/ ; elle en touche $(printf '%s\\n' "$changes" | grep -c .)"; exit 1; }
          statut=$(printf '%s\\n' "$changes" | cut -f1)
          fichier=$(printf '%s\\n' "$changes" | cut -f2-)
          [ "$statut" = "A" ] || { echo "::error::DEMANDE REFUSEE : le fichier n'est pas ajoute (etat $statut)"; exit 1; }
          [[ "$fichier" =~ """ + NOM_DE_DEMANDE + """ ]] || { echo "::error::DEMANDE REFUSEE : nom refuse (demandes/DEMANDE_AAAA-MM-JJ_HHhMM.txt)"; exit 1; }
          taille=$(git cat-file -s "$APRES:$fichier") || { echo "::error::DEMANDE REFUSEE : fichier illisible"; exit 1; }
          [[ "$taille" =~ ^[0-9]{1,4}$ ]] && [ "$taille" -le """ + str(TAILLE_DE_DEMANDE) + """ ] || { echo "::error::DEMANDE REFUSEE : plus de """ + str(TAILLE_DE_DEMANDE) + """ octets"; exit 1; }
          D=$(mktemp -d)
          git cat-file blob "$APRES:$fichier" > "$D/demande.txt" || { echo "::error::DEMANDE REFUSEE : fichier illisible"; exit 1; }
          hors=$(tr -d ' -~\\n' < "$D/demande.txt" | wc -c)
          [ "$hors" = "0" ] || { echo "::error::DEMANDE REFUSEE : $hors octet(s) hors de l'ASCII imprimable (accent, tabulation, retour chariot, caractere de controle)"; exit 1; }
          vus=" "
          CIRCUIT=""
          SERIE=""
          POINTE=""
          EPREUVES=""
          A_BLANC="non"
""" + _relais_par_serie("""          PARTS_%(M)s=%(n)d
          LOT_%(M)s=%(l)d
""") + """          while IFS= read -r ligne || [ -n "$ligne" ]; do
            [ -n "$ligne" ] && [[ "$ligne" != "#"* ]] || continue
            if [[ "$ligne" == pointe=* ]]; then
              valeur="${ligne#pointe=}"
              [[ "$valeur" =~ """ + MOTIF_DE_POINTE + """ ]] || { echo "::error::DEMANDE REFUSEE : pointe de 40 caracteres hexadecimaux en minuscules (${#valeur} caractere(s) recus)"; exit 1; }
              [[ "$vus" != *" pointe "* ]] || { echo "::error::DEMANDE REFUSEE : cle donnee deux fois : pointe"; exit 1; }
              vus="${vus}pointe "
              POINTE="$valeur"
              continue
            fi
            if [[ "$ligne" == epreuves=* ]]; then
              valeur="${ligne#epreuves=}"
              [[ "$valeur" =~ ^(""" + TOUTES + """|""" + CODE_DE_SERIE + """(,""" + CODE_DE_SERIE + """)*)$ ]] || { echo "::error::DEMANDE REFUSEE : epreuves = toutes, ou des codes separes par des virgules (${#valeur} caractere(s) recus)"; exit 1; }
              [[ "$vus" != *" epreuves "* ]] || { echo "::error::DEMANDE REFUSEE : cle donnee deux fois : epreuves"; exit 1; }
              vus="${vus}epreuves "
              if [ "$valeur" != \"""" + TOUTES + """\" ]; then
                deja=" "
                for c in ${valeur//,/ }; do
                  [[ " """ + " ".join(e[0] for e in EPREUVES_DU_CIRCUIT) + """ " == *" $c "* ]] || { echo "::error::DEMANDE REFUSEE : epreuve inconnue : $c"; exit 1; }
                  [[ "$deja" != *" $c "* ]] || { echo "::error::DEMANDE REFUSEE : epreuve demandee deux fois : $c"; exit 1; }
                  deja="$deja$c "
                done
              fi
              EPREUVES="$valeur"
              continue
            fi
            [[ "$ligne" =~ ^([a-z_]{1,20})=([A-Za-z0-9]{1,20})$ ]] || { echo "::error::DEMANDE REFUSEE : ligne illisible (cle=valeur, lettres et chiffres, sans espace ; ${#ligne} caractere(s))"; exit 1; }
            cle="${BASH_REMATCH[1]}"
            valeur="${BASH_REMATCH[2]}"
            [[ "$vus" != *" $cle "* ]] || { echo "::error::DEMANDE REFUSEE : cle donnee deux fois : $cle"; exit 1; }
            vus="$vus$cle "
            if [ "$cle" = "circuit" ]; then
              [[ "$valeur" =~ ^(""" + "|".join(c[0] for c in CIRCUITS_DU_RELAIS) + """)$ ]] || { echo "::error::DEMANDE REFUSEE : circuit inconnu (""" + " ou ".join(c[0] for c in CIRCUITS_DU_RELAIS) + """)"; exit 1; }
              CIRCUIT="$valeur"
            elif [ "$cle" = "serie" ]; then
              [[ "$valeur" =~ ^(""" + "|".join([TOUTES] + [s[0] for s in SERIES_DU_CIRCUIT]) + """)$ ]] || { echo "::error::DEMANDE REFUSEE : serie inconnue de la table"; exit 1; }
              SERIE="$valeur"
            elif [ "$cle" = "a_blanc" ]; then
              [[ "$valeur" =~ ^(oui|non)$ ]] || { echo "::error::DEMANDE REFUSEE : a_blanc vaut oui ou non"; exit 1; }
              A_BLANC="$valeur"
""" + _relais_par_serie("""            elif [ "$cle" = "parts_%(m)s" ]; then
              [[ "$valeur" =~ ^[1-9][0-9]?$ ]] || { echo "::error::DEMANDE REFUSEE : parts_%(m)s de 1 a 99"; exit 1; }
              PARTS_%(M)s="$valeur"
            elif [ "$cle" = "lot_%(m)s" ]; then
              [[ "$valeur" =~ ^[1-9][0-9]?$ ]] || { echo "::error::DEMANDE REFUSEE : lot_%(m)s de 1 a 99"; exit 1; }
              LOT_%(M)s="$valeur"
""") + """            else
              echo "::error::DEMANDE REFUSEE : cle inconnue : $cle"
              exit 1
            fi
          done < "$D/demande.txt"
          [ -n "$CIRCUIT" ] || { echo "::error::DEMANDE REFUSEE : la cle circuit manque (""" + " ou ".join(c[0] for c in CIRCUITS_DU_RELAIS) + """)"; exit 1; }
          FICHIER=""
""" + "".join("""          if [ "$CIRCUIT" = "%s" ]; then
            FICHIER="%s"
            [[ "$BRANCHE" =~ %s ]] || { echo "::error::DEMANDE REFUSEE : le circuit %s ne se lance pas depuis cette branche"; exit 1; }
          fi
""" % (c, f, m, c) for c, f, m in CIRCUITS_DU_RELAIS) + """          [ -n "$FICHIER" ] || { echo "::error::DEMANDE REFUSEE : circuit sans fichier : $CIRCUIT"; exit 1; }
          if [ "$CIRCUIT" = "examen" ]; then
            [ "$vus" = " circuit " ] || [ "$vus" = " circuit a_blanc " ] || [ "$vus" = " a_blanc circuit " ] || { echo "::error::DEMANDE REFUSEE : le circuit $CIRCUIT ne prend aucun reglage (seulement circuit et a_blanc) :$vus"; exit 1; }
          fi
          if [ "$CIRCUIT" = "epreuve" ]; then
            for k in $vus; do
              [[ " circuit epreuves pointe a_blanc " == *" $k "* ]] || { echo "::error::DEMANDE REFUSEE : le circuit epreuve ne prend que circuit, epreuves, pointe et a_blanc : $k"; exit 1; }
            done
            [ -n "$EPREUVES" ] || { echo "::error::DEMANDE REFUSEE : la cle epreuves manque"; exit 1; }
            [ "$BRANCHE" = "main" ] || [ -n "$POINTE" ] || { echo "::error::DEMANDE REFUSEE : la cle pointe manque (obligatoire depuis une version en attente, A-811)"; exit 1; }
          fi
          [ "$CIRCUIT" = "epreuve" ] || [ -z "$EPREUVES" ] || { echo "::error::DEMANDE REFUSEE : la cle epreuves ne vaut que pour le circuit epreuve"; exit 1; }
          [ "$CIRCUIT" != "series" ] || [ -n "$SERIE" ] || { echo "::error::DEMANDE REFUSEE : la cle serie manque"; exit 1; }
          [ "$CIRCUIT" != "series" ] || [ "$BRANCHE" = "main" ] || [ -n "$POINTE" ] || { echo "::error::DEMANDE REFUSEE : la cle pointe manque (obligatoire depuis une version en attente, A-811)"; exit 1; }
""" + _relais_par_serie("""          if [[ "$vus" == *" parts_%(m)s "* || "$vus" == *" lot_%(m)s "* ]] && [ "$SERIE" != "%(t)s" ] && [ "$SERIE" != "%(c)s" ]; then
            echo "::error::DEMANDE REFUSEE : elle regle la serie %(c)s, qu'elle ne joue pas (serie $SERIE)"
            exit 1
          fi
""") + """          COMPTES="$FICHIER"
          if [[ " """ + " ".join(CIRCUITS_DU_GROUPE_LONG) + """ " == *" $FICHIER "* ]]; then COMPTES=\"""" + " ".join(CIRCUITS_DU_GROUPE_LONG) + """\"; fi
          for F in $COMPTES; do
            en_cours=$(gh run list --workflow "$F" --limit 100 --json status --jq '[.[] | select(.status != "completed")] | length' 2>"$D/erreur_gh") || {
              if grep -qi "could not find" "$D/erreur_gh"; then echo "::error::DEMANDE REFUSEE : le circuit $F est inconnu de GitHub au depot public (le relais et $F s installent dans la meme publication, puis une demande a_blanc=oui)"; else echo "::error::DEMANDE REFUSEE : passages de $F illisibles"; fi
              exit 1; }
            [ "$en_cours" = "0" ] || { echo "::error::DEMANDE REFUSEE : $en_cours passage(s) de $F en cours ou en attente ; redeposer la demande quand ils sont finis"; exit 1; }
          done
          echo "demande $fichier : circuit $CIRCUIT ($FICHIER) ; version $BRANCHE ; pointe ${POINTE:-actuelle} ; serie $SERIE""" + _relais_par_serie(" ; parts_%(m)s $PARTS_%(M)s ; lot_%(m)s $LOT_%(M)s") + """ ; epreuves $EPREUVES ; a blanc $A_BLANC"
          if [ "$A_BLANC" = "oui" ]; then
            echo "A BLANC : rien n'est lance"
            exit 0
          fi
          if [ "$CIRCUIT" = "epreuve" ]; then
            gh workflow run "$FICHIER" --ref "$BRANCHE" -f "version=$BRANCHE" -f "pointe=$POINTE" -f "epreuves=$EPREUVES" || { echo "::error::le circuit des epreuves n'a pas pu etre lance"; exit 1; }
            echo "LANCE : $FICHIER sur $BRANCHE"
            exit 0
          fi
          if [ "$CIRCUIT" != "series" ]; then
            gh workflow run "$FICHIER" --ref "$BRANCHE" || { echo "::error::le circuit $FICHIER n'a pas pu etre lance"; exit 1; }
            echo "LANCE : $FICHIER sur $BRANCHE"
            exit 0
          fi
          gh workflow run "$FICHIER" --ref "$BRANCHE" -f "version=$BRANCHE" -f "pointe=$POINTE" -f "serie=$SERIE\"""" + _relais_par_serie(""" -f "parts_%(m)s=$PARTS_%(M)s" -f "lot_%(m)s=$LOT_%(M)s\"""") + """ || { echo "::error::le circuit des series n'a pas pu etre lance"; exit 1; }
          echo "LANCE : $FICHIER sur $BRANCHE"
"""
if ERREUR_DE_LA_TABLE:
    SERIES = RELAIS = EPREUVES = None


# LE FILET DES GABARITS PUBLICS (superviseur R-759 du 04-11-2026, R3 ; relecture du 04-11-2026 à 19h53, I3 : quatre
# sabotages du gabarit SERIES — garde « parts vertes » retirée, identité « certification-publique », archive jointe
# publique, « contents: write » — passaient sans aucune alarme). La liste noire de `fabriquer_le_circuit` (« une archive
# jointe est téléchargeable »…) ne s'appliquait qu'au circuit privé ; ces PROPRIÉTÉS-ci portent sur les gabarits que ce
# programme écrit lui-même, sans épeler un nom de pas.
# Les actions permises dans un gabarit public : le clonage et l'installation de Python. Toute autre action — une
# archive jointe (« upload-artifact »), un cache — rend lisible par tous ce qu'elle emporte.
ACTIONS_PERMISES = ("actions/checkout@", "actions/setup-python@")
# Les jobs qui tournent malgré l'échec d'un job EN MATRICE dont ils dépendent, SANS lire son résultat, avec la raison
# qui le permet. Par défaut, un tel job doit lire « needs.<job>.result » : sinon il travaillerait sur des parts dont une
# a échoué. Un gabarit nouveau est donc strict sans rien déclarer.
SANS_LECTURE_DU_RESULTAT = {
    ("certification", "reunir"): "programmes/CERTIFIER_LA_VERSION.py --reunir rougit s'il manque un certificat partiel",
}
# Le résumé public du passage : la variable de GitHub dont le fichier s'affiche à tout visiteur du dépôt public. Écrit
# UNE fois, lu par les deux contrôles — la liste noire du circuit privé (`fabriquer_le_circuit`) et ce filet (superviseur
# R-759 du 04-11-2026, tour 4, R2 ; deux écritures d'une même chose divergent toujours, R-708).
RESUME_PUBLIC = "GITHUB_STEP_SUMMARY"
# Les gabarits qui ont leurs branches : ils ne poussent que vers elles (« jamais sur main »).
BRANCHES_DES_GABARITS = {"series": SERIES_BRANCHES, "epreuves": EPREUVES_BRANCHES}
# LA SEULE FORME PERMISE D'UNE POUSSÉE dans un gabarit de BRANCHES_DES_GABARITS (superviseur R-759 du 04-11-2026, tour 4,
# R2 : « une liste de formes interdites oublie toujours la suivante ; une forme permise unique n'a rien à oublier »).
# Mesuré par le superviseur en git local : la propriété précédente (« toute cible refs/heads/… commence par le
# préfixe ») laissait passer trois poussées qui écrasent main — « HEAD:main » (git complète un nom court par la branche
# d'en face), une 2e cible sur la ligne suivante après « \ », et « git -c … push ».
# La forme, une fois recollées les lignes coupées par « \ » :
#   git push -q origin "HEAD:refs/heads/<préfixe><nom>" || { echo "<message>"; exit 1; }
# <nom> (CIBLE_DE_POUSSEE) : lettres, chiffres, « _ . / - », « ${VARIABLE} » du shell, « ${{ matrix.<clé> }} » de
# GitHub — rien d'autre : ni « : », ni « + », ni espace hors d'une expression, ni « $( », ni guillemet. La cible est
# donc UNE référence entre guillemets, sous le préfixe. LIMITE MESURÉE (relecture t4, 04-11-2026, D1) : git coupe la
# référence au DERNIER « : » ; une variable qui porterait « :refs/heads/main » écrirait donc main (mesuré en git
# local). Le filet ne lit pas le contenu des variables : il arrête les poussées écrites en clair, pas un gabarit
# piégé volontairement (fonction shell qui redéfinit git, « uses: » d'une action tierce, échappement YAML, fins de
# ligne CRLF — cas D2 à D5 de la même relecture). Seule protection de fond : protéger main sur le serveur. Seules les expressions « matrix. » sont permises : la
# matrice est fabriquée par « preparer » (nombres et séries vérifiés), alors qu'une entrée « inputs. » serait recopiée
# telle quelle dans le script. <message> : sans « $ », « ` », « \ » ni guillemet.
# LE JETON N'APPARAÎT QU'À DEUX ENDROITS PERMIS (superviseur R-759 du 05-11-2026, tour 3, M-2 : « Le mot `secrets`,
# sous toute forme, n'apparaît que dans le `env:` d'un pas permis » ; la relecture du tour 2 a fait passer six formes
# qui donnent le jeton au code de la version — F1 env du job, F2 env du circuit, F3 toJSON(secrets), F4
# secrets['…'], F5 un pas bash qui lance un programme de la version, F6 un pas bash qui écrit $GITHUB_ENV — parce que
# le filet cherchait les mots « secrets. » et « python » à l'intérieur d'un pas). Les deux lignes permises, mot pour
# mot : JETON_DU_PAS dans le bloc « env: » d'un pas PERMIS, et « token: » d'un clonage du dépôt privé. Toute autre
# ligne qui porte « secrets » (sans égard à la casse), à tout niveau d'indentation, est refusée.
# UN PAS PERMIS tourne sous « shell: bash » et son script ne lance que des COMMANDES DU SYSTÈME : chaque mot en
# position de commande (`commandes_d_un_script`) est dans COMMANDES_DU_SYSTEME, aucune sortie n'est redirigée ailleurs
# que vers /dev/null, et aucun FICHIER DE COMMANDES DE GITHUB n'est nommé (un fichier que GitHub relit pour les pas
# suivants : y écrire, c'est donner le jeton à ces pas). Écart déclaré au texte du superviseur (« un pas permis ne
# lance que git, printf et base64 ») : les scripts du gabarit emploient aussi des commandes du système qui ne lancent
# aucun programme (test, grep, cut, awk, tr, tar, mkdir…) ; la liste les nomme, et SANS_RIEN_DE_LA_VERSION fixe le
# PATH, pour qu'elles soient celles du système et non une copie posée par une épreuve.
# FICHIERS_DE_COMMANDES_DE_GITHUB est lu aussi par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py (tour 6, R5-4), qui
# retire ces variables de l'environnement de l'épreuve qu'il joue : la changer ici, c'est la changer là.
COMMANDES_DU_SYSTEME = frozenset(("git", "printf", "base64", "echo", "[", "[[", "test", "cut", "grep", "awk", "tr",
                                  "true", "exit", "set", "mkdir", "rm", "tar", "mv", "cp", "cd", "mktemp", "export",
                                  "read", "unset"))
FICHIERS_DE_COMMANDES_DE_GITHUB = ("GITHUB_ENV", "GITHUB_PATH", "GITHUB_OUTPUT", "GITHUB_STATE", RESUME_PUBLIC, "BASH_ENV")
# les jetons après lesquels le mot suivant est en position de commande
_AVANT_UNE_COMMANDE = frozenset((";", "&&", "||", "|", "(", "<(", "{", "!", "then", "do", "else", "elif", "if", "while",
                                 "until", "&", "|&", ";;"))


def _substitutions(mot):
    """Rend le texte de chaque « $( … ) » d'un mot (entre guillemets), parenthèses comptées.

    ① RÔLE — Lire les commandes cachées dans un mot entre guillemets (« "$(git rev-parse HEAD)" »).
    ② CONTEXTE D'APPEL — `commandes_d_un_script`, pour chaque mot qui porte « $( ».
    ③ ENTRÉE — `mot` : un mot rendu par shlex.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des textes intérieurs.
      [rend: 1]
    ⑥ TRAITEMENT — à chaque « $( », compter les parenthèses jusqu'à la fermante ; une ouverture sans fermante rend
      le reste du mot (le lecteur le refusera s'il n'y lit pas de commande permise).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche de COMMANDES_DU_SYSTEME : une commande entre guillemets se lance aussi.
    ⑨ CE QUI CLOCHE — Une parenthèse dans une chaîne à l'intérieur de la substitution fausse le compte (le texte
      intérieur est alors plus court ou plus long : la lecture reste prudente, elle ne saute rien d'ouvert).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rendu, i = [], mot.find("$(")
    while i >= 0:
        profondeur, j = 1, i + 2
        while j < len(mot) and profondeur:
            profondeur += {"(": 1, ")": -1}.get(mot[j], 0)
            j += 1
        rendu.append(mot[i + 2:j - 1] if profondeur == 0 else mot[i + 2:])
        i = mot.find("$(", j)
    return rendu


def commandes_d_un_script(script):
    """Rend (mots en position de commande, cibles des redirections de sortie) d'un script de shell d'un gabarit.

    ① RÔLE — Dire ce qu'un pas qui tient le jeton LANCE, pour la propriété ⑧ du filet des gabarits.
    ② CONTEXTE D'APPEL — `verifier_les_gabarits_publics`, pour chaque pas qui reçoit JETON_DU_PAS ; par récurrence
      sur chaque « $( … ) » écrit entre guillemets.
    ③ ENTRÉE — `script` : le texte du bloc « run: | », sans son indentation, ou l'intérieur d'une substitution.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des mots en position de commande, la liste des cibles de « > », « >> »,
      « >| », « &> », « &>> ».
        [rend: 2]
    ⑥ TRAITEMENT — les expressions de GitHub « ${{ … }} » remplacées par un mot neutre (GitHub les remplace avant
      bash) ; l'arithmétique « $(( … )) » remplacée par 0 ; les lignes coupées par une barre inverse recollées ;
      chaque ligne lue par shlex (POSIX, ponctuation séparée, sans commentaires) ; un mot est en position de commande
      au début de la ligne et après un jeton de _AVANT_UNE_COMMANDE ; les affectations « NOM=… » qui précèdent sont
      sautées (et le tableau « NOM=( … ) » entier) ; « [[ … ]] » compte pour « [[ » ; « for … do » est sauté
      jusqu'à « do » ; les mots de fin (fi, done, }, ), esac) ne sont pas des commandes ; chaque mot qui porte « $( »
      est relu par récurrence (`_substitutions`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche de COMMANDES_DU_SYSTEME (M-2 du tour 3 : une propriété du pas, pas un mot cherché).
    ⑨ CE QUI CLOCHE — Un lecteur de shell PARTIEL, écrit pour les scripts de ce fichier : « case », les documents
      intégrés (<<), les fonctions et les alias ne sont pas lus ; une ligne que shlex ne sait pas lire lève
      ValueError (refus). Contre un script écrit pour tromper (alias, `eval` caché dans une variable), il ne protège
      pas : le modèle de menace est l'accident (fiche de JETON_DU_PAS).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève ValueError ; la récurrence s'arrête (chaque intérieur est plus court que
      son mot).
        [sort: non]
    """
    texte = re.sub(r"\$\{\{[^}]*\}\}", "X", script)
    texte = re.sub(r"\$\(\([^()]*\)\)", "0", texte)
    texte = re.sub(r"\\\n[ \t]*", " ", texte)
    commandes, cibles = [], []
    for ligne in texte.split("\n"):
        if not ligne.strip() or ligne.strip().startswith("#"):
            continue
        lecteur = shlex.shlex(ligne, posix=True, punctuation_chars=True)
        lecteur.whitespace_split = True
        lecteur.commenters = ""
        try:
            mots = list(lecteur)
        except ValueError as e:
            raise ValueError(f"ligne de shell illisible ({e}) : {ligne.strip()[:100]}") from e
        attendue, i = True, 0
        while i < len(mots):
            m = mots[i]
            if "$(" in m:
                for interieur in _substitutions(m):
                    c, s = commandes_d_un_script(interieur)
                    commandes += c
                    cibles += s
            if m in (">", ">>", ">|", "&>", "&>>"):
                cibles.append(mots[i + 1] if i + 1 < len(mots) else "")
                i += 2
                continue
            if m == "<":    # une entrée : le mot suivant est un fichier, ou « <( » (lu ensuite comme un séparateur)
                i += 1 if i + 1 < len(mots) and mots[i + 1] == "<(" else 2
                continue
            if m in _AVANT_UNE_COMMANDE:
                attendue = True
            elif attendue and re.match(r"^[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\+?=", m):
                if m.endswith("=") and i + 1 < len(mots) and mots[i + 1] == "(":
                    profondeur, i = 1, i + 2
                    while i < len(mots) and profondeur:
                        if "$(" in mots[i]:
                            for interieur in _substitutions(mots[i]):
                                c, s = commandes_d_un_script(interieur)
                                commandes += c
                                cibles += s
                        profondeur += {"(": 1, ")": -1}.get(mots[i], 0)
                        i += 1
                    continue
            elif attendue and m in ("fi", "done", "}", ")", "esac"):
                pass
            elif attendue and m == "[[":
                commandes.append(m)
                attendue = False
                while i < len(mots) and mots[i] != "]]":
                    i += 1
            elif attendue and m == "for":
                while i < len(mots) and mots[i] != "do":
                    i += 1
                continue
            elif attendue:
                commandes.append(m)
                attendue = False
            i += 1
    return commandes, cibles


CIBLE_DE_POUSSEE = r"(?:[A-Za-z0-9_./-]|\$\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{\{ matrix\.[A-Za-z_][A-Za-z0-9_]* \}\})+"
# Une fonction d'état qui fait tourner un job malgré l'échec d'un job dont il dépend.
MALGRE_L_ECHEC = re.compile(r"(?<![\w.])(?:always|failure|cancelled)\s*\(\s*\)", re.I)


MOTIF_CONTROLE = re.compile(r'\[\[ "(\$\{?!?[A-Za-z_][A-Za-z0-9_]*[^"]*)" =~ .*?\]\](.*)$')
MESSAGE_D_ECHEC = re.compile(r'\b(?:echo|echec)\s+"([^"]*)"')


def valeur_citee_apres_un_motif(texte):
    """Rend la première ligne d'un script dont le message d'échec d'un contrôle par motif cite la valeur contrôlée.

    ① RÔLE — La propriété C-D3 : une valeur REFUSÉE par un motif ne s'écrit jamais au journal.
    ② CONTEXTE D'APPEL — `verifier_les_gabarits_publics`, pour chaque gabarit.
    ③ ENTRÉE — `texte` : un gabarit fabriqué.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la ligne fautive (sans ses blancs de tête), ou None.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne « [[ "<valeur>" =~ … ]] … » : le nom de la variable de <valeur> (« $X », « ${X…} »,
      « ${!X} ») ; dans le reste de la ligne, chaque message « echo "…" » ou « echec "…" » ; s'il porte « $X » ou
      « ${X » (« ${!X » pour une valeur indirecte), la ligne est fautive. « ${#X} » (la longueur) est permis.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — C-D3 (Cowork, relecture du 15-11-2026, cas B15 « travail-x\nmain ») : la valeur refusée était écrite
      au journal PUBLIC ; un saut de ligne dans l'entrée y ouvrait une ligne libre, commandes « ::…:: » comprises.
      Superviseur R-759 du 15-11-2026 : réparation « DE FOND » ; une propriété qui couvre toutes ces lignes, sans
      distinguer celles qu'un « read » protège déjà.
    ⑨ CE QUI CLOCHE — Une ligne de contrôle coupée en deux, un message écrit par « printf », ou une valeur recopiée
      dans une autre variable avant d'être citée ne sont pas vus.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for ligne in texte.split("\n"):
        m = MOTIF_CONTROLE.search(ligne)
        if not m:
            continue
        n = re.match(r"\$\{?(!?)([A-Za-z_][A-Za-z0-9_]*)", m.group(1))
        interdit = re.compile(r"\$\{" + n.group(1) + re.escape(n.group(2)) + r"(?![A-Za-z0-9_])"
                              + ("" if n.group(1) else r"|\$" + re.escape(n.group(2)) + r"(?![A-Za-z0-9_])"))
        if any(interdit.search(msg) for msg in MESSAGE_D_ECHEC.findall(m.group(2))):
            return ligne.strip()
    return None


def verifier_les_gabarits_publics(gabarits, circuit_du_soir):
    """Post-condition du fabricant : refuse un gabarit public qui rendrait lisible ou poussable ce qu'il ne doit pas.

    ① RÔLE — Donner un filet aux gabarits écrits dans ce programme (certification, séries), qui n'en avaient pas.
    ② CONTEXTE D'APPEL — `main`, une fois, avant d'écrire quoi que ce soit au clone public.
    ③ ENTRÉE — `gabarits` : {nom : texte} des gabarits à vérifier (« certification », « series ») ·
      `circuit_du_soir` : le texte fabriqué du circuit du soir, lu seulement pour ses identités git.
    ④ CONDITIONS D'ENTRÉE — Les textes sont des fichiers de circuit au format de GitHub, jobs à deux espaces.
    ⑤ SORTIE — Aucune valeur ; lève ValueError à la première propriété violée, avec le gabarit et la raison.
      [rend: rien]
    ⑥ TRAITEMENT — Pour chaque gabarit : ① chaque « uses: » nomme une action de ACTIONS_PERMISES · ② il porte un
      « permissions: » au premier niveau, et chaque « permissions: » ne contient que « contents: read » · ③ aucun
      « GITHUB_STEP_SUMMARY » (le résumé public du passage) · ④ s'il commite, il signe d'au moins une identité
      (« user.name »), et ses identités sont DISTINCTES de celles de chaque autre gabarit et du circuit du soir ·
      ⑤ un job dont la condition porte always(), failure() ou cancelled() lit « needs.<j>.result » de chaque job en
      matrice <j> dont il dépend, sauf déclaration dans SANS_LECTURE_DU_RESULTAT · ⑥ dans un gabarit de
      BRANCHES_DES_GABARITS, les lignes coupées par une barre inverse sont recollées (la barre, la fin de ligne et
      les blancs du début de la ligne suivante retirés), puis toute ligne qui contient « push » (sans égard à la casse) doit avoir
      EXACTEMENT la forme permise, git push -q origin "HEAD:refs/heads/<préfixe><CIBLE_DE_POUSSEE>" || { echo
      "<message>"; exit 1; } ; et le préfixe de ses branches ne commence pas par « travail- » · ⑦ dans un gabarit de
      BRANCHES_DES_GABARITS, chaque clonage du dépôt privé (« - uses: actions/checkout@… » dont le bloc, lu par
      indentation, porte « repository: » DEPOT_PRIVE) porte une ligne « ref: » non vide · ⑧ dans un gabarit de
      BRANCHES_DES_GABARITS, chaque pas (« - » à six espaces, lu jusqu'au pas suivant) : un clonage du dépôt privé
      porte « persist-credentials: false » ; toute ligne qui porte « secrets » (sans égard à la casse, à tout
      niveau d'indentation) est soit « token: ${{ secrets.JETON_DEPOTS }} » d'un clonage du dépôt privé, soit
      JETON_DU_PAS mot pour mot dans le bloc « env: » d'un PAS PERMIS : « shell: bash », chaque commande de son script
      dans COMMANDES_DU_SYSTEME (`commandes_d_un_script`), aucune sortie redirigée ailleurs que vers /dev/null, aucun
      nom de FICHIERS_DE_COMMANDES_DE_GITHUB (tour 3, M-2), et le mot « JETON » n'y apparaît, hors de sa ligne
      JETON_DU_PAS, que dans une copie mot pour mot d'AUTORISATION (tour 4, M-a) · ⑨ (tour 5) dans un gabarit de
      BRANCHES_DES_GABARITS, les pas de chaque job lus dans l'ordre : un pas EXÉCUTE DU CODE DE LA VERSION sauf s'il est
      une action de ACTIONS_PERMISES ou un pas « shell: bash » dont chaque commande est dans COMMANDES_DU_SYSTEME ; un
      pas à jeton placé après le premier pas qui en exécute est refusé, sauf s'il est le DERNIER pas de son job et
      qu'il porte « git push » · ⑩ (tour 5) le script (« run: | ») d'un pas à jeton ne porte aucune expression
      « ${{ ». · ⑪ (08-11-2026) « actions: write » n'est admis qu'au premier niveau, avec « contents: read », et
      alors le gabarit doit passer `verifier_un_relais` (choix n°347, Q5 = 1) · ⑫ (08-11-2026, NV-1) aucun gabarit
      ne porte la souche du nom d'une épreuve de série de la table (`souches_des_epreuves`) · ⑬ (15-11-2026, C-D3)
      aucun message d'échec d'un contrôle par motif ne cite la valeur contrôlée (`valeur_citee_apres_un_motif`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 04-11-2026, R3 : étendre le filet existant plutôt qu'écrire un second contrôle,
      par des propriétés (SI JE RENOMME UN PAS, LE CONTRÔLE NE CHANGE PAS D'AVIS). ⑥ ④ : programmes/MESSAGE_DU_SOIR.py
      juge la certification sur le dernier commit d'auteur « certification-publique », quel que soit le fichier ; une
      identité partagée fausserait ce jugement. ⑥ ⑤ : relecture du 04-11-2026, défaut D1 du tour 1 (un job « jouer »
      rouge ne rougissait pas le rassemblement). ⑥ ⑥ : R1 du superviseur ; « travail- » est réservé à la version en
      attente (A-448) ; une forme PERMISE unique et non une liste de formes interdites (superviseur, tour 4, R2 :
      « HEAD:main », une 2e cible après une barre inverse et « git -c … push » passaient la propriété précédente
      et écrasent main, mesuré en git local). Le recollement retire aussi les blancs de la ligne suivante : un mot
      coupé (« pu », barre inverse, puis « sh ») est alors lu « push » et refusé, au lieu de passer. ⑥ ⑦ : décision de
      Jean-Luc du 05-11-2026 à 13h36 (« 2 », les séries éprouvent la version en attente AVANT sa fusion ; voir
      SERIES_VERSION) : un clonage du privé sans « ref: » prend la branche par défaut, la version officielle ; ce job
      jouerait alors main pendant que les autres jouent la version en attente, et le relevé mêlerait deux versions.
      Propriété et non nom de pas : un job ajouté demain est couvert sans rien déclarer. ⑥ ⑧ : superviseur R-759 du
      05-11-2026, N1 (« persist-credentials: false sur chaque clonage. Le jeton seulement dans les pas qui poussent ou
      lisent les parts ») ; avec l'option 2, ETAPE_MUETTE, les parts et le rassembleur sont du code NON VALIDÉ.
      Depuis le tour 3 (M-2), une propriété du TEXTE ENTIER et non deux mots cherchés dans un pas : commentaire de
      COMMANDES_DU_SYSTEME. Modèle de menace : l'ACCIDENT, décision de Jean-Luc du 05-11-2026 à 17h36 (fiche de
      JETON_DU_PAS) — ce filet arrête une retouche ordinaire qui donnerait le jeton au code de la version (factoriser
      un « env: », lancer un programme de la version dans un pas à jeton), ou qui ÉCRIRAIT LE JETON OU SON DÉRIVÉ AU
      JOURNAL, public pour ce circuit (tour 4, M-a, relecture du tour 3 : une ligne de mise au point qui calcule le
      base64, F9, ou un « echo » du jeton, F13, passaient ; une seule lecture permise, celle d'AUTORISATION, ferme les
      deux par la même propriété, sans liste de commandes interdites), pas un gabarit écrit pour tromper. ⑥ ⑨ :
      superviseur R-759 du 06-11-2026, §3 (relecture de Cowork du 06-11-2026, D1) : le shell par défaut de chaque job
      (programmes/ETAPE_MUETTE.py) est du code de la version ; ce qu'il a exécuté a pu écrire $GITHUB_ENV (BASH_ENV,
      appliqué par GitHub au pas suivant) ou .git/config ; un pas à jeton qui tourne AVANT n'a rien de tout cela à
      lire. La poussée ne peut pas tourner avant (elle dépose ce que ce code a produit) : elle est admise en dernier,
      et ce qu'il lui reste d'exposé attend une décision de Jean-Luc (fiche de `pas_de_depot`, ⑨). ⑥ ⑩ : superviseur
      R-759 du 06-11-2026, §4 ② : GitHub remplace « ${{ … }} » dans le texte du script AVANT que bash le lise ; une
      valeur de la matrice, sortie d'un pas qui a exécuté du code de la version, y deviendrait du code. Dans « env: »,
      c'est une valeur. Le circuit du soir n'est pas vérifié ici : il porte
      « contents: write » (lu le 04-11-2026 dans un circuit fabriqué), et sa liste noire est celle de
      `fabriquer_le_circuit` ; ce filet n'y est pas ajouté, car le circuit privé pousse légitimement sur main.
    ⑨ CE QUI CLOCHE — Lecture ligne à ligne, pas un lecteur YAML : une action écrite dans une forme que ce lecteur ne
      voit pas (« uses » entre guillemets…) passerait ; ces gabarits sont écrits ICI, pas venus du privé. ⑥ ⑤ ne
      vérifie pas que la lecture du résultat PRÉCÈDE le travail du job, seulement qu'elle existe. ⑥ ⑥ ne voit qu'une
      poussée dont le texte porte « push » : une poussée cachée (nom dans une variable, « eval », mot coupé par des
      guillemets comme p"u"sh, alias de git, crochet « pre-push » posé dans .git par une épreuve) n'est pas lisible
      dans le texte. Le crochet « pre-push » est le risque résiduel relevé aux tours 2, 3 et 4, THÉORIQUE, à consigner
      au BACKLOG. Sur-détection VOULUE : une ligne de commentaire qui porte « push » est refusée elle aussi (sauter les
      commentaires rouvrirait un trou : une ligne de commentaire finie par une barre inverse serait recollée à la
      poussée suivante, puis sautée) ; les commentaires d'un gabarit de BRANCHES_DES_GABARITS n'emploient donc pas
      ce mot (constaté le 04-11-2026 : l'en-tête du circuit des séries le citait, le fabricant a refusé).
      ⑥ ⑧ (tour 4) : le mot « JETON » écrit autrement (indirection « ${!x} », mot coupé JE""TON) n'est pas lu, ce
      qui est hors du modèle de l'accident ; une trace rallumée (« set -x ») n'est pas refusée : depuis le tour 5,
      aucune valeur tirée du jeton n'existe dans le shell (AUTORISATION), et l'épreuve du circuit des séries le mesure
      (N4). ⑥ ⑨ juge « exécute du code » par la LISTE des commandes du système, comme ⑧ : un pas « shell: bash » qui
      lance un programme sous un nom de cette liste (« tar --to-command », « git -c alias… ») est cru inoffensif ;
      l'ordre des jobs entre eux n'est pas lu (chaque job a sa machine). ⑥ ⑩ ne lit que le bloc « run: | ».
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    def identites(texte):
        """Rend les identités git (« user.name ») qu'un texte de circuit déclare.

        ① RÔLE — Lire les identités d'un gabarit pour la propriété ⑥ ④.
        ② CONTEXTE D'APPEL — `verifier_les_gabarits_publics`, pour chaque gabarit et pour le circuit du soir.
        ③ ENTRÉE — `texte` : un fichier de circuit.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : l'ensemble des noms.
          [rend: 1]
        ⑥ TRAITEMENT — expression régulière sur « user.name » suivi d'espaces ou de « = ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Fiche de `verifier_les_gabarits_publics`, ⑧ (MESSAGE_DU_SOIR.py juge la certification par son
          auteur).
        ⑨ CE QUI CLOCHE — Une identité posée autrement (variable d'environnement GIT_AUTHOR_NAME) n'est pas lue.
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return set(re.findall(r"user\.name[ =]+[\"']?([^\s\"']+)", texte))

    tous = dict(gabarits)
    tous["circuit du soir"] = circuit_du_soir
    for nom, texte in gabarits.items():
        lignes = texte.split("\n")
        for l in lignes:
            m = re.match(r"^\s*(?:-\s+)?uses:\s*(\S+)", l)
            if m and not m.group(1).startswith(ACTIONS_PERMISES):
                raise ValueError(f"gabarit {nom} : action non permise « {m.group(1)} » (une archive jointe ou un cache "
                                 "est lisible par tous au public)")
        if not re.search(r"^permissions:\s*$", texte, re.M):
            raise ValueError(f"gabarit {nom} : pas de « permissions: » au premier niveau")
        for i, l in enumerate(lignes):
            m = re.match(r"^(\s*)permissions:\s*(.*)$", l)
            if not m:
                continue
            if m.group(2).strip():
                raise ValueError(f"gabarit {nom} : « permissions: {m.group(2).strip()} » (seul « contents: read » est permis)")
            bloc = []
            for suite in lignes[i + 1:]:
                if suite.strip() and len(suite) - len(suite.lstrip()) <= len(m.group(1)):
                    break
                if suite.strip():
                    bloc.append(suite.strip())
            if bloc == ["contents: read", "actions: write"] and not m.group(1):
                verifier_un_relais(nom, texte)    # Q5 = 1 (relevé n°347) : le seul relais, sous conditions
            elif bloc != ["contents: read"]:
                raise ValueError(f"gabarit {nom} : permissions {bloc} (seul « contents: read » est permis, et "
                                 "« actions: write » au premier niveau pour un relais)")
        if RESUME_PUBLIC in texte:
            raise ValueError(f"gabarit {nom} : le résumé public du passage ({RESUME_PUBLIC})")
        citee = valeur_citee_apres_un_motif(texte)
        if citee:
            raise ValueError(f"gabarit {nom} : le message d'échec d'un contrôle par motif cite la valeur contrôlée "
                             f"(C-D3 : une valeur refusée ne s'écrit pas au journal public) : {citee[:120]}")
        for souche in souches_des_epreuves():   # NV-1 (08-11-2026) : le lien série → épreuve vient de la table
            if souche in texte:
                raise ValueError(f"gabarit {nom} : il nomme l'épreuve d'une série (« {souche} ») : le lien série → "
                                 "épreuve se lit dans la table (serie_du_circuit), jamais tapé dans un gabarit")
        les_miennes = identites(texte)
        if "git commit" in texte and not les_miennes:
            raise ValueError(f"gabarit {nom} : il commite sans identité déclarée (user.name)")
        for autre, son_texte in tous.items():
            communes = les_miennes & identites(son_texte) if autre != nom else set()
            if communes:
                raise ValueError(f"gabarit {nom} : identité partagée avec {autre} : {', '.join(sorted(communes))}")
        corps = texte.split("\njobs:\n", 1)[1] if "\njobs:\n" in texte else ""
        jobs = dict(re.findall(r"^  ([A-Za-z_][\w-]*):\n((?:(?:    .*|\s*)\n)*)", corps + "\n", re.M))
        en_matrice = {j for j, b in jobs.items() if re.search(r"^      matrix:", b, re.M)}
        for j, b in jobs.items():
            m_if = re.search(r"^    if:\s*(.*)$", b, re.M)
            m_needs = re.search(r"^    needs:\s*(.*)$", b, re.M)
            if not (m_if and m_needs and MALGRE_L_ECHEC.search(m_if.group(1))):
                continue
            for d in re.findall(r"[A-Za-z_][\w-]*", m_needs.group(1)):
                if d in en_matrice and f"needs.{d}.result" not in b and (nom, j) not in SANS_LECTURE_DU_RESULTAT:
                    raise ValueError(f"gabarit {nom} : le job « {j} » tourne malgré l'échec du job en matrice « {d} » "
                                     f"sans lire needs.{d}.result")
        prefixe = BRANCHES_DES_GABARITS.get(nom)
        if prefixe is not None:
            if prefixe.startswith("travail-"):
                raise ValueError(f"gabarit {nom} : ses branches commencent par « travail- », réservé à la version en attente")
            forme = re.compile(r'\s*git push -q origin "HEAD:refs/heads/' + re.escape(prefixe) + CIBLE_DE_POUSSEE
                               + r'" \|\| \{ echo "[^"$`\\]*"; exit 1; \}\s*')
            for l in re.sub(r"\\\n[ \t]*", "", texte).split("\n"):
                if "push" in l.lower() and not forme.fullmatch(l):
                    raise ValueError(f"gabarit {nom} : une poussée hors de la forme permise (git push -q origin "
                                     f"\"HEAD:refs/heads/{prefixe}…\" || {{ echo …; exit 1; }}) : {l.strip()[:120]}")
            for i, l in enumerate(lignes):
                m = re.match(r"^(\s*)-\s+uses:\s*actions/checkout@", l)
                if not m:
                    continue
                bloc = []
                for suite in lignes[i + 1:]:
                    if suite.strip() and len(suite) - len(suite.lstrip()) <= len(m.group(1)):
                        break
                    bloc.append(suite.strip())
                if ("repository: " + DEPOT_PRIVE) in bloc and not any(re.fullmatch(r"ref:\s*\S.*", b) for b in bloc):
                    raise ValueError(f"gabarit {nom} : un clonage du dépôt privé sans « ref: » (ligne {i + 1}) : il "
                                     "prendrait la version officielle, quelle que soit la version demandée")
            # ⑧ le jeton (superviseur R-759 du 05-11-2026, N1, et tour 3, M-2 ; commentaire de COMMANDES_DU_SYSTEME)
            permises = set()
            debuts = [i for i, l in enumerate(lignes) if re.match(r"^      - ", l)] + [len(lignes)]
            for a, b in zip(debuts, debuts[1:]):
                bloc = []
                for suite in lignes[a:b]:
                    if bloc and suite.strip() and len(suite) - len(suite.lstrip()) < 6:
                        break
                    bloc.append(suite)
                pas = "\n".join(bloc)
                if ("repository: " + DEPOT_PRIVE) in pas:
                    if not re.search(r"^\s*persist-credentials:\s*false\s*$", pas, re.M):
                        raise ValueError(f"gabarit {nom} : un clonage du dépôt privé garde le jeton (ligne {a + 1}, sans "
                                         "« persist-credentials: false ») : le code de la version l'aurait pendant tout le job")
                    permises.update(a + k for k, l in enumerate(bloc) if l.strip() == "token: ${{ secrets.JETON_DEPOTS }}")
                    continue
                if JETON_DU_PAS.rstrip("\n") not in bloc:
                    continue
                k = bloc.index(JETON_DU_PAS.rstrip("\n"))
                env = [e for e in range(k) if bloc[e] == "        env:"]
                if not env or any(not bloc[e].startswith("          ") for e in range(env[-1] + 1, k)):
                    continue   # pas dans le bloc « env: » du pas : la ligne reste non permise, refusée plus bas
                if not re.search(r"^        shell:\s*bash\s*$", pas, re.M):
                    raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) ne tourne pas sous "
                                     "« shell: bash » : le code de la version l'aurait")
                if any(f in pas for f in FICHIERS_DE_COMMANDES_DE_GITHUB):
                    raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) nomme un fichier de "
                                     "commandes de GitHub : les pas suivants l'auraient")
                r = [i for i, l in enumerate(bloc) if l.strip() == "run: |"]
                script = "\n".join(l[10:] for l in bloc[r[0] + 1:]) if r else ""
                # ⑩ (tour 5, superviseur R-759 du 06-11-2026, §4 ②) : aucune expression de GitHub dans le script
                if "${{" in script:
                    raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) porte une expression "
                                     "« ${{ … }} » dans son script : GitHub la remplace avant bash, et une valeur venue "
                                     "d'un pas qui a exécuté du code de la version y serait exécutée ; la passer par « env: »")
                try:
                    commandes, cibles = commandes_d_un_script(script)
                except ValueError as e:
                    raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) : {e}") from e
                hors = sorted(set(commandes) - COMMANDES_DU_SYSTEME)
                raison = ("sans bloc « run: | »" if not r else "commande(s) " + ", ".join(hors) if hors else
                          "sortie redirigée vers " + ", ".join(c for c in cibles if c != "/dev/null")
                          if any(c != "/dev/null" for c in cibles) else "")
                if raison:
                    raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) lance autre chose que "
                                     f"des commandes du système ({raison}) : le code de la version l'aurait")
                # tour 4, M-a : le nom JETON n'est lu que dans une copie mot pour mot d'AUTORISATION (fiche ⑥ ⑧)
                reste = "\n".join(l for e, l in enumerate(bloc) if e != k).replace(AUTORISATION.rstrip("\n"), "")
                if "JETON" in reste:
                    raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) nomme JETON hors de "
                                     "la copie exacte d'AUTORISATION : il pourrait écrire le jeton ou son dérivé au journal")
                permises.add(a + k)
            # ⑨ (tour 5, superviseur R-759 du 06-11-2026, §3) : dans un job, un pas à jeton ne vient après un pas qui
            # exécute du code de la version que s'il est le DERNIER pas du job et qu'il pousse. N'exécute pas de code de
            # la version : une action permise (« uses: »), ou un pas « shell: bash » dont chaque commande est du
            # système. Tout autre pas en exécute : le shell par défaut des jobs (ETAPE_MUETTE.py), un autre « shell: »,
            # un programme lancé, un script illisible.
            jobs_de = {}
            if "jobs:" in lignes:
                job = None
                for i in range(lignes.index("jobs:") + 1, len(lignes)):
                    mj = re.match(r"^  ([A-Za-z_][\w-]*):\s*$", lignes[i])
                    if mj:
                        job = mj.group(1)
                    jobs_de[i] = job
            par_job = {}
            for a, b in zip(debuts, debuts[1:]):
                bloc = [lignes[a]]
                for suite in lignes[a + 1:b]:
                    if suite.strip() and len(suite) - len(suite.lstrip()) < 6:
                        break
                    bloc.append(suite)
                pas = "\n".join(bloc)
                action = re.search(r"^\s*(?:-\s+)?uses:\s*(\S+)", pas, re.M)
                du_code = True
                if action:
                    du_code = not action.group(1).startswith(ACTIONS_PERMISES)
                elif re.search(r"^        shell:\s*bash\s*$", pas, re.M):
                    r_ = [i for i, l in enumerate(bloc) if l.strip() == "run: |"]
                    try:
                        commandes_, _ = commandes_d_un_script("\n".join(l[10:] for l in bloc[r_[0] + 1:]) if r_ else "")
                        du_code = not r_ or not set(commandes_) <= COMMANDES_DU_SYSTEME
                    except ValueError:
                        du_code = True
                par_job.setdefault(jobs_de.get(a), []).append((a, du_code, JETON_DU_PAS.rstrip("\n") in bloc,
                                                               "git push" in pas))
            for job, suite in par_job.items():
                premier = next((a for a, du_code, _, _ in suite if du_code), None)
                for rang, (a, _, a_jeton, pousse) in enumerate(suite):
                    if a_jeton and premier is not None and a > premier and not (rang == len(suite) - 1 and pousse):
                        raise ValueError(f"gabarit {nom} : un pas qui reçoit le jeton (ligne {a + 1}) vient après un pas "
                                         f"qui exécute du code de la version (ligne {premier + 1}) dans le job « {job} » : "
                                         "ce code a pu écrire ce que le pas lit (fichiers de commandes de GitHub, "
                                         ".git/config) ; seule la poussée, dernier pas du job, y est admise")
            for i, l in enumerate(lignes):
                if "secrets" in l.lower() and i not in permises:
                    raise ValueError(f"gabarit {nom} : le jeton (« secrets ») ligne {i + 1} hors des deux places permises "
                                     f"(clonage du privé, « env: » d'un pas permis) : {l.strip()[:100]}")


def souches_des_epreuves():
    """Rend la souche du nom de chaque épreuve de série de la table : « HISTORIQUE_LONG », « COURS_PROPRE_DE_YAHOO »…

    ① RÔLE — Donner au filet ce qu'un lien série → épreuve tapé à la main écrirait (le défaut NV-1).
    ② CONTEXTE D'APPEL — `verifier_les_gabarits_publics`, une fois par gabarit.
    ③ ENTRÉE — — (SERIES_DU_CIRCUIT).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des souches.
      [rend: 1]
    ⑥ TRAITEMENT — le nom du fichier sans « .py », sans le préfixe « EPREUVES_ » suivi de « DE_L_ », « DE_LA_ »,
      « DES_ », « DU_ » ou « DE_ », et sans la date finale « _Jjj_JJ-MM-AAAA ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le pas « Fabriquer la matrice » d'avant le 08-11-2026 cherchait l'épreuve par ces souches
      (« HISTORIQUE_LONG », « COURS_PROPRE_DE_YAHOO ») : un gabarit qui les porte de nouveau a un lien tapé à la main.
      Propriété et non liste : une série ajoutée à la table est couverte sans rien déclarer.
    ⑨ CE QUI CLOCHE — Un morceau plus court de la souche (« LONG ») n'est pas vu.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    souches = []
    for _, epreuve, _, _ in SERIES_DU_CIRCUIT:
        s = re.sub(r"^EPREUVES_(?:DE_L_|DE_LA_|DES_|DU_|DE_)?", "", os.path.basename(epreuve)[:-3])
        souches.append(re.sub(r"_[A-Z][a-z]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}$", "", s))
    return souches


# LA PROPRIÉTÉ DU RELAIS (superviseur R-759 du 08-11-2026, verdict « ARRÊTER ET SIMPLIFIER » ; réparation de fond
# choisie par le Chat sous la délégation de Jean-Luc, n°347) : le relais publié est, OCTET POUR OCTET, le texte RELAIS
# que fabrique ce programme — comparé par empreinte. Le gabarit RELAIS lui-même est relu une fois par un relecteur
# (protocole de livraison) : aucun filet ne prétend juger tout YAML possible. Avant ce tour, une liste blanche de
# commandes laissait passer awk system(), git -c alias / core.pager, gh extension install, tar --to-command
# (essais du superviseur A3, A4, A9, A10, A13 : un relais qui exécute du code avec « actions: write » était ACCEPTÉ).
# Et AUCUN autre circuit publié ne porte « actions: write » (ni « write-all ») : la permission de lancer un circuit
# n'existe que dans ce fichier.
EMPREINTE_DU_RELAIS = hashlib.sha256(RELAIS.encode("utf-8")).hexdigest() if RELAIS is not None else None
PERMISSION_DE_LANCER = re.compile(r"""["']?actions["']?\s*:\s*["']?write\b|\bwrite-all\b""", re.I)


def verifier_un_relais(nom, texte):
    """Refuse un gabarit qui porte « actions: write » s'il n'est pas, octet pour octet, le relais fabriqué.

    ① RÔLE — La condition de la permission « actions: write » (relevé n°347, Q5 = 1 ; réparation de fond du
      superviseur R-759 du 08-11-2026).
    ② CONTEXTE D'APPEL — `verifier_les_gabarits_publics`, quand un gabarit porte « actions: write » au premier niveau ;
      `refus_des_circuits_publies`, pour chaque circuit publié qui porte la permission de lancer.
    ③ ENTRÉE — `nom` : le nom du gabarit ou du fichier ; `texte` : son contenu.
    ④ CONDITIONS D'ENTRÉE — RELAIS est fabriqué (table des séries lisible).
    ⑤ SORTIE — Aucune valeur ; lève ValueError si l'empreinte diffère.
      [rend: rien]
    ⑥ TRAITEMENT — sha256 du texte en UTF-8, comparé à EMPREINTE_DU_RELAIS.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de EMPREINTE_DU_RELAIS : une propriété (« c'est le texte fabriqué ») au lieu d'une
      énumération de commandes, qui laissait chaque tour trouver une nouvelle porte.
    ⑨ CE QUI CLOCHE — Ce contrôle ne dit rien du gabarit RELAIS lui-même : sa sûreté repose sur sa relecture (une
      fois, puis à chaque changement de son texte). Il ne protège pas un relais modifié À LA MAIN au dépôt public sans
      passer par ce programme : celui-là tournerait avant tout contrôle ; seul le pas « circuit_a_jour » du circuit des
      séries le verrait, après coup.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    vue = hashlib.sha256(texte.encode("utf-8")).hexdigest()
    if EMPREINTE_DU_RELAIS is None or vue != EMPREINTE_DU_RELAIS:
        raise ValueError(f"relais {nom} : il porte la permission de lancer un circuit et n'est pas, octet pour octet, le "
                         f"relais fabriqué (empreinte {vue[:16]}, attendue {(EMPREINTE_DU_RELAIS or '?')[:16]})")


# LE REGISTRE DE PROVENANCE (A-599, A-812) : donnees/PROVENANCE_DES_FICHIERS.csv dit d'où vient chaque fichier de
# données du dépôt privé (téléchargement, écrit à la main, fabriqué par un programme), avec son empreinte sha256. Il
# sert ICI de liste de ce qui ne se publie JAMAIS : ni à son chemin, ni sous un autre nom (même empreinte), ni dans les
# dossiers qu'il décrit. Contrôle demandé par l'étape GHUB ② (« tous les fichiers ÉCRITS au public sont publiables,
# confronté au registre ») ; MODE_EMPLOI_DEPOT.md §13.5, bloc C-4, le disait THÉORIQUE.
REGISTRE_DE_PROVENANCE = "donnees/PROVENANCE_DES_FICHIERS.csv"


def refus_selon_la_provenance(prive, public, ecrits):
    """Rend (refus, note) : les fichiers écrits au clone public qui ne sont pas publiables selon le registre.

    ① RÔLE — Dire, APRÈS l'écriture au clone public et AVANT toute poussée, si un fichier écrit est une donnée du dépôt
      privé : son chemin est au registre de provenance, ou sous un dossier que le registre décrit, ou son contenu est,
      octet pour octet, celui d'un fichier du registre ; ou s'il n'est pas un vrai fichier du clone public.
    ② CONTEXTE D'APPEL — `main`, une fois, après l'écriture des gabarits, avant `refus_des_circuits_publies` et
      `publier` ; l'épreuve tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py.
    ③ ENTRÉE — `prive` : la racine du dépôt privé (où est le registre) · `public` : le clone public · `ecrits` : les
      chemins écrits ou retirés au clone public par `main` (séparés par « / »).
    ④ CONDITIONS D'ENTRÉE — Le registre, s'il existe, est un CSV en UTF-8 dont l'en-tête porte « fichier » et
      « sha256 ». S'il n'existe pas et que le dépôt privé a un dossier « donnees », le contrôle ne peut pas tourner :
      OSError (R-734 : un contrôle qui n'a pas pu tourner rend un code non nul). Sans registre ni dossier « donnees »
      (un dépôt d'essai), il n'y a rien à confronter : aucun refus, et la note le dit.
    ⑤ SORTIE — DEUX valeurs : la liste des refus (une phrase par fichier, la première raison ; vide si tout est
      publiable) ; une note d'une ligne (ce qui a été confronté). La phrase nomme le fichier et la raison, jamais le
      contenu. Lève OSError ou ValueError si le registre manque ou ne se lit pas.
      [rend: 2]
    ⑥ TRAITEMENT — lire le registre : l'ensemble des chemins, des empreintes, et des premiers dossiers des chemins
      (aujourd'hui « donnees » et « temoins ») ; pour chaque chemin écrit (une fois chacun) qui existe encore au clone
      (un fichier retiré ne publie rien) : ① le chemin réel n'est pas exactement la racine réelle du clone suivie du
      chemin, ou c'est un lien → refus (un lien posé côté public, fiche ⑨ de `refus_avant_publication`) ; ② son
      premier dossier est un dossier du registre, ou le chemin est au registre → refus ; ③ un fichier non vide dont la
      sha256 est au registre → refus.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le dépôt public est lisible par toute personne connectée ; une donnée privée publiée ne se retire pas
      (décisions de Jean-Luc A-543 du 06 et 08-10-2026, « Je ne veux rien rendre public » ; A-812 du 15-11-2026, « Tu
      sembles oublier les questions de public ou privé sur GitHub »). Les gardes d'AVANT l'écriture
      (`refus_avant_publication`) jugent le dépôt privé ; celle-ci juge ce qui est réellement ÉCRIT au clone public,
      donc aussi les gabarits fabriqués et tout fichier que `main` y pose demain. Propriété et non liste : les dossiers
      refusés sont lus dans le registre, un fichier ajouté au registre est refusé sans rien écrire ici.
    ⑨ CE QUI CLOCHE — Une donnée privée ABSENTE du registre, ou recopiée en partie, ou transformée (autre fin de ligne,
      compressée) n'est pas vue ici (la garde des lignes de `refus_avant_publication` en voit une partie ; depuis le
      15-11-2026, l'étage A, `refus_selon_l_historique`, voit une copie ENTIÈRE de tout fichier du dépôt privé qui ne se
      publie pas, au registre ou non). Le rôle du registre comme liste de ce qui est privé est gardé tant que Jean-Luc
      n'a pas tranché (proposition GHUB2, § 12, point 3). Un fichier
      vide n'est pas confronté aux empreintes (il ne porte rien, et l'empreinte du vide serait un faux refus). Le
      contrôle lit les fichiers APRÈS leur écriture : entre lui et la poussée, un acteur local peut encore les changer
      (même limite que `refus_avant_publication`).
    ⑩ EFFET — Lit le registre et les fichiers écrits. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; des lectures locales.
      [sort: non]
    """
    registre = os.path.join(prive, REGISTRE_DE_PROVENANCE)
    if not os.path.isfile(registre):
        if os.path.isdir(os.path.join(prive, DOSSIER_DES_DONNEES)):
            raise OSError(f"{REGISTRE_DE_PROVENANCE} absent alors que le dépôt privé a un dossier {DOSSIER_DES_DONNEES}/")
        return [], "provenance : aucun registre ni dossier de données au dépôt privé, rien à confronter"
    with open(registre, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if not lecteur.fieldnames or "fichier" not in lecteur.fieldnames or "sha256" not in lecteur.fieldnames:
            raise ValueError(f"{REGISTRE_DE_PROVENANCE} : en-tête sans « fichier » ni « sha256 »")
        lignes = list(lecteur)
    if not lignes:
        raise ValueError(f"{REGISTRE_DE_PROVENANCE} : aucune ligne")
    chemins = {l["fichier"].strip() for l in lignes if l.get("fichier")}
    empreintes = {l["sha256"].strip().lower() for l in lignes if l.get("sha256")}
    dossiers = {c.split("/")[0] for c in chemins if "/" in c}
    racine = os.path.realpath(public)
    refus, vus = [], 0
    for rel in dict.fromkeys(ecrits):
        p = os.path.join(public, rel)
        if not os.path.lexists(p):
            continue
        vus += 1
        if os.path.islink(p) or os.path.realpath(p) != os.path.join(racine, os.path.normpath(rel)):
            refus.append(f"{rel} : lien, ou chemin réel hors du clone public")
        elif rel in chemins or rel.split("/")[0] in dossiers:
            refus.append(f"{rel} : chemin d'une donnée du registre de provenance ({', '.join(sorted(dossiers))})")
        elif os.path.getsize(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() in empreintes:
            refus.append(f"{rel} : même contenu, octet pour octet, qu'un fichier du registre de provenance")
    return refus, (f"provenance : {vus} fichier(s) écrit(s) au public confrontés aux {len(lignes)} lignes du registre "
                   f"({', '.join(sorted(dossiers))}) ; {len(refus)} refus")


# LA PUBLICATION DU COMMIT, L'ÉTAGE A ET LE TÉMOIN DU PARCOURS (livraison 1 du superviseur R-759 du 15-11-2026,
# SUPERVISEUR_GHUB2_Dim_15-11-2026.md, § 3 et § 4 ; jugement fait à partir de la proposition
# PROPOSITION_REPARATION_GHUB2_Dim_15-11-2026.md et de la relecture RELECTEUR_GHUB2_TOUR1_Dim_15-11-2026.md, défaut D1 :
# « donnees/indice_cac40_quotidien.csv recopié sous tests/outils/VOLE_DONNEE.py […] fabricant au code 0, 0 refus »).
# ① CE QUI SE PUBLIE, CE SONT LES BLOBS DU COMMIT du dépôt privé (HEAD), jamais le disque : un fichier non commité
# n'est pas publié, et le fichier contrôlé est celui qui est écrit (plus de course entre le contrôle et la copie).
# ② L'ÉTAGE A : un fichier publié dont le contenu ENTIER est, octet pour octet, celui d'un fichier du dépôt privé à un
# chemin qui NE SE PUBLIE PAS (un fichier de données, une étude, une archive), dans N'IMPORTE QUEL commit de N'IMPORTE
# QUELLE branche, ou sur le disque, est refusé. Aucune exemption par extension (le superviseur, § 1 (a)) : un « .py »
# rangé dans `etudes/` est une référence comme une autre.
# ③ AUCUNE EXEMPTION « DÉJÀ PUBLIC » (retirée le 15-11-2026 : F1 du RELU de Cowork d21df83c, superviseur R-759
# SUPERVISEUR_GHUB2_F1_Dim_15-11-2026.md, « arrêter et simplifier »). Elle exemptait ce qui est sur `main` du PRIVÉ
# à un chemin publié ; or être sur `main` ne prouve pas qu'un contenu a été publié : une donnée fusionnée dans `main`
# (X2), ou un `main` local non poussé (X3), passait, code 0. La lire au dépôt public blanchirait toute fuite déjà
# présente (X4). Les deux programmes qui la justifiaient (programmes/CONTROLER_LES_CAUSES_DES_TROUS.py et
# programmes/verif_backlog.py, identiques à des copies rangées dans des études) ont changé une ligne de leur texte
# explicatif : leur blob n'est plus celui des copies, leur code est le même.
# ④ LE TÉMOIN DU PARCOURS (C-D2 de Cowork) : chaque chemin du registre de provenance (A-599) doit être vu par le
# parcours du disque et lisible ; sinon le parcours n'a pas tourné en entier : arrêt, code 1 (R-734). Seulement présent
# et lisible, jamais son empreinte : une donnée mise à jour avant son registre ne doit pas bloquer la publication.


def est_un_chemin_publie(chemin):
    """Dit si un chemin du dépôt privé est de ceux que le fabricant publie.

    ① RÔLE — La propriété « ce chemin se publie », pour juger un chemin LU DANS L'HISTORIQUE, où `code_a_publier` et
      `fiches_a_publier` (qui listent un dossier) ne peuvent pas servir.
    ② CONTEXTE D'APPEL — `extraire_le_commit` (contrôle d'accord avec les deux listes), `refus_selon_l_historique`.
    ③ ENTRÉE — `chemin` : relatif à la racine, séparé par « / ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si le chemin est un `.py` d'un emplacement de DOSSIERS_DE_CODE (sans sous-dossier),
      tests/LANCEMENT_DES_EPREUVES.json, ou une fiche `.yml`/`.yaml` de `.github/workflows/`.
      [rend: 1]
    ⑥ TRAITEMENT — Séparer le dossier et le nom ; comparer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une propriété, comme les deux listes. Deux écritures d'une même chose divergent (R-708) : `main`
      vérifie à chaque fabrication que cette propriété et les deux listes désignent les MÊMES fichiers du commit
      (`extraire_le_commit`), et s'arrête sinon.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    dossier, nom = posixpath.split(chemin)
    return ((dossier in DOSSIERS_DE_CODE and nom.endswith(".py")) or chemin == LANCEMENT
            or (dossier == FICHES_PRIVEES.replace(os.sep, "/") and nom.endswith((".yml", ".yaml"))))


def _git_prive(prive, *args, entree=None):
    """Lance git en lecture dans le dépôt privé ; rend la sortie en octets, ou lève OSError.

    ① RÔLE — Un appel git borné, pour la publication du commit et l'étage A.
    ② CONTEXTE D'APPEL — `extraire_le_commit`, `refus_selon_l_historique`.
    ③ ENTRÉE — `prive` ; `args` : les arguments de git ; `entree` : des octets donnés à git sur son entrée, ou None.
    ④ CONDITIONS D'ENTRÉE — git est installé.
    ⑤ SORTIE — UNE valeur : la sortie de git, en octets. Lève OSError si git rend un code non nul (R-734 : un contrôle
      qui n'a pas pu tourner ne passe jamais pour un contrôle vert).
      [rend: 1]
    ⑥ TRAITEMENT — « git -c core.quotepath=off -C <prive> <args> », sortie capturée.
    ⑦ UNITÉ — Des secondes : la borne, 600.
    ⑧ POURQUOI — Une seule écriture de l'appel (R-708).
    ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired, que `main` arrête.
    ⑩ EFFET — Ce que fait la commande git (des lectures).
    ⑪ TERMINAISON — Rend la main ; 600 s au plus. Un de mes appels peut-il ne pas revenir ? git, borné à 600 s.
      [sort: non]
    """
    p = subprocess.run(["git", "-c", "core.quotepath=off", "-C", prive] + list(args), input=entree,
                       capture_output=True, timeout=600)
    if p.returncode != 0:
        raise OSError(f"git {args[0]} : code {p.returncode} : {p.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return p.stdout


def empreinte_git(octets):
    """Rend l'identifiant git (blob, SHA-1) d'un contenu.

    ① RÔLE — Comparer un fichier publié aux blobs du dépôt privé sans relancer git pour chacun.
    ② CONTEXTE D'APPEL — `extraire_le_commit`, `refus_selon_l_historique`.
    ③ ENTRÉE — `octets` : le contenu.
    ④ CONDITIONS D'ENTRÉE — Le dépôt privé est au format SHA-1 de git (le format par défaut ; `extraire_le_commit`
      vérifie que le blob relu redonne son identifiant, sinon il s'arrête).
    ⑤ SORTIE — UNE valeur : 40 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — sha1(« blob <taille>\0 » + contenu), la règle de git.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépôt au format SHA-256 de git : les identifiants ne se recouvrent pas ; l'arrêt est garanti
      par la vérification de `extraire_le_commit`.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return hashlib.sha1(b"blob %d\0" % len(octets) + octets).hexdigest()


def extraire_le_commit(prive, dossier):
    """Écrit dans `dossier` les blobs du commit HEAD du dépôt privé qui se trouvent aux emplacements du code publié.

    ① RÔLE — Donner à `main` la SOURCE de la publication : le commit du dépôt privé, jamais son disque.
    ② CONTEXTE D'APPEL — `main`, une fois, avant tout contrôle, quand le dépôt privé porte un « .git ».
    ③ ENTRÉE — `prive` : le dépôt privé · `dossier` : un dossier neuf et vide.
    ④ CONDITIONS D'ENTRÉE — `prive` est un dépôt git qui a un commit HEAD.
    ⑤ SORTIE — DEUX valeurs : le commit (40 caractères hexadécimaux) ; la liste des chemins du commit qui se publient
      selon `est_un_chemin_publie` (fichiers ordinaires seulement). Lève OSError si git échoue, si un blob relu ne
      redonne pas son identifiant, ou si la propriété et les deux listes du fabricant ne désignent pas les mêmes
      fichiers (R-708).
      [rend: 2]
    ⑥ TRAITEMENT — « git rev-parse HEAD^{commit} » ; « git ls-tree -r -z --full-tree <commit> » ; chaque entrée dont le
      dossier est un emplacement de DOSSIERS_DE_CODE ou `.github/workflows/` est écrite dans `dossier` : un fichier
      ordinaire avec les octets du blob (« git cat-file --batch »), un lien symbolique (mode 120000) comme un lien
      symbolique — `refus_avant_publication` le refusera —, un sous-module (mode 160000) ignoré. Puis
      `code_a_publier(dossier)` et `fiches_a_publier(dossier)` doivent désigner exactement les fichiers ordinaires du
      commit que `est_un_chemin_publie` désigne.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Livraison 1 du superviseur R-759 du 15-11-2026 (§ 4 (a)) : « Publier les blobs du commit, pas le
      disque : git archive (ou git show) du SHA poussé au privé ». Le relecteur du 15-11-2026 (D1) a publié un `.py` NON
      SUIVI par git ; et la fiche ⑨ de `refus_avant_publication` disait la course entre le contrôle et la copie. Les
      blobs sont lus par « git cat-file » et non par « git archive », qui applique les attributs `export-subst` et
      `export-ignore` d'un `.gitattributes` : les octets écrits seraient alors autre chose que le blob.
    ⑨ CE QUI CLOCHE — Le commit publié est HEAD : que ce commit soit DÉJÀ POUSSÉ au dépôt privé n'est pas vérifié ici
      (les circuits publics le vérifient : leur porte compare la pointe demandée à celle du dépôt privé). La table des
      séries et des épreuves (`series_du_circuit`, `epreuves_du_circuit`) est lue, au chargement de ce programme, sur
      le disque à côté de lui, et non dans le commit (antérieur, BACKLOG). Les sous-dossiers des emplacements ne sont
      pas extraits : `code_a_publier` ne les publie pas.
    ⑩ EFFET — Lance git en lecture ; écrit dans `dossier`.
    ⑪ TERMINAISON — Rend la main ; chaque git est borné (`_git_prive`).
      [sort: non]
    """
    sha = _git_prive(prive, "rev-parse", "--verify", "HEAD^{commit}").decode().strip()
    lieux = set(DOSSIERS_DE_CODE) | {FICHES_PRIVEES.replace(os.sep, "/")}
    entrees = []
    for e in _git_prive(prive, "ls-tree", "-r", "-z", "--full-tree", sha).split(b"\0"):
        if not e:
            continue
        meta, chemin = e.split(b"\t", 1)
        mode, _, objet = meta.decode().split()
        chemin = chemin.decode("utf-8", "surrogateescape")
        if posixpath.dirname(chemin) in lieux and mode != "160000":
            entrees.append((mode, objet, chemin))
    lot = _git_prive(prive, "cat-file", "--batch", entree="".join(o + "\n" for _, o, _ in entrees).encode())
    i, publies = 0, []
    for mode, objet, chemin in entrees:
        fin = lot.index(b"\n", i)
        tete = lot[i:fin].decode().split()
        taille = int(tete[2])
        octets = lot[fin + 1:fin + 1 + taille]
        i = fin + 1 + taille + 1
        if tete[0] != objet or empreinte_git(octets) != objet:
            raise OSError(f"{chemin} : le blob relu ne redonne pas son identifiant")
        cible = os.path.join(dossier, *chemin.split("/"))
        os.makedirs(os.path.dirname(cible), exist_ok=True)
        if mode == "120000":
            os.symlink(os.fsdecode(octets), cible)
            continue
        with open(cible, "wb") as f:
            f.write(octets)
        if est_un_chemin_publie(chemin):
            publies.append(chemin)
    listes = set(code_a_publier(dossier)) | {FICHES_PRIVEES.replace(os.sep, "/") + "/" + f for f in fiches_a_publier(dossier)}
    if listes != set(publies):
        raise OSError("les listes du fabricant et la propriété est_un_chemin_publie ne désignent pas les mêmes fichiers : "
                      + " ".join(sorted(listes ^ set(publies)))[:300])
    return sha, sorted(publies)


def refus_selon_l_historique(prive, public, ecrits, exclus=()):
    """Rend (refus, note) : l'ÉTAGE A et le TÉMOIN DU PARCOURS, sur les fichiers écrits au clone public.

    ① RÔLE — Refuser un fichier écrit au public dont le contenu entier est celui d'un fichier du dépôt privé à un chemin
      qui ne se publie pas — dans l'historique entier, toutes branches, ou sur le disque —, sans aucune exemption ;
      et prouver que le parcours du disque a tourné en entier (registre de provenance).
    ② CONTEXTE D'APPEL — `main`, une fois, après l'écriture au clone public et avant `publier` ; l'épreuve
      tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py.
    ③ ENTRÉE — `prive` : le dépôt privé · `public` : le clone public · `ecrits` : les chemins écrits ou retirés au
      clone public par `main` (séparés par « / ») · `exclus` : des dossiers à ne pas parcourir sur le disque (le clone
      public et la source extraite, s'ils sont sous le dépôt privé).
    ④ CONDITIONS D'ENTRÉE — Avec un « .git » au dépôt privé, git est installé. Le registre de provenance, s'il existe
      au disque ou au commit, est un CSV en UTF-8 dont l'en-tête porte « fichier ».
    ⑤ SORTIE — DEUX valeurs : la liste des refus (une phrase par fichier, qui nomme le fichier publié et l'identifiant
      du blob, jamais un chemin ni un contenu du dépôt privé : le journal d'un circuit public est lisible par tous) ;
      une note d'une ligne (ce qui a été parcouru, en nombres). Lève OSError si git échoue, si un dossier du disque est
      illisible, ou si le témoin du parcours manque (un chemin du registre absent ou illisible) : le contrôle n'a pas
      tourné en entier (R-734).
      [rend: 2]
    ⑥ TRAITEMENT — ① l'empreinte git de chaque fichier écrit qui existe au clone public ; ② avec git : « git log --all
      --raw --no-renames --diff-merges=separate --root -z » donne chaque couple (chemin, blob) de chaque commit de
      chaque référence (un couple d'un commit apparaît dans le diff qui l'introduit) ; ③ le disque du dépôt privé,
      sans `.git` ni les dossiers `exclus`, sans suivre les liens, `os.walk` qui lève sur un dossier illisible : chaque
      fichier ordinaire est noté VU, et son empreinte n'est calculée que si sa taille est celle d'un fichier écrit ;
      ④ AUCUNE EXEMPTION « DÉJÀ PUBLIC » (retirée le 15-11-2026, F1 du RELU de Cowork d21df83c, superviseur R-759
      « arrêter et simplifier ») : être sur `main` du privé ne prouve pas qu'un contenu a déjà été publié, et lire le
      public blanchirait toute fuite déjà présente ; ⑤ un fichier écrit dont le blob est, en ② ou ③, à un chemin où
      `est_un_chemin_publie` est faux → refus ; ⑥ LE TÉMOIN : le registre REGISTRE_DE_PROVENANCE, exigé au disque s'il est au commit HEAD ;
      chacun de ses chemins doit avoir été VU en ③ et s'ouvrir en lecture → sinon OSError. Un dépôt SUPERFICIEL
      (« shallow ») lève OSError avant ② : son historique n'est pas entier. SANS « .git » au dépôt privé (une copie
      d'épreuve, la copie jouée de la certification) : aucun refus de l'étage A — rien ne peut être poussé d'un tel
      dépôt (`refus_de_branche` refuse un clone public qui a un « .git », `publier` exige une branche) ; le parcours du disque et le témoin tournent quand même.
    ⑦ UNITÉ — Des octets, des fichiers.
    ⑧ POURQUOI — Commentaire de tête (livraison 1 du superviseur R-759 du 15-11-2026). Le registre de provenance n'est
      pas la liste de ce qui est privé (défaut D1 du relecteur : 47 fichiers de données de `donnees/` et 4 051 hors de
      `donnees/` et `temoins/` n'y sont pas) ; ce qui est privé, c'est tout ce qui ne se publie pas.
    ⑨ CE QUI CLOCHE — L'ÉTAGE A NE VOIT QU'UNE COPIE ENTIÈRE, octet pour octet : une donnée découpée, transformée
      (autres fins de ligne, colonnes réordonnées, nombres arrondis), recopiée en partie dans un programme, encodée en
      base64 ou compressée sous un nom de texte n'est pas vue (le texte UTF-8 strict de `refus_avant_publication`
      refuse un ZIP ou un binaire publié sous un `.py` ; un base64 reste du texte et passe). Un fichier VIDE écrit au
      public n'est pas confronté : il ne porte rien, et le blob vide est à des chemins privés (comme au registre de
      provenance, `refus_selon_la_provenance`). Les barres de cours dans
      le code sont l'affaire de la garde de la forme (livraison 2) et du remplacement des barres d'A-825 (livraison 3).
      Une donnée qui n'est ni dans le dépôt (aucun commit, aucune branche, aucun fichier du disque) ni au registre —
      chez Cowork, sur le Drive — n'est pas vue. Un programme publié IDENTIQUE, octet pour octet, à une copie rangée
      dans une étude (ou à un fichier privé quelconque) est refusé à CHAQUE publication, même s'il est déjà au public :
      le Chat change une ligne du texte explicatif du programme (son blob change, son code non) — refus voulu, la règle
      la plus stricte (superviseur R-759 du 15-11-2026, F1). Une fuite déjà présente au public reste refusée à chaque
      passage, jusqu'à la décision de Jean-Luc. L'exemption « sans .git, étage A sans objet » (0dfdab57) avait été
      ajoutée pour les deux mêmes programmes : sa raison d'être a disparu, la garder ou non est au BACKLOG. Le témoin dit qu'un chemin du registre est vu ; il ne dit rien d'un fichier
      qui n'y est pas (un dossier sans fichier enregistré, illisible, est arrêté par `os.walk`).
    ⑩ EFFET — Lance git en lecture ; lit les fichiers écrits, le registre, les fichiers du disque de même taille qu'un
      fichier écrit, et un octet de chaque fichier du registre. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; git est borné (`_git_prive`) ; des lectures locales.
      [sort: non]
    """
    publies = {}
    for rel in dict.fromkeys(ecrits):
        p = os.path.join(public, rel)
        if os.path.isfile(p) and not os.path.islink(p) and os.path.getsize(p):
            with open(p, "rb") as f:
                publies[rel] = empreinte_git(f.read())
    tailles = {os.path.getsize(os.path.join(public, rel)) for rel in publies}
    voulus = set(publies.values())
    lieux = {}
    avec_git = os.path.lexists(os.path.join(prive, ".git"))
    couples = 0
    if avec_git:
        if _git_prive(prive, "rev-parse", "--is-shallow-repository").strip() != b"false":
            raise OSError("le dépôt privé est SUPERFICIEL (clone « shallow ») : son historique n'est pas entier, l'étage A "
                          "ne peut pas le parcourir ; « git fetch --unshallow », puis relancer")
        morceaux = _git_prive(prive, "log", "--all", "--raw", "--no-renames", "--diff-merges=separate", "--root",
                              "--no-abbrev", "-z", "--format=").split(b"\0")
        k = 0
        while k < len(morceaux):
            m = morceaux[k].lstrip(b"\n")
            if m.startswith(b":") and k + 1 < len(morceaux):
                couples += 1
                blob = m.split()[3].decode()
                if blob in voulus:
                    lieux.setdefault(blob, set()).add(morceaux[k + 1].decode("utf-8", "surrogateescape"))
                k += 2
            else:
                k += 1
    racine = os.path.realpath(prive)
    sauts = {os.path.realpath(x) for x in exclus}
    vus, lus = set(), 0
    for dossier, sous, fichiers in os.walk(racine, onerror=_ne_pas_taire):
        sous[:] = [s for s in sous if not os.path.islink(os.path.join(dossier, s))
                   and os.path.join(dossier, s) not in sauts and not (dossier == racine and s == ".git")]
        for f in fichiers:
            p = os.path.join(dossier, f)
            if os.path.islink(p) or not os.path.isfile(p):
                continue
            rel = os.path.relpath(p, racine).replace(os.sep, "/")
            vus.add(rel)
            if os.path.getsize(p) in tailles:
                lus += 1
                with open(p, "rb") as e:
                    b = empreinte_git(e.read())
                if b in voulus:
                    lieux.setdefault(b, set()).add(rel)
    refus = []
    for rel, b in publies.items():
        prives = sorted(c for c in lieux.get(b, ()) if not est_un_chemin_publie(c))
        if avec_git and prives:
            refus.append(f"{rel} : même contenu, octet pour octet (blob {b[:12]}), qu'un fichier du dépôt privé qui ne se "
                         f"publie pas ({len(prives)} chemin(s) dans l'historique ou sur le disque ; "
                         f"« git log --all --find-object={b[:12]} » les nomme) — étage A")
    au_commit = False
    if avec_git:
        try:
            _git_prive(prive, "cat-file", "-e", "HEAD:" + REGISTRE_DE_PROVENANCE)
            au_commit = True
        except OSError:
            au_commit = False
    registre = os.path.join(racine, REGISTRE_DE_PROVENANCE)
    if not os.path.isfile(registre):
        if au_commit:
            raise OSError(f"témoin du parcours : {REGISTRE_DE_PROVENANCE} est au commit mais pas sur le disque "
                          "(clone partiel ?) : le parcours n'a pas vu les données")
        temoin = "aucun registre de provenance (dépôt d'essai) : témoin sans objet"
    else:
        with open(registre, encoding="utf-8", newline="") as f:
            lecteur = csv.DictReader(f)
            if not lecteur.fieldnames or "fichier" not in lecteur.fieldnames:
                raise OSError(f"témoin du parcours : {REGISTRE_DE_PROVENANCE} sans colonne « fichier »")
            attendus = [l["fichier"].strip() for l in lecteur if (l.get("fichier") or "").strip()]
        if not attendus:
            raise OSError(f"témoin du parcours : {REGISTRE_DE_PROVENANCE} ne porte aucun chemin")
        manquants = [c for c in attendus if c not in vus]
        if manquants:
            raise OSError(f"témoin du parcours : {len(manquants)} chemin(s) du registre de provenance non vus par le "
                          f"parcours du disque (absents, liens ou illisibles), dont {manquants[0]} : contrôle incomplet")
        for c in attendus:
            try:
                with open(os.path.join(racine, c), "rb") as e:
                    e.read(1)
            except OSError as e:
                raise OSError(f"témoin du parcours : {c} du registre de provenance illisible ({type(e).__name__}) : "
                              "contrôle incomplet") from e
        temoin = f"témoin : les {len(attendus)} chemins du registre de provenance vus et lisibles"
    if not avec_git:
        return refus, (f"étage A sans objet : dépôt privé sans git, rien n'en peut être poussé (`refus_de_branche`) · "
                       f"{len(vus)} fichier(s) du disque parcourus · {temoin}")
    return refus, (f"étage A : {len(publies)} fichier(s) écrit(s) au public confrontés à "
                   + f"{couples} couple(s) (chemin, blob) de l'historique entier, "
                   + f"{len(vus)} fichier(s) du disque ({lus} de même taille relus), aucune exemption ; "
                   f"{len(refus)} refus · {temoin}")


def circuits_du_relais_non_ecrits(ecrits):
    """Rend les circuits que le relais lance ou compte et que la publication n'écrit pas, si elle écrit le relais.

    ① RÔLE — La propriété R-D3 : le relais et chaque circuit qu'il nomme arrivent dans la MÊME publication.
    ② CONTEXTE D'APPEL — `fabriquer_et_publier`, après l'écriture des circuits ; l'épreuve du circuit des épreuves
      longues (E3a).
    ③ ENTRÉE — `ecrits` : les chemins écrits ou retirés au clone public (séparés par « / »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des noms de fichier absents ; vide si le relais n'est pas écrit.
      [rend: 1]
    ⑥ TRAITEMENT — Les fichiers de CIRCUITS_DU_RELAIS et de CIRCUITS_DU_GROUPE_LONG, cherchés sous
      `.github/workflows/` dans `ecrits`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-D3 du relecteur du 15-11-2026 : le relais compte `epreuves_longues.yml` même pour une demande de
      série ; tant que GitHub ne connaît pas ce circuit au dépôt public, il est plausible que « gh run list » échoue et
      que TOUTE demande soit refusée (THÉORIQUE : aucun appel à l'API n'était permis). Le message du relais distingue
      désormais « circuit inconnu de GitHub » de « passages illisibles ».
    ⑨ CE QUI CLOCHE — Écrire le circuit dans la même publication ne garantit pas que GitHub l'ait enregistré au moment
      de la première demande : le premier geste après installation reste une demande « a_blanc=oui ».
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if CIRCUIT_RELAIS.replace(os.sep, "/") not in ecrits:
        return []
    comptes = {f for _, f, _ in CIRCUITS_DU_RELAIS} | set(CIRCUITS_DU_GROUPE_LONG)
    return sorted(f for f in comptes if FICHES_PRIVEES.replace(os.sep, "/") + "/" + f not in ecrits)


def refus_des_circuits_publies(public):
    """Rend la liste des circuits du clone public qui portent la permission de lancer sans être le relais fabriqué.

    ① RÔLE — Garder la permission « actions: write » dans le SEUL relais, dans tous les circuits publiés.
    ② CONTEXTE D'APPEL — `main`, après l'écriture des circuits et avant toute publication ; l'épreuve du relais.
    ③ ENTRÉE — `public` : le clone public.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des refus (texte), vide si tout va.
      [rend: 1]
    ⑥ TRAITEMENT — chaque fichier .yml ou .yaml de .github/workflows : s'il porte PERMISSION_DE_LANCER (texte, sans
      égard à la casse, commentaires compris), il doit être le relais (même nom de fichier, empreinte de RELAIS) ; tout
      fichier qui ne porte pas « permissions: » au premier niveau est refusé (N9 de Cowork, tour 3 : sans ce bloc, le
      circuit reçoit le réglage « Workflow permissions » du dépôt, illisible sans l'API, peut-être en écriture).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de EMPREINTE_DU_RELAIS. Lecture du TEXTE, pas de la structure : elle sur-détecte (un
      commentaire qui écrit la permission est refusé), et ne dépend d'aucun lecteur YAML.
    ⑨ CE QUI CLOCHE — Une permission écrite d'une façon que le motif ne voit pas passe : échappement YAML
      (« \\x61ctions »), ancre YAML (« &w write » plus haut, puis « actions: *w » ; N10 de Cowork, tour 3). Un bloc
      « permissions: » qui n'est pas au premier niveau mais dans chaque job n'est pas admis : refusé (sur-détection
      voulue).
    ⑩ EFFET — Lit les fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    dossier = os.path.join(public, ".github", "workflows")
    refus = []
    for f in sorted(os.listdir(dossier)) if os.path.isdir(dossier) else []:
        if not f.endswith((".yml", ".yaml")):
            continue
        texte = open(os.path.join(dossier, f), encoding="utf-8", errors="replace").read()
        if not re.search(r"^permissions:", texte, re.M):   # N9 de Cowork (tour 3)
            refus.append(f"{f} ne porte pas « permissions: » au premier niveau : il recevrait le réglage par défaut du "
                         "dépôt public, peut-être la permission de lancer")
            continue
        if not PERMISSION_DE_LANCER.search(texte):
            continue
        try:
            if f != os.path.basename(CIRCUIT_RELAIS):
                raise ValueError(f"{f} porte la permission de lancer un circuit ; seul {os.path.basename(CIRCUIT_RELAIS)} "
                                 "peut la porter")
            verifier_un_relais(f, texte)
        except ValueError as e:
            refus.append(str(e))
    return refus

CHECKOUT_PRIVE = re.compile(r"      - uses: actions/checkout@v5\n        with:\n(?:\s*#.*\n)*\s*fetch-depth: 0\n")

# LA PROPRIÉTÉ DES PAS QUI TOURNENT APRÈS UN ÉCHEC, ÉCRITE ICI ET NULLE PART AILLEURS (superviseur R-759 du 30-10-2026,
# défaut E3) : « une condition `if:` de pas qui contient une fonction d'état — always(), failure(), cancelled(),
# success(), avec ou sans ! — doit, au public, exiger que les programmes publics soient posés ». Chacune de ces
# fonctions retire le success() implicite que GitHub ajoute aux autres conditions : le pas peut alors tourner après
# l'échec de « Poser », avec le programmes/ETAPE_MUETTE.py du clone privé. Le fabricant l'applique
# (`proteger_les_pas`, puis `verifier_les_pas`) et l'épreuve du circuit public l'importe d'ici (E3 bis) : deux
# écritures d'une même règle divergent toujours (R-708). Avant, le fabricant remplaçait la seule chaîne
# « if: always() » : le pas J5, écrit « always() && … », est passé sans protection.
# LA LIMITE, ÉCRITE AU LIEU D'ÊTRE CHASSÉE (superviseur R-759, troisième tour, ③5) : le lecteur des conditions
# (`conditions_du_circuit`) refuse toute forme qu'un auteur écrirait par mégarde ; il ne prétend pas lire comme GitHub un
# texte fabriqué exprès. L'épreuve compare sa lecture à celle de PyYAML, qui n'est pas le lecteur de GitHub (`on` y est
# lu comme le booléen True, mesuré par le superviseur) : c'est un étalonnage, pas un arbitre. La réponse structurelle,
# un verrou à l'exécution qui ne dépend d'aucune lecture, est au BACKLOG.
FONCTION_D_ETAT = re.compile(r"(?<![\w.])(?:always|failure|cancelled|success)\s*\(\s*\)", re.I)
LITTERAL = re.compile(r"'(?:[^']|'')*'")    # une chaîne d'une expression de GitHub : entre apostrophes, '' pour '
PAS_POSE = "poser_les_programmes"
COLONNE_JOB, COLONNE_PAS = 4, 8              # en espaces : « if: » d'un job (`  collecte:` + 2), d'un pas (`      - ` + 2)
CLE_YAML = re.compile(r"^( *)(- +)?([A-Za-z_][\w-]*) *:(?: +(.*))?$")
# LE SOUS-ENSEMBLE YAML QUE LE FABRICANT LIT (superviseur R-759, second tour, R3) : en dehors du contenu des blocs, des
# lignes vides et des commentaires, une ligne est « [- ]clé_nue: [valeur] » (CLE_YAML) ou « - scalaire »
# (SCALAIRE_DE_LISTE) ; une valeur ne commence par aucun indicateur YAML, sauf « | » et « > » qui ouvrent un bloc (BLOC).
SCALAIRE_DE_LISTE = re.compile(r"^( *- +)(\S.*)$")
INDICATEURS = tuple("*&!{[?@%`")
BLOC = re.compile(r"^[|>][-+0-9]*(?: +#.*)?$")
HORS_DU_SOUS_ENSEMBLE = "hors du sous-ensemble YAML lu par le fabricant"
# LES CARACTÈRES QUE LE FABRICANT NE LIT PAS, PAR LEUR CATÉGORIE UNICODE ET NON PAR UNE LISTE (superviseur R-759, troisième
# tour, ③1 ; relecteur, B1(a)) : contrôle (Cc : tabulation, U+0085, « \r »…), format (Cf : marque d'ordre des octets,
# largeurs nulles), séparateurs de ligne et de paragraphe (Zl U+2028, Zp U+2029), usage privé (Co), demi-codets (Cs).
# PyYAML lit U+2028, U+2029 et U+0085 comme des fins de ligne : un `if:` ou un `shell:` posé derrière eux, dans une ligne
# `run:`, échappait au découpage par « \n » de ce programme. Seul « \n » est admis.
CATEGORIES_REFUSEES = ("Cc", "Cf", "Zl", "Zp", "Co", "Cs")
# UNE CHAÎNE ENTRE GUILLEMETS SE FERME SUR SA LIGNE (relecteur, B1(b)) : ouverte, elle se continue sur les lignes suivantes,
# même moins indentées, et une ligne de la chaîne serait lue comme une clé.
CHAINE_SUR_SA_LIGNE = re.compile(r'''^(?:"(?:[^"\\]|\\.)*"|'(?:[^']|'')*')(?: +#.*)?$''')


def porte_une_fonction_d_etat(condition):
    """Dit si une condition `if:` appelle une fonction d'état de GitHub, hors des chaînes entre apostrophes.

    ① RÔLE — La moitié « déclencheur » de la propriété : une condition qui appelle always(), failure(), cancelled()
      ou success() — avec ou sans « ! », espaces tolérés, majuscules comprises — n'a plus le success() implicite.
    ② CONTEXTE D'APPEL — `proteger_les_pas`, `condition_exige_le_code_pose` ; l'épreuve du circuit public (E3 bis).
    ③ ENTRÉE — `condition` : le texte de la condition, avec ou sans `${{ }}`.
    ④ CONDITIONS D'ENTRÉE — Une chaîne.
    ⑤ SORTIE — UNE valeur : vrai si une fonction d'état est appelée hors d'une chaîne entre apostrophes.
      [rend: 1]
    ⑥ TRAITEMENT — remplacer chaque chaîne entre apostrophes par « '' », puis chercher le motif FONCTION_D_ETAT.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `steps.x.outputs.y == 'always()'` n'appelle rien : la protéger lui ferait perdre son success()
      implicite et la ferait tourner après un échec. Les majuscules sont comprises par prudence : la casse des noms de
      fonctions de GitHub n'a pas été vérifiée (superviseur, ④) ; une protection de trop ne fait que retenir un pas.
    ⑨ CE QUI CLOCHE — La syntaxe de GitHub n'est pas analysée : une chaîne entre guillemets doubles (invalide chez
      GitHub) n'est pas reconnue comme chaîne.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return bool(FONCTION_D_ETAT.search(LITTERAL.sub("''", condition)))


def sans_enveloppe(condition):
    """Rend la condition sans son enveloppe `${{ … }}` ; lève si une enveloppe reste à l'intérieur.

    ① RÔLE — Donner l'expression nue, à mettre entre parenthèses dans la condition composée.
    ② CONTEXTE D'APPEL — `proteger_les_pas`, `condition_exige_le_code_pose`.
    ③ ENTRÉE — `condition` : le texte d'une condition `if:` sur une ligne.
    ④ CONDITIONS D'ENTRÉE — Une chaîne.
    ⑤ SORTIE — UNE valeur : l'expression, sans espaces en tête ni en queue ; lève `ValueError` si « ${{ » ou « }} »
      reste hors des chaînes entre apostrophes après le retrait de l'enveloppe entière.
      [rend: 1]
    ⑥ TRAITEMENT — retirer `${{` en tête et `}}` en queue quand les deux y sont, puis chercher un reste.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Composer `${{ … && (${{ always() }}) }}` donnerait une expression imbriquée, invalide (superviseur, ②2).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    c = condition.strip()
    if c.startswith("${{") and c.endswith("}}"):
        c = c[3:-2].strip()
    if "${{" in LITTERAL.sub("''", c) or "}}" in LITTERAL.sub("''", c):
        raise ValueError(f"condition « if: {condition.strip()} » : une enveloppe ${{{{ }}}} partielle, forme non prise en charge")
    return c


def conjoints_de_tete(expression):
    """Rend les termes reliés par « && » au premier niveau de l'expression, ou None.

    ① RÔLE — Dire de quoi une expression est la conjonction, pour savoir si un terme y est EXIGÉ.
    ② CONTEXTE D'APPEL — `condition_exige_le_code_pose`, `proteger_les_pas`.
    ③ ENTRÉE — `expression` : une expression de GitHub, sans enveloppe `${{ }}`.
    ④ CONDITIONS D'ENTRÉE — Une chaîne.
    ⑤ SORTIE — UNE valeur : la liste des termes, espaces réduits à un seul ; None si un « || » est au premier niveau
      (aucun terme n'est alors exigé) ou si les parenthèses ne s'équilibrent pas hors des chaînes.
      [rend: 1]
    ⑥ TRAITEMENT — masquer les chaînes entre apostrophes en gardant leur longueur, parcourir en comptant les
      parenthèses, couper aux « && » du niveau 0, refuser un « || » du niveau 0.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « && » lie plus fort que « || » : `failure() || steps.poser….outcome == 'success'` contient le nom du
      pas « Poser » sans l'exiger. Chercher le nom comme une sous-chaîne (ce que faisait E3 bis) ne le voit pas.
    ⑨ CE QUI CLOCHE — Un terme écrit autrement (sans espaces autour de « == », entre parenthèses) n'est pas reconnu par
      `condition_exige_le_code_pose` : la protection est alors jugée absente — un refus de trop, jamais un silence.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    nu = LITTERAL.sub(lambda m: "'" + "_" * (len(m.group(0)) - 2) + "'", expression)
    niveau, debut, termes, i = 0, 0, [], 0
    while i < len(nu):
        if nu[i] == "(":
            niveau += 1
        elif nu[i] == ")":
            niveau -= 1
            if niveau < 0:
                return None
        elif niveau == 0 and nu.startswith("||", i):
            return None
        elif niveau == 0 and nu.startswith("&&", i):
            termes.append(" ".join(expression[debut:i].split()))
            debut = i + 2
            i += 2
            continue
        i += 1
    if niveau != 0:
        return None
    termes.append(" ".join(expression[debut:].split()))
    return termes


def condition_exige_le_code_pose(condition, pas_pose=PAS_POSE):
    """LA PROPRIÉTÉ : vrai si la condition n'appelle aucune fonction d'état, ou si elle EXIGE que le pas `pas_pose` ait réussi.

    ① RÔLE — Juger une condition `if:` de pas : peut-elle faire tourner le pas alors que le code public n'est pas posé ?
    ② CONTEXTE D'APPEL — `verifier_les_pas` (la post-condition du fabricant) ; l'épreuve du circuit public (E3 bis),
      avec `pas_pose` = « poser_le_code » pour la certification.
    ③ ENTRÉE — `condition` : le texte de la condition (avec ou sans `${{ }}`) · `pas_pose` : l'id du pas qui pose le code.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si la condition est sans fonction d'état, ou si
      « steps.<pas_pose>.outcome == 'success' » est un terme de sa conjonction de premier niveau ; faux sinon. Faux si
      l'enveloppe ne se lit pas ; avec une fonction d'état, faux aussi si les parenthèses ne se lisent pas (sans
      fonction d'état, les parenthèses ne sont pas lues : `(x` rend vrai).
      [rend: 1]
    ⑥ TRAITEMENT — retirer l'enveloppe ; sans fonction d'état : vrai ; sinon lire les termes de premier niveau et y
      chercher celui de `pas_pose`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir le commentaire de FONCTION_D_ETAT. Une condition sans fonction d'état garde le success()
      implicite de GitHub : elle ne tourne pas après l'échec de « Poser ».
    ⑨ CE QUI CLOCHE — Le success() implicite et le sens des fonctions d'état sont tirés de la connaissance de GitHub
      Actions du superviseur, pas d'un passage réel (superviseur, ④).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        c = sans_enveloppe(str(condition))
    except ValueError:
        return False
    if not porte_une_fonction_d_etat(c):
        return True
    termes = conjoints_de_tete(c)
    return termes is not None and f"steps.{pas_pose}.outcome == 'success'" in termes


def conditions_du_circuit(texte):
    """Rend chaque clé `if:` d'un texte de circuit ; lève sur toute ligne hors du sous-ensemble YAML que ce programme lit.

    ① RÔLE — Lire les conditions ligne à ligne, sans yaml, par une LISTE BLANCHE : une ligne que ce programme ne
      comprend pas entièrement est refusée, jamais sautée.
    ② CONTEXTE D'APPEL — `fabriquer_le_circuit` (le texte privé ENTIER), `proteger_les_pas`, `verifier_les_pas` ;
      l'épreuve du circuit public (E3 quater, comparaison avec la lecture par yaml).
    ③ ENTRÉE — `texte` : un texte de circuit, entier ou à partir de « jobs: ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des triplets (numéro de ligne à partir de 0, colonne de la clé, condition brute),
      dans l'ordre du texte ; lève `ValueError` (« hors du sous-ensemble YAML lu par le fabricant ») sur : un
      caractère d'une catégorie de CATEGORIES_REFUSEES, n'importe où dans le texte, blocs compris (tabulation,
      U+0085, U+2028, U+2029, marque d'ordre des octets…) · une ligne qui n'est ni `espaces [- ]clé_nue: [valeur]`
      ni `espaces - scalaire` (clé entre guillemets, `? clé`, style en ligne `{…}`, `---`…) · un élément de liste
      entre guillemets · une valeur ou un scalaire qui commence par un indicateur YAML (INDICATEURS : alias,
      ancre, étiquette, style en ligne…) · une valeur entre guillemets qui ne se ferme pas sur sa ligne · un
      en-tête de bloc non lu (`|` ou `>` suivi d'autre chose qu'un indicateur de bloc) · une valeur qui se
      continue sur la ligne suivante, quelle que soit la clé · une clé « if » écrite dans une autre casse ; et,
      propres à `if:` : bloc `|` ou `>` ·
      valeur vide · valeur entre guillemets ou apostrophes · « # » en fin de valeur · `- if:` en tête de pas ·
      colonne autre que COLONNE_JOB ou COLONNE_PAS.
      [rend: 1]
    ⑥ TRAITEMENT — parcourir les lignes ; sauter le contenu d'un bloc ouvert par une valeur `|` ou `>` (les lignes plus
      indentées que la clé, et les vides), les lignes vides et les commentaires ; toute autre ligne doit être l'une
      des deux formes admises, sinon lever ; vérifier la valeur, la continuation, la casse ; à chaque clé `if`,
      vérifier sa forme et sa colonne, et la retenir.
    ⑦ UNITÉ — Des colonnes en ESPACES.
    ⑧ POURQUOI — Superviseur R-759 du 30-10-2026, second tour (R3, défaut I1 du relecteur) : la version précédente
      SAUTAIT les lignes qu'elle ne reconnaissait pas (`if not m: continue`) ; `"if": always()`, `'if':`, `? if`,
      `if: *alias` passaient alors la post-condition en silence, alors que PyYAML les lit comme des conditions.
      Troisième tour (B1 du relecteur, verdict « arrêter et simplifier ») : U+2028 dans une ligne `run:`, puis une
      chaîne entre guillemets laissée ouverte, passaient encore ; ils sont refusés, par catégorie et par fermeture.
      LA LIMITE : ce lecteur refuse toute forme qu'un auteur écrirait par mégarde ; il ne prétend pas lire comme
      GitHub un texte fabriqué exprès. Sans yaml : aucun programme de `programmes/` ne
      l'importe, et le fabricant tourne au soir public et en certification avant toute installation (superviseur,
      ③) ; la seconde lecture par yaml vit dans l'épreuve.
    ⑨ CE QUI CLOCHE — Ce lecteur n'est pas celui de GitHub, et rien hors de GitHub ne prouve qu'il voit toutes les
      conditions que GitHub verrait dans un texte fabriqué exprès (YAML 1.1 ou 1.2, casse des clés : non vérifiés).
      L'épreuve le compare à PyYAML (E3 quater) sur les textes acceptés : un étalonnage, pas un arbitre — PyYAML lit
      `on` comme True, ce que GitHub ne fait pas. REFUS DE TROP, mesurés par le relecteur du 30-10-2026 sur des
      formes valides : `needs: [a]`, `branches: [main]` (style en ligne), `- 'x'` (élément de liste entre
      apostrophes), une marque d'ordre des octets en tête de fichier, une valeur simple sur deux lignes, un `if` clé
      de `with:` ou de `env:` (colonne 10) ; le refus est bruyant, pas silencieux. Un `if` en colonne 8 sous une
      table de job (`strategy:` puis `matrix:`) serait pris pour une condition de pas (non éprouvé). `- - x` est lu
      comme un scalaire. Le contrôle de l'en-tête de bloc, le seuil du « - scalaire » et la continuation hors `if`
      n'ont aucun sabotage : défense en profondeur, non éprouvée.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    for n, car in enumerate(texte):
        if car != "\n" and unicodedata.category(car) in CATEGORIES_REFUSEES:
            raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : caractère U+{ord(car):04X} (catégorie {unicodedata.category(car)}), "
                             f"ligne {texte.count(chr(10), 0, n) + 1} ; seul le saut de ligne est admis")
    lignes = texte.split("\n")
    rendu, bloc = [], None
    for i, l in enumerate(lignes):
        indent = len(l) - len(l.lstrip(" "))
        if bloc is not None:
            if not l.strip() or indent > bloc:
                continue
            bloc = None
        if not l.strip() or l.lstrip(" ").startswith("#"):
            continue
        ou = f"ligne {i + 1}, « {l.strip()} »"
        m = CLE_YAML.match(l)
        if m:
            colonne = len(m.group(1)) + len(m.group(2) or "")
            valeur = (m.group(4) or "").strip()
        else:
            s = SCALAIRE_DE_LISTE.match(l)
            if not s:
                raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : ligne ni « clé: valeur » ni « - scalaire » ({ou})")
            colonne, valeur = len(s.group(1)), s.group(2).strip()
            if valeur[:1] in ('"', "'"):
                raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : élément de liste entre guillemets ({ou})")
        if m and valeur[:1] in ('"', "'") and m.group(3) != "if" and not CHAINE_SUR_SA_LIGNE.match(valeur):
            raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : chaîne entre guillemets non fermée sur sa ligne ({ou})")
        if valeur[:1] in INDICATEURS:
            raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : valeur qui commence par un indicateur YAML ({ou})")
        cle = m.group(3) if m else None
        if cle is not None and cle.lower() == "if" and cle != "if":
            raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : clé « if » écrite dans une autre casse ({ou})")
        if cle == "if":
            if valeur[:1] in ("|", ">"):
                raise ValueError(f"condition « if: » en bloc ({ou}) : forme non prise en charge, l'écrire sur une ligne")
            if not valeur:
                raise ValueError(f"condition « if: » sans valeur sur sa ligne ({ou}) : forme non prise en charge")
            if valeur[:1] in ("'", '"'):
                raise ValueError(f"condition « if: » entre guillemets ({ou}) : forme non prise en charge")
            if " #" in LITTERAL.sub("''", valeur):
                raise ValueError(f"condition « if: » suivie d'un commentaire ({ou}) : forme non prise en charge")
            if m.group(2):
                raise ValueError(f"« - if: » en tête de pas ({ou}) : forme non prise en charge, mettre « if: » après « name: »")
            if colonne not in (COLONNE_JOB, COLONNE_PAS):
                raise ValueError(f"condition « if: » à la colonne {colonne} ({ou}) : ni un job ({COLONNE_JOB}) ni un pas ({COLONNE_PAS})")
        if valeur[:1] in ("|", ">"):
            if not BLOC.match(valeur):
                raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : en-tête de bloc non lu ({ou})")
            bloc = colonne
            continue
        if valeur:
            suite = next((s_ for s_ in lignes[i + 1:] if s_.strip() and not s_.lstrip(" ").startswith("#")), "")
            seuil = colonne if m else indent     # « - scalaire » : se continue plus à droite que son tiret
            if len(suite) - len(suite.lstrip(" ")) > seuil:
                quoi = "condition « if: » continuée sur la ligne suivante" if cle == "if" else \
                    f"{HORS_DU_SOUS_ENSEMBLE} : valeur continuée sur la ligne suivante"
                raise ValueError(f"{quoi} ({ou})" + (" : forme non prise en charge" if cle == "if" else ""))
        if cle == "if":
            rendu.append((i, colonne, valeur))
    return rendu


def proteger_les_pas(corps):
    """Applique la propriété aux pas du circuit privé : toute condition qui appelle une fonction d'état exige « Poser ».

    ① RÔLE — Réécrire chaque `if:` de pas porteur d'une fonction d'état en
      `${{ always() && steps.poser_les_programmes.outcome == 'success' && (X) }}`, X étant la condition d'origine.
    ② CONTEXTE D'APPEL — `fabriquer_le_circuit`, une fois, sur le corps du circuit privé, avant tout autre ajout.
    ③ ENTRÉE — `corps` : le texte du circuit privé après « jobs: ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le corps réécrit ; lève `ValueError` sur une forme que `conditions_du_circuit` refuse, sur
      un `if:` de job qui appelle une fonction d'état, sur une condition aux parenthèses déséquilibrées.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque condition lue : au niveau du job, refuser une fonction d'état ; au niveau d'un pas, si
      elle en appelle une, retirer l'enveloppe et composer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir le commentaire de FONCTION_D_ETAT. La conjonction garantit que le pas ne tourne JAMAIS si
      « Poser » n'a pas réussi, quelle que soit X — `failure()` et `success() || …` compris ; X garde tout le reste de
      son sens. Un `if:` de job avec fonction d'état est refusé : le fabricant pose déjà le sien (JOB_CONDITION).
    ⑨ CE QUI CLOCHE — La protection porte sur « Poser a réussi », pas sur « le garde mord » : si le pas « Le garde du
      code mord-il ? » tombe, ces pas tournent avec un garde qui ne mord pas (superviseur, hors périmètre, à consigner).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    lignes = corps.split("\n")
    for i, colonne, valeur in conditions_du_circuit(corps):
        if not porte_une_fonction_d_etat(valeur):
            continue
        if colonne == COLONNE_JOB:
            raise ValueError(f"le circuit privé porte un « if: » de job qui appelle une fonction d'état (« {valeur} »)")
        x = sans_enveloppe(valeur)
        if conjoints_de_tete("(" + x + ")") is None:
            raise ValueError(f"condition « if: {valeur} » : parenthèses déséquilibrées")
        lignes[i] = " " * COLONNE_PAS + f"if: ${{{{ always() && steps.{PAS_POSE}.outcome == 'success' && ({x}) }}}}"
    return "\n".join(lignes)


def verifier_les_pas(corps_public):
    """POST-CONDITION : lève si un `if:` de pas du job du circuit fabriqué viole la propriété.

    ① RÔLE — Rendre impossible la publication d'un circuit dont un pas pourrait tourner sur un code non posé, quelle
      que soit la façon dont la transformation a été écrite ou cassée.
    ② CONTEXTE D'APPEL — `fabriquer_le_circuit`, une fois, sur le job fabriqué depuis le privé (pas propres au public
      exclus : le job de décision et JOURNAL sont écrits ici, en `shell: bash` pour JOURNAL).
    ③ ENTRÉE — `corps_public` : le texte du job, transformé, commentaires retirés.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien : rend None ; lève `ValueError` au premier pas fautif, ou sur une forme non prise en charge.
      [rend: rien]
    ⑥ TRAITEMENT — relire les conditions (`conditions_du_circuit`) ; à la colonne d'un pas, juger chacune par
      `condition_exige_le_code_pose`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 30-10-2026, ③1 : le fabricant est le seul chemin vers le public ; l'invariant y
      vit, que l'auteur ait pensé à l'épreuve ou non. Le pas « Le circuit public est-il celui que fabrique le dépôt
      privé ? » du soir relance le fabricant : il crierait aussi.
    ⑨ CE QUI CLOCHE — Elle juge avec la même propriété que la transformation : une propriété fausse les trompe toutes
      deux (l'épreuve du circuit public la calibre sur des cas connus).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    for i, colonne, valeur in conditions_du_circuit(corps_public):
        if colonne == COLONNE_PAS and not condition_exige_le_code_pose(valeur):
            raise ValueError(f"POST-CONDITION — le pas de la ligne {i + 1} du job peut tourner sur un code non posé "
                             f"(« if: {valeur} »)")


def fabriquer_le_circuit(texte_prive):
    """Fabrique le texte du fichier du circuit public à partir de celui du privé.

    ① RÔLE — Transformer le texte du circuit privé en circuit public.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves.
    ③ ENTRÉE — `texte_prive` : le contenu de `.github/workflows/collecte_abc.yml`.
    ④ CONDITIONS D'ENTRÉE — Le texte porte `jobs:`, `runs-on: ubuntu-latest` et un
      clonage `actions/checkout@v5` avec `fetch-depth: 0`, chacun UNE fois ; son job
      s'appelle `collecte` ; il porte `${{ inputs.rattrapage }}` UNE fois.
    ⑤ SORTIE — UNE valeur : le texte du circuit public ; lève `ValueError` si une
      forme attendue manque, s'il reste du code Python écrit, si une ligne du texte
      privé ENTIER sort du sous-ensemble YAML lu ou si une condition `if:` a une forme
      non prise en charge (`conditions_du_circuit`), ou si la post-condition
      trouve un pas qui peut tourner sur un code non posé (`verifier_les_pas`). [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête du programme, ⑥ ②-③. Le texte privé entier passe
      d'abord la liste blanche ; les conditions des pas sont protégées ensuite, sur le
      corps privé ; la post-condition relit le job fabriqué.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête, ⑧ : une seule rédaction des pas.
    ⑨ CE QUI CLOCHE — Les commentaires sont retirés ligne entière : un « # » en
      fin de ligne de commande reste.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
      [sort: non]
    """
    # LE TEXTE PRIVÉ ENTIER passe la liste blanche : une ancre posée dans « on: » servirait dans un job (superviseur R-759,
    # second tour, R3).
    conditions_du_circuit(texte_prive)
    if texte_prive.count("\njobs:\n") != 1:
        raise ValueError("le circuit privé ne porte pas une seule ligne « jobs: »")
    corps = corps_prive = texte_prive.split("\njobs:\n", 1)[1]
    if corps.count("    runs-on: ubuntu-latest\n") != 1:
        raise ValueError("« runs-on: ubuntu-latest » absent ou répété")
    if len(CHECKOUT_PRIVE.findall(corps)) != 1:
        raise ValueError("le clonage du dépôt privé n'a pas la forme attendue")
    if not corps.startswith(JOB_PRIVE):
        raise ValueError("le circuit privé ne commence pas par le job « collecte: »")
    if corps.count(RATTRAPAGE_PRIVE) != 1:
        raise ValueError(f"« {RATTRAPAGE_PRIVE} » absent ou répété dans le circuit privé")
    # UN PAS DU PRIVÉ QUI TOURNE APRÈS UN ÉCHEC NE TOURNE QUE SI LE CODE PUBLIC EST POSÉ : sinon il exécuterait les
    # programmes du clone privé (relecture du 15-10-2026, A3). Par la PROPRIÉTÉ (superviseur R-759 du 30-10-2026, défaut
    # E3), sur le corps privé, avant tout ajout du fabricant : JOB_CONDITION porte son propre « !cancelled() ».
    corps = proteger_les_pas(corps)
    corps = corps.replace(JOB_PRIVE, JOB_CONDITION, 1).replace(RATTRAPAGE_PRIVE, RATTRAPAGE_PUBLIC)
    corps = CHECKOUT_PRIVE.sub(lambda m: CLONAGES, corps)
    corps = corps.replace("    runs-on: ubuntu-latest\n", "    runs-on: ubuntu-latest\n" + DEFAULTS, 1)
    corps = corps.replace("${{ secrets.TOKEN_PUBLIC }}", "${{ secrets.JETON_DEPOTS }}")
    lignes = [l for l in corps.split("\n") if not l.lstrip().startswith("#")]
    verifier_les_pas("\n".join(lignes))
    texte = (ENTETE + DECISION_ENTETE + CLONAGES + DECISION_PAS + JOURNAL
             + "\n".join(lignes).rstrip("\n") + "\n" + JOURNAL)
    for interdit in ("secrets.TOKEN_PUBLIC",):
        if interdit in texte:
            raise ValueError(f"il reste « {interdit} » dans le circuit public")
    # CE QUE LES PAS DU PRIVÉ NE DOIVENT PAS PORTER, parce que le circuit public le
    # rendrait lisible (relecture du 08-10-2026, sabotages S1 à S5) : un interpréteur
    # propre (sa sortie échapperait à l'enrobage), une action autre que le clonage
    # (une archive jointe est téléchargeable), du code Python écrit, un texte « << »
    # (un commentaire y serait retiré), le résumé public du passage.
    for motif, raison in ((r"^\s*shell:", "un pas qui déclare son propre interpréteur"),
                          (r"^\s*-?\s*uses:\s*(?!\s|actions/checkout@)", "une action autre que le clonage"),
                          (r"python3?\s+(?:-\w+\s+)*-c\b", "du code Python écrit dans le fichier"),
                          (r"python3?\s+(?:-\w+\s+)*-\s", "du code Python lu sur l'entrée"),
                          (r"<<", "un texte « << »"),
                          (re.escape(RESUME_PUBLIC), "le résumé public du passage")):
        if re.search(motif, corps_prive, re.M):
            raise ValueError(f"le circuit privé porte {raison}")
    return texte


def branche_du_clone(dossier):
    """Rend la branche git sur laquelle est un dossier, s'il est la racine d'un dépôt git.

    ① RÔLE — Lire, pour `refus_de_branche`, la version que porte un clone : sa branche courante.
    ② CONTEXTE D'APPEL — `refus_de_branche`, deux fois (le dépôt privé, le clone public).
    ③ ENTRÉE — `dossier` : un chemin.
    ④ CONDITIONS D'ENTRÉE — Le programme git est installé dès que `dossier` porte un « .git » (sinon FileNotFoundError,
      que `main` traite en ARRÊT).
    ⑤ SORTIE — DEUX valeurs : vrai si `dossier` porte un « .git » (dossier ou fichier, comme un « worktree ») ; le nom
      court de la branche courante (« main », « travail-x »), ou None (pas de « .git », ou HEAD détachée sur un
      commit, comme un clonage à « ref: <sha> »).
      [rend: 2]
    ⑥ TRAITEMENT — « .git » absent : (False, None). Sinon « git -C <dossier> symbolic-ref -q --short HEAD » : son texte
      si le code est 0, None sinon.
    ⑦ UNITÉ — Des secondes : la borne de git, 30.
    ⑧ POURQUOI — Décision de Jean-Luc du 05-11-2026 à 13h36 (voir `refus_de_branche`). Le « .git » est cherché À LA
      RACINE du dossier et non par git lui-même : un dossier jetable rangé sous un autre dépôt git (le RUNNER_TEMP du
      pas « circuit à jour », une copie d'épreuve) serait sinon lu comme une branche de ce dépôt-là.
    ⑨ CE QUI CLOCHE — Une branche « non née » (dépôt créé par « git init », sans commit) a un nom, et il est rendu :
      voulu, les épreuves s'en servent. Un « .git » qui n'est pas un dépôt valide rend None (git échoue).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main, ou lève subprocess.TimeoutExpired après 30 s : l'appel à git peut ne pas revenir,
      la borne le coupe.
      [sort: non]
    """
    if not os.path.lexists(os.path.join(dossier, ".git")):
        return False, None
    r = subprocess.run(["git", "-C", dossier, "symbolic-ref", "-q", "--short", "HEAD"],
                       capture_output=True, text=True, timeout=30)
    return True, (r.stdout.strip() or None) if r.returncode == 0 else None


def refus_de_branche(prive, public):
    """Rend la raison de refuser d'écrire dans le clone public, ou None : il doit être sur la branche du dépôt privé.

    ① RÔLE — Garantir que la branche du dépôt public reçoit le code de la version du même nom, et d'elle seule.
    ② CONTEXTE D'APPEL — `main`, une fois, avant toute écriture au clone public.
    ③ ENTRÉE — `prive` : la racine du dépôt privé · `public` : le clone du dépôt public.
    ④ CONDITIONS D'ENTRÉE — Celles de `branche_du_clone`.
    ⑤ SORTIE — UNE valeur : None si l'écriture est permise ; sinon le texte de la raison.
      [rend: 1]
    ⑥ TRAITEMENT — Le clone public n'a pas de « .git » (le dossier jetable du pas « circuit à jour » d'un circuit
      public, le faux public d'une épreuve) : None, rien à comparer. Sinon : refus s'il n'est sur aucune branche,
      ou si sa branche n'est pas celle du dépôt privé (y compris un dépôt privé sans « .git » ou détaché : sa version
      n'a pas de nom).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 05-11-2026 à 13h36, « 2 » : les séries longues tournent sur GitHub AVANT la
      fusion. Le circuit reçoit une entrée « version en attente » ; le dépôt public reçoit le code de cette version sur
      une branche du même nom (« publier ce qui tourne », cadre du 08-10-2026, A-543) ; le contrôle d'identité compare
      à cette branche au lieu de main ; la barrière « séries conformes avant fusion » est gardée. Option 1 refusée
      (après la fusion, retour arrière si NON CONFORME) : une version non éprouvée par ses séries serait la version
      officielle pendant environ une heure, une baisse de contrôle. Cette fonction est la GARDE D'ENTRÉE du fabricant :
      il n'ÉCRIT pas la version « travail-x » dans un clone public sur une autre branche (refus). Elle ne dit rien de
      la POUSSÉE qui suit (relecture du 05-11-2026, M2 : une branche locale « travail-x » qui suit origin/main se
      pousse sur main) : la cible de la poussée est gardée par `publier` (option --publier) et par le crochet
      `poser_le_crochet`.
    ⑨ CE QUI CLOCHE — Un clone public SANS « .git » n'est pas contrôlé : c'est le cas du pas « circuit à jour » et des
      épreuves ; un Chat qui copierait à la main le résultat d'une fabrication sans « .git » dans un vrai clone
      contournerait la propriété. La branche est lue, pas le dépôt distant visé par la poussée qui suivra.
    ⑩ EFFET — Lance git en lecture (`branche_du_clone`).
    ⑪ TERMINAISON — Rend la main, ou lève (voir `branche_du_clone`).
      [sort: non]
    """
    git_public, b_public = branche_du_clone(public)
    if not git_public:
        return None
    _, b_prive = branche_du_clone(prive)
    if b_public is None:
        return "le clone public n'est sur aucune branche"
    if b_public != b_prive:
        return (f"le clone public est sur la branche « {b_public} », le dépôt privé sur « {b_prive or 'aucune branche'} » : "
                "une branche publique ne porte que le code de la version du même nom")
    return None


# LA POUSSÉE VERS LE PUBLIC, PAR CE PROGRAMME (superviseur R-759 du 05-11-2026, M2 : la relecture a montré, dans de vrais
# clones, qu'un « git push » ordinaire depuis une branche « travail-essai » qui suit origin/main, avec push.default
# upstream, ou « git push origin HEAD:main », écrit la version en attente sur main du public). La cible est une
# PROPRIÉTÉ : « refs/heads/<branche du dépôt privé> », écrite en clair, quel que soit le réglage du clone. Le crochet
# CROCHET_DE_POUSSEE, posé dans chaque clone public où ce programme écrit, refuse en plus toute poussée dont la
# référence distante n'est pas « refs/heads/<branche courante du clone> » ou dont le commit n'est pas HEAD (filet, pas
# la garde : il vit dans .git et ne se clone pas). TOUR 3, B-1 (superviseur R-759 du 05-11-2026, 17h13) : le crochet du
# tour 2 jugeait la forme écrite à gauche de la refspec ; `publier` pousse « HEAD:refs/heads/<b> », que git lui
# présente comme « HEAD » : il refusait TOUJOURS la publication que le même programme venait de préparer (relecture du
# tour 2, B-1, mesuré de bout en bout). La propriété porte maintenant sur la CIBLE et sur le COMMIT, quelle que soit
# l'écriture de la poussée.
CROCHET_DE_POUSSEE = """#!/bin/sh
# Posé par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (superviseur R-759 du 05-11-2026, M2). Simulation uniquement.
# Refuse toute poussée dont la référence distante n'est pas refs/heads/<branche courante du clone>, ou dont le commit
# poussé n'est pas HEAD. La forme écrite à gauche (« HEAD », « refs/heads/b ») ne compte pas (tour 3, B-1).
b=$(git symbolic-ref -q --short HEAD) || { echo "REFUS : le clone public n'est sur aucune branche"; exit 1; }
tete=$(git rev-parse HEAD) || { echo "REFUS : HEAD illisible"; exit 1; }
while read -r l_ref l_sha r_ref r_sha; do
  [ "$r_ref" = "refs/heads/$b" ] || { echo "REFUS : poussée vers $r_ref depuis la branche $b — une branche publique ne porte que la version du même nom"; exit 1; }
  [ "$l_sha" = "$tete" ] || { echo "REFUS : le commit poussé ($l_sha) n'est pas HEAD ($tete)"; exit 1; }
done
exit 0
"""


def poser_le_crochet(public):
    """Pose CROCHET_DE_POUSSEE dans un clone public qui a un .git ; rend son chemin, ou None.

    ① RÔLE — Le filet contre une poussée manuelle vers une autre branche publique que celle du même nom.
    ② CONTEXTE D'APPEL — `main`, après l'écriture au clone public.
    ③ ENTRÉE — `public` : le clone public.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin du crochet, ou None si `public` n'a pas de dossier .git (dossier de « circuit à
      jour » sur GitHub, épreuves).
        [rend: 1]
    ⑥ TRAITEMENT — écrit .git/hooks/pre-push, exécutable.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de CROCHET_DE_POUSSEE.
    ⑨ CE QUI CLOCHE — « git push --no-verify » le saute ; un .git en fichier (sous-module, worktree) n'est pas traité.
      La garde de fond est `publier`. Il admet « git push origin <b> » d'une branche <b> locale où la version en
      attente a été fusionnée dans un autre nom (BACKLOG, relecture du tour 2).
    ⑩ EFFET — Écrit un fichier dans .git/hooks.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    hooks = os.path.join(public, ".git", "hooks")
    if not os.path.isdir(os.path.join(public, ".git")):
        return None
    os.makedirs(hooks, exist_ok=True)
    chemin = os.path.join(hooks, "pre-push")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(CROCHET_DE_POUSSEE)
    os.chmod(chemin, 0o755)
    return chemin


def publier(prive, public, liste, sha_publie=None):
    """Commite ce que `main` a écrit ou retiré au clone public, et rien d'autre, et le pousse vers la branche du MÊME NOM.

    ① RÔLE — La seule poussée vers le dépôt public (le Chat ne fait plus « git push » au public).
    ② CONTEXTE D'APPEL — `main`, avec l'option --publier, après la fabrication.
    ③ ENTRÉE — `prive` : le clone privé ; `public` : le clone public, déjà écrit par `main` ; `liste` : les chemins
      (relatifs à la racine, séparés par « / ») que `main` a ÉCRITS ou RETIRÉS au clone public, rendus par `main` ;
      `sha_publie` (15-11-2026) : le commit dont les blobs ont été écrits (`extraire_le_commit`), ou None.
    ④ CONDITIONS D'ENTRÉE — `refus_de_branche(prive, public)` a rendu None ; les deux sont des dépôts git ; `liste`
      n'est pas recalculée ici, elle est CONFRONTÉE à l'état du clone.
    ⑤ SORTIE — DEUX valeurs : code et message ; code 0 publié (ou rien à publier), 1 refusé.
      [rend: 2]
    ⑥ TRAITEMENT — b = branche du privé (`branche_du_clone`), exigée non vide ; refus_de_branche revérifié ;
      (tour 4, M-b) « git add » des chemins de `liste` qui existent, « git rm --cached » de ceux qui n'existent plus
      (chemins lus mot pour mot, « --literal-pathspecs ») ; puis « git status --porcelain » (fichiers non suivis
      compris, un par un) ne doit rien montrer hors de `liste`, et « git diff --cached --name-only » doit être dans
      `liste` : sinon refus, code 1, RIEN de commité ni poussé, et le message NOMME les fichiers en trop ; commit
      s'il y a un changement (message : la branche et le commit du privé) ; puis
      « git push origin HEAD:refs/heads/<b> » — cible écrite en clair, jamais celle d'un réglage du clone ; enfin
      la pointe distante relue (« git ls-remote ») doit être HEAD.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026, M2 : « C'est la seule forme qui porte sur la PROPRIÉTÉ (la cible est
      égale à la branche du privé) au lieu d'un état local qu'un réglage (push.default upstream) ou un geste
      (HEAD:main) contourne. » Tour 4, M-b (superviseur R-759 du 05-11-2026, 18h56) : « Ce qui part au public = ce
      que `main` a écrit ou retiré, ni plus ni moins. » Mesuré par la relecture du tour 3 : avec « git add -A », un
      fichier égaré dans le clone public (une note portant un jeton, fictif, et tmp_essai/entete.txt) partait sur la
      branche publique, code 0. Le refus porte sur la LISTE, pas sur le contenu : un fichier égaré sans jeton est
      refusé aussi. Un .gitignore du clone public ne change rien : seuls des noms donnés sont ajoutés.
    ⑨ CE QUI CLOCHE — Le commit prend l'identité git du clone (aucune n'est imposée ici) : sans identité, refus. La
      poussée passe par le crochet posé par `main` (même propriété, vérifiée deux fois ; depuis le tour 3, B-1, le
      crochet juge la cible et le commit, et non la forme « HEAD » écrite ici). Jamais « --force » : une branche
      publique qui a divergé est refusée par git (cas X3 de l'épreuve du circuit des séries). Le contrôle de
      « git diff --cached » est une garde EN DOUBLE de « git status » (tout ce qui est indexé y paraît aussi) : son
      retrait seul ne fait rien tomber. Un refus laisse indexés les chemins de `liste` (rien n'est commité) ; un
      chemin de `liste` ignoré par un .gitignore du clone fait refuser « git add » (code 1, nommé par git).
    ⑩ EFFET — Commit et poussée au dépôt public.
    ⑪ TERMINAISON — Rend la main ; chaque appel git est borné à 300 s.
      [sort: non]
    """
    def git(*args):
        """Lance git dans le clone public ; rend le résultat de subprocess.run.

        ① RÔLE — Un appel git borné, toujours dans le clone public.
        ② CONTEXTE D'APPEL — `publier`, à chaque étape.
        ③ ENTRÉE — `args` : les arguments de git.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le subprocess.CompletedProcess (code, sortie, erreur).
          [rend: 1]
        ⑥ TRAITEMENT — « git -C <public> <args> », sortie capturée en texte.
        ⑦ UNITÉ — Secondes (la borne).
        ⑧ POURQUOI — Une seule écriture de l'appel (R-708) ; le clone public est toujours la cible.
        ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired, non rattrapé ici : `main` sort sur une trace.
        ⑩ EFFET — Ce que fait la commande git.
        ⑪ TERMINAISON — Rend la main ; 300 s au plus.
          [sort: non]
        """
        return subprocess.run(["git", "-C", public] + list(args), capture_output=True, text=True, timeout=300)

    _, b = branche_du_clone(prive)
    if not b or refus_de_branche(prive, public):
        return 1, "publication refusée : le dépôt privé n'est sur aucune branche, ou le clone public sur une autre"
    sha = subprocess.run(["git", "-C", prive, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=300).stdout.strip()
    if sha_publie is not None and sha != sha_publie:
        return 1, (f"publication refusée : le dépôt privé est à {sha[:12]}, le code écrit vient de {sha_publie[:12]} "
                   "(HEAD a bougé pendant la fabrication) ; RIEN n'est commité")
    presents = [c for c in liste if os.path.lexists(os.path.join(public, c))]
    absents = [c for c in liste if c not in presents]
    for etape in ((git("--literal-pathspecs", "add", "--", *presents) if presents else None),
                  (git("--literal-pathspecs", "rm", "-q", "--cached", "--ignore-unmatch", "--", *absents)
                   if absents else None)):
        if etape is not None and etape.returncode != 0:
            return 1, "git add refusé : " + etape.stderr.strip()[:200]
    permis = set(liste)
    etat = git("status", "--porcelain=v1", "-z", "--untracked-files=all")
    indexe = git("diff", "--cached", "--name-only", "--no-renames", "-z")
    if etat.returncode != 0 or indexe.returncode != 0:
        return 1, "état du clone public illisible : " + (etat.stderr or indexe.stderr).strip()[:200]
    vus, morceaux = [], etat.stdout.split("\0")
    while morceaux:
        m = morceaux.pop(0)
        if not m:
            continue
        vus.append(m[3:])
        if m[0] in "RC" and morceaux:   # renommage ou copie indexés : le chemin d'origine suit
            vus.append(morceaux.pop(0))
    vus += [c for c in indexe.stdout.split("\0") if c]
    en_trop = sorted(set(c for c in vus if c not in permis))
    if en_trop:
        return 1, (f"publication refusée : {len(en_trop)} fichier(s) du clone public hors de ce que le fabricant a "
                   "écrit ou retiré, RIEN n'est commité : " + " ".join(en_trop))
    if git("diff", "--cached", "--quiet").returncode != 0:
        c = git("commit", "-q", "-m", f"code publié de la version {b} du dépôt privé, commit {sha[:12]}")
        if c.returncode != 0:
            return 1, "commit refusé : " + (c.stderr or c.stdout).strip()[:200]
    cible = "refs/heads/" + b
    p = git("push", "-q", "origin", "HEAD:" + cible)
    if p.returncode != 0:
        return 1, f"poussée vers {cible} refusée : " + (p.stderr or p.stdout).strip()[:200]
    tete = git("rev-parse", "HEAD").stdout.strip()
    distante = git("ls-remote", "origin", cible).stdout.split()
    if not distante or distante[0] != tete:
        return 1, f"la pointe publique de {cible} n'est pas le commit poussé"
    return 0, f"publié : {cible} = {tete[:12]} (version {b} du dépôt privé, commit {sha[:12]})"


def main():
    """Vérifie, fabrique, écrit ; avec --publier, commite et pousse vers la branche publique du même nom (`publier`).

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Deux arguments : racine privée, clone public.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête. Depuis le tour 4 (M-b), chaque chemin écrit ou retiré au clone public est noté au
      moment même de l'écriture ou du retrait, et cette liste est donnée à `publier`, qui n'ajoute qu'elle.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Rend la main. [sort: oui]
      [sort: non]
    """
    if len(sys.argv) not in (3, 4) or (len(sys.argv) == 4 and sys.argv[3] != "--publier"):
        print("usage : FABRIQUER_LE_CIRCUIT_PUBLIC.py <racine du dépôt privé> <clone du dépôt public> [--publier]")
        return 1
    prive, public = sys.argv[1], sys.argv[2]
    if not os.path.lexists(os.path.join(prive, ".git")):
        return fabriquer_et_publier(prive, public, prive, None)
    extrait = tempfile.mkdtemp(prefix="commit_publie_")
    try:
        try:
            sha, _ = extraire_le_commit(prive, extrait)
        except (OSError, ValueError, subprocess.SubprocessError) as e:
            print("ARRÊT — le commit du dépôt privé n'a pas pu être extrait ; RIEN n'est écrit au dépôt public :", e)
            return 1
        print(f"source de la publication : le commit {sha[:12]} du dépôt privé (ses blobs, jamais le disque)")
        return fabriquer_et_publier(prive, public, extrait, sha)
    finally:
        shutil.rmtree(extrait, ignore_errors=True)


def fabriquer_et_publier(prive, public, source, sha):
    """Vérifie, fabrique, écrit ; avec --publier, commite et pousse ; rend le code de sortie.

    ① RÔLE — Le corps de `main`, une fois la source choisie.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `prive` : le dépôt privé (ses données, son historique, sa branche) · `public` : le clone public ·
      `source` : où LIRE ce qui se publie — le commit extrait par `extraire_le_commit` (dépôt privé avec git), ou le
      dépôt privé lui-même (sans git : une copie d'épreuve ; rien n'en peut être poussé, `refus_de_branche` refuse
      un clone public qui a un « .git ») · `sha` : le commit extrait, ou None.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête du programme.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête. Après l'écriture : le registre de provenance (`refus_selon_la_provenance`), l'étage A
      et le témoin du parcours (`refus_selon_l_historique`), les circuits que le relais compte écrits dans la même
      publication (R-D3), les permissions des circuits.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Livraison 1 du superviseur R-759 du 15-11-2026 (commentaire de `est_un_chemin_publie`).
    ⑨ CE QUI CLOCHE — Voir l'en-tête et `extraire_le_commit`, ⑨.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a_publier = code_a_publier(source)
    if not any(f.startswith("programmes/") for f in a_publier) or LANCEMENT not in a_publier:
        print("ARRÊT — le dépôt privé ne porte pas de programmes, ou pas", LANCEMENT)
        return 1
    fiches = fiches_a_publier(source)
    try:
        refus = refus_avant_publication(prive, a_publier + [FICHES_PRIVEES.replace(os.sep, "/") + "/" + f for f in fiches], source=source)
    except OSError as e:
        print("ARRÊT — le contrôle avant publication n'a pas pu tourner ; RIEN n'est écrit au dépôt public :", e)
        return 1
    if refus:
        print(f"ARRÊT — {len(refus)} fichier(s) ne peuvent pas aller au dépôt public ; RIEN n'y est écrit (défaut M5) :")
        for r in refus:
            print("  " + r)
        return 1
    try:
        texte = fabriquer_le_circuit(open(os.path.join(source, CIRCUIT_PRIVE), encoding="utf-8").read())
    except (OSError, ValueError) as e:
        print("ARRÊT — circuit public non fabriqué :", e)
        return 1
    if ERREUR_DE_LA_TABLE:
        print("ARRÊT — table des séries illisible (" + LANCEMENT + ", serie_du_circuit) ; RIEN n'est écrit :",
              ERREUR_DE_LA_TABLE)
        return 1
    try:
        verifier_les_gabarits_publics({"certification": CERTIFICATION, "series": SERIES, "relais": RELAIS,
                                       "epreuves": EPREUVES}, texte)
    except ValueError as e:
        print("ARRÊT — gabarit public refusé :", e)
        return 1
    try:
        refus = refus_de_branche(prive, public)
    except (OSError, subprocess.SubprocessError) as e:
        print("ARRÊT — la branche des deux dépôts n'a pas pu être lue ; RIEN n'est écrit au dépôt public :", e)
        return 1
    if refus:
        print("ARRÊT — " + refus + " ; RIEN n'est écrit au dépôt public")
        return 1
    for dossier in DOSSIERS_DE_CODE:
        os.makedirs(os.path.join(public, dossier), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.join(public, CIRCUIT_PUBLIC)), exist_ok=True)
    ecrits = []   # tour 4, M-b : chaque chemin écrit ou retiré au clone public, noté au geste même
    for f in a_publier:
        shutil.copyfile(os.path.join(source, f), os.path.join(public, f))
        ecrits.append(f)
    os.makedirs(os.path.join(public, FICHES_PUBLIEES), exist_ok=True)
    for f in fiches:
        shutil.copyfile(os.path.join(source, FICHES_PRIVEES, f), os.path.join(public, FICHES_PUBLIEES, f))
        ecrits.append(_chemin(FICHES_PUBLIEES, f))
    fiches_retirees = sorted(f for f in os.listdir(os.path.join(public, FICHES_PUBLIEES)) if f not in fiches)
    for f in fiches_retirees:
        os.remove(os.path.join(public, FICHES_PUBLIEES, f))
        ecrits.append(_chemin(FICHES_PUBLIEES, f))
    retires = sorted(_chemin(d, f) for d in DOSSIERS_DE_CODE for f in os.listdir(os.path.join(public, d))
                     if f.endswith(".py") and os.path.isfile(os.path.join(public, d, f)) and _chemin(d, f) not in a_publier)
    for f in retires:
        os.remove(os.path.join(public, f))
        ecrits.append(f)
    for chemin, contenu in ((CIRCUIT_PUBLIC, texte), (CIRCUIT_CERTIFICATION, CERTIFICATION), (CIRCUIT_SERIES, SERIES),
                             (CIRCUIT_RELAIS, RELAIS), (CIRCUIT_EPREUVES, EPREUVES)):
        with open(os.path.join(public, chemin), "w", encoding="utf-8") as s:
            s.write(contenu)
        ecrits.append(chemin.replace(os.sep, "/"))
    print(f"{len(a_publier)} fichiers de code copiés · {len(retires)} retiré(s) {' '.join(retires)}".rstrip())
    print(f"{len(fiches)} fiches de circuit du privé copiées dans {FICHES_PUBLIEES}/ · {len(fiches_retirees)} retirée(s) "
          f"{' '.join(fiches_retirees)}".rstrip())
    print(f"circuit fabriqué : {CIRCUIT_PUBLIC} ({len(texte.splitlines())} lignes)")
    print(f"circuit fabriqué : {CIRCUIT_CERTIFICATION} ({len(CERTIFICATION.splitlines())} lignes)")
    print(f"circuit fabriqué : {CIRCUIT_SERIES} ({len(SERIES.splitlines())} lignes)")
    print(f"circuit fabriqué : {CIRCUIT_RELAIS} ({len(RELAIS.splitlines())} lignes)")
    print(f"circuit fabriqué : {CIRCUIT_EPREUVES} ({len(EPREUVES.splitlines())} lignes)")
    try:
        refus, note = refus_selon_la_provenance(prive, public, ecrits)
    except (OSError, ValueError) as e:
        print("ARRÊT — le contrôle des fichiers écrits au public (registre de provenance) n'a pas pu tourner ; RIEN n'est "
              "publié :", e)
        return 1
    print(note)
    if refus:
        print(f"ARRÊT — {len(refus)} fichier(s) écrit(s) au clone public ne sont pas publiables ; RIEN n'est publié :")
        for r in refus:
            print("  " + r)
        return 1
    try:
        refus, note = refus_selon_l_historique(prive, public, ecrits, exclus=(public, source))
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        print("ARRÊT — l'étage A ou le témoin du parcours n'a pas pu tourner ; RIEN n'est publié :", e)
        return 1
    print(note)
    if refus:
        print(f"ARRÊT — {len(refus)} fichier(s) écrit(s) au clone public sont des fichiers du dépôt privé qui ne se "
              "publient pas ; RIEN n'est publié :")
        for r in refus:
            print("  " + r)
        return 1
    # R-D3 (relecteur du 15-11-2026) : chaque circuit que le relais lance ou compte est écrit dans la MÊME publication
    # que lui ; sinon GitHub ne le connaîtrait pas, et le relais refuserait toute demande du groupe.
    absents = circuits_du_relais_non_ecrits(ecrits)
    if absents:
        print("ARRÊT — le relais compte ou lance des circuits que cette publication n'écrit pas ; RIEN n'est publié :",
              " ".join(absents))
        return 1
    refus = refus_des_circuits_publies(public)
    if refus:
        print(f"ARRÊT — {len(refus)} circuit(s) du clone public portent la permission de lancer sans être le relais "
              "fabriqué ; RIEN n'est publié :")
        for r in refus:
            print("  " + r)
        return 1
    if poser_le_crochet(public):
        print("crochet de poussée posé au clone public (une branche ne se pousse que vers la branche du même nom)")
    if len(sys.argv) == 4:
        code, message = publier(prive, public, ecrits, sha)
        print(("" if code == 0 else "ARRÊT — ") + message)
        return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
