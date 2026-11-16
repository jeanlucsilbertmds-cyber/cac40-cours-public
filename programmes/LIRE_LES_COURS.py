#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LIRE_LES_COURS — Sam 10-10-2026 (Paris) — le programme unique qui lit les cours pour tous les autres (R-111).
Simulation uniquement.

① RÔLE — Lire un fichier de cours (par défaut donnees/cours_maitre.csv) et le rendre aux autres programmes sous une
  forme commune : chaque barre rangée sous le MNÉMONIQUE de sa valeur, jamais sous son nom ; chaque séance du
  calendrier (R-110) sans cours relevée comme un TROU ; chaque anomalie de lecture signalée. Il ne change aucun cours.
② CONTEXTE D'APPEL — Importé par les programmes qui ont besoin des cours (aucun ne l'importe encore le 10-10-2026 :
  la bascule de chacun est une action à part, A-566). Lancé seul, il lit le fichier et affiche ce qu'il signale :
  python3 programmes/LIRE_LES_COURS.py [racine] [fichier des cours, relatif à la racine].
③ ENTRÉE — Sous la racine du dépôt : le fichier des cours (contrat COURS_MAITRE : valeur, date, open, high, low,
  close, volume, source) ; le référentiel des valeurs (donnees/REFERENTIEL_VALEURS_*.csv, le plus récent par la date
  de son nom) ; le calendrier des séances (programmes/CALENDRIER_DE_LA_BOURSE.py) ; donnees/NATURE_DES_TROUS.csv
  (contrat NATURE_DES_TROUS) ; les deux tables de la règle I-3, donnees/sources_indice/PASSAGES_DANS_LE_CAC40.csv et
  IDENTITES_DES_SOCIETES.csv — exigées pour TOUT fichier de cours, même figé.
④ CONDITIONS D'ENTRÉE — Voir chaque fonction. Un fichier absent ou mal formé arrête la lecture (OSError, ValueError),
  jamais ne la fausse.
⑤ SORTIE — Voir chaque fonction. Lancé seul : le code 0 quand rien n'est à signaler, 1 quand quelque chose l'est,
  2 quand la lecture n'a pas pu se faire (R-734).
⑥ TRAITEMENT — ① relier chaque écriture d'un nom à son mnémonique, par le référentiel · ② lire le calendrier des
  séances · ③ lire les cours, ranger chaque barre sous son mnémonique, écarter et signaler ce qui ne peut pas être
  rangé · ④ lire la nature des trous · ⑤ à la demande, calculer les trous d'une valeur et ses dernières séances.
⑦ UNITÉ — Des SÉANCES du calendrier, jamais des lignes du fichier ; les cours sont rendus tels qu'écrits (du texte).
⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 (R-111, « Oui, telle quelle » ; construction approuvée le même jour,
  « Oui, vas-y »). Relevé le 10-10-2026 : 17 programmes de programmes/ nomment le fichier des cours ou la référence
  Google, chacun lisant à sa façon ; un calcul « sur les 14 dernières lignes » enjambe un trou sans le dire (Vinci,
  séance du 03-07-2026 retirée d'une copie : le CMF passe de −0,136 à −0,087, mesuré par Cowork) ; 13 valeurs sont
  écrites de deux façons dans donnees/cours_maitre.csv (« AIR LIQUIDE » 644 lignes, « AIR_LIQUIDE » 65), mesuré par ce
  module le 10-10-2026 — le relevé de Cowork du même jour en dit 14.
⑨ CE QUI CLOCHE — Aucun programme ne passe encore par ce module. · Les séances postérieures au dernier jour de
  l'indice (02-10-2026 le 10-10-2026) ne sont que PRÉVUES par la liste d'Euronext. · Les barres ne sont pas jugées
  (barre impossible, plate, recopiée : lignes B de la table de réception, à venir). · Le rapprochement des écritures
  passe par `COMMUN.norm_valeur`, qui rend équivalents espaces, tirets et soulignés : « AIR-LIQUIDE » serait reconnu
  comme Air Liquide ; une autre faute de frappe ne l'est pas, et elle est signalée.
⑩ EFFET — Lit des fichiers. N'écrit rien. Lancé seul, affiche.
⑪ TERMINAISON — Rend la main ; lancé seul, sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import csv
import hashlib
import importlib.util
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER_DES_COURS = os.path.join("donnees", "cours_maitre.csv")
FICHIER_DES_NATURES = os.path.join("donnees", "NATURE_DES_TROUS.csv")
CHAMPS_DE_LA_BARRE = ("open", "high", "low", "close", "volume")
COLONNES_DES_NOMS = ("nom_usuel", "onglet_google")
VIDES = ("", "—", "-")
NON_DECIDEE = "NON DÉCIDÉE"
# Les deux tables de la règle I-3 (décision de Jean-Luc du 11-10-2026) : depuis quand chaque société était dans le
# CAC 40, et sous quels codes ISIN. Lues pour la cassure B de Cowork (11-10-2026, e183c98) : une valeur dans l'indice
# avant sa première barre doit avoir ses trous (décision de Jean-Luc A8, 10-10-2026 : ces séances sont marquées).
PASSAGES = os.path.join("donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv")
IDENTITES = os.path.join("donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv")
NOMBRE = re.compile(r"[-+]?\d+(\.\d*)?([eE][-+]?\d+)?")   # un nombre écrit simplement : ni « 1_000 », ni « inf »
PREAVIS_DU_CALENDRIER = 30   # jours avant la fin de la liste d'Euronext où son relevé manquant est signalé (R-110 ②)


def _charger(nom):
    """Importe un programme de ce dossier par son chemin.

    ① RÔLE — Charger le calendrier, les contrats et COMMUN depuis le dossier de ce module, quel que soit le dossier
      courant.
    ② CONTEXTE D'APPEL — À l'import de ce module, trois fois.
    ③ ENTRÉE — `nom` : le nom du fichier, sans « .py ».
    ④ CONDITIONS D'ENTRÉE — Le fichier est dans le même dossier que ce module.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, par le chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves copient ce module avec ses voisins dans un dossier jetable : un import par le chemin y
      trouve les voisins copiés, et non ceux du dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le fichier chargé (des déclarations seulement, pour les trois).
    ⑪ TERMINAISON — Rend la main ou lève l'erreur d'import.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(f"{nom}_lc_{id(ICI)}", os.path.join(ICI, nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CAL = _charger("CALENDRIER_DE_LA_BOURSE")
CONTRATS = _charger("CONTRATS_DES_FICHIERS")
COMMUN = _charger("COMMUN")


def _lire_csv(chemin, contrats, quoi):
    """Lit un CSV dont l'en-tête doit être exactement l'un des contrats admis.

    ① RÔLE — Une seule lecture confrontée au contrat, pour les trois fichiers de ce module.
    ② CONTEXTE D'APPEL — `table_des_ecritures`, `lire_les_natures`, `lire`.
    ③ ENTRÉE — `chemin` : le fichier · `contrats` : les en-têtes admis (un tuple de listes de colonnes), ou None pour
      ne pas exiger d'en-tête exact · `quoi` : le nom du fichier dans les messages.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (OSError sinon), en UTF-8 ; une marque d'ordre d'octets d'Excel est
      tolérée.
    ⑤ SORTIE — DEUX valeurs : l'en-tête lu, et la liste des lignes, chacune un dictionnaire. Lève ValueError pour un en-tête faux, une ligne
      au nombre de cases différent de l'en-tête, ou un CSV que le lecteur ne sait pas lire (csv.Error, par exemple une
      case de plus de 131 072 caractères).
      [rend: 2]
    ⑥ TRAITEMENT — lire l'en-tête, le confronter, lire les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Ce qui se partage se déclare » : chaque bout se confronte au contrat, le lecteur comme l'écrivain.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        try:
            entete = next(r, None)
            if entete is None or (contrats is not None and entete not in [list(c) for c in contrats]):
                raise ValueError(f"{quoi} : en-tête {entete} au lieu de l'un des contrats {list(contrats or [])}")
            out = []
            for n, l in enumerate(r, start=2):
                if not l:
                    continue
                if len(l) != len(entete):
                    raise ValueError(f"{quoi}, ligne {n} : {len(l)} cases au lieu de {len(entete)}")
                out.append(dict(zip(entete, l)))
        except csv.Error as e:
            raise ValueError(f"{quoi} : CSV illisible, {e}")
    return entete, out


