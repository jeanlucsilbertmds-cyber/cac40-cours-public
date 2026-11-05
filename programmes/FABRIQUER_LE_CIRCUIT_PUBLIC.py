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
  fichier). Sinon : arrêt, code 1, RIEN n'est écrit.
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
  `.github/workflows/circuit_du_soir.yml` et `.github/workflows/certifier_la_version.yml` ;
  et `circuits_du_prive/*.yml` ; RETIRE du clone public, à ces emplacements, ce qui
  est absent du dépôt privé. Ne pousse rien.
⑪ TERMINAISON — Rend la main. Aucun appel qui puisse ne pas revenir. [sort: oui]
⑫ DÉFINITIONS
  le circuit du soir : la suite de programmes lancés chaque soir de bourse par
    GitHub Actions — collecte des cours, versement, signaux, positions, mesure,
    pilote, radar.
  le dépôt privé : `jeanlucsilbertmds-cyber/Cac-40-signals-sur-git-hub-pour-Claude-`.
  le dépôt public : `jeanlucsilbertmds-cyber/cac40-cours-public`.
"""
import importlib.util
import os
import re
import shutil
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


def pas_de_depot(apres_echec, chemins, avant):
    """Rend le pas qui pousse au dépôt privé ce qu'une tâche de la certification a écrit.

    ① RÔLE — Écrire une fois le dépôt au privé (R-708), pour les tranches et pour la tâche finale.
    ② CONTEXTE D'APPEL — Le gabarit CERTIFICATION, deux fois.
    ③ ENTRÉE — `apres_echec` : le message d'erreur si rien n'est à ajouter · `chemins` : les chemins à ajouter,
      séparés par une espace · `avant` : des lignes de commande jouées avant l'ajout (indentées de dix espaces).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte du pas, au format du fichier de circuit.
      [rend: 1]
    ⑥ TRAITEMENT — identité `certification-publique` (programmes/MESSAGE_DU_SOIR.py la cherche dans l'historique),
      `avant`, ajout, commit, puis `ESSAIS_DE_POUSSEE` essais : chacun abandonne d'abord un rebasage resté en plan
      par l'essai précédent, reprend le dépôt et pousse ; après chaque essai refusé, le dernier compris, une attente
      tirée au hasard de 1 à 15 s (jusqu'à 15 s perdues avant le message d'erreur).
    ⑦ UNITÉ — Des secondes (l'attente entre deux essais).
    ⑧ POURQUOI — Les tranches poussent leur certificat partiel au dépôt privé, où la tâche finale le lit : les
      archives jointes d'un passage public sont téléchargeables par tous (fiche du programme, ⑥ ③).
    ⑨ CE QUI CLOCHE — Les tranches qui finissent à la même seconde se disputent la poussée. Un essai d'une tranche ne
      peut échouer que si un autre écrivain a réussi entre sa lecture et sa poussée : une tranche échoue au plus
      (tranches − 1) + (poussées étrangères pendant la fenêtre) fois — c'est ce que couvre `ESSAIS_DE_POUSSEE`, et non
      le hasard. L'attente au hasard ne fait qu'accélérer : à pas fixe, les essais restent synchronisés et il n'y a
      qu'un gagnant par tour (mesuré par le superviseur R-759 du 31-10-2026). Plus de poussées étrangères que la marge
      pendant la fenêtre : une tranche peut encore échouer, et la réunion rougit (« certificat partiel absent »).
      L'abandon du rebasage dans la boucle n'a pas été vu servir : les fichiers des tranches sont distincts, aucun
      conflit n'a été observé (THÉORIQUE). La loi ne compte que les échecs dus à la concurrence : une erreur passagère
      du réseau ou de GitHub consomme aussi un essai.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return ("""      - name: Deposer au depot prive
        id: deposer
        if: always()
        shell: bash
        run: |
          git config user.name certification-publique
          git config user.email certification-publique@users.noreply.github.com
""" + avant + "          git add " + chemins + """ \\
            || { echo \"::error::""" + apres_echec + """\"; exit 1; }
          if git diff --cached --quiet; then echo "rien a deposer"; exit 0; fi
          git commit -q -m "certificat de la version, passage public ${GITHUB_RUN_ID} [skip ci]"
          for i in $(seq 1 """ + str(ESSAIS_DE_POUSSEE) + """); do
            git rebase --abort 2>/dev/null || true
            if git pull -q --rebase --autostash origin main && git push -q; then echo "depose"; exit 0; fi
            sleep $((RANDOM % 15 + 1))
          done
          echo "::error::POUSSEE REFUSEE """ + str(ESSAIS_DE_POUSSEE) + """ FOIS — le certificat reste sur la machine jetable"; exit 1
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
                          (r"GITHUB_STEP_SUMMARY", "le résumé public du passage")):
        if re.search(motif, corps_prive, re.M):
            raise ValueError(f"le circuit privé porte {raison}")
    return texte


def main():
    """Vérifie, fabrique, écrit.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Deux arguments : racine privée, clone public.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Rend la main. [sort: oui]
      [sort: non]
    """
    if len(sys.argv) != 3:
        print("usage : FABRIQUER_LE_CIRCUIT_PUBLIC.py <racine du dépôt privé> <clone du dépôt public>")
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
    for dossier in DOSSIERS_DE_CODE:
        os.makedirs(os.path.join(public, dossier), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.join(public, CIRCUIT_PUBLIC)), exist_ok=True)
    for f in a_publier:
        shutil.copyfile(os.path.join(prive, f), os.path.join(public, f))
    os.makedirs(os.path.join(public, FICHES_PUBLIEES), exist_ok=True)
    for f in fiches:
        shutil.copyfile(os.path.join(prive, FICHES_PRIVEES, f), os.path.join(public, FICHES_PUBLIEES, f))
    fiches_retirees = sorted(f for f in os.listdir(os.path.join(public, FICHES_PUBLIEES)) if f not in fiches)
    for f in fiches_retirees:
        os.remove(os.path.join(public, FICHES_PUBLIEES, f))
    retires = sorted(_chemin(d, f) for d in DOSSIERS_DE_CODE for f in os.listdir(os.path.join(public, d))
                     if f.endswith(".py") and os.path.isfile(os.path.join(public, d, f)) and _chemin(d, f) not in a_publier)
    for f in retires:
        os.remove(os.path.join(public, f))
    with open(os.path.join(public, CIRCUIT_PUBLIC), "w", encoding="utf-8") as s:
        s.write(texte)
    with open(os.path.join(public, CIRCUIT_CERTIFICATION), "w", encoding="utf-8") as s:
        s.write(CERTIFICATION)
    print(f"{len(a_publier)} fichiers de code copiés · {len(retires)} retiré(s) {' '.join(retires)}".rstrip())
    print(f"{len(fiches)} fiches de circuit du privé copiées dans {FICHES_PUBLIEES}/ · {len(fiches_retirees)} retirée(s) "
          f"{' '.join(fiches_retirees)}".rstrip())
    print(f"circuit fabriqué : {CIRCUIT_PUBLIC} ({len(texte.splitlines())} lignes)")
    print(f"circuit fabriqué : {CIRCUIT_CERTIFICATION} ({len(CERTIFICATION.splitlines())} lignes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
