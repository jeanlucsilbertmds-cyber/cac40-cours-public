#!/usr/bin/env python3
"""EPREUVE_UNE_STATION_PAR_FICHE — chaque fiche du registre des stratégies porte exactement une station.

① RÔLE — Vérifier la règle R-513 du REGISTRE : l'état d'une stratégie se lit à un seul endroit,
  la colonne `etat_vie` de la dernière ligne de sa fiche dans `donnees/cac40_strategies.csv` ;
  la colonne `statut` s'en déduit par la table de R-513 et ne peut pas la contredire. Une fiche
  sans état connu (aucune station) ou dont le `statut` contredit l'état (deux stations) rougit.
② CONTEXTE D'APPEL — Lancé à la main ou par une relecture, depuis la racine d'une copie du dépôt :
  `python3 tests/EPREUVE_UNE_STATION_PAR_FICHE_Mer_04-11-2026.py [--racine DOSSIER] [--saboter]`.
  Il n'est inscrit à aucun circuit (voir ⑨).
③ ENTRÉE — Deux fichiers lus sous la racine : `gouvernance/REGISTRE_REGLES.md` (la table de R-513)
  et `donnees/cac40_strategies.csv` (le registre des stratégies, séparateur virgule, UTF-8).
  Option `--saboter` : rejoue l'épreuve sur des cas fabriqués qui doivent rougir, et sur un cas
  qui doit rester vert, sans toucher aux fichiers.
④ CONDITIONS D'ENTRÉE — Le REGISTRE porte une puce `- **R-513**` suivie de sa table, dont l'en-tête
  commence par « | etat_vie ». Le CSV a les colonnes `id`, `statut` et `etat_vie`.
⑤ SORTIE — UN code de sortie : 0 = chaque fiche porte exactement une station · 1 = au moins une
  fiche sans station ou à deux stations, chacune nommée à l'écran · 2 = l'épreuve n'a pas pu
  tourner (table introuvable ou vide, fichier ou colonne absents), raison à l'écran (R-734bis).
  Avec `--saboter` : 0 si chaque sabotage a rougi et le cas témoin est resté vert, 1 sinon.
⑥ TRAITEMENT — Lire la table de R-513 dans le REGISTRE ; lire le CSV ; garder la dernière ligne de
  chaque `id` ; pour chacune, chercher son `etat_vie` dans la table, puis comparer son `statut`
  au statut déduit ; écrire un verdict par fiche fautive, puis un bilan.
⑦ UNITÉ — Des fiches (une par `id`).
⑧ POURQUOI — Lot G du plan du 31-10-2026 : « chaque fiche porte exactement une station de la règle
  du chemin, une fiche à deux états fait rougir ». La table vit au REGISTRE et jamais ici : si la
  règle change, l'épreuve suit sans être réécrite (R-743 ② ; « réparer par une propriété »).
⑨ CE QUI CLOCHE — Sur le registre du 04-11-2026, l'épreuve rougissait pour MA200-S1 (`statut`
  « ✅ VALIDÉE », `etat_vie` LABO). Réparé le 09-11-2026 par une ligne AJOUTÉE (« 🔍 EN COURS DE
  TEST », décision de Jean-Luc du 08-11-2026 à 23h04, « Retire validé. »), la ligne close restant
  telle quelle (R-727) : l'épreuve lit la dernière ligne et passe au vert ; elle est inscrite à
  `tests/LANCEMENT_DES_EPREUVES.json`. Elle ne vérifie pas encore la station du catalogue
  (R-512), qui n'est pas un fichier de données.
⑩ EFFET — Écrit à l'écran seulement ; aucun fichier écrit.
⑪ TERMINAISON — Rend la main avec son code de sortie ; aucun de ses appels ne peut ne pas revenir
  (lectures de fichiers locaux seulement).
  [sort: oui]
"""

import argparse
import csv
import io
import os
import re
import sys

