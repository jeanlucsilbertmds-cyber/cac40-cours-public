#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_RATTRAPAGE — Jeu 01-10-2026 (Paris)
Rôle : prouver que le rattrapage du matin relance le circuit quand il le faut, pas quand il ne le faut pas, et qu'une
relance ne double rien ; et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/FAUT_IL_RATTRAPER.py,
.github/workflows/rattrapage_du_matin.yml, ou l'anti-doublon de programmes/TENIR_LES_POSITIONS.py (R-731).

À QUOI ÇA SERT. Décision de Jean-Luc du 01-10-2026 à 00h01 (« 1 ») : un soir où le circuit de GitHub ne finit pas, il
est relancé seul le lendemain matin (A-515). Deux fautes coûtent : ne pas relancer un soir raté (les signaux de la séance
sont perdus pour toujours) ; relancer et doubler une position ou un trade. Les épreuves visent les deux.

LES ÉPREUVES — chaque décision est lancée à une heure de Paris FIXÉE (tests/HORLOGE_D_EPREUVE.py), sur un petit dépôt
qui porte le VRAI calendrier ; les séances attendues sont écrites à la main :
R1 jeudi 01-10 07h15, radar du 30-09, signaux du 30-09 : rien (0) ;
R2 radar du 29-09, signaux du 30-09 : à rattraper (10) ;
R3 radar du 30-09, signaux du 29-09 (la collecte, non bloquante, a échoué) : à rattraper (10) ;
R4 radar absent, puis radar sans date (un plantage écrit à sa place) : à rattraper (10) ;
R5 calendrier absent : indécis (1), « PAR PRÉCAUTION » ;
R6 samedi 03-10 : radar et signaux du 02-10 : rien ; radar du 01-10 : à rattraper ;
R7 samedi 26-12 : radar du 25-12 (le circuit tourne un soir férié), signaux du 24-12 : rien ;
R8 mardi 07-04 (après le vendredi saint et le lundi de Pâques, fermés) : radar et signaux du 02-04 : rien ;
R9 signaux absents, puis séance « 20260930 » : à rattraper ;
R10 radar du 01-10 à 07h16 (relancé ce matin), signaux du 30-09 : rien ;
R11 sans argument : 1 ;
R12 vendredi 02-10 : radar du rattrapage du jeudi matin (07h16), signaux du jeudi soir (20h21), positions tombées : à
    rattraper — la date seule du radar disait « rien » (relecteur, 01-10-2026) ;
