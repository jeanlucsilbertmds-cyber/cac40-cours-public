#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_TABLE_DES_DIVIDENDES — Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/FABRIQUER_LA_TABLE_DES_DIVIDENDES.py refait à l'octet la table déposée
  (donnees/TABLE_DES_DIVIDENDES.csv) depuis des sources figées ; qu'il refuse une source changée ; que chaque dividende
  de la source est dans la table, à SA date ; que chaque colonne que lira `jouer` (date, montant, clôture de la
  veille, rendement, statut) se RECALCULE par un chemin qui n'importe pas le programme ; qu'Unibail du 07-10-2010 y
  est, avec sa décision ; qu'une donnée absente est DITE et jamais écrite zéro ; que les dates sont celles du témoin
  officiel ABC ; que la table prend tout ce que dit sa source et écrit ce qu'elle couvre ; que la table est inscrite au carnet de provenance avec ce qu'elle lit ; que le relevé des montants
  n'a pas de valeur par défaut ; qu'un dividende mal formé ou en double est refusé ; que la confrontation à la courbe
  (programmes/CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py) mesure juste, compte juste, ne mesure pas à travers un trou,
  dit la partie de la courbe que la table ne couvre pas et n'écrit rien — et que chacune de
  ces épreuves rougit quand on retire ce qu'elle éprouve (--saboter).
② CONTEXTE D'APPEL — À la main, ou par une série de sabotages : python3 -B tests/EPREUVES_DE_LA_TABLE_DES_DIVIDENDES_
  Jeu_05-11-2026.py <racine> [--saboter | --cas=<un cas>]. Aucune tâche du soir ne l'appelle.
