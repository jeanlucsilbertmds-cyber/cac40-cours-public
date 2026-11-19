#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_E8_LE_SOIR_SUIT_LA_STRATEGIE_DECIDEE_Mer_18-11-2026.py — Mer 18-11-2026 (Paris) — épreuves de l'étape E8
du planning (plan V7, bloc 9 ; BACKLOG A-644). Simulation uniquement — aucun ordre réel.

LE SENS EN TÊTE. Le circuit du soir doit faire tourner la stratégie que Jean-Luc a DÉCIDÉE, telle que sa fiche la
déclare, chaque fiche isolée des autres, et le radar doit juger chaque position sur les seuils de SA fiche. Trois
changements du 18-11-2026 le portent : ① le soir choisit ses fiches sur `etat_vie` (QA ou PRODUCTION), par
`suivie_par_le_soir` de programmes/CONTRATS_DES_FICHIERS.py, appelée par programmes/DETECTER_LES_SIGNAUX_GITHUB.py et
programmes/TENIR_LES_POSITIONS.py (R-513 ① ; avant : « VIVANTE » dans la colonne d'affichage `statut`, deux copies) ;
② une fiche suivie que la garde du soir refuse, ou dont l'horizon est illisible, est MISE À PART par le teneur, les
autres tournent, et la sortie du pas `fiches_mises_a_part=<n>` fait rougir le pas de fin « Rougir si une fiche suivie
a ete mise a part » de .github/workflows/collecte_abc.yml (avant : un horizon illisible arrêtait tout le soir, code 1) ;
③ le maillon 11 de programmes/audit_ecosysteme.py confronte l'objectif et le stop de chaque position ouverte aux
seuils de sa fiche (avant : aux constantes de C5, en critique pour toute autre stratégie).

① RÔLE — Prouver ces trois propriétés sur une copie du dépôt, et, avec `--saboter`, que chaque épreuve MORD : chaque
  sabotage retire une partie de la correction et doit faire rougir au moins une épreuve.
② CONTEXTE D'APPEL — À la main : `python3 -I tests/EPREUVES_E8_LE_SOIR_SUIT_LA_STRATEGIE_DECIDEE_Mer_18-11-2026.py
  <racine> [--saboter]` ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis « --saboter ».
③ ENTRÉE — `<racine>` : un clone du dépôt, jamais modifié (tout se joue sur une copie sous /dev/shm ou /tmp).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/, donnees/ (registre des stratégies avec C5E10-QA-V1 et
  C5E10-OBS-V1, référentiel, cours maître avec la séance VEOLIA du 2026-11-17), tests/GARDE_DU_PAS_ROUGE.py et
  .github/workflows/collecte_abc.yml ; le module `yaml` de Python.
⑤ SORTIE — UNE valeur, le code de sortie : 0 si toutes les épreuves passent (et, avec --saboter, si chaque sabotage
  fait rougir au moins une épreuve) ; 1 sinon ; 2 si la copie n'a pas pu être faite. [rend: 1]
⑥ TRAITEMENT — ① copier la racine sans .git, etudes/, archives/ · ② jouer les cas K1 à K9 (registre, signaux et
  positions fabriqués à partir des vraies lignes, programmes lancés en ligne de commande comme le circuit) · ③ avec
  --saboter : pour chaque sabotage, remettre les fichiers d'origine, saboter, rejouer les cas, exiger un rouge.
⑦ UNITÉ — Prix en euros ; seuils de fiche en pourcents au registre.
⑧ POURQUOI — Boucle R-731 (épreuves avec sabotages, une vraie ligne R-732) : une épreuve qui reste verte quand on
  retire ce qu'elle teste est une décoration.
⑨ CE QUI CLOCHE — ① La seconde porte du teneur (horizon illisible d'une fiche que `porte_0` aurait laissée passer)
  n'est PAS éprouvée : `porte_0` refuse déjà tout horizon illisible, le chemin réel passe par la garde. ② Le circuit
  n'est pas lancé : K5 lit la forme du pas rouge par `GARDE_DU_PAS_ROUGE.garde_du_pas_rouge` (voir son ⑨). ③ Les cas
  dépendent des deux fiches vivantes au 18-11-2026 et de la séance VEOLIA du 2026-11-17 au cours maître.
⑩ EFFET — Écrit seulement dans son dossier temporaire, qu'il efface à la fin.
⑪ TERMINAISON — Rend la main ; chaque programme lancé est borné à 300 s. [sort: oui — code]
"""
import csv, io, json, os, shutil, subprocess, sys, tempfile

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
SABOTER = "--saboter" in sys.argv
CTR = "programmes/CONTRATS_DES_FICHIERS.py"
DET = "programmes/DETECTER_LES_SIGNAUX_GITHUB.py"
TEN = "programmes/TENIR_LES_POSITIONS.py"
RAD = "programmes/audit_ecosysteme.py"
YML = ".github/workflows/collecte_abc.yml"
REG = "donnees/cac40_strategies.csv"
SIG = "donnees/signaux_du_jour.json"
POS = "donnees/claude_positions_ouvertes.csv"
QA, OBS = "C5E10-QA-V1", "C5E10-OBS-V1"
# LA VRAIE LIGNE (R-732) : cours maître, « VEOLIA,2026-11-17,34.7,34.74,34.21,34.36,1121896,abc » ; VEOLIA (VIE) est
# dans l'univers des deux fiches vivantes, TOTALENERGIES (TTE) dans celui de C5E10-OBS-V1 seulement.
SEANCE, VALEUR, CLOTURE = "2026-11-17", "VEOLIA", 34.36


def copier():
    """Copie la racine dans un dossier jetable. ① RÔLE — Ne jamais jouer sur le dépôt. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — RACINE. ④ CONDITIONS D'ENTRÉE — de la place sous /dev/shm ou le dossier temporaire. ⑤ SORTIE — UNE valeur,
    le chemin de la copie. [rend: 1] ⑥ TRAITEMENT — copier sans .git, etudes/, archives/. ⑦ UNITÉ — —. ⑧ POURQUOI — les
    programmes du circuit écrivent tous (instructions du projet, §7). ⑨ CE QUI CLOCHE — une copie laissée par un arrêt
    brutal reste. ⑩ EFFET — écrit la copie. ⑪ TERMINAISON — rend la main ; lève OSError. [sort: non]"""
    base = os.path.join("/dev/shm" if os.path.isdir("/dev/shm") else tempfile.gettempdir(), "epreuves_E8_%d" % os.getpid())
    shutil.copytree(RACINE, base, ignore=lambda d, n: [x for x in n if d == RACINE and x in (".git", "etudes", "archives")])
    return base


def changer(t, ident, valeurs):
    """Rend le texte du registre où la DERNIÈRE ligne de `ident` porte les `valeurs` ({colonne: texte}).
    ① RÔLE — Fabriquer un registre de cas. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `t` : texte du registre ·
    `ident` · `valeurs`. ④ CONDITIONS D'ENTRÉE — `ident` présent, colonnes dans l'en-tête. ⑤ SORTIE — UNE valeur, le texte.
    [rend: 1] ⑥ TRAITEMENT — lire en CSV, changer les cases, réécrire. ⑦ UNITÉ — —. ⑧ POURQUOI — la dernière ligne d'un
    identifiant fait foi (n°83). ⑨ CE QUI CLOCHE — les guillemets sont réécrits à la manière du module csv. ⑩ EFFET —
    Aucun. ⑪ TERMINAISON — lève ValueError si l'identifiant ou une colonne manque. [sort: non]"""
    lignes = list(csv.reader(io.StringIO(t)))
    rang = max(i for i, l in enumerate(lignes) if l and l[0] == ident)
    for col, v in valeurs.items():
        lignes[rang][lignes[0].index(col)] = v
    s = io.StringIO()
    csv.writer(s, lineterminator="\n").writerows(lignes)
    return s.getvalue()


def ajouter_copie(t, ident, nouvel, valeurs):
    """Rend le registre avec une ligne de plus : la dernière ligne de `ident`, renommée `nouvel`, cases `valeurs` changées.
    ① RÔLE — Fabriquer une fiche d'essai à partir d'une vraie fiche (R-732). ② CONTEXTE D'APPEL — K6. ③ ENTRÉE — `t`,
    `ident`, `nouvel`, `valeurs`. ④ CONDITIONS D'ENTRÉE — celles de `changer`. ⑤ SORTIE — UNE valeur, le texte. [rend: 1]
    ⑥ TRAITEMENT — copier la ligne, changer `id` et les cases, l'ajouter à la fin. ⑦ UNITÉ — —. ⑧ POURQUOI — une fiche
    aux seuils autres que ceux de C5. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — comme `changer`. [sort: non]"""
    lignes = list(csv.reader(io.StringIO(t)))
    rang = max(i for i, l in enumerate(lignes) if l and l[0] == ident)
    neuve = list(lignes[rang])
    neuve[0] = nouvel
    for col, v in valeurs.items():
        neuve[lignes[0].index(col)] = v
    lignes.append(neuve)
    s = io.StringIO()
    csv.writer(s, lineterminator="\n").writerows(lignes)
    return s.getvalue()


def lancer(base, programme):
    """Lance un programme du circuit sur la copie, avec un GITHUB_OUTPUT ; rend (code, affichage, sortie du pas).
    ① RÔLE — Emprunter le chemin réel, en ligne de commande. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `base`,
    `programme` (chemin relatif). ④ CONDITIONS D'ENTRÉE — le programme sous `base`. ⑤ SORTIE — TROIS valeurs. [rend: 3]
    ⑥ TRAITEMENT — vider le fichier de sortie, lancer `python3 -B <programme> .`, relire. ⑦ UNITÉ — —. ⑧ POURQUOI — le
    code et la sortie du pas font partie de ce qui est éprouvé. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — le programme écrit dans
    la copie. ⑪ TERMINAISON — borné à 300 s, lève au-delà. [sort: non]"""
    so = os.path.join(base, "_sortie_du_pas")
    open(so, "w").close()
    p = subprocess.run([sys.executable, "-B", programme, "."], cwd=base, capture_output=True, text=True, timeout=300,
                       env=dict(os.environ, GITHUB_OUTPUT=so))
    sortie = dict(l.split("=", 1) for l in open(so, encoding="utf-8").read().splitlines() if "=" in l)
    return p.returncode, p.stdout + p.stderr, sortie


def position(strategie, valeur, pe, tp, sl, compta="un_jeton"):
    """Rend une ligne OUVERTE du fichier des positions. ① RÔLE — Fabriquer une position de cas. ② CONTEXTE D'APPEL — K6.
    ③ ENTRÉE — stratégie, valeur, prix d'entrée, objectif, stop (euros), comptabilité. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur, un dictionnaire aux colonnes du contrat POSITION. [rend: 1] ⑥ TRAITEMENT — remplir.
    ⑦ UNITÉ — euros. ⑧ POURQUOI — le radar lit ce fichier. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — rend
    la main. [sort: non]"""
    return {"strategie": strategie, "valeur": valeur, "date_signal": "2026-11-12", "date_entree": "2026-11-13",
            "prix_entree": "%.5f" % pe, "tp": "%.5f" % tp, "sl": "%.5f" % sl, "horizon_fin": "2026-12-11",
            "statut": "OUVERTE", "comptabilite": compta, "regles_pre_trade": "", "explication": "epreuve E8",
            "frais_non_chiffrables": ""}


def ecrire_positions(base, lignes):
    """Écrit le fichier des positions de la copie. ① RÔLE — Poser l'état du cas. ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — `base`, `lignes`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune. [rend: rien] ⑥ TRAITEMENT — écrire l'en-tête
    du contrat POSITION, lu dans le fichier d'origine, puis les lignes. ⑦ UNITÉ — —. ⑧ POURQUOI — l'en-tête ne se
    recopie pas ici (R-708). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit le fichier. ⑪ TERMINAISON — rend la main. [sort: non]"""
    entete = open(os.path.join(base, POS), encoding="utf-8").readline().strip().split(",") if os.path.isfile(
        os.path.join(base, POS)) else list(lignes[0])
    with open(os.path.join(base, POS), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=entete, lineterminator="\n")
        w.writeheader()
        for l in lignes:
            w.writerow(l)


def les_cas(base, reg0, pos0):
    """Joue K1 à K9 sur `base` ; rend la liste (nom, vrai/faux, preuve).
    ① RÔLE — Les cas. ② CONTEXTE D'APPEL — `main`, une fois puis une fois par sabotage. ③ ENTRÉE — `base`, `reg0` (le
    vrai registre), `pos0` (le vrai fichier des positions). ④ CONDITIONS D'ENTRÉE — celles du fichier. ⑤ SORTIE — UNE
    valeur, la liste. [rend: 1] ⑥ TRAITEMENT — chaque cas pose registre, signaux et positions, lance, juge.
    ⑦ UNITÉ — —. ⑧ POURQUOI — voir ⑧ du fichier. ⑨ CE QUI CLOCHE — voir ⑨ du fichier. ⑩ EFFET — écrit dans la copie.
    ⑪ TERMINAISON — celle des programmes lancés. [sort: non]"""
    res = []

    def dire(nom, ok, preuve):
        res.append((nom, bool(ok), str(preuve)[-500:]))

    def poser(reg, signaux=None, positions=None):
        open(os.path.join(base, REG), "w", encoding="utf-8").write(reg)
        open(os.path.join(base, POS), "w", encoding="utf-8").write(pos0)
        if positions is not None:
            ecrire_positions(base, positions)
        if signaux is not None:
            json.dump({"seance": SEANCE, "signaux": signaux}, open(os.path.join(base, SIG), "w", encoding="utf-8"))

    def positions_lues():
        return list(csv.DictReader(open(os.path.join(base, POS), encoding="utf-8-sig")))

    un_signal = [{"valeur": VALEUR, "date_signal": SEANCE, "cmf": 0.01, "cci": -80.0, "close": CLOTURE}]

    # K1 — LA STRATÉGIE DÉCIDÉE SE LIT DANS `etat_vie` : C5E10-QA-V1 garde `etat_vie` QA, son `statut` (affichage) est
    # vidé ; le détecteur et le teneur la suivent encore.
    poser(changer(reg0, QA, {"statut": ""}))
    cd, od, _s = lancer(base, DET)
    poser(changer(reg0, QA, {"statut": ""}), un_signal)
    ct, ot, st = lancer(base, TEN)
    ok = (cd == 0 and "fiches suivies : " in od and QA in od.split("fiches suivies : ", 1)[1].split("·")[0]
          and ct == 0 and ("horizon lu au registre · %s" % QA) in ot
          and {p["strategie"] for p in positions_lues()} == {QA, OBS})
    dire("K1 statut vidé, etat_vie QA : la fiche est suivie par le détecteur et reçoit le signal VEOLIA", ok,
         "det %d · teneur %d · %s" % (cd, ct, (od + ot)[-300:]))

    # K2 — UNE FICHE FERMÉE PAR SON ÉTAT DE VIE N'EST PLUS SUIVIE, MÊME SI `statut` DIT « VIVANTE ».
    reg = changer(reg0, OBS, {"etat_vie": "VECUE-PUIS-ARCHIVEE"})
    poser(reg)
    cd, od, _s = lancer(base, DET)
    poser(reg, un_signal)
    ct, ot, st = lancer(base, TEN)
    suivies = od.split("fiches suivies : ", 1)[1].split("·")[0] if "fiches suivies : " in od else ""
    ok = (cd == 0 and QA in suivies and OBS not in suivies and ct == 0
          and ("horizon lu au registre · %s" % OBS) not in ot
          and {p["strategie"] for p in positions_lues()} == {QA})
    dire("K2 etat_vie VECUE-PUIS-ARCHIVEE, statut « VIVANTE » : la fiche n'est plus suivie", ok,
         "det %d · suivies %r · teneur %d · %s" % (cd, suivies, ct, ot[-300:]))

    # K3 — ISOLATION : l'horizon illisible de C5E10-QA-V1 ne coupe que sa ligne ; C5E10-OBS-V1 reçoit le signal, code 0,
    # sortie du pas fiches_mises_a_part=1, la fiche nommée.
    poser(changer(reg0, QA, {"horizon": "abc"}), un_signal)
    ct, ot, st = lancer(base, TEN)
    ok = (ct == 0 and st.get("fiches_mises_a_part") == "1" and QA in ot and "MISE(S) A PART" in ot
          and {p["strategie"] for p in positions_lues()} == {OBS})
    dire("K3 horizon illisible sur une fiche : elle seule est mise à part, l'autre tourne, code 0, sortie 1", ok,
         "teneur %d · sortie %s · %s" % (ct, st, ot[-400:]))

    # K4 — ISOLATION : une fiche refusée par la garde (entrée « CLOSE », injouable) est mise à part et COMPTÉE.
    poser(changer(reg0, QA, {"entree": "CLOSE"}), un_signal)
    ct, ot, st = lancer(base, TEN)
    ok = (ct == 0 and st.get("fiches_mises_a_part") == "1" and ("FICHE %s REFUSEE PAR LE JUGE" % QA) in ot
          and {p["strategie"] for p in positions_lues()} == {OBS})
    dire("K4 fiche refusée par la garde : mise à part, comptée dans la sortie, l'autre tourne", ok,
         "teneur %d · sortie %s · %s" % (ct, st, ot[-300:]))

    # K4b — un soir ordinaire : la sortie vaut 0 (le pas rouge ne tourne pas).
    poser(reg0, un_signal)
    ct, ot, st = lancer(base, TEN)
    dire("K4b soir ordinaire : fiches_mises_a_part=0, code 0", ct == 0 and st.get("fiches_mises_a_part") == "0",
         "teneur %d · sortie %s" % (ct, st))

    # K5 — LE PAS ROUGE EXISTE ET A LA BONNE FORME (garde partagée du 14-11-2026).
    sys.path.insert(0, os.path.join(base, "tests"))
    try:
        import importlib
        G = importlib.import_module("GARDE_DU_PAS_ROUGE")
        importlib.reload(G)
        manques = G.garde_du_pas_rouge(open(os.path.join(base, YML), encoding="utf-8").read(),
                                       "fiches_mises_a_part", TEN)
    finally:
        sys.path.pop(0)
    dire("K5 le pas « Rougir si une fiche suivie a ete mise a part » rougit sur fiches_mises_a_part", not manques, manques)

    # K6 — RADAR PAR FICHE. (a) une position de C5E10-OBS-V1 aux seuils de C5 et une position d'une fiche d'essai à
    # +6 % / -3 % (copie de la vraie ligne de C5E10-OBS-V1, état LABO) : conformes, aucun ❌ ; (b) une position de
    # C5E10-QA-V1 dont l'objectif est à +5 % : ❌ critique, nommée.
    reg = ajouter_copie(reg0, OBS, "ESSAI-E8-SEUILS", {"nom": "ESSAI E8 SEUILS", "tp": "+6.0%", "sl": "-3.0%",
                                                       "etat_vie": "LABO", "statut": ""})
    poser(reg, positions=[position(OBS, VALEUR, 30.0, 31.2, 29.25),
                          position("ESSAI-E8-SEUILS", "TOTALENERGIES", 50.0, 53.0, 48.5)])
    cr, orad, _s = lancer(base, RAD)
    l11 = [l for l in orad.splitlines() if "11-Positions" in l and "TP/SL" in l]
    ok = cr == 0 and l11 and all(l.startswith("✅") for l in l11) and any("ESSAI-E8-SEUILS +6.0 %" in l for l in l11)
    dire("K6a radar : chaque position jugée sur les seuils de SA fiche (C5 et +6 % / -3 %), aucune alerte", ok,
         "radar %d · %s" % (cr, l11))
    poser(reg, positions=[position(QA, VALEUR, 40.0, 42.0, 39.0)])
    cr, orad, _s = lancer(base, RAD)
    l11 = [l for l in orad.splitlines() if "11-Positions" in l and "TP/SL" in l]
    ok = any(l.startswith("❌") and "INCOHÉRENTS" in l and VALEUR in l for l in l11)
    dire("K6b radar : un objectif à +5 % sur une fiche à +4 % rougit, position nommée", ok, "radar %d · %s" % (cr, l11))

    # K7 — L'ÉTAT DE VIE « SUSPENDUE » N'EST PAS SUIVI (table de R-513 : pas d'affichage « VIVANTE »).
    reg = changer(changer(reg0, OBS, {"etat_vie": "SUSPENDUE"}), QA, {"etat_vie": "PRODUCTION"})
    poser(reg, un_signal)
    ct, ot, st = lancer(base, TEN)
    ok = ct == 0 and {p["strategie"] for p in positions_lues()} == {QA}
    dire("K7 PRODUCTION suivie, SUSPENDUE non suivie", ok, "teneur %d · %s" % (ct, ot[-300:]))

    # K8 — UNIVERS VIDE : une fiche QA sans univers n'est pas suivie (elle ne déclare aucune valeur) ; elle n'est donc
    # ni servie ni comptée parmi les fiches mises à part (relecture c81c1457, T1).
    poser(changer(reg0, QA, {"univers": ""}), un_signal)
    ct, ot, st = lancer(base, TEN)
    ok = (ct == 0 and st.get("fiches_mises_a_part") == "0" and {p["strategie"] for p in positions_lues()} == {OBS}
          and QA not in ot)
    dire("K8 univers vide : fiche QA non suivie, non comptée, l'autre tourne", ok,
         "teneur %d · sortie %s · %s" % (ct, st, ot[-300:]))

    # K9 — L'ÉTAT DE VIE SE LIT SANS BLANCS NI CASSE : « qa » entouré d'espaces reste QA (relecture c81c1457, T2 ;
    # même normalisation que le radar, `.strip().upper()`).
    poser(changer(reg0, QA, {"etat_vie": " qa "}), un_signal)
    ct, ot, st = lancer(base, TEN)
    ok = ct == 0 and {p["strategie"] for p in positions_lues()} == {QA, OBS}
    dire("K9 etat_vie « qa » entouré de blancs : la fiche reste suivie", ok, "teneur %d · %s" % (ct, ot[-300:]))

    open(os.path.join(base, REG), "w", encoding="utf-8").write(reg0)
    open(os.path.join(base, POS), "w", encoding="utf-8").write(pos0)
    return res


# (nom, fichier saboté, texte avant, texte après) — chaque texte « avant » doit exister une seule fois.
SABOTAGES = [
    ("S1 le critère relit statut", CTR,
     '    etat = (fiche.get("etat_vie") or "").strip().upper()\n    return etat in ETATS_SUIVIS_PAR_LE_SOIR and',
     '    etat = "QA" if "VIVANTE" in (fiche.get("statut") or "") else ""\n    return etat in ETATS_SUIVIS_PAR_LE_SOIR and'),
    ("S2 SUSPENDUE ajoutée aux états suivis", CTR, 'ETATS_SUIVIS_PAR_LE_SOIR = ("QA", "PRODUCTION")',
     'ETATS_SUIVIS_PAR_LE_SOIR = ("QA", "PRODUCTION", "SUSPENDUE")'),
    ("S3 le détecteur garde sa copie sur statut", DET, "        if not suivie_par_le_soir(f):\n",
     "        if \"VIVANTE\" not in (f.get(\"statut\") or \"\") or not (f.get(\"univers\") or \"\").strip():\n"),
    ("S4 le teneur garde sa copie sur statut", TEN, "        if suivie_par_le_soir(ligne):\n",
     "        if \"VIVANTE\" in (ligne.get(\"statut\") or \"\") and (ligne.get(\"univers\") or \"\").strip():\n"),
    ("S5 une fiche mise à part arrête tout le soir", TEN,
     "    if _mises_a_part:\n        print(", "    if _mises_a_part:\n        return 1\n        print("),
    ("S6 un refus de la garde n'est pas compté", TEN,
     "                _mises_a_part.append((ligne[\"id\"], _refus))\n", ""),
    ("S7 sortie du pas tue", TEN, "    _ligne_du_pas += \"\\nfiches_mises_a_part=%d\" % len(_mises_a_part)\n", ""),
    ("S8 pas rouge retiré", YML, "        if: always() && steps.tenir_les_positions.outputs.fiches_mises_a_part != '' "
     "&& steps.tenir_les_positions.outputs.fiches_mises_a_part != '0'\n",
     "        if: always() && steps.tenir_les_positions.outputs.fiches_mises_a_part == 'jamais'\n"),
    ("S9 le radar revient aux seuils de C5", RAD, "            tp_f, sl_f, _h = J.lecture_du_soir(PROJ, fiche)\n",
     "            tp_f, sl_f, _h = 0.04, 0.025, 20\n"),
    ("S11 univers vide accepté", CTR,
     '    return etat in ETATS_SUIVIS_PAR_LE_SOIR and bool((fiche.get("univers") or "").strip())',
     '    return etat in ETATS_SUIVIS_PAR_LE_SOIR'),
    ("S12 état de vie lu sans normalisation", CTR,
     '    etat = (fiche.get("etat_vie") or "").strip().upper()\n', '    etat = (fiche.get("etat_vie") or "")\n'),
    ("S10 le radar ne compare plus", RAD, "        if abs(tp - pe*(1+tp_f)) > 0.01 or abs(sl - pe*(1-sl_f)) > 0.01:\n",
     "        if False:\n"),
]


def main():
    """Joue les cas, puis les sabotages ; affiche et rend le code.
    ① RÔLE — Le programme. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — RACINE, SABOTER. ④ CONDITIONS D'ENTRÉE —
    voir ④ du fichier. ⑤ SORTIE — UNE valeur, le code. [rend: 1] ⑥ TRAITEMENT — copier, lire les vrais fichiers, jouer,
    saboter un à un (fichiers remis à l'octet avant chaque sabotage), effacer la copie. ⑦ UNITÉ — —. ⑧ POURQUOI — voir
    ⑧ du fichier. ⑨ CE QUI CLOCHE — un texte « avant » introuvable rend le sabotage NON JOUÉ, compté rouge (R-734).
    ⑩ EFFET — écrit et efface la copie. ⑪ TERMINAISON — rend la main avec le code. [sort: non]"""
    try:
        base = copier()
    except OSError as e:
        print("CODE 2 — copie impossible : %s" % e)
        return 2
    try:
        reg0 = open(os.path.join(base, REG), encoding="utf-8").read()
        pos0 = open(os.path.join(base, POS), encoding="utf-8").read()
        origines = {f: open(os.path.join(base, f), encoding="utf-8").read() for f in (CTR, DET, TEN, RAD, YML)}
        rouge = False
        res = les_cas(base, reg0, pos0)
        for nom, ok, preuve in res:
            print("  %s %s" % ("✅" if ok else "❌", nom))
            if not ok:
                print("       " + preuve.replace("\n", " | "))
                rouge = True
        if SABOTER:
            for nom, fichier, avant, apres in SABOTAGES:
                for f, t in origines.items():
                    open(os.path.join(base, f), "w", encoding="utf-8").write(t)
                t = origines[fichier]
                if t.count(avant) != 1:
                    print("  ❌ %s NON JOUÉ — texte visé trouvé %d fois" % (nom, t.count(avant)))
                    rouge = True
                    continue
                open(os.path.join(base, fichier), "w", encoding="utf-8").write(t.replace(avant, apres))
                rouges = [n.split(" ")[0] for n, ok, _p in les_cas(base, reg0, pos0) if not ok]
                print("  %s %s → rougissent : %s" % ("✅" if rouges else "❌", nom, ", ".join(rouges) or "AUCUNE"))
                rouge = rouge or not rouges
            for f, t in origines.items():
                open(os.path.join(base, f), "w", encoding="utf-8").write(t)
        print("VERDICT : %s" % ("ROUGE" if rouge else "VERT"))
        return 1 if rouge else 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
