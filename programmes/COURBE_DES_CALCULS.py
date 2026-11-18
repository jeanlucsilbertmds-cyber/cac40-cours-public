#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COURBE_DES_CALCULS — Dim 15-11-2026 (Paris), étape « LU · lecteur unique » du plan V7, point ③ (BACKLOG A-713 ③).
PROPOSÉ, non validé. Simulation uniquement.

① RÔLE — Donner au juge des stratégies, pour un fichier de cours au COURS BRUT de Paris, la courbe qui sert aux
  calculs : chaque barre multipliée par le produit des facteurs des opérations sur titre POSTÉRIEURES à sa date
  (divisions, actions gratuites, droits, distributions d'actions d'une autre société ; jamais un dividende, POUR AUTANT
  QUE la liste de RECONSTRUIRE n'en contienne pas : la nature d'une opération n'est pas vérifiée ici), le volume
  divisé par ce produit. C'est R-108 ② : « La courbe qui sert aux calculs est corrigée de tout événement qui change le
  nombre ou la nature des actions […] ; un dividende […] ne se corrige jamais. » Le vrai cours reste ce que le lecteur
  unique rend (R-108 ① : « le vrai cours est toujours gardé ») : cette courbe est calculée À CÔTÉ, jamais écrite.
② CONTEXTE D'APPEL — `lire_par_le_lecteur` de programmes/JUGE_DES_STRATEGIES.py (le juge, et JOUER_LES_VERSIONS qui
  lit comme lui), une fois par lecture, par `courbe_si_le_fichier_est_brut`. Lancé seul, il mesure :
  python3 programmes/COURBE_DES_CALCULS.py <racine> [fichier des cours, relatif à la racine].
  Son épreuve : tests/EPREUVES_DE_LA_COURBE_DES_CALCULS_Dim_15-11-2026.py.
③ ENTRÉE — Le rendu de `LIRE_LES_COURS.lire` ; sous la racine, ce que lit `ASSEMBLER_LES_VINGT_ANS.operations` (par
  RECONSTRUIRE_L_HISTORIQUE_LONG : l'historique long réparé, l'extrait bnains, le fichier maître, les opérations
  déclarées) ; la déclaration CONTRATS_DES_FICHIERS.FICHIERS_DE_COURS_AU_COURS_BRUT.
④ CONDITIONS D'ENTRÉE — Voir chaque fonction. Pour tout fichier autre que le maître : les opérations se lisent sans
  défaut, et la nature MESURÉE du fichier s'accorde à sa déclaration (`garder_la_nature`). Pour un fichier déclaré au
  cours brut, en plus : deux noms d'opérations ne tombent pas sur un même mnémonique, et chaque barre d'une valeur
  connue de RECONSTRUIRE a un facteur connu. Sinon ValueError, et le juge ne juge rien (R-734 : un contrôle qui n'a pas
  pu tourner ne rend pas « bon »).
⑤ SORTIE — Voir chaque fonction. Lancé seul : 0 quand le fichier n'est pas déclaré au cours brut ou que la courbe se
  calcule ; 2 quand elle ne peut pas se calculer (R-734).
⑥ TRAITEMENT — `est_au_cours_brut` (la déclaration du fichier) · `lire_les_operations` (la liste unique des
  opérations, celle de RECONSTRUIRE par l'assemblage) · `operations_jugees` et `garder_la_nature` (la nature MESURÉE,
  confrontée à la déclaration) · `operations_par_mnemonique` (les opérations sous les mnémoniques du lecteur, et les
  valeurs que RECONSTRUIRE connaît) · `corriger` (la courbe) · `courbe_si_le_fichier_est_brut` (la porte du juge) ·
  `main` (la mesure, à la main).
⑦ UNITÉ — Des euros par titre et des titres, à l'échelle des actions d'aujourd'hui ; des rapports sans unité pour les
  facteurs.