③ ENTRÉE — La racine d'un dépôt ; l'option --saboter ou --cas=.
④ CONDITIONS D'ENTRÉE — La racine porte les deux programmes, la table déposée et leurs sources.
⑤ SORTIE — Le code de sortie, UNE valeur : 0 si les cas E1–E12 sont justes (et, avec --saboter, si chaque sabotage fait
  tomber le cas qu'il vise) ; 1 si un cas est faux ou si un sabotage ne mord pas ; 2 si l'épreuve n'a pas pu juger
  (panne, sabotage qui ne s'applique plus). [rend: 1]
⑥ TRAITEMENT — Chaque cas est une fonction qui rend la liste de ses fautes (vide : juste). Avec --saboter : le dépôt est
  reflété dans un dossier jetable (liens symboliques, sauf les fichiers sabotés, copiés puis modifiés), et l'épreuve
  est relancée sur ce reflet dans un sous-processus ; le sabotage « mord » si le cas qu'il vise tombe avec la faute
  attendue.
⑦ UNITÉ — —
⑧ POURQUOI — Superviseur R-759 du 05-11-2026 (« ARRÊTER ET SIMPLIFIER », D1) : « chaque colonne que lit `jouer` est
  recalculée par l'épreuve depuis les sources figées, par un chemin qui n'importe pas le programme, sur la table
  déposée ET sur la table refaite ; un sabotage par colonne doit faire tomber un cas autre qu'E1 » — au tour 1, le
  sabotage R4 du relecteur (montant faux de 22 % sur Pernod Ricard 11-06-2002) laissait l'épreuve VERTE. Décision de
  Jean-Luc du 05-11-2026 à 14h22 (« 1 », Q-DIV5) : dates et montants de Yahoo tels quels. Règle commune aux lots de D :
  aucun argument à valeur par défaut. Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une
  preuve (instructions du projet, §7).
⑨ CE QUI CLOCHE — Le recalcul indépendant (E5) réécrit les filtres de barres du cours propre de Yahoo et lit un
  réglage de son module (DEBUT_STELLANTIS) ; il ne lit plus sa COUPURE depuis le tour 3 (superviseur R-759 du
  05-11-2026, T1) : une coupure remise dans le programme fait tomber E3 (sabotage S22). · Le reflet par liens symboliques suppose un système qui les accepte ; K23 refuse de lire à
  travers un lien, si bien qu'E8 tombe dans tout reflet (d'où la faute attendue, par sabotage). · Le témoin ABC (E7)
  ne couvre que d'octobre 2025 à septembre 2026.
⑩ EFFET — Écrit seulement dans des dossiers temporaires, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque sous-processus a un délai (DELAI_S).
  [sort: oui]
"""
import builtins
import csv
import datetime
import hashlib
import importlib.util
import inspect
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from contextlib import redirect_stdout
from zoneinfo import ZoneInfo

PROGRAMME = "programmes/FABRIQUER_LA_TABLE_DES_DIVIDENDES.py"
CONFRONTATION = "programmes/CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py"
TABLE = "donnees/TABLE_DES_DIVIDENDES.csv"
COURBE_DU_JUGE = "donnees/cours_maitre.csv"  # `fichiers_de_cours` de programmes/JUGE_DES_STRATEGIES.py (relu le 05-11-2026)
TEMOIN_ABC = "temoins/TEMOIN_ABC_DIVIDENDES_CAC40_Jeu_08-10-2026_19h31.csv"
DELAI_S = 600  # délai d'un sous-processus de sabotage : la fabrication dure ~10 s mesurées le 05-11-2026


def charger(racine, chemin, nom):
    """Charge un programme depuis la racine donnée.

    ① RÔLE — Éprouver le texte de CETTE racine (le dépôt, ou un reflet saboté).
    ② CONTEXTE D'APPEL — `jouer`, E5.
    ③ ENTRÉE — `racine` · `chemin` : le programme, relatif à la racine · `nom` : le nom du module.
    ④ CONDITIONS D'ENTRÉE — Le programme existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib par chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les programmes ajoutent eux-mêmes leur dossier aux imports : leurs voisins viennent de la même racine.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève l'erreur d'import.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, os.path.join(racine, chemin))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def lire_table(chemin):
    """Rend l'en-tête et les lignes d'une table.
    ① RÔLE — Lire la table déposée.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `chemin`.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs : l'en-tête, les lignes (dictionnaires).
    [rend: 2]
    ⑥ TRAITEMENT — csv.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — —.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def releve_de_la_table(m, lignes):
    """Rend la clé de RELEVES qu'a utilisée la table, lue dans la table elle-même.

    ① RÔLE — Refaire la table avec le réglage qu'elle déclare, sans le recopier ici (R-708).
    ② CONTEXTE D'APPEL — `jouer`, E1, E2, E3, E8, E9.
    ③ ENTRÉE — `m` : le module · `lignes` : la table.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : la clé, ou None si la table en mêle plusieurs ou aucune.
    [rend: 1]
    ⑥ TRAITEMENT — Les sources de Yahoo de la table, ramenées aux clés.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Une table qui mêlerait deux relevés est fausse par construction.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    noms = {r["source"] for r in lignes} - {m.SOURCE_DECIDEE}
    cles = [k for k, (_, n) in m.RELEVES.items() if n in noms]
    return cles[0] if len(cles) == 1 and len(noms) == 1 else None


def refleter(racine, banc, a_copier):
    """Reflète une racine dans `banc` par des liens symboliques, sauf les chemins à copier (vraies copies).

    ① RÔLE — Un dépôt jetable sans recopier ses centaines de méga-octets.
    ② CONTEXTE D'APPEL — E2, E11, `saboter`.
    ③ ENTRÉE — `racine` · `banc` : dossier à créer · `a_copier` : chemins relatifs.
    ④ CONDITIONS D'ENTRÉE — `banc`
    n'existe pas.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Pour chaque entrée : ancêtre d'un chemin à copier →
    dossier et récursion ; chemin à copier → copie ; sinon lien.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Garder 3 Go libres
    (consigne du lot).
    ⑨ CE QUI CLOCHE — Le programme lit à travers les liens : un programme qui écrirait dans la
    racine écrirait dans le vrai dépôt (les programmes n'écrivent que leur sortie ; E12 le vérifie pour la
    confrontation).
    ⑩ EFFET — Crée `banc`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def rec(src, dst, rel):
        """Reflète un dossier.
        ① RÔLE — Un niveau du reflet.
        ② CONTEXTE D'APPEL — `refleter`, puis elle-même.
        ③ ENTRÉE — `src` : dossier réel · `dst` : dossier à créer · `rel` : chemin relatif de `src` (vide à la racine).
        ④ CONDITIONS D'ENTRÉE — `dst` n'existe pas.
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — Voir `refleter`.
        ⑦ UNITÉ — —.
        ⑧ POURQUOI — —.
        ⑨ CE QUI CLOCHE — Un lien symbolique du dépôt serait reflété par un lien vers un
        lien.
        ⑩ EFFET — Crée `dst`.
        ⑪ TERMINAISON — Rend la main ; la récursion suit la profondeur des chemins à
        copier.
          [sort: non]
        """
        os.makedirs(dst)
        for e in sorted(os.listdir(src)):
            r = (rel + "/" + e) if rel else e
            s, d = os.path.join(src, e), os.path.join(dst, e)
            if r in a_copier:
                shutil.copy2(s, d)
            elif any(c.startswith(r + "/") for c in a_copier):
                rec(s, d, r)
            else:
                os.symlink(s, d)
    rec(os.path.abspath(racine), banc, "")


def inscrire_a_nouveau(banc, chemin):
    """Remet au carnet d'un reflet l'empreinte actuelle d'un fichier (pour qu'un sabotage passe le carnet).

    ① RÔLE — Simuler quelqu'un qui change une source ET son inscription.
    ② CONTEXTE D'APPEL — E2, E11, `saboter`.
    ③ ENTRÉE — `banc` (le carnet y est une vraie copie) · `chemin`.
    ④ CONDITIONS D'ENTRÉE — Une ligne au carnet.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Remplacer l'empreinte de la ligne.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Un montant changé avec son carnet doit encore faire rougir l'épreuve (superviseur, contrôle 2).
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Réécrit le carnet du reflet.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    p = os.path.join(banc, "donnees", "PROVENANCE_DES_FICHIERS.csv")
    with open(p, encoding="utf-8", newline="") as f:
        lignes = list(csv.reader(f))
    h = hashlib.sha256(open(os.path.join(banc, chemin), "rb").read()).hexdigest()
    for l in lignes[1:]:
        if l[0] == chemin:
            l[1] = h
    os.unlink(p)
    with open(p, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(lignes)


def cas_e1(racine, m, m2, entete, lignes, tmp):
    """E1 REFABRICATION À L'OCTET — la table refaite par `main` est la table déposée.

    ① RÔLE — Prouver que la table vient du programme (R-728).
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `racine`, `m` (le programme), `m2` (la confrontation), `entete`, `lignes` (la table), `tmp`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Lancer `main` avec le relevé que déclare la table ; comparer les octets.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur, contrôle 1.
    ⑨ CE QUI CLOCHE — Seul, E1 ne protège rien de ce que le programme calcule :
    une table refaite par un programme faux puis redéposée le passe (relecture du 05-11-2026, D1) ; d'où E5.
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    releve = releve_de_la_table(m, lignes)
    if releve is None:
        return ["la table ne déclare pas un relevé unique"]
    sortie = os.path.join(tmp, "refaite.csv")
    ecran = io.StringIO()
    with redirect_stdout(ecran):
        code = m.main([racine, sortie, "--releve=" + releve])
    if code != 0:
        return [f"main rend {code} : {ecran.getvalue()[-400:]}"]
    if open(sortie, "rb").read() != open(os.path.join(racine, TABLE), "rb").read():
        return ["la table refaite diffère de la table déposée"]
    return []


def cas_e2(racine, m, m2, entete, lignes, tmp):
    """E2 SOURCE CHANGÉE — un montant changé dans une source est refusé ; changé AVEC son carnet, il change la table.

    ① RÔLE — Superviseur, contrôle 2.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — La réponse de Yahoo de BUREAU VERITAS porte le dividende du 01-07-2025 (vraie ligne).
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Reflet où la réponse BVI.PA.json a le montant de son dividende du 01-07-2025 multiplié par deux :
      `lire_les_dividendes` doit lever Refus ; le montant d'Unibail 2010 doublé dans les distributions décidées :
      `lire_les_decidees` doit lever Refus (la garde propre au programme, `verifier_au_carnet`) ; puis, carnet remis à
      l'empreinte nouvelle, `fabriquer` doit rendre une ligne différente pour ce dividende.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — « Changer un montant d'une source fait rougir l'épreuve ».
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rel = "donnees/sources_yahoo/bruts_yahoo_21-10-2026/BVI.PA.json"
    banc = os.path.join(tmp, "e2")
    refleter(racine, banc, {rel, "donnees/PROVENANCE_DES_FICHIERS.csv", m.DECIDEES.replace(os.sep, "/")})
    p = os.path.join(banc, rel)
    d = json.load(open(p, encoding="utf-8"))
    divs = d["chart"]["result"][0]["events"]["dividends"]
    cible = [t for t in divs if datetime.datetime.fromtimestamp(int(t), ZoneInfo("Europe/Paris")).date().isoformat() == "2025-07-01"]
    if len(cible) != 1:
        return [f"la vraie ligne BVI du 01-07-2025 est trouvée {len(cible)} fois"]
    divs[cible[0]]["amount"] *= 2
    open(p, "w", encoding="utf-8").write(json.dumps(d))
    fautes = []
    try:
        m.lire_les_dividendes(banc, "bruts_yahoo_21-10-2026")
        fautes.append("une réponse changée sans son carnet n'est pas refusée")
    except m.Refus:
        pass
    dec = os.path.join(banc, m.DECIDEES)
    original = open(os.path.join(racine, m.DECIDEES), encoding="utf-8").read()
    os.unlink(dec)
    open(dec, "w", encoding="utf-8").write(original.replace(",2010-10-07,20,", ",2010-10-07,40,"))
    try:
        m.lire_les_decidees(banc)
        fautes.append("une distribution décidée changée sans son carnet n'est pas refusée")
    except m.Refus:
        pass
    open(dec, "w", encoding="utf-8").write(original)
    inscrire_a_nouveau(banc, rel)
    neuves = m.fabriquer(banc, "bruts_yahoo_21-10-2026")
    av = [r for r in lignes if r["mnemonique"] == "BVI" and r["date_detachement"] == "2025-07-01"]
    ap = [r for r in neuves if r[1] == "BVI" and r[3] == "2025-07-01"]
    if len(av) != 1 or len(ap) != 1 or [av[0][k] for k in entete] == ap[0]:
        fautes.append("un montant changé avec son carnet ne change pas la ligne de la table")
    return fautes


def norme(nom):
    """Rend un nom de valeur sans accents, sans espaces ni signes, en majuscules.

    ① RÔLE — Rapprocher des écritures différentes d'un même nom (« CREDIT_AGRICOLE_SA », « Crédit Agricole SA »).
    ② CONTEXTE D'APPEL — `sources_independantes`, E7.
    ③ ENTRÉE — `nom`.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : le texte normé.
      [rend: 1]
    ⑥ TRAITEMENT — NFKD, ASCII, lettres et chiffres.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Propriété plutôt que table de correspondance.
    ⑨ CE QUI CLOCHE — Deux valeurs dont les
    noms ne diffèrent que par la ponctuation se confondraient (aucune au référentiel le 05-11-2026).
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return "".join(c for c in unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode().upper() if c.isalnum())


def seances_independantes(racine, jusqu_au):
    """Rend les séances, relues SANS le calendrier du dépôt : l'indice, puis les jours ouvrés qu'Euronext n'a pas fermés.

    ① RÔLE — Le calendrier de R-110 refait à part, pour E5 et E12.
    ② CONTEXTE D'APPEL — `sources_independantes` (jusqu'à la fin des réponses de Yahoo) ; E12 (jusqu'à la fin de la
      courbe du juge).
    ③ ENTRÉE — `racine` · `jusqu_au` : la dernière date voulue, AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — L'indice et donnees/CALENDRIER_EURONEXT.csv sont au dépôt.
    ⑤ SORTIE — UNE valeur : la liste triée des séances, AAAA-MM-JJ.
      [rend: 1]
    ⑥ TRAITEMENT — Les dates de l'indice (csv) ; puis, du lendemain de sa dernière date à `jusqu_au` et au plus la date
      COUVERT_JUSQU_AU de la liste d'Euronext : chaque lundi-vendredi qu'elle ne déclare pas FERME.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026, avant le tour 3 (T1) : la table prend tout jusqu'à la fin de sa
      source (21-10-2026), au-delà du dernier jour de l'indice (02-10-2026) ; un recalcul limité à l'indice ne verrait
      pas les trois dividendes d'octobre.
    ⑨ CE QUI CLOCHE — Les demi-séances comptent comme des séances, comme dans le calendrier du dépôt.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; une boucle bornée par `jusqu_au`.
      [sort: non]
    """
    with open(os.path.join(racine, "donnees/sources_indice/INDICE_CAC40.csv"), encoding="utf-8-sig", newline="") as f:
        seances = sorted(r["date"] for r in csv.DictReader(f))
    euronext = list(csv.DictReader(open(os.path.join(racine, "donnees/CALENDRIER_EURONEXT.csv"), encoding="utf-8-sig")))
    fermes = {r["date"] for r in euronext if r["etat"] == "FERME"}
    borne = min([jusqu_au] + [r["date"] for r in euronext if r["etat"] == "COUVERT_JUSQU_AU"])
    d = datetime.date.fromisoformat(seances[-1]) + datetime.timedelta(days=1)
    while d.isoformat() <= borne:
        if d.weekday() < 5 and d.isoformat() not in fermes:
            seances.append(d.isoformat())
        d += datetime.timedelta(days=1)
    return seances


def sources_independantes(racine):
    """Relit, SANS le programme, tout ce qu'il faut pour recalculer la table et la confrontation.

    ① RÔLE — Le chemin indépendant de D1 (superviseur R-759 du 05-11-2026).
    ② CONTEXTE D'APPEL — `jouer`, une fois.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Les sources sont là.
    ⑤ SORTIE — UNE valeur : {seances : liste triée AAAA-MM-JJ (dates de l'indice, puis jours de semaine qu'Euronext
      ne déclare pas fermés jusqu'à la fin des réponses de Yahoo), fin : {mnémonique : date de Paris du dernier
      horodatage de sa réponse}, valeur_de : {mnémonique : nom
      usuel}, mnemo_de : {nom normé : mnémonique} (nom usuel et onglet Google), dividendes : liste de (mnémonique,
      date, source, montant), clot : {(source, mnémonique) : {date : clôture}} — Yahoo : clôture arrondie au 1e-4 comme
      le cours propre, barres filtrées par les mêmes règles écrites ici une seconde fois ; décidées : clôture brute
      de bnains hors des fenêtres de barres fausses}.
      [rend: 1]
    ⑥ TRAITEMENT — Lire l'indice (csv), le référentiel (csv), chaque réponse brute de Yahoo (JSON, dates de Paris),
      TOUS ses dividendes et toutes ses barres, sans coupure, les distributions décidées (csv), bnains et ses barres
      fausses (csv) ; les séances par `seances_independantes`. Seuls DEBUT_STELLANTIS, BRUTS et REFERENTIEL sont lus
      dans le module du cours propre de Yahoo, chargé à part, jamais par le programme.
    ⑦ UNITÉ — Euros de leur source ; dates de Paris.
    ⑧ POURQUOI — Une épreuve qui lit par le programme ne voit pas une faute du programme.
    ⑨ CE QUI CLOCHE — Les filtres de barres sont recopiés du cours propre (`barres`) : c'est voulu — deux lectures
      indépendantes qui doivent s'accorder ; elles divergeraient si l'une changeait, et l'épreuve rougirait.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    yp = charger(racine, "programmes/FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py", "yp_independant")
    ref = list(csv.DictReader(open(os.path.join(racine, yp.REFERENTIEL), encoding="utf-8-sig")))
    valeur_de = {r["mnemonique"]: r["nom_usuel"] for r in ref}
    mnemo_de = {}
    for r in ref:
        mnemo_de[norme(r["nom_usuel"])] = r["mnemonique"]
        mnemo_de[norme(r["onglet_google"])] = r["mnemonique"]
    paris = lambda t: datetime.datetime.fromtimestamp(int(t), ZoneInfo("Europe/Paris")).date().isoformat()  # noqa: E731
    dividendes, clot, fin = [], {}, {}
    dossier = os.path.join(racine, yp.BRUTS)
    for fichier in sorted(os.listdir(dossier)):
        s = fichier[:-len(".PA.json")]
        res = json.load(open(os.path.join(dossier, fichier), encoding="utf-8"))["chart"]["result"][0]
        fin[s] = paris(max(res["timestamp"]))
        for t, x in res.get("events", {}).get("dividends", {}).items():
            dividendes.append((s, paris(t), "yahoo du 21-10-2026", float(x["amount"])))
        q = res.get("indicators", {}).get("quote", [{}])[0]
        c = {}
        for i, t in enumerate(res.get("timestamp") or []):
            o, h, b, cl, v = (q.get(k, [None] * (i + 1))[i] for k in ("open", "high", "low", "close", "volume"))
            d = paris(t)
            if None in (o, h, b, cl, v) or v == 0 or not (b <= o <= h and b <= cl <= h):
                continue
            if valeur_de.get(s) == "STELLANTIS" and d < yp.DEBUT_STELLANTIS:
                continue
            c[d] = round(cl, 4)
        clot[("yahoo du 21-10-2026", s)] = c
    nom_mn = {r["nom_usuel"]: r["mnemonique"] for r in ref}
    for r in csv.DictReader(open(os.path.join(racine, "donnees/sources_dividendes/DISTRIBUTIONS_DECIDEES.csv"), encoding="utf-8-sig")):
        dividendes.append((nom_mn[r["valeur"]], r["date"], "décision écrite à la main", float(r["montant"])))
    fausses = list(csv.DictReader(open(os.path.join(racine, "donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv"), encoding="utf-8-sig")))
    for r in csv.DictReader(open(os.path.join(racine, "donnees/sources_bnains/bnains_cac40.csv"), encoding="utf-8-sig")):
        if r["valeur"] not in nom_mn or any(f["valeur"] == r["valeur"] and f["premiere_seance"] <= r["date"] <= f["derniere_seance"] for f in fausses):
            continue
        clot.setdefault(("décision écrite à la main", nom_mn[r["valeur"]]), {})[r["date"]] = float(r["close"])
    seances = seances_independantes(racine, max(fin.values()))
    return {"seances": seances, "fin": fin, "valeur_de": valeur_de, "mnemo_de": mnemo_de, "dividendes": dividendes,
            "clot": clot}


