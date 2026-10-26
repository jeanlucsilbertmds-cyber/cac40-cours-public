#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VERIFIER_LES_PREUVES_DU_REFERENTIEL — Sam 24-10-2026 (Paris). Simulation uniquement.

① RÔLE — Vérifier, par des propriétés et sans juger aucun nom, les trois colonnes de preuve du référentiel des valeurs
  (donnees/REFERENTIEL_VALEURS_*.csv) : source, citation, fichiers_cites. Chaque valeur doit prouver son code ISIN,
  chaque ancien ISIN que la chaîne des 20 ans lit dans source_isin (« remplace <ISIN> »), et son code de bourse avec
  le nom que Yahoo lui donne, par des ENREGISTREMENTS ENTIERS trouvés par leur clé dans les fichiers qu'elle cite ;
  aucun ISIN, aucun code n'est porté par deux lignes, et le lecteur des cours accepte les noms.
② CONTEXTE D'APPEL — À la main, avant tout dépôt qui touche le référentiel ou un fichier qu'il cite ; et par son
  épreuve, tests/EPREUVES_DES_PREUVES_DU_REFERENTIEL_Sam_24-10-2026.py, que la certification rejoue chaque nuit.
  python3 -I programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py <racine du dépôt>
  Le module est aussi importé par etudes/brouillons_chat/REFERENTIEL_PROUVE_Sam_24-10-2026/COMPLETER_LE_REFERENTIEL.py,
  qui a écrit les trois colonnes une fois : les deux lisent les fichiers cités par les MÊMES fonctions (deux
  implémentations d'une même chose divergent toujours, R-708).
③ ENTRÉE — La racine du dépôt : le référentiel, le carnet donnees/PROVENANCE_DES_FICHIERS.csv et les fichiers cités.
④ CONDITIONS D'ENTRÉE — Un seul fichier donnees/REFERENTIEL_VALEURS_*.csv ; pdftotext (poppler) installé quand un PDF
  est cité.
⑤ SORTIE — Le code de sortie : 0 si aucun défaut ; 1 s'il y a au moins un défaut ; 2 si la vérification n'a pas pu
  tourner (appel mal formé, fichier cité absent ou illisible, pdftotext absent ou en échec, ou toute erreur imprévue,
  rattrapée par le dernier filet de `main`) — un contrôle qui n'a pas pu tourner ne rend jamais 0 (R-734), et une
  panne ne se confond pas avec un défaut. L'écran : une ligne « DÉFAUT … » par défaut, puis « VERDICT … ».
  [rend: 1]
⑥ TRAITEMENT — (1) aucune clé — nom_usuel, isin, mnemonique — ne porte d'espace en bord ; (2) unicité : chaque ISIN,
  chaque ancien ISIN et chaque code n'apparaît que sur une ligne ; l'identité des noms est jugée par le lecteur des
  cours lui-même (programmes/LIRE_LES_COURS.py, `table_des_ecritures`) : deux noms rapprochés qui désignent deux
  codes, ou une ligne au mauvais nombre de cases, sont un défaut, et la vérification s'arrête là : le circuit ne
  peut pas tourner sur un fichier que le lecteur refuse (superviseur R-759 du 24-10-2026, tour 4 ; une case en moins
  faisait planter la suite et rendre 2) ; (3) pour chaque ligne, la citation est
  découpée en morceaux « <désignation> : « <texte> » » séparés par « · » ; chaque morceau doit être UN ENREGISTREMENT
  ENTIER du fichier désigné : une ligne entière d'un fichier quotidien de Paris (désignation « <archive>.ZIP › … ›
  <jour>.txt »), une ligne entière du texte d'un avis PDF (espaces resserrés), ou le membre "symbol" ou "longName" de
  la réponse de Yahoo, égal à la valeur lue dans le JSON ; (4) couverture : l'ISIN et chaque ancien ISIN ont chacun un
  morceau dont la CLÉ est la leur (premier champ de la ligne de Paris, ou ISIN écrit dans la ligne du PDF) ; la
  réponse de Yahoo dont "symbol" vaut <code>.PA est citée, et son "longName" est cité DANS CE MÊME FICHIER ; (5) chaque
  fichier cité sert à au moins un morceau, et chaque morceau désigne un fichier cité ; (6) la colonne source est
  exactement la liste des adresses que le carnet donne aux fichiers cités, dans leur ordre.
