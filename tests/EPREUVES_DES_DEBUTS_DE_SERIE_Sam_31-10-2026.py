#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_DEBUTS_DE_SERIE — Sam 31-10-2026 (Paris)
Rôle : prouver que `combler_les_debuts` de programmes/REPARER_L_HISTORIQUE_LONG.py comble juste le début des séries
décidées, s'arrête quand il ne peut pas mesurer sûrement, et que chaque épreuve a des dents (R-731).
Quand l'appeler : avant toute livraison qui touche `combler_les_debuts`, `raison_du_manque` ou `DEBUTS_A_COMBLER`.

À QUOI ÇA SERT. Décision de Jean-Luc du 29-10-2026 à 11h58 (A-577 ④, point 1 de A-633) : combler depuis les archives
de Paris (bnains) les séances d'avant la première ligne de Yahoo. Un début de série comblé au mauvais facteur, ou à
travers une division oubliée, reste plausible ligne par ligne, et K10 ne le voit plus : dans une zone toute venue de
Paris, le rapport au cours brut est constant par construction. Ces épreuves jouent les VRAIES lignes du dépôt (Yahoo
déposé, bnains sans ses barres fausses, Francfort, le calendrier officiel) ; les défauts sont FABRIQUÉS sur des copies.

LES ÉPREUVES (les défauts sont FABRIQUÉS sur des copies des vraies données) :
D1 THALES, du 03-01-2000 : une séance comblée, le 03-01-2000, à la barre de Paris arrondie à 4 décimales (facteur
   1,0 mesuré), geste « comblé » parti de Paris, clôture avant vide, source bnains.
D2 AIRBUS, du 10-07-2000 : chaque séance du calendrier du 10-07-2000 au 31-08-2001 est soit comblée (source bnains),
   soit au journal en « non comblé » avec une raison, jamais les deux ni aucun ; le 13-10-2000, sans barre chez bnains,
   est « non comblé » (« pas de barre chez bnains ») ; aucune ligne comblée un jour où `K.barre_sure` refuse.
D3 STMICROELECTRONICS, du 03-01-2000, vraies données (décision de Jean-Luc du 31-10-2026 à 19h23) : la division par
   3 du 09-05-2000, prouvée par le 6-K de 2000 (DIVISIONS_OFFICIELLES.csv), est PORTÉE : les 88 séances d'avant le
   09-05-2000 sont comblées, chaque ligne le dit (« portée »), et la marche de la courbe du 08 au 09-05-2000 vaut 1/3
   à `K.MARCHE_EXACTE` près.
D3c la même demande, SANS la table officielle : la division n'est plus vue que chez bnains ; ARRÊT par P2 (« rapport
   pris de bnains seul », DIVISIONS_BNAINS) ; rien n'est écrit (règle de fond du superviseur R-759 du 31-10-2026).
D3b la même demande, sans la table officielle et la ligne du 09-05-2000 ôtée de la table de bnains : P2 se tait, et
   la garde des SAUTS arrête, en nommant le 08-05-2000 → 09-05-2000 (−68 %) (piège T3 du superviseur du 31-10-2026).
D4 UNIBAIL-RODAMCO-WESTFIELD, du 18-06-2007 : ARRÊT, référence de 0 séance (bnains finit le 28-02-2017, Yahoo
   commence le 14-04-2023) ; rien n'est écrit.
D5 AIRBUS avec un détachement officiel FABRIQUÉ le 15-01-2001, un droit « document » (une action gratuite pour neuf :
   × 0,9) : PORTÉ ; 291 séances comblées, et la marche de la courbe du 12 au 15-01-2001 vaut 0,9 à `K.MARCHE_EXACTE`
   près (avant le 31-10-2026, ce cas arrêtait). 291 et non plus 290 depuis le 13-11-2026 (décision de Jean-Luc A-752 ⑥,
   après vérification indépendante) : la remise au bon jour des fichiers bnains échangés des 19 et 20-06-2001 (E2c,
   commit 8710a224) rend sûre la barre d'AIRBUS du 19-06-2001, « non comblé » avant (jour douteux, Francfort ne
   confirmait pas la barre du mauvais jour).
D6 AIRBUS dont la série de Yahoo est FABRIQUÉE à moitié prix et à double volume : chaque clôture comblée vaut la
   moitié de la barre de Paris, chaque volume le double, et le journal écrit 0,5 et 2,0 (les facteurs sont MESURÉS,
   jamais supposés 1).
D7 AIRBUS avec une division FABRIQUÉE (2 pour 1 le 02-01-2001, DÉCLARÉE PAR YAHOO, et les barres de Paris d'avant
   doublées) : les clôtures comblées d'avant le 02-01-2001 valent la barre de Paris ÷ 2, sans arrêt — P2 ne compte
   pas les divisions de Yahoo, que `K.divisions` applique déjà.