def cas_e3(racine, m, m2, entete, lignes, tmp, src):
    """E3 COUVERTURE — chaque dividende de la source est dans la table, une fois, À SA DATE ; la table n'a rien d'autre.

    ① RÔLE — Superviseur, contrôle 3 ; décision Q-DIV5 (date de la source telle quelle).
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1, et `src` (`sources_independantes`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Comparer les clés (mnémonique, date, source,
    montant) de la source et de la table, en multiensembles.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — « En retirer un fait rougir ».
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if releve_de_la_table(m, lignes) != "bruts_yahoo_21-10-2026":
        return ["E3 ne sait relire que le relevé bruts_yahoo_21-10-2026"]
    s = sorted((a, b, c, repr(d)) for a, b, c, d in src["dividendes"])
    t = sorted((r["mnemonique"], r["date_detachement"], r["source"], r["montant_source"]) for r in lignes)
    if s == t:
        return []
    return [f"table {len(t)} lignes, source {len(s)} ; manquent {[k for k in s if k not in t][:5]} ; "
            f"en trop {[k for k in t if k not in s][:5]}"]


def cas_e4(racine, m, m2, entete, lignes, tmp):
    """E4 UNIBAIL 07-10-2010 — la distribution de 20 € est dans la table, avec sa décision, et inscrite au carnet.

    ① RÔLE — Superviseur, contrôle 4 ; décision n°89.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Une ligne UNIBAIL 2010-10-07 de source décidée ; son montant est celui que la question de n°89
      énonce (« 20 € par action », lu dans le fichier que nomme la citation, jamais recopié ici) ; sa citation nomme
      n°89 ; le fichier des distributions est inscrit au carnet comme écrit à la main.
    ⑦ UNITÉ — Euros du jour.
    ⑧ POURQUOI — Rustine interdite : « ajouter Unibail 2010 sans source ni ligne de
      provenance ».
    ⑨ CE QUI CLOCHE — Le montant n'a pas de document officiel au dépôt.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    u = [r for r in lignes if r["mnemonique"] == "URW" and r["date_detachement"] == "2010-10-07"]
    if len(u) != 1 or u[0]["source"] != m.SOURCE_DECIDEE:
        return [f"Unibail 2010-10-07 trouvée {len(u)} fois avec la source décidée"]
    dec = [r for r in csv.DictReader(open(os.path.join(racine, m.DECIDEES), encoding="utf-8-sig"))
           if r["valeur"].startswith("UNIBAIL") and r["date"] == "2010-10-07"]
    if len(dec) != 1 or "n°89" not in dec[0]["citation"]:
        return [f"distribution d'Unibail du 2010-10-07 trouvée {len(dec)} fois dans les distributions décidées "
                "(il en faut une, qui cite la décision n°89)"]
    textes = re.findall(r"etudes/\S+?\.md", dec[0]["citation"])
    if not textes:
        fautes.append("la citation ne nomme pas le fichier qui porte le texte de la décision n°89")
    for cite in textes:
        texte = open(os.path.join(racine, cite), encoding="utf-8").read()
        mt = re.search(r"## n°89 .*?versé (\d+) € par action", texte, re.S)
        if not mt:
            fautes.append(f"{cite} ne porte pas le montant de la décision n°89")
        elif float(mt.group(1)) != float(u[0]["montant_source"]):
            fautes.append(f"montant {u[0]['montant_source']} au lieu de {mt.group(1)} (décision n°89)")
    carnet = [r for r in csv.DictReader(open(os.path.join(racine, "donnees/PROVENANCE_DES_FICHIERS.csv"), encoding="utf-8"))
              if r["fichier"] == m.DECIDEES.replace(os.sep, "/")]
    if len(carnet) != 1 or carnet[0]["produit_par"] != m.ECRIT_A_LA_MAIN or "n°89" not in carnet[0]["preuve"]:
        fautes.append("les distributions décidées ne sont pas inscrites au carnet, écrites à la main, avec n°89")
    return fautes


