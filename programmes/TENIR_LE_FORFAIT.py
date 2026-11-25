#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tient le journal du forfait d'utilisation de Claude et rend un verdict : continuer, alerter, ou arrêter les nouveaux agents.

Simulation boursière uniquement : ce programme ne touche ni aux cours ni aux positions, et ne passe aucun ordre.

① RÔLE — Remplacer le calcul du forfait que le Chat faisait « de tête » par un programme qui refait le même calcul à
  l'identique (R-754 : ce qu'un programme peut faire, un programme le fait). Trois parties.
  ① Un JOURNAL qui ne fait que grandir, `donnees/JOURNAL_DU_FORFAIT.csv` : les captures de la jauge (date et heure de
     Paris, pourcentage, source), la consommation de chaque agent fini (date, étiquette, jetons), et les remises à
     zéro (date de la remise, date et heure de la suivante).
  ② Des COMMANDES pour y ajouter une ligne, et `--etat`, qui rend le rythme réel en points de jauge par heure (entre
     les deux dernières captures), le RYTHME DE POINTE (le plus fort rythme entre deux captures qui
     montent dans la période, chacune avec la plus récente qui la précède d'au moins
     `duree_min_d_une_paire`), le rapport « jetons par point » calé sur les captures, la JAUGE PROJETÉE à l'instant
     présent (dernière capture + le plus grand de : jetons des agents finis depuis ÷ rapport, et rythme de pointe ×
     âge réel de la capture ; A-827, décision de Jean-Luc du 15-11-2026 à 16h41 ; rapport inconnu : une BORNE BASSE,
     dernière capture + rythme de pointe × âge, qui peut faire alerter ou arrêter mais jamais continuer — K-1), la projection à la prochaine
     remise, l'heure prévue pour atteindre le seuil, et un verdict pris sur la jauge projetée : CONTINUER · ALERTER
     (jauge ≥ seuil − marge) · ARRÊTER LES NOUVEAUX AGENTS (jauge ≥ seuil) · INCONNU quand les données ne suffisent
     pas. Jamais un chiffre inventé.
  ③ Le SEUIL, la MARGE d'alerte, l'ÂGE MAXIMAL d'une capture et la DURÉE MINIMALE d'une paire de captures pour le
     rythme de pointe (P-1 de Cowork, 15-11-2026) vivent dans UN seul fichier de réglage,
     `donnees/REGLAGES_DU_FORFAIT.csv`, lu à chaque `--etat` ; aucun des quatre n'est écrit dans ce code (R-708 : un
     chiffre qui existe ailleurs ne se recopie pas). Une capture plus vieille que l'âge maximal est une donnée qui
     manque : la jauge est INCONNUE et le compte rendu dit « demander une capture » (superviseur R-759 du 15-11-2026).
② CONTEXTE D'APPEL — Lancé à la main par le Chat : `--capture` quand Jean-Luc envoie une capture de la jauge,
  `--agent` à la fin de chaque agent (avec les jetons que l'agent a rendus), `--remise` quand une remise à zéro a
  lieu, et `--etat` à chaque réveil de l'heure. Ce geste était le geste 9 du §13.2 de MODE_EMPLOI_DEPOT.md sur
  cette branche ; à la fusion de main du 25-11-2026, la version de main du mode d'emploi a été gardée (consigne de la
  demande) et ce geste n'y figure plus : son texte vit, à l'octet, dans
  archives/MODE_EMPLOI_DEPOT_BRANCHE_TRAVAIL-FORF2_GESTE_9_DU_FORFAIT_REMPLACE_PAR_LA_VERSION_DE_MAIN_A_LA_FUSION_Mer_25-11-2026.md,
  en attente de réinsertion (question dans echanges/A_RELIRE.md). Éprouvé par
  tests/EPREUVES_DU_FORFAIT_Dim_15-11-2026.py. Aucune tâche du soir ne l'appelle.