D7r la même, evenements.json et `K.EVENEMENTS` RENOMMÉS ensemble : toujours verte (défaut 5 du superviseur R-759 du
   31-10-2026 : un contrôle ne change pas d'avis quand on renomme un fichier).
D8 la réparation entière sur une copie des fichiers qu'elle lit (`LU`, `DOSSIERS_LUS`, le registre), lancée
   depuis un dossier VIDE, la liste décidée : code 0, et les lignes « comblé » et « non comblé » de début de série
   du journal écrit sont celles du journal du dépôt, à l'octet.
D9 la même, STMICROELECTRONICS demandée dès le 03-01-2000, la table DIVISIONS_OFFICIELLES ôtée de la copie : code 2,
   la table nommée, ni le fichier réparé ni le journal n'existent dans la copie.
D9b la même, la table DIVISIONS_OFFICIELLES GARDÉE mais privée de sa ligne de STMICROELECTRONICS (en-tête et autres
   lignes gardés) : la division du 09-05-2000 n'est plus vue que chez bnains, `combler_les_debuts` refuse, et la
   réparation entière doit passer par sa garde d'arrêt (`if refus_des_comblements:`) : code 1, une ligne « ARRÊT —
   STMICROELECTRONICS : début de série » qui dit « rapport pris de bnains seul », « rien n'est écrit », ni le fichier
   réparé ni le journal dans la copie. Raison (superviseur R-759 du 13-11-2026, h-1 de la seconde relecture de
   Cowork) : depuis que D9 ôte la table (code 2, avant la garde), plus aucune épreuve ne passait par cette garde, et
   le sabotage G8 ne mordait plus. Sous G8, mesuré par le superviseur : code 0 et les deux fichiers écrits.
D9i LA PROPRIÉTÉ « TOUT REFUS RENDU PAR UN GESTE DE LA RÉPARATION L'ARRÊTE » (superviseur R-759 du 13-11-2026, n-1
   de la relecture de Cowork de 13h55 : trois des quatre termes de la somme des refus pouvaient être ôtés sans
   qu'aucune épreuve rougisse, et la réparation entière ÉCRIVAIT alors, code 0). CLASSEMENT FERMÉ (N-a du relecteur
   du 13-11-2026 à 18h45, verdict du superviseur R-759 de 18h55) : chaque fonction du module atteinte depuis `reparer`
   (appel par nom, en descendant dans les fonctions appelées : 21 le 13-11-2026, dont 17 appelées par `reparer`
   lui-même) porte dans son ⑤ la marque `[refus: dernier]` ou `[refus: non — raison]`. `classement_des_refus` rend
   les cibles (marque `dernier` : combler_les_debuts, combler_les_seances, combler_les_seances_decidees,
   combler_par_raccords, reconstruire, retirer), les atteintes NON CLASSÉES et les marquées NON ATTEINTES. Pour
   CHAQUE cible, une épreuve D9i_<fonction> : la réparation entière, la
   liste décidée (le cadre de D8), la fonction enveloppée pour ajouter à ses refus « INJECTÉ PAR L'ÉPREUVE D9i dans
   <fonction> » ; exigé : code 1, la ligne « ARRÊT — <cette marque> », « rien n'est écrit », ni le fichier réparé ni
   le journal dans la copie. La garde D9i rougit si aucune fonction n'est repérée, ou si le témoin sans ajout (D8 :
   code 0, les deux fichiers écrits) n'est pas vert, ou si l'ensemble classé n'est pas ÉGAL à l'ensemble atteint
   (une fonction atteinte sans marque, ou une marque sur une fonction qui n'est plus atteinte) ; une marque qui
   n'apparaît pas fait rougir l'épreuve de sa fonction. Aucune donnée en litige n'y entre : le refus est fabriqué.
   Un renommage ne fait plus rien perdre : la marque suit la fonction (sabotage G38, le mutant M1 du relecteur).
   DEUX TÉMOINS CONFRONTÉS (superviseur R-759 du 13-11-2026 à 20h12, sur M-1 du relecteur de 20h06 : la marque
   `[refus: non — …]` posée sur `reconstruire` et ses arrêts jetés par `arrets = []` laissaient tout vert, code 0 ; la
   marque était une déclaration que personne ne confrontait au code). Le TÉMOIN DU CODE (`alimentation_des_arrets`) :
   dans l'arbre de `reparer`, chaque `if X:` dont le corps imprime « ARRÊT — » et fait `return 1` est un PUITS ; ses
   variables sont remontées par leurs liaisons (`=`, `+=`, somme `a + b`, dernier élément d'un tuple) jusqu'aux
   fonctions du module appelées : elles ALIMENTENT un arrêt, et sont cibles de D9i quelle que soit leur marque. Le
   TÉMOIN DÉCLARÉ : la marque `[refus: …]`. La garde D9i rougit aussi si une fonction qui alimente un arrêt n'est pas
   marquée `dernier`, ou si une fonction marquée `dernier` n'alimente aucun arrêt. Les cibles de D9i sont l'UNION des
   deux témoins (une cible déclarée qui n'alimente rien garde donc son épreuve D9i_, qui rougit). Le témoin du code
   est calibré à chaque jeu sur trois sources fabriquées (une qui doit trouver, deux qui ne doivent rien trouver) ;
   une calibration fausse fait rougir D9i.
   LIMITES (⑨ de `classement_des_refus`) : DEUX mensonges coordonnés rendent encore un arrêt muet (sortir l'appel de
   tout puits ET marquer la fonction `non`) ; les appels par attribut (`K.x`, `RC.x`) ne sont pas classés ; les
   puits hors de `reparer` et les puits nourris par une compréhension (`trous`) ne sont pas suivis.
D10 P1, LA PREMIÈRE SÉANCE DE LA RÉFÉRENCE (ici la couture : la première ligne de Yahoo, le 03-09-2001, est dans la
   référence) — défaut A' de la relecture du 31-10-2026 : AIRBUS dont Yahoo est FABRIQUÉ × 0,9 avant le
   05-09-2001, sans AUCUNE déclaration : la médiane de la référence prend le régime d'après (1,0) ; ARRÊT nommant la
   couture du 03-09-2001.
D11 P2, UNE OPÉRATION DANS LA ZONE — défaut B' : AIRBUS, barres de Paris d'avant le 15-01-2001 FABRIQUÉES × 1,1, et
   la table de bnains qui déclare ÷ 1,1 ce jour-là : ARRÊT nommant le 15-01-2001 (la marche, −9 %, est sous la garde
   des sauts).
D12 P2, LA BORNE HAUTE : une opération FABRIQUÉE à la table de bnains le 03-12-2001, DANS la référence, sans trace dans
   les cours : ARRÊT. La borne est la DERNIÈRE séance de la référence, pas la première (défaut A).
D13 L'ACCORD : AIRBUS dont 15 séances de la référence (de la 11e à la 25e) sont FABRIQUÉES × 1,01 chez Yahoo :
   100 séances, accord sous 90 % ; ARRÊT « instable ».
D14 LA COUTURE DANS LA GARDE DES SAUTS : les barres de Paris d'avant le 03-09-2001 FABRIQUÉES × 1,5, que rien ne
   déclare : la référence et P1 se taisent (elles commencent à la couture) ; ARRÊT nommant 31-08-2001 → 03-09-2001,
   le seul saut, qui n'existe qu'avec la première ligne de Yahoo dans la suite.
D15 LA RÉFÉRENCE NE COMPTE JAMAIS UNE LIGNE VENUE DE PARIS, même posée par une entrée précédente de la liste (défaut
   C) : AIRBUS demandée du 02-01-2001, puis du 10-07-2000 ; chaque ligne « comblé » dit une référence qui commence au
   03-09-2001, la première ligne de Yahoo.
D16 la réparation entière, la table des divisions de bnains ôtée de la copie : code 2, la table nommée, rien d'écrit
   (sans elle, P2 perdrait une source sans un mot).
D17 LE CAS C2 de la relecture du tour 2 (31-10-2026) : la barre de Paris du 03-09-2001 ôtée et Yahoo FABRIQUÉ × 0,9
   avant le 04-09-2001, déclaré par personne : ARRÊT « non à la couture » (avant le lot de comblement : 290 séances
   fausses de +11,1 %).
D18 la couture du 03-09-2001 est un jour douteux : ARRÊT « non à la couture ».
D19 P1 DANS L'AUTRE SENS (défaut 2) : Yahoo FABRIQUÉ × 1,1 avant le 05-09-2001 : ARRÊT nommant la couture.
D20 UN AJUSTEMENT CACHÉ DE YAHOO (défaut 3) : une ligne FABRIQUÉE « aucune déclaration » au 15-01-2001 dans une copie
   des verdicts, facteur non documenté : ARRÊT « rapport inconnu ».
D21 LA BORNE BASSE DE P2 EXCLUE : STMICROELECTRONICS demandée dès le 09-05-2000, SANS la table officielle : la division
   de bnains du 09-05-2000 ne touche que les séances d'avant ; 333 séances comblées, aucun arrêt (la demande du
   29-10-2026). 333 et non plus 331 depuis le 13-11-2026 (décision de Jean-Luc A-752 ⑥, après vérification
   indépendante) : la même remise au bon jour rend sûres les barres de STMICROELECTRONICS des 19 et 20-06-2001.
D22 UNE OPÉRATION DOCUMENTÉE APRÈS LA COUTURE : un droit « document » FABRIQUÉ pour AIRBUS le 03-12-2001, dans la
   référence : ARRÊT « dans la référence » (relecture du lot du 31-10-2026, D4 ; sabotage G32).

LES SABOTAGES (avec --saboter) — chacun doit faire rougir au moins une épreuve : G1 garde des sauts ôtée · G2 garde
de la référence ôtée · G3 P2 ôtée · G4 facteur de prix forcé à 1 · G5 divisions de Yahoo ignorées · G6 barre sûre
non exigée · G7 « non comblé » non écrit · G8 `reparer` ignore les refus des comblements · G9 la première séance demandée
exclue · G10 `raison_du_manque` muette sur l'absence de barre · G11 P1 ôtée · G12 borne haute de P2 ramenée au premier
jour de la référence · G13 borne basse de P2 inclusive · G14 P2 compte aussi les divisions de Yahoo · G15 accord non
exigé · G16 la première ligne de Yahoo ôtée de la garde des sauts · G17 sources figées avant la boucle · G18 facteur
de volume forcé à 1 · G19 le journal écrit le facteur de prix comme facteur de volume · G20 table de bnains absente
tolérée · G21 `reparer` passe une liste d'opérations vide · G22 `reparer` lit les verdicts en chemin relatif ·
G23 la couture non exigée · G24 P1 d'un seul sens · G25 toute opération de facteur connu portée, même de bnains seul ·
G26 un rapport inconnu laissé passer comme une division de Yahoo · G27 rien n'est porté · G28 l'opération portée
touche aussi son propre jour · G29 (reconstruction) la table officielle ignorée · G30 (reconstruction) la source des
divisions de Yahoo écrite en dur · G31 (reconstruction) le facteur None non reconnu · G32 une
opération documentée portée même datée après la couture · G33 (tour 3, le X8b de la relecture du tour 2) une
barre seulement utilisable, et non sûre, acceptée (jour douteux ou Francfort ignorés) · G34 la somme des refus sans
`refus_des_decidees` · G35 sans `refus_des_seances` · G36 sans `refus_de_la_chaine` (m1, m2, m3 de la relecture de
Cowork du 13-11-2026) · G37 `arrets += retirer(…)` ramené à `retirer(…)` (m4 du superviseur R-759 du 13-11-2026) :
chacun doit être mordu par D9i_ de SA fonction · G38 le mutant M1 du relecteur du 13-11-2026 (dans
`combler_par_raccords`, `refus` renommé `rejets`, et `refus_de_la_chaine` ôté de la somme) : doit être mordu par
D9i_combler_par_raccords · G39 une fonction marquée `[refus: non — …]` que `reparer` n'atteint pas : doit faire
rougir la garde D9i · G40 la marque de `texte` ôtée (une fonction atteinte non classée) : doit faire rougir la garde
D9i · G41 le mutant M-1 du relecteur du 13-11-2026 à 20h06 (⑤ de `reconstruire` passé à `[refus: non — …]`, et
`arrets = []` inséré avant `arrets += retirer(…)`) : doit être mordu par D9i_reconstruire ou D9i · G42 une marque
SEULE qui ment (⑤ de `reconstruire` passé à `[refus: non — …]`, le code intact) : D9i_reconstruire reste vert (le code
arrête bien), seule la confrontation des deux témoins peut rougir · G43 la calibration du témoin du code faussée (la
première entrée de `CALIBRATION_DU_TEMOIN` attend `["f", "k"]` au lieu de `["f", "k", "m"]`, aucun programme touché) :
seule `all(calibration)` peut rougir. G42 et G43 : R-1 du relecteur M1 du 13-11-2026 (21h16 ; son mutant qui retire la
confrontation laissait G38 et G41 mordre), voie V1 « FIGER » du superviseur R-759 de 21h19. « Mord » veut dire :
les rouges du jeu MOINS les rouges de Z0, non vide (m-b du relecteur du 13-11-2026). Les sabotages marqués « RC »
visent programmes/RECONSTRUIRE_L_HISTORIQUE_LONG.py.
G6 ne mord que par un PLANTAGE : ses rouges sont tous `KeyError : '2000-10-13'` (sans la garde, le code lit une barre
de bnains qui n'existe pas ; relecture du tour 2, Q2). Il reste dans la liste : il montre qu'on ne peut pas ôter la
garde sans faire planter le programme. G33 tient la propriété par de vrais motifs de compte (« AIRBUS 291 comblées,
1 non comblées »). Sous sabotage, chaque épreuve tombée est suivie de la ligne qu'elle a imprimée (`motifs`) ; ce jeu ne
sépare pas encore un refus d'un plantage (BACKLOG, superviseur R-759 du 01-11-2026, d).

CE QUI N'EST PAS ÉPROUVÉ, ET POURQUOI. ① Une opération qu'AUCUNE source du dépôt ne déclare et de moins de 25 %,
dans la zone à combler, passe : c'est le résidu non attrapable écrit au ⑨ de `combler_les_debuts` (STMICROELECTRONICS
÷ 1,1 le 09-05-2000, déclarée par personne : 419 séances comblées, marche de −12,7 %) ; aucune épreuve ne peut
l'exiger. La limite de 25 % vaut pour CHAQUE marche : plusieurs marches non déclarées se cumulent, et l'erreur
cumulée n'est pas bornée (relecture du tour 2, 31-10-2026 : AIRBUS, trois ÷ 1,2 déclarées par personne, aucun arrêt,
290 séances comblées fausses jusqu'à +72,8 %).
② L'exclusion des lignes venues de Paris est exercée sur les vraies lignes (D8 : des lignes comblées par `combler`
tombent dans les fenêtres de référence — AIRBUS et STMICROELECTRONICS les 28-09, 16-10 et 26-10-2001,
THALES 7 lignes du 10-01 au 27-03-2000 — mesuré le 31-10-2026 dans le fichier réparé), mais sans changer le facteur :
seule la période de référence écrite au journal en dépend. ③ P1 mesurée à la première séance de la référence et non
à la couture : quand la première ligne de Yahoo n'était pas dans la référence, un ajustement de Yahoo non déclaré passait
(cas C2 de la relecture du tour 2, 31-10-2026 : 290 séances fausses de +25 %) ;
réparé au lot de comblement du 31-10-2026 : D17 l'exige. ④ G31 ne mord que par le texte de l'arrêt : sans la ligne
du facteur None, l'ajustement caché arrête encore, sous « source non déclarée » (deux gardes, fermées l'une et l'autre).

USAGE : python3 tests/EPREUVES_DES_DEBUTS_DE_SERIE_Sam_31-10-2026.py <racine du dépôt> [--saboter | --saboter=G1,G2…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve verte en Z0 ; 1
sinon ; 2 si un sabotage ne s'applique plus (texte cible absent ou en double), ou si un nom demandé par --saboter=
ne désigne aucun sabotage (m-a du relecteur du 13-11-2026 : `G99` était ignoré en silence, code 0 ; R-3 du relecteur
M1 : TOUS les `--saboter=` sont lus), ou si un argument suit `--saboter` après une espace ou s'ajoute à la racine
(`--saboter G99` faisait de G99 la racine), ou si une option autre que `--saboter` et `--saboter=` est donnée
(m-a bis de Cowork du 13-11-2026 : `--sabotage=G42` jouait Z0 seul et rendait 0).
"""
import ast, contextlib, copy, csv, hashlib, importlib.util, io, json, os, re, shutil, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROGRAMMES = os.path.join(RACINE, "programmes")
REPARATION = os.path.join(PROGRAMMES, "REPARER_L_HISTORIQUE_LONG.py")
RECONSTRUCTION = os.path.join(PROGRAMMES, "RECONSTRUIRE_L_HISTORIQUE_LONG.py")   # visée par les sabotages marqués « RC »
MODULES = ("CONTRATS_DES_FICHIERS", "CALENDRIER_DE_LA_BOURSE", "CONTROLER_L_HISTORIQUE_LONG",
           "RECONSTRUIRE_L_HISTORIQUE_LONG", "REPARER_L_HISTORIQUE_LONG")

# Chaque sabotage : une liste de (texte cible, remplacement), appliqués ensemble à la réparation.
SABOTAGES = {
    "G1": [("\n        if sauts:\n", "\n        if False:\n")],   # le saut de la chaîne a 12 espaces : cible unique
    "G2": [("        if accord < K.PART_PROPRE or len(ref) < MIN_REFERENCE:", "        if False:")],
    "G3": [("        if bloquantes:\n", "        if False:\n")],
    "G4": [("            nouvelles[d], fp, fv = barre(b[d], f * a, k / a,", "            nouvelles[d], fp, fv = barre(b[d], a, k / a,")],
    "G5": [("barre(b[d], f * a, k / a, K.divisions(evenements, valeur, d))", "barre(b[d], f * a, k / a, 1.0)")],
    "G6": [("\n            if not sure:\n", "\n            if False:\n")],
    "G7": [("        for d, geste, apres, fp, texte_, fv in lignes:\n",
            "        for d, geste, apres, fp, texte_, fv in [x for x in lignes if x[1] != \"non comblé\"]:\n")],
    "G8": [("    if refus_des_comblements:", "    if False:")],
    "G9": [("a_combler = [d for d in cal if du <= d < premier]", "a_combler = [d for d in cal if du < d < premier]")],
    "G10": [('        return "pas de barre chez bnains ce jour-là"', '        return ""')],
    "G11": [("        if abs(r0 / f - 1) > K.ECART:\n", "        if False:\n")],
    "G12": [("operations_a_porter(operations, valeur, du, couture, ref[-1])", "operations_a_porter(operations, valeur, du, couture, ref[0])")],
    "G13": [("        if not du < o[0] <= fin:\n", "        if not du <= o[0] <= fin:\n")],
    "G14": [("        if p == RC.APPLIQUEE_PAR_YAHOO:\n            continue\n", "")],
    "G15": [("        if accord < K.PART_PROPRE or len(ref) < MIN_REFERENCE:", "        if len(ref) < MIN_REFERENCE:")],
    "G16": [("\n        suite = [(d, nouvelles[d][3]) for d in sorted(nouvelles)] + [(premier, y[premier][3])]\n",
             "\n        suite = [(d, nouvelles[d][3]) for d in sorted(nouvelles)]\n")],
    "G17": [("    comblees, refus = 0, []\n    cal = sorted(K.calendrier(series, seances))\n",
             "    comblees, refus = 0, []\n    figees = dict(sources)\n    cal = sorted(K.calendrier(series, seances))\n"),
            ("and sources.get((valeur, d)) != \"bnains\"]", "and figees.get((valeur, d)) != \"bnains\"]")],
    "G18": [("barre(b[d], f * a, k / a, K.divisions", "barre(b[d], f * a, 1.0, K.divisions")],
    "G19": [("for o in portees if d < o[0]),\n                           fv))", "for o in portees if d < o[0]),\n                           fp))")],
    "G20": [("        if not os.path.isfile(chemin_divisions):\n", "        if False:\n")],
    "G21": [("douteux, journal, operations,\n", "douteux, journal, {},\n")],
    "G22": [("                               os.path.join(racine, K.VERDICTS_YAHOO), officielles)[0]",
             "                               None, officielles)[0]")],
    # lot de comblement du 31-10-2026 (superviseur R-759, défauts 1, 2, 3, 5)
    "G32": [("        if p == RC.DOCUMENT and o[1] is not None and o[0] <= premier:\n",
             "        if p == RC.DOCUMENT and o[1] is not None:\n")],
    "G23": [("        if ref[0] != couture:\n", "        if False:\n")],
    "G24": [("        if abs(r0 / f - 1) > K.ECART:\n", "        if 1 - r0 / f > K.ECART:\n")],
    "G25": [("        if p == RC.DOCUMENT and o[1] is not None and o[0] <= premier:\n",
             "        if o[1] is not None and o[0] <= premier:\n")],
    "G26": [("        if p == RC.APPLIQUEE_PAR_YAHOO:\n", "        if p != RC.BNAINS_SEULE and p != RC.DOCUMENT:\n")],
    "G27": [("            a = porte(portees, d)\n", "            a = 1.0\n")],
    "G28": [("        if d < o[0]:\n            a *= o[1]\n", "        if d <= o[0]:\n            a *= o[1]\n")],
    "G29": [("RC", "    for r in officielles or []:\n", "    for r in []:\n")],
    "G30": [("RC", "            ops.setdefault(v, []).append((d, den / num, f\"division déclarée par Yahoo, {num:g} pour {den:g}\",\n                                          K.EVENEMENTS))",
             "            ops.setdefault(v, []).append((d, den / num, f\"division déclarée par Yahoo, {num:g} pour {den:g}\",\n                                          \"donnees/sources_yahoo/evenements.json\"))")],
    "G31": [("RC", "    if o[1] is None:\n        return RAPPORT_INCONNU\n", "")],
    # tour 3 (superviseur R-759 du 01-11-2026, d) : le X8b de la relecture du tour 2, sous un nom neuf ; G6 reste
    # n-1 de la relecture de Cowork du 13-11-2026 à 13h55 (m1, m2, m3) et m4 du superviseur R-759 : chaque terme ôté
    # de la garde d'arrêt doit être mordu par l'épreuve D9i de SA fonction
    "G34": [('    refus_des_comblements = refus_des_seances + refus_de_la_chaine + refus_des_debuts + refus_des_decidees\n',
             '    refus_des_comblements = refus_des_seances + refus_de_la_chaine + refus_des_debuts\n')],
    "G35": [('    refus_des_comblements = refus_des_seances + refus_de_la_chaine + refus_des_debuts + refus_des_decidees\n',
             '    refus_des_comblements = refus_de_la_chaine + refus_des_debuts + refus_des_decidees\n')],
    "G36": [('    refus_des_comblements = refus_des_seances + refus_de_la_chaine + refus_des_debuts + refus_des_decidees\n',
             '    refus_des_comblements = refus_des_seances + refus_des_debuts + refus_des_decidees\n')],
    "G37": [("    arrets += retirer(series, sources, bnains, evenements, journal)\n",
             "    retirer(series, sources, bnains, evenements, journal)\n")],
    # N-a du relecteur du 13-11-2026 (18h45) et verdict du superviseur R-759 (18h55) : le classement fermé
    "G38": [("    comblees, refus = {}, []\n", "    comblees, rejets = {}, []\n"),
            ('            refus.append(f"{valeur} : chaîne, la première ligne',
             '            rejets.append(f"{valeur} : chaîne, la première ligne'),
            ("            refus.append(arret)\n", "            rejets.append(arret)\n"),
            (" laissées\")\n    return comblees, refus\n", " laissées\")\n    return comblees, rejets\n"),
            ('    refus_des_comblements = refus_des_seances + refus_de_la_chaine + refus_des_debuts + refus_des_decidees\n',
             '    refus_des_comblements = refus_des_seances + refus_des_debuts + refus_des_decidees\n')],
    "G39": [("\ndef reparer(racine):\n",
             '\ndef fantome():\n    """Fabriquée par le sabotage G39.\n\n    ⑤ SORTIE — —\n      [refus: non — fabriquée]\n'
             '    ⑥ TRAITEMENT — —\n    """\n\n\ndef reparer(racine):\n')],
    "G40": [("      [refus: non — rend un texte]\n", "")],
    # M-1 du relecteur du 13-11-2026 à 20h06, mot pour mot, et verdict du superviseur R-759 de 20h12 : sabotage permanent
    "G41": [("pour `K.calendrier` (depuis le 27-10-2026).\n    ④ CONDITIONS D'ENTRÉE — —\n    ⑤ SORTIE — UNE valeur : la "
             "liste des raisons d'arrêt, vide si tout s'est fait.\n      [rend: 1]\n      [refus: dernier]\n",
             "pour `K.calendrier` (depuis le 27-10-2026).\n    ④ CONDITIONS D'ENTRÉE — —\n    ⑤ SORTIE — UNE valeur : la "
             "liste des raisons d'arrêt, vide si tout s'est fait.\n      [rend: 1]\n"
             "      [refus: non — rend les barres reconstruites]\n"),
            ("    arrets += retirer(series, sources, bnains, evenements, journal)\n",
             "    arrets = []\n    arrets += retirer(series, sources, bnains, evenements, journal)\n")],
    "G33": [('            sure = K.barre_sure(bnains, francfort or {}, valeur, d, douteux)\n            if not sure:\n'
             '                lignes.append((d, "non comblé", "", "", f"début de série absent chez Yahoo ; "',
             '            sure = d in b and K.barre_utilisable(bnains, valeur, d, frozenset())\n            if not sure:\n'
             '                lignes.append((d, "non comblé", "", "", f"début de série absent chez Yahoo ; "')],
}

