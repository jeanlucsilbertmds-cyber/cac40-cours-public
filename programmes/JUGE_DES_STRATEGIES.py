#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCIDÉ · outil · v1.6 · 30-10-2026 · Rôle : juger une strategie a partir de sa fiche.
UN SEUL NUMERO DE VERSION DANS CE FICHIER : ce cartouche et la constante
VERSION plus bas disent la meme chose. Le rapport imprime celui du code, un
lecteur voit celui-ci — deux numeros differents dans le meme fichier etaient
exactement le defaut que la v1.5 corrigeait.

VERSION 1.6 — 30-10-2026. CHAQUE FICHE NOMME SON SIGNAL (A-542 ① ②). Le juge
    imposait le signal de la famille C5-ETENDU-10 a toute fiche ; il joue
    desormais la fonction que la fiche nomme dans `module_signal`,
    `fonction_signal` et `reglages_signal`, lues par `signal_de_la_fiche`
    seule. Une fiche sans signal nomme est refusee a la porte 0.

VERSION 1.5 — 29-08-2026. Le juge des stratégies lit le REGISTRE DES STRATEGIES et non
    plus le sas, qui est absorbe. Les TROIS FENETRES sont rendues. La
    PERIODE devient le sixieme champ obligatoire de la porte 0, et la
    fiche de calibrage y passe elle aussi. Le numero de version bouge
    quand le fond bouge : deux rapports de contenus differents ne doivent
    jamais porter le meme numero.

VERSION 1.2 — LE JUGEMENT EST BRANCHE. Le juge des stratégies rendait les gains ; il rend
    desormais les mesures qui disent si ces gains veulent dire quelque chose :
    point mort, observations independantes (mesurees depuis le 05-11-2026, n°106 ;
    avant : episodes a 5 seances), coupure sur le TEMPS avec embargo de
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
  copie du dépôt. EXCEPTION depuis la mission REGARD (12-11-2026) : quand une séance jouée tombe dans la fenêtre du
  regard unique, `jouer` lit la branche des regards au dépôt distant (`fetch`, par TENIR_LE_REGISTRE_DES_ESSAIS) pour
  vérifier le reçu ; `k_a_la_date` lance git par le lanceur unique du même programme. Il LIT sept fichiers et EXÉCUTE le code de quatre modules
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
    barème des frais et des règles de sortie d'une position.
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

import ast
import csv
import hashlib
import importlib.util
import json
import math
import numbers
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from COMMUN import lire_horizon       # la seule lecture d'un horizon (R-708, défaut 4 de A-491)
# la lecture qui accepte « aucune » (contrat du lot 0, 09-11-2026) : porte_0, lecture_de_jeu, jouer, juger depuis le
# 11-11-2026 (plan V7, bloc 4) — une stratégie sans durée maximale se juge
from COMMUN import lire_horizon_ou_aucune, HORIZON_AUCUNE
# le stop « sans stop » (contrat du 11-11-2026, mission VENTE ; A-541) : porte_0, lecture_de_jeu, jouer l'acceptent par
# `seuil_de_la_fiche_ou_aucun` ; `seuil_de_la_fiche` (donc le soir et le juge à 8 critères) le refuse toujours
from COMMUN import STOP_AUCUN, est_le_mot_du_stop_aucun
from COMMUN import MOTIF_FIN_DES_DONNEES   # positions encore ouvertes à la fin des données (décision du 12-11-2026, 09h18)
from COMMUN import lire_csv   # le réglage du soir (`soir_accepte_aucune`, 12-11-2026)

