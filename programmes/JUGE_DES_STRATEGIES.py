#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCIDÉ · outil · v1.5 · 29-08-2026 · Rôle : juger une strategie a partir de sa fiche.
UN SEUL NUMERO DE VERSION DANS CE FICHIER : ce cartouche et la constante
VERSION plus bas disent la meme chose. Le rapport imprime celui du code, un
lecteur voit celui-ci — deux numeros differents dans le meme fichier etaient
exactement le defaut que la v1.5 corrigeait.

VERSION 1.5 — 29-08-2026. Le juge des stratégies lit le REGISTRE DES STRATEGIES et non
    plus le sas, qui est absorbe. Les TROIS FENETRES sont rendues. La
    PERIODE devient le sixieme champ obligatoire de la porte 0, et la
    fiche de calibrage y passe elle aussi. Le numero de version bouge
    quand le fond bouge : deux rapports de contenus differents ne doivent
    jamais porter le meme numero.

VERSION 1.2 — LE JUGEMENT EST BRANCHE. Le juge des stratégies rendait les gains ; il rend
    desormais les mesures qui disent si ces gains veulent dire quelque chose :
    point mort, episodes independants, coupure sur le TEMPS avec embargo de
    21 seances, gain au pire, pire serie de pertes, pire creux, et l'etalon de
    hasard en deux modes. Toutes ces mesures ont ete produites le 28/08 dans des
    scripts jetables : elles ne vivaient donc NULLE PART. Le juge des stratégies n'en implemente
    aucune, il APPELLE le module de jugement et le module de statistiques (R-708).
    Si le module de jugement manque, le juge des stratégies le DIT au lieu de rendre des gains
    nus en les faisant passer pour un jugement.

VERSION 1.1 — deux defauts releves par relecture adverse le 28/08 :
    · os.walk au lieu de os.listdir. Le juge des stratégies ne voyait pas les sous-dossiers,
      defaut corrige dans le programme du pilote le 26/08 et JAMAIS PORTE ICI.
      Mesure : 76 operations d'un cote, 77 de l'autre, pour le meme juge des stratégies et la
      meme fiche — les cours du jour vivant dans « claude/ », que le disque du
      Chat aplatit a la racine et que l'executant voit reellement.
    · l'absence des cours du jour devient une ALERTE et non une mention noyee
      dans six lignes : elle change le perimetre juge, donc le resultat.
Quand l'appeler : avant toute mise en vie d'une strategie, et pour toute ligne du
registre a l'etat LABO ou QA. Jamais dans une tache automatique : il ne conclut
pas, il rend des chiffres.

LE JUGE DES STRATÉGIES — version generique
Mer 26-08-2026 (Paris)

CE QU'IL FAIT
    Il prend une FICHE de strategie, la joue sur les cours, et rend un rapport
    chiffre. Pas de verdict oui / non : la grille qui le rendra (A-210) n'est pas encore figée.

CE QUI LE REND GENERIQUE, ET C'EST LE POINT CENTRAL
    IL NE COMPREND AUCUN INDICATEUR. Il ne sait pas ce qu'est un CMF ni un CCI.
    La fiche lui dit QUEL MODULE produit les signaux ; il l'appelle.
    Consequence : une strategie fondee sur des indicateurs qui n'existent pas
    encore fonctionnera sans qu'une ligne de ce fichier ne change.
    Le jour ou il faudrait le modifier pour accueillir une idee nouvelle, c'est
    que la conception est fausse.

LE CONTRAT D'UN MODULE DE SIGNAL — la seule chose qu'il doit respecter
    une fonction  f(ohlcv) -> [ {"i": indice_de_la_seance}, ... ]
    ohlcv est la liste des seances d'UNE valeur, triee par date, chaque seance
    etant un dict open/high/low/close/volume/date.
    Tout le reste — periodes, seuils, combinaisons — appartient au module.

LES SORTIES VIENNENT DE MODULE_POSITIONS, JAMAIS D'AILLEURS
    Decouvert le 25-08-2026 (A-289) : deux mecaniques de sortie coexistaient.
    Le module de signal sortait au prix THEORIQUE, MODULE_POSITIONS au prix
    REELLEMENT disponible. Mesure du 26/08 (A-290) : 19 operations sur 100
    sortent sur un gap, ecart de plus 12 501 euros, soit 11,2 % de l'etalon.
    MODULE_POSITIONS fait foi puisque c'est lui qui pilote les positions reelles.

CE QU'IL NE FAIT JAMAIS
    Il ne conclut pas · il n'ecrit dans aucun fichier de gouvernance ·
    il ne modifie aucune strategie · il ne choisit pas ses essais.

CE QU'IL REFUSE, ET C'EST LA OU EST SA VALEUR
    PORTE 0 — une fiche incomplete est refusee AVANT tout calcul, sans consommer
    d'essai. Ce n'est pas un rejet de l'idee : c'est une mise en attente de sa
    fiche (A-212, A-281).
    CALIBRAGE — si l'instrument ne retrouve pas un resultat connu, ARRET TOTAL.

USAGE
    python3 JUGE_DES_STRATEGIES.py <dossier_projet> [ID_FICHE]

① RÔLE — Rejouer une stratégie sur l'historique des cours et rendre un rapport
  chiffré, sans jamais conclure. Il lit le registre des stratégies
  `donnees/cac40_strategies.csv`, écarte les lignes closes, refuse les fiches
  incomplètes, vérifie qu'il retrouve un résultat connu, puis joue chaque fiche
  restante et affiche ce qu'elle aurait donné. Mesuré le 20-09-2026 sur une
  copie du dépôt, `python3 programmes/JUGE_DES_STRATEGIES.py .` : 68 fiches lues,
  31 écartées parce que leur état de vie est clos, 3 passées, jugées, et code
  de sortie 0.
  ET IL CHOISIT LES FICHIERS DE COURS QUE TOUT LE RESTE LIRA — ce que son nom
  ne dit pas. Sa fonction `fichiers_de_cours` désigne le fichier d'historique à
  ouvrir, et trois autres programmes le lui demandent au lieu de le décider
  eux-mêmes. Ce nom trompeur est relevé au BACKLOG sous l'action A-426, ouverte
  le 19-09-2026 : « rien dans le nom ne dit qu'il choisit les fichiers de cours
  et les charge ».
② CONTEXTE D'APPEL — Deux usages, et le second n'a pas besoin de son programme
  principal.
  · À LA MAIN, par Jean-Luc ou par le Chat, avant toute mise en vie d'une
  stratégie. Son propre cartouche écrit : « Jamais dans une tache automatique :
  il ne conclut pas, il rend des chiffres. »
  · COMME BIBLIOTHÈQUE, CHAQUE SOIR, SANS QUE PERSONNE NE LE LANCE.
  `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` ligne 152 fait
  `import JUGE_DES_STRATEGIES as B`, puis appelle `B.fichiers_de_cours` ligne 162,
  `B.charger_cours` ligne 167, `B.charger_module` ligne 153 et `B.cle_valeur`
  lignes 203 et 281. Ce programme-là est lancé par
  `.github/workflows/collecte_abc.yml` ligne 136, dans le passage automatique
  programmé à 18h UTC du lundi au vendredi. `programmes/TENIR_LES_POSITIONS.py`
  l'appelle aussi, lignes 376 et 463, et il est lancé ligne 171 du même
  fichier de circuit. `programmes/JUGER_SUR_8_CRITERES.py` l'appelle lignes
  1180, 1193 et 1202. Relevé le 20-09-2026 en cherchant chaque nom de fonction
  dans les 34 fichiers de `programmes/`.
③ ENTRÉE — La ligne de commande, deux arguments, tous deux facultatifs :
  le dossier racine où chercher les fichiers, `/mnt/project` par défaut, et
  l'identifiant d'une seule fiche à juger, par exemple `C5E10-QA-V1`. Sans ce
  second argument, toutes les fiches recevables sont jouées.
④ CONDITIONS D'ENTRÉE — Python 3.9 ou plus récent, pour `zoneinfo`. Quatre
  fichiers doivent exister sous la racine, sans quoi rien n'est produit : le
  registre des stratégies, les cours, le module de signal et le module de
  positions. Aucun accès réseau n'est nécessaire.
⑤ SORTIE — Un code de sortie, et rien d'autre : 0 quand le rapport est allé au
  bout, ou quand aucune fiche n'était recevable ; 1 quand un fichier
  indispensable manque, et 1 quand le calibrage échoue. Tout le reste est
  affiché à l'écran.
⑥ TRAITEMENT — ① afficher la version et l'heure de Paris · ② relever les sept
  fichiers dont il a besoin et afficher leur nom réel et leur empreinte ·
  ③ signaler tout nom qui répond sous plusieurs graphies · ④ s'arrêter si un
  fichier indispensable manque · ⑤ charger les cours, la table des mnémoniques
  et les quatre modules · ⑥ lire le registre des stratégies et n'y garder que
  les lignes à l'état LABO ou QA · ⑦ passer chaque fiche par la porte 0 ·
  ⑧ rejouer une stratégie de référence et s'arrêter si le nombre d'opérations
  attendu n'est pas retrouvé · ⑨ pour chaque fiche recevable, jouer, résumer,
  puis appeler le module de jugement · ⑩ rappeler que le juge des stratégies ne conclut pas.
⑦ UNITÉ — Les gains sont des EUROS, sur 100 000 € engagés par opération. Les
  objectifs de gain et les pertes acceptées se lisent en POURCENTS dans les
  fiches et se manipulent en FRACTIONS dans le code : 0,040 vaut +4 %. Les
  horizons et les embargos se comptent en SÉANCES de bourse. Les taux de
  réussite et les points morts sont des POURCENTS entre 0 et 100. Les empreintes
  affichées sont des nombres hexadécimaux de 16 caractères.
⑧ POURQUOI — Il ne comprend aucun indicateur, et c'est délibéré : la fiche lui
  dit quel module produit les signaux, et il l'appelle. Une stratégie fondée sur
  des indicateurs qui n'existent pas encore fonctionnera donc sans qu'une ligne
  de ce fichier ne change. Le jour où il faudrait le modifier pour accueillir
  une idée nouvelle, la conception serait fausse.
  ET LES SEUILS D'UNE STRATÉGIE NE SONT PAS ÉCRITS ICI. L'objectif de gain, la
  perte acceptée et l'horizon sont lus dans la ligne du registre des stratégies
  `donnees/cac40_strategies.csv`, jamais dans le code : `jouer` les prend dans
  `fiche["tp"]`, `fiche["sl"]` et `fiche["horizon"]`, et `juger` fait de même.
  Mesuré le 20-09-2026 : la ligne `C5E10-QA-V1` du registre porte `+4.0%`,
  `-2.5%` et `20`, et le rapport affiche « TP +4.0% . SL -2.5% . horizon 20
  seances ». La même exigence est écrite au REGISTRE sous la règle R-201, qui
  décrit la stratégie C5-ETENDU-10 : « TP +4 % · SL −2,5 % · 20 séances ».
  UNE EXCEPTION, ET ELLE EST UN DÉFAUT : la fiche de calibrage construite par
  `calibrer` recopie ces trois chiffres dans le code du juge des stratégies.
⑨ CE QUI CLOCHE —
  ① UNE SEULE FICHE MAL REMPLIE ARRÊTE TOUT LE RAPPORT. `porte_0` rend DEUX
  valeurs quand la période est mal formée, et TROIS dans tous les autres cas ;
  ses deux appelants en attendent trois. Mesuré le 20-09-2026 en ajoutant au
  registre d'une copie une fiche `ZZ-TEST` dont la période vaut « du 2 janvier
  au 10 juillet » : le juge des stratégies affiche les 36 premières fiches, puis s'arrête sur
  « ValueError: not enough values to unpack (expected 3, got 2) », ligne 831,
  code de sortie 1. Aucune des trois fiches recevables n'a été jugée. C'est
  exactement ce que la porte 0 existe pour éviter : refuser une fiche sans
  arrêter le travail.
  ② LE JUGE DES STRATÉGIES N'APPELLE PAS SA PROPRE FONCTION DE CHOIX DES COURS. `main` va
  chercher `donnees/cac40_ohlcv.csv` et `donnees/claude_cours_nouveaux.csv` par
  leur nom, alors que `fichiers_de_cours` désigne `donnees/cours_maitre.csv`.
  Mesuré le 20-09-2026 : le rapport affiche « cours cac40_ohlcv.csv » et
  « cours du jour claude_cours_nouveaux.csv », tandis que
  `fichiers_de_cours` rend `donnees/cours_maitre.csv`, qui existe. Le périmètre
  est le même aujourd'hui — 40 valeurs, 694 dates, du 2024-01-02 au 2026-09-18
  des deux côtés — parce que l'historique figé s'arrête au 2026-07-10 et que le
  fichier du jour reprend au 2026-07-13, sans un jour de recouvrement. Le jour
  où le fichier du jour portera moins de séances que le trou ouvert depuis le
  2026-07-10, le juge des stratégies jugera sur un historique amputé pendant que les
  programmes du soir liront le fichier maître complet, et rien ne le dira.
  ③ LE CALIBRAGE CRIE QUE LES DONNÉES ONT CHANGÉ ALORS QU'ELLES SONT LES BONNES.
  Le golden déclare 25 111 lignes et l'empreinte `e472c09da5679ec3` ; le témoin
  déposé porte cette empreinte exacte, mais le juge des stratégies compte ses lignes en
  comptant l'en-tête, donc 25 112. Mesuré le 20-09-2026, sortie réelle :
  « ATTENTION - LES DONNEES ONT CHANGE depuis le golden : 25112 lignes contre
  25111, empreinte e472c09da5679ec3 contre e472c09da5679ec3. » L'alerte
  s'affiche à chaque passage, sur les données exactes de la référence, et une
  alerte permanente apprend à ne plus regarder.
  ④ L'ABSENCE DU MODULE DE STATISTIQUES N'EST PAS ANNONCÉE, CELLE DU MODULE DE
  JUGEMENT L'EST. `main` affiche « ALERTE - LE MODULE DE JUGEMENT EST
  INTROUVABLE » quand il manque, mais rien du tout pour le module de
  statistiques. Mesuré le 20-09-2026 en appelant `juger` avec ce module à
  `None` : le rapport perd deux mesures sur onze et les remplace par
  « VOISINAGE non mesure : 'NoneType' object has no attribute
  'calculer_stabilite_parametrique' » et « CREUX non mesure : 'NoneType' object
  has no attribute 'calculer_time_underwater' », deux lignes noyées au milieu
  de quinze autres. Un lecteur pressé lit un rapport complet.
  ⑤ UN MODULE EFFACÉ CONTINUE DE TOURNER DEPUIS SON CACHE. `trouver` accepte
  n'importe quel fichier dont le nom commence par le motif, y compris un
  `.pyc` rangé dans `__pycache__`, et `charger_module` le charge sans broncher.
  Mesuré le 20-09-2026 en retirant le module de statistiques d'une copie :
  `trouver` rend
  `programmes/__pycache__/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.cpython-311.pyc`,
  le module se charge, et le rapport affiche le voisinage comme si de rien
  n'était. Dans le même temps, `trouver_tous`, qui est censé alerter sur les
  graphies multiples, ignore explicitement `__pycache__` et rend une liste vide.
  Les deux fonctions ne regardent donc pas le même dépôt : celle qui CHOISIT
  accepte un fichier compilé, celle qui ALERTE ne le voit pas.
  ⑥ LE COMMENTAIRE QUI JUSTIFIE LE TRI DES FICHES COMPTE FAUX. Il annonce, au
  30-08-2026, « 68 lignes dont 30 VECUE-PUIS-ARCHIVEE, 1 JAMAIS_VECUE et
  1 PRODUCTION ». Mesuré le 20-09-2026 sur le fichier réel : 35 LABO,
  30 VECUE-PUIS-ARCHIVEE, 2 QA, 1 JAMAIS_VECUE, et AUCUNE ligne en PRODUCTION.
  Un lecteur qui suit le commentaire pour recompter ne retrouve pas le total.
  ⑦ LA MÊME EMPREINTE EST CALCULÉE À TROIS ENDROITS. La fonction `empreinte`
  existe, et deux autres passages refont le même calcul à la main : `main` pour
  le témoin du golden, `calibrer` pour les cours. Relevé le 20-09-2026 :
  `hexdigest()[:16]` apparaît 3 fois dans le fichier, `empreinte(` 2 fois. Un
  chiffre qui existe ailleurs ne se recopie pas (R-708), et une correction faite
  à l'un des trois endroits ne touchera pas les deux autres.
⑩ EFFET — N'ÉCRIT AUCUN FICHIER et ne touche pas au réseau : recherche de
  `open(` en écriture, de `.write(`, de `makedirs`, de `remove(`, de `requests`,
  de `urllib`, de `socket` et de `subprocess` dans ce fichier le 20-09-2026,
  zéro occurrence, et `git status` reste vide après un passage complet sur une
  copie du dépôt. Il LIT sept fichiers et EXÉCUTE le code de quatre modules
  Python qu'il charge depuis le disque : ce qu'ils font, il le fait.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par `main`. Et un de ses
  appels peut ne pas revenir : `main` lève une erreur non rattrapée sur une
  fiche dont la période est mal formée, mesuré le 20-09-2026.
