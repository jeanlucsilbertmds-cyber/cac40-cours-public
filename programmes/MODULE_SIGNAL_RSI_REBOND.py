#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE_SIGNAL_RSI_REBOND.py — Mer 11-11-2026 16h34 (Paris) · corrigé le Mer 11-11-2026 17h56 et 18h06 (Paris)
EN ESSAI · module de signal · Rôle : le signal d'achat de la fiche IND-001-RETEST — « BAISSE IMPORTANTE — PARI SUR REBOND : RSI 14 jours repasse au-dessus de 30 ».
Quand l'appeler : jamais directement ; une fiche du registre des stratégies le nomme, et le juge le joue.

SIMULATION UNIQUEMENT : ce module dit quelles séances déclencheraient un achat simulé. Aucun ordre réel.

ÉCRIT PAR UN AGENT DU DÉROULÉ DU 11-11-2026 (branche locale deroule-ind001), À LA DEMANDE DU CHAT. Relu une fois par
un relecteur neuf (verdict rapporté par le Chat à 17h56 : « DÉPLOYABLE APRÈS CORRECTIONS ») ; corrigé ici ; NON
VALIDÉ, NON FUSIONNÉ.

COMMENT UNE FICHE LE NOMME (A-542, 30-10-2026) — trois colonnes de `donnees/cac40_strategies.csv` :
    module_signal   = programmes/MODULE_SIGNAL_RSI_REBOND.py
    fonction_signal = signaux_rsi_rebond
    reglages_signal = {"periode": 14, "seuil": 30, "chauffe": 100}

① RÔLE — Décider l'achat de l'idée IND-001-RETEST : le RSI de Wilder à 14 séances était STRICTEMENT SOUS 30 la veille
  et est STRICTEMENT AU-DESSUS de 30 le jour même ; aucun signal pendant les 100 premières séances de la série ; on
  achète à l'ouverture du lendemain (c'est le juge qui le fait, R-601 : entrée à l'ouverture qui suit le signal).
② CONTEXTE D'APPEL — Chargé par `signal_de_la_fiche` de `programmes/JUGE_DES_STRATEGIES.py` pour une fiche qui le
  nomme ; `signaux_rsi_rebond` est appelée par `jouer` du juge, une fois par morceau de série de chaque valeur ;
  `memoire_signaux_rsi_rebond` est lue par l'épreuve d'arrivée des signaux. Épreuve propre du module :
  `tests/EPREUVES_DU_SIGNAL_RSI_REBOND_Mer_11-11-2026.py`.
③ ENTRÉE — Pour `signaux_rsi_rebond` : `ohlcv`, la liste des séances d'UNE valeur, chacune un dictionnaire portant
  au moins `date` (texte AAAA-MM-JJ) et `close` (la clôture, en euros) ; et trois réglages lus dans
  `reglages_signal` de la fiche, sans valeur par défaut : `periode` (séances du lissage, 14), `seuil` (niveau du RSI,
  30), `chauffe` (séances sans signal au début de la série, 100). Pour `memoire_signaux_rsi_rebond` : les mêmes trois
  réglages.
④ CONDITIONS D'ENTRÉE — `periode` entier ≥ 1 ; `seuil` nombre de ]0, 100[ ; `chauffe` entier ≥ 0 (les booléens sont
  refusés). Chaque séance porte une `date` et une clôture finie (ni NaN ni infini) ; les dates sont STRICTEMENT
  croissantes (triées, sans doublon). Tout manquement LÈVE ValueError, avec le rang de la séance en cause et sa date
  quand elle existe : le juge
  met alors la fiche « EN ÉCHEC » au lieu de rendre une liste vide en silence (R-734 : ce qui n'a pas pu se mesurer
  ne se fait pas passer pour un résultat).
⑤ SORTIE — Le module expose `signaux_rsi_rebond`, `memoire_signaux_rsi_rebond` et `rsi_wilder` (reprise du module
  RSI(2)). [rend: 3]
⑥ TRAITEMENT — Voir les deux fonctions. Le RSI n'est PAS recalculé ici : il est pris à `rsi_wilder` de
  `programmes/MODULE_SIGNAL_RSI2_CONNORS.py`, chargé par son chemin à côté de ce fichier.
