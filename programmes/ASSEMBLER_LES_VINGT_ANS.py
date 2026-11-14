#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASSEMBLER_LES_VINGT_ANS.py — Jeu 12-11-2026 (Paris), mission E2b du plan V7. Simulation uniquement.

① RÔLE — Assembler les cours de 2000 à la date de coupure dans UN fichier À PART du fichier maître, la source écrite
  sur chaque ligne, puis le FIGER : l'écrire sous temoins/ sous un nom qui dit ce qu'il est et quand il a été pris,
  déclarer son empreinte et sa dernière séance au contrat des fichiers de cours figés
  (programmes/CONTRATS_DES_FICHIERS.py, FICHIERS_DE_COURS_FIGES), et écrire à côté un manifeste (comptes par part,
  lignes non versées et pourquoi, trous mesurés par le lecteur unique). Le juge le lit sur demande seulement :
  python3 programmes/JUGE_DES_STRATEGIES.py <racine> <fiche> --cours=<chemin du témoin>.
② CONTEXTE D'APPEL — À la main, par le Chat ou un agent : python3 programmes/ASSEMBLER_LES_VINGT_ANS.py <racine>
  [--coupure=AAAA-MM-JJ] [--ecrire]. Sans option : essai à blanc, rien n'est écrit, les comptes sont affichés.
  --ecrire refuse de figer s'il reste une opération non vue (relecteur E2b tour 3, m2). L'option --signaler (addenda
  datés) a été RETIRÉE au tour 4 (superviseur R-759 de E2b, tour 3, ②) : elle faisait comparer le programme à
  lui-même ; l'addenda du 2026-11-12 à 13h20 déjà commité reste en place, son archivage attend Jean-Luc.
  Son épreuve : tests/EPREUVES_DU_FICHIER_DES_VINGT_ANS_Jeu_12-11-2026.py (qui appelle `assembler` et relit le témoin).
③ ENTRÉE — Sous la racine : l'historique long réparé (donnees/sources_yahoo/historique_long_repare.csv) et ce qu'il
  faut à RECONSTRUIRE_L_HISTORIQUE_LONG pour en calculer les facteurs ; l'extrait de Paris (bnains) ; le fichier maître
  donnees/cours_maitre.csv ; les barres de Paris des sociétés sorties (N3) ; les séances reconstruites depuis Yahoo
  (A_VERSER.csv) et la liste qui relie leurs noms à leurs ISIN (LISTE.csv) ; la table des identités
  donnees/sources_indice/IDENTITES_DES_SOCIETES.csv ; pour la règle des jours douteux (E2c), ce que le contrôle de
  l'historique long lit pour elle : l'indice CAC 40, Francfort, evenements.json, AJUSTEMENTS_DE_YAHOO.csv. Facultatifs :
  la date de coupure (par défaut la dernière date du fichier maître) ; l'option de A-748, SOURCE_RECOUPEE (fichier
  de données ; 13 lignes d'Alstom « oui » depuis la décision de A-748 du 12-11-2026 à 23h47).
④ CONDITIONS D'ENTRÉE — La coupure est une date AAAA-MM-JJ postérieure ou égale à la première date du maître. Le
  maître a l'en-tête du contrat COURS_MAITRE. Chaque fichier lu existe (sinon code 2).
⑤ SORTIE — UNE valeur : le code de sortie — 0 assemblage fait (et écrit avec --ecrire), 1 assemblage refusé par l'un
  de ses propres contrôles (une clé écrite deux fois, une ligne sans source, un nom de société sortie qui serait lu
  comme une valeur d'aujourd'hui), 2 programme qui n'a pas pu tourner (R-734). Avec --ecrire : le témoin, son manifeste
  et l'entrée du contrat.
  [rend: 1]
⑥ TRAITEMENT — `jours_douteux_de_paris` et `barre_de_paris_retenue` (la règle des jours douteux du contrôle) ·
  `assembler` (quatre parts, chacune avec sa règle, une clé (valeur, date) écrite une seule fois) ·
  `ecrire_le_temoin` · `declarer_au_contrat` · `mesurer_les_trous` (lecteur unique) · `ecrire_le_manifeste`.
⑦ UNITÉ — Des euros par titre et des titres échangés, comme écrits par chaque source ; des séances.
⑧ POURQUOI — Décisions de Jean-Luc : 11-11-2026 à 18h04, « 1 » — les 20 ans dans un FICHIER À PART, jamais dans le
  fichier maître (le juge lit le maître par défaut et jugerait sinon 2000-2023 à chaque appel, contre le regard
  unique de R-505) ; 11-11-2026 à 20h52, « 1 » — R-108 telle quelle : le fichier garde le VRAI cours de Paris, les
  divisions sont corrigées à part pour les calculs seulement, jamais les dividendes, et les parts de Yahoo en cours
  ajustés sont ramenées au cours brut ; 31-10-2026 à 16h05 et 20h48 — les sociétés sorties de l'indice entrent dans le
  fichier, achetées seulement aux dates où elles étaient dans le CAC 40 (le choix des dates est celui du juge, A-577,
  pas de ce fichier) ; 11-11-2026 à 22h26, « 1 » — une société sortie y est désignée par son mnémonique de la table des
  identités (règles I-2 à I-4) ; 12-11-2026 à 09h13, « 1 » — 2024-2026 est une COPIE FIGÉE ET DATÉE AVEC SON EMPREINTE,
  comme le témoin du golden, pour qu'un jugement refait plus tard donne le même résultat. Règle A8 de Jean-Luc : une
  séance sans cours de Paris n'est jamais inventée ; elle est exclue des rejeux et son manque est écrit.
⑨ CE QUI CLOCHE — Le lecteur unique (programmes/LIRE_LES_COURS.py) ne connaît que les valeurs du référentiel : les
  lignes des sociétés sorties y sont « inconnues », et le juge refuse un fichier dont des lignes sont mises à part ;
  lui apprendre les sociétés sorties est un changement du lecteur du circuit du soir, hors de cette mission. · Les
  sociétés sorties dont le mnémonique est « non trouvé » (question QA) ne sont PAS versées : leurs barres sont comptées
  au manifeste. · Les barres N3 d'un code qui appartient à une société d'aujourd'hui (Arcelor, ArcelorMittal :
  numéro 40) ne sont pas versées : elles réuniraient deux lignes de cotation sous une clé (règle I-7) ou doubleraient
  l'historique long ; comptées au manifeste. · Les lignes « google » du maître (02-01-2024 → 08-09-2026) sont corrigées
  des divisions par Google (RECONSTRUIRE ①) : depuis E2c, celles qu'une opération postérieure touche sont ramenées au
  brut dans CE fichier (décision du 11-11-2026 à 20h52, R-108 ①) — le maître ne change pas ; la justesse de ce ramené
  repose sur la mesure « Google = historique long » du 12-11-2026 (voir `assembler` ⑨). · Les trous déclarés de A-748
  (barre discontinue, aucune autre source) sont écrits au manifeste, pas au fichier : le lecteur unique
  ne connaît pas encore les sociétés sorties (QE). ·
  De mars 2017 à décembre 2023, aucun cours brut de Paris n'est au dépôt : ces lignes sont l'historique long divisé par
  ses facteurs, sans confrontation possible. · Les opérations sur titre viennent des fonctions de RECONSTRUIRE
  (`lire_les_entrees`, `operations_completes`) que son `main` appelle aussi ; INVENTORIER_LES_VINGT_ANS garde sa copie
  (→ BACKLOG). · La justesse du ramené au brut n'est gardée que par la continuité des cours (`variations_hors_seuil`) :
  une opération dont le facteur reste dans le seuil de variation ne s'y voit pas. · Le contrat est
  modifié par remplacement de texte dans un fichier .py.
⑩ EFFET — Sans option : lit, n'écrit rien. Avec --ecrire : écrit le témoin et son manifeste sous temoins/ et une
  entrée de FICHIERS_DE_COURS_FIGES dans programmes/CONTRATS_DES_FICHIERS.py. Lit l'horloge (Europe/Paris) pour le nom.
⑪ TERMINAISON — Rend la main : chaque étape parcourt un nombre fini de lignes, aucun appel réseau. Aucun de mes
  appels ne peut ne pas revenir.
