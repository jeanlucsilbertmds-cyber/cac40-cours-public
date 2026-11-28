#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py — Ven 27-11-2026 (Paris), lot W2c du plan R505. Simulation uniquement : on
mesure des gains passés, aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — Ce programme porte les DEUX mesures de ressemblance de R-505 version 2 (texte accepté par Jean-Luc le
27-11-2026 à 18h38, etudes/R505_V2/R505_v2_corps.md), différentes PARCE QUE les questions diffèrent (la loi, « Une
version, est-ce une autre stratégie ? ») : « combien de chances le hasard a-t-il eues ? » et « perdent-elles ensemble ? ».
1. LE COMPTE DES ESSAIS k (étape 5) : « les versions de la stratégie RÉELLEMENT envoyées au juge, et les autres
   stratégies déjà RÉELLEMENT jugées » (décision de Jean-Luc du 27-11-2026 à 16h46, A-1082) ; « les versions aux trades
   presque identiques comptent pour UN essai, regroupées par la mesure, valeur la plus prudente fixée avant chaque
   jugement » (décision du 14-11-2026 à 13h44, A-772 : « une méthode de regroupement […] programmée, […] déterministe,
   […] faite systématiquement à chaque fois ») ; nom du programme choisi par Jean-Luc le 14-11 à 14h01 (A-772). La
   méthode est celle de l'expert du 14-11-2026 (etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/
   EXPERT_ESSAIS_SEMBLABLES_Sam_14-11-2026.md, §3 ④ et §4 point 2, scripts gardés au dépôt sous
   etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/preuves/EXPERT_ESSAIS_SEMBLABLES_SCRIPTS_Sam_14-11-2026/) : le « k équivalent
   par simulation du maximum » — on tire des statistiques sous l'hypothèse « aucune version ne vaut rien » avec
   EXACTEMENT la corrélation mesurée des gains quotidiens, on prend le maximum, on cherche la barre que ce maximum ne
   passe que 5 fois sur 100, et k est le nombre de versions INDÉPENDANTES qui auraient cette barre ; « la valeur la plus
   prudente » est « la plus haute du rééchantillonnage et du calcul plein » (loi, « À PRÉCISER », point ⑨ ; « 168
   aujourd'hui » pour C5).
2. LA RESSEMBLANCE POUR LA MISE EN SERVICE (étape 6 ⑤) : « elles se ressemblent si leurs gains quotidiens sont corrélés
   à 0,5 ou plus, OU si elles détiennent la même action le même jour au moins une fois sur deux ; elles entrent en
   service par ordre de mérite, chacune seulement si elle ne ressemble à aucune déjà en service » (décision de Jean-Luc
   du 14-11-2026 à 18h58, « Ok pour la une », A-791). Le dénominateur de « une fois sur deux » est repris TEL QUEL du
   collège (loi, « À PRÉCISER », point ⑥ ; DEFINIR_STRATEGIES_QUI_SE_RESSEMBLENT_Sam_14-11-2026.md, §4 point 2) :
   « nombre de (action, jour) communs ÷ nombre de (action, jour) de la plus petite des deux ».

① RÔLE — Mesurer, à UN seul endroit (R-708 : deux implémentations d'une même chose divergent toujours), le nombre
  effectif d'essais k du juge et la ressemblance de deux stratégies pour la mise en service ; et CALIBRER les deux
  mesures sur les chiffres publiés de l'expert et du collège du 14-11-2026 avant tout autre usage (préférences §9bis :
  « un motif de recherche se calibre sur un cas connu avant de servir »).
② CONTEXTE D'APPEL — Au 27-11-2026 : les épreuves tests/EPREUVES_DE_LA_RESSEMBLANCE_Ven_27-11-2026.py, et la ligne de
  commande du calibrage :
    python3 -B programmes/COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py <racine> --calibrer-c5 [--raccourci] [--processus=N]
  (sans « --raccourci » : les 2 695 versions rejouées une à une, plus de 2 minutes, à jouer sur GitHub, code
  « EssaisRessemblance » de tests/LANCEMENT_DES_EPREUVES.json). DESTINÉ au juge (contrôle 1 de l'étape 5, le Sharpe
  dégonflé avec N = k, programmes/MODULE_SHARPE_DEGONFLE.py) et à la mise en service (étape 6 ⑤) quand la courbe du
  compte au jour le jour de chaque version existera (A-1071, lot W2b du plan R505) : AUCUN programme du circuit ne
  l'appelle encore. Il exige numpy, que le circuit du soir n'installe pas.
③ ENTRÉE — Voir chaque fonction ; la ligne de commande ci-dessus.
④ CONDITIONS D'ENTRÉE — Python 3.9 et plus ; numpy (une matrice de corrélation de milliers de versions et sa
  décomposition ne se calculent pas en Python pur).
⑤ SORTIE — Le chargement ne rend rien ; la ligne de commande sort par un code : 0 calibrage reproduit · 1 calibrage NON
  reproduit (l'écart est affiché) · 2 calcul impossible (argument, fichier, exception).
⑥ TRAITEMENT — Voir chaque fonction ; `main` pour la ligne de commande.
⑦ UNITÉ — Les gains quotidiens sont dans une unité quelconque, la MÊME pour toute la série (euros chez l'expert,
  fraction du compte chez le juge) : une corrélation ne dépend pas de l'unité. k est un nombre d'essais (entier ≥ 1).
  Les dates sont au format AAAA-MM-JJ.
⑧ POURQUOI — Voir le sens en tête. La simulation du maximum est retenue parce qu'elle « ne dépend d'aucun seuil choisi,
  et c'est exactement la question posée » (expert, §4 point 2) ; les autres méthodes divergent de 65 à 2 509 sur nos
  données (Nyholt, Galwey, Li et Ji, regroupements à seuil ; expert, §3, point 4 de la lecture).
⑨ CE QUI CLOCHE — ① La série quotidienne de chaque version n'est pas encore fabriquée par le circuit (A-1071, lot W2b) :
  les fonctions la prennent en paramètre ; le calibrage refait la série comme l'expert (valorisée chaque soir), ce qui
  est une SECONDE fabrication, provisoire, à remplacer par celle de W2b dès qu'elle existe (R-708). ② La contre-expertise
  du 14-11-2026 (CONTRE_EXPERTISE_ESSAIS_SEMBLABLES_Sam_14-11-2026.md, §4 ; « corrections appliquées sans question »,
  A-774) demandait le quantile du maximum de la statistique DU JUGE par rééchantillonnage stationnaire, sur la famille
  entière en un seul maximum ; la loi v2 a retenu le nombre de l'expert (point ⑨) : ce programme suit la loi, l'écart est
  signalé dans la note de livraison. ③ La loi ne dit pas sur quelle période se mesurent les séries : l'expert demande
  « la partie de réglage, jamais ceux de la partie d'examen » (§4 point 3) ; c'est à l'appelant de passer les 70 %.
  ④ « Plus d'une fois sur deux » (collège, §3, lecture 1) contre « au moins la moitié » et « ≥ 0,5 » (collège, §4 point
  2 et script `combine.py`) et « au moins une fois sur deux » (loi) : le programme applique « ≥ », comme la définition
  et le script du collège ; signalé dans la note.
⑩ EFFET — Les fonctions de mesure ne lisent ni n'écrivent rien, sauf `lire_les_seuils` et `strategies_deja_jugees`
  (lecture). Le calibrage lit le dépôt et lance le juge en mémoire (`JUGE_DES_STRATEGIES.jouer`) ; il n'écrit rien.
⑪ TERMINAISON — Le chargement rend la main ; `main` sort par sys.exit.
⑫ DÉFINITIONS
  une version : une stratégie déclinée par la moulinette ; « une version est équivalent à une nouvelle stratégie »
    (Jean-Luc, 31-10-2026 à 15h51, A-666)
  le gain quotidien : la variation du compte d'une version d'une séance à la suivante, frais compris le jour de sortie
  le k équivalent : le nombre de versions indépendantes dont le meilleur dépasserait la même barre, 5 fois sur 100
  le chevauchement : la part des jours de position de la plus petite des deux stratégies où l'autre tient la même
    action le même jour
