#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE_SIGNAL_AU_HASARD.py — Ven 30-10-2026 19h55 (Paris)
EN ESSAI · module de signal · Rôle : un signal d'achat TIRÉ AU SORT, témoin négatif de la famille des signaux.
Quand l'appeler : jamais directement ; une fiche du registre des stratégies le nomme, et le juge le joue.

SIMULATION UNIQUEMENT : ce module dit quelles séances déclencheraient un achat simulé. Aucun ordre réel.

COMMENT UNE FICHE LE NOMME (A-542, 30-10-2026) — trois colonnes de `donnees/cac40_strategies.csv` :
    module_signal   = programmes/MODULE_SIGNAL_AU_HASARD.py
    fonction_signal = signaux_au_hasard
    reglages_signal = {"graine": 7, "proportion": 0.02}

① RÔLE — Fournir un signal qui ne sait RIEN du marché : à chaque séance, un tirage à graine fixe décide si la valeur
  est achetée. Joué par le juge exactement comme un vrai signal, il dit ce que rapporte le seul fait d'acheter
  au hasard dans l'univers, aux mêmes seuils et aux mêmes frais : une stratégie qui ne le bat pas nettement ne
  prouve rien.
② CONTEXTE D'APPEL — Chargé par `signal_de_la_fiche` de `programmes/JUGE_DES_STRATEGIES.py`, pour une fiche qui le
  nomme ; sa fonction est appelée par `jouer` du juge, une fois par morceau de série de chaque valeur.
③ ENTRÉE — Voir `signaux_au_hasard`.
④ CONDITIONS D'ENTRÉE — Voir `signaux_au_hasard`.
⑤ SORTIE — Le module expose `signaux_au_hasard` et `memoire_signaux_au_hasard`. [rend: 2]
⑥ TRAITEMENT — Voir `signaux_au_hasard`.
⑦ UNITÉ — La proportion est une FRACTION des séances (0,02 = 2 %).
⑧ POURQUOI — A-542 ④ (plan du circuit validé par Jean-Luc le 30-10-2026) : chaque famille de signal se branche par
  son module et sa fiche ; un signal au hasard est le premier témoin négatif, pour vérifier que le circuit ne
  fabrique pas de gain là où il n'y a aucune information. L'étalon de hasard du juge (`MODULE_JUGEMENT.etalon_hasard`)
  tire, lui, autour des opérations d'une stratégie ; ce module en fait une STRATÉGIE à part entière, jugée comme
  les autres.
