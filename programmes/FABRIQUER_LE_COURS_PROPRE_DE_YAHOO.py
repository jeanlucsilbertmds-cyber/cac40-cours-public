#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py — Jeu 22-10-2026 (Paris). Simulation uniquement.

① RÔLE — Refaire, depuis les réponses brutes de Yahoo gardées au dépôt, les deux fichiers qui ouvrent l'historique des
  20 ans : le cours propre de Yahoo (`yahoo_ohlcv_propre.csv`, une barre par valeur et par séance) et le relevé des
  événements (`evenements.json`, les divisions et le nombre de dividendes de chaque valeur). C'est le maillon
  « brut + traitement = fichier propre » qui manquait : le fichier propre du 02-10-2026 venait d'un brut perdu et de
  cinq programmes jamais déposés (A-578 ④).
② CONTEXTE D'APPEL — Lancé à la main par le Chat, ou par son épreuve
  (tests/EPREUVES_DU_COURS_PROPRE_DE_YAHOO_Jeu_22-10-2026.py). Aucune tâche du soir ne l'appelle. Commande :
  python3 programmes/FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py <racine du dépôt> <dossier de sortie>
③ ENTRÉE — Deux arguments : la racine d'un dépôt ; un dossier de sortie QUI N'EXISTE PAS ENCORE. Sont lus sous la
  racine : le référentiel des valeurs (REFERENTIEL), les réponses brutes (BRUTS, une par valeur, nommée
  <mnémonique>.PA.json) et le carnet de provenance (CARNET). Le programme ne télécharge rien.
④ CONDITIONS D'ENTRÉE — Les trois sources existent ; le dossier de sortie n'existe pas (son dossier parent doit exister,
  sinon l'écriture échoue et rend 2), et il n'est ni sous la racine donnée ni sous le dépôt qui porte ce programme (verser dans les données est un geste à part,
  décidé par Jean-Luc). Chaque réponse est inscrite UNE fois au carnet, comme téléchargement, avec l'empreinte qu'elle a.
⑤ SORTIE — Le code de sortie, UNE valeur : 0 si le dossier de sortie est créé avec les deux fichiers ; 1 « REFUSÉ » si
  une réponse manque, n'est pas inscrite au carnet comme téléchargement, ou n'a pas l'empreinte inscrite ; 2
  « IMPOSSIBLE » si le programme n'a pas pu tourner (arguments, source absente, dossier de sortie refusé, réponse
  illisible ou mal formée, écriture impossible). Hors du code 0, le dossier de sortie n'existe pas. À l'écran : une
  ligne par fichier écrit, avec son nombre de lignes ou d'entrées et son empreinte. [rend: 1]
⑥ TRAITEMENT — ① lire le référentiel : 40 valeurs, nom usuel et mnémonique · ② pour chaque valeur, lire sa réponse et
  vérifier au carnet son inscription et son empreinte · ③ cours : seulement les réponses d'une ACTION cotée en euros
  (`meta.instrumentType` « EQUITY », `meta.currency` « EUR ») ; garder chaque barre complète et cohérente (ouverture,
  plus haut, plus bas, clôture et volume présents ; volume non nul ; plus bas ≤ ouverture ≤ plus haut et plus bas ≤
  clôture ≤ plus haut), datée à Paris, jusqu'à COUPURE, sans STELLANTIS avant DEBUT_STELLANTIS ; prix arrondis à
  4 décimales ; lignes triées · ④ événements : pour les 40 valeurs, divisions [date, numérateur, dénominateur] triées et
  nombre de dividendes, jusqu'à COUPURE ; d'abord les actions par ordre alphabétique, puis les autres par ordre
  alphabétique · ⑤ écrire les deux fichiers dans un dossier provisoire, puis le renommer d'un seul geste.
