#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CONTRAT_DE_STRATEGIE_Jeu_19-11-2026.py — Jeu 19-11-2026 (Paris). EN ESSAI · épreuve. Simulation uniquement.

LE SENS EN TÊTE. Éprouve le CONTRAT DE STRATÉGIE (BACKLOG A-923 ; A-925, décision de Jean-Luc du 19-11-2026 à 19h23 :
« écrire le contrat », étape 1 de l'étude du 19-11-2026) : `CONTRAT_DE_STRATEGIE`, `manques_du_contrat` et
`avis_du_contrat` de programmes/CONTRATS_DES_FICHIERS.py, et leurs deux branchements à l'entrée de la chaîne —
PREPARER ⓪ (programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py) et la porte du juge
(`porte_du_juge` de programmes/VERIFIER_LA_CHAINE.py). Les fiches éprouvées sont de VRAIES lignes du registre
(R-732) ; tout se joue sur des COPIES sous <travail>, jamais sur le dépôt. Puis deux SABOTAGES du contrat, qui
doivent rougir, et redevenir verts une fois retirés (R-731 : une épreuve qui reste verte quand on retire ce qu'elle
teste est une décoration).

USAGE
    python3 -B tests/EPREUVES_DU_CONTRAT_DE_STRATEGIE_Jeu_19-11-2026.py <source> <travail>
    <source> : la racine d'un worktree du dépôt ; <travail> : un dossier sous /dev/shm qui n'existe pas encore.

① RÔLE — Prouver que le contrat laisse passer les fiches complètes, refuse les autres en NOMMANT chaque case, donne un
  avis sans refuser sur ce que Jean-Luc n'a pas tranché, et qu'il est branché à ⓪ et à la porte du juge.
② CONTEXTE D'APPEL — À la main (le Chat, le relecteur). Aucune tâche automatique.
③ ENTRÉE — La ligne de commande (USAGE). Avec « --sonde <programmes> <A> <B> <C> <D> <E> » : appel interne, en sous-processus.
④ CONDITIONS D'ENTRÉE — <travail> n'existe pas ; <source> porte programmes/, donnees/ et donnees/combinatoires/.
⑤ SORTIE — UNE valeur, le code : 0 tout tient (épreuves vertes, sabotages rouges puis verts) · 1 une épreuve ou un
  sabotage ne se comporte pas comme attendu · 2 une épreuve n'a pas pu tourner (R-734).
⑥ TRAITEMENT — ① copies : A (programmes/ et les fichiers de donnees/ du premier niveau, plus combinatoires/), B (= A,
  la ligne AIR 2025 retirée de VALEURS_TTF.csv), C (= A sans référentiel), D (= A sans MODULE_POSITIONS.py), E (= A,
  C5E10-OBS-V1 réécrite au registre avec l'univers « TTE,ZZZ ») · ② la sonde (E1 à E15) sur la copie A
  intacte : tout vert · ③ sabotage S1 (`manques_du_contrat` rend toujours []) : rouge attendu, puis retiré : vert ·
  ④ sabotage S2 (le contrôle de l'univers retiré) : rouge attendu, puis retiré : vert · ④bis sabotage S3 (la case
  d'un refus cherchée parmi TOUTES les cases, défaut trouvé par l'auteur le 19-11-2026) : E8b rouge, puis vert ·
  ④ter sabotages S4 à S8 (relecteur neuf du 19-11-2026 : I2, M1, M3, M2 ③), chacun EXACTEMENT ses épreuves rouges
  (S4 → E6b, S5 → E13, S6 → E14, S7 → E15, S8 → E5b), puis tout vert retiré · ⑤ bilan.
⑦ UNITÉ — —
⑧ POURQUOI — R-731 ; consigne du Chat du 19-11-2026 (A-925) : « les fiches complètes du registre passent (dis
  lesquelles) ; C5-EI-RETEST refusée avec ses cases ; MA200-S1 (univers « A TRANCHER ») refusée sur l'univers ; un
  « +150% » donne un avis ; sabotages : manques_du_contrat rendant toujours une liste vide → rouge ; contrôle de
  l'univers retiré → rouge ; chacun redevient vert retiré ».
⑨ CE QUI CLOCHE — ① La liste des fiches complètes (E1) est celle du registre du 19-11-2026 : un registre qui change
  la fait rougir — c'est voulu, la liste est une mesure à relire, pas une règle. ② E12 (porte du juge) neutralise
  `VERIFIER_LA_CHAINE.motifs` dans la sonde pour isoler le contrat : la chaîne elle-même est éprouvée par
  tests/EPREUVES_ENCHAINER_LA_MOULINETTE_Jeu_19-11-2026.py. ③ Les clauses du module de signal (étude A.3) ne sont pas
  éprouvées : elles ne sont pas au contrat d'entrée.
⑩ EFFET — Écrit sous <travail> seulement (copies, sorties de PREPARER).
⑪ TERMINAISON — Chaque sous-processus est borné à 300 s. [sort: oui — code]
"""
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
PREP = "programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py"
CONTRATS = "programmes/CONTRATS_DES_FICHIERS.py"
COMPLETES = ["IND-001-RETEST", "C5E10-QA-V1", "C5E10-OBS-V1", "C5-EI-PARAMS"]   # mesurées le 19-11-2026
CASES_C5_EI_RETEST = {"univers", "tp", "sl", "horizon", "periode", "module_signal", "fonction_signal", "entree",
                      "donnees_demandees"}   # cas connu du 14-11-2026 : neuf cases
JOUER = "programmes/JOUER_LES_VERSIONS.py"
# (nom, fichier saboté, texte d'avant, texte d'après, épreuves qui DOIVENT rougir — None : au moins une). Un sabotage
# nouveau (relecteur neuf du 19-11-2026, I2, M1, M3, M2 ③) nomme EXACTEMENT les épreuves qu'il fait rougir : il rougit
# pour SA raison, et pour elle seule.
SABOTAGES = (
    ("S1 manques_du_contrat rend toujours []", CONTRATS,
     '    import os as _os\n    if J is None:\n        import JUGE_DES_STRATEGIES as J\n    refus = []\n',
     '    return []\n    import os as _os\n    if J is None:\n        import JUGE_DES_STRATEGIES as J\n    refus = []\n', None),
    ("S2 contrôle de l'univers retiré", CONTRATS,
     '    if "univers" not in deja:\n        f_ref = J.trouver(racine, "REFERENTIEL_VALEURS")',
     '    if False:\n        f_ref = J.trouver(racine, "REFERENTIEL_VALEURS")', None),
    ("S3 attribution non bornée aux cases du contrôle", CONTRATS,
     '    for c in cases_du_controle:\n        m = _re.search',
     '    for c in CASES_DU_CONTRAT:\n        m = _re.search', None),
    ("S4 rappel de porte_0 sans la période retiré (T2)", CONTRATS,
     '    if len(rendu) == 2:\n', '    if False:\n', {"E6b"}),
    ("S5 id vide accepté", CONTRATS,
     '        refus.append(("id", "aucun identifiant"))\n', '        pass\n', {"E13"}),
    ("S6 MODULE_POSITIONS absent : pas d'arrêt", CONTRATS,
     '                    raise ContratImpossible("MODULE_POSITIONS.py introuvable sous %s" % racine)\n',
     '                    return ["%s : %s" % r for r in refus]\n', {"E14"}),
    ("S7 JOUER ne passe plus la fiche relue au contrat (M3)", JOUER,
     '        refus_du_contrat = contrat.manques_du_contrat(fiche, base, J=J, mod_pos=mod_pos)\n',
     '        refus_du_contrat = []\n', {"E15"}),
    ("S8 années sans liste dans VALEURS_TTF sautées (ancien choix des années, M2 ③)", CONTRATS,
     '                    if d[:4] in manquent:\n',
     '                    if d[:4] in manquent or d[:4] > "2026":\n', {"E5b"}),
)


def cases_de(refus):
    """Rend l'ensemble des cases nommées par une liste de refus « <case> : <motif> ».

    ① RÔLE — Lire la case de chaque refus rendu par `manques_du_contrat`.
    ② CONTEXTE D'APPEL — `sonde`, pour E2, E3, E5, E6, E7, E8.
    ③ ENTRÉE — `refus` : une liste de textes.
    ④ CONDITIONS D'ENTRÉE — Chaque texte porte « : ».
    ⑤ SORTIE — UNE valeur : un ensemble de noms de cases (un groupe « a/b/c » donne a, b et c). [rend: 1]
    ⑥ TRAITEMENT — couper au premier « : », puis aux « / ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui exige qu'un refus NOMME sa case doit lire le nom, pas le motif.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main. [sort: non]
    """
    return {c.strip() for r in refus for c in r.split(" : ", 1)[0].split("/")}


def sonde(programmes, A, B, C, D, E):
    """Joue E1 à E12 dans CE processus, modules chargés depuis `programmes` ; affiche un JSON {épreuve: [vert, détail]}.

    ① RÔLE — Mesurer le contrat tel qu'il est écrit dans la copie (intacte ou sabotée), en un processus neuf.
    ② CONTEXTE D'APPEL — `__main__` avec « --sonde », lancé par `lancer_la_sonde`.
    ③ ENTRÉE — `programmes` : le dossier programmes/ de la copie A ; `A` à `E` : les cinq racines copiées.
    ④ CONDITIONS D'ENTRÉE — Les copies faites par `copier`.
    ⑤ SORTIE — Aucune valeur rendue ; un JSON affiché sur la sortie standard. [rend: 0]
    ⑥ TRAITEMENT — E1 fiches complètes · E2 C5-EI-RETEST · E3 MA200-S1 · E4 « +150% » · E5 AIR sans ligne 2025 (B) ·
      E6 période « banane » et univers « TTE,ZZZ » ensemble · E7 « sans stop » au soir / au labo · E8 module absent ·
      E8b un réglage de signal nommé « periode » (vraie fiche IND-001-RETEST, réglage « inconnu » ajouté) ·
      E9 référentiel absent (C) · E10 forme du contrat · E11 PREPARER ⓪ · E12 porte du juge · ajoutées le 19-11-2026
      (relecteur neuf, I2, M1, M2 ③, M3) : E5b période qui déborde sur 2027 (année sans liste, taxée) · E6b T2 sur une
      fiche du LABO (période « banane », tp « x », entree vide : les trois cases nommées) · E13 id vide · E14
      MODULE_POSITIONS absent (D) : ContratImpossible · E15 JOUER_LES_VERSIONS (copie E, registre réécrit après ⓪) :
      arrêt nommé sur le contrat, avant tout jeu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un processus neuf par mesure : un module saboté ne reste pas en mémoire d'une mesure à l'autre.
    ⑨ CE QUI CLOCHE — voir ⑨ ② de l'en-tête (E12).
    ⑩ EFFET — Charge les modules de la copie ; E11 écrit sous un dossier neuf A/../sortie_prep_* ; E12 crée un journal
      vide sous A.
    ⑪ TERMINAISON — Rend la main ; E11 lance PREPARER borné à 300 s. [sort: non]
    """
    sys.path.insert(0, programmes)
    import CONTRATS_DES_FICHIERS as CT
    import JUGE_DES_STRATEGIES as J
    res = {}

    def e(nom, fn):
        try:
            ok, det = fn()
        except Exception as x:          # noqa: BLE001 — une épreuve qui lève est rouge, avec sa raison
            ok, det = False, "LÈVE %s: %s" % (type(x).__name__, x)
        res[nom] = [bool(ok), str(det)[:400]]

    fiches = CT.fiches_du_registre(os.path.join(A, CT.REGISTRE_DES_STRATEGIES))
    m = lambda f, r=A: CT.manques_du_contrat(f, r, J=J)

    def e1():
        passent = [i for i, f in fiches.items() if not m(f)]
        return passent == COMPLETES, "passent : %s" % passent
    e("E1 fiches complètes du registre : passent, et elles seules", e1)

    def e2():
        r = m(fiches["C5-EI-RETEST"])
        return cases_de(r) == CASES_C5_EI_RETEST, "cases : %s" % sorted(cases_de(r))
    e("E2 C5-EI-RETEST refusée, ses neuf cases nommées", e2)

    def e3():
        r = [x for x in m(fiches["MA200-S1"]) if x.startswith("univers : ")]
        return any("A TRANCHER" in x for x in r), r
    e("E3 MA200-S1 refusée sur l'univers « A TRANCHER »", e3)

    def e4():
        f = dict(fiches["C5E10-QA-V1"], tp="+150%")
        r, a = m(f), CT.avis_du_contrat(f, J=J)
        return r == [] and any(x.startswith("tp : AVIS") for x in a), "refus %s · avis %s" % (r, a)
    e("E4 tp « +150% » : un avis, aucun refus", e4)

    def e5():
        r = m(fiches["C5-EI-PARAMS"], B)
        temoin = m(fiches["C5E10-QA-V1"], B)          # sans AIR : doit passer (le motif ne sur-détecte pas)
        return any(x.startswith("univers : AIR") and "2025" in x for x in r) and temoin == [], \
            "C5-EI-PARAMS %s · C5E10-QA-V1 %s" % (r, temoin)
    e("E5 valeur sans ligne VALEURS_TTF 2025 : refus univers nommé ; une fiche sans elle passe", e5)

    def e5b():
        r = m(dict(fiches["C5-EI-PARAMS"], periode="2024-04-29 -> 2027-03-11"))
        return any(x.startswith("univers : AIR") and "2027" in x for x in r), r
    e("E5b période qui déborde sur 2027 (taxée, sans liste) : refus univers nommé, l'année dite", e5b)

    def e6():
        r = m(dict(fiches["C5E10-QA-V1"], periode="banane", univers="TTE,ZZZ"))
        return {"periode", "univers"} <= cases_de(r), r
    e("E6 période mal formée ne cache plus l'univers (T2)", e6)

    def e6b():
        # LA CASE QUE SEULE `porte_0` VOIT (entree), sur une fiche du LABO pour que la lecture du soir ne rattrape rien
        # (relecteur neuf du 19-11-2026, I2 : E6 restait verte sans le rappel, l'univers venant de l'étape ④).
        r = m(dict(fiches["C5-EI-PARAMS"], periode="banane", tp="x", entree=""))
        return {"periode", "tp", "entree"} <= cases_de(r), r
    e("E6b T2 : période « banane », tp « x », entree vide (LABO) : les trois cases nommées", e6b)

    def e7():
        qa = m(dict(fiches["C5E10-QA-V1"], sl="sans stop"))
        labo = m(dict(fiches["C5-EI-PARAMS"], sl="sans stop"))
        return "sl" in cases_de(qa) and labo == [], "QA %s · LABO %s" % (qa, labo)
    e("E7 « sans stop » : refusé au soir (QA), admis au labo", e7)

    def e8():
        r = m(dict(fiches["C5-EI-PARAMS"], module_signal="programmes/N_EXISTE_PAS.py"))
        return "module_signal" in cases_de(r), r
    e("E8 module de signal introuvable : refus nommé", e8)

    def e8b():
        f = dict(fiches["IND-001-RETEST"], reglages_signal='{"periode": 14, "seuil": 30, "chauffe": 100, "inconnu": 1}')
        r = m(f)
        return r != [] and "periode" not in cases_de(r) and all(
            set(x.split(" : ", 1)[0].split("/")) <= {"module_signal", "fonction_signal", "reglages_signal"} for x in r), r
    e("E8b réglage de signal nommé « periode », refusé par la signature : attribué au signal, jamais à la période", e8b)

    def e9():
        try:
            CT.manques_du_contrat(fiches["C5E10-QA-V1"], C, J=J)
        except CT.ContratImpossible as x:
            return True, str(x)
        return False, "aucune exception : un contrôle sans référentiel a rendu un verdict"
    e("E9 référentiel absent : ContratImpossible (R-734), jamais une liste", e9)

    def e10():
        cles = {"case", "type", "admis", "source", "controle"}
        ok = len(CT.CONTRAT_DE_STRATEGIE) == 13 and all(set(c) == cles and all(c.values())
                                                         for c in CT.CONTRAT_DE_STRATEGIE) \
            and set(CT.CASES_DU_CONTRAT) <= set(CT.STRATEGIE) and len(set(CT.CASES_DU_CONTRAT)) == 13
        return ok, "%d cases ; hors des colonnes du registre : %s" % (
            len(CT.CONTRAT_DE_STRATEGIE), sorted(set(CT.CASES_DU_CONTRAT) - set(CT.STRATEGIE)))
    e("E10 treize cases, chacune avec type, valeurs admises, source et contrôle, toutes colonnes du registre", e10)

    def e11():
        import tempfile
        sortie = tempfile.mkdtemp(prefix="sortie_prep_", dir=os.path.dirname(A))   # un dossier neuf par sonde
        args = [sys.executable, "-B", os.path.join(A, PREP), os.path.join(A, CT.REGISTRE_DES_STRATEGIES)]
        vois = os.path.join(A, "donnees/combinatoires/VOISINAGE.csv")
        p1 = subprocess.run(args + ["C5E10-TP5-SL5", vois, "E01", sortie], capture_output=True, text=True, timeout=300)
        p2 = subprocess.run(args + ["C5E10-OBS-V1", vois, "E77", sortie], capture_output=True, text=True, timeout=300)
        o1 = p1.stdout + p1.stderr
        ok = p1.returncode == 1 and "contrat de stratégie (A-923) — module_signal" in o1 and \
            "contrat de stratégie (A-923) — periode" in o1 and p2.returncode == 0
        return ok, "TP5-SL5 code %d : %s ‖ OBS-V1 code %d" % (p1.returncode, " | ".join(
            l.strip() for l in o1.splitlines() if "contrat" in l), p2.returncode)
    e("E11 PREPARER ⓪ refuse C5E10-TP5-SL5 en nommant les cases, laisse passer C5E10-OBS-V1", e11)

    def e12():
        import VERIFIER_LA_CHAINE as V
        V.motifs = lambda *a, **k: []          # isoler le contrat (⑨ ② de l'en-tête)
        sid, essai = "C5-EI-PARAMS", "E99"
        d = V.dossier(A, sid, essai)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, V.JOURNAL), "a").close()
        marquee = dict(fiches["C5-EI-PARAMS"], univers="TTE,ZZZ")
        marquee[CT.COLONNE_DE_LA_MARQUE_DE_MOULINETTE] = "%s %s %s" % (CT.MARQUE_DE_MOULINETTE, sid, essai)
        r = V.porte_du_juge(A, marquee, J=J)
        bonne = V.porte_du_juge(A, dict(marquee, univers="TTE,ENGI"), J=J)
        return any(x.startswith("contrat de stratégie (A-923) — univers : ") and "ZZZ" in x for x in (r or [])) \
            and bonne == [], "ZZZ %s · TTE,ENGI %s" % (r, bonne)
    e("E12 porte du juge : une version marquée hors contrat est refusée, la case nommée", e12)

    def e13():
        r = m(dict(fiches["C5-EI-PARAMS"], id=""))
        return "id" in cases_de(r), r
    e("E13 id vide : refus, la case id nommée", e13)

    def e14():
        try:
            r = CT.manques_du_contrat(fiches["C5E10-QA-V1"], D, J=J)
        except CT.ContratImpossible as x:
            return "MODULE_POSITIONS" in str(x), str(x)
        return False, "aucune exception : un contrôle sans MODULE_POSITIONS a rendu %s" % r
    e("E14 MODULE_POSITIONS absent : ContratImpossible (R-734), jamais une liste", e14)

    def e15():
        # JOUER, LANCÉ DANS UN PROCESSUS NEUF SUR LA COPIE E, dont le registre porte en DERNIÈRE ligne C5E10-OBS-V1
        # réécrite avec l'univers « TTE,ZZZ » (passe `porte_0`, hors contrat). Le calibrage par le juge seul est
        # remplacé par un succès : l'épreuve mesure ce que JOUER fait de la fiche RELUE, pas le juge.
        import tempfile
        sortie = os.path.join(tempfile.mkdtemp(prefix="sortie_jouer_", dir=os.path.dirname(E)), "R.csv")
        pilote = ("import sys; sys.path.insert(0, %r); import JOUER_LES_VERSIONS as JV; "
                  "JV.calibrer_par_le_juge = lambda *a, **k: (True, 'calibrage remplacé par l épreuve'); "
                  "sys.argv = ['JOUER', %r, %r, %r]; sys.exit(JV.main())"
                  % (os.path.join(E, "programmes"), E,
                     os.path.join(E, "donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv"), sortie))
        p = subprocess.run([sys.executable, "-B", "-c", pilote], capture_output=True, text=True, timeout=300, cwd=E)
        o = p.stdout + p.stderr
        ok = p.returncode == 1 and "ne suit pas le contrat de stratégie" in o and "ZZZ" in o \
            and not os.path.exists(sortie)
        return ok, "code %d : %s" % (p.returncode, " | ".join(l for l in o.splitlines() if "ARR" in l or "Error" in l)
                                     or o[-300:])
    e("E15 JOUER refuse la fiche relue hors contrat (registre réécrit après ⓪), avant tout jeu", e15)
    print(json.dumps(res, ensure_ascii=False))


def copier(source, travail):
    """Fabrique les cinq copies A à E sous `travail`, et rend leurs chemins.

    ① RÔLE — Ne jamais éprouver sur le dépôt : programmes/ et les fichiers de donnees/ utiles, copiés.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `source` : la racine du worktree ; `travail` : le dossier de travail (créé ici).
    ④ CONDITIONS D'ENTRÉE — `travail` n'existe pas.
    ⑤ SORTIE — CINQ valeurs : les racines A, B, C, D, E. [rend: 5]
    ⑥ TRAITEMENT — A : programmes/ (sans __pycache__), les fichiers .py de la racine (emp.py, importé par la chaîne),
      les fichiers du premier niveau de donnees/, donnees/combinatoires/ et donnees/sources_indice/ · B : A, puis la ligne « 2025,AIR, » retirée de donnees/VALEURS_TTF.csv (exactement une) ·
      C : A sans donnees/REFERENTIEL_VALEURS*.csv · D : A sans programmes/MODULE_POSITIONS.py · E : A, plus une
      DERNIÈRE ligne au registre : la vraie fiche C5E10-OBS-V1, univers « TTE,ZZZ » (la dernière ligne fait foi, n°83).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — E5 a besoin d'une valeur connue du référentiel et absente de la liste d'une année ; E9 d'une racine
      sans référentiel. Les fabriquer à partir des VRAIS fichiers (R-732).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sous `travail`.
    ⑪ TERMINAISON — Rend la main ; lève FileExistsError si `travail` existe, AssertionError si la ligne AIR 2025 n'est
      pas unique. [sort: non]
    """
    os.makedirs(travail)
    A, B, C, D, E = (os.path.join(travail, x) for x in ("A", "B", "C", "D", "E"))
    shutil.copytree(os.path.join(source, "programmes"), os.path.join(A, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    for n in os.listdir(source):
        if n.endswith(".py") and os.path.isfile(os.path.join(source, n)):
            shutil.copy2(os.path.join(source, n), os.path.join(A, n))
    os.makedirs(os.path.join(A, "donnees"))
    for n in os.listdir(os.path.join(source, "donnees")):
        p = os.path.join(source, "donnees", n)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(A, "donnees", n))
    shutil.copytree(os.path.join(source, "donnees", "combinatoires"), os.path.join(A, "donnees", "combinatoires"))
    # le lecteur unique des cours lit l'identité des sociétés (E15 : JOUER lit les cours avant la fiche)
    shutil.copytree(os.path.join(source, "donnees", "sources_indice"), os.path.join(A, "donnees", "sources_indice"))
    shutil.copytree(A, B)
    shutil.copytree(A, C)
    shutil.copytree(A, D)
    shutil.copytree(A, E)
    os.remove(os.path.join(D, "programmes", "MODULE_POSITIONS.py"))
    import csv
    reg = os.path.join(E, "donnees", "cac40_strategies.csv")
    texte = open(reg, encoding="utf-8").read()
    entete = next(l for l in texte.split("\n") if l.startswith("id,") or ",univers," in l)
    lignes_obs = [r for r in csv.DictReader(texte.split("\n")[texte.split("\n").index(entete):])
                  if r.get("id") == "C5E10-OBS-V1"]
    assert lignes_obs, "C5E10-OBS-V1 absente du registre"
    import io
    tampon = io.StringIO()
    w = csv.DictWriter(tampon, fieldnames=next(csv.reader([entete])), lineterminator="\n")
    w.writerow(dict(lignes_obs[-1], univers="TTE,ZZZ"))
    open(reg, "a", encoding="utf-8").write(("" if texte.endswith("\n") else "\n") + tampon.getvalue())
    ttf = os.path.join(B, "donnees", "VALEURS_TTF.csv")
    lignes = open(ttf, encoding="utf-8").read().split("\n")
    air = [l for l in lignes if l.startswith("2025,AIR,")]
    assert len(air) == 1, air
    open(ttf, "w", encoding="utf-8").write("\n".join(l for l in lignes if l not in air))
    for n in os.listdir(os.path.join(C, "donnees")):
        if n.upper().startswith("REFERENTIEL_VALEURS"):
            os.remove(os.path.join(C, "donnees", n))
    return A, B, C, D, E


def lancer_la_sonde(A, B, C, D, E):
    """Lance la sonde dans un processus neuf ; rend le dictionnaire des épreuves.

    ① RÔLE — Mesurer le contrat tel qu'il est écrit À CET INSTANT dans la copie A.
    ② CONTEXTE D'APPEL — `main`, une fois sans sabotage, puis deux fois par sabotage.
    ③ ENTRÉE — Les cinq racines.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {épreuve: [vert, détail]}. [rend: 1]
    ⑥ TRAITEMENT — `python3 -B <ce fichier> --sonde`, dernière ligne de la sortie lue en JSON.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un processus neuf : aucun module chargé ne survit au sabotage suivant.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de la sonde.
    ⑪ TERMINAISON — Rend la main ; lève RuntimeError si la sonde ne rend pas de JSON (épreuve impossible), et
      subprocess.TimeoutExpired au-delà de 600 s. [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--sonde", os.path.join(A, "programmes"),
                        A, B, C, D, E], capture_output=True, text=True, timeout=600, cwd=A)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        raise RuntimeError("la sonde n'a pas rendu de JSON (code %d) : %s" % (p.returncode, (p.stdout + p.stderr)[-800:]))


def main(argv):
    """Rend le code de sortie : copies, épreuves, sabotages, bilan.

    ① RÔLE — Le déroulé de l'épreuve (⑥ de l'en-tête).
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `argv` : [programme, source, travail].
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — ① copies · ② sonde intacte, tout vert · ③ pour chaque sabotage : poser, sonder (au moins une
      épreuve rouge attendue, nommées), retirer à l'octet, sonder (tout vert) · ④ afficher chaque ligne et le bilan.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sous <travail> ; affiche.
    ⑪ TERMINAISON — Rend la main ; `__main__` passe le code à `sys.exit`. [sort: non]
    """
    if len(argv) != 3:
        print(__doc__.split("① RÔLE")[0])
        return 2
    source, travail = os.path.abspath(argv[1]), os.path.abspath(argv[2])
    try:
        A, B, C, D, E = copier(source, travail)
        rouge = 0
        base = lancer_la_sonde(A, B, C, D, E)
        print("— CONTRAT INTACT —")
        for k, (ok, det) in base.items():
            print("  %s %s\n      %s" % ("✅" if ok else "❌", k, det))
            rouge += not ok
        for nom, fichier, avant, apres, attendues in SABOTAGES:
            # le fichier saboté l'est dans CHAQUE copie qui le porte et le sert (A, et E pour JOUER) — restitué à l'octet
            cibles = [os.path.join(r, fichier) for r in (A, E)]
            originaux = {f: open(f, "rb").read() for f in cibles}
            for f in cibles:
                texte = originaux[f].decode("utf-8")
                if texte.count(avant) != 1:
                    raise RuntimeError("%s : le texte à saboter n'est pas unique (%d)" % (nom, texte.count(avant)))
                open(f, "w", encoding="utf-8").write(texte.replace(avant, apres))
            sab = lancer_la_sonde(A, B, C, D, E)
            rouges = [k for k, (ok, _) in sab.items() if not ok]
            for f in cibles:
                open(f, "wb").write(originaux[f])
            retire = lancer_la_sonde(A, B, C, D, E)
            verts = all(ok for ok, _ in retire.values()) and all(open(f, "rb").read() == originaux[f] for f in cibles)
            noms = {r.split(" ")[0] for r in rouges}
            pour_sa_raison = bool(rouges) if attendues is None else noms == attendues
            print("— %s — posé : %s ; retiré : %s" % (nom, ("ROUGE %s (%d) : %s%s" % (
                "✅" if pour_sa_raison else "❌", len(rouges), ", ".join(r.split(" ")[0] for r in rouges),
                "" if attendues is None else " (attendu : %s)" % ", ".join(sorted(attendues))))
                if rouges else "VERT ❌ (le sabotage ne se voit pas)", "VERT ✅" if verts else "ROUGE ❌"))
            if attendues is not None:   # la raison du rouge, lisible : le détail de chaque épreuve tombée
                for k in rouges:
                    print("      %s sous sabotage : %s" % (k.split(" ")[0], sab[k][1][:220]))
            rouge += (not pour_sa_raison) + (not verts)
        print("BILAN : %s" % ("TOUT TIENT" if not rouge else "%d défaut(s)" % rouge))
        return 0 if not rouge else 1
    except (OSError, RuntimeError, AssertionError, subprocess.TimeoutExpired) as x:
        print("ÉPREUVE IMPOSSIBLE (R-734) : %s: %s" % (type(x).__name__, x))
        return 2


if __name__ == "__main__":
    if len(sys.argv) == 8 and sys.argv[1] == "--sonde":
        sonde(*sys.argv[2:])
        sys.exit(0)
    sys.exit(main(sys.argv))
