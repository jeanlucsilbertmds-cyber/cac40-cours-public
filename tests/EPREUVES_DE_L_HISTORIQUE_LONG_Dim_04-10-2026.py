#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_HISTORIQUE_LONG — Dim 04-10-2026 (Paris)
Rôle : prouver que programmes/REPARER_L_HISTORIQUE_LONG.py répare juste et s'arrête quand il ne peut pas réparer
sûrement, et que programmes/CONTROLER_L_HISTORIQUE_LONG.py refuse chaque défaut qu'il doit refuser ; et que chaque
épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche l'un de ces deux programmes (R-731).

À QUOI ÇA SERT. L'historique long réparé servira, après décision de Jean-Luc, à juger les stratégies sur 26 ans. Une
réparation fausse ne se voit pas : un cours reconstruit avec le mauvais facteur reste un cours plausible. Ces
épreuves travaillent sur de VRAIES données : un extrait de janvier à octobre 2005 du fichier Yahoo déposé et de
l'extrait bnains (tests/temoins_historique_long/), le vrai donnees/sources_yahoo/evenements.json, et, pour le
calibrage, les vrais fichiers entiers du dépôt. Les défauts sont FABRIQUÉS sur des copies de ces vraies données.

LES ÉPREUVES DU CONTRÔLE :
H1  sur l'extrait Yahoo 2005 : refus par K5 (AXA 2005, barres plates), K8 (AXA 2005, écarts) et K9 (ENGIE, les cours
    de Suez) ; code 1 ;
H8  ecarts() : une clôture bnains augmentée de 5 % un jour donne un écart d'environ −4,8 % ce jour-là et moins de
    0,05 % les autres jours ; moins de MINIMUM séances communes ne donnent aucun écart ; une série vide n'a pas de
    séance manquante ;
H7  jours_douteux() : EXACTEMENT 5 valeurs en écart le même jour font un jour douteux, 4 non ; une séance manquante ce jour-là
    n'est pas comblée et le contrôle la range en K7 — quand Francfort se tait ; quand Francfort confirme la barre de
    bnains (la vraie cotation d'Air Liquide du 16-05-2005), elle est comblée ;
H9  K1 (une ligne en double), K2 (plus haut sous la clôture), K3 (volume nul), K4 (un samedi), K10 (une clôture
    Yahoo multipliée par 1,4 un jour : saut contredit par bnains) refusent ; K10b nomme un saut que bnains ne peut
    pas vérifier sans refuser ;
H10 facteur_local() : un changement de facteur à côté de la séance → pas sûr (None) ; loin → le facteur ; des lignes
    déjà venues de bnains ne comptent pas comme voisines ; des voisins d'un seul côté → None ; des voisins à plus
    de 45 jours → None ; controler() range la première en K7, pas en K6 ;
H16 barre_utilisable() : barre incohérente → non ; volume nul → non ; barre saine → oui ;
H11 divisions() sur le vrai evenements.json : AXA le 15-05-2001 → 4, le 16-05-2001 → 1 ;
H18 « nan » en volume et « inf » en clôture → K1 (ligne illisible) ; une barre à zéro → K2 et code 1, pas 2 ;
H20 K11 : 10 séances manquantes de suite dans une série → refus, 9 → non ; K12 : une série coupée au 01-09-2005 →
    refus ; K13 : une valeur retirée entière → refus ; K14 : une série amputée de ses deux premiers mois → signalée ;
H21 calendrier : une séance où le fichier n'a AUCUNE ligne (le 10-03-2005, retiré du fichier d'essai) reste une
    séance, parce que le calendrier officiel le dit, et la réparation y comble chaque valeur que bnains porte, ou
    écrit au journal pourquoi elle ne la comble pas (27-10-2026 : les cinq demi-séances, où Yahoo n'a aucune ligne,
    étaient tues par l'ancien calendrier, tiré des cours) ;
H63 la trace (27-10-2026, décision de Jean-Luc : « toute la mécanique de trace ») : après la réparation, chaque séance
    encore manquante a sa ligne « non comblé » au journal, et le registre de provenance porte l'empreinte du fichier
    réparé et du journal écrits ;
H22 la couture d'AXA, sur les vraies lignes de 2008-2009, au jour de détachement OFFICIEL (10-11-2009, communiqué
    d'AXA du 09-11-2009) : la fenêtre déclarée finit le 09-11-2009 et K15 ne trouve rien ; finie le 10-11-2009 (la
    fin retenue du 04 au 06-10-2026), K15 refuse la marche nulle du jour de détachement, où le droit permet +2,5 %, et
    la marche de +2,3 % du lendemain ; sans les jours de détachement, K15 refuserait aussi la couture juste du
    10-11-2009 ; une ligne reconstruite décalée de 3 % entre deux autres lignes reconstruites est refusée aussi ; la
    fenêtre reconstruite × 0,95 (relecture de Cowork du 04-10-2026, 21h54) est refusée à ses deux coutures, dont le
    10-11-2009 : marche +7,7 %, le droit n'en permet que +2,5 % (l'épreuve fait commencer la fenêtre en juin 2008) ;
H23 recaler aux jours de détachement OFFICIELS (relecture du Chat du 07-10-2026), sur les vraies lignes de 2007 à
    2010 de Crédit Agricole, Danone, Michelin, Pernod Ricard, Société Générale et Veolia : seule la séance du
    20-02-2008 de Société Générale est recalée, à 63.5677 (Yahoo y ajuste la veille du détachement du 21-02-2008) ;
    Danone, Michelin et Pernod Ricard, recalés à tort du 04 au 06-10-2026, ne le sont plus ; les barres bnains
    prouvées fausses ôtées, K15 ne trouve plus rien — il refusait Société Générale en octobre 2009 tant qu'on les
    laissait (Yahoo y est juste, bnains faux du 14-09 au 07-10-2009) ; SANS le recalage, K15 refuse les deux marches
    de février 2008, et rien d'autre ; une veille fabriquée chez Danone (29-05-2009 ÷ 1,06)
    est recalée à 33,15 ; un écart fabriqué chez Société Générale le 07-10-2009 n'est PAS recalé (sa barre bnains est
    fausse) ; chez Michelin, la marche du 30-09-2010 annulée et un écart fabriqué le 28 : le 28 n'est PAS recalé, la marche
    totale n'étant pas celle du droit ; une barre bnains sans volume le 20-02-2008 empêche le recalage, et K15 refuse ;
H25 lire_detachements() : un droit sans jour officiel → manque nommé ; un jour officiel 16 jours avant la première
    cotation, ou après elle → « impossible » ; K16 ne refuse que les valeurs du fichier (ni Michelin, absent du
    fichier d'épreuve, ni Suez) ; marche_permise() sans barre bnains, ou à clôture nulle → 0, avec la vraie → +2,47 % pour AXA ;
    un droit absent de bnains, AXA juin 2006, se calcule avec les chiffres du document → +1,95 % ; sans ses chiffres → manque nommé ;
    un chiffre illisible (« 24,47 ») → ValueError ;
H26 reconstruire() sur les vraies lignes d'AXA de 2006 (le facteur lu au journal est l'appliqué, f / a / s ; s = 1 pour AXA après
2006) : le facteur d'avant le 19-06-2006 est celui d'après ÷ 1,0195, et K15 ne
    trouve rien en juin 2006 ; sans les détachements, le facteur est unique et K15 refuse la marche nulle du 19-06-2006 ;
H27 le fichier réparé du dépôt face aux cours extrêmes mensuels des rapports annuels (AXA 2005-2007, Essilor 2000-2001) :
    rapport constant à moins de 1 % près sur les 40 chiffres d'AXA (0,9771) et les 24 de chaque année d'Essilor ;
H28 oter_les_barres_fausses() sur les vraies lignes : Société Générale perd ses 18 barres du 14-09 au 07-10-2009 et garde
    le 11-09 et le 08-10, TotalEnergies ses 90 barres du 16-08 au 20-12-2016, rien d'autre ; un en-tête faux, une
    fenêtre qui finit avant de commencer, une date illisible → ValueError ; K9 compte les 90 lignes de TotalEnergies
    sans barre bnains, et ne les compte plus quand on lui dit qu'elles sont fausses ;
H29 ajuster() sur les vraies lignes 2006-2021 d'Air Liquide, BNP Paribas, Michelin, Société Générale et Euronext : deux
    droits ajustés, BNP Paribas 2009 et Société Générale 2006 ; la clôture du 29-09-2009 divisée par 1 + 2,89 %, son
    volume multiplié d'autant, celle du 30-09-2009 intacte ; Michelin et Air Liquide, que Yahoo ajuste, intacts ;
    Euronext 2021 non mesurable ; K15 refusait la marche nulle de BNP Paribas au 30-09-2009 avant, plus après ;
H30 K15 et un détachement qui n'est pas une séance comparable (Air Liquide, 14-09-2016, barre bnains fausse) : la marche
    du 31-05 au 15-09-2016 est permise ; sans les détachements, elle est signalée (+2,7 %) ;
H31 le fichier réparé du dépôt : tous les contrôles l'acceptent (code 0, « aucun contrôle bloquant n'a rien trouvé »),
    K23 compris depuis le 24-10-2026, quand sa chaîne a été remontée jusqu'à ses sources (du 13 au 24-10-2026, K23 seul
    le refusait, A-578) ; il retrouve la clôture officielle de Société Générale du
    05-10-2009 (52,20 €, à 0,2 % près), celle de BNP Paribas du 28-09-2009 (56,57 €, à 0,05 % près) et la moyenne
    officielle des ouvertures de TotalEnergies du 17-11 au 14-12-2016 (44,72 €, à 0,2 % près) ;