⑦ UNITÉ — —
⑧ POURQUOI — Décisions de Jean-Luc du 24-10-2026 : à 16h06 (« 1 » à « Compléter le référentiel : ajouter les trois
  colonnes, avec pour chaque valeur une adresse complète et la phrase exacte de la source ») et à 16h39 (« 1 » à
  « Ajouter dans chaque ligne aussi l'adresse d'origine »). Le contrôle de provenance K23 n'accepte un fichier écrit à
  la main que s'il porte ces colonnes (décision du 19-10-2026 à 07h05), mais il n'en vérifie que la forme. La forme de
  ce contrôle vient de deux superviseurs R-759 du 24-10-2026 : le premier essai cherchait chaque citation comme un
  morceau de texte, et le relecteur neuf a montré qu'une ligne décalée (l'ISIN d'Air Liquide sur la ligne d'Accor)
  restait verte, et qu'une citation raccourcie ou recousue passait ; le second relecteur a montré qu'un nom Yahoo
  pris dans un autre fichier, un nom en double et une clé à espace passaient encore. L'unicité rend impossible le
  décalage qui crée un doublon, et le jugement des noms par le lecteur des cours fait qu'il n'existe qu'une définition
  de leur identité ; l'enregistrement entier trouvé par sa clé, dans le fichier même qui porte la clé,
  rend impossible la citation recousue. Une clé à espace est un défaut, sans l'imiter ni la corriger : les lecteurs
  du référentiel ne la traitent pas pareil (LIRE_LES_ARCHIVES_BNAINS retire les espaces, FABRIQUER_LE_COURS_PROPRE_DE_
  YAHOO non).
