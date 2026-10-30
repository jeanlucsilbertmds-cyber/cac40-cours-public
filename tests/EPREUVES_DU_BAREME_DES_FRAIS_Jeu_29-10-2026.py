#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_BAREME_DES_FRAIS — Jeu 29-10-2026 (Paris)
DÉCIDÉ · Rôle : garder au dépôt les frais réels de A-550 (taxe sur les transactions financières comprise), lus dans
UN barème daté, et interdire qu'un taux de frais soit de nouveau écrit en dur dans un programme.
Quand l'appeler : avant toute livraison qui touche les frais, le module des positions, le juge des stratégies, le
point mort, le journal des trades ou le radar (R-755 ②) ; la certification la rejoue à chaque version.

À QUOI ÇA SERT. Jusqu'au 29-10-2026, les frais étaient un taux unique, 0,15 % par ordre (`FRAIS_TAUX`), recopié à
plusieurs endroits, et la taxe de 0,4 % à l'achat des valeurs françaises de plus d'un milliard d'euros n'existait
nulle part dans le code (ÉTUDE 18, `etudes/ETUDE_18_FRAIS_REELS_Jeu_08-10-2026_09h29.md`, validée par Jean-Luc le
08-10-2026 à 10h12). Depuis A-550 ②, UNE fonction (`MODULE_POSITIONS.cout_d_un_ordre`) lit le barème daté
(`donnees/BAREME_FRAIS.csv`) et la liste annuelle des valeurs taxées (`donnees/VALEURS_TTF.csv`) ; tous les
programmes l'appellent. Exemple : achat de 100 000 € de Bureau Veritas le 27-07-2026 — 150 € de courtage et 400 € de
taxe ; même achat d'Airbus, non taxée — 150 € et 0 €.