def cas_e5(racine, m, m2, entete, lignes, tmp, src):
    """E5 RECALCUL INDÉPENDANT — chaque colonne que lira `jouer` se refait depuis les sources, sans le programme.

    ① RÔLE — Superviseur R-759 du 05-11-2026, D1.
    ② CONTEXTE D'APPEL — `jouer`, sur les deux tables.
    ③ ENTRÉE — comme E1, et `src`.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — L'en-tête est exactement celui attendu (10 colonnes : aucune ne dépend d'une courbe). Pour chaque
      ligne, la clé (mnémonique, date_detachement, source) doit être un dividende de la source ; la veille est la
      séance de l'indice qui précède la date ; cloture_source_veille = la clôture de la veille DANS LA MÊME SOURCE ;
      rendement = montant ÷ clôture ; statut MONTANT CONNU si le rendement se calcule, MONTANT INCONNU sinon ; valeur =
      le nom usuel du mnémonique ; couverte_jusqu_au = la date du dernier horodatage de la réponse de Yahoo de la
      valeur, ou, pour une distribution décidée, sa propre date. Comparaison au texte écrit (6 et 10 décimales).
    ⑦ UNITÉ — Euros de la source ; fraction.
    ⑧ POURQUOI — Voir la fiche en tête, ⑧ ; exemple réel : Pernod Ricard
      11-06-2002, montant faux de 22 % au tour 1, épreuve verte.
    ⑨ CE QUI CLOCHE — Voir `sources_independantes`, ⑨.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    attendu = ["valeur", "mnemonique", "source", "date_detachement", "montant_source", "unite_source",
               "cloture_source_veille", "rendement", "statut", "couverte_jusqu_au"]
    fautes = [] if list(entete) == attendu else [f"en-tête {entete} au lieu de {attendu}"]
    divs = {}
    for s, d, so, mt in src["dividendes"]:
        divs.setdefault((s, d, so), []).append(mt)
    for r in lignes:
        k = (r["mnemonique"], r["date_detachement"], r["source"])
        if len(divs.get(k, [])) != 1:
            fautes.append(f"{k} : {len(divs.get(k, []))} dividende(s) à cette date dans la source")
            continue
        mt = divs[k][0]
        i = src["seances"].index(r["date_detachement"]) if r["date_detachement"] in src["seances"] else -1
        veille = src["seances"][i - 1] if i > 0 else None
        cs = src["clot"].get((r["source"], r["mnemonique"]), {}).get(veille)
        ren = mt / cs if cs else None
        voulu = {"valeur": src["valeur_de"].get(r["mnemonique"]), "montant_source": repr(mt),
                 "cloture_source_veille": "" if cs is None else f"{cs:.6f}",
                 "rendement": "" if ren is None else f"{ren:.10f}",
                 "statut": "MONTANT CONNU" if ren is not None else "MONTANT INCONNU",
                 "couverte_jusqu_au": src["fin"].get(r["mnemonique"]) if r["source"] != "décision écrite à la main"
                 else r["date_detachement"]}
        for col, v in voulu.items():
            if r[col] != v:
                fautes.append(f"{r['valeur']} {r['date_detachement']} : {col} « {r[col]} » au lieu de « {v} » "
                              f"(clôture de la veille {veille} dans la source)")
    return fautes[:10]


def cas_e6(racine, m, m2, entete, lignes, tmp):
    """E6 JAMAIS UN ZÉRO SILENCIEUX — une donnée absente est vide et son statut le dit.

    ① RÔLE — Consigne du lot : « une donnée manquante est DITE (jamais un zéro silencieux) ».
    ② CONTEXTE D'APPEL —
    `jouer`, sur les deux tables.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : la liste
    des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — rendement vide si et seulement si cloture_source_veille vide, si et seulement si MONTANT INCONNU ;
      aucun nombre de la table ne vaut zéro ; vraie ligne : au moins une ligne MONTANT INCONNU (ArcelorMittal et
      Peugeot sous Stellantis avant le 18-01-2021, sans clôture chez Yahoo).
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Un zéro passerait pour « aucun dividende ».
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    for r in lignes:
        if not (bool(r["rendement"]) == bool(r["cloture_source_veille"]) == (r["statut"] == "MONTANT CONNU")):
            fautes.append(f"{r['valeur']} {r['date_detachement']} : rendement « {r['rendement']} », clôture "
                          f"« {r['cloture_source_veille']} », statut {r['statut']}")
        for k in ("montant_source", "cloture_source_veille", "rendement"):
            if r[k] and float(r[k]) == 0:
                fautes.append(f"{r['valeur']} {r['date_detachement']} : {k} vaut zéro")
    if not any(r["statut"] == "MONTANT INCONNU" for r in lignes):
        fautes.append("aucune ligne MONTANT INCONNU : l'absence n'est jamais dite sur les vraies données")
    return fautes[:10]


def cas_e7(racine, m, m2, entete, lignes, tmp):
    """E7 VRAIES LIGNES — Bureau Veritas 01-07-2025 rend le montant et le rendement de l'exemple de R-113 ; chaque
    détachement du témoin officiel ABC est dans la table, à la date officielle.

    ① RÔLE — Des cas réellement survenus (R-732), et la garde de la décision Q-DIV5.
    ② CONTEXTE D'APPEL — `jouer`,
    sur les deux tables.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — R-113 porte « dividende de 0,90 € (3,11 %) » pour Bureau Veritas ; le témoin ABC est au
    dépôt.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le montant et le pourcentage dans le texte de R-113 (jamais recopiés ici) ; les comparer à la
      ligne BVI 2025-07-01 ; pour chaque ligne du témoin ABC datée jusqu'à la dernière date de la table : une valeur de
      la table dont le nom normé commence par celui d'ABC (ou l'inverse), exactement une, et une ligne à la date d'ABC.
    ⑦ UNITÉ — Euros, pourcentages.
    ⑧ POURQUOI — Mesure du superviseur du 05-11-2026 : la date de Yahoo est la date
      officielle 50 fois sur 50 ; la correction automatique en déplaçait 4 (LVMH 02-12-2025 → 03-12-2025…).
    ⑨ CE QUI CLOCHE — Le pourcentage de R-113 est arrondi à deux décimales ; le témoin ne couvre qu'une année.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    reg = open(os.path.join(racine, "gouvernance/REGISTRE_REGLES.md"), encoding="utf-8").read()
    mt = re.search(r"Bureau Veritas, détachement du (\d\d)-(\d\d)-(\d{4}), dividende de (\d+),(\d+) € \((\d+),(\d+) %\)", reg)
    if not mt:
        return ["l'exemple de R-113 (Bureau Veritas) est introuvable au REGISTRE"]
    jour = f"{mt.group(3)}-{mt.group(2)}-{mt.group(1)}"
    montant, pct = float(mt.group(4) + "." + mt.group(5)), float(mt.group(6) + "." + mt.group(7))
    b = [r for r in lignes if r["mnemonique"] == "BVI" and r["date_detachement"] == jour]
    if len(b) != 1 or float(b[0]["montant_source"]) != montant or not b[0]["rendement"] \
            or round(100 * float(b[0]["rendement"]), 2) != pct:
        fautes.append(f"Bureau Veritas {jour} : {[(r['montant_source'], r['rendement']) for r in b]} au lieu de "
                      f"{montant} € · {pct} %")
    fin = max(r["date_detachement"] for r in lignes)
    noms = {norme(r["valeur"]) for r in lignes}
    vus = 0
    for l in csv.reader(open(os.path.join(racine, TEMOIN_ABC), encoding="utf-8")):
        if len(l) < 5 or not re.fullmatch(r"\d\d/\d\d/\d{4}", l[1]):
            continue
        j, mo, a = l[1].split("/")
        d = f"{a}-{mo}-{j}"
        if d > fin:
            continue
        n = norme(l[2].replace("CAC 40", ""))
        cand = [v for v in noms if v.startswith(n) or n.startswith(v)]
        if len(cand) != 1:
            fautes.append(f"témoin ABC : {l[2]} rapproché de {cand}")
            continue
        vus += 1
        if not any(norme(r["valeur"]) == cand[0] and r["date_detachement"] == d for r in lignes):
            fautes.append(f"témoin ABC : {l[2]} détaché le {d}, absent de la table à cette date")
    if vus == 0:
        fautes.append("aucune ligne du témoin ABC jugée")
    return fautes[:10]


def cas_e8(racine, m, m2, entete, lignes, tmp):
    """E8 PROVENANCE — la table est inscrite UNE fois au carnet, à son empreinte, produite par le programme, avec la liste
    exacte des fichiers qu'il ouvre ; la chaîne remonte jusqu'à un premier maillon (K23).

    ① RÔLE — Règle de n°54 : la table au dépôt est inscrite à la provenance.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Lire la ligne du carnet ; espionner `open` pendant `fabriquer` pour relever les fichiers ouverts
      sous la racine (le carnet mis à part, ⑥ de `fichiers_lus`) ; comparer à la colonne `lu` et à `fichiers_lus` ;
      lancer `maillons_manquants` du contrôle K23.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Une liste `lu` tenue à côté du code peut mentir : seule la mesure le dit.
    ⑨ CE QUI CLOCHE — Un fichier ouvert autrement que par `open` (os.open, mmap) échapperait à l'espion.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    carnet = [r for r in csv.DictReader(open(os.path.join(racine, "donnees/PROVENANCE_DES_FICHIERS.csv"), encoding="utf-8"))
              if r["fichier"] == TABLE]
    if len(carnet) != 1:
        return [f"table inscrite {len(carnet)} fois au carnet"]
    c = carnet[0]
    if c["sha256"] != hashlib.sha256(open(os.path.join(racine, TABLE), "rb").read()).hexdigest():
        fautes.append("empreinte du carnet différente de la table")
    if c["produit_par"] != PROGRAMME:
        fautes.append(f"produite par {c['produit_par']}")
    releve = releve_de_la_table(m, lignes)
    ouverts = set()
    vrai_open = builtins.open
    base = os.path.abspath(racine)

    def espion(f, *a, **k):
        """Relève un fichier ouvert puis l'ouvre.
        ① RÔLE — Mesurer ce que lit `fabriquer`.
        ② CONTEXTE D'APPEL — à la
        place de `open`, pendant E8.
        ③ ENTRÉE — Les arguments de `open`.
        ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — UNE valeur : le fichier ouvert par le vrai `open`.
          [rend: 1]
        ⑥ TRAITEMENT — Garder le chemin
        relatif s'il est sous la racine.
        ⑦ UNITÉ — —.
        ⑧ POURQUOI — Voir E8.
        ⑨ CE QUI CLOCHE — Un descripteur entier
        n'est pas relevé.
        ⑩ EFFET — Ajoute à `ouverts`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if isinstance(f, str):
            p = os.path.abspath(f)
            if p.startswith(base + os.sep):
                ouverts.add(os.path.relpath(p, base).replace(os.sep, "/"))
        return vrai_open(f, *a, **k)
    builtins.open = espion
    try:
        m.fabriquer(racine, releve)
    finally:
        builtins.open = vrai_open
    declares = m.fichiers_lus(racine, releve)
    ouverts.discard(m.YP.CARNET.replace(os.sep, "/"))  # le carnet contrôle les sources, il n'en est pas une (⑥ de fichiers_lus)
    if sorted(ouverts) != declares:
        fautes.append(f"ouverts et non déclarés {sorted(ouverts - set(declares))} ; déclarés et non ouverts "
                      f"{sorted(set(declares) - ouverts)}")
    if c["lu"].split(";") != declares:
        fautes.append("la colonne lu du carnet n'est pas la liste des fichiers lus")
    manques = m.HL.maillons_manquants(racine, [TABLE])
    if manques:
        fautes.append(f"K23 : {manques[:3]}")
    return fautes


def cas_e9(racine, m, m2, entete, lignes, tmp):
    """E9 RÉGLAGE SANS DÉFAUT, CODES DE SORTIE des deux programmes.

    ① RÔLE — Le choix du relevé revient à Jean-Luc (Q-DIV1) : jamais de valeur par défaut ; un refus rend 1, une panne
    2.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — EVENEMENTS_YAHOO.csv n'est pas inscrit au carnet (vrai le 05-11-2026).
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Fabrication : sans --releve → 2 ; relevé inconnu → 1 ; relevé non inscrit → 1 ; racine absente → 2.
      Confrontation : un argument de moins → 2 ; courbe absente → 2 ; table à l'en-tête faux → 1.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Un code 1 de Python non attrapé passerait pour un refus.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    faux = os.path.join(tmp, "entete_faux.csv")
    open(faux, "w", encoding="utf-8").write("valeur,date\nACCOR,2024-01-02\n")
    essais = ((m.main, [racine, os.path.join(tmp, "a.csv")], 2),
              (m.main, [racine, os.path.join(tmp, "b.csv"), "--releve=nimporte"], 1),
              (m.main, [racine, os.path.join(tmp, "c.csv"), "--releve=evenements_yahoo_08-10-2026"], 1),
              (m.main, [os.path.join(tmp, "absente"), os.path.join(tmp, "d.csv"), "--releve=bruts_yahoo_21-10-2026"], 2),
              (m2.main, [racine, TABLE], 2),
              (m2.main, [racine, TABLE, "donnees/absent.csv"], 2),
              (m2.main, [racine, faux, COURBE_DU_JUGE], 1))
    for f, args, attendu in essais:
        with redirect_stdout(io.StringIO()):
            code = f(args)
        if code != attendu:
            fautes.append(f"{f.__module__}.main{args[1:]} rend {code} au lieu de {attendu}")
    return fautes


