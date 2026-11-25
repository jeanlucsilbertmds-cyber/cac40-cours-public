#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVE DE CALIBRAGE DE LA MÉTHODE DES 30 % (ARBITRAGE du 14-11-2026, étape 6, correction C6) — Simulation uniquement.
Mercredi 25-11-2026.

LE SENS EN TÊTE — Au regard unique sur les 30 %, m versions d'une famille sont jugées ensemble, et le contrôle ⑤
(« le gain bat zéro ») se décide par `MODULE_JUGEMENT.romano_wolf_du_gain`, qui promet : « si aucune version n'a de
talent, je n'en validerai au moins une qu'au plus une fois sur 1 ÷ seuil ». Cette promesse n'est prouvée qu'en grand
échantillon (Romano et Wolf 2005). Ce programme la MESURE à nos tailles (50 à 250 opérations par version), avec des
gains dissymétriques (+1/−3) et des opérations LIÉES PAR PAQUETS — c'est là que la contre-expertise du 14-11-2026 a
mesuré 10 à 17 % au lieu de 5 % pour un écart-type ordinaire (C6 : « c'est là qu'elle peut rougir »). L'arbitre exige un
risque ≤ 2,5 % par famille ; s'il est dépassé, on studentise autrement (variance robuste à la dépendance) et on relance.
Données FABRIQUÉES : formes de gains écrites ici, dates fictives à partir du 2024-01-01 ; aucun cours n'est lu, et
surtout aucune année de 2000 à 2023.

USAGE : python3 -B programmes/CALIBRER_LA_METHODE_DES_30.py <racine> [mondes par case, défaut 1000] [seuil]
        python3 -B programmes/CALIBRER_LA_METHODE_DES_30.py <racine> --famille <mondes par case> <seuil par contrôle>
  Le mode « --famille » (décision de Jean-Luc du 25-11-2026, 15h36, « 1 ») mesure le taux de FAUSSES GAGNANTES d'une
  famille jugée par ⑤ ET ⑥ ensemble, au pire cas de l'arbitre (voir `mesurer_la_famille`).
CODE : 0 si chaque case EXIGÉE tient le seuil ; 1 si l'une le dépasse de façon démontrée ; 2 si une donnée manque, si
un argument est faux ou si une case n'a pas pu se mesurer (R-734).

① RÔLE — Mesurer le taux de familles « sans talent » où au moins une version est validée à tort, et sortir non nul
  s'il dépasse le seuil promis.
② CONTEXTE D'APPEL — Avant tout regard sur des années d'examen d'une famille (étape 6 de l'ARBITRAGE), et après toute
  modification de `romano_wolf_du_gain`. Trop long pour la machine du Chat : joué sur GitHub, code `CalibrageDes30`
  de `tests/LANCEMENT_DES_EPREUVES.json` (« epreuves_longues »). Les épreuves rapides, dont les dents de ce calibrage
  (E8), vivent dans `tests/EPREUVES_DE_LA_METHODE_DES_30_Mer_25-11-2026.py`.
