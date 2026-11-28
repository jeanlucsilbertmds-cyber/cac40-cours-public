#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_COURS_DE_LA_MOULINETTE_Ven_27-11-2026.py — Ven 27-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Éprouve le lot L1 du plan R505 (BACKLOG A-1076 ① ②, A-1100 ; loi R-505 version 2, étape 3) :
① LA MOULINETTE JOUE SUR LES 20 ANS — l'enchaîneur (programmes/ENCHAINER_LA_MOULINETTE.py) fixe les cours de la chaîne
UNE fois, à ⓪ (par défaut le fichier des 20 ans, PREPARER_LA_MOULINETTE_D_ESSAI.COURS_DES_VINGT_ANS), et les passe par
« --cours= » à ② jouer, à l'assemblage et à ④ le juge ; « --cours-du-maitre » garde le fichier maître pour les épreuves
qui ne lisent que 2024 et après (A-952) ; le lanceur (programmes/LANCER_UNE_STRATEGIE.py) transmet l'option à ⓪ et
refuse ensuite de la changer. ② LE CONTRÔLE DE COUVERTURE — programmes/JOUER_LES_VERSIONS.py refuse de jouer quand le
fichier de cours lu ne couvre pas la période déclarée par la fiche (écart de plus d'un mois de calendrier), AVANT le
calibrage, et affiche à chaque lancement la période et le nombre de séances lus. Cas réel (A-1076) : le 26-11-2026,
IND-001-RETEST déclarait 2000-01-03 → 2026-10-30 et a été joué sur 742 séances 2024-2026 sans alerte. ③ LE RECUL DE
FIN CALCULÉ — le délai chiffré le plus long + 1, au lieu du chiffre 26 lu dans
donnees/combinatoires/RECUL_MAXIMUM_DE_LA_FIN.csv (décision de Jean-Luc du 27-11-2026 à 19h29, « 1 », A-1100).
Puis des SABOTAGES : chaque correction retirée dans une copie du programme doit faire tomber au moins un cas (« une
épreuve qui reste verte quand on retire ce qu'elle teste est une décoration »).

AUCUN REGARD SUR 2000-2023 : aucune stratégie réelle n'est jouée. Les cas d'enchaînement tournent sur une racine
FACTICE dont les programmes de la moulinette sont les doublures de tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py
(importées, pas recopiées, R-708) ; les cas réels lisent les DATES des cours (aucun calcul de stratégie) et jouent la
seule fiche d'essai ESSAI-C5-2000-2026 (A-853 : famille C5, déjà jouée sur 2000-2023 ; essai déclaré A-863, une
version, hors de tout compte), dans une copie jetable sans .git.

USAGE
    python3 -B tests/EPREUVES_DES_COURS_DE_LA_MOULINETTE_Ven_27-11-2026.py <source> [--sans-sabotages] [--sans-reel]

① RÔLE — Prouver les trois propriétés ci-dessus, et que chaque épreuve rougit quand on retire ce qu'elle teste.
② CONTEXTE D'APPEL — À la main (l'auteur, son relecteur, Cowork), ou la certification (seule la source en argument).
③ ENTRÉE — `<source>` : la racine d'une COPIE du dépôt (sans .git ; elle n'est jamais modifiée : tout ce qui écrit
  travaille dans une copie ou une racine factice sous /dev/shm) ; `--sans-sabotages` : les cas seulement ;
  `--sans-reel` : sans les cas qui lisent les vrais cours (K3, K12, K13).
④ CONDITIONS D'ENTRÉE — La source porte programmes/, tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py, emp.py ;
  pour les cas réels : donnees/cours_maitre.csv, le témoin des 20 ans, le registre des stratégies.
⑤ SORTIE — UNE valeur, le code : 0 tout tient · 1 un cas tombe ou un sabotage ne mord pas · 2 l'épreuve n'a pas pu
  tourner (ancre de sabotage absente, fichier absent, usage faux — R-734).
⑥ TRAITEMENT — ① dossier de travail sous /dev/shm (sinon le dossier temporaire) · ② les dates des cours lues une fois
  (maître, 20 ans) par le lecteur unique du juge · ③ une copie jetable préparée par PREPARER_LA_MOULINETTE_D_ESSAI
  (sans --jouer) · ④ les cas K1 à K13 sur les vrais programmes · ⑤ chaque sabotage : un dossier de programmes fait de
  liens, le programme visé remplacé par son texte saboté (et, s'il est visé par un cas réel, le même texte posé dans la
  copie jetable le temps du sabotage), les cas rejoués, au moins un doit tomber · ⑥ tout est effacé.
