#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVE_DE_L_ANCRE_DE_C5 — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Une épreuve COURTE qui rougit, avec un message clair, dès que le code du module de C5 (ou un réglage
de la fiche C5E10-QA-V1, l'univers, la période) change sans que la valeur figée de
CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE suive. Fait qui l'a fait naître : le 20-11-2026, le merge d2ba76264
(A-928 D2) a changé `_c5e10_sortie` ; l'empreinte des réglages de C5 est passée de 813e12bed9ff8410 à
2373a2d54f9402b3, et seul l'essai de moulinette (MoulinetteEssai, plusieurs minutes) l'a dit, en rendant 2 sans dire
pourquoi. L'épreuve E-ancre, qui le voit en quelques secondes, vivait dans
tests/EPREUVES_DE_L_ESSAI_SANS_REGARD_Lun_16-11-2026.py, épreuve longue qui n'est pas au lancement de GitHub. Celle-ci
APPELLE cette E-ancre (`cas_e_ancre`, la seule définition, jamais recopiée : deux implémentations d'une même chose
divergent toujours, R-708) et n'ajoute que le message et les sabotages.

① RÔLE — Jouer E-ancre sur la racine reçue ; avec --saboter, prouver sur une copie jetable qu'elle rougit quand le code
  du module C5 change (S1) ou quand la valeur figée revient à l'ancienne (S3, le cas du 20-11-2026), et qu'elle reste
  verte quand seul un commentaire du module change (S2 : elle ne sur-détecte pas).