def cas_e10(racine, m, m2, entete, lignes, tmp):
    """E10 AUCUN ARGUMENT À VALEUR PAR DÉFAUT dans les fonctions des deux programmes.

    ① RÔLE — Règle commune aux lots de D (superviseur R-759 du 05-11-2026, §1) : un seuil, une durée ou un réglage
    arrive en argument sans valeur par défaut.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `m`, `m2`.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — inspect.signature de chaque fonction définie dans chaque programme.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Propriété plutôt que liste : toute fonction, sans en nommer aucune.
    ⑨ CE QUI CLOCHE — Plus strict que
    la règle (qui ne vise que les seuils) : assumé, les programmes n'en ont aucun besoin.
    ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    for mod in (m, m2):
        for nom, f in inspect.getmembers(mod, inspect.isfunction):
            if f.__module__ != mod.__name__:
                continue
            for p in inspect.signature(f).parameters.values():
                if p.default is not inspect.Parameter.empty:
                    fautes.append(f"{nom}({p.name}={p.default!r})")
    return fautes


def cas_e11(racine, m, m2, entete, lignes, tmp):
    """E11 REFUS — un dividende mal formé ou en double est refusé (code 1), quelle que soit sa source.

    ① RÔLE — Superviseur R-759 du 05-11-2026, D2 et D5.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — Les distributions décidées portent la ligne d'Unibail du 07-10-2010.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — Dans un reflet, la ligne d'Unibail est recopiée en une seconde ligne changée, le carnet remis à
      l'empreinte, et la fabrication doit être REFUSÉE avec la bonne raison : a) doublon d'un dividende de Yahoo
      (BUREAU VERITAS, 2025-07-01, 0.9 — cas du relecteur), par `main`, code 1 ; b) date mal écrite « 01/07/2009 » ;
      c) date hors séance (samedi 04-07-2009) ; d) montant négatif ; e) montant « nan » ; f) montant illisible ; g)
      doublon de la ligne d'Unibail elle-même.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Au tour 1, b) donnait un détachement au 03-01-2000 en silence, a) et d) étaient acceptés.
    ⑨ CE QUI CLOCHE — Chaque variante refait une fabrication (~10 s).
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rel = m.DECIDEES.replace(os.sep, "/")
    banc = os.path.join(tmp, "e11")
    refleter(racine, banc, {rel, "donnees/PROVENANCE_DES_FICHIERS.csv"})
    original = open(os.path.join(racine, rel), encoding="utf-8").read()
    unibail = [l for l in original.splitlines() if ",2010-10-07,20," in l]
    if len(unibail) != 1:
        return [f"ligne d'Unibail 2010-10-07 trouvée {len(unibail)} fois"]
    u = unibail[0]
    variantes = [
        ("a", u.replace("UNIBAIL-RODAMCO-WESTFIELD,2010-10-07,20,", "BUREAU VERITAS,2025-07-01,0.9,"), "à la même date"),
        ("b", u.replace(",2010-10-07,20,", ",01/07/2009,1,"), "date mal écrite"),
        ("c", u.replace(",2010-10-07,20,", ",2009-07-04,1,"), "pas une séance"),
        ("d", u.replace(",2010-10-07,20,", ",2009-07-01,-5,"), "strictement positif"),
        ("e", u.replace(",2010-10-07,20,", ",2009-07-01,nan,"), "strictement positif"),
        ("f", u.replace(",2010-10-07,20,", ",2009-07-01,abc,"), "montant illisible"),
        ("g", u, "à la même date"),
    ]
    fautes = []
    p = os.path.join(banc, rel)
    for nom, ligne, raison in variantes:
        os.unlink(p)
        open(p, "w", encoding="utf-8").write(original.rstrip("\n") + "\n" + ligne + "\n")
        inscrire_a_nouveau(banc, rel)
        if nom == "a":
            ecran = io.StringIO()
            with redirect_stdout(ecran):
                code = m.main([banc, os.path.join(tmp, "a.csv"), "--releve=bruts_yahoo_21-10-2026"])
            if code != 1 or raison not in ecran.getvalue():
                fautes.append(f"{nom}) main rend {code} : {ecran.getvalue()[-200:]!r} (refus « {raison} » attendu)")
            continue
        try:
            m.fabriquer(banc, "bruts_yahoo_21-10-2026")
            fautes.append(f"{nom}) acceptée : {ligne[:60]} (refus « {raison} » attendu)")
        except m.Refus as e:
            if raison not in str(e):
                fautes.append(f"{nom}) refusée pour une autre raison : {str(e)[:160]}")
    return fautes