⑦ UNITÉ — Le RSI va de 0 à 100. `periode` et `chauffe` se comptent en SÉANCES de la série reçue.
⑧ POURQUOI —
  L'IDÉE. Wilder, « New Concepts in Technical Trading Systems » (1978) : un RSI sous 30 dit une valeur « survendue » ;
  sa remontée au-dessus de 30 est la lecture classique d'un rebond qui commence. L'idée vient de IND-001 (archivée :
  elle achetait à la CLÔTURE du jour du signal, prix inconnu avant la fermeture du marché, donc irréalisable). Le RSI
  est pris au module RSI(2) parce que deux implémentations d'une même chose divergent toujours (R-708). Méfiance
  d'usage : une règle publiée perd en moyenne une part de sa performance après publication (McLean & Pontiff,
  2016) ; elle se TESTE sur nos données avant toute conclusion.
  STRICTEMENT AU-DESSUS (décision de Jean-Luc du 11-11-2026 à 17h55, rapportée par le Chat) : le signal exige
  RSI(veille) < 30 ET RSI(jour) > 30 ; un RSI à 30,00 pile, la veille ou le jour, ne déclenche pas. La première
  version écrivait `rv < seuil <= r` : un jour à 30 pile déclenchait.
  LA PÉRIODE DE CHAUFFE (décision de Jean-Luc du 11-11-2026 à 17h55, rapportée par le Chat). Le RSI de Wilder est une
  moyenne LISSÉE : chaque jour, moyenne nouvelle = (moyenne ancienne × 13 + valeur du jour) / 14, pour 14 séances.
  Le point de départ du calcul ne disparaît donc jamais tout à fait : après n séances, il pèse encore (13/14)^n dans
  la moyenne (un POIDS, pas des points de RSI) — 35 % après 14 séances, 11 % après 30, 2,5 % après 50, 0,06 % après 100 (calcul : (13/14)^14 = 0,354 ;
  ^30 = 0,108 ; ^50 = 0,0246 ; ^100 = 0,000605). Conséquence : le même jour, la même valeur peut avoir un RSI
  différent selon la date où la série commence, et ce écart peut faire passer le RSI d'un côté ou de l'autre de 30.
  EXEMPLE RÉEL, VINCI, fichier maître des cours `donnees/cours_maitre.csv` : le 07-04-2025, RSI(14) = 29,78 calculé
  depuis le début de l'historique (2024-01-02), mais 30,01 calculé depuis le 13-01-2025 (60 séances plus tôt :
  60 rangs du fichier maître séparent le 13-01-2025 du 07-04-2025, mesuré le 11-11-2026). Avec
  le premier calcul, le 08-04-2025 (RSI 37,82) est un signal ; avec le second, la veille n'est plus sous 30, et il
  n'y a pas de signal. Après 100 séances, le POIDS du point de départ tombe à 0,06 % ; en points de RSI, mesuré le 11-11-2026 sur le
  fichier maître : au-delà du rang 100, une série commencée 20 séances plus tard laisse encore jusqu'à 0,049 point
  d'écart (DASSAULT SYSTEMES, 2024-06-24) — assez peu pour ne changer un signal que si le RSI frôle 30 à moins de
  0,05 point. On ne signale donc RIEN
  pendant les 100 premières séances de chaque série reçue. La chauffe et le seuil se lisent dans les réglages de la
  fiche, jamais en dur.
⑨ CE QUI CLOCHE — ① Dépendance : si `MODULE_SIGNAL_RSI2_CONNORS.py` est renommé ou déplacé, ce module ne se charge
  plus (le juge le refuse alors « ne se charge pas » ; il ne se trompe pas en silence). ② La chauffe compte les
  séances de la SÉRIE REÇUE : le juge coupe les séries aux trous et appelle la fonction morceau par morceau, donc
  chaque morceau a sa propre chauffe ; le maître n'a aucun trou au 11-11-2026 (juge : « 0 coupures »). ③ Une série
  plate rend un RSI indéfini (`rsi_wilder` rend None) : aucun signal ce jour-là, sans erreur.
⑩ EFFET — LIT `programmes/MODULE_SIGNAL_RSI2_CONNORS.py` et l'exécute au chargement (il ne fait que définir des
  fonctions) ; n'écrit rien, ne touche pas au réseau.
