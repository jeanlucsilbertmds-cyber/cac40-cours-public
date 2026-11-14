#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_COMBLEMENT_DES_20_ANS — Sam 31-10-2026 (Paris)
Rôle : prouver que les gestes du lot de comblement d'A-633 — `combler_par_raccords` (Unibail par la chaîne bnains →
ABC → Yahoo), `combler_les_seances` (Michelin 24-07-2000), `lire_les_degradees` (les 81 barres de Yahoo dégradées) dans
programmes/REPARER_L_HISTORIQUE_LONG.py, et, dans programmes/CONTROLER_L_HISTORIQUE_LONG.py, `lire_abc`, le rejeu de K23
parti d'ABC et la marche permise de K15 pour une division documentée — font juste sur les vraies données, s'arrêtent
quand ils ne peuvent pas mesurer sûrement, et que chaque épreuve a des dents (R-731).
Quand l'appeler : avant toute livraison qui touche ces fonctions, SERIES_EN_CHAINE, SEANCES_A_COMBLER, la table des
barres dégradées, les bruts d'ABC ou la table des divisions documentées.

À QUOI ÇA SERT. Décisions de Jean-Luc du 31-10-2026 : 19h23 (STMicro, annexe n°39), 20h11 (Unibail par ABC, n°37ter),
21h04 (combler ce dont le cours de Paris est déjà chez nous, n°47). Les épreuves jouent les VRAIES lignes du dépôt ; les
défauts sont FABRIQUÉS sur des copies en mémoire.

LES ÉPREUVES :
A1 Unibail, vraies données : 1 571 séances « versé » (source abc, dont 1 567 du 01-03-2017 au 13-04-2023) et 2 476
   « comblé » (source bnains), 7 « non comblé » (2 471 et 12 avant les rectifications du 04-11-2026, choix D6),
   aucun arrêt ; la séance du 07-10-2010 porte « À SIGNALER » et la distribution de 20 € ; les lignes d'ABC nomment les
   14 et 17-04-2023, non confrontées.
A2 une barre d'ABC ôtée DANS le raccord (02-05-2023) : ARRÊT « raccord ».
A3 10 barres d'ABC du raccord × 1,01 : accord sous 90 % ; ARRÊT « raccord ».
A4 une division FABRIQUÉE à la table de bnains pour Unibail le 02-01-2012 : ARRÊT « opération connue dans la chaîne ».
A5 les barres d'ABC d'avant le 02-01-2020 × 2, que rien ne déclare : ARRÊT « saut ».
A6 le raccord déclaré à partir du 19-04-2023 au lieu du 18 : une séance commune plus proche de la couture ; ARRÊT.
A7 la barre d'ABC du 15-03-2017 rendue incohérente : « non comblé » (« barre d'ABC inutilisable »), rien d'écrit ce jour.
A8 Michelin 24-07-2000, vraies données : une séance comblée, facteur de prix 0,24156 à 1e-4 près (relecture, S6).
A9 la ligne de Yahoo du 21-07-2000 FABRIQUÉE × 1,05 : ARRÊT « voisine ».
A10 une division FABRIQUÉE à la table de bnains pour Michelin le 01-08-2000, dans la référence : ARRÊT.
A11 K23 : une ligne « versé » dont la clôture est changée de 0,01 € est refusée ; une ligne « versé » rejouée sans les
   cours d'ABC est refusée (« ABC, qui n'a pas de barre ») ; `lire_abc` refuse une séance écrite deux fois avec deux
   chiffres différents.
A12 K15, vrai fichier réparé : sans la table des divisions documentées, K15 refuse la marche de STMicro du 09-05-2000 ;
   avec elle, K15 est vide.
A14 K23 sur la table des divisions de bnains (décision de Jean-Luc du 31-10-2026 à 22h30) : sa chaîne de provenance est
   complète au dépôt ; une ligne retirée de la table (copie de liens durs, le fichier recréé) fait rougir K23 ; la table
   est dans `LU`, et `LU_HORS_REGISTRE` n'existe plus.
A13 `lire_les_degradees`, vraie table : 81 barres, sans EssilorLuxottica 02-03-2004 ; une barre écrite deux fois est
   refusée ; le journal du dépôt écarte puis comble chacune des 81.

A15 (relecture du lot, D1) les 16-01, 23-01, 06-02 et 16-02-2017, barres de bnains incohérentes : chacune reçoit la barre
   d'ABC du même jour (geste « versé », source abc), au facteur du maillon d'ABC ; A1 compte alors 1 571 « versé ».
A16 (tour 3, N2) la VRAIE barre d'ABC du 16-01-2017 rendue incohérente (clôture 10 % au-dessus du plus haut) : la
   séance sort « non comblé », absente de la série, et ABC compte 1 570 « versé » — le repli ne prend qu'une barre
   UTILISABLE.
