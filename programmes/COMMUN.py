"""Rassemble les gestes partagés par plusieurs programmes : rapprocher deux
écritures d'un même nom, retrouver un fichier, lire une source ou dire qu'on n'a
pas pu, et lire la date écrite dans un nom de fichier.

① RÔLE — Servir de réserve de gestes communs, pour qu'un même travail ne soit pas
  réécrit dans chaque programme. Son nom ne dit ni ce qu'il fait ni sur quoi il
  agit, et ce défaut de nommage est déjà consigné au tableau des décisions du
  projet sous l'identifiant A-426 ; ce texte dit donc ce qu'il contient réellement.
  Il contient CINQ familles de gestes et rien d'autre :
  ① réduire deux écritures d'un nom de fichier à une seule clé — `norm` ;
  ② faire de même pour un nom d'entreprise cotée, en appliquant une table
  d'équivalences — `norm_valeur`, `ALIAS_VALEURS`, et `rapprocher` qui ramène un
  dictionnaire vers le vocabulaire de celui qui appelle ;
  ③ retrouver le chemin réel d'un fichier sans supposer son nom, sous-dossiers
  compris — `trouver` et `trouver_tous` ;
  ④ lire un fichier texte ou un fichier de tableau, en distinguant « je n'ai pas
  pu lire » de « il n'y a rien » — `lire`, `lire_csv` et la classe `Illisible` ;
  ⑤ lire la date écrite DANS un nom de fichier et désigner le plus récent d'une
  liste — `date_du_nom` et `le_plus_recent`.
  Une sixième fonction, `_calibrage`, rejoue des cas connus sur une partie de ces
  gestes.
② CONTEXTE D'APPEL — Quatre programmes l'importent, et TOUS LES QUATRE n'en
  prennent qu'une seule fonction, `le_plus_recent` : programmes/audit_ecosysteme.py
  ligne 193, programmes/COLLECTER_ABC_GITHUB.py ligne 305,
  programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py ligne 84 et
  programmes/GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py ligne 36. Deux d'entre eux
  tournent chaque soir sans intervention : le fichier de tâches planifiées
  .github/workflows/collecte_abc.yml lance la collecte à sa ligne 29 et le
  programme de surveillance à sa ligne 259. Ce fichier peut aussi être lancé
  directement, et il rejoue alors ses cas connus.
③ ENTRÉE — Aucune. Importé, il ne reçoit rien. Lancé directement, il ne lit aucun
  argument de la ligne de commande : tout ce qu'on lui passe est ignoré.
④ CONDITIONS D'ENTRÉE — Pour être importé, le dossier programmes/ doit figurer
  parmi les dossiers où Python cherche ses modules ; les quatre programmes qui
  l'importent l'y ajoutent eux-mêmes juste avant, chacun avec sa propre ligne.
  Aucun fichier, aucun réseau, aucun réglage n'est exigé au chargement.
⑤ SORTIE — Lancé directement : un code de sortie, 0 si les neuf cas connus passent,
  1 si l'un d'eux échoue. Mesuré le 19-09-2026 : les neuf passent, le programme
  affiche « CALIBRAGE OK. » et rend 0. Importé, il ne rend rien : il met à
  disposition dix fonctions, une classe et deux valeurs, `VERSION` et la table
  d'équivalences `ALIAS_VALEURS`.
⑥ TRAITEMENT — ① au chargement, préparer la table d'équivalences des noms
  d'entreprises et trois motifs de lecture de date · ② définir les dix fonctions et
  la classe · ③ si et seulement si le fichier est lancé directement, rejouer les
  neuf cas connus, les afficher un par un, et sortir sur leur verdict.
⑦ UNITÉ — Aucune grandeur physique. Ce qui se compte ici se compte en NOMBRE DE
  FICHIERS et en NOMBRE DE VALEURS. Les dates sont rendues sous forme de cinq
  nombres entiers, dans l'ordre année, mois, jour, heure, minute.
⑧ POURQUOI — Ce fichier a été écrit le 28-08-2026 pour RETIRER des implémentations,
  pas pour en ajouter une de plus. La mesure qui l'a déclenché, prise le même jour
  sur les neuf programmes qui lisaient des fichiers : deux seulement parcouraient
  les sous-dossiers, cinq rapprochaient les écritures d'un nom, un seul réunissait
  correctement les trois écritures d'UNIBAIL, et deux distinguaient une lecture
  ratée d'un fichier vide. Neuf programmes, quatre gestes communs, neuf façons de
  les faire. La cause n'était pas la négligence : chaque correctif avait été
  appliqué chez le programme qui l'avait révélé, et nulle part ailleurs. La règle
  du projet qui l'interdit est que deux implémentations d'une même chose divergent
  toujours (R-708) : on importe, on ne recopie pas.
  Rien ici n'a été inventé. Les deux fonctions de normalisation viennent de
  programmes/audit_ecosysteme.py, seul programme qui réunissait correctement les
  écritures d'UNIBAIL. La recherche de fichier et la classe `Illisible` viennent de
  programmes/claude_FABRIQUER_LE_PILOTE.py, seul programme qui descendait dans les
  sous-dossiers. On a rassemblé, on n'a pas récrit.
⑨ CE QUI CLOCHE —
  ① LE RETRAIT ANNONCÉ N'A PAS EU LIEU. Ce fichier dit exister pour supprimer huit
  implémentations concurrentes ; treize mois plus tard, neuf de ses dix fonctions
  n'ont AUCUN appelant hors de ce fichier, et les implémentations qu'elles
  devaient remplacer sont toujours là. Mesuré le 19-09-2026, en cherchant chaque
  nom dans tous les fichiers .py du dépôt : `norm` est redéfini dans
  programmes/CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py ligne 105 · `trouver`
  dans programmes/JUGE_DES_STRATEGIES.py ligne 168, dans
  programmes/claude_FABRIQUER_LE_PILOTE.py ligne 198 et, sous une autre forme,
  dans programmes/PROUVER_L_EXECUTION.py ligne 268 · `trouver_tous` dans
  programmes/JUGE_DES_STRATEGIES.py ligne 126 · `lire` dans
  programmes/claude_FABRIQUER_LE_PILOTE.py ligne 262, dans
  programmes/TENIR_L_HISTORIQUE.py ligne 191 et dans
  programmes/EPREUVES_DU_SOCLE.py ligne 187 · `lire_csv` dans
  programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py ligne 89 · et la
  classe `Illisible` dans programmes/claude_FABRIQUER_LE_PILOTE.py ligne 240. Le
  fichier écrit pour fermer la divergence vit donc À CÔTÉ d'elle, et l'a augmentée
  d'un exemplaire.
  ② DEUX TABLES D'ÉQUIVALENCES, CHACUNE SE DÉCLARANT LA SEULE. La table
  `ALIAS_VALEURS` de ce fichier porte au-dessus d'elle « LA SEULE TABLE D'ALIAS DU
  PROJET. À compléter ICI et nulle part ailleurs. » ; programmes/audit_ecosysteme.py
  porte aux lignes 211 à 214 une table de même nom, au contenu identique aujourd'hui,
  surmontée de « Table unique, à compléter ici et NULLE PART AILLEURS (R-708) ».
  Les deux sont vraies séparément et fausses ensemble : le jour où une entreprise
  change de nom, celui qui complète l'une des deux aura suivi la consigne écrite
  au-dessus, et l'autre table restera en arrière sans que rien ne le dise.
  ③ LA SEULE FONCTION QUE QUELQU'UN IMPORTE N'EST PAS ÉPROUVÉE. Les neuf cas connus
  rejoués par ce fichier portent sur `norm`, `norm_valeur`, `rapprocher`,
  `lire_csv` et `Illisible`. Ils ne touchent ni `trouver`, ni `trouver_tous`, ni
  `lire`, ni `date_du_nom`, ni `le_plus_recent`. Or `le_plus_recent` est la seule
  fonction que les quatre programmes importent, et programmes/audit_ecosysteme.py
  affirme pourtant en commentaire, lignes 189 et 190 : « La fonction vit dans
  COMMUN (R-708) et se calibre sur ce cas même. » Mesuré le 19-09-2026 : la sortie
  du fichier lancé directement affiche neuf lignes, aucune ne nomme
  `le_plus_recent`, et une recherche des mots `le_plus_recent`, `date_du_nom` et
  `REGISTRE` dans le corps de `_calibrage` ne rend aucune ligne. Le filet est
  tendu sous ce que personne n'emploie, et absent sous ce dont tout le monde
  dépend.
  ④ LA PREMIÈRE LIGNE DU FICHIER EST UN IMPORT, ET ELLE PRÉCÈDE LA LIGNE
  D'INTERPRÉTEUR. Le fichier commence par `from datetime import date as _date`,
  et la ligne `#!/usr/bin/env python3` vient seulement après. Une ligne
  d'interpréteur n'a d'effet qu'en toute première ligne : ici elle n'en a aucun, et
  le fichier ne peut pas être lancé comme un programme autonome — ses droits ne le
  permettent d'ailleurs pas non plus, `ls -l` rendant `-rw-r--r--` le 19-09-2026.
  Le même import écartait le texte d'en-tête de sa place : tant qu'une
  instruction précède un texte en tête de fichier, Python ne le tient pas pour le
  texte du programme, et programmes/PHOTOGRAPHIER.py — rangé aux archives le 24-09-2026, A-452 —, qui le demandait à Python, en
  recevait une valeur vide — le document archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md décrivait donc ce
  programme sans aucune ligne d'en-tête.
  ⑤ LE NUMÉRO DE VERSION EST ÉCRIT À DEUX ENDROITS. Le texte d'en-tête porte
  « v1.0 » et la ligne 55 porte `VERSION = "1.0"`. Un chiffre qui existe ailleurs
  ne se recopie pas (R-708) : une correction faite sur l'un laisse l'autre annoncer
  une version qui n'existe plus, et c'est le second qui s'affiche au lancement.
⑩ EFFET — Importé, il ne change rien : aucun fichier écrit, aucun accès réseau,
  aucune lecture au chargement. Lancé directement, il affiche douze lignes et
  n'écrit rien. Les fichiers ne sont LUS que si l'appelant appelle lui-même
  `trouver`, `trouver_tous`, `lire` ou `lire_csv`.
⑪ TERMINAISON — Importé, le chargement rend la main et rien ne s'exécute ensuite.
  Lancé directement, il SORT DU PROGRAMME avec le code 0 si les neuf cas passent,
  1 sinon. Et un de ses appels peut ne pas revenir : `_calibrage` appelle
  `rapprocher`, qui parcourt le dictionnaire reçu — un dictionnaire modifié pendant
  ce parcours ferait lever. Aucun cas de ce genre n'existe aujourd'hui.
⑫ DÉFINITIONS
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les
    fichiers du projet
  le rapprochement : le fait de reconnaître que deux écritures différentes
    désignent le même fichier ou la même entreprise
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
  l'exécutant : le service qui lance les programmes du soir sans intervention
    humaine
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
  la table d'équivalences : `ALIAS_VALEURS`, le dictionnaire de ce fichier qui dit quelle écriture courte désigne quelle écriture longue
"""
from datetime import date as _date
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCIDÉ · outil · v1.0 · 28-08-2026 · Rôle : les quatre gestes que TOUS les
programmes du projet partagent — trouver un fichier, normaliser un nom,
normaliser une valeur, lire une source ou crier.
Quand l'appeler : au début de tout programme qui lit des fichiers du projet.
Jamais recopier ce qu'il contient : on l'IMPORTE.

POURQUOI CE FICHIER EXISTE
    Mesure du 28-08-2026 sur les neuf programmes qui lisent des fichiers :

      parcourent les sous-dossiers ........ 2 sur 9
      rapprochent les graphies d'un NOM ... 5 sur 9
      réunissent les graphies d'UNIBAIL ... 1 sur 5
      distinguent illisible de vide ....... 2 sur 9

    Neuf programmes, quatre gestes communs, NEUF implémentations différentes.
    Et la cause n'est pas la négligence : **chaque correctif a été appliqué chez
    celui qui l'a révélé, et nulle part ailleurs.** `os.walk` existait depuis le
    26/08 chez le programme du pilote ; il a fallu deux jours pour l'apporter au
    juge des stratégies, et l'audit ne l'a toujours pas.

CE QUE CELA COÛTE AUJOURD'HUI, ET C'EST MESURÉ
    · Le maillon 10 de l'audit — le recalcul indépendant de chaque trade, le
      contrôle le plus important du radar — passe au VERT en annonçant « aucun
      trade clôturé, rien à contrôler », parce qu'il ne regarde pas dans le
      sous-dossier où vivent les trades. Il ne se voit pas grâce à un
      contournement écrit dans le PROMPT de la tâche : il tient tant que
      personne ne réécrit ce prompt.
    · L'audit dit « position conforme » sur UNIBAIL pendant que le service de
      mesure évalue sa variation latente à 0,00 € — il ne retrouve pas le cours,
      et rend zéro au lieu de crier. Deux chiffres, aucune alerte.
    · Le cockpit affiche « cours indisponibles » là où les cours existent, parce
      qu'il ne traite pas le tiret de UNIBAIL-RODAMCO-WESTFIELD.

CE QUE CE FICHIER N'EST PAS
    Ce n'est pas un dixième programme. C'est le RETRAIT de huit implémentations.
    Corriger neuf programmes ferait grossir le système ; en importer un le fait
    rétrécir. C'est R-708 appliquée : « ne jamais réécrire ce qui existe déjà ».

RIEN ICI N'EST INVENTÉ
    Les deux fonctions de normalisation sont reprises de `audit_ecosysteme.py`,
    seul programme qui réunit correctement les graphies d'UNIBAIL. La recherche
    de fichier est reprise du programme du pilote, seul à parcourir les
    sous-dossiers. La classe Illisible en vient aussi. On rassemble, on ne
    récrit pas.