⑪ TERMINAISON — Rend la main ; lève l'erreur de chargement si le module RSI(2) manque. [sort: non]
"""
import importlib.util
import math
import os
import re

_CHEMIN_RSI2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MODULE_SIGNAL_RSI2_CONNORS.py")
_spec = importlib.util.spec_from_file_location("module_signal_rsi2_pour_rebond", _CHEMIN_RSI2)
_RSI2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_RSI2)
rsi_wilder = _RSI2.rsi_wilder


def _controler_reglages(periode, seuil, chauffe):
    """Refuse des réglages mal formés.

    ① RÔLE — La seule écriture du contrôle des réglages, partagée par les deux fonctions publiques.
    ② CONTEXTE D'APPEL — `signaux_rsi_rebond` et `memoire_signaux_rsi_rebond`, à leur entrée.
    ③ ENTRÉE — `periode`, `seuil`, `chauffe` : les réglages lus dans la fiche.
    ④ CONDITIONS D'ENTRÉE — Aucune : c'est elle qui les vérifie.
    ⑤ SORTIE — Aucune valeur. [rend: rien]
    ⑥ TRAITEMENT — ① `periode` entier ≥ 1 · ② `seuil` nombre de ]0, 100[ · ③ `chauffe` entier ≥ 0 ; un booléen est refusé
      partout (en Python, vrai vaut 1).
    ⑦ UNITÉ — Séances pour `periode` et `chauffe` ; points de RSI pour `seuil`.
    ⑧ POURQUOI — Une valeur mal tapée dans la fiche (« 14 » en texte) doit arrêter le jeu, pas être devinée.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError. [sort: non]
    """
    if isinstance(periode, bool) or not isinstance(periode, int) or periode < 1:
        raise ValueError("signaux_rsi_rebond : la periode doit etre un entier >= 1 (lu %r)" % (periode,))
    if isinstance(seuil, bool) or not isinstance(seuil, (int, float)) or not 0 < seuil < 100:
        raise ValueError("signaux_rsi_rebond : le seuil doit etre un nombre de ]0, 100[ (lu %r)" % (seuil,))
    if isinstance(chauffe, bool) or not isinstance(chauffe, int) or chauffe < 0:
        raise ValueError("signaux_rsi_rebond : la chauffe doit etre un entier >= 0 (lu %r)" % (chauffe,))


def signaux_rsi_rebond(ohlcv, periode, seuil, chauffe):
    """Rend les séances où le RSI passe de strictement sous le seuil à strictement au-dessus, pour UNE valeur.

    ① RÔLE — Décider les achats de l'idée IND-001-RETEST.
    ② CONTEXTE D'APPEL — `jouer` du juge, à travers le `SignalNomme` rendu par `signal_de_la_fiche`, une fois par
      morceau de série de chaque valeur de l'univers de la fiche ; l'épreuve du module.
    ③ ENTRÉE — `ohlcv` : les séances d'UNE valeur, dictionnaires portant `date` (AAAA-MM-JJ) et `close` · `periode`,
      `seuil`, `chauffe` : lus dans `reglages_signal` ; aucun n'a de valeur par défaut, la fiche les nomme (A-542).
    ④ CONDITIONS D'ENTRÉE — Réglages : `periode` entier ≥ 1, `seuil` nombre de ]0, 100[, `chauffe` entier ≥ 0, aucun
      booléen (contrôlés par `_controler_reglages`). Séances : chacune porte `date` et une clôture convertible en
      nombre fini ; dates strictement croissantes. La fonction NE TRIE PAS : elle refuse, par ValueError, avec le
      rang et la date de la séance en cause (date absente, clôture absente, vide, illisible, None, NaN ou infinie,
      date pas strictement après la précédente).
    ⑤ SORTIE — UNE valeur : la liste des {"i": rang, "rsi": valeur, "rsi_veille": valeur} des séances signalées,
      vide si aucune. Exemples calculés à la main (chauffe 0) : clôtures 10, 9, 8, 9, période 2 → RSI None, None, 0, 50 ;
      au seuil 30 → [{"i": 3, …}] ; au seuil 50 → [] (50 n'est pas STRICTEMENT au-dessus de 50). Exemple réel (fichier
      maître, période 14, seuil 30, chauffe 100) : VINCI, RSI 29,776 le 07-04-2025 et 37,820 le 08-04-2025 → signal
      le 08-04-2025 (rang 324), achat à l'ouverture du 09-04-2025 (107,75 €).
      [rend: 1]
    ⑥ TRAITEMENT — ① contrôler les réglages · ② contrôler chaque séance : date présente, clôture finie, date
      strictement après la précédente · ③ calculer le RSI (`rsi_wilder`) · ④ retenir chaque séance de rang ≥ `chauffe`
      dont la veille a un RSI < seuil et le jour un RSI > seuil.
    ⑦ UNITÉ — RSI de 0 à 100 ; `periode`, `chauffe` et `i` en SÉANCES de la série reçue.
    ⑧ POURQUOI — Le franchissement et non l'état : un seul achat par sortie de survente. « Strictement » des deux
      côtés (décision de Jean-Luc du 11-11-2026 à 17h55) : un RSI à 30 pile, la veille ou le jour, ne déclenche pas.
      La chauffe (même décision) : le RSI de Wilder garde un poids (13/14)^n de son point de départ ; tant que la
      série est courte, le même jour peut tomber d'un côté ou de l'autre du seuil selon la date où la série commence
      (VINCI, 07-04-2025 : 29,78 depuis 2024-01-02, 30,01 depuis 2025-01-13) ; après 100 séances, ce poids n'est plus
      que de 0,06 %.
    ⑨ CE QUI CLOCHE — La chauffe compte les séances de la SÉRIE REÇUE : le juge coupe les séries aux trous et appelle
      la fonction morceau par morceau, donc chaque morceau a sa propre chauffe (aucun trou dans le maître au
      11-11-2026). Au-delà de la chauffe, un départ différent laisse encore jusqu'à 0,049 point de RSI d'écart.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError (réglage mal formé, séance sans date ou dont la date n'est pas un texte
      AAAA-MM-JJ — relecture Cowork du 11-11-2026, RB-3 —, clôture absente,
      illisible, None, NaN ou infinie, dates non croissantes). Aucun de ses appels ne peut ne pas revenir : ses boucles et celle de `rsi_wilder` sont bornées
      par le nombre de séances. [sort: non]
    """
    _controler_reglages(periode, seuil, chauffe)
    clotures = []
    precedente = None
    for k, b in enumerate(ohlcv):
        d = b.get("date")
        if not isinstance(d, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            raise ValueError("signaux_rsi_rebond : la seance de rang %d n'a pas de date lisible AAAA-MM-JJ (lu %r)" % (k, d))
        try:
            c = float(b["close"])
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError("signaux_rsi_rebond : cloture illisible au rang %d, date %s (%s: %s)"
                             % (k, d, type(e).__name__, e))
        if not math.isfinite(c):
            raise ValueError("signaux_rsi_rebond : cloture non finie (%r) au rang %d, date %s" % (c, k, d))
        if precedente is not None and not d > precedente:
            raise ValueError("signaux_rsi_rebond : dates non strictement croissantes au rang %d (%s apres %s)"
                             % (k, d, precedente))
        precedente = d
        clotures.append(c)
    rsi = rsi_wilder(clotures, periode)
    out = []
    for i in range(max(1, chauffe), len(clotures)):
        r, rv = rsi[i], rsi[i - 1]
        if r is None or rv is None:
            continue
        if rv < seuil and r > seuil:
            out.append({"i": i, "rsi": r, "rsi_veille": rv})
    return out


def memoire_signaux_rsi_rebond(periode, seuil, chauffe):
    """Rend la mémoire de `signaux_rsi_rebond` à ces réglages : le nombre de séances, jour décidé compris, dont elle a besoin.

    ① RÔLE — Déclarer, à côté de la fonction de signal, combien de séances passées elle lit, pour l'épreuve d'arrivée
      des signaux (`tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py`, décision de Jean-Luc du 06-11-2026 à
      19h41).
    ② CONTEXTE D'APPEL — `memoire_declaree` de l'épreuve d'arrivée des signaux, qui la trouve par son nom.
    ③ ENTRÉE — `periode`, `seuil`, `chauffe` : les réglages de `signaux_rsi_rebond`, tels que la fiche les nomme.
    ④ CONDITIONS D'ENTRÉE — Celles de `_controler_reglages`.
    ⑤ SORTIE — UNE valeur : un entier. Exemple : (14, 30, 100) → 615. [rend: 1]
    ⑥ TRAITEMENT — ① contrôler les réglages · ② rendre le plus grand de `memoire_signaux_rsi2(periode, seuil, 0)` du
      module RSI(2) (le jour, la veille et l'oubli du lissage de Wilder) et de `chauffe + 1`.
    ⑦ UNITÉ — Des séances de bourse, le jour décidé compris.
    ⑧ POURQUOI — La décision du jour i lit le RSI du jour et de la veille, comme `signaux_rsi2` : ce calcul n'est pas
      réécrit (R-708). LA CHAUFFE EN DÉPEND : une coupe plus courte que `chauffe + 1` séances mettrait le jour décidé
      dans la chauffe et lui retirerait un signal que la série entière donne ; il faut donc au moins `chauffe + 1`
      séances. Aux réglages de la fiche, l'oubli du lissage (615) domine la chauffe (101).
    ⑨ CE QUI CLOCHE — Si la fonction de signal se met à lire plus loin, ce chiffre ne suit pas de lui-même ; l'épreuve
      d'arrivée des signaux le refuserait. NON ÉPROUVÉ par cette épreuve-là (elle tourne aussi sur les 20 ans).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError sur un réglage mal formé. [sort: non]
    """
    _controler_reglages(periode, seuil, chauffe)
    return max(_RSI2.memoire_signaux_rsi2(periode, seuil, 0), chauffe + 1)
