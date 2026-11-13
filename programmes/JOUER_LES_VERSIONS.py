#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JOUER_LES_VERSIONS.py — Jeu 08-10-2026 (Paris)
EN ESSAI · outil · Rôle : rejouer chaque version d'une combinatoire avec le vrai juge des stratégies.
Quand l'appeler : à la main, après DECLINER_LES_STRATEGIES.

USAGE
    python3 JOUER_LES_VERSIONS.py <racine_du_depot> <combinatoire> <fichier_resultats> [--cours=<fichier>]
    exemple :
    python3 programmes/JOUER_LES_VERSIONS.py . \
        donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv \
        donnees/combinatoires/RESULTATS_C5E10-OBS-V1_E01.csv
    --cours=<fichier, relatif à la racine> : jouer sur un autre fichier de cours que le
    fichier maître, par exemple l'historique des 20 ans (plan V7, bloc 5l ⑤) ; la même
    option que le juge des stratégies, lue et refusée de la même façon, et passée au
    juge pour son calibrage. Sans l'option, le fichier maître, comme avant.

CE QUE CE PROGRAMME EST DANS LA CHAÎNE (action A-541 du BACKLOG)
    ⓪ PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES propose les réglages ;
    Jean-Luc valide · ① DECLINER_LES_STRATEGIES fabrique les versions ·
    ② CE PROGRAMME les rejoue en appelant `jouer` du juge des stratégies, sans rien
    recalculer lui-même · ③ TRIER_LES_VARIANTES (écrit le 11-11-2026, lit le fichier
    de résultats de ce programme) · ④ `juger`.

① RÔLE — Donner, pour chaque version figée d'une stratégie, le résultat qu'elle
  aurait eu sur la période de sa fiche : nombre d'opérations, réussite, gain net.
  C'est la matière que le tri et le jugement examineront.
② CONTEXTE D'APPEL — À la main, par le Chat. Aucune tâche automatique ne l'appelle.
③ ENTRÉE — La ligne de commande, trois arguments : la racine d'un dépôt (registre
  des stratégies, fichier maître des cours, référentiel, modules de signal et de
  positions, témoin du golden) ; une combinatoire écrite par DECLINER ; le chemin
  du fichier de résultats, qui ne doit pas exister. Une option facultative,
  `--cours=<fichier>` : le fichier de cours à jouer, relatif à la racine ; toute
  autre option, ou celle-ci mal écrite, arrête tout (comme le juge, 27-10-2026).
④ CONDITIONS D'ENTRÉE — ① la combinatoire n'est pas vide, toutes ses lignes
  portent la même stratégie et le même essai, ses identifiants sont uniques, et
  son nombre de lignes égale la colonne `versions_dans_l_essai`, aucun univers
  n'écrit deux fois la même valeur · ② une seule
  version y est marquée identique à la fiche · ③ la fiche existe une fois au
  registre · ④ le juge des stratégies, lancé seul sur cette fiche, se calibre sur
  le témoin du golden et rend le même résultat que ce programme · ⑤ chaque
  version, une fois fusionnée, est lue par le juge avec ses propres réglages ·
  ⑥ les cours de CHAQUE valeur vont assez loin après le début de la période pour
  laisser, après la FIN CALCULÉE (voir ⑥ du traitement), l'horizon le plus long
  plus la séance d'achat · ⑦ si un témoin de résultats existe, chaque version le
  retrouve · ⑧ le fichier nommé par `--cours=` existe.
  Le moindre manquement arrête tout, avant ou pendant le jeu.
⑤ SORTIE — UNE valeur : le code de sortie, 0 quand toutes les versions sont
  jouées et écrites, 1 sinon.
  [rend: 1]
⑥ TRAITEMENT — ① lire la ligne de commande et contrôler la combinatoire · ② lancer
  le juge des stratégies seul sur la fiche (avec le même `--cours=`) et exiger son
  calibrage · ③ charger cours et modules
  par les fonctions du juge, et la fiche par `fiches_du_registre` du contrat (sa
  DERNIÈRE ligne, n°83, depuis le 05-11-2026) · ④ jouer la fiche telle quelle et exiger le résultat
  que le juge vient d'afficher · ⑤ jouer la version identique et exiger le même
  résultat · ⑥ CALCULER LA FIN DE PÉRIODE UTILISABLE (`fin_utilisable`, plan V7,
  bloc 5g) : la plus tardive des dates, au plus la fin écrite dans la fiche, qui
  laisse à CHAQUE valeur jouée au moins « horizon le plus long + 1 » séances
  après elle ; puis recompter cette marge valeur par valeur ; si la fin calculée
  diffère de celle de la fiche, rejouer la fiche sur la période calculée ; refuser
  un recul de plus de séances que `RECUL_MAXIMUM` n'en permet (réglage lu, provisoire) ;
  demander la frontière 70/30 à `frontiere_de_la_fiche` du module de jugement ·
  ⑦ pour chaque version : fusionner, contrôler la fusion, jouer sur la période
  calculée, la couper par la même coupure (`partie_de_reglage`), écrire une ligne
  dans un fichier provisoire — chiffres de la période entière ET, colonnes « _70 »,
  chiffres de la seule partie de réglage, les seules que le tri lit ; la version identique
  doit retrouver la fiche rejouée · ⑧ comparer au témoin de résultats s'il
  existe · ⑨ renommer le fichier provisoire en fichier final.
  OÙ VIT LA FIN CALCULÉE : dans la colonne `periode_fin` de chaque ligne du
  fichier de résultats (la fin réellement jouée) ; la fin écrite dans la fiche
  est recopiée à côté, colonne `fin_ecrite_dans_la_fiche`, et le fichier de
  cours joué dans `cours_joues`, avec son empreinte. LA FICHE N'EST JAMAIS MODIFIÉE.
⑦ UNITÉ — Gains en EUROS pour 100 000 € engagés par opération ; réussite en
  POURCENTS ; tp et sl en FRACTIONS du prix d'entrée ; horizon en SÉANCES.
⑧ POURQUOI — TOUT LE CALCUL RESTE DANS LE JUGE : deux implémentations d'une même
  chose divergent toujours (R-708). Le calibrage passe par le juge lancé seul,
  parce qu'un calibrage maison comparant deux appels du même code resterait vert
  si le code ou les données changeaient (relecture du 08-10-2026, défaut A1).
  La fusion est contrôlée version par version, parce que la version identique
  à la fiche ne peut pas révéler une case oubliée (défaut A2).
⑨ CE QUI CLOCHE — ① le calibrage du juge compare le nombre d'opérations et les
  sorties, pas les frais : des frais doublés passeraient (relecture du
  08-10-2026) ; seul le témoin de résultats les attrape, et sans témoin rien ne
  les attrape · ② le DÉBUT de la période jouée est celui de la fiche, pas la
  première séance du fichier de cours : sur un fichier qui commence plus tard
  (le fichier maître commence le 02-01-2024), `periode_debut` dit une date sans
  cours — c'est arrivé le 11-11-2026, résultats « 2000-01-03 » joués sur 2024-2026 ;
  la colonne `cours_joues` le rend visible, elle ne le corrige pas · ③ la fin
  calculée dépend de l'horizon le plus long DE CETTE COMBINATOIRE et des valeurs
  de SES univers : deux stratégies d'une même campagne peuvent donc avoir des
  fins différentes, alors que le bloc 5g ① veut une fin commune (question posée
  à Jean-Luc dans echanges/A_RELIRE_TRI.md) ; une valeur dont les cours
  s'arrêtent tôt (sortie de la cote) ramène la fin de TOUTES les versions — au
  plus de `RECUL_MAXIMUM` séances, au-delà le programme refuse en la nommant ·
  ④bis le juge, lui, ne lit pas la fin calculée (relecteur neuf, D10, question
  posée) : la partie de réglage est coupée sur les bornes de la FICHE, comme le
  juge les coupe, donc la frontière 70/30 est la même des deux côtés ; seuls les
  30 % diffèrent ·
  ④ un horizon « aucune » (COMMUN.lire_horizon_ou_aucune) n'a pas de marge
  définie : `int` lève, ce programme s'arrête · ⑤ le signal est celui
  que la fiche nomme (`module_signal`, `fonction_signal`, `reglages_signal`),
  lu par `signal_de_la_fiche` du juge — depuis le 30-10-2026 (A-542), il n'est
  plus forcé à `signaux_c5etendu10` ; une version ne fait pas varier le signal ·
  ⑥ la version à zéro
  opération porte un gain de 0, que le tri devra traiter à part.
