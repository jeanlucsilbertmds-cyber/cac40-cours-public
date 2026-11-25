#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_FORFAIT — Dim 15-11-2026 (Paris)

Simulation boursière uniquement : rien ici ne touche aux cours ni aux positions.

À QUOI ÇA SERT. Prouver que programmes/TENIR_LE_FORFAIT.py tient son journal sans le réécrire, rend INCONNU quand les
données ne suffisent pas (jamais un chiffre inventé), rend ARRÊTER LES NOUVEAUX AGENTS au seuil, et lit le seuil dans
donnees/REGLAGES_DU_FORFAIT.csv et nulle part ailleurs (R-708). Décision de Jean-Luc du 15-11-2026 à 12h42 (A-804),
après l'épuisement sans alerte du 14-11 vers 22h45 (A-799).

LANCEMENT : python3 -B tests/EPREUVES_DU_FORFAIT_Dim_15-11-2026.py <racine> [--saboter [--lot K/N]]
  Sans option : les épreuves sur programmes/TENIR_LE_FORFAIT.py de <racine>. Code 0 si toutes vertes, 1 sinon.
  --saboter : les épreuves, puis chaque sabotage sur une COPIE du programme dans un dossier temporaire ; chacun doit
  faire rougir l'épreuve nommée. Un sabotage dont le texte n'est pas trouvé, ou qui laisse cette épreuve verte, rend
  le code 1 (R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0).
  --lot K/N (ajouté le 25-11-2026) : ne joue que les sabotages de rang K, K+N, K+2N… (rangs comptés de 1), pour que
  chaque lancement tienne sous deux minutes ; les N lots ensemble jouent chaque sabotage une fois. Le code 0 d'un lot
  ne dit rien des autres lots.

