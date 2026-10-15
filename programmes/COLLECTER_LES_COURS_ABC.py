#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COLLECTER_LES_COURS_ABC.py — Jeu 10-09-2026 (Paris)
FABRIQUÉ · Rôle : lire les cours du jour sur ABC Bourse pour les 40 valeurs du
référentiel, les convertir au format du fichier des cours, et les EMPILER —
jamais écraser — après contrôle de vraisemblance.

POURQUOI CE PROGRAMME EXISTE (décision de Jean-Luc, 10-09-2026, A-391) :
  Google Sheets ne fournit plus les cours. Le 08-09, trois feuilles sur quatre se
  sont vidées ; le 10-09 à 08h36 la boucle a constaté que même la quatrième
  s'arrêtait à la veille. ABC Bourse, source Six Financial Information, porte la
  clôture du jour dès ~17h55 pour Paris, identique au centime à Google sur les
  séances comparées (A-388).

CE QUE CE PROGRAMME NE FAIT PAS, ET C'EST VOULU (R-708 : jamais réimplémenter) :
  · il ne normalise pas les noms ni les dates — CONTROLER_LES_COURS le fait
  · il ne contrôle pas la vraisemblance — CONTROLER_LES_COURS le fait
  · il n'écrit pas au fichier — CONTROLER_LES_COURS.ajouter_au_fichier le fait
  · il ne calcule aucun signal, ne touche pas cac40_ohlcv.csv, ne supprime rien
  Son seul rôle : LIRE la page, EXTRAIRE le tableau, CONVERTIR le format.

LE CODE ABC SE DÉDUIT DU RÉFÉRENTIEL, aucune table nouvelle (vérifié 11/11 le
10-09) : code = mnémonique Euronext + 'p' (Paris) ou 'n' (Amsterdam).

PIÈGE MESURÉ LE 10-09 : pour Amsterdam (ArcelorMittal, MTn), la ligne la plus
récente peut être PARTIELLE — horodatage 11h43, volume cinq fois trop faible. On
l'écarte toujours. CONSÉQUENCE ACTÉE : ArcelorMittal n'a jamais sa séance du jour,
seulement J-1 — et une séance non lue le jour même perd ses signaux pour toujours.
ARCELORMITTAL EST DONC, PAR CONSTRUCTION, HORS DU DISPOSITIF DE SIGNAUX. Ses cours
sont collectés pour l'historique et les comparaisons, pas pour trader.

LE VRAI CONTRAT D'ENTRÉE EST LE PROMPT DONNÉ À L'OUTIL WEB PAR LA TÂCHE (Cowork,
10-09). Il décide de la forme du rendu et doit être FIXÉ MOT POUR MOT dans le prompt
de la tâche. Celui qui a donné 30 lignes sur 30 le 10-09 à 14h15 :
    « Rends le tableau des cours historiques de cette page, ligne par ligne, avec
      des barres verticales entre chaque colonne, et rien d'autre. »

LIMITE MESURÉE QUE CE PROGRAMME NE PEUT PAS COMBLER : le modèle qui lit la page peut
GLISSER UN CHIFFRE dans un volume — 3 654 181 rendu pour 3 664 181 le 10-09. Prix
justes 112/112, volumes 26/28. Le contrôle de vraisemblance ne regarde le volume que
comme « > 0 » : un chiffre glissé passe. SEULE UNE SECONDE SOURCE LE VERRAIT — A-392
cesse d'être un confort pour devenir une nécessité.

USAGE :
  python3 COLLECTER_LES_COURS_ABC.py <dossier_du_projet> <dossier_de_sortie>
    <dossier_du_projet>  : porte le référentiel et cours_nouveaux.csv existant
    <dossier_de_sortie>  : où écrire cours_nouveaux.csv mis à jour et le rapport
  Option --pages <dossier> : lit les pages HTML déjà téléchargées dans ce dossier
    (une par valeur, nommée <code>.html) au lieu de les récupérer — c'est ainsi
    que la tâche planifiée le lance : elle télécharge par son outil web, puis
    passe les fichiers. Le programme ne fait AUCUN appel réseau lui-même.

CODE DE SORTIE (R-734, R-734bis) :
  0 = toutes les valeurs lues et au moins une séance nouvelle ou rien à ajouter
  1 = au moins une valeur en échec (page absente, tableau introuvable, 0 ligne)
  2 = le contrôle n'a pas pu tourner (référentiel absent, module absent)

════════════════════════════════════════════════════════════════════════
LES DOUZE ÉLÉMENTS — R-752 les pose à tous les niveaux, et le programme
entier est le premier niveau
════════════════════════════════════════════════════════════════════════
① RÔLE — Il n'en a plus. Ce programme a été le pas n°1 de la collecte des cours
  pendant une journée, le 10-09-2026 ; le même jour il a été remplacé par
  programmes/COLLECTER_ABC_GITHUB.py, qui fait le même travail sans passer par
  un modèle qui lit la page. Trois relevés du 19-09-2026 le disent : le seul
  programme de collecte nommé dans .github/workflows/collecte_abc.yml est
  COLLECTER_ABC_GITHUB.py · gouvernance/SOCLE.csv, à la ligne qui porte le chemin
  de ce fichier-ci, le range en PRESUME avec le motif « aucun lanceur detecte — un
  lancement a la main ne s ecrit nulle part » · la photographie, rangée depuis aux
  archives sous archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md, le
  comptait parmi les « 23 programme(s) QUI NE TOURNENT PAS LE SOIR ». Les deux
  premiers relevés sont vérifiés à nouveau le 24-09-2026. Ce qu'il faisait quand il
  servait : recevoir le texte qu'un outil web a tiré des pages d'ABC Bourse,
  y retrouver le tableau des cours, le convertir au format du fichier des cours,
  et confier le jugement et l'écriture à programmes/CONTROLER_LES_COURS.py.
② CONTEXTE D'APPEL — Une tâche planifiée Cowork, le 10-09-2026 : elle
  téléchargeait les pages avec son outil web, les déposait dans un dossier sous
  le nom `<code>.html`, puis lançait ce programme avec `--pages <dossier>`.
  AUCUN APPELANT AUTOMATIQUE AUJOURD'HUI : le 19-09-2026, une recherche du nom
  `COLLECTER_LES_COURS_ABC` dans les deux tâches planifiées du dépôt —
  .github/workflows/collecte_abc.yml et .github/workflows/comparer_google_abc.yml
  — puis dans tous les fichiers de programmes/, ne rend aucune ligne qui le
  lance. Le seul autre endroit qui le nomme est la consigne de commentage
  prompts_taches/CONSIGNE_COMMENTER_LES_28_PROGRAMMES_Sam_19-09-2026.md, qui le
  cite comme programme à documenter, pas comme programme à exécuter.
③ ENTRÉE — La ligne de commande, trois choses : le dossier du projet · le
  dossier de sortie · et `--pages <dossier>`, le dossier qui porte une page par
  valeur. Et trois fichiers lus : le référentiel des valeurs, le fichier des
  cours déjà écrit — relu pour savoir où chaque valeur s'était arrêtée — et une
  page par valeur, nommée d'après son code ABC, par exemple `ACp.html` pour
  ACCOR.
④ CONDITIONS D'ENTRÉE — Trois exigences, et chacune arrête le programme si elle
  n'est pas tenue : au moins deux arguments · l'option `--pages`, faute de quoi
  il n'y a rien à lire, ce programme ne sortant jamais sur le réseau · et
  programmes/CONTROLER_LES_COURS.py atteignable depuis le dossier du projet. Le
  fichier des cours, lui, peut ne pas exister : c'est alors une création, et le
  plancher du 10-07-2026 sert de seuil à toutes les valeurs.
⑤ SORTIE — Un code de sortie, un rapport affiché à l'écran, et deux fichiers
  écrits dans le dossier de sortie : `cours_nouveaux.csv` et
  `rapport_collecte_abc.md`.
⑥ TRAITEMENT — ① contrôler les arguments · ② charger le module de contrôle des
  cours · ③ lire le référentiel et en déduire le code ABC de chaque valeur ·
  ④ retrouver le fichier des cours existant, en copier le contenu dans le
  fichier de sortie, et relever pour chaque valeur sa dernière séance et sa
  dernière clôture · ⑤ pour chaque valeur : lire sa page, en extraire le tableau,
  écarter les séances que la règle d'horloge refuse, ne garder que celles plus
  récentes que ce qui est déjà au fichier · ⑥ soumettre le lot entier au contrôle
  de vraisemblance · ⑦ écrire ce que le contrôle laisse passer · ⑧ composer le
  rapport, l'écrire et l'afficher · ⑨ sortir avec 0, 1 ou 2.
⑦ UNITÉ — Les prix sont en euros, le volume en titres, les dates au format
  AAAA-MM-JJ. L'heure de bascule qui accepte ou refuse la séance du jour est une
  heure de Paris, fixée à 18. L'écart maximal entre deux séances voisines est un
  nombre de JOURS de calendrier, fixé à 6.