CE QUE CE FICHIER ÉPROUVE (Z0, tout doit être vert) :
  E1 le garde-fou de l'ÉTUDE 18 (A4) : aucun programme du dépôt (`programmes/` et ses sous-dossiers,
     `etudes/outils/`, la racine) n'écrit un nombre en dur sous un nom de variable, de paramètre, d'argument nommé
     ou de clé qui contient « frais », « ttf » ou « courtage », ni ne passe un `taux=` chiffré à `pnl_net`,
     `frais_ordre` ou `cout_d_un_ordre` — sauf un nombre dont l'EMPLACEMENT (fichier, dictionnaire, clé) est déclaré
     dans `programmes/CONTRATS_DES_FICHIERS.py` (`EXEMPTIONS_DU_GARDE_FOU_DES_FRAIS`), jamais par sa valeur.
     CE GARDE-FOU PAR LES NOMS EST UN FILET CONTRE L'OUBLI, PAS UNE PREUVE (décision de Jean-Luc du 17-10-2026 à
     16h10 sur les contrôles de forme) : `brut - 300.0` passe sous lui. La preuve est E10, par la propriété. Le motif
     est CALIBRÉ : il doit trouver les cinq copies du taux relevées le 29-10-2026 sur la version d'avant
     (`FRAIS = 300.0`, deux `FRAIS_TAUX = 0.0015`, `taux=0.0015`, `frais_pct: float = 0.0025`) — voir E1bis.
  E1bis le motif retrouve chacun de ces cinq cas sur un texte fabriqué, et ne retient pas `timeout=300`.
  E2 le calibrage de `programmes/MODULE_POSITIONS.py` passe : les trois montants du journal sous leur barème
     d'époque, la taxe (400,00 €, 300,00 € avant le 01-04-2025, 0,00 € pour Airbus, 0,00 € à la vente), le courtage.
  E3 le calibrage du teneur de positions passe, Unibail sous le barème réel compris (−3 196,25 €, journal « REEL »).
  E4 le calibrage du module de jugement passe, point mort de 49,25 % sur une valeur taxée compris.
  E5 les deux fichiers du barème suivent leur contrat (en-tête lu, confronté à `CONTRATS_DES_FICHIERS`).
  E6 VRAIES LIGNES (R-732) : chaque montant du journal des trades se refait au centime sous le barème que sa ligne
     nomme (`bareme_reel`, `bareme_convention`).
  E7 le juge des stratégies paie la taxe : un achat de Bouygues à 100,00 € le 30-04-2026 revendu à l'objectif de
     +4 % le lendemain rend 4 000 − 150 − 400 − 156 = +3 294,00 € ; sous le courtage seul, +3 694,00 €.
  E8 (superviseur R-759, C3) le teneur de positions, quand les frais ne se chiffrent pas (liste des valeurs taxées
     absente pour 2023), LAISSE la position ouverte et écrit la raison dans sa case `frais_non_chiffrables` ; et quand
     le calcul des frais lève une AUTRE erreur (`KeyError`), il LÈVE au lieu de l'avaler.
  E9 (C3, C4, C12) le radar, maillon 10bis, À UNE DATE FIXÉE (29-10-2026, par l'horloge d'épreuve du dépôt,
     `tests/HORLOGE_D_EPREUVE.py`), rougit sur quatre fautes posées dans une copie : un montant du journal décalé de
     2 €, une position à la vente bloquée, une valeur d'univers retirée de la liste de l'année, et un trade vendu le
     jour de la mise en service sous une étiquette historique (montant juste, seule l'étiquette est fausse).
  E9bis le même radar le 05-12-2026, sans liste de l'année suivante : ⚠ (l'alerte de décembre).
  E10 (C5, C10, C11) PROPRIÉTÉ — dans une copie, le barème réel est remplacé par un BARÈME PIÈGE : courtage 0,21 %,
     taxe 0,57 % jusqu'au 30-04-2026 puis 0,13 % à partir du 01-05-2026, et la liste 2026 RETOURNÉE pour Airbus (taxée)
     et Bouygues (non taxée). Chaque chemin qui chiffre un trade doit rendre ce que le piège prédit, calculé À LA MAIN
     dans cette épreuve (jamais par `cout_d_un_ordre`, sinon l'épreuve se vérifierait elle-même) : un chemin qui
     n'irait pas lire le barème ne bougerait pas. Achat d'Airbus à 100 € le 04-05-2026, vente à 104 € : le lendemain
     4 000 − 210 − 130 − 218,40 = +3 441,60 € ; le jour même, sans taxe, +3 571,60 €. Les chemins : `pnl_net`,
     `jouer_une_entree` du juge, `_c5e10_sortie`, `cloturer` du teneur, `point_mort_en_fractions`, `sortie_position`. ET L'ÉPREUVE CHERCHE
     ELLE-MÊME, dans l'arbre syntaxique de `programmes/*.py`, toute fonction qui appelle un calcul de frais : une
     fonction trouvée qui n'est ni éprouvée ici ni un contrôle (calibrage, radar) rougit.
  E12 (C1) AUCUN NOM LU N'EST JAMAIS DÉFINI dans `programmes/*.py` (pyflakes, « undefined name ») : le 29-10-2026, la
     suppression par plage de lignes d'une variable de frais avait emporté `GRILLE` du juge à huit critères, et rien
     ne l'a vu avant le relecteur. pyflakes absent = ROUGE (un contrôle qui n'a pas pu tourner ne passe pas, R-734) ;
     il s'installe par `pip install pyflakes`.
  E11 (C7) la mesure de la performance, verdicts aux vrais frais (le cas d'après la décision de Jean-Luc), quand une
     valeur JOUÉE manque à la liste de l'année de son achat : elle écrit toutes ses lignes, dit « point mort non
     chiffrable : … » dans `verdict_c7` de chaque ligne touchée, et rend 1 (R-734). Depuis la méthode A (décision de
     Jean-Luc du 29-10-2026 à 21h28), seules les valeurs jouées comptent, à l'année de LEUR ACHAT : l'épreuve lit au
     journal de la copie la valeur jouée sur le plus de lignes (au 29-10-2026 : Unibail, URW, achetée le 21-08-2026)
     et la retire de la liste de chaque année où elle a été achetée — aucune année en dur (relecture de la barre A,
     I2) ; les lignes qui doivent dire « non chiffrable » se déduisent des noms de chaque stratégie vivante au contrat.
  E11bis la mesure n'attrape QUE cette exception-là : un barème corrompu la fait lever, sans rien écrire.
  E14 (relecteur T2, D2 ; décisions de Jean-Luc du 29-10-2026 à 19h16 et à 21h28) LE BARÈME DES VERDICTS : sans
     barème donné, le juge et le point mort publié se chiffrent sous `MODULE_POSITIONS.BAREME_DES_VERDICTS`, aux vrais
     frais (Bouygues, taxée en 2026, revendue le lendemain : +3 294,00 €) ; le point mort publié est la MOYENNE des
     opérations reçues, chacune à sa valeur et à sa date d'achat (méthode A) : Bouygues 2026 (0,4 %), Airbus 2026
     (non taxée), Bouygues 2025 avant le 01-04 (0,3 %) → 46,68 % ; aucune opération → aucun point mort.
  E15 le VRAI `jouer` du juge, sur C5E10-QA-V1 et le maître, au barème piège de E10 : chaque opération paie les frais
     calculés à la main, et son gain est la variation moins ses frais. E15bis le VRAI `juger` demande le point mort
     moyen des opérations JUGÉES (les mêmes, une seule fois), sous le barème donné, et ce point mort vaut la moyenne
     calculée à la main au barème piège (méthode A, décision de Jean-Luc du 29-10-2026 à 21h28).
  E16 une borne du barème mal écrite (« 2026-5-1 ») lève en nommant la borne.
  E17 (relecture de Cowork du 29-10-2026, défaut 1) DEUX BARÈMES, DEUX ÉTIQUETTES : la vraie mesure, lancée deux fois
     sur deux copies qui ne diffèrent que par `BAREME_DES_VERDICTS` (HIST_COURTAGE_SANS_TTF, puis REEL), écrit des
     lignes dont chaque `verdict_c7` à point mort se termine par « (bareme <celui de sa copie>) », et partout où le
     point mort diffère, le verdict diffère. Aucun calcul n'est refait : on compare deux sorties du vrai programme.
     Exemple réel : « echantillon insuffisant (bareme HIST_COURTAGE_SANS_TTF) » à 43,1 % contre « … (bareme REEL) »
     à 49,2 %.
  E18 (relecture de Cowork, défaut 2 ; superviseur T3) UN JOURNAL SANS GAIN NI PERTE, SUR DES COURS QUI NE BOUGENT
     PAS, DONNE UNE MESURE SANS GAIN NI PERTE : les vraies lignes du journal (gain mis à 0, prix d'entrée à 100), le
     vrai calendrier du maître (cours aplatis à 100), les vraies `courbe_capital` et `stats` — courbe plate au capital,
     cumul nul, pire chute nulle. Elle voit tout montant AJOUTÉ par une colonne dérivée (le forfait de 300 € posé par
     Cowork dans la courbe : 66 points à −300 €) ; elle ne voit PAS une erreur proportionnelle au montant (un gain
     multiplié par 0,99 reste nul à zéro) — limite écrite à A-635. DEPUIS LE SUPERVISEUR R-759 T4 (R2), UNE PROPRIÉTÉ
     ET NON UNE LISTE : la vraie `ligne` est appelée, et TOUTE colonne publiée dont le nom finit par `_eur` (liste lue
     dans `COLONNES` du programme) doit valoir 0, et le rapport gain/secousses « non calculable » (courbe plate). Hors
     de la propriété : `pire_chute_pct` et `facteur_profit`, qui ne finissent pas par `_eur`. LIMITES DÉCLARÉES
     (relecture de Cowork du 29-10-2026, tour 3, défaut 2 ; superviseur R-759 T5, R2) : ① la propriété repose sur une
     CONVENTION DE NOMMAGE que rien ne contrôle — une colonne en euros dont le nom ne finit pas par `_eur` lui échappe
     (mutation « Me » de Cowork : une colonne `gain_moyen` = espérance − 300 € → 25 vertes, 0 rouge) ; la propriété plus
     forte (chaque colonne déclare son unité au contrat MESURE) est au BACKLOG A-635 ⑬ ; ② le scénario est à gain nul :
     une erreur qui s'annule quand l'espérance vaut zéro n'est pas vue (mutation « Mf » : −300 € seulement si
     l'espérance n'est pas nulle → 25 vertes, 0 rouge), de la même famille que le « × 0,99 » ci-dessus.
  E19 (méthode A, décision de Jean-Luc du 29-10-2026 à 21h28) PROPRIÉTÉ du point mort des opérations : trois
     opérations sur Airbus (non taxée) ont le point mort du courtage seul (43,08 %) ; UNE opération taxée de plus
     (Bouygues, 0,4 %) l'élève, et d'exactement (49,25 − 43,08) / 4 — la moyenne, pas le pire cas ; une opération
     signalée le 31-03-2025 et achetée le 01-04-2025 paie la taxe du jour de l'ACHAT (0,4 %, 49,25 %, et non 0,3 %,
     47,71 %) ; une liste vide lève. Attendus calculés à la main dans l'épreuve.
  E21 (relecture de Cowork du commit 11ebf39, défaut 1 ; superviseur R-759, T4, R1) les VRAIES `stats` et `ligne`
     de la mesure, sur des opérations tirées d'une vraie ligne du journal, sous HIST_COURTAGE_SANS_TTF et REEL : les
     cinq branches du verdict (vert, rouge, insuffisant avec point mort, sans opération, non chiffrable) doivent être
     ATTEINTES, et chaque verdict à point mort finit par « (bareme <son barème>) », les autres n'en portent pas.
  E20 (relecture de la barre A, I1) la vraie mesure, sur un journal FABRIQUÉ dans une copie (Airbus non taxée,
     Bouygues taxée, deux stratégies, deux comptabilités, plus la vraie ligne Bureau Veritas qu'exige son calibrage),
     publie pour chaque ligne le point mort des opérations de SA stratégie et de SA comptabilité, calculé à la main :
     43.1 · vide · 46.2 · 45.1 ; la ligne sans opération a une case vide et « echantillon insuffisant » sans étiquette.

USAGE : python3 tests/EPREUVES_DU_BAREME_DES_FRAIS_Jeu_29-10-2026.py <racine du dépôt> [--saboter | nom]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Chaque épreuve travaille sur une COPIE temporaire ; le dépôt n'est jamais touché. Simulation uniquement.
"""
import ast, csv, glob, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
POS, TEN, JUG = "programmes/MODULE_POSITIONS.py", "programmes/TENIR_LES_POSITIONS.py", "programmes/MODULE_JUGEMENT.py"
MES, A9 = "programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py", "programmes/audit_ecosysteme.py"
BAN, CON = "programmes/JUGE_DES_STRATEGIES.py", "programmes/CONTRATS_DES_FICHIERS.py"

# Chaque sabotage retire UNE protection ; au moins une épreuve doit rougir (R-731).
SABOTAGES = {
    "Z0": [],
    # le forfait de 300 € revient dans le module de jugement : le garde-fou doit le voir
    "S1_forfait_remis": [(JUG, "CAPITAL = 100_000.0\n", "CAPITAL = 100_000.0\nFRAIS = 300.0\n")],
    # la taxe n'est plus appliquée aux actions : les calibrages et le juge doivent le voir
    "S2_taxe_oubliee": [(POS, "            if valeur_taxee(valeur, date):\n                taxe = taxes[0] * m\n",
                         "            if valeur_taxee(valeur, date):\n                taxe = 0.0\n")],
    # le juge achète sous le courtage seul, quel que soit le barème demandé
    "S3_juge_sans_taxe": [(BAN, 'f_tot = _far(q, pe, px, v, serie[j]["date"], d_sortie, bareme)["total"]',
                           'f_tot = _far(q, pe, px, v, serie[j]["date"], d_sortie, "HIST_COURTAGE_SANS_TTF")["total"]')],
    # le teneur de positions écrit un barème faux dans le journal
    "S4_etiquette_fausse": [(TEN, '            "bareme_reel": _bar,\n', '            "bareme_reel": "HIST_FORFAIT_300",\n')],
    # le journal porte une étiquette fausse sur sa première ligne (donnée, pas code)
    "S5_journal_mal_etiquete": [("donnees/claude_journal_trades.csv", ",HIST_FORFAIT_300,", ",HIST_COURTAGE_SANS_TTF,")],
    # un taux chiffré passé à pnl_net revient dans un programme
    "S6_taux_chiffre": [(POS, '    q = CAPITAL / prix_entree\n    brut = CAPITAL * (prix_sortie / prix_entree - 1.0)\n',
                         '    q = CAPITAL / prix_entree\n    brut = CAPITAL * (prix_sortie / prix_entree - 1.0)\n'
                         '    _inutile = dict(taux=0.0015) if False else None\n    _x = pnl_net if False else None\n'
                         '    if False:\n        pnl_net(1.0, 1.0, "A", "2026-01-02", "2026-01-02", taux=0.0015)\n')],
    # une valeur par défaut chiffrée revient sur un paramètre de frais
    "S7_defaut_chiffre": [("programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py",
                           "                                 frais_pct: float, fraction: float = 0.25) -> dict:\n",
                           "                                 frais_pct: float = 0.0025, fraction: float = 0.25) -> dict:\n")],
    # la taxe frappe aussi la vente : le barème lui-même est faussé (donnée)
    "S8_taxe_a_la_vente": [("donnees/BAREME_FRAIS.csv", "REEL,action,ttf,achat,0.004,", "REEL,action,ttf,achat_et_vente,0.004,")],
    # l'exemption du chiffre témoin de C5-EI n'est plus déclarée : son nombre redevient un frais en dur
    "S9_exemption_non_declaree": [(CON, '    ("JUGER_SUR_8_CRITERES", "TEMOIN", "frais_pct"),\n', '')],
    # l'achat revendu le jour même paie de nouveau la taxe (C10)
    "S10_exoneration_retiree": [(POS, '    exoneree = a["taxe"] if date_achat == date_vente else 0.0\n',
                                 '    exoneree = 0.0\n')],
    # la date n'est plus lue au calendrier : « 2025-13-45 » repasse (C11)
    "S11_date_non_lue": [(POS, "        datetime.date.fromisoformat(date)\n", "        pass\n")],
    # le teneur avale toute erreur du calcul des frais (C3)
    "S12_teneur_avale_tout": [(TEN, "            if _fnc is None or not isinstance(e, _fnc):\n                raise\n",
                               "            if False:\n                raise\n")],
    # le radar ne voit plus un montant faux (C4)
    "S13_radar_aveugle_au_montant": [("programmes/audit_ecosysteme.py", "            elif abs(refait - ecrit) > 1.0:\n",
                                      "            elif abs(refait - ecrit) > 1e9:\n")],
    # le radar ne voit plus une vente bloquée (C3)
    "S14_radar_aveugle_a_la_vente_bloquee": [("programmes/audit_ecosysteme.py",
                                              '                for p in (pos or []) if (p.get("frais_non_chiffrables") or "").strip()]\n',
                                              '                for p in (pos or []) if False]\n')],
    # le forfait de 300 € revient dans la stratégie C5E10, hors de tout nom de frais (le cas du relecteur T1)
    "S15_brut_moins_300": [("programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py",
                            '    pnl  = brut - _p.frais_aller_retour(',
                            '    pnl  = brut - 300.0 + 0 * _p.frais_aller_retour(')],
    # la mesure avale l'absence de liste et rend 0 (C7)
    "S17_mesure_muette": [("programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py",
                           "        return 1\n    return 0\n\nif __name__", "        return 0\n    return 0\n\nif __name__")],
    # un morceau de suppression emporte une définition encore lue (C1)
    "S18_grille_effacee": [("programmes/JUGER_SUR_8_CRITERES.py", "GRILLE = ", "_GRILLE_EFFACEE = ")],
    # --- relecteur T2 et superviseur T2 (29-10-2026) : une protection retirée, une épreuve qui rougit ---
    # les verdicts reviennent au courtage seul, contre la décision de Jean-Luc du 29-10-2026 à 19h16 — vu par E14
    "S19_verdicts_revenus_au_courtage_seul": [(POS, 'BAREME_DES_VERDICTS = "REEL"\n', 'BAREME_DES_VERDICTS = "HIST_COURTAGE_SANS_TTF"\n')],
    # le radar ne regarde plus l'année suivante (D5 « MB ») — vu par E9bis
    "S20_radar_sans_alerte_de_decembre": [(A9, "    for jour, grave in ((auj, True), (auj + _tdl(days=31), False)):\n",
                                           "    for jour, grave in ((auj, True),):\n")],
    # le radar ne contrôle plus l'étiquette des trades récents (D5 « MA ») — vu par E9
    "S21_radar_sans_controle_reel": [(A9, 'and bar != "REEL":', "and False:")],
    # la mesure avale toute erreur des frais (D5 « MC ») — vu par E11bis
    "S22_mesure_avale_tout": [(MES, "        if _fnc is None or not isinstance(e, _fnc):\n            raise\n",
                               "        if False:\n            raise\n")],
    # le forfait revient dans les opérations du juge, en aval de jouer_une_entree (D4 « MG ») — vu par E15
    "S23_forfait_dans_jouer": [(BAN, '"motif": op["motif"], "net": op["net"], "date_sortie"',
                                '"motif": op["motif"], "net": op["net"] + op["frais"] - 300.0, "date_sortie"')],
    # juger prend la date du signal pour le point mort (D5 « ME ») — vu par E15bis
    # (méthode A, 29-10-2026 : la date se lit désormais dans `point_mort_des_operations`) — vu par E19
    "S24_point_mort_du_juge_au_signal": [(JUG, 'v, d = o.get("valeur"), o.get("date_entree")',
                                          'v, d = o.get("valeur"), o.get("date_signal") or o.get("date_entree")')],
    # juger ne passe plus le barème au point mort — vu par E15bis
    "S25_juger_sans_bareme": [(BAN, "J.point_mort_des_operations(tp, sl, ops, mod_pos, bareme)",
                               "J.point_mort_des_operations(tp, sl, ops, mod_pos)")],
    # le teneur écrit un montant de convention au forfait (D4 « MH ») — vu par E10
    "S26_convention_au_forfait": [(TEN, '"pnl_net_convention_eur": "%.2f" % (q * (prix_conv - pe) - f_conv),',
                                   '"pnl_net_convention_eur": "%.2f" % (q * (prix_conv - pe) - 300.0),')],
    # les bornes du barème ne sont plus lues au calendrier (M5) — vu par E16
    "S27_bornes_non_lues": [(POS, "        if debut:\n            _date_du_calendrier(debut, f\"début d'une ligne du barème {nom!r}\")\n",
                             "        if False:\n            _date_du_calendrier(debut, f\"début d'une ligne du barème {nom!r}\")\n")],
    # le point mort publié ignore le barème des verdicts (D2) — vu par E14
    "S28_point_mort_publie_au_reel": [(MES, "                                      _mp.BAREME_DES_VERDICTS)",
                                       "                                      None)")],
    # --- relecture de Cowork et superviseur T3 (29-10-2026) ---
    # l'étiquette du barème n'est plus posée sur le verdict (défaut 1 de Cowork) — vu par E17
    "S29_verdict_sans_etiquette": [(MES, "    if pm is not None:\n        verdict = f\"{verdict} (bareme",
                                    "    if False:\n        verdict = f\"{verdict} (bareme")],
    # un forfait de 300 € posé dans la courbe de la mesure, hors de tout appel de frais (défaut 2 de Cowork) — vu par E18
    "S30_forfait_dans_la_courbe": [(MES, "pnl=nombre(o.get('pnl_net_eur'), 0.0))",
                                    "pnl=nombre(o.get('pnl_net_eur'), 0.0) - 300.0)")],
    # le juge prend la taxe du jour du signal, pas du jour de l'achat (C11) — vu par E10 (frontière des deux périodes)
    "S16_taxe_du_jour_du_signal": [(BAN, 'f_tot = _far(q, pe, px, v, serie[j]["date"], d_sortie, bareme)["total"]',
                                    'f_tot = _far(q, pe, px, v, serie[j - 1]["date"], d_sortie, bareme)["total"]')],
    # --- méthode A du point mort (décision de Jean-Luc du 29-10-2026 à 21h28) ---
    # le point mort des opérations revient au pire cas (la plus chère au lieu de la moyenne) — vu par E14, E15bis, E19
    "S31_point_mort_revenu_au_pire_cas": [(JUG, "    return sum(pms) / len(pms)\n", "    return max(pms)\n")],
    # juger rappelle l'ancien pire cas de l'univers acheté, au barème du dernier achat — vu par E15bis
    "S32_juger_revenu_au_pire_cas": [(BAN, "J.point_mort_des_operations(tp, sl, ops, mod_pos, bareme)",
                                      'J.point_mort_pire_cas(tp, sl, sorted({o["valeur"] for o in ops}), '
                                      'max(o["date_entree"] for o in ops), mod_pos, bareme)[0]')],
    # la mesure publiée rappelle l'ancien pire cas des valeurs jouées, au barème de la dernière — vu par E14
    "S33_mesure_revenue_au_pire_cas": [(MES, "    _r = _j.point_mort_des_operations(tp_pct / 100.0, abs(sl_pct) / 100.0, operations, _mp,\n",
                                        "    _r = (lambda *a: _j.point_mort_pire_cas(a[0], a[1], sorted({o['valeur'] for o in a[2]}), "
                                        "max(o['date_entree'] for o in a[2]), a[3], a[4])[0])(tp_pct / 100.0, abs(sl_pct) / 100.0, operations, _mp,\n")],

    # --- relecture de la barre A, I1 (29-10-2026) : les deux mutations du relecteur ---
    # X1 : la mesure passe TOUT le journal au point mort de chaque ligne — vu par E20
    "S34_point_mort_sur_tout_le_journal": [(MES, "operations_de(operations, carte, gref)))", "operations))")],
    # X2 : la mesure mélange les deux comptabilités — vu par E20
    "S35_point_mort_comptabilites_melangees": [(MES, "operations_de(operations, carte, gref)))",
                                                "operations_de(operations, carte)))")],
    # --- relecture de Cowork du commit 11ebf39 et superviseur R-759, T4 (29-10-2026) ---
    # M1 de Cowork : l'étiquette du barème n'est plus posée que sur « echantillon insuffisant » — vu par E21
    "S36_etiquette_seulement_branche_insuffisante": [(MES, "    if pm is not None:\n        verdict = f\"{verdict} (bareme",
                                                      "    if pm is not None and verdict == 'echantillon insuffisant':\n"
                                                      "        verdict = f\"{verdict} (bareme")],
    # M4 du superviseur : le seuil de Wilson passe de 10 à 20 opérations, vert et rouge ne sont plus atteints — vu par E21
    "S37_seuil_de_wilson_deplace": [(MES, "    if n < 10:\n        return None\n    p = gagnantes / n\n",
                                     "    if n < 20:\n        return None\n    p = gagnantes / n\n")],
    # M2 de Cowork : 300 € retirés de l'espérance publiée — vu par E18
    "S38_esperance_moins_300": [(MES, "esperance=sum(pnls)/n,", "esperance=sum(pnls)/n - 300.0,")],
    # M3 de Cowork : 300 € retirés du premier point de la courbe dans le rapport gain/secousses — vu par E18
    "S39_gain_secousses_premier_point_moins_300": [(MES, "    if not courbe or len(courbe) < 30:\n        return None\n    rend = []\n",
                                                    "    courbe = [courbe[0] - 300.0] + list(courbe[1:]) if courbe else courbe\n"
                                                    "    if not courbe or len(courbe) < 30:\n        return None\n    rend = []\n")],
}

# LES DATES FIXÉES DES ÉPREUVES DU RADAR (relecteur T2, D6) et la mise en service attendue (contrat).
HORLOGE_E9, HORLOGE_DECEMBRE = "2026-10-29T21:00:00", "2026-12-05T21:00:00"


def _env_horloge(H, dossier, heure):
    """L'environnement qui fait lire `heure` au programme lancé : le sitecustomize de tests/HORLOGE_D_EPREUVE.py."""
    hd = os.path.join(dossier, "_horloge")
    os.makedirs(hd, exist_ok=True)
    open(os.path.join(hd, "sitecustomize.py"), "w", encoding="utf-8").write(H.SITECUSTOMIZE)
    return dict(os.environ, EPREUVE_HORLOGE=heure, PYTHONPATH=hd + os.pathsep + os.environ.get("PYTHONPATH", ""))


# LE BARÈME PIÈGE de E10 : les lignes réelles de courtage au-delà de 3 000 € et de taxe sont REMPLACÉES.
PIEGE_COURTAGE, PIEGE_TAXE_AVANT, PIEGE_TAXE_APRES, PIEGE_FRONTIERE = 0.0021, 0.0057, 0.0013, "2026-05-01"
# Les fonctions qui chiffrent des frais et que E10 éprouve ; celles du module des frais lui-même ; les contrôles.
CHEMINS_EPROUVES = {"pnl_net", "jouer_une_entree", "_c5e10_sortie", "cloturer", "point_mort_en_fractions",
                    "sortie_position"}
APPELS_DE_FRAIS = {"frais_aller_retour", "frais_ordre", "pnl_net", "cout_d_un_ordre"}
# Les fonctions qui chiffrent des frais et qu'une AUTRE épreuve garde, nommée ici avec le cas qui rougirait.
EPROUVES_AILLEURS = {
    ("JOUER_LES_VERSIONS.py", "main"): "tests/EPREUVES_DE_LA_MOULINETTE_Mar_20-10-2026.py, cas « témoin étiqueté d'un "
                                       "autre barème » (la taxe payée de part et d'autre, C15) et ses sabotages C15",
}

MOTIF = re.compile(r"frais|ttf|courtage", re.I)
FONCTIONS_DE_FRAIS = {"pnl_net", "frais_ordre", "cout_d_un_ordre"}


def _litteral(v):
    """Rend le nombre écrit en dur dans une expression (constante, signe, opération entre constantes), sinon None."""
    if isinstance(v, ast.Constant) and isinstance(v.value, (int, float)) and not isinstance(v.value, bool):
        return v.value
    if isinstance(v, ast.UnaryOp) and isinstance(v.op, (ast.USub, ast.UAdd)):
        return _litteral(v.operand)
    if isinstance(v, ast.BinOp):
        a = _litteral(v.left)
        return a if a is not None else _litteral(v.right)
    return None


def _noms(cible):
    """Rend les noms qu'une affectation écrit."""
    if isinstance(cible, ast.Name):
        return [cible.id]
    if isinstance(cible, ast.Attribute):
        return [cible.attr]
    if isinstance(cible, (ast.Tuple, ast.List)):
        return [n for e in cible.elts for n in _noms(e)]
    return []


def frais_en_dur(texte, exemptions=(), fichier=""):
    """Rend la liste (ligne, nom, nombre) des frais écrits en dur dans un texte de programme (A-550, ÉTUDE 18 A4)."""
    trouves, dans_dict, conteneurs = [], [], {}
    arbre = ast.parse(texte)
    for n in ast.walk(arbre):
        if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            v = _litteral(n.value) if n.value is not None else None
            for c in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                for nom in _noms(c):
                    if MOTIF.search(nom) and v is not None:
                        trouves.append((n.lineno, nom, v))
        elif isinstance(n, ast.FunctionDef) or isinstance(n, ast.AsyncFunctionDef) or isinstance(n, ast.Lambda):
            a = n.args
            pos = a.posonlyargs + a.args
            for arg, d in list(zip(pos[len(pos) - len(a.defaults):], a.defaults)) + \
                    [(x, d) for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is not None]:
                if MOTIF.search(arg.arg) and _litteral(d) is not None:
                    trouves.append((n.lineno, arg.arg, _litteral(d)))
        elif isinstance(n, ast.Call):
            f = n.func.attr if isinstance(n.func, ast.Attribute) else (n.func.id if isinstance(n.func, ast.Name) else "")
            for k in n.keywords:
                if k.arg and (MOTIF.search(k.arg) or (k.arg == "taux" and f in FONCTIONS_DE_FRAIS)) \
                        and _litteral(k.value) is not None:
                    trouves.append((n.lineno, k.arg, _litteral(k.value)))
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict):
            conteneurs[id(n.value)] = ",".join(x for c in n.targets for x in _noms(c))
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str) and MOTIF.search(k.value) \
                        and _litteral(v) is not None:
                    dans_dict.append((n, k.value, _litteral(v)))
    # Un nombre n'est EXEMPTÉ que par son EMPLACEMENT déclaré au contrat — (fichier, dictionnaire, clé) —, jamais par
    # sa valeur (superviseur R-759, C5 ④, 29-10-2026) : avant, tout nombre égal au seuil C8 passait, n'importe où.
    for n, cle, v in dans_dict:
        if (fichier, conteneurs.get(id(n), ""), cle) not in exemptions:
            trouves.append((n.lineno, cle, v))
    return trouves


