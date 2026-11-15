#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVE DE CALIBRAGE DU P DU GAIN (bootstrap-t par blocs, A-782, A-786) — Simulation uniquement. Samedi 14-11-2026.

LE SENS EN TÊTE — `MODULE_JUGEMENT.probabilite_que_le_gain_soit_du_hasard` promet : « si la stratégie n'a aucun
talent, je ne dirai p < α qu'au plus une fois sur 1 ÷ α ». Ce programme VÉRIFIE cette promesse au lieu de la croire :
il fabrique des milliers de stratégies SANS TALENT (gain moyen nul par construction) avec les VRAIES formes de gains du
projet, leur fait calculer leur p par la fonction elle-même, et compte combien passent le seuil. Il le fait au seuil
0,05 et au seuil le plus strict (par défaut 0,05 ÷ 69, celui de la loi R-505 ⑤ avec k = 69), avec des opérations
indépendantes PUIS liées par paquets (le scénario « régime » de la contre-expertise du 14-11-2026, C6 : « l'épreuve de
calibrage doit inclure un scénario d'opérations liées […] ; c'est là qu'elle peut rougir »). A-782 (Jean-Luc,
14-11-2026, 16h56) la rend obligatoire avant le regard.

USAGE : python3 -B programmes/CALIBRER_LE_HASARD_DES_GAINS.py <racine> [mondes par case, défaut 2000] [seuil strict]
CODE : 0 si chaque case EXIGÉE tient sa promesse aux deux seuils ; 1 si l'une la dépasse de façon démontrée ;
2 si une donnée manque ou si une case n'a pas pu se mesurer (R-734).

① RÔLE — Mesurer le taux de « faux gagnants » du p du gain, et sortir non nul s'il dépasse le risque promis.
② CONTEXTE D'APPEL — À la main, avant tout regard sur des années d'examen (A-782), et après toute modification de
  `probabilite_que_le_gain_soit_du_hasard`. Il n'est PAS lancé par la certification de la nuit : 2 000 mondes par case
  prennent plusieurs minutes, et la nuit est déjà à 328 minutes sur 330 (`programmes/CERTIFIER_LA_VERSION.py`, relevé
  du 14-11-2026). Les épreuves rapides (sabotages) vivent dans `tests/EPREUVES_DU_HASARD_DES_GAINS_Sam_14-11-2026.py`.
