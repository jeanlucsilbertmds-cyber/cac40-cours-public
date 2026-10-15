#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_HORAIRE_DU_CIRCUIT — Mar 13-10-2026 (Paris)
Rôle : prouver que le circuit public ne travaille qu'au bon moment — jamais pendant la séance ni avant la clôture
définitive, une seule fois par séance, la mesure datée par sa séance — et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/FAUT_IL_TOURNER.py ou programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py
(R-731).

À QUOI ÇA SERT. Décision de Jean-Luc du 13-10-2026 : le circuit part au plus tôt après la clôture (18h07), avec un secours
le soir (21h23) et un rattrapage le matin (7h41). GitHub compte en heure universelle, qui ne suit pas l'heure d'été : le
circuit est réveillé quatre fois, et programmes/FAUT_IL_TOURNER.py décide à l'heure de Paris. Deux fautes coûtent : tourner
avant 18h (la séance du jour manque, et la mesure de la journée, écrite trop tôt, empêche celle du soir) ; ne pas tourner
quand la séance n'est pas finie (ses signaux sont perdus pour toujours).

LES ÉPREUVES — chaque décision est lancée en ligne de commande à une heure de Paris FIXÉE (tests/HORLOGE_D_EPREUVE.py),
sur un petit dépôt qui porte le VRAI calendrier (fabriqué par `depot_de_decision`, emprunté aux épreuves du rattrapage) :
H1 mercredi 14-10 à 17h07, travail du 13-10 fait : ne pas tourner (la veille est faite, le jour n'est pas clos) ;
H2 14-10 à 17h59, rien de fait depuis le 12-10 : tourner pour rattraper le 13-10, mesure gardée ;
H3 14-10 à 18h00, travail du 13-10 fait : tourner, sans sauter la mesure ;
H4 14-10 à 18h07, travail du 14-10 fait (radar 18:20) : ne pas tourner ;
H5 14-10 à 21h23, travail du 14-10 fait : ne pas tourner ;
H6 14-10 à 21h23, signaux du 13-10 : tourner, sans sauter la mesure ;
H7 jeudi 15-10 à 07h41, signaux du 13-10 : tourner, mesure gardée ;
H8 15-10 à 07h41, travail du 14-10 fait : ne pas tourner ;
H9 15-10 à 08h59, signaux du 13-10 : tourner, mesure gardée ; H10 15-10 à 09h00, de même : AUCUNE fenêtre en
    journée (le 14-10, le réveil de 7h41 est parti à 12h37 et une fenêtre 9h-18h l'avait arrêté — cassure K) ;
H11 lancé à la main, à 12h00 comme à 20h00 : tourner, et sauter la mesure seulement si la case est cochée ;
H12 calendrier absent à 18h07 : tourner par précaution, code 1 ;
H13 samedi 17-10 à 07h41 : travail du 16-10 fait, ne pas tourner ; signaux du 15-10, tourner, mesure gardée ;
H14 vendredi 25-12 (fermé) à 18h07, travail du 24-12 fait : ne pas tourner ;
H15 mardi 27-10 (heure d'hiver) à 17h07 : ne pas tourner ; à 18h07, signaux du 26-10 : tourner ;
H16 les deux sorties écrites pour GitHub, exactement ; H17 sans les trois arguments : code 1 ;
H18 sur les VRAIES données du dépôt, à 23h10 le 13-10 : le travail du 13-10 est fait (le lancement à la main du Chat) ;
H19 le cas réel du 14-10 : réveil à 12h37, la veille (13-10) manquante : tourner, mesure gardée ; la veille faite :
    ne pas tourner ;
H20 la décision plante (FAUT_IL_RATTRAPER.py retiré d'une copie) : tourner par précaution, code 1, mesure gardée ;
M1 la mesure de la performance, lancée sur une copie des VRAIES données à 00h17 le lendemain de la dernière séance
   versée : elle se date de cette séance, jamais du jour d'horloge (cassure J, décision de Jean-Luc du 14-10-2026 à
   18h50) ;
M2 une séance nouvelle (le jour ouvré qui suit la dernière séance versée) ajoutée à la copie : la mesure à 00h17 le
   lendemain écrit autant de lignes datées de cette séance que la séance précédente en avait, aucune du lendemain
   (le cas positif : S21, une mesure qui n'écrit rien, doit rougir).
   M1 ET M2 SE DATENT DEPUIS LES DONNÉES (15-10-2026) : écrites avec le 14-10 et le 15-10 en dur, elles devenaient
   fausses dès que le circuit versait la séance du 14-10 — S21 ne mordait plus, la séance « nouvelle » existant déjà.
DEPUIS LE 14-10-2026, AUCUN RÉVEIL PLANIFIÉ NE SAUTE LA MESURE (elle est datée par sa séance) : les épreuves H attendent
rattrapage=false partout, sauf à la main case cochée.
C1 le circuit public fabriqué : les quatre réveils, aucun à l'heure pile ; le job `collecte` attend `faut_il_tourner` et
   ne tourne que sur « true » ; plus aucun `inputs.rattrapage` dans ce job ; le job de décision passe la case et rougit
   sur un code non nul ;
C2 la commande de la mesure du circuit public, JOUÉE sous bash avec « true », « false » et vide : sautée seulement avec « true » ;
C3 le fabricant refuse un circuit privé sans `${{ inputs.rattrapage }}`, puis un job qui ne s'appelle pas `collecte` ;
C4 le pas de décision du circuit public, JOUÉ sous bash -e comme sur GitHub (ETAPE_MUETTE.py lance `bash -e`), avec un
   faux programme qui rend 1 : le pas passe et écrit code=1 ;
C5 les deux jobs rejoués sur des dépôts git locaux, avec les vrais pas et le vrai ETAPE_MUETTE.py : le journal poussé par
   le job de décision ne fait pas tomber le premier commit du job du circuit (relecture du 13-10-2026).
LES SABOTAGES : S1 une fenêtre 9h-18h remise (H10, H19a) · S2 l'heure de clôture écrite en dur à 17 (H2) · S3 le soir n'attend
plus la séance du jour (H3) · S4 la mesure jamais sautée le matin (H7) · S5 « déjà fait » fait tourner (H4) · S6 la case
ignorée à la main (H11) · S7 l'indécis ne tourne pas (H12) · S8 la sortie « tourner » mal écrite (H16) · S9 le lancement à
la main soumis à la fenêtre (H11) · S10 le job du circuit sans condition (C1) · S11 la case du privé non remplacée (C1, C2) ·
S12 un réveil à l'heure pile (C1) · S13 « tourner » sauf « false » (C1) · S14 `set +e` retiré du pas de décision (C4) ·
S15 la garde sur la case du privé retirée (C3) · S16 le rattrapage du lundi au vendredi (C1) · S17 le journal nommé sans
le job (C5) · S18 la mesure non sautée à la main avant 18h (H11b) · S19 la mesure sautée quand la décision
plante (H20) · S20 la mesure datée par l'horloge (M1) · S4 un réveil planifié qui saute la mesure avant 18h (H2…) ·
S6 la case ignorée (H11a) · S18 la mesure toujours sautée à la main (H11b).

USAGE : python3 tests/EPREUVES_DE_L_HORAIRE_DU_CIRCUIT_Mar_13-10-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import importlib.util, os, re, shlex, shutil, subprocess, sys, tempfile
from datetime import date, timedelta

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HORLOGE_D_EPREUVE import lancer_a_l_heure                        # l horloge, posée à un seul endroit (R-708)
_sp = importlib.util.spec_from_file_location(   # le cas d'épreuve, écrit une fois (R-708) ; nom de fichier à tirets
    "epreuves_du_rattrapage", os.path.join(os.path.dirname(os.path.abspath(__file__)), "EPREUVES_DU_RATTRAPAGE_Jeu_01-10-2026.py"))
_R = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_R)
depot_de_decision = _R.depot_de_decision

TOURNER = "programmes/FAUT_IL_TOURNER.py"
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
SABOTAGES = {
    "Z0": [],
    "S1_fenetre_remise": [(TOURNER, "    soir = maintenant.hour >= cloture\n", "    if 9 <= maintenant.hour < cloture:\n        return DECIDE, False, False, ['fenêtre']\n    soir = maintenant.hour >= cloture\n")],
    "S2_cloture_en_dur": [(TOURNER, 'cloture = _module("COLLECTER_ABC_GITHUB.py").HEURE_CLOTURE_PARIS', "cloture = 17")],
    "S3_soir_sans_seance_du_jour": [(TOURNER, "(timedelta(days=1) if soir else timedelta(0))", "timedelta(0)")],
    "S4_reveil_saute_la_mesure": [(TOURNER, "    rattrapage = False      # la mesure est datée par sa séance : aucun réveil planifié ne la saute\n", "    rattrapage = not soir\n")],
    "S5_deja_fait_tourne": [(TOURNER, 'return DECIDE, False, rattrapage, [f"⏹️', 'return DECIDE, True, rattrapage, [f"⏹️')],
    "S6_case_ignoree": [(TOURNER, '        r = case_rattrapage == "true"\n', "        r = False\n")],
    "S7_indecis_ne_tourne_pas": [(TOURNER, "return INDECIS, True, rattrapage, [", "return INDECIS, False, rattrapage, [")],
    "S8_sortie_mal_ecrite": [(TOURNER, 'f.write(f"tourner=', 'f.write(f"tourne=')],
    "S9_main_soumise_a_la_fenetre": [(TOURNER, '    if evenement != "schedule":\n', '    if evenement == "jamais":\n')],
    "S10_job_sans_condition": [(FAB, "corps = corps.replace(JOB_PRIVE, JOB_CONDITION, 1).replace(", "corps = corps.replace(")],
    "S11_case_non_remplacee": [(FAB, ".replace(RATTRAPAGE_PRIVE, RATTRAPAGE_PUBLIC)\n", "\n")],
    "S12_reveil_heure_pile": [(FAB, '"7 16 * * 1-5"', '"0 16 * * 1-5"')],
    "S13_tourner_sauf_false": [(FAB, "outputs.tourner == 'true' }}", "outputs.tourner != 'false' }}")],
    "S14_sans_set_plus_e": [(FAB, '          set +e\n          python3 programmes/FAUT_IL_TOURNER.py', '          python3 programmes/FAUT_IL_TOURNER.py')],
    "S15_garde_case_retiree": [(FAB, "    if corps.count(RATTRAPAGE_PRIVE) != 1:\n", "    if False:\n")],
    "S16_rattrapage_lundi_vendredi": [(FAB, '"41 5 * * 2-6"', '"41 5 * * 1-5"')],
    "S17_journal_sans_job": [("programmes/ETAPE_MUETTE.py", ' + "_"\n                               + os.environ.get("GITHUB_JOB", "job-sans-nom")', "")],
    "S19_plantage_mesure_sautee": [(TOURNER, "        code, tourner, rattrapage = INDECIS, True, False", "        code, tourner, rattrapage = INDECIS, True, True")],
    "S20_mesure_datee_par_l_horloge": [("programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py", "    jour = seances[-1]      # la seance mesuree", "    jour = now.strftime('%Y-%m-%d')      # la seance mesuree")],
    "S21_mesure_n_ecrit_rien": [("programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py", "    neuves = [l for l in lignes if (l['date_mesure'], l['strategie'], l['comptabilite']) not in deja]", "    neuves = []")],
    "S18_main_saute_toujours": [(TOURNER, '        r = case_rattrapage == "true"\n', "        r = True\n")],
}
REVEILS = ["7 16 * * 1-5", "7 17 * * 1-5", "23 19 * * 1-5", "41 5 * * 2-6"]


def decision(depot, racine, heure, tmp, evenement="schedule", case=""):
    """Lance FAUT_IL_TOURNER.py à l'heure donnée et rend (code, sortie, sorties pour GitHub).

    ① RÔLE — Emprunter le chemin réel : le programme en ligne de commande, avec un fichier GITHUB_OUTPUT.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `depot` : la copie éprouvée (sabotée ou non) · `racine` : le cas, ou None pour lancer sans argument ·
      `heure` : AAAA-MM-JJTHH:MM:SS, heure de Paris · `tmp` : dossier jetable · `evenement`, `case` : les deux
      autres arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le code de sortie · la sortie standard et d'erreur · le dictionnaire lu dans GITHUB_OUTPUT.
      [rend: 3]
    ⑥ TRAITEMENT — poser GITHUB_OUTPUT, lancer à l'heure fixée, relire le fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ce que lit GitHub, ce sont le code et le fichier, pas la fonction.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus ; écrit puis efface un fichier.
    ⑪ TERMINAISON — Rend la main ; au-delà de 60 secondes, lève.
      [sort: non]
    """
    sortie = os.path.join(tmp, "github_output")
    open(sortie, "w").close()
    os.environ["GITHUB_OUTPUT"] = sortie
    try:
        cmd = [sys.executable, os.path.join(depot, TOURNER)] + ([racine, evenement, case] if racine else [])
        p = lancer_a_l_heure(cmd, heure, os.path.join(tmp, "_horloge"), delai=60)
    finally:
        del os.environ["GITHUB_OUTPUT"]
    lu = dict(l.split("=", 1) for l in open(sortie).read().splitlines() if "=" in l)
    return p.returncode, p.stdout + p.stderr, lu


def epreuves(depot, tmp):
    """Joue les épreuves sur la copie `depot` et rend la liste (nom, verdict).

    ① RÔLE — Toutes les épreuves de la fiche du fichier.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `depot` : la copie éprouvée · `tmp` : dossier jetable.
    ④ CONDITIONS D'ENTRÉE — La copie porte programmes/ et .github/.
    ⑤ SORTIE — UNE valeur : la liste des couples (nom de l'épreuve et ce qui a été vu, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche du fichier.
    ⑦ UNITÉ — Des heures de Paris.
    ⑧ POURQUOI — Une épreuve par faute possible.
    ⑨ CE QUI CLOCHE — H18 dépend des données du jour : elle dit vrai le 13-10-2026 ; plus tard, son verdict suit le dépôt.
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    res, n = [], [0]

    def cas(radar, seance, **k):
        n[0] += 1
        return depot_de_decision(os.path.join(tmp, f"cas{n[0]}"), radar, seance, **k)

    def voir(nom, racine, heure, tourner, rattrapage=None, code=0, evenement="schedule", case=""):
        c, txt, lu = decision(depot, racine, heure, tmp, evenement, case)
        ok = c == code and lu.get("tourner") == tourner and (rattrapage is None or lu.get("rattrapage") == rattrapage)
        res.append((f"{nom} : code {c}, tourner={lu.get('tourner')}, rattrapage={lu.get('rattrapage')} — "
                    f"{txt.splitlines()[0][:90] if txt else 'rien'}", ok))

    fait13 = cas("2026-10-13 20:21", "2026-10-13")
    fait14 = cas("2026-10-14 18:20", "2026-10-14", calcul="2026-10-14 18:15")
    fait14s = cas("2026-10-14 20:21", "2026-10-14")
    voir("H1 14-10 17h07, fait le 13", fait13, "2026-10-14T17:07:00", "false")
    voir("H2 14-10 17h59, rien depuis le 12", cas("2026-10-12 20:21", "2026-10-12"), "2026-10-14T17:59:00", "true", "false")
    voir("H3 14-10 18h00, fait le 13", fait13, "2026-10-14T18:00:00", "true", "false")
    voir("H4 14-10 18h07, fait le 14", fait14, "2026-10-14T18:07:00", "false")
    voir("H5 14-10 21h23, fait le 14", fait14s, "2026-10-14T21:23:00", "false")
    voir("H6 14-10 21h23, signaux du 13", fait13, "2026-10-14T21:23:00", "true", "false")
    voir("H7 15-10 07h41, signaux du 13", fait13, "2026-10-15T07:41:00", "true", "false")
    voir("H8 15-10 07h41, fait le 14", fait14s, "2026-10-15T07:41:00", "false")
    voir("H9 15-10 08h59, signaux du 13", fait13, "2026-10-15T08:59:00", "true", "false")
    voir("H10 15-10 09h00, signaux du 13", fait13, "2026-10-15T09:00:00", "true", "false")
    voir("H11a à la main 12h00, case cochée", fait14s, "2026-10-14T12:00:00", "true", "true",
         evenement="workflow_dispatch", case="true")
    voir("H11b à la main 12h00, case non cochée : mesure gardée (datée par sa séance)", fait14s,
         "2026-10-14T12:00:00", "true", "false", evenement="workflow_dispatch", case="false")
    voir("H11c à la main 20h00, case non cochée", fait14s, "2026-10-14T20:00:00", "true", "false",
         evenement="workflow_dispatch", case="false")
    voir("H11d à la main 20h00, case cochée", fait14s, "2026-10-14T20:00:00", "true", "true",
         evenement="workflow_dispatch", case="true")
    voir("H12 calendrier absent, 18h07", cas("2026-10-13 20:21", "2026-10-13", calendrier=False),
         "2026-10-14T18:07:00", "true", "false", code=1)
    voir("H13a samedi 17-10 07h41, fait le 16", cas("2026-10-16 20:21", "2026-10-16"), "2026-10-17T07:41:00", "false")
    voir("H13b samedi 17-10 07h41, signaux du 15", cas("2026-10-15 20:21", "2026-10-15"), "2026-10-17T07:41:00",
         "true", "false")
    voir("H14 vendredi 25-12 18h07, fait le 24", cas("2026-12-24 20:21", "2026-12-24"), "2026-12-25T18:07:00", "false")
    hiver = cas("2026-10-26 20:21", "2026-10-26")
    voir("H15a mardi 27-10 (hiver) 17h07", hiver, "2026-10-27T17:07:00", "false")
    voir("H15b mardi 27-10 (hiver) 18h07", hiver, "2026-10-27T18:07:00", "true", "false")
    c, txt, lu = decision(depot, fait13, "2026-10-14T18:07:00", tmp)
    res.append((f"H16 sorties pour GitHub exactement {{tourner, rattrapage}} : {sorted(lu)}",
                sorted(lu) == ["rattrapage", "tourner"]))
    c, txt, lu = decision(depot, None, "2026-10-14T18:07:00", tmp)
    res.append((f"H17 sans argument : code {c}", c == 1 and "usage" in txt))
    voir("H18 vraies données, 13-10 23h10", DEPOT, "2026-10-13T23:10:00", "false")
    voir("H19a 14-10 12h37, veille manquante", cas("2026-10-12 20:21", "2026-10-12"), "2026-10-14T12:37:00", "true", "false")
    voir("H19b 14-10 12h37, veille faite", fait13, "2026-10-14T12:37:00", "false")
    # H20 : la décision plante (FAUT_IL_RATTRAPER absent) — tourner par précaution, la mesure gardée après 18h
    mutile = os.path.join(tmp, "mutile")
    shutil.copytree(os.path.join(depot, "programmes"), os.path.join(mutile, "programmes"))
    os.remove(os.path.join(mutile, "programmes", "FAUT_IL_RATTRAPER.py"))
    for nom, h, attendu in (("H20a plantage à 20h23", "2026-10-14T20:23:00", "false"),
                            ("H20b plantage à 12h00", "2026-10-14T12:00:00", "false")):
        c, txt, lu = decision(mutile, fait13, h, tmp)
        res.append((f"{nom} : code {c}, tourner={lu.get('tourner')}, rattrapage={lu.get('rattrapage')}",
                    c == 1 and lu.get("tourner") == "true" and lu.get("rattrapage") == attendu))

    # M1 — la mesure datée par sa séance : vraies données (dernière séance versée), horloge à 00h17 le 15-10
    donnees = os.path.join(tmp, "donnees_reelles")
    shutil.copytree(DEPOT, donnees, ignore=shutil.ignore_patterns(".git", "archives", "etudes", "tests", "temoins", "programmes"))
    shutil.copytree(os.path.join(depot, "programmes"), os.path.join(donnees, "programmes"))
    hist = os.path.join(donnees, "donnees", "historique_mesures.csv")
    avant = set(l.split(",", 1)[0] for l in open(hist, encoding="utf-8"))
    derniere = max(l.split(",", 2)[1] for l in open(os.path.join(donnees, "donnees", "cours_maitre.csv"), encoding="utf-8")
                   if l[:1].isalpha() and l.count(",") >= 2 and l.split(",", 2)[1][:2] == "20")
    lendemain_1 = (date.fromisoformat(derniere) + timedelta(days=1)).isoformat()
    p = lancer_a_l_heure([sys.executable, os.path.join(donnees, "programmes", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py"),
                          donnees, donnees], f"{lendemain_1}T00:17:00", os.path.join(tmp, "_horloge_m"), delai=300)
    apres = set(l.split(",", 1)[0] for l in open(hist, encoding="utf-8"))
    vu = next((l for l in p.stdout.splitlines() if l.startswith("seance mesuree")), "rien")
    res.append((f"M1 mesure à 00h17 le {lendemain_1} : « {vu[:40]} », dates ajoutées {sorted(apres - avant)} (dernière séance {derniere})",
                p.returncode == 0 and vu.startswith(f"seance mesuree : {derniere}") and lendemain_1 not in apres
                and apres - avant <= {derniere}))
    # M2 — le cas POSITIF (relecture du 14-10-2026 : M1 resterait vert si rien ne s'écrivait) : une séance nouvelle,
    # le 14-10, copiée du 13-10 pour chaque valeur, puis la mesure à 00h17 le 15-10 : des lignes datées du 14-10,
    # autant que la séance précédente en avait, et aucune du 15-10
    maitre = os.path.join(donnees, "donnees", "cours_maitre.csv")
    lignes_m = open(maitre, encoding="utf-8").read().splitlines()
    nouvelle = date.fromisoformat(derniere) + timedelta(days=1)
    while nouvelle.weekday() >= 5:
        nouvelle += timedelta(days=1)
    nouvelle, lendemain_2 = nouvelle.isoformat(), (nouvelle + timedelta(days=1)).isoformat()
    neuves_m = [l.replace(f",{derniere},", f",{nouvelle},", 1) for l in lignes_m if l.split(",")[1:2] == [derniere]]
    open(maitre, "a", encoding="utf-8").write("\n".join(neuves_m) + "\n")
    par_date = {}
    for l in open(hist, encoding="utf-8"):
        par_date[l.split(",", 1)[0]] = par_date.get(l.split(",", 1)[0], 0) + 1
    attendu = par_date.get(derniere, 0)
    p = lancer_a_l_heure([sys.executable, os.path.join(donnees, "programmes", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py"),
                          donnees, donnees], f"{lendemain_2}T00:17:00", os.path.join(tmp, "_horloge_m"), delai=300)
    dates = [l.split(",", 1)[0] for l in open(hist, encoding="utf-8")]
    res.append((f"M2 séance nouvelle du {nouvelle} ({len(neuves_m)} valeurs), mesure à 00h17 le {lendemain_2} : "
                f"{dates.count(nouvelle)} ligne(s) du {nouvelle} (attendu {attendu}), {dates.count(lendemain_2)} du {lendemain_2}",
                p.returncode == 0 and attendu > 0 and nouvelle not in avant and dates.count(nouvelle) == attendu
                and lendemain_2 not in dates))

    # C — le circuit public fabriqué
    pub = os.path.join(tmp, "public")
    p = subprocess.run([sys.executable, os.path.join(depot, FAB), depot, pub], capture_output=True, text=True)
    wf = open(os.path.join(pub, ".github/workflows/circuit_du_soir.yml"), encoding="utf-8").read() if p.returncode == 0 else ""
    reveils = re.findall(r'^\s*- cron: "([^"]+)"', wf, re.M)
    job = wf.split("\n  collecte:\n", 1)[-1] if "\n  collecte:\n" in wf else ""
    decide = wf.split("\n  faut_il_tourner:\n", 1)[-1].split("\n  collecte:\n", 1)[0] if "\n  faut_il_tourner:\n" in wf else ""
    ok = (p.returncode == 0 and reveils == REVEILS and all(not r.startswith("0 ") for r in reveils)
          and job.startswith("    needs: faut_il_tourner\n    if: ${{ !cancelled() && needs.faut_il_tourner.outputs.tourner == 'true' }}\n")
          and "inputs.rattrapage" not in job and "needs.faut_il_tourner.outputs.rattrapage" in job
          and '"${{ github.event_name }}" "${{ inputs.rattrapage }}"' in decide
          and "if: steps.decision.outputs.code != '0'" in decide and "tourner: ${{ steps.decision.outputs.tourner }}" in decide)
    res.append((f"C1 circuit public : code {p.returncode}, réveils {reveils}", ok))
    ligne = next((l.strip() for l in job.splitlines() if "mesure sautée" in l), "")
    vus = []
    for v in ("true", "false", ""):
        cmd = ligne.replace("${{ needs.faut_il_tourner.outputs.rattrapage }}", v) + '\necho "MESURE LANCEE"'
        q = subprocess.run(["bash", "-e", "-c", cmd], capture_output=True, text=True)
        vus.append("sautée" if "mesure sautée" in q.stdout else ("lancée" if "MESURE LANCEE" in q.stdout else "?"))
    res.append((f"C2 la mesure avec true/false/vide : {vus}", bool(ligne) and "rattrapage }}" in ligne
                and vus == ["sautée", "lancée", "lancée"]))
    spec = importlib.util.spec_from_file_location("fab_epreuve", os.path.join(depot, FAB))
    F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
    prive = open(os.path.join(depot, ".github/workflows/collecte_abc.yml"), encoding="utf-8").read()
    refus = []
    for texte in (prive.replace("${{ inputs.rattrapage }}", "true"), prive.replace("\n  collecte:\n", "\n  recolte:\n")):
        try:
            F.fabriquer_le_circuit(texte); refus.append("ACCEPTÉ")
        except ValueError as e:
            refus.append(str(e)[:50])
    res.append((f"C3 refus du fabricant : {refus}", "ACCEPTÉ" not in refus))
    pas = re.search(r"        id: decision\n        run: \|\n((?:          .*\n)+)", decide)
    vu = "pas trouvé"
    if pas:
        faux = os.path.join(tmp, "faux"); os.makedirs(os.path.join(faux, "programmes"), exist_ok=True)
        open(os.path.join(faux, "programmes", "FAUT_IL_TOURNER.py"), "w").write("import sys\nsys.exit(1)\n")
        texte = "\n".join(l[10:] for l in pas.group(1).splitlines()).replace("${{ github.event_name }}", "schedule").replace("${{ inputs.rattrapage }}", "")
        open(os.path.join(tmp, "pas.sh"), "w").write(texte + "\n")
        open(os.path.join(tmp, "go"), "w").close()
        q = subprocess.run(["bash", "-e", os.path.join(tmp, "pas.sh")], cwd=faux, capture_output=True, text=True,
                           env=dict(os.environ, GITHUB_OUTPUT=os.path.join(tmp, "go")))
        vu = f"code {q.returncode}, sortie {open(os.path.join(tmp, 'go')).read().strip()!r}"
    res.append((f"C4 le pas de décision sous bash -e, programme rendant 1 : {vu}", vu == "code 0, sortie 'code=1'"))
    res.append(c5_deux_jobs(depot, wf, tmp))
    return res


def c5_deux_jobs(depot, wf, tmp):
    """Rejoue les deux jobs du circuit public sur des dépôts git locaux et rend (ce qui a été vu, verte ?).

    ① RÔLE — Épreuve C5 : le journal enregistré par le job de décision ne doit pas faire tomber le job du circuit.
    ② CONTEXTE D'APPEL — `epreuves`, une fois.
    ③ ENTRÉE — `depot` : la copie éprouvée (son ETAPE_MUETTE.py) · `wf` : le texte du circuit public fabriqué ·
      `tmp` : dossier jetable.
    ④ CONDITIONS D'ENTRÉE — `git` et le module `yaml` sont présents ; sinon l'épreuve est ROUGE (R-734).
    ⑤ SORTIE — UNE valeur : le couple (texte, booléen).
      [rend: 1]
    ⑥ TRAITEMENT — ① un dépôt d'origine nu, garni de quelques fichiers et d'ETAPE_MUETTE.py · ② job 1 : un pas
      passé par ETAPE_MUETTE, puis le VRAI pas « journal » du job `faut_il_tourner` (il pousse) · ③ job 2 : un clone
      neuf, un pas par ETAPE_MUETTE, puis le VRAI pas « Commiter ce qui a été écrit » du job `collecte` ·
      ④ verte si ce pas sort en 0.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture à mandat inversé du 13-10-2026, prouvée par exécution : les deux jobs écrivaient le
      même fichier de journal ; le second le recevait déjà suivi par git, l'allongeait, et son premier commit
      tombait (« fichier suivi modifié sans être enregistré »). Le circuit tombait à chaque passage qui travaille.
      Adapté du script du relecteur.
    ⑨ CE QUI CLOCHE — Le pas « Commiter » est joué avec un code de collecte écrit à 0.
    ⑩ EFFET — Crée des dépôts git dans `tmp`.
    ⑪ TERMINAISON — Rend la main ; chaque commande a un délai de 60 secondes.
      [sort: non]
    """
    try:
        import yaml
        d = yaml.safe_load(wf)
        pas = lambda job, i: next(x for x in d["jobs"][job]["steps"] if x.get("id") == i)["run"]
        journal, commit = pas("faut_il_tourner", "journal"), pas("collecte", "commiter_ce_qui_a_ete_ecrit_cours_et_r")
    except Exception as e:
        return (f"C5 deux jobs : circuit illisible ({type(e).__name__}: {str(e)[:60]})", False)
    W = os.path.join(tmp, "c5")
    os.makedirs(W)
    sh = lambda c, cwd, env=None: subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True,
                                                  timeout=60, env=env)
    sh("git init -q --bare -b main origin.git && git clone -q origin.git seed", W)
    seed = os.path.join(W, "seed")
    for f in ("donnees/claude_cours_nouveaux.csv", "rapports/collecte_abc_x.md"):
        os.makedirs(os.path.dirname(os.path.join(seed, f)), exist_ok=True)
        open(os.path.join(seed, f), "w").write("x\n")
    os.makedirs(os.path.join(seed, "programmes"))
    shutil.copy(os.path.join(depot, "programmes", "ETAPE_MUETTE.py"), os.path.join(seed, "programmes"))
    sh("git add -A && git -c user.name=a -c user.email=a@b commit -qm init && git push -q origin main", seed)
    base = dict(os.environ, GITHUB_RUN_ID="4242", GITHUB_RUN_ATTEMPT="1", GITHUB_OUTPUT=os.path.join(W, "out"))

    def etape(rep, job, ident, texte):
        f = os.path.join(W, ident + ".sh")
        open(f, "w").write(texte)
        e = dict(base, GITHUB_WORKSPACE=rep, GITHUB_ACTION=ident, GITHUB_JOB=job)
        return subprocess.run([sys.executable, "programmes/ETAPE_MUETTE.py", f], cwd=rep, env=e,
                              capture_output=True, text=True, timeout=60).returncode

    sh("git clone -q origin.git job1", W)
    j1 = os.path.join(W, "job1")
    etape(j1, "faut_il_tourner", "decision", "echo decision")
    r1 = sh("bash -e -c " + shlex.quote(journal), j1, dict(base, GITHUB_WORKSPACE=j1))
    sh("git clone -q origin.git job2", W)
    j2 = os.path.join(W, "job2")
    etape(j2, "collecte", "collecte", "echo b >> donnees/claude_cours_nouveaux.csv")
    c = etape(j2, "collecte", "commiter_ce_qui_a_ete_ecrit_cours_et_r",
              commit.replace("${{ steps.collecte.outputs.code }}", "0"))
    return (f"C5 deux jobs : journal du job 1 {r1.returncode} ({r1.stdout.strip()[:30]}), commit du job 2 : code {c}",
            r1.returncode == 0 and "enregistre" in r1.stdout and c == 0)


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — Dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — Le lancement du fichier.
    ③ ENTRÉE — La ligne de commande.
    ④ CONDITIONS D'ENTRÉE — La racine donnée porte programmes/, .github/, donnees/, rapports/ et
      tests/LANCEMENT_DES_EPREUVES.json.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier programmes/, .github/ et le fichier de lancement des épreuves, saboter,
      jouer, compter les rouges.
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
        tmp = tempfile.mkdtemp(prefix="horaire_")
        try:
            depot = os.path.join(tmp, "depot")
            for d in ("programmes", ".github"):
                shutil.copytree(os.path.join(DEPOT, d), os.path.join(depot, d), ignore=shutil.ignore_patterns("__pycache__"))
            # le fichier de lancement des épreuves : le fabricant du circuit public refuse un dépôt qui ne le porte pas
            # (15-10-2026, la certification passe au public, A-576)
            os.makedirs(os.path.join(depot, "tests"))
            shutil.copy(os.path.join(DEPOT, "tests", "LANCEMENT_DES_EPREUVES.json"), os.path.join(depot, "tests"))
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
        for x in (rouges if sab != "Z0" else [x for x, _ in res]) if sab == "Z0" or rouges else []:
            print("     " + ("ROUGE " if x in rouges else "verte ") + x)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