"""

import csv
import os
import re

VERSION = "1.0"

# ─────────────────────────────────────────────────────────────────────────
# ① NORMALISER UN NOM DE FICHIER
# ─────────────────────────────────────────────────────────────────────────

def norm(s):
    """Rend une clé de comparaison où espaces, tirets et soulignés sont équivalents.

    ① RÔLE — Permettre à deux programmes qui écrivent le même nom différemment de
      reconnaître qu'il s'agit du même. C'est le geste de rapprochement le plus bas
      du fichier : tout ce qui compare des noms passe par lui, des deux côtés de la
      comparaison.
    ② CONTEXTE D'APPEL — Quatre appelants, tous dans ce fichier : `norm_valeur` avant
      d'appliquer la table d'équivalences, `trouver` et `trouver_tous` sur chaque nom
      de fichier rencontré et sur chaque motif cherché, et `_calibrage` pour rejouer
      ses cas connus. Aucun appel depuis un autre programme : mesuré le 19-09-2026,
      une recherche du mot `norm` dans tous les fichiers .py du dépôt ne rend, hors
      de ce fichier, que la définition d'une AUTRE fonction du même nom, dans
      programmes/CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py ligne 105.
    ③ ENTRÉE — `s` : le texte à réduire en clé. `norm_valeur` y passe sans le modifier
      le nom d'entreprise qu'elle a reçu, par exemple `UNIBAIL-RODAMCO-WESTFIELD` ;
      `trouver` et `trouver_tous` y passent tantôt un nom de fichier lu sur le
      disque, tantôt le motif cherché, par exemple `cac40_ohlcv.csv`.
    ④ CONDITIONS D'ENTRÉE — Aucune. N'importe quel objet est accepté : il est
      converti en texte avant tout traitement. Rien n'est exigé de l'appelant.
    ⑤ SORTIE — UNE valeur : un texte, toujours en minuscules, où toute suite
      d'espaces, de tirets et de soulignés est remplacée par un seul souligné.
      Mesuré le 19-09-2026 : `BUREAU VERITAS`, `BUREAU_VERITAS`, `Bureau Veritas` et
      `bureau-veritas` rendent tous les quatre `bureau_veritas`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir ce qui est reçu en texte · ② tout mettre en minuscules
      · ③ remplacer chaque suite d'espaces, de tirets et de soulignés par un unique
      souligné.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le même fichier apparaît avec des espaces chez l'un et des soulignés
      chez l'autre selon le canal par lequel il est lu : le service qui lance les
      programmes du soir voit une écriture, la conversation qui les rédige en voit
      une autre. AUCUNE des deux n'est « la bonne ». Un programme qui épellerait un
      nom serait donc faux pour l'un des deux lecteurs quoi qu'on écrive, et la règle
      du projet qui l'interdit dit qu'un nom se rapproche, il ne s'épelle pas (R-729).
      Le souligné a été retenu comme forme d'arrivée parce qu'il est le seul des
      trois séparateurs qui ne soit ni coupé ni échappé quand un nom voyage dans une
      adresse ou dans une ligne de commande.
    ⑨ CE QUI CLOCHE —
      ① UNE CASE ABSENTE DEVIENT UN NOM. Mesuré le 19-09-2026 : `norm(None)` rend le
      texte `none`, et `norm(0)` rend `0`. Une colonne vide d'un fichier de tableau
      ne produit donc pas une clé vide mais la clé `none` — et deux lignes à qui il
      manque le nom de l'entreprise portent alors la MÊME clé, ce qui les fait
      passer pour deux écritures d'une même valeur. Rien ne le signale.
      ② DEUX FONCTIONS DU DÉPÔT PORTENT CE NOM ET NE RENDENT PAS LA MÊME CLÉ. Celle
      de ce fichier met en minuscules et remplace les séparateurs par un souligné ;
      celle de programmes/CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py ligne 105 met
      en MAJUSCULES et SUPPRIME tout ce qui n'est ni lettre ni chiffre. Mesuré le
      19-09-2026 sur les mêmes textes : `BUREAU VERITAS` devient `bureau_veritas`
      ici et `BUREAUVERITAS` là-bas, ce qui n'est qu'une différence d'écriture ;
      mais `TOTAL ENERGIES` et `TOTALENERGIES` sont DEUX valeurs distinctes pour
      cette fonction-ci et UNE SEULE pour l'autre. Deux programmes du même dépôt ne
      répondent donc pas pareil à la question « est-ce la même entreprise ? », et
      deux implémentations d'une même chose divergent toujours (R-708).
      ③ LA SUPPRESSION DU SÉPARATEUR N'EST PAS TRAITÉE. `BUREAUVERITAS` écrit sans
      séparateur rend `bureauveritas`, mesuré le 19-09-2026, et ne rejoint donc pas
      `bureau_veritas`. Le rapprochement ne couvre que les noms dont les mots sont
      séparés d'une façon ou d'une autre, jamais ceux qui sont collés.
    ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau, aucune valeur
      extérieure modifiée. Elle lit ce qu'on lui donne et rend un texte neuf.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : tout objet est converti
      en texte avant d'être traité. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms
        et n'est jamais affiché à un lecteur
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
      l'exécutant : le service qui lance les programmes du soir sans intervention
        humaine
    
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      la table d'équivalences : `ALIAS_VALEURS`, le dictionnaire de ce fichier qui dit quelle écriture courte désigne quelle écriture longue
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return re.sub(r"[ \-_]+", "_", str(s).lower())


# ─────────────────────────────────────────────────────────────────────────
# ② NORMALISER UN NOM DE VALEUR
# ─────────────────────────────────────────────────────────────────────────

# LA SEULE TABLE D'ALIAS DU PROJET. À compléter ICI et nulle part ailleurs.
# Reprise de `audit_ecosysteme.py`, seul programme sur cinq à réunir les trois
# graphies d'UNIBAIL. Les quatre autres en font trois valeurs distinctes.
ALIAS_VALEURS = {
    "unibail_rodamco": "unibail_rodamco_westfield",
    "unibail": "unibail_rodamco_westfield",
}


def norm_valeur(s):
    """Rend la clé d'un nom d'entreprise, après application de la table d'équivalences.

    ① RÔLE — Faire d'un nom d'entreprise écrit de plusieurs façons une clé unique,
      pour qu'un cours, une position et un trade portant le même titre soient
      rapprochés au lieu d'être comptés comme trois entreprises différentes. C'est
      la seule porte par laquelle un nom de valeur entre dans une comparaison.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier : `rapprocher`,
      sur chaque nom attendu puis sur chaque nom reçu, et `_calibrage`, pour rejouer
      ses cas connus. Aucun appel depuis un autre programme : mesuré le 19-09-2026,
      une recherche du mot `norm_valeur` dans tous les fichiers .py du dépôt ne rend
      aucune ligne hors de ce fichier.
    ③ ENTRÉE — `s` : le nom d'entreprise à réduire en clé, tel qu'il est écrit dans
      le fichier d'où il vient. `rapprocher` y passe sans le modifier chaque nom
      attendu par son appelant, puis chaque clé du dictionnaire reçu, par exemple
      `UNIBAIL-RODAMCO-WESTFIELD` tel qu'il est écrit dans l'historique des cours.
    ④ CONDITIONS D'ENTRÉE — Aucune. N'importe quel objet est accepté et converti en
      texte. Rien n'est exigé de l'appelant.
    ⑤ SORTIE — UNE valeur : un texte, la clé. C'est la forme minuscule-et-soulignés
      du nom reçu, remplacée par la forme d'arrivée si la table d'équivalences en
      donne une. Mesuré le 19-09-2026 : `UNIBAIL-RODAMCO-WESTFIELD`,
      `UNIBAIL_RODAMCO`, `UNIBAIL_RODAMCO_WESTFIELD` et `Unibail` rendent tous les
      quatre `unibail_rodamco_westfield`.
      [rend: 1]
    ⑥ TRAITEMENT — ① réduire le nom reçu à sa clé, espaces, tirets et soulignés
      confondus et tout en minuscules · ② chercher cette clé dans la table
      d'équivalences · ③ rendre la forme d'arrivée si la table en donne une, et la
      clé inchangée sinon.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le cas qui a fait écrire cette fonction est consigné au tableau des
      décisions du projet sous l'identifiant A-264, daté du 23-08-2026 : trois
      écritures de BUREAU VERITAS et d'UNIBAIL ont fait disparaître 26 pour cent des
      lignes d'une mesure, EN SILENCE, sans aucune erreur affichée. Les lignes
      perdues étaient celles des opérations les moins rentables, et la mesure ainsi
      amputée a failli être présentée comme une découverte.
      Les trois écritures d'UNIBAIL coexistaient réellement dans le dépôt le
      28-08-2026, chacune dans un fichier différent : `UNIBAIL-RODAMCO-WESTFIELD`
      dans l'historique figé des cours, `UNIBAIL_RODAMCO` dans les cours du jour et
      dans les positions ouvertes, `UNIBAIL_RODAMCO_WESTFIELD` dans le tableau des
      trades de référence. Le rapprochement des séparateurs ne suffit pas à les
      réunir, puisque l'une des trois est plus courte que les autres : il faut une
      table qui dise que la forme courte désigne la longue.
      La table est volontairement la plus petite possible et ne porte que ce qui a
      été CONSTATÉ dans les fichiers, jamais ce qui pourrait arriver : une
      équivalence écrite d'avance rapprocherait un jour deux entreprises réellement
      distinctes, et personne n'irait la relire.
    ⑨ CE QUI CLOCHE —
      ① DEUX TABLES D'ÉQUIVALENCES VIVENT DANS LE DÉPÔT, CHACUNE SE DÉCLARANT LA
      SEULE. Celle de ce fichier porte au-dessus d'elle « LA SEULE TABLE D'ALIAS DU
      PROJET. À compléter ICI et nulle part ailleurs. » ;
      programmes/audit_ecosysteme.py porte aux lignes 211 à 214 une table de même
      nom, `ALIAS_VALEURS`, au contenu identique aujourd'hui, surmontée de « Table
      unique, à compléter ici et NULLE PART AILLEURS (R-708) ». Les deux consignes
      sont exactes séparément et se contredisent ensemble : le jour où une
      entreprise change de nom, celui qui complète l'une aura suivi la consigne
      qu'il avait sous les yeux, l'autre table restera en arrière, et rien
      n'affichera l'écart.
      ② LA TABLE NE COUVRE QU'UNE SEULE ENTREPRISE. Elle porte deux lignes, toutes
      deux pour UNIBAIL. BUREAU VERITAS, dont ce texte dit qu'il porte quatre
      écritures, n'y figure pas : ses quatre écritures se réunissent par le seul
      rapprochement des séparateurs, sans passer par la table. La fonction n'apporte
      donc rien au-delà d'UNIBAIL, et un lecteur qui la croit chargée de tous les
      cas connus se trompe.
      ③ UNE CASE ABSENTE DEVIENT UN NOM D'ENTREPRISE. Mesuré le 19-09-2026 :
      `norm_valeur(None)` rend le texte `none`. Deux lignes à qui il manque le nom
      de la valeur portent donc la même clé et sont rapprochées comme si elles
      désignaient la même entreprise, sans qu'aucune alerte soit produite.
    ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau. Elle LIT la table
      d'équivalences du fichier et ne la modifie jamais.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne
      se termine : elle n'appelle que le rapprochement des séparateurs, qui rend
      toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les
        fichiers du projet
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms
        et n'est jamais affiché à un lecteur
      la table d'équivalences : `ALIAS_VALEURS`, le dictionnaire de ce fichier qui
        dit quelle écriture courte désigne quelle écriture longue
      l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de référence
        qui n'est jamais réécrit
    
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      un trade : une opération simulée, de l'achat à la revente
"""
    k = norm(s)
    return ALIAS_VALEURS.get(k, k)