③ ENTRÉE — La racine du dépôt ; facultatifs : le nombre de mondes par case (entier ≥ 100), le seuil strict (dans ]0, 0,05[).
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/MODULE_JUGEMENT.py`, `donnees/cours_maitre.csv`,
  `donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv`. Sinon code 2.
⑤ SORTIE — Le code de sortie dit en « CODE ». À l'écran : les trois formes de gains lues, une ligne par case (taux
  mesuré, combien de fois le promis, verdict), la précision des tirages, le verdict d'ensemble.
  [rend: 1]
⑥ TRAITEMENT — ① lire les trois formes de gains (`lire_les_formes`) · ② pour chaque forme, chaque scénario et chaque
  nombre d'opérations : fabriquer des mondes sans talent (`fabriquer_une_strategie`), calculer le p de chacun UNE fois
  au seuil strict (la précision du p est réglée pour le plus strict ; le même p se compare aussi à 0,05), compter
  (`mesurer_une_case`) · ③ juger chaque case exigée au seuil 0,05, et chaque couple (forme, scénario) exigé au seuil
  strict sur l'ensemble de ses tailles (`binomiale_au_dessus`) · ④ mesurer la dispersion du p d'une graine à l'autre
  sur la vraie série de C5 (`precision_des_tirages`) · ⑤ rendre le code.
⑦ UNITÉ — Gains en EUROS sur 100 000 € par opération ; durées et périodes en JOURS DE CALENDRIER ; taux sans unité.
⑧ POURQUOI — Une promesse de risque se mesure, elle ne se suppose pas : la loi de Student promettait 5 % et donnait
  jusqu'à 80 fois plus au seuil de la loi (rapport TERMINER du 14-11-2026, B.2). Le bootstrap-t ne tient sa promesse
  qu'en théorie et en grand échantillon (Hall 1988 ; Götze et Künsch 1996) ; avec des opérations liées, la
  contre-expertise du 14-11 a mesuré 10 à 17 % au lieu de 5 % pour un bootstrap-t à écart-type ordinaire. Les formes
  de gains sont les VRAIES (cours 2024-2026 et les 100 opérations de C5), parce que c'est leur dissymétrie qui trompe
  Student. Les années 2000-2023 ne sont PAS lues (ce sont des années d'examen ; R-505 ③).
⑨ CE QUI CLOCHE — ① Le monde simulé n'est pas le marché : les liens entre opérations sont une copule normale par
  paquets, choisie pour garder exactement la forme réelle des gains ; un krach réel peut lier autrement. ② Au seuil
  strict, 6 000 mondes n'attendent que 4,3 faux au niveau promis : seul un dépassement d'environ trois fois est
  démontrable ; pour plus de finesse, augmenter le nombre de mondes (argument 2). ③ Le scénario « régime persistant »
  (paquets liés d'un paquet au suivant, 0,8) est AFFICHÉ et non exigé : aucune méthode qui ne regarde qu'une période ne
  voit un régime aussi long qu'elle (`probabilite_que_le_gain_soit_du_hasard`, ⑨ ①) ; c'est le rôle de R-505 ⑦.
  ④ Le critère « dépasse de façon démontrée » est un test binomial unilatéral à 0,001 (une fausse alerte sur mille
  cases environ) : un dépassement léger (6 % au lieu de 5 %) peut passer inaperçu avec 2 000 mondes.
  ⑤ Les sorties d'opération sont celles de la forme (objectif, stop, échéance), pas rejouées sur des cours.
⑩ EFFET — N'écrit aucun fichier ; affiche.
⑪ TERMINAISON — Rend un code de sortie. Toutes les boucles sont bornées par le nombre de mondes, de cases et de
  tirages (bornés par `MODULE_JUGEMENT.TIRAGES_MAXIMUM`). Aucun de ses appels ne peut ne pas revenir.
  [sort: oui — code de sortie]
⑫ DÉFINITIONS
  un monde : une stratégie fabriquée, sans talent, avec ses opérations, ses dates et ses gains
  sans talent : dont le vrai gain moyen par opération est nul — la forme réelle, recentrée
  une case : une forme × un scénario × un nombre d'opérations
  un faux gagnant : un monde sans talent dont le p passe sous le seuil
  le risque promis : le seuil lui-même (au seuil 0,05, au plus 5 % de faux gagnants)
"""
import csv
import datetime
import importlib.util
import math
import os
import random
import sys
import time
import zlib
from statistics import NormalDist

JOUR_ZERO = datetime.date(2030, 1, 1).toordinal()     # dates fictives : aucun calendrier réel n'est suggéré
PERIODE_JOURS = 900                                   # ≈ 2,5 ans, la durée du tableau des 100 opérations de C5
TAILLES = (50, 100, 250)                              # la plage « 50 à 250 observations » de la méthode (ARBITRAGE, étape 6)
# scénario : (taille des paquets, corrélation dans un paquet, persistance d'un paquet au suivant, exigé ?)
SCENARIOS = {
    "independantes": (1, 0.0, 0.0, True),
    "paquets de 5 liés (0,30)": (5, 0.30, 0.0, True),
    "régime : paquets de 10 liés (0,36)": (10, 0.36, 0.0, True),     # contre-expertise du 14-11, choc commun 0,6
    "régime persistant (0,8) — affiché": (10, 0.36, 0.8, False),
}
SEUIL_LARGE = 0.05
NIVEAU_DE_L_ALERTE = 0.001


def lire_les_formes(racine):
    """Lit les trois formes de gains réelles : C5 (100 opérations), +1 % / −3 % et +1,2 % / −1 % (toutes les entrées).

    ① RÔLE — Donner les formes de gains (gain, durée) sur lesquelles les mondes sans talent sont fabriqués.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Les deux fichiers de données existent ; sinon `FileNotFoundError` (main → code 2).
    ⑤ SORTIE — UNE valeur : {nom : liste de (gain en euros, durée en jours)}.
      [rend: 1]
    ⑥ TRAITEMENT — ① C5 : les 100 lignes du tableau du 01-08-2026, gain `net_eur`, durée sortie − entrée + 1 ·
      ② les deux autres : chaque valeur × chaque séance de `donnees/cours_maitre.csv` (2024-2026) ; achat à
      l'ouverture du lendemain ; sortie au stop ou à l'objectif touché par le plus bas ou le plus haut (les deux le même
      jour : le stop), sinon à la clôture de la dernière séance de l'horizon (10 et 3 séances) ; frais 0,15 % par ordre.
    ⑦ UNITÉ — Euros pour 100 000 € investis ; jours de calendrier.
    ⑧ POURQUOI — Ce sont les formes mesurées par le collège « terminer » du 14-11-2026 (B.2), celles où Student se
      trompe ; les frais n'ont pas d'effet (tout est recentré).
    ⑨ CE QUI CLOCHE — Les frais sont ceux du taux affiché par les instructions du projet, pas le barème réel : sans effet
      ici, la forme étant recentrée. Recalcul du 14-11-2026 : +1/−3, 28 530 entrées, part des PERDANTES 0,2509 (le q
      d'A-782, celui de `minimum_d_observations`), part sous la moyenne 0,2499 ; +1,2/−1, 28 557, perdantes 0,555,
      sous la moyenne 0,545 ; C5 réelle, 100, perdantes 0,39, sous la moyenne 0,40 (TERMINER : 28 073 et 0,252 ;
      28 444 et 0,555 — fin de période différente). Le calibrage n'utilise ni l'une ni l'autre : la sortie affiche
      les deux, nommées, pour qu'un lecteur ne confonde pas le q du minimum avec la part sous la moyenne.
    ⑩ EFFET — Lit deux fichiers.
    ⑪ TERMINAISON — Rend la main ; boucles bornées par le nombre de lignes et l'horizon.
      [sort: non]
    """
    formes = {}
    c5 = []
    with open(os.path.join(racine, "donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            e = datetime.date.fromisoformat(r["date_entree"])
            s = datetime.date.fromisoformat(r["date_sortie"])
            c5.append((float(r["net_eur"].replace(",", ".")), (s - e).days + 1))
    formes["C5 réelle +4/-2,5"] = c5
    par = {}
    with open(os.path.join(racine, "donnees/cours_maitre.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            par.setdefault(r["valeur"], []).append(r)
    for nom, objectif, stop, horizon in (("+1/-3 (10 séances)", 0.01, 0.03, 10), ("+1,2/-1 (3 séances)", 0.012, 0.01, 3)):
        sortie_forme = []
        for lignes in par.values():
            lignes.sort(key=lambda r: r["date"])
            for i in range(len(lignes) - 1):
                e = lignes[i + 1]
                pe = float(e["open"])
                if pe <= 0:
                    continue
                haut, bas, fin = pe * (1 + objectif), pe * (1 - stop), None
                for j in range(i + 1, min(i + 1 + horizon, len(lignes))):
                    if float(lignes[j]["low"]) <= bas:
                        fin = (bas, lignes[j]["date"])
                        break
                    if float(lignes[j]["high"]) >= haut:
                        fin = (haut, lignes[j]["date"])
                        break
                else:
                    if i + horizon < len(lignes):
                        fin = (float(lignes[i + horizon]["close"]), lignes[i + horizon]["date"])
                if fin is None:
                    continue
                ps, ds = fin
                gain = 100000.0 * (ps / pe - 1.0) - 150.0 - 150.0 * ps / pe
                duree = (datetime.date.fromisoformat(ds) - datetime.date.fromisoformat(e["date"])).days + 1
                sortie_forme.append((gain, duree))
        formes[nom] = sortie_forme
    return formes


def fabriquer_une_strategie(hasard, forme, n, paquet, rho, persistance):
    """Fabrique les opérations d'une stratégie SANS TALENT, avec la forme de gains reçue.

    ① RÔLE — Donner un monde où la vérité est connue : le vrai gain moyen est nul.
    ② CONTEXTE D'APPEL — `mesurer_une_case`, une fois par monde.
    ③ ENTRÉE — `hasard` : un `random.Random` · `forme` : liste de (gain, durée) RECENTRÉE et TRIÉE par gain ·
      `n` : nombre d'opérations · `paquet` : taille des paquets (1 = indépendantes) · `rho` : corrélation des gains dans
      un paquet · `persistance` : corrélation d'un paquet au suivant.
    ④ CONDITIONS D'ENTRÉE — `forme` non vide, de moyenne nulle ; 0 ≤ rho < 1 ; 0 ≤ persistance < 1.
    ⑤ SORTIE — UNE valeur : la liste des opérations ({net, date_entree, date_sortie}).
      [rend: 1]
    ⑥ TRAITEMENT — ① indépendantes : chaque opération tire un (gain, durée) au hasard dans la forme et un jour d'entrée
      au hasard sur `PERIODE_JOURS` · ② en paquets : ⌈n ÷ paquet⌉ jours de départ au hasard ; un facteur commun u par
      paquet (qui suit le précédent avec la persistance) ; chaque opération du paquet entre un jour plus tard que la
      précédente, avec z = √rho × u + √(1 − rho) × bruit, et prend dans la forme le gain de rang Φ(z) (copule normale).
    ⑦ UNITÉ — Euros ; jours de calendrier.
    ⑧ POURQUOI — La copule garde EXACTEMENT la forme réelle des gains (chaque opération, prise seule, a la forme réelle,
      donc un gain moyen nul) tout en liant les gains d'un même paquet : « cinq achats la même semaine de krach ».
    ⑨ CE QUI CLOCHE — Le rang Φ(z) est arrondi à la case inférieure de la forme (écart d'au plus 1 ÷ taille de la forme).
    ⑩ EFFET — Consomme des tirages de `hasard`.
    ⑪ TERMINAISON — Rend la main ; boucles bornées par n.
      [sort: non]
    """
    phi = NormalDist().cdf
    N = len(forme)
    vues = []
    if paquet == 1:
        for _ in range(n):
            g, d = forme[hasard.randrange(N)]
            vues.append((hasard.randrange(PERIODE_JOURS), g, d))
    else:
        departs = sorted(hasard.randrange(PERIODE_JOURS - paquet) for _ in range(-(-n // paquet)))
        u = hasard.gauss(0.0, 1.0)
        for i, j in enumerate(departs):
            if i:
                u = persistance * u + math.sqrt(1.0 - persistance * persistance) * hasard.gauss(0.0, 1.0)
            for k in range(paquet):
                if len(vues) >= n:
                    break
                z = math.sqrt(rho) * u + math.sqrt(1.0 - rho) * hasard.gauss(0.0, 1.0)
                g, d = forme[min(N - 1, int(phi(z) * N))]
                vues.append((j + k, g, d))
    return [{"net": g, "date_entree": datetime.date.fromordinal(JOUR_ZERO + j).isoformat(),
             "date_sortie": datetime.date.fromordinal(JOUR_ZERO + j + d - 1).isoformat()} for j, g, d in vues]


def binomiale_au_dessus(x, n, p):
    """Rend la probabilité d'observer au moins x succès sur n, chacun de probabilité p.

    ① RÔLE — Dire si un nombre de faux gagnants dépasse le promis de façon démontrée (et pas par le bruit des mondes).
    ② CONTEXTE D'APPEL — `main`, une fois par case et par seuil.
    ③ ENTRÉE — `x` : le nombre de succès observés, entier, 0 ≤ `x` ≤ `n` · `n` : le nombre d'essais, entier ·
      `p` : la probabilité promise d'un succès, dans ]0, 1[.
    ④ CONDITIONS D'ENTRÉE — Celles de ③ ; sinon le calcul est faux sans prévenir (appelant interne).
    ⑤ SORTIE — UNE valeur : la probabilité, entre 0 et 1.
      [rend: 1]
    ⑥ TRAITEMENT — Somme des termes de la loi binomiale de x à n, en logarithmes (`math.lgamma`).
    ⑦ UNITÉ — Sans unité.
    ⑧ POURQUOI — Test binomial exact unilatéral : la façon standard de comparer un compte à un taux promis.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; boucle bornée par n.
      [sort: non]
    """
    if x <= 0:
        return 1.0
    lp, lq = math.log(p), math.log1p(-p)
    return min(1.0, math.fsum(math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * lp
                                       + (n - k) * lq) for k in range(x, n + 1)))


def mesurer_une_case(J, forme, n, scenario, mondes, seuil_strict):
    """Joue `mondes` stratégies sans talent d'une case et compte les faux gagnants aux deux seuils.

    ① RÔLE — Le cœur de l'épreuve : la fonction réelle sur des mondes de vérité connue.
    ② CONTEXTE D'APPEL — `main`, une fois par case.
    ③ ENTRÉE — `J` : le module de jugement chargé · `forme` : recentrée, triée · `n` : opérations par monde ·
      `scenario` : une clé de SCENARIOS · `mondes` : nombre de mondes · `seuil_strict` : le seuil strict.
    ④ CONDITIONS D'ENTRÉE — Celles de `fabriquer_une_strategie`.
    ⑤ SORTIE — UNE valeur : {« faux_large », « faux_strict », « non_calculables », « mondes », « secondes »}.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque monde : fabriquer (graine du monde tirée de la case, fixe) ; p =
      `probabilite_que_le_gain_soit_du_hasard(ops, seuil_strict, graine=numéro du monde)` ; un `ValueError` compte
      « non calculable » et PAS faux gagnant (la grille en fait un INCONNU, qui ne valide jamais) ; compter p < 0,05 et
      p < seuil strict.
    ⑦ UNITÉ — Comptes ; secondes.
    ⑧ POURQUOI — Un seul p par monde, calculé avec la précision du seuil le plus strict, sert aux deux comparaisons
      (`probabilite_que_le_gain_soit_du_hasard`, ⑨ ⑤ : comparer à un seuil PLUS LARGE que celui reçu est permis).
      Graine des tirages = numéro du monde : sinon tous les mondes partageraient les mêmes tirages de blocs.
    ⑨ CE QUI CLOCHE — Une graine de monde dérivée du nom de la case (`zlib.crc32`) : stable d'une machine à l'autre.
    ⑩ EFFET — Aucun hors calcul.
    ⑪ TERMINAISON — Rend la main ; boucle bornée par `mondes`, chaque appel par `TIRAGES_MAXIMUM`.
      [sort: non]
    """
    paquet, rho, persistance, _exige = SCENARIOS[scenario]
    hasard = random.Random(zlib.crc32(("%s|%d|%s" % (scenario, n, forme[0])).encode()))
    debut = time.time()
    faux_large = faux_strict = non_calculables = 0
    for k in range(mondes):
        ops = fabriquer_une_strategie(hasard, forme, n, paquet, rho, persistance)
        try:
            p = J.probabilite_que_le_gain_soit_du_hasard(ops, seuil_strict, graine=k)
        except ValueError:
            non_calculables += 1
            continue
        faux_large += p < SEUIL_LARGE
        faux_strict += p < seuil_strict
    return {"faux_large": faux_large, "faux_strict": faux_strict, "non_calculables": non_calculables,
            "mondes": mondes, "secondes": time.time() - debut}


def precision_des_tirages(J, racine, seuil_strict, graines=30):
    """Mesure la dispersion du p d'une graine à l'autre, sur la VRAIE série des 100 opérations de C5.

    ① RÔLE — Mesurer ce que vaut la règle « 40 ÷ seuil tirages » (`DEPASSEMENTS_POUR_CONCLURE`) : la part du p qui
      vient des tirages et non des données.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `J`, `racine`, `seuil_strict`, `graines` (nombre de graines essayées).
    ④ CONDITIONS D'ENTRÉE — Le tableau des 100 opérations existe.
    ⑤ SORTIE — UNE valeur : la liste des lignes à afficher.
      [rend: 1]
    ⑥ TRAITEMENT — Pour h = 40 (la règle) puis h = 10 (pour comparer) : p de la série de C5 au seuil strict avec
      `graines` graines ; moyenne, écart-type, écart-type relatif. `DEPASSEMENTS_POUR_CONCLURE` est remis à sa valeur
      après la mesure, même en cas d'erreur.
    ⑦ UNITÉ — Probabilités ; écart relatif en pourcents.
    ⑧ POURQUOI — Le mandat du 14-11-2026 : « au moins ~ 40/seuil — mesure-le ». Théorie : écart relatif ≈ 1 ÷ √h.
    ⑨ CE QUI CLOCHE — Mesuré sur UNE série (p ≈ 0,013, loin du seuil strict) : la dispersion près du seuil est celle
      de la théorie, non mesurée ici.
    ⑩ EFFET — Modifie puis rétablit une constante du module chargé en mémoire (jamais le fichier).
    ⑪ TERMINAISON — Rend la main ; 2 × `graines` appels bornés.
      [sort: non]
    """
    ops = []
    with open(os.path.join(racine, "donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            ops.append({"net": float(r["net_eur"].replace(",", ".")), "date_entree": r["date_entree"],
                        "date_sortie": r["date_sortie"]})
    lignes, avant = [], J.DEPASSEMENTS_POUR_CONCLURE
    try:
        for h in (avant, 10):
            J.DEPASSEMENTS_POUR_CONCLURE = h
            ps = [J.probabilite_que_le_gain_soit_du_hasard(ops, seuil_strict, graine=g) for g in range(1, graines + 1)]
            m = sum(ps) / len(ps)
            e = math.sqrt(sum((x - m) ** 2 for x in ps) / (len(ps) - 1))
            lignes.append("  h = %2d (tirages max %d) : p moyen %.5f, écart-type %.5f, soit %.1f %% (théorie 1/√h = %.1f %%)"
                          % (h, max(J.TIRAGES_MINIMUM, math.ceil(h / seuil_strict)), m, e, 100 * e / m,
                             100 / math.sqrt(h)))
    finally:
        J.DEPASSEMENTS_POUR_CONCLURE = avant
    return lignes


def main(argv):
    """Lance l'épreuve et rend le code de sortie.

    ① RÔLE — Enchaîner lecture, mesure, verdict.
    ② CONTEXTE D'APPEL — La ligne de commande, une fois.
    ③ ENTRÉE — `argv` : [programme, racine, (mondes), (seuil strict)].
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête, ④ ; sinon le code 2.
    ⑤ SORTIE — UNE valeur : le code 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Celui de l'en-tête, ⑥.
    ⑦ UNITÉ — Taux sans unité ; secondes.
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main ; aucun appel ne peut ne pas revenir (tirages bornés).
      [sort: non]
    """
    if len(argv) < 2:
        print(__doc__.split("USAGE")[1].split("①")[0].strip())
        return 2
    racine = os.path.abspath(argv[1])
    try:
        mondes = int(argv[2]) if len(argv) > 2 else 2000
        seuil_strict = float(argv[3]) if len(argv) > 3 else 0.05 / 69
        if mondes < 100 or not (0.0 < seuil_strict < SEUIL_LARGE):
            raise ValueError
    except ValueError:
        print("ARGUMENTS INVALIDES : mondes entier ≥ 100, seuil strict dans ]0 ; 0,05[")
        return 2
    try:
        spec = importlib.util.spec_from_file_location("MODULE_JUGEMENT", os.path.join(racine, "programmes/MODULE_JUGEMENT.py"))
        J = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(J)
        formes_brutes = lire_les_formes(racine)
    except (FileNotFoundError, OSError, AttributeError) as ex:
        print("DONNÉE MANQUANTE : %s" % ex)
        return 2
    print("ÉPREUVE DE CALIBRAGE DU P DU GAIN (bootstrap-t par blocs) — %d mondes par case, seuil strict %.6f, "
          "période %d jours" % (mondes, seuil_strict, PERIODE_JOURS))
    formes = {}
    for nom, f in formes_brutes.items():
        if len(f) < 2:
            print("DONNÉE MANQUANTE : forme %s vide" % nom)
            return 2
        moy = math.fsum(g for g, _ in f) / len(f)
        formes[nom] = sorted((g - moy, d) for g, d in f)
        print("  forme %-22s %6d gains, moyenne brute %8.1f EUR, part des perdantes (q d'A-782) %.3f, part sous la "
              "moyenne %.3f, détention max %d jours"
              % (nom, len(f), moy, sum(1 for g, _ in f if g < 0.0) / len(f), sum(1 for g, _ in f if g < moy) / len(f),
                 max(d for _, d in f)))
    rouges, trous = [], []
    print("\n  %-22s %-36s %4s | %-30s | %-30s | non calc." % ("forme", "scénario", "n", "seuil 0,05", "seuil strict"))
    for nom, forme in formes.items():
        for scenario, (_p, _r, _ph, exige) in SCENARIOS.items():
            cumul = [0, 0]
            for n in TAILLES:
                r = mesurer_une_case(J, forme, n, scenario, mondes, seuil_strict)
                calcules = r["mondes"] - r["non_calculables"]
                if calcules < r["mondes"] // 2:
                    trous.append("%s / %s / n=%d : %d mondes non calculables sur %d" % (nom, scenario, n,
                                                                                      r["non_calculables"], r["mondes"]))
                cumul[0] += r["faux_strict"]
                cumul[1] += r["mondes"]
                pb = binomiale_au_dessus(r["faux_large"], r["mondes"], SEUIL_LARGE)
                depasse = exige and pb < NIVEAU_DE_L_ALERTE
                if depasse:
                    rouges.append("%s / %s / n=%d au seuil 0,05 : %.4f" % (nom, scenario, n, r["faux_large"] / r["mondes"]))
                print("  %-22s %-36s %4d | %.4f (x%.2f) %-14s | %.5f (x%.2f) %-11s | %d  [%.0f s]"
                      % (nom, scenario, n, r["faux_large"] / r["mondes"], r["faux_large"] / r["mondes"] / SEUIL_LARGE,
                         "DÉPASSÉ" if depasse else ("tient" if exige else "affiché"),
                         r["faux_strict"] / r["mondes"], r["faux_strict"] / r["mondes"] / seuil_strict, "",
                         r["non_calculables"], r["secondes"]), flush=True)
            ps = binomiale_au_dessus(cumul[0], cumul[1], seuil_strict)
            depasse = exige and ps < NIVEAU_DE_L_ALERTE
            if depasse:
                rouges.append("%s / %s au seuil strict : %d sur %d" % (nom, scenario, cumul[0], cumul[1]))
            print("  %-22s %-36s TOUS | seuil strict : %d faux sur %d mondes = %.5f (promis %.5f, attendu %.1f) "
                  "P(au moins autant) = %.3g → %s" % (nom, scenario, cumul[0], cumul[1], cumul[0] / cumul[1],
                                                       seuil_strict, cumul[1] * seuil_strict, ps,
                                                       "DÉPASSÉ" if depasse else ("tient" if exige else "affiché")))
    print("\nPRÉCISION DES TIRAGES (vraie série des 100 opérations de C5, seuil strict, 30 graines) :")
    for l in precision_des_tirages(J, racine, seuil_strict):
        print(l)
    if trous:
        print("\nCASES NON MESURÉES (R-734) : " + " ; ".join(trous))
        return 2
    if rouges:
        print("\nVERDICT : PROMESSE DÉPASSÉE — " + " ; ".join(rouges))
        return 1
    print("\nVERDICT : chaque case exigée tient le risque promis aux deux seuils (test binomial à %g)" % NIVEAU_DE_L_ALERTE)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