"""
import hashlib
import json
import math
import os
import sys
from datetime import datetime
from statistics import NormalDist

# LA PROCÉDURE DE L'EXPERT DU 14-11-2026, FIXÉE AVANT TOUT JUGEMENT (A-772 : « déterministe ») — mesurer_k_effectif.py,
# §4 : graine 20261114 ; 20 000 tirages pour le calcul plein, par lots de 2 000 ; rééchantillonnage des séances par
# blocs de 20, 10 fois, 10 000 tirages chacun. Ce sont des CHOIX TECHNIQUES de la méthode (loi, « À PRÉCISER » :
# fixés à la programmation), pas des seuils de décision : le seul seuil, le risque global 0,05, se lit à la table de la loi.
GRAINE = 20261114
TIRAGES = 20000
TIRAGES_PAR_LOT = 2000
REECHANTILLONNAGES = 10
LONGUEUR_DES_BLOCS = 20
TIRAGES_PAR_REECHANTILLONNAGE = 10000

# LES CHIFFRES PUBLIÉS QUE LE CALIBRAGE DOIT REPRODUIRE, recopiés des rapports du 14-11-2026 (sorties capturées ; ce sont
# des RÉFÉRENCES de calibrage, pas des valeurs de calcul). Expert, §3 : « CORRÉLATIONS (paires de versions) : médiane
# 0.043 · moyenne 0.141 · part > 0,9 : 0.012 · part < 0,1 : 0.620 » ; « MAXIMUM SIMULÉ (20 000 tirages) : barre z à 5 % =
# 3.434 -> k équivalent = 168 » ; « rééchantillonnage par blocs (10) : k équivalent de 119 à 156 » ; § en tête « environ
# 140 à 170 ». Collège, §3 : « tp 2 % contre tp 3 % […] un jeton : ρ = 0.67 · chevauchement = 0.85 ; tp 2 % contre tp 8 % :
# ρ = 0.35 · chevauchement = 0.65 » ; « DG seule contre TTE seule (tp 4 %, sl 2,5 %, 20 séances) : ρ = -0.08 ·
# chevauchement = 0.00 ». La tolérance du k simulé, ±5 %, est le bruit de simulation MESURÉ par la contre-expertise
# (§2, F : « 168 dans un tirage, 161 dans un autre de 40 000 — ±5 % ») ; les chiffres sans hasard doivent sortir égaux
# à la précision publiée.
REFERENCES_DU_CALIBRAGE = {
    "correlation_mediane": (0.043, 0.0005), "correlation_moyenne": (0.141, 0.0005),
    "part_au_dessus_de_0_9": (0.012, 0.0005), "part_sous_0_1": (0.620, 0.0005),
    "k_plein": (168.0, 0.05 * 168.0), "k_prudent_bas": 140.0, "k_prudent_haut": 170.0 * 1.05,
    "tp2_tp3": (0.67, 0.85), "tp2_tp8": (0.35, 0.65), "dg_tte": (-0.08, 0.00), "precision_ressemblance": 0.005,
}


def lire_les_seuils(racine):
    """Rend la table des seuils de la loi telle que la porte du juge la compose : le REGISTRE, puis les seuils en attente.

    ① RÔLE — Lire le risque global (« 0,05 » de « 0,05 ÷ k ») et les deux seuils de ressemblance là où ils vivent, jamais
      dans ce code (R-728, R-743 ②).
    ② CONTEXTE D'APPEL — `compter_les_essais` et `se_ressemblent` quand l'appelant ne passe pas de table ; `main` ; les
      épreuves.
    ③ ENTRÉE — `racine` : la racine d'un dépôt (gouvernance/REGISTRE_REGLES.md et le fichier des seuils en attente).
    ④ CONDITIONS D'ENTRÉE — programmes/MODULE_JUGEMENT.py et programmes/CONTRATS_DES_FICHIERS.py sous la racine.
    ⑤ SORTIE — UNE valeur : la table {clé : {"valeur", "sens", "source"}}.
      [rend: 1]
    ⑥ TRAITEMENT — ① `MODULE_JUGEMENT.table_de_la_loi` sur le texte du REGISTRE · ② recouvrir par
      `MODULE_JUGEMENT.table_des_seuils_en_attente` — le même ordre que `JUGER_UNE_FICHE.juger_une_fiche`.
    ⑦ UNITÉ — Des textes.
    ⑧ POURQUOI — La table est composée une fois, par les fonctions du juge (R-708) ; ce programme ne relit rien à sa façon.
    ⑨ CE QUI CLOCHE — La composition « REGISTRE puis en attente » est écrite deux fois (ici et dans JUGER_UNE_FICHE) :
      deux lignes, à fusionner à l'installation de R-505 v2 au REGISTRE (étape I1), quand le fichier en attente disparaît.
    ⑩ EFFET — Lit deux fichiers ; ajoute programmes/ au chemin d'import.
    ⑪ TERMINAISON — Rend la main ; lève OSError ou ValueError si le REGISTRE manque ou si sa table est illisible.
      [sort: non]
    """
    dossier = os.path.join(racine, "programmes")
    if dossier not in sys.path:
        sys.path.insert(0, dossier)
    import MODULE_JUGEMENT as MJ
    with open(os.path.join(racine, "gouvernance", "REGISTRE_REGLES.md"), encoding="utf-8") as f:
        table = MJ.table_de_la_loi(f.read())
    table.update(MJ.table_des_seuils_en_attente(racine))
    return table


def risque_global(table):
    """Rend le risque global de la loi, le « 0,05 » de « 0,05 ÷ k », lu à la table.

    ① RÔLE — Donner le niveau de la simulation du maximum : la barre que le meilleur des essais sans valeur ne passe que
      « 0,05 » du temps (n°42, A-1070 : « au seuil 0,05 ÷ k »).
    ② CONTEXTE D'APPEL — `compter_les_essais` ; les épreuves.
    ③ ENTRÉE — `table` : le rendu de `lire_les_seuils`.
    ④ CONDITIONS D'ENTRÉE — programmes/ dans le chemin d'import (MODULE_JUGEMENT).
    ⑤ SORTIE — UNE valeur : le risque, un nombre dans ]0, 1[.
      [rend: 1]
    ⑥ TRAITEMENT — `MODULE_JUGEMENT.seuil_de_la_loi(table, "seuil_de_preuve", k=1)` : « 0,05 ÷ k » avec k = 1.
    ⑦ UNITÉ — Une probabilité.
    ⑧ POURQUOI — Le même nombre que la barre du juge, lu par la même fonction (R-708) ; la méthode de l'expert est la
      définition M_eff = log(1−α)/log(1−α_loc), avec le α du juge.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si la case est illisible ou vaut 1.
      [sort: non]
    """
    import MODULE_JUGEMENT as MJ
    alpha, raison = MJ.seuil_de_la_loi(table, "seuil_de_preuve", k=1)
    if alpha is None or not 0.0 < alpha < 1.0:
        raise ValueError("risque global illisible à la table de la loi : %s" % (raison or alpha))
    return alpha


def seuils_de_ressemblance(table):
    """Rend les deux seuils de la ressemblance pour la mise en service, lus à la table.

    ① RÔLE — Lire « corrélés à 0,5 ou plus » et « au moins une fois sur deux » (A-791) à un seul endroit.
    ② CONTEXTE D'APPEL — `se_ressemblent`, `mettre_en_service` ; les épreuves.
    ③ ENTRÉE — `table` : le rendu de `lire_les_seuils`.
    ④ CONDITIONS D'ENTRÉE — programmes/ dans le chemin d'import.
    ⑤ SORTIE — DEUX valeurs : le seuil de corrélation et le seuil de chevauchement, chacun dans ]0, 1].
      [rend: 2]
    ⑥ TRAITEMENT — `seuil_de_la_loi` pour `ressemblance_correlation_minimum` et `ressemblance_chevauchement_minimum`
      (domaine « proba », MODULE_JUGEMENT.DOMAINES_DES_CLES_DE_LA_TABLE).
    ⑦ UNITÉ — Une corrélation ; une part.
    ⑧ POURQUOI — La table de la loi v2 porte la ligne « ressemblance » en prose (« corrélation des gains quotidiens ≥
      0,5, ou même action le même jour ≥ 1 fois sur 2 ») : les deux nombres vivent, en attendant l'installation de la loi
      au REGISTRE (I1), dans donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv, comme la PBO du lot L3.
    ⑨ CE QUI CLOCHE — Aucune référence de strictesse : un seuil RELEVÉ (0,7) passerait et laisserait entrer des doublons
      (collège, §3, lecture 2) ; à ajouter avec la loi (REFERENCES_DE_STRICTESSE de MODULE_JUGEMENT).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si une case est illisible.
      [sort: non]
    """
    import MODULE_JUGEMENT as MJ
    rendu = []
    for cle in ("ressemblance_correlation_minimum", "ressemblance_chevauchement_minimum"):
        s, raison = MJ.seuil_de_la_loi(table, cle)
        if s is None:
            raise ValueError("seuil de ressemblance illisible : %s" % raison)
        rendu.append(s)
    return rendu[0], rendu[1]


def _matrice(series):
    """Rend les séries quotidiennes en matrice numpy, une ligne par version, après contrôle.

    ① RÔLE — Refuser une entrée qui fausserait la corrélation sans le dire (R-734).
    ② CONTEXTE D'APPEL — `mesurer_le_nombre_effectif`, `empreinte_des_series`.
    ③ ENTRÉE — `series` : une liste de listes ou un tableau numpy, n lignes × T séances, alignées sur le même calendrier.
    ④ CONDITIONS D'ENTRÉE — numpy.
    ⑤ SORTIE — UNE valeur : le tableau float64 (n, T).
      [rend: 1]
    ⑥ TRAITEMENT — conversion ; refus si la forme n'est pas 2 dimensions, si n < 1 ou T < 2, si une valeur n'est pas finie.
    ⑦ UNITÉ — Celle des séries.
    ⑧ POURQUOI — Une valeur manquante (NaN) rendrait toute la matrice NaN, et la barre avec elle.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    import numpy as np
    X = np.asarray(series, dtype=np.float64)
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 2:
        raise ValueError("séries : il faut n ≥ 1 lignes de T ≥ 2 séances, reçu la forme %r" % (X.shape,))
    if not np.isfinite(X).all():
        raise ValueError("séries : %d valeur(s) non finie(s)" % int((~np.isfinite(X)).sum()))
    return X


def empreinte_des_series(series):
    """Rend l'empreinte des séries mesurées, pour prouver plus tard sur QUOI k a été fixé.

    ① RÔLE — « Fixée avant chaque jugement » (A-772) : l'empreinte relie le k écrit au verdict aux séries exactes.
    ② CONTEXTE D'APPEL — `compter_les_essais`.
    ③ ENTRÉE — `series` : comme `_matrice`.
    ④ CONDITIONS D'ENTRÉE — numpy.
    ⑤ SORTIE — UNE valeur : « sha256:<64 caractères> ».
      [rend: 1]
    ⑥ TRAITEMENT — sha256 de la forme puis des octets float64 petit-boutistes, ligne par ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une empreinte ne dépend ni de la machine ni de l'ordre des octets.
    ⑨ CE QUI CLOCHE — L'ordre des lignes compte : deux appelants qui rangent les versions autrement ont deux empreintes
      (le k, lui, ne change pas).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (par `_matrice`).
      [sort: non]
    """
    import numpy as np
    X = _matrice(series)
    h = hashlib.sha256(("%d,%d;" % X.shape).encode())
    h.update(np.ascontiguousarray(X, dtype="<f8").tobytes())
    return "sha256:" + h.hexdigest()


