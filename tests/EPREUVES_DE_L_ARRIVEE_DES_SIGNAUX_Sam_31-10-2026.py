#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX — Sam 31-10-2026 21h40 (Paris)
EN ESSAI · Rôle : éprouver, CHAQUE SOIR, sur le fichier maître et sur l'historique des 20 ans, à chacune des dates que
`dates_eprouvees` retient, que chaque programme de signal du dépôt ne se sert pas des séances qui suivent le jour qu'il
signale. Et que l'épreuve a des dents. SIMULATION UNIQUEMENT.
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
  LE TEST : il se joue sur CHAQUE FICHIER DE RÉFÉRENCE (`fichiers_de_reference`) : le fichier maître des cours, que
  le juge et le détecteur du soir jouent, PUIS l'historique des 20 ans, sur lequel C5 a été jugé. Pour chaque valeur
  d'un fichier, la RÉFÉRENCE est sa série entière, lue par le lecteur du juge, depuis sa première séance. Pour chaque
  jour J que `dates_eprouvees` retient dans cette série — les FENETRE derniers, PLUS FENETRE jours répartis par un pas
  fixe depuis l'origine —, le programme reçoit les cours JUSQU'À J seulement (depuis l'origine sur le maître ; ses
  séances de mémoire déclarée ailleurs, voir « LA MÉMOIRE DÉCLARÉE ») ; il doit dire pour J la même chose que quand il
  reçoit la série entière. Sinon il se sert de l'avenir : REFUSÉ, avec le fichier, la valeur, la date et le
  sens de l'écart. Un signal PASSE seulement s'il passe sur chaque fichier.
  LES 20 ANS (lot N72, 05-11-2026) : décision n°72 de Jean-Luc du 01-11-2026 à 12h05, réponse « 1 » à la question
  « Tester chaque stratégie une fois sur les 20 ans, à son arrivée (☑ recommandé). C'est le plus sûr, et cela couvre
  le futur test de C5. » ; elle complète A-674 (31-10-2026 à 21h15 : une fois par programme, à son arrivée, sur une
  période de 400 séances, hors du juge) ; « une fois, à son arrivée » est remplacé le 06-11-2026 à 19h41 par « chaque
  soir, pour toutes les stratégies » (voir « LA MÉMOIRE DÉCLARÉE »). QUELLES DATES : décision n°213 de Jean-Luc du 05-11-2026 à 23h57, réponse
  « 2 » à la question « Sur les 20 ans, quels jours vérifier qu'une stratégie ne voit pas l'avenir ? », option 2 :
  « Ces 400 jours, plus 400 jours répartis sur les 20 ans (☑ recommandé) : environ 85 min pour C5. Chaque époque est
  vérifiée. Une erreur rare, un jour non tiré, n'est toujours pas vue. » Pourquoi : les 400 derniers jours sont tous
  en 2025-2026 ; seuls des jours répartis vérifient que le jugement de C5 sur 2000-2023 ne repose pas sur un
  programme qui lit le lendemain. ON ÉTEND, ON NE REMPLACE PAS : le maître reste éprouvé, parce que c'est la série que
  le détecteur du soir donne au signal (un programme qui ne triche que sur une série courte, tricheur X8, serait
  invisible avec les 20 ans seuls).
  LA MÉMOIRE DÉCLARÉE (lot N72, tour t6, 06-11-2026). Le défaut, mesuré (étude « 54 heures », hors dépôt) : pour
  vérifier UNE date J, l'épreuve donnait au signal toute la série depuis son origine, et le signal recalculait tout ;
  sur les 20 ans, une coupe faisait en moyenne 4 471 séances quand C5 n'en lit que 16, et C5 coûtait environ 1 h 45 par
  lancement, la série de sabotages environ 54 h. Jean-Luc, 06-11-2026 à 18h22 : « Il est impossible qu'un petit
  contrôle comme ça […] prenne 54 heures. C'est un défaut de conception. » DÉCISIONS DE JEAN-LUC DU 06-11-2026 À 19h41,
  deux réponses « 1 » : ① « chaque stratégie dira de combien de jours passés elle a besoin, et un programme vérifiera ce
  chiffre ; le fichier du soir resterait vérifié depuis son début, comme en vrai » (la variante A de l'étude) ; ② les
  20 ans sont vérifiés CHAQUE SOIR pour TOUTES les stratégies, et le visa par empreinte et le contrôle du samedi,
  construits l'après-midi même, sont RETIRÉS (ils contournaient le défaut au lieu de le réparer ; ce qu'ils étaient et
  pourquoi ils sont tombés : etudes/RETRAIT_DU_VISA_DE_L_ARRIVEE_DES_SIGNAUX_Ven_06-11-2026.md). COMMENT :
  ⓐ LA MÉMOIRE d'une fonction de signal est le nombre de séances, jour J compris, dont elle a besoin pour décider le
  jour J : sa décision au rang i ne dépend que des séances i − mémoire + 1 à i. Le MODULE la déclare par une fonction
  nommée `memoire_` suivi du nom de la fonction de signal, qui reçoit les mêmes réglages et rend un entier (lue par
  `memoire_declaree`). Exemple : `memoire_signaux_c5etendu10()` rend 16 ; `memoire_signaux_rsi2(periode, seuil,
  tendance)` rend la tendance quand elle domine. Elle vit dans le module, jamais dans la fiche : une fiche pourrait
  dire 16 pour un module qui en a besoin de 200 (superviseur R-759 du 06-11-2026). ⓑ SUR LE FICHIER MAÎTRE, chaque
  date est coupée DEPUIS L'ORIGINE, comme avant : c'est la série que le détecteur du soir donne au signal ; un
  programme qui déciderait autrement quand sa série commence le 2 janvier 2024 y est donc vu (tricheur X11). ⓒ SUR
  LES AUTRES FICHIERS (les 20 ans), la coupe de la date J ne garde que les `mémoire` dernières séances jusqu'à J.
  Aucune n'est postérieure à J : la lecture de l'avenir est vue exactement comme avant. Un module qui NE DÉCLARE PAS
  de mémoire y est coupé depuis l'origine, comme avant (tricheur X12) : ne pas déclarer ne laisse rien passer, cela
  coûte seulement plus cher. ⓓ LA VÉRIFICATION DE LA MÉMOIRE (`verifier_la_memoire`, après les coupes de chaque
  valeur) : la série privée de ses k premières séances doit rendre, rang pour rang, les décisions de la série
  entière, à partir du rang k + mémoire − 1 ; sinon REFUSÉ « MÉMOIRE DÉCLARÉE TROP COURTE ». ⓔ LE DIAGNOSTIC
  (`decision_depuis_l_origine`) : quand une coupe à la mémoire décide autrement que la série entière, la même date est
  rejouée DEPUIS L'ORIGINE avec un module rechargé ; si elle y décide comme la série entière, le signal ne lit pas
  l'avenir, sa mémoire est trop courte : le refus le DIT (« MÉMOIRE DÉCLARÉE TROP COURTE »), au lieu d'accuser un
  signal honnête de lire l'avenir (le superviseur R-759 du 06-11-2026 l'a montré avec un RSI(14) honnête à mémoire
  sans fin). CE QUE LA MÉMOIRE PERD, NOMMÉ : sur les 20 ans, un programme qui ne lit pas l'avenir mais décide autrement
  selon le DÉBUT ou la LONGUEUR de la série qu'il reçoit, ET qui déclare une mémoire, n'y est plus vu (la forme
  « Y_20 » de l'étude) ; aucun usage réel ne donne au signal une série qui commence en 2000. Un signal à mémoire
  réellement sans fin (lissage exponentiel, RSI de Wilder) déclare une mémoire PRATIQUE, au-delà de laquelle l'écart
  avec le calcul depuis l'origine est sous la précision des nombres : l'écart n'est pas nul, la vérification ⓓ dit
  s'il change une décision.
  L'UNIVERS À CHAQUE DATE, SANS SAUT SILENCIEUX : toutes les valeurs d'un fichier sont éprouvées à toutes les dates
  retenues, dans l'indice ou non (ce qu'on éprouve — le programme ne lit pas l'avenir — ne dépend pas de l'indice) ; la
  ligne PASSE compte les dates éprouvées hors de l'indice. Une valeur que le lecteur unique connaît dans le CAC 40
  pendant la période d'un fichier, mais SANS AUCUN cours dans ce fichier, est NOMMÉE sur une ligne « DANS L'INDICE,
  SANS COURS DANS <fichier> : … » (mesuré le 05-11-2026 : ARCELORMITTAL dans l'historique des 20 ans) ; cette ligne ne
  rend pas l'épreuve rouge : la complétude du fichier relève du contrôle de la décision n°48 (chaque séance manquante
  a sa cause).
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