A17 (tour 3, N2) INVARIANCE du facteur du maillon : les prix d'ABC tous multipliés par 2 (les volumes intacts) ; le
   facteur du maillon d'ABC devient 0,5, et la série d'Unibail écrite est IDENTIQUE à celle du cas vrai, séance par
   séance, les 4 séances du repli comprises. 2 est choisi parce que multiplier puis diviser par 2 est exact en virgule
   flottante : l'égalité est stricte.
A15, A16 et A17 DÉPENDENT DE LA DÉCISION 2ter, encore ouverte (les 4 séances de janvier-février 2017 prises chez ABC au
   titre de la décision n°47, alors que la décision n°37ter ne visait ABC qu'à partir du 01-03-2017) : si Jean-Luc
   répond non, le repli et ces trois épreuves partent ensemble, avec B14, B15 et B16.

LES SABOTAGES (avec --saboter, ou --saboter=B1,B2…) — chacun doit faire rougir au moins une épreuve : B1 la séance
commune plus proche non refusée · B2 la complétude du raccord non exigée · B3 l'accord du raccord non exigé · B4 les
opérations de la chaîne ignorées · B5 la garde des sauts de la chaîne ôtée · B6 une barre d'ABC versée sans être
utilisable · B7 la voisine de Yahoo non jugée · B8 l'opération dans la référence de la séance décidée ignorée · B9
(contrôle) le rejeu d'un geste parti d'ABC lit la barre de Paris · B10 (contrôle) K15 ignore les divisions
documentées · B11 (contrôle) `lire_abc` garde la dernière de deux séances contradictoires · B12 une barre dégradée
écrite deux fois acceptée · B13 (contrôle) K23 ne vérifie plus l'empreinte d'un fichier présent · B14 une barre
de bnains sans barre sûre ne prend plus la barre d'ABC du même jour · B15 (le X1 de la relecture du tour 2) le repli
prend une barre présente au lieu d'une barre utilisable · B16 (X2) le facteur du maillon du repli forcé à 1.
Sous sabotage, chaque épreuve tombée est suivie de la ligne qu'elle a imprimée : son MOTIF (`motifs`). Une ligne qui
porte un nom d'exception dit un plantage, pas un refus ; ce jeu ne les sépare pas encore (BACKLOG, superviseur R-759 du
01-11-2026, d).

CE QUI N'EST PAS ÉPROUVÉ. ① Que les cours d'ABC de 2017-2023 soient justes au milieu de la période : aucune deuxième
source (etudes/JOURNEE_31-10-2026/unibail_source/RAPPORT.md, § 2.4). ② Les lignes de Yahoo des 14 et 17-04-2023 (A1 les nomme seulement). ③ Le
volume d'ABC de juin 2018 à avril 2023 (carnet unique Paris-Amsterdam ou Paris seul).

