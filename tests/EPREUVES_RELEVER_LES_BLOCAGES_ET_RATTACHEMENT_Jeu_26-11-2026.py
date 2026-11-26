#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_RELEVER_LES_BLOCAGES_ET_RATTACHEMENT — Jeu 26-11-2026 (Paris)
Rôle : prouver que programmes/RELEVER_LES_BLOCAGES.py et programmes/VERIFIER_LE_RATTACHEMENT.py rendent les codes
que leur fiche annonce, et que l'épreuve a des dents (R-731, R-755 ②). Simulation uniquement : aucun ordre réel.
Quand l'appeler : avant toute livraison qui touche l'un de ces deux programmes.

À QUOI ÇA SERT. Ces deux programmes sont des contrôles de confiance (A-1011 : un blocage écrit est relevé ; A-1014 :
un travail sert une décision). Un contrôle qui rend 0 quoi qu'il arrive ne contrôle rien. L'épreuve lance chaque
programme, par sous-processus, sur des COPIES posées dans un dossier temporaire : jamais sur le dépôt.

LES CAS (chacun dit le code attendu et un mot attendu dans la sortie) :
  R1  vraie ligne A-1055 du BACKLOG (R-732), rapport du « Pilote V8 » qui écrit « BLOCAGE ⑥ » → code 3
  R2  un rapport du pilote sans le mot → code 0, « AUCUN BLOCAGE »
  R3  aucun rapport du pilote → code 2, « AUCUN RAPPORT DU PILOTE »
  R4  N = 1 : un blocage dans l'avant-dernier rapport seulement → code 0 (seuls les N derniers sont lus)
  R5  le mot écrit par le Chat (colonne responsable « Chat ») n'est pas relevé → code 0
  V1  vraie ligne A-1014 du BACKLOG (R-732, statut DÉCIDÉ), note « SERT : A-1014 » → code 0, « RATTACHÉ »
  V2  note sans ligne « SERT : A-… » → code 3, « NON RATTACHÉ »
  V3  note qui sert une action absente du BACKLOG → code 3
  V4  note qui sert une action non décidée (À FAIRE) → code 3
  V5  aucune paire ÉTIQUETTE=CHEMIN → code 2, « USAGE »
  Ajoutés au tour 2 (N-112, RELU Cowork 15h21 ; jugement du superviseur R-759 « DE FOND sous conditions ») :
  C1  rapport du pilote, phrase SYNTHÉTIQUE où un blocage est en cours, écrit « blocage » en minuscules → code 3
      (la fiche ⑥ promet « majuscules ou non » ; jamais la vraie ligne A-1024 « Aucun blocage nouveau », qui
      n'est pas un blocage en cours)
  C2a quatre rapports du pilote, blocage dans le plus ancien seulement, N non donné → code 0 (défaut N = 3)
  C2b trois rapports du pilote, blocage dans le plus ancien, N non donné → code 3 (le défaut lit bien 3 rapports)
  C3  « déblocage » seul dans un rapport du pilote → code 0 (mot entier exigé, fiche ⑥)
  C4  note à deux lignes SERT, « SERT : A-1014 » puis « SERT : A-99999 » (absente du BACKLOG) → code 3 (toutes les
      lignes SERT sont lues, ⑥ d'en-tête de VERIFIER). Ce cas remplace l'idée « SERT en ligne 3 », qui aurait figé
      le défaut consigné ⑨-③ (« une ligne SERT placée n'importe où compte »).
  NON FIGÉ, laissé au ⑨ de `index_du_backlog` : l'identifiant en double (seule la première ligne compte).
  Ajoutés au tour 3 (RELU Cowork 15h40, N-118 à N-121 ; superviseur R-759 neuf « RUSTINE, À REPRENDRE » : passe
  systématique, une propriété à la fois, et non plus cas par cas) :
  C5  « blocages » (pluriel) seul dans un rapport du pilote → code 3 (N-118)
  C6  deux mentions dans un même rapport → code 3, bilan « 2 MENTION(S) … (A-90030) » (chaque occurrence est comptée)
  E1  l'extrait : un mot à plus de 20 caractères AVANT « blocage » et un autre APRÈS, tous deux à moins de 150, doivent
      paraître ; deux mots à plus de 150 caractères ne doivent PAS paraître (N-120, condition 3 du superviseur)
  F1  une ligne « | B-90050 | » et une ligne « | A-X51 | », rapports du pilote avec « BLOCAGE », hors du filtre → code 0
  P1  le mot « Pilote » dans le TEXTE d'une ligne dont le responsable est le Chat → code 0 (seule la 4e case compte)
  I1  le BACKLOG lu sur l'entrée standard (« - ») → code 3
  A0  aucun argument → code 2, « USAGE » · A4  quatre éléments → code 2, « USAGE »
  L1  N illisible (« trois ») → code 2, « LECTURE IMPOSSIBLE » · L2  fichier absent → code 2, « LECTURE IMPOSSIBLE »
  T1  note « SERT : A-90006 », action au statut TRANCHÉ → code 0 (N-119)
  D1  note « SERT : A-90007 », action au statut DÉCIDÉ et sans le mot TRANCHÉ → code 0 (N-119 ; la vraie ligne
      A-1014 de V1 porte AUSSI le mot TRANCHÉ dans son texte : le sabotage Z9 « TRANCHÉ seul » n'y mordait pas)
  W1  « SERT » précédé de blancs → code 0 · W2  « SERT:A-1014 » sans blancs → code 0
  W3  « SERT : A-1014 » au milieu d'une ligne de texte → code 3 (le motif exige le début de ligne)
  N1  note illisible → code 3, « note illisible », comptée au bilan · B1  BACKLOG illisible → code 2
  Q1  paire sans « = » → code 2, « USAGE » · Q2  CHEMIN qui contient lui-même un « = » → code 0
  M1  deux notes, la mauvaise d'abord · M2  deux notes, la mauvaise ensuite → code 3, une ligne par note et le bilan
      « 1 NOTE(S) NON RATTACHÉE(S) SUR 2 » (le quatorzième point du superviseur, joué sur un vrai cas)
  V6  une ligne de texte AVANT le tableau cite « | A-90004 | … DÉCIDÉ » : l'index ne prend que les lignes qui COMMENCENT
      par « | A-<n> | », l'action reste non décidée → code 3

INVENTAIRE PAR PROPRIÉTÉ (condition 1 du superviseur R-759 du tour 3). Une ligne par promesse des éléments ③ ④ ⑤ ⑥
des fiches des deux programmes (en-tête et fonctions) : chaque élément de motif, chaque valeur par défaut, chaque code de
sortie, chaque format de sortie, chaque forme d'entrée. Troisième case : soit la liste « sabotage→cas » (le sabotage
retire la propriété dans la copie, le cas nommé doit rougir), soit « NON GARDÉ : raison ». Cet inventaire est LU par
l'épreuve (`controler_l_inventaire`) : un sabotage absent de la table, un cas qui ne correspond pas à celui du sabotage,
ou un sabotage de la table qu'aucune propriété ne nomme, et l'épreuve rend 1. Les sabotages Z1 à Z14 sont ceux du
superviseur (script de session sup.py), repris à l'identique ; Z4b est Z4 rejoué sur le fichier absent.
  RELEVER_LES_BLOCAGES.py
  P-R01 ¦ le mot « blocage » est cherché (motif MOT ; ⑥ en-tête et `main`) ¦ S1_mot_jamais_trouve→R1
  P-R02 ¦ majuscules ou non (re.I) ¦ X1_sans_re_I_motif_en_capitales→C1, X1b_sans_re_I_motif_en_minuscules→R1
  P-R03 ¦ mot entier (\\b) : « déblocage » ne compte pas ¦ X4_sans_mot_entier→C3
  P-R04 ¦ « blocage » ou « blocages » (s?) ¦ Z1_pluriel→C5
  P-R05 ¦ chaque occurrence est affichée et comptée (finditer) ¦ Z5_premiere_occurrence→C6
  P-R06 ¦ extrait de 150 caractères de part et d'autre du mot ¦ Z6_extrait_vide→E1, E1_extrait_10→E1, E2_sans_avant→E1, E3_sans_apres→E1, E4_sans_borne_avant→E1, E5_sans_borne_apres→E1, E6_sans_plancher_0→C1
  P-R07 ¦ format « BLOCAGE <identifiant> : …extrait… », identifiant = 2e case sans ses blancs ¦ B1_format_sans_BLOCAGE→R1, I2_mauvais_identifiant→R1, I3_cases_sans_strip→R1
  P-R08 ¦ seules les lignes qui commencent par « | A-<nombre> | » sont lues ¦ Z7_sans_filtre_A→F1, F2_filtre_sans_A→F1, F3_filtre_sans_chiffres→F1
  P-R09 ¦ « ^ » du filtre de `rapports_du_pilote` ¦ NON GARDÉ : `re.match` ancre déjà en tête, retirer « ^ » ne change rien d'observable
  P-R10 ¦ un rapport du pilote : la case de rang 4 (responsable) contient « Pilote » ¦ S5_tout_responsable→R5, P1_pilote_partout→P1, P2_mauvaise_colonne→R1
  P-R11 ¦ « Pilote » cherché comme sous-chaîne (« Copilote » serait pris) ¦ NON GARDÉ : défaut consigné au ⑨ de `rapports_du_pilote`, à ne pas figer
  P-R12 ¦ un « | » dans le texte décale les cases ; une ligne mal formée est ignorée sans le dire ¦ NON GARDÉ : défauts consignés au ⑨ de `rapports_du_pilote`, à ne pas figer
  P-R13 ¦ rapports gardés dans l'ordre du fichier, seuls les N derniers lus ¦ S4_tous_les_rapports→R4, O1_ordre_inverse→R4
  P-R14 ¦ N lu sur la ligne de commande ¦ N1_argument_ignore→R4
  P-R15 ¦ N vaut 3 par défaut ¦ X3a_N_defaut_4→C2a, X3b_N_defaut_2→C2b
  P-R16 ¦ N = 0 lit tout, N négatif retire les premiers ¦ NON GARDÉ : défaut consigné au ⑨ de `main`, à ne pas figer
  P-R17 ¦ « - » = entrée standard ¦ Z2_stdin_jamais→I1
  P-R18 ¦ fichier lu en UTF-8 ¦ U1_relever_ascii→R1
  P-R19 ¦ deux ou trois éléments dans argv, sinon USAGE et code 2 ¦ Z3_usage_relever→A0, A1_un_argument_admis→A0, A2_quatre_admis→A4
  P-R20 ¦ N illisible → « LECTURE IMPOSSIBLE », code 2 ¦ Z4_N_illisible_0→L1
  P-R21 ¦ fichier absent → « LECTURE IMPOSSIBLE », code 2 ¦ Z4b_fichier_absent_0→L2
  P-R22 ¦ aucun rapport du pilote → « AUCUN RAPPORT DU PILOTE TROUVÉ », code 2 ¦ S3_sans_rapport_passe→R3
  P-R23 ¦ au moins une mention → code 3 ¦ S2_blocage_rend_0→R1
  P-R24 ¦ aucune mention → code 0 ¦ O2_sans_mention_rend_3→R2
  P-R25 ¦ bilan « <n> MENTION(S) DE BLOCAGE dans les <k> derniers rapports du pilote (<identifiants>) » ¦ B2_bilan_sans_mot→C6
  P-R26 ¦ bilan « AUCUN BLOCAGE dans les <k> derniers rapports du pilote (<identifiants>) », k = rapports lus ¦ B3_noms_vides→R2, B4_K_vaut_N→R2
  P-R27 ¦ le mot compté même quand le blocage est levé ou absent ¦ NON GARDÉ : défaut consigné au ⑨ de l'en-tête et de `main`, à ne pas figer
  P-R28 ¦ les lignes sont prises sans leur fin de ligne (découpe sur « \\n ») ¦ NON GARDÉ : aucune différence observable sur un fichier à fins de ligne « \\n » ; un « \\r » final resterait dans la dernière case, que le relevé ne lit pas
  VERIFIER_LE_RATTACHEMENT.py
  P-V01 ¦ « SERT » cherché en début de ligne (« ^ » avec re.M), sur chaque ligne ¦ X2_sans_re_M→C4, W3_sans_ancre→W3
  P-V02 ¦ blancs admis avant « SERT » (^\\s*) ¦ Z14_sans_blancs_tete→W1
  P-V03 ¦ blancs facultatifs autour des deux-points (\\s*:\\s*) ¦ W2_deux_points_espaces→W2
  P-V04 ¦ l'action relevée est « A- » suivi de TOUS ses chiffres ¦ W4_un_seul_chiffre→V1
  P-V05 ¦ toutes les lignes SERT de la note sont lues (findall) ¦ W5_premiere_ligne_seule→C4
  P-V06 ¦ seule la première action d'une ligne « SERT : A-…, A-… » est vérifiée ¦ NON GARDÉ : défaut consigné au ⑨-① de `main`, à ne pas figer
  P-V07 ¦ une ligne SERT placée n'importe où dans la note compte ¦ NON GARDÉ : défaut consigné au ⑨-③ de `main`, à ne pas figer
  P-V08 ¦ DÉCIDÉ vaut décision ¦ Z9_tranche_seul→D1, S6_aucune_decision→V1
  P-V09 ¦ TRANCHÉ vaut décision ¦ Z8_decide_seul→T1
  P-V10 ¦ DÉCIDÉ ou TRANCHÉ cherché dans toute la ligne (« NON TRANCHÉ » suffit) ; FAIT n'est pas une décision ¦ NON GARDÉ : défauts consignés au ⑨-② de `main` et au ⑨ d'en-tête, à ne pas figer
  P-V11 ¦ action absente du BACKLOG → non rattachée ¦ S8_absente_passe→V3
  P-V12 ¦ action non décidée → non rattachée ¦ S9_non_decidee_passe→V4
  P-V13 ¦ note sans ligne SERT → non rattachée ¦ S7_note_sans_sert_passe→V2
  P-V14 ¦ index : seules les lignes qui COMMENCENT par « | A-<n> | » ¦ V7_index_hors_tete→V6
  P-V15 ¦ index : identifiant en double, seule la première ligne ; identifiant mal espacé ignoré ¦ NON GARDÉ : défauts consignés au ⑨ de `index_du_backlog`, à ne pas figer
  P-V16 ¦ index : « \\d+ » de l'identifiant ¦ NON GARDÉ : inobservable, le motif SERT ne relève que des « A-<chiffres> », jamais un identifiant sans chiffres
  P-V17 ¦ au moins trois éléments dans argv, sinon USAGE et code 2 ¦ S11_sans_paire_accepte→V5
  P-V18 ¦ un « = » dans chaque paire, sinon USAGE et code 2 ¦ Z10_egal_absent→Q1
  P-V19 ¦ CHEMIN = tout ce qui suit le premier « = » ¦ Q3_coupe_a_chaque_egal→Q2
  P-V20 ¦ BACKLOG lu en UTF-8 ¦ U2_backlog_ascii→V1
  P-V21 ¦ note lue en UTF-8 ¦ U3_note_ascii→V1
  P-V22 ¦ BACKLOG illisible → « LECTURE IMPOSSIBLE DU BACKLOG », code 2 ¦ Z11_backlog_illisible_0→B1
  P-V23 ¦ note illisible → « NON RATTACHÉ … note illisible », comptée parmi les mauvaises ¦ Z12_note_illisible_passe→N1
  P-V24 ¦ plusieurs notes : chacune lue, une ligne chacune, code 3 dès qu'une seule est mauvaise ¦ Z13_derniere_note_seule→M1, M1b_premiere_paire_seule→M2
  P-V25 ¦ bilan « <x> NOTE(S) NON RATTACHÉE(S) SUR <y> », y = nombre de paires ¦ M3_bilan_sur_1→M1
  P-V26 ¦ au moins une note non rattachée → code 3 ¦ S10_non_rattache_rend_0→V2
  P-V27 ¦ toutes rattachées → code 0 ¦ Y1_toujours_3→V1
  P-V28 ¦ formats « RATTACHÉ <étiquette> : sert <actions> » et « NON RATTACHÉ <étiquette> : … » ¦ Y2_format_rattache→V1
LES SABOTAGES (chacun retire, dans la COPIE, ce qu'un cas teste ; le cas nommé doit rougir) : voir SABOTAGES.

USAGE : python3 tests/EPREUVES_RELEVER_LES_BLOCAGES_ET_RATTACHEMENT_Jeu_26-11-2026.py <racine du dépôt>
        [--saboter | --saboter=S1,S2,…]
CODE : 0 tout vert (et, avec --saboter, chaque sabotage mord) · 1 un cas faux ou un sabotage non vu ·
       2 un contrôle n'a pas pu tourner (vraie ligne introuvable, programme absent, délai dépassé — R-734).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

RELEVER = "programmes/RELEVER_LES_BLOCAGES.py"
VERIFIER = "programmes/VERIFIER_LE_RATTACHEMENT.py"
BACKLOG = "BACKLOG_DECISIONS.md"
DELAI = 30  # secondes par lancement ; chaque lancement dure moins d'une seconde

# Chaque sabotage : (programme, texte exact à remplacer, remplaçant, cas qui doit rougir).
SABOTAGES = {
    "S1_mot_jamais_trouve": (RELEVER, 'MOT = re.compile(r"\\bblocages?\\b", re.I)',
                             'MOT = re.compile(r"\\bJAMAIS_ECRIT\\b", re.I)', "R1"),
    "S2_blocage_rend_0": (RELEVER, "        return 3\n", "        return 0\n", "R1"),
    "S3_sans_rapport_passe": (RELEVER, "    if not rapports:\n", "    if False:\n", "R3"),
    "S4_tous_les_rapports": (RELEVER, "[-n:]", "", "R4"),
    "S5_tout_responsable": (RELEVER, 'if len(cases) > 4 and "Pilote" in cases[4]:', "if len(cases) > 4:", "R5"),
    "S6_aucune_decision": (VERIFIER, 'DECISION = re.compile(r"DÉCIDÉ|TRANCHÉ")',
                           'DECISION = re.compile(r"JAMAIS_ECRIT")', "V1"),
    "S7_note_sans_sert_passe": (VERIFIER, "        if not cites:\n", "        if False:\n", "V2"),
    "S8_absente_passe": (VERIFIER, "if a not in idx or not DECISION.search(idx[a])",
                         "if a in idx and not DECISION.search(idx[a])", "V3"),
    "S9_non_decidee_passe": (VERIFIER, "if a not in idx or not DECISION.search(idx[a])",
                             "if a not in idx", "V4"),
    "S10_non_rattache_rend_0": (VERIFIER, "    return 3 if mauvais else 0\n", "    return 0\n", "V2"),
    "S11_sans_paire_accepte": (VERIFIER, "if len(argv) < 3 or", "if len(argv) < 2 or", "V5"),
    # X1 : sans re.I, le motif ne lit plus que la casse qu'il écrit. Écrit en capitales (la forme du BACKLOG,
    # « BLOCAGE »), il devient aveugle aux minuscules : C1 doit rougir. Retirer re.I en gardant le motif en
    # minuscules (X1b) le rend aveugle aux capitales : c'est R1 qui rougit, pas C1 (mesuré au tour 2).
    "X1_sans_re_I_motif_en_capitales": (RELEVER, 'MOT = re.compile(r"\\bblocages?\\b", re.I)',
                                        'MOT = re.compile(r"\\bBLOCAGES?\\b")', "C1"),
    "X1b_sans_re_I_motif_en_minuscules": (RELEVER, 'MOT = re.compile(r"\\bblocages?\\b", re.I)',
                                          'MOT = re.compile(r"\\bblocages?\\b")', "R1"),
    "X2_sans_re_M": (VERIFIER, 'SERT = re.compile(r"^\\s*SERT\\s*:\\s*(A-\\d+)", re.M)',
                     'SERT = re.compile(r"^\\s*SERT\\s*:\\s*(A-\\d+)")', "C4"),
    "X3a_N_defaut_4": (RELEVER, "if len(argv) == 3 else 3", "if len(argv) == 3 else 4", "C2a"),
    "X3b_N_defaut_2": (RELEVER, "if len(argv) == 3 else 3", "if len(argv) == 3 else 2", "C2b"),
    "X4_sans_mot_entier": (RELEVER, 'MOT = re.compile(r"\\bblocages?\\b", re.I)',
                           'MOT = re.compile(r"blocages?", re.I)', "C3"),
    # Tour 3 — les sabotages du superviseur R-759 (Z1 à Z14, repris à l'identique de son script de session),
    # puis ceux de la passe systématique, un par propriété de l'INVENTAIRE en tête.
    "Z1_pluriel": (RELEVER, 'r"\\bblocages?\\b", re.I)', 'r"\\bblocage\\b", re.I)', "C5"),
    "Z2_stdin_jamais": (RELEVER, 'if argv[1] == "-" else', 'if False else', "I1"),
    "Z3_usage_relever": (RELEVER, 'if len(argv) not in (2, 3):', 'if False:', "A0"),
    "Z4_N_illisible_0": (RELEVER, '        print("LECTURE IMPOSSIBLE : %s" % e)\n        return 2',
                         '        print("LECTURE IMPOSSIBLE : %s" % e)\n        return 0', "L1"),
    "Z4b_fichier_absent_0": (RELEVER, '        print("LECTURE IMPOSSIBLE : %s" % e)\n        return 2',
                             '        print("LECTURE IMPOSSIBLE : %s" % e)\n        return 0', "L2"),
    "Z5_premiere_occurrence": (RELEVER, 'for m in MOT.finditer(l):', 'for m in list(MOT.finditer(l))[:1]:', "C6"),
    "Z6_extrait_vide": (RELEVER, 'l[max(0, m.start() - 150):m.end() + 150]', '""', "E1"),
    "Z7_sans_filtre_A": (RELEVER, '        if not re.match(r"^\\| A-\\d+ \\|", l):\n            continue\n', '', "F1"),
    "Z8_decide_seul": (VERIFIER, 'r"DÉCIDÉ|TRANCHÉ"', 'r"DÉCIDÉ"', "T1"),
    "Z9_tranche_seul": (VERIFIER, 'r"DÉCIDÉ|TRANCHÉ"', 'r"TRANCHÉ"', "D1"),
    "Z10_egal_absent": (VERIFIER, ' or any("=" not in a for a in argv[2:])', '', "Q1"),
    "Z11_backlog_illisible_0": (VERIFIER, '        print("LECTURE IMPOSSIBLE DU BACKLOG : %s" % e)\n        return 2',
                                '        print("LECTURE IMPOSSIBLE DU BACKLOG : %s" % e)\n        return 0', "B1"),
    "Z12_note_illisible_passe": (VERIFIER, '            mauvais += 1\n            continue\n        cites',
                                 '            continue\n        cites', "N1"),
    "Z13_derniere_note_seule": (VERIFIER, '    return 3 if mauvais else 0', '    return 3 if fautes or not cites else 0', "M1"),
    "Z14_sans_blancs_tete": (VERIFIER, 'r"^\\s*SERT', 'r"^SERT', "W1"),
    "E1_extrait_10": (RELEVER, 'l[max(0, m.start() - 150):m.end() + 150]', 'l[max(0, m.start() - 10):m.end() + 10]', "E1"),
    "E2_sans_avant": (RELEVER, 'max(0, m.start() - 150)', 'm.start()', "E1"),
    "E3_sans_apres": (RELEVER, 'm.end() + 150]', 'm.end()]', "E1"),
    "E4_sans_borne_avant": (RELEVER, 'max(0, m.start() - 150)', '0', "E1"),
    "E5_sans_borne_apres": (RELEVER, 'm.end() + 150]', 'len(l)]', "E1"),
    "E6_sans_plancher_0": (RELEVER, 'max(0, m.start() - 150)', 'm.start() - 150', "C1"),
    "B1_format_sans_BLOCAGE": (RELEVER, '"BLOCAGE %s : …%s…"', '"%s : …%s…"', "R1"),
    "I2_mauvais_identifiant": (RELEVER, 'sortie.append((cases[1], l))', 'sortie.append((cases[2], l))', "R1"),
    "I3_cases_sans_strip": (RELEVER, '[c.strip() for c in l.split("|")]', '[c for c in l.split("|")]', "R1"),
    "F2_filtre_sans_A": (RELEVER, 'r"^\\| A-\\d+ \\|"', 'r"^\\| \\S+ \\|"', "F1"),
    "F3_filtre_sans_chiffres": (RELEVER, 'r"^\\| A-\\d+ \\|"', 'r"^\\| A-\\S+ \\|"', "F1"),
    "P1_pilote_partout": (RELEVER, '"Pilote" in cases[4]', '"Pilote" in l', "P1"),
    "P2_mauvaise_colonne": (RELEVER, '"Pilote" in cases[4]', '"Pilote" in cases[5]', "R1"),
    "O1_ordre_inverse": (RELEVER, 'sortie.append((cases[1], l))', 'sortie.insert(0, (cases[1], l))', "R4"),
    "N1_argument_ignore": (RELEVER, 'int(argv[2]) if len(argv) == 3 else 3', '3', "R4"),
    "U1_relever_ascii": (RELEVER, 'open(argv[1], encoding="utf-8").read()', 'open(argv[1], encoding="ascii").read()', "R1"),
    "A1_un_argument_admis": (RELEVER, 'not in (2, 3):', 'not in (1, 2, 3):', "A0"),
    "A2_quatre_admis": (RELEVER, 'not in (2, 3):', 'not in (2, 3, 4):', "A4"),
    "O2_sans_mention_rend_3": (RELEVER, "    return 0\n", "    return 3\n", "R2"),
    "B2_bilan_sans_mot": (RELEVER, '"%d MENTION(S) DE BLOCAGE dans', '"%d dans', "C6"),
    "B3_noms_vides": (RELEVER, 'noms = ", ".join(i for i, _ in rapports)', 'noms = ""', "R2"),
    "B4_K_vaut_N": (RELEVER, '% (len(rapports), noms)', '% (n, noms)', "R2"),
    "W2_deux_points_espaces": (VERIFIER, 'SERT\\s*:\\s*(', 'SERT : (', "W2"),
    "W3_sans_ancre": (VERIFIER, 'r"^\\s*SERT', 'r"\\s*SERT', "W3"),
    "W4_un_seul_chiffre": (VERIFIER, '(A-\\d+)", re.M', '(A-\\d)", re.M', "V1"),
    "W5_premiere_ligne_seule": (VERIFIER, 'SERT.findall(note)', 'SERT.findall(note)[:1]', "C4"),
    "V7_index_hors_tete": (VERIFIER, 're.match(r"^\\| (A-\\d+) \\|", l)', 're.search(r"\\| (A-\\d+) \\|", l)', "V6"),
    "Q3_coupe_a_chaque_egal": (VERIFIER, 'paire.split("=", 1)', 'paire.split("=")', "Q2"),
    "U2_backlog_ascii": (VERIFIER, 'open(argv[1], encoding="utf-8")', 'open(argv[1], encoding="ascii")', "V1"),
    "U3_note_ascii": (VERIFIER, 'open(chemin, encoding="utf-8")', 'open(chemin, encoding="ascii")', "V1"),
    "M1b_premiere_paire_seule": (VERIFIER, 'for paire in argv[2:]:', 'for paire in argv[2:3]:', "M2"),
    "M3_bilan_sur_1": (VERIFIER, '(mauvais, len(argv) - 2)', '(mauvais, 1)', "M1"),
    "Y1_toujours_3": (VERIFIER, "    return 3 if mauvais else 0\n", "    return 3\n", "V1"),
    "Y2_format_rattache": (VERIFIER, '"RATTACHÉ %s : sert %s"', '"%s : sert %s"', "V1"),
}


class NonJoue(Exception):
    """Un contrôle qui n'a pas pu tourner (R-734) : jamais confondu avec un vert."""


def vraie_ligne(depot, ident):
    """Rend la ligne du BACKLOG réel qui porte l'action `ident` (R-732), ou lève NonJoue."""
    try:
        with open(os.path.join(depot, BACKLOG), encoding="utf-8") as f:
            for l in f:
                if l.startswith("| %s |" % ident):
                    return l.rstrip("\n")
    except OSError as e:
        raise NonJoue("BACKLOG illisible : %s" % e)
    raise NonJoue("vraie ligne %s introuvable dans %s" % (ident, BACKLOG))


def poser_la_copie(depot, dossier, sabotage):
    """Copie les deux programmes dans `dossier`, applique le sabotage s'il y en a un, rend leurs chemins."""
    chemins = {}
    for prog in (RELEVER, VERIFIER):
        src = os.path.join(depot, prog)
        if not os.path.isfile(src):
            raise NonJoue("programme absent : %s" % prog)
        dst = os.path.join(dossier, os.path.basename(prog))
        shutil.copyfile(src, dst)
        chemins[prog] = dst
    if sabotage:
        prog, avant, apres, _ = SABOTAGES[sabotage]
        t = open(chemins[prog], encoding="utf-8").read()
        if t.count(avant) != 1:
            raise NonJoue("sabotage %s : le texte à remplacer apparaît %d fois dans %s"
                          % (sabotage, t.count(avant), prog))
        with open(chemins[prog], "w", encoding="utf-8") as f:
            f.write(t.replace(avant, apres))
    return chemins


def ecrire(dossier, nom, texte):
    """Écrit un fichier de cas dans le dossier temporaire et rend son chemin."""
    p = os.path.join(dossier, nom)
    with open(p, "w", encoding="utf-8") as f:
        f.write(texte)
    return p


def lancer(programme, arguments, dossier, entree=""):
    """Lance un programme copié, `entree` sur son entrée standard (fermée ensuite) ; rend (code, sortie).
    Un délai dépassé lève NonJoue."""
    try:
        x = subprocess.run([sys.executable, "-B", programme] + arguments, cwd=dossier,
                           capture_output=True, text=True, timeout=DELAI, input=entree)
    except subprocess.TimeoutExpired:
        raise NonJoue("délai de %d s dépassé : %s" % (DELAI, os.path.basename(programme)))
    return x.returncode, x.stdout + x.stderr


def controler_l_inventaire():
    """Lit l'INVENTAIRE de l'en-tête ; rend (gardées, non_gardées, problèmes).

    Une propriété gardée nomme des « sabotage→cas » : chaque sabotage doit exister dans SABOTAGES et y viser ce cas.
    Chaque sabotage de SABOTAGES doit être nommé par au moins une propriété. Une propriété sans sabotage doit dire
    « NON GARDÉ : raison »."""
    gardees, non_gardees, problemes, nommes = 0, 0, [], set()
    vus = set()
    for ligne in (__doc__ or "").splitlines():
        m = re.match(r"^  (P-[RV]\d+) ¦ (.+?) ¦ (.+)$", ligne)
        if not m:
            continue
        ident, _, garde = m.groups()
        if ident in vus:
            problemes.append("%s en double dans l'inventaire" % ident)
        vus.add(ident)
        if garde.startswith("NON GARDÉ : ") and len(garde) > len("NON GARDÉ : "):
            non_gardees += 1
            continue
        gardees += 1
        for paire in garde.split(", "):
            sc = paire.split("→")
            if len(sc) != 2:
                problemes.append("%s : « %s » n'est ni « sabotage→cas » ni « NON GARDÉ : raison »" % (ident, paire))
                continue
            s, c = sc
            nommes.add(s)
            if s not in SABOTAGES:
                problemes.append("%s : sabotage %s absent de la table" % (ident, s))
            elif SABOTAGES[s][3] != c:
                problemes.append("%s : %s vise %s dans la table, pas %s" % (ident, s, SABOTAGES[s][3], c))
    for s in SABOTAGES:
        if s not in nommes:
            problemes.append("sabotage %s : aucune propriété de l'inventaire ne le nomme" % s)
    if not vus:
        problemes.append("inventaire introuvable dans l'en-tête")
    return gardees, non_gardees, problemes


def jouer_les_cas(depot, sabotage=None):
    """Joue les cas de la liste `cas` sur une copie ; rend la liste (cas, bon, détail). Lève NonJoue si un cas ne peut
    tourner. Avec un sabotage, seuls les cas du programme saboté sont joués : l'autre programme n'est pas touché.
    Un cas : (nom, programme, arguments, code attendu, mots qui doivent paraître, mots qui ne doivent pas paraître,
    entrée standard)."""
    l1055 = vraie_ligne(depot, "A-1055")
    l1014 = vraie_ligne(depot, "A-1014")
    tete = "| Id | Action | Statut | Responsable | Source | Échéance | Liens |\n|---|---|---|---|---|---|---|\n"
    fin = " | CONSTAT·26/11 | Pilote V8 | essai | immédiat | — |"
    propre = "| A-90001 | rapport de passage sans rien à signaler" + fin
    bloque = "| A-90002 | rapport de passage : **BLOCAGE** sur l'essai" + fin
    chat = "| A-90003 | le Chat écrit **BLOCAGE** ici | CONSTAT·26/11 | Chat | essai | immédiat | — |"
    afaire = "| A-90004 | une action proposée | À FAIRE·26/11 | Chat | essai | — | — |"
    minus = ("| A-90005 | rapport de passage : le blocage de l'essai tient toujours, rien n'avance tant qu'il n'est "
             "pas levé" + fin)
    tranche = "| A-90006 | une décision prise | TRANCHÉ·26/11 | Jean-Luc | essai | — | — |"
    decide = "| A-90007 | une autre décision | DÉCIDÉ·26/11 | Jean-Luc | essai | — | — |"
    p1, p2, p3 = (propre.replace("A-90001", "A-9001%d" % i) for i in (1, 2, 3))
    debloc = "| A-90020 | rapport de passage : déblocage de l'essai constaté" + fin
    plur = "| A-90021 | rapport de passage : deux blocages de l'essai tiennent toujours" + fin
    deux = "| A-90030 | rapport de passage : premier BLOCAGE sur l'essai, puis un second blocage sur la mesure" + fin
    # E1 : AVANTMOT finit 45 caractères avant « blocage », APRESMOT commence 59 caractères après ; LOINAVANT et
    # LOINAPRES sont à plus de 200 caractères (condition 3 du superviseur : plus de 20, et moins de 150 pour les
    # deux premiers).
    extr = ("| A-90040 | rapport de passage : LOINAVANT " + "w" * 200 + " AVANTMOT " + "x" * 40
            + " le blocage de l'essai tient " + "y" * 40 + " APRESMOT " + "z" * 200 + " LOINAPRES" + fin)
    hors = ("| B-90050 | rapport de passage : **BLOCAGE** hors du tableau d'actions" + fin + "\n"
            "| A-X51 | rapport de passage : **BLOCAGE** sous un identifiant sans chiffres" + fin)
    pil = "| A-90060 | le Chat rapporte ce que dit le Pilote V8 : **BLOCAGE** | CONSTAT·26/11 | Chat | essai | — | — |"
    resultats = []
    d = tempfile.mkdtemp(prefix="epreuve_blocages_")
    try:
        c = poser_la_copie(depot, d, sabotage)
        r, v = c[RELEVER], c[VERIFIER]
        b2 = ecrire(d, "b2.md", tete + propre + "\n")
        # Chemin RELATIF (les programmes tournent dans `d`) : le message d'erreur ne porte pas le nom du dossier
        # temporaire, et la sortie se rejoue à l'identique (garde-fou, « SORTIE FABRIQUEE »).
        absent = "absent.md"
        cas = [
            ("R1", r, [ecrire(d, "b1.md", tete + l1055 + "\n")], 3, ("BLOCAGE A-1055 :",)),
            ("R2", r, [b2], 0, ("AUCUN BLOCAGE dans les 1 derniers rapports du pilote (A-90001)",)),
            ("R3", r, [ecrire(d, "b3.md", tete + afaire + "\n")], 2, ("AUCUN RAPPORT DU PILOTE",)),
            ("R4", r, [ecrire(d, "b4.md", tete + bloque + "\n" + propre + "\n"), "1"], 0, ("AUCUN BLOCAGE",)),
            ("R5", r, [ecrire(d, "b5.md", tete + chat + "\n" + propre + "\n")], 0, ("AUCUN BLOCAGE",)),
            ("C1", r, [ecrire(d, "c1.md", tete + minus + "\n")], 3, ("BLOCAGE A-90005 :", "rapport de passage")),
            ("C2a", r, [ecrire(d, "c2a.md", tete + "\n".join([bloque, p1, p2, p3]) + "\n")], 0,
             ("AUCUN BLOCAGE dans les 3 derniers",)),
            ("C2b", r, [ecrire(d, "c2b.md", tete + "\n".join([bloque, p1, p2]) + "\n")], 3, ("BLOCAGE A-90002 :",)),
            ("C3", r, [ecrire(d, "c3.md", tete + debloc + "\n")], 0, ("AUCUN BLOCAGE",)),
            ("C5", r, [ecrire(d, "c5.md", tete + plur + "\n")], 3, ("BLOCAGE A-90021 :",)),
            ("C6", r, [ecrire(d, "c6.md", tete + deux + "\n")], 3,
             ("2 MENTION(S) DE BLOCAGE dans les 1 derniers rapports du pilote (A-90030)",)),
            ("E1", r, [ecrire(d, "e1.md", tete + extr + "\n")], 3, ("BLOCAGE A-90040 :", "AVANTMOT", "APRESMOT"),
             ("LOINAVANT", "LOINAPRES")),
            ("F1", r, [ecrire(d, "f1.md", tete + hors + "\n" + propre + "\n")], 0,
             ("AUCUN BLOCAGE dans les 1 derniers rapports du pilote (A-90001)",)),
            ("P1", r, [ecrire(d, "p1.md", tete + pil + "\n" + propre + "\n")], 0,
             ("AUCUN BLOCAGE dans les 1 derniers rapports du pilote (A-90001)",)),
            ("I1", r, ["-"], 3, ("BLOCAGE A-90002 :",), (), tete + bloque + "\n"),
            ("A0", r, [], 2, ("USAGE",)),
            ("A4", r, [b2, "1", "en-trop"], 2, ("USAGE",)),
            ("L1", r, [b2, "trois"], 2, ("LECTURE IMPOSSIBLE",)),
            ("L2", r, [absent], 2, ("LECTURE IMPOSSIBLE",)),
        ]
        bv = ecrire(d, "backlog_v.md", tete + l1014 + "\n" + afaire + "\n" + tranche + "\n" + decide + "\n")
        n1 = ecrire(d, "n1.md", "SERT : A-1014\nRôle : essai.\n")
        n2 = ecrire(d, "n2.md", "Rôle : essai, sans ligne de rattachement.\n")
        n4 = ecrire(d, "n4.md", "SERT : A-90004\n")
        cas += [
            ("V1", v, [bv, "n=" + n1], 0, ("RATTACHÉ n : sert A-1014",)),
            ("V2", v, [bv, "n=" + n2], 3, ("NON RATTACHÉ n : aucune ligne",)),
            ("V3", v, [bv, "n=" + ecrire(d, "n3.md", "SERT : A-99999\n")], 3, ("NON RATTACHÉ n : A-99999",)),
            ("V4", v, [bv, "n=" + n4], 3, ("NON RATTACHÉ n : A-90004",)),
            ("V5", v, [bv], 2, ("USAGE",)),
            ("C4", v, [bv, "n=" + ecrire(d, "c4.md", "SERT : A-1014\nSERT : A-99999\nRôle : essai.\n")], 3,
             ("NON RATTACHÉ n : A-99999",)),
            ("T1", v, [bv, "n=" + ecrire(d, "t1.md", "SERT : A-90006\n")], 0, ("RATTACHÉ n : sert A-90006",)),
            ("D1", v, [bv, "n=" + ecrire(d, "d1.md", "SERT : A-90007\n")], 0, ("RATTACHÉ n : sert A-90007",)),
            ("W1", v, [bv, "n=" + ecrire(d, "w1.md", "Rôle : essai.\n   SERT : A-1014\n")], 0,
             ("RATTACHÉ n : sert A-1014",)),
            ("W2", v, [bv, "n=" + ecrire(d, "w2.md", "SERT:A-1014\n")], 0, ("RATTACHÉ n : sert A-1014",)),
            ("W3", v, [bv, "n=" + ecrire(d, "w3.md", "Rôle : un texte qui cite SERT : A-1014 en passant.\n")], 3,
             ("NON RATTACHÉ n : aucune ligne",)),
            ("N1", v, [bv, "n=" + absent], 3, ("NON RATTACHÉ n : note illisible", "1 NOTE(S) NON RATTACHÉE(S) SUR 1")),
            ("B1", v, [absent, "n=" + n1], 2, ("LECTURE IMPOSSIBLE DU BACKLOG",)),
            ("Q1", v, [bv, n1], 2, ("USAGE",)),
            ("Q2", v, [bv, "n=" + ecrire(d, "q=2.md", "SERT : A-1014\n")], 0, ("RATTACHÉ n : sert A-1014",)),
            ("M1", v, [bv, "a=" + n2, "b=" + n1], 3,
             ("NON RATTACHÉ a : aucune ligne", "RATTACHÉ b : sert A-1014", "1 NOTE(S) NON RATTACHÉE(S) SUR 2")),
            ("M2", v, [bv, "a=" + n1, "b=" + n2], 3,
             ("RATTACHÉ a : sert A-1014", "NON RATTACHÉ b : aucune ligne", "1 NOTE(S) NON RATTACHÉE(S) SUR 2")),
            ("V6", v, [ecrire(d, "backlog_v6.md", "> rappel : | A-90004 | était DÉCIDÉ autrefois\n" + tete + afaire
                              + "\n"), "n=" + n4], 3, ("NON RATTACHÉ n : A-90004",)),
        ]
        visee = c[SABOTAGES[sabotage][0]] if sabotage else None
        for un in cas:
            nom, prog, args, code_attendu, mots = un[:5]
            interdits = un[5] if len(un) > 5 else ()
            entree = un[6] if len(un) > 6 else ""
            if visee and prog != visee:
                continue
            code, sortie = lancer(prog, args, d, entree)
            manquants = [m for m in mots if m not in sortie]
            presents = [m for m in interdits if m in sortie]
            bon = code == code_attendu and not manquants and not presents
            der = (sortie.strip().splitlines() or [""])[-1][:110]
            resultats.append((nom, bon, "code %s (attendu %s) · %s · %s"
                              % (code, code_attendu,
                                 "ABSENT : « %s »" % " / ".join(manquants) if manquants else
                                 ("EN TROP : « %s »" % " / ".join(presents) if presents else "mots vus"), der)))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return resultats


def main(argv):
    """Contrôle l'inventaire, joue le passage normal, ou les sabotages demandés ; rend le code de sortie (0, 1 ou 2)."""
    positionnels = [a for a in argv[1:] if not a.startswith("--")]
    depot = os.path.abspath(positionnels[0] if positionnels else ".")
    choix = None
    for a in argv[1:]:
        if a == "--saboter":
            choix = list(SABOTAGES)
        elif a.startswith("--saboter="):
            choix = [s for s in a.split("=", 1)[1].split(",") if s]
            inconnus = [s for s in choix if s not in SABOTAGES]
            if inconnus:
                print("SABOTAGE INCONNU : %s" % ", ".join(inconnus))
                return 2
    gardees, non_gardees, problemes = controler_l_inventaire()
    print("INVENTAIRE : %d propriétés gardées, %d NON GARDÉES, %d sabotages" % (gardees, non_gardees, len(SABOTAGES)))
    for p in problemes:
        print("INVENTAIRE FAUX : %s" % p)
    if problemes:
        print("VERDICT : ÉCHEC — l'inventaire ne correspond pas à la table des sabotages")
        return 1
    faute, non_joue = False, False
    try:
        normaux = jouer_les_cas(depot)
    except NonJoue as e:
        print("NON JOUÉ (R-734) : %s" % e)
        return 2
    for nom, bon, det in normaux:
        print("== %s : %s · %s" % (nom, "vert" if bon else "ROUGE <-- ATTENDU VERT", det))
        faute = faute or not bon
    if choix:
        if faute:
            print("SABOTAGES NON JOUÉS : le passage normal n'est pas vert, un sabotage n'y prouverait rien")
            return 1
        for s in choix:
            cible = SABOTAGES[s][3]
            try:
                res = dict((n, (b, d)) for n, b, d in jouer_les_cas(depot, s))
            except NonJoue as e:
                print("%s NON JOUÉ (R-734) : %s" % (s, e))
                non_joue = True
                continue
            rouges = [n for n, (b, _) in res.items() if not b]
            if cible in rouges:
                print("%s mord : [%s] · %s" % (s, ", ".join(rouges), res[cible][1]))
            else:
                print("%s NE MORD PAS <-- SABOTAGE NON VU : %s reste vert (rouges : %s)"
                      % (s, cible, ", ".join(rouges) or "aucun"))
                faute = True
    if non_joue:
        print("VERDICT : NON JOUÉ — au moins un contrôle n'a pas pu tourner (R-734)")
        return 2
    print("VERDICT :", "tout est conforme" if not faute else "ÉCHEC — voir ci-dessus")
    return 1 if faute else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