def copie(sab):
    d = tempfile.mkdtemp(prefix="bareme_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8", newline="").read()
        assert t.count(a) == 1, (sab, f, a[:60], t.count(a))
        open(p, "w", encoding="utf-8", newline="").write(t.replace(a, b))
    return d


def run(d, *args):
    r = subprocess.run([sys.executable, "-B", *args], cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def epreuves(sab):
    res = []

    def dire(nom, ok, detail=""):
        res.append((nom, bool(ok), detail))

    d = copie(sab)
    # E1 le garde-fou, sur tous les programmes de la copie (une PROPRIÉTÉ : aucun nom de fichier n'est épelé)
    c, o = run(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import CONTRATS_DES_FICHIERS as c; "
                        "print(repr(sorted(c.EXEMPTIONS_DU_GARDE_FOU_DES_FRAIS)))")
    try:
        exemptions = set(ast.literal_eval(o.strip().splitlines()[-1]))
    except Exception:
        exemptions = None
    if exemptions is None:
        dire("E1 garde-fou : exemptions déclarées lisibles", False, o.strip()[-80:])
    else:
        fautes = []
        # LE CHAMP : tout programme Python du dépôt hors archives, études gelées et épreuves (C5 ③) — `programmes/`
        # et ses sous-dossiers, `etudes/outils/`, la racine. Aucun nom de fichier n'est épelé.
        champ = sorted(set(glob.glob(os.path.join(d, "programmes", "**", "*.py"), recursive=True)
                           + glob.glob(os.path.join(d, "etudes", "outils", "**", "*.py"), recursive=True)
                           + glob.glob(os.path.join(d, "*.py"))))
        for f in champ:
            try:
                for ligne, nom, v in frais_en_dur(open(f, encoding="utf-8").read(), exemptions,
                                              os.path.splitext(os.path.basename(f))[0]):
                    fautes.append(f"{os.path.relpath(f, d)}:{ligne} {nom}={v}")
            except SyntaxError as e:
                fautes.append(f"{os.path.relpath(f, d)} illisible ({e})")
        dire(f"E1 garde-fou : aucun frais écrit en dur dans {len(champ)} programmes", champ and not fautes,
             " · ".join(fautes[:4]))
    # E1bis le motif est calibré sur les cinq copies relevées le 29-10-2026, et sur un cas qui ne doit pas sortir
    cas = ("FRAIS = 300.0\nclass F:\n    FRAIS_TAUX = 0.0015\nFRAIS_TAUX = 0.0015\n"
           "x = pnl_net(27.28, 28.3712, taux=0.0015)\n"
           "def kelly(wr, tp, sl, frais_pct: float = 0.0025, fraction: float = 0.25):\n    pass\n"
           "y = attendre(timeout=300)\n")
    vus = sorted(nom for _l, nom, _v in frais_en_dur(cas))
    dire("E1bis motif calibré : 5 cas connus vus, timeout=300 non retenu",
         vus == sorted(["FRAIS", "FRAIS_TAUX", "FRAIS_TAUX", "taux", "frais_pct"]), str(vus))
    # E2 calibrage du module des positions
    c, o = run(d, POS)
    dire("E2 calibrage du module des positions (taxe, courtage, trois montants du journal)",
         c == 0 and "CALIBRAGE : OK" in o and o.count("✅") >= 13, f"code {c} · {o.strip()[-90:]}")
    # E3 calibrage du teneur de positions, Unibail sous le barème réel
    c, o = run(d, TEN, d, "--calibrage")
    dire("E3 calibrage du teneur : Unibail −2 796,25 € d'époque et −3 196,25 € au barème réel",
         c == 0 and re.search(r"sous le bareme reel : -3 196,25 EUR \(taxe comprise\)\s+OK", o)
         and re.search(r"sous le bareme reel : le journal nomme REEL\s+OK", o)
         and re.search(r"le journal nomme le bareme employe\s+OK", o), f"code {c}")
    # E4 calibrage du module de jugement, point mort taxé
    c, o = run(d, JUG)
    dire("E4 calibrage du jugement : point mort 49,25 % sur une valeur taxée",
         c == 0 and re.search(r"49,25 % sur une valeur taxee \(bareme reel\)\s+OK", o), f"code {c}")
    # E5 les deux fichiers du barème suivent leur contrat
    c, o = run(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import CONTRATS_DES_FICHIERS as c; "
                        "e = [x for x in c.confronter_tous('.') if 'BAREME_FRAIS' in x or 'VALEURS_TTF' in x]; "
                        "print('ECARTS', len(e), e)")
    dire("E5 BAREME_FRAIS.csv et VALEURS_TTF.csv suivent leur contrat", "ECARTS 0 []" in o, o.strip()[-90:])
    # E6 vraies lignes : chaque montant du journal se refait sous le barème que sa ligne nomme
    code = ("import csv, sys; sys.path.insert(0, 'programmes'); import MODULE_POSITIONS as p\n"
            "n = f = 0\n"
            "for l in csv.DictReader(open('donnees/claude_journal_trades.csv', encoding='utf-8', newline='')):\n"
            "    for cp, cn, cb in (('prix_sortie', 'pnl_net_eur', 'bareme_reel'),"
            " ('prix_sortie_convention', 'pnl_net_convention_eur', 'bareme_convention')):\n"
            "        r = round(p.pnl_net(float(l['prix_entree']), float(l[cp]), l['valeur'], l['date_entree'],"
            " l['date_sortie'], l[cb]), 2)\n"
            "        n += 1; f += abs(r - float(l[cn])) >= 0.005\n"
            "print('MONTANTS', n, 'FAUX', f)\n")
    c, o = run(d, "-c", code)
    m = re.search(r"MONTANTS (\d+) FAUX (\d+)", o)
    dire("E6 vraies lignes : chaque montant du journal se refait sous son barème",
         c == 0 and m and int(m.group(1)) > 0 and m.group(2) == "0", o.strip()[-90:])
    # E7 le juge des stratégies paie la taxe (Bouygues, valeur taxée en 2026)
    code = ("import sys; sys.path.insert(0, 'programmes'); import MODULE_POSITIONS as p, JUGE_DES_STRATEGIES as b\n"
            "s = [dict(date='2026-04-29', open=100.0, high=100.5, low=99.5, close=100.0),\n"
            "     dict(date='2026-04-30', open=100.0, high=100.5, low=99.5, close=100.0),\n"
            "     dict(date='2026-05-04', open=101.0, high=105.0, low=100.5, close=104.5)]\n"
            "r = b.jouer_une_entree('BOUYGUES', s, 1, 0.04, 0.025, 20, p, None, 'REEL')\n"
            "h = b.jouer_une_entree('BOUYGUES', s, 1, 0.04, 0.025, 20, p, None, 'HIST_COURTAGE_SANS_TTF')\n"
            "print('NET %.2f %.2f' % (r['net'], h['net']))\n")
    c, o = run(d, "-c", code)
    dire("E7 juge : +3 294,00 € taxe comprise, +3 694,00 € au courtage seul",
         c == 0 and "NET 3294.00 3694.00" in o, o.strip()[-90:])
    # E8 le teneur : frais non chiffrables -> position laissée ouverte et dite ; autre erreur -> lève
    code = ("import sys; sys.path.insert(0, 'programmes'); import MODULE_POSITIONS as p, TENIR_LES_POSITIONS as T\n"
            "def pos(v, d):\n"
            "    return dict(strategie='S', valeur=v, date_signal=d, date_entree=d, prix_entree='100.0', tp='104.0',\n"
            "                sl='97.5', horizon_fin='2099-01-01', statut='OUVERTE', comptabilite='un_jeton',\n"
            "                regles_pre_trade='', explication='', frais_non_chiffrables='')\n"
            "c = {'AIRBUS': [dict(date='2023-06-01', open=100.0, high=105.0, low=99.0, close=104.5)]}\n"
            "tr, rest, inc = T.cloturer([pos('AIRBUS', '2023-06-01')], c, p)\n"
            "print('BLOQUEE', len(tr), len(rest), rest[0]['statut'], '2023' in rest[0]['frais_non_chiffrables'],\n"
            "      any('VENTE BLOQUEE' in x for x in inc))\n"
            "class Faux:\n"
            "    tester_seance = staticmethod(p.tester_seance); CAPITAL = p.CAPITAL; BAREME_PAR_DEFAUT = 'REEL'\n"
            "    FraisNonChiffrables = p.FraisNonChiffrables\n"
            "    @staticmethod\n"
            "    def frais_aller_retour(*a, **k):\n"
            "        raise KeyError('faute de programmation')\n"
            "try:\n"
            "    T.cloturer([pos('AIRBUS', '2023-06-01')], c, Faux)\n"
            "    print('AUTRE ERREUR AVALEE')\n"
            "except KeyError:\n"
            "    print('AUTRE ERREUR LEVEE')\n")
    c, o = run(d, "-c", code)
    dire("E8 teneur : vente bloquée dite dans sa case, toute autre erreur lève",
         c == 0 and "BLOQUEE 0 1 OUVERTE True True" in o and "AUTRE ERREUR LEVEE" in o, o.strip()[-120:])
    # E9 le radar, maillon 10bis, sur quatre fautes posées dans une autre copie, À UNE DATE FIXÉE (relecteur T2, D6 :
    # l'épreuve ne dépend plus du jour où on la lance) par l'horloge d'épreuve du dépôt (tests/HORLOGE_D_EPREUVE.py)
    sys.path.insert(0, os.path.join(DEPOT, "tests"))
    import HORLOGE_D_EPREUVE as H
    d9 = tempfile.mkdtemp(prefix="bareme_radar_")
    shutil.copytree(d, d9, dirs_exist_ok=True)
    fj = os.path.join(d9, "donnees", "claude_journal_trades.csv")
    lignes = list(csv.DictReader(open(fj, encoding="utf-8", newline="")))
    champs = list(lignes[0].keys())
    lignes[0]["pnl_net_eur"] = "%.2f" % (float(lignes[0]["pnl_net_eur"]) + 2.0)
    # quatrième faute (T2, D5 « MA ») : un trade vendu le jour de la mise en service, montant JUSTE sous son étiquette
    # historique — seule l'étiquette est fausse. Une ligne au courtage seul : son montant ne dépend pas de la date.
    hist = [l for l in lignes if l.get("bareme_reel") == "HIST_COURTAGE_SANS_TTF"]
    if hist:
        recent = dict(hist[0])
        _c, _o = run(d9, "-c", "import sys; sys.path.insert(0, 'programmes'); import CONTRATS_DES_FICHIERS as c; "
                               "print(c.MISE_EN_SERVICE_DU_BAREME_REEL)")
        recent["date_sortie"] = _o.strip().splitlines()[-1]   # lue au contrat, jamais recopiée (R-708)
        lignes.append(recent)
    with open(fj, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs); w.writeheader(); w.writerows(lignes)
    fp = os.path.join(d9, "donnees", "claude_positions_ouvertes.csv")
    pl = list(csv.DictReader(open(fp, encoding="utf-8", newline="")))
    ch = list(pl[0].keys()) if pl else []
    if "frais_non_chiffrables" not in ch:
        ch.append("frais_non_chiffrables")
    for x in pl:
        x.setdefault("frais_non_chiffrables", "")
    if pl:
        pl[0]["frais_non_chiffrables"] = "2027-01-04 TP : liste 2027 absente"
    with open(fp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ch); w.writeheader(); w.writerows(pl)
    ft = os.path.join(d9, "donnees", "VALEURS_TTF.csv")
    tt = open(ft, encoding="utf-8", newline="").read().splitlines(True)
    an = HORLOGE_E9[:4]
    tt = [l for l in tt if not l.startswith(an + ",VIE,")]
    open(ft, "w", encoding="utf-8", newline="").write("".join(tt))
    p9 = subprocess.run([sys.executable, "-B", "programmes/audit_ecosysteme.py", d9], cwd=d9, capture_output=True,
                        text=True, env=_env_horloge(H, d9, HORLOGE_E9))
    o = p9.stdout + p9.stderr
    # le même radar le 5 décembre, liste de l'année suivante absente : ⚠ (C3 ① du superviseur T1 ; T2, D5 « MB »)
    p9b = subprocess.run([sys.executable, "-B", "programmes/audit_ecosysteme.py", d9], cwd=d9, capture_output=True,
                         text=True, env=_env_horloge(H, d9, HORLOGE_DECEMBRE))
    ob = p9b.stdout + p9b.stderr
    an_suivant = str(int(HORLOGE_DECEMBRE[:4]) + 1)
    shutil.rmtree(d9)
    dire("E9 radar 10bis (horloge fixée) : montant décalé, vente bloquée, valeur hors liste, étiquette historique "
         "récente — quatre ❌",
         bool(pl) and bool(hist) and re.search(r"❌ \[10bis-Frais\] MONTANT QUI NE RETOMBE PAS", o)
         and re.search(r"❌ \[10bis-Frais\] VENTE BLOQUÉE", o)
         and re.search(r"❌ \[10bis-Frais\] LISTE DES VALEURS TAXÉES " + an + r" INCOMPLÈTE.*VIE", o)
         and re.search(r"❌ \[10bis-Frais\] BARÈME HISTORIQUE SUR UN TRADE RÉCENT", o),
         " / ".join(l for l in o.splitlines() if "10bis" in l)[:300] or o.strip()[-120:])
    dire("E9bis radar 10bis le " + HORLOGE_DECEMBRE[:10] + " : liste " + an_suivant + " absente — ⚠",
         re.search(r"⚠️ \[10bis-Frais\] LISTE DES VALEURS TAXÉES " + an_suivant + r" INCOMPLÈTE", ob),
         " / ".join(l for l in ob.splitlines() if "10bis" in l)[:300] or ob.strip()[-120:])
    # E10 la propriété : chaque chemin qui chiffre un trade suit le barème piège
    fb = os.path.join(d, "donnees", "BAREME_FRAIS.csv")
    bl = open(fb, encoding="utf-8", newline="").read().splitlines(True)
    nouv, vus = [], 0
    for l in bl:
        if l.startswith("REEL,action_et_etf,courtage,achat_et_vente,0.0015,"):
            nouv.append(l.replace(",0.0015,", ",%s," % PIEGE_COURTAGE, 1)); vus += 1
        elif l.startswith("REEL,action,ttf,achat,0.003,"):
            nouv.append("REEL,action,ttf,achat,%s,,,,,2026-04-30,piege,2026-10-29,piege\r\n" % PIEGE_TAXE_AVANT); vus += 1
        elif l.startswith("REEL,action,ttf,achat,0.004,"):
            nouv.append("REEL,action,ttf,achat,%s,,,,%s,,piege,2026-10-29,piege\r\n" % (PIEGE_TAXE_APRES, PIEGE_FRONTIERE)); vus += 1
        else:
            nouv.append(l)
    open(fb, "w", encoding="utf-8", newline="").write("".join(nouv))
    tt = open(ft.replace(d9, d), encoding="utf-8", newline="").read()
    n_flip = tt.count("2026,AIR,AIRBUS,NON,") + tt.count("2026,EN,BOUYGUES,OUI,")
    tt = tt.replace("2026,AIR,AIRBUS,NON,", "2026,AIR,AIRBUS,OUI,").replace("2026,EN,BOUYGUES,OUI,", "2026,EN,BOUYGUES,NON,")
    open(ft.replace(d9, d), "w", encoding="utf-8", newline="").write(tt)
    # LES ATTENDUS, À LA MAIN : capital 100 000 €, achat à 100 €, vente à 104 € (objectif de 4 %).
    K, cg = 100000.0, PIEGE_COURTAGE
    att = {
        "pnl AIRBUS lendemain": 4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg,
        "pnl AIRBUS jour même": 4000 - K * cg - 104000 * cg,
        "pnl BOUYGUES lendemain": 4000 - K * cg - 104000 * cg,
        "pnl AIRBUS avant la frontière": 4000 - K * cg - K * PIEGE_TAXE_AVANT - 104000 * cg,
        "juge AIRBUS acheté le 04-05": 4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg,
        "c5e10 AIRBUS acheté le 04-05": 4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg,
        "teneur AIRBUS acheté le 04-05": 4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg,
        "sortie_position AIRBUS achetée le 04-05": 4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg,
        "teneur AIRBUS, montant de convention": 4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg,
        "point mort AIRBUS le 04-05": 100.0 * (2500 + K * cg + K * PIEGE_TAXE_APRES + 97500 * cg)
                                      / ((4000 - K * cg - K * PIEGE_TAXE_APRES - 104000 * cg)
                                         + (2500 + K * cg + K * PIEGE_TAXE_APRES + 97500 * cg)),
    }
    code = ("import sys, glob, importlib.util; sys.path.insert(0, 'programmes')\n"
            "import MODULE_POSITIONS as p, JUGE_DES_STRATEGIES as b, TENIR_LES_POSITIONS as T, MODULE_JUGEMENT as J\n"
            "sp = importlib.util.spec_from_file_location('c5', glob.glob('programmes/MODULE_C5_ETENDU_10_*.py')[0])\n"
            "C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)\n"
            "s = [dict(date='2026-04-30', open=100.0, high=100.5, low=99.5, close=100.0, volume=1.0),\n"
            "     dict(date='2026-05-04', open=100.0, high=101.0, low=99.0, close=100.5, volume=1.0),\n"
            "     dict(date='2026-05-05', open=100.5, high=105.0, low=100.0, close=104.5, volume=1.0)]\n"
            "o = {}\n"
            "o['pnl AIRBUS lendemain'] = p.pnl_net(100.0, 104.0, 'AIRBUS', '2026-05-04', '2026-05-05')\n"
            "o['pnl AIRBUS jour même'] = p.pnl_net(100.0, 104.0, 'AIRBUS', '2026-05-04', '2026-05-04')\n"
            "o['pnl BOUYGUES lendemain'] = p.pnl_net(100.0, 104.0, 'BOUYGUES', '2026-05-04', '2026-05-05')\n"
            "o['pnl AIRBUS avant la frontière'] = p.pnl_net(100.0, 104.0, 'AIRBUS', '2026-04-29', '2026-04-30')\n"
            "o['juge AIRBUS acheté le 04-05'] = b.jouer_une_entree('AIRBUS', s, 1, 0.04, 0.025, 20, p, None, 'REEL')['net']\n"
            "o['c5e10 AIRBUS acheté le 04-05'] = C._c5e10_sortie(s, 0, 'AIRBUS')['pnl']\n"
            "pos = dict(strategie='S', valeur='AIRBUS', date_signal='2026-04-30', date_entree='2026-05-04',\n"
            "           prix_entree='100.0', tp='104.0', sl='97.5', horizon_fin='2099-01-01', statut='OUVERTE',\n"
            "           comptabilite='un_jeton', regles_pre_trade='', explication='', frais_non_chiffrables='')\n"
            "tr, _r, _i = T.cloturer([pos], {'AIRBUS': s}, p)\n"
            "o['teneur AIRBUS acheté le 04-05'] = float(tr[0]['pnl_net_eur']) if tr else None\n"
            "o['teneur AIRBUS, montant de convention'] = float(tr[0]['pnl_net_convention_eur']) if tr else None\n"
            "o['sortie_position AIRBUS achetée le 04-05'] = p.sortie_position(s[2:], 100.0, 'AIRBUS', '2026-05-04')['pnl_net_convention_eur']\n"
            "o['point mort AIRBUS le 04-05'] = J.point_mort_en_fractions(0.04, 0.025, p, 'AIRBUS', '2026-05-04')\n"
            "print('OBTENU', repr(o))\n")
    c, o = run(d, "-c", code)
    m = re.search(r"OBTENU (\{.*\})", o)
    obt = ast.literal_eval(m.group(1)) if m else {}
    faux = [f"{k} : {obt.get(k)!r} au lieu de {v:.4f}" for k, v in att.items()
            if not isinstance(obt.get(k), (int, float)) or abs(obt[k] - v) > 0.01]
    dire("E10 propriété : chaque chemin suit le barème piège (deux périodes, liste retournée)",
         vus == 3 and n_flip == 2 and m and not faux, f"lignes piégées {vus}/3, liste {n_flip}/2 · "
         + (" · ".join(faux[:3]) if m else o.strip()[-160:]))
    # E10bis l'épreuve cherche elle-même les fonctions qui chiffrent des frais
    trouvees = set()
    for f in sorted(glob.glob(os.path.join(d, "programmes", "*.py"))):
        try:
            arbre = ast.parse(open(f, encoding="utf-8").read())
        except SyntaxError:
            continue
        for fn in ast.walk(arbre):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or fn.name in APPELS_DE_FRAIS:
                continue
            appelle = False
            for n in ast.walk(fn):
                if isinstance(n, ast.Call):
                    nom = n.func.attr if isinstance(n.func, ast.Attribute) else (
                        n.func.id if isinstance(n.func, ast.Name) else "")
                    appelle = appelle or nom in APPELS_DE_FRAIS
                    if nom == "getattr" and any(isinstance(x, ast.Constant) and x.value in APPELS_DE_FRAIS
                                                for x in n.args):
                        appelle = True   # getattr(module, "frais_aller_retour")
            if appelle:
                trouvees.add((os.path.basename(f), fn.name))
    controles = {x for x in trouvees if re.match(r"_?calibr|_maillon|leve$|epreuve", x[1])}
    orphelines = sorted(f"{a}:{n}" for a, n in trouvees - controles
                        if n not in CHEMINS_EPROUVES and (a, n) not in EPROUVES_AILLEURS)
    dire("E10bis toute fonction qui chiffre des frais est éprouvée par E10 (ou est un contrôle)",
         not orphelines and not (CHEMINS_EPROUVES - APPELS_DE_FRAIS - {n for _a, n in trouvees}),
         " · ".join(orphelines[:5]) + " | éprouvés mais introuvables (motif à recaler) : "
         + ", ".join(sorted(CHEMINS_EPROUVES - APPELS_DE_FRAIS - {n for _a, n in trouvees})))
    # E11 (C7) la mesure : une valeur d'univers absente de la liste de l'année -> lignes écrites, raison dite, code 1
    d11 = tempfile.mkdtemp(prefix="bareme_mesure_")
    shutil.copytree(d, d11, dirs_exist_ok=True)
    shutil.copy(os.path.join(DEPOT, "donnees", "VALEURS_TTF.csv"), os.path.join(d11, "donnees", "VALEURS_TTF.csv"))
    shutil.copy(os.path.join(DEPOT, "donnees", "BAREME_FRAIS.csv"), os.path.join(d11, "donnees", "BAREME_FRAIS.csv"))
    # la mesure ne lit la liste des valeurs taxées que si ses verdicts se chiffrent aux vrais frais : E11 joue le cas
    # d'APRÈS la décision de Jean-Luc (`BAREME_DES_VERDICTS = "REEL"`), seul où l'absence de liste la touche
    fm11 = os.path.join(d11, "programmes", "MODULE_POSITIONS.py")
    tm11 = open(fm11, encoding="utf-8").read()
    # (depuis la décision du 29-10-2026 à 19h16, c'est déjà la valeur du dépôt ; on la POSE quand même, pour que E11
    # joue ce cas sous tout sabotage du barème des verdicts — la ligne doit exister une fois)
    tm11, n_bv = re.subn(r'^BAREME_DES_VERDICTS = "[^"]*"$', 'BAREME_DES_VERDICTS = "REEL"', tm11, flags=re.M)
    open(fm11, "w", encoding="utf-8").write(tm11)
    ft11 = os.path.join(d11, "donnees", "VALEURS_TTF.csv")
    # MÉTHODE A (décision de Jean-Luc du 29-10-2026 à 21h28) : le point mort lit la liste de l'année de CHAQUE ACHAT, et
    # seulement les valeurs JOUÉES. La valeur retirée et son ANNÉE se lisent donc au journal de la copie, jamais en dur
    # (relecture de la barre A, I2 : retirée à l'année de la dernière séance, Unibail aurait fait rougir E11 à tort dès
    # la première séance de 2027 — son achat est de 2026). On prend la valeur jouée sur le plus de lignes du journal
    # (au 29-10-2026 : Unibail, URW, 4 lignes, achat du 21-08-2026), et on la retire de la liste de chaque année où
    # elle a été achetée. Le rapprochement de la graphie du journal (« UNIBAIL_RODAMCO ») et de la liste
    # (« UNIBAIL-RODAMCO-WESTFIELD ») passe par la clé d'identité du juge ; les lignes touchées se déduisent des noms
    # que le contrat donne à chaque stratégie vivante (`CONTRATS_DES_FICHIERS.noms_d_une_strategie`).
    c_, o_ = run(d11, "-c", "import sys, csv, json, collections; sys.path.insert(0, 'programmes')\n"
                            "import JUGE_DES_STRATEGIES as B, CONTRATS_DES_FICHIERS as C\n"
                            "tt = list(csv.DictReader(l for l in open('donnees/VALEURS_TTF.csv', encoding='utf-8') if not l.startswith('#')))\n"
                            "j = list(csv.DictReader(open('donnees/claude_journal_trades.csv', encoding='utf-8')))\n"
                            "n = collections.Counter(o['valeur'] for o in j)\n"
                            "v = sorted(n, key=lambda x: (-n[x], x))[0]\n"
                            "mn = sorted({x['mnemonique'] for x in tt if x['mnemonique'].upper() == v.upper() or B.cle_valeur(x['nom_usuel']) == B.cle_valeur(v)})\n"
                            "ans = sorted({o['date_entree'][:4] for o in j if o['valeur'] == v})\n"
                            "viv = [r for r in csv.DictReader(open('donnees/cac40_strategies.csv', encoding='utf-8-sig')) if (r.get('etat_vie') or '').strip().upper() in ('QA', 'PRODUCTION')]\n"
                            "tou = sorted({(r['id'], o['comptabilite'].replace('_', ' ')) for r in viv for o in j if o['valeur'] == v and (o.get('strategie') or '').strip() in C.noms_d_une_strategie(r)})\n"
                            "print('CHOIX ' + json.dumps([v, mn, ans, tou]))\n")
    m11 = re.search(r"CHOIX (.*)", o_)
    v11, mn11, ans11, tou11 = json.loads(m11.group(1)) if c_ == 0 and m11 else ("?", [], [], [])
    tt = open(ft11, encoding="utf-8", newline="").read().splitlines(True)
    retirer = tuple(f"{a},{m}," for a in ans11 for m in mn11)
    n_retirees = sum(1 for l in tt if retirer and l.startswith(retirer))
    open(ft11, "w", encoding="utf-8", newline="").write("".join(l for l in tt if not (retirer and l.startswith(retirer))))
    sortie11 = os.path.join(d11, "_sortie_mesure")
    os.makedirs(os.path.join(sortie11, "donnees"))
    mes = sorted(glob.glob(os.path.join(d11, "programmes", "MESURER_LA_PERFORMANCE_*.py")))[0]
    c, o = run(d11, mes, d11, sortie11)
    ecrites = list(csv.DictReader(open(os.path.join(sortie11, "donnees", "historique_mesures.csv"), encoding="utf-8")))\
        if os.path.isfile(os.path.join(sortie11, "donnees", "historique_mesures.csv")) else []
    non_chiffrables = {(l["strategie"], l["comptabilite"]) for l in ecrites if l["verdict_c7"].startswith("point mort non chiffrable")}
    nommees = {(l["strategie"], l["comptabilite"]) for l in ecrites
               if l["verdict_c7"].startswith("point mort non chiffrable") and repr(v11) in l["verdict_c7"]}
    attendues = {tuple(x) for x in tou11}
    shutil.rmtree(d11)
    # chaque ligne qui a joué la valeur retirée dit « non chiffrable » en la nommant ; aucune autre ne le dit
    dire("E11 mesure : point mort non chiffrable dit dans verdict_c7 de chaque ligne qui a joué la valeur retirée, "
         "à l'année de son achat ; lignes écrites, code 1",
         n_bv == 1 and len(mn11) == 1 and ans11 and n_retirees == len(ans11) and attendues and c == 1 and ecrites
         and non_chiffrables == attendues == nommees and "SANS POINT MORT" in o,
         f"{v11} {mn11} retirée de {ans11} ({n_retirees} ligne(s)) · code {c} · {len(ecrites)} ligne(s) · non chiffrables "
         f"{sorted(non_chiffrables)} · attendues {sorted(attendues)} · {o.strip()[-100:]}")
    # E11bis (T2, D5 « MC ») la mesure n'attrape QUE l'exception des frais non chiffrables : un barème corrompu (une
    # ligne de taxe à la nature inconnue) doit la faire LEVER, sans écrire de ligne « point mort non chiffrable »
    d11b = copie(sab)          # une copie NEUVE, sabotage compris (la copie `d` porte déjà le barème piège de E10)
    fm = os.path.join(d11b, "programmes", "MODULE_POSITIONS.py")
    tm = open(fm, encoding="utf-8").read()
    tm, n_bv2 = re.subn(r'^BAREME_DES_VERDICTS = "[^"]*"$', 'BAREME_DES_VERDICTS = "REEL"', tm, flags=re.M)
    open(fm, "w", encoding="utf-8").write(tm)
    fb2 = os.path.join(d11b, "donnees", "BAREME_FRAIS.csv")
    tb = open(fb2, encoding="utf-8", newline="").read()
    n_nat = tb.count("REEL,action,ttf,achat,0.004,")
    open(fb2, "w", encoding="utf-8", newline="").write(tb.replace("REEL,action,ttf,achat,0.004,",
                                                                  "REEL,action,inconnue,achat,0.004,"))
    s11b = os.path.join(d11b, "_sortie_mesure")
    os.makedirs(os.path.join(s11b, "donnees"))
    mes_b = sorted(glob.glob(os.path.join(d11b, "programmes", "MESURER_LA_PERFORMANCE_*.py")))[0]
    c, o = run(d11b, mes_b, d11b, s11b)
    ecrit_b = os.path.isfile(os.path.join(s11b, "donnees", "historique_mesures.csv"))
    shutil.rmtree(d11b)
    dire("E11bis mesure : une autre erreur des frais LÈVE (ValueError), rien n'est écrit comme « non chiffrable »",
         n_bv2 == 1 and n_nat == 1 and c != 0 and "ValueError" in o and "nature inconnue" in o and not ecrit_b,
         f"code {c} · écrit {ecrit_b} · {o.strip()[-140:]}")
    # E14 (T2, D2) LE BARÈME DES VERDICTS : sans barème donné, le juge et le point mort publié se chiffrent sous
    # `MODULE_POSITIONS.BAREME_DES_VERDICTS`, aux vrais frais depuis la décision de Jean-Luc du 29-10-2026 à 19h16 ; le
    # teneur de positions chiffre aussi les trades vécus au barème réel (E3). Attendus à la main : Bouygues (taxée en
    # 2026) achetée à 100 € le 30-04-2026, revendue à 104 € le 04-05 : 4 000 − 150 − 400 (taxe à l'achat) − 156 =
    # +3 294,00 €.
    # POINT MORT PUBLIÉ, MÉTHODE A (décision de Jean-Luc du 29-10-2026 à 21h28) : la moyenne des points morts des
    # opérations reçues, chacune à sa valeur et à sa date d'achat. +4 % / −2,5 %, 100 000 € ; courtage 150 € à l'achat,
    # 156 € à la vente au gain, 146,25 € à la vente au stop ; gain + perte = 6 500 − 9,75 = 6 490,25 € dans les trois cas :
    #   Bouygues 27-07-2026, taxe 0,4 % = 400 € : 100 × (2 500 + 150 + 400 + 146,25) / 6 490,25 = 3 196,25 / 6 490,25 = 49,2469 %
    #   Airbus   27-07-2026, non taxée          : 100 × (2 500 + 150 + 146,25) / 6 490,25       = 2 796,25 / 6 490,25 = 43,0839 %
    #   Bouygues 03-03-2025, taxe 0,3 % = 300 € : 100 × (2 500 + 150 + 300 + 146,25) / 6 490,25 = 3 096,25 / 6 490,25 = 47,7062 %
    #   moyenne : (3 196,25 + 2 796,25 + 3 096,25) / 3 / 6 490,25 × 100 = 46,68 % — le pire cas rendrait 49,25 %.
    # Et sans aucune opération : aucun point mort (None).
    code = ("import sys, glob, importlib.util; sys.path.insert(0, 'programmes')\n"
            "import MODULE_POSITIONS as p, JUGE_DES_STRATEGIES as b\n"
            "s = [dict(date='2026-04-29', open=100.0, high=100.5, low=99.5, close=100.0),\n"
            "     dict(date='2026-04-30', open=100.0, high=100.5, low=99.5, close=100.0),\n"
            "     dict(date='2026-05-04', open=101.0, high=105.0, low=100.5, close=104.5)]\n"
            "r = b.jouer_une_entree('BOUYGUES', s, 1, 0.04, 0.025, 20, p, None)\n"
            "f = glob.glob('programmes/MESURER_LA_PERFORMANCE_*.py')[0]\n"
            "sp = importlib.util.spec_from_file_location('m', f); m = importlib.util.module_from_spec(sp)\n"
            "sp.loader.exec_module(m)\n"
            "ops = [dict(valeur='BOUYGUES', date_entree='2026-07-27'), dict(valeur='AIRBUS', date_entree='2026-07-27'),\n"
            "       dict(valeur='BOUYGUES', date_entree='2025-03-03')]\n"
            "print('DEFAUT %s NET %.2f PM %.2f VIDE %s' % (p.BAREME_DES_VERDICTS, r['net'],\n"
            "      m.point_mort_en_pourcents(4.0, -2.5, ops), m.point_mort_en_pourcents(4.0, -2.5, [])))\n")
    dp = copie(sab)            # une copie NEUVE, sabotage compris
    c, o = run(dp, "-c", code)
    shutil.rmtree(dp)
    att_pm = 100 * (3196.25 + 2796.25 + 3096.25) / 3 / ((4000 - 150 - 156) + (2500 + 150 + 146.25))
    dire("E14 barème des verdicts : juge et point mort publié aux vrais frais (+3 294,00 €, moyenne %.2f %%, vide sans "
         "point mort)" % att_pm,
         c == 0 and ("DEFAUT REEL NET 3294.00 PM %.2f VIDE None" % att_pm) in o, o.strip()[-140:])
    # E15 (T2, D4 et D5 « ME ») LE VRAI `jouer` ET LE VRAI `juger`, sur une vraie fiche (C5E10-QA-V1) et le maître, dans
    # la copie au barème PIÈGE de E10 : chaque opération porte un gain égal à la variation moins SES frais, et ses frais
    # valent la formule à la main (courtage piège aux deux ordres, taxe piège de la période de l'ACHAT si la valeur est
    # taxée dans la liste piège de son année et que la vente n'a pas lieu le même jour) ; puis `juger` demande le
    # point mort au jour du DERNIER ACHAT joué et sous le barème donné.
    code = ("import sys, csv, types, importlib.util as iu, io, contextlib; sys.path.insert(0, 'programmes')\n"
            "import MODULE_JUGEMENT as J, MODULE_POSITIONS as P, JUGE_DES_STRATEGIES as B\n"
            "R = '.'\n"
            "mnemo = B.table_mnemoniques(B.trouver(R, 'REFERENTIEL_VALEURS'))\n"
            "sig = B.charger_module(B.trouver(R, 'MODULE_C5_ETENDU_10'), 'sig')\n"
            "f = next(x for x in csv.DictReader(open('donnees/cac40_strategies.csv', encoding='utf-8-sig')) if x['id'] == 'C5E10-QA-V1')\n"
            "ok0, _m, bornes = B.porte_0(f); f.setdefault('_fonction_signal', 'signaux_c5etendu10')\n"
            "cr, lr = B.lire_par_le_lecteur(R, 'donnees/cours_maitre.csv', mnemo)\n"
            "ops, _ = B.jouer(f, cr, mnemo, sig, P, periode=bornes, lecture=lr, bareme='REEL')\n"
            "inv = {}\n"
            "for k, v in mnemo.items(): inv.setdefault(v, k)\n"
            "liste = {(l['annee'], l['mnemonique']): l['assujettie'] for l in csv.DictReader(io.StringIO(\n"
            "    ''.join(open('donnees/VALEURS_TTF.csv', encoding='utf-8').read().splitlines(True)[1:])))}\n"
            "faux = []\n"
            "for o in ops:\n"
            "    q = 100000.0 / o['pe']\n"
            "    taxe = 0.0\n"
            "    if o['date_entree'] != o['date_sortie'] and liste.get((o['date_entree'][:4], inv.get(o['valeur']))) == 'OUI':\n"
            "        taxe = 100000.0 * (" + repr(PIEGE_TAXE_AVANT) + " if o['date_entree'] <= '2026-04-30' else " + repr(PIEGE_TAXE_APRES) + ")\n"
            "    att = " + repr(PIEGE_COURTAGE) + " * 100000.0 + " + repr(PIEGE_COURTAGE) + " * q * o['px'] + taxe\n"
            "    if abs(o['frais'] - att) > 0.01 or abs(o['net'] - (q * (o['px'] - o['pe']) - o['frais'])) > 0.01:\n"
            "        faux.append((o['valeur'], o['date_entree'], round(o['frais'], 2), round(att, 2), round(o['net'], 2)))\n"
            "taxees = sum(1 for o in ops if o['date_entree'] != o['date_sortie'] and liste.get((o['date_entree'][:4], inv.get(o['valeur']))) == 'OUI')\n"
            "print('OPS', len(ops), 'TAXEES', taxees, 'FAUX', faux[:3])\n"
            # LE POINT MORT ATTENDU, À LA MAIN, AU BARÈME PIÈGE (méthode A, décision de Jean-Luc du 29-10-2026 à 21h28) :
            # pour chaque opération jugée, achat = courtage piège + taxe piège de la période de son ACHAT si la valeur
            # est taxée dans la liste de son année (sans exonération du jour même : le point mort la suppose payée),
            # vente au gain = courtage × 100 000 × (1 + tp), vente au stop = courtage × 100 000 × (1 − sl) ; point mort =
            # 100 × (100 000 × sl + achat + stop) / ((100 000 × tp − achat − gain) + (100 000 × sl + achat + stop)) ;
            # puis la MOYENNE sur les opérations. tp et sl : ceux de la fiche C5E10-QA-V1 (+4,0 % / −2,5 %).
            "tp, sl = B.pourcent(f['tp']), B.pourcent(f['sl'])\n"
            "pms = []\n"
            "for o in ops:\n"
            "    taxe = 0.0\n"
            "    if liste.get((o['date_entree'][:4], inv.get(o['valeur']))) == 'OUI':\n"
            "        taxe = 100000.0 * (" + repr(PIEGE_TAXE_AVANT) + " if o['date_entree'] <= '2026-04-30' else " + repr(PIEGE_TAXE_APRES) + ")\n"
            "    ach = " + repr(PIEGE_COURTAGE) + " * 100000.0 + taxe\n"
            "    vg = " + repr(PIEGE_COURTAGE) + " * 100000.0 * (1 + tp); vp = " + repr(PIEGE_COURTAGE) + " * 100000.0 * (1 - sl)\n"
            "    g = 100000.0 * tp - ach - vg; pe_ = 100000.0 * sl + ach + vp\n"
            "    pms.append(100.0 * pe_ / (g + pe_))\n"
            "att = sum(pms) / len(pms)\n"
            "vus = []\n"
            "mand = types.SimpleNamespace(**{n: getattr(J, n) for n in dir(J) if not n.startswith('__')})\n"
            "def pm(*a, **k):\n"
            "    r = J.point_mort_des_operations(*a, **k); vus.append((a, k, r)); return r\n"
            "mand.point_mort_des_operations = pm\n"
            "mand.etalon_hasard = lambda *a, **k: {}\n"
            "fs = B.trouver(R, 'MODULE_STATISTIQUES'); sp = iu.spec_from_file_location('sta', fs); S_ = iu.module_from_spec(sp); sp.loader.exec_module(S_)\n"
            "seances = {x['date'] for s_ in cr.values() for x in s_}\n"
            "with contextlib.redirect_stdout(io.StringIO()):\n"
            "    B.juger(f, ops, cr, seances, mand, S_, P, mnemo, bornes, (sig,), lecture=lr, bareme='REEL')\n"
            "a, k, r = vus[0] if vus else ((None,) * 5, {}, None)\n"
            "print('JUGER', len(vus), a[2] is ops, (list(a) + [None] * 5)[4] or k.get('bareme'),\n"
            "      'ECART_A_LA_MAIN', 'aucun' if r is not None and abs(r - att) < 1e-9 else (r, att),\n"
            "      'MIN %.4f MAX %.4f' % (min(pms), max(pms)))\n")
    c, o = run(d, "-c", code)
    m15 = re.search(r"OPS (\d+) TAXEES (\d+) FAUX (\[.*\])", o)
    dire("E15 vrai `jouer` au barème piège : chaque opération paie ses frais à la main, gain = variation − frais",
         c == 0 and m15 and int(m15.group(1)) > 10 and int(m15.group(2)) > 0 and m15.group(3) == "[]",
         o.strip()[-200:])
    m15b = re.search(r"MIN (\S+) MAX (\S+)", o)
    dire("E15bis vrai `juger` : point mort moyen des opérations jugées, sous le barème donné, égal au calcul à la main",
         c == 0 and "JUGER 1 True REEL ECART_A_LA_MAIN aucun" in o and m15b and m15b.group(1) != m15b.group(2),
         o.strip()[-200:])
    # E16 (T2, M5 ; C11 amendement 2) une borne du barème mal écrite lève, en nommant la borne
    fb3 = os.path.join(d, "donnees", "BAREME_FRAIS.csv")
    tb3 = open(fb3, encoding="utf-8", newline="").read()
    open(fb3, "w", encoding="utf-8", newline="").write(tb3.replace(",%s,,piege," % PIEGE_FRONTIERE, ",2026-5-1,,piege,"))
    c, o = run(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import MODULE_POSITIONS as p\n"
                        "try:\n    p.cout_d_un_ordre('AIRBUS', '2026-06-01', 'achat', 1000.0)\n    print('PASSE')\n"
                        "except ValueError as e:\n    print('LEVE', e)\n")
    dire("E16 une borne du barème mal écrite (« 2026-5-1 ») lève en nommant la borne",
         "LEVE" in o and "début d'une ligne du barème" in o, o.strip()[-140:])
    # E17 DEUX BARÈMES, DEUX ÉTIQUETTES (relecture de Cowork du 29-10-2026, défaut 1 ; superviseur T3, amendement B)
    def _mesure_sous(bareme):
        dm = tempfile.mkdtemp(prefix="bareme_e17_")
        shutil.copytree(d, dm, dirs_exist_ok=True)
        # les épreuves d'avant (E11bis, E16) ont abîmé le barème de la copie `d` exprès : comme E11, on remet les deux
        # fichiers de données du dépôt (sinon la copie REEL lève sur « 2026-5-1 », mesuré le 29-10-2026)
        for _f in ("VALEURS_TTF.csv", "BAREME_FRAIS.csv"):
            shutil.copy(os.path.join(DEPOT, "donnees", _f), os.path.join(dm, "donnees", _f))
        fm = os.path.join(dm, "programmes", "MODULE_POSITIONS.py")
        tm, n = re.subn(r'^BAREME_DES_VERDICTS = "[^"]*"$', f'BAREME_DES_VERDICTS = "{bareme}"',
                        open(fm, encoding="utf-8").read(), flags=re.M)
        open(fm, "w", encoding="utf-8").write(tm)
        so = os.path.join(dm, "_sortie_e17")
        os.makedirs(os.path.join(so, "donnees"))
        cm, om = run(dm, sorted(glob.glob(os.path.join(dm, "programmes", "MESURER_LA_PERFORMANCE_*.py")))[0], dm, so)
        fh = os.path.join(so, "donnees", "historique_mesures.csv")
        lu = list(csv.DictReader(open(fh, encoding="utf-8"))) if os.path.isfile(fh) else []
        shutil.rmtree(dm)
        return n, cm, lu, om
    nh, ch, lh, oh = _mesure_sous("HIST_COURTAGE_SANS_TTF")
    nr, cr, lr, orr = _mesure_sous("REEL")
    cle = lambda l: (l["strategie"], l["comptabilite"])
    dh, dr = {cle(l): l for l in lh}, {cle(l): l for l in lr}
    mal_h = [k for k, l in dh.items() if l["point_mort"] and not l["verdict_c7"].endswith("(bareme HIST_COURTAGE_SANS_TTF)")]
    mal_r = [k for k, l in dr.items() if l["point_mort"] and not l["verdict_c7"].endswith("(bareme REEL)")]
    differents = [k for k in dh if k in dr and dh[k]["point_mort"] != dr[k]["point_mort"]]
    muets = [k for k in differents if dh[k]["verdict_c7"] == dr[k]["verdict_c7"]]
    avec_pm = [k for k, l in dh.items() if l["point_mort"]]
    dire("E17 deux barèmes des verdicts, deux étiquettes : chaque verdict à point mort nomme le barème de sa copie",
         nh == 1 and nr == 1 and ch == 0 and cr == 0 and lh and set(dh) == set(dr) and avec_pm and differents
         and not mal_h and not mal_r and not muets,
         f"barème posé {nh}/{nr} · codes {ch}/{cr} · {len(lh)}/{len(lr)} ligne(s) · {len(avec_pm)} à point mort · "
         f"{len(differents)} point(s) mort(s) différent(s) · sans étiquette {mal_h[:2]} {mal_r[:2]} · même verdict {muets[:2]}"
         f" · {(oh + orr).strip()[-120:]}")
    # E21 (relecture de Cowork du commit 11ebf39, défaut 1 ; superviseur R-759, T4, R1) TOUTES LES BRANCHES DU VERDICT C7,
    # SOUS LES DEUX BARÈMES. E17 ne voit que ce que le vrai journal donne (4 lignes sur 4 « echantillon insuffisant ») :
    # retirer l'étiquette des branches « vert » et « rouge » restait vert (mutation M1 de Cowork, 22/0). Ici, les VRAIES
    # `stats` et `ligne` de la mesure, dans le processus, sur des opérations fabriquées à partir d'une VRAIE ligne du
    # journal (R-732 ; seuls le gain et, pour un cas, la date d'achat changent), sous HIST_COURTAGE_SANS_TTF puis REEL :
    #   10 gains (borne basse de Wilson > point mort → vert) · 10 pertes (→ rouge) · 3 gains (pas de borne basse →
    #   « echantillon insuffisant », point mort écrit) · aucune opération (case vide, verdict SANS étiquette) ·
    #   10 gains achetés le 01-06-2023 (aucune liste des valeurs taxées pour 2023 : sous REEL, « point mort non
    #   chiffrable », case vide, sans étiquette ; sous le courtage seul la taxe n'est pas lue, la ligne est verte).
    # L'épreuve EXIGE d'avoir atteint les cinq branches que le code de `ligne` porte (vert, rouge, attente avec point
    # mort, attente sans point mort, non chiffrable) : si un seuil bouge et qu'une branche n'est plus atteinte, elle
    # rougit au lieu de se vider en silence. Et chaque verdict à point mort finit par « (bareme <son barème>) ».
    # E17 reste tel quel : c'est lui qui voit un barème lu à deux endroits (S28).
    for _f in ("VALEURS_TTF.csv", "BAREME_FRAIS.csv"):      # E10 et E16 ont abîmé ces deux fichiers de `d` exprès
        shutil.copy(os.path.join(DEPOT, "donnees", _f), os.path.join(d, "donnees", _f))
    c, o = run(d, "-c", "import sys, os, csv, glob, importlib.util as u; sys.path.insert(0, 'programmes')\n"
                        "prog = sorted(glob.glob(os.path.join('programmes', 'MESURER_LA_PERFORMANCE_*.py')))[0]\n"
                        "s = u.spec_from_file_location('mes', prog); m = u.module_from_spec(s); s.loader.exec_module(m)\n"
                        "vraie = list(csv.DictReader(open(os.path.join('donnees', 'claude_journal_trades.csv'), encoding='utf-8')))[0]\n"
                        "carte = next(r for r in csv.DictReader(open(os.path.join('donnees', 'cac40_strategies.csv'), encoding='utf-8-sig')) "
                        "if (r.get('etat_vie') or '').strip().upper() in ('QA', 'PRODUCTION'))\n"
                        "f = lambda n, pnl, **k: [dict(vraie, pnl_net_eur=pnl, **k) for _ in range(n)]\n"
                        "cas = {'vert': f(10, '3000'), 'rouge': f(10, '-2600'), 'insuffisant': f(3, '3000'), 'aucune': [],\n"
                        "       'sans_liste': f(10, '3000', date_entree='2023-06-01')}\n"
                        "vus, faux = set(), []\n"
                        "for bar in ('HIST_COURTAGE_SANS_TTF', 'REEL'):\n"
                        "    m._positions().BAREME_DES_VERDICTS = bar\n"
                        "    for nom, ops in cas.items():\n"
                        "        l = m.ligne('2026-10-28', carte['id'], 'un jeton', 'QA', m.stats(ops, 'pnl_net_eur'), carte, None, '', '', None, '', ops)\n"
                        "        v = l['verdict_c7']\n"
                        "        vus.add('non_chiffrable' if v.startswith(m.PREFIXE_NON_CHIFFRABLE) else l['voyant_c7'] + ('/pm' if l['point_mort'] else '/vide'))\n"
                        "        bon = v.endswith('(bareme %s)' % bar) if l['point_mort'] else '(bareme' not in v\n"
                        "        if not bon: faux.append((bar, nom, v))\n"
                        "print('BRANCHES', ','.join(sorted(vus)), 'FAUX', len(faux), faux[:2])\n")
    m21 = re.search(r"BRANCHES (\S+) FAUX (\d+)", o)
    attendues21 = {"vert/pm", "rouge/pm", "attente/pm", "attente/vide", "non_chiffrable"}
    dire("E21 vraies `stats` et `ligne`, deux barèmes : les cinq branches du verdict atteintes, chaque verdict à point "
         "mort étiqueté de son barème, les autres sans étiquette",
         c == 0 and m21 and set(m21.group(1).split(",")) >= attendues21 and m21.group(2) == "0",
         f"attendues {sorted(attendues21)} · {o.strip()[-220:]}")
    # E18 COURBE PLATE (relecture de Cowork du 29-10-2026, défaut 2 ; prototype du superviseur T3) : aucune règle de
    # sélection n'est refaite ici — on appelle les VRAIES fonctions, et l'attendu est le capital lu dans le module
    c, o = run(d, "-c", "import sys, os, csv, glob, tempfile, importlib.util as u\n"
                        "prog = sorted(glob.glob(os.path.join('programmes', 'MESURER_LA_PERFORMANCE_*.py')))[0]\n"
                        "s = u.spec_from_file_location('mes', prog); m = u.module_from_spec(s); s.loader.exec_module(m)\n"
                        "base = tempfile.mkdtemp(prefix='courbe_plate_'); os.makedirs(os.path.join(base, 'donnees'))\n"
                        "with open(os.path.join('donnees', 'cours_maitre.csv'), encoding='utf-8') as f, "
                        "open(os.path.join(base, 'donnees', 'cours_maitre.csv'), 'w', encoding='utf-8', newline='') as g:\n"
                        "    r = csv.DictReader(f); w = csv.DictWriter(g, fieldnames=r.fieldnames); w.writeheader()\n"
                        "    for l in r:\n        l.update(open='100', high='100', low='100', close='100'); w.writerow(l)\n"
                        "ops = list(csv.DictReader(open(os.path.join('donnees', 'claude_journal_trades.csv'), encoding='utf-8')))\n"
                        "for o in ops:\n    o['pnl_net_eur'] = '0'; o['pnl_net_convention_eur'] = '0'; o['prix_entree'] = '100'\n"
                        "seances, courbe = m.courbe_capital(ops, base, None)\n"
                        "ecarts = [x - m.CAPITAL for x in courbe if abs(x - m.CAPITAL) > 1e-6]\n"
                        "st = m.stats(ops, 'pnl_net_eur')\n"
                        # LA PROPRIÉTÉ, PAS UNE LISTE (superviseur R-759, T4, R2) : la VRAIE `ligne`, et TOUTE colonne
                        # publiée dont le nom finit par `_eur` — liste lue dans `COLONNES` du programme, jamais recopiée
                        "gs = m.rapport_gain_secousses(courbe)\n"
                        "carte = next(r for r in csv.DictReader(open(os.path.join('donnees', 'cac40_strategies.csv'), encoding='utf-8-sig')) "
                        "if (r.get('etat_vie') or '').strip().upper() in ('QA', 'PRODUCTION'))\n"
                        "l = m.ligne('2026-10-28', carte['id'], 'un jeton', 'QA', st, carte, None, '', '', gs, '', ops)\n"
                        "eur = {k: l.get(k) for k in m.COLONNES if k.endswith('_eur')}\n"
                        "non_nulles = {k: v for k, v in eur.items() if v in (None, '') or abs(float(v)) > 1e-9}\n"
                        "print('OPS', len(ops), 'SEANCES', len(seances), 'HORS_CAPITAL', len(ecarts), "
                        "'PREMIER', ecarts[0] if ecarts else '-', 'CUMUL', st['cumul'], 'CHUTE', st['chute_eur'], "
                        "'EUR', len(eur), 'NON_NULLES', repr(non_nulles).replace(' ', ''), 'GS', repr(l['rapport_gain_secousses']).replace(' ', '_'))\n")
    m18 = re.search(r"OPS (\d+) SEANCES (\d+) HORS_CAPITAL (\d+) PREMIER \S+ CUMUL (\S+) CHUTE (\S+) EUR (\d+) NON_NULLES (\S+) GS (\S+)", o)
    dire("E18 un journal sans gain sur des cours plats donne une mesure sans gain : courbe plate, toute colonne publiée "
         "en `_eur` nulle, rapport gain/secousses « non calculable »",
         c == 0 and m18 and int(m18.group(1)) > 0 and int(m18.group(2)) > 0 and m18.group(3) == "0"
         and abs(float(m18.group(4))) < 1e-9 and abs(float(m18.group(5))) < 1e-9 and int(m18.group(6)) > 0
         and m18.group(7) == "{}" and m18.group(8) == "'non_calculable'", o.strip()[-200:])
    # E19 PROPRIÉTÉ DU POINT MORT DES OPÉRATIONS (méthode A, décision de Jean-Luc du 29-10-2026 à 21h28), sur une copie
    # NEUVE (sabotage compris) et le barème réel du dépôt. Attendus À LA MAIN, +4 % / −2,5 %, 100 000 € par opération ;
    # courtage 0,15 % : 150 € à l'achat, 156 € à la vente au gain, 146,25 € à la vente au stop ; gain + perte vaut
    # (4 000 − achat − 156) + (2 500 + achat + 146,25) = 6 490,25 € quel que soit l'achat :
    #   Airbus 27-07-2026, non taxée (courtage seul) : 100 × 2 796,25 / 6 490,25 = 43,0839 %
    #   Bouygues 27-07-2026, taxe 0,4 % (+400 €)      : 100 × 3 196,25 / 6 490,25 = 49,2469 %
    #   trois Airbus + un Bouygues : 100 × (3 × 2 796,25 + 3 196,25) / 4 / 6 490,25 = 44,6246 % — élevé de
    #     (49,2469 − 43,0839) / 4 = 1,5408 point, PAS jusqu'à 49,25 (ce que rendrait le pire cas)
    #   Bouygues signalée le 31-03-2025 (taxe 0,3 %) et achetée le 01-04-2025 (taxe 0,4 %) : la taxe du jour de
    #     l'ACHAT, 49,2469 % ; au jour du signal ce serait 100 × 3 096,25 / 6 490,25 = 47,7062 %.
    #   liste vide : ValueError.
    d19 = copie(sab)
    c, o = run(d19, "-c", "import sys; sys.path.insert(0, 'programmes')\n"
                          "import MODULE_JUGEMENT as J, MODULE_POSITIONS as P\n"
                          "A = dict(valeur='AIRBUS', date_entree='2026-07-27')\n"
                          "E = dict(valeur='BOUYGUES', date_entree='2026-07-27')\n"
                          "pm = lambda ops: J.point_mort_des_operations(0.04, 0.025, ops, P, 'REEL')\n"
                          "x = [pm([A, A, A]), pm([A, A, A, E]),\n"
                          "     pm([dict(valeur='BOUYGUES', date_signal='2025-03-31', date_entree='2025-04-01')])]\n"
                          "try:\n    pm([]); vide = 'PASSE'\nexcept ValueError:\n    vide = 'LEVE'\n"
                          "print('PM ' + ' '.join('%.4f' % v for v in x) + ' VIDE ' + vide)\n")
    shutil.rmtree(d19)
    courtage_seul = 100 * 2796.25 / 6490.25
    att19 = "PM %.4f %.4f %.4f VIDE LEVE" % (courtage_seul, 100 * (3 * 2796.25 + 3196.25) / 4 / 6490.25,
                                             100 * 3196.25 / 6490.25)
    dire("E19 propriété : opérations non taxées = courtage seul ; une taxée de plus élève de (taxée − courtage)/N ; "
         "taxe du jour d'achat ; liste vide lève", c == 0 and att19 in o, f"attendu « {att19} » · {o.strip()[-160:]}")
    # E20 (relecture de la barre A, I1, 29-10-2026) LES OPÉRATIONS DU POINT MORT PUBLIÉ SONT CELLES DE LA STRATÉGIE ET DE
    # LA COMPTABILITÉ MESURÉES. Sur le vrai journal, les sept lignes portent sur des valeurs taxées en 2026 : le point
    # mort vaut 49,2 quelles que soient les opérations passées, et passer tout le journal (X1) ou mélanger les deux
    # comptabilités (X2) restait vert. Dans une copie NEUVE, la vraie mesure tourne sur un journal FABRIQUÉ qui mêle
    # Airbus (non taxée) et Bouygues (taxée), deux stratégies et deux comptabilités ; la vraie ligne Bureau Veritas
    # (27-07-2026, `COURS_BAS_ARGENT_REVIENT_10`, jetons illimités) est gardée : le calibrage de la mesure l'exige.
    # Attendus À LA MAIN, +4 % / −2,5 % (les deux fiches), barème réel, 100 000 € ; gain + perte = 6 490,25 € :
    #   A = Airbus 2026, non taxée          : 100 × 2 796,25 / 6 490,25 = 43,08 % → « 43.1 »
    #   B = Bouygues ou Bureau Veritas 2026 : 100 × 3 196,25 / 6 490,25 = 49,25 % → « 49.2 »
    #   C5E10-QA-V1  · un jeton         : [A]          → 43,08 → « 43.1 »
    #   C5E10-QA-V1  · jetons illimités : aucune       → case vide, « echantillon insuffisant » SANS étiquette
    #   C5E10-OBS-V1 · un jeton         : [A, B]       → (43,08 + 49,25) / 2 = 46,17 → « 46.2 »
    #   C5E10-OBS-V1 · jetons illimités : [BV, A, A]   → (49,25 + 2 × 43,08) / 3 = 45,14 → « 45.1 »
    # Tout le journal (X1) donnerait 100 × (4 × 2 796,25 + 2 × 3 196,25) / 6 / 6 490,25 = 45,14 partout ; les
    # comptabilités mélangées (X2), 43,1 aux deux lignes de QA et 45,5 aux deux d'OBS.
    d20 = copie(sab)
    fm20 = os.path.join(d20, "programmes", "MODULE_POSITIONS.py")
    tm20, n_bv20 = re.subn(r'^BAREME_DES_VERDICTS = "[^"]*"$', 'BAREME_DES_VERDICTS = "REEL"',
                           open(fm20, encoding="utf-8").read(), flags=re.M)
    open(fm20, "w", encoding="utf-8").write(tm20)
    fj20 = os.path.join(d20, "donnees", "claude_journal_trades.csv")
    lu20 = list(csv.DictReader(open(fj20, encoding="utf-8")))
    champs20 = list(lu20[0].keys()) if lu20 else []
    bv20 = [o for o in lu20 if "BUREAU" in (o.get("valeur") or "").upper()][:1]
    def _op(strat, val, compta, pnl):
        o = dict(bv20[0]) if bv20 else {}
        o.update(strategie=strat, valeur=val, date_entree="2026-09-01", prix_entree="100", date_sortie="2026-09-03",
                 prix_sortie="104", motif_sortie="TP", pnl_net_eur=pnl, prix_sortie_convention="104",
                 pnl_net_convention_eur=pnl, comptabilite=compta, regles_pre_trade="",
                 explication="ligne FABRIQUÉE par l'épreuve E20 (copie)", bareme_reel="REEL", bareme_convention="REEL")
        return o
    fab20 = bv20 + [_op("C5E10-QA-V1", "AIRBUS", "un_jeton", "3694.00"),
                    _op("C5E10-OBS-V1", "AIRBUS", "un_jeton", "3694.00"),
                    _op("C5E10-OBS-V1", "BOUYGUES", "un_jeton", "3294.00"),
                    _op("C5E10-OBS-V1", "AIRBUS", "jetons_illimites", "3694.00"),
                    _op("C5E10-OBS-V1", "AIRBUS", "jetons_illimites", "3694.00")]
    with open(fj20, "w", encoding="utf-8", newline="") as g20:
        w20 = csv.DictWriter(g20, fieldnames=champs20); w20.writeheader(); w20.writerows(fab20)
    s20 = os.path.join(d20, "_sortie_e20")
    os.makedirs(os.path.join(s20, "donnees"))
    c, o = run(d20, sorted(glob.glob(os.path.join(d20, "programmes", "MESURER_LA_PERFORMANCE_*.py")))[0], d20, s20)
    fh20 = os.path.join(s20, "donnees", "historique_mesures.csv")
    lignes20 = {(l["strategie"], l["comptabilite"]): (l["point_mort"], l["verdict_c7"])
                for l in (csv.DictReader(open(fh20, encoding="utf-8")) if os.path.isfile(fh20) else [])}
    shutil.rmtree(d20)
    pmA, pmB = 100 * 2796.25 / 6490.25, 100 * 3196.25 / 6490.25
    att20 = {("C5E10-QA-V1", "un jeton"): "%.1f" % pmA,
             ("C5E10-QA-V1", "jetons illimites"): "",
             ("C5E10-OBS-V1", "un jeton"): "%.1f" % ((pmA + pmB) / 2),
             ("C5E10-OBS-V1", "jetons illimites"): "%.1f" % ((pmB + 2 * pmA) / 3)}
    obt20 = {k: v[0] for k, v in lignes20.items()}
    vide20 = lignes20.get(("C5E10-QA-V1", "jetons illimites"), ("?", "?"))[1]
    dire("E20 point mort publié sur les opérations de SA stratégie et de SA comptabilité (journal fabriqué Airbus + "
         "Bouygues) ; sans opération, case vide et verdict sans étiquette",
         n_bv20 == 1 and len(bv20) == 1 and c == 0 and obt20 == att20 and vide20 == "echantillon insuffisant",
         f"obtenu {obt20} · attendu {att20} · verdict sans opération {vide20!r} · code {c} · {o.strip()[-120:]}")
    # E12 aucun nom lu sans définition (C1)
    c, o = run(d, "-m", "pyflakes", *sorted(glob.glob(os.path.join(d, "programmes", "*.py"))))
    absent = "No module named pyflakes" in o
    indef = [l.replace(d + os.sep, "") for l in o.splitlines() if "undefined name" in l]
    dire("E12 aucun nom lu sans définition dans programmes/ (pyflakes)", not absent and not indef,
         "pyflakes absent : pip install pyflakes" if absent else " · ".join(indef[:3]))
    shutil.rmtree(d)
    return res


_choix = (list(SABOTAGES) if "--saboter" in sys.argv else [_args[1]] if len(_args) > 1 else ["Z0"])
_faute = False
for sab in _choix:
    try:
        r = epreuves(sab)
    except Exception as e:                     # un plantage n'est JAMAIS compté comme un sabotage vu
        r = [("PLANTAGE de l'épreuve", None, f"{type(e).__name__} : {e}")]
    plante = any(x[1] is None for x in r)
    rouges = [x for x in r if not x[1]]
    vert = sab == "Z0"
    print(f"== {sab} : {len(r) - len(rouges)} vertes, {len(rouges)} rouges" + (
        "  <-- PLANTAGE" if plante else
        "  <-- ATTENDU : 0 rouge" if vert and rouges else "  <-- SABOTAGE NON VU" if not vert and not rouges else ""))
    for nom, ok, det in r:
        if not ok:
            print(f"     ROUGE {nom} · {det}")
    _faute = _faute or plante or (vert and bool(rouges)) or (not vert and not rouges)
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