USAGE : python3 tests/EPREUVES_DU_COMBLEMENT_DES_20_ANS_Sam_31-10-2026.py <racine du dépôt> [--saboter | --saboter=B1,…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import contextlib, copy, csv, importlib.util, io, json, os, re, shutil, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROGRAMMES = os.path.join(RACINE, "programmes")
REPARATION = os.path.join(PROGRAMMES, "REPARER_L_HISTORIQUE_LONG.py")
CONTROLE = os.path.join(PROGRAMMES, "CONTROLER_L_HISTORIQUE_LONG.py")
MODULES = ("CONTRATS_DES_FICHIERS", "CALENDRIER_DE_LA_BOURSE", "CONTROLER_L_HISTORIQUE_LONG",
           "RECONSTRUIRE_L_HISTORIQUE_LONG", "REPARER_L_HISTORIQUE_LONG")
URW, ML = "UNIBAIL-RODAMCO-WESTFIELD", "MICHELIN"

# (fichier visé, texte cible, remplacement) ; « K » vise le contrôle, sinon la réparation
SABOTAGES = {
    "B1": [("R", " or tous_deux or accord < K.PART_PROPRE:", " or accord < K.PART_PROPRE:")],
    "B2": [("R", "            if len(communes) != len(fenetre) or len(fenetre) < MIN_RACCORD or",
            "            if len(fenetre) < MIN_RACCORD or")],
    "B3": [("R", " or tous_deux or accord < K.PART_PROPRE:", " or tous_deux:")],
    "B4": [("R", "            if dans:\n                arret = f\"{valeur} : chaîne, opération connue",
            "            if False:\n                arret = f\"{valeur} : chaîne, opération connue")],
    "B5": [("R", "            if sauts:\n                arret = f\"{valeur} : chaîne, saut",
            "            if False:\n                arret = f\"{valeur} : chaîne, saut")],
    "B6": [("R", "                    sure = K.barre_utilisable({valeur: brut}, valeur, d, frozenset())\n",
            "                    sure = d in brut\n")],
    "B7": [("R", "        faux = [f\"{x} : {r!r}\" for x, r in bords if abs(r / f - 1) > K.ECART]\n", "        faux = []\n")],
    "B8": [("R", "                if ref[0] < o[0] <= ref[-1] and RC.preuve(o) != RC.APPLIQUEE_PAR_YAHOO]\n",
            "                if False]\n")],
    "B9": [("K", "            base = ({\"paris\": paris, \"abc\": abc or {}}[g[\"depart\"]]",
            "            base = ({\"paris\": paris, \"abc\": paris}[g[\"depart\"]]")],
    "B10": [("K", "            for j in divisees:\n                permise *= documentees[v][j]\n",
             "            for j in divisees:\n                permise *= 1.0\n")],
    "B11": [("K", "                if deja is not None and deja != barre:\n", "                if False:\n")],
    "B13": [("K", "e]\n            if len(lignes) != 1:\n", "e]\n            if False:\n")],
    "B14": [("R", "                if not sure and repli and K.barre_utilisable({valeur: repli[1]}, valeur, d, frozenset()):\n",
             "                if False:\n")],
    "B12": [("R", "            if not ok or not r[\"constat\"].strip() or (r[\"valeur\"], r[\"date\"]) in vues:\n",
             "            if not ok or not r[\"constat\"].strip():\n")],
    # tour 3 (superviseur R-759 du 01-11-2026, b) : les X1 et X2 de la relecture du tour 2
    "B15": [("R", "if not sure and repli and K.barre_utilisable({valeur: repli[1]}, valeur, d, frozenset()):",
             "if not sure and repli and d in repli[1]:")],
    "B16": [("R", "nouvelles[d], fp, fv = barre(b_r[d], f_r, v_r, 1.0)", "nouvelles[d], fp, fv = barre(b_r[d], 1.0, 1.0, 1.0)")],
}

# Les 4 séances d'Unibail de janvier-février 2017 dont la barre de bnains est incohérente (relecture du lot, D1) ;
# elles dépendent de la décision 2ter, encore ouverte.
JOURS_DU_REPLI = ("2017-01-16", "2017-01-23", "2017-02-06", "2017-02-16")


def motifs(sortie, tombees):
    """Rend, pour chaque épreuve tombée, la ligne qu'elle a imprimée : le motif de son rouge.

    ① RÔLE — Montrer POURQUOI un sabotage mord, et pas seulement qu'il mord.
    ② CONTEXTE D'APPEL — `main`, après chaque sabotage.
    ③ ENTRÉE — `sortie` : le texte imprimé par `epreuves` sous ce sabotage · `tombees` : les clés des épreuves rouges.
    ④ CONDITIONS D'ENTRÉE — Chaque épreuve imprime ses lignes en commençant par sa clé (« A16 : … »), et `tenter`
      imprime « clé : Exception : … » quand elle plante.
    ⑤ SORTIE — UNE valeur : la liste des lignes « [clé] … », une par épreuve tombée ; « (aucune ligne imprimée) » quand
      l'épreuve n'a rien écrit (A7, par exemple, juge sans imprimer).
      [rend: 1]
    ⑥ TRAITEMENT — Garder les lignes de `sortie` qui commencent, après les blancs, par la clé suivie d'une fin de mot.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du tour 2 (01-11-2026) : un sabotage comptait « mord » alors qu'il ne faisait que planter ;
      le relecteur a dû fabriquer des copies « bavardes » pour le voir.
    ⑨ CE QUI CLOCHE — Le motif est montré, il n'est pas jugé (BACKLOG, superviseur R-759 du 01-11-2026, d). · La même
      fonction vit dans les trois jeux du lot (causes, comblement, débuts) : chaque jeu se lance seul et n'importe pas
      les autres ; une seule copie partagée serait à créer (BACKLOG, avec le point d).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    lignes = sortie.splitlines()
    rendu = []
    for e in tombees:
        a = [x.strip()[:400] for x in lignes if re.match(r"\s*" + re.escape(e) + r"\b", x)]
        rendu.append(f"    [{e}] " + (" || ".join(a) if a else "(aucune ligne imprimée)"))
    return rendu


def charger(sabotage=None):
    """Charge le contrôle puis la réparation (qui charge la reconstruction), vrais ou sabotés, dans un dossier jetable."""
    dossier = PROGRAMMES
    if sabotage is not None:
        dossier = tempfile.mkdtemp()
        for nom in MODULES:
            shutil.copy(os.path.join(PROGRAMMES, nom + ".py"), dossier)
        for cle, chemin in (("R", REPARATION), ("K", CONTROLE)):
            texte = open(chemin, encoding="utf-8").read()
            for f, cible, remplace in sabotage:
                if f == cle:
                    texte = texte.replace(cible, remplace)
            open(os.path.join(dossier, os.path.basename(chemin)), "w", encoding="utf-8").write(texte)
    for nom in MODULES:
        sys.modules.pop(nom, None)
    sys.path.insert(0, dossier)
    try:
        sortie = []
        for nom in ("CONTROLER_L_HISTORIQUE_LONG", "REPARER_L_HISTORIQUE_LONG"):
            sp = importlib.util.spec_from_file_location(nom, os.path.join(dossier, nom + ".py"))
            m = importlib.util.module_from_spec(sp)
            sys.modules[nom] = m
            sp.loader.exec_module(m)
            sortie.append(m)
    finally:
        sys.path.remove(dossier)
    return sortie


def donnees(K, R):
    """Les vraies données du dépôt, lues par les fonctions du contrôle (R-708), comme `reparer` les lit."""
    series, defauts, _ = K.lire_cours(os.path.join(RACINE, K.ORIGINE))
    bnains, defauts_b, _ = K.lire_paris(RACINE)
    assert not defauts and not defauts_b
    evenements = json.load(open(os.path.join(RACINE, K.EVENEMENTS), encoding="utf-8"))
    detachements, _ = K.lire_detachements(os.path.join(RACINE, K.DROITS), os.path.join(RACINE, K.OFFICIELS))
    francfort = K.lire_francfort(os.path.join(RACINE, K.FRANCFORT))
    seances = K.CAL.lire_les_seances(RACINE)
    # les jours douteux comme `reparer` les calcule : après `defaire`, hors des fenêtres reconstruites, moins les séances
    # où l'indice donne tort à Yahoo (une autre recette en change cinq : mesuré le 31-10-2026, A1)
    a_defaire = K.lire_a_defaire(os.path.join(RACINE, K.VERDICTS_YAHOO))
    evenements = K.sans_les_divisions_fausses(evenements, a_defaire)
    with contextlib.redirect_stdout(io.StringIO()):
        R.defaire(series, a_defaire, [])
    fenetres = {(v, d) for v, du, au, *_ in R.RECONSTRUCTIONS for d in series.get(v, {}) if du <= d <= au}
    tort = {d for jours, *_, verdict in K.arbitre_de_l_indice(series, bnains, evenements,
                                                                K.lire_indice(os.path.join(RACINE, K.INDICE)), fenetres)
            if verdict == "le fichier a tort" for d in jours}
    douteux = K.jours_douteux(K.ecarts(series, bnains, exclure=fenetres)) - tort
    abc = K.lire_abc(RACINE)[0]
    return series, bnains, evenements, detachements, francfort, seances, douteux, abc


def operations(R, D, divisions_en_plus=()):
    series, bnains, evenements, detachements = D[0], D[1], D[2], D[3]
    divisions = R.RC.lire_divisions(os.path.join(RACINE, R.RC.DIVISIONS)) + list(divisions_en_plus)
    officielles = R.RC.lire_divisions_officielles(os.path.join(RACINE, R.RC.OFFICIELLES))
    a_defaire = R.K.lire_a_defaire(os.path.join(RACINE, R.K.VERDICTS_YAHOO))
    return R.RC.operations(evenements, a_defaire, detachements, bnains, divisions,
                           os.path.join(RACINE, R.K.VERDICTS_YAHOO), officielles)[0]


def ligne_de_bnains(valeur, date, diviseur):
    vraie = DIVISIONS_REELLES[0]
    return dict(vraie, valeur=valeur, date=date, diviseur=diviseur, commentaire="division FABRIQUÉE pour l'épreuve")


def epreuves(K, R, D):
    """Joue chaque épreuve sur le contrôle et la réparation chargés ; rend leurs verdicts.

    ① RÔLE — Le cœur du jeu : A1 à A17, sur les programmes vrais (Z0) ou sabotés (`charger`).
    ② CONTEXTE D'APPEL — `main`, une fois sur les vrais programmes, puis une fois par sabotage demandé.
    ③ ENTRÉE — `K`, `R` : les modules du contrôle et de la réparation · `D` : les vraies données, lues par `donnees`.
    ④ CONDITIONS D'ENTRÉE — `main` a posé `DIVISIONS_REELLES`.
    ⑤ SORTIE — UNE valeur : clé de l'épreuve → vrai (verte) ou faux (rouge, ou plantée).
      [rend: 1]
    ⑥ TRAITEMENT — Chaque épreuve passe par `tenter` : une exception est imprimée et compte pour un rouge. Les
      données ne sont jamais modifiées en place : chaque épreuve copie ce qu'elle abîme (`abc_avec`, `chaine`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 : chaque garde a son épreuve, et chaque épreuve ses dents (`SABOTAGES`).
    ⑨ CE QUI CLOCHE — Une épreuve qui plante compte comme un rouge (BACKLOG, superviseur R-759 du 01-11-2026, d).
      · A15 à A17 dépendent de la décision 2ter, encore ouverte.
    ⑩ EFFET — Imprime une ligne par épreuve ; crée et supprime des dossiers jetables (A11, A13, A14).
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    res = {}
    series, bnains, evenements, detachements, francfort, seances, douteux, abc = D

    def tenter(cle, f):
        try:
            res[cle] = bool(f())
        except Exception as e:
            print(f"      {cle} : {type(e).__name__} : {e}")
            res[cle] = False

    def chaine(abc_=None, chaine_=None, divisions_en_plus=()):
        s, src = dict(series), {(v, d): "yahoo" for v, x in series.items() for d in x}
        s[URW] = dict(series[URW])
        j = []
        ops = operations(R, D, divisions_en_plus)
        garde = R.SERIES_EN_CHAINE
        try:
            if chaine_ is not None:
                R.SERIES_EN_CHAINE = chaine_
            with contextlib.redirect_stdout(io.StringIO()):
                n, refus = R.combler_par_raccords(s, src, bnains, abc_ if abc_ is not None else abc, evenements,
                                                  douteux, j, ops, francfort, seances=seances)
        finally:
            R.SERIES_EN_CHAINE = garde
        return n, refus, s, src, j

    def abc_avec(f):
        a = dict(abc)
        a[URW] = f(dict(abc[URW]))
        return a

    def arret(cle, mots, **k):
        def f():
            n, refus, s, src, j = chaine(**k)
            print(f"      {cle} : {refus}")
            return not n and len(refus) == 1 and all(m in refus[0] for m in mots) and not j and s[URW] == series[URW]
        tenter(cle, f)

    def a1():
        n, refus, s, src, j = chaine()
        l1010 = [l for l in j if l[1] == "2010-10-07"]
        verse = [l for l in j if l[2] == "versé"]
        print(f"      A1 : {n}, refus {refus}, non comblé {sum(1 for l in j if l[2] == 'non comblé')}")
        zone = [l for l in verse if l[1] >= "2017-03-01"]
        # 2 476 et 7 depuis le 04-11-2026 (2 471 et 12 avant) : les 5 barres incohérentes d'Unibail (02-08-2011,
        # 11-06-2012, 01-08-2013, 22-06-2016, 21-12-2016) sont rectifiées sur décision (choix D6, délégation n°129 ;
        # donnees/sources_bnains/BARRES_DE_PARIS_RECTIFIEES.csv), et la chaîne les comble
        return (n == {"abc": 1571, "bnains": 2476} and not refus and sum(1 for l in j if l[2] == "non comblé") == 7
                and len(l1010) == 1 and "À SIGNALER" in l1010[0][6] and "20 €" in l1010[0][6]
                and all("'2023-04-14', '2023-04-17'" in l[6] for l in zone) and len(zone) == 1567
                and all(src[(URW, l[1])] == "abc" for l in verse))
    tenter("A1", a1)

    def a15():
        """D1 de la relecture : les 4 barres de bnains incohérentes de janvier-février 2017 prennent la barre d'ABC.

        ① RÔLE — Dire que le repli de `combler_par_raccords` prend, pour ces 4 séances, la barre d'ABC du même jour.
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Les vraies données ; la première des 4 barres de bnains est inutilisable.
        ⑤ SORTIE — UNE valeur : vrai si les 4 séances sont « versé », source abc, à la barre d'ABC.
          [rend: 1]
        ⑥ TRAITEMENT — Jouer la chaîne vraie ; lire le journal des 4 jours.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture du lot du 31-10-2026, D1. Les 4 jours sont lus de `JOURS_DU_REPLI` depuis le tour 3,
          partagés avec A16 et A17 (un chiffre qui existe ailleurs ne se recopie pas, R-708).
        ⑨ CE QUI CLOCHE — Dépend de la décision 2ter, encore ouverte. · Le facteur du maillon d'ABC vaut 1 : seule
          A17 éprouve qu'il est bien appliqué.
        ⑩ EFFET — Imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        n, refus, s, src, j = chaine()
        jours = JOURS_DU_REPLI
        lignes = {l[1]: l for l in j if l[1] in jours}
        print(f"      A15 : {[(d, lignes[d][2], src.get((URW, d))) for d in jours if d in lignes]}")
        return (all(d in lignes and lignes[d][2] == "versé" and src[(URW, d)] == "abc" and s[URW][d] == abc[URW][d]
                    and "barre de Paris du maillon abc" in lignes[d][6] for d in jours)
                and not K.barre_utilisable(bnains, URW, jours[0], frozenset()))
    tenter("A15", a15)

    def a16():
        """Le repli ne prend qu'une barre d'ABC UTILISABLE : une vraie barre rendue incohérente sort « non comblé ».

        ① RÔLE — Donner des dents à la condition « utilisable » du repli (sabotage B15, le X1 de la relecture).
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — ABC a une barre le premier jour de `JOURS_DU_REPLI` (vraie ligne, R-732).
        ⑤ SORTIE — UNE valeur : vrai si ce jour sort « non comblé », absent de la série, ABC à 1 570 « versé », sans arrêt.
          [rend: 1]
        ⑥ TRAITEMENT — Copier les cours d'ABC ; la clôture de ce jour mise à 1,1 fois le plus haut (incohérente,
          `K.barre_utilisable` la refuse) ; jouer la chaîne ; lire le journal de ce jour.
        ⑦ UNITÉ — Des euros (la barre) ; des séances (les comptes).
        ⑧ POURQUOI — La notice de `combler_par_raccords` promet « la barre utilisable de la source du maillon
          précédent » ; les 4 vraies barres sont cohérentes, et aucune épreuve ne le voyait (relecture du tour 2, N2 ;
          superviseur R-759 du 01-11-2026, b).
        ⑨ CE QUI CLOCHE — Dépend de la décision 2ter, encore ouverte.
        ⑩ EFFET — Imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        d = JOURS_DU_REPLI[0]
        b = abc[URW][d]
        casse = (b[0], b[1], b[2], b[1] * 1.1) + tuple(b[4:])
        n, refus, s, src, j = chaine(abc_=abc_avec(lambda x: dict(x, **{d: casse})))
        l = [x for x in j if x[1] == d]
        print(f"      A16 : barre d'ABC du {d} rendue {casse[:4]} → {[(x[2], x[6][:110]) for x in l]} ; {n}, refus {refus}")
        return (not refus and n["abc"] == 1570 and len(l) == 1 and l[0][2] == "non comblé" and d not in s[URW]
                and not K.barre_utilisable({URW: {d: casse}}, URW, d, frozenset()))
    tenter("A16", a16)

    def a17():
        """Invariance : ABC aux prix multipliés par 2 donne la même série d'Unibail, séance par séance.

        ① RÔLE — Donner des dents au facteur du maillon dans le repli (sabotage B16, le X2 de la relecture).
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Les vraies données ; la chaîne vraie comble sans arrêt (A1).
        ⑤ SORTIE — UNE valeur : vrai si la série écrite est identique au cas vrai, mêmes comptes, sans arrêt, et si le
          journal dit le facteur 0,5 au maillon d'ABC et dans les 4 lignes du repli.
          [rend: 1]
        ⑥ TRAITEMENT — Jouer la chaîne vraie, puis la chaîne avec les prix d'ABC × 2 (volumes intacts) ; comparer les
          deux séries d'Unibail séance par séance ; lire les facteurs écrits au journal.
        ⑦ UNITÉ — Un facteur sans unité ; des séances.
        ⑧ POURQUOI — Le vrai facteur du maillon d'ABC vaut 1 : une barre prise sans son facteur était juste par hasard.
          Une invariance plutôt qu'une valeur fabriquée : elle ne dépend d'aucun chiffre écrit dans l'épreuve
          (superviseur R-759 du 01-11-2026, b). 2 est exact en virgule flottante, l'égalité est stricte. Sous B16, les
          4 barres du repli sortent doublées.
        ⑨ CE QUI CLOCHE — Dépend de la décision 2ter, encore ouverte. · Le facteur de VOLUME du repli n'a pas
          d'invariance éprouvée (les volumes d'ABC ne sont pas touchés).
        ⑩ EFFET — Imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        n0, r0, s0, _, _ = chaine()
        deux = abc_avec(lambda x: {d: tuple(v * 2 for v in b[:4]) + tuple(b[4:]) for d, b in x.items()})
        n2, r2, s2, _, j2 = chaine(abc_=deux)
        autres = sorted(d for d in set(s0[URW]) | set(s2[URW]) if s0[URW].get(d) != s2[URW].get(d))
        repli = [x[6] for x in j2 if x[1] in JOURS_DU_REPLI]
        maillon = [x[6] for x in j2 if x[2] == "versé" and x[1] >= "2017-03-01"][:1]
        print(f"      A17 : ABC × 2 : {n2}, refus {r2} ; séances différentes du cas vrai : {len(autres)} {autres[:4]} ; "
              f"repli au facteur 0,5 : {sum('au facteur de ce maillon 0.5' in t for t in repli)}/{len(JOURS_DU_REPLI)} ; "
              f"maillon d'ABC au facteur 0,5 : {bool(maillon) and 'facteur 0.5 ' in maillon[0]}")
        return (not r0 and not r2 and n2 == n0 and autres == [] and len(repli) == len(JOURS_DU_REPLI)
                and all("au facteur de ce maillon 0.5" in t for t in repli) and bool(maillon)
                and "facteur 0.5 " in maillon[0])
    tenter("A17", a17)

    def sans_le_02_05(x):
        del x["2023-05-02"]
        return x
    arret("A2", ("raccord de abc",), abc_=abc_avec(sans_le_02_05))
    fenetre = sorted(d for d in abc[URW] if "2023-04-18" <= d <= "2023-06-30")[:10]
    arret("A3", ("raccord de abc", "accord 8"),
          abc_=abc_avec(lambda x: {d: (tuple(v * 1.01 for v in b[:4]) + b[4:]) if d in fenetre else b
                                   for d, b in x.items()}))
    arret("A4", ("opération connue dans la chaîne", "2012-01-02"),
          divisions_en_plus=[ligne_de_bnains(URW, "2012-01-02", "1.1")])
    arret("A5", ("saut",), abc_=abc_avec(lambda x: {d: (tuple(v * 2 for v in b[:4]) + b[4:]) if d < "2020-01-02" else b
                                                    for d, b in x.items()}))
    (v0, maillons, signales, raison), = R.SERIES_EN_CHAINE
    decale = ((v0, ((maillons[0][0], maillons[0][1], ("2023-04-19", "2023-06-30")),) + maillons[1:], signales, raison),)
    arret("A6", ("raccord de abc", "2023-04-18"), chaine_=decale)

    def a7():
        a = abc_avec(lambda x: dict(x, **{"2017-03-15": (10.0, 9.0, 11.0, 10.0, 1000.0)}))
        n, refus, s, src, j = chaine(abc_=a)
        l = [x for x in j if x[1] == "2017-03-15"]
        return (not refus and n["abc"] == 1570 and len(l) == 1 and l[0][2] == "non comblé"
                and "barre d'ABC inutilisable" in l[0][6] and "2017-03-15" not in s[URW])
    tenter("A7", a7)

    def seance(abimer=None, divisions_en_plus=()):
        s, src = dict(series), {(v, d): "yahoo" for v, x in series.items() for d in x}
        s[ML] = dict(series[ML])
        if abimer:
            abimer(s[ML])
        j = []
        n, refus = R.combler_les_seances(s, src, bnains, evenements, douteux, j, operations(R, D, divisions_en_plus),
                                         francfort, seances=seances)
        return n, refus, s, j

    def a8():
        n, refus, s, j = seance()
        print(f"      A8 : {n}, {refus}, facteur {j[0][5] if j else None}")
        return n == 1 and not refus and abs(j[0][5] - 0.24156) < 1e-4 and j[0][1] == "2000-07-24" and \
            s[ML]["2000-07-24"][3] == round(bnains[ML]["2000-07-24"][3] * j[0][5], K.DECIMALES)
    tenter("A8", a8)

    def a9_a10(cle, mots, **k):
        def f():
            n, refus, s, j = seance(**k)
            print(f"      {cle} : {refus}")
            return n == 0 and len(refus) == 1 and all(m in refus[0] for m in mots) and not j and "2000-07-24" not in s[ML]
        tenter(cle, f)

    def plus5(x):
        x["2000-07-21"] = tuple(v * 1.05 for v in x["2000-07-21"][:4]) + x["2000-07-21"][4:]
    a9_a10("A9", ("voisine", "2000-07-21"), abimer=plus5)
    a9_a10("A10", ("opération connue", "2000-08-01"), divisions_en_plus=[ligne_de_bnains(ML, "2000-08-01", "1.1")])

    def a11():
        repare, _, _ = K.lire_cours(os.path.join(RACINE, K.FICHIER))
        sources = K.lire_les_sources(os.path.join(RACINE, K.FICHIER))
        journal = K.lire_journal(os.path.join(RACINE, K.JOURNAL))
        cle = (URW, "2020-06-02")
        sous = {v: {d: repare[v][d] for d in repare[v] if d == "2020-06-02"} for v in (URW,)}
        origine = {URW: {}}
        ok = K.lignes_non_rejouees(sous, sources, origine, {}, {cle: journal[cle]}, abc) == []
        faux = [dict(g, close_apres=str(float(g["close_apres"]) + 0.01)) for g in journal[cle]]
        un = K.lignes_non_rejouees(sous, sources, origine, {}, {cle: faux}, abc)
        deux = K.lignes_non_rejouees(sous, sources, origine, {}, {cle: journal[cle]}, None)
        r = tempfile.mkdtemp()
        os.makedirs(os.path.join(r, K.ABC))
        open(os.path.join(r, K.ABC, "a.csv"), "w").write("FR0013326246;02/06/20;1;2;0,5;1,5;10\n")
        open(os.path.join(r, K.ABC, "b.csv"), "w").write("FR0013326246;02/06/20;1;2;0,5;1,6;10\n")
        try:
            K.lire_abc(r)
            trois = False
        except ValueError as e:
            trois = "déjà lu avec d'autres chiffres" in str(e)
        shutil.rmtree(r, ignore_errors=True)
        print(f"      A11 : rejeu juste {ok}, faux {un[:1]}, sans ABC {deux[:1]}, doublon refusé {trois}")
        return ok and len(un) == 1 and len(deux) == 1 and "ABC, qui n'a pas de barre" in deux[0] and trois
    tenter("A11", a11)

    def a12():
        repare, defauts, venues = K.lire_cours(os.path.join(RACINE, K.FICHIER))
        officielles = K.lire_divisions_officielles(os.path.join(RACINE, K.DIVISIONS_DOCUMENTEES))
        sans = avec = None
        for nom, off in (("sans", None), ("avec", officielles)):
            with contextlib.redirect_stdout(io.StringIO()):
                k15 = [c for n, *_, c in K.controler(repare, defauts, bnains, K.sans_les_divisions_fausses(
                    evenements, K.lire_a_defaire(os.path.join(RACINE, K.VERDICTS_YAHOO))), venues, detachements,
                    seances=seances, officielles=off, francfort=francfort) if n == "K15"][0]
            sans, avec = (k15, avec) if nom == "sans" else (sans, k15)
        print(f"      A12 : K15 sans la table {sans[:2]}, avec {avec[:2]}")
        return any("STMICROELECTRONICS 2000-05-08→2000-05-09" in c for c in sans) and avec == []
    tenter("A12", a12)

    def a13():
        table = R.lire_les_degradees(os.path.join(RACINE, R.DEGRADEES))
        journal = K.lire_journal(os.path.join(RACINE, K.JOURNAL))
        refaites = [(v, d) for v, d, _ in table if [g["geste"] for g in journal.get((v, d), [])][-2:] == ["écarté", "comblé"]]
        texte = open(os.path.join(RACINE, R.DEGRADEES), encoding="utf-8").read().splitlines()
        r = tempfile.mkdtemp()
        open(os.path.join(r, "t.csv"), "w", encoding="utf-8").write("\n".join(texte + [texte[1]]) + "\n")
        try:
            R.lire_les_degradees(os.path.join(r, "t.csv"))
            refus = False
        except ValueError:
            refus = True
        shutil.rmtree(r, ignore_errors=True)
        print(f"      A13 : {len(table)} barres, {len(refaites)} écartées puis comblées, doublon refusé {refus}")
        return (len(table) == 81 and ("ESSILORLUXOTTICA", "2004-03-02") not in {(v, d) for v, d, _ in table}
                and len(refaites) == 81 and refus)
    tenter("A13", a13)

    def a14():
        """K23 sur la table des divisions de bnains : juste au dépôt ; une ligne retirée → son empreinte n'est plus inscrite."""
        juste = K.maillons_manquants(RACINE, [R.RC.DIVISIONS.replace(os.sep, "/")])
        r = tempfile.mkdtemp()
        racine = os.path.join(r, "depot")
        shutil.copytree(RACINE, racine, copy_function=os.link, ignore=shutil.ignore_patterns(".git"))   # liens durs
        cible = os.path.join(racine, R.RC.DIVISIONS)
        lignes = open(cible, encoding="utf-8").read().splitlines(keepends=True)
        os.remove(cible)                                   # recréé, jamais écrit par-dessus : le dépôt reste intact
        open(cible, "w", encoding="utf-8").writelines(lignes[:-1])
        faux = K.maillons_manquants(racine, [R.RC.DIVISIONS.replace(os.sep, "/")])
        shutil.rmtree(r, ignore_errors=True)
        print(f"      A14 : au dépôt {juste} ; une ligne retirée {faux[:1]}")
        return juste == [] and any("empreinte" in c for c in faux) and R.RC.DIVISIONS in R.LU \
            and not hasattr(R, "LU_HORS_REGISTRE")
    tenter("A14", a14)
    return res