PUCE_R513 = re.compile(r"^- \*\*R-513\*\*", re.M)
LIGNE_DE_TABLE = re.compile(r"^\s*\|(.+)\|\s*$")
VALEUR_EN_CODE = re.compile(r"`([^`]*)`")


def lire_la_table(texte_registre):
    """Rend la table de R-513 : {etat_vie: statut déduit, ou None si seule la case vide est admise}.

    ① RÔLE — Extraire du texte du REGISTRE la table qui relie chaque état de vie à son statut affiché.
    ② CONTEXTE D'APPEL — `eprouver`, une fois par lancement.
    ③ ENTRÉE — `texte_registre` : le texte entier de `gouvernance/REGISTRE_REGLES.md`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire, vide si la puce de R-513 ou sa table manque.
      [rend: 1]
    ⑥ TRAITEMENT — trouver la puce `- **R-513**` ; à partir d'elle, prendre la première table dont
      l'en-tête commence par « etat_vie », jusqu'à la première ligne qui n'est plus une ligne de
      table ; pour chaque ligne de données, la clé est le texte en code de la 1re cellule, la
      valeur le texte en code de la 3e cellule, ou None si elle n'en porte pas (« — »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La table vit au REGISTRE (R-513) : l'épreuve la lit, elle ne la recopie pas (R-708).
    ⑨ CE QUI CLOCHE — Une deuxième table « etat_vie » plus bas dans R-513 serait ignorée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = PUCE_R513.search(texte_registre)
    if not m:
        return {}
    lignes = texte_registre[m.start():].splitlines()
    table, dans_la_table = {}, False
    for ligne in lignes:
        lt = LIGNE_DE_TABLE.match(ligne)
        if not dans_la_table:
            if lt and lt.group(1).strip().lower().startswith("etat_vie"):
                dans_la_table = True
            continue
        if not lt:
            break
        cellules = [c.strip() for c in lt.group(1).split("|")]
        if len(cellules) < 3 or set(cellules[0]) <= set("-: "):
            continue
        cle = VALEUR_EN_CODE.findall(cellules[0])
        if not cle:
            continue
        deduit = VALEUR_EN_CODE.findall(cellules[2])
        table[cle[0]] = deduit[0] if deduit else None
    return table


def juger_les_fiches(table, texte_csv):
    """Rend la liste des fiches fautives et le nombre de fiches lues.

    ① RÔLE — Appliquer R-513 à chaque fiche du registre des stratégies.
    ② CONTEXTE D'APPEL — `eprouver` et `saboter`.
    ③ ENTRÉE — `table` : la table rendue par `lire_la_table` · `texte_csv` : le texte du CSV.
    ④ CONDITIONS D'ENTRÉE — Le CSV a les colonnes `id`, `statut`, `etat_vie` (sinon KeyError).
    ⑤ SORTIE — DEUX valeurs : la liste de (id, motif) des fiches fautives ; le nombre de fiches.
      [rend: 2]
    ⑥ TRAITEMENT — garder la dernière ligne de chaque `id` (n°83 : la dernière ajoutée fait foi) ;
      `etat_vie` absent de la table → « AUCUNE STATION » ; `statut` non vide et différent du
      statut déduit (ou non vide quand seule la case vide est admise) → « DEUX STATIONS ».
    ⑦ UNITÉ — Des fiches.
    ⑧ POURQUOI — R-513 ① et ②.
    ⑨ CE QUI CLOCHE — Les espaces en bord de case sont retirés avant comparaison ; une différence
      invisible (espace insécable au milieu) serait comptée comme deux stations.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lecteur = csv.DictReader(io.StringIO(texte_csv))
    if lecteur.fieldnames is None or not {"id", "statut", "etat_vie"} <= set(lecteur.fieldnames):
        raise KeyError("colonnes id, statut, etat_vie attendues dans le registre des stratégies")
    derniere = {}
    for ligne in lecteur:
        derniere[ligne["id"].strip()] = ligne
    fautives = []
    for ident, ligne in derniere.items():
        etat = (ligne["etat_vie"] or "").strip()
        statut = (ligne["statut"] or "").strip()
        if etat not in table:
            fautives.append((ident, f"AUCUNE STATION : etat_vie « {etat} » absent de la table de R-513"))
            continue
        deduit = table[etat]
        if statut and statut != (deduit or ""):
            attendu = f"« {deduit} » ou vide" if deduit else "vide"
            fautives.append((ident, f"DEUX STATIONS : etat_vie « {etat} » et statut « {statut} » (attendu {attendu})"))
    return fautives, len(derniere)