def cas_e12(racine, m, m2, entete, lignes, tmp):
    """E12 CONFRONTATION — sur la courbe du juge, chaque mesure se refait sans le programme ; aucune ligne mesurable
    n'est perdue ; le résumé par année et source se refait EN ENTIER ; la partie non couverte se refait ; sur une copie
    de la courbe percée de deux trous, rien ne se mesure à travers un trou ; le programme n'écrit rien.

    ① RÔLE — Éprouver programmes/CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — comme E1.
    ④ CONDITIONS D'ENTRÉE — COURBE_DU_JUGE est au dépôt ; Engie 30-04-2026 y est mesurable.
    ⑤ SORTIE — UNE valeur : la liste des fautes.
      [rend: 1]
    ⑥ TRAITEMENT — ① Lire la courbe en csv (noms normés vers les mnémoniques du référentiel, colonnes nom usuel et
      onglet Google) et les séances par `seances_independantes` ; pour chaque ligne de la table : mesurable si elle a
      un rendement, si la valeur est dans la courbe, si sa date est après la première date de la courbe et au plus
      tard la dernière, et si les barres du jour et de la veille existent ; observée = ouverture ÷ clôture de la
      veille − 1 ; témoin = la même à la séance d'avant. Comparer à `confronter` (raison None ⇔ mesurable ; valeurs à
      1e-12). ② Refaire, par (année, source de la barre), n, la moyenne attendue, la moyenne observée, leur rapport,
      le compte « sans baisse » |o| ≤ |o + rendement|, et le témoin « un dividende entier ajouté au mouvement de la
      séance d'avant sortirait-il sans baisse ? » |t − rendement| ≤ |t| ; comparer à `resumer` (comptes égaux,
      fractions à 1e-12). ③ Refaire la partie non couverte : pour chaque valeur de la courbe, ses barres après le plus
      tard des couverte_jusqu_au de ses lignes ; comparer à `confronter` et à la ligne « COURBE NON COUVERTE » de
      `main`. ④ TROUS FABRIQUÉS (R-110, R-115) : copie de la courbe sans la barre d'Engie à la veille du 30-04-2026,
      et sans la barre d'une autre valeur mesurée deux séances avant son détachement ; Engie doit sortir « BARRE DU
      JOUR OU DE LA VEILLE ABSENTE », l'autre doit rester mesurée avec un témoin inconnu. ⑤ `main` : code 0, une ligne
      d'écart par ligne mesurée, Engie 30-04-2026 dans la liste, aucune ouverture de fichier en écriture.
    ⑦ UNITÉ — Fractions ; nombres de lignes ; nombres de barres.
    ⑧ POURQUOI — Le contrôle qui signale doit lui-même être juste (R-731). Relecture du tour 2 (T2, T8) : les
      programmes faussés X1 (rapport sans les hausses), X2 (témoin pris le jour du détachement) et X3 (séance d'avant
      prise dans les barres) laissaient E12 vert ; superviseur R-759 avant le tour 3 : ils doivent le faire tomber.
    ⑨ CE QUI CLOCHE — La courbe du juge ne couvre que 2024-2026 : la confrontation sur vingt ans n'est éprouvée que par
      le même code, pas par ce cas. · Les trous sont fabriqués sur deux lignes seulement.
    ⑩ EFFET — Écrit la copie percée dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    mesures, desc = m2.confronter(racine, TABLE, COURBE_DU_JUGE)
    ref = list(csv.DictReader(open(os.path.join(racine, m.YP.REFERENTIEL), encoding="utf-8-sig")))
    mn = {norme(r[k]): r["mnemonique"] for r in ref for k in ("nom_usuel", "onglet_google")}
    brutes = list(csv.DictReader(open(os.path.join(racine, COURBE_DU_JUGE), encoding="utf-8-sig")))
    barres = {}
    for r in brutes:
        barres.setdefault(mn.get(norme(r["valeur"]), "?" + r["valeur"]), {})[r["date"]] = r
    debut = min(min(b) for b in barres.values())
    fin = max(max(b) for b in barres.values())
    s = seances_independantes(racine, fin)

    def ouv(b, d):
        """Écart d'ouverture indépendant.
        ① RÔLE — Recalcul de E12.
        ② CONTEXTE D'APPEL — E12.
        ③ ENTRÉE — `b` : les
        barres d'une valeur, `d` : une date.
        ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — UNE valeur : fraction ou None.
        [rend: 1]
        ⑥ TRAITEMENT — veille au calendrier (`seances_independantes`).
        ⑦ UNITÉ — Fraction.
        ⑧ POURQUOI — R-110.
        ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — —.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if d not in s or s.index(d) == 0:
            return None
        v = s[s.index(d) - 1]
        return float(b[d]["open"]) / float(b[v]["close"]) - 1 if d in b and v in b else None
    if len(mesures) != len(lignes):
        fautes.append(f"{len(mesures)} mesures pour {len(lignes)} lignes")
    groupes = {}
    for r, x in zip(lignes, mesures):
        b = barres.get(r["mnemonique"], {})
        o = ouv(b, r["date_detachement"]) if r["rendement"] and debut < r["date_detachement"] <= fin else None
        if (o is None) != (x["raison"] is not None) or (x["mnemonique"], x["date"]) != (r["mnemonique"], r["date_detachement"]):
            fautes.append(f"{r['valeur']} {r['date_detachement']} : mesurable {o is not None}, raison {x['raison']}")
            continue
        if o is None:
            continue
        t = ouv(b, s[s.index(r["date_detachement"]) - 1])
        if abs(x["observee"] - o) > 1e-12 or abs(x["attendue"] + float(r["rendement"])) > 1e-12 \
                or (t is None) != (x["temoin"] is None) or (t is not None and abs(x["temoin"] - t) > 1e-12):
            fautes.append(f"{r['valeur']} {r['date_detachement']} : observée {x['observee']} au lieu de {o}, témoin "
                          f"{x['temoin']} au lieu de {t}")
        groupes.setdefault((r["date_detachement"][:4], b[r["date_detachement"]].get("source") or "non dite"), []).append(
            (o, float(r["rendement"]), t))
    voulu = {}
    for k, g in groupes.items():
        att = -sum(ren for _, ren, _ in g) / len(g)
        obs = sum(o for o, _, _ in g) / len(g)
        tem = [(t, ren) for _, ren, t in g if t is not None]
        voulu[k] = {"n": len(g), "attendue_moy": att, "observee_moy": obs, "rapport": obs / att,
                    "sans_baisse": sum(1 for o, ren, _ in g if abs(o) <= abs(o + ren)),
                    "temoin_n": len(tem), "temoin_sans_baisse": sum(1 for t, ren in tem if abs(t - ren) <= abs(t))}
    resume = m2.resumer(mesures)
    ecarts = sorted(f"{k} {c} : {resume.get(k, {}).get(c)} au lieu de {v}" for k, g in voulu.items() for c, v in g.items()
                    if not (isinstance(resume.get(k, {}).get(c), (int, float)) and abs(resume[k][c] - v) <= 1e-12))
    if set(resume) != set(voulu) or ecarts:
        fautes.append(f"comptes par année et source : groupes {sorted(resume)} au lieu de {sorted(voulu)} ; {ecarts[:4]}")
    couverture = {}
    for r in lignes:
        couverture[r["mnemonique"]] = max(couverture.get(r["mnemonique"], ""), r["couverte_jusqu_au"])
    nc = {}
    for mm, b in barres.items():
        apres = sorted(d for d in b if d > couverture.get(mm, ""))
        if apres:
            nc[mm] = (apres[0], apres[-1], len(apres))
    if desc["non_couvert"] != nc:
        fautes.append(f"non couvert : {sorted(desc['non_couvert'].items())[:3]} au lieu de {sorted(nc.items())[:3]} "
                      f"({len(desc['non_couvert'])} valeurs au lieu de {len(nc)})")
    # ④ les trous fabriqués
    eng = [x for x in mesures if x["mnemonique"] == "ENGI" and x["date"] == "2026-04-30"]
    autre = [x for x in mesures if x["raison"] is None and x["temoin"] is not None and x["mnemonique"] != "ENGI"]
    if len(eng) != 1 or eng[0]["raison"] is not None or not autre:
        fautes.append("trou fabriqué : Engie 30-04-2026 n'est pas mesurable sur la courbe entière, ou aucune autre ligne")
    else:
        a = autre[0]
        percer = {("ENGI", s[s.index("2026-04-30") - 1]), (a["mnemonique"], s[s.index(a["date"]) - 2])}
        copie = os.path.join(tmp, "courbe_percee", os.path.basename(COURBE_DU_JUGE))
        os.makedirs(os.path.dirname(copie))
        with open(os.path.join(racine, COURBE_DU_JUGE), encoding="utf-8-sig", newline="") as f:
            lecteur = csv.DictReader(f)
            garde = [r for r in lecteur if (mn.get(norme(r["valeur"])), r["date"]) not in percer]
            champs = lecteur.fieldnames
        with open(copie, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, champs, lineterminator="\n")
            w.writeheader()
            w.writerows(garde)
        if len(garde) != len(brutes) - 2:
            fautes.append(f"trou fabriqué : {len(brutes) - len(garde)} barres retirées au lieu de 2")
        percee, _ = m2.confronter(racine, TABLE, copie)
        pe = [x for x in percee if (x["mnemonique"], x["date"]) == ("ENGI", "2026-04-30")]
        pa = [x for x in percee if (x["mnemonique"], x["date"]) == (a["mnemonique"], a["date"])]
        if [x["raison"] for x in pe] != [m2.RAISONS[3]]:
            fautes.append(f"trou fabriqué : Engie 30-04-2026 sans sa veille sort {[x['raison'] for x in pe]} au lieu de "
                          f"« {m2.RAISONS[3]} » (mesure à travers un trou)")
        if [(x["raison"], x["temoin"]) for x in pa] != [(None, None)]:
            fautes.append(f"trou fabriqué : {a['valeur']} {a['date']} sans la barre de deux séances avant sort "
                          f"{[(x['raison'], x['temoin']) for x in pa]} au lieu d'une mesure au témoin inconnu")
    ecritures = []
    vrai_open = builtins.open

    def espion(f, mode="r", *a, **k):  # noqa: E306
        """Relève une ouverture en écriture.
        ① RÔLE — Prouver que la confrontation n'écrit rien.
        ② CONTEXTE
        D'APPEL — à la place de `open`, pendant `main` de la confrontation.
        ③ ENTRÉE — Les arguments de `open`.
        ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — UNE valeur : le fichier ouvert.
          [rend: 1]
        ⑥ TRAITEMENT — Un mode
        qui contient w, a, x ou + est relevé.
        ⑦ UNITÉ — —.
        ⑧ POURQUOI — « Elle n'écrit rien que `jouer` lise »
        (superviseur).
        ⑨ CE QUI CLOCHE — os.open échapperait.
        ⑩ EFFET — Ajoute à `ecritures`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if any(c in mode for c in "wax+"):
            ecritures.append(f)
        return vrai_open(f, mode, *a, **k)
    ecran = io.StringIO()
    builtins.open = espion
    try:
        with redirect_stdout(ecran):
            code = m2.main([racine, TABLE, COURBE_DU_JUGE])
    finally:
        builtins.open = vrai_open
    lignes_ecart = [l for l in ecran.getvalue().splitlines() if l.startswith("  ") and " · attendue " in l]
    mesurees = sum(1 for x in mesures if x["raison"] is None)
    if code != 0 or ecritures or len(lignes_ecart) != mesurees or mesurees == 0:
        fautes.append(f"main : code {code}, écritures {ecritures}, {len(lignes_ecart)} écarts affichés pour {mesurees}")
    if not any(" · ENGIE · 2026-04-30 · " in l for l in lignes_ecart):
        fautes.append("Engie 30-04-2026 (vrai dividende de 1,35 €, témoin ABC) n'est pas dans la liste des écarts")
    dit = f"COURBE NON COUVERTE PAR LA TABLE : {len(nc)} valeur(s), {sum(n for _, _, n in nc.values())} barre(s)"
    if not any(l.startswith(dit) for l in ecran.getvalue().splitlines()):
        fautes.append(f"main : la ligne « {dit} » manque à l'écran (non couvert tu)")
    return fautes[:10]


CAS = [("E1", cas_e1), ("E2", cas_e2), ("E3", cas_e3), ("E4", cas_e4), ("E5", cas_e5), ("E6", cas_e6),
       ("E7", cas_e7), ("E8", cas_e8), ("E9", cas_e9), ("E10", cas_e10), ("E11", cas_e11), ("E12", cas_e12)]
# Les cas qui éprouvent une PROPRIÉTÉ DE LA TABLE se jouent sur la table déposée ET sur la table refaite par le
# programme : sur la seule table déposée, un programme saboté passait (défaut trouvé au tour 1, S3, S6, S7).
SUR_LES_DEUX_TABLES = {"E3", "E5", "E6", "E7"}
# Les cas qui reçoivent en plus les sources relues sans le programme.
AVEC_LES_SOURCES = {"E3", "E5"}

# Chaque sabotage : (nom, cas visé, faute attendue — un morceau du texte de la faute, fichier changé, ancien texte,
# nouveau texte, réinscrire au carnet ?). Le cas visé doit tomber AVEC cette faute : dans un reflet, E8 tombe toujours,
# car K23 refuse de lire à travers un lien symbolique (mesuré le 05-11-2026) ; « le cas tombe » ne suffirait pas.
# R… : les programmes faussés du relecteur du 05-11-2026, adaptés à la table simplifiée ; ils doivent mordre hors E1.
SABOTAGES = [
    ("S1 table déposée : un montant changé", "E1", "diffère de la table déposée", TABLE, None, None, False),
    ("S2 la vérification de l'empreinte retirée", "E2", "distribution décidée changée sans son carnet", PROGRAMME,
     '    if hashlib.sha256(octets).hexdigest() != lignes[0]["sha256"]:\n        raise Refus(f"{chemin} : empreinte différente de celle du carnet")\n',
     "", False),
    ("S3 un dividende de la source oublié", "E3", "AC', '2019-05-10", PROGRAMME,
     "                d = YP.date_de_paris(t)\n",
     "                d = YP.date_de_paris(t)\n                if s == \"AC.PA\" and d == \"2019-05-10\":\n                    continue\n", False),
    ("S4 Unibail 2010 retirée des distributions décidées", "E4", "trouvée 0 fois dans les distributions décidées",
     "donnees/sources_dividendes/DISTRIBUTIONS_DECIDEES.csv", None, None, True),
    ("S5 (R4 adapté) mélange d'unités : clôture brute de Paris pour un montant de Yahoo avant 2017", "E5",
     "cloture_source_veille", PROGRAMME,
     "        clot_src = clot_y if x[\"unite\"] == UNITE_YAHOO else clot_p\n",
     "        clot_src = clot_y if x[\"unite\"] == UNITE_YAHOO and x[\"date\"] >= \"2017-03-01\" else clot_p\n", False),
    ("S6 une donnée absente écrite zéro", "E6", "vaut zéro", PROGRAMME,
     '    return "" if x is None else f"{x:.{chiffres}f}"', '    return f"{0 if x is None else x:.{chiffres}f}"', False),
    ("S7 (R7 adapté) clôture de la veille remplacée par l'ouverture", "E5", "cloture_source_veille", PROGRAMME,
     "        clotures[s[:-3]] = {b[1]: float(b[5]) for b in YP.barres(v, reponses[s], None)}\n",
     "        clotures[s[:-3]] = {b[1]: float(b[2]) for b in YP.barres(v, reponses[s], None)}\n", False),
    ("S8 un fichier lu non déclaré", "E8", "ouverts et non déclarés ['donnees/sources_indice/INDICE_CAC40.csv']", PROGRAMME,
     '    lus = {YP.REFERENTIEL, DECIDEES, CAL.INDICE, CAL.FICHIER,',
     '    lus = {YP.REFERENTIEL, DECIDEES, CAL.FICHIER,', False),
    ("S9 un relevé par défaut", "E9", "rend 0 au lieu de 2", PROGRAMME,
     '    releves = [a.split("=", 1)[1] for a in opts if a.startswith("--releve=")]',
     '    releves = [a.split("=", 1)[1] for a in opts if a.startswith("--releve=")] or ["bruts_yahoo_21-10-2026"]\n    opts = opts or ["--releve=bruts_yahoo_21-10-2026"]', False),
    ("S10 un argument à valeur par défaut", "E10", "fabriquer(releve=", PROGRAMME,
     "def fabriquer(racine, releve):", "def fabriquer(racine, releve=\"bruts_yahoo_21-10-2026\"):", False),
    ("S11 table déposée : une ligne retirée", "E3", "manquent", TABLE, None, None, False),
    ("S12 (R6 adapté) veille prise deux séances avant", "E5", "rendement", PROGRAMME,
     "        veille = seances[i - 1] if i > 0 else None\n", "        veille = seances[i - 2] if i > 1 else None\n", False),
    ("S13 (R3 adapté) la date corrigée revient : LVMH à la séance suivante", "E5", "dividende(s) à cette date", PROGRAMME,
     "        lignes.append([x[\"valeur\"], x[\"mnemonique\"], x[\"source\"], x[\"date\"], ",
     "        lignes.append([x[\"valeur\"], x[\"mnemonique\"], x[\"source\"], seances[i + 1] if x[\"mnemonique\"] == \"MC\" else x[\"date\"], ",
     False),
    ("S14 (R2 adapté) clôture absente : rendement zéro", "E6", "vaut zéro", PROGRAMME,
     "        rendement = x[\"montant\"] / cs if cs else None\n", "        rendement = x[\"montant\"] / cs if cs else 0.0\n", False),
    ("S15 le refus des doublons retiré", "E11", "a) main rend 0", PROGRAMME,
     "        if len(sources) > 1:\n", "        if len(sources) > 99:\n", False),
    ("S16 le contrôle de la forme des dates retiré", "E11", "b) refusée pour une autre raison", PROGRAMME,
     "            bonne = bool(DATE_ECRITE.fullmatch(x[\"date\"])) and datetime.date.fromisoformat(x[\"date\"]) is not None\n",
     "            bonne = True\n", False),
    ("S17 le contrôle du signe des montants retiré", "E11", "d) acceptée", PROGRAMME,
     "        if not (math.isfinite(x[\"montant\"]) and x[\"montant\"] > 0):\n", "        if False:\n", False),
    ("S18 les distributions décidées échappent au contrôle", "E11", "a) main rend 0", PROGRAMME,
     "    controler_les_dividendes(divs + decidees, seances)\n", "    controler_les_dividendes(divs, seances)\n", False),
    ("S19 confrontation : clôture du jour au lieu de l'ouverture", "E12", "observée", CONFRONTATION,
     '    return float(b["open"]) / float(barres[seances[i - 1]]["close"]) - 1, b.get("source") or "non dite"',
     '    return float(b["close"]) / float(barres[seances[i - 1]]["close"]) - 1, b.get("source") or "non dite"', False),
    ("S20 confrontation : point milieu déplacé", "E12", "comptes par année et source", CONFRONTATION,
     "    return abs(observee) <= abs(observee - attendue)\n", "    return abs(observee) <= abs(observee - attendue) / 4\n", False),
    ("S21 confrontation : la dernière séance de la courbe jamais mesurée", "E12", "mesurable True", CONFRONTATION,
     "        elif not (debut < x[\"date\"] <= fin):\n", "        elif not (debut < x[\"date\"] < fin) or x[\"date\"] >= \"2026-04-30\":\n", False),
    # Tour 3 (superviseur R-759 du 05-11-2026 avant le tour 3, T1, T2, T8 ; X1, X2, X3 : programmes faussés du relecteur
    # du tour 2, qui laissaient l'épreuve verte).
    ("S22 la coupure du cours propre remise : dividendes d'après le 02-10-2026 oubliés", "E3", "manquent [('ACA', '2026-10-13'",
     PROGRAMME, "                d = YP.date_de_paris(t)\n",
     "                d = YP.date_de_paris(t)\n                if d > YP.COUPURE:\n                    continue\n", False),
    ("S23 la couverture écrite à la coupure du cours propre", "E5", "couverte_jusqu_au", PROGRAMME,
     "statut, x[\"couverte_jusqu_au\"]])", "statut, YP.COUPURE])", False),
    ("S24 confrontation : l'ancien témoin (un jour sans dividende)", "E12", "comptes par année et source", CONFRONTATION,
     'ne_baisse_pas(x["temoin"] + x["attendue"], x["attendue"])', 'ne_baisse_pas(x["temoin"], x["attendue"])', False),
    ("S25 (X1) confrontation : le rapport des moyennes ignore les hausses", "E12", "comptes par année et source",
     CONFRONTATION, '        obs = sum(x["observee"] for x in xs) / len(xs)\n',
     '        obs = sum(min(x["observee"], 0.0) for x in xs) / len(xs)\n', False),
    ("S26 (X2) confrontation : le témoin compte le jour du détachement", "E12", "comptes par année et source",
     CONFRONTATION, 'ne_baisse_pas(x["temoin"] + x["attendue"], x["attendue"])',
     'ne_baisse_pas(x["observee"], x["attendue"])', False),
    ("S27 (X3) confrontation : la séance d'avant prise dans les barres, pas dans le calendrier", "E12", "trou fabriqué",
     CONFRONTATION, "    i = bisect.bisect_left(seances, jour)\n    if i == 0",
     "    av = sorted(d for d in barres if d < jour)\n    if av and jour in barres and jour in seances:\n"
     "        return float(barres[jour][\"open\"]) / float(barres[av[-1]][\"close\"]) - 1, barres[jour].get(\"source\") or \"non dite\"\n"
     "    i = bisect.bisect_left(seances, jour)\n    if i == 0", False),
    ("S28 confrontation : la partie non couverte tue", "E12", "non couvert", CONFRONTATION,
     "        if apres:\n", "        if apres and False:\n", False),
    ("S29 confrontation : la couverture prise à la plus ancienne ligne", "E12", "non couvert", CONFRONTATION,
     '        couverture[r["mnemonique"]] = max(couverture.get(r["mnemonique"], ""), r["couverte_jusqu_au"])\n',
     '        couverture[r["mnemonique"]] = min(couverture.get(r["mnemonique"], "9"), r["couverte_jusqu_au"])\n', False),
]


def jouer(racine, seuls):
    """Joue les cas sur une racine et rend la liste des cas tombés.

    ① RÔLE — Le tour Z0 (ou un tour saboté, dans le sous-processus).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` · `seuls` : les noms des cas à jouer (tous si vide).
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : {cas : fautes} des cas tombés.
      [rend: 1]
    ⑥ TRAITEMENT — Charger les deux programmes, lire la table déposée, refaire la table une fois (`fabriquer`), relire
      les sources sans le programme si un cas en a besoin, jouer chaque cas dans un dossier temporaire — ceux de
      SUR_LES_DEUX_TABLES sur les deux tables ; une exception d'un cas est une faute de ce cas.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — —.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = charger(racine, PROGRAMME, "table_des_dividendes")
    m2 = charger(racine, CONFRONTATION, "confrontation_des_dividendes")
    entete, lignes = lire_table(os.path.join(racine, TABLE))
    try:
        refaites = [dict(zip(m.TABLE_DES_DIVIDENDES, r)) for r in m.fabriquer(racine, releve_de_la_table(m, lignes))]
        panne = None
    except Exception as e:  # noqa: BLE001 — la table refaite manque : chaque cas qui la lit tombe en le disant
        refaites, panne = None, f"table refaite impossible : {type(e).__name__} : {e}"
    src = sources_independantes(racine) if (not seuls or set(seuls) & AVEC_LES_SOURCES) else None
    tombes = {}
    with tempfile.TemporaryDirectory() as tmp:
        for nom, f in CAS:
            if seuls and nom not in seuls:
                continue
            os.makedirs(os.path.join(tmp, nom))
            plus = (src,) if nom in AVEC_LES_SOURCES else ()
            try:
                fautes = f(racine, m, m2, entete, lignes, os.path.join(tmp, nom), *plus)
                if nom in SUR_LES_DEUX_TABLES:
                    fautes = ["table déposée : " + x for x in fautes]
                    if refaites is None:
                        fautes.append(panne)
                    else:
                        fautes += ["table refaite : " + x for x in
                                   f(racine, m, m2, list(m.TABLE_DES_DIVIDENDES), refaites, os.path.join(tmp, nom), *plus)]
            except Exception as e:  # noqa: BLE001 — une panne d'un cas est une faute de ce cas
                fautes = [f"exception {type(e).__name__} : {e}"]
            print(f"{nom} {'juste' if not fautes else 'FAUX'}" + ("" if not fautes else " : " + " | ".join(map(str, fautes))[:4000]))
            if fautes:
                tombes[nom] = fautes
    return tombes


def saboter(racine):
    """Joue chaque sabotage dans un reflet de la racine et rend le nombre de sabotages qui ne mordent pas, ou None.

    ① RÔLE — Prouver que chaque cas a des dents.
    ② CONTEXTE D'APPEL — `main`, avec --saboter.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Z0 est juste.
    ⑤ SORTIE — UNE valeur : le nombre de sabotages qui ne
    mordent pas ; None si un sabotage ne s'applique plus.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque sabotage : reflet, modification du fichier (texte remplacé exactement une fois, ou, pour
      les données, ligne changée), réinscription au carnet si demandée, sous-processus de l'épreuve sur le reflet,
      limité au cas visé (--cas=) ; le sabotage mord si le sous-processus rend 1 ET que le cas visé tombe avec la
      faute attendue.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Instructions du projet §7.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Affiche ; dossiers effacés.
    ⑪ TERMINAISON — Rend la main ; chaque sous-processus a un délai de DELAI_S secondes, au-delà subprocess lève
    TimeoutExpired (attrapée par `main`, code 2).
      [sort: non]
    """
    rates = 0
    for nom, vise, faute, fichier, ancien, nouveau, reinscrire in SABOTAGES:
        with tempfile.TemporaryDirectory() as tmp:
            banc = os.path.join(tmp, "banc")
            refleter(racine, banc, {fichier, "donnees/PROVENANCE_DES_FICHIERS.csv"})
            p = os.path.join(banc, fichier)
            texte = open(p, encoding="utf-8").read()
            if ancien is not None:
                if texte.count(ancien) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS ({texte.count(ancien)} occurrences)")
                    return None
                texte = texte.replace(ancien, nouveau)
            elif fichier == TABLE and nom.startswith("S11"):
                texte = "\n".join(l for i, l in enumerate(texte.split("\n")) if i != 1)
            elif fichier == TABLE:
                l = texte.split("\n")
                c = l[1].split(",")
                c[4] = repr(float(c[4]) * 2)
                l[1] = ",".join(c)
                texte = "\n".join(l)
            else:
                texte = "\n".join(l for l in texte.split("\n") if "2010-10-07" not in l)
            open(p, "w", encoding="utf-8").write(texte)
            if reinscrire:
                inscrire_a_nouveau(banc, fichier)
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), banc, "--cas=" + vise],
                               capture_output=True, text=True, timeout=DELAI_S)
            tombe = any(l.startswith(vise + " FAUX") and faute in l for l in r.stdout.splitlines())
            mord = r.returncode == 1 and tombe
            print(f"{nom} → vise {vise} : {'mord' if mord else 'NE MORD PAS'} (code {r.returncode}) "
                  + " ".join(l.split(" :")[0] for l in r.stdout.splitlines() if " FAUX" in l))
            rates += 0 if mord else 1
    return rates


def main():
    """Point d'entrée.
    ① RÔLE — Lancer Z0 puis, sur demande, les sabotages.
    ② CONTEXTE D'APPEL — Ligne de commande.
    ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : le code 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Z0 ; s'il est juste et si --saboter, les sabotages.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — —.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Affiche le VERDICT.
    ⑪ TERMINAISON — Rend la main ; le bas du fichier sort par
    sys.exit.
      [sort: non]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = [a for a in sys.argv[1:] if a.startswith("--")]
    seuls = [o.split("=", 1)[1] for o in opts if o.startswith("--cas=")]
    autres = [o for o in opts if not o.startswith("--cas=")]
    if len(args) != 1 or autres not in ([], ["--saboter"]) or (seuls and autres) or any(c not in dict(CAS) for c in seuls):
        print("usage : <racine> [--saboter | --cas=E1]")
        return 2
    try:
        tombes = jouer(args[0], seuls)
        if tombes:
            print(f"VERDICT : {len(tombes)} cas faux")
            return 1
        if autres:  # --cas= seul ne lance pas les sabotages (défaut trouvé au tour 1 : le sous-processus les relançait)
            rates = saboter(args[0])
            if rates is None:
                print("VERDICT : L'ÉPREUVE N'A PAS PU JUGER — un sabotage ne s'applique plus")
                return 2
            if rates:
                print(f"VERDICT : {rates} sabotage(s) ne mordent pas")
                return 1
        print("VERDICT : tout est conforme")
        return 0
    except Exception as e:  # noqa: BLE001 — dernier filet : l'épreuve dit qu'elle n'a pas pu juger
        print(f"VERDICT : L'ÉPREUVE N'A PAS PU JUGER — {type(e).__name__} : {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