③ ENTRÉE — La ligne de commande, une action à la fois :
  `--capture POURCENT --a AAAA-MM-JJTHH:MM [--source TEXTE]` · `--agent ETIQUETTE JETONS [--a …]` ·
  `--remise PROCHAINE [--a …]` (PROCHAINE : date et heure de la remise suivante ; `--a` : date de celle qui vient
  d'avoir lieu, maintenant par défaut) · `--etat [--maintenant AAAA-MM-JJTHH:MM]`.
  Options communes : `--journal CHEMIN` et `--reglages CHEMIN` (par défaut, les deux fichiers de `donnees/` du dépôt
  qui contient ce programme). Toutes les heures sont des heures de PARIS.
④ CONDITIONS D'ENTRÉE — Le journal, s'il existe, porte exactement l'en-tête de COLONNES. Le fichier de réglage
  existe et porte les quatre réglages `seuil_d_arret`, `marge_d_alerte`, `age_max_de_la_capture` et
  `duree_min_d_une_paire`, en nombres finis. Un pourcentage est entre 0 et
  100, des jetons sont un entier positif ou nul, une étiquette n'a ni virgule ni saut de ligne.
⑤ SORTIE — Un code de sortie et un compte rendu affiché. Ajout : 0 si la ligne est écrite, 2 si elle est refusée.
  `--etat` : 0 CONTINUER · 3 ALERTER · 4 ARRÊTER LES NOUVEAUX AGENTS · 5 INCONNU · 2 réglage ou journal illisible
  (R-734 : un contrôle qui n'a pas pu conclure ne rend jamais 0).
⑥ TRAITEMENT — Voir `main`, `ajouter` et `etat`.
⑦ UNITÉ — Pourcentages et POINTS de jauge (un point = 1 % de la jauge hebdomadaire) · JETONS (tokens) · heures ·
  dates et heures de Paris, au format AAAA-MM-JJTHH:MM.
⑧ POURQUOI — Le 14-11-2026 vers 22h45, le forfait hebdomadaire s'est épuisé sans alerte : le Chat extrapolait
  depuis une seule capture (75 % à 11h03) à 0,35 point par heure, sans compter la quinzaine d'agents lancés entre 19h
  et 22h45, et trois réparations se sont arrêtées net (A-799). Décision de Jean-Luc du 15-11-2026 à 12h42 (A-804) :
  « il faudra une mécanique à insérer dans le plan obligatoire qui consiste à gérer […] le forfait […] et ton calcul
  théorique, avec les arrêts, l'arrêt prévu à 95 % par exemple, qui peut bien sûr être mis en cause ».
⑨ CE QUI CLOCHE — ① Le rapport « jetons par point » ne compte que les agents inscrits : la consommation propre du
  Chat (relecture de son contexte à chaque action) entre dans les points mais pas dans les jetons ; le rapport la
  répartit donc sur les agents, ce qui ne tient que si leur part reste la même. ② Le rapport se cale dans la période
  en cours seulement : au début de chaque semaine, il reste INCONNU tant qu'il n'y a pas deux captures avec des agents
  inscrits entre elles. ③ « Append-only » est tenu par ce programme, qui n'ouvre le journal qu'en ajout ; une
  réécriture à la main ne serait pas détectée. ④ Une remise oubliée au journal fait paraître la jauge en baisse : le
  programme le signale (ANOMALIE) et rend INCONNU pour le rythme et le rapport. ⑤ La limite de 5 heures, si elle
  existe à côté de la limite de la semaine (A-803), n'est pas suivie. ⑥ TROU MESURÉ, PAS BORNÉ : un agent non
  inscrit pendant la fenêtre d'âge d'une capture (au plus `age_max_de_la_capture`) n'est vu que par le terme
  « rythme de pointe × âge » de la jauge projetée (A-827) ; une pointe plus forte que toute paire de captures
  consécutives n'est pas vue. `--etat` affiche en plus, pour information, une borne BASSE de ce trou mesurée sur les
  captures du journal (`trou_mesure`), confrontée à la marge d'alerte. Le chiffre « 2,14 points/h × 2 h = 4,3
  points », écrit ici avant le 15-11-2026 16h, était faux (G-1 de Cowork) : une moyenne sur 11,7 h prise pour une
  pointe. Sur les captures du 15-11 (0 % à 12h14, 10 % à 14h16, 17 % à 15h27), la borne basse vaut 17 ÷ 2 = 8,5
  points (3,22 h se couvrent par deux fenêtres de 2 h, dont l'une a reçu au moins la moitié des 17 points), sous la
  marge de 10 sans prouver qu'elle couvre le trou. Le chiffre « 17 × 2 ÷ 3,22 = 10,6 », écrit ici avant le
  25-11-2026, était une extrapolation et non une borne (G-5 de Cowork) : 8,5 points au début et 8,5 à la fin de la
  paire laissent toute fenêtre de 2 h à 8,5. Le superviseur R-759 du 15-11-2026 à 16h42 a jugé « RUSTINE » une
  réparation qui affichait ce trou sans changer le verdict ; Jean-Luc a décidé à 16h41 (A-827, réponse « 1 ») que le
  verdict se prend sur la jauge projetée au rythme mesuré. ⑦ Le Chat date lui-même `--a` : une capture
  datée trop récemment contournerait l'âge maximal ; `inscrit_le_paris` permet de recouper, sans contrôle ici.
  ⑧ RYTHME DE POINTE SUR DES PAIRES COURTES (P-1 et K-2 de Cowork, 15-11-2026) :
  la jauge se lit au point près, et une paire de captures à une minute d'écart qui gagne un point
  donne 60 points/h ; le réglage `duree_min_d_une_paire` écarte les paires plus courtes que lui, mais sa valeur est
  0 (aucune paire écartée, comportement d'avant) tant que Jean-Luc ne l'a pas choisie.
⑩ EFFET — Les commandes d'ajout ÉCRIVENT une ligne en fin de journal (et l'en-tête s'il n'existait pas). `--etat`
  n'écrit rien. Aucun accès réseau.
⑪ TERMINAISON — Rend un code de sortie au système par `sys.exit` à la toute fin ; aucun appel ne peut ne pas
  revenir (aucune attente, aucun réseau).
⑫ DÉFINITIONS
  la jauge : le pourcentage « Tous les modèles » de la limite hebdomadaire, tel que l'application le montre
  une remise : la remise à zéro de la jauge (hebdomadaire, ou réinitialisation gratuite utilisée par Jean-Luc)
  une période : l'intervalle entre deux remises ; seules les lignes de la période en cours servent au calcul
"""
import argparse
import csv
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURNAL_PAR_DEFAUT = os.path.join(RACINE, "donnees", "JOURNAL_DU_FORFAIT.csv")
REGLAGES_PAR_DEFAUT = os.path.join(RACINE, "donnees", "REGLAGES_DU_FORFAIT.csv")
COLONNES = ["type", "horodatage_paris", "valeur", "etiquette", "source", "prochaine_remise_paris", "inscrit_le_paris"]
FORMAT = "%Y-%m-%dT%H:%M"


def lire_horodatage(texte):
    """Lit une date et heure de Paris écrite AAAA-MM-JJTHH:MM.

    ① RÔLE — Transformer le texte d'une heure en un instant comparable, dans le fuseau de Paris.
    ② CONTEXTE D'APPEL — `main` (arguments `--a`, `--remise`, `--maintenant`) et `lire_journal` (chaque ligne).
    ③ ENTRÉE — `texte` : par exemple « 2026-11-15T12:14 ».
    ④ CONDITIONS D'ENTRÉE — Exactement ce format ; sinon ValueError.
    ⑤ SORTIE — UNE valeur : l'instant, avec le fuseau Europe/Paris.
      [rend: 1]
    ⑥ TRAITEMENT — Lecture stricte au format, puis rattachement au fuseau de Paris.
    ⑦ UNITÉ — Une date et heure de Paris, à la minute.
    ⑧ POURQUOI — Les captures de Jean-Luc portent l'heure de Paris ; deux écritures de l'heure qui divergent font des
      rythmes faux.
    ⑨ CE QUI CLOCHE — Une heure ambiguë du changement d'heure d'octobre est prise dans sa première occurrence. Les
      écarts entre deux instants se calculent par `heures`, en UTC (F-6 de Cowork, 15-11-2026) : deux instants du même
      fuseau se soustraient sinon à l'horloge murale.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    return datetime.strptime(texte.strip(), FORMAT).replace(tzinfo=PARIS)


def heures(debut, fin):
    """Rend le nombre d'heures réelles entre deux instants.

    ① RÔLE — Mesurer un écart de temps sans se laisser tromper par le changement d'heure.
    ② CONTEXTE D'APPEL — `etat` : rythme, âge de la capture, projection, heure du seuil.
    ③ ENTRÉE — `debut` et `fin` : deux instants avec fuseau.
    ④ CONDITIONS D'ENTRÉE — Les deux portent un fuseau.
    ⑤ SORTIE — UNE valeur : les heures, négatives si `fin` précède `debut`.
      [rend: 1]
    ⑥ TRAITEMENT — Les deux instants passent en UTC, puis se soustraient.
    ⑦ UNITÉ — Heures.
    ⑧ POURQUOI — F-6 de Cowork (15-11-2026) : en Python, deux instants du même `ZoneInfo` se soustraient à l'horloge
      murale ; 01h30 → 03h30 le 28-03-2027 comptait 2 h au lieu d'1, et le rythme était divisé par deux.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return (fin.astimezone(timezone.utc) - debut.astimezone(timezone.utc)).total_seconds() / 3600


def lire_reglages(chemin):
    """Lit le seuil d'arrêt, la marge d'alerte, l'âge maximal d'une capture et la durée minimale d'une paire.

    ① RÔLE — Donner au calcul le seuil, la marge, l'âge maximal et la durée minimale fixés, depuis LEUR seul endroit.
    ② CONTEXTE D'APPEL — `main`, pour `--etat`.
    ③ ENTRÉE — `chemin` : le fichier de réglage, CSV à virgules, en-tête `reglage,valeur,etat,qui_decide,raison`.
    ④ CONDITIONS D'ENTRÉE — Les lignes `seuil_d_arret`, `marge_d_alerte`, `age_max_de_la_capture` et
      `duree_min_d_une_paire` existent, une seule fois chacune, avec un nombre FINI ; le seuil est dans ]0, 100], la
      marge positive ou nulle, l'âge strictement positif, la durée minimale positive ou nulle ; sinon ValueError, ou
      OSError si le fichier manque.
    ⑤ SORTIE — QUATRE valeurs : le seuil d'arrêt et la marge d'alerte (points de jauge), l'âge maximal et la durée
      minimale d'une paire (heures).
      [rend: 4]
    ⑥ TRAITEMENT — Lire toutes les lignes, retenir les quatre réglages, vérifier qu'ils sont uniques, finis et bornés.
    ⑦ UNITÉ — Points de jauge ; heures pour l'âge maximal et la durée minimale.
    ⑧ POURQUOI — Le seuil de 95 % est contestable par Jean-Luc (A-799, A-804) : il change dans le fichier, jamais dans
      le code (R-708). La durée minimale d'une paire vient de P-1 et K-2 de Cowork (15-11-2026) ; sa valeur est une
      décision de Jean-Luc, pas du programme.
    ⑨ CE QUI CLOCHE — `nan` et `inf` sont refusés depuis F-5 de Cowork (15-11-2026) : une marge `nan` éteignait
      l'alerte sans un mot.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    noms = ("seuil_d_arret", "marge_d_alerte", "age_max_de_la_capture", "duree_min_d_une_paire")
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    vus = {}
    for l in lignes:
        cle = (l.get("reglage") or "").strip()
        if cle in noms:
            if cle in vus:
                raise ValueError(f"réglage {cle} écrit deux fois dans {chemin}")
            vus[cle] = float((l.get("valeur") or "").strip().replace(",", "."))
    if set(vus) != set(noms):
        raise ValueError(f"réglage absent de {chemin} : " + ", ".join(sorted(set(noms) - set(vus))))
    if not all(math.isfinite(v) for v in vus.values()):
        raise ValueError(f"réglage non fini (nan ou inf) dans {chemin} : {vus}")
    if (not 0 < vus["seuil_d_arret"] <= 100 or vus["marge_d_alerte"] < 0 or vus["age_max_de_la_capture"] <= 0
            or vus["duree_min_d_une_paire"] < 0):
        raise ValueError(f"réglage hors bornes dans {chemin} : {vus}")
    return vus["seuil_d_arret"], vus["marge_d_alerte"], vus["age_max_de_la_capture"], vus["duree_min_d_une_paire"]


def lire_journal(chemin):
    """Lit le journal du forfait et rend ses lignes, avec leurs instants.

    ① RÔLE — Donner au calcul toutes les lignes du journal, dans l'ordre du fichier, chaque heure déjà lue.
    ② CONTEXTE D'APPEL — `main`, pour `--etat` et avant chaque ajout (pour vérifier l'en-tête).
    ③ ENTRÉE — `chemin` : le journal.
    ④ CONDITIONS D'ENTRÉE — S'il existe, son en-tête est exactement COLONNES ; sinon ValueError. Absent : liste vide.
    ⑤ SORTIE — UNE valeur : la liste des lignes (dictionnaires), chacune complétée de `t` (l'instant de la ligne) et,
      pour une remise, de `t_prochaine`.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le CSV, vérifier l'en-tête ; pour chaque ligne, refuser des champs en trop ou manquants, lire
      l'heure, le type et la valeur (capture : nombre de 0 à 100 ; agent : entier positif ou nul ; remise : vide).
      Toute ligne refusée lève ValueError avec son numéro.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un journal dont l'en-tête a changé serait lu de travers sans le dire. F-3 de Cowork (15-11-2026) :
      une ligne collée à la précédente (dernier saut de ligne ôté par un éditeur) portait des champs en trop, que
      DictReader range sous la clé None ; la capture de 97 % disparaissait et le verdict restait INCONNU au lieu
      d'ARRÊTER. F-4 : une valeur illisible faisait tomber le programme sur une trace Python au lieu d'une ERREUR.
      G-2 (15-11-2026) : « ² » passe `isdigit` mais pas `int` ; d'où `isascii` et `int` dans le même `try`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != COLONNES:
            raise ValueError(f"en-tête inattendu dans {chemin} : {lecteur.fieldnames}")
        lignes = []
        for n, l in enumerate(lecteur, start=2):
            if None in l or any(v is None for v in l.values()):
                raise ValueError(f"ligne {n} de {chemin} : champs en trop ou manquants (ligne collée ou coupée ?)")
            try:
                l["t"] = lire_horodatage(l["horodatage_paris"])
                l["t_prochaine"] = (lire_horodatage(l["prochaine_remise_paris"])
                                    if l["type"] == "remise" else None)
            except ValueError as e:
                raise ValueError(f"ligne {n} de {chemin} : heure illisible ({e})")
            if l["type"] not in ("capture", "agent", "remise"):
                raise ValueError(f"ligne {n} de {chemin} : type inconnu « {l['type']} »")
            v = l["valeur"].strip()
            try:
                ok = ((l["type"] == "capture" and 0 <= float(v) <= 100)
                      or (l["type"] == "agent" and v.isascii() and v.isdigit() and int(v) >= 0)
                      or (l["type"] == "remise" and v == ""))
            except ValueError:
                ok = False
            if not ok:
                raise ValueError(f"ligne {n} de {chemin} : valeur « {v} » illisible pour le type {l['type']}")
            lignes.append(l)
    return lignes


def ajouter(chemin, ligne):
    """Ajoute une ligne en fin de journal, sans jamais réécrire ce qui précède.

    ① RÔLE — Tenir le journal « append-only » : on ajoute, on ne réécrit jamais.
    ② CONTEXTE D'APPEL — `main`, pour `--capture`, `--agent` et `--remise`, après validation de la ligne.
    ③ ENTRÉE — `chemin` : le journal · `ligne` : un dictionnaire dont les clés sont COLONNES.
    ④ CONDITIONS D'ENTRÉE — Si le journal existe, son en-tête a été vérifié par `lire_journal`. S'il n'est pas vide, il
      finit par un saut de ligne ; sinon ValueError, et rien n'est écrit.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Lire le dernier octet du journal et refuser s'il n'est pas un saut de ligne ; ouvrir en AJOUT ;
      écrire l'en-tête si le fichier est vide ou neuf ; écrire la ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un journal qu'on réécrit perd ce qu'il prouve (A-804 : « un programme tient un journal »). F-3 de
      Cowork (15-11-2026) : sans saut de ligne final, la ligne ajoutée se collait à la précédente, le programme disait
      « AJOUTÉ » et la capture était perdue. Refuser plutôt qu'ajouter le saut de ligne en silence : une retouche à la
      main du journal est déjà une anomalie.
    ⑨ CE QUI CLOCHE — Deux ajouts simultanés pourraient s'entremêler ; le Chat est seul à écrire.
    ⑩ EFFET — ÉCRIT une ligne (et l'en-tête s'il manquait) en fin de fichier.
    ⑪ TERMINAISON — Rend la main, ou lève OSError ou ValueError.
      [sort: non]
    """
    neuf = not os.path.exists(chemin) or os.path.getsize(chemin) == 0
    if not neuf:
        with open(chemin, "rb") as f:
            f.seek(-1, os.SEEK_END)
            if f.read(1) != b"\n":
                raise ValueError(f"journal retouché : sa dernière ligne n'a pas de fin ({chemin})")
    with open(chemin, "a", encoding="utf-8", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=COLONNES)
        if neuf:
            ecrivain.writeheader()
        ecrivain.writerow({c: ligne.get(c, "") for c in COLONNES})


def trou_mesure(passees, age_max):
    """Mesure, sur les captures du journal, une borne BASSE de ce qui peut se consommer pendant l'âge maximal.

    ① RÔLE — Dire, à chaque `--etat`, si la marge d'alerte couvre le trou de la fenêtre d'âge : un agent non inscrit
      pendant qu'une capture est encore « fraîche » (au plus `age_max` heures) n'est vu par la jauge projetée qu'à
      travers le rythme de pointe × âge (A-827) ; cette mesure reste affichée pour information.
    ② CONTEXTE D'APPEL — `etat`, une fois par appel.
    ③ ENTRÉE — `passees` : les couples (rang dans le fichier, ligne) des lignes antérieures ou égales à maintenant ·
      `age_max` : l'âge maximal d'une capture, en heures.
    ④ CONDITIONS D'ENTRÉE — Les lignes viennent de `lire_journal` (instants lus, valeurs vérifiées).
    ⑤ SORTIE — UNE valeur, None, si aucune paire ne sert ; sinon QUATRE valeurs : les points (borne basse), la capture
      de début et la capture de fin de la paire qui la donne, et un booléen vrai si cette paire est dans la période
      EN COURS (P-2 de Cowork : la ligne TROU ne dit pas la même chose selon la période).
      [rend: 1 ou 4]
    ⑥ TRAITEMENT — ① ranger les lignes par (instant, rang) et numéroter les périodes : chaque remise en ouvre une, et
      une ligne de même heure qu'une remise mais placée avant elle reste dans la période d'avant (même règle que
      `etat`) · ② écarter toute période où une capture est plus basse que la précédente (ANOMALIE : G-6 de Cowork,
      15-11-2026 — 96, 9,6, 97 donnait « au moins 87,4 points » mesurés depuis la valeur fautive) · ③ pour CHAQUE
      paire de captures (a avant b) d'une même période restante : la durée de la paire se couvre par
      n = plafond(durée ÷ âge maximal) fenêtres d'âge (au moins une), dont l'une a reçu au moins (b − a) ÷ n points
      — c'est la borne de la paire ; un trou de durée nulle compte en une fenêtre · ④ rendre la plus grande de ces
      bornes, la paire qui la donne, et si elle est dans la dernière période.
    ⑦ UNITÉ — Points de jauge ; heures.
    ⑧ POURQUOI — G-1 de Cowork (15-11-2026) : le ⑨ ⑥ du programme et le réglage justifiaient l'âge maximal de 2 h par
      « 2,14 points/h × 2 h = 4,3 points < marge de 10 » ; 2,14 était une MOYENNE sur 11,7 h (75 % à 11h03, épuisement
      vers 22h45 le 14-11), donc une borne basse de la pointe prise pour une borne haute. Le 15-11, 10 % à 14h16 puis
      17 % à 15h27 ont donné 5,9 points/h. Le calcul est désormais fait par le programme sur le journal, et non plus
      écrit à la main (R-728 : ce qui se calcule ne s'écrit pas à la main ; R-754). G-5 de Cowork (15-11-2026) :
      l'ancienne borne (b − a) × âge ÷ durée était une extrapolation, pas une borne — 0 %, 10 %, 17 % sur 3,22 h
      affichait 10,6 points, alors que 8,5 points au début et 8,5 à la fin laissent toute fenêtre de 2 h à 8,5.
    ⑨ CE QUI CLOCHE — C'est une borne BASSE : la consommation entre deux captures n'est pas connue, et une pointe plus
      forte que ce que les captures montrent reste possible. Une borne au-dessous de la marge ne PROUVE donc pas que la
      marge couvre le trou ; une borne au-dessus prouve qu'elle ne le couvre pas. La ligne d'épuisement du 14-11
      (100 % vers 22h45, heure approchée) compte comme une capture.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    periode, caps = 0, []
    for i, l in sorted(passees, key=lambda x: (x[1]["t"], x[0])):
        if l["type"] == "remise":
            periode += 1
        elif l["type"] == "capture":
            caps.append((periode, l))
    en_anomalie = {pb for (pa, a), (pb, b) in zip(caps, caps[1:])
                   if pa == pb and float(b["valeur"]) < float(a["valeur"])}
    meilleur = None
    for k, (pa, a) in enumerate(caps):
        if pa in en_anomalie:
            continue
        for pb, b in caps[k + 1:]:
            if pb != pa:
                continue
            points = float(b["valeur"]) - float(a["valeur"])
            fenetres = max(1, math.ceil(heures(a["t"], b["t"]) / age_max))
            borne = points / fenetres
            if meilleur is None or borne > meilleur[0]:
                meilleur = (borne, a, b, pa == periode)
    return meilleur


def rythme_pointe(caps, duree_min):
    """Rend le plus fort rythme mesuré entre deux captures qui montent, et la paire qui le donne.

    ① RÔLE — Donner à la jauge projetée le rythme le plus fort que les captures de la période ont montré, pour
      prolonger la dernière capture jusqu'à l'instant présent sans sous-estimer (convention pessimiste, A-827).
    ② CONTEXTE D'APPEL — `etat`, une fois par appel, quand la période a au moins deux captures et aucune ANOMALIE.
    ③ ENTRÉE — `caps` : les captures de la période en cours, rangées dans l'ordre du temps · `duree_min` : la durée
      minimale d'une paire, en heures (réglage `duree_min_d_une_paire`).
    ④ CONDITIONS D'ENTRÉE — Les lignes viennent de `lire_journal` (instants lus, valeurs vérifiées) ; `duree_min` ≥ 0.
    ⑤ SORTIE — TROIS valeurs : le rythme de pointe (points de jauge par heure), la capture de début et la capture de
      fin de la paire qui le donne ; les trois valent None si aucune paire ne monte avec du temps écoulé.
      [rend: 3]
    ⑥ TRAITEMENT — Pour chaque capture b (à partir de la deuxième), sa paire part de la capture a la PLUS RÉCENTE
      parmi celles d'avant qui précède b d'au moins `duree_min` heures ; avec `duree_min` = 0, c'est la capture
      juste avant (la règle du 15-11-2026, paires consécutives). Retenir (b − a) ÷ heures entre elles si la jauge
      monte (b > a) et si du temps a passé ; rendre le plus grand.
    ⑦ UNITÉ — Points de jauge par heure ; heures réelles (`heures`, en UTC).
    ⑧ POURQUOI — Superviseur R-759 du 15-11-2026 à 16h42 (SUPERVISEUR_FORF_G1_Dim_15-11-2026.md), choix « 1 » de
      Jean-Luc à 16h41 (A-827) : « rythme de pointe = le plus fort rythme mesuré entre deux captures consécutives
      croissantes de la période (pas seulement les deux dernières) ». Une MOYENNE prise pour une pointe a déjà trompé
      le calcul (G-1 de Cowork : 2,14 points/h sur 11,7 h, alors que 5,9 points/h ont été mesurés le 15-11).
    ⑨ CE QUI CLOCHE — Le rythme entre deux captures est lui-même une moyenne sur leur écart : une pointe plus brève et
      plus forte que toute paire capturée n'est pas vue. Deux captures très proches (quelques minutes) donnent une
      pointe démesurée par l'arrondi de la jauge au point près, qui reste la pointe jusqu'à la remise (P-1 et K-2 de
      Cowork, 15-11-2026 : 50 % à 10h00 et 51 % à 10h01 donnent 60 points/h, puis ARRÊTER à 11h00 pour une
      consommation de 2,5 points/h) ; tant que `duree_min_d_une_paire` vaut 0, ce défaut reste entier : la valeur
      est une décision de Jean-Luc.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    meilleur = (None, None, None)
    for k in range(1, len(caps)):
        b = caps[k]
        a = next((caps[j] for j in range(k - 1, -1, -1) if heures(caps[j]["t"], b["t"]) >= duree_min), None)
        if a is None:
            continue
        points = float(b["valeur"]) - float(a["valeur"])
        h = heures(a["t"], b["t"])
        if points <= 0 or h <= 0:
            continue
        if meilleur[0] is None or points / h > meilleur[0]:
            meilleur = (points / h, a, b)
    return meilleur


def etat(lignes, seuil, marge, age_max, duree_min, maintenant):
    """Calcule l'état du forfait à un instant donné.

    ① RÔLE — Faire, sur les lignes du journal, le calcul que le Chat faisait de tête, et rendre INCONNU partout où les
      données ne suffisent pas.
    ② CONTEXTE D'APPEL — `main`, pour `--etat` ; les épreuves l'appellent par la ligne de commande.
    ③ ENTRÉE — `lignes` : rendues par `lire_journal` · `seuil`, `marge`, `age_max` et `duree_min` : rendus par
      `lire_reglages` ·
      `maintenant` : l'instant du calcul (Paris).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire ; chaque grandeur vaut None quand elle est INCONNUE, et sa clé
      `pourquoi_…` dit pourquoi.
      [rend: 1]
    ⑥ TRAITEMENT — ① écarter les lignes postérieures à `maintenant` · ② la période en cours commence à la dernière
      remise antérieure ou égale à `maintenant` ; une ligne de même heure que la remise mais placée AVANT elle dans le
      fichier reste dans la période précédente · ③ captures de la période dans l'ordre du temps ; une capture plus
      basse que la précédente est une ANOMALIE · ④ rythme = écart des deux dernières captures ÷ heures entre elles ;
      rythme de pointe = `rythme_pointe` (paires d'au moins `duree_min` heures) · ⑤ rapport = jetons des agents finis entre la première et la dernière
      capture ÷ points gagnés entre elles · ⑥ JAUGE PROJETÉE = dernière capture + le plus grand de (jetons des agents
      finis depuis ÷ rapport) et (rythme de pointe × âge réel de la capture) (A-827) ; rythme de pointe inconnu :
      jauge INCONNUE ; rapport inconnu : jauge INCONNUE, même
      sans agent inscrit depuis — mais si la capture a au plus `age_max` heures et que le rythme de pointe est
      connu, la jauge vaut AU MOINS dernière capture + rythme de pointe × âge (le terme des jetons, inconnu, est
      positif ou nul) ; de même rapport connu et rythme de pointe INCONNU (aucune paire, ou paire écartée par
      `duree_min` : R-1 de Cowork, 25-11-2026 : 70 % puis 75 % en 10 min, 240 000 jetons ensuite à 20 000 jetons par
      point = au moins 87 %, et la durée minimale 0,5 h rendait INCONNU) : la jauge vaut AU MOINS dernière capture +
      jetons inscrits ÷ rapport (le terme du rythme, inconnu, est positif ou nul) ; cette BORNE BASSE peut faire ALERTER ou ARRÊTER, jamais CONTINUER (K-1 de Cowork, 15-11-2026 :
      60, 72, 88 % sans agent inscrit rendaient ALERTER à 11h55, et ARRÊTER avec un agent ; A-827 : « le programme
      estime la jauge à l'instant présent en prolongeant le dernier rythme mesuré, et alerte sur cette estimation ») — (le Chat consomme aussi, et un agent peut ne pas avoir été inscrit : c'est l'erreur
      du 14-11, une capture de 75 % prolongée sans rien compter), la plus haute capture de la période restant un
      PLANCHER (la jauge ne baisse pas sans remise ; G-4 de Cowork, 15-11-2026 : sous une ANOMALIE, 96 % puis 9,6 %
      gardaient 9,6) ; une dernière capture plus vieille que `age_max` heures est une donnée qui manque :
      jauge INCONNUE, plancher gardé, « demander une capture » · ⑥bis trou de la fenêtre d'âge mesuré par
      `trou_mesure` et confronté à la marge, pour information, sans effet sur le verdict · ⑦ projection = jauge +
      rythme × heures jusqu'à la prochaine remise · ⑧ heure du seuil = maintenant + (seuil − jauge) ÷ rythme ·
      ⑨ verdict sur la jauge projetée si elle est connue ; sinon sur la borne basse si elle est connue, sinon sur
      le plancher, s'ils suffisent à alerter ou arrêter ; sinon INCONNU. Le « plus grand de la jauge et du plancher »
      écrit ici avant le 25-11-2026 ne changeait jamais rien (P-3 de Cowork) : la jauge n'est connue que sans
      ANOMALIE, où le plancher est la dernière capture, que la jauge dépasse ou égale par construction ; de même
      pour la borne basse.
    ⑦ UNITÉ — Points de jauge, points par heure, jetons par point, heures.
    ⑧ POURQUOI — A-799 : extrapoler depuis une seule capture sans compter les agents a laissé le forfait s'épuiser.
      F-1 de Cowork (15-11-2026) : rapport connu, capture de 10h00, aucun agent inscrit → CONTINUER à 16h00, l'erreur
      même du 14-11. Le superviseur R-759 a retenu la seule règle qui aurait agi le 14-11 : l'âge maximal. Superviseur
      R-759 du 15-11-2026 à 16h42 : avec une capture de 80 % à 10h00 et 6 points/h mesurés, le programme rendait
      CONTINUER à 11h55 alors que la jauge valait 80 + 6 × 1,92 = 91,5 % ; d'où la jauge projetée (A-827).
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme : la consommation propre du Chat n'est pas comptée en jetons ; elle
      n'entre dans la jauge projetée que par le rythme de pointe × âge, et une pointe non capturée n'est pas vue. Une
      durée minimale non nulle écarte les paires courtes, donc aussi les vraies pointes brèves (C-1 de Cowork,
      25-11-2026 : sur 20 000 journaux tirés au hasard, 1 197 verdicts moins stricts à 0,5 h qu'à 0, dont une part
      voulue — les pointes démesurées d'arrondi) ; la valeur reste une décision de Jean-Luc. La
      projection à la remise et l'heure du seuil prolongent la jauge projetée au rythme des deux DERNIÈRES captures,
      pas au rythme de pointe (A-827 ne porte que sur le verdict) : l'affichage le dit sur leurs lignes (H-3 de
      Cowork, 15-11-2026 : « jamais au rythme mesuré » à côté d'une jauge qui monte au rythme de pointe trompait).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    e = {"seuil": seuil, "marge": marge, "age_max": age_max, "maintenant": maintenant, "ignorees": 0,
         "anomalie": None, "age": None}
    passees = []
    for i, l in enumerate(lignes):
        if l["t"] > maintenant:
            e["ignorees"] += 1
        else:
            passees.append((i, l))
    remises = [(i, l) for i, l in passees if l["type"] == "remise"]
    if remises:
        i0, r0 = max(remises, key=lambda x: (x[1]["t"], x[0]))
        debut = r0["t"]
        e["remise"], e["prochaine"] = r0["t"], r0["t_prochaine"]
        periode = [l for i, l in passees if l["type"] != "remise" and (l["t"] > debut or (l["t"] == debut and i > i0))]
    else:
        e["remise"], e["prochaine"] = None, None
        periode = [l for i, l in passees if l["type"] != "remise"]
    caps = sorted((l for l in periode if l["type"] == "capture"), key=lambda l: l["t"])
    agents = [l for l in periode if l["type"] == "agent"]
    e["captures"] = caps
    e["derniere"] = caps[-1] if caps else None
    for a, b in zip(caps, caps[1:]):
        if float(b["valeur"]) < float(a["valeur"]):
            e["anomalie"] = (f"la jauge baisse de {a['valeur']} % ({a['horodatage_paris']}) à {b['valeur']} % "
                             f"({b['horodatage_paris']}) sans remise inscrite entre les deux")
    # rythme réel, entre les deux dernières captures
    e["rythme"], e["pourquoi_rythme"] = None, None
    if len(caps) < 2:
        e["pourquoi_rythme"] = f"il faut deux captures dans la période, il y en a {len(caps)}"
    elif e["anomalie"]:
        e["pourquoi_rythme"] = "ANOMALIE : " + e["anomalie"]
    else:
        h = heures(caps[-2]["t"], caps[-1]["t"])
        if h <= 0:
            e["pourquoi_rythme"] = "les deux dernières captures portent la même heure"
        else:
            e["rythme"] = (float(caps[-1]["valeur"]) - float(caps[-2]["valeur"])) / h
    # rythme de pointe, entre deux captures consécutives qui montent (A-827)
    e["pointe"], e["pointe_de"], e["pointe_a"], e["pourquoi_pointe"] = None, None, None, None
    if len(caps) < 2:
        e["pourquoi_pointe"] = f"il faut deux captures dans la période, il y en a {len(caps)}"
    elif e["anomalie"]:
        e["pourquoi_pointe"] = "ANOMALIE : " + e["anomalie"]
    else:
        e["pointe"], e["pointe_de"], e["pointe_a"] = rythme_pointe(caps, duree_min)
        if e["pointe"] is None:
            e["pourquoi_pointe"] = "aucune paire de captures consécutives qui monte avec du temps écoulé"
            if duree_min > 0 and rythme_pointe(caps, 0)[0] is not None:
                e["pourquoi_pointe"] = (f"une paire de captures qui monte existe, mais elle dure moins de "
                                        f"{duree_min:g} h (réglage duree_min_d_une_paire) : écartée")
    # rapport jetons par point, calé entre la première et la dernière capture de la période
    e["rapport"], e["pourquoi_rapport"] = None, None
    if len(caps) < 2:
        e["pourquoi_rapport"] = f"il faut deux captures dans la période, il y en a {len(caps)}"
    elif e["anomalie"]:
        e["pourquoi_rapport"] = "ANOMALIE : " + e["anomalie"]
    else:
        points = float(caps[-1]["valeur"]) - float(caps[0]["valeur"])
        jetons = sum(int(a["valeur"]) for a in agents if caps[0]["t"] < a["t"] <= caps[-1]["t"])
        e["jetons_calage"], e["points_calage"] = jetons, points
        if points <= 0:
            e["pourquoi_rapport"] = "aucun point gagné entre la première et la dernière capture"
        elif jetons <= 0:
            e["pourquoi_rapport"] = "aucun agent inscrit entre la première et la dernière capture"
        else:
            e["rapport"] = jetons / points
    # jauge projetée maintenant (A-827)
    e["jauge"], e["pourquoi_jauge"], e["plancher"], e["borne"] = None, None, None, None
    e["terme_jetons"], e["terme_rythme"], e["borne_de"] = None, None, None
    if not caps:
        e["pourquoi_jauge"] = "aucune capture dans la période"
        e["jetons_depuis"], e["agents_depuis"] = 0, 0
    else:
        der = caps[-1]
        depuis = [a for a in agents if a["t"] > der["t"]]
        e["jetons_depuis"], e["agents_depuis"] = sum(int(a["valeur"]) for a in depuis), len(depuis)
        e["plancher"] = max(float(c["valeur"]) for c in caps)
        e["age"] = heures(der["t"], maintenant)
        if e["age"] > age_max:
            e["pourquoi_jauge"] = (f"capture vieille de {e['age']:.1f} h (âge maximal {age_max:g} h) : "
                                   "demander une capture")
        elif e["rapport"] is None:
            e["pourquoi_jauge"] = ("le rapport jetons par point est inconnu — la dernière capture ne dit rien de "
                                   "ce qui a été consommé depuis")
            if e["pointe"] is not None:
                e["terme_rythme"] = e["pointe"] * e["age"]
                e["borne"] = float(der["valeur"]) + e["terme_rythme"]
                e["borne_de"] = "rythme"
        elif e["pointe"] is None:
            e["pourquoi_jauge"] = ("le rythme de pointe est inconnu — " + e["pourquoi_pointe"])
            e["terme_jetons"] = e["jetons_depuis"] / e["rapport"]
            e["borne"] = float(der["valeur"]) + e["terme_jetons"]
            e["borne_de"] = "jetons"
        else:
            e["terme_jetons"] = e["jetons_depuis"] / e["rapport"]
            e["terme_rythme"] = e["pointe"] * e["age"]
            e["jauge"] = float(der["valeur"]) + max(e["terme_jetons"], e["terme_rythme"])
    # trou de la fenêtre d'âge, confronté à la marge, pour information (G-1 de Cowork, 15-11-2026)
    e["trou"] = trou_mesure(passees, age_max)
    e["trou_couvert"] = None if e["trou"] is None else e["trou"][0] < marge
    # projection à la remise et heure du seuil
    e["projection"], e["pourquoi_projection"] = None, None
    if e["prochaine"] is None:
        e["pourquoi_projection"] = "aucune remise inscrite au journal : la prochaine est inconnue"
    elif e["prochaine"] <= maintenant:
        e["pourquoi_projection"] = "la remise prévue est passée : inscrire la nouvelle par --remise"
    elif e["jauge"] is None or e["rythme"] is None:
        e["pourquoi_projection"] = "jauge ou rythme inconnu"
    else:
        h = heures(maintenant, e["prochaine"])
        e["projection"] = e["jauge"] + e["rythme"] * h
    e["heure_seuil"], e["texte_seuil"] = None, None
    if e["jauge"] is not None and e["jauge"] >= seuil:
        e["texte_seuil"] = "déjà atteint"
    elif e["jauge"] is None or e["rythme"] is None:
        e["texte_seuil"] = "INCONNUE — jauge ou rythme inconnu"
    elif e["rythme"] <= 0:
        e["texte_seuil"] = "jamais au rythme mesuré (rythme nul)"
    else:
        e["heure_seuil"] = (maintenant.astimezone(timezone.utc)
                            + timedelta(hours=(seuil - e["jauge"]) / e["rythme"])).astimezone(PARIS)
        apres = e["prochaine"] is not None and e["heure_seuil"] >= e["prochaine"]
        e["texte_seuil"] = (e["heure_seuil"].strftime("%Y-%m-%d %H:%M")
                            + (" — après la prochaine remise : non atteint d'ici là" if apres else ""))
    # verdict : sur la jauge projetée ; à défaut, sur la borne basse ou le plancher s'ils suffisent ; sinon INCONNU
    base = next((x for x in (e["jauge"], e["borne"], e["plancher"]) if x is not None), None)
    if base is not None and base >= seuil:
        e["verdict"] = "ARRÊTER LES NOUVEAUX AGENTS"
    elif base is not None and base >= seuil - marge:
        e["verdict"] = "ALERTER"
    elif e["jauge"] is not None:
        e["verdict"] = "CONTINUER"
    else:
        e["verdict"] = "INCONNU"
    e["sur_le_plancher"] = e["jauge"] is None and e["borne"] is None and e["verdict"] != "INCONNU"
    e["sur_la_borne"] = e["jauge"] is None and e["borne"] is not None and e["verdict"] != "INCONNU"
    return e


def afficher(e, chemin_reglages):
    """Affiche l'état du forfait, une grandeur par ligne, INCONNU dit avec sa raison.

    ① RÔLE — Rendre lisible, en français, ce que `etat` a calculé.
    ② CONTEXTE D'APPEL — `main`, pour `--etat`.
    ③ ENTRÉE — `e` : le dictionnaire rendu par `etat` · `chemin_reglages` : le fichier d'où viennent seuil et marge.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; affiche.
      [rend: rien]
    ⑥ TRAITEMENT — Une ligne par grandeur, dans l'ordre de la demande, puis le VERDICT ; sous un verdict INCONNU, la
      règle que le Chat applique, en clair.
    ⑦ UNITÉ — % et points de jauge, points par heure, jetons par point, heures de Paris.
    ⑧ POURQUOI — Le Chat recopie ces lignes à Jean-Luc ; un chiffre sans sa raison d'être inconnu se lit comme sûr.
      La règle sous INCONNU vient du superviseur R-759 du 15-11-2026 (« le verdict INCONNU vaut pas de nouvel
      agent ») ; Jean-Luc l'a décidée le 15-11-2026 à 14h14 (A-810, réponse « 1 »).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    f = lambda t: t.strftime("%Y-%m-%d %H:%M") if t else "—"
    s, m = e["seuil"], e["marge"]
    print(f"ÉTAT DU FORFAIT — maintenant {f(e['maintenant'])} (Paris) · seuil {s:g} % · alerte dès {s - m:g} % "
          f"· âge maximal d'une capture {e['age_max']:g} h (réglages : {os.path.relpath(chemin_reglages, RACINE)})")
    if e["ignorees"]:
        print(f"LIGNES POSTÉRIEURES À MAINTENANT, IGNORÉES : {e['ignorees']}")
    print(f"PÉRIODE : depuis la remise du {f(e['remise'])} · prochaine remise {f(e['prochaine'])}"
          if e["remise"] else "PÉRIODE : aucune remise inscrite — tout le journal forme une seule période")
    if e["anomalie"]:
        print("ANOMALIE : " + e["anomalie"])
    d = e["derniere"]
    print(f"CAPTURES DE LA PÉRIODE : {len(e['captures'])}"
          + (f" · dernière {d['valeur']} % le {d['horodatage_paris'].replace('T', ' ')} ({d['source']}), "
             f"vieille de {e['age']:.1f} h" if d else ""))
    print(f"RYTHME RÉEL : {e['rythme']:.2f} points/h (entre les deux dernières captures)" if e["rythme"] is not None
          else f"RYTHME RÉEL : INCONNU — {e['pourquoi_rythme']}")
    print(f"RYTHME DE POINTE : {e['pointe']:.2f} points/h (de {e['pointe_de']['valeur']} % le "
          f"{e['pointe_de']['horodatage_paris'].replace('T', ' ')} à {e['pointe_a']['valeur']} % le "
          f"{e['pointe_a']['horodatage_paris'].replace('T', ' ')})" if e["pointe"] is not None
          else f"RYTHME DE POINTE : INCONNU — {e['pourquoi_pointe']}")
    print(f"RAPPORT JETONS PAR POINT : {e['rapport']:.0f} ({e['jetons_calage']} jetons ÷ {e['points_calage']:g} points)"
          if e["rapport"] is not None else f"RAPPORT JETONS PAR POINT : INCONNU — {e['pourquoi_rapport']}")
    print(f"JETONS D'AGENTS DEPUIS LA DERNIÈRE CAPTURE : {e['jetons_depuis']} ({e['agents_depuis']} agent(s))")
    if e["jauge"] is not None:
        print(f"JAUGE PROJETÉE MAINTENANT : {e['jauge']:.1f} % (dernière capture {d['valeur']} % + le plus grand de : "
              f"jetons inscrits ÷ rapport = {e['terme_jetons']:.1f} points ; rythme de pointe {e['pointe']:.2f} × âge "
              f"{e['age']:.2f} h = {e['terme_rythme']:.1f} points)"
              + (" — au-delà de 100 : la jauge réelle s'arrête à 100, l'épuisement est probable"
                 if e["jauge"] > 100 else ""))
    else:
        if e["borne_de"] == "jetons":
            detail = (f"dernière capture {d['valeur']} % + jetons inscrits ÷ rapport = {e['terme_jetons']:.1f} points, "
                      "rythme de pointe non compté")
        elif e["borne_de"] == "rythme":
            detail = (f"dernière capture {d['valeur']} % + rythme de pointe {e['pointe']:.2f} × âge {e['age']:.2f} h = "
                      f"{e['terme_rythme']:.1f} points, jetons non comptés")
        print(f"JAUGE PROJETÉE MAINTENANT : INCONNUE — {e['pourquoi_jauge']}"
              + (f" ; AU MOINS {e['borne']:.1f} % ({detail})"
                 + (" — au-delà de 100 : l'épuisement est probable" if e["borne"] > 100 else "")
                 if e["borne"] is not None else "")
              + (f" ; plancher {e['plancher']:g} % (plus haute capture de la période)"
                 if e["plancher"] is not None else ""))
    rr = " [au rythme réel des deux dernières captures ; le verdict, lui, compte le rythme de pointe]"
    print(f"PROJECTION À LA REMISE : {e['projection']:.1f} %"
          + (" — au-delà de 100 : épuisement avant la remise" if e["projection"] > 100 else "") + rr
          if e["projection"] is not None else f"PROJECTION À LA REMISE : INCONNUE — {e['pourquoi_projection']}")
    print(f"SEUIL ATTEINT VERS : {e['texte_seuil']}" + (rr if e["texte_seuil"] != "déjà atteint" else ""))
    if e["trou"] is None:
        print("TROU POSSIBLE PENDANT L'ÂGE MAXIMAL : INCONNU — aucune paire de captures dans une même période "
              "où la jauge ne baisse jamais")
    else:
        b, ca, cb, en_cours = e["trou"]
        avant = ("mesuré AVANT la dernière remise : le verdict ne compte que le rythme de pointe de la période "
                 "en cours, pas ce trou")
        if not e["trou_couvert"]:
            fin = ("NON COUVERT par la marge d'alerte de " + f"{m:g} points : ALERTER peut ne pas sonner avant le seuil "
                   "si la pointe dépasse celle des captures "
                   + (("(information : le verdict compte déjà rythme de pointe × âge, A-827)"
                       if e["terme_rythme"] is not None else
                       "(information : le rythme de pointe est INCONNU, le verdict ne compte donc pas ce trou)"
                       if e["pointe"] is None else
                       "(information : le verdict ne compte pas ce trou — " + str(e["pourquoi_jauge"]) + ")")
                      if en_cours else f"({avant})"))
        else:
            fin = (f"sous la marge d'alerte de {m:g} points, sans le prouver (borne basse : une pointe non capturée "
                   "peut dépasser)" + (f" ; {avant}" if not en_cours else ""))
        print(f"TROU POSSIBLE PENDANT L'ÂGE MAXIMAL : au moins {b:.1f} points en {e['age_max']:g} h (mesuré de "
              f"{ca['valeur']} % le {ca['horodatage_paris'].replace('T', ' ')} à {cb['valeur']} % le "
              f"{cb['horodatage_paris'].replace('T', ' ')}) — " + fin)
    print("VERDICT : " + e["verdict"] + (" (sur le plancher des captures)" if e["sur_le_plancher"] else "")
          + (" (sur la borne basse : dernière capture + " + ("jetons inscrits ÷ rapport" if e["borne_de"] == "jetons"
                                                    else "rythme de pointe × âge") + ")" if e["sur_la_borne"] else ""))
    if e["verdict"] == "INCONNU":
        print("RÈGLE DÉCIDÉE PAR JEAN-LUC (A-810, 15-11-2026 14h14) : INCONNU : pas de nouvel agent avant une "
              "nouvelle capture")


def main(arguments):
    """Lit la ligne de commande, fait l'ajout ou le calcul demandé, et rend le code de sortie.

    ① RÔLE — Point d'entrée : une action par appel.
    ② CONTEXTE D'APPEL — Le bas du fichier, quand il est lancé comme programme.
    ③ ENTRÉE — `arguments` : la ligne de commande sans le nom du programme (voir le ③ du programme).
    ④ CONDITIONS D'ENTRÉE — Une seule action parmi `--capture`, `--agent`, `--remise`, `--etat`.
    ⑤ SORTIE — UNE valeur : le code de sortie (voir le ⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les options · ② vérifier le journal existant (en-tête, heures) · ③ pour un ajout : valider
      la valeur et l'heure, ajouter, afficher la ligne · ④ pour `--etat` : lire les réglages, calculer, afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une erreur d'entrée se dit et rend 2, sans rien écrire (R-734).
    ⑨ CE QUI CLOCHE — `--a` est libre : une capture peut être datée dans le futur ; `--etat` l'ignore alors tant que
      son heure n'est pas venue, et le dit.
    ⑩ EFFET — Écrit une ligne au journal pour un ajout ; affiche.
    ⑪ TERMINAISON — Rend la main avec le code. Un de ses appels peut ne pas revenir : argparse sort lui-même
      (code 2) sur une option mal écrite.
      [sort: non]
    """
    p = argparse.ArgumentParser(prog="TENIR_LE_FORFAIT.py", description="Journal et verdict du forfait.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--capture", metavar="POURCENT")
    g.add_argument("--agent", nargs=2, metavar=("ETIQUETTE", "JETONS"))
    g.add_argument("--remise", metavar="PROCHAINE")
    g.add_argument("--etat", action="store_true")
    p.add_argument("--a", dest="quand")
    p.add_argument("--source", default="capture de Jean-Luc")
    p.add_argument("--maintenant")
    p.add_argument("--journal", default=JOURNAL_PAR_DEFAUT)
    p.add_argument("--reglages", default=REGLAGES_PAR_DEFAUT)
    o = p.parse_args(arguments)
    horloge = datetime.now(PARIS).replace(second=0, microsecond=0)
    try:
        lignes = lire_journal(o.journal)
        maintenant = lire_horodatage(o.maintenant) if o.maintenant else horloge
        quand = lire_horodatage(o.quand) if o.quand else horloge
    except (OSError, ValueError) as x:
        print(f"ERREUR : {x}")
        return 2
    if o.etat:
        try:
            seuil, marge, age_max, duree_min = lire_reglages(o.reglages)
        except (OSError, ValueError) as x:
            print(f"ERREUR RÉGLAGE ILLISIBLE — aucun verdict : {x}")
            return 2
        e = etat(lignes, seuil, marge, age_max, duree_min, maintenant)
        afficher(e, o.reglages)
        return {"CONTINUER": 0, "ALERTER": 3, "ARRÊTER LES NOUVEAUX AGENTS": 4}.get(e["verdict"], 5)
    ligne = {"horodatage_paris": quand.strftime(FORMAT), "inscrit_le_paris": horloge.strftime(FORMAT)}
    try:
        if o.capture is not None:
            v = float(o.capture.replace(",", "."))
            if not 0 <= v <= 100:
                raise ValueError(f"pourcentage hors de 0-100 : {o.capture}")
            if not o.quand:
                raise ValueError("une capture porte l'heure de la jauge : --a AAAA-MM-JJTHH:MM est obligatoire")
            if "\n" in o.source or "," in o.source:
                raise ValueError("la source ne porte ni virgule ni saut de ligne")
            ligne.update(type="capture", valeur=f"{v:g}", source=o.source)
        elif o.agent is not None:
            etiquette, jetons = o.agent
            if not etiquette.strip() or "," in etiquette or "\n" in etiquette:
                raise ValueError("étiquette vide, ou avec virgule ou saut de ligne")
            if not (jetons.isascii() and jetons.isdigit()):
                raise ValueError(f"jetons : un entier positif ou nul est attendu, pas « {jetons} »")
            ligne.update(type="agent", valeur=str(int(jetons)), etiquette=etiquette.strip(), source="agent fini")
        else:
            prochaine = lire_horodatage(o.remise)
            if prochaine <= quand:
                raise ValueError("la prochaine remise doit venir après celle qui vient d'avoir lieu")
            ligne.update(type="remise", prochaine_remise_paris=prochaine.strftime(FORMAT), source=o.source
                         if o.source != "capture de Jean-Luc" else "remise à zéro")
    except ValueError as x:
        print(f"ERREUR — rien n'est écrit : {x}")
        return 2
    try:
        ajouter(o.journal, ligne)
    except ValueError as x:
        print(f"ERREUR — rien n'est écrit : {x}")
        return 2
    print("AJOUTÉ : " + ",".join(str(ligne.get(c, "")) for c in COLONNES))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