② CONTEXTE D'APPEL — Le lancement des épreuves de GitHub (tests/LANCEMENT_DES_EPREUVES.json, « AncreC5 ») ; à la main.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ou d'une copie (lue, jamais écrite) ; « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — Celles d'E-ancre : la racine porte programmes/ (juge, contrat, PREPARER, module C5), emp.py,
  le registre avec C5E10-QA-V1, et le fichier des vingt ans (PREPARER n'en lit que la première et la dernière date).
⑤ SORTIE — Le code de sortie : 0 si E-ancre est verte (et, avec --saboter, si S1 et S3 rougissent et S2 reste vert) ;
  1 si E-ancre rougit ou si un sabotage ne mord pas ; 2 si l'épreuve n'a pas pu tourner (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① E-ancre sur la racine · ② si rouge : message clair, code 1 · ③ sous --saboter : une copie jetable
  (`copie_jetable` de l'épreuve longue), chaque sabotage écrit, E-ancre rejouée, le fichier remis à l'octet.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du Sam 21-11-2026 à 00h49 (A-957, « 1 ») : refiger la valeur après preuve que C5
  rend les mêmes sorties, et une épreuve courte pour que le cas ne se reproduise pas en silence.
⑨ CE QUI CLOCHE — ① E-ancre ne voit que C5E10-QA-V1 : une autre fiche figée, s'il en venait une, ne serait pas vue.
  ② Le code que le module C5 CHARGE par chemin n'est pas dans l'empreinte (limite déjà écrite au juge, N7).
⑩ EFFET — Sous --saboter, crée puis efface un dossier temporaire ; n'écrit rien dans la racine reçue.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Non : chaque E-ancre est bornée au
  délai de l'épreuve longue (DELAI).
  [sort: oui]
"""
import ast
import importlib.util
import os
import shutil
import sys

sys.dont_write_bytecode = True

ICI = os.path.dirname(os.path.abspath(__file__))
LONGUE = os.path.join(ICI, "EPREUVES_DE_L_ESSAI_SANS_REGARD_Lun_16-11-2026.py")
CONTRATS = os.path.join("programmes", "CONTRATS_DES_FICHIERS.py")
# L'ANCIENNE VALEUR, celle que le contrat portait le 20-11-2026 quand le code de C5 avait déjà changé : le cas réel (R-732).
ANCIENNE = "813e12bed9ff8410"


def charger_la_longue():
    """Charge l'épreuve longue comme un module. ① RÔLE — Atteindre `cas_e_ancre`, `copie_jetable` et `MODULE_C5` sans
    les recopier. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — LONGUE existe. ⑤ SORTIE — UNE
    valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib depuis le chemin. ⑦ UNITÉ — — ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le haut du fichier long (des définitions seulement). ⑪ TERMINAISON — Rend la
    main ; lève ce que lève l'import. [sort: non]"""
    spec = importlib.util.spec_from_file_location("EPREUVES_DE_L_ESSAI_SANS_REGARD", LONGUE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def valeur_figee(texte):
    """Lit la valeur figée de C5E10-QA-V1 dans l'arbre du texte du contrat. ① RÔLE — Viser la valeur sans l'épeler.
    ② CONTEXTE D'APPEL — `remettre_l_ancienne`. ③ ENTRÉE — le texte de CONTRATS. ④ CONDITIONS D'ENTRÉE — il affecte
    FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE en littéral. ⑤ SORTIE — UNE valeur : la chaîne, ou None. [rend: 1]
    ⑥ TRAITEMENT — ast.literal_eval de l'affectation. ⑦ UNITÉ — — ⑧ POURQUOI — même lecture que S11 de l'épreuve longue.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    for n in ast.parse(texte).body:
        if (isinstance(n, ast.Assign) and any(isinstance(c, ast.Name) and c.id == "FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE"
                                              for c in n.targets)):
            return ast.literal_eval(n.value).get("C5E10-QA-V1", (None, None))[1]
    return None


def changer_le_code(texte):
    """S1 : ajoute une instruction au module C5. ① RÔLE — Changer le CODE, pas un commentaire. ② CONTEXTE D'APPEL —
    `main`. ③ ENTRÉE — le texte du module. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte saboté. [rend: 1]
    ⑥ TRAITEMENT — une affectation ajoutée en fin de fichier. ⑦ UNITÉ — — ⑧ POURQUOI — le cas du 20-11-2026 : du code
    changé, la valeur figée immobile. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    return texte + "\n_SABOTAGE_S1_DE_L_ANCRE = 1\n"


def changer_un_commentaire(texte):
    """S2 : ajoute un commentaire au module C5. ① RÔLE — Prouver que l'épreuve ne sur-détecte pas. ② CONTEXTE D'APPEL —
    `main`. ③ ENTRÉE — le texte du module. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte. [rend: 1]
    ⑥ TRAITEMENT — une ligne de commentaire ajoutée. ⑦ UNITÉ — — ⑧ POURQUOI — l'empreinte ignore les commentaires (A-865).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    return texte + "\n# commentaire ajouté par le sabotage S2 de l'ancre\n"


def remettre_l_ancienne(texte):
    """S3 : remet au contrat l'ancienne valeur figée. ① RÔLE — Rejouer le cas réel du 20-11-2026. ② CONTEXTE D'APPEL —
    `main`. ③ ENTRÉE — le texte de CONTRATS. ④ CONDITIONS D'ENTRÉE — la valeur figée y figure une fois. ⑤ SORTIE — UNE
    valeur : le texte saboté. [rend: 1] ⑥ TRAITEMENT — lire la valeur dans l'arbre, la remplacer par ANCIENNE.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-732 : un cas vient d'un fait réel. ⑨ CE QUI CLOCHE — si la valeur figée vaut déjà
    ANCIENNE, le sabotage ne change rien : ValueError, l'épreuve rend 2. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ;
    lève ValueError. [sort: non]"""
    v = valeur_figee(texte)
    if not v or v == ANCIENNE or texte.count('"%s"' % v) != 1:
        raise ValueError("valeur figée introuvable, en double, ou déjà l'ancienne : %r" % v)
    return texte.replace('"%s"' % v, '"%s"' % ANCIENNE)


def main():
    """Point d'entrée. ① RÔLE — Voir fiche en tête. ② CONTEXTE D'APPEL — Le lancement. ③ ENTRÉE — fiche en tête, ③.
    ④ CONDITIONS D'ENTRÉE — fiche en tête, ④. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — fiche en
    tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — fiche en tête, ⑩.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) != 1 or any(o != "--saboter" for o in options):
        print("usage : EPREUVE_DE_L_ANCRE_DE_C5_Sam_21-11-2026.py <racine> [--saboter]")
        return 2
    racine = os.path.abspath(args[0])
    try:
        L = charger_la_longue()
    except Exception as e:  # l'épreuve n'a pas pu tourner (R-734)
        print("ARRÊT : épreuve longue illisible : %s: %s" % (type(e).__name__, e))
        return 2
    faux = L.cas_e_ancre(racine)
    if any("n'a pas tourné" in f for f in faux):
        print("ARRÊT : " + " ; ".join(faux))
        return 2
    if faux:
        print("ROUGE — LA VALEUR FIGÉE DE C5E10-QA-V1 NE SUIT PLUS LE CODE. Le code du module C5 (ou un réglage de la "
              "fiche, l'univers, la période, emp.py) a changé sans que CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE "
              "suive. L'essai de moulinette refusera en 2. Suite : prouver que C5 rend les mêmes sorties, puis décision "
              "de Jean-Luc pour refiger (cas du 20-11-2026, A-957).")
        for f in faux:
            print("  " + f)
        return 1
    print("E-ancre verte : la valeur figée de C5E10-QA-V1 suit le code.")
    if "--saboter" not in options:
        return 0
    copie = L.copie_jetable(racine)
    sabotages = [("S1 code du module C5 changé", L.MODULE_C5, changer_le_code, True),
                 ("S2 commentaire seul du module C5", L.MODULE_C5, changer_un_commentaire, False),
                 ("S3 valeur figée remise à l'ancienne (20-11-2026)", CONTRATS, remettre_l_ancienne, True)]
    ne_mord_pas = []
    try:
        for nom, rel, saboter, doit_rougir in sabotages:
            chemin = os.path.join(copie, rel)
            with open(chemin, "rb") as f:
                origine = f.read()
            try:
                texte = saboter(origine.decode("utf-8"))
            except ValueError as e:
                print("ARRÊT : sabotage %s : %s" % (nom, e))
                return 2
            with open(chemin, "wb") as f:
                f.write(texte.encode("utf-8"))
            try:
                f_s = L.cas_e_ancre(copie)
            finally:
                with open(chemin, "wb") as f:
                    f.write(origine)
            if any("n'a pas tourné" in f for f in f_s):
                print("ARRÊT : sous %s : %s" % (nom, " ; ".join(f_s)))
                return 2
            rouge = bool(f_s)
            print("%s : %s (attendu %s)" % (nom, "ROUGE" if rouge else "VERT", "ROUGE" if doit_rougir else "VERT"))
            if rouge != doit_rougir:
                ne_mord_pas.append(nom)
    finally:
        shutil.rmtree(os.path.dirname(copie), ignore_errors=True)
    if ne_mord_pas:
        print("SABOTAGES QUI NE MORDENT PAS : %s" % ne_mord_pas)
        return 1
    print("Sabotages S1, S2, S3 : conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
