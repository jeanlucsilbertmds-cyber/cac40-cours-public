#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_GRILLE_R505 — Ven 27-11-2026 (Paris), lot L4 du plan R505. Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. Jean-Luc a demandé le 27-11-2026 à 13h25 (BACKLOG A-1067) qu'aucune décision sur la sélection des
stratégies ne reste « notée mais pas faite » : la grille unique donnees/GRILLE_R505_V2.csv relie chaque critère de la
loi R-505 v2 à la fonction qui l'applique et à l'épreuve qui le prouve, et programmes/CONTROLER_LA_GRILLE.py refuse tout
verdict tant qu'une ligne décidée n'est pas branchée. Ces épreuves prouvent que le contrôleur ROUGIT quand il le doit —
fonction nommée qui n'existe pas, épreuve absente, critère de la loi sans ligne, extrait faux, décision absente du
BACKLOG, « plus tard » non écrit par la loi, ligne BRANCHÉE sans épreuve, en-tête faux, grille absente — et, avec
--saboter, que chaque épreuve rougit quand on retire du contrôleur ce qu'elle garde.

① RÔLE — Juger programmes/CONTROLER_LA_GRILLE.py sur la vraie grille, la vraie loi, le vrai BACKLOG, et sur des copies
  sabotées de la grille et de la loi ; avec --saboter, le juger sur des copies sabotées de lui-même.
② CONTEXTE D'APPEL — À la main avant toute livraison qui touche la grille ou le contrôleur (R-731), et par la
  certification : python3 -B tests/EPREUVES_DE_LA_GRILLE_R505_Ven_27-11-2026.py [<racine>] [--loi SOURCE]
  [--backlog SOURCE] [--saboter]. Avant l'installation de la loi au REGISTRE (étape I1), la loi se passe par --loi
  (par exemple origin/travail-carte:etudes/R505_V2/R505_v2_corps.md, ou un fichier).
③ ENTRÉE — La racine (défaut : le parent de tests/) : programmes/CONTROLER_LA_GRILLE.py, programmes/
  CONTRATS_DES_FICHIERS.py, donnees/GRILLE_R505_V2.csv, la loi et le BACKLOG (mêmes défauts que le contrôleur :
  gouvernance/REGISTRE_REGLES.md et BACKLOG_DECISIONS.md), programmes/MODULE_JUGEMENT.py et tests/
  EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py (une vraie fonction et une vraie épreuve, R-732).
④ CONDITIONS D'ENTRÉE — La loi et le BACKLOG se lisent ; sinon : FAUTE, code 1 (R-734).
⑤ SORTIE — Le code de sortie : 0 si chaque cas donne la réponse attendue et, avec --saboter, si chaque sabotage fait
  rougir au moins les cas qu'il vise ; 1 sinon ; 2 si un sabotage ne s'applique plus au texte du contrôleur.
  [rend: rien]
⑥ TRAITEMENT — Les cas (`les_cas`), chacun sur une copie de la grille dans un dossier jetable :
  G1 la vraie grille sur la vraie loi : code 1, aucune faute, chaque ligne non PLUS_TARD non branchée, P-GRILLE-REFUS
  « prête » · G2 l'extraction sur la vraie loi rend EXACTEMENT les 48 critères numérotés et les 33 seuils dont 4
  retirés (calibrage sur un cas connu) · G3 une fonction qui n'existe pas (dans un vrai module, et un module absent)
  rougit, une vraie (MODULE_JUGEMENT:frontiere_de_la_fiche) non · G4 une épreuve absente, un cas absent d'un vrai
  fichier rougissent, un vrai cas (F10) non · G5 la ligne E5-3 retirée, puis E2-4 (seule à réclamer le seuil
  phases_courtes) retirée : rouge, en nommant E5-3, puis le seuil · G6 le verrou : sur la vraie grille, le refus
  nomme E5-1 ; sur un dépôt fictif où tout est BRANCHÉ, aucun refus et code 0 ; une ligne BRANCHÉE sans épreuve :
  refus ; une grille absente : refus et code 3 · G7 un mot changé dans un extrait rougit ; l'extrait de E4-3 posé sur
  E5-3 rougit (pas le paragraphe de E5-3) · G8 E5-6 passée PLUS_TARD rougit · G9 une décision A-99999 rougit · G10 la
  loi sabotée : le numéro « 6. » du Kelly retiré → la ligne E5-6 rougit ; un affichage ⑫ ajouté → « la loi porte
  AFF-12 » · G11 une colonne renommée rougit · G12 l'en-tête de la vraie grille est celui du contrat.
  Ajouts du lot L4-FIX (relecture neuve V1_RELU_L4 et A-1109, 27-11-2026) : G13 la loi change ou une ligne disparaît
  → faute d'empreinte (D4) · G14 grille à l'en-tête seul → refus et code 2 (D1) · G15 un cas en commentaire, « :def »,
  print rougissent, un vrai cas passe, la grille branchée sur un commentaire est refusée (D2) · G16 rôle contraire à
  la loi, seuil retiré dans une ligne qui décide, decisions sans A-nnn (D3, D5) · G17 les deux portes (A-1109). Toute
  faute attendue doit être NOUVELLE par rapport à la vraie grille (D6). Les contrôles se font en mode
  --voir-les-lots (③ du contrôleur) tant que les lots ne sont pas réunis.
  Avec --saboter, pour chaque sabotage de SABOTAGES : copier le contrôleur et le contrat dans un dossier jetable, y
  remplacer UNE fois le texte visé, rejouer tous les cas avec la copie, et exiger que les cas visés rougissent.
⑦ UNITÉ — —
⑧ POURQUOI — R-731 : tout code écrit ou modifié passe des épreuves sabotées ; une épreuve qui reste verte quand on
  retire ce qu'elle teste est une décoration.
⑨ CE QUI CLOCHE — Les cas portent sur la FORME du branchement (existence), pas sur le fond (la fonction applique-t-elle
  la loi ?) : c'est la limite du contrôleur lui-même (son ⑨ (1)). G2 fige la forme du texte du 27-11-2026 : une
  réécriture de la loi le fera rougir, ce qui est voulu (recalibrer, et dire pourquoi).