def table_des_ecritures(racine):
    """Relie chaque écriture connue d'un nom de valeur à son mnémonique, par le référentiel.

    ① RÔLE — Le seul endroit de ce module où un nom rencontre un code (chapitre de l'identité, I-3 et I-4).
    ② CONTEXTE D'APPEL — `lire`, une fois par lecture.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Un fichier donnees/REFERENTIEL_VALEURS_*.csv au moins, avec les colonnes nom_usuel,
      onglet_google, mnemonique et hors_univers ; chaque ligne porte un mnémonique.
    ⑤ SORTIE — DEUX valeurs : la table {écriture rapprochée par COMMUN.norm_valeur : mnémonique}, et la table
      {mnémonique : motif hors univers, vide sinon}.
      [rend: 2]
    ⑥ TRAITEMENT — ① prendre le référentiel le plus récent par la date de son nom (COMMUN.le_plus_recent, comme la
      collecte du soir) · ② pour chaque ligne, rapprocher le nom usuel et le nom d'onglet · ③ refuser qu'une même
      écriture rapprochée désigne deux mnémoniques.
    ⑦ UNITÉ — Des écritures, pas des valeurs : une valeur en apporte une ou deux.
    ⑧ POURQUOI — R-111 ③ : une valeur se reconnaît à son mnémonique, jamais à son nom. Le nom officiel d'Euronext n'est
      pas pris : relevé le 10-10-2026, il vaut « non visible dans l extrait public Euronext » pour plusieurs valeurs,
      qui désignerait donc plusieurs mnémoniques. Les anciens noms ne sont pas pris : ils décrivent une autre société
      (E2 : jamais de réunion par le nom). Le mnémonique lui-même n'est PAS une écriture admise dans la colonne `valeur`
      d'un fichier de cours : relecture indépendante du 10-10-2026, une ligne « CA » (l'abréviation courante de Crédit
      Agricole) était rangée sous Carrefour, dont le mnémonique est CA ; aucun fichier de cours n'écrit de mnémonique
      (relevé le même jour sur donnees/cours_maitre.csv et l'historique réparé).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le dossier donnees/ et un fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    d = os.path.join(racine, "donnees")
    cands = [f for f in os.listdir(d) if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    if not cands:
        raise OSError("référentiel des valeurs introuvable dans donnees/")
    _, lignes = _lire_csv(os.path.join(d, COMMUN.le_plus_recent(cands)), None, "référentiel")
    table, hors = {}, {}
    for n, r in enumerate(lignes, start=2):
        if any(c not in r for c in COLONNES_DES_NOMS + ("hors_univers",)):
            raise ValueError("référentiel : colonne manquante parmi " + ", ".join(COLONNES_DES_NOMS + ("hors_univers",)))
        m = r["mnemonique"].strip()
        if m in VIDES:
            raise ValueError(f"référentiel, ligne {n} : pas de mnémonique pour « {r['nom_usuel']} »")
        hors[m] = r["hors_univers"].strip()
        for c in COLONNES_DES_NOMS:
            e = r[c].strip()
            if e in VIDES:
                continue
            k = COMMUN.norm_valeur(e)
            if table.get(k, m) != m:
                raise ValueError(f"référentiel : l'écriture « {e} » désigne {table[k]} et {m}")
            table[k] = m
    return table, hors


def lire_les_natures(racine, hors_univers):
    """Lit la nature décidée de chaque trou.

    ① RÔLE — R-111 ⑤ : garder à part la seule chose qui ne se calcule pas sur un trou.
    ② CONTEXTE D'APPEL — `lire`, une fois par lecture.
    ③ ENTRÉE — `racine` : la racine du dépôt · `hors_univers` : la table des mnémoniques connus (seconde sortie de
      `table_des_ecritures`).
    ④ CONDITIONS D'ENTRÉE — donnees/NATURE_DES_TROUS.csv existe, en-tête exactement le contrat NATURE_DES_TROUS ;
      chaque mnémonique est connu du référentiel, chaque date s'écrit AAAA-MM-JJ, chaque nature est l'une de
      NATURES_DES_TROUS, la preuve, `decide_par` et `le` ne sont pas vides, et un couple (mnémonique, date) n'est écrit
      qu'une fois. Que la date soit une séance est vérifié par `lire`, qui a le calendrier.
    ⑤ SORTIE — UNE valeur : le dictionnaire {(mnémonique, date) : (nature, preuve)}.
      [rend: 1]
    ⑥ TRAITEMENT — lire, confronter chaque ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une nature sans preuve, sur une valeur inconnue, ou dont on ne sait pas qui l'a décidée, ne vaut rien :
      elle est refusée (R-109 : c'est Jean-Luc qui décide).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    out = {}
    for n, r in enumerate(_lire_csv(os.path.join(racine, FICHIER_DES_NATURES), (CONTRATS.NATURE_DES_TROUS,),
                                    "nature des trous")[1], start=2):
        if r["mnemonique"] not in hors_univers:
            raise ValueError(f"nature des trous, ligne {n} : mnémonique inconnu « {r['mnemonique']} »")
        try:
            d = CAL._date_stricte(r["date"])
        except ValueError:
            raise ValueError(f"nature des trous, ligne {n} : date illisible « {r['date']} »")
        if r["nature"] not in CONTRATS.NATURES_DES_TROUS:
            raise ValueError(f"nature des trous, ligne {n} : nature inconnue « {r['nature']} »")
        if not r["preuve"].strip():
            raise ValueError(f"nature des trous, ligne {n} : pas de preuve")
        if not r["decide_par"].strip() or not r["le"].strip():
            raise ValueError(f"nature des trous, ligne {n} : qui a décidé, et quand, n'est pas écrit")
        if (r["mnemonique"], d) in out:
            raise ValueError(f"nature des trous, ligne {n} : {r['mnemonique']} le {r['date']} est écrit deux fois")
        out[(r["mnemonique"], d)] = (r["nature"], r["preuve"])
    return out


FORME_ISIN = re.compile(r"[A-Z]{2}[A-Z0-9]{9}[0-9]")


def isin_valide(code):
    """Dit si un code a la forme d'un ISIN et une clé juste.

    ① RÔLE — Reconnaître un code ISIN mal écrit avant qu'il ne détache un passage de sa société.
    ② CONTEXTE D'APPEL — `lire_les_passages`, pour chaque code non vide des deux tables ; les épreuves.
    ③ ENTRÉE — `code` : le texte tel qu'écrit dans la table, sans rien retirer.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si le code a douze caractères — deux lettres capitales, neuf lettres capitales ou
      chiffres, un chiffre — et si ce dernier chiffre est la clé.
      [rend: 1]
    ⑥ TRAITEMENT — ① la forme, exactement (une espace, une minuscule : faux) · ② la clé, norme ISO 6166 : chaque lettre
      devient son rang plus neuf (A = 10 … Z = 35), on garde tous les chiffres sauf le dernier, et l'algorithme de Luhn
      doit donner le dernier chiffre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture de Cowork du 13-10-2026 (15e647c, cassure H) : le code de STMicroelectronics écrit avec une
      espace, ou en minuscules, n'était plus celui de sa société ; il passait pour celui d'une société sortie de
      l'indice, et les 423 trous de STMicroelectronics disparaissaient sans un mot. La forme et la clé sont une
      propriété du code : aucune liste à tenir. Calibré sur Accor : FR0000120404 vrai, FR0000120405 faux.
    ⑨ CE QUI CLOCHE — Un code bien formé mais d'une AUTRE société passe : seule la relecture de la table l'empêche.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not FORME_ISIN.fullmatch(code):
        return False
    chiffres = "".join(str(int(c, 36)) for c in code[:-1])
    somme = 0
    for i, c in enumerate(reversed(chiffres)):
        n = int(c) * (2 if i % 2 == 0 else 1)
        somme += n - 9 if n > 9 else n
    return (10 - somme % 10) % 10 == int(code[-1])


def presence_des_societes_sorties_sans_cle(ident, passages, seances, debut, fin):
    """Rend, pour chaque société sortie SANS clé de lecture, ses séances de présence dans l'indice entre deux dates.

    ① RÔLE — Compter à part ce que le lecteur ne peut pas lire : une société sortie dont aucune barre ne se range, faute
      de mnémonique (« non trouvé »), reste visible par sa présence dans l'indice.
    ② CONTEXTE D'APPEL — `lire`, pour un fichier déclaré porter les sociétés sorties.
    ③ ENTRÉE — `ident`, `passages` : les lignes des deux tables de la règle I-3 · `seances` : le calendrier
      (CAL.lire_les_seances) · `debut`, `fin` : les bornes du fichier (dates).
    ④ CONDITIONS D'ENTRÉE — Les dates des passages se lisent (`lire_les_passages` l'a déjà exigé).
    ⑤ SORTIE — UNE valeur : {numéro : (société, nombre de séances, première, dernière)} pour chaque société sans ligne
      ouverte et absente de `societes_sorties`, présente au moins une séance entre `debut` et `fin`.
      [rend: 1]
    ⑥ TRAITEMENT — ① les sociétés sorties : aucune ligne sans `fin` · ② sans clé : absentes de `societes_sorties` ·
      ③ leurs codes ISIN (toutes lignes) · ④ les passages de ces codes, bornés à [debut, fin], en séances du calendrier.
    ⑦ UNITÉ — Des séances du calendrier.
    ⑧ POURQUOI — D1 du relecteur QE2 (14-11-2026) : 20 sociétés sorties « non trouvé » (Dexia, Lagardère, AGF…),
      19 813 séances de présence, comptées nulle part ; avec TechnipFMC (D3), 811 de plus (mesuré : 811 au calendrier comme aux dates de l'indice, Q-6 de Cowork). Superviseur R-759 du
      14-11-2026, liste fermée ① : compter à part, par une propriété des deux tables, pas par `dans_l_indice`.
      K-4 de Cowork (14-11-2026) : toute anomalie de la table des identités y est fatale, parce que le compte de
      présence dépend de toute la table ; le message le dit, pour ne pas laisser croire à la tolérance de `lire` (I-1).
    ⑨ CE QUI CLOCHE — Ces séances ne sont PAS des trous de `trous` : aucune clé ne les porte. Leur versement (barres N3
      déjà gardées pour 19 d'entre elles) est au BACKLOG, A-829 (B1 ; K-6 de Cowork).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève ValueError sur toute anomalie de la table des identités (motif : fichier
      déclaré). Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    ouvertes = {r["numero"] for r in ident if not r["fin"]}
    try:
        avec_cle = {n for n, _ in societes_sorties(ident).values()}
    except ValueError as e:
        # K-4 de Cowork (14-11-2026) : le comportement ne change pas — toute anomalie y reste fatale ; le motif se dit
        raise ValueError(f"{e} — fichier déclaré porter les sociétés sorties "
                         f"(CONTRATS.FICHIERS_DE_COURS_QUI_PORTENT_LES_SOCIETES_SORTIES) : son compte de présence "
                         f"dépend de toute la table des identités, toute anomalie d'identité y est fatale") from None
    codes, nom = defaultdict(set), {}
    for r in ident:
        if r["numero"] not in ouvertes and r["numero"] not in avec_cle:
            nom.setdefault(r["numero"], r["societe"])
            if r["isin"]:
                codes[r["numero"]].add(r["isin"])
    out = {}
    for numero in sorted(nom, key=lambda x: int(x) if x.isdigit() else 0):
        jours = set()
        for p in passages:
            if p["isin_bnains"] in codes[numero]:
                a = max(CAL._date_stricte(p["premiere_seance"]), debut)
                b = min(CAL._date_stricte(p["derniere_seance"]) if p["derniere_seance"] else fin, fin)
                if a <= b:
                    jours |= {d for d, _ in CAL.seances_entre(a, b, seances)}
        if jours:
            out[numero] = (nom[numero], len(jours), min(jours), max(jours))
    return out


def societes_sorties(ident, anomalies=None):
    """Rend le mnémonique de chaque société SORTIE de l'indice, lu dans la table des identités.

    ① RÔLE — Dire, en un seul endroit, sous quel mnémonique une société qui n'est plus cotée dans le CAC 40 est
      reconnue : par la lecture des cours (`lire`, ses barres) et par `lire_les_passages` (ses périodes dans l'indice).
    ② CONTEXTE D'APPEL — `lire`, une fois par lecture ; `lire_les_passages`, une fois.
    ③ ENTRÉE — `ident` : les lignes de donnees/sources_indice/IDENTITES_DES_SOCIETES.csv, chacune un dictionnaire sous
      le contrat CONTRATS.IDENTITES_DES_SOCIETES (rendu de `_lire_csv`) · `anomalies` : None (lever), ou une liste où
      ranger les anomalies.
    ④ CONDITIONS D'ENTRÉE — La date `fin` de chaque ligne d'une société sortie s'écrit AAAA-MM-JJ ; deux lignes d'une
      même société sortie ne finissent pas le même jour sous deux mnémoniques différents, et deux sociétés sorties n'ont
      pas le même mnémonique. Sinon : ValueError avec la société, OU, quand `anomalies` est une liste (`lire`, depuis le
      14-11-2026, I-1 de Cowork), l'anomalie (numéros, texte) y est ajoutée et la société sort du rendu.
    ⑤ SORTIE — UNE valeur : {mnémonique : (numéro de la société, date de fin de sa dernière ligne)}. Exemple réel du
      14-11-2026 : « UG » → (« 48 », 2021-01-15), Peugeot S.A. ; 18 mnémoniques sur la vraie table.
      [rend: 1]
    ⑥ TRAITEMENT — ① une société est SORTIE quand AUCUNE de ses lignes n'est sans `fin` (une ligne sans `fin` dit son
      nom d'aujourd'hui : `lire_les_passages`) · ② sa dernière ligne est celle dont la `fin` est la plus tardive ;
      son mnémonique, espaces de bord retirés, est celui de la société · ③ un mnémonique vide (VIDES) ou
      CONTRATS.MNEMONIQUE_NON_TROUVE ne désigne rien : la société n'est pas rendue.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — A-713 ① (QE), superviseur R-759 du 14-11-2026 (SUPERVISEUR_LU_TOUR7_Sam_14-11-2026) : le lecteur ne
      connaissait que les 40 valeurs du référentiel et les sociétés sans date de fin ; les 18 sociétés sorties, que
      l'assemblage des 20 ans écrit sous leur mnémonique (décision de Jean-Luc du 11-11-2026 à 22h26), étaient des
      « noms sans mnémonique » : 68 391 lignes mises à part sur le témoin installé, et le juge refusait tout le fichier.
      Reconnues par une PROPRIÉTÉ de la table (aucune ligne ouverte), jamais par une liste : une société qui sort
      demain y entre d'elle-même quand sa ligne reçoit sa date de fin. La dernière ligne, comme le nom d'aujourd'hui
      d'une société cotée : Alstom (42) a deux lignes, « non trouvé » jusqu'au 2002-04-02 puis ALO jusqu'au
      2024-03-15 — ALO.
    ⑨ CE QUI CLOCHE — Une société sortie dont la DERNIÈRE ligne porte « non trouvé » mais une ligne plus ancienne un
      vrai mnémonique n'est pas rendue : ses barres seraient « sans mnémonique », mises à part et signalées — le sens
      sûr, aucun cas sur la vraie table au 14-11-2026. · Une barre écrite sous un AUTRE mnémonique de la société que
      celui de sa dernière ligne n'est pas reconnue (même sens sûr ; l'assemblage écrit le mnémonique de la ligne qui
      couvre la date, `cle_d_une_societe_sortie`, et chaque société sortie n'a qu'un vrai mnémonique au 14-11-2026).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    ecartees = set()

    def refuser(numeros, texte):
        """Lève l'anomalie d'identité, ou la range et retire la ou les sociétés en cause du rendu.

        ① RÔLE — Un seul endroit où `societes_sorties` dit une anomalie de la table des identités.
        ② CONTEXTE D'APPEL — `societes_sorties`, à chaque anomalie (fin illisible, deux dernières lignes, un mnémonique
          pour deux sociétés sorties).
        ③ ENTRÉE — `numeros` : les numéros des sociétés en cause · `texte` : le message.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Ne rend rien.
          [rend: rien]
        ⑥ TRAITEMENT — sans liste d'anomalies : lever ValueError(texte) ; sinon ajouter (numéros, texte) à la liste et
          les numéros aux sociétés écartées du rendu.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — I-1 de Cowork (14-11-2026) : une faute dans IDENTITES sur une société sortie arrêtait la lecture du
          maître, où elle n'a aucune barre ; `lire` décide désormais si l'anomalie touche une valeur écrite dans le fichier.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie `anomalies` et l'ensemble des sociétés écartées.
        ⑪ TERMINAISON — Rend la main ou lève ValueError. Aucun de mes appels ne peut ne pas revenir.
          [sort: non]
        """
        if anomalies is None:
            raise ValueError(texte)
        anomalies.append((tuple(numeros), texte))
        ecartees.update(numeros)

    ouvertes = {r["numero"] for r in ident if not r["fin"]}
    derniere = {}
    for r in ident:
        if r["numero"] in ouvertes:
            continue
        try:
            fin = CAL._date_stricte(r["fin"])
        except ValueError:
            refuser([r["numero"]], f"identités : date de fin illisible « {r['fin']} » pour la société {r['numero']} "
                                   f"({r['societe']})")
            continue
        m = r["mnemonique"].strip()
        avant = derniere.get(r["numero"])
        if avant is not None and avant[0] == fin and avant[1] != m:
            refuser([r["numero"]], f"identités : la société sortie {r['numero']} ({r['societe']}) a deux dernières "
                                   f"lignes le {fin}, sous {avant[1]} et {m}")
        if avant is None or fin > avant[0]:
            derniere[r["numero"]] = (fin, m)
    out = {}
    for numero, (fin, m) in sorted(derniere.items()):
        if m in VIDES or m == CONTRATS.MNEMONIQUE_NON_TROUVE:
            continue
        if m in out:
            refuser([out[m][0], numero], f"identités : le mnémonique {m} désigne deux sociétés sorties ({out[m][0]} et "
                                         f"{numero})")
            continue
        out[m] = (numero, fin)
    return {m: v for m, v in out.items() if v[0] not in ecartees}


def lire_les_passages(racine, anomalies=None):
    """Rend, pour chaque mnémonique d'aujourd'hui ou de société sortie, les périodes où sa société était dans le CAC 40.

    ① RÔLE — Dire depuis quand une valeur est attendue, sans le déduire de ses cours (cassure B de Cowork).
    ② CONTEXTE D'APPEL — `lire`, une fois par lecture ; les épreuves de l'arrivée des signaux.
    ③ ENTRÉE — `racine` : la racine du dépôt, qui porte PASSAGES et IDENTITES · `anomalies` : transmise à
      `societes_sorties` (None : une anomalie d'une société sortie lève).
    ④ CONDITIONS D'ENTRÉE — Les deux fichiers existent, chacun sous son contrat (CONTRATS.PASSAGES_DANS_LE_CAC40,
      CONTRATS.IDENTITES_DES_SOCIETES) ; une société a au plus une ligne d'identité sans date de fin (son nom
      d'aujourd'hui) ; deux sociétés n'ont pas le même mnémonique d'aujourd'hui ; un code ISIN n'appartient qu'à une
      société (une case vide ne compte pas : le code d'une société sortie peut rester à trouver, A-564) ; chaque code
      non vide des deux tables a la forme et la clé d'un ISIN (`isin_valide`) ; chaque date
      de la table des passages se lit ; aucun passage ne sort de l'indice avant d'y entrer ; deux passages d'un même
      code ISIN ne se chevauchent pas, une sortie le jour d'une entrée comprise, et seul le dernier peut être sans fin
      (ValueError sinon, pour chacune de ces conditions, avec le passage en cause). `lire` vérifie en plus que chaque valeur de l'univers a au moins un passage. Un mnémonique
      d'aujourd'hui inconnu du référentiel est admis : c'est une société sortie de l'indice (relecture indépendante du
      12-10-2026 : l'exiger aurait fait tomber toute lecture le jour où A-564 ajoute Vivendi). Les conditions de
      `societes_sorties` s'appliquent, et un mnémonique de société sortie qui est aussi celui d'une société
      d'aujourd'hui est refusé (« désigne deux sociétés »).
    ⑤ SORTIE — UNE valeur : {mnémonique : liste triée des (première séance, dernière séance ou None pour une société
      encore dans l'indice)} — le mnémonique d'aujourd'hui pour une société cotée, celui de `societes_sorties` pour une
      société sortie (depuis le 14-11-2026, QE ; exemple réel : UG, Peugeot S.A., DEUX passages, du 2000-01-03 au
      2012-09-21 et du 2015-03-23 au 2021-01-15 — D2 du relecteur QE, tour 1).
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ chaque code non vide des deux tables, forme et clé d'un ISIN (relecture de Cowork 15e647c,
      cassure H : un code écrit avec une espace détachait STMicroelectronics de son premier passage) · chaque
      passage, qu'il appartienne ou non à une société connue : ses dates se lisent, sa sortie
      n'est pas avant son entrée ; les passages d'un même code ISIN (un code vide n'en est pas un), dans l'ordre, ne se
      chevauchent pas · ① chaque société (colonne `numero`) : l'ensemble de ses codes ISIN, toutes périodes
      confondues, et son mnémonique d'aujourd'hui (la ligne sans `fin`) ou, pour une société sortie, celui de
      `societes_sorties` · ② chaque passage dont le code ISIN de bnains est l'un de ces codes est rangé sous ce
      mnémonique.
      Un passage à l'envers ou un code dans l'indice deux fois le même jour est une table fausse : relecture de Cowork
      du 12-10-2026 (9c882a6, cassure G) — la sortie d'EADS mise au 09-07-1999, avant son entrée du 10-07-2000, faisait
      disparaître les 292 trous d'Airbus sans un mot. Les deux dates d'un passage sont des séances DANS l'indice
      (etudes/outils/RELEVER_LA_COMPOSITION_DU_CAC40.py, son ⑦) : une sortie le jour d'une entrée du même code le
      compterait deux fois ce jour-là ; un passage d'une seule séance (Edenred, 2010-07-02) est juste.
    ⑦ UNITÉ — Des séances (dates).
    ⑧ POURQUOI — Un passage est une LIGNE DE COTATION, pas une société : bnains garde parfois un code périmé (Dassault
      Systèmes avant sa division de 2021) ; la table des identités relie chaque code à sa société. Peugeot S.A.
      (FR0000121501) n'est pas Stellantis (NL00150001Q9) : son code n'est dans aucune identité de Stellantis, ses
      années ne lui sont donc pas prêtées (ligne E2 de Cowork).
    ⑨ CE QUI CLOCHE — Une société sortie dont le mnémonique est « non trouvé » (CONTRATS.MNEMONIQUE_NON_TROUVE, 25
      sociétés au 14-11-2026) : ses passages ne sont rangés sous aucun mnémonique. · La table des identités est écrite à la main : une ligne fausse qui rattache le code d'une
      autre société (Peugeot S.A., FR0000121501, sous Stellantis) lui prête ses années sans alerte — relecture
      indépendante du 12-10-2026 : 4 742 trous pour STLAP ; seule la relecture de la table l'empêche. · Le
      chevauchement de deux codes DIFFÉRENTS d'une même société n'est pas refusé : il ne change rien aux séances
      attendues (`_attendues` fait l'union), et une société absorbée rangée sous celle qui l'absorbe (Aventis sous
      Sanofi, comme Arcelor l'est déjà sous ArcelorMittal) serait deux fois dans l'indice en même temps — que faire
      d'une société absorbée est à décider avec A-564 (relecture indépendante du 12-10-2026, cas C4). · Les dates
      `debut` et `fin` de la table des identités ne sont jamais lues comme des dates : une date illisible y passe, et
      ne tombe plus loin que sous un autre motif (« valeur sans passage ») ; elles ne sont pas non plus confrontées
      aux dates des passages (même relecture, cas T19 et T22).
    ⑩ EFFET — Lit deux fichiers.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    _, ident = _lire_csv(os.path.join(racine, IDENTITES), [CONTRATS.IDENTITES_DES_SOCIETES], IDENTITES)
    _, passages = _lire_csv(os.path.join(racine, PASSAGES), [CONTRATS.PASSAGES_DANS_LE_CAC40], PASSAGES)
    for table, lignes, champ in ((IDENTITES, ident, "isin"), (PASSAGES, passages, "isin_bnains")):
        for r in lignes:
            if r[champ] and not isin_valide(r[champ]):
                raise ValueError(f"{os.path.basename(table)} : code ISIN mal écrit « {r[champ]} » "
                                 f"({r.get('libelle_bnains') or r.get('societe')}) — forme ou clé fausse")
    par_code = defaultdict(list)
    for p in passages:
        try:
            entree = CAL._date_stricte(p["premiere_seance"])
            sortie = CAL._date_stricte(p["derniere_seance"]) if p["derniere_seance"] else None
        except ValueError:
            raise ValueError(f"passages : date illisible pour {p['libelle_bnains']} ({p['isin_bnains']}) : entrée "
                             f"« {p['premiere_seance']} », sortie « {p['derniere_seance']} »") from None
        if sortie is not None and sortie < entree:
            raise ValueError(f"passages : {p['libelle_bnains']} ({p['isin_bnains']}) sort de l'indice le {sortie} "
                             f"avant d'y entrer le {entree}")
        if p["isin_bnains"]:
            par_code[p["isin_bnains"]].append((entree, sortie))
    for code, periodes in par_code.items():
        periodes.sort(key=lambda x: (x[0], x[1] or date.max))
        for (a1, b1), (a2, b2) in zip(periodes, periodes[1:]):
            if b1 is None or a2 <= b1:
                raise ValueError(f"passages : deux passages du code {code} se chevauchent ({a1} → {b1 or 'sans fin'} "
                                 f"et {a2} → {b2 or 'sans fin'})")
    codes, actuel, societe_du_code = defaultdict(set), {}, {}
    for r in ident:
        if r["isin"] and societe_du_code.setdefault(r["isin"], r["numero"]) != r["numero"]:
            raise ValueError(f"identités : le code {r['isin']} appartient à deux sociétés "
                             f"({societe_du_code[r['isin']]} et {r['numero']})")
        if r["isin"]:
            codes[r["numero"]].add(r["isin"])
        if not r["fin"]:
            if r["numero"] in actuel:
                raise ValueError(f"identités : la société {r['numero']} a deux lignes sans date de fin")
            actuel[r["numero"]] = r["mnemonique"]
    for m, (numero, _) in societes_sorties(ident, anomalies).items():   # QE : une société sortie, sous son dernier mnémonique
        actuel[numero] = m
    out = {}
    for numero, m in actuel.items():
        if m in out:
            raise ValueError(f"identités : le mnémonique {m} désigne deux sociétés")
        out[m] = sorted(((CAL._date_stricte(p["premiere_seance"]),
                          CAL._date_stricte(p["derniere_seance"]) if p["derniere_seance"] else None)
                         for p in passages if p["isin_bnains"] in codes[numero]),
                        key=lambda x: (x[0], x[1] or date.max))
    return out


def jusqu_au_par_defaut():
    """Rend la date jusqu'à laquelle une lecture sans date attend les cours : la veille, heure de Paris.

    ① RÔLE — Écrire en un seul endroit la date que `lire` prend quand on ne lui en donne pas.
    ② CONTEXTE D'APPEL — `lire`, quand `jusqu_au` n'est pas donné.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la date d'hier à Paris.
      [rend: 1]
    ⑥ TRAITEMENT — lire l'horloge, retirer un jour.
    ⑦ UNITÉ — Une date.
    ⑧ POURQUOI — Une lecture faite pendant la séance ne doit pas compter la séance du jour comme un trou : ses cours ne
      sont pas encore publiés. Le circuit du soir, qui lit après la collecte, doit passer le jour même : la valeur par
      défaut ne verrait pas la séance du jour manquer (seconde relecture indépendante du 10-10-2026).
    ⑨ CE QUI CLOCHE — Rien n'oblige le circuit du soir à passer le jour même : c'est à vérifier quand il passera par ce
      module.
    ⑩ EFFET — Lit l'horloge.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return datetime.now(ZoneInfo("Europe/Paris")).date() - timedelta(days=1)


def _meme_barre(a, b):
    """Dit si deux lignes de cours portent la même barre.

    ① RÔLE — Distinguer un doublon d'un conflit.
    ② CONTEXTE D'APPEL — `lire`, à chaque second exemplaire d'une barre.
    ③ ENTRÉE — `a`, `b` : deux lignes du fichier des cours.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si chacun des cinq champs de la barre est égal : même texte (espaces de bord
      retirés), ou deux nombres décimaux écrits simplement (chiffres, un point, un exposant) de même valeur.
      [rend: 1]
    ⑥ TRAITEMENT — champ par champ ; NOMBRE décide de ce qui se lit en nombre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : « 45.39 » et « 45.390 » étaient pris pour deux versions, et la
      barre était écartée — une fausse alerte. Seconde relecture du même jour : « nan » contre « nan » faisait un
      conflit (nan n'est égal à rien), et « 1_000 » égalait « 1000 » (Python lit le souligné) — d'où le même texte
      d'abord, et un motif de nombre écrit simplement.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for c in CHAMPS_DE_LA_BARRE:
        x, y = a[c].strip(), b[c].strip()
        if x == y:
            continue
        if not (NOMBRE.fullmatch(x) and NOMBRE.fullmatch(y)) or float(x) != float(y):
            return False
    return True


def lire(racine, fichier=FICHIER_DES_COURS, jusqu_au=None):
    """Lit un fichier de cours et le rend rangé par mnémonique et par séance.

    ① RÔLE — La lecture unique des cours (R-111 ①).
    ② CONTEXTE D'APPEL — Les programmes qui ont besoin des cours ; `main`.
    ③ ENTRÉE — `racine` : la racine du dépôt · `fichier` : le fichier des cours, relatif à la racine ; par défaut
      donnees/cours_maitre.csv, et donnees/sources_yahoo/historique_long_repare.csv pour l'historique long ·
      `jusqu_au` : la date jusqu'à laquelle chaque séance doit avoir ses cours ; par défaut `jusqu_au_par_defaut`, la
      veille (Paris) — sauf pour un fichier déclaré figé (CONTRATS.FICHIERS_DE_COURS_FIGES, par son chemin depuis la
      racine), attendu jusqu'à la date qu'y déclare sa ligne, même quand `jusqu_au` va plus loin.
    ④ CONDITIONS D'ENTRÉE — L'en-tête du fichier est exactement l'un des CONTRATS_DE_COURS de
      programmes/CONTRATS_DES_FICHIERS.py — huit colonnes avec la source (le maître, l'historique long), ou sept sans
      elle (l'arrivée du soir, la référence Google) ; `jusqu_au` est couvert par le
      calendrier, sinon HorsCalendrier (une ValueError) ; chaque nature de trou tombe une séance ; voir aussi
      `table_des_ecritures`, `lire_les_natures` et CALENDRIER_DE_LA_BOURSE.lire_les_seances.
    ⑤ SORTIE — UNE valeur : un dictionnaire. « barres » : {mnémonique : {date : la ligne telle que lue}} ;
      « ecritures » : {mnémonique : Counter des noms rencontrés} ; « inconnues » : Counter des noms sans mnémonique ;
      « doublons » : les (mnémonique, date) écrits deux fois à l'identique ; « conflits » : les (mnémonique, date)
      écrits deux fois différemment ; « hors_seance » : les (mnémonique, date, état) tombés un jour FERMÉE ;
      « hors_calendrier » : les (mnémonique, date) hors du calendrier ; « dates_illisibles » : Counter des dates
      refusées ; « debut » : la première date rangée ; « fin » : la dernière séance du calendrier au plus tard
      `jusqu_au` ou la dernière date rangée, la plus tardive des deux ; « natures_sans_trou » : les (mnémonique, date)
      dont la nature est écrite alors que la barre existe ; « seances » : le calendrier ; « hors_univers » ;
      « natures » ; « fichier » ; « source_ecrite » : faux pour un fichier à sept colonnes, dont la source n'est donc
      pas dite ligne par ligne ; « fige » : vrai pour un fichier déclaré figé ; « fige_allonge » : les dates rangées
      après la dernière séance déclarée d'un fichier figé (vide sinon) ; « fige_modifie » : l'empreinte trouvée quand
      elle diffère de l'empreinte déclarée (None sinon) ; « au_dela_du_fige » : la date demandée par l'appelant quand
      elle passe la dernière séance déclarée (None sinon) — les séances d'entre les deux ne sont pas des trous ;
      « fin_du_fige » : la dernière séance déclarée (None pour un fichier non figé) ; « dans_l_indice » : le rendu de
      `lire_les_passages`, vide pour un fichier déclaré incrément (CONTRATS.FICHIERS_DE_COURS_INCREMENTS) ;
      « lignes_lues » : le nombre de lignes de données du fichier (depuis le 27-10-2026, pour `lignes_mises_a_part`) ;
      « ecartees » : les (valeur, date, cause) des lignes écartées sur décision (CONTRATS.LIGNES_ECARTEES_SUR_DECISION,
      depuis le 14-11-2026), ni rangées ni mises à part ; « sorties » : les mnémoniques des sociétés sorties de
      l'indice (`societes_sorties`, depuis le 14-11-2026, QE2), attendues à chaque séance de leur présence dans l'indice
      couverte par le fichier (`_attendues`) ; « porte_les_sorties » : vrai pour un fichier déclaré
      CONTRATS.FICHIERS_DE_COURS_QUI_PORTENT_LES_SOCIETES_SORTIES ; « sorties_sans_cle » : pour un tel fichier, le rendu de
      `presence_des_societes_sorties_sans_cle` (vide sinon) ; « anomalies_d_identite » : les textes des TROIS anomalies
      de `societes_sorties` — fin illisible, deux dernières lignes le même jour, un mnémonique pour deux sociétés
      sorties — sur des sociétés sorties ABSENTES du fichier lu (I-1 de Cowork, 14-11-2026). Les autres fautes des deux
      tables — ISIN mal écrit, ISIN à deux sociétés, date de PASSAGES — arrêtent TOUJOURS la lecture (ValueError), même
      sur une société sortie absente (K-2 et K-7 de Cowork, lot C). Une des trois qui touche un nom écrit dans le fichier
      arrête la lecture (ValueError) ; sur un fichier déclaré porter les
      sociétés sorties, toute anomalie d'identité arrête la lecture, parce que le compte de présence dépend de toute la
      table (K-4 de Cowork) ; les autres sont rendues ici ; `resume` les dit, et le versement du soir aussi
      (`TENIR_L_HISTORIQUE.dire_les_anomalies_d_identite`, sortie du pas `anomalies_d_identite`, K-1 de Cowork).
      [rend: 1]
    ⑥ TRAITEMENT — ① la table des écritures, à laquelle s'ajoute le mnémonique de chaque société sortie
      (`societes_sorties`, hors univers au motif « sortie de l'indice le … » ; QE, 14-11-2026) · ② le calendrier des
      séances · ③ chaque ligne : son nom rapproché en
      mnémonique (sinon « inconnues »), sa date lue (sinon « dates_illisibles »), son état au calendrier (hors séance ou
      hors calendrier : mise à part), puis rangée ; un second exemplaire égal sur les cinq champs de la barre est un
      doublon, gardé une fois ; différent, un conflit, et les DEUX sont mis à part · ④ la fin, en reculant jusqu'à une
      séance · ⑤ la nature des trous, confrontée au calendrier et aux barres.
    ⑦ UNITÉ — Des séances ; les cours restent du texte, tels qu'écrits.
    ⑧ POURQUOI — R-111 ② ③ ④ et la table de réception, lignes A2 (tout le marché manque), A3 (jour férié reçu comme une
      séance), E1 (une valeur écrite de deux façons), E3 (valeur attendue absente), E4 (doublon : identiques, une
      gardée et alerte ; différentes, mise en attente). Un conflit n'est pas tranché : choisir l'un des deux cours
      appartient à Jean-Luc (R-109). Relecture indépendante du 10-10-2026 : la fin était la dernière date LUE, si bien
      que des séances manquantes pour toutes les valeurs à la fin du fichier passaient sans un mot, et qu'une seule
      ligne datée de 2027 arrêtait toute la lecture. Relecture de Cowork du 11-10-2026 (e183c98) : la lecture refusait
      la référence Google et l'arrivée du soir, à sept colonnes ; un lecteur « pour tous » doit les lire. Relecture de
      Cowork du 12-10-2026 (108efa5) : lue sans date, la référence Google, figée au 10-07-2026, sortait 65 « trous de
      tout le marché » ; un fichier figé se DÉCLARE (le maître dont la collecte tombe a la même allure, et doit crier),
      par son chemin et sa dernière séance (relecture indépendante du 12-10-2026 : déclaré par son seul nom, une copie
      du maître posée ailleurs sous ce nom se taisait ; fini à sa dernière date LUE, une référence tronquée aussi).
    ⑨ CE QUI CLOCHE — Une barre mise à part n'est écrite nulle part : le fichier « en attente » de la table de réception
      n'existe pas encore ; elle est seulement rendue et affichée. · L'empreinte d'un fichier figé porte sur ses octets :
      le même contenu en fins de ligne Windows, ou avec la marque UTF-8 en tête, dit « FICHIER FIGÉ MODIFIÉ » (fausse
      alarme, le sens sûr) ; un clone sous Windows avec conversion des fins de ligne crierait (aucun .gitattributes ne
      l'empêche le 12-10-2026). L'empreinte et la lecture ouvrent le fichier chacune une fois : un fichier écrit entre
      les deux ne serait pas vu. · Le chemin d'un fichier figé se compare tel qu'écrit : sur un système qui ignore la
      casse, « CAC40_OHLCV.csv » ouvrirait le fichier sans le dire figé — il crierait alors ses trous, le sens sûr.
    ⑩ EFFET — Lit six fichiers (les cours, le référentiel, l'indice, la liste d'Euronext, la nature des trous, les deux
      tables de la règle I-3 comptent pour une) et le dossier donnees/ ; lit l'horloge quand `jusqu_au` n'est pas donné, sauf pour un
      fichier déclaré figé, dont il lit une seconde fois les octets pour en prendre l'empreinte.
    ⑪ TERMINAISON — Rend la main ou lève ; un passage sur le fichier ; le recul vers la fin s'arrête au début du
      calendrier.
      [sort: non]
    """
    table, hors = table_des_ecritures(racine)
    _, ident = _lire_csv(os.path.join(racine, IDENTITES), [CONTRATS.IDENTITES_DES_SOCIETES], IDENTITES)
    sorties, anomalies = set(), []
    for m, (numero, sortie) in sorted(societes_sorties(ident, anomalies).items()):
        # QE (A-713 ①, 14-11-2026) : l'assemblage des 20 ans écrit une société sortie sous son MNÉMONIQUE (décision de
        # Jean-Luc du 11-11-2026 à 22h26) ; elle est hors univers, motif « sortie de l'indice » : plus collectée, elle
        # n'est attendue qu'entre sa première et sa dernière barre (`_periode`), jamais absente du maître.
        k = COMMUN.norm_valeur(m)
        if m in hors or table.get(k, m) != m:
            raise ValueError(f"identités : le mnémonique « {m} » de la société sortie {numero} est déjà une écriture "
                             f"ou un mnémonique du référentiel ({table.get(k, m)})")
        table[k] = m
        hors[m] = f"sortie de l'indice le {sortie.isoformat()} (IDENTITES_DES_SOCIETES, société {numero})"
        sorties.add(m)
    sc = CAL.lire_les_seances(racine)
    chemin = os.path.relpath(os.path.join(racine, fichier), racine).replace(os.sep, "/")
    fige = chemin in CONTRATS.FICHIERS_DE_COURS_FIGES
    fin_declaree = CAL._date_stricte(CONTRATS.FICHIERS_DE_COURS_FIGES[chemin]["fin"]) if fige else None
    au_dela = jusqu_au if fige and jusqu_au is not None and jusqu_au > fin_declaree else None
    if fige and (jusqu_au is None or au_dela):
        jusqu_au = fin_declaree
    modifie = None
    if fige:
        with open(os.path.join(racine, fichier), "rb") as f:
            empreinte = hashlib.sha256(f.read()).hexdigest()
        modifie = empreinte if empreinte != CONTRATS.FICHIERS_DE_COURS_FIGES[chemin]["sha256"] else None
    entete, lignes = _lire_csv(os.path.join(racine, fichier), CONTRATS.CONTRATS_DE_COURS, fichier)
    # LIGNES ÉCARTÉES SUR DÉCISION (14-11-2026, décision de Jean-Luc de 13h41) : une DONNÉE du contrat, jamais une date
    # écrite ici ; la ligne doit être retrouvée à l'identique, sinon la lecture s'arrête.
    a_ecarter = {}
    for x in getattr(CONTRATS, "LIGNES_ECARTEES_SUR_DECISION", {}).get(chemin, []):
        a_ecarter[tuple(next(csv.reader([x["ligne"]])))] = x
    ecartees = []
    barres, ecritures = defaultdict(dict), defaultdict(Counter)
    inconnues, illisibles = Counter(), Counter()
    doublons, conflits, hors_seance, hors_cal = [], set(), [], []
    for r in lignes:
        if a_ecarter and tuple(r[c] for c in entete) in a_ecarter:
            ecartees.append((r["valeur"], r["date"], a_ecarter[tuple(r[c] for c in entete)]["cause"]))
            continue
        m = table.get(COMMUN.norm_valeur(r["valeur"]))
        if m is None:
            inconnues[r["valeur"]] += 1
            continue
        try:
            d = CAL._date_stricte(r["date"])
        except ValueError:
            illisibles[r["date"]] += 1
            continue
        ecritures[m][r["valeur"]] += 1
        try:
            etat = CAL.etat_du_jour(d, sc)
        except CAL.HorsCalendrier:
            hors_cal.append((m, d))
            continue
        if etat == CAL.FERMEE:
            hors_seance.append((m, d, etat))
            continue
        if (m, d) in conflits:
            continue
        deja = barres[m].get(d)
        if deja is None:
            barres[m][d] = r
        elif _meme_barre(deja, r):
            doublons.append((m, d))
        else:
            conflits.add((m, d))
            del barres[m][d]
    if len(ecartees) != len(a_ecarter):
        vues = Counter((v, d) for v, d, _ in ecartees)
        manquent = [k[:2] for k in a_ecarter if vues[tuple(k[:2])] == 0]
        doubles = sorted(k for k, n in vues.items() if n > 1)   # D3 du relecteur QE : « introuvable : [] » trompait
        raise ValueError(f"{fichier} : ligne(s) déclarée(s) écartée(s) au contrat (LIGNES_ECARTEES_SUR_DECISION) "
                         + (f"introuvable(s) à l'identique : {manquent}" if manquent else "")
                         + (" ; " if manquent and doubles else "")
                         + (f"présente(s) plusieurs fois à l'identique : {doubles}" if doubles else ""))
    rangees = [d for b in barres.values() for d in b]
    debut = min(rangees) if rangees else None
    allonge = sorted({d for d in rangees if d > fin_declaree}) if fige else []
    if jusqu_au is None:
        jusqu_au = jusqu_au_par_defaut()
    fin = max([jusqu_au] + rangees)
    while CAL.etat_du_jour(fin, sc) == CAL.FERMEE:
        fin -= timedelta(days=1)
    natures = lire_les_natures(racine, hors)
    dans_l_indice = lire_les_passages(racine, [])   # ses anomalies sont celles de `anomalies`, déjà rangées
    # I-1 de Cowork (14-11-2026) : une anomalie d'identité d'une société sortie n'arrête la lecture que si elle touche une
    # valeur PRÉSENTE dans le fichier lu — un nom écrit dans le fichier qui est l'un des mnémoniques de cette société ;
    # sinon elle est signalée et comptée (`resume`), et la lecture se poursuit : une faute de saisie sur Peugeot S.A. ne
    # doit pas faire perdre au circuit du soir la séance du maître, où Peugeot n'a aucune barre.
    lus = {COMMUN.norm_valeur(x) for x in inconnues}
    for numeros, texte in anomalies:
        noms = {COMMUN.norm_valeur(r["mnemonique"].strip()) for r in ident if r["numero"] in numeros
                and r["mnemonique"].strip() not in VIDES and r["mnemonique"].strip() != CONTRATS.MNEMONIQUE_NON_TROUVE}
        if noms & lus:
            raise ValueError(texte + f" — elle touche une valeur écrite dans {fichier}")
    sans = sorted(m for m, motif in hors.items() if not motif and not dans_l_indice.get(m))
    if sans:
        raise ValueError(f"identités : valeur(s) de l'univers sans aucun passage dans l'indice {sans} — un renommage "
                         f"dans IDENTITES_DES_SOCIETES, ou ses lignes retirées ?")
    if chemin in CONTRATS.FICHIERS_DE_COURS_INCREMENTS:
        dans_l_indice = {}
    # QE2 tour 2 (D1 du relecteur QE2, superviseur R-759 du 14-11-2026 ①) : un fichier DÉCLARÉ porter les sociétés
    # sorties (contrat) compte À PART la présence dans l'indice de chaque société sortie SANS clé de lecture
    porte = chemin in getattr(CONTRATS, "FICHIERS_DE_COURS_QUI_PORTENT_LES_SOCIETES_SORTIES", ())
    _, rangees_passages = _lire_csv(os.path.join(racine, PASSAGES), [CONTRATS.PASSAGES_DANS_LE_CAC40], PASSAGES)
    sans_cle = (presence_des_societes_sorties_sans_cle(ident, rangees_passages, sc, debut, fin)
                if porte and debut is not None else {})
    for (m, d) in natures:
        try:
            ferme = CAL.etat_du_jour(d, sc) == CAL.FERMEE
        except CAL.HorsCalendrier:
            raise ValueError(f"nature des trous : {m} le {d.isoformat()} est hors du calendrier")
        if ferme:
            raise ValueError(f"nature des trous : {m} le {d.isoformat()} n'est pas une séance")
    sans_trou = sorted(k for k in natures if k[1] in barres.get(k[0], {}))
    return {"barres": dict(barres), "ecritures": dict(ecritures), "inconnues": inconnues,
            "dates_illisibles": illisibles, "doublons": doublons, "conflits": sorted(conflits),
            "hors_seance": hors_seance, "hors_calendrier": hors_cal, "debut": debut, "fin": fin, "seances": sc,
            "hors_univers": hors, "natures": natures, "natures_sans_trou": sans_trou, "fichier": fichier,
            "source_ecrite": "source" in entete, "fige": fige, "fige_allonge": allonge, "fige_modifie": modifie,
            "au_dela_du_fige": au_dela, "fin_du_fige": fin_declaree, "dans_l_indice": dans_l_indice,
            "lignes_lues": len(lignes), "ecartees": ecartees, "sorties": sorties,
            "porte_les_sorties": porte, "sorties_sans_cle": sans_cle,
            "anomalies_d_identite": [texte for _, texte in anomalies]}


def _periode(cours, m):
    """Rend la période où une valeur doit avoir un cours à chaque séance.

    ① RÔLE — Écrire en un seul endroit d'où à où une valeur est attendue, pour `trous` et `trous_de_tout_le_marche`.
    ② CONTEXTE D'APPEL — `trous`, `trous_de_tout_le_marche`.
    ③ ENTRÉE — `cours` : le rendu de `lire` · `m` : un mnémonique.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la première date et la dernière ; toutes deux None quand la valeur n'est attendue nulle
      part.
      [rend: 2]
    ⑥ TRAITEMENT — ① une valeur inconnue du référentiel, ou un fichier sans aucune barre : None, None · ② le début :
      sa première barre, ou, si elle n'en a aucune, la première date rangée du fichier · ③ la fin : la fin du fichier
      (`fin`), ou, pour une valeur hors univers, sa dernière barre — None, None si elle n'en a aucune.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Une valeur de l'univers absente du fichier entier est un trou à chaque séance (relecture indépendante
      du 10-10-2026 : toutes les lignes de Vinci retirées, la lecture rendait « rien à signaler »). Une valeur hors
      univers n'est plus collectée par décision (colonne hors_univers du référentiel, par exemple ArcelorMittal,
      « AMSTERDAM — decision Jean-Luc ») : son absence après sa dernière barre n'est pas un trou.
    ⑨ CE QUI CLOCHE — Avant sa première barre, cette période ne dit rien : `_attendues` y ajoute les séances où la
      valeur était dans l'indice (cassure B de Cowork, 11-10-2026).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if m not in cours["hors_univers"] or cours["debut"] is None:
        return None, None
    b = cours["barres"].get(m) or {}
    if cours["hors_univers"][m]:
        if not b:
            return None, None
        return min(b), max(b)
    return (min(b) if b else cours["debut"]), cours["fin"]


def _attendues(cours, m):
    """Rend les séances où une valeur doit avoir un cours.

    ① RÔLE — Écrire en un seul endroit QUELLES séances une valeur doit couvrir, pour `trous` et
      `trous_de_tout_le_marche`.
    ② CONTEXTE D'APPEL — `trous`, `trous_de_tout_le_marche`.
    ③ ENTRÉE — `cours` : le rendu de `lire` · `m` : un mnémonique.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des séances.
      [rend: 1]
    ⑥ TRAITEMENT — ① les séances de `_periode`, sauf pour une société sortie · ② pour une valeur de l'univers ET pour une société sortie de l'indice
      (« sorties », depuis le 14-11-2026, QE2), en plus, les séances où sa société était dans le CAC 40
      (« dans_l_indice », lu par `lire_les_passages`), bornées au fichier : de sa première date rangée (« debut ») à sa
      fin (« fin »).
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Cassure B de Cowork (11-10-2026, e183c98) : avant sa première barre, une valeur n'avait pas de trou —
      9 514 séances tues dans l'historique long, alors qu'elle était dans l'indice ; décision de Jean-Luc A8
      (10-10-2026) : ces séances sont marquées. Exemple : Airbus (AIR), dans l'indice sous EADS depuis le 10-07-2000
      (avis 2000-2926), première barre de l'historique long le 03-09-2001. Borné au début du FICHIER, pas de l'indice :
      le fichier maître, qui commence plus tard, n'est pas tenu de couvrir 2000.
      QE2 (14-11-2026, D1 du relecteur QE, tour 1) : une société SORTIE n'était attendue qu'entre sa première et sa
      dernière barre — mesuré par le relecteur, 6 027 séances dans l'indice sans barre et aucune comptée (Worldline,
      2023-01-30 au 2023-12-15 : 227) ; un biais du survivant sur les périodes qui précèdent une sortie. Elle est
      reconnue par la table des identités (`societes_sorties`), pas par une liste. Seulement dans un fichier DÉCLARÉ porter les sociétés
      sorties (CONTRATS.FICHIERS_DE_COURS_QUI_PORTENT_LES_SOCIETES_SORTIES, « porte_les_sorties »), ou qui porte au moins
      une barre d'elle : le maître et la référence Google, collectés pour les valeurs du référentiel, ne disent rien d'une société
      sortie et n'en attendent rien (mesuré : sans cette condition, ALO, VIV, EDEN et TEP y prenaient des trous en
      2024-2025, et L14, L17, L26, L27 rougissaient).
    ⑨ CE QUI CLOCHE — Un fichier NON DÉCLARÉ qui a perdu toutes les barres d'une société sortie n'en dit rien (un fichier
      déclaré, lui, garde ses trous : L42). · Une valeur hors univers PAR DÉCISION (ArcelorMittal, « AMSTERDAM ») n'en reçoit rien : elle n'est
      plus collectée. Un fichier déclaré incrément (CONTRATS.FICHIERS_DE_COURS_INCREMENTS) n'en reçoit rien non plus : « dans_l_indice » y est vide.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    # QE2 : une société sortie n'est attendue QUE pendant sa présence dans l'indice (ci-dessous), jamais entre ses barres
    # hors de l'indice (Nokia, barres de 2004 et de 2011, entrée au CAC 40 le 2016-01-07)
    p = _periode(cours, m) if m not in cours.get("sorties", ()) else (None, None)
    jours = set()
    if p[0] is not None:
        jours |= {d for d, _ in CAL.seances_entre(p[0], p[1], cours["seances"])}
    if m in cours["hors_univers"] and (not cours["hors_univers"][m] or m in cours.get("sorties", ())
                                       and (cours.get("porte_les_sorties") or cours["barres"].get(m))) \
            and cours["debut"] is not None:
        for a, b in cours["dans_l_indice"].get(m, []):
            a, b = max(a, cours["debut"]), min(b or cours["fin"], cours["fin"])
            if a <= b:
                jours |= {d for d, _ in CAL.seances_entre(a, b, cours["seances"])}
    return sorted(jours)


def lignes_mises_a_part(cours):
    """Rend le nombre de lignes du fichier que la lecture n'a pas rangées, et qui ne sont pas des doublons exacts.

    ① RÔLE — Dire, en un nombre, si une lecture a écarté quelque chose — par une PROPRIÉTÉ de conservation, sans
      énumérer les sortes d'écart : un appelant qui énumère oublie la sorte suivante.
    ② CONTEXTE D'APPEL — `programmes/JUGE_DES_STRATEGIES.py` (`lire_par_le_lecteur`), qui refuse de juger sur une
      lecture qui a écarté des lignes ; toute autre lecture qui doit tout garder.
    ③ ENTRÉE — `cours` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : lignes lues − barres rangées − doublons exacts − lignes écartées SUR DÉCISION (« ecartees »,
      déclarées au contrat, depuis le 14-11-2026) ; 0 quand rien n'a été mis à part.
      [rend: 1]
    ⑥ TRAITEMENT — Une soustraction.
    ⑦ UNITÉ — Des LIGNES du fichier.
    ⑧ POURQUOI — Relecture et superviseur (R-759) du 27-10-2026 : le juge des stratégies comptait les écarts par une
      liste de clés (« inconnues », « conflits », « hors_seance », « hors_calendrier ») et ne voyait pas une date
      illisible — mesuré : une ligne datée « 26/10/2026 » mise à part, et le juge jugeait quand même. Toute ligne
      écartée (nom sans mnémonique, date illisible, jour hors du calendrier ou fermé, les deux exemplaires d'une
      séance en conflit) manque à cette égalité, quelle que soit la sorte. Mesuré le 27-10-2026 : 0 sur le fichier
      maître (28 110 lignes) et sur l'historique des 20 ans.
    ⑨ CE QUI CLOCHE — Ne dit rien d'un fichier figé modifié ou allongé (« fige_modifie », « fige_allonge ») : ce sont
      des affaires de fichier, pas de lignes, que l'appelant regarde à part.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return (cours["lignes_lues"] - sum(len(b) for b in cours["barres"].values()) - len(cours["doublons"])
            - len(cours.get("ecartees", [])))


def trous(cours, m):
    """Rend les trous d'une valeur : les séances du calendrier où elle n'a pas de cours.

    ① RÔLE — R-111 ② : calculer chaque trou à chaque lecture.
    ② CONTEXTE D'APPEL — `resume` ; les programmes qui calculent sur une période.
    ③ ENTRÉE — `cours` : le rendu de `lire` · `m` : un mnémonique.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste, dans l'ordre, des couples (date, nature) ; la nature est celle de
      donnees/NATURE_DES_TROUS.csv, « DEUX VERSIONS » pour une séance en conflit, NON DÉCIDÉE sinon. Liste vide pour
      une valeur qui n'est attendue nulle part (`_attendues`).
      [rend: 1]
    ⑥ TRAITEMENT — les séances où la valeur est attendue (`_attendues`), moins celles qui ont une barre.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Une valeur absente à la fin du fichier est un trou à chaque séance, signalé chaque jour (table de
      réception, E3 : « une valeur absente deux jours de suite n'est signalée que le premier » par le contrôle actuel).
    ⑨ CE QUI CLOCHE — Voir `_attendues`.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    b = cours["barres"].get(m) or {}
    en_conflit = {d for (x, d) in cours["conflits"] if x == m}
    out = []
    for d in _attendues(cours, m):
        if d not in b:
            nature = "DEUX VERSIONS" if d in en_conflit else cours["natures"].get((m, d), (NON_DECIDEE, ""))[0]
            out.append((d, nature))
    return out


def trous_par_periode(cours, m):
    """Rend les trous d'une valeur regroupés en périodes de séances consécutives du calendrier, avec leur nature.

    ① RÔLE — Dire ce qui manque « par valeur et par période » : la liste à remettre à une recherche de sources, et le
      résumé que le juge affiche.
    ② CONTEXTE D'APPEL — Le juge des stratégies (`lire_par_le_lecteur`) ; le relevé des trous des sociétés sorties.
    ③ ENTRÉE — `cours` : le rendu de `lire` · `m` : un mnémonique.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste, dans l'ordre, des (première séance, dernière séance, nombre de séances, nature) ;
      une période ne mêle pas deux natures.
      [rend: 1]
    ⑥ TRAITEMENT — les trous de `trous` ; deux trous sont dans la même période quand aucune séance du calendrier ne les
      sépare et qu'ils ont la même nature.
    ⑦ UNITÉ — Des séances du calendrier.
    ⑧ POURQUOI — QE2 (14-11-2026) : 6 027 séances manquent aux sociétés sorties ; les lire une à une ne sert à
      personne, une période (Worldline, du 2023-01-30 au 2023-12-15, 227 séances) se cherche en une fois.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    t = trous(cours, m)
    rang = {d: i for i, (d, _) in enumerate(CAL.seances_entre(t[0][0], t[-1][0], cours["seances"]))} if t else {}
    out = []
    for d, nature in t:
        if out and out[-1][3] == nature and rang[d] == rang[out[-1][1]] + 1:
            out[-1] = (out[-1][0], d, out[-1][2] + 1, nature)
        else:
            out.append((d, d, 1, nature))
    return out


def dernieres_seances(cours, m, n, jusqu_au):
    """Rend les `n` dernières séances du calendrier au plus tard `jusqu_au`, avec la barre de la valeur ou None.

    ① RÔLE — Donner à un calcul « sur les n dernières séances » des séances du calendrier, jamais des lignes.
    ② CONTEXTE D'APPEL — Les programmes qui calculent un indicateur sur une fenêtre (aucun encore le 10-10-2026).
    ③ ENTRÉE — `cours` : le rendu de `lire` · `m` : un mnémonique · `n` : un entier positif · `jusqu_au` : une date.
    ④ CONDITIONS D'ENTRÉE — `n` ≥ 1 (ValueError sinon) ; les jours parcourus sont couverts par le calendrier.
    ⑤ SORTIE — UNE valeur : la liste, la plus ancienne en tête, d'au plus `n` couples (date, ligne de la barre ou None
      pour un trou) ; moins de `n` quand le calendrier commence avant. Pour un fichier figé, `jusqu_au` est ramené à sa
      dernière séance déclarée (« fin_du_fige »), comme dans `lire`.
      [rend: 1]
    ⑥ TRAITEMENT — reculer de séance en séance depuis `jusqu_au`.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — R-111 ② : le trou est rendu, l'appelant décide quoi en faire (le calcul se suspend, ou il dit qu'il
      enjambe un trou) ; il ne peut plus l'enjamber sans le voir. Exemple : Vinci (DG), la séance du 03-07-2026 retirée
      d'une copie, les 14 dernières séances au 10-07-2026 portent (03-07-2026, None). Relecture indépendante du
      12-10-2026 : sur la référence figée, `lire` disait « pas de trou » au-delà du 10-07-2026, et cette fonction
      rendait 14 séances vides du 22-09 au 09-10-2026 — un calcul aurait vu 14 trous que la lecture niait.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ; chaque tour recule d'un jour, et s'arrête au début du calendrier.
      [sort: non]
    """
    if n < 1:
        raise ValueError(f"n = {n} : au moins une séance")
    sc, b = cours["seances"], cours["barres"].get(m) or {}
    if cours.get("fin_du_fige") and jusqu_au > cours["fin_du_fige"]:
        jusqu_au = cours["fin_du_fige"]
    out, d = [], jusqu_au
    while len(out) < n and d >= sc["debut"]:
        if CAL.etat_du_jour(d, sc) != CAL.FERMEE:
            out.append((d, b.get(d)))
        d -= timedelta(days=1)
    return out[::-1]


def trous_de_tout_le_marche(cours):
    """Rend les séances où AUCUNE valeur en activité n'a de cours.

    ① RÔLE — La ligne A2 de la table de réception : tout le marché manque, l'indice est publié.
    ② CONTEXTE D'APPEL — `resume`.
    ③ ENTRÉE — `cours` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des dates, dans l'ordre.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque valeur du référentiel, ses trous (`trous`) ; une séance est un trou de tout le marché
      quand elle est un trou de chaque valeur attendue ce jour-là (`_attendues`) et qu'au moins une valeur l'est.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Un trou de tout le marché est le cas que le calendrier tiré des cours ne pouvait pas voir. Exemple
      mesuré le 10-10-2026 sur l'historique réparé : 24-12-2010, 31-12-2010, 24-12-2012, 31-12-2012, 31-12-2015.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    actives, manquantes = Counter(), Counter()
    for m in cours["hors_univers"]:
        for d in _attendues(cours, m):
            actives[d] += 1
        for d, _ in trous(cours, m):
            manquantes[d] += 1
    return sorted(d for d, k in manquantes.items() if k == actives[d])


def resume(cours):
    """Rend les lignes à afficher : tout ce que la lecture signale.

    ① RÔLE — Dire, en clair, chaque chose que la lecture a vue (R-109 : tout problème de cours est signalé).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `cours` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des lignes, et le nombre de choses signalées.
      [rend: 2]
    ⑥ TRAITEMENT — une ligne de bilan, puis une ligne par sorte d'anomalie présente : alertes du calendrier, liste
      d'Euronext qui s'achève dans moins de PREAVIS_DU_CALENDRIER jours, indice qui s'arrête avant la fin, écritures
      multiples, fichier figé modifié, demande au-delà d'un fichier figé (un signalement, au lieu d'un trou de tout le
      marché par séance : l'appelant a demandé une date que ce fichier ne peut pas couvrir), fichier figé allongé, noms
      et dates illisibles, doublons, conflits, barres mises à part, natures qui ne portent sur aucun
      trou, trous de tout le marché, puis les trous valeur par valeur. Une valeur de l'univers jamais lue est dite
      ABSENTE DU FICHIER ; lue mais sans aucune barre gardée (toutes en conflit, ou mises à part), AUCUNE BARRE GARDÉE ;
      les deux sont signalées même quand le fichier n'a aucune barre et que leurs trous ne se comptent pas.
    ⑦ UNITÉ — Des lignes ; des séances.
    ⑧ POURQUOI — Le message du soir reprendra ces lignes (action suivante d'A-566). L'indice qui s'arrête est signalé
      chaque fois : R-110 ③ veut que l'indice du jour dise que la Bourse était ouverte, et aucun programme ne le
      relève encore ; tant que c'est vrai, les séances d'après ne sont que PRÉVUES (relecture indépendante du
      10-10-2026 : un indice coupé au 30-06-2026 passait sans un mot). Conséquence, mesurée le même jour : sur le vrai
      fichier maître, le code 0 est inatteignable tant que l'indice n'est pas relevé chaque soir. La fin de la liste
      d'Euronext est signalée PREAVIS_DU_CALENDRIER jours avant (R-110 ② : une alerte si l'année suivante manque au
      1er décembre) ; passé sa fin, la lecture par défaut s'arrête (code 2).
    ⑨ CE QUI CLOCHE — Les trous d'une valeur sont montrés par les cinq premiers et le compte : la liste entière se
      recalcule par `trous`.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c, L = cours, []
    k = 0
    sc = c["seances"]
    L.append(f"{c['fichier']} : {sum(len(b) for b in c['barres'].values())} barres rangées, {len(c['barres'])} valeurs "
             f"(mnémoniques){'' if c['source_ecrite'] else ', fichier sans colonne de source'}"
             f"{', fichier figé (déclaré)' if c.get('fige') else ''} ; calendrier : indice du "
             f"{sc['debut']} au {sc['fin']} ; séances attendues jusqu'au {c['fin']}")
    for alerte in sc["alertes"]:
        L.append("  CALENDRIER : " + alerte)
        k += 1
    reste = (sc["euronext"]["jusqu_au"] - jusqu_au_par_defaut()).days
    if reste <= PREAVIS_DU_CALENDRIER:
        L.append(f"  CALENDRIER : la liste d'Euronext s'arrête au {sc['euronext']['jusqu_au']} ({reste} jour(s)) ; "
                 f"au-delà, toute lecture s'arrête (R-110 ② : relever l'année suivante)")
        k += 1
    if c["fin"] > sc["fin"]:
        n = len(CAL.seances_entre(sc["fin"] + timedelta(days=1), c["fin"], sc))
        L.append(f"  INDICE : publié jusqu'au {sc['fin']} seulement ; {n} séance(s) jusqu'au {c['fin']} ne sont que "
                 f"PRÉVUES par la liste d'Euronext (R-110 ③ : aucun programme ne relève encore l'indice chaque soir)")
        k += 1
    if c.get("fige_modifie"):
        L.append(f"  FICHIER FIGÉ MODIFIÉ : empreinte {c['fige_modifie'][:16]}, différente de l'empreinte déclarée "
                 f"(CONTRATS.FICHIERS_DE_COURS_FIGES) — un fichier figé ne change pas")
        k += 1
    if c.get("au_dela_du_fige"):
        L.append(f"  AU-DELÀ DU FICHIER FIGÉ : séances demandées jusqu'au {c['au_dela_du_fige']} ; le fichier est figé, "
                 f"déclaré jusqu'au {c['fin_du_fige']} : les séances d'après ne sont pas des trous ; un seul signalement")
        k += 1
    if c.get("fige_allonge"):
        a = c["fige_allonge"]
        L.append(f"  FICHIER FIGÉ ALLONGÉ : {len(a)} date(s) après la dernière séance déclarée "
                 f"(CONTRATS.FICHIERS_DE_COURS_FIGES), du {a[0]} au {a[-1]} — un fichier figé ne grandit pas")
        k += 1
    deux = {m: e for m, e in c["ecritures"].items() if len(e) > 1}
    if deux:
        L.append(f"  ÉCRITURES : {len(deux)} valeur(s) écrite(s) de plusieurs façons, réunies par leur mnémonique : "
                 + " · ".join(f"{m} ({', '.join(f'{x} {y}' for x, y in sorted(e.items()))})" for m, e in sorted(deux.items())))
        k += 1
    for titre, objet in (("NOMS SANS MNÉMONIQUE", c["inconnues"]), ("DATES ILLISIBLES", c["dates_illisibles"])):
        if objet:
            L.append(f"  {titre} : " + " · ".join(f"« {x} » {y}" for x, y in sorted(objet.items())))
            k += 1
    if c.get("anomalies_d_identite"):
        L.append(f"  IDENTITÉS : {len(c['anomalies_d_identite'])} anomalie(s) sur des sociétés sorties absentes du fichier "
                 f"(lecture poursuivie, I-1) — " + " · ".join(c["anomalies_d_identite"][:3]))
        k += 1
    if c.get("sorties_sans_cle"):
        sc_ = c["sorties_sans_cle"]
        L.append(f"  SOCIÉTÉS SORTIES SANS CLÉ (dans l'indice, aucun mnémonique pour lire leurs barres) : "
                 f"{sum(x[1] for x in sc_.values())} séance(s), {len(sc_)} société(s) — "
                 + ", ".join(f"{x[0]} {x[1]}" for x in list(sc_.values())[:5]) + (" …" if len(sc_) > 5 else ""))
        k += 1
    if c.get("ecartees"):
        L.append(f"  LIGNES ÉCARTÉES SUR DÉCISION (CONTRATS.LIGNES_ECARTEES_SUR_DECISION) : {len(c['ecartees'])} — "
                 + ", ".join(f"{v} {d}" for v, d, _ in c["ecartees"][:5]))
        k += 1
    for titre, objet in (("DOUBLONS IDENTIQUES (un gardé)", c["doublons"]),
                         ("CONFLITS (deux versions, aucune gardée)", c["conflits"]),
                         ("BARRES UN JOUR SANS SÉANCE (mises à part)", c["hors_seance"]),
                         ("BARRES HORS DU CALENDRIER (mises à part)", c["hors_calendrier"]),
                         ("NATURES QUI NE PORTENT SUR AUCUN TROU", _natures_inutiles(c))):
        if objet:
            L.append(f"  {titre} : {len(objet)} — " + ", ".join(f"{x[0]} {x[1]}" for x in objet[:5])
                     + (" …" if len(objet) > 5 else ""))
            k += 1
    marche = trous_de_tout_le_marche(c)
    if marche:
        L.append(f"  TROUS DE TOUT LE MARCHÉ : {len(marche)} — " + ", ".join(d.isoformat() for d in marche))
        k += 1
    for m in sorted(c["hors_univers"]):
        t = [x for x in trous(c, m) if x[0] not in set(marche)]
        if c["hors_univers"][m] or c["barres"].get(m):
            quoi = "TROUS"
        elif m in c["ecritures"]:
            quoi = "AUCUNE BARRE GARDÉE"
        else:
            quoi = "ABSENTE DU FICHIER"
        if t or quoi != "TROUS":
            L.append(f"  {quoi} {m} : {len(t)} trou(s)" + (" — " if t else "")
                     + ", ".join(f"{d} {n}" for d, n in t[:5]) + (" …" if len(t) > 5 else ""))
            k += 1
    return L, k


def _natures_inutiles(cours):
    """Rend les natures écrites qui ne portent sur aucun trou calculé.

    ① RÔLE — Dire qu'une nature décidée ne sert à rien, au lieu de la taire.
    ② CONTEXTE D'APPEL — `resume`.
    ③ ENTRÉE — `cours` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des (mnémonique, date) de donnees/NATURE_DES_TROUS.csv qui ne sont pas un
      trou de `trous`.
      [rend: 1]
    ⑥ TRAITEMENT — calculer les trous de chaque valeur nommée dans le fichier des natures, garder les natures hors de
      ces trous.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Seconde relecture indépendante du 10-10-2026 : une nature sur une séance qui a son cours, avant le
      début du fichier, après la fin attendue, ou après la dernière barre d'une valeur hors univers était acceptée et
      jamais montrée.
    ⑨ CE QUI CLOCHE — Une nature écrite sur une séance en conflit n'est pas utilisée (le trou porte « DEUX VERSIONS »)
      et n'est pas relevée ici.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    faits = {(m, d) for m in {k[0] for k in cours["natures"]} for d, _ in trous(cours, m)}
    return sorted(k for k in cours["natures"] if k not in faits)


def main(argv):
    """Lit le fichier des cours et affiche ce qui est signalé.

    ① RÔLE — Vérification à la main, et premier pas du compte rendu du soir.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la racine (par défaut le dossier courant), puis le fichier des cours relatif à la racine
      (par défaut donnees/cours_maitre.csv), puis la date jusqu'à laquelle chaque séance doit avoir ses cours,
      AAAA-MM-JJ (par défaut la veille, voir `lire`). Pour l'historique long, qui s'arrête au 02-10-2026 :
      python3 programmes/LIRE_LES_COURS.py . donnees/sources_yahoo/historique_long_repare.csv 2026-10-02
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie — 0 rien à signaler, 1 quelque chose l'est, 2 lecture impossible.
      [rend: 1]
    ⑥ TRAITEMENT — lire, résumer, afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul ; R-109 : ce qui est signalé se voit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        racine = argv[0] if argv else "."
        fichier = argv[1] if len(argv) > 1 else FICHIER_DES_COURS
        jusqu_au = CAL._date_stricte(argv[2]) if len(argv) > 2 else None
        cours = lire(racine, fichier, jusqu_au)
        lignes, k = resume(cours)
    except (OSError, ValueError) as e:
        print(f"LECTURE DES COURS IMPOSSIBLE : {type(e).__name__} : {e}")
        return 2
    print("\n".join(lignes))
    print(f"SIGNALÉ : {k}")
    return 1 if k else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
