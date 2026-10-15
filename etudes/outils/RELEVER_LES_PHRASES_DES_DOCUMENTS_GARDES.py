#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES.py — Sam 10-10-2026 (Paris) — OUTIL, non validé. Simulation uniquement.

① RÔLE — Remplir la colonne `phrases_des_documents_gardes` de donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv :
  pour chaque ligne, chaque phrase de la citation écrite entre « » qui se trouve, mot pour mot, dans l'un des
  documents GARDÉS que la ligne invoque, est inscrite « fichier :: phrase ». Les phrases entre « » qui ne sont
  dans aucun de ces documents (presse non gardée, mots de Jean-Luc, rubriques) sont AFFICHÉES, pour une
  lecture humaine, et ne sont pas inscrites.
② CONTEXTE D'APPEL — À la main, depuis la racine du dépôt, après etudes/outils/GARDER_LES_DOCUMENTS_DES_DROITS.py :
  python3 etudes/outils/RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES.py. Aucune tâche ne l'appelle.
③ ENTRÉE — —
④ CONDITIONS D'ENTRÉE — La table porte les colonnes de son contrat, les deux colonnes ajoutées le 10-10-2026
  (`phrases_des_documents_gardes`, `chiffres_sans_document`) pouvant manquer (avant son premier passage) ; le registre ; les outils d'extraction (voir programmes/CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py).
⑤ SORTIE — UNE valeur : le code de sortie. 0 = la table est écrite · 2 = rien n'est écrit (table ou registre
  illisible, document gardé modifié, extraction impossible).
⑥ TRAITEMENT — ① lire le registre (`C.lire_le_registre`) ; un document modifié arrête tout · ② pour chaque
  ligne, les documents qu'elle invoque (`C.documents_invoques`) · ③ chaque phrase entre « » d'au moins `PLUS_COURTE`
  signes, cherchée dans ces documents dans l'ordre du registre (`C.phrase_dans_le_texte`) ; la première qui
  la contient est la sienne · ④ garder les entrées déjà dans la colonne et ajouter les nouvelles, sans doublon ·
  ⑤ réécrire la table, colonnes du contrat, le reste à l'identique.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 à 13h18 (voir programmes/CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py,
  ⑧). Ce qu'un programme peut faire, un programme le fait (R-754) : relever à la main 32 lignes de phrases
  ferait des fautes de recopie, que la confrontation refuserait ensuite.
⑨ CE QUI CLOCHE — Une phrase présente dans DEUX documents de la ligne est attribuée au premier du registre. ·
  Une phrase que la mise en page coupe autrement que la citation n'est pas trouvée : elle est affichée, et
  peut être ajoutée à la main à la colonne, où la confrontation la jugera. · Une phrase courte (« 26,75
  euros ») est inscrite si elle est dans le document : elle prouve un chiffre sans en dire le contexte.
⑩ EFFET — RÉÉCRIT donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv (seule la colonne des phrases change ; la
  colonne des raisons, absente, est ajoutée vide).
  Affiche, par ligne, le nombre de phrases inscrites et les phrases non trouvées.
⑪ TERMINAISON — Rend la main : un nombre fini de lignes et de documents.
"""
import csv, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
import CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS as C
from CONTRATS_DES_FICHIERS import DETACHEMENTS_OFFICIELS

PLUS_COURTE = 6   # signes, après `C.forme` : « 1 » ou « Ex » ne prouvent rien


def main():
    """Remplit la colonne et réécrit la table.

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
    ⑩ EFFET — Réécrit la table ; affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        documents, changes = C.lire_le_registre(".")
        if changes:
            raise ValueError(f"documents gardés modifiés : {changes}")
        with open(C.TABLE, encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            nouvelles_colonnes = [C.COLONNE, C.COLONNE_RAISONS]
            if [c for c in DETACHEMENTS_OFFICIELS if c not in nouvelles_colonnes] != \
                    [c for c in (lecteur.fieldnames or []) if c not in nouvelles_colonnes] or \
                    not set(lecteur.fieldnames) <= set(DETACHEMENTS_OFFICIELS):
                raise ValueError(f"{C.TABLE} : en-tête {lecteur.fieldnames}")
            lignes = list(lecteur)
        textes = {}
        for r in lignes:
            nom = f"{r['valeur']} {r['jour_du_detachement']}"
            invoques = C.documents_invoques(r, documents)
            entrees = [f"{f}{C.ENTRE_FICHIER_ET_PHRASE}{p}" for f, p in C.phrases_de_la_ligne(r)]
            nouvelles, absentes = 0, []
            for q in re.findall(r"«([^»]*)»", r["citation"]):
                q = q.strip()
                if len(C.forme(q)) < PLUS_COURTE:
                    continue
                trouve = None
                for f in invoques:
                    if f not in textes:
                        textes[f] = C.texte_du_document(documents[f][0])
                    if C.phrase_dans_le_texte(q, textes[f]):
                        trouve = f
                        break
                if trouve is None:
                    absentes.append(q)
                    continue
                e = f"{trouve}{C.ENTRE_FICHIER_ET_PHRASE}{q}"
                if e not in entrees:
                    entrees.append(e)
                    nouvelles += 1
            r[C.COLONNE] = C.ENTRE_LES_PHRASES.join(entrees)
            print(f"{nom:32} documents invoqués et gardés {len(invoques)} · phrases inscrites {len(entrees)} "
                  f"(nouvelles {nouvelles}) · entre « » non trouvées {len(absentes)}")
            for q in absentes:
                print(f"      non trouvée : « {q[:100]} »")
    except Exception as e:  # rien n'est écrit si quoi que ce soit a échoué
        print(f"RIEN N'EST ÉCRIT : {type(e).__name__} : {e}")
        return 2
    for r in lignes:
        r.setdefault(C.COLONNE_RAISONS, "")
    with open(C.TABLE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=DETACHEMENTS_OFFICIELS, lineterminator="\n")
        w.writeheader()
        w.writerows(lignes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