def eprouver(racine):
    """Lance l'épreuve sur les vrais fichiers de `racine` et rend le code de sortie.

    ① RÔLE — Le geste principal : lire, juger, afficher, rendre 0, 1 ou 2.
    ② CONTEXTE D'APPEL — `main`, sans `--saboter`.
    ③ ENTRÉE — `racine` : le dossier racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir la fiche du fichier, ⑤).
      [rend: 1]
    ⑥ TRAITEMENT — lire les deux fichiers ; une lecture impossible, une table vide ou une colonne
      absente rendent 2 ; sinon juger et afficher chaque fiche fautive, puis le bilan.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734bis : un contrôle qui n'a pas pu tourner rend un code non nul.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin_reg = os.path.join(racine, "gouvernance", "REGISTRE_REGLES.md")
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import CONTRATS_DES_FICHIERS as C   # le nom du registre se lit au contrat (G1 de EPREUVES_DU_REGISTRE_DES_STRATEGIES)
    chemin_csv = C.chemin_du_registre(racine)
    try:
        with open(chemin_reg, encoding="utf-8") as f:
            texte_reg = f.read()
        with open(chemin_csv, encoding="utf-8", newline="") as f:
            texte_csv = f.read()
    except OSError as e:
        print(f"IMPOSSIBLE — lecture : {e}")
        return 2
    table = lire_la_table(texte_reg)
    if not table:
        print("IMPOSSIBLE — la table de R-513 est introuvable ou vide dans le REGISTRE")
        return 2
    try:
        fautives, n = juger_les_fiches(table, texte_csv)
    except KeyError as e:
        print(f"IMPOSSIBLE — {e}")
        return 2
    print(f"Table de R-513 lue : {len(table)} états — {', '.join(sorted(table))}")
    for ident, motif in fautives:
        print(f"ROUGE  {ident} : {motif}")
    if fautives:
        print(f"ROUGE — {len(fautives)} fiche(s) sur {n} ne portent pas exactement une station")
        return 1
    print(f"VERT — {n} fiches, chacune porte exactement une station")
    return 0


def saboter(racine):
    """Rejoue l'épreuve sur des cas fabriqués : chaque sabotage doit rougir, le témoin rester vert.

    ① RÔLE — Prouver que l'épreuve a des dents (« une épreuve qui reste verte quand on retire ce
      qu'elle teste est une décoration », instructions du projet, §7).
    ② CONTEXTE D'APPEL — `main`, avec `--saboter`.
    ③ ENTRÉE — `racine` : le dossier racine d'une copie du dépôt (on y lit la vraie table).
    ④ CONDITIONS D'ENTRÉE — La table de R-513 est lisible.
    ⑤ SORTIE — UNE valeur : 0 si chaque cas a rendu ce qu'il devait, 1 sinon, 2 si la table manque.
      [rend: 1]
    ⑥ TRAITEMENT — S1 une fiche à deux stations (LABO et « ⭐ VIVANTE ») → rouge ; S2 un état
      inconnu → rouge ; S3 un état vide → rouge ; S4 une fiche à deux lignes dont la DERNIÈRE est
      à deux stations → rouge ; S5 la table retirée du REGISTRE → table vide (code 2 attendu) ;
      S6 le statut « ✅ VALIDÉE » de MA200-S1, copié tel quel d'une vraie ligne du registre
      (R-732) → rouge ; T1 témoin : une fiche à deux lignes dont la première était fautive et la
      dernière juste → vert ; T2 témoin : une case statut vide → vert.
    ⑦ UNITÉ — Des cas.
    ⑧ POURQUOI — R-731 : épreuves à la main avec sabotages ; R-732 : un cas vient d'une vraie ligne.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(os.path.join(racine, "gouvernance", "REGISTRE_REGLES.md"), encoding="utf-8") as f:
        texte_reg = f.read()
    table = lire_la_table(texte_reg)
    if not table:
        print("IMPOSSIBLE — la table de R-513 est introuvable ou vide")
        return 2
    entete = "id,statut,etat_vie\n"
    cas = [
        ("S1 deux stations", entete + "X1,⭐ VIVANTE,LABO\n", True),
        ("S2 état inconnu", entete + "X2,,VALIDEE\n", True),
        ("S3 état vide", entete + "X3,🔍 EN COURS DE TEST,\n", True),
        ("S4 dernière ligne fautive", entete + "X4,🔍 EN COURS DE TEST,LABO\nX4,📦 ARCHIVÉE,QA\n", True),
        ("S6 vraie ligne MA200-S1", entete + "MA200-S1,✅ VALIDÉE,LABO\n", True),
        ("T1 dernière ligne juste", entete + "X5,📦 ARCHIVÉE,QA\nX5,⭐ VIVANTE,QA\n", False),
        ("T2 statut vide", entete + "X6,,SUSPENDUE\n", False),
    ]
    tout_bon = True
    for nom, texte, doit_rougir in cas:
        fautives, _ = juger_les_fiches(table, texte)
        a_rougi = bool(fautives)
        ok = a_rougi == doit_rougir
        tout_bon &= ok
        print(f"{'OK ' if ok else 'FAUX'} {nom} : {'ROUGE' if a_rougi else 'VERT'} (attendu {'ROUGE' if doit_rougir else 'VERT'})"
              + (f" — {fautives[0][1]}" if fautives else ""))
    sans_table = PUCE_R513.sub("- **R-5l3**", texte_reg)
    s5 = lire_la_table(sans_table) == {}
    tout_bon &= s5
    print(f"{'OK ' if s5 else 'FAUX'} S5 puce de R-513 retirée : table {'vide' if s5 else 'encore lue'} (attendu vide, code 2)")
    print("VERT — chaque sabotage a rougi, chaque témoin est resté vert" if tout_bon else "ROUGE — un cas n'a pas rendu ce qu'il devait")
    return 0 if tout_bon else 1