def main():
    """Joue les épreuves sur les vrais programmes, puis sous chaque sabotage demandé ; rend le code de sortie.

    ① RÔLE — Porter le jeu : Z0, puis les sabotages.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `sys.argv` : la racine, et `--saboter` ou `--saboter=B1,…`.
    ④ CONDITIONS D'ENTRÉE — La racine est un dépôt complet.
    ⑤ SORTIE — UNE valeur : 0 (tout vert, et chaque sabotage demandé mord) · 1 (une épreuve rouge, ou un sabotage
      qui ne mord pas) · 2 (une cible de sabotage absente ou en double).
      [rend: 1]
    ⑥ TRAITEMENT — Charger, lire, jouer ; pour chaque sabotage : vérifier que sa cible est unique, charger les copies
      sabotées, rejouer en gardant la sortie, imprimer « mord » ou « NE MORD PAS », puis (tour 3) le motif de chaque
      épreuve tombée (`motifs`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 ; le motif imprimé, parce qu'un « mord » sans motif ne dit pas si c'est un refus ou un plantage
      (relecture du tour 2, Q2).
    ⑨ CE QUI CLOCHE — Un plantage compte encore comme une morsure (BACKLOG).
    ⑩ EFFET — Imprime ; crée des dossiers jetables sous le dossier d'essai.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    global DIVISIONS_REELLES
    K, R = charger()
    DIVISIONS_REELLES = R.RC.lire_divisions(os.path.join(RACINE, R.RC.DIVISIONS))
    D = donnees(K, R)
    res = epreuves(K, R, D)
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programmes tels quels : {len(res) - len(rouges)}/{len(res)} épreuves vertes"
          + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        for k, paires in SABOTAGES.items():
            if choix and k not in choix[0]:
                continue
            for f, cible, _ in paires:
                n = open(CONTROLE if f == "K" else REPARATION, encoding="utf-8").read().count(cible)
                if n != 1:
                    print(f"{k} NE S'APPLIQUE PLUS : texte cible trouvé {n} fois")
                    return 2
            K2, R2 = charger(paires)
            garde = io.StringIO()
            with contextlib.redirect_stdout(garde):
                r = epreuves(K2, R2, D)
            tombees = [e for e, v in r.items() if not v]
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}")
            for l in motifs(garde.getvalue(), tombees):
                print(l)
            if not tombees:
                code = 1
    return code


if __name__ == "__main__":
    _DOSSIER_D_ESSAI = tempfile.mkdtemp(prefix="epreuves_comblement_")
    tempfile.tempdir = os.environ["TMPDIR"] = _DOSSIER_D_ESSAI
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(_DOSSIER_D_ESSAI, ignore_errors=True)
