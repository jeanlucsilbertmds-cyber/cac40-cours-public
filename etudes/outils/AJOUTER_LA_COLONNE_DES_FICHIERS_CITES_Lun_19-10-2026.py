#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AJOUTER_LA_COLONNE_DES_FICHIERS_CITES_Lun_19-10-2026.py — Lun 19-10-2026 (Paris). Simulation uniquement.

① RÔLE — Ajouter, une fois, la colonne `fichiers_cites` en dernière colonne des trois fichiers écrits à la main que lit la
  réparation de l'historique long (DETACHEMENTS_OFFICIELS, BARRES_BNAINS_FAUSSES, AJUSTEMENTS_DE_YAHOO), et y déplacer
  les chemins du dépôt que la colonne `source` portait dans son texte, SANS RIEN RETIRER : l'ancienne source entière est
  recopiée, datée, à la fin de la citation de chaque ligne retouchée.
② CONTEXTE D'APPEL — À la main, une fois, sur le dépôt : python3 etudes/outils/AJOUTER_LA_COLONNE_DES_FICHIERS_CITES_Lun_19-10-2026.py <racine>.
  Relancé sur un fichier qui a déjà la colonne, il s'arrête sans rien écrire.
③ ENTRÉE — La racine du dépôt.
④ CONDITIONS D'ENTRÉE — Les trois fichiers existent, sans colonne `fichiers_cites`.
⑤ SORTIE — UNE valeur : le code de sortie — 0 écrit et vérifié ; 1 la vérification a échoué (rien n'est écrit) ; 2 le
  programme n'a pas pu tourner (fichier absent, colonne déjà là).
  [rend: 1]
⑥ TRAITEMENT — Pour chaque ligne : découper `source` sur « ; ». Si chaque morceau est une adresse entière
  (`K.ADRESSE_ENTIERE`), la ligne ne change pas et `fichiers_cites` est vide. Sinon : ① une adresse suivie d'un
  commentaire garde l'adresse ; ② un chemin de fichier du dépôt passe dans `fichiers_cites` ; ③ un dossier n'est pas un
  fichier cité ; ④ le LISEZ-MOI des cours n'est pas une source d'origine : il ne passe pas dans `fichiers_cites`, et la
  ligne ACCOR 2010 cite à sa place DETACHEMENTS_OFFICIELS.csv ; ⑤ la citation reçoit, à la fin, « [source écrite jusqu'au
  19-10-2026 : <l'ancienne source entière>] ». Puis la VÉRIFICATION, avant toute écriture : chaque cellule des autres
  colonnes est identique ; la citation retouchée commence par l'ancienne citation et porte l'ancienne source entière ;
  chaque morceau de la nouvelle source est une adresse entière ; chaque fichier cité existe ; aucune ligne n'est perdue.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 19-10-2026 à 08h23 (« 1 » à « Une colonne à part pour les fichiers cités. La
  colonne source ne garde que les adresses web, et une nouvelle colonne liste les fichiers du dépôt, séparés par « ; ».
  Le contrôle les vérifie comme il vérifie déjà les fichiers lus, sans rien deviner. Le coût : retoucher 8 lignes déjà
  validées ») ; décision du même jour à 12h35 (« 1 » à « Citer la source d'origine » pour les deux lignes qui citaient le
  LISEZ-MOI : ACCOR 2010 cite la ligne Accor/Edenred des détachements officiels, CARREFOUR 2000 garde ses deux adresses,
  la mention du LISEZ-MOI reste dans la citation). L'ancienne source entière recopiée en citation, plutôt que son seul
  commentaire : superviseur n° 3 du même jour — « Preuve au dépôt : voir la source. » renverrait sinon à une colonne vide.
  La colonne en DERNIER : placée après `citation`, elle rendait rouges cinq épreuves des 20 ans (superviseur n° 3).
⑨ CE QUI CLOCHE — Les règles ④ (LISEZ-MOI, ACCOR) sont écrites ici pour ces deux lignes seulement : c'est une
  migration d'une fois, pas un programme qui doit resservir. · La réécriture par le module csv peut changer les
  guillemets d'une cellule sans changer sa valeur ; la vérification porte sur les valeurs, pas sur l'octet (mesuré par
  le superviseur n° 3 : l'aller-retour est identique à l'octet sur les trois fichiers, sans BOM ni CRLF). · La ligne
  ACCOR 2010 cite DETACHEMENTS_OFFICIELS.csv, qui n'écrit pas « 0,704727 », le facteur de Yahoo qu'elle défait : ce
  facteur vient d'une MESURE sur 64 séances, écrite dans le verdict de la ligne, pas d'un document. · La ligne
  CARREFOUR 2000 ne repose plus que sur deux sites secondaires (alphaspread, digrin) ; le « rapport annuel 2000 » que
  cite le LISEZ-MOI n'a d'adresse nulle part ; DIVISIONS_BNAINS.csv, ligne 26, serait une meilleure source, et
  l'ajouter est une décision de Jean-Luc. · L'ajout à la citation de la ligne ACCOR 2010 contient des « » ; aucun
  programme ne lit les citations d'AJUSTEMENTS_DE_YAHOO (mesuré par le superviseur n° 3), mais RELEVER, `jour_ecrit`
  et CONFRONTER liraient de tels guillemets comme une phrase du document dans DETACHEMENTS_OFFICIELS — l'ancienne
  source de sa ligne 31 n'en contient pas.
⑩ EFFET — Réécrit les trois fichiers (seulement si la vérification passe). Affiche une ligne par ligne retouchée.
⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
  [sort: non]
"""
import csv, io, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
import CONTROLER_L_HISTORIQUE_LONG as K

FICHIERS = ("donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv", "donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv",
            "donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv")
NOUVELLE = K.COLONNES_DES_SOURCES_A_LA_MAIN[2]
LISEZ_MOI = "donnees/LISEZ_MOI_LES_COURS.md"
A_SA_PLACE = {("ACCOR", "2010-07-02"): "donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv"}


def retoucher(racine, rel):
    """Rend l'en-tête, les lignes d'avant, les lignes d'après et le journal des retouches d'un fichier.

    ① RÔLE — La transformation d'un fichier, sans l'écrire. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `racine`, `rel`.
    ④ CONDITIONS D'ENTRÉE — Le fichier n'a pas encore la colonne (ValueError sinon).
    ⑤ SORTIE — QUATRE valeurs : en-tête nouveau, lignes d'avant, lignes d'après (dictionnaires), journal. [rend: 4]
    ⑥ TRAITEMENT — ⑥ du programme. ⑦ UNITÉ — — ⑧ POURQUOI — ⑧ du programme. ⑨ CE QUI CLOCHE — ⑨ du programme.
    ⑩ EFFET — Lit le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lecteur = csv.DictReader(io.StringIO(open(os.path.join(racine, rel), encoding="utf-8", newline="").read()))
    entete = list(lecteur.fieldnames)
    if NOUVELLE in entete:
        raise ValueError(f"{rel} a déjà la colonne {NOUVELLE}")
    avant = [dict(x) for x in lecteur]
    apres, journal = [], []
    for x in avant:
        y = dict(x)
        morceaux = [m.strip() for m in x["source"].split(";") if m.strip()]
        if all(K.ADRESSE_ENTIERE.fullmatch(m) for m in morceaux):
            y[NOUVELLE] = ""
            apres.append(y)
            continue
        adresses, fichiers = [], []
        for m in morceaux:
            u = K.ADRESSE_ENTIERE.match(m)
            if u:
                adresses.append(u.group(0))
                continue
            premier = m.split(",")[0].split(" ")[0].strip()
            if premier == LISEZ_MOI:
                cle = (x.get("valeur"), x.get("date"))
                if cle in A_SA_PLACE:
                    fichiers.append(A_SA_PLACE[cle])
                continue
            c, defaut = K.chemin_du_depot(racine, premier) if premier else (None, "vide")
            if defaut is None and os.path.isfile(os.path.join(racine, c)):
                fichiers.append(c)
        y["source"] = " ; ".join(adresses)
        y[NOUVELLE] = " ; ".join(dict.fromkeys(fichiers))
        y["citation"] = f"{x['citation']} [source écrite jusqu'au 19-10-2026 : {x['source']}]"
        journal.append((rel, x.get("valeur"), x.get("date") or x.get("jour_du_detachement") or x.get("premiere_seance"),
                        y["source"], y[NOUVELLE]))
        apres.append(y)
    return entete + [NOUVELLE], avant, apres, journal


def verifier(racine, entete, avant, apres):
    """Rend la liste des défauts de la transformation ; vide si rien n'est perdu.

    ① RÔLE — La preuve que rien n'est retiré. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `racine`, l'en-tête nouveau, les
    lignes d'avant et d'après. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des défauts. [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme, la vérification. ⑦ UNITÉ — — ⑧ POURQUOI — R-751 ⑩ : rien ne se supprime sans accord.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    defauts = []
    if len(avant) != len(apres):
        defauts.append(f"{len(avant)} lignes avant, {len(apres)} après")
    for n, (x, y) in enumerate(zip(avant, apres), 2):
        for c in x:
            if c not in ("source", "citation") and x[c] != y[c]:
                defauts.append(f"ligne {n} : la colonne {c} a changé")
        if y["citation"] != x["citation"] and not (y["citation"].startswith(x["citation"]) and x["source"] in y["citation"]):
            defauts.append(f"ligne {n} : la citation ne garde pas l'ancienne citation et l'ancienne source")
        for m in [m.strip() for m in y["source"].split(";") if m.strip()]:
            if not K.ADRESSE_ENTIERE.fullmatch(m):
                defauts.append(f"ligne {n} : source « {m} » n'est pas une adresse entière")
        for m in [m.strip() for m in y[NOUVELLE].split(";") if m.strip()]:
            if not os.path.isfile(os.path.join(racine, m)):
                defauts.append(f"ligne {n} : fichier cité « {m} » absent")
        if not y["source"].strip() and not y[NOUVELLE].strip():
            defauts.append(f"ligne {n} : ni adresse ni fichier cité")
    return defauts


def main(argv):
    """Transforme, vérifie, écrit ; rend le code de sortie.

    ① RÔLE — ① du programme. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — `argv` : la racine.
    ④ CONDITIONS D'ENTRÉE — ④ du programme. ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ du programme). [rend: 1]
    ⑥ TRAITEMENT — Tout transformer et tout vérifier avant d'écrire quoi que ce soit. ⑦ UNITÉ — —
    ⑧ POURQUOI — Une écriture à moitié faite laisserait deux fichiers à l'ancienne forme et un à la nouvelle.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — ⑩ du programme. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : AJOUTER_LA_COLONNE_DES_FICHIERS_CITES_Lun_19-10-2026.py <racine>")
        return 2
    racine, faits = argv[0], []
    try:
        for rel in FICHIERS:
            entete, avant, apres, journal = retoucher(racine, rel)
            defauts = verifier(racine, entete, avant, apres)
            if defauts:
                print(f"REFUS — {rel} : {defauts[0]} (et {len(defauts) - 1} de plus) ; rien n'est écrit")
                return 1
            faits.append((rel, entete, apres, journal))
    except (OSError, ValueError) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    for rel, entete, apres, journal in faits:
        sortie = io.StringIO()
        w = csv.DictWriter(sortie, fieldnames=entete, lineterminator="\n")
        w.writeheader()
        w.writerows(apres)
        open(os.path.join(racine, rel), "w", encoding="utf-8", newline="").write(sortie.getvalue())
        for j in journal:
            print("RETOUCHÉE · " + " · ".join(str(v) for v in j))
        print(f"écrit : {rel} ({len(apres)} lignes, {len(journal)} retouchée(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
