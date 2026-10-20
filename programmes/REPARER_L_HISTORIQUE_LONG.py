#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REPARER_L_HISTORIQUE_LONG.py — Dim 04-10-2026 (Paris) — PROPOSÉ, non validé (A-539, actions ②, ③, ④).
Rôle : réparer le fichier Yahoo des 26 ans avec la seconde source, bnains.org, en trois gestes et
dans l'ordre de A-539 : ② reconstruire AXA 2000 → 09-11-2009 (`RECONSTRUCTIONS` dit pourquoi) et
EssilorLuxottica 2000-2001,
③ retirer d'Engie les séances d'avant le 08-07-2005, ④ combler les séances manquantes. Il écrit un
fichier RÉPARÉ à côté du fichier Yahoo, et le journal de chaque ligne touchée. Il ne verse RIEN au
fichier maître des cours.
Simulation uniquement.

① RÔLE — Fabriquer donnees/sources_yahoo/historique_long_repare.csv : le fichier Yahoo déposé, dont
  les lignes fausses sont remplacées par les cours de la Bourse de Paris archivés par bnains,
  ramenés à la convention de Yahoo (cours ajustés des divisions et des augmentations de capital,
  pas des dividendes). La huitième colonne, source, dit pour chaque ligne d'où elle vient : yahoo ou
  bnains. Le journal des réparations dit, pour chaque ligne touchée, le geste, l'ancienne et la
  nouvelle clôture, d'où part le geste (la ligne, ou la barre de Paris), les facteurs appliqués aux prix
  et au volume, et la raison : K23 refait chaque ligne en le rejouant, à l'égalité exacte (contrat
  JOURNAL_DES_REPARATIONS).
② CONTEXTE D'APPEL — À la main, après programmes/LIRE_LES_ARCHIVES_BNAINS.py :
  python3 programmes/REPARER_L_HISTORIQUE_LONG.py <racine>. Puis
  programmes/CONTROLER_L_HISTORIQUE_LONG.py juge le résultat. Aucun circuit ne le lance. Ses
  épreuves : tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py.
③ ENTRÉE — Un argument : la racine du dépôt.
④ CONDITIONS D'ENTRÉE — Sous la racine : donnees/sources_yahoo/yahoo_ohlcv_propre.csv (le fichier
  déposé par Cowork le 04-10-2026), donnees/sources_yahoo/evenements.json (les divisions vues par
  Yahoo), donnees/sources_bnains/bnains_cac40.csv (l'extrait bnains), DROITS_BNAINS.csv (les
  droits de souscription), et, écrits à la main, DETACHEMENTS_OFFICIELS.csv (les jours officiels et
  les chiffres des droits) et BARRES_BNAINS_FAUSSES.csv (les barres bnains prouvées fausses) ;
  donnees/sources_francfort/COURS_DE_FRANCFORT.csv (la troisième source) ;
  donnees/sources_indice/INDICE_CAC40.csv (l'indice CAC 40 à deux sources, qui départage une séance) ;
  donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv (les ajustements de Yahoo jugés, dont ceux à défaire).
⑤ SORTIE — UNE valeur : le code de sortie. 0 = les deux fichiers écrits · 1 = un geste n'a pas pu
  se faire sur une base sûre (période de référence trop instable, témoin qui ne ressemble pas) :
  RIEN n'est écrit, la raison est affichée · 2 = rien n'a pu être fait (fichier absent ou
  illisible, ou toute erreur imprévue).
⑥ TRAITEMENT — ① lire les neuf fichiers, et ôter de l'extrait bnains les barres prouvées fausses
  (`K.oter_les_barres_fausses`) ; ôter des divisions de Yahoo celles qu'il déclare à tort
  (`K.sans_les_divisions_fausses`) · ①bis `defaire` les ajustements de Yahoo jugés faux et dont la
  correction est décidée (`K.lire_a_defaire`) · ② calculer le calendrier et les jours douteux avec les
  définitions du contrôle (programmes/CONTROLER_L_HISTORIQUE_LONG.py, importées, jamais recopiées),
  et les séances où l'indice CAC 40 donne tort à Yahoo (`K.arbitre_de_l_indice`) ·
  ③ `reconstruire` chaque fenêtre de `RECONSTRUCTIONS` · ④ `retirer` chaque cas de `RETRAITS` ·
  ④bis `recaler` les séances d'avant un détachement où Yahoo ajuste trop tôt · ④ter `ajuster` les
  droits que Yahoo n'a pas ajustés (Veolia 2002, France Télécom 2003, Société Générale 2006,
  Saint-Gobain 2009, BNP Paribas 2009) · ④quater `corriger` : les séances où l'indice donne tort à
  Yahoo, remplacer chaque ligne de Yahoo qui s'écarte de Paris · ④quinquies `trancher` : remplacer les
  clôtures de Yahoo que bnains et Francfort démentent ensemble · ⑤ `combler` les séances manquantes,
  les séances où l'indice a donné tort à Yahoo n'étant plus douteuses pour bnains · ⑥ écrire le
  fichier réparé et le journal, puis le résumé.
⑦ UNITÉ — Des COURS en EUROS ajustés comme Yahoo les ajuste, des VOLUMES en NOMBRE DE TITRES
  ajustés de même, des DATES de séance.
⑧ POURQUOI — Les défauts et leurs remèdes ont été trouvés par Cowork le 04-10-2026 (relevé dans
  echanges/RELU.md ; action A-539, à la demande de Jean-Luc : « Recherche à fond […] uniquement
  après avoir tout essayé »). Le facteur qui ramène bnains à la convention de Yahoo n'est jamais
  écrit à la main (R-728) : il est MESURÉ sur une période où les deux sources s'accordent, et le
  programme s'arrête si elles ne s'accordent pas assez. Pour AXA, il retrouve le 0,9771 de Cowork.
⑨ CE QUI CLOCHE — AXA : la reconstruction applique 0,9771 après le détachement du 19-06-2006 et
  0,9771 ÷ 1,0195 avant (`reconstruire`) ; le jour du 19-06-2006 est celui de l'avis d'AXA au BALO
  du 16-06-2006 (« Les droits préférentiels de souscription seront détachés le 19 juin 2006. »,
  lu le 07-10-2026 ; il avait d'abord été déduit du cours de 24,47 € du rapport annuel, clôture du
  vendredi 16-06-2006). Jusqu'au 07-10-2026, un facteur
  unique laissait là une fausse baisse de 1,95 %. · Les volumes de
  Yahoo ne suivent pas toujours la convention ordinaire (volume brut multiplié par les divisions
  à venir) : avant le 16-05-2001, AXA porte 4,17 fois ce volume ; avant le 16-07-2007,
  EssilorLuxottica 2,04 fois (mesuré le 04-10-2026). La reconstruction mesure le facteur de volume
  sur la période de référence et le reporte avec les divisions : elle suit donc Yahoo pour
  EssilorLuxottica (référence et fenêtre avant 2007), mais pas pour AXA avant le 16-05-2001, où
  elle donne le volume ordinaire, quatre fois moindre que celui de Yahoo (relecture indépendante
  du 04-10-2026). · Les dates de division de evenements.json diffèrent de celles de bnains pour
  Schneider Electric 2011, Bureau Veritas 2013, Dassault Systèmes 2014 et Air Liquide 2012 et 2014 :
  c'est bnains qui a tort, les communiqués officiels donnent les dates de Yahoo (lus le 07-10-2026) ;
  ces barres sont dans BARRES_BNAINS_FAUSSES.csv et ne servent plus. · Un jour
  douteux dans une fenêtre reconstruite devient une séance manquante, déclarée au journal. · Les
  séances que rien ne comble restent manquantes : décision de Jean-Luc (A-539, action ⑤). → BACKLOG.
  · Le 18-10-2026, les gestes partis de la ligne (« défait », « ajusté », « aligné ») passent par
  `K.appliquer`, qui multiplie par le facteur que le journal écrit, au lieu de diviser : des lignes
  du fichier réparé ont changé au 16e chiffre (4,4e-16 au plus, en relatif ; pour « ajusté », sur les
  prix ; pour « défait » et « aligné », sur le volume — superviseur n° 2 et relecture du même jour),
  pour que K23 compare à l'égalité exacte (décision de Jean-Luc, 20h41). · Les noms « yahoo » et
  « bnains » de la colonne source sont écrits ici en clair, quand le contrat les déclare
  (SOURCE_YAHOO, SOURCE_PARIS) : une divergence ferait refuser chaque ligne par K23, bruyamment.