⑩ EFFET — Crée le fichier de résultats, via un fichier provisoire `.en_cours`
  effacé en cas d'échec s'il a été créé par ce lancement. Rien d'autre n'est
  écrit : le juge est lancé avec `-B`.
⑪ TERMINAISON — Sort du programme avec le code 0 ou 1. Le juge est lancé dans un
  processus séparé, sans limite de temps : s'il ne revenait pas, ce programme
  non plus.
  [sort: oui]
⑫ DÉFINITIONS
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui
    rejoue une stratégie sur l'historique des cours et rend ses opérations.
  une fiche : la ligne qui décrit une stratégie dans `donnees/cac40_strategies.csv`.
  une version : une ligne de la combinatoire, où chaque réglage n'a qu'une valeur.
  la combinatoire : le fichier `COMBINATOIRE_<STRATÉGIE>_<ESSAI>.csv` écrit par
    DECLINER_LES_STRATEGIES, une version par ligne.
  le témoin du golden : la copie conservée des cours qui ont produit les chiffres
    de référence ; le juge s'y calibre.
  la porte 0 : la fonction `porte_0` du juge, qui refuse une fiche incomplète.
"""
import csv
import os
import subprocess
import sys

sys.dont_write_bytecode = True

REGLAGES = ("tp", "sl", "horizon", "univers")
OPTION_COURS = "--cours="
RECUL_MAXIMUM = "donnees/combinatoires/RECUL_MAXIMUM_DE_LA_FIN.csv"


def lire_le_recul_maximum(base):
    """Lit, dans un fichier de réglages, de combien de séances la fin calculée peut au plus reculer.

    ① RÔLE — Remettre la protection que le refus « pas assez de cours » donnait avant le 11-11-2026 (un horizon
      absurde, 250 au lieu de 25, faisait refuser), sans écrire de seuil dans le code (R-743 ②).
    ② CONTEXTE D'APPEL — `main`, une fois, juste après le calcul de la fin ; les épreuves, par import.
    ③ ENTRÉE — `base` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — `RECUL_MAXIMUM` existe sous la racine, en-tête « reglage, valeur, unite, statut, source »,
      une seule ligne, réglage `recul_maximum`, valeur entière positive ou nulle, unité `seances`, statut non vide.
    ⑤ SORTIE — TROIS valeurs : le recul maximum en séances ; son statut (« PROVISOIRE, À DÉCIDER PAR JEAN-LUC » tant
      que Jean-Luc n'a pas décidé) ; sa source.
      [rend: 3]
    ⑥ TRAITEMENT — ① lire le fichier · ② contrôler l'en-tête, la ligne unique, le nom, l'unité, l'entier, le statut.
    ⑦ UNITÉ — Des séances (dates de cours distinctes des valeurs jouées).
    ⑧ POURQUOI — Relecteur neuf du 11-11-2026, D6 : sans plafond, une faute de frappe sur l'horizon, ou une seule
      valeur dont les cours s'arrêtent tôt, ramenait la fin de TOUTES les versions de plusieurs mois sans arrêt. Le
      plafond est une décision de Jean-Luc (question 6 de la note de la mission TRI) : la valeur du fichier est
      provisoire et le dit.
    ⑨ CE QUI CLOCHE — Le fichier ne vit pas au REGISTRE : c'est un réglage provisoire ; s'il devient une règle, il
      s'y écrira et ce fichier sera lu de là.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si le fichier manque ou est mal écrit.
      [sort: non]
    """
    chemin = os.path.join(base, RECUL_MAXIMUM)
    if not os.path.isfile(chemin):
        raise ValueError("réglage introuvable : %s (le recul maximum de la fin ne peut pas être contrôlé)"
                         % RECUL_MAXIMUM)
    lecteur = csv.DictReader(open(chemin, encoding="utf-8-sig"))
    lignes = list(lecteur)
    if lecteur.fieldnames != ["reglage", "valeur", "unite", "statut", "source"] or len(lignes) != 1:
        raise ValueError("%s : il faut l'en-tête « reglage, valeur, unite, statut, source » et une seule ligne"
                         % RECUL_MAXIMUM)
    l = lignes[0]
    v = (l["valeur"] or "").strip()
    if l["reglage"].strip() != "recul_maximum" or l["unite"].strip() != "seances" or not v.isdigit() \
            or not (l["statut"] or "").strip():
        raise ValueError("%s : attendu « recul_maximum », un entier de séances et un statut ; lu %r" % (RECUL_MAXIMUM, l))
    return int(v), l["statut"].strip(), (l["source"] or "").strip()


def recul_en_seances(dates_par_valeur, fin, fin_de_la_fiche):
    """Compte de combien de séances la fin calculée recule par rapport à celle de la fiche.

    ① RÔLE — Mesurer le recul que `lire_le_recul_maximum` borne.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves, par import.
    ③ ENTRÉE — `dates_par_valeur` : {valeur : dates triées} des valeurs jouées · `fin` : la fin calculée ·
      `fin_de_la_fiche` : la fin écrite dans la fiche.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de dates de séance distinctes, toutes valeurs jouées réunies, après `fin` et au
      plus tard à `fin_de_la_fiche`.
      [rend: 1]
    ⑥ TRAITEMENT — Réunir les dates, garder celles de l'intervalle, compter.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Ce sont ces séances-là que la période jouée perd.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return len({d for ds in dates_par_valeur.values() for d in ds if fin < d <= fin_de_la_fiche})


def empreinte_des_cours_jusqu_a(chemin, fin):
    """Rend l'empreinte des seules séances d'un fichier de cours datées au plus tard de la fin de la fiche.

    ① RÔLE — Identifier les cours qui ont servi au choix, sans dépendre des séances ajoutées ensuite.
    ② CONTEXTE D'APPEL — `main` (écrit l'empreinte dans les résultats) ; `frontiere_attendue` de
      `programmes/TRIER_LES_VARIANTES.py` (la recalcule), par import : une seule écriture (R-708).
    ③ ENTRÉE — `chemin` : un fichier de cours au format du fichier maître (colonne `date`) · `fin` : la fin écrite
      dans la fiche, AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — Le fichier a une colonne `date`.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux (SHA-256 de l'en-tête et des lignes retenues, dans
      l'ordre du fichier).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire l'en-tête et repérer `date` · ② garder chaque ligne dont la date est ≤ `fin`, telle
      qu'écrite · ③ hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecteur de la mission TRI, tour 3, M2 : le fichier maître grandit chaque soir ; une empreinte
      du fichier ENTIER rendait intriable le lendemain un fichier de résultats dont la fiche finit avant les
      séances ajoutées. Ce que le tri garantit (frontière et colonnes « _70 ») ne dépend que des séances jusqu'à la
      fin de la fiche : c'est la propriété qui compte. Une séance passée révisée change l'empreinte, et c'est voulu.
    ⑨ CE QUI CLOCHE — ① Les colonnes de la période ENTIÈRE dépendent aussi des séances après la fin (sorties des
      dernières positions) : l'empreinte ne les protège pas ; le tri ne les lit pas. ② Une ligne déplacée dans le
      fichier sans changer de contenu change l'empreinte (ordre gardé).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sans colonne `date`.
      [sort: non]
    """
    import hashlib
    h = hashlib.sha256()
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        if "date" not in entete:
            raise ValueError("%s : pas de colonne « date »" % chemin)
        i = entete.index("date")
        h.update(("\x1f".join(entete) + "\n").encode("utf-8"))
        for ligne in lecteur:
            if len(ligne) > i and ligne[i] <= fin:
                h.update(("\x1f".join(ligne) + "\n").encode("utf-8"))
    return h.hexdigest()[:16]


def partie_de_reglage(mod_jug, ops, seances_de_la_fiche, horizon, frontiere):
    """Rend la partie de réglage (les 70 % les plus anciens) d'une version, coupée PAR LE MODULE DE JUGEMENT.

    ① RÔLE — Donner au tri des chiffres qui ne contiennent RIEN des 30 % gardés pour le jugement.
    ② CONTEXTE D'APPEL — `main`, une fois par version.
    ③ ENTRÉE — `mod_jug` : `programmes/MODULE_JUGEMENT.py` chargé · `ops` : les opérations jouées ·
      `seances_de_la_fiche` : les dates de séance des cours lus comprises dans les bornes de la FICHE · `horizon` :
      l'horizon de la version, en séances · `frontiere` : la date rendue par `frontiere_de_la_fiche` du module de
      jugement, la seule fonction qui l'établit (12-11-2026).
    ④ CONDITIONS D'ENTRÉE — Les dates sont celles du fichier de cours joué.
    ⑤ SORTIE — DEUX valeurs : l'embargo en séances (ou None sans opération), le résumé des opérations de la partie
      de réglage (`{"n": 0}` sans opération).
      [rend: 2]
    ⑥ TRAITEMENT — ① appeler `coupure_70_30` du module de jugement, avec l'horizon de la version et la frontière
      reçue · ② refuser une coupure qui ne reconnaît aucune date · ③ refuser une coupure qui a coupé à une AUTRE
      séance que la frontière reçue, celle que `main` écrit dans le fichier (relecteur, tour 3, M1) · ④ rendre son
      embargo et son résumé « res_70 ».
    ⑦ UNITÉ — Dates ; séances ; euros et pourcents dans le résumé.
    ⑧ POURQUOI — Relecteur neuf du 11-11-2026, D1 MAJEUR : le tri choisissait sur la période entière, 30 % réservés
      compris ; la version retenue n'était plus jugée hors échantillon. La coupure est celle du juge (`juger`, ligne
      `c = J.coupure_70_30(ops, _sea, horizon=_h_emb, frontiere=J.frontiere_de_la_fiche(fiche, seances, _bornes))`,
      avec `_sea` réduit aux bornes de la fiche) : importée, jamais recopiée (R-708). Le contrôle ③ compare la coupe
      RÉELLE à la valeur écrite : sans lui, une frontière DÉCLARÉE perdue en route (`frontiere=None`, ou une autre
      date) faisait couper ailleurs que la frontière écrite, et entrer des séances des 30 % dans les colonnes « _70 »
      sans bruit (sonde X4 du relecteur du 12-11-2026 : 40 opérations devenues 50). Le calendrier est construit comme dans `main` du juge (`seances = {b["date"] for s in
      cours.values() for b in s}`), une ligne recopiée faute de fonction exposée.
    ⑨ CE QUI CLOCHE — ① La frontière dépend des bornes de la FICHE, pas de la fin calculée : c'est ce que fera le
      juge, et c'est voulu (la fin ne touche que les 30 %). ② Sans opération, `coupure_70_30` ne rend pas
      d'embargo : la case reste vide.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si aucune date de signal n'est reconnue au calendrier, ou si la
      coupe réelle n'est pas la frontière reçue.
      [sort: non]
    """
    c = mod_jug.coupure_70_30(ops, seances_de_la_fiche, horizon=horizon, frontiere=frontiere)
    if "motif" in c:
        raise ValueError("coupure 70/30 impossible : %s" % c["motif"])
    if ops and c.get("frontiere") != frontiere:
        raise ValueError("la coupure a coupé au %s, la frontière écrite est le %s : rien n'est écrit"
                         % (c.get("frontiere"), frontiere))
    return c.get("embargo_seances"), c.get("res_70", {"n": 0})


def lire_la_ligne_de_commande(arguments):
    """Sépare les arguments de position et l'option `--cours=`, et refuse une option mal écrite.

    ① RÔLE — Lire la ligne de commande comme le juge des stratégies la lit (`main` du juge, lignes
      `_args = ...` et `_mal = ...`, 27-10-2026), pour que `--cours=` veuille dire la même chose ici et là.
    ② CONTEXTE D'APPEL — `main`, une fois, avant tout ; et les épreuves du tri
      (`tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py`), par import.
    ③ ENTRÉE — `arguments` : la liste des arguments, sans le nom du programme (`sys.argv[1:]`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la liste des arguments de position ; le fichier de cours nommé par
      `--cours=`, ou None sans l'option ; le motif du refus, ou None si la ligne est bien écrite.
      [rend: 3]
    ⑥ TRAITEMENT — ① séparer ce qui commence par « -- » du reste · ② refuser toute option qui n'est pas
      « --cours=<quelque chose> » · ③ refuser « --cours= » écrit deux fois · ④ rendre le fichier nommé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture et superviseur du 27-10-2026, sur le juge : « --cours fichier », sans « = »,
      était ignoré, et « fichier » devenait la fiche visée. Ici, il deviendrait le troisième argument de
      position. Le refus de deux `--cours=` est PLUS STRICT que le juge, qui prend le premier en silence :
      deux fichiers de cours pour un lancement, c'est une ligne de commande à reprendre, pas un choix.
    ⑨ CE QUI CLOCHE — C'est une seconde écriture de la lecture du juge (R-708) : le juge ne l'expose pas
      comme fonction. Si le juge accepte un jour une autre option, ce programme la refusera : il rougit,
      il ne se tait pas.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    positions = [a for a in arguments if not a.startswith("--")]
    options = [a for a in arguments if a.startswith("--")]
    mal = [a for a in options if not (a.startswith(OPTION_COURS) and len(a) > len(OPTION_COURS))]
    if mal:
        return positions, None, ("option inconnue ou mal écrite : %s (seule « --cours=<fichier> » existe)"
                                 % mal)
    if len(options) > 1:
        return positions, None, "option « --cours= » écrite %d fois : %s" % (len(options), options)
    return positions, (options[0][len(OPTION_COURS):] if options else None), None


def fin_utilisable(dates_par_valeur, debut, fin_de_la_fiche, horizon_max):
    """Calcule la fin de période la plus tardive qui laisse assez de séances après elle à chaque valeur.

    ① RÔLE — Donner, PAR PROGRAMME, la fin de la période jouée (plan V7, bloc 5g, complément du
      11-11-2026 à 20h17 : « LA FIN DE LA PÉRIODE SE CALCULE PAR PROGRAMME, ELLE NE S'ÉCRIT PAS À LA MAIN »).
    ② CONTEXTE D'APPEL — `main`, une fois, après le calibrage et la version identique ; les épreuves du tri,
      par import, sur de vraies séries de cours.
    ③ ENTRÉE — `dates_par_valeur` : pour chaque valeur jouée (son mnémonique), la liste TRIÉE des dates
      de ses séances, AAAA-MM-JJ, telle que le lecteur unique les rend · `debut` et `fin_de_la_fiche` : les
      bornes rendues par la porte 0 · `horizon_max` : l'horizon le plus long de la combinatoire, en séances.
    ④ CONDITIONS D'ENTRÉE — Au moins une valeur ; `horizon_max` est un entier positif.
    ⑤ SORTIE — DEUX valeurs : la fin calculée (AAAA-MM-JJ), ou None si aucune fin ne laisse assez de
      séances ; la valeur qui la limite (celle dont les cours s'arrêtent le plus tôt ; None si c'est la
      fiche qui limite), ou la première valeur fautive si la fin est None.
      [rend: 2]
    ⑥ TRAITEMENT — ① le besoin est `horizon_max + 1` séances après la fin : la séance d'achat (l'Open du
      lendemain du signal, R-601) puis `horizon_max` séances de détention · ② pour chaque valeur, la
      séance qui doit rester après la fin est `dates[-besoin]` ; une valeur qui n'a pas `besoin + 1`
      séances ne laisse aucune fin · ③ la borne est la plus précoce de ces séances · ④ si la borne tombe
      après la fin écrite dans la fiche, la fin de la fiche est gardée telle quelle · ⑤ sinon la fin est la
      DERNIÈRE séance, parmi celles des valeurs jouées, qui tombe avant la borne ; elle n'est donc pas
      forcément une séance de la valeur qui limite (une valeur en trou n'empêche pas les autres de jouer
      jusqu'à la veille de sa séance) · ⑥ aucune séance entre le début de la fiche et la borne vaut
      « aucune fin ».
    ⑦ UNITÉ — Des dates AAAA-MM-JJ ; des séances.
    ⑧ POURQUOI — Une position achetée le dernier jour doit avoir une fin connue, sinon elle est fermée à
      la fin des données, avant son horizon, sans alerte (relecture du 08-10-2026, défaut N3). Exemple
      réel du 11-11-2026 à 19h53 : la fiche IND-001-RETEST portait une fin au 30-10-2026 écrite à la
      main, Accor n'avait que 7 séances après, pour une durée essayée de 25 ; le Chat a dû ramener la fin
      à la main au 05-10-2026, la 26e séance d'Accor avant sa dernière. La même condition, `marge <
      h_max + 1`, existait déjà ici en REFUS : elle devient un CALCUL, et le refus reste comme garde-fou.
      La fin de la fiche n'est jamais dépassée : la fiche dit jusqu'où on a le droit de regarder.
    ⑨ CE QUI CLOCHE — ① Les séances comptées sont celles du fichier de cours, trous exclus ; une valeur
      suspendue longtemps à la fin compterait moins de jours de calendrier. ② Cette fonction ne borne pas le recul :
      `main` le borne ensuite par `lire_le_recul_maximum` (réglage provisoire, relecteur neuf du
      11-11-2026, D6) et refuse au-delà en nommant la valeur qui limite.
      ③ La fin dépend des valeurs jouées : une valeur sortie de la cote tôt ramène la fin de tous.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    besoin = horizon_max + 1
    borne, limite = None, None
    for m in sorted(dates_par_valeur):
        dates = dates_par_valeur[m]
        if len(dates) < besoin + 1:
            return None, m
        if borne is None or dates[-besoin] < borne:
            borne, limite = dates[-besoin], m
    if borne > fin_de_la_fiche:
        return fin_de_la_fiche, None          # la fiche laisse déjà assez de séances : sa fin est gardée telle quelle
    candidates = [d for ds in dates_par_valeur.values() for d in ds if debut <= d < borne]
    if not candidates:
        return None, limite
    return max(candidates), limite


def arreter(message):
    """Affiche un motif d'arrêt et rend le code d'échec.

    ① RÔLE — Donner une seule forme à tous les arrêts.
    ② CONTEXTE D'APPEL — `main`, à chaque condition manquée.
    ③ ENTRÉE — `message` : le motif, en français.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'entier 1.
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher « ARRÊT : » et le motif · ② rendre 1.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un arrêt doit se lire sans ambiguïté sur un téléphone.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Une ligne affichée.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    print("ARRÊT : %s" % message)
    return 1


def codes(texte):
    """Découpe un univers comme le juge le découpe.

    ① RÔLE — Comparer deux univers sans dépendre de l'ordre ni des espaces.
    ② CONTEXTE D'APPEL — `controler_fusion`, deux fois par version.
    ③ ENTRÉE — `texte` : un univers écrit « TTE,ENGI,... ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste TRIÉE des codes en majuscules, doublons gardés.
      [rend: 1]
    ⑥ TRAITEMENT — ① couper sur la virgule · ② retirer les espaces · ③ mettre en
      majuscules · ④ écarter le vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `jouer` découpe exactement ainsi (ligne `demandes = ...`). Une
      liste et non un ensemble : un ensemble effaçait un doublon « TTE,TTE », que
      `jouer` joue deux fois (relecture du 08-10-2026, défaut N4).
    ⑨ CE QUI CLOCHE — C'est une seconde écriture de ce découpage : si le juge
      change le sien, celui-ci ne suivra pas. Le juge n'expose pas de fonction
      à appeler.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return sorted(x.strip().upper() for x in (texte or "").split(",") if x.strip())


def fusionner(fiche, version):
    """Rend une copie de la fiche portant les réglages de la version.

    ① RÔLE — Fabriquer la fiche jouable d'une version.
    ② CONTEXTE D'APPEL — `main`, une fois par version.
    ③ ENTRÉE — `fiche` : la ligne du registre · `version` : la ligne de la
      combinatoire.
    ④ CONDITIONS D'ENTRÉE — Les deux portent tp, sl, horizon et univers.
    ⑤ SORTIE — UNE valeur : la fiche fusionnée, un nouveau dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① copier la fiche, avec le signal qu'elle nomme · ② y remplacer
      tp, sl, horizon, univers.
    ⑦ UNITÉ — tp et sl en fractions ; horizon en séances.
    ⑧ POURQUOI — DECLINER le prescrit dans son en-tête : la version ne porte que
      ce qui varie, le reste vient de la fiche.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun : la fiche d'origine n'est pas modifiée.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    f = dict(fiche)
    for k in REGLAGES:
        f[k] = version[k]
    return f


def controler_fusion(J, fusion, version):
    """Vérifie que le juge lira bien les réglages de la version.

    ① RÔLE — Empêcher qu'une case oubliée à la fusion produise un résultat faux
      sans alerte.
    ② CONTEXTE D'APPEL — `main`, une fois par version, avant de la jouer.
    ③ ENTRÉE — `J` : le module du juge · `fusion` : la fiche fusionnée ·
      `version` : la ligne de la combinatoire.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts, vide si tout concorde.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire tp et sl par `pourcent` du juge et les comparer à la
      version · ② lire l'horizon par `lire_horizon` · ③ comparer les univers.
    ⑦ UNITÉ — Fractions ; séances.
    ⑧ POURQUOI — Relecture du 08-10-2026 (défaut A2) : une fusion qui oubliait
      l'horizon écrivait 125 842,31 € pour une version à 5 séances, au lieu de
      73 093,64 €, sans aucune alerte.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; `pourcent` et `lire_horizon` peuvent lever sur
      une case illisible.
      [sort: non]
    """
    ecarts = []
    for k in ("tp", "sl"):
        if abs(J.pourcent(fusion[k]) - float(version[k])) > 1e-12:
            ecarts.append("%s lu %r, version %r" % (k, fusion[k], version[k]))
    if J.lire_horizon(fusion["horizon"]) != int(version["horizon"]):
        ecarts.append("horizon lu %r, version %r" % (fusion["horizon"], version["horizon"]))
    if codes(fusion["univers"]) != codes(version["univers"]):
        ecarts.append("univers lu %r, version %r" % (fusion["univers"], version["univers"]))
    return ecarts


def calibrer_par_le_juge(base, ident, cours=None):
    """Lance le juge seul sur la fiche et lit son verdict.

    ① RÔLE — Prouver que l'instrument retrouve les chiffres de référence avant de
      jouer quoi que ce soit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `base` : la racine du dépôt · `ident` : l'identifiant de la fiche · `cours` : le
      fichier de cours de `--cours=`, relatif à la racine, ou None pour le fichier maître.
    ④ CONDITIONS D'ENTRÉE — Le juge est dans `programmes/` sous la racine.
    ⑤ SORTIE — DEUX valeurs : vrai si le juge est calibré et rend 0 ; la ligne de
      résultat qu'il affiche pour la fiche, ou None.
      [rend: 2]
    ⑥ TRAITEMENT — ① lancer le juge avec l'identifiant, et `--cours=` s'il est donné, pour que
      la ligne qu'il affiche soit jouée sur les mêmes cours que ce programme · ② exiger le code 0, la
      phrase « calibrage sur le TEMOIN du golden » et la phrase « OK, l'instrument
      est calibre » · ③ relever la ligne
      « N operations . X % de reussite . G EUR ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le calibrage du juge compare au tableau des 100 opérations de
      référence, sur le témoin du golden. Le refaire ici serait une seconde
      écriture (R-708). Le témoin est exigé : sans lui, le juge ne compare plus
      que le nombre d'opérations et se dit quand même calibré (défaut N2).
    ⑨ CE QUI CLOCHE — Ce calibrage ne porte que sur les réglages de la fiche ; les
      autres réglages sont protégés par le témoin de résultats (voir `main`).
      Dépend du texte affiché par le juge : s'il change sa phrase,
      ce contrôle s'arrête (il rougit, il ne se tait pas).
    ⑩ EFFET — Lance un processus avec `-B`, pour que Python n'écrive pas de
      fichiers compilés ; le juge lui-même n'écrit aucun fichier.
    ⑪ TERMINAISON — Rend la main ; le processus lancé n'a pas de limite de temps.
      [sort: non]
    """
    commande = [sys.executable, "-B", os.path.join(base, "programmes", "JUGE_DES_STRATEGIES.py"), base, ident]
    if cours:
        commande.append(OPTION_COURS + cours)
    p = subprocess.run(commande, capture_output=True, text=True)
    sortie = p.stdout + p.stderr
    ok = (p.returncode == 0 and "OK, l'instrument est calibre" in sortie
          and "calibrage sur le TEMOIN du golden" in sortie)
    ligne = next((l.strip() for l in sortie.splitlines()
                  if "operations ." in l and "de reussite" in l and "EUR" in l), None)
    return ok, ligne


def bareme_du_temoin(f_comb, sid, essai):
    """Dit sous quel barème des frais le témoin de résultats a été fait, ou None sans témoin.

    ① RÔLE — Lire l'étiquette de barème du témoin (A-550, superviseur R-759, C15, 29-10-2026).
    ② CONTEXTE D'APPEL — `main`, une fois, avant de jouer les versions.
    ③ ENTRÉE — `f_comb` : la combinatoire · `sid`, `essai` : la stratégie et l'essai.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom du barème (une ligne de `donnees/BAREME_FRAIS.csv`), ou None s'il
      n'y a pas de témoin.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher le témoin à côté de la combinatoire · ② lire sa colonne `bareme` ·
      ③ exiger UNE seule valeur, non vide, sur toutes les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un montant ne se vérifie qu'avec le barème qui l'a produit (ÉTUDE 18, A1bis). Le
      témoin de C5E10-OBS-V1 E01 a été fait au courtage seul, avant la taxe : sans son étiquette, la
      moulinette, passée au barème réel, ne le retrouvait plus (mesuré le 29-10-2026 : version 0914,
      gain 71 855,72 € au lieu de 97 155,72 €) et s'arrêtait. Le superviseur a refusé de REMPLACER le
      témoin (une référence de calibrage ne se réécrit pas) : il est GARDÉ et ÉTIQUETÉ.
    ⑨ CE QUI CLOCHE — Un témoin sans colonne `bareme` arrête la moulinette (ValueError) : c'est voulu,
      un témoin sans barème ne prouve rien.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si l'étiquette manque ou varie.
      [sort: non]
    """
    f_tem = os.path.join(os.path.dirname(f_comb), "TEMOIN_RESULTATS_%s_%s.csv" % (sid, essai))
    if not os.path.exists(f_tem):
        return None
    vals = {(r.get("bareme") or "").strip() for r in csv.DictReader(open(f_tem, encoding="utf-8-sig"))}
    if len(vals) != 1 or "" in vals:
        raise ValueError("le témoin %s ne dit pas sous quel barème des frais il a été fait (colonne "
                         "« bareme », une seule valeur) : %r" % (os.path.basename(f_tem), sorted(vals)))
    return vals.pop()


def comparer_au_temoin(f_comb, sid, essai, f_resultats):
    """Compare les résultats d'un lancement au témoin de résultats, s'il existe.

    ① RÔLE — Protéger les réglages que le calibrage du juge ne touche pas : il ne
      rejoue que les réglages de la fiche.
    ② CONTEXTE D'APPEL — `main`, une fois, après avoir joué toutes les versions.
    ③ ENTRÉE — `f_comb` : la combinatoire · `sid`, `essai` : la stratégie et
      l'essai · `f_resultats` : le fichier provisoire qui vient d'être écrit, ou
      (depuis le 29-10-2026, C15) un dictionnaire id_version -> ligne, quand les
      versions ont été rejouées sous le barème du témoin.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts, vide si tout concorde ou s'il
      n'y a pas de témoin.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher `TEMOIN_RESULTATS_<STRATÉGIE>_<ESSAI>.csv` à côté
      de la combinatoire · ② absent : l'annoncer et rendre une liste vide ·
      ③ présent : comparer, version par version, opérations, réussite exacte et
      gain net, et signaler toute version manquante ou en trop.
    ⑦ UNITÉ — Euros ; pourcents.
    ⑧ POURQUOI — Relecture du 08-10-2026, défaut N1 : l'ordre des tests de sortie
      inversé dans le module de positions laissait le juge calibré, la fiche
      inchangée, et faisait passer la version tp 2 % / sl 1,5 % de 25 495,70 € à
      28 990,45 € sans alerte.
    ⑨ CE QUI CLOCHE — Un témoin absent ne protège rien : c'est annoncé à l'écran,
      pas refusé. Un témoin se fige sur décision de Jean-Luc ; une révision des
      cours passés par ABC fera aussi rougir la comparaison, ce qui est voulu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      le témoin de résultats : une copie figée des résultats d'un lancement jugé
        bon, rangée à côté de la combinatoire, qui sert de référence aux suivants.
    """
    f_tem = os.path.join(os.path.dirname(f_comb), "TEMOIN_RESULTATS_%s_%s.csv" % (sid, essai))
    if not os.path.exists(f_tem):
        print("AUCUN TÉMOIN DE RÉSULTATS (%s) : seuls les réglages de la fiche sont"
              " protégés par le calibrage." % os.path.basename(f_tem))
        return []
    champs = ("operations", "reussite_pourcents_exacte", "gain_net_euros")
    tem = {r["id_version"]: r for r in csv.DictReader(open(f_tem, encoding="utf-8-sig"))}
    # `f_resultats` : un fichier de résultats, OU un dictionnaire id_version -> ligne, quand la comparaison se fait
    # sous le barème du témoin et non sous celui des résultats écrits (C15, 29-10-2026).
    res = f_resultats if isinstance(f_resultats, dict) else \
        {r["id_version"]: r for r in csv.DictReader(open(f_resultats, encoding="utf-8"))}
    ecarts = ["%s absente du témoin" % k for k in sorted(set(res) - set(tem))]
    ecarts += ["%s absente des résultats" % k for k in sorted(set(tem) - set(res))]
    for k in sorted(set(res) & set(tem)):
        for c in champs:
            if res[k].get(c) != tem[k].get(c):
                ecarts.append("%s %s : %s au lieu de %s" % (k, c, res[k].get(c), tem[k].get(c)))
    print("TÉMOIN DE RÉSULTATS : %d versions comparées, %d écarts" % (len(tem), len(ecarts)))
    return ecarts


def main():
    """Contrôle, calibre, puis joue toutes les versions.

    ① RÔLE — Point d'entrée du programme.
    ② CONTEXTE D'APPEL — Le lancement, et lui seul.
    ③ ENTRÉE — La ligne de commande (voir l'en-tête).
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — UNE valeur : 0 ou 1, passée à la sortie du processus.
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Crée le fichier de résultats.
    ⑪ TERMINAISON — Rend la main ; une exception imprévue efface le fichier
      provisoire puis remonte.
      [sort: non]
    """
    positions, autre_cours, refus = lire_la_ligne_de_commande(sys.argv[1:])
    if refus:
        return arreter(refus + ". Rien n'est joué.")
    if len(positions) != 3:
        print(__doc__.split("①")[0])
        return 1
    base, f_comb, f_out = (os.path.abspath(a) for a in positions)
    if os.path.exists(f_out):
        return arreter("le fichier de résultats existe déjà : %s" % f_out)
    # LE FICHIER DE COURS, RELATIF À LA RACINE COMME POUR LE JUGE (`os.path.join(base, _autre)` dans son `main`) ;
    # son existence est exigée ici, avant le calibrage, pour que l'arrêt dise ce qui manque.
    if autre_cours is not None and not os.path.isfile(os.path.join(base, autre_cours)):
        return arreter("le fichier de cours de --cours= n'existe pas : %s" % os.path.join(base, autre_cours))

    versions = list(csv.DictReader(open(f_comb, encoding="utf-8-sig")))
    if not versions:
        return arreter("la combinatoire est vide")
    strats = {v["strategie"] for v in versions}
    essais = {v["essai"] for v in versions}
    if len(strats) != 1 or len(essais) != 1:
        return arreter("plusieurs stratégies ou essais dans la combinatoire : %s %s"
                       % (sorted(strats), sorted(essais)))
    ids = [v["id_version"] for v in versions]
    if len(set(ids)) != len(ids):
        return arreter("identifiants de version en double")
    annonces = {v["versions_dans_l_essai"] for v in versions}
    if annonces != {str(len(versions))}:
        return arreter("la combinatoire annonce %s versions et en porte %d"
                       % (sorted(annonces), len(versions)))
    vides = [v["id_version"] for v in versions if not codes(v["univers"])]
    if vides:
        # « , » passe la porte 0 et se joue avec zéro opération, sans alerte
        # (relecture du 08-10-2026, défaut N7).
        return arreter("univers vide pour %s" % vides[:5])
    doubles = [v["id_version"] for v in versions if len(set(codes(v["univers"]))) != len(codes(v["univers"]))]
    if doubles:
        # `jouer` joue un code autant de fois qu'il est écrit : « TTE,TTE » double
        # les opérations (relecture du 08-10-2026, défaut N4).
        return arreter("valeur écrite deux fois dans l'univers de %s" % doubles[:5])
    ident_v = [v for v in versions if (v.get("version_de_la_fiche") or "").strip()]
    if len(ident_v) != 1:
        return arreter("%d versions marquées identiques à la fiche" % len(ident_v))
    sid, essai = strats.pop(), essais.pop()

    ok, ligne_juge = calibrer_par_le_juge(base, sid, autre_cours)
    print("CALIBRAGE PAR LE JUGE SEUL : %s" % ("OK" if ok else "ÉCHEC"))
    if not ok or not ligne_juge:
        return arreter("le juge des stratégies ne se calibre pas, ou n'a pas joué la fiche")
    print("  le juge affiche : %s" % ligne_juge)

    sys.path.insert(0, os.path.join(base, "programmes"))
    import JUGE_DES_STRATEGIES as J
    if os.path.dirname(os.path.abspath(J.__file__)) != os.path.join(base, "programmes"):
        return arreter("le juge importé n'est pas celui du dépôt : %s" % J.__file__)
    mnemo = J.table_mnemoniques(J.trouver(base, "REFERENTIEL_VALEURS"))
    # LES COURS PASSENT PAR LE LECTEUR UNIQUE, COMME DANS `main` DU JUGE (A-577, étape 1, 27-10-2026) : ce
    # programme se compare au juge, il lit donc comme lui — sinon le juge affiche 89 opérations et ce
    # programme 100 sur la même fiche (C5E10-OBS-V1, mesuré le 27-10-2026). Deux lectures divergent (R-708).
    # `--cours=` : le fichier nommé, relatif à la racine, comme le juge (plan V7, bloc 5l ⑤) ; sinon le maître.
    f_cours_rel = (os.path.relpath(os.path.join(base, autre_cours), base) if autre_cours is not None
                   else os.path.relpath(J.fichiers_de_cours(base)[0], base))
    try:   # le juge refuse lui-même une lecture qui a écarté des lignes (`lire_par_le_lecteur`, 27-10-2026)
        cours, lecture = J.lire_par_le_lecteur(base, f_cours_rel, mnemo)
    except ValueError as e:
        if not str(e).startswith("le lecteur unique"):
            raise
        return arreter(str(e))
    # LE SIGNAL N'EST PLUS CHARGÉ ICI (A-542, 30-10-2026) : chaque fiche jouée le nomme, `jouer_une` le lit par
    # `signal_de_la_fiche` du juge, la seule lecture (R-708).
    mod_pos = J.charger_module(J.trouver(base, "MODULE_POSITIONS.py"), "pos")
    # LA FICHE EST LA DERNIÈRE LIGNE DE SON IDENTIFIANT (décision de Jean-Luc n°83 du 01-11-2026 à 12h33 : « La
    # dernière ligne ajoutée fait foi. Les précédentes restent comme historique. ») : le nom du registre et sa lecture
    # vivent au contrat (programmes/CONTRATS_DES_FICHIERS.py, chargé depuis le même dossier que le juge). Avant le
    # 05-11-2026, une fiche écrite deux fois arrêtait ce programme (« trouvée 2 fois au registre »).
    import CONTRATS_DES_FICHIERS as contrat
    fiche = contrat.fiches_du_registre(J.trouver(base, contrat.NOM_DU_REGISTRE_DES_STRATEGIES)).get(sid)
    if fiche is None:
        return arreter("fiche %s absente du registre" % sid)

    def jouer_une(f, bareme=None, ops_rendues=None, periode=None):
        """Fait passer une fiche par la porte 0 puis la joue.

        ① RÔLE — Un seul chemin de jeu pour la fiche, la version identique et
          toutes les versions.
        ② CONTEXTE D'APPEL — `main`, une fois par fiche à jouer.
        ③ ENTRÉE — `f` : une fiche, d'origine ou fusionnée · `bareme` : None pour le
          barème des trades vécus, sinon le nom d'un barème (celui du témoin, C15) ·
          `ops_rendues` : une liste où recopier les opérations jouées, ou None · `periode` : les bornes à
          jouer, ou None pour celles de la fiche (la fin calculée, bloc 5g, arrive par là).
        ④ CONDITIONS D'ENTRÉE — Les cours, le référentiel et les deux modules sont
          chargés par `main`.
        ⑤ SORTIE — DEUX valeurs : le résumé rendu par `resumer` du juge ; les bornes
          de la période rendues par la porte 0 (celles de la fiche, même quand `periode`
          en impose d'autres : `main` compare ces bornes d'une version à l'autre).
          [rend: 2]
        ⑥ TRAITEMENT — ① porte 0 · ② lire le signal que la fiche nomme, par
          `signal_de_la_fiche` du juge (A-542) · ③ `jouer` sur `periode`, ou à défaut
          sur la période de la fiche, avec CE signal · ④ refuser une valeur absente
          des cours · ⑤ résumer.
        ⑦ UNITÉ — Euros ; pourcents ; dates AAAA-MM-JJ.
        ⑧ POURQUOI — Le même appel que `main` du juge, ligne `ops, inconnus = jouer(...)`.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Aucun sur la fiche reçue. Charge le module de signal nommé au
          premier appel (le juge le garde ensuite en mémoire).
        ⑪ TERMINAISON — Rend la main, ou lève ValueError sur un refus — porte 0, ou
          signal nommé introuvable.
          [sort: non]
        ⑫ DÉFINITIONS
          la porte 0 : la fonction `porte_0` du juge, qui refuse une fiche incomplète.
        """
        ok0, manq, bornes = J.porte_0(f)
        if not ok0:
            raise ValueError("la porte 0 refuse : %s" % manq)
        mod_sig = J.signal_de_la_fiche(base, f)   # le signal que la fiche nomme, lu à un seul endroit (A-542)
        a_jouer = periode if periode is not None else bornes
        # REGARD UNIQUE (R-505 ③, mission REGARD du 12-11-2026) : aucune inscription ici, donc aucun reçu — une version
        # jouée dans la fenêtre du regard unique est REFUSÉE par `jouer` (RegardNonInscrit). Pas 7 (GitHub), hors mission.
        if bareme is None:
            ops, inconnus = J.jouer(f, cours, mnemo, mod_sig, mod_pos, periode=a_jouer, lecture=lecture)
        else:
            ops, inconnus = J.jouer(f, cours, mnemo, mod_sig, mod_pos, periode=a_jouer, lecture=lecture,
                                    bareme=bareme)
        if ops_rendues is not None:
            ops_rendues.extend(ops)
        if inconnus:
            raise ValueError("valeurs absentes des cours : %s" % inconnus)
        return J.resumer(ops), bornes

    ref, bornes = jouer_une(dict(fiche))
    if ref["n"] == 0:
        return arreter("la fiche elle-même ne produit aucune opération")
    texte_ref = "{} operations . {} % de reussite . {:+,.2f} EUR".format(ref["n"], ref["wr"], ref["net"])
    print("  ce programme : %s" % texte_ref)
    if texte_ref != ligne_juge:
        return arreter("ce programme et le juge seul ne rendent pas la même chose pour la fiche")
    r_id, _ = jouer_une(fusionner(fiche, ident_v[0]))
    if (r_id["n"], r_id.get("wr_exact"), r_id.get("net")) != (ref["n"], ref["wr_exact"], ref["net"]):
        return arreter("la version %s, identique à la fiche, ne retrouve pas la fiche"
                       % ident_v[0]["id_version"])
    print("  version identique %s : même résultat" % ident_v[0]["id_version"])

    # LA FIN DE LA PÉRIODE JOUÉE SE CALCULE (plan V7, bloc 5g, complément du 11-11-2026 à 20h17) : la plus tardive
    # qui laisse à chaque valeur l'horizon le plus long plus la séance d'achat, sans dépasser la fiche. La fiche
    # n'est pas modifiée ; la fin calculée vit dans la colonne `periode_fin` des résultats.
    h_max = max(int(v["horizon"]) for v in versions)
    dates = {}
    for m in sorted({c for v in versions for c in codes(v["univers"])}):
        cle = mnemo.get(m, J.cle_valeur(m))
        dates[m] = [b["date"] for b in cours.get(cle, [])]
    fin, limite = fin_utilisable(dates, bornes[0], bornes[1], h_max)
    if fin is None:
        return arreter("pas assez de cours après la période pour %s et l'horizon %d" % (limite, h_max))
    periode_jouee = (bornes[0], fin)
    try:
        recul_max, statut_recul, _ = lire_le_recul_maximum(base)
    except ValueError as e:
        return arreter(str(e))
    recul = recul_en_seances(dates, fin, bornes[1])
    print("RECUL DE LA FIN : %d séance(s) · au plus %d (%s, %s)" % (recul, recul_max, statut_recul, RECUL_MAXIMUM))
    if recul > recul_max:
        # UNE SEULE VALEUR QUI S'ARRÊTE TÔT NE RAMÈNE PAS EN SILENCE LA FIN DE TOUTES LES VERSIONS (D6, 11-11-2026)
        return arreter("la fin calculée recule de %d séances (au plus %d) : ramenée au %s par %s et l'horizon %d ; "
                       "rien n'est joué" % (recul, recul_max, fin, limite, h_max))
    print("PÉRIODE ÉCRITE DANS LA FICHE : %s -> %s · FIN CALCULÉE : %s%s" % (
        bornes[0], bornes[1], fin, " (inchangée)" if limite is None else
        " (ramenée par %s et l'horizon %d ; la fiche n'est pas modifiée)" % (limite, h_max)))
    # LA MARGE SE COMPTE VALEUR PAR VALEUR, ET SE RECOMPTE APRÈS LE CALCUL : compter les séances de toutes les
    # valeurs laissait passer un univers dont les cours s'arrêtaient trois séances après la période (relecture du
    # 08-10-2026, défaut N3). Ce recompte est le garde-fou du calcul : il ne peut rougir que si `fin_utilisable` se
    # trompe.
    marge = {m: sum(1 for d in ds if d > fin) for m, ds in dates.items()}
    plus_court = min(marge, key=marge.get)
    print("PÉRIODE JOUÉE : %s -> %s · cours : %s · marge la plus courte : %s, %d séances après la fin"
          " · horizon max %d" % (periode_jouee[0], periode_jouee[1], f_cours_rel, plus_court, marge[plus_court],
                                 h_max))
    if marge[plus_court] < h_max + 1:
        return arreter("pas assez de cours après la période pour %s et l'horizon %d"
                       % (plus_court, h_max))
    # LA FICHE REJOUÉE SUR LA PÉRIODE CALCULÉE : la version identique doit la retrouver plus bas, sur cette période-là.
    ref_jouee = ref if fin == bornes[1] else jouer_une(dict(fiche), periode=periode_jouee)[0]
    if fin != bornes[1]:
        # AUCUNE OPÉRATION EST UN RÉSULTAT, JAMAIS UN ARRÊT (D5, 11-11-2026) : `resumer` rend alors {"n": 0}, sans « wr ».
        print("  la fiche sur la période jouée : %s" % ("aucune opération" if not ref_jouee["n"] else
              "{} operations . {} % de reussite . {:+,.2f} EUR".format(ref_jouee["n"], ref_jouee["wr"],
                                                                     ref_jouee["net"])))
    # LA PARTIE DE RÉGLAGE (70 %) : coupée par le module de jugement, sur les séances des bornes de la FICHE, comme
    # `juger` le fera (D1, 11-11-2026). LA FRONTIÈRE VIENT DE `frontiere_de_la_fiche`, la seule fonction qui l'établit,
    # appelée aussi par le juge et par le tri (superviseur R-759 de la mission TRI, 12-11-2026) ; le calendrier est
    # celui que `main` du juge construit (`seances = {b["date"] for s in cours.values() for b in s}`).
    mod_jug = J.charger_module(J.trouver(base, "MODULE_JUGEMENT.py"), "jug")
    seances_lues = {b["date"] for s_ in cours.values() for b in s_}
    frontiere = mod_jug.frontiere_de_la_fiche(fiche, seances_lues, bornes)
    if frontiere is None:
        return arreter("aucune séance des cours lus dans les bornes de la fiche : pas de frontière 70/30")
    seances_fiche = {d for d in seances_lues if bornes[0] <= d <= bornes[1]}
    print("PARTIE DE RÉGLAGE : signaux avant la frontière %s, embargo déduit (coupure du module de jugement) ;"
          " SEULE cette partie est écrite dans les colonnes « _70 », les seules que le tri lit" % frontiere)

    # LES CHAMPS DU FICHIER DE RÉSULTATS VIVENT AU CONTRAT : le tri les lit aussi (programmes/TRIER_LES_VARIANTES.py,
    # 11-11-2026) ; un fichier lu par deux programmes se déclare une fois (instructions du projet, §7).
    champs = list(contrat.RESULTATS_DES_VERSIONS)
    # L'EMPREINTE DES SEULES SÉANCES JUSQU'À LA FIN DE LA FICHE (M2, 12-11-2026) : le maître grandit chaque soir.
    empreinte_cours = empreinte_des_cours_jusqu_a(os.path.join(base, f_cours_rel), bornes[1])
    # LE TÉMOIN SE COMPARE SOUS SON PROPRE BARÈME (C15, 29-10-2026) : chaque version est jouée deux fois quand le
    # témoin a été fait sous un autre barème que celui des résultats — sous le barème des verdicts pour les résultats
    # écrits, sous celui du témoin pour la comparaison — et l'écart entre les deux doit être EXACTEMENT la taxe
    # payée à l'achat (mêmes opérations ; un achat revendu le jour même ne paie pas la taxe). L'écart n'est la taxe
    # que si les deux barèmes ne diffèrent QUE par elle (courtage seul contre réel) : sinon, arrêt, et c'est voulu.
    b_tem = bareme_du_temoin(f_comb, sid, essai)
    # Les résultats se chiffrent sous le BARÈME DES VERDICTS (le défaut du juge, `MODULE_POSITIONS.BAREME_DES_VERDICTS`,
    # superviseur R-759 tour 2, D2) ; le témoin n'est rejoué à part que s'il a été fait sous un autre barème.
    b_res = J.bareme_des_verdicts(None, mod_pos)
    rejouer = b_tem is not None and b_tem != b_res
    vue_du_temoin, invariant_faux = {}, []
    if b_tem is not None:
        print("TÉMOIN FAIT SOUS LE BARÈME %s%s" % (b_tem, " : chaque version est aussi rejouée sous ce barème"
                                                   if rejouer else ""))
    provisoire = f_out + ".en_cours"
    cree = False  # on n'efface que ce qu'on a créé (relecture du 08-10-2026, N5)
    try:
        with open(provisoire, "x", encoding="utf-8", newline="") as s:
            cree = True
            w = csv.DictWriter(s, fieldnames=champs)
            w.writeheader()
            for i, v in enumerate(versions, 1):
                fusion = fusionner(fiche, v)
                ecarts = controler_fusion(J, fusion, v)
                if ecarts:
                    raise ValueError("fusion fausse pour %s : %s" % (v["id_version"], ecarts))
                ops_r = []
                r, b = jouer_une(fusion, None, ops_r, periode_jouee)
                if b != bornes:
                    raise ValueError("période différente pour %s : %s" % (v["id_version"], b))
                emb_v, r70 = partie_de_reglage(mod_jug, ops_r, seances_fiche, int(v["horizon"]), frontiere)
                if v is ident_v[0] and (r["n"], r.get("wr_exact"), r.get("net")) != (
                        ref_jouee["n"], ref_jouee.get("wr_exact"), ref_jouee.get("net")):
                    raise ValueError("la version %s, identique à la fiche, ne retrouve pas la fiche sur la période"
                                     " jouée" % v["id_version"])
                if rejouer:
                    ops_t = []
                    r_t, _ = jouer_une(fusion, b_tem, ops_t, periode_jouee)
                    vue_du_temoin[v["id_version"]] = {
                        "operations": str(r_t["n"]),
                        "reussite_pourcents_exacte": "%.6f" % r_t["wr_exact"] if r_t["n"] else "",
                        "gain_net_euros": "%.2f" % r_t["net"] if r_t["n"] else "0.00"}
                    cle_op = lambda o: (o["valeur"], o["date_signal"], o["date_sortie"], o["motif"], o["px"])
                    # la taxe payée sous un barème : achats non revendus le jour même (BOFiP, BOI-TCA-FIN-10-10, § 60)
                    taxe_de = lambda bar: sum(
                        mod_pos.cout_d_un_ordre(o["valeur"], o["date_entree"], "achat", 100000.0, bar)["taxe"]
                        for o in ops_r if o["date_entree"] != o["date_sortie"])
                    # le gain sous le barème du témoin moins le gain sous celui des résultats = ce que les résultats
                    # paient de taxe en plus (négatif si c'est le témoin qui la paie)
                    taxes = taxe_de(b_res) - taxe_de(b_tem)
                    ecart = sum(o["net"] for o in ops_t) - sum(o["net"] for o in ops_r)
                    if [cle_op(o) for o in ops_t] != [cle_op(o) for o in ops_r] or abs(ecart - taxes) > 0.01:
                        invariant_faux.append("%s : écart %.2f € pour %.2f € de taxe" % (v["id_version"], ecart, taxes))
                w.writerow({"id_version": v["id_version"], "strategie": sid, "essai": essai,
                            "versions_dans_l_essai": len(versions), "tp": v["tp"], "sl": v["sl"],
                            "horizon": v["horizon"], "univers": v["univers"],
                            "periode_debut": periode_jouee[0], "periode_fin": periode_jouee[1],
                            "operations": r["n"],
                            "reussite_pourcents_exacte": "%.6f" % r["wr_exact"] if r["n"] else "",
                            "gain_net_euros": "%.2f" % r["net"] if r["n"] else "0.00",
                            "bareme": b_res, "fin_ecrite_dans_la_fiche": bornes[1],
                            "cours_joues": f_cours_rel, "empreinte_des_cours": empreinte_cours,
                            "frontiere_70_30": frontiere, "embargo_seances": "" if emb_v is None else emb_v,
                            "operations_70": r70["n"],
                            "reussite_pourcents_exacte_70": "%.6f" % r70["wr_exact"] if r70["n"] else "",
                            "gain_net_euros_70": "%.2f" % r70["net"] if r70["n"] else "0.00"})
                if i % 250 == 0:
                    print("  %d / %d" % (i, len(versions)), flush=True)
        if invariant_faux:
            print("L'ÉCART ENTRE LES DEUX BARÈMES N'EST PAS LA TAXE (%d) :" % len(invariant_faux))
            for e in invariant_faux[:10]:
                print("  %s" % e)
            os.remove(provisoire)
            return arreter("l'écart au témoin n'est pas expliqué par la taxe : rien n'est écrit")
        ecarts = comparer_au_temoin(f_comb, sid, essai, vue_du_temoin if rejouer else provisoire)
        if ecarts:
            print("ÉCARTS AVEC LE TÉMOIN DE RÉSULTATS (%d) :" % len(ecarts))
            for e in ecarts[:10]:
                print("  %s" % e)
            os.remove(provisoire)
            return arreter("les résultats ne retrouvent pas le témoin : rien n'est écrit")
    except BaseException:
        if cree and os.path.exists(provisoire):
            os.remove(provisoire)
        raise
    os.replace(provisoire, f_out)
    print("ÉCRIT : %s · %d versions" % (f_out, len(versions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