⑫ DÉFINITIONS
  jetons illimités : la seconde comptabilité, où toute position s'ouvre
    sans limite ; elle ne correspond à aucun portefeuille réel.
  l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ;
    deux fichiers de même empreinte ont le même contenu
  l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de
    référence qui n'est jamais réécrit
  l'horizon : le nombre de séances pendant lesquelles une position est
    tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
  l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
    d'acheter, désignées par leur mnémonique
  l'étalon de hasard : le résultat qu'obtiendraient des entrées tirées au
    sort jouées aux mêmes règles, et auquel la stratégie doit être
    comparée
  la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage
    sur vingt
  la fiche : la ligne d'une stratégie au registre des stratégies
    `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
    acceptée, son horizon et son univers
  la partie jamais vue : la fin de la période, celle sur laquelle la
    stratégie n'a pas été réglée, et donc la seule qui prouve quelque
    chose
  la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
    sans consommer d'essai.
  la racine : le dossier reçu sur la ligne de commande, celui dont on
    classe les fichiers — en général un clone du dépôt.
  le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et
    des actions du projet, où chaque ligne porte un identifiant en `A-`
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
    stratégie sur l'historique des cours et rend la liste de ses
    opérations
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige
    de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
    n'en étant qu'une copie de lecture
  le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
    chiffres de référence ; tout écart à données identiques est une
    régression.
  le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
    l'historique des cours et n'est jamais réécrit.
  le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les
    mesures disant si un gain veut dire quelque chose.
  le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
    taux de frais et des règles de sortie d'une position.
  le module de signal : le programme qui décide quelles valeurs acheter
  le module de statistiques : le programme qui porte le voisinage des
    réglages et le pire creux,
    `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
  le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
    les règles numérotées du projet
  le registre des stratégies : le fichier `cac40_strategies.csv`, une
    ligne par stratégie, qui porte leur état civil — identifiant,
    réglages, résultats connus
  le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste
    des valeurs à suivre, avec pour chacune son mnémonique et sa place
    de cotation.
  le SL : la perte acceptée qui ferme la position, une fraction du prix
    d'entrée — 0,025 vaut −2,5 %.
  le taux de réussite : la part des opérations qui se sont refermées sur
    un gain, écrite en pourcent
  le TP : l'objectif de gain qui ferme la position, une fraction du prix
    d'entrée — 0,040 vaut +4 %.
  le témoin du golden : la copie conservée des cours qui ont produit
    les chiffres figés,
    `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
  un jeton : la comptabilité où une seule position peut être ouverte à la
    fois par stratégie ; un signal reçu pendant une position est ignoré.
  un mnémonique : le code court d'une valeur de bourse, `TTE` pour
    TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
  un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte
    que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
  une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
  une séance : une journée de bourse pour une valeur, avec son ouverture,
    son plus haut, son plus bas, sa clôture et son volume.
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
  CCI : l'indice du canal des matières premières, qui mesure de combien le cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200 et +200.
  CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une valeur ; sans unité, borné à ±1.
  PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
  QA : l etat d une strategie validee sur l historique mais qui n a pas encore realise assez d operations reelles pour etre jugee.
  la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
  le sas : les fiches de strategie en etat LABO a l'etat civil, celles qui attendent d'etre jugees par le juge des stratégies
  une fiche de strategie : une ligne du registre des strategies, qui porte son identifiant, son etat de vie et son univers
"""

import csv
import hashlib
import importlib.util
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from COMMUN import lire_horizon       # la seule lecture d'un horizon (R-708, défaut 4 de A-491)

VERSION = "generique-1.5"
PARIS = ZoneInfo("Europe/Paris")
JOURS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

# LA PERIODE EST UN CHAMP OBLIGATOIRE, au meme titre que les cinq autres.
# Ajoutee le 29-08-2026 sur proposition de la relecture adverse, apres le cas
# fondateur du jour : declarer une periode a fait passer les DEUX strategies
# vivantes de « cas defavorable perdant » a « au-dessus du point mort », sans
# qu'une ligne de leur strategie ne bouge. QA-V1 de 38,7 a 52,4 %, OBS-V1 de
# 37,0 a 45,7 %, pour un point mort de 43,1 %.
# MECANIQUE : la frontiere 70/30 se calcule sur le calendrier de la PERIODE.
# Sans periode declaree, le juge des stratégies prenait tout l'historique disponible — donc un
# perimetre qui BOUGE a chaque seance ajoutee. Les chiffres changeaient alors
# sans que la strategie change, et aucune comparaison dans le temps n'etait
# possible.
# POURQUOI UN REFUS ET NON UNE ALERTE : une alerte apres calcul se tolere, et
# l'on finit par la lire comme du bruit — c'est ce qui est arrive au maillon 14
# du radar pendant des semaines. Un refus AVANT calcul ne se tolere pas.
# La dette se resorbe alors fiche par fiche, au moment ou chacune devient utile,
# au lieu d'un chantier de 33 fiches dont 32 echouent deja pour d'autres champs.
CHAMPS_OBLIGATOIRES = ["indicateurs", "univers", "tp", "sl", "horizon", "periode"]
VIDE = ("", "-", "\u2014", "a renseigner", "\u00e0 renseigner")


def horodatage():
    """Rend la date et l'heure de Paris, prêtes à afficher.

    ① RÔLE — Dater le rapport du juge des stratégies, pour qu'une sortie collée ailleurs dise
      elle-même de quand elle date. Sans cela, deux rapports d'un même jour et
      d'une même stratégie seraient impossibles à distinguer.
    ② CONTEXTE D'APPEL — `main`, une seule fois, pour la première ligne affichée.
      Aucun autre appelant : recherche du nom dans les 34 fichiers de
      `programmes/` le 20-09-2026, un seul appel, celui de `main`.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Que la base de fuseaux horaires du système connaisse
      `Europe/Paris`. Le fuseau est lu une fois au chargement du programme, dans la
      constante `PARIS`.
    ⑤ SORTIE — UNE valeur : un texte. Exemple réel, mesuré le 20-09-2026 :
      `Dim 20-09-2026 00h15 (Paris)`.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander l'instant présent dans le fuseau de Paris ·
      ② traduire le jour de la semaine par la liste `JOURS`, qui porte les sept
      abréviations françaises · ③ coller ce jour devant la date et l'heure.
    ⑦ UNITÉ — Une DATE et une HEURE, en heure de Paris, à la minute.
    ⑧ POURQUOI — L'heure de Paris, et jamais celle de la machine : le circuit du
      soir tourne sur des machines réglées en temps universel, et une heure lue
      telle quelle y serait décalée de une ou deux heures selon la saison. Le jour
      de la semaine est écrit en toutes lettres parce qu'un rapport daté d'un
      samedi ou d'un dimanche ne peut pas porter de séance de bourse nouvelle, et
      qu'on doit le voir sans compter.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun : elle lit l'horloge, n'écrit rien, n'affiche rien elle-même.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne termine le
      programme.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    n = datetime.now(PARIS)
    return f"{JOURS[n.weekday()]} {n.strftime('%d-%m-%Y %Hh%M')} (Paris)"


def empreinte(chemin):
    """Rend l'empreinte d'un fichier, pour dire lequel a été lu.

    ① RÔLE — Donner à chaque fichier relevé une carte d'identité courte, pour que
      deux rapports produits à deux moments puissent être comparés fichier par
      fichier. Deux empreintes identiques disent que l'octet n'a pas bougé ; deux
      empreintes différentes disent qu'il a bougé, même si le nom et la date
      n'ont pas changé.
    ② CONTEXTE D'APPEL — `main`, sept fois, une par fichier relevé : le registre
      des stratégies, les cours, les cours du jour, le référentiel des valeurs, le
      module de signal, le module de positions et le golden. Jamais appelée
      ailleurs.
    ③ ENTRÉE — `chemin` : le chemin d'un fichier existant. Un seul appelant,
      `main`, qui passe le résultat de `trouver`, par exemple
      `donnees/cac40_ohlcv.csv`.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit exister et se lire. `main` ne
      l'appelle que sur un chemin non vide, mais ne vérifie pas davantage.
    ⑤ SORTIE — UNE valeur : un texte de 16 caractères hexadécimaux. Exemple réel,
      mesuré le 20-09-2026 sur `donnees/cac40_ohlcv.csv` : `10e71dc94aed4ef2`.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir le fichier en octets · ② le lire EN ENTIER d'un seul
      coup · ③ en calculer l'empreinte SHA-256 · ④ n'en garder que les
      16 premiers caractères.
    ⑦ UNITÉ — Un NOMBRE HEXADÉCIMAL de 16 caractères.
    ⑧ POURQUOI — L'empreinte porte sur les octets et non sur le nom, parce que
      plusieurs fichiers du projet portent le même nom à des endroits différents et
      que le nom ne dit rien de leur contenu. Seize caractères suffisent : la
      comparaison se fait à l'œil, entre deux rapports collés l'un sous l'autre.
    ⑨ CE QUI CLOCHE —
      ① Le même calcul est réécrit ailleurs au lieu d'appeler cette fonction.
      `main` le refait à la main pour le témoin du golden, et `calibrer` le refait
      pour les cours. Relevé le 20-09-2026 : `hexdigest()[:16]` apparaît 3 fois
      dans le fichier, l'appel `empreinte(` seulement 2. Un chiffre qui existe
      ailleurs ne se recopie pas (R-708) : le jour où la longueur retenue changera,
      deux des trois endroits garderont l'ancienne.
      ② Le fichier entier est chargé en mémoire. Sur les cours, c'est 1,4 million
      d'octets mesurés le 20-09-2026, et cela ne gêne pas ; sur un fichier plus
      gros, rien ne borne la lecture.
    ⑩ EFFET — LIT un fichier en entier. N'écrit rien, n'affiche rien, ne touche
      pas au réseau.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER une erreur non
      rattrapée si le fichier n'existe pas ou n'est pas lisible ; `main` ne la
      rattrape pas, et le programme s'arrêterait alors.
      [sort: non]
    ⑫ DÉFINITIONS
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ;
        deux fichiers de même empreinte ont le même contenu
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste
        des valeurs à suivre, avec pour chacune son mnémonique et sa place
        de cotation.
      le témoin du golden : la copie conservée des cours qui ont produit
        les chiffres figés,
        `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def trouver_tous(base, *motifs):
    """Rend TOUS les chemins qui repondent, pour qu'on VOIE qu'il y en a
    plusieurs au lieu d'en prendre un au hasard.

    POURQUOI : mesure du 29-08-2026. Le registre des candidates existait DEUX
    FOIS au projet — a underscores, a jour, et a espaces, perime du 23/08 ou
    tous les champs valent « a renseigner ». Le juge des stratégies prenait le bon, mais PAR
    COINCIDENCE DE NOMMAGE : trouver() essaie le motif tel qu'il est ecrit
    avant toute autre graphie, et le motif s'ecrit avec des underscores.
    Graphies inversees, il aurait pris le PERIME — CAND-02 aurait ete refusee a
    la porte 0 pour « champs manquants », et RIEN n'aurait dit que ce n'etait
    pas le bon fichier. Plusieurs fichiers du projet portent deja des espaces la
    ou on les nomme avec des underscores.

    ① RÔLE — Faire voir qu'un même nom répond sous plusieurs graphies, pour que le
      choix silencieux d'un fichier parmi deux devienne une alerte imprimée.
      `trouver` en prend UN et se tait ; cette fonction les rend TOUS.
    ② CONTEXTE D'APPEL — `main`, quatre fois, juste après le relevé des fichiers
      et avant leur affichage, sur quatre motifs : `cac40_strategies.csv`,
      `cac40_ohlcv.csv`, `MODULE_C5_ETENDU_10` et `MODULE_POSITIONS.py`. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `base` : le dossier racine à parcourir · `motifs` : un ou plusieurs
      noms ou débuts de nom, donnés les uns après les autres. Un seul appelant,
      `main`, qui passe la racine reçue sur la ligne de commande et un seul motif
      par appel.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une racine vide rend une liste vide sans
      lever.
    ⑤ SORTIE — UNE valeur : la liste des chemins trouvés, dans l'ordre de
      parcours, sans doublon, et VIDE si rien ne répond. Mesuré le 20-09-2026 sur
      le dépôt : 1 chemin pour `MODULE_C5_ETENDU_10`, 1 pour `golden_tests_`.
      [rend: 1]
    ⑥ TRAITEMENT — ① descendre tous les dossiers sous la racine · ② sauter
      `__pycache__` et tout fichier `.pyc` ou `.pyo` · ③ pour chaque fichier,
      remplacer les espaces par des soulignés et passer en minuscules · ④ garder
      celui dont le nom vaut le motif, ou commence par le motif privé de son
      extension · ⑤ ne garder qu'une fois chaque chemin.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS.
    ⑧ POURQUOI — Le motif se calibre avant de servir (R-720) : la première version
      exigeait le nom EXACT alors que `trouver` accepte le simple début de nom. Le
      garde-fou ne couvrait donc que les noms fixes et laissait passer les noms
      datés, qui sont la majorité du projet. Mesuré le 29-08-2026 : deux copies du
      module de signal côte à côte, une à espaces et une à soulignés, `trouver_tous`
      rendait ZÉRO chemin et n'alertait pas pendant que `trouver` en prenait un en
      silence. Un motif qui ne trouve rien ne prouve rien.
    ⑨ CE QUI CLOCHE —
      ① ELLE NE REGARDE PAS AU MÊME ENDROIT QUE LA FONCTION QU'ELLE SURVEILLE.
      `trouver` accepte un fichier compilé rangé dans `__pycache__` ; celle-ci les
      écarte explicitement. Mesuré le 20-09-2026 en retirant le module de
      statistiques d'une copie : `trouver` rend
      `programmes/__pycache__/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.cpython-311.pyc`
      et le module se charge, tandis que `trouver_tous` rend une liste vide. La
      fonction qui alerte est donc aveugle à un choix que la fonction qui décide
      vient de faire.
      ② ELLE PARCOURT AUSSI `archives/`. Une version rangée en archive sous un nom
      commençant par le même motif serait comptée comme une graphie concurrente,
      alors que l'archive est justement l'endroit prévu pour les versions tombées.
      Aucune alerte de ce genre ne s'est déclenchée le 20-09-2026 sur le dépôt, les
      quatre motifs surveillés ne répondant qu'une fois chacun.
      ③ Le critère épelle des noms au lieu de porter sur une propriété. La question
      qui tranche tient en une phrase : si je renomme un fichier, mon contrôle
      change-t-il d'avis ? Ici oui.
    ⑩ EFFET — LIT la liste des noms de tous les dossiers sous la racine. N'écrit
      rien, ne touche pas au réseau, n'affiche rien : elle rend une liste que son
      appelant affiche.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne
      termine le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      la racine : le dossier reçu sur la ligne de commande, celui dont on
        classe les fichiers — en général un clone du dépôt.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
        n'en étant qu'une copie de lecture
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le module de statistiques : le programme qui porte le voisinage des
        réglages et le pire creux,
        `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      un motif : un morceau de nom passé à une fonction de recherche, par
        exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du
        fichier.
      une graphie : l'une des façons dont un même nom de fichier est écrit
        selon le canal par lequel on le lit — avec espaces ou tirets bas,
        avec ou sans accents
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    out = []
    if not base:
        return out
    # LE MOTIF SE CALIBRE AVANT DE S'EN SERVIR (R-720). La premiere version
    # exigeait le nom EXACT alors que trouver() accepte le PREFIXE : le garde-fou
    # ne couvrait donc que les noms fixes, et laissait passer les noms DATES qui
    # sont la majorite du projet. Mesure du 29/08 : deux copies du module de
    # signal cote a cote, une a espaces et une a soulignes — trouver_tous rendait
    # ZERO chemin, aucune alerte, pendant que trouver() en prenait un en silence.
    # On accepte donc le prefixe, extension otee, comme trouver().
    for d, _, fs in os.walk(base):
        if "__pycache__" in d:
            continue                      # un fichier compile n'est pas une graphie
        for f in sorted(fs):
            if f.endswith((".pyc", ".pyo")):
                continue
            nf = f.replace(" ", "_").lower()
            for m in motifs:
                racine = re.sub(r"\.(md|py|csv|json)$", "",
                                m.replace(" ", "_").lower())
                if racine and (nf == m.replace(" ", "_").lower()
                               or nf.startswith(racine)):
                    p = os.path.join(d, f)
                    if p not in out:
                        out.append(p)
    return out


def trouver(base, *motifs):
    """Les noms existent sous deux graphies (R-719). On ne suppose jamais.

    ① RÔLE — Retrouver un fichier dont on ne connaît ni l'orthographe exacte ni le
      dossier. Les fichiers du projet portent tantôt des espaces, tantôt des
      soulignés, et leur nom finit souvent par une date qui change : chercher le
      nom exact ne marcherait qu'un jour sur deux.
    ② CONTEXTE D'APPEL — `main`, neuf fois, pour le registre des stratégies, les
      cours, les cours du jour, le référentiel des valeurs, le module de signal, le
      module de positions, le golden, le module de jugement, le module de
      statistiques et le témoin du golden. Jamais appelée ailleurs.
    ③ ENTRÉE — `base` : le dossier racine à fouiller · `motifs` : un ou plusieurs
      noms ou débuts de nom, essayés dans l'ordre donné. Un seul appelant, `main`,
      qui passe la racine reçue sur la ligne de commande ; un seul motif par appel
      sauf pour les cours du jour, où `claude_cours_nouveaux.csv` est essayé avant
      `cours_nouveaux.csv`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une racine inexistante rend `None`.
    ⑤ SORTIE — UNE valeur : le chemin du premier fichier retenu, ou `None` si
      aucun ne répond. Exemple réel, mesuré le 20-09-2026 : `trouver` sur
      `golden_tests_` rend `gouvernance/golden_tests_Sam_01-08-2026_20h19.json`.
      [rend: 1]
    ⑥ TRAITEMENT — ① essayer chaque motif à la racine, tel quel, puis avec les
      soulignés changés en espaces, puis l'inverse · ② sinon, descendre tous les
      dossiers et prendre le premier fichier dont le nom vaut le motif aux espaces
      près · ③ sinon, descendre à nouveau et prendre le premier dont le nom, mis en
      majuscules, COMMENCE par le motif privé de son extension · ④ sinon `None`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les sous-dossiers comptent. Ce défaut avait été corrigé dans le
      programme du pilote le 26-08-2026 et n'avait pas été porté ici : le disque
      monté du Chat aplatit les sous-dossiers à la racine, celui de l'exécutant
      non. Résultat mesuré le 28-08-2026 : le juge des stratégies rendait 76 opérations d'un côté
      et 77 de l'autre pour la même fiche, sans le dire, les cours du jour vivant
      dans un sous-dossier.
    ⑨ CE QUI CLOCHE —
      ① ELLE ACCEPTE UN FICHIER COMPILÉ DU CACHE PYTHON. La troisième passe ne
      regarde que le début du nom et ne filtre aucune extension. Mesuré le
      20-09-2026 en retirant le module de statistiques d'une copie du dépôt :
      `trouver` rend
      `programmes/__pycache__/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.cpython-311.pyc`,
      `charger_module` le charge sans erreur, et le rapport affiche le voisinage des
      réglages comme si le module vivait toujours. Un fichier effacé du dépôt
      continue donc de faire tourner le système depuis son cache, et le passage de
      `main` qui alerte sur les graphies multiples ne le voit pas.
      ② ELLE PARCOURT `archives/`, OÙ VIVENT LES VERSIONS TOMBÉES. Rien n'écarte ce
      dossier, et le premier fichier trouvé gagne. L'ordre de descente des dossiers
      n'est pas garanti d'un système à l'autre, si bien qu'une version archivée peut
      être retenue à la place de la vivante sans qu'un mot ne soit affiché.
      ③ LE PREMIER TROUVÉ GAGNE, ET IL N'EST PAS ANNONCÉ COMME UN CHOIX. C'est
      `main` qui alerte, et seulement sur quatre motifs sur dix : le module de
      jugement, le module de statistiques, le référentiel, les cours du jour, le
      golden et le témoin du golden ne sont pas surveillés. Relevé le 20-09-2026
      dans la boucle d'alerte de `main`, qui porte sur `cac40_strategies.csv`,
      `cac40_ohlcv.csv`, `MODULE_C5_ETENDU_10` et `MODULE_POSITIONS.py`.
      ④ Le motif vide passerait tout. Un motif réduit à une extension, comme
      `.csv`, donnerait une racine vide après retrait de l'extension, et la
      troisième passe retiendrait alors le premier fichier venu, tout nom
      commençant par la chaîne vide. Aucun appelant ne le fait aujourd'hui.
    ⑩ EFFET — LIT les noms des fichiers de tous les dossiers sous la racine.
      N'ouvre aucun fichier, n'écrit rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main, avec un chemin ou `None`. Elle ne lève
      pas. Aucun de ses appels ne termine le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      l'exécutant : le service qui lance les programmes du soir sans
        intervention humaine
      la racine : le dossier reçu sur la ligne de commande, celui dont on
        classe les fichiers — en général un clone du dépôt.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
        n'en étant qu'une copie de lecture
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les
        mesures disant si un gain veut dire quelque chose.
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le module de statistiques : le programme qui porte le voisinage des
        réglages et le pire creux,
        `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste
        des valeurs à suivre, avec pour chacune son mnémonique et sa place
        de cotation.
      le témoin du golden : la copie conservée des cours qui ont produit
        les chiffres figés,
        `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
      un motif : un morceau de nom passé à une fonction de recherche, par
        exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du
        fichier.
      une graphie : l'une des façons dont un même nom de fichier est écrit
        selon le canal par lequel on le lit — avec espaces ou tirets bas,
        avec ou sans accents
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    
      la boucle : la tache planifiee qui lit les signaux et rend compte
"""
    for m in motifs:
        for essai in (m, m.replace("_", " "), m.replace(" ", "_")):
            p = os.path.join(base, essai)
            if os.path.exists(p):
                return p
    # LES SOUS-DOSSIERS COMPTENT. Ce defaut avait ete corrige dans le programme
    # du pilote le 26/08 et n'avait PAS ete porte ici : le disque monte du Chat
    # aplatit les sous-dossiers a la racine, celui de l'executant non. Resultat
    # mesure le 28/08 : le juge des stratégies rendait 76 operations d'un cote et 77 de l'autre,
    # sans le dire — les cours du jour vivant dans « claude/ ».
    for m in motifs:
        for d, _, fs in os.walk(base):
            for f in fs:
                if f == m or f.replace(" ", "_") == m.replace(" ", "_"):
                    return os.path.join(d, f)
    for d, _, fs in os.walk(base):
        for f in sorted(fs):
            norme = f.replace(" ", "_").upper()
            for m in motifs:
                racine = re.sub(r"\.(MD|PY|CSV|JSON)$", "",
                                m.replace(" ", "_").upper())
                if norme.startswith(racine):
                    return os.path.join(d, f)
    return None


def charger_module(chemin, nom):
    """Charge un fichier Python et rend le module, prêt à l'appel.

    ① RÔLE — Permettre au juge des stratégies d'appeler du code qu'il ne connaît pas à l'avance.
      La fiche d'une stratégie dit quel module produit ses signaux ; le juge des stratégies doit
      donc charger un fichier dont il n'apprend le chemin qu'à l'exécution, sans
      qu'aucune ligne de son propre code ne le nomme.
    ② CONTEXTE D'APPEL — Deux appelants.
      · `main`, quatre fois : le module de signal sous le nom `sig`, le module de
      positions sous `pos`, le module de jugement sous `jug` et le module de
      statistiques sous `sta`.
      · `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` ligne 153, qui charge le module
      de signal par cette fonction. Ce programme tourne chaque soir, lancé par
      `.github/workflows/collecte_abc.yml` ligne 136.
    ③ ENTRÉE — `chemin` : le chemin du fichier Python à charger · `nom` : le nom
      court sous lequel le module sera connu dans le processus. Exemple réel,
      mesuré le 20-09-2026 : chemin
      `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py` et nom `sig`.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit exister et être du code Python valide.
      `main` ne l'appelle que sur un chemin non vide pour le jugement et les
      statistiques, mais l'appelle sans condition pour le signal et les positions,
      dont l'absence a déjà été traitée plus tôt.
    ⑤ SORTIE — UNE valeur : le module chargé, dont on peut ensuite lire les
      fonctions et les constantes.
      [rend: 1]
    ⑥ TRAITEMENT — ① construire une description du module à partir du chemin et du
      nom · ② créer le module vide · ③ EXÉCUTER LE FICHIER, ce qui définit ses
      fonctions et lance tout ce qu'il contient hors fonction · ④ rendre le module.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge des stratégies ne comprend aucun indicateur, et c'est le cœur de sa
      conception : il ne sait pas ce qu'est un CMF ni un CCI. La fiche lui dit quel
      module produit les signaux, et il l'appelle. Une stratégie fondée sur des
      indicateurs qui n'existent pas encore fonctionnera donc sans qu'une ligne du
      juge des stratégies ne change. Cela suppose de charger un fichier par son chemin, ce que
      l'importation ordinaire de Python ne permet pas.
    ⑨ CE QUI CLOCHE —
      ① ELLE EXÉCUTE TOUT CE QUE LE FICHIER CONTIENT, sans aucun filtre. Un module
      qui écrirait un fichier ou appellerait le réseau au moment de son chargement
      le ferait ici, et le juge des stratégies, qui n'écrit rien par lui-même, écrirait par
      procuration. Rien dans la fonction ne le limite.
      ② ELLE ACCEPTE UN FICHIER COMPILÉ. Mesuré le 20-09-2026 : appelée sur
      `programmes/__pycache__/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.cpython-311.pyc`,
      elle rend un module dont `calculer_stabilite_parametrique` répond. Le module
      de statistiques avait pourtant été retiré du dossier `programmes/` de la
      copie. Un module effacé continue donc de tourner depuis son cache, et le
      rapport ne montre aucune différence.
      ③ Le nom court est choisi par l'appelant et n'a pas à être unique. Deux
      chargements sous le même nom se remplaceraient sans qu'un mot ne soit dit.
      Aucun appelant ne le fait aujourd'hui : `main` emploie quatre noms
      différents.
    ⑩ EFFET — LIT un fichier Python et EXÉCUTE SON CONTENU. Tout ce que ce fichier
      fait au chargement — écriture, affichage, accès réseau — est fait ici.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER une erreur non
      rattrapée si le fichier n'existe pas, s'il n'est pas du Python valide, ou si
      son exécution échoue ; ni `main` ni le détecteur de signaux ne la rattrapent
      dans le cas du module de signal, et le programme s'arrêterait alors.
      [sort: non]
    ⑫ DÉFINITIONS
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le CCI : un indicateur de bourse qui mesure de combien le prix s'écarte de
        sa moyenne des quatorze dernières séances.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le CMF : un indicateur de bourse qui mesure si l'argent entre ou sort
        d'une valeur sur les quatorze dernières séances.
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les
        signaux du jour
      le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les
        mesures disant si un gain veut dire quelque chose.
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le module de statistiques : le programme qui porte le voisinage des
        réglages et le pire creux,
        `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a
        lieu à l'ouverture de la séance suivante
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cle_valeur(nom):
    """Rapproche les graphies. Sans cela, 26 % d'une mesure se perd EN SILENCE
    (A-264, cas Bureau Veritas et Unibail).

    ① RÔLE — Donner à une même entreprise une seule écriture, quelle que soit la
      façon dont le fichier qui la nomme l'a écrite. Sans ce rapprochement, deux
      fichiers qui parlent de la même société semblent parler de deux sociétés
      différentes, et l'une des deux est ignorée sans qu'aucune erreur ne
      s'affiche.
    ② CONTEXTE D'APPEL — Quatre appelants dans le juge des stratégies, et deux au-dehors.
      · `charger_cours`, sur la colonne `valeur` de chaque ligne de cours lue.
      · `table_mnemoniques`, sur le nom usuel de chaque valeur du référentiel.
      · `jouer`, sur chaque valeur de l'univers demandé par la fiche.
      · `juger`, sur l'univers passé à l'étalon de hasard.
      · `programmes/DETECTER_LES_SIGNAUX_GITHUB.py`, lignes 203 et 281, qui tourne
      chaque soir.
      · `programmes/JUGER_SUR_8_CRITERES.py`, ligne 1193.
    ③ ENTRÉE — `nom` : le nom d'une valeur tel qu'un fichier l'a écrit, par
      exemple `Bureau Veritas`, `BUREAU-VERITAS` ou
      `UNIBAIL-RODAMCO-WESTFIELD`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un texte vide rend un texte vide.
    ⑤ SORTIE — UNE valeur : le nom mis en forme unique. Exemples réels, mesurés le
      20-09-2026 : `Bureau Veritas` devient `BUREAU_VERITAS`, et
      `UNIBAIL-RODAMCO-WESTFIELD` devient `UNIBAIL_RODAMCO`.
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les espaces de bord et passer en majuscules ·
      ② changer les tirets et les soulignés en espaces · ③ recoller les morceaux
      avec un souligné, ce qui écrase aussi les espaces multiples · ④ remplacer
      `UNIBAIL_RODAMCO_WESTFIELD` par `UNIBAIL_RODAMCO`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une même entreprise est écrite différemment selon le fichier :
      `UNIBAIL-RODAMCO-WESTFIELD` dans l'un, `UNIBAIL_RODAMCO` dans l'autre. Sans
      rapprochement, le programme croit qu'il s'agit de deux sociétés distinctes et
      ignore l'une des deux. Le 23-08-2026, cela a fait disparaître 26 % des lignes
      d'une mesure, sans aucune erreur affichée. L'incident est consigné au BACKLOG
      sous l'action A-264.
    ⑨ CE QUI CLOCHE —
      ① LE RAPPROCHEMENT ÉPELLE UN NOM AU LIEU DE PORTER SUR UNE PROPRIÉTÉ. Un
      seul couple est traité, celui d'Unibail, et il est écrit en clair dans le
      code. Toute autre société dont deux fichiers divergeraient autrement — un
      accent, un « SA » en fin de nom, une abréviation — repartirait en deux clés
      distinctes, et l'une des deux disparaîtrait en silence, exactement comme en
      août 2026. Le critère qui tranche tient en une question : si je renomme une
      valeur dans un fichier, mon contrôle change-t-il d'avis ? Ici oui.
      ② ELLE TRAVAILLE SUR LE NOM, ALORS QUE LA CLÉ DU PROJET EST LE MNÉMONIQUE.
      La règle d'identité des valeurs veut que le mnémonique fasse foi et jamais le
      nom. Cette fonction existe précisément pour rattraper des noms, et
      `table_mnemoniques` s'en sert pour traduire un mnémonique en nom rapproché :
      le nom reste donc la clé effective des séries de cours.
      ③ Le remplacement est écrit après le recollage, donc il ne fonctionne que sur
      la forme déjà normalisée. Un fichier qui écrirait `Unibail Rodamco Westfield`
      est bien rattrapé, mais rien ne le dit dans le code.
    ⑩ EFFET — Aucun : elle ne lit ni n'écrit aucun fichier, ne touche pas au
      réseau, et ne modifie pas le texte qu'on lui donne.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas sur un texte. Aucun de
      ses appels ne termine le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      l'étalon de hasard : le résultat qu'obtiendraient des entrées tirées au
        sort jouées aux mêmes règles, et auquel la stratégie doit être
        comparée
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et
        des actions du projet, où chaque ligne porte un identifiant en `A-`
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
"""
    n = "_".join(nom.strip().upper().replace("-", " ").replace("_", " ").split())
    return n.replace("UNIBAIL_RODAMCO_WESTFIELD", "UNIBAIL_RODAMCO")


def fichiers_de_cours(base):
    """Rend les fichiers de cours à charger — UN SEUL POINT DE DÉCISION.

    POURQUOI, Jean-Luc le 12-09-2026 : « je veux une solution professionnelle,
    simple et totalement fiable ». Dix-huit programmes nommaient `cac40_ohlcv.csv`
    et `claude_cours_nouveaux.csv` chacun de leur côté ; le fichier maître venait
    d'être construit et **personne ne le lisait**.
    LE JOUR OÙ LA SOURCE CHANGE ENCORE, ON MODIFIE CETTE FONCTION, PAS DIX-HUIT
    PROGRAMMES. C'est la règle de Jean-Luc : « ne jamais réécrire ce qui existe
    déjà — deux implémentations d'une même chose divergent toujours ».

    LE MAÎTRE S'IL EXISTE, LES DEUX ANCIENS SINON. Le repli n'est pas une
    politesse : il permet de brancher les programmes un par un, le circuit
    relancé entre chaque, sans qu'une faute dans le dixième casse les neuf
    premiers. Et il rend ce changement réversible d'un `git revert`.

    ① RÔLE — Dire, à un seul endroit pour tout le système, quels fichiers portent
      l'historique des cours. C'est la fonction la plus importante de ce programme
      pour le reste du circuit, et son nom ne figure pas dans celui du fichier :
      le BACKLOG le relève sous l'action A-426, ouverte le 19-09-2026, « rien dans
      le nom ne dit qu'il choisit les fichiers de cours et les charge ».
    ② CONTEXTE D'APPEL — Trois appelants, TOUS AU-DEHORS, et deux tournent chaque
      soir sans intervention humaine.
      · `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` ligne 162, lancé par
      `.github/workflows/collecte_abc.yml` ligne 136.
      · `programmes/TENIR_LES_POSITIONS.py` ligne 376, lancé ligne 171 du même
      fichier de circuit.
      · `programmes/JUGER_SUR_8_CRITERES.py` ligne 1180, lancé à la main.
      AUCUN APPELANT DANS CE PROGRAMME : relevé le 20-09-2026 en cherchant le nom
      dans l'arbre syntaxique du fichier, zéro appel interne.
    ③ ENTRÉE — `base` : le dossier racine du dépôt. Exemple réel, mesuré le
      20-09-2026 : la racine du clone, d'où la fonction rend
      `donnees/cours_maitre.csv`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une racine qui n'existe pas rend le couple des
      deux anciens chemins, sans lever.
    ⑤ SORTIE — **UNE valeur : un tuple d'UN chemin, `donnees/cours_maitre.csv`.**
      Quand ce fichier manque, ou qu'il est vide — l'en-tête seule, depuis le 24-09-2026 (A-471) —, elle ne rend rien : elle lève (voir ⑪). Jusqu'au
      24-09-2026, elle rendait alors les deux anciens fichiers de cours ; ce repli
      est retiré par décision de Jean-Luc (A-442).
      [rend: 1]
    ⑥ TRAITEMENT — ① composer le chemin du fichier maître · ② s'il existe, le
      rendre seul · ③ sinon, ou s'il ne porte aucune ligne après l'en-tête, lever une erreur qui nomme le fichier attendu.
    ⑦ UNITÉ — Un NOMBRE DE CHEMINS : un ou deux.
    ⑧ POURQUOI — Deux implémentations d'une même chose divergent toujours (R-708).
      Dix-huit programmes nommaient les deux anciens fichiers chacun de leur côté,
      et le fichier maître existait pendant que personne ne le lisait : la décision
      de ne garder qu'un seul point de décision date du 12-09-2026.
    ⑨ CE QUI CLOCHE —
      ① **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** SON PROPRE PROGRAMME NE L'APPELLE PAS. `main` va chercher
      `donnees/cac40_ohlcv.csv` et `donnees/claude_cours_nouveaux.csv` par leur nom,
      à travers `trouver`, au lieu de demander à cette fonction. Mesuré le
      20-09-2026 : le rapport affiche « cours cac40_ohlcv.csv » et « cours du jour
      claude_cours_nouveaux.csv », tandis que la fonction rend
      `donnees/cours_maitre.csv`. Le périmètre chargé est le même aujourd'hui —
      40 valeurs et 694 dates, du 2024-01-02 au 2026-09-18 des deux côtés — parce
      que l'historique figé s'arrête au 2026-07-10 et que le fichier du jour
      reprend au 2026-07-13, sans un seul jour de recouvrement. Le jour où le
      fichier du jour portera moins de séances que le trou ouvert depuis le
      2026-07-10, le juge des stratégies jugera sur un historique amputé pendant que les
      programmes du soir liront le maître complet, et rien ne le dira.
      ② **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** LE REPLI EST SILENCIEUX. Quand le maître manque, la fonction rend les deux
      anciens chemins sans afficher un mot, et ses appelants ne vérifient que
      l'existence des fichiers rendus. Un système qui a perdu son fichier maître
      continuerait donc de tourner sur une autre source sans que rien ne le
      signale.
      ③ **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** Elle ne vérifie pas que les fichiers qu'elle nomme existent : seul le
      maître est testé. Les deux anciens chemins sont rendus qu'ils existent ou
      non, et c'est à l'appelant de le voir.
    ⑩ EFFET — LIT l'existence d'un fichier sur le disque. N'ouvre rien, n'écrit
      rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main quand le fichier maître existe. **Sinon, elle LÈVE
      `FileNotFoundError`, avec un message qui nomme le fichier attendu** : c'est
      voulu, décision de Jean-Luc du 20-09-2026 (A-442) — *« Si le maître n'est pas
      là, il y a un message d'alerte de toute urgence. »* L'appelant qui ne la
      rattrape pas s'arrête avec un code non nul, et le circuit du soir rougit.
      [sort: non]
    ⑫ DÉFINITIONS
      l'arbre syntaxique : la représentation d'un fichier Python que le
        langage construit avant de l'exécuter, et qui donne accès aux
        fonctions, aux appels et aux nombres écrits, sans jamais lancer le
        programme.
      l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de
        référence qui n'est jamais réécrit
      la racine : le dossier reçu sur la ligne de commande, celui dont on
        classe les fichiers — en général un clone du dépôt.
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et
        des actions du projet, où chaque ligne porte un identifiant en `A-`
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
        n'en étant qu'une copie de lecture
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les
        signaux du jour
      le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
        l'historique des cours et n'est jamais réécrit.
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    maitre = os.path.join(base, "donnees", "cours_maitre.csv")
    if os.path.isfile(maitre):
        # UN MAITRE VIDE — l en-tete seule — VAUT UN MAITRE ABSENT (A-471, 24-09-2026) :
        # releve par Cowork, lance seul, le juge des stratégies jugeait sur « 0 valeurs » et rendait 0.
        with open(maitre, encoding="utf-8-sig") as _f:
            _f.readline()
            _vide = not _f.readline().strip()
        if not _vide:
            return (maitre,)
    # PLUS DE REPLI — decision de Jean-Luc du 20-09-2026 (A-442) : « Si le maitre
    # n'est pas la, il y a un message d'alerte de toute urgence. »
    raise FileNotFoundError(
        "ARRET : le fichier maitre des cours est absent ou vide : %s. Aucun repli sur les "
        "anciens fichiers de cours (decision de Jean-Luc du 20-09-2026, A-442)." % maitre)


def charger_cours(*chemins):
    """Lit un ou plusieurs fichiers de cours et rend une série par valeur.

    ① RÔLE — Transformer des fichiers de cours en séries utilisables : une liste de
      séances par valeur, triée par date, sans doublon, quel que soit le nombre de
      fichiers d'où elles viennent. Tout le reste du juge des stratégies part de là.
    ② CONTEXTE D'APPEL — Quatre appelants, dont deux au-dehors.
      · `main`, une fois, sur les cours et les cours du jour ensemble.
      · `main` encore, sur le témoin du golden seul, quand ce témoin est conforme.
      · `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` ligne 167 et
      `programmes/TENIR_LES_POSITIONS.py` ligne 463, qui tournent chaque soir.
      · `programmes/JUGER_SUR_8_CRITERES.py` ligne 1180.
    ③ ENTRÉE — `chemins` : un ou plusieurs chemins de fichiers de cours, donnés
      les uns après les autres. Un chemin vide ou `None` est sauté. Exemple réel,
      mesuré le 20-09-2026 : `main` passe `donnees/cac40_ohlcv.csv` puis
      `donnees/claude_cours_nouveaux.csv`.
    ④ CONDITIONS D'ENTRÉE — Chaque fichier doit exister et porter au moins les
      colonnes `valeur`, `date`, `open`, `high`, `low`, `close` et `volume`. Les
      fichiers sont lus dans l'ordre donné, et le DERNIER lu l'emporte pour une
      date déjà vue.
    ⑤ SORTIE — UNE valeur : un dictionnaire qui va du nom rapproché d'une valeur à
      la liste de ses séances, triée par date. Mesuré le 20-09-2026 sur les deux
      fichiers du dépôt : 40 valeurs, 26 690 séances au total, du 2024-01-02 au
      2026-09-18.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque chemin non vide, ouvrir le fichier en texte et le
      lire ligne à ligne · ② rapprocher le nom de la valeur, puis ranger la séance
      sous sa date, ce qui écrase une date déjà lue · ③ SAUTER SANS RIEN DIRE toute
      ligne dont une colonne manque ou dont un nombre est illisible · ④ pour chaque
      valeur, rendre ses séances triées par date.
    ⑦ UNITÉ — Les prix sont des EUROS par titre, le volume un NOMBRE DE TITRES
      échangés, la date une chaîne au format AAAA-MM-JJ.
    ⑧ POURQUOI — Le tri se fait sur la date écrite en AAAA-MM-JJ, sans convertir en
      date véritable : dans cette écriture, l'ordre des textes est déjà l'ordre du
      calendrier, et une conversion de 26 690 lignes serait du travail pour rien.
      Le dernier fichier lu l'emporte parce que le fichier du jour porte la version
      la plus récente d'une séance, l'historique figé la plus ancienne.
    ⑨ CE QUI CLOCHE —
      ① LES LIGNES ILLISIBLES DISPARAISSENT SANS ÊTRE COMPTÉES. Mesuré le
      20-09-2026 sur un fichier d'épreuve de trois lignes dont une porte
      `BANANE` en clôture : la fonction rend deux séances, sans un mot. Sur un
      fichier de cours réel, une colonne abîmée sur mille retirerait mille séances
      et le rapport n'en dirait rien.
      ② UNE COLONNE RENOMMÉE VIDE TOUT, EN SILENCE. Mesuré le 20-09-2026 sur un
      fichier dont la colonne `valeur` a été renommée `nom` : la fonction rend un
      dictionnaire VIDE, sans erreur. Le juge des stratégies afficherait alors « DONNEES :
      0 valeurs » et continuerait son chemin.
      ③ Elle ne dit pas quel fichier a fourni quelle séance. Le fichier maître
      porte une huitième colonne qui nomme la source de chaque ligne ; cette
      fonction ne la lit pas et ne la garde pas. Une séance venue de Google et une
      séance venue d'ABC deviennent indiscernables, alors que leurs volumes
      diffèrent.
      ④ Aucun contrôle de cohérence : une séance dont le plus haut serait inférieur
      au plus bas, ou dont le volume serait nul, est chargée telle quelle.
    ⑩ EFFET — LIT chaque fichier donné, en entier. N'écrit rien, ne touche pas au
      réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER une erreur non
      rattrapée si un chemin non vide désigne un fichier absent ou illisible ;
      aucun de ses appelants ne la rattrape.
      [sort: non]
    ⑫ DÉFINITIONS
      l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de
        référence qui n'est jamais réécrit
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
        l'historique des cours et n'est jamais réécrit.
      le témoin du golden : la copie conservée des cours qui ont produit
        les chiffres figés,
        `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    brut = defaultdict(dict)
    for ch in chemins:
        if not ch:
            continue
        with open(ch, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                try:
                    brut[cle_valeur(r["valeur"])][r["date"]] = {
                        "date": r["date"], "open": float(r["open"]),
                        "high": float(r["high"]), "low": float(r["low"]),
                        "close": float(r["close"]), "volume": float(r["volume"])}
                except (KeyError, ValueError):
                    continue
    return {v: [d[k] for k in sorted(d)] for v, d in brut.items()}


def table_mnemoniques(chemin):
    """mnemonique -> cle de valeur. La cle est le MNEMONIQUE, jamais le nom
    (chapitre IDENTITE DES VALEURS, regle I-1).

    ① RÔLE — Traduire les codes courts employés par les fiches de stratégies en
      noms rapprochés, qui sont les clés des séries de cours. Une fiche écrit son
      univers en codes courts, `TTE,ENGI,VIE` ; les cours sont rangés sous
      `TOTALENERGIES`, `ENGIE`, `VEOLIA`. Sans cette table, aucune valeur demandée
      ne serait retrouvée.
    ② CONTEXTE D'APPEL — `main`, une seule fois, juste après le chargement des
      cours. Jamais appelée ailleurs : recherche du nom dans les 34 fichiers de
      `programmes/` le 20-09-2026, un seul appel.
    ③ ENTRÉE — `chemin` : le chemin du référentiel des valeurs, ou `None`. Un seul
      appelant, `main`, qui passe le résultat de `trouver` sur le motif
      `REFERENTIEL_VALEURS`, soit
      `donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv` mesuré le
      20-09-2026.
    ④ CONDITIONS D'ENTRÉE — Le fichier, s'il est donné, doit exister et porter les
      colonnes `mnemonique` et `nom_usuel`. Un chemin `None` est une situation prévue.
    ⑤ SORTIE — UNE valeur : un dictionnaire qui va du code court en majuscules au
      nom rapproché. Il est VIDE si aucun chemin n'est donné. Mesuré le 20-09-2026
      sur le référentiel du dépôt : 40 mnémoniques.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre une table vide si aucun chemin n'est donné · ② ouvrir
      le fichier et le lire ligne à ligne · ③ ne garder que les lignes où le code
      court ET le nom usuel sont renseignés · ④ ranger le nom rapproché sous le
      code court mis en majuscules.
    ⑦ UNITÉ — Un NOMBRE DE VALEURS DE BOURSE.
    ⑧ POURQUOI — La clé est le mnémonique, jamais le nom. Un nom s'écrit de
      plusieurs façons selon la source et se traduit ; un code court ne change pas.
      C'est la règle d'identité des valeurs du projet, et elle existe parce qu'une
      valeur attendue qui ne renvoie rien doit être une alerte et non un silence.
    ⑨ CE QUI CLOCHE —
      ① ELLE IGNORE UNE COLONNE QUE SES VOISINS LISENT. `programmes/JUGER_SUR_8_CRITERES.py`
      ligne 1191 construit la même table en prenant `onglet_google` d'abord et
      `nom_usuel` seulement en repli, quand cette fonction ne lit que `nom_usuel`.
      Deux programmes construisent donc la même table par deux chemins différents,
      et rien ne garantit qu'ils rendent la même chose. Deux implémentations d'une
      même chose divergent toujours (R-708).
      ② UN RÉFÉRENTIEL ABSENT REND UNE TABLE VIDE, SANS ALERTE. `main` affiche
      alors « 0 mnemoniques » au milieu d'une ligne de bilan, et chaque valeur
      demandée par une fiche est cherchée sous son code court brut. Le code court
      n'étant pas le nom rapproché, toutes les valeurs deviennent inconnues, et le
      juge des stratégies se contente d'une ligne « ALERTE - valeurs demandees et absentes des
      cours ».
      ③ Une ligne dont le code court est renseigné mais le nom vide est sautée sans
      être comptée : le référentiel peut perdre des valeurs en silence.
    ⑩ EFFET — LIT le référentiel des valeurs en entier. N'écrit rien, ne touche pas
      au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER une erreur non
      rattrapée si le chemin donné désigne un fichier absent ou illisible ; `main`
      ne la rattrape pas.
      [sort: non]
    ⑫ DÉFINITIONS
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste
        des valeurs à suivre, avec pour chacune son mnémonique et sa place
        de cotation.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    t = {}
    if not chemin:
        return t
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            m = (r.get("mnemonique") or "").strip()
            n = (r.get("nom_usuel") or "").strip()
            if m and n:
                t[m.upper()] = cle_valeur(n)
    return t


def pourcent(txt, defaut=None):
    """Lit un pourcentage écrit à la main et le rend en fraction.

    ① RÔLE — Accepter les pourcentages tels qu'un humain les écrit dans le registre
      des stratégies — `+4.0%`, `-2,5 %`, `4` — et les rendre sous la seule forme
      que les calculs emploient, la fraction. Sans elle, chaque endroit qui lit un
      seuil devrait refaire ce nettoyage à sa façon.
    ② CONTEXTE D'APPEL — Trois appelants, tous dans ce programme.
      ① `porte_0`, pour vérifier que l'objectif de gain et la perte acceptée d'une
      fiche sont lisibles.
      ② `jouer`, pour obtenir les deux seuils avant de rejouer la stratégie.
      ③ `juger`, pour les mêmes deux seuils avant de calculer le point mort.
    ③ ENTRÉE — `txt` : le texte à lire, venu d'une colonne du registre des
      stratégies · `defaut` : ce qui est rendu quand le texte est vide ou
      illisible, `None` si l'appelant n'en donne pas. Les trois appelants ne
      passent que `txt`.
    ④ CONDITIONS D'ENTRÉE — Aucune. `None`, un texte vide ou un texte quelconque
      sont trois cas prévus.
    ⑤ SORTIE — UNE valeur : une fraction positive, ou la valeur de repli. Exemples
      réels, mesurés le 20-09-2026 : `+4.0%` rend 0,04 · `-2.5%` rend 0,025 ·
      `12` rend 0,12 · `abc` rend `None`.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre la valeur de repli si le texte est `None` · ② remplacer
      la virgule par un point, retirer le signe pourcent et les espaces · ③ rendre
      la valeur de repli si plus rien ne reste · ④ lire le nombre et en prendre la
      VALEUR ABSOLUE, ou rendre la valeur de repli s'il est illisible · ⑤ diviser
      par cent si le nombre vaut au moins 1, le garder tel quel sinon.
    ⑦ UNITÉ — Une FRACTION du prix d'entrée : 0,040 vaut 4 %.
    ⑧ POURQUOI — La valeur absolue est prise parce que la perte acceptée s'écrit
      avec un signe moins dans le registre, `-2.5%`, alors que les calculs la
      veulent positive : le prix de sortie se construit en RETRANCHANT cette
      fraction, et un signe conservé la rajouterait.
    ⑨ CE QUI CLOCHE —
      ① UN SEUIL AU-DESSOUS DE 1 % EST LU CENT FOIS TROP GRAND. La règle « diviser
      par cent si le nombre vaut au moins 1 » sert à accepter `4` pour 4 %, mais
      elle rend 0,8 pour `0.8%`. Mesuré le 20-09-2026 : `pourcent("0.8%")` rend
      0,8 — soit 80 % — là où 0,008 était écrit ; `pourcent("1%")` rend bien 0,01.
      La bascule se fait donc exactement à 1 %. Une stratégie à objectif serré, un
      écart de moins d'un pour cent, serait jouée avec un objectif cent fois plus
      lointain, et aucune alerte ne s'afficherait : le rapport annoncerait
      simplement que presque toutes les opérations sortent à l'horizon.
      ② LE SIGNE EST PERDU, DONC UN SEUIL MAL SIGNÉ NE SE VOIT PAS. Une fiche qui
      écrirait `+2.5%` en perte acceptée serait acceptée telle quelle, et une qui
      écrirait `-4.0%` en objectif de gain aussi. Rien ne vérifie que l'objectif est
      positif et la perte négative dans le fichier.
      ③ Le texte illisible et le texte vide rendent la même chose. `porte_0` s'en
      sort en testant séparément le vide, mais un appelant qui ne le ferait pas ne
      pourrait pas distinguer « champ non rempli » de « champ mal rempli ».
    ⑩ EFFET — Aucun : elle ne lit ni n'écrit aucun fichier, ne touche pas au
      réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec de lecture du
      nombre est rattrapé et rendu sous forme de valeur de repli. Aucun de ses
      appels ne termine le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      l'horizon : le nombre de séances pendant lesquelles une position est
        tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le SL : la perte acceptée qui ferme la position, une fraction du prix
        d'entrée — 0,025 vaut −2,5 %.
      le TP : l'objectif de gain qui ferme la position, une fraction du prix
        d'entrée — 0,040 vaut +4 %.
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    if txt is None:
        return defaut
    s = str(txt).strip().replace(",", ".").replace("%", "").replace(" ", "")
    if not s:
        return defaut
    try:
        v = abs(float(s))
    except ValueError:
        return defaut
    return v / 100 if v >= 1 else v


def porte_0(fiche):
    """Refuse une fiche incomplete AVANT tout calcul. Ne consomme aucun essai.

    ① RÔLE — Écarter une fiche dont les champs indispensables manquent ou sont
      illisibles, avant qu'un seul calcul ne soit lancé, et rendre à l'appelant les
      bornes de période qu'elle vient de valider. Refuser une fiche n'est pas
      rejeter l'idée : c'est mettre sa fiche en attente, et le compteur d'essais de
      la stratégie n'est pas entamé.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce programme.
      · `main`, une fois par fiche du registre restée après le tri des états de
      vie — 37 appels mesurés le 20-09-2026.
      · `calibrer`, une fois, sur la fiche de calibrage qu'il construit lui-même,
      pour que cette fiche passe la même porte que les autres.
    ③ ENTRÉE — `fiche` : un dictionnaire de champs, soit une ligne du registre des
      stratégies lue telle quelle, soit la fiche construite par `calibrer`. Les
      champs regardés sont `periode`, `indicateurs`, `univers`, `tp`, `sl` et
      `horizon`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un champ absent est traité comme un champ vide.
    ⑤ SORTIE — **DEUX valeurs (2) dans un cas, TROIS valeurs (3) dans l'autre — elle a DEUX
      FORMES, et c'est un défaut.** DANS LE CAS ORDINAIRE, elle
      rend TROIS valeurs : un oui-ou-non, la liste des manques, et le couple des
      bornes de période quand la fiche passe, `None` sinon. QUAND LA PÉRIODE EST
      MAL FORMÉE, elle rend DEUX valeurs seulement : un non et la liste d'un seul
      message.
      [rend: 2 ou 3]
    ⑥ TRAITEMENT — ① si une période est écrite, vérifier qu'elle a la forme
      `AAAA-MM-JJ -> AAAA-MM-JJ`, que ses deux dates existent au calendrier, et que
      le début précède la fin · ② relever les champs obligatoires vides · ③ vérifier
      que l'objectif de gain et la perte acceptée sont des nombres lisibles ·
      ④ vérifier que l'horizon est un entier · ⑤ rendre le verdict, la liste des
      manques, et les bornes validées.
    ⑦ UNITÉ — Les bornes rendues sont deux DATES au format AAAA-MM-JJ. Les manques
      se comptent en NOMBRE DE CHAMPS.
    ⑧ POURQUOI — La période est un champ obligatoire depuis le 29-08-2026, au même
      titre que les cinq autres, parce que la frontière qui sépare la partie
      apprise de la partie jamais vue se calcule sur le calendrier de cette période.
      Sans période déclarée, le juge des stratégies prenait tout l'historique disponible, donc un
      périmètre qui bouge à chaque séance ajoutée : les chiffres changeaient sans
      que la stratégie change, et aucune comparaison dans le temps n'était possible.
      Déclarer une période a fait passer les deux stratégies suivies de « cas
      défavorable perdant » à « au-dessus du point mort », sans qu'une ligne de leur
      stratégie ne bouge.
      ET ELLE REFUSE AU LIEU D'ALERTER : une alerte après calcul se tolère, et
      l'on finit par la lire comme du bruit. Refuser avant calcul ne se tolère pas,
      et la dette se résorbe fiche par fiche, au moment où chacune devient utile.
      LA PORTE REND LES BORNES AU LIEU DE LES ÉCRIRE DANS LA FICHE : une fonction
      qui s'appelle « porte » et qui modifie ce qu'elle contrôle surprend qui la
      lit, et une fiche refusée garderait les bornes d'un appel précédent si on la
      repassait.
    ⑨ CE QUI CLOCHE —
      ① ELLE REND DEUX VALEURS DANS UNE SITUATION ET TROIS DANS TOUTES LES
      AUTRES, ET SES DEUX APPELANTS EN ATTENDENT TROIS. Les trois retours du bloc de période —
      période illisible, date inexistante, période inversée — ne rendent qu'un
      couple. Mesuré le 20-09-2026 : `porte_0` appelée sur une fiche dont la période
      vaut « banane » rend 2 valeurs, et le dépaquetage en trois lève
      « ValueError: not enough values to unpack (expected 3, got 2) ». Mesuré de
      bout en bout le même jour, en ajoutant au registre d'une copie une fiche
      `ZZ-TEST` de période « du 2 janvier au 10 juillet » : le juge des stratégies affiche les
      36 premières fiches puis s'arrête, ligne 831, code de sortie 1. Aucune des
      trois fiches recevables n'a été jugée. La porte existe pour refuser une fiche
      SANS arrêter le travail, et elle arrête le travail.
      ② LE CONTRÔLE DE PÉRIODE EST FAIT AVANT LE CONTRÔLE DE PRÉSENCE, DONC IL
      PASSE AVANT LE VERDICT D'ENSEMBLE. Une fiche vide de partout mais dont la
      période serait mal écrite est refusée pour cette seule raison, et les cinq
      autres manques ne sont jamais affichés. Jean-Luc corrigerait un champ et
      découvrirait les cinq autres au passage suivant.
      ③ LA VALEUR `—` EST REFUSÉE, MAIS PAS `à renseigner` ÉCRIT AUTREMENT. La
      liste des textes tenus pour vides porte le tiret, le tiret cadratin et deux
      écritures de « à renseigner ». Mesuré le 20-09-2026 sur le registre réel :
      six fiches sont refusées pour `indicateurs, univers, tp, sl, horizon,
      periode`, ce qui montre que la liste fonctionne ; mais le critère épelle des
      textes au lieu de porter sur une propriété, et une septième écriture
      passerait.
      ④ ELLE NE VÉRIFIE PAS QUE L'HORIZON EST POSITIF. Un horizon de `0` ou de `-5`
      est un entier lisible et passe la porte ; `jouer` prendrait alors une tranche
      de séances vide et ne produirait aucune opération, sans dire pourquoi.
      ⑤ ELLE NE VÉRIFIE PAS QUE L'UNIVERS DÉSIGNE DES VALEURS CONNUES. Le champ est
      seulement testé non vide. Mesuré le 20-09-2026, une fiche du registre porte
      « A TRANCHER — voir etude_ref » en univers : ce texte n'est pas vide, il
      passerait ce contrôle-là.
    ⑩ EFFET — Aucun : elle ne modifie PAS la fiche reçue, ne lit ni n'écrit aucun
      fichier, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas elle-même, mais le
      nombre de valeurs qu'elle rend fait lever ses deux appelants sur une période
      mal formée, ce qui arrête le programme avec le code 1. Aucun de ses appels ne
      termine le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      l'horizon : le nombre de séances pendant lesquelles une position est
        tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      la partie jamais vue : la fin de la période, celle sur laquelle la
        stratégie n'a pas été réglée, et donc la seule qui prouve quelque
        chose
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige
        de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le SL : la perte acceptée qui ferme la position, une fraction du prix
        d'entrée — 0,025 vaut −2,5 %.
      le TP : l'objectif de gain qui ferme la position, une fraction du prix
        d'entrée — 0,040 vaut +4 %.
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
    """
    # une periode presente mais mal formee ne vaut pas mieux qu'absente
    # LE FORMAT SE VERIFIE VRAIMENT, ET LE MESSAGE MONTRE CE QU'IL A LU.
    # Premiere version : on cherchait « -> » et rien d'autre. « banane -> 12 »
    # passait la porte, puis la comparaison de dates s'appliquait a du texte
    # quelconque — silencieusement, puisqu'on compare des CHAINES. Et une
    # periode INVERSEE rendait zero operation sans dire pourquoi.
    _p = (fiche.get("periode") or "").strip()
    if _p:
        _m = re.match(r"^(\d{4}-\d{2}-\d{2})\s*->\s*(\d{4}-\d{2}-\d{2})$", _p)
        if not _m:
            return False, ["periode illisible : lu %r, attendu "
                           "« AAAA-MM-JJ -> AAAA-MM-JJ »" % _p]
        # LA FORME NE SUFFIT PAS : LA DATE DOIT EXISTER. « 2024-13-45 » a la
        # bonne forme et n'est pas une date. La comparaison de CHAINES ne
        # broncherait pas : elle rendrait zero operation ou un perimetre
        # absurde, EN SILENCE — le defaut de l'inversion, un cran plus loin.
        from datetime import datetime as _dtv
        for _d in (_m.group(1), _m.group(2)):
            try:
                _dtv.strptime(_d, "%Y-%m-%d")
            except ValueError:
                return False, ["periode impossible : %r n'existe pas dans le "
                               "calendrier (lu %r)" % (_d, _p)]
        if _m.group(1) > _m.group(2):
            return False, ["periode INVERSEE : lu %r — le debut est apres la "
                           "fin, aucune operation ne serait trouvee" % _p]
    manq = [c for c in CHAMPS_OBLIGATOIRES
            if (fiche.get(c) or "").strip().lower() in VIDE]
    for c in ("tp", "sl"):
        if c not in manq and pourcent(fiche.get(c)) is None:
            manq.append(c + " illisible")
    # L'HORIZON SE LIT PAR LA MEME FONCTION QUE LE PROGRAMME DU SOIR (defaut 4 de
    # A-491, 28-09-2026) : l'ancienne lecture refusait « 20j » et acceptait « 0 ».
    if "horizon" not in manq and lire_horizon(fiche.get("horizon")) is None:
        manq.append("horizon illisible")
    # LA PORTE REND LES BORNES QU'ELLE VIENT DE VALIDER. Sans cela, main()
    # redecoupait le champ a la main alors que la porte venait de le lire
    # proprement — DEUX lectures du meme champ, sous deux formes. A-308 en germe.
    # ELLE LES RETOURNE, ELLE N'ECRIT PAS DANS LA FICHE.
    # Premiere version : la porte rangeait les bornes dans le dictionnaire
    # recu. Ca marchait, mais une fonction qui s'appelle « porte » et qui ECRIT
    # dans ce qu'elle controle surprend qui la lit — et une fiche refusee
    # gardait les bornes d'un appel precedent si on la repassait.
    _b = (_m.group(1), _m.group(2)) if (not manq and _p) else None
    return (not manq), manq, _b


def jouer(fiche, cours, mnemo, mod_signal, mod_positions, periode=None):
    """Comptabilite JETONS ILLIMITES : TOUS les signaux joues. La selection d'un
    signal par jour ne concerne QUE la comptabilite UN JETON, ou il faut bien
    choisir puisqu'on ne detient qu'une position (A-79, 01-08-2026).

    ① RÔLE — Rejouer une stratégie sur l'historique et rendre la liste des
      opérations qu'elle aurait faites, chacune avec son gain net en euros, frais
      payés. C'est le cœur du juge des stratégies : tout ce qui suit — résumé, jugement, étalon de
      hasard — part de cette liste.
    ② CONTEXTE D'APPEL — Quatre appelants, dont un au-dehors.
      · `main`, une fois par fiche recevable.
      · `calibrer`, une fois, sur la fiche de calibrage.
      · `_rejouer`, à l'intérieur de `juger`, une fois par variante de réglages
      quand le voisinage est mesuré.
      · `programmes/JUGER_SUR_8_CRITERES.py` ligne 1202.
    ③ ENTRÉE — `fiche` : la ligne de stratégie, où sont lus `tp`, `sl`, `horizon`,
      `univers` et `_fonction_signal` · `cours` : les séries par valeur, rendues par
      `charger_cours` · `mnemo` : la table qui traduit les codes courts en noms
      rapprochés · `mod_signal` : le module qui produit les signaux ·
      `mod_positions` : le module qui décide des sorties et des frais · `periode` :
      le couple des bornes rendu par la porte 0, ou `None` pour ne pas borner.
      `main` passe toujours les bornes de la fiche.
    ④ CONDITIONS D'ENTRÉE — La fiche doit avoir passé la porte 0 : l'objectif de
      gain, la perte acceptée et l'horizon doivent être lisibles, faute de quoi la
      fonction lève. Le module de signal doit exposer la fonction nommée par
      `_fonction_signal`, et le module de positions doit exposer `tester_seance` et
      `frais_ordre`.
    ⑤ SORTIE — DEUX valeurs : la liste des opérations, et la liste des valeurs
      demandées par la fiche mais absentes des cours. Chaque opération porte la
      valeur, la date du signal, le prix d'entrée, le prix de sortie, le motif de
      sortie, le gain net en euros et, depuis le 28-09-2026, la date de sortie.
      Mesuré le 20-09-2026 sur la fiche
      `C5E10-QA-V1` : 62 opérations, aucune valeur inconnue.
      [rend: 2]
    ⑥ TRAITEMENT — ① lire l'objectif de gain, la perte acceptée et l'horizon dans
      la fiche · ② traduire l'univers demandé, en séparant les valeurs connues des
      inconnues · ③ demander au module de signal les séances qui déclenchent un
      achat · ④ écarter un signal sur la dernière séance, faute de lendemain pour
      entrer · ⑤ écarter un signal hors de la période déclarée · ⑥ entrer à
      l'ouverture du lendemain et poser les deux prix de sortie · ⑦ parcourir les
      séances DEPUIS LA SÉANCE D'ACHAT COMPRISE (R-608, depuis le 28-09-2026), dans
      la limite de l'horizon, et sortir à la première qui touche un seuil · ⑧ sortir
      à la clôture de la h-ième séance APRÈS l'achat si aucun seuil n'a été touché · ⑨ demander au module de positions les frais des DEUX ordres
      et retrancher · ⑩ ranger l'opération.
    ⑦ UNITÉ — Les seuils sont des FRACTIONS du prix d'entrée. L'horizon se compte
      en SÉANCES de bourse. La quantité est un NOMBRE DE TITRES, fractionnaire. Les
      prix et les gains sont des EUROS, pour 100 000 € engagés par opération.
    ⑧ POURQUOI — LES SEUILS VIENNENT DE LA FICHE, JAMAIS DU CODE. L'objectif de
      gain, la perte acceptée et l'horizon sont lus dans `fiche["tp"]`,
      `fiche["sl"]` et `fiche["horizon"]`, c'est-à-dire dans la ligne du registre
      des stratégies `donnees/cac40_strategies.csv`. Mesuré le 20-09-2026 : la ligne
      `C5E10-QA-V1` y porte `+4.0%`, `-2.5%` et `20`, et le rapport affiche
      « TP +4.0% . SL -2.5% . horizon 20 seances ». Les mêmes trois chiffres sont
      écrits au REGISTRE sous la règle R-201, qui décrit la stratégie
      C5-ETENDU-10 : « TP +4 % · SL −2,5 % · 20 séances ».
      LES SORTIES VIENNENT DU MODULE DE POSITIONS, JAMAIS D'AILLEURS. Deux
      mécaniques de sortie coexistaient, découvertes le 25-08-2026 : le module de
      signal sortait au prix théorique, le module de positions au prix réellement
      disponible. Mesure du 26-08-2026 : 19 opérations sur 100 sortent sur un saut,
      et l'écart atteint +12 501 €, soit 11,2 % de l'étalon. Le module de positions
      fait foi, puisque c'est lui qui pilote les positions.
      LES FRAIS NE S'ÉCRIVENT PAS EN DUR. Leur propriétaire est le module de
      positions : 0,15 % de la valeur échangée à l'entrée ET à la sortie, soit
      307,50 € sur une sortie à +5 %, et non 300 € fixes. Un nombre recopié qui
      contredit son module est exactement ce que R-708 interdit ; quand le module
      n'expose pas la fonction de frais, cette fonction lève plutôt que de recopier
      un taux.
      TOUS LES SIGNAUX SONT JOUÉS : c'est la comptabilité « jetons illimités ».
      Choisir un signal par jour ne concerne que la comptabilité « un jeton », où
      il faut bien trancher puisqu'on ne détient qu'une position à la fois.
    ⑨ CE QUI CLOCHE —
      ① LE NOM DE FONCTION DE SIGNAL PAR DÉFAUT NE CORRESPOND À AUCUN MODULE. La
      fiche peut ne pas porter `_fonction_signal`, et le repli écrit ici est
      `signaux`. Mesuré le 20-09-2026 en appelant `jouer` sur une fiche du registre
      sans poser ce champ : « RuntimeError: le module de signal n'expose pas
      'signaux' ». Le seul module de signal du dépôt expose
      `signaux_c5etendu10`. Le vrai repli est écrit deux fois ailleurs, dans `main`
      et dans `calibrer`, et une troisième fois dans
      `programmes/JUGER_SUR_8_CRITERES.py` : quatre endroits décident du même nom,
      et celui qui est écrit ici est faux.
      ② UN SIGNAL SANS LENDEMAIN DISPARAÎT SANS ÊTRE COMPTÉ. Le signal de la
      dernière séance disponible est sauté, puisqu'il n'y a pas d'ouverture du
      lendemain pour entrer. C'est juste, mais rien ne le dit au rapport : un
      signal du jour, le seul qui intéresse une décision, est invisible.
      ③ LA QUANTITÉ DE TITRES EST FRACTIONNAIRE. Elle vaut 100 000 € divisés par le
      prix d'entrée, sans arrondi : à 47,31 € le titre, cela fait 2 113,72 titres.
      Aucun marché n'échange 0,72 titre, et le gain net s'en trouve légèrement
      surévalué. Le module de positions applique le même calcul, donc les deux sont
      d'accord, mais le chiffre reste une simulation d'un ordre impossible.
      ④ LES VALEURS INCONNUES SONT RENDUES, PAS COMPTÉES. La liste des inconnues
      remonte à l'appelant, qui l'affiche ; mais le rapport ne dit pas combien de
      valeurs de l'univers ont réellement été jouées. Une fiche dont neuf valeurs
      sur dix seraient introuvables produirait un résultat sur une seule valeur,
      avec une ligne d'alerte de même taille que pour une seule absente.
    ⑩ EFFET — Aucun sur le disque : ni lecture ni écriture de fichier, aucun accès
      réseau. Elle APPELLE le module de signal et le module de positions, donc tout
      ce que ces modules font, elle le fait. Elle ne modifie pas les cours reçus.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER deux erreurs non
      rattrapées : quand le module de signal n'expose pas la fonction demandée, et
      quand le module de positions n'expose pas la fonction de frais. Aucun de ses
      appelants ne les rattrape, sauf `_rejouer`, dont l'appel est enveloppé par le
      enveloppe de secours du voisinage dans `juger`. Et un de ses appels peut ne pas
      revenir : la fonction de signal du module chargé est du code tiers, et rien
      ne borne son temps d'exécution.
      [sort: non]
    ⑫ DÉFINITIONS
      jetons illimités : la seconde comptabilité, où toute position s'ouvre
        sans limite ; elle ne correspond à aucun portefeuille réel.
      l'horizon : le nombre de séances pendant lesquelles une position est
        tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a
        lieu à l'ouverture de la séance suivante
      le SL : la perte acceptée qui ferme la position, une fraction du prix
        d'entrée — 0,025 vaut −2,5 %.
      le TP : l'objectif de gain qui ferme la position, une fraction du prix
        d'entrée — 0,040 vaut +4 %.
      un jeton : la comptabilité où une seule position peut être ouverte à la
        fois par stratégie ; un signal reçu pendant une position est ignoré.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte
        que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
"""
    tp = pourcent(fiche["tp"])
    sl = pourcent(fiche["sl"])
    h = lire_horizon(fiche["horizon"])

    demandes = [x.strip().upper() for x in fiche["univers"].split(",") if x.strip()]
    univers, inconnus = [], []
    for m in demandes:
        v = mnemo.get(m, cle_valeur(m))
        if v in cours:
            univers.append(v)
        else:
            inconnus.append(m)

    nom_fn = fiche.get("_fonction_signal", "signaux")
    fn = getattr(mod_signal, nom_fn, None)
    if fn is None:
        raise RuntimeError("le module de signal n'expose pas " + repr(nom_fn))

    ops = []
    for v in univers:
        s = cours[v]
        for sg in fn(s):
            i = sg["i"]
            if i + 1 >= len(s):
                continue
            d_sig = s[i]["date"]
            if periode and not (periode[0] <= d_sig <= periode[1]):
                continue
            pe = s[i + 1]["open"]
            tp_abs, sl_abs = pe * (1 + tp), pe * (1 - sl)
            # LA SEANCE D'ACHAT COMPTE (R-608, decision de Jean-Luc du 27-09-2026 a
            # 19h40 ; defaut 4 de A-491). Les seuils se testent des s[i + 1], la
            # seance ou l'on achete a l'ouverture : avant, ils ne l'etaient qu'a
            # partir de s[i + 2]. Exemple reel du tableau de reference : Vinci,
            # achete le 07-06-2024 a 113,60, plus bas du jour 110,75 sous la vente
            # forcee 110,76 -> vendu le jour meme. L'echeance, elle, ne change pas :
            # la h-ieme seance APRES l'achat, s[i + 1 + h].
            suite = s[i + 1:i + 2 + h]
            px = motif = d_sortie = None
            for b in suite:
                r = mod_positions.tester_seance(b, tp_abs, sl_abs)
                if r:
                    px, motif = r
                    d_sortie = b["date"]
                    break
            if px is None:
                apres = suite[1:]          # l'echeance se compte APRES la seance d'achat
                if not apres:
                    continue
                px, motif, d_sortie = apres[-1]["close"], "HORIZON", apres[-1]["date"]
            # LES FRAIS NE S'ECRIVENT PAS EN DUR. Le proprietaire du chiffre
            # est MODULE_POSITIONS : 0,15 % de la valeur echangee a l'entree ET
            # a la sortie, soit 307,50 EUR sur une sortie a +5 %, non 300 fixes.
            # Un nombre recopie qui contredit son module, c'est R-708.
            q = 100000.0 / pe
            _fo = getattr(mod_positions, "frais_ordre", None)
            if callable(_fo):
                f_tot = _fo(q, pe) + _fo(q, px)      # les DEUX ordres
            else:
                raise RuntimeError("MODULE_POSITIONS n'expose pas frais_ordre : "
                                   "le juge des stratégies ne recopie pas un taux de frais")
            ops.append({"valeur": v, "date_signal": d_sig, "pe": pe, "px": px,
                        "motif": motif, "net": q * (px - pe) - f_tot,
                        "date_sortie": d_sortie})
    return ops, inconnus


def juger(fiche, ops, cours, seances, J, S, mod_pos, mnemo=None,
          _bornes=None, mod_pos_sig=None):
    """Rend les mesures qui disent si le gain veut dire quelque chose.

    AUCUN SEUIL N'EST ECRIT EN DUR : le point mort se calcule depuis les
    reglages de la fiche, le nombre effectif se mesure sur les operations.
    Un taux de 55 % est excellent a +5/-2 et ruineux a +1,2/-1 — juger toutes
    les strategies sur le meme nombre n'a aucun sens (A-280).

    ① RÔLE — Afficher, sous les gains d'une stratégie, les mesures qui disent si
      ces gains veulent dire quelque chose : le taux de réussite au-dessous duquel
      la stratégie perd de l'argent, la tenue sur la partie jamais vue, la tenue sur
      trois fenêtres successives, la sensibilité aux réglages voisins, le pire creux
      et la comparaison au hasard. Sans ce passage, le juge des stratégies rendrait des gains nus
      en les faisant passer pour un jugement.
    ② CONTEXTE D'APPEL — `main`, une fois par fiche jouée, et seulement si le
      module de jugement a pu être chargé. Jamais appelée ailleurs : recherche du
      nom dans les 34 fichiers de `programmes/` le 20-09-2026, un seul appel.
    ③ ENTRÉE — `fiche` : la ligne de stratégie, où sont lus `tp`, `sl`, `horizon`
      et `univers` · `ops` : la liste des opérations rendue par `jouer` · `cours` :
      les séries par valeur · `seances` : l'ensemble de toutes les dates de séance
      connues · `J` : le module de jugement · `S` : le module de statistiques, qui
      peut valoir `None` · `mod_pos` : le module de positions · `mnemo` : la table
      des codes courts, vide par défaut · `_bornes` : le couple des bornes de
      période rendu par la porte 0 · `mod_pos_sig` : un tuple d'un seul élément,
      le module de signal, dont seul le premier élément est employé.
    ④ CONDITIONS D'ENTRÉE — La fiche doit avoir passé la porte 0. Le module de
      jugement doit exposer les huit fonctions appelées ici ; le module de
      statistiques peut manquer, ses deux mesures étant alors perdues.
    ⑤ SORTIE — Ne rend rien. Tout passe par l'affichage.
      [rend: rien]
    ⑥ TRAITEMENT — ① s'arrêter avec un message si moins de cinq opérations ont été
      produites · ② calculer le taux de réussite et le point mort, et afficher la
      marge · ③ compter les épisodes indépendants · ④ couper la période en sept
      dixièmes appris et trois dixièmes jamais vus, avec un embargo entre les deux,
      et afficher le taux de la partie jamais vue avec sa borne basse · ⑤ découper
      la même période en trois fenêtres successives et dire si chacune tient face à
      son point mort · ⑥ rejouer la stratégie avec des réglages voisins et dire si
      le gain s'effondre · ⑦ afficher le gain moyen et sa borne basse · ⑧ afficher
      la plus longue série de pertes et le pire creux · ⑨ tirer des opérations au
      hasard, par valeur puis par date, et dire où se situe la stratégie.
    ⑦ UNITÉ — Les taux de réussite, les points morts et les bornes basses sont des
      POURCENTS entre 0 et 100. Les marges sont des POINTS de pourcentage. Les
      seuils passés au module de jugement sont des FRACTIONS. Les gains et les creux
      sont des EUROS. Les embargos et l'horizon se comptent en SÉANCES ; le temps
      de sortie de creux se compte en JOURS de calendrier.
    ⑧ POURQUOI — AUCUN SEUIL DE STRATÉGIE N'EST ÉCRIT ICI. L'objectif de gain, la
      perte acceptée et l'horizon sont relus dans la fiche, donc dans la ligne du
      registre des stratégies `donnees/cac40_strategies.csv`. Le point mort en
      découle par calcul, au lieu d'être un nombre fixe : un taux de réussite de
      55 % est excellent avec un objectif de +5 % et une perte acceptée de −2 %, et
      ruineux avec +1,2 % et −1 %. Mesuré le 20-09-2026 : le point mort vaut 43,1 %
      pour `C5E10-QA-V1`, réglée à +4 %/−2,5 %, et 32,9 % pour `C5-EI-PARAMS`,
      réglée à +5 %/−2 %. Juger deux stratégies sur le même nombre n'aurait aucun
      sens.
      LA BORNE BASSE EST AFFICHÉE À CÔTÉ DU TAUX, jamais le taux seul : un taux nu
      sur douze opérations ne dit rien. Une mesure : 58,3 % sur 12 opérations a
      une borne basse de 32,0 %, SOUS un point mort de 32,9 % — le rapport affichait
      « +25,3 points de marge » et laissait croire à une marge confortable, alors
      que le cas défavorable est perdant.
      TROIS FENÊTRES, ET PAS UNE SEULE COUPURE : une coupure unique dit « tient-elle
      sur la fin ? », trois fenêtres disent « tient-elle à chaque fois ? ». Mesuré
      le 20-09-2026 sur `C5E10-QA-V1` : la coupure en sept dixièmes annonce 72,0 %
      sur la partie jamais vue, au-dessus du point mort, mais la première des trois
      fenêtres tombe à 66,7 % avec une borne basse de 35,4 %, sous le point mort de
      43,1 %.
      L'ÉTALON DE HASARD TIRE DANS L'UNIVERS DE LA FICHE, jamais dans tout le
      projet. Le juge des stratégies passait les 39 valeurs du projet là où la fiche en déclare
      neuf, et mesurait donc la sélection PLUS l'univers, alors que l'univers est le
      paramètre le plus puissant du système. Mesure de l'écart le 29-08-2026 : le
      hasard rendait +2 963 € avec les 39 valeurs et +22 153 € avec les neuf de la
      fiche. Il paraissait sept fois et demie plus mauvais qu'il ne l'est.
      ET IL SE LIT EN PROPORTION DE TIRAGES BATTUS, jamais sur le seul maximum :
      comparer à un maximum a fait conclure à tort, le 28-08-2026, que le signal
      n'apportait rien. Le seuil retenu par la littérature est 90 à 95 %.
      LA COUPURE DÉCOUPE LA PÉRIODE DE LA FICHE, PAS LE CALENDRIER ENTIER. Défaut
      trouvé le 29-08-2026 : la période avait été branchée sur `jouer` mais pas sur
      la coupure, qui recevait toujours le calendrier complet du projet. La
      frontière tombait au 2025-11-06 au lieu du 2025-08-19, et la partie jamais vue
      passait de 21 à 12 opérations : neuf opérations perdues sur la seule partie
      qui compte.
    ⑨ CE QUI CLOCHE —
      ① L'ABSENCE DU MODULE DE STATISTIQUES N'EST PAS ANNONCÉE. Mesuré le
      20-09-2026 en appelant `juger` avec ce module à `None` sur la fiche
      `C5E10-QA-V1` : le rapport garde ses quinze autres lignes et remplace deux
      mesures par « VOISINAGE non mesure : 'NoneType' object has no attribute
      'calculer_stabilite_parametrique' » et « CREUX non mesure : 'NoneType' object
      has no attribute 'calculer_time_underwater' ». Aucune alerte en tête, alors
      que `main` en affiche une quand c'est le module de jugement qui manque. Un
      lecteur pressé lit un rapport complet.
      ② SEPT BLOCS RATTRAPENT TOUTE ERREUR ET L'ÉCRIVENT « NON MESURÉ ». Un module
      absent, une fonction renommée, une division par zéro et une faute dans le
      code du juge des stratégies produisent exactement la même ligne. Rien ne distingue « cette
      mesure n'existe pas ici » de « cette mesure s'est trompée ».
      ③ ELLE NE REND RIEN, DONC SON APPELANT NE SAIT PAS SI LE JUGEMENT A EU LIEU.
      Mesuré le 20-09-2026 : l'appel rend `None`, y compris quand la fonction
      s'arrête d'emblée faute d'opérations. `main` enchaîne sans distinguer un
      jugement complet d'un jugement qui ne s'est pas fait.
      ④ LE SEUIL DE CINQ OPÉRATIONS EST ÉCRIT DANS LE CODE, à deux endroits : une
      fois pour refuser de juger l'ensemble, une fois pour refuser de juger une
      fenêtre. Ce nombre ne vient d'aucun fichier de gouvernance, et le changer
      suppose de modifier le code à deux endroits.
      ⑤ LES BORNES DE LA PÉRIODE SONT RECALCULÉES DANS UNE ENVELOPPE DE SECOURS
      ET RÉUTILISÉES DANS LA SUIVANTE. L'ensemble des séances borné est construit à l'intérieur du bloc
      de la coupure, puis relu par le bloc des trois fenêtres, qui est un autre bloc
      de secours. Si le premier bloc venait à changer, le second lirait une valeur
      qu'il n'a pas posée.
      ⑥ LE DERNIER PARAMÈTRE S'APPELLE `mod_pos_sig` ET NE CONTIENT QUE LE MODULE
      DE SIGNAL. `main` lui passe un tuple d'un seul élément, et seul cet élément
      est employé, pour rejouer les variantes de réglages. Le nom laisse croire
      qu'il porte les positions ET le signal.
      ⑦ LES VARIANTES DE RÉGLAGES SONT DES ESSAIS ET NE SONT PAS COMPTÉES COMME
      TELLES. Le voisinage rejoue la stratégie avec des réglages écartés de 10 %,
      cinq variations ; le commentaire du code le signale lui-même comme un point à
      surveiller. Aucun compteur d'essais n'est incrémenté.
    ⑩ EFFET — N'écrit aucun fichier et ne touche pas au réseau. AFFICHE le bloc de
      jugement : 19 lignes mesurées le 20-09-2026 sur la fiche `C5E10-QA-V1`. Elle
      APPELLE le module de jugement, le module de statistiques et, par `_rejouer`,
      le module de signal et le module de positions. Elle ne modifie ni la fiche ni
      les opérations reçues.
    ⑪ TERMINAISON — Rend toujours la main, sans valeur. Elle ne lève pas : chacun
      de ses neuf calculs est enveloppé d'une enveloppe de secours, sauf le point mort,
      dont l'échec arrêterait la fonction. Et un de ses appels peut ne pas revenir :
      l'étalon de hasard rejoue 120 tirages par mode, et le voisinage rejoue la
      stratégie entière cinq fois, sans qu'aucun temps ne soit borné.
      [sort: non]
    ⑫ DÉFINITIONS
      l'horizon : le nombre de séances pendant lesquelles une position est
        tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      l'étalon de hasard : le résultat qu'obtiendraient des entrées tirées au
        sort jouées aux mêmes règles, et auquel la stratégie doit être
        comparée
      la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage
        sur vingt
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      la partie jamais vue : la fin de la période, celle sur laquelle la
        stratégie n'a pas été réglée, et donc la seule qui prouve quelque
        chose
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les
        mesures disant si un gain veut dire quelque chose.
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le module de statistiques : le programme qui porte le voisinage des
        réglages et le pire creux,
        `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a
        lieu à l'ouverture de la séance suivante
      le SL : la perte acceptée qui ferme la position, une fraction du prix
        d'entrée — 0,025 vaut −2,5 %.
      le taux de réussite : la part des opérations qui se sont refermées sur
        un gain, écrite en pourcent
      le TP : l'objectif de gain qui ferme la position, une fraction du prix
        d'entrée — 0,040 vaut +4 %.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
"""
    mnemo = mnemo or {}
    tp = pourcent(fiche["tp"])
    sl = pourcent(fiche["sl"])
    h = lire_horizon(fiche["horizon"])
    n = len(ops)
    if n < 5:
        print("    JUGEMENT : trop peu d'operations pour juger")
        return
    wr = round(100.0 * sum(1 for o in ops if o["net"] > 0) / n, 1)

    pm = J.point_mort_en_fractions(tp, sl, mod_positions=mod_pos)   # FRACTIONS, cf. Y1
    print("\n    ── JUGEMENT ─────────────────────────────────────────")
    print("    POINT MORT           {:.1f} %  ·  reussite {} %  ·  marge {:+.1f} pts"
          .format(pm, wr, wr - pm))

    try:
        e = J.episodes(ops, seances)
        print("    EPISODES             {} operations . {} jours . {} episodes"
              .format(e["n_operations"], e.get("n_jours_signal", "?"), e["n_episodes"]))
    except Exception as ex:
        print("    EPISODES             non mesures : %s" % ex)

    try:
        # LA COUPURE DECOUPE LA PERIODE DE LA FICHE, PAS LE CALENDRIER ENTIER.
        # Defaut trouve le 29/08 : la periode avait ete branchee sur jouer()
        # mais PAS sur la coupure, qui recevait toujours le calendrier complet
        # du projet. Frontiere au 2025-11-06 au lieu du 2025-08-19, et la partie
        # jamais vue tombait de 21 a 12 operations — on perdait neuf operations
        # sur la SEULE partie qui compte. Correction juste pour un appel, fausse
        # pour le voisin : c'est A-308 a l'identique.
        _sea = seances
        if _bornes:
            _sea = {d for d in seances if _bornes[0] <= d <= _bornes[1]}
        c = J.coupure_70_30(ops, _sea, horizon=h)
        a, b = c["res_70"], c["res_30"]
        print("    COUPURE 70/30        frontiere {} . embargo {} seances"
              .format(c["frontiere"], c["embargo_seances"]))
        print("      apprentissage      {} op . {} %".format(a["n"], a.get("wr")))
        print("      JAMAIS VUE         {} op . {} %  <- c'est CE chiffre qui compte"
              .format(b["n"], b.get("wr")))
        if b.get("wr") is not None:
            print("      verdict            {} point mort de {:+.1f} pts"
                  .format("au-dessus du" if b["wr"] > pm else "sous le", b["wr"] - pm))
            # ET SURTOUT LA BORNE BASSE, exigee par l'ETUDE 11 et jamais branchee.
            # Un taux nu sur douze operations ne dit rien : 58,3 % sur 12 a une
            # borne basse de 32,0 %, SOUS le point mort de 32,9. Le rapport
            # affichait « +25,3 points de marge » et laissait croire a une marge
            # confortable, alors que le cas defavorable est perdant.
            _bb = J.wilson_bas(b["n"], b["wr_exact"] if b.get("wr_exact")
                               is not None else b["wr"])
            if _bb is not None:
                print("      AU PIRE            {:.1f} %  ->  {}"
                      .format(_bb, "encore au-dessus du point mort" if _bb > pm
                              else "SOUS le point mort : cas defavorable PERDANT"))
    except Exception as ex:
        print("    COUPURE 70/30        non mesuree : %s" % ex)

    # TROIS FENETRES, PAS UNE SEULE COUPURE. La methode l'exige (ETUDE 11) et
    # le juge des stratégies ne rendait que la coupure 70/30. Une coupure unique dit « tient-elle
    # sur la fin ? » ; trois fenetres disent « tient-elle A CHAQUE FOIS ? ».
    try:
        fg = J.fenetres_glissantes(ops, _sea if _bornes else seances, n=3,
                                   horizon=h, point_mort_pct=pm)
        if fg.get("fenetres"):
            print("    TROIS FENETRES       embargo {} seances"
                  .format(fg["embargo_seances"]))
            # ON DIT CE QUE L'EMBARGO LAISSE DEHORS. Sans cette ligne, un
            # lecteur qui additionne les trois fenetres trouve un compte
            # inferieur au total sans savoir pourquoi — jusqu'a une operation
            # sur cinq pour la candidate, mesure le 29/08.
            if fg.get("n_ecartees_embargo"):
                print("      {} operation(s) sur {} tombent dans les trous"
                      " d'embargo entre fenetres et ne sont comptees dans"
                      " aucune"
                      .format(fg["n_ecartees_embargo"], fg["n_operations"]))
            for x in fg["fenetres"]:
                if x["n"] < 5:
                    print("      {} {} -> {}  {} op — trop peu pour juger"
                          .format(x["n_fenetre"], x["debut"], x["fin"], x["n"]))
                else:
                    # LE CHIFFRE EST LIVRE AVEC CE QU'IL MESURE. « au pire
                    # 35,4 % » ne dit rien sans le point mort a cote.
                    _b = x.get("au_pire")
                    _t = x.get("tient")
                    print("      {} {} -> {}  {:>2} op . {:>5} % . {:>+9,.0f} EUR"
                          " . au pire {:.1f} % {} point mort {:.1f}"
                          .format(x["n_fenetre"], x["debut"], x["fin"], x["n"],
                                  x["wr"], x["net"], _b,
                                  "AU-DESSUS du" if _t else "SOUS le", pm)
                          .replace(",", " "))
            # LE VERDICT PORTE SUR LE POINT MORT, PAS SUR LE SEUL GAIN.
            _ns = fg.get("n_sous_le_point_mort", 0)
            if fg.get("toutes_tiennent") is not None:
                if fg["toutes_tiennent"]:
                    print("      verdict            les {} fenetres exploitables"
                          " TIENNENT face a leur point mort".format(fg["n_utiles"]))
                else:
                    print("      verdict            {} fenetre(s) sur {} SOUS le"
                          " point mort — gagnantes en euros, mais le cas"
                          .format(_ns, fg["n_utiles"]))
                    print("                         defavorable y est PERDANT")
    except Exception as ex:
        print("    TROIS FENETRES       non mesurees : %s" % ex)

    # LE VOISINAGE : COLLINE OU AIGUILLE. Exige par la methode (ETUDE 11), et
    # jamais execute — la fonction du module de statistiques n'etait appelee
    # nulle part. Elle fait varier les reglages de plus ou moins 10 % et regarde
    # si le resultat s'effondre.
    # CE QU'ELLE DISTINGUE : une strategie posee sur une COLLINE tient encore
    # quand on bouge un peu ses reglages — le gain baisse sans disparaitre. Une
    # strategie posee sur une AIGUILLE s'effondre au premier pas de cote : elle
    # ne decrivait pas le marche, elle collait a un jeu de donnees precis.
    # ATTENTION AU COMPTAGE DES ESSAIS (A-226) : ces variantes sont des essais,
    # et elles doivent etre comptees comme tels.
    try:
        def _rejouer(p):
            """Rejoue la stratégie avec des réglages modifiés et rend son résultat.

            ① RÔLE — Répondre à une seule question, posée par le module de statistiques :
              que devient le résultat si l'on bouge un peu les réglages ? Une stratégie
              posée sur une colline tient encore quand on décale ses seuils — le gain
              baisse sans disparaître. Une stratégie posée sur une aiguille s'effondre au
              premier pas de côté : elle ne décrivait pas le marché, elle collait à un jeu
              de données précis.
            ② CONTEXTE D'APPEL — Elle n'est jamais appelée par son nom. Elle est REMISE au
              module de statistiques, qui l'appelle une fois par variante de réglages :
              cinq variations à plus ou moins 10 % des réglages d'origine, mesuré le
              20-09-2026 sur la fiche `C5E10-QA-V1`.
            ③ ENTRÉE — `p` : un dictionnaire de réglages composé par le module de
              statistiques, portant `tp`, `sl` et `horizon`.
            ④ CONDITIONS D'ENTRÉE — Les trois réglages doivent être présents et lisibles en
              nombre. La fonction vit à l'intérieur de `juger` et réemploie la fiche, les
              cours, la table des mnémoniques, les deux modules et les bornes de période de
              l'appel en cours.
            ⑤ SORTIE — UNE valeur : un dictionnaire de deux cases, le gain total en euros
              et le taux de réussite, tous deux à zéro si la variante n'a produit aucune
              opération.
              [rend: 1]
            ⑥ TRAITEMENT — ① copier la fiche en cours · ② y écrire les trois réglages de la
              variante, l'horizon étant arrondi à la séance entière · ③ rejouer la stratégie
              sur la même période · ④ résumer et rendre le gain et le taux.
            ⑦ UNITÉ — Les seuils reçus sont des FRACTIONS du prix d'entrée. L'horizon est
              un NOMBRE DE SÉANCES, reçu en nombre à virgule et arrondi à l'entier. Le gain
              est en EUROS, le taux en POURCENT entre 0 et 100.
            ⑧ POURQUOI — La fiche est COPIÉE avant d'être modifiée : la fiche d'origine est
              celle que `main` affiche et que le jugement relit, et la modifier ferait
              paraître, dans le rapport, les réglages de la dernière variante au lieu de
              ceux de la stratégie. Mesuré le 20-09-2026 sur `C5E10-QA-V1` : le rapport
              affiche bien « TP +4.0% . SL -2.5% . horizon 20 seances » après les cinq
              variantes.
            ⑨ CE QUI CLOCHE —
              ① LES VARIANTES SONT DES ESSAIS ET NE SONT COMPTÉES NULLE PART. Chaque appel
              rejoue une stratégie complète sur tout l'historique ; le commentaire du code
              le signale lui-même comme un point à surveiller. Aucun compteur d'essais de
              la stratégie n'est incrémenté.
              ② UN HORIZON ARRONDI À ZÉRO PASSERAIT. L'arrondi porte sur le nombre reçu,
              sans borne basse : une variation qui ferait descendre l'horizon au-dessous
              d'une demi-séance donnerait zéro, et `jouer` ne produirait alors aucune
              opération, ce que la fonction rendrait comme un gain de zéro euro. Cela ne se
              produit pas aux réglages actuels, l'horizon le plus court du registre étant de
              20 séances.
              ③ Elle réemploie le module de signal à travers un tuple d'un seul élément
              passé à `juger` sous le nom `mod_pos_sig`, dont le nom laisse croire qu'il
              porte les positions.
            ⑩ EFFET — Aucun sur le disque : ni lecture ni écriture de fichier, aucun accès
              réseau. Elle APPELLE `jouer`, donc le module de signal et le module de
              positions. Elle ne modifie pas la fiche d'origine, qu'elle copie.
            ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER si `jouer` lève ;
              l'erreur est alors rattrapée par le enveloppe de secours du voisinage dans `juger`,
              qui affiche « VOISINAGE non mesure ». Et un de ses appels peut ne pas
              revenir : `jouer` appelle du code tiers dont le temps n'est pas borné.
              [sort: non]
            ⑫ DÉFINITIONS
              l'horizon : le nombre de séances pendant lesquelles une position est
                tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
              la fiche : la ligne d'une stratégie au registre des stratégies
                `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
                acceptée, son horizon et son univers
              le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
                stratégie sur l'historique des cours et rend la liste de ses
                opérations
              le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
                taux de frais et des règles de sortie d'une position.
              le module de signal : le programme qui décide quelles valeurs acheter
              le module de statistiques : le programme qui porte le voisinage des
                réglages et le pire creux,
                `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
              le registre des stratégies : le fichier `cac40_strategies.csv`, une
                ligne par stratégie, qui porte leur état civil — identifiant,
                réglages, résultats connus
              le SL : la perte acceptée qui ferme la position, une fraction du prix
                d'entrée — 0,025 vaut −2,5 %.
              le taux de réussite : la part des opérations qui se sont refermées sur
                un gain, écrite en pourcent
              le TP : l'objectif de gain qui ferme la position, une fraction du prix
                d'entrée — 0,040 vaut +4 %.
              un mnémonique : le code court d'une valeur de bourse, `TTE` pour
                TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
              une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
              une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
              une séance : une journée de bourse pour une valeur, avec son ouverture,
                son plus haut, son plus bas, sa clôture et son volume.
              une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
                dans les fichiers du projet
            
              la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
"""
            f2 = dict(fiche)
            f2["tp"] = str(p["tp"])
            f2["sl"] = str(p["sl"])
            f2["horizon"] = str(int(round(p["horizon"])))
            o2, _ = jouer(f2, cours, mnemo, mod_pos_sig[0], mod_pos,
                          periode=_bornes)
            r2 = resumer(o2)
            return {"net": r2.get("net", 0.0), "wr": r2.get("wr", 0.0)}
        st = S.calculer_stabilite_parametrique(
            _rejouer, {"tp": tp, "sl": sl, "horizon": float(h)},
            pourcentage=0.10, n_variations=5)
        print("    VOISINAGE            gain de {:+,.0f} a {:+,.0f} EUR "
              "(ecart {:.0f} %)"
              .format(st.get("net_min", 0), st.get("net_max", 0),
                      100 * st.get("ecart_relatif", 0)).replace(",", " "))
        print("      verdict            {}"
              .format("COLLINE — les reglages voisins tiennent"
                      if st.get("stable")
                      else "AIGUILLE — un pas de cote fait s'effondrer le gain"))
    except Exception as ex:
        print("    VOISINAGE            non mesure : %s" % ex)

    try:
        g = J.borne_basse_gain(ops)
        print("    GAIN MOYEN           {:+,.0f} EUR  ·  au pire {:+,.0f} EUR"
              .format(g["gain_moyen"], g["borne_basse_5pct"]).replace(",", " "))
    except Exception as ex:
        print("    GAIN MOYEN           non mesure : %s" % ex)

    try:
        print("    PIRE SERIE           {} pertes d'affilee"
              .format(J.plus_longue_serie_de_pertes(ops)))
        tu = S.calculer_time_underwater(
            [{"date": o["date_signal"], "gain": o["net"]} for o in ops])
        print("    PIRE CREUX           {:+,.0f} EUR  ·  {} jours pour en sortir"
              .format(-abs(tu.get("dd_max_eur", 0)),
                      tu.get("time_underwater_max_jours", "?")).replace(",", " "))
    except Exception as ex:
        print("    CREUX                non mesure : %s" % ex)

    # L'ETALON DE HASARD — un resultat ne vaut que par son ECART au hasard.
    # On lit la PROPORTION de tirages battus, JAMAIS un maximum : comparer a
    # un maximum a fait conclure a tort, le 28/08, que le signal n'apportait
    # rien. Le seuil retenu par la litterature est 90 a 95 %.
    try:
        # LE HASARD TIRE DANS L'UNIVERS DE LA FICHE, JAMAIS DANS TOUT LE PROJET.
        # Defaut trouve le 29/08 par relecture adverse : le juge des stratégies passait les 39
        # valeurs du projet la ou la fiche en declare 9. Le mode « valeur » ne
        # mesurait donc plus « la selection comptait-elle » mais selection PLUS
        # univers — or l'univers est le parametre le plus puissant du systeme,
        # 61 % de reussite dedans contre 40,8 % dehors.
        # MESURE DE L'ECART : le hasard rendait +2 963 EUR avec les 39 valeurs,
        # +22 153 EUR avec les 9 de la fiche. Il paraissait SEPT FOIS ET DEMIE
        # plus mauvais qu'il ne l'est, et le rapport concluait donc dans le sens
        # flatteur. La strategie reste devant, l'ecart reel est bien plus mince.
        univ = [mnemo.get(x.strip().upper(), cle_valeur(x))
                for x in fiche["univers"].split(",") if x.strip()]
        univ = [v for v in univ if v in cours]
        for mode, lib in (("valeur", "l'ACTION au hasard"),
                          ("date", "les DATES au hasard")):
            hz = J.etalon_hasard(ops, cours, univ, tp, sl, h, mod_pos,
                                 mode=mode, n_tirages=120)
            if hz.get("n_tirages"):
                # UN ETALON SE LIT EN PROPORTION DE TIRAGES BATTUS, jamais sur
                # la seule mediane : le seuil retenu par la litterature est
                # 90 a 95 %. Afficher la mediane seule cache si la strategie
                # bat le 95e centile ou seulement la moitie des tirages.
                _net = sum(o["net"] for o in ops)
                print("    HASARD, {:<20} median {:+,.0f} . 95e {:+,.0f} . max {:+,.0f} EUR"
                      .format(lib, hz["gain_median"], hz["gain_95pct"],
                              hz["gain_max"]).replace(",", " "))
                print("      la strategie rend {:+,.0f} EUR -> {} 95e centile, {} maximum"
                      .format(_net,
                              "au-dessus du" if _net > hz["gain_95pct"] else "sous le",
                              "au-dessus du" if _net > hz["gain_max"] else "sous le")
                      .replace(",", " "))
    except Exception as ex:
        print("    HASARD               non mesure : %s" % ex)
    print("    ─────────────────────────────────────────────────────")


def resumer(ops):
    """Résume une liste d'opérations en quatre chiffres.

    ① RÔLE — Réduire la liste des opérations d'une stratégie aux quatre chiffres
      qui la décrivent : combien d'opérations, quel taux de réussite, quel gain
      total, et comment les sorties se répartissent. C'est ce que le rapport affiche
      en tête de chaque fiche, et ce que le calibrage compare au golden.
    ② CONTEXTE D'APPEL — Quatre appelants, tous dans ce programme.
      · `main`, une fois par fiche jouée.
      · `calibrer`, une fois, sur les opérations de la fiche de calibrage.
      · `_rejouer`, à l'intérieur de `juger`, une fois par variante de réglages.
      · `juger`, indirectement, à travers `_rejouer`.
    ③ ENTRÉE — `ops` : la liste des opérations rendue par `jouer`, chacune portant
      au moins son gain net et son motif de sortie.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une liste vide est une situation prévue.
    ⑤ SORTIE — UNE valeur, et elle a DEUX FORMES. Sur une liste vide, un
      dictionnaire d'UNE seule case, le compte à zéro. Sinon, un dictionnaire de
      CINQ cases : le compte, le taux de réussite arrondi à une décimale, le taux
      exact non arrondi, le gain total arrondi au centime, et le compte des motifs
      de sortie. Exemple réel, mesuré le 20-09-2026 sur la fiche `C5E10-QA-V1` :
      62 opérations, 71,0 % de réussite, +120 046,63 €, et les motifs
      `{'HORIZON': 2, 'SL': 15, 'SL_GAP': 3, 'TP': 33, 'TP_GAP': 9}` — avant le
      28-09-2026 ; depuis que la séance d'achat compte (R-608), 62 opérations,
      66,1 % de réussite, +98 930,83 €.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre le compte à zéro si la liste est vide · ② compter les
      opérations dont le gain net est strictement positif · ③ compter les motifs de
      sortie · ④ composer le dictionnaire, avec le taux arrondi ET le taux exact
      côte à côte.
    ⑦ UNITÉ — Le compte est un NOMBRE D'OPÉRATIONS. Le taux de réussite est un
      POURCENT entre 0 et 100. Le gain est en EUROS, arrondi au centime.
    ⑧ POURQUOI — LE TAUX EXACT EST GARDÉ À CÔTÉ DE L'ARRONDI D'AFFICHAGE. Le module
      de jugement écrit qu'un témoin nourri d'un arrondi mesure l'arrondi et non le
      calcul, et le juge des stratégies lui passait justement le taux déjà arrondi à une décimale.
      Mesure : 12 opérations gagnantes sur 21 donnent une borne basse de 36,5462 %
      quand le calcul part du taux exact, et 36,5079 % quand il part de 57,1 %.
      L'écart n'a pas changé le verdict ce jour-là, mais la règle était écrite au
      bon endroit et violée à l'appel — septième fois dans la même journée qu'une
      correction se trouvait juste chez celui qui la porte et absente chez le
      voisin, ce que le BACKLOG consigne sous l'action A-308.
    ⑨ CE QUI CLOCHE —
      ① LES DEUX FORMES DE SORTIE NE PORTENT PAS LES MÊMES CASES, ET RIEN NE LE
      SIGNALE. Sur une liste vide, les cases `wr`, `wr_exact`, `net` et `motifs`
      n'existent pas. `main` s'en protège en testant le compte avant de lire le
      reste, et `_rejouer` en demandant les cases avec une valeur de repli ; un
      appelant qui les lirait directement lèverait une erreur.
      ② UNE OPÉRATION DONT LE GAIN NET EST EXACTEMENT NUL EST COMPTÉE PERDANTE. Le
      test retient le gain strictement positif. Frais payés, un gain exactement nul
      est improbable, mais le choix n'est écrit nulle part.
      ③ LE GAIN TOTAL EST ARRONDI AU CENTIME ALORS QUE LE TAUX GARDE SA FORME
      EXACTE. Le calibrage compare ce gain arrondi à celui du golden : un écart
      inférieur au centime serait invisible. C'est sans effet aujourd'hui, l'écart
      mesuré le 20-09-2026 étant de +31 740,56 €.
    ⑩ EFFET — Aucun : elle ne lit ni n'écrit aucun fichier, ne touche pas au
      réseau, n'affiche rien, et ne modifie pas la liste reçue.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas sur une liste
      d'opérations bien formée. Aucun de ses appels ne termine le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et
        des actions du projet, où chaque ligne porte un identifiant en `A-`
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige
        de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les
        mesures disant si un gain veut dire quelque chose.
      le taux de réussite : la part des opérations qui se sont refermées sur
        un gain, écrite en pourcent
      un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte
        que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
      un témoin : un jeu de chiffres dont on connaît d'avance le résultat,
        employé pour prouver qu'un instrument fonctionne avant de s'en
        servir
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    if not ops:
        return {"n": 0}
    g = sum(1 for o in ops if o["net"] > 0)
    motifs = {}
    for o in ops:
        motifs[o["motif"]] = motifs.get(o["motif"], 0) + 1
    # ON GARDE LE TAUX EXACT A COTE DE L'ARRONDI D'AFFICHAGE.
    # Le module de jugement ecrit « un temoin nourri d'un arrondi mesure
    # l'arrondi, pas le calcul » — et le juge des stratégies lui passait justement « wr »,
    # deja arrondi a une decimale. Mesure : 12/21 exact donne une borne basse de
    # 36,5462 %, l'arrondi 57,1 % donne 36,5079 %. Sans effet sur ce verdict,
    # mais la regle est ecrite au bon endroit et violee a l'appel — septieme
    # fois dans la journee qu'une correction est juste chez celui qui la porte
    # et absente chez le voisin (A-308).
    return {"n": len(ops), "wr": round(100.0 * g / len(ops), 1),
            "wr_exact": 100.0 * g / len(ops),
            "net": round(sum(o["net"] for o in ops), 2),
            "motifs": dict(sorted(motifs.items()))}


def calibrer(cours, mnemo, mod_signal, mod_positions, golden, f_cours=None, table=None):
    """Calibre l'INSTRUMENT, pas la strategie : une strategie neuve n'a aucun
    chiffre de reference. LE NET N'EST PAS EXIGE — le golden a ete produit avec
    la mecanique de sortie theorique, le juge des stratégies emploie la mecanique reelle, et
    l'ecart mesure vaut plus 12 501 euros (A-290). C'est un changement DELIBERE
    de definition, que R-701 autorise expressement, pas une regression.

    ① RÔLE — Vérifier que le juge des stratégies retrouve un résultat déjà connu avant de juger
      quoi que ce soit. Si l'instrument ne retrouve pas ce qu'il a mesuré la
      dernière fois, rien de ce qu'il mesurera aujourd'hui ne vaut, et le programme
      s'arrête.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après la porte 0 et avant de juger
      la moindre fiche, et seulement si un fichier de chiffres figés a été trouvé.
      Jamais appelée ailleurs.
    ③ ENTRÉE — `cours` : les séries par valeur sur lesquelles rejouer · `mnemo` :
      la table des codes courts · `mod_signal` : le module de signal · `mod_positions` :
      le module de positions · `golden` : le contenu du fichier de chiffres figés,
      déjà lu · `f_cours` : le chemin du fichier de cours employé, pour en vérifier
      l'empreinte, `None` si l'appelant n'en donne pas. Mesuré le 20-09-2026,
      `main` passe le témoin du golden quand son empreinte est conforme, et le
      fichier de cours vivant sinon. `table` (depuis le 28-09-2026) : le chemin du
      tableau de référence des 100 trades, que `main` passe quand il calibre sur le
      témoin du golden, `None` sinon.
    ④ CONDITIONS D'ENTRÉE — Le golden doit porter une entrée `C5-ETENDU-10` avec
      sa comptabilité « jetons illimités ». Le module de signal doit exposer la
      liste de valeurs `C5E10_UNIVERS` et la fonction `signaux_c5etendu10`. Les
      cours doivent couvrir la période de référence.
    ⑤ SORTIE — DEUX valeurs : un oui-ou-non qui dit si l'instrument est calibré, et
      la liste des lignes à afficher. Le oui-ou-non porte sur le nombre d'opérations
      retrouvé et, quand le tableau de référence est donné, sur chaque sortie
      (famille et date) comparée à ce tableau.
      [rend: 2]
    ⑥ TRAITEMENT — ① refuser si le golden ne porte aucun chiffre de référence ·
      ② comparer le nombre de lignes et l'empreinte du fichier de cours à ceux que
      le golden déclare, et le DIRE sans bloquer · ③ prendre la date de fin déclarée
      par le golden · ④ composer une fiche de calibrage et la faire passer par la
      porte 0 · ⑤ rejouer cette fiche sur la période qu'elle déclare · ⑥ comparer le
      nombre d'opérations au chiffre figé, et afficher le taux de réussite et le
      gain à titre d'information · ⑦ si le tableau de référence est donné,
      comparer chaque sortie, famille et date, trade par trade, et l'exiger.
    ⑦ UNITÉ — Le nombre d'opérations est un COMPTE, exigé au signal près. Le taux
      de réussite est un POURCENT, le gain en EUROS. Les empreintes sont des nombres
      hexadécimaux de 16 caractères. Les lignes du fichier de cours se comptent en
      LIGNES DE TEXTE.
    ⑧ POURQUOI — LE NOMBRE D'OPÉRATIONS ET CHAQUE SORTIE SONT EXIGÉS ; le gain ne
      l'est pas. Depuis le 28-09-2026 (défaut 4 de A-491), chaque sortie se compare
      au tableau de référence des 100 trades, famille et date : le compte seul était
      juste alors que le juge des stratégies ne testait pas la séance d'achat — 91 dates de sortie
      sur 100, 97 familles. Après la réparation : 100 sur 100, et le taux de
      réussite retrouve celui du golden, 61,0 %. Le gain ne peut pas être exigé : le golden a été produit avec la mécanique de
      sortie théorique, et le juge des stratégies emploie la mécanique réelle du module de
      positions, et un autre tarif de frais. Avant le 28-09-2026, trois opérations
      que le tableau compte perdantes étaient gagnantes chez le juge des stratégies (Bouygues et Eiffage
      du 30-04-2026, Renault du 20-05-2026) : elles venaient du défaut 4, pas d'un
      saut d'ouverture, et il n'y en a plus aucune (relecteur du Chat). Ce qui est
      calibré ici, c'est la DÉTECTION DES SIGNAUX ET CHAQUE SORTIE, famille et date.
      LE CALIBRAGE SE FAIT SUR LE PÉRIMÈTRE EXACT DU GOLDEN. Sans cette borne, les
      cours du jour ajoutent des signaux postérieurs à la fenêtre de référence et le
      calibrage échoue à tort : constaté le 26-08-2026, 103 opérations au lieu de
      100, trois signaux nés après le 2026-07-10.
      LA FICHE DE CALIBRAGE PASSE PAR LA PORTE 0, COMME TOUTES LES AUTRES. Elle
      était construite en dur sans période et bornait son périmètre par un autre
      chemin : l'exigence vivait à deux endroits sous deux formes, sans que rien ne
      garantisse qu'elles disent la même chose. Le calibrage prouve désormais la
      porte au lieu de la contourner.
      ET LA PÉRIODE JOUÉE EST CELLE QUI A ÉTÉ DÉCLARÉE. La borne basse ouverte
      vivait à deux endroits ; un seul avait été corrigé, et l'appel gardait la
      borne écrite en dur. Les deux disaient la même chose par accident, mais elles
      ne venaient pas du même endroit, et le calibrage serait passé si elles avaient
      divergé.
    ⑨ CE QUI CLOCHE —
      ① LES TROIS SEUILS DE LA STRATÉGIE DE RÉFÉRENCE SONT ÉCRITS DANS LE CODE DU
      JUGE DES STRATÉGIES. La fiche de calibrage porte `+4.0%`, `-2.5%` et `20` en clair. Les mêmes
      trois chiffres sont écrits au REGISTRE sous la règle R-201 : « TP +4 % ·
      SL −2,5 % · 20 séances ». Mesuré le 20-09-2026, le registre des stratégies
      `donnees/cac40_strategies.csv` ne porte AUCUNE ligne d'identifiant
      `C5-ETENDU-10` : ces seuils ne peuvent donc pas être lus dans le fichier
      d'état civil, et ils sont recopiés ici. Un chiffre qui existe ailleurs ne se
      recopie pas (R-708) : le jour où la règle R-201 changera, le calibrage
      continuera d'exiger les anciens seuils, et il passera au vert sur une
      stratégie qui n'existe plus.
      ② L'UNIVERS DE LA FICHE DE CALIBRAGE VIENT DU CODE DU MODULE DE SIGNAL. Il est
      lu dans la liste `C5E10_UNIVERS`, écrite ligne 188 de
      `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py` : dix sociétés,
      exactement celles que la règle R-201 énumère. Deux écritures de la même liste,
      l'une au REGISTRE et l'autre dans le code, sans que rien ne les confronte.
      ③ LE COMPTAGE DES LIGNES DU FICHIER DE COURS INCLUT L'EN-TÊTE, ET LE GOLDEN
      NON. Mesuré le 20-09-2026 sur le témoin déposé : le fichier porte
      25 112 sauts de ligne et 25 111 lignes de données, le golden déclare
      25 111 lignes, et l'empreinte calculée vaut `e472c09da5679ec3`, exactement
      celle que le golden déclare. La sortie réelle du juge des stratégies est pourtant :
      « ATTENTION - LES DONNEES ONT CHANGE depuis le golden : 25112 lignes contre
      25111, empreinte e472c09da5679ec3 contre e472c09da5679ec3. » L'alerte se
      déclenche à chaque passage, sur les données exactes de la référence, et elle
      affiche deux empreintes identiques à l'appui d'un changement. Une alerte
      permanente apprend à ne plus regarder.
      ④ LE CALCUL D'EMPREINTE EST REFAIT À LA MAIN ALORS QUE LA FONCTION EXISTE. La
      fonction `empreinte` de ce même fichier fait exactement cela ; ce passage
      réimporte la bibliothèque et refait le calcul. Relevé le 20-09-2026 :
      `hexdigest()[:16]` apparaît 3 fois dans le fichier, l'appel `empreinte(`
      seulement 2.
      ⑤ LE NOM DE LA FONCTION DE SIGNAL EST ÉCRIT ICI ET RÉÉCRIT DANS `main`. Les
      deux disent `signaux_c5etendu10`, et `programmes/JUGER_SUR_8_CRITERES.py` le
      réécrit une troisième fois à sa ligne 1203, en disant explicitement qu'il
      reprend la valeur du juge des stratégies.
      ⑥ LA DATE DE FIN A UNE VALEUR DE REPLI ÉCRITE EN DUR, `2026-07-10`, employée
      si le golden ne déclare pas la sienne. Un golden muet ferait donc calibrer sur
      une fenêtre choisie ailleurs que dans le golden, sans qu'un mot ne soit dit.
      ⑦ L'ÉCHEC DE LECTURE DU FICHIER DE COURS EST RATTRAPÉ ET RÉDUIT À UNE LIGNE
      « donnees du golden non verifiables », sans bloquer. Le calibrage continue
      alors sans savoir sur quelles données il porte.
    ⑩ EFFET — LIT le fichier de cours en entier pour en calculer l'empreinte. N'écrit
      aucun fichier, ne touche pas au réseau, n'affiche rien elle-même : elle rend
      des lignes que `main` affiche. Elle APPELLE `jouer`, donc le module de signal
      et le module de positions.
    ⑪ TERMINAISON — Rend la main dans le cas normal, avec le verdict et les lignes.
      PEUT LEVER si `porte_0` rend deux valeurs au lieu de trois, ce qui
      arriverait si la période composée ici devenait illisible, et si `jouer` ne
      trouve pas la fonction de signal attendue. Et un de ses appels peut ne pas
      revenir : `jouer` appelle du code tiers dont le temps n'est pas borné.
      [sort: non]
    ⑫ DÉFINITIONS
      jetons illimités : la seconde comptabilité, où toute position s'ouvre
        sans limite ; elle ne correspond à aucun portefeuille réel.
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ;
        deux fichiers de même empreinte ont le même contenu
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage
        sur vingt
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      le backtest : le rejeu d'une stratégie sur des cours passés, pour
        estimer ce qu'elle aurait donné
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige
        de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le SL : la perte acceptée qui ferme la position, une fraction du prix
        d'entrée — 0,025 vaut −2,5 %.
      le taux de réussite : la part des opérations qui se sont refermées sur
        un gain, écrite en pourcent
      le TP : l'objectif de gain qui ferme la position, une fraction du prix
        d'entrée — 0,040 vaut +4 %.
      le témoin du golden : la copie conservée des cours qui ont produit
        les chiffres figés,
        `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      une fenêtre : un morceau de la période, jugé séparément des autres
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
"""
    ref = golden.get("C5-ETENDU-10", {}).get("jetons_illimites", {})
    if not ref:
        return False, ["    aucun chiffre de reference"]
    # LES DONNEES SONT-ELLES ENCORE CELLES QUI ONT PRODUIT LA REFERENCE ?
    # Defaut trouve le 29/08 : le golden declare le nombre de lignes et
    # l'empreinte du fichier de cours d'epoque, et le juge des stratégies ne lisait NI l'un NI
    # l'autre. Il pouvait donc annoncer « instrument calibre » sur des donnees
    # differentes de celles qui ont produit la reference — mesure : le golden
    # porte 25 111 lignes, les cours d'aujourd'hui en portent 25 117, les six
    # du trou d'octobre repare le 25/08. On ne BLOQUE pas, car ces six lignes
    # sont une correction voulue ; on le DIT, pour qu'aucun ecart de resultat
    # ne soit attribue au calcul alors qu'il vient des donnees.
    prealables = []
    _meta = golden.get("meta", {}) or {}
    if f_cours and _meta.get("nb_lignes_csv"):
        try:
            import hashlib
            _oct = open(f_cours, "rb").read()
            _n = _oct.count(b"\n") + (0 if _oct.endswith(b"\n") else 1)
            _h = hashlib.sha256(_oct).hexdigest()[:16]
            if _n != _meta["nb_lignes_csv"] or _h != _meta.get("hash_donnees_sha256_16"):
                prealables.append(
                    f"    ATTENTION - LES DONNEES ONT CHANGE depuis le golden : "
                    f"{_n} lignes contre {_meta['nb_lignes_csv']}, empreinte "
                    f"{_h} contre {_meta.get('hash_donnees_sha256_16')}. "
                    f"Tout ecart de resultat peut venir des DONNEES, pas du calcul.")
            else:
                prealables.append("    donnees identiques a celles du golden")
        except OSError:
            prealables.append("    donnees du golden non verifiables")
    # LE CALIBRAGE SE FAIT SUR LE PERIMETRE EXACT DU GOLDEN. Sans cette borne,
    # les cours du jour ajoutent des signaux posterieurs a la fenetre de
    # reference et le calibrage echoue a tort — constate le 26/08 : 103
    # operations au lieu de 100, trois signaux nes apres le 10-07-2026.
    fin = (golden.get("meta", {}) or {}).get("periode_fin") or "2026-07-10"
    # LA FICHE DE CALIBRAGE PASSE PAR LA PORTE 0, COMME TOUTES LES AUTRES.
    # Elle etait construite en dur SANS periode, et bornait son perimetre par un
    # autre chemin. L'exigence vivait donc a deux endroits sous deux formes, sans
    # que rien ne garantisse qu'elles disent la meme chose : la structure exacte
    # d'A-308, la regle juste chez celui qui la porte et absente chez le voisin.
    # Le calibrage PROUVE desormais la porte au lieu de la contourner.
    fiche = {"tp": "+4.0%", "sl": "-2.5%", "horizon": "20",
             "univers": ",".join(getattr(mod_signal, "C5E10_UNIVERS", [])),
             "indicateurs": "calibrage",
             # UNE BORNE OUVERTE S'ECRIT AVEC UNE VRAIE DATE. « 0000-00-00 »
             # n'existe pas dans le calendrier, et la porte 0 le refuse depuis
             # qu'elle valide les dates — elle a raison. On prend donc la
             # premiere seance de l'historique, qui est la vraie borne basse.
             "periode": (min(min(b["date"] for b in s) for s in cours.values())
                         + " -> " + fin),
             "_fonction_signal": "signaux_c5etendu10"}
    _ok0, _manq0, _bornes0 = porte_0(fiche)
    if not _ok0:
        return False, ["    la fiche de calibrage elle-meme est refusee a la "
                       "porte 0 : " + ", ".join(_manq0)]
    # LE CALIBRAGE JOUE LA PERIODE QU'IL A DECLAREE, PAS UNE AUTRE.
    # « 0000-00-00 » vivait a DEUX endroits ; un seul a ete corrige, et l'appel
    # gardait la borne en dur. Les deux disaient la meme chose par accident —
    # toute date reelle est superieure a « 0000-00-00 » — mais la periode
    # DECLAREE et la periode JOUEE ne venaient pas du meme endroit, et le
    # calibrage serait passe si elles avaient diverge. C'est le motif que la
    # correction precedente venait d'eliminer entre la porte et le jugement,
    # reste en place a l'etage du dessous. Une seule source, du controle au
    # calcul, dans les deux chemins.
    ops, _ = jouer(fiche, cours, mnemo, mod_signal, mod_positions,
                   periode=_bornes0)
    r = resumer(ops)
    lignes, ok = list(prealables), True
    lignes.append("    perimetre : jusqu'au " + fin + " (borne du golden)")
    # SEUL LE NOMBRE D'OPERATIONS EST EXIGE, et il l'est au signal pres.
    # Le TAUX DE REUSSITE et le NET ne peuvent PAS etre exiges : le golden a
    # ete produit avec la mecanique de sortie theorique, le juge des stratégies emploie la
    # mecanique reelle. Trois operations que le backtest compte perdantes
    # deviennent gagnantes en sortie reelle, la seance ouvrant au-dessus de
    # l'objectif avant que le stop ne soit touche (A-289, A-290).
    # Ce qui est calibre ici, c'est la DETECTION DES SIGNAUX — le seul point
    # ou les deux mecaniques doivent coincider.
    e = abs(r.get("n", 0) - ref.get("n", 0))
    ok = (e == 0)
    lignes.append("    n   : obtenu %s . attendu %s . %s   <- EXIGE"
                  % (r.get("n"), ref.get("n"), "OK" if ok else "ECHEC"))
    lignes.append("    wr  : obtenu %s . golden %s . ecart %+.1f point(s) "
                  "(attendu : mecanique reelle)"
                  % (r.get("wr"), ref.get("wr"), r.get("wr") - ref.get("wr")))
    lignes.append("    net : obtenu {:+,.2f} . golden {:+,.2f} . ecart {:+,.2f} "
                  "(mecanique reelle) — le prix reel aux sauts d'ouverture (A-290) et "
                  "le tarif de frais (0,15 %% par ordre ici, forfait de 300 EUR au golden) ; "
                  "les sorties, elles, se comparent une a une ci-dessous.".replace("%%", "%").format(
                      r.get("net"), ref.get("net"), r.get("net") - ref.get("net")))
    # CHAQUE SORTIE SE COMPARE AU TABLEAU DE REFERENCE, TRADE PAR TRADE (defaut 4 de
    # A-491, 28-09-2026) : la famille (objectif, vente forcee, echeance) et la DATE.
    # C'est ce qui aurait vu le defaut 4 : le juge des stratégies ne testait pas la seance d'achat,
    # et 9 des 100 sorties de reference tombent ce jour-la. Le compte (n) etait juste,
    # les sorties non : 91 dates sur 100 seulement. EXIGE.
    if table:
        _ref = {}
        with open(table, encoding="utf-8-sig", newline="") as _fh:
            for _r in csv.DictReader(_fh, delimiter=";"):
                _ref[(cle_valeur(_r["valeur"]), _r["date_signal"])] = _r
        _fam = lambda m: (m or "").split("_")[0]
        _ecarts = []
        for _o in ops:
            _r = _ref.get((cle_valeur(_o["valeur"]), _o["date_signal"]))
            if _r is None or _fam(_o["motif"]) != _fam(_r["motif"]) or _o.get("date_sortie") != _r["date_sortie"]:
                _ecarts.append("%s %s : juge des stratégies %s %s, reference %s %s" % (
                    _o["valeur"], _o["date_signal"], _o["motif"], _o.get("date_sortie"),
                    _r["motif"] if _r else "-", _r["date_sortie"] if _r else "-"))
        _ok_t = not _ecarts and len(_ref) == len(ops)
        lignes.append("    sorties : %d/%d identiques au tableau de reference (famille et date) . %s"
                      "   <- EXIGE (R-608)" % (len(ops) - len(_ecarts), len(_ref), "OK" if _ok_t else "ECHEC"))
        for _e in _ecarts[:5]:
            lignes.append("      " + _e)
        ok = ok and _ok_t
    return ok, lignes


def main():
    """Déroule le rapport du juge des stratégies, du relevé des fichiers au dernier jugement.

    ① RÔLE — Enchaîner, dans l'ordre et sans que personne n'ait à s'en souvenir,
      les huit gestes qui font le rapport du juge des stratégies : relever les fichiers, alerter
      sur ce qui est ambigu, charger, trier les fiches, refuser les incomplètes,
      prouver que l'instrument retrouve un résultat connu, jouer, juger. C'est le
      seul point d'entrée du programme quand il est lancé à la main.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de
      retour est passée directement à la sortie du processus. Elle n'est jamais
      appelée depuis un autre programme : les trois programmes qui importent le juge des stratégies
      n'en prennent que des fonctions.
    ③ ENTRÉE — Aucun paramètre. Tout arrive par la ligne de commande : le premier
      argument est le dossier racine, `/mnt/project` s'il est absent ; le second est
      l'identifiant d'une seule fiche à juger, toutes les fiches recevables étant
      jouées s'il est absent.
    ④ CONDITIONS D'ENTRÉE — Quatre fichiers doivent exister sous la racine : le
      registre des stratégies, les cours, le module de signal et le module de
      positions. Les cours sont ceux du fichier maître, `donnees/cours_maitre.csv` :
      s'il manque, le juge des stratégies s'arrête (A-442). Le référentiel des valeurs, le golden,
      le module de jugement et le module de statistiques peuvent manquer ; le
      rapport est alors plus pauvre, et il le dit pour le module de jugement.
    ⑤ SORTIE — UNE valeur : un entier passé à la sortie du processus. 0 quand le
      rapport est allé au bout, et 0 aussi quand aucune fiche n'était recevable,
      ce qui n'est pas un échec mais la porte 0 qui fait son travail. 1 quand un
      fichier indispensable manque, et 1 quand le calibrage échoue.
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher la version et l'heure de Paris · ② relever les sept
      fichiers par leur nom réel · ③ alerter si l'un des quatre noms surveillés
      répond sous plusieurs graphies · ④ afficher chaque fichier avec son empreinte
      · ⑤ désigner le fichier maître des cours par `fichiers_de_cours`, et
      s'arrêter s'il manque · ⑥ s'arrêter si un fichier indispensable manque · ⑦ charger les cours,
      la table des mnémoniques et les quatre modules · ⑧ lire le registre des
      stratégies et n'y garder que les lignes à l'état LABO ou QA · ⑨ passer chaque
      fiche restante par la porte 0 et afficher le verdict ligne à ligne ·
      ⑩ calibrer l'instrument sur le témoin du golden si son empreinte est conforme,
      sur le fichier vivant sinon, et s'arrêter si le calibrage échoue · ⑪ pour
      chaque fiche recevable, afficher ses réglages, la jouer, la résumer, compter
      ses sorties sur saut, puis appeler le jugement · ⑫ rappeler que le juge des stratégies ne
      conclut pas.
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
    ⑦ UNITÉ — Les fiches se comptent en LIGNES DE REGISTRE. Les opérations se
      comptent à l'unité. Les gains sont en EUROS. Les empreintes sont des nombres
      hexadécimaux de 16 caractères. L'heure affichée est celle de Paris.
    ⑧ POURQUOI — ON NE JUGE QUE CE QUI EST EN COURS DE ROUTE. Seules les lignes à
      l'état LABO — à l'étude, elle peut être mesurée — et QA — à l'épreuve du
      vivant, son compteur avance — passent devant le juge des stratégies. Une ligne close l'est, et une
      ligne en production se juge par sa vie et non par le juge des stratégies. Les états employés
      sont ceux que le BACKLOG a fixés le 13-08-2026 sous l'action A-194 : LABO, QA,
      PRODUCTION, SUSPENDUE, et les deux conventions historiques JAMAIS_VECUE et
      VECUE-PUIS-ARCHIVEE. Le Chat en avait inventé cinq autres le 29-08-2026 et les
      avait écrits par-dessus les officiels ; l'arbitrage de Jean-Luc du 30-08-2026
      a gardé les officiels.
      LE JUGE DES STRATÉGIES LIT LE REGISTRE DES STRATÉGIES ET PLUS LE SAS. Le sas,
      `registre_candidates.csv`, a été absorbé le 29-08-2026 : il dupliquait sept
      colonnes du registre sous d'autres identifiants, sans qu'aucune colonne ne
      relie les deux fichiers. Le lien se reconstruisait par ressemblance de noms,
      ce que la règle d'identité des valeurs interdit, et ce qui a coûté 26 % d'une
      mesure le 23-08-2026. Un objet, un nom, un registre, de la naissance à la
      mort.
      L'ABSENCE DES COURS DU JOUR EST UNE ALERTE, PAS UNE MENTION. Elle change le
      nombre d'opérations mesurées, donc le résultat : sans elle, deux lancements du
      même juge des stratégies rendraient des chiffres différents sans que rien ne l'annonce.
      UN NOM QUI RÉPOND DEUX FOIS EST UNE ALERTE, JAMAIS UN CHOIX SILENCIEUX.
      Mesure du 29-08-2026 : le registre des candidates existait deux fois au
      projet, l'un à jour et l'autre périmé du 23-08-2026 où tous les champs
      valaient « à renseigner ». Le juge des stratégies prenait le bon, mais par coïncidence de
      nommage.
      LES BORNES VIENNENT DE LA PORTE, QUI LES A DÉJÀ VALIDÉES. L'ancienne branche
      « aucune période déclarée » est devenue du code mort le jour où la période est
      passée obligatoire, et un garde-fou mort est pire qu'absent : il fait croire
      qu'une protection existe alors qu'elle a déménagé. La fonction lève désormais
      si une fiche passée arrive sans bornes.
    ⑨ CE QUI CLOCHE —
      ① UNE SEULE FICHE MAL REMPLIE ARRÊTE TOUT LE RAPPORT. `porte_0` rend deux
      valeurs sur une période mal formée et trois partout ailleurs, et le
      dépaquetage écrit ici en attend trois. Mesuré de bout en bout le 20-09-2026 en
      ajoutant au registre d'une copie une fiche `ZZ-TEST` de période « du 2 janvier
      au 10 juillet » : le juge des stratégies affiche les 36 premières fiches, puis s'arrête sur
      « ValueError: not enough values to unpack (expected 3, got 2) », ligne 831,
      code de sortie 1. Les trois fiches recevables n'ont pas été jugées.
      ② **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** LE JUGE DES STRATÉGIES N'EMPLOIE PAS SA PROPRE FONCTION DE CHOIX DES COURS. Les cours sont
      cherchés ici par leur nom, `cac40_ohlcv.csv` et `claude_cours_nouveaux.csv`,
      alors que `fichiers_de_cours` désigne `donnees/cours_maitre.csv` et que trois
      autres programmes le lui demandent. Mesuré le 20-09-2026 : le rapport affiche
      « cours cac40_ohlcv.csv », et le fichier maître existe. Le périmètre est le
      même aujourd'hui, 40 valeurs et 694 dates du 2024-01-02 au 2026-09-18 des deux
      côtés, l'historique figé s'arrêtant au 2026-07-10 et le fichier du jour
      reprenant au 2026-07-13 sans un jour de recouvrement. Le jour où ce
      raccordement laissera un trou, le juge des stratégies jugera sur un historique amputé pendant
      que les programmes du soir liront le maître complet.
      ③ LE COMMENTAIRE QUI JUSTIFIE LE TRI DES FICHES COMPTE FAUX. Il annonce, au
      30-08-2026, « 68 lignes dont 30 VECUE-PUIS-ARCHIVEE, 1 JAMAIS_VECUE et
      1 PRODUCTION ». Mesuré le 20-09-2026 sur le fichier réel : 35 LABO,
      30 VECUE-PUIS-ARCHIVEE, 2 QA, 1 JAMAIS_VECUE, et AUCUNE ligne en PRODUCTION.
      Le commentaire se corrigeait déjà lui-même d'une erreur de vocabulaire ; il en
      porte maintenant une de comptage.
      ④ L'ABSENCE DU MODULE DE STATISTIQUES N'EST PAS ANNONCÉE, CELLE DU MODULE DE
      JUGEMENT L'EST. Mesuré le 20-09-2026 en passant ce module à `None` : le
      rapport perd le voisinage des réglages et le pire creux, remplacés par deux
      lignes « non mesure : 'NoneType' object has no attribute … » au milieu de
      quinze autres, sans alerte en tête.
      ⑤ QUATRE NOMS SONT SURVEILLÉS CONTRE LES GRAPHIES MULTIPLES, DIX SONT
      CHERCHÉS. La boucle d'alerte porte sur le registre des stratégies, les cours,
      le module de signal et le module de positions. Le golden, son témoin, le
      référentiel des valeurs, les cours du jour, le module de jugement et le module
      de statistiques ne sont pas surveillés : un doublon sur l'un d'eux serait
      tranché en silence.
      ⑥ LE CALCUL D'EMPREINTE DU TÉMOIN EST REFAIT À LA MAIN. La fonction
      `empreinte` existe dans ce même fichier et fait exactement cela ; ce passage
      réimporte la bibliothèque et recalcule. Relevé le 20-09-2026 :
      `hexdigest()[:16]` apparaît 3 fois, l'appel `empreinte(` 2 fois.
      ⑦ LE NOM DE LA FONCTION DE SIGNAL EST ÉCRIT ICI EN CLAIR, `signaux_c5etendu10`,
      et une seconde fois dans `calibrer`. Le registre des stratégies ne porte pas
      cette colonne : le nom ne peut donc pas venir de la fiche, et il est décidé
      dans le code, à deux endroits.
      ⑧ LE GOLDEN EST LU SANS PROTECTION. Le fichier est ouvert et décodé
      directement ; un fichier tronqué ou mal formé arrêterait le programme sur une
      erreur brute, alors que tout le reste de cette fonction traite l'absence d'un
      fichier comme une situation prévue.
    ⑩ EFFET — N'ÉCRIT AUCUN FICHIER et ne touche pas au réseau : `git status` reste
      vide après un passage complet sur une copie du dépôt, mesuré le 20-09-2026.
      Elle LIT sept fichiers, EXÉCUTE le code de quatre modules Python chargés
      depuis le disque, et AFFICHE le rapport : 167 lignes mesurées le 20-09-2026
      sur un passage complet.
    ⑪ TERMINAISON — Rend la main avec 0 ou 1 dans le cas normal. PEUT LEVER des
      erreurs non rattrapées qui arrêtent alors le programme : sur une fiche dont la
      période est mal formée, mesuré le 20-09-2026 ; sur une fiche passée qui
      arriverait sans bornes, ce que le code signale lui-même ; sur un fichier
      indispensable illisible ; et sur un golden mal formé. Et un de ses appels peut
      ne pas revenir : `charger_module` exécute le contenu des fichiers qu'il
      charge, et `jouer` comme `juger` appellent du code tiers dont le temps n'est
      pas borné.
      [sort: non]
    ⑫ DÉFINITIONS
      l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de
        référence qui n'est jamais réécrit
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte
        acceptée, son horizon et son univers
      la porte 0 : le contrôle qui refuse une fiche incomplète avant tout calcul,
        sans consommer d'essai.
      la racine : le dossier reçu sur la ligne de commande, celui dont on
        classe les fichiers — en général un clone du dépôt.
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et
        des actions du projet, où chaque ligne porte un identifiant en `A-`
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une
        stratégie sur l'historique des cours et rend la liste de ses
        opérations
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige
        de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet
        n'en étant qu'une copie de lecture
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
        l'historique des cours et n'est jamais réécrit.
      le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les
        mesures disant si un gain veut dire quelque chose.
      le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du
        taux de frais et des règles de sortie d'une position.
      le module de signal : le programme qui décide quelles valeurs acheter
      le module de statistiques : le programme qui porte le voisinage des
        réglages et le pire creux,
        `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte
        les règles numérotées du projet
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste
        des valeurs à suivre, avec pour chacune son mnémonique et sa place
        de cotation.
      le témoin du golden : la copie conservée des cours qui ont produit
        les chiffres figés,
        `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour
        TotalEnergies ; c'est la clé d'identité des valeurs, jamais leur nom.
      un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte
        que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
    """
    base = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project"
    cible = sys.argv[2] if len(sys.argv) > 2 else None
    print("JUGE DES STRATÉGIES . %s . %s\n" % (VERSION, horodatage()))

    # LE JUGE DES STRATÉGIES LIT LE REGISTRE DES STRATEGIES, PLUS LE SAS.
    # Le sas — registre_candidates.csv — a ete ABSORBE le 29-08-2026 : il
    # dupliquait sept colonnes du registre (id, nom, indicateurs, univers,
    # filtres, tp, sl, horizon) sous d'autres identifiants, sans qu'aucune
    # colonne ne relie les deux fichiers. Le lien se reconstruisait par
    # RESSEMBLANCE DE NOMS — exactement ce que le chapitre IDENTITE DES VALEURS
    # interdit, et qui a coute 26 % d'une mesure le 23/08.
    # Un objet, un nom, un registre, de la naissance a la mort.
    f_sas = trouver(base, "cac40_strategies.csv")
    # LES COURS VIENNENT DU SEUL FICHIER MAITRE, designe par `fichiers_de_cours` :
    # une seule facon de le trouver dans tout le systeme (A-442, R-708).
    try:
        f_cours = fichiers_de_cours(base)[0]
    except FileNotFoundError as _e:
        print(_e)
        return 1
    f_ref = trouver(base, "REFERENTIEL_VALEURS")
    f_sig = trouver(base, "MODULE_C5_ETENDU_10")
    f_pos = trouver(base, "MODULE_POSITIONS.py")
    f_gold = trouver(base, "golden_tests_")

    # UN NOM QUI REPOND DEUX FOIS EST UNE ALERTE, jamais un choix silencieux.
    for _lib, _mot in (("le registre des strategies", "cac40_strategies.csv"),
                       ("les cours", "cours_maitre.csv"),
                       ("le module de signal", "MODULE_C5_ETENDU_10"),
                       ("le module de positions", "MODULE_POSITIONS.py")):
        _tous = trouver_tous(base, _mot)
        if len(_tous) > 1:
            print("ALERTE - %s REPOND SOUS %d GRAPHIES :" % (_lib, len(_tous)))
            for _p in _tous:
                print("    %s" % os.path.relpath(_p, base))
            print("  Le juge des stratégies en prendra UN, et rien ne garantit que ce soit le")
            print("  bon : il essaie le motif tel qu'il est ecrit avant les")
            print("  autres graphies. Tranchez avant de juger quoi que ce soit.\n")

    print("FICHIERS RELEVES - noms reels, jamais supposes (R-719) :")
    for lib, ch in (("registre des strategies", f_sas), ("cours", f_cours),
                    ("referentiel", f_ref),
                    ("module de signal", f_sig), ("module de positions", f_pos),
                    ("chiffres figes", f_gold)):
        if ch:
            print("  %-22s %-46s %s" % (lib, os.path.basename(ch), empreinte(ch)))
        else:
            print("  %-22s INTROUVABLE" % lib)
    print()

    manquants = [l for l, c in (("registre des strategies", f_sas), ("cours", f_cours),
                                ("module de signal", f_sig),
                                ("module de positions", f_pos)) if not c]
    if manquants:
        print("ARRET : introuvable - %s. Rien n'est produit." % ", ".join(manquants))
        return 1

    cours = charger_cours(f_cours)
    mnemo = table_mnemoniques(f_ref)
    mod_sig = charger_module(f_sig, "sig")
    mod_pos = charger_module(f_pos, "pos")
    f_jug = trouver(base, "MODULE_JUGEMENT.py")
    f_sta = trouver(base, "MODULE_STATISTIQUES")
    mod_jug = charger_module(f_jug, "jug") if f_jug else None
    mod_stats = charger_module(f_sta, "sta") if f_sta else None
    if not mod_jug:
        print("ALERTE - LE MODULE DE JUGEMENT EST INTROUVABLE.")
        print("  Le juge des stratégies rendra les gains, mais PAS les mesures qui disent si")
        print("  ces gains veulent dire quelque chose. Ce n'est pas un jugement.\n")
    seances = {b["date"] for s in cours.values() for b in s}
    fiches = list(csv.DictReader(open(f_sas, encoding="utf-8-sig")))
    print("DONNEES : %d valeurs . %d mnemoniques . %d fiches au registre\n"
          % (len(cours), len(mnemo), len(fiches)))

    print("PORTE 0 - une fiche incomplete est refusee AVANT tout calcul :")
    # ON NE JUGE QUE CE QUI EST EN COURS DE ROUTE. Au 30-08-2026 le registre
    # porte 68 lignes dont 30 VECUE-PUIS-ARCHIVEE, 1 JAMAIS_VECUE et
    # 1 PRODUCTION : les rejouer n'aurait aucun sens, et elles noieraient le
    # rapport. Une ligne close l'est (R-727), et une ligne en PRODUCTION se juge
    # par sa vie, pas par le juge des stratégies.
    # CE COMMENTAIRE A ETE CORRIGE LE 30/08 : il parlait encore le vocabulaire
    # invente la veille — « 31 ABANDONNEES et 1 VIVANTE » — alors que le code
    # filtrait deja sur A-194. La correction etait juste dans le code et fausse
    # dans son explication : un lecteur qui suit le commentaire recompte faux.
    # C'est A-308 entre un programme et sa propre documentation.
    # LES ETATS SONT CEUX D'A-194, DECIDES LE 13-08-2026. PAS D'AUTRES.
    # Le Chat en avait invente cinq le 29/08 en absorbant le sas — IDEE,
    # MESUREE, EN EPREUVE, VIVANTE, ABANDONNEE — et les avait ecrits par-dessus
    # les officiels SANS OUVRIR A-194. Le radar l'a denonce des le lendemain :
    # « etats de vie hors nomenclature ». Arbitrage de Jean-Luc le 30/08 : on
    # garde les officiels. Un vocabulaire decide ne se remplace pas sans etre
    # tranche explicitement — c'est ainsi que naissent les divergences.
    #   LABO      = a l'etude, elle peut etre mesuree
    #   QA        = a l'epreuve du vivant, son compteur avance
    #   PRODUCTION = jouable en vrai
    #   SUSPENDUE = alerte, en attente de diagnostic
    #   JAMAIS_VECUE et VECUE-PUIS-ARCHIVEE = conventions historiques, closes
    ETATS_JUGEABLES = ("LABO", "QA")
    n_total = len(fiches)
    hors = [f for f in fiches
            if (f.get("etat_vie") or "").strip().upper() not in ETATS_JUGEABLES]
    fiches = [f for f in fiches
              if (f.get("etat_vie") or "").strip().upper() in ETATS_JUGEABLES]
    if hors:
        from collections import Counter as _C
        _d = _C((f.get("etat_vie") or "?").strip().upper() for f in hors)
        print("  %d ligne(s) sur %d ecartees, ce n'est pas un refus : %s"
              % (len(hors), n_total,
                 " . ".join("%d %s" % (v, k) for k, v in _d.most_common())))

    passees = []
    for f in fiches:
        ok, manq, _b0 = porte_0(f)
        if ok:
            f["_bornes"] = _b0
            passees.append(f)
            print("  %-9s PASSE   %s" % (f["id"], f["nom"][:44]))
        else:
            print("  %-9s refusee %-34s manque : %s"
                  % (f["id"], f["nom"][:34], ", ".join(manq)))
    print("\n  %d fiche(s) sur %d peuvent passer devant le juge des stratégies.\n" % (len(passees), len(fiches)))
    if not passees:
        print("Aucune fiche testable. Ce n'est pas un echec : c'est la porte 0")
        print("qui fait son travail (A-281).")
        return 0

    if f_gold:
        golden = json.load(open(f_gold, encoding="utf-8"))
        # LES CHIFFRES FIGES SE REJOUENT SUR LES DONNEES DE LEUR PRISE, JAMAIS
        # SUR CELLES D AUJOURD HUI. Cowork, 13-09 : le jeu du golden a ete
        # retrouve et depose en temoin. Cinq lignes le separaient du vivant,
        # toutes des AJOUTS du 29-10-2024 — zero modification, zero suppression.
        # LE TEMOIN N EST EMPLOYE QUE S IL EST LE BON : son empreinte doit valoir
        # celle que le golden DECLARE. Sinon on ne calibre pas sur un a-peu-pres,
        # on le dit et on garde le fichier vivant.
        _f_tem = trouver(base, "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN")
        _cours_cal, _f_cal = cours, f_cours
        if _f_tem:
            import hashlib as _h
            _emp = _h.sha256(open(_f_tem, "rb").read()).hexdigest()[:16]
            _att = str((golden.get("meta", {}) or {}).get("hash_donnees_sha256_16", ""))
            if _att and _emp == _att:
                _cours_cal = charger_cours(_f_tem)
                _f_cal = _f_tem
                print("  calibrage sur le TEMOIN du golden : %s (%s)"
                      % (os.path.basename(_f_tem), _emp))
            else:
                print("  TEMOIN PRESENT MAIS NON CONFORME : empreinte %s, le golden"
                      " en declare %s — calibrage sur le fichier vivant." % (_emp, _att or "aucune"))
        else:
            print("  aucun temoin du golden : calibrage sur le fichier VIVANT,"
                  " tout ecart peut venir des donnees.")
        # le tableau de reference des 100 trades ne se compare qu'aux cours de SA prise
        _f_tab = trouver(base, "TABLEAU_100_TRADES_C5E10") if _f_cal == _f_tem else None
        if _f_cal == _f_tem and not _f_tab:
            print("  ARRET : le tableau de reference des 100 trades est introuvable — "
                  "les sorties ne peuvent pas etre comparees.")
            return 1
        ok, lignes = calibrer(_cours_cal, mnemo, mod_sig, mod_pos, golden, _f_cal, _f_tab)
        print("CALIBRAGE DE L'INSTRUMENT (9bis) - rejoue C5-ETENDU-10 :")
        for l in lignes:
            print(l)
        if not ok:
            print("\n  ARRET TOTAL : l'instrument n'est pas calibre, rien n'est juge.")
            return 1
        print("  -> OK, l'instrument est calibre.\n")

    for f in passees:
        if cible and f["id"] != cible:
            continue
        f.setdefault("_fonction_signal", "signaux_c5etendu10")
        print("=== %s . %s" % (f["id"], f["nom"]))
        print("    %s" % f["indicateurs"][:88])
        print("    TP %s . SL %s . horizon %s seances" % (f["tp"], f["sl"], f["horizon"]))
        # LA PERIODE DE LA FICHE FAIT FOI. Sans elle, le juge des stratégies juge sur TOUT
        # l'historique disponible et rend des chiffres non comparables a ceux
        # de la porte 1 : 77 operations a 51,9 % contre 56 a 58,9 % annoncees.
        # Un jugement sans periode declaree n'est pas reproductible.
        # LES BORNES VIENNENT DE LA PORTE, QUI LES A DEJA VALIDEES. L'ancienne
        # branche « AUCUNE PERIODE declaree » est devenue du CODE MORT le jour
        # ou la periode est passee obligatoire. Un garde-fou mort est pire
        # qu'absent : il fait croire qu'une protection existe alors qu'elle a
        # demenage.
        _bornes = f.get("_bornes")
        if not _bornes:
            raise RuntimeError("fiche sans bornes apres la porte 0 : la porte "
                               "et le jugement ne lisent plus la meme chose")
        print("    periode de la fiche : %s -> %s" % _bornes)
        ops, inconnus = jouer(f, cours, mnemo, mod_sig, mod_pos, periode=_bornes)
        if inconnus:
            print("    ALERTE - valeurs demandees et absentes des cours : %s" % inconnus)
        r = resumer(ops)
        if r["n"] == 0:
            print("    aucune operation produite.\n")
            continue
        print("    {} operations . {} % de reussite . {:+,.2f} EUR".format(
              r["n"], r["wr"], r["net"]))
        print("    motifs : %s" % r["motifs"])
        gaps = [o for o in ops if o["motif"].endswith("_GAP")]
        if gaps:
            print("    dont %d sorties sur GAP (%.0f %%) - glissement mesure, A-290"
                  % (len(gaps), 100.0 * len(gaps) / r["n"]))

        # ── LE JUGEMENT ────────────────────────────────────────────────
        # Le juge des stratégies n'implemente AUCUNE de ces mesures : il APPELLE.
        # Sans ce branchement, tout ce qui a ete mesure le 28/08 ne vivait
        # que dans des scripts jetables — donc nulle part.
        if mod_jug:
            juger(f, ops, cours, seances, mod_jug, mod_stats, mod_pos, mnemo,
                  _bornes, (mod_sig,))
        print()

    print("Pas de verdict oui / non : la grille qui le rendra (A-210) n'est pas encore figée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