LES CAS (A1 à A8, A10 à A12), DANS UNE COPIE DU DÉPÔT où l'épreuve dépose ses propres modules (préfixe `EPREUVE_ARRIVEE_`) et
une fiche d'épreuve :
  A1 chaque signal du DÉPÔT passe (le vrai registre, dont la vraie ligne C5E10-QA-V1, R-732 ; les vrais modules RSI(2)
     et hasard par leur déclaration), et aucun module déclaré du dépôt n'est inéprouvable ; un signal qui ne passe
     pas y est NOMMÉ (`nommer_ce_qui_ne_passe_pas`). Dans un lancement de SABOTAGE (tour t6), les signaux du dépôt
     ne sont pas lancés : A1 n'y juge que les modules déclarés inéprouvables, et le dit ;
  A2 le module d'épreuve honnête (décalage 0) passe ;
  A3 chaque tricheur est éprouvé ET refusé : `filtre_lendemain` (C5 confirmé par la séance suivante, une fuite qui
     RETIRE des achats), `frequent_plus_fuite_rare` (un signal fréquent plus un achat les veilles d'une hausse de 6 %),
     `normalisation_globale` (un seuil tiré de toute la série), `memoire` (retient la plus longue série vue),
     `connait_l_echantillon` (ne triche pas aux dates qu'un échantillon à graine écrite tirerait), et les deux
     tricheurs du relecteur du tour 2 dont le comportement dépend de la LONGUEUR de la série : X5 « historique
     minimal » et X6 « normalisation si longue ». Leur seuil (`SEUIL_DES_TRICHEURS_LONGS`, FENETRE + 100) doit être
     plus grand que FENETRE et atteint par au moins une valeur du maître, sinon ils n'ont plus de dents : A3 rougit
     (R-734). A3 exige aussi que chaque tricheur refusé soit NOMMÉ par `nommer_ce_qui_ne_passe_pas` (son module, ses
     réglages et le début de son verdict) : la dent de T3-5 tient aux tricheurs que l'épreuve dépose elle-même.
     LES QUATRE TRICHEURS DES 20 ANS (lot N72), dont les seuils sont CALCULÉS sur les données de la copie
     (`tricheurs_des_donnees`), jamais écrits en chiffres : X7 « historique minimal long » (rien sous la plus longue
     série du maître plus une séance, puis il lit le lendemain : il ne triche que sur les 20 ans) · X8 « historique
     court » (il lit le lendemain seulement sur une série qui commence à la première date du maître ou après : il ne
     triche que sur le maître) · X9 « hors de l'indice » (il lit le lendemain seulement aux dates où la valeur est hors
     de l'indice) · X10 « fuite avant le maître » (il lit le lendemain seulement avant la première date du maître :
     seuls les jours répartis le voient ; il DÉCLARE une mémoire, et prouve que la coupe à la mémoire voit l'avenir et
     que le diagnostic ne l'excuse pas). LES DEUX PROGRAMMES DE LA MÉMOIRE (tour t6), qui ne lisent pas l'avenir mais
     décident autrement selon la série reçue, refusés à raison (voir ⑧, « une garde d'historique ») : X11 « origine du
     maître » (il déclare une mémoire, et retire l'achat du dernier jour d'une série qui commence à la première date du
     maître : seule la coupe DEPUIS L'ORIGINE du maître le voit) · X12 « longue série sans mémoire » (il ne déclare
     PAS de mémoire, et retire l'achat du dernier jour d'une série longue qui finit avant le maître : seule la coupe
     depuis l'origine des 20 ans le voit) · X14 « mémoire courte hors des dates » (tour t7 ; attendu
     ATTENDU_DU_DECALAGE, jugé par A12 : seule la vérification par décalage peut le refuser) · X13 « mémoire avant le maître » (le tricheur `memoire`, qui retient la série
     entière qu'il a vue, limité aux dates d'avant le maître, avec une mémoire déclarée : le diagnostic doit RECHARGER
     le module avant de rejouer la date, sinon il l'excuserait). A3 contrôle leurs préconditions et rougit si l'une
     tombe (R-734) ;
  A4 les réglages d'une FICHE sont éprouvés : la fiche d'épreuve passe au module honnête un décalage de −1, qui lui
     fait lire la séance suivante ; elle est refusée ;
  A5 un module d'épreuve déclaré, sans exemple et sans fiche, est dit inéprouvable ;
  A6 un lancement sans verdict n'est pas un verdict (ajouté le 05-11-2026, superviseur R-759 de la nuit, défaut 1 :
     « un sabotage ne peut viser qu'une règle qu'un cas peut appeler ») : sur des EXEMPLES ÉCRITS, un délai dépassé et
     une trace Python ne rendent aucun verdict pour `verdict_du_lancement` ; `code_des_cas` rend 2 dès qu'un lancement
     inattendu est sans verdict, et 0 pour le seul témoin. Le sabotage T3_3a fait rougir A6, T3_5 fait rougir A3 ;
  A7 une valeur de l'indice sans cours est nommée (lot N72) : la ligne « DANS L'INDICE, SANS COURS DANS <fichier> »
     que le lancement du module honnête a imprimée est, pour chaque fichier de référence, celle que
     `dans_l_indice_sans_cours` calcule ; et sur un EXEMPLE CONSTRUIT (le maître privé d'une de ses valeurs), la
     fonction nomme la valeur retirée. Le sabotage S_absente_tue fait rougir A7 ;
  A8 le fichier des 20 ans n'est pas écrit en dur : renommé dans le contrat EN MÉMOIRE, `fichiers_de_reference` le
     trouve sous son nom nouveau (lot N72, tour t2 ; sabotage S_chemin_en_dur) ;
  A9 (le visa par empreinte) est RETIRÉ au tour t6 avec le visa (décision de Jean-Luc du 06-11-2026 à 19h41) ; le
     numéro n'est pas réutilisé, pour qu'un texte ancien qui cite A9 ne désigne pas autre chose ;
  A10 les délais sortent de la mesure versée : `delais_d_une_mesure` sur une mesure construite, et le délai du
     lancement normal écrit au JSON égal à celui qu'elle calcule (sabotages S_delai_du_json_a_la_main, S_pas_moyen) ;
  A11 le lancement normal (tour t3) : une option inconnue (« --toutes-sur-vingt-ans », l'option du samedi retirée) et
     un argument en trop arrêtent en code 2, en les nommant, avant toute préparation ; les formes acceptées le restent ;
  A12 la mémoire déclarée (tour t6) : ① `verifier_la_memoire` sur une série construite, une mémoire juste passe et une
     mémoire trop courte d'une séance est refusée (sabotage S_decalage_un_rang_trop_loin) ; ② `memoire_declaree` lit
     la mémoire du module honnête selon ses réglages, rend None sans déclaration (S_memoire_par_defaut) et refuse une
     mémoire illisible ; ③ les deux modules à mémoire mal déclarée — trop courte, et réellement sans fin — sont refusés
     avec le diagnostic « MÉMOIRE DÉCLARÉE TROP COURTE », jamais « lit l'avenir » (S_sans_diagnostic) ; ④ le
     BRANCHEMENT : la ligne PASSE du module honnête dit, pour le maître, « coupes depuis l'origine », et pour chaque
     autre fichier, « coupes à la mémoire déclarée de N séances, vérifiée par décalage sur R rangs », R > 0
     (S_maitre_en_memoire, S_sans_verification_de_la_memoire) ; depuis le tour t7 : le décalage de secours sur une série
     courte (S_pas_de_decalage_de_secours), X14 refusé PAR LE DÉCALAGE, motif MOTIF_DU_DECALAGE
     (S_refus_du_decalage_ignore), et un fichier sans aucun rang comparé refusé MEMOIRE_NON_VERIFIEE
     (S_fichier_non_verifie_accepte).
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

USAGE : python3 -B tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py <racine>
        [--saboter | --saboter=S1,S2,… | nom]
  sans option : Z0, le dépôt tel quel : chaque signal, sur le maître et sur les 20 ans (chaque soir, décision de
  Jean-Luc du 06-11-2026 à 19h41) ;
  --saboter : Z0 puis chaque sabotage ; --saboter=<noms séparés par des
  virgules> : Z0 puis ceux-là (c'est ainsi que tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py joue la série par lots) ;
  un nom de sabotage : celui-là seul, sans Z0. TOUT AUTRE ARGUMENT (option inconnue, positionnel en trop, deux
  demandes de sabotage) arrête en code 2, en le nommant, avant toute préparation (`lire_les_arguments`, tour t3).
  UNE LIGNE PAR SABOTAGE, au format que lisent le joueur de séries et le certificateur
  (programmes/SERIES_DE_SABOTAGES.py, `LIGNE`) : « <nom> mord : [<cas rougis>] » ou « <nom> NE MORD PAS : … » ; la
  durée est sur la ligne suivante, à part, pour qu'un essai refait puisse rendre la ligne mot pour mot.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable, si un nom demandé n'existe pas, si un argument est inconnu ou en trop, ou si la mesure par
valeur ne se lit pas.
LA SÉRIE DE SABOTAGES N'EST PLUS JOUÉE LE SOIR (décision de Jean-Luc du 01-11-2026 à 11h41, n°71, réponse « 1 » à
« que fait-on de la série de sabotages de la version B (43 min chaque soir) ? », option 1 : « La sortir du soir, et ne
la rejouer que quand le code de l'essai change. C'est la pratique de la profession, recommandée par l'expert des
tests. ») : elle est déclarée dans tests/LANCEMENT_DES_EPREUVES.json (« series_hors_de_la_nuit ») ; elle se rejoue
à la main par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py, qui écrit son relevé
(tests/resultats/SERIE_DE_SABOTAGES_DE_L_ARRIVEE_DES_SIGNAUX_*.txt) avec l'empreinte de chaque fichier du dépôt dont
le code a été EXÉCUTÉ pendant la série (ce fichier, le juge, ses modules, les modules de signal) ; chaque nuit, la
certification vérifie que ce code n'a pas changé, et rougit sinon. QUEL CODE COMPTE est un CHOIX DU CHAT, PROVISOIRE,
À CONFIRMER PAR JEAN-LUC (D43, 05-11-2026 ; ce n'est pas une décision de Jean-Luc) : portée « code_execute », ce
fichier ET les programmes qu'il exécute, sans les données ; raison d'ORIGINE : changer un seul réglage du RSI(2)
du dépôt (« tendance » 200 → 0) faisait perdre la dent du sabotage Sf sans aucune alerte (relecteur du 05-11-2026).
CETTE RAISON EST CADUQUE depuis le tour t6 (relecteur r6, m1) : Sf mord par X12, et la série ne LANCE plus les
signaux du dépôt. Le fait qui reste (superviseur R-759 du 06-11-2026, m1) : la série EXÉCUTE encore le code de C5 —
le tricheur `filtre_lendemain` le charge par importlib —, et les dents qui passent par lui (Sc, et A3) dépendent de
C5 ; un changement du RSI(2) ou du hasard, en revanche, fait rejouer la série sans qu'aucune de ses dents en dépende.
La portée reste celle du choix D43, à confirmer par Jean-Luc avec ce fait. Si
Jean-Luc retient la lecture au mot de n°71 (ce fichier seul), un mot change dans la table (« epreuve »), sans
rejouer la série : le relevé porte déjà les deux. Le lancement normal (Z0) tourne, lui, chaque nuit.

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; par la vérification de version (`programmes/CERTIFIER_LA_VERSION.py`), qui lance
  chaque épreuve de tests/ depuis la racine avec la racine en argument (Z0), et qui, à la place de « --saboter »,
  vérifie le relevé de la série (décision n°71, voir plus haut) ; par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py,
  avec « --saboter=<noms> », à chaque changement de ce fichier. Ce programme se
  relance lui-même avec « --cas <copie> [--sans-les-signaux-du-depot] » (les cas, dans une copie ; l'option, pour un
  sabotage) et « --signal <racine> <module> <fonction> <réglages> » (UN signal, dans un processus neuf) : ces deux
  modes ne sont pas faits pour la main.
③ ENTRÉE — La racine du dépôt ; `--saboter`, `--saboter=<noms>` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : le juge, le contrat des fichiers (le nom et la lecture du registre, n°83 :
  une fiche par identifiant, sa dernière ligne), le registre des stratégies, le fichier maître des cours (trouvé
  par `fichiers_de_cours` du juge), EXACTEMENT UN fichier réparé que le contrat relie au contrat du maître (l'historique
  des 20 ans, trouvé par `fichiers_de_reference` ; zéro ou plusieurs : arrêt en code 2, avec les noms), le
  référentiel des valeurs, le module C5 (dont dépend le tricheur `filtre_lendemain`), EXACTEMENT UNE mesure par valeur
  (MESURE_PAR_VALEUR, d'où sortent les délais ; sinon code 2).
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par signal éprouvé, par cas et par sabotage. [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① copier la racine dans un dossier temporaire (sans .git, etudes,
  caches) · ② appliquer le sabotage à la copie de CE fichier, en exigeant que sa cible existe une fois · ③ relancer
  la copie de ce programme en mode « --cas » ; pour un SABOTAGE, avec « --sans-les-signaux-du-depot » : aucun signal
  du dépôt n'y est LANCÉ — la série éprouve les dents de l'épreuve, que portent ses propres modules d'épreuve, et Z0
  éprouve le dépôt (tour t6 : C5 seul pesait 94 % d'un lancement ; relevé du 05-11-2026 : seul Sf mordait par A1, par
  le RSI(2), et il mord désormais par X12). Mais le CODE de C5 y est encore exécuté, par le tricheur `filtre_lendemain`
  (tour t7, superviseur R-759, m1) · ④ Z0 doit être vert, un sabotage doit
  faire échouer au moins un cas ;
  dans les deux, CHAQUE SIGNAL, le témoin « sans verdict » excepté, DOIT AVOIR RENDU UN VERDICT (voir `cas`, T3-3) :
  sinon « --cas » rend 2, Z0 est rouge et le sabotage « NE MORD PAS » (`verdict_du_lancement`, `code_des_cas`) ; et
  la sortie doit porter ce qu'exige `ce_que_le_lancement_n_a_pas_porte` (la ligne du témoin, un module dans chaque
  élément rouge de A1), sinon Z0 est rouge et le sabotage « NE MORD PAS : POUR SA RAISON ».
⑦ UNITÉ — Des séances (la fenêtre), des dates AAAA-MM-JJ, des secondes.
⑧ POURQUOI — Voir « POURQUOI ICI ET PAS DANS LE JUGE » et « POURQUOI LA SÉRIE DU JUGE COMME RÉFÉRENCE ». Les coupes
  passent dans l'ORDRE CROISSANT et la série entière est appelée EN DERNIER, dans un état neuf (processus neuf par
  signal, module rechargé pour chaque valeur) : un module qui retiendrait une série plus longue n'a jamais rien vu
  de l'avenir quand il décide d'une coupe (superviseur R-759, mesure S2 : c'est ce qui fait refuser `memoire`). Sur
  le maître, et pour un module sans mémoire déclarée, la coupe part de l'ORIGINE de la série : le calcul du passé ne
  change pas d'une coupe à l'autre, et un signal à longue mémoire (RSI de Wilder, moyenne à 200 séances) reste
  accepté. Ailleurs, elle garde la mémoire déclarée (voir « LA MÉMOIRE DÉCLARÉE »). Seules les dates de
  `dates_eprouvees` sont coupées : le coût suit la somme des longueurs des coupes (`cout_des_coupes`), environ
  3 × 10⁻⁵ s par séance coupée pour C5 (étude « 54 heures », 06-11-2026, mesuré sur ACCOR) ; la durée MESURÉE de chaque
  valeur est versée au dépôt (MESURE_PAR_VALEUR) et les délais en sortent (`delais_d_une_mesure`, cas A10). Un jeu
  d'épreuves se sabote contre sa propre correction (R-731).
  UNE GARDE D'HISTORIQUE ÉCRITE SUR LA LONGUEUR DE LA SÉRIE EST REFUSÉE, ET À RAISON (tricheur N7 du relecteur du
  tour 3, 01-11-2026, retenu par le superviseur R-759 du tour 4) : un programme honnête par ailleurs qui commence par
  `if len(ohlcv) < 500: return []` est refusé le 2025-04-08, parce que cette garde lit la longueur de TOUTE la série,
  avenir compris ; un vrai soir du 2025-04-08, il n'aurait rien signalé. La garde juste s'écrit par date :
  `for i in range(500, len(ohlcv))`. Raison de cette ligne : sans elle, le premier refus de ce genre passera pour un
  faux refus.
⑨ CE QUI CLOCHE — CE QUI EST PROUVÉ : pour chaque signal éprouvé, chaque fichier de référence (le maître, puis les
  20 ans) et chaque valeur de ce fichier, à chacune des dates que `dates_eprouvees` retient (les FENETRE dernières,
  plus FENETRE réparties depuis l'origine ; sur une série de moins de deux FENETRE séances, toutes), la décision prise
  sur la série coupée à ce jour est celle que le signal, CHARGÉ PAR L'ÉPREUVE, tire de la série entière du fichier
  (précision du superviseur R-759 du tour 4 : un module qui se sait éprouvé peut tirer autre chose de la même série
  quand c'est le juge qui le charge, limite ⑥). CE QUI NE L'EST PAS, nommé (superviseurs R-759 du 31-10-2026, du
  01-11-2026 et du 05-11-2026) :
  ① UN MODULE QUI RELIT LUI-MÊME UN FICHIER (le maître des cours, par date) passe n'importe quel contrôle fondé sur
     son comportement ; seul un processus sans accès aux fichiers l'arrêterait, et il n'existe pas aujourd'hui. Y
     COMPRIS UN CACHE QUE LE MODULE ÉCRIT LUI-MÊME : rempli par le juge, il le fait passer (tricheur N3 du relecteur
     du tour 3 : refusé au premier lancement, il passe après un passage « comme le juge » ; c'est la forme
     PLAUSIBLE de cette limite) ;
  ② UNE FUITE À UN JOUR NON RETENU PAR `dates_eprouvees` n'est pas vue (décision n°213 : « Une erreur rare, un jour
     non tiré, n'est toujours pas vue »). Sur le maître, plus court que deux FENETRE, chaque jour est retenu depuis le
     lot N72 (le tricheur X2 du relecteur du tour 2, une fuite le 2024-06-03, y est donc vu désormais, non rejoué).
     Sur les 20 ans, environ 800 jours sur 6 844 pour la plus longue série : une fuite d'un seul jour entre deux jours
     répartis (pas d'environ 16 séances) passe. Le pas est fixe et se calcule : un module qui le connaît peut ne pas
     tricher aux jours retenus (limite ⑥) ;
  ③ UN MODULE AJOUTÉ PUIS JUGÉ AVANT LA PROCHAINE VÉRIFICATION DE VERSION n'a pas été éprouvé : le juge ne le refuse
     pas (BACKLOG) ;
  ④ DES RÉGLAGES ABSENTS DU REGISTRE ET DES DÉCLARATIONS ne sont pas éprouvés (au 31-10-2026, la moulinette ne fait
     varier aucun `reglages_signal`, relevé du superviseur ; le jour où elle le fera, ses versions ne seront pas
     couvertes) ;
  ⑤ L'HISTORIQUE DES 20 ANS EST ÉPROUVÉ depuis le lot N72 (décisions n°72 et n°213), sur les jours de
     `dates_eprouvees`. Ce qui reste : ⓐ ARCELORMITTAL n'a aucun cours dans ce fichier (39 valeurs contre 40 au
     maître) : il n'y est pas éprouvé, et il est NOMMÉ sur la ligne « DANS L'INDICE, SANS COURS » ; ⓑ UNIBAIL_RODAMCO
     n'y commence que le 2023-04-14 (887 séances, 4 077 trous mesurés par le superviseur R-759 du 05-11-2026) : le
     comblement de la décision n°37ter n'y est pas, et ce fichier attend le gel VINGT ; ⓒ LE TEMPS : depuis la
     mémoire déclarée (tour t6), le coût d'un lancement normal tient surtout au MAÎTRE coupé depuis l'origine (C5 :
     727 coupes par valeur) ; la durée prévue se lit dans la ligne « délais tirés de … » du lancement, calculée depuis
     la mesure versée (MESURE_PAR_VALEUR), et la durée de la série dans son relevé. Avant le tour t6 : environ 1 h 45
     par lancement normal, environ 54 h prévus pour la série ;
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
  (code 2), jamais un refus.
  ⑩ UN CODE ÉCRIT CONTRE L'ÉPREUVE N'EST PAS ARRÊTÉ (superviseur R-759 du tour t2, SUP2-3 ; consigné au tour t3, pas
  corrigé) : le code éprouvé tourne dans le processus qui le mesure et le juge. L'épreuve trouve les erreurs d'un code
  honnête ; elle ne résiste pas à un code écrit contre elle, qui peut forger son verdict — imprimer « PASSE · … » puis
  s'arrêter par `os._exit(0)`, ou remplacer `comparer` dans `__main__` (elle y est cherchée au moment de l'appel) (lus
  dans le code, non joués) — ou DÉCLARER UNE MÉMOIRE qui lui sert : sa fonction de mémoire est du code du module, et
  elle est appelée dans le processus qui juge. Le verdict se lit dans la sortie que le signal partage. Seul un
  processus de mesure séparé du code éprouvé le fermerait (la preuve par construction, BACKLOG).
  ⑪ LA MÉMOIRE DÉCLARÉE (tour t6) : ⓐ une mémoire déclarée trop LONGUE n'est pas vue (l'épreuve est seulement plus
     lente) ; ⓑ la vérification par décalage compare les rangs à partir du tiers de chaque série (`decalages`) : une
     erreur de mémoire dont l'effet ne tombe que plus tôt n'est vue qu'aux dates retenues, par le diagnostic ; ⓒ un
     programme qui décide selon le début ou la longueur de sa série ET déclare une mémoire n'est plus vu sur les 20 ans
     (voir « CE QUE LA MÉMOIRE PERD ») ; il l'est sur le maître (X11) ; ⓓ le diagnostic rejoue la date fautive depuis
     l'origine avec un module rechargé : un état gardé HORS des modules (limite ①) peut le tromper.
  · Avec la série sortie du soir (décision
  n°71) et la portée « code_execute » (choix D43 du Chat, à confirmer), ses dents sont revérifiées au changement du
  code EXÉCUTÉ par la série ; une dent qui tient aux DONNÉES (le seuil des tricheurs longs tient à la longueur du
  maître) n'est pas couverte par le relevé : seul le contrôle de sa précondition en Z0 la protège (R-734). Un module
  qui devient module de signal ne fait rejouer la série qu'après sa première exécution par une série ; Z0 l'éprouve
  dès la nuit suivante. Depuis le tour t6, la série ne LANCE plus les signaux du dépôt, mais elle exécute encore le
  code de C5 par le tricheur `filtre_lendemain`, et ses dents Sc et A3 en dépendent (tour t7, m1).
⑩ EFFET — Écrit dans des dossiers temporaires, effacés à la fin normale ; `-B` partout, aucun fichier compilé.
  N'écrit rien au dépôt (le visa, qui y écrivait, est retiré au tour t6).
  LIMITE : une coupure par le certificateur (délai dépassé) laisse la copie du sabotage en cours, environ
  300 Mo (296 Mo mesurés par le relecteur du tour 3), dans le dossier temporaire, car le certificateur ne tue que
  son enfant direct. Sur GitHub, chaque tranche tourne sur une machine jetée à la fin : cela n'y coûte rien ; sur la
  machine du Chat, ce dossier est à effacer à la main (BACKLOG, au nom du certificateur, T3-6).
⑪ TERMINAISON — Sort lui-même. Chaque sous-processus a un délai ; un délai dépassé compte comme un échec.
  [sort: oui]
"""
import ast
import csv
import glob
import io
import math
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import types

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
#   ④ la ligne PASSE de `eprouver_un_signal` (« N parmi les 400 dernières de chaque série, M réparties depuis
#      l'origine », comptes calculés, lot N72 tour t2) : elle dit alors les dernières de la série coupée à FENETRE ;
#   ⑤ les deux « pourquoi » de cette épreuve dans tests/LANCEMENT_DES_EPREUVES.json, celui du lancement normal
#      (« delais ») et celui de la série (« series_hors_de_la_nuit », depuis la décision n°71) : durées mesurées avec
#      la série entière, piste b.
#   (Lot N72, 05-11-2026 : la ligne `s = cours[v]` est désormais dans la boucle sur les fichiers de référence de
#   `eprouver_un_signal` ; le geste est le même, sur chaque fichier. Il faut aussi retirer X7 « historique minimal
#   long », dont le seuil dépasse alors toute coupe, et le contrôle de sa précondition dans `cas`.)
#   CE QUI ROUGIT après le seul geste `s = cours[v][-FENETRE:]` (sabotage Sg, tour t3, 06-11-2026, signaux du dépôt
#   rejoués depuis la mesure versée ; cas rougis : mesurés par programme ; tricheurs : relevés à l'œil) : A3 (X5, X6,
#   X7, mais AUSSI X9 « hors de l'indice » et X10 « fuite avant le maître » passent, la référence ne gardant que des
#   séances récentes) et A9, le visa, alors présent (retiré au tour t6). Ce que la liste ci-dessus ne disait pas :
#   retirer AUSSI X9 et X10 (et, depuis le tour t6, X12, qui ne se voit que sur une longue série ; non rejoué).
# RÉVERSIBILITÉ DES 20 ANS (lot N72 ; décisions n°72 du 01-11-2026 et n°213 du 05-11-2026). Chaque recette dit le
# geste, puis tout ce qu'il entraîne dans le même geste (R-723 : une règle nouvelle traite chaque règle qu'elle touche),
# puis CE QUI ROUGIT si l'on ne fait que le geste — au tour t3 (06-11-2026, lot_N72_t3, hors dépôt ; cas rougis :
# mesurés par programme ; tricheurs : relevés à l'œil sur la sortie), en jouant le sabotage qui EST ce geste avec
# les signaux du dépôt rejoués depuis la mesure versée :
#   ⓐ revenir au maître seul : ① `return [maitre] + longs` → `return [maitre]` dans `fichiers_de_reference` (c'est le
#      sabotage S_sans_extension) ; ② retirer X7, X8, X10 et X12 de `tricheurs_des_donnees` et leurs préconditions
#      (X7, X10 et X12 passeraient ; la précondition de X8 tombe, faute d'autre fichier — relevé à l'œil au tour t3) ;
#      ③ la mémoire déclarée n'a plus d'usage (le maître est coupé depuis l'origine) : retirer `memoire_declaree`,
#      `decalages`, `verifier_la_memoire`, `decision_depuis_l_origine`, les paramètres `memoire` et `neuf` de
#      `comparer`, le cas A12, les deux modules de la mémoire de MODULES_D_EPREUVE et les sabotages de la mémoire
#      (tour t6) — les fonctions `memoire_…` des modules de signal peuvent rester, elles ne sont lues par personne
#      d'autre ; ④ retirer le cas A8, et baisser NOMBRE_DE_CAS d'autant ; ⑤ retirer les sabotages qui visent ce qui
#      disparaît : S_sans_extension, S_remplacement, S_recentes_seules (il ne visait que X10), S_chemin_en_dur ;
#      ⑥ refaire la mesure par valeur (elle porte les 20 ans) et récrire le délai du JSON à la valeur que
#      `delais_de_la_mesure` en tire (A10) ; ⑦ récrire « LE TEST », « LA MÉMOIRE DÉCLARÉE », le ⑨ ⑤ et le ⑨ ⑪ de
#      l'en-tête, et le « pourquoi » du JSON.
#      CE QUI ROUGIT après ① seul (mesuré au tour t3, avant la mémoire ; cas rougis : mesurés par programme ; tricheurs :
#      relevés à l'œil) : A3 (X7 et X10 passent ; préconditions X7, X8, X10), A8 (le fichier des 20 ans n'est plus
#      trouvé), et A9, le visa, alors présent ; non rejoué au tour t6 ;
#   ⓑ revenir aux FENETRE derniers jours seuls (réponse « 1 » au lieu de « 2 » à la question n°213) : ① retirer
#      `reparties` du `return` de `dates_eprouvees` (sabotage S_recentes_seules) ; ② retirer X10 et sa précondition ;
#      ③ récrire le délai du lancement normal dans tests/LANCEMENT_DES_EPREUVES.json à la valeur que
#      `delais_de_la_mesure` rend APRÈS le geste : `cout_des_coupes` passe par `dates_eprouvees`, le délai calculé baisse
#      (superviseur R-759 du 06-11-2026, SUP2-2) et A10 rougit tant que le JSON garde l'ancien ; puis REFAIRE LA MESURE
#      par valeur, dont les secondes ont été prises avec les jours répartis, et récrire le délai une seconde fois ;
#      ④ récrire « LE TEST », le ⑨ ② de l'en-tête et la notice de `dates_eprouvees`.
#      CE QUI ROUGIT après ① seul (tour t3 ; cas rougis : mesurés par programme ; tricheurs : relevés à l'œil) : A3
#      (X10 passe, sa précondition tombe), A10 (au tour t3, le JSON disait 11 000 s, le calcul 10 800 s ; le pas ③ seul
#      le rendait vert, vérifié par programme ; non rejoué au tour t6).
FENETRE = 400
# Le seuil de longueur des tricheurs X5 et X6 : plus grand que FENETRE (sinon ils trichent aussi dans les coupes et ne
# prouvent plus rien sur la référence) et atteint par au moins une valeur du maître (contrôlé dans A3, R-734).
SEUIL_DES_TRICHEURS_LONGS = FENETRE + 100
PREFIXE = "EPREUVE_ARRIVEE_"
# LES DÉLAIS NE SONT PLUS ÉCRITS À LA MAIN (lot N72, tour t2, 06-11-2026 ; superviseur R-759 du 06-11-2026, R-N1,
# « ARRÊTER ET SIMPLIFIER » : au tour précédent, un chiffre recopié était faux de 100 s, relecteur neuf, défaut N1). La
# MESURE PAR VALEUR est versée au dépôt (MESURE_PAR_VALEUR : un seul fichier doit répondre) et les délais en sortent par
# `delais_d_une_mesure` ; le cas A10 vérifie la fonction sur une mesure construite, et que le délai du lancement normal
# écrit dans tests/LANCEMENT_DES_EPREUVES.json est celui qu'elle calcule. DEPUIS LE TOUR t7 (superviseur R-759 du
# 06-11-2026, bloquant), la mesure versée est prise SOUS LA MESURE DE COUVERTURE DE LA CERTIFICATION, qui joue chaque
# épreuve ainsi : elle sort d'UN lancement normal joué par les fonctions mêmes de programmes/CERTIFIER_LA_VERSION.py, dont
# `cas` recopie les lignes « VALEUR · » des signaux du dépôt et la durée de chaque lancement. Une mesure prise sans la
# couverture donnait 600 s par signal quand C5 en demande environ 2,2 fois plus sous la certification.
MESURE_PAR_VALEUR = "tests/resultats/MESURE_DE_L_ARRIVEE_DES_SIGNAUX_PAR_VALEUR_*.tsv"
# La marge : le délai vaut MARGE fois la durée prévue au pas le plus lent mesuré (la machine de GitHub n'est pas mesurée ;
# la même machine a varié de 1,56 fois en une nuit, relecteur neuf du 06-11-2026, point 8 de ce qu'il n'a pas cassé).
MARGE_DES_DELAIS = 1.5
# Le temps de la copie du dépôt, ajouté au délai du lancement normal (quelques secondes mesurées le 06-11-2026).
COPIE_DU_DEPOT = 100             # secondes
# Le nombre de cas qu'un lancement « --cas » complet annonce sur sa ligne « FIN DES CAS ». ÉCRIT À LA MAIN,
# alors qu'il devrait se calculer (R-728 : ce qui se calcule ne s'écrit pas à la main) : consigné au BACKLOG par le
# superviseur R-759 du 05-11-2026, défaut 1, point 5 ; passé de 5 à 6 avec le cas A6, de 6 à 7 avec le cas A7 (N72),
# de 7 à 10 avec A8, A9 et A10 (N72, tour t2), de 10 à 11 avec A11 (N72, tour t3) ; au tour t6, A9 (le visa) part et
# A12 (la mémoire) arrive : 11 cas, A1 à A8 et A10 à A12.
NOMBRE_DE_CAS = 11
# L'OPTION D'UN LANCEMENT « --cas » DE SABOTAGE (tour t6) : les signaux du dépôt n'y sont pas LANCÉS ; Z0 les joue.
# Leur code peut l'être encore par un module d'épreuve (C5, par le tricheur `filtre_lendemain`).
SANS_LE_DEPOT = "--sans-les-signaux-du-depot"
# LE MOT DU DIAGNOSTIC DE LA MÉMOIRE (tour t6), écrit une fois : le refus d'une mémoire trop courte le porte, et le
# cas A12 le cherche. Il ne contient pas « seulement », le mot des refus « lit l'avenir » (A3).
MEMOIRE_TROP_COURTE = "MÉMOIRE DÉCLARÉE TROP COURTE"
# LE MOT PROPRE À LA VÉRIFICATION PAR DÉCALAGE (tour t7), écrit une fois : son refus le porte, celui de la coupe jamais ;
# le cas A12 le cherche pour prouver que c'est bien le DÉCALAGE qui a refusé (relecteur r6, N1).
MOTIF_DU_DECALAGE = "privée de ses"
# LE MOT D'UN FICHIER COUPÉ À LA MÉMOIRE SUR LEQUEL AUCUN RANG N'A PU ÊTRE COMPARÉ (tour t7, m2 ; R-734 : un contrôle
# qui n'a pas pu tourner ne rend pas 0) ; le refus le porte, le cas A12 le cherche.
MEMOIRE_NON_VERIFIEE = "MÉMOIRE NON VÉRIFIÉE"
# L'ATTENDU d'un module d'épreuve que SEULE la vérification par décalage doit refuser (tour t7, X14).
ATTENDU_DU_DECALAGE = MEMOIRE_TROP_COURTE + " PAR DÉCALAGE"

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
        "    return out\n"
        # sa mémoire (tour t6) : la décision au rang i lit les rangs i − decalage − 1 et i − decalage
        "def memoire_signaux(decalage):\n"
        "    return max(2, decalage + 2)\n", "PASSE"),
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
        "            if not (x[\"i\"] + 1 < len(ohlcv) and ohlcv[x[\"i\"] + 1][\"close\"] < ohlcv[x[\"i\"]][\"close\"])]\n"
        # sa mémoire (tour t6) : celle de C5, lue chez C5 (R-708). Sans elle, quand un sabotage le laisse passer le
        # maître (Sc), il est coupé depuis l'origine sur les 20 ans, au prix de C5 depuis l'origine — environ une heure
        # et demie —, et son délai d'un signal (600 s) l'arrête sans verdict (mesuré le 06-11-2026, série du tour t6 :
        # « Sc_un_seul_sens NE MORD PAS : code 2 », « délai de 600 s dépassé »)
        "def memoire_signaux():\n"
        "    return _c5.memoire_signaux_c5etendu10()\n",
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
    # LES DEUX MODULES DE LA MÉMOIRE (tour t6, cas A12) : HONNÊTES — ils ne lisent jamais l'avenir — mais leur mémoire
    # déclarée est fausse. Sur le maître, coupé depuis l'origine, ils passent ; sur les 20 ans, coupés à leur mémoire,
    # ils doivent être refusés avec le diagnostic MEMOIRE_TROP_COURTE, jamais comme lisant l'avenir (superviseur R-759 du
    # 06-11-2026, condition ① : sans ce diagnostic, on dirait un jour à Jean-Luc qu'une stratégie honnête triche).
    # Trop courte : la décision au rang i lit le rang i − 2 (mémoire réelle 3), il en déclare 2.
    "EPREUVE_ARRIVEE_MEMOIRE_TROP_COURTE.py": (_DECLARE % (
        "honnête, achète quand la clôture dépasse de 1 % celle de l'avant-veille ; déclare 2 séances, il lui en faut 3",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    return [{\"i\": i} for i in range(2, len(ohlcv)) if ohlcv[i][\"close\"] > ohlcv[i - 2][\"close\"] * 1.01]\n"
        "def memoire_signaux():\n"
        "    return 2\n", MEMOIRE_TROP_COURTE),
    # Réellement sans fin : un plus haut depuis le début de la série reçue dépend de TOUTE l'histoire ; il déclare un an.
    "EPREUVE_ARRIVEE_MEMOIRE_SANS_FIN.py": (_DECLARE % (
        "honnête, achète quand la clôture dépasse le plus haut de toute la série reçue ; mémoire sans fin, déclare 250",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    out, haut = [], None\n"
        "    for i, b in enumerate(ohlcv):\n"
        "        if haut is not None and b[\"close\"] > haut:\n"
        "            out.append({\"i\": i})\n"
        "        haut = b[\"close\"] if haut is None else max(haut, b[\"close\"])\n"
        "    return out\n"
        "def memoire_signaux():\n"
        "    return 250\n", MEMOIRE_TROP_COURTE),
    # UNE MÉMOIRE QU'AUCUNE SÉRIE NE DÉPASSE (tour t7, m2) : honnête (il ne signale jamais), il déclare un milliard de
    # séances ; sur les 20 ans, chaque coupe part donc de l'origine et aucun rang ne peut être comparé par décalage : le
    # fichier doit être refusé MEMOIRE_NON_VERIFIEE (R-734), jamais passer en silence avec « 0 rangs » (relecteur r6, m2).
    "EPREUVE_ARRIVEE_MEMOIRE_PLUS_LONGUE_QUE_TOUT.py": (_DECLARE % (
        "honnête, ne signale jamais ; déclare une mémoire d'un milliard de séances, plus longue que toute série",
        "fonction_signal = signaux\nreglages_signal = {}\n") +
        "def signaux(ohlcv):\n"
        "    return []\n"
        "def memoire_signaux():\n"
        "    return 10 ** 9\n", MEMOIRE_NON_VERIFIEE),
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
    # qui évite exactement ces dates, passe alors à coup sûr ; la fuite rare sur signal fréquent passe ou non). Cible
    # déplacée par le lot N72 (R-723) : les dates se choisissent désormais dans `dates_eprouvees`, plus dans `comparer`
    "Sa_dix_dates_au_lieu_de_toutes": [(SOI, "    return sorted(set(reparties) | set(recentes))\n",
                                        "    import random\n"
                                        "    return sorted(random.Random(20261031).sample(range(max(0, len(s) - FENETRE), len(s)),\n"
                                        "                                                 min(10, len(s), FENETRE)))\n")],
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
    # Sf : la coupe en fenêtre glissante de 60 séances avant J, partout, au lieu de l'origine (le maître, un module sans
    # mémoire) ou de la mémoire déclarée. Jusqu'au tour t5, il mordait par le RSI(2) du dépôt, refusé à tort (A1) ; depuis
    # le tour t6, la série ne lance plus les signaux du dépôt, et il mord par X12 « longue série sans mémoire », qui
    # passe alors (A3)
    "Sf_fenetre_glissante": [(SOI, "        debut = 0 if memoire is None else max(0, j - memoire + 1)\n",
                              "        debut = max(0, j - 59)\n")],
    # Sg : la référence ramenée aux FENETRE dernières séances, comme au tour 2 (X5 et X6 doivent alors passer, et X7 des
    # 20 ans aussi depuis le lot N72 : la ligne visée est dans la boucle sur les fichiers de référence, une seule fois)
    "Sg_reference_reduite_a_la_fenetre": [(SOI, "            s = cours[v]\n", "            s = cours[v][-FENETRE:]\n")],
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
    # LES SABOTAGES DES 20 ANS (lot N72, superviseur R-759 du 05-11-2026, §4). Chacun vise une règle qu'un cas appelle :
    # S_sans_extension : le maître seul, comme avant N72 (X7 « historique minimal long » doit alors passer : A3 rougit)
    "S_sans_extension": [(SOI, "    return [maitre] + longs\n", "    return [maitre]\n")],
    # S_remplacement : les 20 ans seuls, le maître remplacé (X8 « historique court » doit alors passer : A3 rougit)
    "S_remplacement": [(SOI, "    return [maitre] + longs\n", "    return longs\n")],
    # S_recentes_seules : les FENETRE derniers jours seuls, sans les jours répartis — la réponse « 1 » à la question
    # n°213 (X10 « fuite avant le maître » doit alors passer : A3 rougit)
    "S_recentes_seules": [(SOI, "    return sorted(set(reparties) | set(recentes))\n", "    return recentes\n")],
    # S_hors_indice : `comparer` saute en silence les dates où la valeur est hors de l'indice (X9 doit alors passer)
    "S_hors_indice": [(SOI, "    dates = dates_eprouvees(s)\n",
                       "    dates = [j for j in dates_eprouvees(s) if dans(s[j][\"date\"])]\n")],
    # S_valeur_hors_indice_sautee : une valeur hors de l'indice à une date retenue est sautée en entier, en silence
    # (Eiffage et Euronext sur les deux fichiers ; X9 doit alors passer)
    # (cible à DOUZE espaces, celle de la boucle sur les valeurs : au premier jet, une cible à huit espaces se trouvait
    # DANS la ligne à douze, et le `continue` inséré tuait toute la boucle — mesuré le 06-11-2026 à 01h33, « 0 dates
    # coupées » ; même piège corrigé pour Sg)
    "S_valeur_hors_indice_sautee": [(SOI, "            dans = lambda jour, p=lecture[\"passages\"][v]: B.dans_l_indice(p, jour)\n",
                                     "            dans = lambda jour, p=lecture[\"passages\"][v]: B.dans_l_indice(p, jour)\n"
                                     "            if any(not dans(s[j][\"date\"]) for j in dates_eprouvees(s)):\n"
                                     "                continue\n")],
    # S_absente_tue : la ligne « DANS L'INDICE, SANS COURS » n'est plus imprimée (A7 doit rougir)
    "S_absente_tue": [(SOI, "        print(\"DANS L'INDICE, SANS COURS DANS %s : %s\" % (fichier, \", \".join(sans_cours) or \"aucune\"),\n"
                            "              flush=True)\n", "")],
    # LES SABOTAGES DU TOUR t2 (lot N72, 06-11-2026). La propriété « pas de chemin en dur », jouée une seule fois à la main
    # au tour précédent (le fichier renommé sur disque et au contrat : l'épreuve doit rester VERTE), a désormais sa dent
    # permanente, le cas A8 (superviseur R-759 du 06-11-2026, R-N4) ; le sabotage écrit le chemin en dur (A8 doit rougir)
    "S_chemin_en_dur": [(SOI, "    return [maitre] + longs\n",
                         "    return [maitre] + [\"donnees/sources_yahoo/historique_long_repare.csv\"]\n")],
    # S_delai_du_json_a_la_main : le délai du lancement normal récrit à la main dans le JSON — un chiffre « 1 » ajouté
    # devant lui, sans recopier sa valeur ici (A10 doit rougir)
    "S_delai_du_json_a_la_main": [("tests/LANCEMENT_DES_EPREUVES.json", "\"%s\": {\n   \"secondes\": " % SOI,
                                   "\"%s\": {\n   \"secondes\": 1" % SOI)],
    # S_pas_moyen : le pas moyen au lieu du pas le plus lent (la mesure construite rend d'autres délais : A10 doit rougir)
    "S_pas_moyen": [(SOI, "        pas = max(sec / cout_des_coupes(n, m) for n, m, sec in ls)\n",
                     "        pas = sum(sec / cout_des_coupes(n, m) for n, m, sec in ls) / len(ls)\n")],
    # LES SEPT SABOTAGES DU VISA (S_visa_jamais_lu, S_samedi_lit_les_visas, S_empreinte_du_seul_module,
    # S_chemin_dans_l_empreinte, S_donnees_hors_empreinte, S_soi_hors_empreinte, S_visa_sans_z0_vert) sont RETIRÉS au tour
    # t6 avec le visa qu'ils défendaient (décision de Jean-Luc du 06-11-2026 à 19h41) : voir
    # etudes/RETRAIT_DU_VISA_DE_L_ARRIVEE_DES_SIGNAUX_Ven_06-11-2026.md.
    # LES SABOTAGES DE LA MÉMOIRE DÉCLARÉE (tour t6). Chacun vise une règle qu'un cas appelle :
    # S_maitre_en_memoire : le maître coupé lui aussi à la mémoire (la variante B de l'étude, que Jean-Luc n'a pas
    # retenue) ; X11 « origine du maître » doit alors passer (A3), et la ligne PASSE du maître ne plus dire « depuis
    # l'origine » (A12)
    "S_maitre_en_memoire": [(SOI, "        memoire = None if fichier == maitre else declaree\n",
                             "        memoire = declaree\n")],
    # S_memoire_par_defaut : un module sans mémoire déclarée reçoit une mémoire d'une séance au lieu de l'origine ; X12
    # « longue série sans mémoire » doit alors passer (A3), et `memoire_declaree` ne plus rendre None (A12)
    "S_memoire_par_defaut": [(SOI, "        return None\n    m = f(**sig.reglages)\n",
                              "        return 1\n    m = f(**sig.reglages)\n")],
    # S_coupe_plus_courte_que_la_memoire : la coupe garde une séance de moins que la mémoire déclarée ; le module honnête
    # (mémoire 2) doit alors être refusé (A2), et sa ligne PASSE des 20 ans manquer (A12)
    "S_coupe_plus_courte_que_la_memoire": [(SOI, "        debut = 0 if memoire is None else max(0, j - memoire + 1)\n",
                                            "        debut = 0 if memoire is None else max(0, j - memoire + 2)\n")],
    # S_sans_diagnostic : la date fautive n'est plus rejouée depuis l'origine ; les deux modules honnêtes à mémoire fausse
    # doivent alors être dits « lit l'avenir » au lieu de MEMOIRE_TROP_COURTE (A12)
    "S_sans_diagnostic": [(SOI, "            if memoire is not None and decision_depuis_l_origine(neuf, s, j) == (j in entiere):\n",
                           "            if False:\n")],
    # S_diagnostic_toujours_memoire : tout écart à la mémoire est mis sur le compte de la mémoire ; X10, qui lit
    # l'avenir et déclare une mémoire, doit alors être excusé au lieu d'être refusé comme tricheur (A3)
    "S_diagnostic_toujours_memoire": [(SOI, "            if memoire is not None and decision_depuis_l_origine(neuf, s, j) == (j in entiere):\n",
                                       "            if memoire is not None:\n")],
    # S_diagnostic_sans_rechargement : le diagnostic rejoue la date avec le MÊME module, sans le recharger ; X13, qui a
    # retenu la série entière, doit alors être excusé au lieu d'être refusé comme tricheur (A3)
    "S_diagnostic_sans_rechargement": [(SOI, "            motif, coupees, signalees, hors = comparer(sig, s, dans, memoire, charger)\n",
                                        "            motif, coupees, signalees, hors = comparer(sig, s, dans, memoire, lambda: sig)\n")],
    # S_sans_verification_de_la_memoire : la vérification par décalage n'est plus appelée ; la ligne PASSE du module
    # honnête dit alors 0 rang vérifié (A12)
    "S_sans_verification_de_la_memoire": [(SOI, "                motif_m, rangs = verifier_la_memoire(charger(), s, memoire)\n",
                                           "                motif_m, rangs = None, 0\n")],
    # LES SABOTAGES DU TOUR t7 (relecteur r6, N1 et m2 ; superviseur R-759 du 06-11-2026) :
    # S_refus_du_decalage_ignore : la vérification par décalage tourne et compte ses rangs, mais son refus est jeté (le
    # sabotage même du relecteur r6, qui ne mordait pas au tour t6) ; X14 doit alors passer (A12)
    "S_refus_du_decalage_ignore": [(SOI, "                if motif_m:\n", "                if False and motif_m:\n")],
    # S_fichier_non_verifie_accepte : un fichier coupé à la mémoire sans aucun rang comparé passe ; le module « plus
    # longue que tout » doit alors passer (A12)
    "S_fichier_non_verifie_accepte": [(SOI, "        if memoire is not None and nv == 0:\n", "        if False:\n")],
    # S_pas_de_decalage_de_secours : sans le décalage de secours, une série courte n'a plus aucun rang comparé (A12)
    "S_pas_de_decalage_de_secours": [(SOI, "    if not ks and longueur - memoire >= 1:\n", "    if False:\n")],
    # S_decalage_un_rang_trop_loin : la vérification commence un rang trop tard ; une mémoire trop courte d'UNE séance
    # n'est plus vue sur la série construite (A12)
    "S_decalage_un_rang_trop_loin": [(SOI, "        zone = range(k + memoire - 1, len(s))\n",
                                      "        zone = range(k + memoire, len(s))\n")],
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


class ReferenceIntrouvable(Exception):
    """Les fichiers de référence ne se trouvent pas comme le contrat le dit : l'épreuve s'arrête en code 2 (R-734)."""


def nom_du_maitre(racine, B):
    """Rend le nom du fichier maître, relatif à la racine, par la recherche même du juge.

    ① RÔLE — L'UNIQUE endroit où l'épreuve dit quel fichier est le maître (R-708 : deux implémentations d'une même
      chose divergent toujours).
    ② CONTEXTE D'APPEL — `fichiers_de_reference` ; `le_maitre`.
    ③ ENTRÉE — `racine` : la racine d'une copie · `B` : le juge.
    ④ CONDITIONS D'ENTRÉE — `fichiers_de_cours` du juge rend au moins un fichier.
    ⑤ SORTIE — UNE valeur : le chemin relatif du maître. [rend: 1]
    ⑥ TRAITEMENT — `fichiers_de_cours(racine)[0]` du juge, rendu relatif à `racine`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge calcule sur ce fichier ; l'épreuve doit couper le même (superviseur R-759 du 06-11-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit l'existence des fichiers ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur du juge si le maître manque. [sort: non]
    """
    return os.path.relpath(B.fichiers_de_cours(racine)[0], racine)


def fichiers_de_reference(racine):
    """Rend les fichiers de cours sur lesquels chaque signal est éprouvé : le maître, puis l'historique des 20 ans.

    ① RÔLE — Dire, à un seul endroit de l'épreuve et PAR PROPRIÉTÉ, quels fichiers servent de référence (lot N72).
    ② CONTEXTE D'APPEL — `lire_les_references`, dans chaque processus « --signal » et dans « --cas ».
    ③ ENTRÉE — `racine` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le juge et le contrat des fichiers existent sous la racine.
    ⑤ SORTIE — UNE valeur : la liste des chemins RELATIFS à la racine, le maître en tête. Exemple réel (05-11-2026) :
      [« donnees/cours_maitre.csv », « donnees/sources_yahoo/historique_long_repare.csv »]. [rend: 1]
    ⑥ TRAITEMENT — ① le maître : `fichiers_de_cours(racine)[0]` du juge, la même recherche que le juge, rendue
      relative comme le fait son `main` · ② les 20 ans : chaque fichier de `FICHIERS_REPARES` du contrat dont le nom de
      base est relié, dans `CONTRATS_PAR_FICHIER`, au contrat du maître (`COURS_MAITRE`, le même objet) · ③ zéro ou
      plusieurs : lever `ReferenceIntrouvable` avec les noms.
    ⑦ UNITÉ — Des chemins.
    ⑧ POURQUOI — Aucun chemin en dur (superviseur R-759 du 05-11-2026, P1) : si l'on renomme le fichier des 20 ans, sur
      disque et au contrat, l'épreuve ne change pas d'avis. Le maître reste en tête : c'est la série que le détecteur
      du soir donne au signal (on étend, on ne remplace pas, P2).
    ⑨ CE QUI CLOCHE — Un fichier réparé relié au contrat du maître pour une autre raison qu'un historique serait pris
      pour les 20 ans ; un second ferait arrêter l'épreuve (voulu : c'est alors à Jean-Luc de dire lequel).
    ⑩ EFFET — Importe le juge et le contrat ; lit l'existence du maître.
    ⑪ TERMINAISON — Rend la main, ou lève `ReferenceIntrouvable` (ou l'erreur du juge si le maître manque). [sort: non]
    """
    B, C = juge(racine), contrat(racine)
    maitre = nom_du_maitre(racine, B)
    longs = sorted(f for f in C.FICHIERS_REPARES
                   if C.CONTRATS_PAR_FICHIER.get(os.path.basename(f)) is C.COURS_MAITRE)
    if len(longs) != 1:
        raise ReferenceIntrouvable("il faut exactement UN fichier réparé relié au contrat du maître, trouvés %d : %s"
                                   % (len(longs), ", ".join(longs) or "aucun"))
    return [maitre] + longs


def dates_eprouvees(s):
    """Rend les rangs des jours coupés dans une série : les FENETRE derniers, plus FENETRE répartis depuis l'origine.

    ① RÔLE — Porter, à UN seul endroit, la règle de la décision n°213 (« quels jours vérifier »).
    ② CONTEXTE D'APPEL — `comparer`, une fois par valeur et par fichier ; `tricheurs_des_donnees`, pour les
      préconditions ; le sabotage S_valeur_hors_indice_sautee.
    ③ ENTRÉE — `s` : la série entière d'une valeur, triée par date.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée, sans doublon, des rangs retenus. Avec L = len(s) et D = max(0, L − FENETRE) :
      les rangs D à L − 1, plus les rangs 0, p, 2p… sous D, de pas p = max(1, D // FENETRE). Exemples réels : le maître
      (L ≤ 727) → tous ses rangs ; SOCIETE_GENERALE aux 20 ans (L = 6 844) → D = 6 444, p = 16, 403 + 400 = 803 rangs.
      [rend: 1]
    ⑥ TRAITEMENT — Deux plages, puis leur union triée.
    ⑦ UNITÉ — Des rangs dans la série (séances).
    ⑧ POURQUOI — Décision n°213 de Jean-Luc (05-11-2026, 23h57, « 2 ») : « Ces 400 jours, plus 400 jours répartis sur
      les 20 ans. Chaque époque est vérifiée. » Pas fixe depuis l'origine (superviseur R-759 du 05-11-2026, §6). Le
      pas est arrondi vers le bas : il y a au moins FENETRE jours répartis, jusqu'au début de la fenêtre.
    ⑨ CE QUI CLOCHE — Le nombre de jours répartis va de FENETRE à 2 × FENETRE − 1 selon l'arrondi (une série de
      799 séances a les 399 premiers rangs, pas 1, plus 400 : toutes ses séances). Un jour entre deux jours répartis
      n'est pas vu (⑨ ② de l'en-tête).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    debut = max(0, len(s) - FENETRE)
    recentes = list(range(debut, len(s)))
    reparties = list(range(0, debut, max(1, debut // FENETRE)))
    return sorted(set(reparties) | set(recentes))


def dans_l_indice_sans_cours(passages, mnemo, cours, seances):
    """Rend les valeurs que le lecteur unique sait dans le CAC 40 pendant la période d'un fichier, sans cours dans ce fichier.

    ① RÔLE — Qu'une valeur ne disparaisse jamais en silence de l'épreuve (superviseur R-759 du 05-11-2026, P4).
    ② CONTEXTE D'APPEL — `lire_les_references`, une fois par fichier ; le cas A7, sur un exemple construit.
    ③ ENTRÉE — `passages` : {mnémonique : [(entrée, sortie ou None)]}, rendu par `lire_les_passages` du lecteur unique
      (dates du calendrier, ou textes AAAA-MM-JJ) · `mnemo` : la table du juge, du mnémonique à la clé · `cours` : les
      séries du fichier, par clé · `seances` : les séances du fichier, AAAA-MM-JJ, triées (la lecture du juge).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des clés (le mnémonique quand la table ne le connaît pas). Exemple réel
      (05-11-2026) : [« ARCELORMITTAL »] pour l'historique des 20 ans, [] pour le maître. [rend: 1]
    ⑥ TRAITEMENT — Pour chaque mnémonique : sa clé ; écartée si elle a des cours ; gardée si un de ses passages
      recoupe [première séance, dernière séance] du fichier.
    ⑦ UNITÉ — Des dates AAAA-MM-JJ.
    ⑧ POURQUOI — L'univers se lit par le lecteur unique, jamais par une liste (R-708). La ligne n'est pas rouge : la
      complétude d'un fichier relève du contrôle de la décision n°48.
    ⑨ CE QUI CLOCHE — Un mnémonique d'une société sortie que la table des identités ne garde pas n'est pas vu (le
      lecteur ne rend que les mnémoniques d'aujourd'hui).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if not seances:
        return []
    iso = lambda d: d.isoformat() if hasattr(d, "isoformat") else str(d)
    debut, fin = seances[0], seances[-1]
    noms = set()
    for m, periodes in passages.items():
        v = mnemo.get(m.upper(), m)
        if v not in cours and any(iso(a) <= fin and (b is None or iso(b) >= debut) for a, b in periodes):
            noms.add(v)
    return sorted(noms)


def decalages(longueur, memoire):
    """Rend les décalages k de la vérification de la mémoire : la série est rejouée privée de ses k premières séances.

    ① RÔLE — Dire, à UN seul endroit, où la vérification de la mémoire coupe le début de la série (R-708) : elle s'en
      sert, et le calcul du coût aussi.
    ② CONTEXTE D'APPEL — `verifier_la_memoire`, une fois par valeur ; `cout_des_coupes`, une fois par ligne de mesure.
    ③ ENTRÉE — `longueur` : le nombre de séances de la série entière · `memoire` : la mémoire déclarée, en séances.
    ④ CONDITIONS D'ENTRÉE — `longueur` ≥ 0 ; `memoire` ≥ 1.
    ⑤ SORTIE — UNE valeur : la liste croissante, sans doublon, des k parmi le tiers et les deux tiers de la longueur
      (arrondis vers le bas), gardés si k ≥ 1 et s'il reste au moins `memoire` séances après k ; si aucun ne convient,
      [longueur − memoire] quand ce nombre vaut au moins 1 ; [] sinon. Exemples : (6 844, 16) → [2 281, 4 562] ;
      (30, 16) → [10] ; (30, 25) → [5] ; (2, 1) → [1] ; (25, 25) → [] ; (1, 1) → []. [rend: 1]
    ⑥ TRAITEMENT — ① deux positions, filtrées · ② sinon, le décalage de secours, longueur − mémoire (tour t7) : il
      laisse une seule séance, la dernière, à comparer.
    ⑦ UNITÉ — Des rangs dans la série (séances).
    ⑧ POURQUOI — Deux débuts différents suffisent à trouver une mémoire trop courte d'une séance (chaque rang compris
      entre k + mémoire − 1 et la fin est comparé) ; chaque décalage coûte un appel sur ce qui reste de la série, et
      deux décalages coûtent au plus une série entière de plus. Le prototype de l'étude « 54 heures » en prenait huit.
      LE DÉCALAGE DE SECOURS (tour t7, relecteur r6, m2 ; superviseur R-759 du 06-11-2026, « une propriété ») : une
      mémoire de plus des deux tiers d'une série (le RSI(14), 615 séances, sur UNIBAIL, 887) ne laissait aucun décalage,
      et la ligne PASSE disait « 0 rangs » sans rougir. Si la série n'est PAS plus longue que la mémoire, chaque coupe à
      la mémoire part déjà de l'origine (`debut = max(0, j − m + 1) = 0`) : rien n'est à vérifier, et aucun risque.
    ⑨ CE QUI CLOCHE — Les rangs avant le premier décalage plus la mémoire ne sont comparés par aucun décalage : ils ne
      le sont qu'aux dates retenues, par la coupe à la mémoire (⑨ ⑪ ⓑ de l'en-tête). Le décalage de secours ne compare
      qu'un rang.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    ks = [k for k in sorted({longueur // 3, 2 * longueur // 3}) if k >= 1 and longueur - k >= memoire]
    if not ks and longueur - memoire >= 1:
        ks = [longueur - memoire]
    return ks


def cout_des_coupes(longueur, memoire=None):
    """Rend le nombre de séances que le signal reçoit, en tout, pour une valeur de `longueur` séances.

    ① RÔLE — Dire, à un seul endroit, ce que coûte une valeur : le coût de C5 suit le nombre de séances qu'il reçoit
      (superviseur R-759 du 06-11-2026, §0 1 : de 25,5 à 26,9 µs par séance coupée sur les 39 valeurs des 20 ans).
    ② CONTEXTE D'APPEL — `delais_d_une_mesure`, deux fois par ligne de mesure.
    ③ ENTRÉE — `longueur` : le nombre de séances de la série entière d'une valeur · `memoire` : la mémoire avec laquelle
      elle a été coupée, en séances, ou None (coupes depuis l'origine).
    ④ CONDITIONS D'ENTRÉE — `longueur` ≥ 0 ; `memoire` None ou ≥ 1.
    ⑤ SORTIE — UNE valeur : la somme, sur les rangs j de `dates_eprouvees`, de la longueur de la coupe (j + 1 depuis
      l'origine, min(j + 1, mémoire) avec une mémoire), plus la série entière (`longueur`), plus, avec une mémoire, ce que
      reçoit la vérification (`verifier_la_memoire` : une série entière et, pour chaque k de `decalages`, longueur − k).
      Exemples : (800, None) → 800 × 801 / 2 + 800 = 321 200 ; (6 844, 16) → 803 coupes, 12 833 séances (la coupe du rang 0 n'en a
      qu'une), plus 6 844, plus 6 844 + 4 563 + 2 282 = 33 366. [rend: 1]
    ⑥ TRAITEMENT — `dates_eprouvees` sur les rangs 0 à longueur − 1 (elle ne lit que la longueur), puis la somme.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Les dates retenues et les décalages viennent des règles mêmes de l'épreuve (R-708) : si la décision
      n°213 ou la mémoire change, le coût prévu change avec elles, et le délai du JSON avec lui (A10). La série entière
      est comptée depuis le tour t6 : avec une mémoire de 16, elle pèse plus que toutes les coupes d'une valeur.
    ⑨ CE QUI CLOCHE — Le coût fixe d'un appel (chargement du module, rechargé pour chaque valeur et avant chaque
      vérification) n'est pas compté : il pèse sur les séries courtes et les petites mémoires, d'où le pas le plus lent
      pris dans `delais_d_une_mesure`, par signal ET par fichier.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    rangs = dates_eprouvees(range(longueur))
    if memoire is None:
        return sum(j + 1 for j in rangs) + longueur
    return (sum(min(j + 1, memoire) for j in rangs) + longueur
            + longueur + sum(longueur - k for k in decalages(longueur, memoire)))


def delais_d_une_mesure(lignes):
    """Calcule les trois délais de l'épreuve depuis une mesure par valeur.

    ① RÔLE — Tirer les délais d'une mesure versée au dépôt, jamais d'une arithmétique recopiée à la main (R-728).
    ② CONTEXTE D'APPEL — `delais_de_la_mesure` (lancement normal, mode « --cas ») ; le cas A10, sur une mesure construite.
    ③ ENTRÉE — `lignes` : des dictionnaires portant « signal », « fichier », « seances » (la longueur de la série
      entière ; 0 pour une durée qui ne se rapporte à aucune série), « secondes » (la durée mesurée), en texte ou en
      nombre, et, facultatif, « memoire » (la mémoire des coupes, en séances ; absente, vide ou « - » : depuis
      l'origine).
    ④ CONDITIONS D'ENTRÉE — Au moins une ligne à « seances » non nul ; les nombres se lisent.
    ⑤ SORTIE — UNE valeur : {« prevus » : {signal : secondes prévues}, « fixe » : secondes, « un_signal », « cas »,
      « lancement_normal » : secondes entières}. Exemple (cas A10) : deux lignes d'un signal S sur un même fichier, à
      800 séances depuis l'origine, 3 204 s et 1 602 s, plus une ligne à 0 séance de 100 s → S prévu 6 408 s ;
      un_signal 9 700 ; cas 9 800 ; lancement normal 9 900. [rend: 1]
    ⑥ TRAITEMENT — ① une ligne à 0 séance s'ajoute telle quelle (« fixe ») · ② pour chaque signal ET chaque fichier,
      son PAS LE PLUS LENT : le plus grand rapport secondes / `cout_des_coupes(seances, memoire)` de ses lignes · ③ sa
      durée prévue : ce pas fois la somme des `cout_des_coupes` de ses lignes, c'est-à-dire chaque valeur au pas le plus
      lent ; celle d'un signal : la somme sur ses fichiers · ④ le délai d'un signal : MARGE_DES_DELAIS × le plus long
      signal prévu ; celui des cas : MARGE_DES_DELAIS × (la somme des signaux prévus + le fixe) ; chacun arrondi à la
      centaine de secondes supérieure · ⑤ le lancement normal : le délai des cas plus COPIE_DU_DEPOT.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Au tour t1, les délais étaient calculés à la main (facteur de vitesse 1,6 appliqué aux valeurs
      mesurées après un redémarrage) et l'addition était fausse de 100 s (relecteur neuf du 06-11-2026, N1). Le pas le
      plus lent remplace ce facteur : il couvre la machine la plus lente de la mesure sans qu'on ait à dire quelles
      valeurs ont tourné sur laquelle (superviseur R-759 du 06-11-2026 : le coût est proportionnel aux coupes). Un pas
      PAR FICHIER depuis le tour t6 : le maître est coupé depuis l'origine et les 20 ans à la mémoire, le coût fixe d'un
      appel n'y pèse pas autant ; un seul pas pour les deux ferait payer au maître le pas des 20 ans.
    ⑨ CE QUI CLOCHE — ① Le pas le plus lent vient des séries COURTES (le coût fixe d'un appel y pèse plus) : la durée
      prévue dépasse la mesure ; c'est le sens sûr. ② Un signal mesuré seulement sur une machine rapide est prévu à
      cette vitesse : seule la marge le couvre. ③ La machine de GitHub n'est pas mesurée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève (ValueError) si un nombre ne se lit pas ou si aucune ligne n'a de séances.
      [sort: non]
    """
    par, fixe = {}, 0.0
    for l in lignes:
        n, sec = int(l["seances"]), float(l["secondes"])
        m = str(l.get("memoire") or "-").strip()
        if n == 0:
            fixe += sec
        else:
            par.setdefault((l["signal"], l.get("fichier", "")), []).append((n, None if m == "-" else int(m), sec))
    if not par:
        raise ValueError("aucune ligne de mesure ne porte de séances")
    prevus = {}
    for (sig, _fichier), ls in par.items():
        pas = max(sec / cout_des_coupes(n, m) for n, m, sec in ls)
        prevus[sig] = prevus.get(sig, 0.0) + pas * sum(cout_des_coupes(n, m) for n, m, _ in ls)
    centaine = lambda x: int(math.ceil(round(x, 6) / 100.0)) * 100
    un = centaine(MARGE_DES_DELAIS * max(prevus.values()))
    des_cas = centaine(MARGE_DES_DELAIS * (sum(prevus.values()) + fixe))
    return {"prevus": prevus, "fixe": fixe, "un_signal": un, "cas": des_cas, "lancement_normal": des_cas + COPIE_DU_DEPOT}


def delais_de_la_mesure(racine):
    """Lit la mesure par valeur versée au dépôt et rend ses délais, avec le nom du fichier lu.

    ① RÔLE — Donner au lancement normal, au mode « --cas » et au cas A10 les délais de la MÊME mesure (R-708).
    ② CONTEXTE D'APPEL — Le programme principal (délai d'un lancement « --cas ») ; `cas` (délai d'un signal ; A10).
    ③ ENTRÉE — `racine` : la racine du dépôt ou d'une copie.
    ④ CONDITIONS D'ENTRÉE — Exactement un fichier répond à MESURE_PAR_VALEUR : un texte séparé par des tabulations, des
      lignes de commentaire commençant par « # », puis un en-tête portant au moins « signal », « seances » et
      « secondes ».
    ⑤ SORTIE — UNE valeur : le dictionnaire de `delais_d_une_mesure`, plus « mesure » : le chemin relatif lu. [rend: 1]
    ⑥ TRAITEMENT — ① chercher le fichier par son motif ; zéro ou plusieurs : `ReferenceIntrouvable` avec les noms ·
      ② lire les lignes · ③ `delais_d_une_mesure`.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Superviseur R-759 du 06-11-2026, R-N1 : « la mesure par valeur versée au dépôt (tests/resultats/), et
      un calcul dans l'épreuve elle-même (une fonction, pas un programme nouveau) ».
    ⑨ CE QUI CLOCHE — Une mesure qui vieillit (C5 plus lent demain, maître plus long) n'est pas refaite d'elle-même : le
      délai suit la mesure versée, et la longueur réelle des données n'y entre pas (le maître grandit d'une séance par
      jour ; ses lignes gardent leur longueur mesurée).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève (`ReferenceIntrouvable`, ValueError, KeyError). [sort: non]
    """
    trouves = sorted(glob.glob(os.path.join(racine, MESURE_PAR_VALEUR)))
    if len(trouves) != 1:
        raise ReferenceIntrouvable("il faut exactement UNE mesure par valeur (%s), trouvées %d : %s" % (
            MESURE_PAR_VALEUR, len(trouves), ", ".join(os.path.relpath(t, racine) for t in trouves) or "aucune"))
    with open(trouves[0], encoding="utf-8") as h:
        lignes = list(csv.DictReader((x for x in h if not x.startswith("#")), delimiter="\t"))
    rendu = delais_d_une_mesure(lignes)
    rendu["mesure"] = os.path.relpath(trouves[0], racine)
    return rendu


def lire_les_arguments(args):
    """Lit les arguments du lancement normal ; tout argument inconnu ou en trop est une erreur nommée.

    ① RÔLE — Qu'aucun argument ne soit ignoré en silence (relecteur du tour t2, R2-2 : `--toutes-sur-20-ans`, mal
      écrit, retombait sur le mode du soir et le samedi sautait les 20 ans en code 0).
    ② CONTEXTE D'APPEL — Le programme principal, AVANT toute préparation (lecture de la mesure, copie du dépôt) ; le
      cas A11, sur des formes acceptées.
    ③ ENTRÉE — `args` : `sys.argv[1:]`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la racine (ou None) ; le choix (« Z0 » seul, « Z0 » puis des sabotages, ou un sabotage
      seul) ; la liste des erreurs, vide si tout est reconnu. Exemples : [r, « --toutes-sur-vingt-ans »] → erreur
      « option inconnue : --toutes-sur-vingt-ans » (l'option du samedi, retirée au tour t6) ; [r, « Z0 », « truc »] →
      erreur « argument en trop : truc » ; [r, « --saboter=Sa_dix_dates_au_lieu_de_toutes »] → (r, [« Z0 »,
      « Sa_dix_dates_au_lieu_de_toutes »], []). [rend: 3]
    ⑥ TRAITEMENT — ① les options : « --saboter », « --saboter=<noms> » ; toute autre est nommée ; deux demandes de
      sabotage aussi · ② les positionnels : la racine, puis au plus un nom de sabotage, et aucun avec une option
      « --saboter » ; le reste est nommé · ③ le choix, chaque nom vérifié dans SABOTAGES.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un lancement qui ne fait pas ce qu'on a demandé ne doit pas rendre 0. Le contrôle vient avant
      la préparation : le cas A11 lance le programme principal avec une option inconnue, et dure moins d'une seconde.
      Gardé au tour t6, quand le mode du samedi est retiré : un lancement du samedi qui traînerait encore son option
      s'arrête en code 2 au lieu de faire autre chose que ce qu'on croit.
    ⑨ CE QUI CLOCHE — Les modes internes « --signal » et « --cas » sont lus à part, par leur nombre d'arguments ; un
      nombre faux les fait tomber ici, où « --signal » et « --cas » sont des options inconnues (code 2). La même lecture
      des arguments, qui ignore une option inconnue, se trouve dans d'autres épreuves du dépôt (49 fichiers ont le
      motif, superviseur R-759 du tour t2) : le lecteur commun manque (BACKLOG A-599 ⑬ b).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    options = [a for a in args if a.startswith("--")]
    positionnels = [a for a in args if not a.startswith("--")]
    erreurs = []
    inconnues = [o for o in options if o != "--saboter" and not o.startswith("--saboter=")]
    if inconnues:
        erreurs.append("option inconnue : %s" % ", ".join(inconnues))
    demandes = [o for o in options if o == "--saboter" or o.startswith("--saboter=")]
    if len(demandes) > 1:
        erreurs.append("plusieurs demandes de sabotage : %s" % ", ".join(demandes))
    en_trop = positionnels[1:] if demandes else positionnels[2:]
    if en_trop:
        erreurs.append("argument en trop : %s" % ", ".join(en_trop))
    racine = positionnels[0] if positionnels else None
    if "--saboter" in demandes:
        choix = ["Z0"] + list(SABOTAGES)
    elif demandes:
        noms = demandes[0].split("=", 1)[1].split(",")
        choix = ["Z0"] + [n for n in noms if n != "Z0"]
    else:
        choix = positionnels[1:2] or ["Z0"]
    inconnus = [n for n in choix if n != "Z0" and n not in SABOTAGES]
    if inconnus:
        erreurs.append("%s N'EXISTE PAS dans SABOTAGES" % ", ".join(inconnus))
    return racine, choix, erreurs


def lire_les_references(racine):
    """Lit chaque fichier de référence par le lecteur du juge, et rend ses séries, sa lecture et ses valeurs sans cours.

    ① RÔLE — Une seule lecture des références pour les deux modes (« --signal » et « --cas ») : R-708.
    ② CONTEXTE D'APPEL — `eprouver_un_signal` (chaque processus « --signal ») ; `cas`, une fois par copie.
    ③ ENTRÉE — `racine` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — Celles de `fichiers_de_reference` ; le référentiel des valeurs existe.
    ⑤ SORTIE — DEUX valeurs : le module du juge ; la liste, dans l'ordre de `fichiers_de_reference`, des
      (fichier, séries par clé, lecture du juge, valeurs dans l'indice sans cours). [rend: 2]
    ⑥ TRAITEMENT — ① la table des mnémoniques du juge · ② les passages par `lire_les_passages` du lecteur unique ·
      ③ pour chaque fichier : `lire_par_le_lecteur` du juge, puis `dans_l_indice_sans_cours`.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Les séries que l'épreuve coupe sont celles que le juge lit (même lecteur, même conversion).
    ⑨ CE QUI CLOCHE — Les 20 ans se lisent en environ 3 s (mesuré le 05-11-2026) dans CHAQUE processus « --signal ».
    ⑩ EFFET — Lit des fichiers ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou lève (`ReferenceIntrouvable`, refus du lecteur). [sort: non]
    """
    B = juge(racine)
    mnemo = B.table_mnemoniques(B.trouver(racine, "REFERENTIEL_VALEURS"))
    lecteur = B.charger_module(os.path.join(racine, "programmes", "LIRE_LES_COURS.py"), "lecteur_unique")
    passages = lecteur.lire_les_passages(racine)
    lectures = []
    for f in fichiers_de_reference(racine):
        cours, lecture = B.lire_par_le_lecteur(racine, f, mnemo)
        lectures.append((f, cours, lecture, dans_l_indice_sans_cours(passages, mnemo, cours, lecture["seances"])))
    return B, lectures


def le_maitre(racine, B, lectures):
    """Retrouve le fichier maître, ses séries et sa lecture, par la recherche du juge et jamais par sa position.

    ① RÔLE — Donner à tous ceux qui ont besoin du maître UNE seule façon de le trouver (R-708 : deux implémentations
      d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `tricheurs_des_donnees` ; `cas`, pour le seuil des tricheurs longs X5 et X6 et pour
      l'exemple construit de A7.
    ③ ENTRÉE — `racine` : la racine d'une copie · `B` : le juge · `lectures` : la sortie de `lire_les_references`.
    ④ CONDITIONS D'ENTRÉE — `fichiers_de_cours` du juge rend au moins un fichier ; le référentiel des valeurs existe.
    ⑤ SORTIE — TROIS valeurs : le nom du maître relatif à `racine` ; ses séries par clé ; la lecture du juge. [rend: 3]
    ⑥ TRAITEMENT — ① le nom : `nom_du_maitre`, la même recherche que le juge · ② s'il est
      parmi les lectures, celle-là · ③ sinon, relu par `lire_par_le_lecteur` du juge.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Au premier jet du lot N72, trois endroits prenaient « le premier fichier des lectures » pour le
      maître ; sous le sabotage S_remplacement, ce premier fichier devient les 20 ans : X8 trichait sur les 20 ans
      au lieu de passer (mesuré le 06-11-2026 à 00h10), et l'exemple de A7 disait « le maître » en lisant les 20 ans
      (relecteur neuf du 06-11-2026, défaut N3). Le superviseur R-759 du 06-11-2026 a demandé UNE fonction.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Peut lire un fichier ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou lève (refus du lecteur). [sort: non]
    """
    nom = nom_du_maitre(racine, B)
    trouve = next((x for x in lectures if x[0] == nom), None)
    if trouve is not None:
        return nom, trouve[1], trouve[2]
    cours, lecture = B.lire_par_le_lecteur(racine, nom, B.table_mnemoniques(B.trouver(racine, "REFERENTIEL_VALEURS")))
    return nom, cours, lecture


def tricheurs_des_donnees(racine, B, lectures):
    """Fabrique les tricheurs des 20 ans et de la mémoire (X7 à X14), leurs seuils calculés sur les données, et leurs préconditions.

    ① RÔLE — Donner des dents à l'extension aux 20 ans et à la mémoire déclarée : chaque module ne se fait refuser que
      là où une seule des règles le voit (superviseur R-759 du 05-11-2026, §4 ; la décision n°213 pour X10 ; les
      décisions de Jean-Luc du 06-11-2026 à 19h41 pour X11 et X12).
    ② CONTEXTE D'APPEL — `cas`, une fois par copie, AVANT le dépôt des modules d'épreuve.
    ③ ENTRÉE — `racine` : la racine de la copie · `B` : le juge · `lectures` : la sortie de `lire_les_references`.
    ④ CONDITIONS D'ENTRÉE — Le maître (`fichiers_de_cours` du juge) a au moins une série.
    ⑤ SORTIE — DEUX valeurs : {nom de fichier : (texte du module, attendu)} pour les huit modules (« REFUSÉ », et
      ATTENDU_DU_DECALAGE pour X14) ;
      {texte de la précondition : vrai ou faux}, une par module. [rend: 2]
    ⑥ TRAITEMENT — ⓪ le maître : par `le_maitre` (la recherche du juge, cherché parmi les lectures, relu s'il n'y
      est pas), JAMAIS « le premier fichier des lectures » ; les AUTRES fichiers : les
      lectures qui ne sont pas le maître · ① SEUIL = plus longue série du maître + 1 ; PREMIERE et DERNIERE = première
      et dernière dates du maître · ② les séries hors
      de l'indice à au moins une date retenue, dans chaque fichier, par leur empreinte (première date, première
      clôture) → leurs passages · ③ écrire les sept textes, les valeurs y entrent par `repr` ; X10, X11 et X13
      déclarent une mémoire de 2 séances, X12 n'en déclare pas · ④ les préconditions : X7, aucune série du maître n'atteint SEUIL et
      la série ENTIÈRE d'un autre fichier l'atteint (tour t6 : avant la mémoire, c'était « une coupe éprouvée » ; avec
      la mémoire, la coupe d'un module qui en déclare une ne fait que quelques séances, et X7 est refusé parce que la
      série entière est longue) ; X8, chaque série des autres fichiers commence avant PREMIERE ; X9, au moins une date
      retenue hors de l'indice ; X10, au moins une date retenue d'un autre fichier avant PREMIERE ; X11, une série du
      maître qui commence à PREMIERE et finit à DERNIERE a une date retenue, de rang 40 ou plus, avant DERNIERE, où la
      hausse de 1 % a lieu ; X12, une série d'un autre fichier qui finit à PREMIERE ou après a une date retenue, de rang
      SEUIL − 1 ou plus, avant PREMIERE, où la hausse de 1 % a lieu ; X13, une date retenue d'un autre fichier avant
      PREMIERE, la veille d'une hausse de 1 % ; X14, ses rangs (k + 1, k de `decalages` à la mémoire 2, hors des dates
      retenues) existent, aucun n'est une date retenue d'une série, et l'un est en hausse sur deux séances.
    ⑦ UNITÉ — Des séances, des dates AAAA-MM-JJ.
    ⑧ POURQUOI — Un seuil écrit en chiffre perd ses dents quand les données changent (X5 a un seuil de 500 et il est
      attrapé sur le maître : il ne prouve rien sur l'extension). Une précondition tombée rougit A3 (R-734). Le
      maître est retrouvé INDÉPENDAMMENT de `fichiers_de_reference` (lot N72, reprise du 06-11-2026 à 01h30) : au
      premier jet, il était « le premier fichier des lectures » ; sous le sabotage S_remplacement, ce premier fichier
      devenait les 20 ans, PREMIERE devenait 2000-01-03, et X8 trichait sur les 20 ans au lieu de passer — le sabotage
      ne mordait que par la précondition, jamais par le tricheur (mesuré le 06-11-2026 à 00h10,
      « REFUSÉ · …historique_long_repare.csv · ACCOR le 2000-01-25 »). X11 et X12 (tour t6) ne lisent pas l'avenir :
      ils décident autrement selon le DÉBUT ou la LONGUEUR de la série reçue, la famille que la mémoire déclarée ne voit
      plus sur les 20 ans (étude « 54 heures », §5, ses modules Y_M et Y_20). X11 défend la coupe depuis l'origine du
      MAÎTRE (sabotage S_maitre_en_memoire), X12 celle d'un module SANS mémoire déclarée (S_memoire_par_defaut, Sf).
      X13 défend le RECHARGEMENT du module avant le diagnostic (S_diagnostic_sans_rechargement) : mandat inversé du
      tour t6, sortie capturée hors dépôt — le tricheur `memoire` muni d'une mémoire déclarée, diagnostiqué avec le
      même module, était excusé (« MÉMOIRE DÉCLARÉE TROP COURTE ») ; rechargé, il est refusé comme lisant l'avenir.
      X14 (tour t7) défend le REFUS de la vérification par décalage dans le vrai chemin (S_refus_du_decalage_ignore,
      relecteur r6, N1) : ses fautes de mémoire tombent aux seuls rangs que le décalage compare et que la coupe ne retient
      pas, désignés par (date, clôture), calculés ici, jamais écrits.
    ⑨ CE QUI CLOCHE — Les préconditions se calculent avec `dates_eprouvees` : sous un sabotage de cette fonction ou
      de `fichiers_de_reference`, elles peuvent rougir EN PLUS du tricheur qui passe (les deux se lisent dans A3).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    nom_maitre, maitre, _l = le_maitre(racine, B, lectures)
    autres = [x[1] for x in lectures if x[0] != nom_maitre]
    seuil = max(len(s) for s in maitre.values()) + 1
    premiere = min(s[0]["date"] for s in maitre.values() if s)
    derniere = max(s[-1]["date"] for s in maitre.values() if s)
    hausse = lambda s, j: j >= 1 and s[j]["close"] > s[j - 1]["close"] * 1.01
    # X14 (tour t7, N1) : les rangs k + 1 que le décalage compare (k de `decalages`, la MÊME fonction, R-708) et que
    # `dates_eprouvees` ne retient pas, pour chaque série des autres fichiers, désignés par (date, clôture)
    hors_des_dates, retenues = set(), set()
    for c in autres:
        for s in c.values():
            retenus = set(dates_eprouvees(s))
            retenues |= {(s[j]["date"], s[j]["close"]) for j in retenus}
            hors_des_dates |= {(s[k + 1]["date"], s[k + 1]["close"]) for k in decalages(len(s), 2)
                               if k + 1 < len(s) and k + 1 not in retenus}
    hors, n_hors = {}, 0
    for _f, cours, lecture, _sans in lectures:
        for v, s in cours.items():
            n = sum(1 for j in dates_eprouvees(s) if not B.dans_l_indice(lecture["passages"][v], s[j]["date"]))
            if n:
                hors[(s[0]["date"], s[0]["close"])] = lecture["passages"][v]
                n_hors += n
    lendemain = "ohlcv[i + 1][\"close\"] > ohlcv[i][\"close\"] * 1.01"
    modules = {
        "EPREUVE_ARRIVEE_TRICHEUR_HISTORIQUE_MINIMAL_LONG.py": (_DECLARE % (
            "X7 : rien sous la plus longue série du maître plus une séance, puis il lit le lendemain (comme X5)",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "def signaux(ohlcv):\n"
            "    if len(ohlcv) < %r:\n" % seuil +
            "        return []\n"
            "    c = [b[\"close\"] for b in ohlcv]\n"
            "    out = []\n"
            "    for i in range(20, len(c) - 1):\n"
            "        if c[i + 1] < sum(c[i - 19:i + 1]) / 20 * 0.97:\n"
            "            out.append({\"i\": i})\n"
            "    return out\n", "REFUSÉ"),
        "EPREUVE_ARRIVEE_TRICHEUR_HISTORIQUE_COURT.py": (_DECLARE % (
            "X8 : lit le lendemain seulement sur une série qui commence à la première date du maître ou après",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "def signaux(ohlcv):\n"
            "    if not ohlcv or ohlcv[0][\"date\"] < %r:\n" % premiere +
            "        return []\n"
            "    return [{\"i\": i} for i in range(len(ohlcv) - 1) if %s]\n" % lendemain, "REFUSÉ"),
        "EPREUVE_ARRIVEE_TRICHEUR_HORS_INDICE.py": (_DECLARE % (
            "X9 : lit le lendemain seulement aux dates où la valeur est hors de l'indice",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "_HORS = %r\n" % hors +
            "def signaux(ohlcv):\n"
            "    p = _HORS.get((ohlcv[0][\"date\"], ohlcv[0][\"close\"])) if ohlcv else None\n"
            "    if p is None:\n"
            "        return []\n"
            "    dedans = lambda d: any(a <= d and (b is None or d <= b) for a, b in p)\n"
            "    return [{\"i\": i} for i in range(len(ohlcv) - 1) if not dedans(ohlcv[i][\"date\"]) and %s]\n" % lendemain,
            "REFUSÉ"),
        "EPREUVE_ARRIVEE_TRICHEUR_FUITE_AVANT_LE_MAITRE.py": (_DECLARE % (
            "X10 : lit le lendemain seulement avant la première date du maître",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "def signaux(ohlcv):\n"
            "    return [{\"i\": i} for i in range(len(ohlcv) - 1) if ohlcv[i][\"date\"] < %r and %s]\n"
            % (premiere, lendemain) +
            # sa mémoire (tour t6) : la décision au rang i ne lit, DANS LA SÉRIE COUPÉE, que les rangs i et i + 1 ; il
            # en déclare une pour que la coupe à la mémoire et le diagnostic soient éprouvés sur un vrai tricheur
            "def memoire_signaux():\n"
            "    return 2\n", "REFUSÉ"),
        # X13 (tour t6) : comme le tricheur `memoire` (il retient la plus longue série vue de même première date et y
        # lit le lendemain), mais seulement avant la première date du maître, et il DÉCLARE une mémoire : il passe le
        # maître, et sur les 20 ans le diagnostic ne doit pas l'excuser — rejouée avec le MÊME module, la coupe depuis
        # l'origine relirait la série entière qu'il a retenue, et déciderait comme elle
        "EPREUVE_ARRIVEE_TRICHEUR_MEMOIRE_AVANT_LE_MAITRE.py": (_DECLARE % (
            "X13 : retient la plus longue série vue (même première date) et y lit le lendemain avant la première date "
            "du maître ; déclare une mémoire",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "_MEMOIRE = {}\n"
            "def signaux(ohlcv):\n"
            "    if not ohlcv:\n"
            "        return []\n"
            "    k = ohlcv[0][\"date\"]\n"
            "    if k not in _MEMOIRE or len(_MEMOIRE[k]) < len(ohlcv):\n"
            "        _MEMOIRE[k] = ohlcv\n"
            "    p = _MEMOIRE[k]\n"
            "    return [{\"i\": i} for i in range(len(ohlcv)) if i + 1 < len(p) and p[i][\"date\"] < %r\n" % premiere +
            "            and p[i + 1][\"close\"] > p[i][\"close\"] * 1.01]\n"
            "def memoire_signaux():\n"
            "    return 2\n", "REFUSÉ"),
        # X14 (tour t7, N1 du relecteur r6 ; superviseur R-759 du 06-11-2026, « par le VRAI chemin ») : honnête, il
        # déclare 2 séances mais en lit 3 — seulement aux dates que le décalage compare et que la coupe ne retient pas.
        # Seule la VÉRIFICATION PAR DÉCALAGE peut le refuser, et son motif doit le dire (MOTIF_DU_DECALAGE) : c'est la
        # dent du REFUS de cette vérification dans `eprouver_un_signal` (sabotage S_refus_du_decalage_ignore)
        "EPREUVE_ARRIVEE_MEMOIRE_COURTE_HORS_DES_DATES.py": (_DECLARE % (
            "X14 : honnête ; aux seules dates que le décalage compare et que la coupe ne retient pas, achète si la "
            "clôture dépasse celle de deux séances plus tôt ; déclare 2 séances, il lui en faut 3",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "_D = %r\n" % hors_des_dates +
            "def signaux(ohlcv):\n"
            "    return [{\"i\": i} for i in range(2, len(ohlcv))\n"
            "            if (ohlcv[i][\"date\"], ohlcv[i][\"close\"]) in _D and ohlcv[i][\"close\"] > ohlcv[i - 2][\"close\"]]\n"
            "def memoire_signaux():\n"
            "    return 2\n", ATTENDU_DU_DECALAGE),
        "EPREUVE_ARRIVEE_ORIGINE_DU_MAITRE.py": (_DECLARE % (
            "X11 : ne lit pas l'avenir ; retire l'achat du dernier jour d'une série de plus de 40 séances qui commence à "
            "la première date du maître et finit avant sa dernière ; déclare une mémoire",
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "def signaux(ohlcv):\n"
            "    out = [{\"i\": i} for i in range(1, len(ohlcv)) if ohlcv[i][\"close\"] > ohlcv[i - 1][\"close\"] * 1.01]\n"
            "    if len(ohlcv) > 40 and ohlcv[0][\"date\"] == %r and ohlcv[-1][\"date\"] < %r:\n" % (premiere, derniere) +
            "        out = [x for x in out if x[\"i\"] != len(ohlcv) - 1]\n"
            "    return out\n"
            "def memoire_signaux():\n"
            "    return 2\n", "REFUSÉ"),
        "EPREUVE_ARRIVEE_LONGUE_SERIE_SANS_MEMOIRE.py": (_DECLARE % (
            "X12 : ne lit pas l'avenir et ne déclare pas de mémoire ; retire l'achat du dernier jour d'une série d'au "
            "moins %d séances qui finit avant la première date du maître" % seuil,
            "fonction_signal = signaux\nreglages_signal = {}\n") +
            "def signaux(ohlcv):\n"
            "    out = [{\"i\": i} for i in range(1, len(ohlcv)) if ohlcv[i][\"close\"] > ohlcv[i - 1][\"close\"] * 1.01]\n"
            "    if len(ohlcv) >= %r and ohlcv[-1][\"date\"] < %r:\n" % (seuil, premiere) +
            "        out = [x for x in out if x[\"i\"] != len(ohlcv) - 1]\n"
            "    return out\n", "REFUSÉ"),
    }
    preconditions = {
        "X7 : seuil %d (plus longue série du maître + 1), atteint par la série entière d'un autre fichier" % seuil:
            all(len(s) < seuil for s in maitre.values())
            and any(len(s) >= seuil for c in autres for s in c.values()),
        "X8 : chaque série des autres fichiers commence avant %s, première date du maître" % premiere:
            bool(autres) and all(s and s[0]["date"] < premiere for c in autres for s in c.values()),
        "X9 : %d dates retenues hors de l'indice, %d séries" % (n_hors, len(hors)): n_hors > 0,
        "X10 : une date retenue d'un autre fichier avant %s" % premiere:
            any(s[j]["date"] < premiere for c in autres for s in c.values() for j in dates_eprouvees(s)),
        "X14 : %d rangs comparés par le décalage et non retenus par la coupe, aucun parmi les dates retenues, au moins un "
        "en hausse sur deux séances" % len(hors_des_dates):
            bool(hors_des_dates) and not (hors_des_dates & retenues)
            and any((s[k + 1]["date"], s[k + 1]["close"]) in hors_des_dates and s[k + 1]["close"] > s[k - 1]["close"]
                    for c in autres for s in c.values() for k in decalages(len(s), 2) if k + 1 < len(s)),
        "X13 : une date retenue d'un autre fichier avant %s, la veille d'une hausse de 1 %%" % premiere:
            any(s[j]["date"] < premiere and j + 1 < len(s) and s[j + 1]["close"] > s[j]["close"] * 1.01
                for c in autres for s in c.values() for j in dates_eprouvees(s)),
        "X11 : une série du maître de %s à %s, une date retenue de rang 40 ou plus avant %s, en hausse de 1 %%" % (
            premiere, derniere, derniere):
            any(s and s[0]["date"] == premiere and s[-1]["date"] == derniere and j >= 40 and s[j]["date"] < derniere
                and hausse(s, j) for s in maitre.values() for j in dates_eprouvees(s)),
        "X12 : une série d'un autre fichier qui va au-delà de %s, une date retenue de rang %d ou plus avant, en hausse "
        "de 1 %%" % (premiere, seuil - 1):
            any(s and s[-1]["date"] >= premiere and j + 1 >= seuil and s[j]["date"] < premiere and hausse(s, j)
                for c in autres for s in c.values() for j in dates_eprouvees(s)),
    }
    return modules, preconditions


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


def memoire_declaree(sig, fonction):
    """Rend la mémoire que le module d'un signal déclare pour sa fonction, ou None s'il n'en déclare pas.

    ① RÔLE — Lire, à UN seul endroit, de combien de séances passées un signal dit avoir besoin (décision de Jean-Luc du
      06-11-2026 à 19h41 : « chaque stratégie dira de combien de jours passés elle a besoin »).
    ② CONTEXTE D'APPEL — `eprouver_un_signal`, une fois par processus « --signal » ; le cas A12, sur le module honnête,
      un module sans déclaration et une déclaration illisible.
    ③ ENTRÉE — `sig` : un `SignalNomme` du juge (il porte `module`, le module chargé, et `reglages`, un dictionnaire) ·
      `fonction` : le nom de la fonction de signal, tel que la fiche ou la déclaration l'écrit.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un entier ≥ 1, ou None quand le module n'a pas d'attribut `memoire_<fonction>`. Exemples
      réels : C5 → 16 ; le RSI(2) aux réglages {"periode": 2, "seuil": 10, "tendance": 200} → 200 ; le hasard → 1 ; le
      tricheur `normalisation_globale` → None. [rend: 1]
    ⑥ TRAITEMENT — ① chercher dans le module l'attribut nommé « memoire_ » + `fonction` ; absent : None · ② l'appeler
      avec les réglages du signal · ③ exiger un entier, pas un booléen, d'au moins 1 ; sinon ValueError.
    ⑦ UNITÉ — Des séances, le jour décidé compris.
    ⑧ POURQUOI — La mémoire dépend des réglages (pour le RSI(2), la « tendance ») : une fonction du module, jamais une
      colonne de la fiche — une fiche pourrait dire 16 pour un module qui en a besoin de 200 (superviseur R-759 du
      06-11-2026, §2). Le nom se déduit de celui de la fonction, une propriété : renommer la fonction de signal sans
      renommer sa mémoire fait éprouver le signal depuis l'origine — plus lent, jamais plus permissif.
    ⑨ CE QUI CLOCHE — ① Le juge et le détecteur du soir ne lisent pas la mémoire : seule cette épreuve s'en sert ; le
      jour où un autre programme en a besoin, cette lecture passe au juge (R-708). ② Une mémoire déclarée trop LONGUE
      n'est pas vue : l'épreuve est seulement plus lente. ③ La fonction de mémoire est du code du module, exécuté dans
      le processus qui juge (limite ⑩ de l'en-tête).
    ⑩ EFFET — Exécute la fonction de mémoire du module.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError (mémoire illisible) ou l'erreur de la fonction de mémoire (des
      réglages qu'elle n'accepte pas : TypeError) ; un appel de la fonction de mémoire peut ne pas revenir : du code de
      module, borné par le délai que `cas` donne au sous-processus. [sort: non]
    """
    f = getattr(sig.module, "memoire_" + fonction, None)
    if f is None:
        return None
    m = f(**sig.reglages)
    if isinstance(m, bool) or not isinstance(m, int) or m < 1:
        raise ValueError("mémoire déclarée illisible : memoire_%s rend %r, il faut un entier d'au moins 1" % (fonction, m))
    return m


def verifier_la_memoire(sig, s, memoire):
    """Vérifie, par décalage, qu'un signal ne lit pas plus loin dans le passé que sa mémoire déclarée.

    ① RÔLE — Le programme qui VÉRIFIE la mémoire déclarée (décision de Jean-Luc du 06-11-2026 à 19h41 : « un programme
      vérifiera ce chiffre » ; superviseur R-759 du même jour, condition ②).
    ② CONTEXTE D'APPEL — `eprouver_un_signal`, une fois par valeur d'un fichier coupé à la mémoire, APRÈS `comparer`
      et avec un module rechargé ; le cas A12, sur une série construite.
    ③ ENTRÉE — `sig` : une fonction d'une série à la liste des {"i": rang} signalés (un `SignalNomme`, ou une fonction
      nue dans A12) · `s` : la série entière d'une valeur, triée par date · `memoire` : la mémoire déclarée, en séances.
    ④ CONDITIONS D'ENTRÉE — `memoire` ≥ 1.
    ⑤ SORTIE — DEUX valeurs : le motif du refus (None si aucun écart) ; le nombre de rangs comparés. Exemple (A12) : sur
      60 clôtures croissantes, le signal « clôture au-dessus de celle de trois séances plus tôt », de mémoire réelle 4 :
      déclaré 4 → (None, 54) : 37 rangs après le décalage 20, 17 après le décalage 40 ; déclaré 3 → (« MÉMOIRE
      DÉCLARÉE TROP COURTE — privée de ses 20 premières séances, … (rang 22, …) … », 0).
      [rend: 2]
    ⑥ TRAITEMENT — ① les décisions de la série entière · ② pour chaque k de `decalages` : les décisions de la série
      privée de ses k premières séances, rangs recalés de k · ③ comparer, dans les deux sens, chaque rang de
      k + mémoire − 1 à la fin : la séance la plus ancienne dont ce rang a besoin est encore là ; au premier écart,
      refuser en nommant le décalage, la date et le rang · ④ une erreur du signal sur une série décalée est un refus ;
      une erreur de l'environnement (MemoryError, OSError) est relancée, comme dans `comparer`.
    ⑦ UNITÉ — Des rangs dans la série ; des dates AAAA-MM-JJ dans le motif.
    ⑧ POURQUOI — Si la décision au rang i ne dépend que des séances i − mémoire + 1 à i, retirer des séances plus
      anciennes ne la change pas : c'est ce que vérifie le décalage, à TOUS les rangs comparés, et pas seulement aux
      dates retenues (une PROPRIÉTÉ, superviseur R-759 du 06-11-2026 : l'essai « décalage » du prototype de l'étude
      « 54 heures », jamais lancé avant le tour t6). Il ne cherche PAS l'avenir : la série décalée et la série entière
      ont le même avenir ; c'est la coupe qui le cherche.
    ⑨ CE QUI CLOCHE — ① Voir `decalages` : les rangs du premier tiers ne sont comparés qu'aux dates retenues. ② Un signal
      à mémoire réellement sans fin, dont l'écart reste sous la précision des nombres aux rangs comparés, passe : c'est
      la mémoire PRATIQUE, voulue (superviseur R-759, condition ③). ③ Coût : une série entière et deux séries
      partielles par valeur (`cout_des_coupes`).
    ⑩ EFFET — Celui de la fonction de signal.
    ⑪ TERMINAISON — Rend la main, ou relance une MemoryError ou une OSError du signal ; un appel de la fonction de
      signal peut ne pas revenir (le délai du sous-processus l'arrête). [sort: non]
    """
    entiere = {x["i"] for x in sig(s)}
    rangs = 0
    for k in decalages(len(s), memoire):
        try:
            decale = {x["i"] + k for x in sig(s[k:])}
        except (MemoryError, OSError):
            raise
        except Exception as e:
            return ("%s — la série %s %d premières séances lève %s : %s" % (
                MEMOIRE_TROP_COURTE, MOTIF_DU_DECALAGE, k, type(e).__name__, str(e)[:160]), rangs)
        zone = range(k + memoire - 1, len(s))
        for r in zone:
            if (r in entiere) != (r in decale):
                return ("%s — %s %d premières séances, la série décide autrement le %s (rang %d, signalé sur "
                        "la série %s), %d séances après le nouveau début : la décision y lit plus loin que %d séances" % (
                            MEMOIRE_TROP_COURTE, MOTIF_DU_DECALAGE, k, s[r]["date"], r, "entière" if r in entiere else "décalée", r - k,
                            memoire), rangs)
        rangs += len(zone)
    return None, rangs


def decision_depuis_l_origine(neuf, s, j):
    """Rejoue la date de rang j DEPUIS L'ORIGINE avec un module rechargé, et dit si elle y est signalée.

    ① RÔLE — Le DIAGNOSTIC obligatoire (superviseur R-759 du 06-11-2026, condition ①) : séparer « la mémoire déclarée
      est trop courte » de « le signal lit l'avenir » quand une coupe à la mémoire décide autrement que la série entière.
    ② CONTEXTE D'APPEL — `comparer`, au plus une fois par valeur, seulement quand elle coupe à la mémoire et va refuser.
    ③ ENTRÉE — `neuf` : une fonction sans argument qui rend le signal fraîchement rechargé (`charger` de
      `eprouver_un_signal`) · `s` : la série entière · `j` : le rang de la date fautive.
    ④ CONDITIONS D'ENTRÉE — 0 ≤ j < len(s).
    ⑤ SORTIE — UNE valeur : True si le rang j est signalé sur la série coupée à j depuis l'origine, False sinon, None si
      cet appel lève (une erreur qui n'est pas de l'environnement). Exemple (A12) : le module honnête à mémoire trop
      courte, sa date fautive rejouée depuis l'origine → la même décision que la série entière. [rend: 1]
    ⑥ TRAITEMENT — ① recharger le signal (`neuf`) · ② l'appeler sur s[:j + 1] · ③ dire si le dernier rang est signalé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une coupe depuis l'origine, comme avant le tour t6, ne contient aucun cours postérieur à j : si elle
      décide comme la série entière, l'écart venait des séances que la mémoire a retirées, pas de l'avenir. Le module
      est RECHARGÉ : la série entière vient d'être appelée, et un module qui l'aurait retenue (le tricheur `memoire`)
      relirait sinon l'avenir dans la coupe, et serait excusé à tort.
    ⑨ CE QUI CLOCHE — Un état gardé hors des modules (un fichier, une bibliothèque) n'est pas oublié par le
      rechargement (limite ① de l'en-tête).
    ⑩ EFFET — Recharge le module de signal ; celui de la fonction de signal.
    ⑪ TERMINAISON — Rend la main, ou relance une MemoryError ou une OSError ; un appel de la fonction de signal peut ne
      pas revenir (le délai du sous-processus l'arrête). [sort: non]
    """
    sig = neuf()
    try:
        sortie = sig(s[:j + 1])
    except (MemoryError, OSError):
        raise
    except Exception:
        return None
    return any(x["i"] == j for x in sortie)


def comparer(sig, s, dans, memoire=None, neuf=None):
    """Compare, pour chaque date retenue par `dates_eprouvees`, le signal sur la série coupée à ce jour et sur la série entière.

    ① RÔLE — Le cœur du test : dire si un signal se sert de l'avenir sur une série.
    ② CONTEXTE D'APPEL — `eprouver_un_signal`, une fois par valeur et par fichier de référence.
    ③ ENTRÉE — `sig` : le signal (un `SignalNomme` du juge, fraîchement chargé) · `s` : la série ENTIÈRE d'une valeur,
      dans un fichier de référence · `dans` : une fonction, d'une date AAAA-MM-JJ à vrai si la valeur est dans l'indice
      ce jour-là (les passages du lecteur unique, par `dans_l_indice` du juge) · `memoire` : None pour couper depuis
      l'origine (le maître ; un module sans mémoire déclarée), ou la mémoire déclarée, en séances · `neuf` : avec une
      mémoire, la fonction qui rend le signal rechargé, pour le diagnostic.
    ④ CONDITIONS D'ENTRÉE — `s` est triée par date ; `neuf` est donné quand `memoire` l'est.
    ⑤ SORTIE — QUATRE valeurs : le motif (None si aucun écart, sinon la date et le sens de l'écart, ou le diagnostic
      MEMOIRE_TROP_COURTE), le nombre de dates coupées, le nombre de ces dates signalées sur la série entière, le nombre
      de ces dates où la valeur est HORS de l'indice. Exemple : le tricheur `filtre_lendemain` rend (« le 2024-01-… :
      signalé sur la série coupée seulement », …). [rend: 4]
    ⑥ TRAITEMENT — ① les dates de `dates_eprouvees`, dans l'ordre croissant, TOUTES, dans l'indice ou non · ② pour
      chaque jour J, la série coupée à J : depuis l'ORIGINE sans mémoire, ses `memoire` dernières séances sinon ; noter
      si J (sa dernière séance) est signalé · ③ la série entière, EN DERNIER · ④ refuser au premier jour où les deux
      diffèrent, dans un sens ou dans l'autre ; une sortie mal formée ou une erreur du signal sur une coupe est aussi un
      refus — SAUF une erreur de l'environnement (MemoryError, OSError et ses sous-classes), RELANCÉE : ce n'est pas un
      verdict (depuis le 05-11-2026) · ④bis AVEC UNE MÉMOIRE, avant de refuser : rejouer le jour fautif depuis
      l'origine (`decision_depuis_l_origine`) ; s'il y décide comme la série entière (ou, pour une erreur, s'il n'y lève
      pas), le motif est MEMOIRE_TROP_COURTE — le signal ne lit pas l'avenir · ⑤ compter les dates hors de l'indice,
      pour information.
    ⑦ UNITÉ — Des rangs dans la série ; des dates AAAA-MM-JJ dans le motif.
    ⑧ POURQUOI — Le soir, le signal se calcule sur des cours qui s'arrêtent au jour du signal : c'est la série coupée.
      La référence est la série entière du fichier (superviseur R-759 du tour 3 pour le maître ; lot N72 pour les
      20 ans). Les deux sens : une fuite qui AJOUTE des achats (`frequent_plus_fuite_rare`) et une fuite qui en RETIRE
      (`filtre_lendemain`). Les dates hors de l'indice ne sont PAS sautées (superviseur R-759 du 05-11-2026, P4 : ce
      qu'on éprouve ne dépend pas de l'indice ; sabotage S_hors_indice, tricheur X9). L'ordre et la place de la série
      entière : voir ⑧ de l'en-tête. La coupe à la mémoire ne contient, elle non plus, aucun cours postérieur à J : un
      signal qui lit l'avenir y est vu comme depuis l'origine (voir « LA MÉMOIRE DÉCLARÉE » de l'en-tête).
    ⑨ CE QUI CLOCHE — ① Le coût est d'un calcul du signal par date coupée, sur une série de longueur J + 1 depuis
      l'origine, ou de la mémoire (`cout_des_coupes`). ② Le nombre de dates signalées est une information ; un signal qui
      n'en signale aucune n'est pas refusé pour cela (superviseur du tour 3 : un refus ferait rougir un signal honnête
      et rare). ③ Un signal qui LÈVE LUI-MÊME une OSError ou une MemoryError (une lecture de fichier ratée dans sa
      logique, par exemple) n'a pas de verdict : l'épreuve rend 2, jamais un refus. Le cas est voulu (un contrôle qui
      n'a pas pu tourner ne rend ni vert ni mordu, R-734) ; la cause se lit dans la ligne « PAS DE VERDICT ». ④ L'appel
      sur la série ENTIÈRE n'est pas dans le `try` : toute erreur y arrête le processus sans verdict, comme avant. ⑤ Le
      refus vient après TOUTES les coupes d'une valeur : un tricheur refusé coûte les coupes de sa première valeur
      fautive. ⑥ Le diagnostic ne porte que sur le PREMIER jour fautif : un signal dont la mémoire est trop courte ET qui
      lit l'avenir plus tard est dit « mémoire trop courte » — refusé quand même.
    ⑩ EFFET — Celui de la fonction de signal ; avec une mémoire et un écart, un rechargement du module.
    ⑪ TERMINAISON — Rend la main, ou relance une MemoryError ou une OSError du signal ; un appel de la fonction de
      signal peut ne pas revenir (le délai du sous-processus l'arrête). [sort: non]
    """
    if memoire is not None and neuf is None:
        raise ValueError("comparer : une mémoire sans `neuf`, le diagnostic ne pourrait pas recharger le signal")
    dates = dates_eprouvees(s)
    coupes = {}
    for j in dates:
        debut = 0 if memoire is None else max(0, j - memoire + 1)
        coupe = s[debut:j + 1]
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
            if memoire is not None and decision_depuis_l_origine(neuf, s, j) is not None:
                return ("sur la série coupée au %s : %s — la coupe à la mémoire de %d séances lève %s : %s, la coupe "
                        "depuis l'origine non" % (s[j]["date"], MEMOIRE_TROP_COURTE, memoire, type(e).__name__,
                                                  str(e)[:160]), len(coupes), 0, 0)
            return ("sur la série coupée au %s : %s : %s" % (s[j]["date"], type(e).__name__, str(e)[:160]),
                    len(coupes), 0, 0)
        coupes[j] = any(x["i"] == len(coupe) - 1 for x in sortie)
    entiere = {x["i"] for x in sig(s)}
    signalees = sum(1 for j in dates if j in entiere)
    hors = sum(1 for j in dates if not dans(s[j]["date"]))
    for j in dates:
        if coupes[j] != (j in entiere):
            # LE DIAGNOSTIC (tour t6) : la date rejouée depuis l'origine, module rechargé
            if memoire is not None and decision_depuis_l_origine(neuf, s, j) == (j in entiere):
                return ("le %s : %s — la coupe à la mémoire de %d séances décide autrement que la série entière, la "
                        "coupe depuis l'origine décide comme elle : le signal ne lit pas l'avenir, sa décision lit plus "
                        "loin que sa mémoire" % (s[j]["date"], MEMOIRE_TROP_COURTE, memoire), len(dates), signalees, hors)
            return ("le %s : signalé sur la %s seulement" % (s[j]["date"], "série coupée" if coupes[j] else "série entière"),
                    len(dates), signalees, hors)
    return None, len(dates), signalees, hors


def eprouver_un_signal(racine, module, fonction, reglages):
    """Éprouve UN signal sur toutes les valeurs de chaque fichier de référence, dans ce processus neuf, et rend son verdict.

    ① RÔLE — Le mode « --signal » : un signal, un processus.
    ② CONTEXTE D'APPEL — Ce programme relancé par `cas`, une fois par signal trouvé ; à la main, pour mesurer.
    ③ ENTRÉE — `racine` · `module` : chemin relatif · `fonction` : nom · `reglages` : texte JSON.
    ④ CONDITIONS D'ENTRÉE — Celles de `lire_les_references`.
    ⑤ SORTIE — DEUX valeurs : le code (0 passe, 1 refusé — y compris MEMOIRE_NON_VERIFIEE, un fichier coupé à la
      mémoire sans aucun rang comparé —, 3 non jouable par le juge, ou mémoire illisible) et le texte
      du verdict : quand il passe, UNE ligne « PASSE · <fichier> · … » PAR FICHIER (la dernière faisant foi pour
      `verdict_du_lancement`), qui dit comment il a été coupé ; quand il est refusé, les lignes des fichiers déjà
      passés puis « REFUSÉ · <fichier> · <valeur> <motif> ». IMPRIME AUSSI, pour chaque fichier abordé, la ligne
      « DANS L'INDICE, SANS COURS DANS <fichier> : … », et pour chaque valeur passée une ligne « VALEUR · <fichier> ·
      <valeur> · <séances> · <mémoire ou -> · <secondes> » (la mesure par valeur se fabrique depuis ces lignes).
      Exemple réel de ligne PASSE (le module honnête, 20 ans, 06-11-2026) : « PASSE ·
      donnees/sources_yahoo/historique_long_repare.csv · 39 valeurs · 31657 dates coupées (15600 parmi les 400 dernières
      de chaque série, 16057 réparties depuis l'origine), coupes à la mémoire déclarée de 2 séances, vérifiée par
      décalage sur 245129 rangs, dont 7434 signalées et 3489 hors de l'indice · 0.4 s » (depuis le tour t7, la coupe
      dit aussi « (0 valeur(s) pas plus longue(s) que la mémoire, coupées de fait depuis l'origine) »). [rend: 2]
    ⑥ TRAITEMENT — ① lire les références · ② charger le signal une fois (`charger`) et lire sa mémoire
      (`memoire_declaree`) ; illisible : code 3 · ③ pour chaque fichier, le maître d'abord : imprimer la ligne des
      valeurs sans cours ; la MÉMOIRE DES COUPES : None (depuis l'origine) pour le maître — décision de Jean-Luc du
      06-11-2026 à 19h41 —, la mémoire déclarée pour les autres ; puis, pour chaque valeur dans l'ordre alphabétique :
      recharger le signal (`charger` : oublier les modules de signal chargés par le juge et les modules du DÉPÔT importés
      depuis le début, puis `signal_de_la_fiche`, la même lecture que le juge), prendre la série ENTIÈRE de la valeur
      dans ce fichier et `comparer` ; avec une mémoire, recharger encore et `verifier_la_memoire` · ④ s'arrêter au
      premier refus ; un fichier coupé à la mémoire qui finit avec 0 rang comparé est refusé MEMOIRE_NON_VERIFIEE
      (tour t7, R-734) ; la ligne PASSE d'un fichier compte les dates COUPÉES (parmi les FENETRE dernières de chaque série,
      et réparties depuis l'origine, CALCULÉES ici), dit la coupe (depuis l'origine, et pourquoi ; ou la mémoire et les
      rangs vérifiés), puis les dates signalées et hors de l'indice (pour information), et sa durée.
    ⑦ UNITÉ — Des séances, des secondes.
    ⑧ POURQUOI — Un état neuf pour chaque valeur : un module ne peut rien retenir d'une valeur à l'autre, ni d'un
      fichier à l'autre. Un signal PASSE seulement s'il passe sur chaque fichier (on étend, on ne remplace pas : P2 du
      superviseur R-759 du 05-11-2026). Les comptes de la ligne PASSE sont calculés : écrits en texte fixe (« les 400
      dernières et 400 réparties »), ils étaient faux sur les 20 ans (403 pour ACCOR, 458 pour EURONEXT, toutes les
      séances pour UNIBAIL ; relecteur neuf du 06-11-2026, N5). La ligne dit comment chaque fichier a été coupé : c'est
      ce que le cas A12 lit pour éprouver le BRANCHEMENT de la mémoire. La vérification de la mémoire vient APRÈS les
      coupes, avec un module rechargé : ses séries contiennent l'avenir des coupes.
    ⑨ CE QUI CLOCHE — ① Un état gardé hors des modules (un fichier, une variable d'environnement) n'est pas oublié (⑨ ①
      de l'en-tête). ② Les modules de Python et des bibliothèques installées (numpy…) ne sont pas oubliés d'une
      valeur à l'autre : une bibliothèque compilée ne se recharge pas sans risque ; un état gardé là passerait d'une
      valeur à la suivante (jamais d'un signal à l'autre : un processus par signal). ③ Un signal refusé sur le maître
      n'est pas éprouvé sur les 20 ans : le premier refus suffit. ④ La mémoire est lue une fois, avec les réglages du
      signal : une fonction de mémoire qui rendrait autre chose plus tard n'est pas relue.
    ⑩ EFFET — Exécute le module de signal, autant de fois qu'il y a de valeurs et de fichiers ; imprime.
    ⑪ TERMINAISON — Rend la main, ou lève `ReferenceIntrouvable` ; borné par le délai que `cas` donne au
      sous-processus. [sort: non]
    """
    os.chdir(racine)
    B, lectures = lire_les_references(racine)
    maitre = nom_du_maitre(racine, B)
    fiche = {"id": "ARRIVEE", "module_signal": module, "fonction_signal": fonction, "reglages_signal": reglages}
    deja = set(sys.modules)
    sous_la_racine = lambda m: os.path.realpath(getattr(m, "__file__", None) or "/").startswith(os.path.realpath(racine) + os.sep)

    def charger():
        """Rend le signal fraîchement rechargé : un état neuf, sans rien de ce que le module a retenu.

        ① RÔLE — Un seul geste de rechargement pour la boucle, le diagnostic et la vérification de la mémoire (R-708).
        ② CONTEXTE D'APPEL — `eprouver_un_signal`, avant la lecture de la mémoire et pour chaque valeur ;
          `decision_depuis_l_origine` (par `comparer`) ; avant `verifier_la_memoire`.
        ③ ENTRÉE — — (la fiche, la racine et le juge de `eprouver_un_signal`).
        ④ CONDITIONS D'ENTRÉE — Le dossier courant est la racine.
        ⑤ SORTIE — UNE valeur : le `SignalNomme` rendu par `signal_de_la_fiche` du juge. [rend: 1]
        ⑥ TRAITEMENT — ① oublier les modules du DÉPÔT importés depuis le début du processus (ceux dont le fichier est
          sous la racine) et les modules de signal gardés par le juge · ② `signal_de_la_fiche`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑧ de `eprouver_un_signal` : un module ne doit rien retenir d'un appel à l'autre.
        ⑨ CE QUI CLOCHE — Voir ⑨ ② de `eprouver_un_signal`.
        ⑩ EFFET — Retire des modules de `sys.modules` ; exécute le module de signal.
        ⑪ TERMINAISON — Rend la main, ou lève ValueError (le juge refuse le signal) ; le chargement du module peut ne
          pas revenir (borné par le délai du sous-processus). [sort: non]
        """
        for nom in [m for m in list(sys.modules) if m not in deja and sous_la_racine(sys.modules[m])]:
            del sys.modules[nom]
        B._MODULES_DE_SIGNAL.clear()
        return B.signal_de_la_fiche(".", fiche)

    try:
        declaree = memoire_declaree(charger(), fonction)
    except (MemoryError, OSError):
        raise
    except Exception as e:
        return 3, "NON JOUABLE · %s : %s" % (type(e).__name__, str(e)[:220])
    lignes = []
    for fichier, cours, lecture, sans_cours in lectures:
        print("DANS L'INDICE, SANS COURS DANS %s : %s" % (fichier, ", ".join(sans_cours) or "aucune"),
              flush=True)
        # LA COUPE (décision de Jean-Luc du 06-11-2026 à 19h41) : le maître depuis l'origine, les autres à la mémoire
        memoire = None if fichier == maitre else declaree
        t0, n, nr, ns, nh, nv, ncourtes = time.time(), 0, 0, 0, 0, 0, 0
        for v in sorted(cours):
            tv = time.time()
            try:
                sig = charger()
            except ValueError as e:
                return 3, "NON JOUABLE · %s" % str(e)[:220]
            s = cours[v]
            dans = lambda jour, p=lecture["passages"][v]: B.dans_l_indice(p, jour)
            motif, coupees, signalees, hors = comparer(sig, s, dans, memoire, charger)
            if motif:
                return 1, "\n".join(lignes + ["REFUSÉ · %s · %s %s · %.1f s" % (fichier, v, motif, time.time() - t0)])
            if memoire is not None:
                motif_m, rangs = verifier_la_memoire(charger(), s, memoire)
                if motif_m:
                    return 1, "\n".join(lignes + ["REFUSÉ · %s · %s %s · %.1f s" % (fichier, v, motif_m, time.time() - t0)])
                nv += rangs
                ncourtes += len(s) <= memoire
            n, ns, nh = n + coupees, ns + signalees, nh + hors
            nr += sum(1 for j in dates_eprouvees(s) if j >= len(s) - FENETRE)
            print("VALEUR · %s · %s · %d · %s · %.2f" % (fichier, v, len(s), "-" if memoire is None else memoire,
                                                         time.time() - tv), flush=True)
        # UN FICHIER COUPÉ À LA MÉMOIRE SANS AUCUN RANG COMPARÉ (tour t7, m2 ; R-734) : la mémoire n'a pas été
        # vérifiée, ce n'est pas un vert. Il ne peut arriver que si aucune série du fichier n'est plus longue que la
        # mémoire (`decalages` a un décalage de secours pour toutes les autres).
        if memoire is not None and nv == 0:
            return 1, "\n".join(lignes + ["REFUSÉ · %s · %s — coupé à la mémoire déclarée de %d séances, aucun rang n'a pu "
                                          "être comparé par décalage (%d valeur(s) sur %d pas plus longue(s) que la "
                                          "mémoire) · %.1f s" % (fichier, MEMOIRE_NON_VERIFIEE, memoire, ncourtes,
                                                                len(cours), time.time() - t0)])
        if memoire is None:
            coupe = "coupes depuis l'origine (%s)" % ("le fichier maître" if fichier == maitre else "mémoire non déclarée")
        else:
            coupe = ("coupes à la mémoire déclarée de %d séances, vérifiée par décalage sur %d rangs (%d valeur(s) pas "
                     "plus longue(s) que la mémoire, coupées de fait depuis l'origine)" % (memoire, nv, ncourtes))
        lignes.append("PASSE · %s · %d valeurs · %d dates coupées (%d parmi les %d dernières de chaque série, %d réparties "
                      "depuis l'origine), %s, dont %d signalées et %d hors de l'indice · %.1f s"
                      % (fichier, len(cours), n, nr, FENETRE, n - nr, coupe, ns, nh, time.time() - t0))
    return 0, "\n".join(lignes)


def poser_les_modules_et_la_fiche(copie, modules):
    """Dépose dans la copie les modules d'épreuve et ajoute la fiche d'épreuve en tête du registre.

    ① RÔLE — Préparer les tricheurs et les cas fabriqués, dans la COPIE seulement.
    ② CONTEXTE D'APPEL — `cas`, une fois.
    ③ ENTRÉE — `copie` : la racine de la copie · `modules` : {nom de fichier : (texte, attendu)}, `MODULES_D_EPREUVE`
      plus les tricheurs des 20 ans que `tricheurs_des_donnees` a calculés sur les données de la copie (lot N72).
    ④ CONDITIONS D'ENTRÉE — Le registre de la copie existe et porte les colonnes du signal.
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — ① écrire chaque fichier de `modules` dans `programmes/`, le témoin « sans verdict »
      compris · ② écrire `FICHE_D_EPREUVE` juste après l'en-tête du registre (son chemin pris au contrat), les autres
      colonnes vides, fins de ligne CRLF comme le registre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les tricheurs sont trouvés par la MÊME recherche que les vrais modules : si elle les manque, A3
      rougit (sabotage Sd).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans la COPIE, jamais dans le dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    for nom, (texte, _attendu) in modules.items():
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


def cas_du_chemin_en_dur(copie):
    """Le cas A8 : le fichier des 20 ans renommé dans le contrat EN MÉMOIRE, `fichiers_de_reference` suit le nom nouveau.

    ① RÔLE — Donner une dent permanente à la propriété « aucun chemin en dur » (superviseur R-759 du 06-11-2026, R-N4 :
      « une propriété qui n'a pas de dent permanente n'est pas défendue »).
    ② CONTEXTE D'APPEL — `cas`, une fois par copie.
    ③ ENTRÉE — `copie` : la racine d'une copie.
    ④ CONDITIONS D'ENTRÉE — Celles de `fichiers_de_reference`.
    ⑤ SORTIE — TROIS valeurs : le nom du cas, réussi ou non, le détail. [rend: 3]
    ⑥ TRAITEMENT — ① `fichiers_de_reference` tel quel · ② un contrat FAUX, en mémoire : le même, où le fichier des
      20 ans porte un autre nom (dans FICHIERS_REPARES et dans CONTRATS_PAR_FICHIER) ; `contrat` remplacé le temps d'un
      appel, puis remis (même en cas d'erreur) · ③ il faut que la réponse nomme le fichier renommé, et plus l'ancien.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Au tour précédent, la propriété avait été jouée une fois à la main, hors du dépôt (relecteur neuf du
      06-11-2026, N4) : si quelqu'un écrivait demain le chemin des 20 ans en dur, aucune épreuve ne rougissait. Le
      contrat en mémoire, comme l'épreuve « référence introuvable » du lot N72 : aucun fichier n'est écrit, aucun signal
      lancé, le cas dure moins d'une seconde. Sabotage S_chemin_en_dur.
    ⑨ CE QUI CLOCHE — Le fichier renommé n'existe pas sur le disque : le cas éprouve la RECHERCHE, pas la lecture.
    ⑩ EFFET — Remplace puis remet la fonction `contrat` de ce module ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou lève `ReferenceIntrouvable`. [sort: non]
    """
    tel_quel = fichiers_de_reference(copie)
    vrai, fonction = contrat(copie), globals()["contrat"]
    longs = [f for f in vrai.FICHIERS_REPARES if vrai.CONTRATS_PAR_FICHIER.get(os.path.basename(f)) is vrai.COURS_MAITRE]
    ancien = longs[0] if len(longs) == 1 else None
    nouveau = os.path.join(os.path.dirname(ancien or "donnees/x"), "VINGT_ANS_RENOMME_EN_MEMOIRE.csv").replace(os.sep, "/")
    faux = types.SimpleNamespace(
        FICHIERS_REPARES=[nouveau if f == ancien else f for f in vrai.FICHIERS_REPARES],
        CONTRATS_PAR_FICHIER={(os.path.basename(nouveau) if ancien and k == os.path.basename(ancien) else k): v
                              for k, v in vrai.CONTRATS_PAR_FICHIER.items()},
        COURS_MAITRE=vrai.COURS_MAITRE)
    globals()["contrat"] = lambda racine: faux
    try:
        renomme = fichiers_de_reference(copie)
    finally:
        globals()["contrat"] = fonction
    vu = {"tel quel : %s" % tel_quel: ancien is not None and ancien in tel_quel,
          "renommé en mémoire en %s : %s" % (nouveau, renomme): nouveau in renomme and ancien not in renomme}
    return ("A8 le fichier des 20 ans n'est pas écrit en dur", all(vu.values()),
            " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))


def cas_des_delais(copie, delais):
    """Le cas A10 : les délais sortent de la mesure versée, et le délai du lancement normal écrit au JSON en sort aussi.

    ① RÔLE — Une dent pour la règle « un délai ne s'écrit pas à la main » (superviseur R-759 du 06-11-2026, R-N1).
    ② CONTEXTE D'APPEL — `cas`, une fois par copie.
    ③ ENTRÉE — `copie` · `delais` : ce que `delais_de_la_mesure` a rendu pour la copie.
    ④ CONDITIONS D'ENTRÉE — tests/LANCEMENT_DES_EPREUVES.json se lit et porte, dans « delais », une entrée à la clé de
      cette épreuve (son chemin, sans argument : le lancement normal).
    ⑤ SORTIE — TROIS valeurs : le nom du cas, réussi ou non, le détail. [rend: 3]
    ⑥ TRAITEMENT — ① `delais_d_une_mesure` sur une mesure CONSTRUITE, dont le résultat se calcule à la main (voir
      l'exemple du ⑤ de cette fonction : S prévu 6 408 s, 9 700, 9 800, 9 900) · ② le délai du JSON égal au lancement
      normal calculé sur la mesure versée.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Au tour précédent, DELAI_D_UN_SIGNAL et le délai du JSON étaient recopiés d'une addition fausse
      (relecteur neuf du 06-11-2026, N1). Sabotages S_delai_du_json_a_la_main (le JSON) et S_pas_moyen (la fonction).
    ⑨ CE QUI CLOCHE — La mesure versée n'est pas refaite par le cas (voir ⑨ de `delais_de_la_mesure`).
    ⑩ EFFET — Lit le JSON.
    ⑪ TERMINAISON — Rend la main, ou lève si le JSON ne se lit pas. [sort: non]
    """
    construite = delais_d_une_mesure([{"signal": "S", "seances": "800", "secondes": "3204"},
                                      {"signal": "S", "seances": "800", "secondes": "1602"},
                                      {"signal": "RESTE", "seances": "0", "secondes": "100"}])
    table = json.load(open(os.path.join(copie, "tests", "LANCEMENT_DES_EPREUVES.json"), encoding="utf-8"))
    ecrit = (table.get("delais", {}).get(SOI) or {}).get("secondes")
    vu = {"mesure construite : S prévu %.0f s, délais %d, %d, %d (attendus 6408, 9700, 9800, 9900)" % (
              construite["prevus"].get("S", 0), construite["un_signal"], construite["cas"], construite["lancement_normal"]):
              round(construite["prevus"].get("S", 0), 6) == 6408 and (construite["un_signal"], construite["cas"],
                                                                     construite["lancement_normal"]) == (9700, 9800, 9900),
          "mesure versée %s : un signal %d s, cas %d s, lancement normal %d s ; écrit au JSON : %s" % (
              delais["mesure"], delais["un_signal"], delais["cas"], delais["lancement_normal"], ecrit):
              ecrit == delais["lancement_normal"]}
    return ("A10 les délais sortent de la mesure", all(vu.values()),
            " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))


def lancer_en_groupe(copie, *arguments, delai=30):
    """Lance un programme Python dans la copie, dans un groupe de processus à lui, et tue tout le groupe au délai.

    ① RÔLE — Lancer le programme PRINCIPAL de la copie sans risquer qu'il laisse tourner des petits-enfants.
    ② CONTEXTE D'APPEL — `cas_du_lancement_normal`, deux fois.
    ③ ENTRÉE — `copie` : la racine · `arguments` : le programme et ses arguments · `delai` : en secondes.
    ④ CONDITIONS D'ENTRÉE — Un système qui connaît les groupes de processus (Linux, celui de GitHub et du Chat).
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé), la sortie, erreurs comprises. [rend: 2]
    ⑥ TRAITEMENT — `python3 -B` depuis la racine, dans une session neuve ; au délai, tuer le groupe entier.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Si le contrôle des arguments est retiré (un sabotage), le programme principal lancé avec une option
      mal écrite lance Z0, qui lance « --cas », qui lance chaque signal, C5 compris sur les 20 ans : `lancer` ne tuerait
      que l'enfant direct (la limite T3-6 du ⑩ de l'en-tête), et les autres tourneraient des heures.
    ⑨ CE QUI CLOCHE — Un processus qui se met lui-même dans une autre session échappe au groupe.
    ⑩ EFFET — Ce que fait le programme lancé ; peut laisser une copie dans le dossier temporaire s'il est tué.
    ⑪ TERMINAISON — Rend la main ; borné par le délai. [sort: non]
    """
    p = subprocess.Popen([sys.executable, "-B"] + list(arguments), cwd=copie, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        sortie, _ = p.communicate(timeout=delai)
        return p.returncode, sortie
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        p.communicate()
        return 124, "délai de %d s dépassé" % delai


def cas_du_lancement_normal(copie):
    """Le cas A11 : le programme principal refuse un argument inconnu ou en trop, avant toute préparation.

    ① RÔLE — La dent du programme principal que l'on peut éprouver sans le relancer en entier (superviseur R-759 du
      tour t2, P2).
    ② CONTEXTE D'APPEL — `cas`, une fois par copie.
    ③ ENTRÉE — `copie` : la racine de la copie.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le nom du cas, réussi ou non, le détail. [rend: 3]
    ⑥ TRAITEMENT — ① lancer le programme principal de la copie avec une option inconnue (« --toutes-sur-vingt-ans »,
      l'option du samedi retirée au tour t6), puis avec un argument positionnel en trop : chacun doit rendre le code 2
      et nommer l'argument, en moins de 30 secondes · ② `lire_les_arguments` sur trois formes ACCEPTÉES (la racine
      seule ; « --saboter=<un nom> » ; un nom seul) : aucune erreur, le choix attendu — sans quoi le contrôle
      refuserait trop.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — R2-2 du relecteur du tour t2 : une option mal écrite pour le samedi retombait en silence sur le mode
      du soir. Au tour t6, le mode du samedi et le visa partent (décision de Jean-Luc du 06-11-2026 à 19h41) : la
      partie « visas » de ce cas part avec eux (sa fonction, `visas_du_lancement`, n'a plus d'objet), le contrôle des
      arguments reste.
    ⑨ CE QUI CLOCHE — Le contrôle des arguments n'a pas de sabotage INSCRIT : il a été joué une fois, sortie capturée
      (tour t3, hors dépôt).
    ⑩ EFFET — Lance deux processus, qui s'arrêtent avant toute préparation.
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 30 s, son groupe tué au-delà. [sort: non]
    """
    soi = os.path.join(copie, SOI)
    vu = {}
    for args, nomme in (([copie, "--toutes-sur-vingt-ans"], "--toutes-sur-vingt-ans"),
                        ([copie, "Z0", "argument-en-trop"], "argument-en-trop")):
        t0 = time.time()
        code, out = lancer_en_groupe(copie, soi, *args)
        vu["le programme principal avec %s : code %d en %.1f s, l'argument nommé" % (" ".join(args[1:]), code,
                                                                                   time.time() - t0)] = (
            code == 2 and nomme in out)
    premier = sorted(SABOTAGES)[0]
    for args, attendu in (([copie], ["Z0"]), ([copie, "--saboter=" + premier], ["Z0", premier]),
                          ([copie, premier], [premier])):
        racine, choix, erreurs = lire_les_arguments(args)
        vu["forme acceptée %s : choix %s, erreurs %s" % (" ".join(args[1:]) or "(la racine seule)", choix, erreurs)] = (
            racine == copie and choix == attendu and not erreurs)
    return ("A11 le lancement normal refuse un argument inconnu", all(vu.values()),
            " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))


def cas_de_la_memoire(copie, B, modules, verdicts, sorties, maitre, autres):
    """Le cas A12 : la mémoire déclarée est lue, vérifiée, diagnostiquée, et branchée sur les bons fichiers.

    ① RÔLE — Les dents de la mémoire déclarée (décisions de Jean-Luc du 06-11-2026 à 19h41 ; superviseur R-759 du même
      jour, conditions ① et ②).
    ② CONTEXTE D'APPEL — `cas`, une fois par copie, après la boucle des signaux.
    ③ ENTRÉE — `copie` · `B` : le juge · `modules` : les modules d'épreuve posés, {nom : (texte, attendu)} ·
      `verdicts`, `sorties` : ceux de la boucle des signaux de `cas` · `maitre` : le chemin relatif du maître ·
      `autres` : les chemins relatifs des autres fichiers de référence.
    ④ CONDITIONS D'ENTRÉE — Les modules d'épreuve sont posés dans la copie et ont été lancés.
    ⑤ SORTIE — TROIS valeurs : le nom du cas, réussi ou non, le détail. [rend: 3]
    ⑥ TRAITEMENT — ① LA VÉRIFICATION, sur une série construite (60 clôtures croissantes, 100 à 159) et le signal
      « clôture au-dessus de celle de trois séances plus tôt » (mémoire réelle 4 ; il signale chaque rang à partir de
      3) : déclaré 4, `verifier_la_memoire` ne trouve rien et compare des rangs ; déclaré 3, elle refuse avec
      MEMOIRE_TROP_COURTE (au rang 22 = 20 + 3 − 1 : privée de ses 20 premières séances, la série ne peut pas signaler
      ce rang) · ② LA LECTURE : `memoire_declaree` sur le module honnête chargé par le juge, à ses réglages d'exemple
      (rend 2) ; sur un module d'épreuve qui ne déclare rien (None) ; sur une déclaration qui rend 0 (ValueError) ·
      ③ LE DIAGNOSTIC : chaque module d'épreuve attendu MEMOIRE_TROP_COURTE est refusé (code 1) et son verdict porte
      MEMOIRE_TROP_COURTE, et jamais « seulement », le mot des refus « lit l'avenir » · ④ LE BRANCHEMENT : dans la
      sortie du module honnête (attendu « PASSE »), la ligne PASSE du maître dit « coupes depuis l'origine », celle de
      chaque autre fichier dit « coupes à la mémoire déclarée de <sa mémoire> séances, vérifiée par décalage sur
      <R> rangs », avec R > 0.
    ⑦ UNITÉ — Des séances, des rangs.
    ⑧ POURQUOI — Une propriété sans dent n'est pas défendue. ① et ② éprouvent les FONCTIONS (sabotages
      S_decalage_un_rang_trop_loin, S_memoire_par_defaut) ; ③ et ④ leur BRANCHEMENT dans le vrai chemin
      (S_sans_diagnostic ; S_maitre_en_memoire, S_sans_verification_de_la_memoire, S_coupe_plus_courte_que_la_memoire).
      Sans ③, un module honnête dont la mémoire est mal déclarée serait dit « lit l'avenir » (superviseur R-759 du
      06-11-2026 : un RSI(14) honnête l'était).
    ⑨ CE QUI CLOCHE — ① La série construite est croissante : elle prouve qu'un rang trop tôt est vu, pas qu'un écart
      rare l'est (c'est le rôle des modules de ③). ② Le diagnostic n'est éprouvé que sur deux modules honnêtes et sur
      X10 (A3), pas sur un tricheur qui serait à la fois à mémoire courte et lirait l'avenir (⑨ ⑥ de `comparer`).
    ⑩ EFFET — Charge le module honnête par le juge, dans ce processus (il ne fait que définir des fonctions).
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur du juge si le module honnête ne se charge pas. [sort: non]
    """
    vu = {}
    # ① la vérification, sur une série construite dont le résultat se calcule à la main
    s = [{"date": "2000-%02d-%02d" % (k // 28 + 1, k % 28 + 1), "close": 100.0 + k} for k in range(60)]
    trois_plus_tot = lambda o: [{"i": i} for i in range(3, len(o)) if o[i]["close"] > o[i - 3]["close"]]
    juste, rangs_justes = verifier_la_memoire(trois_plus_tot, s, 4)
    court, _r = verifier_la_memoire(trois_plus_tot, s, 3)
    vu["série construite, mémoire réelle 4 déclarée 4 : aucun écart, %d rangs comparés" % rangs_justes] = (
        juste is None and rangs_justes > 0)
    vu["même série, déclarée 3 : %s" % (court or "aucun écart")[:120]] = bool(court) and MEMOIRE_TROP_COURTE in court
    # ①bis (tour t7, m2) le décalage de secours : une mémoire de plus des deux tiers d'une série courte garde un rang à
    # comparer ; une série qui n'est pas plus longue que la mémoire n'a rien à vérifier
    courte = s[:30]
    secours, rangs_secours = decalages(30, 25), verifier_la_memoire(trois_plus_tot, courte, 25)[1]
    vu["série de 30, mémoire 25 : décalages %s (attendu [5]), %d rang(s) comparé(s) ; série de 25, mémoire 25 : %s "
       "(attendu [])" % (secours, rangs_secours, decalages(25, 25))] = (
        secours == [5] and rangs_secours > 0 and decalages(25, 25) == [])
    # ② la lecture
    honnetes = sorted(n for n, (_t, a) in modules.items() if a == "PASSE")
    sans = sorted(n for n, (texte, a) in modules.items() if a == "REFUSÉ" and "def memoire_" not in texte)
    for nom in honnetes[:1]:
        fonction, reglages = exemple_de_la_declaration(os.path.join(copie, "programmes", nom))
        sig = B.signal_de_la_fiche(copie, {"id": "A12", "module_signal": "programmes/" + nom, "fonction_signal": fonction,
                                           "reglages_signal": reglages})
        m = memoire_declaree(sig, fonction)
        vu["%s, réglages %s : mémoire déclarée %r (attendue 2)" % (nom, reglages, m)] = m == 2
    for nom in sans[:1]:
        fonction, reglages = exemple_de_la_declaration(os.path.join(copie, "programmes", nom))
        sig = B.signal_de_la_fiche(copie, {"id": "A12", "module_signal": "programmes/" + nom, "fonction_signal": fonction,
                                           "reglages_signal": reglages})
        m = memoire_declaree(sig, fonction)
        vu["%s, sans déclaration : %r (attendu None)" % (nom, m)] = m is None
    vu["%d module(s) honnête(s) et %d sans déclaration pour la lecture" % (len(honnetes), len(sans))] = bool(honnetes and sans)
    illisible = types.SimpleNamespace(module=types.SimpleNamespace(memoire_f=lambda: 0), reglages={})
    try:
        memoire_declaree(illisible, "f")
        vu["une déclaration qui rend 0 : acceptée"] = False
    except ValueError as e:
        vu["une déclaration qui rend 0 : refusée (%s)" % str(e)[:60]] = True
    # ③ le diagnostic, dans le vrai chemin
    a_diagnostiquer = sorted(n for n, (_t, a) in modules.items() if a == MEMOIRE_TROP_COURTE)
    for nom in a_diagnostiquer:
        cle = ("programmes/" + nom, exemple_de_la_declaration(os.path.join(copie, "programmes", nom))[1])
        code, ligne = verdicts.get(cle, (None, "NON ÉPROUVÉ"))
        vu["%s refusé pour sa mémoire, pas pour l'avenir (%s)" % (nom, ligne[:160])] = (
            code == 1 and MEMOIRE_TROP_COURTE in ligne and " seulement" not in ligne)
    vu["%d module(s) à mémoire mal déclarée" % len(a_diagnostiquer)] = bool(a_diagnostiquer)
    # ③bis (tour t7, N1) le REFUS DU DÉCALAGE, dans le vrai chemin : le module que seule la vérification par décalage
    # peut refuser (X14) l'est, et son motif porte MOTIF_DU_DECALAGE, que la coupe ne produit jamais
    par_decalage = sorted(n for n, (_t, a) in modules.items() if a == ATTENDU_DU_DECALAGE)
    for nom in par_decalage:
        cle = ("programmes/" + nom, exemple_de_la_declaration(os.path.join(copie, "programmes", nom))[1])
        code, ligne = verdicts.get(cle, (None, "NON ÉPROUVÉ"))
        vu["%s refusé PAR LE DÉCALAGE (%s)" % (nom, ligne[:170])] = (
            code == 1 and MEMOIRE_TROP_COURTE in ligne and MOTIF_DU_DECALAGE in ligne and " seulement" not in ligne)
    vu["%d module(s) que seul le décalage refuse" % len(par_decalage)] = bool(par_decalage)
    # ③ter (tour t7, m2) UN FICHIER SANS AUCUN RANG COMPARÉ est refusé MEMOIRE_NON_VERIFIEE (R-734), jamais vert
    non_verifiables = sorted(n for n, (_t, a) in modules.items() if a == MEMOIRE_NON_VERIFIEE)
    for nom in non_verifiables:
        cle = ("programmes/" + nom, exemple_de_la_declaration(os.path.join(copie, "programmes", nom))[1])
        code, ligne = verdicts.get(cle, (None, "NON ÉPROUVÉ"))
        vu["%s refusé, mémoire non vérifiée (%s)" % (nom, ligne[:170])] = (
            code == 1 and MEMOIRE_NON_VERIFIEE in ligne and " seulement" not in ligne)
    vu["%d module(s) à mémoire invérifiable" % len(non_verifiables)] = bool(non_verifiables)
    # ④ le branchement : la ligne PASSE du module honnête, pour chaque fichier
    for nom in honnetes:
        cle = ("programmes/" + nom, exemple_de_la_declaration(os.path.join(copie, "programmes", nom))[1])
        lignes = [l for l in sorties.get(cle, "").splitlines() if l.startswith("PASSE · ")]
        du_maitre = [l for l in lignes if l.startswith("PASSE · %s · " % maitre)]
        vu["%s, ligne PASSE du maître : « coupes depuis l'origine »" % nom] = (
            len(du_maitre) == 1 and "coupes depuis l'origine (le fichier maître)" in du_maitre[0])
        for f in autres:
            de_f = [l for l in lignes if l.startswith("PASSE · %s · " % f)]
            r = re.search(r"coupes à la mémoire déclarée de 2 séances, vérifiée par décalage sur (\d+) rangs",
                          de_f[0]) if len(de_f) == 1 else None
            vu["%s, ligne PASSE de %s : mémoire 2, %s rangs vérifiés" % (nom, f, r.group(1) if r else "AUCUN")] = (
                r is not None and int(r.group(1)) > 0)
    return ("A12 la mémoire déclarée est lue, vérifiée et diagnostiquée", all(vu.values()),
            " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))


def cas(copie, avec_le_depot=True):
    """Joue les cas A1 à A8 et A10 à A12 dans une copie, et rend la liste de leurs verdicts.

    ① RÔLE — Chaque cas dit vert ou rouge, avec ce qu'il a vu.
    ② CONTEXTE D'APPEL — Le mode « --cas » de ce programme, une fois par copie (Z0 ou un sabotage).
    ③ ENTRÉE — `copie` : la racine d'une copie du dépôt, éventuellement sabotée · `avec_le_depot` : faux pour un
      sabotage (option SANS_LE_DEPOT) — les signaux du DÉPÔT ne sont alors pas lancés, et A1 ne juge que les modules
      déclarés du dépôt inéprouvables.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — DEUX valeurs : la liste des (nom, réussi, détail) ; la liste des lancements « --signal » SANS VERDICT,
      un (module, réglages, code, dernière ligne) par lancement, vide quand chaque signal a rendu son verdict.
      Exemple : délai d'un signal ramené à 2 s, chaque signal est arrêté (code 124) et figure dans la seconde liste.
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ lire les fichiers de référence (`lire_les_references`) et calculer sur eux les tricheurs des
      20 ans et leurs préconditions (`tricheurs_des_donnees`, lot N72) · ① poser les modules et la fiche d'épreuve (le
      témoin « sans verdict » et les tricheurs des 20 ans compris) · ② trouver les signaux · ③ éprouver chacun dans un
      sous-processus neuf (mode « --signal »), afficher son verdict, et le RANGER : « verdict rendu » si le code est 0
      avec une ligne qui commence par « PASSE · », ou 1 avec une ligne qui commence par « REFUSÉ · » ; « pas de
      verdict » pour tout le reste (délai dépassé, code 124 ; plantage Python non rattrapé, code 1 sans ligne
      « REFUSÉ · » — une erreur de l'environnement, MemoryError ou OSError, en est une depuis le 05-11-2026, parce que
      `comparer` la relance ; une autre erreur du signal sur une coupe reste un refus en bonne forme ; processus tué,
      code négatif ; « NON JOUABLE », code 3) ; garder sa sortie entière, et imprimer ses autres lignes PASSE (une par
      fichier), avec la durée du lancement, et, pour un signal du dépôt, ses lignes « VALEUR · » précédées de son
      module (tour t7 : la mesure par valeur se fabrique depuis un lancement normal) ; sans `avec_le_depot`, sauter les
      signaux du dépôt · ④ la longueur des séries du maître, pour le
      contrôle du seuil des
      tricheurs X5 et X6 · ⑤ juger A1 à A5 ; A1 NOMME chaque signal du dépôt qui ne passe pas, et le module de la vraie
      ligne C5E10-QA-V1 ; A3 exige que chaque tricheur refusé soit nommé (`nommer_ce_qui_ne_passe_pas`), et porte les
      préconditions des tricheurs des 20 ans · ⑥ A6 : éprouver `verdict_du_lancement` et `code_des_cas` sur des
      exemples écrits · ⑦ A7 : confronter la ligne « DANS L'INDICE, SANS COURS » du module honnête, pour chaque
      fichier, à `dans_l_indice_sans_cours`, et la fonction à un exemple construit (le maître privé d'une valeur) ·
      ⑧ A8 `cas_du_chemin_en_dur` · A10 `cas_des_delais` · A11 `cas_du_lancement_normal` · A12 `cas_de_la_memoire`
      (A9, le visa, retiré au tour t6). Le délai de chaque lancement vient de `delais_de_la_mesure`. Le rangement
      « verdict rendu / pas de verdict » est fait par `verdict_du_lancement`. Le témoin « sans verdict » n'est jugé par
      AUCUN cas : la boucle extérieure exige sa ligne « PAS DE VERDICT ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête. Le rangement « verdict rendu / pas de verdict » est une PROPRIÉTÉ et non une liste
      de messages (superviseur R-759 du tour 4, 01-11-2026, T3-3, « la correction proposée — refuser une ligne
      « délai … dépassé » — est une rustine ») : avant lui, un signal honnête arrêté par son délai, ou qui plantait,
      faisait rougir A1 ou A2, et un sabotage sans effet était compté « mord » (exemple mesuré par le relecteur du tour
      3, R24 : un sabotage qui ne change rien, délai d'un signal ramené à 2 s). Un seul « pas de verdict » suffit à
      rendre 2 : un contrôle qui n'a pas pu tourner ne rend pas un verdict (R-734). Le nom dans A1 : T3-5 du même
      superviseur — sous le sabotage Sf, la ligne rouge de A1 ne disait pas quel signal avait été refusé (c'était le
      RSI(2), vu à la main). Les signaux du dépôt ne sont pas LANCÉS dans un sabotage (tour t6) : la série éprouve les
      dents de l'épreuve, que portent ses propres modules ; C5 seul pesait 94 % d'un lancement (étude « 54 heures »), et
      Z0 joue le dépôt chaque soir.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨. Dans un sabotage, une règle qui ne serait défendue que par le VERDICT d'un
      signal du dépôt n'aurait plus de dent : au 06-11-2026, il n'y en a aucune (relevé du 05-11-2026 : seul Sf mordait
      par A1, et il mord désormais par X12). Le CODE de C5, lui, est encore exécuté dans un sabotage, par le tricheur
      `filtre_lendemain` (tour t7, m1). La ligne du verdict est cherchée parmi toutes les lignes
      du lancement, la dernière qui commence par « PASSE · » ou « REFUSÉ · » (la sortie d'erreur est mise APRÈS la
      sortie normale par `lancer`, un avertissement d'une bibliothèque y passerait sinon pour la dernière ligne).
    ⑩ EFFET — Écrit dans la copie ; lance un sous-processus par signal, le témoin compris.
    ⑪ TERMINAISON — Rend la main ; chaque sous-processus est borné. [sort: non]
    """
    # LES DÉLAIS sortent de la mesure versée (R-N1, tour t2) ; LES TRICHEURS DES 20 ANS se calculent sur les données de
    # la COPIE avant le dépôt des modules (lot N72)
    delais = delais_de_la_mesure(copie)
    B, lectures = lire_les_references(copie)
    des_donnees, preconditions = tricheurs_des_donnees(copie, B, lectures)
    modules = dict(MODULES_D_EPREUVE, **des_donnees)
    poser_les_modules_et_la_fiche(copie, modules)
    signaux, ineprouvables, ecartes = signaux_a_eprouver(copie)
    verdicts, sans_verdict, sorties = {}, [], {}
    du_depot = [sg for sg in signaux if not sg["module"].startswith("programmes/" + PREFIXE)]
    for sg in signaux:
        if not avec_le_depot and sg in du_depot:
            continue
        t_l = time.time()
        code, sortie = lancer(copie, os.path.join(copie, SOI), "--signal", copie, sg["module"], sg["fonction"],
                              sg["reglages"], delai=delais["un_signal"])
        t_l = time.time() - t_l
        # T3-3 : le verdict rendu est une propriété du lancement (son code ET sa ligne), jamais un message épelé
        ligne = verdict_du_lancement(code, sortie)
        if ligne is None:
            ligne = (sortie.strip().splitlines() or ["(aucune sortie)"])[-1]
            sans_verdict.append((sg["module"], sg["reglages"], code, ligne[:160]))
        verdicts[(sg["module"], sg["reglages"])] = (code, ligne)
        sorties[(sg["module"], sg["reglages"])] = sortie
        print("  signal %s · %s · réglages %s · %s · lancé en %.1f s\n      -> code %d · %s"
              % (sg["module"], sg["fonction"], sg["reglages"], ", ".join(sg["sources"]), t_l, code, ligne), flush=True)
        # LA MESURE PAR VALEUR SE FABRIQUE DEPUIS CE LANCEMENT (tour t7, R-728) : pour un signal du DÉPÔT, ses lignes
        # « VALEUR · » sont recopiées, précédées de son module ; avec la durée de chaque lancement, elles suffisent à
        # refaire tests/resultats/MESURE_DE_L_ARRIVEE_DES_SIGNAUX_PAR_VALEUR_*.tsv depuis la sortie d'un lancement normal
        # joué comme la certification le joue (sous la mesure de couverture)
        if sg in du_depot:
            for l in sortie.splitlines():
                if l.startswith("VALEUR · "):
                    print("  VALEUR · %s · %s" % (sg["module"], l[len("VALEUR · "):]), flush=True)
        # les lignes PASSE des autres fichiers (une par fichier, lot N72) : la durée de chacun se lit dans la sortie
        for autre in sortie.strip().splitlines():
            if autre.startswith("PASSE · ") and autre != ligne:
                print("         " + autre, flush=True)
    for e in ecartes:
        print("  fiche écartée (le juge refuse aussi son signal) : %s · %s" % e)
    for m in ineprouvables:
        print("  module déclaré INÉPROUVABLE : %s · %s" % m)
    res = []
    maitre = nom_du_maitre(copie, B)
    autres = [x[0] for x in lectures if x[0] != maitre]
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
    if not avec_le_depot:
        # un SABOTAGE (tour t6) : les signaux du dépôt n'ont pas été lancés ; A1 ne juge que ce qui ne demande aucun
        # lancement, et le DIT (Z0, qui les lance, juge le reste)
        vu = {"signaux du dépôt non lancés dans un sabotage (%d ; Z0 les joue)" % len(du_depot): True,
              "aucun module déclaré du dépôt inéprouvable %s" % ine_depot: not ine_depot}
    res.append(("A1 chaque signal du dépôt passe", all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())))
    # A2 à A5 les modules et la fiche d'épreuve
    vu2, vu3, vu5 = {}, {}, {}
    for nom, (texte, attendu) in modules.items():
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
    # R-734 : les tricheurs X5 et X6 n'ont de dents que si leur seuil dépasse FENETRE et qu'une valeur l'atteint ; le
    # maître est retrouvé par `le_maitre`, jamais par sa position (relecteur neuf du 06-11-2026, défaut connu n°1)
    _nom_m, _cours, _l_m = le_maitre(copie, B, lectures)
    longues = sum(1 for _s in _cours.values() if len(_s) >= SEUIL_DES_TRICHEURS_LONGS)
    vu3["seuil des tricheurs longs %d au-dessus de FENETRE %d et atteint par %d valeurs du maître (plus longue %d)"
        % (SEUIL_DES_TRICHEURS_LONGS, FENETRE, longues, max([len(_s) for _s in _cours.values()] or [0]))] = (
        SEUIL_DES_TRICHEURS_LONGS > FENETRE and longues > 0)
    # R-734 : les préconditions des tricheurs des 20 ans et de la mémoire, X7 à X12 (lot N72, tours t1 et t6),
    # calculées sur les données de la copie
    for texte_p, ok_p in preconditions.items():
        vu3["précondition " + texte_p] = ok_p
    # T3-5, dent permanente (superviseur R-759 du 05-11-2026, défaut 1, point 3) : chaque tricheur refusé est NOMMÉ
    # par `nommer_ce_qui_ne_passe_pas` — son module, ses réglages et le début de son verdict, dans un même texte
    tricheurs = [sg for sg in signaux if sg["module"].startswith("programmes/" + PREFIXE)
                 and modules.get(sg["module"][len("programmes/"):], ("", ""))[1] == "REFUSÉ"
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
    exemple_sans_verdict = ("programmes/MODULE_X.py", "{}", 124, "délai de %d s dépassé" % delais["un_signal"])
    exemple_temoin = (TEMOINS_SANS_VERDICT[0], "{}", 1, "MemoryError: plantage simulé") if TEMOINS_SANS_VERDICT else None
    vu6 = {"délai dépassé (124) avec une ligne « PASSE · » : aucun verdict": verdict_du_lancement(124, "PASSE · 40 valeurs") is None,
           "code 1 avec une trace Python : aucun verdict": verdict_du_lancement(1, "Traceback (most recent call last):\nRuntimeError: x") is None,
           "code 1 avec une ligne « REFUSÉ · » : verdict rendu": verdict_du_lancement(1, "REFUSÉ · ACCOR le 2025-05-23") is not None,
           "un cas réussi et un lancement sans verdict inattendu : code 2": code_des_cas([("x", True, "")], [exemple_sans_verdict]) == 2,
           "un cas réussi et le seul témoin sans verdict : code 0": exemple_temoin is not None and code_des_cas([("x", True, "")], [exemple_temoin]) == 0,
           "tous les cas réussis, chaque verdict rendu : code 0": code_des_cas([("x", True, "")], []) == 0}
    res.append(("A6 un lancement sans verdict n'est pas un verdict", all(vu6.values()),
                " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu6.items())))
    # A7 (lot N72) : une valeur de l'indice sans cours est NOMMÉE. ① Le BRANCHEMENT : le lancement de chaque module
    # honnête (attendu « PASSE ») a imprimé, pour chaque fichier de référence, la ligne que `dans_l_indice_sans_cours`
    # calcule ici. ② La FONCTION, sur un EXEMPLE CONSTRUIT : le maître privé de sa première valeur, elle la nomme.
    vu7 = {}
    for nom, (_t, attendu) in modules.items():
        if attendu != "PASSE":
            continue
        cle = ("programmes/" + nom, exemple_de_la_declaration(os.path.join(copie, "programmes", nom))[1])
        lues = [l for l in sorties.get(cle, "").splitlines() if l.startswith("DANS L'INDICE, SANS COURS DANS ")]
        for f, _c, _l, sans_cours in lectures:
            attendue = "DANS L'INDICE, SANS COURS DANS %s : %s" % (f, ", ".join(sans_cours) or "aucune")
            vu7["%s imprime « %s »" % (nom, attendue)] = lues.count(attendue) == 1
    _f0, cours0, lecture0 = le_maitre(copie, B, lectures)
    retiree = sorted(cours0)[0]
    lecteur = B.charger_module(os.path.join(copie, "programmes", "LIRE_LES_COURS.py"), "lecteur_unique")
    calcule = dans_l_indice_sans_cours(lecteur.lire_les_passages(copie),
                                       B.table_mnemoniques(B.trouver(copie, "REFERENTIEL_VALEURS")),
                                       {v: s for v, s in cours0.items() if v != retiree}, lecture0["seances"])
    vu7["exemple construit : le maître (%s) privé de %s, la fonction rend %s" % (_f0, retiree, calcule)] = retiree in calcule
    res.append(("A7 une valeur de l'indice sans cours est nommée", bool(vu7) and all(vu7.values()),
                " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu7.items())))
    # A8, A10 (lot N72, tour t2) : le chemin en dur, les délais tirés de la mesure ; A11 (tour t3) les arguments ;
    # A12 (tour t6) la mémoire déclarée. A9 (le visa) est retiré au tour t6.
    res.append(cas_du_chemin_en_dur(copie))
    res.append(cas_des_delais(copie, delais))
    res.append(cas_du_lancement_normal(copie))
    res.append(cas_de_la_memoire(copie, B, modules, verdicts, sorties, maitre, autres))
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
        try:
            _code, _ligne = eprouver_un_signal(os.path.abspath(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
        except ReferenceIntrouvable as _e:
            # R-734 : sans ses fichiers de référence, l'épreuve n'a pas pu tourner — code 2, ni vert ni refusé
            print("ARRÊT : %s" % _e)
            sys.exit(2)
        print(_ligne)
        sys.exit(_code)
    if len(sys.argv) in (3, 4) and sys.argv[1] == "--cas":
        if len(sys.argv) == 4 and sys.argv[3] != SANS_LE_DEPOT:
            print("ARRÊT : argument inconnu %r (attendu : %s)" % (sys.argv[3], SANS_LE_DEPOT))
            sys.exit(2)
        try:
            resultats, sans_verdict = cas(os.path.abspath(sys.argv[2]), avec_le_depot=len(sys.argv) == 3)
        except ReferenceIntrouvable as _e:
            print("ARRÊT : %s" % _e)
            sys.exit(2)
        for nom, ok, detail in resultats:
            print(("  ok    " if ok else "  ÉCHEC ") + nom + " — " + detail)
        # T3-3 : un signal sans verdict, c'est un contrôle qui n'a pas pu tourner (R-734) — code 2, ni vert ni mordu
        for module, reglages, code_s, ligne_s in sans_verdict:
            print("  PAS DE VERDICT : signal %s · réglages %s · code %d · %s" % (module, reglages, code_s, ligne_s))
        # LE MARQUEUR DE FIN : sans lui, une épreuve interrompue ne passe ni pour verte ni pour mordue
        print("FIN DES CAS : %d" % len(resultats))
        sys.exit(code_des_cas(resultats, sans_verdict))
    # LES ARGUMENTS, lus AVANT toute préparation (relecteur du tour t2, R2-2) : un argument inconnu ou en trop arrête en
    # code 2, en le nommant (l'option du samedi, retirée au tour t6, est désormais inconnue)
    _racine, _choix, _erreurs = lire_les_arguments(sys.argv[1:])
    if _erreurs:
        print("ARRÊT : %s" % " · ".join(_erreurs))
        sys.exit(2)
    if _racine is None:
        print(__doc__.split("① RÔLE")[0])
        sys.exit(2)
    DEPOT = os.path.abspath(_racine)
    try:
        DELAIS = delais_de_la_mesure(DEPOT)
    except (ReferenceIntrouvable, ValueError, KeyError) as _e:
        # R-734 : sans sa mesure, l'épreuve ne sait pas combien de temps donner : elle n'a pas pu tourner
        print("ARRÊT : la mesure par valeur ne se lit pas : %s" % _e)
        sys.exit(2)
    print("délais tirés de %s : un signal %d s, un lancement « --cas » %d s"
          % (DELAIS["mesure"], DELAIS["un_signal"], DELAIS["cas"]))
    # --saboter=<noms> : Z0 puis ces sabotages (le joueur de séries, par lots ; décision n°71) ; lu par
    # `lire_les_arguments` (BACKLOG A-599 ⑬ b : un lecteur commun des arguments manque au dépôt)
    _faute = False
    for sab in _choix:
        t0 = time.time()
        try:
            d, r = preparer(DEPOT, sab)
        except AssertionError as e:
            print("%s NE S'APPLIQUE PLUS : CIBLE INTROUVABLE — %s" % (sab, e))
            sys.exit(2)
        try:
            # un SABOTAGE ne lance pas les signaux du dépôt (tour t6) : Z0 les joue
            code, out = lancer(r, os.path.join(r, SOI), "--cas", r, *([] if sab == "Z0" else [SANS_LE_DEPOT]),
                               delai=DELAIS["cas"])
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
