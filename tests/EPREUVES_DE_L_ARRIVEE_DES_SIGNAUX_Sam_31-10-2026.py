#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX — Sam 31-10-2026 21h40 (Paris)
EN ESSAI · Rôle : éprouver, UNE FOIS et à CHACUNE des FENETRE dernières dates de la série que le juge joue, que chaque
programme de signal du dépôt ne se sert pas des séances qui suivent le jour qu'il signale. Et que l'épreuve a des
dents. SIMULATION UNIQUEMENT.
Quand l'appeler : à l'arrivée d'un programme de signal (un module qui se déclare « module de signal »), à chaque
changement d'un tel module ou des réglages qu'une fiche lui passe ; la vérification de version la lance d'elle-même.

À QUOI ÇA SERT, EN FRANÇAIS SIMPLE (décision de Jean-Luc du 31-10-2026 à 21h15, ses mots : « Ok, je ne comprends
pas très bien, mais je te fais confiance. Donc fais le 1, mais tu traces tout ça en autoportant, tu traces toute
cette décision, qu'on puisse la comprendre dans 6 mois. ») :
  Une stratégie est un PROGRAMME DE SIGNAL (il reçoit les cours d'une valeur et rend les jours d'achat) plus des
  RÉGLAGES. Une erreur de programmation involontaire — un décalage d'une ligne dans un calcul — peut faire utiliser
  au programme, pour décider un jour, le cours d'un jour SUIVANT. Exemple : C5 décide sur la clôture du jour et achète
  à l'ouverture du lendemain (R-601 : entrée à l'ouverture qui suit le signal) ; si son programme lisait par erreur la
  clôture du lendemain, il paraîtrait excellent sur le passé et serait impossible à suivre en vrai. C'est le « biais
  d'anticipation » des tests sur le passé ; personne ne triche. Avec la moulinette, des centaines de versions seront
  jugées : une seule erreur de ce genre fabriquerait une fausse excellente stratégie.
  LE TEST : pour chaque valeur, la RÉFÉRENCE est la série entière que le juge joue (le fichier maître des cours, lu
  par le lecteur du juge, depuis sa première séance). Pour chacun des FENETRE derniers jours J de cette série, le
  programme reçoit les cours JUSQU'À J seulement ; il doit dire pour J la même chose que quand il reçoit la série
  entière. Sinon il se sert de l'avenir : REFUSÉ, avec la valeur, la date et le sens de l'écart.
  POURQUOI LA SÉRIE DU JUGE COMME RÉFÉRENCE (superviseur R-759 du tour 3, 01-11-2026, « piste b ») : le juge appelle
  le signal UNE fois, sur la série entière. Au tour 2, la référence était une série à part, les 400 dernières
  séances (à partir du 2025-04-08), alors que le juge joue 724 séances (à partir du 2024-01-02). Un signal qui se
  comporte autrement selon la longueur de la série passait : le tricheur « historique minimal » du relecteur (rien
  sous 500 séances, puis une erreur d'indice qui lit le lendemain) ne signalait rien sur 400 séances et passait,
  alors qu'il lit l'avenir sur la série du juge (373 écarts sur trois valeurs).
  CE SENS NOUVEAU A ÉTÉ ACCEPTÉ PAR UNE DÉCISION PROVISOIRE de Jean-Luc du 01-11-2026 à 01h20, à reconfirmer après
  réexplication (il a écrit à 01h25 : « Tu me réexpliqueras demain ces 2 points, pas compris »). Question posée :
  « on garde les 400 jours vérifiés, mais chaque jour serait désormais vérifié sur la série entière, celle que le juge
  joue chaque soir et qui commence en janvier 2024, et non plus sur les 400 dernières séances prises à part ;
  pourquoi : prises à part, deux tricheurs passaient » ; réponse : « Oui, série entière (recommandé) ». Elle s'ajoute
  à la décision du 31-10-2026 à 21h15 (« sur TOUS les jours d'une période fixe de 400 séances »), qui fixe le nombre
  de jours. Le geste qui la défait, s'il le faut, est écrit à côté de FENETRE (« RÉVERSIBILITÉ ») : une ligne de
  code et ce qu'elle entraîne, plus cinq textes à reprendre.
  POURQUOI ICI ET PAS DANS LE JUGE : ce test tournait dans le juge (`regard_sur_l_avenir`, retiré le 31-10-2026), à
  chaque jugement ; pour rester léger il ne regardait que 5 + 5 dates tirées par série, ne prouvait presque rien (le
  relecteur de la version B a fait passer une fuite rare sur les deux fiches vivantes) et faisait passer l'épreuve
  du juge par le lecteur de 593 s à 977 s sur une machine seule. Fait une fois par programme, il couvre toutes ses
  versions. Le juge garde le contrôle de la FORME de la sortie (`forme_du_signal`), qui ne coûte presque rien.
  CHIFFRES DU SUPERVISEUR R-759 (versionB/superviseur/VERDICT.md, 31-10-2026) : environ 110 s pour C5 sur 39 valeurs
  et une série de référence de 400 séances (la manière du tour 2, avant la série du juge) ; toutes les dates de 20 ans prendraient environ 9 heures (extrapolé) ; empêcher par construction le
  programme de voir l'avenir coûterait environ 56 fois un appel normal (BACKLOG).

LES SIGNAUX ÉPROUVÉS SE TROUVENT PAR PROPRIÉTÉ, JAMAIS PAR UNE LISTE ÉCRITE (`signaux_a_eprouver`) :
  ① chaque module de `programmes/` qui se déclare « module de signal » (`declaration_de_signal` du juge, la même
     lecture que le juge), avec la fonction et les réglages d'exemple que sa déclaration écrit (lignes
     « fonction_signal = … » et « reglages_signal = … ») ;
  ② chaque triple (module, fonction, réglages) qu'une fiche du registre des stratégies nomme ;
  ③ un module déclaré qui n'a ni exemple ni fiche est INÉPROUVABLE, et l'épreuve rougit (R-734 : un contrôle qui n'a
     pas pu tourner ne rend pas 0). Un nouveau module est donc couvert sans que personne pense à l'ajouter.

LES CAS (A1 à A6), DANS UNE COPIE DU DÉPÔT où l'épreuve dépose ses propres modules (préfixe `EPREUVE_ARRIVEE_`) et
une fiche d'épreuve :
  A1 chaque signal du DÉPÔT passe (le vrai registre, dont la vraie ligne C5E10-QA-V1, R-732 ; les vrais modules RSI(2)
     et hasard par leur déclaration), et aucun module déclaré du dépôt n'est inéprouvable ; un signal qui ne passe
     pas y est NOMMÉ (`nommer_ce_qui_ne_passe_pas`) ;
  A2 le module d'épreuve honnête (décalage 0) passe ;
  A3 chaque tricheur est éprouvé ET refusé : `filtre_lendemain` (C5 confirmé par la séance suivante, une fuite qui
     RETIRE des achats), `frequent_plus_fuite_rare` (un signal fréquent plus un achat les veilles d'une hausse de 6 %),
     `normalisation_globale` (un seuil tiré de toute la série), `memoire` (retient la plus longue série vue),
     `connait_l_echantillon` (ne triche pas aux dates qu'un échantillon à graine écrite tirerait), et les deux
     tricheurs du relecteur du tour 2 dont le comportement dépend de la LONGUEUR de la série : X5 « historique
     minimal » et X6 « normalisation si longue ». Leur seuil (`SEUIL_DES_TRICHEURS_LONGS`, FENETRE + 100) doit être
     plus grand que FENETRE et atteint par au moins une valeur du maître, sinon ils n'ont plus de dents : A3 rougit
     (R-734). A3 exige aussi que chaque tricheur refusé soit NOMMÉ par `nommer_ce_qui_ne_passe_pas` (son module, ses
     réglages et le début de son verdict) : la dent de T3-5 tient aux tricheurs que l'épreuve dépose elle-même ;
  A4 les réglages d'une FICHE sont éprouvés : la fiche d'épreuve passe au module honnête un décalage de −1, qui lui
     fait lire la séance suivante ; elle est refusée ;
  A5 un module d'épreuve déclaré, sans exemple et sans fiche, est dit inéprouvable ;
  A6 un lancement sans verdict n'est pas un verdict (ajouté le 05-11-2026, superviseur R-759 de la nuit, défaut 1 :
     « un sabotage ne peut viser qu'une règle qu'un cas peut appeler ») : sur des EXEMPLES ÉCRITS, un délai dépassé et
     une trace Python ne rendent aucun verdict pour `verdict_du_lancement` ; `code_des_cas` rend 2 dès qu'un lancement
     inattendu est sans verdict, et 0 pour le seul témoin. Le sabotage T3_3a fait rougir A6, T3_5 fait rougir A3.
  LE TÉMOIN « SANS VERDICT » ET CE QUE LA BOUCLE EXTÉRIEURE EXIGE (tour de n°83, 05-11-2026 ; superviseur R-759 du
  même jour, après le tour final, défauts 1 et 4) : le module d'épreuve `EPREUVE_ARRIVEE_PLANTE.py` est lancé dans la
  VRAIE boucle des signaux, plante par MemoryError (que `comparer` relance : une erreur de la machine n'est pas un
  verdict), et n'est jugé par aucun cas. C'est la boucle extérieure — le processus qui sabote les copies, et qu'aucun
  sabotage n'atteint — qui exige, de Z0 et de chaque sabotage : ① la ligne « PAS DE VERDICT » du témoin ; ② un module
  nommé dans chaque élément rouge de A1 (`ce_que_le_lancement_n_a_pas_porte`). Sinon Z0 est ROUGE, et un sabotage
  « NE MORD PAS : POUR SA RAISON ». Z0 tournant chaque nuit, le BRANCHEMENT de la règle T3-3 (le rangement, la ligne
  imprimée) est éprouvé chaque nuit. Preuves jouées une fois, sorties capturées (n83/RAPPORT.md, hors dépôt) : les
  sabotages X1, X3 combiné à Sf, T3_3b et « relance retirée de `comparer` » sont vus ; la même exigence retirée, X1 ne
  l'est plus. RETRAIT SIGNALÉ : le sabotage inscrit T3_3b et le lancement à part du module qui plante (cas A6) sont
  retirés, voir SABOTAGES.

USAGE : python3 -B tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py <racine> [--saboter | --saboter=S1,S2,… | nom]
  sans option : Z0, le dépôt tel quel ; --saboter : Z0 puis chaque sabotage ; --saboter=<noms séparés par des
  virgules> : Z0 puis ceux-là (c'est ainsi que tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py joue la série par lots) ;
  un nom de sabotage : celui-là seul, sans Z0.
  UNE LIGNE PAR SABOTAGE, au format que lisent le joueur de séries et le certificateur
  (programmes/SERIES_DE_SABOTAGES.py, `LIGNE`) : « <nom> mord : [<cas rougis>] » ou « <nom> NE MORD PAS : … » ; la
  durée est sur la ligne suivante, à part, pour qu'un essai refait puisse rendre la ligne mot pour mot.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable ou si un nom demandé n'existe pas.
LA SÉRIE DE SABOTAGES N'EST PLUS JOUÉE LE SOIR (décision de Jean-Luc du 01-11-2026 à 11h41, n°71, réponse « 1 » à
« que fait-on de la série de sabotages de la version B (43 min chaque soir) ? », option 1 : « La sortir du soir, et ne
la rejouer que quand le code de l'essai change. C'est la pratique de la profession, recommandée par l'expert des
tests. ») : elle est déclarée dans tests/LANCEMENT_DES_EPREUVES.json (« series_hors_de_la_nuit ») ; elle se rejoue
à la main par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py, qui écrit son relevé
(tests/resultats/SERIE_DE_SABOTAGES_DE_L_ARRIVEE_DES_SIGNAUX_*.txt) avec l'empreinte de chaque fichier du dépôt dont
le code a été EXÉCUTÉ pendant la série (ce fichier, le juge, ses modules, les modules de signal) ; chaque nuit, la
certification vérifie que ce code n'a pas changé, et rougit sinon. QUEL CODE COMPTE est un CHOIX DU CHAT, PROVISOIRE,
À CONFIRMER PAR JEAN-LUC (D43, 05-11-2026 ; ce n'est pas une décision de Jean-Luc) : portée « code_execute », ce
fichier ET les programmes qu'il exécute, sans les données ; raison : changer un seul réglage du RSI(2) du dépôt
(« tendance » 200 → 0) faisait perdre la dent du sabotage Sf sans aucune alerte (relecteur du 05-11-2026). Si
Jean-Luc retient la lecture au mot de n°71 (ce fichier seul), un mot change dans la table (« epreuve »), sans
rejouer la série : le relevé porte déjà les deux. Le lancement normal (Z0) tourne, lui, chaque nuit.

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; par la vérification de version (`programmes/CERTIFIER_LA_VERSION.py`), qui lance
  chaque épreuve de tests/ depuis la racine avec la racine en argument (Z0), et qui, à la place de « --saboter »,
  vérifie le relevé de la série (décision n°71, voir plus haut) ; par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py,
  avec « --saboter=<noms> », à chaque changement de ce fichier. Ce programme se
  relance lui-même avec « --cas <copie> » (les cas, dans une copie) et « --signal <racine> <module> <fonction>
  <réglages> » (UN signal, dans un processus neuf) : ces deux modes ne sont pas faits pour la main.
③ ENTRÉE — La racine du dépôt ; `--saboter`, `--saboter=<noms>` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : le juge, le contrat des fichiers (le nom et la lecture du registre, n°83 :
  une fiche par identifiant, sa dernière ligne), le registre des stratégies, le fichier maître des cours, le
  référentiel des valeurs, le module C5 (dont dépend le tricheur `filtre_lendemain`).
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par signal éprouvé, par cas et par sabotage. [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① copier la racine dans un dossier temporaire (sans .git, etudes,
  caches) · ② appliquer le sabotage à la copie de CE fichier, en exigeant que sa cible existe une fois · ③ relancer
  la copie de ce programme en mode « --cas » · ④ Z0 doit être vert, un sabotage doit faire échouer au moins un cas ;
  dans les deux, CHAQUE SIGNAL, le témoin « sans verdict » excepté, DOIT AVOIR RENDU UN VERDICT (voir `cas`, T3-3) :
  sinon « --cas » rend 2, Z0 est rouge et le sabotage « NE MORD PAS » (`verdict_du_lancement`, `code_des_cas`) ; et
  la sortie doit porter ce qu'exige `ce_que_le_lancement_n_a_pas_porte` (la ligne du témoin, un module dans chaque
  élément rouge de A1), sinon Z0 est rouge et le sabotage « NE MORD PAS : POUR SA RAISON ».
⑦ UNITÉ — Des séances (la fenêtre), des dates AAAA-MM-JJ, des secondes.
⑧ POURQUOI — Voir « POURQUOI ICI ET PAS DANS LE JUGE » et « POURQUOI LA SÉRIE DU JUGE COMME RÉFÉRENCE ». Les coupes
  passent dans l'ORDRE CROISSANT et la série entière est appelée EN DERNIER, dans un état neuf (processus neuf par
  signal, module rechargé pour chaque valeur) : un module qui retiendrait une série plus longue n'a jamais rien vu
  de l'avenir quand il décide d'une coupe (superviseur R-759, mesure S2 : c'est ce qui fait refuser `memoire`). La
  coupe part de l'ORIGINE de la série : le calcul du passé ne change pas d'une coupe à l'autre, et un signal à longue
  mémoire (RSI de Wilder, moyenne à 200 séances) reste accepté. Seules les FENETRE dernières dates sont coupées : le
  coût suit la somme des longueurs des coupes (C5 sur 40 valeurs : 293 s mesurées seul le 01-11-2026 à 01h28, et
  +0,6 s par séance ajoutée au maître, calcul du superviseur du tour 3) ; toutes les dates coûteraient environ 400 s, au carré de la
  longueur. Un jeu d'épreuves se sabote contre sa propre correction (R-731).
  UNE GARDE D'HISTORIQUE ÉCRITE SUR LA LONGUEUR DE LA SÉRIE EST REFUSÉE, ET À RAISON (tricheur N7 du relecteur du
  tour 3, 01-11-2026, retenu par le superviseur R-759 du tour 4) : un programme honnête par ailleurs qui commence par
  `if len(ohlcv) < 500: return []` est refusé le 2025-04-08, parce que cette garde lit la longueur de TOUTE la série,
  avenir compris ; un vrai soir du 2025-04-08, il n'aurait rien signalé. La garde juste s'écrit par date :
  `for i in range(500, len(ohlcv))`. Raison de cette ligne : sans elle, le premier refus de ce genre passera pour un
  faux refus.
⑨ CE QUI CLOCHE — CE QUI EST PROUVÉ : pour chaque signal éprouvé et chaque valeur du fichier maître, à chacune des
  FENETRE dernières dates, la décision prise sur la série coupée à ce jour est celle que le signal, CHARGÉ PAR
  L'ÉPREUVE, tire de la série entière que le juge lit ce soir (précision du superviseur R-759 du tour 4 : un module
  qui se sait éprouvé peut tirer autre chose de la même série quand c'est le juge qui le charge, limite ⑥). CE QUI NE
  L'EST PAS, nommé (superviseurs R-759 du 31-10-2026 et du 01-11-2026) :
  ① UN MODULE QUI RELIT LUI-MÊME UN FICHIER (le maître des cours, par date) passe n'importe quel contrôle fondé sur
     son comportement ; seul un processus sans accès aux fichiers l'arrêterait, et il n'existe pas aujourd'hui. Y
     COMPRIS UN CACHE QUE LE MODULE ÉCRIT LUI-MÊME : rempli par le juge, il le fait passer (tricheur N3 du relecteur
     du tour 3 : refusé au premier lancement, il passe après un passage « comme le juge » ; c'est la forme
     PLAUSIBLE de cette limite) ;
  ② UNE FUITE À UNE DATE ANTÉRIEURE AUX FENETRE DERNIÈRES n'est pas vue. Concrètement, au 31-10-2026 : les deux
     fiches vivantes jouent 644 dates (du 2024-01-02 au 2026-07-10) et 324 d'entre elles sont avant les 400
     dernières ; le tricheur X2 du relecteur du tour 2 (une fuite le 2024-06-03) passe ;
  ③ UN MODULE AJOUTÉ PUIS JUGÉ AVANT LA PROCHAINE VÉRIFICATION DE VERSION n'a pas été éprouvé : le juge ne le refuse
     pas (BACKLOG : un visa par empreinte du module) ;
  ④ DES RÉGLAGES ABSENTS DU REGISTRE ET DES DÉCLARATIONS ne sont pas éprouvés (au 31-10-2026, la moulinette ne fait
     varier aucun `reglages_signal`, relevé du superviseur ; le jour où elle le fera, ses versions ne seront pas
     couvertes) ;
  ⑤ L'HISTORIQUE DES 20 ANS (option `--cours=` du juge, lancée à la main) n'est pas éprouvé : un signal qui change de
     comportement au-delà de la longueur du maître (724 séances au 31-10-2026) n'y est pas vu (BACKLOG : l'épreuve
     à la demande sur ce fichier, environ 3 950 s extrapolées) ;
  ⑥ UN MODULE QUI RECONNAÎT QU'IL EST ÉPROUVÉ — par la suite des coupes (même origine, une séance de plus à chaque
     appel : tricheur X4 du relecteur du tour 2, T2-5), par sa ligne de commande, son dossier ou la pile d'appels
     (tricheur N4 du relecteur du tour 3 : honnête quand `--signal` est dans sa ligne de commande, il lit le
     lendemain sinon, et il passe) — peut ne pas tricher dans l'épreuve et tricher dans le juge. Seule la preuve par
     construction (BACKLOG) le rend impossible. Aucune parade n'est codée (superviseur R-759 du tour 4 : renommer
     `--signal` ou changer de dossier appellerait le tricheur suivant ; c'est la limite de toute épreuve faite de
     l'extérieur, et elle repose sur la relecture humaine).
  Et aussi : ⑦ une valeur plus courte que FENETRE est coupée à toutes ses dates, dès la première séance (au
  31-10-2026, une valeur n'a que 30 séances) : un signal honnête qui lève sur une série d'une séance y est dit
  « REFUSÉ » au lieu de « ne tourne pas » (T2-3, BACKLOG) ; ⑧ un module déclaré hors de `programmes/`, ou dans un
  SOUS-DOSSIER de `programmes/`, n'est trouvé que si une fiche le nomme ; un module du dépôt dont le nom commence
  par `EPREUVE_ARRIVEE_` n'est vérifié par aucun cas (T2-2, BACKLOG) ; ⑨ la série reçue est celle du lecteur des
  cours, sans la coupe aux trous que `jouer` fait : un signal se juge sur n'importe quelle série.
  Et encore : les deux défauts trouvés par le relecteur du tour 3 (T3-3, T3-5) sont réparés au dernier tour de la
  version B (04-11-2026) ; leurs FONCTIONS ont des dents depuis le 05-11-2026 (cas A6 et A3, sabotages T3_3a, T3_5),
  et leur BRANCHEMENT depuis le tour de n°83, même jour (le témoin et la boucle extérieure, voir « LE TÉMOIN »). Ce
  qui reste : ⓐ le maillon 3, `sys.exit(code_des_cas(resultats, sans_verdict))` du mode « --cas », n'est exercé par
  aucun chemin réel (le témoin y est écarté ; un vrai signal sans verdict coûterait un lancement de plus) : il tient
  en une ligne, et le sabotage X2 du relecteur reste « NE MORD PAS » ; ⓑ un module de signal qui écrit lui-même
  « REFUSÉ · … » sur sa sortie puis s'arrête en code 1 passerait pour un verdict rendu (un tricheur de la limite ⑥,
  non codé ; BACKLOG) ; ⓒ un signal du dépôt qui lève lui-même une OSError ou une MemoryError n'a pas de verdict
  (code 2), jamais un refus. · Avec la série sortie du soir (décision
  n°71) et la portée « code_execute » (choix D43 du Chat, à confirmer), ses dents sont revérifiées au changement du
  code EXÉCUTÉ par la série ; une dent qui tient aux DONNÉES (le seuil des tricheurs longs tient à la longueur du
  maître) n'est pas couverte par le relevé : seul le contrôle de sa précondition en Z0 la protège (R-734). Un module
  qui devient module de signal ne fait rejouer la série qu'après sa première exécution par une série ; Z0 l'éprouve
  dès la nuit suivante. Avec la portée « epreuve », un changement d'un autre fichier dont une dent dépend (Sf mord
  parce que le RSI(2) du dépôt a une moyenne de 200 séances) ne ferait pas rejouer la série.