③ ENTRÉE — La racine du dépôt ; facultatifs : le nombre de mondes par case (entier ≥ 50), le seuil (dans ]0, 0,5[ ;
  par défaut `MODULE_JUGEMENT.SEUIL_PAR_FAMILLE_DEFAUT`, dont la valeur revient à Jean-Luc).
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/MODULE_JUGEMENT.py` et `programmes/CALIBRER_LE_HASARD_DES_GAINS.py`.
  Sinon code 2.
⑤ SORTIE — Le code de sortie dit en « CODE ». À l'écran : une ligne par case (taux mesuré, verdict), le verdict d'ensemble.
  [rend: 1]
⑥ TRAITEMENT — ① lire les arguments · ② pour chaque forme, chaque taille, chaque liaison et chaque ressemblance :
  fabriquer des familles sans talent (`fabriquer_une_famille`), les juger par `romano_wolf_du_gain`, compter
  (`mesurer_le_risque`) · ③ juger chaque case exigée (`verdict_d_une_case`) · ④ rendre le code.
⑦ UNITÉ — Gains en EUROS pour 100 000 € par opération ; jours de CALENDRIER ; taux sans unité.
⑧ POURQUOI — Une promesse de risque se mesure, elle ne se suppose pas (même principe que
  `programmes/CALIBRER_LE_HASARD_DES_GAINS.py`, qui calibre une version seule ; ici, une FAMILLE). La ressemblance
  0,96 est celle de deux versions à un cran de réglage (méthode « au carré », §A.4) ; le maximum de Romano et Wolf doit
  en tenir compte sans dépasser son seuil.
⑨ CE QUI CLOCHE — ① Monde stylisé : copule normale par paquets ; un krach réel peut lier autrement. ② Le régime
  persistant (0,8 d'un paquet au suivant) est AFFICHÉ, non exigé : aucune méthode qui ne regarde qu'une période ne voit
  un régime aussi long qu'elle (`probabilite_que_le_gain_soit_du_hasard`, ⑨ ①). ③ « Dépasse de façon démontrée » est
  un test binomial unilatéral à 0,001 : un dépassement léger peut passer inaperçu à 1 000 mondes. ④ Le contrôle ⑥
  (Holm sur des p de tirage) n'est pas calibré seul : ses p sont exacts par construction ; il n'est mesuré qu'avec ⑤,
  dans le mode « --famille ». ⑤ Durée NON MESURÉE en entier
  sur la machine du Chat (seul un essai réduit l'a été).
⑩ EFFET — N'écrit aucun fichier ; affiche.
⑪ TERMINAISON — Rend un code de sortie. Boucles bornées par le nombre de cases, de mondes et de tirages. Aucun appel ne
  peut ne pas revenir.
  [sort: oui — code de sortie]
⑫ DÉFINITIONS
  une famille sans talent : m versions dont le vrai gain moyen par opération est nul
  un faux gagnant : une version de cette famille validée par `romano_wolf_du_gain`
  une case : forme × taille × liaison × ressemblance
"""
import datetime
import importlib.util
import math
import os
import random
import sys
import zlib
from statistics import NormalDist

sys.dont_write_bytecode = True

DEBUT = datetime.date(2024, 1, 1)                     # dates fictives, 2024 et après (aucune année 2000-2023)
PERIODE_JOURS = 900                                   # ≈ 2,5 ans
VERSIONS_PAR_FAMILLE = 10
TAILLES = (50, 250)                                   # les deux bords de « 50 à 250 observations » (ARBITRAGE, étape 6)
# liaison : (taille des paquets, corrélation dans un paquet, persistance d'un paquet au suivant, exigée ?)
LIAISONS = {
    "indépendantes": (1, 0.0, 0.0, True),
    "paquets de 10 liés (0,36)": (10, 0.36, 0.0, True),
    "régime persistant (0,8) — affiché": (10, 0.36, 0.8, False),
}
RESSEMBLANCES = {"versions indépendantes": 0.0, "versions ressemblantes (0,96)": 0.96}
NIVEAU_DE_L_ALERTE = 0.001


def fabriquer_les_formes():
    """Fabrique les formes de gains, chacune recentrée sur un gain moyen exactement nul.

    ① RÔLE — Donner aux familles des gains dissymétriques, sans lire aucun cours.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : dictionnaire nom → liste triée de (gain en euros, durée en jours).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque forme (objectif, stop, part gagnante, durée) : 400 opérations régulièrement réparties
      entre gains et pertes, avec un petit écart déterministe ; puis retrancher la moyenne ; trier par gain.
    ⑦ UNITÉ — EUROS pour 100 000 € ; JOURS.
    ⑧ POURQUOI — « +1/−3 » est la forme qui trompe le plus Student (méthode « au carré », §7.1) ; « +4/−2,5 » est
      celle de C5 ; le tri permet la copule (rang ↔ gain).
    ⑨ CE QUI CLOCHE — Formes stylisées, pas mesurées sur des cours.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    formes = {}
    for nom, objectif, stop, gagnantes, duree in (("+1/-3 (10 jours)", 1000.0, 3000.0, 300, 10),
                                                  ("+4/-2,5 (20 jours)", 4000.0, 2500.0, 154, 20)):
        brut = [(objectif + 10.0 * (k % 15) - 70.0, duree) for k in range(gagnantes)]
        brut += [(-stop + 20.0 * (k % 15) - 140.0, duree) for k in range(400 - gagnantes)]
        moyenne = math.fsum(g for g, _ in brut) / len(brut)
        formes[nom] = sorted((g - moyenne, d) for g, d in brut)
    return formes


def fabriquer_une_famille(hasard, forme, n, m, liaison, ressemblance):
    """Fabrique une famille de m versions SANS TALENT, de n opérations chacune.

    ① RÔLE — Le monde simulé d'une case.
    ② CONTEXTE D'APPEL — `mesurer_le_risque`, une fois par monde.
    ③ ENTRÉE — `hasard` : un `random.Random` · `forme` : liste triée (gain, durée) · `n`, `m` : entiers ≥ 2 et ≥ 1 ·
      `liaison` : une valeur de LIAISONS · `ressemblance` : corrélation des gains entre versions, dans [0, 1[.
    ④ CONDITIONS D'ENTRÉE — Celles de ③.
    ⑤ SORTIE — UNE valeur : dictionnaire nom → opérations (`net`, `date_entree`, `date_sortie`).
      [rend: 1]
    ⑥ TRAITEMENT — ① tirer des jours de départ de paquets et, par opération, un z de base (facteur commun du paquet,
      qui suit le précédent avec la persistance, plus un bruit) · ② si `ressemblance` > 0 : toutes les versions
      gardent ces jours, et la version i prend le gain de rang Φ(√r × z + √(1 − r) × bruit_i) ; sinon chaque version
      est tirée à part · ③ convertir en opérations datées à partir de `DEBUT`.
    ⑦ UNITÉ — EUROS ; JOURS.
    ⑧ POURQUOI — Copule normale : garde exactement la forme (donc un gain moyen nul) tout en liant les gains d'un
      paquet et ceux de versions voisines (mêmes jours, gains très corrélés) — le cas des versions à un cran.
    ⑨ CE QUI CLOCHE — `CALIBRER_LE_HASARD_DES_GAINS.fabriquer_une_strategie` fait la même chose pour une version : elle
      n'est pas réutilisée, car elle ne rend pas les z dont la ressemblance a besoin.
    ⑩ EFFET — Aucun (consomme le hasard reçu).
    ⑪ TERMINAISON — Rend la main. Boucles bornées par n × m. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    phi = NormalDist().cdf
    paquet, rho, persistance, _exigee = liaison
    taille = len(forme)

    def jours_et_z():
        """Tire les jours d'entrée et les z d'une version.

        ① RÔLE — Le tirage de base d'une version.
        ② CONTEXTE D'APPEL — `fabriquer_une_famille`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : liste de n couples (jour, z).
          [rend: 1]
        ⑥ TRAITEMENT — Départs de paquets triés ; facteur commun u qui suit le précédent ; z = √rho × u + bruit.
        ⑦ UNITÉ — Jours depuis `DEBUT` ; z sans unité.
        ⑧ POURQUOI — Voir `fabriquer_une_famille`, ⑧.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Consomme le hasard de la fonction qui l'entoure.
        ⑪ TERMINAISON — Rend la main ; boucles bornées par n. Aucun appel ne peut ne pas revenir.
          [sort: non]
        """
        sortie = []
        departs = sorted(hasard.randrange(PERIODE_JOURS - paquet - 40) for _ in range(-(-n // paquet)))
        u = hasard.gauss(0.0, 1.0)
        for rang, depart in enumerate(departs):
            if rang:
                u = persistance * u + math.sqrt(1.0 - persistance * persistance) * hasard.gauss(0.0, 1.0)
            for k in range(paquet):
                if len(sortie) < n:
                    sortie.append((depart + k, math.sqrt(rho) * u + math.sqrt(1.0 - rho) * hasard.gauss(0.0, 1.0)))
        return sortie

    base = jours_et_z()
    famille = {}
    for i in range(m):
        if ressemblance > 0.0:
            vues = [(j, math.sqrt(ressemblance) * z + math.sqrt(1.0 - ressemblance) * hasard.gauss(0.0, 1.0))
                    for j, z in base]
        else:
            vues = base if i == 0 else jours_et_z()
        ops = []
        for j, z in vues:
            gain, duree = forme[min(taille - 1, int(phi(z) * taille))]
            ops.append({"net": gain, "date_entree": (DEBUT + datetime.timedelta(days=j)).isoformat(),
                        "date_sortie": (DEBUT + datetime.timedelta(days=j + duree - 1)).isoformat()})
        famille["v%02d" % i] = ops
    return famille


def mesurer_le_risque(methode, fabriquer, mondes, seuil):
    """Compte les mondes où une méthode valide au moins une version d'une famille sans talent.

    ① RÔLE — Le cœur du calibrage, séparé de la méthode jugée pour que l'épreuve E8 puisse lui donner une méthode
      fausse et vérifier qu'il la voit.
    ② CONTEXTE D'APPEL — `main`, une fois par case ; l'épreuve E8.
    ③ ENTRÉE — `methode` : fonction (versions, debut, fin, seuil) qui rend la liste des noms validés, ou lève
      `ValueError` · `fabriquer` : fonction (k) qui rend la famille du monde k · `mondes` : entier ≥ 1 · `seuil` :
      dans ]0, 1[.
    ④ CONDITIONS D'ENTRÉE — Celles de ③.
    ⑤ SORTIE — UNE valeur : dictionnaire `faux` (mondes à au moins un faux gagnant), `non_calculables`, `mondes`.
      [rend: 1]
    ⑥ TRAITEMENT — Pour k de 0 à mondes − 1 : fabriquer, juger sur [DEBUT, DEBUT + PERIODE_JOURS − 1] ; un
      `ValueError` compte « non calculable », jamais « faux » ni « juste ».
    ⑦ UNITÉ — Des NOMBRES DE MONDES.
    ⑧ POURQUOI — Le risque promis porte sur la famille : un seul faux gagnant suffit à compter le monde.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Une boucle bornée par `mondes`. Un appel de `methode` peut-il ne pas revenir ? Pas
      celui de `romano_wolf_du_gain` (boucles bornées).
      [sort: non]
    """
    fin = (DEBUT + datetime.timedelta(days=PERIODE_JOURS - 1)).isoformat()
    faux = non_calculables = 0
    for k in range(mondes):
        try:
            validees = methode(fabriquer(k), DEBUT.isoformat(), fin, seuil)
        except ValueError:
            non_calculables += 1
            continue
        faux += bool(validees)
    return {"faux": faux, "non_calculables": non_calculables, "mondes": mondes}


def verdict_d_une_case(mesure, seuil, binomiale):
    """Rend le verdict d'une case : « TIENT », « DÉPASSE » ou « INCONNU ».

    ① RÔLE — Décider si le taux mesuré dépasse le seuil promis de façon démontrée.
    ② CONTEXTE D'APPEL — `main`, une fois par case ; l'épreuve E8.
    ③ ENTRÉE — `mesure` : un rendu de `mesurer_le_risque` · `seuil` : le risque promis · `binomiale` : fonction (x, n, p), la
      probabilité d'au moins x succès sur n (`CALIBRER_LE_HASARD_DES_GAINS.binomiale_au_dessus`, réutilisée, R-708).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le mot du verdict.
      [rend: 1]
    ⑥ TRAITEMENT — Plus de 10 % de mondes non calculables → INCONNU (R-734) ; sinon DÉPASSE si la probabilité d'au
      moins `faux` faux gagnants au seuil promis est sous `NIVEAU_DE_L_ALERTE` ; sinon TIENT.
    ⑦ UNITÉ — Sans unité.
    ⑧ POURQUOI — Un taux mesuré fluctue : seul un dépassement improbable au risque promis est une preuve.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨ ③.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    calcules = mesure["mondes"] - mesure["non_calculables"]
    if calcules < 0.9 * mesure["mondes"]:
        return "INCONNU"
    if binomiale(mesure["faux"], calcules, seuil) < NIVEAU_DE_L_ALERTE:
        return "DÉPASSE"
    return "TIENT"


# ─────────────────────────────────────────────────────────────────────
# MODE « --famille » — ⑤ ET ⑥ ENSEMBLE (décision de Jean-Luc du 25-11-2026, 15h36, « 1 » : mesurer avant de fixer C13)
# ─────────────────────────────────────────────────────────────────────
# Le pire cas de l'arbitre (ARBITRAGE_METHODE_DE_SELECTION_Sam_14-11-2026, §5) : une famille de 20 versions dont
# 10 ont un gain moyen NUL mais battent sûrement le hasard (⑤ est leur seule barrière), et 10 gagnent sûrement mais
# PAS MIEUX que le hasard (⑥ est leur seule barrière). Chacune des 20 a une hypothèse nulle vraie : toute version validée
# est une fausse gagnante. L'arbitre a mesuré, avec des statistiques normales idéales, 9,45 % à 5 % par contrôle et
# 4,9 % à 2,5 % (versions indépendantes) ; 8,25 % et 4,1 % avec le maximum et des versions ressemblantes à 0,96.
FAMILLE_PAR_MOITIE = 10                               # 10 + 10 versions, comme l'arbitre (m = 20)
FAMILLE_TAILLE = 50                                   # le bord le plus petit de « 50 à 250 » : là où la méthode peut rougir
FAMILLE_DECALAGE_EUR = 3000.0                         # gain ajouté aux 10 « sûres pour ⑤ » : t de l'ordre de 10 à n = 50
FAMILLE_CASES = {                                     # nom → (liaison des opérations, ressemblance des versions)
    "pire cas, opérations et versions indépendantes": ("indépendantes", 0.0),
    "pire cas, paquets de 10 liés, versions ressemblantes (0,96)": ("paquets de 10 liés (0,36)", 0.96),
}
FAMILLE_P_DU_PLAN = 0.5                               # le pire pour la largeur : l'intervalle tient ±1 point QUEL QUE SOIT le taux
FAMILLE_DEMI_LARGEUR = 0.01                           # ±1 point, demandé le 25-11-2026
FAMILLE_Z = 1.96                                      # intervalle à 95 %


def mondes_pour_la_precision(p_du_plan=FAMILLE_P_DU_PLAN, demi_largeur=FAMILLE_DEMI_LARGEUR, z=FAMILLE_Z):
    """Rend le nombre de mondes qui donne à un taux mesuré un intervalle à 95 % plus étroit que ±demi_largeur.

    ① RÔLE — Dimensionner le mode « --famille » et afficher le calcul.
    ② CONTEXTE D'APPEL — `mesurer_la_famille`, pour l'affichage ; l'épreuve E9.
    ③ ENTRÉE — `p_du_plan` : le taux le plus défavorable qu'on prévoit (la largeur est maximale à 0,5 et croît avec p
      jusque-là) · `demi_largeur` : en taux (0,01 = 1 point) · `z` : 1,96 pour 95 %.
    ④ CONDITIONS D'ENTRÉE — 0 < p_du_plan < 1 ; demi_largeur > 0.
    ⑤ SORTIE — UNE valeur : l'entier N = ⌊z² × p × (1 − p) ÷ demi_largeur²⌋ + 1, le plus petit qui rend l'intervalle
      STRICTEMENT plus étroit.
      [rend: 1]
    ⑥ TRAITEMENT — La formule de ⑤ (approximation normale de la binomiale : demi-largeur = z × √(p(1 − p) ÷ N)).
    ⑦ UNITÉ — Un NOMBRE DE MONDES.
    ⑧ POURQUOI — Le 25-11-2026, Jean-Luc veut NOS chiffres à ±1 point près : un taux sans sa précision ne tranche rien.
      Exemple : p = 0,5 → 1,96² × 0,5 × 0,5 ÷ 0,01² = 9 604 → 9 605 ; à un taux mesuré de 9,45 %, la demi-largeur
      est alors 1,96 × √(0,0945 × 0,9055 ÷ 9 605) = 0,58 point.
    ⑨ CE QUI CLOCHE — Approximation normale : l'intervalle de Wilson affiché par `mesurer_la_famille` en diffère de
      quelques centièmes de point à ces tailles.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    return math.floor(round(z * z * p_du_plan * (1.0 - p_du_plan) / (demi_largeur * demi_largeur), 9)) + 1


def fabriquer_la_famille_mixte(hasard, J, forme, liaison, ressemblance, tirages):
    """Fabrique UNE famille du pire cas de l'arbitre : 10 versions nulles pour ⑤, 10 versions nulles pour ⑥.

    ① RÔLE — Le monde simulé du mode « --famille ».
    ② CONTEXTE D'APPEL — `mesurer_la_famille`, une fois par monde ; l'épreuve E9.
    ③ ENTRÉE — `hasard` : un `random.Random` · `J` : le module MODULE_JUGEMENT · `forme` : liste triée (gain, durée) de
      `fabriquer_les_formes` · `liaison` : une valeur de LIAISONS · `ressemblance` : dans [0, 1[ · `tirages` : le nombre
      de tirages de l'étalon de hasard de chaque version (entier ≥ 1).
    ④ CONDITIONS D'ENTRÉE — Celles de ③.
    ⑤ SORTIE — DEUX valeurs : les versions (nom → opérations, pour ⑤) et les p de ⑥ (nom → (p, tirages), pour
      `holm_du_hasard`).
      [rend: 2]
    ⑥ TRAITEMENT —
      ① « z » (gain NUL, bat sûrement le hasard) : `fabriquer_une_famille` (gains de moyenne nulle) ; leur p de ⑥ est
         celui d'un gain au-dessus de tous les tirages de l'étalon, soit 1 ÷ (tirages + 1).
      ② « h » (gain SÛR, pas mieux que le hasard) : `fabriquer_une_famille`, puis FAMILLE_DECALAGE_EUR ajouté à chaque
         gain ; leur p de ⑥ : le gain de la version et ceux des tirages sont tirés de la MÊME loi normale — la version
         n'est qu'un tirage de plus. Avec la ressemblance r, la version i prend √r × c + √(1 − r) × e_i, c commun aux 10.
      ③ Chaque p passe par `MODULE_JUGEMENT.p_du_hasard` (R-708 : la même formule que le juge).
    ⑦ UNITÉ — Gains en EUROS ; les valeurs de l'étalon sont sans unité (seul leur rang compte).
    ⑧ POURQUOI — C'est le cas où le risque des deux contrôles s'additionne (ARBITRAGE §5 : P ≤ α₅ + α₆) ; l'arbitre
      l'a mesuré avec des statistiques idéales ; ici ⑤ est la vraie `romano_wolf_du_gain` sur des opérations datées.
    ⑨ CE QUI CLOCHE — ① ⑥ n'est pas rejoué par `etalon_hasard` (il faudrait des cours) : son p est fabriqué par sa
      définition (version échangeable avec les tirages), ce qui le rend exact — c'est ce que promet ⑥ (ARBITRAGE §5).
      ② Les statistiques de ⑤ et de ⑥ d'une même version sont indépendantes, comme chez l'arbitre (corrélation 0).
    ⑩ EFFET — Aucun (consomme le hasard reçu).
    ⑪ TERMINAISON — Rend la main. Boucles bornées par 20 × (taille + tirages). Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    nulles = fabriquer_une_famille(hasard, forme, FAMILLE_TAILLE, FAMILLE_PAR_MOITIE, liaison, ressemblance)
    sures = fabriquer_une_famille(hasard, forme, FAMILLE_TAILLE, FAMILLE_PAR_MOITIE, liaison, ressemblance)
    versions, p6 = {}, {}
    commun = hasard.gauss(0.0, 1.0)
    for nom, ops in nulles.items():
        etalon = [hasard.gauss(0.0, 1.0) for _ in range(tirages)]
        versions["z" + nom] = ops
        p6["z" + nom] = J.p_du_hasard(max(etalon) + 1.0, {"gains_des_tirages": etalon})[:2]
    for nom, ops in sures.items():
        etalon = [hasard.gauss(0.0, 1.0) for _ in range(tirages)]
        versions["h" + nom] = [dict(o, net=o["net"] + FAMILLE_DECALAGE_EUR) for o in ops]
        net = math.sqrt(ressemblance) * commun + math.sqrt(1.0 - ressemblance) * hasard.gauss(0.0, 1.0)
        p6["h" + nom] = J.p_du_hasard(net, {"gains_des_tirages": etalon})[:2]
    return versions, p6


def juger_les_deux(J, versions, p6, debut, fin, seuil, graine):
    """Rend les versions validées par ⑤ ET par ⑥, chaque contrôle corrigé sur sa famille au même seuil.

    ① RÔLE — La règle arbitrée du regard sur les 30 % : ⑤ par Romano et Wolf, ⑥ par Holm, valider exige les deux.
    ② CONTEXTE D'APPEL — `mesurer_la_famille`, une fois par monde ; l'épreuve E9.
    ③ ENTRÉE — `J` : MODULE_JUGEMENT · `versions` : nom → opérations · `p6` : nom → (p, tirages) · `debut`, `fin` :
      AAAA-MM-JJ · `seuil` : le seuil PAR CONTRÔLE · `graine` : entier.
    ④ CONDITIONS D'ENTRÉE — Mêmes noms dans `versions` et `p6`.
    ⑤ SORTIE — UNE valeur : la liste des noms validés par les deux.
      [rend: 1]
    ⑥ TRAITEMENT — `romano_wolf_du_gain(...)["validees"]` ∩ {nom : `holm_du_hasard(p6, seuil)["etats"][nom]` = PASSE}.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une version est une fausse gagnante si l'une de ses deux hypothèses nulles est vraie (ARBITRAGE §5).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève `ValueError` (compté « non calculable » par `mesurer_le_risque`).
      [sort: non]
    """
    etats = J.holm_du_hasard(p6, seuil)["etats"]
    return [v for v in J.romano_wolf_du_gain(versions, debut, fin, seuil=seuil, graine=graine)["validees"]
            if etats[v] == "PASSE"]


def mesurer_la_famille(J, C, mondes, seuil):
    """Mesure, case par case, le taux de mondes où une famille du pire cas a au moins une fausse gagnante.

    ① RÔLE — Le mode « --famille » : NOS chiffres face à ceux de l'arbitre (9,45 % à 5 %, 4,9 % à 2,5 %).
    ② CONTEXTE D'APPEL — `main` ; sur GitHub, codes `SeuilFamille5` et `SeuilFamille25` de
      `tests/LANCEMENT_DES_EPREUVES.json`.
    ③ ENTRÉE — `J` : MODULE_JUGEMENT · `C` : CALIBRER_LE_HASARD_DES_GAINS · `mondes` : par case · `seuil` : par contrôle.
    ④ CONDITIONS D'ENTRÉE — Celles de `main`.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir ⑥ ④).
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher le calcul du nombre de mondes (`mondes_pour_la_precision`) · ② pour chaque case de
      FAMILLE_CASES : fabriquer chaque monde (`fabriquer_la_famille_mixte`, forme « +1/-3 », tirages de l'étalon =
      `tirages_exiges_par_holm(20, seuil)`), juger (`juger_les_deux`), compter (`mesurer_le_risque`) · ③ afficher le
      taux, son intervalle de Wilson à 95 % (`wilson_bas`, R-708) et le verdict face à la borne α₅ + α₆ = 2 × seuil
      (`verdict_d_une_case`) · ④ code 2 si une case est INCONNUE, 1 si une case DÉPASSE 2 × seuil, sinon 0.
    ⑦ UNITÉ — Taux en POURCENTS à l'écran.
    ⑧ POURQUOI — Décision de Jean-Luc du 25-11-2026, 15h36 : mesurer avant de fixer SEUIL_PAR_FAMILLE_DEFAUT (C13).
      La borne 2 × seuil est prouvée (ARBITRAGE §5) : la dépasser serait un défaut de la méthode, pas un choix.
    ⑨ CE QUI CLOCHE — ① Le verdict ne porte que sur la borne prouvée ; comparer le taux à 5 % revient à Jean-Luc.
      ② Une seule forme (+1/-3) et une seule taille (50) : les plus défavorables à Student, choix d'économie de durée.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. Boucles bornées par le nombre de cases et de mondes. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    m = 2 * FAMILLE_PAR_MOITIE
    tirages = J.tirages_exiges_par_holm(m, seuil)
    n_plan = mondes_pour_la_precision()
    print("MODE FAMILLE (⑤ ET ⑥) — pire cas de l'arbitre : %d versions (%d à gain nul qui battent sûrement le hasard, "
          "%d à gain sûr pas mieux que le hasard), %d opérations, seuil %r PAR CONTRÔLE, %d mondes par case, "
          "%d tirages d'étalon par version" % (m, FAMILLE_PAR_MOITIE, FAMILLE_PAR_MOITIE, FAMILLE_TAILLE, seuil, mondes,
                                              tirages))
    print("  NOMBRE DE MONDES : ⌊%.2f² × %.2f × %.2f ÷ %.2f²⌋ + 1 = %d pour moins de ±%.0f point à 95 %% quel que soit "
          "le taux ; joués ici : %d%s" % (FAMILLE_Z, FAMILLE_P_DU_PLAN, 1 - FAMILLE_P_DU_PLAN, FAMILLE_DEMI_LARGEUR,
                                         n_plan, 100 * FAMILLE_DEMI_LARGEUR, mondes,
                                         "" if mondes >= n_plan else " — PRÉCISION NON ATTEINTE"))
    forme = fabriquer_les_formes()["+1/-3 (10 jours)"]
    code = 0
    for nom_case, (nom_liaison, ress) in FAMILLE_CASES.items():
        hasard = random.Random(zlib.crc32(("famille|%s|%r" % (nom_case, seuil)).encode()))
        du_monde = {}

        def fabriquer(k):
            """Fabrique le monde k et garde ses p de ⑥ et sa graine pour `methode`.

            ① RÔLE — Le monde k. ② CONTEXTE D'APPEL — `mesurer_le_risque`. ③ ENTRÉE — `k` : entier.
            ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les versions. [rend: 1]
            ⑥ TRAITEMENT — `fabriquer_la_famille_mixte` ; ranger p6 et k dans `du_monde`. ⑦ UNITÉ — —
            ⑧ POURQUOI — `mesurer_le_risque` (réutilisé, R-708) ne passe que les versions à la méthode.
            ⑨ CE QUI CLOCHE — — ⑩ EFFET — Consomme le hasard de la case. ⑪ TERMINAISON — Rend la main. Aucun appel ne
            peut ne pas revenir.
              [sort: non]
            """
            versions, du_monde["p6"] = fabriquer_la_famille_mixte(hasard, J, forme, LIAISONS[nom_liaison], ress, tirages)
            du_monde["k"] = k
            return versions

        def methode(versions, debut, fin_, s):
            """Juge le monde par ⑤ et ⑥ ensemble.

            ① RÔLE — Brancher `juger_les_deux` sur `mesurer_le_risque`. ② CONTEXTE D'APPEL — `mesurer_le_risque`.
            ③ ENTRÉE — versions, période, seuil. ④ CONDITIONS D'ENTRÉE — `fabriquer` vient d'être appelé.
            ⑤ SORTIE — UNE valeur : la liste des validées. [rend: 1] ⑥ TRAITEMENT — Graine propre au monde.
            ⑦ UNITÉ — — ⑧ POURQUOI — Comme `main`. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main ou lève `ValueError`.
              [sort: non]
            """
            return juger_les_deux(J, versions, du_monde["p6"], debut, fin_, s, len(versions) + du_monde["k"])

        mesure = mesurer_le_risque(methode, fabriquer, mondes, seuil)
        calcules = mesure["mondes"] - mesure["non_calculables"]
        verdict = verdict_d_une_case(mesure, 2.0 * seuil, C.binomiale_au_dessus)
        taux = 100.0 * mesure["faux"] / max(1, calcules)
        bas = J.wilson_bas(calcules, taux)
        haut = None if bas is None else 100.0 - J.wilson_bas(calcules, 100.0 - taux)
        print("  %-8s %-62s : %5.2f %% [%s ; %s] (%d sur %d, %d non calculables) — borne prouvée α₅ + α₆ = %.1f %%"
              % (verdict, nom_case, taux, "—" if bas is None else "%.2f" % bas, "—" if haut is None else "%.2f" % haut,
                 mesure["faux"], calcules, mesure["non_calculables"], 200.0 * seuil))
        if verdict == "INCONNU":
            code = max(code, 2) if code != 1 else 1
        elif verdict == "DÉPASSE":
            code = 1
    print("VERDICT FAMILLE : %s" % {0: "chaque case tient la borne prouvée 2 × seuil ; la comparaison à 5 % revient "
                                       "à Jean-Luc", 1: "DÉPASSE la borne prouvée 2 × seuil — défaut de la méthode",
                                    2: "INCONNU — une case n'a pas pu se mesurer"}[code])
    return code


def charger(chemin, nom):
    """Charge un programme du dépôt par son chemin.

    ① RÔLE — Prendre le module de la racine reçue, pas un autre.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve E8.
    ③ ENTRÉE — `chemin` : chemin du fichier · `nom` : nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — spec_from_file_location, exécution, rangé dans sys.modules.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les modules importent leurs voisins par leur nom.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Charge et exécute du code.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


def main(argv):
    """Joue toutes les cases et rend le code.

    ① RÔLE — Le chef d'orchestre du calibrage.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ③ et ④.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Lire les arguments et les modules ; en « --famille », passer la main à `mesurer_la_famille` ;
      sinon, pour chaque case, mesurer et juger ; afficher ; rendre le code.
    ⑦ UNITÉ — Taux en POURCENTS à l'écran.
    ⑧ POURQUOI — R-731 (une mesure qui peut rougir), R-734 (code non nul si une case n'a pas pu se mesurer).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    famille = len(argv) > 2 and argv[2] == "--famille"
    if (len(argv) != 5 if famille else not 2 <= len(argv) <= 4) or "--famille" in argv[3:]:
        print(__doc__.split("USAGE")[1].split("①")[0].strip())
        return 2
    if famille:
        argv = argv[:2] + argv[3:]
    racine = os.path.abspath(argv[1])
    for f in ("programmes/MODULE_JUGEMENT.py", "programmes/CALIBRER_LE_HASARD_DES_GAINS.py"):
        if not os.path.exists(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            return 2
    sys.path.insert(0, os.path.join(racine, "programmes"))
    J = charger(os.path.join(racine, "programmes/MODULE_JUGEMENT.py"), "MODULE_JUGEMENT")
    C = charger(os.path.join(racine, "programmes/CALIBRER_LE_HASARD_DES_GAINS.py"), "CALIBRER_LE_HASARD_DES_GAINS")
    try:
        mondes = int(argv[2]) if len(argv) > 2 else 1000
        seuil = float(argv[3]) if len(argv) > 3 else J.SEUIL_PAR_FAMILLE_DEFAUT
    except ValueError:
        print("ARGUMENT ILLISIBLE : %s" % argv[2:])
        return 2
    if mondes < 50 or not (0.0 < seuil < 0.5):
        print("ARGUMENT HORS DE SA FORME : mondes %d (≥ 50), seuil %r (dans ]0, 0,5[)" % (mondes, seuil))
        return 2

    if famille:
        return mesurer_la_famille(J, C, mondes, seuil)

    def methode(versions, debut, fin, s):
        """Juge une famille par la méthode éprouvée.

        ① RÔLE — Brancher `romano_wolf_du_gain` sur `mesurer_le_risque`.
        ② CONTEXTE D'APPEL — `mesurer_le_risque`.
        ③ ENTRÉE — `versions` : la famille · `debut`, `fin` : la période · `s` : le seuil.
        ④ CONDITIONS D'ENTRÉE — `methode.monde` posé par `fabriquer`.
        ⑤ SORTIE — UNE valeur : la liste des validées.
          [rend: 1]
        ⑥ TRAITEMENT — Appel avec une graine propre au monde.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Sans graine propre, tous les mondes partageraient leurs tirages.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main ou lève `ValueError`.
          [sort: non]
        """
        return J.romano_wolf_du_gain(versions, debut, fin, seuil=s, graine=len(versions) + methode.monde)["validees"]

    print("CALIBRAGE DE LA MÉTHODE DES 30 %% — %d versions par famille, %d mondes par case, seuil %r"
          % (VERSIONS_PAR_FAMILLE, mondes, seuil))
    code = 0
    for nom_forme, forme in fabriquer_les_formes().items():
        for n in TAILLES:
            for nom_liaison, liaison in LIAISONS.items():
                for nom_ress, ress in RESSEMBLANCES.items():
                    hasard = random.Random(zlib.crc32(("%s|%d|%s|%s" % (nom_forme, n, nom_liaison, nom_ress)).encode()))

                    def fabriquer(k):
                        """Fabrique la famille du monde k de la case.

                        ① RÔLE — Le monde k.
                        ② CONTEXTE D'APPEL — `mesurer_le_risque`.
                        ③ ENTRÉE — `k` : entier.
                        ④ CONDITIONS D'ENTRÉE — —
                        ⑤ SORTIE — UNE valeur : la famille.
                          [rend: 1]
                        ⑥ TRAITEMENT — Noter k pour la graine de `methode`, puis `fabriquer_une_famille`.
                        ⑦ UNITÉ — —
                        ⑧ POURQUOI — La graine du jugement suit le monde.
                        ⑨ CE QUI CLOCHE — —
                        ⑩ EFFET — Consomme le hasard de la case.
                        ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
                          [sort: non]
                        """
                        methode.monde = k
                        return fabriquer_une_famille(hasard, forme, n, VERSIONS_PAR_FAMILLE, liaison, ress)
                    mesure = mesurer_le_risque(methode, fabriquer, mondes, seuil)
                    verdict = verdict_d_une_case(mesure, seuil, C.binomiale_au_dessus)
                    exigee = liaison[3]
                    calcules = max(1, mesure["mondes"] - mesure["non_calculables"])
                    print("  %-8s %-20s n=%-4d %-36s %-30s : %5.2f %% (%d sur %d, %d non calculables)%s"
                          % (verdict, nom_forme, n, nom_liaison, nom_ress, 100.0 * mesure["faux"] / calcules,
                             mesure["faux"], calcules, mesure["non_calculables"], "" if exigee else " — affiché"))
                    if exigee and verdict == "INCONNU":
                        code = max(code, 2) if code != 1 else 1
                    if exigee and verdict == "DÉPASSE":
                        code = 1
    print("VERDICT : %s" % {0: "la méthode tient son seuil dans chaque case exigée",
                            1: "DÉPASSE — studentiser autrement (ARBITRAGE, étape 6) et relancer",
                            2: "INCONNU — une case n'a pas pu se mesurer"}[code])
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