⑨ CE QUI CLOCHE — Voir `signaux_au_hasard`, ⑨.
⑩ EFFET — Aucun : n'écrit rien, ne lit rien, ne touche pas au réseau. Le charger ne fait que définir des fonctions.
⑪ TERMINAISON — Rend la main. [sort: non]
"""
import hashlib


def tirage(graine, date, cloture):
    """Rend le tirage d'une séance : un nombre de [0, 1) qui ne dépend que de la graine, de la date et de la clôture.

    ① RÔLE — Le dé de ce module : le même trio rend toujours le même nombre, quels que soient l'ordre des appels, la
      machine ou la version de Python.
    ② CONTEXTE D'APPEL — `signaux_au_hasard`, une fois par séance ; l'épreuve du signal nommé, pour vérifier la
      reproductibilité.
    ③ ENTRÉE — `graine` : un entier · `date` : la date de la séance, AAAA-MM-JJ · `cloture` : sa clôture.
    ④ CONDITIONS D'ENTRÉE — `cloture` se convertit en nombre.
    ⑤ SORTIE — UNE valeur : un nombre de [0, 1).
      [rend: 1]
    ⑥ TRAITEMENT — ① écrire « graine|date|clôture » (clôture en nombre à virgule, écriture la plus courte de Python)
      · ② en prendre l'empreinte SHA-256 · ③ lire ses 8 premiers octets comme un entier et le diviser par 2⁶⁴.
    ⑦ UNITÉ — Sans unité.
    ⑧ POURQUOI — Un générateur aléatoire tiré dans l'ordre des appels rendrait un tirage qui dépend de l'ordre des
      valeurs et de la coupure des séries aux trous ; et une graine seule, sans rien de la valeur, ferait acheter
      TOUTES les valeurs les mêmes jours. La fonction de signal ne connaît pas le nom de la valeur : la clôture du
      jour la distingue. SHA-256 rend un tirage uniforme et identique partout (`random` dépend de la version).
    ⑨ CE QUI CLOCHE — Une clôture révisée change le tirage de sa séance. Deux valeurs de même clôture le même jour
      tirent le même nombre (rare, et sans effet sur l'absence d'information du signal).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main, ou lève ValueError si la clôture n'est pas un nombre.
      [sort: non]
    """
    texte = "%d|%s|%r" % (graine, date, float(cloture))
    return int.from_bytes(hashlib.sha256(texte.encode("utf-8")).digest()[:8], "big") / 2.0 ** 64


def signaux_au_hasard(ohlcv, graine, proportion):
    """Rend les séances où le tirage décide un achat, pour UNE valeur.

    ① RÔLE — Choisir, séance par séance et valeur par valeur, les achats d'une stratégie qui ne sait rien.
    ② CONTEXTE D'APPEL — `jouer` du juge, à travers le `SignalNomme` rendu par `signal_de_la_fiche`, une fois par
      morceau de série de chaque valeur de l'univers de la fiche. Aucun autre appelant dans le circuit.
    ③ ENTRÉE — `ohlcv` : la liste des séances d'UNE valeur, triées par date, chacune portant `date` et `close` ·
      `graine` : un entier, lu dans `reglages_signal` · `proportion` : la part des séances tirées, lue dans
      `reglages_signal`. Ni la graine ni la proportion n'ont de valeur par défaut : la fiche les nomme (A-542).
    ④ CONDITIONS D'ENTRÉE — `graine` est un entier (pas un booléen) ; `proportion` est un nombre de ]0, 1].
    ⑤ SORTIE — UNE valeur : la liste des {"i": rang, "tirage": t} des séances tirées, vide si aucune. Exemple : sur
      100 séances à la proportion 0,02, environ 2 séances.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser une graine ou une proportion mal formées · ② pour chaque séance, tirer
      (`tirage`) et retenir la séance si le tirage est inférieur à la proportion.
    ⑦ UNITÉ — `proportion` : FRACTION des séances. `i` : rang dans `ohlcv`.
    ⑧ POURQUOI — Un témoin négatif : à graine égale, les mêmes achats (reproductible) ; à graine différente, d'autres
      achats (la graine compte). Il tire aussi la DERNIÈRE séance : le juge écarte lui-même un signal sans lendemain.
    ⑨ CE QUI CLOCHE — ① Le tirage dépend de la clôture (voir `tirage`, ⑨). ② Une proportion trop forte fait acheter
      presque chaque jour : le juge joue alors toutes ces opérations (comptabilité des jetons illimités), ce qui n'a
      pas de sens pour un portefeuille réel ; c'est la fiche qui fixe la proportion.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError sur un réglage mal formé ; un appel ne peut pas ne pas
      revenir : une boucle bornée par le nombre de séances.
      [sort: non]
    """
    if isinstance(graine, bool) or not isinstance(graine, int):
        raise ValueError("signaux_au_hasard : la graine doit etre un entier (lu %r)" % (graine,))
    if isinstance(proportion, bool) or not isinstance(proportion, (int, float)) or not 0 < proportion <= 1:
        raise ValueError("signaux_au_hasard : la proportion doit etre un nombre de ]0, 1] (lu %r)" % (proportion,))
    out = []
    for i, b in enumerate(ohlcv):
        t = tirage(graine, b["date"], b["close"])
        if t < proportion:
            out.append({"i": i, "tirage": t})
    return out


def memoire_signaux_au_hasard(graine, proportion):
    """Rend la mémoire de `signaux_au_hasard` : une séance, le jour décidé lui-même.

    ① RÔLE — Déclarer, à côté de la fonction de signal, combien de séances passées elle lit, pour que l'épreuve
      d'arrivée des signaux (`tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py`) ne lui donne, sur les 20 ans,
      que ces séances-là pour chaque date vérifiée (décision de Jean-Luc du 06-11-2026 à 19h41).
    ② CONTEXTE D'APPEL — `memoire_declaree` de l'épreuve d'arrivée des signaux, qui la trouve par son nom (« memoire_ »
      suivi du nom de la fonction de signal) et lui passe les réglages de la fiche. Aucun programme du circuit du soir
      ne l'appelle.
    ③ ENTRÉE — `graine`, `proportion` : les réglages de `signaux_au_hasard` ; ils n'entrent pas dans le calcul.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 1.
      [rend: 1]
    ⑥ TRAITEMENT — Rendre 1.
    ⑦ UNITÉ — Des séances de bourse, le jour décidé compris.
    ⑧ POURQUOI — Lu dans `signaux_au_hasard` et `tirage` : le tirage d'une séance ne dépend que de la graine, de la date
      et de la clôture de cette séance. Mesuré par l'étude « 54 heures » (06-11-2026, hors dépôt) : avec une mémoire
      de 1, le hasard passe sur toutes les valeurs des deux fichiers. L'épreuve VÉRIFIE ce chiffre à chaque lancement,
      par décalage (`verifier_la_memoire`).
    ⑨ CE QUI CLOCHE — Les réglages sont reçus pour que l'épreuve appelle toutes les fonctions de mémoire de la même
      façon ; ils ne servent pas.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return 1