⑨ CE QUI CLOCHE — L'IDENTITÉ DES NOMS N'EST PAS VÉRIFIÉE : un ISIN unique d'une société hors du CAC 40, cité par sa vraie
  ligne de Paris, passe. Le nom se juge par un relecteur, sur etudes/brouillons_chat/REFERENTIEL_PROUVE_Sam_24-10-2026/
  TABLEAU_DES_NOMS.md (décision de Jean-Luc du 17-10-2026 à 16h10 : le fond reste au relecteur). · DEUX LIGNES QUI
  ÉCHANGENT LEURS ISIN, OU LEURS CODES, AVEC LEURS CITATIONS, PASSENT : aucun doublon ne naît. Mesuré par le relecteur
  du 24-10-2026 (tour 2) : les contrôles de la chaîne des 20 ans (programmes/CONTROLER_L_HISTORIQUE_LONG.py) rougissent
  alors (K8 de 0 à 36 écarts, K15 de 0 à 47, K18 de 0 à 10), parce que les cours de Paris, rattachés par l'ISIN, ne
  s'accordent plus avec ceux de Yahoo, rattachés par le code. · CE CONTRÔLE PROUVE QU'UN ISIN A ÉTÉ CELUI DE LA SOCIÉTÉ,
  PAS QU'IL L'EST ENCORE : un ancien ISIN écrit comme actuel passe (avec « remplace » inversé, pour DSY, URW, ERF et
  STLAP, dont l'avis porte les deux sur la même ligne), et un changement d'ISIN postérieur à la preuve, non déclaré,
  passerait aussi. La chaîne des 20 ans n'en est pas touchée (elle lit l'ISIN et les anciens comme un seul ensemble) ;
  ce qui prouve qu'un ISIN est actuel, c'est le moment où il sert : programmes/COLLECTER_LE_CONSENSUS.py refuse une
  page dont l'ISIN diffère du référentiel ; pour programmes/COMBLER_LE_TROU_DEPUIS_EURONEXT.py, c'est THÉORIQUE — à
  tester (BACKLOG A-622 ⑦). · UN FICHIER CITÉ FORGÉ PASSE : l'empreinte des fichiers cités n'est pas comparée au carnet
  (une réponse de Yahoo réduite à son "symbol" et à son "longName", ou un avis PDF modifié, rendent 0 — relecteur du
  24-10-2026, tour 3, N6). Ce travail est celui de K23 (`remonter` compare l'empreinte de chaque fichier au carnet, et
  remonte chaque fichier cité par un fichier écrit à la main) ; le recopier ici ferait deux implémentations (R-708).
  · Un morceau superflu est accepté (une ligne de Paris d'une autre valeur ajoutée à la citation, tour 3, N8) : chaque
  morceau doit être entier, pas forcément utile. · CE CONTRÔLE ET LE LECTEUR DES COURS PEUVENT JUGER DEUX FICHIERS DIFFÉRENTS : ce programme exige un seul fichier
  répondant à donnees/REFERENTIEL_VALEURS_*.csv ; le lecteur prend, parmi les noms qui commencent par
  REFERENTIEL_VALEURS en majuscules et finissent par .csv, le plus récent. Avec un second fichier nommé hors du motif
  d'ici (« REFERENTIEL_VALEURS-v4_… », « referentiel_valeurs_… »), un référentiel fautif rend 0 (relecteur du
  24-10-2026, tour 4, D1). Au 24-10-2026, un seul fichier existe, et LIRE_LES_ARCHIVES_BNAINS refuse lui aussi d'en
  trouver plusieurs. LA VRAIE RÉPARATION (superviseur R-759 du tour 4) : une fonction de LIRE_LES_COURS rend les
  candidats et le fichier retenu, et table_des_ecritures comme ce programme l'emploient ; elle touche un programme
  du circuit du soir et passe sa propre boucle R-731 : décision de Jean-Luc du 24-10-2026 à 20h18 de la remettre au
  jour où ce programme sera modifié (BACKLOG A-622 ⑬). · Le nombre de valeurs n'est pas contrôlé : une ligne supprimée passe ; un garde-fou porte sur une
  propriété, jamais sur un compte. · K23, le contrôle du circuit, n'atteint ce fichier que si une fiche du carnet le
  déclare lu : depuis le 24-10-2026, les fiches du cours propre de Yahoo et des cours de Paris le déclarent (décision
  de Jean-Luc de 22h22, BACKLOG A-622 ④), et K23 compare au carnet son empreinte et celle de chaque fichier qu'il cite. · Le texte d'un PDF dépend de pdftotext en mode -layout : une autre version peut couper les lignes
  autrement et rendre des défauts sur un avis inchangé. · Les autres colonnes du référentiel ne sont pas prouvées ; la
  chaîne des 20 ans ne les lit pas. · Les anciens ISIN écrits dans le code de LIRE_LES_ARCHIVES_BNAINS (ANCIENS_ISIN)
  ne sont pas dans le référentiel et ne sont pas vérifiés ici.
⑩ EFFET — Lit le dépôt ; charge programmes/LIRE_LES_COURS.py ; lance pdftotext ; n'écrit rien.
⑪ TERMINAISON — Rend la main ; pdftotext est borné à 60 s par avis ; sort par sys.exit.
  [sort: oui]
"""
import csv
import glob
import io
import json
import os
import re
import subprocess
import sys
import zipfile

CARNET = os.path.join("donnees", "PROVENANCE_DES_FICHIERS.csv")
COLONNES = ("source", "citation", "fichiers_cites")
CLES = ("nom_usuel", "isin", "mnemonique")
SEPARATEUR = " · "
DANS = " › "
MORCEAU = re.compile(r"^(.+?) : « (.*) »$", re.S)
ANCIEN = re.compile(r"remplace ([A-Z]{2}[0-9A-Z]{10})")
UN_ISIN = re.compile(r"\b[A-Z]{2}[0-9A-Z]{9}[0-9]\b")
YAHOO = re.compile(r'^"(symbol|longName)":"(.*)"$', re.S)


class Panne(Exception):
    """La vérification ne peut pas tourner (code 2)."""


def lignes_du_quotidien(racine, archive, membres):
    """Rend les lignes d'un fichier quotidien de Paris rangé dans une archive, imbriquée ou non.

    ① RÔLE — Lire un fichier quotidien de Paris dans une archive de bnains.org.
    ② CONTEXTE D'APPEL — `verifier_une_valeur`, ici et dans le programme qui a écrit les colonnes.
    ③ ENTRÉE — `racine` · `archive` : chemin de l'archive depuis la racine · `membres` : la suite des noms de membres,
      de l'archive extérieure vers le fichier du jour.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des lignes, décodées en latin-1 (le codage des archives).
      [rend: 1]
    ⑥ TRAITEMENT — Ouvrir chaque membre dans le précédent.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les archives annuelles portent des archives mensuelles ; 201701 et 201702 portent les jours.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit une archive.
    ⑪ TERMINAISON — Rend la main ou lève Panne. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    try:
        z = zipfile.ZipFile(os.path.join(racine, archive))
        for m in membres[:-1]:
            z = zipfile.ZipFile(io.BytesIO(z.read(m)))
        return z.read(membres[-1]).decode("latin-1").splitlines()
    except (OSError, KeyError, zipfile.BadZipFile) as e:
        raise Panne(f"{archive} › {DANS.join(membres)} illisible : {e}")


