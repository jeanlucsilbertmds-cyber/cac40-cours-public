#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_CAUSES_DES_TROUS — Sam 31-10-2026 (Paris)
Rôle : prouver que programmes/CONTROLER_LES_CAUSES_DES_TROUS.py rougit dès qu'une séance sans cours n'a pas sa cause
prouvée, et que chaque épreuve a des dents (R-731).
Quand l'appeler : avant toute livraison qui touche ce contrôle, la table donnees/CAUSES_DES_SEANCES_SANS_COURS.csv, ou
l'historique long réparé.

À QUOI ÇA SERT. Décision de Jean-Luc du 31-10-2026 à 21h08 (annexe n°48) : « chaque séance manquante porte sa cause
prouvée, sinon le contrôle rougit ». Les épreuves jouent les VRAIES lignes du dépôt ; les défauts sont FABRIQUÉS sur des
copies en mémoire (le fichier du dépôt n'est jamais réécrit), ou dans une racine jetable de quelques fichiers.

LES ÉPREUVES :
T1 vraies données, le programme entier (`main`) : code 0.
T2 une séance manquante AJOUTÉE sans cause — la vraie ligne LVMH du 15-06-2012 ôtée du fichier en mémoire : un cas, et
   un seul, « LVMH 2012-06-15 : séance sans cours, SANS CAUSE » (R-732 : un cas venu d'une vraie ligne).
T3 une ligne de cause FABRIQUÉE sur une séance pourvue (LVMH 15-06-2012, « suspension », cause que rien d'autre ne
   contredit) : un cas « couvre 1 séance(s)
   où la valeur a un cours ».
T4 la cause d'une vraie ligne remplacée par « INCONNUE » (hors de la liste fermée) : un cas « liste fermée », et les
   séances de la ligne sortent « SANS CAUSE ».
T5 la preuve d'une vraie ligne vidée : « sans preuve ».
T6 les sources cherchées d'une vraie ligne « source perdue » vidées : « sans les sources cherchées ».
T7 une vraie ligne écrite deux fois : « DEUX CAUSES ».
T8 la table absente d'une racine jetable : code 2, jamais 0 (R-734).
T9 la table à l'en-tête faux, dans une racine jetable : code 2.
T10 une ligne aux dates dans le désordre : « dates illisibles ou dans le désordre ».
T12 à T14 la vraie séance LVMH du 15-06-2012 ôtée, et une cause que nos fichiers contredisent : « pas encore cotée » au
    milieu de sa série, « hors indice » alors que LVMH est au CAC 40 (table des passages), « plus cotée » avant sa
    dernière barre — chacune refusée (relecture du lot du 31-10-2026, D3).
T11 le programme entier, la table privée de sa ligne de Schneider du 07-06-2001 (racine jetable) : code 1, la séance
    nommée « SANS CAUSE » — le programme rougit, pas seulement la fonction.
T15 (tour 3, N1 de la relecture du tour 2) le programme entier, une ligne « hors indice » FABRIQUÉE sur LVMH le
    15-06-2012 ajoutée à la table (racine jetable ; seule la table est recréée, le fichier de cours n'est jamais
    réécrit : la racine jetable est en liens durs) : code 1 ET le motif « « hors indice » contredit » sur cette ligne —
    le code seul ne suffit pas, la même ligne sortirait aussi « couvre 1 séance(s) où la valeur a un cours ».
T16 (tour 3, X4) la borne de fin d'une période est incluse : la première période FERMÉE de la table des passages, prise
    par propriété (première valeur dans l'ordre, première période qui a une fin ; aujourd'hui ACCOR, sortie du CAC 40 le
    18-09-2020), et une ligne « hors indice » le jour même de sa fin : « « hors indice » contredit ».
T17 (tour 3, a′) la fermeture quand la donnée manque : les passages privés de LVMH, une ligne « hors indice » sur LVMH
    le 15-06-2012 (séance ôtée) : « « hors indice » non vérifiable », jamais une acceptation.

LES SABOTAGES (avec --saboter, ou --saboter=C1,C2…) — chacun doit faire rougir au moins une épreuve : C1 une séance
sans cause n'est pas dite · C2 deux causes tolérées · C3 une cause sur une séance pourvue tolérée · C4 la liste fermée
non vérifiée · C5 la preuve non exigée · C6 les sources cherchées non exigées · C7 `main` rend 0 quoi qu'il trouve ·
C8 l'en-tête non vérifié · C9 les dates non vérifiées · C10 « pas encore cotée » non confrontée à la première barre ·
C11 « plus cotée » non confrontée à la dernière · C12 « hors indice » non confrontée aux passages dans le CAC 40 ·
C13 (le X4 de la relecture du tour 2) la borne de fin exclue (`<` au lieu de `<=`) · C14 (X5) `passages_par_valeur`
rend des listes vides · C15 (X6) `main` ne passe plus les passages · C16 (tour 3) la fermeture « non vérifiable » ôtée.
Sous sabotage, chaque épreuve tombée est suivie de la ligne qu'elle a imprimée : son MOTIF (`motifs`). Une ligne qui
porte un nom d'exception dit un plantage, pas un refus ; ce jeu ne les sépare pas encore (BACKLOG, superviseur R-759 du
01-11-2026, d).

CE QUI N'EST PAS ÉPROUVÉ. ① La VÉRITÉ d'une preuve : le contrôle exige un texte, il ne le lit pas. ② Le découpage de la
table en lignes : il vient de l'outil d'écriture du lot (hors dépôt), la table est jugée telle qu'écrite.

USAGE : python3 tests/EPREUVES_DES_CAUSES_DES_TROUS_Sam_31-10-2026.py <racine du dépôt> [--saboter | --saboter=C1,…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus (texte cible absent ou en double).
"""
import contextlib, csv, importlib.util, io, os, re, shutil, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROGRAMMES = os.path.join(RACINE, "programmes")
CONTROLE = os.path.join(PROGRAMMES, "CONTROLER_LES_CAUSES_DES_TROUS.py")
MODULES = ("CONTRATS_DES_FICHIERS", "CALENDRIER_DE_LA_BOURSE", "CONTROLER_L_HISTORIQUE_LONG")

SABOTAGES = {
    "C1": [('                cas.append(f"{v} {d} : séance sans cours, SANS CAUSE")\n', "                pass\n")],
    "C2": [("            elif len(n) > 1:\n", "            elif False:\n")],
    "C3": [("        if pourvues:\n", "        if False:\n")],
    "C4": [('if r["cause"] not in CAUSES_DES_TROUS', "if False")],
    "C5": [('else "sans preuve" if not r["preuve"].strip()', 'else "sans preuve" if False')],
    "C6": [('and not r["sources_cherchees"].strip() else ""', 'and False else ""')],
    "C7": [("    return 1 if cas else 0\n", "    return 0\n")],
    "C8": [("        if lecteur.fieldnames != CAUSES_DES_SEANCES_SANS_COURS:\n", "        if False:\n")],
    "C10": [('if r["cause"] == PAS_ENCORE and r["fin"] >= premiere', 'if False')],
    "C11": [('if r["cause"] == PLUS_COTEE and r["debut"] <= derniere', 'if False')],
    "C12": [('if r["cause"] == HORS_INDICE and dedans else ""', 'if False else ""')],
    "C9": [("            dates_ok = a == r[\"debut\"] and z == r[\"fin\"] and a <= z\n", "            dates_ok = True\n")],
    # tour 3 (superviseur R-759 du 01-11-2026, a, a′ et c) : les X4, X5 et X6 de la relecture du tour 2, et la fermeture
    "C13": [('(y is None or r["debut"] <= y)', '(y is None or r["debut"] < y)')],
    "C14": [('            sortie[nom] = [(a.isoformat(), b.isoformat() if b else None) for a, b in lu["dans_l_indice"].get(m, [])]',
             '            sortie[nom] = []')],
    "C15": [("    cas = cas_des_causes(series, cal, causes, passages)", "    cas = cas_des_causes(series, cal, causes, {})")],
    "C16": [('if r["cause"] == HORS_INDICE and not periodes', 'if False')],
}


def motifs(sortie, tombees):
    """Rend, pour chaque épreuve tombée, la ligne qu'elle a imprimée : le motif de son rouge.

    ① RÔLE — Montrer POURQUOI un sabotage mord, et pas seulement qu'il mord.
    ② CONTEXTE D'APPEL — `main`, après chaque sabotage.
    ③ ENTRÉE — `sortie` : le texte imprimé par `epreuves` sous ce sabotage · `tombees` : les clés des épreuves rouges.
    ④ CONDITIONS D'ENTRÉE — Chaque épreuve imprime ses lignes en commençant par sa clé (« T15 : … »), et `tenter`
      imprime « clé : Exception : … » quand elle plante.
    ⑤ SORTIE — UNE valeur : la liste des lignes « [clé] … », une par épreuve tombée ; « (aucune ligne imprimée) » quand
      l'épreuve n'a rien écrit.
      [rend: 1]
    ⑥ TRAITEMENT — Garder les lignes de `sortie` qui commencent, après les blancs, par la clé suivie d'une fin de mot.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du tour 2 (01-11-2026) : un sabotage comptait « mord » alors qu'il ne faisait que planter
      (G6, KeyError) ; le relecteur a dû fabriquer des copies « bavardes » pour le voir. Le motif voyage désormais avec
      le verdict.
    ⑨ CE QUI CLOCHE — Le motif est montré, il n'est pas jugé : une exception compte encore comme un rouge (BACKLOG,
      superviseur R-759 du 01-11-2026, d). « T1 » ne prend pas « T10 » : la clé doit finir le mot. · La même
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
    """Charge le contrôle des causes — le vrai fichier, ou une copie sabotée posée à côté des modules qu'il lit."""
    dossier = PROGRAMMES
    if sabotage is not None:
        dossier = tempfile.mkdtemp()
        for nom in MODULES:
            shutil.copy(os.path.join(PROGRAMMES, nom + ".py"), dossier)
        texte = open(CONTROLE, encoding="utf-8").read()
        for cible, remplace in sabotage:
            texte = texte.replace(cible, remplace)
        open(os.path.join(dossier, os.path.basename(CONTROLE)), "w", encoding="utf-8").write(texte)
    for nom in MODULES + ("CONTROLER_LES_CAUSES_DES_TROUS",):
        sys.modules.pop(nom, None)
    sys.path.insert(0, dossier)
    try:
        sp = importlib.util.spec_from_file_location("CONTROLER_LES_CAUSES_DES_TROUS",
                                                    os.path.join(dossier, os.path.basename(CONTROLE)))
        m = importlib.util.module_from_spec(sp)
        sys.modules["CONTROLER_LES_CAUSES_DES_TROUS"] = m
        sp.loader.exec_module(m)
    finally:
        sys.path.remove(dossier)
    return m


def racine_jetable(C, table=None):
    """Une racine jetable : le dépôt en liens durs (sans .git), la table des causes recréée (absente, ou `table`)."""
    r = os.path.join(tempfile.mkdtemp(), "depot")
    shutil.copytree(RACINE, r, copy_function=os.link, ignore=shutil.ignore_patterns(".git"))
    if table is not None:
        os.remove(os.path.join(r, C.CAUSES))         # recréée, jamais écrite par-dessus : le dépôt reste intact
    if table not in (None, "absente"):
        os.makedirs(os.path.join(r, os.path.dirname(C.CAUSES)), exist_ok=True)
        open(os.path.join(r, C.CAUSES), "w", encoding="utf-8").write(table)
    return r


def epreuves(C, D):
    """Joue chaque épreuve sur le contrôle chargé ; rend leurs verdicts.

    ① RÔLE — Le cœur du jeu : T1 à T17, sur le contrôle vrai (Z0) ou sabotée (`charger`).
    ② CONTEXTE D'APPEL — `main`, une fois sur le vrai contrôle, puis une fois par sabotage demandé.
    ③ ENTRÉE — `C` : le module du contrôle · `D` : (séries, calendrier, lignes de cause), lues par `donnees`.
    ④ CONDITIONS D'ENTRÉE — `donnees` a posé `PASSAGES` (les passages du vrai contrôle) ; LVMH a une barre le
      15-06-2012 ; la table a une ligne « source perdue ».
    ⑤ SORTIE — UNE valeur : clé de l'épreuve → vrai (verte) ou faux (rouge, ou plantée).
      [rend: 1]
    ⑥ TRAITEMENT — Chaque épreuve passe par `tenter` : une exception est imprimée et compte pour un rouge.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 : chaque garde a son épreuve, et chaque épreuve ses dents (les sabotages de `SABOTAGES`).
    ⑨ CE QUI CLOCHE — Une épreuve qui plante compte comme un rouge : un sabotage peut « mordre » par un plantage
      (BACKLOG, superviseur R-759 du 01-11-2026, d) ; `motifs` le montre sans le juger. · T2 à T7, T10, T12 à T14, T16
      et T17 jouent la FONCTION ; seuls T1, T8, T9, T11 et T15 jouent le programme entier.
    ⑩ EFFET — Imprime une ligne par épreuve ; crée et supprime des racines jetables (T8, T9, T11, T15) ; ôte puis
      remet une ligne des séries en mémoire (`jouer`).
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    series, cal, causes = D
    res = {}

    def tenter(cle, f):
        try:
            res[cle] = bool(f())
        except Exception as e:
            print(f"      {cle} : {type(e).__name__} : {e}")
            res[cle] = False

    def jouer(cle, causes_, attendu, retirer=None, passages=None):
        """Joue `cas_des_causes` sur une table donnée ; rend le verdict de `attendu`.

        ① RÔLE — Jouer la fonction du contrôle sur des données en mémoire, une ligne de série ôtée au besoin.
        ② CONTEXTE D'APPEL — Les épreuves de fonction (T2 à T7, T10, T12 à T14, T16, T17).
        ③ ENTRÉE — `cle` : le nom de l'épreuve · `causes_` : les lignes de cause · `attendu` : prédicat sur les cas ·
          `retirer` : (valeur, date) à ôter le temps de l'épreuve, ou rien · `passages` : les passages à passer, ou
          rien pour les vrais (`PASSAGES`) — ajouté au tour 3 pour T17.
        ④ CONDITIONS D'ENTRÉE — La ligne à retirer existe.
        ⑤ SORTIE — UNE valeur : ce que rend `attendu(cas)`.
          [rend: 1]
        ⑥ TRAITEMENT — Ôter, jouer, remettre (même sur exception), imprimer les trois premiers cas, juger.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Les séries ne sont jamais copiées (39 valeurs, 20 ans) : la ligne est remise dans `finally`.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie puis restaure `series` ; imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        garde = None
        if retirer:
            v, d = retirer
            garde = series[v].pop(d)
        try:
            cas = C.cas_des_causes(series, cal, causes_, PASSAGES if passages is None else passages)
        finally:
            if retirer:
                series[retirer[0]][retirer[1]] = garde
        print(f"      {cle} : {len(cas)} cas {cas[:3]}")
        return attendu(cas)

    def code_de_main(racine):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = C.main([racine])
        return code, sortie.getvalue()

    def t1():
        """Le programme entier sur les vraies données ; vert au code 0.

        ① RÔLE — Dire que le vrai contrôle accepte la vraie table.
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — La racine porte la table et le fichier réparé.
        ⑤ SORTIE — UNE valeur : vrai si le code est 0.
          [rend: 1]
        ⑥ TRAITEMENT — `main` ; imprimer la première ligne, et, si le code n'est pas 0, les deux premiers cas et le
          verdict (tour 3 : le motif d'un rouge de T1 se lit, « non vérifiable » sous C14 et C15).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — T1 est l'épreuve qui voit un `main` qui ne passe plus sa donnée, avec la fermeture a′.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Imprime.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        code, out = code_de_main(RACINE)
        lignes = out.splitlines()
        motif = "" if code == 0 else " · " + " · ".join([l.strip()[:200] for l in lignes if l.startswith("   ")][:2]
                                                       + [l for l in lignes if l.startswith("VERDICT")])
        print(f"      T1 : code {code}, {lignes[0][:160] if lignes else ''}{motif}")
        return code == 0
    tenter("T1", t1)
    perdue = next(r for r in causes if r["cause"] == C.SOURCE_PERDUE)
    tenter("T2", lambda: jouer("T2", causes, lambda c: c == ["LVMH 2012-06-15 : séance sans cours, SANS CAUSE"],
                               retirer=("LVMH", "2012-06-15")))
    fabriquee = dict(causes[0], valeur="LVMH", debut="2012-06-15", fin="2012-06-15", cause="suspension",
                     preuve="FABRIQUÉE pour l'épreuve", n=9999)
    tenter("T3", lambda: jouer("T3", causes + [fabriquee],
                               lambda c: len(c) == 1 and "couvre 1 séance(s) où la valeur a un cours" in c[0]))
    tenter("T4", lambda: jouer("T4", [dict(perdue, cause="INCONNUE")] + [r for r in causes if r is not perdue],
                               lambda c: any("liste fermée" in x for x in c) and any("SANS CAUSE" in x for x in c)))
    tenter("T5", lambda: jouer("T5", [dict(perdue, preuve=" ")] + [r for r in causes if r is not perdue],
                               lambda c: any("sans preuve" in x for x in c)))
    tenter("T6", lambda: jouer("T6", [dict(perdue, sources_cherchees="")] + [r for r in causes if r is not perdue],
                               lambda c: any("sans les sources cherchées" in x for x in c)))
    tenter("T7", lambda: jouer("T7", causes + [dict(perdue, n=9998)], lambda c: any("DEUX CAUSES" in x for x in c)))

    def t8_t9(cle, table):
        def f():
            r = racine_jetable(C, table)
            try:
                code, out = code_de_main(r)
            finally:
                shutil.rmtree(r, ignore_errors=True)
            print(f"      {cle} : code {code}, {out.strip()[:160]}")
            return code == 2
        tenter(cle, f)
    t8_t9("T8", "absente")
    t8_t9("T9", "valeur,debut,fin,cause,preuve\nLVMH,2012-06-15,2012-06-15,hors indice,x\n")
    def t11():
        """Le programme entier, la table privée de sa ligne de Schneider du 07-06-2001 : code 1, et la séance nommée."""
        texte = open(os.path.join(RACINE, C.CAUSES), encoding="utf-8").read().splitlines(keepends=True)
        reste = [x for x in texte if not x.startswith("SCHNEIDER ELECTRIC,2001-06-07,")]
        r = racine_jetable(C, "".join(reste))
        try:
            code, out = code_de_main(r)
        finally:
            shutil.rmtree(r, ignore_errors=True)
        print(f"      T11 : code {code}, {len(texte) - len(reste)} ligne ôtée")
        return code == 1 and len(texte) - len(reste) == 1 and "SCHNEIDER ELECTRIC 2001-06-07 : séance sans cours, SANS CAUSE" in out
    tenter("T11", t11)
    # T12 à T14 : une cause que nos fichiers contredisent (relecture du lot, D3), sur la vraie ligne LVMH du 15-06-2012
    lv = dict(causes[0], valeur="LVMH", debut="2012-06-15", fin="2012-06-15", preuve="x", sources_cherchees="", n=9997)
    for cle, cause, mot in (("T12", "pas encore cotée", "« pas encore cotée » contredit"),
                            ("T13", "hors indice", "« hors indice » contredit"),
                            ("T14", "plus cotée", "« plus cotée » contredit")):
        tenter(cle, lambda cause=cause, mot=mot, cle=cle: jouer(cle, causes + [dict(lv, cause=cause)],
                                                                 lambda c: any(mot in x for x in c),
                                                                 retirer=("LVMH", "2012-06-15")))
    tenter("T10", lambda: jouer("T10", [dict(perdue, debut=perdue["fin"], fin=perdue["debut"])]
                                + [r for r in causes if r is not perdue]
                                if perdue["debut"] != perdue["fin"] else
                                [dict(perdue, debut="2099-01-01")] + [r for r in causes if r is not perdue],
                                lambda c: any("dates illisibles ou dans le désordre" in x for x in c)))

    def t15():
        """Le programme entier refuse, avec son motif, une cause « hors indice » que la table des passages contredit.

        ① RÔLE — Faire au niveau du programme, pour le refus « contredit », ce que T11 fait pour « SANS CAUSE ».
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — La vraie table se termine par une fin de ligne ; LVMH est au CAC 40 le 15-06-2012.
        ⑤ SORTIE — UNE valeur : vrai si `main` rend 1 ET nomme la ligne fabriquée avec « « hors indice » contredit ».
          [rend: 1]
        ⑥ TRAITEMENT — Une ligne « hors indice » LVMH 15-06-2012 ajoutée à la vraie table, écrite par `csv` ; une
          racine jetable où SEULE la table est recréée (`racine_jetable`) ; `main` ; chercher la ligne du cas.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture du tour 2, N1 : sous X6 (`main` ne passe plus les passages), les 14 épreuves restaient
          vertes et le vrai programme acceptait cette cause avec le code 0. Le MOTIF est exigé : sans lui, la même
          ligne sort aussi « couvre 1 séance(s) où la valeur a un cours », le code vaut 1, et l'épreuve resterait
          verte (superviseur R-759 du 01-11-2026, a, piège 2). La séance n'est pas ôtée du fichier de cours : la
          racine jetable est en LIENS DURS, et réécrire le fichier de cours y écrirait dans le dépôt (piège 1) ; la
          contradiction est jugée avant la couverture, elle n'en a pas besoin.
        ⑨ CE QUI CLOCHE — Le numéro de ligne attendu suppose que la table n'a pas de champ sur deux lignes : sinon le
          numéro diffère, et l'épreuve rougit (du côté prudent).
        ⑩ EFFET — Crée puis supprime une racine jetable ; imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        texte = open(os.path.join(RACINE, C.CAUSES), encoding="utf-8").read()
        assert texte.endswith("\n")
        neuve = io.StringIO()
        csv.writer(neuve, lineterminator="\n").writerow(
            ["LVMH", "2012-06-15", "2012-06-15", C.HORS_INDICE, "FABRIQUÉE pour l'épreuve T15", ""])
        n = len(causes) + 2                                 # en-tête en ligne 1, comme `lire_les_causes`
        r = racine_jetable(C, texte + neuve.getvalue())
        try:
            code, out = code_de_main(r)
        finally:
            shutil.rmtree(r, ignore_errors=True)
        ici = f"ligne {n} (LVMH 2012-06-15 → 2012-06-15, « hors indice ») : "
        du_cas = [l.strip() for l in out.splitlines() if ici in l]
        verdict = [l for l in out.splitlines() if l.startswith("VERDICT")]
        print(f"      T15 : code {code}, la ligne fabriquée : {[x[:220] for x in du_cas]} · {verdict}")
        return code == 1 and any(ici + "« hors indice » contredit" in x for x in du_cas)
    tenter("T15", t15)

    def t16():
        """La borne de fin d'une période dans le CAC 40 est incluse : un « hors indice » ce jour-là est contredit.

        ① RÔLE — Donner des dents au `<=` de la fin de période (le X4 de la relecture du tour 2, sabotage C13).
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — La table des passages a au moins une période fermée pour une valeur du fichier ;
          sinon `next` lève, et l'épreuve rougit.
        ⑤ SORTIE — UNE valeur : vrai si la ligne fabriquée sort « « hors indice » contredit ».
          [rend: 1]
        ⑥ TRAITEMENT — La période choisie PAR PROPRIÉTÉ : la première valeur, dans l'ordre, qui a une période avec une
          fin, et sa première telle période ; une ligne « hors indice » du jour de la fin au jour de la fin ; jouer.
        ⑦ UNITÉ — Des dates AAAA-MM-JJ.
        ⑧ POURQUOI — La table des passages a `premiere_seance` et `derniere_seance` : la fin est un jour DANS l'indice.
          Avec `<`, le contrôle accepterait une cause fausse : c'est le côté dangereux (superviseur R-759 du 01-11-2026,
          c). Aujourd'hui : ACCOR, du 03-01-2000 au 18-09-2020.
        ⑨ CE QUI CLOCHE — Le début de période n'a pas son épreuve de borne (un `<` à la place du `<=` de `x <= fin`).
        ⑩ EFFET — Imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        v, a, b = next((v, a, b) for v in sorted(PASSAGES) if v in series for a, b in PASSAGES[v] if b is not None)
        print(f"      T16 : période choisie {v} {a} → {b}, barre ce jour {b in series[v]}")
        ligne = dict(causes[0], valeur=v, debut=b, fin=b, cause=C.HORS_INDICE, preuve="FABRIQUÉE pour l'épreuve T16",
                     sources_cherchees="", n=9996)
        return jouer("T16", causes + [ligne],
                     lambda c: any(x.startswith("ligne 9996 ") and "« hors indice » contredit" in x for x in c))
    tenter("T16", t16)

    def t17():
        """Une valeur sans aucune période connue rend « hors indice » non vérifiable : refusé, jamais accepté.

        ① RÔLE — Donner des dents à la fermeture a′ (sabotage C16).
        ② CONTEXTE D'APPEL — `epreuves`, par `tenter`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — LVMH a une barre le 15-06-2012 (ôtée le temps de l'épreuve).
        ⑤ SORTIE — UNE valeur : vrai si la ligne fabriquée sort « « hors indice » non vérifiable ».
          [rend: 1]
        ⑥ TRAITEMENT — Les vrais passages, LVMH ôtée ; la séance du 15-06-2012 ôtée ; une ligne « hors indice » sur ce
          trou ; jouer.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Sans la fermeture, la ligne couvrirait le trou et le contrôle ne trouverait AUCUN cas : une cause
          acceptée sur une donnée absente (superviseur R-759 du 01-11-2026, a′).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Imprime une ligne.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
        """
        sans = {k: x for k, x in PASSAGES.items() if k != "LVMH"}
        ligne = dict(causes[0], valeur="LVMH", debut="2012-06-15", fin="2012-06-15", cause=C.HORS_INDICE,
                     preuve="FABRIQUÉE pour l'épreuve T17", sources_cherchees="", n=9995)
        return jouer("T17", causes + [ligne],
                     lambda c: any(x.startswith("ligne 9995 ") and "« hors indice » non vérifiable" in x for x in c),
                     retirer=("LVMH", "2012-06-15"), passages=sans)
    tenter("T17", t17)
    return res


def donnees(C):
    global PASSAGES
    PASSAGES = C.passages_par_valeur(RACINE, C.K.FICHIER)
    series, defauts, _ = C.K.lire_cours(os.path.join(RACINE, C.K.FICHIER))
    assert not defauts
    cal = sorted(C.K.calendrier(series, C.K.CAL.lire_les_seances(RACINE)))
    return series, cal, C.lire_les_causes(os.path.join(RACINE, C.CAUSES))


def main():
    """Joue les épreuves sur le vrai contrôle, puis sous chaque sabotage demandé ; rend le code de sortie.

    ① RÔLE — Porter le jeu : Z0, puis les sabotages.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `sys.argv` : la racine, et `--saboter` ou `--saboter=C1,…`.
    ④ CONDITIONS D'ENTRÉE — La racine est un dépôt complet (fichier réparé, table, calendrier, lecteur unique).
    ⑤ SORTIE — UNE valeur : 0 (tout vert, et chaque sabotage demandé mord) · 1 (une épreuve rouge, ou un sabotage
      qui ne mord pas) · 2 (une cible de sabotage absente ou en double).
      [rend: 1]
    ⑥ TRAITEMENT — Charger, lire, jouer ; pour chaque sabotage : vérifier que sa cible est unique, charger la copie
      sabotée, rejouer en gardant la sortie, imprimer « mord » ou « NE MORD PAS », puis (tour 3) le motif de chaque
      épreuve tombée (`motifs`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 ; le motif imprimé, parce qu'un « mord » sans motif ne dit pas si c'est un refus ou un plantage
      (relecture du tour 2, Q2).
    ⑨ CE QUI CLOCHE — Un plantage compte encore comme une morsure (BACKLOG).
    ⑩ EFFET — Imprime ; crée des dossiers jetables sous le dossier d'essai.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    C = charger()
    D = donnees(C)
    res = epreuves(C, D)
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programme tel quel : {len(res) - len(rouges)}/{len(res)} épreuves vertes"
          + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        source = open(CONTROLE, encoding="utf-8").read()
        for k, paires in SABOTAGES.items():
            if choix and k not in choix[0]:
                continue
            for cible, _ in paires:
                if source.count(cible) != 1:
                    print(f"{k} NE S'APPLIQUE PLUS : texte cible trouvé {source.count(cible)} fois")
                    return 2
            C2 = charger(paires)
            garde = io.StringIO()
            with contextlib.redirect_stdout(garde):
                r = epreuves(C2, (D[0], D[1], C2.lire_les_causes(os.path.join(RACINE, C2.CAUSES))))
            tombees = [e for e, v in r.items() if not v]
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}")
            for l in motifs(garde.getvalue(), tombees):
                print(l)
            if not tombees:
                code = 1
    return code


if __name__ == "__main__":
    _DOSSIER_D_ESSAI = tempfile.mkdtemp(prefix="epreuves_causes_")
    tempfile.tempdir = os.environ["TMPDIR"] = _DOSSIER_D_ESSAI
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(_DOSSIER_D_ESSAI, ignore_errors=True)