R13 deux valeurs sans la séance, puis la liste absente : à rattraper ;
R14 radar sans heure, puis signaux sans heure de calcul : à rattraper ;
R15 radar à 07h45, signaux calculés à 20:21 le même jour : à rattraper ;
R16 radar et calcul à la même minute (le cas réel du dépôt) : rien ;
D1 date_ecrite lit « Jeu 01-10-2026 07h45 » en (2026-10-01, 07:45), et dit l'absence ;
T1 tenir() deux fois de suite sur un cas connu (une vente forcée, un signal, puis une entrée vendue à l'échéance) : la
   seconde fois, aucun trade et les mêmes positions ;
T2 programmes/TENIR_LES_POSITIONS.py lancé deux fois sur une copie du dépôt (vraies données) : la seconde fois ne change
   aucun fichier ;
W1 le pas qui décide, JOUÉ sous bash -e comme sur GitHub, avec un faux programme qui rend 0, 10 puis 1 : il passe
   et écrit le bon code ;
W2 le passage du matin : S'IL A UN HORAIRE, du mardi au samedi ; droit de lancer un circuit, relance dès que le code
   n'est pas 0, vers la branche par défaut et avec rattrapage=true, rougit quand il n'est ni 0 ni 10. Son horaire est
   COUPÉ depuis le 11-10-2026 (décision de Jean-Luc, 18h59, « 1 » : quota du dépôt privé épuisé, A-543) : W2 exigeait
   un horaire et rougissait depuis ; le réveil du matin qui tourne est celui du circuit public (« 41 5 * * 2-6 »),
   éprouvé par tests/EPREUVES_DE_L_HORAIRE_DU_CIRCUIT_Mar_13-10-2026.py (S16). Modifié le 16-10-2026 ;
W3 le circuit du soir : une entrée « rattrapage » ; la commande de la mesure, JOUÉE avec « true », « false » et vide
   (l'horaire du soir), n'est sautée qu'avec « true » ; un seul circuit à la fois.
LES SABOTAGES : F1 la séance attendue est le jour même (R1) · F2 les signaux ne comptent plus (R3) · F3 le radar ne compte
plus (R2) · F4 le radar comparé au calcul par la date seule (R12) · F5 un calendrier illisible décide « rien » (R5) · F6 des
signaux illisibles passent pour à jour (R9) · F7 la forme de la séance n'est plus exigée (R9) · P1 l'anti-doublon des
positions est retiré (T1) · F8 un radar antérieur au calcul des signaux est accepté (R12) · F9 les valeurs sans la séance
ne comptent plus (R13) · W4 un horaire du lundi au vendredi est remis au passage (W2) · W5 un code indécis ne relance plus (W2) · W6
`set +e` retiré (W1) · W7 un code écrit en dur (W1) · W8 la relance sans rattrapage=true (W2) · W9 la mesure n'est plus
sautée (W3) · W10 deux circuits à la fois (W3) · F10 heure et minutes inversées (R15, D1) · F11 une liste absente
tenue pour vide (R13) · F12 la même minute refusée (R16) · W11 la mesure sautée sans entrée, chaque soir (W3) · F13 une
seule valeur sans la séance tolérée (R13) · F14 l'heure cherchée n'importe où dans l'en-tête (D1) · W12 un groupe par
passage, donc deux circuits à la fois (W3).

USAGE : python3 tests/EPREUVES_DU_RATTRAPAGE_Jeu_01-10-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import copy, filecmp, importlib.util, json, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HORLOGE_D_EPREUVE import lancer_a_l_heure   # l horloge posée à un seul endroit (R-708)

FAUT = "programmes/FAUT_IL_RATTRAPER.py"
POS = "programmes/TENIR_LES_POSITIONS.py"
WF = ".github/workflows/rattrapage_du_matin.yml"
SABOTAGES = {
    "Z0": [],
    "F1_attendue_jour_meme": [(FAUT, "K.dernier_jour_de_bourse(aujourd_hui - timedelta(days=1), cal)", "K.dernier_jour_de_bourse(aujourd_hui, cal)")],
    "F2_signaux_ignores": [(FAUT, "    if seance is None or seance < a:\n", "    if False:\n")],
    "F3_radar_ignore": [(FAUT, "    if radar is None or calcul is None or radar < calcul:\n", "    if False:\n")],
    "F4_radar_du_jour_exact": [(FAUT, "radar < calcul", "radar[:10] < calcul[:10]")],
    "F5_indecis_rien": [(FAUT, "return INDECIS, [", "return RIEN, [")],
    "F6_signaux_illisibles_a_jour": [(FAUT, '        seance = None\n        lignes.append(f"signaux : illisibles', '        seance = "9999-12-31"\n        lignes.append(f"signaux : illisibles')],
    "F7_forme_libre": [(FAUT, 'if not (isinstance(seance, str) and re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", seance)):', "if not isinstance(seance, str):")],
    "P1_anti_doublon_retire": [(POS, "            if deja:\n                continue\n", "            if False:\n                continue\n")],
    "F8_radar_avant_calcul_accepte": [(FAUT, "radar is None or calcul is None or radar < calcul", "radar is None")],
    "F9_valeurs_manquantes_ignorees": [(FAUT, "    elif manquent is None or manquent:\n", "    elif False:\n")],
    "F10_heure_inversee": [("programmes/CONTRATS_DES_FICHIERS.py", '(f"{h.group(1)}:{h.group(2)}" if h else None)', '(f"{h.group(2)}:{h.group(1)}" if h else None)')],
    "F11_liste_absente_vide": [(FAUT, "manquent = manquent if isinstance(manquent, list) else None", "manquent = manquent if isinstance(manquent, list) else []")],
    "F12_meme_minute_refusee": [(FAUT, "radar < calcul", "radar <= calcul")],
    "W11_mesure_sautee_sans_entree": [(".github/workflows/collecte_abc.yml", '" = "true" ]; then echo "mesure sautée', '" != "false" ]; then echo "mesure sautée')],
    "F13_une_valeur_toleree": [(FAUT, "    elif manquent is None or manquent:\n", "    elif manquent is None or len(manquent) > 1:\n")],
    "F14_heure_cherchee_partout": [("programmes/CONTRATS_DES_FICHIERS.py", 'h = _re.match(r"\\s+(\\d{2})h(\\d{2})\\b", t[m.end(1):])', 'h = _re.search(r"(\\d{2})h(\\d{2})", t[m.end(1):])')],
    "W12_un_groupe_par_passage": [(".github/workflows/collecte_abc.yml", "  group: circuit-du-soir\n", "  group: circuit-du-soir-${{ github.run_id }}\n")],
    "W4_lundi_au_vendredi": [(WF, "  workflow_dispatch:\n", '  workflow_dispatch:\n  schedule:\n    - cron: "15 5 * * 1-5"\n')],
    "W5_indecis_sans_relance": [(WF, "        if: steps.faut.outputs.code != '0'\n", "        if: steps.faut.outputs.code == '10'\n")],
    "W6_sans_set_plus_e": [(WF, "          set +e\n", "")],
    "W7_code_en_dur": [(WF, 'echo "code=$?" >> "$GITHUB_OUTPUT"', 'echo "code=0" >> "$GITHUB_OUTPUT"')],
    "W8_relance_sans_rattrapage": [(WF, " -f rattrapage=true", "")],
    "W9_mesure_non_sautee": [(".github/workflows/collecte_abc.yml", ' = "true" ]; then echo "mesure sautée', ' = "vrai" ]; then echo "mesure sautée')],
    "W10_deux_circuits_a_la_fois": [(".github/workflows/collecte_abc.yml", "  cancel-in-progress: false\n", "  cancel-in-progress: true\n")],
}
ENTETE_RADAR = "# AUDIT ÉCOSYSTÈME CAC 40 — Jeu {j}-{m}-{a}{h} (Paris)\n# Score : 44 ✅  ·  0 ⚠️  ·  0 ❌\n"


def depot_de_decision(d, radar, seance, calendrier=True, calcul=None, manquent=()):
    """Fabrique la racine d'une décision et la rend.

    ① RÔLE — Poser un cas : le calendrier réel, un rapport du radar daté, des signaux.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par cas.
    ③ ENTRÉE — `d` : un dossier neuf · `radar` : « AAAA-MM-JJ HH:MM » (20:21 si l'heure manque), « AAAA-MM-JJ
      sans_heure », « absent » ou « sans_date » · `seance` : la séance des signaux, ou « absent » · `calendrier` : faux
      pour ne pas le poser · `calcul` : le `calcule_le` des signaux (par défaut la séance à 20:15) · `manquent` : les
      valeurs sans la séance, None pour omettre la clé.
    ④ CONDITIONS D'ENTRÉE — Le dépôt éprouvé porte donnees/CALENDRIER_EURONEXT.csv.
    ⑤ SORTIE — UNE valeur : la racine `d`.
      [rend: 1]
    ⑥ TRAITEMENT — créer rapports/ et donnees/, y écrire ce que le cas demande.
    ⑦ UNITÉ — Des dates AAAA-MM-JJ.
    ⑧ POURQUOI — Le rapport a l'en-tête exact que le radar écrit (« CAC 40 — Jeu 01-10-2026 »), lu par le même motif.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(os.path.join(d, "rapports")); os.makedirs(os.path.join(d, "donnees"))
    if calendrier:
        shutil.copy(os.path.join(DEPOT, "donnees", "CALENDRIER_EURONEXT.csv"), os.path.join(d, "donnees"))
    if radar == "sans_date":
        open(os.path.join(d, "rapports", "audit_du_jour.md"), "w", encoding="utf-8").write(
            "Traceback (most recent call last):\n  File \"programmes/audit_ecosysteme.py\"\nKeyError: 'x'\n")
    elif radar != "absent":
        jour, _, heure = radar.partition(" ")
        a, m, j = jour.split("-")
        h = "" if heure == "sans_heure" else " " + (heure or "20:21").replace(":", "h")
        # LE VRAI CORPS du rapport du dépôt sous l'en-tête d'épreuve (relecteur, 01-10-2026) : il porte des noms de
        # fichiers horodatés (« …_14h39.md ») dans ses 600 premiers caractères, qu'une lecture lâche prendrait pour l'heure
        corps = open(os.path.join(DEPOT, "rapports", "audit_du_jour.md"), encoding="utf-8").read().split("\n", 2)[-1]
        open(os.path.join(d, "rapports", "audit_du_jour.md"), "w", encoding="utf-8").write(
            ENTETE_RADAR.format(a=a, m=m, j=j, h=h) + corps)
    if seance != "absent":
        sig = {"seance": seance, "signaux": [], "calcule_le": (calcul or f"{seance} 20:15") + " (Europe/Paris)"}
        if manquent is not None:   # None : la clé manque
            sig["valeurs_sans_cette_seance"] = list(manquent)
        json.dump(sig, open(os.path.join(d, "donnees", "signaux_du_jour.json"), "w", encoding="utf-8"))
    return d


def decision(depot, racine, heure, tmp):
    """Lance FAUT_IL_RATTRAPER.py à l'heure donnée et rend (code, sortie).

    ① RÔLE — Emprunter le chemin réel : le programme en ligne de commande.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `depot` : la copie éprouvée (sabotée ou non) · `racine` : le cas · `heure` : AAAA-MM-JJTHH:MM:SS ·
      `tmp` : dossier jetable.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code de sortie · la sortie standard.
      [rend: 2]
    ⑥ TRAITEMENT — lancer à l'heure fixée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le code de sortie est ce que lit le passage du matin.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus.
    ⑪ TERMINAISON — Rend la main ; au-delà de 60 secondes, lève.
      [sort: non]
    """
    cmd = [sys.executable, os.path.join(depot, FAUT)] + ([racine] if racine else [])
    p = lancer_a_l_heure(cmd, heure, os.path.join(tmp, "_horloge"), delai=60)
    return p.returncode, p.stdout + p.stderr


def epreuves(depot, tmp):
    """Joue les épreuves sur la copie `depot` et rend la liste (nom, verdict).

    ① RÔLE — Les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `depot` : une copie du dépôt, sabotée ou non · `tmp` : un dossier jetable.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des couples (nom, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — les décisions R1-R14, puis la relance des positions T1-T2, puis les deux circuits W1-W3.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Chaque cas vise une façon de perdre une séance ou de doubler une position.
    ⑨ CE QUI CLOCHE — T2 tourne sur les vraies données du dépôt éprouvé : un soir sans position ouverte, elle prouve
      moins que T1.
    ⑩ EFFET — Écrit dans `tmp` et dans `depot` (T2 y relance les positions : c'est une copie).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    res = []
    n = iter(range(100))
    dos = lambda: os.path.join(tmp, "c%d" % next(n))
    D = lambda radar, seance, heure, cal=True, **k: decision(depot, depot_de_decision(dos(), radar, seance, cal, **k), heure, tmp)
    JEU = "2026-10-01T07:15:00"
    c, o = D("2026-09-30", "2026-09-30", JEU)
    res.append(("R1 jeudi, radar et signaux du 30-09 : rien (0)", c == 0 and "RIEN À RATTRAPER" in o and "2026-09-30" in o))
    c, o = D("2026-09-29", "2026-09-30", JEU)
    res.append(("R2 radar de l'avant-veille : à rattraper (10)", c == 10 and "radar n'a pas écrit son rapport après" in o))
    c, o = D("2026-09-30", "2026-09-29", JEU)
    res.append(("R3 signaux de l'avant-veille : à rattraper (10)", c == 10 and "signaux ne portent pas" in o))
    c1, o = D("absent", "2026-09-30", JEU)
    c2, o = D("sans_date", "2026-09-30", JEU)
    res.append(("R4 radar absent, puis sans date : à rattraper (10)", c1 == 10 and c2 == 10))
    c, o = D("2026-09-30", "2026-09-30", JEU, cal=False)
    res.append(("R5 calendrier absent : indécis (1), par précaution", c == 1 and "PAR PRÉCAUTION" in o))
    c1, o = D("2026-10-02", "2026-10-02", "2026-10-03T07:15:00")
    c2, o = D("2026-10-01", "2026-10-02", "2026-10-03T07:15:00")
    res.append(("R6 samedi 03-10 : du 02-10, rien ; radar du 01-10, à rattraper", c1 == 0 and c2 == 10))
    c, o = D("2026-12-25", "2026-12-24", "2026-12-26T07:15:00")
    res.append(("R7 samedi 26-12, radar du 25-12 férié, signaux du 24-12 : rien", c == 0 and "2026-12-24" in o))
    c, o = D("2026-04-02", "2026-04-02", "2026-04-07T07:15:00")
    res.append(("R8 mardi 07-04 après Pâques : la séance attendue est le 02-04, rien", c == 0 and "séance du 2026-04-02" in o))
    # le MOTIF est vérifié, pas seulement le code : sans signaux, l'heure du calcul manque aussi et le radar ferait
    # rattraper à lui seul — un sabotage des signaux passerait inaperçu
    c1, o1 = D("2026-09-30", "absent", JEU)
    c2, o2 = D("2026-09-30", "20260930", JEU)
    res.append(("R9 signaux absents, puis séance « 20260930 » : à rattraper, parce que les signaux ne portent pas la séance",
                c1 == 10 and c2 == 10 and all("les signaux ne portent pas cette séance" in o.splitlines()[0] for o in (o1, o2))))
    c, o = D("2026-10-01 07:16", "2026-09-30", JEU)
    res.append(("R10 radar relancé ce matin (01-10 07h16), signaux du 30-09 : rien", c == 0))
    c, o = D("2026-10-01 07:16", "2026-10-01", "2026-10-02T07:15:00", calcul="2026-10-01 20:21")
    res.append(("R12 vendredi : radar du rattrapage d'hier matin, signaux d'hier soir, positions tombées : à rattraper",
                c == 10 and "après le calcul des signaux" in o))
    c, o = D("2026-09-30", "2026-09-30", JEU, manquent=["ENGIE", "VINCI"])
    c2, o2 = D("2026-09-30", "2026-09-30", JEU, manquent=None)
    c3, o3 = D("2026-09-30", "2026-09-30", JEU, manquent=["ACCOR"])
    res.append(("R13 deux valeurs sans la séance, puis la liste absente, puis une seule valeur : à rattraper",
                c == 10 and "valeurs n'ont pas cette séance" in o and c2 == 10 and "ILLISIBLE" in o2 and c3 == 10))
    c1, o = D("2026-09-30 sans_heure", "2026-09-30", JEU)
    c2, o = D("2026-09-30", "2026-09-30", JEU, calcul="illisible")
    res.append(("R14 radar sans heure, puis signaux sans heure de calcul : à rattraper", c1 == 10 and c2 == 10))
    # les minutes au-delà de 24 attrapent une heure et des minutes inversées (relecteur, 01-10-2026)
    c, o = D("2026-10-01 07:45", "2026-10-01", "2026-10-02T07:15:00", calcul="2026-10-01 20:21")
    res.append(("R15 radar à 07h45, signaux calculés à 20:21 le même jour : à rattraper", c == 10))
    c, o = D("2026-09-30 20:21", "2026-09-30", JEU, calcul="2026-09-30 20:21")
    res.append(("R16 radar et calcul à la même minute, le cas réel du dépôt : rien", c == 0))
    try:
        sp = importlib.util.spec_from_file_location("ctr_%d" % id(tmp), os.path.join(depot, "programmes", "CONTRATS_DES_FICHIERS.py"))
        CT = importlib.util.module_from_spec(sp); sp.loader.exec_module(CT)
        dd = depot_de_decision(dos(), "2026-10-01 07:45", "2026-10-01")
        mot = next(x[1] for x in CT.FABRIQUES_DU_SOIR if x[0] == "rapports/audit_du_jour.md")
        ds = depot_de_decision(dos(), "2026-10-01 sans_heure", "2026-10-01")
        ok_d = (CT.date_ecrite(dd, "rapports/audit_du_jour.md", mot) == ("2026-10-01", "07:45", None)
                and CT.date_ecrite(ds, "rapports/audit_du_jour.md", mot) == ("2026-10-01", None, None)
                and CT.date_ecrite(dd, "absent.md", mot) == (None, None, "ABSENT"))
    except Exception:
        ok_d = False
    res.append(("D1 date_ecrite lit « Jeu 01-10-2026 07h45 » en (2026-10-01, 07:45), un en-tête sans heure sans heure "
                "(sur le vrai corps du rapport), et dit l'absence", ok_d))
    c, o = decision(depot, None, JEU, tmp)
    res.append(("R11 sans argument : 1", c == 1))
    # T1 — tenir() deux fois, sur des cas connus du calibrage du programme
    try:
        sp = importlib.util.spec_from_file_location("pos_%d" % id(tmp), os.path.join(depot, POS))
        T = importlib.util.module_from_spec(sp); sp.loader.exec_module(T)
        mod = T.charger_module_positions(T.trouver_module(depot))
        att = lambda v, d: {"strategie": "S", "valeur": v, "date_signal": d, "date_entree": "", "prix_entree": T.INCONNU,
                            "tp": T.INCONNU, "sl": T.INCONNU, "horizon_fin": T.INCONNU, "statut": T.EN_ATTENTE,
                            "comptabilite": T.UN_JETON, "regles_pre_trade": "", "explication": ""}
        ca = [{"date": "2026-05-04", "open": 100.0, "high": 100.5, "low": 99.5, "close": 100.0},
              {"date": "2026-05-05", "open": 100.0, "high": 100.5, "low": 97.0, "close": 97.2}]
        cours = {"A": ca, "B": [dict(x, open=50.0, high=51.0, low=49.0, close=50.0) for x in ca]}
        sig = [{"strategie": "S", "valeur": "B", "date_signal": "2026-05-05"}]
        reg = {"S": {"tp": 0.04, "sl": 0.025, "horizon": 20}}
        r1 = T.tenir([att("A", "2026-05-04")], cours, sig, None, mod, reglages=reg)
        r2 = T.tenir(copy.deepcopy(r1["positions"]), cours, sig, None, mod, reglages=reg)
        cl = [{"date": "2026-05-%02d" % (4 + k), "open": 100.0, "high": 100.5, "low": 99.5, "close": 100.0} for k in range(12)]
        reg5 = {"S": {"tp": 0.04, "sl": 0.025, "horizon": 5}}
        q1 = T.tenir([att("L", "2026-05-04")], {"L": cl}, [], None, mod, reglages=reg5)
        q2 = T.tenir(copy.deepcopy(q1["positions"]), {"L": cl}, [], None, mod, reglages=reg5)
        ok1 = (len(r1["trades"]) == 1 and len(r1["positions"]) == 2 and r2["trades"] == [] and r2["positions"] == r1["positions"]
               and len(q1["trades"]) == 1 and q2["trades"] == [] and q2["positions"] == q1["positions"])
    except Exception as e:
        ok1 = False
        print("     T1 : " + type(e).__name__ + " : " + str(e)[:200])
    res.append(("T1 tenir() deux fois : la seconde, aucun trade et les mêmes positions", ok1))
    # T2 — le programme réel, deux fois, sur une copie du dépôt
    p1 = subprocess.run([sys.executable, os.path.join(depot, POS), depot], capture_output=True, text=True, timeout=300)
    snap = os.path.join(tmp, "apres_un")
    os.makedirs(snap)
    fichiers = ("donnees/claude_positions_ouvertes.csv", "donnees/claude_journal_trades.csv")
    for f in fichiers:
        shutil.copy(os.path.join(depot, f), os.path.join(snap, os.path.basename(f)))
    p2 = subprocess.run([sys.executable, os.path.join(depot, POS), depot], capture_output=True, text=True, timeout=300)
    same = all(filecmp.cmp(os.path.join(depot, f), os.path.join(snap, os.path.basename(f)), shallow=False) for f in fichiers)
    res.append(("T2 le programme des positions deux fois sur les vraies données : la seconde ne change rien",
                p1.returncode == 0 and p2.returncode == 0 and same))
    # W1 — le pas qui décide, JOUÉ comme GitHub le joue (bash -e), avec un faux programme qui rend 0, 10 puis 1 ; la
    # recherche de textes seule laissait passer le retrait de `set +e` et un code écrit en dur (relecteur, 01-10-2026)
    import yaml
    wf = yaml.safe_load(open(os.path.join(depot, WF), encoding="utf-8"))
    pas = {x.get("id") or x.get("name"): x for x in wf["jobs"]["rattrapage"]["steps"]}
    bloc = pas["faut"]["run"]
    lus = []
    for voulu in (0, 10, 1):
        sortie = os.path.join(tmp, "sortie_%d" % voulu)
        open(sortie, "w").close()
        faux = bloc.replace('python3 programmes/FAUT_IL_RATTRAPER.py "$GITHUB_WORKSPACE"',
                            f'{sys.executable} -c "import sys; sys.exit({voulu})"')
        q = subprocess.run(["bash", "-e", "-c", faux], env=dict(os.environ, GITHUB_OUTPUT=sortie, GITHUB_WORKSPACE=depot),
                           capture_output=True, text=True, timeout=30)
        lus.append((q.returncode, open(sortie).read().strip()))
    ok_w1 = lus == [(0, "code=0"), (0, "code=10"), (0, "code=1")] and bloc.count("FAUT_IL_RATTRAPER.py") == 1
    res.append(("W1 le pas qui décide, joué sous bash -e : il passe et écrit code=0, 10 puis 1", ok_w1))
    relance = next(x for x in wf["jobs"]["rattrapage"]["steps"] if "gh workflow run" in str(x.get("run", "")))
    rougit = [x for x in wf["jobs"]["rattrapage"]["steps"] if "exit 1" in str(x.get("run", ""))]
    res.append(("W2 horaire, s'il y en a un, mardi-samedi, droit de lancer, relance si code ≠ 0 vers la branche par défaut avec "
                "rattrapage=true, rougit si ni 0 ni 10",
                all(h["cron"].split()[4] == "2-6" for h in ((wf[True] or {}).get("schedule") or []))
                and wf["permissions"].get("actions") == "write"
                and relance.get("if") == "steps.faut.outputs.code != '0'"
                and "collecte_abc.yml" in relance["run"] and "github.event.repository.default_branch" in relance["run"]
                and "-f rattrapage=true" in relance["run"]
                and len(rougit) == 1 and rougit[0].get("if") == "steps.faut.outputs.code != '0' && steps.faut.outputs.code != '10'"))
    cw = yaml.safe_load(open(os.path.join(depot, ".github/workflows/collecte_abc.yml"), encoding="utf-8"))
    mes = [x for x in cw["jobs"]["collecte"]["steps"] if "MESURER_LA_PERFORMANCE" in str(x.get("run", ""))]
    # la commande de la mesure est JOUÉE, l'entrée remplacée comme GitHub la remplace : « true » puis « false »
    joue = []
    for val in ("true", "false", ""):   # "" : l'horaire du soir n'a pas d'entrée
        cmd = mes[0]["run"].replace("${{ inputs.rattrapage }}", val).replace(
            'python3 "programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py" "$GITHUB_WORKSPACE"', "echo MESURE_LANCEE") if mes else ""
        q = subprocess.run(["bash", "-e", "-c", cmd], capture_output=True, text=True, timeout=30)
        joue.append((q.returncode, "MESURE_LANCEE" in q.stdout))
    res.append(("W3 le circuit : entrée « rattrapage » ; la mesure, jouée, est sautée à la relance et lancée sinon ; un seul "
                "circuit à la fois", "rattrapage" in (cw[True]["workflow_dispatch"] or {}).get("inputs", {})
                and len(mes) == 1 and joue == [(0, False), (0, True), (0, True)]
                and isinstance((cw.get("concurrency") or {}).get("group"), str) and "${{" not in cw["concurrency"]["group"]
                and (cw.get("concurrency") or {}).get("cancel-in-progress") is False))
    return res


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — Dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — Le lancement du fichier.
    ③ ENTRÉE — La ligne de commande.
    ④ CONDITIONS D'ENTRÉE — La racine donnée est un dépôt complet (programmes, données, circuits).
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier le dépôt sans son historique, saboter, jouer, compter les rouges.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée puis efface des copies jetables ; affiche un compte rendu.
    ⑪ TERMINAISON — Rend la main par son code.
      [sort: non]
    """
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        tmp = tempfile.mkdtemp(prefix="rattrapage_")
        try:
            depot = os.path.join(tmp, "depot")
            shutil.copytree(DEPOT, depot, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            for f, a, b in SABOTAGES[sab]:
                t = open(os.path.join(depot, f), encoding="utf-8").read()
                if t.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple dans {f}")
                    return 2
                open(os.path.join(depot, f), "w", encoding="utf-8").write(t.replace(a, b))
            res = epreuves(depot, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        rouges = [x for x, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for x in rouges:
            print("     ROUGE " + x)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
