#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FABRIQUER_LA_TABLE_DES_DIVIDENDES.py — Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Fabriquer, depuis des sources figées du dépôt, la table des dividendes que lira la simulation des opérations
  (R-113 : « le jour du détachement, le stop et l'objectif baissent du montant du dividende, et le dividende s'ajoute,
  brut, au gain du trade »). Pour chaque dividende déclaré par une source, la table dit : la date de détachement
  donnée par la source, TELLE QUELLE ; le montant tel que la source l'écrit ; la clôture de la veille dans la MÊME
  source ; le RENDEMENT (montant ÷ cette clôture, sans unité) ; si ce rendement se calcule (statut) ; et le DERNIER
  JOUR QUE SA SOURCE COUVRE pour cette valeur (couverte_jusqu_au) : après ce jour, l'absence de ligne n'est pas « aucun
  dividende », c'est « on ne sait pas ». La table ne
  lit AUCUNE courbe de cours : `jouer` (lot J3) calcule le montant dans SA courbe, montant = rendement × clôture de la
  veille qu'il lit déjà. La confrontation à une courbe vit à part, dans
  programmes/CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py, qui signale et ne décide rien.
② CONTEXTE D'APPEL — Lancé à la main par le Chat, ou par son épreuve
  (tests/EPREUVES_DE_LA_TABLE_DES_DIVIDENDES_Jeu_05-11-2026.py). Aucune tâche du soir ne l'appelle. Commande :
  python3 programmes/FABRIQUER_LA_TABLE_DES_DIVIDENDES.py <racine> <fichier de sortie> --releve=<nom>
  <nom> est l'une des clés de RELEVES. Le réglage n'a PAS de valeur par défaut : le choix appartient à Jean-Luc
  (question Q-DIV1).
③ ENTRÉE — Sous la racine : le référentiel des valeurs, les réponses brutes de Yahoo du 21-10-2026 (chacune vérifiée au
  carnet de provenance par `FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.lire_les_sources`), le relevé des montants choisi,
  les distributions décidées à la main (DECIDEES), l'extrait de Paris bnains sans ses barres prouvées fausses
  (`CONTROLER_L_HISTORIQUE_LONG.lire_paris`) et le calendrier des séances (`CALENDRIER_DE_LA_BOURSE.lire_les_seances`).
  Le programme ne télécharge rien.
④ CONDITIONS D'ENTRÉE — Chaque fichier source (relevé, distributions décidées) est inscrit UNE fois au carnet avec
  l'empreinte qu'il a ; le fichier de sortie n'existe pas et son dossier existe. Chaque dividende, toutes sources
  confondues, a une date écrite AAAA-MM-JJ qui est une séance du calendrier, un montant fini et strictement positif,
  et aucun autre dividende de la même valeur n'a la même date (`controler_les_dividendes`) — sinon REFUS.
⑤ SORTIE — Le code de sortie, UNE valeur : 0 si la table est écrite ; 1 « REFUSÉ » si une source n'est pas celle du
  carnet, si une valeur ou une unité n'est pas connue, ou si un dividende est mal formé ou en double ; 2 « IMPOSSIBLE »
  si le programme n'a pas pu tourner (arguments, fichier absent ou illisible, sortie déjà présente). Hors du code 0,
  aucun fichier n'est écrit. À l'écran : le nombre de lignes, l'empreinte de la table, le compte par statut.
  [rend: 1]
⑥ TRAITEMENT — ① lire et vérifier les sources · ② refuser tout dividende mal formé ou en double · ③ pour chaque
  dividende : la veille est la séance du calendrier qui précède la date de la source ; la clôture de la veille se lit
  dans la MÊME source ; rendement = montant ÷ cette clôture ; couverte_jusqu_au = le dernier jour de la source pour
  cette valeur · ④ écrire la table triée dans un fichier provisoire, puis le renommer d'un seul geste. Le calendrier
  est celui de R-110 (`CAL.seances_entre`) : l'indice dans le passé, la liste d'Euronext au-delà de son dernier jour
  (02-10-2026) ; la table prend TOUT ce que dit sa source, sans coupure empruntée à un autre fichier.
⑦ UNITÉ — Dates de Paris (AAAA-MM-JJ) ; montant_source et cloture_source_veille dans l'unité de leur source (UNITES) ;
  rendement sans unité (fraction) ; couverte_jusqu_au, date de Paris.