⑧ POURQUOI — Trois choix commandent tout le reste. ① Le programme ne sort jamais
  sur le réseau et reçoit des pages déjà téléchargées : le réseau Python d'une
  tâche Claude est fermé, et seul l'outil web de la tâche pouvait atteindre ABC
  Bourse. ② Il ne juge ni n'écrit lui-même : normaliser, contrôler la
  vraisemblance, dédoublonner et écrire viennent tous de
  programmes/CONTROLER_LES_COURS.py, parce que deux implémentations d'une même
  chose divergent toujours (R-708). ③ Le lot entier passe le contrôle avant
  qu'une seule ligne soit écrite : une séance fausse rend le lot suspect, et
  mieux vaut ne rien écrire que d'en écrire la moitié.
⑨ CE QUI CLOCHE —
  ① Il écrit les noms de valeurs tels que le référentiel les porte, avec leurs
  espaces, alors que le fichier des cours les porte avec des tirets bas. Mesuré
  le 19-09-2026 sur une copie du dépôt, avec quarante pages fabriquées : le
  fichier écrit reçoit `AIR LIQUIDE`, `BNP PARIBAS`, `BUREAU VERITAS`, quand
  donnees/claude_cours_nouveaux.csv porte `AIR_LIQUIDE`, `BNP_PARIBAS`,
  `BUREAU_VERITAS`. Treize des quarante noms du référentiel contiennent un
  espace ou un tiret, donc treize valeurs sur quarante existeraient en double.
  Tout programme qui relit ce fichier sans rapprocher les deux orthographes croit
  à deux sociétés distinctes et n'en compte qu'une. C'est le défaut qui a fait
  perdre 26 % des lignes d'une
  mesure le 23-08-2026 ; COLLECTER_ABC_GITHUB.py l'a corrigé chez lui le
  10-09-2026 en écrivant le nom normalisé, ce fichier-ci ne l'a pas.
  ② Il ignore la colonne `hors_univers` du référentiel, c'est-à-dire la décision
  écrite de ne pas collecter une valeur. Mesuré le 19-09-2026 : le référentiel
  donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv porte quarante lignes,
  dont une seule remplit cette colonne — ARCELORMITTAL, avec le motif
  « AMSTERDAM — decision Jean-Luc 13-09-2026, voir A-410 ». Ce programme la
  collecte quand même : sur une copie du dépôt, il a écrit cinq séances
  d'ARCELORMITTAL, du 14 au 18-09-2026. Et le même jour, sur un autre jeu de
  pages, cette seule valeur a rendu le lot BLOQUANT : rien n'a été écrit pour
  les trente-neuf autres, et le programme est sorti en code 2.
  ③ Il choisit le référentiel par ordre alphabétique et non par date. Mesuré le
  19-09-2026 sur un dossier portant REFERENTIEL_VALEURS_Lun_14-09-2026_10h00.csv,
  REFERENTIEL_VALEURS_Ven_01-08-2026_10h00.csv et
  REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv : ce programme retient celui
  du 17-08, tandis que la fonction `le_plus_recent` de programmes/COMMUN.py,
  que COLLECTER_ABC_GITHUB.py utilise depuis le 12-09-2026, retient celui du
  14-09. Les noms du projet commencent par le jour de la semaine, et l'alphabet
  range « Ven » après « Lun » : le plus récent ne se lit pas dans l'alphabet.
  ④ Le rapport annonce comme REFUSÉES des séances qui sont écrites. Mesuré le
  19-09-2026 : sur une valeur dont la clôture passe de 31,74 à 44,44, le rapport
  affiche « SÉANCES REFUSÉES PAR LE CONTRÔLE DE VRAISEMBLANCE — variation de
  +40.0 % sur VEOLIA le 2026-09-21 », le programme sort en code 0, et cette
  ligne est bel et bien dans le fichier écrit. Le contrôle des cours range en
  effet les alertes à part mais les laisse dans les séances écrivables ; seul un
  verdict BLOQUANT arrête l'écriture. Un lecteur du rapport croit qu'une donnée
  douteuse a été écartée alors qu'elle est entrée.
  ⑤ Le nom du jour est écrit en anglais dans l'en-tête du rapport. Mesuré le
  19-09-2026 : le rapport commence par « # COLLECTE ABC BOURSE — Sat 19-09-2026
  23h10 (Paris) », où tout le dépôt écrit « Sam ». L'heure, elle, est juste : la
  variable qui la porte est déjà en heure de Paris. C'est donc un défaut de
  lisibilité et non de justesse, et il est consigné au backlog sous A-429 avec
  sa correction, volontairement non appliquée tant que le chantier en cours est
  la description du système et non sa réparation.
  ⑥ Le fichier écrit ne porte pas le nom du fichier des cours du dépôt. Il écrit
  `cours_nouveaux.csv` dans le dossier de sortie, alors que le fichier vivant du
  dépôt est donnees/claude_cours_nouveaux.csv — relevé le 19-09-2026, la liste
  de donnees/ ne contient aucun fichier nommé `cours_nouveaux.csv`. Le programme
  recopie d'abord le fichier existant sous ce nouveau nom, puis empile dedans :
  le fichier du dépôt n'est jamais mis à jour, et c'est à celui qui lance le
  programme de reporter le résultat, sans que rien ne le lui dise.
  ⑦ Le rapport porte un nom fixe. Deux exécutions le même jour écrasent le
  premier rapport sans un mot, et la première peut avoir échoué pour une raison
  que la seconde efface.
  ⑧ Trois noms de fonction de ce fichier vivent aussi ailleurs, avec des
  comportements différents. Mesuré le 19-09-2026 sur la même valeur, le nombre
  4 225 636 écrit avec l'espace fine insécable qu'ABC Bourse emploie : `_nombre`
  de ce fichier rend 4225636.0, celle de programmes/COLLECTER_ABC_GITHUB.py lève
  une erreur, celle de programmes/CONTROLER_LES_COURS.py rend « rien ». Et
  `extraire` rend ici UNE liste, quand celle de COLLECTER_ABC_GITHUB.py rend
  DEUX valeurs, la liste et le motif de l'échec. Deux implémentations d'une même
  chose divergent toujours (R-708) : ici elles ont divergé jusqu'à la forme de
  ce qu'elles rendent.
⑩ EFFET — ÉCRIT deux fichiers dans le dossier de sortie : `cours_nouveaux.csv`,
  qui est d'abord une copie du fichier des cours existant puis grandit par
  ajout, et `rapport_collecte_abc.md`, écrasé à chaque passage. LIT le
  référentiel, le fichier des cours existant, et une page par valeur. MODIFIE le
  chemin de recherche des modules du processus. AUCUN ACCÈS RÉSEAU : le
  programme refuse de tourner sans `--pages`. Ne touche jamais
  donnees/cac40_ohlcv.csv ni aucun fichier de gouvernance, et ne supprime rien.
⑪ TERMINAISON — SORT DU PROGRAMME dans tous les cas, avec trois codes, tous
  mesurés le 19-09-2026 sur une copie du dépôt : 0 quand les quarante valeurs
  ont été lues et que ce qui devait être écrit l'a été · 1 quand au moins une
  page manque ou qu'un tableau est introuvable, le reste étant tout de même
  écrit · 2 quand rien n'a pu tourner — aucun argument, option `--pages`
  absente, module de contrôle illisible, référentiel introuvable — ou quand le
  lot est BLOQUANT et que rien n'a été écrit. Et un de ses appels peut ne pas
  revenir : `_importer_controle` et `lire_referentiel` sortent toutes deux en
  code 2 sans rendre la main.
⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à
    suivre, avec pour chacune son mnémonique et sa place de cotation.
  le code ABC : le nom sous lequel ABC Bourse désigne une valeur, formé du
    mnémonique Euronext suivi de `p` pour Paris ou `n` pour Amsterdam.
  le contrôle de vraisemblance : les tests de programmes/CONTROLER_LES_COURS.py
    qui jugent une séance avant qu'elle soit écrite.
  un lot BLOQUANT : un ensemble de séances dont l'une est jugée fausse, ce qui
    fait refuser l'écriture de tout l'ensemble.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des
    décisions et des actions du projet
  Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
  l'outil web : l'outil d'une tâche planifiée Cowork qui ouvre une page et en rend un texte écrit par un modèle, jamais la page elle-même.
  la boucle : la tache planifiee qui lit les signaux et rend compte
  la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
  le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