# R-1 du relecteur M1 du 13-11-2026 (21h16) et voie V1 « FIGER » du superviseur R-759 (21h19) : la confrontation des
# deux témoins de D9i protégée SEULE. (a) G42 : la première paire de G41, seule — la marque ment, le code est intact.
SABOTAGES["G42"] = SABOTAGES["G41"][:1]
# (b) G43 : aucun texte de programme ; le harnais joue ce jeu avec une calibration faussée (`main`) : (rang de l'entrée
# de `CALIBRATION_DU_TEMOIN`, liste attendue fausse)
SABOTAGES["G43"] = []
CALIBRATIONS_FAUSSEES = {"G43": (0, ["f", "k"])}


def motifs(sortie, tombees):
    """Rend, pour chaque épreuve tombée, la ligne qu'elle a imprimée : le motif de son rouge.

    ① RÔLE — Montrer POURQUOI un sabotage mord, et pas seulement qu'il mord.
    ② CONTEXTE D'APPEL — `main`, après chaque sabotage.
    ③ ENTRÉE — `sortie` : le texte imprimé par `epreuves` sous ce sabotage · `tombees` : les clés des épreuves rouges.
    ④ CONDITIONS D'ENTRÉE — Chaque épreuve imprime ses lignes en commençant par sa clé (« D2 : … »), et `tenter`
      imprime « clé : Exception : … » quand elle plante.
    ⑤ SORTIE — UNE valeur : la liste des lignes « [clé] … », une par épreuve tombée ; « (aucune ligne imprimée) » quand
      l'épreuve n'a rien écrit.
      [rend: 1]
    ⑥ TRAITEMENT — Garder les lignes de `sortie` qui commencent, après les blancs, par la clé suivie d'une fin de mot.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du tour 2 (01-11-2026) : les 11 rouges de G6 étaient tous `KeyError : '2000-10-13'`, un
      plantage compté comme une morsure ; le relecteur a dû fabriquer des copies « bavardes » pour le voir.
    ⑨ CE QUI CLOCHE — Le motif est montré, il n'est pas jugé (BACKLOG, superviseur R-759 du 01-11-2026, d). « D3 » ne
      prend pas « D3b » ni « D3c » : la clé doit finir le mot. · La même fonction vit dans les trois jeux du lot
      (causes, comblement, débuts) : chaque jeu se lance seul ; une seule copie partagée serait à créer (BACKLOG).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    lignes = sortie.splitlines()
    rendu = []
    for e in tombees:
        a = [x.strip()[:400] for x in lignes if re.match(r"\s*" + re.escape(e) + r"(?![\w])", x)]
        rendu.append(f"    [{e}] " + (" || ".join(a) if a else "(aucune ligne imprimée)"))
    return rendu


def charger(sabotage=None):
    """Charge le contrôle puis la réparation (qui charge la reconstruction) — les vrais fichiers, ou des copies dont la
    réparation est sabotée."""
    dossier = PROGRAMMES
    if sabotage is not None:
        dossier = tempfile.mkdtemp()
        for nom in MODULES:
            shutil.copy(os.path.join(PROGRAMMES, nom + ".py"), dossier)
        for fichier in (REPARATION, RECONSTRUCTION):
            texte = open(fichier, encoding="utf-8").read()
            for cible, remplace in [p[-2:] for p in sabotage if (fichier == RECONSTRUCTION) == (len(p) == 3)]:
                texte = texte.replace(cible, remplace)
            open(os.path.join(dossier, os.path.basename(fichier)), "w", encoding="utf-8").write(texte)
    for nom in MODULES:
        sys.modules.pop(nom, None)
    sys.path.insert(0, dossier)
    try:
        sortie = []
        for nom in ("CONTROLER_L_HISTORIQUE_LONG", "REPARER_L_HISTORIQUE_LONG"):
            sp = importlib.util.spec_from_file_location(nom, os.path.join(dossier, nom + ".py"))
            m = importlib.util.module_from_spec(sp)
            sys.modules[nom] = m
            sp.loader.exec_module(m)
            sortie.append(m)
    finally:
        sys.path.remove(dossier)
    assert sortie[1].RC.K is sortie[0], "la reconstruction doit voir le même contrôle que la réparation"
    return sortie


def donnees(K):
    """Les vraies données du dépôt, lues par les fonctions du contrôle (R-708)."""
    series, defauts, _ = K.lire_cours(os.path.join(RACINE, K.ORIGINE))
    bnains, defauts_b, _ = K.lire_paris(RACINE)
    assert not defauts and not defauts_b
    evenements = json.load(open(os.path.join(RACINE, K.EVENEMENTS), encoding="utf-8"))
    detachements, _ = K.lire_detachements(os.path.join(RACINE, K.DROITS), os.path.join(RACINE, K.OFFICIELS))
    francfort = K.lire_francfort(os.path.join(RACINE, K.FRANCFORT))
    seances = K.CAL.lire_les_seances(RACINE)
    douteux = K.jours_douteux(K.ecarts(series, bnains))
    return series, bnains, evenements, detachements, francfort, seances, douteux


def jouer(R, D, debuts, abimer=None, divisions=None, officielles=None, verdicts=None, douteux_en_plus=()):
    """Joue `combler_les_debuts` sur une copie des données, avec la liste `debuts` et les opérations que la
    reconstruction calcule sur ces données (`R.RC.operations`, comme `reparer`) ; `divisions` remplace la table de
    bnains du dépôt, `officielles` la table des divisions prouvées par un document, `verdicts` le chemin des verdicts
    sur Yahoo ; `douteux_en_plus` s'ajoute aux jours douteux. Rend (comblées, refus, séries, sources, journal, barres
    de Paris utilisées)."""
    series, bnains, evenements, detachements, francfort, seances, douteux = copy.deepcopy(D)
    douteux = set(douteux) | set(douteux_en_plus)
    if abimer:
        series, bnains, evenements, detachements = abimer(series, bnains, evenements, detachements)
    if divisions is None:
        divisions = R.RC.lire_divisions(os.path.join(RACINE, R.RC.DIVISIONS))
    if officielles is None:
        officielles = R.RC.lire_divisions_officielles(os.path.join(RACINE, R.RC.OFFICIELLES))
    a_defaire = R.K.lire_a_defaire(os.path.join(RACINE, R.K.VERDICTS_YAHOO))
    operations = R.RC.operations(evenements, a_defaire, detachements, bnains, divisions,
                                 verdicts or os.path.join(RACINE, R.K.VERDICTS_YAHOO), officielles)[0]
    sources = {(v, d): "yahoo" for v, s in series.items() for d in s}
    journal = []
    R.DEBUTS_A_COMBLER = debuts
    with contextlib.redirect_stdout(io.StringIO()):
        n, refus = R.combler_les_debuts(series, sources, bnains, evenements, douteux, journal, operations, francfort,
                                        seances=seances)
    return n, refus, series, sources, journal, bnains


def racine_copiee(K, R, sans=()):
    """Une racine jetable avec les fichiers que la réparation déclare lire (`LU`, `DOSSIERS_LUS`) et le registre où
    elle s'inscrit, moins `sans`."""
    r = tempfile.mkdtemp()
    for c in (set(R.LU) | {K.PROVENANCE}) - set(sans):
        os.makedirs(os.path.join(r, os.path.dirname(c)), exist_ok=True)
        shutil.copy(os.path.join(RACINE, c), os.path.join(r, c))
    for d in getattr(R, "DOSSIERS_LUS", ()):      # les dossiers lus en entier (les bruts d'ABC, 31-10-2026)
        shutil.copytree(os.path.join(RACINE, d), os.path.join(r, d))
    return r