def rapprocher(brut, noms_attendus):
    """Ramène un dictionnaire de données vers les noms ATTENDUS par l'appelant.

    ① RÔLE — Faire qu'un programme retrouve ses données sous le vocabulaire qu'il
      emploie lui-même, quelles que soient les écritures du fichier d'où elles
      viennent, ET qu'il apprenne nommément ce qui manque. Sans elle, chaque
      programme devrait connaître les écritures de tous les autres.
    ② CONTEXTE D'APPEL — Un seul appelant, `_calibrage`, dans ce fichier, qui l'appelle
      deux fois pour rejouer ses cas connus. AUCUN PROGRAMME DU DÉPÔT NE L'APPELLE :
      mesuré le 19-09-2026, une recherche du mot `rapprocher` dans tous les fichiers
      .py du dépôt ne rend, hors de ce fichier, que deux commentaires qui emploient
      le verbe français, dans programmes/TENIR_LES_POSITIONS.py ligne 444 et
      programmes/COLLECTER_LES_COURS_ABC.py ligne 130.
    ③ ENTRÉE — DEUX paramètres. `brut` : le dictionnaire des données telles qu'elles
      ont été lues, dont les clés sont des noms d'entreprises écrits comme dans le
      fichier d'origine. `noms_attendus` : la liste des noms que l'appelant emploie,
      dans SON écriture à lui. `_calibrage` y passe deux cas écrits dans ce fichier :
      le dictionnaire `{"UNIBAIL-RODAMCO-WESTFIELD": [1], "AIRBUS": [2]}` avec la
      liste `["UNIBAIL_RODAMCO", "AIRBUS"]`, puis `{"AIRBUS": [1]}` avec la liste
      `["AIRBUS", "SAFRAN"]`.
    ④ CONDITIONS D'ENTRÉE — `brut` doit se parcourir par couples clé-valeur, et ne
      doit pas être modifié pendant ce parcours. `noms_attendus` doit se parcourir
      deux fois de suite, ce qui interdit un générateur : un générateur serait vidé
      au premier parcours et la liste des manquants sortirait fausse, vide.
    ⑤ SORTIE — DEUX valeurs. La première est un dictionnaire dont les clés sont les
      noms ATTENDUS, portant les données trouvées. La seconde est la liste des noms
      attendus pour lesquels rien n'a été trouvé, dans l'ordre où ils ont été donnés.
      Mesuré le 19-09-2026 : `rapprocher({"AIRBUS": [1]}, ["AIRBUS", "SAFRAN"])` rend
      le dictionnaire `{"AIRBUS": [1]}` et la liste `["SAFRAN"]`.
      [rend: 2]
    ⑥ TRAITEMENT — ① construire une table qui va de la clé de chaque nom attendu vers
      ce nom attendu lui-même · ② pour chaque couple du dictionnaire reçu, réduire sa
      clé et chercher à quel nom attendu elle correspond · ③ ranger la donnée sous ce
      nom attendu quand il y en a un, et l'écarter sinon · ④ relever les noms attendus
      qui ne sont pas arrivés jusqu'au dictionnaire de sortie.
    ⑦ UNITÉ — Ce qui se compte ici se compte en NOMBRE DE VALEURS, c'est-à-dire en
      nombre d'entreprises. Les données transportées ne sont pas regardées : elles
      sont déplacées telles quelles, quelle que soit leur unité.
    ⑧ POURQUOI — Le piège que cette fonction ferme est que RAPPROCHER LES DEUX CÔTÉS
      NE SUFFIT PAS, et la conversation qui rédige les programmes y est tombée le
      28-08-2026 en écrivant le module de jugement. Si les cours sont rangés sous
      `UNIBAIL_RODAMCO_WESTFIELD` et que le module de signal cherche
      `UNIBAIL_RODAMCO`, les deux clés se ressemblent mais ne se correspondent plus :
      dix opérations sur cent avaient disparu sans un mot, et le taux de réussite
      mesuré était passé de 61,0 à 62,2 pour cent — un chiffre parfaitement
      plausible, que rien ne signalait.
      Le rapprochement ramène donc vers LE NOM ATTENDU et jamais vers une forme
      d'arrivée commune : c'est celui qui appelle qui impose son vocabulaire, et il
      retrouve ses données sous les noms qu'il a lui-même donnés.
      Et la seconde valeur rendue existe pour que rien ne se perde en silence : une
      valeur attendue qui ne répond pas est une ALERTE, jamais un zéro.
    ⑨ CE QUI CLOCHE —
      ① DEUX ÉCRITURES QUI SE RÉUNISSENT FONT PERDRE UNE DONNÉE, SANS ALERTE, DANS LA
      FONCTION MÊME QUI PROMET DE NE RIEN PERDRE EN SILENCE. Quand deux clés du
      dictionnaire reçu se réduisent à la même clé, la seconde rencontrée écrase la
      première et la liste des manquants reste vide, puisque le nom attendu a bien
      été servi. Mesuré le 19-09-2026 :
      `rapprocher({"UNIBAIL_RODAMCO": [1], "UNIBAIL-RODAMCO-WESTFIELD": [2]},
      ["UNIBAIL_RODAMCO"])` rend le dictionnaire `{"UNIBAIL_RODAMCO": [2]}` et une
      liste de manquants VIDE. La donnée `[1]` a disparu, et les deux valeurs
      rendues affirment ensemble que tout s'est bien passé. C'est exactement la
      forme de perte silencieuse qui avait coûté 26 pour cent d'une mesure le
      23-08-2026 (A-264), reparue à l'intérieur du remède.
      ② UN NOM ATTENDU PRÉSENT MAIS VIDE EST COMPTÉ COMME TROUVÉ. Les manquants sont
      relevés sur la seule PRÉSENCE de la clé dans le dictionnaire de sortie, jamais
      sur ce qu'elle porte : une entreprise dont la donnée est une liste vide ou la
      valeur `None` n'apparaît pas dans les manquants. L'appelant croit alors avoir
      reçu quelque chose.
      ③ DEUX NOMS ATTENDUS QUI SE RÉDUISENT À LA MÊME CLÉ S'EFFACENT L'UN L'AUTRE. La
      table construite au premier pas va de la clé vers le nom attendu ; si deux noms
      attendus donnent la même clé, seul le dernier survit dans la table, et le
      premier sera systématiquement rendu comme manquant alors que sa donnée est là,
      rangée sous l'autre nom.
      ④ PERSONNE NE L'APPELLE. La fonction a été écrite le 28-08-2026 pour fermer un
      piège rencontré dans le module de jugement ; treize mois plus tard, son seul
      appelant est le jeu de cas de ce fichier. Le piège qu'elle ferme reste donc
      ouvert partout ailleurs, et le fait qu'elle existe peut faire croire le
      contraire à qui lit le dépôt.
    ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau. Le dictionnaire reçu
      n'est pas modifié ; un dictionnaire neuf est construit. Les données elles-mêmes
      ne sont pas recopiées : ce sont les mêmes objets qui sont rangés sous un autre
      nom, et les modifier ensuite modifie aussi ce que portait le dictionnaire reçu.
    ⑪ TERMINAISON — Rend toujours la main dans le cas normal. PEUT LEVER si le
      dictionnaire reçu est modifié pendant son parcours, ou si `noms_attendus` ne se
      parcourt pas. Aucun de ses appels ne se termine : elle n'appelle que la mise en
      clé des noms, qui rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les
        fichiers du projet
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms
        et n'est jamais affiché à un lecteur
      le module de signal : le programme qui décide quelles valeurs acheter
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
    
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      le module de jugement : `programmes/MODULE_JUGEMENT.py`, qui rend les mesures disant si un gain veut dire quelque chose.
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      le taux de réussite : la part des opérations qui se sont refermées sur un gain, écrite en pourcent
"""
    table = {norm_valeur(n): n for n in noms_attendus}
    out = {}
    for cle_brute, valeur in brut.items():
        attendu = table.get(norm_valeur(cle_brute))
        if attendu is not None:
            out[attendu] = valeur
    manquants = [n for n in noms_attendus if n not in out]
    return out, manquants


# ─────────────────────────────────────────────────────────────────────────
# ③ TROUVER UN FICHIER — sous-dossiers compris, graphies rapprochées
# ─────────────────────────────────────────────────────────────────────────

def trouver(base, *motifs):
    """Rend le chemin RÉEL d'un fichier, sous-dossiers compris, ou rien.

    ① RÔLE — Donner le chemin du fichier qui existe vraiment, sans qu'un programme
      ait à supposer où il est rangé ni comment son nom est écrit. Sans elle, un
      programme construit un chemin de mémoire et ne trouve rien le jour où le
      fichier change de dossier ou de séparateur.
    ② CONTEXTE D'APPEL — AUCUN APPELANT, nulle part. Mesuré le 19-09-2026 de deux
      façons : d'une part la lecture de l'arbre de ce fichier ne trouve aucun appel
      de `trouver` dans aucune de ses fonctions ; d'autre part une recherche du mot
      `trouver` dans tous les fichiers .py du dépôt ne rend, hors de ce fichier, que
      des commentaires en français et TROIS AUTRES DÉFINITIONS du même nom —
      programmes/JUGE_DES_STRATEGIES.py ligne 168, programmes/claude_FABRIQUER_LE_PILOTE.py
      ligne 198 et programmes/PROUVER_L_EXECUTION.py ligne 268.
    ③ ENTRÉE — DEUX paramètres. `base` : le dossier à partir duquel chercher, tous
      ses sous-dossiers compris. `motifs` : un ou plusieurs noms cherchés, donnés à
      la suite, chacun avec ou sans son extension. N'ayant aucun appelant, aucune
      valeur ne lui est passée aujourd'hui ; la forme d'appel prévue par ce fichier
      est `trouver(base, "cac40_ohlcv.csv")`.
    ④ CONDITIONS D'ENTRÉE — Rien n'est exigé : un dossier vide, inexistant ou illisible
      ne la fait pas tomber, et aucun motif du tout est accepté. L'appelant doit en
      revanche savoir que le chemin rendu est construit à partir de `base` : si
      `base` est relatif, le chemin rendu l'est aussi.
    ⑤ SORTIE — UNE valeur : le chemin du premier fichier retenu, ou la valeur `None`
      quand aucun ne correspond. Mesuré le 19-09-2026 sur le dépôt entier :
      `trouver(".", "REGISTRE_REGLES.md")` rend `./gouvernance/REGISTRE_REGLES.md`, et
      `trouver("", "cac40_ohlcv.csv")` rend `None`.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` tout de suite si le dossier de départ est vide ·
      ② PREMIER PASSAGE, le nom exact : pour chaque motif dans l'ordre donné,
      parcourir tout l'arbre et rendre le premier fichier dont le nom, séparateurs et
      casse confondus, est identique au motif · ③ SECOND PASSAGE, le préfixe :
      parcourir de nouveau tout l'arbre, et pour chaque fichier pris dans l'ordre
      alphabétique de son dossier, rendre le premier dont le nom commence par le
      motif privé de son extension · ④ rendre `None` si les deux passages échouent.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS : elle en rend un, ou aucun.
    ⑧ POURQUOI — Deux défauts mesurés sont à l'origine de cette fonction.
      LES SOUS-DOSSIERS. Sur les neuf programmes qui lisaient des fichiers le
      28-08-2026, sept ne regardaient que la racine, alors que le dossier des
      fichiers écrits chaque soir portait les positions ouvertes, le journal des
      trades, les cours du jour et le rapport de surveillance. Le disque par lequel
      la conversation lit le projet APLATIT ces sous-dossiers à la racine, celui de
      l'exécutant non : deux programmes écrits pareil rendaient 76 et 77 opérations
      sur la même fiche, et l'écart est consigné au tableau des décisions sous
      l'identifiant A-302.
      LA TRONCATURE. L'identité d'un fichier se joue sur le motif ENTIER et jamais
      sur ses premiers caractères. Si l'on acceptait de couper le motif, deux
      fichiers partageant un début de nom deviendraient indiscernables et c'est
      l'ordre alphabétique qui trancherait entre eux : un arbitrage par table de
      caractères là où il faut une décision. Le cas est consigné sous l'identifiant
      A-284. Le second passage ne coupe donc que l'EXTENSION, jamais le nom.
      Le nom exact passe avant le préfixe pour que la présence du fichier cherché
      l'emporte toujours sur celle d'un fichier qui lui ressemble.
    ⑨ CE QUI CLOCHE —
      ① ELLE REND UNE VERSION ARCHIVÉE À LA PLACE DU PROGRAMME VIVANT. Le second
      passage retient le premier fichier dont le nom COMMENCE par le motif, dans
      l'ordre où le système rend les dossiers — et le dossier des versions
      abandonnées est rendu avant celui des programmes. Mesuré le 19-09-2026 sur le
      dépôt : `trouver(".", "claude_FABRIQUER_LE_PILOTE")` rend
      `./archives/claude_FABRIQUER_LE_PILOTE_AVANT_4_MOTIFS_Mar_08-09-2026_22h40.py`,
      alors que le programme vivant `./programmes/claude_FABRIQUER_LE_PILOTE.py`
      existe et porte le même début de nom. Un programme qui chercherait ainsi son
      propre code lirait une version tombée le 08-09-2026.
      ② ELLE CHOISIT LE PREMIER RENCONTRÉ, JAMAIS LE PLUS RÉCENT — alors que la
      fonction qui sait lire la date d'un nom vit dans CE FICHIER, quinze lignes plus
      bas. Mesuré le 19-09-2026 : `trouver(".", "golden_tests.json")` rend
      `./gouvernance/golden_tests_Sam_01-08-2026_20h19.json` parce que c'est le
      premier trouvé, et non parce que c'est le plus récent. Le fichier porte
      pourtant en toutes lettres, plus bas, que le plus récent se lit dans la date et
      jamais dans l'alphabet.
      ③ L'ORDRE DES MOTIFS EST RESPECTÉ AU PREMIER PASSAGE ET IGNORÉ AU SECOND. Au
      premier, chaque motif est cherché dans tout l'arbre avant de passer au
      suivant : le premier motif donné l'emporte. Au second, c'est le fichier qui est
      pris en premier et les motifs sont essayés sur lui : le motif donné en dernier
      peut l'emporter si son fichier vient plus tôt dans le parcours. Un appelant qui
      donne ses motifs par ordre de préférence n'est donc obéi que dans la moitié des
      cas, et rien ne lui dit lequel des deux passages a répondu.
      ④ ELLE PARCOURT L'ARBRE ENTIER DEUX FOIS. Le premier passage relit tout le
      dossier pour CHAQUE motif, et le second le relit encore. Sur le dépôt entier,
      292 fichiers relevés le 19-09-2026, cela reste sans conséquence ; sur un
      dossier plus grand, le coût croît avec le nombre de motifs.
    ⑩ EFFET — Ne change rien : aucun fichier écrit, aucun accès réseau. Elle LIT les
      noms de tous les dossiers et sous-dossiers à partir du dossier de départ, y
      compris ceux des versions abandonnées, et n'ouvre aucun fichier.
    ⑪ TERMINAISON — Rend toujours la main : un dossier illisible est sauté sans
      erreur par le parcours. Aucun de ses appels ne se termine : elle n'appelle que
      la mise en clé des noms, qui rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
      les archives : le dossier archives/ du dépôt, où sont rangées les versions
        abandonnées, sous un nom qui dit pourquoi elles sont tombées
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
      l'exécutant : le service qui lance les programmes du soir sans intervention
        humaine
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not base:
        return None
    # d'abord le nom exact, dans les deux graphies
    for m in motifs:
        for d, _, fs in os.walk(base):
            for f in fs:
                if norm(f) == norm(m):
                    return os.path.join(d, f)
    # puis le préfixe, extension ôtée
    for d, _, fs in os.walk(base):
        for f in sorted(fs):
            nf = norm(f)
            for m in motifs:
                racine = re.sub(r"\.(md|py|csv|json|html|txt)$", "", norm(m))
                if racine and nf.startswith(racine):
                    return os.path.join(d, f)
    return None


def trouver_tous(base, *motifs):
    """Rend TOUS les chemins qui correspondent, pour que l'appelant voie qu'il y en a
    plusieurs au lieu d'en prendre un au hasard.

    ① RÔLE — Rendre visible la présence de plusieurs fichiers là où l'on en attendait
      un seul, au lieu de trancher à la place de l'appelant. Elle ne choisit pas :
      elle montre.
    ② CONTEXTE D'APPEL — AUCUN APPELANT, nulle part. Mesuré le 19-09-2026 de deux
      façons : la lecture de l'arbre de ce fichier ne trouve aucun appel de
      `trouver_tous` dans aucune de ses fonctions, et une recherche du mot
      `trouver_tous` dans tous les fichiers .py du dépôt ne rend, hors de ce fichier,
      qu'une AUTRE définition du même nom, dans programmes/JUGE_DES_STRATEGIES.py ligne 126,
      appelée là-bas à la ligne 739.
    ③ ENTRÉE — DEUX paramètres. `base` : le dossier à partir duquel chercher, tous ses
      sous-dossiers compris. `motifs` : un ou plusieurs noms cherchés, donnés à la
      suite, avec ou sans extension. N'ayant aucun appelant, aucune valeur ne lui est
      passée aujourd'hui ; la forme d'appel prévue par ce fichier est
      `trouver_tous(base, "REGISTRE_REGLES.md")`.
    ④ CONDITIONS D'ENTRÉE — Rien n'est exigé : un dossier vide, inexistant ou illisible
      ne la fait pas tomber. Comme pour toute recherche de ce fichier, un dossier de
      départ relatif donne des chemins relatifs.
    ⑤ SORTIE — UNE valeur : une liste de chemins, éventuellement vide. Les doublons de
      chemin sont écartés, et l'ordre est celui du parcours des dossiers, puis
      l'ordre alphabétique à l'intérieur de chacun. Mesuré le 19-09-2026 sur le dépôt
      entier : `trouver_tous(".", "claude_FABRIQUER_LE_PILOTE.py")` rend trois
      chemins, les deux premiers dans le dossier des versions abandonnées et le
      troisième seulement étant le programme vivant.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre une liste vide tout de suite si le dossier de départ est
      vide · ② parcourir tout l'arbre à partir de ce dossier · ③ pour chaque fichier,
      pris dans l'ordre alphabétique de son dossier, retenir son chemin si son nom
      est identique à l'un des motifs, séparateurs et casse confondus, OU s'il
      commence par ce motif privé de son extension · ④ ne pas ajouter deux fois le
      même chemin.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS.
    ⑧ POURQUOI — Un dépôt peut porter deux fichiers différents sous le même nom ; un
      dossier, non. Quand plusieurs fichiers répondent, le silence est le pire des
      choix : le programme qui en prendrait un seul travaillerait sur une version
      sans jamais dire qu'il y en avait une autre. Cette fonction laisse donc la
      décision à celui qui appelle, et son seul travail est de ne rien cacher.
      Elle accepte le préfixe, extension ôtée, exactement comme la recherche qui rend
      un seul chemin dans ce même fichier : deux façons de chercher qui ne
      répondraient pas pareil feraient passer pour absent, chez l'une, un fichier que
      l'autre trouve.
    ⑨ CE QUI CLOCHE —
      ① ELLE FAIT PASSER POUR DES DOUBLONS DES FICHIERS QUI N'EN SONT PAS. Le préfixe
      suffit à retenir un fichier, donc une version archivée et un fichier voisin sont
      comptés avec le fichier cherché. Mesuré le 19-09-2026 sur le dépôt :
      `trouver_tous(".", "PILOTE.md")` rend DEUX chemins,
      `./gouvernance/PILOTE.md` et `./gouvernance/PILOTE_SOCLE.md`, qui sont deux
      documents différents ; et `trouver_tous(".", "claude_FABRIQUER_LE_PILOTE.py")`
      en rend trois, dont deux versions abandonnées. Le critère qui tranche tient en
      une question : si je renomme un fichier, mon contrôle change-t-il d'avis ? Ici
      oui, donc le nom est épelé au lieu d'une propriété.
      ② L'APPELANT NE SAIT PAS POURQUOI UN CHEMIN A ÉTÉ RETENU. Un chemin retenu parce
      que son nom est exactement le motif et un chemin retenu parce qu'il commence
      par le motif arrivent mélangés dans la même liste, sans rien qui les
      distingue. Qui veut le fichier exact doit recommencer la comparaison lui-même.
      ③ ELLE NE DÉDOUBLONNE QUE LES CHEMINS, PAS LES FICHIERS. Deux chemins différents
      qui désignent le même fichier, par exemple à travers un lien, sont comptés
      deux fois et présentés comme deux fichiers.
      ④ PERSONNE NE L'APPELLE, ET UNE AUTRE FONCTION DU MÊME NOM, ELLE, EST APPELÉE.
      programmes/JUGE_DES_STRATEGIES.py porte sa propre `trouver_tous` ligne 126 et l'emploie
      ligne 739. Deux implémentations d'une même chose divergent toujours (R-708) ;
      ici la copie sert et l'originale dort, ce qui garantit que les corrections
      faites à l'une n'atteindront jamais l'autre.
    ⑩ EFFET — Ne change rien : aucun fichier écrit, aucun accès réseau. Elle LIT les
      noms de tous les dossiers et sous-dossiers à partir du dossier de départ, y
      compris ceux des versions abandonnées, et n'ouvre aucun fichier.
    ⑪ TERMINAISON — Rend toujours la main : un dossier illisible est sauté sans erreur
      par le parcours. Aucun de ses appels ne se termine : elle n'appelle que la mise
      en clé des noms, qui rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
      les archives : le dossier archives/ du dépôt, où sont rangées les versions
        abandonnées, sous un nom qui dit pourquoi elles sont tombées
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    out = []
    if not base:
        return out
    for d, _, fs in os.walk(base):
        for f in sorted(fs):
            nf = norm(f)
            for m in motifs:
                racine = re.sub(r"\.(md|py|csv|json|html|txt)$", "", norm(m))
                if nf == norm(m) or (racine and nf.startswith(racine)):
                    p = os.path.join(d, f)
                    if p not in out:
                        out.append(p)
    return out