⑧ POURQUOI — DÉCISION DE JEAN-LUC du 05-11-2026 à 14h22, « 1 », à la question Q-DIV5 du superviseur R-759 du même jour
  (« La date du dividende : celle de Yahoo, ou une date "corrigée" par le programme ? ») : la date et le montant des
  dividendes sont pris chez Yahoo TELS QUELS ; un écart avec la baisse du cours est SIGNALÉ (par le programme de
  confrontation), jamais corrigé automatiquement. Cette décision REMPLACE la correction de date de sa décision n°35
  (31-10-2026 à 18h49, « 1 » : « la date de détachement corrigée par programme (le jour où le cours baisse
  vraiment) »). RAISON : n°35 s'appuyait sur une mesure du 28-10-2026 (« Yahoo donne la veille 378 fois sur 1 237 ») ;
  le superviseur a mesuré le contraire le 05-11-2026 — sur les 50 détachements à date officielle connue (témoin ABC
  Bourse, temoins/TEMOIN_ABC_DIVIDENDES_CAC40_Jeu_08-10-2026_19h31.csv, d'octobre 2025 à septembre 2026), Yahoo
  donne la date officielle 50 fois sur 50, et la correction automatique en déplaçait 4 au mauvais jour (LVMH
  02-12-2025, Hermès 21-04-2026, Schneider 11-05-2026, Kering 02-06-2026) ; sur vingt ans, la séance qui suit la date
  de Yahoo ne baisse pas en moyenne. Une date fausse fait exactement le dommage que R-113 veut éviter : le stop
  baisserait un jour trop tard, et la baisse due au dividende pourrait faire vendre la position. LIMITE : aucune date
  officielle n'est au dépôt pour les années d'avant octobre 2025 ; leur justesse repose sur la mesure moyenne du
  superviseur, qui n'exclut pas quelques décalages isolés. — Le RENDEMENT, calculé dans une seule source, ne dépend
  d'aucun ajustement de cours (superviseur R-759 du 05-11-2026 : ne jamais mélanger des montants ajustés et des cours
  bruts ; exemple mesuré : Air Liquide, 3,3636 chez Yahoo pour 3,70 € chez ABC, après une attribution d'actions
  gratuites) : c'est lui qui voyage d'une courbe à l'autre, si bien qu'une seule table sert à toutes les courbes.
  — La COUVERTURE (superviseur R-759 du 05-11-2026, avant le tour 3, T1) : au tour 2, la table lisait les dividendes
  jusqu'à la coupure du cours propre de Yahoo (02-10-2026), une limite qui n'était pas la sienne ; trois dividendes
  de la réponse du 21-10 manquaient en silence (Société Générale 05-10-2026, Crédit Agricole et Vinci 13-10-2026),
  alors que la courbe du juge va jusqu'au 04-11-2026. Une absence doit être DITE : la table prend tout jusqu'à la fin
  de sa source et écrit ce dernier jour dans une colonne, que lisent la confrontation et, demain, `jouer` (J3).
  Décision n°89 du 01-11-2026 à 12h42 (« 1 ») : la distribution de 20 € d'Unibail du 07-10-2010 est inscrite comme
  un dividende. R-728 : la table ne s'écrit jamais à la main.
⑨ CE QUI CLOCHE — Avant 2009, les cours de la courbe des vingt ans ne baissent en moyenne que d'environ la moitié des
  dividendes de Yahoo, et 24 paires de dividendes d'une même valeur sont à 10 jours ou moins (aucune après 2009) :
  la source ou la courbe a tort, on ne sait pas laquelle (question Q-DIV6) ; ce programme ne le voit pas, la
  confrontation le montre. · Le montant d'Unibail 2010 n'a pas de document officiel au dépôt. · Le relevé
  EVENEMENTS_YAHOO (08-10) n'est pas inscrit au carnet : le choisir est refusé tant qu'il ne l'est pas. · Une valeur
  absente de Yahoo n'a aucun dividende (Unibail avant le 14-04-2023, valeurs sorties de l'indice) : rien ne le dit
  ligne par ligne. · La couverture d'une valeur se lit sur SES lignes : une valeur sans aucune ligne n'a pas de
  couverture écrite (mesuré le 05-11-2026 : chacune des 40 réponses porte au moins un dividende). · Du 22-10-2026 à
  aujourd'hui, aucune source n'est au dépôt (BACKLOG A-555, les dividendes à venir) : la colonne le dit, elle ne le
  comble pas.
⑩ EFFET — Écrit UN fichier, le fichier de sortie. Ne touche à aucun autre fichier.
⑪ TERMINAISON — Rend la main ; aucun appel réseau, aucune attente.
  [sort: oui]
