#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py — Ven 20-11-2026 (Paris). EN ESSAI · épreuve. Simulation
uniquement : aucun ordre réel.

LE SENS EN TÊTE. Décision de Jean-Luc du 19-11-2026 à 19h09 (BACKLOG A-923, réponse « 1 ») : faire passer N'IMPORTE
QUELLE stratégie dans tout le circuit, en éprouvant des PROPRIÉTÉS sur des stratégies factices plutôt qu'une stratégie
à la fois (étude etudes/ETUDE_CONTRAT_DE_STRATEGIE_ET_PROPRIETES_2026-11-19_19h16.md, sections B et C, étape 2 du plan
D). Décision de Jean-Luc du 20-11-2026 à 12h45 (BACKLOG A-941, réponse « 1 ») : l'épreuve se joue SUR GITHUB (deux
copies du dépôt avaient été refusées sur la machine du Chat), et les maillons ② JOUER, ③ TRIER, ④ juge restent
BLOQUÉS : ils sont nommés « non joués, décision de Jean-Luc », jamais comptés verts. Décision de Jean-Luc du
20-11-2026 à 17h53 (BACKLOG A-945, réponse « 1 » à « Faire tourner la suite sur 2024 et après uniquement, en étalonnant
sur ces années-là ») : la SUITE de la chaîne — ② le juge, ③ les positions, ④ la mesure — tourne et s'étalonne sur 2024
et après, et 2000-2023 n'est jamais lu, même pas les dates. Elle se joue avec l'option « --suite-seule ». Jean-Luc,
le 20-11-2026 à 20h58 : « je vois pas la partie Moulinette… vérifie tout à fond » : l'option « --bout-en-bout » fait
passer une fiche factice par les PROGRAMMES EN LIGNE DE COMMANDE, moulinette par programmes/ENCHAINER_LA_MOULINETTE.py
puis le soir, sur un dépôt fabriqué de 2024-2025, et nomme chaque maillon qui ne peut pas tourner sans lire d'avant 2024.

Ce que l'épreuve joue, sur des COPIES faites sous un dossier temporaire de la machine qui la lance :
  · la COUCHE EN MÉMOIRE : le contrat de stratégie (`manques_du_contrat`) et `jouer` du juge, sur des cours FABRIQUÉS
    aux séances réelles 2024-2025 (jamais 2000-2023 : aucun regard, R-505 ③) ;
  · les maillons ⓪ PREPARER et ① DECLINER, par programmes/ENCHAINER_LA_MOULINETTE.py, comme la chaîne officielle ;
  · le SOIR : programmes/DETECTER_LES_SIGNAUX_GITHUB.py puis programmes/TENIR_LES_POSITIONS.py, sur une copie entière
    (cours réels du cours maître), avec deux fiches factices à l'état QA.
  · AVEC « --suite-seule », et seulement elle : la SUITE, en mémoire, sur un dépôt FABRIQUÉ R (liens vers programmes/
    et vers trois fichiers de réglages, jamais une copie ; référentiel, valeurs taxées, registre et cours fabriqués,
    2024-2025) — ② le juge (contrat, porte, `jouer`, `juger`, grille de R-505), ③ le teneur (`tenir`, séance par
    séance), ④ la mesure (`mesurer_une_strategie`). Une garde d'audit y refuse toute lecture du dépôt réel.
  · AVEC « --bout-en-bout », et seulement elle : sur un dépôt FABRIQUÉ R (liens DURS vers programmes/, données de
    2024-2025 fabriquées : cours maître, indice, composition, calendrier), la fiche PROP-BEB passe ⓪ ① ② ③ ④ par
    l'enchaîneur, puis quatorze soirs (versement, contrôle des valeurs, détecteur, teneur), puis le cockpit, la mesure,
    le pilote et le radar, chacun en ligne de commande et sous une garde A-945 posée dans CHAQUE processus
    (sitecustomize) ; PROP-BEB-X, fautive, doit être refusée à ⓪. Un maillon bloqué par une lecture d'avant 2024 écrite
    dans son programme est NON JOUÉ, motif nommé (BLOCAGES_CONNUS) : jamais vert.
Les stratégies factices sortent d'un générateur à graine fixe (Python standard, aucun paquet nouveau) : les limites
de l'étude une par une sur une fiche ordinaire, plus des fiches tirées au hasard. Leur module de signal factice est
écrit dans la copie, jamais au dépôt.

LES PROPRIÉTÉS (étude, tableau B) — P1 rien ne plante sur une fiche conforme · P2 une fiche non conforme est refusée,
sa case nommée · P3 chaque maillon ⓪ ① laisse sa preuve (journal de la chaîne, témoins intacts) · P4 le soir n'achète
que ce que la fiche permet (univers, seuils de SA fiche, un jeton) · SIL aucune fiche conforme suivie n'est ignorée en
silence par le soir · P5 le gain écrit se retrouve (vente rejouée par MODULE_POSITIONS.vendre) · P6 aucun signal ne lit
une séance future · P7 même entrée, même résultat · P8 les limites sont tenues (jamais → 0 opération, rien sur la
dernière séance, rien hors période, horizon 1 tenu).
LA SUITE (« --suite-seule ») — A945 rien n'est lu dans le dépôt réel · ETA l'étalonnage sur QUINZE CAS CONNUS aux
résultats écrits d'avance (CAS_CONNUS : stop, objectif, double touche R-602, sauts R-607 ① ② ③, échéance, séance
manquante R-112, valeur taxée et non taxée, vente le jour de l'achat, une vraie ligne du journal R-732, et les quatre
seuils touchés PILE — plus haut, plus bas, ouverture au stop, ouverture à l'objectif, K12 à K15), plus le témoin
`_c5e10_sortie` (concorde sans saut, diverge comme documenté avec saut) · JUG le juge rend un verdict du contrat ou un
refus motivé, jamais une exception · POS le teneur rend les cas connus ; sur les cours fabriqués, les positions
respectent tp, sl et horizon de la fiche et chaque sortie est la première séance qui touche un seuil · GAIN la mesure
rend les cas connus, égale la somme des gains écrits, et les frais implicites restent dans leurs bornes · PREUVE chaque
maillon ② ③ ④ laisse sa preuve · ACC les cours fabriqués portent chaque accident (saut bas, saut haut, double touche,
trou), le soir sort en SL_GAP et en TP_GAP, et des POSITIONS traversent les accidents : au moins une sort sur une
double touche accidentée, au moins une a une fenêtre qui enjambe un trou. AUCUNE de ces propriétés n'appelle `vendre`, `frais_aller_retour` ni
`prix_de_convention` (réparation du 20-11-2026, superviseur R-759 : « RUSTINE, À REPRENDRE » pour un oracle réécrit).
Un cas connu dont le code n'applique pas encore la règle (K07, R-112) est un ÉCART CONNU : nommé, jamais vert.

USAGE
    python3 -B tests/EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py <racine> [--saboter]
    python3 -B tests/EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py <racine> --suite-seule [--saboter]
                [--seulement=S-ETA,S-JUG]
    python3 -B tests/EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py <racine> --bout-en-bout [--saboter]
    <racine> : la racine d'une copie du dépôt (sur GitHub, la copie du circuit des épreuves longues), jamais modifiée.

① RÔLE — Mesurer les propriétés P1 à P8 et SIL, et dresser la liste des maillons où une stratégie CONFORME au contrat
  est REFUSÉE ou IGNORÉE.
② CONTEXTE D'APPEL — Le circuit des épreuves longues sur GitHub (codes ProprietesChaine et ProprietesSabot de
  tests/LANCEMENT_DES_EPREUVES.json), décision A-941. À la main ailleurs que sur la machine du Chat.
③ ENTRÉE — La ligne de commande (USAGE). Appels internes : « --couche <W> », « --chaine <W> [--octet] », « --soir <S> »,
  « --suite <R> <racine> », « --beb <R> <racine> [<sabotage>] ». « --seulement=S-ETA,… » limite les sabotages de la suite (tranches à la main).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/, donnees/ (registre des stratégies avec la ligne C5E10-QA-V1,
  référentiel, VALEURS_TTF.csv, calendrier, cours maître) et donnees/combinatoires/VOISINAGE.csv.
⑤ SORTIE — UNE valeur, le code : 0 toutes les propriétés VERTES (et, avec --saboter, chaque sabotage fait rougir SA
  propriété) · 1 une propriété ROUGE ou NON MESURÉE, ou un sabotage qui ne mord pas · 2 l'épreuve n'a pas pu tourner
  (R-734). Affiche le tableau propriété × verdict et la liste des refus et des silences sur fiche conforme. [rend: 1]
⑥ TRAITEMENT — Pour le passage sans sabotage, puis pour chaque sabotage : ① copie W (programmes, fichiers de données
  utiles) et copie S (le dépôt entier sans .git, etudes, archives) · ② le sabotage posé dans les deux · ③ trois
  processus neufs : couche, chaîne, soir, chacun rend un JSON · ④ propriétés rassemblées · ⑤ copies effacées.
⑦ UNITÉ — Euros pour 100 000 € par opération ; seuils en fractions ; horizon en séances.
⑧ POURQUOI — R-731 (chaque propriété a son sabotage, une épreuve qui reste verte quand on retire ce qu'elle teste est
  une décoration) ; R-732 (la fiche modèle est la VRAIE ligne C5E10-QA-V1 du registre) ; R-734 (ce qui n'a pas tourné
  rend un code non nul, jamais vert) ; R-708 (aucune formule recopiée : dans la couche et la chaîne, les seuils, la
  vente, les frais sont demandés aux programmes du circuit ; dans la suite, l'indépendance vient des CAS CONNUS,
  littéraux posés à la main, et des propriétés écrites en inégalités — jamais une troisième vente).
⑨ CE QUI CLOCHE — ① La validation des réglages exigée par DECLINER (« Jean-Luc le JJ-MM-AAAA ») est ÉCRITE PAR
  L'ÉPREUVE dans la copie jetable, pour des fiches factices : elle ne vaut validation de rien, et ne quitte jamais la
  copie. ② La couche en mémoire joue `jouer` sans lecture du lecteur (pas de composition de l'indice ni de trous) : la
  composition n'est pas éprouvée ici. ③ Le soir est joué une fois (deux passages du teneur), sur la dernière séance du
  cours maître ; P4 exige une position OUVERTE pour chaque fiche QA dont l'univers porte le signal posé (le teneur
  se calibre lui-même et refuse de tourner sous le sabotage S-P4a : sans cette exigence, P4 ne mesurerait rien et
  resterait verte) ; « NON MESURÉE » si aucune fiche QA n'est servie. ④ P6 est mesurée sur
  un échantillon de séances (une sur trois). ⑤ Maillons ②, ③, ④ non joués (A-941). ⑥ Les fiches réelles du registre
  restent dans la copie du soir : le détecteur voit ensemble C5 et les fiches factices. ⑦ SANS « --suite-seule », LE
  MAILLON ① LIT ENCORE DES DATES ET DES COURS D'AVANT 2024 : `seances_reelles` lit l'indice CAC 40 du dépôt (depuis
  2000), le soir copie le dépôt entier (cours maître depuis 2000), `ligne_modele` lit le registre réel ; non changé
  ici (A-941, maillon ①), à trancher par Jean-Luc au regard d'A-945. ⑧ La suite : la grille de R-505 reçoit k
  « INCONNU » et aucune déclaration (verdict « NON TRANCHÉE » par construction : la propriété porte sur la FORME) ; le
  teneur tourne sans lecture du lecteur (pas de contrôle « dans le CAC 40 ») ; le calendrier fabriqué garde les jours
  fériés ; le barème des frais, la loi et le voisinage du juge sont des RÉGLAGES liés tels quels (le barème porte des
  dates de début de tarif d'avant 2024, ni cours ni séances) ; le modèle des fiches est VIDE (R-732 non tenu dans la
  suite : aucune vraie fiche, consigne du 20-11-2026). ⑨ `CONTRATS_DES_FICHIERS.manques_du_contrat` résout le chemin
  RÉEL de MODULE_POSITIONS (`realpath`) : sur un dépôt de liens, il chargeait le module du dépôt réel, et ses frais
  auraient lu les données réelles (292 ouvertures refusées par la garde, 20-11-2026) ; la suite lui passe `mod_pos`.
  JOUER_LES_VERSIONS, TRIER_LES_VARIANTES, le juge et la mesure en ligne de commande ne sont pas joués : leur
  calibrage lit le témoin du golden ou les chiffres du golden (2000-2026), sans équivalent sur 2024 et après.
  ⑩ La suite : P5 (maillon ①) rejoue encore par `vendre` et `frais_aller_retour` (`ecarts_d_une_vente`) ; les
  propriétés POS des cours fabriqués appellent encore `seuils_de_vente` pour l'objectif et le stop écrits dans la
  position (les cas connus, eux, les posent en littéral) ; l'échéance d'une fenêtre à trou n'est pas jugée sur les cours
  fabriqués (R-112 non appliquée par le code : écart connu K07) ; la mesure compte « jetons illimités » au prix de
  convention (A-330), les attendus le suivent tant que Jean-Luc n'a pas tranché (R-607, « CE QUE CETTE RÈGLE CHANGE »).
  ⑪ « --bout-en-bout » (mesuré le 20-11-2026 sur un mini dépôt fabriqué) : ② JOUER_LES_VERSIONS ne tourne pas — il
  exige du juge la phrase « calibrage sur le TEMOIN du golden » (programmes/JOUER_LES_VERSIONS.py l.762-763), écrite
  seulement avec le témoin du golden (cours depuis 2000) ; ③ et ④ ne s'atteignent donc pas par l'enchaîneur. Le
  versement lit donnees/cac40_ohlcv.csv en dur (programmes/TENIR_L_HISTORIQUE.py l.183, l.1131-1137) : la séance du
  soir est écrite au maître par l'épreuve. La mesure exige le trade Bureau Veritas du journal réel (programmes/
  MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py l.2001-2007). Le détecteur ne sert pas un module sans étalon : le
  signal du teneur est posé. Le teneur exige UNIBAIL_RODAMCO pour se calibrer et lit le référentiel sous son nom daté
  (l.3353-3354) : le dépôt fabriqué les porte. La collecte, la publication au dépôt public et la météo (réseau), la
  confrontation aux contrats et « dire les pas tombés » ne sont pas joués.
⑩ EFFET — Écrit sous un dossier temporaire, effacé à la fin ; affiche.
⑪ TERMINAISON — Chaque processus lancé est borné (couche 1 800 s, chaîne 2 400 s, soir 1 800 s, suite 1 800 s,
  bout en bout 3 600 s ; chaque programme du circuit 400 s, 900 s pour un pas de la moulinette). [sort: oui — code]