# ─────────────────────────────────────────────────────────────────────────
# ④ LIRE UNE SOURCE — ou dire qu'on n'a pas pu
# ─────────────────────────────────────────────────────────────────────────

class Illisible:
    """Marque une lecture qui n'a pas pu se faire, sans jamais se confondre avec un
    fichier vide.

    ① RÔLE — Donner à une lecture ratée une valeur qui se RECONNAÎT, pour qu'un
      programme puisse crier au lieu de rendre zéro. Tant qu'une lecture ratée et un
      fichier vide portent la même valeur — une liste vide, un texte vide — aucun
      garde-fou ne peut les distinguer.
    ② CONTEXTE D'APPEL — Construite à trois endroits, tous dans ce fichier : `lire`
      quand elle ne peut pas rendre un texte, `lire_csv` quand elle ne peut pas rendre
      de lignes, et `_calibrage` qui vérifie qu'une lecture ratée en produit bien une.
      Aucun programme du dépôt ne l'emploie : mesuré le 19-09-2026, une recherche du
      mot `Illisible` dans tous les fichiers .py du dépôt ne rend, hors de ce fichier,
      qu'une AUTRE classe du même nom, dans programmes/claude_FABRIQUER_LE_PILOTE.py
      ligne 240.
    ③ ENTRÉE — DEUX paramètres à la construction. `motif` : la raison, en un mot ou
      deux, pour laquelle la lecture a échoué. `chemin` : le fichier concerné, absent
      quand il n'y en a pas. Les valeurs réellement passées dans ce fichier sont
      `"chemin absent"` sans chemin, `"fichier vide"` avec le chemin, et le nom de
      l'erreur rencontrée avec le chemin, par exemple `"UnicodeDecodeError"` ou
      `"FileNotFoundError"`, mesurés le 19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Aucune : n'importe quelle valeur est acceptée pour l'un
      comme pour l'autre, et rien n'est vérifié.
    ⑤ SORTIE — Un objet qui se comporte comme un vide : sa longueur est zéro, il se
      parcourt sans rien rendre, et il vaut faux dans un test. Mais il se reconnaît,
      et il porte sa raison. La façon de s'en servir est :
          r = lire_csv(chemin)
          if isinstance(r, Illisible):
              alerter(f"source illisible : {r.motif}")
    ⑥ TRAITEMENT — ① retenir la raison et le chemin à la construction · ② répondre
      zéro à qui demande sa longueur · ③ répondre un parcours vide à qui le parcourt ·
      ④ répondre faux à qui le teste · ⑤ rendre un texte qui porte sa raison à qui
      l'affiche.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ce que coûte l'absence de cette distinction a été mesuré le
      28-08-2026 sur les neuf programmes du dépôt qui lisaient des fichiers : DEUX
      distinguaient une lecture ratée d'un fichier vide, deux le faisaient à moitié,
      et CINQ rendaient zéro en silence. Le service qui mesure la performance en
      faisait partie : quand il ne retrouvait pas un cours, il annonçait une
      variation latente de 0,00 euro. Pendant ce temps, le programme de surveillance
      annonçait « position conforme » sur la même valeur. Deux chiffres, aucune
      alerte, et rien qui dise lequel des deux avait regardé.
      La règle du projet qui l'interdit est consignée au tableau des décisions sous
      l'identifiant A-226 : ne jamais confondre « inconnu » et « zéro ».
      L'objet se comporte volontairement comme un vide, et ce n'est pas une
      contradiction : un programme qui ne sait pas encore le reconnaître continue de
      fonctionner comme avant au lieu de tomber, et celui qui sait le reconnaître
      obtient l'alerte. C'est ce qui permet de l'introduire sans réécrire les
      appelants d'un seul coup.
    ⑨ CE QUI CLOCHE —
      ① LE COMPORTEMENT DE VIDE ANNULE L'ALERTE CHEZ QUI NE LA CHERCHE PAS. Un
      appelant qui écrit `if not lignes: return 0` obtient exactement le zéro
      silencieux que cette classe existe pour empêcher, puisque l'objet vaut faux.
      La distinction n'a d'effet que si l'appelant la demande explicitement, et RIEN
      dans la valeur rendue n'oblige à la demander. La classe rend l'alerte
      possible ; elle ne la rend pas obligatoire.
      ② DEUX CLASSES DU MÊME NOM VIVENT DANS LE DÉPÔT.
      programmes/claude_FABRIQUER_LE_PILOTE.py ligne 240 porte sa propre `Illisible`
      et s'en sert à onze endroits, tandis que celle-ci n'est employée que dans ce
      fichier. Deux implémentations d'une même chose divergent toujours (R-708), et
      un objet reconnu par `isinstance` divergera de la pire façon : un `Illisible`
      de l'un ne sera JAMAIS reconnu comme un `Illisible` de l'autre, même si les
      deux classes sont écrites à l'identique. Le jour où les deux fichiers se
      croiseront, l'alerte se taira sans qu'aucune erreur ne s'affiche.
      ③ LE CHEMIN N'EST PAS TOUJOURS RENSEIGNÉ. Quand la raison est `"chemin absent"`,
      le chemin vaut `None` : un message d'alerte qui l'afficherait écrirait
      « source illisible : None ». Mesuré le 19-09-2026 sur `lire_csv(None)`.
      ④ LE TEXTE D'AFFICHAGE NE PORTE QUE LA RAISON. Il rend `Illisible('chemin
      absent')` et tait le chemin, mesuré le 19-09-2026. Un rapport qui afficherait
      plusieurs de ces objets ne dirait pas quels fichiers sont concernés.
    ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau. Elle ne retient que
      les deux valeurs qu'on lui donne.
    ⑪ TERMINAISON — Toutes ses méthodes rendent la main et ne lèvent pas. Aucun de
      leurs appels ne se termine.
    ⑫ DÉFINITIONS
      le zéro silencieux : un programme qui rend zéro là où il aurait dû dire qu'il
        n'a pas pu lire, sans rien afficher
      le service de mesure : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        qui calcule la performance des positions
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    """

    def __init__(self, motif, chemin=None):
        """Retient la raison de l'échec et le fichier concerné.

        ① RÔLE — Garder, dans l'objet rendu à la place des données, les deux
          renseignements qu'un message d'alerte devra porter : pourquoi la lecture a
          échoué, et sur quel fichier.
        ② CONTEXTE D'APPEL — Appelée par Python à chaque construction d'un `Illisible`.
          Les trois endroits qui en construisent sont dans ce fichier : `lire`,
          `lire_csv` et `_calibrage`.
        ③ ENTRÉE — TROIS paramètres. `self` : l'objet en cours de construction,
          que Python passe de lui-même et qu'aucun appelant ne fournit. `motif` : la
          raison de l'échec, en un mot ou deux. `chemin` : le fichier concerné,
          absent par défaut. Les valeurs réellement
          passées dans ce fichier sont `"chemin absent"` seul, `"fichier vide"` avec
          le chemin, et le nom de l'erreur rencontrée avec le chemin, par exemple
          `"FileNotFoundError"`, mesuré le 19-09-2026.
        ④ CONDITIONS D'ENTRÉE — Aucune. Rien n'est vérifié : n'importe quelle valeur
          est acceptée pour l'un comme pour l'autre.
        ⑤ SORTIE — Ne rend rien. Elle pose deux valeurs sur l'objet en construction.
          [rend: rien]
        ⑥ TRAITEMENT — ① poser la raison sur l'objet · ② poser le chemin sur l'objet.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — La raison est retenue plutôt que reconstruite au moment de
          l'affichage, parce qu'elle n'est connue qu'à l'instant de l'échec : le nom
          de l'erreur rencontrée disparaît dès que la lecture est abandonnée. Sans
          cela, l'alerte ne pourrait dire que « lecture impossible », sans distinguer
          un fichier absent d'un fichier aux octets invalides.
        ⑨ CE QUI CLOCHE — Le chemin est facultatif et vaut alors `None`, ce qui fait
          qu'un objet construit sur `"chemin absent"` ne porte aucun chemin : mesuré
          le 19-09-2026, `lire_csv(None).chemin` vaut `None`. Un message d'alerte qui
          l'afficherait écrirait le mot `None` à la place d'un nom de fichier.
        ⑩ EFFET — Ne change rien hors de l'objet en construction : aucun fichier,
          aucun accès réseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
          ne se termine : elle n'appelle rien.
          [sort: non]
        ⑫ DÉFINITIONS
          la raison : le texte court qui dit pourquoi une lecture a échoué, retenu
            sous le nom `motif`
        """
        self.motif = motif
        self.chemin = chemin

    def __len__(self):
        """Rend zéro, pour que l'objet se compte comme un vide.

        ① RÔLE — Permettre qu'un programme qui ne connaît pas encore cette classe
          continue de fonctionner comme avant, au lieu de tomber sur une valeur
          inattendue. C'est la moitié « se comporte comme un vide » du contrat de
          cette classe.
        ② CONTEXTE D'APPEL — Appelée par Python chaque fois qu'on demande la longueur
          de l'objet, ou qu'on le teste dans une condition si la réponse à la
          question du vrai ou faux n'était pas définie. Dans ce fichier, `_calibrage`
          la déclenche en vérifiant que la longueur d'une lecture ratée vaut zéro.
        ③ ENTRÉE — UN paramètre, `self` : l'objet de lecture ratée lui-même,
          que Python passe de lui-même. Aucun appelant ne fournit de valeur.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : le nombre entier zéro, toujours, quelles que soient la
          raison et le chemin retenus. Mesuré le 19-09-2026 : `len(lire_csv(None))`
          vaut 0.
          [rend: 1]
        ⑥ TRAITEMENT — ① rendre zéro.
        ⑦ UNITÉ — Un NOMBRE DE LIGNES, par convention avec ce que rendrait une lecture
          réussie.
        ⑧ POURQUOI — Zéro est rendu, et non une erreur, pour que cette classe puisse
          être introduite dans le dépôt sans réécrire d'un seul coup tous les
          programmes qui lisent des fichiers. Un programme qui compte les lignes
          obtient zéro et se comporte comme avant ; celui qui sait reconnaître
          l'objet obtient l'alerte. Le coût de ce choix est écrit au texte de la
          classe : l'alerte reste possible, elle n'est pas obligatoire.
        ⑨ CE QUI CLOCHE — Rendre zéro rend cet objet indiscernable d'un vrai fichier
          vide POUR QUI NE REGARDE QUE LA LONGUEUR, et c'est exactement la confusion
          que la classe existe pour empêcher. La distinction ne survit que dans le
          type de l'objet, jamais dans ce qu'il compte.
        ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau, aucune valeur
          modifiée.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
          ne se termine : elle n'appelle rien.
          [sort: non]
        """
        return 0

    def __iter__(self):
        """Rend un parcours vide, pour que l'objet se parcoure comme un vide.

        ① RÔLE — Permettre qu'une boucle écrite sur le résultat d'une lecture tourne
          zéro fois au lieu de tomber, quand la lecture a échoué. C'est la seconde
          moitié du comportement de vide de cette classe, celle qui sert aux boucles.
        ② CONTEXTE D'APPEL — Appelée par Python chaque fois que l'objet est parcouru,
          typiquement par une boucle écrite sur le résultat de `lire_csv`. Aucun
          appel explicite dans ce fichier.
        ③ ENTRÉE — UN paramètre, `self` : l'objet de lecture ratée lui-même,
          que Python passe de lui-même. Aucun appelant ne fournit de valeur.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : un parcours sur une suite vide, qui ne rend aucun
          élément. Une boucle écrite dessus s'exécute zéro fois.
          [rend: 1]
        ⑥ TRAITEMENT — ① rendre le parcours d'une suite vide.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un parcours neuf est rendu à chaque appel, et non un parcours
          conservé sur l'objet : un parcours conservé serait vidé au premier usage, et
          la deuxième boucle écrite sur le même objet se comporterait différemment de
          la première sans que rien ne l'explique.
        ⑨ CE QUI CLOCHE — Une boucle qui tourne zéro fois ne se distingue pas d'une
          boucle sur un fichier sans ligne : un programme qui ne lit les données que
          par une boucle n'apprendra jamais que la lecture a échoué. La reconnaissance
          de l'objet doit se faire AVANT la boucle, et rien ne l'y oblige.
        ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau, aucune valeur
          modifiée.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
          ne se termine : elle n'appelle rien.
          [sort: non]
        """
        return iter(())

    def __bool__(self):
        """Rend faux, pour que l'objet soit testé comme un vide.

        ① RÔLE — Permettre qu'un test écrit sur le résultat d'une lecture prenne la
          branche « rien à traiter » quand la lecture a échoué, au lieu de traiter un
          objet qu'il ne connaît pas.
        ② CONTEXTE D'APPEL — Appelée par Python chaque fois que l'objet est placé dans
          une condition, par exemple `if not donnees:`. Aucun appel explicite dans ce
          fichier.
        ③ ENTRÉE — UN paramètre, `self` : l'objet de lecture ratée lui-même,
          que Python passe de lui-même. Aucun appelant ne fournit de valeur.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : faux, toujours. Mesuré le 19-09-2026 :
          `bool(lire_csv(None))` vaut faux.
          [rend: 1]
        ⑥ TRAITEMENT — ① rendre faux.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — La réponse est écrite explicitement alors que la longueur nulle
          suffirait à la produire, pour que le comportement reste le même le jour où
          la longueur changerait de définition : deux façons de répondre à la même
          question finissent toujours par diverger (R-708), et celle-ci est la plus
          souvent employée dans le dépôt.
        ⑨ CE QUI CLOCHE — C'est par cette méthode que l'alerte se perd le plus
          facilement. Un appelant qui écrit `if not lignes: return 0` obtient
          exactement le zéro silencieux que cette classe existe pour empêcher, et il
          ne peut pas le deviner en lisant son propre code : rien, à l'endroit du
          test, ne dit que la valeur testée pouvait être une lecture ratée.
        ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau, aucune valeur
          modifiée.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
          ne se termine : elle n'appelle rien.
          [sort: non]
        ⑫ DÉFINITIONS
          le zéro silencieux : un programme qui rend zéro là où il aurait dû dire
            qu'il n'a pas pu lire, sans rien afficher
        
          le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
          une lecture ratée : un objet de la classe `Illisible`, rendu à la place des données quand la lecture n'a pas pu se faire, et qui porte sa raison
          une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        return False

    def __repr__(self):
        """Rend le texte qui montre la raison de l'échec quand l'objet est affiché.

        ① RÔLE — Faire qu'un objet de lecture ratée, s'il apparaît dans un affichage
          ou dans une trace, dise POURQUOI la lecture a échoué, au lieu de n'être
          qu'une adresse en mémoire illisible pour un lecteur.
        ② CONTEXTE D'APPEL — Appelée par Python chaque fois que l'objet est affiché ou
          placé dans une trace. Aucun appel explicite dans ce fichier.
        ③ ENTRÉE — UN paramètre, `self` : l'objet de lecture ratée lui-même,
          que Python passe de lui-même. Aucun appelant ne fournit de valeur.
        ④ CONDITIONS D'ENTRÉE — Aucune. La raison retenue à la construction doit
          pouvoir être affichée, ce qui est vrai de toute valeur.
        ⑤ SORTIE — UNE valeur : un texte de la forme exacte `Illisible('chemin
          absent')`, mesurée le 19-09-2026 sur `lire_csv(None)`.
          [rend: 1]
        ⑥ TRAITEMENT — ① composer un texte portant le nom de la classe et la raison
          retenue, entre guillemets.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — La raison est affichée entre guillemets, telle qu'on l'écrirait
          dans du code, pour qu'on voie où elle commence et où elle finit : une raison
          affichée sans guillemets se confond avec le reste de la phrase dès qu'elle
          contient un espace, ce qui est le cas des deux raisons les plus fréquentes,
          `chemin absent` et `fichier vide`.
        ⑨ CE QUI CLOCHE — LE CHEMIN N'EST PAS AFFICHÉ. Le texte ne porte que la
          raison, et tait le fichier concerné : mesuré le 19-09-2026,
          `repr(lire_csv("/un/fichier/absent.csv"))` rend
          `Illisible('FileNotFoundError')`, sans le chemin. Un rapport qui afficherait
          plusieurs de ces objets ne dirait pas lesquels de ses fichiers sont en
          cause, et la valeur nécessaire est pourtant retenue sur l'objet.
        ⑩ EFFET — Ne change rien : aucun fichier, aucun accès réseau, aucune valeur
          modifiée. Elle n'affiche rien elle-même : elle rend un texte que son
          appelant affiche.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
          ne se termine : elle n'appelle rien.
          [sort: non]
        """
        return f"Illisible({self.motif!r})"


def lire(chemin):
    """Rend le texte d'un fichier, ou un objet de lecture ratée. Jamais un texte vide
    en cas d'échec.

    ① RÔLE — Donner le contenu d'un fichier texte à qui le demande, en distinguant
      « je n'ai pas pu lire » de « il n'y a rien dedans », pour qu'une lecture ratée
      puisse produire une alerte au lieu d'être traitée comme un fichier vide.
    ② CONTEXTE D'APPEL — AUCUN APPELANT, nulle part. Mesuré le 19-09-2026 de deux
      façons : la lecture de l'arbre de ce fichier ne trouve aucun appel de `lire`
      dans aucune de ses fonctions, pas même dans le jeu de cas connus ; et une
      recherche du mot `lire` dans tous les fichiers .py du dépôt ne rend, hors de ce
      fichier, que des commentaires en français et TROIS AUTRES DÉFINITIONS du même
      nom — programmes/claude_FABRIQUER_LE_PILOTE.py ligne 262,
      programmes/TENIR_L_HISTORIQUE.py ligne 191 et programmes/EPREUVES_DU_SOCLE.py
      ligne 187.
    ③ ENTRÉE — `chemin` : le chemin du fichier texte à lire. N'ayant aucun appelant,
      aucune valeur ne lui est passée aujourd'hui ; la forme d'appel prévue par ce
      fichier est `lire(trouver(base, "PILOTE.md"))`, avec la valeur `None` acceptée
      comme réponse d'une recherche qui n'a rien trouvé.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un chemin vide, la valeur `None`, un fichier
      absent, un dossier ou un fichier sans droit de lecture ne la font pas tomber :
      chacun de ces cas rend un objet de lecture ratée portant sa raison.
    ⑤ SORTIE — UNE valeur, de DEUX formes. Un texte, quand le fichier a été lu et
      qu'il porte autre chose que des espaces. Un objet de lecture ratée sinon, avec
      trois raisons possibles : `"chemin absent"` quand rien n'a été donné,
      `"fichier vide"` quand le fichier ne porte que des espaces, et le nom de
      l'erreur rencontrée quand l'ouverture a échoué, par exemple
      `"FileNotFoundError"`, mesuré le 19-09-2026.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre une lecture ratée tout de suite si aucun chemin n'est
      donné · ② ouvrir le fichier et lire tout son contenu d'un coup · ③ rendre une
      lecture ratée portant le nom de l'erreur si l'ouverture ou la lecture a échoué ·
      ④ rendre une lecture ratée si le contenu ne porte que des espaces · ⑤ rendre le
      texte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un texte vide n'est pas rendu en cas d'échec parce qu'un texte vide
      se confond avec un fichier réellement vide, et que ce que cette confusion coûte
      a été mesuré le 28-08-2026 : sur les neuf programmes du dépôt qui lisaient des
      fichiers, CINQ rendaient zéro en silence quand ils ne pouvaient pas lire.
      Trois familles d'erreurs sont rattrapées et non une seule, parce qu'elles ne
      viennent pas de la même famille : l'erreur d'un fichier absent ou d'un droit
      refusé vient du système, celle d'un chemin qui n'est pas un texte vient du
      langage, et celle d'un octet invalide vient de la conversion. Rattraper la
      première seule laisserait le programme s'arrêter sur les deux autres.
    ⑨ CE QUI CLOCHE —
      ① ELLE NE CRIE JAMAIS SUR UN FICHIER ABÎMÉ, ALORS QUE SA VOISINE LE FAIT. Les
      octets invalides sont REMPLACÉS à la lecture au lieu de faire échouer la
      conversion. Mesuré le 19-09-2026 sur un fichier de six octets commençant par
      trois octets invalides : `lire` rend le texte `'\ufffd\ufffd\x00bad'` et n'est
      PAS une lecture ratée, tandis que `lire_csv`, dans ce même fichier et sur ce
      même fichier, rend une lecture ratée portant la raison `"UnicodeDecodeError"`.
      Deux lectures du même fichier, dans le même module, écrites à quinze lignes
      l'une de l'autre, et deux réponses contraires : l'une corrompt en silence, la
      seule qui crie est celle que l'on n'appelle pas pour du texte.
      ② UN FICHIER QUI NE PORTE QUE DES ESPACES EST DÉCLARÉ VIDE ET NON LU. La
      décision est raisonnable pour un document, mais elle est prise à la place de
      l'appelant : un fichier dont le contenu attendu est justement une suite
      d'espaces ou de sauts de ligne ne pourra jamais être lu par cette fonction, et
      rien ne distingue ce cas d'un fichier de taille nulle, les deux portant la même
      raison `"fichier vide"`.
      ③ PERSONNE NE L'APPELLE, ET TROIS AUTRES FONCTIONS DU MÊME NOM, ELLES, SONT
      APPELÉES. Elle a été écrite le 28-08-2026 pour remplacer les lectures
      dispersées ; treize mois plus tard, les trois qu'elle devait remplacer sont
      toujours en service. Deux implémentations d'une même chose divergent toujours
      (R-708), et ici il y en a quatre.
    ⑩ EFFET — LIT le fichier désigné, en entier et d'un coup. N'écrit aucun fichier,
      ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main : les trois familles d'erreurs d'ouverture
      et de lecture sont rattrapées et rendues sous forme d'objet de lecture ratée.
      Aucun de ses appels ne se termine : elle ne construit qu'un objet de lecture
      ratée, dont la construction rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une lecture ratée : un objet de la classe `Illisible`, rendu à la place des
        données quand la lecture n'a pas pu se faire, et qui porte sa raison
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    """
    if not chemin:
        return Illisible("chemin absent")
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            t = f.read()
    except (OSError, TypeError, ValueError) as e:
        return Illisible(type(e).__name__, chemin)
    if not t.strip():
        return Illisible("fichier vide", chemin)
    return t


def lire_csv(chemin):
    """Rend les lignes d'un fichier de tableau, ou un objet de lecture ratée. Jamais
    une liste vide en cas d'échec.

    ① RÔLE — Donner les lignes d'un fichier de tableau à qui les demande, chacune
      sous forme de couples colonne-valeur, en distinguant « je n'ai pas pu lire » de
      « il n'y a aucune ligne », pour qu'une lecture ratée puisse produire une alerte
      au lieu d'être comptée comme zéro ligne.
    ② CONTEXTE D'APPEL — Un seul appelant, `_calibrage`, dans ce fichier, qui l'appelle
      trois fois sur la valeur `None` pour vérifier qu'une lecture ratée se reconnaît,
      se compte comme un vide et porte sa raison. AUCUN PROGRAMME DU DÉPÔT NE
      L'APPELLE : mesuré le 19-09-2026, une recherche du mot `lire_csv` dans tous les
      fichiers .py du dépôt ne rend, hors de ce fichier, qu'une AUTRE fonction du même
      nom dans programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py ligne 89,
      appelée là-bas six fois.
    ③ ENTRÉE — `chemin` : le chemin du fichier de tableau à lire. Le seul appelant,
      `_calibrage`, y passe la valeur `None`, et seulement elle, pour éprouver le cas
      du chemin absent.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un chemin vide, la valeur `None`, un fichier
      absent, un dossier, un fichier sans droit de lecture, un fichier aux octets
      invalides ou un tableau mal formé ne la font pas tomber : chacun de ces cas rend
      un objet de lecture ratée portant sa raison.
    ⑤ SORTIE — UNE valeur, de DEUX formes. Une liste de lignes, chaque ligne étant un
      dictionnaire qui va du nom de colonne à sa valeur, quand la lecture a réussi.
      Un objet de lecture ratée sinon, avec trois raisons possibles : `"chemin
      absent"`, `"fichier vide"`, ou le nom de l'erreur rencontrée. Mesuré le
      19-09-2026 : un fichier de deux octets rend `Illisible('fichier vide')`, un
      fichier aux octets invalides rend `Illisible('UnicodeDecodeError')`, un fichier
      absent rend `Illisible('FileNotFoundError')`, et un fichier de dix-sept octets
      portant une ligne rend `[{'nom': 'AIRBUS', 'val': '1'}]`.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre une lecture ratée tout de suite si aucun chemin n'est
      donné · ② ouvrir le fichier en écartant la marque d'ordre des octets s'il en
      porte une, et en laissant la lecture de tableau gérer elle-même les fins de
      ligne · ③ lire toutes les lignes d'un coup · ④ rendre une lecture ratée portant
      le nom de l'erreur si l'ouverture, la conversion ou la lecture du tableau a
      échoué · ⑤ si aucune ligne n'a été lue, regarder la TAILLE du fichier : rendre
      une lecture ratée s'il pèse moins de quatre octets, et la liste vide sinon ·
      ⑥ rendre les lignes.
    ⑦ UNITÉ — Les lignes se comptent en NOMBRE DE LIGNES DE TABLEAU, la ligne des noms
      de colonnes non comprise. Le seuil du cinquième pas se compte en OCTETS.
    ⑧ POURQUOI — L'erreur des octets invalides descend de l'erreur de valeur et NON de
      l'erreur du système : une clause qui ne rattraperait que les erreurs du système
      laisserait le programme s'ARRÊTER sur un fichier dont l'encodage est invalide.
      Le cas a été constaté le 26-08-2026.
      La marque d'ordre des octets est écartée à l'ouverture parce que les fichiers
      de tableau produits par un tableur en portent une : sans cela, le nom de la
      PREMIÈRE colonne porterait trois octets invisibles en tête et ne
      correspondrait à rien, alors que toutes les autres seraient justes.
      Et la taille du fichier est regardée quand aucune ligne n'a été lue, parce
      qu'une liste vide a deux causes très différentes qu'il faut séparer : un fichier
      réellement vide, et un fichier qui porte ses noms de colonnes mais aucune ligne
      de données.
    ⑨ CE QUI CLOCHE —
      ① LE SEUIL DE QUATRE OCTETS EST UN NOMBRE ÉCRIT DANS LE CODE, ET IL SE TROMPE
      SUR DE VRAIS FICHIERS. Un fichier qui porte ses noms de colonnes mais aucune
      ligne de données est déclaré VIDE dès que ces noms tiennent en moins de quatre
      octets. Mesuré le 19-09-2026 : un fichier de deux octets portant `a` et un saut
      de ligne rend `Illisible('fichier vide')`, alors qu'il porte une colonne ; un
      fichier de quatre octets portant `a,b` et un saut de ligne rend la liste vide,
      qui est la bonne réponse. Deux fichiers de même nature, deux réponses
      contraires, et ce qui les sépare est leur POIDS et non leur contenu. Un
      garde-fou porte sur une propriété, jamais sur un compte (R-721) : la propriété
      est ici « le fichier porte-t-il une ligne de noms de colonnes ? », et elle se
      lit dans ce qui a déjà été ouvert.
      ② UNE LIGNE MAL FORMÉE EST RENDUE SANS ALERTE. La lecture de tableau range dans
      une clé à part les cases en trop d'une ligne qui en porte plus que l'en-tête, et
      met la valeur `None` dans les cases manquantes d'une ligne qui en porte moins.
      Ni l'un ni l'autre ne fait échouer la lecture : les lignes sont rendues
      telles quelles, et c'est à l'appelant de s'en apercevoir.
      ③ ELLE PEUT RENDRE UNE LISTE VIDE, ce que son propre titre dit qu'elle ne fait
      jamais en cas d'échec. La phrase est exacte au sens strict — la liste vide n'est
      rendue que sur un fichier qui a bien été lu — mais un lecteur pressé y
      comprendra que la liste vide ne sort jamais de cette fonction, ce qui est faux.
      ④ PERSONNE NE L'APPELLE HORS DE SON PROPRE JEU DE CAS, ET UNE AUTRE FONCTION DU
      MÊME NOM, ELLE, EST APPELÉE SIX FOIS.
      programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py porte la sienne
      ligne 89 : elle reçoit en plus un séparateur, ne rattrape AUCUNE erreur et ne
      connaît pas la lecture ratée. C'est précisément le programme dont il a été
      mesuré le 28-08-2026 qu'il rend une variation latente de 0,00 euro quand il ne
      retrouve pas un cours. Deux implémentations d'une même chose divergent toujours
      (R-708) ; ici celle qui crie dort, et celle qui se tait est en service.
    ⑩ EFFET — LIT le fichier désigné, en entier, et LIT sa taille quand aucune ligne
      n'en est sortie. N'écrit aucun fichier, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main : les quatre familles d'erreurs d'ouverture,
      de conversion et de lecture de tableau sont rattrapées, et l'échec de la lecture
      de la taille l'est aussi. Aucun de ses appels ne se termine : elle ne construit
      qu'un objet de lecture ratée, dont la construction rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une lecture ratée : un objet de la classe `Illisible`, rendu à la place des
        données quand la lecture n'a pas pu se faire, et qui porte sa raison
      la marque d'ordre des octets : trois octets invisibles que certains tableurs
        posent en tête d'un fichier et qui, s'ils ne sont pas écartés, se collent au
        nom de la première colonne
      le service de mesure : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        qui calcule la performance des positions
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not chemin:
        return Illisible("chemin absent")
    try:
        with open(chemin, encoding="utf-8-sig", newline="") as f:
            r = list(csv.DictReader(f))
    except (OSError, TypeError, ValueError, csv.Error) as e:
        return Illisible(type(e).__name__, chemin)
    if not r:
        try:
            vide = os.path.getsize(chemin) < 4
        except OSError:
            vide = True
        if vide:
            return Illisible("fichier vide", chemin)
    return r