"""
import bisect
import csv
import datetime
import hashlib
import json
import math
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import COLONNES_DES_SOURCES_A_LA_MAIN, ECRIT_A_LA_MAIN  # noqa: E402
import FABRIQUER_LE_COURS_PROPRE_DE_YAHOO as YP  # noqa: E402  la lecture vérifiée des réponses de Yahoo (R-708)
import CONTROLER_L_HISTORIQUE_LONG as HL  # noqa: E402  le seul Paris (bnains sans ses barres fausses)
import CALENDRIER_DE_LA_BOURSE as CAL  # noqa: E402  les séances, lues dans un calendrier (R-110)

# Les colonnes de la table et des distributions décidées. À DÉPLACER dans programmes/CONTRATS_DES_FICHIERS.py par le lot C,
# seul écrivain de ce fichier (superviseur R-759 du 05-11-2026, §3) : fragment remis dans le RAPPORT du lot DIV.
TABLE_DES_DIVIDENDES = [
    "valeur", "mnemonique", "source", "date_detachement", "montant_source", "unite_source", "cloture_source_veille",
    "rendement", "statut", "couverte_jusqu_au",
]
DISTRIBUTIONS_DECIDEES = ["valeur", "date", "montant", "unite"] + list(COLONNES_DES_SOURCES_A_LA_MAIN)

DECIDEES = os.path.join("donnees", "sources_dividendes", "DISTRIBUTIONS_DECIDEES.csv")
EVENEMENTS = os.path.join("donnees", "sources_yahoo", "EVENEMENTS_YAHOO.csv")
# Les relevés de montants que Jean-Luc peut choisir (question Q-DIV1). Chacun : le fichier lu en plus des réponses
# brutes (None : les réponses elles-mêmes), et le nom écrit dans la colonne `source`.
RELEVES = {
    "bruts_yahoo_21-10-2026": (None, "yahoo du 21-10-2026"),
    "evenements_yahoo_08-10-2026": (EVENEMENTS, "yahoo du 08-10-2026"),
}
SOURCE_DECIDEE = "décision écrite à la main"
# L'unité du montant de chaque source. Yahoo : ses montants suivent ses propres ajustements de cours (divisions) ;
# une distribution décidée : l'euro versé ce jour-là, à rapporter au cours brut de Paris.
UNITE_YAHOO, UNITE_DU_JOUR = "euro de Yahoo, ajusté par Yahoo", "euro du jour"
# Le statut ne dit que ce que dit la source : le rendement se calcule (MONTANT CONNU), ou la source n'a pas de clôture
# à la veille et le montant dans une courbe ne se calcule pas (MONTANT INCONNU, rendement vide, jamais zéro).
STATUTS = ("MONTANT CONNU", "MONTANT INCONNU")
DATE_ECRITE = re.compile(r"\d{4}-\d{2}-\d{2}")  # la forme AAAA-MM-JJ, entière (fullmatch)


class Refus(Exception):
    """Un refus voulu : une source n'est pas celle du carnet, une valeur ou une unité est inconnue, un dividende est
    mal formé ou en double.

    ① RÔLE — Distinguer un refus décidé (code 1) d'une panne (code 2).
    ② CONTEXTE D'APPEL — Levée par `verifier_au_carnet`, `lire_les_dividendes`, `lire_les_decidees`,
      `controler_les_dividendes` ; attrapée par `main`.
    ③ ENTRÉE — Le texte du refus.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Même distinction que FABRIQUER_LE_COURS_PROPRE_DE_YAHOO (superviseur R-759 du 22-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
      [sort: non]
    """


def verifier_au_carnet(racine, chemin, sortes):
    """Rend les octets d'un fichier source, après avoir vérifié son inscription au carnet de provenance.

    ① RÔLE — Une seule propriété pour toute source lue : « exactement une ligne au carnet, à son empreinte ».
    ② CONTEXTE D'APPEL — `lire_les_dividendes` (relevé EVENEMENTS) et `lire_les_decidees`.
    ③ ENTRÉE — `racine` : la racine du dépôt · `chemin` : le fichier, relatif à la racine · `sortes` : les valeurs de
      `produit_par` admises (exemple : (ECRIT_A_LA_MAIN,)), ou None pour toute sorte.
    ④ CONDITIONS D'ENTRÉE — Le carnet existe.
    ⑤ SORTIE — UNE valeur : les octets du fichier.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le fichier ; chercher au carnet les lignes de ce chemin ; il en faut une ; sa sorte doit être
      admise ; son empreinte doit être celle du fichier.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026 : « lire le fichier figé, avec son empreinte ». Même propriété que
      `YP.lire_les_sources`, étendue aux autres sources (une source changée sans le carnet est refusée).
    ⑨ CE QUI CLOCHE — L'empreinte dit qu'on lit le fichier inscrit, pas que son contenu est juste.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève Refus, ou OSError si le fichier manque.
      [sort: non]
    """
    p = os.path.join(racine, chemin)
    if not os.path.isfile(p):
        raise OSError(f"source absente : {chemin}")
    octets = open(p, "rb").read()
    with open(os.path.join(racine, YP.CARNET), encoding="utf-8", newline="") as f:
        lignes = [r for r in csv.DictReader(f) if r["fichier"] == chemin.replace(os.sep, "/")]
    if len(lignes) != 1:
        raise Refus(f"{chemin} : inscrit {len(lignes)} fois au carnet, au lieu d'une")
    if sortes is not None and lignes[0]["produit_par"] not in sortes:
        raise Refus(f"{chemin} : inscrit au carnet comme « {lignes[0]['produit_par']} », pas comme {sortes}")
    if hashlib.sha256(octets).hexdigest() != lignes[0]["sha256"]:
        raise Refus(f"{chemin} : empreinte différente de celle du carnet")
    return octets


def lire_les_dividendes(racine, releve):
    """Rend les dividendes du relevé choisi et les clôtures de Yahoo qui servent à les rapporter au cours.

    ① RÔLE — Donner, pour chaque dividende de Yahoo, sa date et son montant tels quels, et la série de clôtures de la
      MÊME source.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt · `releve` : une clé de RELEVES.
    ④ CONDITIONS D'ENTRÉE — Les réponses brutes sont celles du carnet (`YP.lire_les_sources`).
    ⑤ SORTIE — DEUX valeurs : la liste des dividendes, chacun {valeur, mnemonique, source, date, montant, unite,
      couverte_jusqu_au} ; les clôtures de Yahoo, {mnémonique : {date : clôture}}.
      [rend: 2]
    ⑥ TRAITEMENT — Vérifier les réponses ; garder leurs barres propres (`YP.barres`, mêmes filtres que le cours propre,
      mais SANS sa coupure : `jusqu_au` None) ; selon le relevé, lire TOUS les dividendes des réponses (datés à Paris),
      couverts jusqu'à la date de Paris du dernier horodatage de la réponse de leur valeur, ou ceux du fichier
      EVENEMENTS, vérifié au carnet, couverts jusqu'à la date la plus récente que ce fichier porte.
    ⑦ UNITÉ — Montants et clôtures en euros de Yahoo, ajustés par Yahoo de la même façon dans une même réponse.
    ⑧ POURQUOI — Le rendement n'a de sens que si montant et clôture viennent de la même source (superviseur R-759 du
      05-11-2026 : ne pas mélanger montants ajustés et bruts).
    ⑨ CE QUI CLOCHE — Avec le relevé du 08-10, montants (08-10) et clôtures (21-10) ne viennent pas du même
      téléchargement : 109 montants diffèrent entre les deux (mesuré le 05-11-2026, sortie du lot DIV) ; sa couverture
      (la date la plus récente du fichier) est une borne basse, le jour du téléchargement n'y étant pas écrit. · Le
      dernier horodatage d'une réponse du 21-10 tombe le 21-10-2026 : si elle a été prise pendant la séance, un
      dividende détaché ce jour-là y est quand même (la date est connue d'avance), mais rien au dépôt ne le prouve.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève Refus (source, valeur ou relevé inconnus, montant illisible ; le refus du
      lecteur de Yahoo est relevé sous ce nom, sinon `main` le prenait pour une panne — trouvé par l'épreuve E2 le
      05-11-2026) ; une panne de lecture se propage.
      [sort: non]
    """
    if releve not in RELEVES:
        raise Refus(f"relevé inconnu : {releve!r} (connus : {sorted(RELEVES)})")
    fichier, nom = RELEVES[releve]
    try:
        valeurs, reponses = YP.lire_les_sources(racine)
    except YP.Refus as e:  # un refus du lecteur de Yahoo reste un refus (code 1), jamais une panne (code 2)
        raise Refus(str(e)) from e
    nom_de = {s: v for v, s in valeurs}
    clotures = {}
    for v, s in valeurs:
        clotures[s[:-3]] = {b[1]: float(b[5]) for b in YP.barres(v, reponses[s], None)}
    divs = []
    if fichier is None:
        for v, s in valeurs:
            r = json.loads(reponses[s].decode("utf-8"))["chart"]["result"][0]
            fin = YP.date_de_paris(max(r["timestamp"]))
            for t, x in r.get("events", {}).get("dividends", {}).items():
                d = YP.date_de_paris(t)
                divs.append({"valeur": v, "mnemonique": s[:-3], "source": nom, "date": d,
                             "montant": _montant(x["amount"], f"{s} {d}"), "unite": UNITE_YAHOO, "couverte_jusqu_au": fin})
    else:
        octets = verifier_au_carnet(racine, fichier, None)
        lues = list(csv.DictReader(octets.decode("utf-8-sig").splitlines()))
        fin = max(r["date"] for r in lues)
        for r in lues:
            if r["type"] != "dividende":
                continue
            if r["symbole"] not in nom_de:
                raise Refus(f"{fichier} : symbole inconnu du référentiel : {r['symbole']}")
            divs.append({"valeur": nom_de[r["symbole"]], "mnemonique": r["symbole"][:-3], "source": nom,
                         "date": r["date"], "montant": _montant(r["montant_ou_rapport"], f"{r['symbole']} {r['date']}"),
                         "unite": UNITE_YAHOO, "couverte_jusqu_au": fin})
    return divs, clotures


def _montant(texte, ou):
    """Lit un montant ; un texte illisible est un refus, jamais une panne.

    ① RÔLE — Une seule lecture des montants de toutes les sources.
    ② CONTEXTE D'APPEL — `lire_les_dividendes`, `lire_les_decidees`, une fois par dividende.
    ③ ENTRÉE — `texte` : le montant tel que la source l'écrit (texte ou nombre) · `ou` : de quoi il s'agit, pour le
      message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre (float).
      [rend: 1]
    ⑥ TRAITEMENT — float() ; une erreur devient Refus. Le signe et la finitude se contrôlent dans
      `controler_les_dividendes`, pour toutes les sources à la fois.
    ⑦ UNITÉ — Celle de la source.
    ⑧ POURQUOI — Relecture du 05-11-2026 (D5) : une ligne décidée mal écrite passait en silence ; illisible, elle
      sortait en panne (code 2) au lieu d'un refus (code 1).
    ⑨ CE QUI CLOCHE — « 1,5 » (virgule) est refusé : c'est voulu, la forme du fichier est le point.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève Refus.
      [sort: non]
    """
    try:
        return float(texte)
    except (TypeError, ValueError):
        raise Refus(f"{ou} : montant illisible « {texte} »") from None


def lire_les_decidees(racine):
    """Rend les distributions décidées à la main, et les clôtures brutes de Paris qui servent à les rapporter au cours.

    ① RÔLE — Ajouter à la table ce qu'aucune source téléchargée ne porte et que Jean-Luc a décidé (n°89 : Unibail 2010).
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — DECIDEES est inscrit au carnet comme écrit à la main, à son empreinte ; son en-tête est
      DISTRIBUTIONS_DECIDEES ; chaque ligne a une citation et au moins une adresse ou un fichier cité.
    ⑤ SORTIE — DEUX valeurs : la liste des distributions, même forme que `lire_les_dividendes` (une distribution
      décidée ne couvre que son propre jour : couverte_jusqu_au = sa date) ; les clôtures brutes de Paris,
      {mnémonique : {date : clôture}}.
      [rend: 2]
    ⑥ TRAITEMENT — Vérifier au carnet ; lire les lignes ; refuser une valeur absente du référentiel, une unité autre que
      UNITE_DU_JOUR, un montant illisible ; lire Paris sans ses barres fausses (`HL.lire_paris`). La date et le signe du
      montant se contrôlent avec ceux de toutes les sources (`controler_les_dividendes`).
    ⑦ UNITÉ — Montants en euros du jour ; clôtures en euros bruts de Paris.
    ⑧ POURQUOI — Un montant versé un jour se rapporte au cours brut de ce jour-là ; bnains est le cours brut de Paris
      jusqu'au 28-02-2017 (donnees/LISEZ_MOI_LES_COURS.md, « les mots »).
    ⑨ CE QUI CLOCHE — Après le 28-02-2017, aucune clôture brute de Paris n'est lue : une distribution décidée d'après
      cette date aurait un rendement INCONNU (dit, jamais nul).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève Refus ; une panne de lecture se propage.
      [sort: non]
    """
    octets = verifier_au_carnet(racine, DECIDEES, (ECRIT_A_LA_MAIN,))
    with open(os.path.join(racine, YP.REFERENTIEL), encoding="utf-8-sig", newline="") as f:
        mnemo = {r["nom_usuel"]: r["mnemonique"] for r in csv.DictReader(f)}
    lecteur = csv.DictReader(octets.decode("utf-8-sig").splitlines())
    if lecteur.fieldnames != DISTRIBUTIONS_DECIDEES:
        raise Refus(f"{DECIDEES} : en-tête {lecteur.fieldnames} au lieu de {DISTRIBUTIONS_DECIDEES}")
    out = []
    for r in lecteur:
        if r["valeur"] not in mnemo:
            raise Refus(f"{DECIDEES} : valeur inconnue du référentiel : {r['valeur']}")
        if r["unite"] != UNITE_DU_JOUR:
            raise Refus(f"{DECIDEES} : unité inconnue : {r['unite']!r} (seule « {UNITE_DU_JOUR} » est lue)")
        if not r["citation"] or not (r["source"] or r["fichiers_cites"]):
            raise Refus(f"{DECIDEES} : {r['valeur']} {r['date']} sans citation ou sans source")
        out.append({"valeur": r["valeur"], "mnemonique": mnemo[r["valeur"]], "source": SOURCE_DECIDEE,
                    "date": r["date"], "montant": _montant(r["montant"], f"{DECIDEES} : {r['valeur']} {r['date']}"),
                    "unite": UNITE_DU_JOUR, "couverte_jusqu_au": r["date"]})
    paris, _, _ = HL.lire_paris(racine)
    clotures = {mnemo[v]: {d: b[3] for d, b in barres.items()} for v, barres in paris.items() if v in mnemo}
    return out, clotures


def controler_les_dividendes(divs, seances):
    """Refuse tout dividende mal formé ou en double, toutes sources confondues.

    ① RÔLE — Une seule propriété pour chaque ligne qui entre dans la table, quelle que soit sa source.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois, avant tout calcul.
    ③ ENTRÉE — `divs` : la liste des dividendes ({valeur, mnemonique, source, date, montant, unite}) · `seances` : la
      liste triée des séances, AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien : lève, ou rend la main.
      [rend: rien]
    ⑥ TRAITEMENT — Pour chaque dividende : la date s'écrit AAAA-MM-JJ et se lit comme une date du calendrier civil ;
      elle est une séance ; le montant est un nombre fini strictement positif. Puis : aucune clé (mnémonique, date)
      n'est portée par deux dividendes. Toutes les fautes sont rassemblées en un seul refus.
    ⑦ UNITÉ — Dates ; montants dans l'unité de leur source (seul le signe compte ici).
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026 (D2, D5) : une date mal écrite (« 01/07/2009 ») donnait un
      détachement au 03-01-2000 en silence ; un montant négatif était accepté ; une distribution décidée qui doublait
      un dividende de Yahoo (Bureau Veritas 01-07-2025) aurait été créditée deux fois par R-113. Une date hors séance
      n'aurait aucune ouverture où le stop baisse : refusée plutôt que devinée (mesuré le 05-11-2026 : 0 date de
      Yahoo hors séance sur 1 345, 0 clé en double).
    ⑨ CE QUI CLOCHE — Deux dividendes d'une même valeur à quelques jours d'écart (24 paires avant 2009, dont Accor
      15-05-2008 et 20-05-2008, 3,15 € chacun) ne sont PAS refusés : aucune règle décidée ne dit à partir de combien
      de jours deux dividendes n'en font qu'un (question Q-DIV6, BACKLOG). Le refus arrête toute la table : une seule
      ligne fausse d'une source bloque les autres (le sens prudent).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève Refus.
      [sort: non]
    """
    fautes, vues = [], {}
    jours = set(seances)
    for x in divs:
        quoi = f"{x['valeur']} {x['date']} ({x['source']})"
        try:
            bonne = bool(DATE_ECRITE.fullmatch(x["date"])) and datetime.date.fromisoformat(x["date"]) is not None
        except ValueError:
            bonne = False
        if not bonne:
            fautes.append(f"{quoi} : date mal écrite (AAAA-MM-JJ attendu)")
        elif x["date"] not in jours:
            fautes.append(f"{quoi} : la date n'est pas une séance du calendrier")
        if not (math.isfinite(x["montant"]) and x["montant"] > 0):
            fautes.append(f"{quoi} : montant {x['montant']!r} (un nombre fini strictement positif attendu)")
        vues.setdefault((x["mnemonique"], x["date"]), []).append(x["source"])
    for (s, d), sources in sorted(vues.items()):
        if len(sources) > 1:
            fautes.append(f"{s} {d} : {len(sources)} dividendes à la même date ({sources}) — un seul détachement par "
                          "valeur et par séance")
    if fautes:
        raise Refus(f"{len(fautes)} dividende(s) refusé(s) : " + " | ".join(fautes[:20]))


def _nombre(x, chiffres):
    """Écrit un nombre avec un nombre fixe de décimales, ou rien s'il est inconnu.

    ① RÔLE — Une seule écriture des nombres de la table, pour qu'elle se refasse à l'octet.
    ② CONTEXTE D'APPEL — `fabriquer`.
    ③ ENTRÉE — `x` : nombre ou None · `chiffres` : décimales.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un texte, vide pour None.
      [rend: 1]
    ⑥ TRAITEMENT — Format fixe.
    ⑦ UNITÉ — Celle de `x`.
    ⑧ POURQUOI — Une valeur inconnue est DITE vide, jamais écrite 0 (consigne du lot DIV).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return "" if x is None else f"{x:.{chiffres}f}"