⑦ UNITÉ — Des euros (prix arrondis à 4 décimales), des titres (volume), des dates de Paris (AAAA-MM-JJ).
⑧ POURQUOI — Décisions de Jean-Luc du 22-10-2026 : à 08h38, « l'historique des 20 ans remonte à un brut » ; à 08h42,
  le brut est celui du 21-10-2026, le seul dont chaque réponse garde son adresse ; à 23h29, les 40 réponses sont
  rangées une par une et inscrites au carnet (BACKLOG A-599 ⑦ à ⑨). Ce programme les contrôle à chaque lancement contre
  le carnet, et son épreuve le prouve chaque nuit ; le contrôle K23 ne les verra qu'une fois inscrite au carnet la ligne
  du fichier propre (A-599 ⑪, défaut I6). Les règles du traitement sont celles qui redonnent, MESURÉ la nuit du 21 au 22-10-2026, le fichier propre et les
  événements (scripts de mesure de
  `etudes/brouillons_chat/INVENTAIRE_DE_LA_PROVENANCE_DES_20_ANS_Dim_18-10-2026/scripts/`). Vérifier les réponses
  contre le carnet, et non contre un fichier écrit par le même téléchargement, est l'avis du superviseur R-759 du
  22-10-2026 : une seule propriété, « chaque source a l'empreinte inscrite au carnet », couvre tous les cas d'altération.