VERSION = "generique-1.6"
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
        barème des frais et des règles de sortie d'une position.
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
    ② CONTEXTE D'APPEL — `main`, trois fois, juste après le relevé des fichiers
      et avant leur affichage, sur trois motifs : `cac40_strategies.csv`,
      `cours_maitre.csv` et `MODULE_POSITIONS.py` (le motif `MODULE_C5_ETENDU_10`
      en est sorti le 30-10-2026, A-542 : chaque fiche nomme son module par son
      chemin exact). Jamais appelée ailleurs.
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
        barème des frais et des règles de sortie d'une position.
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
      cours, les cours du jour, le référentiel des valeurs, le
      module de positions (le module de signal n'y est plus depuis le 30-10-2026,
      A-542 : chaque fiche le nomme par son chemin exact), le golden, le module de jugement, le module de
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
        barème des frais et des règles de sortie d'une position.
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
    ② CONTEXTE D'APPEL — Cinq appelants, relevés le 31-10-2026 par recherche de
      « charger_module( » dans programmes/.
      · `main`, trois fois : le module de
      positions sous `pos`, le module de jugement sous `jug` et le module de
      statistiques sous `sta`.
      · `signal_de_la_fiche` (depuis le 30-10-2026, A-542), une fois par chemin de
      module de signal nommé par une fiche, sous un nom tiré de ce chemin.
      · `lire_par_le_lecteur`, pour `programmes/LIRE_LES_COURS.py`.
      · `main` de `programmes/JOUER_LES_VERSIONS.py`, pour le module de positions.
      · `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` ligne 192, qui charge le module
      C5 par son chemin écrit en dur. Ce programme tourne chaque soir, lancé par
      `.github/workflows/collecte_abc.yml`.
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
      procuration. Rien dans la fonction ne le limite. Pour le module de signal
      nommé par une fiche, la porte filtre AVANT : `signal_de_la_fiche` n'appelle
      cette fonction que sur un fichier qui se déclare module de signal, lu sans
      exécution (`declaration_de_signal`, depuis le 31-10-2026).
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
        barème des frais et des règles de sortie d'une position.
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


# ── LE SIGNAL QUE LA FICHE NOMME (A-542 ① ②, plan du circuit validé par Jean-Luc le 30-10-2026) ─────────────────
# Jusqu'au 30-10-2026, le juge, la moulinette (JOUER_LES_VERSIONS) et le juge à 8 critères imposaient le signal de la
# famille C5-ETENDU-10 à N'IMPORTE QUELLE fiche : le module était cherché par le motif « MODULE_C5_ETENDU_10 » et la
# fonction posée par défaut, `setdefault("_fonction_signal", "signaux_c5etendu10")`, à quatre endroits. Une fiche
# RSI ou MA200 aurait donc été jugée sur le signal C5 sans un mot. Désormais CHAQUE FICHE NOMME SON SIGNAL dans trois
# colonnes du registre des stratégies, et UNE SEULE fonction les lit, `signal_de_la_fiche`, appelée par les trois
# programmes (deux implémentations d'une même chose divergent toujours, R-708). Ajouter une famille = écrire son
# module et sa fiche ; aucun autre fichier ne change.
#   module_signal   : le chemin du module, RELATIF À LA RACINE, exact (ex. programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py)
#   fonction_signal : le nom de la fonction de ce module qui rend les séances d'achat (ex. signaux_c5etendu10)
#   reglages_signal : vide, ou un objet JSON passé à la fonction en arguments nommés (ex. {"periode": 2, "seuil": 10})
COLONNES_DU_SIGNAL = ("module_signal", "fonction_signal", "reglages_signal")

# Les modules de signal déjà chargés, par chemin réel : la moulinette joue des milliers de versions d'une même fiche,
# et recharger le module à chaque version referait tourner tout son code de chargement.
_MODULES_DE_SIGNAL = {}


class SignalNomme:
    """Le signal d'une fiche, prêt à jouer : la fonction nommée par la fiche, avec ses réglages.

    ① RÔLE — Porter, en un seul objet, ce que la fiche a nommé : la fonction qui rend les séances d'achat, ses
      réglages, le module d'où elle vient et la déclaration lue. `jouer` n'accepte que cet objet : un module passé à
      sa place, ou une fonction prise ailleurs, est refusé.
    ② CONTEXTE D'APPEL — Construit par `signal_de_la_fiche`, et par les épreuves qui fabriquent un signal (tests/).
      Appelé par `jouer`, une fois par morceau de série de chaque valeur de l'univers.
    ③ ENTRÉE — `fonction` : la fonction de signal · `reglages` : un dictionnaire d'arguments nommés, vide si aucun ·
      `declaration` : le texte qui dit d'où vient le signal, affiché par le juge · `module` : le module chargé, ou None ·
      `chemin` : le chemin du module tel que la fiche l'écrit, relatif à la racine, ou None.
    ④ CONDITIONS D'ENTRÉE — `fonction` est appelable ; `reglages` est un dictionnaire.
    ⑤ SORTIE — L'appel rend UNE valeur : ce que rend la fonction nommée, la liste des {"i": rang} des séances
      signalées. [rend: 1]
    ⑥ TRAITEMENT — Appeler `fonction(serie, **reglages)`.
    ⑦ UNITÉ — Le rang `i` est un indice dans la série passée.
    ⑧ POURQUOI — Un objet à part, et non la fonction nue, pour que `jouer` puisse REFUSER ce qui n'est pas passé par
      la lecture de la fiche (A-542 : plus aucun repli silencieux), et pour que le juge puisse AFFICHER quel signal il
      joue.
    ⑨ CE QUI CLOCHE — Une épreuve peut construire cet objet à la main avec n'importe quelle fonction : le refus de
      `jouer` protège les programmes, pas une main qui contournerait exprès la fiche.
    ⑩ EFFET — Ce que fait la fonction nommée ; aucun par lui-même.
    ⑪ TERMINAISON — Rend la main, sauf si la fonction nommée ne revient pas : c'est du code de module, dont rien ne
      borne le temps. [sort: non]
    """

    def __init__(self, fonction, reglages, declaration, module=None, chemin=None):
        """Range la fonction, ses réglages et leur provenance.

        ① RÔLE — Construire le signal, en refusant ce qui ne pourrait pas jouer.
        ② CONTEXTE D'APPEL — `signal_de_la_fiche` ; les épreuves qui fabriquent un signal.
        ③ ENTRÉE — `self` : l'objet construit · `fonction`, `reglages`, `declaration`, `module`, `chemin` : voir ③ de la
          classe.
        ④ CONDITIONS D'ENTRÉE — `fonction` appelable ; `reglages` dictionnaire.
        ⑤ SORTIE — Aucune valeur (constructeur).
          [rend: rien]
        ⑥ TRAITEMENT — ① refuser une fonction non appelable ou des réglages qui ne sont pas un dictionnaire ·
          ② ranger les cinq attributs, les réglages copiés.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Les réglages sont copiés : la fiche qui les a fournis peut changer ensuite sans changer le signal.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun hors de l'objet.
        ⑪ TERMINAISON — Rend la main, ou lève TypeError.
          [sort: non]
        """
        if not callable(fonction):
            raise TypeError("SignalNomme : la fonction de signal n'est pas appelable (%r)" % (fonction,))
        if not isinstance(reglages, dict):
            raise TypeError("SignalNomme : les reglages doivent etre un dictionnaire (%r)" % (reglages,))
        self.fonction, self.reglages, self.declaration, self.module = fonction, dict(reglages), declaration, module
        self.chemin = chemin

    def __call__(self, serie):
        """Rend les séances d'achat de la série, après avoir contrôlé la FORME de la sortie.

        ① RÔLE — Appliquer le signal à une série, et refuser — avant que `jouer` ne s'en serve — une sortie mal
          formée (point 8 du plan du juge, 31-10-2026).
        ② CONTEXTE D'APPEL — `jouer`, une fois par morceau de série de chaque valeur (donc pour le juge, son
          calibrage, son voisinage, la moulinette et le juge à 8 critères) ; l'épreuve d'arrivée des signaux
          (`tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py`), sur des séries coupées.
        ③ ENTRÉE — `self` : le signal (fonction et réglages) · `serie` : les séances d'UNE valeur, triées par date.
        ④ CONDITIONS D'ENTRÉE — Celles de la fonction nommée.
        ⑤ SORTIE — UNE valeur : la liste des {"i": rang} rendue par la fonction nommée, inchangée.
          [rend: 1]
        ⑥ TRAITEMENT — ① appeler la fonction (`_appeler`) · ② refuser une sortie mal formée (`forme_du_signal`) ·
          ③ rendre la sortie.
        ⑦ UNITÉ — Rangs dans `serie`.
        ⑧ POURQUOI — `jouer` prend `s[i]` sans rien vérifier : un rang négatif achète à une autre date, en silence
          (audit du code, D2). Le contrôle de la forme vit ICI parce que tout signal joué passe par cet objet (A-542) :
          un seul endroit pour les trois programmes, et son coût suit le nombre de signaux.
          LE CONTRÔLE « LE SIGNAL NE VOIT PAS L'AVENIR » N'EST PLUS ICI (décision de Jean-Luc du 31-10-2026 à 21h15,
          ses mots : « Ok, je ne comprends pas très bien, mais je te fais confiance. Donc fais le 1 »). Il tournait à
          chaque jugement : réduit pour rester léger à 5 + 5 dates tirées par série, il ne prouvait presque rien (une
          fuite rare passait, relecteur de la version B) et il faisait passer l'épreuve du juge par le lecteur de
          593 s à 977 s sur une machine seule. Il se fait désormais UNE FOIS par signal, sur TOUTES les dates d'une
          fenêtre fixe, hors du juge : `tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py`.
        ⑨ CE QUI CLOCHE — ① Le juge ne contrôle pas l'avenir : un module ajouté puis jugé avant la prochaine
          vérification de version n'a pas été éprouvé (BACKLOG : un visa par empreinte du module). ② La sortie n'est
          pas recopiée : la fonction pourrait la modifier ensuite (aucune ne le fait).
        ⑩ EFFET — Celui de la fonction nommée ; aucun par lui-même.
        ⑪ TERMINAISON — Rend la main ; lève `SignalRefuse` (motif nommé) ; un appel de la fonction nommée peut ne
          pas revenir : du code de module, non borné.
          [sort: non]
        """
        resultat = self._appeler(serie)
        motif = forme_du_signal(resultat, len(serie))
        if motif:
            raise SignalRefuse("NON JUGEABLE — la sortie du signal %s est mal formée : %s" % (self.declaration, motif))
        return resultat

    def _appeler(self, serie):
        """Appelle la fonction nommée avec les réglages de la fiche, sans contrôle.

        ① RÔLE — Le seul appel de la fonction de signal.
        ② CONTEXTE D'APPEL — `__call__`.
        ③ ENTRÉE — `self` : le signal (fonction et réglages) · `serie` : des séances triées par date.
        ④ CONDITIONS D'ENTRÉE — Celles de la fonction nommée.
        ⑤ SORTIE — UNE valeur : ce que rend la fonction nommée.
          [rend: 1]
        ⑥ TRAITEMENT — `fonction(serie, **reglages)`.
        ⑦ UNITÉ — Rangs dans `serie`.
        ⑧ POURQUOI — Les réglages de la fiche arrivent à la fonction sans que `jouer` les connaisse.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Celui de la fonction nommée.
        ⑪ TERMINAISON — Celle de la fonction nommée : du code de module, non borné.
          [sort: non]
        """
        return self.fonction(serie, **self.reglages)


def declaration_du_signal(fiche):
    """Rend les trois cases du signal d'une fiche, en texte : LA SEULE lecture des colonnes du signal (A-542, R-708).

    ① RÔLE — Lire, une seule fois pour tout le juge, ce que la fiche déclare de son signal : les cases
      `module_signal`, `fonction_signal` et `reglages_signal`, chacune par SON NOM.
    ② CONTEXTE D'APPEL — `manques_du_signal` (une fois par fiche, depuis `porte_0` et `signal_de_la_fiche`),
      `signal_de_la_fiche` (une fois par fiche jouée), `forme_du_module` et `lecture_de_jeu` (une fois par ligne lue
      pour compter k).
    ③ ENTRÉE — `fiche` : la fiche reçue (ligne du registre des stratégies, fiche construite, ou `_FicheLue`).
    ④ CONDITIONS D'ENTRÉE — `fiche` a une méthode `get`. Une case absente, ou vide, vaut le texte vide.
    ⑤ SORTIE — TROIS valeurs, trois textes sans blancs de bord : le module, la fonction, le texte des réglages, NON
      décodé. Exemple réel : C5-EI-PARAMS, ligne 70 du registre → (« programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py »,
      « signaux_c5etendu10 », « ») ; C5-EI, ligne 6, sans signal → (« », « », « »).
      [rend: 3]
    ⑥ TRAITEMENT — ① lire `fiche.get("module_signal")`, `fiche.get("fonction_signal")`, `fiche.get("reglages_signal")`
      sur la fiche REÇUE · ② une case absente ou vide devient « » · ③ mettre en texte et retirer les blancs de bord ·
      ④ rendre les trois, sans rien juger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026, 17h33-17h38 (lot S_kk, avant le tour 2) : la « lecture unique » du
      signal comptait déjà DEUX lecteurs (`manques_du_signal` et `signal_de_la_fiche`), et le compte de k en ajoutait
      deux autres (`forme_du_module`, `lecture_de_jeu`) ; deux implémentations d'une même chose divergent toujours
      (R-708). Elle NE DÉCODE PAS le JSON et ne lève pas : `manques_du_signal` doit pouvoir DIRE « réglages
      illisibles » sans exception ; le décodage reste à `reglages_du_texte`. Elle lit la fiche REÇUE, jamais une
      copie : `lecture_de_jeu` passe une `_FicheLue` à `porte_0`, qui retient les cases lues ; une copie ferait perdre
      les cases du signal aux lignes refusées, et deux lignes refusées aux signaux différents compteraient pour une
      seule version. Chaque case est lue par son nom écrit en clair, et non par une boucle sur `COLONNES_DU_SIGNAL` :
      l'épreuve E7 du signal nommé cherche ces noms, et rougit si elle ne les trouve pas ici (sabotage S12).
    ⑨ CE QUI CLOCHE — Elle ne dit rien de la validité : un chemin hors de la racine, une fonction illisible ou un
      JSON faux sont rendus tels quels ; c'est `manques_du_signal` et `signal_de_la_fiche` qui jugent.
    ⑩ EFFET — Aucun, sinon celui du `get` de la fiche reçue (une `_FicheLue` note la case lue).
    ⑪ TERMINAISON — Rend toujours la main ; aucun de ses appels ne peut ne pas revenir.
      [sort: non]
    """
    module = str(fiche.get("module_signal") or "").strip()
    fonction = str(fiche.get("fonction_signal") or "").strip()
    reglages = str(fiche.get("reglages_signal") or "").strip()
    return module, fonction, reglages


def manques_du_signal(fiche):
    """Dit ce qui manque, ou est illisible, dans la déclaration du signal d'une fiche.

    ① RÔLE — La seule écriture de la règle « une fiche nomme son signal » : `porte_0` en tire ses refus, et
      `signal_de_la_fiche` refuse sur la même liste. Une fiche qui ne nomme pas son module et sa fonction est refusée,
      jamais complétée par un défaut.
    ② CONTEXTE D'APPEL — `porte_0`, une fois par fiche ; `signal_de_la_fiche`, à son entrée.
    ③ ENTRÉE — `fiche` : un dictionnaire de champs (ligne du registre des stratégies, ou fiche construite).
    ④ CONDITIONS D'ENTRÉE — Aucune : une colonne absente vaut vide.
    ⑤ SORTIE — UNE valeur : la liste des manques, en texte, VIDE si la déclaration est complète et lisible. Exemple
      réel : une ligne du registre sans signal rend ["module_signal (aucun signal nommé)",
      "fonction_signal (aucun signal nommé)"].
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ lire les trois cases par `declaration_du_signal` (la seule lecture des colonnes du signal,
      superviseur R-759 du 05-11-2026, 17h33-17h38) · ① `module_signal` vide → manque ; sinon il doit être un chemin
      relatif sous la racine, sans « .. », finissant par « .py » · ② `fonction_signal` vide → manque ; sinon un nom
      Python · ③ `reglages_signal` vide, ou un objet JSON dont les clés sont des noms Python.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-542 : le signal C5 était imposé à toute fiche par défaut. Un défaut qui choisit le signal à la
      place de la fiche fait juger une stratégie sur une autre, sans que rien ne le dise. Le chemin est EXACT, et non
      un motif : un motif prend le premier fichier qui répond, y compris un compilé du cache ou une archive (⑨ de
      `trouver`).
    ⑨ CE QUI CLOCHE — Elle ne vérifie pas que le module existe ni que la fonction y est : elle n'a pas la racine.
      C'est `signal_de_la_fiche` qui le fait, et le juge l'appelle dès la porte 0.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    manq = []
    module, fonction, reglages = declaration_du_signal(fiche)
    if module.lower() in VIDE:
        manq.append("module_signal (aucun signal nommé)")
    elif (os.path.isabs(module) or "\\" in module or ".." in module.split("/")
          or not module.endswith(".py")):
        manq.append("module_signal illisible : lu %r, attendu un chemin relatif à la racine finissant par .py" % module)
    if fonction.lower() in VIDE:
        manq.append("fonction_signal (aucun signal nommé)")
    elif not fonction.isidentifier():
        manq.append("fonction_signal illisible : lu %r, attendu un nom de fonction" % fonction)
    if reglages.lower() not in VIDE:
        try:
            r = reglages_du_texte(reglages)
        except ValueError as e:
            manq.append("reglages_signal illisible : lu %r (%s)" % (reglages, e))
        else:
            if not isinstance(r, dict) or not all(isinstance(k, str) and k.isidentifier() for k in r):
                manq.append("reglages_signal illisible : lu %r, attendu un objet JSON {\"nom\": valeur}" % reglages)
    return manq


# LA LIGNE QUI DÉCLARE UN MODULE DE SIGNAL (superviseur R-759 du 31-10-2026, voie D) : une ligne de la docstring du
# module qui S'OUVRE par « <STATUT> · module de signal · », le statut en majuscules (« DÉCIDÉ », « EN ESSAI »). Elle doit
# OUVRIR la ligne : une recherche large rendait 13 rôles dont 11 faux (claude_FABRIQUER_LE_PILOTE.py, vers la ligne 2105).
DECLARATION_DE_SIGNAL = re.compile(r"^[A-ZÀ-Ý][A-ZÀ-Ý ]* · module de signal · ")


def declaration_de_signal(chemin):
    """Lit, SANS L'EXÉCUTER, si un fichier Python se déclare module de signal.

    ① RÔLE — Dire si le fichier qu'une fiche nomme est un module de signal, avant que le juge ne l'exécute.
    ② CONTEXTE D'APPEL — `signal_de_la_fiche`, une fois par chemin et par processus, avant `charger_module`.
    ③ ENTRÉE — `chemin` : le chemin réel du fichier, sous la racine.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (vérifié par l'appelant).
    ⑤ SORTIE — DEUX valeurs : la ligne qui déclare (ou None) ; le motif du refus (ou None). Exemple réel : le module
      C5 rend (« DÉCIDÉ · module de signal · Rôle : … », None) ; `programmes/audit_ecosysteme.py` rend
      (None, « ne se déclare pas « module de signal » (il n'est pas exécuté) »).
      [rend: 2]
    ⑥ TRAITEMENT — ① lire les octets et construire l'arbre syntaxique (`ast.parse`) ; un fichier illisible comme du
      Python est refusé · ② prendre la docstring du module · ③ chercher une ligne qui S'OUVRE par
      `DECLARATION_DE_SIGNAL` · ④ sinon, refuser.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge exécute le fichier que la fiche nomme. Mesuré par le superviseur R-759 le 31-10-2026 : une fiche
      qui nommait par erreur `programmes/audit_ecosysteme.py` faisait tourner le radar complet DANS le juge (environ
      240 lignes d'audit versées au rapport, 8,8 s de calcul), sans aucune exception, puis code 0 ; rattraper l'erreur
      ne voit rien quand le fichier ne lève pas. Deux programmes du dépôt écrivent un fichier à leur chargement.
      L'arbre syntaxique se lit sans rien exécuter (0,2 à 3,3 ms par module). Une liste blanche a été écartée : c'est
      une énumération, qu'un renommage ferait changer d'avis.
    ⑨ CE QUI CLOCHE — ① C'est une déclaration, pas une preuve : un fichier qui se déclare à tort est exécuté (le filet
      de `signal_de_la_fiche` rattrape alors son erreur ou son `sys.exit`, pas ses effets). ② Seule la docstring du
      MODULE compte, pas un commentaire.
    ⑩ EFFET — LIT le fichier ; ne l'exécute pas.
    ⑪ TERMINAISON — Rend toujours la main ; une erreur de lecture du fichier (droits) lèverait OSError.
      [sort: non]
    """
    try:
        arbre = ast.parse(open(chemin, "rb").read(), chemin)
    except (SyntaxError, ValueError) as _e_syntaxe:      # ValueError : octets nuls dans le source
        return None, "n'est pas du Python lisible : %s : %s" % (type(_e_syntaxe).__name__, _e_syntaxe)
    for ligne in (ast.get_docstring(arbre) or "").splitlines():
        if DECLARATION_DE_SIGNAL.match(ligne.strip()):
            return ligne.strip(), None
    return None, "ne se déclare pas « module de signal » (il n'est pas exécuté)"


def signal_de_la_fiche(base, fiche):
    """Rend le signal que la fiche nomme : la SEULE traduction des colonnes du signal en signal jouable (A-542, R-708).

    ① RÔLE — Traduire la déclaration de la fiche (`module_signal`, `fonction_signal`, `reglages_signal`) en un signal
      prêt à jouer. Les trois cases sont LUES par `declaration_du_signal`, la seule lecture (superviseur R-759 du
      05-11-2026, 17h33-17h38) ; dans le juge, la moulinette et le juge à 8 critères, aucun programme ne les lit
      ailleurs et aucun ne choisit un signal à la place de la fiche. HORS DE CE PÉRIMÈTRE : le programme du soir
      `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` calcule toujours le signal C5 par son chemin écrit en dur, quelle
      que soit la fiche (A-542 ③, à faire).
    ② CONTEXTE D'APPEL — Trois programmes, et eux seuls : `main` et `calibrer` de ce juge ; `jouer_une` dans `main`
      de `programmes/JOUER_LES_VERSIONS.py` (la moulinette), une fois par version ; `_juger_une` de
      `programmes/JUGER_SUR_8_CRITERES.py`, une fois.
    ③ ENTRÉE — `base` : la racine du dépôt · `fiche` : un dictionnaire de champs portant les trois colonnes.
    ④ CONDITIONS D'ENTRÉE — Aucune : tout manque, et tout module qui ne se déclare pas module de signal ou ne se charge
      pas, est refusé par une ValueError qui dit pourquoi.
    ⑤ SORTIE — UNE valeur : un `SignalNomme`. Exemple réel : la fiche C5E10-QA-V1 rend la fonction
      `signaux_c5etendu10` de `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py`, sans réglages.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser si `manques_du_signal` trouve un manque ; sinon lire les trois cases par
      `declaration_du_signal` et décoder les réglages par `reglages_du_texte` · ② refuser un chemin qui sort de la racine
      ou qui n'est pas un fichier · ③ au premier appel pour ce chemin, lire SANS L'EXÉCUTER si le fichier se déclare
      module de signal (`declaration_de_signal`) et le refuser sinon ; puis le charger (`charger_module`), toute erreur
      du chargement, `SystemExit` compris, devenant un refus « ne se charge pas » · ④ refuser une
      fonction absente ou non appelable · ⑤ refuser des réglages que la signature de la fonction n'accepte pas ·
      ⑥ rendre le signal.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule rédaction de cette lecture : le 30-10-2026, le même défaut (le signal C5 imposé) vivait à
      quatre endroits de trois programmes. Les réglages se confrontent à la signature AVANT de jouer, mais
      `inspect.signature(...).bind` ne vérifie que leurs NOMS (un réglage oublié ou en trop est refusé ici) ; une
      mauvaise VALEUR (graine « 7 » en texte, proportion 5) n'est vue qu'au jeu, où la fonction de signal lève : le
      juge met alors la fiche « EN ÉCHEC » et juge les suivantes (superviseur R-759 du 31-10-2026 : un essai à vide
      de la fonction a été écarté, il ne prouve pas qu'un réglage est valide).
      LE MODULE SE DÉCLARE AVANT D'ÊTRE EXÉCUTÉ (superviseur R-759, tour 3, 31-10-2026) : une fiche qui nommait par erreur
      `programmes/audit_ecosysteme.py` faisait tourner le radar complet dans le juge, sans exception, code 0 (voir
      `declaration_de_signal`, ⑧). LE FILET reste derrière, pour un module déclaré mais cassé : relecture du tour 2,
      une erreur de syntaxe, un import absent ou une exception au chargement arrêtaient le juge avant toute fiche, et
      un `sys.exit(0)` le faisait sortir avec 0.
    ⑨ CE QUI CLOCHE — ① Le module est gardé en mémoire par chemin : modifié pendant un même lancement, il ne serait
      pas relu. ② Charger un module DÉCLARÉ exécute son code (⑨ ① de `charger_module`) : ses effets au chargement
      ne sont pas empêchés, seuls son erreur et son `sys.exit` sont rattrapés ; un fichier NON déclaré n'est jamais
      exécuté. ③ Le chemin est exact : renommer un
      module oblige à réécrire ses fiches — voulu, un renommage devient visible au lieu d'être deviné.
    ⑩ EFFET — LIT le module nommé ; l'EXÉCUTE à son premier appel pour ce chemin, s'il se déclare module de signal.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError avec le motif du refus, y compris quand le chargement lève ou
      appelle `sys.exit` (rattrapés). `KeyboardInterrupt` n'est pas rattrapé. Un module dont le chargement ne revient
      pas (boucle) bloque l'appel.
      [sort: non]
    """
    ident = fiche.get("id") or "(sans identifiant)"
    manq = manques_du_signal(fiche)
    if manq:
        raise ValueError("fiche %s : signal refusé — %s" % (ident, " ; ".join(manq)))
    module, fonction, texte = declaration_du_signal(fiche)
    reglages = reglages_du_texte(texte)
    racine = os.path.realpath(base)
    chemin = os.path.realpath(os.path.join(racine, module))
    if os.path.commonpath([racine, chemin]) != racine:
        raise ValueError("fiche %s : signal refusé — module_signal %r sort de la racine" % (ident, module))
    if not os.path.isfile(chemin):
        raise ValueError("fiche %s : signal refusé — module_signal %r introuvable sous la racine" % (ident, module))
    mod = _MODULES_DE_SIGNAL.get(chemin)
    if mod is None:
        # LE FICHIER SE DÉCLARE AVANT D'ÊTRE EXÉCUTÉ, puis LE FILET (superviseur R-759, tour 3, 31-10-2026)
        _ligne, _refus = declaration_de_signal(chemin)
        if _refus:
            raise ValueError("fiche %s : signal refusé — le module %s %s" % (ident, module, _refus))
        try:
            mod = charger_module(chemin, "signal_" + hashlib.sha256(chemin.encode("utf-8")).hexdigest()[:12])
        except (Exception, SystemExit) as _e_charge:
            raise ValueError("fiche %s : signal refusé — le module %s ne se charge pas : %s : %s"
                             % (ident, module, type(_e_charge).__name__, _e_charge))
        _MODULES_DE_SIGNAL[chemin] = mod
    fn = getattr(mod, fonction, None)
    if not callable(fn):
        raise ValueError("fiche %s : signal refusé — le module %s n'expose pas la fonction %r" % (ident, module, fonction))
    import inspect
    try:
        inspect.signature(fn).bind(None, **reglages)
    except TypeError as e:
        raise ValueError("fiche %s : signal refusé — les réglages %s ne s'appliquent pas à %s : %s"
                         % (ident, texte or "{}", fonction, e))
    return SignalNomme(fn, reglages, "%s · %s · réglages %s" % (module, fonction, texte or "aucun"), mod, module)


class SignalRefuse(ValueError):
    """Le refus nommé d'un signal au moment de le jouer : sortie mal formée (point 8).

    ① RÔLE — Distinguer un REFUS (la fiche n'est pas jugeable, le motif est nommé) d'une PANNE (« EN ÉCHEC »).
    ② CONTEXTE D'APPEL — Levé par `SignalNomme.__call__` ; rattrapé par `main` (fiche « REFUSÉE AU JEU »), et par les
      appelants de `jouer` comme toute ValueError.
    ③ ENTRÉE — Le motif, en texte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune (exception). [rend: 0]
    ⑥ TRAITEMENT — Celui de ValueError.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Sous-classe de ValueError : la moulinette et le juge à 8 critères, qui rattrapent déjà les erreurs
      de `jouer`, n'ont rien à changer pour ne pas jouer la fiche.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — — [sort: non]
    """


def forme_du_signal(resultat, longueur):
    """Dit si ce que rend une fonction de signal a la forme que `jouer` attend.

    ① RÔLE — Refuser, avant de jouer, une sortie que `jouer` lirait de travers sans rien dire.
    ② CONTEXTE D'APPEL — `SignalNomme.__call__`, à chaque appel : par `jouer` (série entière ou morceau), et par
      l'épreuve d'arrivée des signaux (séries coupées).
    ③ ENTRÉE — `resultat` : ce qu'a rendu la fonction de signal · `longueur` : le nombre de séances de la série passée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None si la forme est bonne, sinon le motif en texte. Exemple : le signal C5 rend une liste
      de {"i": rang, "cci": …, "cmf": …} aux rangs croissants : None.
      [rend: 1]
    ⑥ TRAITEMENT — Exiger ① une liste · ② de dictionnaires portant « i » · ③ un « i » ENTIER au sens de
      `numbers.Integral` (un entier de Python, ou un entier de numpy comme `np.int64`), qui n'est pas un booléen ·
      ④ compris entre 0 et longueur − 1 · ⑤ strictement croissant (ni recul, ni doublon).
    ⑦ UNITÉ — Rangs dans la série passée.
    ⑧ POURQUOI — `jouer` lit `s[i]` : un rang négatif prend une séance comptée depuis la fin (une autre date, en
      silence) ; un booléen vaut 0 ou 1 ; un doublon achète deux fois le même jour. Point 8 du plan du juge.
      Les entiers de numpy sont acceptés depuis le 31-10-2026 (relecteur de la version B, défaut D8) : un module
      honnête qui calcule ses rangs avec numpy était refusé « mal formé », alors que `s[i]` les lit sans erreur. Un
      flottant, même entier (« 1.0 »), reste refusé : `s[1.0]` lève.
    ⑨ CE QUI CLOCHE — ① Les autres clés des dictionnaires (cci, cmf…) ne sont pas regardées : `jouer` ne les lit pas.
      ② Un type d'entier inscrit à la main comme `numbers.Integral` sans savoir servir d'indice serait accepté ici,
      puis ferait lever `jouer` (fiche « EN ÉCHEC »). Aucun module ne le fait.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not isinstance(resultat, list):
        return "rend %s au lieu d'une liste" % type(resultat).__name__
    precedent = -1
    for k, sg in enumerate(resultat):
        if not isinstance(sg, dict) or "i" not in sg:
            return "l'élément %d n'est pas un dictionnaire portant « i » : %r" % (k, sg)
        i = sg["i"]
        if isinstance(i, bool) or not isinstance(i, numbers.Integral):
            return "l'élément %d porte un rang %r qui n'est pas un entier" % (k, i)
        if not 0 <= i < longueur:
            return "l'élément %d porte le rang %d, hors de la série (0 à %d)" % (k, i, longueur - 1)
        if i <= precedent:
            return "l'élément %d porte le rang %d après le rang %d : rangs non croissants ou en double" % (k, i, precedent)
        precedent = i
    return None


# LES DEUX CASES DE LA FICHE QUE LE JUGE SAIT JOUER (points 5 et 9 du plan du juge, 31-10-2026) — listes FERMÉES.
# Le moment d'achat : le juge n'achète qu'à l'ouverture de la séance qui suit le signal (`jouer_une_entree`). La clé est
# la case écrite en majuscules, sans espace ni souligné ; « DÉFAUT » est le mot que la fiche écrit pour le
# comportement habituel (synthèse du chemin d'une stratégie : « une case vide est refusée »).
ENTREES_JOUABLES = {"OPENJ+1": "ouverture du lendemain", "DÉFAUT": "ouverture du lendemain"}
# Les données fournies au programme de signal : la série des cours de LA valeur, rien d'autre (`jouer` lui passe
# `cours[valeur]`). Chaque donnée ajoutée (indice, dates de résultats, consensus) sera un lot à part.
DONNEES_FOURNIES = ("cours",)


def manques_du_jeu(fiche):
    """Dit pourquoi une fiche n'est pas jouable par le juge : moment d'achat ou données hors de ses listes fermées.

    ① RÔLE — La seule écriture des deux règles « le juge n'achète qu'à l'ouverture du lendemain » et « le signal ne
      reçoit que les cours de la valeur ». `porte_0` en tire ses refus ; `jouer` refuse sur la même liste.
    ② CONTEXTE D'APPEL — `porte_0`, une fois par fiche ; `jouer`, à son entrée.
    ③ ENTRÉE — `fiche` : un dictionnaire de champs portant `entree` et `donnees_demandees`.
    ④ CONDITIONS D'ENTRÉE — Aucune : une case absente vaut vide.
    ⑤ SORTIE — UNE valeur : la liste des motifs, VIDE si la fiche est jouable. Exemples réels : C5E10-QA-V1
      (« Open J+1 », « cours ») rend [] ; C1-004 (« CLOSE ») rend le motif « NON JUGEABLE — moment d'achat non
      jouable … » ; C2-001 (« INTRADAY ») aussi.
      [rend: 1]
    ⑥ TRAITEMENT — ① `entree` vide ou « — » → manque ; sinon, écrite en majuscules sans espace ni souligné, elle doit
      être une clé de `ENTREES_JOUABLES`, sinon NON JUGEABLE · ② `donnees_demandees` vide → manque ; sinon chaque
      donnée (séparée par « , », « ; » ou « + ») doit être dans `DONNEES_FOURNIES`, sinon NON JUGEABLE, donnée absente.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge achetait TOUJOURS à l'ouverture du lendemain sans lire la case : 28 fiches du registre
      portent « CLOSE » et 1 « INTRADAY », elles auraient été jouées à l'ouverture sans un mot (audit du code, B4).
      Et une fiche qui demande le consensus (C2-001) ou la tendance de l'indice (MA200-S1) aurait été calculée sans
      cette donnée (audit du code, point 6). Refuser en nommant vaut mieux que jouer une autre stratégie que celle de
      la fiche. Une case VIDE est refusée aussi : pour le comportement habituel, la fiche écrit « DÉFAUT » (synthèse
      du chemin d'une stratégie) ; jouer une case vide à l'ouverture serait la jouer en silence.
    ⑨ CE QUI CLOCHE — ① « DEFAUT » sans accent n'est pas reconnu (liste fermée, épelée). ② La case `donnees_demandees`
      est une DÉCLARATION : un module qui lirait un fichier de son côté n'est pas empêché (le juge ne lui en passe
      aucun). ③ La colonne `filtres` n'est PAS lue ici : décision de Jean-Luc du 31-10-2026 à 17h15 (QJ-17), elle
      reste un texte affiché, jamais joué.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    manq = []
    entree = (fiche.get("entree") or "").strip()
    if entree.lower() in VIDE:
        manq.append("entree (aucun moment d'achat déclaré — écrire DÉFAUT pour l'ouverture du lendemain)")
    elif cle_d_entree(entree) not in ENTREES_JOUABLES:
        manq.append("NON JUGEABLE — moment d'achat non jouable : entree lu %r ; le juge n'achète qu'à l'ouverture du "
                    "lendemain (OPEN_J+1, Open J+1, DÉFAUT)" % entree)
    donnees = (fiche.get("donnees_demandees") or "").strip()
    if donnees.lower() in VIDE:
        manq.append("donnees_demandees (aucune donnée déclarée — écrire « cours »)")
    else:
        absentes = [d for d in donnees_du_texte(donnees) if d not in DONNEES_FOURNIES]
        if absentes:
            manq.append("NON JUGEABLE — donnée absente : %s ; le juge ne fournit au signal que : %s"
                        % (", ".join(absentes), ", ".join(DONNEES_FOURNIES)))
    return manq


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
    ② CONTEXTE D'APPEL — Trois appelants, dont deux au-dehors (relevé le 29-10-2026 ; `main`
      lit les cours à juger par `lire_par_le_lecteur` depuis le 26-10-2026, A-577 étape 1).
      · `main`, sur le témoin du golden seul, quand ce témoin est conforme.
      · `charger_cours_du_banc` de `programmes/TENIR_LES_POSITIONS.py`, que la copie des
      boucles Cowork appelle sur la référence Google et que le calibrage de ce programme
      éprouve. Le détecteur et le teneur (son chemin réel) lisent par `lire_par_le_lecteur`
      depuis le 29-10-2026 (A-577, étape 7) ; ce qui lit encore autrement est dit au ⑨ de
      `lire_par_le_lecteur`.
      · `programmes/JUGER_SUR_8_CRITERES.py` ligne 1193 (relevée le 29-10-2026).
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


def lire_par_le_lecteur(base, fichier, mnemo, jusqu_au=None):
    """Lit les cours par le lecteur unique et rend, en plus des séries, l'appartenance au CAC 40 et les trous.

    ① RÔLE — Donner au juge des stratégies les cours tels que les lit le lecteur unique
      (`programmes/LIRE_LES_COURS.py`), avec ce que ce lecteur sait et que `charger_cours`
      ignore : les périodes où chaque valeur était dans le CAC 40, et les séances où elle
      n'a pas de cours (les trous).
    ② CONTEXTE D'APPEL — Quatre appelants : `main`, pour juger les fiches (A-577, étape 1) ;
      `main` de `programmes/JOUER_LES_VERSIONS.py`, qui se compare au juge et lit donc comme
      lui (27-10-2026) ; et, depuis le 29-10-2026 (A-577, étape 7, décision de Jean-Luc du
      26-10-2026 à 19h43 : « n'oublie pas de le basculer plus tard, sinon on va se casser les
      dents »), les deux pas du circuit du soir : `charger` de
      `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` et `lire_les_cours_du_soir` de
      `programmes/TENIR_LES_POSITIONS.py`.
    ③ ENTRÉE — `base` : la racine du dépôt · `fichier` : le fichier des cours, relatif à la
      racine (`donnees/cours_maitre.csv` ou l'historique long) · `mnemo` : la table de
      `table_mnemoniques`, du mnémonique à la clé de la valeur · `jusqu_au` : la date jusqu'à
      laquelle les séances doivent avoir leurs cours, passée telle quelle au lecteur.
    ④ CONDITIONS D'ENTRÉE — Celles de `LIRE_LES_COURS.lire`. Chaque mnémonique lu doit être
      dans `mnemo`.
    ⑤ SORTIE — DEUX valeurs : les séries, au format de `charger_cours` (clé de la valeur →
      séances triées, prix en nombres) ; et la lecture, un dictionnaire : « passages »
      (clé → liste des (entrée, sortie ou None), dates AAAA-MM-JJ), « trous » (clé → liste
      triée des séances sans cours, AAAA-MM-JJ), « composition » (vrai : n'acheter qu'une
      valeur dans l'indice le jour de l'achat), « seances » (depuis le 29-10-2026 : la liste
      triée, AAAA-MM-JJ, des séances du calendrier officiel — l'indice publié pour le passé, la
      liste d'Euronext `donnees/CALENDRIER_EURONEXT.csv` pour l'avenir, R-110 — de la première
      à la dernière date du fichier ; vide pour un fichier sans barre). Exemple mesuré le
      29-10-2026 sur le maître : 722 séances, du 2024-01-02 au 2026-10-28.
      [rend: 2]
    ⑥ TRAITEMENT — ① lire par le lecteur unique · ② REFUSER la lecture (ValueError) quand le
      lecteur a mis des lignes à part (`LIRE_LES_COURS.lignes_mises_a_part`, une propriété de
      conservation, pas une liste de sortes), quand le fichier est un fichier figé modifié ou
      allongé, ou quand une valeur lue n'a aucun passage dans l'indice · ③ pour chaque
      mnémonique, traduire en clé, convertir chaque barre en nombres, trier · ④ relever ses
      passages dans l'indice et ses trous · ⑤ relever les séances du calendrier officiel entre
      la première et la dernière date du fichier (`CALENDRIER_DE_LA_BOURSE.seances_entre`, que
      le lecteur a chargé : aucune seconde lecture du calendrier).
      La borne de fin est la dernière date LUE, pas la date demandée : le teneur de positions
      tient pour « pas encore publiée » une séance que le fichier ne porte pas encore ; une
      séance du calendrier au-delà des cours la ferait passer pour une séance manquante.
    ⑦ UNITÉ — Des euros par titre, des titres échangés, des dates AAAA-MM-JJ, des séances.
    ⑧ POURQUOI — A-577 ① et ② : la pratique reconnue n'ouvre un trade que si la valeur est
      dans l'indice à la date d'entrée (Norgate avec Wealth-Lab), et ne calcule pas un
      indicateur à travers un trou (pandas, min_periods). Mesuré : rejoué sur l'historique
      long, Eiffage avait 86 trades sur 87 datés d'avant son entrée (22-12-2025). Deux lectures
      des mêmes cours divergent toujours (R-708) : le juge lit par le lecteur unique au lieu
      d'en refaire une partie.
    ⑨ CE QUI CLOCHE — Une barre que le lecteur rend mais dont un prix ne se lit pas lève une
      ValueError : `charger_cours` la sautait sans le dire. · `programmes/JUGER_SUR_8_CRITERES.py`
      lit encore autrement (`charger_cours`, relevé le 27-10-2026). · Dans le circuit du soir,
      le détecteur (`programmes/DETECTER_LES_SIGNAUX_GITHUB.py`) et le teneur de positions
      (`programmes/TENIR_LES_POSITIONS.py`, son chemin réel) lisent par ici depuis le 29-10-2026 (A-577,
      étape 7), et le versement (`programmes/TENIR_L_HISTORIQUE.py`) fait relire par le lecteur commun le
      maître complété avant de l'écrire ; NE SONT PAS basculés (relevé du relecteur du 29-10-2026, dans le
      code) : la mesure de la performance (`programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py`,
      son propre lecteur), le cockpit (`programmes/PUBLIER_LE_SITE.py`), le PILOTE
      (`programmes/claude_FABRIQUER_LE_PILOTE.py`) et le calibrage du teneur (`charger_cours_du_banc`,
      volontaire) ; voir BACKLOG A-638. La copie des boucles Cowork appelle `charger_cours_du_banc` sur la
      référence Google.
      · Le calendrier officiel ne couvre que jusqu'au 31-12-2026 (fiche de
      `programmes/CALENDRIER_DE_LA_BOURSE.py`) : une lecture attendue au-delà lève HorsCalendrier —
      mesuré le 29-10-2026 : lire(…, 2026-12-31) rend 0 ligne à part, lire(…, 2027-01-01) lève.
      Le lecteur attend les cours jusqu'à la veille : le circuit du lundi 04-01-2027 s'arrêtera
      (versement, détecteur, teneur) tant que 2027 n'est pas relevé (BACKLOG A-639, bloquant).
    ⑩ EFFET — Lit des fichiers. N'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError (lecture refusée, voir ⑥ ②, message
      commençant par « le lecteur unique ») ou l'erreur du lecteur (OSError, ValueError) ou de la
      traduction (KeyError pour un mnémonique hors de `mnemo`).
      [sort: non]
    """
    lecteur = charger_module(os.path.join(base, "programmes", "LIRE_LES_COURS.py"), "lecteur_unique")
    c = lecteur.lire(base, fichier) if jusqu_au is None else lecteur.lire(base, fichier, jusqu_au)
    # LA LECTURE SE REFUSE ICI, UNE FOIS, POUR TOUS LES APPELANTS (superviseur R-759 du 27-10-2026) : le même test,
    # recopié dans `main` et dans `programmes/JOUER_LES_VERSIONS.py`, aurait divergé (R-708). Mesuré le 27-10-2026 :
    # une ligne datée « 26/10/2026 » passait l'ancienne liste de défauts, qui oubliait les dates illisibles.
    a_part = lecteur.lignes_mises_a_part(c)
    if a_part:
        raise ValueError("le lecteur unique a mis %d ligne(s) de cours à part dans %s : rien n'est jugé" % (a_part, fichier))
    if c.get("fige_modifie") or c.get("fige_allonge"):
        raise ValueError("le lecteur unique dit que le fichier figé %s a changé : rien n'est jugé" % fichier)
    sans = sorted(m for m in c["barres"] if not c["dans_l_indice"].get(m))
    if sans:   # un fichier déclaré incrément n'a aucun passage : toute valeur serait refusée sans un mot (relecture, 27-10)
        raise ValueError("le lecteur unique ne connaît aucun passage dans le CAC 40 pour %s : rien n'est jugé"
                         % ", ".join(sans))
    iso = lambda d: d.isoformat() if hasattr(d, "isoformat") else str(d)
    cours, passages, trous = {}, {}, {}
    for m, barres in c["barres"].items():
        v = mnemo[m.upper()]
        cours[v] = [{"date": iso(d), "open": float(r["open"]), "high": float(r["high"]),
                     "low": float(r["low"]), "close": float(r["close"]), "volume": float(r["volume"])}
                    for d, r in sorted(barres.items())]
        passages[v] = [(iso(a), iso(b) if b else None) for a, b in c["dans_l_indice"].get(m, [])]
        trous[v] = sorted(iso(d) for d, _ in lecteur.trous(c, m))
    # LES SÉANCES DU CALENDRIER OFFICIEL (A-577, étape 7, 29-10-2026) : celles que le lecteur a lues, bornées aux
    # dates du fichier ; le teneur de positions les prend au lieu de les tirer des cours (R-708).
    lues = [d for b in c["barres"].values() for d in b]
    seances = [iso(d) for d, _ in lecteur.CAL.seances_entre(min(lues), max(lues), c["seances"])] if lues else []
    return cours, {"passages": passages, "trous": trous, "composition": True, "seances": seances}


def dans_l_indice(passages, jour):
    """Dit si une valeur était dans le CAC 40 un jour donné.

    ① RÔLE — Répondre, pour une date d'achat, oui ou non.
    ② CONTEXTE D'APPEL — `jouer`, à chaque signal, quand la lecture demande la composition.
    ③ ENTRÉE — `passages` : la liste des (entrée, sortie ou None) d'une valeur, rendue par
      `lire_par_le_lecteur` · `jour` : une date AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — Les dates sont écrites AAAA-MM-JJ : leur ordre de texte est l'ordre
      du calendrier.
    ⑤ SORTIE — UNE valeur : vrai si le jour tombe dans un passage, bornes comprises.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir les passages.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Les deux dates d'un passage sont des séances DANS l'indice (fiche de
      `LIRE_LES_COURS.lire_les_passages`).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return any(a <= jour and (b is None or jour <= b) for a, b in passages)


def couper_aux_trous(serie, trous):
    """Coupe une série de séances en morceaux sans trou.

    ① RÔLE — Rendre les morceaux d'une série entre lesquels manque au moins une séance, pour
      qu'aucun indicateur ne se calcule à travers un trou.
    ② CONTEXTE D'APPEL — `jouer`, une fois par valeur, quand une lecture est donnée.
    ③ ENTRÉE — `serie` : les séances triées d'une valeur · `trous` : la liste triée des
      séances sans cours de cette valeur (AAAA-MM-JJ).
    ④ CONDITIONS D'ENTRÉE — Les deux listes sont triées par date.
    ⑤ SORTIE — UNE valeur : la liste des morceaux, chacun une liste de séances consécutives ;
      la série entière, en un morceau, quand aucun trou ne tombe entre deux de ses séances.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque paire de séances voisines, chercher un trou strictement entre
      les deux ; s'il y en a un, commencer un nouveau morceau.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — A-577 ② : un indicateur sur N jours exige N vraies observations ; une ligne
      de cours ne compte pas pour une séance quand des séances manquent entre deux lignes.
    ⑨ CE QUI CLOCHE — Un trou avant la première séance ou après la dernière ne coupe rien : il
      n'est entre aucune paire.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import bisect
    morceaux, courant = [], []
    for b in serie:
        if courant:
            k = bisect.bisect_right(trous, courant[-1]["date"])
            if k < len(trous) and trous[k] < b["date"]:
                morceaux.append(courant)
                courant = []
        courant.append(b)
    if courant:
        morceaux.append(courant)
    return morceaux

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
    ② CONTEXTE D'APPEL — Depuis le 31-10-2026 (A-547, A-548, version B) : la SEULE
      lecture des pourcentages des fiches. Appelée par `seuil_de_la_fiche` (qui la
      fait servir à `porte_0`, `jouer` et `juger` de ce programme, à `_seuils` de
      `programmes/JUGER_SUR_8_CRITERES.py` et à `reglages_du_registre` de
      `programmes/TENIR_LES_POSITIONS.py`), et directement par `controler_fusion` de
      `programmes/JOUER_LES_VERSIONS.py` (la moulinette, qui compare une fiche à une
      version écrite en fraction).
    ③ ENTRÉE — `txt` : le texte à lire, venu d'une colonne du registre des
      stratégies, ou un nombre · `defaut` : ce qui est rendu quand le texte est vide ou
      illisible, `None` si l'appelant n'en donne pas. Les appelants ne
      passent que `txt`.
    ④ CONDITIONS D'ENTRÉE — Aucune. `None`, un texte vide ou un texte quelconque
      sont trois cas prévus.
    ⑤ SORTIE — UNE valeur : une fraction positive, ou la valeur de repli. Exemples
      réels : `+4.0%` rend 0,04 · `-2.5%` rend 0,025 · `-0.6%` (stop de la fiche
      C1-004) rend 0,006 depuis le 31-10-2026 (0,6 avant) · `12` rend 0,12 ·
      `0.005` (fraction écrite par la moulinette) rend 0,005 · `abc` rend `None`.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre la valeur de repli si le texte est `None` · ② noter si
      le texte porte le signe « % » · ③ remplacer la virgule par un point, retirer
      le signe pourcent et les espaces · ④ rendre la valeur de repli si plus rien ne
      reste · ⑤ lire le nombre et en prendre la VALEUR ABSOLUE, ou rendre la valeur
      de repli s'il est illisible · ⑥ AVEC « % » : toujours diviser par cent ;
      SANS « % » : diviser par cent si le nombre vaut au moins 1, le garder tel
      quel sinon (la lecture d'avant, gardée : voir ⑨ ①).
    ⑦ UNITÉ — Une FRACTION du prix d'entrée : 0,040 vaut 4 %.
    ⑧ POURQUOI — La valeur absolue est prise parce que la perte acceptée s'écrit
      avec un signe moins dans le registre, `-2.5%`, alors que les calculs la
      veulent positive : le prix de sortie se construit en RETRANCHANT cette
      fraction, et un signe conservé la rajouterait.
    ⑨ CE QUI CLOCHE —
      ① [RÉPARÉ LE 31-10-2026 POUR LE TEXTE AVEC « % », A-547] Un seuil au-dessous
      de 1 % était lu cent fois trop grand : `pourcent("0.8%")` rendait 0,8 (mesuré
      le 20-09-2026), et les six fiches archivées à stop sous 1 % (C1-004, C4-002,
      C4-001 à « -0.6% » ; C4-BOLL, C4-MFI, C5-TRIPLE à « -0.8% ») ne sortaient
      jamais au stop. RESTE OUVERT : un nombre SANS « % » est encore deviné
      (`4` → 0,04, `0.04` → 0,04, `0.8` → 0,8 soit 80 %). La règle « sans % »
      appartient à la convention d'A-548, que Jean-Luc n'a pas décidée ; elle est
      gardée telle qu'avant parce que la moulinette écrit ses versions en fraction
      (« 0.005 ») et que `programmes/EPREUVES_DE_LA_DECLINAISON.py` l'éprouve.
      Aucune fiche du registre n'écrit un seuil sans « % » (relevé le 31-10-2026 :
      toutes portent « % », ou « — », ou « à renseigner »).
      ② LE SIGNE EST PERDU ICI. Le contrôle du signe est fait par
      `seuil_de_la_fiche`, qui sait quelle colonne il lit ; un appelant qui lirait
      un seuil par `pourcent` directement ne le verrait pas (seule la moulinette le
      fait, sur des versions déjà passées par la porte 0).
      ③ Le texte illisible et le texte vide rendent la même chose. `seuil_de_la_fiche`
      les sépare dans son motif.
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
    avec_signe_pourcent = "%" in str(txt)
    s = str(txt).strip().replace(",", ".").replace("%", "").replace(" ", "")
    if not s:
        return defaut
    try:
        v = abs(float(s))
    except ValueError:
        return defaut
    # A-547 (31-10-2026) : un texte qui porte « % » est un POURCENT, quelle que soit sa taille — « -0.6% » vaut 0,006.
    if avec_signe_pourcent:
        return v / 100
    return v / 100 if v >= 1 else v


def seuil_de_la_fiche(fiche, champ):
    """Rend l'objectif de gain ou la perte acceptée d'une fiche, en fraction positive : LA lecture unique (A-548).

    ① RÔLE — Lire `tp` ou `sl` d'une fiche du registre des stratégies, refuser ce qui est illisible ou mal signé, et
      rendre la fraction que les calculs emploient. Trois programmes lisaient ces deux cases de trois façons
      différentes ; ils appellent tous celle-ci depuis le 31-10-2026.
    ② CONTEXTE D'APPEL — `porte_0`, `jouer` et `juger` de ce programme ; `_seuils` de
      `programmes/JUGER_SUR_8_CRITERES.py` (le juge à 8 critères) ; `reglages_du_registre` de
      `programmes/TENIR_LES_POSITIONS.py` (le programme du soir, qui ouvre et ferme les positions simulées).
    ③ ENTRÉE — `fiche` : un dictionnaire de champs (ligne du registre, ou fiche construite) · `champ` : « tp » ou « sl ».
    ④ CONDITIONS D'ENTRÉE — `champ` vaut « tp » ou « sl » ; sinon ValueError.
    ⑤ SORTIE — UNE valeur : la fraction positive. Exemples réels : C5E10-QA-V1, `tp` « +4.0% » → 0,04, `sl` « -2.5% »
      → 0,025 ; C1-004, `sl` « -0.6% » → 0,006.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le texte par `pourcent` ; illisible ou vide → refus « <champ> illisible » · ② refuser une
      valeur qui n'est pas un nombre FINI et STRICTEMENT POSITIF (« nan% », « -inf% », « 0% ») · ③ refuser un
      objectif de gain écrit avec un signe moins, et une perte acceptée écrite avec un signe plus · ④ rendre la fraction.
    ⑦ UNITÉ — Elle reçoit un POURCENT écrit à la main (« +4.0% ») ou une fraction (0.04) et rend une FRACTION : 0,04
      vaut 4 %.
    ⑧ POURQUOI — Deux implémentations d'une même chose divergent toujours (R-708) : le 31-10-2026, le juge lisait
      « -0.6% » comme 0,6 (60 %), le juge à 8 critères comme 0,006 en levant sur une case vide, et le programme du
      soir comme 0,006 en gardant le signe de l'objectif. Le signe se contrôle ICI parce que seule cette fonction sait
      quelle case elle lit (A-547 ④ : « le traducteur refuse un objectif négatif et un stop positif »). Un seuil sans
      signe est accepté, comme avant : refuser l'absence de signe serait une convention nouvelle (A-548), non décidée.
      Un seuil infini, indéfini ou nul est refusé depuis le 31-10-2026 (relecteur de la version B, défaut D7) : la
      porte acceptait « nan% » (un stop qui ne se déclenche jamais, toute comparaison avec nan étant fausse) et
      « 0% » (un stop au prix d'achat) ; `float` lit « nan » et « inf » sans erreur, et `pourcent` en prend la valeur
      absolue, d'où « -inf% » rendu +inf.
    ⑨ CE QUI CLOCHE — ① Un nombre sans « % » est encore deviné (⑨ ① de `pourcent`, convention d'A-548 à décider).
      ② Le contrôle du signe ne voit que le PREMIER caractère du texte : « 4 % - » passerait, puis serait illisible.
      ③ Aucune borne haute : « +150% » rend 1,5 (A-548). ④ Quatre lectures de `tp`/`sl` ne passent pas par ici
      (relecteur de la version B, défaut D4, BACKLOG A-548) : elles ne refusent ni « nan% » ni « 0% ».
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError avec le motif (champ, texte lu).
      [sort: non]
    """
    if champ not in ("tp", "sl"):
        raise ValueError("seuil_de_la_fiche : champ %r inconnu, attendu « tp » ou « sl »" % (champ,))
    texte = fiche.get(champ)
    v = pourcent(texte)
    if v is None:
        raise ValueError("%s illisible : lu %r" % (champ, texte))
    if not (math.isfinite(v) and v > 0):
        raise ValueError("%s hors des bornes : lu %r — un seuil est un nombre fini et non nul" % (champ, texte))
    debut = str(texte).strip()[:1]
    if champ == "tp" and debut == "-":
        raise ValueError("tp mal signé : lu %r — un objectif de gain s'écrit sans signe moins (A-547)" % (texte,))
    if champ == "sl" and debut == "+":
        raise ValueError("sl mal signé : lu %r — une perte acceptée s'écrit sans signe plus (A-547)" % (texte,))
    return v


def seuil_de_la_fiche_ou_aucun(fiche, champ):
    """Lit `tp` ou `sl` comme `seuil_de_la_fiche`, en acceptant de plus « sans stop » pour `sl` : rend une fraction ou STOP_AUCUN.

    ① RÔLE — LA lecture d'un seuil pour les lecteurs du juge qui ACCEPTENT une version sans stop : la porte 0, la
      lecture du jeu et `jouer` (la moulinette joue ses versions par `jouer`).
    ② CONTEXTE D'APPEL — `porte_0`, `lecture_de_jeu`, `jouer` de ce programme ; `controler_fusion` de
      `programmes/JOUER_LES_VERSIONS.py`. PAS `juger` : il refuse une fiche sans stop par MOTIF_SANS_STOP_NON_JUGEABLE.
    ③ ENTRÉE — `fiche` : un dictionnaire de champs · `champ` : « tp » ou « sl ».
    ④ CONDITIONS D'ENTRÉE — Celles de `seuil_de_la_fiche`.
    ⑤ SORTIE — UNE valeur : `COMMUN.STOP_AUCUN` si `champ` vaut « sl » et que la case porte le mot « sans stop »
      (`COMMUN.est_le_mot_du_stop_aucun`) ; sinon ce que rend `seuil_de_la_fiche`. Exemples : C5E10-QA-V1, `sl`
      « -2.5% » → 0,025 ; une version de la moulinette, `sl` « sans stop » → STOP_AUCUN ; `tp` « sans stop » → refus.
      [rend: 1]
    ⑥ TRAITEMENT — ① « sl » et le mot : rendre la sentinelle · ② sinon déléguer à `seuil_de_la_fiche`.
    ⑦ UNITÉ — Une FRACTION du prix d'entrée, ou la sentinelle.
    ⑧ POURQUOI — DÉCISION DE JEAN-LUC du 19-10-2026 à 20h22 (A-541) : la moulinette essaie le stop « sans stop ».
      Même forme que `lire_horizon_ou_aucune` pour « aucune » (contrat du lot 0) : la lecture stricte ne change pas,
      un lecteur qui accepte le cas l'appelle explicitement. Le programme du soir lit le registre par
      `seuil_de_la_fiche` : il continue de refuser « sans stop » (A-645, garde-fou : aucune fiche VIVANTE ne reçoit
      une sortie que le soir ne sait pas tenir).
    ⑨ CE QUI CLOCHE — « sans stop » n'existe que pour le stop : un objectif « sans objectif » n'est pas décidé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError comme `seuil_de_la_fiche`.
      [sort: non]
    """
    if champ == "sl" and est_le_mot_du_stop_aucun(fiche.get("sl")):
        return STOP_AUCUN
    return seuil_de_la_fiche(fiche, champ)


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
      champs regardés sont `periode`, `indicateurs`, `univers`, `tp`, `sl`,
      `horizon` et, depuis le 30-10-2026 (A-542), les trois colonnes du signal
      `module_signal`, `fonction_signal` et `reglages_signal`.
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
      manques, et les bornes validées. Entre ② et ③, les manques du signal nommé
      (`manques_du_signal`, A-542) : une fiche qui ne nomme pas son module et sa
      fonction de signal est refusée, avec le motif « aucun signal nommé ».
      Depuis le 31-10-2026 (A-547, A-548), le ③ passe par `seuil_de_la_fiche`, la
      lecture unique, qui refuse aussi un objectif écrit avec un signe moins et une
      perte acceptée écrite avec un signe plus.
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
    # LA FICHE NOMME SON SIGNAL (A-542, 30-10-2026) : sans module ni fonction nommés, elle est refusée ici, jamais
    # complétée par le signal C5 comme avant. La règle s'écrit une fois, dans `manques_du_signal`.
    manq += manques_du_signal(fiche)
    # LE MOMENT D'ACHAT ET LES DONNÉES (points 5 et 9 du plan du juge, 31-10-2026) : hors des listes fermées, la fiche
    # est refusée ici, en le nommant, jamais jouée à l'ouverture en silence. La règle s'écrit une fois, dans
    # `manques_du_jeu`.
    manq += manques_du_jeu(fiche)
    # LES SEUILS SE LISENT PAR LA LECTURE UNIQUE (A-548, 31-10-2026) : illisible ou mal signé, la fiche est refusée ici.
    # « sans stop » est lisible depuis le 11-11-2026 (A-541, mission VENTE) : `seuil_de_la_fiche_ou_aucun`.
    for c in ("tp", "sl"):
        if c not in manq:
            try:
                seuil_de_la_fiche_ou_aucun(fiche, c)
            except ValueError as _e_seuil:
                manq.append(str(_e_seuil))
    # L'HORIZON SE LIT PAR LA MEME FONCTION QUE LE PROGRAMME DU SOIR (defaut 4 de
    # A-491, 28-09-2026) : l'ancienne lecture refusait « 20j » et acceptait « 0 ».
    # DEPUIS LE 11-11-2026 (plan V7, bloc 4), « aucune » (aucune durée maximale) est lisible : la vente unique
    # (`MODULE_POSITIONS.vendre`) et le programme du soir la traitent.
    if "horizon" not in manq and lire_horizon_ou_aucune(fiche.get("horizon")) is None:
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


# ══ LE COMPTE DES ESSAIS (lot S_kk, étape D, 05-11-2026) ═════════════════════════════════════════════════════════════
# Quatre LECTURES extraites, chacune écrite UNE fois et appelée par son ancien appelant ET par `lecture_de_jeu` (R-708 :
# deux implémentations d'une même chose divergent toujours) ; puis la lecture de jeu, le compteur de versions et k à la
# date d'une déclaration. Décision de Jean-Luc du 05-11-2026 à 13h40 (Q-G5, « 1 ») : k compte chaque VERSION QUI CHANGE
# UN CALCUL, en comparant une ligne « à la ligne précédente de la même stratégie ».


def mnemoniques_de_l_univers(texte):
    """Rend les mnémoniques d'un univers écrit, dans l'ordre : LA lecture de la case `univers`.

    ① RÔLE — Découper la case `univers` d'une fiche en mnémoniques, une seule fois pour tout le juge.
    ② CONTEXTE D'APPEL — `jouer` (une fois par fiche jouée), `juger` (une fois, pour le hasard « valeur ») et
      `lecture_de_jeu` (une fois par ligne lue).
    ③ ENTRÉE — `texte` : la case `univers`, telle qu'écrite au registre.
    ④ CONDITIONS D'ENTRÉE — `texte` est un texte (une case absente lève, comme avant l'extraction).
    ⑤ SORTIE — UNE valeur : la liste des mnémoniques, en majuscules, sans blancs ni case vide. Exemple réel :
      C5-EI-PARAMS, « TTE,ENGI,VIE,EN,FGR,AIR,SAF,HO,DSY » → ['TTE', 'ENGI', …, 'DSY'], 9 mnémoniques.
      [rend: 1]
    ⑥ TRAITEMENT — couper aux virgules, retirer les blancs, mettre en majuscules, écarter les morceaux vides.
    ⑦ UNITÉ — Des mnémoniques.
    ⑧ POURQUOI — `jouer` et `juger` écrivaient chacun cette lecture, et le prototype du superviseur la recopiait une
      troisième fois (superviseur R-759 du 05-11-2026, §3.2) : une seule écriture, sinon elles divergent (R-708).
    ⑨ CE QUI CLOCHE — L'ORDRE est gardé : c'est à l'appelant de prendre un ensemble s'il compare (`lecture_de_jeu`
      le fait). Un doublon (« TTE,TTE ») est gardé deux fois.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève AttributeError si `texte` n'est pas un texte.
      [sort: non]
    """
    return [x.strip().upper() for x in texte.split(",") if x.strip()]


# LE RÉGLAGE QUI DIT SI LE SOIR TIENT UNE FICHE SANS DURÉE (« aucune ») — question à Jean-Luc (superviseur R-759 du
# 12-11-2026, §4) : le bloc 4 suffit-il pour dire que « le soir sait lire aucune » (A-645 : « aucune fiche VIVANTE ne
# reçoit AUCUNE avant que le soir sache la lire (A-644) », A-644 À FAIRE) ? Le réglage se LIT dans ce fichier, sous la
# racine ; marqué À DÉCIDER ; tout ce qui n'est pas exactement « accepter » (fichier absent, ligne absente, autre mot)
# vaut REFUSER, la valeur la plus stricte.
FICHIER_DES_REGLAGES_DU_SOIR = os.path.join("donnees", "REGLAGES_DU_SOIR.csv")
REGLAGE_HORIZON_AUCUNE_AU_SOIR = "horizon_aucune_au_soir"
MOTIF_SANS_STOP_AU_SOIR = (
    "sans stop : le soir ne sait pas tenir une position sans stop (garde-fou d'A-645 ; « sans stop » est un réglage "
    "du laboratoire, A-541)")
MOTIF_AUCUNE_AU_SOIR = (
    "horizon « aucune » refusé au soir : réglage « %s » de %s ≠ « accepter » (À DÉCIDER par Jean-Luc : le bloc 4 "
    "suffit-il pour dire que le soir sait lire « aucune », A-644 ?)" % (REGLAGE_HORIZON_AUCUNE_AU_SOIR,
                                                                       FICHIER_DES_REGLAGES_DU_SOIR))


def soir_accepte_aucune(racine):
    """Dit si le soir tient une fiche à l'horizon « aucune » : lit le réglage, refuse par défaut.

    ① RÔLE — Lire, à un seul endroit, le réglage À DÉCIDER qui ouvre ou ferme le soir à l'horizon « aucune ».
    ② CONTEXTE D'APPEL — `lecture_du_soir`, pour une fiche dont l'horizon est « aucune ».
    ③ ENTRÉE — `racine` : la racine du dépôt (ou d'une copie).
    ④ CONDITIONS D'ENTRÉE — Aucune : un fichier absent ou illisible est un cas prévu.
    ⑤ SORTIE — UNE valeur : vrai seulement si `donnees/REGLAGES_DU_SOIR.csv` porte une ligne
      `horizon_aucune_au_soir` dont la `valeur`, sans blancs de bord et en minuscules, vaut « accepter » ; faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le fichier par `lire_csv` · ② chercher la ligne du réglage · ③ comparer sa valeur.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Demande du Chat du 12-11-2026 (tour 2 de la mission VENTE), d'après le superviseur R-759 du même
      jour : la décision revient à Jean-Luc ; en attendant, le code la lit dans un fichier (un seuil ou un réglage se
      lit, il ne s'écrit pas dans le code) et prend la valeur la plus stricte.
    ⑨ CE QUI CLOCHE — Le fichier n'est pas déclaré au contrat des fichiers (le programme des contrats) :
      un seul lecteur, celui-ci. Une faute de frappe dans la valeur ferme le soir à « aucune » sans le dire ailleurs
      que dans le motif de refus.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    lignes = lire_csv(os.path.join(racine, FICHIER_DES_REGLAGES_DU_SOIR))
    if not isinstance(lignes, list):
        return False
    return any((l.get("reglage") or "").strip() == REGLAGE_HORIZON_AUCUNE_AU_SOIR
               and (l.get("valeur") or "").strip().lower() == "accepter" for l in lignes)


def lecture_du_soir(racine, fiche):
    """Rend l'objectif, le stop et l'horizon d'une fiche TELS QUE LE SOIR LES EXÉCUTE, ou lève un refus nommé.

    ① RÔLE — LA lecture d'une fiche par le circuit du soir : la porte (`fiche_suivie`) et l'exécution
      (`reglages_du_registre` de `programmes/TENIR_LES_POSITIONS.py`) l'appellent toutes les deux, si bien qu'une fiche
      suivie est une fiche réglée, et réciproquement, par construction.
    ② CONTEXTE D'APPEL — `fiche_suivie` (donc le détecteur des signaux et le teneur des positions) ; `reglages_du_registre`.
    ③ ENTRÉE — `racine` : la racine du dépôt (pour le réglage du soir) · `fiche` : une ligne du registre des stratégies.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — TROIS valeurs : `tp` et `sl` en FRACTIONS (0,04 et 0,025 pour C5E10-QA-V1), l'horizon (entier de
      séances, `COMMUN.HORIZON_AUCUNE` si le réglage du soir l'accepte, ou None s'il est illisible — comme avant le
      12-11-2026 : la porte `porte_0` refuse déjà un horizon illisible, et le teneur garde son garde-fou
      `horizons_illisibles`).
      [rend: 3]
    ⑥ TRAITEMENT — ① stop « sans stop » → refus MOTIF_SANS_STOP_AU_SOIR · ② `seuil_de_la_fiche` (strict) pour tp et sl
      · ③ horizon par `lire_horizon_ou_aucune` : « aucune » → refus MOTIF_AUCUNE_AU_SOIR sauf si `soir_accepte_aucune`.
    ⑦ UNITÉ — Fractions ; séances.
    ⑧ POURQUOI — Défaut D1 du relecteur neuf du 11-11-2026 (23h56) : après l'ajout de « sans stop » au laboratoire,
      `porte_0` (donc `fiche_suivie`) laissait passer une fiche VIVANTE sans stop, que `reglages_du_registre` écartait
      en silence — deux positions EN_ATTENTE le soir de la faute, l'arrêt « seuils inconnus » un soir plus tard. Le
      superviseur R-759 du 12-11-2026 : « UNE fonction, `lecture_du_soir(fiche)` […] appelée par les DEUX lecteurs du
      soir » ; une garde ajoutée dans le seul teneur serait une rustine (le détecteur ne la verrait pas, R-708).
      `porte_0` garde le sens « laboratoire » : `JOUER_LES_VERSIONS` doit laisser passer une version sans stop.
    ⑨ CE QUI CLOCHE — le programme de mesure de la performance du soir (MESURER_LA_PERFORMANCE…, l. 2161) lit encore le stop à sa
      façon : troisième lecteur du soir, proposé au BACKLOG (note de la mission VENTE). Un horizon illisible est rendu
      None et non refusé ici (comportement du soir d'avant, gardé ; le calibrage du teneur lit des registres sans
      colonne horizon) : la propriété « suivie ⇔ réglée » ne vaut donc que pour les fiches qui passent `porte_0`.
    ⑩ EFFET — Lit le réglage du soir (fichier), pour une fiche « aucune » seulement.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError avec le motif.
      [sort: non]
    """
    if est_le_mot_du_stop_aucun(fiche.get("sl")):
        raise ValueError(MOTIF_SANS_STOP_AU_SOIR)
    tp, sl = seuil_de_la_fiche(fiche, "tp"), seuil_de_la_fiche(fiche, "sl")
    h = lire_horizon_ou_aucune(fiche.get("horizon", ""))
    if h is HORIZON_AUCUNE and not soir_accepte_aucune(racine):
        raise ValueError(MOTIF_AUCUNE_AU_SOIR)
    return tp, sl, h


def fiche_suivie(racine, fiche, mnemo):
    """Dit si le soir peut suivre une fiche : le signal et les valeurs qu'elle déclare, ou le motif de son refus.

    ① RÔLE — LE seul critère de la garde du soir (« une fiche que le juge refuse ne reçoit pas de signal »), pour le
      détecteur ET pour le teneur des positions.
    ② CONTEXTE D'APPEL — `programmes/DETECTER_LES_SIGNAUX_GITHUB.py`, `fiches_du_soir` (quelles fiches donnent leur
      signal et leur univers) ; `programmes/TENIR_LES_POSITIONS.py`, `tenir_pour_de_vrai` (quelles fiches reçoivent
      les signaux du jour). Les deux l'appellent pour chaque fiche VIVANTE à univers non vide.
    ③ ENTRÉE — `racine` : la racine du dépôt · `fiche` : la ligne du registre des stratégies (la dernière d'un
      identifiant) · `mnemo` : la table du référentiel des valeurs, mnémonique → clé de valeur (`table_mnemoniques`).
    ④ CONDITIONS D'ENTRÉE — La fiche porte `univers`.
    ⑤ SORTIE — TROIS valeurs : le signal (`SignalNomme`), la liste des clés de valeurs de l'univers, None — si la
      fiche est suivie ; sinon None, None, et le motif du refus (texte).
      [rend: 3]
    ⑥ TRAITEMENT — ① `porte_0` : refus avec ses motifs · ①bis `lecture_du_soir` (depuis le 12-11-2026) : refus avec
      son motif (« sans stop », « aucune » non accepté au soir) · ② `signal_de_la_fiche` : refus si elle lève ValueError ·
      ③ chaque mnémonique de l'univers doit être au référentiel, sinon la fiche ENTIÈRE est refusée, mnémonique(s)
      nommé(s).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le critère était écrit deux fois (détecteur de C, `refus_du_juge` du teneur de A) et divergeait :
      RELU Cowork ab8fc49f du 11-11-2026, LC-1 — avec un univers « TTE,ZZZ », le détecteur disait la fiche « PAS
      suivie » et le teneur lui ouvrait quand même des positions sur TOTALENERGIES (A-706 ④ non tenu). Deux
      implémentations d'une même chose divergent toujours (R-708). Elle vit DANS LE JUGE, pas au contrat : elle
      rejoue la porte et la lecture du signal du juge, et le contrat ne porte que des déclarations de champs.
    ⑨ CE QUI CLOCHE — Une autre exception que ValueError, levée par le module de signal, n'est pas un refus : elle
      remonte (une vraie panne, pas une fiche mal écrite), et arrête l'appelant.
    ⑩ EFFET — `signal_de_la_fiche` charge (exécute) le module de signal de la fiche.
    ⑪ TERMINAISON — Rend la main, ou lève ce que lève le module de signal (hors ValueError).
      [sort: non]
    """
    porte = porte_0(fiche)
    if not porte[0]:
        return None, None, "porte du juge : " + " ; ".join(map(str, porte[1]))
    # LA LECTURE DU SOIR, LA MÊME QUE CELLE DE L'EXÉCUTION (`reglages_du_registre`) : défaut D1 de la mission VENTE,
    # marche du superviseur R-759 du 12-11-2026. `porte_0` est la porte du LABORATOIRE (« sans stop » y passe).
    try:
        lecture_du_soir(racine, fiche)
    except ValueError as e:
        return None, None, "lecture du soir : " + str(e)
    try:
        sig = signal_de_la_fiche(racine, fiche)
    except ValueError as e:
        return None, None, str(e)
    codes = mnemoniques_de_l_univers(fiche["univers"])
    inconnus = [c for c in codes if c not in mnemo]
    if inconnus:
        return None, None, "mnémonique(s) absent(s) du référentiel : " + ", ".join(inconnus)
    return sig, [mnemo[c] for c in codes], None


def cle_d_entree(texte):
    """Rend la clé sous laquelle le juge cherche un moment d'achat dans `ENTREES_JOUABLES`.

    ① RÔLE — LA lecture de la case `entree` en clé : majuscules, sans espace ni souligné.
    ② CONTEXTE D'APPEL — `manques_du_jeu` (une fois par fiche) et `lecture_de_jeu` (une fois par ligne jouable).
    ③ ENTRÉE — `texte` : la case `entree`, déjà débarrassée de ses blancs de bord par l'appelant.
    ④ CONDITIONS D'ENTRÉE — `texte` est un texte.
    ⑤ SORTIE — UNE valeur : la clé. Exemples réels : « Open J+1 » → « OPENJ+1 » ; « DÉFAUT » → « DÉFAUT ».
      [rend: 1]
    ⑥ TRAITEMENT — majuscules, puis retrait des espaces et des soulignés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Copiée par le prototype du superviseur depuis `manques_du_jeu` (R-708).
    ⑨ CE QUI CLOCHE — « DEFAUT » sans accent ne donne pas « DÉFAUT » (⑨ ① de `manques_du_jeu`).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return texte.upper().replace(" ", "").replace("_", "")


def reglages_du_texte(texte):
    """Rend les réglages d'un signal lus dans la case `reglages_signal` : LA lecture JSON de cette case.

    ① RÔLE — Traduire la case `reglages_signal` en dictionnaire, une seule fois pour tout le juge.
    ② CONTEXTE D'APPEL — `manques_du_signal` (case non vide), `signal_de_la_fiche` et `lecture_de_jeu`.
    ③ ENTRÉE — `texte` : la case, ou None.
    ④ CONDITIONS D'ENTRÉE — Aucune : None ou vide au sens de `VIDE` rend {}.
    ⑤ SORTIE — UNE valeur : ce que rend `json.loads` (un dictionnaire pour une case valide), {} pour une case vide.
      Exemple réel : C5-EI-PARAMS, case vide → {} ; « {"periode_cci": 20} » → {'periode_cci': 20}.
      [rend: 1]
    ⑥ TRAITEMENT — retirer les blancs de bord ; vide → {} ; sinon `json.loads`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge l'écrivait deux fois (`manques_du_signal`, `signal_de_la_fiche`) et le prototype une
      troisième (R-708).
    ⑨ CE QUI CLOCHE — Elle ne vérifie pas que le résultat est un objet : `manques_du_signal` le fait.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (json) sur un texte illisible.
      [sort: non]
    """
    t = (texte or "").strip()
    return json.loads(t) if t.lower() not in VIDE else {}


def donnees_du_texte(texte):
    """Rend les données demandées par une fiche, lues dans la case `donnees_demandees`.

    ① RÔLE — LA lecture de la case `donnees_demandees` : chaque donnée, séparée par « , », « ; » ou « + ».
    ② CONTEXTE D'APPEL — `manques_du_jeu` (case non vide) et `lecture_de_jeu`.
    ③ ENTRÉE — `texte` : la case, texte.
    ④ CONDITIONS D'ENTRÉE — `texte` est un texte.
    ⑤ SORTIE — UNE valeur : la liste des données, en minuscules, sans morceau vide. Exemple réel : « cours » → ['cours'].
      [rend: 1]
    ⑥ TRAITEMENT — couper aux séparateurs, retirer les blancs, minuscules, écarter le vide.
    ⑦ UNITÉ — Des noms de données.
    ⑧ POURQUOI — Copiée par le prototype depuis `manques_du_jeu` (R-708).
    ⑨ CE QUI CLOCHE — L'ordre et les doublons sont gardés : `lecture_de_jeu` prend un ensemble.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [x.strip().lower() for x in re.split(r"[,;+]", texte) if x.strip()]


class _FicheLue(dict):
    """Une fiche qui retient les cases qu'on y lit, sans la recopier.

    ① RÔLE — Dire quelles cases `porte_0` a examinées sur une ligne refusée.
    ② CONTEXTE D'APPEL — `lecture_de_jeu`, une fois par ligne.
    ③ ENTRÉE — `fiche` : le dictionnaire lu ; il n'est PAS copié, chaque lecture passe par lui.
    ④ CONDITIONS D'ENTRÉE — `fiche` a `get` et `[]`.
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — `get` et `[]` notent la case dans `lues`, puis lisent la fiche reçue.
    ⑦ UNITÉ — Des noms de cases.
    ⑧ POURQUOI — Ne pas recopier : une fiche qui retient elle-même ses lectures (l'épreuve de la trace) les voit ainsi.
    ⑨ CE QUI CLOCHE — Un parcours (`items`, `in`) ne passe pas par la fiche reçue : porte_0 n'en fait pas.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — —
    """

    def __init__(self, fiche):
        """Garde la fiche reçue.
        ① RÔLE — envelopper.
        ② CONTEXTE D'APPEL — `lecture_de_jeu`.
        ③ ENTRÉE — `self` : l'enveloppe · `fiche` : la fiche reçue.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — —
        [rend: rien]
        ⑥ TRAITEMENT — garder la fiche, liste des lues vide.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — ne pas recopier.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        super().__init__()
        self._fiche = fiche
        self.lues = []

    def get(self, cle, defaut=None):
        """Lit une case et la note.
        ① RÔLE — lire.
        ② CONTEXTE D'APPEL — `porte_0` et ses lecteurs.
        ③ ENTRÉE — `self` : l'enveloppe · `cle` : la case · `defaut` : la valeur si elle manque.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur, celle de la fiche.
        [rend: 1]
        ⑥ TRAITEMENT — noter,
        lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — savoir ce que porte_0 examine.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        self.lues.append(cle)
        return self._fiche.get(cle, defaut)

    def __getitem__(self, cle):
        """Lit une case et la note.
        ① RÔLE — lire.
        ② CONTEXTE D'APPEL — les lecteurs du juge.
        ③ ENTRÉE — `self` : l'enveloppe · `cle` : la case.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur, celle de la fiche.
        [rend: 1]
        ⑥ TRAITEMENT — noter, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — savoir ce que porte_0 examine.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main ; lève KeyError si la case manque.
        [sort: non]"""
        self.lues.append(cle)
        return self._fiche[cle]


def forme_du_module(fiche, lire_module):
    """Range la déclaration du module de signal d'une ligne : « sans module », « module déclaré » ou « module
    déclaré, introuvable ».

    ① RÔLE — Dire si une ligne DÉCLARE un module (au sens de `VIDE`), et, si oui, si son octet a été trouvé.
    ② CONTEXTE D'APPEL — `lecture_de_jeu` (une fois par ligne) et l'épreuve du compte des essais (M1 de n°184).
    ③ ENTRÉE — `fiche` : un dictionnaire de champs · `lire_module` : une fonction (chemin) qui rend l'empreinte du
      module ou None.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — DEUX valeurs : la forme (un des trois textes) et l'empreinte (None sans module ou introuvable).
      Exemples réels : C5-EI-PARAMS ligne 70 → « module déclaré » ; C5-EI ligne 6 (case vide) → « sans module ».
      [rend: 2]
    ⑥ TRAITEMENT — ① lire la case `module_signal` par `declaration_du_signal` (la seule lecture des colonnes du
      signal) · ② case vide au sens de `VIDE` → « sans module » ; sinon demander l'empreinte à `lire_module`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du lot C, T7 et T8 (n°184, M1) : juger « avec module » par l'EXISTENCE d'un fichier change
      d'avis quand on renomme, et range un module déclaré mais inexistant avec les lignes sans module. La déclaration
      se lit dans la case ; l'octet se demande à l'appelant. La case se lit par `declaration_du_signal` et non ici
      (superviseur R-759 du 05-11-2026, 17h33-17h38 : une seconde lecture des colonnes du signal, R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `lire_module` (lecture de l'octet, chez l'appelant).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin = declaration_du_signal(fiche)[0]
    if chemin.lower() in VIDE:
        return "sans module", None
    emp = lire_module(chemin)
    return ("module déclaré" if emp is not None else "module déclaré, introuvable"), emp


def lecture_de_jeu(fiche, lire_module):
    """Rend ce que le juge tire d'une ligne pour jouer : deux lignes de même lecture sont la même version.

    ① RÔLE — Porter la propriété du superviseur R-759 du lot C (05-11-2026, 14h58-15h05) : « deux lignes d'une même
      fiche sont la même version si et seulement si le juge, en les lisant comme il les lit pour jouer, en tire
      exactement la même chose ».
    ② CONTEXTE D'APPEL — `versions_du_registre`, une fois par ligne ; l'épreuve du compte des essais.
    ③ ENTRÉE — `fiche` : une ligne du registre (un dictionnaire) · `lire_module` : une fonction (chemin) qui rend
      l'empreinte du module nommé, ou None s'il est introuvable ; c'est l'appelant qui fournit l'octet (au jour, ou à
      une date).
    ④ CONDITIONS D'ENTRÉE — Aucune. Elle NE CONNAÎT PAS la règle « entrée vide → DÉFAUT » (règle de D1, n°177) : une
      entrée vide est refusée ici comme par `porte_0`.
    ⑤ SORTIE — UN tuple comparable par `==` d'un bloc : DOUZE valeurs (ligne jouable) ou DEUX (ligne refusée), ce que
      la marque compte. Ligne jouable : ("JOUABLE", tp, sl, horizon, ensemble des valeurs,
      moment d'achat, forme du module, empreinte, fonction, réglages en JSON trié, bornes de la période, ensemble des
      données). Ligne refusée : ("REFUSÉE", tuple trié des (case, texte aux blancs normalisés) que `porte_0` a lues).
      Exemple réel : C5-EI-PARAMS ligne 70 → jouable, tp 0,05, sl 0,02, horizon 30, 9 valeurs, « ouverture du
      lendemain ».
      [rend: 2 ou 12]
    ⑥ TRAITEMENT — ① appeler `porte_0` sur la fiche enveloppée (`_FicheLue`) · ② refusée : rendre les textes lus ·
      ③ jouable : appeler `seuil_de_la_fiche` (tp), `seuil_de_la_fiche_ou_aucun` (sl, « sans stop » compris, depuis
      le 11-11-2026), `lire_horizon`, `mnemoniques_de_l_univers`, `cle_d_entree`,
      `declaration_du_signal` (la seule lecture des colonnes du signal : la fonction et le texte des réglages),
      `forme_du_module`, `reglages_du_texte`, `donnees_du_texte` — les lecteurs mêmes du jeu — et prendre les bornes
      rendues par `porte_0`. Elle ne lit elle-même aucune colonne du signal (superviseur R-759 du 05-11-2026,
      17h33-17h38 ; épreuve E7 du signal nommé, sabotage S11).
    ⑦ UNITÉ — Seuils en fraction positive · horizon en séances · bornes en dates AAAA-MM-JJ.
    ⑧ POURQUOI — Une liste de colonnes oubliait `indicateurs` et comparait des textes (« +5.0 % » comptait comme un
      calcul neuf, relecture du lot C). Appeler les lecteurs du jeu, et non les recopier, empêche la lecture et le jeu
      de diverger (R-708). ÉCART VOLONTAIRE au point 6 du superviseur du lot C (« porte_0 et jouer la consomment ») :
      c'est la lecture qui appelle porte_0 et les lecteurs du jeu ; `jouer` ne la consomme pas, pour ne pas changer le
      chemin de calcul de C5 avant la série unique de fin de D. L'unicité tient par les lecteurs partagés et la trace.
    ⑨ CE QUI CLOCHE — ① Les cases lues par `main` seul (`etat_vie`, pour ETATS_JUGEABLES) et par `signal_de_la_fiche`
      au chargement ne sont pas dans la trace de l'épreuve (elle suit `jouer` et `juger`). ② La colonne `indicateurs`
      n'entre dans la lecture que sur une ligne refusée : sur une ligne jouable, le signal est le module.
      ③ L'empreinte est celle que rend `lire_module` : si l'appelant la prend sur le fichier du jour, une ligne
      ancienne est lue avec le module d'aujourd'hui.
    ⑩ EFFET — Celui de `lire_module`.
    ⑪ TERMINAISON — Rend la main ; lève si un lecteur du juge lève (réglages illisibles sur une ligne qui a passé
      `porte_0` : impossible, `manques_du_signal` les refuse).
      [sort: non]
    """
    lue = _FicheLue(fiche)
    rendu = porte_0(lue)
    ok, bornes = rendu[0], (rendu[2] if len(rendu) > 2 else None)
    if not ok:
        return ("REFUSÉE", tuple(sorted({(c, " ".join(str(fiche.get(c) or "").split())) for c in lue.lues})))
    _module, fonction, texte = declaration_du_signal(fiche)
    forme, emp = forme_du_module(fiche, lire_module)
    return ("JOUABLE",
            seuil_de_la_fiche(fiche, "tp"), seuil_de_la_fiche_ou_aucun(fiche, "sl"),
            lire_horizon_ou_aucune(fiche["horizon"]),
            frozenset(mnemoniques_de_l_univers(fiche["univers"])),
            ENTREES_JOUABLES[cle_d_entree(fiche["entree"].strip())],
            forme, emp, fonction,
            json.dumps(reglages_du_texte(texte), sort_keys=True),
            bornes,
            frozenset(donnees_du_texte(fiche["donnees_demandees"])))


def versions_du_registre(lignes, lire_module):
    """Compte les VERSIONS du registre des stratégies : une ligne compte si sa lecture de jeu diffère de celle de la
    ligne précédente de la même fiche.

    ① RÔLE — Appliquer la décision de Jean-Luc du 05-11-2026 à 13h40 (Q-G5, « 1 ») : k compte chaque version qui
      change un calcul ; « une ligne qui ne change aucun calcul ne compte pas » ; la comparaison se fait « avec la
      ligne précédente de la même stratégie ». Et n°175 : un changement de période ou de données compte.
    ② CONTEXTE D'APPEL — `k_a_la_date`, une fois ; l'épreuve du compte des essais.
    ③ ENTRÉE — `lignes` : les lignes du registre, dans l'ordre du fichier (dictionnaires) · `lire_module` : une fonction
      (chemin, rang) qui rend l'empreinte du module nommé par la ligne de rang `rang` (0 = première ligne de données),
      ou None.
    ④ CONDITIONS D'ENTRÉE — Chaque ligne porte `id`.
    ⑤ SORTIE — DEUX valeurs : un dictionnaire {fiche : nombre de versions} et le total. Exemple réel : sur le registre
      du 05-11-2026, C5-EI-PARAMS (lignes 65 et 70 du fichier) → 1.
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque ligne, dans l'ordre : ① LA RÈGLE DE D1, ICI SEULEMENT (n°177 ; n°53 du 31-10-2026 à
      22h26, « sa case entree vide reçoit DÉFAUT, par une LIGNE AJOUTÉE ») : une `entree` vide au sens de `VIDE` est
      lue « DÉFAUT », sur une COPIE de la ligne · ② lire la ligne par `lecture_de_jeu` · ③ la compter si sa fiche n'a
      pas de ligne précédente, ou si la lecture diffère de celle de la précédente.
    ⑦ UNITÉ — Des versions.
    ⑧ POURQUOI — Mots de Jean-Luc, 13h40 : « ce n'est pas un essai » (la ligne 70 de C5-EI-PARAMS, mêmes 48
      opérations). La première ligne d'une fiche compte : elle n'a pas de précédente (lecture du lot C, confirmée).
    ⑨ CE QUI CLOCHE — ① Une suite A → B → A compte TROIS versions : on compare à la ligne précédente, pas à toutes
      (côté strict, mots de Jean-Luc). ② Seule `entree` reçoit la règle du vide : une autre case vide est refusée.
    ⑩ EFFET — Celui de `lire_module`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    precedente, par_fiche = {}, {}
    for rang, ligne in enumerate(lignes):
        copie = dict(ligne)
        if (copie.get("entree") or "").strip().lower() in VIDE:
            copie["entree"] = "DÉFAUT"
        lue = lecture_de_jeu(copie, lambda chemin, _r=rang: lire_module(chemin, _r))
        ident = copie["id"]
        if ident not in precedente or precedente[ident] != lue:
            par_fiche[ident] = par_fiche.get(ident, 0) + 1
        precedente[ident] = lue
    return par_fiche, sum(par_fiche.values())


def k_a_la_date(racine, date_declaration, temoins):
    """Rend k, le nombre d'essais, tel que le registre des stratégies le donnait À LA DATE d'une déclaration.

    ① RÔLE — Compter les versions du registre tel qu'il était à `date_declaration` (R-505 ⑤ : k se compte à la date
      de la déclaration), plus les témoins déclarés.
    ② CONTEXTE D'APPEL — Aucun programme du circuit aujourd'hui ; l'épreuve du compte des essais.
    ③ ENTRÉE — `racine` : un dépôt git · `date_declaration` : AAAA-MM-JJTHH:MM+01:00 (contrat DECLARATION_DATEE) ·
      `temoins` : le nombre de témoins déclarés, entier ou texte ; « aucun » vaut 0.
    ④ CONDITIONS D'ENTRÉE — Le dépôt porte la branche principale du contrat (`BRANCHE_PRINCIPALE`, lue à
      `CONTRATS_DES_FICHIERS`) ; sinon INCONNU, avec la raison « branche principale … absente du dépôt » — JAMAIS de
      repli sur HEAD (relecture Cowork du 12-11-2026, E-3 ; superviseur R-759 du 12-11-2026, 13h46). Histoire absente,
      date illisible ou témoins illisibles rendent aussi INCONNU.
    ⑤ SORTIE — DEUX valeurs : un dictionnaire aux clés de `K_DU_VERDICT` (lues au contrat), `compte` =
      `COMPTES_DE_K[0]`, `valeur` = versions + témoins, ou « INCONNU » ; et la raison (vide si k est compté).
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ AVANT TOUT, vérifier que la branche principale existe (`git rev-parse --verify --quiet
      <branche>^{commit}`) : sans elle, la raison d'après (« aucun commit du registre ») mentait sur la cause ·
      ① refuser un dépôt superficiel (`git rev-parse --is-shallow-repository`) · ② prendre le dernier
      commit au plus à la date SUR LA BRANCHE PRINCIPALE du contrat (`git rev-list -1 --before=… origin/main --
      <registre>`, mission REGARD du 12-11-2026 ; c'était HEAD) · ③ lire le registre à ce commit
      (`git show`, puis `lignes_du_registre_pour_compter_k` du contrat) · ④ pour chaque ligne, le commit qui l'a ajoutée
      (`git blame --porcelain`) · ⑤ l'empreinte du module AU COMMIT DE LA LIGNE (`git show <commit>:<module>`) ·
      ⑥ `versions_du_registre` · ⑦ ajouter les témoins.
    ⑦ UNITÉ — Des essais ; la date en heure de Paris avec son décalage.
    ⑧ POURQUOI — Sans histoire, compter le registre du jour donnerait un k qui grandit avec le temps et contredit la
      déclaration (R-734 : ce qui n'a pas pu se mesurer se dit INCONNU, jamais remplacé). L'empreinte du module à la
      date de la ligne : point 8 du superviseur du lot C, sa limite 2.
    ⑨ CE QUI CLOCHE — ① Une réécriture du registre (colonne ajoutée) fait pointer `git blame` sur le commit de
      réécriture : le module est alors pris à cette date-là. ② Un rebase change la date de commit, donc le registre
      retenu. ③ `donnees/DECLARATIONS_DATEES.csv` n'a encore aucune ligne : aucun k réel n'est calculable aujourd'hui.
      ④ Une ligne du registre sur plusieurs lignes du fichier rend INCONNU (le blame ne se rapporte plus aux lignes).
    ⑩ EFFET — Lance `git` en lecture, par le lanceur unique `TENIR_LE_REGISTRE_DES_ESSAIS.git_de` ; le contrat écrit
      puis efface un fichier temporaire (le registre à la date, `lignes_du_registre_pour_compter_k`).
    ⑪ TERMINAISON — Rend la main ; un appel à `git` peut ne pas revenir si git bloque (aucun délai posé).
      [sort: non]
    """
    from CONTRATS_DES_FICHIERS import K_DU_VERDICT, COMPTES_DE_K, REGISTRE_DES_STRATEGIES, lignes_du_registre_pour_compter_k
    from CONTRATS_DES_FICHIERS import BRANCHE_PRINCIPALE
    import TENIR_LE_REGISTRE_DES_ESSAIS as _TR
    k = {c: None for c in K_DU_VERDICT}
    k.update(valeur="INCONNU", date_de_comptage=date_declaration, compte=COMPTES_DE_K[0])
    # LE LANCEUR GIT UNIQUE (superviseur J du 12-11-2026, réponse 3a ; R-708) : environnement purgé des variables de
    # LIEU du dépôt (GIT_DIR…), configuration gardée — il remplace le lanceur qui vivait ici.
    git = _TR.git_de(racine)
    # LA BRANCHE PRINCIPALE D'ABORD (relecture Cowork du 12-11-2026, E-3) : sans elle, rev-list échouait et la raison
    # disait « aucun commit du registre », alors que le registre en avait. Aucun repli sur HEAD : ce serait rouvrir la
    # faille du commit antidaté posé au-dessus de la branche (superviseur J, réponse 3b).
    branche = BRANCHE_PRINCIPALE
    code, _ = git("rev-parse", "--verify", "--quiet", branche + "^{commit}")
    if code != 0:
        return k, "branche principale %s absente du dépôt — k ne se lit que sur elle, jamais sur HEAD" % branche

    try:
        datetime.fromisoformat(date_declaration)
    except (TypeError, ValueError):
        return k, "date de déclaration illisible : %r" % (date_declaration,)
    t = str(temoins).strip().lower()
    if t == "aucun":
        nb_temoins = 0
    elif t.isdigit():
        nb_temoins = int(t)
    else:
        return k, "témoins illisibles : %r" % (temoins,)
    code, sortie = git("rev-parse", "--is-shallow-repository")
    if code != 0 or sortie.strip() != b"false":
        return k, "histoire absente : dépôt superficiel ou illisible — k ne se compte pas sur le registre du jour"
    # k SE LIT SUR LA BRANCHE PRINCIPALE, JAMAIS SUR HEAD (superviseur J, réponse 3b ; relecteur J, D2) : un commit
    # antidaté posé au-dessus d'elle choisissait le registre compté.
    code, sortie = git("rev-list", "-1", "--before=" + date_declaration, branche, "--",
                       REGISTRE_DES_STRATEGIES)
    commit = sortie.decode().strip()
    if code != 0 or not commit:
        return k, "histoire absente : aucun commit du registre au plus à %s" % date_declaration
    code, octets = git("show", "%s:%s" % (commit, REGISTRE_DES_STRATEGIES))
    if code != 0:
        return k, "registre illisible au commit %s" % commit[:12]
    lignes = lignes_du_registre_pour_compter_k(octets)
    texte = octets.decode("utf-8-sig")
    if texte.count("\n") + (0 if texte.endswith("\n") else 1) != len(lignes) + 1:
        return k, "une ligne du registre s'étend sur plusieurs lignes du fichier : le blame ne s'y rapporte plus"
    code, sortie = git("blame", "--porcelain", commit, "--", REGISTRE_DES_STRATEGIES)
    if code != 0:
        return k, "blame impossible au commit %s" % commit[:12]
    auteur_de_la_ligne = {}
    for l in sortie.decode("utf-8", "replace").splitlines():
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", l)
        if m:
            auteur_de_la_ligne[int(m.group(2))] = m.group(1)
    empreintes = {}

    def lire_module(chemin_module, rang):
        """Empreinte du module au commit qui a ajouté la ligne.
        ① RÔLE — fournir l'octet daté à `lecture_de_jeu`.
        ② CONTEXTE D'APPEL — `versions_du_registre`.
        ③ ENTRÉE — `chemin_module` : le chemin du module · `rang` : le rang de la ligne (0 = ligne 2 du fichier).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux, ou None si le
        module n'existe pas à ce commit.
        [rend: 1]
        ⑥ TRAITEMENT — commit de la ligne par le blame, `git show`, sha256.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — limite 2 du point 8 du superviseur du lot C.
        ⑨ CE QUI CLOCHE — ⑨ ① de `k_a_la_date`.
        ⑩ EFFET — lance git.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        sha = auteur_de_la_ligne.get(rang + 2)
        if (sha, chemin_module) not in empreintes:
            c, o = git("show", "%s:%s" % (sha, chemin_module)) if sha else (1, b"")
            empreintes[(sha, chemin_module)] = hashlib.sha256(o).hexdigest()[:16] if c == 0 else None
        return empreintes[(sha, chemin_module)]

    par_fiche, total = versions_du_registre(lignes, lire_module)
    k.update(valeur=total + nb_temoins, lignes_du_registre=len(lignes), fiches_du_registre=len(par_fiche),
             versions_comptees=total, temoins=nb_temoins)
    if set(k) != set(K_DU_VERDICT):
        raise ValueError("k_a_la_date : clés %s, contrat K_DU_VERDICT %s" % (sorted(k), sorted(K_DU_VERDICT)))
    return k, ""


def bareme_des_verdicts(bareme, mod_positions):
    """Rend le barème sous lequel le juge chiffre : celui qu'on lui donne, sinon le barème des verdicts.

    ① RÔLE — Donner au juge UN défaut de barème, lu chez le propriétaire des frais, jamais écrit ici.
    ② CONTEXTE D'APPEL — `jouer`, `jouer_une_entree` et `juger`, à leur entrée.
    ③ ENTRÉE — `bareme` : un nom de barème, ou None · `mod_positions` : le module des positions.
    ④ CONDITIONS D'ENTRÉE — Le module des positions porte `BAREME_DES_VERDICTS`.
    ⑤ SORTIE — UNE valeur : le nom du barème.
      [rend: 1]
    ⑥ TRAITEMENT — `bareme` s'il est donné, sinon `mod_positions.BAREME_DES_VERDICTS`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759, tour 2, D2 (29-10-2026) : les verdicts sont restés sous le régime d'avant la taxe
      jusqu'à la décision de Jean-Luc ; elle a changé une seule valeur, `MODULE_POSITIONS.BAREME_DES_VERDICTS`, passée
      à « REEL » le 29-10-2026 à 19h16 (réponse « 1 » à la question de Cowork).
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève RuntimeError si le module ne porte pas `BAREME_DES_VERDICTS` (un défaut
      silencieux au barème réel changerait les verdicts sans décision).
      [sort: non]
    """
    if bareme is not None:
        return bareme
    b = getattr(mod_positions, "BAREME_DES_VERDICTS", None)
    if not b:
        raise RuntimeError("MODULE_POSITIONS ne porte pas BAREME_DES_VERDICTS : le juge ne choisit pas seul le "
                           "barème de ses verdicts")
    return b


class RegardNonInscrit(RuntimeError):
    """Le refus de jouer une séance de la fenêtre du regard unique sans le reçu d'une inscription au registre des essais.

    ① RÔLE — Nommer ce refus : ce n'est pas une panne du juge, c'est R-505 ③ appliqué au moment où l'on JOUE.
    ② CONTEXTE D'APPEL — Levée par `_garde_du_regard_unique` ; `main` la range comme tout échec de fiche.
    ③ ENTRÉE — Le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur J du 12-11-2026, réponse 2 : « Sans reçu, `jouer` lève une erreur et ne rend aucune
      opération ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """


# Les reçus déjà LUS sur la branche dans CE processus : {(racine, nom) : l'entrée}. `jouer_une_entree` est appelée une
# fois par opération et par tirage du hasard ; sans ce cache, chaque appel referait un `fetch`. Seule la LECTURE est
# gardée (présence, nature, pas de résultat) : la fiche, le module et la période se confrontent à chaque appel. Un reçu
# clos APRÈS sa première lecture reste admis dans ce processus (même processus : limite J1).
_RECUS_VERIFIES = {}


def _garde_du_regard_unique(qui, premiere, derniere, periode, recu, nom_du_module=None):
    """Exige le reçu d'une inscription au registre des essais dès que des séances jouées touchent la fenêtre du regard
    unique ; sinon lève, avant toute opération.

    ① RÔLE — LA garde du regard unique (R-505 ③), posée sur chaque calculateur de gain nommé : `jouer`,
      `jouer_une_entree` et `MODULE_C5_ETENDU_10.backtest_c5etendu10` (superviseur GITHUB, M1 ; superviseur J,
      réponse 2 ; relecteur REGARD, R-D4).
    ② CONTEXTE D'APPEL — `jouer` (une fois, avant le premier signal), `jouer_une_entree` (à chaque entrée),
      `backtest_c5etendu10` (une fois). Des sept appelants de `jouer`, seul `JUGER_UNE_FICHE` passe un reçu ; les
      autres REFUSENT dans la fenêtre ; `JUGER_SUR_8_CRITERES` refuse toujours.
    ③ ENTRÉE — `qui` : l'identifiant de la fiche jouée, ou None quand l'appelant ne la connaît pas · `premiere`,
      `derniere` : la première et la dernière séance jouée, textes AAAA-MM-JJ · `periode` : (début, fin) que le reçu
      doit couvrir, ou None · `recu` : (racine, nom d'entrée) rendu par `TENIR_LE_REGISTRE_DES_ESSAIS.preenregistrer`,
      ou None · `nom_du_module` : le nom du fichier du module, ou None — si donné, la fiche du reçu doit nommer ce
      module (`backtest_c5etendu10`, qui ne connaît pas sa fiche).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur : rend la main si la garde passe.
      [rend: rien]
    ⑥ TRAITEMENT — ① la fenêtre au contrat (`CONTRATS_DES_FICHIERS.fenetre_du_regard_unique`) · ② [premiere,
      derniere] ne touche pas la fenêtre → rendre la main sans rien lire · ③ pas de reçu → lever · ④ reçu déjà lu
      dans ce processus → son entrée en mémoire, sans relire · ⑤ sinon le registre lu sur la branche des regards (`lire_le_registre`, après
      fetch ; il signale aussi un dépôt distant qui n'est pas le dépôt commun), sans défaut ; l'entrée nommée est un
      PREENREGISTREMENT ; aucun RESULTAT ne la clôt ; sa fiche est `qui` (forme canonique) si `qui` est donné ; sa
      fiche nomme `nom_du_module` s'il est donné ; sa période couvre `periode` (sans période : refus) — sinon lever.
    ⑦ UNITÉ — Des séances (dates AAAA-MM-JJ comparées en texte).
    ⑧ POURQUOI — La garde porte sur le moment où l'on JOUE, pas sur celui où l'on lit (superviseur GITHUB, M6). Un
      reçu clos par son RÉSULTAT a déjà servi : le rejeu le plus naturel (relecteur REGARD, R-D5). Un reçu d'une copie
      ou d'un dépôt jetable est refusé par la lecture (R-D3). Première et dernière séance plutôt que chaque barre :
      hors fenêtre, rien n'est parcouru (C5 reste identique au golden).
    ⑨ CE QUI CLOCHE — ① FILET CONTRE L'ERREUR D'AGENT, PAS CONTRE UN FAUSSAIRE (limite J1, décidée par Jean-Luc le
      12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708). ② Une série qui saute la fenêtre (avant 2000 puis après 2023) est prise pour la toucher : côté strict.
      ③ `jouer_une_entree` ne connaît pas sa fiche : le reçu n'y est confronté qu'à la période. ④ Des calculateurs non
      nommés ici (`MODULE_JUGEMENT.etalon_hasard` appelé seul, des frais propres à `JUGER_SUR_8_CRITERES`) ne sont pas
      gardés : relevé par énumération (superviseur REGARD, M6). ⑤ Le cas 2 de R-505 est bloqué (J1 GITHUB).
    ⑩ EFFET — Lit la branche des regards (réseau) seulement si la fenêtre est touchée.
    ⑪ TERMINAISON — Rend la main ou lève RegardNonInscrit ; le fetch peut ne pas revenir.
      [sort: non]
    """
    import CONTRATS_DES_FICHIERS as _C
    debut, fin = _C.fenetre_du_regard_unique()
    if not premiere or str(premiere) > fin or str(derniere) < debut:
        return
    cause = "fiche %s : séances jouées de %s à %s, dans la fenêtre du regard unique %s..%s" % (
        qui or "(non nommée)", premiere, derniere, debut, fin)
    if recu is None:
        raise RegardNonInscrit(cause + " sans reçu d'inscription au registre des essais (R-505 ③)")
    import TENIR_LE_REGISTRE_DES_ESSAIS as _TR
    racine, nom = recu
    e = _RECUS_VERIFIES.get(tuple(recu))
    if e is None:
        entrees, defauts = _TR.lire_le_registre(racine)
        if defauts:
            raise RegardNonInscrit(cause + " : registre des essais illisible ou abîmé : " + defauts[0])
        e = entrees.get(nom)
        if not e or e.get("nature") != "PREENREGISTREMENT":
            raise RegardNonInscrit(cause + " : reçu %r absent de la branche des regards" % (nom,))
        if any(x.get("nature") == "RESULTAT" and x.get("preenregistrement") == nom for x in entrees.values()):
            raise RegardNonInscrit(cause + " : le reçu %s est déjà clos par son résultat" % nom)
    if qui is not None:
        canon, raison = _C.identite_de_la_fiche(racine, qui)
        if canon is None or e["fiche_id"] != canon:
            raise RegardNonInscrit(cause + " : le reçu %s inscrit la fiche %s, pas celle-ci (%s)" % (
                nom, e["fiche_id"], raison or canon))
    if nom_du_module is not None:
        f = _C.lire_les_fiches(racine).get(e["fiche_id"]) or {}
        if os.path.basename(declaration_du_signal(f)[0]) != nom_du_module:     # LA lecture du signal (T2-D2)
            raise RegardNonInscrit(cause + " : la fiche %s du reçu ne nomme pas le module %s" % (
                e["fiche_id"], nom_du_module))
    p = _TR._bornes(e["hypothese"].get("periode"))
    if not periode or p is None or not (p[0].isoformat() <= str(periode[0]) and str(periode[1]) <= p[1].isoformat()):
        raise RegardNonInscrit(cause + " : la période inscrite au reçu %s (%r) ne couvre pas la période jouée %r" % (
            nom, e["hypothese"].get("periode"), periode))
    _RECUS_VERIFIES[tuple(recu)] = e


def jouer(fiche, cours, mnemo, mod_signal, mod_positions, periode=None, lecture=None, bareme=None,
          recu=None):
    """Comptabilite JETONS ILLIMITES : TOUS les signaux joues. La selection d'un
    signal par jour ne concerne QUE la comptabilite UN JETON, ou il faut bien
    choisir puisqu'on ne detient qu'une position (A-79, 01-08-2026).

    ① RÔLE — Rejouer une stratégie sur l'historique et rendre la liste des
      opérations qu'elle aurait faites, chacune avec son gain net en euros, frais
      payés. C'est le cœur du juge des stratégies : tout ce qui suit — résumé, jugement, étalon de
      hasard — part de cette liste.
    ② CONTEXTE D'APPEL — Sept appels (relevé du superviseur J du 12-11-2026, M1) : les quatre ci-dessous, plus
      `programmes/JOUER_LES_VERSIONS.py` (deux appels) et `programmes/JUGER_UNE_FICHE.py` (la porte, SEUL appelant
      qui passe un reçu) ; les autres refusent dans la fenêtre du regard unique.
      · `main`, une fois par fiche recevable.
      · `calibrer`, une fois, sur la fiche de calibrage.
      · `_rejouer`, à l'intérieur de `juger`, une fois par variante de réglages
      quand le voisinage est mesuré.
      · `programmes/JUGER_SUR_8_CRITERES.py`, dans `_juger_une` (ligne 1216 au 31-10-2026).
    ③ ENTRÉE — `fiche` : la ligne de stratégie, où sont lus `tp`, `sl`, `horizon` et
      `univers` · `cours` : les séries par valeur, rendues par
      `charger_cours` ou par `lire_par_le_lecteur` · `mnemo` : la table qui traduit les codes courts en noms
      rapprochés · `mod_signal` : LE SIGNAL DE LA FICHE, un `SignalNomme` rendu par
      `signal_de_la_fiche` (depuis le 30-10-2026, A-542 ; avant, le module C5 et un nom de fonction lu dans
      `_fonction_signal`) ·
      `mod_positions` : le module qui décide des sorties et des frais · `periode` :
      le couple des bornes rendu par la porte 0, ou `None` pour ne pas borner.
      `main` passe toujours les bornes de la fiche. · `lecture` : le second rendu de
      `lire_par_le_lecteur` (passages dans l'indice, trous, composition), ou `None` pour
      jouer la série entière sans composition, comme avant le 26-10-2026 (A-577, étape 1). · `bareme` : le
      nom d'un barème de frais, None pour le barème réel (A-550, voir `jouer_une_entree`). · `recu` : (racine, nom)
      d'un préenregistrement poussé au registre des essais, ou None — EXIGÉ dès qu'une séance jouée tombe dans la
      fenêtre du regard unique (`_garde_du_regard_unique`, mission REGARD du 12-11-2026).
    ④ CONDITIONS D'ENTRÉE — La fiche doit avoir passé la porte 0 : l'objectif de
      gain, la perte acceptée et l'horizon doivent être lisibles, faute de quoi la
      fonction lève (un horizon illisible : ValueError depuis le 11-11-2026 ; « aucune »
      est lisible, par `lire_horizon_ou_aucune` ; le stop « sans stop » aussi, par `seuil_de_la_fiche_ou_aucun`,
      depuis le 11-11-2026, A-541). `mod_signal` doit être un `SignalNomme` — un module, ou une
      fonction prise ailleurs, est refusé par TypeError — et le module de positions
      doit exposer `vendre` et `frais_aller_retour` (depuis le 07-11-2026, lot ①a de J1 ; avant : `tester_seance`).
    ⑤ SORTIE — DEUX valeurs : la liste des opérations, et la liste des valeurs
      demandées par la fiche mais absentes des cours. Chaque opération porte la
      valeur, la date du signal, le prix d'entrée, le prix de sortie, le motif de
      sortie (TP, SL, leurs variantes de saut, HORIZON), le gain net en euros, depuis le
      28-09-2026 la date de sortie et, depuis le 29-10-2026, les frais des deux ordres en
      euros (`frais`, A-550).
      Mesuré le 20-09-2026 sur la fiche
      `C5E10-QA-V1` : 62 opérations, aucune valeur inconnue.
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ refuser (ValueError) une fiche que le juge ne sait pas jouer
      — moment d'achat ou données hors des listes fermées, `manques_du_jeu`, depuis le
      31-10-2026 · ① lire l'objectif de gain, la perte acceptée (par
      `seuil_de_la_fiche`, la lecture unique, depuis le 31-10-2026) et l'horizon dans
      la fiche · ② traduire l'univers demandé, en séparant les valeurs connues des
      inconnues · ②bis avec une lecture, couper chaque série à ses trous
      (`couper_aux_trous`) et demander les signaux morceau par morceau ; l'achat et les
      sorties, eux, se jouent sur la série entière, à travers les trous (décision de Jean-Luc
      du 27-10-2026, 13h30) ; refuser un signal dont la séance d'achat est hors de l'indice
      (`dans_l_indice`) · ③ demander au signal de la fiche les séances qui déclenchent un
      achat · ④ écarter un signal sur la dernière séance, faute de lendemain pour
      entrer · ⑤ écarter un signal hors de la période déclarée · ⑥ entrer à
      l'ouverture du lendemain et poser les deux prix de sortie · ⑦ parcourir les
      séances DEPUIS LA SÉANCE D'ACHAT COMPRISE (R-608, depuis le 28-09-2026), dans
      la limite de l'horizon, et sortir à la première qui touche un seuil · ⑧ sortir
      à la clôture de la h-ième séance APRÈS l'achat si aucun seuil n'a été touché · ⑨ demander au module de positions les frais des DEUX ordres
      et retrancher · ⑩ ranger l'opération. Depuis le 28-10-2026, les gestes de la composition et ⑥ à ⑨ vivent dans
      `achat_admis` et `jouer_une_entree`, que l'étalon de hasard appelle aussi (R-708) ; mesuré : les opérations
      rendues sont identiques à l'octet (18 cas, 4 264 opérations, même empreinte avant et après).
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
      ① (RÉPARÉ LE 30-10-2026, A-542) Le nom de la fonction de signal avait un repli,
      `signaux`, écrit ici, et un autre, `signaux_c5etendu10`, écrit dans `main`, dans
      `calibrer` et dans `programmes/JUGER_SUR_8_CRITERES.py`. Il n'y a plus de repli :
      le signal est celui que la fiche nomme, lu par `signal_de_la_fiche` seule.
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
      ⑤ À TRAVERS UN TROU, L'HORIZON SE COMPTE EN SÉANCES QUI ONT UN COURS : une position
      qui traverse un trou de six séances (Bouygues, novembre 2011) est tenue six séances
      de calendrier de plus. Et un signal donné la veille d'un trou achète à la séance
      suivante qui a un cours, après le trou. Mesuré le 27-10-2026 : 41 séances sans cours
      au milieu des séries de l'historique des 20 ans, 32 coupures ; aucune dans le maître.
    ⑩ EFFET — Aucun sur le disque : ni lecture ni écriture de fichier, aucun accès
      réseau — SAUF la garde du regard unique, qui lit la branche des regards (fetch) quand la fenêtre est touchée. Elle APPELLE le module de signal et le module de positions, donc tout
      ce que ces modules font, elle le fait. Elle ne modifie pas les cours reçus.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER, non rattrapées ici :
      RegardNonInscrit quand une séance jouée tombe dans la fenêtre du regard unique sans reçu valable (avant toute
      opération) ; ValueError quand la fiche n'est pas jouable (`manques_du_jeu`) ou qu'un seuil
      est illisible ou mal signé (`seuil_de_la_fiche`) ; `SignalRefuse` quand la
      sortie du signal est mal formée (contrôle de `SignalNomme`, 31-10-2026) —
      `main` en fait une fiche « REFUSÉE AU JEU » ;
      TypeError quand `mod_signal` n'est pas un
      `SignalNomme` ; l'erreur du module de positions quand il n'expose pas la
      fonction de frais ; et TOUTE ERREUR DE LA FONCTION DE SIGNAL NOMMÉE, par
      exemple ValueError sur un réglage de mauvaise valeur (graine « 7 » en texte)
      ou une fonction qui n'est pas un signal. `main` les rattrape fiche par fiche
      et met la fiche « EN ÉCHEC » (depuis le 31-10-2026) ; `_rejouer` est enveloppé
      par l'enveloppe de secours du voisinage dans `juger` ; la moulinette et le
      juge à 8 critères, qui jouent une fiche par lancement, s'arrêtent sur une
      trace ou un code non nul. Et un de ses appels peut ne pas
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
        barème des frais et des règles de sortie d'une position.
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
    bareme = bareme_des_verdicts(bareme, mod_positions)   # le barème des verdicts, sauf barème donné (D2)
    # UNE FICHE QUE LE JUGE NE SAIT PAS JOUER N'EST PAS JOUÉE, même par un appelant qui ne passe pas par la porte 0
    # (le juge à 8 critères) : points 5 et 9 du plan du juge, 31-10-2026.
    _non_jouable = manques_du_jeu(fiche)
    if _non_jouable:
        raise ValueError("fiche %s non jouable : %s" % (fiche.get("id") or "(sans identifiant)", " ; ".join(_non_jouable)))
    tp = seuil_de_la_fiche(fiche, "tp")
    # LE STOP : une fraction, ou « sans stop » (STOP_AUCUN, A-541, mission VENTE du 11-11-2026) : `vendre` le tient.
    sl = seuil_de_la_fiche_ou_aucun(fiche, "sl")
    # L'HORIZON : un entier de séances, ou « aucune » (HORIZON_AUCUNE, plan V7 bloc 4, 11-11-2026). Illisible, la
    # fiche est refusée ici, avec son motif, au lieu de tomber plus loin dans la vente.
    h = lire_horizon_ou_aucune(fiche["horizon"])
    if h is None:
        raise ValueError("fiche %s non jouable : horizon illisible %r" % (fiche.get("id") or "(sans identifiant)",
                                                                       fiche.get("horizon")))

    demandes = mnemoniques_de_l_univers(fiche["univers"])
    univers, inconnus = [], []
    for m in demandes:
        v = mnemo.get(m, cle_valeur(m))
        if v in cours:
            univers.append(v)
        else:
            inconnus.append(m)

    # LA GARDE DU REGARD UNIQUE (R-505 ③ ; mission REGARD du 12-11-2026) : une séance jouée dans la fenêtre exige le
    # reçu d'une inscription poussée au registre des essais ; sans lui, AUCUNE opération n'est rendue.
    _debuts = [str(cours[v][0]["date"]) for v in univers if cours[v]]
    _fins = [str(cours[v][-1]["date"]) for v in univers if cours[v]]
    _premiere = max([min(_debuts)] + ([str(periode[0])] if periode else [])) if _debuts else ""
    # une fiche SANS identifiant n'est jamais la fiche d'un reçu : « » ne se ramène à aucune fiche (T2-D4)
    _garde_du_regard_unique(fiche.get("id") or "", _premiere, max(_fins, default=""), periode, recu)

    # LE SIGNAL EST CELUI QUE LA FICHE NOMME, LU PAR `signal_de_la_fiche` SEULE (A-542, 30-10-2026) : plus aucun
    # repli — un module passé à la place, ou une fonction prise ailleurs, est refusé.
    if not isinstance(mod_signal, SignalNomme):
        raise TypeError("jouer attend le signal de la fiche, rendu par signal_de_la_fiche (A-542) ; recu %r"
                        % type(mod_signal).__name__)
    fn = mod_signal

    ops = []
    for v in univers:
        # AVEC UNE LECTURE (A-577, étape 1) : les SIGNAUX se calculent morceau par morceau — aucun
        # indicateur ne traverse un trou ; la POSITION, elle, vit sur la série entière : l'achat se fait à
        # la séance suivante qui a un cours, et les sorties se testent sur les séances qui ont un cours,
        # à travers les trous (décision de Jean-Luc du 27-10-2026 à 13h30, « 1 la garder » : une position
        # ouverte avant un trou est gardée ; la vente forcée ne se fait qu'à la fin des données, comme
        # RealTest, « when the data ends before the test does »). Un achat n'a lieu que si la valeur est
        # dans le CAC 40 le jour de l'achat. Sans lecture : la série entière, comme avant.
        serie = cours[v]
        morceaux = [serie] if lecture is None else couper_aux_trous(serie, lecture["trous"].get(v, []))
        rang = {b["date"]: k for k, b in enumerate(serie)}
        for s in morceaux:
            for sg in fn(s):
                i = sg["i"]
                d_sig = s[i]["date"]
                j = rang[d_sig] + 1           # la séance d'achat, dans la série entière
                if j >= len(serie):
                    continue                  # un signal sans lendemain : la fin des données
                if periode and not (periode[0] <= d_sig <= periode[1]):
                    continue
                # L'ACHAT ET LA SORTIE SE JOUENT DANS `jouer_une_entree`, LA SEULE MÉCANIQUE : l'étalon de hasard
                # l'appelle aussi (R-708 ; superviseur R-759 du 28-10-2026 : deux copies avaient déjà divergé
                # deux fois le 28-09-2026, sur les frais et sur la séance d'achat).
                op = jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture, bareme, recu)
                if op is None:
                    continue
                ops.append({"valeur": v, "date_signal": d_sig, "pe": op["pe"], "px": op["px"],
                            "motif": op["motif"], "net": op["net"], "date_sortie": op["date_sortie"],
                            "frais": op["frais"], "date_entree": op["date_entree"]})
    return ops, inconnus


def achat_admis(v, serie, j, lecture):
    """Dit si la séance `j` de la série d'une valeur peut être une séance d'achat.

    ① RÔLE — La seule règle qui dit si un achat est permis ce jour-là : la valeur doit être dans le CAC 40 le
      jour de l'ACHAT, quand la lecture le demande.
    ② CONTEXTE D'APPEL — `jouer_une_entree`, à chaque entrée ; l'étalon de hasard (`MODULE_JUGEMENT.etalon_hasard`),
      par la fonction que `juger` lui passe, pour ne tirer que parmi les achats permis.
    ③ ENTRÉE — `v` : la valeur · `serie` : sa série entière de séances · `j` : le rang de la séance d'achat dans
      `serie` · `lecture` : le second rendu de `lire_par_le_lecteur`, ou None.
    ④ CONDITIONS D'ENTRÉE — `0 <= j < len(serie)`.
    ⑤ SORTIE — UNE valeur : vrai si l'achat est permis. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — sans lecture, ou si la lecture ne demande pas la composition : vrai ; sinon, le jour de l'achat
      doit tomber dans un passage de la valeur (`dans_l_indice`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le 27-10-2026, le juge a appris à n'acheter que dans l'indice ; l'étalon de hasard tirait encore
      hors de l'indice : sur C5E10-QA-V1, 306 achats possibles, dont 42 hors de l'indice (relecteur du 27-10-2026,
      point 2). Une seule écriture de la règle, pour les deux (R-708). Décision de Jean-Luc du 28-10-2026 à 23h03 :
      réparer tout de suite.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if lecture is None or not lecture.get("composition"):
        return True
    return dans_l_indice(lecture["passages"].get(v, []), serie[j]["date"])


def jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture=None, bareme=None, recu=None):
    """Joue UNE entrée : achat à l'ouverture de la séance `j`, puis sortie ; la seule mécanique d'achat-sortie.

    ① RÔLE — Rendre l'opération qu'aurait faite un achat à l'ouverture de la séance `j` de la série d'une valeur :
      seuils testés dès la séance d'achat, échéance à la h-ième séance après l'achat, frais des deux ordres.
    ② CONTEXTE D'APPEL — `jouer`, à chaque signal retenu ; l'étalon de hasard (`MODULE_JUGEMENT.etalon_hasard`),
      par la fonction que `juger` lui passe, à chaque achat tiré au sort.
    ③ ENTRÉE — `v` : la valeur · `serie` : sa série entière · `j` : le rang de la séance d'achat · `tp`, `sl` : les
      seuils en FRACTIONS · `h` : l'horizon en séances, ou `COMMUN.HORIZON_AUCUNE` (aucune durée maximale, depuis le
      11-11-2026, plan V7 bloc 4 : `vendre` ne vend alors que sur l'objectif, le stop ou la fin des données) ·
      `mod_positions` : le module des positions (`vendre`,
      `frais_aller_retour`) · `recu` : (racine, nom) d'un préenregistrement poussé, EXIGÉ si l'entrée touche la fenêtre
      du regard unique (relecteur REGARD, R-D4), ou None · `lecture` : le second rendu de `lire_par_le_lecteur`, ou None · `bareme` : le nom d'un barème
      de `donnees/BAREME_FRAIS.csv`, None pour le barème des trades vécus (« REEL ») ; un autre nom rejoue un chiffre
      ancien sous le régime qui l'a produit (A-550).
    ④ CONDITIONS D'ENTRÉE — `0 <= j < len(serie)` ; le module des positions expose `vendre` et `frais_aller_retour` ;
      chaque séance porte sa `date` ; sous le barème réel, la valeur et l'année de l'achat figurent dans
      `donnees/VALEURS_TTF.csv`.
    ⑤ SORTIE — UNE valeur : None si l'achat n'est pas permis (`achat_admis`) ou s'il tombe sur la DERNIÈRE séance
      sans qu'un seuil y soit touché (aucune séance après lui pour l'échéance) ; un achat suivi de moins de h séances
      est vendu à la dernière clôture, motif HORIZON ; sinon un dictionnaire de sept cases : `pe`, `px`, `motif`, `net`
      (euros, frais payés), `date_sortie`, `frais` (euros, les deux ordres), `date_entree` (le jour de l'achat, celui
      où la taxe frappe). [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser un achat non permis · ② demander la vente à `MODULE_POSITIONS.vendre` (fin des
      données : `"vendre"`), qui entre à l'ouverture de `serie[j]`, teste les séances `serie[j:j + 1 + h]`, séance
      d'achat comprise (R-608), sort à la première qui touche un seuil, sinon à la clôture de la h-ième séance APRÈS
      l'achat · ③ retrancher les frais des deux ordres.
    ⑦ UNITÉ — Seuils en FRACTIONS du prix d'entrée ; horizon en SÉANCES ; prix et gains en EUROS, pour 100 000 €
      engagés.
    ⑧ POURQUOI — Ce corps vivait dans `jouer`, et l'étalon de hasard en avait sa copie ; le superviseur R-759 du
      28-10-2026 a jugé « rustine » de seulement partager le test de l'indice : les deux copies avaient déjà divergé
      deux fois le 28-09-2026 (A-435 ④ sur les frais, R-608 sur la séance d'achat). Le code est celui de `jouer`,
      déplacé sans changement : les opérations du juge restent identiques à l'octet (empreinte avant et après).
      Le 07-11-2026 (lot ①a de J1, superviseur R-759 du même jour), la boucle de vente est partie, à son tour sans
      changement, dans `MODULE_POSITIONS.vendre`, pour que la décision « quand vendre » vive à un seul endroit
      (R-708) : les 100 opérations de l'étalon gardent leur empreinte complète, `788dc3a04cddc988` sous le barème réel.
      LES FRAIS NE S'ÉCRIVENT PAS EN DUR : leur propriétaire est MODULE_POSITIONS, qui les lit dans le barème daté —
      courtage de 0,15 % de la valeur échangée à l'entrée ET à la sortie, et, depuis le 29-10-2026 (A-550), la taxe
      sur les transactions financières à l'achat d'une valeur taxée, au taux de la date (0,3 % puis 0,4 % depuis le
      01-04-2025). Exemple : achat de 100 000 € de Bouygues le 30-04-2026, 150 € de courtage et 400 € de taxe.
    ⑨ CE QUI CLOCHE — Le capital de 100 000 € est écrit ici, comme il l'était dans `jouer` : MODULE_POSITIONS porte le
      sien. Ne pas le changer garde les opérations identiques ; consigné au BACKLOG.
    ⑩ EFFET — Appelle le module des positions.
    ⑪ TERMINAISON — Rend la main ; lève RegardNonInscrit (garde du regard unique, avant tout calcul), RuntimeError si le module des positions n'expose pas `vendre` ou
      `frais_aller_retour`, ce que lève `vendre` (une séance sans l'une de ses clés de prix), et ce que lève `frais_aller_retour` (une date absente du calendrier, une valeur ou une année absente de la liste des valeurs taxées : un juge qui rejoue
      2000-2023 sous le barème réel s'arrête là, faute des listes de ces années — voulu, pas de taxe supposée).
      [sort: non]
    """
    # LA GARDE DU REGARD UNIQUE, ici aussi : l'étalon de hasard appelle cette fonction directement (relecteur REGARD,
    # R-D4). Hors fenêtre, deux comparaisons de dates, rien d'autre.
    _garde_du_regard_unique(None, str(serie[j]["date"]), str(serie[-1]["date"]),
                            (str(serie[j]["date"]), str(serie[j]["date"])), recu)
    bareme = bareme_des_verdicts(bareme, mod_positions)   # le barème des verdicts, sauf barème donné (D2)
    if not achat_admis(v, serie, j, lecture):
        return None
    # LA VENTE SE DÉCIDE DANS `MODULE_POSITIONS.vendre`, ET NULLE PART AILLEURS (R-708 ; lot ①a de J1, superviseur
    # R-759 du 07-11-2026) : la boucle qui vivait ici y est déplacée sans changement. Pas de copie de repli : un module
    # des positions sans `vendre` arrête le juge, comme un module sans `frais_aller_retour`.
    _vendre = getattr(mod_positions, "vendre", None)
    if not callable(_vendre):
        raise RuntimeError("MODULE_POSITIONS n'expose pas vendre : "
                           "le juge des stratégies ne recopie pas la décision de vente")
    _vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")
    if _vente is None:
        return None
    pe, px, motif, d_sortie = _vente["pe"], _vente["px"], _vente["motif"], _vente["date_sortie"]
    q = 100000.0 / pe
    _far = getattr(mod_positions, "frais_aller_retour", None)
    if callable(_far):
        # les DEUX ordres, chacun au jour où il est passé (A-550) : la taxe ne frappe que l'achat,
        # et pas un achat revendu le jour même (BOFiP, BOI-TCA-FIN-10-10, § 60)
        f_tot = _far(q, pe, px, v, serie[j]["date"], d_sortie, bareme)["total"]
    else:
        raise RuntimeError("MODULE_POSITIONS n'expose pas frais_aller_retour : "
                           "le juge des stratégies ne recopie pas un taux de frais")
    return {"pe": pe, "px": px, "motif": motif, "net": q * (px - pe) - f_tot, "date_sortie": d_sortie,
            "frais": f_tot, "date_entree": serie[j]["date"]}


# LE REFUS NOMMÉ D'UNE FICHE « AUCUNE » PAR `juger`, tant que Jean-Luc n'a pas tranché l'embargo (plan V7, bloc 4 ;
# message du Chat du 11-11-2026, après le relecteur neuf et le superviseur R-759 du même jour).
MOTIF_AUCUNE_NON_TRANCHEE = (
    "NON JUGEABLE — horizon « aucune » : l'embargo de la coupure 70/30 et des fenêtres n'est pas tranché (plafond ; "
    "plus longue détention ou quantile) ; décision de Jean-Luc attendue — la fiche se JOUE (`jouer`), elle ne se JUGE pas")

# LE REFUS NOMMÉ D'UNE FICHE « SANS STOP » PAR `juger` (A-541 ④, 19-10-2026 : « une version sans stop n'a pas de point
# mort au sens du juge […] le juge doit le dire pour ces versions, ne pas appeler ce calcul […] et ne pas rendre de
# verdict des fenêtres glissantes, plutôt qu'un chiffre faux »).
MOTIF_SANS_STOP_NON_JUGEABLE = (
    "NON JUGEABLE — stop « sans stop » : le point mort suppose qu'une perte s'arrête au stop, il n'est pas défini "
    "(A-541 ④) ; la fiche se JOUE (`jouer`, la moulinette), elle ne se JUGE pas")


def duree_d_embargo_sans_horizon(ops, seances, frontiere):
    """Rend la plus longue détention, en séances, des opérations d'APPRENTISSAGE d'une stratégie sans durée maximale.

    ① RÔLE — Donner un nombre de séances à l'embargo de la coupure 70/30 quand la fiche n'a AUCUNE durée maximale.
      PROPOSITION de l'agent A, non tranchée ; `juger` ne l'emploie pas tant que Jean-Luc n'a pas décidé.
    ② CONTEXTE D'APPEL — L'épreuve de la vente unique (V12) ; aucun programme du circuit au 11-11-2026.
    ③ ENTRÉE — `ops` : les opérations jouées (`date_signal`, `date_entree`, `date_sortie`, `motif`) · `seances` : les
      séances de bourse, dates AAAA-MM-JJ · `frontiere` : la date de la frontière 70/30, celle que rend
      `MODULE_JUGEMENT.coupure_70_30` (qui la calcule sans dépendre de l'embargo).
    ④ CONDITIONS D'ENTRÉE — Les opérations d'une fiche « aucune » : chez elles, la FIN DES DONNÉES porte le motif
      `FIN_DES_DONNEES` depuis le 13-11-2026 (`vendre`, décision de Jean-Luc du 12-11-2026 à 09h18), `HORIZON` avant ;
      les deux sont écartés.
    ⑤ SORTIE — UNE valeur : un entier >= 1, le plus grand nombre de séances entre l'achat (exclu) et la vente (incluse)
      parmi les opérations signalées au plus tard à la frontière et vendues sur un seuil ; 1 s'il n'y en a aucune.
      [rend: 1]
    ⑥ TRAITEMENT — ① écarter les opérations signalées après la frontière (les 30 % jamais vus) · ② écarter les ventes
      `FIN_DES_DONNEES` ou `HORIZON` (fin des données) · ③ compter les séances de chacune, garder le maximum, au moins 1.
    ⑦ UNITÉ — Des SÉANCES de bourse.
    ⑧ POURQUOI — Mesurer l'embargo sur les opérations des 30 % ferait dépendre la coupure des données de test (une
      fuite) ; une vente forcée par la fin des données n'est pas une durée de la stratégie : le relecteur neuf du
      11-11-2026 a montré qu'une seule opération gardée jusqu'à la fin donnait un embargo de 698 séances et vidait la
      partie 70 % (n_70 = 0). Le plancher de 21 séances reste celui de `coupure_70_30`.
    ⑨ CE QUI CLOCHE — Aucun plafond : une stratégie qui tient une position d'apprentissage très longtemps reçoit un
      très long embargo. Le plafond, et le choix maximum ou quantile, reviennent à Jean-Luc.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève KeyError si une opération n'a pas ses dates ou son motif.
      [sort: non]
    """
    import bisect
    cal = sorted(seances)
    plus_longue = 1
    for o in ops:
        if o["date_signal"] > frontiere or o["motif"] in ("HORIZON", MOTIF_FIN_DES_DONNEES):
            continue
        n = bisect.bisect_right(cal, o["date_sortie"]) - bisect.bisect_right(cal, o["date_entree"])
        plus_longue = max(plus_longue, n)
    return plus_longue


def juger(fiche, ops, cours, seances, J, S, mod_pos, mnemo=None,
          _bornes=None, mod_pos_sig=None, lecture=None, bareme=None, racine=None):
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
      le signal de la fiche (un `SignalNomme`, depuis le 30-10-2026, A-542 ; avant,
      le module de signal), dont seul le premier élément est employé · `lecture` : le
      second rendu de `lire_par_le_lecteur`, ou `None` ; il est passé tel quel à `jouer`
      quand la stabilité paramétrique rejoue la fiche (`_rejouer`), pour que les voisins se
      jouent comme la fiche (27-10-2026). L'étalon de hasard, lui, ne le reçoit pas (BACKLOG
      A-577, en attente de Jean-Luc).
      `bareme` : le nom d'un barème de `donnees/BAREME_FRAIS.csv`, ou None pour le barème des verdicts (`MODULE_POSITIONS.BAREME_DES_VERDICTS`) ; il chiffre le point mort et l'étalon de hasard (A-550, 29-10-2026).
      `racine` : le dossier du dépôt, où le voisinage lit `donnees/combinatoires/VOISINAGE_DU_JUGE.csv` (ses
      réglages : depuis le 12-11-2026 ceux de R-505 ⑩ ; le 11-11-2026 il lisait aussi la grille de la moulinette,
      `VOISINAGE.csv`) ; None : le voisinage ne peut pas tourner, le rapport écrit « EN ÉCHEC » et la fonction lève
      à la fin (R-734).
    ④ CONDITIONS D'ENTRÉE — La fiche doit avoir passé la porte 0. Le module de
      jugement doit exposer les huit fonctions appelées ici ; le module de
      statistiques peut manquer, ses deux mesures étant alors perdues.
    ⑤ SORTIE — Ne rend rien. Tout passe par l'affichage.
      [rend: rien]
    ⑥ TRAITEMENT — ① s'arrêter avec un message si moins de cinq opérations ont été
      produites · ② calculer le taux de réussite et le point mort — la moyenne des
      points morts des opérations jugées, chacune à sa valeur et à sa date d'achat
      (`point_mort_des_operations`, décision de Jean-Luc du 29-10-2026 à 21h28,
      « A ») —, et afficher la marge · ③ mesurer et afficher les observations indépendantes (`observations_independantes`, n°106, depuis le 05-11-2026 ; avant : les épisodes à 5 séances) · ④ couper la période en sept
      dixièmes appris et trois dixièmes jamais vus, avec un embargo entre les deux,
      et afficher le taux de la partie jamais vue avec sa borne basse · ⑤ découper
      la même période en trois fenêtres successives et dire si chacune tient face à
      son point mort · ⑥ rejouer la stratégie avec ses réglages voisins par pas
      réguliers (`grille_du_voisinage`, réglages lus dans `VOISINAGE_DU_JUGE.csv`,
      jamais au hasard depuis le 11-11-2026 ; à ±10 % de chaque réglage depuis le
      12-11-2026) et lever le DRAPEAU « voisinage » de R-505 ⑩ si un voisin ne gagne pas · ⑦ afficher le gain moyen et sa borne basse · ⑧ afficher
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
      lecteur pressé lit un rapport complet. DEPUIS LE 11-11-2026, le voisinage n'écrit plus « non mesure » dans ce
      cas : il écrit « EN ÉCHEC » et la fiche sort EN ÉCHEC, code 1 ; le creux, lui, reste muet.
      ② SIX BLOCS RATTRAPENT TOUTE ERREUR ET L'ÉCRIVENT « NON MESURÉ » (le septième, le
      voisinage, écrit « EN ÉCHEC » et fait lever `juger` à la fin depuis le 11-11-2026). Un module
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
      ⑦ LES VARIANTES DE RÉGLAGES SONT DES ESSAIS ET NE SONT PAS ENCORE INSCRITES.
      Depuis le 11-11-2026, le voisinage rejoue des voisins par pas réguliers
      et affiche leur nombre comme « essais NON INSCRITS » : le registre
      des essais (BACKLOG A-226, lot L4) n'existe pas au dépôt, l'appel est préparé
      (paramètre `inscrire` de `calculer_voisinage_sur_grille`) mais rien n'est inscrit.
      ⑧ LE VOISINAGE SUIT R-505 ⑩ DEPUIS LE 12-11-2026 (26 voisins à ±10 %, tous
      gagnants, sinon DRAPEAU soumis à Jean-Luc) ; seule la règle d'arrondi de la durée
      reste provisoire, et le rapport le dit. Le drapeau est AFFICHÉ, il ne change pas
      le code de sortie : `juger` ne rend pas encore de verdict (bloc 5a du plan V7).
    ⑩ EFFET — N'écrit aucun fichier et ne touche pas au réseau. AFFICHE le bloc de
      jugement : 19 lignes mesurées le 20-09-2026 sur la fiche `C5E10-QA-V1`. Elle
      APPELLE le module de jugement, le module de statistiques et, par `_rejouer`,
      le module de signal et le module de positions. Elle ne modifie ni la fiche ni
      les opérations reçues.
    ⑪ TERMINAISON — Rend la main, sans valeur. Elle LÈVE ValueError, avant tout calcul, pour une fiche
      « sans stop » (MOTIF_SANS_STOP_NON_JUGEABLE, depuis le 11-11-2026, A-541 ④), un horizon illisible ou
      « aucune » (MOTIF_AUCUNE_NON_TRANCHEE). Elle LÈVE RuntimeError À LA FIN DU RAPPORT quand le voisinage n'a
      pas pu tourner (depuis le 11-11-2026, R-734 : `main` met alors la fiche EN ÉCHEC et sort en 1). Hors de ces
      refus, ses calculs sont enveloppés d'une enveloppe de secours, sauf le point mort, dont l'échec arrêterait
      la fonction. Et un de ses appels peut ne pas revenir :
      l'étalon de hasard rejoue 120 tirages par mode, et le voisinage rejoue la
      stratégie entière une fois par voisin (26 au plus avec les réglages de
      R-505 ⑩), sans qu'aucun temps ne soit borné.
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
        barème des frais et des règles de sortie d'une position.
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
    bareme = bareme_des_verdicts(bareme, mod_pos)   # le barème des verdicts, sauf barème donné (D2, 29-10-2026)
    mnemo = mnemo or {}
    # SANS STOP, PAS DE POINT MORT, DONC PAS DE VERDICT (A-541 ④) : refus nommé, avant la lecture stricte du stop.
    if seuil_de_la_fiche_ou_aucun(fiche, "sl") is STOP_AUCUN:
        raise ValueError(MOTIF_SANS_STOP_NON_JUGEABLE)
    tp = seuil_de_la_fiche(fiche, "tp")
    sl = seuil_de_la_fiche(fiche, "sl")
    h = lire_horizon_ou_aucune(fiche["horizon"])
    # UN HORIZON ILLISIBLE N'OBTIENT PAS DE VERDICT (relecteur neuf du 11-11-2026, tour 2, N2) : `jouer` le refuse
    # déjà ; sans ce refus, `juger` le changeait en un embargo de 21 séances (« "" », None, 0, « 0 », « aucun »…).
    if h is None:
        raise ValueError("fiche %s non jugeable : horizon illisible %r" % (fiche.get("id") or "(sans identifiant)",
                                                                         fiche.get("horizon")))
    n = len(ops)
    if n < 5:
        print("    JUGEMENT : trop peu d'operations pour juger")
        return
    wr = round(100.0 * sum(1 for o in ops if o["net"] > 0) / n, 1)

    # SANS DURÉE MAXIMALE (« aucune », plan V7 bloc 4, 11-11-2026) : l'embargo n'est pas tranché par Jean-Luc ; le
    # juge REFUSE de juger, avec un motif nommé, plutôt que de juger sur un embargo choisi par le code.
    if h is HORIZON_AUCUNE:
        raise ValueError(MOTIF_AUCUNE_NON_TRANCHEE)
    _h_emb = h

    # LE POINT MORT DEPEND DES FRAIS, DONC DE LA VALEUR ET DE LA DATE (A-550, 29-10-2026) : la
    # taxe sur les transactions financieres frappe l'achat des valeurs taxees. DECISION DE
    # JEAN-LUC DU 29-10-2026, message recu a 21h28 : « A » — chaque operation compte la taxe
    # qu'elle a vraiment payee, a SA valeur et a SA date d'ACHAT (le jour ou la taxe frappe, pas
    # celui du signal, la veille : superviseur R-759, C11) ; le point mort est la MOYENNE de ces
    # points morts sur les operations jugees (`point_mort_des_operations`). Jusque-la, le pire
    # cas des valeurs achetees au bareme du dernier achat (`point_mort_pire_cas`, garde pour
    # comparaison).
    pm = J.point_mort_des_operations(tp, sl, ops, mod_pos, bareme)   # FRACTIONS, cf. Y1
    print("\n    ── JUGEMENT ─────────────────────────────────────────")
    print("    POINT MORT           {:.1f} %  ·  reussite {} %  ·  marge {:+.1f} pts"
          .format(pm, wr, wr - pm))
    print("    (point mort moyen des {} operations jouees, bareme {} : chacune a sa valeur et a sa date d'achat)"
          .format(n, bareme))

    # LES OBSERVATIONS INDÉPENDANTES SE MESURENT, ELLES NE SE COMPTENT PLUS PAR UN SEUIL DE SÉANCES (décision de
    # Jean-Luc du 01-11-2026 à 13h19, « 1 », n°106 : « A-304 S'APPLIQUE » ; R-505 ④ ; lot S_ep du 05-11-2026). L'ancien
    # appel regroupait les signaux distants de 5 séances ou moins en « épisodes » ; ce seuil fixe est retiré. Ce pas
    # AFFICHE la mesure ; la comparer au plancher (`plancher_observations`, lu dans la table de R-505) revient au juge
    # de la loi (lot JG), jamais à un nombre écrit ici. Une mesure impossible s'affiche INCONNUE, jamais comme un nombre.
    # LA MESURE EST CELLE DU CHEVAUCHEMENT RÉEL DES POSITIONS (lot S_ep, tour 2, 05-11-2026, avis du superviseur R-759
    # « ARRÊTER ET SIMPLIFIER ») : les paires d'opérations ouvertes en même temps, sans nombre de séances, sans règle à
    # choisir, sans test qui décide. Au tour 1, ce pas appelait la mesure avec la règle « prudente » écrite ici en dur et
    # renvoyait à la question Q-Sep1 ; règle et question sont SUPPRIMÉES. La probabilité sous le hasard est AFFICHÉE et
    # ne décide rien.
    # LE NOMBRE RETENU EST BORNÉ PAR LES PÉRIODES DISTINCTES (lot S_ep, tour 3, 05-11-2026, avis du superviseur R-759
    # « DE FOND ») : retenu = le plus petit des observations mesurées et de K, le nombre de positions deux à deux jamais
    # ouvertes en même temps, parce qu'une ressemblance à l'intérieur d'une même période ne peut pas se vérifier. La
    # ligne affiche les trois : retenu (ce que JG et n°107 liront), mesurées et K (affichés, ne décident pas).
    try:
        e = J.observations_independantes(ops)
        if e["n_observations"] is None:
            print("    OBSERVATIONS         INCONNUES : %s" % e["motif"])
        else:
            print("    OBSERVATIONS         {} operations . {:.1f} observations independantes retenues . groupes de "
                  "{:.2f} operation(s) . le plus petit de {:.1f} mesurees et {} periodes distinctes . {} paires de "
                  "positions ouvertes en meme temps . sous le hasard p = {} (affichee, ne decide pas ; A-304, n°106)"
                  .format(e["n_operations"], e["n_observations"], e["taille_des_groupes"],
                          e["observations_mesurees"], e["periodes_distinctes"],
                          e["paires_qui_se_chevauchent"],
                          "sans objet (aucune paire)" if e["p_hasard"] is None else "%.3f" % e["p_hasard"]))
    except Exception as ex:
        print("    OBSERVATIONS         non mesurees : %s" % ex)

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
        # LA FRONTIÈRE EST CELLE DE `frontiere_de_la_fiche`, LA SEULE FONCTION QUI L'ÉTABLIT (superviseur R-759 de la
        # mission TRI, 12-11-2026) : JOUER_LES_VERSIONS et le tri l'appellent aussi, et le tri refuse tout fichier
        # de résultats dont la frontière diffère. Même formule qu'avant : la frontière de C5 ne bouge pas.
        c = J.coupure_70_30(ops, _sea, horizon=_h_emb, frontiere=J.frontiere_de_la_fiche(fiche, seances, _bornes))
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
                                   horizon=_h_emb, point_mort_pct=pm)
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
    # nulle part. Depuis le 11-11-2026, elle rejoue des voisins par pas reguliers
    # (jamais plus au hasard) ; depuis le 12-11-2026, le critere est celui de
    # R-505 ⑩ : les 26 voisins a +-10 % doivent tous gagner, sinon DRAPEAU.
    # CE QU'ELLE DISTINGUE : une strategie posee sur une COLLINE tient encore
    # quand on bouge un peu ses reglages — le gain baisse sans disparaitre. Une
    # strategie posee sur une AIGUILLE s'effondre au premier pas de cote : elle
    # ne decrivait pas le marche, elle collait a un jeu de donnees precis.
    # ATTENTION AU COMPTAGE DES ESSAIS (A-226) : ces variantes sont des essais,
    # et elles doivent etre comptees comme tels.
    _echec_du_voisinage = None
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
              module de statistiques (`calculer_voisinage_sur_grille`), qui l'appelle une
              fois pour le centre et une fois par voisin (`grille_du_voisinage` : depuis le
              12-11-2026, chaque réglage à −10 %, 0, +10 %, croisés, R-505 ⑩ ; le 11-11-2026, la
              grille de la moulinette ; avant : cinq variations tirées au hasard à plus ou moins 10 %).
            ③ ENTRÉE — `p` : un dictionnaire de réglages fabriqué par `juger` à partir de la
              grille, portant `tp`, `sl` et, sauf durée « aucune », `horizon`.
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
              ① LES VARIANTES SONT DES ESSAIS ET NE SONT PAS ENCORE INSCRITES. Chaque appel
              rejoue une stratégie complète ; `juger` affiche leur nombre comme « NON
              INSCRITS », le registre des essais (A-226) n'existant pas au dépôt.
              ② UN HORIZON ARRONDI À ZÉRO PASSERAIT. L'arrondi porte sur le nombre reçu,
              sans borne basse : une variation qui ferait descendre l'horizon au-dessous
              d'une demi-séance donnerait zéro, et `jouer` ne produirait alors aucune
              opération, ce que la fonction rendrait comme un gain de zéro euro. La grille
              du voisinage (`COMMUN.grille_du_voisinage`, depuis le 12-11-2026 à ±10 %) ne garde
              aucune durée sous 1 séance, et rend des séances entières.
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
                barème des frais et des règles de sortie d'une position.
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
            # « aucune » ne varie pas : le voisinage ne bouge alors que l'objectif et la perte acceptée.
            f2["horizon"] = str(int(round(p["horizon"]))) if "horizon" in p else fiche["horizon"]
            # REGARD UNIQUE (R-505 ③) : le voisinage ne passe aucun reçu — refus dans la fenêtre.
            o2, _ = jouer(f2, cours, mnemo, mod_pos_sig[0], mod_pos,
                          periode=_bornes, lecture=lecture)
            r2 = resumer(o2)
            return {"net": r2.get("net", 0.0), "wr": r2.get("wr", 0.0)}
        # LE DRAPEAU « VOISINAGE » DE R-505 ⑩, PAR PAS RÉGULIERS, JAMAIS AU HASARD (décision de Jean-Luc du 11-11-2026 à
        # 19h08 ; BACKLOG A-220). R-505 ⑩ [CHOIX DÉLÉGUÉ DÉL-D13, DÉL-D36] : « les 26 voisins à ±10 % de chaque réglage
        # doivent tous gagner » ; un drapeau arrête la stratégie et la soumet à Jean-Luc, ce n'est pas un échec du juge.
        # Les valeurs voisines viennent de `voisins` (COMMUN.py, la même que la moulinette, R-708) ; les réglages, de
        # VOISINAGE_DU_JUGE.csv.
        if racine is None:
            raise RuntimeError("racine du dépôt non transmise : réglages du voisinage introuvables")
        import COMMUN as GRILLE
        _rv = GRILLE.lire_reglages_du_voisinage_du_juge(
            os.path.join(racine, "donnees", "combinatoires", "VOISINAGE_DU_JUGE.csv"))
        # Les voisins se calculent en POURCENTS ; `_rejouer` reçoit des FRACTIONS, comme la fiche lue.
        _centre = {"tp": round(tp * 100, 4), "sl": round(sl * 100, 4)}
        if h is not HORIZON_AUCUNE:
            _centre["horizon"] = float(h)
        _g = GRILLE.grille_du_voisinage(_centre, _rv["bougent"], _rv["amplitude_relative"],
                                        _rv["pas_de_part_et_d_autre"], _rv["croisement"], _rv["arrondi_de_la_duree"])
        _en_fractions = lambda j: dict(j, tp=round(j["tp"] / 100, 6), sl=round(j["sl"] / 100, 6))
        st = S.calculer_voisinage_sur_grille(
            _rejouer, _en_fractions(_centre), [_en_fractions(j) for j in _g["jeux"]],
            _rv["gain_net_de_chaque_voisin_doit_depasser"], inscrire=None)
        _bougent = [p for p in _rv["bougent"] if p in _centre]
        print("    VOISINAGE            {} voisin(s) a +-{:g} % de chaque reglage ({} ; {} pas de part et d'autre ; {} ; R-505 ⑩)"
              .format(st["n_voisins"], _rv["amplitude_relative"], " ".join(_bougent) or "aucun reglage",
                      _rv["pas_de_part_et_d_autre"], _rv["croisement"]))
        for _p in _rv["bougent"]:
            if _p not in _centre:
                print("      ne bouge pas       %s : duree « aucune »" % _p)
        for _c in _g["confondus"]:
            print("      CONFONDUS          %s" % _c)
        _seuil = _rv["gain_net_de_chaque_voisin_doit_depasser"]
        if st["verdict"] is None:
            print("      verdict            NON MESURE — %s" % st["motif_non_mesure"])
        else:
            print("      gain des voisins   de {:+,.0f} a {:+,.0f} EUR · centre {:+,.0f} EUR"
                  .format(st["net_min_voisins"], st["net_max_voisins"], st["net_base"]).replace(",", " "))
            print("      ecart relatif      %s (information, ne decide pas)"
                  % ("%.0f %%, centre compris" % (100 * st["ecart_relatif"]) if st["ecart_relatif"] is not None
                     else "indefini (gain moyen nul)"))
            if st["verdict"] == "PASSE":
                print("      verdict            PASSE — les {} voisins gagnent (chacun au-dessus de {:+,.0f} EUR)"
                      .format(st["n_voisins"], _seuil).replace(",", " "))
            else:
                print("      verdict            DRAPEAU « voisinage » — {} voisin(s) sur {} ne depasse(nt) pas {:+,.0f} EUR ;"
                      " la strategie est soumise a Jean-Luc : forcage trace ou archive (R-505 ⑩)"
                      .format(len(st["perdants"]), st["n_voisins"], _seuil).replace(",", " "))
                for _d in st["perdants"]:
                    _q = _d["params"]
                    print("        perdant          TP {:+.2f}% . SL -{:.2f}% . horizon {} : {:+,.0f} EUR"
                          .format(100 * _q["tp"], 100 * _q["sl"],
                                  "%d seances" % int(_q["horizon"]) if "horizon" in _q else "aucune",
                                  _d["net"]).replace(",", " "))
        if _rv["provisoires"]:
            print("      reglages PROVISOIRES, A DECIDER PAR JEAN-LUC : %s (VOISINAGE_DU_JUGE.csv, colonne question)"
                  % ", ".join(_rv["provisoires"]))
        print("      essais             %d joue(s), %d NON INSCRIT(S) : le registre des essais n'existe pas au depot (A-226)"
              % (st["n_voisins"], st["essais_non_inscrits"]))
    except Exception as ex:
        # UN VOISINAGE QUI N'A PAS PU TOURNER N'EST PAS « NON MESURÉ » (R-734 ; relecteur du 11-11-2026, D1) : rejeu en
        # panne, fichier de réglages absent, racine non transmise. Le rapport continue, puis `juger` lève à la fin :
        # `main` met la fiche EN ÉCHEC et sort en 1. « Aucun voisin » ou « gain moyen nul », eux, restent NON MESURÉ.
        _echec_du_voisinage = "%s : %s" % (type(ex).__name__, ex)
        print("    VOISINAGE            EN ÉCHEC — n'a pas pu tourner : %s" % _echec_du_voisinage)

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
        univ = [mnemo.get(m, cle_valeur(m)) for m in mnemoniques_de_l_univers(fiche["univers"])]
        univ = [v for v in univ if v in cours]
        for mode, lib in (("valeur", "l'ACTION au hasard"),
                          ("date", "les DATES au hasard")):
            # LE HASARD JOUE AVEC LA MÉCANIQUE DE LA STRATÉGIE ET SA RÈGLE D'ACHAT, SUR SA PÉRIODE (R-708 ; décision de
            # Jean-Luc du 28-10-2026 à 23h03 ; superviseur R-759) : jusque-là il tirait hors de l'indice, sur tout
            # l'historique, avec sa propre copie de l'achat-sortie.
            hz = J.etalon_hasard(ops, cours, univ, tp, sl, h, mod_pos,
                                 mode=mode, n_tirages=120,
                                 entree=lambda v, j: jouer_une_entree(v, cours[v], j, tp, sl, h, mod_pos, lecture,
                                                                      bareme),
                                 admis=lambda v, j: achat_admis(v, cours[v], j, lecture),
                                 periode=_bornes)
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
                # L'EFFECTIF JOUÉ SE DIT (relecture du 28-10-2026) : un tirage qui joue moins d'opérations que la stratégie
                # n'est pas comparable au même gain total.
                print("      operations jouees par tirage : %s a %s, pour %s reelles"
                      % (hz.get("jouees_par_tirage_min"), hz.get("jouees_par_tirage_max"), hz.get("operations_reelles")))
    except Exception as ex:
        print("    HASARD               non mesure : %s" % ex)
    print("    ─────────────────────────────────────────────────────")
    if _echec_du_voisinage:
        raise RuntimeError("le voisinage n'a pas pu tourner (R-734) : %s" % _echec_du_voisinage)


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
      de sortie. LES POSITIONS ENCORE OUVERTES À LA FIN DES DONNÉES (motif
      `FIN_DES_DONNEES`, versions sans durée maximale) n'entrent dans AUCUNE de ces
      cases : quand il y en a, une case de plus, `fin_des_donnees`, porte leur
      nombre (`n`) et leur gain ou perte du moment en euros (`net`, arrondi au
      centime) ; sans elles, la sortie est exactement celle d'avant le 13-11-2026.
      Une liste faite seulement de telles positions rend le compte à zéro et cette
      case. Exemple réel, mesuré le 20-09-2026 sur la fiche `C5E10-QA-V1` :
      62 opérations, 71,0 % de réussite, +120 046,63 €, et les motifs
      `{'HORIZON': 2, 'SL': 15, 'SL_GAP': 3, 'TP': 33, 'TP_GAP': 9}` — avant le
      28-09-2026 ; depuis que la séance d'achat compte (R-608), 62 opérations,
      66,1 % de réussite, +98 930,83 €.
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ mettre à part les opérations `FIN_DES_DONNEES` (décision de
      Jean-Luc du 12-11-2026 à 09h18) · ① rendre le compte à zéro si la liste
      restante est vide · ② compter les
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
    # LES POSITIONS ENCORE OUVERTES À LA FIN DES DONNÉES SONT MISES À PART (décision de Jean-Luc du jeu 12-11-2026 à
    # 09h18, « 1 » : « On les met à part : exclues du total, affichées séparément avec leur nombre et leur gain ou perte
    # du moment ») : hors du compte, de la réussite et du total ; rendues dans une case à elles. Sans elles, la sortie
    # est identique à celle d'avant (le golden, à durée chiffrée, n'en a aucune).
    ouvertes = [o for o in ops if o["motif"] == MOTIF_FIN_DES_DONNEES]
    ops = [o for o in ops if o["motif"] != MOTIF_FIN_DES_DONNEES]
    a_part = ({"fin_des_donnees": {"n": len(ouvertes), "net": round(sum(o["net"] for o in ouvertes), 2)}}
              if ouvertes else {})
    if not ops:
        return dict({"n": 0}, **a_part)
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
            "motifs": dict(sorted(motifs.items())), **a_part}


# LE SIGNAL DU CALIBRAGE (A-542, 30-10-2026) : le calibrage rejoue la stratégie de référence du golden, C5-ETENDU-10,
# et le golden nomme lui-même le module qui l'a produit (`meta.module`). Ce n'est PAS un repli pour les fiches : seule
# la fiche de calibrage, construite par `calibrer`, porte ces trois valeurs, et elles passent par `signal_de_la_fiche`
# comme toute fiche. `calibrer` refuse si le module nommé ici n'est pas celui que le golden déclare.
SIGNAL_DU_CALIBRAGE = {"module_signal": "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py",
                       "fonction_signal": "signaux_c5etendu10", "reglages_signal": ""}


def calibrer(cours, mnemo, base, mod_positions, golden, f_cours=None, table=None):
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
      la table des codes courts · `base` : la racine du dépôt, où `signal_de_la_fiche` trouve
      le module de signal nommé par `SIGNAL_DU_CALIBRAGE` (avant le 30-10-2026 : le module de
      signal lui-même, chargé par `main` sous le motif « MODULE_C5_ETENDU_10 ») · `mod_positions` :
      le module de positions · `golden` : le contenu du fichier de chiffres figés,
      déjà lu · `f_cours` : le chemin du fichier de cours employé, pour en vérifier
      l'empreinte, `None` si l'appelant n'en donne pas. Mesuré le 20-09-2026,
      `main` passe le témoin du golden quand son empreinte est conforme, et le
      fichier de cours vivant sinon. `table` (depuis le 28-09-2026) : le chemin du
      tableau de référence des 100 trades, que `main` passe quand il calibre sur le
      témoin du golden, `None` sinon.
    ④ CONDITIONS D'ENTRÉE — Le golden doit porter une entrée `C5-ETENDU-10` avec
      sa comptabilité « jetons illimités », et le PREMIER MOT de son `meta.module`
      doit être ÉGAL au nom du fichier nommé par `SIGNAL_DU_CALIBRAGE` (le golden
      porte « MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py (inchange) » ; un chemin
      « programmes/MODULE_… » y ferait échouer le calibrage, ⑨ consigné). Ce module doit exposer la
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
      ⑤ (RÉPARÉ LE 30-10-2026, A-542) Le nom de la fonction de signal était écrit ici,
      réécrit dans `main` et dans `programmes/JUGER_SUR_8_CRITERES.py`. Il n'est plus
      écrit qu'ici, dans `SIGNAL_DU_CALIBRAGE`, pour la seule fiche de calibrage, et
      confronté au module que le golden déclare. Restent deux écritures du NOM DU
      FICHIER du module, celle-ci et `meta.module` du golden : c'est voulu, la seconde
      contrôle la première.
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
      arriverait si la période composée ici devenait illisible. Un signal
      introuvable rend un refus (faux et une ligne), il ne lève pas. Et un de ses appels peut ne pas
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
        barème des frais et des règles de sortie d'une position.
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
    # LE MODULE DU CALIBRAGE EST CELUI QUE LE GOLDEN DÉCLARE (A-542, 30-10-2026), et il passe par la lecture unique.
    # (Le chemin se lit sur le signal rendu, jamais dans le dictionnaire : les colonnes du signal ne se lisent que dans
    # `manques_du_signal` et `signal_de_la_fiche`, ce que l'épreuve du signal nommé vérifie.)
    try:
        _sig_cal = signal_de_la_fiche(base, dict(SIGNAL_DU_CALIBRAGE, id="calibrage"))
    except ValueError as _e:
        return False, ["    " + str(_e)]
    _mod_golden = str((golden.get("meta", {}) or {}).get("module") or "").split(" ")[0]
    _mod_cal = os.path.basename(_sig_cal.chemin)
    if _mod_golden != _mod_cal:
        return False, ["    le golden declare le module %r, le calibrage nomme %r : rien n'est calibre"
                       % (_mod_golden or "(aucun)", _mod_cal)]
    fiche = {"tp": "+4.0%", "sl": "-2.5%", "horizon": "20",
             # C5 achète à l'ouverture du lendemain et ne lit que les cours (points 5 et 9, 31-10-2026)
             "entree": "Open J+1", "donnees_demandees": "cours",
             "univers": ",".join(getattr(_sig_cal.module, "C5E10_UNIVERS", [])),
             "indicateurs": "calibrage",
             # UNE BORNE OUVERTE S'ECRIT AVEC UNE VRAIE DATE. « 0000-00-00 »
             # n'existe pas dans le calendrier, et la porte 0 le refuse depuis
             # qu'elle valide les dates — elle a raison. On prend donc la
             # premiere seance de l'historique, qui est la vraie borne basse.
             "periode": (min(min(b["date"] for b in s) for s in cours.values())
                         + " -> " + fin)}
    fiche.update(SIGNAL_DU_CALIBRAGE)
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
    # LE BARÈME JOUÉ ET LE BARÈME AFFICHÉ SONT LA MÊME VARIABLE (superviseur R-759, tour 3, 29-10-2026) : le texte
    # disait « ici le bareme reel » alors que `jouer`, appelé sans barème, prend le barème des verdicts
    # (REEL depuis la décision de Jean-Luc du 29-10-2026 à 19h16, HIST_COURTAGE_SANS_TTF avant) — une réparation (D2)
    # avait rendu la phrase fausse.
    _bareme_cal = bareme_des_verdicts(None, mod_positions)
    # REGARD UNIQUE (R-505 ③) : le calibrage ne passe aucun reçu — refus dans la fenêtre (J3 en attente de Jean-Luc :
    # un calibrage compte-t-il comme regard ?).
    ops, _ = jouer(fiche, cours, mnemo, _sig_cal, mod_positions,
                   periode=_bornes0, bareme=_bareme_cal)
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
                  "le bareme de frais (ici le bareme {}, A-550 ; forfait de 300 EUR au golden) ; "
                  "les sorties, elles, se comparent une a une ci-dessous.".replace("%%", "%").format(
                      r.get("net"), ref.get("net"), r.get("net") - ref.get("net"), _bareme_cal))
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
    ④ CONDITIONS D'ENTRÉE — Trois fichiers doivent exister sous la racine : le
      registre des stratégies, les cours et le module de positions. Depuis le
      30-10-2026 (A-542), le module de signal n'est plus cherché ici : chaque fiche
      nomme le sien, et une fiche dont le module est introuvable est refusée à la
      porte 0, sans arrêter les autres. Une fiche qui passe la porte 0 mais dont le
      JEU ou le JUGEMENT lève (par exemple un réglage de mauvaise valeur, graine
      « 7 » en texte) est mise « EN ÉCHEC », ce qui n'est pas un refus, et les
      fiches suivantes sont jugées (superviseur R-759 du 31-10-2026). Les cours sont ceux du fichier maître, `donnees/cours_maitre.csv` :
      s'il manque, le juge des stratégies s'arrête (A-442). Le référentiel des valeurs, le golden,
      le module de jugement et le module de statistiques peuvent manquer ; le
      rapport est alors plus pauvre, et il le dit pour le module de jugement.
    ⑤ SORTIE — UNE valeur : un entier passé à la sortie du processus. 0 quand le
      rapport est allé au bout, et 0 aussi quand aucune fiche n'était recevable,
      ce qui n'est pas un échec mais la porte 0 qui fait son travail. 1 quand un
      fichier indispensable manque, 1 quand le calibrage échoue, et 1 quand une
      fiche au moins est « EN ÉCHEC » : un contrôle qui n'a pas pu tourner ne rend
      pas 0 (R-734).
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher la version et l'heure de Paris · ② relever les sept
      fichiers par leur nom réel · ③ alerter si l'un des trois noms surveillés
      répond sous plusieurs graphies · ④ afficher chaque fichier avec son empreinte
      · ⑤ désigner le fichier maître des cours par `fichiers_de_cours`, et
      s'arrêter s'il manque · ⑥ s'arrêter si un fichier indispensable manque · ⑦ charger les cours,
      la table des mnémoniques et les trois modules (positions, jugement,
      statistiques) · ⑧ lire le registre des
      stratégies par `fiches_du_registre` du contrat — une fiche par identifiant,
      sa DERNIÈRE ligne (n°83, depuis le 05-11-2026) — et n'y garder que les
      fiches à l'état LABO ou QA · ⑨ passer chaque
      fiche restante par la porte 0, puis lire le signal qu'elle nomme
      (`signal_de_la_fiche`, A-542) et la refuser s'il est introuvable, et afficher
      le verdict ligne à ligne ·
      ⑩ calibrer l'instrument sur le témoin du golden si son empreinte est conforme,
      sur le fichier vivant sinon, et s'arrêter si le calibrage échoue · ⑪ pour
      chaque fiche recevable, afficher ses réglages et son signal, la jouer avec CE
      signal, la résumer, compter
      ses sorties sur saut, puis appeler le jugement ; une fiche dont le jeu ou le
      jugement lève (`SystemExit` compris) est mise « EN ÉCHEC » et la suivante est
      jugée ; depuis le 31-10-2026, une fiche dont le signal est refusé au jeu
      (`SignalRefuse` : sortie mal formée) est dite « REFUSÉE
      AU JEU », ce qui n'est pas une panne et ne change pas le code ; et chaque
      fiche jouée affiche, sous la ligne de son signal, « filtres non joués : »
      suivi du texte de sa colonne `filtres` quand elle n'est pas vide (décision de
      Jean-Luc du 31-10-2026 à 17h15, QJ-17) · ⑫ rappeler que le juge des stratégies ne conclut pas, lister les fiches
      EN ÉCHEC et rendre 1 s'il y en a.
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
      ⑤ TROIS NOMS SONT SURVEILLÉS CONTRE LES GRAPHIES MULTIPLES, NEUF SONT
      CHERCHÉS. La boucle d'alerte porte sur le registre des stratégies, les cours
      et le module de positions (le module de signal en est sorti le 30-10-2026 :
      chaque fiche le nomme par son chemin exact, A-542). Le golden, son témoin, le
      référentiel des valeurs, les cours du jour, le module de jugement et le module
      de statistiques ne sont pas surveillés : un doublon sur l'un d'eux serait
      tranché en silence.
      ⑥ LE CALCUL D'EMPREINTE DU TÉMOIN EST REFAIT À LA MAIN. La fonction
      `empreinte` existe dans ce même fichier et fait exactement cela ; ce passage
      réimporte la bibliothèque et recalcule. Relevé le 20-09-2026 :
      `hexdigest()[:16]` apparaît 3 fois, l'appel `empreinte(` 2 fois.
      ⑦ (RÉPARÉ LE 30-10-2026, A-542) Le nom de la fonction de signal était écrit ici
      en clair, `signaux_c5etendu10`, et imposé à toute fiche. Le registre porte
      désormais `module_signal`, `fonction_signal` et `reglages_signal`, lus par
      `signal_de_la_fiche` seule ; une fiche sans signal nommé est refusée.
      ⑧ LE GOLDEN EST LU SANS PROTECTION. Le fichier est ouvert et décodé
      directement ; un fichier tronqué ou mal formé arrêterait le programme sur une
      erreur brute, alors que tout le reste de cette fonction traite l'absence d'un
      fichier comme une situation prévue.
    ⑩ EFFET — N'ÉCRIT AUCUN FICHIER et ne touche pas au réseau : `git status` reste
      vide après un passage complet sur une copie du dépôt, mesuré le 20-09-2026.
      Elle LIT sept fichiers, EXÉCUTE le code des modules Python chargés
      depuis le disque (positions, jugement, statistiques, et le module de signal
      nommé par chaque fiche recevable), et AFFICHE le rapport : 167 lignes mesurées le 20-09-2026
      sur un passage complet.
    ⑪ TERMINAISON — Rend la main avec 0 ou 1 dans le cas normal. Une erreur levée
      par `jouer` ou `juger` pour UNE fiche, `SystemExit` compris, est rattrapée : la
      fiche est « EN ÉCHEC », les suivantes sont jugées, le code final est 1. Un module
      de signal non déclaré, illisible, ou qui lève ou sort au chargement est REFUSÉ à
      la porte 0 (`signal_de_la_fiche`), sans arrêter les autres. PEUT LEVER des
      erreurs non rattrapées qui arrêtent alors le programme : sur une fiche dont la
      période est mal formée, mesuré le 20-09-2026 — défaut ANTÉRIEUR au lot L3,
      `porte_0` rendant deux valeurs au lieu de trois (son ⑤), consigné au BACKLOG ; sur une fiche passée qui
      arriverait sans bornes, ce que le code signale lui-même et qui reste HORS de
      l'enveloppe, parce qu'elle dit une incohérence du juge et non de la fiche ;
      sur un fichier indispensable illisible ; et sur un golden mal formé. Et un de ses appels peut
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
        barème des frais et des règles de sortie d'une position.
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
    _args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = _args[0] if _args else "/mnt/project"
    cible = _args[1] if len(_args) > 1 else None
    # --cours=<fichier, relatif à la racine> : juger sur un autre fichier de cours que le maître, par exemple
    # l'historique des 20 ans (A-577, étape 1). Sans l'option, le maître, comme avant.
    _autre = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--cours=")), None)
    print("JUGE DES STRATÉGIES . %s . %s\n" % (VERSION, horodatage()))
    # UNE OPTION INCONNUE OU MAL ÉCRITE ARRÊTE TOUT (relecture et superviseur du 27-10-2026) : « --cours fichier »,
    # sans « = », était ignoré, et « fichier » devenait la fiche visée — aucune fiche jugée, code 0.
    _mal = [a for a in sys.argv[1:] if a.startswith("--") and not (a.startswith("--cours=") and len(a) > len("--cours="))]
    if _mal:
        print("ARRET : option inconnue ou mal ecrite : %s (seule « --cours=<fichier> » existe). Rien n'est juge." % _mal)
        return 1

    # LE JUGE DES STRATÉGIES LIT LE REGISTRE DES STRATEGIES, PLUS LE SAS.
    # Le sas — registre_candidates.csv — a ete ABSORBE le 29-08-2026 : il
    # dupliquait sept colonnes du registre (id, nom, indicateurs, univers,
    # filtres, tp, sl, horizon) sous d'autres identifiants, sans qu'aucune
    # colonne ne relie les deux fichiers. Le lien se reconstruisait par
    # RESSEMBLANCE DE NOMS — exactement ce que le chapitre IDENTITE DES VALEURS
    # interdit, et qui a coute 26 % d'une mesure le 23/08.
    # Un objet, un nom, un registre, de la naissance a la mort.
    # LE NOM DU REGISTRE ET SA LECTURE VIVENT AU CONTRAT (n°83, 05-11-2026) : ce programme le cherche par son nom,
    # écrit une fois dans programmes/CONTRATS_DES_FICHIERS.py, et le lit par `fiches_du_registre` (la dernière ligne
    # d'un identifiant fait foi). Importé ici, au moment de lire, pour que les programmes qui chargent le juge comme
    # une bibliothèque (le soir, la moulinette, les épreuves) n'en dépendent pas.
    from CONTRATS_DES_FICHIERS import NOM_DU_REGISTRE_DES_STRATEGIES, fiches_du_registre
    f_sas = trouver(base, NOM_DU_REGISTRE_DES_STRATEGIES)
    # LES COURS VIENNENT DU SEUL FICHIER MAITRE, designe par `fichiers_de_cours` :
    # une seule facon de le trouver dans tout le systeme (A-442, R-708).
    try:
        f_cours = os.path.join(base, _autre) if _autre else fichiers_de_cours(base)[0]
    except FileNotFoundError as _e:
        print(_e)
        return 1
    f_ref = trouver(base, "REFERENTIEL_VALEURS")
    # LE MODULE DE SIGNAL N'EST PLUS CHERCHÉ ICI (A-542, 30-10-2026) : chaque fiche nomme le sien, par son chemin exact,
    # et `signal_de_la_fiche` le charge. Avant, le motif « MODULE_C5_ETENDU_10 » l'imposait à toutes les fiches.
    f_pos = trouver(base, "MODULE_POSITIONS.py")
    f_gold = trouver(base, "golden_tests_")

    # UN NOM QUI REPOND DEUX FOIS EST UNE ALERTE, jamais un choix silencieux.
    for _lib, _mot in (("le registre des strategies", NOM_DU_REGISTRE_DES_STRATEGIES),
                       ("les cours", "cours_maitre.csv"),
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
                    ("module de positions", f_pos),
                    ("chiffres figes", f_gold)):
        if ch:
            print("  %-22s %-46s %s" % (lib, os.path.basename(ch), empreinte(ch)))
        else:
            print("  %-22s INTROUVABLE" % lib)
    print()

    manquants = [l for l, c in (("registre des strategies", f_sas), ("cours", f_cours),
                                ("module de positions", f_pos)) if not c]
    if manquants:
        print("ARRET : introuvable - %s. Rien n'est produit." % ", ".join(manquants))
        return 1

    mnemo = table_mnemoniques(f_ref)
    # LES COURS PASSENT PAR LE LECTEUR UNIQUE (A-577, étape 1, 26-10-2026) : avec eux, les périodes de chaque
    # valeur dans le CAC 40 et ses trous. Une lecture qui a dû mettre des lignes à part ne juge rien.
    try:
        cours, lecture = lire_par_le_lecteur(base, os.path.relpath(f_cours, base), mnemo)
    except ValueError as _e:
        if not str(_e).startswith("le lecteur unique"):
            raise
        print("ARRET : %s" % _e)
        return 1
    # LE COMPTE VIENT DES MORCEAUX QUE REND `couper_aux_trous`, la règle même de la coupure (R-708) : compter les
    # séances sans cours d'une valeur, c'était compter aussi celles d'avant sa première séance et d'après sa
    # dernière, qui ne coupent rien (relecture du 27-10-2026 : 5 615 comptées, 221 coupaient une série).
    _morceaux = {v: couper_aux_trous(s, lecture["trous"].get(v, [])) for v, s in cours.items()}
    _coupures = sum(len(m) - 1 for m in _morceaux.values())
    _enjambees = sum(1 for v, m in _morceaux.items() for i in range(1, len(m)) for d in lecture["trous"].get(v, [])
                     if m[i - 1][-1]["date"] < d < m[i][0]["date"])
    print("LECTURE : par le lecteur unique ; achats limites aux valeurs du CAC 40 le jour de l'achat ;"
          " %d coupures des series, sur %d seances sans cours" % (_coupures, _enjambees))
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
    # UNE FICHE PAR IDENTIFIANT, SA DERNIÈRE LIGNE (décision de Jean-Luc n°83, 01-11-2026 à 12h33 : « La dernière
    # ligne ajoutée fait foi. Les précédentes restent comme historique. ») ; avant le 05-11-2026, chaque ligne était
    # jugée, l'ancienne ligne de C5-EI-PARAMS comprise (refusée à la porte 0).
    fiches = list(fiches_du_registre(f_sas).values())
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
            # LE SIGNAL NOMMÉ SE LIT DÈS LA PORTE (A-542, 30-10-2026) : un module ou une fonction introuvable refuse la
            # fiche ici, avec son motif, au lieu de lever au milieu du jeu.
            try:
                f["_signal"] = signal_de_la_fiche(base, f)
            except ValueError as _e:
                ok, manq = False, [str(_e)]
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
        ok, lignes = calibrer(_cours_cal, mnemo, base, mod_pos, golden, _f_cal, _f_tab)
        print("CALIBRAGE DE L'INSTRUMENT (9bis) - rejoue C5-ETENDU-10 :")
        for l in lignes:
            print(l)
        if not ok:
            print("\n  ARRET TOTAL : l'instrument n'est pas calibre, rien n'est juge.")
            return 1
        print("  -> OK, l'instrument est calibre.\n")

    if cible and not any(f["id"] == cible for f in passees):
        # Une fiche visée qui n'existe pas, ou que la porte 0 refuse, ne se juge pas en silence (R-734, superviseur
        # du 27-10-2026) : une faute de frappe dans l'identifiant rendait 0 sans rien juger.
        print("ARRET : la fiche visee %s n'est pas parmi les fiches qui passent la porte 0. Rien n'est juge." % cible)
        return 1
    # UNE ERREUR AU CHARGEMENT DU SIGNAL, AU JEU OU AU JUGEMENT D'UNE FICHE N'ARRÊTE PAS LES SUIVANTES (superviseur R-759
    # du 31-10-2026, I1 ; tour 3 : `SystemExit` compris). Une fiche qui passe la porte 0 peut encore lever au jeu — un
    # réglage de mauvaise VALEUR, graine « 7 » en texte, que `bind` ne voit pas. Elle est mise « EN ÉCHEC », ce qui n'est
    # pas un refus (un refus dit qu'un champ manque), les suivantes sont jugées, et le code final est 1 (R-734).
    # CE QUI ARRÊTE ENCORE TOUT, ET C'EST ANTÉRIEUR AU LOT : une période mal formée, parce que `porte_0` rend alors deux
    # valeurs au lieu de trois (son ⑤ ; consigné au BACKLOG) ; et une fiche sans bornes après la porte, voulu. Mesuré par le superviseur : sans cette enveloppe, une telle fiche placée en tête
    # du registre arrêtait le juge, et aucune des trois fiches C5 n'était jugée.
    en_echec = []
    for f in passees:
        if cible and f["id"] != cible:
            continue
        # LE SIGNAL JOUÉ EST CELUI QUE LA FICHE NOMME, LU À LA PORTE (A-542, 30-10-2026) — plus aucun repli vers C5.
        mod_sig = f["_signal"]
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
        try:
            # REGARD UNIQUE (R-505 ③) : `main` n'inscrit rien, donc ne passe aucun reçu — refus dans la fenêtre.
            ops, inconnus = jouer(f, cours, mnemo, mod_sig, mod_pos, periode=_bornes, lecture=lecture)
        except SignalRefuse as _refus_au_jeu:
            # UN REFUS NOMMÉ, PAS UNE PANNE (point 8 du plan du juge, 31-10-2026) : sortie du signal mal formée. La fiche
            # n'est pas jugée ; ce n'est pas « EN ÉCHEC », le code ne change pas.
            print("    REFUSÉE AU JEU (ce n'est pas une panne) : %s\n" % _refus_au_jeu)
            continue
        except (Exception, SystemExit) as _ex_jeu:
            en_echec.append(f["id"])
            print("    EN ÉCHEC (ce n'est pas un refus) : %s : %s\n" % (type(_ex_jeu).__name__, _ex_jeu))
            continue
        if inconnus:
            print("    ALERTE - valeurs demandees et absentes des cours : %s" % inconnus)
        r = resumer(ops)
        # LE SIGNAL JOUÉ SE DIT, APRÈS LE RÉSULTAT (A-542) : la ligne du résultat reste à sa place, trois lignes au plus
        # après « === » — tests/EPREUVES_DU_JUGE_PAR_LE_LECTEUR (M3) et la moulinette la lisent là.
        _ligne_signal = "    signal : %s . empreinte du module %s" % (mod_sig.declaration, empreinte(mod_sig.module.__file__))
        # LES FILTRES SE DISENT, ILS NE SE JOUENT PAS (décision de Jean-Luc du 31-10-2026 à 17h15, QJ-17) : la colonne
        # `filtres` reste un texte affiché ; chaque verdict écrit ce qui n'a pas été joué.
        _filtres = (f.get("filtres") or "").strip()
        if _filtres.lower() not in VIDE:
            _ligne_signal += "\n    filtres non joués : %s" % _filtres
        # LES POSITIONS ENCORE OUVERTES À LA FIN DES DONNÉES SE DISENT À PART, APRÈS LE RÉSULTAT (décision de Jean-Luc du
        # 12-11-2026 à 09h18 : « affichées séparément avec leur nombre et leur gain ou perte du moment ») ; `resumer`
        # les a déjà sorties du total.
        if "fin_des_donnees" in r:
            _ligne_signal += ("\n    à part, hors du total : %d position(s) encore ouverte(s) à la fin des données . "
                              "gain ou perte du moment {:+,.2f} EUR".format(r["fin_des_donnees"]["net"])
                              % r["fin_des_donnees"]["n"])
        if r["n"] == 0:
            print(_ligne_signal)
            print("    aucune operation produite.\n")
            continue
        print("    {} operations . {} % de reussite . {:+,.2f} EUR".format(
              r["n"], r["wr"], r["net"]))
        print(_ligne_signal)
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
            try:
                juger(f, ops, cours, seances, mod_jug, mod_stats, mod_pos, mnemo,
                      _bornes, (mod_sig,), lecture=lecture, racine=base)
            except (Exception, SystemExit) as _ex_jugement:
                en_echec.append(f["id"])
                print("    EN ÉCHEC (ce n'est pas un refus) : %s : %s\n"
                      % (type(_ex_jugement).__name__, _ex_jugement))
                continue
        print()

    print("Pas de verdict oui / non : la grille qui le rendra (A-210) n'est pas encore figée.")
    if en_echec:
        print("FICHES EN ÉCHEC (%d) : %s — code de sortie 1 (R-734)" % (len(en_echec), ", ".join(en_echec)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
