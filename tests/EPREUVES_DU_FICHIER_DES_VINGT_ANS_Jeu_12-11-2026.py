#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_FICHIER_DES_VINGT_ANS — Jeu 12-11-2026 (Paris), mission E2b du plan V7. Simulation uniquement.

① RÔLE — Éprouver le fichier des 20 ans figé (le témoin écrit par programmes/ASSEMBLER_LES_VINGT_ANS.py) par ses
  propriétés, chacune sabotée sur sa condition : P1 une seule ligne par valeur et date · P2 2024 → coupure identiques
  au maître · P3 empreinte recalculée = empreinte du contrat = empreinte du manifeste · P4 aucune ligne sans source ·
  P5 trous écrits (le manifeste dit ce que le lecteur unique mesure : séances sans cours et lignes mises à part) ·
  P6 deux vraies lignes (ACCOR 2000-01-03 = la barre de Paris de bnains ; ALSTOM 2006-08-01 = la ligne de A_VERSER) ·
  P7 le programme, relancé, rend le fichier ligne pour ligne (R-728 : le fichier se calcule, il ne s'écrit pas) ·
  P8 aucune opération connue hors du seuil de variation qui ne se voie pas au jour dit, EN ABSOLU (seuil lu dans
  CONTROLER_LES_COURS.SEUIL_VARIATION ; rien n'est comparé au manifeste) · P9 l'ancre : sur chaque ligne « ramené au
  brut » qui est la veille d'une opération de donnees/sources_bnains/DIVISIONS_BNAINS.csv, la clôture vaut la colonne
  `dernier_cours` de ce fichier (lu, rien recopié), à TOLERANCE_P9 près (constante propre, raison écrite à côté) —
  SAUF quand ce `dernier_cours` EST une barre listée fausse par donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv (sa
  date dans une fenêtre fausse, lue par `K.oter_les_barres_fausses`, la fonction du contrôle, ET sa valeur égale au
  centime à la clôture de l'extrait bnains brut ce jour-là) : une barre prouvée fausse n'est jamais une ancre (E2c) ·
  P10 la couture du maître : de la dernière séance d'avant la première date du maître à la première séance à partir
  d'elle, aucune valeur ne bouge de plus de TOLERANCE_P10 (E2c, les lignes google ramenées au brut) · P11 aucun
  aller-retour au-delà du seuil de variation (une ligne qui s'écarte de plus du seuil de la précédente ET de la
  suivante, pour revenir) et aucun trou déclaré au manifeste présent au témoin (E2c, les jours douteux de bnains) ·
  P12 aucune journée datée d'un autre jour : la majorité des barres d'un jour ne ressemble pas mieux à la veille ou au
  lendemain de l'historique réparé (E2c tour 2, B-1) · P13 à P16, l'option de A-748, pour chaque ligne « oui » de
  donnees/sources_societes_sorties/COURS_DE_REMPLACEMENT_DES_TROUS.csv : P13 elle cite une décision présente au BACKLOG
  DU COMMIT ÉPROUVÉ, mot pour mot (action, heure, réponse et question citée ; E2c tour 3, D-2), sur une ligne de
  l'action qui nomme la valeur de la ligne « oui » (E2c tour 4, m-e) · P14 le témoin porte la ligne telle quelle, source comprise · P15 elle est continue avec la veille
  et le lendemain du témoin et vaut la barre bnains démentie × les divisions que Yahoo déclare après la date (2,000 pour
  Alstom), à TOLERANCE_P15 près · P16 elle comble un trou déclaré, compté au manifeste, et lui seul · P17 (E2c tour 3,
  D-1) aux journées que `K.journees_d_un_autre_jour` dit rangées par bnains sous un autre jour (table LUE, jamais
  recalculée), chaque ligne d'origine bnains (Paris, société sortie) est ÉGALE à la ligne brute de son fichier rangée au
  jour d'à côté, lue ici en CSV.
② CONTEXTE D'APPEL — python3 -I tests/EPREUVES_DU_FICHIER_DES_VINGT_ANS_Jeu_12-11-2026.py <racine> [--saboter].
  Sans --saboter : les dix-sept propriétés. Avec : en plus, chaque sabotage, qui doit faire tomber SA propriété ; S10,
  S11, S16, S17 et S18 font le chemin de bout en bout sur une copie du dépôt (programme saboté → retrait du gel →
  --ecrire, qui doit refuser, ou épreuve, qui doit rougir) ; S12 garde la tolérance de P9. --saboter refuse de tourner (code 2) si
  programmes/ ou tests/ ont des changements non commités : S10 et S11 partent du dernier commit, les autres de l'arbre.
③ ENTRÉE — La racine d'un dépôt qui porte le témoin, son manifeste et son entrée au contrat.
④ CONDITIONS D'ENTRÉE — Exactement un fichier figé du contrat a un manifeste à côté (chemin sans « .csv » +
  « _MANIFESTE.json ») ; sinon code 2.
⑤ SORTIE — UNE valeur : le code — 0 tout tient (et, avec --saboter, chaque sabotage mord et l'épreuve J17 du compte
  des lignes jugées par P17 tient), 1 sinon, 2 épreuve
  impossible (R-734). Un sabotage « mord » quand il fait tomber sa propriété EN PLUS de celles qui tombent déjà sur
  le témoin tel quel (aucune exemption). Une ligne par propriété, puis une par sabotage.
  [rend: 1]
⑥ TRAITEMENT — Lire le témoin, le manifeste, le contrat, le maître, les deux sources des vraies lignes ; vérifier ;
  puis, avec --saboter, refaire chaque vérification sur une copie abîmée de son entrée.
⑦ UNITÉ — Des lignes ; des séances.
⑧ POURQUOI — Mission E2b (12-11-2026) : « épreuves : propriétés (…), chacune sabotée sur sa CONDITION, un cas tiré
  d'une vraie ligne (Accor 2000-01-03, Alstom 2006-08-01) ». R-731, R-732.
⑨ CE QUI CLOCHE — P8 ne voit pas une opération dont le facteur reste dans le seuil (une action gratuite pour dix,
  0,909, vaut un mouvement d'une séance) ; seul un décalage VERS PLUS TÔT ou un facteur faux se voit, un décalage
  d'une séance PLUS TARD est invisible (relecteur E2b tour 3, m3). Les sauts de clôture sont écrits au manifeste par
  le programme au gel, à titre informatif (`sauts_signales`), jamais lus ni jugés ici : une variation de plus que le seuil n'est pas un invariant des cours (244 paires
  réelles au-delà de 25 %) ; leur juge revient au lecteur unique, sur la courbe corrigée (A-713). · P9 ne porte que
  sur les opérations que bnains liste ET dont la veille est une ligne ramenée (8 au 12-11-2026, 5 valeurs) ; les
  autres ne sont pas ancrées. P9 ne voit pas une opération dont l'effet est sous TOLERANCE_P9 (PERNOD RICARD
  2009-11-18, diviseur 1,02, effet 1,96 %). P9 compte à part les ancres démenties : un `dernier_cours` pris d'une
  barre que BARRES_BNAINS_FAUSSES.csv liste (AIR LIQUIDE 2014-05-30, 97,14, document AMF) n'est ni une ancre ni un
  écart. · P10 ne regarde que la couture : un facteur faux à l'intérieur de 2024-2026 ne s'y voit que s'il change
  la couture. · P11 ne voit pas un aller-retour sous le seuil de variation (LAFARGE, −13 % les mêmes jours de
  2006-2007, ne se voyait pas avant E2c), ni une barre fausse qui dure deux séances ou plus (ce n'est plus un
  aller-retour d'une séance), ni un doublon (deux séances à la même barre : un mouvement nul), ni un échange de journée
  (m-4 du relecteur E2c tour 1) — l'échange que l'indice prouve est gardé par P17 ; le doublon reste une mesure de
  réception, pas une propriété. · P12 ne juge que jusqu'à la dernière séance de bnains, ne voit pas un échange PARTIEL
  et ne juge pas les sociétés sorties (X1 et X2 du relecteur E2c tour 2 : P12 tient) ; elle reste un filet pour un
  échange total que l'indice ne prouverait pas. · P13 lit le seul BACKLOG de la racine éprouvée (jamais origin/main) :
  aucun programme ne vérifie que Jean-Luc a dit la phrase, seulement qu'elle y est consignée (la limite que le REGISTRE
  déclare à sa v8.11 : « aucun programme ne vérifie qu'une source dit la phrase »). · P17 tient sans rien juger si la table de K est vide : ce cas est gardé par les épreuves de
  l'historique long (H69), pas ici. · P15 n'a de juge que pour une valeur dont Yahoo est au dépôt (Alstom, le 13-11-2026). Son indépendance tient à la COLONNE `dernier_cours` (jamais utilisée par
  le programme), pas au fichier : le facteur vient du même DIVISIONS_BNAINS.csv. Une
  opération retirée des DONNÉES (evenements.json et DIVISIONS_BNAINS.csv à la fois) ou un saut fabriqué dans
  l'historique réparé sont des défauts de données (R-107, R-109), hors de cette épreuve. · P2 compare au maître DU JOUR : une révision future du maître avant la coupure la fera tomber (c'est
  voulu : elle dit que la copie ne vaut plus le maître). · Les sabotages abîment les ENTRÉES des vérifications, pas le
  programme : seul P7 relance le programme (S7 le prive de la barre de Paris).
⑩ EFFET — Lit des fichiers ; le dossier courant devient la racine (le programme l'exige). N'écrit rien.
⑪ TERMINAISON — Rend la main : nombre fini de lignes, aucun réseau. Aucun de mes appels ne peut ne pas revenir.
"""
import csv
import glob
import hashlib
import importlib.util
import json
import os
import re
import statistics
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
# LA TOLÉRANCE DE P9 (superviseur R-759 de E2b, tour 3, ① a) — l'écart admis entre la clôture « ramenée au brut » de la
# veille d'une opération et le `dernier_cours` que bnains donne pour ce jour. RAISON : au-dessus de l'écart honnête
# mesuré entre les deux sources (1,2 %, EUROFINS 2020-11-18 : la clôture ramenée vient de Yahoo, `dernier_cours` de
# Paris), au-dessous du plus petit effet que P9 doit voir (une action gratuite pour dix comptée deux fois ou oubliée :
# |1 − 1/1,1| = 9,1 %). 5 % laisse une marge de part et d'autre. Elle est propre à P9 : celle de l'historique long
# (CONTROLER_L_HISTORIQUE_LONG.ACCORD) sert à autre chose et pourrait changer sans que P9 le dise (relecteur E2b tour
# 3, B1). Gardée par le sabotage S12 : au-dessus de 9,1 %, S12 ne mord plus et l'épreuve rougit. Une opération dont
# l'effet est sous cette tolérance n'est pas vue (PERNOD RICARD 2009, diviseur 1,02, 1,96 %).
TOLERANCE_P9 = 0.05
# LA TOLÉRANCE DE P10 (E2c, 12-11-2026) — la variation admise d'une valeur à la couture du maître (dernière séance avant
# sa première date → première séance à partir d'elle). RAISON : au-dessus du plus grand mouvement honnête mesuré à cette
# couture sur le fichier assemblé avec les lignes google ramenées au brut (2,63 %, PERNOD RICARD 2023-12-29 →
# 2024-01-02), au-dessous du plus petit effet qu'une ligne google NON ramenée y crée (une action gratuite pour dix
# oubliée : |1 − 1/1,1| = 9,1 % ; AIR LIQUIDE, deux attributions : −17,9 %). Gardée par S14 et S16.
TOLERANCE_P10 = 0.05
# L'ÉCART ADMIS ENTRE UNE LIGNE GOOGLE RAMENÉE ET LE MAÎTRE (P2, E2c) — la ligne du témoin × le facteur écrit dans sa
# source doit redonner le maître. RAISON : le facteur est écrit à six décimales (≈ 1,2e-6 en relatif pour 0,826446) et
# les prix à quatre (≈ 3e-7 pour 150 €) ; 1e-5 couvre les deux, et reste mille fois sous le centime d'un cours de 10 €.
TOLERANCE_P2_RAMENE = 1e-5
# `dernier_cours` est écrit au centime par la page de bnains (« 97.14 ») : une barre est la même quand sa clôture en est à
# un demi-centime au plus (P9, ancres démenties, E2c).
DERNIER_COURS_AU_CENTIME = 0.005
# P12 (E2c tour 2) : séances communes prises de chaque côté pour le rapport de référence témoin ÷ réparé, et nombre de
# barres qui doivent ressembler à un jour voisin pour signaler une journée. RAISON : 5 et 5, calibrés le 13-11-2026 —
# sur le témoin de 11h27, les 19 et 20-06-2001 sont signalés (25 barres sur 31), et aucun autre jour ; sur le témoin
# corrigé, aucun. Une valeur seule qui ressemble à la veille (deux séances voisines presque égales) ne fait pas une
# journée.
VOISINS_P12 = 5
MINIMUM_P12 = 5
# P15 (E2c tour 2, A-748) : l'écart admis entre (ligne retenue ÷ barre bnains démentie) et le facteur des divisions que
# Yahoo déclare après la date. RAISON : mesuré 2,000 ± 0,0003 sur les 13 lignes d'Alstom (rapport SOURCE_DES_28_COURS) ;
# 0,5 % couvre l'arrondi de la barre bnains au centime et reste vingt fois sous une erreur de 10 % (sabotage S22).
TOLERANCE_P15 = 0.005


def charger(racine, nom):
    """Charge un programme de programmes/ par son chemin.

    ① RÔLE — Importer le programme du dépôt éprouvé, et non un autre.
    ② CONTEXTE D'APPEL — `principal`.
    ③ ENTRÉE — `racine`, `nom` sans « .py ».
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute les déclarations du module.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    spec = importlib.util.spec_from_file_location(nom + "_epreuve", os.path.join(racine, "programmes", nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def propriete_p8(e):
    """Rend les opérations connues hors du seuil qui ne se voient pas au jour dit (la propriété P8).

    ① RÔLE — P8 en une fonction (N-1 de Cowork).
    ② CONTEXTE D'APPEL — `verifier`.
    ③ ENTRÉE — `e` : le dictionnaire de `verifier` (« lignes », « ops », « seuil », « table », « norm », « variations »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des opérations non vues (second rendu de `variations_hors_seuil`).
      [rend: 1]
    ⑥ TRAITEMENT — Un appel.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule écriture de P8, que `verifier` appelle (S8 passe par `verifier` depuis le 13-11-2026, m-c du
      relecteur E2c tour 2, pour vérifier que P8 tombe SEULE).
    ⑨ CE QUI CLOCHE — Le juge est la fonction du programme (A-727 ②).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return e["variations"](e["lignes"], e["ops"], e["seuil"], e["table"], e["norm"])[1]


def journees_datees_d_un_autre_jour(lignes, repare, fin):
    """Rend les journées du témoin dont la majorité des barres ressemble à un jour VOISIN de l'historique réparé.

    ① RÔLE — Le juge de P12, indépendant du détecteur de K (`K.journees_d_un_autre_jour`, qui lit l'indice) : il ne
      regarde que les barres du témoin et les clôtures de l'historique réparé.
    ② CONTEXTE D'APPEL — `verifier`.
    ③ ENTRÉE — `lignes` : le témoin · `repare` : {valeur : {date : clôture}} de l'historique réparé, lu en CSV par
      `principal` · `fin` : la dernière séance de bnains.
    ④ CONDITIONS D'ENTRÉE — Clôtures positives.
    ⑤ SORTIE — UNE valeur : {date : (barres qui ressemblent au jour même, barres qui ressemblent à un jour voisin,
      barres comparées)} pour les journées signalées.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque valeur que les deux fichiers portent, jusqu'à `fin` : le rapport témoin ÷ réparé de
      référence est la médiane sur les VOISINS_P12 séances communes de chaque côté ; la barre du jour « ressemble » au
      jour voisin (veille ou lendemain du réparé) quand l'écart y est STRICTEMENT plus petit qu'au jour même. Une
      journée est signalée quand les barres qui ressemblent à un voisin sont plus nombreuses que les autres et au moins
      MINIMUM_P12.
    ⑦ UNITÉ — Des rapports sans unité ; des barres.
    ⑧ POURQUOI — Relecteur E2c tour 1, B-1 : les fichiers bnains des 19 et 20-06-2001 sont échangés. Calibré le
      13-11-2026 : sur le témoin de 11h27, les 19 et 20-06-2001 seuls (25 barres sur 31 ressemblent au voisin) ; contre
      le fichier de Yahoo avant réparation, le 26-07-2007 sortait aussi (un jour où l'indice donne tort à Yahoo) —
      c'est pourquoi le juge lit l'historique réparé.
    ⑨ CE QUI CLOCHE — P12 NE VOIT PAS UN ÉCHANGE PARTIEL, ET NE JUGE PAS LES SOCIÉTÉS SORTIES. Mesuré par le relecteur
      E2c tour 2 (13-11-2026, regels jetables) : avec l'appel de `redater_les_journees` retiré de `K.lire_paris` (X1),
      9 et 11 barres restent échangées les 19 et 20-06-2001 — la règle `barre_sure` en a remplacé une partie par
      Yahoo —, le vote donne 23 contre 9 et 21 contre 11, et P12 tient ; avec l'appel retiré de la lecture N3
      d'ASSEMBLER (X2), 26 barres de sociétés sorties sont à la mauvaise date et P12 tient : elle ne juge que les
      valeurs que l'historique réparé porte. Les journées que l'indice prouve échangées sont gardées par P17 ; P12 reste
      un filet pour un échange TOTAL que l'indice ne prouverait pas. · Une journée échangée sur moins de MINIMUM_P12
      valeurs ne se voit pas ; deux séances qui ont peu bougé ne se départagent pas (CARREFOUR 60,0 contre 60,5). ·
      Au-delà de `fin`, aucun jugement (le maître n'a pas d'autre source au dépôt).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    serie = {}
    for l in lignes:
        if l[1] <= fin and l[0] in repare:
            serie.setdefault(l[0], {})[l[1]] = float(l[5])
    vote = {}
    for v, s in serie.items():
        y = repare[v]
        yd = sorted(y)
        rang = {d: i for i, d in enumerate(yd)}
        ds = [d for d in sorted(s) if y.get(d, 0) > 0]
        r = [s[d] / y[d] for d in ds]
        for i, d in enumerate(ds):
            ref = r[max(0, i - VOISINS_P12):i] + r[i + 1:i + 1 + VOISINS_P12]
            if len(ref) < VOISINS_P12:
                continue
            ref = statistics.median(ref)
            meme = abs(s[d] / (y[d] * ref) - 1)
            autre = min((abs(s[d] / (y[yd[k]] * ref) - 1) for k in (rang[d] - 1, rang[d] + 1)
                         if 0 <= k < len(yd) and y[yd[k]] > 0), default=meme)
            n = vote.setdefault(d, [0, 0])
            n[1 if autre < meme else 0] += 1
    return {d: (a, b, a + b) for d, (a, b) in vote.items() if b > a and b >= MINIMUM_P12}


def journees_hors_de_leur_fichier(lignes, table, brut_paris, brut_n3, source_paris, prefixe_sortie):
    """Rend les lignes du témoin, aux journées que bnains a rangées sous un autre jour, qui ne sont pas la ligne brute de leur
    fichier (la propriété P17).

    ① RÔLE — Le juge de P17 : une propriété EXACTE sur la date de chaque barre d'origine bnains, sans vote ni tolérance.
    ② CONTEXTE D'APPEL — `verifier`.
    ③ ENTRÉE — `lignes` : le témoin · `table` : {jour de rangement : jour vrai}, rendue par `K.journees_d_un_autre_jour`
      (LUE par `principal`, jamais recalculée ici : deux implémentations d'une même chose divergent toujours, R-708) ·
      `brut_paris` : {(valeur, date) : cinq textes (ouverture, plus haut, plus bas, clôture, volume)} de l'extrait bnains
      BRUT, lu en CSV par `principal` aux seuls jours de rangement (None quand deux barres brutes se disputent la clé :
      m-g du relecteur E2c tour 3, les deux lectures sont symétriques) · `brut_n3` : de même pour les archives N3 des
      sociétés sorties (statut GARDEE, sous le mnémonique de la table des identités ; None de même) · `source_paris` : la source d'une barre de Paris (ASSEMBLER.SOURCE_PARIS) · `prefixe_sortie` : le début de la
      source d'une barre N3 (ASSEMBLER.SOURCE_SORTIE avant « {numero} »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des lignes fautives (texte) ; le nombre de lignes jugées. Une table NON VIDE
      sans aucune ligne jugée ajoute une fautive (m-k, E2c tour 5) : P17 ne tient jamais sans avoir rien jugé. Le
      nombre est gardé par l'épreuve J17 (`lignes_que_p17_doit_juger`, m-l du relecteur E2c tour 5).
      [rend: 2]
    ⑥ TRAITEMENT — Pour chaque ligne du témoin dont la date est un jour VRAI de la table : ① source = `source_paris`,
      ou commençant par `prefixe_sortie` → la ligne brute de sa source au JOUR DE RANGEMENT (le jour j tel que
      table[j] = date de la ligne) doit exister et lui être ÉGALE, valeur par valeur, en nombres (« 23.40 » = « 23.4 ») ;
      ② source « bnains ramené au brut … » (une ligne de l'historique réparé venue de Paris, divisée par ses facteurs) →
      fautive, « non jugeable » : son égalité à la ligne brute passerait par un facteur que l'épreuve n'a pas de source
      indépendante pour lire ; ③ toute autre source (Yahoo, Google, l'option) n'est pas un fichier bnains : non jugée.
    ⑦ UNITÉ — Des lignes ; euros par titre, titres.
    ⑧ POURQUOI — Superviseur R-759 E2c tour 3 (13-11-2026), (1) couche B, après D-1 du relecteur E2c tour 2 : les
      sabotages X1 (l'appel de `redater_les_journees` retiré de `K.lire_paris`) et X2 (retiré de la lecture N3
      d'ASSEMBLER), regelés de bout en bout, laissaient TOUTES les propriétés vertes — P12 vote à la majorité et ne voit
      pas un échange partiel (la règle `barre_sure` remplace une partie des barres par Yahoo), et ne juge pas les
      sociétés sorties. La date d'une barre bnains est celle de son FICHIER, et l'indice du même fichier prouve ce jour
      (5170,49 rangé au 19-06-2001 chez bnains = Yahoo du 20) : la ligne au jour vrai doit donc être, à l'identique, la
      ligne brute rangée au jour d'à côté. Calibré le 13-11-2026 sur le regel jetable de 01h48 (sortie capturée :
      etudes/VINGT_ANS_A_PART_Mer_11-11-2026/sorties/SORTIE_E2c_TOUR3_calibrage_P13_P17.txt) : AIRBUS 2001-06-19 =
      22,35 / 23,40 / 22,35 / 23,00 / 1 653 371, la ligne brute de bnains rangée au 20 ; ALU 2001-06-19 = 25,39 /
      26,13 / 24,90 / 24,91, la ligne N3 rangée au 20 (au 19 elle vaut 24,50 : le cas qui doit échouer).
    ⑨ CE QUI CLOCHE — Si la table est VIDE, P17 tient sans rien juger : ce cas est gardé par la couche A (H69, cas connu
      des 19 et 20-06-2001, dans les épreuves de l'historique long), pas ici. Une table NON vide sans ligne jugée, en
      revanche, fait tomber P17 (m-k du superviseur E2c tour 5 : avant, si les lignes bnains de ces jours disparaissaient
      du jugement, P17 restait vraie ; sabotage S39, contre-cas S40). · Une ligne bnains ABSENTE au jour vrai
      (barre écartée par la règle des jours douteux, ou trou) n'est pas jugée : P17 juge les lignes écrites. La perte
      d'une barre par la remise au bon jour elle-même est gardée par H73, propriété de conservation de
      `redater_les_journees` (13-11-2026), dans les épreuves de l'historique long, pas ici. · Une barre seule de son
      jour laissée à la date de son fichier tombe ici par la branche `brut is None` (sabotage S28). · Une ligne
      « bnains ramené au brut » à un jour échangé fait tomber P17 sans être fausse pour autant (0 au regel de 01h48,
      même sortie : « 89 lignes jugées, fautives 0 ») :
      un humain la tranche. · P17 ne voit pas un échange que l'indice ne prouve pas (`journees_d_un_autre_jour`, ⑨).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rangee_au = {vrai: j for j, vrai in table.items()}
    fautives, jugees = [], 0
    for l in lignes:
        j = rangee_au.get(l[1])
        if j is None:
            continue
        if l[7] == source_paris or l[7].startswith(prefixe_sortie):
            jugees += 1
            brut = (brut_paris if l[7] == source_paris else brut_n3).get((l[0], j))
            if brut is None or [float(x) for x in l[2:7]] != [float(x) for x in brut]:
                fautives.append(f"{l[0]} {l[1]} {l[2:7]} contre la ligne brute rangée au {j} {brut}")
        elif l[7].startswith(source_paris + " ramené au brut"):
            jugees += 1
            fautives.append(f"{l[0]} {l[1]} « {l[7]} » : non jugeable")
    # m-k du superviseur E2c tour 5 (13-11-2026) : une table non vide où aucune ligne n'est jugée rendrait P17 vraie
    # sans rien juger — une PROPRIÉTÉ, pas un compte : table non vide ⇒ au moins une ligne jugée (sabotage S39)
    if table and not jugees:
        fautives.append(f"table non vide {sorted(table.items())}, mais aucune ligne d'origine bnains jugée à ses jours")
    return fautives, jugees


def lignes_que_p17_doit_juger(e):
    """Compte, sans passer par le juge de P17, les lignes que ce juge doit juger ; rend ce nombre.

    ① RÔLE — La valeur attendue de la seconde sortie du juge de P17 (`journees_hors_de_leur_fichier`), calculée par
      l'épreuve elle-même : l'épreuve J17 confronte les deux.
    ② CONTEXTE D'APPEL — `principal`, avec --saboter (épreuve J17) ; le balayage par mutation des journées
      (tests/outils/BALAYER_LES_MUTANTS_DES_JOURNEES.py), qui juge chaque mutant du juge par la même épreuve.
    ③ ENTRÉE — `e` : un jeu d'entrées de `verifier` (« lignes », « journees », « source_paris », « prefixe_sortie »
      sont lus).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de lignes du témoin dont la date est un jour VRAI de la table et dont la source
      est un fichier bnains — Paris, une société sortie, ou « bnains ramené au brut … ».
      [rend: 1]
    ⑥ TRAITEMENT — Un filtre sur les lignes : la date dans l'ensemble des jours vrais, la source dans l'une des trois
      familles.
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — m-l du relecteur E2c tour 5 (13-11-2026) : depuis m-k, le nombre de lignes jugées entre dans le
      verdict de P17 (une table non vide sans ligne jugée la fait tomber), et la note de livraison le citait comme
      preuve (« lignes bnains jugées : 89 ») ; aucune épreuve ne le gardait — le juge muté en « jugees += 2 » affichait
      178 sur le vrai témoin sans que rien ne rougisse. Le nombre est calculé ici, et non recopié (R-728) : un chiffre
      écrit à la main ne vaudrait que pour un témoin.
    ⑨ CE QUI CLOCHE — Le compte reprend la définition des trois familles de sources du juge (même `source_paris`, même
      `prefixe_sortie`) : une erreur commune aux deux définitions ne se verrait pas. Il ne dit rien des lignes fautives,
      que jugent P17 et ses sabotages.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    vrais = set(e["journees"].values())
    familles = (e["source_paris"], e["prefixe_sortie"], e["source_paris"] + " ramené au brut")
    return sum(1 for l in e["lignes"] if l[1] in vrais and (l[7] == familles[0] or l[7].startswith(familles[1:])))


def ecarts_de_j17(jeux):
    """Confronte, jeu par jeu, le nombre de lignes jugées par le juge de P17 au compte de l'épreuve ; rend les écarts.

    ① RÔLE — L'épreuve J17, écrite UNE fois : `principal` (avec --saboter) et le balayage par mutation des journées
      (tests/outils/BALAYER_LES_MUTANTS_DES_JOURNEES.py, `juger_p17`) l'appellent tous deux.
    ② CONTEXTE D'APPEL — `principal` ; `juger_p17` du balayage.
    ③ ENTRÉE — `jeux` : une liste de (nom du jeu, lignes jugées par le juge, compte de `lignes_que_p17_doit_juger`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts « <premier mot du nom> : jugées n, compte m », dans l'ordre des jeux ;
      vide quand J17 tient.
      [rend: 1]
    ⑥ TRAITEMENT — Une comparaison par jeu.
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — n-2 de Cowork (E2c tour 5, 13-11-2026) et superviseur R-759 E2c tour 6, (3) : la comparaison était
      écrite dans `principal` ET dans `juger_p17` (son ⑨ le déclarait) ; le balayage ne jouait que sa copie, et la ligne
      de `principal` qui portait J17 au verdict pouvait être retirée sans que rien ne rougisse. Deux implémentations
      d'une même chose divergent toujours (R-708). Le compte et les lignes jugées restent calculés par l'appelant : le
      balayage les a déjà en main pour chaque mutant (un recalcul du compte par mutant coûterait un parcours du témoin
      de plus par jeu).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [f"{nom.split()[0]} : jugées {jugees}, compte {compte}" for nom, jugees, compte in jeux if jugees != compte]


def sabotages_de_p17(e):
    """Construit les sabotages de P17 (S24, S25, S28, S30 à S40) sur un jeu d'entrées sain ; rend {nom : (cible, entrées)}.

    ① RÔLE — Les sabotages en mémoire qui donnent des dents à P17, en un seul exemplaire.
    ② CONTEXTE D'APPEL — `principal`, avec --saboter ; le balayage par mutation des journées
      (tests/outils/BALAYER_LES_MUTANTS_DES_JOURNEES.py), qui les rejoue contre chaque mutant du juge de P17.
    ③ ENTRÉE — `e` : le dictionnaire des entrées de `verifier` sur le témoin tel quel (« lignes », « journees »,
      « brut_paris », « brut_n3_rangees », « source_paris », « prefixe_sortie », « brut_paris_paires »,
      « brut_n3_paires » sont lus).
    ④ CONDITIONS D'ENTRÉE — Le témoin est trié par valeur puis par date (c'est l'écriture d'ASSEMBLER) : S28 déplace une
      ligne d'un jour à son voisin sans la déplacer dans la liste.
    ⑤ SORTIE — DEUX valeurs : {nom du sabotage : (cible, copie de `e` abîmée, `reassemble` à None)} — la cible est
      « P17 » (P17 doit tomber, elle seule) ou None (S30 : rien ne doit tomber) ; un message d'arrêt (texte) quand un
      sabotage ne trouve pas sa ligne, None sinon (le dictionnaire est alors incomplet).
      [rend: 2]
    ⑥ TRAITEMENT — Chaque ligne visée est choisie par une PROPRIÉTÉ, jamais par son nom : ① S24 (source Paris) et S25
      (société sortie) : la première ligne du témoin, à un jour de la table, dont la ligne brute de son propre jour
      existe et DIFFÈRE de celle du jour d'à côté — cette ligne brute est mise à sa place (la barre remise à la date de
      son fichier, ce que font X1 et X2) · ② S28 : la première ligne d'origine bnains (Paris ou société sortie), à un
      jour vrai d de la table, dont la ligne brute existe au jour de rangement j, n'existe PAS au jour d, et dont la
      valeur n'a aucune ligne au jour j — cette ligne est remise au jour j (la barre seule de son jour laissée à la date
      de son fichier, E1 du relecteur E2c tour 3). P17 doit la trouver par la branche `brut is None` : au jour j, la
      ligne brute attendue est celle du jour d, qui n'existe pas · ③ S30 et S31 : la première ligne de Paris à un jour
      de la table prend une source empruntée au témoin — une source qui n'est pas un fichier bnains (S30 : non jugée,
      P17 TIENT) ou « bnains ramené au brut … » (S31 : non jugeable, P17 tombe) · ④ S32 à S36 (E2c tour 5, m-i) : la
      ligne de S24 change UN seul de ses cinq champs · ⑤ S37 et S38 (m-j) : la première ligne brute (Paris, puis N3) à
      un jour de rangement dont la ligne du témoin au jour vrai est jugée est DOUBLÉE avant d'être rangée par
      `ranger_les_lignes_brutes` · ⑥ S39 (m-k) : les lignes d'origine bnains des jours vrais sortent du jugement (elles
      prennent la source prêtée de S30 ; les retirer ferait aussi tomber P5) ; S40, son contre-cas : une table vide,
      P17 TIENT.
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — Superviseur R-759 E2c tour 4 (13-11-2026), (1) 2, après D-4 du relecteur E2c tour 3 : aucun sabotage
      ne passait par la branche `brut is None` de P17 (S24 et S25 visent une ligne dont la ligne brute existe aux deux
      jours), et le seul cas réel d'une barre seule de son jour, SOLB (société sortie 72, une seule barre brute N3
      rangée au 19-06-2001, vrai jour le 20), passait toutes les épreuves sous E1′ et E2. Sabotage contre la
      correction : P17 privée de `brut is None or` doit laisser S28 manquée (sortie capturée du tour 4). S30 et S31 :
      le balayage par mutation du tour 4 (tests/outils/BALAYER_LES_MUTANTS_DES_JOURNEES.py) a trouvé trois mutants
      survivants du juge — le test de source forcé à vrai, la branche « ramené au brut » forcée à vrai ou à faux — :
      le témoin n'a, aux deux jours, que des lignes bnains (89, aucune « ramenée », aucune d'une autre source).
    ⑨ CE QUI CLOCHE — S28 ne trouve sa ligne que si le témoin porte une barre seule de son jour : sur le témoin du
      13-11-2026, c'est SOLB, et elle seule (mesure du relecteur E2c tour 3 : N3 GARDEE, {'BE0003470755':
      ['2001-06-19']}) ; une coupure ou une source qui la retirerait arrêterait l'épreuve (code 2), sans faux vert. ·
      S30 et S31 sont fabriqués (une source prêtée) : aucune vraie ligne du témoin n'est, aux deux jours, d'une autre
      source ; ils éprouvent les branches du juge, pas les données.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes, journees = e["lignes"], e["journees"]
    sabotages = {}
    for nom24, est in (("S24 une barre bnains remise à la date de son fichier", lambda s: s == e["source_paris"]),
                       ("S25 une barre N3 remise à la date de son fichier", lambda s: s.startswith(e["prefixe_sortie"]))):
        brut24 = e["brut_paris"] if nom24.startswith("S24") else e["brut_n3_rangees"]
        i24b = next((i for i, l in enumerate(lignes) if l[1] in journees and est(l[7])
                     and brut24.get((l[0], l[1])) and brut24.get((l[0], l[1])) != brut24.get((l[0], journees[l[1]]))),
                    None)
        if i24b is None:
            return sabotages, f"{nom24[:3]} ARRÊT — aucune barre à remettre à la date de son fichier : le sabotage ne s'applique pas"
        l24 = lignes[i24b][:2] + list(brut24[(lignes[i24b][0], lignes[i24b][1])]) + lignes[i24b][7:]
        sabotages[f"{nom24} ({l24[0]} {l24[1]} : clôture {lignes[i24b][5]} → {l24[5]})"] = ("P17", dict(
            e, reassemble=None, lignes=lignes[:i24b] + [l24] + lignes[i24b + 1:]))
    cles = {(l[0], l[1]) for l in lignes}
    rangee_au = {vrai: j for j, vrai in journees.items()}

    def seule(l):
        if l[1] not in rangee_au:
            return False
        if l[7] == e["source_paris"]:
            brut = e["brut_paris"]
        elif l[7].startswith(e["prefixe_sortie"]):
            brut = e["brut_n3_rangees"]
        else:
            return False
        j = rangee_au[l[1]]
        return brut.get((l[0], j)) is not None and (l[0], l[1]) not in brut and (l[0], j) not in cles
    i28 = next((i for i, l in enumerate(lignes) if seule(l)), None)
    if i28 is None:
        return sabotages, "S28 ARRÊT — aucune barre seule de son jour dans le témoin : le sabotage ne s'applique pas"
    l28 = [lignes[i28][0], rangee_au[lignes[i28][1]]] + lignes[i28][2:]
    sabotages[f"S28 une barre seule de son jour remise à la date de son fichier ({l28[0]} {lignes[i28][1]} → {l28[1]})"] = (
        "P17", dict(e, reassemble=None, lignes=lignes[:i28] + [l28] + lignes[i28 + 1:]))
    # S30 et S31 (balayage par mutation du tour 4 : les branches de SOURCE du juge n'étaient prises par aucun cas) —
    # la première ligne de Paris à un jour de la table reçoit la source d'une autre ligne du témoin, choisie par une
    # PROPRIÉTÉ : S30, la première source qui n'est ni Paris, ni une société sortie, ni « ramené au brut » (une ligne
    # qui n'est pas un fichier bnains n'est PAS jugée : P17 doit TENIR, cible None) ; S31, la première source « bnains
    # ramené au brut … » (non jugeable : P17 doit tomber)
    i30 = next((i for i, l in enumerate(lignes) if l[1] in journees and l[7] == e["source_paris"]), None)
    ramene = e["source_paris"] + " ramené au brut"
    autre = next((l[7] for l in lignes if l[7] != e["source_paris"] and not l[7].startswith(e["prefixe_sortie"])
                  and not l[7].startswith(ramene)), None)
    ramenee = next((l[7] for l in lignes if l[7].startswith(ramene)), None)
    if i30 is None or autre is None or ramenee is None:
        return sabotages, "S30 ARRÊT — pas de ligne de Paris à un jour de la table, ou pas de source à prêter : S30 et S31 ne s'appliquent pas"
    for nom30, cible30, source30 in (("S30 une ligne d'une autre source à un jour de la table, non jugée", None, autre),
                                     ("S31 une ligne « ramenée au brut » à un jour de la table, non jugeable", "P17", ramenee)):
        l30 = lignes[i30][:7] + [source30]
        sabotages[f"{nom30} ({l30[0]} {l30[1]} : source « {source30[:40]} »)"] = (
            cible30, dict(e, reassemble=None, lignes=lignes[:i30] + [l30] + lignes[i30 + 1:]))
    # S32 à S36 (m-i du relecteur E2c tour 4) : le juge compare CINQ champs ; chacun est éprouvé SEUL — la ligne de
    # Paris visée par S24 (choisie par sa propriété, ci-dessus) change ce seul champ, d'un centime pour un cours, d'un
    # titre pour le volume. P17 doit tomber à chaque fois (contre-épreuve du balayage : comparer quatre champs, ou la
    # seule clôture, laisse manqués les sabotages des champs oubliés)
    i32 = next(i for i, l in enumerate(lignes) if l[1] in journees and l[7] == e["source_paris"]
               and e["brut_paris"].get((l[0], l[1])) and e["brut_paris"].get((l[0], l[1])) != e["brut_paris"].get((l[0], journees[l[1]])))
    for k32, (code32, champ32) in enumerate((("S32", "ouverture"), ("S33", "plus haut"), ("S34", "plus bas"),
                                              ("S35", "clôture"), ("S36", "volume"))):
        l32 = list(lignes[i32])
        l32[2 + k32] = repr(float(l32[2 + k32]) + (1 if champ32 == "volume" else 0.01))
        sabotages[f"{code32} le seul champ « {champ32} » changé ({l32[0]} {l32[1]} : {lignes[i32][2 + k32]} → {l32[2 + k32]})"] = (
            "P17", dict(e, reassemble=None, lignes=lignes[:i32] + [l32] + lignes[i32 + 1:]))
    # S37 et S38 (m-j du relecteur E2c tour 4) : une ligne brute DOUBLÉE avant la lecture — rangée par la MÊME fonction
    # que `principal` (`ranger_les_lignes_brutes`, R-708) — pour l'extrait de Paris, puis pour les archives N3. La paire
    # doublée est choisie par une PROPRIÉTÉ : la première ligne brute à un jour de rangement dont la ligne du témoin au
    # jour vrai, de la même valeur et de la source correspondante, est jugée. Aucune ligne brute n'est plus « la » ligne
    # de son fichier : P17 doit tomber (contre-épreuve du balayage : « la dernière gagne » laisse le sabotage manqué)
    juges = {(l[0], l[1]): l[7] for l in lignes if l[1] in rangee_au}
    for code37, cle_paires, cle_rangees, est37 in (
            ("S37", "brut_paris_paires", "brut_paris", lambda s: s == e["source_paris"]),
            ("S38", "brut_n3_paires", "brut_n3_rangees", lambda s: s.startswith(e["prefixe_sortie"]))):
        paires = e[cle_paires]
        p37 = next((p for p in paires if p[0][1] in journees and est37(juges.get((p[0][0], journees[p[0][1]]), ""))), None)
        if p37 is None:
            return sabotages, f"{code37} ARRÊT — aucune ligne brute à doubler : le sabotage ne s'applique pas"
        sabotages[f"{code37} une ligne brute doublée avant la lecture ({cle_rangees} : {p37[0][0]} {p37[0][1]})"] = (
            "P17", dict(e, reassemble=None, **{cle_rangees: ranger_les_lignes_brutes(paires + [p37])}))
    # S39 (m-k du superviseur E2c tour 5) : les lignes d'origine bnains (Paris et sociétés sorties) des jours vrais de la
    # table SORTENT DU JUGEMENT — elles prennent la source prêtée de S30 (une source qui n'est pas un fichier bnains).
    # La table reste non vide, aucune ligne n'est jugée : P17 doit tomber. Pourquoi pas les RETIRER du témoin, comme le
    # disait le superviseur : mesuré le 13-11-2026 (copie de développement), le retrait fait tomber P17 ET P5 (des lignes
    # de sociétés sorties manquent au manifeste), et le sabotage ne serait plus propre à P17
    retirees39 = {i for i, l in enumerate(lignes) if l[1] in rangee_au
                  and (l[7] == e["source_paris"] or l[7].startswith(e["prefixe_sortie"]))}
    sabotages[f"S39 les {len(retirees39)} lignes bnains des jours de la table sorties du jugement (source « {autre[:30]} »)"] = (
        "P17", dict(e, reassemble=None, lignes=[(l[:7] + [autre] if i in retirees39 else l) for i, l in enumerate(lignes)]))
    # S40 (contre-cas de S39, balayage par mutation du tour 5 : la clause « table » de la règle m-k retirée n'était vue
    # par aucun cas) : une table VIDE n'a rien à juger, et P17 TIENT — sa vacuité est gardée par H69 (couche A), pas ici
    sabotages["S40 une table des journées vide, rien à juger (contre-cas de S39)"] = (None, dict(e, reassemble=None, journees={}))
    return sabotages, None