⑩ EFFET — Écrit puis efface des dossiers jetables ; lance le contrôleur en sous-processus ; peut lancer `git show`.
⑪ TERMINAISON — Sort du programme.
"""
import csv
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
CONTROLEUR = "programmes/CONTROLER_LA_GRILLE.py"
VRAIE_FONCTION = "MODULE_JUGEMENT:frontiere_de_la_fiche"
VRAIE_EPREUVE = "EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py:F10"
# Calibrage sur la loi du 27-11-2026, pointe 683f65ca0 d'origin/travail-carte (48 critères, 33 seuils, 4 retirés) ;
# la loi du 27-11 à 20h (800b4a37) en portait 46 et 20 : E3-S6 et E6-6 sont venus avec A-1106 et A-1092 intégrés.
IDS_ATTENDUS = (["E2-%d" % i for i in range(1, 6)] + ["E3-S%d" % i for i in range(1, 7)]
                + ["E4-%d" % i for i in range(1, 5)] + ["E5-%d" % i for i in range(1, 7)]
                + ["E6-%d" % i for i in range(1, 7)] + ["AFF-%d" % i for i in range(1, 12)]
                + ["DIR-%d" % i for i in range(1, 7)] + ["VERDICT-%d" % i for i in range(1, 5)])
SEUILS_ATTENDUS = 33
RETIRES_ATTENDUS = {"epoques_gagnantes_minimum", "voisins", "frais_doubles", "minimum_de_donnees"}

SABOTAGES = [
    ("Z1 fonction toujours trouvée",
     "    return \"%s n'est pas défini dans %s\" % (ref.split(\":\", 1)[1], ou)",
     "    return \"\"", {"G3"}),
    ("Z2 cas d'épreuve toujours trouvé", "    if not cas_dans_l_arbre(arbre, m.group(2)):", "    if False:",
     {"G4", "G15"}),
    ("Z3 sans le lien loi → grille", "    for ident in sorted(set(ids_loi) - vus):", "    for ident in []:",
     {"G5"}),
    ("Z4 le refus du verdict oublie les non branchées",
     "    return list(r[\"fautes\"]) + [\"critère décidé non branché : %s\" % i for i in r[\"non_branchees_du_verdict\"]]",
     "    return list(r[\"fautes\"])", {"G6", "G17"}),
    ("Z4b le refus de la mise en direct oublie les non branchées",
     "    return list(r[\"fautes\"]) + [\"critère décidé non branché : %s\" % i for i in r[\"non_branchees\"]]",
     "    return list(r[\"fautes\"])", {"G6", "G17"}),
    ("Z4c l'étape 6 retient aussi le verdict (A-1109 ignoré)",
     "            if l[\"etape\"] not in ETAPES_DE_LA_MISE_EN_DIRECT:", "            if True:", {"G17"}),
    ("Z5 extrait non cherché", "        elif extrait not in bloc_nu:", "        elif False:", {"G7"}),
    ("Z6 PLUS_TARD sans garde", "            if \"plus tard\" not in", "            if False and \"plus tard\" not in",
     {"G8"}),
    ("Z7 BACKLOG non lu", "            if a not in actions:", "            if False:", {"G9"}),
    ("Z7b tout numéro CITÉ compte comme décision (SN1 de V1, 28-11-2026)",
     r'    actions = set(re.findall(r"(?m)^\| (A-\d+) \|", backlog))', r'    actions = set(re.findall(r"(A-\d+)", backlog))',
     {"G9"}),
    # (28-11-2026, réunion I1) les deux sabotages muets de la relecture V2 (L4FIX2 ②)
    ("Z7c ligne propre exigée hors du début de ligne",
     r'    actions = set(re.findall(r"(?m)^\| (A-\d+) \|", backlog))', r'    actions = set(re.findall(r"\| (A-\d+) \|", backlog))',
     {"G9"}),
    ("Z7d tout numéro cité accepté sauf A-987",
     "            if a not in actions:", "            if a not in actions and a == \"A-987\":", {"G9"}),
    ("Z8 numéros non confrontés", "        elif forme_numerotee.fullmatch(ident):", "        elif False:",
     {"G7", "G10"}),
    ("Z9 BRANCHÉ sans épreuve admis", "            if not fonctions or not epreuves:", "            if False:", {"G6"}),
    ("Z10 en-tête non confronté", "        if list(lecteur.fieldnames or []) != colonnes:", "        if False:",
     {"G11"}),
    ("Z11 refus ouvert sur panne",
     "        return [\"grille non contrôlée (%s) : %s\" % (type(ex).__name__, ex)]", "        return []", {"G6"}),
    ("Z12 seuils non réclamés", "    for s in sorted(k for k, retire in seuils_loi.items() if not retire and k "
     "not in reclames):", "    for s in []:", {"G5"}),
    ("Z13 grille vide admise (D1)",
     "        fautes.append(\"la grille ne porte aucune ligne : le lien loi → grille ne se saute jamais\")",
     "        pass", {"G14"}),
    ("Z14 lien loi → grille sauté sur grille vide (D1, le défaut d'origine)",
     "    for ident in sorted(set(ids_loi) - vus):", "    for ident in (sorted(set(ids_loi) - vus) if lignes else []):",
     {"G14"}),
    ("Z15 cas cherché comme mot (D2, le défaut d'origine)", "    if not cas_dans_l_arbre(arbre, m.group(2)):",
     "    if not re.search(r\"(?<![\\w-])%s(?![\\w-])\" % re.escape(m.group(2)), texte):", {"G15"}),
    ("Z16 rôle non confronté (D3)", "            if l[\"role\"] != attendu:", "            if False:", {"G16"}),
    ("Z17 seuil retiré admis dans une ligne qui décide (D3)",
     "            elif seuils_loi[s] and l[\"role\"] == \"DÉCIDE\":", "            elif False:", {"G16"}),
    ("Z18 décisions sans A-nnn admises (D5)", "        elif not re.search(r\"A-\\d+\", l[\"decisions\"]):",
     "        elif False:", {"G16"}),
    ("Z19 empreinte de la loi non confrontée (D4)", "        if portee.get(\"loi\") != e_loi:", "        if False:",
     {"G13"}),
    ("Z20 empreinte des lignes non confrontée (D4)", "        if portee.get(\"lignes\") != e_lignes:",
     "        if False:", {"G13"}),
    ("Z21 grille sans ligne d'empreinte admise (D4)", "    if constat_d_empreinte is None:",
     "    if constat_d_empreinte is None and False:", {"G13"}),
]


def charger(chemin):
    """Charge un contrôleur (le vrai, ou une copie sabotée) comme module.

    ① RÔLE — Donner aux cas le contrôleur à éprouver.
    ② CONTEXTE D'APPEL — `les_cas`, une fois par passage.
    ③ ENTRÉE — `chemin` : le fichier du contrôleur.
    ④ CONDITIONS D'ENTRÉE — CONTRATS_DES_FICHIERS.py est dans le même dossier que lui.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — Chargement par chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contrôleur saboté doit être celui qu'on juge, jamais le vrai.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le corps du contrôleur (définitions seulement).
    ⑪ TERMINAISON — Rend la main ; lève si le fichier ne se charge pas.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("grille_eprouvee_%d" % abs(hash(chemin)), chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def lire_grille(chemin):
    """Lit une grille en (en-tête, lignes).

    ① RÔLE — Fabriquer les copies sabotées de la grille.
    ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — `chemin` : la grille.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — DEUX valeurs : la liste des colonnes et la liste des lignes (dictionnaires).
      [rend: 2]
    ⑥ TRAITEMENT — csv, séparateur « ; ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter=";")
        return list(r.fieldnames), list(r)


def ecrire_grille(chemin, colonnes, lignes):
    """Écrit une grille.

    ① RÔLE — Poser une copie sabotée dans un dossier jetable.
    ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — `chemin` : où écrire · `colonnes` : l'en-tête · `lignes` : les lignes (dictionnaires).
    ④ CONDITIONS D'ENTRÉE — Le dossier existe.
    ⑤ SORTIE — Aucune valeur.
      [rend: rien]
    ⑥ TRAITEMENT — csv, séparateur « ; ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(lignes)


def les_cas(racine, controleur, loi, backlog):
    """Joue G1 à G17 avec le contrôleur donné ; rend {cas : (vrai si vert, raison)}.

    ① RÔLE — Le jeu d'épreuves lui-même.
    ② CONTEXTE D'APPEL — `main`, une fois avec le vrai contrôleur, puis une fois par sabotage.
    ③ ENTRÉE — `racine` : le dépôt · `controleur` : le fichier du contrôleur à éprouver · `loi` et `backlog` : les
      textes lus (déjà lus par `main`).
    ④ CONDITIONS D'ENTRÉE — Le contrat est à côté du contrôleur.
    ⑤ SORTIE — UNE valeur : {« G1 » … « G17 » : (vrai si vert, raison)}.
      [rend: 1]
    ⑥ TRAITEMENT — Voir ⑥ du programme ; chaque cas dans un dossier jetable ; une exception rend le cas rouge.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule fonction pour le vrai et pour les sabotés : les cas sont les mêmes.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit puis efface des dossiers jetables ; lance le contrôleur en sous-processus.
    ⑪ TERMINAISON — Rend la main ; chaque sous-processus est borné à 120 secondes.
      [sort: non]
    """
    G = charger(controleur)
    tmp = tempfile.mkdtemp(prefix="grille_r505_")
    res = {}
    try:
        f_loi, f_bk = os.path.join(tmp, "loi.md"), os.path.join(tmp, "backlog.md")
        open(f_loi, "w", encoding="utf-8").write(loi)
        open(f_bk, "w", encoding="utf-8").write(backlog)
        vraie = os.path.join(racine, "donnees", "GRILLE_R505_V2.csv")
        col, lignes = lire_grille(vraie)
        par_id = {l["identifiant"]: l for l in lignes}

        def ctl(lgn, cols=None, loi_txt=None, rac=None):
            """Contrôle une copie de la grille et rend le rendu de `controler`.

            ① RÔLE — Un contrôle sur une copie.
            ② CONTEXTE D'APPEL — les cas.
            ③ ENTRÉE — `lgn` : les lignes ·
            `cols` : l'en-tête (défaut : le vrai) · `loi_txt` : un texte de loi (défaut : la vraie) · `rac` : la
            racine (défaut : le dépôt). Le contrôle se fait en mode --voir-les-lots : avant la réunion des lots,
            leurs fonctions ne sont que sur leurs branches (③ du contrôleur).
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : le dictionnaire de `controler`.
              [rend: 1]
            ⑥ TRAITEMENT — Écrire, contrôler.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — —
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Écrit dans le dossier jetable.
            ⑪ TERMINAISON — Rend la main ; lève si le contrôle lève.
              [sort: non]
            """
            g = os.path.join(tmp, "g.csv")
            ecrire_grille(g, cols or col, lgn)
            fl = f_loi
            if loi_txt is not None:
                fl = os.path.join(tmp, "loi_sabotee.md")
                open(fl, "w", encoding="utf-8").write(loi_txt)
            return G.controler(rac or racine, g, fl, f_bk, voir_les_lots=True)

        def avec(ident, **chg):
            """Rend une copie des vraies lignes où la ligne `ident` est changée.

            ① RÔLE — Fabriquer un sabotage d'une ligne.
            ② CONTEXTE D'APPEL — les cas.
            ③ ENTRÉE — `ident` :
            l'identifiant · `**chg` : les cases à changer.
            ④ CONDITIONS D'ENTRÉE — l'identifiant existe.
            ⑤ SORTIE — UNE valeur : la liste des lignes.
              [rend: 1]
            ⑥ TRAITEMENT — Copier, changer.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — —
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            return [dict(l, **chg) if l["identifiant"] == ident else dict(l) for l in lignes]

        def a_faute(r, *mots):
            """Dit si une faute NOUVELLE du rendu (absente du contrôle de la vraie grille) porte tous les mots.

            ① RÔLE — Lire une faute attendue.
            ② CONTEXTE D'APPEL — les cas.
            ③ ENTRÉE — `r` : le rendu ·
            `*mots` : les mots.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : vrai ou faux.
              [rend: 1]
            ⑥ TRAITEMENT — Écarter les fautes déjà présentes sur la vraie grille (`base`), puis chercher.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une faute attendue doit être la BONNE faute, et NOUVELLE (défaut D6 de la relecture du
            27-11-2026 : G7 restait vert parce qu'E5-1 était DÉJÀ fausse sur la loi nouvelle).
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            return any(all(m in x for m in mots) for x in r["fautes"] if x not in base)

        def lancer(*args):
            """Lance le contrôleur éprouvé en sous-processus et rend (code, sortie).

            ① RÔLE — Éprouver les codes de sortie.
            ② CONTEXTE D'APPEL — G1, G6.
            ③ ENTRÉE — `*args` : les options.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : le code et la sortie.
              [rend: 2]
            ⑥ TRAITEMENT — subprocess.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Le code de sortie est ce que lit le circuit.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Lance un processus.
            ⑪ TERMINAISON — Rend la main ; borné à 120 s.
              [sort: non]
            """
            p = subprocess.run([sys.executable, "-B", controleur] + list(args), capture_output=True, text=True,
                               timeout=120)
            return p.returncode, p.stdout + p.stderr

        def cas(nom, fonction):
            """Joue un cas ; une exception le rend rouge.

            ① RÔLE — Ranger un cas.
            ② CONTEXTE D'APPEL — `les_cas`.
            ③ ENTRÉE — `nom` : G1… · `fonction` : rend
            (vert, raison).
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur : écrit dans `res`.
              [rend: rien]
            ⑥ TRAITEMENT — Appeler, attraper.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un cas qui plante n'est pas vert.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Écrit dans `res`.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            try:
                res[nom] = fonction()
            except Exception as ex:
                res[nom] = (False, "exception %s : %s" % (type(ex).__name__, ex))

        base = set(ctl(lignes)["fautes"])

        def g1():
            """G1 — la vraie grille sur la vraie loi.

            ① RÔLE — Cas réel (R-732).
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Contrôler, lancer.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — La vérité du jour : rien n'est branché.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Sous-processus.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r = ctl(lignes)
            attendues = [l["identifiant"] for l in lignes if l["etat"] == "DÉCIDÉ_NON_BRANCHÉ"]
            code, out = lancer("--racine", racine, "--loi", f_loi, "--backlog", f_bk, "--voir-les-lots")
            ok = (not r["fautes"] and r["non_branchees"] == attendues and "P-GRILLE-REFUS" in r["pretes"]
                  and code == 1 and "AUCUN VERDICT NE PEUT SORTIR" in out)
            return ok, "fautes=%d non_branchees=%d code=%d" % (len(r["fautes"]), len(r["non_branchees"]), code)

        def g2():
            """G2 — l'extraction sur la vraie loi.

            ① RÔLE — Calibrer le lien loi → grille sur un cas connu.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Extraire, comparer.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un motif se calibre avant de servir.
            ⑨ CE QUI CLOCHE — Fige la forme du 27-11-2026.
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            ids, seuils = G.identifiants_de_la_loi(G.bloc_de_la_loi(loi))
            retires = {k for k, v in seuils.items() if v}
            return (set(ids) == set(IDS_ATTENDUS) and len(seuils) == SEUILS_ATTENDUS and retires == RETIRES_ATTENDUS,
                    "%d ids, %d seuils, retirés %s" % (len(ids), len(seuils), sorted(retires)))

        def g3():
            """G3 — une fonction nommée qui n'existe pas rougit ; une vraie non.

            ① RÔLE — Sabotage de la colonne fonction.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Trois copies.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — A-1067 ③.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r1 = ctl(avec("E5-6", fonction="MODULE_JUGEMENT:kelly_qui_n_existe_pas"))
            r2 = ctl(avec("E5-6", fonction="MODULE_QUI_N_EXISTE_PAS:f"))
            r3 = ctl(avec("E5-6", fonction=VRAIE_FONCTION))
            ok = (a_faute(r1, "E5-6", "kelly_qui_n_existe_pas") and a_faute(r2, "E5-6", "MODULE_QUI_N_EXISTE_PAS")
                  and not r3["fautes"])
            return ok, "inexistante=%s module=%s vraie=%s" % (len(r1["fautes"]), len(r2["fautes"]), len(r3["fautes"]))

        def g4():
            """G4 — une épreuve absente rougit ; un vrai cas non.

            ① RÔLE — Sabotage de la colonne épreuve.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Trois copies.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — A-1067 ③.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r1 = ctl(avec("E5-6", epreuve="EPREUVES_QUI_N_EXISTENT_PAS.py:C1"))
            r2 = ctl(avec("E5-6", epreuve=VRAIE_EPREUVE.split(":")[0] + ":CAS_ABSENT_ZZ9"))
            r3 = ctl(avec("E5-6", epreuve=VRAIE_EPREUVE))
            ok = (a_faute(r1, "E5-6", "n'existe pas") and a_faute(r2, "E5-6", "CAS_ABSENT_ZZ9") and not r3["fautes"])
            return ok, "absente=%d cas=%d vraie=%d" % (len(r1["fautes"]), len(r2["fautes"]), len(r3["fautes"]))

        def g5():
            """G5 — une ligne retirée alors que la loi la porte rougit.

            ① RÔLE — Le lien loi → grille.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Deux copies.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une ligne oubliée est une décision non faite.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r1 = ctl([l for l in lignes if l["identifiant"] != "E5-3"])
            r2 = ctl([l for l in lignes if l["identifiant"] != "E2-4"])
            ok = a_faute(r1, "E5-3") and a_faute(r2, "E2-4") and a_faute(r2, "phases_courtes")
            return ok, "sans E5-3 : %d faute(s) · sans E2-4 : %d" % (len(r1["fautes"]), len(r2["fautes"]))

        def g6():
            """G6 — le verrou du juge : refus tant que tout n'est pas branché, ouverture seulement si tout l'est.

            ① RÔLE — Éprouver `motifs_de_refus_du_verdict` et les codes 0 et 3.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Vraie grille : le refus du verdict nomme E5-1 (étape 5) et pas E6-2 (étape 6), celui de
            la mise en direct nomme E6-2 ; dépôt fictif tout BRANCHÉ ; une ligne sans épreuve ; grille absente.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — A-1067 ② et ⑤.
            ⑨ CE QUI CLOCHE — Le dépôt fictif ne prouve pas qu'une vraie
            fonction applique la loi.
            ⑩ EFFET — Dossiers jetables, sous-processus.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            g = os.path.join(tmp, "g6.csv")
            ecrire_grille(g, col, lignes)
            m1 = G.motifs_de_refus_du_verdict(racine, g, f_loi, f_bk)
            m1b = G.motifs_de_refus_de_la_mise_en_direct(racine, g, f_loi, f_bk)
            fic = os.path.join(tmp, "depot_fictif")
            os.makedirs(os.path.join(fic, "programmes"))
            os.makedirs(os.path.join(fic, "tests"))
            open(os.path.join(fic, "programmes", "FICTIF.py"), "w").write("def appliquer():\n    return 1\n")
            open(os.path.join(fic, "tests", "EPREUVES_FICTIVES.py"), "w").write("def cas1():\n    pass\n")
            tout = [dict(l, etat="BRANCHÉ", fonction="FICTIF:appliquer", epreuve="EPREUVES_FICTIVES.py:CAS1")
                    if l["etat"] != "PLUS_TARD" else dict(l) for l in lignes]
            gf = os.path.join(tmp, "g6_fictive.csv")
            ecrire_grille(gf, col, tout)
            m2 = G.motifs_de_refus_du_verdict(fic, gf, f_loi, f_bk)
            m2b = G.motifs_de_refus_de_la_mise_en_direct(fic, gf, f_loi, f_bk)
            code0, _o = lancer("--racine", fic, "--grille", gf, "--loi", f_loi, "--backlog", f_bk)
            trou = [dict(l, epreuve="") if l["identifiant"] == "E5-1" else l for l in tout]
            gt = os.path.join(tmp, "g6_trou.csv")
            ecrire_grille(gt, col, trou)
            m3 = G.motifs_de_refus_du_verdict(fic, gt, f_loi, f_bk)
            m4 = G.motifs_de_refus_du_verdict(fic, os.path.join(tmp, "absente.csv"), f_loi, f_bk)
            m4b = G.motifs_de_refus_de_la_mise_en_direct(fic, os.path.join(tmp, "absente.csv"), f_loi, f_bk)
            code3, _o = lancer("--racine", fic, "--grille", os.path.join(tmp, "absente.csv"), "--loi", f_loi,
                               "--backlog", f_bk)
            ok = ("critère décidé non branché : E5-1" in m1 and "critère décidé non branché : E6-2" in m1b
                  and "critère décidé non branché : E6-2" not in m1 and m2 == [] and m2b == [] and code0 == 0
                  and any("E5-1" in x and "BRANCHÉ sans épreuve" in x for x in m3) and len(m4) == 1
                  and len(m4b) == 1 and code3 == 3)
            return ok, "vraie=%d motifs · fictive=%d (code %d) · trou=%d · absente=%d (code %d)" % (
                len(m1), len(m2), code0, len(m3), len(m4), code3)

        def g7():
            """G7 — un extrait faux rougit ; un extrait hors du paragraphe du numéro rougit.

            ① RÔLE — Le lien grille → loi.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Deux copies.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — L'extrait est la trace de la phrase de la loi.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            p = par_id["E5-1"]["phrase_de_la_loi"].replace("0,05", "0,10", 1)
            r1 = ctl(avec("E5-1", phrase_de_la_loi=p))
            r2 = ctl(avec("E5-3", phrase_de_la_loi=par_id["E4-3"]["phrase_de_la_loi"]))
            ok = a_faute(r1, "E5-1", "pas dans la loi") and a_faute(r2, "E5-3", "paragraphe")
            return ok, "mot changé=%d · autre paragraphe=%d" % (len(r1["fautes"]), len(r2["fautes"]))

        def g8():
            """G8 — PLUS_TARD sans « plus tard » dans la loi rougit.

            ① RÔLE — Garde contre l'échappatoire.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Une copie.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une ligne PLUS_TARD ne bloque pas le verdict.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r = ctl(avec("E5-6", etat="PLUS_TARD"))
            return a_faute(r, "E5-6", "PLUS_TARD"), "%d faute(s)" % len(r["fautes"])

        def g9():
            """G9 — une décision absente du BACKLOG rougit, y compris un numéro CITÉ dans le BACKLOG sans ligne propre.

            ① RÔLE — Le lien grille → BACKLOG.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — ① une copie qui cite A-99999, cité nulle part · ② une copie qui cite A-987, cité dans le texte du
              BACKLOG mais sans ligne « | A-987 | » à lui (relecture V1 du 28-11-2026, défaut 1 de L4FIX : 10 numéros de
              ce genre, dont A-987 ; si le BACKLOG lu n'en fait plus un tel cas, le premier numéro cité sans ligne).
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une décision citée doit exister, comme ligne du BACKLOG : un numéro seulement CITÉ n'est pas une
              décision (SN1 de V1 : compter tout numéro cité laissait passer A-987, vert).
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r = ctl(avec("E5-6", decisions="A-99999"))
            # (28-11-2026, réunion I1 ; relecture V2, L4FIX2 ②) LA PROPRIÉTÉ, PAS UN CAS : TOUS les numéros cités sans
            # ligne propre doivent rougir, pas le seul A-987 ; et l'oracle ne recopie PAS l'expression du contrôleur
            # (R-708) : une ligne propre est lue en découpant la ligne sur « | ».
            lignes_propres = set()
            for lg in backlog.splitlines():
                morceaux = lg.split("|")
                if lg.startswith("| A-") and len(morceaux) > 2 and morceaux[1].strip().startswith("A-") \
                        and morceaux[1].strip()[2:].isdigit():
                    lignes_propres.add(morceaux[1].strip())
            cites = sorted(set(re.findall(r"A-\d+", backlog)) - lignes_propres, key=lambda a: int(a[2:]))
            if not cites:
                return False, "le BACKLOG lu n'a aucun numéro cité sans ligne propre : le cas ne peut pas se jouer"
            passes = [c for c in cites if not a_faute(ctl(avec("E5-6", decisions=c)), "E5-6", c)]
            # un numéro écrit « | A-nnn | » AU MILIEU d'une ligne (tableau, citation) n'est pas une ligne propre
            f_bk2 = os.path.join(tmp, "backlog_milieu.md")
            open(f_bk2, "w", encoding="utf-8").write(backlog + "\nrenvoi | A-99998 | au milieu d'une ligne\n")
            g2 = os.path.join(tmp, "g_milieu.csv")
            ecrire_grille(g2, col, avec("E5-6", decisions="A-99998"))
            r3 = G.controler(racine, g2, f_loi, f_bk2, voir_les_lots=True)
            return (a_faute(r, "E5-6", "A-99999") and not passes and a_faute(r3, "E5-6", "A-99998"),
                    "%d faute(s) ; %d numéro(s) cités sans ligne, %d passent %s ; « | A-99998 | » au milieu : %d faute(s)"
                    % (len(r["fautes"]), len(cites), len(passes), passes[:5], len(r3["fautes"])))

        def g10():
            """G10 — la loi sabotée : un numéro retiré, un numéro ajouté.

            ① RÔLE — Le lien loi → grille, du côté de la loi.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — Les deux textes visés sont dans la vraie loi (sinon rouge).
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Deux lois sabotées.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une loi qui change doit faire rougir la
            grille.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            a, b = "6. **LE CRITÈRE DE KELLY", "⑪ Le nombre d'opérations nécessaire pour conclure"
            if loi.count(a) != 1 or loi.count(b) != 1:
                return False, "texte visé absent de la loi"
            r1 = ctl(lignes, loi_txt=loi.replace(a, "**LE CRITÈRE DE KELLY"))
            r2 = ctl(lignes, loi_txt=loi.replace(b, "⑫ Le TABLEAU NOUVEAU ; " + b))
            ok = a_faute(r1, "E5-6", "ne numérote pas") and a_faute(r2, "AFF-12")
            return ok, "sans 6. : %d · avec ⑫ : %d" % (len(r1["fautes"]), len(r2["fautes"]))

        def g11():
            """G11 — une colonne renommée rougit.

            ① RÔLE — L'en-tête est celui du contrat.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Une copie.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — CE QUI SE PARTAGE SE DÉCLARE.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            c2 = ["état" if c == "etat" else c for c in col]
            l2 = [{("état" if k == "etat" else k): v for k, v in l.items()} for l in lignes]
            r = ctl(l2, cols=c2)
            return a_faute(r, "en-tête"), "%d faute(s)" % len(r["fautes"])

        def g12():
            """G12 — l'en-tête de la vraie grille est celui du contrat.

            ① RÔLE — La déclaration au contrat.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Lire le contrat, comparer, et lire l'en-tête comme le circuit le lit.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Le circuit confronte la grille par `champs_de_l_en_tete`.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            C = G._contrat()
            ok = (col == list(C.GRILLE_R505_V2) == C.champs_de_l_en_tete(vraie)
                  and C.CONTRATS_PAR_FICHIER.get(C.NOM_DE_LA_GRILLE_R505) == C.GRILLE_R505_V2)
            return ok, "colonnes=%d" % len(col)

        def g13():
            """G13 — la loi change → la grille rougit ; une ligne disparaît → la grille rougit (défaut D4).

            ① RÔLE — Éprouver les empreintes de la ligne LOI-EMPREINTE.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — Le paragraphe des seuils est dans la vraie loi (sinon rouge).
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — ① vraie grille : aucune faute d'empreinte ; ② la loi reçoit un contrôle NOUVEAU SANS
              NUMÉRO (sabotage S8 de la relecture) : « la loi a changé » ; ③ la loi reflowée (retours à la ligne en
              plus) : aucune faute d'empreinte ; ④ la ligne non numérotée E3-GLISSEMENT retirée (S7) : « les lignes de
              la grille ont changé » ; ⑤ la ligne LOI-EMPREINTE retirée : faute ; ⑥ son empreinte de loi faussée d'un
              caractère : faute.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Les numéros ne voient ni une phrase nouvelle sans numéro, ni une ligne nommée supprimée.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            ancre = "**LES SEUILS DE CETTE LOI**"
            if loi.count(ancre) != 1:
                return False, "texte visé absent de la loi"
            r1 = ctl(lignes)
            ajout = loi.replace(ancre, "**UN CONTRÔLE NOUVEAU** : le juge REFUSE toute version dont le gain dépend "
                                       "d'une seule action.\n\n  " + ancre, 1)
            r2 = ctl(lignes, loi_txt=ajout)
            r3 = ctl(lignes, loi_txt=loi.replace(" ; ", " ;\n   ", 3))
            r4 = ctl([l for l in lignes if l["identifiant"] != "E3-GLISSEMENT"])
            r5 = ctl([l for l in lignes if l["identifiant"] != G.LIGNE_D_EMPREINTE])
            c = par_id[G.LIGNE_D_EMPREINTE]["constat"]
            i = c.index("loi=") + 4
            faux = c[:i] + ("0" if c[i] != "0" else "1") + c[i + 1:]
            r6 = ctl(avec(G.LIGNE_D_EMPREINTE, constat=faux))
            emp = [x for x in r1["fautes"] if "recalage" in x] + [x for x in r3["fautes"] if "recalage" in x]
            ok = (not emp and a_faute(r2, "la loi a changé") and a_faute(r4, "les lignes de la grille ont changé")
                  and a_faute(r5, "pas de ligne " + G.LIGNE_D_EMPREINTE) and a_faute(r6, "la loi a changé"))
            return ok, "vraie=%d · loi+phrase=%d · reflowée=%d · sans E3-GLISSEMENT=%d · sans ligne=%d · faussée=%d" % (
                len(emp), len(r2["fautes"]), len(r3["fautes"]), len(r4["fautes"]), len(r5["fautes"]),
                len(r6["fautes"]))

        def g14():
            """G14 — une grille réduite à son en-tête REFUSE (défaut D1).

            ① RÔLE — Le lien loi → grille ne se saute jamais.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Grille à l'en-tête seul : fautes « aucune ligne » et « la loi porte E5-1 » ; les deux portes
              refusent ; le contrôleur en ligne de commande rend 2 (la relecture avait obtenu 0).
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une écriture tronquée ou une fusion ratée ne doit jamais ouvrir le verrou.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable, sous-processus.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r = ctl([])
            gv = os.path.join(tmp, "g14_vide.csv")
            ecrire_grille(gv, col, [])
            m1 = G.motifs_de_refus_du_verdict(racine, gv, f_loi, f_bk)
            m2 = G.motifs_de_refus_de_la_mise_en_direct(racine, gv, f_loi, f_bk)
            code, _o = lancer("--racine", racine, "--grille", gv, "--loi", f_loi, "--backlog", f_bk)
            ok = (a_faute(r, "ne porte aucune ligne") and a_faute(r, "la loi porte E5-1") and m1 and m2 and code == 2)
            return ok, "fautes=%d · refus verdict=%d · refus direct=%d · code %d" % (len(r["fautes"]), len(m1),
                                                                                   len(m2), code)

        def g15():
            """G15 — un cas d'épreuve doit être DÉFINI : un commentaire ou un mot-clé ne suffit pas (défaut D2).

            ① RÔLE — Éprouver `epreuve_existe` et `cas_dans_l_arbre`.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Un dépôt fictif : « # CAS1 » (commentaire), « print("CAS4") » rougissent ; « :def » rougit ;
              « def cas2(): » , « essai("E3", e3) », « ("E7", e7) » passent ; le vrai cas F10 (forme « voulu("F10") »)
              passe ; toute la grille BRANCHÉE sur « # CAS1 » (sabotage S2 de la relecture) : les deux portes refusent.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Avant D2, la grille entière branchée sur un commentaire ouvrait le verrou.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            fic = os.path.join(tmp, "depot_d2")
            os.makedirs(os.path.join(fic, "programmes"))
            os.makedirs(os.path.join(fic, "tests"))
            open(os.path.join(fic, "programmes", "FICTIF.py"), "w").write("def appliquer():\n    return 1\n")
            open(os.path.join(fic, "tests", "EPR.py"), "w").write(
                "# CAS1\nprint(\"CAS4\")\ndef cas2():\n    pass\ndef e3():\n    pass\nessai(\"E3\", e3)\n"
                "for c, f in ((\"E7\", e3),):\n    pass\n")
            rouge = [G.epreuve_existe(fic, x) for x in ("EPR.py:CAS1", "EPR.py:CAS4", "EPR.py:def",
                                                       VRAIE_EPREUVE.split(":")[0] + ":def")]
            vert = [G.epreuve_existe(fic, x) for x in ("EPR.py:CAS2", "EPR.py:E3", "EPR.py:E7")]
            vraie = G.epreuve_existe(racine, VRAIE_EPREUVE)
            tout = [dict(l, etat="BRANCHÉ", fonction="FICTIF:appliquer", epreuve="EPR.py:CAS1")
                    if l["etat"] != "PLUS_TARD" else dict(l) for l in lignes]
            gf = os.path.join(tmp, "g15.csv")
            ecrire_grille(gf, col, tout)
            m1 = G.motifs_de_refus_du_verdict(fic, gf, f_loi, f_bk)
            m2 = G.motifs_de_refus_de_la_mise_en_direct(fic, gf, f_loi, f_bk)
            ok = all(rouge) and not any(vert) and not vraie and bool(m1) and bool(m2)
            return ok, "rouges=%d/4 · verts=%d/3 · F10=%s · refus=%d/%d" % (
                sum(1 for x in rouge if x), sum(1 for x in vert if not x), "oui" if not vraie else vraie, len(m1),
                len(m2))

        def g16():
            """G16 — le rôle confronté à la loi, le seuil retiré, la case decisions sans A-nnn (défauts D3, D5).

            ① RÔLE — Éprouver la lecture du rôle et des décisions.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — E5-1 passée AFFICHE (sabotage S5) : rôle faux ; AFF-1 passée DÉCIDE : rôle faux ; E4-4
              passée DÉCIDE — vraie ligne qui réclame minimum_de_donnees, retiré par A-1103 (sabotage S14) : faute
              « que la loi a retiré » ; E5-1 sans A-nnn (sabotage S6, et L4-1 de Cowork) : faute.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Le juge brancherait sinon un critère que la loi ne fait plus décider, ou ne bloquerait plus un
              critère qui décide.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            r1 = ctl(avec("E5-1", role="AFFICHE"))
            r2 = ctl(avec("AFF-1", role="DÉCIDE"))
            r3 = ctl(avec("E4-4", role="DÉCIDE"))
            r4 = ctl(avec("E5-1", decisions="n°42 · DÉL-D15"))
            ok = (a_faute(r1, "E5-1", "role AFFICHE") and a_faute(r2, "AFF-1", "role DÉCIDE")
                  and a_faute(r3, "E4-4", "minimum_de_donnees", "retiré") and a_faute(r4, "E5-1", "A-nnn"))
            return ok, "E5-1 AFFICHE=%d · AFF-1 DÉCIDE=%d · E4-4 DÉCIDE=%d · sans A-nnn=%d" % (
                len(r1["fautes"]), len(r2["fautes"]), len(r3["fautes"]), len(r4["fautes"]))

        def g17():
            """G17 — les deux portes d'A-1109 : une ligne d'étape 6 non branchée retient la mise en direct, pas le verdict.

            ① RÔLE — Éprouver `motifs_de_refus_du_verdict` et `motifs_de_refus_de_la_mise_en_direct`.
            ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — Aucune.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert, et la raison affichée.
              [rend: 2]
            ⑥ TRAITEMENT — Dépôt fictif tout BRANCHÉ sauf une ligne laissée DÉCIDÉ_NON_BRANCHÉ, sans fonction ni
              épreuve (une référence absente du dépôt fictif serait une FAUTE, qui ferme les deux portes) : ① E6-2 (étape 6) : verdict permis, mise en direct refusée
              en nommant E6-2 ; ② DIR-1 (suivi en direct) : même chose ; ③ E5-3 (étape 5) : les deux refusent ;
              ④ la vraie grille : les deux refusent, et la mise en direct porte plus de motifs que le verdict.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — « le VERDICT attend que toutes les lignes des étapes 1 à 5 soient branchées, la MISE EN DIRECT
              attend en plus celles de l'étape 6 et du suivi en direct » (A-1109).
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Dossier jetable.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            fic = os.path.join(tmp, "depot_a1109")
            os.makedirs(os.path.join(fic, "programmes"))
            os.makedirs(os.path.join(fic, "tests"))
            open(os.path.join(fic, "programmes", "FICTIF.py"), "w").write("def appliquer():\n    return 1\n")
            open(os.path.join(fic, "tests", "EPR.py"), "w").write("def cas1():\n    pass\n")
            res = []
            for laisse in ("E6-2", "DIR-1", "E5-3"):
                t = [dict(l, etat="BRANCHÉ", fonction="FICTIF:appliquer", epreuve="EPR.py:CAS1")
                     if l["etat"] != "PLUS_TARD" and l["identifiant"] != laisse
                     else dict(l, fonction="", epreuve="", etat="DÉCIDÉ_NON_BRANCHÉ") if l["identifiant"] == laisse
                     else dict(l) for l in lignes]
                g = os.path.join(tmp, "g17.csv")
                ecrire_grille(g, col, t)
                res.append((G.motifs_de_refus_du_verdict(fic, g, f_loi, f_bk),
                            G.motifs_de_refus_de_la_mise_en_direct(fic, g, f_loi, f_bk)))
            g = os.path.join(tmp, "g17_vraie.csv")
            ecrire_grille(g, col, lignes)
            v, d = G.motifs_de_refus_du_verdict(racine, g, f_loi, f_bk), G.motifs_de_refus_de_la_mise_en_direct(
                racine, g, f_loi, f_bk)
            ok = (res[0][0] == [] and any("E6-2" in x for x in res[0][1]) and res[1][0] == []
                  and any("DIR-1" in x for x in res[1][1]) and any("E5-3" in x for x in res[2][0])
                  and any("E5-3" in x for x in res[2][1]) and v and len(d) > len(v))
            return ok, "E6-2 : %d/%d · DIR-1 : %d/%d · E5-3 : %d/%d · vraie : %d/%d (verdict/direct)" % (
                len(res[0][0]), len(res[0][1]), len(res[1][0]), len(res[1][1]), len(res[2][0]), len(res[2][1]),
                len(v), len(d))

        for nom, f in (("G1", g1), ("G2", g2), ("G3", g3), ("G4", g4), ("G5", g5), ("G6", g6), ("G7", g7),
                       ("G8", g8), ("G9", g9), ("G10", g10), ("G11", g11), ("G12", g12), ("G13", g13),
                       ("G14", g14), ("G15", g15), ("G16", g16), ("G17", g17)):
            cas(nom, f)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return res


def main():
    """Lit les options, joue les cas, puis les sabotages.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande (② du programme).
    ③ ENTRÉE — sys.argv : `<racine>`, `--loi`, `--backlog`, `--saboter`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur : le code de sortie (⑤ du programme).
      [rend: rien]
    ⑥ TRAITEMENT — ① lire la loi et le BACKLOG par le lecteur du contrôleur (une seule lecture, R-708) · ② jouer les
      cas, les afficher · ③ avec --saboter, pour chaque sabotage : copie, remplacement unique, cas rejoués, cas visés
      rouges exigés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑧ du programme.
    ⑨ CE QUI CLOCHE — Un sabotage qui fait rougir PLUS que les cas visés est accepté (les cas se recouvrent : un refus
      ouvert sur panne touche aussi les codes).
    ⑩ EFFET — Écrit à l'écran ; dossiers jetables.
    ⑪ TERMINAISON — Sort du programme.
      [sort: oui]
    """
    args = sys.argv[1:]
    saboter = "--saboter" in args
    args = [a for a in args if a != "--saboter"]
    opts, pos = {}, []
    while args:
        a = args.pop(0)
        if a in ("--loi", "--backlog") and args:
            opts[a[2:]] = args.pop(0)
        else:
            pos.append(a)
    racine = os.path.abspath(pos[0] if pos else os.path.dirname(ICI))
    vrai = os.path.join(racine, CONTROLEUR)
    G = charger(vrai)
    try:
        loi = G.lire_une_source(racine, opts.get("loi") or G.LOI_PAR_DEFAUT)
        G.bloc_de_la_loi(loi)
        backlog = G.lire_une_source(racine, opts.get("backlog") or G.BACKLOG_PAR_DEFAUT)
    except Exception as ex:
        print("FAUTE : la loi ou le BACKLOG ne se lisent pas (%s) — rien n'est éprouvé" % ex)
        sys.exit(1)
    res = les_cas(racine, vrai, loi, backlog)
    rouges = [n for n, (ok, _r) in res.items() if not ok]
    for n, (ok, r) in res.items():
        print("%s %s — %s" % ("VERT " if ok else "ROUGE", n, r))
    print("%d/%d cas verts" % (len(res) - len(rouges), len(res)))
    if rouges:
        sys.exit(1)
    if not saboter:
        sys.exit(0)
    fautes = 0
    for nom, ancien, neuf, vises in SABOTAGES:
        src = open(vrai, encoding="utf-8").read()
        if src.count(ancien) != 1:
            print("SABOTAGE %s : le texte visé n'est plus unique dans le contrôleur (%d)" % (nom, src.count(ancien)))
            sys.exit(2)
        d = tempfile.mkdtemp(prefix="sabotage_grille_")
        try:
            shutil.copy(os.path.join(racine, "programmes", "CONTRATS_DES_FICHIERS.py"), d)
            mut = os.path.join(d, "CONTROLER_LA_GRILLE.py")
            open(mut, "w", encoding="utf-8").write(src.replace(ancien, neuf, 1))
            r = les_cas(racine, mut, loi, backlog)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        rg = {n for n, (ok, _x) in r.items() if not ok}
        bon = vises <= rg
        fautes += not bon
        print("%s %s — rouges : %s (visés : %s)" % ("SABOTAGE MORD " if bon else "SABOTAGE MUET ", nom,
                                                    ",".join(sorted(rg)) or "aucun", ",".join(sorted(vises))))
    print("%d/%d sabotages mordent" % (len(SABOTAGES) - fautes, len(SABOTAGES)))
    sys.exit(1 if fautes else 0)


if __name__ == "__main__":
    main()