# ─────────────────────────────────────────────────────────────────────────
# CALIBRAGE — ce fichier se prouve lui-même
# ─────────────────────────────────────────────────────────────────────────

def _calibrage():
    """Rejoue des cas connus sur une partie des gestes du fichier, et rend le verdict
    avec le détail ligne à ligne.

    ① RÔLE — Donner à ce fichier le moyen de se prouver lui-même avant qu'on
      construise quoi que ce soit dessus. Il ne mesure rien de neuf : il vérifie que
      des cas dont on connaît déjà la réponse donnent toujours cette réponse.
    ② CONTEXTE D'APPEL — Un seul appelant : le lancement direct de ce fichier, une
      fois. Il n'est appelé par aucune autre fonction et par aucun autre programme :
      mesuré le 19-09-2026, une recherche du mot `_calibrage` dans tous les fichiers
      .py du dépôt ne rend, hors de ce fichier, que deux AUTRES fonctions du même nom,
      dans programmes/MODULE_JUGEMENT.py ligne 571 et programmes/MODULE_POSITIONS.py
      ligne 299, et une troisième de signature différente dans
      programmes/TENIR_LES_POSITIONS.py ligne 984.
    ③ ENTRÉE — Aucun paramètre. Tous les cas sont écrits dans son propre corps.
    ④ CONDITIONS D'ENTRÉE — Rien n'est exigé : aucun fichier, aucun réseau, aucun
      réglage. Les cas ne dépendent que des fonctions de ce fichier.
    ⑤ SORTIE — DEUX valeurs. La première dit si TOUS les cas sont passés, vrai ou
      faux. La seconde est la liste des lignes à afficher, une par cas, portant le
      libellé du cas et le mot `OK` ou `ECHEC`, suivi de ce qui a été obtenu et de ce
      qui était attendu quand le cas échoue. Mesuré le 19-09-2026 : neuf lignes,
      toutes `OK`, et un verdict vrai.
      [rend: 2]
    ⑥ TRAITEMENT — ① préparer un verdict à vrai et une liste de lignes vide · ② pour
      chaque cas, comparer ce qu'une fonction rend à ce qu'on attend, et ajouter une
      ligne · ③ les cas, dans l'ordre : les quatre écritures d'UNIBAIL font une seule
      valeur · les quatre écritures de BUREAU VERITAS font une seule valeur · un nom
      de fichier à espaces et le même à soulignés sont le même nom · le rapprochement
      ramène vers le nom attendu · le rapprochement ne perd rien en silence · une
      valeur attendue absente est signalée · un chemin absent rend une lecture ratée
      et non une liste vide · une lecture ratée se compte comme un vide · une lecture
      ratée porte sa raison · ④ rendre le verdict et les lignes.
    ⑦ UNITÉ — Les cas se comptent en NOMBRE DE CAS : il y en a neuf. Ce qu'ils
      comparent se compte en NOMBRE DE VALEURS, c'est-à-dire en nombre d'entreprises
      distinctes.
    ⑧ POURQUOI — Les écritures employées par les cas ne sont pas inventées : ce sont
      celles qui coexistaient RÉELLEMENT dans les fichiers du dépôt le 28-08-2026.
      Les trois d'UNIBAIL étaient `UNIBAIL-RODAMCO-WESTFIELD` dans l'historique figé
      des cours, `UNIBAIL_RODAMCO` dans les cours du jour et les positions ouvertes,
      et `UNIBAIL_RODAMCO_WESTFIELD` dans le tableau des trades de référence. La
      règle du projet qui l'exige veut qu'un cas au moins vienne d'une VRAIE ligne
      d'un fichier (R-732) : un cas inventé éprouve ce qu'on a imaginé, pas ce qui
      arrive.
      Le verdict est rendu à l'appelant au lieu d'être affiché ici, et les lignes
      sont rendues plutôt qu'imprimées, pour que la fonction n'ait aucun effet de
      bord : elle peut ainsi être appelée depuis un autre contrôle sans polluer son
      affichage.
      ET CE JEU DE CAS SE SABOTE CONTRE SA PROPRE CORRECTION, ce qui a été vérifié :
      le 19-09-2026, en vidant la table d'équivalences, trois cas passent au rouge —
      « les 4 graphies d'UNIBAIL font 1 valeur » rend 3 au lieu de 1, et les deux cas
      du rapprochement échouent ; et en remplaçant la mise en clé des noms par une
      fonction qui ne rapproche rien, CINQ cas sur neuf passent au rouge. Une épreuve
      qui reste verte quand on retire ce qu'elle teste n'est pas une preuve : celle-ci
      rougit, donc elle en est une.
    ⑨ CE QUI CLOCHE —
      ① LE FILET NE COUVRE QUE LA MOITIÉ DU FICHIER, ET PAS LA MOITIÉ QUI SERT. Les
      neuf cas portent sur `norm`, `norm_valeur`, `rapprocher`, `lire_csv` et la
      classe de lecture ratée. Ils ne touchent NI `trouver`, NI `trouver_tous`, NI
      `lire`, NI `date_du_nom`, NI `le_plus_recent`. Or `le_plus_recent` est la SEULE
      fonction de ce fichier que quiconque importe, et les quatre programmes qui
      l'importent le font dans le circuit du soir ou juste à côté. Mesuré le
      19-09-2026 : la sortie du fichier lancé directement affiche neuf lignes, aucune
      ne nomme `le_plus_recent`, et une recherche des mots `le_plus_recent`,
      `date_du_nom` et `REGISTRE` dans le corps de cette fonction ne rend aucune
      ligne. Le filet est tendu sous ce que personne n'emploie, et absent sous ce dont
      tout le monde dépend.
      ② UN PROGRAMME DU DÉPÔT AFFIRME LE CONTRAIRE. programmes/audit_ecosysteme.py
      porte en commentaire, lignes 189 et 190, juste avant d'importer la fonction :
      « La fonction vit dans COMMUN (R-708) et se calibre sur ce cas même. » C'est
      faux, et la mesure ci-dessus le montre. Une documentation qui promet un
      contrôle qui n'existe pas est un défaut au même titre qu'une erreur de calcul,
      parce que personne n'ira vérifier ce qu'on lui a dit d'acquis.
      ③ LE MÊME NOM SERT À DEUX CHOSES DANS LE MÊME CORPS. La lettre `b` porte
      d'abord l'ensemble des clés de BUREAU VERITAS, puis, dix lignes plus bas, le
      dictionnaire rendu par le rapprochement. Les deux usages ne se gênent pas
      aujourd'hui, le premier étant consommé avant le second ; mais un cas inséré
      entre les deux qui relirait `b` obtiendrait la valeur de l'autre, sans aucune
      erreur affichée.
      ④ LE VERDICT NE DIT PAS COMBIEN DE CAS ONT TOURNÉ. Il rend vrai ou faux, jamais
      un compte. Un jeu de cas amputé de la moitié de ses lignes rendrait donc
      exactement le même verdict vert qu'un jeu complet, et rien ne le distinguerait
      à l'affichage.
    ⑩ EFFET — Ne change rien : aucun fichier écrit, aucun accès réseau, et rien
      d'affiché. Les lignes sont RENDUES à l'appelant, qui les affiche.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas dans son état actuel.
      Aucun de ses appels ne se termine : `norm`, `norm_valeur`, `rapprocher` et
      `lire_csv` rendent tous la main.
      [sort: non]
    ⑫ DÉFINITIONS
      un cas connu : une comparaison dont la réponse est sue d'avance, rejouée pour
        vérifier qu'elle n'a pas changé
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les
        fichiers du projet
      l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de référence
        qui n'est jamais réécrit
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      la table d'équivalences : `ALIAS_VALEURS`, le dictionnaire de ce fichier qui dit quelle écriture courte désigne quelle écriture longue
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une lecture ratée : un objet de la classe `Illisible`, rendu à la place des données quand la lecture n'a pas pu se faire, et qui porte sa raison
"""
    L, ok = [], True

    def dire(lib, obtenu, attendu):
        """Compare un résultat à ce qui était attendu, et range la ligne correspondante.

        ① RÔLE — Éviter que chacun des neuf cas réécrive la même comparaison et le
          même formatage : un cas se réduit ainsi à ce qu'il éprouve.
        ② CONTEXTE D'APPEL — `_calibrage`, neuf fois par exécution, une fois par cas.
          Elle n'existe qu'à l'intérieur de cette fonction et n'est visible de nulle
          part ailleurs.
        ③ ENTRÉE — TROIS paramètres. `lib` : le libellé du cas, la phrase affichée.
          `obtenu` : ce que la fonction éprouvée a rendu. `attendu` : ce qu'elle
          devait rendre. Les neuf appels passent par exemple le libellé « les 4
          graphies d'UNIBAIL font 1 valeur », le nombre d'écritures distinctes
          obtenu, et le nombre 1.
        ④ CONDITIONS D'ENTRÉE — `obtenu` et `attendu` doivent pouvoir être comparés
          entre eux ; `lib` doit pouvoir être affiché. Elle exige aussi que le verdict
          et la liste de lignes existent déjà dans la fonction qui l'entoure.
        ⑤ SORTIE — Ne rend rien. Elle agit sur le verdict et sur la liste de lignes de
          la fonction qui l'entoure.
          [rend: rien]
        ⑥ TRAITEMENT — ① comparer ce qui est obtenu à ce qui est attendu · ② faire
          passer le verdict d'ensemble à faux si le cas échoue, sans jamais le
          remettre à vrai · ③ composer une ligne portant le libellé aligné sur
          quarante-six caractères puis `OK` ou `ECHEC` · ④ ajouter à cette ligne, en
          cas d'échec seulement, ce qui a été obtenu et ce qui était attendu ·
          ⑤ ranger la ligne dans la liste.
        ⑦ UNITÉ — Un NOMBRE DE CAS : elle en traite un par appel.
        ⑧ POURQUOI — Le verdict d'ensemble ne peut que descendre de vrai à faux, et
          jamais remonter : un cas qui passe APRÈS un cas qui échoue ne doit pas
          effacer l'échec. Et ce qui a été obtenu n'est affiché qu'en cas d'échec,
          parce qu'une sortie qui affiche tout ne se lit plus : sur neuf cas verts, la
          seule information utile est qu'ils sont verts.
        ⑨ CE QUI CLOCHE — La comparaison est une égalité simple, sans aucune
          tolérance. Elle convient aux cas d'aujourd'hui, qui comparent des nombres
          entiers, des listes et des textes ; elle serait fausse le jour où un cas
          comparerait deux nombres à virgule, deux valeurs très proches étant alors
          déclarées différentes. Aucun cas de ce genre n'existe aujourd'hui.
        ⑩ EFFET — MODIFIE le verdict et la liste de lignes de la fonction qui
          l'entoure. Aucun fichier écrit, aucun accès réseau, rien d'affiché.
        ⑪ TERMINAISON — Rend toujours la main. Elle peut LEVER si les deux valeurs
          comparées refusent de l'être, ce qui n'arrive avec aucun des neuf cas
          d'aujourd'hui. Aucun de ses appels ne se termine.
          [sort: non]
        """
        nonlocal ok
        passe = obtenu == attendu
        ok = ok and passe
        L.append(f"  {lib:<46} {'OK' if passe else 'ECHEC'}"
                 + ("" if passe else f"  obtenu {obtenu!r} attendu {attendu!r}"))

    # les trois graphies reelles d'UNIBAIL doivent faire UNE valeur
    u = {norm_valeur(x) for x in ("UNIBAIL-RODAMCO-WESTFIELD", "UNIBAIL_RODAMCO",
                                  "UNIBAIL_RODAMCO_WESTFIELD", "Unibail")}
    dire("les 4 graphies d'UNIBAIL font 1 valeur", len(u), 1)

    # les quatre graphies reelles de BUREAU VERITAS
    b = {norm_valeur(x) for x in ("BUREAU VERITAS", "BUREAU_VERITAS",
                                  "Bureau Veritas", "bureau-veritas")}
    dire("les 4 graphies de BUREAU VERITAS font 1 valeur", len(b), 1)

    # deux graphies d'un meme nom de fichier
    dire("un nom a espaces et a soulignes est le meme",
         norm("cac40 ohlcv.csv") == norm("cac40_ohlcv.csv"), True)

    # le rapprochement ramene vers le nom ATTENDU
    b, m = rapprocher({"UNIBAIL-RODAMCO-WESTFIELD": [1], "AIRBUS": [2]},
                      ["UNIBAIL_RODAMCO", "AIRBUS"])
    dire("rapprocher() ramene vers le nom attendu",
         sorted(b) == ["AIRBUS", "UNIBAIL_RODAMCO"], True)
    dire("rapprocher() ne perd rien en silence", m, [])
    _, m2 = rapprocher({"AIRBUS": [1]}, ["AIRBUS", "SAFRAN"])
    dire("une valeur attendue absente est SIGNALEE", m2, ["SAFRAN"])

    # inconnu n'est pas zero
    dire("un chemin absent rend Illisible, pas []",
         isinstance(lire_csv(None), Illisible), True)
    dire("un Illisible se comporte comme un vide", len(lire_csv(None)), 0)
    dire("un Illisible porte son motif", lire_csv(None).motif, "chemin absent")
    return ok, L


