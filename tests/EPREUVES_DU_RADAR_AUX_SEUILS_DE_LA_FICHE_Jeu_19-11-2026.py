#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_RADAR_AUX_SEUILS_DE_LA_FICHE_Jeu_19-11-2026.py — Jeu 19-11-2026 (Paris) — le maillon 10 du radar
recalcule chaque trade clôturé aux seuils de SA fiche (BACKLOG A-928, point D2). Simulation uniquement — aucun ordre
réel.

LE SENS EN TÊTE. Le maillon 10 de `programmes/audit_ecosysteme.py` reprend chaque trade du journal et le refait. Jusqu'au
19-11-2026, il le refaisait aux seuils de C5 écrits dans le module (+4 % / −2,5 % / 20 séances), quelle que soit la
stratégie du trade. Le relecteur (RELU e5113b94, défaut D2) l'a mesuré sur les deux vrais signaux RSI du 2026-01-21,
LVMH et STELLANTIS : une fiche à +6 % / −3 % ferait rougir le radar de 499 € sur un trade JUSTE (fausse alerte), et un
teneur qui appliquerait par erreur les seuils de C5 resterait VERT. Il ne restait vert que par coïncidence :
IND-001-RETEST porte au registre les mêmes seuils que C5. La réparation : le radar lit l'objectif, le stop et
l'horizon de LA FICHE du trade par `lecture_du_soir` du juge des stratégies, la lecture que le teneur des positions
exécute (R-708 : deux implémentations d'une même chose divergent toujours).

Le « trade juste » de chaque cas est fabriqué PAR LE TENEUR, pas par le radar : `vendre`, `prix_de_convention` et
`pnl_net` de `programmes/MODULE_POSITIONS.py`, aux seuils de la fiche. Le radar, lui, refait le trajet par
`_c5e10_sortie` (calcul de la vente indépendant, BACKLOG A-208 ⑤). Les deux doivent tomber d'accord. RÉSERVE
(RELU 37f397227, D-R1) : le radar et le teneur lisent les seuils par la MÊME fonction, `lecture_du_soir` (R-708) ; une
erreur de cette lecture les rend faux tous les deux et le radar reste vert. Cette épreuve ne peut pas la voir : seule
la vente est recalculée indépendamment.

CAS :
  R0 vraie ligne (R-732) : les montants du teneur à +6 / −3 sont ceux mesurés par le relecteur, à 1 € près
     (LVMH −3 696, STELLANTIS −3 296 ; aux seuils de C5 : −3 196 et −2 796).
  R1 fiche à +6 / −3, trades justes → maillon 10 VERT.
  R2 fiche à +6 / −3, journal écrit aux seuils de C5 (teneur fautif) → maillon 10 ROUGE, les deux trades nommés.
  R3 trade dont la stratégie n'a pas de fiche → maillon 10 ROUGE, jamais vert.
  R4 fiche à +30 / −30 / 3 séances, trades justes (sortie à l'échéance) → maillon 10 VERT : l'horizon de la fiche est lu.
  R5 fiche à +1 / −30 / 20, trades justes (sortie à l'objectif) → maillon 10 VERT : l'objectif de la fiche est lu.
  R6 fiche à stop illisible (refusée par `lecture_du_soir`), journal aux seuils de C5 → ROUGE, « fiche refusée » nommé
     (RELU 37f397227, D-R2 : sans ce cas, un retour silencieux aux seuils de C5 passait toutes les épreuves).
  R7 fiche à +6 / −3, journal aux seuils de C5 → ROUGE, et le message nomme la cause probable « fiche modifiée après
     l'achat (interdit par A-754/A-768) ? » DANS LA LIGNE DE LVMH, nommément, avec « seuil vendu −2.50 % ≠ fiche du
     jour −3.00 % » (RELU 37f397227, point ② ; RELU 45677132d, D-T1 : la cause portée par STELLANTIS seule suffisait).
  R8 fiche à +6 / −3, trades vendus aux BONS seuils mais montant de LVMH faux de 500 € → ROUGE, et la cause n'est PAS
     nommée : le cas qui doit échouer, sans lequel un message qui accuse toujours la fiche passerait.
  R9 SORTIE À L'OBJECTIF (RELU 45677132d, D-T1, ajouté Ven 20-11-2026) : journal juste à +1 / −30 / 20, fiche du jour
     à +2 / −30 / 20 → ROUGE, et la ligne de STELLANTIS porte « seuil vendu +1.00 % ≠ fiche du jour +2.00 % » et la
     cause. Vrai signal RSI du 2026-01-21, vrais cours (fichier Google) : achat à l'Open du 2026-01-22, 8,44 € ;
     objectif +1 % = 8,5244 €, touché le 2026-02-03 (plus haut 8,56, ouverture 8,40 : pas de saut) ; le teneur rend
     « TP », exigé avant le cas. LVMH, à l'échéance aux deux réglages (plus haut 598 < 602,87), n'est pas en écart.
  R10 SAUT D'OUVERTURE SOUS LE STOP (SL_GAP) (RELU 45677132d, D-T1, ajouté Ven 20-11-2026) : journal juste à +6 / −3,
     fiche du jour aux seuils de C5 (+4 / −2,5) → ROUGE, et la ligne de LVMH porte « seuil vendu −3.00 % ≠ fiche du jour
     −2.50 % » et la cause. Le teneur rend « SL_GAP » pour LVMH à +6 / −3, exigé avant le cas : le prix de convention
     reste le stop, pas l'ouverture.

① RÔLE — Jouer R0 à R10 ; avec `--saboter`, prouver que chaque cas mord : chaque sabotage retire une partie de la
  correction et doit faire rougir au moins un cas ; les fichiers sont remis à l'octet avant chaque sabotage.
② CONTEXTE D'APPEL — À la main : `python3 -I -B tests/EPREUVES_DU_RADAR_AUX_SEUILS_DE_LA_FICHE_Jeu_19-11-2026.py
  <racine> [--saboter]` ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis « --saboter ».
③ ENTRÉE — `<racine>` : un clone du dépôt, jamais modifié (tout se joue sur une copie sous /dev/shm ou /tmp).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/ (radar, module de C5, juge, module des positions, contrat),
  donnees/ (registre avec IND-001-RETEST, cours avec les séances de janvier 2026, barème des frais, valeurs taxées).
⑤ SORTIE — UNE valeur, le code de sortie : 0 si tous les cas passent (et, avec --saboter, si chaque sabotage fait
  rougir au moins un cas) ; 1 sinon ; 2 si la copie n'a pas pu être faite. [rend: 1]
⑥ TRAITEMENT — ① copier la racine sans .git, etudes/, archives/, prompts_taches/, donnees/sources_*, ni PILOTE_SOCLE* ;
  garder des fichiers de cours les seules séances depuis le 2025-12-01 · ② fabriquer les journaux de cas par le teneur ·
  ③ pour chaque cas, poser registre et journal, lancer le radar en ligne de commande, lire ses lignes [10-Trades] ;
  R7, R9 et R10 exigent leur texte dans le MORCEAU du message propre à la valeur nommée (« VALEUR 2026-01-22 : … »,
  morceaux séparés par « | ») ; R9 et R10 exigent d'abord le motif rendu par le teneur (TP, SL_GAP) ·
  ④ avec --saboter, chaque sabotage, dont Y1, Y2, Y3 sur `_cause_de_l_ecart` (RELU 45677132d, D-T1).
⑦ UNITÉ — Montants en euros ; seuils en FRACTIONS (0,06 pour « +6.0% ») ; horizon en séances de bourse.
⑧ POURQUOI — Boucle R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration. Cours
  récents seulement : aucune séance de 2000 à 2023 n'est lue (les fichiers de cours du dépôt commencent en 2024 ;
  donnees/sources_* n'est pas copié).
⑨ CE QUI CLOCHE — ① Une fiche modifiée après le trade et un teneur fautif donnent le même journal : R2 et R7 jouent
  les mêmes fichiers ; le message nomme les deux causes. ② Un horizon « aucune » n'est pas joué : le radar le refuse (TypeError comptée en écart). ③ Les cas
  dépendent de la fiche IND-001-RETEST du registre et des séances de janvier 2026 des fichiers de cours. ④ Une
  erreur de `lecture_du_soir` commune au radar et au teneur n'est pas jouée : elle est invisible au radar (réserve
  ci-dessus). ⑤ R9 dépend des séances de février 2026 de STELLANTIS (objectif touché le 2026-02-03) ; R10 dépend du
  saut d'ouverture de LVMH du 2026-01-28 (ouverture 556 sous le stop). Si le teneur rend un autre motif, le cas rougit
  par sa condition préalable, sans lancer le radar. ⑥ Un saut au-dessus de l'objectif (TP_GAP) n'est pas joué ici :
  la branche « TP » est la même ligne (motif commençant par « TP ») ; le relecteur l'a mesurée sur un vrai trade
  (BUREAU_VERITAS, RELU 45677132d ①). ⑦ Les morceaux du message se découpent sur « | » : un motif de refus qui en
  contiendrait un fausserait le découpage (aucun aujourd'hui).
⑩ EFFET — Écrit seulement dans son dossier temporaire, qu'il efface à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement du radar est borné à 600 s. [sort: oui — code]
"""
import csv, importlib.util, io, os, shutil, subprocess, sys, tempfile

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
SABOTER = "--saboter" in sys.argv
RAD = "programmes/audit_ecosysteme.py"
C5 = "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"
CTR = "programmes/CONTRATS_DES_FICHIERS.py"
POSI = "programmes/MODULE_POSITIONS.py"
JOU = "donnees/claude_journal_trades.csv"
COURS = ("donnees/cac40_ohlcv.csv", "donnees/claude_cours_nouveaux.csv", "donnees/cours_maitre.csv")
DEPUIS = "2025-12-01"
IND = "IND-001-RETEST"
ACHAT = "2026-01-22"          # Open J+1 des signaux RSI du 2026-01-21 (LVMH, STELLANTIS)
VALEURS = ("LVMH", "STELLANTIS")
MOTIFS = {}          # (tp, sl, horizon, valeur) → motif de sortie rendu par le teneur, affiché
CAUSE = "fiche modifiée après l'achat (interdit par A-754/A-768) ?"   # libellé du maillon 10 (RELU 37f397227 ②)
RELECTEUR = {(0.06, 0.03): {"LVMH": -3696.0, "STELLANTIS": -3296.0},
             (0.04, 0.025): {"LVMH": -3196.0, "STELLANTIS": -2796.0}}   # RELU e5113b94, arrondis à l'euro


def charger(base, chemin, nom):
    """Charge un programme de la copie par son chemin.
    ① RÔLE — Employer les fonctions du dépôt, jamais une copie (R-708). ② CONTEXTE D'APPEL — `contrat`,
    `journal_juste`. ③ ENTRÉE — `base`, `chemin` relatif, `nom` du module. ④ CONDITIONS D'ENTRÉE — le fichier existe ;
    programmes/ de la copie est en tête de sys.path. ⑤ SORTIE — UNE valeur, le module. [rend: 1] ⑥ TRAITEMENT —
    spec, module, exécution. ⑦ UNITÉ — —. ⑧ POURQUOI — les noms datés ne s'importent pas. ⑨ CE QUI CLOCHE — charger,
    c'est exécuter. ⑩ EFFET — exécute le fichier. ⑪ TERMINAISON — rend la main ; lève ce que lève le fichier.
    [sort: non]"""
    sp = importlib.util.spec_from_file_location(nom, os.path.join(base, chemin))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def copier():
    """Copie la racine dans un dossier jetable, cours récents seulement.
    ① RÔLE — Ne jamais jouer sur le dépôt. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — RACINE. ④ CONDITIONS D'ENTRÉE — de
    la place sous /dev/shm ou le dossier temporaire. ⑤ SORTIE — UNE valeur, le chemin de la copie. [rend: 1]
    ⑥ TRAITEMENT — ① copier sans .git, etudes/, archives/, prompts_taches/, donnees/sources_*, ni PILOTE_SOCLE* ;
    ② réécrire chaque fichier de COURS en ne gardant que les séances depuis DEPUIS. ⑦ UNITÉ — —. ⑧ POURQUOI — les
    programmes du circuit écrivent tous ; prompts_taches/ et PILOTE_SOCLE* ne doivent pas être recopiés ; les cours
    anciens ne servent à aucun cas. ⑨ CE QUI CLOCHE — une copie laissée par un arrêt brutal reste. ⑩ EFFET — écrit la
    copie. ⑪ TERMINAISON — rend la main ; lève OSError. [sort: non]"""
    base = os.path.join("/dev/shm" if os.path.isdir("/dev/shm") else tempfile.gettempdir(),
                        "epreuves_radar_fiche_%d" % os.getpid())

    def ignorer(d, noms):
        out = [n for n in noms if n.startswith("PILOTE_SOCLE")]
        if d == RACINE:
            out += [n for n in noms if n in (".git", "etudes", "archives", "prompts_taches")]
        if d == os.path.join(RACINE, "donnees"):
            out += [n for n in noms if n.startswith("sources_")]
        return out
    shutil.copytree(RACINE, base, ignore=ignorer)
    for f in COURS:
        p = os.path.join(base, f)
        if os.path.exists(p):
            lignes = open(p, encoding="utf-8").read().splitlines(True)
            garde = [lignes[0]] + [l for l in lignes[1:] if l.split(",")[1:2] and l.split(",")[1] >= DEPUIS]
            open(p, "w", encoding="utf-8").writelines(garde)
    return base


def changer(t, ident, valeurs):
    """Rend le texte du registre où la DERNIÈRE ligne de `ident` porte les `valeurs` ({colonne: texte}).
    ① RÔLE — Fabriquer un registre de cas. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `t` : texte du registre ·
    `ident` · `valeurs`. ④ CONDITIONS D'ENTRÉE — `ident` présent, colonnes dans l'en-tête. ⑤ SORTIE — UNE valeur, le
    texte. [rend: 1] ⑥ TRAITEMENT — lire en CSV, changer les cases, réécrire. ⑦ UNITÉ — —. ⑧ POURQUOI — la dernière
    ligne d'un identifiant fait foi (n°83). ⑨ CE QUI CLOCHE — les guillemets sont réécrits à la manière du module csv.
    ⑩ EFFET — Aucun. ⑪ TERMINAISON — lève ValueError si l'identifiant ou une colonne manque. [sort: non]"""
    lignes = list(csv.reader(io.StringIO(t)))
    rang = max(i for i, l in enumerate(lignes) if l and l[0] == ident)
    for col, v in valeurs.items():
        lignes[rang][lignes[0].index(col)] = v
    s = io.StringIO()
    csv.writer(s, lineterminator="\n").writerows(lignes)
    return s.getvalue()


def series(base):
    """Rend {valeur: séances triées} pour VALEURS, lues dans les fichiers de cours de la copie (les récents).
    ① RÔLE — Donner au teneur la série où il vend. ② CONTEXTE D'APPEL — `journal_juste`. ③ ENTRÉE — `base`.
    ④ CONDITIONS D'ENTRÉE — colonnes valeur, date, open, high, low, close. ⑤ SORTIE — UNE valeur, le dictionnaire.
    [rend: 1] ⑥ TRAITEMENT — l'historique Google puis les cours nouveaux, comme le radar (le second écrase le premier à
    date égale), triés par date. ⑦ UNITÉ — euros. ⑧ POURQUOI — la même série que celle du maillon 10. ⑨ CE QUI CLOCHE —
    l'assemblage est récrit ici (quatre lignes) : le radar ne l'expose pas en fonction. ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    d = {}
    for f in COURS[:2]:
        for r in csv.DictReader(open(os.path.join(base, f), encoding="utf-8-sig")):
            if r.get("valeur") in VALEURS:
                d.setdefault(r["valeur"], {})[r["date"]] = {"date": r["date"], **{k: float(r[k]) for k in
                                                                                ("open", "high", "low", "close")}}
    return {v: [s[k] for k in sorted(s)] for v, s in d.items()}


def journal_juste(base, entete, tp, sl, horizon, strategie=IND):
    """Rend (texte du journal, montants) des trades LVMH et STELLANTIS achetés le 2026-01-22, chiffrés PAR LE TENEUR.
    ① RÔLE — Le « trade juste » d'un cas. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `base`, `entete` (première ligne du
    vrai journal), `tp`, `sl` (fractions), `horizon` (séances), `strategie`. ④ CONDITIONS D'ENTRÉE — le module des
    positions de la copie porte `vendre`, `prix_de_convention`, `pnl_net`. ⑤ SORTIE — DEUX valeurs : le texte CSV,
    {valeur: montant de convention}. [rend: 2] ⑥ TRAITEMENT — pour chaque valeur : `vendre` en « vendre », prix de
    convention, `pnl_net` au barème REEL ; une ligne au contrat du journal. ⑦ UNITÉ — euros. ⑧ POURQUOI — le juste est
    ce que le teneur exécute, pas ce que le radar recalcule. ⑨ CE QUI CLOCHE — `vendre` attrape les sauts d'ouverture
    (SL_GAP) ; le journal porte le montant de CONVENTION, celui que le radar compare. ⑩ EFFET — exécute le module des
    positions de la copie. ⑪ TERMINAISON — rend la main ; lève si une séance manque. [sort: non]"""
    sys.path.insert(0, os.path.join(base, "programmes"))
    P = charger(base, POSI, "positions_pour_radar_fiche")
    S = series(base)
    champs = next(csv.reader([entete]))
    out, montants = io.StringIO(), {}
    w = csv.DictWriter(out, fieldnames=champs, lineterminator="\n")
    w.writeheader()
    for v in VALEURS:
        j = [k for k, b in enumerate(S[v]) if b["date"] == ACHAT][0]
        r = P.vendre(S[v], j, {"tp": tp, "sl": sl, "horizon": horizon}, "vendre")
        px_c = P.prix_de_convention(r["motif"], r["px"], r["objectif"], r["stop"])
        net = P.pnl_net(r["pe"], px_c, v, ACHAT, r["date_sortie"], "REEL")
        montants[v] = net
        MOTIFS[(tp, sl, horizon, v)] = r["motif"]
        w.writerow({**{c: "" for c in champs}, "strategie": strategie, "valeur": v, "date_entree": ACHAT,
                    "prix_entree": "%.4f" % r["pe"], "date_sortie": r["date_sortie"], "prix_sortie": "%.4f" % r["px"],
                    "motif_sortie": r["motif"], "pnl_net_eur": "%.2f" % net, "prix_sortie_convention": "%.4f" % px_c,
                    "pnl_net_convention_eur": "%.2f" % net, "comptabilite": "un_jeton", "bareme_reel": "REEL",
                    "bareme_convention": "REEL"})
    return out.getvalue(), montants


def radar(base):
    """Lance le radar sur la copie ; rend ses lignes [10-Trades].
    ① RÔLE — Jouer le maillon 10 comme le circuit. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `base`. ④ CONDITIONS
    D'ENTRÉE — `python3` dans /usr/bin ou /bin. ⑤ SORTIE — UNE valeur, la liste des lignes. [rend: 1] ⑥ TRAITEMENT —
    lancer `python3 -I -B programmes/audit_ecosysteme.py <copie>`, environnement vidé ; garder les lignes qui portent
    « [10-Trades] ». ⑦ UNITÉ — —. ⑧ POURQUOI — l'environnement vidé évite qu'un jeton de l'appelant n'entre. ⑨ CE QUI
    CLOCHE — un délai dépassé rend une seule ligne « délai dépassé », jugée ni verte ni rouge. ⑩ EFFET — ce qu'écrit le
    radar, dans la copie. ⑪ TERMINAISON — borné à 600 s. [sort: non]"""
    env = {"PATH": "/usr/bin:/bin", "HOME": tempfile.gettempdir()}
    try:
        p = subprocess.run([sys.executable, "-I", "-B", RAD, base], cwd=base, env=env,
                           capture_output=True, text=True, timeout=600)
        return [l for l in (p.stdout + p.stderr).splitlines() if "[10-Trades]" in l]
    except subprocess.TimeoutExpired:
        return ["délai dépassé"]


def morceau(lignes, valeur):
    """Rend le morceau du message [10-Trades] propre à `valeur` (achat ACHAT), ou "".
    ① RÔLE — Exiger une cause NOMMÉMENT sur une valeur (RELU 45677132d, D-T1). ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — `lignes` : les lignes [10-Trades] du radar · `valeur` : un nom de VALEURS. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur, le texte du morceau, "" si aucun. [rend: 1] ⑥ TRAITEMENT — découper chaque ligne sur
    « | » ; rendre le premier morceau qui contient « VALEUR 2026-01-22 : ». ⑦ UNITÉ — —. ⑧ POURQUOI — le radar met
    tous les écarts dans UNE ligne ; chercher un texte dans la ligne entière laissait la cause de STELLANTIS couvrir
    LVMH. ⑨ CE QUI CLOCHE — voir ⑨ ⑦ du fichier. ⑩ EFFET — Aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    cle = "%s %s :" % (valeur, ACHAT)
    return next((m for l in lignes for m in l.split(" | ") if cle in m), "")


def les_cas(base, reg0, journaux):
    """Joue R1 à R10 sur `base` ; rend la liste (nom, vrai/faux, preuve).
    ① RÔLE — Les cas joués par le radar. ② CONTEXTE D'APPEL — `main`, une fois puis une fois par sabotage.
    ③ ENTRÉE — `base`, `reg0` (le vrai registre), `journaux` ({nom: texte}) ; `jouer` reçoit aussi `aussi` (textes
    exigés dans une ligne [10-Trades]), `jamais` (textes interdits dans toutes), `chez` ({valeur: textes exigés dans
    SON morceau}) et `motif` ((clé de MOTIFS, motif attendu du teneur), condition préalable). ④ CONDITIONS D'ENTRÉE —
    celles du fichier ; MOTIFS rempli par `journal_juste`.
    ⑤ SORTIE — UNE valeur, la liste. [rend: 1] ⑥ TRAITEMENT — chaque cas vérifie d'abord `motif` (faux : le cas
    rougit, le radar n'est pas lancé), pose registre et journal, lance le radar,
    juge ses lignes [10-Trades] : VERT = une ligne ✅ et aucune ❌ ; ROUGE = une ligne ❌ et aucune ✅ ; puis `aussi`,
    `jamais` et `chez`. ⑦ UNITÉ — —.
    ⑧ POURQUOI — voir ⑧ du fichier. ⑨ CE QUI CLOCHE — voir ⑨ du fichier. ⑩ EFFET — écrit dans la copie.
    ⑪ TERMINAISON — celle du radar. [sort: non]"""
    from CONTRATS_DES_FICHIERS import REGISTRE_DES_STRATEGIES as REG
    res = []

    def jouer(nom, reglage, journal, attendu, aussi=(), jamais=(), chez=None, motif=None):
        if motif is not None and MOTIFS.get(motif[0]) != motif[1]:
            res.append((nom, False, "condition préalable : le teneur rend %r pour %s, attendu %r"
                        % (MOTIFS.get(motif[0]), motif[0], motif[1])))
            return
        open(os.path.join(base, REG), "w", encoding="utf-8").write(
            changer(reg0, IND, {"tp": reglage[0], "sl": reglage[1], "horizon": reglage[2]}))
        open(os.path.join(base, JOU), "w", encoding="utf-8").write(journal)
        l = radar(base)
        vert = any(x.startswith("✅") for x in l) and not any(x.startswith("❌") for x in l)
        rouge = any(x.startswith("❌") for x in l) and not any(x.startswith("✅") for x in l)
        ok = ((vert if attendu == "vert" else rouge) and all(any(a in x for x in l) for a in aussi)
              and not any(a in x for x in l for a in jamais)
              and all(a in morceau(l, v) for v, textes in (chez or {}).items() for a in textes))
        res.append((nom, ok, " | ".join(l)[-600:]))
    jouer("R1 fiche +6/−3, trades justes → vert", ("+6.0%", "-3.0%", "20"), journaux["juste_6_3"], "vert")
    jouer("R2 fiche +6/−3, journal aux seuils de C5 → rouge", ("+6.0%", "-3.0%", "20"), journaux["c5"], "rouge",
          aussi=("LVMH", "STELLANTIS"))
    jouer("R3 fiche introuvable → rouge", ("+6.0%", "-3.0%", "20"), journaux["sans_fiche"], "rouge",
          aussi=("fiche introuvable",))
    jouer("R4 fiche +30/−30/3, trades justes → vert", ("+30.0%", "-30.0%", "3"), journaux["juste_h3"], "vert")
    jouer("R5 fiche +1/−30/20, trades justes → vert", ("+1.0%", "-30.0%", "20"), journaux["juste_tp1"], "vert")
    jouer("R6 fiche à stop illisible (refusée), journal aux seuils de C5 → rouge", ("+6.0%", "illisible", "20"),
          journaux["c5"], "rouge", aussi=("fiche refusée",))
    jouer("R7 fiche +6/−3, journal aux seuils de C5 → rouge, cause nommée sur LVMH", ("+6.0%", "-3.0%", "20"),
          journaux["c5"], "rouge", aussi=(CAUSE,),
          chez={"LVMH": ("seuil vendu −2.50 % ≠ fiche du jour −3.00 %", CAUSE)})
    jouer("R8 fiche +6/−3, montant faux aux bons seuils → rouge, cause NON nommée", ("+6.0%", "-3.0%", "20"),
          journaux["montant_faux"], "rouge", aussi=("LVMH",), jamais=(CAUSE,))
    jouer("R9 sortie à l'objectif : journal +1/−30/20, fiche +2/−30/20 → rouge, cause nommée sur STELLANTIS",
          ("+2.0%", "-30.0%", "20"), journaux["juste_tp1"], "rouge",
          chez={"STELLANTIS": ("seuil vendu +1.00 % ≠ fiche du jour +2.00 %", CAUSE)},
          motif=((0.01, 0.30, 20, "STELLANTIS"), "TP"))
    jouer("R10 saut sous le stop : journal +6/−3, fiche aux seuils de C5 → rouge, cause nommée sur LVMH",
          ("+4.0%", "-2.5%", "20"), journaux["juste_6_3"], "rouge",
          chez={"LVMH": ("seuil vendu −3.00 % ≠ fiche du jour −2.50 %", CAUSE)},
          motif=((0.06, 0.03, 20, "LVMH"), "SL_GAP"))
    return res


# (nom, fichier saboté, texte avant, texte après) — chaque texte « avant » doit exister une seule fois.
SABOTAGES = [
    ("SB1 le radar ne passe plus les seuils de la fiche", RAD,
     "MOD._c5e10_sortie(oh, idx[0] - 1, v, _bar, tp=_reg[0], sl=_reg[1], horizon=_reg[2])",
     "MOD._c5e10_sortie(oh, idx[0] - 1, v, _bar)"),
    ("SB2 une fiche introuvable n'est plus un écart", RAD,
     "                ecarts.append(f\"{v} {d_e} ({_sid or 'sans stratégie'}) : {_refus} — recalcul impossible\")\n",
     "                sans_cours += 1\n"),
    ("SB3 la fonction de sortie ignore l'objectif reçu", C5,
     "    _tp = C5E10_TP if tp is None else tp\n", "    _tp = C5E10_TP\n"),
    ("SB4 la fonction de sortie ignore le stop reçu", C5,
     "    _sl = C5E10_SL if sl is None else sl\n", "    _sl = C5E10_SL\n"),
    ("SB5 la fonction de sortie ignore l'horizon reçu", C5,
     "    _h = C5E10_HORIZON if horizon is None else horizon\n", "    _h = C5E10_HORIZON\n"),
    ("SB6 le radar prend la première fiche venue", RAD,
     "    fiche = next((x for x in (fiches or []) if sid in contrat.noms_d_une_strategie(x)), None)\n",
     "    fiche = next((x for x in (fiches or [])), None)\n"),
    ("X2 une fiche refusée est ramenée aux seuils de C5 en silence (relecteur, D-R2)", RAD,
     "        return None, f\"fiche refusée par la lecture du soir — {e}\"\n",
     "        return (0.04, 0.025, 20), None\n"),
    ("SB7 la cause d'un écart n'est jamais nommée", RAD,
     "    if abs(vendu - fiche) < 0.0005:\n        return \"\"\n    return (",
     "    return \"\"\n    return ("),
    ("SB8 la cause d'un écart est nommée sans comparer les seuils", RAD,
     "    if abs(vendu - fiche) < 0.0005:\n        return \"\"\n    return (",
     "    return ("),
    # RELU 45677132d, D-T1 : ces trois sabotages restaient verts avec R0 à R8 ; R9, R10 et R7 nommément les voient.
    ("Y1 la branche objectif de la cause est muette (relecteur, D-T1)", RAD,
     "            vendu, fiche, signe = pc / pe - 1, float(reglage[0]), \"+\"\n",
     "            return \"\"\n"),
    ("Y2 la branche objectif compare le seuil vendu au stop (relecteur, D-T1)", RAD,
     "            vendu, fiche, signe = pc / pe - 1, float(reglage[0]), \"+\"\n",
     "            vendu, fiche, signe = pc / pe - 1, float(reglage[1]), \"+\"\n"),
    ("Y3 le motif SL_GAP est ignoré par la cause (relecteur, D-T1)", RAD,
     "        elif motif.startswith(\"SL\"):\n",
     "        elif motif == \"SL\":\n"),
]


def main():
    """Fabrique les journaux, joue R0 à R10, puis les sabotages.
    ① RÔLE — Le programme. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — RACINE, SABOTER. ④ CONDITIONS
    D'ENTRÉE — celles du fichier. ⑤ SORTIE — UNE valeur, le code (voir ⑤ du fichier). [rend: 1] ⑥ TRAITEMENT — copier ;
    journaux par le teneur, plus le journal de R8 (montant de LVMH +500 €) ; R0 contre les chiffres du relecteur ;
    R1 à R10 ; avec --saboter, remettre les fichiers à
    l'octet, saboter un à un, exiger un rouge. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — un motif de sabotage
    trouvé 0 ou 2 fois rougit le verdict (voulu : le sabotage doit viser le code livré). ⑩ EFFET — copie effacée à la
    fin. ⑪ TERMINAISON — rend la main. [sort: non]"""
    try:
        base = copier()
    except OSError as e:
        print("CODE 2 — copie impossible : %s" % e)
        return 2
    try:
        sys.path.insert(0, os.path.join(base, "programmes"))
        from CONTRATS_DES_FICHIERS import REGISTRE_DES_STRATEGIES as REG
        reg0 = open(os.path.join(base, REG), encoding="utf-8").read()
        entete = open(os.path.join(base, JOU), encoding="utf-8").readline()
        j63, m63 = journal_juste(base, entete, 0.06, 0.03, 20)
        jc5, mc5 = journal_juste(base, entete, 0.04, 0.025, 20)
        jsf, _ = journal_juste(base, entete, 0.06, 0.03, 20, strategie="IND-999-SANS-FICHE")
        jh3, mh3 = journal_juste(base, entete, 0.30, 0.30, 3)
        jt1, mt1 = journal_juste(base, entete, 0.01, 0.30, 20)
        # R8 : les trades justes à +6/−3, montant de LVMH gonflé de 500 € (au-dessus du seuil de calcul de 25 €)
        _l = list(csv.DictReader(io.StringIO(j63)))
        for _r in _l:
            if _r["valeur"] == "LVMH":
                _r["pnl_net_convention_eur"] = "%.2f" % (float(_r["pnl_net_convention_eur"]) + 500)
        _s = io.StringIO()
        _w = csv.DictWriter(_s, fieldnames=list(_l[0]), lineterminator="\n")
        _w.writeheader()
        _w.writerows(_l)
        journaux = {"juste_6_3": j63, "c5": jc5, "sans_fiche": jsf, "juste_h3": jh3, "juste_tp1": jt1,
                    "montant_faux": _s.getvalue()}
        print("  montants du teneur : +6/−3 %s · C5 %s · +30/−30/3 %s" % (
            {k: round(v, 2) for k, v in m63.items()}, {k: round(v, 2) for k, v in mc5.items()},
            {k: round(v, 2) for k, v in mh3.items()}))
        print("  motifs du teneur : %s" % " · ".join("%s %s/%s/%s %s" % (k[3], k[0], k[1], k[2], m)
                                                    for k, m in sorted(MOTIFS.items())))
        r0 = all(abs(m[v] - RELECTEUR[k][v]) <= 1.0 for k, m in (((0.06, 0.03), m63), ((0.04, 0.025), mc5))
                 for v in VALEURS)
        textes0 = {f: open(os.path.join(base, f), encoding="utf-8").read() for f in (RAD, C5)}
        res = [("R0 le teneur retrouve les montants du relecteur à 1 € près", r0, "")] + les_cas(base, reg0, journaux)
        for nom, ok, preuve in res:
            print(("  ✅ " if ok else "  ❌ ") + nom + ("" if ok else "\n       " + preuve))
        bon = all(ok for _n, ok, _p in res)
        if SABOTER:
            for nom, fichier, avant, apres in SABOTAGES:
                for f, t in textes0.items():
                    open(os.path.join(base, f), "w", encoding="utf-8").write(t)
                if textes0[fichier].count(avant) != 1:
                    print("  ❌ %s : motif trouvé %d fois (attendu 1)" % (nom, textes0[fichier].count(avant)))
                    bon = False
                    continue
                open(os.path.join(base, fichier), "w", encoding="utf-8").write(textes0[fichier].replace(avant, apres))
                r = les_cas(base, reg0, journaux)
                rouges = [n.split(" ")[0] for n, ok, _p in r if not ok]
                print(("  ✅ " if rouges else "  ❌ ") + "%s → rougissent : %s" % (nom, ", ".join(rouges) or "AUCUNE"))
                bon = bon and bool(rouges)
            for f, t in textes0.items():
                open(os.path.join(base, f), "w", encoding="utf-8").write(t)
        print("VERDICT :", "VERT" if bon else "ROUGE")
        return 0 if bon else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