⑦ UNITÉ — secondes (délais) ; séances ; dates.
⑧ POURQUOI — R-731 (épreuves avec sabotages) ; A-1076 (« un CONTRÔLE PAR PROGRAMME qui refuse de jouer quand les cours
  ne couvrent pas la période déclarée par la fiche (écart d'un mois au plus), avec une épreuve sabotée qui rougit ») ;
  A-1100.
⑨ CE QUI CLOCHE — ① Les programmes de la moulinette sont des doublures dans K5 à K10 : le vrai JOUER n'y reçoit pas
  « --cours= » ; il le reçoit dans K12 et K13, appelé directement, pas par l'enchaîneur. ② Le juge réel n'est jamais
  lancé par l'enchaîneur ici (doublure) : que le juge relise bien le fichier passé est éprouvé par JOUER (`calibrer_par_
  le_juge` lui passe le même --cours=, cas J5 de tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py), pas ici.
  ③ K13 (75 s environ sur la machine du Chat le 27-11-2026) n'est rejoué que pour le sabotage du recul dans `main`.
  ④ Le texte « COURS LUS » attendu est recopié de JOUER_LES_VERSIONS.main.
⑩ EFFET — Écrit sous le dossier de travail seulement ; l'efface en sortant.
  ⑤ Sous un sabotage, une exception levée par les cas compte comme une chute, nommée « EXCEPTION … » ; sur les vrais
  programmes, elle remonte (code 1, trace affichée).
⑪ TERMINAISON — Chaque programme lancé est borné (120 s, 600 s pour K13). [sort: oui — code]
"""
import csv
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
TEST_DU_LANCEUR = os.path.join(ICI, "EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py")
JOUER, ENCH, LANC = "JOUER_LES_VERSIONS.py", "ENCHAINER_LA_MOULINETTE.py", "LANCER_UNE_STRATEGIE.py"
JOURNAL_DES_ARGUMENTS = "ARGV_RECUS.jsonl"
# une ligne posée en tête des doublures de JOUER et du JUGE : elle consigne les arguments reçus (cwd = la racine)
CONSIGNER = ('import sys as _s, json as _j, os as _o\n'
             'open(_o.path.join(_o.getcwd(), %r), "a").write(_j.dumps(_s.argv[1:]) + "\\n")\n' % JOURNAL_DES_ARGUMENTS)
L = None            # le module de l'épreuve du lanceur (fabriquer, SID, ESSAI), chargé par `main`
DATES = {}          # « maitre », « vingt_ans » : ensembles de dates lues une fois par `main`
FICHE_REELLE = {}   # les bornes de la fiche réelle IND-001-RETEST, lues au registre de la source (R-732)


def module(chemin, nom):
    """Charge un fichier Python sous un nom ; rend le module. [rend: 1]

    ① charger un programme d'un dossier donné (vrai ou saboté) · ② les cas · ③ `chemin`, `nom` · ④ le fichier existe ·
    ⑤ UNE valeur · ⑥ importlib, le dossier du fichier mis en tête de sys.path le temps du chargement · ⑦ — · ⑧ un
    sabotage se juge sur SON texte · ⑨ — · ⑩ exécute le haut du module · ⑪ rend la main ou lève. [sort: non]
    """
    sys.path.insert(0, os.path.dirname(chemin))
    try:
        spec = importlib.util.spec_from_file_location(nom, chemin)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        sys.path.pop(0)


def lancer(args, cwd, delai=120):
    """Lance `python3 -B <args>` ; rend (code, sortie). [rend: 2]

    ① lancer un programme · ② les cas · ③ `args`, `cwd`, `delai` en secondes · ④ — · ⑤ DEUX valeurs ·
    ⑥ subprocess.run borné · ⑦ secondes · ⑧ le code et le texte sont éprouvés · ⑨ — · ⑩ le programme écrit ce qu'il
    écrit · ⑪ rend la main ; au-delà du délai, code 124. [sort: non]
    """
    try:
        p = subprocess.run([sys.executable, "-B"] + list(args), cwd=cwd, capture_output=True, text=True, timeout=delai)
    except subprocess.TimeoutExpired:
        return 124, "délai de %d s dépassé" % delai
    return p.returncode, p.stdout + p.stderr


def racine_factice(dossier):
    """Fabrique la racine factice de l'épreuve du lanceur, doublures de JOUER et du JUGE consignant leurs arguments.
    [rend: 1]

    ① RÔLE — Une chaîne complète sans aucun cours réel · ② K5 à K10 · ③ `dossier` (absent) · ④ L est chargé ·
    ⑤ UNE valeur : le chemin · ⑥ `L.fabriquer` (fiche factice, famille neuve, réglages validés, doublures), puis
    CONSIGNER en tête des doublures JOUER_LES_VERSIONS.py et JUGE_DES_STRATEGIES.py · ⑦ — · ⑧ R-708 : les doublures
    vivent dans l'épreuve du lanceur, elles ne sont pas recopiées · ⑨ — · ⑩ écrit sous `dossier` · ⑪ rend la main.
    [sort: non]
    """
    r = L.fabriquer(dossier)
    for nom in (JOUER, "JUGE_DES_STRATEGIES.py"):
        p = os.path.join(r, "programmes", nom)
        texte = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(CONSIGNER + texte)
    return r


def arguments_recus(racine):
    """Rend la liste des listes d'arguments reçues par les doublures de JOUER et du JUGE, dans l'ordre. [rend: 1]
    ① lire le journal des arguments · ② K5, K6, K10 · ③ `racine` · ④ — · ⑤ UNE liste · ⑥ une ligne JSON par appel ·
    ⑦ — · ⑧ — · ⑨ — · ⑩ lit · ⑪ rend la main. [sort: non]"""
    p = os.path.join(racine, JOURNAL_DES_ARGUMENTS)
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []


def journal_de_la_chaine(racine):
    """Rend les lignes du journal de la chaîne factice. [rend: 1]
    ① lire · ② K5, K9 · ③ `racine` · ④ — · ⑤ UNE liste de dictionnaires · ⑥ csv · ⑦ — · ⑧ — · ⑨ le nom du journal est
    celui de VERIFIER_LA_CHAINE.JOURNAL, recopié · ⑩ lit · ⑪ rend la main. [sort: non]"""
    p = os.path.join(racine, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "JOURNAL_DE_LA_CHAINE.csv")
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def chaine_complete(prog, racine, maitre=False):
    """Fait ⓪ → ④ par l'enchaîneur `prog` sur la racine factice ; rend la liste des (étape, code, sortie). [rend: 1]

    ① RÔLE — Le chemin réel de la chaîne, étape par étape, comme à la main.
    ② CONTEXTE D'APPEL — K5, K6.
    ③ ENTRÉE — `prog` : le dossier des programmes éprouvés ; `racine` ; `maitre` : « --cours-du-maitre » à ⓪.
    ④ CONDITIONS D'ENTRÉE — la racine sort de `racine_factice`.
    ⑤ SORTIE — UNE liste de triplets ; arrêt à la première étape qui ne rend pas 0.
    ⑥ TRAITEMENT — preparer, decliner, jouer 0 1, assembler, trier, puis juger la première version retenue (lue au
      fichier trié témoigné au journal).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-1076 : « --cours= » manquait à jouer, à l'assemblage et au juge.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — l'enchaîneur écrit sous la racine.
    ⑪ TERMINAISON — rend la main ; chaque appel borné à 120 s. [sort: non]
    """
    faits = []
    for etape in (["preparer"] + (["--cours-du-maitre"] if maitre else []), ["decliner"], ["jouer", "0", "1"],
                  ["assembler"], ["trier"]):
        c, o = lancer([os.path.join(prog, ENCH), racine, L.SID, L.ESSAI] + etape, racine)
        faits.append((etape[0], c, o))
        if c:
            return faits
    tri = [l for l in journal_de_la_chaine(racine) if l["etape"] == "3-trier"][-1]["fichier"]
    v = next(csv.DictReader(open(os.path.join(racine, "CHAINE_%s_%s" % (L.SID, L.ESSAI), tri), encoding="utf-8")))
    c, o = lancer([os.path.join(prog, ENCH), racine, L.SID, L.ESSAI, "juger", v["id_version"]], racine)
    faits.append(("juger", c, o))
    return faits


def les_cas(prog, travail, copie, vingt_ans, long=True):
    """Joue les cas sur les programmes du dossier `prog` ; rend la liste (nom, vrai/faux, détail). [rend: 1]

    ① RÔLE — Les cas K1 à K17 (K10c, K14 à K17 ajoutés le 27-11-2026 par le lot L1-CORR).
    ② CONTEXTE D'APPEL — `main`, une fois sur les vrais programmes, une fois par sabotage.
    ③ ENTRÉE — `prog` : le dossier des programmes (vrai, ou fait de liens avec un programme saboté) ; `travail` : un
      dossier vide ; `copie` : la copie jetable préparée (ou None sous --sans-reel) ; `vingt_ans` : le chemin du témoin
      des 20 ans relatif à la racine ; `long` : jouer K13 (75 s environ).
    ④ CONDITIONS D'ENTRÉE — L, DATES et FICHE_REELLE posés par `main` (sauf --sans-reel).
    ⑤ SORTIE — UNE liste de triplets.
    ⑥ TRAITEMENT — voir chaque cas.
    ⑦ UNITÉ — séances, dates.
    ⑧ POURQUOI — A-1076 ① ②, A-1100.
    ⑨ CE QUI CLOCHE — voir ⑨ de l'en-tête.
    ⑩ EFFET — écrit sous `travail` (et, K12/K13, des résultats sous `travail`).
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    r = []
    os.makedirs(travail)
    J = module(os.path.join(prog, JOUER), "jouer_%d" % id(travail))
    # K1 — un mois de calendrier, dans les deux sens, jour ramené au dernier du mois
    vus = [J.decaler_d_un_mois(d, s) for d, s in (("2000-01-03", 1), ("2026-03-31", -1), ("2025-12-15", 1),
                                                    ("2026-01-10", -1), ("2024-01-31", 1))]
    r.append(("K1 un mois de calendrier (±1, bouts d'année, fin de mois)",
              vus == ["2000-02-03", "2026-02-28", "2026-01-15", "2025-12-10", "2024-02-29"], vus))
    # K2 — la couverture, à la séance près autour d'un mois
    b = ("2000-01-03", "2026-10-30")
    k2 = [J.couverture_des_cours(s, b)[3] for s in ({"2000-02-03", "2026-09-30"}, {"2000-02-04", "2026-10-30"},
                                                    {"2000-01-03", "2026-09-29"}, set())]
    r.append(("K2 couverture : un mois juste passe ; un jour de plus au début, ou à la fin, ou aucune séance : refus",
              k2[0] is None and all(k2[1:]) and "commence" in k2[1] and "finit" in k2[2] and "aucune" in k2[3], k2))
    # K3 — LE CAS RÉEL (R-732) : IND-001-RETEST, déclarée au registre, sur le maître (refus) et sur les 20 ans (passe)
    if DATES:
        m = J.couverture_des_cours(DATES["maitre"], FICHE_REELLE["bornes"])
        v = J.couverture_des_cours(DATES["vingt_ans"], FICHE_REELLE["bornes"])
        r.append(("K3 cas réel IND-001-RETEST %s → %s : maître (%s → %s) REFUSÉ ; 20 ans (%s → %s, %d séances) accepté"
                  % (FICHE_REELLE["bornes"] + m[:2] + v[:2] + (v[2],)),
                  m[3] is not None and "commence le %s" % FICHE_REELLE["bornes"][0] in m[3] and v[3] is None,
                  (m[3], v[3])))
    # K4 — le recul calculé : délai chiffré le plus long + 1
    k4 = [J.recul_maximum(h) for h in (25, 20, 3, 0)]
    r.append(("K4 recul maximum calculé (25 → 26, 20 → 21, 3 → 4, 0 → 1)", k4 == [26, 21, 4, 1], k4))
    # K5 — la chaîne par défaut : « --cours=<20 ans> » reçu par jouer, l'assemblage ET le juge, une fois chacun
    a = racine_factice(os.path.join(travail, "k5"))
    faits = chaine_complete(prog, a)
    recus = arguments_recus(a)
    attendu = "--cours=" + vingt_ans
    par_role = {"jouer": [x for x in recus if any(y.startswith("--tranche=") for y in x)],
                "assembler": [x for x in recus if x[:1] == ["--assembler"]],
                "juger": [x for x in recus if x[:1] == [a]]}
    contenu = open(os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "cours_de_la_chaine.txt"), encoding="utf-8").read()
    ok = [f[1] for f in faits] == [0] * 6 and all(len(v) == 1 and v[0].count(attendu) == 1 for v in par_role.values()) \
        and contenu.strip() == vingt_ans and any(l["etape"] == "0-cours-de-la-chaine" for l in journal_de_la_chaine(a)) \
        and "COURS DE LA CHAÎNE : " + attendu in faits[0][2]
    r.append(("K5 chaîne par défaut : %s reçu par jouer, l'assemblage et le juge ; témoin au journal" % attendu, ok,
              "codes %s · reçus %s" % ([f[1] for f in faits], {k: len(v) for k, v in par_role.items()})))
    # K6 — « --cours-du-maitre » à ⓪ : aucune option de cours nulle part
    a = racine_factice(os.path.join(travail, "k6"))
    faits = chaine_complete(prog, a, maitre=True)
    recus = arguments_recus(a)
    ok = [f[1] for f in faits] == [0] * 6 and len(recus) == 3 and not any(y.startswith("--cours") for x in recus
                                                                           for y in x)
    r.append(("K6 --cours-du-maitre à ⓪ : aucun --cours= reçu (le maître, défaut du juge et de JOUER)", ok,
              "codes %s · %d appels" % ([f[1] for f in faits], len(recus))))
    # K7 — l'option hors de ⓪ ou écrite deux fois : usage, code 2
    a = racine_factice(os.path.join(travail, "k7"))
    c1, _ = lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "preparer", "--cours-du-maitre", "--cours-du-maitre"], a)
    c2, _ = lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "preparer"], a)
    c3, _ = lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "decliner", "--cours-du-maitre"], a)
    r.append(("K7 --cours-du-maitre deux fois, ou à decliner : code 2", (c1, c2, c3) == (2, 0, 2), (c1, c2, c3)))
    # K8 — le fichier des cours de la chaîne changé après ⓪ : l'étape suivante est refusée
    a = racine_factice(os.path.join(travail, "k8"))
    lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "preparer"], a)
    f = os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "cours_de_la_chaine.txt")
    if os.path.exists(f):
        open(f, "w", encoding="utf-8").write("donnees/cours_maitre.csv\n")
    c, o = lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "decliner"], a)
    r.append(("K8 cours de la chaîne réécrits après ⓪ : decliner refusé (empreinte du témoin)",
              c == 1 and "cours_de_la_chaine.txt a changé" in o, "code %d" % c))
    # K9 — une chaîne sans témoin des cours (commencée avant le lot L1) : jouer refusé, code 2, motif nommé
    a = racine_factice(os.path.join(travail, "k9"))
    for e in (["preparer"], ["decliner"]):
        lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI] + e, a)
    j = os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "JOURNAL_DE_LA_CHAINE.csv")
    if os.path.exists(j):   # sans journal (⓪ ou ① a échoué), le cas tombe plus bas : aucun « aucun témoin » lu
        lignes = open(j, encoding="utf-8").read().splitlines(True)
        open(j, "w", encoding="utf-8").writelines(l for l in lignes if not l.startswith("0-cours-de-la-chaine,"))
    c, o = lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "jouer", "0", "1"], a)
    r.append(("K9 chaîne sans témoin des cours : jouer refusé (code 2, « aucun témoin »), rien de joué",
              os.path.exists(j) and c == 2 and "aucun témoin 0-cours-de-la-chaine" in o and not arguments_recus(a),
              "code %d" % c))
    # K10 — le lanceur : l'option transmise à ⓪ ; puis refusée sur une chaîne commencée sur les 20 ans
    a = racine_factice(os.path.join(travail, "k10"))
    c, o = lancer([os.path.join(prog, LANC), a, L.SID, L.ESSAI, "--tranches=2", "--cours-du-maitre"], a)
    recus = arguments_recus(a)
    r.append(("K10 lanceur --cours-du-maitre : chaîne finie, aucun --cours= reçu", c == 0 and recus and
              not any(y.startswith("--cours") for x in recus for y in x), "code %d · %d appels" % (c, len(recus))))
    a = racine_factice(os.path.join(travail, "k10b"))
    lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "preparer"], a)
    c, o = lancer([os.path.join(prog, LANC), a, L.SID, L.ESSAI, "--tranches=2", "--cours-du-maitre"], a)
    etat = os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "ETAT_DU_LANCEUR.json")
    statut = json.load(open(etat, encoding="utf-8")).get("statut") if os.path.exists(etat) else None
    # (27-11-2026, lot L1-CORR, N7 de la relecture neuve V1) l'état écrit est « ÉCHEC », exigé aussi
    r.append(("K10b lanceur --cours-du-maitre sur une chaîne commencée sur les 20 ans : refus, état ÉCHEC, rien de joué",
              c == 1 and "REFUS : --cours-du-maitre demandé" in o and not arguments_recus(a) and statut == "ÉCHEC",
              "code %d · état %s" % (c, statut)))
    # K10c — LE SENS INVERSE (V1-3, 27-11-2026) : chaîne commencée sur le maître, lanceur SANS l'option → refus, ÉCHEC
    a = racine_factice(os.path.join(travail, "k10c"))
    lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "preparer", "--cours-du-maitre"], a)
    c, o = lancer([os.path.join(prog, LANC), a, L.SID, L.ESSAI, "--tranches=2"], a)
    etat = os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "ETAT_DU_LANCEUR.json")
    statut = json.load(open(etat, encoding="utf-8")).get("statut") if os.path.exists(etat) else None
    r.append(("K10c lanceur SANS --cours-du-maitre sur une chaîne commencée sur le maître : refus, état ÉCHEC, rien de joué",
              c == 1 and "REFUS : chaîne demandée sur les 20 ans" in o and not arguments_recus(a) and statut == "ÉCHEC",
              "code %d · état %s" % (c, statut)))
    # K14 — (N6, 27-11-2026) l'enchaîneur affiche « COURS LUS » après chaque tranche jouée (A-1076 ②) : les doublures
    # n'écrivent pas la ligne, l'enchaîneur dit donc « ligne absente » — preuve que l'affichage est appelé
    a = racine_factice(os.path.join(travail, "k14"))
    for e in (["preparer"], ["decliner"]):
        lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI] + e, a)
    c, o = lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "jouer", "0", "1"], a)
    r.append(("K14 enchaîneur, tranche jouée : la ligne « COURS LUS » (ou son absence) est affichée", c == 0 and
              "COURS LUS : ligne absente de la sortie de JOUER" in o, "code %d" % c))
    # K15 — (N3, 27-11-2026) un contenu inconnu du fichier des cours de la chaîne est REFUSÉ par `options_de_cours`
    a = racine_factice(os.path.join(travail, "k15"))
    lancer([os.path.join(prog, ENCH), a, L.SID, L.ESSAI, "preparer"], a)
    f = os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI), "cours_de_la_chaine.txt")
    E = module(os.path.join(prog, ENCH), "ench_%d" % id(travail))
    vu = "fichier absent"
    if os.path.exists(f):
        open(f, "w", encoding="utf-8").write("donnees/cac40_ohlcv.csv\n")
        try:
            vu = "accepté : %r" % (E.options_de_cours(os.path.join(a, "CHAINE_%s_%s" % (L.SID, L.ESSAI))),)
        except Exception as e:
            vu = "%s : %s" % (type(e).__name__, e)
    r.append(("K15 cours de la chaîne inconnus (« donnees/cac40_ohlcv.csv ») : options_de_cours refuse",
              vu.startswith("Impossible") and "cours de la chaîne inconnus" in vu, vu[:160]))
    # K16 — (N1, 27-11-2026) le nombre de séances lues DANS la période : 3 sur 5 (deux séances hors des bornes)
    k16 = J.couverture_des_cours({"2023-12-01", "2024-01-02", "2025-06-02", "2026-07-10", "2026-08-03"},
                                 ("2024-01-02", "2026-07-10"))
    r.append(("K16 couverture : séances dans la période comptées (3 sur 5)", k16[2] == 3 and k16[3] is None, k16))
    # K17 — (V1-1, 27-11-2026) en chaîne « 20 ans », une fiche qui ne déclare pas les 20 ans est refusée, aux deux bouts
    vingt = {"2000-01-03", "2013-05-02", "2026-11-11"}
    k17 = [J.fiche_couvre_le_fichier(vingt, b) for b in (("2000-01-03", "2026-10-30"), ("2024-01-02", "2026-10-30"),
                                                          ("2000-01-03", "2026-10-10"), ("2000-02-03", "2026-10-11"))]
    r.append(("K17 fiche qui ne couvre pas les 20 ans : 2000→2026-10-30 et 2000-02-03→2026-10-11 acceptées ; début 2024 "
              "ou fin 2026-10-10 refusés", k17[0] is None and k17[3] is None and k17[1] and "commence" in k17[1]
              and k17[2] and "finit" in k17[2], k17))
    # K11 — l'assemblage réel (JOUER --assembler) refuse une tranche jouée sur d'autres cours
    d = os.path.join(travail, "k11")
    os.makedirs(d)
    C = module(os.path.join(prog, "CONTRATS_DES_FICHIERS.py"), "contrats_%d" % id(travail))
    comb = os.path.join(d, "COMBINATOIRE_X_E01.csv")
    open(comb, "w", encoding="utf-8").write("id_version\nX-E01-0001\n")
    tr = os.path.join(d, "tranche_0.csv")
    with open(tr, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(C.RESULTATS_DES_VERSIONS))
        w.writeheader()
        w.writerow(dict({k: "x" for k in C.RESULTATS_DES_VERSIONS}, id_version="X-E01-0001",
                        cours_joues="donnees/cours_maitre.csv"))
    sortie = [lancer([os.path.join(prog, JOUER), "--assembler", comb, os.path.join(d, "R%d.csv" % i), tr] + opt, d)
              for i, opt in enumerate((["--cours=" + vingt_ans], ["--cours=donnees/cours_maitre.csv"],
                                       ["--cours=a", "--cours=b"]))]
    r.append(("K11 assemblage : tranche jouée sur le maître refusée sous --cours=<20 ans> ; acceptée (sur ce point) sous "
              "--cours=<maître> ; deux --cours= refusés",
              sortie[0][0] == 1 and "a été jouée sur donnees/cours_maitre.csv" in sortie[0][1]
              and "a été jouée sur" not in sortie[1][1] and "au plus une option" in sortie[2][1],
              [(c, o.strip().splitlines()[-1][:120] if o.strip() else "") for c, o in sortie]))
    if copie is None:
        return r
    comb_e = os.path.join(copie, "donnees", "combinatoires", "COMBINATOIRE_ESSAI-C5-2000-2026_E01.csv")
    # K12 — LE VRAI JOUER sur la vraie copie : la fiche d'essai (2000-2026) sur le maître → refus de couverture AVANT le
    # calibrage, rien d'écrit
    out = os.path.join(travail, "R12.csv")
    c, o = lancer([os.path.join(copie, "programmes", JOUER), copie, comb_e, out, "--essai-sans-regard"], copie)
    r.append(("K12 vrai JOUER, fiche d'essai 2000-2026 sur le maître : refus de couverture avant le calibrage",
              c == 1 and "COUVERTURE DES COURS INSUFFISANTE" in o and "COURS LUS : donnees/cours_maitre.csv" in o
              and "CALIBRAGE PAR LE JUGE" not in o and not os.path.exists(out),
              "code %d · %s" % (c, " | ".join(l for l in o.splitlines() if "COUVERTURE" in l or "COURS LUS" in l)[:300])))
    if long:
        # K13 — LE VRAI JOUER sur les 20 ans : couverture acceptée, période et séances affichées, recul calculé = le
        # délai de la combinatoire + 1 (lu dans le fichier, jamais écrit ici : R-728)
        h = max(int(l["horizon"]) for l in csv.DictReader(open(comb_e, encoding="utf-8")))
        out = os.path.join(travail, "R13.csv")
        c, o = lancer([os.path.join(copie, "programmes", JOUER), copie, comb_e, out, "--cours=" + vingt_ans,
                       "--essai-sans-regard"], copie, delai=600)
        r.append(("K13 vrai JOUER, fiche d'essai sur les 20 ans : code 0, « COURS LUS : %s · 2000-… », recul au plus "
                  "%d (calculé : %d + 1)" % (vingt_ans, h + 1, h),
                  c == 0 and ("COURS LUS : %s · 2000-" % vingt_ans) in o
                  and ("au plus %d (calculé : délai chiffré le plus long %d + 1" % (h + 1, h)) in o and os.path.exists(out),
                  "code %d · %s" % (c, " | ".join(l.split("· ", 1)[-1] for l in o.splitlines()
                                                  if "COURS LUS" in l or "RECUL DE LA FIN" in l)[:400])))
    return r


# LES SABOTAGES : (nom, quoi, programme visé, texte d'origine, texte saboté, long ?)
SABOTAGES = [
    ("SA1", "refus de couverture retiré", JOUER, "        if refus_c:\n            return arreter(",
     "        if False:\n            return arreter(", False),
    ("SA2", "début non contrôlé", JOUER, "    if premiere > decaler_d_un_mois(bornes[0], 1):", "    if False:", False),
    ("SA3", "fin non contrôlée", JOUER, "    if derniere < decaler_d_un_mois(bornes[1], -1):", "    if False:", False),
    ("SA4", "mois non décalé", JOUER, "    m += sens\n", "    m += 0\n", False),
    ("SA5", "recul fixe 26", JOUER, "    return horizon_max + 1\n", "    return 26\n", False),
    ("SA6", "main reprend un recul fixe", JOUER, "    recul_max = recul_maximum(h_max)", "    recul_max = 26", True),
    ("SA7", "assemblage sans contrôle des cours", JOUER,
     '            if attendu and os.path.normpath(r["cours_joues"]) != os.path.normpath(attendu[0]):',
     "            if False:", False),
    ("SA8", "jouer sans --cours=", ENCH, '"--tranche=%s/%s" % (k, n), *options_de_cours(ch), delai=580)',
     '"--tranche=%s/%s" % (k, n), delai=580)', False),
    ("SA9", "assembler sans --cours=", ENCH, "*[os.path.join(ch, t[e][0]) for e in noms], *options_de_cours(ch)):",
     "*[os.path.join(ch, t[e][0]) for e in noms]):", False),
    ("SA10", "juge sans --cours=", ENCH, "racine, ident,\n                  *options_de_cours(ch), delai=580)",
     "racine, ident,\n                  delai=580)", False),
    ("SA11", "--cours-du-maitre ignoré à ⓪", ENCH, "fh.write((MOT_DU_MAITRE if maitre else COURS_DES_VINGT_ANS)",
     "fh.write((COURS_DES_VINGT_ANS)", False),
    ("SA12", "option acceptée hors de ⓪", ENCH, '(maitre and argv[4:5] != ["preparer"])', "False", False),
    ("SA13", "chaîne sans témoin des cours tolérée", ENCH, "    if TEMOIN_DES_COURS not in t:\n        raise",
     "    if TEMOIN_DES_COURS not in t:\n        return []\n        raise", False),
    ("SA14", "cours non témoignés au journal", ENCH, "    V.temoigner(ch, TEMOIN_DES_COURS, FICHIER_DES_COURS)",
     "    pass", False),
    ("SA15", "lanceur : contradiction non refusée", LANC, "        if maitre and lus:", "        if False:", False),
    ("SA16", "lanceur : option non transmise à ⓪", LANC,
     'options = [MAITRE] if etape == "preparer" and maitre else []', "options = []", False),
    # (27-11-2026, lot L1-CORR : les sabotages muets N1, N3, N6, N7 de la relecture neuve V1, et V1-1, V1-3)
    ("SA17", "N1 compte faux des séances dans la période", JOUER,
     "    dedans = sum(1 for d in seances if bornes[0] <= d <= bornes[1])", "    dedans = len(seances)", False),
    ("SA18", "N3 contenu inconnu accepté", ENCH,
     '    raise V.Impossible("cours de la chaîne inconnus dans %s : %r" % (FICHIER_DES_COURS, texte))',
     '    return ["--cours=" + texte]', False),
    ("SA19", "N6 « COURS LUS » retiré de l'enchaîneur", ENCH,
     '        afficher_les_cours_lus(ch, "e2/sortie_%s" % k)', "        pass", False),
    ("SA20", "N7 état non écrit ÉCHEC au refus", LANC,
     '            ecrire_l_etat(ch, etat, "ÉCHEC", message)\n            print(message)\n            return 1\n        # LE SENS',
     '            print(message)\n            return 1\n        # LE SENS', False),
    ("SA21", "V1-3 sens inverse non refusé", LANC, "        if not maitre and not lus:", "        if False:", False),
    ("SA22", "V1-1 fiche qui ne couvre pas les 20 ans acceptée", JOUER,
     "    if bornes[0] > decaler_d_un_mois(premiere, 1):", "    if False:", False),
]


def main(argv):
    """Rend le code de sortie. [rend: 1]

    ① RÔLE — Préparer, jouer les cas, puis les sabotages. ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `<source>` [--sans-sabotages] [--sans-reel]. ④ CONDITIONS D'ENTRÉE — voir l'en-tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. ⑥ TRAITEMENT — voir ⑥ de l'en-tête. ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — R-731, A-1076, A-1100. ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — dossier de travail, effacé.
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    global L
    opts = [a for a in argv[1:] if a.startswith("--")]
    pos = [a for a in argv[1:] if not a.startswith("--")]
    if len(pos) != 1 or set(opts) - {"--sans-sabotages", "--sans-reel"}:
        print(__doc__.split("① RÔLE")[0])
        return 2
    source = os.path.abspath(pos[0])
    prog_dir = os.path.join(source, "programmes")
    if os.path.lexists(os.path.join(source, ".git")):
        print("❌ IMPOSSIBLE — %s porte .git : l'épreuve ne tourne que sur une copie" % source)
        return 2
    for f in (os.path.join(prog_dir, JOUER), os.path.join(prog_dir, ENCH), os.path.join(prog_dir, LANC),
              TEST_DU_LANCEUR, os.path.join(source, "emp.py")):
        if not os.path.exists(f):
            print("❌ IMPOSSIBLE — absent : %s" % f)
            return 2
    _argv, sys.argv = sys.argv, sys.argv[:1]
    try:
        L = module(TEST_DU_LANCEUR, "epreuve_du_lanceur")
    finally:
        sys.argv = _argv
    L.SOURCE_DES_PROGRAMMES = prog_dir
    P = module(os.path.join(prog_dir, "PREPARER_LA_MOULINETTE_D_ESSAI.py"), "preparer_essai")
    vingt_ans = P.COURS_DES_VINGT_ANS
    base = "/dev/shm" if os.path.isdir("/dev/shm") else None
    travail = tempfile.mkdtemp(prefix="cours_moulinette_", dir=base)
    rouge, copie = False, None
    try:
        if "--sans-reel" not in opts:
            sys.path.insert(0, prog_dir)
            import JUGE_DES_STRATEGIES as JS
            import CONTRATS_DES_FICHIERS as CS
            mn = JS.table_mnemoniques(JS.trouver(source, "REFERENTIEL_VALEURS"))
            for cle, f in (("maitre", "donnees/cours_maitre.csv"), ("vingt_ans", vingt_ans)):
                cours, _ = JS.lire_par_le_lecteur(source, f, mn)
                DATES[cle] = {b["date"] for s in cours.values() for b in s}
            fiche = CS.fiches_du_registre(JS.trouver(source, CS.NOM_DU_REGISTRE_DES_STRATEGIES))["IND-001-RETEST"]
            ok0, manq, bornes = JS.porte_0(dict(fiche))
            if not ok0:
                print("❌ IMPOSSIBLE — la porte 0 refuse la fiche réelle IND-001-RETEST : %s" % manq)
                return 2
            FICHE_REELLE["bornes"] = tuple(bornes)
            # LA COPIE JETABLE de la fiche d'essai (A-853, A-861) : sans .git, préparée sans --jouer
            copie = os.path.join(travail, "copie")
            shutil.copytree(source, copie, symlinks=True,
                            ignore=shutil.ignore_patterns(".git", "etudes", "archives", "prompts_taches", "PILOTE_SOCLE*"))
            c, o = lancer([os.path.join(copie, "programmes", "PREPARER_LA_MOULINETTE_D_ESSAI.py"), copie], copie)
            if c:
                print("❌ IMPOSSIBLE — la copie d'essai ne se prépare pas (code %d) : %s" % (c, o[-400:]))
                return 2
        for nom, ok, detail in les_cas(prog_dir, os.path.join(travail, "vrai"), copie, vingt_ans):
            print("%s %s : %s" % ("✅" if ok else "❌", nom, detail))
            rouge |= not ok
        if "--sans-sabotages" in opts:
            return 1 if rouge else 0
        os.symlink(os.path.join(source, "emp.py"), os.path.join(travail, "emp.py"))
        for nom, quoi, cible, avant, apres, long in SABOTAGES:
            texte = open(os.path.join(prog_dir, cible), encoding="utf-8").read()
            if texte.count(avant) != 1:
                print("❌ IMPOSSIBLE — ancre du sabotage %s trouvée %d fois dans %s" % (nom, texte.count(avant), cible))
                return 2
            sab = os.path.join(travail, "prog_" + nom)
            os.makedirs(sab)
            for f in os.listdir(prog_dir):
                if f.endswith(".py") and f != cible:
                    os.symlink(os.path.join(prog_dir, f), os.path.join(sab, f))
            open(os.path.join(sab, cible), "w", encoding="utf-8").write(texte.replace(avant, apres))
            dans_la_copie = copie is not None and cible == JOUER
            if dans_la_copie:   # K12, K13 jouent le JOUER de la copie (l'essai déclaré l'exige) : le même sabotage
                open(os.path.join(copie, "programmes", cible), "w", encoding="utf-8").write(texte.replace(avant, apres))
            try:
                try:
                    tombes = [c for c, ok, _ in les_cas(sab, os.path.join(travail, nom), copie, vingt_ans, long=long)
                              if not ok]
                except Exception as e:   # un sabotage qui fait LEVER l'épreuve la fait tomber : c'est dit, nommé
                    tombes = ["EXCEPTION %s: %s" % (type(e).__name__, str(e)[:120])]
            finally:
                if dans_la_copie:
                    open(os.path.join(copie, "programmes", cible), "w", encoding="utf-8").write(texte)
            print("%s %s %s (%s) → %s" % ("✅" if tombes else "❌", nom, quoi, cible,
                                          ("tombe(nt) : " + " · ".join(c.split()[0] for c in tombes)) if tombes
                                          else "AUCUN CAS NE TOMBE"))
            rouge |= not tombes
            shutil.rmtree(os.path.join(travail, nom), ignore_errors=True)
        return 1 if rouge else 0
    finally:
        shutil.rmtree(travail, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