def lignes_du_pdf(racine, chemin):
    """Rend les lignes du texte d'un avis PDF, espaces resserrés, lignes vides retirées.

    ① RÔLE — Lire un avis officiel en PDF.
    ② CONTEXTE D'APPEL — `verifier_une_valeur`, ici et dans le programme qui a écrit les colonnes.
    ③ ENTRÉE — `racine` · `chemin` : l'avis, depuis la racine.
    ④ CONDITIONS D'ENTRÉE — pdftotext installé.
    ⑤ SORTIE — UNE valeur : la liste des lignes.
      [rend: 1]
    ⑥ TRAITEMENT — pdftotext -layout, puis chaque ligne : espaces resserrés, bords retirés ; les lignes vides tombent.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — -layout garde les lignes d'un tableau d'avis ensemble : l'ISIN et le nom restent sur la même ligne.
    ⑨ CE QUI CLOCHE — Dépend de la version de pdftotext (voir le ⑨ du programme).
    ⑩ EFFET — Lance pdftotext.
    ⑪ TERMINAISON — Rend la main ou lève Panne ; pdftotext est borné à 60 s.
      [sort: non]
    """
    try:
        r = subprocess.run(["pdftotext", "-layout", os.path.join(racine, chemin), "-"],
                           capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Panne(f"pdftotext n'a pas pu lire {chemin} : {e}")
    if r.returncode != 0:
        raise Panne(f"pdftotext a échoué sur {chemin} (code {r.returncode})")
    lignes = (re.sub(r"\s+", " ", l).strip() for l in r.stdout.decode("utf-8", "replace").splitlines())
    return [l for l in lignes if l]


def meta_yahoo(racine, chemin):
    """Rend le bloc « meta » d'une réponse de Yahoo.

    ① RÔLE — Lire l'identité d'une valeur dans une réponse de Yahoo.
    ② CONTEXTE D'APPEL — `verifier_une_valeur`, ici et dans le programme qui a écrit les colonnes.
    ③ ENTRÉE — `racine` · `chemin` : la réponse, depuis la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire chart.result[0].meta, ou {} si la réponse n'a pas de résultat.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le JSON.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — C'est sous <code>.PA que la chaîne demande les cours à Yahoo : la réponse prouve le code tel qu'elle
      l'emploie, et "longName" dit à quelle société il répond.
    ⑨ CE QUI CLOCHE — "symbol" répète le code demandé ; c'est "longName" qui identifie la société.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève Panne. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    try:
        res = json.load(open(os.path.join(racine, chemin), encoding="utf-8"))["chart"]["result"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise Panne(f"{chemin} illisible : {e}")
    if not res:
        return {}
    return res[0].get("meta") or {}


def morceaux(citation):
    """Découpe une citation en morceaux (désignation, texte).

    ① RÔLE — Lire la forme d'une citation.
    ② CONTEXTE D'APPEL — `verifier_une_valeur`.
    ③ ENTRÉE — `citation` : le texte de la colonne citation.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des couples (désignation, texte) ; la liste des morceaux mal formés.
      [rend: 2]
    ⑥ TRAITEMENT — Couper sur « · », puis chaque morceau doit avoir la forme « <désignation> : « <texte> » ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une forme fixe permet de retrouver chaque enregistrement cité sans rien deviner.
    ⑨ CE QUI CLOCHE — Un texte cité qui contiendrait « · » serait coupé à tort ; aucun ne le contient aujourd'hui, et un
      morceau coupé à tort ne serait plus un enregistrement entier : il rougirait, il ne passerait pas.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    bons, mauvais = [], []
    for m in citation.split(SEPARATEUR):
        x = MORCEAU.match(m.strip())
        if x:
            bons.append((x.group(1), x.group(2)))
        else:
            mauvais.append(m.strip())
    return bons, mauvais


def adresses_du_carnet(racine):
    """Rend, pour chaque fichier inscrit au carnet, ses adresses.

    ① RÔLE — Lire les adresses d'origine au carnet de provenance.
    ② CONTEXTE D'APPEL — `verifier`, et le programme qui a écrit les colonnes.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire fichier → liste des adresses de ses lignes.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le carnet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La colonne source recopie les adresses du carnet : elles se comparent, elles ne se devinent pas.
    ⑨ CE QUI CLOCHE — Recopier l'adresse est une seconde écriture d'un fait du carnet (R-708) ; c'est la décision de
      Jean-Luc du 24-10-2026 à 16h39, et ce contrôle compare les deux pour que la copie ne dérive pas.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève Panne.
      [sort: non]
    """
    try:
        lus = list(csv.DictReader(open(os.path.join(racine, CARNET), encoding="utf-8-sig", newline="")))
    except OSError as e:
        raise Panne(f"carnet illisible : {e}")
    a = {}
    for r in lus:
        a.setdefault(r["fichier"], []).append(r["adresse"])
    return a


def verifier_une_valeur(racine, r, carnet, cache):
    """Rend les défauts de la preuve d'une ligne.

    ① RÔLE — Vérifier la preuve d'une ligne du référentiel.
    ② CONTEXTE D'APPEL — `verifier`.
    ③ ENTRÉE — `racine` · `r` : la ligne · `carnet` : rendu par `adresses_du_carnet` · `cache` : les fichiers déjà lus.
    ④ CONDITIONS D'ENTRÉE — La ligne porte les trois colonnes.
    ⑤ SORTIE — UNE valeur : la liste des défauts, en textes.
      [rend: 1]
    ⑥ TRAITEMENT — Les étapes (3) à (6) du ⑥ du programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir le ⑧ du programme.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme.
    ⑩ EFFET — Lit les fichiers cités.
    ⑪ TERMINAISON — Rend la main ou lève Panne.
      [sort: non]
    """
    code, isin = r["mnemonique"], r["isin"]
    d = []
    cites = [f for f in r["fichiers_cites"].split(";") if f]
    par_nom = {os.path.basename(f): f for f in cites}
    bons, mauvais = morceaux(r["citation"])
    d += [f"{code} : morceau de citation mal formé : « {m[:60]} »" for m in mauvais]
    cles, utilises, yahoo, symboles = set(), set(), {}, set()
    for designation, texte in bons:
        parties = designation.split(DANS)
        f = par_nom.get(parties[0])
        if f is None:
            d.append(f"{code} : « {designation} » ne désigne aucun fichier cité")
            continue
        utilises.add(f)
        if f.upper().endswith(".ZIP"):
            if len(parties) < 2:
                d.append(f"{code} : « {designation} » ne dit pas quel fichier du jour")
                continue
            cle = (f,) + tuple(parties[1:])
            if cle not in cache:
                cache[cle] = lignes_du_quotidien(racine, f, parties[1:])
            if texte not in cache[cle]:
                d.append(f"{code} : « {texte[:60]} » n'est pas une ligne entière de {designation}")
                continue
            cles.add(texte.split("\t")[0])
        elif f.lower().endswith(".pdf"):
            if f not in cache:
                cache[f] = lignes_du_pdf(racine, f)
            if texte not in cache[f]:
                d.append(f"{code} : « {texte[:60]} » n'est pas une ligne entière de {designation}")
                continue
            cles.update(UN_ISIN.findall(texte))
        elif f.endswith(".json"):
            if f not in cache:
                cache[f] = meta_yahoo(racine, f)
            y = YAHOO.match(texte)
            if not y or cache[f].get(y.group(1)) != y.group(2):
                d.append(f"{code} : « {texte[:60]} » n'est pas un membre de {designation}")
                continue
            yahoo.setdefault(f, set()).add(y.group(1))
            if y.group(1) == "symbol":
                symboles.add((y.group(2), f))
        else:
            d.append(f"{code} : {f} n'est ni une archive de Paris, ni un avis PDF, ni une réponse de Yahoo")
    for k in [isin] + ANCIEN.findall(r["source_isin"]):
        if k not in cles:
            d.append(f"{code} : aucun enregistrement entier cité n'a pour clé {k}")
    fichiers_du_code = [f for (s, f) in symboles if s == code + ".PA"]
    if not fichiers_du_code:
        d.append(f"{code} : aucune réponse de Yahoo citée n'a pour \"symbol\" {code}.PA")
    elif not any("longName" in yahoo.get(f, ()) for f in fichiers_du_code):
        d.append(f"{code} : le \"longName\" n'est pas cité dans la réponse de Yahoo dont le \"symbol\" vaut {code}.PA")
    for f in cites:
        if f not in utilises:
            d.append(f"{code} : {f} est cité mais ne sert à aucun morceau")
    attendu = []
    for f in cites:
        if f not in carnet:
            d.append(f"{code} : {f} n'est pas au carnet")
            continue
        attendu += [a for a in carnet[f] if a and a not in attendu]
    if r["source"] != ";".join(attendu):
        d.append(f"{code} : la colonne source n'est pas la liste des adresses que le carnet donne aux fichiers cités")
    return d


def identite_des_noms(racine):
    """Rend le refus du lecteur des cours, s'il refuse le référentiel.

    ① RÔLE — Faire juger l'identité des noms par la seule définition qu'en a le dépôt.
    ② CONTEXTE D'APPEL — `verifier`, une fois.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — programmes/LIRE_LES_COURS.py et ses voisins (COMMUN, CONTRATS_DES_FICHIERS,
      CALENDRIER_DE_LA_BOURSE) sont à côté de ce programme.
    ⑤ SORTIE — UNE valeur : la liste des défauts, vide ou d'un seul texte.
      [rend: 1]
    ⑥ TRAITEMENT — Charger LIRE_LES_COURS depuis le dossier de ce programme et appeler `table_des_ecritures` : un
      ValueError (deux écritures rapprochées qui désignent deux codes, une ligne au mauvais nombre de cases) est un
      défaut. Toute autre erreur remonte au dernier filet de `main` (code 2) : `verifier` a déjà ouvert le référentiel,
      un OSError ici ne peut venir que d'un fichier disparu entre-temps, et aucun cas ne saurait l'exercer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le lecteur rapproche le nom usuel ET le nom d'onglet, par COMMUN.norm_valeur et sa table
      d'équivalences, espaces de bord retirés : « Accor » sur la ligne AI passait ici et y était refusé (relecteur du
      24-10-2026, tour 3, N1). Le superviseur R-759 du même tour : importer seulement norm_valeur aurait recopié une
      partie de la règle ; appeler la fonction est la seule définition, utilisée deux fois (R-708).
    ⑨ CE QUI CLOCHE — Le chargement de LIRE_LES_COURS exécute son module (lecture de ses voisins) : s'il échoue, le
      dernier filet de `main` rend 2. · LIRE_LES_COURS prend le référentiel le plus récent par la date de son nom, ce
      programme exige qu'il n'y en ait qu'un : avec un seul, c'est le même fichier.
    ⑩ EFFET — Lit le référentiel et les modules voisins ; n'écrit pas leur cache de compilation (relecteur du
      24-10-2026, tour 4, D5 : sans ce réglage, le chargement écrivait programmes/__pycache__).
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    import importlib.util
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("LIRE_LES_COURS", os.path.join(ici, "LIRE_LES_COURS.py"))
    lecteur = importlib.util.module_from_spec(spec)
    avant = sys.dont_write_bytecode
    sys.dont_write_bytecode = True                      # le chargement n'écrit pas programmes/__pycache__
    try:
        spec.loader.exec_module(lecteur)
    finally:
        sys.dont_write_bytecode = avant                 # rétabli : le programme qui importe ce module garde son réglage
    try:
        lecteur.table_des_ecritures(racine)
    except ValueError as e:
        return [f"le lecteur des cours refuse le référentiel : {e}"]
    return []


def verifier(racine):
    """Rend les défauts des preuves du référentiel.

    ① RÔLE — Le contrôle entier, sans l'écran.
    ② CONTEXTE D'APPEL — `main` ; le programme qui a écrit les colonnes, pour se contrôler avant d'écrire.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Voir le ④ du programme.
    ⑤ SORTIE — UNE valeur : la liste des défauts.
      [rend: 1]
    ⑥ TRAITEMENT — Les étapes (1) et (2) du ⑥ du programme, `identite_des_noms` — s'il rend un refus, la vérification
      s'arrête là et rend les défauts trouvés jusque-là avec ce refus —, puis `verifier_une_valeur` pour chaque ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir le ⑧ du programme.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme.
    ⑩ EFFET — Lit le dépôt.
    ⑪ TERMINAISON — Rend la main ou lève Panne.
      [sort: non]
    """
    refs = glob.glob(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS_*.csv"))
    if len(refs) != 1:
        raise Panne(f"{len(refs)} référentiel(s) trouvé(s) au lieu d'un")
    try:
        lus = list(csv.DictReader(open(refs[0], encoding="utf-8-sig", newline="")))
    except OSError as e:
        raise Panne(f"référentiel illisible : {e}")
    if not lus:
        return ["référentiel vide"]
    manque = [c for c in COLONNES + CLES + ("source_isin",) if c not in lus[0]]
    if manque:
        return [f"référentiel sans les colonnes {', '.join(manque)}"]
    d, vus = [], {}
    for n, r in enumerate(lus, start=2):                 # la clé de la ligne est son rang, jamais son code
        for c in CLES:
            if r[c] != r[c].strip():
                d.append(f"ligne {n} : la colonne {c} porte une espace en bord : « {r[c]} »")
        for k in set([r["isin"], r["mnemonique"]] + ANCIEN.findall(r["source_isin"])):
            if k in vus:
                d.append(f"{k} est porté par deux lignes du référentiel : la ligne {vus[k]} et la ligne {n}")
            vus.setdefault(k, n)
    refus = identite_des_noms(racine)
    if refus:                                           # le lecteur refuse le fichier : vérifier ses lignes n'a plus de sens
        return d + refus
    carnet, cache = adresses_du_carnet(racine), {}
    for r in lus:
        d += verifier_une_valeur(racine, r, carnet, cache)
    return d


def main(argv):
    """Lance le contrôle et rend son code de sortie.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : le nom du programme, puis la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie 0, 1 ou 2 (voir le ⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — Appeler `verifier`, écrire chaque défaut puis le verdict ; une Panne ou une erreur imprévue
      (Exception, jamais SystemExit ni KeyboardInterrupt) rend « VERDICT IMPOSSIBLE » et 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une panne ne doit pas passer pour un défaut trouvé (relecteur du 24-10-2026, tour 2 : une case
      manquante levait AttributeError et rendait 1).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(argv) != 2 or not os.path.isdir(argv[1]):
        print(__doc__.split("③")[0])
        print("VERDICT IMPOSSIBLE — appel mal formé")
        return 2
    try:
        d = verifier(argv[1])
    except Panne as e:
        print(f"VERDICT IMPOSSIBLE — {e}")
        return 2
    except Exception as e:                                # dernier filet : une erreur imprévue n'est pas un défaut
        print(f"VERDICT IMPOSSIBLE — erreur imprévue : {type(e).__name__} : {e}")
        return 2
    for x in d:
        print("DÉFAUT", x)
    print("VERDICT", "CONFORME — aucun défaut" if not d else f"{len(d)} DÉFAUT(S)")
    return 0 if not d else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
