#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_LOT_0 — Lun 09-11-2026 (Paris)
Rôle : prouver le contrat de l'horizon « aucune » et les lecteurs de la fiche déclarés au lot 0 (interfaces communes des
agents A, B, C, D du plan V7), et rougir si on les défait.

À QUOI ÇA SERT. Mercredi, quatre agents travaillent en parallèle. Le lot 0 fixe UNE fois : ① comment s'écrit et se lit
une stratégie sans durée maximale (programmes/COMMUN.py, fin du fichier) ; ② ce que reçoivent les fonctions du jugement
(programmes/MODULE_JUGEMENT.py, textes de coupure_70_30, fenetres_glissantes, etalon_hasard) ; ③ les colonnes de la fiche
lues par le soir et leurs lecteurs (programmes/CONTRATS_DES_FICHIERS.py, LECTEURS_DE_LA_FICHE_POUR_LE_SOIR).

LES ÉPREUVES :
E1 `lire_horizon` REFUSE « aucune » (None) sous trois écritures : ses dix appels d'aujourd'hui ne changent pas d'avis.
E2 `lire_horizon_ou_aucune` rend HORIZON_AUCUNE pour ces trois écritures, 20 pour « 20j », None pour « aucun », « none »,
   « 0 », « », « ∞ », None, « Intraday ».
E3 HORIZON_AUCUNE refuse int, float, <, + par une TypeError qui nomme le lot 0 ; il vaut True ; str() rend « aucune ».
E4 le jugement : coupure_70_30 et fenetres_glissantes TOMBENT (TypeError du lot 0) avec horizon=HORIZON_AUCUNE et sans
   embargo ; avec un embargo explicite, elles ne lisent pas l'horizon et rendent un résultat.
E5 VRAIES LIGNES (R-732) de donnees/cac40_strategies.csv : C1-002 « 5j » → 5 et C2-001 « Intraday » → None, par les deux
   lecteurs ; et sur TOUTES les lignes réelles, les deux lecteurs sont d'accord (aucune ne porte « aucune » au 09-11).
E6 chaque colonne de LECTEURS_DE_LA_FICHE_POUR_LE_SOIR est dans le contrat STRATEGIE ET dans l'en-tête réel du registre,
   et chaque lecteur « programme:fonction » est une fonction définie au niveau du module de ce programme.

LES SABOTAGES (--saboter), chacun sur une copie de programmes/ dans un dossier temporaire, avec les épreuves qui DOIVENT
rougir : S1 le mot devient « aucun » (E2) · S2 la sentinelle vaut False en logique, `int(h or 0)` donnerait 21 séances
en silence (E3, E4) · S3 la sentinelle ne refuse plus int/float (E3, E4) · S4 `lire_horizon_ou_aucune` rend None pour
« aucune » (E2) · S5 un lecteur de la fiche renommé vers une fonction absente (E6) · S6 `lire_horizon` accepte « aucune »
(E1 ; E5 ne le voit pas : aucune ligne réelle ne porte « aucune » au 09-11-2026 — constaté au premier passage).

