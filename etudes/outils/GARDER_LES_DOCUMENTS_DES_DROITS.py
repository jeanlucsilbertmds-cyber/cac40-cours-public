#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GARDER_LES_DOCUMENTS_DES_DROITS.py — Sam 10-10-2026 (Paris) — OUTIL, non validé. Simulation uniquement.

① RÔLE — Garder au dépôt, octet pour octet, chaque document dont l'adresse est écrite dans
  donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv (colonne `source`, et les adresses écrites dans la
  colonne `citation`), et l'inscrire au registre des documents gardés avec son empreinte. C'est le
  premier pas de la confrontation des chiffres déclarés à leurs documents
  (programmes/CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py) : on ne confronte qu'à ce qu'on a gardé.
② CONTEXTE D'APPEL — À la main, depuis la racine du dépôt, quand une ligne est ajoutée à la table :
  python3 etudes/outils/GARDER_LES_DOCUMENTS_DES_DROITS.py. Aucune tâche ne l'appelle.
③ ENTRÉE — —
④ CONDITIONS D'ENTRÉE — Le réseau ; le registre `REGISTRE` (colonnes fichier, adresse, octets, sha256).
⑤ SORTIE — UNE valeur : le code de sortie. 0 = l'outil a tourné jusqu'au bout (les adresses qu'il n'a pas pu
  garder sont AFFICHÉES, une par ligne, avec la raison) · 2 = le registre ou la table est illisible.
⑥ TRAITEMENT — ① relever les adresses de la table (`adresses_de_la_ligne`) · ② ignorer celles que le
  registre porte déjà · ③ celles qu'un autre registre de temoins/ porte déjà (les pages de bnains, les
  documents d'Accor et d'Edenred) sont inscrites en renvoyant à ce fichier, sans le copier
  (`autres_registres`) · ④ télécharger les autres ; une réponse autre que 200, ou un contenu de moins de
  `PLUS_PETIT` octets, n'est pas gardée · ⑤ un contenu déjà gardé ailleurs dans temoins/ (même empreinte)
  est inscrit en renvoyant à ce fichier · ⑥ sinon, l'écrire dans le dossier du registre sous un nom
  fabriqué (`nom_du_fichier`) et l'inscrire.
⑦ UNITÉ — Des octets ; des empreintes sha256.
⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 à 13h18 : « 1 » à « Écrire le programme qui confronte chaque
  citation et chaque chiffre déclaré à son document gardé, et refuse ce qui n'y est pas ». Relecture de
  Cowork du même jour (22cc10b) : un chiffre déclaré faux de 0,15 % passe tous les contrôles des cours ;
  seuls les documents peuvent le refuser. Ce qu'un programme peut faire, un programme le fait (R-754).
⑨ CE QUI CLOCHE — Un site qui refuse les robots (sec.gov, zonebourse, group.bnpparibas,
  societegenerale.com, mesuré le 10-10-2026 : réponse 403) ne laisse rien garder : ses chiffres restent
  « non prouvés ». · Une page qui change (presse, bnains) est gardée telle qu'elle est le jour du
  téléchargement. · Le nom fabriqué ne dit pas la nature du document (communiqué, BALO) : l'adresse le dit.
⑩ EFFET — Écrit les documents dans le dossier du registre et AJOUTE des lignes au registre ; ne réécrit
  jamais une ligne existante.