⑨ CE QUI CLOCHE — Les règles des filtres sont MESURÉES (elles redonnent le fichier du 02-10-2026), pas retrouvées dans
  les programmes perdus : un filtre de l'original qui ne change rien sur ces données ne se voit pas. · Le fichier propre
  refait diffère de celui du 02-10-2026 sur 13 lignes retirées et 14 ajoutées, toutes du 02-10-2026 (cause non prouvée ;
  la barre ESSILORLUXOTTICA de ce jour manquait entièrement à l'ancien fichier). · Le référentiel n'est pas vérifié
  contre le carnet : s'il échangeait deux mnémoniques, les cours d'une valeur seraient écrits sous le nom d'une autre ;
  seule l'empreinte attendue par l'épreuve le verrait ; une valeur écrite deux fois au référentiel passe aussi, avec
  le code 0 (relecteur du tour 2, 23-10-2026, A-N4 : ACCOR doublée → 252 922 lignes), car les dictionnaires par nom et par
  symbole écrasent sans le dire. · Les événements de STELLANTIS comptent les dividendes de
  Peugeot S.A. d'avant le 18-01-2021 (fidèle au fichier du 02-10-2026). · Sur ces réponses, la date de Paris est
  partout la date en temps universel (séances datées entre 09h00 et 16h30 à Paris) : la règle « dater à Paris » n'a de
  dent que sur un cas fabriqué. · À NE PAS VERSER avant d'avoir relancé la réparation de l'historique long et ses
  contrôles (BACKLOG A-599 ⑧, ⑨ et ⑪) : le nouveau fichier change 13 lignes du 02-10-2026 et en ajoute 1 ; K23, lancé
  sur une copie où il remplace l'ancien, refuse 14 lignes de l'historique réparé (11 volumes, 2 plus bas, la ligne
  ESSILORLUXOTTICA) et K20 une (ACCOR, volume) — mesuré le 23-10-2026, sortie entière
  `etudes/brouillons_chat/COURS_PROPRE_DE_YAHOO_Jeu_22-10-2026/PREUVES_DU_RELECTEUR_TOUR2/SORTIE_K23_BRANCHE_juste_LISTE_COMPLETE.txt`,
  sur une copie où le relecteur a ajouté au carnet une ligne qui relie le cours propre aux 40 réponses : une
  conception possible, NON DÉCIDÉE (voir le LISEZ_MOI de ce dossier).
  · Entre le contrôle de la sortie et le renommage, un dossier VIDE créé au même nom par un autre processus serait
  remplacé sans erreur (relecteur du 23-10-2026, A-N7) : cas d'école, non traité. · Ce programme n'est pas au
  certificat de référence (gouvernance/CERTIFICAT_REFERENCE.json) : aucun recul de couverture ne le signalerait.
⑩ EFFET — Lit les trois sources ; crée le dossier de sortie avec deux fichiers, aux droits 0o700 (le dossier provisoire
  est créé par tempfile.mkdtemp, qui les fixe) ; rien d'autre. Un échec n'efface que le dossier provisoire que le
  programme a lui-même créé ; une coupure peut en laisser un, nommé <sortie>.en_cours.<suffixe au hasard>.
⑪ TERMINAISON — Rend la main ; aucun appel réseau, aucun sous-processus ; chaque réponse est lue en entier en mémoire
  (moins de 1 Mo chacune aujourd'hui) ; sort par sys.exit. [sort: oui]
"""
import csv
import datetime
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
from zoneinfo import ZoneInfo

REFERENTIEL = os.path.join("donnees", "REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv")
BRUTS = os.path.join("donnees", "sources_yahoo", "bruts_yahoo_21-10-2026")
CARNET = os.path.join("donnees", "PROVENANCE_DES_FICHIERS.csv")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# La sorte « téléchargement » du carnet de provenance : déclarée une fois au contrat des fichiers, lue ici (R-708 :
# deux écritures d'une même valeur divergent). Le 22-10-2026, une copie écrite « TELECHARGEMENT » faisait refuser
# les 40 réponses par le contrôleur K23.
# L'en-tête du cours propre est celui d'un fichier de cours nouveau, déclaré au même contrat (relecteur du 23-10-2026, P-N2).
from CONTRATS_DES_FICHIERS import COURS_NOUVEAUX, TELECHARGEMENT  # noqa: E402
# La dernière séance gardée. Le fichier propre du 02-10-2026 s'arrête ce jour-là ; au-delà, les séances viennent du
# fichier maître des cours, tenu chaque soir. Mesuré : coupées au 02-10, ces réponses redonnent le fichier propre refait
# depuis le témoin du 08-10 (empreinte ea18640899c7a90d…) ; sans coupure, l'empreinte change.
COUPURE = "2026-10-02"
# Stellantis est née le 16-01-2021 de la fusion de Peugeot S.A. et de Fiat Chrysler ; sa première séance est le
# 18-01-2021. Avant, Yahoo sert sous STLAP.PA la série de Peugeot S.A., une autre société (REGISTRE, règle I-7 :
# « jamais fusionner les séries »). Mesuré : le fichier du 02-10-2026 n'a aucune barre STELLANTIS avant cette date.
DEBUT_STELLANTIS = "2021-01-18"
# Une réponse donne des COURS seulement si c'est une action cotée en euros. Mesuré le 22-10-2026 : 39 réponses sur 40 ;
# la 40e, MT.PA (ARCELORMITTAL), est rangée par Yahoo en fonds, sans devise, dernière clôture le 07-05-2018 — ses cours
# ne servent pas, ses événements si (rapport N2 de la nuit du 21-10-2026).
TYPE_ACTION, DEVISE = "EQUITY", "EUR"
PARIS = ZoneInfo("Europe/Paris")
ENTETE = COURS_NOUVEAUX


class Refus(Exception):
    """Un refus voulu : une source n'est pas celle qu'inscrit le carnet.

    ① RÔLE — Distinguer un refus décidé par un contrôle (code 1) d'une panne (code 2).
    ② CONTEXTE D'APPEL — Levée par `lire_les_sources` seulement ; attrapée par `main`.
    ③ ENTRÉE — Le texte du refus. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — ⑥ TRAITEMENT — —
    ⑦ UNITÉ — — ⑧ POURQUOI — Superviseur R-759 du 22-10-2026 : ranger toute erreur Python en « refus » faisait
      passer un plantage pour un refus, et l'épreuve ne voyait plus la différence.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — — [sort: non]
    """


def date_de_paris(horodatage):
    """Rend la date de Paris d'un horodatage de Yahoo.

    ① RÔLE — Dater une barre ou un événement au jour de la Bourse de Paris.
    ② CONTEXTE D'APPEL — `barres` et `evenements`, pour chaque horodatage lu ; l'épreuve, directement.
    ③ ENTRÉE — `horodatage` : des secondes depuis le 01-01-1970 en temps universel, entier ou texte d'entier.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la date, texte AAAA-MM-JJ.
      [rend: 1]
    ⑥ TRAITEMENT — Convertir en heure de Paris, garder le jour.
    ⑦ UNITÉ — Secondes en entrée ; date de Paris en sortie.
    ⑧ POURQUOI — Une séance de Paris se date à Paris. Exemple fabriqué : 23h30 en temps universel un soir d'hiver est
      déjà le lendemain à Paris.
    ⑨ CE QUI CLOCHE — Sur les réponses du 21-10-2026, les deux lectures donnent partout le même jour (mesuré par le
      relecteur du 22-10-2026) : seul le cas fabriqué de l'épreuve donne une dent à cette règle.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return datetime.datetime.fromtimestamp(int(horodatage), PARIS).date().isoformat()


def lire_les_sources(racine):
    """Rend les valeurs du référentiel et leurs réponses, chacune vérifiée contre le carnet.

    ① RÔLE — Ne laisser passer que des réponses identiques, à l'octet, à celles que le carnet inscrit.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Les trois sources existent (vérifié par `main`).
    ⑤ SORTIE — DEUX valeurs : la liste des (nom usuel, symbole) du référentiel, dans son ordre, et {symbole : octets de
      la réponse}.
      [rend: 2]
    ⑥ TRAITEMENT — Lire le référentiel (symbole = mnémonique + « .PA ») et le carnet ; pour chaque symbole, lire
      BRUTS/<symbole>.json, chercher au carnet les lignes de ce chemin : il en faut exactement une, de sorte
      TELECHARGEMENT, dont l'empreinte est celle du fichier.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Voir la fiche en tête, ⑧ : une seule propriété, l'empreinte inscrite au carnet.
    ⑨ CE QUI CLOCHE — Le référentiel lui-même n'est pas vérifié (voir la fiche en tête, ⑨).
    ⑩ EFFET — Lit les fichiers ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève Refus (réponse absente, non inscrite, inscrite deux fois, d'une autre sorte, ou
      d'une autre empreinte) ; une panne de lecture se propage.
      [sort: non]
    """
    with open(os.path.join(racine, REFERENTIEL), encoding="utf-8-sig", newline="") as f:
        valeurs = [(r["nom_usuel"], r["mnemonique"] + ".PA") for r in csv.DictReader(f)]
    with open(os.path.join(racine, CARNET), encoding="utf-8", newline="") as f:
        carnet = list(csv.DictReader(f))
    reponses = {}
    for _, s in valeurs:
        chemin = os.path.join(BRUTS, s + ".json").replace(os.sep, "/")
        p = os.path.join(racine, BRUTS, s + ".json")
        if not os.path.isfile(p):
            raise Refus(f"{s} : réponse absente ({chemin})")
        octets = open(p, "rb").read()
        lignes = [r for r in carnet if r["fichier"] == chemin]
        if len(lignes) != 1:
            raise Refus(f"{s} : inscrit {len(lignes)} fois au carnet, au lieu d'une")
        if lignes[0]["produit_par"] != TELECHARGEMENT:
            raise Refus(f"{s} : inscrit au carnet comme « {lignes[0]['produit_par']} », pas comme téléchargement")
        if hashlib.sha256(octets).hexdigest() != lignes[0]["sha256"]:
            raise Refus(f"{s} : empreinte différente de celle du carnet")
        reponses[s] = octets
    return valeurs, reponses


def est_une_action(octets):
    """Dit si une réponse est celle d'une action cotée en euros.

    ① RÔLE — Choisir les réponses qui donnent des cours.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par valeur.
    ③ ENTRÉE — `octets` : la réponse.
    ④ CONDITIONS D'ENTRÉE — Elle se lit en JSON et porte chart.result[0].meta.
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — Comparer meta.instrumentType à TYPE_ACTION et
    meta.currency à DEVISE.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une propriété de la réponse plutôt qu'un nom de valeur épelé :
    voir la constante TYPE_ACTION.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; une réponse mal
    formée lève une erreur.
      [sort: non]
    """
    m = json.loads(octets.decode("utf-8"))["chart"]["result"][0]["meta"]
    return m.get("instrumentType") == TYPE_ACTION and m.get("currency") == DEVISE


def barres(valeur, octets):
    """Rend les barres gardées d'une valeur, au format du fichier propre.

    ① RÔLE — Appliquer les règles du fichier propre aux cours d'une réponse.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par action.
    ③ ENTRÉE — `valeur` : le nom usuel de la valeur ; `octets` : la réponse de Yahoo.
    ④ CONDITIONS D'ENTRÉE — La réponse se lit en JSON et porte chart.result[0], ses horodatages et ses cours.
    ⑤ SORTIE — UNE valeur : la liste des lignes [valeur, date, ouverture, haut, bas, clôture, volume], textes.
     
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥ ③.
    ⑦ UNITÉ — Euros, titres, dates de Paris.
    ⑧ POURQUOI — Ces règles redonnent, mesuré, le fichier propre (voir la fiche en tête, ⑧).
    ⑨ CE QUI CLOCHE — Une barre écartée ne laisse pas de trace ici ; une action dont toutes les barres seraient
      écartées disparaîtrait du fichier sans un mot (seule l'empreinte attendue par l'épreuve le verrait).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; une réponse mal formée lève KeyError, IndexError, TypeError ou ValueError.
     
      [sort: non]
    """
    r = json.loads(octets.decode("utf-8"))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    lignes = []
    for i, t in enumerate(r["timestamp"]):
        d = date_de_paris(t)
        o, h, b, c, vol = (q[k][i] for k in ("open", "high", "low", "close", "volume"))
        if None in (o, h, b, c, vol) or vol == 0 or not (b <= o <= h and b <= c <= h):
            continue
        if d > COUPURE or (valeur == "STELLANTIS" and d < DEBUT_STELLANTIS):
            continue
        lignes.append([valeur, d, *(repr(round(x, 4)) for x in (o, h, b, c)), str(int(vol))])
    return lignes


def evenements(octets):
    """Rend les divisions et le nombre de dividendes d'une réponse, jusqu'à la coupure.

    ① RÔLE — Refaire une entrée de `evenements.json`.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par valeur.
    ③ ENTRÉE — `octets` : la réponse de Yahoo.
    ④ CONDITIONS D'ENTRÉE — La réponse se lit en JSON et porte chart.result[0] ; « events » peut manquer.
    ⑤ SORTIE — UNE valeur : {"divisions": [[date, numérateur, dénominateur], …] triées, "n_dividendes": entier}.
     
      [rend: 1]
    ⑥ TRAITEMENT — Lire « splits » et « dividends » ; garder ceux dont la date de Paris est au plus COUPURE.
    ⑦ UNITÉ — Dates de Paris ; rapports sans unité ; un compte.
    ⑧ POURQUOI — Même forme que le fichier du 02-10-2026, lue par la réparation de l'historique long ; mesuré : ces
      réponses, coupées au 02-10, le redonnent à l'octet, ARCELORMITTAL comprise.
    ⑨ CE QUI CLOCHE — Les montants des dividendes ne sont pas gardés : 109 ont changé chez Yahoo entre le 08-10 et le
      21-10-2026 (rapport N2) ; le fichier n'en garde que le nombre. · Aucun événement de ces réponses ne tombe le jour
      de la coupure : que la borne soit incluse n'est pas éprouvé sur les vraies données.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; une réponse mal formée lève une erreur.
      [sort: non]
    """
    ev = json.loads(octets.decode("utf-8"))["chart"]["result"][0].get("events", {})
    div = sorted([date_de_paris(t), float(x["numerator"]), float(x["denominator"])]
                 for t, x in ev.get("splits", {}).items() if date_de_paris(t) <= COUPURE)
    n = sum(1 for t in ev.get("dividends", {}) if date_de_paris(t) <= COUPURE)
    return {"divisions": div, "n_dividendes": n}


def fabriquer(racine):
    """Rend les octets des deux fichiers, sans rien écrire.

    ① RÔLE — Assembler le fichier propre et le relevé des événements.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Celles de `lire_les_sources`.
    ⑤ SORTIE — DEUX valeurs : les octets du CSV du fichier propre, les octets du JSON des événements.
      [rend: 2]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥ : CSV à fins de ligne « \\r\\n » et en-tête ENTETE ; JSON indenté d'un
      espace, accents gardés, sans fin de ligne finale — la forme du fichier du 02-10-2026.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Séparer le calcul de l'écriture, pour que l'écriture soit d'un seul geste.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les sources.
    ⑪ TERMINAISON — Rend la main, ou propage le Refus ou la panne.
      [sort: non]
    """
    valeurs, reponses = lire_les_sources(racine)
    actions = {s for _, s in valeurs if est_une_action(reponses[s])}
    lignes = []
    for v, s in valeurs:
        if s in actions:
            lignes += barres(v, reponses[s])
    lignes.sort()
    tampon = io.StringIO()
    w = csv.writer(tampon, lineterminator="\r\n")
    w.writerow(ENTETE)
    w.writerows(lignes)
    ordre = sorted(v for v, s in valeurs if s in actions) + sorted(v for v, s in valeurs if s not in actions)
    symbole = dict(valeurs)
    ev = {v: evenements(reponses[symbole[v]]) for v in ordre}
    return tampon.getvalue().encode("utf-8"), json.dumps(ev, indent=1, ensure_ascii=False).encode("utf-8")


def sortie_refusee(racine, sortie):
    """Rend la raison de refuser le dossier de sortie, ou une chaîne vide.

    ① RÔLE — Empêcher d'écrire dans un dépôt : verser est un geste à part.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine`, `sortie` : deux chemins absolus.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un texte, vide si la sortie est acceptée.
      [rend: 1]
    ⑥ TRAITEMENT — Refuser si la sortie existe déjà, ou si elle est sous la racine donnée
      ou sous le dépôt qui porte ce programme (comparaison par os.path.commonpath, chemins résolus).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une propriété (« sous un dépôt »), pas un nom de dossier épelé : le relecteur du
      22-10-2026 a écrit `donnees/yahoo_ohlcv_propre.csv` à côté de l'original, deux fichiers de même nom.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s = os.path.realpath(sortie)
    depot_du_programme = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if os.path.exists(s):
        return "le dossier de sortie existe déjà"
    for d in (os.path.realpath(racine), depot_du_programme):
        if os.path.commonpath([s, d]) == d:
            return f"la sortie est sous un dépôt ({d}) : verser est un geste à part"
    return ""


def main(argv):
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la racine et le
    dossier de sortie.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Vérifier les arguments, les sources et la sortie ; fabriquer ; écrire dans un dossier provisoire
    voisin, puis le renommer d'un seul geste ; afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée le dossier de sortie.
    ⑪ TERMINAISON — Rend la main ; toute erreur est
    attrapée et rend 1 (Refus) ou 2 (le reste).
      [sort: non]
    """
    if len(argv) != 2:
        print("IMPOSSIBLE : usage — FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py <racine du dépôt> <dossier de sortie>")
        return 2
    racine, sortie = (os.path.abspath(a) for a in argv)
    for p in (REFERENTIEL, BRUTS, CARNET):
        if not os.path.exists(os.path.join(racine, p)):
            print(f"IMPOSSIBLE : source absente — {p}")
            return 2
    raison = sortie_refusee(racine, sortie)
    if raison:
        print(f"IMPOSSIBLE : {raison}")
        return 2
    try:
        propre, ev = fabriquer(racine)
    except Refus as e:
        print(f"REFUSÉ : {e}")
        return 1
    except Exception as e:
        print(f"IMPOSSIBLE : {type(e).__name__} — {e}")
        return 2
    # Un dossier provisoire au nom NEUF, que le programme possède : en cas d'échec, il n'efface que ce qu'il a créé
    # (relecteur du 23-10-2026, I-N2 : un nom fixe effaçait un « .en_cours » qui existait déjà ; superviseur du même
    # jour : de fond). Un parent absent fait échouer mkdtemp : code 2, rien de créé.
    provisoire = None
    try:
        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + ".en_cours.", dir=os.path.dirname(sortie))
        for nom, octets in (("yahoo_ohlcv_propre.csv", propre), ("evenements.json", ev)):
            with open(os.path.join(provisoire, nom), "wb") as f:
                f.write(octets)
        os.rename(provisoire, sortie)
    except Exception as e:
        if provisoire is not None:
            shutil.rmtree(provisoire, ignore_errors=True)
        print(f"IMPOSSIBLE : écriture — {type(e).__name__} — {e}")
        return 2
    n_lignes = propre.count(b"\n") - 1
    print(f"écrit : yahoo_ohlcv_propre.csv · {n_lignes} lignes · "
          f"sha256 {hashlib.sha256(propre).hexdigest()}")
    print(f"écrit : evenements.json · {len(json.loads(ev))} entrées · sha256 {hashlib.sha256(ev).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
