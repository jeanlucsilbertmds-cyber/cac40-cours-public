#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_LECTURE_DES_COURS — Sam 10-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que le calendrier des séances (programmes/CALENDRIER_DE_LA_BOURSE.py : `lire_les_seances`,
  `etat_du_jour`, `seances_entre`, R-110) et le programme unique de lecture des cours (programmes/LIRE_LES_COURS.py,
  R-111) répondent juste, SUR DES RÉPONSES ÉCRITES À LA MAIN, et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main, avant toute livraison qui touche l'un de ces deux programmes (R-731) :
  python3 tests/EPREUVES_DE_LA_LECTURE_DES_COURS_Sam_10-10-2026.py <racine du dépôt> [--saboter]
  [--seulement=S31,S37] (pour rejouer quelques sabotages ; le jeu entier prend environ neuf minutes)
③ ENTRÉE — La racine du dépôt, qui porte les vrais fichiers : donnees/cours_maitre.csv,
  donnees/sources_yahoo/historique_long_repare.csv, donnees/sources_indice/INDICE_CAC40.csv,
  donnees/CALENDRIER_EURONEXT.csv, donnees/REFERENTIEL_VALEURS_*.csv, donnees/NATURE_DES_TROUS.csv.
④ CONDITIONS D'ENTRÉE — Ces fichiers tels qu'au 10-10-2026 : les réponses attendues portent sur eux. Les DEUX que le
  circuit du soir réécrit chaque soir — donnees/cours_maitre.csv et donnees/claude_cours_nouveaux.csv — ne sont plus lus
  dans le dépôt : l'épreuve les prend dans leurs témoins figés (FIGES, plus bas), sur une copie des données.
⑤ SORTIE — UNE valeur : le code de sortie — 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au
  moins une épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus, ou si une épreuve est tombée sur une panne de
  l'environnement (PANNES : disque plein…), qui ne juge rien.
  [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis pour chaque sabotage : copier les quatre programmes dans un dossier jetable, y appliquer
  le sabotage, importer la lecture des cours copiée, jouer les épreuves L1 à L31.
⑦ UNITÉ — Des séances et des dates.
⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026, « Oui, vas-y » : construire le calendrier et le module. R-731 : tout
  code passe des épreuves sabotées ; un cas au moins vient d'une vraie ligne (R-732).
  LES ÉPREUVES :
  L1 ÉTALON : privé de ses lignes des cinq demi-séances, l'historique réparé a pour trous de tout le marché exactement
     24-12-2010, 31-12-2010, 24-12-2012, 31-12-2012, 31-12-2015 (mesure de Cowork rapportée en R-110 ①) ; tel quel, il
     n'en a plus aucun : elles sont comblées depuis bnains depuis le 27-10-2026 (A-555 (b)) ;
  L2 sur l'historique réparé, hors trous de tout le marché, Bouygues (EN) a exactement six trous, du 03 au 10-11-2011
     (03, 04, 07, 08, 09, 10), et AXA (CS) vingt, du 13-10-2000 au 30-04-2007 (table de réception, ligne A1) ;
  L3 sur le fichier maître : Air Liquide (AI) a 709 barres, écrites « AIR LIQUIDE » 644 fois et « AIR_LIQUIDE » 65 ;
     13 valeurs écrites de plusieurs façons ; aucun nom sans mnémonique ;
  L4 une copie du maître sans la séance de Vinci du 03-07-2026 : le seul trou de DG est le 03-07-2026, et ses 14
     dernières séances au 10-07-2026 commencent le 23-06-2026 et portent (03-07-2026, None) ;
  L5 DOIT ÉCHOUER : une ligne « AIR LIQUID » n'est pas réunie à Air Liquide, elle est signalée sans mnémonique ;
  L6 le calendrier : 02-10-2026 CONSTATÉE, 09-10-2026 PRÉVUE, 25-12-2015 FERMÉE, 24-12-2010 CONSTATÉE, 25-12-2026
     FERMÉE, 10-10-2026 FERMÉE ; du 20 au 31-12-2010, dix séances écrites à la main ; 31-12-1999 et 04-01-2027 hors
     du calendrier ;
  L7 les deux alertes du calendrier : indice publié le 03-04-2026 (Euronext : fermé) ; indice absent le 30-09-2026
     (Euronext : séance), et ce jour reste une séance PRÉVUE ;
  L8 les refus de l'indice : en-tête faux, date « 20100105 », date écrite deux fois, un samedi, une ligne sans cours,
     un cours illisible, un cours « inf », un cours « nan », une date après aujourd'hui (lundi 05-01-2099) ; et la
     marque d'ordre d'octets d'Excel en tête de l'indice est tolérée ;
  L9 un doublon identique est gardé une fois et signalé, y compris écrit « 45.390 » au lieu de « 45.39 » ; deux
     versions différentes ne gardent aucune barre et le trou porte « DEUX VERSIONS » ; trois exemplaires A, B, A non
     plus ;
  L10 une barre un jour fermé (01-05-2026), un samedi (03-10-2026), hors du calendrier (31-12-1999 et 04-01-2027) est
     mise à part, et la lecture se poursuit ;
  L11 la nature d'un trou est lue (EN, 03-11-2011, SUSPENSION) ; une nature écrite sur une séance qui a son cours est
     relevée ; les refus : mnémonique inconnu, nature inconnue, preuve vide, qui a décidé vide, date illisible, ligne
     écrite deux fois, un samedi, hors du calendrier ;
  L12 un référentiel où une même écriture désigne deux mnémoniques est refusé ;
  L13 ArcelorMittal (MT), hors univers, n'a aucun trou dans le maître ; une valeur dans l'univers absente des deux
     dernières séances (Accor, 08 et 09-10-2026 retirés) a ces deux trous ;
  L14 lancé seul : 1 sur le maître (13 valeurs à plusieurs écritures, indice arrêté au 02-10-2026), 0 sur un maître
     sans ces doubles écritures avec un indice prolongé au 09-10-2026, 2 sans fichier des cours ;
  L15 `dernieres_seances` avec n = 0 est refusé ;
  L16 une date illisible dans les cours est comptée, pas rangée ;
  L17 CHAQUE sorte de signal, seule, fait rendre 1 à `main` : alerte du calendrier (indice absent le 30-09-2026),
     indice arrêté avant la fin, écritures multiples (une seule ligne « AIR_LIQUIDE »), nom sans mnémonique, date
     illisible, doublon, conflit, barre un jour fermé, nature sur une séance qui a son cours, trou d'une valeur, trou
     de tout le marché ; la base sans rien rend 0 ;
  L18 une valeur de l'univers absente du fichier entier (Vinci retiré) a un trou à chacune des 709 séances, et elle est
     dite ABSENTE ;
  L19 tout le marché absent des deux dernières séances (08 et 09-10-2026 retirés) : deux trous de tout le marché ;
  L20 DOIT ÉCHOUER : une ligne « CA » (abréviation de Crédit Agricole, mnémonique de Carrefour) n'est rangée sous
     aucune valeur ;
  L21 `main` rend 2 pour un fichier des cours mal formé : en-tête faux, case de 200 000 caractères, ligne à neuf cases ;
  L22 un référentiel avec un mnémonique vide est refusé ;
  L23 « jusqu_au » est respecté : lire l'historique réparé jusqu'au 09-10-2026 fait des cinq séances du 05 au
     09-10-2026 des trous de tout le marché, et de rien d'autre depuis le comblement du 27-10-2026 ;
  L24 sans date, la lecture attend les cours jusqu'à la veille, heure de Paris ;
  L25 une liste d'Euronext qui s'arrête dans moins de 30 jours est signalée ; une qui s'arrête en 2099 ne l'est pas ;
  L26 (ajoutée le 11-10-2026, relecture de Cowork e183c98, cassure A) les trois fichiers de cours du dépôt se lisent :
     la référence Google (sept colonnes, sans source) donne 25 116 barres, 39 valeurs, et ses 65 séances absentes du
     13-07 au 09-10-2026 sont des trous de tout le marché (elle s'arrête au 10-07-2026) ; l'arrivée du soir (sept
     colonnes) se lit sans source écrite ; un en-tête à six colonnes est refusé ;
  L27 (ajoutée le 12-10-2026, relecture de Cowork 108efa5, cassure C) lue SANS date, la référence Google, déclarée
     figée, s'arrête au 10-07-2026 et n'a aucun trou de tout le marché ; son contenu exact posé sous le nom du maître ou
     sous autre/cac40_ohlcv.csv, non déclaré, sort au moins 65 trous de tout le marché (figé se déclare, par son chemin,
     il ne se déduit pas) ; amputée de ses dix dernières séances à sa place, elle sort ces dix trous ; le témoin du
     golden est figé sans trou ; l'arrivée du soir n'est pas figée ; allongée d'une séance (13-07-2026), la référence le
     dit (« FICHIER FIGÉ ALLONGÉ ») — un fichier figé ne grandit pas ; la clôture de Vinci du 03-03-2025 augmentée de
     10 % au milieu, elle le dit (« FICHIER FIGÉ MODIFIÉ », un signalement) — un fichier figé ne change pas (relecture
     de Cowork 81998cc, cas 3). L26 (complétée le 12-10-2026, même relecture, cas 1) : lue jusqu'au 09-10-2026, la
     référence n'a plus aucun trou de tout le marché — la demande au-delà de sa fin déclarée est dite (« AU-DELÀ DU
     FICHIER FIGÉ », un seul signalement au lieu de 65 trous) ; et les 14 dernières séances de Vinci au 09-10-2026
     s'arrêtent au 10-07-2026, toutes avec leur barre (relecture indépendante du 12-10-2026 : elles sortaient vides du
     22-09 au 09-10-2026).
  L28 (ajoutée le 12-10-2026, cassure B de Cowork e183c98 ; décision de Jean-Luc A8 et « Oui, clore et passer à B ») :
     dans l'historique réparé, une valeur dans l'indice avant sa première barre a ses trous — Airbus 292 (du 10-07-2000,
     entrée sous EADS, au 31-08-2001), STMicroelectronics 423 (du 03-01-2000 au 31-08-2001), Unibail-Rodamco-Westfield
     4 054 (du 18-06-2007 au 13-04-2023 ; 4 049 avant le 27-10-2026 : ses cinq demi-séances, qui n'étaient pas comptées
     parce qu'elles étaient des trous de tout le marché, le sont depuis qu'elles ne le sont plus), Thales 1 (03-01-2000) ; Stellantis aucun : les années de Peugeot S.A. ne
     lui sont pas prêtées ; ArcelorMittal, hors univers, aucun ; le maître n'a aucun trou avant sa première date ; une
     table des identités où une société a deux noms d'aujourd'hui, ou où deux sociétés ont le même mnémonique, est
     refusée, et l'absence de la table des passages aussi, et un renommage qui laisse une valeur sans passage (STMPA
     écrit STM, ou ses lignes retirées), et un code ISIN rattaché à deux sociétés ; des sociétés sorties (Vivendi, et
     deux codes encore vides) sont admises, et un passage sans code ne leur est pas prêté ; l'incrément déclaré est celui qu'écrit programmes/TENIR_L_HISTORIQUE.py ; un passage fermé après la fin du fichier n'y crée aucun
     trou ; l'arrivée du soir, déclarée incrément, n'attend chaque valeur qu'à partir de sa première barre (relecture
     indépendante du 12-10-2026 : elle sortait 420 « trous » que le maître couvre).
  L29 (ajoutée le 12-10-2026, même relecture) : avec une table où Accor et Vinci sortent de l'indice le 29-12-2023,
     avant la première date du maître, Accor sans ses deux dernières séances a encore ses deux trous, et Vinci absent
     ses 709 — une valeur de l'univers est attendue jusqu'à la fin du fichier, dans l'indice ou non. L12 et L22 lisent
     désormais le MESSAGE du refus, pas seulement son nom.
  L30 (ajoutée le 12-10-2026, cassure G de Cowork 9c882a6) : une table des passages où la sortie d'EADS précède son
     entrée (1999-07-09 contre 2000-07-10) est refusée, avec sa raison — elle faisait disparaître les 292 trous
     d'Airbus sans un mot ; un second passage d'Air Liquide pris dans son passage ouvert, aussi ; un passage à l'envers
     d'une société inconnue des identités, aussi ; deux passages fermés d'Edenred (code inconnu des identités) qui se
     croisent, ou dont l'un entre le jour où l'autre sort, aussi ; une date illisible est dite avec son passage ; la
     vraie table, lignes dans l'ordre inverse, rend les mêmes passages (relecture indépendante du même soir).
  L32 (ajoutée le 27-10-2026) : `lignes_mises_a_part` vaut 0 sur le maître et l'historique réparé, 1 pour une ligne
     d'un nom inconnu, d'une date illisible ou d'un samedi ajoutée au maître, 0 pour un doublon exact ;
  L31 (ajoutée le 13-10-2026, cassure H de Cowork 15e647c) : un code ISIN mal écrit est refusé, avec sa raison — le
     premier passage de STMicroelectronics avec une espace après son code, ou en minuscules (il passait pour une
     société sortie, et les 423 trous disparaissaient) ; le code d'Accor aux identités avec une clé fausse ; la clé
     est calibrée sur Accor, Apple et Stellantis, vraie, et fausse au dernier chiffre changé.
