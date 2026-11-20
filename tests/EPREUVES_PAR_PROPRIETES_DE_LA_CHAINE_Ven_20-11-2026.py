#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py — Ven 20-11-2026 (Paris). EN ESSAI · épreuve. Simulation
uniquement : aucun ordre réel.

LE SENS EN TÊTE. Décision de Jean-Luc du 19-11-2026 à 19h09 (BACKLOG A-923, réponse « 1 ») : faire passer N'IMPORTE
QUELLE stratégie dans tout le circuit, en éprouvant des PROPRIÉTÉS sur des stratégies factices plutôt qu'une stratégie
à la fois (étude etudes/ETUDE_CONTRAT_DE_STRATEGIE_ET_PROPRIETES_2026-11-19_19h16.md, sections B et C, étape 2 du plan
D). Décision de Jean-Luc du 20-11-2026 à 12h45 (BACKLOG A-941, réponse « 1 ») : l'épreuve se joue SUR GITHUB (deux
copies du dépôt avaient été refusées sur la machine du Chat), et les maillons ② JOUER, ③ TRIER, ④ juge restent
BLOQUÉS : ils sont nommés « non joués, décision de Jean-Luc », jamais comptés verts.

Ce que l'épreuve joue, sur des COPIES faites sous un dossier temporaire de la machine qui la lance :
  · la COUCHE EN MÉMOIRE : le contrat de stratégie (`manques_du_contrat`) et `jouer` du juge, sur des cours FABRIQUÉS
    aux séances réelles 2024-2025 (jamais 2000-2023 : aucun regard, R-505 ③) ;
  · les maillons ⓪ PREPARER et ① DECLINER, par programmes/ENCHAINER_LA_MOULINETTE.py, comme la chaîne officielle ;
  · le SOIR : programmes/DETECTER_LES_SIGNAUX_GITHUB.py puis programmes/TENIR_LES_POSITIONS.py, sur une copie entière
    (cours réels du cours maître), avec deux fiches factices à l'état QA.
Les stratégies factices sortent d'un générateur à graine fixe (Python standard, aucun paquet nouveau) : les limites
de l'étude une par une sur une fiche ordinaire, plus des fiches tirées au hasard. Leur module de signal factice est
écrit dans la copie, jamais au dépôt.

LES PROPRIÉTÉS (étude, tableau B) — P1 rien ne plante sur une fiche conforme · P2 une fiche non conforme est refusée,
sa case nommée · P3 chaque maillon ⓪ ① laisse sa preuve (journal de la chaîne, témoins intacts) · P4 le soir n'achète
que ce que la fiche permet (univers, seuils de SA fiche, un jeton) · SIL aucune fiche conforme suivie n'est ignorée en
silence par le soir · P5 le gain écrit se retrouve (vente rejouée par MODULE_POSITIONS.vendre) · P6 aucun signal ne lit
une séance future · P7 même entrée, même résultat · P8 les limites sont tenues (jamais → 0 opération, rien sur la
dernière séance, rien hors période, horizon 1 tenu).

USAGE
    python3 -B tests/EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py <racine> [--saboter]
    <racine> : la racine d'une copie du dépôt (sur GitHub, la copie du circuit des épreuves longues), jamais modifiée.

① RÔLE — Mesurer les propriétés P1 à P8 et SIL, et dresser la liste des maillons où une stratégie CONFORME au contrat
  est REFUSÉE ou IGNORÉE.
② CONTEXTE D'APPEL — Le circuit des épreuves longues sur GitHub (codes ProprietesChaine et ProprietesSabot de
  tests/LANCEMENT_DES_EPREUVES.json), décision A-941. À la main ailleurs que sur la machine du Chat.
③ ENTRÉE — La ligne de commande (USAGE). Appels internes : « --couche <W> », « --chaine <W> [--octet] », « --soir <S> ».
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
  rend un code non nul, jamais vert) ; R-708 (aucune formule recopiée : les seuils, la vente, les frais sont demandés
  aux programmes du circuit).