def _racine_de_la_correlation(X):
    """Rend A tel que A Aᵀ soit la matrice de corrélation de Pearson des lignes de X, construite comme l'expert.

    ① RÔLE — Fabriquer des tirages gaussiens qui ont EXACTEMENT la corrélation mesurée (expert, §3 ④).
    ② CONTEXTE D'APPEL — `mesurer_le_nombre_effectif`.
    ③ ENTRÉE — `X` : n × T, aucune ligne constante.
    ④ CONDITIONS D'ENTRÉE — numpy.
    ⑤ SORTIE — UNE valeur : A, n × n.
      [rend: 1]
    ⑥ TRAITEMENT — ① R = `numpy.corrcoef(X)` · ② valeurs et vecteurs propres (`numpy.linalg.eigh`) · ③ valeurs
      négatives (arrondis) ramenées à 0 · ④ A = V × √w — les gestes de mesurer_k_effectif.py, dans cet ordre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — À l'identique de l'expert : sur la machine du Chat, le 27-11-2026, cette construction redonne
      EXACTEMENT sa barre (3,434) et son k (168,0) avec sa graine ; une autre construction de même loi (C g, C les lignes
      centrées réduites, essayée ce jour) donnait 152 avec la même graine et 154 à 169 avec d'autres — le bruit de
      simulation, pas une erreur.
    ⑨ CE QUI CLOCHE — Le signe d'un vecteur propre est laissé à la bibliothèque de calcul (LAPACK) : sur une autre
      machine, la même graine peut donner d'autres tirages, donc un k différent dans le bruit de simulation (±5 %,
      contre-expertise du 14-11). C'est pourquoi k est FIXÉ et ÉCRIT avant le jugement, avec l'empreinte des séries
      (`compter_les_essais`), jamais recalculé ensuite.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import numpy as np
    w, V = np.linalg.eigh(np.corrcoef(X))
    return V * np.sqrt(np.clip(w, 0.0, None))


def _barre_du_maximum(A, rng, tirages, alpha):
    """Rend la barre que le maximum de statistiques corrélées (sans aucune valeur) ne dépasse qu'avec la probabilité alpha.

    ① RÔLE — Le cœur de la méthode de l'expert (`barre_du_max`, mesurer_k_effectif.py).
    ② CONTEXTE D'APPEL — `mesurer_le_nombre_effectif`.
    ③ ENTRÉE — `A` : la racine de la corrélation (`_racine_de_la_correlation`) · `rng` : un générateur numpy · `tirages` : un multiple de
      TIRAGES_PAR_LOT · `alpha` : le risque global.
    ④ CONDITIONS D'ENTRÉE — numpy.
    ⑤ SORTIE — UNE valeur : la barre (un nombre de la loi normale centrée réduite).
      [rend: 1]
    ⑥ TRAITEMENT — par lots de TIRAGES_PAR_LOT : z = A × (gaussiennes indépendantes, une par colonne de A), maximum par tirage (test
      unilatéral) ; puis le quantile 1 − alpha des maxima.
    ⑦ UNITÉ — Écarts-types.
    ⑧ POURQUOI — Les lots bornent la mémoire (n × 2 000 nombres à la fois) et gardent l'ordre des tirages de l'expert.
      Le quantile est pris à 1 − alpha : 0,95 pour alpha = 0,05 (1,0 − 0,05 == 0,95 en flottants, vérifié).
    ⑨ CE QUI CLOCHE — L'hypothèse gaussienne : la contre-expertise du 14-11 mesure qu'elle SOUS-estime la barre par
      rapport au rééchantillonnage stationnaire (k presque doublé sur la famille jugeable) — sens anti-prudent, consigné.
    ⑩ EFFET — Fait avancer `rng`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import numpy as np
    if tirages % TIRAGES_PAR_LOT:
        raise ValueError("tirages = %r : il faut un multiple de %d" % (tirages, TIRAGES_PAR_LOT))
    maxima = [(A @ rng.standard_normal((A.shape[1], TIRAGES_PAR_LOT))).max(axis=0)
              for _ in range(tirages // TIRAGES_PAR_LOT)]
    return float(np.quantile(np.concatenate(maxima), 1.0 - alpha))


def k_de_la_barre(barre, alpha):
    """Rend le nombre de versions INDÉPENDANTES dont la barre, au même risque global, serait celle-ci.

    ① RÔLE — Convertir une barre en nombre d'essais : k = alpha ÷ (1 − Φ(barre)) (expert, §3 ④ ; c'est la barre de
      Bonferroni du juge, « 0,05 ÷ k », lue à l'envers).
    ② CONTEXTE D'APPEL — `mesurer_le_nombre_effectif` ; les épreuves.
    ③ ENTRÉE — `barre` : un nombre · `alpha` : le risque global.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : k (un nombre réel, non arrondi).
      [rend: 1]
    ⑥ TRAITEMENT — `statistics.NormalDist().cdf`.
    ⑦ UNITÉ — Des essais.
    ⑧ POURQUOI — Φ⁻¹(1 − 0,05/k) est la barre du juge pour k essais indépendants ; inverser donne le k qui a la même barre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ZeroDivisionError si la barre est hors de portée des flottants (> 38).
      [sort: non]
    """
    return alpha / (1.0 - NormalDist().cdf(barre))


def mesurer_le_nombre_effectif(series, alpha, graine=GRAINE, tirages=TIRAGES, reechantillonnages=REECHANTILLONNAGES,
                               longueur_des_blocs=LONGUEUR_DES_BLOCS,
                               tirages_par_reechantillonnage=TIRAGES_PAR_REECHANTILLONNAGE):
    """Mesure le nombre effectif d'essais de n versions par la simulation du maximum, calcul plein et rééchantillonné.

    ① RÔLE — La mesure de l'expert du 14-11-2026 (§3 ④ et son incertitude), geste pour geste (mesurer_k_effectif.py).
    ② CONTEXTE D'APPEL — `compter_les_essais` ; le calibrage ; les épreuves.
    ③ ENTRÉE — `series` : n versions × T séances de gains quotidiens, alignés · `alpha` : le risque global (lu à la loi
      par `risque_global`) · `graine`, `tirages`, `reechantillonnages`, `longueur_des_blocs`,
      `tirages_par_reechantillonnage` : les réglages de la procédure, par défaut ceux de l'expert.
    ④ CONDITIONS D'ENTRÉE — numpy ; aucune version sans aucun gain non nul (écart-type nul) : refusée, nommée par son
      rang ; T > longueur_des_blocs.
    ⑤ SORTIE — UNE valeur : un dictionnaire — n_versions, n_seances, barre_pleine, k_plein, k_par_reechantillonnage
      (liste), k_prudent (le plus haut de k_plein et des k rééchantillonnés, non arrondi), procedure (les réglages).
      [rend: 1]
    ⑥ TRAITEMENT — ① n = 1 : k = 1, sans tirage · ② racine de la corrélation de Pearson des lignes · ③ barre du
      maximum, TIRAGES tirages, puis k · ④ REECHANTILLONNAGES fois : T ÷ longueur_des_blocs blocs de séances
      consécutives tirés au hasard (début dans [0, T − longueur_des_blocs[), versions devenues muettes dans l'échantillon
      écartées, racine recalculée, barre sur tirages_par_reechantillonnage, k · ⑤ le plus prudent = le plus haut
      (loi, « À PRÉCISER », point ⑨). UN SEUL générateur, graine fixe, consommé dans cet ordre (celui de l'expert).
    ⑦ UNITÉ — Des essais (nombres réels).
    ⑧ POURQUOI — Le rééchantillonnage dit l'incertitude de la corrélation estimée sur T séances ; « prendre la valeur
      prudente (la plus haute du rééchantillonnage et du calcul plein : 168 aujourd'hui) » (expert, §4 point 2).
    ⑨ CE QUI CLOCHE — ① k peut dépasser n par le seul bruit de simulation quand les versions sont presque
      indépendantes : c'est `compter_les_essais` qui le borne à n. ② Les versions muettes dans un échantillon en sont
      écartées (choix de l'expert, gardé) : elles font baisser ce k-là. ③ Le temps croît comme n² × tirages : l'expert
      écrivait 7 s pour le calcul plein de 2 695 versions ; sur la machine du Chat, 12 s pour le calcul plein, et le
      rééchantillonnage en plus (durées dans la note de livraison) — au-delà de 2 minutes avec le jeu des versions.
    ⑩ EFFET — Aucun (le générateur est local).
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    import numpy as np
    X = _matrice(series)
    n, T = X.shape
    procedure = {"methode": "simulation du maximum (expert du 14-11-2026), plus haut du calcul plein et du "
                            "rééchantillonnage par blocs", "alpha": alpha, "graine": graine, "tirages": tirages,
                 "reechantillonnages": reechantillonnages, "longueur_des_blocs": longueur_des_blocs,
                 "tirages_par_reechantillonnage": tirages_par_reechantillonnage}
    muettes = [i for i in range(n) if not X[i].std() > 0]
    if muettes:
        raise ValueError("%d version(s) sans aucun gain non nul (rangs %s) : leur corrélation n'existe pas"
                         % (len(muettes), muettes[:10]))
    if n == 1:
        return {"n_versions": 1, "n_seances": T, "barre_pleine": None, "k_plein": 1.0, "k_par_reechantillonnage": [],
                "k_prudent": 1.0, "procedure": procedure}
    if T <= longueur_des_blocs:
        raise ValueError("T = %d séances : il en faut plus que la longueur des blocs (%d)" % (T, longueur_des_blocs))
    rng = np.random.default_rng(graine)
    barre = _barre_du_maximum(_racine_de_la_correlation(X), rng, tirages, alpha)
    k_plein = k_de_la_barre(barre, alpha)
    k_blocs = []
    for _ in range(reechantillonnages):
        debuts = rng.integers(0, T - longueur_des_blocs, size=T // longueur_des_blocs)
        colonnes = np.concatenate([np.arange(s, s + longueur_des_blocs) for s in debuts])
        Xb = X[:, colonnes]
        actives = Xb.std(axis=1) > 0
        if actives.sum() < 2:
            k_blocs.append(float(actives.sum()))
            continue
        k_blocs.append(k_de_la_barre(_barre_du_maximum(_racine_de_la_correlation(Xb[actives]), rng,
                                                        tirages_par_reechantillonnage, alpha), alpha))
    return {"n_versions": n, "n_seances": T, "barre_pleine": barre, "k_plein": k_plein,
            "k_par_reechantillonnage": k_blocs, "k_prudent": max([k_plein] + k_blocs), "procedure": procedure}


def strategies_deja_jugees(racine, avant):
    """Compte les autres stratégies déjà RÉELLEMENT jugées, d'après les verdicts écrits avant un instant.

    ① RÔLE — La seconde moitié de k : « et les autres stratégies déjà RÉELLEMENT jugées ; pas les lignes du registre
      jamais jugées » (A-1082) ; « rejuger crée un nouveau verdict daté […] et il compte dans k » (loi, « À PRÉCISER »,
      point ⑩).
    ② CONTEXTE D'APPEL — `compter_les_essais`.
    ③ ENTRÉE — `racine` : la racine du dépôt · `avant` : l'instant du jugement, AAAA-MM-JJTHH:MM:SS+01:00 (comme
      `date_verdict` du contrat VERDICT).
    ④ CONDITIONS D'ENTRÉE — Les verdicts sont les fichiers JSON du dossier verdicts/ (contrat VERDICT et
      FICHIERS_A_VENIR de programmes/CONTRATS_DES_FICHIERS.py, « à venir » : écrit par le juge).
    ⑤ SORTIE — DEUX valeurs : le nombre de verdicts comptés, et la liste des (fiche_id, date_verdict) comptés.
      [rend: 2]
    ⑥ TRAITEMENT — ① dossier verdicts/ absent → 0 (aucun verdict n'a jamais été écrit ; A-1082 : « zéro à ce jour ») ·
      ② chaque *.json : lu, champs `fiche_id`, `date_verdict`, `verdict` exigés · ③ compté si `date_verdict` < `avant`
      et si `verdict` n'est pas « NON JUGEABLE » (un mot de MOTS_DU_VERDICT, sinon refus).
    ⑦ UNITÉ — Des jugements.
    ⑧ POURQUOI — « NON JUGEABLE » dit qu'il manquait un champ de la déclaration : rien n'a été jugé (contrôle ① de la
      version 1). Chaque verdict compte UN, même pour une stratégie à plusieurs versions : la loi compte « les autres
      stratégies ».
    ⑨ CE QUI CLOCHE — ① Ces deux lectures (NON JUGEABLE exclu ; un verdict = 1, quelles que soient ses versions) sont des
      choix du lot, signalés dans la note : la loi ne les dit pas mot à mot. ② Un dossier verdicts/ absent PARCE QU'une
      copie partielle l'a omis rendrait 0 à tort : l'appelant juge sur un clone complet.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ; lève ValueError pour un verdict illisible, OSError pour un fichier illisible.
      [sort: non]
    """
    dossier = os.path.join(racine, "programmes")
    if dossier not in sys.path:
        sys.path.insert(0, dossier)
    import CONTRATS_DES_FICHIERS as CT
    limite = datetime.fromisoformat(avant)
    if limite.tzinfo is None:
        raise ValueError("instant du jugement sans fuseau : %r" % (avant,))
    rep = os.path.join(racine, "verdicts")
    if not os.path.isdir(rep):
        return 0, []
    comptes = []
    for nom in sorted(os.listdir(rep)):
        if not nom.endswith(".json"):
            continue
        with open(os.path.join(rep, nom), encoding="utf-8") as f:
            try:
                v = json.load(f)
            except ValueError as e:
                raise ValueError("verdict illisible %s : %s" % (nom, e))
        if not isinstance(v, dict) or any(c not in v for c in ("fiche_id", "date_verdict", "verdict")):
            raise ValueError("verdict %s : champs fiche_id, date_verdict, verdict exigés" % nom)
        if v["verdict"] not in CT.MOTS_DU_VERDICT:
            raise ValueError("verdict %s : mot %r hors de MOTS_DU_VERDICT" % (nom, v["verdict"]))
        d = datetime.fromisoformat(v["date_verdict"])
        if d.tzinfo is None:
            raise ValueError("verdict %s : date sans fuseau %r" % (nom, v["date_verdict"]))
        if d < limite and v["verdict"] != "NON JUGEABLE":
            comptes.append((v["fiche_id"], v["date_verdict"]))
    return len(comptes), comptes


def compter_les_essais(series_des_versions_envoyees, racine, avant, table=None, **procedure):
    """Rend k, le nombre d'essais du juge, fixé AVANT le jugement : versions envoyées regroupées par ressemblance + autres.

    ① RÔLE — La valeur de k que le contrôle 1 de l'étape 5 (Sharpe dégonflé, N = k) et la barre 0,05 ÷ k emploient
      (A-1082, A-772, A-774 ; loi, table des seuils, ligne « k »).
    ② CONTEXTE D'APPEL — Destiné au juge, juste avant le regard unique sur les 30 % ; aucun appelant au 27-11-2026.
    ③ ENTRÉE — `series_des_versions_envoyees` : les gains quotidiens de CHAQUE version envoyée au juge, mesurés sur les
      70 % (expert, §4 point 3), une ligne par version · `racine` · `avant` : l'instant du jugement (avec fuseau) ·
      `table` : la table des seuils, ou None pour `lire_les_seuils(racine)` · `procedure` : les réglages de
      `mesurer_le_nombre_effectif`, par défaut ceux de l'expert.
    ④ CONDITIONS D'ENTRÉE — Celles de `mesurer_le_nombre_effectif` et de `strategies_deja_jugees`.
    ⑤ SORTIE — UNE valeur : un dictionnaire — k (entier ≥ 1), k_des_versions (entier), autres_strategies_jugees
      (entier), verdicts_comptes, mesure (le rendu de `mesurer_le_nombre_effectif`), empreinte_des_series, avant.
      [rend: 1]
    ⑥ TRAITEMENT — ① alpha lu à la loi · ② mesure · ③ k_des_versions = ⌈k_prudent⌉, borné à n (une version ne vaut
      jamais plus d'un essai) · ④ + les verdicts déjà rendus · ⑤ l'empreinte des séries.
    ⑦ UNITÉ — Des essais.
    ⑧ POURQUOI — Arrondi vers le HAUT : la valeur la plus prudente (A-772) ; le Sharpe dégonflé exige un entier
      (programmes/MODULE_SHARPE_DEGONFLE.py). Borne à n : au-delà, c'est le bruit de simulation (⑨ ① de la mesure).
    ⑨ CE QUI CLOCHE — ① Les autres stratégies s'ajoutent une par une, en Bonferroni : la contre-expertise mesure que
      « 168 + 69 » dépasse un peu le risque visé (0,0517 pour 0,05), la loi l'additionne pourtant (« plus les autres
      stratégies ») ; signalé. ② Ce dictionnaire n'est écrit nulle part : le verdict (contrat VERDICT, champ « k ») doit
      le porter — K_DU_VERDICT décrit encore le compte de la version 1 (lignes du registre), à revoir par le lot du juge.
    ⑩ EFFET — Lit des fichiers (seuils, verdicts).
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    if table is None:
        table = lire_les_seuils(racine)
    alpha = risque_global(table)
    mesure = mesurer_le_nombre_effectif(series_des_versions_envoyees, alpha, **procedure)
    k_versions = min(int(math.ceil(mesure["k_prudent"] - 1e-9)), mesure["n_versions"])
    k_versions = max(k_versions, 1)
    autres, comptes = strategies_deja_jugees(racine, avant)
    return {"k": k_versions + autres, "k_des_versions": k_versions, "autres_strategies_jugees": autres,
            "verdicts_comptes": comptes, "mesure": mesure,
            "empreinte_des_series": empreinte_des_series(series_des_versions_envoyees), "avant": avant}


def lire_les_series_des_versions_envoyees(racine, fiche_id):
    """Rend les gains quotidiens de chaque version envoyée au juge pour une fiche, alignés sur leurs séances communes.

    ① RÔLE — Donner à `compter_les_essais` son entrée, lue à UN endroit déclaré au contrat
      (`CONTRATS_DES_FICHIERS.SERIES_DES_VERSIONS_ENVOYEES`, champs `SERIE_D_UNE_VERSION_ENVOYEE`).
    ② CONTEXTE D'APPEL — `k_du_juge`.
    ③ ENTRÉE — `racine` : le dépôt · `fiche_id` : l'identifiant de la fiche jugée.
    ④ CONDITIONS D'ENTRÉE — Le fichier, s'il existe, a l'en-tête du contrat ; dates AAAA-MM-JJ ; gains en euros, finis.
    ⑤ SORTIE — DEUX valeurs : (la liste des séries, une par version, toutes de la même longueur ; None si le fichier
      manque ou est illisible) et la raison (texte vide si tout est lu).
      [rend: 2]
    ⑥ TRAITEMENT — ① chemin du contrat · ② absent → (None, raison) · ③ lire les lignes, en-tête confronté au contrat ·
      ④ calendrier = l'union triée des dates · ⑤ chaque version alignée par `aligner_sur_le_calendrier` (0 les jours
      sans gain).
    ⑦ UNITÉ — Euros par séance.
    ⑧ POURQUOI — A-1082 (Jean-Luc, 27-11-2026 à 16h46, « 1 ») : k compte les versions RÉELLEMENT envoyées au juge,
      regroupées par ressemblance de leurs gains quotidiens (A-772) ; ces gains doivent donc être lus, pas supposés.
    ⑨ CE QUI CLOCHE — ① AU 28-11-2026, AUCUN PROGRAMME N'ÉCRIT CE FICHIER : la moulinette (JOUER_LES_VERSIONS) ne
      garde que des totaux par version (contrat RESULTATS_DES_VERSIONS). Tant que l'écrivain manque, k est INCONNU et
      aucun verdict n'est rendu (réunion I1 ; à porter en Section 0 du BACKLOG). ② Les gains doivent être mesurés sur
      les 70 % (expert, §4 point 3) : ce lecteur ne le vérifie pas, c'est à l'écrivain de le garantir.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; ne lève pas sur un fichier mal formé (rend None et la raison).
      [sort: non]
    """
    import csv
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import CONTRATS_DES_FICHIERS as CT
    chemin = os.path.join(racine, CT.SERIES_DES_VERSIONS_ENVOYEES.format(fiche_id=fiche_id))
    if not os.path.isfile(chemin):
        return None, ("séries des versions envoyées au juge absentes (%s) : k par ressemblance (A-1082) incalculable"
                      % os.path.relpath(chemin, racine))
    par_version = {}
    try:
        with open(chemin, encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            if list(r.fieldnames or []) != list(CT.SERIE_D_UNE_VERSION_ENVOYEE):
                return None, "en-tête %r, contrat %r" % (r.fieldnames, list(CT.SERIE_D_UNE_VERSION_ENVOYEE))
            for ligne in r:
                g = float(ligne["gain_eur"])
                if not math.isfinite(g):
                    return None, "gain non fini pour %s le %s" % (ligne["id_version"], ligne["date"])
                d = par_version.setdefault(ligne["id_version"], {})
                if ligne["date"] in d:
                    return None, "date en double pour %s : %s" % (ligne["id_version"], ligne["date"])
                d[ligne["date"]] = g
    except (OSError, ValueError, KeyError) as ex:
        return None, "séries illisibles : %s: %s" % (type(ex).__name__, ex)
    if not par_version:
        return None, "aucune version dans %s" % os.path.relpath(chemin, racine)
    cal = sorted({d for v in par_version.values() for d in v})
    return [aligner_sur_le_calendrier(par_version[v], cal) for v in sorted(par_version)], ""


def k_du_juge(racine, fiche_id, avant, table=None):
    """Rend k, le nombre d'essais que le juge emploie, PAR `compter_les_essais` — la seule source de k du juge.

    ① RÔLE — Le point où le juge prend k (contrôle 1, Sharpe dégonflé N = k ; contrôle 2, barre 0,05 ÷ k) : réunion I1
      du 28-11-2026, contradiction C3 de la relecture V2 — `JUGE_DES_STRATEGIES.k_a_la_date` (lignes du registre) ne
      décide plus, il n'est plus qu'affiché.
    ② CONTEXTE D'APPEL — `JUGER_UNE_FICHE.juger_une_fiche`, une fois par jugement.
    ③ ENTRÉE — `racine` · `fiche_id` · `avant` : l'instant du jugement (datetime avec fuseau) · `table` : la table des
      seuils ou None.
    ④ CONDITIONS D'ENTRÉE — Celles de `lire_les_series_des_versions_envoyees` et de `compter_les_essais`.
    ⑤ SORTIE — TROIS valeurs : k (entier ≥ 1) ou None ; le dictionnaire de `compter_les_essais` ou None ; la raison.
      [rend: 3]
    ⑥ TRAITEMENT — ① lire les séries · ② absentes → (None, None, raison) · ③ `compter_les_essais` ; une ValueError ou
      une ImportError (numpy) → (None, None, raison).
    ⑦ UNITÉ — Des essais.
    ⑧ POURQUOI — A-1082 (Jean-Luc, 27-11-2026 à 16h46) : « le nombre qui divise la barre de 5 % (k) compte les versions
      de la stratégie réellement envoyées au juge […] ET les autres stratégies déjà réellement jugées ; PAS les lignes
      du registre jamais jugées ».
    ⑨ CE QUI CLOCHE — Voir ⑨ ① de `lire_les_series_des_versions_envoyees` : sans écrivain des séries, k est None.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    series, r = lire_les_series_des_versions_envoyees(racine, fiche_id)
    if series is None:
        return None, None, r
    try:
        d = compter_les_essais(series, racine, avant, table=table)
    except (ValueError, ImportError) as ex:
        return None, None, "compter_les_essais : %s: %s" % (type(ex).__name__, ex)
    return d["k"], d, ""


def aligner_sur_le_calendrier(gains_par_date, calendrier):
    """Rend la liste des gains d'une stratégie, jour par jour du calendrier commun, 0 les jours sans gain.

    ① RÔLE — Mettre deux stratégies sur les MÊMES jours avant de les corréler (loi : « le risque est de […] mal aligner
      les dates »).
    ② CONTEXTE D'APPEL — L'appelant de `se_ressemblent` et de `mettre_en_service` ; les épreuves.
    ③ ENTRÉE — `gains_par_date` : {AAAA-MM-JJ : gain} · `calendrier` : la liste des séances communes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des gains, de la longueur du calendrier.
      [rend: 1]
    ⑥ TRAITEMENT — ① calendrier trié, sans doublon, sinon refus · ② une date des gains hors du calendrier → refus ·
      ③ un jour du calendrier sans gain → 0.
    ⑦ UNITÉ — Celle des gains.
    ⑧ POURQUOI — Un jour sans position ne gagne rien : 0 est exact (collège : série « valorisée chaque soir », nulle hors
      position). Une date hors calendrier serait un gain perdu en silence.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    cal = list(calendrier)
    if cal != sorted(set(cal)):
        raise ValueError("calendrier non trié ou avec doublons")
    hors = sorted(set(gains_par_date) - set(cal))
    if hors:
        raise ValueError("%d date(s) de gain hors du calendrier, dont %s" % (len(hors), hors[:3]))
    return [float(gains_par_date.get(d, 0.0)) for d in cal]


def jours_en_position(operations, dates_de_cotation):
    """Rend l'ensemble des (action, jour) où une stratégie est en position.

    ① RÔLE — Fabriquer ce que compare le chevauchement (collège, §4 point 1 : « la liste des (action, jour) où elle est en
      position »).
    ② CONTEXTE D'APPEL — L'appelant de `se_ressemblent` ; le calibrage ; les épreuves.
    ③ ENTRÉE — `operations` : des dictionnaires à clés « valeur », « date_entree », « date_sortie » (forme des opérations
      de `JUGE_DES_STRATEGIES.jouer`) · `dates_de_cotation` : {valeur : séances où elle cote}.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un ensemble de couples (valeur, AAAA-MM-JJ).
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque opération, chaque séance de cotation de sa valeur entre l'entrée et la sortie, bornes
      COMPRISES (comme le script `ressemblance.py` du collège, `series`).
    ⑦ UNITÉ — Des jours de position.
    ⑧ POURQUOI — Le jour d'entrée et le jour de sortie, la position est tenue : le prix de ces jours compte dans le gain.
    ⑨ CE QUI CLOCHE — Une valeur absente de `dates_de_cotation` est refusée, jamais ignorée.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    jours = set()
    for o in operations:
        m = o["valeur"]
        if m not in dates_de_cotation:
            raise ValueError("valeur %r sans dates de cotation" % (m,))
        if o["date_sortie"] < o["date_entree"]:
            raise ValueError("opération %r : sortie avant l'entrée" % (o,))
        jours.update((m, d) for d in dates_de_cotation[m] if o["date_entree"] <= d <= o["date_sortie"])
    return jours


def correlation_des_gains(gains_a, gains_b):
    """Rend la corrélation de Pearson de deux séries de gains quotidiens alignées.

    ① RÔLE — La première mesure de la ressemblance (A-791 : « gains quotidiens corrélés à 0,5 ou plus »).
    ② CONTEXTE D'APPEL — `se_ressemblent` ; les épreuves.
    ③ ENTRÉE — `gains_a`, `gains_b` : deux listes de même longueur (≥ 2), déjà alignées (`aligner_sur_le_calendrier`).
    ④ CONDITIONS D'ENTRÉE — numpy.
    ⑤ SORTIE — UNE valeur : la corrélation, dans [−1, 1].
      [rend: 1]
    ⑥ TRAITEMENT — `numpy.corrcoef`.
    ⑦ UNITÉ — Sans unité.
    ⑧ POURQUOI — La mesure de toute la littérature (López de Prado ; Meucci ; collège §1).
    ⑨ CE QUI CLOCHE — Peu d'opérations donnent une corrélation bruitée (collège, §6 (b)) : non corrigé, comme la loi.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (longueurs, série constante).
      [sort: non]
    """
    import numpy as np
    X = _matrice([gains_a, gains_b]) if len(gains_a) == len(gains_b) else None
    if X is None:
        raise ValueError("séries de longueurs différentes : %d et %d" % (len(gains_a), len(gains_b)))
    if not (X[0].std() > 0 and X[1].std() > 0):
        raise ValueError("une série est constante : sa corrélation n'existe pas")
    return float(np.corrcoef(X)[0, 1])


def chevauchement(jours_a, jours_b):
    """Rend la part des jours de position de la plus petite des deux stratégies où l'autre tient la même action.

    ① RÔLE — La seconde mesure de la ressemblance (A-791 : « la même action le même jour au moins une fois sur deux »),
      dénominateur repris TEL QUEL du collège (loi, « À PRÉCISER », point ⑥ ; collège, §4 point 2 : « nombre de (action,
      jour) communs ÷ nombre de (action, jour) de la plus petite des deux »).
    ② CONTEXTE D'APPEL — `se_ressemblent` ; les épreuves.
    ③ ENTRÉE — `jours_a`, `jours_b` : deux ensembles de (valeur, jour), rendus par `jours_en_position`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une part dans [0, 1].
      [rend: 1]
    ⑥ TRAITEMENT — |A ∩ B| ÷ min(|A|, |B|).
    ⑦ UNITÉ — Une part.
    ⑧ POURQUOI — La plus petite au dénominateur : une stratégie entièrement contenue dans une autre est un doublon, même
      si l'autre joue aussi ailleurs (collège, §3, lecture 3 : tp 2 % contre tp 8 %, corrélées à 0,35 seulement).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si une stratégie n'a aucun jour de position.
      [sort: non]
    """
    a, b = set(jours_a), set(jours_b)
    if not a or not b:
        raise ValueError("une stratégie sans aucun jour de position : chevauchement indéfini")
    return len(a & b) / min(len(a), len(b))


def se_ressemblent(gains_a, gains_b, jours_a, jours_b, table):
    """Dit si deux stratégies font le même pari, au sens de la mise en service (A-791).

    ① RÔLE — Appliquer la définition décidée : corrélation ≥ seuil OU chevauchement ≥ seuil.
    ② CONTEXTE D'APPEL — `mettre_en_service` ; les épreuves.
    ③ ENTRÉE — `gains_a`, `gains_b` : les gains alignés · `jours_a`, `jours_b` : les jours de position des deux
      stratégies · `table` : la table des seuils.
    ④ CONDITIONS D'ENTRÉE — Celles de `correlation_des_gains` et de `chevauchement`.
    ⑤ SORTIE — UNE valeur : {"correlation", "chevauchement", "semblables" (booléen), "par" (les critères atteints)}.
      [rend: 1]
    ⑥ TRAITEMENT — les deux mesures, puis les deux comparaisons « ≥ ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « ≥ » : la loi dit « 0,5 ou plus » et « au moins une fois sur deux » ; le collège écrit « ≥ 0,5 » dans sa
      définition et son script (`combine.py` : semblables sauf si ρ < 0,5 et chevauchement < 0,5).
    ⑨ CE QUI CLOCHE — Le collège écrit aussi « plus d'une fois sur deux » (§3, lecture 1) : l'égalité exacte à 0,5 est
      tranchée ici par la définition, signalé dans la note.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    s_rho, s_chev = seuils_de_ressemblance(table)
    rho = correlation_des_gains(gains_a, gains_b)
    chev = chevauchement(jours_a, jours_b)
    par = [c for c, oui in (("correlation", rho >= s_rho), ("chevauchement", chev >= s_chev)) if oui]
    return {"correlation": rho, "chevauchement": chev, "semblables": bool(par), "par": par}


def mettre_en_service(candidats, table):
    """Choisit, par ordre de mérite, les stratégies qui entrent en service sans jamais deux qui font le même pari.

    ① RÔLE — La règle gloutonne de l'étape 6 ⑤ : « elles entrent en service par ordre de mérite, chacune seulement si elle
      ne ressemble à aucune déjà en service » (A-791).
    ② CONTEXTE D'APPEL — Destiné à la mise en service (étape 6), après les contrôles ① à ④ ; les épreuves.
    ③ ENTRÉE — `candidats` : liste DÉJÀ RANGÉE par ordre de mérite (étape 6, point 4, A-797 : d'abord le plus petit creux, puis
      la meilleure probabilité de réussite, calculé ailleurs), chaque élément {"id", "gains" (alignés), "jours"} ·
      `table` : la table des seuils.
    ④ CONDITIONS D'ENTRÉE — identifiants distincts ; séries de même longueur.
    ⑤ SORTIE — DEUX valeurs : la liste des identifiants en service, dans l'ordre ; {identifiant écarté : (identifiant en
      service auquel il ressemble, mesure)}.
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque candidat dans l'ordre : comparer à chacun de ceux déjà en service ; au premier semblable,
      l'écarter (il reste mesuré, collège §4 point 4) ; sinon, l'ajouter.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Pas de grappes : « pas d'algorithme instable ni d'enchaînement (A ressemble à B, B à C, mais A pas à C) »
      (collège, §4 point 4).
    ⑨ CE QUI CLOCHE — Le mérite n'est pas calculé ici (A-797) : un ordre faux donne un service faux.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError.
      [sort: non]
    """
    ids = [c["id"] for c in candidats]
    if len(ids) != len(set(ids)):
        raise ValueError("identifiants en double parmi les candidats")
    en_service, ecartes = [], {}
    for c in candidats:
        for s in en_service:
            m = se_ressemblent(c["gains"], s["gains"], c["jours"], s["jours"], table)
            if m["semblables"]:
                ecartes[c["id"]] = (s["id"], m)
                break
        else:
            en_service.append(c)
    return [c["id"] for c in en_service], ecartes


# ------------------------------------------------------------------------------------------------------------------
# LE CALIBRAGE SUR C5 (2024-2026, années de RÉGLAGE de C5 : aucun regard sur des années d'examen, préambule du plan §4)
# ------------------------------------------------------------------------------------------------------------------

def _preparer_c5(racine):
    """Rend ce qu'il faut pour rejouer les versions de C5E10-OBS-V1 E01 comme l'expert (preparer.py), sur une racine.

    ① RÔLE — Reprendre la préparation de l'expert (lecteur de cours, référentiel, module des positions, fiche mère).
    ② CONTEXTE D'APPEL — `_jouer_les_versions_de_c5`.
    ③ ENTRÉE — `racine` : la racine d'une COPIE du dépôt.
    ④ CONDITIONS D'ENTRÉE — donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv et son témoin ; le registre.
    ⑤ SORTIE — UNE valeur : un dictionnaire (J, JV, versions, temoin, cours, lecture, mnemo, mod_pos, fiche).
      [rend: 1]
    ⑥ TRAITEMENT — les appels de preparer.py, chemin changé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les mêmes fonctions du juge que l'expert (R-708) : 0 écart au témoin est la preuve.
    ⑨ CE QUI CLOCHE — Le lecteur lit le fichier de cours du jour (donnees/cours_maitre.csv, qui grandit) : la période du
      témoin borne le jeu ; une révision du passé changerait le jeu, et l'écart au témoin le dirait.
    ⑩ EFFET — Lit des fichiers ; ajoute programmes/ au chemin d'import.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import csv
    dossier = os.path.join(racine, "programmes")
    if dossier not in sys.path:
        sys.path.insert(0, dossier)
    import JOUER_LES_VERSIONS as JV
    import JUGE_DES_STRATEGIES as J
    import CONTRATS_DES_FICHIERS as contrat
    base = os.path.join(racine, "donnees", "combinatoires")
    with open(os.path.join(base, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"), encoding="utf-8-sig") as f:
        versions = list(csv.DictReader(f))
    with open(os.path.join(base, "TEMOIN_RESULTATS_C5E10-OBS-V1_E01.csv"), encoding="utf-8-sig") as f:
        temoin = {r["id_version"]: r for r in csv.DictReader(f)}
    mnemo = J.table_mnemoniques(J.trouver(racine, "REFERENTIEL_VALEURS"))
    cours, lecture = J.lire_par_le_lecteur(racine, os.path.relpath(J.fichiers_de_cours(racine)[0], racine), mnemo)
    mod_pos = J.charger_module(J.trouver(racine, "MODULE_POSITIONS.py"), "pos")
    fiche = contrat.fiches_du_registre(J.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES)).get("C5E10-OBS-V1")
    return {"J": J, "JV": JV, "versions": versions, "temoin": temoin, "cours": cours, "lecture": lecture,
            "mnemo": mnemo, "mod_pos": mod_pos, "fiche": fiche, "racine": racine}


_ETAT = {}


def _jouer_une(v):
    """Joue UNE version de C5 et la confronte au témoin (fonction de processus, état lu dans `_ETAT`).

    ① RÔLE — Le geste de jouer_toutes.py pour une version.
    ② CONTEXTE D'APPEL — `_jouer_les_versions_de_c5`, directement ou par un processus fils.
    ③ ENTRÉE — `v` : une ligne de la combinatoire.
    ④ CONDITIONS D'ENTRÉE — `_ETAT["p"]` posé par `_preparer_c5`.
    ⑤ SORTIE — TROIS valeurs : l'identifiant, les opérations, vrai si nombre d'opérations et gain net égalent le témoin.
      [rend: 3]
    ⑥ TRAITEMENT — fusionner la fiche et la version, signal, `J.jouer` sur la période et au barème du témoin.
    ⑦ UNITÉ — Euros (gain net).
    ⑧ POURQUOI — Tolérance 0,006 € : celle de l'expert (jouer_toutes.py).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève AssertionError si une valeur est inconnue du juge.
      [sort: non]
    """
    p = _ETAT["p"]
    J, t = p["J"], p["temoin"][v["id_version"]]
    f = p["JV"].fusionner(p["fiche"], v)
    J.porte_0(f)
    ops, inconnus = J.jouer(f, p["cours"], p["mnemo"], J.signal_de_la_fiche(p["racine"], f), p["mod_pos"],
                            periode=(t["periode_debut"], t["periode_fin"]), lecture=p["lecture"], bareme=t["bareme"])
    assert not inconnus, inconnus
    r = J.resumer(ops)
    ok = str(r["n"]) == t["operations"] and abs((r.get("net", 0.0) if r["n"] else 0.0) - float(t["gain_net_euros"])) < 0.006
    return v["id_version"], ops, ok


def _initialiser(racine):
    """Pose l'état de préparation dans un processus (initialiseur du lot de processus).
    ① RÔLE — Préparer une fois par processus.
    ② CONTEXTE D'APPEL — `multiprocessing.Pool(initializer=…)` ; `_jouer_les_versions_de_c5`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Ne rend rien.
      [rend: rien]
    ⑥ TRAITEMENT — `_ETAT["p"] = _preparer_c5(racine)`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les processus fils ne partagent pas la mémoire du père.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit `_ETAT`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    _ETAT["p"] = _preparer_c5(racine)


def _jouer_les_versions_de_c5(racine, raccourci, processus):
    """Rejoue les 2 695 versions de C5E10-OBS-V1 E01 (ou les 2 450 « une valeur seule », en raccourci) et rend leurs opérations.

    ① RÔLE — Retrouver le matériau de l'expert : les opérations de chaque version, 0 écart au témoin.
    ② CONTEXTE D'APPEL — `calibrer_sur_c5`.
    ③ ENTRÉE — `racine` · `raccourci` : vrai pour ne jouer que les versions à une valeur et reconstituer l'univers
      entier · `processus` : nombre de processus.
    ④ CONDITIONS D'ENTRÉE — Celles de `_preparer_c5`.
    ⑤ SORTIE — QUATRE valeurs : {identifiant : opérations}, la liste des versions (lignes de la combinatoire), une liste
      de lignes de compte rendu, et le nombre total d'écarts (témoin, somme, rejeu direct).
      [rend: 4]
    ⑥ TRAITEMENT — ① jouer (en raccourci : les versions sans virgule dans l'univers) · ② compter les écarts au témoin ·
      ③ en raccourci : pour CHACUNE des 245 versions « univers entier », vérifier au témoin que nombre d'opérations et
      gain net sont la somme de ses 10 valeurs seules, puis rejouer directement 15 d'entre elles (tirées avec la graine)
      et vérifier que leurs opérations sont exactement la réunion de celles des valeurs seules ; enfin poser cette
      réunion comme opérations de la version.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Rejouer les 2 695 versions dépasse 2 minutes sur la machine du Chat (mesuré : 0,5 s par version à 10
      valeurs) ; l'expert a mesuré « UNIVERS ENTIER = SOMME DES 10 VALEURS SEULES : écart max 0.000000 EUR/jour » en
      jetons illimités. Le raccourci repose sur cette identité, VÉRIFIÉE à chaque passage (③), jamais supposée.
    ⑨ CE QUI CLOCHE — En raccourci, 230 des 245 versions « univers entier » ne sont pas rejouées directement : seule leur
      somme au témoin est vérifiée. Le passage complet (sans raccourci) se joue sur GitHub.
    ⑩ EFFET — Lance des processus fils ; lit des fichiers.
    ⑪ TERMINAISON — Rend la main ; un processus fils bloqué ne rendrait pas la main (aucun délai posé).
      [sort: non]
    """
    import random
    from multiprocessing import Pool
    _initialiser(racine)
    p = _ETAT["p"]
    versions, temoin = p["versions"], p["temoin"]
    a_jouer = [v for v in versions if not raccourci or "," not in v["univers"]]
    if processus > 1:
        with Pool(processus, initializer=_initialiser, initargs=(racine,)) as pool:
            res = pool.map(_jouer_une, a_jouer, chunksize=25)
    else:
        res = [_jouer_une(v) for v in a_jouer]
    ops = {vid: o for vid, o, _ in res}
    lignes = ["JOUÉES : %d versions ; écarts au témoin : %d" % (len(res), sum(not ok for _, _, ok in res))]
    ecarts = sum(not ok for _, _, ok in res)
    if raccourci:
        cle = {(v["tp"], v["sl"], v["horizon"], v["univers"]): v["id_version"] for v in versions}
        entieres = [v for v in versions if "," in v["univers"]]
        e_t = 0
        for v in entieres:
            ids = [cle[(v["tp"], v["sl"], v["horizon"], m)] for m in v["univers"].split(",")]
            n = sum(int(temoin[i]["operations"]) for i in ids)
            g = sum(float(temoin[i]["gain_net_euros"]) for i in ids)
            t = temoin[v["id_version"]]
            if n != int(t["operations"]) or abs(g - float(t["gain_net_euros"])) > 0.006 * len(ids):
                e_t += 1
        random.seed(GRAINE)
        echantillon = random.sample(entieres, 15)

        def forme(o):
            """Écrit une opération sous une forme comparable.
            ① RÔLE — Comparer deux listes d'opérations sans dépendre de l'ordre.
            ② CONTEXTE D'APPEL — `_jouer_les_versions_de_c5`.
            ③ ENTRÉE — `o` : une opération.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : un tuple trié de (clé, valeur arrondie au millionième).
              [rend: 1]
            ⑥ TRAITEMENT — trier les clés, arrondir les flottants.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Les flottants d'une somme peuvent différer au dernier chiffre.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]"""
            return tuple(sorted((k, round(x, 6) if isinstance(x, float) else x) for k, x in o.items()))
        e_d = 0
        for v in echantillon:
            _vid, directes, ok = _jouer_une(v)
            union = [o for m in v["univers"].split(",") for o in ops[cle[(v["tp"], v["sl"], v["horizon"], m)]]]
            if not ok or sorted(map(forme, directes)) != sorted(map(forme, union)):
                e_d += 1
        for v in entieres:
            ops[v["id_version"]] = sorted(
                (o for m in v["univers"].split(",") for o in ops[cle[(v["tp"], v["sl"], v["horizon"], m)]]),
                key=lambda o: (o["date_entree"], o["valeur"]))
        lignes.append("RACCOURCI : %d versions univers entier ; écarts au témoin à la somme des 10 valeurs seules : %d ; "
                      "rejeu direct de 15 (graine %d) : opérations différentes de la réunion : %d" % (len(entieres), e_t,
                                                                                                  GRAINE, e_d))
        ecarts += e_t + e_d
    lignes.append("ÉCARTS TOTAUX : %d" % ecarts)
    return ops, versions, lignes, ecarts


def _un_jeton(ops):
    """Rend les opérations qu'un seul jeton aurait prises : une opération n'entre qu'après la sortie de la précédente.

    ① RÔLE — Le mode « un jeton » du collège, reconstruit depuis les opérations (`un_jeton` de ressemblance.py).
    ② CONTEXTE D'APPEL — `calibrer_sur_c5`.
    ③ ENTRÉE — `ops` : les opérations en jetons illimités.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste retenue.
      [rend: 1]
    ⑥ TRAITEMENT — tri par (entrée, valeur) ; garder si l'entrée est STRICTEMENT après la dernière sortie gardée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Reproduire les chiffres du collège ; le collège l'écrit lui-même « reconstruit depuis les opérations,
      pas tiré de MODULE_POSITIONS » (§6 (f)).
    ⑨ CE QUI CLOCHE — Calibrage seulement : en service, le mode un jeton vient du circuit, pas de cette fonction.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    gardees, fin = [], ""
    for o in sorted(ops, key=lambda x: (x["date_entree"], x["valeur"])):
        if o["date_entree"] > fin:
            gardees.append(o)
            fin = o["date_sortie"]
    return gardees


def _serie_valorisee_chaque_soir(ops, close, dates_m, rang):
    """Rend le gain quotidien en euros d'une liste d'opérations, valorisé chaque soir à la clôture (méthode de l'expert).

    ① RÔLE — Fabriquer la série de l'expert (jouer_toutes.py) pour le SEUL calibrage.
    ② CONTEXTE D'APPEL — `calibrer_sur_c5`.
    ③ ENTRÉE — `ops` · `close` : {valeur : {date : clôture}} · `dates_m` : {valeur : séances du calendrier} · `rang` :
      {date : rang dans le calendrier}.
    ④ CONDITIONS D'ENTRÉE — numpy.
    ⑤ SORTIE — UNE valeur : le tableau des gains, une case par séance.
      [rend: 1]
    ⑥ TRAITEMENT — quantité = 100 000 ÷ prix d'entrée ; chaque séance tenue, quantité × (clôture − précédente), le prix
      de sortie le jour de sortie ; frais retirés le jour de sortie.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — L'expert l'a contrôlée : « la série quotidienne reconstruite redonne le gain net de chaque version (écart
      max 0,000000 €) » ; le calibrage refait ce contrôle.
    ⑨ CE QUI CLOCHE — SECONDE fabrication d'une courbe de compte (la première sera celle du lot W2b, A-1071) : à
      remplacer dès qu'elle existe (R-708).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import numpy as np
    s = np.zeros(len(rang))
    for o in ops:
        q, m, prec = 100000.0 / o["pe"], o["valeur"], o["pe"]
        for d in dates_m[m]:
            if o["date_entree"] <= d <= o["date_sortie"]:
                c = o["px"] if d == o["date_sortie"] else close[m][d]
                s[rang[d]] += q * (c - prec)
                prec = c
        s[rang[o["date_sortie"]]] -= o["frais"]
    return s


def calibrer_sur_c5(racine, raccourci=True, processus=2):
    """Reproduit les chiffres publiés de l'expert et du collège du 14-11-2026 sur C5, et dit s'ils sont reproduits.

    ① RÔLE — Le CALIBRAGE OBLIGATOIRE avant tout usage des deux mesures (mandat du lot W2c ; préférences §9bis).
    ② CONTEXTE D'APPEL — `main` (« --calibrer-c5 ») ; l'épreuve longue « EssaisRessemblance » sur GitHub (sans raccourci).
    ③ ENTRÉE — `racine` : une COPIE du dépôt · `raccourci` · `processus`.
    ④ CONDITIONS D'ENTRÉE — Celles de `_preparer_c5` ; numpy.
    ⑤ SORTIE — DEUX valeurs : vrai si TOUT est reproduit, et la liste des lignes du compte rendu.
      [rend: 2]
    ⑥ TRAITEMENT — ① rejouer (0 écart exigé) · ② calendrier de l'expert (séances des valeurs jouées, de la date de début du
      témoin à la dernière sortie), séries valorisées chaque soir, reconstruction du gain net exigée au centime ·
      ③ statistiques des corrélations des paires (chiffres sans hasard, égaux à la précision publiée) · ④ k par
      `mesurer_le_nombre_effectif` au risque lu à la loi (k plein à ±5 % de 168 ; k prudent dans [140, 178,5]) ·
      ⑤ ressemblance en un jeton : tp 2 % / 3 % et 2 % / 8 % (univers entier, sl 2,5 %, 20 séances), DG / TTE (tp 4 %,
      sl 2,5 %, 20 séances), à 0,005 près.
    ⑦ UNITÉ — Euros pour les séries ; essais pour k.
    ⑧ POURQUOI — Les références sont REFERENCES_DU_CALIBRAGE (tête du fichier, avec leurs sources).
      IND-001-RETEST n'est PAS rejouée : sur 2024-2026 elle serait jouée sur ses propres années d'examen (les 30 % des 20
      ans), interdit par le préambule du plan (§4) ; le chiffre du collège « 0,26 ; 21 % » reste donc non reproduit.
    ⑨ CE QUI CLOCHE — Les chiffres du collège ne portent que sur 2024-2026 (644 séances) : le calibrage prouve le
      programme, pas la valeur de la mesure sur les 20 ans.
    ⑩ EFFET — Lance des processus ; lit des fichiers ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; un processus fils bloqué ne rendrait pas la main.
      [sort: non]
    """
    import time
    import numpy as np
    debut = time.time()
    ops, versions, lignes, ecarts = _jouer_les_versions_de_c5(racine, raccourci, processus)
    lignes.append("durée du jeu : %.1f s" % (time.time() - debut))
    ok = ecarts == 0
    p = _ETAT["p"]
    t0 = next(iter(p["temoin"].values()))
    ids = [v["id_version"] for v in versions]
    valeurs = sorted({o["valeur"] for v in ids for o in ops[v]})
    fin = max(o["date_sortie"] for v in ids for o in ops[v])
    cal = sorted({b["date"] for m in valeurs for b in p["cours"][m] if t0["periode_debut"] <= b["date"] <= fin})
    rang = {d: i for i, d in enumerate(cal)}
    close = {m: {b["date"]: b["close"] for b in p["cours"][m]} for m in valeurs}
    dates_m = {m: [d for d in sorted(close[m]) if d in rang] for m in valeurs}
    X = np.array([_serie_valorisee_chaque_soir(ops[v], close, dates_m, rang) for v in ids])
    recon = max(abs(X[j].sum() - sum(o["net"] for o in ops[v])) for j, v in enumerate(ids))
    lignes.append("CALENDRIER : %d séances %s -> %s ; reconstruction max |somme série - gain net| = %.6f EUR"
                  % (len(cal), cal[0], cal[-1], recon))
    ok = ok and recon < 0.01
    R = np.corrcoef(X)
    iu = np.triu_indices(len(ids), 1)
    stats = {"correlation_mediane": float(np.median(R[iu])), "correlation_moyenne": float(R[iu].mean()),
             "part_au_dessus_de_0_9": float((R[iu] > 0.9).mean()), "part_sous_0_1": float((R[iu] < 0.1).mean())}
    ref = REFERENCES_DU_CALIBRAGE
    for c, x in stats.items():
        bon = abs(x - ref[c][0]) <= ref[c][1]
        ok = ok and bon
        lignes.append("%-24s %.4f (publié %.3f) %s" % (c, x, ref[c][0], "REPRODUIT" if bon else "ÉCART"))
    alpha = risque_global(lire_les_seuils(racine))
    t = time.time()
    m = mesurer_le_nombre_effectif(X, alpha)
    kb = m["k_par_reechantillonnage"]
    bon_plein = abs(m["k_plein"] - ref["k_plein"][0]) <= ref["k_plein"][1]
    bon_prudent = ref["k_prudent_bas"] <= m["k_prudent"] <= ref["k_prudent_haut"]
    ok = ok and bon_plein and bon_prudent
    lignes.append("k : risque lu à la loi %.4g ; barre %.3f (publié 3.434) ; k plein %.1f (publié 168) %s ; "
                  "rééchantillonné de %.0f à %.0f, médiane %.0f (publié 119 à 156, médiane 137) ; k prudent %.1f %s (%.0f s)"
                  % (alpha, m["barre_pleine"], m["k_plein"], "REPRODUIT" if bon_plein else "ÉCART", min(kb), max(kb),
                     float(np.median(kb)), m["k_prudent"], "dans [140 ; 178,5]" if bon_prudent else "HORS DE [140 ; 178,5]",
                     time.time() - t))
    cle = {(v["tp"], v["sl"], v["horizon"], v["univers"]): v["id_version"] for v in versions}
    entier = next(v["univers"] for v in versions if "," in v["univers"])
    table = lire_les_seuils(racine)
    for nom, a, b in (("tp2_tp3", ("0.02", "0.025", "20", entier), ("0.03", "0.025", "20", entier)),
                      ("tp2_tp8", ("0.02", "0.025", "20", entier), ("0.08", "0.025", "20", entier)),
                      ("dg_tte", ("0.04", "0.025", "20", "DG"), ("0.04", "0.025", "20", "TTE"))):
        va, vb = cle[a], cle[b]
        oa, ob = _un_jeton(ops[va]), _un_jeton(ops[vb])
        mesure = se_ressemblent(list(_serie_valorisee_chaque_soir(oa, close, dates_m, rang)),
                                list(_serie_valorisee_chaque_soir(ob, close, dates_m, rang)),
                                jours_en_position(oa, dates_m), jours_en_position(ob, dates_m), table)
        rho_p, chev_p = ref[nom]
        bon = (abs(mesure["correlation"] - rho_p) <= ref["precision_ressemblance"]
               and abs(mesure["chevauchement"] - chev_p) <= ref["precision_ressemblance"])
        ok = ok and bon
        lignes.append("RESSEMBLANCE %s (%s contre %s, un jeton) : ρ = %.3f (publié %.2f) · chevauchement = %.3f (publié "
                      "%.2f) · semblables : %s %s" % (nom, va, vb, mesure["correlation"], rho_p, mesure["chevauchement"],
                                                     chev_p, mesure["semblables"], "REPRODUIT" if bon else "ÉCART"))
    lignes.append("CALIBRAGE : %s (durée totale %.0f s)" % ("REPRODUIT" if ok else "NON REPRODUIT", time.time() - debut))
    return ok, lignes


def main(argv):
    """La ligne de commande : « <racine> --calibrer-c5 [--raccourci] [--processus=N] ».

    ① RÔLE — Lancer le calibrage et rendre un code de sortie qui peut rougir (R-734).
    ② CONTEXTE D'APPEL — À la main ; l'épreuve longue « EssaisRessemblance ».
    ③ ENTRÉE — `argv` : les arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Ne rend rien : sort par 0 (reproduit), 1 (non reproduit), 2 (impossible).
      [rend: rien]
    ⑥ TRAITEMENT — lire les arguments ; `calibrer_sur_c5` ; afficher le compte rendu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un calibrage qui n'a pas pu tourner ne doit jamais sortir en 0.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche ; lance le calibrage.
    ⑪ TERMINAISON — SORT DU PROGRAMME par sys.exit.
      [sort: oui]
    """
    args = [a for a in argv if not a.startswith("--")]
    options = [a for a in argv if a.startswith("--")]
    processus = 2
    for o in options:
        if o.startswith("--processus="):
            processus = int(o.split("=", 1)[1])
        elif o not in ("--calibrer-c5", "--raccourci"):
            print("option inconnue : %s" % o)
            sys.exit(2)
    if len(args) != 1 or "--calibrer-c5" not in options:
        print(__doc__.split("②")[1].split("③")[0])
        sys.exit(2)
    try:
        ok, lignes = calibrer_sur_c5(os.path.abspath(args[0]), "--raccourci" in options, processus)
    except Exception as e:  # R-734 : tout échec est un code non nul, jamais un 0
        print("CALIBRAGE IMPOSSIBLE : %s : %s" % (type(e).__name__, e))
        sys.exit(2)
    print("\n".join(lignes))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
