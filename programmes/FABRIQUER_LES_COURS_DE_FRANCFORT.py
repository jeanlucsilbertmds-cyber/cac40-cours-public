#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FABRIQUER_LES_COURS_DE_FRANCFORT — Sam 24-10-2026 (Paris). Simulation uniquement.

① RÔLE — Refaire donnees/sources_francfort/COURS_DE_FRANCFORT.csv, les clôtures des actions du CAC 40 à la Bourse de
  Francfort du 03-01-2000 au 28-02-2017, depuis les 38 réponses brutes de Yahoo rangées au dépôt, et refuser toute
  réponse que le carnet de provenance n'inscrit pas telle qu'elle est.
② CONTEXTE D'APPEL — À la main, quand une réponse change ; et par son épreuve,
  tests/EPREUVES_DES_COURS_DE_FRANCFORT_Sam_24-10-2026.py. Importé par etudes/outils/CONFRONTER_A_FRANCFORT.py, qui
  télécharge les réponses et confronte les séances comblées : les deux lisent les réponses par les MÊMES fonctions
  (deux implémentations d'une même chose divergent toujours, R-708).
  python3 -I programmes/FABRIQUER_LES_COURS_DE_FRANCFORT.py <racine du dépôt> <fichier de sortie>
③ ENTRÉE — La racine : les réponses BRUTS/<symbole>.json et le carnet donnees/PROVENANCE_DES_FICHIERS.csv ; le chemin
  du fichier à écrire, hors de tout dépôt (verser dans le dépôt est un geste à part).
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le code de sortie : 0 si le fichier est écrit ; 1 si une réponse est refusée (absente, non inscrite au
  carnet, inscrite deux fois, d'une autre sorte que téléchargement, ou d'une autre empreinte) ; 2 si l'appel est mal
  formé, si la sortie est refusée, ou pour toute autre erreur (dernier filet de `main`). L'écran : « écrit : … » ou
  « REFUSÉ : … » ou « IMPOSSIBLE : … ».
  [rend: 1]
⑥ TRAITEMENT — Pour chaque valeur de SYMBOLES, dans l'ordre des noms « <valeur>__<symbole>.csv » : la réponse, vérifiée
  contre le carnet ; ses clôtures non vides et positives, datées par l'heure de chaque cotation plus deux heures ; les
  séances jusqu'au 28-02-2017, en ordre de date, chaque clôture arrondie à quatre décimales. Puis le fichier, au
  contrat COURS_DE_FRANCFORT, écrit d'un seul geste (fichier provisoire voisin, renommé).
⑦ UNITÉ — Des clôtures en devise de cotation de Francfort (euros) ; des dates de séance.
⑧ POURQUOI — Décision de Jean-Luc du 24-10-2026 à 22h41 (« 1 » à « Faire comme pour le cours de Yahoo : garder au dépôt
  les 38 réponses brutes, et séparer le programme en deux. Une partie fabrique les cours de Francfort à partir des
  réponses brutes, sans lire le fichier des 20 ans. L'autre fait la confrontation »). Jusque-là, l'outil
  etudes/outils/CONFRONTER_A_FRANCFORT.py écrivait ce fichier depuis des conversions non gardées, et lisait aussi le
  fichier des 20 ans : le contrôle de provenance K23 ne pouvait ni remonter les cours de Francfort à un téléchargement,
  ni accepter la boucle. La conversion reprend celle de l'outil sans rien changer (heure + 2 h, clôture > 0, arrondi à 4
  décimales, coupure au 28-02-2017, période de bnains) : mesuré le 24-10-2026, l'outil, relancé sur des réponses
  retéléchargées, refait le fichier du dépôt à l'octet (empreinte 38c3ce950f6dc815…).
⑨ CE QUI CLOCHE — « Plus deux heures » est l'heure d'été de Paris appliquée toute l'année, reprise telle quelle de
  l'outil : une cotation horodatée après 22h en hiver serait datée du lendemain ; aucune ne l'est dans les réponses
  du 24-10-2026 (le fichier refait est identique). · La garde des réponses contre le carnet est la même que celle de
  programmes/FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py, écrite une seconde fois ici (R-708 ; BACKLOG A-622). · SYMBOLES
  est écrit à la main (relevé le 07-10-2026) ; Pernod Ricard n'a que Xetra (« .DE ») et seulement depuis 2007.
⑩ EFFET — Lit la racine ; écrit le fichier de sortie (et un provisoire voisin, effacé en cas d'échec).
⑪ TERMINAISON — Rend la main ; aucun appel réseau ; sort par sys.exit.
  [sort: oui]
"""
import csv
import datetime
import hashlib
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import COURS_DE_FRANCFORT, TELECHARGEMENT  # noqa: E402  (R-708)

BRUTS = os.path.join("donnees", "sources_francfort", "bruts_yahoo_24-10-2026")
CARNET = os.path.join("donnees", "PROVENANCE_DES_FICHIERS.csv")
FIN_DE_BNAINS = "2017-02-28"
# La demande faite à Yahoo, reprise de l'outil : de 2000 (946684800) au 31-12-2026, heure de la machine de l'outil.
ADRESSE = "https://query2.finance.yahoo.com/v8/finance/chart/{symbole}?period1=946684800&period2={fin}&interval=1d"
# Les cotations de Francfort chez Yahoo (symbole « .F »), cherchées le 07-10-2026 ; Pernod Ricard n'a que Xetra
# (« .DE ») et seulement depuis décembre 2007.
SYMBOLES = {
    "ACCOR": "ACR.F", "AIR LIQUIDE": "AIL.F", "AIRBUS": "AIR.F", "AXA": "AXA.F", "BNP PARIBAS": "BNP.F",
    "BOUYGUES": "BYG.F", "BUREAU VERITAS": "4BV.F", "CAPGEMINI": "CGM.F", "CARREFOUR": "CAR.F",
    "CREDIT AGRICOLE SA": "XCA.F", "DANONE": "BSN.F", "DASSAULT SYSTEMES": "DSY.F", "EIFFAGE": "EF3.F",
    "ENGIE": "GZF.F", "ESSILORLUXOTTICA": "ESL.F", "EUROFINS SCIENTIFIC": "ESF0.DE", "EURONEXT": "ENXB.F",
    "HERMES INTL": "HMI.F", "KERING": "PPX.F", "L'OREAL": "LOR.F", "LEGRAND": "LRC.F", "LVMH": "MOH.F",
    "MICHELIN": "MCHA.F", "ORANGE": "FTE.F", "PERNOD RICARD": "PER.DE", "PUBLICIS GROUPE": "PUB.F",
    "RENAULT": "RNL.F", "SAFRAN": "SEJ1.F", "SAINT-GOBAIN": "GOB.F", "SANOFI": "SNW.F",
    "SCHNEIDER ELECTRIC": "SND.F", "SOCIETE GENERALE": "SGE.F", "STMICROELECTRONICS": "SGM.F", "THALES": "CSF.F",
    "TOTALENERGIES": "TOTB.F", "UNIBAIL-RODAMCO-WESTFIELD": "1BR1.F", "VEOLIA": "VVD.F", "VINCI": "SQU.F",
}


class Refus(Exception):
    """Un refus voulu : une réponse n'est pas celle qu'inscrit le carnet.

    ① RÔLE — Distinguer un refus décidé par la garde (code 1) d'une panne (code 2).
    ② CONTEXTE D'APPEL — Levée par `reponse_verifiee` ; attrapée par `main`.
    ③ ENTRÉE — Le texte du refus.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une panne ne doit pas passer pour un refus (superviseur R-759 du 22-10-2026, sur le cours de Yahoo).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
      [sort: non]
    """


def chemin_de(symbole):
    """Rend le chemin, depuis la racine, de la réponse brute d'un symbole.

    ① RÔLE — Le seul endroit où le nom d'une réponse se forme.
    ② CONTEXTE D'APPEL — `reponse_verifiee`, et l'outil qui télécharge les réponses.
    ③ ENTRÉE — `symbole` : un symbole de SYMBOLES.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin, avec « / ».
      [rend: 1]
    ⑥ TRAITEMENT — BRUTS/<symbole>.json.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le carnet inscrit des chemins écrits avec « / » ; un seul endroit les forme (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return os.path.join(BRUTS, symbole + ".json").replace(os.sep, "/")


def reponse_verifiee(racine, symbole, carnet):
    """Rend les octets d'une réponse, s'ils sont ceux que le carnet inscrit.

    ① RÔLE — Ne laisser passer qu'une réponse identique, à l'octet, à celle que le carnet inscrit.
    ② CONTEXTE D'APPEL — `clotures_de_toutes_les_valeurs`, une fois par valeur.
    ③ ENTRÉE — `racine` · `symbole` · `carnet` : les lignes du carnet.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les octets de la réponse.
      [rend: 1]
    ⑥ TRAITEMENT — La réponse doit exister ; le carnet doit porter exactement une ligne de son chemin, de sorte
      TELECHARGEMENT, à son empreinte.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Une seule propriété, l'empreinte inscrite au carnet, comme pour le cours de Yahoo.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme (garde écrite deux fois).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève Refus.
      [sort: non]
    """
    chemin = chemin_de(symbole)
    p = os.path.join(racine, chemin)
    if not os.path.isfile(p):
        raise Refus(f"{symbole} : réponse absente ({chemin})")
    octets = open(p, "rb").read()
    lignes = [r for r in carnet if r["fichier"] == chemin]
    if len(lignes) != 1:
        raise Refus(f"{symbole} : inscrit {len(lignes)} fois au carnet, au lieu d'une")
    if lignes[0]["produit_par"] != TELECHARGEMENT:
        raise Refus(f"{symbole} : inscrit au carnet comme « {lignes[0]['produit_par']} », pas comme téléchargement")
    if hashlib.sha256(octets).hexdigest() != lignes[0]["sha256"]:
        raise Refus(f"{symbole} : empreinte différente de celle du carnet")
    return octets


def clotures(octets):
    """Rend les clôtures d'une réponse de Yahoo, par date.

    ① RÔLE — La conversion d'une réponse en clôtures, telle que l'outil de Francfort la faisait.
    ② CONTEXTE D'APPEL — `clotures_de_toutes_les_valeurs`.
    ③ ENTRÉE — `octets` : la réponse.
    ④ CONDITIONS D'ENTRÉE — Elle se lit en JSON et porte chart.result[0], ses horodatages et ses clôtures.
    ⑤ SORTIE — UNE valeur : {date ISO : clôture}, sans clôture vide ni nulle ou négative.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque horodatage, dans l'ordre : sauter une clôture vide ; dater par l'heure en temps universel
      plus deux heures ; garder la clôture si elle est positive (une date vue deux fois garde la dernière).
    ⑦ UNITÉ — Des clôtures et des dates de séance.
    ⑧ POURQUOI — L'outil écrivait chaque clôture dans un fichier CSV (str d'un nombre à virgule), puis la relisait
      (float) : l'aller-retour rend le même nombre, la conversion directe est donc la même.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme (« plus deux heures »).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; une réponse mal formée lève une erreur.
      [sort: non]
    """
    r = json.loads(octets.decode("utf-8"))["chart"]["result"][0]
    fermes = r["indicators"]["quote"][0]["close"]
    sortie = {}
    for i, t in enumerate(r.get("timestamp") or []):
        if fermes[i] is None:
            continue
        jour = (datetime.datetime.fromtimestamp(t, datetime.timezone.utc) + datetime.timedelta(hours=2)).date()
        if fermes[i] > 0:
            sortie[jour.isoformat()] = fermes[i]
    return sortie


def clotures_de_toutes_les_valeurs(racine):
    """Rend, pour chaque valeur, son symbole et ses clôtures, chaque réponse vérifiée contre le carnet.

    ① RÔLE — Lire les 38 réponses, une fois, pour ce programme et pour l'outil de confrontation.
    ② CONTEXTE D'APPEL — `fabriquer`, et etudes/outils/CONFRONTER_A_FRANCFORT.py.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des (valeur, symbole, {date : clôture}), dans l'ordre des noms
      « <valeur>__<symbole>.csv » (l'ordre de l'outil).
      [rend: 1]
    ⑥ TRAITEMENT — Lire le carnet ; pour chaque valeur de SYMBOLES : `reponse_verifiee`, puis `clotures`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'ordre des lignes du fichier est celui de l'outil, qui listait ses fichiers par leur nom.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le carnet et les réponses.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    with open(os.path.join(racine, CARNET), encoding="utf-8", newline="") as f:
        carnet = list(csv.DictReader(f))
    ordre = sorted(SYMBOLES.items(), key=lambda vs: f"{vs[0]}__{vs[1]}.csv")
    return [(v, s, clotures(reponse_verifiee(racine, s, carnet))) for v, s in ordre]


def fabriquer(racine):
    """Rend les octets du fichier des cours de Francfort.

    ① RÔLE — Le fichier entier, en mémoire.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les octets.
      [rend: 1]
    ⑥ TRAITEMENT — L'en-tête COURS_DE_FRANCFORT, puis, valeur après valeur, chaque séance jusqu'à FIN_DE_BNAINS, en ordre
      de date, la clôture arrondie à quatre décimales et écrite par repr.
    ⑦ UNITÉ — Des clôtures en euros.
    ⑧ POURQUOI — Voir le ⑧ du programme : la forme de l'outil, à l'identique.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit la racine.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    t = io.StringIO()
    w = csv.writer(t, lineterminator="\n")
    w.writerow(COURS_DE_FRANCFORT)
    for v, s, c in clotures_de_toutes_les_valeurs(racine):
        w.writerows([v, s, d, repr(round(x, 4))] for d, x in sorted(c.items()) if d <= FIN_DE_BNAINS)
    return t.getvalue().encode("utf-8")


def main(argv):
    """Le point d'entrée.

    ① RÔLE — Vérifier l'appel, fabriquer, écrire d'un seul geste.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la racine et le fichier de sortie.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir le ⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — Refuser une sortie qui existe déjà ou qui est sous la racine ; `fabriquer` ; écrire dans un fichier
      provisoire voisin, puis le renommer ; afficher l'empreinte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Verser au dépôt est un geste à part (comme pour le cours de Yahoo, relecteur du 22-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le fichier de sortie.
    ⑪ TERMINAISON — Rend la main ; toute erreur imprévue rend 2.
      [sort: non]
    """
    if len(argv) != 2:
        print("IMPOSSIBLE : usage — FABRIQUER_LES_COURS_DE_FRANCFORT.py <racine du dépôt> <fichier de sortie>")
        return 2
    racine, sortie = (os.path.realpath(a) for a in argv)
    if os.path.exists(sortie) or os.path.commonpath([sortie, racine]) == racine:
        print("IMPOSSIBLE : la sortie existe déjà, ou elle est sous la racine : verser est un geste à part")
        return 2
    provisoire = None
    try:
        octets = fabriquer(racine)
        fd, provisoire = tempfile.mkstemp(prefix=os.path.basename(sortie) + ".en_cours.", dir=os.path.dirname(sortie))
        with os.fdopen(fd, "wb") as f:
            f.write(octets)
        os.rename(provisoire, sortie)
    except Refus as e:
        print(f"REFUSÉ : {e}")
        return 1
    except Exception as e:                                # dernier filet : une panne n'est pas un refus
        if provisoire is not None and os.path.exists(provisoire):
            os.remove(provisoire)
        print(f"IMPOSSIBLE : {type(e).__name__} — {e}")
        return 2
    n = octets.count(b"\n") - 1
    print(f"écrit : {sortie} · {n} clôtures · sha256 {hashlib.sha256(octets).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