H32 la réparation entière, lancée sur une copie des vrais fichiers, rend code 0, ajuste douze droits et en défait trois
    (« ajustés : 12 », « défaits : 3 », le 09-10-2026), et refait À L'OCTET
    le fichier réparé et le journal du dépôt ; K1 à K22 acceptent le résultat, K23 seul le refuse. Depuis le 27-10-2026,
    la copie porte le carnet de provenance `donnees/PROVENANCE_DES_FICHIERS.csv` (la réparation y inscrit ses deux
    fichiers) et le calendrier d'Euronext : K23 la refuse parce qu'elle ne porte pas les programmes qui produisent ses
    fichiers (« qui n'est pas un programme du dépôt ») ; avant, parce qu'elle ne portait pas le carnet (13-10-2026) ;
H33 facteur_local() la veille d'un détachement officiel (Crédit Agricole, 03-01-2007, absent de Yahoo) : sans les jours
    officiels, pas sûr (None) ; avec eux, le facteur d'avant, 0,9090 ; le surlendemain, celui d'après, 0,9227 ; loin du
    détachement, le facteur ordinaire ;
H34 la troisième source, sur les vraies lignes de septembre 2011 : BNP Paribas et Société Générale du 13-09-2011 sont
    « fausse » (Yahoo 27,15 et 17,41 ; bnains 28,00 et 17,90 ; Francfort 27,995 et 17,99) ; sans Francfort, « Francfort
    muet » ; Carrefour, 05-07-2007, jour douteux : la barre bnains est sûre parce que Francfort la confirme, et ne l'est
    pas sans lui ; un cours de Francfort qui répète la veille ne donne aucun avis ;
H35 trancher() sur les mêmes lignes : les deux clôtures du 13-09-2011 remplacées par celles de Paris (28,00 et 17,90, à 0,2 %
    près), venues de bnains ; K17 les refusait avant, ne trouve plus rien après ;
H36 arbitre_de_l_indice() sur les vraies lignes de toutes les valeurs, novembre 2009 à février 2012 : le 07-05-2010 et la
    suite des 15 séances du 29-08 au 16-09-2011 (07-09-2011 compris, où bnains n'a pas l'indice) donnent tort au
    fichier Yahoo, marge de plus de 5 ; lire_indice() écarte le 19-06-2001 (bnains et Yahoo à 0,56 % l'un de
    l'autre) et le 07-09-2011, garde le 08-09-2011 ; resoudre() retrouve (1, 2, 3) sur un système dont le premier
    pivot est nul ;
H37 corriger() sur les vraies lignes de septembre 2011 : les clôtures de BNP Paribas du 12, du 13 et du 14-09-2011
    remplacées par celles de Paris (26,12, 28,00, 26,90, à 0,2 % près) ; Hermès du 14-09-2011 gardé (barre bnains plate
    sans volume) ; trancher() seul, comme au neuvième tour, rend le rendement de BNP Paribas du 12 au 13-09-2011 plus
    faux et K18 le trouve, et ses passages successifs (47, 8 puis 2 lignes « fausse ») n'en laissent aucune ; après
    corriger(), K18 et K19 ne trouvent rien ; sur le fichier Yahoo d'origine, K19 refuse la seule suite du 29-08 au
    16-09-2011 ;
H38 rendements_degrades() sur trois séances fabriquées : une ligne remplacée qui rend le rendement avec sa voisine plus
    faux de près d'un point est trouvée ; une voisine dont la barre bnains est plate et sans volume n'est pas un cours
    de Paris et ne juge rien (prise pour Paris, elle ferait paraître le rendement réparé plus faux d'un point) ; le
    contrôle du fichier Yahoo de l'extrait tourne (code 0 ou 1) avec l'indice, et rend 2 en le nommant sans lui
    (R-734) ; corriger() sur trois séances, où le facteur du jour ne se mesure pas, ne touche à rien ;
H39 défaire les deux erreurs de Yahoo (décision de Jean-Luc du 08-10-2026, « S'il y a des erreurs, il faut les
    corriger ») : lire_a_defaire() rend exactement 1/0,704727 pour Accor au 02-07-2010 (ajouté le 09-10-2026), 27/26
    pour Crédit Agricole au 22-05-2018 et 184,07/180,12 pour EssilorLuxottica au 06-05-2024 ; sans_les_divisions_fausses() ôte la seule division du 22-05-2018 de Crédit
    Agricole et rien d'autre ; defaire() sur les vraies lignes de mai 2018 multiplie les 6 séances d'avant le 22 (du 14 au 21) par
    27/26, divise leur volume, ne touche pas les suivantes ; K20 accepte le résultat et refuse, ligne par ligne :
    les 6 lignes d'origine, les 6 lignes aux prix corrigés mais au volume d'origine, les 8 lignes d'après le 22
    corrigées à tort (le mauvais côté), les 3 lignes laissées dans une correction faite une ligne sur deux, les 6
    lignes dont seule la clôture est corrigée (les trois cassures de la relecture indépendante du 08-10-2026) ; un
    facteur « 27:26 », négatif, « nan/1 », « inf/1 », en double, une date « 20180522 » ou un en-tête faux font lever
    ValueError ;
H24 autour_du_detachement() : au milieu d'une série → l'ancrage et les 5 séances d'avant ; quand la série commence
    dans la fenêtre → pas d'ancrage (None) et les séances qui existent ; un jour absent → (None, []) ;
H17 CALIBRAGE sur les vrais fichiers entiers du dépôt : passé sur le fichier Yahoo déposé, le contrôle retrouve les
    barres plates d'AXA de Cowork année par année (22, 49, 122, 173, 153, 124, 92), ses 150 740 séances communes moins
    la séance d'Hermès du 21-10-2004, que le lecteur écarte comme conflit, et, sur le calendrier officiel (depuis le
    27-10-2026), 530 séances manquantes : les 222 de Cowork aux séances où au moins 25 valeurs ont une ligne, 181 aux
    cinq demi-séances des 24 et 31-12-2010, 24 et 31-12-2012 et 31-12-2015, le reste aux séances de 2000 et 2001 où
    Yahoo cote peu de valeurs.
LES ÉPREUVES DE LA RÉPARATION :
H2  sur l'extrait 2005, fenêtre EssilorLuxottica de janvier-février, référence mars-octobre (Yahoo y est juste) :
    code 0 ; chaque clôture reconstruite est à moins de 0,2 % de la clôture Yahoo d'origine, et vient de bnains sauf
    les jours gardés (bnains n'a pas la séance, Yahoo juste autour) ; ENGIE n'a plus de
    ligne avant le 08-07-2005 et garde celle du 08-07-2005 ; des séances réelles manquantes sont comblées, venues de
    bnains ; le contrôle sur le résultat ne refuse plus ni K6 ni K9 ;
H4  une vraie ligne Yahoo retirée (TotalEnergies, 15-03-2005) est comblée à moins de 0,3 % de sa clôture d'origine ;
    un ajustement fabriqué la veille d'une séance retirée (Vinci, cours d'avant le 15-06-2005 × 0,97) la laisse
    « non comblé » ;
H5  fenêtre AXA dont la référence est en 2005, où Yahoo est faux → code 1, raison nommée, AUCUN fichier écrit ;
H6  le témoin Suez multiplié par 1,1 chez bnains → code 1, « pas prouvées », aucun fichier écrit ;
H19 un fichier déjà débarrassé des lignes d'Engie d'avant le 08-07-2005 : rien à retirer, code 0 ;
H15 dans la fenêtre EssilorLuxottica, un jour sans barre bnains est GARDÉ quand Yahoo est juste autour, et RETIRÉ
    quand Yahoo est faux autour — retiré, il reste manquant, et le journal le dit aussi (« non comblé », 27-10-2026) ; un jour où Yahoo n'a rien et bnains une barre sans volume reste manquant, le journal
    le dit (« non comblé », depuis le 27-10-2026) et le contrôle dit pourquoi ;
H12 texte() : 33.80 → « 33.8 », 902383.0 → « 902383 » ;
H13 lignes de commande : sans argument → 2 (les deux) ; fichier absent → 2 (les deux) ; colonne volume absente → 2
    (contrôle) ; fichier des droits, ou des jours officiels, à l'en-tête faux → 2 (contrôle) ; extrait bnains au défaut
    de lecture → 2 (contrôle) ; fichier Yahoo à ligne en double → 2 (réparation) ; erreur imprévue → 2 (les deux) ;
H14 le fichier maître des cours et le fichier Yahoo déposé ne changent pas d'un octet.
Z0 charge les VRAIS fichiers des deux programmes ; les sabotages se jouent sur des copies.
LES SABOTAGES (avec --saboter) — contrôle : T1 médiane remplacée par la moyenne · T2 jour douteux à plus de 5 et non
5 · T3 jours douteux ignorés par barre_utilisable · T4 barre incohérente acceptée · T5 facteur local ignoré par K6 ·
T6 K9 muet · T7 K10 muet · T8 séances manquantes hors de la série comptées · T9 doublons non vus · T10 division
comptée le jour même · T11 lignes venues de bnains prises pour voisines · T12 colonne manquante acceptée · T13 écart
calculé sur moins de MINIMUM points · T14 série vide parcourue · T15 calendrier sans bnains · T16 « nan » et « inf »
acceptés · T17 clôture nulle divisée · T18 voisins d'un seul côté acceptés · T19 voisins lointains acceptés · T20 K11
muet · T21 K12 muet · T22 K13 muet · T23 K15 muet · T24 jours de détachement ignorés · T25 marches entre deux lignes de bnains ignorées · T26 marche du jour de
détachement sans borne · T27 fenêtre réduite à la veille (la version du 04-10-2026) · T28 fenêtre du
détachement non surveillée par K15 · T29 ancrage pris hors de la série · T30 K16 muet · T31 jour officiel
impossible accepté · T32 premier jour de cotation chez bnains pris pour le détachement (l'erreur du 04 au
06-10-2026) · T33 barre bnains à clôture nulle divisée · T34 cours théorique ex-droit mal calculé · T35 lignes officielles
sans droit chez bnains ignorées · T36 barres fausses gardées · T37 K9 compte les barres fausses · T38 détachement vu le
jour d'arrivée seulement · T39 fenêtre à l'envers acceptée · T40 côté coupé par un détachement refusé · T41 voisins pris
des deux côtés d'un détachement · T42 tolérance de Francfort décuplée · T43 barre d'un jour douteux jamais sûre · T44 cours
répété pris pour un avis · T45 K17 muet · T46 toute couture contre une ligne de Yahoo excusée. Réparation : U1 référence instable acceptée
· U2 témoin non vérifié · U3 jour Yahoo jamais gardé · U4 séance du 08-07-2005 retirée · U5 jours douteux comblés ·
U6 fichiers écrits malgré un arrêt · U7 nombres entiers écrits avec « .0 » · U8 jour absent de Yahoo et inutilisable
chez bnains « retiré » quand même · U9 séance comblée avec un facteur incertain · U10 rien à retirer refusé ·
U11 fenêtre d'AXA finie le 10-11-2009 · U12 marche de la fenêtre non confrontée au droit · U13 toute la fenêtre
recalée, même les séances justes · U14 fenêtre ramenée au facteur du jour de détachement · U15 fenêtre recalée en
partie quand une barre bnains manque · U16 facteur de reconstruction jamais divisé aux détachements · U17 jour du
détachement divisé lui aussi · U18 ajuster n'ajuste jamais · U19 ajuster divise aussi le jour du détachement · U20 volume
non ajusté · U21 détachement absent des séances comparables pris pour non mesurable · U22 barres fausses gardées par la
réparation · U23 trancher ne remplace rien · U24 un seul passage · U25 reconstruction sans Francfort · U26 comblement sans
Francfort. · T55 K20 muet · T56 aucune division fausse ôtée · T57 K20 ne regarde que la clôture · T58 deux lignes pour
le même ajustement acceptées · T59 date non exigée en AAAA-MM-JJ · T60 facteur non fini accepté · T61 K20 ne regarde
pas après la date · T62 K20 compare aussi les lignes venues de bnains · U32 defaire ne touche rien · U33 defaire touche aussi le jour de la date · U34 volume
non divisé par defaire. · T63 distribution sans marche · T64 colonne de la valeur distribuée ignorée · T65 K18 sans les
détachements · T66 ligne de distribution ambiguë acceptée · U35 barre écartée sur décision gardée. · T67 deux opérations un même jour acceptées · T68 document impossible accepté · T69 K18
tolère la marche entière · T70 doublon de libellé accepté · U36 barre écartée non comblée écrite.
H40 les opérations omises par Yahoo lues dans les vrais fichiers, facteurs officiels · H41 une ligne de distribution
ambiguë ou impossible refusée · H42 K18 juge un jour de détachement droit compris · H43 une barre de Yahoo écartée
sur décision est comblée par la barre de Paris · H44 deux opérations un même jour, un doublon, un document impossible
refusés · H45 K18 voit une dégradation un jour de détachement omis par Yahoo · H46 une barre écartée non comblée
arrête la réparation · H47 K21 juge le jour des opérations déclarées sur les vrais cours : la vraie table passe,
les 120 décalages de ±1 à ±3 séances gardent leurs verdicts mesurés (35 refusés, 82 signalés, 3 acceptés ; 114, 29, 82, 3
avant Accor 2010, ajoutée le 09-10-2026 à 21h00, dont les 6 décalages sont refusés),
Carrefour décalé d'une séance ou un dimanche est refusé, un jour « 20110705 » aussi ; K21b bloque, AXA 2003
acceptée par décision de Jean-Luc (JOURS_ACCEPTES) passe en K21c ; une exception sans opération, en double ou
sans emploi est refusée, et une opération acceptée que la mesure contredit reste refusée par K21. Les sabotages
T71 à T90 portent sur K21, K21b et K21c (le contrôle des opérations déclarées). · H48 jour_ecrit lit le jour
dans la phrase citée, pas un jour voisin ni une date hors des « » · H49 un extrait bnains vide arrête le contrôle ·
H50 K20 juge une correction défaite remplacée le même jour par une opération déclarée, « document » ou « distribution »,
et refuse le même fichier si l'opération est déclarée un autre jour ou n'est pas posée. · H51 (10-10-2026) K21 ramène
les rendements de bnains par les divisions de Yahoo : Sagem, 10-07-2000, division par 3 et action gratuite pour cinq le
même jour, contredite sans elles, confirmée avec ; tous les contrôles passent le fichier, K23 compris depuis le 24-10-2026
(du 13 au 24-10-2026, K23 seul le refusait) (sabotages T93, T94). · H52 et H53
(10-10-2026, décision de Jean-Luc à 09h39 : la règle officielle) : la lecture prend les chiffres du document pour un droit
vu chez bnains, ajoute le dividende non attaché, le refuse sur une distribution, lit « du 10 au 23 novembre 2009 » ;
`aligner` ramène quatre droits de Yahoo à la règle officielle et seulement eux (sabotages T95 à T97, U37 à U39) · H54
K20 attend le facteur que le journal écrit pour une ligne alignée (T98, T99) · H55 K22 : chaque opération déclarée porte la
règle officielle à 0,05 % près dans le fichier, le premier jet faux de Vinci 2006 est refusé (T100, T101).
H56 à H59 (13-10-2026, A-578 ; demande de Jean-Luc à 09h34, « Tu ne vas pas oublier de le faire pour notre historique
des 20 ans », et décision « Les deux, dans l'ordre ») — K23, le verrou. Depuis le 18-10-2026 (le journal écrit ses
facteurs complets et son départ ; décision de Jean-Luc du même jour à 20h41 : égalité exacte ; superviseurs R-759 et
relecture du même jour), K23 REJOUE le journal (`lignes_non_rejouees`), avec les calculs mêmes de la réparation
(`appliquer`, `arrondir`) : H56 sur les vrais fichiers, le fichier réparé du dépôt se refait en entier, et chacun des
26 abîmes d'une vraie ligne est vu, seul, et PAR LE CONTRÔLE QU'IL GARDE (la ligne et le motif) — Hermès 14-02-2025,
ouverture + 0,01 € puis + 0,0001 €, colonne source « bnains » ou « Yahoo », ligne retirée du fichier ; Total
12-05-2006, volume + 1 000 puis + 1 ; Michelin 16-09-2011, plus bas + 0,0001 € (un arrondi à mi-chemin, qu'une
tolérance laissait passer) ; Air Liquide 04-01-2000 (comblé), ouverture + 0,00004 €, volume + 0,4, source « yahoo »,
départ « Paris », facteur de volume 0, clôture avant écrite, ligne retirée du fichier ; Accor 16-03-2000, clôture
× 1,001 ; Accor 03-01-2000, départ « Ligne », facteur infini, clôture avant fausse, deux gestes inversés, le second
supprimé ou doublé, un « corrigé » inventé ; Air Liquide 27-04-2012 bâtie sur une barre de Paris prouvée fausse
(B1 ; le Paris de l'épreuve est celui de `lire_paris`, le même que celui de la réparation) ; un « gardé » d'AXA (13-10-2008) qui ment sur sa clôture ; Engie
03-01-2000, retirée au journal et remise au fichier · H57 sur des cas fabriqués : une chaîne juste passe (geste depuis
Yahoo, ligne comblée depuis Paris, « gardé » à 1 et 1) ; dix-neuf règles cassées une à une sont vues, chacune par son
motif ; un journal à l'en-tête faux, ou portant « inf » ou « nan », est refusé · H58 la provenance : registre absent,
chaîne juste jusqu'à un téléchargement (chemins avec « \ » et « ./ » compris), empreinte fausse ou inscrite deux
fois, téléchargement sans adresse http(s) ou sans empreinte, programme absent ou qui n'est pas un programme, aucun
fichier lu, un dossier lu, fichier absent qui n'est pas un téléchargement, boucle, boucle sans téléchargement, en-tête
faux · H59 de bout en bout par `main` sur l'extrait 2005 : registre juste, K23 se tait ; une clôture retouchée, K23 la
voit ; registre retiré, K23 le dit (relecture indépendante du 13-10-2026 : sans H59, couper K23 dans `main` ne
faisait rougir aucune épreuve) · H61 : le fichier Yahoo d'origine avec une ligne en double, le contrôle s'arrête
(code 2) au lieu de rejouer sur une base fausse · H62 (19-10-2026, décisions de Jean-Luc de 07h05, « écrit à la main », et de 08h23, une colonne `fichiers_cites` à
part) : un fichier bâti sur une vraie ligne de BARRES_BNAINS_FAUSSES.csv (Société Générale, 2009) passe ; sans preuve,
avec des fichiers lus, avec une adresse, `lu` absolu, sans la colonne des fichiers cités, une seule colonne, une
citation vide, une adresse précédée de texte, un chemin dans `source`, une adresse sans nom d'hôte, ni adresse ni
fichier, un fichier cité absolu, par « .. », lien symbolique, dossier, absent, qui ne se remonte pas, un fichier sans
ligne, illisible, absent du dépôt, le fichier réparé inscrit « à la main » sont vus par leur motif ; les formes
« inscrit » et « qui revient » (chemin absolu, « .. », lien, dossier, lettre de lecteur) font basculer le verdict ;
un fichier cité absent est refusé même inscrit comme téléchargement ; une SECONDE ligne fausse et un SECOND morceau
faux (dans `source`, `fichiers_cites` et `lu`) sont vus (relecteur n° 2 du 19-10-2026, M1) ; le parent d'un fichier
cité qui ne se remonte pas le dit ; sur les vrais
fichiers, les trois fichiers écrits à la main citent leurs sources, et le fichier Yahoo nettoyé ne passerait pas « à la
main » ; le référentiel passe depuis qu'il porte ses trois colonnes de preuve (décision de Jean-Luc du 24-10-2026 à
16h06 ; superviseur R-759 du même jour : il reste un témoin réel, d'un fichier écrit à la main qui passe).
Sabotages T102 à T172 (T142 à T172, le 19-10-2026 : chacune des conditions de H62, l'ordre de la garde des fichiers
réparés, et la forme d'une adresse ; T159 : le refus d'un dossier dans `chemin_du_depot`, qui ne mord au verdict que
par le cas « lu : dossier inscrit » (pour un fichier cité, un dossier est refusé de toute façon par le refus d'un
fichier absent : T159 n'y change que le message — relecteur n° 3 et superviseur n° 5 du 19-10-2026, N4) ; T155 et T157 remplacent la vérification du chemin par le seul `_chemin`, au lieu
d'ôter le `if defaut`, qui faisait planter K23 au lieu de le faire passer (sonde du 19-10-2026) ; T160 à T166 :
une vérification faite sur la première ligne ou le premier morceau seulement (relecteur n° 2 du 19-10-2026, M1 :
« « ligne par ligne » n'est éprouvé nulle part ») ; T167 : le refus d'un fichier cité absent du dépôt (décision de
Jean-Luc du 19-10-2026, « 1 » à « Oui, le refuser ») ; T168 : le faux rendu quand un fichier cité ne se remonte pas (le
message du parent seulement) ; T169 : le seul refus de la lettre de lecteur ; T170 à T172 : une vérification faite
sur la dernière ligne ou le dernier morceau seulement (relecteur n° 3 du 19-10-2026, N2 et N3) ; T107, T122, T148 à T151 réécrits sur la colonne `fichiers_cites`) ; réécrits le 18-10-2026 sur le rejeu : T102 à
T105, T109, T112, T114, T116, T119 à T121, T129 à T131 (T131 : l'arrondi de Paris remplacé par `appliquer`, au lieu
de « tolérance propagée », qui n'existe plus) ; ajoutés : T132 à T139 (origine abîmée, retrait, présence dans l'autre
sens, clés de l'origine et du journal dans la boucle, vocabulaire des gestes, nombres finis du journal, clôture après
sur un retrait), puis T140 (le Paris de `lire_paris` d'avant le retrait des barres fausses) et T141 (un geste
qui part de la ligne ou de Paris sans écrire sa clôture après ou ses facteurs — il mord par une exception : sans ce
contrôle, le cas fabriqué fait planter la lecture du nombre ; `main` sortirait alors en code 2) ; T114 et T139 réécrits
après le superviseur n° 3 ; U9, U19, U20, U22, U25, U34 suivis sur la nouvelle écriture de la réparation (même sens).

USAGE : python3 tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py <racine du dépôt> [--saboter | --saboter=S1,S2…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si
un sabotage ne s'applique plus (son texte cible a disparu du programme).
"""
import contextlib, csv, hashlib, importlib.util, io, json, os, shutil, statistics, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROGRAMMES = os.path.join(RACINE, "programmes")
CONTROLE = os.path.join(PROGRAMMES, "CONTROLER_L_HISTORIQUE_LONG.py")
REPARATION = os.path.join(PROGRAMMES, "REPARER_L_HISTORIQUE_LONG.py")
TEMOINS = os.path.join(RACINE, "tests", "temoins_historique_long")
EVENEMENTS = os.path.join(RACINE, "donnees", "sources_yahoo", "evenements.json")
DROITS = os.path.join(RACINE, "donnees", "sources_bnains", "DROITS_BNAINS.csv")
OFFICIELS = os.path.join(RACINE, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv")
FAUSSES = os.path.join(RACINE, "donnees", "sources_bnains", "BARRES_BNAINS_FAUSSES.csv")
FRANCFORT = os.path.join(RACINE, "donnees", "sources_francfort", "COURS_DE_FRANCFORT.csv")
INDICE = os.path.join(RACINE, "donnees", "sources_indice", "INDICE_CAC40.csv")
RAPPORTS = os.path.join(RACINE, "donnees", "sources_rapports_annuels", "COURS_MENSUELS_DES_RAPPORTS_ANNUELS.csv")
REPARE = os.path.join(RACINE, "donnees", "sources_yahoo", "historique_long_repare.csv")
VERDICTS = os.path.join(RACINE, "donnees", "sources_yahoo", "AJUSTEMENTS_DE_YAHOO.csv")
EURONEXT = os.path.join(RACINE, "donnees", "CALENDRIER_EURONEXT.csv")
PROVENANCE = os.path.join(RACINE, "donnees", "PROVENANCE_DES_FICHIERS.csv")
DEMI_SEANCES = ("2010-12-24", "2010-12-31", "2012-12-24", "2012-12-31", "2015-12-31")
_sp = importlib.util.spec_from_file_location("CALENDRIER_DE_LA_BOURSE", os.path.join(PROGRAMMES, "CALENDRIER_DE_LA_BOURSE.py"))
CAL = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(CAL)
# LE CALENDRIER OFFICIEL DU DÉPÔT, lu une fois : depuis le 27-10-2026, le contrôle et la réparation le reçoivent en argument
# au lieu de calculer les séances depuis les cours (A-555 (b), décision de Jean-Luc du 27-10-2026).
SEANCES = CAL.lire_les_seances(RACINE)


def cal_(f):
    """Rend la fonction `f` du contrôle ou de la réparation, avec le calendrier officiel en argument `seances`."""
    return lambda *a, **k: f(*a, seances=SEANCES, **k)
_AXA_REEL = {}
_REEL = {}


def reel(valeurs, du, au):
    """Les vraies lignes Yahoo et bnains de quelques valeurs entre deux dates, lues une fois (sans le programme éprouvé)."""
    cle = (tuple(valeurs), du, au)
    if cle not in _REEL:
        y, b = {}, {}
        for dest, chemin, cols in ((y, os.path.join(RACINE, "donnees", "sources_yahoo", "yahoo_ohlcv_propre.csv"), 2),
                                   (b, os.path.join(RACINE, "donnees", "sources_bnains", "bnains_cac40.csv"), 4)):
            for l in csv.reader(open(chemin, encoding="utf-8")):
                if l[0] in valeurs and du <= l[1] <= au:
                    dest.setdefault(l[0], {})[l[1]] = tuple(float(x) for x in l[cols:cols + 5])
        _REEL[cle] = (y, b)
    y, b = _REEL[cle]
    return {v: dict(x) for v, x in y.items()}, {v: dict(x) for v, x in b.items()}


def axa_reel():
    """Les vraies lignes d'AXA de 2008 à 2009, Yahoo et bnains, lues une fois (sans le programme éprouvé)."""
    if not _AXA_REEL:
        for nom, chemin, cols in (("yahoo", os.path.join(RACINE, "donnees", "sources_yahoo", "yahoo_ohlcv_propre.csv"), 2),
                                  ("bnains", os.path.join(RACINE, "donnees", "sources_bnains", "bnains_cac40.csv"), 4)):
            _AXA_REEL[nom] = {l[1]: tuple(float(x) for x in l[cols:cols + 5])
                              for l in csv.reader(open(chemin, encoding="utf-8"))
                              if l[0] == "AXA" and "2008-01-01" <= l[1] <= "2009-12-31"}
    return dict(_AXA_REEL["yahoo"]), dict(_AXA_REEL["bnains"])
FENETRE_EL = (("ESSILORLUXOTTICA", "2005-01-01", "2005-02-28", "2005-03-01", "2005-10-31", "épreuve"),)

SABOTAGES = {
    "T1": (CONTROLE, "med = fen[m // 2] if m % 2 else (fen[m // 2 - 1] + fen[m // 2]) / 2", "med = sum(fen) / m"),
    "T2": (CONTROLE, "if n >= POUR_DOUTER}", "if n > POUR_DOUTER}"),
    "T3": (CONTROLE, "b is not None and date not in douteux and b[4] > 0", "b is not None and b[4] > 0"),
    "T4": (CONTROLE, "and 0 < b[2] <= min(b[0], b[3]) <= max(b[0], b[3]) <= b[1])", ")"),
    "T5": (CONTROLE, "        elif facteur_local(series, bnains, evenements, v, d, douteux, venues_de_bnains,\n",
           "        elif False and facteur_local(series, bnains, evenements, v, d, douteux, venues_de_bnains,\n"),
    "T6": (CONTROLE, "if n >= NON_CORROBOREES:", "if False:"),
    "T7": (CONTROLE, "if abs((s[q][3] / b[q][3]) / (s[p][3] / b[p][3]) - 1) > ACCORD:", "if False:"),
    "T8": (CONTROLE, "for d in cal if a <= d <= z and d not in s]", "for d in cal if d not in s]"),
    "T9": (CONTROLE, 'if r["date"] in s:', "if False:"),
    "T10": (CONTROLE, "if date < jour:", "if date <= jour:"),
    "T11": (CONTROLE, "x for x in y if x in b and x not in douteux and (valeur, x) not in venues_de_bnains",
            "x for x in y if x in b and x not in douteux"),
    "T12": (CONTROLE, "        if manquants:\n", "        if False:\n"),
    "T13": (CONTROLE, "            if len(fen) >= MINIMUM:", "            if len(fen) >= 1:"),
    "T14": (CONTROLE, "        if s:\n            a, z = min(s), max(s)", "        if True:\n            a, z = min(s), max(s)"),
    "T15": (CONTROLE, "    return {d.isoformat() for d, _ in CAL.seances_entre(a, z, seances)}",
            "    return {d.isoformat() for d, _ in CAL.seances_entre(a, z, seances) if any(d.isoformat() in x for x in series.values())}"),
    "T16": (CONTROLE, "                if not all(math.isfinite(x) for x in barre):", "                if False:"),
    "T17": (CONTROLE, "if s[p][3] <= 0 or s[q][3] <= 0 or abs(", "if abs("),
    "T18": (CONTROLE, "if (not avant and not coupe_avant) or (not apres and not coupe_apres) or len(voisins)", "if len(voisins)"),
    "T40": (CONTROLE, "    coupe_apres = jusqu_a != \"9999-12-31\" and proche(jusqu_a)", "    coupe_apres = False"),
    "T41": (CONTROLE, "                      and depuis <= x < jusqu_a)", "                      )"),
    "T19": (CONTROLE, "    proche = lambda x: abs((datetime.date.fromisoformat(x) - jour).days) <= PORTEE",
            "    proche = lambda x: True"),
    "T20": (CONTROLE, "            if suite == LACUNE:", "            if False:"),
    "T21": (CONTROLE, "        if ordre and max(s) < ordre[-min(FIN, len(ordre))]:", "        if False:"),
    "T22": (CONTROLE, "if b and max(b) == fin_bnains and v not in series]", "if False]"),
    "T23": (CONTROLE, "            if q in surveilles or entre:\n                k15.append(cas)",
            "            if q in surveilles or entre:\n                pass"),
    "T24": (CONTROLE, "            entre = [j for j in detache if p < j <= q]", "            entre = []"),
    "T26": (CONTROLE, "            permise -= 1\n", "            permise = rq / rp - 1\n"),
    "T34": (CONTROLE, "return cours / ((n * cours + prix) / (n + 1)) - 1", "return cours / ((cours + prix) / 2) - 1"),
    "T35": (CONTROLE, "        if cle in prises:\n            continue\n", "        if True:\n            continue\n"),
    "T30": (CONTROLE, "True, [m for v, m in sans_date if v in series]", "True, []"),
    "T31": (CONTROLE, "if ecart is None or not 0 <= ecart <= ECART_DE_COTATION:", "if ecart is None:"),
    "T32": (CONTROLE, "poser(r[\"valeur\"], jour, (\"bnains\",", "poser(r[\"valeur\"], premiere, (\"bnains\","),
    "T33": (CONTROLE, "return cloture / b[3] if b and b[3] > 0 else 0.0", "return cloture / b[3] if b else 0.0"),
    "T25": (CONTROLE, "            elif (v, p) in venues_de_bnains or (v, q) in venues_de_bnains:\n",
            "            elif ((v, p) in venues_de_bnains) != ((v, q) in venues_de_bnains):\n"),
    "T27": (CONTROLE, "AUTOUR = 5 ", "AUTOUR = 1 "),
    "T28": (CONTROLE, "            if q in surveilles or entre:\n", "            if entre:\n"),
    "T42": (CONTROLE, "return f[date] / b[date][3] / m - 1, max(ACCORD_FRANCFORT, 2 * bruit)",
            "return f[date] / b[date][3] / m - 1, 10 * max(ACCORD_FRANCFORT, 2 * bruit)"),
    "T43": (CONTROLE, "    return ecart is not None and abs(ecart) <= tolerance", "    return False"),
    "T44": (CONTROLE, "    if precedent is not None and f[precedent] == f[date]:\n        return None, None\n", ""),
    "T45": (CONTROLE, "        if verdict == \"fausse\":\n            k17.append(cas)", "        if False:\n            k17.append(cas)"),
    "T46": (CONTROLE, "                if f is not None and abs(rx / f - 1) <= ECART < abs(rz / f - 1):", "                if True:"),
    "T36": (CONTROLE, "                del barres[d]\n", "                pass\n"),
    "T37": (CONTROLE, " and (v, d) not in fausses)", ")"),
    "T38": (CONTROLE, "            entre = [j for j in detache if p < j <= q]", "            entre = [j for j in detache if j == q]"),
    "T39": (CONTROLE, "            if au < du:\n", "            if False:\n"),
    "T29": (CONTROLE, "(dates[i - AUTOUR - 1] if i > AUTOUR else None)", "dates[i - AUTOUR - 1]"),
    "T47": (CONTROLE, 'verdict = "le fichier a tort" if marge > MARGE', 'verdict = "le fichier a tort" if marge > 100 * MARGE'),
    "T48": (CONTROLE, "if b > 0 and y > 0 and abs(y / b - 1) <= ACCORD_INDICE:", "if b > 0:"),
    "T49": (CONTROLE, "    for d in sorted(set(indice) | soupconnees):", "    for d in seances:"),
    "T50": (CONTROLE, "                if apres > avant + SOUPCON:", "                if False:"),
    "T51": (CONTROLE, 'for j, n, _, _, _, m, ver in arbitrages\n          if ver == "le fichier a tort"]',
            'for j, n, _, _, _, m, ver in arbitrages\n          if False]'),
    "T52": (CONTROLE, "x in o and o[x][3] > 0 and barre_utilisable(bnains, v, x, frozenset())",
            "x in o and o[x][3] > 0 and x in bnains.get(v, {})"),
    "T53": (CONTROLE, "        k = max(range(i, n), key=lambda x: abs(m[x][i]))", "        k = i"),
    "T54": (CONTROLE, "        indice = lire_indice(os.path.join(racine, INDICE))", "        indice = None"),
    "U12": (REPARATION, "if (abs(r[d] / r[a] - 1 - K.marche_permise(b, droit)) > K.ECART or not fausses", "if (not fausses"),
    "U13": (REPARATION, "fausses = [x for x in fenetre if abs(r[x] / r[a] - 1) > K.ECART]", "fausses = list(fenetre)"),
    "U15": (REPARATION, "\n                    or not all(K.barre_utilisable(bnains, valeur, x, douteux) for x in fausses)):",
            "):"),
    "U14": (REPARATION, "f, k, _ = K.rapports(y, b, evenements, valeur, [a])", "f, k, _ = K.rapports(y, b, evenements, valeur, [d])"),
    "U16": (REPARATION, "                    a *= 1 + K.marche_permise(b, droit)", "                    a *= 1"),
    "U17": (REPARATION, "                if d < j <= ref_du:", "                if d <= j <= ref_du:"),
    "U18": (REPARATION, "            if abs(s) > abs(m) / 4:", "            if True:"),
    "U19": (REPARATION, '            for x in [x for x in y if x < d]:\n                o, h, l, c, vol = y[x]\n                y[x] = K.appliquer(y[x], 1 / (1 + m)', '            for x in [x for x in y if x <= d]:\n                o, h, l, c, vol = y[x]\n                y[x] = K.appliquer(y[x], 1 / (1 + m)'),
    "U20": (REPARATION, 'K.appliquer(y[x], 1 / (1 + m), 1 + m)', 'K.appliquer(y[x], 1 / (1 + m), 1)'),
    "U21": (CONTROLE, "    i = bisect.bisect_left(dates, jour)       # la première séance comparable à partir du jour",
            "    i = dates.index(jour) if jour in dates else 0"),
    "U22": (REPARATION, '        bnains, defauts_b, fausses = K.lire_paris(racine)', '        bnains, defauts_b, fausses = K.lire_cours(os.path.join(racine, K.BNAINS), COURS_BNAINS)[:2] + (set(),)'),
    "U23": (REPARATION, "            if verdict != \"fausse\" or not K.barre_sure(", "            if True or not K.barre_sure("),
    "U24": (REPARATION, "        if not remplacees:\n            return total", "        return total"),
    "U25": (REPARATION, "            if K.barre_sure(bnains, francfort or {}, valeur, d, douteux):\n                y[d], fp, fv = barre(b[d], f / a,",
            "            if K.barre_utilisable(bnains, valeur, d, douteux):\n                y[d], fp, fv = barre(b[d], f / a,"),
    "U26": (REPARATION, "        if not K.barre_sure(bnains, francfort or {}, valeur, d, douteux):",
            "        if not K.barre_utilisable(bnains, valeur, d, douteux):"),
    "U27": (REPARATION, "            if abs(ecart) <= K.PROPRE:\n                continue\n            avant = series[v][d][3]",
            "            if True:\n                continue\n            avant = series[v][d][3]"),
    "U28": (REPARATION, "    douteux = douteux - tort_de_yahoo ", "    douteux = douteux "),
    "U29": (REPARATION, 'if verdict == "le fichier a tort" for d in jours}', 'if verdict == "bnains a tort" for d in jours}'),
    "U30": (REPARATION, '            if sources.get((v, d)) != "yahoo" or not K.barre_utilisable(bnains, v, d, frozenset()):',
            '            if sources.get((v, d)) != "yahoo":'),
    "U11": (REPARATION, '("AXA", "2000-01-01", "2009-11-09",', '("AXA", "2000-01-01", "2009-11-10",'),
    "U10": (REPARATION, "        if not partie:\n", "        if False:\n"),
    "U1": (REPARATION, "if len(ref) < MIN_REFERENCE or accord < K.PART_PROPRE:", "if False:"),
    "U2": (REPARATION, "if len(communes) < MIN_REFERENCE or accord < K.PART_PROPRE or abs(f - 1) > K.PROPRE:",
           "if False:"),
    "U3": (REPARATION, "if f_ici is not None and abs(f_ici / (f / a) - 1) <= K.PROPRE:", "if False:"),
    "U4": (REPARATION, "for d, x in y.items() if d < debut}", "for d, x in y.items() if d <= debut}"),
    "U5": (REPARATION, "        if not K.barre_sure(bnains, francfort or {}, valeur, d, douteux):",
           "        if not K.barre_utilisable(bnains, valeur, d, frozenset()):"),
    "U6": (REPARATION, "    if arrets:\n", "    if False:\n"),
    "U7": (REPARATION, "str(int(x)) if float(x).is_integer() else repr(float(x))", "repr(float(x))"),
    "U8": (REPARATION, "            if d not in y:\n                continue\n", ""),
    "U9": (REPARATION, '        if f is None:\n            noter(journal, valeur, d, "non comblé"', '        if False:\n            noter(journal, valeur, d, "non comblé"'),
    "T55": (CONTROLE, "portes(series, origine, a_defaire, venues_de_bnains, detachements, alignes)\n                                     if origine is not None else []",
            "portes(series, origine, a_defaire, venues_de_bnains, detachements, alignes)\n                                     if False else []"),
    "T56": (CONTROLE, "if not ((v, x[0]) in fausses and abs(x[1] / x[2] / fausses[(v, x[0])] - 1) <= DEFAIT)]",
            "if True]"),
    "T57": (CONTROLE, "attendu) if abs(a / b / e - 1) > DEFAIT]", "attendu) if nom == \"clôture\" and abs(a / b / e - 1) > DEFAIT]"),
    "T59": (CONTROLE, "        if datetime.date.fromisoformat(r[\"date\"]).isoformat() != r[\"date\"]:\n",
            "        if datetime.date.fromisoformat(r[\"date\"]) is None:\n"),
    "T60": (CONTROLE, "all(math.isfinite(float(x)) and float(x) > 0 for x in (a, b))",
            "all(not float(x) <= 0 for x in (a, b))"),
    "T61": (CONTROLE, "        for x in lignes:\n            q = (alignes", "        for x in [x for x in lignes if x < d]:\n            q = (alignes"),
    "T62": (CONTROLE, "if x in o and (v, x) not in venues_de_bnains and min(o[x]) > 0]", "if x in o and min(o[x]) > 0]"),
    "T58": (CONTROLE, "        if (r[\"valeur\"], r[\"date\"]) in sortie:\n", "        if False:\n"),
    "U32": (REPARATION, "    for valeur, date, f in a_defaire:\n        y = series.get(valeur, {})",
            "    for valeur, date, f in []:\n        y = series.get(valeur, {})"),
    "U33": (REPARATION, "for x in sorted(x for x in y if x < date):", "for x in sorted(x for x in y if x <= date):"),
    "U34": (REPARATION, 'y[x] = K.appliquer(y[x], f, 1 / f)', 'y[x] = K.appliquer(y[x], f, 1)'),
    "T63": (CONTROLE, "        return distribue / (cours - distribue)\n", "        return 0.0\n"),
    "T64": (CONTROLE, "        if r[\"valeur_distribuee\"]:\n", "        if False:\n"),
    "T65": (CONTROLE, "                droit = (detachements or {}).get(v, {}).get(q)\n", "                droit = None\n"),
    "T66": (CONTROLE, "            if r[\"prix_souscription\"] or r[\"anciennes_pour_une_nouvelle\"] or not r[\"cours_veille\"]:",
            "            if False:"),
    "U35": (REPARATION, "    for valeur, d, raison in BARRES_YAHOO_ECARTEES:\n", "    for valeur, d, raison in ():\n"),
    "T67": (CONTROLE, "        if jour in detachements.get(valeur, {}):\n", "        if False:\n"),
    "T68": (CONTROLE, "        if not (droit[1] > 0 and droit[3] > 0 and 0 <= droit[2] < droit[1]):", "        if False:"),
    "T69": (CONTROLE, "avant = min(abs(o[q][3] / o[p][3] - 1 - rp), abs(o[q][3] / o[p][3] - 1 - rp_brut))",
            "avant = abs(o[q][3] / o[p][3] - 1 - rp)"),
    "T70": (CONTROLE, "            if (r[\"valeur\"], r[\"libelle_du_droit\"]) in officielles:", "            if False:"),
    "U36": (REPARATION, "    if trous:      #", "    if False:      #"),
    "T71": (CONTROLE, "            if bruit and m >= NETTETE * bruit and 0 in restes:", "            if bruit and 0 in restes:"),
    "T72": (CONTROLE, "if not (restes[0] < abs(e[0]) and all(restes[0] < r for k, r in restes.items() if k)):",
            "if not (restes[0] < abs(e[0])):"),
    "T73": (CONTROLE, "    return any(f in t for f in lettres) or any(", "    return True or any("),
    "T74": (CONTROLE, "    k21, k21b, k21c, k21_jugees = dates_declarees(bnains, detachements, citations, evenements)\n",
            "    k21, k21b, k21c, k21_jugees = [], [], [], 0\n"),
    "T75": (CONTROLE, "    t = \" \".join(re.findall(r\"«([^»]*)»\", citation))", "    t = citation"),
    "T76": (CONTROLE, "if x is not None and abs(x) <= SAUT] if i is not None else []", "if x is not None] if i is not None else []"),
    "T77": (CONTROLE, "            if datetime.date.fromisoformat(jour).weekday() >= 5 or (", "            if False and ("),
    "T78": (CONTROLE, "                valide = not j or datetime.date.fromisoformat(j).isoformat() == j",
            "                valide = True"),
    "T79": (CONTROLE, "VOISINAGE = 3 ", "VOISINAGE = 1 "),
    "T80": (CONTROLE, "    if not bnains:      #", "    if False:      #"),
    "T81": (CONTROLE, "    t = \"\".join(c for c in t if not unicodedata.combining(c))\n", ""),
    "T82": (CONTROLE, "re.search(r\"(?<!\\d)\" + re.escape(f) + r\"(?!\\d)\", t)", "f in t"),
    "T83": (CONTROLE, "NETTETE = 3 ", "NETTETE = 1.5 "),
    "T84": (CONTROLE, "                if (valeur, jour) in acceptes:\n", "                if False:\n"),
    "T85": (CONTROLE, "Jean-Luc n'a pas acceptées (JOURS_ACCEPTES) ; et jours acceptés sans opération\", True, k21b),",
            "Jean-Luc n'a pas acceptées (JOURS_ACCEPTES) ; et jours acceptés sans opération\", False, k21b),"),
    "T86": (CONTROLE, "    for v, j in sorted(set(acceptes)):\n", "    for v, j in []:\n"),
    "T87": (CONTROLE, "            jugees += 1\n", "            jugees += 1\n            if (valeur, jour) in acceptes:\n"
            "                acceptees.append(f\"{valeur} {jour}\")\n                continue\n"),
    "T88": (CONTROLE, "        if sum(1 for x in JOURS_ACCEPTES if x[:2] == (v, j)) > 1:", "        if False:"),
    "T89": (CONTROLE, "        elif citations is not None and (v, j) not in utilisees:", "        elif False:"),
    "T92": (CONTROLE, "        if droit and droit[0] in (\"document\", \"distribution\"):\n            f = f /",
            "        if droit and droit[0] == \"distribution\":\n            f = f /"),
    "T91": (CONTROLE, "        if droit and droit[0] in (\"document\", \"distribution\"):\n            f = f / (1 + marche_permise({}, droit))\n",
            "        if False:\n            f = f / (1 + marche_permise({}, droit))\n"),
    "T90": (CONTROLE, "    if detachements is None:\n        return contredites, non_tranchees, acceptees, jugees",
            "    if not detachements:\n        return contredites, non_tranchees, acceptees, jugees"),
    "T93": (CONTROLE, "(divisions(evenements, w, p) / divisions(evenements, w, d)",
            "(1.0 or divisions(evenements, w, p) / divisions(evenements, w, d)"),
    "T94": (CONTROLE, "dates_declarees(bnains, detachements, citations, evenements)",
            "dates_declarees(bnains, detachements, citations)"),
    "T95": (CONTROLE, "float(chiffres[1]) + float(r[\"dividende_non_attache\"] or 0)", "float(chiffres[1])"),
    "T96": (CONTROLE, "            if all((o[\"cours_veille\"], o[\"prix_souscription\"], o[\"anciennes_pour_une_nouvelle\"])):",
            "            if False:"),
    "T97": (CONTROLE, "    t += \" \".join(f\" {j} {m} {a} \" for j, m, a in re.findall(", "    t += \" \".join(f\" {j} {m} {a} \" for j, m, a in [] and re.findall("),
    "T98": (CONTROLE, "            q = (alignes or {}).get((v, x), 1.0)", "            q = 1.0"),
    "T99": (CONTROLE, "        if r[\"geste\"] == \"aligné\":", "        if False:"),
    "U37": (REPARATION, "ALIGNEMENT = K.MARCHE_EXACTE ", "ALIGNEMENT = 1.0 "),
    "T100": (CONTROLE, "MARCHE_EXACTE = 0.0005 ", "MARCHE_EXACTE = 1.0 "),
    "T101": (CONTROLE, "            if s is not None and abs((1 + s) / (1 + m) - 1) > MARCHE_EXACTE:", "            if False:"),
    "T102": (CONTROLE, '            if etat is not None and etat[3] != float(g["close_avant"]):', '            if False:'),
    "T103": (CONTROLE, '            if etat[3] != float(g["close_apres"]):', '            if False:'),
    "T104": (CONTROLE, '                        if barre[i] != etat[i]]', '                        if i == 4 and barre[i] != etat[i]]'),
    "T105": (CONTROLE, '                        if barre[i] != etat[i]]', '                        if i < 4 and barre[i] != etat[i]]'),
    "T106": (CONTROLE, "            lignes = [r for r in lignes if r[\"sha256\"].strip().lower() == e]\n            if len(lignes) != 1:",
             "            lignes = [r for r in lignes if r[\"sha256\"].strip().lower() == e] or lignes\n            if len(lignes) != 1:"),
    "T107": (CONTROLE, '            if not ADRESSE_ENTIERE.fullmatch(r["adresse"].strip()):', '            if False:'),
    "T108": (CONTROLE, "        if not (programme.endswith(\".py\") and os.path.isfile(os.path.join(racine, programme))):",
             "        if not os.path.isfile(os.path.join(racine, programme)):"),
    "T109": (CONTROLE, '"manquants (A-578)", True, k23)]:', '"manquants (A-578)", False, k23)]:'),
    "T110": (CONTROLE, "        if lecteur.fieldnames != PROVENANCE_DES_FICHIERS:", "        if False:"),
    "T111": (CONTROLE, "        if not lus:\n", "        if False:\n"),
    "T112": (CONTROLE, '            if barre is not None and etat is None:', '            if barre is not None and etat is None and not gestes:'),
    "T113": (CONTROLE, "        if lecteur.fieldnames != JOURNAL_DES_REPARATIONS:", "        if False:"),
    "T114": (CONTROLE, '            k23 += lignes_non_rejouees(series, lire_les_sources(fichier), origine, bnains, journal)', '            pass'),
    "T115": (CONTROLE, "                                  else [relatif, ORIGINE.replace(os.sep, \"/\"), BNAINS.replace(os.sep, \"/\")])",
             "                                  else [])"),
    "T116": (CONTROLE, '            base = paris.get(v, {}).get(d) if g["depart"] == "paris" else etat', '            base = (etat or paris.get(v, {}).get(d)) if g["depart"] == "paris" else etat'),
    "T117": (CONTROLE, "        if f in chemin:\n", "        if False:\n"),
    "T118": (CONTROLE, "        if not arrive:\n            cas.add", "        if False:\n            cas.add"),
    "T119": (CONTROLE, '            if g["depart"] != GESTES_DU_JOURNAL.get(g["geste"]):', '            if False:'),
    "T120": (CONTROLE, '            if (g["close_avant"] == "") != (etat is None):', '            if False:'),
    "T121": (CONTROLE, '                        if barre[i] != etat[i]]', '                        if abs(barre[i] - etat[i]) > 1e-5 * max(abs(barre[i]), abs(etat[i]))]'),
    "T122": (CONTROLE, '            if defaut == "un dossier":', '            if False:'),
    "T123": (CONTROLE, "    return posixpath.normpath(x.strip().replace(\"\\\\\", \"/\"))", "    return x"),
    "T124": (CONTROLE, "            if not re.fullmatch(r\"[0-9a-f]{64}\", r[\"sha256\"].strip().lower()):", "            if False:"),
    "T125": (CONTROLE, "            if len(lignes) != 1:\n                cas.add(f\"{f} : son empreinte",
             "            if not lignes:\n                cas.add(f\"{f} : son empreinte"),
    "T126": (CONTROLE, "f\"ne se remontent pas\"] if declare and not a_la_source else []", "f\"ne se remontent pas\"] if False else []"),
    "T127": (CONTROLE, "        if f in FICHIERS_REPARES and _chemin(r[\"produit_par\"]) != FICHIERS_REPARES[f]:", "        if False:"),
    "T128": (CONTROLE, "                                  else [relatif, ORIGINE.replace(os.sep, \"/\"), BNAINS.replace(os.sep, \"/\")])",
             "                                  else [ORIGINE.replace(os.sep, \"/\"), BNAINS.replace(os.sep, \"/\")])"),
    "T129": (CONTROLE, '                elif sources.get((v, d)) != venue:', '                elif False:'),
    "T130": (CONTROLE, '                etat, venue = arrondir(base, fp, fv), SOURCE_PARIS', '                etat, venue = arrondir(base, fp, 1 / fp), SOURCE_PARIS'),
    "T131": (CONTROLE, '                etat, venue = arrondir(base, fp, fv), SOURCE_PARIS', '                etat, venue = appliquer(base, fp, fv), SOURCE_PARIS'),
    "T132": (CONTROLE, '            if defauts_o:      # superviseur', '            if False:      # superviseur'),
    "T133": (CONTROLE, '                etat, venue = None, None\n                continue', '                continue'),
    "T134": (CONTROLE, '            elif barre is None and etat is not None:', '            elif barre is None and etat is not None and not gestes:'),
    "T135": (CONTROLE, '\n                       | {(v, d) for v, s in origine.items() for d in s}):', '):'),
    "T136": (CONTROLE, '    for v, d in sorted({(v, d) for v, s in series.items() for d in s} | set(journal)\n', '    for v, d in sorted({(v, d) for v, s in series.items() for d in s}\n'),
    "T137": (CONTROLE, '            if g["geste"] not in GESTES_DU_JOURNAL:', '            if False:'),
    "T138": (CONTROLE, '                if r[c] != "" and not math.isfinite(float(r[c])):', '                if False:'),
    "T139": (CONTROLE, '            if g["depart"] == "" and ecrits:', '            if False:'),
    "T140": (CONTROLE, '    return bnains, defauts, oter_les_barres_fausses(os.path.join(racine, FAUSSES), bnains)', '    return bnains, defauts, oter_les_barres_fausses(os.path.join(racine, FAUSSES), {v: dict(x) for v, x in bnains.items()})'),
    "T141": (CONTROLE, '            if g["depart"] != "" and len(ecrits) < 3:', '            if False:'),
    "T142": (CONTROLE, '            if r["lu"].strip():\n                cas.add(f"{f} : écrit à la main', '            if False:\n                cas.add(f"{f} : écrit à la main'),
    "T143": (CONTROLE, '            if r["adresse"].strip():', '            if False:'),
    "T144": (CONTROLE, '            if not r["preuve"].strip():', '            if False:'),
    "T145": (CONTROLE, '            defaut, cites = sources_ecrites_a_la_main(racine, f)', '            defaut, cites = None, []'),
    "T146": (CONTROLE, '                if not remonter(x, chemin + [f]):', '                if False:'),
    "T147": (CONTROLE, '        if f in FICHIERS_REPARES and _chemin(r["produit_par"]) != FICHIERS_REPARES[f]:', '        if f in FICHIERS_REPARES and _chemin(r["produit_par"]) != FICHIERS_REPARES[f] and r["produit_par"] != ECRIT_A_LA_MAIN:'),
    "T148": (CONTROLE, '                if not (x.get(citation) or "").strip():', '                if False:'),
    "T149": (CONTROLE, '                    if not ADRESSE_ENTIERE.fullmatch(m):', '                    if False:'),
    "T150": (CONTROLE, '            if not set(COLONNES_DES_SOURCES_A_LA_MAIN) <= set(lecteur.fieldnames or []):', '            if False:'),
    "T151": (CONTROLE, '    if not vu:\n        return "sans aucune ligne", []', '    if False:\n        return "sans aucune ligne", []'),
    "T152": (CONTROLE, '    if c.startswith("/") or re.match(r"[A-Za-z]:", c):', '    if False:'),
    "T153": (CONTROLE, '    if ".." in c.split("/"):', '    if False:'),
    "T154": (CONTROLE, '        if os.path.islink(partiel):', '        if False:'),
    "T155": (CONTROLE, '                    c, defaut = chemin_du_depot(racine, m)', '                    c, defaut = _chemin(m), None'),
    "T156": (CONTROLE, '                if not adresses and not chemins:', '                if False:'),
    "T157": (CONTROLE, '            x, defaut = chemin_du_depot(racine, brut)', '            x, defaut = _chemin(brut), None'),
    "T158": (CONTROLE, 'ADRESSE_ENTIERE = re.compile(r"https?://[A-Za-z0-9-]+(?:\\.[A-Za-z0-9-]+)+(?::[0-9]+)?(?:/\\S*)?")', 'ADRESSE_ENTIERE = re.compile(r"https?://\\S+|.*https?://\\S*")'),
    "T159": (CONTROLE, '    if os.path.isdir(os.path.join(racine, n)):\n        return n, "un dossier"', '    if False:\n        return n, "un dossier"'),
    "T160": (CONTROLE, '                if not (x.get(citation) or "").strip():', '                if n == 2 and not (x.get(citation) or "").strip():'),
    "T161": (CONTROLE, '                for m in adresses:', '                for m in (adresses if n == 2 else []):'),
    "T162": (CONTROLE, '                for m in adresses:', '                for m in adresses[:1]:'),
    "T163": (CONTROLE, '                for m in chemins:', '                for m in (chemins if n == 2 else []):'),
    "T164": (CONTROLE, '                for m in chemins:', '                for m in chemins[:1]:'),
    "T165": (CONTROLE, '                if not adresses and not chemins:', '                if n == 2 and not adresses and not chemins:'),
    "T166": (CONTROLE, '        for brut in lus:', '        for brut in lus[:1]:'),
    "T167": (CONTROLE, '                    if not os.path.isfile(os.path.join(racine, c)):', '                    if False:'),
    "T168": (CONTROLE, 'qui ne se remonte pas")\n                    arrive = False', 'qui ne se remonte pas")\n                    pass'),
    "T169": (CONTROLE, '    if c.startswith("/") or re.match(r"[A-Za-z]:", c):', '    if c.startswith("/"):'),
    "T170": (CONTROLE, '            for x in lecteur:', '            for x in list(lecteur)[-1:]:'),
    "T171": (CONTROLE, '                for m in adresses:', '                for m in adresses[-1:]:'),
    "T172": (CONTROLE, '                for m in chemins:', '                for m in chemins[-1:]:'),
    # 27-10-2026 : la trace de chaque séance non comblée, et l'empreinte que la réparation inscrit au registre (H63)
    "T173": (REPARATION, '            noter(journal, valeur, d, "non comblé", "", "", "", raison, "")\n', '            pass\n'),
    "T174": (REPARATION, '        l[i_s] = hashlib.sha256(open(os.path.join(racine, c), "rb").read()).hexdigest()', '        pass'),
    "U38": (REPARATION, "            q = (1 + s) / (1 + m)\n", "            q = (1 + m) / (1 + s)\n"),
    "U39": (REPARATION, "            if abs(s) <= abs(m) / 4 or abs((1 + s) / (1 + m) - 1) <= ALIGNEMENT:",
            "            if abs((1 + s) / (1 + m) - 1) <= ALIGNEMENT:"),
    "U31": (REPARATION, "            if f is None:\n                continue\n            ecart = series[v][d][3]",
            "            if False:\n                continue\n            ecart = series[v][d][3]"),
}


def charger(sabotage=None):
    """Charge le contrôle puis la réparation — les vrais fichiers, ou des copies dont l'un est saboté."""
    if sabotage is None:
        dossier = PROGRAMMES
    else:
        dossier = tempfile.mkdtemp()
        for f in ("CONTRATS_DES_FICHIERS.py", "CALENDRIER_DE_LA_BOURSE.py", "CONTROLER_L_HISTORIQUE_LONG.py",
                  "REPARER_L_HISTORIQUE_LONG.py"):
            shutil.copy(os.path.join(PROGRAMMES, f), dossier)
        chemin, cible, remplace = sabotage
        copie = os.path.join(dossier, os.path.basename(chemin))
        open(copie, "w", encoding="utf-8").write(open(chemin, encoding="utf-8").read().replace(cible, remplace))
    for nom in ("CONTRATS_DES_FICHIERS", "CALENDRIER_DE_LA_BOURSE", "CONTROLER_L_HISTORIQUE_LONG", "REPARER_L_HISTORIQUE_LONG"):
        sys.modules.pop(nom, None)
    sys.path.insert(0, dossier)
    try:
        modules = []
        for nom in ("CONTROLER_L_HISTORIQUE_LONG", "REPARER_L_HISTORIQUE_LONG"):
            sp = importlib.util.spec_from_file_location(nom, os.path.join(dossier, nom + ".py"))
            m = importlib.util.module_from_spec(sp)
            sys.modules[nom] = m
            sp.loader.exec_module(m)
            modules.append(m)
    finally:
        sys.path.remove(dossier)
    return modules


def racine_d_essai(abimer_yahoo=None, abimer_bnains=None):
    """Une racine jetable : l'extrait Yahoo 2005, l'extrait bnains 2005, le vrai evenements.json, un faux maître."""
    r = tempfile.mkdtemp()
    os.makedirs(os.path.join(r, "donnees", "sources_yahoo"))
    os.makedirs(os.path.join(r, "donnees", "sources_bnains"))
    for src, dst, abimer in (("yahoo_2005.csv", "donnees/sources_yahoo/yahoo_ohlcv_propre.csv", abimer_yahoo),
                             ("bnains_2005.csv", "donnees/sources_bnains/bnains_cac40.csv", abimer_bnains)):
        lignes = list(csv.reader(open(os.path.join(TEMOINS, src), encoding="utf-8", newline="")))
        if abimer:
            lignes = abimer(lignes)
        with open(os.path.join(r, dst), "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(lignes)
    shutil.copy(EVENEMENTS, os.path.join(r, "donnees", "sources_yahoo", "evenements.json"))
    shutil.copy(VERDICTS, os.path.join(r, "donnees", "sources_yahoo", "AJUSTEMENTS_DE_YAHOO.csv"))
    shutil.copy(DROITS, os.path.join(r, "donnees", "sources_bnains", "DROITS_BNAINS.csv"))
    shutil.copy(OFFICIELS, os.path.join(r, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv"))
    shutil.copy(FAUSSES, os.path.join(r, "donnees", "sources_bnains", "BARRES_BNAINS_FAUSSES.csv"))
    os.makedirs(os.path.join(r, "donnees", "sources_francfort"))
    shutil.copy(FRANCFORT, os.path.join(r, "donnees", "sources_francfort", "COURS_DE_FRANCFORT.csv"))
    os.makedirs(os.path.join(r, "donnees", "sources_indice"))
    shutil.copy(INDICE, os.path.join(r, "donnees", "sources_indice", "INDICE_CAC40.csv"))
    shutil.copy(EURONEXT, os.path.join(r, "donnees", "CALENDRIER_EURONEXT.csv"))   # le calendrier officiel (27-10-2026)
    shutil.copy(PROVENANCE, os.path.join(r, "donnees", "PROVENANCE_DES_FICHIERS.csv"))   # la réparation y inscrit ses fichiers
    open(os.path.join(r, "donnees", "cours_maitre.csv"), "w").write("valeur,date,open,high,low,close,volume,source\n")
    return r


def lancer(f, *argv):
    sortie = io.StringIO()
    with contextlib.redirect_stdout(sortie):
        code = f(*argv)
    return code, sortie.getvalue()


def lire(r, chemin):
    return list(csv.DictReader(open(os.path.join(r, chemin), encoding="utf-8", newline="")))


def multiplier(lignes, valeur, date, colonne, facteur):
    """Multiplie une colonne d'une ligne (valeur, date) d'une liste CSV lue avec son en-tête."""
    i = lignes[0].index(colonne)
    for l in lignes[1:]:
        if l[0] == valeur and l[1] == date:
            l[i] = repr(float(l[i]) * facteur)
    return lignes


def resultats_du_controle(K, r, fichier):
    code, out = lancer(K.main, [r, fichier])
    lignes = {l.split()[0]: l for l in out.splitlines() if l[:5].strip().startswith("K")}
    return code, out, lignes


def synthese(K, regimes, trou):
    """Deux séries d'une valeur « X » sur 30 séances : bnains à 100, la série à 100 × facteur du régime ; sans `trou`."""
    dates = [f"2005-03-{j:02d}" for j in range(1, 31)]
    b = {d: (100.0, 101.0, 99.0, 100.0, 1000.0) for d in dates}
    y = {}
    for i, d in enumerate(dates):
        f = regimes(i)
        if d != trou:
            y[d] = (100 * f, 101 * f, 99 * f, 100 * f, 1000.0)
    return {"X": y}, {"X": b}, dates


def epreuves(K, R):
    res = {}
    axa_fenetre = [x for x in R.RECONSTRUCTIONS if x[0] == "AXA"]     # la vraie, avant que les épreuves la changent
    reconstructions_vraies, retraits_vrais = R.RECONSTRUCTIONS, R.RETRAITS
    # H1 : le contrôle sur l'extrait Yahoo
    try:
        r = racine_d_essai()
        code, out, k = resultats_du_controle(K, r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        res["H1"] = code == 1 and "REFUS" in k["K5"] and "AXA 2005" in out and "REFUS" in k["K8"] \
            and "REFUS" in k["K9"] and "ENGIE :" in out
    except Exception:
        res["H1"] = False
    # H8 : ecarts
    try:
        r = racine_d_essai(abimer_bnains=lambda l: multiplier(l, "VINCI", "2005-06-15", "close", 1.05))
        s, _, _ = K.lire_cours(os.path.join(r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"))
        b, _, _ = K.lire_cours(os.path.join(r, "donnees/sources_bnains/bnains_cac40.csv"), K.COURS_BNAINS)
        e = K.ecarts({"VINCI": s["VINCI"]}, b)
        autres = [abs(x) for (v, d), x in e.items() if d != "2005-06-15"]
        courte = {"VINCI": dict(sorted(s["VINCI"].items())[:K.MINIMUM - 1])}
        res["H8"] = abs(e[("VINCI", "2005-06-15")] - (1 / 1.05 - 1)) < 0.003 and max(autres) < 0.0005 and len(autres) > 100 \
            and K.ecarts(courte, b) == {} and K.trous({"VIDE": {}}, {"2005-06-15"}) == []
    except Exception:
        res["H8"] = False
    # H7 : jours douteux — 5 valeurs abîmées le 2005-05-16, jour où AIR LIQUIDE manque chez Yahoo ; 4 le 2005-09-15
    try:
        # Les vraies données ont déjà des valeurs en écart certains jours (AXA en 2005) : on en abîme juste assez
        # pour qu'il y en ait EXACTEMENT 5 le 16-05-2005 et EXACTEMENT 4 le 15-09-2005.
        r0 = racine_d_essai()
        s0, _, _ = K.lire_cours(os.path.join(r0, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"))
        b0, _, _ = K.lire_cours(os.path.join(r0, "donnees/sources_bnains/bnains_cac40.csv"), K.COURS_BNAINS)
        e0 = K.ecarts(s0, b0)
        saines = ("ACCOR", "LVMH", "BNP PARIBAS", "CARREFOUR", "RENAULT", "VINCI", "L'OREAL")
        a_abimer = {}
        for jour, cible in (("2005-05-16", 5), ("2005-09-15", 4)):
            deja = sum(1 for (v, d), x in e0.items() if d == jour and abs(x) > K.ECART)
            a_abimer[jour] = [v for v in saines if abs(e0.get((v, jour), 1)) < K.ECART / 2][:cible - deja]

        def abime(l):
            for jour, valeurs in a_abimer.items():
                for v in valeurs:
                    multiplier(l, v, jour, "close", 1.03)
            return l
        r = racine_d_essai(abimer_bnains=abime)
        ff = os.path.join(r, "donnees", "sources_francfort", "COURS_DE_FRANCFORT.csv")
        lignes_f = open(ff, encoding="utf-8").read().splitlines(True)
        avec_francfort = racine_d_essai(abimer_bnains=abime)
        open(ff, "w", encoding="utf-8").writelines(l for l in lignes_f if not (l.split(",")[2:3] == ["2005-05-16"]
                                                                           and l.split(",")[0] in ("AIR LIQUIDE", "DANONE")))
        s, _, _ = K.lire_cours(os.path.join(r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"))
        b, _, _ = K.lire_cours(os.path.join(r, "donnees/sources_bnains/bnains_cac40.csv"), K.COURS_BNAINS)
        dt = K.jours_douteux(K.ecarts(s, b))
        R.RECONSTRUCTIONS, R.RETRAITS = (), ()
        code, out = lancer(R.reparer, r)
        repare = {(l["valeur"], l["date"]) for l in lire(r, R.SORTIE)}
        code2, out2, _ = resultats_du_controle(K, r, R.SORTIE)
        code3, _ = lancer(R.reparer, avec_francfort)
        confirme = {(l["valeur"], l["date"]): l["source"] for l in lire(avec_francfort, R.SORTIE)}
        res["H7"] = dt == {"2005-05-16"} and code == 0 and ("AIR LIQUIDE", "2005-05-16") not in repare \
            and code3 == 0 and confirme.get(("AIR LIQUIDE", "2005-05-16")) == "bnains" \
            and ("DANONE", "2005-05-16") not in repare and "AIR LIQUIDE 2005-05-16 (bnains : jour douteux)" in out2 \
            and ("BOUYGUES", "2005-01-06") in repare
    except Exception:
        res["H7"] = False
    # H9 : K1, K2, K3, K4, K10, K10b
    try:
        def abime(l):
            l.append(list(l[5]))                                   # K1 : une ligne en double
            multiplier(l, "ACCOR", "2005-02-01", "high", 0.5)      # K2 : plus haut sous la clôture
            multiplier(l, "ACCOR", "2005-02-02", "volume", 0)      # K3 : volume nul
            l.append(["ACCOR", "2005-02-05", "22", "23", "21", "22", "1000"])   # K4 : un samedi
            multiplier(l, "LVMH", "2005-04-12", "close", 1.4)       # K10 : saut que bnains contredit
            for c in ("open", "high", "low"):
                multiplier(l, "LVMH", "2005-04-12", c, 1.4)
            return l
        r = racine_d_essai(abimer_yahoo=abime,
                           abimer_bnains=lambda l: [x for x in l if not (x[0] == "SANOFI" and x[1] == "2005-05-02")])
        r2 = racine_d_essai(abimer_yahoo=lambda l: multiplier(multiplier(multiplier(multiplier(
            l, "SANOFI", "2005-05-02", "close", 1.4), "SANOFI", "2005-05-02", "high", 1.4), "SANOFI", "2005-05-02", "open", 1.4),
            "SANOFI", "2005-05-02", "low", 1.4),
            abimer_bnains=lambda l: [x for x in l if not (x[0] == "SANOFI" and x[1] == "2005-05-02")])
        code, out, k = resultats_du_controle(K, r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        code2, out2, k2 = resultats_du_controle(K, r2, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        res["H9"] = all("REFUS" in k[x] for x in ("K1", "K2", "K3", "K4", "K10")) and "ACCOR 2005-02-05" in out \
            and "LVMH 2005-04-11→2005-04-12" in out and "REFUS" not in k2["K10"] \
            and "SANOFI 2005-04-29→2005-05-02 +" in out2 and "bnains n'a pas les deux séances" in out2
    except Exception:
        res["H9"] = False
    # H10 : facteur_local, et son rang dans controler
    try:
        ev = {}
        s, b, dates = synthese(K, lambda i: 0.9 if i < 15 else 1.0, "2005-03-16")
        a = K.facteur_local(s, b, ev, "X", "2005-03-16", set(), ())
        s2, b2, _ = synthese(K, lambda i: 0.9 if i < 5 else 1.0, "2005-03-20")
        f2 = K.facteur_local(s2, b2, ev, "X", "2005-03-20", set(), ())
        venues = {("X", d) for d in dates[16:21]}
        s3, b3, _ = synthese(K, lambda i: 0.9 if i < 15 or 16 <= i <= 20 else 1.0, "2005-03-16")
        f3 = K.facteur_local(s3, b3, ev, "X", "2005-03-16", set(), venues)
        s4, b4, _ = synthese(K, lambda i: 0.9 if i < 15 else 1.0, "2005-03-16")
        s4["Y"] = {d: (100.0, 101.0, 99.0, 100.0, 1000.0) for d in dates}
        rang = {num: cas for num, _, _, cas in cal_(K.controler)(s4, [], b4, ev)}
        s5, b5, _ = synthese(K, lambda i: 1.0, "2005-03-16")
        un_cote = K.facteur_local(s5, b5, ev, "X", "2005-03-16", set(), {("X", d) for d in dates[16:]})
        loin_y = {d: (100.0, 101.0, 99.0, 100.0, 1000.0) for d in
                  ("2005-01-03", "2005-01-04", "2005-01-05", "2005-06-01", "2005-06-02", "2005-06-03")}
        loin = K.facteur_local({"X": loin_y}, {"X": dict(loin_y)}, ev, "X", "2005-03-15", set(), ())
        res["H10"] = a[0] is None and abs(f2[0] - 1.0) < 1e-9 and f2[3] == 10 and f3[0] is None \
            and un_cote[0] is None and un_cote[3] == 5 and loin[0] is None and loin[3] == 0 \
            and rang["K6"] == [] and any(c.startswith("X 2005-03-16 (le facteur change") for c in rang["K7"])
    except Exception:
        res["H10"] = False
    # H16 : barre_utilisable
    try:
        b = {"X": {"a": (10.0, 11.0, 9.0, 12.0, 5.0), "b": (10.0, 11.0, 9.0, 10.5, 0.0), "c": (10.0, 11.0, 9.0, 10.5, 5.0)}}
        res["H16"] = not K.barre_utilisable(b, "X", "a", set()) and not K.barre_utilisable(b, "X", "b", set()) \
            and K.barre_utilisable(b, "X", "c", set()) and not K.barre_utilisable(b, "X", "c", {"c"})
    except Exception:
        res["H16"] = False
    # H11 : divisions
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        res["H11"] = K.divisions(ev, "AXA", "2001-05-15") == 4 and K.divisions(ev, "AXA", "2001-05-16") == 1
    except Exception:
        res["H11"] = False
    # H17 : calibrage sur les vrais fichiers entiers
    try:
        s, d, _ = K.lire_cours(os.path.join(RACINE, "donnees", "sources_yahoo", "yahoo_ohlcv_propre.csv"))
        b, _, _ = K.lire_cours(os.path.join(RACINE, K.BNAINS), K.COURS_BNAINS)
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        rang = {num: cas for num, _, _, cas in cal_(K.controler)(s, d, b, ev)}
        res["H17"] = [c for c in rang["K5"] if c.startswith("AXA")] == [
            "AXA 2001 : 22", "AXA 2002 : 49", "AXA 2003 : 122", "AXA 2004 : 173", "AXA 2005 : 153", "AXA 2006 : 124",
            "AXA 2007 : 92"] and len(K.ecarts(s, b)) == 150740 - 1
        # Sur le calendrier officiel (27-10-2026), les séances manquantes se décomposent : les 222 de Cowork, aux séances
        # où au moins 25 valeurs ont une ligne ; 181 aux cinq demi-séances, où Yahoo n'en a aucune ; le reste aux séances
        # où Yahoo cote peu de valeurs (2000 et 2001). Mesuré le 27-10-2026 : 222 + 181 + 127 = 530.
        cal = K.calendrier(s, SEANCES)
        t_ = K.trous(s, cal)
        lignes_du_jour = {}
        for x in s.values():
            for d_ in x:
                lignes_du_jour[d_] = lignes_du_jour.get(d_, 0) + 1
        pleins = sum(1 for _, d_ in t_ if lignes_du_jour.get(d_, 0) >= 25)
        demi = sum(1 for _, d_ in t_ if d_ in DEMI_SEANCES)
        print(f"      H17 : séances manquantes {len(t_)} — {pleins} aux séances pleines, {demi} aux demi-séances")
        res["H17"] = res["H17"] and set(DEMI_SEANCES) <= cal and (pleins, demi, len(t_)) == (222, 181, 530)
    except Exception:
        res["H17"] = False
    # H2 et H14 : la réparation sur l'extrait
    try:
        r = racine_d_essai()
        avant = {c: hashlib.sha256(open(os.path.join(r, c), "rb").read()).hexdigest()
                 for c in ("donnees/cours_maitre.csv", "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")}
        R.RECONSTRUCTIONS = FENETRE_EL
        R.RETRAITS = (("ENGIE", "2005-07-08", "SUEZ", "épreuve"),)
        code, out = lancer(R.reparer, r)
        orig = {(l["valeur"], l["date"]): l for l in lire(r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")}
        rep = {(l["valeur"], l["date"]): l for l in lire(r, R.SORTIE)}
        journal = lire(r, R.JOURNAL)
        el = [k for k in rep if k[0] == "ESSILORLUXOTTICA" and k[1] <= "2005-02-28"]
        # EssilorLuxottica est d'abord défait (le 06-05-2024 de Yahoo, × 184,07/180,12) : la clôture d'origine corrigée
        defait = {(v, d): f for v, d, f in K.lire_a_defaire(VERDICTS)}
        f_el = next(f for (v, d), f in defait.items() if v == "ESSILORLUXOTTICA" and d > "2005-02-28")
        ecart_max = max(abs(float(rep[k]["close"]) / float(orig[k]["close"]) / f_el - 1) for k in el if k in orig)
        engie = sorted(d for v, d in rep if v == "ENGIE")
        code2, out2, k2 = resultats_du_controle(K, r, R.SORTIE)
        gardes = {j["date"] for j in journal if j["geste"] == "gardé" and j["valeur"] == "ESSILORLUXOTTICA"}
        # Accor, 03-01-2005 (Yahoo : 22,7838, volume 533 797) : le facteur de Yahoo du 02-07-2010 (0,704727) est défait
        # (décision de Jean-Luc du 09-10-2026 à 21h00) ; la distribution d'Edenred qui le remplace ne se mesure pas sur
        # l'extrait de 2005 (`ajuster` la range en « non mesurable ») : elle n'est pas posée, et K20 REFUSE ce fichier —
        # une correction défaite que rien ne remplace ne passe pas
        res["H2"] = code == 0 and len(el) >= 35 and ecart_max < 0.002 \
            and all(rep[k]["source"] == ("yahoo" if k[1] in gardes else "bnains") for k in el) \
            and engie[0] == "2005-07-08" and rep[("TOTALENERGIES", "2005-05-23")]["source"] == "bnains" \
            and sum(1 for j in journal if j["geste"] == "retiré" and j["valeur"] == "ENGIE") == \
            sum(1 for k in orig if k[0] == "ENGIE" and k[1] < "2005-07-08") \
            and "REFUS" not in k2["K6"] and "REFUS" not in k2["K9"] \
            and abs(float(rep[("ACCOR", "2005-01-03")]["close"]) - 22.7838 / 0.704727) < 1e-6 \
            and abs(float(rep[("ACCOR", "2005-01-03")]["volume"]) - 533797 * 0.704727) < 1e-3 and "REFUS" in k2["K20"]
        apres = {c: hashlib.sha256(open(os.path.join(r, c), "rb").read()).hexdigest() for c in avant}
        res["H14"] = avant == apres
    except Exception:
        res["H2"] = res["H14"] = False
    # H4 : une vraie ligne retirée puis comblée
    try:
        r = racine_d_essai(abimer_yahoo=lambda l: [x for x in l if not (x[0] == "TOTALENERGIES" and x[1] == "2005-03-15")])
        R.RECONSTRUCTIONS, R.RETRAITS = (), ()
        code, out = lancer(R.reparer, r)
        vrai = lire(r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        orig = [l for l in csv.DictReader(open(os.path.join(TEMOINS, "yahoo_2005.csv"), encoding="utf-8"))
                if l["valeur"] == "TOTALENERGIES" and l["date"] == "2005-03-15"][0]
        comble = [l for l in lire(r, R.SORTIE) if l["valeur"] == "TOTALENERGIES" and l["date"] == "2005-03-15"][0]
        def ajustement(l):
            l = [x for x in l if not (x[0] == "VINCI" and x[1] == "2005-06-15")]
            for x in l[1:]:
                if x[0] == "VINCI" and x[1] < "2005-06-15":
                    x[2:6] = [repr(float(c) * 0.97) for c in x[2:6]]
            return l
        r2 = racine_d_essai(abimer_yahoo=ajustement)
        code2, _ = lancer(R.reparer, r2)
        non = [j for j in lire(r2, R.JOURNAL) if j["valeur"] == "VINCI" and j["date"] == "2005-06-15"]
        res["H4"] = code == 0 and comble["source"] == "bnains" and len(vrai) > 7000 \
            and abs(float(comble["close"]) / float(orig["close"]) - 1) < 0.003 \
            and code2 == 0 and len(non) == 1 and non[0]["geste"] == "non comblé"
    except Exception:
        res["H4"] = False
    # H5 : référence instable
    try:
        r = racine_d_essai()
        R.RECONSTRUCTIONS = (("AXA", "2005-01-01", "2005-02-28", "2005-03-01", "2005-10-31", "épreuve"),)
        R.RETRAITS = ()
        code, out = lancer(R.reparer, r)
        res["H5"] = code == 1 and "trop courte ou instable" in out and not os.path.exists(os.path.join(r, R.SORTIE)) \
            and not os.path.exists(os.path.join(r, R.JOURNAL))
    except Exception:
        res["H5"] = False
    # H6 : témoin faux
    try:
        def abime(l):
            i = l[0].index("close")
            for x in l[1:]:
                if x[0] == "SUEZ":
                    x[i] = repr(float(x[i]) * 1.1)
            return l
        r = racine_d_essai(abimer_bnains=abime)
        R.RECONSTRUCTIONS, R.RETRAITS = (), (("ENGIE", "2005-07-08", "SUEZ", "épreuve"),)
        code, out = lancer(R.reparer, r)
        res["H6"] = code == 1 and "pas prouvées" in out and not os.path.exists(os.path.join(r, R.SORTIE))
    except Exception:
        res["H6"] = False
    # H15 : gardé ou retiré dans une fenêtre reconstruite
    try:
        sans = lambda l: [x for x in l if not (x[0] == "ESSILORLUXOTTICA" and x[1] == "2005-02-10")]
        r = racine_d_essai(abimer_bnains=sans)
        R.RECONSTRUCTIONS, R.RETRAITS = FENETRE_EL, ()
        lancer(R.reparer, r)
        hors_defait = lambda r_: [j for j in lire(r_, R.JOURNAL) if j["geste"] != "défait"]   # EssilorLuxottica est défait d'abord
        garde = [j for j in hors_defait(r) if j["valeur"] == "ESSILORLUXOTTICA" and j["date"] == "2005-02-10"]

        def faux_autour(l):
            for d in ("2005-02-03", "2005-02-04", "2005-02-07", "2005-02-08", "2005-02-09", "2005-02-11", "2005-02-14"):
                for c in ("open", "high", "low", "close"):
                    multiplier(l, "ESSILORLUXOTTICA", d, c, 1.05)
            return l
        r2 = racine_d_essai(abimer_yahoo=faux_autour, abimer_bnains=sans)
        lancer(R.reparer, r2)
        retire = [j for j in hors_defait(r2) if j["valeur"] == "ESSILORLUXOTTICA" and j["date"] == "2005-02-10"]
        r3 = racine_d_essai(
            abimer_yahoo=lambda l: [x for x in l if not (x[0] == "ESSILORLUXOTTICA" and x[1] == "2005-02-15")],
            abimer_bnains=lambda l: multiplier(l, "ESSILORLUXOTTICA", "2005-02-15", "volume", 0))
        lancer(R.reparer, r3)
        rien = [j for j in hors_defait(r3) if j["valeur"] == "ESSILORLUXOTTICA" and j["date"] == "2005-02-15"]
        code3, out3, _ = resultats_du_controle(K, r3, R.SORTIE)
        res["H15"] = len(garde) == 1 and garde[0]["geste"] == "gardé" and [j["geste"] for j in retire] == ["retiré", "non comblé"] \
            and [j["geste"] for j in rien] == ["non comblé"] and "inutilisable" in rien[0]["raison"] \
            and "ESSILORLUXOTTICA 2005-02-15 (bnains : barre sans échange ou incohérente)" in out3
    except Exception:
        res["H15"] = False
    # H12 : texte
    try:
        res["H12"] = R.texte(33.80) == "33.8" and R.texte(902383.0) == "902383" and R.texte(22.7838) == "22.7838"
    except Exception:
        res["H12"] = False
    # H13 : lignes de commande
    try:
        codes = []
        codes.append(lancer(K.main, [])[0])
        codes.append(lancer(R.main, [])[0])
        r = racine_d_essai()
        codes.append(lancer(K.main, [r, "donnees/absent.csv"])[0])
        os.remove(os.path.join(r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"))
        codes.append(lancer(R.main, [r])[0])
        r = racine_d_essai(abimer_bnains=lambda l: l + [["AXA", "2005-01-03", "x", "AXA", "a", "b", "c", "d", "e"]])
        codes.append(lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])[0])
        r = racine_d_essai(abimer_yahoo=lambda l: l + [list(l[1])])
        codes.append(lancer(R.main, [r])[0])
        r = racine_d_essai(abimer_yahoo=lambda l: [x[:6] for x in l])
        code_col, out_col = lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])
        r = racine_d_essai()
        open(os.path.join(r, "donnees/sources_bnains/DROITS_BNAINS.csv"), "w").write("valeur,date\n")
        code_dr, out_dr = lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])
        r = racine_d_essai()
        open(os.path.join(r, "donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv"), "w").write("valeur,jour\n")
        code_of, out_of = lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])
        r = racine_d_essai()
        open(os.path.join(r, "donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv"), "w").write("valeur,du,au\n")
        code_fa, out_fa = lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])
        code_fr, out_fr = lancer(R.main, [r])
        r = racine_d_essai()
        open(os.path.join(r, "donnees/sources_francfort/COURS_DE_FRANCFORT.csv"), "w").write("valeur,date,close\n")
        code_ff, out_ff = lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])
        code_fg, out_fg = lancer(R.main, [r])
        imprevues = []
        for prog in (getattr(K, "__file__", CONTROLE), getattr(R, "__file__", REPARATION)):
            r = racine_d_essai()
            open(os.path.join(r, "donnees/sources_yahoo/evenements.json"), "w").write("[]")
            p = subprocess.run([sys.executable, "-B", prog, r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"][:5 if "CONTROLER" in prog else 4],
                               capture_output=True, timeout=300)
            imprevues.append((p.returncode, "imprévue" in p.stdout.decode("utf-8")))
        res["H13"] = codes == [2, 2, 2, 2, 2, 2] and imprevues == [(2, True), (2, True)] \
            and code_col == 2 and "colonne(s) absente(s) ['volume']" in out_col and code_dr == 2 and "DROITS_BNAINS.csv" in out_dr \
            and code_of == 2 and "DETACHEMENTS_OFFICIELS.csv" in out_of \
            and code_fa == 2 and "BARRES_BNAINS_FAUSSES.csv" in out_fa and code_fr == 2 and "BARRES_BNAINS_FAUSSES.csv" in out_fr \
            and code_ff == 2 and "COURS_DE_FRANCFORT.csv" in out_ff and code_fg == 2 and "COURS_DE_FRANCFORT.csv" in out_fg
    except Exception:
        res["H13"] = False
    # H18 : nombres infinis ou indéfinis, clôture nulle
    try:
        def abime(l):
            multiplier(l, "ACCOR", "2005-02-01", "volume", float("nan"))
            multiplier(l, "ACCOR", "2005-02-02", "close", float("inf"))
            for c in ("open", "high", "low", "close"):
                multiplier(l, "LVMH", "2005-04-12", c, 0)
            return l
        r = racine_d_essai(abimer_yahoo=abime)
        code, out, k = resultats_du_controle(K, r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        res["H18"] = code == 1 and "REFUS" in k["K1"] and "infini ou indéfini" in out and "REFUS" in k["K2"] \
            and "LVMH 2005-04-12" in out
    except Exception:
        res["H18"] = False
    # H19 : rien à retirer
    try:
        r = racine_d_essai(abimer_yahoo=lambda l: [x for x in l if not (x[0] == "ENGIE" and x[1] < "2005-07-08")])
        R.RECONSTRUCTIONS, R.RETRAITS = (), (("ENGIE", "2005-07-08", "SUEZ", "épreuve"),)
        code, out = lancer(R.reparer, r)
        res["H19"] = code == 0 and "rien à retirer" in out
    except Exception:
        res["H19"] = False
    # H20 : K11 lacune, K12 fin, K13 absente, K14 début tardif
    try:
        dates_vinci = sorted(l[1] for l in csv.reader(open(os.path.join(TEMOINS, "yahoo_2005.csv"), encoding="utf-8"))
                             if l[0] == "VINCI")
        dix, neuf = set(dates_vinci[100:110]), set(dates_vinci[100:109])

        def abime(sans_vinci):
            return lambda l: [x for x in l if not (x[0] == "VINCI" and x[1] in sans_vinci)
                              and not (x[0] == "DANONE" and x[1] > "2005-09-01") and x[0] != "LVMH"
                              and not (x[0] == "ACCOR" and x[1] < "2005-03-01")]
        sans = lambda l: [x for x in l if not (x[0] == "VINCI" and x[1] in dix)]
        r = racine_d_essai(abimer_yahoo=abime(dix), abimer_bnains=sans)
        code, out, k = resultats_du_controle(K, r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        r2 = racine_d_essai(abimer_yahoo=abime(neuf), abimer_bnains=sans)
        code2, out2, k2 = resultats_du_controle(K, r2, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv")
        res["H20"] = "REFUS" in k["K11"] and f"VINCI à partir du {dates_vinci[100]}" in out and "REFUS" not in k2["K11"] \
            and "REFUS" in k["K12"] and "DANONE s'arrête le 2005-09-01" in out \
            and "REFUS" in k["K13"] and "LVMH : bnains l'archive jusqu'au 2005-10-31" in out \
            and "signalé" in k["K14"] and "ACCOR commence le 2005-03-01" in out
    except Exception:
        res["H20"] = False
    # H21 : une séance où le fichier n'a AUCUNE ligne reste une séance, parce que le calendrier officiel le dit, et la
    # réparation la comble depuis bnains (27-10-2026 : les cinq demi-séances, où Yahoo n'a aucune ligne, étaient tues).
    # H63 : toute séance laissée manquante a sa ligne « non comblé » au journal, et le registre de provenance porte
    # l'empreinte des deux fichiers écrits (décision de Jean-Luc du 27-10-2026 : « toute la mécanique de trace »).
    try:
        jour = "2005-03-10"
        r = racine_d_essai(abimer_yahoo=lambda l: [x for x in l if x[1] != jour])
        s, _, _ = K.lire_cours(os.path.join(r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"))
        b, _, _ = K.lire_cours(os.path.join(r, "donnees/sources_bnains/bnains_cac40.csv"), K.COURS_BNAINS)
        R.RECONSTRUCTIONS, R.RETRAITS = (), ()
        code, out = lancer(R.reparer, r)
        rep = {(l["valeur"], l["date"]): l["source"] for l in lire(r, R.SORTIE)}
        journal = lire(r, R.JOURNAL)
        attendues = {v for v in s if jour in b.get(v, {})}
        comblees = {v for v in attendues if rep.get((v, jour)) == "bnains"}
        non = {l["valeur"] for l in journal if l["geste"] == "non comblé" and l["date"] == jour}
        print(f"      H21 : {len(attendues)} valeurs attendues le {jour}, {len(comblees)} comblées, {len(non)} non comblées")
        res["H21"] = code == 0 and not any(jour in x for x in s.values()) and jour in K.calendrier(s, SEANCES) \
            and len(comblees) >= 20 and attendues - comblees <= non and not comblees & non
        apres, _, _ = K.lire_cours(os.path.join(r, R.SORTIE))
        manquantes = set(K.trous(apres, K.calendrier(apres, SEANCES)))
        tracees = {(l["valeur"], l["date"]) for l in journal if l["geste"] == "non comblé"}
        carnet = {l["fichier"]: l for l in lire(r, os.path.join("donnees", "PROVENANCE_DES_FICHIERS.csv"))}
        empreinte = lambda c: hashlib.sha256(open(os.path.join(r, c), "rb").read()).hexdigest()
        print(f"      H63 : {len(manquantes)} séances manquantes après la réparation, {len(tracees)} au journal")
        res["H63"] = code == 0 and manquantes == tracees and all(
            carnet[c.replace(os.sep, "/")]["sha256"] == empreinte(c) for c in (R.SORTIE, R.JOURNAL))
    except Exception as ex:
        print(f"      H21/H63 : {type(ex).__name__} : {ex}")
        res["H21"] = res["H63"] = False
    # H23 : recaler aux jours de détachement OFFICIELS, sur les vraies lignes de 2007 à 2010
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        six = ["CREDIT AGRICOLE SA", "DANONE", "MICHELIN", "PERNOD RICARD", "SOCIETE GENERALE", "VEOLIA"]
        # les actions gratuites de Pernod Ricard (2007, 2009), ajoutées le 09-10-2026 (A-555 ⑥), sont éprouvées
        # par H40 à H43 : H23 garde les cas du recalage pour lesquels elle a été écrite
        nouveaux = {("PERNOD RICARD", "2007-01-16"), ("PERNOD RICARD", "2009-11-18")}
        detache = {v: {d: x for d, x in jours.items() if (v, d) not in nouveaux}
                   for v, jours in K.lire_detachements(DROITS, OFFICIELS)[0].items() if v in six}

        def passe(abimer=None, abimer_b=None):
            y, b = reel(six, "2007-01-01", "2010-12-31")
            K.oter_les_barres_fausses(FAUSSES, b)
            if abimer:
                abimer(y)
            if abimer_b:
                abimer_b(b)
            sources, journal = {(v, d): "yahoo" for v, s in y.items() for d in s}, []
            n = R.recaler(y, sources, b, ev, detache, set(), journal)
            venues = {k for k, x in sources.items() if x == "bnains"}
            rang = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, venues, detache)}
            return n, {(j[0], j[1]): j[4] for j in journal}, rang["K15"]

        def brut(oter=True):              # sans recalage : le contrôle seul, sur les vraies lignes
            y, b = reel(six, "2007-01-01", "2010-12-31")
            if oter:
                K.oter_les_barres_fausses(FAUSSES, b)
            return {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, frozenset(), detache)}["K15"]

        def fois(valeur, jour, k):        # une barre Yahoo multipliée par k
            def abimer(s):
                o, h, l, c, x = s[valeur][jour]
                s[valeur][jour] = (o * k, h * k, l * k, c * k, x)
            return abimer

        def sans_volume(b):               # Société Générale : barre bnains du 20-02-2008 sans volume
            o, h, l, c, x = b["SOCIETE GENERALE"]["2008-02-20"]
            b["SOCIETE GENERALE"]["2008-02-20"] = (o, h, l, c, 0.0)
        juste, k15_brut, k15_avec_les_fausses = passe(), brut(), brut(oter=False)
        veille = passe(fois("DANONE", "2009-05-29", 1 / 1.06))     # Yahoo ajusterait Danone un jour trop tôt
        sg2009 = passe(fois("SOCIETE GENERALE", "2009-10-07", 1.03))   # écart, mais marche totale nulle
        trou = passe(abimer_b=sans_volume)

        def michelin(s):                  # la marche du jour annulée, et un écart dans la fenêtre : rien n'est recalé
            fois("MICHELIN", "2010-09-30", 1 / 1.0349)(s)
            fois("MICHELIN", "2010-09-28", 1.03)(s)
        sans_marche = passe(michelin)
        # la marche permise suit la règle officielle depuis le 10-10-2026 (décision de Jean-Luc, 09h39) : +5,5 % et
        # +6,8 % (dividende compris) au lieu de +5,3 % et +6,2 % tirés du cours du droit chez bnains
        sg2009_seul = ["SOCIETE GENERALE 2009-10-07→2009-10-08 rapport -0.0 %, le droit détaché n'en permet que +5.5 %"]
        res["H23"] = juste[0] == 1 and juste[1] == {("SOCIETE GENERALE", "2008-02-20"): 63.5677} \
            and juste[2] == [] and sg2009_seul[0] in k15_avec_les_fausses \
            and k15_brut == ["SOCIETE GENERALE 2008-02-19→2008-02-20 rapport -6.4 %",
                             "SOCIETE GENERALE 2008-02-20→2008-02-21 rapport +13.3 %, le droit détaché n'en permet que +6.8 %"]\
            and veille[0] == 2 and round(veille[1][("DANONE", "2009-05-29")], 2) == 33.15 \
            and sg2009[0] == 1 and ("SOCIETE GENERALE", "2009-10-07") not in sg2009[1] \
            and trou[0] == 0 and "SOCIETE GENERALE 2008-02-19→2008-02-20 rapport -6.4 %" in trou[2] \
            and sans_marche[0] == 1 and ("MICHELIN", "2010-09-28") not in sans_marche[1]
    except Exception:
        res["H23"] = False
    # H25 : les jours officiels — un manque, un jour impossible, la marche sans barre
    try:
        r = racine_d_essai()
        chemin = os.path.join(r, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv")
        lignes = list(csv.reader(open(chemin, encoding="utf-8", newline="")))
        garde = [l for l in lignes if l[0] not in ("DANONE", "MICHELIN")]
        # le droit de 2009 seulement : les actions gratuites de 2007 et 2009 (ajoutées le 09-10-2026) n'ont pas de
        # droit chez bnains, leur jour n'est donc jamais confronté à une première cotation
        tot = [l if l[:3] != ["PERNOD RICARD", l[1], "2009-04-16"] else l[:2] + ["2009-04-01"] + l[3:] for l in garde]
        tard = [l if l[:3] != ["PERNOD RICARD", l[1], "2009-04-16"] else l[:2] + ["2009-04-20"] + l[3:] for l in garde]
        sans_chiffres = [l if not l[1].startswith("AXA DS 2006") else l[:5] + ["", "", ""] for l in garde]
        illisible = [l if not l[1].startswith("AXA DS 2006") else l[:5] + ["24,47", "19.80", "9"] for l in garde]
        manques = {}
        for nom, contenu in (("tot", tot), ("tard", tard), ("sans_chiffres", sans_chiffres)):
            with open(chemin, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(contenu)
            det, manq = K.lire_detachements(os.path.join(r, "donnees", "sources_bnains", "DROITS_BNAINS.csv"), chemin)
            manques[nom] = (det, manq)
        with open(chemin, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(illisible)
        try:
            K.lire_detachements(os.path.join(r, "donnees", "sources_bnains", "DROITS_BNAINS.csv"), chemin)
            leve = False
        except ValueError as e:
            leve = "illisibles" in str(e)
        series = {"DANONE": {"2009-06-01": (1, 1, 1, 1, 1)}, "PERNOD RICARD": {"2009-06-01": (1, 1, 1, 1, 1)}}
        k16 = {num: cas for num, _, _, cas in cal_(K.controler)(series, [], {}, {}, frozenset(), manques["tot"][0],
                                                            manques["tot"][1])}["K16"]
        res["H25"] = sorted(v for v, _ in manques["tot"][1]) == ["DANONE", "MICHELIN", "PERNOD RICARD", "SUEZ"] \
            and any("PERNOD RICARD" in m and "2009-04-01 impossible" in m for _, m in manques["tot"][1]) \
            and any("PERNOD RICARD" in m and "2009-04-20 impossible" in m for _, m in manques["tard"][1]) \
            and any("DANONE" in m and "aucun jour officiel" in m for _, m in manques["tot"][1]) \
            and not {"2009-04-01", "2009-04-16"} & set(manques["tot"][0].get("PERNOD RICARD", {})) \
            and "SUEZ" not in manques["tot"][0] \
            and len(k16) == 2 and not any("MICHELIN" in m or "SUEZ" in m for m in k16) \
            and K.marche_permise({}, ("bnains", 0.413, "2009-11-11")) == 0.0 \
            and K.marche_permise({"2009-11-11": (0, 0, 0, 0, 1)}, ("bnains", 0.413, "2009-11-11")) == 0.0 \
            and round(K.marche_permise({"2009-11-11": (0, 0, 0, 16.725, 1)}, ("bnains", 0.413, "2009-11-11")), 4) == 0.0247 \
            and round(K.marche_permise({}, ("document", 24.47, 19.80, 9.0)), 4) == 0.0195 \
            and manques["tot"][0]["AXA"]["2006-06-19"] == ("document", 24.47, 19.8, 9.0) \
            and "2006-06-19" not in manques["sans_chiffres"][0].get("AXA", {}) \
            and any("ni droit chez bnains, ni chiffres du document" in m for _, m in manques["sans_chiffres"][1]) and leve
    except Exception:
        res["H25"] = False
    # H24 : autour_du_detachement, sur une série de dix séances
    try:
        dix = [f"2009-01-{j:02d}" for j in range(5, 15)]
        res["H24"] = K.autour_du_detachement(dix, dix[7]) == (dix[1], dix[2:7]) \
            and K.autour_du_detachement(dix, dix[3]) == (None, dix[0:3]) \
            and K.autour_du_detachement(dix, "2009-02-01") == (None, [])
    except Exception:
        res["H24"] = False
    # H26 : reconstruire divise le facteur aux détachements entre une date et la référence (AXA, juin 2006). Depuis le
    # 18-10-2026, le facteur écrit au journal (j[5]) est celui APPLIQUÉ aux prix, f / a / s, divisions comprises : H26
    # reste juste parce qu'AXA n'a aucune division après 2006 (s = 1 ; superviseur du 18-10-2026, E1 ④).
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        detache = {"AXA": K.lire_detachements(DROITS, OFFICIELS)[0]["AXA"]}

        def fenetre_2006(detachements):
            y, b = reel(["AXA"], "2006-01-01", "2009-11-09")
            sources, journal = {("AXA", d): "yahoo" for d in y["AXA"]}, []
            R.RECONSTRUCTIONS = (("AXA", "2006-01-01", "2006-12-31", "2008-01-01", "2009-11-09", "épreuve"),)
            with contextlib.redirect_stdout(io.StringIO()):
                arrets = cal_(R.reconstruire)(y, sources, b, ev, set(), journal, detachements)
            venues = {k for k, v in sources.items() if v == "bnains"}
            k15 = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, venues, detache)}["K15"]
            return arrets, {j[1]: j[5] for j in journal if j[2] == "reconstruit"}, k15
        avec, sans = fenetre_2006(detache), fenetre_2006(None)
        res["H26"] = avec[0] == [] and round(avec[1]["2006-06-16"] * 1.019456, 4) == round(avec[1]["2006-06-19"], 4) \
            and round(avec[1]["2006-06-19"], 4) == 0.9771 and not [c for c in avec[2] if "2006-06" in c] \
            and sans[1]["2006-06-16"] == sans[1]["2006-06-19"] \
            and [c for c in sans[2] if "2006-06" in c] == ["AXA 2006-06-16→2006-06-19 rapport +0.0 %, le droit détaché n'en permet que +1.9 %"]
    except Exception:
        res["H26"] = False
    # H27 : le fichier réparé du dépôt face aux cours extrêmes mensuels des rapports annuels
    try:
        officiel = {}
        for r in csv.DictReader(open(RAPPORTS, encoding="utf-8", newline="")):
            officiel[(r["valeur"], r["mois"])] = (float(r["plus_haut"]), float(r["plus_bas"]))
        extremes = {}
        for l in csv.reader(open(REPARE, encoding="utf-8", newline="")):
            if (l[0], l[1][:7]) in officiel:
                e = extremes.setdefault((l[0], l[1][:7]), [0.0, 1e9])
                e[0], e[1] = max(e[0], float(l[3])), min(e[1], float(l[4]))
        pires = {}
        for valeur, an in (("AXA", ""), ("ESSILORLUXOTTICA", "2000"), ("ESSILORLUXOTTICA", "2001")):
            r = [extremes[k][i] / officiel[k][i] for k in officiel if k[0] == valeur and k[1].startswith(an) for i in (0, 1)]
            m = statistics.median(r)
            pires[(valeur, an)] = (len(r), max(abs(x / m - 1) for x in r), round(m, 4))
        res["H27"] = pires[("AXA", "")][0] == 40 and pires[("AXA", "")][1] < 0.01 and pires[("AXA", "")][2] == 0.9771 \
            and all(n == 24 and e < 0.01 for (v, a), (n, e, m) in pires.items() if v == "ESSILORLUXOTTICA")
    except Exception:
        res["H27"] = False
    # H28 : les barres bnains prouvées fausses — retirées, et seulement elles ; fichier faux → ValueError ; K9 et K7
    try:
        y, b = reel(["SOCIETE GENERALE", "TOTALENERGIES"], "2009-01-01", "2016-12-31")
        avant = {v: set(x) for v, x in b.items()}
        otees = K.oter_les_barres_fausses(FAUSSES, b)
        sg = sorted(d for v, d in otees if v == "SOCIETE GENERALE")
        total = sorted(d for v, d in otees if v == "TOTALENERGIES")
        r = racine_d_essai()
        chemin = os.path.join(r, "donnees", "sources_bnains", "BARRES_BNAINS_FAUSSES.csv")
        lignes = list(csv.reader(open(FAUSSES, encoding="utf-8", newline="")))
        erreurs = []
        for contenu in ([["valeur", "du", "au"]],
                        [lignes[0], ["X", "2009-10-07", "2009-09-14", "s", "c", "m"]],
                        [lignes[0], ["X", "2009-13-01", "2009-12-01", "s", "c", "m"]]):
            with open(chemin, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(contenu)
            try:
                K.oter_les_barres_fausses(chemin, {})
                erreurs.append(None)
            except ValueError as e:
                erreurs.append(str(e))
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        tot = {"TOTALENERGIES": {d: x for d, x in y["TOTALENERGIES"].items() if "2016-06-01" <= d <= "2017-02-28"}}
        k_sans = {num: cas for num, _, _, cas in cal_(K.controler)(tot, [], b, ev)}
        k_avec = {num: cas for num, _, _, cas in cal_(K.controler)(tot, [], b, ev, fausses=otees)}
        res["H28"] = sg[0] == "2009-09-14" and sg[-1] == "2009-10-07" and len(sg) == 18 \
            and "2009-09-11" in b["SOCIETE GENERALE"] and "2009-10-08" in b["SOCIETE GENERALE"] \
            and total[0] == "2016-08-16" and total[-1] == "2016-12-20" and len(total) == 90 \
            and all(d in avant[v] for v, d in otees) and len(otees) == 108 \
            and erreurs[0] is not None and "en-tête" in erreurs[0] and erreurs[1] is not None and "finit le" in erreurs[1] \
            and erreurs[2] is not None \
            and k_sans["K9"] == ["TOTALENERGIES : 90"] and k_avec["K9"] == []
    except Exception:
        res["H28"] = False
    # H29 : ajuster — les droits que Yahoo a oubliés, et eux seuls, sur les vraies lignes
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        cinq = ["AIR LIQUIDE", "BNP PARIBAS", "MICHELIN", "SOCIETE GENERALE", "EURONEXT"]
        y, b = reel(cinq, "2006-01-01", "2021-12-31")
        K.oter_les_barres_fausses(FAUSSES, b)
        detache = {v: x for v, x in K.lire_detachements(DROITS, OFFICIELS)[0].items() if v in cinq}
        origine = {v: dict(x) for v, x in y.items()}
        k15_avant = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, frozenset(), detache)}["K15"]
        journal = []
        n, non_mesurables = R.ajuster(y, b, ev, detache, set(), journal)
        k15_apres = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, frozenset(), detache)}["K15"]
        m_bnp = K.marche_permise({}, ("document", 57.90, 40.0, 10.0))
        m_sg = K.marche_permise({}, ("document", 125.50, 108.0, 20.0))
        touches = {(j[0], j[1]) for j in journal}
        res["H29"] = n == 2 and non_mesurables == ["EURONEXT 2021-04-30"] \
            and abs(y["BNP PARIBAS"]["2009-09-29"][3] - origine["BNP PARIBAS"]["2009-09-29"][3] / (1 + m_bnp)) < 1e-9 \
            and abs(y["BNP PARIBAS"]["2009-09-29"][4] - origine["BNP PARIBAS"]["2009-09-29"][4] * (1 + m_bnp)) < 1e-6 \
            and y["BNP PARIBAS"]["2009-09-30"] == origine["BNP PARIBAS"]["2009-09-30"] \
            and abs(y["SOCIETE GENERALE"]["2006-09-29"][3] - origine["SOCIETE GENERALE"]["2006-09-29"][3] / (1 + m_sg)) < 1e-9 \
            and y["SOCIETE GENERALE"]["2006-10-02"] == origine["SOCIETE GENERALE"]["2006-10-02"] \
            and y["MICHELIN"] == origine["MICHELIN"] and y["AIR LIQUIDE"] == origine["AIR LIQUIDE"] \
            and not any(v in ("MICHELIN", "AIR LIQUIDE") for v, _ in touches) \
            and "BNP PARIBAS 2009-09-11→2009-09-30 rapport +0.0 %, le droit détaché n'en permet que +2.9 %" in k15_avant \
            and not [c for c in k15_apres if "→2009-09-30" in c or "→2006-10-02" in c]
    except Exception:
        res["H29"] = False
    # H30 : K15 et un jour de détachement qui n'est pas une séance comparable (Air Liquide, 14-09-2016)
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        y, b = reel(["AIR LIQUIDE"], "2016-01-01", "2016-12-31")
        K.oter_les_barres_fausses(FAUSSES, b)
        detache = {"AIR LIQUIDE": K.lire_detachements(DROITS, OFFICIELS)[0]["AIR LIQUIDE"]}
        rang = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, frozenset(), detache)}
        rang_sans = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, frozenset(), None)}
        res["H30"] = "2016-09-14" not in b["AIR LIQUIDE"] and rang["K15"] == [] \
            and not [c for c in rang["K15b"] if "2016-09" in c] \
            and [c for c in rang_sans["K15b"] if "2016-09" in c] == ["AIR LIQUIDE 2016-05-31→2016-09-15 rapport +2.7 %"]
    except Exception:
        res["H30"] = False
    # H31 : le fichier réparé du dépôt — le contrôle l'accepte, et il retrouve trois chiffres officiels
    try:
        code, out = lancer(K.main, [RACINE])
        rep_ = {}
        for l in csv.reader(open(REPARE, encoding="utf-8", newline="")):
            if l[0] in ("SOCIETE GENERALE", "BNP PARIBAS", "TOTALENERGIES") and "2009-09-01" <= l[1] <= "2016-12-31":
                rep_[(l[0], l[1])] = (float(l[2]), float(l[5]))
        _, bn = reel(["SOCIETE GENERALE"], "2009-09-11", "2009-09-11")
        facteur_sg = rep_[("SOCIETE GENERALE", "2009-09-11")][1] / bn["SOCIETE GENERALE"]["2009-09-11"][3]
        sg = rep_[("SOCIETE GENERALE", "2009-10-05")][1] / facteur_sg          # officiel : 52,20 (note d'opération)
        bnp = rep_[("BNP PARIBAS", "2009-09-28")][1] * (1 + K.marche_permise({}, ("document", 57.90, 40.0, 10.0)))   # 56,57
        ouv = [rep_[k][0] for k in sorted(rep_) if k[0] == "TOTALENERGIES" and k[1] < "2016-12-15"][-20:]
        total = sum(ouv) / 20                                                    # officiel : (41,87 + 0,61) / 0,95
        res["H31"] = code == 0 and "VERDICT : aucun contrôle bloquant n'a rien trouvé\n" in out \
            and abs(sg / 52.20 - 1) < 0.002 and abs(bnp / 56.57 - 1) < 0.0005 and abs(total / ((41.87 + 0.61) / 0.95) - 1) < 0.002
    except Exception:
        res["H31"] = False
    # H32 : la réparation entière, sur une copie des vrais fichiers, refait le fichier réparé du dépôt à l'octet
    try:
        r = tempfile.mkdtemp()
        for chemin in (R.ENTREE, K.BNAINS, K.EVENEMENTS, K.DROITS, K.OFFICIELS, K.FAUSSES, K.FRANCFORT, K.INDICE,
                       K.VERDICTS_YAHOO, K.CAL.FICHIER, K.PROVENANCE):   # + calendrier et registre : 27-10-2026
            os.makedirs(os.path.dirname(os.path.join(r, chemin)), exist_ok=True)
            shutil.copy(os.path.join(RACINE, chemin), os.path.join(r, chemin))
        R.RECONSTRUCTIONS, R.RETRAITS = reconstructions_vraies, retraits_vrais
        code_r, out_r = lancer(R.reparer, r)
        code_k, out_k = lancer(K.main, [r])
        empreinte = lambda c: hashlib.sha256(open(c, "rb").read()).hexdigest()
        res["H32"] = code_r == 0 and code_k == 1 and "VERDICT : REFUSÉ par K23\n" in out_k \
            and "programmes/REPARER_L_HISTORIQUE_LONG.py, qui n'est pas un programme du dépôt" in out_k and "ajustés : 14" in out_r and "défaits : 3," in out_r \
            and empreinte(os.path.join(r, R.SORTIE)) == empreinte(REPARE) \
            and empreinte(os.path.join(r, R.JOURNAL)) == empreinte(os.path.join(RACINE, R.JOURNAL))
    except Exception:
        res["H32"] = False
    # H33 : combler la veille d'un détachement officiel, au facteur d'avant (Crédit Agricole, 03-01-2007)
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        y, b = reel(["CREDIT AGRICOLE SA"], "2006-11-01", "2007-02-28")
        jours = K.lire_detachements(DROITS, OFFICIELS)[0]["CREDIT AGRICOLE SA"]
        sans = K.facteur_local(y, b, ev, "CREDIT AGRICOLE SA", "2007-01-03", set(), ())
        avec = K.facteur_local(y, b, ev, "CREDIT AGRICOLE SA", "2007-01-03", set(), (), jours)
        lendemain = K.facteur_local(y, b, ev, "CREDIT AGRICOLE SA", "2007-01-05", set(), (), jours)
        loin = K.facteur_local(y, b, ev, "CREDIT AGRICOLE SA", "2006-11-20", set(), (), {"2007-01-04": None})
        res["H33"] = "2007-01-03" not in y["CREDIT AGRICOLE SA"] and sans[0] is None and avec[0] is not None \
            and round(avec[0], 4) == 0.9090 and lendemain[0] is not None and round(lendemain[0], 4) == 0.9227 \
            and loin[0] is not None and round(loin[0], 4) == 0.9090
    except Exception:
        res["H33"] = False
    # H34 : la troisième source — avis de Francfort, barre sûre un jour douteux, barres démenties (septembre 2011)
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        F = K.lire_francfort(FRANCFORT)
        y, b = reel(["BNP PARIBAS", "SOCIETE GENERALE"], "2011-06-01", "2011-12-31")
        cas = {(c[0], c[1]): c[4] for c in K.barres_dementies(y, b, F, ev, set(), frozenset())}
        muets = {(c[0], c[1]): c[4] for c in K.barres_dementies(y, b, {}, ev, set(), frozenset())}
        _, bc = reel(["CARREFOUR"], "2007-05-01", "2007-09-30")
        avis = K.avis_de_francfort(F, bc, "CARREFOUR", "2007-07-05", {"2007-07-05"})
        sure = K.barre_sure(bc, F, "CARREFOUR", "2007-07-05", {"2007-07-05"})
        sans_f = K.barre_sure(bc, {}, "CARREFOUR", "2007-07-05", {"2007-07-05"})
        fige = dict(F["CARREFOUR"]); fige["2007-07-05"] = max(x for x in fige if x < "2007-07-05") and fige[max(x for x in fige if x < "2007-07-05")]
        res["H34"] = cas.get(("BNP PARIBAS", "2011-09-13")) == "fausse" and cas.get(("SOCIETE GENERALE", "2011-09-13")) == "fausse" \
            and muets.get(("BNP PARIBAS", "2011-09-13")) == "Francfort muet" \
            and avis[0] is not None and abs(avis[0]) <= avis[1] and sure and not sans_f \
            and K.avis_de_francfort({"CARREFOUR": fige}, bc, "CARREFOUR", "2007-07-05", set()) == (None, None)
    except Exception:
        res["H34"] = False
    # H35 : trancher sur les vraies lignes de septembre 2011 — le 13-09 remplacé, K17 vide après, plein avant
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        F = K.lire_francfort(FRANCFORT)
        y, b = reel(["BNP PARIBAS", "SOCIETE GENERALE"], "2011-06-01", "2011-12-31")
        k17_avant = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, frozenset(), None, (), frozenset(), F)}["K17"]
        sources, journal = {(v, d): "yahoo" for v, s_ in y.items() for d in s_}, []
        n = R.trancher(y, sources, b, F, ev, set(), {}, journal)
        venues = {k for k, x in sources.items() if x == "bnains"}
        k17_apres = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, venues, None, (), frozenset(), F)}["K17"]
        remplacees = {(j[0], j[1]): j[4] for j in journal if j[2] == "remplacé"}
        res["H35"] = n == len(remplacees) and n >= 2 and k17_apres == [] \
            and any(c.startswith("BNP PARIBAS 2011-09-13") for c in k17_avant) \
            and abs(remplacees[("BNP PARIBAS", "2011-09-13")] / 28.0 - 1) < 0.002 \
            and abs(remplacees[("SOCIETE GENERALE", "2011-09-13")] / 17.9 - 1) < 0.002 \
            and sources[("BNP PARIBAS", "2011-09-13")] == "bnains"
    except Exception:
        res["H35"] = False
    # H36 : l'arbitre de l'indice sur les vraies lignes de toutes les valeurs, 2009-2012
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        I = K.lire_indice(INDICE)
        toutes = sorted({l[0] for l in csv.reader(open(os.path.join(RACINE, R.ENTREE), encoding="utf-8"))} - {"valeur"})
        y, b = reel(toutes, "2009-11-01", "2012-02-29")
        K.oter_les_barres_fausses(FAUSSES, b)
        arb = {j: (ver, m) for j, n, _, _, _, m, ver in K.arbitre_de_l_indice(y, b, ev, I)}
        fenetre = [j for j in arb if "2011-09-07" in j]
        x = K.resoudre([[0.0, 2.0, 1.0], [1.0, 1.0, 0.0], [3.0, 0.0, 1.0]], [7.0, 3.0, 6.0])
        res["H36"] = arb.get(("2010-05-07",), (None, 0))[0] == "le fichier a tort" and arb[("2010-05-07",)][1] > 5 \
            and len(fenetre) == 1 and fenetre[0][0] == "2011-08-29" and fenetre[0][-1] == "2011-09-16" \
            and len(fenetre[0]) == 15 and arb[fenetre[0]][0] == "le fichier a tort" and arb[fenetre[0]][1] > 5 \
            and "2001-06-19" not in I and "2011-09-07" not in I and "2011-09-08" in I \
            and all(abs(a - e) < 1e-9 for a, e in zip(x, [1.0, 2.0, 3.0]))
    except Exception:
        res["H36"] = False
    # H37 : corriger sur les vraies lignes de septembre 2011 ; K18 et K19 avant et après
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        I, F = K.lire_indice(INDICE), K.lire_francfort(FRANCFORT)
        toutes = sorted({l[0] for l in csv.reader(open(os.path.join(RACINE, R.ENTREE), encoding="utf-8"))} - {"valeur"})
        y, b = reel(toutes, "2011-03-01", "2012-02-29")
        K.oter_les_barres_fausses(FAUSSES, b)
        origine = {v: dict(s_) for v, s_ in y.items()}
        jours = {d for j, *_, ver in K.arbitre_de_l_indice(y, b, ev, I) if ver == "le fichier a tort" for d in j}
        y9 = {v: dict(s_) for v, s_ in y.items()}
        src9 = {(v, d): "yahoo" for v, s_ in y9.items() for d in s_}
        with contextlib.redirect_stdout(io.StringIO()):
            R.trancher(y9, src9, b, F, ev, set(), {}, [])
        venues9 = {k for k, x in src9.items() if x == "bnains"}
        k18_9 = K.rendements_degrades(y9, origine, b, ev, venues9)
        reste9 = [c for c in K.barres_dementies(y9, b, F, ev, K.jours_douteux(K.ecarts(y9, b)), venues9) if c[4] == "fausse"]
        sources, journal = {(v, d): "yahoo" for v, s_ in y.items() for d in s_}, []
        n = R.corriger(y, sources, b, ev, jours, set(), {}, journal)
        venues = {k for k, x in sources.items() if x == "bnains"}
        apres = {num: cas for num, _, _, cas in cal_(K.controler)(y, [], b, ev, venues, None, (), frozenset(), F, I, origine)}
        avant = {num: cas for num, _, _, cas in cal_(K.controler)(origine, [], b, ev, frozenset(), None, (), frozenset(), F, I,
                                                            origine)}
        corr = {(j[0], j[1]): j[4] for j in journal if j[2] == "corrigé"}
        res["H37"] = len(jours) == 15 and n == len(corr) and n >= 100 \
            and abs(corr[("BNP PARIBAS", "2011-09-12")] / 26.12 - 1) < 0.002 \
            and abs(corr[("BNP PARIBAS", "2011-09-13")] / 28.00 - 1) < 0.002 \
            and abs(corr[("BNP PARIBAS", "2011-09-14")] / 26.90 - 1) < 0.002 \
            and ("HERMES INTL", "2011-09-14") not in corr and sources[("BNP PARIBAS", "2011-09-12")] == "bnains" \
            and any(c[:3] == ("BNP PARIBAS", "2011-09-12", "2011-09-13") for c in k18_9) and reste9 == [] \
            and apres["K18"] == [] and apres["K19"] == [] \
            and len(avant["K19"]) == 1 and avant["K19"][0].startswith("2011-08-29…2011-09-16")
    except Exception:
        res["H37"] = False
    # H38 : K18 sur trois séances fabriquées ; le contrôle sans l'indice rend 2
    try:
        def bar(c, vol=1000.0):
            return (c, c * 1.01, c * 0.99, c, vol)
        d1, d2, d3 = "2010-03-01", "2010-03-02", "2010-03-03"
        bn = {"Z": {d1: bar(100.0), d2: bar(102.0), d3: bar(100.0)},
              "P": {d1: bar(100.0), d2: bar(102.0), d3: (110.0, 110.0, 110.0, 110.0, 0.0)}}
        org = {"Z": {d1: bar(100.0), d2: bar(101.0), d3: bar(99.0)}, "P": {d1: bar(100.0), d2: bar(101.0), d3: bar(101.0)}}
        rep_ = {"Z": {d1: bar(100.0), d2: bar(102.0), d3: bar(99.0)}, "P": {d1: bar(100.0), d2: bar(102.0), d3: bar(101.0)}}
        cas = K.rendements_degrades(rep_, org, bn, {}, {("Z", d2), ("P", d2)})
        court, src_c, jr_c = {"Z": dict(org["Z"])}, {("Z", d): "yahoo" for d in org["Z"]}, []
        n_court = R.corriger(court, src_c, bn, {}, {d2}, set(), {}, jr_c)
        r = racine_d_essai()
        yahoo = os.path.join("donnees", "sources_yahoo", "yahoo_ohlcv_propre.csv")
        code_avec, _ = lancer(K.main, [r, yahoo])
        os.remove(os.path.join(r, "donnees", "sources_indice", "INDICE_CAC40.csv"))
        code, out = lancer(K.main, [r, yahoo])
        res["H38"] = [c[:3] for c in cas] == [("Z", d2, d3)] and abs(cas[0][4] - 0.0098) < 0.0002 \
            and code_avec in (0, 1) and code == 2 and "INDICE_CAC40" in out \
            and n_court == 0 and jr_c == [] and court["Z"][d2] == org["Z"][d2]
    except Exception:
        res["H38"] = False
    # H39 : défaire les deux erreurs de Yahoo (décision de Jean-Luc du 08-10-2026) — lecture, divisions, geste, K20
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        a_def = K.lire_a_defaire(VERDICTS)
        ev2 = K.sans_les_divisions_fausses(ev, a_def)
        nb = lambda e: sum(len(x.get("divisions", [])) for x in e.values())
        aca, el = "CREDIT AGRICOLE SA", "ESSILORLUXOTTICA"
        y, _ = reel([aca], "2018-05-14", "2018-05-31")
        org = {aca: dict(y[aca])}
        journal = []
        n = R.defaire(y, [x for x in a_def if x[0] == aca], journal)
        avant = [d for d in org[aca] if d < "2018-05-22"]
        f = 27 / 26
        juste = all(abs(y[aca][d][3] / org[aca][d][3] / f - 1) < 1e-12 and abs(y[aca][d][4] * f / org[aca][d][4] - 1) < 1e-12
                    for d in avant) and all(y[aca][d] == org[aca][d] for d in org[aca] if d >= "2018-05-22")
        k20 = lambda s: {num: cas for num, _, _, cas in cal_(K.controler)(s, [], {}, ev2, origine=org, a_defaire=[x for x in a_def if x[0] == aca])}["K20"]
        sans_vol = {aca: {d: (x[0], x[1], x[2], x[3], org[aca][d][4]) for d, x in y[aca].items()}}
        # les trois cassures de la relecture indépendante du 08-10-2026 : mauvais côté, moitié des lignes, clôture seule
        apres = {aca: {d: (tuple(c * f for c in x[:4]) + (x[4] / f,) if d >= "2018-05-22" else x) for d, x in y[aca].items()}}
        moitie = {aca: {d: (org[aca][d] if i % 2 else x) for i, (d, x) in enumerate(sorted(y[aca].items()))}}
        cloture = {aca: {d: (org[aca][d][:3] + (x[3],) + org[aca][d][4:] if d < "2018-05-22" else x) for d, x in y[aca].items()}}
        def illisible(texte):
            c = os.path.join(tempfile.mkdtemp(), "v.csv")
            open(c, "w", encoding="utf-8").write(texte)
            try:
                K.lire_a_defaire(c)
                return False
            except ValueError:
                return True
        tete = ",".join(K.AJUSTEMENTS_DE_YAHOO) + "\n"
        res["H39"] = a_def == [("ACCOR", "2010-07-02", 1 / 0.704727), (aca, "2018-05-22", 27 / 26), (el, "2024-05-06", 184.07 / 180.12)] \
            and ev2[aca]["divisions"] == [] and ev[aca]["divisions"] == [["2018-05-22", 27.0, 26.0]] \
            and nb(ev2) == nb(ev) - 1 and ev2[el] == ev[el] \
            and n == len(avant) == 6 and len(journal) == 6 and {j[2] for j in journal} == {"défait"} and juste \
            and k20(y) == [] and len(k20(org)) == 6 and len(k20(sans_vol)) == 6 and len(k20(apres)) == 8 \
            and len(k20(moitie)) == 3 and len(k20(cloture)) == 6 \
            and illisible(tete + "X,2018-05-22,d,v,s,c,27:26\n") and illisible(tete.replace("verdict", "jugement")) \
            and illisible(tete + "X,2018-05-22,d,v,s,c,27/26\nX,2018-05-22,d,v,s,c,2/1\n") \
            and illisible(tete + "X,2018-05-22,d,v,s,c,-27/26\n") and illisible(tete + "X,20180522,d,v,s,c,27/26\n") \
            and illisible(tete + "X,2018-05-22,d,v,s,c,nan/1\n") and illisible(tete + "X,2018-05-22,d,v,s,c,inf/1\n")
    except Exception:
        res["H39"] = False
    # H22 : la couture d'AXA, sur ses vraies lignes de 2008-2009
    try:
        ev = json.load(open(EVENEMENTS, encoding="utf-8"))
        detache = K.lire_detachements(DROITS, OFFICIELS)[0]

        def couture(fin, detachements):
            y, b = axa_reel()
            series, journal = {"AXA": y}, []
            sources = {("AXA", d): "yahoo" for d in y}
            R.RECONSTRUCTIONS = ((("AXA", "2008-06-01", fin) + tuple(axa_fenetre[0][3:])),)
            with contextlib.redirect_stdout(io.StringIO()):
                arrets = cal_(R.reconstruire)(series, sources, {"AXA": b}, ev, set(), journal)
            venues = {k for k, v in sources.items() if v == "bnains"}
            rang = {num: cas for num, _, _, cas in cal_(K.controler)(series, [], {"AXA": b}, ev, venues, detachements)}
            return arrets, sources, rang["K15"], rang["K15b"], series, venues, b
        juste = couture(axa_fenetre[0][2], detache)
        faux = couture("2009-11-10", detache)
        sans = couture(axa_fenetre[0][2], None)
        serie = dict(juste[4]["AXA"])
        o, h, l, c, v = serie["2009-03-12"]
        serie["2009-03-12"] = (o * 1.03, h * 1.03, l * 1.03, c * 1.03, v)        # deux lignes de bnains, l'une décalée
        interne = {num: cas for num, _, _, cas in cal_(K.controler)({"AXA": serie}, [], {"AXA": juste[6]}, ev, juste[5], detache)}
        basse = {d: ((o * 0.95, h * 0.95, l * 0.95, c * 0.95, x) if ("AXA", d) in juste[5] else (o, h, l, c, x))
                 for d, (o, h, l, c, x) in juste[4]["AXA"].items()}                # relecture de Cowork de 21h54
        trop_bas = {num: cas for num, _, _, cas in cal_(K.controler)({"AXA": basse}, [], {"AXA": juste[6]}, ev, juste[5], detache)}
        res["H22"] = axa_fenetre[0][2] == "2009-11-09" and juste[0] == [] and juste[1][("AXA", "2009-11-09")] == "bnains" \
            and juste[1][("AXA", "2009-11-10")] == "yahoo" \
            and juste[2] == [] and faux[2] == ["AXA 2009-11-09→2009-11-10 rapport +0.0 %, le droit détaché n'en permet que +2.3 %",
                                               "AXA 2009-11-10→2009-11-11 rapport +2.3 %"] \
            and sans[2] == ["AXA 2009-11-09→2009-11-10 rapport +2.3 %"] and juste[3] == [] \
            and detache.get("AXA") == {"2009-11-10": ("document", 16.95, 11.9, 12.0), "2006-06-19": ("document", 24.47, 19.8, 9.0),
                                       "2003-09-22": ("document", 16.84, 12.75, 16.0)} \
            and trop_bas["K15"] == ["AXA 2008-05-30→2008-06-02 rapport -5.0 %",
                                    "AXA 2009-11-09→2009-11-10 rapport +7.7 %, le droit détaché n'en permet que +2.3 %"] \
            and interne["K15"] == ["AXA 2009-03-11→2009-03-12 rapport +3.0 %", "AXA 2009-03-12→2009-03-13 rapport -2.9 %"]
    except Exception:
        res["H22"] = False
    # H40 : les opérations que Yahoo omet, lues dans les vrais fichiers (A-555 ⑥, 09-10-2026)
    try:
        det = K.lire_detachements(DROITS, OFFICIELS)[0]
        m = lambda v, d: K.marche_permise({}, det[v][d])
        res["H40"] = det["KERING"]["2013-06-20"] == ("distribution", 162.4, 2.50375) \
            and det["CARREFOUR"]["2011-07-05"] == ("distribution", 27.685, 3.4) \
            and det["PERNOD RICARD"]["2007-01-16"] == ("document", 171.8, 0.0, 5.0) \
            and abs(m("KERING", "2013-06-20") - 2.50375 / (162.4 - 2.50375)) < 1e-12 \
            and abs(1 / (1 + m("CARREFOUR", "2011-07-05")) - 0.877190) < 1e-6 \
            and abs(1 / (1 + m("LVMH", "2014-12-17")) - 0.900121) < 1e-6 \
            and abs(m("PERNOD RICARD", "2007-01-16") - 0.2) < 1e-12 \
            and abs(1 / (1 + m("TOTALENERGIES", "2006-05-18")) - 0.987143) < 1e-6
    except Exception:
        res["H40"] = False
    # H41 : une ligne de distribution ambiguë ou impossible est refusée, jamais lue de travers
    try:
        def refuse(ligne):
            r = tempfile.mkdtemp()
            o = os.path.join(r, "o.csv")
            lignes = list(csv.reader(open(OFFICIELS, encoding="utf-8", newline=""))) + [ligne]
            with open(o, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(lignes)
            try:
                K.lire_detachements(DROITS, o)
                return False
            except ValueError:
                return True
        base = ["ESSAI", "ESSAI distribution", "2010-01-04", "s", "c"]
        res["H41"] = refuse(base + ["50", "40", "", "5"]) and refuse(base + ["50", "", "", "50"]) \
            and refuse(base + ["", "", "", "5"]) and refuse(base + ["50", "", "", "x"]) and not refuse(base + ["50", "", "", "5"])
    except Exception:
        res["H41"] = False
    # H42 : K18 juge le rendement d'un jour de détachement droit compris (AXA, 22-09-2003, cassure du 09-10-2026)
    try:
        d0, d1, d2 = "2005-01-03", "2005-01-04", "2005-01-05"
        bn = {"Z": {d0: (99.0, 101.0, 98.0, 100.0, 1000.0), d1: (89.0, 91.0, 88.0, 90.0, 1000.0),
                    d2: (90.0, 92.0, 89.0, 91.0, 1000.0)}}
        org = {"Z": dict(bn["Z"])}                                    # Yahoo n'a pas ajusté la distribution
        f = 1 / (1 + 10 / 90)
        rep_ = {"Z": {d0: tuple(x * f for x in bn["Z"][d0][:4]) + (1000.0,), d1: bn["Z"][d1], d2: bn["Z"][d2]}}
        detache = {"Z": {d1: ("distribution", 100.0, 10.0)}}
        avec = K.rendements_degrades(rep_, org, bn, {}, {("Z", d0)}, detache)
        sans = K.rendements_degrades(rep_, org, bn, {}, {("Z", d0)})
        res["H42"] = avec == [] and len(sans) == 1 and sans[0][:3] == ("Z", d0, d1)
    except Exception:
        res["H42"] = False
    # H43 : une barre de Yahoo écartée sur décision est laissée au comblement, qui prend la barre de Paris
    try:
        r = racine_d_essai()
        garde = R.BARRES_YAHOO_ECARTEES
        R.RECONSTRUCTIONS, R.RETRAITS = (), ()        # l'extrait 2005 n'a pas la période de référence d'AXA
        R.BARRES_YAHOO_ECARTEES = (("VINCI", "2005-06-15", "essai"),)
        try:
            code, _ = lancer(R.reparer, r)
        finally:
            R.BARRES_YAHOO_ECARTEES = garde
        rep_ = {(l["valeur"], l["date"]): l for l in lire(r, "donnees/sources_yahoo/historique_long_repare.csv")}
        jr = [l for l in lire(r, "donnees/sources_yahoo/journal_des_reparations.csv") if l["valeur"] == "VINCI" and l["date"] == "2005-06-15"]
        res["H43"] = code == 0 and rep_[("VINCI", "2005-06-15")]["source"] == "bnains" \
            and [l["geste"] for l in jr] == ["écarté", "comblé"] \
            and R.BARRES_YAHOO_ECARTEES[0][:2] == ("PERNOD RICARD", "2007-01-15")
    except Exception:
        res["H43"] = False
    # H44 : relecture du 09-10-2026 — deux opérations un même jour, un doublon, un document impossible : refusés
    try:
        def refuse_44(*lignes):
            r = tempfile.mkdtemp()
            o = os.path.join(r, "o.csv")
            with open(o, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(list(csv.reader(open(OFFICIELS, encoding="utf-8", newline=""))) + list(lignes))
            try:
                K.lire_detachements(DROITS, o)
                return False
            except ValueError:
                return True
        vraies = list(csv.reader(open(OFFICIELS, encoding="utf-8", newline="")))
        lvmh = [l for l in vraies if l[0] == "LVMH" and l[2] == "2014-12-17"][0]
        doc = ["ESSAI", "ESSAI doc", "2010-01-04", "s", "c"]
        res["H44"] = refuse_44(["LVMH", "LVMH bis", "2014-12-17", "s", "c", "136.8", "", "", "1.0"]) \
            and refuse_44(lvmh) and refuse_44(doc + ["50", "60", "5", ""]) and refuse_44(doc + ["50", "0", "0", ""]) \
            and refuse_44(doc + ["50", "-1", "5", ""]) and refuse_44(doc + ["0", "0", "5", ""]) \
            and not refuse_44(doc + ["50", "0", "5", ""]) and not refuse_44(doc + ["50", "40", "10", ""])
    except Exception:
        res["H44"] = False
    # H45 : K18 voit une vraie dégradation le jour d'un détachement que Yahoo n'avait pas ajusté
    try:
        d0, d1, d2 = "2005-01-03", "2005-01-04", "2005-01-05"
        bn = {"Z": {d0: (99.0, 101.0, 98.0, 100.0, 1000.0), d1: (89.0, 91.0, 88.0, 90.0, 1000.0),
                    d2: (90.0, 92.0, 89.0, 91.0, 1000.0)}}
        org = {"Z": dict(bn["Z"])}
        f = 1 / (1 + 10 / 90)
        abime = {"Z": {d0: tuple(x * f * 1.05 for x in bn["Z"][d0][:4]) + (1000.0,), d1: bn["Z"][d1], d2: bn["Z"][d2]}}
        cas = K.rendements_degrades(abime, org, bn, {}, {("Z", d0)}, {"Z": {d1: ("distribution", 100.0, 10.0)}})
        res["H45"] = len(cas) == 1 and cas[0][:3] == ("Z", d0, d1)
    except Exception:
        res["H45"] = False
    # H46 : une barre écartée que bnains ne peut pas combler arrête la réparation, rien n'est écrit
    try:
        def sans_vinci(lignes):
            return [l for l in lignes if not (l[0] == "VINCI" and l[1] == "2005-06-15")]
        r = racine_d_essai(abimer_bnains=sans_vinci)
        garde = R.BARRES_YAHOO_ECARTEES
        R.RECONSTRUCTIONS, R.RETRAITS = (), ()
        R.BARRES_YAHOO_ECARTEES = (("VINCI", "2005-06-15", "essai"),)
        try:
            code, out = lancer(R.reparer, r)
        finally:
            R.BARRES_YAHOO_ECARTEES = garde
        res["H46"] = code == 1 and "VINCI 2005-06-15" in out and "rien n'est écrit" in out \
            and not os.path.exists(os.path.join(r, "donnees", "sources_yahoo", "historique_long_repare.csv"))
    except Exception:
        res["H46"] = False
    # H47 : K21 juge le jour des opérations déclarées sur les VRAIS cours de bnains (décision de Jean-Luc du
    # 09-10-2026 à 12h28 ; seconde relecture indépendante du même jour) — la vraie table passe, AXA 2003 seule
    # non tranchée sans jour écrit, acceptée (K21c) ; chaque opération chiffrée décalée de ±1 à ±3 séances : 35
    # refusées, 82 signalées, 3 acceptées (mesuré le 09-10-2026 à 21h, avec Accor 2010 — avant elle : 29, 82, 3) ;
    # 47, 82, 3 depuis le 10-10-2026, avec les deux actions gratuites de Sagem (2000 et 2003), dont les 12 décalages
    # sont refusés ; les rendements sont ramenés par les divisions de Yahoo (`ev`) ; 58, 119, 3 depuis la règle officielle
    # (10-10-2026, 09h39) : huit droits de bnains deviennent « document », donc jugés (32 opérations) ; Carrefour décalé d'une séance (le cas de la
    # relecture, +9,70 % accepté le 06-07-2011) et Carrefour un dimanche sont refusés, et controler() les range en
    # K21, bloquant ; un jour « 20110705 » est refusé à la lecture
    try:
        b, _, _ = K.lire_cours(os.path.join(RACINE, "donnees", "sources_bnains", "bnains_cac40.csv"), K.COURS_BNAINS)
        K.oter_les_barres_fausses(FAUSSES, b)
        det, _ = K.lire_detachements(DROITS, OFFICIELS)
        cit = K.lire_citations(OFFICIELS)
        ev = K.sans_les_divisions_fausses(json.load(open(EVENEMENTS, encoding="utf-8")),
                                          K.lire_a_defaire(os.path.join(RACINE, K.VERDICTS_YAHOO)))
        c, n, ac, jugees = K.dates_declarees(b, det, cit, ev)
        seances = sorted({d for s in b.values() for d in s})
        rang = {d: i for i, d in enumerate(seances)}
        compte, acceptes = {"refusé": 0, "signalé": 0, "accepté": 0}, []
        for v in sorted(det):
            for jour, droit in sorted(det[v].items()):
                if droit[0] not in ("document", "distribution") or jour not in rang:
                    continue
                for k in (-3, -2, -1, 1, 2, 3):
                    nj = seances[rang[jour] + k]
                    d2 = {w: dict(x) for w, x in det.items()}
                    del d2[v][jour]
                    d2[v][nj] = droit
                    c2 = dict(cit)
                    c2[(v, nj)] = cit.get((v, jour), "")
                    cc, nn, _, _ = K.dates_declarees(b, d2, c2, ev)
                    if any(x.startswith(f"{v} {nj} ") for x in cc):
                        compte["refusé"] += 1
                    elif any(x.startswith(f"{v} {nj} ") for x in nn):
                        compte["signalé"] += 1
                    else:
                        compte["accepté"] += 1
                        acceptes.append(f"{v} {jour}{k:+d}")

        def table(changer):
            lignes = list(csv.reader(open(OFFICIELS, encoding="utf-8", newline="")))
            for l in lignes:
                if l[0] == "CARREFOUR" and l[2] == "2011-07-05":
                    l[2] = changer
            o = os.path.join(tempfile.mkdtemp(), "o.csv")
            with open(o, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(lignes)
            return o
        o = table("2011-07-06")
        det2, _ = K.lire_detachements(DROITS, o)
        c2, n2, _, _ = K.dates_declarees(b, det2, K.lire_citations(o), ev)
        o3 = table("2011-07-03")
        det3, _ = K.lire_detachements(DROITS, o3)
        c3, _, _, _ = K.dates_declarees(b, det3, K.lire_citations(o3), ev)
        garde = K.JOURS_ACCEPTES
        try:
            K.JOURS_ACCEPTES = (("AXA", "2003-09-23", "essai"),)
            _, n4, ac4, _ = K.dates_declarees(b, det, cit, ev)
            # une opération acceptée reste jugée par la mesure : Carrefour décalé et accepté part en K21
            K.JOURS_ACCEPTES = garde + (("CARREFOUR", "2011-07-06", "essai"),)
            c5, _, ac5, _ = K.dates_declarees(b, det2, K.lire_citations(o), ev)
            # en double, et sans emploi (LVMH 2014 est tranchée par la mesure)
            K.JOURS_ACCEPTES = garde + garde + (("LVMH", "2014-12-17", "essai"),)
            _, n6, _, _ = K.dates_declarees(b, det, cit, ev)
            # une table lue mais vide : l'exception n'a plus d'objet
            K.JOURS_ACCEPTES = garde
            _, n7, _, _ = K.dates_declarees(b, {}, {})
        finally:
            K.JOURS_ACCEPTES = garde
        k = {x[0]: x for x in cal_(K.controler)({}, [], b, ev, frozenset(), det2, (), frozenset(), None, None, None, (),
                                          K.lire_citations(o))}
        try:
            K.lire_detachements(DROITS, table("20110705"))
            iso = False
        except ValueError:
            iso = True
        res["H47"] = c == [] and n == [] and [x.split(" :")[0] for x in ac] == ["AXA 2003-09-22"] and jugees == 32 \
            and [x.split(" :")[0] for x in n4] == ["AXA 2003-09-22", "AXA 2003-09-23"] and ac4 == [] \
            and [x.split(" :")[0] for x in c5] == ["CARREFOUR 2011-07-06"] \
            and not any(x.startswith("CARREFOUR") for x in ac5) \
            and [(x.split(" :")[0], "deux fois" in x, "sans emploi" in x) for x in n6] == \
                [("AXA 2003-09-22", True, False), ("LVMH 2014-12-17", False, True)] \
            and [x.split(" :")[0] for x in n7] == ["AXA 2003-09-22"] \
            and compte == {"refusé": 58, "signalé": 119, "accepté": 3} \
            and acceptes == ["AIR LIQUIDE 2016-09-14-3", "BNP PARIBAS 2006-03-07-1", "BNP PARIBAS 2009-09-30-2"] \
            and [x.split(" :")[0] for x in c2] == ["CARREFOUR 2011-07-06"] and n2 == n \
            and [x.split(" :")[0] for x in c3] == ["CARREFOUR 2011-07-03"] and "pas une séance" in c3[0] \
            and k["K21"][2] is True and len(k["K21"][3]) == 1 and k["K21b"][2] is True and k["K21b"][3] == [] \
            and k["K21c"][2] is False and len(k["K21c"][3]) == 1 and iso \
            and K.dates_declarees(b, det, None, ev)[:2] == ([], [])
    except Exception:
        res["H47"] = False
    # H48 : jour_ecrit() lit le jour dans la phrase citée (entre « »), en lettres ou en chiffres, et pas un jour
    # voisin, ni une date écrite hors des « » (« Cours de la veille : … »), ni un nombre plus long
    try:
        res["H48"] = all(K.jour_ecrit(c, j) == att for c, j, att in (
            ("« Ex-rights date..................July 4,.2002 »", "2002-07-04", True),
            ("« commencera le 1er juin 2009 »", "2009-06-01", True), ("« débuteront le 02 juin 2014 »", "2014-06-02", True),
            ("« On June 20, 2013 prior to the start of market »", "2013-06-20", True),
            ("« Ex-rights Date: 30 April 2021 »", "2021-04-30", True),
            ("« La période commencera le 23 février 2009 »", "2009-02-23", True),
            ("« séance du 05-07-2011 »", "2011-07-05", True),
            ("« le 2 octobre 2006 »", "2006-10-03", False), ("« le 12 octobre 2006 »", "2006-10-02", False),
            ("Communiqués des 04 et 05-07-2011 : « une action DIA »", "2011-07-05", False),
            ("« une action » Cours de la veille : clôture du 04-07-2011 chez bnains", "2011-07-04", False),
            ("« séance du 2009-06-011 »", "2009-06-01", False), ("« le 19 septembre 2003 »", "2003-09-22", False)))
    except Exception:
        res["H48"] = False
    # H49 : un extrait bnains vide arrête le contrôle, code 2 — il ne peut pas juger (R-734)
    try:
        r = racine_d_essai(abimer_bnains=lambda lignes: lignes[:1])
        code, out = lancer(K.main, [r, "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"])
        res["H49"] = code == 2 and "bnains est vide" in out
    except Exception:
        res["H49"] = False
    # H50 : K20 juge une correction défaite remplacée le même jour par une opération déclarée — de type « document »
    # comme « distribution » (relecture indépendante du 09-10-2026 : la branche « document » n'était éprouvée par rien)
    try:
        jours = ["2005-03-01", "2005-03-02", "2005-03-03", "2005-03-04"]
        org = {"Z": {d: (100.0, 101.0, 99.0, 100.0, 1000.0) for d in jours}}
        f = 1.25
        cas = {"document": ("document", 100.0, 80.0, 4.0), "distribution": ("distribution", 100.0, 20.0)}
        bon = True
        for nom, droit in cas.items():
            g = f / (1 + K.marche_permise({}, droit))
            juste = {"Z": {d: (tuple(x * (g if d < "2005-03-03" else 1) for x in v[:4]) + (v[4] / (g if d < "2005-03-03" else 1),))
                           for d, v in org["Z"].items()}}
            seul = {"Z": {d: (tuple(x * (f if d < "2005-03-03" else 1) for x in v[:4]) + (v[4] / (f if d < "2005-03-03" else 1),))
                          for d, v in org["Z"].items()}}
            det = {"Z": {"2005-03-03": droit}}
            a_def = [("Z", "2005-03-03", f)]
            bon = bon and K.portes(juste, org, a_def, frozenset(), det) == [] \
                and len(K.portes(seul, org, a_def, frozenset(), det)) == 2 \
                and len(K.portes(juste, org, a_def, frozenset(), {"Z": {"2005-03-04": droit}})) == 2
        res["H50"] = bon
    except Exception:
        res["H50"] = False
    # H51 : K21 ramène les rendements de bnains par les divisions de Yahoo (10-10-2026). Sagem, 10-07-2000 :
    # Yahoo déclare une division par 3 et la table déclare une action gratuite pour cinq, le même jour ; le cours
    # brut passe de 1 287 € à 331 €. Sans les divisions, K21 contredit le jour ; avec, il le confirme. Et le contrôle
    # entier, sur les vrais fichiers, les lui passe (sinon K21 refuse le dépôt).
    try:
        b, _, _ = K.lire_cours(os.path.join(RACINE, "donnees", "sources_bnains", "bnains_cac40.csv"), K.COURS_BNAINS)
        K.oter_les_barres_fausses(FAUSSES, b)
        det, _ = K.lire_detachements(DROITS, OFFICIELS)
        cit = K.lire_citations(OFFICIELS)
        ev = K.sans_les_divisions_fausses(json.load(open(EVENEMENTS, encoding="utf-8")),
                                          K.lire_a_defaire(os.path.join(RACINE, K.VERDICTS_YAHOO)))
        seul = {"SAFRAN": {"2000-07-10": det["SAFRAN"]["2000-07-10"]}}
        sans, _, _, j1 = K.dates_declarees(b, seul, cit)
        avec, _, _, j2 = K.dates_declarees(b, seul, cit, ev)
        code_k, out_k = lancer(K.main, [RACINE])
        res["H51"] = [x.split(" :")[0] for x in sans] == ["SAFRAN 2000-07-10"] and avec == [] and j1 == j2 == 1 \
            and code_k == 0 and "VERDICT : aucun contrôle bloquant n'a rien trouvé\n" in out_k and "K21 ok" in out_k
    except Exception:
        res["H51"] = False
    # H52 : la règle officielle à la lecture (décision de Jean-Luc du 10-10-2026, 09h39) — un droit vu chez bnains dont
    # la ligne officielle porte ses chiffres se lit « document » (Danone 2009 : +5,976 %, le facteur de Yahoo) ; sans
    # ses chiffres, il reste « bnains » (le cours du droit, 2,19 €) ; le dividende non attaché s'ajoute au prix (Société
    # Générale 2008 : 47,50 + 0,90) et se refuse sur une distribution ; « du 10 au 23 novembre 2009 » écrit le 10.
    try:
        b, _, _ = K.lire_cours(os.path.join(RACINE, "donnees", "sources_bnains", "bnains_cac40.csv"), K.COURS_BNAINS)
        det = K.lire_detachements(DROITS, OFFICIELS)[0]

        def table(changer):
            lignes = list(csv.reader(open(OFFICIELS, encoding="utf-8", newline="")))
            for l in lignes[1:]:
                changer(l)
            o = os.path.join(tempfile.mkdtemp(), "o.csv")
            with open(o, "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(lignes)
            return o

        def blanchir(l):
            if l[0] == "DANONE" and l[2] == "2009-06-01":
                l[5] = l[6] = l[7] = ""

        def dividende_sur_distribution(l):
            if l[0] == "KERING" and l[2] == "2013-06-20":
                l[9] = "0.5"
        sans_chiffres = K.lire_detachements(DROITS, table(blanchir))[0]
        try:
            K.lire_detachements(DROITS, table(dividende_sur_distribution))
            leve = False
        except ValueError:
            leve = True
        res["H52"] = det["DANONE"]["2009-06-01"] == ("document", 35.13, 24.73, 4.25) \
            and abs(K.marche_permise({}, det["DANONE"]["2009-06-01"]) - 0.059759) < 1e-6 \
            and det["SOCIETE GENERALE"]["2008-02-21"] == ("document", 71.15, 47.5 + 0.9, 4.0) \
            and abs(K.marche_permise({}, det["SOCIETE GENERALE"]["2008-02-21"]) - 0.068318) < 1e-6 \
            and sans_chiffres["DANONE"]["2009-06-01"] == ("bnains", 2.19, "2009-06-02") and leve \
            and K.jour_ecrit("« du 10 au 23 novembre 2009 inclus »", "2009-11-10") \
            and not K.jour_ecrit("« du 10 au 23 novembre 2009 inclus »", "2009-11-11") \
            and not K.jour_ecrit("du 10 au 23 novembre 2009", "2009-11-10")
    except Exception:
        res["H52"] = False
    # H53 : `aligner` ramène à la règle officielle les droits que Yahoo a ajustés autrement, sur les vraies lignes de
    # 2005 à 2010 : BNP Paribas 2006, Crédit Agricole 2007, Schneider Electric 2007, Société Générale 2008 (après
    # `recaler`) — pas Danone ni Vinci 2006, où Yahoo suit la règle (Vinci : dividende de 2005 non attaché compris,
    # relecture indépendante du 10-10-2026), ni Société Générale 2006, que Yahoo n'a pas ajusté (c'est l'affaire
    # d'`ajuster`) ; un second passage ne change rien ; une ligne de Vinci ne bouge pas ; une ligne de Crédit Agricole
    # d'avant le 04-01-2007 est multipliée par 1,015141 ÷ 1,016394.
    try:
        ev = K.sans_les_divisions_fausses(json.load(open(EVENEMENTS, encoding="utf-8")),
                                          K.lire_a_defaire(os.path.join(RACINE, K.VERDICTS_YAHOO)))
        quatre = ["BNP PARIBAS", "CREDIT AGRICOLE SA", "DANONE", "SCHNEIDER ELECTRIC", "SOCIETE GENERALE", "VINCI"]
        det = {v: x for v, x in K.lire_detachements(DROITS, OFFICIELS)[0].items() if v in quatre}
        y, b = reel(quatre, "2005-01-01", "2010-12-31")
        K.oter_les_barres_fausses(FAUSSES, b)
        avant, avant_ca = y["VINCI"]["2006-03-28"][3], y["CREDIT AGRICOLE SA"]["2007-01-02"][3]
        sources, journal = {(v, d): "yahoo" for v, s_ in y.items() for d in s_}, []
        R.recaler(y, sources, b, ev, det, set(), journal)
        n, mesures = R.aligner(y, b, ev, det, set(), journal)
        n2, _ = R.aligner(y, b, ev, det, set(), [])
        alignes = sorted({(j[0], j[6].split("détaché le ")[1].split(" ")[0]) for j in journal if j[2] == "aligné"})
        res["H53"] = n == 4 and n2 == 0 and alignes == [("BNP PARIBAS", "2006-03-07"), ("CREDIT AGRICOLE SA", "2007-01-04"),
                                                         ("SCHNEIDER ELECTRIC", "2007-03-12"),
                                                         ("SOCIETE GENERALE", "2008-02-21")] \
            and y["VINCI"]["2006-03-28"][3] == avant \
            and abs(y["CREDIT AGRICOLE SA"]["2007-01-02"][3] / avant_ca - 1.015141 / 1.016394) < 2e-5 \
            and any(v == "DANONE" for v, *_ in mesures)
    except Exception:
        res["H53"] = False
    # H54 : K20 attend, sur une ligne alignée, le facteur que le journal écrit pour elle (relecture indépendante du
    # 10-10-2026 : ne juger que depuis la dernière opération laissait passer un fichier faux de 0,5 %) ; sans le
    # journal, la ligne est signalée, jamais acceptée ; lire_alignes ne garde que le geste « aligné ».
    try:
        org = {"Z": {"2005-03-01": (10, 10, 10, 10, 100), "2005-03-02": (10, 10, 10, 10, 100),
                     "2005-03-03": (10, 10, 10, 10, 100)}}
        f, q = 1.04, 0.99
        juste = {"Z": {"2005-03-01": tuple(x * f * q for x in (10, 10, 10, 10)) + (100 / (f * q),),
                       "2005-03-02": tuple(x * f for x in (10, 10, 10, 10)) + (100 / f,),
                       "2005-03-03": (10, 10, 10, 10, 100)}}
        a_def = [("Z", "2005-03-03", f)]
        r = tempfile.mkdtemp()
        j = os.path.join(r, "j.csv")
        with open(j, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(R.CHAMPS_JOURNAL)
            w.writerow(["Z", "2005-03-01", "aligné", 1, 1, q, "essai", 1 / q, "ligne"])
            w.writerow(["Z", "2005-03-02", "ajusté", 1, 1, 0.5, "essai", 2.0, "ligne"])
        al = K.lire_alignes(j)
        res["H54"] = al == {("Z", "2005-03-01"): q} and K.portes(juste, org, a_def, frozenset(), None, al) == [] \
            and len(K.portes(juste, org, a_def, frozenset(), None, None)) == 1 \
            and K.lire_alignes(os.path.join(r, "absent.csv")) == {}
    except Exception:
        res["H54"] = False
    # H55 : K22 (relecture indépendante du 10-10-2026) — sur le vrai fichier réparé, chaque opération déclarée que
    # bnains mesure porte la règle officielle à 0,05 % près ; Vinci 2006 décalé de +0,25 % avant le 30-03-2006 (le
    # premier jet d'`aligner`) est refusé, nommé ; Euronext 2021 ne se mesure pas (bnains s'arrête en 2017).
    try:
        f, _, _ = K.lire_cours(REPARE)
        b, _, _ = K.lire_cours(os.path.join(RACINE, "donnees", "sources_bnains", "bnains_cac40.csv"), K.COURS_BNAINS)
        K.oter_les_barres_fausses(FAUSSES, b)
        ev = K.sans_les_divisions_fausses(json.load(open(EVENEMENTS, encoding="utf-8")),
                                          K.lire_a_defaire(os.path.join(RACINE, K.VERDICTS_YAHOO)))
        det = K.lire_detachements(DROITS, OFFICIELS)[0]
        juste = K.marches_inexactes(f, b, ev, det, set())
        faux = {v: dict(x) for v, x in f.items()}
        for d, (o, h, l, c, x) in list(faux["VINCI"].items()):
            if d < "2006-03-30":
                faux["VINCI"][d] = (o * 1.0025, h * 1.0025, l * 1.0025, c * 1.0025, x / 1.0025)
        refuse = K.marches_inexactes(faux, b, ev, det, set())
        res["H55"] = juste == [] and [x.split(" :")[0] for x in refuse] == ["VINCI 2006-03-30"] \
            and K.marche_mesuree(f["EURONEXT"], b.get("EURONEXT", {}), ev, "EURONEXT", "2021-04-30", set()) is None
    except Exception:
        res["H55"] = False
    # H56 : K23, le rejeu, sur les vrais fichiers (A-578 ; superviseurs R-759 et relecture du 18-10-2026) — le fichier
    # réparé du dépôt se refait en entier, à l'égalité exacte ; et chaque abîme d'UNE vraie ligne est vu, seul, PAR LE
    # CONTRÔLE QU'IL GARDE : on vérifie la ligne ET le motif (un abîme vu par un autre contrôle laissait un sabotage
    # sans dents — relecture du 18-10-2026, X1).
    try:
        s_, _, _ = K.lire_cours(REPARE)
        src_ = K.lire_les_sources(REPARE)
        p_, _, _ = K.lire_paris(RACINE)               # le Paris même de la réparation et de `main` (R-708)
        brut_, _, _ = K.lire_cours(os.path.join(RACINE, K.BNAINS), K.COURS_BNAINS)     # avec les barres fausses
        o_, _, _ = K.lire_cours(os.path.join(RACINE, K.ORIGINE))
        j_ = K.lire_journal(os.path.join(RACINE, K.JOURNAL))
        rejeu = lambda s=s_, src=src_, j=j_: K.lignes_non_rejouees(s, src, o_, p_, j)
        tout = rejeu()

        def cellule(valeur, date, i, f):
            s = {v: dict(x) for v, x in s_.items()}
            b = list(s[valeur][date])
            b[i] = f(b[i])
            s[valeur][date] = tuple(b)
            return rejeu(s=s)

        def sans(valeur, date):
            s = {v: dict(x) for v, x in s_.items()}
            del s[valeur][date]
            return rejeu(s=s)

        def geste(valeur, date, nom, champ, nouveau):
            j = dict(j_)
            j[(valeur, date)] = [dict(g, **{champ: nouveau}) if g["geste"] == nom else g for g in j_[(valeur, date)]]
            return rejeu(j=j)

        def ordre(valeur, date, f):
            j = dict(j_)
            j[(valeur, date)] = f(list(j_[(valeur, date)]))
            return rejeu(j=j)
        def sur_barre_fausse(valeur, date):       # relecture n° 2 du 18-10-2026, B1 : la ligne refaite depuis une barre
            s = {v: dict(x) for v, x in s_.items()}   # de Paris prouvée fausse, avec un geste « corrigé » cohérent
            e, pb = s_[valeur][date], brut_[valeur][date]
            n = K.arrondir(pb, e[3] / pb[3], e[4] / pb[4])
            s[valeur][date] = n
            j = dict(j_)
            j[(valeur, date)] = j_.get((valeur, date), []) + [dict(
                valeur=valeur, date=date, geste="corrigé", close_avant=repr(e[3]), close_apres=repr(n[3]),
                facteur=repr(e[3] / pb[3]), raison="abîme", facteur_volume=repr(e[4] / pb[4]), depart="paris")]
            return rejeu(s=s, src={**src_, (valeur, date): K.SOURCE_PARIS}, j=j)
        accor, al, hermes = ("ACCOR", "2000-01-03"), ("AIR LIQUIDE", "2000-01-04"), ("HERMES INTL", "2025-02-14")
        engie = ("ENGIE", "2000-01-03")                 # « retiré » : Yahoo y mettait les cours de Suez (RETRAITS)
        ajoute = lambda g: dict(g, geste="corrigé", raison="geste inventé", facteur="1.0", facteur_volume="1.0")
        abimes = {      # nom : (cas obtenus, ligne attendue, fragment attendu du motif)
            "Hermès ouverture + 0,01 €": (cellule(*hermes, 0, lambda x: x + 0.01), hermes, "ouverture : le fichier a"),
            "Hermès ouverture + 0,0001 €": (cellule(*hermes, 0, lambda x: x + 0.0001), hermes, "ouverture : le fichier a"),
            "Total volume + 1 000": (cellule("TOTALENERGIES", "2006-05-12", 4, lambda x: x + 1000),
                                     ("TOTALENERGIES", "2006-05-12"), "volume : le fichier a"),
            "Total volume + 1": (cellule("TOTALENERGIES", "2006-05-12", 4, lambda x: x + 1),
                                 ("TOTALENERGIES", "2006-05-12"), "volume : le fichier a"),
            "Michelin plus bas + 0,0001 € (arrondi à mi-chemin)": (
                cellule("MICHELIN", "2011-09-16", 2, lambda x: round(x + 0.0001, 4)), ("MICHELIN", "2011-09-16"),
                "plus bas : le fichier a"),
            "Air Liquide comblé, ouverture + 0,00004 €": (cellule(*al, 0, lambda x: x + 0.00004), al,
                                                          "ouverture : le fichier a"),
            "Air Liquide comblé, volume + 0,4": (cellule(*al, 4, lambda x: x + 0.4), al, "volume : le fichier a"),
            "Accor 2000-03-16, clôture × 1,001": (
                cellule("ACCOR", "2000-03-16", 3, lambda x: x * 1.001), ("ACCOR", "2000-03-16"), "clôture : le fichier a"),
            "source yahoo → bnains (Hermès)": (rejeu(src={**src_, hermes: K.SOURCE_PARIS}), hermes, "colonne source"),
            "source bnains → yahoo (Air Liquide comblé)": (rejeu(src={**src_, al: K.SOURCE_YAHOO}), al, "colonne source"),
            "source « Yahoo » (Hermès)": (rejeu(src={**src_, hermes: "Yahoo"}), hermes, "colonne source « Yahoo »"),
            "« gardé » d'AXA, clôture après 25.0": (geste("AXA", "2008-10-13", "gardé", "close_apres", "25.0"),
                                                    ("AXA", "2008-10-13"), "clôture après 25.0"),
            "départ « Paris » au lieu de « paris »": (geste(*al, "comblé", "depart", "Paris"), al, "doit partir de"),
            "départ « Ligne » au lieu de « ligne »": (geste(*accor, "ajusté", "depart", "Ligne"), accor,
                                                      "doit partir de"),
            "facteur de volume 0 (Air Liquide comblé)": (geste(*al, "comblé", "facteur_volume", "0"), al,
                                                         "volume : le fichier a"),
            "facteur infini (Accor défait)": (geste(*accor, "défait", "facteur", "inf"), accor, "clôture après"),
            "Accor, clôture avant fausse": (geste(*accor, "ajusté", "close_avant", "1.0"), accor,
                                            "la ligne rejouée vaut"),
            "Air Liquide comblé, clôture avant écrite": (geste(*al, "comblé", "close_avant", "1.0"), al,
                                                         "alors que la ligne n’existe pas"),
            "Accor, ordre des deux gestes inversé": (ordre(*accor, lambda g: g[::-1]), accor, "la ligne rejouée vaut"),
            "Accor, second geste supprimé": (ordre(*accor, lambda g: g[:1]), accor, ": le fichier a"),
            "Accor, second geste doublé": (ordre(*accor, lambda g: g[:2] + g[1:2] + g[2:]), accor,
                                           "la ligne rejouée vaut"),
            "Accor, geste « corrigé » inventé, parti de la ligne": (ordre(*accor, lambda g: g + [ajoute(g[-1])]), accor,
                                                                   "doit partir de « paris »"),
            "Air Liquide comblé, retiré du fichier": (sans(*al), al, "le journal l'écrit, le fichier ne l'a pas"),
            "Hermès retirée du fichier, sans geste": (sans(*hermes), hermes, "ligne de l'origine absente du fichier"),
            "Air Liquide 2012-04-27 bâtie sur une barre de Paris prouvée fausse": (
                sur_barre_fausse("AIR LIQUIDE", "2012-04-27"), ("AIR LIQUIDE", "2012-04-27"),
                "part de Paris, qui n'a pas de barre ce jour"),
            "Engie retirée au journal, remise au fichier": (
                rejeu(s={**s_, "ENGIE": dict(s_["ENGIE"], **{engie[1]: o_["ENGIE"][engie[1]]})}), engie,
                "le journal la retire, le fichier l'a"),
        }
        vus = {nom: len(c) == 1 and c[0].startswith(f"{l[0]} {l[1]} : ") and frag in c[0]
               for nom, (c, l, frag) in abimes.items()}
        res["H56"] = tout == [] and len(abimes) == 26 and all(vus.values()) \
            and [g["geste"] for g in j_[accor]][:2] == ["défait", "ajusté"] and al not in o_.get("AIR LIQUIDE", {}) \
            and engie[1] in o_["ENGIE"] and [g["geste"] for g in j_[engie]] == ["retiré"] \
            and "2012-04-27" in brut_["AIR LIQUIDE"] and "2012-04-27" not in p_["AIR LIQUIDE"]
        if not res["H56"]:
            print(f"      H56 : {len(tout)} cas sur le dépôt {tout[:2]} ; abîmes non vus : "
                  f"{[(n, abimes[n][0][:2]) for n, ok in vus.items() if not ok]}")
    except Exception as e:
        print(f"      H56 : {type(e).__name__} : {e}")
        res["H56"] = False
    # H57 : K23, le rejeu, sur des cas fabriqués — une chaîne juste, et chaque règle du rejeu cassée une à une, vue par
    # le contrôle qui la garde (ligne ET motif) ; un journal à l'en-tête faux, ou à un nombre infini, est refusé
    try:
        org = {"Z": {"2005-01-03": (9.0, 11.0, 8.0, 10.0, 1000.0)}}
        par = {"Z": {"2005-01-04": (98.0, 104.0, 96.0, 100.0, 500.0), "2005-01-07": (100.0, 104.0, 98.0, 102.0, 500.0)}}
        geste = lambda ge, av, ap, f, fv, dep: {"valeur": "Z", "date": "", "geste": ge, "close_avant": av,
                                                "close_apres": ap, "facteur": f, "raison": "épreuve",
                                                "facteur_volume": fv, "depart": dep}
        jr = {("Z", "2005-01-03"): [geste("défait", "10.0", "20.0", "2.0", "0.5", "ligne")],
              ("Z", "2005-01-04"): [geste("comblé", "", "50.0", "0.5", "2.0", "paris")]}
        juste = {"Z": {"2005-01-03": (18.0, 22.0, 16.0, 20.0, 500.0), "2005-01-04": (49.0, 52.0, 48.0, 50.0, 1000.0)}}
        src = {("Z", "2005-01-03"): K.SOURCE_YAHOO, ("Z", "2005-01-04"): K.SOURCE_PARIS}
        r_ = lambda s=juste, sr=src, j=jr, o=org: K.lignes_non_rejouees(s, sr, o, par, j)
        avec = lambda cle, *g: {**jr, ("Z", cle): list(g)}

        def refuse(texte):
            f = os.path.join(tempfile.mkdtemp(), "journal.csv")
            open(f, "w", encoding="utf-8").write(texte)
            try:
                K.lire_journal(f)
                return False
            except ValueError:
                return True
        entete = ",".join(K.JOURNAL_DES_REPARATIONS) + "\n"
        cas = {     # nom : (cas obtenus, date attendue, fragment attendu du motif)
            "clôture du fichier fausse": (r_(s={"Z": dict(juste["Z"], **{"2005-01-03": (18.0, 22.0, 16.0, 21.0,
                                                                                         500.0)})}),
                                          "2005-01-03", "clôture : le fichier a"),
            "volume du fichier faux": (r_(s={"Z": dict(juste["Z"], **{"2005-01-04": (49.0, 52.0, 48.0, 50.0, 999.0)})}),
                                       "2005-01-04", "volume : le fichier a"),
            "clôture avant fausse": (r_(j=avec("2005-01-03", geste("défait", "11.0", "20.0", "2.0", "0.5", "ligne"))),
                                     "2005-01-03", "la ligne rejouée vaut"),
            "clôture après fausse": (r_(j=avec("2005-01-03", geste("défait", "10.0", "21.0", "2.0", "0.5", "ligne"))),
                                     "2005-01-03", "le rejeu donne"),
            "facteur non appliqué": (r_(j=avec("2005-01-03", geste("défait", "10.0", "20.0", "3.0", "0.5", "ligne"))),
                                     "2005-01-03", "clôture après 20.0"),
            "départ vide sur un geste qui écrit": (
                r_(j=avec("2005-01-03", geste("défait", "10.0", "20.0", "2.0", "0.5", ""))), "2005-01-03",
                "doit partir de"),
            "départ écrit sur un retrait": (r_(j=avec("2005-01-03", geste("retiré", "10.0", "", "", "", "ligne"))),
                                            "2005-01-03", "doit partir de"),
            "clôture après écrite sur un retrait": (
                r_(j=avec("2005-01-03", geste("retiré", "10.0", "20.0", "1.0", "1.0", ""))), "2005-01-03",
                "retire la ligne mais écrit close_apres"),
            "facteur écrit sur un retrait": (r_(j=avec("2005-01-03", geste("retiré", "10.0", "", "7.0", "", ""))),
                                             "2005-01-03", "retire la ligne mais écrit facteur"),
            "geste parti de la ligne sans clôture après": (
                r_(j=avec("2005-01-03", geste("défait", "10.0", "", "2.0", "0.5", "ligne"))), "2005-01-03",
                "mais n'écrit pas close_apres"),
            "geste inconnu": (r_(j=avec("2005-01-03", geste("bidon", "10.0", "20.0", "2.0", "0.5", "ligne"))),
                              "2005-01-03", "geste inconnu"),
            "clôture avant écrite, ligne absente": (
                r_(j=avec("2005-01-04", geste("comblé", "1.0", "50.0", "0.5", "2.0", "paris"))), "2005-01-04",
                "alors que la ligne n’existe pas"),
            "Paris sans barre ce jour": (r_(j={**jr, ("Z", "2005-01-06"): [geste("comblé", "", "51.0", "0.5", "2.0",
                                                                                  "paris")]}),
                                         "2005-01-06", "Paris, qui n'a pas de barre"),
            "ligne retirée au journal, présente au fichier": (
                r_(j=avec("2005-01-03", geste("retiré", "10.0", "", "", "", ""))), "2005-01-03",
                "le journal la retire, le fichier l'a"),
            "ligne écrite au journal, absente du fichier": (
                r_(j={**jr, ("Z", "2005-01-07"): [geste("comblé", "", "51.0", "0.5", "2.0", "paris")]}), "2005-01-07",
                "le journal l'écrit, le fichier ne l'a pas"),
            "ligne du fichier sans origine ni geste": (
                r_(s={"Z": dict(juste["Z"], **{"2005-01-05": (1.0, 1.0, 1.0, 1.0, 1.0)})}), "2005-01-05",
                "sans origine ni geste"),
            "ligne de l'origine absente du fichier, sans geste": (
                r_(s={"Z": {"2005-01-04": juste["Z"]["2005-01-04"]}}, j={("Z", "2005-01-04"): jr[("Z", "2005-01-04")]}),
                "2005-01-03", "ligne de l'origine absente du fichier"),
            "colonne source qui ment": (r_(sr={**src, ("Z", "2005-01-04"): K.SOURCE_YAHOO}), "2005-01-04",
                                        "colonne source"),
            "colonne source hors vocabulaire": (r_(sr={**src, ("Z", "2005-01-03"): "Yahoo"}), "2005-01-03",
                                                "colonne source « Yahoo »"),
        }
        garde = r_(s={"Z": dict(juste["Z"], **{"2005-01-03": (9.0, 11.0, 8.0, 10.0, 1000.0)})},
                   j=avec("2005-01-03", geste("gardé", "10.0", "10.0", "1.0", "1.0", "ligne")))
        un_seul = {nom: len(c) == 1 and c[0].startswith(f"Z {d} : ") and frag in c[0] for nom, (c, d, frag) in cas.items()}
        res["H57"] = r_() == [] and garde == [] and len(cas) == 19 and all(un_seul.values()) and refuse("valeur,date,geste\n") \
            and refuse(entete + "Z,2005-01-03,défait,10.0,20.0,inf,épreuve,0.5,ligne\n") \
            and refuse(entete + "Z,2005-01-03,défait,10.0,20.0,2.0,épreuve,nan,ligne\n") \
            and not refuse(entete + "Z,2005-01-03,défait,10.0,20.0,2.0,épreuve,0.5,ligne\n")
        if not res["H57"]:
            print(f"      H57 : juste {r_()} · gardé {garde} · non vus : {[(n, cas[n][0]) for n, ok in un_seul.items() if not ok]}")
    except Exception as e:
        print(f"      H57 : {type(e).__name__} : {e}")
        res["H57"] = False
    # H58 : K23, la provenance — registre absent, chaîne juste, chaque maillon faux, boucles, en-tête faux
    try:
        r = tempfile.mkdtemp()
        os.makedirs(os.path.join(r, "donnees"))
        os.makedirs(os.path.join(r, "programmes"))
        for n, t in (("donnees/A.csv", "a\n"), ("donnees/B.csv", "b\n"), ("programmes/P.py", "# p\n")):
            open(os.path.join(r, n), "w").write(t)
        e = lambda n: hashlib.sha256(open(os.path.join(r, n), "rb").read()).hexdigest()
        absent = K.maillons_manquants(r, ["donnees/A.csv"])
        def registre(lignes):
            with open(os.path.join(r, K.PROVENANCE), "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(K.PROVENANCE_DES_FICHIERS)
                w.writerows(lignes)
            return K.maillons_manquants(r, ["donnees/A.csv"])
        a_ = ["donnees/A.csv", e("donnees/A.csv"), "programmes/P.py", "donnees/B.csv ; donnees/C.zip", "", "2026-10-13", "épreuve"]
        b_ = ["donnees/B.csv", e("donnees/B.csv"), "programmes/P.py", "donnees/C.zip", "", "2026-10-13", "épreuve"]
        c_ = ["donnees/C.zip", "0" * 64, K.TELECHARGEMENT, "", "https://exemple.org/C.zip", "2026-10-13", "épreuve"]
        remplace = lambda l, i, x: l[:i] + [x] + l[i + 1:]
        juste = registre([a_, b_, c_])
        oblique = registre([remplace(a_, 3, "donnees\\B.csv ; ./donnees/C.zip"), b_, c_])
        sha = registre([remplace(a_, 1, "f" * 64), b_, c_])
        sans_adresse = registre([a_, b_, remplace(c_, 4, "x")])
        sans_empreinte = registre([a_, b_, remplace(c_, 1, "")])
        sans_prog = registre([remplace(a_, 2, "programmes/ABSENT.py"), b_, c_])
        donnee = registre([remplace(a_, 2, "donnees/B.csv"), b_, c_])
        sans_lu = registre([remplace(a_, 3, "")])
        pas_tele = registre([a_, b_, remplace(c_, 2, "programmes/P.py")])
        cycle = registre([a_, remplace(b_, 3, "donnees/A.csv"), c_])
        seul = registre([remplace(a_, 3, "donnees/A.csv")])
        doublon = registre([a_, a_, b_, c_])
        dossier = registre([remplace(a_, 3, "donnees"), b_, c_])
        open(os.path.join(r, K.PROVENANCE), "w").write("fichier,sha256\n")
        try:
            K.maillons_manquants(r, ["donnees/A.csv"])
            entete = False
        except ValueError:
            entete = True
        res["H58"] = len(absent) == 1 and "aucun registre" in absent[0] and juste == [] and oblique == [] \
            and len(sha) == 1 and "inscrite 0 fois" in sha[0] \
            and "donnees/C.zip : téléchargement sans adresse http(s)" in sans_adresse \
            and "donnees/C.zip : téléchargement sans empreinte de 64 caractères" in sans_empreinte \
            and sans_prog == ["donnees/A.csv : produit par programmes/ABSENT.py, qui n'est pas un programme du dépôt"] \
            and donnee == ["donnees/A.csv : produit par donnees/B.csv, qui n'est pas un programme du dépôt"] \
            and sans_lu == ["donnees/A.csv : produit par programmes/P.py, sans aucun fichier lu déclaré"] \
            and "donnees/C.zip : absent du dépôt, et le registre en fait 0 téléchargement(s), au lieu d'un" in pas_tele \
            and [c for c in cycle if "boucle" in c] == ["donnees/A.csv : boucle dans la provenance "
                                                         "(donnees/A.csv → donnees/B.csv → donnees/A.csv)"] \
            and "donnees/A.csv : aucune de ses sources n'arrive à un premier maillon (téléchargement ou fichier écrit à la main)" in seul \
            and len(doublon) == 1 and "inscrite 2 fois" in doublon[0] \
            and "donnees/A.csv : lit donnees, qui est un dossier" in dossier and entete
    except Exception:
        res["H58"] = False
    # H59 : K23 de bout en bout par `main` — l'extrait 2005 déclaré, le registre juste : K23 se tait ; une clôture
    # retouchée : K23 la voit ; le registre retiré : K23 le dit (relecture indépendante du 13-10-2026, X1 et X2)
    try:
        r = racine_d_essai()
        yahoo = "donnees/sources_yahoo/yahoo_ohlcv_propre.csv"
        lignes = list(csv.reader(open(os.path.join(r, yahoo), encoding="utf-8", newline="")))
        def ecrire(ls):
            with open(os.path.join(r, K.FICHIER), "w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows([ls[0] + ["source"]] + [x + ["yahoo"] for x in ls[1:]])
        ecrire(lignes)
        with open(os.path.join(r, K.JOURNAL), "w", encoding="utf-8") as f:
            f.write(",".join(K.JOURNAL_DES_REPARATIONS) + "\n")
        e = lambda n: hashlib.sha256(open(os.path.join(r, n), "rb").read()).hexdigest()
        prog = K.FICHIERS_REPARES[K.FICHIER.replace(os.sep, "/")]
        os.makedirs(os.path.join(r, "programmes"), exist_ok=True)
        shutil.copy(os.path.join(RACINE, prog), os.path.join(r, prog))
        def registre(producteur=prog):
            with open(os.path.join(r, K.PROVENANCE), "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(K.PROVENANCE_DES_FICHIERS)
                w.writerow([K.FICHIER, e(K.FICHIER), producteur, K.ORIGINE + " ; " + K.BNAINS,
                            "https://exemple.org/repare.csv" if producteur == K.TELECHARGEMENT else "", "2026-10-13",
                            "épreuve"])
                for n in (K.ORIGINE, K.BNAINS):
                    w.writerow([n, e(n), K.TELECHARGEMENT, "", "https://exemple.org/" + os.path.basename(n),
                                "2026-10-13", "épreuve"])
        registre()
        _, _, l_juste = resultats_du_controle(K, r, K.FICHIER)
        i = next(k for k, x in enumerate(lignes) if k and x[0] == "ACCOR")
        lignes[i] = lignes[i][:5] + [str(float(lignes[i][5]) * 1.01)] + lignes[i][6:]
        ecrire(lignes)
        registre()                                   # le fichier a changé : son empreinte aussi
        _, out_r, l_retouche = resultats_du_controle(K, r, K.FICHIER)
        os.remove(os.path.join(r, K.PROVENANCE))
        _, out_s, l_sans = resultats_du_controle(K, r, K.FICHIER)
        res["H59"] = l_juste["K23"].split()[1:3] == ["ok", "0"] and l_retouche["K23"].split()[1:3] == ["REFUS", "1"] \
            and "ACCOR " + lignes[i][1] + " : clôture : le fichier a " in out_r \
            and l_sans["K23"].split()[1:3] == ["REFUS", "4"] and "aucun registre de provenance" in out_s
    except Exception:
        res["H59"] = False
    # H60 : « réparé » se déclare — le fichier réparé privé de sa colonne source, ou inscrit au registre comme
    # téléchargement, ne fait plus taire K23 (relecture de Cowork du 13-10-2026, 91d4ac8, cassure I)
    try:
        registre(K.TELECHARGEMENT)
        _, out_t, _ = resultats_du_controle(K, r, K.FICHIER)
        with open(os.path.join(r, K.FICHIER), "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(lignes)          # sans la colonne source
        registre(K.TELECHARGEMENT)
        _, out_c, l_c = resultats_du_controle(K, r, K.FICHIER)
        res["H60"] = (K.FICHIER.replace(os.sep, "/") + " : déclaré écrit par " + prog) in out_t \
            and "inscrit au registre comme produit par « téléchargement »" in out_t \
            and "déclaré réparé (écrit par " + prog + ") mais sans colonne source" in out_c \
            and l_c["K23"].split()[1] == "REFUS"
    except Exception:
        res["H60"] = False
    # H61 : K23 ne rejoue pas sur une origine abîmée (superviseur du 18-10-2026, R-734) — le fichier Yahoo d'origine
    # avec une ligne en double : le contrôle s'arrête, code 2, au lieu de rejouer sur une base fausse
    try:
        r = tempfile.mkdtemp()
        for nom in os.listdir(RACINE):
            if nom != "donnees":
                os.symlink(os.path.join(RACINE, nom), os.path.join(r, nom))
        os.makedirs(os.path.join(r, "donnees", "sources_yahoo"))
        for nom in os.listdir(os.path.join(RACINE, "donnees")):
            if nom != "sources_yahoo":
                os.symlink(os.path.join(RACINE, "donnees", nom), os.path.join(r, "donnees", nom))
        for nom in os.listdir(os.path.join(RACINE, "donnees", "sources_yahoo")):
            if nom != os.path.basename(K.ORIGINE):
                os.symlink(os.path.join(RACINE, "donnees", "sources_yahoo", nom),
                           os.path.join(r, "donnees", "sources_yahoo", nom))
        lignes = open(os.path.join(RACINE, K.ORIGINE), encoding="utf-8").read().split("\n")
        open(os.path.join(r, K.ORIGINE), "w", encoding="utf-8").write("\n".join(lignes[:2] + lignes[1:]))
        code, out = lancer(K.main, [r])
        res["H61"] = code == 2 and "défaut(s) de lecture" in out and "K23 ne peut pas rejouer" in out
        shutil.rmtree(r, ignore_errors=True)
    except Exception as e:
        print(f"      H61 : {type(e).__name__} : {e}")
        res["H61"] = False
    # H62 : K23, le premier maillon « écrit à la main » (décisions de Jean-Luc du 19-10-2026 à 07h05 et 08h23 ;
    # superviseurs R-759 du même jour) — un fichier bâti sur une VRAIE ligne de BARRES_BNAINS_FAUSSES.csv (Société
    # Générale, 2009) passe ; chaque condition cassée une à une est vue par son motif ; sur les vrais fichiers, les trois
    # fichiers écrits à la main citent leurs sources, et le fichier Yahoo nettoyé ne passerait pas ; le référentiel passe
    # depuis qu'il porte ses trois colonnes de preuve (décision de Jean-Luc du 24-10-2026 à 16h06).
    # Les cas « inscrit » et « qui revient » donnent des dents AU VERDICT aux refus du chemin absolu, du « .. », du lien
    # et du dossier (pour le dossier, par le seul cas « lu : dossier inscrit » : un fichier cité qui est un dossier est
    # refusé de toute façon, comme fichier absent) : sans eux, chacun de ces refus retiré laissait le fichier refusé pour une autre raison (absent du
    # registre), et le sabotage ne mordait que par le texte du message (superviseur n° 3 du 19-10-2026, H5 : « S5, S6
    # et S7 n'ont de dents que par les formes « inscrites » et « qui revient » »).
    try:
        r = tempfile.mkdtemp()
        dehors = tempfile.mkdtemp()
        X = os.path.join(dehors, "X.csv")
        open(X, "w").write("x\n")
        for d in ("donnees", "programmes", "donnees/sources_yahoo"):
            os.makedirs(os.path.join(r, d), exist_ok=True)
        vraies = list(csv.reader(open(os.path.join(RACINE, "donnees", "sources_bnains", "BARRES_BNAINS_FAUSSES.csv"),
                                      encoding="utf-8", newline="")))
        sg = [l for l in vraies if l[0] == "SOCIETE GENERALE" and l[1].startswith("2009")]
        tete = vraies[0]

        def ecrire(n, lignes, encodage="utf-8"):
            with open(os.path.join(r, n), "w", encoding=encodage, newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(lignes)
        open(os.path.join(r, "programmes/P.py"), "w").write("# p\n")
        open(os.path.join(r, "donnees/A.csv"), "w").write("a\n")
        open(os.path.join(r, "donnees/B.csv"), "w").write("b\n")
        os.symlink(X, os.path.join(r, "donnees/L.csv"))
        e = lambda n: hashlib.sha256(open(os.path.join(r, n), "rb").read()).hexdigest()

        def avec(entete=None, sans_ligne=False, encodage="utf-8", **champs):
            l = dict(zip(tete, sg[0]))
            l.update(champs)
            t = entete or tete
            ecrire("donnees/M.csv", [t] + ([] if sans_ligne else [[l.get(c, "") for c in t]]), encodage)

        def registre(m_champs=None, autres=(), a_lu="donnees/M.csv"):
            m = ["donnees/M.csv", (m_champs or {}).get(1) or e("donnees/M.csv"), K.ECRIT_A_LA_MAIN, "", "", "2026-10-19",
                 "décision du 19-10"]
            for i, x in (m_champs or {}).items():
                m[i] = x
            a_ = ["donnees/A.csv", e("donnees/A.csv"), "programmes/P.py", a_lu, "", "2026-10-19", "épreuve"]
            with open(os.path.join(r, K.PROVENANCE), "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(K.PROVENANCE_DES_FICHIERS)
                w.writerows([a_, m] + list(autres))
            return K.maillons_manquants(r, ["donnees/A.csv"])
        b_ = ["donnees/B.csv", e("donnees/B.csv"), K.TELECHARGEMENT, "", "https://exemple.org/B.csv", "2026-10-19", "épr"]
        x_ = [X, e(X), K.TELECHARGEMENT, "", "https://exemple.org/X.csv", "2026-10-19", "épr"]
        l_ = ["donnees/L.csv", e("donnees/L.csv"), K.TELECHARGEMENT, "", "https://exemple.org/L.csv", "2026-10-19", "épr"]
        d_ = ["donnees", "0" * 64, K.TELECHARGEMENT, "", "https://exemple.org/donnees", "2026-10-19", "épr"]
        cas = {}
        avec()
        cas["juste"] = (registre(), None)
        cas["sans preuve"] = (registre({6: ""}), "sans preuve")
        cas["avec des fichiers lus"] = (registre({3: "donnees/B.csv"}), "des fichiers lus")
        cas["avec une adresse"] = (registre({4: "https://exemple.org/M.csv"}), "une adresse")
        cas["lu : chemin absolu"] = (registre(a_lu=X), f"lit « {X} », un chemin absolu")
        cas["lu : chemin absolu inscrit"] = (registre(a_lu=X, autres=[x_]), f"lit « {X} », un chemin absolu")
        cas["lu : « .. » qui revient, inscrit"] = (registre(a_lu="donnees/../donnees/B.csv", autres=[b_]), "sort par « .. »")
        cas["lu : lien inscrit"] = (registre(a_lu="donnees/L.csv", autres=[l_]), "un lien symbolique")
        cas["lu : dossier inscrit"] = (registre(a_lu="donnees", autres=[d_]), "lit donnees, qui est un dossier")
        avec(entete=[c for c in tete if c != K.COLONNES_DES_SOURCES_A_LA_MAIN[2]])
        cas["sans la colonne des fichiers cités"] = (registre(), "sans les colonnes source, citation, fichiers_cites")
        avec(entete=["valeur", "source"])
        cas["une seule des colonnes"] = (registre(), "sans les colonnes source, citation, fichiers_cites")
        avec(citation="")
        cas["citation vide"] = (registre(), "ligne 2 sans citation")
        avec(source="voir http://exemple.org")
        cas["adresse précédée de texte"] = (registre(), "pas une adresse http(s) entière")
        avec(source="donnees/B.csv")
        cas["chemin dans la source"] = (registre(), "pas une adresse http(s) entière")
        avec(source="http://.")
        cas["adresse sans nom d'hôte"] = (registre(), "pas une adresse http(s) entière")
        avec(source="", fichiers_cites="")
        cas["ni adresse ni fichier"] = (registre(), "ni adresse en source ni fichier en fichiers_cites")
        avec(fichiers_cites=X)
        cas["fichier cité absolu"] = (registre(), "un chemin absolu")
        cas["fichier cité absolu inscrit"] = (registre(autres=[x_]), "un chemin absolu")
        avec(fichiers_cites="../hors.csv")
        cas["fichier cité par « .. »"] = (registre(), "sort par « .. »")
        avec(fichiers_cites="donnees/../donnees/B.csv")
        cas["fichier cité par « .. » qui revient, inscrit"] = (registre(autres=[b_]), "sort par « .. »")
        avec(fichiers_cites="donnees/L.csv")
        cas["fichier cité, lien symbolique"] = (registre(), "un lien symbolique")
        cas["fichier cité, lien inscrit"] = (registre(autres=[l_]), "un lien symbolique")
        avec(fichiers_cites="donnees")
        cas["fichier cité, dossier"] = (registre(), "un dossier")
        cas["fichier cité, dossier inscrit"] = (registre(autres=[d_]), "un dossier")
        avec(fichiers_cites="donnees/ABSENT.csv")
        cas["fichier cité absent"] = (registre(), "« donnees/ABSENT.csv », absent du dépôt")
        fant_ = ["donnees/ABSENT.csv", "ab" * 32, K.TELECHARGEMENT, "", "https://exemple.org/F.csv", "2026-10-19", "épr"]
        cas["fichier cité absent, inscrit téléchargement"] = (registre(autres=[fant_]), "« donnees/ABSENT.csv », absent du dépôt")
        avec(fichiers_cites="donnees/B.csv")
        cas["fichier cité qui ne se remonte pas"] = (registre(), "cite comme source donnees/B.csv, qui ne se remonte pas")
        cas["fichier cité qui ne se remonte pas : le parent le dit"] = (cas["fichier cité qui ne se remonte pas"][0], "donnees/A.csv : aucune de ses sources n'arrive")
        cas["fichier cité qui se remonte"] = (registre(autres=[b_]), None)
        # « Ligne par ligne » et « morceau par morceau », dans LES DEUX SENS : chaque défaut est placé en 1re position
        # puis en 2e, l'autre juste (relecteur n° 3 du 19-10-2026, N2 : un contrôle qui ne vérifiait que la dernière
        # ligne restait vert ; superviseur n° 5 : la grille « chaque position » laisse passer 0 des 34 boucles et
        # vérifications sabotées qu'il a essayées, « le milieu de 3 » en laissait passer 2).
        def deux(fausse, **champs):
            juste = dict(zip(tete, sg[0])); faux = dict(juste); faux.update(champs)
            lignes = [juste, faux] if fausse == 2 else [faux, juste]
            ecrire("donnees/M.csv", [tete] + [[l.get(c, "") for c in tete] for l in lignes])
        def morceaux(fausse, bon, mauvais):
            return " ; ".join([bon, mauvais] if fausse == 2 else [mauvais, bon])
        for k in (1, 2):
            deux(k, citation="")
            cas[f"2 lignes, la {k}e sans citation"] = (registre(), f"ligne {k + 1} sans citation")
            deux(k, source="voir le rapport")
            cas[f"2 lignes, la {k}e adresse fausse"] = (registre(), f"ligne {k + 1} : source « voir le rapport »")
            deux(k, fichiers_cites=X)
            cas[f"2 lignes, la {k}e cite un absolu inscrit"] = (registre(autres=[x_]), f"ligne {k + 1} : fichiers_cites")
            deux(k, fichiers_cites="donnees")
            cas[f"2 lignes, la {k}e cite un dossier inscrit"] = (registre(autres=[d_]),
                                                                f"ligne {k + 1} : fichiers_cites « donnees », un dossier")
            deux(k, source="", fichiers_cites="")
            cas[f"2 lignes, la {k}e sans adresse ni fichier"] = (registre(), f"ligne {k + 1} : ni adresse")
            avec(source=morceaux(k, "https://www.bnains.org/x", "voir le rapport"))
            cas[f"2 adresses, la {k}e fausse"] = (registre(), "« voir le rapport », pas une adresse")
            avec(fichiers_cites=morceaux(k, "donnees/B.csv", X))
            cas[f"2 fichiers cités, le {k}e absolu inscrit"] = (registre(autres=[b_, x_]), "un chemin absolu")
            avec()
            cas[f"lu : 2 morceaux, le {k}e absolu inscrit"] = (registre(a_lu=morceaux(k, "donnees/M.csv", X), autres=[x_]),
                                                              f"lit « {X} », un chemin absolu")
        c_ = ["C:/x.csv", "ab" * 32, K.TELECHARGEMENT, "", "https://exemple.org/x.csv", "2026-10-19", "épr"]
        cas["lu : lettre de lecteur inscrite"] = (registre(a_lu="C:/x.csv", autres=[c_]), "lit « C:/x.csv », un chemin absolu")
        avec(sans_ligne=True)
        cas["sans aucune ligne"] = (registre(), "sans aucune ligne")
        avec(encodage="utf-16")
        cas["illisible"] = (registre(), "illisible")
        avec()
        m_sha = e("donnees/M.csv")
        os.remove(os.path.join(r, "donnees/M.csv"))
        cas["absent du dépôt"] = (registre({1: m_sha}), "absent du dépôt")
        repare = K.FICHIER.replace(os.sep, "/")
        ecrire(repare, [tete] + sg)
        with open(os.path.join(r, K.PROVENANCE), "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(
                [K.PROVENANCE_DES_FICHIERS, [repare, e(repare), K.ECRIT_A_LA_MAIN, "", "", "2026-10-19", "décision"]])
        cas["le fichier réparé inscrit à la main"] = (K.maillons_manquants(r, [repare]), "déclaré écrit par")
        vus = {n: (c == [] if frag is None else any(frag in x for x in c)) for n, (c, frag) in cas.items()}
        noms = ("donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv", "donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv",
                "donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv", "donnees/sources_yahoo/yahoo_ohlcv_propre.csv",
                "donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv")
        reels = {n: K.sources_ecrites_a_la_main(RACINE, n) for n in noms}
        res["H62"] = len(sg) == 1 and len(cas) == 50 and all(vus.values()) \
            and all(reels[n][0] is None for n in noms[:3] + noms[4:]) and reels[noms[4]][1] \
            and reels[noms[2]][1] == ["donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv"] \
            and reels[noms[3]][0] == "sans les colonnes source, citation, fichiers_cites"
        if not res["H62"]:
            print(f"      H62 : non vus {[(n, cas[n][0]) for n, ok in vus.items() if not ok]} · réels {reels}")
        shutil.rmtree(r, ignore_errors=True)
        shutil.rmtree(dehors, ignore_errors=True)
    except Exception as ex:
        print(f"      H62 : {type(ex).__name__} : {ex}")
        res["H62"] = False
    return res


def main():
    K, R = charger()
    res = epreuves(K, R)
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programmes tels quels : {len(res) - len(rouges)}/{len(res)} épreuves vertes" + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        for k, (chemin, cible, remplace) in SABOTAGES.items():
            if choix and k not in choix[0]:
                continue
            source = open(chemin, encoding="utf-8").read()
            if source.count(cible) != 1:
                print(f"{k} NE S'APPLIQUE PLUS : texte cible trouvé {source.count(cible)} fois")
                return 2
            r = epreuves(*charger((chemin, cible, remplace)))
            tombees = [e for e, v in r.items() if not v]
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}")
            if not tombees:
                code = 1
    return code


if __name__ == "__main__":
    # Tous les dossiers d'essai vont sous UN dossier, effacé à la fin : mesuré le 07-10-2026, les
    # passages successifs avaient laissé 2 460 dossiers dans /tmp et rempli le disque.
    _DOSSIER_D_ESSAI = tempfile.mkdtemp(prefix="epreuves_")
    tempfile.tempdir = os.environ["TMPDIR"] = _DOSSIER_D_ESSAI
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(_DOSSIER_D_ESSAI, ignore_errors=True)