⑧ POURQUOI — BACKLOG A-713 ③ : la courbe de R-108 ② n'existait dans aucun programme branché sur le juge ; sur le
  témoin des 20 ans, MICHELIN semble perdre 75,6 % le 16-06-2022 (division par quatre) et le juge le voyait. Le
  superviseur R-759 du 14-11-2026 (SUPERVISEUR_LU_TOUR7, verdict ARRÊTER ET SIMPLIFIER) a demandé de repartir de main
  et de « brancher la courbe sur le juge : ce maillon manque partout », la branche sauvegarde/v7-LU-courbe (708 lignes
  de courbe, 1 108 d'épreuve, sept tours) restant en sauvegarde. Ce module ne garde de cette branche que le calcul ;
  les contrôles de la courbe (sauts sur la courbe, A-713 ④ ; ancre du jour de l'opération, A-713 ⑥) et la nature
  ligne par ligne y restent, au BACKLOG. Les facteurs viennent de RECONSTRUIRE, jamais recopiés (R-708 : deux
  implémentations d'une même chose divergent toujours). « Jamais un dividende » est une promesse de RECONSTRUIRE, pas
  de ce module : la nature des opérations y est un texte libre, que ce module ne lit pas (Cowork, RELU de 4be799c3,
  L-2 ; superviseur R-759 de LU2, tour 3, § 3 : une liste de natures admises écrite ici est à ne pas faire).
⑨ CE QUI CLOCHE — Les opérations des sociétés sorties de l'indice, et celles d'ArcelorMittal (MT), ne sont pas
  connues de RECONSTRUIRE (son univers : les 39 valeurs de l'historique long réparé) : depuis le tour 2 (15-11-2026),
  ces valeurs sont NOMMÉES dans la lecture (« valeurs_aux_operations_inconnues »), leurs barres gardées au facteur 1 ;
  depuis le 18-11-2026, le juge lit cette clé et REFUSE une fiche dont l'univers en contient une sur la période jugée
  (`JUGE_DES_STRATEGIES.refus_des_operations_inconnues`, D4 de LU2, A-895 ⑮). Une division d'une société sortie reste
  une fausse chute de la courbe : seul le refus empêche le juge de la voir. Mesuré par `main` le 15-11-2026 sur l'essai de fusion avec la
  branche travail-QE2 (qui fait connaître les sociétés sorties au lecteur) : 22 sauts de plus de 25 % restent sur les
  valeurs sans opération connue, dont des divisions évidentes (ALO 2008-07-07 ×0,5127 ; UG 2001-07-02 ×0,1678, la
  division de Peugeot rangée sous STELLANTIS, A-713 ⑤ ; NOKIA 2000-04-11 ×0,2324 ; VK 2006-07-17 ×0,1917) ; aucune
  fiche du registre n'a aujourd'hui de société sortie dans son univers. · La déclaration
  FICHIERS_DE_COURS_AU_COURS_BRUT est écrite à la main : un témoin figé demain doit y être ajouté à son gel
  (l'assemblage ne le fait pas) — BACKLOG. · Le rangement des opérations sous les mnémoniques (deux noms sous un même
  mnémonique : refus) est écrit aussi, en ligne, dans `assembler` de programmes/ASSEMBLER_LES_VINGT_ANS.py : deux
  écritures (R-708) — BACKLOG. · Sur les lignes « ramené au brut » (historique long ÷ facteurs), la courbe redevient
  l'historique long : elle n'est pas indépendante des facteurs qui l'ont produite. · LA GARDE DE NATURE ne juge que
  les GRANDES opérations (|facteur − 1| au-delà du seuil de R-104) : un fichier sans aucune dans ses dates
  (INDÉCIDABLE : le maître, la référence Google, une copie partielle du témoin) passe sous les deux règles, et ses
  petites opérations (droits, actions gratuites) ne sont pas corrigées, sans que rien le voie ; un krach de plus que le
  seuil le jour d'une grande opération ferait lire « vue » sur un fichier corrigé. · Le maître est exempté de la
  garde (le fichier par défaut du lecteur, LIRE_LES_COURS.FICHIER_DES_COURS) : quand il manque,
  `fichiers_de_cours` du juge se rabat sur la référence Google, qui est alors mesurée (INDÉCIDABLE, elle passe). ·
  La garde ne répond pas à une division FUTURE d'une valeur du CAC 40 : ABC donne des cours bruts, et la fausse chute
  entrera au maître (BACKLOG A-478). · La courbe d'un témoin figé suit la liste des opérations du jour, qui peut changer
  (le maître grandit) : reproductible ou non, à décider (BACKLOG). · TROIS FACTEURS DE RECONSTRUIRE SONT MESURÉS ET
  NON DOCUMENTÉS (nature « ajustement caché de Yahoo, facteur MESURÉ (non documenté) », relevés par le superviseur de LU2,
  tour 3) : EIFFAGE 2001-07-02 ×0,9 ; KERING 2018-05-14 ×0,9294 ; SANOFI 2022-05-06 ×0,9946. La courbe les applique ;
  si l'un était un dividende, elle le corrigerait à tort. Leur nature est à prouver par une source datée (BACKLOG).
⑩ EFFET — Lit des fichiers ; change le dossier courant le temps de lire les opérations et le rétablit. N'écrit rien.
  Lancé seul, affiche. Au premier besoin, charge ASSEMBLER_LES_VINGT_ANS par son chemin, sous un nom propre à ce
  module ; l'assemblage, à son chargement, insère son dossier en tête de `sys.path` et importe
  CONTROLER_L_HISTORIQUE_LONG, RECONSTRUIRE_L_HISTORIQUE_LONG et CONTRATS_DES_FICHIERS sous leurs noms, pour tout le
  processus. Rien de cela pour le maître.
⑪ TERMINAISON — Rend la main ; lancé seul, sort par sys.exit avec le code dit en ⑤. Aucun de mes appels ne peut ne
  pas revenir : chaque étape parcourt un nombre fini de lignes, sans réseau.
  [sort: oui]
"""
import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
_ASSEMBLER = []   # le module ASSEMBLER_LES_VINGT_ANS, chargé au premier besoin (jamais à l'import de ce module)


def _assembler():
    """Rend le module ASSEMBLER_LES_VINGT_ANS de ce dossier, chargé une fois.

    ① RÔLE — Donner la seule lecture des opérations (`operations`), la seule boucle de continuité
      (`confronter_aux_operations`), le seuil de R-104 (`seuil_de_variation`) et, par son module R, `facteur_apres` —
      sans rien charger tant qu'aucun fichier autre que le maître n'est lu.
    ② CONTEXTE D'APPEL — `lire_les_operations`, `operations_jugees`, `courbe_si_le_fichier_est_brut`, `main` ; l'épreuve.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — programmes/ASSEMBLER_LES_VINGT_ANS.py est à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, par le chemin, sous le nom « assembler_courbe_des_calculs », au premier appel ; la liste
      _ASSEMBLER garde le module.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : l'assemblage a produit le témoin avec ces fonctions ; la courbe et sa garde les reprennent au
      lieu d'en écrire de secondes (superviseur R-759 de LU2, 15-11-2026, D3 amendement 1). Jusqu'au tour 1, ce module
      refaisait l'enchaînement de `operations` (LU2-4) : il l'appelle désormais.
    ⑨ CE QUI CLOCHE — L'assemblage importe CONTROLER_L_HISTORIQUE_LONG et RECONSTRUIRE sous leurs noms : si un autre
      dossier les a déjà mis dans `sys.modules`, ce sont ceux-là qui servent (déclaré au ⑩ du programme).
    ⑩ EFFET — Exécute l'assemblage (ses déclarations ; son `main` n'est pas appelé).
    ⑪ TERMINAISON — Rend la main ou lève l'erreur de chargement.
      [sort: non]
    """
    if not _ASSEMBLER:
        spec = importlib.util.spec_from_file_location("assembler_courbe_des_calculs",
                                                      os.path.join(ICI, "ASSEMBLER_LES_VINGT_ANS.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _ASSEMBLER.append(m)
    return _ASSEMBLER[0]


def chemin_declare(racine, fichier):
    """Rend le chemin d'un fichier de cours tel que le contrat l'écrit : depuis la racine, séparé par « / ».

    ① RÔLE — Comparer un fichier lu à la déclaration du contrat, quelle que soit l'écriture du chemin donné.
    ② CONTEXTE D'APPEL — `est_au_cours_brut`, `courbe_si_le_fichier_est_brut` (l'exemption du maître).
    ③ ENTRÉE — `racine` : la racine du dépôt · `fichier` : le chemin du fichier de cours, relatif à la racine ou absolu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin relatif, avec « / ». Exemple : « ./temoins/X.csv » rend « temoins/X.csv ».
      [rend: 1]
    ⑥ TRAITEMENT — `os.path.relpath` depuis la racine, séparateurs remplacés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La même écriture que `LIRE_LES_COURS.lire` pour FICHIERS_DE_COURS_FIGES (sa ligne « chemin = … »), pour
      que les deux déclarations d'un même fichier se lisent de la même façon.
    ⑨ CE QUI CLOCHE — L'expression est écrite aussi dans `LIRE_LES_COURS.lire`, qui ne la rend pas : deux écritures
      (R-708) — BACKLOG.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return os.path.relpath(os.path.join(racine, fichier), racine).replace(os.sep, "/")


def est_au_cours_brut(contrats, racine, fichier):
    """Dit si un fichier de cours est déclaré au cours brut de Paris.

    ① RÔLE — La nature DÉCLARÉE d'un fichier : elle décide si le juge calcule sur la courbe corrigée.
    ② CONTEXTE D'APPEL — `courbe_si_le_fichier_est_brut` ; `main`.
    ③ ENTRÉE — `contrats` : le module CONTRATS_DES_FICHIERS que le lecteur a chargé (`LIRE_LES_COURS.CONTRATS`) ·
      `racine` · `fichier` : le fichier de cours lu.
    ④ CONDITIONS D'ENTRÉE — Le contrat définit FICHIERS_DE_COURS_AU_COURS_BRUT ; sinon AttributeError (une déclaration
      absente n'est pas « aucun fichier brut » : elle arrête).
    ⑤ SORTIE — UNE valeur : vrai si le chemin du fichier est dans la déclaration.
      [rend: 1]
    ⑥ TRAITEMENT — `chemin_declare`, puis l'appartenance.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le témoin des 20 ans est au cours brut PAR CONSTRUCTION (`assembler` ramène au brut les lignes
      « google » qu'une opération postérieure touche), alors que le maître et la référence Google portent des lignes
      déjà corrigées par Google, auxquelles appliquer les facteurs une seconde fois fabriquerait une marche (AIR LIQUIDE
      2024-06-10 au maître : relecteur LU tour 1, B2). La déclaration est CONFRONTÉE à la mesure par `garder_la_nature`.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme (déclaration écrite à la main).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève AttributeError.
      [sort: non]
    """
    return chemin_declare(racine, fichier) in contrats.FICHIERS_DE_COURS_AU_COURS_BRUT


def lire_les_operations(racine):
    """Rend les valeurs que RECONSTRUIRE connaît et leurs opérations sur titre, par les noms de l'historique long.

    ① RÔLE — La liste unique des opérations (R-708), lue par la fonction qui a servi à produire le témoin.
    ② CONTEXTE D'APPEL — `courbe_si_le_fichier_est_brut` ; `main` ; l'épreuve.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Celles de `ASSEMBLER_LES_VINGT_ANS.operations` (historique long et bnains lisibles sans
      défaut, opérations déclarées présentes) ; sinon ValueError ou OSError.
    ⑤ SORTIE — DEUX valeurs : ① l'ensemble des noms de l'historique long réparé (l'UNIVERS de RECONSTRUIRE : une valeur
      de cet ensemble sans opération n'a AUCUNE opération ; une valeur hors de lui a des opérations INCONNUES) — 39 noms
      mesurés le 15-11-2026 ; ② {nom : liste des opérations (date ISO, facteur ou None, nature, source, …)}, 34 noms.
      [rend: 2]
    ⑥ TRAITEMENT — Changer de dossier vers la racine (les chemins de l'assemblage sont relatifs) ; `operations` ; retour
      au dossier d'origine, même en cas d'erreur.
    ⑦ UNITÉ — Des rapports sans unité pour les facteurs.
    ⑧ POURQUOI — Superviseur R-759 de LU2 (15-11-2026, D4) : « opérations inconnues » n'est pas « aucune opération » ;
      seul l'univers de RECONSTRUIRE (l'historique long) les distingue, pas les clés de sa liste d'opérations.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers ; change le dossier courant et le rétablit.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    A = _assembler()
    avant = os.getcwd()
    os.chdir(racine)
    try:
        fichier, ops = A.operations(racine)
    finally:
        os.chdir(avant)
    return set(fichier), ops


def operations_jugees(cours, ops, table, norm):
    """Mesure, sur une lecture, les grandes opérations vues et non vues au jour dit.

    ① RÔLE — La nature MESURÉE d'un fichier de cours : au cours brut, une grande opération (division, regroupement) se
      voit au jour dit ; dans un fichier corrigé, elle ne se voit pas.
    ② CONTEXTE D'APPEL — `garder_la_nature` ; `main` ; l'épreuve.
    ③ ENTRÉE — `cours` : le rendu de `LIRE_LES_COURS.lire` · `ops` : le second rendu de `lire_les_operations` (par
      noms) · `table`, `norm` : la table des écritures du lecteur et sa normalisation.
    ④ CONDITIONS D'ENTRÉE — Clôtures lisibles et positives (le juge les lit déjà en nombres).
    ⑤ SORTIE — DEUX valeurs : la liste des grandes opérations VUES et celle des NON VUES, telles que
      `ASSEMBLER_LES_VINGT_ANS.confronter_aux_operations` les rend (son deuxième et son troisième rendu). Mesuré le
      15-11-2026 : témoin des 20 ans, 33 et 0 ; historique long réparé, 0 et 33 ; maître et référence Google, 0 et 0.
      [rend: 2]
    ⑥ TRAITEMENT — Les barres gardées par le lecteur, remises en lignes de huit textes (valeur, date ISO, cinq champs,
      source) ; le seuil de R-104 lu par `seuil_de_variation` de l'assemblage ; `confronter_aux_operations`.
    ⑦ UNITÉ — Des opérations.
    ⑧ POURQUOI — Superviseur R-759 de LU2 (15-11-2026, D3 amendement 1) : le décompte vient de la boucle de
      l'assemblage, jamais d'une seconde (R-708). Les opérations passent par les noms de l'historique long, comme dans
      `signaler` de l'assemblage.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme (INDÉCIDABLE, krach le jour d'une opération).
    ⑩ EFFET — Exécute la lecture du seuil (CONTROLER_LES_COURS).
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    A = _assembler()
    iso = lambda d: d.isoformat() if hasattr(d, "isoformat") else str(d)
    lignes = [[l.get("valeur", m), iso(d), l["open"], l["high"], l["low"], l["close"], l["volume"], l.get("source", "")]
              for m, b in cours["barres"].items() for d, l in b.items()]
    _, vues, non_vues = A.confronter_aux_operations(lignes, ops, A.seuil_de_variation(), table, norm)
    return vues, non_vues


def garder_la_nature(declare_brut, vues, non_vues, fichier):
    """Refuse un fichier dont la nature mesurée contredit sa déclaration.

    ① RÔLE — La garde de nature : la courbe ne s'applique qu'à un fichier au cours brut, et un fichier au cours brut
      n'est jamais lu au brut en silence.
    ② CONTEXTE D'APPEL — `courbe_si_le_fichier_est_brut` ; l'épreuve.
    ③ ENTRÉE — `declare_brut` : `est_au_cours_brut` · `vues`, `non_vues` : `operations_jugees` · `fichier` : pour le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien : rend la main quand la nature s'accorde ; LÈVE ValueError sinon.
      [rend: rien]
    ⑥ TRAITEMENT — Deux règles. ① Un fichier DÉCLARÉ au cours brut n'a AUCUNE grande opération non vue : sinon il porte
      déjà des facteurs, et la courbe les appliquerait une seconde fois. ② Un fichier NON déclaré n'a AUCUNE grande
      opération vue : sinon il est au brut, et le juge verrait ses divisions comme des chutes. Un fichier sans grande
      opération dans ses dates passe sous les deux règles.
    ⑦ UNITÉ — Des opérations.
    ⑧ POURQUOI — Relecteur LU2 tour 1 (15-11-2026, D3) : une copie du témoin sous un autre nom était lue au brut, sans
      un mot (40 sauts sur la courbe, comme au brut). Superviseur R-759 de LU2 (D3) : deux règles, sans les quatre
      états proposés ; une PROPRIÉTÉ — renommer le fichier ne change pas l'avis de la garde. Le mot de la colonne
      source ne dit pas la nature : l'historique long, corrigé, porte 7 205 lignes « bnains » (mesuré le 15-11-2026).
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme (INDÉCIDABLE passe ; krach le jour d'une opération).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    if declare_brut and non_vues:
        raise ValueError(f"la courbe des calculs : {fichier} est déclaré au cours brut, mais {len(non_vues)} grande(s) "
                         f"opération(s) n'y sont pas vues au jour dit (le fichier porte déjà les facteurs), dont "
                         + ", ".join(f"{k} {x}" for k, x, *_ in non_vues[:3]) + " : rien n'est jugé")
    if not declare_brut and vues:
        raise ValueError(f"la courbe des calculs : {fichier} n'est pas déclaré au cours brut "
                         f"(CONTRATS.FICHIERS_DE_COURS_AU_COURS_BRUT), mais {len(vues)} grande(s) opération(s) y sont "
                         f"vues au jour dit (le fichier est au brut), dont "
                         + ", ".join(f"{k} {x}" for k, x, *_ in vues[:3]) + " : rien n'est jugé")


def operations_par_mnemonique(table, norm, connus, ops):
    """Range les opérations et l'univers de RECONSTRUIRE sous les mnémoniques du lecteur unique.

    ① RÔLE — Passer de la clé de RECONSTRUIRE (le nom de l'historique long) à celle du lecteur : le mnémonique.
    ② CONTEXTE D'APPEL — `courbe_si_le_fichier_est_brut` ; `main` ; l'épreuve.
    ③ ENTRÉE — `table` : nom normalisé → mnémonique (`LIRE_LES_COURS.table_des_ecritures`, son premier rendu) ·
      `norm` : `LIRE_LES_COURS.COMMUN.norm_valeur` · `connus`, `ops` : les deux rendus de `lire_les_operations`.
    ④ CONDITIONS D'ENTRÉE — CHAQUE nom de l'univers de RECONSTRUIRE et de sa liste d'opérations a un mnémonique ; deux
      noms d'opérations ne tombent pas sur un même mnémonique ; sinon ValueError « la courbe des calculs : … ».
    ⑤ SORTIE — DEUX valeurs : ① {mnémonique : liste des opérations} ; ② l'ensemble des mnémoniques que RECONSTRUIRE
      connaît (les noms de `connus` qui ont un mnémonique). Exemple mesuré le 15-11-2026 : MICHELIN porte l'opération
      du 2022-06-16 au facteur 0,25 ; MT n'est pas dans ②.
      [rend: 2]
    ⑥ TRAITEMENT — ① la totalité : un nom sans mnémonique arrête · ② ranger chaque nom sous `table[norm(nom)]`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux noms sous un même mnémonique compteraient les facteurs deux fois : c'est un arrêt (le même refus
      que `assembler`). Jusqu'au tour 3, un nom sans mnémonique était LAISSÉ : ses opérations disparaissaient en silence
      (Cowork, RELU de 4be799c3, N-1 : CARREFOUR renommé, sa courbe gardait le brut) ; superviseur R-759 de LU2, tour 3,
      § 2 ① : « la totalité ». Mesuré le 15-11-2026 : 39 noms d'univers et 34 noms d'opérations, 0 sans mnémonique.
    ⑨ CE QUI CLOCHE — Le rangement est écrit aussi, en ligne, dans `assembler` (R-708) — BACKLOG.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    sans = sorted(v for v in set(connus) | set(ops) if table.get(norm(v)) is None)
    if sans:
        raise ValueError(f"la courbe des calculs : {len(sans)} nom(s) de l'univers de RECONSTRUIRE sans mnémonique au "
                         f"lecteur, dont {sans[:5]} : leurs opérations seraient perdues en silence ; rien n'est jugé")
    par_m, de = {}, {}
    for v, liste in ops.items():
        m = table[norm(v)]
        if m in de:
            raise ValueError(f"la courbe des calculs : les noms {de[m]!r} et {v!r} tombent sur le même mnémonique {m} : "
                             f"facteurs comptés deux fois ; rien n'est jugé")
        de[m] = v
        par_m[m] = list(liste)
    return par_m, {table[norm(v)] for v in connus}


def corriger(barres, ops, connus, facteur_apres):
    """Rend la courbe corrigée de chaque valeur, à la forme des barres du lecteur, et les valeurs aux opérations inconnues.

    ① RÔLE — R-108 ② : la courbe qui sert aux calculs, à côté du vrai cours.
    ② CONTEXTE D'APPEL — `courbe_si_le_fichier_est_brut` ; `main` ; l'épreuve.
    ③ ENTRÉE — `barres` : mnémonique → {date : ligne lue (textes)}, le « barres » de `LIRE_LES_COURS.lire`, NON
      modifié · `ops`, `connus` : les deux rendus de `operations_par_mnemonique` · `facteur_apres` :
      RECONSTRUIRE.facteur_apres (le produit des facteurs des opérations de date STRICTEMENT postérieure à la date
      donnée, None si l'un est inconnu).
    ④ CONDITIONS D'ENTRÉE — Les cinq champs de chaque barre se lisent en nombres. Chaque barre d'une valeur CONNUE a un
      facteur connu ; sinon ValueError, qui compte et nomme les barres sans facteur.
    ⑤ SORTIE — DEUX valeurs : ① mnémonique → {date : ligne}, chaque ligne une COPIE de la ligne lue, ses cinq champs
      remplacés par le texte (`repr`) du nombre corrigé : les quatre prix × p, volume ÷ p ; même nombre de barres, mêmes
      dates ; ② la liste triée des mnémoniques HORS de `connus` (opérations INCONNUES) : leurs barres sont copiées au
      facteur 1, gardées et nommées, jamais retirées. Exemple réel (témoin des 20 ans) : MICHELIN 2022-06-15, clôture
      111,45 et p = 0,25 → 27,8625 ; le 2022-06-16 (jour de la division, déjà ex-opération), 27,22 et p = 1 ; MT
      (ArcelorMittal) dans ②.
      [rend: 2]
    ⑥ TRAITEMENT — Pour chaque barre du jour d d'une valeur connue : p = facteur_apres(ops[m], d ISO) ; une valeur connue
      sans opération a p = 1 ; p None → la barre est comptée ; à la fin, s'il y en a, LÈVE. Une valeur inconnue : p = 1,
      et son mnémonique dans ②.
    ⑦ UNITÉ — Euros par titre et titres, à l'échelle des actions d'aujourd'hui ; p sans unité.
    ⑧ POURQUOI — R-108 ② et son exemple : « Michelin, 16-06-2022 […] les cours d'avant sont divisés par 4, les volumes
      multipliés par 4. » Une barre au facteur inconnu n'est ni gardée telle quelle ni retirée en silence : elle arrête
      (R-109 ; règle la plus stricte). Une VALEUR aux opérations inconnues n'arrête pas tout le fichier : le refus vit
      là où l'univers de la fiche est lu (superviseur R-759 de LU2, D4 : IND-001-RETEST, qui ne lit aucune société
      sortie, serait bloqué à tort), au lot QE2 après sa fusion ; ici, elle est NOMMÉE, ses barres gardées (même
      superviseur, première lecture de l'ambiguïté « gardées ou retirées »).
    ⑨ CE QUI CLOCHE — Le second rendu est lu par le juge depuis le 18-11-2026 (`lire_par_le_lecteur`, puis
      `refus_des_operations_inconnues` ; voir le ⑨ du programme). · Le texte d'un nombre
      corrigé est `repr(float)` : il n'est relu qu'en nombre par le juge.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    out, inconnus, sans_operations_connues = {}, [], []
    for m, b in barres.items():
        if m not in connus:
            sans_operations_connues.append(m)
        liste = ops.get(m, [])
        c = out[m] = {}
        for d, ligne in b.items():
            p = facteur_apres(liste, d.isoformat() if hasattr(d, "isoformat") else str(d)) if m in connus else 1.0
            if p is None:
                inconnus.append((m, d))
                continue
            x = dict(ligne)
            for k in ("open", "high", "low", "close"):
                x[k] = repr(float(ligne[k]) * p)
            x["volume"] = repr(float(ligne["volume"]) / p)
            c[d] = x
    if inconnus:
        inconnus.sort()
        raise ValueError(f"la courbe des calculs : {len(inconnus)} barre(s) au facteur inconnu (RECONSTRUIRE), dont "
                         + ", ".join(f"{m} {d}" for m, d in inconnus[:5]) + " : rien n'est jugé")
    return out, sorted(sans_operations_connues)


def courbe_si_le_fichier_est_brut(racine, lecteur, cours):
    """Rend la lecture à juger : la courbe corrigée pour un fichier au cours brut, la lecture telle quelle sinon.

    ① RÔLE — La porte du juge vers la courbe de R-108 ②, et la garde de nature de tout fichier de cours autre que le
      maître.
    ② CONTEXTE D'APPEL — `lire_par_le_lecteur` de programmes/JUGE_DES_STRATEGIES.py, juste après `lecteur.lire` — la
      porte unique de ses six appelants (le juge, JOUER_LES_VERSIONS, JUGER_UNE_FICHE, TRIER_LES_VARIANTES,
      DETECTER_LES_SIGNAUX_GITHUB, TENIR_LES_POSITIONS).
    ③ ENTRÉE — `racine` : la racine du dépôt · `lecteur` : le module LIRE_LES_COURS chargé par l'appelant · `cours` :
      le rendu de `lecteur.lire`.
    ④ CONDITIONS D'ENTRÉE — Celles de `est_au_cours_brut` ; pour un fichier autre que le maître, celles de
      `lire_les_operations`, `operations_jugees` et `garder_la_nature` ; pour un fichier déclaré, celles de
      `operations_par_mnemonique` et de `corriger`.
    ⑤ SORTIE — UNE valeur : pour le maître et pour un fichier non déclaré qui passe la garde, `cours` lui-même (le même
      objet : rien ne change pour le circuit du soir et le golden) ; pour un fichier déclaré, une copie de `cours` dont
      la clé « barres » est remplacée par la courbe, et qui porte en plus « valeurs_aux_operations_inconnues » ;
      `cours` n'est pas modifié.
      [rend: 1]
    ⑥ TRAITEMENT — ① le maître (le fichier par défaut du lecteur, `lecteur.FICHIER_DES_COURS`) : rendu tel quel, sans
      rien charger · ② sinon : la déclaration, les opérations (une erreur de lecture devient ValueError « la courbe des
      calculs : les opérations ne se lisent pas … »), la mesure, la garde · ③ non déclaré : rendu tel quel ·
      ④ déclaré : les opérations sous les mnémoniques (la totalité), la courbe, la copie · ⑤ la courbe se mesure
      CORRIGÉE : `garder_la_nature` en règle 2 sur sa propre sortie — une grande opération encore vue arrête.
    ⑦ UNITÉ — Voir `corriger`.
    ⑧ POURQUOI — Une seule porte, au seul endroit où les six appelants lisent les cours : la garde placée dans deux
      `main` en aurait oublié deux (superviseur R-759 de LU2, D3 : « une garde dans deux `main` sur quatre portes,
      c'est une énumération »). Le maître est exempté par son RÔLE (le fichier par défaut du lecteur), pas par son nom :
      le circuit du soir ne charge ni l'assemblage ni l'historique long. Appelée AVANT les refus de
      `lire_par_le_lecteur` : elle garde chaque barre et chaque date, si bien que les comptes du lecteur ne changent pas.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme (INDÉCIDABLE ; repli sur la référence Google quand le maître manque ;
      sociétés sorties). · Le contrôle de sortie ⑤ ne voit que les GRANDES opérations : une valeur qui perdrait
      seulement ses droits ou ses actions gratuites (moins de 25 %) passerait (le cas INDÉCIDABLE ; BACKLOG N-2 / LU2-8).
    ⑩ EFFET — Celui de `lire_les_operations` pour tout fichier autre que le maître ; aucun pour le maître.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError dont le message commence par « la courbe des calculs », ou
      AttributeError si le contrat ne déclare pas FICHIERS_DE_COURS_AU_COURS_BRUT.
      [sort: non]
    """
    if chemin_declare(racine, cours["fichier"]) == chemin_declare(racine, lecteur.FICHIER_DES_COURS):
        return cours
    brut = est_au_cours_brut(lecteur.CONTRATS, racine, cours["fichier"])
    try:
        connus, ops = lire_les_operations(racine)
    except (OSError, ValueError) as e:
        raise ValueError(f"la courbe des calculs : les opérations ne se lisent pas ({type(e).__name__} : {e}) ; un "
                         f"fichier autre que le maître ne se juge pas sans elles") from e
    table, _ = lecteur.table_des_ecritures(racine)
    norm = lecteur.COMMUN.norm_valeur
    garder_la_nature(brut, *operations_jugees(cours, ops, table, norm), cours["fichier"])
    if not brut:
        return cours
    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)
    x = dict(cours)
    x["barres"], x["valeurs_aux_operations_inconnues"] = corriger(cours["barres"], par_m, connus_m,
                                                                   _assembler().R.facteur_apres)
    # LA COURBE SE MESURE CORRIGÉE (superviseur R-759 de LU2, tour 3, § 2 ②) : la règle 2 de la garde appliquée à sa
    # propre sortie — une grande opération encore VUE sur la courbe est une valeur que la courbe n'a pas corrigée
    garder_la_nature(False, *operations_jugees(x, ops, table, norm), f"la courbe corrigée de {cours['fichier']}")
    return x


def main(argv):
    """Lit un fichier de cours, mesure sa nature, calcule sa courbe s'il est au cours brut, et mesure les sauts.

    ① RÔLE — La mesure, à la main, de ce que la courbe change pour le juge : le chiffre du chemin critique du point ③
      (les fausses chutes visibles du juge), et la nature mesurée du fichier.
    ② CONTEXTE D'APPEL — Le bloc final. Exemple :
      python3 programmes/COURBE_DES_CALCULS.py . temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv
    ③ ENTRÉE — `argv` : la racine, et le fichier des cours relatif à la racine (par défaut celui du lecteur).
    ④ CONDITIONS D'ENTRÉE — Celles de `LIRE_LES_COURS.lire` et de `lire_les_operations`.
    ⑤ SORTIE — UNE valeur : le code de sortie — 0 quand la mesure a tourné (c'est une mesure, pas un contrôle : elle ne
      refuse rien, elle DIT si la garde refuserait), 2 quand la ligne de commande est fausse ou que la lecture ou la
      courbe n'a pas pu se faire (R-734).
      [rend: 1]
    ⑥ TRAITEMENT — Lire ; la déclaration ; les opérations ; la mesure (`operations_jugees`) et ce que dirait la garde ;
      si le fichier est déclaré, la courbe (`operations_par_mnemonique` puis `corriger`) ; puis, pour chaque couple de
      barres d'une même valeur à deux SÉANCES CONSÉCUTIVES du calendrier, compter les variations de clôture au-delà du
      seuil de R-104, sur le cours brut et sur la courbe, en séparant les valeurs aux opérations connues des autres ;
      afficher chaque saut qui reste sur la courbe.
    ⑦ UNITÉ — Des paires de séances ; des rapports ; des opérations.
    ⑧ POURQUOI — Règle d'arrêt ① du superviseur R-759 du 14-11-2026 (SUPERVISEUR_LU_TOUR7) : « chaque tour nomme le
      chiffre du chemin critique qu'il fait bouger, mesuré avant et après sur le témoin installé ». Ce qui se mesure ne
      s'écrit pas à la main (R-728).
    ⑨ CE QUI CLOCHE — Un saut qui reste n'est pas une erreur prouvée ; « vrai mouvement ou division » ne se tranche que
      par une source datée (BACKLOG A-807, LU2-2), jamais par un rapport voisin d'une fraction (superviseur R-759 de
      LU2, D2 : les sept sauts restants sont tous à moins de 1,4 % d'une fraction simple). · Ce n'est PAS le contrôle
      des sauts d'A-713 ④. · Le maître est lu ici, mesure comprise (la porte, elle, l'exempte).
    ⑩ EFFET — Lit des fichiers. Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : COURBE_DES_CALCULS.py <racine> [fichier des cours, relatif à la racine]")
        return 2
    racine = argv[0]
    try:   # R-734 : UNE enveloppe ; tout échec rend 2, jamais 0
        spec = importlib.util.spec_from_file_location("lire_les_cours_courbe_des_calculs",
                                                      os.path.join(ICI, "LIRE_LES_COURS.py"))
        L = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(L)
        cours = L.lire(racine, argv[1]) if len(argv) > 1 else L.lire(racine)
        brut = est_au_cours_brut(L.CONTRATS, racine, cours["fichier"])
        table, _ = L.table_des_ecritures(racine)
        connus, ops = lire_les_operations(racine)
        vues, non_vues = operations_jugees(cours, ops, table, L.COMMUN.norm_valeur)
        par_m, connus_m = operations_par_mnemonique(table, L.COMMUN.norm_valeur, connus, ops)
        courbe, inconnues = (corriger(cours["barres"], par_m, connus_m, _assembler().R.facteur_apres) if brut
                             else (cours["barres"], sorted(m for m in cours["barres"] if m not in connus_m)))
        seuil = _assembler().seuil_de_variation()
        toutes = [d for b in cours["barres"].values() for d in b]
        rang = {d: i for i, (d, _) in enumerate(L.CAL.seances_entre(min(toutes), max(toutes), cours["seances"]))}
    except BaseException as e:   # noqa: BLE001  sans énumérer
        print(f"ARRÊT — la mesure n'a pas pu se faire : {type(e).__name__} : {e}")
        return 2
    try:
        garder_la_nature(brut, vues, non_vues, cours["fichier"])
        garde = "passe"
    except ValueError as e:
        garde = f"REFUSERAIT — {e}"
    print(f"fichier : {cours['fichier']} · déclaré au cours brut : {'oui' if brut else 'non'} · seuil lu : {seuil}")
    print(f"grandes opérations vues au jour dit : {len(vues)} · non vues : {len(non_vues)} · garde de nature : {garde}")
    print(f"valeurs aux opérations inconnues : {len(inconnues)} {inconnues}")
    compte = {(q, g): 0 for q in ("brut", "courbe") for g in ("connues", "inconnues")}
    restants, paires = [], 0
    for m in sorted(cours["barres"]):
        g = "connues" if m in connus_m else "inconnues"
        ds = sorted(cours["barres"][m])
        for d0, d1 in zip(ds, ds[1:]):
            if rang[d1] - rang[d0] != 1:
                continue
            paires += 1
            for q, b in (("brut", cours["barres"]), ("courbe", courbe)):
                r = float(b[m][d1]["close"]) / float(b[m][d0]["close"])
                if abs(r - 1) > seuil:
                    compte[(q, g)] += 1
                    if q == "courbe":
                        restants.append((m, d0, d1, round(r, 4)))
    print(f"paires de séances consécutives : {paires}")
    for (q, g), n in compte.items():
        print(f"sauts au-delà du seuil, {q}, valeurs aux opérations {g} : {n}")
    for m, d0, d1, r in restants:
        print(f"SAUT RESTANT {m} {d0} → {d1} : ×{r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