if __name__ == "__main__":
    import sys
    print(f"COMMUN v{VERSION} — calibrage\n")
    ok, lignes = _calibrage()
    for l in lignes:
        print(l)
    print("\n  " + ("CALIBRAGE OK." if ok
                    else "CALIBRAGE ECHOUE — ne rien construire dessus."))
    sys.exit(0 if ok else 1)

# ══════════════════════════════════════════════════════════════════════════
# LE PLUS RÉCENT SE LIT DANS LA DATE, JAMAIS DANS L'ALPHABET
# ══════════════════════════════════════════════════════════════════════════
# Posé le 12-09-2026 sur la question de Jean-Luc : « est-ce qu'il prend bien le
# dernier ? il regarde la date de création la plus fraîche, c'est ça ? »
# NON. Les programmes prenaient `sorted(candidats)[-1]` — le dernier par ordre
# ALPHABÉTIQUE. Et les noms du projet commencent par le JOUR DE LA SEMAINE :
#     REGISTRE_Jeu_30-07-2026 · REGISTRE_Sam_01-08-2026
#     REGISTRE_Ven_05-09-2026 · REGISTRE_Mar_09-09-2026
# L'alphabet les met dans l'ordre Jeu, Mar, Sam, Ven : il rend le 05-09 alors
# que le plus récent est le 09-09. PROUVÉ, pas supposé.
# Le commentaire du radar disait « c'est le DERNIER par ordre alphabétique qui
# fait foi » — une convention affirmée, jamais vérifiée, et fausse.
# LE DÉPÔT PORTE DEUX FORMES DE DATE, comptées : 67 noms en JJ-MM-AAAA,
# 20 en AAAA-MM-JJ, et 86 sans aucune date. La fonction lit les deux, et
# range les sans-date avant tout le reste — un fichier non daté ne peut pas
# prétendre être le plus récent.

