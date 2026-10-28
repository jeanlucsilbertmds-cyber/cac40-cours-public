#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROLER_L_HISTORIQUE_LONG.py — Dim 04-10-2026 (Paris) — PROPOSÉ, non validé (A-539, action ⑥).
Rôle : dire si un historique long des cours (26 ans, Yahoo réparé ou non) peut être versé, en le
confrontant à lui-même et à la seconde source, bnains.org. Il REFUSE toute série qui garde un des
défauts trouvés par Cowork le 04-10-2026. Il ne répare rien et n'écrit rien.
Simulation uniquement.

① RÔLE — Passer un historique long au crible des contrôles K1 à K22 (`controler`) et K23 (la remontée jusqu'à
  la source, A-578 : `lignes_non_rejouees`, `maillons_manquants`), dire pour chacun ce
  qu'il a trouvé, et refuser dès qu'un contrôle bloquant trouve quelque chose. Il porte aussi les
  DÉFINITIONS dont la réparation se sert — ce qu'est une séance manquante, un écart entre les deux
  sources, un jour douteux (les deux sources se contredisent pour cinq valeurs au moins), une séance
  où l'indice CAC 40 donne tort à l'une des deux — pour que réparer et contrôler mesurent la même chose
  (R-708 : deux implémentations d'une même chose divergent toujours).
② CONTEXTE D'APPEL — À la main, avant toute décision de verser l'historique long au fichier maître :
  python3 programmes/CONTROLER_L_HISTORIQUE_LONG.py <racine> [fichier à contrôler].
  Sans fichier : donnees/sources_yahoo/historique_long_repare.csv. Importé par
  programmes/REPARER_L_HISTORIQUE_LONG.py. Ses épreuves :
  tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py.
③ ENTRÉE — La racine du dépôt ; facultatif, le chemin du fichier à contrôler (relatif à la racine).
④ CONDITIONS D'ENTRÉE — Le fichier à contrôler porte au moins les colonnes valeur, date, open, high,
  low, close, volume (le fichier Yahoo déposé n'a pas la huitième, source ; le fichier réparé l'a).
  donnees/sources_bnains/bnains_cac40.csv et DROITS_BNAINS.csv existent
  (programmes/LIRE_LES_ARCHIVES_BNAINS.py), donnees/sources_yahoo/evenements.json (les
  divisions vues par Yahoo), et, écrits à la main, donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv
  et BARRES_BNAINS_FAUSSES.csv ; donnees/sources_francfort/COURS_DE_FRANCFORT.csv (la troisième source,
  écrite par etudes/outils/CONFRONTER_A_FRANCFORT.py) ; donnees/sources_indice/INDICE_CAC40.csv (l'indice
  CAC 40 relevé chez bnains et chez Yahoo, écrit par etudes/outils/LIRE_L_INDICE_CAC40.py) ; et
  donnees/sources_yahoo/yahoo_ohlcv_propre.csv (le fichier Yahoo avant réparation, auquel K18 et K20
  comparent) ; donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv (les ajustements de Yahoo jugés, dont ceux à
  défaire : `lire_a_defaire`).
⑤ SORTIE — UNE valeur : le code de sortie. 0 = aucun contrôle bloquant n'a rien trouvé · 1 = au
  moins un refus, chacun nommé · 2 = le contrôle n'a pas pu tourner (fichier absent, illisible,
  colonnes manquantes, ou toute erreur imprévue) — jamais 0 dans ce cas (R-734).
⑥ TRAITEMENT — ① lire le fichier (`lire_cours`) et l'extrait bnains, et en ôter les barres prouvées
  fausses (`oter_les_barres_fausses`) · ② calculer le calendrier, les
  écarts et les jours douteux · ③ passer les contrôles K1 à K22 (`controler`), puis K23 : pour un fichier réparé
  (déclaré dans CONTRATS.FICHIERS_REPARES, qui doit alors porter la colonne source ; ou qui la porte), chaque ligne refaite
  en rejouant le journal des réparations depuis sa ligne de Yahoo ou de Paris (`lignes_non_rejouees`), et la provenance du fichier Yahoo d'origine et de l'extrait de Paris déclarée jusqu'à un
  premier maillon — un téléchargement, ou un fichier écrit à la main qui cite ses sources (donnees/PROVENANCE_DES_FICHIERS.csv),
  et celle du fichier réparé lui-même, qui doit y être écrit par
  le programme déclaré ; pour un autre fichier, sa seule provenance · ④ afficher chaque
  contrôle : nombre trouvé, exemples, REFUS ou non · ⑤ sortir.
⑦ UNITÉ — Des NOMBRES DE LIGNES (une ligne = une valeur un jour de séance), des RAPPORTS de prix
  sans unité, des DATES de séance.
⑧ POURQUOI — Accord de Jean-Luc du 04-10-2026 pour un programme de contrôle (A-539, action ⑥ :
  « refuse toute série qui garde ces défauts »). Les seuils reprennent ceux des mesures de Cowork du
  même jour (relevé dans echanges/RELU.md, brouillons dans etudes/brouillons_cowork/), qui ont trouvé
  les défauts : médiane glissante de 41 séances, écart de 1 %, 25 valeurs pour faire une séance,
  20 jours par valeur et par année. Le contrôle est CALIBRÉ sur eux : passé sur le fichier Yahoo
  déposé, il doit retrouver les défauts que Cowork y a mesurés (épreuves, et passe ③ de la livraison).