def fichiers_lus(racine, releve):
    """Rend la liste des fichiers que lit une fabrication, pour la colonne `lu` du carnet de provenance.

    ① RÔLE — Dire, au carnet, de quoi la table est faite, sans l'écrire à la main.
    ② CONTEXTE D'APPEL — L'épreuve, et l'inscription de la table au carnet.
    ③ ENTRÉE — `racine` · `releve` : une clé de RELEVES.
    ④ CONDITIONS D'ENTRÉE — `releve` est connu.
    ⑤ SORTIE — UNE valeur : la liste triée des chemins, séparateur « / ».
      [rend: 1]
    ⑥ TRAITEMENT — Les fichiers ouverts par `fabriquer` et par les lecteurs qu'il appelle, sauf le carnet lui-même :
      il est le registre qui contrôle les sources, pas une source (même usage que la ligne du cours propre de Yahoo,
      dont la colonne `lu` ne le nomme pas ; le nommer ferait demander à K23 l'inscription du carnet dans le carnet).
    ⑦ UNITÉ — Des chemins.
    ⑧ POURQUOI — Règle du carnet (n°54) : un fichier produit par programme nomme ce qu'il a lu.
    ⑨ CE QUI CLOCHE — La liste est tenue à côté du code qui lit : un lecteur ajouté sans elle ne serait pas dit ;
      l'épreuve compare la liste aux fichiers que le programme ouvre réellement.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lus = {YP.REFERENTIEL, DECIDEES, CAL.INDICE, CAL.FICHIER,
           os.path.join("donnees", "sources_bnains", "bnains_cac40.csv"),
           os.path.join("donnees", "sources_bnains", "BARRES_BNAINS_FAUSSES.csv")}
    with open(os.path.join(racine, YP.REFERENTIEL), encoding="utf-8-sig", newline="") as f:
        lus |= {os.path.join(YP.BRUTS, r["mnemonique"] + ".PA.json") for r in csv.DictReader(f)}
    if RELEVES[releve][0]:
        lus.add(RELEVES[releve][0])
    return sorted(p.replace(os.sep, "/") for p in lus)


def fabriquer(racine, releve):
    """Rend les lignes de la table des dividendes.

    ① RÔLE — Le calcul entier de la table, sans écriture.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `racine` · `releve` : une clé de RELEVES.
    ④ CONDITIONS D'ENTRÉE — Celles de `lire_les_dividendes`, `lire_les_decidees` et `controler_les_dividendes`.
    ⑤ SORTIE — UNE valeur : les lignes (listes de textes, dans l'ordre de TABLE_DES_DIVIDENDES), triées par valeur,
      date puis source.
      [rend: 1]
    ⑥ TRAITEMENT — Les séances de R-110 (`CAL.seances_entre`, constatées par l'indice puis prévues par Euronext),
      du premier jour de l'indice au plus tard des jours couverts ; contrôler les dividendes ; pour chacun : la veille,
      séance du calendrier qui précède sa date ; la clôture de la veille dans sa source ; le rendement ; le statut ; la
      couverture de sa source.
    ⑦ UNITÉ — Voir la fiche en tête, ⑦.
    ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Jusqu'au 02-10-2026, les séances sont celles où l'indice est publié : une valeur cotée un jour
      sans indice ne compte pas ; au-delà, elles sont PRÉVUES par la liste d'Euronext, sans constat (R-110 ③). · Un
      jour couvert au-delà du 31-12-2026 (fin de la liste d'Euronext) arrête le calendrier à cette date : un dividende
      d'après est refusé comme hors séance. ·
      Une clôture de la source absente à la veille (barre écartée par les filtres du cours propre, ou valeur
      sans cours ce jour-là chez Yahoo) rend le rendement INCONNU, sans chercher une autre veille.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève Refus ou une erreur de lecture.
      [sort: non]
    """
    divs, clot_y = lire_les_dividendes(racine, releve)
    decidees, clot_p = lire_les_decidees(racine)
    sc = CAL.lire_les_seances(racine)
    fin = sc["fin"]
    for x in divs + decidees:
        try:
            fin = max(fin, datetime.date.fromisoformat(x["couverte_jusqu_au"]))
        except ValueError:
            pass  # une date mal écrite est refusée par `controler_les_dividendes`, avec les autres fautes
    fin = min(fin, sc["euronext"]["jusqu_au"])  # au-delà, aucun calendrier : la date sera refusée, jamais devinée
    seances = [d.isoformat() for d, _ in CAL.seances_entre(sc["debut"], fin, sc)]
    controler_les_dividendes(divs + decidees, seances)
    lignes = []
    for x in divs + decidees:
        clot_src = clot_y if x["unite"] == UNITE_YAHOO else clot_p
        i = bisect.bisect_left(seances, x["date"])
        veille = seances[i - 1] if i > 0 else None
        cs = clot_src.get(x["mnemonique"], {}).get(veille)
        rendement = x["montant"] / cs if cs else None
        statut = STATUTS[0] if rendement is not None else STATUTS[1]
        lignes.append([x["valeur"], x["mnemonique"], x["source"], x["date"], repr(x["montant"]), x["unite"],
                       _nombre(cs, 6), _nombre(rendement, 10), statut, x["couverte_jusqu_au"]])
    lignes.sort(key=lambda r: (r[0], r[3], r[2]))
    return lignes


def main(argv):
    """Fabrique la table et l'écrit d'un seul geste.

    ① RÔLE — Le point d'entrée en ligne de commande.
    ② CONTEXTE D'APPEL — La ligne de commande (fiche en tête, ②).
    ③ ENTRÉE — `argv` : <racine> <fichier de sortie> --releve=<nom>.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : le code 0, 1 ou 2 (fiche en tête, ⑤).
      [rend: 1]
    ⑥ TRAITEMENT — Lire les arguments ; `fabriquer` (un Refus rend 1, toute autre panne rend 2) ; écrire dans un
      fichier provisoire du même dossier puis le renommer ; afficher les comptes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un code 1 d'une erreur Python non attrapée passerait pour un refus.
    ⑨ CE QUI CLOCHE — Entre le contrôle « la sortie n'existe pas » et le renommage, un fichier créé au même nom par un
      autre processus serait remplacé (même cas d'école que FABRIQUER_LE_COURS_PROPRE_DE_YAHOO).
    ⑩ EFFET — Écrit le fichier de sortie, et lui seul.
    ⑪ TERMINAISON — Rend la main (c'est le bas du fichier qui sort, par sys.exit) ; aucun appel qui puisse ne pas revenir.
      [sort: non]
    """
    opts = [a for a in argv if a.startswith("--")]
    pos = [a for a in argv if not a.startswith("--")]
    releves = [a.split("=", 1)[1] for a in opts if a.startswith("--releve=")]
    if len(pos) != 2 or len(releves) != 1 or len(opts) != 1:
        print("IMPOSSIBLE : usage <racine> <fichier de sortie> --releve=<"
              + "|".join(sorted(RELEVES)) + "> (aucun relevé par défaut : question Q-DIV1)")
        return 2
    racine, sortie = pos
    if os.path.exists(sortie) or not os.path.isdir(os.path.dirname(os.path.abspath(sortie))):
        print(f"IMPOSSIBLE : la sortie existe déjà, ou son dossier manque : {sortie}")
        return 2
    try:
        lignes = fabriquer(racine, releves[0])
    except Refus as e:
        print(f"REFUSÉ : {e}")
        return 1
    except Exception as e:  # toute panne rend 2 : le code 1 d'une erreur Python non attrapée passerait pour un refus
        print(f"IMPOSSIBLE : {type(e).__name__} : {e}")
        return 2
    dossier = os.path.dirname(os.path.abspath(sortie))
    fd, provisoire = tempfile.mkstemp(dir=dossier, suffix=".provisoire")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(TABLE_DES_DIVIDENDES)
        w.writerows(lignes)
    os.replace(provisoire, sortie)
    octets = open(sortie, "rb").read()
    print(f"écrit : {sortie} · {len(lignes)} lignes · sha256 {hashlib.sha256(octets).hexdigest()}")
    print("statuts : " + " · ".join(f"{s} {sum(1 for r in lignes if r[8] == s)}" for s in STATUTS))
    print("Les écarts avec la baisse du cours se lisent par programmes/CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