⑩ EFFET — Écrit seulement dans des dossiers temporaires, effacés à la fin normale ; `-B` partout, aucun fichier
  compilé. LIMITE : une coupure par le certificateur (délai dépassé) laisse la copie du sabotage en cours, environ
  300 Mo (296 Mo mesurés par le relecteur du tour 3), dans le dossier temporaire, car le certificateur ne tue que
  son enfant direct. Sur GitHub, chaque tranche tourne sur une machine jetée à la fin : cela n'y coûte rien ; sur la
  machine du Chat, ce dossier est à effacer à la main (BACKLOG, au nom du certificateur, T3-6).
⑪ TERMINAISON — Sort lui-même. Chaque sous-processus a un délai ; un délai dépassé compte comme un échec.
  [sort: oui]
"""
import ast
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

SOI = "tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
# LA FENÊTRE, en séances : le nombre des DERNIÈRES DATES coupées dans la série entière que le juge joue.
# ① Décision de Jean-Luc du 31-10-2026 à 21h15 : « sur TOUS les jours d'une période fixe de 400 séances ».
# ② Décision PROVISOIRE de Jean-Luc du 01-11-2026 à 01h20, à reconfirmer après réexplication (il a écrit à 01h25 :
#    « Tu me réexpliqueras demain ces 2 points, pas compris ») : le sens nouveau est accepté. Question posée : « on
#    garde les 400 jours vérifiés, mais chaque jour serait désormais vérifié sur la série entière, celle que le juge
#    joue chaque soir et qui commence en janvier 2024, et non plus sur les 400 dernières séances prises à part ;
#    pourquoi : prises à part, deux tricheurs passaient » ; réponse : « Oui, série entière (recommandé) ».
# Le nombre de jours éprouvés ne change pas (400 par valeur) ; la série de RÉFÉRENCE change : c'est la série entière
# du fichier maître, depuis sa première séance (superviseur R-759 du tour 3, piste b).
# RÉVERSIBILITÉ (si Jean-Luc dit « non » après réexplication) : le sens tient dans UNE ligne, `s = cours[v]` dans
# `eprouver_un_signal` ; la remplacer par `s = cours[v][-FENETRE:]` rend exactement la manière du tour 2 (c'est le
# sabotage Sg). Il faut alors, dans le même geste, retirer de MODULES_D_EPREUVE les tricheurs HISTORIQUE_MINIMAL et
# NORMALISATION_SI_LONGUE (ils passeraient, A3 rougirait), le contrôle de leur seuil dans `cas`, les sabotages Sg et
# Sh, et écrire au ⑨ de l'en-tête la limite « un signal qui se comporte autrement sur la série du juge que sur 400
# séances prises à part n'est pas éprouvé » (verdict du superviseur t3 : ARRÊTER ET SIMPLIFIER).
# Ce geste de code a été joué sur une copie par le relecteur du tour 3 (Z0 tout vert après lui, en 131 s, R17). Il ne
# suffit pas : CINQ TEXTES décrivent la série entière et diraient alors le contraire du code ; ils sont à reprendre
# dans le même geste (relecteur du tour 3, retenu par le superviseur R-759 du tour 4) :
#   ① le paragraphe « LE TEST » de l'en-tête (« la RÉFÉRENCE est la série entière que le juge joue ») ;
#   ② la phrase « CE QUI EST PROUVÉ » du ⑨ de l'en-tête ;
#   ③ les éléments ③, ⑥ et ⑧ de la notice de `comparer` ;
#   ④ la ligne PASSE de `eprouver_un_signal` (« les 400 dernières de chaque série entière ») ;
#   ⑤ les deux « pourquoi » de cette épreuve dans tests/LANCEMENT_DES_EPREUVES.json, celui du lancement normal
#      (« delais ») et celui de la série (« series_hors_de_la_nuit », depuis la décision n°71) : durées mesurées avec
#      la série entière, piste b.
FENETRE = 400
# Le seuil de longueur des tricheurs X5 et X6 : plus grand que FENETRE (sinon ils trichent aussi dans les coupes et ne
# prouvent plus rien sur la référence) et atteint par au moins une valeur du maître (contrôlé dans A3, R-734).
SEUIL_DES_TRICHEURS_LONGS = FENETRE + 100
PREFIXE = "EPREUVE_ARRIVEE_"
# Le délai d'UN signal (un sous-processus) : C5 sur 40 valeurs, 293 s mesurées seul le 01-11-2026 à 01h28 (charge 0,7 à
# 2,0), soit 1 173 s avec le facteur 4 de la mesure de couverture, et +0,6 s par séance ajoutée au maître.
DELAI_D_UN_SIGNAL = 1800         # secondes
# Le nombre de cas (A1 à A6) qu'un lancement « --cas » complet annonce sur sa ligne « FIN DES CAS ». ÉCRIT À LA MAIN,
# alors qu'il devrait se calculer (R-728 : ce qui se calcule ne s'écrit pas à la main) : consigné au BACKLOG par le
# superviseur R-759 du 05-11-2026, défaut 1, point 5 ; passé de 5 à 6 avec le cas A6.
NOMBRE_DE_CAS = 6

# LES MODULES D'ÉPREUVE, déposés dans programmes/ de la COPIE : nom du fichier → (texte, verdict attendu). Les
# tricheurs reprennent ceux du relecteur de la version B (versionB/relecture/outils/tricheurs.py, 31-10-2026).
_DECLARE = '"""EN ESSAI · module de signal · Rôle : module d\'épreuve de l\'arrivée des signaux — %s.\n%s"""\n'
MODULES_D_EPREUVE = {
    "EPREUVE_ARRIVEE_HONNETE_DECALAGE.py": (_DECLARE % (
        "achète quand la clôture du jour i − decalage dépasse de 1 % la précédente ; honnête à decalage = 0",
        "fonction_signal = signaux\nreglages_signal = {\"decalage\": 0}\n") +
        "def signaux(ohlcv, decalage):\n"
        "    out = []\n"
        "    for i in range(1, len(ohlcv)):\n"
        "        k = i - decalage\n"
        "        if 1 <= k < len(ohlcv) and ohlcv[k][\"close\"] > ohlcv[k - 1][\"close\"] * 1.01:\n"
        "            out.append({\"i\": i})\n"
        "    return out\n", "PASSE"),
    "EPREUVE_ARRIVEE_TRICHEUR_FILTRE_LENDEMAIN.py": (_DECLARE % (
        "C5, sauf les jours où la séance SUIVANTE baisse (une fuite qui retire des achats)",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "import importlib.util, os\n"
        "_sp = importlib.util.spec_from_file_location('c5_de_l_epreuve', os.path.join(os.path.dirname(os.path.abspath(__file__)),\n"
        "                                             'MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py'))\n"
        "_c5 = importlib.util.module_from_spec(_sp)\n"
        "_sp.loader.exec_module(_c5)\n"
        "def signaux(ohlcv):\n"
        "    return [{\"i\": x[\"i\"]} for x in _c5.signaux_c5etendu10(ohlcv)\n"
        "            if not (x[\"i\"] + 1 < len(ohlcv) and ohlcv[x[\"i\"] + 1][\"close\"] < ohlcv[x[\"i\"]][\"close\"])]\n",
        "REFUSÉ"),
    "EPREUVE_ARRIVEE_TRICHEUR_FREQUENT_PLUS_FUITE_RARE.py": (_DECLARE % (
        "clôture 2 % sous sa moyenne de 5 séances, plus un achat les veilles d'une hausse de 6 % (fuite rare)",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    out = set()\n"
        "    for i in range(5, len(ohlcv)):\n"
        "        if ohlcv[i][\"close\"] < sum(b[\"close\"] for b in ohlcv[i - 5:i]) / 5 * 0.98:\n"
        "            out.add(i)\n"
        "    out |= {i for i in range(len(ohlcv) - 1) if ohlcv[i + 1][\"close\"] > ohlcv[i][\"close\"] * 1.06}\n"
        "    return [{\"i\": i} for i in sorted(out)]\n", "REFUSÉ"),
    "EPREUVE_ARRIVEE_TRICHEUR_NORMALISATION_GLOBALE.py": (_DECLARE % (
        "seuil tiré de TOUTE la série (les 5 % des clôtures les plus basses)",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    cl = sorted(b[\"close\"] for b in ohlcv)\n"
        "    if not cl:\n"
        "        return []\n"
        "    seuil = cl[max(0, len(cl) // 20 - 1)]\n"
        "    return [{\"i\": i} for i in range(1, len(ohlcv)) if ohlcv[i][\"close\"] <= seuil and ohlcv[i - 1][\"close\"] > seuil]\n",
        "REFUSÉ"),
    "EPREUVE_ARRIVEE_TRICHEUR_MEMOIRE.py": (_DECLARE % (
        "retient la plus longue série vue (même première date) et y lit le lendemain",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "_MEMOIRE = {}\n"
        "def signaux(ohlcv):\n"
        "    if not ohlcv:\n"
        "        return []\n"
        "    k = ohlcv[0][\"date\"]\n"
        "    if k not in _MEMOIRE or len(_MEMOIRE[k]) < len(ohlcv):\n"
        "        _MEMOIRE[k] = ohlcv\n"
        "    p = _MEMOIRE[k]\n"
        "    return [{\"i\": i} for i in range(len(ohlcv)) if i + 1 < len(p) and p[i + 1][\"close\"] > p[i][\"close\"] * 1.01]\n",
        "REFUSÉ"),
    # ce tricheur connaît l'échantillon du sabotage Sa (graine écrite, comme l'était celle du contrôle retiré du juge,
    # GRAINE_DU_CONTROLE_DE_L_AVENIR = 20261031) et ne triche jamais sur les dates tirées : il passe tout échantillon
    # dont la graine est connue, et seule une épreuve de TOUTES les dates le refuse
    "EPREUVE_ARRIVEE_TRICHEUR_CONNAIT_L_ECHANTILLON.py": (_DECLARE % (
        "lit le lendemain (hausse de plus de 1 %), sauf aux dix dates qu'un échantillon à graine 20261031 tirerait",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "import random\n"
        "def signaux(ohlcv):\n"
        "    tirees = set(random.Random(20261031).sample(range(max(0, len(ohlcv) - %d), len(ohlcv)), min(10, len(ohlcv), %d)))\n"
        % (FENETRE, FENETRE) +
        "    return [{\"i\": i} for i in range(len(ohlcv) - 1)\n"
        "            if i not in tirees and ohlcv[i + 1][\"close\"] > ohlcv[i][\"close\"] * 1.01]\n", "REFUSÉ"),
    # X5 du relecteur du tour 2 (versionB/relecture_t2/outils/tricheurs/RT2_X5_HISTORIQUE_MINIMAL.py), seuil en FENETRE
    "EPREUVE_ARRIVEE_TRICHEUR_HISTORIQUE_MINIMAL.py": (_DECLARE % (
        "PLAUSIBLE : exige un long historique, puis un décalage d'une ligne lui fait lire le lendemain (X5)",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    if len(ohlcv) < %d:\n" % SEUIL_DES_TRICHEURS_LONGS +
        "        return []\n"
        "    c = [b[\"close\"] for b in ohlcv]\n"
        "    out = []\n"
        "    for i in range(20, len(c) - 1):\n"
        "        moy = sum(c[i - 19:i + 1]) / 20\n"
        "        if c[i + 1] < moy * 0.97:\n"
        "            out.append({\"i\": i})\n"
        "    return out\n", "REFUSÉ"),
    # X6 du relecteur du tour 2 (RT2_X6_NORMALISATION_SI_LONGUE.py), seuil en FENETRE
    "EPREUVE_ARRIVEE_TRICHEUR_NORMALISATION_SI_LONGUE.py": (_DECLARE % (
        "PLAUSIBLE : seuil tiré de toute la série quand elle est assez longue, des 250 séances passées sinon (X6)",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    c = [b[\"close\"] for b in ohlcv]\n"
        "    out = []\n"
        "    if len(c) >= %d:\n" % SEUIL_DES_TRICHEURS_LONGS +
        "        s = sorted(c); seuil = s[len(s) // 10]\n"
        "        return [{\"i\": i} for i in range(1, len(c)) if c[i] <= seuil < c[i - 1]]\n"
        "    for i in range(250, len(c)):\n"
        "        s = sorted(c[i - 250:i]); seuil = s[25]\n"
        "        if c[i] <= seuil < c[i - 1]:\n"
        "            out.append({\"i\": i})\n"
        "    return out\n", "REFUSÉ"),
    "EPREUVE_ARRIVEE_SANS_EXEMPLE.py": (_DECLARE % ("déclaré, sans exemple et sans fiche : inéprouvable", "") +
        "def signaux(ohlcv):\n"
        "    return []\n", "INÉPROUVABLE"),
    # LE TÉMOIN « SANS VERDICT » (superviseur R-759 du 05-11-2026, après le tour final, défauts 1 et 4 ; tour de n°83) :
    # un module d'épreuve comme les tricheurs, trouvé par la même recherche, lancé dans la VRAIE boucle des signaux de
    # `cas`, et attendu SANS VERDICT. Il plante par une erreur de l'ENVIRONNEMENT (MemoryError) : `comparer` la relance
    # (défaut 4), le processus finit en code 1 sans ligne « REFUSÉ · », `verdict_du_lancement` rend None, `cas` le
    # range parmi les lancements sans verdict, et le programme principal imprime sa ligne « PAS DE VERDICT ». C'est le
    # processus NON SABOTÉ (la boucle extérieure, qui tourne dans le fichier du dépôt) qui exige cette ligne à chaque
    # lancement : le branchement de la règle T3-3 est ainsi éprouvé chaque nuit par Z0, et une retouche qui le
    # débrancherait rougit sans attendre un rejeu de la série. Avant le 05-11-2026, ce module (MODULE_QUI_PLANTE) était
    # lancé à part par le cas A6, hors de la boucle : ses dents défendaient les FONCTIONS et non leur BRANCHEMENT
    # (relecteur du 05-11-2026, sabotages X1, X2, X3 : NE MORD PAS).
    "EPREUVE_ARRIVEE_PLANTE.py": (_DECLARE % (
        "TÉMOIN : plante au premier appel par une erreur de l'environnement, sans rendre de verdict",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    raise MemoryError(\"plantage simulé : le témoin de l'épreuve d'arrivée s'arrête sans verdict\")\n",
        "SANS VERDICT"),
}
# LES TÉMOINS « SANS VERDICT », tirés de MODULES_D_EPREUVE par leur attendu (une propriété, jamais une liste écrite) :
# `code_des_cas` ne rend pas 2 pour eux, et la boucle extérieure exige leur ligne « PAS DE VERDICT » à chaque lancement.
TEMOINS_SANS_VERDICT = sorted("programmes/" + nom for nom, (_t, attendu) in MODULES_D_EPREUVE.items()
                              if attendu == "SANS VERDICT")
# LA FICHE D'ÉPREUVE, ajoutée au registre de la COPIE : les réglages d'une fiche doivent être éprouvés (A4).
FICHE_D_EPREUVE = {"id": "AAA-EPREUVE-ARRIVEE-DECALAGE", "nom": "EPREUVE decalage -1, lit la seance suivante",
                   "etat_vie": "LABO", "module_signal": "programmes/EPREUVE_ARRIVEE_HONNETE_DECALAGE.py",
                   "fonction_signal": "signaux", "reglages_signal": "{\"decalage\": -1}"}
# LE MODULE QUI PLANTE du cas A6 (05-11-2026, SystemExit, lancé à part après la recherche des signaux) est devenu le
# témoin EPREUVE_ARRIVEE_PLANTE.py de MODULES_D_EPREUVE (tour de n°83, même jour) : voir plus haut.

# Z0 (le dépôt tel quel) N'EST PAS UN SABOTAGE et n'est pas dans ce dictionnaire : le relevé de la série exige que
# CHAQUE clé de SABOTAGES « morde » (programmes/SERIES_DE_SABOTAGES.py, `verifier_la_serie`) ; une clé « Z0 » y
# était lue comme un sabotage sans résultat, et la série du 04-11-2026 (21h41-22h47, 8 sabotages sur 8 mordent) a été
# déclarée NON CONFORME pour cette seule raison.
SABOTAGES = {
    # Sa : un échantillon de 10 dates, tirées parmi les FENETRE dernières, au lieu de toutes (`connait_l_echantillon`,
    # qui évite exactement ces dates, passe alors à coup sûr ; la fuite rare sur signal fréquent passe ou non)
    "Sa_dix_dates_au_lieu_de_toutes": [(SOI, "    dates = list(range(max(0, len(s) - FENETRE), len(s)))\n",
                                        "    import random\n"
                                        "    dates = sorted(random.Random(20261031).sample(range(max(0, len(s) - FENETRE), len(s)),\n"
                                        "                                                  min(10, len(s), FENETRE)))\n")],
    # Sb : la série entière appelée AVANT les coupes (le tricheur `memoire` doit alors passer)
    "Sb_entiere_avant_les_coupes": [(SOI, "    coupes = {}\n    for j in dates:\n",
                                     "    entiere_d_abord = {x[\"i\"] for x in sig(s)}\n    coupes = {}\n    for j in dates:\n")],
    # Sc : seules les dates signalées sur la série entière sont comparées (`filtre_lendemain` doit alors passer)
    "Sc_un_seul_sens": [(SOI, "        if coupes[j] != (j in entiere):\n", "        if (j in entiere) and not coupes[j]:\n")],
    # Sd : les modules lus dans une liste écrite au lieu de leur propriété (les tricheurs déposés ne sont plus vus) ; la
    # liste garde le témoin « sans verdict » (tour de n°83) : sans lui, la boucle extérieure dirait « NE MORD PAS : POUR
    # SA RAISON », et le sabotage ne viserait plus ce qu'il vise
    "Sd_liste_ecrite": [(SOI, "    for f in sorted(os.listdir(dossier)):\n",
                         "    for f in [\"MODULE_SIGNAL_RSI2_CONNORS.py\", \"MODULE_SIGNAL_AU_HASARD.py\",\n"
                         "              \"MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py\", \"EPREUVE_ARRIVEE_HONNETE_DECALAGE.py\",\n"
                         "              \"EPREUVE_ARRIVEE_PLANTE.py\"]:\n")],
    # Se : un module éprouvé une seule fois, avec les réglages de sa déclaration (ceux de la fiche sont ignorés)
    "Se_reglages_de_la_fiche_ignores": [(SOI, "    cle = (module, fonction, reglages)\n", "    cle = (module, fonction)\n")],
    # Sf : la coupe en fenêtre glissante de 60 séances avant J au lieu de l'origine fixe (à éprouver : le RSI(2)
    # honnête, à moyenne de 200 séances, doit alors être refusé à tort)
    "Sf_fenetre_glissante": [(SOI, "        coupe = s[:j + 1]\n", "        coupe = s[max(0, j - 59):j + 1]\n")],
    # Sg : la référence ramenée aux FENETRE dernières séances, comme au tour 2 (X5 et X6 doivent alors passer)
    "Sg_reference_reduite_a_la_fenetre": [(SOI, "        s = cours[v]\n", "        s = cours[v][-FENETRE:]\n")],
    # Sh : le seuil des tricheurs X5 et X6 écrit en dur SOUS la fenêtre (le contrôle de A3 doit rougir)
    "Sh_seuil_des_tricheurs_sous_la_fenetre": [(SOI, "SEUIL_DES_TRICHEURS_LONGS = FENETRE + 100\n",
                                                "SEUIL_DES_TRICHEURS_LONGS = 300\n")],
    # T3-3a : un signal sans verdict ne fait plus rendre 2 à « --cas » (la règle T3-3 retirée ; A6 doit rougir)
    "T3_3a_sans_verdict_ignore": [(SOI, "    return 2 if inattendus else 0 if all(ok for _, ok, _ in resultats) else 1\n",
                                   "    return 0 if all(ok for _, ok, _ in resultats) else 1\n")],
    # T3-3b (« tout lancement en code 1 compte pour un verdict ») N'EST PLUS INSCRIT ICI depuis le tour de n°83
    # (05-11-2026) — RETRAIT SIGNALÉ : il fait perdre son « pas de verdict » au témoin EPREUVE_ARRIVEE_PLANTE.py, et la
    # boucle extérieure le voit à CHAQUE lancement, Z0 de chaque nuit compris (« la ligne PAS DE VERDICT du témoin
    # manque ») ; inscrit, il rendrait « NE MORD PAS : POUR SA RAISON » et la série serait non conforme. Il a été joué
    # une fois, sortie capturée, pour la preuve (superviseur R-759 du 05-11-2026, après le tour final, défaut 1, point 7).
    # T3-5 : la nomination de ce qui ne passe pas perd le module (A3 doit rougir)
    "T3_5_module_non_nomme": [(SOI, "    return [\"%s %s → %s\" % (sg[\"module\"], sg[\"reglages\"],\n",
                               "    return [\"%s → %s\" % (sg[\"reglages\"],\n")],
}


def juge(racine):
    """Charge le juge des stratégies de la racine, et le rend.

    ① RÔLE — Donner à l'épreuve les lectures du juge lui-même (déclaration, signal nommé, cours) : une seule écriture
      de chaque règle (R-708).
    ② CONTEXTE D'APPEL — `signaux_a_eprouver` (mode « --cas ») et `eprouver_un_signal` (mode « --signal »).
    ③ ENTRÉE — `racine` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — `programmes/JUGE_DES_STRATEGIES.py` existe sous la racine.
    ⑤ SORTIE — UNE valeur : le module du juge. [rend: 1]
    ⑥ TRAITEMENT — Mettre `programmes/` de la racine en tête du chemin d'import, importer le juge.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge importe `COMMUN` depuis son dossier : il se charge comme le fait le programme du soir.
    ⑨ CE QUI CLOCHE — Dans un même processus, le premier juge importé est gardé : chaque mode ne sert qu'une racine.
    ⑩ EFFET — Exécute le premier niveau du juge (définitions).
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur d'import. [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import JUGE_DES_STRATEGIES as B
    return B


def contrat(racine):
    """Charge le contrat des fichiers de la racine, et le rend.

    ① RÔLE — Donner à l'épreuve le nom et la lecture du registre des stratégies, écrits une fois dans
      `programmes/CONTRATS_DES_FICHIERS.py` (n°83, 05-11-2026) : la dernière ligne d'un identifiant fait foi.
    ② CONTEXTE D'APPEL — `signaux_a_eprouver` et `poser_les_modules_et_la_fiche` (mode « --cas »), une fois chacun.
    ③ ENTRÉE — `racine` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — `programmes/CONTRATS_DES_FICHIERS.py` existe sous la racine.
    ⑤ SORTIE — UNE valeur : le module du contrat. [rend: 1]
    ⑥ TRAITEMENT — Mettre `programmes/` de la racine en tête du chemin d'import, importer le contrat.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule écriture du nom du registre et de sa lecture (R-708) : avant n°83, cette épreuve lisait le
      fichier par son nom écrit ici, ligne par ligne.
    ⑨ CE QUI CLOCHE — Comme `juge` : dans un même processus, le premier contrat importé est gardé.
    ⑩ EFFET — Exécute le premier niveau du contrat (déclarations).
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur d'import. [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import CONTRATS_DES_FICHIERS as C
    return C


def exemple_de_la_declaration(chemin):
    """Lit, SANS L'EXÉCUTER, la fonction et les réglages d'exemple que la déclaration d'un module écrit.

    ① RÔLE — Trouver comment éprouver un module déclaré qu'aucune fiche ne nomme encore.
    ② CONTEXTE D'APPEL — `signaux_a_eprouver`, une fois par module déclaré.
    ③ ENTRÉE — `chemin` : le fichier du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier se lit comme du Python (la déclaration l'a déjà lu).
    ⑤ SORTIE — DEUX valeurs : le nom de la fonction (ou None) ; le texte JSON des réglages, ou le motif si la fonction
      manque ou si les réglages sont illisibles. Exemple réel : `programmes/MODULE_SIGNAL_RSI2_CONNORS.py` rend
      (« signaux_rsi2 », « {"periode": 2, "seuil": 10, "tendance": 200} »). [rend: 2]
    ⑥ TRAITEMENT — ① prendre la docstring du module par l'arbre syntaxique · ② chercher une ligne
      « fonction_signal = <nom> » et une ligne « reglages_signal = <objet JSON> » · ③ sans réglages : « {} ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les modules RSI(2) et hasard écrivent déjà ces lignes (« COMMENT UNE FICHE LE NOMME ») ; les lire
      évite une liste écrite à la main des modules et de leurs réglages.
    ⑨ CE QUI CLOCHE — La ligne doit être écrite seule (espaces autour du « = » permis) ; une autre écriture n'est pas
      lue, et le module devient inéprouvable s'il n'a pas de fiche (ce qui fait rougir : voulu).
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    doc = ast.get_docstring(ast.parse(open(chemin, "rb").read(), chemin)) or ""
    fonction = texte = None
    for ligne in doc.splitlines():
        m = re.match(r"^\s*fonction_signal\s*=\s*([A-Za-z_]\w*)\s*$", ligne)
        if m and fonction is None:
            fonction = m.group(1)
        m = re.match(r"^\s*reglages_signal\s*=\s*(\{.*\})\s*$", ligne)
        if m and texte is None:
            texte = m.group(1)
    if fonction is None:
        return None, "aucune ligne « fonction_signal = » dans sa déclaration"
    try:
        r = json.loads(texte or "{}")
    except ValueError as e:
        return None, "réglages d'exemple illisibles : %r (%s)" % (texte, e)
    if not isinstance(r, dict):
        return None, "réglages d'exemple illisibles : %r" % texte
    return fonction, json.dumps(r, sort_keys=True)


def ajouter(trouves, module, fonction, reglages, source):
    """Range un signal à éprouver, un seul exemplaire par (module, fonction, réglages).

    ① RÔLE — Ne pas éprouver deux fois le même signal, sans jamais fondre deux réglages différents.
    ② CONTEXTE D'APPEL — `signaux_a_eprouver`, pour chaque déclaration et chaque fiche.
    ③ ENTRÉE — `trouves` : le dictionnaire en cours · `module` : chemin relatif · `fonction` : nom · `reglages` : texte
      JSON trié · `source` : d'où vient ce signal (une fiche, une déclaration).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur ; `trouves` est complété. [rend: 0]
    ⑥ TRAITEMENT — La clé est le triple ; la source s'ajoute à la liste du signal.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les trois fiches C5 du registre nomment le même triple : il s'éprouve une fois. Des réglages
      différents font un autre signal (A4 : un décalage de −1 lit l'avenir, un décalage de 0 non).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Modifie `trouves`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    cle = (module, fonction, reglages)
    trouves.setdefault(cle, {"module": module, "fonction": fonction, "reglages": reglages, "sources": []})
    trouves[cle]["sources"].append(source)


def signaux_a_eprouver(racine):
    """Trouve, PAR PROPRIÉTÉ, les signaux à éprouver : les modules déclarés et les fiches du registre.

    ① RÔLE — La liste des signaux que l'épreuve doit faire passer, sans liste écrite à la main.
    ② CONTEXTE D'APPEL — `cas`, une fois par copie.
    ③ ENTRÉE — `racine` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — `programmes/` et le registre des stratégies (REGISTRE_DES_STRATEGIES du contrat) existent
      sous la racine.
    ⑤ SORTIE — TROIS valeurs : la liste des signaux (dictionnaires module, fonction, réglages, sources) ; la liste des
      modules déclarés inéprouvables (chemin, motif) ; la liste des fiches écartées parce que le juge lui-même refuse
      leur signal (identifiant, motif). [rend: 3]
    ⑥ TRAITEMENT — ① chaque fichier `.py` de `programmes/` qui se déclare module de signal (`declaration_de_signal`
      du juge, sans exécution) : son exemple, s'il en a un · ② chaque fiche du registre, lue par `lire_les_fiches` du
      contrat (une par identifiant, sa DERNIÈRE ligne : n°83, depuis le 05-11-2026), dont la colonne `module_signal`
      n'est pas vide : son triple, si `manques_du_signal` du juge n'y trouve rien, sinon la fiche est écartée · ③ un module
      déclaré qu'aucun signal trouvé n'emploie est inéprouvable.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Si je renomme un fichier, ce contrôle ne change pas d'avis : il ne nomme aucun module. Un module
      déposé demain avec une déclaration est éprouvé sans que personne pense à l'ajouter (sabotage Sd).
    ⑨ CE QUI CLOCHE — ① Une fiche écartée (signal mal déclaré) n'est pas éprouvée : le juge ne peut pas la jouer non
      plus. ② Un module déclaré hors de `programmes/`, ou dans un SOUS-DOSSIER de `programmes/` (non lu), n'est trouvé
      que par une fiche.
    ⑩ EFFET — Lit les fichiers de `programmes/` et le registre ; n'exécute aucun module.
    ⑪ TERMINAISON — Rend la main, ou lève si le registre ne se lit pas. [sort: non]
    """
    B = juge(racine)
    trouves, declares, ineprouvables, ecartes = {}, {}, [], []
    dossier = os.path.join(racine, "programmes")
    for f in sorted(os.listdir(dossier)):
        if not f.endswith(".py"):
            continue
        _ligne, refus = B.declaration_de_signal(os.path.join(dossier, f))
        if refus:
            continue
        declares["programmes/" + f] = exemple_de_la_declaration(os.path.join(dossier, f))
    for module, (fonction, reglages) in declares.items():
        if fonction:
            ajouter(trouves, module, fonction, reglages, "déclaration")
    for fiche in contrat(racine).lire_les_fiches(racine).values():
        if (fiche.get("module_signal") or "").strip().lower() in B.VIDE:
            continue
        manq = B.manques_du_signal(fiche)
        if manq:
            ecartes.append((fiche.get("id"), " ; ".join(manq)))
            continue
        texte = (fiche.get("reglages_signal") or "").strip()
        reglages = json.dumps(json.loads(texte) if texte.lower() not in B.VIDE else {}, sort_keys=True)
        ajouter(trouves, fiche["module_signal"].strip(), fiche["fonction_signal"].strip(), reglages, "fiche " + fiche["id"])
    employes = {t["module"] for t in trouves.values()}
    for module, (fonction, motif) in declares.items():
        if module not in employes:
            ineprouvables.append((module, motif if not fonction else "jamais employé"))
    return list(trouves.values()), ineprouvables, ecartes


def comparer(sig, s):
    """Compare, pour chacune des FENETRE dernières dates, le signal sur la série coupée à ce jour et sur la série entière.

    ① RÔLE — Le cœur du test : dire si un signal se sert de l'avenir sur une série.
    ② CONTEXTE D'APPEL — `eprouver_un_signal`, une fois par valeur.
    ③ ENTRÉE — `sig` : le signal (un `SignalNomme` du juge, fraîchement chargé) · `s` : la série ENTIÈRE d'une valeur,
      celle que le juge joue.
    ④ CONDITIONS D'ENTRÉE — `s` est triée par date.
    ⑤ SORTIE — TROIS valeurs : le motif (None si aucun écart, sinon la date et le sens de l'écart), le nombre de dates
      coupées (au plus FENETRE), le nombre de ces dates signalées sur la série entière. Exemple : le tricheur
      `filtre_lendemain` rend (« le 2026-07-16 : signalé sur la série coupée seulement », 400, …). [rend: 3]
    ⑥ TRAITEMENT — ① les FENETRE dernières dates de la série, dans l'ordre croissant · ② pour chaque jour J, la série
      coupée à J, depuis l'ORIGINE de la série ; noter si J (sa dernière séance) est signalé · ③ la série entière,
      EN DERNIER · ④ refuser au premier jour où les deux diffèrent, dans un sens ou dans l'autre ; une sortie mal
      formée ou une erreur du signal sur une coupe est aussi un refus — SAUF une erreur de l'environnement
      (MemoryError, OSError et ses sous-classes), RELANCÉE : ce n'est pas un verdict (depuis le 05-11-2026).
    ⑦ UNITÉ — Des rangs dans la série ; des dates AAAA-MM-JJ dans le motif.
    ⑧ POURQUOI — Le soir, le signal se calcule sur des cours qui s'arrêtent au jour du signal : c'est la série coupée.
      La référence est la série entière parce que c'est elle que le juge joue (superviseur R-759 du tour 3). Les deux
      sens : une fuite qui AJOUTE des achats (`frequent_plus_fuite_rare`) et une fuite qui en RETIRE
      (`filtre_lendemain`). L'ordre et la place de la série entière : voir ⑧ de l'en-tête.
    ⑨ CE QUI CLOCHE — ① Le coût est d'un calcul du signal par date coupée, sur une série qui va de L − FENETRE à L
      séances (environ 7,3 s par valeur pour C5 le 01-11-2026 : 293 s sur 40 valeurs) ; il croît avec la longueur L du maître. ② Le nombre de
      dates signalées est une information ; un signal qui n'en signale aucune n'est pas refusé pour cela (superviseur
      du tour 3 : un refus ferait rougir un signal honnête et rare). ③ Un signal qui LÈVE LUI-MÊME une OSError ou une
      MemoryError (une lecture de fichier ratée dans sa logique, par exemple) n'a pas de verdict : l'épreuve rend 2,
      jamais un refus. Le cas est voulu (un contrôle qui n'a pas pu tourner ne rend ni vert ni mordu, R-734) ; la
      cause se lit dans la ligne « PAS DE VERDICT ». ④ L'appel sur la série ENTIÈRE n'est pas dans le `try` : toute
      erreur y arrête le processus sans verdict, comme avant.
    ⑩ EFFET — Celui de la fonction de signal.
    ⑪ TERMINAISON — Rend la main, ou relance une MemoryError ou une OSError du signal ; un appel de la fonction de
      signal peut ne pas revenir (le délai du sous-processus l'arrête). [sort: non]
    """
    dates = list(range(max(0, len(s) - FENETRE), len(s)))
    coupes = {}
    for j in dates:
        coupe = s[:j + 1]
        try:
            sortie = sig(coupe)
        except (MemoryError, OSError):
            # UNE ERREUR DE LA MACHINE N'EST PAS UNE CONCLUSION SUR LE SIGNAL (superviseur R-759 du 05-11-2026, après
            # le tour final, défaut 4) : relancée, elle arrête le processus en code 1 sans ligne « REFUSÉ · », donc
            # sans verdict (T3-3) ; rattrapée comme les autres, elle devenait un refus en bonne forme, et un sabotage
            # pouvait être compté « mord » sur un disque plein. Critère : la famille d'erreurs de l'environnement
            # (mémoire, système de fichiers), jamais une liste de messages.
            raise
        except Exception as e:
            return ("sur la série coupée au %s : %s : %s" % (s[j]["date"], type(e).__name__, str(e)[:160]),
                    len(coupes), 0)
        coupes[j] = any(x["i"] == len(coupe) - 1 for x in sortie)
    entiere = {x["i"] for x in sig(s)}
    signalees = sum(1 for j in dates if j in entiere)
    for j in dates:
        if coupes[j] != (j in entiere):
            return ("le %s : signalé sur la %s seulement" % (s[j]["date"], "série coupée" if coupes[j] else "série entière"),
                    len(dates), signalees)
    return None, len(dates), signalees


def eprouver_un_signal(racine, module, fonction, reglages):
    """Éprouve UN signal sur toutes les valeurs, dans ce processus neuf, et rend son verdict.

    ① RÔLE — Le mode « --signal » : un signal, un processus.
    ② CONTEXTE D'APPEL — Ce programme relancé par `cas`, une fois par signal trouvé.
    ③ ENTRÉE — `racine` · `module` : chemin relatif · `fonction` : nom · `reglages` : texte JSON.
    ④ CONDITIONS D'ENTRÉE — Le fichier maître des cours et le référentiel existent sous la racine.
    ⑤ SORTIE — DEUX valeurs : le code (0 passe, 1 refusé, 3 non jouable par le juge) et la ligne du verdict. [rend: 2]
    ⑥ TRAITEMENT — ① lire les cours par le lecteur du juge · ② pour chaque valeur, dans l'ordre alphabétique : oublier
      les modules de signal chargés par le juge, et les modules du DÉPÔT importés depuis le début (ceux dont le
      fichier est sous la racine), recharger le signal par
      `signal_de_la_fiche` (la même lecture que le juge), prendre la série ENTIÈRE de la valeur et `comparer` ·
      ③ s'arrêter au premier refus ; la ligne PASSE compte les dates COUPÉES (au plus FENETRE par valeur), et, pour
      information, celles qui sont signalées.
    ⑦ UNITÉ — Des séances, des secondes.
    ⑧ POURQUOI — Un état neuf pour chaque valeur : un module ne peut rien retenir d'une valeur à l'autre.
    ⑨ CE QUI CLOCHE — ① Un état gardé hors des modules (un fichier, une variable d'environnement) n'est pas oublié (⑨ ①
      de l'en-tête). ② Les modules de Python et des bibliothèques installées (numpy…) ne sont pas oubliés d'une
      valeur à l'autre : une bibliothèque compilée ne se recharge pas sans risque ; un état gardé là passerait d'une
      valeur à la suivante (jamais d'un signal à l'autre : un processus par signal).
    ⑩ EFFET — Exécute le module de signal, autant de fois qu'il y a de valeurs.
    ⑪ TERMINAISON — Rend la main ; borné par le délai que `cas` donne au sous-processus. [sort: non]
    """
    os.chdir(racine)
    B = juge(racine)
    mnemo = B.table_mnemoniques(B.trouver(".", "REFERENTIEL_VALEURS"))
    cours, _lecture = B.lire_par_le_lecteur(".", "donnees/cours_maitre.csv", mnemo)
    fiche = {"id": "ARRIVEE", "module_signal": module, "fonction_signal": fonction, "reglages_signal": reglages}
    deja = set(sys.modules)
    sous_la_racine = lambda m: os.path.realpath(getattr(m, "__file__", None) or "/").startswith(os.path.realpath(racine) + os.sep)
    t0, n, ns = time.time(), 0, 0
    for v in sorted(cours):
        for nom in [m for m in list(sys.modules) if m not in deja and sous_la_racine(sys.modules[m])]:
            del sys.modules[nom]
        B._MODULES_DE_SIGNAL.clear()
        try:
            sig = B.signal_de_la_fiche(".", fiche)
        except ValueError as e:
            return 3, "NON JOUABLE · %s" % str(e)[:220]
        s = cours[v]
        motif, coupees, signalees = comparer(sig, s)
        if motif:
            return 1, "REFUSÉ · %s %s · %.1f s" % (v, motif, time.time() - t0)
        n, ns = n + coupees, ns + signalees
    return 0, ("PASSE · %d valeurs · %d dates coupées (les %d dernières de chaque série entière), dont %d signalées · %.1f s"
               % (len(cours), n, FENETRE, ns, time.time() - t0))


def poser_les_modules_et_la_fiche(copie):
    """Dépose dans la copie les modules d'épreuve et ajoute la fiche d'épreuve en tête du registre.

    ① RÔLE — Préparer les tricheurs et les cas fabriqués, dans la COPIE seulement.
    ② CONTEXTE D'APPEL — `cas`, une fois.
    ③ ENTRÉE — `copie` : la racine de la copie.
    ④ CONDITIONS D'ENTRÉE — Le registre de la copie existe et porte les colonnes du signal.
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — ① écrire chaque fichier de `MODULES_D_EPREUVE` dans `programmes/`, le témoin « sans verdict »
      compris · ② écrire `FICHE_D_EPREUVE` juste après l'en-tête du registre (son chemin pris au contrat), les autres
      colonnes vides, fins de ligne CRLF comme le registre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les tricheurs sont trouvés par la MÊME recherche que les vrais modules : si elle les manque, A3
      rougit (sabotage Sd).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans la COPIE, jamais dans le dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    for nom, (texte, _attendu) in MODULES_D_EPREUVE.items():
        open(os.path.join(copie, "programmes", nom), "w", encoding="utf-8").write(texte)
    p = os.path.join(copie, contrat(copie).REGISTRE_DES_STRATEGIES)     # le chemin vit au contrat (n°83)
    entete = next(csv.reader(open(p, encoding="utf-8-sig")))
    tampon = io.StringIO()
    csv.writer(tampon, lineterminator="\r\n").writerow([FICHE_D_EPREUVE.get(c, "") for c in entete])
    brut = open(p, "rb").read().decode("utf-8")
    k = brut.index("\n") + 1
    with open(p, "w", encoding="utf-8", newline="") as h:
        h.write(brut[:k] + tampon.getvalue() + brut[k:])


def lancer(copie, *arguments, delai=900):
    """Lance un programme Python dans la copie et rend son code et sa sortie.

    ① RÔLE — Un seul geste pour tous les lancements.
    ② CONTEXTE D'APPEL — `cas` (un signal par processus) ; le programme principal (mode « --cas »).
    ③ ENTRÉE — `copie` : la racine · `arguments` : le programme et ses arguments · `delai` : en secondes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé), la sortie, erreurs comprises. [rend: 2]
    ⑥ TRAITEMENT — `python3 -B` depuis la racine de la copie.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Un processus neuf par signal : rien de ce qu'un module a chargé ou retenu ne passe à un autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ce que fait le programme lancé ; dans la copie seulement.
    ⑪ TERMINAISON — Rend la main ; borné par le délai. [sort: non]
    """
    try:
        r = subprocess.run([sys.executable, "-B"] + list(arguments), cwd=copie, capture_output=True, text=True,
                           timeout=delai)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 124, "délai de %d s dépassé" % delai


def verdict_du_lancement(code, sortie):
    """Rend la ligne de verdict d'un lancement « --signal », ou None s'il n'a pas rendu de verdict (T3-3).

    ① RÔLE — Dire, par une PROPRIÉTÉ du lancement (son code ET sa ligne), si un signal a été jugé.
    ② CONTEXTE D'APPEL — `cas`, une fois par signal lancé (le témoin « sans verdict » compris), et une fois par exemple
      écrit du cas A6.
    ③ ENTRÉE — `code` : le code de sortie rendu par `lancer` (124 pour un délai dépassé) · `sortie` : sa sortie,
      erreurs comprises (la sortie d'erreur APRÈS la sortie normale, comme `lancer` les met).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la DERNIÈRE ligne qui commence par « PASSE · » quand le code est 0, ou par « REFUSÉ · »
      quand le code est 1 ; None dans tous les autres cas (délai dépassé, code 124 ; plantage Python, code 1 sans
      ligne « REFUSÉ · » ; processus tué, code négatif ; « NON JOUABLE », code 3 ; code 0 sans ligne « PASSE · »).
      Exemples (cas A6) : (124, « PASSE · … ») → None ; (1, « Traceback… ») → None ; le témoin, qui plante par
      MemoryError relancée par `comparer` : (1, « …MemoryError: plantage simulé… ») → None. [rend: 1]
    ⑥ TRAITEMENT — choisir le début attendu selon le code ; chercher, de la dernière ligne à la première, une ligne
      qui commence par lui.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du tour 4 (01-11-2026), T3-3 : un signal honnête arrêté par son délai, ou qui
      plantait, faisait rougir A1 ou A2, et un sabotage sans effet était compté « mord » (mesure R24 du relecteur du
      tour 3 : délai d'un signal ramené à 2 s). Sortie de `cas` en fonction le 05-11-2026 (superviseur R-759 de la
      nuit, défaut 1) : « un sabotage ne peut viser qu'une règle qu'un cas peut appeler » — A6 l'appelle.
    ⑨ CE QUI CLOCHE — Un module de signal qui écrit lui-même une ligne « REFUSÉ · … » puis sort en code 1 passe pour
      un verdict rendu (un tricheur de la limite ⑥ de l'en-tête ; lu par le relecteur, non joué ; au BACKLOG).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    attendue = {0: "PASSE · ", 1: "REFUSÉ · "}.get(code)
    lignes = sortie.strip().splitlines()
    return next((l for l in reversed(lignes) if attendue and l.startswith(attendue)), None)


def code_des_cas(resultats, sans_verdict):
    """Rend le code de sortie du mode « --cas » : 2 si un signal non témoin n'a pas rendu de verdict, sinon 0 ou 1 (T3-3).

    ① RÔLE — Écrire en un seul endroit la règle « un contrôle qui n'a pas pu tourner ne rend ni vert ni mordu ».
    ② CONTEXTE D'APPEL — Le mode « --cas » du programme principal, une fois ; le cas A6, sur des exemples.
    ③ ENTRÉE — `resultats` : la liste des (nom, réussi, détail) rendue par `cas` · `sans_verdict` : la liste des
      lancements sans verdict rendue par `cas`, des (module, réglages, code, dernière ligne).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 2 si `sans_verdict` porte un lancement INATTENDU (un module qui n'est pas un témoin de
      TEMOINS_SANS_VERDICT) ; sinon 0 si chaque cas est réussi, 1 sinon. Exemples (cas A6) : ([(« x », True, «  »)],
      [(« programmes/MODULE_X.py », « {} », 124, « délai »)]) → 2 ; ([(« x », True, «  »)], [le témoin]) → 0. [rend: 1]
    ⑥ TRAITEMENT — ① écarter les témoins, qui sont attendus sans verdict · ② une expression.
    ⑦ UNITÉ — Un code de sortie.
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0. Avec 2, Z0 est rouge et un sabotage « NE
      MORD PAS » (le programme principal exige le code 1 pour « mord »). Sortie de l'expression du programme
      principal le 05-11-2026 pour que le sabotage T3_3a ait un cas qui l'appelle (A6). Les témoins sont écartés par
      leur ATTENDU déclaré dans MODULES_D_EPREUVE, une propriété de l'épreuve et non une liste du dépôt (superviseur
      R-759 du 05-11-2026, après le tour final, défaut 1, point 3).
    ⑨ CE QUI CLOCHE — Un module du DÉPÔT qui porterait le nom d'un témoin (`programmes/EPREUVE_ARRIVEE_PLANTE.py`)
      serait écrasé dans la copie par le témoin : il n'est de toute façon pas éprouvé (limite ⑧ de l'en-tête).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    inattendus = [x for x in sans_verdict if x[0] not in TEMOINS_SANS_VERDICT]
    return 2 if inattendus else 0 if all(ok for _, ok, _ in resultats) else 1


def nommer_ce_qui_ne_passe_pas(signaux, verdicts):
    """Nomme chaque signal qui ne passe pas : son module, ses réglages et le début de son verdict (T3-5).

    ① RÔLE — Dire, dans la ligne d'un cas rouge, QUEL signal a été refusé, sans aller le chercher à la main.
    ② CONTEXTE D'APPEL — `cas` : A1 l'applique aux signaux du dépôt, A3 aux tricheurs (refusés à chaque Z0 par
      construction, donc nommés à chaque Z0).
    ③ ENTRÉE — `signaux` : des dictionnaires portant « module » et « reglages » (ceux de `signaux_a_eprouver`) ·
      `verdicts` : {(module, réglages) : (code, ligne)} rempli par `cas`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des textes « <module> <réglages> → <90 premiers caractères du verdict> », un par
      signal dont le code n'est pas 0, dans l'ordre de `signaux` ; « NON ÉPROUVÉ » quand le signal n'a pas de verdict.
      Exemple réel (sabotage Sf, 04-11-2026) : « programmes/MODULE_SIGNAL_RSI2_CONNORS.py {"periode": 2, "seuil": 10,
      "tendance": 200} → REFUSÉ · ACCOR le 2025-05-23 : signalé sur la série entière seulement · 0.0 s ». [rend: 1]
    ⑥ TRAITEMENT — Une liste en compréhension.
    ⑦ UNITÉ — Des caractères (90).
    ⑧ POURQUOI — Superviseur R-759 du tour 4, T3-5 : sous le sabotage Sf, la ligne rouge de A1 ne disait pas quel
      signal avait été refusé (c'était le RSI(2), vu à la main). Sortie de A1 en fonction le 05-11-2026 (superviseur
      R-759 de la nuit, défaut 1, point 3) : appliquée aux tricheurs que l'épreuve dépose elle-même, la dent tient à
      l'épreuve et non à un module du dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return ["%s %s → %s" % (sg["module"], sg["reglages"],
                            verdicts.get((sg["module"], sg["reglages"]), (None, "NON ÉPROUVÉ"))[1][:90])
            for sg in signaux if verdicts.get((sg["module"], sg["reglages"]), (None, ""))[0] != 0]


def cas(copie):
    """Joue les cas A1 à A6 dans une copie, et rend la liste de leurs verdicts.

    ① RÔLE — Chaque cas dit vert ou rouge, avec ce qu'il a vu.
    ② CONTEXTE D'APPEL — Le mode « --cas » de ce programme, une fois par copie (Z0 ou un sabotage).
    ③ ENTRÉE — `copie` : la racine d'une copie du dépôt, éventuellement sabotée.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — DEUX valeurs : la liste des (nom, réussi, détail) ; la liste des lancements « --signal » SANS VERDICT,
      un (module, réglages, code, dernière ligne) par lancement, vide quand chaque signal a rendu son verdict.
      Exemple : délai d'un signal ramené à 2 s, chaque signal est arrêté (code 124) et figure dans la seconde liste.
      [rend: 2]
    ⑥ TRAITEMENT — ① poser les modules et la fiche d'épreuve (le témoin « sans verdict » compris) · ② trouver les
      signaux · ③ éprouver chacun dans un
      sous-processus neuf (mode « --signal »), afficher son verdict, et le RANGER : « verdict rendu » si le code est 0
      avec une ligne qui commence par « PASSE · », ou 1 avec une ligne qui commence par « REFUSÉ · » ; « pas de
      verdict » pour tout le reste (délai dépassé, code 124 ; plantage Python non rattrapé, code 1 sans ligne
      « REFUSÉ · » — une erreur de l'environnement, MemoryError ou OSError, en est une depuis le 05-11-2026, parce que
      `comparer` la relance ; une autre erreur du signal sur une coupe reste un refus en bonne forme ; processus tué,
      code négatif ; « NON JOUABLE », code 3) · ④ lire la longueur des séries du maître (lecteur du juge) pour le
      contrôle du seuil des tricheurs X5 et X6 · ⑤ juger A1 à A5 ; A1 NOMME chaque signal du dépôt qui ne passe pas,
      et le module de la vraie ligne C5E10-QA-V1 ; A3 exige que chaque tricheur refusé soit nommé
      (`nommer_ce_qui_ne_passe_pas`) · ⑥ A6 : éprouver `verdict_du_lancement` et `code_des_cas` sur des exemples
      écrits. Le rangement « verdict rendu / pas de verdict » est fait par `verdict_du_lancement`. Le témoin « sans
      verdict » n'est jugé par AUCUN cas : la boucle extérieure exige sa ligne « PAS DE VERDICT ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête. Le rangement « verdict rendu / pas de verdict » est une PROPRIÉTÉ et non une liste
      de messages (superviseur R-759 du tour 4, 01-11-2026, T3-3, « la correction proposée — refuser une ligne
      « délai … dépassé » — est une rustine ») : avant lui, un signal honnête arrêté par son délai, ou qui plantait,
      faisait rougir A1 ou A2, et un sabotage sans effet était compté « mord » (exemple mesuré par le relecteur du tour
      3, R24 : un sabotage qui ne change rien, délai d'un signal ramené à 2 s). Un seul « pas de verdict » suffit à
      rendre 2 : un contrôle qui n'a pas pu tourner ne rend pas un verdict (R-734). Le nom dans A1 : T3-5 du même
      superviseur — sous le sabotage Sf, la ligne rouge de A1 ne disait pas quel signal avait été refusé (c'était le
      RSI(2), vu à la main).
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨. La ligne du verdict est cherchée parmi toutes les lignes du lancement, la
      dernière qui commence par « PASSE · » ou « REFUSÉ · » (la sortie d'erreur est mise APRÈS la sortie normale par
      `lancer`, un avertissement d'une bibliothèque y passerait sinon pour la dernière ligne).
    ⑩ EFFET — Écrit dans la copie ; lance un sous-processus par signal, le témoin compris.
    ⑪ TERMINAISON — Rend la main ; chaque sous-processus est borné. [sort: non]
    """
    poser_les_modules_et_la_fiche(copie)
    signaux, ineprouvables, ecartes = signaux_a_eprouver(copie)
    verdicts, sans_verdict = {}, []
    for sg in signaux:
        code, sortie = lancer(copie, os.path.join(copie, SOI), "--signal", copie, sg["module"], sg["fonction"],
                              sg["reglages"], delai=DELAI_D_UN_SIGNAL)
        # T3-3 : le verdict rendu est une propriété du lancement (son code ET sa ligne), jamais un message épelé
        ligne = verdict_du_lancement(code, sortie)
        if ligne is None:
            ligne = (sortie.strip().splitlines() or ["(aucune sortie)"])[-1]
            sans_verdict.append((sg["module"], sg["reglages"], code, ligne[:160]))
        verdicts[(sg["module"], sg["reglages"])] = (code, ligne)
        print("  signal %s · %s · réglages %s · %s\n      -> code %d · %s"
              % (sg["module"], sg["fonction"], sg["reglages"], ", ".join(sg["sources"]), code, ligne), flush=True)
    for e in ecartes:
        print("  fiche écartée (le juge refuse aussi son signal) : %s · %s" % e)
    for m in ineprouvables:
        print("  module déclaré INÉPROUVABLE : %s · %s" % m)
    res = []
    du_depot = [sg for sg in signaux if not sg["module"].startswith("programmes/" + PREFIXE)]
    passe = lambda module, reglages: verdicts.get((module, reglages), (None, ""))[0] == 0
    refuse = lambda module, reglages: (verdicts.get((module, reglages), (None, ""))[0] == 1
                                       and " seulement" in verdicts[(module, reglages)][1])
    # A1 le dépôt
    qa = [sg for sg in du_depot if "fiche C5E10-QA-V1" in sg["sources"]]
    ine_depot = [m for m in ineprouvables if not m[0].startswith("programmes/" + PREFIXE)]
    # T3-5 : A1 nomme chaque signal du dépôt qui ne passe pas, avec le début de son verdict
    ne_passent_pas = nommer_ce_qui_ne_passe_pas(du_depot, verdicts)
    vu ={"%d signaux du dépôt, tous passent%s" % (len(du_depot), (" (ne passent pas : %s)" % " ; ".join(ne_passent_pas))
                                                    if ne_passent_pas else ""):
          bool(du_depot) and not ne_passent_pas,
          # le module est NOMMÉ dans l'élément (la boucle extérieure exige que tout élément rouge de A1 nomme un module)
          "la vraie ligne C5E10-QA-V1 éprouvée (%s)" % (" ; ".join("%s %s" % (x["module"], x["reglages"]) for x in qa)
                                                       or "absente des signaux trouvés"):
              len(qa) == 1 and passe(qa[0]["module"], qa[0]["reglages"]),
          "aucun module déclaré du dépôt inéprouvable %s" % ine_depot: not ine_depot}
    res.append(("A1 chaque signal du dépôt passe", all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())))
    # A2 à A5 les modules et la fiche d'épreuve
    vu2, vu3, vu5 = {}, {}, {}
    for nom, (texte, attendu) in MODULES_D_EPREUVE.items():
        module = "programmes/" + nom
        _f, reglages = exemple_de_la_declaration(os.path.join(copie, "programmes", nom))
        if attendu == "PASSE":
            vu2["%s passe" % nom] = passe(module, reglages)
        elif attendu == "REFUSÉ":
            vu3["%s éprouvé et refusé (%s)" % (nom, verdicts.get((module, reglages), (None, "NON ÉPROUVÉ"))[1][:90])] = refuse(module, reglages)
        elif attendu == "INÉPROUVABLE":
            vu5["%s inéprouvable" % nom] = any(m[0] == module for m in ineprouvables)
        # attendu « SANS VERDICT » (le témoin) : jugé par la boucle extérieure, sur la ligne « PAS DE VERDICT » que le
        # programme principal imprime — jamais ici, où un sabotage du rangement le ferait taire avec lui (tour de n°83)
    # R-734 : les tricheurs X5 et X6 n'ont de dents que si leur seuil dépasse FENETRE et qu'une valeur l'atteint
    B = juge(copie)
    _cours, _l = B.lire_par_le_lecteur(copie, "donnees/cours_maitre.csv",
                                       B.table_mnemoniques(B.trouver(copie, "REFERENTIEL_VALEURS")))
    longues = sum(1 for _s in _cours.values() if len(_s) >= SEUIL_DES_TRICHEURS_LONGS)
    vu3["seuil des tricheurs longs %d au-dessus de FENETRE %d et atteint par %d valeurs du maître (plus longue %d)"
        % (SEUIL_DES_TRICHEURS_LONGS, FENETRE, longues, max([len(_s) for _s in _cours.values()] or [0]))] = (
        SEUIL_DES_TRICHEURS_LONGS > FENETRE and longues > 0)
    # T3-5, dent permanente (superviseur R-759 du 05-11-2026, défaut 1, point 3) : chaque tricheur refusé est NOMMÉ
    # par `nommer_ce_qui_ne_passe_pas` — son module, ses réglages et le début de son verdict, dans un même texte
    tricheurs = [sg for sg in signaux if sg["module"].startswith("programmes/" + PREFIXE)
                 and MODULES_D_EPREUVE.get(sg["module"][len("programmes/"):], ("", ""))[1] == "REFUSÉ"
                 and refuse(sg["module"], sg["reglages"])]
    noms = nommer_ce_qui_ne_passe_pas(tricheurs, verdicts)
    pas_nommes = [sg["module"] for sg in tricheurs
                  if not any(sg["module"] in n and sg["reglages"] in n and verdicts[(sg["module"], sg["reglages"])][1][:40] in n
                             for n in noms)]
    vu3["%d tricheurs refusés, chacun nommé par module, réglages et verdict%s" % (
        len(tricheurs), (" (pas nommés : %s)" % ", ".join(pas_nommes)) if pas_nommes else "")] = bool(tricheurs) and not pas_nommes
    for nom, vu_ in (("A2 le module d'épreuve honnête passe", vu2), ("A3 chaque tricheur est éprouvé et refusé", vu3),
                     ("A5 un module déclaré sans exemple ni fiche est inéprouvable", vu5)):
        res.append((nom, bool(vu_) and all(vu_.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu_.items())))
    cle_fiche = (FICHE_D_EPREUVE["module_signal"], json.dumps(json.loads(FICHE_D_EPREUVE["reglages_signal"]), sort_keys=True))
    vu4 = {"fiche %s (réglages %s) éprouvée et refusée (%s)" % (FICHE_D_EPREUVE["id"], cle_fiche[1],
                                                                  verdicts.get(cle_fiche, (None, "NON ÉPROUVÉE"))[1][:90]): refuse(*cle_fiche)}
    res.append(("A4 les réglages d'une fiche sont éprouvés", all(vu4.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu4.items())))
    # A6 (superviseur R-759 du 05-11-2026, défaut 1) : un lancement sans verdict n'est pas un verdict — sur des
    # EXEMPLES ÉCRITS, la dent du sabotage T3_3a. Le BRANCHEMENT de la règle dans le vrai chemin est éprouvé par le
    # témoin « sans verdict », lancé dans la boucle des signaux plus haut, et jugé par la boucle extérieure (tour de
    # n°83 ; avant, un module qui plante était lancé ici, à part, et ses dents ne défendaient que les fonctions).
    exemple_sans_verdict = ("programmes/MODULE_X.py", "{}", 124, "délai de 1800 s dépassé")
    exemple_temoin = (TEMOINS_SANS_VERDICT[0], "{}", 1, "MemoryError: plantage simulé") if TEMOINS_SANS_VERDICT else None
    vu6 = {"délai dépassé (124) avec une ligne « PASSE · » : aucun verdict": verdict_du_lancement(124, "PASSE · 40 valeurs") is None,
           "code 1 avec une trace Python : aucun verdict": verdict_du_lancement(1, "Traceback (most recent call last):\nRuntimeError: x") is None,
           "code 1 avec une ligne « REFUSÉ · » : verdict rendu": verdict_du_lancement(1, "REFUSÉ · ACCOR le 2025-05-23") is not None,
           "un cas réussi et un lancement sans verdict inattendu : code 2": code_des_cas([("x", True, "")], [exemple_sans_verdict]) == 2,
           "un cas réussi et le seul témoin sans verdict : code 0": exemple_temoin is not None and code_des_cas([("x", True, "")], [exemple_temoin]) == 0,
           "tous les cas réussis, chaque verdict rendu : code 0": code_des_cas([("x", True, "")], []) == 0}
    res.append(("A6 un lancement sans verdict n'est pas un verdict", all(vu6.values()),
                " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu6.items())))
    res.sort(key=lambda x: x[0])
    return res, sans_verdict


def preparer(depot, sab):
    """Copie le dépôt et applique un sabotage à la copie de CE fichier.

    ① RÔLE — Donner à chaque sabotage sa copie, pour que rien ne touche au dépôt.
    ② CONTEXTE D'APPEL — Le programme principal, une fois par sabotage joué.
    ③ ENTRÉE — `depot` : la racine · `sab` : le nom du sabotage, ou « Z0 » (aucun remplacement).
    ④ CONDITIONS D'ENTRÉE — Chaque cible du sabotage existe UNE fois dans son fichier.
    ⑤ SORTIE — DEUX valeurs : le dossier temporaire et la racine de la copie. [rend: 2]
    ⑥ TRAITEMENT — ① copier sans .git, etudes, caches · ② remplacer chaque cible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une cible introuvable ne sabote rien : elle lève au lieu de passer pour un sabotage qui mord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un dossier temporaire (dans TMPDIR s'il est posé).
    ⑪ TERMINAISON — Rend la main, ou lève AssertionError. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="arrivee_signaux_")
    r = os.path.join(d, "r")
    shutil.copytree(depot, r, ignore=shutil.ignore_patterns(".git", "etudes", "__pycache__", "_site_travail"))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(r, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, "%s : cible trouvée %d fois dans %s : %r" % (sab, t.count(a), f, a[:60])
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d, r


def ce_que_le_lancement_n_a_pas_porte(sortie):
    """Dit ce qu'un lancement « --cas » n'a pas porté : la ligne de chaque témoin, un module dans chaque rouge de A1.

    ① RÔLE — Le constat par le processus NON SABOTÉ (superviseur R-759 du 05-11-2026, après le tour final, défaut 1,
      points 4 et 5) : le chemin réel de l'épreuve a traversé la chaîne « pas de verdict » (`lancer` →
      `verdict_du_lancement` → le rangement dans `cas` → l'impression « PAS DE VERDICT »), et toute ligne rouge de A1
      dit QUEL signal (T3-5).
    ② CONTEXTE D'APPEL — Le programme principal, une fois par lancement, pour Z0 et pour chaque sabotage. Il tourne dans
      le fichier du DÉPÔT : `preparer` sabote la COPIE de ce fichier, et le lancement « --cas » est celui de la copie ;
      aucun sabotage de SABOTAGES ne peut donc l'atteindre.
    ③ ENTRÉE — `sortie` : la sortie entière du lancement « --cas » (sortie normale puis erreurs).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des manques, vide quand tout est porté. Exemples : sous le sabotage X1 du
      relecteur (le rangement débranché), « la ligne « PAS DE VERDICT » du témoin programmes/EPREUVE_ARRIVEE_PLANTE.py
      manque » ; sous Sf combiné à X3 (A1 sans nomination), « un élément rouge de A1 ne nomme aucun module : … ».
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque témoin de TEMOINS_SANS_VERDICT, chercher la ligne « PAS DE VERDICT : signal <témoin> · »
      · ② pour la ligne « ÉCHEC » de A1, s'il y en a une, couper ses éléments comme le fait l'affichage des sabotages,
      et exiger dans chaque élément rouge (« … NON ») un chemin `programmes/<…>.py`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relecteur du 05-11-2026 a joué trois sabotages de BRANCHEMENT (X1 rangement débranché, X2 maillon 3
      ignoré, X3 A1 sans nomination) : aucun ne mordait, parce que les dents d'alors ne défendaient que les fonctions.
      Une dent portée par la boucle extérieure mord dès le Z0 de la nuit qui suit la retouche, sans rejeu de la série.
    ⑨ CE QUI CLOCHE — ① Le maillon 3 (`sys.exit(code_des_cas(resultats, sans_verdict))` du mode « --cas ») n'est
      exercé par aucun chemin réel : le témoin est écarté par `code_des_cas`, et un vrai signal sans verdict coûterait
      un lancement de plus ; il tient en une ligne, et le sabotage X2 du relecteur reste « NE MORD PAS » (déclaré).
      ② Une ligne rouge de A1 qui nomme un module SANS que ce soit le signal refusé (un texte qui citerait un autre
      module) passerait : le contrôle porte sur la présence d'un nom, pas sur son exactitude. ③ Le témoin prouve le
      chemin d'un plantage en code 1 ; un délai dépassé (code 124) n'est éprouvé que par l'exemple écrit de A6.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    manques = ["la ligne « PAS DE VERDICT » du témoin %s manque" % t for t in TEMOINS_SANS_VERDICT
               if ("PAS DE VERDICT : signal %s · " % t) not in sortie]
    for l in sortie.splitlines():
        if l.strip().startswith("ÉCHEC A1 "):
            for morceau in re.split(r"(?<= oui) · |(?<= NON) · ", l.strip().partition(" — ")[2]):
                if morceau.endswith(" NON") and not re.search(r"programmes/\S+\.py", morceau):
                    manques.append("un élément rouge de A1 ne nomme aucun module : %s" % morceau[:200])
    return manques


if __name__ == "__main__":
    if len(sys.argv) == 6 and sys.argv[1] == "--signal":
        _code, _ligne = eprouver_un_signal(os.path.abspath(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
        print(_ligne)
        sys.exit(_code)
    if len(sys.argv) > 2 and sys.argv[1] == "--cas":
        resultats, sans_verdict = cas(os.path.abspath(sys.argv[2]))
        for nom, ok, detail in resultats:
            print(("  ok    " if ok else "  ÉCHEC ") + nom + " — " + detail)
        # T3-3 : un signal sans verdict, c'est un contrôle qui n'a pas pu tourner (R-734) — code 2, ni vert ni mordu
        for module, reglages, code_s, ligne_s in sans_verdict:
            print("  PAS DE VERDICT : signal %s · réglages %s · code %d · %s" % (module, reglages, code_s, ligne_s))
        # LE MARQUEUR DE FIN : sans lui, une épreuve interrompue ne passe ni pour verte ni pour mordue
        print("FIN DES CAS : %d" % len(resultats))
        sys.exit(code_des_cas(resultats, sans_verdict))
    _args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not _args:
        print(__doc__.split("① RÔLE")[0])
        sys.exit(2)
    DEPOT = os.path.abspath(_args[0])
    # --saboter=<noms> : Z0 puis ces sabotages (le joueur de séries, par lots ; décision n°71) ; la lecture reprend
    # celle des épreuves qui le font déjà (épreuve du cours propre de Yahoo ; BACKLOG A-599 ⑬ b : un lecteur commun
    # manque)
    _demandes = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
    if "--saboter" in sys.argv:
        _choix = ["Z0"] + list(SABOTAGES)
    elif _demandes:
        _inconnus = [n for n in _demandes[0] if n not in SABOTAGES and n != "Z0"]
        if _inconnus:
            print("%s N'EXISTE PAS dans SABOTAGES" % ", ".join(_inconnus))
            sys.exit(2)
        _choix = ["Z0"] + [n for n in _demandes[0] if n != "Z0"]
    else:
        _choix = [_args[1]] if len(_args) > 1 else ["Z0"]
        if _choix[0] != "Z0" and _choix[0] not in SABOTAGES:
            print("%s N'EXISTE PAS dans SABOTAGES" % _choix[0])
            sys.exit(2)
    _faute = False
    for sab in _choix:
        t0 = time.time()
        try:
            d, r = preparer(DEPOT, sab)
        except AssertionError as e:
            print("%s NE S'APPLIQUE PLUS : CIBLE INTROUVABLE — %s" % (sab, e))
            sys.exit(2)
        try:
            code, out = lancer(r, os.path.join(r, SOI), "--cas", r, delai=3600)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
        # LES LIGNES DE VERDICT au format de programmes/SERIES_DE_SABOTAGES.py (`LIGNE`) : le nom en tête, la durée à
        # part (décision n°71 : la série est jouée par le joueur de séries, qui relève ces lignes mot pour mot)
        # CE QUE LE PROCESSUS NON SABOTÉ EXIGE DE CHAQUE LANCEMENT (tour de n°83) : la ligne de chaque témoin « sans
        # verdict », un module dans chaque élément rouge de A1 ; sinon Z0 est rouge, et un sabotage ne mord pas « pour
        # sa raison » (la ligne garde le début « NE MORD PAS », que lisent le joueur de séries et le certificateur)
        manques = ce_que_le_lancement_n_a_pas_porte(out)
        if sab == "Z0":
            bon = code == 0 and not echecs and "FIN DES CAS : %d" % NOMBRE_DE_CAS in out and not manques
            print("Z0 dépôt tel quel : %s" % ("tout vert" if bon else "ROUGE (code %d)%s" % (
                code, (" — " + " · ".join(manques)) if manques else "")))
            print("   durée : %d s" % (time.time() - t0))
            print("\n".join(l for l in out.splitlines() if l.strip()))
        else:
            bon = code == 1 and bool(echecs) and "FIN DES CAS : %d" % NOMBRE_DE_CAS in out and not manques
            print(("%s mord : %r" % (sab, echecs)) if bon else
                  ("%s NE MORD PAS : POUR SA RAISON — %s · cas rougis : %r" % (sab, " · ".join(manques), echecs))
                  if manques else "%s NE MORD PAS : code %d · %s" % (sab, code, out.strip()[-600:]))
            print("   durée : %d s" % (time.time() - t0))
            # CE QUI A ROUGI, en clair : pour chaque cas en échec, chacun de ses éléments rouges (« … NON »), EN ENTIER,
            # pour voir QUEL tricheur a passé ou QUEL contrôle a rougi. Avant le 01-11-2026, la ligne du cas était coupée
            # à 900 caractères : dès le septième tricheur, l'élément rouge de Sg (X5, X6) et celui de Sh (le contrôle du
            # seuil, dernier de A3) tombaient au-delà, et la sortie ne disait plus ce qui avait mordu.
            for l in out.splitlines():
                if l.strip().startswith("ÉCHEC"):
                    nom_du_cas, _, detail = l.strip()[len("ÉCHEC "):].partition(" — ")
                    print("     ÉCHEC " + nom_du_cas)
                    for morceau in re.split(r"(?<= oui) · |(?<= NON) · ", detail):
                        if morceau.endswith(" NON"):
                            print("        rouge : " + morceau)
        sys.stdout.flush()
        _faute = _faute or not bon
    print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
    sys.exit(1 if _faute else 0)