"""

import sys, os, re, csv, io
from datetime import datetime, date
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
DATE_PLANCHER = "2026-07-10"   # même plancher que CONTROLER_LES_COURS

# ─── le module de contrôle est OBLIGATOIRE ───────────────────────────────────
def _importer_controle(dossier):
    """Charge le module de contrôle des cours, ou arrête le programme en code 2.

    ① RÔLE — Donner au programme le seul module qui sait normaliser un nom et une
      date, juger une séance et l'écrire au fichier des cours. Ce programme ne
      refait rien de ce travail lui-même, parce que deux implémentations d'une
      même chose divergent toujours (R-708). Sans ce module, il saurait encore
      lire des pages, mais plus rien ne vérifierait qu'une clôture est
      vraisemblable ni qu'une date est lisible.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après le contrôle des arguments
      et avant toute lecture de fichier. Aucun autre appelant : le 19-09-2026,
      une recherche du nom `_importer_controle` dans tous les fichiers de
      programmes/, dans .github/workflows/ et dans prompts_taches/ ne rend aucune
      ligne hors de ce fichier.
    ③ ENTRÉE — `dossier` : le dossier du projet. Un seul appelant, `main`, qui
      transmet sans le modifier le premier argument de la ligne de commande, par
      exemple `.` quand le programme est lancé depuis la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le dossier reçu doit porter
      `programmes/CONTROLER_LES_COURS.py`, ou ce fichier doit déjà être
      atteignable par le chemin de recherche des modules du processus.
    ⑤ SORTIE — UNE valeur : le module CONTROLER_LES_COURS lui-même. `main` y
      prend ensuite quatre fonctions — `normaliser_valeur`, `normaliser_date`,
      `controler` et `ajouter_au_fichier`.
      [rend: 1]
    ⑥ TRAITEMENT — ① mettre le dossier reçu en tête du chemin de recherche des
      modules · ② y mettre aussi son sous-dossier `programmes` · ③ importer le
      module et le rendre · ④ si l'import échoue, afficher une ligne commençant
      par « CODE 2 » et arrêter le programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'arrêt immédiat est voulu : un contrôle qui n'a pas pu tourner
      rend un code de sortie non nul (R-734). Continuer sans ce module écrirait
      des cours que personne n'aurait jugés, et le rapport dirait quand même
      « écrites : 40 ». Le code 2 sépare ce cas du code 1, qui dit qu'une valeur
      n'a pas pu être lue, et du code 0, qui dit que tout s'est bien passé.
    ⑨ CE QUI CLOCHE —
      ① Le message dit « introuvable » pour un module qui est trouvé mais cassé.
      Mesuré le 19-09-2026 sur un CONTROLER_LES_COURS.py volontairement amputé
      d'une parenthèse : la sortie est « CODE 2 — CONTROLER_LES_COURS
      introuvable : '(' was never closed (CONTROLER_LES_COURS.py, line 1) ». La
      cause exacte est là, mais le premier mot envoie chercher un fichier absent
      alors qu'il est présent et illisible.
      ② Elle rattrape toutes les erreurs, pas seulement l'absence du module. Le
      module importé exécute son propre corps à l'import ; une erreur venue de
      là — un fichier qu'il lit et qui manque, par exemple — serait rendue sous
      le même message d'import raté.
      ③ Les deux chemins ajoutés ne sont jamais retirés, et rien ne vérifie
      qu'ils y sont déjà. Le dossier du projet passe devant tout le reste pour la
      durée du processus : un fichier qui y porterait le nom d'un module du
      langage serait chargé à sa place.
    ⑩ EFFET — MODIFIE le chemin de recherche des modules du processus, en y
      ajoutant deux entrées en tête, définitivement. N'écrit aucun fichier, ne
      touche pas au réseau. Affiche une ligne, et seulement quand l'import
      échoue.
    ⑪ TERMINAISON — **PEUT NE PAS RENDRE LA MAIN : elle SORT DU PROGRAMME quand l'import échoue.** Rend la main avec le module quand l'import réussit. SORT DU
      PROGRAMME avec le code 2 sinon — mesuré le 19-09-2026. Aucun de ses appels
      ne se termine.
      [sort: oui]
    ⑫ DÉFINITIONS
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
      le fichier des cours : le fichier où les séances s'empilent sans jamais
        être réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
        n'en étant qu'une copie de lecture
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
"""
    sys.path.insert(0, dossier)
    sys.path.insert(0, os.path.join(dossier, "programmes"))
    try:
        import CONTROLER_LES_COURS as C
        return C
    except Exception as e:
        print(f"CODE 2 — CONTROLER_LES_COURS introuvable : {e}")
        sys.exit(2)


# ─── lecture du référentiel → liste (nom_usuel, code_abc, place) ─────────────
def lire_referentiel(dossier):
    """Rend le référentiel retenu et la liste des valeurs à collecter, ou arrête
    le programme en code 2.

    ① RÔLE — Dire QUI collecter, et sous quel nom le demander à ABC Bourse.
      C'est le seul endroit qui décide du périmètre du passage : une valeur
      absente de cette liste ne sera ni lue, ni écrite, ni manquée par personne.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après le chargement du module de
      contrôle et avant la lecture des pages. Aucun autre appelant dans ce
      fichier. Une fonction du même nom vit dans
      programmes/COLLECTER_ABC_GITHUB.py, ligne 269 : c'est une autre fonction,
      qui ne rend pas la même liste.
    ③ ENTRÉE — `dossier` : le dossier du projet. Un seul appelant, `main`, qui
      transmet sans le modifier le premier argument de la ligne de commande, par
      exemple `.` quand le programme est lancé depuis la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le dossier reçu, ou son sous-dossier `donnees`, doit
      porter au moins un fichier dont le nom commence par REFERENTIEL_VALEURS et
      finit par `.csv`. Ce fichier doit porter les colonnes `mnemonique`,
      `nom_usuel` et `place_cotation`.
    ⑤ SORTIE — DEUX valeurs : le chemin du référentiel retenu, et la liste des
      valeurs. Chaque valeur est un triplet — son nom usuel tel que le
      référentiel l'écrit, son code ABC, et sa place, `PARIS` ou `AMSTERDAM`.
      Mesuré le 19-09-2026 sur le référentiel du dépôt : 40 valeurs, dont une
      seule à Amsterdam, ARCELORMITTAL.
      [rend: 2]
    ⑥ TRAITEMENT — ① rassembler les référentiels trouvés dans le dossier du
      projet et dans son sous-dossier `donnees` · ② arrêter le programme s'il n'y
      en a aucun · ③ garder le dernier par ordre alphabétique du chemin complet ·
      ④ pour chaque ligne du fichier : sauter celles sans mnémonique · ⑤ ajouter
      `n` au mnémonique si la place contient AMSTERDAM, `p` sinon · ⑥ rendre le
      chemin retenu et la liste.
    ⑦ UNITÉ — Un NOMBRE DE VALEURS. Le code ABC n'est pas une grandeur : c'est un
      nom, formé du mnémonique Euronext suivi d'une lettre de place.
    ⑧ POURQUOI — Le code ABC se déduit du référentiel au lieu d'être écrit dans
      une table à part : une table de plus serait un second endroit à tenir à
      jour, et un chiffre ou un nom qui existe ailleurs ne se recopie pas
      (R-708). La correspondance a été vérifiée sur onze valeurs sur onze le
      10-09-2026. La place de cotation, elle, ne sert pas qu'au nom : elle décide
      plus loin si la séance la plus récente est acceptée, Amsterdam servant une
      dernière ligne encore incomplète.
    ⑨ CE QUI CLOCHE —
      ① Elle ignore la colonne `hors_univers`, qui porte la décision écrite de ne
      pas collecter une valeur. Mesuré le 19-09-2026 sur
      donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv : quarante lignes,
      une seule remplit cette colonne, ARCELORMITTAL, avec le motif
      « AMSTERDAM — decision Jean-Luc 13-09-2026, voir A-410 ». Cette fonction la
      rend quand même, et le programme la collecte : cinq séances écrites pour
      elle sur une copie du dépôt le même jour. La fonction de même nom de
      programmes/COLLECTER_ABC_GITHUB.py, elle, saute cette ligne.
      ② Elle choisit le référentiel par l'alphabet, jamais par la date. Mesuré le
      19-09-2026 sur un dossier portant REFERENTIEL_VALEURS_Lun_14-09-2026_10h00.csv,
      REFERENTIEL_VALEURS_Ven_01-08-2026_10h00.csv et
      REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv : elle retient celui du
      17-08, quand `le_plus_recent` de programmes/COMMUN.py retient celui du
      14-09. Les noms du projet commencent par le jour de la semaine, et
      l'alphabet range « Ven » après « Lun ».
      ③ Elle mélange deux dossiers dans une même liste et tranche entre eux par
      le tri du chemin complet. Un référentiel oublié à la racine du projet et un
      référentiel à jour dans `donnees` sont comparés par leur chemin ; mesuré le
      19-09-2026, c'est celui de `donnees` qui l'emporte, mais par l'ordre des
      lettres du chemin et non par une règle écrite.
      ④ Une valeur dont le mnémonique est vide est sautée en silence. Aucun
      compte, aucune ligne au rapport : une valeur attendue qui ne renvoie rien
      est pourtant une alerte, jamais un silence.
      ⑤ La colonne `place_cotation` décide par le seul mot AMSTERDAM. Une valeur
      cotée ailleurs qu'à Paris et qu'à Amsterdam recevrait le suffixe de Paris,
      et sa page serait demandée sous un code qui n'existe pas.
    ⑩ EFFET — LIT la liste des noms de deux dossiers, puis un fichier CSV en
      entier. N'écrit rien, ne touche pas au réseau. Affiche une ligne, et
      seulement quand aucun référentiel n'est trouvé.
    ⑪ TERMINAISON — **PEUT NE PAS RENDRE LA MAIN : elle SORT DU PROGRAMME si aucun référentiel n'est lisible.** Rend la main avec ses deux valeurs dans le cas normal. SORT
      DU PROGRAMME avec le code 2 quand aucun référentiel n'est trouvé. PEUT
      LEVER, sans que ce soit rattrapé : sur un fichier dont la colonne
      `nom_usuel` manque, la lecture d'une clé absente arrête le programme.
      Aucun de ses appels ne se termine.
      [sort: oui]
    ⑫ DÉFINITIONS
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à
        suivre, avec pour chacune son mnémonique et sa place de cotation.
      le code ABC : le nom sous lequel ABC Bourse désigne une valeur, formé du
        mnémonique Euronext suivi de `p` pour Paris ou `n` pour Amsterdam.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
        n'en étant qu'une copie de lecture
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
"""
    cands = []
    for racine in (dossier, os.path.join(dossier, "donnees")):
        if os.path.isdir(racine):
            cands += [os.path.join(racine, f) for f in os.listdir(racine)
                      if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    if not cands:
        print("CODE 2 — référentiel des valeurs introuvable"); sys.exit(2)
    chemin = sorted(cands)[-1]
    out = []
    with open(chemin, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            m = (r.get("mnemonique") or "").strip()
            if not m:
                continue
            place = (r.get("place_cotation") or "").upper()
            suffixe = "n" if "AMSTERDAM" in place else "p"
            out.append((r["nom_usuel"].strip(), m + suffixe, "AMSTERDAM" if suffixe == "n" else "PARIS"))
    return chemin, out


# ─── extraction du tableau "Cours historiques" d'une page ABC ────────────────
# La page rend, en markdown ou en HTML, un tableau dont chaque ligne vaut :
#   | 09/09/2026 | 78,20 | 78,88 | 78,08 | 4 225 636 | 78,21 | 0,59% |
#   Date · Ouverture · Plus Haut · Plus Bas · Volume · Dernier · Variation
# On cherche le motif, jamais la position : une ligne = une date + six nombres.
# LE MOTIF EXIGE LES BARRES VERTICALES ENTRE CHAQUE CHAMP. Cowork l'a éprouvé le
# 10-09 : sans les barres, l'ancien motif GLISSAIT d'une colonne — le volume avalait
# la clôture, la variation devenait la clôture (close 701,03 sur AIRBUS). Le contrôle
# aval rattrapait en BLOQUANT tout le lot, et le programme sortait avec 0. Un
# changement de rendu n'aurait pas corrompu les données : il aurait éteint la
# collecte en silence. Avec les barres obligatoires, un rendu différent donne ZÉRO
# ligne — bruyant, donc acceptable.
# CE QUE L'OUTIL WEB REND N'EST PAS LA PAGE : c'est un texte produit par un modèle
# qui l'a lue (relevé par la tâche jetable du 10-09). Le tableau y arrive en
# markdown, avec des barres. C'est cette forme, et elle seule, que le motif accepte.
_SEP = r"\s*\|\s*"
_NB  = r"([\d\s\u202f]+,\d+|\d+)"
_LIGNE = re.compile(
    r"\|" + r"\s*(\d{2})/(\d{2})/(\d{4})" + _SEP   # | date
    + _NB + _SEP                                   # ouverture |
    + _NB + _SEP                                   # plus haut |
    + _NB + _SEP                                   # plus bas |
    + r"([\d\s\u202f]+)" + _SEP                   # volume |
    + _NB + _SEP                                   # dernier |
)

def _nombre(s):
    """Convertit un nombre écrit à la française en nombre calculable.

    ① RÔLE — Traduire ce qu'ABC Bourse affiche en ce qu'un programme peut
      comparer. La page écrit « 4 225 636 » et « 78,20 » ; un calcul a besoin de
      4225636.0 et de 78.2. Sans cette traduction, aucune séance ne pourrait être
      jugée ni triée.
    ② CONTEXTE D'APPEL — `_lignes_seance`, pour les six nombres de chaque ligne
      du tableau : ouverture, plus haut, plus bas, volume et clôture — le volume
      étant ensuite arrondi en entier. Sur quarante valeurs et trente séances,
      quelques milliers d'appels par passage. Aucun autre appelant.
    ③ ENTRÉE — `s` : un nombre écrit à la française, tel que le motif de lecture
      l'a découpé dans la ligne. Un seul appelant, `_lignes_seance`, qui passe
      les morceaux du motif sans les modifier, par exemple `4 225 636` ou
      `78,20`.
    ④ CONDITIONS D'ENTRÉE — La chaîne doit être convertible une fois ses espaces
      retirés et sa virgule changée en point. Elle ne vérifie rien elle-même :
      c'est le motif de lecture, en amont, qui garantit qu'elle ne reçoit que des
      chiffres, des espaces et une virgule.
    ⑤ SORTIE — UNE valeur : le nombre, en virgule flottante. Mesuré le
      19-09-2026 : `4 225 636` rend 4225636.0 et `78,20` rend 78.2.
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les espaces ordinaires, qui séparent les milliers ·
      ② retirer les espaces fines insécables, qui font le même travail et sont
      invisibles à l'affichage · ③ remplacer la virgule décimale par un point ·
      ④ convertir.
    ⑦ UNITÉ — Celle de la cellule reçue : des euros pour les prix, des titres
      pour le volume. La fonction ne le sait pas et ne peut pas le vérifier.
    ⑧ POURQUOI — L'espace fine insécable est traitée à part parce qu'elle est
      invisible : un volume qui la porte ressemble en tout point à un volume qui
      porte un espace ordinaire, et la conversion échouerait sans qu'on voie
      pourquoi. Convertir ici, à un seul endroit, évite que chaque appelant s'en
      charge à sa façon.
    ⑨ CE QUI CLOCHE —
      ① Elle ne distingue pas un nombre absent d'un nombre illisible : les deux
      font lever. Mesuré le 19-09-2026 : `n/d` et la chaîne vide lèvent toutes
      deux la même erreur. L'appelant ignore alors la ligne entière, ce qui est
      le bon comportement, mais la cause ne remonte nulle part.
      ② Trois fonctions du dépôt portent ce nom et ne se comportent pas de la
      même façon. Mesuré le 19-09-2026 sur `4 225 636` écrit avec l'espace fine
      insécable : celle-ci rend 4225636.0, celle de
      programmes/COLLECTER_ABC_GITHUB.py lève une erreur, et celle de
      programmes/CONTROLER_LES_COURS.py rend « rien ». Trois lectures du même
      chiffre, trois réponses : deux implémentations d'une même chose divergent
      toujours (R-708).
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main quand la chaîne est convertible. LÈVE sinon, et
      la levée n'est pas rattrapée ici : c'est `_lignes_seance` qui l'attrape
      pour ignorer la ligne. Aucun de ses appels ne se termine.
      [sort: non]
    """
    return float(s.replace(" ", "").replace("\u202f", "").replace(",", "."))

BLOC_MIN = 5          # à partir de ce nombre de lignes toutes isolées, c'est un ordre inversé : zéro, bruyant
ECART_MAX_JOURS = 6   # deux séances consécutives ne sont jamais espacées de plus
                      # (vendredi → lundi = 3 ; un pont ou une fermeture = 4 à 5)

def _lignes_seance(texte):
    """Toutes les lignes du texte qui ont la forme d'une séance, avec leur numéro.

    ① RÔLE — Séparer, dans un texte qui peut contenir n'importe quoi, ce qui
      ressemble à une séance de bourse de ce qui n'y ressemble pas — et retenir à
      quel rang chaque ligne se trouvait. Ce rang est ce qui permet ensuite de
      dire que deux séances se suivent : sans lui, un tableau de dividendes rangé
      plus bas dans la page serait indistinguable du tableau des cours.
    ② CONTEXTE D'APPEL — `extraire`, une fois par valeur, au tout début de son
      travail. Aucun autre appelant : le 19-09-2026, une recherche du nom
      `_lignes_seance` dans tous les fichiers de programmes/, dans
      .github/workflows/ et dans prompts_taches/ ne rend aucune ligne hors de ce
      fichier.
    ③ ENTRÉE — `texte` : le contenu entier du fichier d'une valeur, tel que
      l'outil web l'a écrit. Un seul appelant, `extraire`, qui transmet sans le
      modifier ce que `main` a lu du fichier `<code>.html`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un texte vide, une page d'erreur ou un
      tableau d'une autre nature ne la font pas tomber : elle rend alors une
      liste vide.
    ⑤ SORTIE — UNE valeur : une liste de triplets, dans l'ordre où les lignes se
      présentent. Chaque triplet porte le rang de la ligne dans le texte, la date
      de la séance, et la séance elle-même — date au format AAAA-MM-JJ,
      ouverture, plus haut, plus bas, clôture et volume.
      [rend: 1]
    ⑥ TRAITEMENT — ① découper le texte en lignes · ② chercher dans chaque ligne
      le motif d'une séance : une date en jour, mois, année, puis cinq nombres,
      chacun encadré de barres verticales · ③ passer à la suivante si le motif ne
      s'y trouve pas · ④ construire la date, et passer à la suivante si elle
      n'existe pas au calendrier · ⑤ convertir les cinq nombres et ranger le
      triplet.
    ⑦ UNITÉ — Les prix sont en euros, le volume en titres, la date est ramenée au
      format AAAA-MM-JJ. Le rang est un NUMÉRO DE LIGNE dans le texte reçu,
      compté à partir de zéro ; il ne sert qu'à comparer deux lignes entre elles.
    ⑧ POURQUOI — Le motif exige une barre verticale entre chaque champ. Sans
      elles, l'ancien motif glissait d'une colonne : le volume avalait la
      clôture, et la variation devenait la clôture — une clôture de 701,03 a été
      relevée ainsi sur AIRBUS le 10-09-2026. Avec les barres obligatoires, un
      rendu d'une autre forme ne donne pas des données décalées, il ne donne
      RIEN : mesuré le 19-09-2026, le même tableau privé de ses barres rend zéro
      séance. Une collecte qui s'éteint bruyamment vaut mieux qu'une collecte qui
      écrit faux.
      La date impossible est écartée au lieu d'arrêter le programme, parce
      qu'une ligne mal lue ne doit pas coûter les trente-neuf autres valeurs :
      mesuré le 19-09-2026, une ligne datée du 31/02/2026 est simplement ignorée.
    ⑨ CE QUI CLOCHE —
      ① Elle ne voit qu'une séance par ligne. Le motif est cherché, pas répété.
      Mesuré le 19-09-2026 sur deux séances écrites bout à bout sur la même
      ligne : une seule est rendue, l'autre disparaît sans un mot.
      ② Une date impossible et une ligne qui n'est pas une séance sont traitées
      de la même façon : passées. Rien ne compte ces lignes, rien ne les nomme au
      rapport. Une page dont toutes les dates seraient mal formées rendrait donc
      « tableau introuvable », ce qui est vrai mais ne dit pas ce qui s'est
      passé.
      ③ Le volume est converti en virgule flottante avant d'être arrondi en
      entier. Un volume de plus de quinze chiffres perdrait sa précision en
      chemin ; aucun volume du CAC 40 n'en approche, mais rien dans le code ne
      borne ce que la page peut écrire.
      ④ Le rang compté est celui de la ligne dans le texte reçu, donc la
      contiguïté suppose que les séances se suivent sans ligne vide. Mesuré le
      19-09-2026 : le même tableau avec une ligne vide entre chaque séance ne
      rend plus aucune séance au bout de la chaîne, alors que les six lignes sont
      bien lues ici.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : la date impossible
      est rattrapée et la ligne passée. Un de ses appels peut ne pas revenir en
      rendant une valeur : `_nombre` lève sur une chaîne non convertible — mais
      le motif, en amont, ne lui laisse passer que des chiffres, des espaces et
      une virgule.
      [sort: non]
    ⑫ DÉFINITIONS
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
      l'outil web : l'outil d'une tâche planifiée Cowork qui ouvre une page et en
        rend un texte écrit par un modèle, jamais la page elle-même.
    """
    out = []
    for n, ligne in enumerate(texte.split("\n")):
        m = _LIGNE.search(ligne)
        if not m:
            continue
        jj, mm, aaaa, o, h, b, v, c = m.groups()
        try:
            d = date(int(aaaa), int(mm), int(jj))
            out.append((n, d, {"date": d.isoformat(), "open": _nombre(o), "high": _nombre(h),
                                "low": _nombre(b), "close": _nombre(c), "volume": int(_nombre(v))}))
        except ValueError:
            continue
    return out


def extraire(texte):
    """Rend la liste des séances du tableau des cours, du plus récent au plus ancien.

    LA ZONE SE TROUVE PAR UNE PROPRIÉTÉ, JAMAIS PAR UNE ANCRE TEXTUELLE.
    Cowork l'a éprouvé le 10-09 sur le rendu réel : l'ancre « Cours historiques »
    n'apparaît que si le modèle qui lit la page décide de l'écrire — avec le prompt
    qui donne le rendu le plus stable (« le tableau, rien d'autre »), elle n'apparaît
    JAMAIS, et l'ancienne version rendait zéro tous les jours. Et la fin de zone sur
    « ## » laissait passer un tableau de dividendes introduit par « **Dividendes** ».
    LA PROPRIÉTÉ : le tableau des cours est LE PLUS LONG BLOC CONTIGU de lignes à
    barres dont les dates sont STRICTEMENT DÉCROISSANTES et jamais espacées de plus
    de ECART_MAX_JOURS. Un dividende du 15/05 sous un 31/07 rompt l'écart ; un titre,
    quel qu'il soit, rompt la contiguïté. Aucune prose n'est requise.

    ① RÔLE — Décider, dans un texte qui peut porter plusieurs tableaux, lequel est
      le tableau des cours, et n'en rendre que lui. C'est le seul endroit du
      programme qui comprend la forme de ce que l'outil web a rendu ; tout ce qui
      suit travaille sur des séances et ne sait plus d'où elles viennent.
    ② CONTEXTE D'APPEL — `main`, une fois par valeur, juste après la lecture du
      fichier de cette valeur. Aucun autre appelant. Une fonction du même nom vit
      dans programmes/COLLECTER_ABC_GITHUB.py, ligne 164 : c'est une autre
      fonction, qui lit du HTML brut et rend DEUX valeurs.
    ③ ENTRÉE — `texte` : le contenu entier du fichier d'une valeur. Un seul
      appelant, `main`, qui passe ce qu'il vient de lire dans `<code>.html`, par
      exemple `ACp.html` pour ACCOR.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une page vide, une page d'erreur, un tableau
      d'une autre forme : tous ces cas sont prévus et rendent une liste vide.
    ⑤ SORTIE — UNE valeur : la liste des séances du bloc retenu, du plus récent au
      plus ancien. Une liste VIDE quand aucune ligne n'a la forme d'une séance, et
      quand le tableau est servi à l'envers.
      [rend: 1]
    ⑥ TRAITEMENT — ① relever toutes les lignes qui ont la forme d'une séance, avec
      leur rang · ② rendre une liste vide s'il n'y en a aucune · ③ découper ces
      lignes en blocs : deux lignes sont du même bloc si elles se suivent dans le
      texte, si la seconde est plus ancienne que la première, et si l'écart entre
      leurs dates ne dépasse pas six jours · ④ rendre une liste vide si tous les
      blocs font une seule ligne et qu'il y a au moins cinq lignes en tout ·
      ⑤ garder les blocs qui contiennent la date la plus grande · ⑥ rendre le plus
      long d'entre eux.
    ⑦ UNITÉ — L'écart entre deux séances voisines est un nombre de JOURS de
      calendrier, borné à six. La taille d'un bloc est un NOMBRE DE SÉANCES, et le
      seuil qui déclenche le refus est de cinq lignes relevées. Les prix des
      séances rendues sont en euros, les volumes en titres.
    ⑧ POURQUOI — Trois gardes, chacun venu d'une perte mesurée.
      ① L'écart borné à six jours coupe ce qui n'est pas un tableau de cours.
      Deux séances ne sont jamais séparées de plus : du vendredi au lundi il y a
      trois jours, un pont ou une fermeture en donne quatre ou cinq. Un tableau de
      dividendes rangé plus bas continuerait pourtant la décroissance des dates ;
      l'écart le coupe. Mesuré le 19-09-2026 : une ligne datée du 15/05/2026
      ajoutée sous un tableau allant du 11/09 au 04/09 n'entre pas dans le
      résultat, qui reste à six séances.
      ② Le bloc retenu est celui qui porte la date la plus grande, jamais le plus
      long. Après une suspension de cotation de dix jours, le bloc le plus long
      est l'ancien, et les séances récentes — les seules nouvelles — seraient
      jetées sans un mot. Mesuré le 19-09-2026 : sur un texte portant deux séances
      de septembre puis onze séances de juillet, le résultat est bien les deux de
      septembre.
      ③ Le refus quand tous les blocs font une ligne reconnaît un tableau servi à
      l'envers, du plus ancien au plus récent. Dans ce cas chaque paire de lignes
      croît, donc aucune ne rejoint sa voisine, et « le bloc le plus long » rendait
      une seule séance, déjà au fichier — un échec qui ne se voyait pas. Mesuré le
      19-09-2026 : le même tableau à l'envers rend zéro séance, ce qui devient
      « tableau introuvable » au rapport et fait sortir le programme en code 1.
    ⑨ CE QUI CLOCHE —
      ① Le garde qui reconnaît le tableau à l'envers ne s'arme qu'à partir de cinq
      lignes relevées, et le cas qu'il laisse passer est précisément celui qu'il
      devait couvrir. Mesuré le 19-09-2026 sur quatre séances isolées les unes des
      autres : la fonction rend UNE séance, la plus récente, et jette les trois
      autres sans un mot. Le seuil est un COMPTE, et un garde-fou porte sur une
      propriété, jamais sur un compte (R-721).
      ② Le texte en tête de cette fonction annonce « LE PLUS LONG BLOC CONTIGU »,
      alors que le code retient d'abord les blocs portant la date la plus grande
      et ne choisit le plus long qu'entre ceux-là. Le commentaire qui suit dans le
      fichier dit bien « jamais le plus long » : deux phrases du même fichier se
      contredisent, et la première est celle qu'on lit en premier.
      ③ Une seule séance qui manque au milieu du tableau coupe le bloc en deux,
      parce que la contiguïté porte sur le rang des lignes. La moitié ancienne est
      alors perdue sans être comptée ni nommée au rapport.
      ④ Le seuil de six jours est écrit dans ce fichier et dans
      programmes/COLLECTER_ABC_GITHUB.py, où le commentaire de la ligne 226
      affirme « Même borne que COLLECTER_LES_COURS_ABC — un seul chiffre, jamais
      deux (R-708) ». Le chiffre est pourtant écrit deux fois, dans deux fichiers :
      corriger l'un sans l'autre les ferait diverger en silence.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Un de ses appels peut
      ne pas revenir en rendant une valeur : `_lignes_seance` appelle `_nombre`,
      qui lève sur une chaîne non convertible — mais le motif de lecture, en
      amont, ne lui laisse passer que des chiffres, des espaces et une virgule.
      [sort: non]
    ⑫ DÉFINITIONS
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
      l'outil web : l'outil d'une tâche planifiée Cowork qui ouvre une page et en
        rend un texte écrit par un modèle, jamais la page elle-même.
      un bloc : une suite de lignes qui se suivent dans le texte et dont les dates
        décroissent sans trou plus grand que six jours.
    
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
"""
    lignes = _lignes_seance(texte)
    if not lignes:
        return []
    blocs, bloc = [], [lignes[0]]
    for prev, cur in zip(lignes, lignes[1:]):
        n0, d0, _ = prev; n1, d1, _ = cur
        if n1 == n0 + 1 and d1 < d0 and (d0 - d1).days <= ECART_MAX_JOURS:
            bloc.append(cur)
        else:
            blocs.append(bloc); bloc = [cur]
    blocs.append(bloc)
    # LE BLOC QUI CONTIENT LA DATE LA PLUS GRANDE — jamais « le plus long ». Cowork,
    # 10-09 : après une suspension de dix jours, le plus long bloc était l'ancien, et
    # les quatre séances récentes — les seules nouvelles — étaient jetées en silence.
    # ET UNE TAILLE MINIMALE : servi du plus ancien au plus récent, chaque ligne faisait
    # un bloc d'une ligne, et « le plus long » rendait UNE séance déjà au fichier —
    # échec ouvert. Sous BLOC_MIN, on rend zéro : bruyant, « tableau introuvable ».
    # ORDRE INVERSÉ (servi du plus ancien au plus récent) : chaque paire croît, donc
    # TOUS les blocs font une ligne. C'est la signature — pas la taille du bloc récent,
    # qui peut légitimement être petite après une suspension (4 séances, mesuré).
    if len(lignes) >= BLOC_MIN and all(len(b) == 1 for b in blocs):
        return []
    date_max = max(d for _, d, _ in lignes)
    candidats = [b for b in blocs if any(d == date_max for _, d, _ in b)]
    meilleur = max(candidats, key=len) if candidats else []
    return [x[2] for x in meilleur]


# ─── règle de fraîcheur : la ligne du jour est-elle finale ? ─────────────────
# LA FRAÎCHEUR PAR LA PAGE EST RETIRÉE — Cowork, 10-09, après l'avoir proposée
# lui-même : le modèle qui lit la page a rendu « 12:37:13 » pour une page qui disait
# « 14:13:47 » quarante minutes plus tôt. S'il peut rendre 12:37 pour 14:13, il peut
# rendre 17:55 pour 14:13, et une ligne partielle entrerait avec la bénédiction de la
# règle. UNE VALEUR LUE PAR UN MODÈLE NE PEUT PAS SERVIR DE GARDE-FOU. Reste la règle
# d'horloge, prudente et bête, qui ne dépend de personne.
# Conséquence : Amsterdam n'a jamais sa ligne la plus récente, et reste hors signaux.

def seances_acceptables(seances, place, maintenant, jour):
    """Filtre par la règle d'horloge, seule qui ne dépende d'aucun modèle :
    Amsterdam écarte toujours sa plus récente ; Paris écarte la ligne du jour avant 18h.

    ① RÔLE — Empêcher qu'une ligne encore en cours de séance entre dans le fichier
      des cours. Une ligne partielle porte un volume incomplet et une clôture qui
      n'en est pas une ; une fois écrite, elle ne se réécrit jamais, puisque le
      fichier des cours ne fait que grandir.
    ② CONTEXTE D'APPEL — `main`, une fois par valeur, entre l'extraction du
      tableau et la comparaison avec ce qui est déjà au fichier. Aucun autre
      appelant : le 19-09-2026, une recherche du nom `seances_acceptables` dans
      tous les fichiers de programmes/, dans .github/workflows/ et dans
      prompts_taches/ ne rend aucune ligne hors de ce fichier.
    ③ ENTRÉE — `seances` : les séances rendues par l'extraction, du plus récent au
      plus ancien · `place` : `PARIS` ou `AMSTERDAM`, tel que le référentiel l'a
      donné · `maintenant` : l'instant du passage, en heure de Paris · `jour` : ce
      même instant réduit à sa date, au format AAAA-MM-JJ. Un seul appelant,
      `main`, qui prend `maintenant` et `jour` du même instant, relevé une seule
      fois au début du passage.
    ④ CONDITIONS D'ENTRÉE — `maintenant` doit porter l'heure de Paris, faute de
      quoi la comparaison à 18 h se fait dans un autre fuseau et accepte une ligne
      partielle. `jour` doit être écrit au format AAAA-MM-JJ, comme les dates des
      séances, sans quoi la comparaison ne reconnaît rien.
    ⑤ SORTIE — UNE valeur : la liste des séances gardées, dans l'ordre reçu. Une
      liste VIDE quand elle n'a rien reçu. Mesuré le 19-09-2026 sur six séances
      allant du 11/09 au 04/09 : six gardées à Paris à 20 h, cinq à Paris à 17 h,
      cinq à Amsterdam à 20 h.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre une liste vide s'il n'y a rien à filtrer · ② relever la
      date la plus récente des séances reçues · ③ pour Amsterdam, écarter toutes
      les séances qui portent cette date · ④ pour Paris avant 18 h, écarter toutes
      les séances datées du jour · ⑤ pour Paris à partir de 18 h, tout garder.
    ⑦ UNITÉ — L'heure de bascule est une HEURE DE PARIS, fixée à 18. Le filtre
      d'Amsterdam ne regarde pas l'heure du tout : il porte sur un RANG, la séance
      la plus récente, quelle que soit sa date.
    ⑧ POURQUOI — La règle ne lit aucun horodatage de la page, et c'est le point
      entier. Cowork avait proposé de se fier à l'heure que la page annonce, puis
      l'a retiré lui-même le 10-09-2026 : le modèle qui lisait la page a rendu
      « 12:37:13 » pour une page qui portait « 14:13:47 » quarante minutes plus
      tôt. Un modèle qui rend 12:37 pour 14:13 peut rendre 17:55 pour 14:13, et
      une ligne partielle entrerait alors avec la bénédiction de la règle. Une
      valeur lue par un modèle ne peut pas servir de garde-fou. Reste l'horloge de
      la machine, qui ne dépend de personne.
      Amsterdam perd toujours sa ligne la plus récente parce qu'elle a été mesurée
      partielle le 10-09-2026 sur ArcelorMittal : horodatage 11h43, volume cinq
      fois trop faible. La conséquence est actée et non réparée — cette valeur n'a
      jamais sa séance du jour, seulement celle de la veille, et une séance non
      lue le jour même perd ses signaux pour toujours.
    ⑨ CE QUI CLOCHE —
      ① Pour Amsterdam, la séance écartée est la plus RÉCENTE, jamais celle du
      jour. Un passage lancé un samedi écarte donc la séance du vendredi, qui est
      close depuis la veille. Mesuré le 19-09-2026 sur six séances allant du 11/09
      au 04/09 et un instant fixé au 11/09 à 20 h : la séance du 11/09 est
      écartée, ce qui est voulu ; mais le même filtre appliqué le 12/09 écarterait
      encore celle du 11/09, déjà définitive.
      ② `maintenant` et `jour` disent la même chose et sont passés séparément.
      Rien n'oblige l'appelant à les prendre du même instant : deux paramètres qui
      doivent s'accorder et qu'on peut fournir séparément finissent par diverger.
      ③ La règle de Paris ne regarde que l'heure, jamais le jour de la semaine ni
      le calendrier de bourse. Un dimanche à 20 h, une ligne datée du dimanche
      serait acceptée sans discussion.
      ④ Le seuil de 18 h et la place `AMSTERDAM` sont écrits dans le corps de la
      fonction. Une place nouvelle, ou une heure de clôture différente, demande de
      rouvrir le code : l'information vit dans le programme et non dans le
      référentiel, qui porte pourtant déjà la place de chaque valeur.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau. Elle ne modifie pas la liste reçue : elle en
      construit une autre.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas, et aucun de ses appels
      ne se termine : elle n'appelle aucune fonction du programme.
      [sort: non]
    ⑫ DÉFINITIONS
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
      le fichier des cours : le fichier où les séances s'empilent sans jamais être
        réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à
        suivre, avec pour chacune son mnémonique et sa place de cotation.
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
    
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
"""
    if not seances:
        return []
    plus_recente = max(x["date"] for x in seances)
    if place == "AMSTERDAM":
        return [x for x in seances if x["date"] != plus_recente]
    if maintenant.hour < 18:
        return [x for x in seances if x["date"] != jour]
    return seances


# ─── programme ───────────────────────────────────────────────────────────────
def main():
    """Lit les pages déjà téléchargées, en tire les séances nouvelles, les fait
    juger, les écrit, et sort avec 0, 1 ou 2.

    ① RÔLE — Tenir ensemble toute la collecte : le périmètre, la lecture, le
      filtre de fraîcheur, le jugement, l'écriture et le rapport. Ce programme ne
      tourne plus — le 19-09-2026, .github/workflows/collecte_abc.yml lance
      programmes/COLLECTER_ABC_GITHUB.py et pas celui-ci, et gouvernance/SOCLE.csv,
      à la ligne qui porte le chemin de ce fichier, le range en PRESUME avec le motif
      « aucun lanceur detecte » — vérifié à nouveau le 24-09-2026. Ce qu'il faisait
      quand il servait reste exact.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Aucun appelant
      automatique aujourd'hui ; le 10-09-2026, une tâche planifiée Cowork
      téléchargeait les pages avec son outil web puis lançait ce programme avec
      `--pages`.
    ③ ENTRÉE — Ne prend aucun paramètre : elle lit la ligne de commande
      elle-même. Trois choses y sont attendues : le dossier du projet · le dossier
      de sortie · `--pages` suivi du dossier des pages. Et trois sources lues : le
      référentiel, le fichier des cours existant, et une page par valeur.
    ④ CONDITIONS D'ENTRÉE — Au moins deux arguments, l'option `--pages`, et
      programmes/CONTROLER_LES_COURS.py atteignable depuis le dossier du projet.
      Le dossier de sortie doit exister et être accessible en écriture. Le fichier
      des cours, lui, peut manquer : c'est alors une création.
    ⑤ SORTIE — Ne rend rien. Tout passe par le code de sortie, par le rapport
      affiché et par les deux fichiers écrits.
      [rend: rien]
    ⑥ TRAITEMENT — ① arrêter le programme, en affichant le mode d'emploi, s'il y a
      moins de deux arguments · ② relever le dossier des pages, et arrêter s'il
      manque · ③ charger le module de contrôle des cours · ④ relever l'instant du
      passage en heure de Paris · ⑤ lire le référentiel · ⑥ chercher le fichier des
      cours existant parmi quatre emplacements, en relever pour chaque valeur sa
      dernière séance et sa dernière clôture, et le recopier dans le fichier de
      sortie · ⑦ pour chaque valeur : lire sa page, en extraire le tableau,
      écarter ce que la règle d'horloge refuse, ne garder que ce qui est plus
      récent que le fichier, et y inscrire le nom de la valeur · ⑧ soumettre le
      lot entier au contrôle de vraisemblance · ⑨ écrire ce que le contrôle laisse
      passer · ⑩ composer le rapport, l'écrire et l'afficher · ⑪ sortir avec 0, 1
      ou 2.
    ⑦ UNITÉ — Les prix sont en euros, les volumes en titres, les dates au format
      AAAA-MM-JJ. Le seuil par valeur est une DATE, jamais un rang : une séance
      est nouvelle si sa date est strictement plus grande que la dernière au
      fichier. Le plancher qui s'applique à une valeur inconnue du fichier est le
      10-07-2026, la même date que celle du module de contrôle.
    ⑧ POURQUOI — Le lot entier est jugé avant qu'une seule ligne soit écrite : une
      séance fausse rend tout le lot suspect, et le module de contrôle refuse
      alors d'écrire quoi que ce soit. Les clôtures de la veille sont relues et
      passées au contrôle pour que le test de variation puisse tourner ; sans
      elles il ne tourne pas, et le contrôle le dit au lieu de se taire — un test
      muet passe pour un test réussi.
      Le seuil par valeur est relu dans le fichier plutôt que supposé, parce que
      les valeurs ne s'arrêtent pas toutes à la même séance : mesuré le
      19-09-2026 sur donnees/claude_cours_nouveaux.csv, trente-neuf valeurs
      s'arrêtent au 18-09-2026 et une au 10-09-2026.
    ⑨ CE QUI CLOCHE —
      ① Elle écrit le nom de la valeur tel que le référentiel l'orthographie, sans
      le normaliser. Mesuré le 19-09-2026 sur une copie du dépôt : le fichier
      reçoit `AIR LIQUIDE`, `BNP PARIBAS`, `BUREAU VERITAS`, alors qu'il portait
      déjà `AIR_LIQUIDE`, `BNP_PARIBAS`, `BUREAU_VERITAS`. Treize des quarante
      noms du référentiel portent un espace ou un tiret. Le fichier porte alors
      deux orthographes pour la même entreprise. Ce programme s'en tire, parce
      qu'il normalise ce qu'il relit ; tout programme qui ne le fait pas y voit
      deux sociétés distinctes et n'en compte qu'une. C'est ainsi que 26 % des
      lignes d'une mesure ont disparu le 23-08-2026, sans aucune erreur affichée.
      programmes/COLLECTER_ABC_GITHUB.py écrit, lui, le nom normalisé depuis le
      10-09-2026.
      ② Le rapport range sous « SÉANCES REFUSÉES PAR LE CONTRÔLE DE
      VRAISEMBLANCE » des séances qui sont écrites. Mesuré le 19-09-2026 : une
      clôture passant de 31,74 à 44,44 produit la ligne « variation de +40.0 % sur
      VEOLIA le 2026-09-21 » sous ce titre, le programme sort en code 0, et la
      séance est dans le fichier écrit. Le module de contrôle range les alertes à
      part mais les laisse écrivables ; seul un verdict BLOQUANT arrête tout.
      ③ Le compte d'alertes du rapport mélange des séances et un message qui n'en
      est pas un. Quand aucune clôture de la veille n'est disponible, le contrôle
      ajoute la phrase « TEST DE VARIATION NON EFFECTUÉ » à la même liste :
      elle est alors comptée dans « alertes : N » et affichée sous le titre des
      séances refusées, où elle ne désigne aucune séance.
      ④ Le verdict affiché quand il n'y a rien à ajouter est « OK », alors
      qu'aucun contrôle n'a tourné. Mesuré le 19-09-2026 : la variable qui le
      porte vaut « OK » avant tout appel et n'est remplacée que si le lot n'est
      pas vide. Un rapport qui annonce « verdict du contrôle : OK · écrites : 0 »
      ne distingue pas une soirée sans nouveauté d'une soirée où le contrôle n'a
      pas eu lieu.
      ⑤ Le nom du jour de l'en-tête est en anglais. Mesuré le 19-09-2026 : le
      rapport commence par « # COLLECTE ABC BOURSE — Sat 19-09-2026 23h10
      (Paris) », là où tout le dépôt écrit « Sam ». L'heure est juste, seul le nom
      du jour est fautif ; le défaut est consigné au backlog sous A-429, avec sa
      correction volontairement non appliquée tant que le chantier en cours est la
      description du système.
      ⑥ Le fichier écrit s'appelle `cours_nouveaux.csv` dans le dossier de sortie,
      un nom que le dépôt ne porte pas : le 19-09-2026, donnees/ contient
      `claude_cours_nouveaux.csv` et aucun fichier de ce nom-là. Le fichier du
      dépôt n'est donc jamais mis à jour par ce programme, et rien dans le rapport
      ne dit qu'il reste à reporter.
      ⑦ Le rapport porte un nom fixe, `rapport_collecte_abc.md`. Deux passages le
      même jour écrasent le premier sans un mot, et le premier peut avoir échoué
      pour une raison que le second efface.
      ⑧ Le fichier des cours existant est cherché à quatre emplacements et le
      premier trouvé l'emporte. Deux fichiers de même nature à deux endroits sont
      un défaut, jamais une intention : celui qui n'est pas lu vieillit sans que
      rien ne le dise.
      ⑨ La ligne « plus récente sur ABC » du rapport est prise avant le filtre de
      fraîcheur. Pour une valeur d'Amsterdam, elle affiche donc une date qui n'a
      jamais été candidate à l'écriture, et un lecteur qui compare les deux dates
      de cette ligne croit à une perte.
      ⑩ Une page absente fait sortir en code 1 même quand tout le reste a été
      écrit, et un lot bloquant fait sortir en code 2 même quand les pages étaient
      toutes là. Le code de sortie dit donc « quelque chose a manqué » sans dire
      quoi, et c'est le rapport qu'il faut ouvrir.
    ⑩ EFFET — ÉCRIT deux fichiers dans le dossier de sortie : `cours_nouveaux.csv`,
      d'abord copié depuis le fichier des cours existant puis complété par ajout —
      jamais réécrit — et `rapport_collecte_abc.md`, écrasé à chaque passage.
      LIT le référentiel, le fichier des cours existant, et une page par valeur.
      AFFICHE le rapport en entier. MODIFIE le chemin de recherche des modules du
      processus. AUCUN ACCÈS RÉSEAU. Ne touche ni à donnees/cac40_ohlcv.csv, ni à
      la gouvernance, et ne supprime rien.
    ⑪ TERMINAISON — NE REND JAMAIS LA MAIN : elle sort du programme dans tous les
      cas. Trois codes, tous mesurés le 19-09-2026 sur une copie du dépôt : 0
      quand les quarante pages ont été lues et que ce qui devait être écrit l'a
      été · 1 quand au moins une page manque ou qu'un tableau est introuvable, le
      reste étant tout de même écrit · 2 sans argument, sans `--pages`, sans
      module de contrôle, sans référentiel, ou sur un lot BLOQUANT. Et deux de ses
      appels peuvent ne pas revenir : `_importer_controle` et `lire_referentiel`
      sortent en code 2 sans rendre la main. Un troisième peut lever sans être
      rattrapé : l'écriture au fichier des cours refuse une ligne incomplète ou
      une date illisible en levant une erreur, ce qui arrête le programme sans
      écrire le rapport.
      [sort: oui]
    ⑫ DÉFINITIONS
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
      le fichier des cours : le fichier où les séances s'empilent sans jamais être
        réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à
        suivre, avec pour chacune son mnémonique et sa place de cotation.
      le contrôle de vraisemblance : les tests de programmes/CONTROLER_LES_COURS.py
        qui jugent une séance avant qu'elle soit écrite.
      un lot BLOQUANT : un ensemble de séances dont l'une est jugée fausse, ce qui
        fait refuser l'écriture de tout l'ensemble.
      l'outil web : l'outil d'une tâche planifiée Cowork qui ouvre une page et en
        rend un texte écrit par un modèle, jamais la page elle-même.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des
        décisions et des actions du projet
    """
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    projet, sortie = sys.argv[1], sys.argv[2]
    pages = None
    if "--pages" in sys.argv:
        pages = sys.argv[sys.argv.index("--pages") + 1]
    if not pages:
        print("CODE 2 — ce programme ne fait aucun appel réseau : passer --pages <dossier>")
        sys.exit(2)

    C = _importer_controle(projet)
    maintenant = datetime.now(PARIS)
    ref_chemin, valeurs = lire_referentiel(projet)

    # le fichier des cours existant : pour connaître la dernière séance par valeur
    cible = os.path.join(sortie, "cours_nouveaux.csv")
    src_existant = None
    for cand in (os.path.join(projet, "claude_cours_nouveaux.csv"),
                 os.path.join(projet, "claude", "cours_nouveaux.csv"),
                 os.path.join(projet, "cours_nouveaux.csv"),
                 os.path.join(projet, "donnees", "claude_cours_nouveaux.csv")):
        if os.path.isfile(cand):
            src_existant = cand; break
    derniere, cloture_prec = {}, {}
    if src_existant:
        with open(src_existant, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                v = C.normaliser_valeur(r["valeur"]); d = C.normaliser_date(r["date"])
                if d and (v not in derniere or d > derniere[v]):
                    derniere[v] = d
                    try: cloture_prec[v] = float(r["close"])
                    except (ValueError, KeyError): pass
        if src_existant != cible:
            import shutil; shutil.copy(src_existant, cible)

    rapport = [f"# COLLECTE ABC BOURSE — {maintenant.strftime('%a %d-%m-%Y %Hh%M')} (Paris)",
               f"référentiel : {os.path.basename(ref_chemin)} · {len(valeurs)} valeurs",
               f"fichier des cours : {src_existant or '(aucun — création)'}",
               f"ligne du jour acceptée pour Paris : {'OUI' if maintenant.hour >= 18 else 'NON (avant 18h)'} · pour Amsterdam : jamais", ""]
    a_ajouter, echecs, sans_nouveau = [], [], []
    jour = maintenant.strftime("%Y-%m-%d")

    for nom, code, place in valeurs:
        chemin_page = os.path.join(pages, code + ".html")
        if not os.path.isfile(chemin_page):
            echecs.append((nom, code, "page absente")); continue
        texte = open(chemin_page, encoding="utf-8", errors="replace").read()
        seances = extraire(texte)
        if not seances:
            echecs.append((nom, code, "tableau introuvable — 0 ligne")); continue
        nom_n = C.normaliser_valeur(nom)
        seuil = derniere.get(nom_n, DATE_PLANCHER)
        neuves = [s for s in seances_acceptables(seances, place, maintenant, jour) if s["date"] > seuil]
        for s in neuves:
            s["valeur"] = nom
        if neuves:
            a_ajouter += neuves
        else:
            sans_nouveau.append((nom, code, seuil, seances[0]["date"]))

    # contrôle de vraisemblance AVANT d'écrire — c'est CONTROLER_LES_COURS qui juge
    ecrites, refusees, verdict_global, bloquant = 0, [], "OK", ""
    if a_ajouter:
        # CONTROLER_LES_COURS.controler rend (verdict_global, ecrivables, alertes, bloquant)
        # — relevé dans sa docstring le 10-09, pas supposé. Un lot BLOQUANT n'écrit RIEN :
        # une donnée fausse rend tout le lot suspect, c'est voulu par ce module.
        # les clôtures précédentes permettent le test de variation — sans elles il
        # ne tourne pas et le contrôle le dit (mesuré le 10-09 : « TEST NON EFFECTUÉ »)
        verdict_global, bonnes, alertes, bloquant = C.controler(a_ajouter, clotures_precedentes=cloture_prec)
        refusees = list(alertes)
        if bonnes:
            ecrites, _doublons, _vieilles = C.ajouter_au_fichier(bonnes, cible)

    rapport.append(f"## RÉSULTAT")
    rapport.append(f"valeurs lues : {len(valeurs) - len(echecs)}/{len(valeurs)} · séances nouvelles proposées : {len(a_ajouter)} · verdict du contrôle : {verdict_global} · écrites : {ecrites} · alertes : {len(refusees)}")
    if bloquant:
        rapport.append(f"\n## ❌ LOT BLOQUANT — rien n'a été écrit : {bloquant}")
    if echecs:
        rapport.append(f"\n## ⚠️ VALEURS EN ÉCHEC — une valeur attendue qui ne renvoie rien est une ALERTE (chapitre I)")
        for nom, code, motif in echecs: rapport.append(f"- {nom} ({code}) : {motif}")
    if refusees:
        rapport.append(f"\n## ⚠️ SÉANCES REFUSÉES PAR LE CONTRÔLE DE VRAISEMBLANCE")
        for a in refusees: rapport.append(f"- {a}")
    if sans_nouveau:
        rapport.append(f"\n## valeurs sans séance nouvelle ({len(sans_nouveau)})")
        for nom, code, seuil, plus_recente in sans_nouveau:
            rapport.append(f"- {nom} : dernière au fichier {seuil}, plus récente sur ABC {plus_recente}")
    rapport.append(f"\nfichier écrit : {cible}")
    open(os.path.join(sortie, "rapport_collecte_abc.md"), "w", encoding="utf-8").write("\n".join(rapport) + "\n")
    print("\n".join(rapport))
    # R-734bis : un lot BLOQUANT — zéro ligne écrite — ne rend JAMAIS 0. Cowork l'a
    # relevé le 10-09 : c'était le seul défaut qui rendait les trois autres invisibles.
    sys.exit(2 if bloquant else (1 if echecs else 0))


if __name__ == "__main__":
    main()
