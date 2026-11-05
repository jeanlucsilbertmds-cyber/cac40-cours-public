#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE_SIGNAL_RSI2_CONNORS.py — Ven 30-10-2026 20h00 (Paris)
EN ESSAI · module de signal · Rôle : le signal d'achat RSI(2) de Larry Connors — acheter quand le RSI à très court
terme passe sous un seuil de survente, éventuellement au-dessus d'une moyenne mobile longue.
Quand l'appeler : jamais directement ; une fiche du registre des stratégies le nomme, et le juge le joue.

SIMULATION UNIQUEMENT : ce module dit quelles séances déclencheraient un achat simulé. Aucun ordre réel.

COMMENT UNE FICHE LE NOMME (A-542, 30-10-2026) — trois colonnes de `donnees/cac40_strategies.csv` :
    module_signal   = programmes/MODULE_SIGNAL_RSI2_CONNORS.py
    fonction_signal = signaux_rsi2
    reglages_signal = {"periode": 2, "seuil": 10, "tendance": 200}

① RÔLE — Une troisième famille de signal, simple et publiée, branchée sans toucher au juge : la preuve qu'une
  famille s'ajoute par son module et sa fiche, et rien d'autre.
② CONTEXTE D'APPEL — Chargé par `signal_de_la_fiche` de `programmes/JUGE_DES_STRATEGIES.py`, pour une fiche qui le
  nomme ; `signaux_rsi2` est appelée par `jouer` du juge, une fois par morceau de série de chaque valeur.
③ ENTRÉE — Voir `signaux_rsi2`.
④ CONDITIONS D'ENTRÉE — Voir `signaux_rsi2`.
⑤ SORTIE — Le module expose `signaux_rsi2` et `rsi_wilder`. [rend: 2]
⑥ TRAITEMENT — Voir les deux fonctions.
⑦ UNITÉ — Le RSI va de 0 à 100. Les périodes se comptent en SÉANCES.
⑧ POURQUOI — Connors et Alvarez, « Short Term Trading Strategies That Work » (2008), chapitre sur le RSI(2) :
  acheter une valeur au-dessus de sa moyenne mobile à 200 séances quand son RSI à 2 séances descend sous 10 (ou 5).
  C'est une règle de retour vers la moyenne, à l'opposé des signaux de suivi ; elle sert ici de famille témoin. La
  règle publiée sort sur une clôture au-dessus de la moyenne à 5 séances : le juge, lui, sort par l'objectif, la
  perte acceptée et l'horizon de la FICHE (les sorties viennent du module des positions, jamais du signal). Ce
  module ne reproduit donc que l'ENTRÉE de Connors. Méfiance d'usage : une règle publiée perd en moyenne une part de
  sa performance après publication (McLean & Pontiff, 2016) ; elle se TESTE sur nos données avant toute conclusion.
⑨ CE QUI CLOCHE — ① Seule l'entrée de Connors est reproduite (voir ⑧). ② « Passe sous » est lu comme un
  FRANCHISSEMENT (la veille au-dessus ou au seuil, le jour en dessous) : la règle publiée achète tant que le RSI est
  sous le seuil ; une fiche qui voudrait l'état et non le franchissement demanderait une autre fonction.