⑨ CE QUI CLOCHE — Les seuils sont des PROPOSITIONS, non décidées par Jean-Luc. · Les barres bnains
  prouvées fausses (donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv, `oter_les_barres_fausses`) sont
  écartées avant tout calcul. · Au-delà du
  28-02-2017, dernière séance archivée par bnains, seuls les contrôles de forme s'appliquent : aucune
  seconde source ne recoupe 2017-2023. · Un écart entre les deux sources ne dit pas laquelle a tort ;
  quand cinq valeurs au moins s'écartent le même jour, l'indice CAC 40 l'attribue (K19,
  `arbitre_de_l_indice`) ; une valeur seule, Francfort la départage quand il le peut (K17). → BACKLOG.
  · K23 (13-10-2026, demande de Jean-Luc à 09h34 : « Tu ne vas pas oublier de le faire pour notre historique des
  20 ans », puis « Les deux, dans l'ordre ») est un VERROU : il refuse l'historique tant que chaque chiffre ne se
  remonte et ne se refait pas jusqu'à sa source. Il ne tient que si l'on lance ce contrôle : ni le versement au
  fichier maître (A-538) ni le juge des stratégies (A-577) ne l'appellent encore — à brancher quand ils seront
  écrits (A-578).
⑩ EFFET — Lit dix fichiers, plus le journal des réparations et le registre de provenance (K23) ; K23 lit en entier
  chaque fichier présent qu'il remonte (pour son empreinte), et lit ligne à ligne chaque fichier écrit à la main
  jusqu'au premier défaut. N'écrit rien.
  Affiche le compte rendu.
⑪ TERMINAISON — Toujours : chaque contrôle parcourt un nombre fini de lignes. Aucun de mes appels
  ne peut boucler.
"""
import bisect, csv, datetime, hashlib, json, math, os, re, statistics, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import (BARRES_BNAINS_FAUSSES, COURS_BNAINS, COURS_DE_FRANCFORT,   # les champs, déclarés une fois (R-708)
                                   DETACHEMENTS_OFFICIELS, DROITS_BNAINS, INDICE_CAC40, AJUSTEMENTS_DE_YAHOO,
                                   JOURNAL_DES_REPARATIONS, PROVENANCE_DES_FICHIERS, FICHIERS_REPARES,
                                   TELECHARGEMENT, ECRIT_A_LA_MAIN, COLONNES_DES_SOURCES_A_LA_MAIN,
                                   GESTES_DU_JOURNAL, SOURCE_YAHOO, SOURCE_PARIS)
import CALENDRIER_DE_LA_BOURSE as CAL   # les séances officielles d'Euronext, lues une seule façon (R-110, R-708)

BNAINS = os.path.join("donnees", "sources_bnains", "bnains_cac40.csv")
DROITS = os.path.join("donnees", "sources_bnains", "DROITS_BNAINS.csv")
OFFICIELS = os.path.join("donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv")
FAUSSES = os.path.join("donnees", "sources_bnains", "BARRES_BNAINS_FAUSSES.csv")
FRANCFORT = os.path.join("donnees", "sources_francfort", "COURS_DE_FRANCFORT.csv")
AVIS = 10               # Francfort est ramené à Paris sur 10 séances voisines au moins, à moins de PORTEE jours
ACCORD_FRANCFORT = 0.005   # Francfort confirme une barre bnains à 0,5 % près, ou à deux fois son bruit s'il est plus grand
INDICE = os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv")
ORIGINE = os.path.join("donnees", "sources_yahoo", "yahoo_ohlcv_propre.csv")   # le fichier Yahoo avant réparation
ACCORD_INDICE = 0.0005     # l'indice n'est cru qu'une séance où bnains et Yahoo le donnent à 0,05 % près
SOUPCON = 0.005            # une séance où 5 valeurs au moins (POUR_DOUTER) s'écartent de bnains de plus de 0,5 % passe à l'indice
MARGE = 3                  # l'indice départage quand les deux erreurs diffèrent de plus de 3 fois son bruit
PORTEE_POIDS = 150         # les poids des valeurs dans l'indice se mesurent sur les séances à moins de 150 jours
CRETE = 1e-4               # régularisation des poids : rend le système soluble quand deux valeurs bougent ensemble
ECART_DE_COTATION = 7   # un droit est vu chez bnains au plus 7 jours de calendrier après son détachement officiel
FICHIER = os.path.join("donnees", "sources_yahoo", "historique_long_repare.csv")
JOURNAL = os.path.join("donnees", "sources_yahoo", "journal_des_reparations.csv")   # écrit par la réparation
PROVENANCE = os.path.join("donnees", "PROVENANCE_DES_FICHIERS.csv")   # K23 : d'où vient chaque fichier (A-578)
# K23 : les deux sortes de premier maillon d'une chaîne (TELECHARGEMENT, ECRIT_A_LA_MAIN) sont déclarées au contrat
# (R-708)
DECIMALES = 4           # K23 : les barres prises à Paris sont écrites à 4 décimales, le volume entier (`arrondir`, seul
                        # calcul, appelé par `barre` de REPARER et par le rejeu — R-708)
MARCHE_EXACTE = 0.0005  # la marche d'une opération déclarée, dans le fichier, vaut la règle officielle à 0,05 % près
                        # (K22 ; et le seuil d'`aligner` dans la réparation). Mesuré le 10-10-2026 sur le fichier
                        # aligné : au pire 0,017 % (Saint-Gobain 2009), le bruit des médianes de cinq séances.
CHAMPS = ["valeur", "date", "open", "high", "low", "close", "volume"]
FENETRE = 41            # séances de la médiane glissante du rapport entre les deux sources, centrée
MINIMUM = 10            # points au moins dans la fenêtre, sinon pas d'écart calculé (bords de série)
ECART = 0.01            # un jour « en écart » s'écarte de plus de 1 % de la médiane glissante
POUR_DOUTER = 5         # une date où 5 valeurs au moins sont en écart est un JOUR DOUTEUX (l'indice dit qui a tort)
PAR_ANNEE = 20          # 20 jours d'écart, ou 20 barres plates, la même année pour une valeur : refus
NON_CORROBOREES = 20    # 20 lignes sans barre bnains alors que bnains a la séance : refus
SAUT = 0.25             # une variation de clôture à clôture de plus de 25 % est un saut
ACCORD = 0.02           # un saut est confirmé quand le rapport des deux sources bouge de moins de 2 %
EVENEMENTS = os.path.join("donnees", "sources_yahoo", "evenements.json")
VERDICTS_YAHOO = os.path.join("donnees", "sources_yahoo", "AJUSTEMENTS_DE_YAHOO.csv")   # dont les ajustements à défaire
DEFAIT = 1e-4           # K20 : le fichier doit porter le facteur à défaire à 0,01 % près
PROPRE = 0.002          # un jour est « d'accord » quand son rapport est à moins de 0,2 % du facteur mesuré
PART_PROPRE = 0.90      # il faut 90 % de jours d'accord pour croire un facteur
VOISINS = 5             # pour combler une séance : les 5 séances communes avant et les 5 après
PORTEE = 45             # … prises à moins de 45 jours de calendrier de la séance, et au moins une de chaque côté
LACUNE = 10             # 10 séances manquantes de suite dans une série : refus
FIN = 5                 # une série doit avoir une ligne parmi les 5 dernières séances du calendrier
AUTOUR = 5              # Yahoo pose parfois l'ajustement d'un droit jusqu'à 5 séances avant son détachement
NETTETE = 3             # K21 : la mesure tranche le jour d'une opération quand sa marche vaut au moins 3 fois le bruit propre de la valeur
BRUIT_SEANCES = 60      # K21 : le bruit propre se mesure sur les 60 séances qui précèdent la veille du jour déclaré
BRUIT_MINIMUM = 30      # K21 : au moins 30 écarts mesurés dans ces 60 séances, sinon pas de bruit, donc pas de verdict
VOISINAGE = 3           # K21 : le jour déclaré doit mieux s'expliquer par la marche que les 3 séances avant et les 3 après
# Les jours d'opération que la mesure ne tranche pas et qu'aucune phrase citée n'écrit, ACCEPTÉS PAR DÉCISION DE
# JEAN-LUC (K21b est bloquant) : valeur, jour, raison avec les mots de la décision. Un jour accepté qui ne
# correspond plus à aucune opération déclarée est refusé par K21b : une exception ne survit pas à son objet.
JOURS_ACCEPTES = (
    ("AXA", "2003-09-22",
     "décision de Jean-Luc du 09-10-2026 à 17h31 (« 1 » à « Répondre \"refusé\", et j'accepte AXA 2003 au 22-09-2003 en "
     "connaissance de cause ») : bons d'ORAN gratuits ; aucun document trouvé n'écrit le jour du détachement, déduit "
     "comme la séance qui suit l'enregistrement du 19-09-2003, date reprise de l'agent du lot 4 et non vérifiée"),
)


def lire_cours(chemin, champs=CHAMPS):
    """Lit un fichier de cours en colonnes et le range par valeur puis par date.

    ① RÔLE — Donner aux contrôles et à la réparation une seule façon de lire un fichier de cours.
    ② CONTEXTE D'APPEL — `main` (le fichier contrôlé, l'extrait bnains) ; REPARER_L_HISTORIQUE_LONG.
    ③ ENTRÉE — `chemin` : le fichier · `champs` : les colonnes exigées.
    ④ CONDITIONS D'ENTRÉE — Un fichier CSV en UTF-8 avec un en-tête.
    ⑤ SORTIE — TROIS valeurs : ① un dictionnaire valeur → {date: (open, high, low, close, volume)} en
      nombres, la première ligne gardée pour une (valeur, date) vue deux fois · ② la liste des
      défauts de lecture : lignes illisibles et (valeur, date) en double, chacune nommée · ③ les
      (valeur, date) dont la colonne source vaut « bnains » (vide si le fichier n'a pas cette colonne).
      Lève ValueError si une colonne exigée manque.
      [rend: 3]
    ⑥ TRAITEMENT — ① vérifier l'en-tête · ② pour chaque ligne, lire les cinq nombres ; une ligne
      illisible, ou dont un nombre est infini ou indéfini (« inf », « nan »), est nommée et sautée · ③ une (valeur, date) déjà vue est nommée, la seconde est sautée.
    ⑦ UNITÉ — Des EUROS et des NOMBRES DE TITRES.
    ⑧ POURQUOI — Un doublon gardé deux fois fausserait tous les comptes ; un doublon écrasé en
      silence cacherait une réparation qui écrit deux fois. « nan » et « inf » se lisent comme des
      nombres et passaient tous les contrôles (relecture indépendante du 04-10-2026 : « nan <= 0 »
      est faux).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le fichier. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    series, defauts, venues_de_bnains = {}, [], set()
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        manquants = [c for c in champs if c not in (lecteur.fieldnames or [])]
        if manquants:
            raise ValueError(f"{chemin} : colonne(s) absente(s) {manquants}")
        for n, r in enumerate(lecteur, 2):
            try:
                barre = tuple(float(r[c]) for c in ("open", "high", "low", "close", "volume"))
                if not all(math.isfinite(x) for x in barre):
                    raise ValueError("nombre infini ou indéfini")
            except (TypeError, ValueError) as e:
                defauts.append(f"ligne {n} illisible ({e}) : {r}")
                continue
            s = series.setdefault(r["valeur"], {})
            if r["date"] in s:
                defauts.append(f"{r['valeur']} {r['date']} en double (ligne {n})")
                continue
            s[r["date"]] = barre
            if r.get("source") == SOURCE_PARIS:
                venues_de_bnains.add((r["valeur"], r["date"]))
    return series, defauts, venues_de_bnains


def calendrier(series, seances):
    """Rend les dates de séance que le fichier doit couvrir : le calendrier OFFICIEL d'Euronext.

    ① RÔLE — Dire quels jours la Bourse était ouverte, entre la première et la dernière date du fichier.
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG (`reconstruire`, `combler`) ; les épreuves.
    ③ ENTRÉE — `series` : comme rendu par `lire_cours` · `seances` : le rendu de
      `CALENDRIER_DE_LA_BOURSE.lire_les_seances(racine)`, lu une fois par l'appelant.
    ④ CONDITIONS D'ENTRÉE — Les dates des séries sont écrites AAAA-MM-JJ ; `seances` couvre la période du
      fichier, sinon `CALENDRIER_DE_LA_BOURSE.seances_entre` dit ce qui manque.
    ⑤ SORTIE — UNE valeur : l'ensemble des dates AAAA-MM-JJ ; vide quand les séries n'ont aucune date.
      [rend: 1]
    ⑥ TRAITEMENT — ① la première et la dernière date de toutes les séries · ② les séances officielles entre les
      deux, bornes comprises.
    ⑦ UNITÉ — Des DATES.
    ⑧ POURQUOI — Une seule définition des séances dans tout le dépôt : deux définitions d'une même chose divergent
      toujours (R-708), et un calendrier tiré des cours prend une séance où toutes les valeurs manquent pour un jour
      de fermeture (R-110, rappelée par `programmes/CALENDRIER_DE_LA_BOURSE.py`). Jusqu'au 27-10-2026, cette fonction
      calculait les séances depuis les cours (au moins 25 valeurs avec une ligne, ou bnains) : elle
      écartait les cinq demi-séances des 24 et 31-12-2010, des 24 et 31-12-2012 et du 31-12-2015, où Yahoo n'a
      aucune ligne, avec pour raison « Yahoo ne les porte jamais » — démentie (BACKLOG A-555 (b) : Yahoo les porte
      en 2018 et 2019). Mesuré le 27-10-2026 : 6 839 séances calculées contre 6 844 officielles du 03-01-2000 au
      02-10-2026, l'écart étant ces cinq jours seulement. Décision de Jean-Luc du 27-10-2026 : les combler depuis
      bnains, avec toute leur trace (A-555 (b)).
    ⑨ CE QUI CLOCHE — Une série plus courte que le fichier se voit attribuer les séances du fichier entier, comme
      avant : ses séances avant sa première ligne ou après sa dernière sont écartées par `trous`, qui ne regarde
      qu'au milieu de chaque série.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur de `CALENDRIER_DE_LA_BOURSE.seances_entre`.
      [sort: non]
    """
    dates = [d for s in series.values() for d in s]
    if not dates:
        return set()
    a, z = datetime.date.fromisoformat(min(dates)), datetime.date.fromisoformat(max(dates))
    return {d.isoformat() for d, _ in CAL.seances_entre(a, z, seances)}


def trous(series, cal):
    """Rend les séances manquantes au milieu de chaque série.

    ① RÔLE — Trouver chaque (valeur, date) où la valeur devrait avoir une ligne et n'en a pas.
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG.
    ③ ENTRÉE — `series` · `cal` : le calendrier de `calendrier`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des (valeur, date).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque valeur : chaque date du calendrier entre sa première et sa dernière
      ligne, où elle n'a pas de ligne.
    ⑦ UNITÉ — Des LIGNES manquantes.
    ⑧ POURQUOI — Définition de Cowork (qualite_yahoo.py, contrôle 7), qui donne 222 sur le fichier
      Yahoo déposé ; reproduite au chiffre près (épreuves).
    ⑨ CE QUI CLOCHE — Une séance manquante avant la première ligne d'une valeur ne se voit pas.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    manque = []
    for v, s in series.items():
        if s:
            a, z = min(s), max(s)
            manque += [(v, d) for d in cal if a <= d <= z and d not in s]
    return sorted(manque)


def ecarts(series, bnains, exclure=()):
    """Rend, pour chaque (valeur, date) commune aux deux sources, l'écart du rapport des clôtures à sa médiane glissante.

    ① RÔLE — Mesurer où le fichier et bnains divergent, sans connaître les divisions ni les
      ajustements : un ajustement change le rapport d'un coup et pour longtemps, une erreur le change
      quelques jours.
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG (pour les jours douteux).
    ③ ENTRÉE — `series` · `bnains` : l'extrait lu par `lire_cours` · `exclure` : des (valeur, date)
      à laisser hors du calcul.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire (valeur, date) → écart (0,012 = 1,2 %), pour chaque date
      dont la fenêtre compte au moins `MINIMUM` points.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque valeur : ① les dates communes où les deux clôtures sont positives,
      hors `exclure`, triées · ② le rapport
      clôture du fichier / clôture bnains · ③ sa médiane sur `FENETRE` dates communes centrées sur
      chaque date · ④ l'écart = rapport / médiane − 1.
    ⑦ UNITÉ — Un RAPPORT sans unité.
    ⑧ POURQUOI — Méthode de Cowork (recouper.py) : sur le fichier Yahoo déposé, 150 740 séances
      communes et 1 509 jours à plus de 1 %.
    ⑨ CE QUI CLOCHE — Un ajustement qui change le rapport moins de 21 séances avant ou après un
      autre fait sortir quelques jours en écart sans erreur ; une erreur qui dure plus de 20
      séances devient la médiane et disparaît.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    exclure, sortie, demi = set(exclure), {}, FENETRE // 2
    for v, s in series.items():
        b = bnains.get(v, {})
        dates = sorted(d for d in s if d in b and b[d][3] > 0 and s[d][3] > 0 and (v, d) not in exclure)
        r = [s[d][3] / b[d][3] for d in dates]
        fen = sorted(r[:demi])
        for i, d in enumerate(dates):
            if i + demi < len(r):
                bisect.insort(fen, r[i + demi])
            if i - demi - 1 >= 0:
                del fen[bisect.bisect_left(fen, r[i - demi - 1])]
            if len(fen) >= MINIMUM:
                m = len(fen)
                med = fen[m // 2] if m % 2 else (fen[m // 2 - 1] + fen[m // 2]) / 2
                sortie[(v, d)] = r[i] / med - 1
    return sortie


def jours_douteux(ecart, seuil=ECART):
    """Rend les dates où au moins `POUR_DOUTER` valeurs sont en écart de plus de `seuil` (`ECART` par défaut).

    ① RÔLE — Désigner les séances où les deux sources se contredisent pour plusieurs valeurs à la fois :
      mal archivées par bnains, ou fausses chez Yahoo — `arbitre_de_l_indice` dit lequel.
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, qui ne prend une barre bnains un jour
      douteux que si Francfort la confirme, ou si l'indice donne tort à Yahoo ce jour-là ;
      `arbitre_de_l_indice`, avec le seuil `SOUPCON`, pour repérer les séances à juger.
    ③ ENTRÉE — `ecart` : le dictionnaire de `ecarts` · `seuil` : l'écart au-delà duquel une valeur compte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des dates.
      [rend: 1]
    ⑥ TRAITEMENT — Compter les valeurs en écart de plus de `seuil` par date ; garder celles à `POUR_DOUTER` ou plus.
    ⑦ UNITÉ — Des DATES.
    ⑧ POURQUOI — Mesuré par le Chat le 04-10-2026 : bnains porte, certains jours de 2006-2007
      (17-07-2006, 15-08-2006… 13-06-2007), des cours DÉJÀ AJUSTÉS de divisions et d'augmentations
      de capital qui n'avaient pas encore eu lieu — Air Liquide, Danone, EssilorLuxottica, Pernod
      Ricard, Vinci divisés par deux, Société Générale +12,7 %, BNP Paribas +2,9 %, les mêmes jours.
      Une barre de ces jours-là ne doit jamais remplacer une barre Yahoo. Le seuil de 5 ne dépend
      pas du choix : 33 dates à 4, 31 à 5, 29 à 6, 26 à 7.
    ⑨ CE QUI CLOCHE — Un jour douteux ne dit pas quelle source a tort ce jour-là : mesuré dans la nuit du
      07 au 08-10-2026, l'indice CAC 40 donne tort à Yahoo pour 16 des 32 jours douteux du fichier de
      Yahoo (05-07-2007, 26-07-2007, 07-05-2010, 13 séances de septembre 2011). Et une erreur de bnains
      sur une seule valeur ne fait pas un jour douteux.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    compte = {}
    for (v, d), e in ecart.items():
        if abs(e) > seuil:
            compte[d] = compte.get(d, 0) + 1
    return {d for d, n in compte.items() if n >= POUR_DOUTER}


def oter_les_barres_fausses(chemin, bnains):
    """Retire de l'extrait bnains les barres des fenêtres prouvées fausses ; rend les (valeur, date) retirées.

    ① RÔLE — Une seule façon d'écarter les barres bnains que des documents officiels contredisent, pour
      le contrôle et pour la réparation (REPARER_L_HISTORIQUE_LONG), qui mesurent ainsi la même chose.
    ② CONTEXTE D'APPEL — `main`, une fois, juste après la lecture de l'extrait ; REPARER_L_HISTORIQUE_LONG ;
      les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv · `bnains` : l'extrait,
      valeur → {date: barre}, modifié EN PLACE.
    ④ CONDITIONS D'ENTRÉE — Le fichier porte les colonnes de son contrat.
    ⑤ SORTIE — UNE valeur : l'ensemble des (valeur, date) retirées. Lève ValueError si l'en-tête n'est
      pas celui du contrat, si une date est illisible, ou si une fenêtre finit avant de commencer.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier l'en-tête · ② pour chaque fenêtre, vérifier ses deux dates · ③ retirer
      de l'extrait chaque barre de la valeur entre la première et la dernière séance, bornes comprises.
    ⑦ UNITÉ — Des LIGNES (valeur, date).
    ⑧ POURQUOI — Mesuré le 07-10-2026 : bnains porte, pour UNE valeur à la fois et sur plusieurs
      séances, des cours déjà ajustés d'un événement à venir — Société Générale du 14-09 au
      07-10-2009 (clôture officielle du 05-10-2009 : 52,20 € ; bnains 49,47 €), BNP Paribas du 14 au
      29-09-2009, Air Liquide avant ses attributions gratuites de 2012 et 2014 et avant son
      augmentation de capital de 2016, Schneider Electric, Bureau Veritas et Dassault Systèmes avant
      leurs divisions, TotalEnergies d'août à décembre 2016. Le jour douteux (`jours_douteux`) ne les
      voit pas : il faut cinq valeurs le même jour. Laissées dans l'extrait, ces barres faisaient
      refuser par K15 une série juste (Société Générale 2009) et cachaient un ajustement manquant
      (BNP Paribas 2009). Chaque fenêtre est une DONNÉE, prouvée par une source officielle.
    ⑨ CE QUI CLOCHE — Une fenêtre qui ne retire rien ne le dit pas ici : `main` affiche le nombre
      retiré. · Une fenêtre trop large retirerait des barres justes ; ses bornes viennent du rapport
      entre les deux sources, mesuré jour par jour (colonne « mesure »).
    ⑩ EFFET — Lit le fichier. Modifie `bnains`.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    retirees = set()
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != BARRES_BNAINS_FAUSSES:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {BARRES_BNAINS_FAUSSES}")
        for r in lecteur:
            du, au = (datetime.date.fromisoformat(r[c]).isoformat() for c in ("premiere_seance", "derniere_seance"))
            if au < du:
                raise ValueError(f"{chemin} : la fenêtre de {r['valeur']} finit le {au}, avant de commencer le {du}")
            barres = bnains.get(r["valeur"], {})
            for d in [d for d in barres if du <= d <= au]:
                del barres[d]
                retirees.add((r["valeur"], d))
    return retirees


def lire_paris(racine):
    """Lit l'extrait de Paris (bnains) et en ôte les barres prouvées fausses : le seul Paris de la réparation et du contrôle.

    ① RÔLE — Donner à la réparation, au contrôle et à ses épreuves les mêmes barres de Paris.
    ② CONTEXTE D'APPEL — `main` de ce programme ; `reparer` de programmes/REPARER_L_HISTORIQUE_LONG.py ; l'épreuve H56.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — L'extrait bnains et donnees/sources_bnains/BARRES_BNAINS_FAUSSES.csv existent (OSError
      sinon).
    ⑤ SORTIE — TROIS valeurs : les barres de Paris sans les barres prouvées fausses (`lire_cours`, valeur → {date :
      barre}) ; les défauts de lecture ; la liste des barres ôtées (`oter_les_barres_fausses`).
      [rend: 3]
    ⑥ TRAITEMENT — `lire_cours` de l'extrait, puis `oter_les_barres_fausses`.
    ⑦ UNITÉ — Des euros et des nombres de titres, cours bruts de Paris.
    ⑧ POURQUOI — Relecture n° 2 et superviseur n° 3 du 18-10-2026 (R-759) : le rejeu de K23 partait des barres de Paris
      lues AVANT le retrait des fausses, la réparation de celles d'APRÈS ; une ligne bâtie sur une barre déclarée fausse
      (Air Liquide, 27-04-2012) passait K1 à K23. L'assemblage existait à trois endroits (les deux `main` et
      l'épreuve) : deux implémentations d'une même chose divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — programmes/RECONSTRUIRE_L_HISTORIQUE_LONG.py et etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py
      assemblent encore Paris à leur façon, et l'épreuve tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py aussi, pour
      d'autres contrôles que K23 (une dizaine d'appels à `oter_les_barres_fausses`) ; tous équivalents aujourd'hui (→
      BACKLOG, A-597). · `main` n'est éprouvé sur aucune fenêtre fausse : l'extrait 2005 des épreuves n'en a pas ; c'est
      H56 qui garde cette fonction, et un `main` qui relirait bnains directement pour K23 passerait toutes les épreuves
      (relecteur n° 3 du 18-10-2026, sabotage X5 ; → A-597).
    ⑩ EFFET — Lit les deux fichiers.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    bnains, defauts, _ = lire_cours(os.path.join(racine, BNAINS), COURS_BNAINS)
    return bnains, defauts, oter_les_barres_fausses(os.path.join(racine, FAUSSES), bnains)


def lire_francfort(chemin):
    """Lit les clôtures de Francfort ; rend valeur → {date: clôture}.

    ① RÔLE — Donner au contrôle et à la réparation leur troisième source, lue d'une seule façon.
    ② CONTEXTE D'APPEL — `main` ; REPARER_L_HISTORIQUE_LONG ; les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_francfort/COURS_DE_FRANCFORT.csv.
    ④ CONDITIONS D'ENTRÉE — Le fichier porte les colonnes de son contrat.
    ⑤ SORTIE — UNE valeur : le dictionnaire valeur → {date: clôture}, sans les clôtures nulles,
      négatives ou illisibles. Lève ValueError si l'en-tête n'est pas celui du contrat.
      [rend: 1]
    ⑥ TRAITEMENT — Vérifier l'en-tête, puis ranger chaque clôture positive et finie.
    ⑦ UNITÉ — Des EUROS, tels que Yahoo les donne pour Francfort (ajustés de certaines opérations).
    ⑧ POURQUOI — Paris et Francfort cotent la même action : un écart durable entre eux est impossible
      sur un marché réel. Quand bnains et Yahoo se contredisent, Francfort départage (A-539, relecture
      de Cowork du 07-10-2026, 21h33).
    ⑨ CE QUI CLOCHE — Les cours de Francfort chez Yahoo sont ajustés de certaines opérations et pas
      d'autres : `avis_de_francfort` ne les compare donc qu'à des séances voisines.
    ⑩ EFFET — Lit le fichier. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    francfort = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != COURS_DE_FRANCFORT:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {COURS_DE_FRANCFORT}")
        for r in lecteur:
            try:
                c = float(r["close"])
            except ValueError:
                continue
            if c > 0 and math.isfinite(c):
                francfort.setdefault(r["valeur"], {})[r["date"]] = c
    return francfort


def avis_de_francfort(francfort, bnains, valeur, date, douteux):
    """Dit de combien la barre bnains d'un jour s'écarte de Francfort ; rend (écart, tolérance), ou (None, None).

    ① RÔLE — Une seule façon de demander à la troisième source si la barre de Paris archivée par bnains
      est juste un jour donné, pour trancher une barre de Yahoo (`barres_dementies`) et pour combler
      un jour douteux (`barre_sure`).
    ② CONTEXTE D'APPEL — `barres_dementies`, `barre_sure` ; les épreuves.
    ③ ENTRÉE — `francfort` : `lire_francfort` · `bnains` : l'extrait · `valeur`, `date` · `douteux`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : (None, None) quand Francfort se tait — pas de cours ce jour-là, le même
      cours que la veille, ou moins de `AVIS` séances voisines communes à moins de `PORTEE` jours ;
      sinon (écart, tolérance) : écart = (Francfort ÷ bnains ce jour-là) ÷ (sa médiane sur les
      voisins) − 1 ; tolérance = max(`ACCORD_FRANCFORT`, 2 × l'écart médian des voisins).
      [rend: 2]
    ⑥ TRAITEMENT — ① refuser de répondre si Francfort n'a rien ou répète la veille · ② prendre les
      `AVIS` séances communes avant et les `AVIS` après, hors jours douteux, à moins de `PORTEE` jours ·
      ③ rapporter Francfort à bnains sur elles, et ce jour-là.
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — Francfort clôt plus tard que Paris et y est parfois peu liquide : un seul jour ne se
      compare qu'à sa médiane sur les voisins, et la tolérance suit son bruit. Mesuré le 07-10-2026 :
      les jours où Yahoo manque Paris, Yahoo répète souvent aussi la veille pour Francfort ; un
      cours répété ne dit rien.
    ⑨ CE QUI CLOCHE — Des voisins de part et d'autre d'une opération que Yahoo ajuste à Francfort et pas
      bnains déplacent la médiane : le bruit grandit, la tolérance aussi, et l'avis devient moins
      tranchant — jamais plus.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    f, b = francfort.get(valeur, {}), bnains.get(valeur, {})
    if date not in f or date not in b or b[date][3] <= 0:
        return None, None
    precedent = max((x for x in f if x < date), default=None)
    if precedent is not None and f[precedent] == f[date]:
        return None, None
    communes = sorted(x for x in f if x in b and b[x][3] > 0 and x not in douteux and x != date)
    i = bisect.bisect_left(communes, date)
    jour = datetime.date.fromisoformat(date)
    voisins = [x for x in communes[max(0, i - AVIS):i] + communes[i:i + AVIS]
               if abs((datetime.date.fromisoformat(x) - jour).days) <= PORTEE]
    if len(voisins) < AVIS:
        return None, None
    r = [f[x] / b[x][3] for x in voisins]
    m = statistics.median(r)
    bruit = statistics.median(abs(x / m - 1) for x in r)
    return f[date] / b[date][3] / m - 1, max(ACCORD_FRANCFORT, 2 * bruit)


def barre_sure(bnains, francfort, valeur, date, douteux):
    """Dit si une barre bnains peut servir : utilisable, ou d'un jour douteux mais confirmée par Francfort.

    ① RÔLE — Une seule règle pour « bnains peut combler » (K6), pour le comblement et pour le
      remplacement d'une barre de Yahoo démentie (REPARER_L_HISTORIQUE_LONG).
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, `combler` et `trancher`.
    ③ ENTRÉE — `bnains` · `francfort` : `lire_francfort` · `valeur`, `date` · `douteux`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai quand `barre_utilisable` le dit, ou quand la barre est utilisable hors
      la règle du jour douteux ET que Francfort la confirme (écart d'`avis_de_francfort` dans sa
      tolérance) ; faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① `barre_utilisable` · ② sinon, la même sans jours douteux, puis l'avis de Francfort.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un jour douteux est faux pour CERTAINES valeurs (cinq au moins) : mesuré le
      07-10-2026 sur le fichier réparé de la version 7a22087, Francfort confirme la barre de 26 des 41
      séances manquantes qui ont une barre bnains utilisable hors la règle du jour douteux. Deux
      sources indépendantes qui s'accordent valent preuve.
    ⑨ CE QUI CLOCHE — Quand Francfort se tait, un jour douteux reste inutilisable.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if barre_utilisable(bnains, valeur, date, douteux):
        return True
    if not barre_utilisable(bnains, valeur, date, frozenset()):
        return False
    ecart, tolerance = avis_de_francfort(francfort, bnains, valeur, date, douteux)
    return ecart is not None and abs(ecart) <= tolerance


def facteur_du_jour(series, bnains, evenements, valeur, date, douteux, venues_de_bnains, detache=(), exiger_accord=True):
    """Mesure le facteur qui ramène bnains au fichier un jour donné, sans ce jour ; rend (prix, volume), ou (None, None).

    ① RÔLE — Une seule mesure du facteur d'un jour pour juger la ligne de ce jour : `barres_dementies`
      (une clôture de Yahoo démentie ?) et K15 (une couture qui marche, de quel côté ?).
    ② CONTEXTE D'APPEL — `barres_dementies` ; `controler`, K15.
    ③ ENTRÉE — `series`, `bnains` : par valeur puis par date · `evenements` · `valeur`, `date` ·
      `douteux` · `venues_de_bnains` · `detache` : les jours de détachement officiels de la valeur ·
      `exiger_accord` : vrai par défaut ; faux, la médiane des ouvertures est rendue même sans accord.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le facteur de prix et le facteur de volume ; (None, None) quand moins de
      `VOISINS` séances voisines, ou, si `exiger_accord`, moins de `PART_PROPRE` d'accord sur les
      ouvertures comme sur les clôtures.
      [rend: 2]
    ⑥ TRAITEMENT — ① les séances communes à la valeur et à bnains, prix positifs, hors `date`, hors
      jours douteux, hors lignes venues de bnains, du même côté que `date` de chaque détachement
      officiel · ② les `VOISINS` plus proches avant et après, à moins de `PORTEE` jours · ③ `rapports`
      sur les OUVERTURES ; s'ils ne s'accordent pas à `PART_PROPRE`, sur les clôtures ; sans accord,
      la médiane des ouvertures si `exiger_accord` est faux.
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — Mesuré le 07-10-2026 : Yahoo et bnains portent souvent la même ouverture, le même plus
      haut et le même plus bas, et seule la clôture diffère. Les ouvertures donnent donc le facteur
      même quand des clôtures fausses brouillent les voisines : Société Générale, septembre 2011,
      accord des clôtures 60 %, des ouvertures entier.
    ⑨ CE QUI CLOCHE — Sans accord, la médiane ne vaut que si une minorité des voisines est fausse :
      K15 seul s'en sert, pour dire de quel côté d'une couture vient la marche, jamais pour réparer.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s, b = series.get(valeur, {}), bnains.get(valeur, {})
    depuis = max((j for j in detache if j <= date), default="")
    jusqu_a = min((j for j in detache if j > date), default="9999-12-31")
    communes = sorted(x for x in s if x in b and x != date and x not in douteux and (valeur, x) not in venues_de_bnains
                      and depuis <= x < jusqu_a and min(b[x][0], b[x][3], s[x][0], s[x][3]) > 0)
    i = bisect.bisect_left(communes, date)
    jour = datetime.date.fromisoformat(date)
    voisins = [x for x in communes[max(0, i - VOISINS):i] + communes[i:i + VOISINS]
               if abs((datetime.date.fromisoformat(x) - jour).days) <= PORTEE]
    if len(voisins) < VOISINS:
        return None, None
    for colonne in (0, 3):
        prix, volume, accord = rapports(s, b, evenements, valeur, voisins, colonne)
        if accord >= PART_PROPRE:
            return prix, volume
    if not exiger_accord:
        prix, volume, _ = rapports(s, b, evenements, valeur, voisins, 0)
        return prix, volume
    return None, None


def barres_dementies(series, bnains, francfort, evenements, douteux, venues_de_bnains, detachements=None):
    """Cherche les barres du fichier qui s'écartent de bnains, et les fait départager par Francfort.

    ① RÔLE — Trouver les clôtures de Yahoo fausses hors de tout ajustement : celles que Paris (bnains)
      et Francfort démentent ensemble. Une seule définition pour le contrôle (K17) et pour la
      réparation (`trancher`).
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, `trancher` ; les épreuves.
    ③ ENTRÉE — `series` · `bnains` · `francfort` · `evenements` · `douteux` · `venues_de_bnains` :
      les lignes déjà venues de bnains, jamais jugées · `detachements` : `lire_detachements`, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des cas (valeur, date, écart du fichier à bnains, écart de
      Francfort à bnains, verdict, facteur de prix, facteur de volume), le verdict valant « fausse »
      (bnains et Francfort d'accord contre le fichier), « bnains faux » (Francfort d'accord avec le
      fichier), « non tranchée », « Francfort muet » ou « facteur instable » ; écarts et facteurs
      valent None quand ils n'ont pas pu se mesurer.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne du fichier qui a une barre bnains et n'en vient pas : ① tri rapide —
      rapport fichier ÷ bnains, divisions comprises, à plus de `ECART` de sa médiane sur les
      `VOISINS` séances de chaque côté · ② facteur du jour sans la ligne (`facteur_du_jour`) ;
      instable → « facteur instable » ; écart du fichier à ce facteur au plus `ECART` → rien · ③ avis de Francfort sur la barre bnains (`avis_de_francfort`) : muet →
      « Francfort muet » ; bnains confirmé et fichier à plus de `ECART` de Francfort → « fausse » ;
      fichier dans la tolérance de Francfort → « bnains faux » ; sinon « non tranchée ».
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — Relecture de Cowork du 07-10-2026, 21h33 : 359 barres de Yahoo restaient à plus de
      1 % de bnains, et K8 les tolérait jusqu'à 20 par valeur et par an. Mesuré le même soir :
      Yahoo et bnains portent souvent la MÊME ouverture, le même plus haut, le même plus bas, et
      seule la clôture diffère — BNP Paribas, 13-09-2011 : Yahoo 27,15, bnains 28,00, Francfort
      27,995. Deux sources indépendantes contre une : la clôture de Yahoo est fausse.
    ⑨ CE QUI CLOCHE — Francfort muet, ou au bruit trop fort, laisse le cas « non tranchée » : il est
      signalé (K17b), pas réparé. · Le tri rapide manque une barre fausse de moins de `ECART`.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cas = []
    for v, s in sorted(series.items()):
        b, jours = bnains.get(v, {}), (detachements or {}).get(v, {})
        dates = [d for d in sorted(s) if d in b and b[d][3] > 0 and s[d][3] > 0]
        q = {d: s[d][3] * divisions(evenements, v, d) / b[d][3] for d in dates}
        for i, d in enumerate(dates):
            if (v, d) in venues_de_bnains:
                continue
            proches = [q[x] for x in dates[max(0, i - VOISINS):i] + dates[i + 1:i + 1 + VOISINS]]
            if len(proches) < VOISINS or abs(q[d] / statistics.median(proches) - 1) <= ECART:
                continue
            facteur, volume = facteur_du_jour(series, bnains, evenements, v, d, douteux, venues_de_bnains, jours)
            if facteur is None:
                cas.append((v, d, None, None, "facteur instable", None, None))
                continue
            ecart = q[d] / facteur - 1
            if abs(ecart) <= ECART:
                continue
            ecart_f, tolerance = avis_de_francfort(francfort, bnains, v, d, douteux)
            if ecart_f is None:
                cas.append((v, d, ecart, None, "Francfort muet", facteur, volume))
                continue
            contre_fichier = abs((1 + ecart_f) / (1 + ecart) - 1)
            verdict = ("fausse" if abs(ecart_f) <= tolerance and contre_fichier > ECART
                       else "bnains faux" if contre_fichier <= tolerance else "non tranchée")
            cas.append((v, d, ecart, ecart_f, verdict, facteur, volume))
    return cas


def lire_indice(chemin):
    """Lit l'indice CAC 40 relevé à deux sources ; rend date → clôture, pour les séances où elles s'accordent.

    ① RÔLE — Donner à `arbitre_de_l_indice` un indice dont chaque séance est un fait : deux relevés indépendants
      qui s'accordent.
    ② CONTEXTE D'APPEL — `main` ; REPARER_L_HISTORIQUE_LONG ; les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_indice/INDICE_CAC40.csv (etudes/outils/LIRE_L_INDICE_CAC40.py).
    ④ CONDITIONS D'ENTRÉE — Le fichier porte les colonnes de son contrat.
    ⑤ SORTIE — UNE valeur : le dictionnaire date → clôture de bnains, pour les seules séances où bnains et Yahoo
      sont tous deux lisibles et positifs et s'accordent à `ACCORD_INDICE` près. Lève ValueError si l'en-tête
      n'est pas celui du contrat.
      [rend: 1]
    ⑥ TRAITEMENT — Vérifier l'en-tête ; garder chaque séance où les deux relevés s'accordent.
    ⑦ UNITÉ — Des POINTS d'indice.
    ⑧ POURQUOI — Mesuré le 07-10-2026 : 4 358 séances communes, 7 à plus de 0,05 % l'une de l'autre — dont le
      19 et le 20-06-2001, où bnains porte les deux clôtures interverties. Ces séances-là ne prouvent rien.
    ⑨ CE QUI CLOCHE — Après le 28-02-2017, bnains n'a rien : l'indice ne départage plus rien, et il n'y a plus
      rien à départager (Yahoo seul).
    ⑩ EFFET — Lit le fichier. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    indice = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != INDICE_CAC40:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {INDICE_CAC40}")
        for r in lecteur:
            try:
                b, y = float(r["bnains"]), float(r["yahoo"])
            except ValueError:
                continue
            if b > 0 and y > 0 and abs(y / b - 1) <= ACCORD_INDICE:
                indice[r["date"]] = b
    return indice


def resoudre(a, r):
    """Résout le système linéaire a·x = r (méthode de Gauss, pivot partiel) ; rend x.

    ① RÔLE — Calculer les poids des valeurs dans l'indice sans dépendre d'une bibliothèque.
    ② CONTEXTE D'APPEL — `arbitre_de_l_indice`.
    ③ ENTRÉE — `a` : matrice carrée (liste de lignes) · `r` : second membre, de même longueur.
    ④ CONDITIONS D'ENTRÉE — `a` est inversible : `arbitre_de_l_indice` lui ajoute `CRETE` sur la diagonale.
    ⑤ SORTIE — UNE valeur : la liste x.
      [rend: 1]
    ⑥ TRAITEMENT — Triangulariser en prenant à chaque colonne le plus grand pivot, puis remonter.
    ⑦ UNITÉ — Celle du problème.
    ⑧ POURQUOI — Le programme ne dépend que de Python : il tourne partout où Python tourne.
    ⑨ CE QUI CLOCHE — Un pivot nul lève ZeroDivisionError ; `CRETE` l'empêche.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Toujours : deux boucles bornées par la taille.
      [sort: non]
    """
    n = len(a)
    m = [list(a[i]) + [r[i]] for i in range(n)]
    for i in range(n):
        k = max(range(i, n), key=lambda x: abs(m[x][i]))
        m[i], m[k] = m[k], m[i]
        for x in range(i + 1, n):
            f = m[x][i] / m[i][i]
            for j in range(i, n + 1):
                m[x][j] -= f * m[i][j]
    sol = [0.0] * n
    for i in reversed(range(n)):
        sol[i] = (m[i][n] - sum(m[i][j] * sol[j] for j in range(i + 1, n))) / m[i][i]
    return sol


def arbitre_de_l_indice(series, bnains, evenements, indice, exclure=()):
    """Dit, pour chaque suite de séances où le fichier et bnains se contredisent, lequel reproduit l'indice CAC 40.

    ① RÔLE — Attribuer la faute quand deux sources se contredisent sur plusieurs valeurs le même jour. L'indice
      est calculé par Euronext à partir des clôtures officielles : les vraies clôtures le reproduisent.
    ② CONTEXTE D'APPEL — `controler`, K19 ; REPARER_L_HISTORIQUE_LONG, `reparer` ; les épreuves.
    ③ ENTRÉE — `series` : le fichier jugé (Yahoo avant réparation, ou le fichier réparé) · `bnains` · `evenements`
      · `indice` : `lire_indice` · `exclure` : des (valeur, date) à ne pas compter pour repérer les séances
      (les fenêtres que la réparation reconstruit).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des suites, chacune (séances, nombre de valeurs, bruit, erreur de bnains,
      erreur du fichier, marge, verdict). Le verdict vaut « le fichier a tort » (marge > `MARGE`), « bnains a
      tort » (marge < −`MARGE`), « indifférent », ou « non mesurable » (aucune séance de la suite n'a l'indice,
      suite au bord, poids non estimables) ; bruit, erreurs et marge valent alors None.
      [rend: 1]
    ⑥ TRAITEMENT — ① SÉANCES SOUPÇONNÉES : celles où `POUR_DOUTER` valeurs au moins s'écartent de bnains de plus
      de `SOUPCON` (`jours_douteux` au seuil `SOUPCON`), groupées en suites consécutives sur le calendrier fait des séances de l'indice et
      des séances soupçonnées — une séance soupçonnée sans indice reste dans sa suite, et le pas qui l'enjambe
      se mesure d'un bout à l'autre (07-09-2011 : bnains n'a pas l'indice ce jour-là) · ② pour une suite, la
      séance propre d'avant (c0) et celle d'après (c1), et entre elles les seules séances qui ont l'indice ; les valeurs présentes chez les deux sources de c0 à c1,
      dont le rapport fichier ÷ bnains, divisions comprises, ne bouge pas de plus de `SOUPCON` de c0 à c1 (aucun
      ajustement entre les deux) · ③ POIDS : moindres carrés, régularisés de `CRETE`, du rendement de l'indice
      sur les rendements des valeurs, aux séances propres consécutives à moins de `PORTEE_POIDS` jours où les
      deux sources s'accordent à `PROPRE` près pour toutes ces valeurs — il en faut deux par valeur ; le bruit
      est l'écart-type des résidus · ④ sur chaque pas de c0 à c1, l'écart du rendement de l'indice au rendement
      pondéré, une fois avec les clôtures de bnains, une fois avec celles du fichier ; on somme les écarts
      absolus · ⑤ marge = (erreur du fichier − erreur de bnains) ÷ (bruit × racine du nombre de pas).
    ⑦ UNITÉ — Erreurs et bruit en RENDEMENTS (0,01 = 1 point) ; marge en nombre de bruits.
    ⑧ POURQUOI — Relecture de Cowork du 07-10-2026, 23h04 : remplacer une clôture de Yahoo au milieu de clôtures
      de Yahoo elles-mêmes fausses rendait 13 rendements PLUS faux (BNP Paribas, 12→13-09-2011 : 0,73 point
      d'erreur avant, 2,61 après). Mesuré le même soir : du 29-08 au 16-09-2011, Yahoo porte une autre clôture
      que Paris pour les deux tiers des valeurs, chaque séance, et aucune avant ni après ; Francfort, qui clôt
      plus tard, ne départage qu'un jour sur deux. L'indice, lui, tranche : marge +10,9 pour la suite entière ;
      +55 le 07-05-2010 ; et, à l'inverse, −150 à −258 pour les séances de 2006-2007 où bnains porte des
      barres fausses. Les jours « douteux chez bnains » mêlaient donc les deux fautes.
    ⑨ CE QUI CLOCHE — Le verdict porte sur la SÉANCE, pas sur chaque valeur : une valeur juste chez le perdant
      reste juste, et c'est à l'appelant de ne changer que les lignes qui s'écartent. · Les poids sont estimés,
      pas lus : là où les séances propres manquent (2006-2007), la suite est « non mesurable ».
    ⑩ EFFET — —
    ⑪ TERMINAISON — Toujours : un nombre fini de suites, chacune un système de la taille du nombre de valeurs.
      [sort: non]
    """
    soupconnees = jours_douteux(ecarts(series, bnains, exclure), SOUPCON)
    seances = sorted(indice)
    sortie, suites, cours = [], [], []
    for d in sorted(set(indice) | soupconnees):     # une séance soupçonnée sans indice reste DANS sa suite
        if d in soupconnees:
            cours.append(d)
        elif cours:
            suites.append(cours)
            cours = []
    if cours:
        suites.append(cours)

    def lisible(v, d):
        """Dit si une valeur a, un jour donné, une clôture positive chez les deux sources, hors des lignes exclues.

        ① RÔLE — Choisir les valeurs et les séances qui entrent dans le calcul des poids et des écarts.
        ② CONTEXTE D'APPEL — `arbitre_de_l_indice`, pour chaque valeur et chaque séance de la suite et des voisines.
        ③ ENTRÉE — `v` : la valeur · `d` : la date ; et, de l'appelant, `series`, `bnains`, `exclure`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai ou faux.
          [rend: 1]
        ⑥ TRAITEMENT — La ligne existe dans le fichier et chez bnains, les deux clôtures sont positives, et
          (v, d) n'est pas dans `exclure`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une clôture absente ou nulle ne donne pas de rendement ; une ligne que la réparation
          reconstruit ne doit pas juger.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return d in series.get(v, {}) and d in bnains.get(v, {}) and series[v][d][3] > 0 and bnains[v][d][3] > 0 \
            and (v, d) not in exclure

    def paris(v, d):
        """Rend la clôture de Paris (bnains) d'un jour, ramenée aux divisions que le fichier a déjà appliquées.

        ① RÔLE — Comparer des rendements de Paris et du fichier sans qu'une division d'action les sépare.
        ② CONTEXTE D'APPEL — `arbitre_de_l_indice`, après `lisible`.
        ③ ENTRÉE — `v` : la valeur · `d` : la date ; et, de l'appelant, `bnains`, `evenements`.
        ④ CONDITIONS D'ENTRÉE — `lisible(v, d)` est vrai.
        ⑤ SORTIE — UNE valeur : la clôture de bnains divisée par `divisions` de ce jour.
          [rend: 1]
        ⑥ TRAITEMENT — Une division.
        ⑦ UNITÉ — Des EUROS, à l'échelle du fichier pour les divisions (pas pour les droits).
        ⑧ POURQUOI — Le fichier est ajusté des divisions, bnains non : sans cela, une division entre deux
          séances ferait un rendement de −50 % chez Paris seulement.
        ⑨ CE QUI CLOCHE — Les droits de souscription ne sont pas ramenés : une suite qui en enjambe un sort du
          calcul, faute de rapport stable de c0 à c1 (`SOUPCON`).
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return bnains[v][d][3] / divisions(evenements, v, d)

    for suite in suites:
        i, j = bisect.bisect_left(seances, suite[0]), bisect.bisect_right(seances, suite[-1])
        mesurees = [d for d in suite if d in indice]
        if i == 0 or j == len(seances) or not mesurees:
            sortie.append((tuple(suite), 0, None, None, None, None, "non mesurable"))
            continue
        chemin = [seances[i - 1]] + mesurees + [seances[j]]
        c0, c1 = chemin[0], chemin[-1]
        vals = sorted(v for v in series if all(lisible(v, x) for x in chemin)
                      and abs(series[v][c1][3] / paris(v, c1) / (series[v][c0][3] / paris(v, c0)) - 1) <= SOUPCON)
        milieu = datetime.date.fromisoformat(suite[len(suite) // 2])
        proches = [x for x in seances if abs((datetime.date.fromisoformat(x) - milieu).days) <= PORTEE_POIDS]
        lignes, cible = [], []
        for a, z in zip(proches, proches[1:]):
            if a in soupconnees or z in soupconnees or not all(lisible(v, a) and lisible(v, z) for v in vals):
                continue
            rp = [paris(v, z) / paris(v, a) - 1 for v in vals]
            if any(abs(series[v][z][3] / series[v][a][3] - 1 - x) > PROPRE for v, x in zip(vals, rp)):
                continue
            lignes.append(rp)
            cible.append(indice[z] / indice[a] - 1)
        if not vals or len(cible) < 2 * len(vals):
            sortie.append((tuple(suite), len(vals), None, None, None, None, "non mesurable"))
            continue
        n = len(vals)
        a = [[sum(l[x] * l[y] for l in lignes) + (CRETE if x == y else 0) for y in range(n)] for x in range(n)]
        poids = resoudre(a, [sum(l[x] * c for l, c in zip(lignes, cible)) for x in range(n)])
        bruit = statistics.pstdev(c - sum(w * x for w, x in zip(poids, l)) for l, c in zip(lignes, cible))
        e_bnains = e_fichier = 0.0
        for a_, z in zip(chemin, chemin[1:]):
            ri = indice[z] / indice[a_] - 1
            e_bnains += abs(ri - sum(w * (paris(v, z) / paris(v, a_) - 1) for w, v in zip(poids, vals)))
            e_fichier += abs(ri - sum(w * (series[v][z][3] / series[v][a_][3] - 1) for w, v in zip(poids, vals)))
        marge = (e_fichier - e_bnains) / (bruit * math.sqrt(len(chemin) - 1)) if bruit > 0 else 0.0
        verdict = "le fichier a tort" if marge > MARGE else "bnains a tort" if marge < -MARGE else "indifférent"
        sortie.append((tuple(suite), n, bruit, e_bnains, e_fichier, marge, verdict))
    return sorted(sortie)


def rendements_degrades(series, origine, bnains, evenements, venues_de_bnains, detachements=None):
    """Cherche les rendements qu'une ligne remplacée rend plus éloignés de Paris que le fichier d'origine.

    ① RÔLE — Vérifier qu'une réparation n'abîme pas ce qu'elle touche : le rendement d'une ligne remplacée avec
      ses voisines doit être au moins aussi proche de celui de Paris (bnains) qu'avant.
    ② CONTEXTE D'APPEL — `controler`, K18 ; les épreuves.
    ③ ENTRÉE — `series` : le fichier réparé · `origine` : le fichier Yahoo avant réparation · `bnains` ·
      `evenements` · `venues_de_bnains` : les lignes du fichier venues de bnains · `detachements` :
      `lire_detachements`, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des cas (valeur, date de départ, date d'arrivée, écart avant, écart après),
      écarts en rendement (0,01 = 1 point), pour chaque rendement dont l'écart après dépasse l'écart avant de
      plus de `SOUPCON`.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne venue de bnains qui existait dans `origine` (remplacée, pas comblée) :
      avec la séance précédente et la suivante du fichier réparé, si les deux dates sont dans `origine` et ont
      une barre bnains utilisable (`barre_utilisable`, sans la règle du jour douteux), comparer |rendement réparé − rendement de Paris| à |rendement d'origine − rendement de Paris|,
      Paris pris divisions comprises, et, quand la séance d'arrivée est un jour de détachement
      officiel, droit compris : (1 + rendement de Paris) × (1 + marche permise) − 1.
    ⑦ UNITÉ — Des RENDEMENTS.
    ⑧ POURQUOI — Relecture de Cowork du 07-10-2026, 23h04, proposition 2 : 13 rendements devenaient plus faux
      autour des barres remplacées, et aucun contrôle ne le voyait (BNP Paribas, 12→13-09-2011 : 0,73 point
      avant, 2,61 après).
    ⑨ CE QUI CLOCHE — Une ligne comblée n'a pas de rendement d'origine : elle n'est pas jugée ici, mais par K15.
      · Une barre bnains plate sans volume n'est pas un cours de Paris : Hermès, 14-09-2011, bnains 268,30 quatre
      fois et volume nul — pris pour Paris, il faisait paraître le rendement réparé plus faux qu'avant.
      · Un rendement qui enjambe un droit que Yahoo ajuste et bnains non porte la valeur du droit des deux côtés
      de la comparaison ; elle s'annule à `SOUPCON` près. · Un droit que Yahoo n'a PAS ajusté et que la
      réparation ajuste (AXA, bons d'ORAN, 22-09-2003, ajouté le 09-10-2026, A-555 ⑥) ne s'annulait pas :
      Paris brut donnait −5,58 %, la courbe ajustée −4,21 %, Yahoo −5,88 %, et le contrôle refusait une
      réparation juste. D'où Paris pris droit compris au jour du détachement : la courbe juste est
      alors la plus proche.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Toujours : chaque ligne venue de bnains est vue une fois.
      [sort: non]
    """
    cas = []
    for v, s in sorted(series.items()):
        o, b, dates = origine.get(v, {}), bnains.get(v, {}), sorted(s)
        vus = set()
        for i, d in enumerate(dates):
            if (v, d) not in venues_de_bnains or d not in o:
                continue
            for paire in ([(dates[i - 1], d)] if i else []) + ([(d, dates[i + 1])] if i + 1 < len(dates) else []):
                p, q = paire
                if paire in vus or not all(x in o and o[x][3] > 0 and barre_utilisable(bnains, v, x, frozenset())
                                           for x in paire):
                    continue
                vus.add(paire)
                rp = b[q][3] / divisions(evenements, v, q) / (b[p][3] / divisions(evenements, v, p)) - 1
                droit = (detachements or {}).get(v, {}).get(q)
                rp_brut = rp
                if droit is not None:
                    rp = (1 + rp) * (1 + marche_permise(b, droit)) - 1
                # relecture du 09-10-2026 : l'origine est jugée contre la meilleure des deux références,
                # Paris brut (Yahoo n'a pas ajusté) ou droit compris (Yahoo a ajusté) ; sinon la marche
                # entière servait de tolérance et cachait une vraie dégradation ce jour-là
                avant = min(abs(o[q][3] / o[p][3] - 1 - rp), abs(o[q][3] / o[p][3] - 1 - rp_brut))
                apres = abs(s[q][3] / s[p][3] - 1 - rp)
                if apres > avant + SOUPCON:
                    cas.append((v, p, q, avant, apres))
    return cas


def barre_utilisable(bnains, valeur, date, douteux):
    """Dit si la barre bnains d'une valeur un jour donné peut remplacer ou combler une barre du fichier.

    ① RÔLE — Une seule règle pour « bnains peut combler » (contrôle K6) et pour « la réparation
      prend cette barre » (REPARER_L_HISTORIQUE_LONG).
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, à chaque barre qu'il voudrait prendre.
    ③ ENTRÉE — `bnains` : l'extrait · `valeur`, `date` · `douteux` : les jours de `jours_douteux`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — Vrai quand bnains a la barre, que le jour n'est pas douteux, que le volume est
      positif et que la barre est cohérente (prix positifs, plus bas ≤ ouverture et clôture ≤ plus haut).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un jour douteux porte des cours ajustés d'avance (⑧ de `jours_douteux`) ; une barre
      sans volume n'est pas une séance où l'on a échangé ; une barre incohérente est fausse (AXA,
      05-10-2005 : clôture 22,77 sous le plus bas 22,84, lu dans l'extrait le 04-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    b = bnains.get(valeur, {}).get(date)
    return (b is not None and date not in douteux and b[4] > 0
            and 0 < b[2] <= min(b[0], b[3]) <= max(b[0], b[3]) <= b[1])


def divisions(evenements, valeur, date):
    """Rend le produit des rapports des divisions de `valeur` POSTÉRIEURES à `date`.

    ① RÔLE — Dire par combien Yahoo a divisé les cours d'un jour pour les rendre comparables à
      aujourd'hui.
    ② CONTEXTE D'APPEL — `rapports`, `facteur_local` ; REPARER_L_HISTORIQUE_LONG, à chaque barre.
    ③ ENTRÉE — `evenements` : le contenu de evenements.json · `valeur` · `date`.
    ④ CONDITIONS D'ENTRÉE — `evenements[valeur]["divisions"]` est une liste de [date, nouveau,
      ancien], ou absent.
    ⑤ SORTIE — UNE valeur : un nombre (4 pour AXA avant le 16-05-2001, 1 après).
      [rend: 1]
    ⑥ TRAITEMENT — Multiplier nouveau / ancien pour chaque division datée APRÈS `date`.
    ⑦ UNITÉ — Un RAPPORT sans unité.
    ⑧ POURQUOI — bnains donne les cours bruts du jour ; Yahoo les divise par les divisions venues
      ensuite. Le jour même de la division, le cours est déjà divisé : la comparaison est stricte.
    ⑨ CE QUI CLOCHE — Une division que Yahoo ne déclare pas n'est pas connue ici.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    f = 1.0
    for jour, nouveau, ancien in evenements.get(valeur, {}).get("divisions", []):
        if date < jour:
            f *= nouveau / ancien
    return f


def rapports(yahoo, bnains, evenements, valeur, dates, colonne=3):
    """Rend le facteur de prix et le facteur de volume entre une série et bnains sur des dates, et leur accord.

    ① RÔLE — Mesurer la convention de Yahoo pour une valeur, là où les deux sources ont la même séance.
    ② CONTEXTE D'APPEL — `facteur_local`, `barres_dementies` ; REPARER_L_HISTORIQUE_LONG (période de
      référence, témoin).
    ③ ENTRÉE — `yahoo`, `bnains` : les séries d'UNE valeur, par date · `evenements` · `valeur` (pour
      ses divisions) · `dates` · `colonne` : le prix comparé, 3 la clôture (par défaut), 0 l'ouverture.
    ④ CONDITIONS D'ENTRÉE — Chaque date est dans les deux séries.
    ⑤ SORTIE — TROIS valeurs : le facteur de prix (médiane du prix × divisions / prix bnains, sur la
      `colonne` choisie),
      le facteur de volume (médiane de volume / (volume bnains × divisions), None sans volume bnains),
      la part des dates où le rapport de prix est à moins de `PROPRE` du facteur. Sans date :
      (None, None, 0).
      [rend: 3]
    ⑥ TRAITEMENT — Calculer les deux rapports par date, en prendre les médianes, compter l'accord.
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — La médiane ne se laisse pas tirer par quelques jours faux ; la part d'accord dit si
      les dates sont sûres.
    ⑨ CE QUI CLOCHE — Le facteur de volume n'est pas jugé sur son accord.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not dates:
        return None, None, 0
    prix = [yahoo[d][colonne] * divisions(evenements, valeur, d) / bnains[d][colonne] for d in dates]
    vol = [yahoo[d][4] / (bnains[d][4] * divisions(evenements, valeur, d)) for d in dates if bnains[d][4] > 0]
    f = statistics.median(prix)
    return f, (statistics.median(vol) if vol else None), sum(abs(p / f - 1) <= PROPRE for p in prix) / len(prix)


def facteur_local(series, bnains, evenements, valeur, date, douteux, venues_de_bnains, detache=()):
    """Mesure, autour d'une séance manquante, le facteur qui ramène bnains à la convention du fichier.

    ① RÔLE — Une seule règle pour « combler est sûr » (contrôle K6) et pour le comblement
      (REPARER_L_HISTORIQUE_LONG).
    ② CONTEXTE D'APPEL — `controler`, par séance manquante ; REPARER_L_HISTORIQUE_LONG.
    ③ ENTRÉE — `series`, `bnains` : par valeur puis par date · `evenements` · `valeur` · `date`, une
      date où la valeur n'a PAS de ligne ·
      `douteux` · `venues_de_bnains` : (valeur, date) des lignes déjà venues de bnains · `detache` : les
      jours de détachement officiels de la valeur (`lire_detachements`), vide par défaut.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — QUATRE valeurs : facteur de prix, facteur de volume, accord, nombre de voisins ; le
      facteur de prix vaut None quand combler n'est pas sûr : aucun voisin d'un côté — sauf quand un
      jour de détachement officiel coupe ce côté à moins de `PORTEE` jours —, moins de `VOISINS`
      voisins en tout, ou moins de `PART_PROPRE` d'accord.
      [rend: 4]
    ⑥ TRAITEMENT — ① les séances communes à la valeur et à bnains, hors jours douteux et hors lignes
      venues de bnains, et du même côté que la séance de chaque jour de détachement officiel (le
      dernier jour de détachement à la séance ou avant elle, compris ; le premier après elle, exclu) ·
      ② les `VOISINS` plus proches avant et les `VOISINS` plus proches après, chacune à moins de
      `PORTEE` jours · ③ `rapports` sur elles.
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — Mesuré le 04-10-2026 : Yahoo manque souvent le jour même d'un ajustement (BNP
      Paribas 06-03-2006, Crédit Agricole 03-01-2007 et 05-06-2008, Vinci 29-03-2006) ; le facteur
      change entre la veille et le lendemain, et rien ne dit de quel côté tombe la séance manquante.
      Avec les plus proches voisins, un changement à côté de la séance fait tomber l'accord sous 90 %
      et la séance n'est pas comblée ; un changement plus loin ne laisse qu'une minorité de voisins
      de l'autre côté. Les lignes venues de bnains sont exclues : elles diraient que bnains s'accorde
      avec lui-même. Un côté vide, ou des voisins lointains, cachent un changement de facteur : la
      relecture indépendante du 04-10-2026 a comblé AXA en mars 2004 avec des voisins de novembre
      2009 seulement, au facteur 1,0 au lieu de 0,9771 (2,3 % d'erreur, contrôle muet). Mais quand
      le changement est un détachement officiel, on sait de quel côté tombe la séance : la veille
      du détachement prend le facteur d'avant. Mesuré le 07-10-2026 : quatre des cinq séances
      laissées pour cette raison sont des veilles de détachement officiel (BNP Paribas 06-03-2006,
      Crédit Agricole 03-01-2007 et 05-06-2008, Vinci 29-03-2006).
    ⑨ CE QUI CLOCHE — Un côté coupé par un détachement laisse des voisins d'un seul côté : un
      changement de facteur inconnu de ce côté-là ne se verrait que par l'accord.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    y, b = series.get(valeur, {}), bnains.get(valeur, {})
    jour = datetime.date.fromisoformat(date)
    proche = lambda x: abs((datetime.date.fromisoformat(x) - jour).days) <= PORTEE
    depuis = max((j for j in detache if j <= date), default="")       # même régime d'ajustement que la séance
    jusqu_a = min((j for j in detache if j > date), default="9999-12-31")
    communes = sorted(x for x in y if x in b and x not in douteux and (valeur, x) not in venues_de_bnains
                      and depuis <= x < jusqu_a)
    i = bisect.bisect_left(communes, date)
    avant = [x for x in communes[max(0, i - VOISINS): i] if proche(x)]
    apres = [x for x in communes[i: i + VOISINS] if proche(x)]
    voisins = avant + apres
    f, k, accord = rapports(y, b, evenements, valeur, voisins)
    coupe_avant = bool(depuis) and proche(depuis)                       # un détachement officiel ferme ce côté
    coupe_apres = jusqu_a != "9999-12-31" and proche(jusqu_a)
    if (not avant and not coupe_avant) or (not apres and not coupe_apres) or len(voisins) < VOISINS \
            or accord < PART_PROPRE:
        return None, k, accord, len(voisins)
    return f, k, accord, len(voisins)


def seances_comparables(serie, barres, douteux):
    """Rend, dans l'ordre, les séances d'une valeur où le fichier et bnains se comparent.

    ① RÔLE — Une seule définition des séances sur lesquelles on mesure le rapport aux cours bruts,
      pour le contrôle K15 et pour le recalage (REPARER_L_HISTORIQUE_LONG).
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, `recaler`.
    ③ ENTRÉE — `serie`, `barres` : la série du fichier et celle de bnains d'UNE valeur, par date ·
      `douteux` : les jours de `jours_douteux`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des dates.
      [rend: 1]
    ⑥ TRAITEMENT — Garder les dates du fichier que bnains a aussi, aux deux clôtures positives, hors
      jours douteux.
    ⑦ UNITÉ — Des DATES.
    ⑧ POURQUOI — Deux définitions d'une même chose divergent toujours (R-708) : avant le 06-10-2026,
      le recalage ne demandait pas une clôture positive au fichier, le contrôle si.
    ⑨ CE QUI CLOCHE — Une séance du fichier sans barre bnains, ou un jour douteux, n'est pas vue.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [d for d in sorted(serie) if d in barres and barres[d][3] > 0 and serie[d][3] > 0 and d not in douteux]


def marche_mesuree(serie, barres, evenements, valeur, jour, douteux):
    """Rend la marche du rapport série ÷ cours bruts au jour d'une opération, ou None si rien ne la mesure.

    ① RÔLE — UNE seule mesure de la marche qu'une série ajustée fait au jour d'une opération, pour la réparation
      (`ajuster`, `aligner`) et pour le contrôle K22 (R-708 : deux implémentations d'une même chose divergent).
    ② CONTEXTE D'APPEL — `controler` (K22) ; REPARER_L_HISTORIQUE_LONG, `ajuster` et `aligner`.
    ③ ENTRÉE — `serie` : la série ajustée d'une valeur · `barres` : sa série bnains · `evenements` : les divisions
      gardées · `valeur` : son nom · `jour` : le jour de l'opération · `douteux` : les jours douteux.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la marche (0,02 pour +2 %), ou None quand aucune séance comparable n'existe d'un côté.
      [rend: 1]
    ⑥ TRAITEMENT — Sur les séances comparables (`seances_comparables`), le rapport clôture ajustée × divisions
      postérieures ÷ clôture brute ; la médiane des `VOISINS` séances d'avant le jour, celle des `VOISINS` à partir
      du jour ; la marche est la seconde ÷ la première − 1.
    ⑦ UNITÉ — Un RAPPORT sans unité.
    ⑧ POURQUOI — La mesure vivait deux fois dans la réparation (`ajuster`, puis `aligner` le 10-10-2026) ; la
      relecture indépendante du 10-10-2026 a demandé que le contrôle la refasse (K22) : elle vit ici, une fois.
    ⑨ CE QUI CLOCHE — Après le 28-02-2017, bnains manque : None (Euronext 2021, Veolia 2021).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    dates = seances_comparables(serie, barres, douteux)
    i = bisect.bisect_left(dates, jour)       # la première séance comparable à partir du jour
    if i == 0 or i == len(dates):
        return None
    r = lambda x: serie[x][3] * divisions(evenements, valeur, x) / barres[x][3]
    avant = statistics.median(r(x) for x in dates[max(0, i - VOISINS):i])
    apres = statistics.median(r(x) for x in dates[i:i + VOISINS])
    return apres / avant - 1


def marches_inexactes(series, bnains, evenements, detachements, douteux):
    """Rend les opérations déclarées dont la marche, dans le fichier, n'est pas la règle officielle à `MARCHE_EXACTE` près.

    ① RÔLE — Le contrôle K22 : chaque opération déclarée porte-t-elle, dans le fichier, exactement sa marche ?
    ② CONTEXTE D'APPEL — `controler` ; les épreuves.
    ③ ENTRÉE — `series` : le fichier contrôlé · `bnains` : l'extrait, barres fausses ôtées · `evenements` ·
      `detachements` : `lire_detachements`, ou None · `douteux` : les jours douteux.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des cas, chacun un texte (valeur, jour, marche du fichier, marche officielle).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque opération déclarée que `marche_mesuree` mesure : refuser quand (1 + marche du
      fichier) ÷ (1 + `marche_permise`) s'écarte de 1 de plus de `MARCHE_EXACTE`.
    ⑦ UNITÉ — Des RAPPORTS.
    ⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 à 09h39 : la règle officielle partout. La relecture
      indépendante du même jour a montré que rien ne la gardait : K15 tolère 1 %, et K20 lit le journal que la
      réparation écrit elle-même — un fichier faux de 0,5 % avant le 05-06-2008 chez Crédit Agricole, avec un
      journal assorti, passait ; et Vinci 2006, faux de +0,25 % le temps d'un premier jet, passait aussi.
    ⑨ CE QUI CLOCHE — Une opération que bnains ne mesure pas (après le 28-02-2017) n'est pas jugée. · La règle
      officielle elle-même vient des chiffres déclarés : un chiffre faux dans DETACHEMENTS_OFFICIELS.csv donnerait
      une règle fausse, que le fichier suivrait et que K22 accepterait.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    cas = []
    for valeur, jours in sorted((detachements or {}).items()):
        y, b = series.get(valeur, {}), bnains.get(valeur, {})
        for d, droit in sorted(jours.items()):
            s = marche_mesuree(y, b, evenements, valeur, d, douteux)
            m = marche_permise(b, droit)
            if s is not None and abs((1 + s) / (1 + m) - 1) > MARCHE_EXACTE:
                cas.append(f"{valeur} {d} : marche du fichier {100 * s:+.3f} %, règle officielle {100 * m:+.3f} %")
    return cas


def autour_du_detachement(dates, jour):
    """Rend la séance d'ancrage et les séances qui précèdent un détachement, là où Yahoo peut poser l'ajustement.

    ① RÔLE — Une seule définition de « autour d'un détachement », pour le contrôle K15 et pour le
      recalage (REPARER_L_HISTORIQUE_LONG).
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, `recaler`.
    ③ ENTRÉE — `dates` : les séances de `seances_comparables` · `jour` : un jour de détachement.
    ④ CONDITIONS D'ENTRÉE — `dates` est triée.
    ⑤ SORTIE — DEUX valeurs : la séance d'ancrage (celle qui précède la fenêtre, None quand la série
      commence dans la fenêtre) et la liste des `AUTOUR` séances au plus qui précèdent `jour`. Quand
      `jour` n'est pas dans `dates` : (None, []).
      [rend: 2]
    ⑥ TRAITEMENT — Prendre les `AUTOUR` séances qui précèdent `jour` dans `dates`, et celle d'avant.
    ⑦ UNITÉ — Des DATES (séances comparables, non des jours de calendrier).
    ⑧ POURQUOI — Mesuré le 07-10-2026 sur les huit droits que la série Yahoo couvre, aux jours de
      détachement officiels : Yahoo change de facteur le jour même pour AXA, Crédit Agricole,
      Danone, Michelin, Pernod Ricard et Veolia ; pour Société Générale en octobre 2009 aussi — on
      avait cru le contraire jusqu'au 07-10-2026, parce que bnains y porte des cours faux du 14-09 au
      07-10 (`oter_les_barres_fausses`) ; pour Société Générale en février 2008, il le change deux fois, la veille
      (0,8934 le 19-02 → 0,8363 le 20-02, −6,4 %) et le jour même (→ 0,9478 le 21-02). Avant le
      détachement, le facteur est celui de la séance d'ancrage. `AUTOUR` couvre le cas mesuré le
      plus large (1 séance) avec de la marge.
    ⑨ CE QUI CLOCHE — Un ajustement posé plus de `AUTOUR` séances avant le détachement n'est pas vu
      ici ; K15b le signale encore, sans refus.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if jour not in dates:
        return None, []
    i = dates.index(jour)
    return (dates[i - AUTOUR - 1] if i > AUTOUR else None), dates[max(0, i - AUTOUR):i]


def controler(series, defauts, bnains, evenements, venues_de_bnains=frozenset(), detachements=None, sans_date=(),
              fausses=frozenset(), francfort=None, indice=None, origine=None, a_defaire=(), citations=None,
              alignes=None, seances=None):
    """Passe les contrôles K1 à K21 ; rend leur compte rendu.

    ① RÔLE — Tout ce que le programme juge.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves.
    ③ ENTRÉE — `series`, `defauts`, `venues_de_bnains` : rendus par `lire_cours` sur le fichier ·
      `bnains` : l'extrait · `evenements` : le contenu de evenements.json · `detachements` : valeur
      → {jour officiel de détachement : (clôture du droit, son premier jour chez bnains)}, ou None ·
      `sans_date` : les manques rendus par `lire_detachements` · `fausses` : les (valeur, date) que
      `oter_les_barres_fausses` a retirées de l'extrait · `francfort` : `lire_francfort`, ou None (aucun
      avis de Francfort : K17 ne trouve rien, K17b signale tout) · `indice` : `lire_indice`, ou None (K19 ne
      juge rien) · `origine` : le fichier Yahoo avant réparation, ou None (K18 et K20 ne jugent rien) ·
      `a_defaire` : `lire_a_defaire`, ou vide (K20 ne juge rien) · `citations` : `lire_citations`, ou None
      (K21b ne juge que les jours acceptés sans opération ou en double ; K21c rien) · `alignes` :
      `lire_alignes`, ou None (K20 attend alors chaque ligne sans geste « aligné ») · `seances` : le rendu de
      `CALENDRIER_DE_LA_BOURSE.lire_les_seances`, pour `calendrier` (K6 et K7 : depuis le 27-10-2026, les séances
      manquantes se comptent sur le calendrier officiel) ; sans lui, `calendrier` lève une erreur.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une liste de quadruplets (numéro, intitulé, bloquant, liste des cas),
      un par contrôle, dans l'ordre K1 à K21.
      [rend: 1]
    ⑥ TRAITEMENT — K1 lignes illisibles ou en double · K2 barre incohérente (plus bas au-dessus de
      l'ouverture ou de la clôture, plus haut au-dessous) ou prix nul ou négatif · K3 volume nul ou
      négatif · K4 séance un samedi ou un dimanche · K5 valeur-année à `PAR_ANNEE` barres plates ou
      plus (ouverture = plus haut = plus bas = clôture) · K6 séance manquante que bnains peut
      combler sûrement (`barre_utilisable` et `facteur_local`) · K7 séance manquante que rien ne comble
      (NON bloquant : à combler, décision de Jean-Luc) · K8 valeur-année à `PAR_ANNEE` jours d'écart
      ou plus avec bnains · K9 valeur à `NON_CORROBOREES` lignes ou plus sur des séances que bnains
      archive sans cette valeur, hors barres prouvées fausses (`fausses`) · K10 saut de plus de `SAUT` que bnains contredit (bloquant) ; les
      sauts que bnains ne peut pas vérifier sont listés sans refus (K10b) · K11 `LACUNE` séances du
      calendrier manquantes de suite dans une série · K12 série sans ligne parmi les `FIN` dernières
      séances du calendrier · K13 valeur que bnains archive jusqu'à sa dernière séance et que le
      fichier n'a pas · K14 (non bloquant) série qui commence `FIN` séances ou plus après bnains ·
      K15 entre deux séances qui se suivent dont l'une au moins vient de bnains — une COUTURE, ou
      deux lignes posées par la réparation —, le rapport fichier/bnains, divisions comprises, change
      de plus de `ECART` de la marche permise : zéro, sauf quand un jour de détachement tombe entre
      les deux séances, celle d'arrivée comprise — la marche permise est alors la valeur du droit
      (`marche_permise`), même si le jour du détachement n'est pas lui-même une séance comparable
      (barre bnains fausse ce jour-là : Air Liquide, 14-09-2016) ; K15 juge aussi,
      même entre deux séances venues de Yahoo, toute marche qui arrive dans les `AUTOUR` séances qui
      précèdent un détachement ou le jour même (`autour_du_detachement`) · K15b (non bloquant) le
      même écart entre deux séances venues de Yahoo, ailleurs, et la couture entre une ligne venue de
      bnains et une ligne de Yahoo quand la ligne de bnains est, à `ECART` près, au facteur du jour
      (`facteur_du_jour`, médiane des ouvertures des voisines, même sans accord) et que la ligne de Yahoo s'en écarte de plus : la marche vient alors de la
      ligne de Yahoo, qui s'écartait déjà de bnains avant la réparation (Airbus, 06→07-04-2009 : le 06
      remplacé, deux sources contre Yahoo ; le 07, Yahoo 9,40, bnains 9,57, Francfort 9,72, que rien
      ne tranche) — une ligne de bnains au mauvais facteur s'écarte, elle, du facteur du jour, et
      reste refusée · K16 droit de souscription d'une
      valeur du fichier sans jour de détachement officiel, ou à un jour impossible (`lire_detachements`)
      · K17 ligne venue de Yahoo que bnains et Francfort démentent ensemble (`barres_dementies`) ·
      K17b (non bloquant) les autres écarts de plus de `ECART` à bnains, avec leur verdict · K18 rendement
      qu'une ligne remplacée rend plus éloigné de Paris que le fichier d'origine (`rendements_degrades`) ·
      K19 suite de séances où l'indice CAC 40 donne tort au fichier (`arbitre_de_l_indice`) · K19b (non
      bloquant) les suites que l'indice ne départage pas, ou ne peut pas mesurer · K20 ligne de Yahoo d'une valeur
      à défaire qui ne porte pas exactement la correction (`portes`) : avant la date, quatre prix × facteur et
      volume ÷ facteur, à `DEFAIT` près ; à partir de la date, inchangée · K21 opération déclarée par un
      document dont la mesure des cours contredit le jour (`dates_declarees`) · K21b celles qu'elle ne peut
      pas trancher, dont la citation n'écrit pas le jour et que Jean-Luc n'a pas acceptées (`JOURS_ACCEPTES`),
      et les jours acceptés sans opération · K21c (non bloquant) les jours acceptés, rappelés. K6 et K7
      jugent avec `barre_sure` : une barre d'un jour douteux que Francfort confirme peut combler.
    ⑦ UNITÉ — Des LIGNES, des valeur-années.
    ⑧ POURQUOI — Chaque contrôle porte un défaut trouvé par Cowork le 04-10-2026 : K5 AXA 2001-2007
      (735 barres plates), K6 et K7 les 222 séances manquantes, K8 AXA 2001-2007 et
      EssilorLuxottica 2000-2001, K9 Engie avant le 08-07-2005 (les cours de Suez, que bnains archive
      sous un autre code), K10 les sauts de plus de 25 %. K1 à K4 sont les contrôles de forme de son
      brouillon qualite_yahoo.py. K11 à K14 viennent de la relecture indépendante du Chat du
      04-10-2026 : une archive bnains amputée de deux mois, une valeur retirée entière, une série
      coupée en 2012 passaient toutes, code 0. Le seuil de K11 laisse passer la plus longue lacune
      réelle, Bouygues du 03 au 10-11-2011 (6 séances, relevé de Cowork). K15 vient des relectures
      de Cowork du 04-10-2026 : une série ajustée ne peut changer de rapport aux cours bruts qu'un
      jour de détachement ; ailleurs, c'est un mouvement que la Bourse n'a pas fait. Et ce jour-là,
      la marche a une taille : la valeur du droit détaché (sans cette borne, AXA reconstruit 5 % trop
      bas sur dix ans passait en 0). Mesuré sur AXA : marche +2,34 % le 10-11-2009, droit 0,413 sur
      une action à 16,725, soit +2,47 %. Relecture de Cowork du 05-10-2026 : Société Générale gardait
      −12,02 % le 20-02-2008, là où Paris fait −6,01 % ; cette marche, entre deux séances de Yahoo,
      ne faisait que se signaler (K15b) et le contrôle rendait 0. Autour d'un détachement, le
      rapport ne change qu'UNE fois, le jour même, de la valeur du droit. K16 vient de la relecture
      du Chat du 07-10-2026 : le jour du détachement était pris au premier jour de cotation du droit
      chez bnains, qui vient souvent une séance trop tard (⑧ de `lire_detachements`) ; la couture
      juste d'AXA du 10-11-2009 avait été prise pour fausse, et Danone, Michelin, Pernod Ricard
      recalés à tort.
    ⑨ CE QUI CLOCHE — K8 et K9 ne portent que jusqu'à la dernière séance de bnains (28-02-2017).
      · K10 ne regarde que la clôture. · K14 n'est pas bloquant : Yahoo commence plusieurs séries
      après bnains (Airbus, Publicis…), et les compléter n'est pas demandé — mais une série amputée
      de son début ne fait donc que se signaler.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cal = calendrier(series, seances)
    ecart = ecarts(series, bnains)
    douteux = jours_douteux(ecart)
    arbitrages = arbitre_de_l_indice(series, bnains, evenements, indice) if indice is not None else []
    seances_bnains = {d for s in bnains.values() for d in s}
    fin_bnains = max(seances_bnains) if seances_bnains else ""
    k2, k3, k4, plates = [], [], [], {}
    for v, s in sorted(series.items()):
        for d, (o, h, l, c, vol) in sorted(s.items()):
            if min(o, h, l, c) <= 0 or not l <= min(o, c) <= max(o, c) <= h:
                k2.append(f"{v} {d}")
            if vol <= 0:
                k3.append(f"{v} {d}")
            if datetime.date.fromisoformat(d).weekday() >= 5:
                k4.append(f"{v} {d}")
            if o == h == l == c and vol > 0:
                plates[(v, d[:4])] = plates.get((v, d[:4]), 0) + 1
    francfort = francfort or {}
    k6, k7 = [], []
    for v, d in trous(series, cal):
        if not barre_sure(bnains, francfort, v, d, douteux):
            k7.append(f"{v} {d}" + (" (bnains : barre fausse, écartée)" if (v, d) in fausses else
                                    "" if d not in bnains.get(v, {}) else " (bnains : jour douteux)"
                                    if d in douteux else " (bnains : barre sans échange ou incohérente)"))
        elif facteur_local(series, bnains, evenements, v, d, douteux, venues_de_bnains,
                           (detachements or {}).get(v, {}))[0] is None:
            k7.append(f"{v} {d} (le facteur change à côté : ajustement du jour ?)")
        else:
            k6.append(f"{v} {d}")
    par_an = {}
    for (v, d), e in ecart.items():
        if abs(e) > ECART:
            par_an[(v, d[:4])] = par_an.get((v, d[:4]), 0) + 1
    non_corr = {}
    for v, s in series.items():
        n = sum(1 for d in s if d in seances_bnains and d not in bnains.get(v, {}) and (v, d) not in fausses)
        if n >= NON_CORROBOREES:
            non_corr[v] = n
    k10, k10_libres = [], []
    for v, s in sorted(series.items()):
        dates, b = sorted(s), bnains.get(v, {})
        for p, q in zip(dates, dates[1:]):
            if s[p][3] <= 0 or s[q][3] <= 0 or abs(s[q][3] / s[p][3] - 1) <= SAUT:
                continue                       # une clôture nulle ou négative est déjà refusée par K2
            cas = f"{v} {p}→{q} {100 * (s[q][3] / s[p][3] - 1):+.1f} %"
            if p in b and q in b and b[p][3] > 0 and b[q][3] > 0:
                if abs((s[q][3] / b[q][3]) / (s[p][3] / b[p][3]) - 1) > ACCORD:
                    k10.append(cas + " — bnains ne le montre pas")
            else:
                k10_libres.append(cas + (" — après la fin de bnains" if q > fin_bnains else " — bnains n'a pas les deux séances"))
    ordre = sorted(cal)
    rang = {d: i for i, d in enumerate(ordre)}
    k11, k12 = [], []
    for v, s in sorted(series.items()):
        a, z = min(s), max(s)
        manque = sorted(rang[d] for d in cal if a <= d <= z and d not in s)
        suite, debut = 0, None
        for i, j in enumerate(manque):
            suite = suite + 1 if i and j == manque[i - 1] + 1 else 1
            debut = ordre[j] if suite == 1 else debut
            if suite == LACUNE:
                k11.append(f"{v} à partir du {debut}")
        if ordre and max(s) < ordre[-min(FIN, len(ordre))]:
            k12.append(f"{v} s'arrête le {max(s)}, le calendrier va jusqu'au {ordre[-1]}")
    k13 = [f"{v} : bnains l'archive jusqu'au {fin_bnains}" for v, b in sorted(bnains.items())
           if b and max(b) == fin_bnains and v not in series]
    k14 = []
    for v, s in sorted(series.items()):
        b, premier = bnains.get(v, {}), min(s)
        avant = [d for d in b if d < premier and d in rang]
        if len(avant) >= FIN:
            k14.append(f"{v} commence le {premier} ; bnains a {len(avant)} séances avant, dès le {min(b)}")
    k17, k17b = [], []
    for v, d, ecart, ecart_f, verdict, _, _ in barres_dementies(series, bnains, francfort, evenements, douteux,
                                                                venues_de_bnains, detachements):
        cas = f"{v} {d}" + (f" fichier {100 * ecart:+.1f} % de bnains" if ecart is not None else "") + (
            f", Francfort {100 * ecart_f:+.1f} %" if ecart_f is not None else "")
        if verdict == "fausse":
            k17.append(cas)
        else:
            k17b.append(f"{cas} — {verdict}")
    k15, k15b = [], []
    for v, s in sorted(series.items()):
        b, detache = bnains.get(v, {}), (detachements or {}).get(v, {})
        dates = seances_comparables(s, b, douteux)
        surveilles = {q for d in detache for q in autour_du_detachement(dates, d)[1] + [d]}
        for p, q in zip(dates, dates[1:]):
            rp = s[p][3] * divisions(evenements, v, p) / b[p][3]
            rq = s[q][3] * divisions(evenements, v, q) / b[q][3]
            entre = [j for j in detache if p < j <= q]     # le jour du détachement peut manquer aux séances comparables
            permise = 1.0
            for j in entre:                    # le droit vaut d sur une action ex-droit à a : marche d / a
                permise *= 1 + marche_permise(b, detache[j])
            permise -= 1
            if abs(rq / rp - 1 - permise) <= ECART:
                continue
            cas = f"{v} {p}→{q} rapport {100 * (rq / rp - 1):+.1f} %" + (
                f", le droit détaché n'en permet que {100 * permise:+.1f} %" if entre else "")
            if q in surveilles or entre:
                k15.append(cas)
            elif (v, p) in venues_de_bnains or (v, q) in venues_de_bnains:
                x, z = (p, q) if (v, p) in venues_de_bnains else (q, p)          # x vient de bnains
                f = facteur_du_jour(series, bnains, evenements, v, x, douteux, venues_de_bnains, detache, False)[0] \
                    if (v, z) not in venues_de_bnains else None
                rx, rz = (rp, rq) if x == p else (rq, rp)
                if f is not None and abs(rx / f - 1) <= ECART < abs(rz / f - 1):
                    k15b.append(cas + f" — la ligne de bnains du {x} est au facteur du jour ; c'est la ligne de Yahoo du "
                                      f"{z} qui s'en écarte, écart déjà là avant la réparation")
                else:
                    k15.append(cas)
            else:
                k15b.append(cas)
    k21, k21b, k21c, k21_jugees = dates_declarees(bnains, detachements, citations, evenements)
    return [
        ("K1", "lignes illisibles ou en double", True, defauts),
        ("K2", "barres incohérentes ou prix ≤ 0", True, k2),
        ("K3", "volume ≤ 0", True, k3),
        ("K4", "séances un samedi ou un dimanche", True, k4),
        ("K5", f"valeur-années à {PAR_ANNEE} barres plates ou plus", True,
         [f"{v} {a} : {n}" for (v, a), n in sorted(plates.items()) if n >= PAR_ANNEE]),
        ("K6", "séances manquantes que bnains peut combler", True, k6),
        ("K7", "séances manquantes que rien ne comble — à combler, décision de Jean-Luc", False, k7),
        ("K8", f"valeur-années à {PAR_ANNEE} jours ou plus d'écart > {ECART:.0%} avec bnains", True,
         [f"{v} {a} : {n}" for (v, a), n in sorted(par_an.items()) if n >= PAR_ANNEE]),
        ("K9", f"valeurs à {NON_CORROBOREES} lignes ou plus que bnains n'archive pas un jour qu'il archive", True,
         [f"{v} : {n}" for v, n in sorted(non_corr.items())]),
        ("K10", f"sauts de plus de {SAUT:.0%} contredits par bnains", True, k10),
        ("K10b", f"sauts de plus de {SAUT:.0%} que bnains ne peut pas vérifier (non bloquant)", False, k10_libres),
        ("K11", f"lacunes de {LACUNE} séances de suite ou plus dans une série", True, k11),
        ("K12", f"séries qui s'arrêtent avant les {FIN} dernières séances du calendrier", True, k12),
        ("K13", "valeurs que bnains archive jusqu'à sa dernière séance et que le fichier n'a pas", True, k13),
        ("K14", f"séries qui commencent {FIN} séances ou plus après bnains (non bloquant)", False, k14),
        ("K15", f"marches du rapport aux cours bruts à plus de {ECART:.0%} de la marche permise, touchant une ligne "
                f"venue de bnains ou arrivant dans les {AUTOUR} séances qui précèdent un détachement, ou le jour même",
         True, k15),
        ("K15b", f"les mêmes marches entre deux séances venues de Yahoo, loin de tout détachement (non bloquant)", False, k15b),
        ("K16", "droits de souscription d'une valeur du fichier sans jour de détachement officiel, ou à un jour impossible",
         True, [m for v, m in sans_date if v in series]),
        ("K17", f"lignes à plus de {ECART:.0%} de bnains que bnains et Francfort démentent ensemble", True, k17),
        ("K17b", f"les autres lignes à plus de {ECART:.0%} de bnains, et ce qu'en dit Francfort (non bloquant)", False, k17b),
        ("K18", f"rendements qu'une ligne remplacée rend plus éloignés de Paris que le fichier d'origine, de plus de "
                f"{SOUPCON:.1%}", True,
         [f"{v} {p}→{q} écart à Paris {100 * a:.2f} pt avant, {100 * b:.2f} pt après"
          for v, p, q, a, b in (rendements_degrades(series, origine, bnains, evenements, venues_de_bnains, detachements)
                                if origine is not None else [])]),
        ("K19", "suites de séances où l'indice CAC 40 donne tort au fichier, et raison à bnains", True,
         [f"{j[0]}…{j[-1]} ({len(j)} séances, {n} valeurs) marge {m:+.1f}" for j, n, _, _, _, m, ver in arbitrages
          if ver == "le fichier a tort"]),
        ("K19b", "suites de séances où le fichier et bnains se contredisent et que l'indice ne départage pas "
                 "(non bloquant)", False,
         [f"{j[0]}…{j[-1]} ({len(j)} séances) : {ver}" + ("" if m is None else f", marge {m:+.1f}")
          for j, n, _, _, _, m, ver in arbitrages if ver in ("indifférent", "non mesurable")]),
        ("K20", f"lignes de Yahoo qui ne portent pas exactement un ajustement à défaire (à {DEFAIT:.2%} près, des "
                f"deux côtés de sa date)", True,
         [f"{v} (correction du {d}, × {f:.6f}) {x or ''} : {raison}"
          for v, d, f, x, raison in (portes(series, origine, a_defaire, venues_de_bnains, detachements, alignes)
                                     if origine is not None else [])]),
        ("K21", f"opérations déclarées dont le jour n'est pas une séance, ou que la mesure des cours contredit (marche "
                f"d'au moins {NETTETE} fois le bruit de la valeur) — sur {k21_jugees} opérations jugées", True, k21),
        ("K21b", "opérations déclarées que la mesure ne tranche pas, dont la phrase citée n'écrit pas le jour et que "
                 "Jean-Luc n'a pas acceptées (JOURS_ACCEPTES) ; et jours acceptés sans opération", True, k21b),
        ("K21c", "jours d'opération acceptés par décision de Jean-Luc, sans preuve écrite (non bloquant, rappel)", False,
         k21c),
        ("K22", f"opérations déclarées dont la marche, dans le fichier, s'écarte de la règle officielle de plus de "
                f"{MARCHE_EXACTE:.2%}", True, marches_inexactes(series, bnains, evenements, detachements, douteux)),
    ]


MOIS_ECRITS = (("janvier", "january"), ("fevrier", "february"), ("mars", "march"), ("avril", "april"), ("mai", "may"),
               ("juin", "june"), ("juillet", "july"), ("aout", "august"), ("septembre", "september"),
               ("octobre", "october"), ("novembre", "november"), ("decembre", "december"))


def jour_ecrit(citation, jour):
    """Dit si la phrase citée d'un document — le texte entre « » — écrit un jour donné, en lettres ou en chiffres.

    ① RÔLE — Savoir si la date d'une opération déclarée se LIT dans la phrase du document recopiée à
      côté d'elle, pour K21b.
    ② CONTEXTE D'APPEL — `dates_declarees` ; les épreuves.
    ③ ENTRÉE — `citation` : le texte de la colonne `citation` de DETACHEMENTS_OFFICIELS.csv · `jour` :
      le jour déclaré, AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — `jour` est une date valide au format AAAA-MM-JJ.
    ⑤ SORTIE — UNE valeur : vrai si le texte entre « » de la citation porte le jour sous l'une des formes « 4 juillet 2002 »,
      « 04 juillet 2002 », « 1er juin 2009 », « July 4, 2002 », « 4 July 2002 », « 04-07-2002 »,
      « 04/07/2002 » ou « 2002-07-04 » ; faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① ne garder que le texte entre « » · ② le ramener en minuscules, sans accents, sans
      points ni virgules, « 1er » en « 1 », les espaces regroupées ; une période « du J au J2 mois AAAA »
      écrit aussi « J mois AAAA », le jour où elle s'ouvre (ajouté le 10-10-2026 : AXA 2009 « du 10 au 23
      novembre 2009 », Veolia 2007 « du 14 au 27 juin 2007 ») · ③ fabriquer les formes du jour ·
      ④ chercher chacune ; une forme en chiffres ne compte pas collée à un autre chiffre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Quand la mesure ne peut pas trancher le jour d'une opération (K21), le jour ne repose
      plus que sur le document : il doit alors y être ÉCRIT, et non déduit. Mesuré le 09-10-2026 :
      sur les 21 opérations déclarées avec un cours et une parité, trois phrases citées n'écrivent pas
      le jour — Orange 2003, qui écrit la veille (« of record as of the close of trading […] on March 24,
      2003 »), et Carrefour 2011, dont la date n'est écrite que hors des « », toutes deux tranchées par
      la mesure ; AXA 2003, dont le jour est déduit de l'enregistrement du 19-09-2003, et que la mesure
      ne tranche pas.
    ⑨ CE QUI CLOCHE — Relecture indépendante du 09-10-2026 : 19 citations sur 29 portent, HORS des « », un
      commentaire « Cours de la veille : … » qui date la veille — lue en entier, la citation laissait passer une opération
      déclarée la veille ; d'où le seul texte entre « ». · Une phrase citée qui écrit le jour pour une
      autre raison (la fin d'une période, par exemple) passe. Un document qui écrit la veille (« détachés le 6 mars 2006 après la séance »)
      ne passe que si la citation recopie aussi le jour suivant. Une date écrite sans son année
      (« du 10 au 23 novembre 2009 ») ne passe pas, ni « March 25th, 2003 », « 25.03.2003 », « 25/3/2003 » :
      l'opération est alors signalée, jamais acceptée à tort.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir. [sort: non]
      [sort: non]
    """
    t = " ".join(re.findall(r"«([^»]*)»", citation))        # la phrase du document, pas le commentaire autour
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = " " + " ".join(t.replace(".", " ").replace(",", " ").replace("1er ", "1 ").split()) + " "
    # « du 10 au 23 novembre 2009 » écrit aussi le 10 novembre 2009 (AXA ; Veolia, « du 14 au 27 juin 2007 »)
    t += " ".join(f" {j} {m} {a} " for j, m, a in re.findall(r" du (\d{1,2}) au \d{1,2} ([a-z]+) (\d{4}) ", t))
    a, m, j = jour.split("-")
    fr, en = MOIS_ECRITS[int(m) - 1]
    chiffres = [f"{a}-{m}-{j}", f"{j}-{m}-{a}", f"{j}/{m}/{a}"]
    lettres = []
    for d in {str(int(j)), j}:
        lettres += [f" {d} {fr} {a} ", f" {d} {en} {a} ", f" {en} {d} {a} "]
    return any(f in t for f in lettres) or any(re.search(r"(?<!\d)" + re.escape(f) + r"(?!\d)", t) for f in chiffres)


def lire_citations(officiels):
    """Lit la citation de chaque opération déclarée ; rend (valeur, jour) → citation.

    ① RÔLE — Donner à K21b la phrase du document de chaque opération, que `lire_detachements` ne rend pas.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves.
    ③ ENTRÉE — `officiels` : le chemin de donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv.
    ④ CONDITIONS D'ENTRÉE — Le fichier porte les colonnes de son contrat (`DETACHEMENTS_OFFICIELS`).
    ⑤ SORTIE — UNE valeur : le dictionnaire (valeur, jour du détachement) → citation. Lève ValueError
      si l'en-tête n'est pas celui du contrat.
      [rend: 1]
    ⑥ TRAITEMENT — Lire chaque ligne, ranger sa citation sous (valeur, jour).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `lire_detachements` rend les droits dont les marches se calculent ; changer ce qu'elle
      rend toucherait tous ses appels. Une lecture à part, du seul champ qui manque, sous le même contrat.
    ⑨ CE QUI CLOCHE — Deux lignes d'une valeur le même jour garderaient la dernière citation ; elles
      sont refusées plus tôt par `lire_detachements`, que `main` appelle avant.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir. [sort: non]
      [sort: non]
    """
    with open(officiels, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != DETACHEMENTS_OFFICIELS:
            raise ValueError(f"{officiels} : en-tête {lecteur.fieldnames} au lieu de {DETACHEMENTS_OFFICIELS}")
        return {(r["valeur"], r["jour_du_detachement"]): r["citation"] for r in lecteur}


def dates_declarees(bnains, detachements, citations=None, evenements=None):
    """Juge le jour de chaque opération déclarée par un document sur la mesure des cours ; rend contredites, non tranchées, acceptées, et combien jugées.

    ① RÔLE — Vérifier les DÉCLARATIONS de DETACHEMENTS_OFFICIELS.csv, que la réparation applique sans
      les vérifier : un jour faux y donnait un fichier faux accepté.
    ② CONTEXTE D'APPEL — `controler`, pour K21 et K21b ; les épreuves.
    ③ ENTRÉE — `bnains` : l'extrait, barres prouvées fausses ôtées · `detachements` : valeur → {jour :
      droit}, rendu par `lire_detachements`, ou None (aucune table lue : rien n'est jugé) · `citations` :
      rendu par `lire_citations`, ou None (seuls les jours acceptés sans opération, ou en double, sont
      alors jugés) · `evenements` : les divisions de Yahoo qu'on garde (celles que lit `divisions`), ou
      None (les rendements de bnains sont alors pris tels quels).
    ④ CONDITIONS D'ENTRÉE — Les jours sont au format AAAA-MM-JJ (`lire_detachements` le vérifie).
    ⑤ SORTIE — QUATRE valeurs : ① les opérations dont le jour est CONTREDIT — par la mesure, ou parce
      que ce n'est pas une séance · ② celles que la mesure ne peut pas trancher, dont la phrase citée
      n'écrit pas le jour (`jour_ecrit`) et que `JOURS_ACCEPTES` n'accepte pas — et les jours acceptés qui
      ne correspondent à aucune opération déclarée, en double, ou devenus sans emploi · ③ les opérations acceptées par `JOURS_ACCEPTES`,
      avec leur raison · ④ le nombre d'opérations jugées. Chaque opération rendue est un texte qui nomme
      la valeur, le jour et la raison.
      [rend: 4]
    ⑥ TRAITEMENT — Pour chaque opération déclarée avec ses chiffres (droit « document » ou
      « distribution » ; les droits vus chez bnains ont leur propre contrôle, K16) : ① un samedi, un
      dimanche, ou un jour que bnains n'a pas alors qu'il tombe dans sa période : CONTREDIT · ② sa marche
      `marche_permise` · ③ l'écart au marché d'une séance : le rendement de clôture de la valeur chez
      bnains moins la médiane de celui des autres valeurs, chaque cours étant d'abord ramené par les
      divisions de `evenements` (`divisions`) · ④ le bruit propre : l'écart-type de cet
      écart sur les `BRUIT_SEANCES` séances qui précèdent la veille, sans les écarts de plus de `SAUT`
      (une division ou un changement de série chez bnains), s'il en reste au moins `BRUIT_MINIMUM` ·
      ⑤ le reste d'une séance : l'écart au marché une fois la marche rendue, |(1 + écart)(1 + marche) − 1|
      · ⑥ si la marche vaut au moins `NETTETE` fois le bruit et que le jour se mesure : le jour est
      confirmé quand la marche y RAPPROCHE l'écart de zéro (reste plus petit que l'écart) et que son reste
      est plus petit que celui de chacune des `VOISINAGE` séances d'avant et d'après ; sinon il est
      CONTREDIT · ⑦ sinon, la mesure ne tranche pas : si la phrase citée n'écrit pas le jour, l'opération
      est rangée en ③ quand `JOURS_ACCEPTES` l'accepte, en ② sinon ; une opération acceptée reste jugée
      d'abord par la mesure, et refusée si la mesure la contredit · ⑧ un jour de `JOURS_ACCEPTES` est
      rangé en ② s'il est écrit deux fois, s'il ne correspond à aucune opération déclarée, ou si
      l'opération n'en a plus besoin (la mesure la juge ou la phrase citée écrit le jour).
    ⑦ UNITÉ — Marches, bruits, écarts et restes en FRACTIONS (0,01 = 1 %) ; le rapport marche ÷ bruit
      sans unité ; ④ en NOMBRE D'OPÉRATIONS.
    ⑧ POURQUOI — Relecture indépendante du 09-10-2026 : Carrefour déclaré au 06-07-2011 au lieu du 05
      donnait une hausse de +9,70 % le 06, et le contrôle acceptait. La mesure proposée alors donnait
      des fausses alertes sur des jours écrits par des documents officiels. Mesuré par le Chat le
      09-10-2026 (tests/resultats/CAUSE_DES_FAUSSES_ALERTES_DU_CONTROLE_DE_DATE_Ven_09-10-2026_12h26.txt,
      barres fausses ôtées) : celles qui se mesurent ont une marche de 0,1 à 1,3 fois le bruit de la
      valeur, noyée dans les mouvements d'un jour ordinaire ; les cinq opérations à 3,7 fois ou plus
      sont confirmées. Décision de Jean-Luc du 09-10-2026 à 12h28 (« 1 » à « le construire maintenant,
      seuil 3 »). Seconde relecture indépendante du même jour, sur le premier jet : un décalage de deux
      séances échappait (Orange au 21-03-2003) ; le critère « le plus grand gain » s'inversait quand la
      baisse du jour dépasse la marche (Saint-Gobain 2009 confirmée à 0,10 point près) ; un saut de
      bnains gonflait le bruit (Pernod Ricard, 17-10-2006 : 68,33 → 162,50 €, bruit 17,83 % au lieu de
      0,86 %, d'où Pernod 2007 accepté un jour trop tôt) ; un dimanche déclaré passait. D'où le reste sur
      ±3 séances, le bruit sans les sauts et le refus d'un jour qui n'est pas une séance. Le 10-10-2026,
      les actions gratuites de Sagem du 10-07-2000, déclarées le jour où Yahoo déclare aussi une division
      par 3, étaient contredites : le cours brut porte les deux opérations ce jour-là (1 287 → 331 €), et la
      marche seule ne l'expliquait pas. D'où les rendements ramenés par les divisions. Seules les divisions
      de Yahoo le sont : une division vue seulement dans la table de bnains (Société Générale 11-05-2000,
      Pernod Ricard 14-02-2003, Carrefour 11-04-2000 — donnees/sources_bnains/DIVISIONS_BNAINS.csv) ne
      l'est pas, et une opération déclarée le même jour qu'elle serait refusée à tort ; aucun cas
      aujourd'hui (relecture indépendante du 10-10-2026 ; BACKLOG A-555 (d)).
    ⑨ CE QUI CLOCHE — Un jour accepté l'est sur la parole de Jean-Luc, pas sur une preuve : il reste
      affiché à chaque contrôle (K21c). L'exception tient sur (valeur, jour) : une parité ou un cours
      changés pour cette opération restent acceptés. · K21b dépend de l'extrait bnains : sans les séances
      autour d'Orange 2003 ou de Carrefour 2011, la mesure ne les tranche plus et K21b les refuse, leur
      phrase citée n'écrivant pas le jour (seconde relecture du 09-10-2026). · Le seuil de 3 repose sur peu de cas. · Au-delà du 28-02-2017, bnains s'arrête :
      aucune opération récente ne se mesure, son jour repose sur sa phrase citée, et seul un samedi ou
      un dimanche y est refusé. · La GRANDEUR de l'opération n'est pas vérifiée : une valeur distribuée
      ou une parité fausse passe, tant que le jour est le bon (relecture du 09-10-2026 : Carrefour à
      5,10 € au lieu de 3,40 € accepté) — au BACKLOG. · Une opération de petite marche dont la phrase
      citée écrit un jour faux passe.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir. [sort: non]
      [sort: non]
    """
    contredites, non_tranchees, acceptees, jugees = [], [], [], 0
    acceptes = {(v, j): raison for v, j, raison in JOURS_ACCEPTES}
    utilisees = set()
    if detachements is None:
        return contredites, non_tranchees, acceptees, jugees
    seances = sorted({d for s in bnains.values() for d in s})
    rang = {d: i for i, d in enumerate(seances)}
    medianes = {}

    def ecart(valeur, i):
        """Rend l'écart au marché d'une valeur à une séance : son rendement de clôture moins la médiane des autres.

        ① RÔLE — La seule mesure dont K21 se sert, pour le jour, ses voisins et le bruit.
        ② CONTEXTE D'APPEL — `dates_declarees`, la fonction qui l'enferme, pour chaque séance qu'elle juge.
        ③ ENTRÉE — `valeur` : le nom de la valeur · `i` : le rang de la séance dans `seances`.
        ④ CONDITIONS D'ENTRÉE — `seances`, `bnains` et `medianes` de la fonction englobante existent.
        ⑤ SORTIE — UNE valeur : l'écart, en fraction, ou None quand la séance ou la veille manque pour la
          valeur, quand `i` sort du calendrier, ou quand aucune autre valeur ne cote ces deux séances.
          [rend: 1]
        ⑥ TRAITEMENT — ① les rendements de clôture de toutes les valeurs qui ont la séance et la veille,
          calculés une fois par séance et gardés dans `medianes` · ② celui de la valeur moins la médiane
          des autres.
        ⑦ UNITÉ — Une FRACTION (0,01 = 1 %).
        ⑧ POURQUOI — Le marché bouge toutes les valeurs ensemble ; retirer sa médiane laisse ce qui est
          propre à la valeur, dont la marche d'une opération. La médiane plutôt que la moyenne : une autre
          valeur qui détache le même jour ne la déplace presque pas.
        ⑨ CE QUI CLOCHE — La médiane compte toutes les valeurs à poids égal, pas comme l'indice.
        ⑩ EFFET — ÉCRIT dans `medianes`, le cache de la fonction englobante.
        ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir. [sort: non]
          [sort: non]
        """
        if i < 1 or i >= len(seances):
            return None
        d, p = seances[i], seances[i - 1]
        if d not in medianes:
            autres = {}
            for w, s in bnains.items():
                if d in s and p in s and s[p][3] > 0:
                    autres[w] = (s[d][3] / s[p][3]) * (divisions(evenements, w, p) / divisions(evenements, w, d)
                                                       if evenements else 1.0) - 1
            medianes[d] = autres
        autres = medianes[d]
        if valeur not in autres:
            return None
        reste = [x for w, x in autres.items() if w != valeur]
        return autres[valeur] - statistics.median(reste) if reste else None

    for valeur in sorted(detachements):
        for jour, droit in sorted(detachements[valeur].items()):
            if droit[0] not in ("document", "distribution"):
                continue
            jugees += 1
            if datetime.date.fromisoformat(jour).weekday() >= 5 or (
                    seances and seances[0] <= jour <= seances[-1] and jour not in rang):
                contredites.append(f"{valeur} {jour} : ce jour n'est pas une séance")
                continue
            m = marche_permise(bnains.get(valeur, {}), droit)
            i = rang.get(jour)
            e = {k: ecart(valeur, i + k) for k in range(-VOISINAGE, VOISINAGE + 1)} if i is not None else {}
            restes = {k: abs((1 + x) * (1 + m) - 1) for k, x in e.items() if x is not None}
            bruits = [x for x in (ecart(valeur, k) for k in range(i - BRUIT_SEANCES - 1, i - 1))
                      if x is not None and abs(x) <= SAUT] if i is not None else []
            bruit = statistics.pstdev(bruits) if len(bruits) >= BRUIT_MINIMUM else None
            if bruit and m >= NETTETE * bruit and 0 in restes:
                if not (restes[0] < abs(e[0]) and all(restes[0] < r for k, r in restes.items() if k)):
                    meilleur = min(restes, key=restes.get)
                    contredites.append(f"{valeur} {jour} : marche {m:.2%}, bruit {bruit:.2%} (× {m / bruit:.1f}) — "
                                       f"écart du jour {e[0]:+.2%}, reste {restes[0]:.2%} ; la marche s'explique "
                                       f"mieux {meilleur:+d} séance(s) plus loin (reste {restes[meilleur]:.2%})")
                continue
            if citations is not None and not jour_ecrit(citations.get((valeur, jour), ""), jour):
                raison = "hors de bnains" if i is None else ("bruit non mesurable" if not bruit else
                                                             f"marche {m:.2%} = {m / bruit:.1f} × le bruit")
                if (valeur, jour) in acceptes:
                    utilisees.add((valeur, jour))
                    acceptees.append(f"{valeur} {jour} : {raison} — accepté : {acceptes[(valeur, jour)]}")
                else:
                    non_tranchees.append(f"{valeur} {jour} : {raison} — la phrase citée n'écrit pas ce jour")
    declarees = {(v, j) for v, jours in detachements.items() for j, d in jours.items()
                 if d[0] in ("document", "distribution")}
    for v, j in sorted(set(acceptes)):
        if sum(1 for x in JOURS_ACCEPTES if x[:2] == (v, j)) > 1:
            non_tranchees.append(f"{v} {j} : jour accepté deux fois dans JOURS_ACCEPTES — une seule ligne, une seule raison")
        if (v, j) not in declarees:
            non_tranchees.append(f"{v} {j} : jour accepté par décision, mais aucune opération déclarée ce jour-là — "
                                 "l'exception est à retirer ou à corriger")
        elif citations is not None and (v, j) not in utilisees:
            non_tranchees.append(f"{v} {j} : jour accepté par décision, mais la mesure le juge ou la phrase citée "
                                 "l'écrit — l'exception est devenue sans emploi, à retirer")
    return contredites, non_tranchees, acceptees, jugees


def lire_a_defaire(chemin):
    """Lit les ajustements de Yahoo que la réparation retire ; rend la liste (valeur, date, facteur).

    ① RÔLE — Une seule lecture, pour la réparation (`defaire`) et le contrôle (K20) (R-708).
    ② CONTEXTE D'APPEL — `main` ; REPARER_L_HISTORIQUE_LONG, `reparer` ; les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv.
    ④ CONDITIONS D'ENTRÉE — L'en-tête est le contrat `AJUSTEMENTS_DE_YAHOO` ; sinon ValueError.
    ⑤ SORTIE — UNE valeur : la liste, triée, des (valeur, date, facteur) des lignes dont la colonne
      facteur_a_defaire est remplie ; facteur = a ÷ b pour « a/b ».
      [rend: 1]
    ⑥ TRAITEMENT — Lire ; garder les lignes à facteur ; refuser (ValueError) un facteur qui n'est pas « a/b »
      avec a et b finis et positifs, une date qui n'est pas écrite AAAA-MM-JJ, ou deux lignes pour la même valeur et
      la même date.
    ⑦ UNITÉ — Un RAPPORT sans unité : ce par quoi multiplier les cours d'avant la date.
    ⑧ POURQUOI — Depuis le 09-10-2026, une troisième : Accor, 02-07-2010 (Yahoo valorisait l'action Edenred distribuée à 10,96 €), défaite et remplacée par la distribution déclarée à 13,00 € (décision de Jean-Luc à 21h00). — Décision de Jean-Luc du 08-10-2026 à 11h14, sur les deux erreurs de Yahoo trouvées le même
      matin (Crédit Agricole, 22-05-2018 : une division « 27 pour 26 » qui n'a pas eu lieu ; EssilorLuxottica,
      06-05-2024 : un dividende payable en actions corrigé comme une distribution) : « S'il y a des erreurs, il
      faut les corriger ». Le facteur est écrit à la main avec les chiffres du document officiel cité sur la
      même ligne ; etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py vérifie qu'il est celui que Yahoo a appliqué.
    ⑨ CE QUI CLOCHE — Relecture indépendante du 08-10-2026 : « 20180522 » passait `date.fromisoformat` (Python 3.11)
      mais se compare en chaîne après « 2018-12-31 » — 158 lignes de Crédit Agricole faussées sans refus ; « nan/1 »
      passait le test « positif ». Les deux sont refusés depuis.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lecteur = csv.DictReader(open(chemin, encoding="utf-8"))
    if lecteur.fieldnames != AJUSTEMENTS_DE_YAHOO:
        raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames}, attendu {AJUSTEMENTS_DE_YAHOO}")
    sortie = {}
    for r in lecteur:
        if not r["facteur_a_defaire"]:
            continue
        a, _, b = r["facteur_a_defaire"].partition("/")
        if datetime.date.fromisoformat(r["date"]).isoformat() != r["date"]:
            raise ValueError(f"{chemin} : date « {r['date']} » ({r['valeur']}) — attendu AAAA-MM-JJ")
        if not _ or not all(math.isfinite(float(x)) and float(x) > 0 for x in (a, b)):
            raise ValueError(f"{chemin} : facteur « {r['facteur_a_defaire']} » ({r['valeur']} {r['date']})")
        if (r["valeur"], r["date"]) in sortie:
            raise ValueError(f"{chemin} : deux lignes pour {r['valeur']} {r['date']}")
        sortie[(r["valeur"], r["date"])] = float(a) / float(b)
    return sorted((v, d, f) for (v, d), f in sortie.items())


def sans_les_divisions_fausses(evenements, a_defaire):
    """Rend une copie des événements de Yahoo d'où sont ôtées les divisions qu'il déclare à tort.

    ① RÔLE — Que la réparation et le contrôle ne divisent plus les cours bruts par une division qui n'a pas eu lieu.
    ② CONTEXTE D'APPEL — `main` ; REPARER_L_HISTORIQUE_LONG, `reparer`.
    ③ ENTRÉE — `evenements` : le contenu de evenements.json · `a_defaire` : `lire_a_defaire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les événements, sans chaque division [jour, nouveau, ancien] dont la valeur et le jour
      sont ceux d'un ajustement à défaire et dont le rapport nouveau ÷ ancien vaut son facteur à 0,01 % près.
      [rend: 1]
    ⑥ TRAITEMENT — Copier ; filtrer les divisions.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une division déclarée à tort et défaite dans les cours doit l'être aussi dans la liste des
      divisions, pour que le rapport fichier ÷ bnains de Crédit Agricole vaille 1 avant 2017, et non 27 ÷ 26. Le
      filtre ne retire que la division dont le rapport EST le facteur défait : EssilorLuxottica 2024, défait sans
      division déclarée, n'en retire aucune.
    ⑨ CE QUI CLOCHE — Relecture indépendante du 08-10-2026 : sans effet mesurable sur les cours ni sur les verdicts
      du contrôle (toutes leurs mesures sont relatives) : sans lui, le fichier réparé est identique à l'octet, et seule
      change la colonne facteur de 19 lignes de Crédit Agricole au journal (11 « corrigé », 7 « comblé », 1 « remplacé »
      ; la relecture en annonçait 11, recompté le même jour). C'est la liste des divisions qui devient vraie, rien de plus. · Les épreuves qui lisent
      evenements.json directement gardent la division fausse : aucune ne porte sur Crédit Agricole en 2018.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fausses = {(v, d): f for v, d, f in a_defaire}
    copie = {}
    for v, e in evenements.items():
        copie[v] = dict(e)
        if "divisions" in e:
            copie[v]["divisions"] = [x for x in e["divisions"]
                                     if not ((v, x[0]) in fausses and abs(x[1] / x[2] / fausses[(v, x[0])] - 1) <= DEFAIT)]
    return copie


def lire_alignes(chemin):
    """Rend, pour chaque ligne que la réparation a alignée, le facteur écrit au journal ; vide sans journal.

    ① RÔLE — Donner à K20 ce que le geste « aligné » a posé, ligne par ligne.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_yahoo/journal_des_reparations.csv.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (valeur, date) → le produit des facteurs « aligné » de cette ligne.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le journal ; garder les lignes du geste « aligné » ; multiplier leurs facteurs par ligne.
    ⑦ UNITÉ — Des RAPPORTS.
    ⑧ POURQUOI — `aligner` (REPARER_L_HISTORIQUE_LONG, décision de Jean-Luc du 10-10-2026 à 09h39) change des lignes
      de Yahoo que K20 compare au fichier d'origine.
    ⑨ CE QUI CLOCHE — Un journal absent rend un dictionnaire vide : une ligne alignée serait alors signalée par K20,
      jamais acceptée à tort. · Le facteur est écrit en pleine précision depuis le 18-10-2026 (il l'était à 6 décimales, écart sous `DEFAIT`).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    sortie = {}
    if not os.path.exists(chemin):
        return sortie
    for r in csv.DictReader(open(chemin, encoding="utf-8")):
        if r["geste"] == "aligné":
            sortie[(r["valeur"], r["date"])] = sortie.get((r["valeur"], r["date"]), 1.0) * float(r["facteur"])
    return sortie


def portes(series, origine, a_defaire, venues_de_bnains=frozenset(), detachements=None, alignes=None):
    """Rend, pour chaque ajustement à défaire, les lignes du fichier qui ne portent pas exactement la correction.

    ① RÔLE — Le contrôle K20 : le fichier porte-t-il exactement la correction décidée, et seulement elle ?
    ② CONTEXTE D'APPEL — `controler` ; les épreuves.
    ③ ENTRÉE — `series` : le fichier contrôlé · `origine` : le fichier Yahoo avant réparation · `a_defaire` :
      `lire_a_defaire` · `venues_de_bnains` : les (valeur, date) refaites depuis bnains · `detachements` :
      `lire_detachements`, ou None — une opération déclarée par un document le JOUR MÊME d'une correction
      défaite la remplace (Accor, 02-07-2010) · `alignes` : (valeur, date) → le facteur que le geste « aligné » de
      la réparation a posé sur cette ligne, lu au journal (`lire_alignes`), ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des (valeur, date de la correction, facteur, séance, raison), une par ligne
      fautive, plus une (…, None, « aucune ligne de Yahoo d'avant la date ») quand rien ne se compare avant la date.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ajustement et chaque ligne de la valeur venue de Yahoo, présente dans le fichier
      d'origine : avant la date, chacun des quatre prix ÷ celui d'origine doit valoir le facteur et le volume ÷ celui
      d'origine son inverse, à `DEFAIT` près ; à partir de la date, les cinq doivent valoir 1. Quand
      `detachements` déclare, pour la valeur et le jour de la correction, une opération chiffrée (droit
      « document » ou « distribution »), le facteur attendu avant la date est celui de la correction
      ÷ (1 + la marche permise de l'opération) : la réparation défait l'ajustement de Yahoo, puis pose
      celui de l'opération (`ajuster`), qui ne voit plus de marche ce jour-là. Une ligne qu'`aligner` a ramenée à la
      règle officielle (décision de Jean-Luc du 10-10-2026, 09h39) doit porter, en plus, le facteur que le journal
      de la réparation écrit pour elle.
    ⑦ UNITÉ — Des RAPPORTS.
    ⑧ POURQUOI — Relecture indépendante du 08-10-2026 : la première version comparait des MÉDIANES, et acceptait
      une correction posée du mauvais côté de la date (EssilorLuxottica, du 06-05 au 30-09-2024 : code 0), faite sur
      la moitié des lignes, ou sur la seule clôture. Ligne à ligne, aucune ne passe. Les lignes refaites depuis
      bnains ne se comparent pas au fichier d'origine : elles en diffèrent par construction.
    ⑨ CE QUI CLOCHE — Le contrôle vérifie que la correction décidée est faite, pas qu'elle est juste : c'est
      l'outil etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py qui confronte le facteur aux cours bruts et au
      témoin officiel. · Une valeur à défaire qui porterait aussi un autre geste de la réparation sur des lignes de
      Yahoo (`ajuster` pour une opération d'un AUTRE jour, `recaler`) verrait ces lignes signalées : aucune ne
      l'est sur le fichier du 09-10-2026. Le 10-10-2026, l'alignement du droit de Crédit Agricole de 2007 a fait
      signaler 1 288 lignes d'avant 2007 ; un premier remède (ne juger que depuis la dernière opération déclarée)
      laissait passer un fichier faux de 0,5 % sur les lignes d'avant 2008 (relecture indépendante du même jour) :
      remplacé par le facteur du journal, ligne par ligne. Ce facteur, K20 le lit sans le vérifier ; K15 juge la
      marche au jour du droit, à 1 % près. · Le cas du même jour (Accor 2010 : facteur de Yahoo défait, distribution
      d'Edenred déclarée à 13,00 €, décision de Jean-Luc du 09-10-2026 à 21h00) est jugé avec le produit des deux
      facteurs ; il suppose que `ajuster` pose bien l'opération — K15 le vérifie au jour même. · Si Yahoo corrigeait un jour son erreur dans un nouveau fichier
      déposé, défaire créerait l'erreur, et K20, qui compare à ce même fichier, l'accepterait (→ BACKLOG).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sortie = []
    for v, d, f in a_defaire:
        droit = (detachements or {}).get(v, {}).get(d)
        if droit and droit[0] in ("document", "distribution"):
            f = f / (1 + marche_permise({}, droit))
        s, o = series.get(v, {}), (origine or {}).get(v, {})
        lignes = [x for x in sorted(s) if x in o and (v, x) not in venues_de_bnains and min(o[x]) > 0]
        if not [x for x in lignes if x < d]:
            sortie.append((v, d, f, None, "aucune ligne de Yahoo d'avant la date"))
        for x in lignes:
            q = (alignes or {}).get((v, x), 1.0)      # le geste « aligné » de la réparation, écrit au journal
            g = (f if x < d else 1) * q
            attendu = (g, g, g, g, 1 / g)
            faux = [nom for nom, a, b, e in zip(("ouverture", "plus haut", "plus bas", "clôture", "volume"), s[x], o[x],
                                                attendu) if abs(a / b / e - 1) > DEFAIT]
            if faux:
                sortie.append((v, d, f, x, f"{', '.join(faux)} : rapport au fichier d'origine "
                                           f"{s[x][3] / o[x][3]:.6f} en clôture, attendu {attendu[3]:.6f}"))
    return sortie

def marche_permise(barres, droit):
    """Rend la marche que le détachement d'un droit permet au rapport entre une série ajustée et les cours bruts.

    ① RÔLE — Une seule définition de la marche permise, pour le contrôle K15, le recalage et la
      reconstruction (REPARER_L_HISTORIQUE_LONG).
    ② CONTEXTE D'APPEL — `controler` ; REPARER_L_HISTORIQUE_LONG, `recaler` et `reconstruire`.
    ③ ENTRÉE — `barres` : la série bnains d'UNE valeur, par date · `droit` : un des deux droits
      que rend la lecture des détachements — ("bnains", clôture du droit à son premier jour de cotation
      chez bnains, ce premier jour) ou ("document", cours de la veille, prix de souscription,
      actions anciennes pour une nouvelle) ou ("distribution", cours de la veille, valeur
      distribuée par action).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la marche, un nombre (0,0247 pour +2,47 %). 0 quand bnains n'a pas la
      barre de l'action le jour du premier cours du droit.
      [rend: 1]
    ⑥ TRAITEMENT — « bnains » : clôture du droit ÷ clôture de l'action le même jour. « document » :
      cours de la veille ÷ cours théorique ex-droit − 1, avec cours théorique ex-droit = (n × cours de
      la veille + prix de souscription) ÷ (n + 1). « distribution » : valeur distribuée ÷ (cours de
      la veille − valeur distribuée).
    ⑦ UNITÉ — Un RAPPORT sans unité.
    ⑧ POURQUOI — Le droit vaut d sur une action ex-droit à a : la série ajustée garde la valeur du
      droit, la série brute la perd, et leur rapport change de d / a. Pour un droit coté chez bnains,
      les deux clôtures sont prises le MÊME jour, le premier où bnains cote le droit. AXA 2009 :
      0,413 / 16,725 = +2,47 %, pour une marche mesurée de +2,34 % chez Yahoo le 10-11-2009. Pour un
      droit absent de bnains, la valeur théorique se calcule avec les chiffres du document : AXA, juin
      2006, une action nouvelle pour 9 à 19,80 € quand l'action valait 24,47 € (rapport annuel 2006) :
      (9 × 24,47 + 19,80) ÷ 10 = 24,003 ; 24,47 ÷ 24,003 − 1 = +1,95 %, exactement l'ajustement que le
      rapport annuel applique à ses propres cours mensuels d'avant juin 2006 (1,0195, mesuré le
      07-10-2026). Des actions GRATUITES sont un droit à prix nul : prix de souscription 0, n
      anciennes pour une nouvelle ; Pernod Ricard, 16-01-2007, une pour cinq : 5 × P ÷ 6 ; marche
      1 ÷ 5 = +20 %. Une DISTRIBUTION d'actions d'une autre société (A-555 ⑥, 09-10-2026) retire du
      cours la valeur distribuée v : l'action ex vaut cours − v, et le rapport change de
      v ÷ (cours − v) ; Kering, 20-06-2013, une action Fnac à 20,03 € pour 8 : v = 2,50375,
      cours de la veille 162,40, marche +1,566 %.
    ⑨ CE QUI CLOCHE — Le droit et l'action d'un jour après le détachement ne valent pas exactement
      ceux du jour même : l'écart est absorbé par `ECART`. · Une marche nulle, quand bnains n'a pas
      la barre, fait refuser une marche réelle — jamais accepter une fausse.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if droit[0] == "document":
        _, cours, prix, n = droit
        return cours / ((n * cours + prix) / (n + 1)) - 1
    if droit[0] == "distribution":
        _, cours, distribue = droit
        return distribue / (cours - distribue)
    _, cloture, premiere = droit
    b = barres.get(premiere)
    return cloture / b[3] if b and b[3] > 0 else 0.0


def lire_detachements(chemin, officiels):
    """Joint les droits vus chez bnains à leurs jours de détachement officiels ; rend les détachements et les manques.

    ① RÔLE — Donner à K15, au recalage et à la reconstruction les seuls jours où une série ajustée
      peut changer de rapport aux cours bruts, et de quoi calculer de combien.
    ② CONTEXTE D'APPEL — `main`, une fois ; REPARER_L_HISTORIQUE_LONG ; les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_bnains/DROITS_BNAINS.csv · `officiels` :
      donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv.
    ④ CONDITIONS D'ENTRÉE — Les deux fichiers portent les colonnes de leurs contrats.
    ⑤ SORTIE — DEUX valeurs : ① un dictionnaire valeur → {jour officiel du détachement : droit}, où
      droit est ("bnains", clôture du droit à son premier jour chez bnains, ce premier jour) ou
      ("document", cours de la veille, prix de souscription, actions anciennes pour une nouvelle) ou
      ("distribution", cours de la veille, valeur distribuée par action) quand la colonne
      `valeur_distribuee` est remplie · ② la liste des manques, des couples (valeur, phrase) : un droit vu chez bnains sans jour
      officiel, ou dont le jour officiel n'est pas dans les `ECART_DE_COTATION` jours qui précèdent
      sa première cotation chez bnains (ou ce jour même) ; une ligne officielle sans droit chez
      bnains et sans les chiffres du document. Lève ValueError si un en-tête n'est pas celui du
      contrat, si un chiffre du document est illisible ou impossible, si deux lignes portent la même
      valeur et le même libellé, ou deux opérations la même valeur le même jour.
      [rend: 2]
    ⑥ TRAITEMENT — ① vérifier les deux en-têtes · ② lire les lignes officielles sous (valeur,
      libellé du droit) · ③ pour chaque droit vu chez bnains : son jour officiel, s'il existe et s'il
      est possible, reçoit le droit « document » si la ligne officielle porte ses trois chiffres (la règle
      officielle, décision de Jean-Luc du 10-10-2026 à 09h39, `document`), le droit « bnains » sinon ; sinon
      un manque · ④ chaque ligne officielle qu'aucun droit de bnains n'a prise reçoit le droit « document »
      si ses trois chiffres sont là, sinon un manque.
    ⑦ UNITÉ — Des DATES et des EUROS.
    ⑧ POURQUOI — Lu le 07-10-2026 dans les communiqués des émetteurs : le droit est détaché le jour
      où la souscription ouvre (« 8 octobre 2009 Ouverture de la période de souscription -
      Détachement et début des négociations des droits préférentiels de souscription », Société
      Générale ; même phrase chez Michelin le 30-09-2010), et bnains ne le montre souvent qu'une
      séance plus tard : AXA souscription du 10-11-2009, bnains le 11 ; Danone le 01-06-2009,
      bnains le 02. Prendre le premier jour de bnains a fait croire, du 04 au 06-10-2026, que Yahoo
      ajustait un jour trop tôt, et a fait « recaler » à tort Danone, Michelin et Pernod Ricard. Le
      jour officiel est donc une DONNÉE, prouvée ligne par ligne par une citation et son adresse.
      Un droit sans jour officiel est un manque visible (K16), jamais un jour deviné. Certains droits
      manquent aux archives bnains (AXA, juin 2006, trouvé le 07-10-2026 dans le rapport annuel 2006
      d'AXA ; douze autres le même jour, de Veolia 2002 à Veolia 2021, dans le BALO, les déclarations
      à la SEC et les notes d'opération) : leur valeur se calcule alors avec les chiffres du document
      (`marche_permise`). Les bons de souscription gratuits de France Télécom (2003) et de
      Saint-Gobain (2009) y sont rangés aussi : attribués à tous les actionnaires, ils pèsent sur le
      cours comme un droit.
    ⑨ CE QUI CLOCHE — Le jour de France Télécom en mars 2003 est DÉDUIT (la séance qui suit la date
      d'enregistrement du 24-03-2003). Pour Crédit Agricole 2003, Société Générale 2006 et 2008 et
      Schneider Electric 2007, le jour est celui de l'ouverture de la souscription : le mot
      « détachement » n'est pas écrit dans les textes trouvés (voir leur citation).
    ⑩ EFFET — Lit les deux fichiers. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    officielles = {}
    with open(officiels, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != DETACHEMENTS_OFFICIELS:
            raise ValueError(f"{officiels} : en-tête {lecteur.fieldnames} au lieu de {DETACHEMENTS_OFFICIELS}")
        for r in lecteur:
            j = r["jour_du_detachement"]
            try:                                       # relecture du 09-10-2026 : « 20110705 » passait, fichier faux
                valide = not j or datetime.date.fromisoformat(j).isoformat() == j
            except ValueError:
                valide = False
            if not valide:
                raise ValueError(f"{officiels} : {r['valeur']} « {r['libelle_du_droit']} » : jour « {j} » illisible, "
                                 "il faut AAAA-MM-JJ")
            if (r["valeur"], r["libelle_du_droit"]) in officielles:      # relecture du 09-10-2026 : un doublon écrasait
                raise ValueError(f"{officiels} : deux lignes pour {r['valeur']} « {r['libelle_du_droit']} »")
            officielles[(r["valeur"], r["libelle_du_droit"])] = r
    detachements, manques, prises = {}, [], set()

    def poser(valeur, jour, droit):
        """Range un détachement à son jour, et refuse un second détachement de la même valeur le même jour.

        ① RÔLE — Écrire dans `detachements` le droit d'une valeur à son jour de détachement, une seule fois.
        ② CONTEXTE D'APPEL — `lire_detachements`, la fonction qui l'enferme, pour chaque droit retenu
          (droit vu chez bnains, ou opération déclarée par un document ou par une valeur distribuée).
        ③ ENTRÉE — `valeur` : le nom de la valeur · `jour` : le jour du détachement, AAAA-MM-JJ ·
          `droit` : le tuple du droit, tel que `marche_permise` le lit.
        ④ CONDITIONS D'ENTRÉE — Le dictionnaire `detachements` de la fonction englobante existe.
        ⑤ SORTIE — Ne rend rien : range le droit, ou lève ValueError quand la valeur a déjà un
          détachement ce jour-là.
          [rend: rien]
        ⑥ TRAITEMENT — ① chercher le jour parmi les détachements déjà rangés de la valeur · ② s'il y est,
          lever ValueError en nommant le fichier, la valeur et le jour · ③ sinon, ranger le droit.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture indépendante du 09-10-2026 : deux opérations d'une valeur le même jour
          s'écrasaient sans rien dire, et la seconde effaçait la première. Une seule ligne par jour.
        ⑨ CE QUI CLOCHE — Deux opérations réelles le même jour (Total, 18-05-2006 : division par quatre et
          distribution d'Arkema) ne passent pas ici : la division vient des événements de Yahoo, pas de ce
          fichier, et ne se pose donc pas par cette fonction.
        ⑩ EFFET — ÉCRIT dans le dictionnaire `detachements` de la fonction englobante.
        ⑪ TERMINAISON — Rend la main, ou lève. Aucun de mes appels ne peut ne pas revenir. [sort: non]
          [sort: non]
        """
        # relecture du 09-10-2026 : deux opérations d'une valeur le même jour s'écrasaient sans rien dire
        if jour in detachements.get(valeur, {}):
            raise ValueError(f"{officiels} : deux opérations pour {valeur} le {jour} — une seule ligne par jour")
        detachements.setdefault(valeur, {})[jour] = droit

    def document(r):
        """Rend le droit « document » d'une ligne officielle, calculé par la règle officielle, ou lève ValueError.

        ① RÔLE — Lire les chiffres d'un document (cours de la veille, prix de souscription, actions anciennes pour
          une nouvelle, dividende non attaché) et les vérifier, en UN seul endroit (R-708).
        ② CONTEXTE D'APPEL — `lire_detachements`, la fonction qui l'enferme : pour un droit vu chez bnains dont la
          ligne officielle porte ses chiffres, et pour une ligne officielle sans droit chez bnains.
        ③ ENTRÉE — `r` : une ligne de DETACHEMENTS_OFFICIELS.csv, dont les trois chiffres du droit sont remplis.
        ④ CONDITIONS D'ENTRÉE — `officiels` (le chemin) existe dans la fonction englobante.
        ⑤ SORTIE — QUATRE valeurs, en un tuple : ("document", cours de la veille, prix de souscription + dividende
          non attaché, actions anciennes pour une nouvelle).
          [rend: 4]
        ⑥ TRAITEMENT — ① lire les nombres · ② ajouter le dividende non attaché au prix : le droit vaut
          (cours − prix − dividende) ÷ (n + 1), ce qui est la formule de `marche_permise` avec ce prix · ③ refuser
          un cours nul, moins d'une action ancienne pour une nouvelle, un prix négatif ou au moins égal au cours.
        ⑦ UNITÉ — Des EUROS par action ; n sans unité.
        ⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 à 09h39 (« 1 » à « Règle officielle partout, fichier corrigé
          sur les 4 écarts ») : la valeur d'un droit se calcule par la règle officielle — prix de référence technique
          ÷ clôture de la veille. Le cours du droit chez bnains à son premier jour s'en écartait jusqu'à 0,64 point
          (Danone 2009 : +6,45 % pour +5,976 % ; Société Générale 2008 : +6,19 % pour +6,83 %). Le dividende :
          Société Générale, 21-02-2008, les actions nouvelles ne touchent pas le dividende de 0,90 € ; le document
          donne 5,86 € = (77,72 − 47,50 − 0,90) ÷ 5 ; de même Vinci 2006 (1,30 €), BNP Paribas 2006 (2,60 €) et
          Schneider Electric 2007 (3 €, que son document compte lui-même), trouvés par la relecture indépendante.
        ⑨ CE QUI CLOCHE — Le dividende non attaché n'est vérifié par rien : il se lit dans le document.
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main, ou lève. Aucun de mes appels ne peut ne pas revenir.
          [sort: non]
        """
        chiffres = (r["cours_veille"], r["prix_souscription"], r["anciennes_pour_une_nouvelle"])
        try:
            droit = ("document", float(chiffres[0]), float(chiffres[1]) + float(r["dividende_non_attache"] or 0),
                     float(chiffres[2]))
        except ValueError:
            raise ValueError(f"{officiels} : chiffres illisibles pour {r['valeur']} « {r['libelle_du_droit']} » : {chiffres}")
        if not (droit[1] > 0 and droit[3] > 0 and 0 <= droit[2] < droit[1]):     # relecture du 09-10-2026
            raise ValueError(f"{officiels} : {r['valeur']} « {r['libelle_du_droit']} » : il faut un cours de la veille "
                             "positif, au moins une action ancienne pour une nouvelle et un prix de souscription "
                             "de zéro (actions gratuites) au cours de la veille exclu")
        return droit
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != DROITS_BNAINS:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {DROITS_BNAINS}")
        for r in lecteur:
            cle, premiere = (r["valeur"], r["libelle"]), r["premiere_seance"]
            jour = officielles[cle]["jour_du_detachement"] if cle in officielles else None
            prises.add(cle)
            ecart = (datetime.date.fromisoformat(premiere) - datetime.date.fromisoformat(jour)).days if jour else None
            if ecart is None or not 0 <= ecart <= ECART_DE_COTATION:
                manques.append((r["valeur"], f"{r['valeur']} « {r['libelle']} », coté chez bnains dès le {premiere} : "
                                + (f"jour officiel {jour} impossible" if jour else "aucun jour officiel")))
                continue
            o = officielles[cle]
            if all((o["cours_veille"], o["prix_souscription"], o["anciennes_pour_une_nouvelle"])):
                # la règle officielle, quand le document donne ses chiffres (décision de Jean-Luc du 10-10-2026, 09h39)
                poser(r["valeur"], jour, document(o))
                continue
            poser(r["valeur"], jour, ("bnains", float(r["cloture_premiere_seance"]), premiere))
    for cle, r in sorted(officielles.items()):
        if cle in prises:
            continue
        if r["valeur_distribuee"]:
            # une distribution d'actions d'une autre société (A-555 ⑥) : la valeur distribuée et le
            # cours de la veille, et RIEN dans les deux colonnes du droit — un mélange serait ambigu
            if r["prix_souscription"] or r["anciennes_pour_une_nouvelle"] or not r["cours_veille"]:
                raise ValueError(f"{officiels} : {r['valeur']} « {r['libelle_du_droit']} » : une distribution porte "
                                 "son cours de la veille et sa valeur distribuée, et rien d'autre")
            if r["dividende_non_attache"]:
                raise ValueError(f"{officiels} : {r['valeur']} « {r['libelle_du_droit']} » : un dividende non attaché "
                                 "ne se déclare que pour un droit de souscription")
            try:
                droit = ("distribution", float(r["cours_veille"]), float(r["valeur_distribuee"]))
            except ValueError:
                raise ValueError(f"{officiels} : chiffres illisibles pour {r['valeur']} « {r['libelle_du_droit']} »")
            if not 0 < droit[2] < droit[1]:
                raise ValueError(f"{officiels} : {r['valeur']} « {r['libelle_du_droit']} » : la valeur distribuée doit "
                                 "être positive et inférieure au cours de la veille")
            poser(r["valeur"], r["jour_du_detachement"], droit)
            continue
        chiffres = (r["cours_veille"], r["prix_souscription"], r["anciennes_pour_une_nouvelle"])
        if not all(chiffres):
            manques.append((r["valeur"], f"{r['valeur']} « {r['libelle_du_droit']} », jour officiel {r['jour_du_detachement']} : "
                            "ni droit chez bnains, ni chiffres du document"))
            continue
        poser(r["valeur"], r["jour_du_detachement"], document(r))
    return detachements, manques


def lire_journal(chemin):
    """Rend le journal des réparations, rangé par ligne de cours, dans l'ordre où les gestes ont été posés.

    ① RÔLE — Donner à K23 chaque geste posé sur chaque ligne de cours.
    ② CONTEXTE D'APPEL — `main`, pour K23 ; les épreuves.
    ③ ENTRÉE — `chemin` : donnees/sources_yahoo/journal_des_reparations.csv.
    ④ CONDITIONS D'ENTRÉE — En-tête exactement JOURNAL_DES_REPARATIONS (programmes/CONTRATS_DES_FICHIERS.py), sinon
      ValueError. Le fichier existe, sinon OSError : sans journal, aucune ligne réparée ne se remonte.
    ⑤ SORTIE — UNE valeur : (valeur, date) → la liste des lignes du journal (dictionnaires), dans l'ordre du fichier.
      [rend: 1]
    ⑥ TRAITEMENT — Lire ; vérifier l'en-tête ; ranger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'ordre des gestes est celui où la réparation les a posés : la chaîne se refait dans cet ordre.
    ⑨ CE QUI CLOCHE — L'ordre n'est garanti que par la façon dont la réparation écrit le journal, ligne après ligne.
      · Un nombre infini ou indéfini (« inf », « nan ») dans une colonne de nombres lève ValueError : il passait le
      rejeu (superviseur n° 2 du 18-10-2026, D4 : « inf ≤ inf » est vrai), comme il passait `lire_cours` le 04-10-2026.
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    sortie = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != JOURNAL_DES_REPARATIONS:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {JOURNAL_DES_REPARATIONS}")
        for r in lecteur:
            for c in ("close_avant", "close_apres", "facteur", "facteur_volume"):
                if r[c] != "" and not math.isfinite(float(r[c])):
                    raise ValueError(f"{chemin} : {r['valeur']} {r['date']} « {r['geste']} », {c} = {r[c]} : nombre "
                                     f"infini ou indéfini")
            sortie.setdefault((r["valeur"], r["date"]), []).append(r)
    return sortie


def appliquer(b, fp, fv):
    """Rend une barre dont les quatre prix sont multipliés par un facteur et le volume par un autre.

    ① RÔLE — Le seul calcul d'un geste parti de la ligne, pour la réparation qui le pose ET pour K23 qui le rejoue.
    ② CONTEXTE D'APPEL — `defaire`, `ajuster`, `aligner` de programmes/REPARER_L_HISTORIQUE_LONG.py ;
      `lignes_non_rejouees`.
    ③ ENTRÉE — `b` : (open, high, low, close, volume) · `fp` : le facteur des prix · `fv` : le facteur du volume.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (open × fp, high × fp, low × fp, close × fp, volume × fv).
      [rend: 1]
    ⑥ TRAITEMENT — ⑤, sans arrondi.
    ⑦ UNITÉ — Des euros et des nombres de titres ; facteurs sans unité.
    ⑧ POURQUOI — Décision de Jean-Luc du 18-10-2026 à 20h41 (« 1 » à « Supprimer la tolérance : le contrôle exige
      l'égalité exacte ») : la réparation et le contrôle font le même calcul, dans cette fonction, et K23 compare à
      l'égalité exacte. Trois tolérances écrites à la main en un jour ont chacune laissé passer une faute (Hermès
      + 0,01 €, Michelin + 0,0001 €, un facteur infini — superviseur n° 2, R-759). Deux implémentations d'une même
      chose divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — Avant le 18-10-2026, la réparation divisait (prix ÷ (1 + m), volume ÷ f) quand le journal écrit
      l'inverse du facteur : le passage à cette fonction a changé 16 961 lignes du fichier réparé au 16e chiffre
      (4,4e-16 au plus, en relatif — mesuré par le superviseur n° 2).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return tuple(x * fp for x in b[:4]) + (b[4] * fv,)


def arrondir(b, fp, fv):
    """Rend une barre de Paris ramenée par deux facteurs, prix arrondis à `DECIMALES` décimales, volume à l'unité.

    ① RÔLE — Le seul calcul d'un geste parti de Paris, pour la réparation qui le pose ET pour K23 qui le rejoue.
    ② CONTEXTE D'APPEL — `barre` de programmes/REPARER_L_HISTORIQUE_LONG.py ; `lignes_non_rejouees`.
    ③ ENTRÉE — `b` : la barre brute de bnains (open, high, low, close, volume) · `fp` · `fv` : les facteurs.
    ④ CONDITIONS D'ENTRÉE — `fv` fini : un facteur infini lèverait OverflowError (`lire_journal` les refuse avant).
    ⑤ SORTIE — UNE valeur : (round(open × fp, DECIMALES), … les quatre prix …, float(round(volume × fv))).
      [rend: 1]
    ⑥ TRAITEMENT — ⑤.
    ⑦ UNITÉ — Des euros et des nombres de titres.
    ⑧ POURQUOI — Comme `appliquer`. La précision écrite (4 décimales, volume entier) est déclarée ICI et nulle part
      ailleurs (relecture du 18-10-2026 : elle était réglée à deux endroits, et un volume de 0,4 titre passait).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return tuple(round(x * fp, DECIMALES) for x in b[:4]) + (float(round(b[4] * fv)),)


def lire_les_sources(chemin):
    """Rend, pour chaque ligne d'un fichier de cours, le texte exact de sa colonne `source`.

    ① RÔLE — Donner à K23 la colonne `source` telle qu'écrite, sans l'interpréter.
    ② CONTEXTE D'APPEL — `main`, pour K23 ; les épreuves.
    ③ ENTRÉE — `chemin` : le fichier contrôlé, qui porte la colonne `source`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (OSError sinon).
    ⑤ SORTIE — UNE valeur : (valeur, date) → le texte de la colonne `source`, vide si la cellule l'est.
      [rend: 1]
    ⑥ TRAITEMENT — Lire ; ranger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `lire_cours` ne retient que les lignes dont la source vaut « bnains » : toute autre valeur s'y lit
      « yahoo ». Relecture du 18-10-2026 : « Yahoo », vide, « bnain », « paris » passaient K23. Le rejeu compare donc
      le texte exact à la provenance qu'il refait.
    ⑨ CE QUI CLOCHE — Une ligne en double garde la dernière source lue ; `lire_cours` signale le doublon (K1).
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    with open(chemin, encoding="utf-8", newline="") as f:
        return {(r["valeur"], r["date"]): r.get("source") or "" for r in csv.DictReader(f)}


def lignes_non_rejouees(series, sources, origine, paris, journal):
    """Rend les lignes du fichier réparé que le journal des réparations ne refait pas, à l'égalité exacte, depuis leur source.

    ① RÔLE — K23, le rejeu : chaque ligne du fichier réparé doit se refaire, colonne par colonne et au chiffre près, en
      rejouant dans l'ordre les gestes que le journal écrit pour elle, depuis la ligne de Yahoo d'origine ou la barre
      de Paris ; et chaque ligne d'origine absente du fichier doit avoir un geste qui la retire.
    ② CONTEXTE D'APPEL — `main`, pour K23, quand le fichier contrôlé porte la colonne `source` ; les épreuves.
    ③ ENTRÉE — `series` : le fichier contrôlé · `sources` : `lire_les_sources` du même fichier · `origine` : le
      fichier Yahoo avant réparation · `paris` : les cours de Paris (bnains) SANS les barres prouvées fausses
      (`lire_paris`, le même Paris que la réparation) · `journal` : `lire_journal`.
    ④ CONDITIONS D'ENTRÉE — Le journal a les colonnes de JOURNAL_DES_REPARATIONS et des nombres finis (`lire_journal`
      l'a vérifié) ; `origine` est lu sans défaut (`main` arrête sinon).
    ⑤ SORTIE — UNE valeur : la liste triée des cas, un texte par ligne qui ne se refait pas ; vide si tout se refait.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque (valeur, date) du fichier, du journal ou de l'origine : l'état part de la ligne Yahoo
      d'origine (ou de rien). Pour chaque geste, dans l'ordre : ① le geste est dans GESTES_DU_JOURNAL et son départ
      est celui que le contrat lui donne · ② il écrit sa clôture après et ses deux facteurs si et seulement si son
      départ n'est pas vide (un facteur non appliqué va dans la raison) ·
      ③ `close_avant` est vide si et seulement si la ligne n'existe pas à ce moment · ④ `close_avant` égale la clôture
      de l'état · ⑤ un geste sans clôture après retire la ligne · ⑥ sinon il part de l'état (« ligne », `appliquer`) ou
      de la barre de Paris du jour (« paris », `arrondir`, la barre doit exister), et sa clôture égale `close_apres`.
      À la fin : la ligne du fichier existe si et seulement si l'état existe, égale l'état sur les cinq colonnes, et sa
      colonne `source` vaut SOURCE_PARIS si un geste parti de Paris a écrit la ligne depuis son dernier retrait (depuis
      l'origine s'il n'y en a pas), SOURCE_YAHOO sinon. Toutes les comparaisons sont des égalités exactes.
    ⑦ UNITÉ — Des euros et des nombres de titres ; facteurs sans unité.
    ⑧ POURQUOI — Demande de Jean-Luc du 13-10-2026 à 09h34 (« Tu ne vas pas oublier de le faire pour notre historique
      des 20 ans ») et sa décision du même jour (« Les deux, dans l'ordre ») : chaque cours de l'historique long doit
      se remonter et se recalculer jusqu'à sa source (A-578). Cette fonction remplace, le 18-10-2026, les deux
      fonctions `etapes_non_recalculables` et `lignes_non_remontees`, qui devinaient le départ et le facteur de volume
      faute de les lire : elles refusaient 1 010 gestes et 611 lignes. L'égalité exacte : décision de Jean-Luc du
      18-10-2026 à 20h41 (voir `appliquer`). Ce que les relectures du même jour ont fait ajouter : l'origine dans la
      boucle (une ligne Yahoo supprimée du fichier sans geste passait — Hermès 14-02-2025) ; le texte exact de la
      source (« Yahoo » passait) ; le vocabulaire des gestes (un geste inventé passait).
    ⑨ CE QUI CLOCHE — Le rejeu prouve que le journal EXPLIQUE le fichier, pas que ses facteurs sont JUSTES : un facteur
      mesuré sur des séances voisines ne se recalcule pas depuis le journal ; la justesse relève de K1 à K22, et de
      l'épreuve qui relance la réparation et retrouve le fichier et le journal à l'octet. · Deux gestes de même départ
      se confondent : « comblé » renommé « corrigé », ou « écarté » renommé « retiré », passe ; un « gardé » (facteurs 1
      et 1) supprimé ou doublé passe ; un geste neutre inventé (« non comblé », ou « retiré » sur une ligne qui n'existe
      nulle part) passe — sans effet sur aucun nombre (relecture n° 2 du 18-10-2026 ; → BACKLOG, A-597). · Paris est
      donné APRÈS le retrait des barres prouvées fausses (`lire_paris`) : une fenêtre déclarée fausse après la
      réparation fera refuser ses lignes avec « Paris, qui n'a pas de barre ce jour » — refus juste, message trompeur.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : chaque ligne a un nombre fini de gestes. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    cas = []
    for v, d in sorted({(v, d) for v, s in series.items() for d in s} | set(journal)
                       | {(v, d) for v, s in origine.items() for d in s}):
        etat = origine.get(v, {}).get(d)
        venue, motif = SOURCE_YAHOO if etat is not None else None, None
        gestes = journal.get((v, d), [])
        for g in gestes:
            if g["geste"] not in GESTES_DU_JOURNAL:
                motif = f"« {g['geste']} » : geste inconnu du contrat (GESTES_DU_JOURNAL)"
                break
            if g["depart"] != GESTES_DU_JOURNAL.get(g["geste"]):
                motif = (f"« {g['geste']} » doit partir de « {GESTES_DU_JOURNAL.get(g['geste'])} », le journal écrit "
                         f"« {g['depart']} »")
                break
            ecrits = [c for c in ("close_apres", "facteur", "facteur_volume") if g[c] != ""]
            if g["depart"] == "" and ecrits:
                motif = f"« {g['geste']} » retire la ligne mais écrit {', '.join(ecrits)}"
                break
            if g["depart"] != "" and len(ecrits) < 3:
                manque = [c for c in ("close_apres", "facteur", "facteur_volume") if c not in ecrits]
                motif = f"« {g['geste']} » part de « {g['depart']} » mais n'écrit pas {', '.join(manque)}"
                break
            if (g["close_avant"] == "") != (etat is None):
                motif = (f"« {g['geste']} » : clôture avant {g['close_avant'] or 'vide'}, alors que la ligne "
                         f"{'n’existe pas' if etat is None else 'existe'} à ce moment")
                break
            if etat is not None and etat[3] != float(g["close_avant"]):
                motif = f"« {g['geste']} » : clôture avant {g['close_avant']}, la ligne rejouée vaut {etat[3]}"
                break
            if g["depart"] == "":
                etat, venue = None, None
                continue
            base = paris.get(v, {}).get(d) if g["depart"] == "paris" else etat
            if base is None:
                motif = (f"« {g['geste']} » part de " + ("Paris, qui n'a pas de barre ce jour" if g["depart"] == "paris"
                                                          else "la ligne, qui n'existe pas à ce moment"))
                break
            fp, fv = float(g["facteur"]), float(g["facteur_volume"])
            if g["depart"] == "paris":
                etat, venue = arrondir(base, fp, fv), SOURCE_PARIS
            else:
                etat = appliquer(base, fp, fv)
            if etat[3] != float(g["close_apres"]):
                motif = f"« {g['geste']} » : clôture après {g['close_apres']}, le rejeu donne {etat[3]}"
                break
        barre = series.get(v, {}).get(d)
        if motif is None:
            if barre is not None and etat is None:
                motif = "le journal la retire, le fichier l'a" if gestes else "ligne sans origine ni geste au journal"
            elif barre is None and etat is not None:
                motif = ("le journal l'écrit, le fichier ne l'a pas" if gestes
                         else "ligne de l'origine absente du fichier, sans geste qui la retire")
            elif barre is not None and etat is not None:
                faux = [c for i, c in enumerate(("ouverture", "plus haut", "plus bas", "clôture", "volume"))
                        if barre[i] != etat[i]]
                if faux:
                    motif = f"{', '.join(faux)} : le fichier a {barre}, le rejeu donne {etat}"
                elif sources.get((v, d)) != venue:
                    motif = (f"colonne source « {sources.get((v, d))} », le rejeu part de "
                             f"{'Paris' if venue == SOURCE_PARIS else 'Yahoo'} (« {venue} »)")
        if motif:
            cas.append(f"{v} {d} : {motif}")
    return sorted(cas)


def _empreinte(chemin):
    """Rend l'empreinte SHA-256 d'un fichier, en hexadécimal minuscule.

    ① RÔLE — K23 : reconnaître un fichier dans un état donné.
    ② CONTEXTE D'APPEL — `maillons_manquants`.
    ③ ENTRÉE — `chemin` : un fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — Lire par blocs, hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un nom ne dit pas l'état d'un fichier ; l'empreinte, si.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _chemin(x):
    """Rend un chemin du registre sous une seule écriture : barres obliques, sans « ./ » ni « .. » superflus.

    ① RÔLE — Qu'un même fichier ait un seul nom dans K23.
    ② CONTEXTE D'APPEL — `maillons_manquants`.
    ③ ENTRÉE — `x` : un chemin depuis la racine du dépôt, tel qu'écrit.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin normalisé.
      [rend: 1]
    ⑥ TRAITEMENT — Les barres inverses deviennent des barres obliques ; posixpath.normpath.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 13-10-2026 : « donnees\\X.csv » faisait d'un fichier présent un
      téléchargement non vérifié, « ./donnees/X.csv » un refus à tort.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import posixpath
    return posixpath.normpath(x.strip().replace("\\", "/"))


ADRESSE_ENTIERE = re.compile(r"https?://[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+(?::[0-9]+)?(?:/\S*)?")
# K23 : la seule forme d'une adresse acceptée — pour un téléchargement (`adresse`) et pour chaque morceau de la colonne
# `source` d'un fichier écrit à la main. CE QU'ELLE VÉRIFIE : « http:// » ou « https:// » en tête, rien avant ; puis au
# moins deux suites de lettres, chiffres ou tirets séparées par des points ; un port facultatif ; puis rien, ou « / »
# suivi de caractères sans espace. CE QU'ELLE NE VÉRIFIE PAS : que le nom d'hôte soit valable (« https://-.- » et
# « http://1.2 » passent) ; une adresse dont « ? » suit directement l'hôte (« https://www.bnains.org?x=1 ») est refusée à
# tort ; une adresse qui contient « ; » est coupée en deux par la lecture de la colonne `source`. Superviseur n° 3 du
# 19-10-2026 : une seule règle d'adresse dans K23 (R-708) ; « http://. » et « xhttps://y » passaient la règle d'avant.
# Superviseur n° 4 du même jour : la resserrer encore ne gagne rien sur les 82 adresses réelles et refuserait à tort
# une adresse IP ou un nom de domaine en alphabet non latin — un fraudeur passe toute règle avec « https://exemple.org » ;
# c'est un filet de forme (décision de Jean-Luc du 17-10-2026 à 16h10), pas une preuve.


def chemin_du_depot(racine, x):
    """Dit si un texte est le chemin relatif d'un fichier du dépôt, et le rend normalisé.

    ① RÔLE — K23 : la seule vérification qu'un chemin écrit au registre (`lu`) ou dans un fichier écrit à la main
      (`fichiers_cites`) désigne un fichier du dépôt, et rien d'autre.
    ② CONTEXTE D'APPEL — `remonter` (les fichiers lus d'un programme) ; `sources_ecrites_a_la_main` (les fichiers cités).
    ③ ENTRÉE — `racine` : la racine du dépôt · `x` : le texte d'un chemin, tel qu'écrit.
    ④ CONDITIONS D'ENTRÉE — `x` n'est pas vide (les appelants ôtent les morceaux vides).
    ⑤ SORTIE — DEUX valeurs : le chemin normalisé (`_chemin`) et None ; ou None et le défaut, en un texte. Un dossier
      rend le chemin ET le défaut « un dossier », pour que l'appelant le nomme.
      [rend: 2]
    ⑥ TRAITEMENT — Refuser un chemin absolu (« / » en tête, ou une lettre de lecteur), un composant « .. », tout
      composant qui est un lien symbolique ; signaler un dossier (« . » compris) ; rendre le reste. Un test « hors de la
      racine » a été retiré le 19-10-2026 : sur 23 331 chemins essayés, il n'était jamais atteint, les deux refus d'avant
      le couvrant (superviseur n° 4, M7).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du 19-10-2026 (D2) : « /etc/hostname », « ../hors.csv » et un lien vers l'extérieur passaient
      pour des fichiers du dépôt, et le verdict dépendait de la machine ; superviseur n° 3 du même jour : le même défaut
      vivait dans `lu`, d'où une seule fonction pour les deux (deux implémentations d'une même chose divergent toujours,
      R-708).
    ⑨ CE QUI CLOCHE — L'existence du fichier n'est pas vérifiée ici, et ses deux appelants la traitent différemment :
      pour un fichier lu, `remonter` la vérifie par son empreinte, et un fichier absent n'y passe que comme
      téléchargement ; pour un fichier cité, `sources_ecrites_a_la_main` refuse un fichier absent avant de le rendre
      (réponse de Jean-Luc du 19-10-2026, « 1 — Oui, le refuser »). · Sous Windows ou macOS, la casse d'un nom ne compte pas : le
      verdict dépend donc de la machine (sous Linux, « Donnees/B.csv » est refusé). · Une barre inverse est ramenée à
      « / », comme `_chemin` le fait déjà pour `lu`.
    ⑩ EFFET — Regarde le disque (liens, dossier).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c = x.strip().replace("\\", "/")
    if c.startswith("/") or re.match(r"[A-Za-z]:", c):
        return None, "un chemin absolu"
    if ".." in c.split("/"):
        return None, "un chemin qui sort par « .. »"
    n = _chemin(c)
    partiel = racine
    for morceau in n.split("/"):
        partiel = os.path.join(partiel, morceau)
        if os.path.islink(partiel):
            return None, "un lien symbolique"
    if os.path.isdir(os.path.join(racine, n)):
        return n, "un dossier"
    return n, None


def sources_ecrites_a_la_main(racine, f):
    """Dit si un fichier écrit à la main cite sa source ligne par ligne, et rend les fichiers du dépôt qu'il cite.

    ① RÔLE — K23 : la propriété qui distingue un fichier vraiment écrit à partir de documents d'un fichier sans origine
      qu'on inscrirait « écrit à la main » pour passer.
    ② CONTEXTE D'APPEL — `remonter`, dans `maillons_manquants`, pour une ligne du registre ECRIT_A_LA_MAIN ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `f` : le chemin normalisé du fichier, depuis la racine.
    ④ CONDITIONS D'ENTRÉE — Le fichier est présent (`remonter` l'a vérifié par son empreinte).
    ⑤ SORTIE — DEUX valeurs : le défaut, en un texte, ou None ; la liste triée des fichiers du dépôt cités.
      [rend: 2]
    ⑥ TRAITEMENT — Lire l'en-tête d'abord : un fichier qui n'est pas un CSV portant les trois colonnes
      COLONNES_DES_SOURCES_A_LA_MAIN est refusé sans lire le reste · puis chaque enregistrement : `citation` non vide ;
      `source` vide, ou des adresses séparées par « ; », chacune ENTIÈRE (ADRESSE_ENTIERE) ; `fichiers_cites` vide, ou
      des chemins séparés par « ; », chacun un fichier du dépôt (`chemin_du_depot`) ET présent sur le disque — un
      fichier cité absent est refusé, même inscrit comme téléchargement ; au moins une adresse ou un fichier
      cité · un fichier sans enregistrement est refusé · les fichiers cités sont rendus, pour que `remonter` les remonte à
      leur tour. Aucun chemin n'est cherché dans un texte libre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 19-10-2026 à 07h05 (« 1 » à « Ajouter au registre une origine « écrit à la
      main », avec sa preuve ») ; le critère qu'il a reçu : « un cours doit pouvoir se remonter jusqu'à ce qui l'a fait
      naître ; pour ces fichiers, c'est un document cité ligne par ligne ». Superviseur du même jour (R-759) : sans cette
      propriété, yahoo_ohlcv_propre.csv, bnains_cac40.csv et evenements.json, inscrits « à la main », passaient. Décision
      de Jean-Luc du même jour à 08h23 (« 1 » à « Une colonne à part pour les fichiers cités. La colonne source ne garde
      que les adresses web, et une nouvelle colonne liste les fichiers du dépôt, séparés par « ; ». Le contrôle les vérifie
      comme il vérifie déjà les fichiers lus, sans rien deviner ») : chercher des chemins dans le texte libre de `source`
      laissait des trous (12 sur la première réparation, superviseur n° 2 ; « fichier.csv voir http://x » passait,
      relecteur n° 1). Le refus d'un fichier cité absent : question posée à Jean-Luc le 19-10-2026 (« Un fichier cité par
      une ligne tapée à la main doit-il obligatoirement être dans le dépôt ? »), réponse « 1 — Oui, le refuser » (lue à
      18h11) : un fichier cité doit pouvoir s'ouvrir ; un document téléchargé et non gardé se cite par son adresse web.
      Le refus vit ici et non dans `chemin_du_depot`, que partagent les fichiers lus : un fichier lu peut être un
      téléchargement absent du dépôt (superviseur n° 4 : placé là, il faisait passer le brouillon du registre de 45 à
      106 défauts).
    ⑨ CE QUI CLOCHE — La forme seule est vérifiée : une citation « x » passe, une adresse qui ne dit pas ce que la citation
      prétend passe ; le fond reste au relecteur (décision de Jean-Luc du 17-10-2026 à 16h10). · Des colonnes ajoutées par
      fraude à un fichier passeraient ; elles changeraient son empreinte et ce que lisent les programmes. · Le contrôle de
      l'en-tête CHANGE le verdict : sans lui, un fichier privé de la colonne `source` ou de la colonne `fichiers_cites`
      passerait dès que ses lignes remplissent l'autre ; seul un fichier privé de `citation` tomberait quand même
      (superviseur n° 4 du 19-10-2026, M5 ; la phrase d'avant, juste avec deux colonnes, ne l'était plus avec trois).
      · Un fichier du dépôt cité par une adresse web (par exemple son adresse GitHub) passe sans être remonté ni comparé
      à son empreinte : le refuser demanderait d'épeler les noms des dépôts et des hôtes, une énumération (relecteur
      n° 2 et superviseur n° 4 du 19-10-2026, M2 ; BACKLOG A-599). · Un fichier cité dit seulement « cette ligne
      s'appuie sur ce fichier » : rien ne vérifie que le fichier cité porte bien la ligne qui l'appuie (par exemple, que
      DETACHEMENTS_OFFICIELS.csv porte la ligne Accor/Edenred que cite la ligne ACCOR 2010 des ajustements de Yahoo —
      superviseur n° 3 du 19-10-2026, H1).
    ⑩ EFFET — Lit le fichier ligne à ligne, jusqu'au premier défaut ; regarde le disque pour chaque fichier cité.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    source, citation, cites_col = COLONNES_DES_SOURCES_A_LA_MAIN
    cites, vu = set(), False
    try:
        with open(os.path.join(racine, f), encoding="utf-8-sig", newline="") as fl:
            lecteur = csv.DictReader(fl)
            if not set(COLONNES_DES_SOURCES_A_LA_MAIN) <= set(lecteur.fieldnames or []):
                return f"sans les colonnes {', '.join(COLONNES_DES_SOURCES_A_LA_MAIN)}", []
            for x in lecteur:
                vu, n = True, lecteur.line_num
                if not (x.get(citation) or "").strip():
                    return f"ligne {n} sans {citation}", []
                adresses = [m.strip() for m in (x.get(source) or "").split(";") if m.strip()]
                for m in adresses:
                    if not ADRESSE_ENTIERE.fullmatch(m):
                        return f"ligne {n} : {source} « {m[:60]} », pas une adresse http(s) entière", []
                chemins = [m.strip() for m in (x.get(cites_col) or "").split(";") if m.strip()]
                for m in chemins:
                    c, defaut = chemin_du_depot(racine, m)
                    if defaut:
                        return f"ligne {n} : {cites_col} « {m[:60]} », {defaut}", []
                    if not os.path.isfile(os.path.join(racine, c)):
                        return f"ligne {n} : {cites_col} « {m[:60]} », absent du dépôt", []
                    cites.add(c)
                if not adresses and not chemins:
                    return f"ligne {n} : ni adresse en {source} ni fichier en {cites_col}", []
    except (UnicodeDecodeError, csv.Error):
        return f"illisible comme un CSV portant les colonnes {', '.join(COLONNES_DES_SOURCES_A_LA_MAIN)}", []
    if not vu:
        return "sans aucune ligne", []
    return None, sorted(cites)


def maillons_manquants(racine, fichiers):
    """Rend ce qui manque pour remonter chaque fichier jusqu'à un premier maillon : un téléchargement, ou un fichier écrit à la main.

    ① RÔLE — K23, la provenance : chaque fichier dont viennent les lignes contrôlées doit se remonter, par le registre de
      provenance, jusqu'à au moins un premier maillon, sans boucle : un téléchargement dont l'adresse et l'empreinte sont
      dites, ou un fichier écrit à la main qui cite sa source ligne par ligne (`sources_ecrites_a_la_main`).
    ② CONTEXTE D'APPEL — `main`, pour K23 ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `fichiers` : les chemins, depuis la racine, à remonter.
    ④ CONDITIONS D'ENTRÉE — Le registre, s'il existe, a l'en-tête PROVENANCE_DES_FICHIERS, sinon ValueError.
      · DANS K23, « AU DÉPÔT » VEUT DIRE « DANS LE DOSSIER CONTRÔLÉ » (`racine`) : K23 regarde le disque, il ne demande
      pas à git ce que le dépôt garde. Sur une copie fraîche du dépôt, c'est la même chose. Sur une machine qui porte
      des fichiers que git ne garde pas (une archive retéléchargée sous hors_depot/, un dossier ignoré), un programme,
      un fichier lu ou un fichier cité peut passer à tort. LE VERDICT QUI FAIT FOI EST CELUI D'UNE COPIE FRAÎCHE. Décision
      de Jean-Luc du 19-10-2026 à 19h56 (« 1 » à « L'écrire une fois et fermer le trou plus tard ») ; le trou se ferme
      quand K23 sera branché au circuit, qui travaille toujours sur une copie fraîche (BACKLOG A-599, rattaché à A-578).
      Relecteur n° 3 et superviseur n° 5 du même jour (N1) : fermer le trou en demandant à git la liste des fichiers
      gardés faisait tomber 7 épreuves sur 61.
    ⑤ SORTIE — UNE valeur : la liste des cas, un texte par maillon manquant, triés et sans doublon.
      [rend: 1]
    ⑥ TRAITEMENT — Registre absent : un cas par fichier. Sinon, chaque fichier est remonté (`remonter`) : ① ses lignes
      au registre (chemins normalisés, `_chemin`) ; présent au dépôt : exactement une ligne à son empreinte actuelle ;
      absent : exactement une ligne de téléchargement ; un fichier déclaré réparé (CONTRATS.FICHIERS_REPARES) doit y
      être produit par le programme déclaré · ② un téléchargement porte une adresse http(s) et une empreinte de
      64 caractères hexadécimaux ; s'il est présent au dépôt, son empreinte est celle du fichier ; il ARRÊTE la remontée
      · ②bis un fichier écrit à la main (après la garde des fichiers réparés) est présent, sans fichier lu, sans
      adresse, avec une preuve, et cite sa source ligne par ligne ; chaque fichier du dépôt qu'il cite est remonté à son
      tour ; sinon il ARRÊTE la remontée · ③ sinon, la ligne nomme un programme (.py) présent au dépôt et au moins un
      fichier lu, chacun un fichier, chacun remonté à son tour ; au moins une branche doit arriver à un premier maillon
      · ④ un fichier rencontré une seconde fois sur le même chemin est une boucle : cas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Même demande et même décision que `lignes_non_rejouees`. Constat du 13-10-2026 : le fichier
      Yahoo d'origine est déjà nettoyé ; le téléchargement brut et les cinq programmes qui l'ont produit ne sont pas au
      dépôt (A-538 ④) ; rien ne déclare d'où il vient. Relecture indépendante du même jour : une boucle sans aucun
      téléchargement passait (« A lu par A »), et plusieurs lignes du même fichier, un programme qui n'en était pas un,
      une empreinte vide, une adresse « x », un dossier lu, aussi ; tous sont refusés. Relecture de Cowork du même soir
      (91d4ac8, cassure I) : le fichier réparé inscrit comme « téléchargement » passait ; refusé. Le premier maillon
      « écrit à la main » : décision de Jean-Luc du 19-10-2026 à 07h05 ; quatre fichiers lus par la réparation sont
      écrits à partir de documents (inventaire du 18-10-2026), et le registre ne savait pas le dire.
    ⑨ CE QUI CLOCHE — Un téléchargement absent du dépôt n'est pas vérifiable ici : son empreinte est écrite, pas
      recalculée. · Aucune garde ne vérifie qu'une adresse inscrite rend bien le fichier : l'empreinte dit qu'on parle
      du même fichier, pas d'où il vient (Cowork, 91d4ac8). · Le registre dit qu'un programme a produit un fichier ; il ne prouve pas que ce programme, relancé,
      le referait (R-731 et les épreuves de chaque programme le prouvent). · Un registre FAUX mais cohérent passe : le
      registre s'écrit, il se relit (A-578). · La preuve d'un fichier écrit à la main n'est pas
      vérifiée ici : une preuve « x » passe.
    ⑩ EFFET — Lit le registre et les fichiers qu'il nomme.
    ⑪ TERMINAISON — Rend la main ou lève. La remontée s'arrête : un fichier déjà sur le chemin n'est pas suivi.
      [sort: non]
    """
    chemin_registre = os.path.join(racine, PROVENANCE)
    if not os.path.exists(chemin_registre):
        return sorted(f"{f} : aucun registre de provenance ({PROVENANCE}) — son premier maillon n'est déclaré nulle "
                      f"part" for f in fichiers)
    with open(chemin_registre, encoding="utf-8", newline="") as fl:
        lecteur = csv.DictReader(fl)
        if lecteur.fieldnames != PROVENANCE_DES_FICHIERS:
            raise ValueError(f"{chemin_registre} : en-tête {lecteur.fieldnames} au lieu de {PROVENANCE_DES_FICHIERS}")
        registre = list(lecteur)
    cas = set()

    def remonter(f, chemin):
        """Rend vrai si un fichier se remonte jusqu'à un premier maillon ; inscrit dans `cas` ce qui manque.

        ① RÔLE — Remonter un fichier d'un maillon, puis ses sources.
        ② CONTEXTE D'APPEL — `maillons_manquants`, une fois par fichier demandé ; elle-même, pour chaque fichier lu.
        ③ ENTRÉE — `f` : un chemin normalisé · `chemin` : les fichiers déjà traversés pour arriver ici.
        ④ CONDITIONS D'ENTRÉE — `registre` et `cas` existent (fonction englobante).
        ⑤ SORTIE — UNE valeur : vrai si au moins une branche arrive à un premier maillon valide (téléchargement, ou
          fichier écrit à la main dont toutes les sources se remontent).
          [rend: 1]
        ⑥ TRAITEMENT — ⑥ ①-④ de `maillons_manquants`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — ⑧ de `maillons_manquants`.
        ⑨ CE QUI CLOCHE — Un fichier lu par deux branches est remonté deux fois : sans boucle, le coût reste fini.
          · Le vrai ou faux rendu ne décide jamais du verdict : chaque refus est déjà inscrit dans `cas` quand il est
          rendu ; il ne décide que du message du parent (« aucune de ses sources n'arrive… », « cite comme source …,
          qui ne se remonte pas »). Mesuré par le superviseur n° 4 du 19-10-2026 : `remonter` forcé à toujours rendre
          vrai, aucun des 54 verdicts ne change. L'épreuve H62 exige ce message (« le parent le dit »).
        ⑩ EFFET — Ajoute à `cas` ; lit les fichiers nommés.
        ⑪ TERMINAISON — Rend la main : un fichier déjà sur `chemin` arrête la branche, et le registre est fini.
          [sort: non]
        """
        if f in chemin:
            cas.add(f"{f} : boucle dans la provenance ({' → '.join(chemin + [f])})")
            return False
        lignes = [r for r in registre if _chemin(r["fichier"]) == f]
        present = os.path.isfile(os.path.join(racine, f))
        if present:
            e = _empreinte(os.path.join(racine, f))
            lignes = [r for r in lignes if r["sha256"].strip().lower() == e]
            if len(lignes) != 1:
                cas.add(f"{f} : son empreinte actuelle ({e[:16]}…) est inscrite {len(lignes)} fois au registre, au lieu "
                        f"d'une")
                return False
        else:
            lignes = [r for r in lignes if r["produit_par"] == TELECHARGEMENT]
            if len(lignes) != 1:
                cas.add(f"{f} : absent du dépôt, et le registre en fait {len(lignes)} téléchargement(s), au lieu d'un")
                return False
        r = lignes[0]
        if f in FICHIERS_REPARES and _chemin(r["produit_par"]) != FICHIERS_REPARES[f]:
            cas.add(f"{f} : déclaré écrit par {FICHIERS_REPARES[f]} (CONTRATS.FICHIERS_REPARES), inscrit au registre "
                    f"comme produit par « {r['produit_par']} »")
            return False
        if r["produit_par"] == ECRIT_A_LA_MAIN:          # après la garde des fichiers réparés, jamais avant
            if r["lu"].strip():
                cas.add(f"{f} : écrit à la main, mais le registre lui donne des fichiers lus")
                return False
            if r["adresse"].strip():
                cas.add(f"{f} : écrit à la main, mais le registre lui donne une adresse — une adresse dit un téléchargement")
                return False
            if not r["preuve"].strip():
                cas.add(f"{f} : écrit à la main, sans preuve (la décision ou le commit qui l'atteste)")
                return False
            defaut, cites = sources_ecrites_a_la_main(racine, f)
            if defaut:
                cas.add(f"{f} : écrit à la main, {defaut}")
                return False
            arrive = True
            for x in cites:
                if not remonter(x, chemin + [f]):
                    cas.add(f"{f} : cite comme source {x}, qui ne se remonte pas")
                    arrive = False
            return arrive
        if r["produit_par"] == TELECHARGEMENT:
            if not ADRESSE_ENTIERE.fullmatch(r["adresse"].strip()):
                cas.add(f"{f} : téléchargement sans adresse http(s)")
                return False
            if not re.fullmatch(r"[0-9a-f]{64}", r["sha256"].strip().lower()):
                cas.add(f"{f} : téléchargement sans empreinte de 64 caractères")
                return False
            return True
        programme = _chemin(r["produit_par"])
        if not (programme.endswith(".py") and os.path.isfile(os.path.join(racine, programme))):
            cas.add(f"{f} : produit par {r['produit_par']}, qui n'est pas un programme du dépôt")
            return False
        lus = [x for x in r["lu"].split(";") if x.strip()]
        if not lus:
            cas.add(f"{f} : produit par {programme}, sans aucun fichier lu déclaré")
            return False
        arrive = False
        for brut in lus:
            x, defaut = chemin_du_depot(racine, brut)
            if defaut == "un dossier":
                cas.add(f"{f} : lit {x}, qui est un dossier")
                continue
            if defaut:
                cas.add(f"{f} : lit « {brut.strip()} », {defaut}")
                continue
            arrive = remonter(x, chemin + [f]) or arrive
        if not arrive:
            cas.add(f"{f} : aucune de ses sources n'arrive à un premier maillon (téléchargement ou fichier écrit à la main)")
        return arrive

    for f in fichiers:
        remonter(_chemin(f), [])
    return sorted(cas)


def main(argv):
    """Lit, contrôle, affiche ; rend le code de sortie.

    ① RÔLE — Porter la ligne de commande.
    ② CONTEXTE D'APPEL — Le bloc final ; les épreuves.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — ④ du programme.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme. Chaque contrôle affiche son nombre et ses huit premiers cas, et
      dit combien il en reste.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un compte sans exemple ne se vérifie pas ; une liste coupée sans le dire ment.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche le compte rendu.
    ⑪ TERMINAISON — Rend la main ; l'erreur imprévue est changée en 2 par le bloc final.
      [sort: non]
    """
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : CONTROLER_L_HISTORIQUE_LONG.py <racine> [fichier à contrôler]")
        return 2
    racine = argv[0]
    fichier = os.path.join(racine, argv[1] if len(argv) > 1 else FICHIER)
    try:
        series, defauts, venues_de_bnains = lire_cours(fichier)
        bnains, defauts_b, fausses = lire_paris(racine)
        a_defaire = lire_a_defaire(os.path.join(racine, VERDICTS_YAHOO))
        evenements = sans_les_divisions_fausses(json.load(open(os.path.join(racine, EVENEMENTS), encoding="utf-8")),
                                                a_defaire)
        detachements, sans_date = lire_detachements(os.path.join(racine, DROITS), os.path.join(racine, OFFICIELS))
        francfort = lire_francfort(os.path.join(racine, FRANCFORT))
        indice = lire_indice(os.path.join(racine, INDICE))
        origine, defauts_o, _ = lire_cours(os.path.join(racine, ORIGINE))
        citations = lire_citations(os.path.join(racine, OFFICIELS))
        alignes = lire_alignes(os.path.join(racine, JOURNAL))
        with open(fichier, encoding="utf-8", newline="") as f:
            a_la_source = "source" in (next(csv.reader(f), []))
        relatif = _chemin(os.path.relpath(fichier, racine))
        declare = relatif in FICHIERS_REPARES      # K23 : « réparé » se déclare (CONTRATS.FICHIERS_REPARES)…
        repare = declare or a_la_source            # … ou se voit à la colonne source
        k23 = [f"{relatif} : déclaré réparé (écrit par {FICHIERS_REPARES[relatif]}) mais sans colonne source — ses lignes "
               f"ne se remontent pas"] if declare and not a_la_source else []
        k23 += maillons_manquants(racine, [relatif] if not repare     # le fichier lui-même, et ses deux sources
                                  else [relatif, ORIGINE.replace(os.sep, "/"), BNAINS.replace(os.sep, "/")])
        if repare and a_la_source:
            if defauts_o:      # superviseur du 18-10-2026 : le rejeu part de ce fichier ; abîmé, il ne prouve rien (R-734)
                raise ValueError(f"{ORIGINE} : {len(defauts_o)} défaut(s) de lecture, dont {defauts_o[0]} — K23 ne peut "
                                 f"pas rejouer le journal sur une origine abîmée")
            journal = lire_journal(os.path.join(racine, JOURNAL))
            k23 += lignes_non_rejouees(series, lire_les_sources(fichier), origine, bnains, journal)
    except (OSError, ValueError) as e:
        print(f"ARRÊT — le contrôle n'a pas pu tourner : {type(e).__name__} : {e}")
        return 2
    if defauts_b:
        print(f"ARRÊT — l'extrait bnains a {len(defauts_b)} défaut(s) de lecture, dont : {defauts_b[0]}")
        return 2
    if not bnains:      # relecture du 09-10-2026 : un extrait vide faisait passer le contrôle entier, code 0 (R-734)
        print("ARRÊT — l'extrait bnains est vide : aucune seconde source, le contrôle ne peut pas juger")
        return 2
    print(f"contrôlé : {os.path.relpath(fichier, racine)} — {sum(len(s) for s in series.values())} lignes, "
          f"{len(series)} valeurs · seconde source : {BNAINS}, moins {len(fausses)} barres prouvées fausses ({FAUSSES})")
    refus = []
    for num, titre, bloquant, cas in controler(series, defauts, bnains, evenements, venues_de_bnains, detachements,
                                               sans_date, fausses, francfort, indice, origine, a_defaire,
                                               citations, alignes, seances=CAL.lire_les_seances(racine)) + [
            ("K23", "lignes que le journal des réparations ne refait pas depuis leur source, et maillons de provenance "
                    "manquants (A-578)", True, k23)]:
        etat = ("REFUS" if cas else "ok") if bloquant else "signalé"
        print(f"{num:>4} {etat:<7} {len(cas):>6} — {titre}")
        for c in cas[:8]:
            print(f"            {c}")
        if len(cas) > 8:
            print(f"            … et {len(cas) - 8} de plus")
        if bloquant and cas:
            refus.append(num)
    print("VERDICT : " + (f"REFUSÉ par {', '.join(refus)}" if refus else "aucun contrôle bloquant n'a rien trouvé"))
    return 1 if refus else 0


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as e:
        print(f"ARRÊT — erreur imprévue {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