_RE_JJMMAAAA = re.compile(r"(\d{2})-(\d{2})-(\d{4})")
_RE_AAAAMMJJ = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_RE_HEURE    = re.compile(r"(\d{2})h(\d{2})")


def date_du_nom(nom):
    """Rend la date et l'heure lues DANS le nom d'un fichier, ou des zéros s'il n'en
    porte pas.

    ① RÔLE — Donner de quand date un fichier d'après son NOM, et non d'après ce que
      le système dit de lui. Une copie, un clone ou un dépôt refait remettent à
      l'heure du jour la date que le système connaît ; le nom, lui, porte la date que
      son auteur a voulu y mettre, et il survit à toutes les copies.
    ② CONTEXTE D'APPEL — Un seul appelant, `le_plus_recent`, dans ce fichier, qui
      l'appelle une fois par candidat pour les ranger. Aucun appel depuis un autre
      programme : mesuré le 19-09-2026, une recherche du mot `date_du_nom` dans tous
      les fichiers .py du dépôt ne rend aucune ligne hors de ce fichier.
    ③ ENTRÉE — `nom` : un nom de fichier, avec ou sans son chemin. `le_plus_recent` y
      passe sans le modifier chaque élément de la liste qu'elle a reçue, et cette
      liste porte tantôt des noms seuls, tantôt des chemins complets, selon le
      programme qui appelle — par exemple
      `REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv`, seul nom de référentiel
      présent dans donnees/ le 19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Aucune : n'importe quel nom est accepté, et l'absence de
      date n'est pas une erreur. Le fichier n'a pas besoin d'exister, puisque rien
      n'est ouvert.
    ⑤ SORTIE — CINQ valeurs, dans l'ordre : année, mois,
      jour, heure, minute. Ce sont cinq zéros quand le nom ne porte aucune date
      lisible. Mesuré le 19-09-2026 :
      `REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv` rend `(2026, 8, 17, 10, 54)`,
      `rapport_boucle_2026-09-17.md` rend `(2026, 9, 17, 0, 0)`, et
      `cac40_ohlcv.csv` rend `(0, 0, 0, 0, 0)`.
      [rend: 5]
    ⑥ TRAITEMENT — ① ne garder que le nom du fichier, sans son chemin · ② y chercher
      d'abord une date écrite année-mois-jour · ③ à défaut, y chercher une date écrite
      jour-mois-année, et rendre cinq zéros si aucune des deux n'est trouvée · ④ y
      chercher une heure écrite sous la forme de deux chiffres, la lettre h, et deux
      chiffres · ⑤ construire la date pour vérifier qu'elle existe vraiment, et rendre
      cinq zéros si elle n'existe pas · ⑥ remettre l'heure à zéro si elle sort des
      bornes d'une journée · ⑦ rendre les cinq nombres.
    ⑦ UNITÉ — Des NOMBRES DE CALENDRIER : une année, un mois, un jour, une heure et
      une minute. L'heure est celle qui était écrite dans le nom au moment où le
      fichier a été produit, à Paris ; aucune conversion n'est faite ici.
    ⑧ POURQUOI — Les deux formes de date sont lues parce que le dépôt en porte
      réellement deux : mesuré le 19-09-2026 sur les 292 noms de fichiers du dépôt,
      161 sont écrits jour-mois-année, 28 sont écrits année-mois-jour, et 103 ne
      portent aucune date. Ne lire qu'une des deux formes rendrait la moitié du dépôt
      invisible au classement.
      Une date IMPOSSIBLE est refusée, et ce refus vient d'un mandat inversé du
      12-09-2026 : le nom `x_32-13-2026.md` était accepté et l'emportait sur une date
      valide, de sorte qu'un nom corrompu ou mal tapé devenait « le plus récent ».
      Construire la date pour la vérifier fait tomber le 32 janvier comme le
      30 février, sans qu'on ait à écrire soi-même les longueurs des mois.
      Les cinq zéros rendus pour un nom sans date font qu'un fichier non daté se
      range AVANT tout le reste : un fichier qui ne dit pas sa date ne peut pas
      prétendre être le plus récent.
    ⑨ CE QUI CLOCHE —
      ① UN NOM CORROMPU EST INDISCERNABLE D'UN NOM SANS DATE. Les deux rendent
      exactement cinq zéros. Mesuré le 19-09-2026 : `x_30-02-2026.md`, qui porte une
      date impossible, et `cac40_ohlcv.csv`, qui n'en porte aucune, rendent tous deux
      `(0, 0, 0, 0, 0)`. Le refus de la date impossible est juste, mais il est MUET :
      un fichier dont le nom a été mal tapé se range silencieusement parmi les
      fichiers non datés, et son auteur ne saura jamais que sa date n'a pas été lue.
      ② LE COMMENTAIRE PLACÉ AU-DESSUS ANNONCE DES COMPTES QUI NE SONT PLUS CEUX DU
      DÉPÔT. Il écrit « 67 noms en JJ-MM-AAAA, 20 en AAAA-MM-JJ, et 86 sans aucune
      date » ; la même mesure refaite le 19-09-2026 sur les 292 noms du dépôt rend
      161, 28 et 103. Un compte écrit à la main vieillit du jour où il est écrit, et
      rien ne le relit : ce qui se calcule ne s'écrit jamais à la main (R-728).
      ③ L'HEURE EST CHERCHÉE DANS TOUT LE NOM, SANS LIEN AVEC LA DATE TROUVÉE. Deux
      chiffres suivis de la lettre h et de deux chiffres suffisent, où qu'ils soient
      placés. Une heure hors bornes est ramenée à zéro heure zéro minute au lieu
      d'être signalée : mesuré le 19-09-2026, `note_12h99_2026-09-17.md` rend
      `(2026, 9, 17, 0, 0)`, l'heure `12h99` étant écartée en silence. Un fichier
      produit à midi se range donc avant un fichier produit à une heure du matin le
      même jour, sans que rien ne l'explique.
      ④ LA PREMIÈRE FORME CHERCHÉE L'EMPORTE, MÊME SI ELLE ARRIVE PLUS TARD DANS LE
      NOM. La forme année-mois-jour est cherchée avant l'autre dans le nom entier, et
      non la première date rencontrée. Mesuré le 19-09-2026 :
      `x_2026-01-05_puis_30-07-2026.md` rend `(2026, 1, 5, 0, 0)`, soit la date du
      5 janvier, alors que le nom porte ensuite celle du 30 juillet. Un nom qui
      porterait une période, ou une date d'origine suivie d'une date de reprise,
      serait donc daté par la mauvaise des deux.
    ⑩ EFFET — Ne change rien : aucun fichier n'est ouvert ni écrit, aucun accès
      réseau. Elle ne regarde que le TEXTE du nom, et le fichier peut ne pas exister.
    ⑪ TERMINAISON — Rend toujours la main : la construction d'une date impossible est
      rattrapée et rendue sous forme de cinq zéros. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un mandat inversé : une relecture faite par quelqu'un d'autre que l'auteur,
        chargée de faire tomber le code plutôt que de le confirmer
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    """
    base = os.path.basename(nom)
    m = _RE_AAAAMMJJ.search(base)
    if m:
        a, mo, j = m.group(1), m.group(2), m.group(3)
    else:
        m = _RE_JJMMAAAA.search(base)
        if not m:
            return (0, 0, 0, 0, 0)
        j, mo, a = m.group(1), m.group(2), m.group(3)
    h = _RE_HEURE.search(base)
    try:
        # UNE DATE IMPOSSIBLE N'EST PAS UNE DATE. Mandat inversé du 12-09 :
        # « x_32-13-2026.md » était accepté et l'emportait sur une date valide —
        # un nom corrompu ou mal tapé serait devenu « le plus récent ».
        # datetime.date lève ValueError sur le 32 janvier comme sur le 30 février.
        _d = _date(int(a), int(mo), int(j))
        _hh = int(h.group(1)) if h else 0
        _mm = int(h.group(2)) if h else 0
        if not (0 <= _hh <= 23 and 0 <= _mm <= 59):
            _hh = _mm = 0
        return (_d.year, _d.month, _d.day, _hh, _mm)
    except ValueError:
        return (0, 0, 0, 0, 0)