LES ÉPREUVES (journal et réglages fabriqués dans un dossier temporaire, sauf E11) :
  E1 append-only : trois ajouts ; chaque fois, le fichier d'avant est le DÉBUT exact du fichier d'après ; un seul
     en-tête.
  E2 INCONNU, deux cas : (a) une seule capture (10 %) puis un agent de 500 000 jetons ; (b) deux captures (0 %, 10 %)
     SANS agent inscrit entre elles, puis un agent → rapport, jauge, projection INCONNUS, verdict INCONNU, code 5,
     aucun « JAUGE ESTIMÉE MAINTENANT : <nombre> ».
  E3 ARRÊTER, au seuil exact : captures 0 % (10h00) et 10 % (12h00), 1 000 000 jetons entre elles (rapport 100 000),
     puis 8 500 000 jetons → jauge 95,0 % → ARRÊTER LES NOUVEAUX AGENTS, code 4.
  E4 ALERTER, au bord exact : même chose avec 7 500 000 jetons → 85,0 % → ALERTER, code 3.
  E5 CONTINUER et chiffres : 1 000 000 jetons après → jauge projetée 20,0 % (10 points de jetons > 5 × 1 h) ; rythme 5,00 points/h ; rapport 100000 ;
     prochaine remise 2026-11-18 02:00, maintenant 2026-11-15 13:00 → 61 h → projection 20 + 5 × 61 = 325,0 % ;
     seuil (95 − 20) ÷ 5 = 15 h → 2026-11-16 04:00.
  E6 LES RÉGLAGES VIENNENT DU FICHIER : le cas E5 (jauge 20 %) avec seuil 25 → ALERTER (20 ≥ 25 − 10) ; seuil 20 →
     ARRÊTER ; marge 4 et seuil 25 → CONTINUER (20 < 21) ; âge maximal 0,5 h (capture vieille d'1 h) → INCONNU.
  E7 réglage absent, en double, `nan` ou `inf` (F-5), ou fichier manquant → code 2, « ERREUR RÉGLAGE », aucun
     « VERDICT ».
  E8 plancher : dernière capture 96 %, rapport inconnu → ARRÊTER (sur le plancher), code 4.
  E9 la remise coupe la période : 90 % avant une remise, puis 0 % et 10 % après, agents entre → seul l'après compte :
     CONTINUER, jauge projetée 15,0 % (10 + rythme de pointe 5 × âge 1 h, A-827), et pas d'ANOMALIE.
  E10 une ligne postérieure à --maintenant est ignorée et comptée : une capture de 99 % datée du lendemain ne change
     pas le verdict CONTINUER du cas E5.
  E11 VRAIES DONNÉES (R-732) : le vrai journal et le vrai réglage de <racine> à --maintenant 2026-11-15T13:00 →
     période depuis la remise du 2026-11-15 12:14, prochaine 2026-11-18 02:00, dernière capture 0 %, seuil 95,
     verdict INCONNU ; à 2026-11-14T23:00 → plancher 100 % (épuisement inscrit après coup) → ARRÊTER. LA VRAIE PREUVE
     (F-2 de Cowork) : le journal COUPÉ aux cinq vraies captures (28 → 75 %), tel qu'il était le 14-11 au soir, à
     13h30, 19h00 et 22h44 → INCONNU, « demander une capture », la règle « pas de nouvel agent » affichée, jamais
     CONTINUER. Le programme n'ARRÊTE pas ces soirs-là : il rend INCONNU. Et (G-1) à 2026-11-15T16:00, sur les
     vraies captures du 15-11 (0 %, 10 %, 17 %) → « au moins 8.5 points » (G-5 : 17 ÷ 2 fenêtres), sous la marge.
     Et (25-11-2026) le vrai relevé de Jean-Luc, 2 % à 11h55 après la remise du 25-11 à 02h00, à 12h00 → période
     depuis le 2026-11-25 02:00, dernière 2 %, VERDICT INCONNU (une seule capture dans la période).
  E12 refus d'entrée sans écriture : capture 120, capture sans --a, jetons « 12k », heure « 15/11/2026 » → code 2,
     journal inchangé à l'octet.
  E13 baisse sans remise : 50 % puis 40 % → ANOMALIE dite, rythme et rapport INCONNUS.
  E14 (F-1 de Cowork) capture vieille : remise 07h00, captures 70 % (08h00) et 80 % (10h00), 2 000 000 jetons entre
     elles, plus rien ; à 16h00 → INCONNU, code 5, « capture vieille de 6.0 h », jamais CONTINUER.
  E17 (F-3) journal sans son dernier saut de ligne : --capture 97 → code 2, journal inchangé à l'octet.
  E18 (F-3) deux lignes déjà collées : --etat → code 2, ERREUR, aucun VERDICT.
  E20 (F-8) aucune constante 95, 85 ou 10 dans le CODE du programme (arbre syntaxique, textes explicatifs exclus).
  E21 (F-4, G-2) valeur illisible au journal (« 12k » ou « ² » pour un agent, vide pour une capture) → code 2, ERREUR,
     pas de trace.
  E22 (F-6) changement d'heure : 10 % à 01h30 et 20 % à 03h30 le 28-03-2027 = 1 h réelle → 10.00 points/h.
  E23 (F-7) en-tête changé · type inconnu (message « type inconnu ») · seuil 120 → code 2 ; remise suivante avant la remise · virgule dans
     l'étiquette → code 2, journal inchangé.
  E24 (G-3, SY1) capture de 120 % écrite à la main au journal → code 2, ERREUR, aucun VERDICT.
  E25 (G-3, SY2) âge en heures réelles : capture à 01h30, maintenant 03h50 le 28-03-2027 → « vieille de 1.3 h ».
  E26 (G-3, SY4) ajout sur un journal à l'en-tête « type;horodatage » → code 2, journal inchangé à l'octet.
  E27 (G-1, G-5) trou de la fenêtre d'âge : (a) 0 % 12h14, 10 % 14h16, 17 % 15h27 → « au moins 8.5 points »,
     sous la marge (17 ÷ plafond(3,217 ÷ 2) = 17 ÷ 2 ; l'ancienne extrapolation 17 × 2 ÷ 3,217 = 10,6 n'était pas une
     borne) ; (b) 0 % puis 6 % en 30 min → « au moins 6.0 points », couvert (pas 24) ;
     (c) remise entre les deux captures → trou INCONNU.
  E28 (G-4) 96 % à 08h00 puis 9,6 % à 09h00 → plancher 96 %, ARRÊTER, code 4. (G-6) puis 97 % à 09h30 : la ligne
     TROU ne se mesure pas sur une période en ANOMALIE → « TROU … : INCONNU » (avant : « au moins 87.4 points »).
  E29 (A-827, décision de Jean-Luc du 15-11-2026 à 16h41) JAUGE PROJETÉE : captures 60 % (06h00), 72 % (08h00),
     80 % (10h00), rapport connu, rythme de pointe 6 points/h → (a) 10h30 : 83,0 %, CONTINUER ; (b) 11h55 : 91,5 %,
     ALERTER ; (c) 10h55 : 85,5 %, ALERTER (au rythme moyen ou au dernier rythme : CONTINUER) ; (d) le plus grand
     des deux termes, pas leur somme : 90,0 % ; (e) rythme de pointe inconnu, rapport connu → INCONNU.
  E30 (P-2 de Cowork) semaine passée 10 → 25 % en 1 h ; remise ; 70 % (08h00) → 74 % (10h00), un agent entre les
     deux ; à 11h55 → RYTHME DE POINTE 2.00 (la période en cours seulement), la ligne TROU (15 points, NON COUVERT)
     dit « mesuré AVANT la dernière remise » et ne prétend pas que le verdict le compte.
  E31 (K-1 de Cowork) sans agent inscrit : 60, 72, 88 % (06h, 08h, 10h) à 11h55 → « AU MOINS 103.3 % », « au-delà
     de 100 » (K-3), ARRÊTER sur la borne basse, code 4 (avant : ALERTER sur le plancher) ; 60, 72, 84 % → 95,5 %,
     ARRÊTER, code 4 (avant : INCONNU) ; 10 % puis 20 % → la borne basse ne rend jamais CONTINUER : INCONNU, code 5.
  E32 (P-1, K-2 de Cowork) 40 % (06h00), un agent, 50 % (10h00), 51 % (10h01), à 10h40 : durée minimale 0 →
     RYTHME DE POINTE 60.00, ALERTER, code 3 (comportement du 15-11, gardé tant que Jean-Luc n'a pas choisi) ;
     durée minimale 0,5 h → la paire de 10h01 part de 06h00 : 2.74 points/h, CONTINUER, code 0.
  E33 (R-1 et C-1 de Cowork, 25-11-2026) 70 % (10h00), 100 000 jetons, 75 % (10h10), 240 000 jetons (10h40), à
     11h00 : durée minimale 0 → jauge 100,0 %, ARRÊTER ; 0,5 h → pointe écartée (le motif le dit), « AU MOINS
     87.0 % » par les jetons ÷ rapport, ALERTER code 3 (avant : INCONNU) ; 20 000 jetons → 76 %, INCONNU, jamais
     CONTINUER.
  E34 (C-3 et R-2 de Cowork, 25-11-2026) paire du 15-11 (0 → 17 %) puis remise du 25-11 : la ligne TROU « sous la
     marge » dit « mesuré AVANT la dernière remise » ; 50 % puis 62 % à la même minute : pointe INCONNUE, la ligne
     TROU dit « le verdict ne compte donc pas ce trou » et jamais « le verdict compte déjà » ; 50 % (08h00) puis 62 %
     (08h30), à 11h00 (capture plus vieille que l'âge maximal) : pointe 24, mais la ligne dit « le verdict ne compte
     pas ce trou — capture vieille … ».

LES SABOTAGES (chacun doit faire rougir l'épreuve entre parenthèses) :
  S1 seuil écrit en dur à 95 dans le code (E6) · S2 rapport inventé (100 000) quand il est inconnu (E2) · S3 « ≥ »
  devient « > » pour l'arrêt (E3) · S4 le journal s'ouvre en réécriture (E1) · S5 la remise ne coupe plus la période
  (E9) · S6 les lignes futures ne sont plus écartées (E10) · S7 plus de plancher (E8) · S8 un pourcentage n'est plus
  borné (E12) · S9 marge écrite en dur à 10 (E6) · S10 jauge = dernière capture quand le rapport est inconnu (E2) ·
  S11 le test d'âge retiré (E14) · S14 l'âge maximal écrit en dur à 2 (E6) · S16 la fin de ligne non vérifiée (E17) ·
  S17 les champs en trop acceptés (E18) · S19 la valeur non lue (E21) · S20 écart à l'horloge murale (E22) · S21
  réglage non fini accepté (E7) · SX3, SX4, SX6, SX7, SX8 (sabotages de Cowork : type, en-tête, bornes du seuil,
  ordre des remises, virgule) (E23) · S22 « ² » accepté (E21) · SY1, SY2, SY4 (sabotages de Cowork du tour 2 :
  bornes de la capture à la lecture, âge à l'horloge murale, ajout sans relire le journal) (E24, E25, E26) · S23 trou
  non mesuré, S24 trou extrapolé sur une paire courte, S25 paire à travers une remise (E27) · S26 plancher sur la
  dernière capture (E28) · S27 terme rythme × âge retiré, S28 rythme moyen au lieu du rythme de pointe, S29 rythme
  des deux dernières captures, S30 somme au lieu du plus grand, S31 rythme de pointe inconnu toléré (E29). Retirés le 15-11-2026 sur avis du superviseur R-759 : E15, E16, S12, S13.
  Ajoutés le 25-11-2026 : S32 période en ANOMALIE mesurée quand même (E28) · S33 rythme de pointe à travers les
  remises — le M2 de Cowork (E30) · S34 la ligne TROU dit toujours « le verdict compte déjà » (E30) · S35 borne basse
  jamais calculée (E31) · S36 la borne basse permet CONTINUER (E31) · S37 durée minimale ignorée (E32) · S38 durée
  minimale négative acceptée (E7). S24 remet désormais l'extrapolation (E27, E11).
  Ajoutés le 25-11-2026 (tour 7, RELU de Cowork de 14h34, N-1) : S39 la borne « jetons ÷ rapport » retirée (E33) · S40
  le motif ne dit pas la durée minimale (E33) · S41 la ligne TROU « sous la marge » tait la période (E34) · S42 la
  ligne TROU dit toujours « le verdict compte déjà » (E34) · S43 elle le dit dès que la pointe est connue, même
  quand le verdict ne la compte pas (E34). S34 suit le nouveau texte de la ligne TROU.
"""
import ast, os, re, shutil, subprocess, sys, tempfile

PROG = "TENIR_LE_FORFAIT.py"
REGL = ("reglage,valeur,etat,qui_decide,raison\nseuil_d_arret,{s},x,x,x\nmarge_d_alerte,{m},x,x,x\n"
        "age_max_de_la_capture,{a},x,x,x\nduree_min_d_une_paire,{p},x,x,x\n")
RET = 'return vus["seuil_d_arret"], vus["marge_d_alerte"], vus["age_max_de_la_capture"], vus["duree_min_d_une_paire"]'

SABOTAGES = {
    "S1_seuil_en_dur": ("E6", RET, RET.replace('vus["seuil_d_arret"]', '95.0')),
    "S2_rapport_invente": ("E2", '            e["pourquoi_rapport"] = "aucun agent inscrit entre la première et la dernière capture"',
                           '            e["rapport"] = 100000.0'),
    "S3_strict": ("E3", 'if base is not None and base >= seuil:', 'if base is not None and base > seuil:'),
    "S4_reecriture": ("E1", 'with open(chemin, "a", encoding="utf-8", newline="") as f:',
                      'neuf = True\n    with open(chemin, "w", encoding="utf-8", newline="") as f:'),
    "S5_remise_ignoree": ("E9", "periode = [l for i, l in passees if l[\"type\"] != \"remise\" and (l[\"t\"] > debut or (l[\"t\"] == debut and i > i0))]",
                          "periode = [l for i, l in passees if l[\"type\"] != \"remise\"]"),
    "S6_futur_garde": ("E10", 'if l["t"] > maintenant:', 'if False:'),
    "S7_sans_plancher": ("E8", 'for x in (e["jauge"], e["borne"], e["plancher"]) if x is not None',
                         'for x in (e["jauge"], e["borne"]) if x is not None'),
    "S8_pourcentage_non_borne": ("E12", "if not 0 <= v <= 100:", "if False:"),
    "S9_marge_en_dur": ("E6", RET, RET.replace('vus["marge_d_alerte"]', '10.0')),
    "S11_age_retire": ("E14", 'if e["age"] > age_max:', 'if False:'),
    "S14_age_en_dur": ("E6", RET, RET.replace('vus["age_max_de_la_capture"]', '2.0')),
    "S16_fin_de_ligne_ignoree": ("E17", 'if f.read(1) != b"\\n":', 'if False:'),
    "S17_champs_en_trop_acceptes": ("E18", 'if None in l or any(v is None for v in l.values()):', 'if False:'),
    "S19_valeur_non_lue": ("E21", 'if not ok:\n                raise ValueError(f"ligne {n}', 'if False:\n                raise ValueError(f"ligne {n}'),
    "S20_horloge_murale": ("E22", 'return (fin.astimezone(timezone.utc) - debut.astimezone(timezone.utc)).total_seconds() / 3600',
                           'return (fin - debut).total_seconds() / 3600'),
    "S21_reglage_non_fini": ("E7", 'if not all(math.isfinite(v) for v in vus.values()):', 'if False:'),
    "SX3_type_inconnu": ("E23", 'if l["type"] not in ("capture", "agent", "remise"):', 'if False:'),
    "SX4_entete_non_verifie": ("E23", 'if lecteur.fieldnames != COLONNES:', 'if False:'),
    "SX6_seuil_hors_bornes": ("E23", 'not 0 < vus["seuil_d_arret"] <= 100 or', 'False and'),
    "SX7_remises_dans_le_desordre": ("E23", 'if prochaine <= quand:', 'if False:'),
    "SX8_virgule_dans_l_etiquette": ("E23", 'if not etiquette.strip() or "," in etiquette or "\\n" in etiquette:',
                                     'if not etiquette.strip():'),
    "S10_jauge_sans_rapport": ("E2", '''        elif e["rapport"] is None:
            e["pourquoi_jauge"]''', '''        elif e["rapport"] is None:
            e["jauge"] = float(der["valeur"])
            e["pourquoi_jauge"]'''),
    "S22_exposant_accepte": ("E21", 'v.isascii() and v.isdigit() and int(v) >= 0', 'v.isdigit()'),
    "SY1_capture_non_bornee_a_la_lecture": ("E24", '(l["type"] == "capture" and 0 <= float(v) <= 100)',
                                            '(l["type"] == "capture" and float(v) == float(v))'),
    "SY2_age_a_l_horloge_murale": ("E25", 'e["age"] = heures(der["t"], maintenant)',
                                   'e["age"] = (maintenant - der["t"]).total_seconds() / 3600'),
    "SY4_ajout_sans_relire": ("E26", 'lignes = lire_journal(o.journal)', 'lignes = lire_journal(o.journal) if o.etat else []'),
    "S23_trou_non_mesure": ("E27", 'e["trou"] = trou_mesure(passees, age_max)', 'e["trou"] = None'),
    "S24_trou_extrapole": ("E27", 'borne = points / fenetres',
                           'borne = points * age_max / max(heures(a["t"], b["t"]), age_max)'),
    "S25_trou_a_travers_la_remise": ("E27", 'if pb != pa:', 'if False:'),
    "S26_plancher_derniere_capture": ("E28", 'e["plancher"] = max(float(c["valeur"]) for c in caps)',
                                      'e["plancher"] = float(der["valeur"])'),
    # A-827 (Jean-Luc, 15-11-2026 16h41) : la jauge projetée
    "S27_sans_rythme_x_age": ("E29", 'max(e["terme_jetons"], e["terme_rythme"])', 'e["terme_jetons"]'),
    "S28_rythme_moyen": ("E29", 'e["pointe"], e["pointe_de"], e["pointe_a"] = rythme_pointe(caps, duree_min)',
                         'e["pointe"], e["pointe_de"], e["pointe_a"] = ((float(caps[-1]["valeur"]) - '
                         'float(caps[0]["valeur"])) / heures(caps[0]["t"], caps[-1]["t"]), caps[0], caps[-1])'),
    "S29_rythme_des_deux_dernieres": ("E29", 'e["pointe"], e["pointe_de"], e["pointe_a"] = rythme_pointe(caps, duree_min)',
                                      'e["pointe"], e["pointe_de"], e["pointe_a"] = rythme_pointe(caps[-2:], duree_min)'),
    "S30_somme_au_lieu_du_plus_grand": ("E29", 'max(e["terme_jetons"], e["terme_rythme"])',
                                        'e["terme_jetons"] + e["terme_rythme"]'),
    "S31_pointe_inconnue_toleree": ("E29", '''        elif e["pointe"] is None:
            e["pourquoi_jauge"]''', '''        elif False:
            e["pourquoi_jauge"]'''),
    # 25-11-2026 : corrections du RELU de Cowork du 15-11-2026 (pointe 0731e8b1)
    "S32_anomalie_mesuree": ("E28", 'if pa in en_anomalie:', 'if False:'),
    "S33_pointe_a_travers_les_remises": ("E30", 'e["pointe"], e["pointe_de"], e["pointe_a"] = rythme_pointe(caps, duree_min)',
                                         'e["pointe"], e["pointe_de"], e["pointe_a"] = rythme_pointe(sorted((l for i, l '
                                         'in passees if l["type"] == "capture"), key=lambda l: l["t"]), duree_min)'),
    "S34_trou_toujours_compte": ("E30", 'if en_cours else f"({avant})"', 'if True else f"({avant})"'),
    "S35_sans_borne_basse": ("E31", 'e["borne"] = float(der["valeur"]) + e["terme_rythme"]', 'pass'),
    "S36_borne_continuer": ("E31", '    elif e["jauge"] is not None:\n        e["verdict"] = "CONTINUER"',
                            '    elif e["jauge"] is not None or e["borne"] is not None:\n        e["verdict"] = "CONTINUER"'),
    "S37_duree_min_ignoree": ("E32", 'if heures(caps[j]["t"], b["t"]) >= duree_min', 'if True'),
    "S38_duree_min_negative": ("E7", '\n            or vus["duree_min_d_une_paire"] < 0)', ')'),
    # 25-11-2026 : dents des corrections du tour 6 (RELU de Cowork 12h55 R-1, C-3, R-2 ; RELU de 14h34 N-1 : les cinq
    # retours en arrière sab1 à sab4 de Cowork restaient verts)
    "S39_borne_jetons_retiree": ("E33", 'e["borne"] = float(der["valeur"]) + e["terme_jetons"]', 'pass'),
    "S40_motif_de_la_duree_muet": ("E33", 'if duree_min > 0 and rythme_pointe(caps, 0)[0] is not None:', 'if False:'),
    "S41_trou_sous_la_marge_sans_periode": ("E34", '"peut dépasser)" + (f" ; {avant}" if not en_cours else "")',
                                            '"peut dépasser)"'),
    "S42_trou_promet_la_pointe_inconnue": ("E34", 'if e["terme_rythme"] is not None else', 'if True else'),
    "S43_trou_promet_sur_la_pointe_seule": ("E34", 'if e["terme_rythme"] is not None else',
                                            'if e["pointe"] is not None else'),
}


def lancer(prog, dossier, *args):
    r = subprocess.run([sys.executable, "-I", prog, "--journal", os.path.join(dossier, "j.csv"),
                        "--reglages", os.path.join(dossier, "r.csv"), *args],
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr


def preparer(prog, dossier, lignes, seuil=95, marge=10, age=2, paire=0):
    """lignes : liste d'arguments (sans --journal) ; échoue si un ajout est refusé."""
    for f in ("j.csv", "r.csv"):
        if os.path.exists(os.path.join(dossier, f)):
            os.remove(os.path.join(dossier, f))
    open(os.path.join(dossier, "r.csv"), "w", encoding="utf-8").write(REGL.format(s=seuil, m=marge, a=age, p=paire))
    for a in lignes:
        c, s = lancer(prog, dossier, *a)
        if c != 0:
            raise AssertionError(f"ajout refusé {a} : {s}")


BASE_E5 = [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T09:00"],
           ["--capture", "0", "--a", "2026-11-15T10:00"],
           ["--agent", "a1", "1000000", "--a", "2026-11-15T11:00"],
           ["--capture", "10", "--a", "2026-11-15T12:00"]]
M = ["--etat", "--maintenant", "2026-11-15T13:00"]


def epreuves(racine):
    prog = os.path.join(racine, "programmes", PROG)
    res = {}
    d = tempfile.mkdtemp(prefix="forfait_")
    try:
        def cas(nom, f):
            try:
                ok, info = f()
            except Exception as x:
                ok, info = False, f"{type(x).__name__} : {x}"
            res[nom] = (ok, info)

        def e1():
            preparer(prog, d, [])
            j = os.path.join(d, "j.csv")
            avant = b""
            for a in BASE_E5[:3]:
                lancer(prog, d, *a)
                apres = open(j, "rb").read()
                if not apres.startswith(avant) or len(apres) <= len(avant):
                    return False, f"le fichier d'avant n'est pas le début de celui d'après ({a})"
                avant = apres
            n = avant.decode().count("type,horodatage_paris")
            return n == 1 and avant.decode().count("\n") == 4, f"en-têtes {n}, lignes {avant.decode().count(chr(10))}"
        cas("E1", e1)

        def e2():
            out = []
            for lignes in ([["--remise", "2026-11-18T02:00", "--a", "2026-11-15T09:00"],
                            ["--capture", "10", "--a", "2026-11-15T10:00"],
                            ["--agent", "x", "500000", "--a", "2026-11-15T11:00"]],
                           [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T09:00"],
                            ["--capture", "0", "--a", "2026-11-15T10:00"],
                            ["--capture", "10", "--a", "2026-11-15T12:00"],
                            ["--agent", "x", "500000", "--a", "2026-11-15T12:30"]]):
                preparer(prog, d, lignes)
                c, s = lancer(prog, d, *M)
                out.append(c == 5 and "VERDICT : INCONNU" in s and "RAPPORT JETONS PAR POINT : INCONNU" in s
                           and "PROJECTION À LA REMISE : INCONNUE" in s
                           and not re.search(r"JAUGE PROJETÉE MAINTENANT : [0-9]", s))
            return all(out), str(out)
        cas("E2", e2)

        def bord(jetons, verdict, code):
            preparer(prog, d, BASE_E5 + [["--agent", "a2", str(jetons), "--a", "2026-11-15T12:30"]])
            c, s = lancer(prog, d, *M)
            return c == code and f"VERDICT : {verdict}" in s, f"code {c} ; " + s.strip().splitlines()[-1]
        cas("E3", lambda: bord(8500000, "ARRÊTER LES NOUVEAUX AGENTS", 4))
        cas("E4", lambda: bord(7500000, "ALERTER", 3))

        def e5():
            preparer(prog, d, BASE_E5 + [["--agent", "a2", "1000000", "--a", "2026-11-15T12:30"]])
            c, s = lancer(prog, d, *M)
            att = ["JAUGE PROJETÉE MAINTENANT : 20.0 %", "RYTHME RÉEL : 5.00 points/h", "RAPPORT JETONS PAR POINT : 100000",
                   "PROJECTION À LA REMISE : 325.0 %", "SEUIL ATTEINT VERS : 2026-11-16 04:00", "VERDICT : CONTINUER",
                   "prochaine remise 2026-11-18 02:00",
                   "SEUIL ATTEINT VERS : 2026-11-16 04:00 [au rythme réel des deux dernières captures ; le verdict, lui, "
                   "compte le rythme de pointe]"]
            manque = [a for a in att if a not in s]
            return c == 0 and not manque, f"code {c} ; manque {manque}"
        cas("E5", e5)

        def e6():
            lignes = BASE_E5 + [["--agent", "a2", "1000000", "--a", "2026-11-15T12:30"]]
            out = []
            for seuil, marge, age, v, code in ((25, 10, 2, "ALERTER", 3), (20, 10, 2, "ARRÊTER LES NOUVEAUX AGENTS", 4),
                                               (25, 4, 2, "CONTINUER", 0), (95, 10, 0.5, "INCONNU", 5)):
                preparer(prog, d, lignes, seuil, marge, age)
                c, s = lancer(prog, d, *M)
                out.append(c == code and f"VERDICT : {v}" in s)
            return all(out), str(out)
        cas("E6", e6)

        def e7():
            out = []
            for contenu in ("reglage,valeur,etat,qui_decide,raison\nmarge_d_alerte,10,x,x,x\n",
                            REGL.format(s=95, m=10, a=2, p=0) + "seuil_d_arret,90,x,x,x\n", REGL.format(s="nan", m=10, a=2, p=0),
                            REGL.format(s=95, m="nan", a=2, p=0), REGL.format(s=95, m="inf", a=2, p=0),
                            REGL.format(s=95, m=10, a="nan", p=0), REGL.format(s=95, m=10, a=2, p="nan"),
                            REGL.format(s=95, m=10, a=2, p=-1),
                            REGL.format(s=95, m=10, a=2, p=0).replace("duree_min_d_une_paire,0,x,x,x\n", ""),
                            None):
                preparer(prog, d, BASE_E5)
                r = os.path.join(d, "r.csv")
                if contenu is None:
                    os.remove(r)
                else:
                    open(r, "w", encoding="utf-8").write(contenu)
                c, s = lancer(prog, d, *M)
                out.append(c == 2 and "ERREUR RÉGLAGE" in s and "VERDICT" not in s)
            return all(out), str(out)
        cas("E7", e7)

        def e8():
            preparer(prog, d, [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T09:00"],
                               ["--capture", "96", "--a", "2026-11-15T10:00"]])
            c, s = lancer(prog, d, *M)
            return c == 4 and "ARRÊTER LES NOUVEAUX AGENTS (sur le plancher" in s, f"code {c}"
        cas("E8", e8)

        def e9():
            preparer(prog, d, [["--capture", "90", "--a", "2026-11-15T08:00"]] + BASE_E5)
            c, s = lancer(prog, d, *M)
            return (c == 0 and "JAUGE PROJETÉE MAINTENANT : 15.0 %" in s and "ANOMALIE" not in s
                    and "VERDICT : CONTINUER" in s), f"code {c}"
        cas("E9", e9)

        def e10():
            preparer(prog, d, BASE_E5 + [["--capture", "99", "--a", "2026-11-16T10:00"]])
            c, s = lancer(prog, d, *M)
            return (c == 0 and "VERDICT : CONTINUER" in s and "IGNORÉES : 1" in s), f"code {c}"
        cas("E10", e10)

        def e11():
            j, r = (os.path.join(racine, "donnees", x) for x in ("JOURNAL_DU_FORFAIT.csv", "REGLAGES_DU_FORFAIT.csv"))
            run = lambda m: subprocess.run([sys.executable, "-I", prog, "--journal", j, "--reglages", r, "--etat",
                                            "--maintenant", m], capture_output=True, text=True, timeout=60)
            a, b = run("2026-11-15T13:00"), run("2026-11-14T23:00")
            att = ["depuis la remise du 2026-11-15 12:14", "prochaine remise 2026-11-18 02:00", "dernière 0 %",
                   "seuil 95 %", "VERDICT : INCONNU"]
            manque = [x for x in att if x not in a.stdout]
            ok = (a.returncode == 5 and not manque and b.returncode == 4
                  and "plancher 100 %" in b.stdout and "ARRÊTER LES NOUVEAUX AGENTS" in b.stdout)
            # le journal tel qu'il était le 14-11 au soir : coupé aux cinq vraies captures (28 → 75 %)
            coupe = os.path.join(d, "coupe.csv")
            with open(j, encoding="utf-8", newline="") as f:
                open(coupe, "w", encoding="utf-8", newline="").write("".join(f.readlines()[:6]))
            codes = []
            for m in ("2026-11-14T13:30", "2026-11-14T19:00", "2026-11-14T22:44"):
                x = subprocess.run([sys.executable, "-I", prog, "--journal", coupe, "--reglages", r, "--etat",
                                    "--maintenant", m], capture_output=True, text=True, timeout=60)
                codes.append(x.returncode)
                ok = ok and (x.returncode == 5 and "VERDICT : INCONNU" in x.stdout and "demander une capture" in x.stdout
                             and "pas de nouvel agent avant une nouvelle capture" in x.stdout)
            # G-1 sur les vraies captures du 15-11 (0 % 12h14, 10 % 14h16, 17 % 15h27) : la marge ne couvre pas le trou
            g = run("2026-11-15T16:00")
            ok = ok and "au moins 8.5 points" in g.stdout and "NON COUVERT" not in g.stdout
            # le vrai relevé de Jean-Luc du 25-11-2026 (2 % à 11h55, après la remise du 25-11 à 02h00)
            v = run("2026-11-25T12:00")
            ok = ok and (v.returncode == 5 and "depuis la remise du 2026-11-25 02:00" in v.stdout
                         and "dernière 2 % le 2026-11-25 11:55" in v.stdout and "VERDICT : INCONNU" in v.stdout)
            return ok, f"codes {a.returncode}/{b.returncode}/{v.returncode}, coupé {codes} ; manque {manque}"
        cas("E11", e11)

        def e12():
            preparer(prog, d, BASE_E5)
            j = os.path.join(d, "j.csv")
            avant = open(j, "rb").read()
            out = []
            for a in (["--capture", "120", "--a", "2026-11-15T12:30"], ["--capture", "5"],
                      ["--agent", "x", "12k"], ["--capture", "5", "--a", "15/11/2026"]):
                c, s = lancer(prog, d, *a)
                out.append(c == 2 and open(j, "rb").read() == avant)
            return all(out), str(out)
        cas("E12", e12)

        def e13():
            preparer(prog, d, [["--capture", "50", "--a", "2026-11-15T10:00"],
                               ["--agent", "x", "1000", "--a", "2026-11-15T10:30"],
                               ["--capture", "40", "--a", "2026-11-15T11:00"]])
            c, s = lancer(prog, d, *M)
            return ("ANOMALIE" in s and "RYTHME RÉEL : INCONNU" in s and "RAPPORT JETONS PAR POINT : INCONNU" in s,
                    f"code {c}")
        cas("E13", e13)

        def e14():
            preparer(prog, d, [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T07:00"],
                               ["--capture", "70", "--a", "2026-11-15T08:00"],
                               ["--agent", "a", "2000000", "--a", "2026-11-15T09:00"],
                               ["--capture", "80", "--a", "2026-11-15T10:00"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T16:00")
            return (c == 5 and "VERDICT : INCONNU" in s and "capture vieille de 6.0 h" in s
                    and "demander une capture" in s and "VERDICT : CONTINUER" not in s), f"code {c}"
        cas("E14", e14)

        def e17():
            preparer(prog, d, BASE_E5)
            j = os.path.join(d, "j.csv")
            b = open(j, "rb").read().rstrip(b"\r\n")
            open(j, "wb").write(b)
            c, s = lancer(prog, d, "--capture", "97", "--a", "2026-11-15T12:40")
            return c == 2 and "ERREUR" in s and open(j, "rb").read() == b, f"code {c}"
        cas("E17", e17)

        def e18():
            preparer(prog, d, BASE_E5)
            j = os.path.join(d, "j.csv")
            b = open(j, "rb").read().rstrip(b"\r\n") + b"capture,2026-11-15T12:40,97,,x,,2026-11-15T12:40\r\n"
            open(j, "wb").write(b)
            c, s = lancer(prog, d, *M)
            return c == 2 and "ERREUR" in s and "VERDICT" not in s, f"code {c}"
        cas("E18", e18)

        def e20():
            src = open(prog, encoding="utf-8").read()
            a = ast.parse(src)
            docs = {id(n.body[0].value) for n in ast.walk(a)
                    if isinstance(n, (ast.Module, ast.FunctionDef)) and n.body and isinstance(n.body[0], ast.Expr)
                    and isinstance(n.body[0].value, ast.Constant)}
            nums = {n.value for n in ast.walk(a) if isinstance(n, ast.Constant) and id(n) not in docs
                    and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)}
            en_dur = sorted(x for x in nums if x in (95, 85, 10))
            return not en_dur, f"seuil ou marge en dur : {en_dur}"
        cas("E20", e20)

        def e21():
            out = []
            for ligne in ("agent,2026-11-15T12:30,12k,x,agent fini,,2026-11-15T12:30\r\n",
                          "capture,2026-11-15T12:40,,,x,,2026-11-15T12:40\r\n",
                          "agent,2026-11-15T12:30,\u00b2,x,agent fini,,2026-11-15T12:30\r\n"):
                preparer(prog, d, BASE_E5)
                open(os.path.join(d, "j.csv"), "a", encoding="utf-8", newline="").write(ligne)
                c, s = lancer(prog, d, *M)
                out.append(c == 2 and "ERREUR" in s and "Traceback" not in s)
            return all(out), str(out)
        cas("E21", e21)

        def e22():
            preparer(prog, d, [["--capture", "10", "--a", "2027-03-28T01:30"],
                               ["--capture", "20", "--a", "2027-03-28T03:30"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2027-03-28T03:45")
            return "RYTHME RÉEL : 10.00 points/h" in s, f"code {c}"
        cas("E22", e22)

        def e23():
            out = []
            j = os.path.join(d, "j.csv")
            # en-tête changé
            preparer(prog, d, BASE_E5)
            txt = open(j, encoding="utf-8", newline="").read().replace("inscrit_le_paris", "inscrit_le", 1)
            open(j, "w", encoding="utf-8", newline="").write(txt)
            out.append(lancer(prog, d, *M)[0] == 2)
            # type inconnu
            preparer(prog, d, BASE_E5)
            open(j, "a", encoding="utf-8", newline="").write("bidule,2026-11-15T12:40,1,,x,,2026-11-15T12:40\r\n")
            c, s = lancer(prog, d, *M)
            out.append(c == 2 and "type inconnu" in s)
            # seuil hors bornes
            preparer(prog, d, BASE_E5, seuil=120)
            out.append(lancer(prog, d, *M)[0] == 2)
            # remise suivante avant la remise, puis virgule dans l'étiquette : refusées, journal inchangé
            preparer(prog, d, BASE_E5)
            avant = open(j, "rb").read()
            for a in (["--remise", "2026-11-15T08:00", "--a", "2026-11-15T09:00"], ["--agent", "a,b", "10"]):
                c, s = lancer(prog, d, *a)
                out.append(c == 2 and open(j, "rb").read() == avant)
            return all(out), str(out)
        cas("E23", e23)

        def e24():
            # G-3 SY1 de Cowork : une capture hors de 0-100 écrite à la main est refusée à la lecture
            preparer(prog, d, BASE_E5)
            open(os.path.join(d, "j.csv"), "a", encoding="utf-8", newline="").write(
                "capture,2026-11-15T12:40,120,,x,,2026-11-15T12:40\r\n")
            c, s = lancer(prog, d, *M)
            return c == 2 and "ERREUR" in s and "VERDICT" not in s, f"code {c}"
        cas("E24", e24)

        def e25():
            # G-3 SY2 de Cowork : l'âge de la capture se compte en heures réelles ; 01h30 → 03h50 le 28-03-2027 = 1 h 20
            preparer(prog, d, [["--capture", "10", "--a", "2027-03-28T01:30"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2027-03-28T03:50")
            return "vieille de 1.3 h" in s and "capture vieille" not in s, f"code {c}"
        cas("E25", e25)

        def e26():
            # G-3 SY4 de Cowork : un ajout relit l'en-tête du journal et refuse un journal à l'en-tête étranger
            preparer(prog, d, [])
            j = os.path.join(d, "j.csv")
            open(j, "w", encoding="utf-8", newline="").write("type;horodatage\r\n")
            avant = open(j, "rb").read()
            c, s = lancer(prog, d, "--capture", "5", "--a", "2026-11-15T12:40")
            return c == 2 and "ERREUR" in s and open(j, "rb").read() == avant, f"code {c}"
        cas("E26", e26)

        def e27():
            # G-1 de Cowork : le programme confronte lui-même « âge maximal × consommation mesurée » à la marge
            out = []
            # (a) 0 % à 12h14, 10 % à 14h16, 17 % à 15h27 (les vraies captures du 15-11) : 17 points en 3,22 h ;
            #     3,217 h = plafond(3,217 ÷ 2) = 2 fenêtres de 2 h : 17 ÷ 2 = 8,5 < marge 10 (G-5 : plus 10,6)
            preparer(prog, d, [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T12:14"],
                               ["--capture", "0", "--a", "2026-11-15T12:14"],
                               ["--capture", "10", "--a", "2026-11-15T14:16"],
                               ["--capture", "17", "--a", "2026-11-15T15:27"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T16:00")
            out.append("au moins 8.5 points" in s and "NON COUVERT" not in s)
            # (b) paire courte : 0 % à 10h00, 6 % à 10h30 : 6 points tombés en 0,5 h, jamais extrapolés à 24 → couvert
            preparer(prog, d, [["--capture", "0", "--a", "2026-11-15T10:00"],
                               ["--capture", "6", "--a", "2026-11-15T10:30"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T10:45")
            out.append("au moins 6.0 points" in s and "NON COUVERT" not in s)
            # (c) une remise entre deux captures : la paire ne compte pas → trou INCONNU
            preparer(prog, d, [["--capture", "0", "--a", "2026-11-15T07:00"],
                               ["--remise", "2026-11-18T02:00", "--a", "2026-11-15T07:30"],
                               ["--capture", "9", "--a", "2026-11-15T08:30"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T09:00")
            out.append("TROU POSSIBLE PENDANT L'ÂGE MAXIMAL : INCONNU" in s)
            return all(out), str(out)
        cas("E27", e27)

        def e28():
            # G-4 de Cowork : sous une ANOMALIE, le plancher est la plus haute capture (la jauge ne baisse pas sans remise)
            preparer(prog, d, [["--capture", "96", "--a", "2026-11-15T08:00"],
                               ["--capture", "9.6", "--a", "2026-11-15T09:00"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T09:30")
            ok = c == 4 and "ARRÊTER LES NOUVEAUX AGENTS" in s and "plancher 96 %" in s
            # G-6 : puis 97 % ; la période est en ANOMALIE, la ligne TROU ne part pas de 9,6 %
            preparer(prog, d, [["--capture", "96", "--a", "2026-11-15T08:00"],
                               ["--capture", "9.6", "--a", "2026-11-15T09:00"],
                               ["--capture", "97", "--a", "2026-11-15T09:30"]])
            c2, s2 = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T09:45")
            ok = ok and c2 == 4 and "TROU POSSIBLE PENDANT L'ÂGE MAXIMAL : INCONNU" in s2
            return ok, f"codes {c}/{c2}"
        cas("E28", e28)

        def e29():
            # A-827 (Jean-Luc, 15-11-2026 16h41 ; superviseur R-759 16h42) : la jauge est projetée à l'instant présent.
            # Captures 60 % (06h00), 72 % (08h00), 80 % (10h00) : rythmes 6 puis 4 points/h, pointe 6, moyenne 5,
            # dernière paire 4 ; 1 200 000 jetons entre la première et la dernière → rapport 60 000 jetons par point.
            base = [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T05:00"],
                    ["--capture", "60", "--a", "2026-11-15T06:00"],
                    ["--capture", "72", "--a", "2026-11-15T08:00"],
                    ["--agent", "a", "1200000", "--a", "2026-11-15T09:00"],
                    ["--capture", "80", "--a", "2026-11-15T10:00"]]
            out = []
            preparer(prog, d, base)
            # (a) 10h30 : 80 + 6 × 0,5 = 83,0 → CONTINUER
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T10:30")
            out.append(c == 0 and "JAUGE PROJETÉE MAINTENANT : 83.0 %" in s and "VERDICT : CONTINUER" in s
                       and "RYTHME DE POINTE : 6.00 points/h" in s)
            # (b) 11h55 : 80 + 6 × 1,9167 = 91,5 → ALERTER (le programme d'avant rendait CONTINUER)
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T11:55")
            out.append(c == 3 and "JAUGE PROJETÉE MAINTENANT : 91.5 %" in s and "VERDICT : ALERTER" in s)
            # (c) 10h55 : pointe 80 + 6 × 0,9167 = 85,5 → ALERTER ; au rythme moyen (5) 84,6 et au dernier (4) 83,7
            #     le verdict serait CONTINUER
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T10:55")
            out.append(c == 3 and "JAUGE PROJETÉE MAINTENANT : 85.5 %" in s)
            # (d) le plus grand des deux termes, pas leur somme : 600 000 jetons à 10h10 → 10 points ; à 10h30,
            #     rythme × âge = 3 points → 80 + 10 = 90,0 (la somme donnerait 93,0)
            preparer(prog, d, base + [["--agent", "b", "600000", "--a", "2026-11-15T10:10"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T10:30")
            out.append(c == 3 and "JAUGE PROJETÉE MAINTENANT : 90.0 %" in s)
            # (e) rythme de pointe inconnu (aucune paire consécutive qui monte avec du temps écoulé) alors que le
            #     rapport est connu : jauge INCONNUE, jamais CONTINUER
            preparer(prog, d, [["--capture", "50", "--a", "2026-11-15T08:00"],
                               ["--agent", "a", "1000000", "--a", "2026-11-15T09:00"],
                               ["--capture", "50", "--a", "2026-11-15T10:00"],
                               ["--capture", "60", "--a", "2026-11-15T10:00"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T10:30")
            out.append(c == 5 and "RYTHME DE POINTE : INCONNU" in s and "VERDICT : INCONNU" in s)
            return all(out), str(out)
        cas("E29", e29)

        def e30():
            # P-2 de Cowork : le trou d'une semaine passée n'est pas compté par le verdict, et la ligne le dit
            preparer(prog, d, [["--capture", "10", "--a", "2026-11-13T10:00"],
                               ["--capture", "25", "--a", "2026-11-13T11:00"],
                               ["--remise", "2026-11-25T02:00", "--a", "2026-11-18T02:00"],
                               ["--capture", "70", "--a", "2026-11-20T08:00"],
                               ["--agent", "a", "400000", "--a", "2026-11-20T09:00"],
                               ["--capture", "74", "--a", "2026-11-20T10:00"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-20T11:55")
            ok = (c == 0 and "RYTHME DE POINTE : 2.00 points/h" in s and "au moins 15.0 points" in s
                  and "NON COUVERT" in s and "mesuré AVANT la dernière remise" in s
                  and "le verdict compte déjà" not in s)
            return ok, f"code {c}"
        cas("E30", e30)

        def e31():
            # K-1 de Cowork : sans agent inscrit, la borne basse « dernière capture + rythme de pointe × âge » agit
            out = []
            for v3, att in (("88", "AU MOINS 103.3 %"), ("84", "AU MOINS 95.5 %")):
                preparer(prog, d, [["--remise", "2026-11-18T02:00", "--a", "2026-11-15T05:00"],
                                   ["--capture", "60", "--a", "2026-11-15T06:00"],
                                   ["--capture", "72", "--a", "2026-11-15T08:00"],
                                   ["--capture", v3, "--a", "2026-11-15T10:00"]])
                c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T11:55")
                out.append(c == 4 and att in s and "VERDICT : ARRÊTER LES NOUVEAUX AGENTS (sur la borne basse" in s
                           and (v3 != "88" or "au-delà de 100" in s))
            # la borne basse ne rend jamais CONTINUER : 10 % puis 20 %, rapport inconnu → INCONNU
            preparer(prog, d, [["--capture", "10", "--a", "2026-11-15T08:00"],
                               ["--capture", "20", "--a", "2026-11-15T10:00"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-15T10:30")
            out.append(c == 5 and "AU MOINS 22.5 %" in s and "VERDICT : INCONNU" in s)
            return all(out), str(out)
        cas("E31", e31)

        def e32():
            # P-1 et K-2 de Cowork : la durée minimale d'une paire vient du réglage
            lignes = [["--remise", "2026-11-25T02:00", "--a", "2026-11-18T02:00"],
                      ["--capture", "40", "--a", "2026-11-18T06:00"],
                      ["--agent", "a", "600000", "--a", "2026-11-18T08:00"],
                      ["--capture", "50", "--a", "2026-11-18T10:00"],
                      ["--capture", "51", "--a", "2026-11-18T10:01"]]
            out = []
            preparer(prog, d, lignes)
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-18T10:40")
            out.append(c == 3 and "RYTHME DE POINTE : 60.00 points/h" in s)
            preparer(prog, d, lignes, paire=0.5)
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-18T10:40")
            out.append(c == 0 and "RYTHME DE POINTE : 2.74 points/h (de 40 % le 2026-11-18 06:00 à 51 %" in s
                       and "VERDICT : CONTINUER" in s)
            return all(out), str(out)
        cas("E32", e32)

        def e33():
            # R-1 de Cowork (25-11-2026) : rapport connu, pointe écartée par la durée minimale → la borne basse prend
            # les jetons inscrits ÷ rapport ; 70 % 10h00, 100 000 jetons, 75 % 10h10 (rapport 20 000), 240 000
            # jetons à 10h40 → au moins 75 + 12 = 87 % à 11h00
            lignes = [["--remise", "2026-11-25T02:00", "--a", "2026-11-18T02:00"],
                      ["--capture", "70", "--a", "2026-11-18T10:00"],
                      ["--agent", "a", "100000", "--a", "2026-11-18T10:05"],
                      ["--capture", "75", "--a", "2026-11-18T10:10"],
                      ["--agent", "b", "240000", "--a", "2026-11-18T10:40"]]
            out = []
            preparer(prog, d, lignes)
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-18T11:00")
            out.append(c == 4 and "JAUGE PROJETÉE MAINTENANT : 100.0 %" in s)
            preparer(prog, d, lignes, paire=0.5)
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-18T11:00")
            out.append(c == 3 and "AU MOINS 87.0 %" in s and "jetons inscrits ÷ rapport = 12.0 points" in s
                       and "VERDICT : ALERTER (sur la borne basse : dernière capture + jetons inscrits ÷ rapport)" in s
                       and "elle dure moins de 0.5 h" in s)
            # la borne des jetons ne rend jamais CONTINUER : 20 000 jetons → 76 % → INCONNU
            preparer(prog, d, lignes[:-1] + [["--agent", "b", "20000", "--a", "2026-11-18T10:40"]], paire=0.5)
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-18T11:00")
            out.append(c == 5 and "AU MOINS 76.0 %" in s and "VERDICT : INCONNU" in s)
            return all(out), str(out)
        cas("E33", e33)

        def e34():
            # C-3 de Cowork : paire d'une période passée, sous la marge → la ligne TROU dit la période
            out = []
            preparer(prog, d, [["--capture", "0", "--a", "2026-11-15T12:14"],
                               ["--capture", "17", "--a", "2026-11-15T15:27"],
                               ["--remise", "2026-12-02T02:00", "--a", "2026-11-25T02:00"],
                               ["--capture", "2", "--a", "2026-11-25T11:55"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-25T12:50")
            out.append(c == 5 and "au moins 8.5 points" in s and "sous la marge" in s
                       and "mesuré AVANT la dernière remise" in s)
            # R-2 de Cowork : deux captures de la même minute → pointe INCONNUE ; la ligne TROU ne promet pas que
            # le verdict compte rythme de pointe × âge
            preparer(prog, d, [["--capture", "50", "--a", "2026-11-25T10:00"],
                               ["--capture", "62", "--a", "2026-11-25T10:00"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-25T10:30")
            out.append(c == 5 and "RYTHME DE POINTE : INCONNU" in s and "NON COUVERT" in s
                       and "le verdict compte déjà" not in s and "le verdict ne compte donc pas ce trou" in s)
            # capture trop vieille (au-delà de l'âge maximal) : la pointe est connue, mais le verdict se prend sur le
            # plancher et ne compte pas rythme × âge ; la ligne TROU ne doit pas dire le contraire
            preparer(prog, d, [["--capture", "50", "--a", "2026-11-25T08:00"],
                               ["--capture", "62", "--a", "2026-11-25T08:30"]])
            c, s = lancer(prog, d, "--etat", "--maintenant", "2026-11-25T11:00")
            out.append(c == 5 and "RYTHME DE POINTE : 24.00 points/h" in s and "NON COUVERT" in s
                       and "le verdict compte déjà" not in s and "le verdict ne compte pas ce trou — capture vieille" in s)
            return all(out), str(out)
        cas("E34", e34)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return res


def afficher(res):
    for k, (ok, info) in res.items():
        print(f"  {'ok   ' if ok else 'ROUGE'} {k} — {info}")
    return all(ok for ok, _ in res.values())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    racine = os.path.abspath(sys.argv[1])
    res = epreuves(racine)
    vert = afficher(res)
    print(f"ÉPREUVES : {sum(ok for ok, _ in res.values())} vertes sur {len(res)}")
    if not vert:
        print("VERDICT : ROUGE")
        return 1
    if "--saboter" not in sys.argv:
        print("VERDICT : TOUT PASSE")
        return 0
    source = open(os.path.join(racine, "programmes", PROG), encoding="utf-8").read()
    k, n = 1, 1
    if "--lot" in sys.argv:
        k, n = (int(x) for x in sys.argv[sys.argv.index("--lot") + 1].split("/"))
        if not 1 <= k <= n:
            print(f"ERREUR : lot {k}/{n} impossible")
            return 1
    choisis = {nom: v for r, (nom, v) in enumerate(SABOTAGES.items(), start=1) if (r - k) % n == 0}
    mordent = 0
    for nom, (cible, vieux, neuf) in choisis.items():
        if source.count(vieux) != 1:
            print(f"{nom} TEXTE INTROUVABLE ou multiple ({source.count(vieux)}) — sabotage non joué")
            continue
        c = tempfile.mkdtemp(prefix="sabot_forfait_")
        try:
            os.makedirs(os.path.join(c, "programmes"))
            os.makedirs(os.path.join(c, "donnees"))
            open(os.path.join(c, "programmes", PROG), "w", encoding="utf-8").write(source.replace(vieux, neuf))
            for f in ("JOURNAL_DU_FORFAIT.csv", "REGLAGES_DU_FORFAIT.csv"):
                shutil.copy(os.path.join(racine, "donnees", f), os.path.join(c, "donnees", f))
            r = epreuves(c)
            rouges = [k for k, (ok, _) in r.items() if not ok]
            if cible in rouges:
                mordent += 1
                print(f"{nom} MORD — rouges : {', '.join(rouges)}")
            else:
                print(f"{nom} NE MORD PAS — {cible} reste verte ; rouges : {rouges}")
        finally:
            shutil.rmtree(c, ignore_errors=True)
    lot = f" (lot {k}/{n} ; {len(SABOTAGES)} en tout)" if n > 1 else ""
    print(f"sabotages qui mordent : {mordent} sur {len(choisis)}{lot}")
    print("VERDICT : TOUT PASSE" if mordent == len(choisis) else "VERDICT : ROUGE")
    return 0 if mordent == len(choisis) else 1


if __name__ == "__main__":
    sys.exit(main())