def main():
    """Lit les options et lance l'épreuve ou ses sabotages.

    ① RÔLE — Point d'entrée en ligne de commande.
    ② CONTEXTE D'APPEL — `python3 tests/EPREUVE_UNE_STATION_PAR_FICHE_Mer_04-11-2026.py`.
    ③ ENTRÉE — Options `--racine` (défaut : le dossier courant) et `--saboter`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur rendue : termine le programme par sys.exit(code).
      [rend: 0]
    ⑥ TRAITEMENT — analyser les options, appeler `saboter` ou `eprouver`, sortir avec leur code.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Termine le processus.
    ⑪ TERMINAISON — Ne revient pas : sys.exit.
      [sort: oui]
    """
    p = argparse.ArgumentParser(description="R-513 : chaque fiche porte exactement une station.")
    # La certification lance chaque épreuve de tests/ avec la racine en PREMIER ARGUMENT, sans nom d'option
    # (CERTIFIER_LA_VERSION.lister_les_epreuves) : sans cet argument de position, l'épreuve rendait 2
    # (« unrecognized arguments ») à chaque lancement, constaté le 08-11-2026 à la préparation du bloc 3.
    p.add_argument("racine_en_position", nargs="?", default=None)
    p.add_argument("--racine", default=".")
    p.add_argument("--saboter", action="store_true")
    a = p.parse_args()
    racine = a.racine_en_position if a.racine_en_position is not None else a.racine
    sys.exit(saboter(racine) if a.saboter else eprouver(racine))


if __name__ == "__main__":
    main()