⑩ EFFET — Aucun : n'écrit rien, ne lit rien, ne touche pas au réseau. Le charger ne fait que définir des fonctions.
⑪ TERMINAISON — Rend la main. [sort: non]
"""


def rsi_wilder(clotures, periode):
    """Rend le RSI de Wilder, séance par séance.

    ① RÔLE — Calculer l'indice de force relative, lissé à la manière de Wilder (1978), sur une liste de clôtures.
    ② CONTEXTE D'APPEL — `signaux_rsi2`, une fois par appel ; l'épreuve du signal nommé, sur un cas calculé à la main.
    ③ ENTRÉE — `clotures` : les clôtures, dans l'ordre des dates · `periode` : le nombre de séances du lissage.
    ④ CONDITIONS D'ENTRÉE — `periode` est un entier ≥ 1 (contrôlé par `signaux_rsi2`).
    ⑤ SORTIE — UNE valeur : une liste de même longueur que `clotures`, None tant que le RSI n'est pas défini.
      Exemple calculé à la main : clôtures 10, 11, 10, 9 à la période 2 → None, None, 50, 25.
      [rend: 1]
    ⑥ TRAITEMENT — ① variations d'une clôture à la suivante, séparées en hausses et baisses · ② à la séance
      `periode`, moyennes simples des `periode` premières hausses et baisses · ③ ensuite, lissage de Wilder :
      moyenne = (moyenne × (période − 1) + valeur du jour) / période · ④ RSI = 100 − 100 / (1 + hausses / baisses) ;
      100 si aucune baisse, None si ni hausse ni baisse.
    ⑦ UNITÉ — De 0 à 100.
    ⑧ POURQUOI — Le lissage de Wilder est celui des plateformes de marché (ProRealTime compris) et de Connors.
    ⑨ CE QUI CLOCHE — Une série plate (ni hausse ni baisse sur la fenêtre) rend None et non 50 : aucun signal n'en
      sort, ce qui est voulu, mais un autre logiciel afficherait 50 ou 100.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; boucle bornée par la longueur de la liste.
      [sort: non]
    """
    n = len(clotures)
    out = [None] * n
    if n <= periode:
        return out
    hausses = [0.0] + [max(clotures[k] - clotures[k - 1], 0.0) for k in range(1, n)]
    baisses = [0.0] + [max(clotures[k - 1] - clotures[k], 0.0) for k in range(1, n)]
    mh = sum(hausses[1:periode + 1]) / periode
    mb = sum(baisses[1:periode + 1]) / periode
    for k in range(periode, n):
        if k > periode:
            mh = (mh * (periode - 1) + hausses[k]) / periode
            mb = (mb * (periode - 1) + baisses[k]) / periode
        if mb == 0:
            out[k] = 100.0 if mh > 0 else None
        else:
            out[k] = 100.0 - 100.0 / (1.0 + mh / mb)
    return out


def signaux_rsi2(ohlcv, periode, seuil, tendance):
    """Rend les séances où le RSI passe sous le seuil, pour UNE valeur.

    ① RÔLE — Décider les achats de la famille RSI(2) : le RSI à `periode` séances franchit le seuil vers le bas, et,
      si `tendance` est non nul, la clôture est au-dessus de sa moyenne mobile simple à `tendance` séances.
    ② CONTEXTE D'APPEL — `jouer` du juge, à travers le `SignalNomme` rendu par `signal_de_la_fiche`, une fois par
      morceau de série de chaque valeur de l'univers de la fiche.
    ③ ENTRÉE — `ohlcv` : la liste des séances d'UNE valeur, triées par date, chacune portant `close` · `periode`,
      `seuil`, `tendance` : lus dans `reglages_signal` ; aucun n'a de valeur par défaut, la fiche les nomme (A-542).
    ④ CONDITIONS D'ENTRÉE — `periode` entier ≥ 1 ; `seuil` nombre de ]0, 100[ ; `tendance` entier ≥ 0 (0 = sans
      filtre de tendance). Les séances sont triées et sans doublon : la fonction ne trie pas.
    ⑤ SORTIE — UNE valeur : la liste des {"i": rang, "rsi": valeur} des séances signalées, vide si aucune. Exemple
      calculé à la main : clôtures 10, 11, 10, 9, période 2, seuil 30, tendance 0 → [{"i": 3, "rsi": 25.0}].
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser un réglage mal formé · ② calculer le RSI (`rsi_wilder`) · ③ pour chaque séance dont
      la veille a un RSI, retenir celle où le RSI de la veille est ≥ seuil et celui du jour < seuil · ④ avec un
      filtre de tendance, n'en garder que les séances dont la clôture est strictement au-dessus de la moyenne des
      `tendance` dernières clôtures, jour compris ; sans assez d'histoire pour la moyenne, aucun signal.
    ⑦ UNITÉ — RSI de 0 à 100 ; `periode` et `tendance` en SÉANCES ; `i` : rang dans `ohlcv`.
    ⑧ POURQUOI — Voir l'en-tête du module, ⑧ (Connors et Alvarez, 2008). Le franchissement plutôt que l'état : un seul
      achat par passage en survente, comme les autres familles du projet, dont le signal est un croisement.
    ⑨ CE QUI CLOCHE — ① Le juge coupe les séries aux trous et appelle la fonction morceau par morceau : la moyenne à
      200 séances recommence à chaque morceau, et un morceau plus court que `tendance` ne signale rien. ② Voir
      l'en-tête, ⑨.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError sur un réglage mal formé ; boucles bornées par le nombre de
      séances.
      [sort: non]
    """
    if isinstance(periode, bool) or not isinstance(periode, int) or periode < 1:
        raise ValueError("signaux_rsi2 : la periode doit etre un entier >= 1 (lu %r)" % (periode,))
    if isinstance(seuil, bool) or not isinstance(seuil, (int, float)) or not 0 < seuil < 100:
        raise ValueError("signaux_rsi2 : le seuil doit etre un nombre de ]0, 100[ (lu %r)" % (seuil,))
    if isinstance(tendance, bool) or not isinstance(tendance, int) or tendance < 0:
        raise ValueError("signaux_rsi2 : la tendance doit etre un entier >= 0 (lu %r)" % (tendance,))
    clotures = [float(b["close"]) for b in ohlcv]
    rsi = rsi_wilder(clotures, periode)
    out = []
    for i in range(1, len(clotures)):
        r, rv = rsi[i], rsi[i - 1]
        if r is None or rv is None or not (rv >= seuil and r < seuil):
            continue
        if tendance:
            if i + 1 < tendance:
                continue
            if clotures[i] <= sum(clotures[i - tendance + 1:i + 1]) / tendance:
                continue
        out.append({"i": i, "rsi": r})
    return out
