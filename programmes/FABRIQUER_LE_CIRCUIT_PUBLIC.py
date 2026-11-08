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
  montre.
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
import hashlib
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
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


def refus_avant_publication(prive, chemins):
    """Rend les raisons de refuser la publication : liens, chemins réels hors du dépôt, liens durs, texte non strict, jetons.

    ① RÔLE — Dire, AVANT que rien ne soit écrit au dépôt public, si un des fichiers que le fabricant s'apprête à
      publier est un lien symbolique, a un chemin réel qui n'est pas son chemin dans le dépôt privé (un dossier lié,
      une cible hors du dépôt), est un lien dur (le même fichier porte un autre nom, peut-être hors du dépôt), n'est
      pas du TEXTE UTF-8 STRICT (de l'UTF-8 valide sans aucun caractère de contrôle, catégorie Unicode Cc, hors
      tabulation et sauts de ligne), ou porte une chaîne de la forme d'un jeton (programmes/FORME_D_UN_JETON.py). Un seul
      contrôle pour les deux familles publiées : le code (`code_a_publier`) et les fiches de circuit
      (`fiches_a_publier`).
    ② CONTEXTE D'APPEL — `main`, une fois, juste après avoir dressé les deux listes et avant de fabriquer ou d'écrire
      quoi que ce soit ; les épreuves du circuit public (E8 de tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py).
    ③ ENTRÉE — `prive` : la racine du dépôt privé · `chemins` : les chemins des fichiers à publier, relatifs à cette
      racine, séparés par « / » (« programmes/X.py », « .github/workflows/collecte_abc.yml »).
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
      puis s'il porte la forme d'un jeton. Le contenu d'un fichier refusé en ①, ② ou ③ n'est jamais lu : on ne lit pas, même en mémoire, un fichier qui peut être hors du dépôt.
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
      FOND » le texte strict (0 refus mesuré sur les 144 fichiers que publie le fabricant).
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
      entre `os.path.realpath` et l'ouverture n'est pas vu. Le remède jugé de fond (lire une fois avec O_NOFOLLOW et
      écrire CES octets, ou publier les blobs commités) est proposé au BACKLOG. · CÔTÉ PUBLIC, rien n'est contrôlé :
      si `circuits_du_prive/` du clone public est un lien vers `.github/workflows/`, les fiches du privé y sont
      écrites et GitHub les MET EN SERVICE au dépôt public, avec ses secrets (relecture du 04-11-2026, D6, cas P1 :
      les sept fiches du privé arrivées dans `.github/workflows/` du public, fabricant au code 0) ; il faut pour cela
      un lien commité au dépôt public, que seul ce circuit écrit. La propriété « tout chemin écrit ou effacé au public
      a pour chemin réel la racine réelle du public suivie du chemin » est proposée au BACKLOG.
    ⑩ EFFET — Lit les fichiers non refusés en ①, ② et ③, et charge programmes/FORME_D_UN_JETON.py. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; des lectures de fichiers locaux, aucun appel qui puisse ne pas revenir.
      [sort: non]
    """
    forme = forme_d_un_jeton()
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
INSTALLER_LA_MESURE = """      - name: Installer la mesure et les dependances des programmes
        id: installer
        run: python3 -m pip install --quiet "coverage==7.16.2" "pyflakes==4.1.0" cryptography pyyaml
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
# page ne dit pas si le total couvre le compte entier (dépôts privé et public) : je ne sais pas ; 4 places restent
# libres. Il ne règle que la matrice (« max-parallel ») : une part pousse UNE fois, sur une branche à elle.
PARTS_EN_MEME_TEMPS = 16
SERIES_IDENTITE = "series-longues-publiques"
# LES BRANCHES DES SÉRIES (superviseur R-759 du 04-11-2026, R1, « RUSTINE, À REPRENDRE » de l'archive jointe et de la
# garde d'horaire). Chaque job pousse UNE fois sur SA branche neuve du dépôt privé, jamais sur main :
#   series-longues/<passage>/<série>/part_<n>  (une part)   et   series-longues/<passage>/<série>/releve  (le relevé).
# Pourquoi : (1) une archive jointe d'un dépôt public est téléchargeable par tout compte GitHub connecté (documentation
# GitHub citée par le superviseur), or une part porte les écoutes (les chemins lus) et etat_du_depart.json (les noms de
# tous les fichiers du privé) ; (2) 20 parts qui poussaient sur main ont fait refuser 3 fois la collecte du soir, une
# fois sur trois (relecture du 04-11-2026, I1, course locale) ; une référence neuve n'a aucun concurrent : mesuré par
# le superviseur, 20 parts sur 20 et la collecte au premier essai, cinq fois sur cinq (course_branches.log), contre 1 à
# 2 parts sur 20 au premier essai sur main (course_contre_epreuve_main.log). Le préfixe ne commence JAMAIS par
# « travail- » : ce nom est réservé à l'unique version en attente que cherche le « check » (A-448).
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
#   ② si c'est une version en attente, c'est la SEULE branche « travail-… » du dépôt privé (A-448 : jamais plus d'une
#     version en attente à la fois) ;
#   ③ le clone du privé est la POINTE actuelle de cette branche au dépôt privé : le sha noté ensuite par « Fabriquer la
#     matrice », que clonent les parts, est donc celui de la version demandée.
# Les valeurs viennent de l'environnement du pas, jamais recopiées dans le script : une entrée « inputs. » écrite en
# clair dans un script de shell y serait exécutée.
# La forme d'une version : la version officielle ou la version en attente (A-448). Écrite UNE fois, lue par la porte du
# circuit des séries (SERIES_VERSION) et par le relais (RELAIS) : deux écritures d'une même chose divergent (R-708).
MOTIF_DE_VERSION = "^(main|travail-[A-Za-z0-9._-]+)$"
SERIES_VERSION = """      - name: La version demandee est-elle celle de cette branche publique ?
        id: version
        shell: bash
        env:
