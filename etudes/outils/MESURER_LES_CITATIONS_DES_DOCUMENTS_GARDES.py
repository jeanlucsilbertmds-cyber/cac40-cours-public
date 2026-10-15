#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MESURER_LES_CITATIONS_DES_DOCUMENTS_GARDES.py — Sam 10-10-2026 (Paris) — ÉTUDE, non validé. Simulation uniquement.

① RÔLE — Pour chaque ligne de donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv dont le document-source est gardé
  au dépôt, chercher chaque phrase citée entre « » dans le texte de ce document, et dire lesquelles n'y sont pas.
② CONTEXTE D'APPEL — À la main : python3 etudes/outils/MESURER_LES_CITATIONS_DES_DOCUMENTS_GARDES.py (depuis la
  racine du dépôt). Aucune tâche ne l'appelle.
③ ENTRÉE — —
④ CONDITIONS D'ENTRÉE — `pdftotext` installé ; la liste des documents gardés,
  temoins/DOCUMENTS_DES_DROITS_REGLE_OFFICIELLE_Sam_10-10-2026/DOCUMENTS.csv (fichier, adresse, octets, sha256).
⑤ SORTIE — Le code de sortie 0 ; une ligne par ligne de la table dont le document est gardé, et chaque phrase absente.
⑥ TRAITEMENT — ① extraire le texte de chaque document gardé (`pdftotext -layout`), espaces et apostrophes ramenés
  à une forme · ② pour chaque ligne dont la colonne source est l'adresse d'un document gardé, les phrases entre « »
  de plus de `LONGUEUR` signes · ③ une phrase est trouvée quand ses `PREFIXE` premiers signes sont dans le texte.
⑦ UNITÉ — Des nombres de phrases.
⑧ POURQUOI — Relecture de Cowork du 10-10-2026 (22cc10b) : deux phrases de BNP Paribas 2006, attribuées depuis le
  07-10-2026 au BALO du 06-03-2006, n'y sont pas — elles sont dans la note d'opération. Premier jet de la mesure que
  Cowork propose d'ériger en contrôle (R-754), gardé ici pour que sa sortie se rejoue.
⑨ CE QUI CLOCHE — Une phrase coupée par une mise en page en colonnes est déclarée absente (« Cotation du droit
  préférentiel de souscription »). · Le préfixe peut retrouver une phrase commune à deux documents. · Les phrases
  entre « » qui ne sont pas du document (mots de Jean-Luc, presse nommée) sont listées absentes : la lecture reste
  humaine. · Un document non gardé n'est pas confronté.
⑩ EFFET — Affiche. N'écrit rien.
⑪ TERMINAISON — Rend la main : un nombre fini de documents et de lignes.
"""
import csv, re, subprocess

LONGUEUR = 25      # signes : plus court, ce n'est pas une phrase (un « 1 » de Jean-Luc, un nom de rubrique)
PREFIXE = 60       # signes : assez pour être propre au document, assez court pour passer une fin de ligne coupée
DOSSIER = "temoins/DOCUMENTS_DES_DROITS_REGLE_OFFICIELLE_Sam_10-10-2026/"


def forme(x):
    """Rend le texte aux espaces regroupées, apostrophes droites, espaces insécables ordinaires.

    ① RÔLE — Comparer une citation à un texte extrait d'un PDF. ② CONTEXTE D'APPEL — le programme.
    ③ ENTRÉE — `x` : un texte. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte ramené.
      [rend: 1]
    ⑥ TRAITEMENT — Remplacer ’ par ', l'espace insécable par une espace, regrouper les blancs.
    ⑦ UNITÉ — — ⑧ POURQUOI — pdftotext et les citations n'écrivent pas l'apostrophe ni les blancs pareil.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return re.sub(r"\s+", " ", x.replace("’", "'").replace(" ", " "))


docs = {r["adresse"]: forme(subprocess.run(["pdftotext", "-layout", DOSSIER + r["fichier"], "-"],
                                             capture_output=True, text=True).stdout)
        for r in csv.DictReader(open(DOSSIER + "DOCUMENTS.csv", encoding="utf-8"))}
for r in csv.DictReader(open("donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv", encoding="utf-8")):
    if r["source"] not in docs:
        continue
    t = docs[r["source"]]
    phrases = [q.strip() for q in re.findall(r"«([^»]*)»", r["citation"]) if len(q.strip()) > LONGUEUR]
    absentes = [q for q in phrases if forme(q)[:PREFIXE] not in t]
    print(f"{r['valeur']:18} {r['jour_du_detachement']} : {len(phrases)} phrases entre « » de plus de {LONGUEUR} signes · "
          f"absentes du document de la ligne : {len(absentes)}")
    for q in absentes:
        print("      absente :", q[:90])