⑩ EFFET — Écrit donnees/sources_yahoo/historique_long_repare.csv et
  donnees/sources_yahoo/journal_des_reparations.csv, en les remplaçant. Ne touche à aucun autre
  fichier — ni au fichier Yahoo déposé, ni au fichier maître des cours.
⑪ TERMINAISON — Toujours : chaque geste parcourt un nombre fini de lignes. Aucun de mes appels ne
  peut boucler.
"""
import bisect, csv, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CONTROLER_L_HISTORIQUE_LONG as K          # les définitions partagées avec le contrôle (R-708)
from CONTRATS_DES_FICHIERS import COURS_MAITRE, COURS_BNAINS, JOURNAL_DES_REPARATIONS, GESTES_DU_JOURNAL

ENTREE = K.ORIGINE        # le fichier Yahoo avant réparation, nommé une fois (R-708), dans le contrôle qui le relit (K18)
SORTIE = os.path.join("donnees", "sources_yahoo", "historique_long_repare.csv")
JOURNAL = K.JOURNAL      # nommé une fois, dans le contrôle qui le relit (K20, R-708)
CHAMPS_JOURNAL = JOURNAL_DES_REPARATIONS   # l'en-tête du journal, déclaré une fois au contrat (R-708, superviseur du 18-10-2026)
# Les fenêtres à reconstruire depuis bnains (A-539, action ②) : valeur, début, fin, puis la PÉRIODE
# DE RÉFÉRENCE où Yahoo et bnains s'accordent et sur laquelle le facteur est mesuré.
RECONSTRUCTIONS = (
    ("AXA", "2000-01-01", "2009-11-09", "2008-01-01", "2009-11-09",
     "Yahoo faux de 2001 à 2007 (735 barres plates, écarts jusqu'à 170 jours par an) ; référence "
     "2008 → 09-11-2009, où le rapport Yahoo/bnains vaut 0,9771 ; la fenêtre va jusqu'au 09-11-2009, "
     "veille du détachement des droits de l'augmentation de capital : « La période de souscription "
     "s'étendra du 10 au 23 novembre 2009 inclus » (communiqué d'AXA du 09-11-2009, lu le 07-10-2026) ; "
     "bnains ne cote le droit que dès le 11, et la fin au 10-11 retenue du 04 au 06-10-2026 était fausse"),
    ("ESSILORLUXOTTICA", "2000-01-01", "2001-12-31", "2002-01-01", "2006-06-30",
     "Yahoo faux en 2000-2001 (174 et 102 jours d'écart) ; référence 2002 → mi-2006, avant les jours "
     "douteux de bnains de 2006-2007"),
)
# Les débuts de série faux (A-539, action ③) : valeur, première séance gardée, société TÉMOIN dont
# les cours doivent être ceux qu'on retire, raison.
RETRAITS = (
    ("ENGIE", "2005-07-08", "SUEZ",
     "avant le 08-07-2005, Yahoo met sous Engie les cours de Suez ; Gaz de France est négocié à partir "
     "du 08-07-2005 (avis Euronext n° 2005-2579, ISIN FR0010208488)"),
)
# Les barres de Yahoo ÉCARTÉES SUR DÉCISION DE JEAN-LUC (A-555 ⑥) : valeur, séance, raison. La barre
# est retirée avant le comblement, qui la remplace par la barre de Paris (bnains) au facteur local,
# avec la même règle que pour une séance manquante (R-708 : un seul calcul). Rien n'est écarté sans
# une décision écrite ici avec ses mots, sa date et la mesure qui l'a motivée.
BARRES_YAHOO_ECARTEES = (
    ("PERNOD RICARD", "2007-01-15",
     "décision de Jean-Luc du 09-10-2026 à 09h58 (« 1 » à « Remplacer la clôture de Yahoo du 15-01-2007 "
     "par celle de Paris, 171,80 € ») : la clôture de Yahoo, ramenée aux cours de Paris, vaut 174,20 €, "
     "l'OUVERTURE de Paris ce jour-là, quand la clôture de Paris vaut 171,80 € (+1,4 %) ; Francfort muet ; "
     "veille de l'attribution d'actions gratuites du 16-01-2007, où l'écart faisait refuser K15"),
)
ALIGNEMENT = K.MARCHE_EXACTE   # un droit ajusté par Yahoo est ramené à la règle officielle quand les deux facteurs
                               # diffèrent de plus de ce seuil, celui que K22 tient (Crédit Agricole 2007 : 0,12 %)
MIN_REFERENCE = 100   # au moins 100 séances communes dans une période de référence ou avec un témoin
# L'accord exigé (K.PROPRE, K.PART_PROPRE) et les voisins d'une séance à combler (K.VOISINS) sont
# déclarés dans le contrôle, qui juge avec les mêmes : jamais recopiés ici (R-708).


def barre(b, f, k, s):
    """Rend une barre bnains ramenée à la convention de Yahoo.

    ① RÔLE — Un seul calcul pour la reconstruction et le comblement.
    ② CONTEXTE D'APPEL — `reconstruire`, `combler`.
    ③ ENTRÉE — `b` : (open, high, low, close, volume) bruts · `f` : facteur de prix · `k` : facteur
      de volume · `s` : divisions postérieures (`K.divisions`).
    ④ CONDITIONS D'ENTRÉE — `s` > 0.
    ⑤ SORTIE — TROIS valeurs : la barre `K.arrondir(b, f / s, s × k)` — prix × f / s arrondis à K.DECIMALES
      décimales, volume × s × k arrondi à l'unité ; le facteur de prix appliqué, f / s ; le facteur de volume
      appliqué, s × k.
      [rend: 3]
    ⑥ TRAITEMENT — ⑤.
    ⑦ UNITÉ — EUROS et NOMBRE DE TITRES, convention de Yahoo ; facteurs sans unité.
    ⑧ POURQUOI — Le journal écrit les facteurs que la barre a APPLIQUÉS, rendus ici, jamais recalculés à côté (R-708,
      superviseur du 18-10-2026). Avant, le journal n'écrivait que f : 1 010 gestes et 611 lignes ne se refaisaient pas
      (K23, A-578). L'arrondi est fait par `K.arrondir`, la fonction même que le rejeu appelle (décision de Jean-Luc du
      18-10-2026 à 20h41 : égalité exacte). Le fichier réparé est resté identique à l'octet en passant de x × f / s à
      x × (f / s) (mesuré le 18-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fp, fv = f / s, s * k
    return K.arrondir(b, fp, fv), fp, fv



def noter(journal, valeur, date, geste, avant, apres, facteur, raison, facteur_volume):
    """Ajoute au journal une ligne, dans l'ordre des colonnes du contrat, avec le départ que le contrat donne au geste.

    ① RÔLE — Le seul écrivain d'une ligne du journal des réparations.
    ② CONTEXTE D'APPEL — Chaque geste de ce programme, une fois par ligne de cours touchée.
    ③ ENTRÉE — `journal` : la liste à compléter · `valeur`, `date` · `geste` : un nom de GESTES_DU_JOURNAL ·
      `avant`, `apres` : les clôtures, ou "" · `facteur`, `facteur_volume` : les facteurs appliqués, ou "" · `raison`.
    ④ CONDITIONS D'ENTRÉE — `geste` est dans GESTES_DU_JOURNAL, sinon KeyError : un geste inconnu du contrat arrête la
      réparation au lieu d'écrire une ligne que K23 refuserait.
    ⑤ SORTIE — Aucune valeur.
      [rend: rien]
    ⑥ TRAITEMENT — Ranger les valeurs par nom de colonne ; DÉDUIRE `depart` de GESTES_DU_JOURNAL ; ajouter la ligne
      dans l'ordre de JOURNAL_DES_REPARATIONS.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur n° 2 du 18-10-2026 (R-759) : le départ était écrit à la main à neuf endroits, et l'ordre
      des colonnes répété à treize ; il se déduit désormais du contrat, qui le déclare une fois (R-708).
    ⑨ CE QUI CLOCHE — Les autres lignes de ce programme qui relisent le journal en mémoire le lisent par position
      (`l[2]` pour le geste) : elles supposent que le contrat garde valeur, date, geste en tête. L'une est MUETTE : la
      garde `trous` de `reparer` (barres écartées que le comblement n'a pas remplacées) deviendrait vide si la colonne
      `geste` bougeait, et son ARRÊT disparaîtrait sans un mot (superviseur n° 3 du 18-10-2026 ; → BACKLOG, A-597).
    ⑩ EFFET — Modifie `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    ligne = {"valeur": valeur, "date": date, "geste": geste, "close_avant": avant, "close_apres": apres,
             "facteur": facteur, "raison": raison, "facteur_volume": facteur_volume, "depart": GESTES_DU_JOURNAL[geste]}
    journal.append([ligne[c] for c in JOURNAL_DES_REPARATIONS])

def defaire(series, a_defaire, journal):
    """Retire de la série de Yahoo un ajustement qu'il n'aurait pas dû faire ; rend le nombre de lignes touchées.

    ① RÔLE — Annuler les deux erreurs de Yahoo trouvées le 08-10-2026 : Crédit Agricole, 22-05-2018 (une division
      « 27 pour 26 » qui n'a pas eu lieu) et EssilorLuxottica, 06-05-2024 (un dividende payable en actions corrigé
      comme une distribution).
      Depuis le 09-10-2026, une troisième : Accor, 02-07-2010 (Yahoo valorisait l'action Edenred distribuée à 10,96 €), défaite et remplacée par la distribution déclarée à 13,00 € (décision de Jean-Luc à 21h00).
    ② CONTEXTE D'APPEL — `reparer`, une fois, EN PREMIER, sur le fichier de Yahoo tel que lu.
    ③ ENTRÉE — `series` : les séries, modifiées EN PLACE · `a_defaire` : `K.lire_a_defaire` · `journal` : liste où
      ajouter.
    ④ CONDITIONS D'ENTRÉE — Chaque facteur est positif (`K.lire_a_defaire` le garantit).
    ⑤ SORTIE — UNE valeur : le nombre de lignes touchées.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque (valeur, date, facteur) : chaque ligne d'avant la date voit ses quatre prix
      multipliés par le facteur et son volume multiplié par 1 / facteur (`K.appliquer`), et le journal le dit
      (« défait »).
    ⑦ UNITÉ — Des EUROS et des NOMBRES DE TITRES ; le facteur est un rapport sans unité.
    ⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 à 11h14 : « S'il y a des erreurs, il faut les corriger ».
      Mesuré le même jour : avant ces dates, Yahoo porte les clôtures × 0,963 et les volumes × 1,0385 pour Crédit
      Agricole (contre bnains, 2014-2016), les clôtures × 0,9785 et les volumes × 1,0219 pour EssilorLuxottica
      (contre le fichier maître, janvier-avril 2024) ; BNP Paribas, Orange et L'Oréal, témoins, sont à 1. Défaire
      EN PREMIER : les gestes suivants mesurent leurs facteurs sur la série de Yahoo, et les lignes qu'ils refont
      depuis bnains suivent alors la série corrigée.
    ⑨ CE QUI CLOCHE — Relecture indépendante du 08-10-2026 : faire ce geste en dernier ne change que l'arrondi de
      515 lignes (les lignes refaites depuis bnains sont arrondies à 4 décimales, celles-ci non) ; seule l'empreinte
      de l'épreuve H32 fige l'ordre. · Les prix et volumes ne sont pas arrondis (16.46304230769231 ; un volume
      46567065.99999999), comme ceux du geste `ajuster` (→ BACKLOG). · Le facteur s'applique sans vérifier que
      l'erreur est encore dans le fichier de Yahoo : un nouveau fichier où Yahoo l'aurait corrigée deviendrait
      faux, et K20 l'accepterait ; seul l'outil de la méthode H le verrait (→ BACKLOG).
    ⑩ EFFET — Modifie `series` et `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    n = 0
    for valeur, date, f in a_defaire:
        y = series.get(valeur, {})
        for x in sorted(x for x in y if x < date):
            o, h, l, c, vol = y[x]
            y[x] = K.appliquer(y[x], f, 1 / f)
            noter(journal, valeur, x, "défait", c, y[x][3], f,
                  f"ajustement de Yahoo du {date} défait (AJUSTEMENTS_DE_YAHOO.csv) : prix × {f:.6f}, volume ÷ {f:.6f}",
                  1 / f)
            n += 1
    return n


def reconstruire(series, sources, bnains, evenements, douteux, journal, detachements=None, francfort=None):
    """Reconstruit depuis bnains chaque fenêtre de `RECONSTRUCTIONS` ; rend la liste des arrêts.

    ① RÔLE — Action ② de A-539.
    ② CONTEXTE D'APPEL — `reparer`, une fois, en premier.
    ③ ENTRÉE — `series` : les séries Yahoo, modifiées EN PLACE · `sources` : (valeur, date) → source,
      modifié en place · `bnains` · `evenements` · `douteux` · `journal` : liste où ajouter ·
      `detachements` : valeur → {jour officiel de détachement : droit} (`K.lire_detachements`), ou None ·
      `francfort` : `K.lire_francfort`, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des raisons d'arrêt, vide si tout s'est fait.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque fenêtre : ① mesurer les facteurs sur la période de référence (dates
      communes, hors jours douteux) ; s'arrêter s'il y a moins de `MIN_REFERENCE` dates ou moins de
      `K.PART_PROPRE` d'accord · ② pour chaque date d de la fenêtre, le facteur est celui de la
      référence divisé par (1 + marche permise) pour chaque détachement qui tombe APRÈS d et au plus
      tard le premier jour de la référence (`K.marche_permise`) ; le facteur de volume est multiplié
      d'autant · ③ pour chaque date de la fenêtre où Yahoo a une ligne ou bnains une
      barre du calendrier : si la barre bnains est sûre (`K.barre_sure` : utilisable, ou d'un jour
      douteux mais confirmée par Francfort), elle remplace
      ou ajoute la ligne ; sinon la ligne Yahoo est GARDÉE si, sur ses séances voisines, Yahoo
      s'accorde avec bnains au facteur de la fenêtre (`K.facteur_local` sur le Yahoo déposé), et
      RETIRÉE sinon — elle est alors fausse et rien ne la remplace.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — Reconstruire TOUTE la fenêtre avec un seul facteur rend la série homogène ; ne
      réparer que les jours visiblement faux laisserait des jours faux mais plausibles. Garder un jour
      Yahoo juste autour évite de creuser un trou là où Yahoo n'était pas faux. Mesuré le
      04-10-2026 : AXA garde ainsi deux jours de 2008-2009 ; ses jours de 2000 sans barre bnains
      (17-07-2000, 13-10-2000) sont RETIRÉS, car Yahoo y applique 0,9600 et non le 0,9771 de la
      fenêtre : les garder ferait une marche de 1,8 % ce jour-là (relecture indépendante du même
      jour). Le facteur se divise aux détachements qui tombent entre une date et la référence :
      mesuré le 07-10-2026 dans le rapport annuel 2006 d'AXA, ses cours mensuels d'avant juin 2006
      sont ajustés de 1,0195 pour l'augmentation de capital de juin 2006 (une action nouvelle pour 9
      à 19,80 € quand l'action valait 24,47 €) ; les cours bruts de bnains s'y retrouvent à 0,05 %
      près sur 20 mois. Un facteur unique, 0,9771, laissait donc une fausse baisse de 1,95 % le
      19-06-2006 ; le bon facteur d'avant est 0,9771 ÷ 1,0195 = 0,958, celui de Yahoo à 0,2 % près.
    ⑨ CE QUI CLOCHE — Un détachement absent de `detachements` n'est pas vu : le facteur reste unique
      de part et d'autre, comme avant le 07-10-2026.
    ⑩ EFFET — Modifie `series`, `sources`, `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    arrets, cal = [], K.calendrier(series, bnains)
    for valeur, du, au, ref_du, ref_au, raison in RECONSTRUCTIONS:
        y, b = series.get(valeur, {}), bnains.get(valeur, {})
        ref = sorted(d for d in y if ref_du <= d <= ref_au and d in b and d not in douteux)
        f, k, accord = K.rapports(y, b, evenements, valeur, ref)
        if len(ref) < MIN_REFERENCE or accord < K.PART_PROPRE:
            arrets.append(f"{valeur} : période de référence {ref_du} → {ref_au} trop courte ou instable "
                          f"({len(ref)} séances, accord {accord:.0%})")
            continue
        print(f"  ② {valeur} {du} → {au} : facteur de prix {f:.4f}, de volume {k:.4f}, "
              f"mesurés sur {len(ref)} séances, accord {accord:.1%}")
        origine = {valeur: dict(y)}      # Yahoo tel que déposé, pour juger s'il est juste autour d'un jour
        detache = (detachements or {}).get(valeur, {})
        for d in sorted({d for d in y if du <= d <= au} | {d for d in b if du <= d <= au and d in cal}):
            a = 1.0                       # les droits détachés entre d et la référence
            for j, droit in detache.items():
                if d < j <= ref_du:
                    a *= 1 + K.marche_permise(b, droit)
            avant = y[d][3] if d in y else ""
            if K.barre_sure(bnains, francfort or {}, valeur, d, douteux):
                y[d], fp, fv = barre(b[d], f / a, k * a, K.divisions(evenements, valeur, d))
                sources[(valeur, d)] = "bnains"
                noter(journal, valeur, d, "reconstruit", avant, y[d][3], fp,
                      raison,
                      fv)
                continue
            if d not in y:
                continue
            f_ici = K.facteur_local(origine, bnains, evenements, valeur, d, douteux | {d}, ())[0]
            if f_ici is not None and abs(f_ici / (f / a) - 1) <= K.PROPRE:
                noter(journal, valeur, d, "gardé", avant, avant, 1.0,
                      "fenêtre reconstruite, bnains n'a pas de barre utilisable ce jour, et Yahoo "
                      "s'accorde avec bnains sur les séances voisines (facteur mesuré sur elles, non "
                      f"appliqué : {f_ici!r})",
                      1.0)
                continue
            del y[d]
            sources.pop((valeur, d), None)
            noter(journal, valeur, d, "retiré", avant, "", "",
                  "fenêtre reconstruite, bnains n'a pas de barre utilisable ce jour"
                  + (" (jour douteux)" if d in douteux else "") + ", et Yahoo est faux autour",
                  "")
    return arrets


def retirer(series, sources, bnains, evenements, journal):
    """Retire chaque début de série de `RETRAITS`, après avoir vérifié qu'il est bien le témoin ; rend les arrêts.

    ① RÔLE — Action ③ de A-539.
    ② CONTEXTE D'APPEL — `reparer`, une fois, après `reconstruire`.
    ③ ENTRÉE — `series` : les séries, modifiées EN PLACE · `sources` : (valeur, date) → source,
      modifié en place · `bnains` : l'extrait · `evenements` : le contenu de evenements.json ·
      `journal` : liste où ajouter.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des raisons d'arrêt, vide si tout s'est fait.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre les lignes d'avant la première séance gardée ; s'il n'y en a aucune,
      rien à retirer, rien à prouver (relecture indépendante du 04-10-2026 : un fichier déjà
      nettoyé était refusé) · ② les confronter au
      témoin chez bnains, divisions de la valeur appliquées ; s'arrêter s'il y a moins de
      `MIN_REFERENCE` séances communes ou moins de `K.PART_PROPRE` d'accord, ou si le facteur n'est
      pas 1 à `K.PROPRE` près · ③ retirer les lignes.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — On ne retire pas des cours sur une affirmation : on prouve d'abord qu'ils sont
      ceux d'une autre société. Cowork l'a mesuré le 04-10-2026 (Suez : rapport 1,0, dispersion
      0,0002) ; le programme le remesure à chaque passage.
    ⑨ CE QUI CLOCHE — Les divisions appliquées sont celles que Yahoo déclare pour la valeur (Engie :
      5 pour 1 le 15-05-2001, qui est la division de Suez).
    ⑩ EFFET — Modifie `series`, `sources`, `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    arrets = []
    for valeur, debut, temoin, raison in RETRAITS:
        y, t = series.get(valeur, {}), bnains.get(temoin, {})
        partie = {d: x for d, x in y.items() if d < debut}
        if not partie:
            print(f"  ③ {valeur} : aucune ligne avant le {debut}, rien à retirer")
            continue
        communes = sorted(d for d in partie if d in t)
        f, _, accord = K.rapports(partie, t, evenements, valeur, communes)
        if len(communes) < MIN_REFERENCE or accord < K.PART_PROPRE or abs(f - 1) > K.PROPRE:
            arrets.append(f"{valeur} : les {len(partie)} lignes d'avant le {debut} ne sont pas prouvées être "
                          f"celles de {temoin} ({len(communes)} séances communes, accord {accord:.0%}, facteur {f})")
            continue
        print(f"  ③ {valeur} avant le {debut} : {len(partie)} lignes, identiques à {temoin} chez bnains "
              f"(facteur {f:.4f}, accord {accord:.1%} sur {len(communes)} séances) — retirées")
        for d in sorted(partie):
            noter(journal, valeur, d, "retiré", y[d][3], "", "",
                  f"{raison} (facteur de la comparaison à {temoin}, non appliqué : {f!r})",
                  "")
            del y[d]
            sources.pop((valeur, d), None)
    return arrets


def recaler(series, sources, bnains, evenements, detachements, douteux, journal):
    """Remet au jour du détachement l'ajustement que Yahoo pose avant lui ; rend le nombre de séances recalées.

    ① RÔLE — Corriger, partout où la preuve est complète, le défaut trouvé sur Société Générale par
      Cowork le 05-10-2026 : Yahoo change de facteur une ou plusieurs séances AVANT le détachement
      officiel d'un droit, et la série porte ces jours-là des mouvements que la Bourse n'a pas faits.
    ② CONTEXTE D'APPEL — `reparer`, une fois, après `retirer` et avant `combler`.
    ③ ENTRÉE — `series` : les séries, modifiées EN PLACE · `sources` : (valeur, date) → source,
      modifié en place · `bnains` : l'extrait · `evenements` : le contenu de evenements.json ·
      `detachements` : valeur → {jour officiel de détachement : (clôture du droit, son premier jour
      chez bnains)} (`K.lire_detachements`) ·
      `douteux` : les jours douteux · `journal` : liste où ajouter.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de séances recalées.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque jour de détachement d d'une valeur, sur ses séances comparables
      (`K.seances_comparables`) : ① prendre la séance d'ancrage a et la fenêtre, les `K.AUTOUR`
      séances qui précèdent d (`K.autour_du_detachement`) · ② calculer les rapports clôture /
      clôture bnains, divisions comprises · ③ ne rien faire si la marche de a à d n'est pas celle que
      permet le droit (à `K.ECART` près), si aucune séance de la fenêtre ne s'écarte du rapport de a
      de plus de `K.ECART`, ou si l'une de celles qui s'écartent n'a pas de barre bnains utilisable ·
      ④ sinon, chaque séance de la fenêtre qui s'écarte devient la barre bnains ramenée au facteur
      de a, venue de bnains.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — Mesuré le 07-10-2026 aux jours de détachement OFFICIELS (`K.lire_detachements`) :
      Société Générale, détachement le 21-02-2008, ouverture de la souscription. Yahoo y change de
      facteur deux fois : 0,8934 le 19-02, 0,8363 le 20, 0,9478 le 21. Sur toute la fenêtre, la
      marche fait +6,1 % et le droit permet +6,2 % (4,00 sur une action à 64,58) : la preuve tient,
      et le 20-02-2008 est recalé ; le fichier y fait −6,01 % comme Paris, au lieu de −12,02 %
      (relecture de Cowork du 05-10-2026). Pour AXA, Crédit Agricole, Danone, Michelin, Pernod Ricard
      et Veolia, Yahoo change de facteur le jour officiel : rien n'est recalé. Du 04 au 06-10-2026,
      le jour du détachement était pris au premier jour de cotation du droit chez bnains, une séance
      trop tard, et Danone (01-06-2009), Michelin (30-09-2010), Pernod Ricard (16-04-2009) et
      Société Générale (21-02-2008) avaient été recalés à tort.
    ⑨ CE QUI CLOCHE — Seuls les droits que le lecteur reconnaît sont vus (⑨ de `lire_archives` dans
      programmes/LIRE_LES_ARCHIVES_BNAINS.py). · La séance d'ancrage est crue juste : si Yahoo y avait
      déjà changé de facteur, la marche de a à d ne serait pas celle du droit et rien ne serait fait.
    ⑩ EFFET — Modifie `series`, `sources`, `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    recalees = 0
    for valeur, jours in sorted(detachements.items()):
        y, b = series.get(valeur, {}), bnains.get(valeur, {})
        dates = K.seances_comparables(y, b, douteux)
        for d, droit in sorted(jours.items()):
            a, fenetre = K.autour_du_detachement(dates, d)
            if a is None:
                continue
            r = {x: y[x][3] * K.divisions(evenements, valeur, x) / b[x][3] for x in [a, d] + fenetre}
            fausses = [x for x in fenetre if abs(r[x] / r[a] - 1) > K.ECART]
            if (abs(r[d] / r[a] - 1 - K.marche_permise(b, droit)) > K.ECART or not fausses
                    or not all(K.barre_utilisable(bnains, valeur, x, douteux) for x in fausses)):
                continue
            f, k, _ = K.rapports(y, b, evenements, valeur, [a])
            for x in fausses:
                avant = y[x][3]
                y[x], fp, fv = barre(b[x], f, k, K.divisions(evenements, valeur, x))
                sources[(valeur, x)] = "bnains"
                noter(journal, valeur, x, "recalé", avant, y[x][3], fp,
                      f"Yahoo change de facteur avant le détachement du {d} ; ramenée au facteur du {a}",
                      fv)
                recalees += 1
    return recalees


def ajuster(series, bnains, evenements, detachements, douteux, journal):
    """Pose l'ajustement d'un droit détaché que Yahoo n'a pas fait ; rend (droits ajustés, droits non mesurables).

    ① RÔLE — Ramener à la convention de Yahoo (cours ajustés des augmentations de capital) les
      séries où Yahoo a oublié un droit : chaque ligne d'avant le détachement est divisée par
      1 + la valeur du droit, comme Yahoo le fait pour les autres.
    ② CONTEXTE D'APPEL — `reparer`, une fois, après `recaler` et avant `combler`.
    ③ ENTRÉE — `series` : les séries, modifiées EN PLACE · `bnains` : l'extrait, barres fausses ôtées ·
      `evenements` : le contenu de evenements.json · `detachements` : `K.lire_detachements` ·
      `douteux` : les jours douteux · `journal` : liste où ajouter.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : ① le nombre de droits ajustés · ② la liste des droits qu'aucune barre
      bnains ne permet de mesurer, chacun nommé (valeur et jour).
      [rend: 2]
    ⑥ TRAITEMENT — Pour chaque détachement d d'une valeur, dans l'ordre des dates, sur ses séances
      comparables (`K.seances_comparables`) : ① mesurer la marche du rapport fichier ÷ bnains,
      divisions comprises, entre la médiane des `K.VOISINS` séances d'avant d et celle des
      `K.VOISINS` séances à partir de d (d lui-même peut manquer : sa barre bnains est fausse) · ② prendre la marche permise m (`K.marche_permise`) ·
      ③ si la marche mesurée ne dépasse pas le quart de m — Yahoo n'a pas ajusté —, diviser les
      prix de chaque ligne d'avant d par 1 + m et multiplier son volume par 1 + m, et le dire au
      journal · ④ un d sans séance comparable avant lui, ou à partir de lui, est non mesurable.
    ⑦ UNITÉ — Des EUROS et des NOMBRES DE TITRES ; m est un rapport sans unité.
    ⑧ POURQUOI — Mesuré le 07-10-2026 aux jours de détachement officiels : Yahoo ajuste la plupart
      des droits (Michelin 2010 : rapport 0,9662 avant, 1,0000 après), mais pas Veolia 2002, France
      Télécom 2003, Société Générale 2006, Saint-Gobain 2009 ni BNP Paribas 2009 — chez BNP Paribas,
      la clôture du 28-09-2009 vaut 56,57 € chez Yahoo, le chiffre officiel BRUT de la note
      d'opération, et la série chute de 5,7 % le 30-09-2009 quand le droit en explique 2,9 %. Une
      marche que la Bourse n'a pas faite fausse les signaux ; laisser le fichier sans ajustement
      ferait refuser K15. Le volume suit la même règle que chez Yahoo : rapport des volumes Yahoo ÷
      bnains 1,0349 avant le détachement de Michelin 2010, 1,0598 chez Danone 2009 (mesuré le même
      jour). Le seuil du quart sépare deux cas que les mesures séparent nettement, sur les vingt
      droits mesurables (07-10-2026) : marche nulle à 0,02 % près quand Yahoo oublie (cinq droits),
      marche à moins de 0,5 % de m quand il ajuste (quinze droits ; Danone 2009 −0,48 %, Michelin
      2010 +0,48 %).
    ⑨ CE QUI CLOCHE — Après la fin de bnains (28-02-2017), rien ne se mesure : Euronext 2021 et
      Veolia 2021 sont rendus non mesurables ; leur ajustement par Yahoo a été vérifié à la main le
      07-10-2026 contre les clôtures officielles. · Un ajustement fait à moitié par Yahoo n'est pas
      touché : K15 le refuse.
    ⑩ EFFET — Modifie `series` et `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    ajustes, non_mesurables = 0, []
    for valeur, jours in sorted(detachements.items()):
        y, b = series.get(valeur, {}), bnains.get(valeur, {})
        for d, droit in sorted(jours.items()):
            s = K.marche_mesuree(y, b, evenements, valeur, d, douteux)     # la mesure, une fois, dans le contrôle
            if s is None:
                non_mesurables.append(f"{valeur} {d}")
                continue
            m = K.marche_permise(b, droit)
            if abs(s) > abs(m) / 4:
                continue
            for x in [x for x in y if x < d]:
                o, h, l, c, vol = y[x]
                y[x] = K.appliquer(y[x], 1 / (1 + m), 1 + m)
                noter(journal, valeur, x, "ajusté", c, y[x][3], 1 / (1 + m),
                      f"Yahoo n'a pas ajusté le droit détaché le {d} (marche mesurée {100 * s:+.2f} %, "
                      f"valeur du droit {100 * m:+.2f} %) ; ligne divisée par {1 + m:.6f}",
                      1 + m)
            ajustes += 1
    return ajustes, non_mesurables


def aligner(series, bnains, evenements, detachements, douteux, journal):
    """Ramène à la règle officielle le facteur d'un droit que Yahoo a ajusté autrement ; rend (droits alignés, écarts mesurés).

    ① RÔLE — Que chaque droit détaché porte, dans le fichier, le facteur de la règle officielle (prix de référence
      technique ÷ clôture de la veille), qu'il ait été ajusté par Yahoo ou par `ajuster`.
    ② CONTEXTE D'APPEL — `reparer`, une fois, juste après `ajuster`.
    ③ ENTRÉE — `series` : les séries, modifiées EN PLACE · `bnains` : l'extrait, barres fausses ôtées ·
      `evenements` : les divisions gardées · `detachements` : `K.lire_detachements` · `douteux` : les jours
      douteux · `journal` : liste où ajouter.
    ④ CONDITIONS D'ENTRÉE — `ajuster` est passé : un droit que Yahoo avait oublié porte déjà la marche officielle.
    ⑤ SORTIE — DEUX valeurs : ① le nombre de droits alignés · ② la liste de tous les écarts mesurés, chacun
      (valeur, jour, marche du fichier, marche officielle), pour être montrés.
      [rend: 2]
    ⑥ TRAITEMENT — Pour chaque détachement d, mesuré comme dans `ajuster` (rapport fichier ÷ bnains, divisions
      comprises, médiane des `K.VOISINS` séances comparables d'avant d contre celle des `K.VOISINS` à partir de d) :
      la marche du fichier s ; la marche officielle m (`K.marche_permise`) ; si Yahoo a ajusté (|s| dépasse le
      quart de |m|, la règle d'`ajuster`) et que (1 + s) ÷ (1 + m) s'écarte de 1 de plus de `ALIGNEMENT`,
      multiplier les prix de chaque ligne d'avant d par (1 + s) ÷ (1 + m), diviser son volume par ce nombre, et le
      dire au journal (« aligné »).
    ⑦ UNITÉ — Des EUROS et des NOMBRES DE TITRES ; s, m et le rapport sans unité.
    ⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 à 09h39 (« 1 » à « Règle officielle partout, fichier corrigé
      sur les 4 écarts »). Mesuré le même jour, puis corrigé par la relecture indépendante (le dividende que les
      actions nouvelles ne touchent pas, que leurs documents comptent) : Yahoo suit exactement la règle officielle
      pour la plupart des droits qu'il a ajustés (Danone 2009 : +5,976 % pour +5,976 % ; Vinci 2006 : +1,849 % pour
      +1,854 %, dividende de 2005 compris), mais pas pour Crédit Agricole 2007 (+1,51 % pour +1,64 %), Société
      Générale 2008 (+6,08 % pour +6,83 %, dividende de 0,90 € compris) ni BNP Paribas 2006 (+1,11 % pour +0,78 %,
      dividende de 2,60 € compris) : chacun laissait sur la courbe une marche que la Bourse n'a pas faite.
    ⑨ CE QUI CLOCHE — Après le 28-02-2017, rien ne se mesure (Euronext 2021, Veolia 2021) : le fichier y garde le
      facteur de Yahoo, qui suit la règle officielle avec une clôture de la veille déduite de Yahoo lui-même. · Une
      distribution d'actions d'une autre société passe par la même règle : la valeur déclarée fait foi (Accor 2010).
    ⑩ EFFET — Modifie `series` et `journal`.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    alignes, mesures = 0, []
    for valeur, jours in sorted(detachements.items()):
        y, b = series.get(valeur, {}), bnains.get(valeur, {})
        for d, droit in sorted(jours.items()):
            s = K.marche_mesuree(y, b, evenements, valeur, d, douteux)     # la mesure, une fois, dans le contrôle
            if s is None:
                continue
            m = K.marche_permise(b, droit)
            mesures.append((valeur, d, s, m))
            if abs(s) <= abs(m) / 4 or abs((1 + s) / (1 + m) - 1) <= ALIGNEMENT:
                continue
            q = (1 + s) / (1 + m)
            for x in [x for x in y if x < d]:
                o, h, l, c, vol = y[x]
                y[x] = K.appliquer(y[x], q, 1 / q)
                noter(journal, valeur, x, "aligné", c, y[x][3], q,
                      f"Yahoo a ajusté le droit détaché le {d} de {100 * s:+.3f} %, la règle officielle donne "
                      f"{100 * m:+.3f} % ; ligne multipliée par {q:.6f} (décision de Jean-Luc du 10-10-2026, 09h39)",
                      1 / q)
            alignes += 1
    return alignes, mesures


def corriger(series, sources, bnains, evenements, jours, douteux, detachements, journal):
    """Les séances où l'indice CAC 40 donne tort à Yahoo, remplace chaque ligne de Yahoo qui s'écarte de Paris ; rend le nombre de lignes remplacées.

    ① RÔLE — Réparer les séances où ce sont les clôtures de Yahoo, et non celles de bnains, qui sont fausses
      (`K.arbitre_de_l_indice`, verdict « le fichier a tort »).
    ② CONTEXTE D'APPEL — `reparer`, une fois, après `ajuster` et avant `trancher`.
    ③ ENTRÉE — `series`, `sources` : modifiés EN PLACE · `bnains` · `evenements` · `jours` : les séances où
      l'indice donne tort à Yahoo · `douteux` : les jours douteux du fichier déposé · `detachements` :
      `K.lire_detachements` · `journal` : liste où ajouter.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de lignes remplacées.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque séance de `jours` et chaque valeur dont la ligne vient de Yahoo et dont la barre
      bnains est utilisable (`K.barre_utilisable`, sans la règle du jour douteux) : ① le facteur du jour
      (`K.facteur_du_jour`), mesuré sur des voisines prises hors des jours douteux ET hors de `jours` ·
      ② si la clôture de Yahoo s'en écarte de plus de `K.PROPRE`, la barre bnains ramenée à ce facteur, venue de
      bnains, et dite au journal (« corrigé ») ; facteur instable : la ligne reste, K17b la signale.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — Relecture de Cowork du 07-10-2026, 23h04 : remplacer UNE clôture de Yahoo au milieu de clôtures
      de Yahoo elles-mêmes fausses rendait le rendement avec la voisine plus faux (BNP Paribas, 12→13-09-2011 :
      0,73 point d'erreur avant, 2,61 après). Mesuré le même soir : du 29-08 au 16-09-2011, Yahoo porte une autre
      clôture que Paris pour les deux tiers des valeurs, chaque séance ; l'indice donne tort à Yahoo sur toute
      la suite (marge +8,0). La séance entière se répare donc d'un coup : toutes les valeurs qui s'écartent,
      et non celles que Francfort a pu départager. Les voisines du facteur sont prises hors de ces séances,
      dont les clôtures sont fausses.
    ⑨ CE QUI CLOCHE — Le verdict de l'indice porte sur la séance : une ligne de Yahoo qui s'écarte de Paris de
      moins de `K.PROPRE` reste, présumée juste. · Une barre bnains elle-même fausse ce jour-là pour une valeur
      serait prise : `K.barre_utilisable` ne refuse que les barres incohérentes, plates ou d'une fenêtre fausse.
    ⑩ EFFET — Modifie `series`, `sources`, `journal`.
    ⑪ TERMINAISON — Toujours : chaque (séance, valeur) est vue une fois.
      [sort: non]
    """
    venues = {cle for cle, src in sources.items() if src == "bnains"}
    exclus = set(douteux) | set(jours)
    n = 0
    for v in sorted(series):
        detache = (detachements or {}).get(v, {})
        for d in sorted(jours):
            if sources.get((v, d)) != "yahoo" or not K.barre_utilisable(bnains, v, d, frozenset()):
                continue
            f, k = K.facteur_du_jour(series, bnains, evenements, v, d, exclus, venues, detache)
            if f is None:
                continue
            ecart = series[v][d][3] * K.divisions(evenements, v, d) / bnains[v][d][3] / f - 1
            if abs(ecart) <= K.PROPRE:
                continue
            avant = series[v][d][3]
            series[v][d], fp, fv = barre(bnains[v][d], f, k, K.divisions(evenements, v, d))
            sources[(v, d)] = "bnains"
            noter(journal, v, d, "corrigé", avant, series[v][d][3], fp,
                  f"l'indice CAC 40 donne tort aux clôtures de Yahoo ce jour-là ; Yahoo à {100 * ecart:+.2f} % "
                  f"de Paris (bnains) ; barre bnains au facteur du jour",
                  fv)
            n += 1
    return n


def trancher(series, sources, bnains, francfort, evenements, douteux, detachements, journal):
    """Remplace chaque clôture de Yahoo que bnains et Francfort démentent ensemble ; rend le nombre de lignes remplacées.

    ① RÔLE — Réparer les barres de Yahoo fausses hors de tout ajustement (relecture de Cowork du
      07-10-2026, 21h33 : « quand deux sources indépendantes, Paris (bnains) et Francfort, s'accordent
      à 0,5 % près contre Yahoo à plus de 1 %, la barre de Yahoo est fausse »).
    ② CONTEXTE D'APPEL — `reparer`, une fois, après `corriger` et avant `combler`.
    ③ ENTRÉE — `series`, `sources` : modifiés EN PLACE · `bnains` · `francfort` : `K.lire_francfort` ·
      `evenements` · `douteux` : les jours douteux du fichier déposé, non utilisés ici — chaque passage
      les remesure sur la série en cours, comme le contrôle les mesurera sur le fichier réparé ·
      `detachements` : `K.lire_detachements` · `journal` : liste où ajouter.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de lignes remplacées.
      [rend: 1]
    ⑥ TRAITEMENT — Jusqu'à ce qu'un passage ne trouve plus rien : ① les cas « fausse » de
      `K.barres_dementies` · ② pour chacun dont la barre bnains est sûre (`K.barre_sure`), la barre
      bnains ramenée aux facteurs de prix et de volume que `K.barres_dementies` a mesurés sans la
      ligne, venue de bnains, et dite au journal.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — Mesuré le 07-10-2026 : Yahoo et bnains portent souvent la même ouverture, le même
      plus haut et le même plus bas ; seule la clôture diffère, de plusieurs pour cent en septembre
      2011 — BNP Paribas, 13-09-2011 : Yahoo 27,15, bnains 28,00, Francfort 27,995. Une ligne
      remplacée devient une ligne venue de bnains, que le passage suivant ne juge plus et ne prend
      plus pour voisine, et les jours douteux changent avec la série : on recommence donc jusqu'à ce
      que rien ne bouge. Mesuré le 07-10-2026 : avec les jours douteux du fichier déposé, sept lignes
      restaient « fausse » au contrôle du fichier réparé.
    ⑨ CE QUI CLOCHE — Les cas que Francfort ne tranche pas restent tels quels (K17b). · Remplacer UNE clôture
      au milieu de clôtures de Yahoo elles-mêmes fausses rend le rendement avec la voisine plus faux : c'est
      pourquoi `corriger` passe avant, séance entière, là où l'indice donne tort à Yahoo ; K18 refuse ce qui
      resterait (relecture de Cowork du 07-10-2026, 23h04).
    ⑩ EFFET — Modifie `series`, `sources`, `journal`.
    ⑪ TERMINAISON — Toujours : chaque passage qui continue remplace au moins une ligne venue de
      Yahoo, et il y en a un nombre fini.
      [sort: non]
    """
    total = 0
    while True:
        venues = {cle for cle, src in sources.items() if src == "bnains"}
        ici = K.jours_douteux(K.ecarts(series, bnains))     # comme le contrôle les mesurera sur le fichier réparé
        remplacees = 0
        for valeur, d, ecart, ecart_f, verdict, f, k in K.barres_dementies(series, bnains, francfort, evenements,
                                                                           ici, venues, detachements):
            if verdict != "fausse" or not K.barre_sure(bnains, francfort, valeur, d, ici):
                continue
            avant = series[valeur][d][3]
            series[valeur][d], fp, fv = barre(bnains[valeur][d], f, k, K.divisions(evenements, valeur, d))
            sources[(valeur, d)] = "bnains"
            noter(journal, valeur, d, "remplacé", avant, series[valeur][d][3], fp,
                  f"clôture de Yahoo démentie par Paris (bnains) et Francfort : Yahoo à "
                  f"{100 * ecart:+.2f} % de bnains, Francfort à {100 * ecart_f:+.2f} % ; barre bnains au facteur local",
                  fv)
            remplacees += 1
        total += remplacees
        if not remplacees:
            return total


def combler(series, sources, bnains, evenements, douteux, journal, detachements=None, francfort=None):
    """Comble chaque séance manquante que bnains peut combler sûrement ; rend le nombre de séances comblées.

    ① RÔLE — Action ④ de A-539.
    ② CONTEXTE D'APPEL — `reparer`, une fois, en dernier.
    ③ ENTRÉE — `series` : les séries, modifiées EN PLACE · `sources` : (valeur, date) → source,
      modifié en place · `bnains` : l'extrait · `evenements` : le contenu de evenements.json ·
      `douteux` : les jours douteux · `journal` : liste où ajouter · `detachements` : les jours de
      détachement officiels (`K.lire_detachements`), ou None · `francfort` : `K.lire_francfort`, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de séances comblées.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque séance manquante (`K.trous`, sur le calendrier de la série ACTUELLE
      et de bnains, `K.calendrier`) :
      ① passer si la barre bnains n'est pas sûre (`K.barre_sure` : utilisable, ou d'un jour douteux mais
      confirmée par Francfort) · ② mesurer le facteur
      local (`K.facteur_local`), du côté du détachement officiel où tombe la séance ; s'il n'est pas sûr, la séance reste manquante et le journal le dit ·
      ③ sinon ajouter la barre, venue de bnains.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — Un facteur LOCAL suit les ajustements de Yahoo (augmentations de capital,
      divisions) sans les connaître tous. Le contrôle juge avec les mêmes fonctions : une séance que
      ce geste laisse, le contrôle ne la lui reproche pas (K7), et une séance qu'il aurait dû combler,
      le contrôle la refuse (K6).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Modifie `series`, `sources`, `journal`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    comblees = 0
    venues = {cle for cle, src in sources.items() if src == "bnains"}
    for valeur, d in K.trous(series, K.calendrier(series, bnains)):
        if not K.barre_sure(bnains, francfort or {}, valeur, d, douteux):
            continue
        f, k, accord, n = K.facteur_local(series, bnains, evenements, valeur, d, douteux, venues,
                                          (detachements or {}).get(valeur, {}))
        if f is None:
            noter(journal, valeur, d, "non comblé", "", "", "",
                  f"{n} séances voisines, accord {accord:.0%} : le facteur change à côté",
                  "")
            continue
        series[valeur][d], fp, fv = barre(bnains[valeur][d], f, k, K.divisions(evenements, valeur, d))
        sources[(valeur, d)] = "bnains"
        venues.add((valeur, d))
        noter(journal, valeur, d, "comblé", "", series[valeur][d][3], fp,
              f"séance manquante chez Yahoo ; facteur mesuré sur {n} séances voisines",
              fv)
        comblees += 1
    return comblees


def texte(x):
    """Écrit un nombre sans rien perdre ni rien ajouter : « 33.8058 » reste 33.8058, un volume reste entier.

    ① RÔLE — Recopier les lignes Yahoo non touchées avec les mêmes nombres.
    ② CONTEXTE D'APPEL — `ecrire`, cinq fois par ligne.
    ③ ENTRÉE — `x` : un nombre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : son écriture la plus courte qui redonne exactement le même nombre.
      [rend: 1]
    ⑥ TRAITEMENT — Un entier s'écrit sans décimale ; sinon l'écriture courte de Python.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une ligne Yahoo relue puis réécrite garde la même valeur ; « 33.80 » devient
      « 33.8 », le même nombre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return str(int(x)) if float(x).is_integer() else repr(float(x))


def reparer(racine):
    """Lit, répare dans l'ordre de A-539, écrit ; rend le code de sortie.

    ① RÔLE — Enchaîner les trois gestes et poser les fichiers.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — ④ du programme.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme. Les jours douteux sont mesurés sur le fichier Yahoo, fenêtres à
      reconstruire exclues : leurs écarts sont des erreurs de Yahoo, pas de bnains.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Écrire tout ou rien : un fichier réparé à moitié aurait l'air réparé.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — ⑩ du programme.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        series, defauts, _ = K.lire_cours(os.path.join(racine, ENTREE))
        bnains, defauts_b, fausses = K.lire_paris(racine)   # le même Paris que le rejeu de K23 (R-708)
        a_defaire = K.lire_a_defaire(os.path.join(racine, K.VERDICTS_YAHOO))
        evenements = K.sans_les_divisions_fausses(json.load(open(os.path.join(racine, K.EVENEMENTS), encoding="utf-8")),
                                                  a_defaire)
        detachements, _ = K.lire_detachements(os.path.join(racine, K.DROITS), os.path.join(racine, K.OFFICIELS))
        francfort = K.lire_francfort(os.path.join(racine, K.FRANCFORT))
        indice = K.lire_indice(os.path.join(racine, K.INDICE))
    except (OSError, ValueError) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    if defauts or defauts_b:
        print(f"ARRÊT — défauts de lecture : {(defauts + defauts_b)[0]}")
        return 2
    sources = {(v, d): "yahoo" for v, s in series.items() for d in s}
    journal = []
    print(f"  ⓪ ajustements de Yahoo défaits : {len(a_defaire)}, lignes touchées : {defaire(series, a_defaire, journal)}")
    fenetres = {(v, d) for v, du, au, *_ in RECONSTRUCTIONS for d in series.get(v, {}) if du <= d <= au}
    arbitrages = K.arbitre_de_l_indice(series, bnains, evenements, indice, fenetres)
    tort_de_yahoo = {d for jours, *_, verdict in arbitrages if verdict == "le fichier a tort" for d in jours}
    douteux = K.jours_douteux(K.ecarts(series, bnains, exclure=fenetres))
    print(f"  barres bnains prouvées fausses, écartées : {len(fausses)} · jours douteux : {len(douteux)}, dont "
          f"{len(douteux & tort_de_yahoo)} où l'indice donne tort à Yahoo et non à bnains · séances où l'indice donne "
          f"tort à Yahoo : {len(tort_de_yahoo)}")
    arrets = reconstruire(series, sources, bnains, evenements, douteux, journal, detachements, francfort)
    arrets += retirer(series, sources, bnains, evenements, journal)
    if arrets:
        for a in arrets:
            print(f"ARRÊT — {a}")
        print("rien n'est écrit")
        return 1
    print(f"  ③bis séances recalées au jour du détachement : {recaler(series, sources, bnains, evenements, detachements, douteux, journal)}")
    ajustes, non_mesurables = ajuster(series, bnains, evenements, detachements, douteux, journal)
    print(f"  ③ter droits que Yahoo n'avait pas ajustés, ajustés : {ajustes} · non mesurables faute de bnains : "
          f"{len(non_mesurables)} {non_mesurables}")
    alignes, mesures = aligner(series, bnains, evenements, detachements, douteux, journal)
    mesures_ = {(v, d) for v, d, *_ in mesures}
    print(f"  ③ter-bis droits ajustés par Yahoo avec un autre facteur que la règle officielle, alignés : {alignes} "
          + " ".join(f"[{v} {d} : {100 * s:+.3f} % pour {100 * m:+.3f} %]" for v, d, s, m in mesures
                     if abs(s) > abs(m) / 4 and abs((1 + s) / (1 + m) - 1) > ALIGNEMENT)
          + " · non mesurables faute de bnains : "
          + str([f"{v} {d}" for v, jours in sorted(detachements.items()) for d in sorted(jours) if (v, d) not in mesures_]))
    print(f"  ③quater séances où l'indice CAC 40 donne tort à Yahoo, lignes remplacées : "
          f"{corriger(series, sources, bnains, evenements, tort_de_yahoo, douteux, detachements, journal)}")
    douteux = douteux - tort_de_yahoo       # ces jours-là, c'est Yahoo qui avait tort : bnains comble
    print(f"  ③quinquies clôtures de Yahoo démenties par bnains et Francfort, remplacées : "
          f"{trancher(series, sources, bnains, francfort, evenements, douteux, detachements, journal)}")
    for valeur, d, raison in BARRES_YAHOO_ECARTEES:
        if d in series.get(valeur, {}):
            noter(journal, valeur, d, "écarté", series[valeur][d][3], "", "",
                  raison,
                  "")
            del series[valeur][d]
            del sources[(valeur, d)]
    print(f"  ③sexies barres de Yahoo écartées sur décision de Jean-Luc, laissées au comblement : "
          f"{sum(1 for l in journal if l[2] == 'écarté')}")
    comblees = combler(series, sources, bnains, evenements, douteux, journal, detachements, francfort)
    trous = [f"{v} {d}" for v, d, _ in BARRES_YAHOO_ECARTEES if (v, d) in {(j[0], j[1]) for j in journal if j[2] == "écarté"}
             and d not in series.get(v, {})]
    if trous:      # relecture du 09-10-2026 : une barre écartée que bnains ne comble pas laissait un trou muet
        print(f"ARRÊT — barre(s) écartée(s) sur décision que le comblement n'a pas remplacée(s) : {' '.join(trous)}")
        print("rien n'est écrit")
        return 1
    for chemin, entete, lignes in (
            (SORTIE, COURS_MAITRE,
             [[v, d, *(texte(x) for x in series[v][d]), sources[(v, d)]] for v in sorted(series) for d in sorted(series[v])]),
            (JOURNAL, CHAMPS_JOURNAL, journal)):
        cible = os.path.join(racine, chemin)
        with open(cible + ".partiel", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(entete)
            w.writerows(lignes)
        os.replace(cible + ".partiel", cible)
    gestes = {}
    for l in journal:
        gestes[l[2]] = gestes.get(l[2], 0) + 1
    print(f"  ④ séances comblées : {comblees}")
    print(f"journal : {dict(sorted(gestes.items()))} · écrit : {SORTIE} ({sum(len(s) for s in series.values())} lignes) · {JOURNAL}")
    return 0


def main(argv):
    """Porte la ligne de commande ; rend le code de sortie.

    ① RÔLE — Vérifier l'argument et lancer `reparer`.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de `reparer`, ou 2 sans racine valable.
      [rend: 1]
    ⑥ TRAITEMENT — ⑤.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `reparer`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        print("USAGE : REPARER_L_HISTORIQUE_LONG.py <racine>")
        return 2
    return reparer(argv[0])


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as e:
        print(f"ARRÊT — erreur imprévue {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