⑨ CE QUI CLOCHE — Les réponses portent sur les fichiers du 10-10-2026. Jusqu'au 15-10-2026, l'épreuve lisait le fichier
  maître du dépôt : chaque versement de nouvelles séances changeait L3 et L18 (709) et L13 (dernières séances), et il
  fallait les réécrire à la main ; le 15-10-2026, avant le versement de l'historique long, 7 épreuves sur 31 étaient
  rouges pour cette seule raison (mesuré : avec le maître et les cours du soir du 13-10-2026 à 11h10, commit b80398b,
  dernier passage vert, les 31 sont vertes). Réparé le 15-10-2026 sur décision de Jean-Luc (« 2 », 08h57 : réparer les
  épreuves rouges avant de verser) : ces deux fichiers sont lus dans leurs témoins figés du 13-10-2026 (FIGES), pris
  au commit b80398b. Reste vrai : les AUTRES fichiers lus (l'historique réparé, l'indice, le calendrier d'Euronext, le
  référentiel, la nature des trous, les deux tables des passages et des identités) sont ceux du dépôt — s'ils changent,
  les réponses sont à revoir. Chaque lecture passe la date du 09-10-2026 (le 02-10-2026 pour l'historique réparé),
  pour que les réponses ne dépendent pas du jour où les épreuves tournent.
⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin ; lance des processus.
⑪ TERMINAISON — Rend la main ; chaque lancement seul est borné à 120 secondes.
  [sort: oui]
"""
import atexit
import contextlib
import csv
import errno
import glob
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT_DONNE = os.path.abspath(_args[0] if _args else ".")
# LES DEUX FICHIERS QUE LE CIRCUIT DU SOIR RÉÉCRIT, FIGÉS (15-10-2026, voir ⑨) : chacun est lu dans son témoin, pris au
# commit b80398b du 13-10-2026 à 11h10, dernier passage vert de ces épreuves ; leur dernière séance est le 09-10-2026
# (la date du nom est celle de la prise, pas celle de la dernière séance). Sans cela, chaque séance versée au maître
# faisait rougir L3, L13 et L18 alors que le code n'avait pas changé. Le maître étant trié par valeur, un témoin n'est
# pas un début du fichier actuel : relecture du 15-10-2026, ses 27 681 lignes sont toutes dans le maître du jour, à
# l'identique (comparées par valeur et date).
FIGES = {
    "donnees/cours_maitre.csv": "temoins/TEMOIN_cours_maitre_JEU_DE_LA_LECTURE_DES_COURS_13-10-2026.csv",
    "donnees/claude_cours_nouveaux.csv": "temoins/TEMOIN_claude_cours_nouveaux_JEU_DE_LA_LECTURE_DES_COURS_13-10-2026.csv",
}


def depot_fige(donne):
    """Rend une copie jetable des données et des programmes du dépôt, où les fichiers de FIGES sont leurs témoins.

    ① RÔLE — Donner aux épreuves des données qui ne bougent pas d'un soir à l'autre.
    ② CONTEXTE D'APPEL — Une fois, au chargement de ce fichier : `DEPOT` désigne ensuite la copie.
    ③ ENTRÉE — `donne` : la racine du dépôt passée sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `donne` porte donnees/, programmes/, le témoin du golden et les témoins de FIGES.
    ⑤ SORTIE — UNE valeur : le chemin de la copie.
      [rend: 1]
    ⑥ TRAITEMENT — ① copier donnees/ et programmes/ (sans les fichiers compilés) et le témoin du golden ·
      ② refuser si un témoin de FIGES manque · ③ poser chaque témoin à la place de son fichier · ④ faire effacer la
      copie à la fin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les réponses écrites à la main portent sur des fichiers datés ; un fichier qui grandit chaque soir les
      rend fausses sans que le code change (voir ⑨ du fichier). Copier, et non lire ailleurs : les programmes éprouvés
      lisent les chemins habituels sous la racine qu'on leur donne.
    ⑨ CE QUI CLOCHE — Un fichier lu par les épreuves hors de donnees/, programmes/ et du témoin du golden manquerait à la
      copie : l'épreuve qui le lit tomberait (rouge), elle ne se tairait pas.
    ⑩ EFFET — Écrit une copie d'environ 70 Mo dans le dossier temporaire ; l'efface à la sortie.
    ⑪ TERMINAISON — Rend la main, ou lève SystemExit (code 2) si un témoin manque.
      [sort: oui]
    """
    copie = tempfile.mkdtemp(prefix="lecture_figee_")
    atexit.register(shutil.rmtree, copie, True)
    sans = shutil.ignore_patterns("__pycache__", "*.pyc")
    for d in ("donnees", "programmes"):
        shutil.copytree(os.path.join(donne, d), os.path.join(copie, d), ignore=sans)
    golden = "temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv"
    os.makedirs(os.path.join(copie, "temoins"))
    shutil.copy(os.path.join(donne, golden), os.path.join(copie, golden))
    for fichier, temoin in FIGES.items():
        if not os.path.isfile(os.path.join(donne, temoin)):
            print(f"ARRÊT : témoin figé introuvable : {temoin}")
            sys.exit(2)
        shutil.copy(os.path.join(donne, temoin), os.path.join(copie, fichier))
    return copie


DEPOT = depot_fige(DEPOT_DONNE)
D = date.fromisoformat
PROGRAMMES = ("CALENDRIER_DE_LA_BOURSE.py", "CONTRATS_DES_FICHIERS.py", "COMMUN.py", "LIRE_LES_COURS.py")
CAL, LC = "CALENDRIER_DE_LA_BOURSE.py", "LIRE_LES_COURS.py"
# Les erreurs de l'ENVIRONNEMENT, qui ne disent rien du code éprouvé : disque plein, quota, trop de fichiers ouverts.
# Relecture indépendante du 12-10-2026 : disque plein, 17 rouges « No space left on device » ont compté comme des
# détections, et le verdict a dit « tout est conforme ». Une épreuve tombée sur l'une d'elles n'est PAS JUGÉE (code 2).
PANNES = (errno.ENOSPC, errno.EDQUOT, errno.EMFILE, errno.ENFILE)
SABOTAGES = {
    "Z0": [],
    "S1_indice_ignore": [(CAL, "    if jour in sc[\"indice\"]:\n        return CONSTATEE\n", "")],
    "S2_absence_d_indice_ferme": [(CAL, "        return PREVUE if est_jour_de_bourse(jour, eu) else FERMEE", "        return FERMEE")],
    "S3_jours_fermes_comptes": [(CAL, "        if e != FERMEE:", "        if True:")],
    "S4_pas_d_alerte_indice_un_jour_ferme": [(CAL, "            alertes.append(f\"le {d.isoformat()} : l'indice est publié, Euronext déclarait la Bourse fermée\")", "            pass")],
    "S5_pas_d_alerte_indice_absent": [(CAL, "            alertes.append(f\"le {d.isoformat()} : Euronext annonçait une séance, l'indice manque (séance gardée, R-110 ③)\")", "            pass")],
    "S6_entete_de_l_indice_libre": [(CAL, "    if not lignes or lignes[0] != list(contrats.INDICE_CAC40):", "    if not lignes:")],
    "S7_indice_un_week_end": [(CAL, "        if d.weekday() in (5, 6):", "        if False:")],
    "S8_indice_deux_fois": [(CAL, "            raise ValueError(f\"indice, ligne {n} : le {l[0]} est écrit deux fois\")", "            pass")],
    "S9_indice_sans_cours": [(CAL, "        if not any(c is not None and c > 0 for c in cours):", "        if False:")],
    "S10_nom_pris_tel_quel": [(LC, "        m = table.get(COMMUN.norm_valeur(r[\"valeur\"]))", "        m = table.get(r[\"valeur\"].lower())")],
    "S11_conflit_garde_la_premiere": [(LC, "            conflits.add((m, d))\n            del barres[m][d]\n", "            conflits.add((m, d))\n")],
    "S12_doublon_pris_pour_conflit": [(LC, "        elif _meme_barre(deja, r):", "        elif False:")],
    "S13_fenetre_en_lignes": [(LC, "        if CAL.etat_du_jour(d, sc) != CAL.FERMEE:\n            out.append((d, b.get(d)))", "        if d in b:\n            out.append((d, b.get(d)))")],
    "S14_hors_univers_ignore": [(LC, "    if cours[\"hors_univers\"][m]:\n        if not b:\n            return None, None\n        return min(b), max(b)\n", "")],
    "S15_absence_finale_toleree": [(LC, "    return (min(b) if b else cours[\"debut\"]), cours[\"fin\"]", "    return (min(b), max(b)) if b else (None, None)")],
    "S16_natures_ignorees": [(LC, "cours[\"natures\"].get((m, d), (NON_DECIDEE, \"\"))[0]", "NON_DECIDEE")],
    "S17_preuve_facultative": [(LC, "        if not r[\"preuve\"].strip():", "        if False:")],
    "S18_barre_un_jour_ferme_gardee": [(LC, "        if etat == CAL.FERMEE:", "        if False:")],
    "S19_hors_calendrier_tu": [(LC, "            hors_cal.append((m, d))\n", "")],
    "S20_ecriture_ambigue_toleree": [(LC, "            if table.get(k, m) != m:", "            if False:")],
    "S21_seul_code_0": [(LC, "    return 1 if k else 0", "    return 0")],
    "S22_trous_du_marche_tus": [(LC, "    return sorted(d for d, k in manquantes.items() if k == actives[d])", "    return []")],
    "S23_trous_tus": [(LC, "        if d not in b:\n            nature", "        if False:\n            nature")],
    "S24_nature_inconnue_admise": [(LC, "        if r[\"nature\"] not in CONTRATS.NATURES_DES_TROUS:", "        if False:")],
    "S26_doublon_compare_en_texte": [(LC, " or float(x) != float(y):", " or x != y:")],
    "S27_fin_par_la_derniere_date_lue": [(LC, "    fin = max([jusqu_au] + rangees)", "    fin = max([jusqu_au] + rangees + [d for _, d in hors_cal])")],
    "S28_valeur_absente_ignoree": [(LC, "    return (min(b) if b else cours[\"debut\"]), cours[\"fin\"]", "    return (min(b), cours[\"fin\"]) if b else (None, None)")],
    "S29_indice_arrete_tu": [(LC, "    if c[\"fin\"] > sc[\"fin\"]:", "    if False:")],
    "S30_nature_sans_trou_tue": [(LC, "    sans_trou = sorted(k for k in natures if k[1] in barres.get(k[0], {}))", "    sans_trou = []")],
    "S31_nature_un_jour_ferme_admise": [(LC, "        if ferme:\n", "        if False:\n")],
    "S32_decideur_facultatif": [(LC, "        if not r[\"decide_par\"].strip() or not r[\"le\"].strip():", "        if False:")],
    "S33_indice_infini_admis": [(CAL, "        if not all(c is None or math.isfinite(c) for c in cours):", "        if False:")],
    "S34_indice_futur_admis": [(CAL, "        if d > aujourd_hui:", "        if False:")],
    "S35_csv_illisible_non_converti": [(LC, "        except csv.Error as e:", "        except KeyError as e:")],
    "S36_mnemonique_pris_pour_un_nom": [(LC, 'COLONNES_DES_NOMS = ("nom_usuel", "onglet_google")', 'COLONNES_DES_NOMS = ("nom_usuel", "onglet_google", "mnemonique")')],
    "S37_alertes_du_calendrier_non_comptees": [(LC, "        L.append(\"  CALENDRIER : \" + alerte)\n        k += 1\n", "        L.append(\"  CALENDRIER : \" + alerte)\n")],
    "S38_ecritures_non_comptees": [(LC, "for m, e in sorted(deux.items())))\n        k += 1\n", "for m, e in sorted(deux.items())))\n")],
    "S39_noms_et_dates_non_comptes": [(LC, "for x, y in sorted(objet.items())))\n            k += 1\n", "for x, y in sorted(objet.items())))\n")],
    "S40_mises_a_part_non_comptees": [(LC, "                     + (\" …\" if len(objet) > 5 else \"\"))\n            k += 1\n", "                     + (\" …\" if len(objet) > 5 else \"\"))\n")],
    "S41_trous_du_marche_non_comptes": [(LC, "for d in marche))\n        k += 1\n", "for d in marche))\n")],
    "S42_trous_non_comptes": [(LC, "for d, n in t[:5]) + (\" …\" if len(t) > 5 else \"\"))\n            k += 1\n", "for d, n in t[:5]) + (\" …\" if len(t) > 5 else \"\"))\n")],
    "S43_seul_le_fichier_absent_rend_2": [(LC, "    except (OSError, ValueError) as e:\n        print(f\"LECTURE DES COURS IMPOSSIBLE", "    except (OSError,) as e:\n        print(f\"LECTURE DES COURS IMPOSSIBLE")],
    "S44_marque_d_excel_refusee_dans_l_indice": [(CAL, "    with open(os.path.join(racine, INDICE), encoding=\"utf-8-sig\"", "    with open(os.path.join(racine, INDICE), encoding=\"utf-8\"")],
    "S45_troisieme_exemplaire_rerange": [(LC, "        if (m, d) in conflits:\n            continue\n", "")],
    "S46_nombre_de_cases_libre": [(LC, "                if len(l) != len(entete):", "                if False:")],
    "S47_mnemonique_vide_admis": [(LC, "        if m in VIDES:\n            raise", "        if False:\n            raise")],
    "S48_par_defaut_aujourd_hui": [(LC, "    return datetime.now(ZoneInfo(\"Europe/Paris\")).date() - timedelta(days=1)", "    return datetime.now(ZoneInfo(\"Europe/Paris\")).date()")],
    "S49_par_defaut_un_mois_avant": [(LC, "    return datetime.now(ZoneInfo(\"Europe/Paris\")).date() - timedelta(days=1)", "    return datetime.now(ZoneInfo(\"Europe/Paris\")).date() - timedelta(days=30)")],
    "S50_meme_texte_en_conflit": [(LC, "        if x == y:\n            continue\n", "")],
    "S51_hors_univers_absent_signale": [(LC, "        if c[\"hors_univers\"][m] or c[\"barres\"].get(m):", "        if c[\"barres\"].get(m):")],
    "S52_date_de_commande_libre": [(LC, "        jusqu_au = CAL._date_stricte(argv[2]) if len(argv) > 2 else None", "        jusqu_au = CAL.date.fromisoformat(argv[2]) if len(argv) > 2 else None")],
    "S53_date_de_decision_facultative": [(LC, "        if not r[\"decide_par\"].strip() or not r[\"le\"].strip():", "        if not r[\"decide_par\"].strip():")],
    "S54_fin_du_calendrier_tue": [(LC, "    if reste <= PREAVIS_DU_CALENDRIER:", "    if False:")],
    "S55_natures_inutiles_tues": [(LC, "    return sorted(k for k in cours[\"natures\"] if k not in faits)", "    return []")],
    "S56_aucune_barre_gardee_dite_absente": [(LC, "        elif m in c[\"ecritures\"]:", "        elif False:")],
    "S57_nombre_avec_souligne": [(LC, "        if not (NOMBRE.fullmatch(x) and NOMBRE.fullmatch(y)) or float(x) != float(y):", "        if float(x) != float(y):")],
    "S58_un_seul_contrat_de_cours": [(LC, "CONTRATS.CONTRATS_DE_COURS, fichier)", "(CONTRATS.COURS_MAITRE,), fichier)")],
    "S59_source_toujours_dite_ecrite": [(LC, "            \"source_ecrite\": \"source\" in entete,", "            \"source_ecrite\": True,")],
    "S60_fige_jamais": [(LC, "    fige = chemin in CONTRATS.FICHIERS_DE_COURS_FIGES\n", "    fige = False\n")],
    "S61_fige_par_le_seul_nom": [(LC, "    fige = chemin in CONTRATS.FICHIERS_DE_COURS_FIGES\n", "    fige = os.path.basename(fichier) in [os.path.basename(x) for x in CONTRATS.FICHIERS_DE_COURS_FIGES]\n"), (LC, "CAL._date_stricte(CONTRATS.FICHIERS_DE_COURS_FIGES[chemin][\"fin\"]) if fige", "CAL._date_stricte(\"2026-07-10\") if fige"), (LC, "        modifie = empreinte if empreinte != CONTRATS.FICHIERS_DE_COURS_FIGES[chemin][\"sha256\"] else None\n", "        modifie = None\n")],
    "S62_fin_du_fige_a_la_derniere_date_lue": [(LC, "        jusqu_au = fin_declaree\n", "        pass\n"),
                                               (LC, "    if jusqu_au is None:\n        jusqu_au = jusqu_au_par_defaut()\n", "    if jusqu_au is None:\n        jusqu_au = max(rangees) if fige else jusqu_au_par_defaut()\n")],
    "S64_fige_allonge_tu": [(LC, "        k += 1\n    deux = {m: e", "        pass\n    deux = {m: e"),
                            (LC, "    if c.get(\"fige_allonge\"):", "    if False:")],
    "S65_empreinte_du_fige_ignoree": [(LC, "        modifie = empreinte if empreinte != CONTRATS.FICHIERS_DE_COURS_FIGES[chemin][\"sha256\"] else None\n", "        modifie = None\n")],
    "S66_au_dela_du_fige_compte_en_trous": [(LC, "    if fige and (jusqu_au is None or au_dela):", "    if fige and jusqu_au is None:")],
    "S67_au_dela_du_fige_tu": [(LC, "    if c.get(\"au_dela_du_fige\"):", "    if False:")],
    "S68_dernieres_seances_au_dela_du_fige": [(LC, "    if cours.get(\"fin_du_fige\") and jusqu_au > cours[\"fin_du_fige\"]:", "    if False:")],
    "S69_indice_ignore": [(LC, "        for a, b in cours[\"dans_l_indice\"].get(m, []):", "        for a, b in []:")],
    "S70_indice_non_borne_au_fichier": [(LC, "            a, b = max(a, cours[\"debut\"]), min(b or cours[\"fin\"], cours[\"fin\"])", "            a, b = max(a, cours[\"debut\"] - timedelta(days=30)), min(b or cours[\"fin\"], cours[\"fin\"])")],
    "S71_hors_univers_attendu_dans_l_indice": [(LC, "    if m in cours[\"hors_univers\"] and not cours[\"hors_univers\"][m] and cours[\"debut\"] is not None:", "    if m in cours[\"hors_univers\"] and cours[\"debut\"] is not None:")],
    "S72_passages_pretes_par_tous_les_codes": [(LC, "                         for p in passages if p[\"isin_bnains\"] in codes[numero]),", "                         for p in passages if p[\"isin_bnains\"] in set().union(*codes.values()) and m != \"MT\"),")],
    "S73_deux_noms_d_aujourd_hui_admis": [(LC, "            if r[\"numero\"] in actuel:\n                raise", "            if False:\n                raise")],
    "S74_meme_mnemonique_admis": [(LC, "        if m in out:\n            raise", "        if False:\n            raise")],
    "S75_increment_attendu_comme_un_historique": [(LC, "    if chemin in CONTRATS.FICHIERS_DE_COURS_INCREMENTS:\n        dans_l_indice = {}", "    if False:\n        dans_l_indice = {}")],
    "S76_valeur_sans_passage_admise": [(LC, "    if sans:\n        raise", "    if False:\n        raise")],
    "S81_passage_a_l_envers_admis": [(LC, "        if sortie is not None and sortie < entree:", "        if False:")],
    "S82_chevauchement_admis": [(LC, "            if b1 is None or a2 <= b1:", "            if False:")],
    "S83_passage_ouvert_suivi_admis": [(LC, "            if b1 is None or a2 <= b1:", "            if a2 <= (b1 or a2 - timedelta(days=1)):")],
    "S84_chevauchement_ferme_admis": [(LC, "            if b1 is None or a2 <= b1:", "            if b1 is None:")],
    "S85_meme_jour_admis": [(LC, "            if b1 is None or a2 <= b1:", "            if b1 is None or a2 < b1:")],
    "S86_passages_non_tries": [(LC, "        periodes.sort(key=lambda x: (x[0], x[1] or date.max))\n", "")],
    "S87_code_inconnu_sans_garde": [(LC, "        if p[\"isin_bnains\"]:\n            par_code", "        if p[\"isin_bnains\"] in {r[\"isin\"] for r in ident}:\n            par_code")],
    "S88_date_illisible_sans_son_passage": [(LC, "        except ValueError:\n            raise ValueError(f\"passages : date illisible", "        except KeyError:\n            raise ValueError(f\"passages : date illisible")],
    "S89_code_mal_ecrit_admis": [(LC, "            if r[champ] and not isin_valide(r[champ]):", "            if False:")],
    "S90_identites_sans_controle_des_codes": [(LC, "((IDENTITES, ident, \"isin\"), (PASSAGES, passages, \"isin_bnains\"))", "((PASSAGES, passages, \"isin_bnains\"),)")],
    "S91_cle_isin_ignoree": [(LC, "    return (10 - somme % 10) % 10 == int(code[-1])", "    return True")],
    "S92_forme_isin_sans_casse": [(LC, "FORME_ISIN = re.compile(r\"[A-Z]{2}[A-Z0-9]{9}[0-9]\")", "FORME_ISIN = re.compile(r\"[A-Z]{2}[A-Z0-9]{9}[0-9]\", re.I)")],
    "S80_code_vide_relie_les_passages_sans_code":[(LC, "        if r[\"isin\"]:\n            codes[", "        if True:\n            codes[")],
    "S79_code_vide_compte_comme_partage": [(LC, "        if r[\"isin\"] and societe_du_code.setdefault(", "        if societe_du_code.setdefault(")],
    "S77_code_de_deux_societes_admis": [(LC, "        if r[\"isin\"] and societe_du_code.setdefault(r[\"isin\"], r[\"numero\"]) != r[\"numero\"]:", "        if False:")],
    "S78_passage_non_borne_a_la_fin": [(LC, "min(b or cours[\"fin\"], cours[\"fin\"])\n", "(b or cours[\"fin\"])\n")],
    "S63_tout_fichier_d_arrivee_fige": [(LC, "    fige = chemin in CONTRATS.FICHIERS_DE_COURS_FIGES\n", "    fige = chemin in CONTRATS.FICHIERS_DE_COURS_FIGES or chemin.startswith(\"donnees/c\") and \"maitre\" not in chemin\n"), (LC, "CAL._date_stricte(CONTRATS.FICHIERS_DE_COURS_FIGES[chemin][\"fin\"]) if fige", "CAL._date_stricte(\"2026-07-10\") if fige"), (LC, "        modifie = empreinte if empreinte != CONTRATS.FICHIERS_DE_COURS_FIGES[chemin][\"sha256\"] else None\n", "        modifie = None\n")],
    "S93_lignes_mises_a_part_muettes": [(LC, "    return cours[\"lignes_lues\"] - sum(len(b) for b in cours[\"barres\"].values()) - len(cours[\"doublons\"])",
                                         "    return 0")],
    "S94_doublons_comptes_ecartes": [(LC, " - len(cours[\"doublons\"])\n\n\ndef trous", "\n\n\ndef trous")],
    "S25_date_des_cours_libre": [(LC, "            d = CAL._date_stricte(r[\"date\"])\n        except ValueError:\n            illisibles", "            d = CAL.date.fromisoformat(r[\"date\"])\n        except ValueError:\n            illisibles")],
}
MARCHE = ["2010-12-24", "2010-12-31", "2012-12-24", "2012-12-31", "2015-12-31"]
BOUYGUES = ["2011-11-03", "2011-11-04", "2011-11-07", "2011-11-08", "2011-11-09", "2011-11-10"]
DECEMBRE_2010 = ["2010-12-20", "2010-12-21", "2010-12-22", "2010-12-23", "2010-12-24", "2010-12-27", "2010-12-28",
                 "2010-12-29", "2010-12-30", "2010-12-31"]
ENTETE_COURS = "valeur,date,open,high,low,close,volume,source"
H, CM = "donnees/sources_yahoo/historique_long_repare.csv", "donnees/cours_maitre.csv"
FIN = {H: D("2026-10-02"), CM: D("2026-10-09")}
SEMAINE = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09"]
ENTETE_NATURES = "mnemonique,date,nature,preuve,decide_par,le"


def lignes_de(chemin):
    """Rend les lignes d'un fichier texte du dépôt, sans leur fin de ligne.

    ① RÔLE — Partir des vraies lignes pour fabriquer les copies.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `chemin` : un chemin relatif au dépôt.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe, en UTF-8.
    ⑤ SORTIE — UNE valeur : la liste des lignes.
      [rend: 1]
    ⑥ TRAITEMENT — lire, découper.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-732 : un cas au moins vient d'une vraie ligne.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(os.path.join(DEPOT, chemin), encoding="utf-8-sig") as f:
        return f.read().splitlines()


def racine(tmp, nom, cours=None, indice=None, natures=None, referentiel=None, euronext=None, identites=None,
           passages=None):
    """Fabrique une racine de dépôt jetable, avec les vrais fichiers sauf ceux qu'on remplace.

    ① RÔLE — Donner à chaque épreuve son propre dépôt.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par cas.
    ③ ENTRÉE — `tmp` : le dossier jetable · `nom` : le nom du cas · `cours`, `indice`, `natures` : des listes de lignes
      (en-tête compris) qui remplacent donnees/cours_maitre.csv, l'indice, la nature des trous ; None garde le vrai
      fichier · `referentiel` : des lignes qui remplacent le référentiel · `euronext` : des lignes qui remplacent
      donnees/CALENDRIER_EURONEXT.csv · `identites`, `passages` : des lignes qui remplacent les deux tables de la
      règle I-3 (donnees/sources_indice/IDENTITES_DES_SOCIETES.csv et PASSAGES_DANS_LE_CAC40.csv).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de la racine.
      [rend: 1]
    ⑥ TRAITEMENT — créer donnees/ et donnees/sources_indice/, copier ou écrire chaque fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve ne touche jamais le dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = os.path.join(tmp, nom)
    os.makedirs(os.path.join(r, "donnees", "sources_indice"), exist_ok=True)
    ref = glob.glob(os.path.join(DEPOT, "donnees", "REFERENTIEL_VALEURS_*.csv"))
    for chemin, remplace in (("donnees/cours_maitre.csv", cours), ("donnees/sources_indice/INDICE_CAC40.csv", indice),
                             ("donnees/NATURE_DES_TROUS.csv", natures), ("donnees/CALENDRIER_EURONEXT.csv", euronext),
                             ("donnees/" + os.path.basename(ref[0]), referentiel),
                             ("donnees/sources_indice/IDENTITES_DES_SOCIETES.csv", identites),
                             ("donnees/sources_indice/PASSAGES_DANS_LE_CAC40.csv", passages)):
        cible = os.path.join(r, chemin)
        if remplace is None:
            shutil.copy(os.path.join(DEPOT, chemin), cible)
        else:
            with open(cible, "w", encoding="utf-8") as f:
                f.write("\n".join(remplace) + "\n")
    return r


def leve(f, *a):
    """Rend le nom de l'erreur levée par f(*a), ou None si elle rend la main.

    ① RÔLE — Dire si un appel est refusé.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `f` : une fonction · `a` : ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom de l'erreur, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — appeler, attraper.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un refus se prouve par l'erreur, pas par le silence.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `f`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        f(*a)
        return None
    except Exception as e:
        return type(e).__name__


def raison(f, *a):
    """Rend le nom ET le message de l'erreur levée par f(*a), ou None si elle rend la main.

    ① RÔLE — Dire POURQUOI un appel est refusé, pas seulement qu'il l'est.
    ② CONTEXTE D'APPEL — `epreuves`, L12 et L22.
    ③ ENTRÉE — `f` : une fonction · `a` : ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « NomDeLErreur : message », ou None.
      [rend: 1]
    ⑥ TRAITEMENT — appeler, attraper.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du banc du 12-10-2026 (pièce B) : depuis que la lecture exige un passage dans l'indice pour
      chaque valeur de l'univers, une valeur ajoutée au référentiel est refusée pour CETTE raison ; L12 et L22, qui ne
      regardaient que le nom de l'erreur, sont restées vertes quand on retirait le refus qu'elles éprouvent (S20, S47).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `f`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        f(*a)
        return None
    except Exception as e:
        return f"{type(e).__name__} : {e}"


def muet(f, *a):
    """Appelle f(*a) sans rien laisser s'afficher, et rend ce qu'elle rend.

    ① RÔLE — Garder l'affichage des épreuves lisible quand une épreuve appelle `main`.
    ② CONTEXTE D'APPEL — `epreuves`, L17 et L21.
    ③ ENTRÉE — `f` : une fonction · `a` : ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : ce que rend `f`.
      [rend: 1]
    ⑥ TRAITEMENT — détourner la sortie standard le temps de l'appel.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Quatorze appels de `main` affichaient leurs comptes rendus au milieu des verdicts.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `f`, sans l'affichage.
    ⑪ TERMINAISON — Rend la main ou laisse passer l'erreur de `f`.
      [sort: non]
    """
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a)


def epreuves(dossier, tmp):
    """Joue L1 à L31 avec les programmes du dossier `dossier`, et rend la liste (nom, verdict).

    ① RÔLE — Les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `dossier` : les quatre programmes, sabotés ou non · `tmp` : un dossier jetable.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : la liste des couples (nom, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — importer la lecture des cours copiée, puis chaque épreuve dans son propre essai : une épreuve qui
      lève est rouge, les suivantes jouent.
    ⑦ UNITÉ — Des séances et des dates.
    ⑧ POURQUOI — Chaque réponse attendue est écrite à la main : le module ne se juge pas lui-même.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `tmp`, lance des processus.
    ⑪ TERMINAISON — Rend la main ; chaque lancement seul est borné à 120 secondes.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("lc_%d" % id(tmp), os.path.join(dossier, LC))
    M = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(M)
    K = M.CAL
    res = []

    def essai(nom, f):
        """Joue une épreuve et range son verdict.

        ① RÔLE — Isoler chaque épreuve : une erreur la rend rouge, sans arrêter les autres.
        ② CONTEXTE D'APPEL — `epreuves`, une fois par épreuve.
        ③ ENTRÉE — `nom` : le nom de l'épreuve · `f` : une fonction sans argument qui rend vrai si l'épreuve est verte.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Ne rend rien : ajoute (nom, verdict) à `res` ; le verdict vaut None quand l'erreur vient de
          l'environnement (PANNES, ou mémoire épuisée) : l'épreuve n'est pas jugée.
          [rend: rien]
        ⑥ TRAITEMENT — appeler `f`, attraper ; une erreur de l'environnement donne None, toute autre erreur False.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un sabotage qui fait lever une épreuve doit la faire rougir, pas arrêter le jeu.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Celui de `f`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        try:
            v = bool(f())
        except Exception as e:
            v = None if isinstance(e, MemoryError) or getattr(e, "errno", None) in PANNES else False
            nom += f" — {type(e).__name__} : {e}"[:200]
        res.append((nom, v))

    maitre = lignes_de(CM)
    reel = {}

    def lire_reel(fichier):
        """Lit un vrai fichier de cours une seule fois par jeu d'épreuves.

        ① RÔLE — Ne pas relire l'historique long à chaque épreuve.
        ② CONTEXTE D'APPEL — Les épreuves L1, L2, L3, L13.
        ③ ENTRÉE — `fichier` : un fichier de cours relatif au dépôt.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le rendu de `lire`.
          [rend: 1]
        ⑥ TRAITEMENT — lire si ce n'est pas déjà fait.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Deux secondes par lecture de l'historique long.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit des fichiers.
        ⑪ TERMINAISON — Rend la main ou lève.
          [sort: non]
        """
        if fichier not in reel:
            reel[fichier] = M.lire(DEPOT, fichier, FIN[fichier])
        return reel[fichier]

    def sans_les_demi_seances():
        """L'historique réparé privé de ses lignes des cinq demi-séances, comblées le 27-10-2026 (A-555 (b)) : le fichier
        tel qu'il était avant le comblement, pour que l'étalon de R-110 ① garde un cas réel."""
        os.makedirs(tmp, exist_ok=True)
        f_ = os.path.join(tmp, "historique_sans_les_demi_seances.csv")
        if not os.path.exists(f_):
            with open(os.path.join(DEPOT, H), encoding="utf-8") as a, open(f_, "w", encoding="utf-8") as b:
                for l in a:
                    if l.split(",")[1:2] and l.split(",")[1] in MARCHE:
                        continue
                    b.write(l)
        return M.lire(DEPOT, os.path.relpath(f_, DEPOT), FIN[H])

    essai("L1 ÉTALON : l'historique réparé n'a plus de trou de tout le marché ; privé des cinq demi-séances, il a celles "
          "de R-110 ①",
          lambda: M.trous_de_tout_le_marche(lire_reel(H)) == []
          and [d.isoformat() for d in M.trous_de_tout_le_marche(sans_les_demi_seances())] == MARCHE)
    essai("L2 hors trous du marché : Bouygues six trous du 03 au 10-11-2011 ; AXA vingt",
          lambda: [d.isoformat() for d, _ in M.trous(lire_reel(H), "EN") if d.isoformat() not in MARCHE] == BOUYGUES
          and len([d for d, _ in M.trous(lire_reel(H), "CS") if d.isoformat() not in MARCHE]) == 20)
    essai("L3 maître : AI 709 barres, 644 + 65 écritures ; 13 valeurs à plusieurs écritures ; aucun nom inconnu",
          lambda: len(lire_reel(CM)["barres"]["AI"]) == 709
          and dict(lire_reel(CM)["ecritures"]["AI"]) == {"AIR LIQUIDE": 644, "AIR_LIQUIDE": 65}
          and sum(1 for e in lire_reel(CM)["ecritures"].values() if len(e) > 1) == 13
          and not lire_reel(CM)["inconnues"])

    def l4():
        """Vinci sans sa séance du 03-07-2026.

        ① RÔLE — L4.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le maître porte une ligne VINCI du 2026-07-03.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — retirer la ligne, lire, comparer.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Le cas mesuré par Cowork en R-111 ②.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        sans = [x for x in maitre if not x.startswith("VINCI,2026-07-03,")]
        if len(sans) != len(maitre) - 1:
            return False
        c = M.lire(racine(tmp, "l4", cours=sans), CM, FIN[CM])
        f = M.dernieres_seances(c, "DG", 14, D("2026-07-10"))
        return (M.trous(c, "DG") == [(D("2026-07-03"), M.NON_DECIDEE)] and len(f) == 14
                and f[0][0] == D("2026-06-23") and (D("2026-07-03"), None) in f)
    essai("L4 Vinci sans le 03-07-2026 : un trou, et les 14 dernières séances le portent", l4)

    def l5():
        """Une écriture inconnue n'est pas réunie.

        ① RÔLE — L5, le cas qui DOIT ÉCHOUER.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — ajouter « AIR LIQUID » un jour de séance, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un motif se calibre aussi sur un cas qui doit échouer, sinon il sur-détecte.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = M.lire(racine(tmp, "l5", cours=maitre + ["AIR LIQUID,2026-10-12,1,1,1,1,1,abc"]), CM, FIN[CM])
        return dict(c["inconnues"]) == {"AIR LIQUID": 1} and len(c["barres"]["AI"]) == 709
    essai("L5 DOIT ÉCHOUER : « AIR LIQUID » signalé sans mnémonique, Air Liquide inchangé", l5)

    def l6():
        """Le calendrier des séances sur des dates écrites à la main.

        ① RÔLE — L6.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — interroger `etat_du_jour` et `seances_entre`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — R-110.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        sc = K.lire_les_seances(DEPOT)
        e = [K.etat_du_jour(D(x), sc) for x in ("2026-10-02", "2026-10-09", "2015-12-25", "2010-12-24", "2026-12-25",
                                                  "2026-10-10")]
        s = [d.isoformat() for d, _ in K.seances_entre(D("2010-12-20"), D("2010-12-31"), sc)]
        return (e == [K.CONSTATEE, K.PREVUE, K.FERMEE, K.CONSTATEE, K.FERMEE, K.FERMEE] and s == DECEMBRE_2010
                and leve(K.etat_du_jour, D("1999-12-31"), sc) == "HorsCalendrier"
                and leve(K.etat_du_jour, D("2027-01-04"), sc) == "HorsCalendrier" and sc["alertes"] == [])
    essai("L6 calendrier : six états, dix séances de décembre 2010, deux jours hors du calendrier, aucune alerte", l6)

    indice = lignes_de("donnees/sources_indice/INDICE_CAC40.csv")
    indice_long = indice + [x + ",,8000" for x in SEMAINE]
    euronext = lignes_de("donnees/CALENDRIER_EURONEXT.csv")
    euronext_long = [x.replace("2026-12-31,COUVERT_JUSQU_AU,", "2099-12-31,COUVERT_JUSQU_AU,") for x in euronext]
    une = [maitre[0]] + [",".join([x.split(",")[0].replace("_", " ")] + x.split(",")[1:]) for x in maitre[1:]]
    une = [x.replace("SAINT GOBAIN,", "SAINT-GOBAIN,").replace("UNIBAIL RODAMCO WESTFIELD,", "UNIBAIL-RODAMCO-WESTFIELD,")
           for x in une]

    def l7():
        """Les deux alertes du calendrier.

        ① RÔLE — L7.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — L'indice porte le 30-09-2026 et pas le 03-04-2026.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — retirer le 30-09-2026, ajouter le 03-04-2026, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — R-110 ③ : l'indice publié dit ouvert ; son absence seule ne ferme jamais.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        L = [x for x in indice if not x.startswith("2026-09-30,")] + ["2026-04-03,,8000"]
        if len(L) != len(indice):
            return False
        sc = K.lire_les_seances(racine(tmp, "l7", indice=L))
        a = sc["alertes"]
        return (len(a) == 2 and any(x.startswith("le 2026-04-03") for x in a)
                and any(x.startswith("le 2026-09-30") for x in a) and K.etat_du_jour(D("2026-09-30"), sc) == K.PREVUE)
    essai("L7 alertes : indice un jour fermé (03-04-2026), indice absent un jour annoncé (30-09-2026, PRÉVUE)", l7)

    refus = {
        "en-tête faux": ["date,bnains,yahooo"] + indice[1:],
        "date 20100105": indice + ["20261005,,8000"],
        "date deux fois": indice + [indice[-1]],
        "un samedi": indice + ["2026-10-03,,8000"],
        "sans cours": indice + ["2026-10-05,,"],
        "cours illisible": indice + ["2026-10-05,,huit"],
        "cours inf": indice + ["2026-10-05,,inf"],
        "cours nan": indice + ["2026-10-05,nan,8000"],
        "date après aujourd'hui": indice + ["2099-01-05,,8000"],
    }

    def bom():
        """L'indice écrit par Excel, avec sa marque d'ordre d'octets.

        ① RÔLE — Partie de L8.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si l'indice se lit avec ses 6 844 dates.
          [rend: 1]
        ⑥ TRAITEMENT — réécrire l'indice avec la marque, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : aucune épreuve ne passait un indice enregistré par Excel.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        r = racine(tmp, "l8_bom")
        with open(os.path.join(r, "donnees", "sources_indice", "INDICE_CAC40.csv"), "w", encoding="utf-8-sig") as f:
            f.write("\n".join(indice) + "\n")
        return len(K.lire_les_seances(r)["indice"]) == 6844
    essai("L8 refus de l'indice : " + ", ".join(refus) + " ; marque d'Excel tolérée",
          lambda: all(leve(K.lire_les_seances, racine(tmp, "l8_%d" % i, indice=L)) == "ValueError"
                      for i, L in enumerate(refus.values())) and bom())

    def l9():
        """Doublon identique et conflit.

        ① RÔLE — L9.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le maître porte ACCOR et AXA le 2026-10-09.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — recopier la vraie ligne d'Accor ; écrire une seconde version d'AXA, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Table de réception, E4.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        ac = [x for x in maitre if x.startswith("ACCOR,2026-10-09,")]
        cs = [x for x in maitre if x.startswith("AXA,2026-10-09,")]
        if len(ac) != 1 or len(cs) != 1:
            return False
        p = cs[0].split(",")
        p[5] = str(float(p[5]) + 1)
        a = ac[0].split(",")
        a[5] = a[5] + "0" if "." in a[5] else a[5] + ".0"
        c = M.lire(racine(tmp, "l9", cours=maitre + [",".join(a), ",".join(p)]), CM, FIN[CM])
        trois = M.lire(racine(tmp, "l9b", cours=maitre + [",".join(p), cs[0]]), CM, FIN[CM])
        n = ac[0].split(","); n[5] = "nan"
        u = cs[0].split(","); u[6] = u[6][:-3] + "_" + u[6][-3:] if len(u[6]) > 3 else u[6]
        texte = M.lire(racine(tmp, "l9c", cours=[x for x in maitre if x not in (ac[0], cs[0])]
                              + [",".join(n), ",".join(n), cs[0], ",".join(u)]), CM, FIN[CM])
        return (c["doublons"] == [("AC", D("2026-10-09"))] and D("2026-10-09") in c["barres"]["AC"]
                and c["conflits"] == [("CS", D("2026-10-09"))] and D("2026-10-09") not in c["barres"]["CS"]
                and M.trous(c, "CS") == [(D("2026-10-09"), "DEUX VERSIONS")]
                and trois["conflits"] == [("CS", D("2026-10-09"))] and D("2026-10-09") not in trois["barres"]["CS"]
                and texte["doublons"] == [("AC", D("2026-10-09"))] and texte["conflits"] == [("CS", D("2026-10-09"))]
                and "_" in u[6])
    essai("L9 doublon gardé une fois (« 45.390 » = « 45.39 », « nan » = « nan ») ; deux versions, A B A, ou "
          "« 1_234 » contre « 1234 » : aucune gardée", l9)

    def l10():
        """Barres un jour fermé, un samedi, hors du calendrier.

        ① RÔLE — L10.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — ajouter trois barres d'Accor, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Table de réception, A3.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = M.lire(racine(tmp, "l10", cours=maitre + ["ACCOR,2026-05-01,1,1,1,1,1,abc", "ACCOR,2026-10-03,1,1,1,1,1,abc",
                                                       "ACCOR,1999-12-31,1,1,1,1,1,google", "ACCOR,2027-01-04,1,1,1,1,1,abc"]),
                   CM, FIN[CM])
        return ([(m, d.isoformat()) for m, d, _ in c["hors_seance"]] == [("AC", "2026-05-01"), ("AC", "2026-10-03")]
                and c["hors_calendrier"] == [("AC", D("1999-12-31")), ("AC", D("2027-01-04"))]
                and c["fin"] == D("2026-10-09")
                and not {D("2026-05-01"), D("2026-10-03"), D("1999-12-31"), D("2027-01-04")} & set(c["barres"]["AC"]))
    essai("L10 barres un jour fermé, un samedi, hors du calendrier : mises à part", l10)

    def l11():
        """La nature des trous, et ses refus.

        ① RÔLE — L11.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — lire l'historique réparé avec une nature écrite, puis cinq fichiers fautifs.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — R-111 ⑤.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        bonne = "EN,2011-11-03,SUSPENSION,avis d'épreuve,épreuve,2026-10-10"
        r = racine(tmp, "l11", natures=[ENTETE_NATURES, bonne])
        os.makedirs(os.path.join(r, "donnees", "sources_yahoo"), exist_ok=True)
        shutil.copy(os.path.join(DEPOT, H), os.path.join(r, H))
        c = M.lire(r, H, FIN[H])
        t = [x for x in M.trous(c, "EN") if x[0].isoformat() not in MARCHE]
        ok = t[0] == (D("2011-11-03"), "SUSPENSION") and all(n == M.NON_DECIDEE for _, n in t[1:])
        ok = ok and c["natures_sans_trou"] == []
        sans = M.lire(racine(tmp, "l11s", natures=[ENTETE_NATURES, "AC,2026-10-09,SUSPENSION,p,e,x"]), CM, FIN[CM])
        ok = ok and sans["natures_sans_trou"] == [("AC", D("2026-10-09"))]
        fautes = ["ZZ,2011-11-03,SUSPENSION,p,e,x", "EN,2011-11-03,FERMETURE,p,e,x", "EN,2011-11-03,SUSPENSION, ,e,x",
                  "EN,2011-11-03,SUSPENSION,p, ,x", "EN,2011-11-03,SUSPENSION,p,e, ", "EN,03-11-2011,SUSPENSION,p,e,x", "AC,2026-10-03,SUSPENSION,p,e,x",
                  "AC,1990-01-02,SUSPENSION,p,e,x"]
        mauvais = [[ENTETE_NATURES, x] for x in fautes] + [[ENTETE_NATURES, bonne, bonne]]
        return ok and all(leve(M.lire, racine(tmp, "l11_%d" % i, natures=L), CM, FIN[CM]) == "ValueError"
                          for i, L in enumerate(mauvais))
    essai("L11 nature lue, nature sur une séance qui a son cours relevée ; neuf natures fautives refusées", l11)

    def l12():
        """Une écriture qui désigne deux mnémoniques.

        ① RÔLE — L12.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le référentiel porte une ligne ACCOR, en deuxième ligne.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — recopier la ligne d'Accor sous le mnémonique ZZ, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Le défaut ⑤ de `charger_referentiel` de la mesure : la dernière ligne lue l'emportait sans message.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        ref = lignes_de(os.path.relpath(glob.glob(os.path.join(DEPOT, "donnees", "REFERENTIEL_VALEURS_*.csv"))[0], DEPOT))
        lignes = list(csv.reader(io.StringIO("\n".join(ref))))
        i = lignes[0].index("mnemonique")
        z = list(lignes[1]); z[i] = "ZZ"
        if lignes[1][0] != "ACCOR":
            return False
        buf = io.StringIO(); csv.writer(buf, lineterminator="\n").writerows(lignes + [z])
        r = raison(M.lire, racine(tmp, "l12", referentiel=buf.getvalue().splitlines()))
        return r is not None and r.startswith("ValueError : référentiel : l'écriture") and "désigne" in r
    essai("L12 une écriture désignant deux mnémoniques est refusée", l12)

    def l13():
        """Hors univers, et absence finale.

        ① RÔLE — L13.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le maître porte ACCOR les 08 et 09-10-2026.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — lire le maître, puis une copie sans les deux dernières séances d'Accor.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Table de réception, E3 ; colonne hors_univers du référentiel.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        sans = [x for x in maitre if not x.startswith(("ACCOR,2026-10-08,", "ACCOR,2026-10-09,"))]
        if len(sans) != len(maitre) - 2:
            return False
        c = M.lire(racine(tmp, "l13", cours=sans), CM, FIN[CM])
        return (M.trous(lire_reel(CM), "MT") == [] and len(lire_reel(CM)["barres"]["MT"]) == 30
                and M.trous(c, "AC") == [(D("2026-10-08"), M.NON_DECIDEE), (D("2026-10-09"), M.NON_DECIDEE)])
    essai("L13 ArcelorMittal hors univers : aucun trou ; Accor sans ses deux dernières séances : deux trous", l13)

    def l14():
        """Lancé seul : codes 1, 0 et 2.

        ① RÔLE — L14.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — lancer le module copié sur trois racines.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — R-734.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lance trois processus.
        ⑪ TERMINAISON — Rend la main ; chaque processus est borné à 120 secondes.
          [sort: non]
        """
        prog = os.path.join(dossier, LC)
        vide = racine(tmp, "l14_vide")
        os.remove(os.path.join(vide, "donnees", "cours_maitre.csv"))
        codes = [subprocess.run([sys.executable, prog, r, CM, "2026-10-09"], capture_output=True, timeout=120).returncode
                 for r in (DEPOT, racine(tmp, "l14_une", cours=une, indice=indice_long, euronext=euronext_long), vide)]
        return codes == [1, 0, 2]
    essai("L14 lancé seul : 1 sur le maître, 0 sans doubles écritures, 2 sans fichier des cours", l14)
    essai("L15 dernieres_seances avec n = 0 est refusé",
          lambda: leve(M.dernieres_seances, lire_reel(CM), "AI", 0, D("2026-10-09")) == "ValueError")
    essai("L16 une date illisible est comptée, pas rangée",
          lambda: dict(M.lire(racine(tmp, "l16", cours=maitre + ["ACCOR,20261009,1,1,1,1,1,abc"]), CM, FIN[CM])["dates_illisibles"])
          == {"20261009": 1})
    def l17():
        """Chaque sorte de signal, seule, fait rendre 1.

        ① RÔLE — L17.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le maître porte ACCOR et AXA le 2026-10-09, et toutes les valeurs le 2026-10-08.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — une base sans rien à signaler (une seule écriture par valeur, indice prolongé), puis neuf copies
          qui portent chacune UNE anomalie ; `main` sur chacune.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : le code de sortie n'était éprouvé que par les écritures
          multiples ; retirer le compte des trous laissait toutes les épreuves vertes.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        ac = [x for x in une if x.startswith("ACCOR,2026-10-09,")][0]
        cs = [x for x in une if x.startswith("AXA,2026-10-09,")][0]
        p = cs.split(","); p[5] = str(float(p[5]) + 1)
        cas = {
            "base": dict(cours=une, indice=indice_long),
            "calendrier": dict(cours=une, indice=[x for x in indice_long if not x.startswith("2026-09-30,")]),
            "écritures": dict(cours=[x.replace("AIR LIQUIDE,2026-10-09,", "AIR_LIQUIDE,2026-10-09,") for x in une],
                              indice=indice_long),
            "indice arrêté": dict(cours=une),
            "nom sans mnémonique": dict(cours=une + ["AIR LIQUID,2026-10-09,1,1,1,1,1,abc"], indice=indice_long),
            "date illisible": dict(cours=une + ["ACCOR,20261009,1,1,1,1,1,abc"], indice=indice_long),
            "doublon": dict(cours=une + [ac], indice=indice_long),
            "conflit": dict(cours=une + [",".join(p)], indice=indice_long),
            "barre un jour fermé": dict(cours=une + ["ACCOR,2026-05-01,1,1,1,1,1,abc"], indice=indice_long),
            "nature sur un cours": dict(cours=une, indice=indice_long,
                                        natures=[ENTETE_NATURES, "AC,2026-10-09,SUSPENSION,p,e,x"]),
            "trou": dict(cours=[x for x in une if x != ac], indice=indice_long),
            "trou du marché": dict(cours=[x for x in une if ",2026-10-08," not in x], indice=indice_long),
            "nature hors univers après la dernière barre": dict(cours=une, indice=indice_long, natures=[
                ENTETE_NATURES, "MT,2026-10-09,SUSPENSION,p,e,x"]),
        }
        codes = {k: muet(M.main, [racine(tmp, "l17_%d" % i, euronext=euronext_long, **v), CM, "2026-10-09"])
                 for i, (k, v) in enumerate(cas.items())}
        return codes == {k: (0 if k == "base" else 1) for k in cas}
    essai("L17 chaque sorte de signal, seule, fait rendre 1 ; la base rend 0", l17)

    def l18():
        """Une valeur absente du fichier entier.

        ① RÔLE — L18.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — retirer toutes les lignes VINCI, lire, résumer.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : Vinci retiré, la lecture rendait « rien à signaler ».
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = M.lire(racine(tmp, "l18", cours=[x for x in une if not x.startswith(("VINCI,", "ARCELORMITTAL,"))],
                          indice=indice_long), CM, FIN[CM])
        lignes, k = M.resume(c)
        ok = (len(M.trous(c, "DG")) == 709 and any(x.startswith("  ABSENTE DU FICHIER DG : 709") for x in lignes)
              and not any(" MT " in x for x in lignes))
        dg = [x for x in une if x.startswith("VINCI,")]
        en_conflit = [",".join(x.split(",")[:5] + [str(float(x.split(",")[5]) + 1)] + x.split(",")[6:]) for x in dg]
        c2 = M.lire(racine(tmp, "l18b", cours=une + en_conflit, indice=indice_long), CM, FIN[CM])
        ok = ok and any(x.startswith("  AUCUNE BARRE GARDÉE DG : 709") for x in M.resume(c2)[0])
        c3 = M.lire(racine(tmp, "l18c", cours=[une[0]], indice=indice_long), CM, FIN[CM])
        l3, k3 = M.resume(c3)
        return ok and sum(1 for x in l3 if x.startswith("  ABSENTE DU FICHIER ")) == 39 and k3 >= 39
    essai("L18 Vinci absent : 709 trous, dit ABSENTE (ArcelorMittal, hors univers, ne l'est pas) ; toutes ses barres en "
          "conflit : AUCUNE BARRE GARDÉE ; fichier sans barre : 39 valeurs ABSENTES", l18)

    def l19():
        """Tout le marché absent des deux dernières séances.

        ① RÔLE — L19.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — retirer toutes les lignes des 08 et 09-10-2026, lire jusqu'au 09-10-2026.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : la fin était la dernière date lue, et ce cas passait sans
          un mot — la collecte en panne pour tout le monde ressemblait à « rien à signaler ».
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = M.lire(racine(tmp, "l19", cours=[x for x in une if ",2026-10-08," not in x and ",2026-10-09," not in x],
                          indice=indice_long), CM, FIN[CM])
        return M.trous_de_tout_le_marche(c) == [D("2026-10-08"), D("2026-10-09")]
    essai("L19 tout le marché absent des 08 et 09-10-2026 : deux trous de tout le marché", l19)

    def l20():
        """Un mnémonique écrit à la place d'un nom.

        ① RÔLE — L20, le cas qui DOIT ÉCHOUER.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — remplacer la barre de Carrefour du 09-10-2026 par une ligne « CA », lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : la ligne « CA » était rangée sous Carrefour.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = M.lire(racine(tmp, "l20", cours=[x for x in une if not x.startswith("CARREFOUR,2026-10-09,")]
                          + ["CA,2026-10-09,99,99,99,99,1,abc"]), CM, FIN[CM])
        return dict(c["inconnues"]) == {"CA": 1} and D("2026-10-09") not in c["barres"]["CA"]
    essai("L20 DOIT ÉCHOUER : une ligne « CA » n'est rangée sous aucune valeur", l20)
    essai("L21 `main` rend 2 : en-tête faux, case de 200 000 caractères, ligne à neuf cases, date « 20261009 »",
          lambda: [muet(M.main, [racine(tmp, "l21_%d" % i, cours=L), CM, "2026-10-09"]) for i, L in enumerate((
              [ENTETE_COURS + "s"] + maitre[1:], maitre + ['ACCOR,2026-10-09,"' + "x" * 200000 + '",1,1,1,1,abc'],
              maitre + ["ACCOR,2026-10-09,1,1,1,1,1,abc,x"]))] == [2, 2, 2]
          and muet(M.main, [DEPOT, CM, "20261009"]) == 2)

    def l22():
        """Un mnémonique vide dans le référentiel.

        ① RÔLE — L22.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le référentiel porte une ligne ACCOR, en deuxième ligne.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — vider le mnémonique d'Accor, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une valeur sans mnémonique ne peut être reconnue (R-111 ③).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        ref = lignes_de(os.path.relpath(glob.glob(os.path.join(DEPOT, "donnees", "REFERENTIEL_VALEURS_*.csv"))[0], DEPOT))
        lignes = list(csv.reader(io.StringIO("\n".join(ref))))
        if lignes[1][0] != "ACCOR":
            return False
        lignes[1][lignes[0].index("mnemonique")] = ""
        buf = io.StringIO(); csv.writer(buf, lineterminator="\n").writerows(lignes)
        r = raison(M.lire, racine(tmp, "l22", referentiel=buf.getvalue().splitlines()), CM, FIN[CM])
        return r is not None and r.startswith("ValueError : référentiel, ligne") and "pas de mnémonique" in r
    essai("L22 un mnémonique vide dans le référentiel est refusé", l22)
    essai("L23 l'historique réparé lu jusqu'au 09-10-2026 : les cinq séances du 05 au 09-10 sont des trous du marché",
          lambda: [d.isoformat() for d in M.trous_de_tout_le_marche(M.lire(DEPOT, H, D("2026-10-09")))] == SEMAINE)
    hier = datetime.now(ZoneInfo("Europe/Paris")).date() - timedelta(days=1)
    essai("L24 sans date, la lecture attend les cours jusqu'à la veille (Paris), calculée ici à part",
          lambda: M.jusqu_au_par_defaut() == hier and M.lire(DEPOT, CM)["fin"] == M.lire(DEPOT, CM, hier)["fin"])

    def l25():
        """La fin prochaine de la liste d'Euronext est signalée.

        ① RÔLE — L25.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — une liste d'Euronext qui s'arrête dix jours après aujourd'hui (jamais avant le 09-10-2026), ses
          fermetures d'après retirées ; une autre qui s'arrête en 2099 ; chercher la ligne dans le résumé.
        ⑦ UNITÉ — Des jours.
        ⑧ POURQUOI — R-110 ② ; seconde relecture indépendante du 10-10-2026 : à partir du 02-01-2027, toute lecture
          sans date s'arrêterait, sans préavis.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        fin = max(D("2026-10-09"), hier + timedelta(days=11))
        courte = [x for x in euronext if x.split(",")[1] not in ("FERME", "DEMI_SEANCE", "COUVERT_JUSQU_AU")
                  or (x.split(",")[1] != "COUVERT_JUSQU_AU" and D(x.split(",")[0]) <= fin)]
        courte.append(fin.isoformat() + ",COUVERT_JUSQU_AU,épreuve,,")   # cinq colonnes depuis le 27-10-2026
        dit = lambda e: any(x.startswith("  CALENDRIER : la liste d'Euronext s'arrête")
                            for x in M.resume(M.lire(racine(tmp, "l25_%d" % len(e), cours=une, indice=indice_long,
                                                            euronext=e), CM, FIN[CM]))[0])
        return dit(courte) and not dit(euronext_long)
    essai("L25 la liste d'Euronext qui s'arrête dans moins de 30 jours est signalée ; celle de 2099 ne l'est pas", l25)

    def l26():
        """Les trois fichiers de cours du dépôt se lisent.

        ① RÔLE — L26.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — donnees/cac40_ohlcv.csv tel qu'au 11-10-2026 (figé : on ne le touche jamais) ;
          donnees/claude_cours_nouveaux.csv, quel qu'il soit (il change chaque soir).
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — lire les deux fichiers à sept colonnes ; compter ; puis un fichier à six colonnes.
        ⑦ UNITÉ — Des barres, des séances.
        ⑧ POURQUOI — Relecture de Cowork du 11-10-2026 : le lecteur « pour tous » refusait ces deux fichiers. Les comptes
          attendus (25 116 lignes, 39 valeurs, dernière date 10-07-2026, 65 jours de semaine du 13-07 au 09-10-2026) ont
          été mesurés à part, sans le module, le 11-10-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        g = M.lire(DEPOT, "donnees/cac40_ohlcv.csv", FIN[CM])
        n = M.lire(DEPOT, "donnees/claude_cours_nouveaux.csv", FIN[CM])
        six = [",".join(x.split(",")[:6]) for x in maitre]
        refuse = leve(M.lire, racine(tmp, "l26", cours=six), CM, FIN[CM]) == "ValueError"
        return (sum(len(b) for b in g["barres"].values()) == 25116 and len(g["barres"]) == 39
                and not g["source_ecrite"] and M.trous_de_tout_le_marche(g) == []
                and g["au_dela_du_fige"] == FIN[CM] and g["fin"] == D("2026-07-10")
                and M.resume(g)[1] == 1 and any(x.startswith("  AU-DELÀ DU FICHIER FIGÉ") for x in M.resume(g)[0])
                and M.dernieres_seances(g, "DG", 14, FIN[CM])[-1][0] == D("2026-07-10")
                and all(x[1] for x in M.dernieres_seances(g, "DG", 14, FIN[CM]))
                and not n["source_ecrite"] and n["barres"] and refuse)
    essai("L26 la référence Google et l'arrivée du soir, à sept colonnes, se lisent ; six colonnes : refus", l26)

    def l27():
        """Un fichier déclaré figé se lit, sans date, jusqu'à sa dernière date ; le même contenu non déclaré, non.

        ① RÔLE — L27.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — donnees/cac40_ohlcv.csv tel qu'au 11-10-2026 (figé : on ne le touche jamais).
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — lire la référence Google sans date ; puis son contenu exact posé à la place du maître, puis sous
          autre/cac40_ohlcv.csv ; puis la référence amputée de ses dix dernières séances (29-06 au 10-07-2026) à sa
          place déclarée ; le témoin du golden ; l'arrivée du soir ; la référence allongée d'une séance — chacun lu sans
          date.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Relecture de Cowork du 12-10-2026 (108efa5) : lue par le module, la référence sortait 65 « trous de
          tout le marché ». Figé se déclare, il ne se déduit pas : posé sous le nom du maître, le même contenu a l'allure
          d'une collecte tombée pour tout le monde, qui doit crier. Relecture indépendante du 12-10-2026 : déclaré par son
          seul nom, le figé faisait taire une copie posée ailleurs ; fini à sa dernière date lue, une référence tronquée
          se taisait aussi.
        ⑨ CE QUI CLOCHE — La seconde lecture prend la veille à l'horloge : elle compte au moins les 65 séances du 13-07 au
          09-10-2026, et davantage chaque jour.
        ⑩ EFFET — Écrit une racine jetable.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        g = M.lire(DEPOT, "donnees/cac40_ohlcv.csv")
        with open(os.path.join(DEPOT, "donnees", "cac40_ohlcv.csv"), encoding="utf-8") as f:
            ref = f.read().splitlines()
        h = M.lire(racine(tmp, "l27", cours=ref), CM)
        r2 = racine(tmp, "l27b")
        os.makedirs(os.path.join(r2, "autre"))
        coupe = ref[:1] + [x for x in ref[1:] if x.split(",")[1] < "2026-06-29"]
        plus = ref + [x.replace(",2026-07-10,", ",2026-07-13,") for x in ref if ",2026-07-10," in x]
        os.makedirs(os.path.join(r2, "plus", "donnees"))
        for chemin, lignes in (("autre/cac40_ohlcv.csv", ref), ("donnees/cac40_ohlcv.csv", coupe),
                               ("plus/donnees/cac40_ohlcv.csv", plus)):
            with open(os.path.join(r2, chemin), "w", encoding="utf-8") as f:
                f.write("\n".join(lignes) + "\n")
        ailleurs = M.lire(r2, "autre/cac40_ohlcv.csv")
        tronque = M.lire(r2, "donnees/cac40_ohlcv.csv")
        temoin = M.lire(DEPOT, "temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv")
        r3 = os.path.join(r2, "plus")
        for x in ("donnees/sources_indice", "donnees/CALENDRIER_EURONEXT.csv", "donnees/NATURE_DES_TROUS.csv"):
            shutil.copytree(os.path.join(r2, x), os.path.join(r3, x)) if os.path.isdir(os.path.join(r2, x)) \
                else shutil.copy(os.path.join(r2, x), os.path.join(r3, x))
        for x in glob.glob(os.path.join(r2, "donnees", "REFERENTIEL_VALEURS_*.csv")):
            shutil.copy(x, os.path.join(r3, "donnees"))
        allonge = M.lire(r3, "donnees/cac40_ohlcv.csv")
        r4 = os.path.join(r2, "milieu")
        shutil.copytree(r3, r4)
        vinci = [i for i, x in enumerate(ref) if x.startswith("VINCI,2025-03-03,")]
        milieu = list(ref)
        c = milieu[vinci[0]].split(",")
        c[5] = f"{float(c[5]) * 1.10:.4f}"
        milieu[vinci[0]] = ",".join(c)
        with open(os.path.join(r4, "donnees", "cac40_ohlcv.csv"), "w", encoding="utf-8") as f:
            f.write("\n".join(milieu) + "\n")
        change = M.lire(r4, "donnees/cac40_ohlcv.csv")
        dit_change = any(x.startswith("  FICHIER FIGÉ MODIFIÉ") for x in M.resume(change)[0])
        dit = any(x.startswith("  FICHIER FIGÉ ALLONGÉ : 1 date(s)") for x in M.resume(allonge)[0])
        soir = M.lire(DEPOT, "donnees/claude_cours_nouveaux.csv")
        return (g["fige"] and g["fin"] == D("2026-07-10") and M.trous_de_tout_le_marche(g) == []
                and not h["fige"] and len(M.trous_de_tout_le_marche(h)) >= 65
                and not ailleurs["fige"] and len(M.trous_de_tout_le_marche(ailleurs)) >= 65
                and tronque["fige"] and len(M.trous_de_tout_le_marche(tronque)) == 10
                and temoin["fige"] and M.trous_de_tout_le_marche(temoin) == [] and not soir["fige"]
                and allonge["fige_allonge"] == [D("2026-07-13")] and dit and not g["fige_allonge"]
                and len(vinci) == 1 and change["fige_modifie"] and dit_change and not g["fige_modifie"]
                and M.resume(change)[1] == 1 and M.resume(g)[1] == 0)
    essai("L27 la référence Google, déclarée figée, se lit sans date jusqu'au 10-07-2026 ; son contenu sous le nom du "
          "maître sort ses trous", l27)
    def meme_increment():
        """Dit si l'incrément que déclare CONTRATS est bien celui qu'écrit le circuit du soir.

        ① RÔLE — Tenir ensemble deux écritures d'un même chemin (R-708 : deux implémentations divergent toujours).
        ② CONTEXTE D'APPEL — L28.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — programmes/TENIR_L_HISTORIQUE.py porte une affectation `INCREMENT = os.path.join(…)` de
          textes.
        ⑤ SORTIE — UNE valeur : vrai si le chemin de TENIR_L_HISTORIQUE est dans CONTRATS.FICHIERS_DE_COURS_INCREMENTS.
          [rend: 1]
        ⑥ TRAITEMENT — lire l'arbre syntaxique de TENIR_L_HISTORIQUE (sans l'importer : il tire la collecte), y trouver
          INCREMENT, joindre ses morceaux par « / ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture indépendante du 12-10-2026 : si la collecte renomme l'incrément, le lecteur le traitera
          comme un historique et les 420 faux trous reviendront.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit un fichier.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        import ast
        with open(os.path.join(DEPOT, "programmes", "TENIR_L_HISTORIQUE.py"), encoding="utf-8") as f:
            arbre = ast.parse(f.read())
        for n in ast.walk(arbre):
            if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "INCREMENT" for t in n.targets):
                return "/".join(a.value for a in n.value.args) in M.CONTRATS.FICHIERS_DE_COURS_INCREMENTS
        return False

    def l28():
        """Une valeur dans l'indice avant sa première barre a ses trous ; Peugeot ne prête pas ses années à Stellantis.

        ① RÔLE — L28.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — L'historique réparé, le maître et les deux tables de la règle I-3 tels qu'au
          12-10-2026.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — lire l'historique réparé jusqu'au 02-10-2026 ; compter les trous d'AIR, STMPA, URW, STLAP et HO hors
          trous de tout le marché ; lire le maître ; puis cinq tables fausses, chacune doit être refusée (deux noms
          d'aujourd'hui, un mnémonique pour deux sociétés, la table des passages absente, STMPA renommé STM, le code
          d'Air Liquide sous Stellantis, les lignes d'Air Liquide retirées) ; trois sociétés sorties (Vivendi, et deux
          dont le code reste à trouver) sont admises, et un passage sans code n'est prêté à aucune des deux ; un passage d'Air Liquide fermé au 31-12-2026, après la fin du maître, ne
          donne aucun trou après cette fin ; l'arrivée du soir, déclarée incrément, n'a aucun trou avant la première
          barre de chaque valeur.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Cassure B de Cowork (11-10-2026, e183c98), décision de Jean-Luc A8 du 10-10-2026 et du 12-10-2026
          (« Oui, clore et passer à B »). Réponses venues d'ailleurs que du module : Airbus est dans l'indice sous EADS
          depuis le 10-07-2000 (avis 2000-2926), STMicroelectronics depuis le 03-01-2000 (composition de bnains),
          Unibail depuis le 18-06-2007 ; leurs premières barres (03-09-2001, 03-09-2001, 14-04-2023) et les séances
          d'avant (292, 423, 4 054) ont été comptées par Cowork le 11-10-2026, hors du module ; pour Unibail, 4 054
          moins les 5 trous de tout le marché tombés dans la période = 4 049. Thales : première barre le 04-01-2000,
          dans l'indice le 03-01-2000 — un trou.
        ⑨ CE QUI CLOCHE — Les comptes portent sur les fichiers du 12-10-2026.
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        h = lire_reel(H)
        marche = set(M.trous_de_tout_le_marche(h))
        hors = lambda m: [d for d, _ in M.trous(h, m) if d not in marche]
        air, stm, urw = hors("AIR"), hors("STMPA"), hors("URW")
        c = lire_reel(CM)
        maitre_avant = [d for m in c["hors_univers"] for d, _ in M.trous(c, m) if d < c["debut"]]
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv"), encoding="utf-8") as f:
            ident = f.read().splitlines()
        deux_actuels = ident + [x for x in ident if x.startswith("2,")]
        meme_mnemo = ident + ["99,Fausse,,,Fausse,AI,FR0000121501,épreuve : le code de Peugeot S.A. qui a des passages"
                              ",épreuve"]
        refus = [leve(M.lire, racine(tmp, "l28_" + n, identites=t), CM, FIN[CM]) for n, t in
                 (("a", deux_actuels), ("b", meme_mnemo))]
        sans = racine(tmp, "l28_c")
        os.remove(os.path.join(sans, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"))
        refus.append(leve(M.lire, sans, CM, FIN[CM]))
        renomme = [x.replace(",STMPA,", ",STM,") if x.startswith("34,") and ",STMPA," in x else x for x in ident]
        sans_air_liquide = [x for x in ident if not x.startswith("2,")]
        sortie = ident + ["41,Vivendi,,,Vivendi,VIV,FR0000127771,épreuve,épreuve", "42,Gemalto,,,Gemalto,GTO,,épreuve,épreuve",
                          "43,Alcatel,,,Alcatel,ALU,,épreuve,épreuve"]
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"), encoding="utf-8") as f:
            pas_vide = f.read().splitlines() + [",Passage sans code,2001-01-02,2001-06-29,épreuve,épreuve"]
        admis = M.lire(racine(tmp, "l28_g", identites=sortie, passages=pas_vide), CM, FIN[CM])
        partage = ident + ["33,Stellantis,2021-01-18,2021-01-18,Faux,FAUX,FR0000120073,épreuve,épreuve"]
        refus += [leve(M.lire, racine(tmp, "l28_" + n, identites=t), CM, FIN[CM]) for n, t in
                  (("d", renomme), ("e", partage), ("h", sans_air_liquide))]
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"), encoding="utf-8") as f:
            pas = f.read().splitlines()
        borne = [x.replace("FR0000120073,AIR LIQUIDE,2000-01-03,,", "FR0000120073,AIR LIQUIDE,2000-01-03,2026-12-31,")
                 for x in pas]
        b = M.lire(racine(tmp, "l28_f", passages=borne), CM, FIN[CM])
        soir = M.lire(DEPOT, "donnees/claude_cours_nouveaux.csv", FIN[CM])
        avant_la_premiere = [(m, d) for m in soir["hors_univers"] for d, _ in M.trous(soir, m)
                             if soir["barres"].get(m) and d < min(soir["barres"][m])]
        return (len(air) == 292 and air[0] == D("2000-07-10") and air[-1] == D("2001-08-31")
                and len(stm) == 423 and stm[0] == D("2000-01-03") and stm[-1] == D("2001-08-31")
                and len(urw) == 4054 and urw[0] == D("2007-06-18") and urw[-1] == D("2023-04-13")
                and hors("STLAP") == [] and hors("HO") == [D("2000-01-03")] and M.trous(h, "MT") == []
                and maitre_avant == [] and refus[0] == "ValueError" and refus[1] == "ValueError"
                and refus[2] in ("FileNotFoundError", "OSError", "ValueError") and refus[3] == "ValueError"
                and refus[4] == "ValueError" and refus[5] == "ValueError" and admis["dans_l_indice"].get("VIV")
                and admis["dans_l_indice"].get("GTO") == [] and admis["dans_l_indice"].get("ALU") == []
                and M.trous(b, "AI") == [] and avant_la_premiere == [] and meme_increment()
                and len(borne) == len(pas) and borne != pas)
    essai("L28 avant sa première barre, une valeur dans l'indice a ses trous (AIR 292, STMPA 423, URW 4 054, HO 1) ; "
          "Stellantis n'hérite pas de Peugeot ; tables fausses refusées", l28)
    def l29():
        """Une valeur de l'univers sortie de l'indice reste attendue jusqu'à la fin du fichier.

        ① RÔLE — L29.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le maître et la table des passages tels qu'au 12-10-2026.
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — une table des passages où Accor et Vinci sortent de l'indice le 29-12-2023, avant la première
          date du maître (02-01-2024) ; Accor sans ses deux dernières séances : deux trous ; Vinci absent : 709 trous,
          dit ABSENTE.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Relecture du banc du 12-10-2026 (pièce B) : depuis que les séances dans l'indice sont attendues,
          L13 et L18 ne mordaient plus sur `_periode` (S15, S28) — Accor et Vinci, dans l'indice jusqu'à la fin, étaient
          attendus par l'indice de toute façon. Une valeur de l'univers est collectée qu'elle soit dans l'indice ou non :
          son absence reste un trou.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"), encoding="utf-8") as f:
            pas = f.read().splitlines()
        sortis = [x.replace("FR0000125486,Vinci,2002-04-03,,", "FR0000125486,Vinci,2002-04-03,2023-12-29,")
                  for x in pas if not x.startswith("FR0000120404,ACCOR,2024-03-18,")]
        sortis = [x.replace("FR0000120404,ACCOR,2000-01-03,2020-09-18,", "FR0000120404,ACCOR,2000-01-03,2023-12-29,")
                  for x in sortis]
        sans_ac = [x for x in maitre if not x.startswith(("ACCOR,2026-10-08,", "ACCOR,2026-10-09,"))]
        a = M.lire(racine(tmp, "l29a", cours=sans_ac, passages=sortis), CM, FIN[CM])
        v = M.lire(racine(tmp, "l29b", cours=[x for x in une if not x.startswith(("VINCI,", "ARCELORMITTAL,"))],
                          indice=indice_long, passages=sortis), CM, FIN[CM])
        return (len(sortis) == len(pas) - 1
                and M.trous(a, "AC") == [(D("2026-10-08"), M.NON_DECIDEE), (D("2026-10-09"), M.NON_DECIDEE)]
                and len(M.trous(v, "DG")) == 709 and any(x.startswith("  ABSENTE DU FICHIER DG : 709")
                                                          for x in M.resume(v)[0]))
    essai("L29 Accor et Vinci sortis de l'indice avant le maître : Accor sans ses deux dernières séances a deux trous ; "
          "Vinci absent, 709", l29)
    def l30():
        """Une table des passages à l'envers ou qui se chevauche est refusée, avec sa raison.

        ① RÔLE — L30.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — La table des passages telle qu'au 12-10-2026 (EADS : 2000-07-10, sans fin ; Air Liquide :
          2000-01-03, sans fin ; Edenred, code FR0010908533 absent des identités : 2010-07-02 → 2010-07-02 et 2023-06-19
          → 2025-12-19).
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — des tables refusées, chacune avec sa raison : ① la sortie d'EADS mise au 1999-07-09, avant son
          entrée (cas de Cowork) ; ② un second passage d'Air Liquide, du 2010-01-04 au 2011-01-03, pris dans son
          passage ouvert depuis 2000 ; ③ un passage d'une société inconnue des identités, à l'envers ; ④ un passage
          d'Edenred (code inconnu des identités) du 2024-01-02 au 2024-06-28, pris dans son passage fermé du 2023-06-19
          au 2025-12-19 ; ⑤ un passage d'Edenred qui entre le 2025-12-19, le jour même de sa sortie ; ⑥ une date
          illisible (2000-7-10), dite avec son passage. Et une table admise : la vraie, lignes dans l'ordre inverse,
          rend les mêmes passages que la vraie.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture de Cowork du 12-10-2026 (9c882a6, cassure G) : la table à l'envers passait, les 292 trous
          d'Airbus disparaissaient, le total tombait de 14 à 13 et rien ne disait pourquoi. Relecture indépendante du
          même soir : sans ④, ⑤ et l'ordre inverse, retirer le chevauchement entre passages fermés, la frontière du
          même jour ou le tri laissait L30 verte (X1, X2, X4) ; et un code inconnu des identités (47 passages de la
          vraie table) n'avait aucune garde (C2).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"), encoding="utf-8") as f:
            pas = f.read().splitlines()
        envers = [x.replace("NL0000235190,EADS,2000-07-10,,", "NL0000235190,EADS,2000-07-10,1999-07-09,") for x in pas]
        chevauche = pas + ["FR0000120073,AIR LIQUIDE,2010-01-04,2011-01-03,épreuve,épreuve"]
        inconnu = pas + ["FR0000000002,Société inconnue,2005-01-03,2004-01-02,épreuve,épreuve"]   # code bien formé (L31)
        fermes = pas + ["FR0010908533,Edenred,2024-01-02,2024-06-28,épreuve,épreuve"]
        meme_jour = pas + ["FR0010908533,Edenred,2025-12-19,2026-01-30,épreuve,épreuve"]
        illisible = [x.replace("NL0000235190,EADS,2000-07-10,,", "NL0000235190,EADS,2000-7-10,,") for x in pas]
        r = [raison(M.lire, racine(tmp, "l30" + n, passages=t), CM, FIN[CM])
             for n, t in (("a", envers), ("b", chevauche), ("c", inconnu), ("d", fermes), ("e", meme_jour),
                          ("f", illisible))]
        inverse = pas[:1] + pas[:0:-1]
        meme = (M.lire_les_passages(racine(tmp, "l30g", passages=inverse))
                == M.lire_les_passages(racine(tmp, "l30h")))
        return (envers != pas and len(envers) == len(pas) and illisible != pas and inverse != pas and meme
                and r[0] is not None and "sort de l'indice le 1999-07-09 avant d'y entrer le 2000-07-10" in r[0]
                and r[1] is not None and "deux passages du code FR0000120073 se chevauchent" in r[1]
                and r[2] is not None and "Société inconnue" in r[2] and "avant d'y entrer" in r[2]
                and r[3] is not None and "deux passages du code FR0010908533 se chevauchent (2023-06-19" in r[3]
                and r[4] is not None and "(2023-06-19 → 2025-12-19 et 2025-12-19" in r[4]
                and r[5] is not None and "date illisible pour EADS" in r[5] and "2000-7-10" in r[5])
    essai("L30 table des passages à l'envers (EADS, cas de Cowork), qui se chevauche (Air Liquide, Edenred) ou à la "
          "date illisible : refusée, avec sa raison ; l'ordre des lignes ne change rien", l30)
    def l31():
        """Un code ISIN mal écrit, dans l'une ou l'autre table, est refusé avec sa raison.

        ① RÔLE — L31.
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Les deux tables telles qu'au 13-10-2026 (STMicroelectronics : NL0000226223, deux
          passages ; Accor : FR0000120404 aux identités).
        ⑤ SORTIE — UNE valeur : vrai si verte.
          [rend: 1]
        ⑥ TRAITEMENT — ① la clé : vraie sur Accor (FR0000120404), Apple (US0378331005, exemple de la norme), Stellantis
          (NL00150001Q9, une lettre dans le code) ; fausse au dernier chiffre changé · ② refusés, avec leur raison : le
          premier passage de STMicroelectronics avec une espace après son code (cas de Cowork), puis en minuscules ;
          le code d'Accor aux identités, clé fausse (FR0000120405) · ③ les vraies tables passent (les autres épreuves
          lisent les vraies).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture de Cowork du 13-10-2026 (15e647c, cassure H) : un code mal écrit détachait un passage
          de sa société, et les 423 trous de STMicroelectronics disparaissaient sans un mot.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"), encoding="utf-8") as f:
            pas = f.read().splitlines()
        with open(os.path.join(DEPOT, "donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv"), encoding="utf-8") as f:
            ident = f.read().splitlines()
        stm = "NL0000226223,STMicroelectronics (Ex-SGS Thomson Microelectronics),2000-01-03,"
        espace = [x.replace(stm, "NL0000226223 ,STMicroelectronics (Ex-SGS Thomson Microelectronics),2000-01-03,")
                  for x in pas]
        minuscule = [x.replace(stm, "nl0000226223,STMicroelectronics (Ex-SGS Thomson Microelectronics),2000-01-03,")
                     for x in pas]
        cle = [x.replace(",AC,FR0000120404,", ",AC,FR0000120405,") for x in ident]
        r = [raison(M.lire, racine(tmp, "l31" + n, **t), CM, FIN[CM])
             for n, t in (("a", {"passages": espace}), ("b", {"passages": minuscule}), ("c", {"identites": cle}))]
        return (espace != pas and minuscule != pas and cle != ident
                and [M.isin_valide(c) for c in ("FR0000120404", "US0378331005", "NL00150001Q9", "FR0000120405",
                                                 "US0378331006", "NL00150001Q8")] == [True] * 3 + [False] * 3
                and r[0] is not None and "code ISIN mal écrit « NL0000226223  »" in r[0]
                and r[1] is not None and "code ISIN mal écrit « nl0000226223 »" in r[1]
                and r[2] is not None and "IDENTITES_DES_SOCIETES.csv : code ISIN mal écrit « FR0000120405 »" in r[2])
    essai("L31 code ISIN mal écrit — une espace, des minuscules (STMicroelectronics, cas de Cowork), une clé fausse "
          "(Accor) : refusé, avec sa raison", l31)

    def l32():
        """`lignes_mises_a_part` : 0 sur les deux vrais fichiers ; une ligne de chaque sorte écartée la compte une fois.

        ① RÔLE — L32 (ajoutée le 27-10-2026 : le juge des stratégies refuse de juger sur une lecture qui a écarté des
          lignes, et c'est cette fonction qui le dit, par conservation).
        ② CONTEXTE D'APPEL — `essai`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le dépôt porte le fichier maître et l'historique réparé.
        ⑤ SORTIE — UNE valeur : vrai si chaque compte est juste.
          [rend: 1]
        ⑥ TRAITEMENT — ① les deux vrais fichiers : 0 · ② le maître plus une ligne d'un nom inconnu, puis d'une date
          illisible (« 26/10/2026 », le cas de la relecture), puis d'un samedi : 1 chaque fois · ③ un doublon exact : 0.
        ⑦ UNITÉ — Des lignes.
        ⑧ POURQUOI — Une propriété, pas une liste : chaque sorte d'écart manque à l'égalité.
        ⑨ CE QUI CLOCHE — Le conflit (deux lignes différentes pour une séance) n'a pas de cas ici.
        ⑩ EFFET — Écrit des racines jetables.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if M.lignes_mises_a_part(lire_reel(H)) or M.lignes_mises_a_part(lire_reel(CM)):
            return False
        vraies = lignes_de(CM)
        derniere = vraies[-1]
        comptes = []
        for n, l in (("inconnu", "SOCIETE INVENTEE,2026-10-08,1,1,1,1,1,abc"), ("illisible", "VINCI,26/10/2026,1,1,1,1,1,abc"),
                     ("samedi", "VINCI,2026-10-03,1,1,1,1,1,abc"), ("doublon", derniere)):
            comptes.append(M.lignes_mises_a_part(M.lire(racine(tmp, "l32_" + n, cours=vraies + [l]), CM, FIN[CM])))
        return comptes == [1, 1, 1, 0]
    essai("L32 lignes mises à part : 0 sur les vrais fichiers ; un nom inconnu, une date illisible, un samedi : 1 ; "
          "un doublon exact : 0", l32)
    return res


def main():
    """Joue Z0, puis chaque sabotage avec --saboter, et rend le code de sortie.

    ① RÔLE — Le chef d'orchestre.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie (0, 1 ou 2).
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque sabotage : copier les programmes, appliquer, jouer, afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit et efface un dossier jetable ; affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    saboter = "--saboter" in sys.argv
    seulement = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--seulement=")]
    code = 0
    tmp = tempfile.mkdtemp(prefix="epreuves_lecture_")
    try:
        for nom, subs in SABOTAGES.items():
            if nom != "Z0" and not saboter:
                continue
            if seulement and nom != "Z0" and not any(nom.startswith(x + "_") for x in seulement[0]):
                continue
            dossier = os.path.join(tmp, "prog_" + nom)
            os.makedirs(dossier)
            for p in PROGRAMMES:
                shutil.copy(os.path.join(DEPOT, "programmes", p), dossier)
            ok = True
            for fichier, ancien, nouveau in subs:
                chemin = os.path.join(dossier, fichier)
                s = open(chemin, encoding="utf-8").read()
                if s.count(ancien) != 1:
                    print(f"SABOTAGE {nom} INAPPLICABLE : ancre absente ou multiple dans {fichier}")
                    ok = False
                    break
                open(chemin, "w", encoding="utf-8").write(s.replace(ancien, nouveau))
            if not ok:
                code = 2
                continue
            res = epreuves(dossier, os.path.join(tmp, "t_" + nom))
            shutil.rmtree(dossier, ignore_errors=True)
            shutil.rmtree(os.path.join(tmp, "t_" + nom), ignore_errors=True)
            pannes = [n for n, v in res if v is None]
            if pannes:
                print(f"== {nom} : NON JUGÉ — l'environnement a manqué (disque, mémoire) : " + pannes[0])
                code = 2
                continue
            rouges = [n for n, v in res if not v]
            print(f"== {nom} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
            for n in rouges:
                print("     ROUGE " + n)
            if nom == "Z0" and rouges:
                code = max(code, 1)
            if nom != "Z0" and not rouges:
                print(f"     SABOTAGE {nom} SANS EFFET : aucune épreuve ne rougit")
                code = max(code, 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("VERDICT : " + ("tout est conforme" if code == 0 else f"NON CONFORME (code {code})"))
    return code


if __name__ == "__main__":
    sys.exit(main())