""" + JETON_DU_PAS + """          VERSION: ${{ inputs.version }}
          BRANCHE_PUBLIQUE: ${{ github.ref_name }}
        run: |
          set -o pipefail
""" + SANS_RIEN_DE_LA_VERSION + AUTORISATION + """          cd "$T"
          [[ "$VERSION" =~ """ + MOTIF_DE_VERSION + """ ]] || { echo "::error::version refusee : $VERSION (main, ou une version en attente travail-...)"; exit 1; }
          [ "$VERSION" = "$BRANCHE_PUBLIQUE" ] || { echo "::error::la version $VERSION n'est pas la branche publique lancee ($BRANCHE_PUBLIQUE) : lancer ce circuit depuis la branche publique $VERSION"; exit 1; }
          tetes=$(git "${A[@]}" ls-remote --heads "$PRIVE") || { echo "::error::branches du depot prive illisibles"; exit 1; }
          if [ "$VERSION" != "main" ]; then
            attente=$(printf '%s\\n' "$tetes" | cut -f2 | grep '^refs/heads/travail-' || true)
            [ "$attente" = "refs/heads/$VERSION" ] || { echo "::error::la version en attente du depot prive n'est pas exactement $VERSION : $(printf '%s' "$attente" | tr '\\n' ' ')"; exit 1; }
          fi
          pointe=$(printf '%s\\n' "$tetes" | awk -v r="refs/heads/$VERSION" '$2 == r { print $1 }')
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
SERIES_AU_PLUS = 4                  # 2 + 2 × 4 = 10 entrées du bouton : la limite de GitHub lue le 05-11-2026 est 10


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
# pas la branche publique lancée, si elle n'est pas l'unique version en attente du dépôt privé, ou si le clone n'est
# pas sa pointe ; chaque job compare ensuite le code publié de cette branche à celui de la version, octet pour octet.
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
%(entrees)sconcurrency:
  group: series-longues
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
            [[ "${!vp}" =~ ^[1-9][0-9]?$ ]] || echec "nombre refuse pour $vp : ${!vp} (1 a 99)"
            [[ "${!vl}" =~ ^[1-9][0-9]?$ ]] || echec "nombre refuse pour $vl : ${!vl} (1 a 99)"
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
    "branches": SERIES_BRANCHES,
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
# écrit au journal ce qui aurait été lancé, et ne lance rien. Exemple :
#   serie=Yahoo
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
CIRCUITS_DU_RELAIS = (("series", os.path.basename(CIRCUIT_SERIES), MOTIF_DE_VERSION),
                      ("examen", os.path.basename(CIRCUIT_CERTIFICATION), "^main$"))