USAGE : python3 tests/EPREUVES_DU_LOT_0_Lun_09-11-2026.py [--saboter]   (depuis n'importe où ; code de sortie 0 = vert)
"""
import csv
import ast
import os
import shutil
import subprocess
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def epreuves(dossier_programmes):
    """Joue E1 à E6 sur les programmes d'un dossier ; rend le dictionnaire {épreuve: vert ?}.

    ① RÔLE — Les six épreuves du lot 0, une fois.
    ② CONTEXTE D'APPEL — `main`, une fois en mode normal ; en mode --saboter, une
      fois par sabotage, dans un sous-processus (`--dossier=`).
    ③ ENTRÉE — `dossier_programmes` : chemin d'un dossier qui contient COMMUN,
      MODULE_JUGEMENT, CONTRATS_DES_FICHIERS, JUGE_DES_STRATEGIES et TENIR_LES_POSITIONS.
    ④ CONDITIONS D'ENTRÉE — Le registre réel est lu à RACINE/donnees/cac40_strategies.csv.
    ⑤ SORTIE — UNE valeur : {« E1 »…« E6 » : booléen}, et une ligne imprimée par épreuve.
      [rend: 1]
    ⑥ TRAITEMENT — Importer les trois modules du dossier, jouer chaque épreuve
      dans un try (une exception = rouge, son message imprimé).
    ⑦ UNITÉ — Horizon en SÉANCES.
    ⑧ POURQUOI — R-731 : tout code écrit passe des épreuves qui mordent.
    ⑨ CE QUI CLOCHE — E6 vérifie que la fonction existe, pas ce qu'elle rend ;
      E4 n'appelle pas etalon_hasard (son corps ne lit pas l'horizon).
    ⑩ EFFET — Importe des modules (sys.path modifié) ; n'écrit aucun fichier.
    ⑪ TERMINAISON — Rend toujours la main ; les fonctions appelées sont des
      lectures en mémoire, sans réseau.
      [sort: non]
    """
    sys.path.insert(0, dossier_programmes)
    import COMMUN as C
    import MODULE_JUGEMENT as MJ
    import CONTRATS_DES_FICHIERS as K
    H = C.HORIZON_AUCUNE
    res = {}

    def jouer(nom, f):
        try:
            ok, detail = f()
        except Exception as e:  # une épreuve qui plante est rouge
            ok, detail = False, "%s: %s" % (type(e).__name__, str(e)[:90])
        res[nom] = ok
        print("  %s %s — %s" % ("VERT " if ok else "ROUGE", nom, detail))

    ecritures = ("aucune", "AUCUNE", "  Aucune ")

    jouer("E1", lambda: (all(C.lire_horizon(x) is None for x in ecritures),
                         [C.lire_horizon(x) for x in ecritures]))

    def e2():
        a = [C.lire_horizon_ou_aucune(x) is H for x in ecritures]
        b = C.lire_horizon_ou_aucune("20j") == 20
        c = [C.lire_horizon_ou_aucune(x) for x in ("aucun", "none", "0", "", "∞", None, "Intraday")]
        return all(a) and b and all(v is None for v in c), "aucune %s · 20j %s · autres %s" % (a, b, c)
    jouer("E2", e2)

    def e3():
        refus = []
        for nom, op in (("int", lambda: int(H)), ("float", lambda: float(H)),
                        ("<", lambda: H < 5), ("+", lambda: H + 1), ("or 0", lambda: int(H or 0))):
            try:
                op()
                refus.append((nom, "PASSE"))
            except TypeError as e:
                refus.append((nom, "lot 0" in str(e)))
        ok = all(r is True for _, r in refus) and bool(H) is True and str(H) == "aucune"
        return ok, "refus %s · bool %s · str %r" % (refus, bool(H), str(H))
    jouer("E3", e3)

    def e4():
        cal = ["2024-01-%02d" % d for d in range(2, 31)]
        ops = [{"date_signal": "1999-01-04"}]
        tombe = []
        for f, kw in ((MJ.coupure_70_30, "embargo_seances"), (MJ.fenetres_glissantes, "embargo")):
            try:
                f(ops, cal, horizon=H)
                tombe.append("PASSE")
            except TypeError as e:
                tombe.append("lot 0" in str(e))
        explicite = [isinstance(MJ.coupure_70_30(ops, cal, embargo_seances=40, horizon=H), dict),
                     isinstance(MJ.fenetres_glissantes(ops, cal, embargo=40, horizon=H), dict)]
        return all(t is True for t in tombe) and all(explicite), "sans embargo %s · avec embargo %s" % (tombe, explicite)
    jouer("E4", e4)

    def e5():
        with open(os.path.join(RACINE, "donnees", "cac40_strategies.csv"), encoding="utf-8") as fh:
            lignes = list(csv.DictReader(fh))
        par_id = {l["id"]: l for l in lignes}
        cas = [(C.lire_horizon(par_id["C1-002"]["horizon"]), C.lire_horizon_ou_aucune(par_id["C1-002"]["horizon"])),
               (C.lire_horizon(par_id["C2-001"]["horizon"]), C.lire_horizon_ou_aucune(par_id["C2-001"]["horizon"]))]
        desaccords = [l["id"] for l in lignes
                      if C.lire_horizon(l.get("horizon", "")) != C.lire_horizon_ou_aucune(l.get("horizon", ""))]
        ok = cas == [(5, 5), (None, None)] and not desaccords and len(lignes) > 0
        return ok, "C1-002/C2-001 %s · %d lignes, désaccords %s" % (cas, len(lignes), desaccords[:5])
    jouer("E5", e5)

    def e6():
        with open(os.path.join(RACINE, "donnees", "cac40_strategies.csv"), encoding="utf-8") as fh:
            entete = next(csv.reader(fh))
        manques = []
        for col, lecteur in K.LECTEURS_DE_LA_FICHE_POUR_LE_SOIR.items():
            if col not in K.STRATEGIE or col not in entete:
                manques.append("colonne " + col)
            prog, fonc = lecteur.split(":")
            with open(os.path.join(dossier_programmes, prog + ".py"), encoding="utf-8") as fh:
                defs = {n.name for n in ast.parse(fh.read()).body if isinstance(n, ast.FunctionDef)}
            if fonc not in defs:
                manques.append(lecteur)
        return not manques and len(K.LECTEURS_DE_LA_FICHE_POUR_LE_SOIR) > 0, "manques %s" % sorted(set(manques))
    jouer("E6", e6)
    return res


# Chaque sabotage : (fichier, texte exact à remplacer, remplacement, épreuves qui doivent rougir).
SABOTAGES = {
    "S1_mot_aucun": ("COMMUN.py", 'MOT_DE_L_HORIZON_AUCUNE = "aucune"', 'MOT_DE_L_HORIZON_AUCUNE = "aucun"', {"E2"}),
    "S2_sentinelle_fausse": ("COMMUN.py", "    __slots__ = ()\n",
                             "    __slots__ = ()\n    __bool__ = lambda self: False\n", {"E3", "E4"}),
    "S3_int_admis": ("COMMUN.py", "    __int__ = __index__ = __float__ = _refuser_le_calcul\n", "", {"E3", "E4"}),
    "S4_aucune_illisible": ("COMMUN.py", "        return HORIZON_AUCUNE\n    return lire_horizon(x)",
                            "        return None\n    return lire_horizon(x)", {"E2"}),
    "S5_lecteur_absent": ("CONTRATS_DES_FICHIERS.py", '"JUGE_DES_STRATEGIES:mnemoniques_de_l_univers"',
                          '"JUGE_DES_STRATEGIES:univers_qui_n_existe_pas"', {"E6"}),
    "S6_ancien_lecteur_accepte": ("COMMUN.py", '    h = str(x).strip().lower().rstrip("j")\n',
                                  '    h = str(x).strip().lower().rstrip("j")\n'
                                  '    if h == "aucune":\n        return HORIZON_AUCUNE\n', {"E1"}),
}


def saboter():
    """Joue chaque sabotage sur une copie et vérifie que les épreuves attendues rougissent ; rend 0 ou 1.

    ① RÔLE — Prouver que les épreuves mordent (une épreuve verte quand on retire
      ce qu'elle teste est une décoration).
    ② CONTEXTE D'APPEL — `main`, avec --saboter.
    ③ ENTRÉE — Aucune (lit SABOTAGES et les programmes de RACINE).
    ④ CONDITIONS D'ENTRÉE — Chaque texte à remplacer existe UNE fois dans son
      fichier ; sinon le sabotage est déclaré « NON APPLIQUÉ », rouge.
    ⑤ SORTIE — UNE valeur : 0 si chaque sabotage fait rougir AU MOINS ses
      épreuves attendues, 1 sinon.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque sabotage : copier programmes/ dans un dossier
      temporaire, remplacer, relancer ce fichier en sous-processus sur la copie,
      lire les épreuves rouges dans sa sortie.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 et le §7 des instructions : un jeu d'épreuves se sabote
      contre sa propre correction.
    ⑨ CE QUI CLOCHE — Copie tout programmes/ à chaque sabotage (quelques Mo) ;
      le dossier temporaire est supprimé à la fin de chaque tour.
    ⑩ EFFET — Écrit puis supprime des dossiers temporaires ; ne touche pas au dépôt.
    ⑪ TERMINAISON — Un de ses appels peut ne pas revenir : le sous-processus ;
      il est borné à 300 s (timeout), au-delà le sabotage est rouge.
      [sort: non]
    """
    echecs = 0
    for nom, (fichier, avant, apres, attendues) in SABOTAGES.items():
        tmp = tempfile.mkdtemp(prefix="lot0_sab_")
        try:
            copie = os.path.join(tmp, "programmes")
            shutil.copytree(os.path.join(RACINE, "programmes"), copie,
                            ignore=shutil.ignore_patterns("__pycache__"))
            chemin = os.path.join(copie, fichier)
            with open(chemin, encoding="utf-8") as fh:
                texte = fh.read()
            if texte.count(avant) != 1:
                print("  ROUGE %s — NON APPLIQUÉ (%d occurrences)" % (nom, texte.count(avant)))
                echecs += 1
                continue
            with open(chemin, "w", encoding="utf-8") as fh:
                fh.write(texte.replace(avant, apres))
            try:
                p = subprocess.run([sys.executable, "-E", os.path.abspath(__file__), "--dossier=" + copie],
                                   capture_output=True, text=True, timeout=300)
                sortie = p.stdout
            except subprocess.TimeoutExpired:
                sortie = ""
            rouges = {l.split()[1] for l in sortie.splitlines() if l.strip().startswith("ROUGE")}
            ok = attendues <= rouges
            echecs += 0 if ok else 1
            print("  %s %s — attendues %s, rouges %s" % ("MORD " if ok else "ROUGE", nom, sorted(attendues),
                                                         sorted(rouges)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return 1 if echecs else 0


def main():
    """Lance les épreuves (ou les sabotages) et sort avec 0 si tout est vert.

    ① RÔLE — Point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv : rien, « --saboter », ou « --dossier=<programmes> ».
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — AUCUNE valeur : sort du processus, code 0 (vert) ou 1.
      [rend: 0]
    ⑥ TRAITEMENT — --saboter → `saboter` ; sinon `epreuves` sur le dossier donné
      ou sur RACINE/programmes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Imprime ; aucun fichier écrit hors des dossiers temporaires.
    ⑪ TERMINAISON — Sort toujours ; voir `saboter` pour le sous-processus borné.
      [sort: oui]
    """
    args = sys.argv[1:]
    if "--saboter" in args:
        sys.exit(saboter())
    dossier = next((a.split("=", 1)[1] for a in args if a.startswith("--dossier=")),
                   os.path.join(RACINE, "programmes"))
    res = epreuves(dossier)
    sys.exit(0 if res and all(res.values()) else 1)


if __name__ == "__main__":
    main()