def le_plus_recent(candidats):
    """Rend, parmi une liste de fichiers, celui dont le NOM porte la date la plus
    récente.

    ① RÔLE — Choisir la bonne version d'un document dont il existe plusieurs
      exemplaires datés. C'est la SEULE fonction de ce fichier que d'autres
      programmes importent, et elle décide quel référentiel, quel registre, quel
      fichier de chiffres de référence et quel rapport le circuit du soir va lire.
    ② CONTEXTE D'APPEL — Six programmes s'en servent, aucun dans ce fichier (relevé
      par l'arbre syntaxique le 30-09-2026, relecteur) : programmes/COLLECTER_ABC_
      GITHUB.py, deux fois, pour choisir le référentiel des valeurs ·
      programmes/COMBLER_LE_TROU_DEPUIS_EURONEXT.py · programmes/GENERATEUR_COCKPIT_
      Sam_15-08-2026_21h50.py, pour choisir ses chiffres de référence et son
      rapport · programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py, par sa
      fonction `_p` puis, depuis le 30-09-2026, par `charger_referentiel`, pour
      choisir le référentiel des valeurs · programmes/TENIR_L_HISTORIQUE.py ·
      programmes/audit_ecosysteme.py. Quatre d'entre eux sont lancés directement
      chaque soir, sans intervention, par .github/workflows/collecte_abc.yml : la
      collecte, le versement de l'historique, la mesure et le radar.
    ③ ENTRÉE — `candidats` : la liste des fichiers entre lesquels choisir. Les
      appelants n'y passent PAS la même chose, et c'est à connaître (deux exemples) :
      programmes/COLLECTER_ABC_GITHUB.py y passe des noms SEULS, relevés dans le
      dossier donnees/ et commençant par `REFERENTIEL_VALEURS`, par exemple
      `REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv`, seul nom de ce genre présent
      le 19-09-2026 ; programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py y
      passe des CHEMINS complets par sa fonction `_p`, et, depuis le 30-09-2026, des
      noms SEULS par `charger_referentiel`, comme la collecte.
    ④ CONDITIONS D'ENTRÉE — La liste doit se parcourir et se trier. Une liste vide est
      acceptée. Les éléments doivent pouvoir être comparés entre eux comme des
      textes, ce qui interdit de mélanger des noms et des objets d'une autre nature.
    ⑤ SORTIE — UNE valeur : l'élément retenu, tel qu'il a été donné, ou la valeur
      `None` si la liste est vide. Mesuré le 19-09-2026 sur les quatre noms du cas
      qui a fait écrire cette fonction : elle rend `REGISTRE_Mar_09-09-2026.md`.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` si la liste est vide · ② ranger les candidats en
      les comparant d'abord sur la date lue dans leur nom, puis, à égalité, sur le nom
      lui-même · ③ rendre le dernier de ce rangement.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS : elle en rend un, ou aucun. Le rangement se fait
      sur des NOMBRES DE CALENDRIER — année, mois, jour, heure, minute.
    ⑧ POURQUOI — La question vient de Jean-Luc, le 12-09-2026 : « est-ce qu'il prend
      bien le dernier ? il regarde la date de création la plus fraîche, c'est ça ? »
      La réponse était NON. Les programmes prenaient le dernier par ordre
      ALPHABÉTIQUE, et les noms de ce projet commencent par le jour de la semaine
      abrégé. Sur les quatre noms réels `REGISTRE_Jeu_30-07-2026`,
      `REGISTRE_Sam_01-08-2026`, `REGISTRE_Ven_05-09-2026` et
      `REGISTRE_Mar_09-09-2026`, l'alphabet range Jeu, Mar, Sam, Ven et rend donc
      celui du 5 septembre, alors que le plus récent est celui du 9 septembre.
      Mesuré de nouveau le 19-09-2026 : le rangement alphabétique rend bien
      `REGISTRE_Ven_05-09-2026.md`, et cette fonction rend
      `REGISTRE_Mar_09-09-2026.md`. Le commentaire du programme de surveillance
      affirmait jusque-là que « c'est le DERNIER par ordre alphabétique qui fait
      foi » : une convention affirmée, jamais vérifiée, et fausse.
      Le nom sert de second critère, à égalité de date, pour que le résultat soit le
      même d'une exécution à l'autre : sans lui, deux fichiers portant la même date
      seraient départagés par l'ordre dans lequel le système les a rendus, qui peut
      changer d'un passage au suivant.
      La date est lue dans le NOM et non demandée au système, parce que la date que
      le système connaît est celle de la dernière copie : un dépôt cloné le matin
      donne à tous ses fichiers la date du matin, et le classement s'effondre.
    ⑨ CE QUI CLOCHE —
      ① SANS AUCUNE DATE DANS LES NOMS, ELLE REFAIT EXACTEMENT LE DÉFAUT QU'ELLE
      CORRIGE, EN SILENCE. Quand aucun candidat ne porte de date, tous rendent cinq
      zéros, et c'est le second critère — le nom — qui tranche seul : le dernier par
      ordre ALPHABÉTIQUE est rendu. Mesuré le 19-09-2026 :
      `le_plus_recent(['b.md', 'a.md', 'c.md'])` rend `c.md`. L'appelant reçoit une
      réponse d'apparence normale et n'a aucun moyen de savoir qu'aucune date n'a été
      lue.
      ② UN DE SES QUATRE APPELANTS, SI L'IMPORT ÉCHOUE, RETOMBE SUR LE PREMIER PAR
      ORDRE ALPHABÉTIQUE, SANS RIEN DIRE. Les quatre programmes se protègent
      différemment d'un import manqué : programmes/audit_ecosysteme.py et
      programmes/GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py lèvent tous deux une
      erreur qui arrête le programme, avec le message « refus de choisir un fichier
      au hasard alphabetique » ; programmes/COLLECTER_ABC_GITHUB.py n'a pas de
      protection et s'arrêterait sur l'import ; mais
      programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py, lignes 82 à 87, rend
      `sorted(trouves)[0]` — le PREMIER par ordre alphabétique — et poursuit sans
      alerte. Mesuré le 19-09-2026 sur les quatre noms du cas fondateur, ce repli
      rend `REGISTRE_Jeu_30-07-2026.md`, soit le PLUS ANCIEN des quatre. Un chemin de
      repli qui rend le contraire de ce que la fonction promet, et qui se tait, est
      pire que pas de repli du tout.
      ③ ELLE N'EST PAS ÉPROUVÉE, ET UN PROGRAMME DU DÉPÔT AFFIRME QU'ELLE L'EST. Les
      neuf cas connus rejoués par ce fichier ne la touchent pas, ni elle ni la lecture
      de date dont elle dépend — mesuré le 19-09-2026, aucune des neuf lignes
      affichées ne la nomme. Or programmes/audit_ecosysteme.py porte en commentaire,
      lignes 189 et 190, juste avant de l'importer : « La fonction vit dans COMMUN
      (R-708) et se calibre sur ce cas même. » La seule fonction partagée du fichier
      est aussi la seule dont personne ne vérifie le comportement, et un lecteur du
      programme de surveillance croira le contraire.
      ④ ELLE NE DIT PAS COMBIEN DE CANDIDATS PORTAIENT UNE DATE. Elle rend un
      fichier, et rien d'autre. Un appelant ne peut donc pas distinguer un choix fondé
      sur des dates d'un choix fondé sur l'alphabet faute de dates, ni savoir que
      trois de ses quatre candidats ont été rangés parmi les non datés.
    ⑩ EFFET — Ne change rien : aucun fichier ouvert, aucun fichier écrit, aucun accès
      réseau. La liste reçue n'est pas modifiée ; un rangement neuf est construit.
    ⑪ TERMINAISON — Rend toujours la main. Elle PEUT LEVER si les éléments de la liste
      ne se comparent pas entre eux, par exemple si l'on y mêle des textes et des
      nombres à départager à égalité de date. Aucun de ses appels ne se termine : la
      lecture de la date d'un nom rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not candidats:
        return None
    return sorted(candidats, key=lambda c: (date_du_nom(c), c))[-1]


def lire_horizon(x):
    """Lit un horizon écrit au registre des stratégies : rend un entier positif, ou None.

    ① RÔLE — **LA seule lecture d'un horizon écrit, pour tout le dépôt** (R-708) :
      le programme du soir et le juge des stratégies l'importent d'ici.
    ② CONTEXTE D'APPEL — `programmes/TENIR_LES_POSITIONS.py` (réglages du
      registre, garde-fou des horizons, affichage du soir) ; `programmes/JUGE_DES_STRATEGIES.py`
      (`porte_0`, `jouer`, `juger`).
    ③ ENTRÉE — `x` : la valeur écrite dans la colonne `horizon`, par exemple
      « 20 » ou « 20j ».
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un entier strictement positif, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les espaces et les « j » finaux · ② exiger des
      chiffres décimaux et une valeur supérieure à 0.
    ⑦ UNITÉ — Des SÉANCES de bourse.
    ⑧ POURQUOI — Écrite le 27-09-2026 dans le programme du soir (défaut 2) : une
      lecture plantait sur « ² », qui passe `isdigit` mais pas `int`, et un
      horizon à 0 mettait l'échéance sur la séance d'achat. Déplacée ici le
      28-09-2026 (défaut 4 de A-491) : le juge des stratégies lisait la même colonne par son
      propre code, `int(str(fiche["horizon"]).strip())`, qui refusait « 20j » et
      acceptait « 0 ». Deux implémentations d'une même chose divergent toujours.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    h = str(x).strip().lower().rstrip("j")
    return int(h) if h.isdecimal() and int(h) > 0 else None