MARQUE_DE_REFUS = re.compile(r"^[ \t]*\[refus: (dernier|non — [^\]]+)\][ \t]*$", re.M)


def classement_des_refus(R):
    """Rend le classement FERMÉ des fonctions atteintes depuis `reparer` : les cibles de D9i et les deux écarts.

    ① RÔLE — Donner à D9i les fonctions dont un refus doit arrêter `reparer`, et faire rougir tout oubli de classement.
    ② CONTEXTE D'APPEL — `epreuves`, bloc D9i, une fois par jeu (Z0 et chaque sabotage).
    ③ ENTRÉE — `R` : le module de la réparation tel qu'il est chargé (le vrai, ou la copie sabotée).
    ④ CONDITIONS D'ENTRÉE — `R.__file__` est lisible et contient une fonction de premier niveau `reparer`.
    ⑤ SORTIE — TROIS valeurs, chacune une liste triée de noms : ① les cibles, fonctions atteintes marquées
      `[refus: dernier]` · ② les fonctions atteintes NON CLASSÉES (aucune marque dans leur ⑤, ou plusieurs) · ③ les
      fonctions marquées qui ne sont PAS atteintes. Le classement est juste quand ② et ③ sont vides.
      [rend: 3]
    ⑥ TRAITEMENT — Lire l'arbre syntaxique du fichier ; partir de `reparer` et descendre, appel par nom après appel
      par nom, dans les fonctions de premier niveau du module (l'ensemble ATTEINT) ; lire dans le ⑤ de chaque
      fonction du module (entre la ligne « ⑤ SORTIE » et la ligne « ⑥ TRAITEMENT ») la marque `[refus: …]`, sur le
      modèle de `[rend: …]` ; comparer l'ensemble atteint à l'ensemble marqué dans les deux sens. Le 13-11-2026 :
      21 atteintes, 6 cibles (combler_les_debuts, combler_les_seances, combler_les_seances_decidees,
      combler_par_raccords, reconstruire, retirer), aucun écart.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-a du relecteur du 13-11-2026 à 18h45 : la découverte précédente reposait sur le NOM de la liste
      rendue (`refus`, `arrets`) et sa garde sur un COMPTE (liste non vide) ; renommer `refus` en `rejets` dans
      `combler_par_raccords` et ôter son terme de la somme (mutant M1) laissait tout vert, code 0. Le superviseur
      R-759 de 18h55 a retenu un classement FERMÉ de tous les appelés, sans filtre « rend une liste » (deviner sans
      exécuter qu'une fonction rend une liste est fragile), contrôlé dans les deux sens (sinon la liste pourrit sans
      bruit), la marque posée près de la fonction pour qu'elle suive un renommage.
    ⑨ CE QUI CLOCHE — Seule, une marque `non` posée à tort sur un geste qui refuse n'est pas vue ici : le sens d'une
      liste ne se devine pas, il se déclare. Depuis le 13-11-2026 (superviseur R-759 de 20h12, M-1), la garde D9i
      confronte ce classement au témoin du code (`alimentation_des_arrets`) : une fonction qui alimente un arrêt de
      `reparer` et n'est pas marquée `dernier` fait rougir. CE QUI RESTE OUVERT (R-2 du relecteur M1 du 13-11-2026) : il
      ne faut pas deux mensonges coordonnés, UN REFACTOR CORRECT SUIVI DE L'OBÉISSANCE AU ROUGE SUFFIT à rendre un arrêt
      muet — porter l'appel dans une forme que le témoin du code ne lit pas (`.extend`, `:=`, `sys.exit`… : liste au ⑨
      de `alimentation_des_arrets`), puis, la garde ayant rougi, marquer la fonction `non`. Le message de la garde dit
      de ne pas toucher la marque et de vérifier l'arbre. Aucune forme statique ne ferme davantage, et le témoin n'est
      pas élargi (superviseur R-759 du 13-11-2026 à 21h19, voie V1 « FIGER »). LA CONFRONTATION ET L'UNION SE MASQUENT
      L'UNE L'AUTRE (R-4 du relecteur M1) : sans l'union, G41 mord encore par la confrontation ; sans la confrontation,
      G41 mord encore par D9i_reconstruire. G42 (une marque seule fausse) et G43 (la calibration faussée) protègent la
      confrontation SEULE, et dans UN SEUL de ses deux sens : G42 protège le sens « alimente sans marque dernier »
      (`alimentent_sans_dernier`) ; le sens « marquée dernier sans arrêt » (`dernier_sans_arret`) est masqué par les
      épreuves de comportement D9i_<f>, comme l'union (V1-a de Cowork du 13-11-2026 à 23h37 : son mutant qui retire ce
      seul terme laisse les dix sabotages G34 à G43 mordre). Ce n'est pas un trou de détection — le comportement le
      voit —, aucune garde ni aucun sabotage n'est ajouté. Rien ne protège l'union seule (son retrait n'a pas été rejoué). Avant cette confrontation (mesuré par le relecteur le
      13-11-2026), la protection contre une marque `non` à tort tenait, pour 5 cibles sur 6, à des gardes voisines
      (ancres de G34-G38, D9b), et pour `reconstruire` à rien. Les appels par attribut (`K.x`, `RC.x`, `K.CAL.x` : 16 le 13-11-2026, dont
      `K.lire_cours`, `K.lire_paris`, `K.lire_detachements`, qui rendent des listes de défauts) et les appels par
      une variable ne sont pas classés : BACKLOG proposé dans la note de livraison. Une marque doit tenir sur une
      ligne.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    arbre = ast.parse(open(R.__file__, encoding="utf-8").read())
    fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}

    def appelees(nom):
        return {n.func.id for n in ast.walk(fonctions[nom])
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in fonctions}
    atteintes, a_voir = set(), ["reparer"]
    while a_voir:
        for c in appelees(a_voir.pop()) - atteintes - {"reparer"}:
            atteintes.add(c)
            a_voir.append(c)

    def marques(nom):
        doc = ast.get_docstring(fonctions[nom], clean=False) or ""
        cinq = re.search(r"(?ms)^\s*⑤ SORTIE.*?(?=^\s*⑥ TRAITEMENT)", doc)
        return MARQUE_DE_REFUS.findall(cinq.group(0)) if cinq else []
    toutes = {n: marques(n) for n in fonctions if n != "reparer"}
    cibles = sorted(n for n in atteintes if toutes[n] == ["dernier"])
    non_classees = sorted(n for n in atteintes if len(toutes[n]) != 1)
    non_atteintes = sorted(n for n in toutes if toutes[n] and n not in atteintes)
    return cibles, non_classees, non_atteintes


def alimentation_des_arrets(source):
    """Rend, lu dans l'arbre de `reparer`, ses puits d'arrêt et les fonctions du module qui les alimentent.

    ① RÔLE — Le TÉMOIN DU CODE de D9i : ce qui arrête vraiment la réparation, lu dans le code et non dans une marque.
    ② CONTEXTE D'APPEL — `epreuves`, bloc D9i, une fois par jeu sur le vrai fichier de la réparation, et sur les trois
      sources fabriquées de la calibration (`CALIBRATION_DU_TEMOIN`).
    ③ ENTRÉE — `source` : le texte d'un module Python qui définit, au premier niveau, une fonction `reparer`.
    ④ CONDITIONS D'ENTRÉE — `source` se lit par `ast.parse` et définit `reparer` au premier niveau.
    ⑤ SORTIE — DEUX valeurs : ① la liste des puits, chacun (numéro de ligne du `if`, liste triée des variables de son
      test) · ② la liste triée des fonctions de premier niveau du module qui alimentent au moins un puits.
      [rend: 2]
      [refus: non — rend des noms, que la garde D9i confronte aux marques]
    ⑥ TRAITEMENT — Un PUITS est un `if X:` du corps de `reparer` dont le corps contient un appel `print` d'un texte
      commençant par « ARRÊT » et un `return 1`. Pour chaque variable lue par X, relever TOUTES ses liaisons dans
      `reparer`, quel que soit leur ordre (`v = …`, `v += …`, et `…, v = …` quand v est le DERNIER élément d'un tuple) ;
      dans la valeur liée : un appel d'une fonction du module la retient ; une somme `a + b` est descendue des deux
      côtés ; un nom de variable est remonté à son tour (une fois chacun). Toute autre forme (compréhension, appel par
      attribut, littéral) n'alimente rien.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — M-1 du relecteur du 13-11-2026 à 20h06 et verdict du superviseur R-759 de 20h12 : les quatre tours
      précédents prenaient pour autorité une chose DÉCLARÉE (un nom de somme, un nom de liste, une marque) que
      personne ne confrontait au code. Toutes les liaisons, sans ordre : `arrets = []` posé après
      `arrets = reconstruire(…)` n'efface pas `reconstruire` du témoin, c'est la garde D9i_reconstruire qui voit que
      ses arrêts sont jetés. Un `return 2` n'est pas un puits : ce sont les arrêts de lecture, avant tout geste.
    ⑨ CE QUI CLOCHE — Un appel sorti de tout puits (`reconstruire(…)` nu) n'alimente plus rien : seul, ce n'est vu que
      si la fonction reste marquée `dernier`. Il ne faut PAS deux mensonges pour rendre un arrêt muet (R-2 du relecteur
      M1 du 13-11-2026) : un refactor CORRECT vers une forme que ce témoin ne lit pas — liaisons `a.extend(f())`,
      `a: list = f()`, `(a := f())`, `[*f()]`, `list(f())`, `x, *a = f()` ; puits `sys.exit(1)`,
      `print('ARRÊT — ' + x)`, `code = 1 ; return code`, `return 1` hors du `if`, `if f():` — fait sortir la fonction
      du témoin ; la garde rougit alors à tort, et OBÉIR à ce rouge en passant la marque à `non` rend l'arrêt muet
      (D9i_<f> n'est plus joué). Le message de la garde dit de vérifier l'arbre et de ne pas toucher la marque. Le témoin
      n'est PAS élargi à ces formes (superviseur R-759 du 13-11-2026 à 21h19, voie V1 « FIGER » : ce serait une
      rustine). Il sur-détecte aussi (un `if` qui englobe un puits, un `return 1` d'une fonction imbriquée,
      `if False: return 1`) : sans danger, l'union n'ajoute que des cibles D9i_, que l'épreuve de comportement tranche.
      Les puits hors de `reparer`, ceux nourris par une compréhension
      (`trous`) ou par un appel par attribut (`K.x`) ne sont pas suivis. Un texte d'arrêt qui ne commence pas par
      « ARRÊT » n'est pas un puits.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir : chaque variable est remontée une fois.
    """
    arbre = ast.parse(source)
    fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
    rep_ = fonctions["reparer"]

    def texte_d_arret(n):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print" and n.args):
            return False
        a = n.args[0]
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            return a.value.startswith("ARRÊT")
        return (isinstance(a, ast.JoinedStr) and bool(a.values) and isinstance(a.values[0], ast.Constant)
                and str(a.values[0].value).startswith("ARRÊT"))
    puits = []
    for n in ast.walk(rep_):
        if isinstance(n, ast.If):
            corps = [x for b in n.body for x in ast.walk(b)]
            if (any(texte_d_arret(x) for x in corps)
                    and any(isinstance(x, ast.Return) and isinstance(x.value, ast.Constant) and x.value.value == 1
                            for x in corps)):
                puits.append((n.lineno, sorted({x.id for x in ast.walk(n.test) if isinstance(x, ast.Name)})))
    liaisons = {}
    for n in ast.walk(rep_):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    liaisons.setdefault(t.id, []).append(n.value)
                elif isinstance(t, ast.Tuple) and t.elts and isinstance(t.elts[-1], ast.Name) and isinstance(n.value, ast.Call):
                    liaisons.setdefault(t.elts[-1].id, []).append(n.value)
        elif isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name) and isinstance(n.op, ast.Add):
            liaisons.setdefault(n.target.id, []).append(n.value)
    alimentent, vues, a_voir = set(), set(), [v for _, vs in puits for v in vs]

    def descendre(valeur):
        if isinstance(valeur, ast.Call) and isinstance(valeur.func, ast.Name) and valeur.func.id in fonctions:
            alimentent.add(valeur.func.id)
        elif isinstance(valeur, ast.BinOp) and isinstance(valeur.op, ast.Add):
            descendre(valeur.left)
            descendre(valeur.right)
        elif isinstance(valeur, ast.Name):
            a_voir.append(valeur.id)
    while a_voir:
        v = a_voir.pop()
        if v in vues:
            continue
        vues.add(v)
        for valeur in liaisons.get(v, []):
            descendre(valeur)
    return sorted(puits), sorted(alimentent - {"reparer"})


# La calibration du témoin du code (consigne du 13-11-2026 : un motif se calibre sur un cas connu ET sur un cas qui
# doit échouer). Chaque entrée : (source fabriquée, fonctions qui doivent alimenter). ① trouve : les quatre formes de
# liaison (appel, `+=`, somme, dernier élément d'un tuple), une variable écrasée après coup (`a = []`) qui n'efface
# pas, et un appel hors puits (`h`) ou au premier élément d'un tuple (`g`) qui n'alimente pas · ② ne doit rien
# trouver : un `return 2` (arrêt de lecture) et un `if` qui imprime un autre texte · ③ ne doit rien trouver : l'appel
# réduit à `f(...)` nu, le cas G37.
CALIBRATION_DU_TEMOIN = (
    ("def f():\n    return []\ndef g():\n    return [], []\ndef h():\n    return []\ndef k():\n    return []\n"
     "def m():\n    return []\n"
     "def reparer(r):\n    a = f()\n    a = []\n    a += k()\n    x, y = g()\n    y, z = m()\n    h()\n"
     "    s = a + z\n    if s:\n        for t in s:\n            print(f\"ARRÊT — {t}\")\n        return 1\n    return 0\n",
     ["f", "k", "m"]),
    ("def f():\n    return []\ndef g():\n    return []\n"
     "def reparer(r):\n    a = f()\n    if a:\n        print(f\"ARRÊT — {a}\")\n        return 2\n"
     "    b = g()\n    if b:\n        print(\"attention\")\n        return 1\n    return 0\n",
     []),
    ("def f():\n    return []\n"
     "def reparer(r):\n    a = []\n    f()\n    if a:\n        print(f\"ARRÊT — {a}\")\n        return 1\n    return 0\n",
     []),
)


def ligne_de_bnains(valeur, date, diviseur, commentaire):
    """Une ligne FABRIQUÉE de la table des divisions de bnains, aux champs de la vraie table."""
    vraie = R0_DIVISIONS[0]
    return dict(vraie, valeur=valeur, date=date, diviseur=diviseur, commentaire=commentaire + " (FABRIQUÉ)")


def fois(serie, facteur, garde=lambda d: True):
    """Une série dont les prix des jours gardés sont multipliés par `facteur` et le volume divisé d'autant."""
    return {d: ((o * facteur, h * facteur, l * facteur, c * facteur, v / facteur) if garde(d) else (o, h, l, c, v))
            for d, (o, h, l, c, v) in serie.items()}


def epreuves(K, R):
    res = {}
    D = donnees(K)
    lignes = lambda j, v, g: [l for l in j if l[0] == v and l[2] == g]
    decision = "décision écrite pour l'épreuve"
    AIR = (("AIRBUS", "2000-07-10", decision),)

    def tenter(cle, f):
        try:
            res[cle] = bool(f())
        except Exception as e:
            print(f"      {cle} : {type(e).__name__} : {e}")
            res[cle] = False

    # D1
    def d1():
        n, refus, s, src, j, b = jouer(R, D, (("THALES", "2000-01-03", decision),))
        c = lignes(j, "THALES", "comblé")
        attendu = round(b["THALES"]["2000-01-03"][3], K.DECIMALES)
        return (n == 1 and not refus and len(c) == 1 and c[0][1] == "2000-01-03" and c[0][3] == ""
                and c[0][8] == "paris" and s["THALES"]["2000-01-03"][3] == attendu == c[0][4]
                and src[("THALES", "2000-01-03")] == "bnains")
    tenter("D1", d1)

    # D2
    def d2():
        n, refus, s, src, j, b = jouer(R, D, AIR)
        cal = [d for d in sorted(K.calendrier(D[0], D[5])) if "2000-07-10" <= d < "2001-09-03"]
        comb = {l[1] for l in lignes(j, "AIRBUS", "comblé")}
        non = {l[1]: l[6] for l in lignes(j, "AIRBUS", "non comblé")}
        venues = {d for d in s["AIRBUS"] if d < "2001-09-03"}
        _, bn, _, _, fr, _, dt = D
        print(f"      D2 : AIRBUS {len(comb)} comblées, {len(non)} non comblées {sorted(non)}")
        return (not refus and n == len(comb) == len(venues) and comb == venues and not (comb & set(non))
                and comb | set(non) == set(cal) and len(cal) == 292
                and "pas de barre chez bnains" in non.get("2000-10-13", "")
                and all(K.barre_sure(bn, fr, "AIRBUS", d, dt) for d in comb)
                and all(src[("AIRBUS", d)] == "bnains" for d in comb))
    tenter("D2", d2)

    # les arrêts : un seul refus, qui contient chaque mot attendu, et rien d'écrit
    def arret(cle, debuts, mots, abimer=None, divisions=None, officielles=None, verdicts=None, douteux_en_plus=()):
        def f():
            n, refus, s, src, j, _ = jouer(R, D, debuts, abimer, divisions, officielles, verdicts, douteux_en_plus)
            avant = copy.deepcopy(D[0])
            if abimer:
                avant = abimer(copy.deepcopy(D[0]), copy.deepcopy(D[1]), copy.deepcopy(D[2]), copy.deepcopy(D[3]))[0]
            print(f"      {cle} : {refus}")
            return n == 0 and len(refus) == 1 and all(m in refus[0] for m in mots) and not j and s == avant
        tenter(cle, f)

    tout = R.RC.lire_divisions(os.path.join(RACINE, R.RC.DIVISIONS))
    sans_stm = [r for r in tout if not (r["valeur"] == "STMICROELECTRONICS" and r["date"] == "2000-05-09")]
    assert len(sans_stm) == len(tout) - 1
    STM = (("STMICROELECTRONICS", "2000-01-03", decision),)

    def marche(s, b, v, avant, jour):
        """Le rapport (courbe ÷ Paris brut) du jour d'avant divisé par celui du jour : la marche que la courbe porte."""
        return (s[v][avant][3] / b[v][avant][3]) / (s[v][jour][3] / b[v][jour][3])

    def d3():
        n, refus, s, src, j, b = jouer(R, D, STM)
        comb = {l[1] for l in lignes(j, "STMICROELECTRONICS", "comblé")}
        avant = {d for d in comb if d < "2000-05-09"}
        m = marche(s, b, "STMICROELECTRONICS", "2000-05-08", "2000-05-09")
        print(f"      D3 : {n} comblées, {len(avant)} avant le 09-05-2000, marche {m!r}, refus {refus}")
        return (not refus and len(avant) == 88 and abs(m * 3 - 1) <= K.MARCHE_EXACTE
                and all(src[("STMICROELECTRONICS", d)] == "bnains" for d in comb)
                and all("portée" in l[6] for l in lignes(j, "STMICROELECTRONICS", "comblé") if l[1] < "2000-05-09"))
    tenter("D3", d3)
    arret("D3c", STM, ("opération connue", "2000-05-09", "DIVISIONS_BNAINS", "bnains seul"), officielles=[])
    arret("D3b", STM, ("saut de plus de", "2000-05-08→2000-05-09"), divisions=sans_stm, officielles=[])
    arret("D4", (("UNIBAIL-RODAMCO-WESTFIELD", "2007-06-18", decision),), ("(0 séances communes",))

    def detachement(series, bnains, evenements, detachements):
        detachements = dict(detachements)
        detachements["AIRBUS"] = {"2001-01-15": ("document", 20.0, 0, 9)}
        return series, bnains, evenements, detachements
    def d5():
        n, refus, s, src, j, b = jouer(R, D, AIR, detachement)
        m = marche(s, b, "AIRBUS", "2001-01-12", "2001-01-15")
        print(f"      D5 : {n} comblées, marche du 12 au 15-01-2001 {m!r}, refus {refus}")
        # 291 (avant le 13-11-2026 : 290) — A-752 ⑥ ; preuve : etudes/VINGT_ANS_A_PART_Mer_11-11-2026/sorties/
        # SORTIE_E2c_GEL_verification_independante_de_D5_et_D21.txt (le 19-06-2001 gagné, barre du fichier bnains du 20)
        return not refus and n == 291 and abs(m / 0.9 - 1) <= K.MARCHE_EXACTE
    tenter("D5", d5)

    # D6
    def d6():
        def moitie(series, bnains, evenements, detachements):
            series["AIRBUS"] = fois(series["AIRBUS"], 0.5)
            return series, bnains, evenements, detachements
        n, refus, s, src, j, b = jouer(R, D, AIR, moitie)
        comb = lignes(j, "AIRBUS", "comblé")
        return (not refus and len(comb) > 200
                and all(s["AIRBUS"][l[1]][3] == round(b["AIRBUS"][l[1]][3] * 0.5, K.DECIMALES) for l in comb)
                and all(s["AIRBUS"][l[1]][4] == b["AIRBUS"][l[1]][4] * 2 for l in comb)
                and all(l[5] == 0.5 and l[7] == 2.0 for l in comb))
    tenter("D6", d6)

    # D7
    def d7():
        def division(series, bnains, evenements, detachements):
            evenements = dict(evenements)
            evenements["AIRBUS"] = {"divisions": [["2001-01-02", 2, 1]]}
            bnains["AIRBUS"] = {d: ((o * 2, h * 2, l * 2, c * 2, v / 2) if d < "2001-01-02" else (o, h, l, c, v))
                                for d, (o, h, l, c, v) in bnains["AIRBUS"].items()}
            return series, bnains, evenements, detachements
        n, refus, s, src, j, b = jouer(R, D, AIR, division)
        comb = [l[1] for l in lignes(j, "AIRBUS", "comblé")]
        avant_div = [d for d in comb if d < "2001-01-02"]
        if refus:
            print(f"      D7 : {refus}")
        return (not refus and len(avant_div) > 100
                and all(s["AIRBUS"][d][3] == round(b["AIRBUS"][d][3] / 2, K.DECIMALES) for d in avant_div))
    tenter("D7", d7)

    def d7r():
        ancien = R.K.EVENEMENTS
        try:
            R.K.EVENEMENTS = os.path.join("donnees", "sources_yahoo", "EVENEMENTS_RENOMMES_POUR_L_EPREUVE.json")
            return d7()
        finally:
            R.K.EVENEMENTS = ancien
    tenter("D7r", d7r)

    # D8, D9, D16 : la réparation entière, sur une copie des fichiers qu'elle lit, lancée depuis un dossier vide
    def entiere(cle, debuts, sans=(), retouche=None):
        def f():
            r, vide, ici = racine_copiee(K, R, sans), tempfile.mkdtemp(), os.getcwd()
            if retouche is not None:
                retouche(r)
            liste = R.DEBUTS_A_COMBLER
            try:
                R.DEBUTS_A_COMBLER = R._LISTE_DECIDEE if debuts is None else debuts
                sortie = io.StringIO()
                os.chdir(vide)       # la réparation ne doit dépendre d'aucun dossier courant (piège T1)
                with contextlib.redirect_stdout(sortie):
                    code = R.reparer(r)
            finally:
                os.chdir(ici)
                R.DEBUTS_A_COMBLER = liste
            out = sortie.getvalue()
            ecrits = [os.path.exists(os.path.join(r, c)) for c in (R.SORTIE, R.JOURNAL)]
            try:
                if cle == "D8":
                    lire = lambda p: [l for l in open(p, encoding="utf-8").read().splitlines() if "début de série" in l]
                    ici_, depot = lire(os.path.join(r, R.JOURNAL)), lire(os.path.join(RACINE, R.JOURNAL))
                    print(f"      D8 : code {code}, {len(ici_)} lignes de début de série au journal, {len(depot)} au dépôt")
                    return code == 0 and all(ecrits) and ici_ == depot and len(ici_) > 600
                if cle == "D9":
                    print(f"      D9 : code {code}, fichiers écrits {ecrits}, " + " | ".join(
                        x for x in out.splitlines() if x.startswith("ARRÊT"))[:300])
                    return code == 2 and R.RC.OFFICIELLES in out and not any(ecrits)
                if cle == "D9b":
                    arrets = [x for x in out.splitlines() if x.startswith("ARRÊT")]
                    debut = [x for x in arrets if x.startswith("ARRÊT — STMICROELECTRONICS : début de série")
                             and "rapport pris de bnains seul" in x]
                    table = os.path.exists(os.path.join(r, R.RC.OFFICIELLES))
                    print(f"      D9b : code {code}, table officielle présente {table}, fichiers écrits {ecrits}, "
                          f"arrêt du début de série {len(debut)} · " + " | ".join(arrets)[:300])
                    return (code == 1 and table and len(debut) == 1 and "rien n'est écrit" in out.splitlines()
                            and not any(ecrits))
                print(f"      D16 : code {code}, fichiers écrits {ecrits}, {out.strip()[:200]}")
                return code == 2 and R.RC.DIVISIONS in out and not any(ecrits)
            finally:
                shutil.rmtree(r, ignore_errors=True)
                shutil.rmtree(vide, ignore_errors=True)
        tenter(cle, f)
    entiere("D8", None)
    entiere("D9", STM, sans=(R.RC.OFFICIELLES,))

    # D9b : la table officielle gardée, privée de sa ligne de STMicro — la réparation entière passe par sa garde d'arrêt
    def sans_la_ligne_de_stmicro(r):
        chemin = os.path.join(r, R.RC.OFFICIELLES)
        with open(chemin, encoding="utf-8", newline="") as f:
            lecteur = csv.DictReader(f)
            champs, gardees = lecteur.fieldnames, [l for l in lecteur if l["valeur"] != "STMICROELECTRONICS"]
        with open(chemin, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=champs, lineterminator="\n")
            w.writeheader()
            w.writerows(gardees)
    entiere("D9b", STM, retouche=sans_la_ligne_de_stmicro)

    # D9i : la propriété « tout refus rendu par un geste de la réparation l'arrête », sans énumérer les gestes
    cibles, non_classees, non_atteintes = classement_des_refus(R)
    puits, alimentent = alimentation_des_arrets(open(R.__file__, encoding="utf-8").read())
    calibration = [alimentation_des_arrets(src)[1] == attendu for src, attendu in CALIBRATION_DU_TEMOIN]
    # la confrontation des deux témoins (superviseur R-759 du 13-11-2026 à 20h12, M-1)
    alimentent_sans_dernier = sorted(set(alimentent) - set(cibles))
    dernier_sans_arret = sorted(set(cibles) - set(alimentent))
    print(f"      D9i : gestes repérés {cibles} · atteintes non classées {non_classees} · marquées non atteintes "
          f"{non_atteintes} · témoin sans ajout (D8) vert {res.get('D8') is True}")
    print(f"      D9i témoin du code : puits {puits} · alimentent {alimentent} · alimentent sans marque dernier "
          f"{alimentent_sans_dernier} · marquées dernier sans arrêt {dernier_sans_arret} · calibration {calibration}")
    if alimentent_sans_dernier or dernier_sans_arret:
        # R-2 du relecteur M1 du 13-11-2026 : le rouge peut venir d'un refactor honnête ; y obéir en passant la marque à
        # `non` rendrait l'arrêt muet
        print("      D9i DÉSACCORD : une marque fausse, ou une forme que le témoin du code ne lit pas (.extend, :=, "
              "sys.exit…) — NE PAS passer la marque à non ; vérifier l'arbre")
    # la garde du classement : FERMÉ dans les deux sens (N-a, superviseur R-759 du 13-11-2026) ; vide, la propriété
    # ne serait éprouvée sur rien ; sans témoin vert, un code 1 ne prouverait pas que c'est le refus ajouté qui arrête ;
    # les deux témoins doivent concorder, et le témoin du code doit tenir sa calibration
    res["D9i"] = (bool(cibles) and bool(puits) and bool(alimentent) and not non_classees and not non_atteintes
                  and res.get("D8") is True and not alimentent_sans_dernier and not dernier_sans_arret
                  and all(calibration))

    def injecter(cible):
        """Joue la réparation entière, la liste décidée, avec un refus marqué ajouté à ce que rend `cible`.

        ① RÔLE — Une dent par geste de la réparation : son refus doit arrêter l'écriture.
        ② CONTEXTE D'APPEL — `epreuves`, une fois par cible rendue par `classement_des_refus`.
        ③ ENTRÉE — `cible` : le nom d'une fonction de premier niveau de `R`.
        ④ CONDITIONS D'ENTRÉE — `R.<cible>` rend une liste, ou un tuple dont le dernier élément est une liste.
        ⑤ SORTIE — UNE valeur : vrai si code 1, une ligne « ARRÊT — <marque> », une ligne « rien n'est écrit », ni
          le fichier réparé ni le journal dans la copie, et la fonction appelée avec un rendu de la forme attendue.
          [rend: 1]
        ⑥ TRAITEMENT — Envelopper `R.<cible>` (les appels de `reparer` passent par les globales du module), copier
          les fichiers lus (`racine_copiee`), lancer `R.reparer` depuis un dossier vide, rétablir la fonction.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — n-1 de la relecture de Cowork du 13-11-2026 à 13h55 : trois des quatre termes de la somme des
          refus pouvaient être ôtés sans qu'aucune épreuve rougisse, et la réparation ÉCRIVAIT alors, code 0.
        ⑨ CE QUI CLOCHE — Le refus est ajouté APRÈS le geste : un geste qui lèverait avant de rendre n'est pas
          éprouvé ici (D9, D16 éprouvent les levées).
        ⑩ EFFET — Crée et efface une copie ; remplace un instant une fonction du module chargé.
        ⑪ TERMINAISON — Rend la main. `R.reparer` peut-il ne pas revenir ? Non : il n'a pas de boucle ouverte.
        """
        marque = f"INJECTÉ PAR L'ÉPREUVE D9i dans {cible}"
        vraie, vu = getattr(R, cible), []

        def piegee(*a, **k):
            rendu = vraie(*a, **k)
            if isinstance(rendu, list):
                vu.append("liste")
                return rendu + [marque]
            if isinstance(rendu, tuple) and rendu and isinstance(rendu[-1], list):
                vu.append("tuple")
                return (*rendu[:-1], rendu[-1] + [marque])
            vu.append(f"forme inattendue {type(rendu).__name__}")
            return rendu
        r, vide, ici, liste = racine_copiee(K, R), tempfile.mkdtemp(), os.getcwd(), R.DEBUTS_A_COMBLER
        try:
            setattr(R, cible, piegee)
            R.DEBUTS_A_COMBLER = R._LISTE_DECIDEE
            sortie = io.StringIO()
            os.chdir(vide)
            with contextlib.redirect_stdout(sortie):
                code = R.reparer(r)
            out = sortie.getvalue().splitlines()
            ecrits = [os.path.exists(os.path.join(r, c)) for c in (R.SORTIE, R.JOURNAL)]
        finally:
            os.chdir(ici)
            setattr(R, cible, vraie)
            R.DEBUTS_A_COMBLER = liste
            shutil.rmtree(r, ignore_errors=True)
            shutil.rmtree(vide, ignore_errors=True)
        vue = f"ARRÊT — {marque}" in out
        print(f"      D9i_{cible} : code {code}, fichiers écrits {ecrits}, marque arrêtée {vue}, appels {vu}")
        return (code == 1 and vue and "rien n'est écrit" in out and not any(ecrits)
                and bool(vu) and all(x in ("liste", "tuple") for x in vu))
    for cible in sorted(set(cibles) | set(alimentent)):   # l'union : le code choisit, la marque n'en retire aucune
        tenter(f"D9i_{cible}", lambda c=cible: injecter(c))

    # D10 : P1, un ajustement de Yahoo que personne ne déclare, tôt dans la référence
    def a_prime(series, bnains, evenements, detachements):
        series["AIRBUS"] = fois(series["AIRBUS"], 0.9, lambda d: d < "2001-09-05")
        return series, bnains, evenements, detachements
    arret("D10", AIR, ("à la couture le 2001-09-03",), a_prime)

    # D11 : P2, une opération que bnains déclare, dans la zone à combler
    def b_prime(series, bnains, evenements, detachements):
        bnains["AIRBUS"] = fois(bnains["AIRBUS"], 1.1, lambda d: d < "2001-01-15")
        return series, bnains, evenements, detachements
    arret("D11", AIR, ("opération connue", "2001-01-15", "DIVISIONS_BNAINS"), b_prime,
          tout + [ligne_de_bnains("AIRBUS", "2001-01-15", "1.1", "une action gratuite pour dix")])

    # D12 : P2, borne haute — une opération déclarée dans la référence, sans trace dans les cours
    arret("D12", AIR, ("opération connue", "2001-12-03"), None,
          tout + [ligne_de_bnains("AIRBUS", "2001-12-03", "1.1", "une action gratuite pour dix")])

    # D13 : l'accord — 15 séances de la référence décalées de 1 %
    _, bn, _, _, _, _, dt = D
    ref_air = [d for d in sorted(D[0]["AIRBUS"]) if d in bn["AIRBUS"] and d not in dt][:100]
    decalees = set(ref_air[10:25])
    def instable(series, bnains, evenements, detachements):
        series["AIRBUS"] = fois(series["AIRBUS"], 1.01, lambda d: d in decalees)
        return series, bnains, evenements, detachements
    arret("D13", AIR, ("instable", "accord 8"), instable)

    # D14 : un saut à la seule couture — les barres de Paris d'avant la première ligne de Yahoo × 1,5, que rien ne déclare
    def couture(series, bnains, evenements, detachements):
        bnains["AIRBUS"] = fois(bnains["AIRBUS"], 1.5, lambda d: d < "2001-09-03")
        return series, bnains, evenements, detachements
    arret("D14", AIR, ("saut de plus de", "2001-08-31→2001-09-03"), couture)

    # D17 : le cas C2 — la barre de Paris de la couture ôtée, Yahoo × 0,9 avant le 04-09-2001, déclaré par personne
    def c2(series, bnains, evenements, detachements):
        del bnains["AIRBUS"]["2001-09-03"]
        series["AIRBUS"] = fois(series["AIRBUS"], 0.9, lambda d: d < "2001-09-04")
        return series, bnains, evenements, detachements
    arret("D17", AIR, ("non à la couture", "2001-09-04", "2001-09-03"), c2)
    # D18 : la couture est un jour douteux
    arret("D18", AIR, ("non à la couture", "2001-09-03"), douteux_en_plus=("2001-09-03",))
    # D19 : P1 dans l'autre sens — Yahoo × 1,1 avant le 05-09-2001
    def x1(series, bnains, evenements, detachements):
        series["AIRBUS"] = fois(series["AIRBUS"], 1.1, lambda d: d < "2001-09-05")
        return series, bnains, evenements, detachements
    arret("D19", AIR, ("à la couture le 2001-09-03",), x1)
    # D20 : un ajustement caché de Yahoo (« aucune déclaration », facteur non documenté) FABRIQUÉ dans la zone
    verdicts_faux = os.path.join(tempfile.mkdtemp(), "AJUSTEMENTS_DE_YAHOO.csv")
    with open(os.path.join(RACINE, R.K.VERDICTS_YAHOO), encoding="utf-8", newline="") as f:
        lus = list(csv.DictReader(f))
    with open(verdicts_faux, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lus[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(lus + [dict({c: "" for c in lus[0]}, valeur="AIRBUS", date="2001-01-15",
                                ce_que_yahoo_declare="aucune déclaration (FABRIQUÉ pour l'épreuve)")])
    arret("D20", AIR, ("opération connue", "2001-01-15", "rapport inconnu"), verdicts=verdicts_faux)

    # D21 : la borne basse de P2 est exclue — STMICROELECTRONICS demandée dès le 09-05-2000, sans la table officielle :
    # la division de bnains du 09-05-2000 ne touche que les séances d'avant, rien n'arrête
    def d21():
        n, refus, s, src, j, b = jouer(R, D, (("STMICROELECTRONICS", "2000-05-09", decision),), officielles=[])
        print(f"      D21 : {n} comblées, refus {refus}")
        # 333 (avant le 13-11-2026 : 331) — A-752 ⑥ ; preuve : etudes/VINGT_ANS_A_PART_Mer_11-11-2026/sorties/
        # SORTIE_E2c_GEL_verification_independante_de_D5_et_D21.txt (les 19 et 20-06-2001 gagnés, barres échangées)
        return not refus and n == 333
    tenter("D21", d21)

    # D22 : une opération DOCUMENTÉE datée APRÈS la couture, dans la référence, arrête (relecture du lot, D4)
    def document_dans_la_reference(series, bnains, evenements, detachements):
        detachements = dict(detachements)
        detachements["AIRBUS"] = {"2001-12-03": ("document", 20.0, 0, 9)}
        return series, bnains, evenements, detachements
    arret("D22", AIR, ("opération connue", "2001-12-03", "dans la référence"), document_dans_la_reference)

    # D15 : la référence de la seconde entrée ne compte pas les lignes posées par la première
    def d15():
        n, refus, s, src, j, b = jouer(R, D, (("AIRBUS", "2001-01-02", decision), AIR[0]))
        comb = lignes(j, "AIRBUS", "comblé")
        print(f"      D15 : {n} comblées, refus {refus}, références {sorted({l[6].split('communes, ')[1][:30] for l in comb})}")
        return not refus and len(comb) > 250 and all("communes, du 2001-09-03 au " in l[6] for l in comb)
    tenter("D15", d15)

    entiere("D16", None, sans=(R.RC.DIVISIONS,))
    return res


def main():
    """Joue les épreuves sur les vrais programmes, puis sous chaque sabotage demandé ; rend le code de sortie.

    ① RÔLE — Porter le jeu : Z0, puis les sabotages.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `sys.argv` : la racine, et `--saboter` ou `--saboter=G1,…` (plusieurs `--saboter=` s'additionnent).
    ④ CONDITIONS D'ENTRÉE — La racine est un dépôt complet.
    ⑤ SORTIE — UNE valeur : 0 (tout vert, et chaque sabotage demandé mord) · 1 (une épreuve rouge, ou un sabotage
      qui ne mord pas : aucune épreuve verte en Z0 n'y rougit) · 2 (une cible de sabotage absente ou en double, ou
      un nom demandé par un `--saboter=` qui ne désigne aucun sabotage, ou un argument de trop : après `--saboter` et
      une espace, ou en plus de la racine, ou une option inconnue).
      [rend: 1]
    ⑥ TRAITEMENT — Charger, jouer ; pour chaque sabotage : vérifier que chaque cible est unique dans son programme
      (la reconstruction pour les paires marquées « RC », sinon la réparation), charger les copies sabotées, rejouer
      en gardant la sortie (sous la calibration faussée de `CALIBRATIONS_FAUSSEES` pour G43, rétablie ensuite),
      imprimer « mord » ou « NE MORD PAS », puis (tour 3) le motif de chaque épreuve tombée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 ; le motif imprimé, parce qu'un « mord » sans motif ne dit pas si c'est un refus ou un plantage
      (relecture du tour 2, Q2 : G6).
    ⑨ CE QUI CLOCHE — Un plantage compte encore comme une morsure (BACKLOG).
    ⑩ EFFET — Imprime ; crée des dossiers jetables sous le dossier d'essai.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
    """
    global R0_DIVISIONS, CALIBRATION_DU_TEMOIN
    # R-3 du relecteur M1 du 13-11-2026 : TOUS les `--saboter=`, et non le premier seul
    choix = [x for a in sys.argv if a.startswith("--saboter=") for x in a.split("=", 1)[1].split(",")]
    apres = [sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a == "--saboter"]
    # m-a bis de Cowork du 13-11-2026 (23h37) : `--sabotage=G42` était écarté de la racine sans être lu, Z0 seul, code 0
    options = [a for a in sys.argv[1:] if a.startswith("--") and a != "--saboter" and not a.startswith("--saboter=")]
    if options:
        print(f"OPTION(S) INCONNUE(S) : {options} — seules --saboter et --saboter=G1,G2 existent — aucun n'est joué")
        return 2
    if len(_args) > 1 or any(not a.startswith("--") for a in apres):
        print(f"ARGUMENT(S) DE TROP : {_args[1:] or apres} — une seule racine ; les sabotages s'écrivent --saboter=G1,G2 "
              "(sans espace) — aucun n'est joué")
        return 2
    # m-a du relecteur du 13-11-2026 : un nom demandé doit désigner exactement un sabotage, sinon rien n'a été joué ;
    # vérifié AVANT Z0 : un nom mal tapé ne coûte pas un jeu entier
    inconnus = [x for x in choix if x not in SABOTAGES]
    if inconnus:
        print(f"SABOTAGE(S) DEMANDÉ(S) INCONNU(S) : {inconnus} — aucun n'est joué")
        return 2
    K, R = charger()
    R0_DIVISIONS = R.RC.lire_divisions(os.path.join(RACINE, R.RC.DIVISIONS))
    R._LISTE_DECIDEE = R.DEBUTS_A_COMBLER
    res = epreuves(K, R)
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programmes tels quels : {len(res) - len(rouges)}/{len(res)} épreuves vertes" + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    if "--saboter" in sys.argv or choix:
        for k, paires in SABOTAGES.items():
            if choix and k not in choix:
                continue
            for p in paires:
                cible = p[-2]
                source = open(RECONSTRUCTION if len(p) == 3 else REPARATION, encoding="utf-8").read()
                if source.count(cible) != 1:
                    print(f"{k} NE S'APPLIQUE PLUS : texte cible trouvé {source.count(cible)} fois")
                    return 2
            K2, R2 = charger(paires)
            R2._LISTE_DECIDEE = R2.DEBUTS_A_COMBLER
            garde, juste = io.StringIO(), CALIBRATION_DU_TEMOIN
            if k in CALIBRATIONS_FAUSSEES:
                rang, faux = CALIBRATIONS_FAUSSEES[k]
                CALIBRATION_DU_TEMOIN = juste[:rang] + ((juste[rang][0], faux),) + juste[rang + 1:]
            try:
                with contextlib.redirect_stdout(garde):
                    r = epreuves(K2, R2)
            finally:
                CALIBRATION_DU_TEMOIN = juste
            # m-b du relecteur du 13-11-2026 : « mord » = les rouges du jeu MOINS les rouges de Z0, non vide
            tombees = [e for e, v in r.items() if not v and e not in rouges]
            deja = [e for e, v in r.items() if not v and e in rouges]
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}"
                  + (f" (rouges déjà en Z0, non comptés : {deja})" if deja else ""))
            for l in motifs(garde.getvalue(), tombees):
                print(l)
            if not tombees:
                code = 1
    return code


if __name__ == "__main__":
    _DOSSIER_D_ESSAI = tempfile.mkdtemp(prefix="epreuves_debuts_")
    tempfile.tempdir = os.environ["TMPDIR"] = _DOSSIER_D_ESSAI
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(_DOSSIER_D_ESSAI, ignore_errors=True)