⑪ TERMINAISON — Rend la main : un nombre fini d'adresses, chaque téléchargement borné à `ATTENTE` secondes.
"""
import csv, glob, hashlib, os, re, sys, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
from CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS import REGISTRE, COLONNES_DU_REGISTRE as COLONNES, TABLE, adresses_de_la_ligne

PLUS_PETIT = 2000   # octets : les pages de refus mesurées le 10-10-2026 font de 445 à 4 819 octets ; voir ⑨ de garder()
ATTENTE = 60        # secondes par téléchargement


def autres_registres(dossier_du_registre):
    """Rend ce que les AUTRES registres de temoins/ gardent déjà : adresse → (chemin relatif au registre, sha256).

    ① RÔLE — Ne pas copier deux fois un document déjà gardé.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `dossier_du_registre` : le dossier de `REGISTRE`.
    ④ CONDITIONS D'ENTRÉE — Lancé depuis la racine du dépôt.
    ⑤ SORTIE — DEUX valeurs, en un tuple : le dictionnaire adresse → (chemin, sha256) · le dictionnaire
      sha256 → chemin de TOUS les fichiers de temoins/ (relatifs au dossier du registre).
      [rend: 2]
    ⑥ TRAITEMENT — ① chaque CSV de temoins/ (un niveau) qui porte les colonnes `adresse` et `sha256` et une
      colonne de chemin, `page` (relative à la racine) ou `fichier` (relative au dossier du CSV) · ② l'empreinte
      de chaque fichier de temoins/.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les pages de bnains (temoins/PAGES_BNAINS_DES_ACTIONS/PAGES.csv) et les documents
      d'Accor et d'Edenred (temoins/DOCUMENTS_OFFICIELS_ACCOR_EDENRED_2010/) sont déjà gardés.
    ⑨ CE QUI CLOCHE — L'empreinte de chaque fichier de temoins/ est recalculée à chaque passage (quelques
      dizaines de Mo).
    ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    par_adresse, par_empreinte = {}, {}
    for chemin in glob.glob(os.path.join("temoins", "*", "*.csv")):
        if os.path.abspath(chemin) == os.path.abspath(REGISTRE):
            continue
        with open(chemin, encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            noms = lecteur.fieldnames or []
            if "adresse" not in noms or "sha256" not in noms or not ({"page", "fichier"} & set(noms)):
                continue
            for r in lecteur:
                p = r["page"] if "page" in noms else os.path.join(os.path.dirname(chemin), r["fichier"])
                par_adresse[r["adresse"]] = (os.path.relpath(p, dossier_du_registre), r["sha256"])
    for p in glob.glob(os.path.join("temoins", "**", "*"), recursive=True):
        if os.path.isfile(p):
            par_empreinte.setdefault(hashlib.sha256(open(p, "rb").read()).hexdigest(),
                                     os.path.relpath(p, dossier_du_registre))
    return par_adresse, par_empreinte


def nom_du_fichier(valeur, jour, adresse, contenu):
    """Fabrique le nom sous lequel un document est gardé : VALEUR_ANNEE_dernier-morceau-de-l-adresse.extension.

    ① RÔLE — Un nom lisible et stable.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `valeur` : le nom de la valeur · `jour` : AAAA-MM-JJ · `adresse` · `contenu` : les octets.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom, sans dossier.
      [rend: 1]
    ⑥ TRAITEMENT — Le dernier morceau non vide du chemin de l'adresse, réduit aux lettres, chiffres, . _ - ;
      l'extension tirée des premiers octets (%PDF → .pdf ; D0CF11E0 → .doc ; sinon .html) quand il n'en a pas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les adresses de BNP Paribas et de Crédit Agricole n'ont pas d'extension.
    ⑨ CE QUI CLOCHE — Deux adresses de même dernier morceau pour la même valeur et la même année
      donneraient le même nom : `main` refuse alors d'écraser.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    morceau = [m for m in adresse.split("?")[0].split("/") if m][-1]
    morceau = re.sub(r"[^A-Za-z0-9._-]+", "_", morceau)[-80:]
    if not re.search(r"\.(pdf|doc|html?|txt)$", morceau, re.I):
        morceau += ".pdf" if contenu[:4] == b"%PDF" else ".doc" if contenu[:4] == b"\xd0\xcf\x11\xe0" else ".html"
    return f"{re.sub(r'[^A-Z0-9]+', '_', valeur.upper())}_{jour[:4]}_{morceau}"


def main():
    """Garde les documents de la table et les inscrit au registre.

    ① RÔLE — Voir l'en-tête du module.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie (0 ou 2).
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Écrit des documents et ajoute des lignes au registre. Affiche une ligne par adresse.
    ⑪ TERMINAISON — Rend la main ; chaque téléchargement est borné à `ATTENTE` secondes.
      [sort: non]
    """
    try:
        dossier = os.path.dirname(REGISTRE)
        with open(REGISTRE, encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            if lecteur.fieldnames != COLONNES:
                raise ValueError(f"{REGISTRE} : en-tête {lecteur.fieldnames} au lieu de {COLONNES}")
            deja = {r["adresse"] for r in lecteur}
        lignes = list(csv.DictReader(open(TABLE, encoding="utf-8")))
    except (OSError, ValueError, KeyError) as e:
        print("ERREUR :", e)
        return 2
    par_adresse, par_empreinte = autres_registres(dossier)
    ajouts, echecs = [], []
    for r in lignes:
        for u in adresses_de_la_ligne(r):
            if u in deja:
                continue
            deja.add(u)
            if u in par_adresse:
                chemin, empreinte = par_adresse[u]
                ajouts.append([chemin, u, os.path.getsize(os.path.join(dossier, chemin)), empreinte])
                print(f"déjà gardé ailleurs : {chemin} ← {u}")
                continue
            try:
                demande = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(demande, timeout=ATTENTE) as rep:
                    contenu = rep.read()
            except Exception as e:  # toute erreur de réseau : l'adresse n'est pas gardée, on le dit
                echecs.append(u)
                print(f"NON GARDÉ ({type(e).__name__} : {str(e)[:60]}) : {u}")
                continue
            if len(contenu) < PLUS_PETIT:
                echecs.append(u)
                print(f"NON GARDÉ (contenu de {len(contenu)} octets) : {u}")
                continue
            empreinte = hashlib.sha256(contenu).hexdigest()
            if empreinte in par_empreinte:
                chemin = par_empreinte[empreinte]
                print(f"même contenu déjà gardé : {chemin} ← {u}")
            else:
                chemin = nom_du_fichier(r["valeur"], r["jour_du_detachement"], u, contenu)
                if os.path.exists(os.path.join(dossier, chemin)):
                    echecs.append(u)
                    print(f"NON GARDÉ (le nom {chemin} est déjà pris) : {u}")
                    continue
                with open(os.path.join(dossier, chemin), "wb") as f:
                    f.write(contenu)
                par_empreinte[empreinte] = chemin
                print(f"gardé : {chemin} ({len(contenu)} octets) ← {u}")
            ajouts.append([chemin, u, len(contenu), empreinte])
    with open(REGISTRE, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(ajouts)
    print(f"inscrits au registre : {len(ajouts)} · non gardés : {len(echecs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