def ranger_les_lignes_brutes(paires):
    """Range des lignes brutes par clé ; une clé portée par deux lignes vaut None (aucune n'est « la » ligne brute).

    ① RÔLE — La lecture des lignes brutes de P17 (extrait de Paris et archives N3), en un seul exemplaire.
    ② CONTEXTE D'APPEL — `principal` (brut_paris, brut_n3_rangees) ; `sabotages_de_p17` (S37, S38) ; le balayage par
      mutation des journées, qui la remplace par « la dernière gagne » pour sa contre-épreuve.
    ③ ENTRÉE — `paires` : une liste de ((valeur, date), cinq textes), dans l'ordre du fichier.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {(valeur, date) : cinq textes, ou None si la clé apparaît plusieurs fois}.
      [rend: 1]
    ⑥ TRAITEMENT — Une passe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — m-g du relecteur E2c tour 3 : deux barres brutes pour une même clé, la dernière gagnait en silence ;
      m-j du relecteur E2c tour 4 : rien ne l'éprouvait, la lecture est isolée ici pour que S37 et S38 la rejouent.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rangees = {}
    for cle, barre in paires:
        rangees[cle] = barre if cle not in rangees else None
    return rangees


def decision_au_backlog(valeur, decision, backlog):
    """Dit si la décision citée par une ligne « oui » est au BACKLOG : son action, sa date et son heure, et la valeur de
    la ligne, sur la ligne de l'action.

    ① RÔLE — Le juge de P13.
    ② CONTEXTE D'APPEL — `verifier`.
    ③ ENTRÉE — `valeur` : la colonne `valeur` de la ligne « oui » (un mnémonique, « ALO ») · `decision` : le texte de la
      colonne `decision` · `backlog` : les lignes du BACKLOG lu par `principal`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai quand le texte commence par une action « A-n · » et cite « du JJ-MM-AAAA à HHhMM,
      « <réponse> » à : « <question> » », et qu'une ligne du BACKLOG commence par « | A-n | » et porte CE MORCEAU tel
      quel — l'heure, la réponse et la question citée mot pour mot — ET nomme `valeur` comme un mot entier (ni lettre,
      ni chiffre, ni tiret collé : « ALO » ne se trouve pas dans « ALOX ») ; faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — Trois motifs, une recherche.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur E2c tour 1, ③ 2 (a) : une ligne retenue sans décision écrite serait un choix du Chat.
      Superviseur E2c tour 3, (2) 2 (13-11-2026), après D-2 du relecteur E2c tour 2 : avec l'action et l'heure seules,
      « A-748 · n'importe quoi du 12-11-2026 à 23h47 » était accepté, et l'heure de 22h45 (« chercher une autre source,
      et sinon un trou déclaré », qui n'autorise aucun « oui ») aussi. Relecteur E2c tour 3, m-e (13-11-2026) : la
      valeur n'était pas reçue — une ligne « oui » d'une AUTRE valeur citant la décision d'Alstom passait P13 (seules P15
      et P16 la rattrapaient) ; la valeur est désormais exigée sur la ligne de l'action (sabotage S29).
    ⑨ CE QUI CLOCHE — Aucun programme ne vérifie que Jean-Luc a dit la phrase (la limite que le REGISTRE déclare à sa
      v8.11 : « aucun programme ne vérifie qu'une source dit la phrase ») : P13 vérifie seulement qu'elle est consignée,
      mot pour mot, dans le BACKLOG du commit éprouvé. · Le SENS n'est pas jugé :
      une question citée exactement qui n'autoriserait pas un « oui » passerait, et un texte qui CONTREDIT la décision
      suivi de la citation exacte aussi (mesuré par le relecteur E2c tour 3, m-e) ; la décision de 22h45 est refusée
      parce que sa citation (heure, réponse, question) ne figure pas sous cette forme à la ligne A-748, pas parce que le
      programme la comprend. · La VALEUR est jugée par sa présence sur la ligne, pas par son rôle : une valeur NOMMÉE
      sur la ligne de l'action sans être l'objet de la décision passe, MÊME NOMMÉE POUR EN ÊTRE EXCLUE. MESURE (m-h du
      relecteur E2c tour 4 ; E2c tour 5, 13-11-2026, avec `nommee_sur_la_ligne`, l'expression même du juge — sortie
      etudes/VINGT_ANS_A_PART_Mer_11-11-2026/sorties/SORTIE_E2c_TOUR5_m-h_valeurs_nommees_sur_A-748.txt) : sur la
      ligne A-748, 7 valeurs du témoin sur 71 sont nommées — ALO, la valeur de la décision, et 6 autres ; parmi ces 6,
      5 sont nommées dans la phrase qui les EXCLUT (« Les 67 autres barres fausses du même épisode (AIR LIQUIDE,
      DANONE, ESSILORLUXOTTICA, PERNOD RICARD, VINCI) ne relèvent PAS de cette décision »), la sixième est LI. Une
      ligne « oui » de l'une de ces 6 valeurs citant la décision d'Alstom passerait donc P13 ; P15 et P16 la
      rattraperaient. Ce compte vaut pour la ligne A-748 du BACKLOG mesuré ; il change avec elle. Valeur et sens sont
      deux limites distinctes ; le sens n'est pas jugeable par programme (superviseur E2c tour 4, m-e).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a = re.match(r"(A-\d+) · ", decision or "")
    q = re.search(r"du \d\d-\d\d-\d{4} à \d\dh\d\d, « [^«»]+ » à : « [^«»]+ »", decision or "")
    return bool(a and q and valeur) and any(l.startswith(f"| {a.group(1)} |") and q.group(0) in l
                                            and nommee_sur_la_ligne(valeur, l) for l in backlog)


def nommee_sur_la_ligne(valeur, ligne):
    """Dit si `valeur` est nommée sur `ligne` comme un mot entier (ni lettre, ni chiffre, ni tiret collé).

    ① RÔLE — L'expression du juge de P13 pour « la valeur est nommée », en un seul exemplaire.
    ② CONTEXTE D'APPEL — `decision_au_backlog` ; la mesure du ⑨ de `decision_au_backlog` (m-h, E2c tour 5).
    ③ ENTRÉE — `valeur` : un mnémonique · `ligne` : une ligne du BACKLOG.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai quand la valeur est nommée sur la ligne ; faux sinon (et pour une valeur vide).
      [rend: 1]
    ⑥ TRAITEMENT — Une expression régulière : la valeur, ni précédée ni suivie d'une lettre, d'un chiffre ou d'un tiret.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « ALO » ne doit pas se trouver dans « ALOX ». La mesure du ⑨ de `decision_au_backlog` doit compter
      avec la MÊME expression que le juge (deux implémentations d'une même chose divergent toujours, R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return bool(valeur) and re.search(r"(?<![\w-])" + re.escape(valeur) + r"(?![\w-])", ligne) is not None


def verifier(e):
    """Vérifie les dix-sept propriétés sur un jeu d'entrées ; rend {propriété : (tient, détail)}.

    ① RÔLE — Les vérifications elles-mêmes, une fonction pour le cas sain et pour chaque sabotage.
    ② CONTEXTE D'APPEL — `principal`.
    ③ ENTRÉE — `e` : dictionnaire — « lignes » (listes de huit textes, sans l'en-tête), « octets » (du témoin),
      « sha_contrat », « manifeste », « maitre » (lignes du maître), « table » (écriture normalisée → mnémonique, du
      lecteur), « norm » (la normalisation du lecteur), « lecture » (rendu de `mesurer_les_trous` sur le témoin),
      « paris_accor », « yahoo_alstom » (les vraies lignes lues dans leurs sources), « reassemble » (lignes rendues
      par le programme relancé, ou None), « ops » (opérations de RECONSTRUIRE), « seuil » (lu), « variations » (la
      fonction `ASSEMBLER.variations_hors_seuil`), « divisions » (DIVISIONS_BNAINS.csv lu par `R.lire_divisions`),
      « tolerance_p9 » (TOLERANCE_P9), « ancres_fausses » (les (valeur, date) de DIVISIONS_BNAINS.csv dont le
      `dernier_cours` est une barre listée fausse, calculées par `principal`), « tolerance_p10 » (TOLERANCE_P10), « prefixe_google », « source_google »
      (le début de la source d'une ligne google ramenée et la source google, lus dans le programme), « repare »,
      « fin_bnains », « option », « backlog », « n3_brut », « divisions_yahoo » (E2c tour 2, lus par `principal`),
      « journees », « brut_paris », « brut_n3_rangees », « source_paris », « prefixe_sortie » (E2c tour 3, P17).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {« P1 » … « P17 » : (booléen, texte)} ; P7 seulement quand « reassemble » n'est pas None.
      [rend: 1]
    ⑥ TRAITEMENT — Voir ① du fichier ; la tolérance de P9 est TOLERANCE_P9 (sa raison est écrite à sa déclaration).
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — P1 range une valeur d'aujourd'hui sous son mnémonique (deux écritures d'un même nom sont la
      même clé) et une société sortie sous son texte.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m, lignes, r = e["manifeste"], e["lignes"], {}
    cle = lambda l: (e["table"].get(e["norm"](l[0]), "sortie:" + l[0]), l[1])
    cles = [cle(l) for l in lignes]
    r["P1"] = (len(set(cles)) == len(cles), f"{len(cles) - len(set(cles))} clé(s) en double sur {len(cles)}")
    # la fenêtre de P2 ne se lit pas au manifeste (critère ③ du superviseur R-759 de E2b, tour 3) : la fin est celle que
    # le contrat déclare, le début la première date du maître lui-même
    fin, debut = e["fin_contrat"], min(l[1] for l in e["maitre"])
    # E2c : une ligne « google » du maître touchée par une opération postérieure est ramenée au brut ; elle doit
    # redonner le maître multipliée par le facteur écrit dans sa source (TOLERANCE_P2_RAMENE), toute autre ligne est
    # identique
    du_maitre = {(l[0], l[1]): tuple(l) for l in e["maitre"] if l[1] <= fin}
    copie = {(l[0], l[1]): tuple(l) for l in lignes if l[1] >= debut and e["norm"](l[0]) in e["table"]}
    differentes, ramenees_p2 = len(set(du_maitre) ^ set(copie)), 0
    for k in set(du_maitre) & set(copie):
        m_, c_ = du_maitre[k], copie[k]
        if c_[7].startswith(e["prefixe_google"]) and m_[7] == e["source_google"]:
            ramenees_p2 += 1
            p = float(c_[7][len(e["prefixe_google"]):])
            prix = all(abs(float(c) * p / float(x) - 1) <= TOLERANCE_P2_RAMENE for c, x in zip(c_[2:6], m_[2:6]))
            vol = abs(float(c_[6]) - float(m_[6]) * p) <= 1 + float(m_[6]) * TOLERANCE_P2_RAMENE
            differentes += not (prix and vol)
        else:
            differentes += m_ != c_
    r["P2"] = (differentes == 0, f"maître ≤ {fin} : {len(du_maitre)} lignes · copie : {len(copie)} · dont google "
                                 f"ramenées au brut : {ramenees_p2} · différentes : {differentes}")
    sha = hashlib.sha256(e["octets"]).hexdigest()
    r["P3"] = (sha == e["sha_contrat"] == m["sha256"], f"recalculée {sha[:16]} · contrat {e['sha_contrat'][:16]} · "
                                                         f"manifeste {m['sha256'][:16]}")
    vides = sum(1 for l in lignes if len(l) != 8 or not l[7].strip())
    r["P4"] = (vides == 0, f"{vides} ligne(s) sans source")
    lu, ecrit = e["lecture"], m["lecture_par_le_lecteur_unique"]
    hors = sum(1 for l in lignes if e["norm"](l[0]) not in e["table"])
    r["P5"] = (lu["trous"] == ecrit["trous"] and lu["seances_sans_cours"] == ecrit["seances_sans_cours"]
               and ecrit["lignes_mises_a_part"] == lu["lignes_mises_a_part"] == hors,
               f"séances sans cours : lecteur {lu['seances_sans_cours']}, manifeste {ecrit['seances_sans_cours']} · "
               f"lignes mises à part : lecteur {lu['lignes_mises_a_part']}, manifeste {ecrit['lignes_mises_a_part']}, "
               f"sociétés sorties écrites {hors}")
    t = {(l[0], l[1]): l for l in lignes}
    a, p = t.get(("ACCOR", "2000-01-03")), e["paris_accor"]
    al, y = t.get(("ALO", "2006-08-01")), e["yahoo_alstom"]
    ok_a = a is not None and [float(x) for x in a[2:7]] == [float(x) for x in p[4:9]] and a[7] == "bnains"
    ok_al = al is not None and al[2:8] == y[2:8]
    r["P6"] = (ok_a and ok_al, f"ACCOR 2000-01-03 {a} contre bnains {p} · ALO 2006-08-01 {al and al[2:7]} contre "
                               f"A_VERSER {y[2:7]}")
    non_vues = propriete_p8(e)
    r["P8"] = (non_vues == [],
               f"seuil lu {e['seuil']} · opérations non vues : "
               f"{len(non_vues)} {non_vues[:3]}")
    ramenees = {(e["table"].get(e["norm"](l[0]), l[0]), l[1]): l for l in lignes if "ramené au brut" in l[7]}
    ancrees, ecarts, dementies = 0, [], []
    for d in e["divisions"]:
        l = ramenees.get((e["table"].get(e["norm"](d["valeur"]), d["valeur"]), d["date_dernier_cours"]))
        if l is None:
            continue
        # E2c : une veille dont la barre est listée fausse (BARRES_BNAINS_FAUSSES.csv) n'est pas une ancre — la page de
        # bnains recopie alors la barre fausse dans `dernier_cours` (AIR LIQUIDE 2014-05-30 : 97,14, document AMF)
        if (d["valeur"], d["date_dernier_cours"]) in e["ancres_fausses"]:
            dementies.append(f"{d['valeur']} {d['date_dernier_cours']}")
            continue
        ancrees += 1
        if abs(float(l[5]) / float(d["dernier_cours"]) - 1) > e["tolerance_p9"]:
            ecarts.append(f"{d['valeur']} {d['date_dernier_cours']} : témoin {l[5]} contre dernier_cours "
                          f"{d['dernier_cours']} (opération du {d['date']})")
    r["P9"] = (ancrees > 0 and not ecarts, f"{ancrees} veille(s) d'opération ancrée(s) à {e['tolerance_p9']:.0%} près · "
                                           f"écarts : {len(ecarts)} {ecarts} · ancres démenties par une preuve "
                                           f"officielle, non comptées : {len(dementies)} {dementies}")
    # P10 (E2c, B2) : la couture du maître — la première date du maître est lue dans le maître lui-même
    series = {}     # par mnémonique : les deux écritures d'un même nom (« AIR LIQUIDE », « AIR_LIQUIDE ») se suivent
    for l in lignes:
        series.setdefault(e["table"].get(e["norm"](l[0]), l[0]), []).append((l[1], float(l[5])))
    sauts_couture = []
    for v, s in series.items():
        avant = [x for x in s if x[0] < debut]
        apres = [x for x in s if x[0] >= debut]
        if avant and apres:
            (d0, c0), (d1, c1) = max(avant), min(apres)
            if abs(c1 / c0 - 1) > e["tolerance_p10"]:
                sauts_couture.append(f"{v} {d0} {c0} → {d1} {c1} ({c1 / c0 - 1:+.1%})")
    r["P10"] = (not sauts_couture, f"couture du {debut}, tolérance {e['tolerance_p10']:.0%} · sauts : "
                                   f"{len(sauts_couture)} {sorted(sauts_couture)[:3]}")
    # P11 (E2c, jours douteux) : aucun aller-retour d'une séance au-delà du seuil lu, aucun trou déclaré écrit
    allers = []
    for v, s in series.items():
        s.sort()
        for (_, c0), (d1, c1), (_, c2) in zip(s, s[1:], s[2:]):
            if (abs(c1 / c0 - 1) > e["seuil"] and abs(c2 / c1 - 1) > e["seuil"]
                    and abs(c2 / c0 - 1) <= e["seuil"]):
                allers.append(f"{v} {d1}")
    cles_ecrites = {(l[0], l[1]) for l in lignes}
    trous_ecrits = [f"{v} {d}" for v, d, *_ in m.get("trous_declares", []) if (v, d) in cles_ecrites]
    r["P11"] = (not allers and not trous_ecrits and "trous_declares" in m,
                f"seuil lu {e['seuil']} · allers-retours : {len(allers)} {allers[:3]} · trous déclarés au manifeste : "
                f"{len(m.get('trous_declares', []))}, dont écrits au témoin : {len(trous_ecrits)} {trous_ecrits[:3]}")
    # P12 (E2c tour 2, B-1) : aucune journée datée d'un autre jour, jugée sans K, contre l'historique réparé
    echangees = journees_datees_d_un_autre_jour(lignes, e["repare"], e["fin_bnains"])
    r["P12"] = (not echangees, f"journées où la majorité des barres ressemble à un jour voisin de l'historique réparé : "
                               f"{len(echangees)} {sorted(echangees.items())[:3]}")
    # P13 à P16 (E2c tour 2, A-748) : l'option de remplacement, ligne « oui » par ligne « oui »
    oui = [o for o in e["option"] if o[8] == "oui"]
    t_ = {(l[0], l[1]): l for l in lignes}
    sans_decision = [f"{o[0]} {o[1]}" for o in oui if not decision_au_backlog(o[0], o[9], e["backlog"])]
    r["P13"] = (not sans_decision, f"lignes « oui » : {len(oui)} · sans décision présente au BACKLOG : "
                                   f"{len(sans_decision)} {sans_decision[:3]}")
    mal_ecrites = [f"{o[0]} {o[1]}" for o in oui if t_.get((o[0], o[1])) != o[:8]]
    r["P14"] = (not mal_ecrites, f"lignes « oui » absentes du témoin ou écrites autrement (source comprise) : "
                                 f"{len(mal_ecrites)} {mal_ecrites[:3]}")
    implausibles = []
    for o in oui:
        s = series.get(e["table"].get(e["norm"](o[0]), o[0]), [])
        dates = [x[0] for x in s]
        i = dates.index(o[1]) if o[1] in dates else None
        c = float(o[5])
        brut = e["n3_brut"].get((o[0], o[1]))
        attendu = 1.0
        for x, f in e["divisions_yahoo"].get(o[0], []):
            if x > o[1]:
                attendu *= f
        if (i is None or i == 0 or i == len(s) - 1 or abs(c / s[i - 1][1] - 1) > e["seuil"]
                or abs(s[i + 1][1] / c - 1) > e["seuil"] or brut is None or not e["divisions_yahoo"].get(o[0])
                or abs(c / brut / attendu - 1) > TOLERANCE_P15):
            implausibles.append(f"{o[0]} {o[1]} (rapport à la barre bnains {c / brut if brut else None}, attendu "
                                f"{attendu})")
    r["P15"] = (not implausibles, f"lignes « oui » discontinues ou hors du facteur prouvé par les divisions de Yahoo "
                                  f"(à {TOLERANCE_P15:.1%}) : {len(implausibles)} {implausibles[:3]}")
    combles = {(x[0], x[1]) for x in m.get("trous_combles_par_l_option", [])}
    hors = sorted(f"{o[0]} {o[1]}" for o in oui if (o[0], o[1]) not in combles)
    r["P16"] = (not hors and "trous_combles_par_l_option" in m and len(combles) == len(oui),
                f"lignes « oui » hors d'un trou déclaré comblé : {len(hors)} {hors[:3]} · trous comblés au manifeste : "
                f"{len(combles)}")
    # P17 (E2c tour 3, D-1) : chaque barre d'origine bnains d'une journée rangée sous un autre jour est la ligne brute de
    # son fichier, rangée au jour d'à côté — égalité exacte, sans vote
    fautives, jugees = journees_hors_de_leur_fichier(lignes, e["journees"], e["brut_paris"], e["brut_n3_rangees"],
                                                      e["source_paris"], e["prefixe_sortie"])
    r["P17"] = (not fautives, f"journées rangées sous un autre jour (lues par K) : {sorted(e['journees'].items())} · "
                              f"lignes bnains jugées : {jugees} · différentes de la ligne brute de leur fichier : "
                              f"{len(fautives)} {fautives[:2]}")
    if e["reassemble"] is not None:
        rl = [list(x) for x in e["reassemble"]]
        r["P7"] = (rl == lignes, f"relancé : {len(rl)} lignes, témoin : {len(lignes)}, "
                                 f"différentes : {sum(1 for x, y in zip(rl, lignes) if x != y) + abs(len(rl) - len(lignes))}")
    return r


def principal(argv):
    """Lit, vérifie, sabote ; rend le code de sortie.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : racine, --saboter.
    ④ CONDITIONS D'ENTRÉE — ④ du fichier.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Avec --saboter, d'abord le refus d'un arbre sale (m4). Lectures (DIVISIONS_BNAINS vide ou des
      opérations vides arrêtent, code 2) ; `verifier` sur le cas sain ;
      avec --saboter : S1 à S6 abîment une entrée et doivent faire tomber leur propriété, et elle seule, EN PLUS de
      celles qui tombent déjà ; S8 (en mémoire) inverse le facteur d'une opération jugée et doit faire tomber P8 seule
      — S8 garde la PROPRIÉTÉ P8, S10 et S11 gardent le DÉTECTEUR du programme (le refus de --ecrire) ; S12 (en mémoire) compte deux fois l'attribution de la veille ancrée à l'effet le plus
      petit et doit ajouter un écart à P9 ; S7 relance le programme saboté (P7) ; S10 et S11 font le chemin de bout en
      bout (`chemin_complet`). E2c : S13 (P9 sans la liste des barres fausses), S14 (lignes google remises comme le
      maître → P10), S15 (une barre de Paris refusée remise → P11), en mémoire, comme S1 à S6 ; S16 (B2 retiré du
      programme → P10), S17 (règle des jours douteux retirée → P11), S18 (trou déclaré retiré → P11), de bout en bout.
      E2c tour 2 : S19 (deux séances échangées → P12), S20 à S23 (l'option → P13 à P16), en mémoire ; S8 rejoue P8 pour
      CHAQUE opération que le fichier des opérations de RECONSTRUIRE dit jugée (N-1), par `verifier` (P8 seule, m-c du
      tour 3). E2c tour 3 : S24 et S25 (une barre bnains, une barre N3, remises à la date de leur fichier → P17), S26
      et S27 (une décision inventée, l'heure d'une autre décision → P13), en mémoire. E2c tour 4 : S28 (une barre seule
      de son jour remise à la date de son fichier → P17, par la branche `brut is None`) et S29 (la décision portée par
      une autre valeur → P13), S30 (une ligne d'une autre source à un jour de la table : un contre-cas, rien ne doit
      tomber) et S31 (une ligne « ramenée au brut » → P17), en mémoire. E2c tour 5 : S32 à S36 (un seul champ changé →
      P17, m-i), S37 et S38 (une ligne brute doublée → P17, m-j), S39 (les lignes jugées sorties du jugement, table non
      vide → P17, m-k) et son contre-cas S40 (une table vide : rien ne doit tomber), en mémoire. Le refus d'arbre sale porte sur
      tout l'arbre, fichiers non suivis compris (M-3). E2c tour 6 (n-2) : J17 par `ecarts_de_j17`, la fonction que le
      balayage appelle aussi ; chaque verdict partiel (sabotages, J17, S8, S12, S7, S10, S11) passe par le seul geste
      `verdict`, qui imprime sa ligne et l'ajoute à la liste dont RÉSULTAT est la conjonction.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit ; affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1 or not os.path.isdir(args[0]) or [a for a in argv if a.startswith("--") and a != "--saboter"]:
        print("USAGE : EPREUVES_DU_FICHIER_DES_VINGT_ANS_Jeu_12-11-2026.py <racine> [--saboter]")
        return 2
    racine = os.path.abspath(args[0])
    if "--saboter" in argv:   # relecteur E2b tour 3, m4 : un seul état jugé — l'arbre propre, qui est le dernier commit
        import subprocess
        try:
            # M-3 de Cowork (E2b) : TOUT l'arbre, fichiers non suivis compris — l'état jugé est le commit cloné, et un
            # contrôle qui nomme des dossiers change d'avis quand on en renomme un
            sale = subprocess.run(["git", "-C", racine, "status", "--porcelain"],
                                  capture_output=True, text=True, timeout=120, check=True).stdout.strip()
        except Exception as x:   # noqa: BLE001
            print(f"ARRÊT — l'état de l'arbre n'a pas pu être lu : {type(x).__name__} : {x}")
            return 2
        if sale:
            print("ARRÊT — --saboter refuse un arbre avec des changements non commités ou des fichiers non suivis "
                  "(les chemins complets jugeraient le dernier commit, les autres l'arbre) : "
                  + " · ".join(sale.splitlines()[:5]))
            return 2
    try:
        A = charger(racine, "ASSEMBLER_LES_VINGT_ANS")
        C = charger(racine, "CONTRATS_DES_FICHIERS")
        temoins = [c for c in C.FICHIERS_DE_COURS_FIGES
                   if os.path.exists(os.path.join(racine, c[:-4] + "_MANIFESTE.json"))]
        if len(temoins) != 1:
            print(f"ARRÊT — {len(temoins)} fichier(s) figé(s) avec un manifeste au contrat (1 attendu) : {temoins}")
            return 2
        chemin = temoins[0]
        with open(os.path.join(racine, chemin), "rb") as f:
            octets = f.read()
        lignes = list(csv.reader(octets.decode("utf-8").splitlines()))
        if lignes[0] != C.COURS_MAITRE:
            print(f"ARRÊT — en-tête {lignes[0]}")
            return 2
        lignes = lignes[1:]
        with open(os.path.join(racine, chemin[:-4] + "_MANIFESTE.json"), encoding="utf-8") as f:
            manifeste = json.load(f)
        with open(os.path.join(racine, "donnees", "cours_maitre.csv"), encoding="utf-8", newline="") as f:
            maitre = [l for l in csv.reader(f) if l][1:]
        lc = A._lecteur()
        table, _ = lc.table_des_ecritures(racine)
        with open(os.path.join(racine, "donnees", "sources_bnains", "bnains_cac40.csv"), encoding="utf-8") as f:
            paris_accor = next(l for l in csv.reader(f) if l[:2] == ["ACCOR", "2000-01-03"])
        with open(os.path.join(racine, A.YAHOO_SORTIES), encoding="utf-8") as f:
            yahoo_alstom = next(l for l in csv.reader(f) if l[:2] == ["ALSTOM", "2006-08-01"])
        lecture = A.mesurer_les_trous(racine, chemin)
        reassemble, _ = A.assembler(racine, C.FICHIERS_DE_COURS_FIGES[chemin]["fin"])
        _, ops = A.operations(racine)
        seuil = A.seuil_de_variation()
        divisions = A.R.lire_divisions(os.path.join(racine, A.R.DIVISIONS))
        # UNE SOURCE VIDE EST UNE ERREUR DE CHARGEMENT, JAMAIS UNE LISTE VIDE (superviseur R-759 de E2b avant le tour 5,
        # ① b) : `R.lire_divisions` rend [] pour un fichier absent, et son ⑧ le veut ainsi pour RECONSTRUIRE ; ici, P9
        # vide jugerait sur rien, et des opérations vides rendraient P8 vraie à vide. Même garde que REPARER l. 1508-1513.
        if not divisions:
            raise OSError(f"{A.R.DIVISIONS} absent ou vide : P9 n'aurait rien à ancrer")
        if not any(ops.values()):
            raise ValueError("aucune opération sur titre lue : P8 serait vraie à vide")
        # E2c : une ancre est DÉMENTIE quand son `dernier_cours` EST une barre que BARRES_BNAINS_FAUSSES.csv liste
        # fausse — la veille tombe dans une fenêtre fausse (lue par `K.oter_les_barres_fausses`, la fonction du
        # contrôle, appliquée à une copie des veilles rangée comme un extrait bnains) ET `dernier_cours` vaut la
        # clôture de l'extrait bnains BRUT ce jour-là, au centime (DERNIER_COURS_AU_CENTIME). Mesuré le 12-11-2026 :
        # AIR LIQUIDE 2014-05-30, 97,14 = la barre fausse 97,14 → démentie ; AIR LIQUIDE 2012-05-30, 95,07 contre la
        # barre fausse 86,23 → la page a pris le vrai cours ailleurs, l'ancre reste.
        veilles = {}
        for d in divisions:
            veilles.setdefault(d["valeur"], {})[d["date_dernier_cours"]] = None
        listees = A.K.oter_les_barres_fausses(os.path.join(racine, A.K.FAUSSES), veilles)
        brut, defauts_brut, _ = A.K.lire_cours(os.path.join(racine, A.K.BNAINS), A.COURS_BNAINS)
        if defauts_brut:
            raise ValueError(f"extrait bnains illisible : {defauts_brut[:3]}")
        ancres_fausses = {(d["valeur"], d["date_dernier_cours"]) for d in divisions
                          if (d["valeur"], d["date_dernier_cours"]) in listees
                          and d["date_dernier_cours"] in brut.get(d["valeur"], {})
                          and abs(brut[d["valeur"]][d["date_dernier_cours"]][3] - float(d["dernier_cours"]))
                          <= DERNIER_COURS_AU_CENTIME}
        # E2c tour 2 — P12 : l'historique réparé, lu en CSV (pas par K) ; P13 à P16 : l'option de A-748, les BACKLOG
        # (celui de la racine et celui d'origin/main, où les décisions s'écrivent), les barres bnains N3 démenties et les
        # divisions que Yahoo déclare, tous lus ici
        repare = {}
        with open(os.path.join(racine, A.K.FICHIER), encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                repare.setdefault(row["valeur"], {})[row["date"]] = float(row["close"])
        option = []
        if os.path.exists(os.path.join(racine, A.SOURCE_RECOUPEE)):
            with open(os.path.join(racine, A.SOURCE_RECOUPEE), encoding="utf-8", newline="") as f:
                rows = [x for x in csv.reader(f) if x]
            if rows[0] != C.COURS_DE_REMPLACEMENT_DES_TROUS:
                raise ValueError(f"{A.SOURCE_RECOUPEE} : en-tête {rows[0]}")
            option = rows[1:]
        # E2c tour 3, D-2 : P13 juge l'état ÉPROUVÉ — le BACKLOG de la racine, et lui seul (jamais origin/main, une
        # référence qui bouge et qui est extérieure au commit) ; absent → aucune décision trouvée, P13 tombe
        backlog = []
        if os.path.exists(os.path.join(racine, "BACKLOG_DECISIONS.md")):
            with open(os.path.join(racine, "BACKLOG_DECISIONS.md"), encoding="utf-8") as f:
                backlog = f.read().splitlines()
        voulues = {(o[0], o[1]) for o in option if o[8] == "oui"}
        with open(os.path.join(racine, A.IDENTITES), encoding="utf-8", newline="") as f:
            mnemos = {}
            for row in csv.DictReader(f):
                if row["isin"]:
                    mnemos.setdefault(row["isin"], set()).add(row["mnemonique"])
        # E2c tour 3, P17 : la table des journées rangées sous un autre jour est LUE par la fonction de K (R-708), et les
        # lignes brutes de leurs fichiers sont lues ICI, en CSV, aux seuls jours de rangement — jamais par `K.lire_paris`
        # ni par la lecture N3 d'ASSEMBLER, qui sont ce que P17 éprouve
        journees = A.K.journees_d_un_autre_jour(racine)
        brut_paris_paires = []
        with open(os.path.join(racine, A.K.BNAINS), encoding="utf-8", newline="") as f:
            lecteur_b = csv.reader(f)
            tete_b = next(lecteur_b)
            cols_b = [tete_b.index(c) for c in ("open", "high", "low", "close", "volume")]
            for row in lecteur_b:
                if row and row[1] in journees:
                    brut_paris_paires.append(((row[0], row[1]), [row[c] for c in cols_b]))
        # m-g du relecteur E2c tour 3 : lue comme N3 — deux barres brutes pour une même clé, aucune n'est « la » ligne
        # brute → None, la ligne tombera (avant : la dernière gagnait en silence) ; m-j du tour 4 : rangée par une seule
        # fonction, que S37 et S38 rejouent
        brut_paris = ranger_les_lignes_brutes(brut_paris_paires)
        n3_brut, brut_n3_paires = {}, []
        import gzip
        with gzip.open(os.path.join(racine, A.N3), "rt", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                ms = mnemos.get(row["isin_passage"], set())
                if row["statut"] == A.GARDEE and len(ms) == 1 and (next(iter(ms)), row["date"]) in voulues:
                    n3_brut[(next(iter(ms)), row["date"])] = float(row["close"].replace(",", "."))
                if row["statut"] == A.GARDEE and len(ms) == 1 and row["date"] in journees:
                    brut_n3_paires.append(((next(iter(ms)), row["date"]),
                                           [row[c].replace(",", ".") for c in ("open", "high", "low", "close", "volume")]))
        # deux barres brutes pour une même clé : aucune n'est « la » ligne brute → None, la ligne tombera
        brut_n3_rangees = ranger_les_lignes_brutes(brut_n3_paires)
        divisions_yahoo = {}
        with open(os.path.join(racine, A.LISTE_YAHOO), encoding="utf-8", newline="") as f:
            symboles = {row["isin"]: row["symbole"] for row in csv.DictReader(f)}
        import datetime
        from zoneinfo import ZoneInfo
        for m_ in {o[0] for o in option if o[8] == "oui"}:
            for isin, ms in mnemos.items():
                j = os.path.join(racine, os.path.dirname(A.LISTE_YAHOO), "bruts", symboles.get(isin, "?") + ".json")
                if ms == {m_} and os.path.exists(j):
                    with open(j, encoding="utf-8") as f:
                        ev = json.load(f)["chart"]["result"][0].get("events", {}).get("splits", {})
                    divisions_yahoo[m_] = sorted((datetime.datetime.fromtimestamp(x["date"], ZoneInfo("Europe/Paris"))
                                                  .date().isoformat(), float(x["numerator"]) / float(x["denominator"]))
                                                 for x in ev.values())
    except Exception as x:   # noqa: BLE001 — relecteur E2b tour 3, m4 : tout échec de chargement rend le code 2 (R-734)
        print(f"ARRÊT — l'épreuve n'a pas pu tourner : {type(x).__name__} : {x}")
        return 2
    e = {"lignes": lignes, "octets": octets, "sha_contrat": C.FICHIERS_DE_COURS_FIGES[chemin]["sha256"],
         "fin_contrat": C.FICHIERS_DE_COURS_FIGES[chemin]["fin"],
         "manifeste": manifeste, "maitre": maitre, "table": table, "norm": lc.COMMUN.norm_valeur, "lecture": lecture,
         "paris_accor": paris_accor, "yahoo_alstom": yahoo_alstom, "reassemble": reassemble, "ops": ops,
         "seuil": seuil, "variations": A.variations_hors_seuil, "divisions": divisions, "tolerance_p9": TOLERANCE_P9,
         "ancres_fausses": ancres_fausses, "tolerance_p10": TOLERANCE_P10,
         "prefixe_google": A.SOURCE_RAMENEE.split("{p")[0].format(origine=A.R.SOURCE_GOOGLE),
         "source_google": A.R.SOURCE_GOOGLE, "repare": repare, "fin_bnains": A.R.FIN_BNAINS, "option": option,
         "backlog": backlog, "n3_brut": n3_brut, "divisions_yahoo": divisions_yahoo, "journees": journees,
         "brut_paris": brut_paris, "brut_n3_rangees": brut_n3_rangees, "source_paris": A.SOURCE_PARIS,
         "brut_paris_paires": brut_paris_paires, "brut_n3_paires": brut_n3_paires,
         "prefixe_sortie": A.SOURCE_SORTIE.split("{")[0]}
    print(f"TÉMOIN {chemin}")
    r = verifier(e)
    for k, (ok, d) in r.items():
        print(f"{k} {'TIENT' if ok else 'TOMBE'} — {d}")
    sain = all(ok for ok, _ in r.values()) and len(r) == 17
    deja = sorted(k for k, (ok, _) in r.items() if not ok)
    if deja:
        print("TOMBÉES SUR LE TÉMOIN TEL QUEL : " + ", ".join(deja) + " — ce sont des constats à trancher, pas des "
              "exemptions : l'épreuve reste NON CONFORME tant qu'ils durent")
    if "--saboter" not in argv:
        print("RÉSULTAT : " + ("tout tient" if sain else "NON CONFORME"))
        return 0 if sain else 1

    def copie(**k):
        return dict(e, reassemble=None, **k)
    i24 = next(i for i, l in enumerate(lignes) if l[1] >= min(x[1] for x in maitre) and l[0] == "ACCOR")
    par_cle_maitre = {(l[0], l[1]): l for l in maitre}
    # S15 : choisie par une PROPRIÉTÉ — la première ligne « ramenée » d'avant 2017-03 dont la barre de Paris (lue par
    # `K.lire_paris`, celle que l'assemblage refuse) vaut moins des deux tiers de la clôture du témoin ; aucune → arrêt
    paris_s15, _, _ = A.K.lire_paris(racine)
    i15 = next((i for i, l in enumerate(lignes) if "ramené au brut" in l[7] and l[1] <= A.R.FIN_BNAINS
                and l[1] in paris_s15.get(l[0], {}) and paris_s15[l[0]][l[1]][3] < float(l[5]) * 2 / 3), None)
    if i15 is None:
        print("S15 ARRÊT — aucune barre de Paris refusée à remettre : le sabotage ne s'applique pas")
        return 2
    l15 = lignes[i15][:2] + list(A.texte(A.K.arrondir(paris_s15[lignes[i15][0]][lignes[i15][1]], 1.0, 1.0))) + ["bnains"]
    sorties = [i for i, l in enumerate(lignes) if lc.COMMUN.norm_valeur(l[0]) not in table]
    sabotages = {
        "S1 une ligne écrite deux fois": ("P1", copie(lignes=lignes + [lignes[0]])),
        "S2 une ligne de 2024 changée d'un centime": ("P2", copie(lignes=lignes[:i24] + [
            lignes[i24][:5] + [repr(float(lignes[i24][5]) + 0.01)] + lignes[i24][6:]] + lignes[i24 + 1:])),
        "S3 un octet du témoin changé": ("P3", copie(octets=octets[:-2] + bytes([octets[-2] ^ 1]) + octets[-1:])),
        "S4 la source d'une ligne de société sortie effacée": ("P4", copie(
            lignes=lignes[:sorties[0]] + [lignes[sorties[0]][:7] + [" "]] + lignes[sorties[0] + 1:])),
        "S5 une ligne de société sortie de moins (manque non écrit)": ("P5", copie(
            lignes=lignes[:sorties[0]] + lignes[sorties[0] + 1:])),
        "S6 ACCOR 2000-01-03 prise ramenée au lieu de Paris": ("P6", copie(lignes=[
            (l[:7] + ["yahoo ramené au brut ÷ 0.652401"] if l[:2] == ["ACCOR", "2000-01-03"] else l) for l in lignes])),
        # E2c — S13 : P9 privée de la liste des barres fausses ; l'ancre fausse redevient un écart (AIR LIQUIDE 2014)
        "S13 P9 sans la liste des barres prouvées fausses": ("P9", copie(ancres_fausses=set())),
        # E2c — S14 : B2 retiré dans le témoin, en mémoire : chaque ligne google ramenée reprend la ligne du maître
        "S14 lignes google remises telles que le maître (B2 retiré)": ("P10", copie(lignes=[
            (list(par_cle_maitre[(l[0], l[1])]) if l[7].startswith(e["prefixe_google"]) else l) for l in lignes])),
        # E2c — S15 : une barre de Paris d'un jour démenti par l'indice remise, en mémoire (la plus forte en écart : la
        # première barre « ramenée » d'un jour où la clôture du témoin vaut plus de 1,5 fois la barre de Paris)
        "S15 une barre de Paris d'un jour douteux remise": ("P11", copie(lignes=lignes[:i15] + [l15] + lignes[i15 + 1:])),
    }
    # E2c tour 2 — S19 : deux séances consécutives du témoin échangées pour TOUTES les valeurs (le défaut B-1), en
    # mémoire. Choisies par une PROPRIÉTÉ : de 2001 à la dernière séance de bnains, les deux séances voisines où la
    # médiane des |variations de clôture| est la plus grande (un échange de deux séances qui ont peu bougé ne se voit pas).
    par_date = {}
    for l in lignes:
        if "2001-01-01" <= l[1] <= A.R.FIN_BNAINS:
            par_date.setdefault(l[1], {})[l[0]] = float(l[5])
    jours = sorted(par_date)
    ecarts19 = [(statistics.median([abs(par_date[b][v] / par_date[a][v] - 1) for v in par_date[a] if v in par_date[b]]
                                   or [0]), a, b) for a, b in zip(jours, jours[1:])]
    _, j1, j2 = max(ecarts19)
    l19 = [(l[:1] + [{j1: j2, j2: j1}[l[1]]] + l[2:] if l[1] in (j1, j2) else l) for l in lignes]
    sabotages[f"S19 les séances {j1} et {j2} échangées pour toutes les valeurs"] = ("P12", copie(lignes=l19))
    # E2c tour 2 — S20 à S23 : l'option de A-748, sur la première ligne « oui » ; aucune → arrêt, code 2
    oui = [o for o in e["option"] if o[8] == "oui"]
    if not oui:
        print("S20 ARRÊT — aucune ligne « oui » dans l'option : les sabotages S20 à S23 ne s'appliquent pas")
        return 2
    o0 = oui[0]
    k0 = next(i for i, l in enumerate(lignes) if l[:2] == o0[:2])
    sabotages["S20 une ligne « oui » sans décision"] = ("P13", copie(option=[
        (o[:9] + [""] + o[10:] if o is o0 else o) for o in e["option"]]))
    sabotages["S21 la source d'une ligne retenue changée dans le témoin"] = ("P14", copie(
        lignes=lignes[:k0] + [lignes[k0][:7] + ["une autre source"]] + lignes[k0 + 1:]))
    fois = lambda x: x[:5] + [repr(float(x[5]) * 1.1)] + x[6:]
    sabotages["S22 une ligne retenue × 1,1 (témoin et option)"] = ("P15", copie(
        lignes=lignes[:k0] + [fois(lignes[k0])] + lignes[k0 + 1:],
        option=[(fois(o) if o is o0 else o) for o in e["option"]]))
    sabotages["S23 un trou comblé ôté du manifeste"] = ("P16", copie(manifeste=dict(manifeste, trous_combles_par_l_option=[
        x for x in manifeste.get("trous_combles_par_l_option", []) if (x[0], x[1]) != (o0[0], o0[1])])))
    # E2c tour 3 et 4 — S24, S25 et S28 (P17, en mémoire), construits par `sabotages_de_p17` : le balayage par
    # mutation (tests/outils/BALAYER_LES_MUTANTS_DES_JOURNEES.py) joue les mêmes, sans les recopier (R-708)
    p17, arret17 = sabotages_de_p17(e)
    if arret17:
        print(arret17)
        return 2
    sabotages.update(p17)
    # E2c tour 3 — S26 et S27 (P13, D-2 du relecteur, en mémoire) : la première ligne « oui » cite une décision INVENTÉE
    # (« A-n · n'importe quoi du <date> à <heure> », le texte du relecteur) ; puis la même citation avec l'heure d'une
    # AUTRE décision de la ligne A-n du BACKLOG (la première heure « à HHhMM » de cette ligne différente de la citée)
    a0 = re.match(r"(A-\d+) · ", o0[9])
    q0 = re.search(r"du (\d\d-\d\d-\d{4}) à (\d\dh\d\d)", o0[9])
    if not (a0 and q0):
        print("S26 ARRÊT — la décision de la première ligne « oui » n'a pas la forme attendue : S26 et S27 ne s'appliquent pas")
        return 2
    ligne_a = next((l for l in e["backlog"] if l.startswith(f"| {a0.group(1)} |")), "")
    autre_heure = next((h for h in re.findall(r"à (\d\dh\d\d)", ligne_a) if h != q0.group(2)), None)
    if autre_heure is None:
        print("S27 ARRÊT — la ligne de l'action n'a pas d'autre heure : S27 ne s'applique pas")
        return 2
    sabotages["S26 une décision inventée citée (action et heure vraies)"] = ("P13", copie(option=[
        (o[:9] + [f"{a0.group(1)} · n'importe quoi {q0.group(0)}"] + o[10:] if o is o0 else o) for o in e["option"]]))
    sabotages[f"S27 l'heure d'une autre décision de {a0.group(1)} ({autre_heure}) à la place de {q0.group(2)}"] = ("P13", copie(
        option=[(o[:9] + [o[9].replace(q0.group(0), f"du {q0.group(1)} à {autre_heure}")] + o[10:] if o is o0 else o)
                for o in e["option"]]))
    # E2c tour 4 — S29 (P13, m-e du relecteur E2c tour 3, en mémoire) : la décision de la ligne A-n portée par une AUTRE
    # valeur — sur une copie du BACKLOG, le mnémonique de la première ligne « oui » est remplacé, sur la ligne A-n et
    # elle seule, par la première valeur du témoin (ordre alphabétique) que cette ligne ne nomme pas. L'option et le
    # témoin ne changent pas : P13 doit tomber seule. Aucune valeur à substituer → arrêt, code 2
    mot29 = lambda v: re.compile(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])")
    autre29 = next((v for v in sorted({l[0] for l in lignes}) if not mot29(v).search(ligne_a)), None)
    if autre29 is None or not mot29(o0[0]).search(ligne_a):
        print("S29 ARRÊT — aucune valeur à substituer sur la ligne de l'action : S29 ne s'applique pas")
        return 2
    sabotages[f"S29 la décision de {a0.group(1)} portée par une autre valeur ({o0[0]} → {autre29} sur la ligne du BACKLOG)"] = (
        "P13", copie(backlog=[(mot29(o0[0]).sub(autre29, l) if l is ligne_a else l) for l in e["backlog"]]))
    # n-2 de Cowork (E2c tour 5) et superviseur R-759 E2c tour 6, (3) ② : CHAQUE verdict partiel passe par UN seul geste
    # qui imprime sa ligne ET entre dans la liste dont la ligne RÉSULTAT est la conjonction — une ligne « NE TIENT PAS »
    # avec « tout tient » est impossible par construction (avant : `morsures &= …` à part de chaque `print`, et la ligne
    # de J17 pouvait être retirée sans que rien ne rougisse)
    verdicts = []

    def verdict(bon, ligne):
        print(ligne)
        verdicts.append(bool(bon))
    for nom, (cible, s) in sabotages.items():
        rs = verifier(s)
        nouvelles = sorted(k for k, (ok, _) in rs.items() if not ok and k not in deja)
        attendu = [cible] if cible else []     # cible None (S30) : un contre-cas, rien ne doit tomber
        bon = nouvelles == attendu
        etat = ("mord" if cible else "tient comme attendu") if bon else "NE MORD PAS comme attendu"
        verdict(bon, f"{nom} {etat} : tombées en plus {nouvelles} (attendu {attendu})")
    # J17 (m-l du relecteur E2c tour 5, 13-11-2026) : la seconde sortie du juge de P17, le nombre de lignes jugées, entre
    # dans son verdict depuis m-k ; elle est confrontée, sur le témoin tel quel ET sur chaque sabotage de P17, au compte
    # que l'épreuve calcule elle-même (`lignes_que_p17_doit_juger`). Sur un sabotage où P17 tombe déjà, le verdict ne
    # montre pas un compte faux : seule cette confrontation le montre (S31, une ligne « ramenée au brut »)
    jeux17 = [(nom, journees_hors_de_leur_fichier(x["lignes"], x["journees"], x["brut_paris"], x["brut_n3_rangees"],
                                                  x["source_paris"], x["prefixe_sortie"])[1], lignes_que_p17_doit_juger(x))
              for nom, x in [("témoin tel quel", e)] + [(n, s) for n, (_, s) in p17.items()]]
    temoin17 = jeux17[0][1:]
    ecarts17 = ecarts_de_j17(jeux17)
    verdict(not ecarts17, f"J17 lignes jugées par P17 confrontées au compte de l'épreuve, sur le témoin et {len(p17)} sabotages de P17 "
          f"{'tient' if not ecarts17 else 'NE TIENT PAS'} : écarts {len(ecarts17)} {ecarts17[:3]} · témoin tel quel : "
          f"jugées {temoin17[0]}, compte {temoin17[1]}")
    # S8 (N-1 de Cowork, superviseur E2c tour 1 ②) : CHAQUE opération que P8 doit juger, inversée une à une, en mémoire ;
    # P8 doit tomber à chaque fois. La liste attendue est lue par l'épreuve dans le fichier des opérations écrit par
    # RECONSTRUIRE (R.PAR_OPERATION), pas par le chemin d'entrée de P8 : une opération jugée par le fichier et absente des
    # opérations du programme est une morsure manquée. Propriété : « P8 voit chaque opération qu'elle doit juger ».
    cle = lambda v: table.get(lc.COMMUN.norm_valeur(v), v)
    bornes = {}
    for l in lignes:
        k = cle(l[0])
        a, b = bornes.get(k, (l[1], l[1]))
        bornes[k] = (min(a, l[1]), max(b, l[1]))
    with open(os.path.join(racine, A.R.PAR_OPERATION), encoding="utf-8", newline="") as f:
        attendues = [(row["valeur"], row["date"], float(row["facteur"])) for row in csv.DictReader(f)
                     if row["facteur"] and abs(float(row["facteur"]) - 1) > seuil and cle(row["valeur"]) in bornes
                     and bornes[cle(row["valeur"])][0] < row["date"] <= bornes[cle(row["valeur"])][1]]
    if not attendues:
        print("S8 ARRÊT — aucune opération à juger dans le fichier des opérations : le sabotage ne s'applique pas")
        return 2
    manquees = []
    for v8, x8, f8 in attendues:
        # le fichier écrit le facteur à six décimales (« 0.333333 ») : l'opération est la même quand le facteur du
        # programme, arrondi à six décimales, vaut celui du fichier (mesuré au premier passage : 1/3 contre 0,333333)
        i8 = next((i for i, (x, f, *_) in enumerate(ops.get(v8, [])) if x == x8 and f and round(f, 6) == round(f8, 6)),
                  None)
        if i8 is None:
            manquees.append(f"{v8} {x8} (absente des opérations du programme)")
            continue
        ops8 = {v: list(l) for v, l in ops.items()}
        x, f, *q = ops8[v8][i8]
        ops8[v8][i8] = (x, 1 / f, *q)
        # m-c du relecteur E2c tour 2 : par `verifier`, comme S1 à S6 — P8 doit tomber, ET ELLE SEULE en plus de celles
        # qui tombent déjà (la garantie « elle seule » de l'ancien S8, retirée au tour 2 sans être déclarée)
        rs8 = verifier(dict(e, ops=ops8, reassemble=None))
        tombees8 = sorted(k for k, (ok, _) in rs8.items() if not ok and k not in deja)
        if tombees8 != ["P8"]:
            manquees.append(f"{v8} {x8} (tombées en plus {tombees8})")
    bon = not manquees
    verdict(bon, f"S8 chaque opération jugée inversée une à une ({len(attendues)}) {'mord' if bon else 'NE MORD PAS'} : "
          f"manquées {len(manquees)} {manquees[:5]}")
    # S12 (superviseur R-759 de E2b tour 3, ① b) : en mémoire, la veille ancrée dont l'opération a l'effet le plus petit
    # (|1 − 1/diviseur|), prise parmi celles qui ne sont pas déjà en écart, multipliée par son diviseur — l'attribution
    # comptée deux fois. P9 doit compter un écart de plus. Si la tolérance de P9 dépasse cet effet, S12 ne mord pas.
    ecarts_p9 = int(re.search(r"écarts : (\d+)", r["P9"][1]).group(1))
    ramenees = {(table.get(lc.COMMUN.norm_valeur(l[0]), l[0]), l[1]): i for i, l in enumerate(lignes)
                if "ramené au brut" in l[7]}
    candidats = []
    for d in divisions:
        i = ramenees.get((table.get(lc.COMMUN.norm_valeur(d["valeur"]), d["valeur"]), d["date_dernier_cours"]))
        if (i is not None and (d["valeur"], d["date_dernier_cours"]) not in ancres_fausses
                and abs(float(lignes[i][5]) / float(d["dernier_cours"]) - 1) <= TOLERANCE_P9):
            candidats.append((abs(1 - 1 / float(d["diviseur"])), i, float(d["diviseur"]), d["valeur"], d["date_dernier_cours"]))
    if not candidats:
        print("S12 ARRÊT — aucune veille ancrée sans écart : le sabotage ne s'applique pas")
        return 2
    effet, i12, div, v12, d12 = min(candidats)
    l12 = lignes[i12][:5] + [repr(float(lignes[i12][5]) * div)] + lignes[i12][6:]
    rs = verifier(copie(lignes=lignes[:i12] + [l12] + lignes[i12 + 1:]))
    n12 = int(re.search(r"écarts : (\d+)", rs["P9"][1]).group(1))
    bon = n12 > ecarts_p9
    verdict(bon, f"S12 attribution comptée deux fois ({v12} {d12}, diviseur {div}, effet {effet:.1%}, tolérance de P9 "
          f"{TOLERANCE_P9:.0%}) {'mord' if bon else 'NE MORD PAS'} : écarts de P9 {n12} (témoin tel quel : {ecarts_p9})")
    # S7 : le programme privé de la barre de Paris (toute ligne d'avant mars 2017 ramenée) — P7 doit tomber
    garde = A.K.lire_paris
    A.K.lire_paris = lambda rac: ({}, [], [])
    try:
        sab, _ = A.assembler(racine, C.FICHIERS_DE_COURS_FIGES[chemin]["fin"])
    finally:
        A.K.lire_paris = garde
    rs = verifier(dict(e, reassemble=sab))
    bon = not rs["P7"][0]
    verdict(bon, f"S7 programme sans barre de Paris {'mord' if bon else 'NE MORD PAS'} : P7 {rs['P7'][1]}")
    # S10 et S11 (superviseur R-759 de E2b tour 2, marche ④ 3) : le CHEMIN COMPLET, sur une copie du dépôt — le
    # programme saboté, l'ancien gel retiré, un gel neuf, puis cette épreuve sur la copie
    for nom, avant, apres, cible in CHEMINS_COMPLETS:
        try:
            sortie = chemin_complet(racine, chemin, avant, apres, C.FICHIERS_DE_COURS_FIGES[chemin]["fin"])
        except Exception as x:   # noqa: BLE001 — R-734 : un sabotage qui ne s'applique pas arrête, code 2
            print(f"{nom} ARRÊT — le chemin complet n'a pas pu se faire : {type(x).__name__} : {x}")
            return 2
        refus = next((l for l in sortie.splitlines() if l.startswith("REFUS") and "non vue" in l), "")
        tombe = next((l for l in sortie.splitlines() if l.startswith(cible + " ")), "")
        # relecteur E2b tour 3, m2 : --ecrire refuse de figer un témoin où une opération n'est pas vue ; pour P8, ce
        # refus EST la morsure ; à défaut, et pour toute autre cible, l'épreuve lancée sur le gel neuf doit faire
        # tomber la propriété visée
        bon = bool(cible == "P8" and refus) or tombe.startswith(cible + " TOMBE")
        verdict(bon, f"{nom} {'mord' if bon else 'NE MORD PAS'} : {((refus if cible == 'P8' else '') or tombe)[:170]}")
    morsures = bool(verdicts) and all(verdicts)
    print("RÉSULTAT : " + ("tout tient, chaque sabotage mord" if sain and morsures else
                           "NON CONFORME — " + ("chaque sabotage mord, mais " if morsures else "") +
                           ("le témoin tel quel fait tomber " + ", ".join(deja) if deja else
                            "un sabotage ne mord pas, ou J17 ne tient pas")))
    return 0 if sain and morsures else 1


# Les sabotages du chemin complet : (nom, texte du programme, remplacement, la propriété qui doit tomber — pour P8, le
# refus de --ecrire suffit). Le texte doit se trouver une fois exactement dans programmes/ASSEMBLER_LES_VINGT_ANS.py de
# la copie, sinon arrêt (code 2).
CHEMINS_COMPLETS = (
    ("S10 de bout en bout, facteur inversé", "K.arrondir(fichier[v][d], 1.0 / p, p)",
     "K.arrondir(fichier[v][d], p, 1.0 / p)", "P8"),
    ("S11 de bout en bout, dates des opérations décalées d'une séance plus tard", "    fichier, ops = operations(racine)\n",
     "    fichier, ops = operations(racine)\n    ops = {v: [((lambda ap: ap[0] if ap else x)("
     "[y for y in sorted(fichier.get(v, {})) if y > x]), f, *q) for x, f, *q in l] for v, l in ops.items()}\n",
     "P8"),
    # E2c — S16 : B2 retiré du programme (les lignes google copiées telles quelles) → la chute d'AIR LIQUIDE revient
    ("S16 de bout en bout, lignes google du maître copiées telles quelles (B2 retiré)",
     "        if l[7] == R.SOURCE_GOOGLE:", "        if False:", "P10"),
    # E2c — S17 : la règle des jours douteux retirée (toute barre de Paris prise, comme avant E2c) → les aller-retours
    ("S17 de bout en bout, barre de Paris prise même un jour douteux démenti",
     "    if d not in douteux or verdicts.get(d) == VERDICT_FICHIER_A_TORT or K.barre_sure(",
     "    if True or d not in douteux or verdicts.get(d) == VERDICT_FICHIER_A_TORT or K.barre_sure(", "P11"),
    # E2c — S18 : le trou déclaré de A-748 retiré (la barre N3 discontinue versée) → les aller-retours d'ALO et LI
    ("S18 de bout en bout, barre N3 discontinue versée au lieu du trou déclaré",
     "            if motif and discontinue(", "            if False and discontinue(", "P11"),
)


def chemin_complet(racine, temoin, avant, apres, coupure):
    """Fait le chemin réel d'un programme fautif jusqu'au gel, sur une copie ; rend la sortie de l'épreuve.

    ① RÔLE — Éprouver le cas que le relecteur du tour 2 a trouvé sans filet : un programme fautif PUIS un gel neuf
      (B1-bis : la mutation du facteur inversé, refigée, rendait l'ancienne épreuve verte).
    ② CONTEXTE D'APPEL — `principal`, avec --saboter, pour S10 et S11.
    ③ ENTRÉE — `racine` : le dépôt éprouvé (cloné tel qu'il est COMMITÉ) · `temoin` : le chemin du témoin déclaré ·
      `avant`, `apres` : le texte du programme à remplacer et son remplaçant · `coupure` : la fin déclarée au contrat du
      témoin éprouvé (E2c tour 3, 13-11-2026 : le gel neuf se fait à la MÊME coupure que le témoin qu'il remplace ; sans
      elle, la coupure suivait le maître, qui a gagné le 2026-11-12 à la fusion de main).
    ④ CONDITIONS D'ENTRÉE — `racine` est un dépôt git ; `avant` se trouve une fois exactement dans le programme.
    ⑤ SORTIE — UNE valeur : la sortie de `--ecrire` quand il REFUSE le gel (code 1, ligne « REFUS ») ; sinon la sortie
      écran de cette épreuve lancée sur la copie (sans --saboter).
      [rend: 1]
    ⑥ TRAITEMENT — ① `git clone --local` dans un dossier jetable · ② le programme saboté · ③ le témoin, son
      manifeste, ses addenda et son entrée au contrat retirés · ④ `ASSEMBLER --ecrire --coupure=<coupure>` (un refus est rendu tel quel,
      tout autre code non nul lève) · ⑤ cette
      épreuve sur la copie · ⑥ la copie effacée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 de E2b, tour 2, marche ④ 3.
    ⑨ CE QUI CLOCHE — La copie part du dernier commit : un changement non commité du dépôt n'y est pas. · Environ
      une minute et quelques centaines de mégaoctets par sabotage (une copie à la fois, effacée).
    ⑩ EFFET — Un dossier jetable sous le dossier temporaire, effacé ; deux processus lancés.
    ⑪ TERMINAISON — Rend la main ou lève ; chaque processus est borné à 900 secondes (subprocess, timeout).
      [sort: non]
    """
    import shutil
    import subprocess
    import tempfile
    d = tempfile.mkdtemp(prefix="E2b_chemin_complet_")
    c = os.path.join(d, "copie")
    try:
        subprocess.run(["git", "clone", "-q", "--local", racine, c], check=True, timeout=900)
        prog = os.path.join(c, "programmes", "ASSEMBLER_LES_VINGT_ANS.py")
        with open(prog, encoding="utf-8") as f:
            t = f.read()
        if t.count(avant) != 1:
            raise ValueError(f"le texte à saboter se trouve {t.count(avant)} fois")
        with open(prog, "w", encoding="utf-8") as f:
            f.write(t.replace(avant, apres))
        for x in glob.glob(os.path.join(c, glob.escape(temoin[:-4])) + "*"):
            os.remove(x)
        contrat = os.path.join(c, "programmes", "CONTRATS_DES_FICHIERS.py")
        with open(contrat, encoding="utf-8") as f:
            lignes = f.read().split("\n")
        k = lignes.index(f'    "{temoin}": {{')
        with open(contrat, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes[:k] + lignes[k + 3:]))
        g = subprocess.run([sys.executable, "-I", prog, c, "--ecrire", f"--coupure={coupure}"], capture_output=True,
                           text=True, timeout=900)
        if g.returncode == 1 and "REFUS" in g.stdout:
            return g.stdout          # le gel refusé : `principal` lit la raison du refus
        if g.returncode != 0:
            raise ValueError(f"--ecrire sur la copie : code {g.returncode} : {g.stdout[-300:]}")
        o = subprocess.run([sys.executable, "-I", os.path.join(c, "tests", os.path.basename(__file__)), c],
                           capture_output=True, text=True, timeout=900)
        return o.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)

if __name__ == "__main__":
    # UNE SEULE ENVELOPPE (superviseur R-759 de E2b avant le tour 5, ① (4) a) : toute exception non rattrapée, où
    # qu'elle naisse (chargement, `verifier`, un sabotage), rend le code 2 — « l'épreuve n'a pas pu tourner » —, jamais
    # le code 1 de Python, qui se lirait « NON CONFORME » (R-734). `SystemExit` n'est pas une `Exception` : il passe.
    try:
        sys.exit(principal(sys.argv[1:]))
    except Exception as x:   # noqa: BLE001
        print(f"ARRÊT — l'épreuve n'a pas pu tourner : {type(x).__name__} : {x}")
        sys.exit(2)