"""
import csv
import hashlib
import io
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
ICI = os.path.abspath(__file__)

REG = "donnees/cac40_strategies.csv"
TTF = "donnees/VALEURS_TTF.csv"
POS = "donnees/claude_positions_ouvertes.csv"
SIG = "donnees/signaux_du_jour.json"
COURS = "donnees/cours_maitre.csv"
CONTRATS = "programmes/CONTRATS_DES_FICHIERS.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
TENIR = "programmes/TENIR_LES_POSITIONS.py"
DET = "programmes/DETECTER_LES_SIGNAUX_GITHUB.py"
ENCH = "programmes/ENCHAINER_LA_MOULINETTE.py"
MODULE = "programmes/SIGNAL_FACTICE_DES_PROPRIETES.py"
MODELE = "C5E10-QA-V1"                 # la vraie ligne qui sert de modèle aux fiches factices (R-732)
DEBUT, FIN = "2024-01-02", "2025-12-31"
ESSAI = "E01"
GRAINE = 20261120
N_HASARD = 120                          # fiches tirées au hasard, à graine fixe
N_CHAINE_HASARD = 12                    # parmi elles, combien passent ⓪ et ①
PROPRIETES = ("P1", "P2", "P3", "P4", "SIL", "P5", "P6", "P7", "P8")
ENONCES = {
    "P1": "rien ne plante sur une fiche conforme",
    "P2": "une fiche non conforme est refusée, sa case nommée",
    "P3": "chaque maillon ⓪ ① laisse sa preuve (journal, témoins intacts)",
    "P4": "le soir n'achète que ce que la fiche permet (univers, seuils de SA fiche, un jeton)",
    "SIL": "aucune fiche conforme suivie n'est ignorée en silence par le soir",
    "P5": "le gain écrit se retrouve (vente rejouée par MODULE_POSITIONS.vendre)",
    "P6": "aucun signal ne lit une séance future",
    "P7": "même entrée, même résultat",
    "P8": "les limites sont tenues (jamais, dernière séance, période, horizon 1)",
}
NON_JOUES = ("② JOUER_LES_VERSIONS", "③ TRIER_LES_VARIANTES", "④ juge")

TEXTE_DU_MODULE = '''"""Signal factice de l'épreuve par propriétés de la chaîne (A-923, A-941) : vit dans une copie jetable, jamais au dépôt.
EN ESSAI · module de signal · Rôle : rendre des séances d'achat selon le mode réglé par la fiche (seuil de baisse, toujours, jamais, tous les k, une date, hasard à graine).
"""
import random


def signal(serie, mode="seuil", baisse=0.02, k=5, graine=7, jour=""):
    """Rend la liste des {"i": rang} des séances signalées ; aucune lecture de fichier, aucun effet."""
    n = len(serie)
    if mode == "jamais":
        return []
    if mode == "toujours":
        return [{"i": i} for i in range(n)]
    if mode == "tous_k":
        return [{"i": i} for i in range(0, n, k)]
    if mode == "date":
        return [{"i": i} for i in range(n) if str(serie[i]["date"]) == jour]
    if mode == "hasard":
        alea = random.Random(graine)
        return [{"i": i} for i in range(n) if alea.random() < 1.0 / k]
    rendu = []
    for i in range(1, n):
        if serie[i]["close"] / serie[i - 1]["close"] - 1 <= -baisse:
            rendu.append({"i": i})
    return rendu


def memoire_signal(mode="seuil", baisse=0.02, k=5, graine=7, jour=""):
    """Mémoire déclarée : une séance avant le jour J (clause 4 de l'étude, A.3)."""
    return 1
'''

# LES SABOTAGES — (nom, propriété qui DOIT rougir, fichier, [(texte avant, texte après), …]) ; fichier None : geste
# spécial (l'octet de P3). Chaque texte « avant » doit être présent UNE fois, sinon le sabotage n'est pas joué (rouge).
# CIBLE RETROUVÉE LE 20-11-2026 (passage 44796155868 : S-P4a et S-P4b « NON JOUÉ — texte à saboter présent 0 fois ») :
# le commit ae65aad03 (A-924 F3) a sorti la boucle de `reglages_des_fiches` (programmes/TENIR_LES_POSITIONS.py) du
# « if os.path.exists(p) » de `reglages_du_registre` ; la MÊME ligne — la lecture des seuils d'une fiche par le juge,
# dans la boucle sur les fiches — est passée de 16 à 12 espaces de retrait. Seul le retrait change, pas le sens :
# le teneur ignore toujours les seuils de SA fiche et prend ceux de C5.
FORCE_C5 = ('            tp, sl, _h = juge.lecture_du_soir(base, x)\n', '            tp, sl, _h = 0.04, 0.025, 20\n')
SABOTAGES = (
    ("S-P1 contrôle VALEURS_TTF neutralisé", "P1", CONTRATS,
     [('                        mod_pos.cout_d_un_ordre(c, d, "achat", mod_pos.CAPITAL, bareme=nom_du_bareme)\n',
       '                        pass\n')]),
    ("S-P2 manques_du_jeu rend []", "P2", JUGE,
     [('    manq = []\n    entree = (fiche.get("entree") or "").strip()\n',
       '    return []\n    manq = []\n    entree = (fiche.get("entree") or "").strip()\n')]),
    ("S-P3 un octet changé dans un fichier témoigné", "P3", None, "octet"),
    # LE TENEUR SE CALIBRE LUI-MÊME (`_calibrage` de programmes/TENIR_LES_POSITIONS.py lit un registre fabriqué où
    # MA200-S1 porte +5 % / -2 %) : forcé aux seuils de C5, il refuse de tourner, et aucune position factice ne s'ouvre
    # (P4a, mesuré le 20-11-2026, passage 44732420101). P4b retire AUSSI ce calibrage, pour que ce soit la comparaison
    # des seuils de P4 elle-même qui morde.
    ("S-P4a teneur forcé aux seuils de C5", "P4", TENIR, [FORCE_C5]),
    ("S-P4b teneur forcé aux seuils de C5, son calibrage retiré", "P4", TENIR,
     [FORCE_C5, ('    if not _calibrage(mod, base):\n', '    if False:\n')]),
    ("S-SIL suivie_par_le_soir rend faux", "SIL", CONTRATS,
     [('    etat = (fiche.get("etat_vie") or "").strip().upper()\n    return etat in ETATS_SUIVIS_PAR_LE_SOIR and',
       '    return False\n    etat = (fiche.get("etat_vie") or "").strip().upper()\n'
       '    return etat in ETATS_SUIVIS_PAR_LE_SOIR and')]),
    ("S-P5 vente jouée avec un autre tp", "P5", JUGE,
     [('                op = jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture, bareme, recu)\n',
       '                op = jouer_une_entree(v, serie, j, tp * 1.5, sl, h, mod_positions, lecture, bareme, recu)\n')]),
    ("S-P6 module tricheur (clôture du lendemain)", "P6", MODULE,
     [('        if serie[i]["close"] / serie[i - 1]["close"] - 1 <= -baisse:\n',
       '        if i + 1 < n and serie[i + 1]["close"] / serie[i]["close"] - 1 <= -baisse:\n')]),
    ("S-P7 tirage sans graine", "P7", MODULE,
     [('        alea = random.Random(graine)\n', '        alea = random.Random()\n')]),
    ("S-P8 filtre de période retiré du juge", "P8", JUGE,
     [('                if periode and not (periode[0] <= d_sig <= periode[1]):\n                    continue\n', '')]),
)


# ═══ OUTILS COMMUNS ═══════════════════════════════════════════════════════════════════════════════════════════════════

def lire_csv(chemin):
    """Rend (en-tête, lignes) d'un CSV dont l'en-tête est la première ligne non commentée.
    ① RÔLE — lire les fichiers de données. ② CONTEXTE D'APPEL — partout. ③ ENTRÉE — le chemin. ④ CONDITIONS D'ENTRÉE —
    le fichier existe. ⑤ SORTIE — DEUX valeurs : la liste des colonnes, la liste des lignes (dictionnaires). [rend: 2]
    ⑥ TRAITEMENT — sauter les lignes « # », DictReader. ⑦ UNITÉ — —. ⑧ POURQUOI — VALEURS_TTF.csv commence par un
    commentaire. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main ; lève OSError. [sort: non]"""
    with open(chemin, encoding="utf-8-sig", newline="") as fh:
        lignes = [l for l in fh.read().splitlines(True) if not l.startswith("#")]
    r = csv.DictReader(io.StringIO("".join(lignes)))
    return list(r.fieldnames or []), list(r)


def env_propre(racine, sortie_du_pas):
    """Rend l'environnement d'un programme du circuit lancé dans une copie (comme `lancer` de l'enchaîneur).
    ① RÔLE — qu'un programme lancé dans la copie lise la copie. ② CONTEXTE D'APPEL — `lancer`. ③ ENTRÉE — la racine
    de la copie, le fichier de sortie du pas. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : un dictionnaire.
    [rend: 1] ⑥ TRAITEMENT — retirer GITHUB_* et DEPOT_*, poser DEPOT_CAC40 et GITHUB_OUTPUT. ⑦ UNITÉ — —.
    ⑧ POURQUOI — relecteur du 19-11-2026, I4 (DEPOT_CAC40 hérité faisait lire le vrai dépôt). ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GITHUB_", "DEPOT_"))}
    env.update(DEPOT_CAC40=racine, GITHUB_OUTPUT=sortie_du_pas, PYTHONDONTWRITEBYTECODE="1")
    return env


def lancer(racine, *args, delai=400):
    """Lance `python3 -B <args>` dans `racine` ; rend (code, sortie et erreurs).
    ① RÔLE — emprunter le chemin réel, en ligne de commande. ② CONTEXTE D'APPEL — chaîne et soir. ③ ENTRÉE — la racine
    de la copie, le programme et ses arguments, un délai en secondes. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX
    valeurs : le code (124 au-delà du délai), le texte. [rend: 2] ⑥ TRAITEMENT — subprocess.run borné. ⑦ UNITÉ —
    secondes. ⑧ POURQUOI — le code et le texte font partie de ce qui est éprouvé. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — le
    programme écrit dans la copie. ⑪ TERMINAISON — rend la main dans le délai. [sort: non]"""
    so = os.path.join(racine, "_sortie_du_pas_%d" % int(time.time() * 1000))
    open(so, "w").close()
    try:
        p = subprocess.run([sys.executable, "-B"] + list(args), cwd=racine, capture_output=True, text=True,
                           timeout=delai, env=env_propre(racine, so))
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, "DÉLAI DÉPASSÉ (%d s) : %s" % (delai, str(e)[-300:])


def ajouter_au_registre(racine, fiches):
    """Ajoute les fiches factices à la fin du registre des stratégies d'une copie.
    ① RÔLE — mettre les factices là où les programmes du circuit les lisent. ② CONTEXTE D'APPEL — `fabriquer_w`,
    `fabriquer_s`. ③ ENTRÉE — la racine de la copie, une liste de dictionnaires (cases du registre). ④ CONDITIONS
    D'ENTRÉE — le registre de la copie existe, l'en-tête en première ligne. ⑤ SORTIE — Aucune. [rend: 0]
    ⑥ TRAITEMENT — DictWriter sur les colonnes de l'en-tête, en ajout. ⑦ UNITÉ — —. ⑧ POURQUOI — la dernière ligne d'un
    identifiant fait foi (n°83). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit le registre de la copie. ⑪ TERMINAISON — rend la
    main. [sort: non]"""
    chemin = os.path.join(racine, REG)
    texte = open(chemin, encoding="utf-8").read()
    entete = next(csv.reader([texte.lstrip("﻿").split("\n", 1)[0]]))
    tampon = io.StringIO()
    w = csv.DictWriter(tampon, fieldnames=entete, lineterminator="\n", extrasaction="ignore")
    for f in fiches:
        w.writerow(f)
    with open(chemin, "a", encoding="utf-8") as fh:
        fh.write(("" if texte.endswith("\n") else "\n") + tampon.getvalue())


def ligne_modele(racine):
    """Rend la DERNIÈRE ligne de C5E10-QA-V1 du registre (R-732), vidée de son état et de sa marque.
    ① RÔLE — un modèle réel pour les fiches factices. ② CONTEXTE D'APPEL — `generer`. ③ ENTRÉE — la racine.
    ④ CONDITIONS D'ENTRÉE — la ligne existe. ⑤ SORTIE — UNE valeur : un dictionnaire. [rend: 1] ⑥ TRAITEMENT — lire.
    ⑦ UNITÉ — —. ⑧ POURQUOI — R-732. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — lève LookupError si la
    ligne manque. [sort: non]"""
    _e, lignes = lire_csv(os.path.join(racine, REG))
    modeles = [l for l in lignes if l.get("id") == MODELE]
    if not modeles:
        raise LookupError("%s absente du registre" % MODELE)
    m = dict(modeles[-1])
    m.update(statut="", origine="", note="épreuve par propriétés (A-923, A-941) — FACTICE, copie jetable")
    return m


def choisir_les_valeurs(racine):
    """Rend six mnémoniques réels, connus du référentiel (hors « hors univers ») et listés dans VALEURS_TTF pour 2024
    ET 2025, triés ; le premier est la VICTIME de P1.
    ① RÔLE — l'univers des factices. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : une liste de 6 codes. [rend: 1] ⑥ TRAITEMENT — croiser les deux fichiers. ⑦ UNITÉ — —.
    ⑧ POURQUOI — étude C : un code inventé fait lever le calcul des frais. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit.
    ⑪ TERMINAISON — lève LookupError s'il y en a moins de 6. [sort: non]"""
    refs = [n for n in os.listdir(os.path.join(racine, "donnees")) if n.startswith("REFERENTIEL_VALEURS") and
            n.endswith(".csv")]
    if len(refs) != 1:
        raise LookupError("référentiel : %d fichier(s)" % len(refs))
    _e, ref = lire_csv(os.path.join(racine, "donnees", refs[0]))
    connus = {(l.get("mnemonique") or "").strip().upper() for l in ref if not (l.get("hors_univers") or "").strip()}
    _e, ttf = lire_csv(os.path.join(racine, TTF))
    par_an = {}
    for l in ttf:
        par_an.setdefault(l.get("annee"), []).append((l.get("mnemonique") or "").strip().upper())
    ok = sorted(c for c in connus if c and par_an.get("2024", []).count(c) == 1 and par_an.get("2025", []).count(c) == 1
                and c.isalnum())
    if len(ok) < 6:
        raise LookupError("moins de 6 valeurs utilisables : %s" % ok)
    return ok[:6]


def seances_reelles(racine):
    """Rend les séances réelles du calendrier entre DEBUT et FIN, en textes AAAA-MM-JJ (par le calendrier du dépôt).
    ① RÔLE — dater les cours fabriqués. ② CONTEXTE D'APPEL — `couche` (processus neuf). ③ ENTRÉE — la racine de W.
    ④ CONDITIONS D'ENTRÉE — programmes/ de W dans sys.path. ⑤ SORTIE — UNE valeur : liste. [rend: 1] ⑥ TRAITEMENT —
    CALENDRIER_DE_LA_BOURSE. ⑦ UNITÉ — séances. ⑧ POURQUOI — les frais refusent une date hors calendrier. ⑨ CE QUI
    CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
    from datetime import date
    import CALENDRIER_DE_LA_BOURSE as CAL
    sc = CAL.lire_les_seances(racine)
    return [d.isoformat() for d, _ in CAL.seances_entre(date.fromisoformat(DEBUT), date.fromisoformat(FIN), sc)]


# ═══ LE GÉNÉRATEUR DE STRATÉGIES FACTICES ═════════════════════════════════════════════════════════════════════════════

def generer(modele, valeurs, derniere):
    """Fabrique les fiches factices : la fiche ordinaire, ses limites une par une, les victimes de P1, deux fiches QA,
    puis N_HASARD fiches tirées à graine fixe.
    ① RÔLE — le générateur de l'étude (section C). ② CONTEXTE D'APPEL — `main`, une fois ; le même tirage à chaque
    passage. ③ ENTRÉE — la ligne modèle, les six codes, la dernière séance des cours fabriqués. ④ CONDITIONS D'ENTRÉE —
    —. ⑤ SORTIE — UNE valeur : la liste des fiches (dictionnaires complets, cases du registre). [rend: 1]
    ⑥ TRAITEMENT — voir le tableau C de l'étude. ⑦ UNITÉ — seuils en pourcents écrits, horizon en séances.
    ⑧ POURQUOI — toutes les limites UNE PAR UNE sur une fiche ordinaire, plus un tirage (étude C, « Combien »).
    ⑨ CE QUI CLOCHE — le tirage est en Python simple (Hypothesis n'est pas installé : décision à Jean-Luc, étude D ⑤).
    ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    victime, pool = valeurs[0], valeurs[1:]

    def fiche(ident, **cases):
        f = dict(modele)
        f.update(id=ident, nom="factice " + ident, indicateurs="factice (épreuve par propriétés)",
                 univers=",".join(pool[:3]), tp="+4.0%", sl="-2.5%", horizon="10",
                 periode="2024-03-01 -> 2025-10-31", module_signal=MODULE, fonction_signal="signal",
                 reglages_signal=json.dumps({"mode": "seuil", "baisse": 0.02}), entree="DÉFAUT",
                 donnees_demandees="cours", etat_vie="LABO")
        if "reglages" in cases:
            cases["reglages_signal"] = json.dumps(cases.pop("reglages"))
        f.update(cases)
        return f

    fiches = [fiche("PROP-ORD")]
    limites = [
        ("PROP-L01", dict(univers=pool[0])),
        ("PROP-L02", dict(univers=",".join(pool))),
        ("PROP-L03", dict(univers="%s,%s" % (pool[0], pool[0]))),
        ("PROP-L04", dict(tp="+0.01%")),
        ("PROP-L05", dict(tp="+50%")),
        ("PROP-L06", dict(tp="+150%")),
        ("PROP-L07", dict(sl="-0.01%")),
        ("PROP-L08", dict(sl="sans stop")),
        ("PROP-L09", dict(horizon="1")),
        ("PROP-L10", dict(horizon="aucune")),
        ("PROP-L11", dict(periode="2024-06-03 -> 2024-06-03", reglages={"mode": "toujours"})),
        ("PROP-L12", dict(reglages={"mode": "toujours"})),
        ("PROP-L13", dict(reglages={"mode": "jamais"})),
        ("PROP-L14", dict(reglages={"mode": "date", "jour": derniere}, periode="%s -> %s" % (DEBUT, FIN))),
        ("PROP-L15", dict(entree="Open J+1")),
        ("PROP-L16", dict(entree="OPEN_J+1")),
        ("PROP-L17", dict(reglages={"mode": "hasard", "k": 4, "graine": 11})),
        ("PROP-L18", dict(reglages={"mode": "tous_k", "k": 3})),
        ("PROP-L19", dict(horizon="7j")),
        ("PROP-L20", dict(horizon="1", reglages={"mode": "toujours"})),
    ]
    fiches += [fiche(i, **c) for i, c in limites]
    # LES VICTIMES DE P1 : la victime est retirée de VALEURS_TTF pour 2025 dans la copie W ; le contrat doit les refuser
    fiches += [fiche("PROP-V%02d" % k, univers="%s,%s" % (victime, pool[k]), reglages={"mode": "toujours"})
               for k in range(2)]
    # LES DEUX FICHES DU SOIR, à l'état QA, aux seuils différents de ceux de C5
    fiches += [fiche("PROP-Q1", etat_vie="QA", tp="+6.0%", sl="-3.0%", horizon="10", univers=",".join(pool[:3])),
               fiche("PROP-Q2", etat_vie="QA", tp="+5.5%", sl="-2.0%", horizon="7j", univers=",".join(pool[:2]),
                     reglages={"mode": "toujours"})]
    alea = random.Random(GRAINE)
    for k in range(N_HASARD):
        univ = alea.sample(pool, alea.randint(2, len(pool)))
        mode = alea.choice(("seuil", "toujours", "jamais", "tous_k", "hasard"))
        reg = {"mode": mode}
        if mode == "seuil":
            reg["baisse"] = round(alea.uniform(0.01, 0.04), 3)
        elif mode in ("tous_k", "hasard"):
            reg["k"] = alea.randint(2, 9)
            if mode == "hasard":
                reg["graine"] = alea.randint(1, 999)
        d1 = alea.randint(0, 700)
        d2 = min(729, d1 + alea.randint(0, 500))
        from datetime import date, timedelta
        p1 = (date(2024, 1, 2) + timedelta(days=d1))
        p2 = (date(2024, 1, 2) + timedelta(days=d2))
        while p1.weekday() > 4:
            p1 += timedelta(days=1)
        while p2.weekday() > 4 or p2 < p1:
            p2 += timedelta(days=1)
        if p2.isoformat() > FIN:
            p2 = date.fromisoformat(FIN)
        fiches.append(fiche(
            "PROP-H%03d" % k, univers=",".join(univ), tp="+%.1f%%" % alea.uniform(1, 10),
            sl=("sans stop" if alea.random() < 0.1 else "-%.1f%%" % alea.uniform(0.5, 5)),
            horizon=("aucune" if alea.random() < 0.05 else str(alea.randint(3, 30))),
            periode="%s -> %s" % (p1.isoformat(), p2.isoformat()), reglages=reg,
            entree=alea.choice(("DÉFAUT", "Open J+1", "OPEN_J+1"))))
    return fiches


# ═══ LA COUCHE EN MÉMOIRE (processus neuf) ════════════════════════════════════════════════════════════════════════════

MUTATIONS = (   # P2 : (case, valeur fautive) — une case à la fois sur la fiche ordinaire ; la case DOIT être nommée
    ("id", ""), ("indicateurs", ""), ("univers", ""), ("univers", "ZZZ"), ("tp", ""), ("tp", "x"), ("tp", "-4%"),
    ("sl", ""), ("sl", "+2%"), ("horizon", ""), ("horizon", "0"), ("horizon", "abc"), ("periode", ""),
    ("periode", "banane"), ("periode", "2025-06-30 -> 2024-01-02"), ("module_signal", ""),
    ("module_signal", "programmes/N_EXISTE_PAS.py"), ("fonction_signal", ""), ("fonction_signal", "fonction_absente"),
    ("reglages_signal", '{"inconnu": 1}'), ("entree", ""), ("entree", "CLOSE"), ("donnees_demandees", ""),
    ("donnees_demandees", "consensus"),
)


def cours_fabriques(valeurs, mnemo, dates, accidents=False, avant=None):
    """Fabrique, à graine fixe, une série par valeur aux séances réelles : marche au hasard bornée, et environ une
    séance sur seize une baisse de 2,5 à 4 % ; avec `accidents`, des sauts d'ouverture, des doubles touches et des trous
    de séances, à taux fixe (TAUX_ACCIDENTS).
    ① RÔLE — des cours où les signaux se déclenchent, et, pour la suite, où chaque cas difficile de la vente arrive.
    ② CONTEXTE D'APPEL — `couche` (sans accidents, inchangée) ; `suite` (avec accidents, sauf sabotage S-ACC).
    ③ ENTRÉE — les codes, la table code → nom du juge, les séances, le drapeau `accidents`, et `avant` (date « AAAA-MM-JJ »
    ou None : None partout sauf sous S-ACC2). ④ CONDITIONS D'ENTRÉE —
    chaque code est dans `mnemo`. ⑤ SORTIE — UNE valeur : {nom: [séances {date, open, high, low, close, volume}]} ; avec
    accidents, une série peut manquer des dates (jamais la première). [rend: 1] ⑥ TRAITEMENT — Random(GRAINE + rang)
    tire chaque séance comme avant (le tirage de base reste le même, accidents ou non) ; avec accidents, un second
    tirage, Random(GRAINE + 100 + rang), choisit pour chaque séance : saut d'ouverture vers le bas (ouverture 4 à 7 %
    sous la clôture de la veille), vers le haut (5 à 8 % au-dessus), double touche (plus haut 5 à 7 % au-dessus de
    l'ouverture ET plus bas 3,5 à 5 % au-dessous), trou (la séance n'est pas écrite), ou rien. Avec `avant` (une date,
    sabotage S-ACC2 seulement), doubles touches et trous ne tombent que sur les séances antérieures : ils restent dans
    les cours, hors des séances du soir rejoué. ⑦ UNITÉ — euros.
    ⑧ POURQUOI — jamais 2000-2023 (aucun regard) ; réparation du 20-11-2026, point ⑤ : sans ces accidents, les sorties
    SL_GAP, TP_GAP, la convention R-602 et les séances manquantes (R-112) n'arrivaient presque jamais dans la suite.
    ⑨ CE QUI CLOCHE — les jours fériés restent des séances ; un trou n'est pas une suspension (R-112 ②, non éprouvé) ;
    aucun prix n'est jamais PILE sur un seuil (arrondi à quatre décimales d'un tirage continu) : l'égalité ne s'éprouve
    que par les cas connus K12 à K15.
    ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    cours = {}
    for r, code in enumerate(valeurs):
        alea, c, serie = random.Random(GRAINE + r), 50.0 + 10 * r, []
        acc = random.Random(GRAINE + 100 + r)
        for k, d in enumerate(dates):
            o = c * (1 + alea.uniform(-0.003, 0.003))
            ret = -alea.uniform(0.025, 0.04) if alea.random() < 1 / 16 else alea.uniform(-0.012, 0.0125)
            cl = c * (1 + ret)
            hi, lo = max(o, cl) * (1 + alea.uniform(0, 0.006)), min(o, cl) * (1 - alea.uniform(0, 0.006))
            if accidents:
                u, genre, borne = acc.random(), None, 0.0
                for g, taux in TAUX_ACCIDENTS:
                    borne += taux
                    if u < borne:
                        genre = g
                        break
                if avant is not None and genre in ("double", "trou") and d >= avant:
                    genre = None                  # S-ACC2 : ces accidents restent hors des séances du soir rejoué
                if genre == "trou" and k > 0:
                    continue                      # la séance n'est pas écrite ; la clôture de la veille reste la base
                if genre in ("saut_bas", "saut_haut", "double"):
                    if genre == "saut_bas":
                        o = c * (1 - acc.uniform(0.04, 0.07))
                    elif genre == "saut_haut":
                        o = c * (1 + acc.uniform(0.05, 0.08))
                    cl = o * (1 + acc.uniform(-0.01, 0.01))
                    hi, lo = max(o, cl) * (1 + acc.uniform(0, 0.006)), min(o, cl) * (1 - acc.uniform(0, 0.006))
                    if genre == "double":
                        hi, lo = o * (1 + acc.uniform(0.05, 0.07)), o * (1 - acc.uniform(0.035, 0.05))
            serie.append({"date": d, "open": round(o, 4), "high": round(hi, 4), "low": round(lo, 4),
                          "close": round(cl, 4), "volume": 100000.0})
            c = cl
        cours[mnemo[code]] = serie
    return cours


def couche(W, valeurs):
    """La couche en mémoire : contrat, P1 (jouer), P2, P5, P6, P7, P8. Affiche un JSON.
    ① RÔLE — mesurer sur les modules de la copie W (intacte ou sabotée). ② CONTEXTE D'APPEL — `__main__` « --couche ».
    ③ ENTRÉE — W, les six codes. ④ CONDITIONS D'ENTRÉE — W fabriquée par `fabriquer_w`. ⑤ SORTIE — Aucune valeur ; un
    JSON {proprietes, refus, contrat} affiché en dernière ligne. [rend: 0] ⑥ TRAITEMENT — voir chaque bloc.
    ⑦ UNITÉ — euros. ⑧ POURQUOI — un processus neuf par passage : un module saboté ne survit pas au suivant.
    ⑨ CE QUI CLOCHE — `jouer` sans lecture (⑨ ② de l'en-tête). ⑩ EFFET — charge les modules de W. ⑪ TERMINAISON —
    rend la main ; le signal factice est borné par sa forme. [sort: non]"""
    sys.path.insert(0, os.path.join(W, "programmes"))
    import CONTRATS_DES_FICHIERS as CT
    import JUGE_DES_STRATEGIES as J
    mod_pos = J.charger_module(J.trouver(W, "MODULE_POSITIONS.py"), "pos_des_proprietes")
    mnemo = J.table_mnemoniques(J.trouver(W, "REFERENTIEL_VALEURS"))
    dates = seances_reelles(W)
    cours = cours_fabriques(valeurs, mnemo, dates)
    fiches = {i: f for i, f in CT.fiches_du_registre(os.path.join(W, REG)).items() if i.startswith("PROP-")}
    prop = {p: [] for p in ("P1", "P2", "P5", "P6", "P7", "P8")}       # défauts trouvés, par propriété
    mesures = {p: 0 for p in prop}                                      # nombre de mesures faites
    refus, contrat = [], {}
    conformes = []
    for i in sorted(fiches):
        try:
            m = CT.manques_du_contrat(fiches[i], W, J=J)
        except Exception as e:  # noqa: BLE001 — un contrat qui lève sur une fiche est un plantage (P1)
            prop["P1"].append("%s : le contrat lève %s: %s" % (i, type(e).__name__, str(e)[:160]))
            continue
        contrat[i] = m
        if not m:
            conformes.append(i)
    # P2 — UNE CASE FAUTIVE À LA FOIS, SUR LA FICHE ORDINAIRE (conforme d'abord)
    if "PROP-ORD" in conformes:
        for case, val in MUTATIONS:
            mesures["P2"] += 1
            try:
                r = CT.manques_du_contrat(dict(fiches["PROP-ORD"], **{case: val}), W, J=J)
            except Exception as e:  # noqa: BLE001
                prop["P2"].append("%s=%r : le contrat lève %s" % (case, val, type(e).__name__))
                continue
            nommees = {c.strip() for x in r for c in x.split(" : ", 1)[0].split("/")}
            if case not in nommees:
                prop["P2"].append("%s=%r : refus %s" % (case, val, ("sans la case : " + " | ".join(r)[:200]) if r
                                                         else "ABSENT (fiche acceptée)"))
    # P1, P5, P7, P8 — JOUER CHAQUE FICHE CONFORME
    jouees = {}
    for i in conformes:
        f = fiches[i]
        mesures["P1"] += 1
        try:
            sig = J.signal_de_la_fiche(W, f)
            bornes = J.porte_0(f)[2]
            ops, inconnus = J.jouer(f, cours, mnemo, sig, mod_pos, periode=bornes)
        except ValueError as e:
            if "non jouable" in str(e):
                refus.append({"maillon": "couche en mémoire (jouer)", "fiche": i, "motif": str(e)[:200]})
            else:
                prop["P1"].append("%s : jouer lève ValueError: %s" % (i, str(e)[:200]))
            continue
        except Exception as e:  # noqa: BLE001 — P1 : jamais une exception sur une fiche conforme
            prop["P1"].append("%s : jouer lève %s: %s" % (i, type(e).__name__, str(e)[:200]))
            continue
        jouees[i] = (f, sig, bornes, ops)
        if inconnus:
            refus.append({"maillon": "couche en mémoire (jouer)", "fiche": i,
                          "motif": "valeurs ignorées (inconnues des cours) : %s" % inconnus})
    for i, (f, sig, bornes, ops) in jouees.items():
        tp = J.seuil_de_la_fiche(f, "tp")
        sl = J.seuil_de_la_fiche_ou_aucun(f, "sl")
        h = J.lire_horizon_ou_aucune(f["horizon"])
        bareme = J.bareme_des_verdicts(None, mod_pos)
        mode = json.loads(f.get("reglages_signal") or "{}").get("mode")
        # P5 — CHAQUE OPÉRATION REJOUÉE PAR `vendre` AUX SEUILS DE SA FICHE, frais par `frais_aller_retour`
        for op in ops:
            mesures["P5"] += 1
            e = ecarts_d_une_vente(cours[op["valeur"]], op, tp, sl, h, mod_pos, bareme)   # une seule écriture (R-708)
            if e:
                prop["P5"].append("%s %s %s : %s" % (i, op["valeur"], op["date_entree"], " ; ".join(e)))
        # P8 — LES LIMITES
        mesures["P8"] += 1
        if mode == "jamais" and ops:
            prop["P8"].append("%s : signal jamais vrai, %d opération(s)" % (i, len(ops)))
        for op in ops:
            serie = cours[op["valeur"]]
            dd = [b["date"] for b in serie]
            if bornes and not (bornes[0] <= op["date_signal"] <= bornes[1]):
                prop["P8"].append("%s : signal du %s hors période %s" % (i, op["date_signal"], bornes))
            if op["date_signal"] == dd[-1]:
                prop["P8"].append("%s : achat sur un signal de la dernière séance %s" % (i, dd[-1]))
            if isinstance(h, int) and h == 1 and dd.index(op["date_sortie"]) - dd.index(op["date_entree"]) > 1:
                prop["P8"].append("%s : horizon 1, entrée %s sortie %s" % (i, op["date_entree"], op["date_sortie"]))
    # P7 — DEUX JEUX, MÊME EMPREINTE (sur toutes les fiches jouées, dont celles au hasard à graine)
    for i, (f, sig, bornes, ops) in jouees.items():
        mesures["P7"] += 1
        try:
            ops2, _x = J.jouer(f, cours, mnemo, J.signal_de_la_fiche(W, f), mod_pos, periode=bornes)
        except Exception as e:  # noqa: BLE001
            prop["P7"].append("%s : second jeu lève %s" % (i, type(e).__name__))
            continue
        e1 = hashlib.sha256(json.dumps(ops, sort_keys=True, default=str).encode()).hexdigest()
        e2 = hashlib.sha256(json.dumps(ops2, sort_keys=True, default=str).encode()).hexdigest()
        if e1 != e2:
            prop["P7"].append("%s : %s… puis %s…" % (i, e1[:12], e2[:12]))
    # P6 — LA SÉRIE COUPÉE AU JOUR J DONNE LE MÊME SIGNAL EN J QUE LA SÉRIE ENTIÈRE (une séance sur trois)
    for i, (f, sig, bornes, ops) in sorted(jouees.items())[:40]:
        for code in [c.strip() for c in f["univers"].split(",") if c.strip()][:2]:
            serie = cours[mnemo[code]]
            entiers = {x["i"] for x in sig(serie)}
            for Jr in list(range(0, len(serie), 3)) + [len(serie) - 1]:
                mesures["P6"] += 1
                coupe = any(x["i"] == Jr for x in sig(serie[:Jr + 1]))
                if coupe != (Jr in entiers):
                    prop["P6"].append("%s %s séance %s : coupée %s, entière %s" % (i, code, serie[Jr]["date"], coupe,
                                                                                Jr in entiers))
    rendu = {"proprietes": {p: (["ROUGE" if prop[p] else ("VERT" if mesures[p] else "NON MESURÉE"),
                                 "%d mesure(s) ; %s" % (mesures[p], " ; ".join(prop[p][:4]) or "aucun défaut")])
                            for p in prop},
             "refus": refus, "contrat": contrat, "conformes": conformes}
    print(json.dumps(rendu, ensure_ascii=False))


# ═══ LES MAILLONS ⓪ ET ① (processus neuf) ═════════════════════════════════════════════════════════════════════════════

def tableau_valide(f, J, quand):
    """Rend les quatre lignes du tableau des réglages « validé » d'une fiche factice : chaque réglage à SA seule valeur.
    ① RÔLE — ce que ⓪ recopie et ① décline. ② CONTEXTE D'APPEL — `chaine`. ③ ENTRÉE — la fiche, le juge, l'instant
    (datetime de Paris). ④ CONDITIONS D'ENTRÉE — la fiche passe le contrat. ⑤ SORTIE — UNE valeur : liste de 4
    dictionnaires aux colonnes de PREPARER. [rend: 1] ⑥ TRAITEMENT — tp, sl en pourcents (lecture du juge), horizon,
    univers. ⑦ UNITÉ — pourcents, séances. ⑧ POURQUOI — une version par fiche suffit à faire passer ⓪ et ①.
    ⑨ CE QUI CLOCHE — la mention « Jean-Luc le … » est FACTICE (⑨ ① de l'en-tête). ⑩ EFFET — aucun. ⑪ TERMINAISON —
    rend la main. [sort: non]"""
    def pct(c):
        v = J.seuil_de_la_fiche_ou_aucun(f, c)
        if not isinstance(v, float):
            return "sans stop"
        return ("%.6f" % (v * 100)).rstrip("0").rstrip(".")
    h = J.lire_horizon_ou_aucune(f["horizon"])
    hv = h if isinstance(h, int) else "aucune"
    raison = "FACTICE — épreuve par propriétés (A-923, A-941), copie jetable : aucune validation réelle"
    vp, pl = quand.strftime("Jean-Luc le %d-%m-%Y"), quand.strftime("%Y-%m-%d %Hh%M Paris")
    univ = ",".join(c.strip().upper() for c in f["univers"].split(",") if c.strip())
    return [dict(strategie=f["id"], essai=ESSAI, parametre=p, valeur_fiche=str(v), valeurs_a_essayer=str(v),
                 unite=u, jouable="OUI", raison=raison, valide_par=vp, prepare_le=pl)
            for p, v, u in (("tp", pct("tp"), "pourcents"), ("sl", pct("sl"), "pourcents"),
                            ("horizon", hv, "seances"), ("univers", univ, "mnemoniques"))]


def chaine(W, ids, octet):
    """⓪ PREPARER et ① DECLINER par l'enchaîneur, pour chaque fiche conforme de `ids` ; P1 et P3. Affiche un JSON.
    ① RÔLE — faire passer des stratégies quelconques dans la chaîne officielle, jusqu'à ① (A-941 bloque ② à ④).
    ② CONTEXTE D'APPEL — `__main__` « --chaine ». ③ ENTRÉE — W, les identifiants, `octet` (sabotage S-P3).
    ④ CONDITIONS D'ENTRÉE — W sans .git. ⑤ SORTIE — Aucune valeur ; un JSON. [rend: 0] ⑥ TRAITEMENT — contrat ; tableau
    validé écrit dans donnees/combinatoires de W ; enchaîneur « preparer » puis « decliner » ; `VERIFIER_LA_CHAINE.motifs`
    (exigées 3) et présence des fichiers témoignés ; avec `octet`, un octet du fichier ① de la première fiche passée
    est changé avant la mesure. ⑦ UNITÉ — —. ⑧ POURQUOI — étude D ③ ; P3 se mesure par le journal de la chaîne.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit sous W. ⑪ TERMINAISON — chaque lancement borné à 400 s. [sort: non]"""
    sys.path.insert(0, os.path.join(W, "programmes"))
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import CONTRATS_DES_FICHIERS as CT
    import JUGE_DES_STRATEGIES as J
    import VERIFIER_LA_CHAINE as V
    quand = datetime.now(ZoneInfo("Europe/Paris"))
    fiches = CT.fiches_du_registre(os.path.join(W, REG))
    p1, p3, refus, n1, n3, sabote = [], [], [], 0, 0, False
    for i in ids:
        f = fiches.get(i)
        if f is None or CT.manques_du_contrat(f, W, J=J):
            continue
        n1 += 1
        chem = os.path.join(W, "donnees", "combinatoires", "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (i, ESSAI))
        lignes = tableau_valide(f, J, quand)
        with open(chem, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(lignes[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(lignes)
        passe = True
        for etape, sous in (("preparer", "e0"), ("decliner", "e1")):
            code, texte = lancer(W, os.path.join(W, ENCH), W, i, ESSAI, etape)
            ch = V.dossier(W, i, ESSAI)
            detail = os.path.join(ch, sous, "sortie.txt")
            detail = open(detail, encoding="utf-8").read() if os.path.isfile(detail) else ""
            if code == 0:
                continue
            passe = False
            tout = texte + "\n" + detail
            maillon = "⓪ PREPARER" if etape == "preparer" else "① DECLINER"
            if code == 1 and ("REFUS" in tout or "ÉCHEC" in tout):
                motif = [l.strip() for l in tout.splitlines() if l.strip().startswith(("·", "REFUS", "ÉCHEC"))]
                refus.append({"maillon": maillon, "fiche": i, "motif": " | ".join(motif[:4])[:300]})
            else:
                p1.append("%s %s : code %d : %s" % (maillon, i, code, tout.strip()[-240:]))
            break
        if not passe:
            continue
        n3 += 1
        ch = V.dossier(W, i, ESSAI)
        t = V.temoins(ch)
        if octet and not sabote and "1-decliner" in t:
            cible = os.path.join(ch, t["1-decliner"][0])
            data = bytearray(open(cible, "rb").read())
            k = next(k for k in range(len(data) - 1, -1, -1) if chr(data[k]).isdigit())
            data[k] = ord("1") if data[k] != ord("1") else ord("2")
            open(cible, "wb").write(bytes(data))
            sabote = True
        m = V.motifs(W, i, ESSAI, 3)
        absents = [e for e in ("0-variables-validees", "0-proposition", "1-decliner") if e not in t or
                   not os.path.isfile(os.path.join(ch, t[e][0]))]
        if m or absents:
            p3.append("%s : %s%s" % (i, " ; ".join(m)[:200], (" ; témoins absents %s" % absents) if absents else ""))
    rendu = {"proprietes": {
        "P1": ["ROUGE" if p1 else ("VERT" if n1 else "NON MESURÉE"),
               "%d fiche(s) conforme(s) lancée(s) ; %s" % (n1, " ; ".join(p1[:3]) or "aucun plantage")],
        "P3": ["ROUGE" if p3 else ("VERT" if n3 else "NON MESURÉE"),
               "%d fiche(s) passée(s) par ⓪ ① ; %s" % (n3, " ; ".join(p3[:3]) or "témoins intacts")]},
        "refus": refus}
    print(json.dumps(rendu, ensure_ascii=False))


# ═══ LE SOIR (processus neuf, copie entière S) ════════════════════════════════════════════════════════════════════════

def nommee(texte, ident):
    """Dit si `ident` apparaît dans `texte` comme un identifiant entier. ① RÔLE — ne pas confondre PROP-Q1 et PROP-Q10.
    ② CONTEXTE D'APPEL — `soir`. ③ ENTRÉE — texte, identifiant. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur :
    booléen. [rend: 1] ⑥ TRAITEMENT — expression régulière bornée. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    import re
    return re.search(r"(?<![A-Za-z0-9_-])%s(?![A-Za-z0-9_-])" % re.escape(ident), texte) is not None


def soir(S, valeur, d_sig, close):
    """Le circuit du soir sur la copie S : détecteur, puis teneur deux fois ; SIL, P4, P1. Affiche un JSON.
    ① RÔLE — mesurer ce que le soir fait des fiches factices QA. ② CONTEXTE D'APPEL — `__main__` « --soir ».
    ③ ENTRÉE — S ; la valeur du signal posé (nom du cours maître), la séance du signal (avant-dernière du cours
    maître), sa clôture. ④ CONDITIONS D'ENTRÉE — S fabriquée par `fabriquer_s`. ⑤ SORTIE — Aucune valeur ; un JSON.
    [rend: 0] ⑥ TRAITEMENT — ① contrat des fiches QA · ② détecteur : chaque fiche QA conforme doit être NOMMÉE (dans sa
    sortie ou dans donnees/signaux_du_jour.json) ; retenue si elle figure aux « fiches suivies » sans garde · ③ un
    signal posé sur `valeur` à `d_sig` (forme d'E8), teneur deux fois : chaque fiche nommée (« horizon lu au registre »
    ou « FICHE … ») · ④ P4 sur les positions factices OUVERTES : valeur dans l'univers, objectif et stop = ceux de
    `MODULE_POSITIONS.seuils_de_vente` aux seuils de `lecture_du_soir` de SA fiche, un jeton au plus.
    ⑦ UNITÉ — euros. ⑧ POURQUOI — étude D ④ ; épreuve E8. ⑨ CE QUI CLOCHE — ⑨ ③ et ⑥ de l'en-tête. ⑩ EFFET — écrit
    sous S. ⑪ TERMINAISON — chaque lancement borné à 400 s. [sort: non]"""
    sys.path.insert(0, os.path.join(S, "programmes"))
    import CONTRATS_DES_FICHIERS as CT
    import JUGE_DES_STRATEGIES as J
    mod_pos = J.charger_module(J.trouver(S, "MODULE_POSITIONS.py"), "pos_du_soir_des_proprietes")
    fiches = {i: f for i, f in CT.fiches_du_registre(os.path.join(S, REG)).items() if i.startswith("PROP-Q")}
    qa = sorted(i for i, f in fiches.items() if not CT.manques_du_contrat(f, S, J=J))
    sil, p1, p4, refus, n4 = [], [], [], [], 0
    code_d, texte_d = lancer(S, DET, ".")
    sig_txt = open(os.path.join(S, SIG), encoding="utf-8").read() if os.path.isfile(os.path.join(S, SIG)) else ""
    if code_d not in (0, 1):
        p1.append("détecteur code %d : %s" % (code_d, texte_d.strip()[-240:]))
    suivies = texte_d.split("fiches suivies : ", 1)[1].split("·")[0] if "fiches suivies : " in texte_d else ""
    for i in qa:
        if not (nommee(texte_d, i) or nommee(sig_txt, i)):
            sil.append("⑥ détecteur : %s ignorée en silence" % i)
            refus.append({"maillon": "⑥ détecteur", "fiche": i, "motif": "IGNORÉE EN SILENCE"})
        elif not (code_d == 0 and nommee(suivies, i) and '"garde"' not in sig_txt):
            motif = [l.strip() for l in (texte_d + "\n" + sig_txt).splitlines() if nommee(l, i) or "GARDE" in l or
                     "CODE" in l]
            refus.append({"maillon": "⑥ détecteur", "fiche": i, "motif": ("code %d : " % code_d) +
                          " | ".join(motif[:3])[:300]})
    json.dump({"seance": d_sig, "signaux": [{"valeur": valeur, "date_signal": d_sig, "cmf": 0.01, "cci": -80.0,
                                              "close": close}]},
              open(os.path.join(S, SIG), "w", encoding="utf-8"))
    code_t, texte_t = lancer(S, "programmes/TENIR_LES_POSITIONS.py", ".")
    code_t2, texte_t2 = lancer(S, "programmes/TENIR_LES_POSITIONS.py", ".")
    for c, t in ((code_t, texte_t), (code_t2, texte_t2)):
        if c not in (0, 1):
            p1.append("teneur code %d : %s" % (c, t.strip()[-240:]))
    for i in qa:
        if not nommee(texte_t, i):
            sil.append("⑥ teneur : %s ignorée en silence" % i)
            refus.append({"maillon": "⑥ teneur", "fiche": i, "motif": "IGNORÉE EN SILENCE"})
        elif ("horizon lu au registre · %s " % i) not in texte_t:
            refus.append({"maillon": "⑥ teneur", "fiche": i, "motif": " | ".join(
                l.strip() for l in texte_t.splitlines() if nommee(l, i))[:300]})
    _e, positions = lire_csv(os.path.join(S, POS)) if os.path.isfile(os.path.join(S, POS)) else ([], [])
    refs = [n for n in os.listdir(os.path.join(S, "donnees")) if n.startswith("REFERENTIEL_VALEURS") and n.endswith(".csv")]
    _e, ref = lire_csv(os.path.join(S, "donnees", refs[0]))
    code_de = {(l.get("onglet_google") or "").strip().upper(): (l.get("mnemonique") or "").strip().upper() for l in ref}
    code_du_signal = code_de.get(valeur.strip().upper())
    servies = 0
    for i in qa:
        f = fiches[i]
        tp_f, sl_f, _h = J.lecture_du_soir(S, f)
        univ = {c.strip().upper() for c in f["univers"].split(",") if c.strip()}
        miennes = [p for p in positions if p.get("strategie") == i]
        # UN SIGNAL POSÉ SUR SON UNIVERS DOIT OUVRIR UNE POSITION À SES SEUILS (sinon P4 ne mesurerait rien et
        # resterait verte : un teneur qui refuse de tourner n'achète pas « ce que la fiche permet »)
        if code_du_signal in univ:
            servies += 1
            if not any((p.get("statut") or "").strip() == "OUVERTE" for p in miennes):
                p4.append("%s : signal posé sur %s (son univers), aucune position OUVERTE ; teneur codes %d puis %d : %s"
                          % (i, valeur, code_t, code_t2, " | ".join(texte_t2.strip().splitlines()[-4:])[:300]))
        jeton = [p for p in miennes if p.get("comptabilite") == "un_jeton" and
                 (p.get("statut") or "").strip() in ("OUVERTE", "EN_ATTENTE_ENTREE")]
        if len(jeton) > 1:
            p4.append("%s : %d positions en un jeton" % (i, len(jeton)))
        for p in miennes:
            if code_de.get((p.get("valeur") or "").strip().upper()) not in univ:
                p4.append("%s : position sur %s hors univers" % (i, p.get("valeur")))
            if (p.get("statut") or "").strip() == "OUVERTE":
                n4 += 1
                pe = float(p["prix_entree"])
                tp_a, sl_a = mod_pos.seuils_de_vente(pe, tp_f, sl_f)
                if abs(float(p["tp"]) - tp_a) > 1e-4 or abs(float(p["sl"]) - sl_a) > 1e-4:
                    p4.append("%s %s : objectif %s stop %s, attendus %s %s (fiche %g / %g)" % (
                        i, p.get("valeur"), p["tp"], p["sl"], tp_a, sl_a, tp_f, sl_f))
    rendu = {"proprietes": {
        "SIL": ["ROUGE" if sil else ("VERT" if qa else "NON MESURÉE"),
                "%d fiche(s) QA conforme(s) : %s ; %s" % (len(qa), qa, " ; ".join(sil) or "toutes nommées")],
        "P4": ["ROUGE" if p4 else ("VERT" if n4 else "NON MESURÉE"),
               "%d fiche(s) QA servie(s) par le signal, %d position(s) factice(s) OUVERTE(S) mesurée(s) ; %s" % (
                   servies, n4, " ; ".join(p4[:3]) or "aucun défaut")],
        "P1": ["ROUGE" if p1 else "VERT", "détecteur %d, teneur %d puis %d ; %s" % (
            code_d, code_t, code_t2, " ; ".join(p1) or "aucun plantage")]},
        "refus": refus}
    print(json.dumps(rendu, ensure_ascii=False))


# ═══ LA SUITE DE LA CHAÎNE : ② LE JUGE, ③ LES POSITIONS, ④ LA MESURE (A-945, processus neuf, dépôt fabriqué R) ══════

def jours_ouvres(debut, fin):
    """Rend les jours du lundi au vendredi de `debut` à `fin`, en textes AAAA-MM-JJ : le calendrier FABRIQUÉ de la suite.
    ① RÔLE — dater les cours fabriqués de la suite sans lire aucun calendrier. ② CONTEXTE D'APPEL — `suite`.
    ③ ENTRÉE — deux textes AAAA-MM-JJ, 2024 et après. ④ CONDITIONS D'ENTRÉE — `debut` ≤ `fin`. ⑤ SORTIE — UNE valeur :
    liste. [rend: 1] ⑥ TRAITEMENT — compter les jours, garder lundi-vendredi. ⑦ UNITÉ — jours. ⑧ POURQUOI — A-945
    (Jean-Luc, 20-11-2026, 17h53) : la suite ne lit rien d'avant 2024, même pas les dates ; le calendrier du dépôt
    (indice CAC 40 depuis 2000) en porte. ⑨ CE QUI CLOCHE — les jours fériés ne sont pas retirés : les cours sont
    fabriqués, aucune propriété n'en dépend. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    from datetime import date, timedelta
    d, f, rendu = date.fromisoformat(debut), date.fromisoformat(fin), []
    while d <= f:
        if d.weekday() < 5:
            rendu.append(d.isoformat())
        d += timedelta(days=1)
    return rendu


def ecarts_d_une_vente(serie, op, tp, sl, h, mod_pos, bareme):
    """Rejoue UNE opération par `MODULE_POSITIONS.vendre` aux seuils de SA fiche, frais par `frais_aller_retour`, et rend
    la liste de ses écarts avec ce qui est écrit.
    ① RÔLE — le rejeu d'une vente pour P5 (maillon ①). ② CONTEXTE D'APPEL — `couche` (P5) seulement : la suite (ETA,
    POS, GAIN) ne l'appelle plus depuis la réparation du 20-11-2026.
    ③ ENTRÉE — la série de la valeur, l'opération du juge (pe, px, motif, date_entree, date_sortie, frais, net), tp et sl
    en fractions, l'horizon, le module de positions, le barème. ④ CONDITIONS D'ENTRÉE — `date_entree` est dans la série.
    ⑤ SORTIE — UNE valeur : liste de textes, vide si tout se retrouve. [rend: 1] ⑥ TRAITEMENT — vendre (« vendre » : le
    juge rejoue un passé fini) ; comparer prix, motif, date ; frais à 1 € près ; gain net (si l'opération le porte) à
    1 centime près. ⑦ UNITÉ — euros. ⑧ POURQUOI — R-708 : le recalcul se demande aux fonctions du circuit, jamais
    recopié. ⑨ CE QUI CLOCHE — le défaut que le relecteur neuf du 20-11-2026 a trouvé dans ETA, POS et GAIN vit encore
    ici : `vendre` et `frais_aller_retour` sont celles du juge, un défaut commun (sabotages M1, M2) laisse P5 verte ;
    P5 n'est pas réparée par ce travail (maillon ①, hors de la suite) — consigné au BACKLOG par la note de relecture.
    ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    j = [b["date"] for b in serie].index(op["date_entree"])
    v = mod_pos.vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")
    if v is None:
        return ["vendre ne rend rien"]
    q = mod_pos.CAPITAL / v["pe"]
    fr = mod_pos.frais_aller_retour(q, v["pe"], v["px"], op["valeur"], op["date_entree"], v["date_sortie"],
                                    bareme)["total"]
    rendu = []
    if (v["pe"], v["px"], v["motif"], v["date_sortie"]) != (op["pe"], op["px"], op["motif"], op["date_sortie"]) or \
            abs(fr - op["frais"]) > 1:
        rendu.append("écrit (%s, %s, %s) · rejoué (%s, %s, %s)" % (op["px"], op["motif"], op["date_sortie"], v["px"],
                                                                 v["motif"], v["date_sortie"]))
    if "net" in op and abs(q * (v["px"] - v["pe"]) - fr - op["net"]) > 0.01:
        rendu.append("gain écrit %.2f · recalculé %.2f" % (op["net"], q * (v["px"] - v["pe"]) - fr))
    return rendu


SUITE_DEBUT, SUITE_FIN = "2024-01-02", "2025-12-31"     # A-945 : 2024 et après, jamais avant
SOIR_DEBUT = "2025-06-02"                                 # le soir est rejoué de là à SUITE_FIN (environ 150 séances)
CODES_FAB = ("FABA", "FABB", "FABC", "FABD", "FABE", "FABF")   # valeurs FABRIQUÉES ; FABA est la victime de P1
N_JUGES = 8          # fiches conformes passées par `juger` (le plus lent : voisinage et étalon de hasard)
N_SOIR_HASARD = 8    # fiches tirées au hasard rejouées par le soir, en plus de ORD, des limites et des QA
PROPRIETES_SUITE = ("A945", "ETA", "JUG", "POS", "GAIN", "PREUVE", "ACC")
ENONCES.update({
    "A945": "rien n'est lu dans le dépôt réel pendant la suite (garde d'audit : toute ouverture y est refusée)",
    "ETA": "étalonnage sur des CAS CONNUS : le juge rend les résultats écrits d'avance ; le témoin _c5e10_sortie "
           "concorde sans saut, diverge comme documenté avec saut",
    "JUG": "le juge rend un verdict du contrat ou un refus motivé, jamais une exception",
    "POS": "les positions respectent tp, sl et horizon de la fiche (Open J+1, un jeton, univers) ; le teneur rend les "
           "cas connus ; chaque sortie est la première séance qui touche un seuil",
    "GAIN": "la mesure rend les cas connus ; elle égale la somme des gains écrits ; les frais implicites sont dans "
            "leurs bornes (0,15 % par ordre, plus 0,4 % de taxe au plus)",
    "PREUVE": "chaque maillon ② ③ ④ laisse sa preuve (rapport et grille, journal complet, mesure de chaque compte)",
    "ACC": "les cours fabriqués portent chaque accident (saut bas, saut haut, double touche, trou), le soir sort au "
           "moins une fois en SL_GAP et en TP_GAP, et des positions traversent une double touche et un trou",
})
SABOTAGES_SUITE = (
    # LE FICHIER SABOTÉ DEVIENT UN VRAI FICHIER DE R : c'est donc le chemin réel d'un AUTRE (un lien) qui doit fuir —
    # comme `manques_du_contrat` résout celui de MODULE_POSITIONS (mesuré le 20-11-2026 : 292 ouvertures refusées).
    ("S-A945 le juge des frais pris par son chemin réel", "A945", "programmes/MODULE_POSITIONS.py",
     [('    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "JUGE_DES_STRATEGIES.py")\n',
       '    chemin = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '
       '"JUGE_DES_STRATEGIES.py"))\n')]),
    ("S-ETA vente du juge jouée avec un autre tp", "ETA", JUGE, [SABOTAGES[6][3][0]]),
    ("S-JUG juger lève KeyError", "JUG", JUGE,
     [('    # SANS STOP, PAS DE POINT MORT, DONC PAS DE VERDICT (A-541 ④) : refus nommé, avant la lecture stricte du stop.\n',
       '    raise KeyError("sabotage S-JUG")\n'
       '    # SANS STOP, PAS DE POINT MORT, DONC PAS DE VERDICT (A-541 ④) : refus nommé, avant la lecture stricte du stop.\n')]),
    ("S-POS échéance du teneur décalée d'une séance", "POS", TENIR,
     [('    return dates[i + h] if i + h < len(dates) else None\n',
       '    return dates[i + h + 1] if i + h + 1 < len(dates) else None\n')]),
    ("S-GAIN cumul de la mesure majoré de 1 %", "GAIN", "MESURER",
     [("cumul=sum(pnls),", "cumul=sum(pnls) * 1.01,")]),
    ("S-PREUVE le journal perd bareme_reel", "PREUVE", TENIR, [('            "bareme_reel": _bar,\n', '')]),
    # LES DEUX SABOTAGES DU RELECTEUR NEUF (20-11-2026) : tant que POS, GAIN et ETA rejouaient les trades avec les
    # fonctions mêmes du teneur, ces deux-là laissaient tout vert. Les CAS CONNUS (littéraux) doivent les voir : le
    # cinquième champ est le texte que le détail de la propriété DOIT porter (la RAISON de la morsure).
    ("S-M1 le stop n'est jamais touché", "POS", "programmes/MODULE_POSITIONS.py",
     [('    if bar["open"] <= sl:\n', '    if False:\n'), ('    if bar["low"] <= sl:\n', '    if False:\n')],
     "K01"),
    ("S-M2 les frais divisés par deux", "GAIN", "programmes/MODULE_POSITIONS.py",
     [('"total": f_achat + f_vente,', '"total": (f_achat + f_vente) / 2,')], "K02"),
    # LE GÉNÉRATEUR SANS SES ACCIDENTS (A-945, point ⑤ de la réparation) : la propriété ACC doit le voir.
    ("S-ACC générateur sans sauts, doubles touches ni trous", "ACC", "EPREUVE", ["--sans-accidents"], "trou"),
    # LES QUATRE ÉGALITÉS DE `tester_seance` (relecteur neuf du 20-11-2026, défaut MOYEN) : chaque comparaison large
    # devient stricte ; SON cas au seuil pile (K12 à K15) doit être nommé dans le détail de POS.
    ("S-EG1 ouverture pile au stop non vue (open < sl)", "POS", "programmes/MODULE_POSITIONS.py",
     [('    if bar["open"] <= sl:\n', '    if bar["open"] < sl:\n')], "K14"),
    ("S-EG2 ouverture pile à l'objectif non vue (open > tp)", "POS", "programmes/MODULE_POSITIONS.py",
     [('    if bar["open"] >= tp:\n', '    if bar["open"] > tp:\n')], "K15"),
    ("S-EG3 plus bas pile au stop non vu (low < sl)", "POS", "programmes/MODULE_POSITIONS.py",
     [('    if bar["low"] <= sl:\n', '    if bar["low"] < sl:\n')], "K13"),
    ("S-EG4 plus haut pile à l'objectif non vu (high > tp)", "POS", "programmes/MODULE_POSITIONS.py",
     [('    if bar["high"] >= tp:\n', '    if bar["high"] > tp:\n')], "K12"),
    # ACC COMPTE AUSSI DANS LES POSITIONS (relecteur neuf du 20-11-2026, défaut MINEUR) : doubles touches et trous
    # restent dans les cours, mais seulement AVANT le soir rejoué ; le compte des cours reste vert, celui des
    # positions doit rougir et le dire.
    ("S-ACC2 doubles touches et trous hors des séances du soir", "ACC", "EPREUVE", ["--accidents-avant-le-soir"],
     "aucune position sortie sur double touche"),
    # LES DEUX CONTRÔLES DE `defauts_d_un_trade` AJOUTÉS POUR I1 (Cowork, 20-11-2026), retirés un à un : le cas limite
    # qu'ils tiennent doit être nommé dans le détail de POS.
    ("S-I1a contrôle « SL sur une ouverture au-dessus de l'objectif » retiré", "POS", "EPREUVE",
     ["--sans-controle=saut"], "I1-C1"),
    ("S-I1b contrôle « sortie sur seuil après l'échéance » retiré", "POS", "EPREUVE",
     ["--sans-controle=echeance"], "I1-C2"),
)

# ═══ LES CAS CONNUS : RÉSULTATS ÉCRITS D'AVANCE, À L'ŒIL, SUR DES PRIX RONDS (réparation du 20-11-2026) ═══════════════
# POURQUOI. Le relecteur neuf du 20-11-2026 a trouvé POS, GAIN et ETA « juges et parties » : ils rejouaient chaque
# trade par `vendre`, `frais_aller_retour` et `prix_de_convention`, les fonctions mêmes du teneur et du juge. Un défaut
# de ces fonctions se retrouvait des deux côtés : stop jamais touché (M1) et frais divisés par deux (M2) laissaient tout
# vert. Verdict du superviseur R-759 : « RUSTINE, À REPRENDRE » pour un oracle réécrit (une 3e implémentation : deux
# implémentations d'une même chose divergent toujours, R-708) ; la vraie indépendance vient de CAS CONNUS. Ici, aucun
# attendu n'est calculé par le code : chacun est un LITTÉRAL, posé à la main sur des prix ronds.
#
# LES TEXTES DU REGISTRE, OUVERTS ET RECOPIÉS AVANT D'ÉCRIRE LES ATTENDUS (gouvernance/REGISTRE_REGLES.md, 20-11-2026) :
# R-602 : « Convention pessimiste : TP et SL même jour → SL compté (résultats = plancher). (Le « plancher » ne vaut que
#   pour ce cas. Le saut d'ouverture au-delà d'un seuil relève de R-607, 27-09-2026 : prix réel d'ouverture, dans les
#   deux sens — y compris quand la séance traverse ensuite l'autre seuil, R-607 ③.) »
# R-607 : « QUAND LE COURS SAUTE À L'OUVERTURE AU-DELÀ DE L'OBJECTIF OU DE LA VENTE FORCÉE, ON COMPTE LE PRIX RÉEL
#   D'OUVERTURE — DANS LES DEUX SENS. » ① « Saut favorable — l'ouverture est au-dessus de l'objectif : on compte la
#   vente au prix d'ouverture. » ② « Saut défavorable — l'ouverture est au-dessous de la vente forcée : on compte aussi
#   le prix d'ouverture, même s'il est pire. » ③ « Une séance ouvre au-delà d'un seuil puis traverse l'autre :
#   l'ouverture l'emporte. » ④ « Objectif et vente forcée touchés la même séance, sans saut : on compte la perte
#   (R-602, inchangée). » ⑤ « Le prix « de convention » — le seuil exact, comme dans le backtest — reste écrit au
#   journal, à côté du prix réel, mais il n'est jamais le chiffre officiel. »
# R-112 : « L'HORIZON D'UNE POSITION SE COMPTE EN SÉANCES DU CALENDRIER : UNE SÉANCE MANQUANTE LE FAIT AVANCER. »
#   ① « Une séance manquante compte comme une séance de l'horizon. […] Exemple : une position achetée le 01-07 dont la
#   séance du 03-07 manque dans les cours est vendue à l'horizon à la même date que si le cours du 03-07 était là. »
#   Le même texte dit : « CE QUI N'EST PAS ENCORE VRAI (10-10-2026) : TENIR_LES_POSITIONS.py (fonction `echeance`)
#   prend la séance « h rangs après la séance d'achat » parmi les DATES PRÉSENTES […] et le juge […] compte aussi en
#   lignes » ; `MODULE_POSITIONS.vendre` ⑨ le consigne encore au 20-11-2026 (n°315). D'où l'ÉCART CONNU du cas K07.
# R-608 (séance d'achat surveillée) et R-601 (entrée à l'ouverture du lendemain du signal) fixent la séance d'achat.
#
# LES FRAIS ATTENDUS, EN EUROS, À LA MAIN : 0,15 % de la valeur échangée à CHAQUE ordre (tarif Fortuneo Progress,
# donnees/BAREME_FRAIS.csv, ligne REEL courtage) ; plus, à l'ACHAT d'une valeur taxée, la taxe sur les transactions
# financières : 0,3 % jusqu'au 31-03-2025, 0,4 % depuis le 01-04-2025 (même fichier) ; pas de taxe sur un achat revendu
# le jour même (BOFiP, BOI-TCA-FIN-10-10-20151221, § 60, rapporté dans `MODULE_POSITIONS.frais_aller_retour`). Le taux
# n'est JAMAIS relu dans MODULE_POSITIONS : il est dans les littéraux ci-dessous, multiplié de tête.
# Achat à 100,00 € : 100 000 € engagés, 1 000 titres. Objectif +4 % : 104,00 €. Stop −2,5 % : 97,50 €.
#   Sortie à 104,00 : 150,00 + 156,00 = 306,00 € ; P&L 4 000,00 − 306,00 = +3 694,00 €.
#   Sortie à  97,50 : 150,00 + 146,25 = 296,25 € ; P&L −2 500,00 − 296,25 = −2 796,25 €.
#   Sortie à  96,00 : 150,00 + 144,00 = 294,00 € ; P&L −4 000,00 − 294,00 = −4 294,00 €.
#   Sortie à 106,00 : 150,00 + 159,00 = 309,00 € ; P&L 6 000,00 − 309,00 = +5 691,00 €.
#   Sortie à 101,00 : 150,00 + 151,50 = 301,50 € ; P&L 1 000,00 − 301,50 = +698,50 €.
#   Sortie à 102,00 : 150,00 + 153,00 = 303,00 € ; P&L 2 000,00 − 303,00 = +1 697,00 €.
#   Valeur taxée en 2024, sortie à 104,00 : 150,00 + 300,00 + 156,00 = 606,00 € ; P&L 4 000,00 − 606,00 = +3 394,00 €.
#
# LE COMPTE DE LA MESURE : « un jeton » au prix réel, « jetons illimités » au prix de convention — c'est ce que fait
# `MESURER_LA_PERFORMANCE.mesurer_une_strategie` au 20-11-2026 (constat A-330) ; R-607, « CE QUE CETTE RÈGLE CHANGE »,
# veut les deux au prix réel APRÈS étude d'impact et oui de Jean-Luc : non fait. Les attendus de la mesure suivent donc
# l'état décidé d'aujourd'hui, nommé, et changeront avec lui.
#
# LE TÉMOIN DIFFÉRENTIEL : `MODULE_C5_ETENDU_10._c5e10_sortie`, le recalcul du radar, gardé INDÉPENDANT par décision de
# Jean-Luc (BACKLOG A-208 ⑤, 14-08-2026 : « DOUBLON VOLONTAIRE, on n'y touche jamais »). Il ne regarde jamais
# l'ouverture (son ⑨ ①) : sur les cas SANS saut il doit CONCORDER avec le juge ; sur les cas AVEC saut, le désaccord
# est ATTENDU et écrit ci-dessous en littéral (« temoin »). Ses frais passent par `frais_aller_retour` : il ne témoigne
# que de la SORTIE (motif, prix, date), pas des frais.
JAN24 = ("2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11",
         "2024-01-12", "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19")
CALME = (100.5, 101.0, 99.5, 100.5)            # ouverture, plus haut, plus bas, clôture : loin de 104,00 et de 97,50
ACHAT = (100.0, 101.0, 99.5, 100.5)            # la séance d'achat : ouverture 100,00 (R-601)
OCT26 = ("2026-10-15", "2026-10-16", "2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-26",
         "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30", "2026-11-02", "2026-11-03", "2026-11-04")
CAS_CONNUS = (
    # K01 — STOP TOUCHÉ À LA DEUXIÈME SÉANCE APRÈS L'ACHAT : plus bas 97,00 sous 97,50, ouverture 99,50 au-dessus.
    dict(id="K01", quoi="stop touché à la séance k=2", code="FABC", horizon="3", signal="2024-01-08", jours=JAN24,
         barres={"2024-01-09": ACHAT, "2024-01-11": (99.5, 100.0, 97.0, 97.8)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="SL", date_sortie="2024-01-11", px=97.5, frais=296.25,
                      net=-2796.25, px_conv=97.5, net_conv=-2796.25)),
    # K02 — OBJECTIF TOUCHÉ : plus haut 104,50 au-dessus de 104,00, ouverture 100,50 en dessous.
    dict(id="K02", quoi="objectif touché", code="FABC", horizon="3", signal="2024-01-08", jours=JAN24,
         barres={"2024-01-09": ACHAT, "2024-01-10": (100.5, 104.5, 100.0, 104.2)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="TP", date_sortie="2024-01-10", px=104.0, frais=306.0,
                      net=3694.0, px_conv=104.0, net_conv=3694.0)),
    # K03 — DOUBLE TOUCHE LE MÊME JOUR, SANS SAUT : plus haut 105,00 et plus bas 97,00 ; R-602 : le SL est compté.
    dict(id="K03", quoi="double touche le même jour : SL compté (R-602)", code="FABC", horizon="3",
         signal="2024-01-08", jours=JAN24, barres={"2024-01-09": ACHAT, "2024-01-10": (100.0, 105.0, 97.0, 101.0)},
         saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="SL", date_sortie="2024-01-10", px=97.5, frais=296.25,
                      net=-2796.25, px_conv=97.5, net_conv=-2796.25)),
    # K04 — SAUT D'OUVERTURE SOUS LE STOP : ouverture 96,00 sous 97,50 ; R-607 ② : prix réel d'ouverture ; la
    # convention (R-607 ⑤) garde le stop, 97,50.
    dict(id="K04", quoi="saut d'ouverture sous le stop : SL_GAP à l'Open (R-607 ②)", code="FABC", horizon="3",
         signal="2024-01-08", jours=JAN24, barres={"2024-01-09": ACHAT, "2024-01-10": (96.0, 98.0, 95.0, 97.0)},
         saut=True,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="SL_GAP", date_sortie="2024-01-10", px=96.0,
                      frais=294.0, net=-4294.0, px_conv=97.5, net_conv=-2796.25),
         temoin=dict(motif="SL", px=97.5, date_sortie="2024-01-10")),
    # K05 — SAUT D'OUVERTURE AU-DESSUS DE L'OBJECTIF : ouverture 106,00 ; R-607 ① : prix réel d'ouverture.
    dict(id="K05", quoi="saut d'ouverture au-dessus de l'objectif : TP_GAP à l'Open (R-607 ①)", code="FABC",
         horizon="3", signal="2024-01-08", jours=JAN24,
         barres={"2024-01-09": ACHAT, "2024-01-10": (106.0, 107.0, 105.0, 106.5)}, saut=True,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="TP_GAP", date_sortie="2024-01-10", px=106.0,
                      frais=309.0, net=5691.0, px_conv=104.0, net_conv=3694.0),
         temoin=dict(motif="TP", px=104.0, date_sortie="2024-01-10")),
    # K06 — ÉCHÉANCE : horizon 3, aucun seuil touché ; vente à la clôture de la 3e séance après l'achat (09 → 12-01),
    # clôture 101,00.
    dict(id="K06", quoi="échéance (horizon 3)", code="FABC", horizon="3", signal="2024-01-08", jours=JAN24,
         barres={"2024-01-09": ACHAT, "2024-01-12": (100.5, 101.0, 99.5, 101.0)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="HORIZON", date_sortie="2024-01-12", px=101.0,
                      frais=301.5, net=698.5, px_conv=101.0, net_conv=698.5)),
    # K07 — SÉANCE MANQUANTE (R-112 ①) : le cours du 10-01 manque pour la valeur ; la bourse était ouverte (FABE, le
    # « calendrier », l'a). R-112 : la séance manquante compte, l'échéance reste le 12-01, clôture 101,00. ÉCART CONNU
    # (R-112, « CE QUI N'EST PAS ENCORE VRAI » ; `vendre` ⑨, n°315) : le code compte en LIGNES, 09 → 11 → 12 → 15-01,
    # et vend à la clôture du 15-01, 102,00. Le cas est NOMMÉ à chaque passage, jamais compté vert.
    dict(id="K07", quoi="séance manquante (R-112) : l'horizon avance", code="FABC", horizon="3", signal="2024-01-08",
         jours=JAN24, trous=("2024-01-10",), calendrier="FABE",
         barres={"2024-01-09": ACHAT, "2024-01-12": (100.5, 101.0, 99.5, 101.0),
                 "2024-01-15": (100.5, 102.5, 99.5, 102.0)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="HORIZON", date_sortie="2024-01-12", px=101.0,
                      frais=301.5, net=698.5, px_conv=101.0, net_conv=698.5),
         ecart_connu=dict(pourquoi="R-112 non appliquée : l'horizon se compte en lignes (vendre ⑨, n°315)",
                          date_entree="2024-01-09", pe=100.0, motif="HORIZON", date_sortie="2024-01-15", px=102.0,
                          frais=303.0, net=1697.0, px_conv=102.0, net_conv=1697.0)),
    # K08 — VALEUR TAXÉE (FABB, taxée en 2024 : 0,3 % à l'achat) : mêmes séances que K02 ; à comparer à K02, non taxée.
    dict(id="K08", quoi="valeur taxée (K02 est la même, non taxée)", code="FABB", horizon="3", signal="2024-01-08",
         jours=JAN24, barres={"2024-01-09": ACHAT, "2024-01-10": (100.5, 104.5, 100.0, 104.2)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="TP", date_sortie="2024-01-10", px=104.0, frais=606.0,
                      net=3394.0, px_conv=104.0, net_conv=3394.0)),
    # K09 — OUVERTURE AU-DESSUS DE L'OBJECTIF PUIS PLUS BAS SOUS LE STOP (R-607 ③) : « l'ouverture l'emporte » —
    # TP_GAP à 106,00. Convention : l'objectif, 104,00 (`prix_de_convention`, A-506 : le backtest retiendrait le stop).
    dict(id="K09", quoi="saut au-dessus puis traversée du stop : l'ouverture l'emporte (R-607 ③)", code="FABC",
         horizon="3", signal="2024-01-08", jours=JAN24,
         barres={"2024-01-09": ACHAT, "2024-01-10": (106.0, 107.0, 97.0, 98.0)}, saut=True,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="TP_GAP", date_sortie="2024-01-10", px=106.0,
                      frais=309.0, net=5691.0, px_conv=104.0, net_conv=3694.0),
         temoin=dict(motif="SL", px=97.5, date_sortie="2024-01-10")),
    # K10 — VALEUR TAXÉE, STOP TOUCHÉ LA SÉANCE MÊME DE L'ACHAT (R-608) : achat et vente le 09-01, pas de taxe
    # (BOFiP § 60) : 150,00 + 146,25 = 296,25 €.
    dict(id="K10", quoi="valeur taxée revendue le jour de l'achat : pas de taxe", code="FABB", horizon="3",
         signal="2024-01-08", jours=JAN24, barres={"2024-01-09": (100.0, 100.5, 97.0, 98.0)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="SL", date_sortie="2024-01-09", px=97.5, frais=296.25,
                      net=-2796.25, px_conv=97.5, net_conv=-2796.25)),
    # K11 — CALQUÉ SUR UNE VRAIE LIGNE DU JOURNAL (R-732) : donnees/claude_journal_trades.csv, ligne
    # « C5E10-QA-V1,EIFFAGE,2026-10-21,98.00000,2026-11-02,101.92000,TP,3294.00,101.92000,3294.00,un_jeton,,,REEL,REEL ».
    # Mêmes dates, mêmes prix, mêmes seuils (+4,0 % / −2,5 %, horizon 20 : la fiche C5E10-QA-V1), valeur taxée (Eiffage
    # l'est en 2026 ; ici FABB, taxée) ; seules les séances autour sont fabriquées. Frais : 150,00 + 400,00 (0,4 %) +
    # 156,00 (104 000 € à la vente) = 706,00 € ; P&L 4 000,00 − 706,00 = +3 294,00 €, le montant même du journal.
    dict(id="K11", quoi="vraie ligne du journal : EIFFAGE du 21-10-2026 (R-732)", code="FABB", horizon="20",
         signal="2026-10-20", jours=OCT26, calme=(98.5, 99.0, 97.5, 98.5),
         barres={"2026-10-21": (98.0, 99.0, 97.5, 98.5), "2026-11-02": (99.5, 102.3, 99.0, 102.0)}, saut=False,
         periode="2026-10-01 -> 2026-11-30",
         attendu=dict(date_entree="2026-10-21", pe=98.0, motif="TP", date_sortie="2026-11-02", px=101.92, frais=706.0,
                      net=3294.0, px_conv=101.92, net_conv=3294.0)),
    # ─── LES SEUILS TOUCHÉS PILE (relecteur neuf du 20-11-2026, défaut MOYEN) ───────────────────────────────────────
    # POURQUOI. Sabotage qui le prouvait : « bar["high"] >= tp » devenu « > tp » dans `MODULE_POSITIONS.tester_seance`
    # laissait la suite verte. Les cours fabriqués ne tombent jamais pile sur un seuil, et la zone morte de 1e-3 € de
    # `defauts_d_un_trade` cache l'égalité. Or des cours réels à deux décimales tombent pile : achat à 100,00, objectif
    # +4 % = 104,00 €, stop −2,5 % = 97,50 € (`seuils_de_vente` arrondit à cinq décimales : 104.0 et 97.5 exactement).
    # CE QUE LA LOI DIT DE L'ÉGALITÉ. R-607 : « Il y a saut quand le cours ouvre déjà au-delà de l'objectif ou de la
    # vente forcée » ; ① « l'ouverture est au-dessus de l'objectif » ; ② « l'ouverture est au-dessous de la vente
    # forcée ». Le REGISTRE ne tranche pas l'ouverture PILE au seuil. Le PRIX ne dépend pas de ce choix (ouverture =
    # seuil) : seul le MOTIF en dépend. K14 et K15 figent le motif que le code écrit aujourd'hui (SL_GAP, TP_GAP : tests
    # « <= » et « >= ») ; c'est un attendu de COMPORTEMENT, pas de loi — question ouverte nommée dans la note de relecture.
    # Pour le plus haut et le plus bas, le REGISTRE dit « touché » (R-602 : « TP et SL même jour → SL compté ») sans
    # définir l'égalité ; le code (« >= », « <= ») et le témoin `_c5e10_sortie`, gardé indépendant (A-208 ⑤), comptent
    # tous deux un seuil ATTEINT comme touché : K12 et K13 figent cet accord.
    # K12 — PLUS HAUT = OBJECTIF EXACTEMENT : plus haut 104,00. Sortie TP à 104,00, comme K02.
    # Sous le sabotage « > tp » : aucune sortie, échéance le 12-01 à la clôture CALME 100,50.
    dict(id="K12", quoi="plus haut = objectif exactement : TP", code="FABC", horizon="3", signal="2024-01-08",
         jours=JAN24, barres={"2024-01-09": ACHAT, "2024-01-10": (100.5, 104.0, 100.0, 103.5)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="TP", date_sortie="2024-01-10", px=104.0, frais=306.0,
                      net=3694.0, px_conv=104.0, net_conv=3694.0)),
    # K13 — PLUS BAS = STOP EXACTEMENT : plus bas 97,50, ouverture 99,50 au-dessus ; sortie SL à 97,50, comme K01.
    # Sous le sabotage « < sl » : aucune sortie, échéance le 12-01 à 100,50.
    dict(id="K13", quoi="plus bas = stop exactement : SL", code="FABC", horizon="3", signal="2024-01-08", jours=JAN24,
         barres={"2024-01-09": ACHAT, "2024-01-10": (99.5, 100.0, 97.5, 98.0)}, saut=False,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="SL", date_sortie="2024-01-10", px=97.5, frais=296.25,
                      net=-2796.25, px_conv=97.5, net_conv=-2796.25)),
    # K14 — OUVERTURE = STOP EXACTEMENT : ouverture 97,50, plus bas 97,00. Prix 97,50 dans tous les cas (R-607 ② ou
    # R-602, même chiffre) ; motif SL_GAP (comportement du code, voir plus haut). Sous le sabotage « open < sl » : le
    # plus bas 97,00 donne SL à 97,50 — même prix, MOTIF différent : c'est le motif qui mord. Le témoin, qui ne regarde
    # jamais l'ouverture, rend SL à 97,50.
    dict(id="K14", quoi="ouverture = stop exactement : SL_GAP au prix du stop", code="FABC", horizon="3",
         signal="2024-01-08", jours=JAN24, barres={"2024-01-09": ACHAT, "2024-01-10": (97.5, 98.5, 97.0, 98.0)},
         saut=True,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="SL_GAP", date_sortie="2024-01-10", px=97.5,
                      frais=296.25, net=-2796.25, px_conv=97.5, net_conv=-2796.25),
         temoin=dict(motif="SL", px=97.5, date_sortie="2024-01-10")),
    # K15 — OUVERTURE = OBJECTIF EXACTEMENT : ouverture 104,00, plus bas 103,50 (loin du stop). Prix 104,00 dans tous les
    # cas ; motif TP_GAP. Sous le sabotage « open > tp » : le plus haut 104,50 donne TP à 104,00 — le motif mord.
    dict(id="K15", quoi="ouverture = objectif exactement : TP_GAP au prix de l'objectif", code="FABC", horizon="3",
         signal="2024-01-08", jours=JAN24, barres={"2024-01-09": ACHAT, "2024-01-10": (104.0, 104.5, 103.5, 104.2)},
         saut=True,
         attendu=dict(date_entree="2024-01-09", pe=100.0, motif="TP_GAP", date_sortie="2024-01-10", px=104.0,
                      frais=306.0, net=3694.0, px_conv=104.0, net_conv=3694.0),
         temoin=dict(motif="TP", px=104.0, date_sortie="2024-01-10")),
)
# Les catégories d'ACCIDENTS que le générateur 2024-2025 injecte, et leur TAUX FIXE par séance et par valeur (point ⑤ de
# la réparation) : la graine reste GRAINE ; un second tirage, à graine dérivée, décide l'accident.
TAUX_ACCIDENTS = (("saut_bas", 0.02), ("saut_haut", 0.02), ("double", 0.02), ("trou", 0.01))


def fabriquer_r(racine, R, fiches, durs=False):
    """Fabrique le dépôt jetable R de la suite : le code, trois fichiers de réglages, et des données FABRIQUÉES de 2024
    et après seulement (référentiel, liste des valeurs taxées, registre des fiches factices, module de signal factice).
    ① RÔLE — un dépôt où ② ③ ④ tournent sans rien lire d'avant 2024 (A-945). ② CONTEXTE D'APPEL — `passage_suite`.
    ③ ENTRÉE — la racine (copie du dépôt), R, les fiches, `durs` (vrai pour « --bout-en-bout » : LIENS DURS vers
    programmes/, voir ⑥). ④ CONDITIONS D'ENTRÉE — R n'existe pas ; la racine porte
    programmes/, gouvernance/REGISTRE_REGLES.md, donnees/BAREME_FRAIS.csv, donnees/combinatoires/VOISINAGE_DU_JUGE.csv
    et la première ligne du registre. ⑤ SORTIE — Aucune. [rend: 0] ⑥ TRAITEMENT — LIENS SYMBOLIQUES (aucune copie du
    dépôt : chaque fichier de programmes/ et les trois fichiers de réglages sont liés, jamais recopiés ; un fichier
    saboté remplace SON lien par un fichier écrit, `passage_suite`) ; avec `durs`, les fichiers de programmes/ sont des
    LIENS DURS (même fichier, aucun octet recopié ; une copie seulement si la racine est sur un autre disque) : Python
    résout le lien SYMBOLIQUE d'un script lancé (sys.path[0] devient programmes/ du dépôt réel, mesuré le 20-11-2026
    avec Python 3.13), et un module qui cherche ses données à côté de lui (`_chemin_des_donnees` de MODULE_POSITIONS)
    lisait alors le dépôt réel — la garde A-945 l'a refusé (donnees/BAREME_FRAIS.csv lu par ⓪ PREPARER) ; écrire le référentiel (CODES_FAB), VALEURS_TTF (2024 à 2026, la victime sans 2025 ni 2026, une valeur
    sur deux taxée), le registre (en-tête lu en PREMIÈRE LIGNE seulement, puis les fiches) et le module. ⑦ UNITÉ — —.
    ⑧ POURQUOI — consigne du Chat du 20-11-2026 : « n'utilise JAMAIS la vraie branche des regards ni de vraies fiches.
    Tout se passe dans un dépôt jetable fabriqué, avec des données de 2024 et après ». ⑨ CE QUI CLOCHE — le barème des
    frais, la loi (REGISTRE_REGLES.md) et le voisinage du juge sont des RÉGLAGES copiés tels quels : le barème porte des
    dates de début de tarif antérieures à 2024, ce ne sont ni des cours ni des séances. ⑩ EFFET — écrit sous R.
    ⑪ TERMINAISON — rend la main ; lève OSError si un fichier de réglages manque. [sort: non]"""
    os.makedirs(os.path.join(R, "programmes"))
    for x in sorted(os.listdir(os.path.join(racine, "programmes"))):
        if os.path.isfile(os.path.join(racine, "programmes", x)):
            if not durs:
                os.symlink(os.path.join(racine, "programmes", x), os.path.join(R, "programmes", x))
                continue
            try:
                os.link(os.path.join(racine, "programmes", x), os.path.join(R, "programmes", x))
            except OSError:
                shutil.copy2(os.path.join(racine, "programmes", x), os.path.join(R, "programmes", x))
    for rel in ("gouvernance/REGISTRE_REGLES.md", "donnees/BAREME_FRAIS.csv",
                "donnees/combinatoires/VOISINAGE_DU_JUGE.csv"):
        os.makedirs(os.path.dirname(os.path.join(R, rel)), exist_ok=True)
        os.symlink(os.path.join(racine, rel), os.path.join(R, rel))
    sys.path.insert(0, os.path.join(R, "programmes"))
    try:
        import CONTRATS_DES_FICHIERS as CT
        colonnes_ttf = list(CT.VALEURS_TTF)
    finally:
        sys.path.pop(0)
    with open(os.path.join(R, "donnees", "REFERENTIEL_VALEURS_FABRIQUE.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["mnemonique", "nom_usuel", "onglet_google", "hors_univers"])
        for c in CODES_FAB:
            w.writerow([c, "Fabriquee %s" % c[-1], "FABRIQUEE_%s" % c[-1], ""])
    with open(os.path.join(R, TTF), "w", encoding="utf-8", newline="") as fh:
        fh.write("# FABRIQUÉ par l'épreuve par propriétés (A-945) : valeurs factices, 2024 à 2026 seulement\n")
        w = csv.DictWriter(fh, fieldnames=colonnes_ttf, lineterminator="\n")
        w.writeheader()
        for an in ("2024", "2025", "2026"):       # 2026 : le cas K11, calqué sur une vraie ligne du journal (R-732)
            for k, c in enumerate(CODES_FAB):
                if an != "2024" and c == CODES_FAB[0]:
                    continue
                w.writerow(dict(annee=an, mnemonique=c, nom_usuel="Fabriquee %s" % c[-1],
                                assujettie="OUI" if k % 2 else "NON", liste_reference="factice", source="factice",
                                releve_le="2026-11-20"))
    with open(os.path.join(racine, REG), encoding="utf-8-sig") as fh:
        entete = fh.readline()
    with open(os.path.join(R, REG), "w", encoding="utf-8", newline="") as fh:
        fh.write(entete if entete.endswith("\n") else entete + "\n")
    ajouter_au_registre(R, fiches)
    open(os.path.join(R, MODULE), "w", encoding="utf-8").write(TEXTE_DU_MODULE)


def juge_une_fiche(f, R, ctx, avec_juger):
    """Passe UNE fiche par le maillon ② du juge, en mémoire : contrat, porte, signal, `jouer`, `juger` (si demandé),
    puis la grille de R-505. Rend (genre, texte, opérations, verdict, rapport).
    ① RÔLE — la propriété JUG et la preuve du juge. ② CONTEXTE D'APPEL — `suite`. ③ ENTRÉE — la fiche, R, le contexte
    (modules, cours, table de la loi), `avec_juger`. ④ CONDITIONS D'ENTRÉE — R fabriqué. ⑤ SORTIE — CINQ valeurs :
    « VERDICT », « REFUS » ou « PLANTE » ; le motif ou le mot du verdict ; les opérations ; le rendu de la grille (ou
    None) ; le texte affiché par `juger` (ou ""). [rend: 5] ⑥ TRAITEMENT — un refus du contrat ou une ValueError
    porteuse d'un motif est un REFUS MOTIVÉ ; toute autre exception, ou une ValueError muette, est un PLANTAGE ; un mot
    hors de CONTRATS.MOTS_DU_VERDICT est un plantage. ⑦ UNITÉ — euros. ⑧ POURQUOI — A-923 : « le juge rend un verdict ou
    un refus, jamais une exception » ; la porte du juge en ligne de commande (`main`, JOUER_LES_VERSIONS) se calibre sur
    le témoin du golden (2000-2026), interdit par A-945 : la suite appelle les fonctions qu'elle enchaîne.
    ⑨ CE QUI CLOCHE — ① la grille reçoit k « INCONNU » et aucune déclaration, aucun regard, aucun hasard : son verdict
    est « NON TRANCHÉE » par construction ; la propriété porte sur la FORME du verdict, pas sur sa valeur.
    ② ContratImpossible (le contrôle n'a pas tourné) compte comme plantage. ⑩ EFFET — `juger` affiche (capturé).
    ⑪ TERMINAISON — rend la main ; `juger` borne ses tirages. [sort: non]"""
    import contextlib
    CT, J = ctx["CT"], ctx["J"]
    try:
        m = CT.manques_du_contrat(f, R, J=J, mod_pos=ctx["pos"])   # le module de R : le contrat, seul, le chercherait
    except Exception as e:  # noqa: BLE001 — R-734 : un contrat qui n'a pas tourné n'est pas un refus
        return "PLANTE", "contrat : %s: %s" % (type(e).__name__, str(e)[:160]), [], None, ""
    if m:
        return "REFUS", "contrat : " + " | ".join(m)[:300], [], None, ""
    rapport = ""
    try:
        sig = J.signal_de_la_fiche(R, f)
        bornes = J.porte_0(f)[2]
        ops, _inc = J.jouer(f, ctx["cours"], ctx["mnemo"], sig, ctx["pos"], periode=bornes)
        if avec_juger:
            tampon = io.StringIO()
            with contextlib.redirect_stdout(tampon):
                J.juger(f, ops, ctx["cours"], ctx["seances"], ctx["jug"], ctx["sta"], ctx["pos"], ctx["mnemo"],
                        bornes, (sig,), racine=R)
            rapport = tampon.getvalue()
        tp, sl = J.seuil_de_la_fiche(f, "tp"), J.seuil_de_la_fiche_ou_aucun(f, "sl")
        pm = ctx["jug"].point_mort_des_operations(tp, sl, ops, ctx["pos"]) if ops and isinstance(sl, float) else None
        g = ctx["jug"].grille_de_validation(ctx["table"], CT.CAS_DE_LA_LOI[0], "INCONNU", ops=ops, point_mort_pct=pm)
    except ValueError as e:
        if str(e).strip():
            return "REFUS", "%s" % str(e)[:300], [], None, rapport
        return "PLANTE", "ValueError sans motif", [], None, rapport
    except Exception as e:  # noqa: BLE001 — JUG : jamais une exception
        return "PLANTE", "%s: %s" % (type(e).__name__, str(e)[:200]), [], None, rapport
    if not isinstance(g, dict) or g.get("verdict") not in CT.MOTS_DU_VERDICT:
        return "PLANTE", "verdict hors du contrat : %r" % (g.get("verdict") if isinstance(g, dict) else g), ops, g, \
            rapport
    return "VERDICT", g["verdict"], ops, g, rapport


def rejouer_le_soir(R, ctx, ids, fiches, debut_du_soir=SOIR_DEBUT):
    """Rejoue le teneur des positions (`TENIR_LES_POSITIONS.tenir`, LA fonction du soir) séance après séance, de
    `debut_du_soir` à la dernière date de ctx["dates"], sur les fiches `ids` ; rend (positions vues à l'ouverture,
    trades, défauts, jours).
    ① RÔLE — le maillon ③. ② CONTEXTE D'APPEL — `suite` (cours fabriqués 2024-2025) ; `jouer_les_cas_connus` (les
    séances d'un cas connu, `debut_du_soir` = sa première date). ③ ENTRÉE — R, le contexte (TE, J, pos, cours, dates :
    le calendrier, mnemo), les identifiants, les fiches, la première soirée rejouée (AAAA-MM-JJ).
    ④ CONDITIONS D'ENTRÉE — chaque fiche passe `lecture_du_soir` ; chaque série est triée par date ; ses dates sont
    dans ctx["dates"] (une série peut en MANQUER : un trou). ⑤ SORTIE — QUATRE valeurs : {clé: position à son dernier
    état OUVERT}, liste des trades, liste des défauts, nombre de séances. [rend: 4] ⑥ TRAITEMENT — chaque soir D :
    chaque série coupée PAR DATE à [première soirée, D] (bisect sur ses dates : un trou ne décale rien), signal de D si
    le module de la fiche, sur la série coupée à D, signale sa DERNIÈRE séance et que celle-ci est D (forme du
    détecteur, CCI distinct), `tenir` avec les réglages de `reglages_des_fiches` ; un jeton : au plus une position
    OUVERTE ou EN ATTENTE par fiche ; un soir « muet » (seuils inconnus) est un défaut. ⑦ UNITÉ — euros ; séances.
    ⑧ POURQUOI — A-923 : « le soir suit la fiche » ; le teneur en ligne de commande lit le cours maître du dépôt (2000
    et après), interdit par A-945. La coupe PAR DATE remplace la coupe par rang (20-11-2026) : avec des trous (point ⑤
    de la réparation), une coupe par rang aurait donné au teneur des séances FUTURES. ⑨ CE QUI CLOCHE — ① sans lecture
    du lecteur ni juge (comme le calibrage du teneur) : le contrôle « dans le CAC 40 » n'est pas joué. ② Le détecteur
    n'est pas rejoué ici (il l'est au maillon ①, soir). ③ Le calendrier du teneur est l'union des dates des séries
    coupées (`calendrier` sans lecture) : un trou commun à toutes les valeurs disparaîtrait du calendrier.
    ⑩ EFFET — aucun fichier. ⑪ TERMINAISON — rend la main ; une boucle par séance. [sort: non]"""
    import bisect
    TE, J, mod_pos, cours = ctx["TE"], ctx["J"], ctx["pos"], ctx["cours"]
    reglages = TE.reglages_des_fiches(R, [fiches[i] for i in ids])
    jours = [d for d in ctx["dates"] if d >= debut_du_soir]
    dates_de = {nom: [b["date"] for b in s] for nom, s in cours.items()}
    bas = {nom: bisect.bisect_left(dd, debut_du_soir) for nom, dd in dates_de.items()}
    sigs, rang = {}, 0
    for i in ids:
        sigs[i] = J.signal_de_la_fiche(R, fiches[i])
    positions, trades, ouvertures, defauts = [], [], {}, []
    for d in jours:
        haut = {nom: bisect.bisect_right(dd, d) for nom, dd in dates_de.items()}
        coupes = {nom: s[bas[nom]:haut[nom]] for nom, s in cours.items()}
        signaux = []
        for i in ids:
            for code in J.mnemoniques_de_l_univers(fiches[i]["univers"]):
                nom = ctx["mnemo"][code]
                n = haut[nom]
                if n == 0 or cours[nom][n - 1]["date"] != d:
                    continue                      # pas de séance D pour cette valeur (trou) : aucun signal ce soir
                if any(x["i"] == n - 1 for x in sigs[i](cours[nom][:n])):
                    rang += 1
                    signaux.append({"strategie": i, "valeur": nom, "date_signal": d, "cci": -100.0 - rang * 1e-3,
                                    "close": cours[nom][n - 1]["close"], "explication": "factice (A-945)"})
        r = TE.tenir(positions, coupes, signaux, None, mod_pos, reglages=reglages, base=R)
        positions, trades = r["positions"], trades + r["trades"]
        if r.get("muet"):
            defauts.append("%s : soir muet — %s" % (d, r.get("alerte", "")[:160]))
        for p in positions:
            if (p.get("statut") or "").strip() == "OUVERTE":
                cle = (p["strategie"], p["valeur"], p.get("date_signal"), p["comptabilite"])
                ouvertures[cle] = dict(p)        # le DERNIER état vu ouvert : l'échéance s'écrit quand elle est connue
        for i in ids:
            tenues = [p for p in positions if p.get("strategie") == i and p.get("comptabilite") == CT_UN_JETON(ctx)
                      and (p.get("statut") or "").strip() in ("OUVERTE", "EN_ATTENTE_ENTREE")]
            if len(tenues) > 1:
                defauts.append("%s : %s tient %d positions en un jeton" % (d, i, len(tenues)))
    return ouvertures, trades, defauts, len(jours)


def comparer_au_litteral(obtenu, attendu, cles):
    """Rend la liste des écarts entre un résultat obtenu et un attendu LITTÉRAL, clé par clé.
    ① RÔLE — la seule comparaison des cas connus. ② CONTEXTE D'APPEL — `jouer_les_cas_connus`. ③ ENTRÉE — deux
    dictionnaires, les clés à comparer. ④ CONDITIONS D'ENTRÉE — les clés de `cles` sont dans `attendu`. ⑤ SORTIE — UNE
    valeur : liste de textes « clé obtenu≠attendu », vide si tout concorde. [rend: 1] ⑥ TRAITEMENT — un nombre attendu
    se compare à 0,005 près (le demi-centime : les montants s'écrivent au centime, les prix à cinq décimales) ; un texte
    à l'identique ; une clé absente de l'obtenu est un écart. ⑦ UNITÉ — euros. ⑧ POURQUOI — réparation du 20-11-2026 :
    l'attendu est écrit à la main, jamais calculé. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    rendu = []
    for c in cles:
        a, o = attendu[c], obtenu.get(c)
        if isinstance(a, float):
            try:
                ok = abs(float(o) - a) < 0.005
            except (TypeError, ValueError):
                ok = False
        else:
            ok = o == a
        if not ok:
            rendu.append("%s %s≠%s" % (c, o, a))
    return rendu


def jouer_les_cas_connus(R, ctx, ME):
    """Joue chaque cas de CAS_CONNUS par le juge (`jouer`), par le teneur (`tenir`, séance par séance), par la mesure
    (`mesurer_une_strategie`) et par le témoin `_c5e10_sortie`, et confronte chacun aux LITTÉRAUX.
    ① RÔLE — l'étalonnage indépendant de ETA, POS et GAIN (réparation du 20-11-2026). ② CONTEXTE D'APPEL — `suite`, une
    fois. ③ ENTRÉE — R, le contexte (CT, J, pos, TE, mnemo), le module de mesure. ④ CONDITIONS D'ENTRÉE — R fabriqué
    (VALEURS_TTF 2024 à 2026, module factice) ; chaque code des cas est dans ctx["mnemo"]. ⑤ SORTIE — TROIS valeurs :
    {propriété: [défauts]} pour ETA, POS et GAIN ; {propriété: nombre de comparaisons} ; la liste des ÉCARTS CONNUS
    rencontrés (textes). [rend: 3] ⑥ TRAITEMENT — pour chaque cas : ① séries — la valeur du cas (séances CALME sauf
    `barres`, moins `trous`) et, si le cas le demande, une valeur « calendrier » complète ; ② une fiche factice (mode
    « date » au jour du signal, seuils +4,0 % / −2,5 %, horizon du cas) ; ③ ETA : `jouer` du juge doit rendre UNE
    opération égale à l'attendu (entrée, prix, motif, sortie, frais, net) ; ④ témoin : `_c5e10_sortie` aux mêmes
    seuils ; sans saut, il doit rendre la sortie du juge (motif, prix, date) ; avec saut, la sortie écrite en « temoin »
    (désaccord documenté) ; ⑤ POS : le soir rejoué doit rendre, dans CHAQUE comptabilité, UN trade égal à l'attendu
    (prix, motif, sortie, gain réel, prix et gain de convention) ; ⑥ GAIN : la mesure doit compter 1 opération par
    comptabilité, de cumul le gain réel (un jeton) ou de convention (jetons illimités) attendu. Un cas qui porte
    `ecart_connu` et rend EXACTEMENT cet écart-là est relevé comme ÉCART CONNU (ni vert, ni rouge) ; tout autre rendu est
    un défaut. ⑦ UNITÉ — euros ; seuils en pourcents écrits. ⑧ POURQUOI — superviseur R-759 du 20-11-2026 : « la vraie
    indépendance vient des CAS CONNUS » ; R-732 : K11 est calqué sur une vraie ligne du journal. ⑨ CE QUI CLOCHE —
    ① le témoin chiffre ses frais par `frais_aller_retour` : il ne témoigne que de la sortie ; ② le teneur tourne sans
    lecture (le calendrier est l'union des dates des séries : d'où la valeur « calendrier » de K07) ; ③ la fiche des cas
    n'est pas passée par le contrat (`manques_du_contrat`) : elle n'est pas au registre de R. ⑩ EFFET — charge le module
    C5 de R. ⑪ TERMINAISON — rend la main ; aucun de ses appels n'attend. [sort: non]"""
    CT, J, mod_pos = ctx["CT"], ctx["J"], ctx["pos"]
    C5 = J.charger_module(J.trouver(R, "MODULE_C5_ETENDU_10"), "c5_temoin_de_la_suite")
    d = {"ETA": [], "POS": [], "GAIN": []}
    n = {"ETA": 0, "POS": 0, "GAIN": 0}
    connus = []
    cles_op = ("date_entree", "pe", "motif", "date_sortie", "px", "frais", "net")
    cles_t = ("date_entree", "pe", "motif", "date_sortie", "px", "net", "px_conv", "net_conv")
    for cas in CAS_CONNUS:
        k, att, ec = cas["id"], cas["attendu"], cas.get("ecart_connu")
        nom = ctx["mnemo"][cas["code"]]
        calme = cas.get("calme", CALME)
        serie = []
        for jour in cas["jours"]:
            if jour in cas.get("trous", ()):
                continue
            o, h, l, c = cas["barres"].get(jour, calme)
            serie.append({"date": jour, "open": o, "high": h, "low": l, "close": c, "volume": 100000.0})
        cours = {nom: serie}
        if cas.get("calendrier"):
            cours[ctx["mnemo"][cas["calendrier"]]] = [{"date": jour, "open": 50.0, "high": 50.5, "low": 49.5,
                                                       "close": 50.0, "volume": 100000.0} for jour in cas["jours"]]
        f = {"id": "PROP-" + k, "nom": "factice cas connu " + k, "univers": cas["code"], "tp": "+4.0%", "sl": "-2.5%",
             "horizon": cas["horizon"], "periode": cas.get("periode", "%s -> %s" % (SUITE_DEBUT, SUITE_FIN)),
             "module_signal": MODULE, "fonction_signal": "signal", "indicateurs": "factice (cas connu)",
             "reglages_signal": json.dumps({"mode": "date", "jour": cas["signal"]}), "entree": "DÉFAUT",
             "donnees_demandees": "cours", "etat_vie": "QA"}
        # ③ ETA — LE JUGE
        juge_sortie = None
        try:
            sig = J.signal_de_la_fiche(R, f)
            ops, _inc = J.jouer(f, cours, ctx["mnemo"], sig, mod_pos, periode=J.porte_0(f)[2])
        except Exception as e:  # noqa: BLE001 — un juge qui tombe sur un cas connu est rouge
            ops = None
            d["ETA"].append("%s : le juge lève %s: %s" % (k, type(e).__name__, str(e)[:160]))
        if ops is not None:
            n["ETA"] += 1
            if len(ops) != 1:
                d["ETA"].append("%s : %d opération(s), 1 attendue" % (k, len(ops)))
            else:
                e1 = comparer_au_litteral(ops[0], att, cles_op)
                if e1 and ec and not comparer_au_litteral(ops[0], ec, cles_op):
                    connus.append("ETA %s : ÉCART CONNU — %s" % (k, ec["pourquoi"]))
                elif e1:
                    d["ETA"].append("%s (%s) : %s" % (k, cas["quoi"], " ; ".join(e1)))
                juge_sortie = {c: ops[0][c] for c in ("motif", "px", "date_sortie")}
        # ④ LE TÉMOIN DIFFÉRENTIEL (`_c5e10_sortie`, gardé indépendant : A-208 ⑤)
        try:
            i_sig = [b["date"] for b in serie].index(cas["signal"])
            t = C5._c5e10_sortie(serie, i_sig, valeur=nom, tp=0.04, sl=0.025, horizon=int(cas["horizon"]))
        except Exception as e:  # noqa: BLE001
            t = None
            d["ETA"].append("%s : le témoin lève %s: %s" % (k, type(e).__name__, str(e)[:160]))
        if t is not None:
            n["ETA"] += 1
            tem = {"motif": t["motif"], "px": float(t["px_out"]), "date_sortie": serie[t["i_out"]]["date"]}
            if cas["saut"]:
                e2 = comparer_au_litteral(tem, cas["temoin"], ("motif", "px", "date_sortie"))
                if e2:
                    d["ETA"].append("%s : témoin hors du désaccord documenté : %s" % (k, " ; ".join(e2)))
            elif juge_sortie is not None:
                e2 = comparer_au_litteral(tem, juge_sortie, ("motif", "px", "date_sortie"))
                if e2:
                    d["ETA"].append("%s : le témoin ne concorde pas avec le juge (cas sans saut) : %s"
                                    % (k, " ; ".join(e2)))
        # ⑤ POS — LE TENEUR, SÉANCE PAR SÉANCE
        try:
            sous = dict(ctx, cours=cours, dates=list(cas["jours"]))
            _ouv, trades, defauts, _nj = rejouer_le_soir(R, sous, [f["id"]], {f["id"]: f}, cas["jours"][0])
        except Exception as e:  # noqa: BLE001
            trades, defauts = [], ["le soir lève %s: %s" % (type(e).__name__, str(e)[:160])]
        for x in defauts:
            d["POS"].append("%s : %s" % (k, x))
        for compta in CT.COMPTABILITES:
            n["POS"] += 1
            miens = [t for t in trades if t.get("comptabilite") == compta]
            if len(miens) != 1:
                d["POS"].append("%s %s : %d trade(s), 1 attendu" % (k, compta, len(miens)))
                continue
            t = miens[0]
            vu = {"date_entree": t.get("date_entree"), "pe": t.get("prix_entree"), "motif": t.get("motif_sortie"),
                  "date_sortie": t.get("date_sortie"), "px": t.get("prix_sortie"), "net": t.get("pnl_net_eur"),
                  "px_conv": t.get("prix_sortie_convention"), "net_conv": t.get("pnl_net_convention_eur")}
            e3 = comparer_au_litteral(vu, att, cles_t)
            if e3 and ec and not comparer_au_litteral(vu, ec, cles_t):
                connus.append("POS %s %s : ÉCART CONNU — %s" % (k, compta, ec["pourquoi"]))
            elif e3:
                d["POS"].append("%s %s (%s) : %s" % (k, compta, cas["quoi"], " ; ".join(e3)))
        # ⑥ GAIN — LA MESURE
        try:
            mesures = ME.mesurer_une_strategie(trades, {"id": f["id"], "nom": f["nom"]})
        except Exception as e:  # noqa: BLE001
            mesures = []
            d["GAIN"].append("%s : la mesure lève %s: %s" % (k, type(e).__name__, str(e)[:160]))
        for _lib, compta, st in mesures:
            n["GAIN"] += 1
            cle = "net" if compta == CT.UN_JETON else "net_conv"      # A-330 : illimités au prix de convention
            vu = {"n": st["n"], cle: st["cumul"]}
            e4 = comparer_au_litteral(vu, dict(att, n=1), ("n", cle))
            if e4 and ec and not comparer_au_litteral(vu, dict(ec, n=1), ("n", cle)):
                connus.append("GAIN %s %s : ÉCART CONNU — %s" % (k, compta, ec["pourquoi"]))
            elif e4:
                d["GAIN"].append("%s %s (%s) : mesure %s" % (k, compta, cas["quoi"], " ; ".join(e4)))
    return d, n, connus


def accidents_vus(cours, dates):
    """Compte, DANS LES COURS fabriqués (pas dans le tirage), chaque catégorie d'accident : saut d'ouverture vers le bas,
    vers le haut, double touche, trou.
    ① RÔLE — la propriété ACC (réparation du 20-11-2026, point ⑤). ② CONTEXTE D'APPEL — `suite`. ③ ENTRÉE — les cours
    {nom: série}, le calendrier fabriqué. ④ CONDITIONS D'ENTRÉE — séries triées, non vides. ⑤ SORTIE — UNE valeur :
    {catégorie: nombre}. [rend: 1] ⑥ TRAITEMENT — saut bas : ouverture au moins 3 % sous la clôture précédente · saut
    haut : au moins 4,5 % au-dessus · double : plus haut au moins 4,5 % au-dessus de l'ouverture ET plus bas au moins 3 %
    au-dessous (les deux seuils des fiches ordinaires, +4 % / −2,5 %, touchés le même jour) · trou : une date du
    calendrier absente de la série, après sa première séance. ⑦ UNITÉ — séances. ⑧ POURQUOI — mesurer ce que les cours
    CONTIENNENT, pas ce que le générateur croit avoir fait. ⑨ CE QUI CLOCHE — la marche ordinaire peut, rarement,
    produire un « saut bas » de 3 % : le compte est un minimum, pas le compte exact des accidents injectés. ⑩ EFFET —
    aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    vus = {"saut_bas": 0, "saut_haut": 0, "double": 0, "trou": 0}
    for s in cours.values():
        presentes = {b["date"] for b in s}
        vus["trou"] += sum(1 for x in dates if x not in presentes and x >= s[0]["date"])
        for a, b in zip(s, s[1:]):
            if b["open"] <= a["close"] * 0.97:
                vus["saut_bas"] += 1
            if b["open"] >= a["close"] * 1.045:
                vus["saut_haut"] += 1
            if b["high"] >= b["open"] * 1.045 and b["low"] <= b["open"] * 0.97:
                vus["double"] += 1
    return vus


# LES DEUX CONTRÔLES AJOUTÉS À `defauts_d_un_trade` (I1 de Cowork, relectures de travail-proprietes-3 et -4) SE
# RETIRENT PAR LA LIGNE DE COMMANDE, et seulement sous les sabotages S-I1a et S-I1b : « --sans-controle=saut » retire
# le refus d'un SL sur une séance ouverte au-dessus de l'objectif, « --sans-controle=echeance » celui d'une sortie sur
# seuil après l'échéance. Raison : un contrôle d'épreuve qu'aucun sabotage ne retire n'est pas prouvé (R-731).
SANS_CONTROLE = {a.split("=", 1)[1] for a in sys.argv if a.startswith("--sans-controle=")}


def defauts_d_un_trade(t, serie, tp, sl, h, calendrier):
    """Rend les défauts d'UN trade du soir rejoué au regard de SA série, par des PROPRIÉTÉS (inégalités), sans rejouer
    la vente : la sortie est la première séance qui touche un seuil, au bon prix, et rien avant elle.
    ① RÔLE — POS sur les cours fabriqués, sans `vendre` (réparation du 20-11-2026). ② CONTEXTE D'APPEL — `suite`.
    ③ ENTRÉE — le trade (colonnes du journal), la série de la valeur, tp et sl en fractions, l'horizon (entier ou
    HORIZON_AUCUNE), le calendrier fabriqué. ④ CONDITIONS D'ENTRÉE — le trade porte ses colonnes (PREUVE l'a vérifié).
    ⑤ SORTIE — DEUX valeurs : la liste des défauts (textes), et vrai si la fenêtre du trade contient un trou (l'échéance
    n'y est alors pas jugée). [rend: 2] ⑥ TRAITEMENT — objectif ≈ pe×(1+tp), stop ≈ pe×(1−sl), avec une ZONE MORTE de
    1e-3 € : on n'affirme « touché » ou « pas touché » que hors de cette zone (l'arrondi à cinq décimales du circuit,
    n°311, n'est pas recopié) · ① l'ouverture de la séance d'achat est pe · ② aucune séance de l'achat à la veille de la
    sortie ne touche un seuil (ouverture, plus bas, plus haut) · ③ la séance de sortie justifie le motif : SL_GAP
    ouverture sous le stop et px = ouverture ; TP_GAP ouverture au-dessus de l'objectif et px = ouverture ; SL plus bas
    sous le stop, px ≈ stop, ET ouverture SOUS l'objectif (sinon R-607 ③ voulait TP_GAP : I1 de Cowork, 20-11-2026) ;
    TP plus haut au-dessus de l'objectif, plus bas AU-DESSUS du stop (sinon R-602 voulait SL), px ≈ objectif ; HORIZON
    aucun seuil, px = clôture et, sans trou dans la fenêtre, h lignes après l'achat · ④ une sortie sur seuil (SL_GAP,
    TP_GAP, SL, TP) d'un horizon entier se fait au plus h LIGNES après l'achat — `vendre` ne teste que serie[j:j+1+h]
    (I1 de Cowork, 20-11-2026 : une sortie TP après l'échéance passait). Les contrôles ③-SL-ouverture et ④ se retirent
    par « --sans-controle=saut » et « --sans-controle=echeance » (sabotages S-I1a, S-I1b) ; ils sont éprouvés par
    `cas_limites_des_defauts`.
    ⑦ UNITÉ — euros ; séances. ⑧ POURQUOI — le superviseur R-759 du 20-11-2026 refuse un oracle réécrit (R-708) ; une
    propriété n'est pas une vente : elle dit ce que toute vente correcte respecte (R-602, R-607, R-608). ⑨ CE QUI
    CLOCHE — ① l'échéance d'une fenêtre à trou n'est pas jugée ici (R-112 non appliquée par le code : cas K07) ; ② la
    zone morte laisse passer un écart de moins d'un millième d'euro, et elle CACHE L'ÉGALITÉ : un seuil touché pile
    (plus haut = objectif) n'est ni « touché » ni « pas touché » ici, si bien qu'un « > » mis pour « >= » dans
    `tester_seance` passe (relecteur neuf du 20-11-2026). La tolérance est gardée ; l'égalité est éprouvée par les cas
    connus K12 à K15 et les sabotages S-EG1 à S-EG4. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    zm = 1e-3
    pe, px, motif = float(t["prix_entree"]), float(t["prix_sortie"]), t["motif_sortie"]
    obj, stp = pe * (1 + tp), pe * (1 - sl)
    dd = [b["date"] for b in serie]
    if t["date_entree"] not in dd or t["date_sortie"] not in dd:
        return ["entrée %s ou sortie %s hors de la série" % (t["date_entree"], t["date_sortie"])], False
    a, z = dd.index(t["date_entree"]), dd.index(t["date_sortie"])
    trou = calendrier.index(dd[z]) - calendrier.index(dd[a]) != z - a
    rendu = []
    if abs(serie[a]["open"] - pe) > zm:
        rendu.append("prix d'entrée %s, ouverture %s" % (pe, serie[a]["open"]))
    if z < a:
        return rendu + ["sortie avant l'entrée"], trou
    for b in serie[a:z]:
        if b["open"] <= stp - zm or b["low"] <= stp - zm or b["open"] >= obj + zm or b["high"] >= obj + zm:
            rendu.append("le %s touche déjà un seuil (o %s h %s l %s ; objectif %.4f stop %.4f), sortie %s %s le %s" % (
                b["date"], b["open"], b["high"], b["low"], obj, stp, motif, px, t["date_sortie"]))
            break
    b = serie[z]
    if motif == "SL_GAP":
        ok = b["open"] <= stp + zm and abs(px - b["open"]) <= zm
    elif motif == "TP_GAP":
        ok = b["open"] >= obj - zm and abs(px - b["open"]) <= zm
    elif motif == "SL":
        ok = b["open"] > stp - zm and b["low"] <= stp + zm and abs(px - stp) <= zm and \
            ("saut" in SANS_CONTROLE or b["open"] < obj + zm)
    elif motif == "TP":
        ok = stp - zm < b["open"] < obj + zm and b["low"] > stp - zm and b["high"] >= obj - zm and abs(px - obj) <= zm
    elif motif == "HORIZON":
        ok = b["open"] > stp - zm and b["low"] > stp - zm and b["open"] < obj + zm and b["high"] < obj + zm and \
            abs(px - b["close"]) <= zm and (trou or not isinstance(h, int) or z - a == h)
    else:
        ok = False
    if not ok:
        rendu.append("sortie %s à %s le %s non justifiée par la séance (o %s h %s l %s c %s ; objectif %.4f stop %.4f ;"
                     " %d ligne(s) après l'achat, horizon %s)" % (motif, px, t["date_sortie"], b["open"], b["high"],
                                                                  b["low"], b["close"], obj, stp, z - a, h))
    if motif in ("SL_GAP", "TP_GAP", "SL", "TP") and isinstance(h, int) and not isinstance(h, bool) and z - a > h \
            and "echeance" not in SANS_CONTROLE:
        rendu.append("sortie %s le %s, %d ligne(s) après l'achat : au-delà de l'échéance (horizon %d)" % (
            motif, t["date_sortie"], z - a, h))
    return rendu, trou


def cas_limites_des_defauts():
    """Rend les écarts de `defauts_d_un_trade` sur QUATRE trades écrits à la main, aux verdicts écrits d'avance.
    ① RÔLE — éprouver le contrôle de POS lui-même (I1 de Cowork, relectures de travail-proprietes-3 et -4, 20-11-2026).
    ② CONTEXTE D'APPEL — `suite`, juste après les cas connus. ③ ENTRÉE — aucune. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs : la liste des écarts (textes préfixés I1-C1 à I1-C4), le nombre de cas joués. [rend: 2]
    ⑥ TRAITEMENT — achat à 100,00 le 2024-01-08, objectif 4 % (104,00), stop 2,5 % (97,50) · I1-C1 : SL à 97,50 sur
    une séance ouverte à 106,00 (R-607 ③ voulait TP_GAP à 106,00) → DOIT être refusé · I1-C2 : horizon 3, TP à 104,00
    sur la QUATRIÈME séance après l'achat (`vendre` vendait à la clôture de la troisième, motif HORIZON) → DOIT être
    refusé · I1-C3 : le HORIZON juste de C2 → DOIT passer · I1-C4 : le TP_GAP juste de C1 → DOIT passer.
    ⑦ UNITÉ — euros ; séances. ⑧ POURQUOI — les deux trades faux de Cowork rendaient une liste vide (« C1 SL au lieu
    de TP_GAP (R-607 ③) : ([], False) », « C2 TP après l'échéance (horizon 3) : ([], False) ») ; les deux témoins
    justes gardent le contrôle de sur-détecter. ⑨ CE QUI CLOCHE — les cas sont reconstruits d'après la description de
    Cowork, son script n'étant pas au dépôt. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    dates = ["2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12"]
    calme = [dict(date=x, open=100.0, high=101.0, low=99.0, close=100.5) for x in dates]
    saut = [calme[0], dict(date=dates[1], open=106.0, high=107.0, low=97.0, close=98.0)] + calme[2:]
    tard = calme[:4] + [dict(date=dates[4], open=100.0, high=104.5, low=99.0, close=103.0)]

    def tr(motif, px, sortie):
        """Un trade minimal. ① RÔLE — fabriquer. ② CONTEXTE D'APPEL — `cas_limites_des_defauts`. ③ ENTRÉE — motif,
        prix, date de sortie. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : dict. [rend: 1] ⑥ TRAITEMENT — —.
        ⑦ UNITÉ — euros. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main.
        [sort: non]"""
        return {"prix_entree": "100.0", "prix_sortie": str(px), "motif_sortie": motif, "date_entree": dates[0],
                "date_sortie": sortie}
    cas = [("I1-C1 SL au lieu de TP_GAP (R-607 ③)", tr("SL", 97.5, dates[1]), saut, 20, True),
           ("I1-C2 TP après l'échéance (horizon 3)", tr("TP", 104.0, dates[4]), tard, 3, True),
           ("I1-C3 témoin HORIZON juste", tr("HORIZON", 100.5, dates[3]), tard, 3, False),
           ("I1-C4 témoin TP_GAP juste", tr("TP_GAP", 106.0, dates[1]), saut, 20, False)]
    ecarts = []
    for nom, t, serie, h, faux in cas:
        rendu, _trou = defauts_d_un_trade(t, serie, 0.04, 0.025, h, dates)
        if faux and not rendu:
            ecarts.append("%s : trade faux ACCEPTÉ par defauts_d_un_trade" % nom)
        if not faux and rendu:
            ecarts.append("%s : trade juste REFUSÉ par defauts_d_un_trade : %s" % (nom, rendu[0]))
    return ecarts, len(cas)


def CT_UN_JETON(ctx):
    """Rend le nom de la comptabilité « un jeton », LU au contrat. ① RÔLE — R-708. ② CONTEXTE D'APPEL — `suite`,
    `rejouer_le_soir`. ③ ENTRÉE — le contexte. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : texte. [rend: 1]
    ⑥ TRAITEMENT — lire. ⑦ UNITÉ — —. ⑧ POURQUOI — le nom vit au contrat. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    return ctx["CT"].UN_JETON


def suite(R, racine):
    """Les maillons ② juge, ③ positions, ④ mesure, en mémoire sur le dépôt fabriqué R ; ETA, JUG, POS, GAIN, PREUVE,
    ACC. Affiche un JSON.
    ① RÔLE — étendre l'épreuve par propriétés à la suite de la chaîne (A-945). ② CONTEXTE D'APPEL — `__main__`
    « --suite » (avec « --sans-accidents » sous le sabotage S-ACC). ③ ENTRÉE — R, la racine réelle (pour la garde).
    ④ CONDITIONS D'ENTRÉE — R fabriqué par `fabriquer_r`. ⑤ SORTIE — Aucune valeur ; un JSON {proprietes, refus,
    conformes, ecarts_connus} en dernière ligne. [rend: 0] ⑥ TRAITEMENT — ① cours fabriqués aux jours ouvrés
    2024-2025, AVEC accidents (sauts, doubles touches, trous) · ② ETA : les CAS CONNUS (`jouer_les_cas_connus`) — le
    juge, le témoin `_c5e10_sortie`, et, pour POS et GAIN, le teneur et la mesure — confrontés à des LITTÉRAUX ; un ETA
    rouge rend JUG non mesurée (un instrument non étalonné ne juge pas) · ③ JUG : chaque fiche PROP-, puis chaque fiche
    fautive de MUTATIONS, par `juge_une_fiche` ; les N_JUGES premières conformes passent aussi par `juger` · ④ POS : le
    soir rejoué (`rejouer_le_soir`) sur ORD, les limites, les QA et N_SOIR_HASARD tirées ; chaque trade est confronté
    à SA série par `defauts_d_un_trade` (propriétés, sans vente rejouée) ; chaque position, à son dernier état ouvert :
    Open J+1 du signal, objectif et stop de `seuils_de_vente`, échéance (quand elle est écrite en date et que la fenêtre
    n'a pas de trou) à la h-ième séance après l'achat, valeur dans l'univers · ⑤ GAIN : les frais implicites de chaque
    trade dans leurs bornes (0,15 % par ordre écrit ici, plus 0,4 % de taxe au plus), le prix de convention au seuil du
    motif ; la mesure (`MESURER…mesurer_une_strategie`) de chaque fiche et de chaque comptabilité égale la somme des
    gains ÉCRITS · ⑥ PREUVE : grille aux seize contrôles et rapport de `juger` non vide ; chaque trade porte toutes les
    colonnes de CONTRATS.TRADE, chaque position celles de CONTRATS.POSITION ; chaque couple (fiche, comptabilité) qui a
    des trades a sa mesure, au même nombre · et ACC : `accidents_vus` ≥ 1 par catégorie, au moins un trade SL_GAP et un
    TP_GAP, au moins un trade sorti sur une séance de double touche accidentée (objectif et stop atteints, ouverture
    entre les deux, et double touche au sens d'`accidents_vus`), au moins un trade dont la fenêtre enjambe un trou
    (« --accidents-avant-le-soir », sabotage S-ACC2, rejette doubles touches et trous avant le soir rejoué).
    ⑦ UNITÉ — euros ; séances.
    ⓪ A945 : une garde d'audit (sys.addaudithook) REFUSE toute ouverture de fichier ou de dossier sous la racine du
    dépôt réel et la relève — R n'en porte que des liens, un programme qui suivrait le lien jusqu'au dépôt (cours,
    registre réels) serait arrêté et dénoncé.
    ⑧ POURQUOI — A-923, A-945. ⑨ CE QUI CLOCHE — voir ⑨ de `juge_une_fiche` et de `rejouer_le_soir` ; la garde ne voit
    que les ouvertures faites par Python (open, listdir, scandir), pas un sous-processus. ⑩ EFFET — charge les modules
    de R. ⑪ TERMINAISON — rend la main. [sort: non]"""
    racine = os.path.abspath(racine)
    interdites, lus = [], [0]

    def garde(evt, args):
        """Refuse toute ouverture sous la racine réelle. ① RÔLE — A945. ② CONTEXTE D'APPEL — chaque événement d'audit.
        ③ ENTRÉE — l'événement, ses arguments. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune. [rend: 0]
        ⑥ TRAITEMENT — chemin absolu (sans résoudre les liens) comparé à la racine. ⑦ UNITÉ — —. ⑧ POURQUOI — A-945.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — note ; lève PermissionError. ⑪ TERMINAISON — rend la main. [sort: non]"""
        if evt in ("open", "os.listdir", "os.scandir") and args and isinstance(args[0], (str, bytes)):
            lus[0] += 1
            chemin = os.path.abspath(os.fsdecode(args[0]))
            if chemin == racine or chemin.startswith(racine + os.sep):
                interdites.append(chemin)
                raise PermissionError("A-945 : lecture dans le dépôt réel refusée : %s" % chemin)
    sys.addaudithook(garde)
    sys.path.insert(0, os.path.join(R, "programmes"))
    import CONTRATS_DES_FICHIERS as CT
    import JUGE_DES_STRATEGIES as J
    ctx = {"CT": CT, "J": J}
    ctx["pos"] = J.charger_module(J.trouver(R, "MODULE_POSITIONS.py"), "pos_de_la_suite")
    ctx["jug"] = J.charger_module(J.trouver(R, "MODULE_JUGEMENT.py"), "jug_de_la_suite")
    f_sta = J.trouver(R, "MODULE_STATISTIQUES")
    ctx["sta"] = J.charger_module(f_sta, "sta_de_la_suite") if f_sta else None
    ctx["TE"] = J.charger_module(os.path.join(R, TENIR), "tenir_de_la_suite")
    ME = J.charger_module(J.trouver(R, "MESURER_LA_PERFORMANCE"), "mesure_de_la_suite")
    ctx["table"] = ctx["jug"].table_de_la_loi(open(os.path.join(R, "gouvernance", "REGISTRE_REGLES.md"),
                                                   encoding="utf-8").read())
    ctx["mnemo"] = J.table_mnemoniques(J.trouver(R, "REFERENTIEL_VALEURS"))
    ctx["dates"] = jours_ouvres(SUITE_DEBUT, SUITE_FIN)
    avec_accidents = "--sans-accidents" not in sys.argv       # S-ACC : le générateur sans ses accidents
    avant = SOIR_DEBUT if "--accidents-avant-le-soir" in sys.argv else None   # S-ACC2
    ctx["cours"] = cours_fabriques(list(CODES_FAB), ctx["mnemo"], ctx["dates"], accidents=avec_accidents, avant=avant)
    ctx["seances"] = set(ctx["dates"])
    mod_pos = ctx["pos"]
    fiches = {i: f for i, f in CT.fiches_du_registre(os.path.join(R, REG)).items() if i.startswith("PROP-")}
    d = {p: [] for p in PROPRIETES_SUITE}
    n = {p: 0 for p in PROPRIETES_SUITE}
    refus = []
    # ② ETA, ET L'ÉTALONNAGE DE POS ET GAIN — LES CAS CONNUS, AUX RÉSULTATS ÉCRITS D'AVANCE (réparation du 20-11-2026 :
    # le rejeu par `vendre`, `frais_aller_retour` et `prix_de_convention` est retiré, il était juge et partie)
    try:
        dk, nk, ecarts_connus = jouer_les_cas_connus(R, ctx, ME)
    except Exception as e:  # noqa: BLE001 — l'étalonnage qui tombe est rouge
        dk, nk, ecarts_connus = {"ETA": ["cas connus en échec : %s: %s" % (type(e).__name__, str(e)[:200])],
                                 "POS": [], "GAIN": []}, {"ETA": 0, "POS": 0, "GAIN": 0}, []
    for p in ("ETA", "POS", "GAIN"):
        d[p] += dk[p]
        n[p] += nk[p]
    # LE CONTRÔLE DE POS ÉPROUVÉ SUR SES CAS LIMITES (I1 de Cowork) : deux trades faux refusés, deux justes acceptés.
    di, ni = cas_limites_des_defauts()
    d["POS"] += di
    n["POS"] += ni
    etalonne = not d["ETA"] and n["ETA"] > 0
    # ② JUG ET SA PREUVE — toutes les fiches, puis une case fautive à la fois sur PROP-ORD
    conformes = []
    if etalonne:
        tete = [i for i in ("PROP-ORD", "PROP-Q1", "PROP-Q2") if i in fiches]     # passées par `juger` d'abord
        candidats = [(i, fiches[i]) for i in tete + sorted(set(fiches) - set(tete))]
        candidats += [("PROP-ORD~%s=%r" % (c, v), dict(fiches["PROP-ORD"], **{c: v})) for c, v in MUTATIONS]
        juges = 0
        for i, f in candidats:
            n["JUG"] += 1
            avec = "~" not in i and juges < N_JUGES and (i in tete or i.startswith("PROP-H"))
            genre, texte, ops, g, rapport = juge_une_fiche(f, R, ctx, avec)
            if genre == "PLANTE":
                d["JUG"].append("%s : %s" % (i, texte))
                continue
            if genre == "REFUS":
                if "~" not in i:
                    refus.append({"maillon": "② juge", "fiche": i, "motif": texte})
                continue
            if "~" in i:
                d["JUG"].append("%s : fiche fautive jugée « %s »" % (i, texte))
                continue
            conformes.append(i)
            n["PREUVE"] += 1
            manque = [c for c in CT.CONTROLES_DU_VERDICT if (g.get("controles") or {}).get(c, {}).get("etat") not in
                      CT.ETATS_D_UN_CONTROLE]
            if manque:
                d["PREUVE"].append("② %s : contrôles sans état %s" % (i, manque[:4]))
            if avec:
                juges += 1
                if not rapport.strip():
                    d["PREUVE"].append("② %s : juger n'a rien affiché" % i)
    # ③ POS — LE SOIR REJOUÉ, PUIS ④ GAIN ET LA MESURE
    lisibles = []
    for i in sorted(fiches):
        try:
            if CT.manques_du_contrat(fiches[i], R, J=J, mod_pos=mod_pos):
                continue
            J.lecture_du_soir(R, fiches[i])
        except Exception:  # noqa: BLE001 — une fiche que le soir refuse n'est pas suivie (le contrat le dit, SIL)
            continue
        lisibles.append(i)
    ids = [i for i in lisibles if not i.startswith("PROP-H")] + [i for i in lisibles if i.startswith("PROP-H")][
        :N_SOIR_HASARD]
    try:
        ouvertures, trades, defauts, nj = rejouer_le_soir(R, ctx, ids, fiches)
    except Exception as e:  # noqa: BLE001
        ouvertures, trades, defauts, nj = {}, [], ["le soir rejoué lève %s: %s" % (type(e).__name__, str(e)[:200])], 0
    d["POS"] += defauts
    lect = {i: J.lecture_du_soir(R, fiches[i]) for i in ids}
    jours = ctx["dates"][len(ctx["dates"]) - nj:] if nj else []
    nets, motifs, fenetres_a_trou = [], {}, 0
    sur_double, sur_trou = 0, 0           # ACC, compté dans les POSITIONS (défaut mineur du relecteur, 20-11-2026)
    for (i, nom, d_sig, compta), p in sorted(ouvertures.items()):
        n["POS"] += 1
        tp, sl, h = lect[i]
        univ = {ctx["mnemo"][c] for c in J.mnemoniques_de_l_univers(fiches[i]["univers"])}
        if nom not in univ:
            d["POS"].append("%s : position sur %s hors univers" % (i, nom))
        if d_sig in jours and jours.index(d_sig) + 1 < len(jours) and p.get("date_entree") != jours[
                jours.index(d_sig) + 1]:
            d["POS"].append("%s %s : signal du %s, entrée le %s (Open J+1 attendu)" % (i, nom, d_sig,
                                                                                   p.get("date_entree")))
        pe = float(p["prix_entree"])
        attendus = mod_pos.seuils_de_vente(pe, tp, sl)
        if abs(float(p["tp"]) - attendus[0]) > 1e-4 or abs(float(p["sl"]) - attendus[1]) > 1e-4:
            d["POS"].append("%s %s : objectif %s stop %s, attendus %s %s" % (i, nom, p["tp"], p["sl"], *attendus))
        serie = ctx["cours"][nom]
        dd = [b["date"] for b in serie]
        fin = (p.get("horizon_fin") or "").strip()
        a_trou = False
        if isinstance(h, int) and p.get("date_entree") in dd and dd.index(p["date_entree"]) + h < len(dd):
            ia = dd.index(p["date_entree"])
            a_trou = ctx["dates"].index(dd[ia + h]) - ctx["dates"].index(dd[ia]) != h
        if a_trou:
            fenetres_a_trou += 1      # R-112 non appliquée par le code (cas K07) : l'échéance n'est pas jugée ici
        elif isinstance(h, int) and len(fin) == 10 and fin[4] == "-" and p.get("date_entree") in dd and \
                dd.index(p["date_entree"]) + h < len(dd) and fin != dd[dd.index(p["date_entree"]) + h]:
            d["POS"].append("%s %s : échéance %s, attendue %s (%d séances après l'achat)" % (
                i, nom, p.get("horizon_fin"), dd[dd.index(p["date_entree"]) + h], h))
        n["PREUVE"] += 1
        manque = [c for c in CT.POSITION if c not in p]
        if manque:
            d["PREUVE"].append("③ position %s %s : colonnes absentes %s" % (i, nom, manque))
    for t in trades:
        n["POS"] += 1
        n["GAIN"] += 1
        n["PREUVE"] += 1
        i, nom = t.get("strategie"), t.get("valeur")
        manque = [c for c in CT.TRADE if c not in t or (c in ("strategie", "valeur", "date_entree", "date_sortie",
                                                                 "prix_entree", "prix_sortie", "motif_sortie",
                                                                 "pnl_net_eur", "comptabilite", "bareme_reel")
                                                         and not str(t.get(c, "")).strip())]
        if manque:
            d["PREUVE"].append("③ trade %s %s %s : colonnes absentes ou vides %s" % (i, nom, t.get("date_entree"),
                                                                                   manque))
            continue          # un trade sans sa preuve ne se recalcule pas : il est déjà rouge (PREUVE)
        if i not in lect:
            d["POS"].append("trade d'une fiche non suivie : %s" % i)
            continue
        tp, sl, h = lect[i]
        serie = ctx["cours"][nom]
        if t.get("date_entree", "") < SOIR_DEBUT:
            d["POS"].append("%s %s : entrée %s avant les séances rejouées" % (i, nom, t.get("date_entree")))
            continue
        fautes, a_trou = defauts_d_un_trade(t, serie, tp, sl, h, ctx["dates"])
        fenetres_a_trou += a_trou
        sur_trou += a_trou
        if t["date_sortie"] in [b["date"] for b in serie]:
            bz = serie[[b["date"] for b in serie].index(t["date_sortie"])]
            pe_t = float(t["prix_entree"])
            # DOUBLE TOUCHE, SANS SAUT : la séance de sortie atteint l'objectif ET le stop, ouverture entre les deux
            # (R-602 : SL compté), ET c'est une double touche au sens d'`accidents_vus` (plus haut ≥ ouverture × 1,045,
            # plus bas ≤ ouverture × 0,97). Mesurée sur les cours, pas lue dans le motif : un motif faux ne la fabrique
            # pas. Pourquoi la seconde condition : la marche ordinaire produit seule quelques doubles touches de
            # position (6 sous S-ACC, 11 sous S-ACC2, mesuré le 20-11-2026) ; sans elle, le compte ne disait pas si
            # une position traverse un ACCIDENT injecté.
            if bz["high"] >= pe_t * (1 + tp) and bz["low"] <= pe_t * (1 - sl) and \
                    pe_t * (1 - sl) < bz["open"] < pe_t * (1 + tp) and \
                    bz["high"] >= bz["open"] * 1.045 and bz["low"] <= bz["open"] * 0.97:
                sur_double += 1
        motifs[t["motif_sortie"]] = motifs.get(t["motif_sortie"], 0) + 1
        for x in fautes:
            d["POS"].append("%s %s %s : %s" % (i, nom, t["date_entree"], x))
        # ⑤ GAIN, PAR TRADE — DES BORNES, PAS UN RECALCUL : les frais implicites (gain brut − gain écrit) sont au moins le
        # courtage, 0,15 % de chaque ordre, et au plus le courtage plus 0,4 % de taxe à l'achat (BAREME_FRAIS.csv,
        # lignes REEL). Le taux est ÉCRIT ICI, jamais relu dans MODULE_POSITIONS ; 100 000 € engagés par trade (R-201).
        # Le prix de convention est le stop (motif SL…), l'objectif (TP…), le prix réel (HORIZON) — R-607 ⑤.
        pe, q = float(t["prix_entree"]), 100000.0 / float(t["prix_entree"])
        for px_c, net_c, lib in ((float(t["prix_sortie"]), float(t["pnl_net_eur"]), "réel"),
                                 (float(t["prix_sortie_convention"]), float(t["pnl_net_convention_eur"]),
                                  "convention")):
            fr = q * (px_c - pe) - net_c
            plancher = 0.0015 * (100000.0 + q * px_c)
            if not plancher - 0.01 <= fr <= plancher + 0.004 * 100000.0 + 0.01:
                d["GAIN"].append("%s %s %s : frais implicites %s %.2f € hors de [%.2f ; %.2f]" % (
                    i, nom, t["date_entree"], lib, fr, plancher, plancher + 400.0))
        conv, m = float(t["prix_sortie_convention"]), t["motif_sortie"]
        voulu = pe * (1 - sl) if m.startswith("SL") else (pe * (1 + tp) if m.startswith("TP") else
                                                          float(t["prix_sortie"]))
        if abs(conv - voulu) > 1e-3:
            d["GAIN"].append("%s %s %s : prix de convention %s pour %s, attendu %.4f (R-607 ⑤)" % (
                i, nom, t["date_entree"], conv, m, voulu))
        cle = "pnl_net_eur" if t["comptabilite"] == CT.UN_JETON else "pnl_net_convention_eur"
        nets.append((i, t["comptabilite"], float(t[cle])))
    vus_mesure = set()
    for i in ids:
        for _lib, compta, st in ME.mesurer_une_strategie(trades, {"id": i, "nom": fiches[i]["nom"]}):
            miens = [x for x in nets if x[0] == i and x[1] == compta]
            somme = sum(x[2] for x in miens)          # le gain ÉCRIT au journal (A-330 : illimités en convention)
            if st["n"]:
                vus_mesure.add((i, compta))
            n["GAIN"] += 1
            if st["n"] != len(miens) or abs(st["cumul"] - somme) > 0.011 * max(1, len(miens)):
                d["GAIN"].append("④ %s %s : mesure %d op., %.2f € · recalcul %d op., %.2f €" % (
                    i, compta, st["n"], st["cumul"], len(miens), somme))
    a_mesurer = {(t.get("strategie"), t.get("comptabilite")) for t in trades if t.get("strategie") in ids}
    n["PREUVE"] += 1
    if a_mesurer - vus_mesure:
        d["PREUVE"].append("④ comptes sans mesure : %s" % sorted(a_mesurer - vus_mesure)[:4])
    if not trades:
        d["POS"].append("aucun trade clôturé en %d séances : le soir n'a rien mesuré" % nj)
    # ⑦ ACC — CHAQUE CATÉGORIE D'ACCIDENT EST DANS LES COURS, ET LES SORTIES À SAUT ARRIVENT AU SOIR
    vus = accidents_vus(ctx["cours"], ctx["dates"])
    n["ACC"] = len(vus) + 4
    # LES POSITIONS D'ABORD (le détail n'affiche que les quatre premiers défauts) : un accident présent dans les cours
    # mais qu'aucune position ne traverse n'éprouve rien.
    if sur_double < 1:
        d["ACC"].append("aucune position sortie sur double touche (séance de sortie accidentée, à l'objectif ET au "
                        "stop, sans saut)")
    if sur_trou < 1:
        d["ACC"].append("aucune position dont la fenêtre traverse un trou de séance")
    for g, nb in sorted(vus.items()):
        if nb < 1:
            d["ACC"].append("aucun « %s » dans les cours fabriqués" % g)
    for m in ("SL_GAP", "TP_GAP"):
        if motifs.get(m, 0) < 1:
            d["ACC"].append("aucun trade du soir sorti en %s" % m)
    n["A945"] = lus[0]
    d["A945"] = ["%d ouverture(s) refusée(s) dans le dépôt réel, dont %s" % (len(interdites), sorted(set(
        os.path.relpath(x, racine) for x in interdites))[:3])] if interdites else []
    etats = {}
    for p in PROPRIETES_SUITE:
        if p == "JUG" and not etalonne:
            etats[p] = ["NON MESURÉE", "instrument non étalonné (ETA) : le juge ne juge pas"]
            continue
        etats[p] = ["ROUGE" if d[p] else ("VERT" if n[p] else "NON MESURÉE"),
                    "%d mesure(s) ; %s" % (n[p], " ; ".join(d[p][:4]) or "aucun défaut")]
    etats["POS"][1] += " · %d fiche(s) suivie(s), %d séance(s), %d position(s), %d trade(s) ; %d fenêtre(s) à " \
        "trou (échéance non jugée, R-112)" % (len(ids), nj, len(ouvertures), len(trades), fenetres_a_trou)
    etats["ACC"][1] += " · accidents vus %s · sorties %s · positions sorties sur double touche %d · traversant un " \
        "trou %d" % (", ".join("%s %d" % x for x in sorted(vus.items())),
                     ", ".join("%s %d" % x for x in sorted(motifs.items())), sur_double, sur_trou)
    print(json.dumps({"proprietes": etats, "refus": refus, "conformes": conformes, "ecarts_connus": ecarts_connus},
                     ensure_ascii=False))


def passage_suite(racine, base, fiches, sabotage):
    """Un passage de la suite (sans sabotage, ou avec UN sabotage de SABOTAGES_SUITE) ; rend {propriété: [état,
    détail]} et les refus.
    ① RÔLE — fabriquer R, poser le sabotage, lancer `--suite` en processus neuf, effacer R. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — racine, dossier de base, fiches, sabotage (ou None) ; un sabotage de cible « EPREUVE » ne touche aucun
    fichier : ses textes sont des arguments passés à `--suite` (S-ACC : « --sans-accidents »). ④ CONDITIONS D'ENTRÉE —
    le texte d'un sabotage est présent UNE fois dans son fichier. ⑤ SORTIE — TROIS valeurs : propriétés, refus, écarts
    connus rencontrés. [rend: 3] ⑥ TRAITEMENT — voir ①.
    ⑦ UNITÉ — —. ⑧ POURQUOI — R-731 : un processus neuf par passage, un module saboté ne survit pas au suivant.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit puis efface R. ⑪ TERMINAISON — rend la main ; lève RuntimeError si un texte
    de sabotage n'est pas unique. [sort: non]"""
    nom = "base" if sabotage is None else sabotage[0].split(" ")[0]
    R = os.path.join(base, "R_" + nom)
    try:
        fabriquer_r(racine, R, fiches)
        en_plus = list(sabotage[3]) if sabotage is not None and sabotage[2] == "EPREUVE" else []
        if sabotage is not None and sabotage[2] != "EPREUVE":
            cible = sabotage[2]
            if cible == "MESURER":
                cible = os.path.relpath(next(os.path.join(R, "programmes", x) for x in
                                             sorted(os.listdir(os.path.join(R, "programmes")))
                                             if x.startswith("MESURER_LA_PERFORMANCE")), R)
            chem = os.path.join(R, cible)
            texte = open(chem, encoding="utf-8").read()
            if os.path.islink(chem):
                os.unlink(chem)       # le LIEN seul est retiré (dans R) ; le fichier du dépôt n'est jamais écrit
            for avant, apres in sabotage[3]:
                if texte.count(avant) != 1:
                    raise RuntimeError("%s : texte à saboter présent %d fois" % (sabotage[0], texte.count(avant)))
                texte = texte.replace(avant, apres)
            open(chem, "w", encoding="utf-8").write(texte)
        r = lancer_json(["--suite", R, racine] + en_plus, 1800)
    finally:
        if os.path.isdir(R):
            shutil.rmtree(R, ignore_errors=True)
    if "impossible" in r:
        return {p: ["NON MESURÉE", "suite : IMPOSSIBLE — %s" % r["impossible"]] for p in PROPRIETES_SUITE}, [], []
    return {p: [v[0], "suite : %s" % v[1]] for p, v in r["proprietes"].items()}, r.get("refus", []), \
        r.get("ecarts_connus", [])


# ═══ DE BOUT EN BOUT, EN LIGNE DE COMMANDE (option « --bout-en-bout », A-923, A-945, 20-11-2026 à 20h58) ═════════════
# POURQUOI. Jean-Luc, le 20-11-2026 à 20h58 : « je vois pas la partie Moulinette… vérifie tout à fond ». Jusqu'ici ② ③ ④
# n'étaient joués qu'en mémoire (« --suite-seule ») et la moulinette s'arrêtait à ①. Ce mode fait passer UNE fiche
# factice conforme par les PROGRAMMES DU CIRCUIT EN LIGNE DE COMMANDE, comme la chaîne officielle : ⓪ ① ② ③ ④ par
# programmes/ENCHAINER_LA_MOULINETTE.py, puis les pas du soir de .github/workflows/collecte_abc.yml (versement, signaux,
# positions, mesure, pilote, radar, cockpit), sur un dépôt FABRIQUÉ R de 2024-2025 seulement (A-945 : « 2000-2023 n'est
# jamais lu, même pas les dates »). Un maillon qui ne peut pas tourner sans lire 2000-2023 est NOMMÉ, avec la ligne du
# programme qui le bloque : il n'est ni contourné ni compté vert.
BEB_FICHE = "PROP-BEB"            # la fiche conforme qui traverse tout (QA : le soir ne suit que QA et PRODUCTION)
BEB_REFUSEE = "PROP-BEB-X"        # la même, objectif négatif : le contrat la refuse, au maillon ⓪ PREPARER
BEB_SORTIE = "FABF"               # la valeur qui SORT de l'indice fabriqué (composition) : plus d'achat après sa sortie
BEB_SORTIE_LE = "2025-11-28"      # sa dernière séance dans l'indice fabriqué
BEB_SOIRS = 14                    # les soirs rejoués en ligne de commande : les 14 derniers jours ouvrés de 2025
TEXTE_DE_LA_GARDE = '''"""sitecustomize de l'épreuve par propriétés (A-945) : vit sous un dossier temporaire, jamais au dépôt.
Refuse, dans CHAQUE processus lancé, toute ouverture de fichier ou de dossier sous la racine du dépôt réel, sauf son
dossier programmes/ (le code : un programme lancé par un lien y importe ses voisins, Python résolvant le lien du
script), et la note dans le journal de la garde ; refuse aussi toute écriture sous programmes/ de R (des liens durs
vers le code du dépôt : y écrire changerait le dépôt).
"""
import os
import sys

_R = os.environ.get("GARDE_A945_RACINE")
_J = os.environ.get("GARDE_A945_JOURNAL")
_P = os.environ.get("GARDE_A945_PROGRAMMES_DE_R")
if _R and _J and _P:
    _R = os.path.abspath(_R)
    _C = os.path.join(_R, "programmes")
    _P = os.path.abspath(_P)

    def _garde_a945(evt, args):
        if evt in ("open", "os.listdir", "os.scandir") and args and isinstance(args[0], (str, bytes)):
            c = os.path.abspath(os.fsdecode(args[0]))
            m = args[1] if evt == "open" and len(args) > 1 and isinstance(args[1], str) else ""
            if any(x in m for x in "wax+") and (c == _P or c.startswith(_P + os.sep)):
                with open(_J, "a", encoding="utf-8") as fh:
                    fh.write("%s\\tÉCRITURE %s\\n" % (os.path.basename(sys.argv[0] if sys.argv else "?"), c))
                raise PermissionError("A-945 : écriture dans programmes/ de R refusée (liens durs) : %s" % c)
            if (c == _R or c.startswith(_R + os.sep)) and not (c == _C or c.startswith(_C + os.sep)):
                with open(_J, "a", encoding="utf-8") as fh:
                    fh.write("%s\\t%s\\n" % (os.path.basename(sys.argv[0] if sys.argv else "?"), c))
                raise PermissionError("A-945 : lecture dans le dépôt réel refusée : %s" % c)

    sys.addaudithook(_garde_a945)
'''


def isin_fabrique(k):
    """Rend un code ISIN FABRIQUÉ à clé juste, « FR » suivi de neuf chiffres puis la clé.
    ① RÔLE — des identités de société pour la composition fabriquée. ② CONTEXTE D'APPEL — `fabriquer_le_dessus`.
    ③ ENTRÉE — un entier k ≥ 0 (le rang de la valeur fabriquée). ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur :
    texte de 12 caractères, exemple « FR0000000017 » pour k = 1. [rend: 1] ⑥ TRAITEMENT — la clé de Luhn sur les
    chiffres des lettres en base 36, comme `isin_valide` de programmes/LIRE_LES_COURS.py (la clé est RECALCULÉE ici :
    c'est un fabricant de données, pas un contrôle ; le lecteur, lui, la vérifie). ⑦ UNITÉ — —. ⑧ POURQUOI — le lecteur
    refuse un ISIN à clé fausse. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    corps = "FR%09d" % (99000 + k)
    chiffres = "".join(str(int(c, 36)) for c in corps)
    somme = 0
    for i, c in enumerate(reversed(chiffres)):
        n = int(c) * (2 if i % 2 == 0 else 1)
        somme += n - 9 if n > 9 else n
    return corps + str((10 - somme % 10) % 10)


def fiches_de_bout_en_bout(fiches):
    """Rend les deux fiches du mode « --bout-en-bout », tirées de PROP-Q2 du générateur : la conforme et la refusée.
    ① RÔLE — la fiche qui traverse tout, et celle que le contrat doit arrêter. ② CONTEXTE D'APPEL — `main_bout_en_bout`.
    ③ ENTRÉE — les fiches de `generer` (sur CODES_FAB). ④ CONDITIONS D'ENTRÉE — PROP-Q2 y est. ⑤ SORTIE — UNE valeur :
    liste de deux dictionnaires. [rend: 1] ⑥ TRAITEMENT — PROP-BEB : QA, signal « toujours », horizon 3 séances (une
    position se ferme au plus tard au troisième soir), univers FABB, FABC et la valeur qui sort de l'indice ; période
    2024-03-01 → 2025-12-31 ; PROP-BEB-X : la même, objectif « -4% ». ⑦ UNITÉ — pourcents écrits, séances.
    ⑧ POURQUOI — une fiche QA est suivie par le soir (CONTRATS.ETATS_SUIVIS_PAR_LE_SOIR) ; horizon court : des trades
    clôturés en BEB_SOIRS soirs, donc une mesure. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    q2 = next(f for f in fiches if f["id"] == "PROP-Q2")
    ok = dict(q2, id=BEB_FICHE, nom="factice " + BEB_FICHE, etat_vie="QA", tp="+3.0%", sl="-2.0%", horizon="3",
              univers="FABB,FABC,%s" % BEB_SORTIE, periode="2024-03-01 -> 2025-12-31",
              reglages_signal=json.dumps({"mode": "toujours"}))
    return [ok, dict(ok, id=BEB_REFUSEE, nom="factice " + BEB_REFUSEE, tp="-4%")]


def fabriquer_le_dessus(R, J, dates, jusqu_au, sortie=True):
    """Écrit dans R les données FABRIQUÉES que les programmes en ligne de commande lisent : cours maître, indice,
    calendrier d'Euronext, composition (passages et identités), VOISINAGE.csv lié.
    ① RÔLE — que le circuit tourne sur R sans rien lire du dépôt réel. ② CONTEXTE D'APPEL — `beb` (processus neuf).
    ③ ENTRÉE — R (fabriqué par `fabriquer_r`), le juge chargé depuis R, les séances (jours ouvrés 2024-2025), la dernière
    séance déjà au maître (AAAA-MM-JJ), `sortie` (faux sous le sabotage S-BEB-COMPO : BEB_SORTIE ne sort jamais de
    l'indice). ④ CONDITIONS D'ENTRÉE — le référentiel fabriqué de R. ⑤ SORTIE — UNE valeur :
    {nom au cours maître: série} (les cours fabriqués entiers, soirs compris). [rend: 1] ⑥ TRAITEMENT — ① cours
    `cours_fabriques` (sans accidents : ils sont éprouvés par la suite) écrits au maître jusqu'à `jusqu_au`, source
    « google » (admise jusqu'au 2026-09-08, CONTRATS.SOURCES_ADMISES), sous l'onglet du référentiel · ② l'indice
    INDICE_CAC40 aux mêmes séances · ③ le calendrier d'Euronext couvert de 2026-01-01 à 2027-12-31, sans fermeture ·
    ④ chaque valeur fabriquée dans l'indice depuis la première séance, BEB_SORTIE jusqu'à BEB_SORTIE_LE seulement ·
    ⑤ UNIBAIL_RODAMCO (URW) ajoutée au référentiel, aux valeurs taxées et au maître, prix plats : le calibrage du teneur
    l'exige (voir le commentaire du code).
    ⑦ UNITÉ — euros ; séances. ⑧ POURQUOI — A-945 ; la composition de l'indice n'était éprouvée nulle part.
    ⑨ CE QUI CLOCHE — le teneur dépend d'une VRAIE valeur (Unibail) pour se calibrer : son nom, sa taxe en 2026 ; les
    jours fériés restent des séances ; le calendrier d'Euronext fabriqué ne couvre pas 2024-2025
    (l'indice fabriqué y tient lieu de calendrier, comme pour le passé réel). ⑩ EFFET — écrit sous R.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    import CONTRATS_DES_FICHIERS as CT
    # LA VALEUR DU CALIBRAGE DU TENEUR : `_calibrage` de programmes/TENIR_LES_POSITIONS.py exige qu'UNIBAIL_RODAMCO soit
    # rendue par le chargeur du dépôt (ligne « il rapproche les deux graphies d'UNIBAIL ») et rejoue le cas Unibail du
    # 27-08-2026 sous le barème réel (taxée en 2026). Mesuré le 20-11-2026 : sans elle, « CALIBRAGE ECHOUE » et aucune
    # position n'est tenue. Elle est FABRIQUÉE comme les autres (prix plats à 100 €), et n'est dans aucun univers.
    # LE NOM DU RÉFÉRENTIEL QUE LE TENEUR LIT EN DUR (programmes/TENIR_LES_POSITIONS.py l.3353-3354 : « REFERENTIEL_
    # VALEURS_v3_Lun_17-08-2026_10h54.csv ») : le référentiel fabriqué prend ce nom, il reste le seul (`trouver`).
    ref = os.path.join(R, "donnees", "REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv")
    os.rename(J.trouver(R, "REFERENTIEL_VALEURS"), ref)
    with open(ref, "a", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerow(["URW", "Unibail-Rodamco", "UNIBAIL_RODAMCO", ""])
    with open(os.path.join(R, TTF), "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(CT.VALEURS_TTF), lineterminator="\n")
        for an in ("2024", "2025", "2026"):
            w.writerow(dict(annee=an, mnemonique="URW", nom_usuel="Unibail-Rodamco", assujettie="OUI",
                            liste_reference="factice", source="factice", releve_le="2026-11-20"))
    mnemo = J.table_mnemoniques(J.trouver(R, "REFERENTIEL_VALEURS"))
    onglet = {c: "FABRIQUEE_%s" % c[-1] for c in CODES_FAB}
    tous = list(CODES_FAB) + ["URW"]                     # la composition porte aussi la valeur du calibrage
    onglet["URW"] = "UNIBAIL_RODAMCO"
    cours = cours_fabriques(list(CODES_FAB), mnemo, dates)
    nom_de = {mnemo[c]: onglet[c] for c in CODES_FAB}
    os.makedirs(os.path.join(R, "donnees", "sources_indice"), exist_ok=True)
    with open(os.path.join(R, COURS), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CT.COURS_MAITRE)
        for nom, serie in sorted(cours.items()):
            for b in serie:
                if b["date"] <= jusqu_au:
                    w.writerow([nom_de[nom], b["date"], b["open"], b["high"], b["low"], b["close"], int(b["volume"]),
                                "google"])
        for d in dates:
            if d <= jusqu_au:
                w.writerow(["UNIBAIL_RODAMCO", d, 100.0, 101.0, 99.0, 100.0, 100000, "google"])   # voir ⑤
    with open(os.path.join(R, "donnees", "sources_indice", "INDICE_CAC40.csv"), "w", encoding="utf-8",
              newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CT.INDICE_CAC40)
        for d in dates:
            w.writerow([d, "7500.0", "7500.0"])
    with open(os.path.join(R, "donnees", "NATURE_DES_TROUS.csv"), "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerow(CT.NATURE_DES_TROUS)       # aucune nature décidée
    with open(os.path.join(R, "donnees", "CALENDRIER_EURONEXT.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CT.CALENDRIER)
        w.writerow(["2026-01-01", "COUVERT_DEPUIS", "fabriqué (A-945)", "épreuve par propriétés", ""])
        w.writerow(["2027-12-31", "COUVERT_JUSQU_AU", "fabriqué (A-945)", "épreuve par propriétés", ""])
    with open(os.path.join(R, "donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"), "w", encoding="utf-8",
              newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CT.PASSAGES_DANS_LE_CAC40)
        for k, c in enumerate(tous):
            w.writerow([isin_fabrique(k), onglet[c], dates[0], BEB_SORTIE_LE if c == BEB_SORTIE and sortie else "",
                        "fabriqué", "fabriqué" if c == BEB_SORTIE else ""])
    with open(os.path.join(R, "donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv"), "w", encoding="utf-8",
              newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CT.IDENTITES_DES_SOCIETES)
        for k, c in enumerate(tous):
            w.writerow([str(900 + k), "Fabriquee %s" % c[-1], "", "", onglet[c], c, isin_fabrique(k), "fabriqué",
                        "fabriqué"])
    rendu = {nom_de[nom]: s for nom, s in cours.items()}
    rendu["UNIBAIL_RODAMCO"] = [{"date": d, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0,
                                 "volume": 100000.0} for d in dates]
    return rendu


def lancer_garde(R, journal, racine, *args, delai=400):
    """Lance `python3 -B <args>` dans R SOUS LA GARDE A-945 ; rend (code, texte, lectures refusées).
    ① RÔLE — le seul chemin par lequel ce mode lance un programme du circuit. ② CONTEXTE D'APPEL — `beb`.
    ③ ENTRÉE — R, le journal de la garde, la racine réelle, le programme et ses arguments, un délai en secondes.
    ④ CONDITIONS D'ENTRÉE — `beb` a écrit TEXTE_DE_LA_GARDE en `<R>/../garde_a945/sitecustomize.py`. ⑤ SORTIE — TROIS
    valeurs : le code (124 au-delà du délai), le texte (sortie et erreurs), la liste des chemins refusés pendant CE
    lancement. [rend: 3] ⑥ TRAITEMENT — l'environnement de `env_propre` (comme `lancer` de l'enchaîneur : sans
    GITHUB_* ni DEPOT_*), plus PYTHONPATH vers la garde et ses deux variables ; le journal relu avant et après.
    ⑦ UNITÉ — secondes. ⑧ POURQUOI — A-945 : la garde en mémoire de la suite ne voit pas un sous-processus (⑨ de
    `suite`) ; ici, CHAQUE processus, et chaque processus qu'il lance (l'enchaîneur passe son environnement, sauf
    GITHUB_* et DEPOT_*), porte la garde. ⑨ CE QUI CLOCHE — un programme lancé avec -I, -E ou -S ne charge pas
    sitecustomize : `beb` calibre la garde sur un cas qui doit échouer avant de s'y fier ; os.stat n'est pas un
    événement d'audit (l'existence d'un fichier réel reste visible, pas son contenu). ⑩ EFFET — celui du programme.
    ⑪ TERMINAISON — rend la main dans le délai. [sort: non]"""
    avant = open(journal, encoding="utf-8").read() if os.path.isfile(journal) else ""
    env = env_propre(R, os.path.join(R, "_sortie_du_pas"))
    env.update(PYTHONPATH=os.path.join(os.path.dirname(R), "garde_a945"), GARDE_A945_RACINE=racine,
               GARDE_A945_JOURNAL=journal, GARDE_A945_PROGRAMMES_DE_R=os.path.join(R, "programmes"))
    try:
        p = subprocess.run([sys.executable, "-B"] + list(args), cwd=R, capture_output=True, text=True, timeout=delai,
                           env=env)
        code, texte = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        code, texte = 124, "DÉLAI DÉPASSÉ (%d s) : %s" % (delai, str(e)[-300:])
    apres = open(journal, encoding="utf-8").read() if os.path.isfile(journal) else ""
    return code, texte, [l for l in apres[len(avant):].splitlines() if l.strip()]


def enregistrer_r(R, message):
    """Enregistre l'état de R dans SON dépôt git jetable (créé au premier appel) ; rend le code de git.
    ① RÔLE — donner au soir un « HEAD » comme au circuit (TENIR_L_HISTORIQUE relit la version enregistrée du maître
    pour refuser qu'il rétrécisse). ② CONTEXTE D'APPEL — `beb`, après la moulinette (qui refuse une racine portant
    .git, A-861), puis après chaque soir. ③ ENTRÉE — R, le message. ④ CONDITIONS D'ENTRÉE — git installé. ⑤ SORTIE —
    UNE valeur : le code de la dernière commande git. [rend: 1] ⑥ TRAITEMENT — `git init` si R n'a pas de .git,
    `git add -A`, `git commit` avec l'identité passée en option (« -c », aucune configuration écrite hors de R).
    ⑦ UNITÉ — —. ⑧ POURQUOI — mesuré le 20-11-2026 : sans HEAD, le versement s'arrête (« la version enregistrée de
    donnees/cours_maitre.csv ne se relit pas »). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit R/.git. ⑪ TERMINAISON — chaque
    commande bornée à 120 s. [sort: non]"""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GITHUB_", "DEPOT_", "GIT_"))}
    ident = ["-c", "user.name=epreuve-proprietes", "-c", "user.email=epreuve@invalid", "-c", "commit.gpgsign=false"]
    code = 0
    for cmd in ([["init", "-q"]] if not os.path.isdir(os.path.join(R, ".git")) else []) + [["add", "-A"], [
            "commit", "-q", "--allow-empty", "-m", message]]:
        code = subprocess.run(["git"] + ident + cmd, cwd=R, capture_output=True, text=True, timeout=120,
                              env=env).returncode
    return code


def ajouter_au_maitre(R, CT, cours, d):
    """Ajoute au cours maître de R les séances `d` des cours fabriqués, une fois (rien si la séance y est déjà).
    ① RÔLE — tenir lieu du versement quand TENIR_L_HISTORIQUE ne peut pas tourner (BLOCAGES_CONNUS). ② CONTEXTE
    D'APPEL — `beb`, chaque soir où le versement n'a pas tenu. ③ ENTRÉE — R, le contrat, les cours {nom: série}, la
    séance AAAA-MM-JJ. ④ CONDITIONS D'ENTRÉE — le maître de R existe, en-tête CONTRATS.COURS_MAITRE. ⑤ SORTIE — Aucune.
    [rend: 0] ⑥ TRAITEMENT — lire les couples (valeur, date) déjà écrits ; ajouter les barres de `d` absentes, source
    « google ». ⑦ UNITÉ — euros. ⑧ POURQUOI — sans séance nouvelle, le détecteur et le teneur rejouent la veille (« Sans
    ce pas, le détecteur calcule sur la veille et tout reste vert », instructions du projet § 10). ⑨ CE QUI CLOCHE — ce
    geste n'éprouve rien du versement : le maillon reste NON JOUÉ. ⑩ EFFET — écrit le maître de R. ⑪ TERMINAISON —
    rend la main. [sort: non]"""
    chemin = os.path.join(R, COURS)
    _e, lignes = lire_csv(chemin)
    deja = {(l["valeur"], l["date"]) for l in lignes}
    with open(chemin, "a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        for nom, serie in sorted(cours.items()):
            for b in serie:
                if b["date"] == d and (nom, d) not in deja:
                    w.writerow([nom, d, b["open"], b["high"], b["low"], b["close"], int(b["volume"]), "google"])


def beb(R, racine, sabotage):
    """Le mode « --bout-en-bout » en processus neuf : la fiche PROP-BEB par ⓪ ① ② ③ ④ (enchaîneur), puis BEB_SOIRS soirs
    (versement, détecteur, teneur), puis mesure, pilote, radar, cockpit ; propriétés BEB-*. Affiche un JSON.
    ① RÔLE — la propriété de bout en bout (A-923) et le tableau joué / non joué des maillons, MESURÉ. ② CONTEXTE
    D'APPEL — `__main__` « --beb <R> <racine> [<sabotage>] ». ③ ENTRÉE — R (fabriqué par `fabriquer_r`, avec PROP-BEB et
    PROP-BEB-X), la racine réelle (pour la garde), le sabotage (texte, ou "" : « sans-<maillon> » retire un maillon,
    « perdre-journal » efface les trades de PROP-BEB entre le teneur et la mesure, « perdre-valide » vide PROP-BEB du
    tableau validé entre ⓪ et ①). ④ CONDITIONS D'ENTRÉE — R sans .git. ⑤ SORTIE — Aucune valeur ; un JSON {maillons,
    proprietes, refus} en dernière ligne. [rend: 0] ⑥ TRAITEMENT — ① garde écrite et CALIBRÉE (une lecture du dépôt réel
    doit être refusée, une lecture de R permise) · ② données du dessus · ③ ⓪ ① ② ③ ④ par l'enchaîneur, pour PROP-BEB et
    PROP-BEB-X ; un code non nul garde sa sortie, une lecture refusée par la garde fait le maillon NON JOUÉ, motif
    nommé · ④ chaque soir : une séance ajoutée à donnees/claude_cours_nouveaux.csv, TENIR_L_HISTORIQUE, détecteur, un
    signal posé (forme d'E8) sur chaque valeur de PROP-BEB, teneur ; le dernier soir, un signal aussi sur BEB_SORTIE,
    sortie de l'indice · ⑤ mesure, pilote, radar (audit_ecosysteme), cockpit (PUBLIER_LE_SITE sans phrase ni jeton :
    fabriqué, jamais publié) · ⑥ propriétés. ⑦ UNITÉ — euros ; séances. ⑧ POURQUOI — A-923, A-945, Jean-Luc le
    20-11-2026 à 20h58. ⑨ CE QUI CLOCHE — ① le détecteur ne sert pas une fiche dont le module n'a pas d'étalon
    (DETECTER_LES_SIGNAUX_GITHUB.ETALONS) : le signal du teneur est POSÉ, comme dans `soir` ; ② la collecte (réseau ABC)
    n'est pas jouée : la séance du soir est écrite par l'épreuve ; ③ le gain affiché est cherché TEL QUE LE JOURNAL
    L'ÉCRIT (deux décimales) dans la page du cockpit et dans la sortie de la mesure. ⑩ EFFET — écrit sous R.
    ⑪ TERMINAISON — chaque lancement borné (400 s, 900 s pour la moulinette). [sort: non]"""
    sys.path.insert(0, os.path.join(R, "programmes"))
    import CONTRATS_DES_FICHIERS as CT
    import JUGE_DES_STRATEGIES as J
    racine = os.path.abspath(racine)
    base = os.path.dirname(R)
    os.makedirs(os.path.join(base, "garde_a945"), exist_ok=True)
    open(os.path.join(base, "garde_a945", "sitecustomize.py"), "w", encoding="utf-8").write(
        "" if sabotage == "sans-garde" else TEXTE_DE_LA_GARDE)
    journal = os.path.join(base, "garde_a945", "journal.txt")
    open(journal, "w").close()
    maillons, refus, prop = [], [], {p: [] for p in PROPRIETES_BEB}
    n = {p: 0 for p in PROPRIETES_BEB}
    sorties = {}

    def noter(nom, code, texte, lus, attendu=(0,)):
        """Range un maillon : JOUÉ (code attendu, rien refusé), NON JOUÉ (garde, motif nommé) ou EN ÉCHEC (autre code).
        ① RÔLE — la colonne « joué » du tableau, mesurée. ② CONTEXTE D'APPEL — `beb`, après chaque lancement.
        ③ ENTRÉE — le nom du maillon, le code, le texte, les lectures refusées, les codes attendus. ④ CONDITIONS
        D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : l'état (« JOUÉ », « NON JOUÉ », « EN ÉCHEC »). [rend: 1]
        ⑥ TRAITEMENT — une lecture refusée l'emporte (le maillon lit le dépôt réel : NON JOUÉ, et BEB-A945 rougit) ;
        puis un BLOCAGE CONNU (texte exact de BLOCAGES_CONNUS dans la sortie, code inattendu : NON JOUÉ, motif nommé) ;
        puis le code.
        ⑦ UNITÉ — —. ⑧ POURQUOI — jamais vert un maillon qui n'a pas tourné (R-734). ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — ajoute à `maillons` et `sorties`. ⑪ TERMINAISON — rend la main. [sort: non]"""
        bloc = [b[2] for b in BLOCAGES_CONNUS if nom.startswith(b[0]) and b[1] in texte]
        if lus:
            etat, motif = "NON JOUÉ", "lit le dépôt réel (refusé par la garde A-945) : %s" % sorted(set(
                os.path.relpath(x.split("\t", 1)[-1], racine) for x in lus))[:3]
            prop["BEB-A945"].append("%s : %s" % (nom, motif))
        elif bloc and code not in attendu:
            etat, motif = "NON JOUÉ", bloc[0]
        elif code in attendu:
            etat, motif = "JOUÉ", "code %d" % code
        else:
            etat, motif = "EN ÉCHEC", "code %d : %s" % (code, " | ".join(texte.strip().splitlines()[-3:])[:300])
        n["BEB-A945"] += 1
        maillons.append([nom, etat, motif])
        sorties[nom] = texte
        return etat

    # ① LA GARDE, CALIBRÉE SUR UN CAS QUI DOIT ÉCHOUER ET UN CAS QUI DOIT PASSER (instructions § 4 : un motif se calibre)
    sonde = "import sys\ntry:\n    open(sys.argv[1]).close()\n    print('LU')\nexcept PermissionError:\n    print('REFUSÉ')\n"
    _c, t1, _l = lancer_garde(R, journal, racine, "-c", sonde, os.path.join(racine, COURS))
    _c, t2, _l = lancer_garde(R, journal, racine, "-c", sonde, os.path.join(R, REG))
    open(journal, "w").close()
    n["BEB-GARDE"] += 2
    if "REFUSÉ" not in t1 or "LU" not in t2:
        prop["BEB-GARDE"].append("garde non calibrée : dépôt réel « %s », R « %s »" % (t1.strip()[-80:], t2.strip()[-80:]))
        print(json.dumps({"maillons": maillons, "refus": refus, "proprietes": {
            p: ["ROUGE" if prop[p] else "NON MESURÉE", " ; ".join(prop[p]) or "garde non calibrée"]
            for p in PROPRIETES_BEB}}, ensure_ascii=False))
        return
    # ② LES DONNÉES DU DESSUS
    dates = jours_ouvres(SUITE_DEBUT, SUITE_FIN)
    soirs = dates[-BEB_SOIRS:]
    cours = fabriquer_le_dessus(R, J, dates, dates[-BEB_SOIRS - 1], sortie=sabotage != "sans-composition")
    os.makedirs(os.path.join(R, "donnees", "combinatoires"), exist_ok=True)
    fiches = CT.fiches_du_registre(os.path.join(R, REG))
    # ③ LA MOULINETTE PAR L'ENCHAÎNEUR, COMME LA CHAÎNE OFFICIELLE (fiche conforme, puis fiche refusée)
    quand = __import__("datetime").datetime.now(__import__("zoneinfo").ZoneInfo("Europe/Paris"))
    etapes = (("⓪ PREPARER", ["preparer"]), ("① DECLINER", ["decliner"]), ("② JOUER_LES_VERSIONS", ["jouer", "0", "1"]),
              ("② assembler", ["assembler"]), ("③ TRIER_LES_VARIANTES", ["trier"]))
    for ident in (BEB_FICHE, BEB_REFUSEE):
        lignes = tableau_valide(dict(fiches[ident], tp="+3.0%"), J, quand)    # le tableau de la conforme pour les deux
        for l in lignes:
            l["strategie"] = ident
        with open(os.path.join(R, "donnees", "combinatoires", "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (ident, ESSAI)),
                  "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(lignes[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(lignes)
        bloque = None
        for nom, args in etapes:
            sous = nom if ident == BEB_FICHE else "%s · %s" % (nom, ident)
            if bloque:
                maillons.append([sous, "NON JOUÉ", "la chaîne ne se saute pas (A-919) : %s n'a pas tenu" % bloque])
                continue
            if sabotage == "sans-" + nom.split(" ")[1] and ident == BEB_FICHE:
                maillons.append([sous, "NON JOUÉ", "SABOTAGE : maillon retiré"])
                bloque = nom
                continue
            code, texte, lus = lancer_garde(R, journal, racine, os.path.join(R, ENCH), R, ident, ESSAI, *args,
                                            delai=900)
            etat = noter(sous, code, texte, lus)
            if sabotage == "perdre-valide" and ident == BEB_FICHE and nom == "⓪ PREPARER":
                ch = os.path.join(R, "CHAINE_%s_%s" % (ident, ESSAI), "valide")
                for x in os.listdir(ch):
                    open(os.path.join(ch, x), "w").write(open(os.path.join(ch, x)).read().split("\n", 1)[0] + "\n")
            if etat != "JOUÉ":
                bloque = nom
                if ident == BEB_REFUSEE:
                    refus.append({"maillon": nom, "fiche": ident, "motif": " | ".join(
                        l.strip() for l in texte.splitlines() if "contrat" in l or "REFUS" in l or "tp" in l)[:300]})
        if ident == BEB_FICHE:
            if bloque:
                maillons.append(["④ juge (ENCHAINER juger)", "NON JOUÉ",
                                 "la chaîne ne se saute pas (A-919) : %s n'a pas tenu" % bloque])
            else:
                t = CT.fiches_du_registre(os.path.join(R, REG))
                tri = os.path.join(R, "CHAINE_%s_%s" % (ident, ESSAI), "e3", "TRI_%s_%s.csv" % (ident, ESSAI))
                _e, retenues = lire_csv(tri) if os.path.isfile(tri) else ([], [])
                if not retenues:
                    maillons.append(["④ juge (ENCHAINER juger)", "NON JOUÉ", "aucune version retenue par le tri"])
                else:
                    code, texte, lus = lancer_garde(R, journal, racine, os.path.join(R, ENCH), R, ident, ESSAI,
                                                    "juger", retenues[0]["id_version"], delai=900)
                    noter("④ juge (ENCHAINER juger)", code, texte, lus)
                del t
    # ④ LE SOIR, BEB_SOIRS FOIS, EN LIGNE DE COMMANDE — dans un dépôt git jetable, comme au circuit
    if enregistrer_r(R, "avant le premier soir"):
        maillons.append(["git de R", "EN ÉCHEC", "git init / commit a échoué : le versement ne pourra pas relire HEAD"])
    mnemo_onglet = {"FABRIQUEE_%s" % c[-1]: c for c in CODES_FAB}
    univers = [x.strip() for x in fiches[BEB_FICHE]["univers"].split(",")]
    etats_soir = {}
    for k, d in enumerate(soirs):
        with open(os.path.join(R, "donnees", "claude_cours_nouveaux.csv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(CT.COURS_NOUVEAUX)
            for nom, serie in sorted(cours.items()):
                for b in serie:
                    if b["date"] == d:
                        w.writerow([nom, d, b["open"], b["high"], b["low"], b["close"], int(b["volume"])])
        pas = [("versement TENIR_L_HISTORIQUE", ["programmes/TENIR_L_HISTORIQUE.py", R], (0,)),
               ("valeurs CONTROLER_LES_VALEURS", ["programmes/CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py", R], (0,)),
               ("signaux DETECTER_LES_SIGNAUX_GITHUB", [DET, R], (0, 1)),
               ("positions TENIR_LES_POSITIONS", [TENIR, R], (0,))]
        for nom, args, attendu in pas:
            if sabotage == "sans-" + nom.split(" ")[0]:
                etats_soir.setdefault(nom, []).append(("NON JOUÉ", "SABOTAGE : maillon retiré", ""))
                if nom.startswith("versement"):
                    ajouter_au_maitre(R, CT, cours, d)
                continue
            if nom.startswith("positions"):
                posés = [{"valeur": "FABRIQUEE_%s" % c[-1], "date_signal": d, "cmf": 0.01, "cci": -80.0 + j,
                          "close": next(b["close"] for b in cours["FABRIQUEE_%s" % c[-1]] if b["date"] == d)}
                         for j, c in enumerate(univers) if c != BEB_SORTIE or d > BEB_SORTIE_LE]
                json.dump({"seance": d, "signaux": posés}, open(os.path.join(R, SIG), "w", encoding="utf-8"))
            code, texte, lus = lancer_garde(R, journal, racine, *args)
            n["BEB-A945"] += 1
            bloc = [b[2] for b in BLOCAGES_CONNUS if nom.startswith(b[0]) and b[1] in texte]
            if nom.startswith("versement") and (lus or code not in attendu):
                ajouter_au_maitre(R, CT, cours, d)       # la séance entre au maître par l'épreuve (versement non joué)
            if lus:
                e = ("NON JOUÉ", "lit le dépôt réel (garde A-945) : %s" % sorted(set(
                    os.path.relpath(x.split("\t", 1)[-1], racine) for x in lus))[:3], texte)
                prop["BEB-A945"].append("%s, soir %s : %s" % (nom, d, e[1]))
            elif bloc and code not in attendu:
                e = ("NON JOUÉ", bloc[0], texte)
            elif code in attendu:
                e = ("JOUÉ", "code %d" % code, texte)
            else:
                e = ("EN ÉCHEC", "soir %s, code %d : %s" % (d, code, " | ".join(texte.strip().splitlines()[-3:])[:300]),
                     texte)
            etats_soir.setdefault(nom, []).append(e)
        enregistrer_r(R, "soir %s" % d)
    # LE JOURNAL TEL QUE LE TENEUR L'A ÉCRIT : la référence des propriétés, relevée AVANT tout sabotage d'aval
    jt = os.path.join(R, "donnees", "claude_journal_trades.csv")
    _e, trades = lire_csv(jt) if os.path.isfile(jt) else ([], [])
    for sab, chemin in (("perdre-journal", jt), ("perdre-registre", os.path.join(R, REG))):
        if sabotage == sab and os.path.isfile(chemin):       # la fiche perdue entre le teneur et la suite du soir
            lignes_s = open(chemin, encoding="utf-8").read().split("\n")
            open(chemin, "w", encoding="utf-8").write("\n".join(l for l in lignes_s if not l.startswith(
                BEB_FICHE + ",") and ("," + BEB_FICHE + ",") not in l))
    for nom, liste in etats_soir.items():
        pire = next((e for e in liste if e[0] == "NON JOUÉ"), None) or next((e for e in liste if e[0] == "EN ÉCHEC"),
                                                                          None) or liste[-1]
        maillons.append([nom, pire[0], "%s (%d soir(s))" % (pire[1], len(liste))])
        sorties[nom] = "\n".join(e[2] for e in liste)
    # ⑤ MESURE, PILOTE, RADAR, COCKPIT
    # DANS L'ORDRE DU CIRCUIT (.github/workflows/collecte_abc.yml : cockpit l.306, mesure l.330, pilote l.338, radar
    # l.366) ; le cockpit sans phrase ni jeton : fabriqué dans _site_travail/, puis « CODE 1 — PHRASE absente », jamais
    # publié (PUBLIER_LE_SITE.py) — le code 1 est donc l'attendu.
    fin = [("cockpit PUBLIER_LE_SITE", ["programmes/PUBLIER_LE_SITE.py", R], (1,)),
           ("mesure MESURER_LA_PERFORMANCE", [next(os.path.join("programmes", x) for x in sorted(os.listdir(
               os.path.join(R, "programmes"))) if x.startswith("MESURER_LA_PERFORMANCE")), R, R], (0,)),
           ("pilote claude_FABRIQUER_LE_PILOTE", ["programmes/claude_FABRIQUER_LE_PILOTE.py", R,
                                                  os.path.join(R, "gouvernance", "PILOTE.md")], (0,)),
           ("radar audit_ecosysteme", ["programmes/audit_ecosysteme.py", R], (0, 1))]
    for nom, args, attendu in fin:
        if sabotage == "sans-" + nom.split(" ")[0]:
            maillons.append([nom, "NON JOUÉ", "SABOTAGE : maillon retiré"])
            continue
        code, texte, lus = lancer_garde(R, journal, racine, *args)
        noter(nom, code, texte, lus, attendu)
    # ⑥ LES PROPRIÉTÉS
    etat_de = {m[0]: m[1] for m in maillons}
    miens = [t for t in trades if t.get("strategie") == BEB_FICHE and t.get("comptabilite") == CT.UN_JETON]
    gain = sum(float(t["pnl_net_eur"]) for t in miens) if miens else None
    # BEB-PASSE : la fiche apparaît dans la sortie de chaque maillon JOUÉ (nommée), et dans les fichiers qu'il écrit
    fichiers_du_maillon = {
        "⓪ PREPARER": os.path.join(R, "CHAINE_%s_%s" % (BEB_FICHE, ESSAI), "e0"),
        "① DECLINER": os.path.join(R, "CHAINE_%s_%s" % (BEB_FICHE, ESSAI), "e1"),
        "pilote claude_FABRIQUER_LE_PILOTE": os.path.join(R, "gouvernance", "PILOTE.md"),
        "radar audit_ecosysteme": None,
        "cockpit PUBLIER_LE_SITE": os.path.join(R, "_site_travail"),
        "mesure MESURER_LA_PERFORMANCE": os.path.join(R, "donnees", "historique_mesures.csv"),
        "positions TENIR_LES_POSITIONS": os.path.join(R, POS),
    }

    def texte_de(chemin):
        """Rend le texte d'un fichier, ou de tous les fichiers d'un dossier, "" s'il n'existe pas.
        ① RÔLE — chercher la fiche dans ce qu'un maillon a écrit. ② CONTEXTE D'APPEL — `beb`. ③ ENTRÉE — un chemin ou
        None. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : texte. [rend: 1] ⑥ TRAITEMENT — lire, sans erreur
        d'encodage. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main.
        [sort: non]"""
        if not chemin:
            return ""
        if os.path.isdir(chemin):
            return "\n".join(texte_de(os.path.join(chemin, x)) for x in sorted(os.listdir(chemin)))
        return open(chemin, encoding="utf-8", errors="replace").read() if os.path.isfile(chemin) else ""
    for nom, etat, motif in maillons:
        if " · " in nom or etat == "NON JOUÉ" and not motif.startswith("SABOTAGE"):
            continue
        n["BEB-PASSE"] += 1
        if etat != "JOUÉ":
            prop["BEB-PASSE"].append("%s : %s — %s" % (nom, etat, motif[:200]))
            continue
        if not (nommee(sorties.get(nom, ""), BEB_FICHE) or nommee(texte_de(fichiers_du_maillon.get(nom)), BEB_FICHE)):
            prop["BEB-PASSE"].append("%s : %s absente de sa sortie et de ce qu'il écrit" % (nom, BEB_FICHE))
    # BEB-REFUS : la fiche refusée l'est au maillon ⓪ PREPARER, motif nommé (la case tp), et nulle part plus loin
    n["BEB-REFUS"] += 1
    e0x = etat_de.get("⓪ PREPARER · %s" % BEB_REFUSEE)
    if e0x != "EN ÉCHEC" or not any(r["maillon"] == "⓪ PREPARER" and "tp" in r["motif"] for r in refus):
        prop["BEB-REFUS"].append("%s : ⓪ %s, refus %s" % (BEB_REFUSEE, e0x, [r for r in refus][:2]))
    if any(etat_de.get(x) == "JOUÉ" for x in etat_de if x.endswith(BEB_REFUSEE) and not x.startswith("⓪")):
        prop["BEB-REFUS"].append("%s passe un maillon après son refus" % BEB_REFUSEE)
    # BEB-SILENCE : entre deux maillons JOUÉS consécutifs, la fiche ne disparaît pas sans refus nommé
    joues = [m[0] for m in maillons if m[1] == "JOUÉ" and " · " not in m[0]]
    for a, b in zip(joues, joues[1:]):
        n["BEB-SILENCE"] += 1
        if nommee(sorties.get(a, "") + texte_de(fichiers_du_maillon.get(a)), BEB_FICHE) and not (
                nommee(sorties.get(b, "") + texte_de(fichiers_du_maillon.get(b)), BEB_FICHE)):
            prop["BEB-SILENCE"].append("%s → %s : %s disparaît sans refus nommé" % (a, b, BEB_FICHE))
    # BEB-GAIN : des trades « un jeton » clôturés par le teneur ; la mesure, si elle a tourné, porte leur somme ; le
    # cockpit affiche CHAQUE trade sur une ligne qui nomme la fiche, avec le gain écrit au journal (chiffres comparés
    # après retrait des espaces et virgule lue comme point : « -2 697,00 € » ↔ « -2697.00 » ; rien n'est recalculé).
    n["BEB-GAIN"] += 1
    if gain is None:
        prop["BEB-GAIN"].append("aucun trade un jeton clôturé de %s en %d soirs" % (BEB_FICHE, len(soirs)))
    else:
        if etat_de.get("mesure MESURER_LA_PERFORMANCE") == "JOUÉ":
            mes = texte_de(fichiers_du_maillon["mesure MESURER_LA_PERFORMANCE"])
            if not any(nommee(l, BEB_FICHE) and "%.2f" % gain in l for l in mes.splitlines()):
                prop["BEB-GAIN"].append("mesure : somme %.2f € de %s introuvable" % (gain, BEB_FICHE))
        page = texte_de(fichiers_du_maillon["cockpit PUBLIER_LE_SITE"])
        rangs = []
        for bout in page.split("<tr")[1:]:
            t = __import__("re").sub(r"<[^>]*>", "|", bout)
            rangs.append("".join(t.split()).replace("\u202f", "").replace("\u00a0", "").replace(",", "."))
        for tr in miens:
            voulu = "%s·unjeton" % BEB_FICHE
            if not any(voulu in r and tr["pnl_net_eur"] in r and tr["date_sortie"] in r for r in rangs):
                prop["BEB-GAIN"].append("cockpit : le trade %s %s du %s (%s €) n'a pas de ligne « %s » avec ce gain" % (
                    BEB_FICHE, tr["valeur"], tr["date_sortie"], tr["pnl_net_eur"], voulu))
    # LE DÉTECTEUR ET LA FICHE CONFORME : ce qu'il en dit (mise à part, faute d'étalon pour son module) est un REFUS d'une
    # fiche conforme, rapporté tel quel (A-923 : la liste des maillons où une stratégie conforme est refusée)
    dit = sorted({l.strip() for l in sorties.get("signaux DETECTER_LES_SIGNAUX_GITHUB", "").splitlines()
                  if nommee(l, BEB_FICHE)})
    if dit:
        refus.append({"maillon": "signaux DETECTER_LES_SIGNAUX_GITHUB", "fiche": BEB_FICHE, "motif": " | ".join(dit)[:300]})
    # BEB-COMPO : aucun ACHAT (date d'entrée écrite) de BEB_SORTIE après sa sortie de l'indice, ET le teneur a dit au
    # moins une fois « ACHAT REFUSE » pour elle : sans ce refus nommé, la composition n'aurait pas été éprouvée.
    n["BEB-COMPO"] += 1
    _e, pos = lire_csv(os.path.join(R, POS)) if os.path.isfile(os.path.join(R, POS)) else ([], [])
    onglet_sortie = "FABRIQUEE_%s" % BEB_SORTIE[-1]
    apres = [x for x in pos + trades if x.get("strategie") == BEB_FICHE and
             mnemo_onglet.get((x.get("valeur") or "").strip().upper()) == BEB_SORTIE and
             (x.get("date_entree") or "").strip() > BEB_SORTIE_LE]
    if apres:
        prop["BEB-COMPO"].append("%d position(s) ou trade(s) sur %s achetés après sa sortie de l'indice (%s)" % (
            len(apres), BEB_SORTIE, BEB_SORTIE_LE))
    refus_compo = [l.strip() for l in sorties.get("positions TENIR_LES_POSITIONS", "").splitlines()
                   if "ACHAT REFUSE %s %s" % (BEB_FICHE, onglet_sortie) in l]
    if not refus_compo:
        prop["BEB-COMPO"].append("aucun « ACHAT REFUSE %s %s » du teneur : la composition n'a pas été éprouvée" % (
            BEB_FICHE, onglet_sortie))
    else:
        refus.append({"maillon": "positions TENIR_LES_POSITIONS (composition)", "fiche": BEB_FICHE,
                      "motif": "%d refus, dont : %s" % (len(refus_compo), refus_compo[0][:240])})
    etats = {p: ["ROUGE" if prop[p] else ("VERT" if n[p] else "NON MESURÉE"),
                 "%d mesure(s) ; %s" % (n[p], " ; ".join(prop[p][:4]) or "aucun défaut")] for p in PROPRIETES_BEB}
    etats["BEB-GAIN"][1] += " · %d trade(s) de %s, gain un jeton %s €" % (len(miens), BEB_FICHE,
                                                                          "—" if gain is None else "%.2f" % gain)
    print(json.dumps({"maillons": maillons, "proprietes": etats, "refus": refus}, ensure_ascii=False))


# LES BLOCAGES CONNUS — un maillon dont la sortie porte EXACTEMENT ce texte n'a pas tourné parce que son programme lit
# en dur des données d'avant 2024 : il est NON JOUÉ, motif nommé avec le fichier et la ligne, jamais compté vert ni
# rouge (consigne du 20-11-2026 : « ne le contourne pas et ne modifie pas le programme du circuit »). Le texte est
# celui que le programme affiche (relevé le 20-11-2026 sur le dépôt fabriqué) : s'il change, le maillon redevient EN
# ÉCHEC, donc rouge — il ne se tait pas.
BLOCAGES_CONNUS = (
    ("② JOUER_LES_VERSIONS", "le juge des stratégies ne se calibre pas, ou n'a pas joué la fiche",
     "lit 2000-2023 en dur : programmes/JOUER_LES_VERSIONS.py l.762-763 exige du juge la phrase « calibrage sur le "
     "TEMOIN du golden », que programmes/JUGE_DES_STRATEGIES.py (l.5623-5641) n'écrit qu'avec gouvernance/golden_tests_"
     "*.json et temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv (cours depuis 2000) ; le dépôt fabriqué n'en "
     "porte pas"),
    ("mesure MESURER_LA_PERFORMANCE", "aucune operation Bureau Veritas dans le journal : reference introuvable",
     "lit le journal RÉEL en dur : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py l.2001-2003 exige au "
     "journal le trade Bureau Veritas du 27-07-2026 (attendus l.2005-2007 : 6 884,75 €, 3 694,00 €, 27,28 €) ; ce "
     "n'est pas d'avant 2024, mais le dépôt fabriqué n'en porte pas, et l'écrire serait contourner le calibrage"),
    ("versement TENIR_L_HISTORIQUE", "l'historique Google de référence donnees/cac40_ohlcv.csv est absent ou vide",
     "lit 2000-2023 en dur : programmes/TENIR_L_HISTORIQUE.py l.183 (donnees/cac40_ohlcv.csv) et l.1131-1137 (arrêt "
     "s'il est absent) — la référence Google depuis 2000 ; la séance du soir est donc écrite au maître PAR L'ÉPREUVE"),
)
PROPRIETES_BEB = ("BEB-GARDE", "BEB-A945", "BEB-PASSE", "BEB-REFUS", "BEB-SILENCE", "BEB-GAIN", "BEB-COMPO")
ENONCES.update({
    "BEB-GARDE": "la garde A-945 de chaque processus est calibrée (une lecture du dépôt réel refusée, une de R permise)",
    "BEB-A945": "aucun programme du circuit ne lit le dépôt réel (aucune ouverture refusée par la garde)",
    "BEB-PASSE": "la fiche conforme passe CHAQUE maillon joué en ligne de commande et y est nommée ; un maillon "
                 "non joué ou en échec rougit",
    "BEB-REFUS": "la fiche non conforme est refusée au maillon ⓪ PREPARER, case nommée, et ne passe rien après",
    "BEB-SILENCE": "aucune fiche conforme ne disparaît en silence entre deux maillons joués",
    "BEB-GAIN": "le teneur clôture des trades « un jeton » de la fiche ; le cockpit affiche chacun avec le gain écrit "
                "au journal ; la mesure, si elle a tourné, porte leur somme",
    "BEB-COMPO": "aucune position n'entre sur une valeur après sa sortie de l'indice fabriqué (composition)",
})
# LES SABOTAGES DE BOUT EN BOUT : (nom, propriété qui DOIT rougir, geste) — chaque geste est fait par CETTE épreuve
# (`passage_bout_en_bout` ou `beb`), jamais dans un programme du circuit : retirer un maillon, perdre la fiche entre deux
# maillons, éteindre la garde, revenir aux liens symboliques (la fuite mesurée le 20-11-2026), rendre conforme la fiche
# qui doit être refusée, ne jamais faire sortir BEB_SORTIE de l'indice.
SABOTAGES_BEB = (
    ("S-BEB1 maillon ⓪ retiré", "BEB-PASSE", "sans-PREPARER"),
    ("S-BEB2 teneur retiré", "BEB-PASSE", "sans-positions"),
    ("S-BEB3 fiche perdue entre le teneur et la mesure (journal)", "BEB-GAIN", "perdre-journal"),
    ("S-BEB4 fiche perdue entre ⓪ et ① (tableau validé vidé)", "BEB-PASSE", "perdre-valide"),
    ("S-BEB5 cockpit retiré", "BEB-PASSE", "sans-cockpit"),
    ("S-BEB6 fiche perdue entre le teneur et le pilote (registre)", "BEB-SILENCE", "perdre-registre"),
    ("S-BEB7 garde éteinte", "BEB-GARDE", "sans-garde"),
    ("S-BEB8 programmes en liens symboliques", "BEB-A945", "liens-symboliques"),
    ("S-BEB9 fiche fautive rendue conforme", "BEB-REFUS", "refusee-conforme"),
    ("S-BEB10 la valeur ne sort jamais de l'indice", "BEB-COMPO", "sans-composition"),
)


def passage_bout_en_bout(racine, base, fiches, sabotage):
    """Un passage du mode « --bout-en-bout » : fabriquer R (avec les deux fiches de bout en bout), lancer « --beb » en
    processus neuf, effacer R ; rend (maillons, propriétés, refus).
    ① RÔLE — comme `passage_suite`. ② CONTEXTE D'APPEL — `main_bout_en_bout`. ③ ENTRÉE — racine, dossier de base, les
    fiches (dont PROP-BEB et PROP-BEB-X), le sabotage (troisième champ de SABOTAGES_BEB) ou "". ④ CONDITIONS D'ENTRÉE —
    celles de `fabriquer_r`. ⑤ SORTIE — TROIS valeurs. [rend: 3] ⑥ TRAITEMENT — `fabriquer_r`, VOISINAGE.csv lié
    (réglage de ⓪), `lancer_json`. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731 : un processus neuf par passage. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — écrit puis efface R et la garde. ⑪ TERMINAISON — rend la main. [sort: non]"""
    R = os.path.join(base, "R_beb_" + (sabotage or "base"))
    try:
        if sabotage == "refusee-conforme":
            fiches = [dict(f, tp="+4%") if f["id"] == BEB_REFUSEE else f for f in fiches]
        fabriquer_r(racine, R, fiches, durs=sabotage != "liens-symboliques")
        rel = "donnees/combinatoires/VOISINAGE.csv"
        os.symlink(os.path.join(racine, rel), os.path.join(R, rel))
        for x in ("rapports", "gouvernance"):
            os.makedirs(os.path.join(R, x), exist_ok=True)
        r = lancer_json(["--beb", R, racine] + ([sabotage] if sabotage else []), 3600)
    finally:
        shutil.rmtree(R, ignore_errors=True)
        shutil.rmtree(os.path.join(base, "garde_a945"), ignore_errors=True)
    if "impossible" in r:
        return [], {p: ["NON MESURÉE", "IMPOSSIBLE — %s" % r["impossible"]] for p in PROPRIETES_BEB}, []
    return r["maillons"], r["proprietes"], r["refus"]


def main_bout_en_bout(racine, base, saboter, t0):
    """Le déroulé du mode « --bout-en-bout » : passage sans sabotage, tableau des maillons, propriétés, sabotages.
    ① RÔLE — ⑥ de `beb`, rassemblé. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — racine, dossier de base, drapeau des
    sabotages, instant du départ. ④ CONDITIONS D'ENTRÉE — celles de `fabriquer_r`. ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
    [rend: 1] ⑥ TRAITEMENT — fiches comme `main_suite` plus les deux de `fiches_de_bout_en_bout`. ⑦ UNITÉ — —.
    ⑧ POURQUOI — R-731, R-734 : un maillon NON JOUÉ ou EN ÉCHEC rend le code 1, jamais 0. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — écrit sous `base`. ⑪ TERMINAISON — rend la main. [sort: non]"""
    try:
        with open(os.path.join(racine, REG), encoding="utf-8-sig") as fh:
            entete = next(csv.reader([fh.readline()]))
        fiches = generer(dict.fromkeys(entete, ""), list(CODES_FAB), jours_ouvres(SUITE_DEBUT, SUITE_FIN)[-1])
        fiches = [f for f in fiches if f["id"] in ("PROP-Q2",)] + fiches_de_bout_en_bout(fiches)
        print("ÉPREUVE DE BOUT EN BOUT (A-923, A-945) — %s et %s · dépôt FABRIQUÉ %s → %s · %d soirs en ligne de "
              "commande · rien d'avant 2024, garde A-945 dans chaque processus" % (BEB_FICHE, BEB_REFUSEE, SUITE_DEBUT,
                                                                                 SUITE_FIN, BEB_SOIRS))
        maillons, final, refus = passage_bout_en_bout(racine, base, fiches, "")
        rouge = False
        print("\n— MAILLONS (mesurés) —")
        for nom, etat, motif in maillons:
            print("  %-42s %-9s %s" % (nom, etat, motif[:400]))
        print("\n— TABLEAU PROPRIÉTÉ × VERDICT (sans sabotage) —")
        for p in PROPRIETES_BEB:
            e, det = final[p]
            print("  %-11s %-12s %s\n         %s" % (p, e, ENONCES[p], det[:900]))
            rouge = rouge or e != "VERT"
        print("\n— REFUS —")
        for r in refus:
            print("  %s · %s · %s" % (r["maillon"], r["fiche"], r["motif"][:300]))
        if saboter:
            print("\n— SABOTAGES DE BOUT EN BOUT (chacun doit faire rougir SA propriété) —")
            for sab in SABOTAGES_BEB:
                _m, f2, _r = passage_bout_en_bout(racine, base, fiches, sab[2])
                mord = f2[sab[1]][0] == "ROUGE"
                print("  %s %s → %s ; %s : %s" % ("✅" if mord else "❌", sab[0], "MORD" if mord else "SURVIT (%s)" %
                                                 f2[sab[1]][0], sab[1], f2[sab[1]][1][:400]))
                rouge = rouge or not mord
        non_joues = [m for m in maillons if m[1] == "NON JOUÉ"]
        print("\nDURÉE : %.0f s" % (time.time() - t0))
        print("MAILLONS NON JOUÉS : %d — nommés ci-dessus avec leur motif ; ni verts ni rouges, jamais comptés verts"
              % len(non_joues))
        print("VERDICT : %s" % ("TOUT TIENT SUR LES MAILLONS JOUÉS" if not rouge else "NON CONFORME"))
        return 1 if rouge else 0
    except (OSError, LookupError, AssertionError, RuntimeError, ValueError) as e:
        print("ÉPREUVE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2


# ═══ LES COPIES ET LE DÉROULÉ ═════════════════════════════════════════════════════════════════════════════════════════

def fabriquer_w(racine, W, fiches, victime):
    """Fabrique la copie W : programmes/, fichiers .py de la racine, fichiers du premier niveau de donnees/,
    donnees/combinatoires/ et donnees/sources_indice/ ; le module factice ; les fiches au registre ; la victime de P1
    retirée de VALEURS_TTF pour 2025.
    ① RÔLE — la copie de la couche et de la chaîne. ② CONTEXTE D'APPEL — `passage`. ③ ENTRÉE — racine, W, fiches,
    victime. ④ CONDITIONS D'ENTRÉE — W n'existe pas. ⑤ SORTIE — Aucune. [rend: 0] ⑥ TRAITEMENT — copier, écrire.
    ⑦ UNITÉ — —. ⑧ POURQUOI — jamais d'épreuve sur le dépôt. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit sous W.
    ⑪ TERMINAISON — lève AssertionError si la ligne de la victime n'est pas unique. [sort: non]"""
    shutil.copytree(os.path.join(racine, "programmes"), os.path.join(W, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    for n in os.listdir(racine):
        if n.endswith(".py") and os.path.isfile(os.path.join(racine, n)):
            shutil.copy2(os.path.join(racine, n), os.path.join(W, n))
    os.makedirs(os.path.join(W, "donnees"))
    for n in os.listdir(os.path.join(racine, "donnees")):
        p = os.path.join(racine, "donnees", n)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(W, "donnees", n))
    for d in ("combinatoires", "sources_indice"):
        if os.path.isdir(os.path.join(racine, "donnees", d)):
            shutil.copytree(os.path.join(racine, "donnees", d), os.path.join(W, "donnees", d))
    ajouter_au_registre(W, fiches)
    lignes = open(os.path.join(W, TTF), encoding="utf-8").read().split("\n")
    vic = [l for l in lignes if l.startswith("2025,%s," % victime)]
    assert len(vic) == 1, "ligne 2025 de %s dans VALEURS_TTF : %d" % (victime, len(vic))
    open(os.path.join(W, TTF), "w", encoding="utf-8").write("\n".join(l for l in lignes if l not in vic))


def fabriquer_s(racine, S, fiches_qa):
    """Fabrique la copie S : le dépôt entier sans .git, etudes, archives ; le module factice ; les fiches QA.
    ① RÔLE — la copie du soir (cours réels). ② CONTEXTE D'APPEL — `passage`. ③ ENTRÉE — racine, S, fiches QA.
    ④ CONDITIONS D'ENTRÉE — S n'existe pas. ⑤ SORTIE — Aucune. [rend: 0] ⑥ TRAITEMENT — copier, écrire. ⑦ UNITÉ — —.
    ⑧ POURQUOI — les programmes du soir lisent tout le dépôt (épreuve E8). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit sous S.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    shutil.copytree(racine, S, ignore=lambda d, n: [x for x in n if (d == racine and x in (".git", "etudes", "archives"))
                                                    or x == "__pycache__"])
    ajouter_au_registre(S, fiches_qa)


def signal_du_soir(racine, valeurs_q):
    """Choisit la valeur et la séance du signal posé au soir : la première valeur des fiches QA dont le nom au cours
    maître est son onglet du référentiel ; la séance est l'AVANT-DERNIÈRE de cette valeur au cours maître (2024 et
    après seulement), pour que l'entrée se fasse à la dernière.
    ① RÔLE — un signal que le teneur sait servir. ② CONTEXTE D'APPEL — `main`, une fois. ③ ENTRÉE — la racine, les
    codes. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — TROIS valeurs : nom, séance, clôture (ou None, None, None). [rend: 3]
    ⑥ TRAITEMENT — lire le référentiel, puis les deux premières colonnes du cours maître. ⑦ UNITÉ — euros.
    ⑧ POURQUOI — la clôture se LIT dans la copie, jamais écrite ici (une ligne chiffrée de donnees/ ne se publie pas,
    A-555). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — rend la main. [sort: non]"""
    refs = [n for n in os.listdir(os.path.join(racine, "donnees")) if n.startswith("REFERENTIEL_VALEURS") and
            n.endswith(".csv")]
    _e, ref = lire_csv(os.path.join(racine, "donnees", refs[0]))
    onglet = {(l.get("mnemonique") or "").strip().upper(): (l.get("onglet_google") or "").strip().upper() for l in ref}
    lignes = {}
    with open(os.path.join(racine, COURS), encoding="utf-8-sig", newline="") as fh:
        r = csv.reader(fh)
        next(r, None)
        voulus = {onglet.get(c) for c in valeurs_q} - {None, ""}
        for l in r:
            if len(l) >= 6 and l[0].strip().upper() in voulus and l[1] >= "2024":
                lignes.setdefault(l[0].strip().upper(), []).append((l[1], l[5], l[0]))
    for c in valeurs_q:
        s = sorted(lignes.get(onglet.get(c), []))
        if len(s) >= 2:
            return s[-2][2], s[-2][0], float(s[-2][1])
    return None, None, None


def lancer_json(args, delai):
    """Lance ce fichier en processus neuf avec `args`, rend le JSON de sa dernière ligne, ou un rendu « impossible ».
    ① RÔLE — un processus neuf par couche. ② CONTEXTE D'APPEL — `passage`. ③ ENTRÉE — arguments, délai.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : dictionnaire. [rend: 1] ⑥ TRAITEMENT — subprocess, json.
    ⑦ UNITÉ — secondes. ⑧ POURQUOI — un module saboté ne survit pas au passage suivant. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — celui de la couche. ⑪ TERMINAISON — rend la main dans le délai. [sort: non]"""
    try:
        p = subprocess.run([sys.executable, "-B", ICI] + list(args), capture_output=True, text=True, timeout=delai)
    except subprocess.TimeoutExpired:
        return {"impossible": "délai de %d s dépassé" % delai}
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return {"impossible": "code %d, pas de JSON : %s" % (p.returncode, (p.stdout + p.stderr).strip()[-600:])}


def passage(racine, base, fiches, valeurs, soir_args, sabotage):
    """Un passage complet (sans sabotage, ou avec UN sabotage) ; rend {propriété: [état, détail]} et les refus.
    ① RÔLE — fabriquer W et S, poser le sabotage, lancer les trois couches, rassembler. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — racine, dossier de base, fiches, codes, arguments du soir, sabotage (ou None). ④ CONDITIONS D'ENTRÉE —
    le texte d'un sabotage est présent UNE fois. ⑤ SORTIE — DEUX valeurs : propriétés, refus. [rend: 2] ⑥ TRAITEMENT —
    voir ⑥ de l'en-tête. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit puis efface W et S.
    ⑪ TERMINAISON — rend la main ; lève RuntimeError si un texte de sabotage n'est pas unique. [sort: non]"""
    nom = "base" if sabotage is None else sabotage[0].split(" ")[0]
    W, S = os.path.join(base, "W_" + nom), os.path.join(base, "S_" + nom)
    try:
        fabriquer_w(racine, W, fiches, valeurs[0])
        fabriquer_s(racine, S, [f for f in fiches if f["id"].startswith("PROP-Q")])
        def saboter(t):
            for avant, apres in sabotage[3]:
                if t.count(avant) != 1:
                    raise RuntimeError("%s : texte à saboter présent %d fois" % (sabotage[0], t.count(avant)))
                t = t.replace(avant, apres)
            return t
        module = TEXTE_DU_MODULE
        if sabotage is not None and sabotage[2] == MODULE:
            module = saboter(module)
        for r in (W, S):
            open(os.path.join(r, MODULE), "w", encoding="utf-8").write(module)
        if sabotage is not None and sabotage[2] not in (None, MODULE):
            for r in (W, S):
                chem = os.path.join(r, sabotage[2])
                texte = saboter(open(chem, encoding="utf-8").read())   # lu AVANT d'ouvrir en écriture (tour 2 :
                open(chem, "w", encoding="utf-8").write(texte)          # l'ouverture vidait le fichier lu ensuite)
        ids = ["PROP-ORD"] + [f["id"] for f in fiches if f["id"].startswith(("PROP-L", "PROP-V"))] + \
              [f["id"] for f in fiches if f["id"].startswith("PROP-H")][:N_CHAINE_HASARD]
        octet = ["--octet"] if sabotage is not None and sabotage[2] is None else []
        rendus = [("couche en mémoire", lancer_json(["--couche", W, ",".join(valeurs)], 1800)),
                  ("⓪ ①", lancer_json(["--chaine", W, ",".join(ids)] + octet, 2400))]
        if soir_args[0] is None:
            rendus.append(("soir", {"impossible": "aucune valeur des fiches QA au cours maître de la copie"}))
        else:
            rendus.append(("soir", lancer_json(["--soir", S, soir_args[0], soir_args[1], repr(soir_args[2])], 1800)))
    finally:
        for r in (W, S):
            if os.path.isdir(r):
                shutil.rmtree(r, ignore_errors=True)
    prop, refus = {}, []
    for couche_, r in rendus:
        if "impossible" in r:
            for p in {"couche en mémoire": ("P1", "P2", "P5", "P6", "P7", "P8"), "⓪ ①": ("P1", "P3"),
                      "soir": ("P1", "P4", "SIL")}[couche_]:
                prop.setdefault(p, []).append(["NON MESURÉE", "%s : IMPOSSIBLE — %s" % (couche_, r["impossible"])])
            continue
        for p, v in r["proprietes"].items():
            prop.setdefault(p, []).append([v[0], "%s : %s" % (couche_, v[1])])
        refus += r.get("refus", [])
    final = {}
    for p in PROPRIETES:
        etats = [e for e, _d in prop.get(p, [])]
        etat = "ROUGE" if "ROUGE" in etats else ("NON MESURÉE" if (not etats or "NON MESURÉE" in etats) else "VERT")
        final[p] = [etat, " ‖ ".join(d for _e, d in prop.get(p, []))]
    return final, refus


def main_suite(racine, base, saboter, t0):
    """Le déroulé de la suite (option « --suite-seule ») : fiches factices aux valeurs fabriquées, passage sans
    sabotage, sabotages avec --saboter, tableau, refus, code.
    ① RÔLE — jouer ② ③ ④ sans rien lire d'avant 2024 (A-945). ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine, le
    dossier de base, le drapeau des sabotages, l'instant du départ. ④ CONDITIONS D'ENTRÉE — celles de `fabriquer_r`.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (comme `main`). [rend: 1] ⑥ TRAITEMENT — modèle VIDE aux colonnes du registre
    (première ligne seulement : les vraies fiches ne sont pas lues), `generer` sur CODES_FAB, `passage_suite`.
    ⑦ UNITÉ — —. ⑧ POURQUOI — consigne du 20-11-2026 : aucune vraie fiche ; R-731 ; R-734. ⑨ CE QUI CLOCHE — le
    modèle n'est plus la vraie ligne C5E10-QA-V1 (R-732) : les cases que `generer` ne remplit pas restent vides.
    ⑩ EFFET — écrit sous `base`. ⑪ TERMINAISON — rend la main. [sort: non]"""
    try:
        with open(os.path.join(racine, REG), encoding="utf-8-sig") as fh:
            entete = next(csv.reader([fh.readline()]))
        fiches = generer(dict.fromkeys(entete, ""), list(CODES_FAB), jours_ouvres(SUITE_DEBUT, SUITE_FIN)[-1])
        print("ÉPREUVE PAR PROPRIÉTÉS, SUITE DE LA CHAÎNE (A-945) — %d fiches factices (graine %d) · valeurs fabriquées "
              "%s · cours fabriqués du %s au %s (jours ouvrés), soir rejoué depuis le %s · rien d'avant 2024"
              % (len(fiches), GRAINE, ",".join(CODES_FAB), SUITE_DEBUT, SUITE_FIN, SOIR_DEBUT))
        print("JOUÉS EN MÉMOIRE : ② juge (contrat, porte, jouer, juger, grille de R-505) · ③ teneur (tenir, séance par "
              "séance) · ④ mesure (mesurer_une_strategie)")
        print("NON JOUÉS EN LIGNE DE COMMANDE : JOUER_LES_VERSIONS, TRIER_LES_VARIANTES, le juge et la mesure « main » "
              "— leur calibrage lit le témoin du golden ou les chiffres du golden (2000-2026), interdits par A-945")
        final, refus, ecarts_connus = passage_suite(racine, base, fiches, None)
        rouge = False
        print("\n— TABLEAU PROPRIÉTÉ × VERDICT (sans sabotage) —")
        for p in PROPRIETES_SUITE:
            e, det = final[p]
            print("  %-6s %-12s %s\n         %s" % (p, e, ENONCES[p], det[:900]))
            rouge = rouge or e != "VERT"
        print("\n— ÉCARTS CONNUS (ni verts ni rouges : nommés à chaque passage, le code n'applique pas encore la règle) —")
        for x in ecarts_connus:
            print("  %s" % x)
        if not ecarts_connus:
            print("  aucun")
        print("\n— MAILLONS OÙ UNE STRATÉGIE CONFORME EST REFUSÉE —")
        for r in refus:
            print("  %s · %s · %s" % (r["maillon"], r["fiche"], r["motif"][:300]))
        if not refus:
            print("  aucun")
        if saboter:
            print("\n— SABOTAGES DE LA SUITE (chacun doit faire rougir SA propriété) —")
            choisis = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--seulement=")]
            for sab in SABOTAGES_SUITE:
                if choisis and sab[0].split(" ")[0] not in choisis[0].split(","):
                    continue          # tranche choisie à la main (machine du Chat : moins de 10 min par tranche)
                try:
                    f2, _r, _e = passage_suite(racine, base, fiches, sab)
                except (RuntimeError, OSError) as e:
                    print("  ❌ %s : NON JOUÉ — %s" % (sab[0], e))
                    rouge = True
                    continue
                rouges = [p for p in PROPRIETES_SUITE if f2[p][0] == "ROUGE"]
                # LA RAISON DE LA MORSURE (cinquième champ, s'il existe) : le détail de la propriété doit la nommer —
                # un sabotage qui rougit pour une autre raison ne prouve pas ce qu'il prétend prouver.
                raison = sab[4] if len(sab) > 4 else None
                mord = f2[sab[1]][0] == "ROUGE" and (raison is None or raison in f2[sab[1]][1])
                print("  %s %s → %s ; rougissent : %s" % ("✅" if mord else "❌", sab[0],
                                                          "MORD" if mord else "SURVIT (%s)" % f2[sab[1]][0],
                                                          ", ".join(rouges) or "aucune"))
                if raison is not None:
                    print("       raison exigée dans le détail de %s : « %s » — %s" % (
                        sab[1], raison, "présente" if raison in f2[sab[1]][1] else "ABSENTE"))
                print("       %s : %s" % (sab[1], f2[sab[1]][1][:400]))
                rouge = rouge or not mord
        print("\nDURÉE : %.0f s" % (time.time() - t0))
        print("VERDICT : %s" % ("TOUT TIENT" if not rouge else "NON CONFORME"))
        return 1 if rouge else 0
    except (OSError, LookupError, AssertionError, RuntimeError, ValueError) as e:
        print("ÉPREUVE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2


def main(argv):
    """Le déroulé : copies, passage sans sabotage, sabotages avec --saboter, tableau, liste des refus, code.
    ① RÔLE — ⑥ de l'en-tête. ② CONTEXTE D'APPEL — `__main__`. ③ ENTRÉE — `argv`. ④ CONDITIONS D'ENTRÉE — celles de
    l'en-tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — générer les fiches (graine fixe), passage
    « base », puis un passage par sabotage ; afficher. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — dossier temporaire effacé. ⑪ TERMINAISON — rend la main. [sort: non]"""
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not os.path.isdir(os.path.join(args[0], "programmes")):
        print(__doc__.split("① RÔLE")[0])
        return 2
    racine, saboter = os.path.abspath(args[0]), "--saboter" in argv
    t0 = time.time()
    base = tempfile.mkdtemp(prefix="proprietes_chaine_")
    if "--suite-seule" in argv:
        try:
            return main_suite(racine, base, saboter, t0)
        finally:
            shutil.rmtree(base, ignore_errors=True)
    if "--bout-en-bout" in argv:
        shutil.rmtree(base, ignore_errors=True)
        base = tempfile.mkdtemp(prefix="proprietes_beb_", dir=os.path.dirname(racine))   # même disque : liens durs
        try:
            return main_bout_en_bout(racine, base, saboter, t0)
        finally:
            shutil.rmtree(base, ignore_errors=True)
    try:
        valeurs = choisir_les_valeurs(racine)
        modele = ligne_modele(racine)
        # la dernière séance des cours fabriqués : le dernier jour ouvré de FIN au plus (contrôlé par le calendrier
        # dans la couche ; L14 n'attend aucune opération quel que soit ce jour)
        from datetime import date, timedelta
        d = date.fromisoformat(FIN)
        while d.weekday() > 4:
            d -= timedelta(days=1)
        fiches = generer(modele, valeurs, d.isoformat())
        q_univ = [c.strip() for c in next(f for f in fiches if f["id"] == "PROP-Q2")["univers"].split(",")]
        soir_args = signal_du_soir(racine, q_univ)
        print("ÉPREUVE PAR PROPRIÉTÉS DE LA CHAÎNE — %d fiches factices (graine %d) · valeurs %s (victime de P1 : %s) · "
              "signal du soir : %s le %s" % (len(fiches), GRAINE, ",".join(valeurs[1:]), valeurs[0], soir_args[0],
                                             soir_args[1]))
        print("MAILLONS NON JOUÉS DANS CE MODE (A-941) : %s — la suite se joue avec « --suite-seule » (A-945) ; en "
              "ligne de commande, « --bout-en-bout » les tente et nomme ce qui les bloque" % " · ".join(NON_JOUES))
        final, refus = passage(racine, base, fiches, valeurs, soir_args, None)
        rouge = False
        print("\n— TABLEAU PROPRIÉTÉ × VERDICT (sans sabotage) —")
        for p in PROPRIETES:
            e, det = final[p]
            print("  %-4s %-12s %s\n         %s" % (p, e, ENONCES[p], det[:900]))
            rouge = rouge or e != "VERT"
        print("\n— MAILLONS OÙ UNE STRATÉGIE CONFORME EST REFUSÉE OU IGNORÉE —")
        vus = set()
        for r in refus:
            cle = (r["maillon"], r["fiche"], r["motif"][:80])
            if cle in vus:
                continue
            vus.add(cle)
            print("  %s · %s · %s" % (r["maillon"], r["fiche"], r["motif"][:300]))
        if not refus:
            print("  aucun")
        for m in NON_JOUES:
            print("  %s · NON JOUÉ dans ce mode (A-941) ; voir « --suite-seule » (A-945) et « --bout-en-bout »" % m)
        if saboter:
            print("\n— SABOTAGES (chacun doit faire rougir SA propriété) —")
            for sab in SABOTAGES:
                try:
                    f2, _r = passage(racine, base, fiches, valeurs, soir_args, sab)
                except (RuntimeError, AssertionError) as e:
                    print("  ❌ %s : NON JOUÉ — %s" % (sab[0], e))
                    rouge = True
                    continue
                rouges = [p for p in PROPRIETES if f2[p][0] == "ROUGE"]
                mord = f2[sab[1]][0] == "ROUGE"
                print("  %s %s → %s ; rougissent : %s" % ("✅" if mord else "❌", sab[0],
                                                          "MORD" if mord else "SURVIT (%s)" % f2[sab[1]][0],
                                                          ", ".join(rouges) or "aucune"))
                if not mord:
                    print("       %s : %s" % (sab[1], f2[sab[1]][1][:500]))
                rouge = rouge or not mord
        print("\nDURÉE : %.0f s" % (time.time() - t0))
        print("VERDICT : %s" % ("TOUT TIENT" if not rouge else "NON CONFORME"))
        return 1 if rouge else 0
    except (OSError, LookupError, AssertionError, RuntimeError, ValueError) as e:
        print("ÉPREUVE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--couche":
        couche(sys.argv[2], sys.argv[3].split(","))
        sys.exit(0)
    if len(sys.argv) >= 4 and sys.argv[1] == "--chaine":
        chaine(sys.argv[2], sys.argv[3].split(","), "--octet" in sys.argv)
        sys.exit(0)
    if len(sys.argv) in (4, 5) and sys.argv[1] == "--suite":      # 5 : « --sans-accidents » (S-ACC) ou
        # « --accidents-avant-le-soir » (S-ACC2) ou « --sans-controle=… » (S-I1a, S-I1b)
        suite(sys.argv[2], sys.argv[3])
        sys.exit(0)
    if len(sys.argv) in (4, 5) and sys.argv[1] == "--beb":       # 5 : un sabotage de SABOTAGES_BEB
        beb(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) == 5 else "")
        sys.exit(0)
    if len(sys.argv) == 6 and sys.argv[1] == "--soir":
        soir(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))
        sys.exit(0)
    sys.exit(main(sys.argv))