TAILLE_DE_DEMANDE = 1000          # octets au plus


def _relais_par_serie(modele):
    """Rend `modele` répété pour chaque série de la table, %(c)s = le code, %(m)s = minuscules, %(M)s = majuscules,
    %(n)s et %(l)s = machines et lot par défaut, %(t)s = TOUTES.

    ① RÔLE — Fabriquer une ligne du relais par série, toutes depuis la même boucle.
    ② CONTEXTE D'APPEL — La construction de RELAIS, quatre fois.
    ③ ENTRÉE — `modele` : un texte à clés %(…)s.
    ④ CONDITIONS D'ENTRÉE — SERIES_DU_CIRCUIT est lue.
    ⑤ SORTIE — UNE valeur : le texte. [rend: 1]
    ⑥ TRAITEMENT — une copie de `modele` par série, dans l'ordre de la table, mises bout à bout.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision n°309 (tout est fabriqué depuis la table) ; un même modèle pour les quatre usages : un code
      ne peut pas recevoir la valeur d'un autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
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
# sur CETTE branche, version = nom de la branche, chaque valeur passée explicitement (celles absentes de la demande
# prennent la valeur de la table).
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
          [[ "$BRANCHE" =~ """ + MOTIF_DE_VERSION + """ ]] || { echo "::error::DEMANDE REFUSEE : branche $BRANCHE (main, ou une version en attente travail-...)"; exit 1; }
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
          A_BLANC="non"
""" + _relais_par_serie("""          PARTS_%(M)s=%(n)d
          LOT_%(M)s=%(l)d
""") + """          while IFS= read -r ligne || [ -n "$ligne" ]; do
            [ -n "$ligne" ] && [[ "$ligne" != "#"* ]] || continue
            [[ "$ligne" =~ ^([a-z_]{1,20})=([A-Za-z0-9]{1,20})$ ]] || { echo "::error::DEMANDE REFUSEE : ligne illisible (cle=valeur, lettres et chiffres, sans espace) : ${ligne:0:80}"; exit 1; }
            cle="${BASH_REMATCH[1]}"
            valeur="${BASH_REMATCH[2]}"
            [[ "$vus" != *" $cle "* ]] || { echo "::error::DEMANDE REFUSEE : cle donnee deux fois : $cle"; exit 1; }
            vus="$vus$cle "
            if [ "$cle" = "circuit" ]; then
              [[ "$valeur" =~ ^(""" + "|".join(c[0] for c in CIRCUITS_DU_RELAIS) + """)$ ]] || { echo "::error::DEMANDE REFUSEE : circuit inconnu : $valeur"; exit 1; }
              CIRCUIT="$valeur"
            elif [ "$cle" = "serie" ]; then
              [[ "$valeur" =~ ^(""" + "|".join([TOUTES] + [s[0] for s in SERIES_DU_CIRCUIT]) + """)$ ]] || { echo "::error::DEMANDE REFUSEE : serie inconnue : $valeur"; exit 1; }
              SERIE="$valeur"
            elif [ "$cle" = "a_blanc" ]; then
              [[ "$valeur" =~ ^(oui|non)$ ]] || { echo "::error::DEMANDE REFUSEE : a_blanc vaut oui ou non : $valeur"; exit 1; }
              A_BLANC="$valeur"
""" + _relais_par_serie("""            elif [ "$cle" = "parts_%(m)s" ]; then
              [[ "$valeur" =~ ^[1-9][0-9]?$ ]] || { echo "::error::DEMANDE REFUSEE : parts_%(m)s de 1 a 99 : $valeur"; exit 1; }
              PARTS_%(M)s="$valeur"
            elif [ "$cle" = "lot_%(m)s" ]; then
              [[ "$valeur" =~ ^[1-9][0-9]?$ ]] || { echo "::error::DEMANDE REFUSEE : lot_%(m)s de 1 a 99 : $valeur"; exit 1; }
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
            [[ "$BRANCHE" =~ %s ]] || { echo "::error::DEMANDE REFUSEE : le circuit %s ne se lance pas depuis la branche $BRANCHE"; exit 1; }
          fi
""" % (c, f, m, c) for c, f, m in CIRCUITS_DU_RELAIS) + """          [ -n "$FICHIER" ] || { echo "::error::DEMANDE REFUSEE : circuit sans fichier : $CIRCUIT"; exit 1; }
          if [ "$CIRCUIT" != "series" ]; then
            [ "$vus" = " circuit " ] || [ "$vus" = " circuit a_blanc " ] || [ "$vus" = " a_blanc circuit " ] || { echo "::error::DEMANDE REFUSEE : le circuit $CIRCUIT ne prend aucun reglage (seulement circuit et a_blanc) :$vus"; exit 1; }
          fi
          [ "$CIRCUIT" != "series" ] || [ -n "$SERIE" ] || { echo "::error::DEMANDE REFUSEE : la cle serie manque"; exit 1; }
""" + _relais_par_serie("""          if [[ "$vus" == *" parts_%(m)s "* || "$vus" == *" lot_%(m)s "* ]] && [ "$SERIE" != "%(t)s" ] && [ "$SERIE" != "%(c)s" ]; then
            echo "::error::DEMANDE REFUSEE : elle regle la serie %(c)s, qu'elle ne joue pas (serie $SERIE)"
            exit 1
          fi
""") + """          en_cours=$(gh run list --workflow "$FICHIER" --limit 100 --json status --jq '[.[] | select(.status != "completed")] | length') || { echo "::error::DEMANDE REFUSEE : passages de $FICHIER illisibles"; exit 1; }
          [ "$en_cours" = "0" ] || { echo "::error::DEMANDE REFUSEE : $en_cours passage(s) de $FICHIER en cours ou en attente ; redeposer la demande quand ils sont finis"; exit 1; }
          echo "demande $fichier : circuit $CIRCUIT ($FICHIER) ; version $BRANCHE ; serie $SERIE""" + _relais_par_serie(" ; parts_%(m)s $PARTS_%(M)s ; lot_%(m)s $LOT_%(M)s") + """ ; a blanc $A_BLANC"
          if [ "$A_BLANC" = "oui" ]; then
            echo "A BLANC : rien n'est lance"
            exit 0
          fi
          if [ "$CIRCUIT" != "series" ]; then
            gh workflow run "$FICHIER" --ref "$BRANCHE" || { echo "::error::le circuit $FICHIER n'a pas pu etre lance"; exit 1; }
            echo "LANCE : $FICHIER sur $BRANCHE"
            exit 0
          fi
          gh workflow run "$FICHIER" --ref "$BRANCHE" -f "version=$BRANCHE" -f "serie=$SERIE\"""" + _relais_par_serie(""" -f "parts_%(m)s=$PARTS_%(M)s" -f "lot_%(m)s=$LOT_%(M)s\"""") + """ || { echo "::error::le circuit des series n'a pas pu etre lance"; exit 1; }
          echo "LANCE : $FICHIER sur $BRANCHE"
"""
if ERREUR_DE_LA_TABLE:
    SERIES = RELAIS = None


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
BRANCHES_DES_GABARITS = {"series": SERIES_BRANCHES}
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
      ne porte la souche du nom d'une épreuve de série de la table (`souches_des_epreuves`).
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
    ⑤ SORTIE — UNE valeur : la liste des souches. [rend: 1]
    ⑥ TRAITEMENT — le nom du fichier sans « .py », sans le préfixe « EPREUVES_ » suivi de « DE_L_ », « DE_LA_ »,
      « DES_ », « DU_ » ou « DE_ », et sans la date finale « _Jjj_JJ-MM-AAAA ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le pas « Fabriquer la matrice » d'avant le 08-11-2026 cherchait l'épreuve par ces souches
      (« HISTORIQUE_LONG », « COURS_PROPRE_DE_YAHOO ») : un gabarit qui les porte de nouveau a un lien tapé à la main.
      Propriété et non liste : une série ajoutée à la table est couverte sans rien déclarer.
    ⑨ CE QUI CLOCHE — Un morceau plus court de la souche (« LONG ») n'est pas vu.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
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
    ⑤ SORTIE — Aucune valeur ; lève ValueError si l'empreinte diffère. [rend: rien]
    ⑥ TRAITEMENT — sha256 du texte en UTF-8, comparé à EMPREINTE_DU_RELAIS.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Commentaire de EMPREINTE_DU_RELAIS : une propriété (« c'est le texte fabriqué ») au lieu d'une
      énumération de commandes, qui laissait chaque tour trouver une nouvelle porte.
    ⑨ CE QUI CLOCHE — Ce contrôle ne dit rien du gabarit RELAIS lui-même : sa sûreté repose sur sa relecture (une
      fois, puis à chaque changement de son texte). Il ne protège pas un relais modifié À LA MAIN au dépôt public sans
      passer par ce programme : celui-là tournerait avant tout contrôle ; seul le pas « circuit_a_jour » du circuit des
      séries le verrait, après coup.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    vue = hashlib.sha256(texte.encode("utf-8")).hexdigest()
    if EMPREINTE_DU_RELAIS is None or vue != EMPREINTE_DU_RELAIS:
        raise ValueError(f"relais {nom} : il porte la permission de lancer un circuit et n'est pas, octet pour octet, le "
                         f"relais fabriqué (empreinte {vue[:16]}, attendue {(EMPREINTE_DU_RELAIS or '?')[:16]})")


def refus_des_circuits_publies(public):
    """Rend la liste des circuits du clone public qui portent la permission de lancer sans être le relais fabriqué.

    ① RÔLE — Garder la permission « actions: write » dans le SEUL relais, dans tous les circuits publiés.
    ② CONTEXTE D'APPEL — `main`, après l'écriture des circuits et avant toute publication ; l'épreuve du relais.
    ③ ENTRÉE — `public` : le clone public.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des refus (texte), vide si tout va. [rend: 1]
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
    ⑪ TERMINAISON — Rend la main. [sort: non]
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


def publier(prive, public, liste):
    """Commite ce que `main` a écrit ou retiré au clone public, et rien d'autre, et le pousse vers la branche du MÊME NOM.

    ① RÔLE — La seule poussée vers le dépôt public (le Chat ne fait plus « git push » au public).
    ② CONTEXTE D'APPEL — `main`, avec l'option --publier, après la fabrication.
    ③ ENTRÉE — `prive` : le clone privé ; `public` : le clone public, déjà écrit par `main` ; `liste` : les chemins
      (relatifs à la racine, séparés par « / ») que `main` a ÉCRITS ou RETIRÉS au clone public, rendus par `main`.
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
    a_publier = code_a_publier(prive)
    if not any(f.startswith("programmes/") for f in a_publier) or LANCEMENT not in a_publier:
        print("ARRÊT — le dépôt privé ne porte pas de programmes, ou pas", LANCEMENT)
        return 1
    fiches = fiches_a_publier(prive)
    try:
        refus = refus_avant_publication(prive, a_publier + [FICHES_PRIVEES.replace(os.sep, "/") + "/" + f for f in fiches])
    except OSError as e:
        print("ARRÊT — le contrôle avant publication n'a pas pu tourner ; RIEN n'est écrit au dépôt public :", e)
        return 1
    if refus:
        print(f"ARRÊT — {len(refus)} fichier(s) ne peuvent pas aller au dépôt public ; RIEN n'y est écrit (défaut M5) :")
        for r in refus:
            print("  " + r)
        return 1
    try:
        texte = fabriquer_le_circuit(open(os.path.join(prive, CIRCUIT_PRIVE), encoding="utf-8").read())
    except (OSError, ValueError) as e:
        print("ARRÊT — circuit public non fabriqué :", e)
        return 1
    if ERREUR_DE_LA_TABLE:
        print("ARRÊT — table des séries illisible (" + LANCEMENT + ", serie_du_circuit) ; RIEN n'est écrit :",
              ERREUR_DE_LA_TABLE)
        return 1
    try:
        verifier_les_gabarits_publics({"certification": CERTIFICATION, "series": SERIES, "relais": RELAIS}, texte)
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
        shutil.copyfile(os.path.join(prive, f), os.path.join(public, f))
        ecrits.append(f)
    os.makedirs(os.path.join(public, FICHES_PUBLIEES), exist_ok=True)
    for f in fiches:
        shutil.copyfile(os.path.join(prive, FICHES_PRIVEES, f), os.path.join(public, FICHES_PUBLIEES, f))
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
                             (CIRCUIT_RELAIS, RELAIS)):
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
        code, message = publier(prive, public, ecrits)
        print(("" if code == 0 else "ARRÊT — ") + message)
        return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