⑨ CE QUI CLOCHE — ① La validation des réglages exigée par DECLINER (« Jean-Luc le JJ-MM-AAAA ») est ÉCRITE PAR
  L'ÉPREUVE dans la copie jetable, pour des fiches factices : elle ne vaut validation de rien, et ne quitte jamais la
  copie. ② La couche en mémoire joue `jouer` sans lecture du lecteur (pas de composition de l'indice ni de trous) : la
  composition n'est pas éprouvée ici. ③ Le soir est joué une fois (deux passages du teneur), sur la dernière séance du
  cours maître ; P4 n'est mesurée que si une position factice s'ouvre — sinon « NON MESURÉE ». ④ P6 est mesurée sur
  un échantillon de séances (une sur trois). ⑤ Maillons ②, ③, ④ non joués (A-941). ⑥ Les fiches réelles du registre
  restent dans la copie du soir : le détecteur voit ensemble C5 et les fiches factices.
⑩ EFFET — Écrit sous un dossier temporaire, effacé à la fin ; affiche.
⑪ TERMINAISON — Chaque processus lancé est borné (couche 1 800 s, chaîne 2 400 s, soir 1 800 s ; chaque programme du
  circuit 400 s). [sort: oui — code]
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

# LES SABOTAGES — (nom, propriété qui DOIT rougir, fichier, texte avant, texte après) ; fichier None : geste spécial.
SABOTAGES = (
    ("S-P1 contrôle VALEURS_TTF neutralisé", "P1", CONTRATS,
     '                        mod_pos.cout_d_un_ordre(c, d, "achat", mod_pos.CAPITAL, bareme=nom_du_bareme)\n',
     '                        pass\n'),
    ("S-P2 manques_du_jeu rend []", "P2", JUGE,
     '    manq = []\n    entree = (fiche.get("entree") or "").strip()\n',
     '    return []\n    manq = []\n    entree = (fiche.get("entree") or "").strip()\n'),
    ("S-P3 un octet changé dans un fichier témoigné", "P3", None, "octet", ""),
    ("S-P4 teneur forcé aux seuils de C5", "P4", TENIR,
     '                tp, sl, _h = juge.lecture_du_soir(base, x)\n',
     '                tp, sl, _h = 0.04, 0.025, 20\n'),
    ("S-SIL suivie_par_le_soir rend faux", "SIL", CONTRATS,
     '    etat = (fiche.get("etat_vie") or "").strip().upper()\n    return etat in ETATS_SUIVIS_PAR_LE_SOIR and',
     '    return False\n    etat = (fiche.get("etat_vie") or "").strip().upper()\n'
     '    return etat in ETATS_SUIVIS_PAR_LE_SOIR and'),
    ("S-P5 vente jouée avec un autre tp", "P5", JUGE,
     '                op = jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture, bareme, recu)\n',
     '                op = jouer_une_entree(v, serie, j, tp * 1.5, sl, h, mod_positions, lecture, bareme, recu)\n'),
    ("S-P6 module tricheur (clôture du lendemain)", "P6", MODULE,
     '        if serie[i]["close"] / serie[i - 1]["close"] - 1 <= -baisse:\n',
     '        if i + 1 < n and serie[i + 1]["close"] / serie[i]["close"] - 1 <= -baisse:\n'),
    ("S-P7 tirage sans graine", "P7", MODULE,
     '        alea = random.Random(graine)\n', '        alea = random.Random()\n'),
    ("S-P8 filtre de période retiré du juge", "P8", JUGE,
     '                if periode and not (periode[0] <= d_sig <= periode[1]):\n                    continue\n', ''),
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


def cours_fabriques(valeurs, mnemo, dates):
    """Fabrique, à graine fixe, une série par valeur aux séances réelles : marche au hasard bornée, et environ une
    séance sur seize une baisse de 2,5 à 4 %.
    ① RÔLE — des cours où les signaux se déclenchent. ② CONTEXTE D'APPEL — `couche`. ③ ENTRÉE — les codes, la table
    code → nom du juge, les séances. ④ CONDITIONS D'ENTRÉE — chaque code est dans `mnemo`. ⑤ SORTIE — UNE valeur :
    {nom: [séances {date, open, high, low, close, volume}]}. [rend: 1] ⑥ TRAITEMENT — Random(GRAINE + rang).
    ⑦ UNITÉ — euros. ⑧ POURQUOI — jamais 2000-2023 (aucun regard). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    cours = {}
    for r, code in enumerate(valeurs):
        alea, c, serie = random.Random(GRAINE + r), 50.0 + 10 * r, []
        for d in dates:
            o = c * (1 + alea.uniform(-0.003, 0.003))
            ret = -alea.uniform(0.025, 0.04) if alea.random() < 1 / 16 else alea.uniform(-0.012, 0.0125)
            cl = c * (1 + ret)
            serie.append({"date": d, "open": round(o, 4), "high": round(max(o, cl) * (1 + alea.uniform(0, 0.006)), 4),
                          "low": round(min(o, cl) * (1 - alea.uniform(0, 0.006)), 4), "close": round(cl, 4),
                          "volume": 100000.0})
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
            serie = cours[op["valeur"]]
            j = [b["date"] for b in serie].index(op["date_entree"])
            v = mod_pos.vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")
            if v is None:
                prop["P5"].append("%s %s %s : vendre ne rend rien" % (i, op["valeur"], op["date_entree"]))
                continue
            fr = mod_pos.frais_aller_retour(100000.0 / v["pe"], v["pe"], v["px"], op["valeur"], op["date_entree"],
                                            v["date_sortie"], bareme)["total"]
            if (v["pe"], v["px"], v["motif"], v["date_sortie"]) != (op["pe"], op["px"], op["motif"],
                                                                     op["date_sortie"]) or abs(fr - op["frais"]) > 1:
                prop["P5"].append("%s %s %s : écrit (%s, %s, %s) · rejoué (%s, %s, %s)" % (
                    i, op["valeur"], op["date_entree"], op["px"], op["motif"], op["date_sortie"], v["px"], v["motif"],
                    v["date_sortie"]))
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
               "⓪ ① : %d fiche(s) conforme(s) lancée(s) ; %s" % (n1, " ; ".join(p1[:3]) or "aucun plantage")],
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
    for i in qa:
        f = fiches[i]
        tp_f, sl_f, _h = J.lecture_du_soir(S, f)
        univ = {c.strip().upper() for c in f["univers"].split(",") if c.strip()}
        miennes = [p for p in positions if p.get("strategie") == i]
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
               "%d position(s) factice(s) OUVERTE(S) mesurée(s) ; %s%s" % (
                   n4, " ; ".join(p4[:3]) or "aucun défaut",
                   "" if n4 else " ; teneur : " + " | ".join(l.strip() for l in texte_t2.splitlines()
                                                             if "PROP-" in l or "❌" in l or "CODE" in l)[:300])],
        "P1": ["ROUGE" if p1 else "VERT", "soir : détecteur %d, teneur %d puis %d ; %s" % (
            code_d, code_t, code_t2, " ; ".join(p1) or "aucun plantage")]},
        "refus": refus}
    print(json.dumps(rendu, ensure_ascii=False))


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
        module = TEXTE_DU_MODULE
        if sabotage is not None and sabotage[2] == MODULE:
            if module.count(sabotage[3]) != 1:
                raise RuntimeError("%s : texte à saboter présent %d fois" % (sabotage[0], module.count(sabotage[3])))
            module = module.replace(sabotage[3], sabotage[4])
        for r in (W, S):
            open(os.path.join(r, MODULE), "w", encoding="utf-8").write(module)
        if sabotage is not None and sabotage[2] not in (None, MODULE):
            for r in (W, S):
                chem = os.path.join(r, sabotage[2])
                t = open(chem, encoding="utf-8").read()
                if t.count(sabotage[3]) != 1:
                    raise RuntimeError("%s : texte à saboter présent %d fois" % (sabotage[0], t.count(sabotage[3])))
                open(chem, "w", encoding="utf-8").write(t.replace(sabotage[3], sabotage[4]))
        ids = ["PROP-ORD"] + [f["id"] for f in fiches if f["id"].startswith(("PROP-L", "PROP-V"))] + \
              [f["id"] for f in fiches if f["id"].startswith("PROP-H")][:N_CHAINE_HASARD]
        octet = ["--octet"] if sabotage is not None and sabotage[3] == "octet" else []
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
        print("MAILLONS NON JOUÉS, DÉCISION DE JEAN-LUC (A-941) : %s" % " · ".join(NON_JOUES))
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
            print("  %s · NON JOUÉ, décision de Jean-Luc (A-941)" % m)
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
    if len(sys.argv) == 6 and sys.argv[1] == "--soir":
        soir(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))
        sys.exit(0)
    sys.exit(main(sys.argv))