"""
import csv
import datetime
import gzip
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import CONTROLER_L_HISTORIQUE_LONG as K          # noqa: E402  lecture des cours, Paris, facteurs appliqués (R-708)
import RECONSTRUIRE_L_HISTORIQUE_LONG as R       # noqa: E402  opérations sur titre et facteur d'une date (R-708)
from CONTRATS_DES_FICHIERS import COURS_MAITRE, COURS_BNAINS, COURS_DE_REMPLACEMENT_DES_TROUS   # noqa: E402

N3 = os.path.join("etudes", "brouillons_chat", "NUIT_DES_20_ANS_Mer_21-10-2026", "N3_societes_sorties",
                  "BARRES_SOCIETES_SORTIES_PROPOSITION.csv.gz")
YAHOO_SORTIES = os.path.join("etudes", "VINGT_ANS_PAR_YAHOO_Dim_08-11-2026", "sorties", "A_VERSER.csv")
LISTE_YAHOO = os.path.join("etudes", "VINGT_ANS_PAR_YAHOO_Dim_08-11-2026", "yahoo", "LISTE.csv")
IDENTITES = os.path.join("donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv")
CONTRAT = os.path.join("programmes", "CONTRATS_DES_FICHIERS.py")
TEMOINS = "temoins"
GARDEE = "GARDEE"                    # statut des barres N3 retenues par leur extraction (RAPPORT_N3.md)
NON_TROUVE = "non trouvé"            # écrit tel quel dans la colonne mnemonique de la table des identités
SAMEDI = 5
JOURS = ("Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim")
# les sources écrites dans la huitième colonne, pour les parts que ce programme calcule (les autres parts gardent la
# source de leur fichier, telle quelle)
SOURCE_PARIS = "bnains"                                  # barre de Paris telle que cotée (extrait bnains)
SOURCE_RAMENEE = "{origine} ramené au brut ÷ {p:.6f}"   # ligne de l'historique long divisée par ses facteurs (R-108)
SOURCE_SORTIE = "bnains archives (société sortie {numero})"   # barre N3
# E2c (12-11-2026) — LES JOURS DOUTEUX DE BNAINS. Les verdicts que rend K.arbitre_de_l_indice (CONTROLER_L_HISTORIQUE_LONG,
# l. 1204-1234), écrits là en clair comme dans REPARER (l. 1532) : un verdict qui ne serait pas l'un d'eux arrête
# l'assemblage (`jours_douteux_de_paris`), pour qu'un renommage chez K ne rende pas la règle muette.
VERDICT_FICHIER_A_TORT = "le fichier a tort"
VERDICT_BNAINS_A_TORT = "bnains a tort"
VERDICTS_CONNUS = (VERDICT_FICHIER_A_TORT, VERDICT_BNAINS_A_TORT, "indifférent", "non mesurable")
# Le motif d'une barre de Paris refusée un jour où l'indice donne tort à bnains (part ②, compté).
MOTIF_DEMENTI = "barre de Paris d'un jour où l'indice donne tort à bnains, non confirmée par Francfort"
# Décision de Jean-Luc du 12-11-2026 à 22h45 (A-748, « 1 ») : « chercher une autre source, et sinon un trou déclaré ».
# Une barre N3 d'une société sortie, un jour douteux, non confirmée, et DISCONTINUE (elle s'écarte de plus du seuil de
# variation de la barre d'avant ET de la barre d'après, qui s'accordent entre elles) est un TROU DÉCLARÉ avec ce motif —
# écrit par PROPRIÉTÉ, jamais par nom : l'indice ne peut rien recouper pour une société qui n'y était pas (Klépierre
# n'entre au CAC 40 que le 21-12-2015 ; rapport SOURCE_DES_28_COURS_ALO_LI du 12-11-2026 à 22h56).
MOTIF_DISCONTINUE = "barre discontinue avec la veille et le lendemain (au-delà du seuil de variation), aucune autre source"
# L'OPTION de remplacement (même rapport) : des barres d'une autre source, déposées dans ce fichier de DONNÉES avec la
# colonne `retenue` ; seules les lignes « oui » priment sur un trou déclaré. Les 13 barres d'Alstom tirées de Yahoo
# ALO.PA (méthode de A_VERSER) y sont « oui » depuis la décision de Jean-Luc du 12-11-2026 à 23h47 (A-748), citée dans la
# colonne `decision` ; Klépierre n'a aucune ligne (aucune source trouvée) : ses 13 jours restent des trous déclarés.
SOURCE_RECOUPEE = os.path.join("donnees", "sources_societes_sorties", "COURS_DE_REMPLACEMENT_DES_TROUS.csv")
RETENUE = ("oui", "non")


def lire_csv(chemin):
    """Lit un CSV (compressé ou non) en liste de dictionnaires.

    ① RÔLE — Une lecture simple, pour les fichiers que les modules réutilisés ne lisent pas.
    ② CONTEXTE D'APPEL — `assembler`, `identites`.
    ③ ENTRÉE — `chemin` : relatif au dossier courant (la racine).
    ④ CONDITIONS D'ENTRÉE — Le fichier existe, en UTF-8, avec un en-tête.
    ⑤ SORTIE — UNE valeur : la liste des lignes, chacune un dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — csv.DictReader ; gzip quand le nom finit par .gz.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Ne confronte aucun contrat : les fichiers de l'étude N3 et de l'étude Yahoo n'en ont pas.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève OSError.
      [sort: non]
    """
    ouvrir = gzip.open if chemin.endswith(".gz") else open
    with ouvrir(chemin, "rt", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def texte(b):
    """Écrit une barre de cinq nombres en cinq textes.

    ① RÔLE — Une seule façon d'écrire les barres que ce programme calcule.
    ② CONTEXTE D'APPEL — `assembler`.
    ③ ENTRÉE — `b` : (open, high, low, close, volume), des nombres, déjà arrondis par `K.arrondir`.
    ④ CONDITIONS D'ENTRÉE — Le volume est entier (`K.arrondir` l'arrondit à l'unité).
    ⑤ SORTIE — UNE valeur : le tuple des cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Les prix par repr (l'écriture la plus courte qui relit le même nombre), le volume en entier.
    ⑦ UNITÉ — Euros par titre ; titres.
    ⑧ POURQUOI — Un texte qui relit exactement le nombre calculé : l'épreuve compare à l'égalité.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return tuple(repr(float(x)) for x in b[:4]) + (str(int(b[4])),)


def operations(racine):
    """Rend l'historique long lu et les opérations sur titre de chaque valeur, facteurs déduits compris.

    ① RÔLE — Les facteurs qui ramènent une ligne de l'historique long (convention de Yahoo, corrigée des opérations sur
      le capital) au cours brut de Paris.
    ② CONTEXTE D'APPEL — `assembler`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt (le dossier courant doit l'être : les chemins de K et R sont relatifs).
    ④ CONDITIONS D'ENTRÉE — Celles du `main` de RECONSTRUIRE_L_HISTORIQUE_LONG (son ④).
    ⑤ SORTIE — DEUX valeurs : l'historique long {valeur : {date : barre}} lu par `K.lire_cours`, et les opérations
      {valeur : liste} rendues par `R.operations` puis `R.deduire`.
      [rend: 2]
    ⑥ TRAITEMENT — `R.lire_les_entrees` puis `R.operations_completes`, les deux fonctions que le `main` de RECONSTRUIRE
      appelle lui-même ; refus si l'historique long ou bnains a une ligne illisible.
    ⑦ UNITÉ — Des rapports sans unité pour les facteurs.
    ⑧ POURQUOI — R-708 : les facteurs se calculent à un seul endroit. Jusqu'au 12-11-2026 (tour 1), ce programme
      recopiait l'enchaînement du `main` de RECONSTRUIRE ; le superviseur R-759 de E2b (tour 1) a demandé une fonction
      partagée : elle existe depuis le tour 2, et les deux tables écrites par RECONSTRUIRE sont restées identiques à
      l'octet (mesuré sur deux clones, avant et après).
    ⑨ CE QUI CLOCHE — etudes/VINGT_ANS_A_PART_Mer_11-11-2026/INVENTORIER_LES_VINGT_ANS.py garde sa propre copie de
      l'enchaînement, sans les divisions officielles (→ BACKLOG). Aucune épreuve ne confronte les facteurs à
      RECONSTRUCTION_PAR_OPERATION.csv : la justesse du ramené au brut est gardée par la propriété de continuité
      (`variations_hors_seuil`, épreuve P8).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ou lève OSError / ValueError.
      [sort: non]
    """
    e = R.lire_les_entrees()
    if e["defauts_fichier"] or e["defauts_bnains"]:
        raise ValueError(f"historique long ou bnains illisible : {(e['defauts_fichier'] + e['defauts_bnains'])[:3]}")
    return e["fichier"], R.operations_completes(e)["ops"]


def identites(lignes):
    """Range la table des identités par code ISIN.

    ① RÔLE — Trouver, pour une barre d'une société sortie connue par son ISIN, son numéro interne et son mnémonique.
    ② CONTEXTE D'APPEL — `assembler`.
    ③ ENTRÉE — `lignes` : les lignes de IDENTITES_DES_SOCIETES.csv.
    ④ CONDITIONS D'ENTRÉE — Colonnes numero, debut, fin, mnemonique, isin.
    ⑤ SORTIE — DEUX valeurs : {isin : liste des lignes de ce code} ; l'ensemble des numéros qui ont une ligne sans fin
      (une société d'aujourd'hui, règle I-2 : la ligne ouverte est l'identité en cours).
      [rend: 2]
    ⑥ TRAITEMENT — Un passage sur la table.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Règles I-2 à I-4 (décision de Jean-Luc du 11-11-2026 à 22h26).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    par_isin, ouverts = defaultdict(list), set()
    for r in lignes:
        if r["isin"]:
            par_isin[r["isin"]].append(r)
        if not r["fin"]:
            ouverts.add(r["numero"])
    return par_isin, ouverts


def cle_d_une_societe_sortie(par_isin, ouverts, isin, d):
    """Rend le mnémonique sous lequel une barre d'une société sortie est écrite, ou la raison de ne pas l'écrire.

    ① RÔLE — Appliquer la décision du 11-11-2026 à 22h26 : une société sortie est désignée par son mnémonique.
    ② CONTEXTE D'APPEL — `assembler`, pour chaque barre N3 et chaque ligne de A_VERSER.
    ③ ENTRÉE — `par_isin`, `ouverts` (rendus par `identites`) · `isin` : le code de la barre · `d` : sa date.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : (le mnémonique, le numéro) quand la barre s'écrit ; (None, la raison) sinon.
      [rend: 2]
    ⑥ TRAITEMENT — ① code absent de la table → « code sans identité » · ② numéro d'une société d'aujourd'hui → « code
      d'une société d'aujourd'hui » · ③ le mnémonique de la ligne dont la période contient la date ; à défaut, celui
      que portent toutes les lignes du code s'il est unique ; sinon « mnémonique ambigu à cette date » ·
      ④ « non trouvé » → « mnémonique non trouvé (QA) ».
    ⑦ UNITÉ — Des dates AAAA-MM-JJ, comparées comme textes.
    ⑧ POURQUOI — La période d'une ligne d'identité d'une société sortie est celle de son passage dans l'indice ; ses
      barres d'avant et d'après (utiles aux indicateurs) gardent le mnémonique quand le code n'en a qu'un.
    ⑨ CE QUI CLOCHE — Un mnémonique qui aurait changé hors des périodes écrites ne se voit pas ici (la table n'en dit
      rien).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = par_isin.get(isin)
    if not lignes:
        return None, "code sans identité"
    numero = lignes[0]["numero"]
    if numero in ouverts:
        return None, "code d'une société d'aujourd'hui (numéro %s)" % numero
    couvrent = [r for r in lignes if (not r["debut"] or r["debut"] <= d) and (not r["fin"] or d <= r["fin"])]
    mnemos = {r["mnemonique"] for r in (couvrent or lignes)}
    if len(mnemos) != 1:
        return None, "mnémonique ambigu à cette date"
    m = mnemos.pop()
    if m == NON_TROUVE:
        return None, "mnémonique non trouvé (QA)"
    return m, numero


def jours_douteux_de_paris(racine, fichier, paris):
    """Rend les jours douteux de bnains, le verdict de l'indice sur chacun, et Francfort — par les fonctions du contrôle.

    ① RÔLE — Donner à l'assemblage LA règle des jours douteux, celle du contrôle et de la réparation de l'historique long,
      sans la recopier (R-708 : deux implémentations d'une même règle divergent toujours).
    ② CONTEXTE D'APPEL — `assembler`, une fois.
    ③ ENTRÉE — `racine` · `fichier` : l'historique long réparé, lu par `K.lire_cours` · `paris` : les barres de Paris
      de `K.lire_paris` (barres fausses ôtées, rectifications faites).
    ④ CONDITIONS D'ENTRÉE — Les fichiers que lit le `main` de CONTROLER_L_HISTORIQUE_LONG pour son contrôle K19
      (evenements.json, AJUSTEMENTS_DE_YAHOO.csv, INDICE_CAC40.csv, COURS_DE_FRANCFORT.csv) existent.
    ⑤ SORTIE — TROIS valeurs : l'ensemble des jours douteux (`K.jours_douteux` de `K.ecarts` du fichier réparé à
      Paris) ; {date : verdict de `K.arbitre_de_l_indice`} ; Francfort ({valeur : {date : clôture}}).
      [rend: 3]
    ⑥ TRAITEMENT — Les lectures et les appels du `main` et de `controler` de CONTROLER_L_HISTORIQUE_LONG (l. 1667-1669,
      3088-3094), dans le même ordre, sur le fichier réparé ; tout verdict hors de VERDICTS_CONNUS lève ValueError.
    ⑦ UNITÉ — Des dates AAAA-MM-JJ.
    ⑧ POURQUOI — A-539 (04-10 et 07-10-2026) et DECISIONS_DEJA_PRISES du 12-11-2026, § 3 : bnains porte, certains jours de
      2006-2007, des cours déjà divisés d'avance ; la réparation ne prend une barre bnains un jour douteux que si Francfort
      la confirme ou si l'indice donne tort à l'autre source (REPARER l. 1531-1559, `K.barre_sure`) ; l'assemblage, lui,
      prenait la barre de Paris dès qu'elle existait (95 barres aller-retour −50 % / +100 % dans le témoin du 12-11 à
      11h27). Mesuré le 12-11-2026 sur l'historique réparé : 16 jours douteux, dont les 13 de 2006-2007 jugés « bnains a
      tort » par l'indice.
    ⑨ CE QUI CLOCHE — La réparation mesurait les jours douteux sur le fichier de Yahoo AVANT réparation, fenêtres
      reconstruites exclues ; le contrôle, et ici, sur le fichier réparé : les jours où l'indice donnait tort à Yahoo y
      sont déjà réparés et n'y sont plus douteux. C'est le fichier que l'assemblage lit, et c'est la mesure du contrôle.
      · Le verdict est par SÉANCE (une suite de séances porte un verdict commun).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ou lève OSError / ValueError. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    douteux = K.jours_douteux(K.ecarts(fichier, paris))
    with open(os.path.join(racine, K.EVENEMENTS), encoding="utf-8") as f:
        evenements = K.sans_les_divisions_fausses(json.load(f), K.lire_a_defaire(os.path.join(racine, K.VERDICTS_YAHOO)))
    indice = K.lire_indice(os.path.join(racine, K.INDICE))
    verdicts = {}
    for jours, *_, verdict in K.arbitre_de_l_indice(fichier, paris, evenements, indice):
        if verdict not in VERDICTS_CONNUS:
            raise ValueError(f"verdict de l'indice inconnu : {verdict!r} (attendus : {VERDICTS_CONNUS})")
        for d in jours:
            verdicts[d] = verdict
    return douteux, verdicts, K.lire_francfort(os.path.join(racine, K.FRANCFORT))


def barre_de_paris_retenue(paris, francfort, douteux, verdicts, valeur, d):
    """Dit si la barre de Paris d'un jour peut entrer au fichier des 20 ans ; rend (barre ou None, motif du refus).

    ① RÔLE — La règle des jours douteux appliquée à une barre de Paris : la même que la réparation et le contrôle.
    ② CONTEXTE D'APPEL — `assembler`, part ② (barres de l'extrait bnains) et part ③ (barres N3 des sociétés sorties,
      `paris` réduit alors à la seule série de la société).
    ③ ENTRÉE — `paris` : {valeur : {date : barre}} · `francfort`, `douteux`, `verdicts` : rendus par
      `jours_douteux_de_paris` · `valeur`, `d`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : (la barre, None) quand elle entre ; (None, None) quand Paris n'a pas de barre ;
      (None, le motif) quand la règle la refuse.
      [rend: 2]
    ⑥ TRAITEMENT — Pas un jour douteux → la barre · jour où l'indice donne tort à l'autre source → la barre ·
      `K.barre_sure` (utilisable, ou d'un jour douteux mais confirmée par Francfort) → la barre · sinon refus, motif
      MOTIF_DEMENTI quand l'indice donne tort à bnains ce jour-là, « jour douteux non confirmé par Francfort » sinon.
      Le motif d'un TROU (part ③) n'est pas celui-ci : il est décidé par `discontinue`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir `jours_douteux_de_paris`. Hors des jours douteux, rien ne change : la barre de Paris est prise
      telle quelle, comme avant ce tour.
    ⑨ CE QUI CLOCHE — `K.barre_sure` exige aussi un volume positif et une barre cohérente, mais seulement un jour
      douteux : hors de ces jours, une barre sans échange entre comme avant (contrôle K3 du contrôle, pas d'ici).
      · Pour une société sortie (part ③), Francfort est rangé sous le nom de l'historique long et la série N3 sous le
      mnémonique (ALO, LI…) : Francfort ne confirme jamais une barre N3 (m-3 du relecteur E2c tour 1, non mesuré ; aucune
      société sortie n'est dans COURS_DE_FRANCFORT.csv, mesuré par le rapport SOURCE_DES_28_COURS pour Alstom et
      Klépierre).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    b = paris.get(valeur, {}).get(d)
    if b is None:
        return None, None
    if d not in douteux or verdicts.get(d) == VERDICT_FICHIER_A_TORT or K.barre_sure(paris, francfort, valeur, d, douteux):
        return b, None
    return None, (MOTIF_DEMENTI if verdicts.get(d) == VERDICT_BNAINS_A_TORT else
                  "jour douteux non confirmé par Francfort")


def discontinue(serie, d, seuil):
    """Dit si la barre d'un jour s'écarte de la barre d'avant ET de celle d'après, qui s'accordent entre elles.

    ① RÔLE — La propriété qui fait d'une barre N3 refusée un jour douteux un TROU DÉCLARÉ (A-748).
    ② CONTEXTE D'APPEL — `assembler`, part ③, pour une barre que `barre_de_paris_retenue` refuse.
    ③ ENTRÉE — `serie` : {date : clôture} d'une société sortie · `d` : une date de `serie` · `seuil` : la variation
      admise d'une séance à la suivante (`seuil_de_variation`, R-104).
    ④ CONDITIONS D'ENTRÉE — Clôtures positives.
    ⑤ SORTIE — UNE valeur : vrai quand la barre a une voisine de chaque côté et que |c ÷ avant − 1| > seuil,
      |après ÷ c − 1| > seuil et |après ÷ avant − 1| ≤ seuil ; faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — Les voisines sont les dates de `serie` juste avant et juste après `d`.
    ⑦ UNITÉ — Des rapports sans unité.
    ⑧ POURQUOI — Rapport SOURCE_DES_28_COURS_ALO_LI (12-11-2026, 22h56) : les barres fausses d'Alstom valent la moitié
      de la vraie, celles de Klépierre le tiers, entre une veille et un lendemain justes ; une vraie division, elle, ne
      revient pas le lendemain (Klépierre 03-09-2007, 115,79 → 38,97 → 41,03). 2007-03-28, entre deux barres fausses,
      n'est pas un jour douteux : cette fonction n'y est pas appelée.
    ⑨ CE QUI CLOCHE — Une barre fausse de moins que le seuil ne se voit pas (LAFARGE, ≈ −13 % les mêmes jours de
      2006-2007, mesuré le 12-11-2026) ; deux barres fausses consécutives non plus (chacune a une voisine fausse).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    dates = sorted(serie)
    i = dates.index(d)
    if i == 0 or i == len(dates) - 1:
        return False
    a, c, b = serie[dates[i - 1]], serie[d], serie[dates[i + 1]]
    return abs(c / a - 1) > seuil and abs(b / c - 1) > seuil and abs(b / a - 1) <= seuil


def lire_les_cours_recoupes(chemin):
    """Lit l'OPTION de A-748 : des barres d'une autre source, qui priment sur un trou déclaré quand elles sont retenues.

    ① RÔLE — Laisser une source trouvée plus tard combler un trou déclaré, par une donnée et sans changer le programme.
    ② CONTEXTE D'APPEL — `assembler`, une fois.
    ③ ENTRÉE — `chemin` : relatif à la racine (SOURCE_RECOUPEE par défaut).
    ④ CONDITIONS D'ENTRÉE — Absent : aucune source. Présent : l'en-tête du contrat COURS_DE_REMPLACEMENT_DES_TROUS, une
      source non vide, `retenue` dans RETENUE, une `decision` non vide pour une ligne « oui », une clé (valeur, date) une
      seule fois — sinon ValueError.
    ⑤ SORTIE — DEUX valeurs : {(valeur, date) : la ligne de huit textes} pour les lignes « oui » ; le nombre de lignes
      « non » (option désactivée).
      [rend: 2]
    ⑥ TRAITEMENT — csv.reader ; contrôles du ④.
    ⑦ UNITÉ — Euros par titre, titres, comme écrits par la source.
    ⑧ POURQUOI — Décision de Jean-Luc du 12-11-2026 à 22h45 (A-748) : « chercher une autre source, et sinon un trou
      déclaré » ; consigne du 12-11-2026 (rapport SOURCE_DES_28_COURS_ALO_LI) : la source d'Alstom est une OPTION
      lue dans un fichier de données, jamais en dur ; le trou déclaré reste le comportement par défaut d'une ligne sans
      « oui » ; décision de Jean-Luc du 12-11-2026 à 23h47 (A-748) : « oui » pour les 13 cours d'Alstom.
    ⑨ CE QUI CLOCHE — Rien ici ne vérifie la preuve écrite dans `preuve` : c'est une donnée. · Une ligne « oui » qui ne
      tombe sur aucun trou déclaré est comptée, jamais versée.
    ⑩ EFFET — Lit un fichier s'il existe.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    if not os.path.exists(chemin):
        return {}, 0
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = [l for l in csv.reader(f) if l]
    if not lignes or lignes[0] != COURS_DE_REMPLACEMENT_DES_TROUS:
        raise ValueError(f"{chemin} : en-tête {lignes[:1]} au lieu de {COURS_DE_REMPLACEMENT_DES_TROUS}")
    sortie, vues, non = {}, set(), 0
    for l in lignes[1:]:
        if (len(l) != len(COURS_DE_REMPLACEMENT_DES_TROUS) or not l[7].strip() or l[8] not in RETENUE
                or (l[8] == "oui" and not l[9].strip()) or (l[0], l[1]) in vues):
            raise ValueError(f"{chemin} : ligne mal formée, sans source, « oui » sans décision, ou en double : {l}")
        vues.add((l[0], l[1]))
        if l[8] == "oui":
            sortie[(l[0], l[1])] = l[:8]
        else:
            non += 1
    return sortie, non


def assembler(racine, coupure=None, recoupee=SOURCE_RECOUPEE):
    """Assemble les quatre parts ; rend les lignes du fichier des 20 ans et ses comptes.

    ① RÔLE — Le cœur : une ligne par (valeur, date), la source écrite.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `racine` · `coupure` : AAAA-MM-JJ, ou None pour la dernière date du maître · `recoupee` : le chemin du
      paramètre de A-748 (`lire_les_cours_recoupes`), relatif à la racine.
    ④ CONDITIONS D'ENTRÉE — Celles du ④ du programme.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes (huit textes chacune, l'ordre de COURS_MAITRE), triée par date puis
      valeur ; un dictionnaire de comptes (« coupure », « debut_du_maitre », « par_part », « non_versees » {raison :
      nombre}, « remplacees » {raison : nombre}, « refus » : liste des défauts qui interdisent d'écrire,
      « jours_douteux » {motif : nombre de barres de Paris refusées}, « trous_declares » : liste des [valeur, date,
      motif], « trous_combles_par_l_option » : liste des [valeur, date, motif, source], « barres_n3_d_un_jour_douteux_
      gardees » : liste des [valeur, date, motif] (VALLOUREC 2006-07-17 et LAFARGE y sont, m-2 du tour 1),
      « barres_n3_redatees » : liste des [valeur, jour de rangement, jour vrai]).
      [rend: 2]
    ⑥ TRAITEMENT — Parts, dans l'ordre de priorité (la première qui écrit une clé la garde, les suivantes sont comptées
      « remplacées ») : ① le maître, lignes de sa première date à la coupure, copiées telles quelles, SAUF les lignes
      « google » (R.SOURCE_GOOGLE) qu'une opération postérieure connue de RECONSTRUIRE touche (`R.facteur_apres` ≠ 1,
      opérations rangées par mnémonique) : ramenées au brut comme la part ② (prix × 1/facteur, volume × facteur, par
      `K.arrondir`), source « google ramené au brut ÷ facteur » ; facteur inconnu → non versée · ② l'historique long,
      lignes d'avant la première date du maître : jusqu'à la dernière séance de bnains, la barre de Paris (lue par
      `K.lire_paris`, barres fausses ôtées et rectifications faites) quand `barre_de_paris_retenue` la prend ; sinon
      la ligne divisée par le facteur des opérations postérieures (`R.facteur_apres`), de même ; facteur inconnu → non
      versée · ③ les barres N3 des sociétés sorties (statut GARDEE), sous leur mnémonique (`cle_d_une_societe_sortie`),
      remises au bon jour par `K.redater_les_journees`, quand `barre_de_paris_retenue` les prend ; refusées ET `discontinue` (seuil lu par `seuil_de_variation`), la
      ligne « oui » de `recoupee` si elle existe, sinon un TROU DÉCLARÉ au motif MOTIF_DISCONTINUE (la clé est fermée
      aux parts suivantes) ; refusées mais continues, la barre est gardée et comptée · ④ les lignes de A_VERSER, sous le mnémonique
      de leur ISIN (LISTE.csv), copiées telles quelles, jusqu'à la coupure, hors des trous déclarés. Puis les refus :
      une clé écrite deux fois, une source vide, un mnémonique de société sortie qui est aussi une écriture d'une
      valeur d'aujourd'hui (le lecteur le rangerait sous elle), deux noms de l'historique long sous un même mnémonique.
    ⑦ UNITÉ — Euros par titre, titres ; des lignes.
    ⑧ POURQUOI — R-108 (le vrai cours de Paris, ramené au brut sinon) ; décision du 12-11-2026 à 09h13 (2024-2026 copie
      FIGÉE ET DATÉE — elle tranche la reproductibilité, pas la convention de prix) ; décision du 11-11-2026 à 20h52
      (PLAN_V7 l. 23) et R-108 ① « le vrai cours est toujours gardé » : les lignes google déjà ajustées sont ramenées
      au brut DANS CE FICHIER SEULEMENT, le maître n'est jamais touché (mesuré le 12-11-2026 : AIR LIQUIDE 2023-12-29
      176,12 → 2024-01-02 144,55 google, fausse chute de −17,9 % ; 619 lignes google d'AIR LIQUIDE portent les
      attributions de 2024 et 2026) ; décisions des 31-10 et 11-11 sur les sociétés sorties ; A-748 (12-11-2026 à
      22h45) pour les trous déclarés ; la priorité de Paris sur Yahoo est celle de R-108 (le vrai cours d'abord).
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme. · La priorité ① → ④ est un ordre posé ici, appliqué aux seules clés
      communes, et compté : il ne tranche qu'entre une barre de Paris et une reconstruction de Yahoo. · Le ramené au
      brut des lignes google suppose que Google a appliqué TOUTES les opérations connues de RECONSTRUIRE postérieures à
      la ligne : mesuré le 12-11-2026, la clôture google vaut celle de l'historique long (corrigé de toutes) à moins de
      0,2 % en médiane pour chaque valeur ; une opération future que Google n'aurait pas appliquée serait divisée à tort
      (aucune connue de RECONSTRUIRE entre le 08-09-2026 et la coupure, au 12-11-2026).
    ⑩ EFFET — Lit des fichiers (le dossier courant devient la racine).
    ⑪ TERMINAISON — Rend la main ou lève OSError / ValueError.
      [sort: non]
    """
    racine = os.path.abspath(racine)
    os.chdir(racine)
    with open(R.MAITRE, encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        if entete != COURS_MAITRE:
            raise ValueError(f"{R.MAITRE} : en-tête {entete} au lieu de {COURS_MAITRE}")
        maitre = [l for l in lecteur if l]
    debut_maitre = min(l[1] for l in maitre)
    coupure = coupure or max(l[1] for l in maitre)
    if coupure < debut_maitre:
        raise ValueError(f"coupure {coupure} avant la première date du maître {debut_maitre}")
    fichier, ops = operations(racine)
    sources_long = {(r["valeur"], r["date"]): r["source"] for r in lire_csv(K.FICHIER)}
    paris, _, _ = K.lire_paris(racine)
    douteux, verdicts, francfort = jours_douteux_de_paris(racine, fichier, paris)
    recoupes, desactivees = lire_les_cours_recoupes(recoupee)
    seuil = seuil_de_variation()
    par_isin, ouverts = identites(lire_csv(IDENTITES))
    nom_vers_isin = {r["valeur"]: r["isin"] for r in lire_csv(LISTE_YAHOO)}
    lc = _lecteur()
    table, _ = lc.table_des_ecritures(racine)
    ops_par_cle, refus = {}, []
    for v, liste in ops.items():          # les opérations rangées par mnémonique : le maître écrit parfois « AIR_LIQUIDE »
        k = table.get(lc.COMMUN.norm_valeur(v), v)
        if k in ops_par_cle:
            refus.append(f"deux noms de l'historique long sous le mnémonique {k}")
        ops_par_cle[k] = liste

    sortie, par_part, non_versees, remplacees = {}, Counter(), Counter(), Counter()
    numero_de, jours_refuses, trous_declares, fermees = {}, Counter(), [], set()
    trous_combles, gardees = [], []

    def poser(valeur, d, barre, source, part):
        """Écrit une ligne sous sa clé, sauf si la clé est déjà prise.

        ① RÔLE — La règle « une clé (valeur, date) écrite une seule fois, par la première part qui l'écrit ».
        ② CONTEXTE D'APPEL — `assembler`, pour chaque ligne de chaque part, dans l'ordre de priorité ① → ④.
        ③ ENTRÉE — `valeur`, `d` (AAAA-MM-JJ), `barre` (cinq textes), `source` (texte), `part` (le nom de la part).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — Clé prise → compter « remplacée » sous la part qui arrive ; sinon écrire et compter.
        ⑦ UNITÉ — Des lignes.
        ⑧ POURQUOI — R-108 : le vrai cours de Paris passe avant une reconstruction, et la copie du maître avant tout.
        ⑨ CE QUI CLOCHE — La clé est le texte de la valeur : deux écritures d'un même nom d'aujourd'hui ne se
          heurteraient pas ici (l'épreuve P1 les range par mnémonique ; 0 mesuré).
        ⑩ EFFET — Modifie `sortie`, `par_part`, `remplacees` de `assembler`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        cle = (valeur, d)
        if cle in sortie:
            remplacees[f"{part} : clé déjà écrite par {sortie[cle][1]}"] += 1
            return
        sortie[cle] = ((valeur, d) + tuple(barre) + (source,), part)
        par_part[part] += 1

    for l in maitre:                                                    # ① le maître
        if l[1] > coupure:
            continue
        if l[7] == R.SOURCE_GOOGLE:     # B2 : déjà corrigée par Google des opérations postérieures (R-108 ①)
            p = R.facteur_apres(ops_par_cle.get(table.get(lc.COMMUN.norm_valeur(l[0]), l[0]), []), l[1])
            if p is None:
                non_versees["① maître google : facteur inconnu"] += 1
                continue
            if p != 1.0:
                poser(l[0], l[1], texte(K.arrondir(tuple(float(x) for x in l[2:7]), 1.0 / p, p)),
                      SOURCE_RAMENEE.format(origine=l[7], p=p), "① maître : google ramené au brut")
                continue
        poser(l[0], l[1], l[2:7], l[7], "① maître")
    for v in sorted(fichier):                                           # ② l'historique long
        for d in sorted(fichier[v]):
            if d >= debut_maitre:
                continue
            b, motif = barre_de_paris_retenue(paris, francfort, douteux, verdicts, v, d) if d <= R.FIN_BNAINS else (None, None)
            if motif:
                jours_refuses["② " + motif] += 1
            if b is not None:
                poser(v, d, texte(K.arrondir(b, 1.0, 1.0)), SOURCE_PARIS, "② historique long : barre de Paris")
                continue
            p = R.facteur_apres(ops.get(v, []), d)
            if p is None:
                non_versees["② historique long : facteur inconnu"] += 1
                continue
            poser(v, d, texte(K.arrondir(fichier[v][d], 1.0 / p, p)),
                  SOURCE_RAMENEE.format(origine=sources_long[(v, d)], p=p), "② historique long : ramené au brut")
    n3 = defaultdict(dict)    # la série de chaque société sortie, pour juger ses jours douteux sur elle seule
    for r in lire_csv(N3):                                              # ③ sociétés sorties, Paris
        if r["statut"] != GARDEE:      # relecteur E2b tour 1, M1 : compté, plus écarté en silence
            non_versees["③ N3 : statut " + r["statut"].split(" (")[0]] += 1
            continue
        m, n = cle_d_une_societe_sortie(par_isin, ouverts, r["isin_passage"], r["date"])
        if m is None:
            non_versees["③ N3 : " + n] += 1
            continue
        numero_de[m] = n
        # 6 449 barres N3 écrivent la décimale par une virgule (« 72,00 », archives de 2000-2001) : lue comme le point,
        # comme le fait déjà etudes/VINGT_ANS_PAR_YAHOO_Dim_08-11-2026/programmes/reconstruire_les_sorties.py (l. 81)
        b = tuple(float(r[c].replace(",", ".")) for c in ("open", "high", "low", "close", "volume"))
        if r["date"] in n3[m]:     # comme `poser` : la première barre d'une clé la garde, la suivante est comptée
            remplacees["③ N3 sociétés sorties : clé déjà écrite par ③ N3 sociétés sorties"] += 1
            continue
        n3[m][r["date"]] = (b, n)
    # E2c tour 2 : les journées que les archives bnains rangent sous un autre jour sont remises au bon jour, par la même
    # fonction que `K.lire_paris` (R-708 ; 19 et 20-06-2001, 55 barres N3 mesurées par le superviseur E2c tour 1)
    redatees = K.redater_les_journees(n3, K.journees_d_un_autre_jour(racine))
    for m in sorted(n3):
        for d in sorted(n3[m]):
            b, n = n3[m][d]
            # la règle des jours douteux, la même que la part ② : appelée sur la seule série de la société sortie
            _, motif = barre_de_paris_retenue({m: {x: y[0] for x, y in n3[m].items()}}, francfort, douteux, verdicts, m, d)
            if motif and discontinue({x: y[0][3] for x, y in n3[m].items()}, d, seuil):   # A-748 : jamais versée
                jours_refuses["③ " + MOTIF_DISCONTINUE] += 1
                fermees.add((m, d))
                if (m, d) in recoupes:
                    poser(m, d, recoupes[(m, d)][2:7], recoupes[(m, d)][7], "③ N3 : option de remplacement retenue")
                    trous_combles.append([m, d, MOTIF_DISCONTINUE, recoupes[(m, d)][7]])
                else:
                    trous_declares.append([m, d, MOTIF_DISCONTINUE])
                    non_versees["③ N3 : trou déclaré — " + MOTIF_DISCONTINUE] += 1
                continue
            if motif:       # refusée par la règle, mais continue : gardée, comptée, et sa clé écrite (m-2 du tour 1)
                jours_refuses["③ " + motif + " — barre continue, gardée"] += 1
                gardees.append([m, d, motif])
            poser(m, d, texte(K.arrondir(b, 1.0, 1.0)), SOURCE_SORTIE.format(numero=n), "③ N3 sociétés sorties")
    hors_trous = sorted(k for k in recoupes if k not in fermees)
    if hors_trous:
        non_versees["option de remplacement : ligne retenue hors d'un trou déclaré"] += len(hors_trous)
    if desactivees:
        non_versees["option de remplacement : ligne non retenue (« non »)"] += desactivees
    for r in lire_csv(YAHOO_SORTIES):                                   # ④ sociétés sorties, Yahoo ramené au brut
        if r["date"] > coupure:
            non_versees["④ A_VERSER : après la coupure"] += 1
            continue
        isin = nom_vers_isin.get(r["valeur"])
        m, n = cle_d_une_societe_sortie(par_isin, ouverts, isin, r["date"]) if isin else (None, "nom sans ISIN")
        if m is None:
            non_versees["④ A_VERSER : " + n] += 1
            continue
        if (m, r["date"]) in fermees:   # A-748 : seule l'option retenue comble un trou déclaré
            non_versees["④ A_VERSER : clé d'un trou déclaré (A-748)"] += 1
            continue
        numero_de[m] = n
        poser(m, r["date"], tuple(r[c] for c in ("open", "high", "low", "close", "volume")), r["source"],
              "④ A_VERSER sociétés sorties")

    lignes = sorted((x for x, _ in sortie.values()), key=lambda x: (x[1], x[0]))
    if len({(x[0], x[1]) for x in lignes}) != len(lignes):
        refus.append("une clé (valeur, date) écrite deux fois")
    vides = sum(1 for x in lignes if not x[7].strip())
    if vides:
        refus.append(f"{vides} ligne(s) sans source")
    heurts = sorted(m for m in numero_de if lc.COMMUN.norm_valeur(m) in table)
    if heurts:
        refus.append(f"mnémonique(s) de société sortie lu(s) comme une valeur d'aujourd'hui : {heurts}")
    return lignes, {"coupure": coupure, "debut_du_maitre": debut_maitre, "par_part": dict(par_part),
                    "non_versees": dict(non_versees), "remplacees": dict(remplacees), "refus": refus,
                    "jours_douteux": dict(jours_refuses), "trous_declares": trous_declares,
                    "trous_combles_par_l_option": trous_combles,
                    "barres_n3_d_un_jour_douteux_gardees": gardees,
                    "barres_n3_redatees": [list(x) for x in redatees],
                    "societes_sorties": dict(sorted(numero_de.items()))}


def _lecteur():
    """Charge le lecteur unique des cours depuis ce dossier.

    ① RÔLE — Donner `table_des_ecritures`, `lire` et `trous` du lecteur unique (R-111), jamais refaits ici.
    ② CONTEXTE D'APPEL — `assembler`, `mesurer_les_trous`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — programmes/LIRE_LES_COURS.py est à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : le module chargé (neuf à chaque appel : il relit le contrat tel qu'il est sur le disque).
      [rend: 1]
    ⑥ TRAITEMENT — importlib, par le chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contrat des fichiers figés est relu à l'import du lecteur ; après `declarer_au_contrat`, un
      lecteur chargé avant ne verrait pas l'entrée nouvelle.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute les déclarations du lecteur et de ses trois voisins.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"lecteur_vingt_ans_{datetime.datetime.now().timestamp()}",
                                                  os.path.join(ICI, "LIRE_LES_COURS.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def nom_du_temoin(coupure, maintenant):
    """Rend le chemin du témoin, relatif à la racine.

    ① RÔLE — Un nom qui dit ce qu'est le fichier, sa période, sa coupure et quand il a été figé.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `coupure` : AAAA-MM-JJ · `maintenant` : l'heure de Paris.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : temoins/TEMOIN_VINGT_ANS_2000_<année de coupure>_COUPURE_<coupure>_FIGE_<Jjj_JJ-MM-AAAA_HHhMM>.csv
      [rend: 1]
    ⑥ TRAITEMENT — Assemblage du nom.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Instructions du projet : horodatage Europe/Paris dans chaque nom de fichier ; le témoin du golden dit
      lui aussi ce qu'il est (TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    quand = f"{JOURS[maintenant.weekday()]}_{maintenant:%d-%m-%Y_%Hh%M}"
    return f"{TEMOINS}/TEMOIN_VINGT_ANS_2000_{coupure[:4]}_COUPURE_{coupure}_FIGE_{quand}.csv"


def ecrire_le_temoin(racine, chemin, lignes):
    """Écrit le témoin ; rend son empreinte.

    ① RÔLE — Le fichier des 20 ans, sur le disque.
    ② CONTEXTE D'APPEL — `main`, avec --ecrire.
    ③ ENTRÉE — `racine` · `chemin` : relatif à la racine · `lignes` : rendues par `assembler`.
    ④ CONDITIONS D'ENTRÉE — Le fichier n'existe pas encore (un témoin ne se réécrit pas).
    ⑤ SORTIE — UNE valeur : l'empreinte sha256 du fichier écrit, relue sur le disque.
      [rend: 1]
    ⑥ TRAITEMENT — En-tête COURS_MAITRE, puis les lignes ; fins de ligne « \\n », UTF-8 sans marque.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'empreinte porte sur les octets (LIRE_LES_COURS ⑨) : une seule façon de les écrire.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève FileExistsError.
      [sort: non]
    """
    with open(os.path.join(racine, chemin), "x", encoding="utf-8", newline="") as f:
        f.write(octets_du_temoin(lignes).decode("utf-8"))
    return empreinte(os.path.join(racine, chemin))


def octets_du_temoin(lignes):
    """Rend les octets exacts du témoin, sans l'écrire.

    ① RÔLE — Une seule façon d'écrire le témoin, pour l'écrire et pour connaître son empreinte AVANT de l'écrire.
    ② CONTEXTE D'APPEL — `ecrire_le_temoin` ; `main` (refus d'un second gel, M3).
    ③ ENTRÉE — `lignes` : rendues par `assembler`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les octets (UTF-8, fins de ligne « \\n », en-tête COURS_MAITRE).
      [rend: 1]
    ⑥ TRAITEMENT — csv.writer dans un tampon.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Relecteur E2b tour 1, M3 : un second --ecrire figeait un second témoin identique.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import io
    tampon = io.StringIO(newline="")
    w = csv.writer(tampon, lineterminator="\n")
    w.writerow(COURS_MAITRE)
    w.writerows(lignes)
    return tampon.getvalue().encode("utf-8")


def variations_hors_seuil(lignes, ops, seuil, table, norm):
    """Relève, dans des lignes de cours, les sauts de clôture que les opérations connues n'expliquent pas, et les
    opérations connues qui ne se voient pas au jour dit.

    ① RÔLE — La propriété de continuité (relecteur E2b tour 1, B1 ; superviseur R-759, marche ①) : les prix viennent
      du marché, les facteurs de la table des opérations ; un facteur inversé ou une date décalée y crée un saut.
    ② CONTEXTE D'APPEL — `signaler` (pour le manifeste) ; l'épreuve P8 (sur le témoin et sur le programme saboté).
    ③ ENTRÉE — `lignes` : listes de huit textes (valeur, date, open, high, low, close, volume, source) · `ops` :
      {nom de l'historique long : liste des (date, facteur, …)} rendue par `operations` · `seuil` : la variation
      admise d'une séance à la suivante (lue par l'appelant dans CONTROLER_LES_COURS.SEUIL_VARIATION, R-104) ·
      `table`, `norm` : la table des écritures du lecteur unique et sa normalisation.
    ④ CONDITIONS D'ENTRÉE — Clôtures lisibles et positives.
    ⑤ SORTIE — DEUX valeurs : ① la liste triée des sauts non expliqués, chacun [clé, date d'avant, date, rapport
      arrondi à 4 décimales] ; ② la liste triée des opérations non vues, chacune [clé, date, facteur, rapport observé
      de la paire qui l'encadre].
      [rend: 2]
    ⑥ TRAITEMENT — Clé : le mnémonique pour une valeur d'aujourd'hui (les deux écritures d'un même nom se suivent),
      le texte sinon. Pour chaque paire de lignes consécutives d'une même clé : le facteur attendu est le produit des
      facteurs des opérations dont la date tombe après la date d'avant et au plus tard à la date ; le saut est
      expliqué quand |rapport ÷ attendu − 1| ≤ seuil. Une opération dont |facteur − 1| > seuil est « non vue » quand
      la paire de lignes qui l'encadre ne l'explique pas ; une opération hors des dates de la valeur n'est pas jugée.
    ⑦ UNITÉ — Des rapports sans unité.
    ⑧ POURQUOI — Une propriété sur toutes les séances, pas sur une couture : une division appliquée un jour trop tôt à
      l'intérieur d'un bloc ramené se voit (superviseur, ①).
    ⑨ CE QUI CLOCHE — Une opération dont le facteur reste dans le seuil (une action gratuite pour dix, 0,909) ne se
      distingue pas du mouvement d'une séance : ni son absence ni son décalage ne se voient. · Les opérations des
      sociétés sorties ne sont pas connues de RECONSTRUIRE : leurs sauts sont tous « non expliqués ». · Les lignes
      « google » du maître portent déjà les opérations : sur le maître, celles de 2024 → 2026-09-08 sont « non vues » ;
      sur le fichier des 20 ans, depuis E2c, l'assemblage ramène ces lignes au brut et elles se voient au jour dit.
      · Les sauts relevés sont SIGNALÉS, jamais retirés ni corrigés (R-109 ④), et SANS VERDICT : une variation de plus
      que le seuil n'est pas un invariant des cours (244 paires réelles au-delà de 25 % au 12-11-2026 ; superviseur
      R-759 de E2b, tour 2) ; le juge des sauts, sur la courbe corrigée de R-108 ② et le calendrier officiel, revient
      au lecteur unique (A-713). · Ce sont des LIGNES consécutives, pas des séances : 8 des 211 sauts du 12-11-2026
      enjambent un trou (ALO 2017-02-28 → 2020-09-21, NOKIA 2004-10-12 → 2011-04-19…), où le seuil d'une séance n'a pas
      de sens (relecteur E2b tour 2, m4). · Seul le second rendu, les opérations non vues, sert d'invariant (épreuve P8).
      · Seul un décalage VERS PLUS TÔT ou un facteur faux se voit : décalée d'une séance PLUS TARD, une opération reste
      expliquée par la paire qui suit (mesuré par le relecteur E2b tour 3, m3 : AIR LIQUIDE 2017-10-02 → 10-03, sortie
      identique) ; ancrer le jour J sur la barre de Paris va à A-713.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cle_de = lambda v: table.get(norm(v), v)
    series = defaultdict(list)
    for l in lignes:
        series[cle_de(l[0])].append((l[1], float(l[5])))
    par_cle = defaultdict(list)
    for v, liste in ops.items():
        par_cle[cle_de(v)].extend((x, f) for x, f, *_ in liste if f is not None)
    sauts, non_vues = [], []
    for k, s in series.items():
        s.sort()
        o = sorted(par_cle.get(k, []))
        vues, rapport = set(), {}
        for (d0, c0), (d1, c1) in zip(s, s[1:]):
            dans = [(x, f) for x, f in o if d0 < x <= d1]
            attendu = 1.0
            for _, f in dans:
                attendu *= f
            r = c1 / c0
            for op in dans:
                rapport[op] = round(r, 4)
            if abs(r / attendu - 1) <= seuil:
                vues.update(dans)
            elif abs(r - 1) > seuil or dans:
                sauts.append([k, d0, d1, round(r, 4)])
        for x, f in o:
            if abs(f - 1) > seuil and (x, f) not in vues and s and s[0][0] < x <= s[-1][0]:
                non_vues.append([k, x, round(f, 6), rapport.get((x, f))])
    return sorted(sauts), sorted(non_vues, key=lambda n: (n[0], n[1]))


def seuil_de_variation():
    """Lit le seuil de variation d'une séance (R-104) là où il est écrit.

    ① RÔLE — Le seuil de la propriété de continuité, jamais recopié (R-708).
    ② CONTEXTE D'APPEL — `signaler` ; l'épreuve.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — programmes/CONTROLER_LES_COURS.py est à côté de ce fichier et définit SEUIL_VARIATION.
    ⑤ SORTIE — UNE valeur : le seuil, une fraction.
      [rend: 1]
    ⑥ TRAITEMENT — Charger le module par son chemin (ses déclarations seulement), lire la constante.
    ⑦ UNITÉ — Une fraction (0,25 = 25 % le 12-11-2026).
    ⑧ POURQUOI — Superviseur R-759 de E2b, tour 1 : « LU, jamais recopié ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute les déclarations de CONTROLER_LES_COURS.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("controler_les_cours_seuil", os.path.join(ICI, "CONTROLER_LES_COURS.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return float(m.SEUIL_VARIATION)


def signaler(racine, lignes, comptes):
    """Rend ce que le manifeste dit en plus des comptes : sauts non expliqués, opérations non vues, manques non comptés.

    ① RÔLE — Écrire au manifeste ce que la propriété de continuité trouve, et ce qui n'est pas compté.
    ② CONTEXTE D'APPEL — `main` (--ecrire, et l'essai à blanc pour le refus du gel).
    ③ ENTRÉE — `racine` · `lignes`, `comptes` : rendus par `assembler`.
    ④ CONDITIONS D'ENTRÉE — Le dossier courant est la racine.
    ⑤ SORTIE — UNE valeur : {« seuil_de_variation », « sauts_signales », « operations_non_vues »,
      « trous_des_societes_sorties »}.
      [rend: 1]
    ⑥ TRAITEMENT — `seuil_de_variation`, `operations`, `variations_hors_seuil`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Écrits une fois au gel, à titre INFORMATIF (superviseur R-759 de E2b, tour 3, ②) : aucune épreuve
      ne les relit. Superviseur R-759 de E2b, tour 1, marche ⑤ 3 : les barres repérées sont signalées, pas retirées ; les
      trous des sociétés sorties ne sont PAS comptés ici (une seconde table des trous serait contraire à R-708) :
      le lecteur unique ne les connaît pas (QE).
    ⑨ CE QUI CLOCHE — Voir `variations_hors_seuil`.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    lc = _lecteur()
    table, _ = lc.table_des_ecritures(racine)
    seuil = seuil_de_variation()
    _, ops = operations(racine)
    sauts, non_vues = variations_hors_seuil(lignes, ops, seuil, table, lc.COMMUN.norm_valeur)
    return {"seuil_de_variation": seuil, "sauts_signales": sauts, "operations_non_vues": non_vues,
            "trous_des_societes_sorties": "non comptés — le lecteur unique ne connaît pas les sociétés sorties (QE)"}


def empreinte(chemin):
    """Rend l'empreinte sha256 d'un fichier.

    ① RÔLE — L'empreinte, comme la calcule LIRE_LES_COURS.lire pour un fichier figé.
    ② CONTEXTE D'APPEL — `ecrire_le_temoin` ; l'épreuve.
    ③ ENTRÉE — `chemin`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — sha256 des octets.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def declarer_au_contrat(racine, chemin, fin, sha):
    """Ajoute le témoin à FICHIERS_DE_COURS_FIGES du contrat des fichiers.

    ① RÔLE — Figer le témoin : sa dernière séance et son empreinte, écrites au contrat que relit le lecteur unique.
    ② CONTEXTE D'APPEL — `main`, avec --ecrire, après `ecrire_le_temoin`.
    ③ ENTRÉE — `racine` · `chemin` : du témoin, relatif à la racine · `fin` : AAAA-MM-JJ · `sha` : son empreinte.
    ④ CONDITIONS D'ENTRÉE — Le contrat contient exactement une ligne « FICHIERS_DE_COURS_FIGES = { » ; le chemin n'y
      est pas encore.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Insérer trois lignes juste après l'ouverture du dictionnaire, puis relire le contrat comme module
      et vérifier que l'entrée y est, telle quelle ; sinon remettre le texte d'avant et lever.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-728 : l'empreinte se calcule, elle ne se recopie pas à la main.
    ⑨ CE QUI CLOCHE — Remplacement de texte dans un .py (voir ⑨ du programme).
    ⑩ EFFET — Écrit programmes/CONTRATS_DES_FICHIERS.py.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    p = os.path.join(racine, CONTRAT)
    with open(p, encoding="utf-8") as f:
        avant = f.read()
    ouverture = "FICHIERS_DE_COURS_FIGES = {\n"
    if avant.count(ouverture) != 1 or f'"{chemin}"' in avant:
        raise ValueError(f"contrat : ouverture trouvée {avant.count(ouverture)} fois, ou {chemin} déjà déclaré")
    entree = f'    "{chemin}": {{\n        "fin": "{fin}",\n        "sha256": "{sha}"}},\n'
    with open(p, "w", encoding="utf-8") as f:
        f.write(avant.replace(ouverture, ouverture + entree))
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"contrat_relu_{sha[:8]}", p)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        ok = m.FICHIERS_DE_COURS_FIGES.get(chemin) == {"fin": fin, "sha256": sha}
    except Exception:   # noqa: BLE001 — tout échec de relecture remet le contrat d'avant
        ok = False
    if not ok:
        with open(p, "w", encoding="utf-8") as f:
            f.write(avant)
        raise ValueError("contrat : l'entrée écrite ne se relit pas ; contrat remis tel qu'avant")


def mesurer_les_trous(racine, chemin):
    """Lit le témoin par le lecteur unique ; rend ce qu'il en dit, trous compris.

    ① RÔLE — Écrire le manque (règle A8) tel que le juge le verra : par le lecteur unique, jamais recalculé ici.
    ② CONTEXTE D'APPEL — `main`, avec --ecrire, après `declarer_au_contrat` ; l'épreuve.
    ③ ENTRÉE — `racine` · `chemin` : du témoin, relatif à la racine.
    ④ CONDITIONS D'ENTRÉE — Le témoin est déclaré figé au contrat.
    ⑤ SORTIE — UNE valeur : {« fige », « fige_modifie », « lignes_lues », « lignes_mises_a_part », « inconnues »
      {nom : lignes}, « trous » {mnémonique : {nature : nombre}}, « seances_sans_cours » : le total}.
      [rend: 1]
    ⑥ TRAITEMENT — `lire`, `lignes_mises_a_part`, puis `trous` pour chaque mnémonique rangé.
    ⑦ UNITÉ — Des séances du calendrier ; des lignes.
    ⑧ POURQUOI — Une seule table des trous (R-708) : ce programme n'en crée pas d'autre ; il écrit au manifeste ce que
      le lecteur mesure, avec la nature qu'il lit dans donnees/NATURE_DES_TROUS.csv.
    ⑨ CE QUI CLOCHE — Les sociétés sorties sont « inconnues » du lecteur : leurs trous ne sont pas mesurés.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    lc = _lecteur()
    c = lc.lire(racine, chemin)
    trous = {m: dict(Counter(n for _, n in lc.trous(c, m))) for m in sorted(c["barres"])}
    return {"fige": c["fige"], "fige_modifie": c["fige_modifie"], "fin_du_fige": str(c["fin_du_fige"]),
            "lignes_lues": c["lignes_lues"], "lignes_mises_a_part": lc.lignes_mises_a_part(c),
            "inconnues": dict(sorted(c["inconnues"].items())),
            "trous": {m: t for m, t in trous.items() if t},
            "seances_sans_cours": sum(sum(t.values()) for t in trous.values())}


def _contrat_relu(racine):
    """Relit le contrat des fichiers tel qu'il est sur le disque.

    ① RÔLE — Connaître les fichiers figés déclarés au moment de l'appel.
    ② CONTEXTE D'APPEL — `main`, pour le refus d'un second gel (M3).
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — programmes/CONTRATS_DES_FICHIERS.py existe sous la racine.
    ⑤ SORTIE — UNE valeur : le module relu.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, sous un nom neuf.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le module importé au lancement peut dater d'avant une écriture du contrat.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute les déclarations du contrat.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"contrat_{datetime.datetime.now().timestamp()}",
                                                  os.path.join(racine, CONTRAT))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(argv):
    """Assemble, et avec --ecrire fige ; rend le code de sortie.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande (② du programme).
    ③ ENTRÉE — `argv` : racine, --coupure=AAAA-MM-JJ, --ecrire.
    ④ CONDITIONS D'ENTRÉE — Toute autre option arrête (code 2).
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — `assembler` ; refus → 1 ; l'empreinte du contenu calculée avant toute écriture ; à blanc →
      afficher ; --ecrire → refus si la même empreinte est déjà au contrat (M3), refus s'il reste une opération non vue
      (`signaler`, m2 du tour 3), sinon témoin, contrat, trous, manifeste (avec `signaler`, informatif), durées.
    ⑦ UNITÉ — Des secondes pour les durées affichées.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir ⑩ du programme. Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    args = [a for a in argv if not a.startswith("--")]
    opts = [a for a in argv if a.startswith("--")]
    mal = [a for a in opts if a != "--ecrire" and not (a.startswith("--coupure=") and len(a) == len("--coupure=") + 10)]
    if len(args) != 1 or not os.path.isdir(args[0]) or mal:
        print("USAGE : ASSEMBLER_LES_VINGT_ANS.py <racine> [--coupure=AAAA-MM-JJ] [--ecrire]")
        return 2
    racine = os.path.abspath(args[0])
    coupure = next((a.split("=", 1)[1] for a in opts if a.startswith("--coupure=")), None)
    t0 = datetime.datetime.now().timestamp()
    try:
        lignes, comptes = assembler(racine, coupure)
    except (OSError, ValueError, KeyError) as e:
        print(f"ARRÊT — l'assemblage n'a pas pu tourner : {type(e).__name__} : {e}")
        return 2
    comptes["duree_d_assemblage_s"] = round(datetime.datetime.now().timestamp() - t0, 1)
    comptes["lignes"] = len(lignes)
    comptes["premiere_date"], comptes["derniere_date"] = lignes[0][1], lignes[-1][1]
    print(json.dumps({k: v for k, v in comptes.items() if k != "societes_sorties"}, ensure_ascii=False, indent=1))
    if comptes["refus"]:
        print("REFUS — rien n'est écrit : " + " · ".join(comptes["refus"]))
        return 1
    octets = octets_du_temoin(lignes)
    sha = hashlib.sha256(octets).hexdigest()
    deja = [c for c in _contrat_relu(racine).FICHIERS_DE_COURS_FIGES.items() if c[1]["sha256"] == sha]
    if "--ecrire" not in opts:
        print("ESSAI À BLANC — rien n'est écrit (--ecrire pour figer)")
        return 0
    if deja:   # relecteur E2b tour 1, M3 : un second gel d'un même contenu est refusé, par l'empreinte
        print(f"REFUS — ce contenu est déjà figé sous {deja[0][0]} (même empreinte {sha[:16]}) : rien n'est écrit")
        return 1
    signale = signaler(racine, lignes, comptes)
    if signale["operations_non_vues"]:   # relecteur E2b tour 3, m2 : on ne fige pas un témoin qui ne passe pas P8
        print(f"REFUS — {len(signale['operations_non_vues'])} opération(s) non vue(s) au jour dit : rien n'est écrit · "
              f"{signale['operations_non_vues'][:3]}")
        return 1
    maintenant = datetime.datetime.now(ZoneInfo("Europe/Paris"))
    chemin = nom_du_temoin(comptes["coupure"], maintenant)
    try:
        sha = ecrire_le_temoin(racine, chemin, lignes)
        declarer_au_contrat(racine, chemin, comptes["derniere_date"], sha)
        t1 = datetime.datetime.now().timestamp()
        lu = mesurer_les_trous(racine, chemin)
    except (OSError, ValueError) as e:
        print(f"ARRÊT — le témoin n'a pas pu être figé : {type(e).__name__} : {e}")
        return 2
    manifeste = dict(comptes, **signale, temoin=chemin, sha256=sha, fige_le=maintenant.isoformat(timespec="minutes"),
                     octets=os.path.getsize(os.path.join(racine, chemin)),
                     duree_de_lecture_par_le_lecteur_s=round(datetime.datetime.now().timestamp() - t1, 1),
                     lecture_par_le_lecteur_unique=lu)
    with open(os.path.join(racine, chemin[:-4] + "_MANIFESTE.json"), "x", encoding="utf-8") as f:
        json.dump(manifeste, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"FIGÉ {chemin} · {manifeste['octets']} octets · sha256 {sha} · fin {comptes['derniere_date']} · "
          f"lecteur : {lu['lignes_mises_a_part']} ligne(s) mises à part, {lu['seances_sans_cours']} séance(s) sans cours")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
