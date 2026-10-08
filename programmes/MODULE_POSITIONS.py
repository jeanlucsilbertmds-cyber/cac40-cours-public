# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════
# MODULE POSITIONS — CAC 40 · gestion des positions simulées
# Transpose en Python la logique de la procédure de tenue des positions
# qui vivait dans un texte de consigne, remplacée par ce module le 11-08-2026.
# Le prompt devient minimal : il APPELLE ce module, il ne décrit plus.
# VERSION 1.0 — Mar 11-08-2026 23h05 (Paris).
# NOM FIXE : ce fichier ne sera jamais renommé ni horodaté, parce que d'autres
# programmes le chargent par son nom ; un nom qui change casse tous ses lecteurs
# en silence. (R-713)
# Simulations uniquement — aucun ordre réel.
#
# RÈGLES TRANSPOSÉES ICI. Elles venaient de trois endroits : une consigne en
# français appliquée à la main, la décision du 29-07-2026 sur les quatre tests de
# sortie (D-290726-01), et le module de la stratégie C5-étendu-10.
#  · Entrée à l'Open J+1 ; TP = entrée ×1,040 ; SL = entrée ×0,975 ;
#    horizon 20 séances de bourse après l'entrée.
#  · Clôture : 4 tests DANS CET ORDRE par séance (l'ouverture d'abord ;
#    ordre du 30-09-2026, R-607 ③ — avant, 2 et 3 étaient inversés) :
#      1. Open <= SL  → sortie à l'OUVERTURE, motif SL_GAP
#      2. Open >= TP  → sortie à l'OUVERTURE,  motif TP_GAP
#      3. Low  <= SL  → sortie au prix SL,     motif SL
#      4. High >= TP  → sortie au prix TP,     motif TP
#    Aucun déclenchement en 20 séances → sortie au Close, motif HORIZON.
#  · DEUX montants, toujours : le RÉEL (prix de sortie effectif) et la
#    CONVENTION du backtest (prix TP/SL théorique) — colonnes séparées.
#  · Frais : 0,15 % par ordre sur la VALEUR ÉCHANGÉE (quantité × prix),
#    à l'entrée ET à la sortie. Jamais de forfait. (tranché le 11-08-2026 ;
#    Tranché par Jean-Luc le 11-08-2026 : 0,15 % par ordre, le tarif réel du
#    compte Fortuneo Progress — et non un forfait. (A-50))
#  · Capital : 100 000 € par stratégie ; quantité fractionnaire.
# ══════════════════════════════════════════════════════════════

"""MODULE_POSITIONS.py — le moteur de calcul des positions simulées.

════════════════════════════════════════════════════════════════════════
LES ONZE ÉLÉMENTS — ce programme est une fonction comme les autres
════════════════════════════════════════════════════════════════════════
① RÔLE — **LE SEUL ENDROIT OÙ SE CALCULE CE QUE RAPPORTE UN TRADE.** Il ne
  décide rien : il applique les règles de sortie et chiffre le résultat.
  **Il porte le TAUX DE FRAIS, et c est l unique endroit où il est écrit** —
  tout autre programme le LIT dans `FRAIS_TAUX`, jamais ne le recopie.
② CONTEXTE D APPEL — Chargé par `programmes/TENIR_LES_POSITIONS.py`, qui lui
  demande deux choses : les frais d un ordre, et le verdict d une séance.
  **Lancé seul, il ne fait que son calibrage.**
③ ENTRÉE — Aucune ligne de commande, sauf pour le calibrage. **Ce sont ses
  fonctions qui reçoivent : des prix, des séances, des taux.**
④ CONDITIONS D ENTRÉE — Aucune : il ne lit aucun fichier et ne dépend d aucun
  autre programme.
⑤ SORTIE — **Lancé seul : un code de sortie, 0 si le calibrage passe.**
  Utilisé comme module : ce que rendent ses six fonctions.
⑥ TRAITEMENT — Il expose cinq constantes et six fonctions. **Rien ne s exécute
  au chargement**, sinon la définition des constantes.
⑦ UNITÉ — **`CAPITAL` en euros · `TP_PCT`, `SL_PCT` et `FRAIS_TAUX` en
  FRACTIONS, jamais en pourcents — 0,0015 vaut 0,15 %** · `HORIZON` en SÉANCES
  DE BOURSE, jamais en jours calendaires · les prix en euros.
⑧ POURQUOI — **Un seul endroit pour le taux de frais**, parce qu un chiffre
  recopié diverge. **Et DEUX montants pour chaque trade** : le RÉEL, au prix de
  sortie effectif, et la CONVENTION, au prix théorique — **c est ce qui permet
  de comparer une opération vécue à un backtest sans confondre les deux.**
⑨ CE QUI CLOCHE — **Trois silences, aucun corrigé** — le ⑨ se consigne et ne se corrige pas (R-752) :
  · **`TP_PCT` et `SL_PCT` sont écrits ici en dur**, alors que les seuils
    viennent du registre `donnees/cac40_strategies.csv` par stratégie. **Deux
    sources pour la même grandeur** — seul `parametres_entree`, qui les emploie,
    n est plus appelé par le circuit du soir ;
  · **`HORIZON = 20` est écrit ici ET passé par l appelant.** Le même chiffre
    vit à deux endroits ;
  · **le calibrage vérifie la mécanique de sortie, pas le taux de frais lui-même
    dans son usage courant** : il le passe explicitement.
⑩ EFFET — **Aucun. Il n écrit aucun fichier, ne sort pas sur le réseau, ne
  modifie rien.** C est du calcul pur.
⑪ TERMINAISON — **Chargé comme module : rien ne s exécute.** Lancé seul : il
  termine le programme, code 0 si le calibrage passe, 1 sinon.

⑫ DÉFINITIONS —
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub
    Actions — collecte, versement, signaux, positions, mesure, surveillance.
  la convention : le prix de sortie théorique, celui de l'objectif ou du stop, par opposition au prix réellement observé. C'est ce qui permet de comparer une opération vécue à un test sur le passé
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  un trade : une opération simulée, de l'achat à la revente
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""

CAPITAL = 100_000.0
TP_PCT  = 0.040
SL_PCT  = 0.025
HORIZON = 20          # séances de bourse après l'entrée
FRAIS_TAUX = 0.0015   # 0,15 % par ordre (Fortuneo PROGRESS, décision de Jean-Luc du 11-08-2026 (A-50) —
                      # décision de Jean-Luc du 11-08-2026 ; source fortuneo.fr/bourse).
                      # L'HISTORIQUE n'est jamais recalculé : les trades déjà au
                      # journal gardent leurs conventions d'époque.


def frais_ordre(quantite, prix, taux=None):
    """Frais d'UN ordre : taux × valeur échangée (défaut : le taux Fortuneo Progress).

    ① RÔLE — **Chiffrer ce que coûte UN passage d ordre.** Appelée deux fois par
      trade : à l entrée et à la sortie.
    ② CONTEXTE D APPEL — `pnl_net`, deux fois par calcul de résultat. **Et
      `programmes/TENIR_LES_POSITIONS.py` l exige à l import** : sans elle, il
      refuse de charger ce module.
    ③ ENTRÉE — `quantite` : le nombre de titres · `prix` : le prix unitaire ·
      `taux` : le taux de frais, **`None` par défaut, et l appelant ne le passe
      que pour rejouer un trade aux conventions de son époque**.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le montant des frais.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre `FRAIS_TAUX` si aucun taux n est donné ·
      ② multiplier par la valeur échangée.
    ⑦ UNITÉ — **`quantite` en titres, `prix` et le résultat en EUROS, `taux` en
      FRACTION — 0,0015 vaut 0,15 %.** Confondre fraction et pourcent donne un
      résultat cent fois trop grand, et plausible.
    ⑧ POURQUOI — **Les frais portent sur la VALEUR ÉCHANGÉE, jamais un forfait.**
      C est le tarif Fortuneo Progress, tranché le 11-08-2026. **Un forfait de
      300 € a été employé par erreur sur un trade de juillet : l écart de
      10,78 € est figé dans l historique, qui ne se réécrit jamais.**
    ⑨ CE QUI CLOCHE — Rien vu. **Le paramètre `taux` pourrait servir à contourner
      le taux officiel, mais son seul appelant ne le passe qu au calibrage.**
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return (FRAIS_TAUX if taux is None else taux) * quantite * prix


def pnl_net(prix_entree, prix_sortie, taux=None):
    """P&L net d'un aller-retour au capital fixe, frais des 2 ordres.
    `taux` ne sert qu'au calibrage sur l'historique (conventions d'époque).

    ① RÔLE — **Chiffrer ce qu un trade a rapporté ou coûté, frais déduits.**
      C est le résultat qui part au journal des trades.
    ② CONTEXTE D APPEL — `sortie_position`, deux fois par sortie : une fois au
      prix réel, une fois au prix de convention.
    ③ ENTRÉE — `prix_entree` · `prix_sortie` · `taux` : **`None` par défaut**,
      renseigné seulement pour rejouer un trade ancien.
    ④ CONDITIONS D ENTRÉE — **`prix_entree` ne doit pas être nul** : il est au
      dénominateur. Aucun appelant ne peut le rendre nul, mais rien ne l empêche.
    ⑤ SORTIE — UNE valeur : le résultat net.
      [rend: 1]
    ⑥ TRAITEMENT — ① la quantité est `CAPITAL` divisé par le prix d entrée, **et
      elle est fractionnaire** · ② le brut est la variation relative appliquée au
      capital · ③ retrancher les frais des DEUX ordres.
    ⑦ UNITÉ — **Prix et résultat en EUROS, quantité en titres, `taux` en
      FRACTION.**
    ⑧ POURQUOI — **Capital fixe de 100 000 € par trade, quantité fractionnaire.**
      Cela rend deux trades comparables quel que soit le prix de la valeur.
    ⑨ CE QUI CLOCHE — **Une division par `prix_entree` sans garde.** Un prix nul
      lèverait, et l erreur remonterait au milieu d une tenue de positions.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. **Lève si `prix_entree` vaut zéro.**
      [sort: non]
    """
    q = CAPITAL / prix_entree
    brut = CAPITAL * (prix_sortie / prix_entree - 1.0)
    return brut - frais_ordre(q, prix_entree, taux) - frais_ordre(q, prix_sortie, taux)


def parametres_entree(prix_open):
    """À l'entrée (Open J+1) : TP, SL. Arrondis : aucun — valeurs brutes.

    ① RÔLE — Poser les deux seuils de sortie à partir du prix d entrée.
    ② CONTEXTE D APPEL — `sortie_position`. **Plus appelée par le circuit du
      soir depuis le 03-09-2026** : elle imposait les mêmes seuils à toutes les
      stratégies, alors qu ils viennent du registre par stratégie.
    ③ ENTRÉE — `prix_open` : le prix d ouverture de la séance d entrée.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un dictionnaire de TROIS clés — `prix_entree`, `tp`,
      `sl`.
      [rend: 1]
    ⑥ TRAITEMENT — ① recopier le prix d entrée · ② l objectif est le prix majoré
      de `TP_PCT` · ③ le stop est le prix minoré de `SL_PCT`.
    ⑦ UNITÉ — **Prix en euros, `TP_PCT` et `SL_PCT` en FRACTIONS.** Aucun
      arrondi : les valeurs sont brutes, et c est voulu.
    ⑧ POURQUOI — Pas d arrondi, parce qu un arrondi à l entrée se propage à la
      sortie et au résultat.
    ⑨ CE QUI CLOCHE — **Elle emploie `TP_PCT` et `SL_PCT` écrits dans ce fichier,
      alors que les seuils vivent au registre `donnees/cac40_strategies.csv` par
      stratégie. Deux sources pour la même grandeur.** C est précisément pourquoi
      le circuit a cessé de l appeler — **mais elle est toujours appelée par
      `sortie_position`, qui sert au calibrage.**
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return {"prix_entree": prix_open,
            "tp": prix_open * (1.0 + TP_PCT),
            "sl": prix_open * (1.0 - SL_PCT)}


def tester_seance(bar, tp, sl):
    """Applique les quatre tests de sortie décidés le 29-07-2026 (D-290726-01), dans l ordre fixé le 30-09-2026 par R-607 ③, sur UNE séance.
    bar = dict open/high/low/close. Retourne (prix_sortie, motif) ou None.

    ① RÔLE — **Dire si une position sort ce jour-là, et à quel prix.** C est le
      grain le plus fin du moteur.
    ② CONTEXTE D APPEL — `sortie_position`, une fois par séance de détention.
      **Et `programmes/TENIR_LES_POSITIONS.py` l exige à l import.**
    ③ ENTRÉE — `bar` : une séance, avec ses quatre prix · `tp` : l objectif ·
      `sl` : le stop.
    ④ CONDITIONS D ENTRÉE — **`bar` DOIT porter les quatre clés** `open`, `high`,
      `low`, `close`. Une clé absente lève.
    ⑤ SORTIE — **DEUX formes selon la branche** : **DEUX valeurs** — le prix de
      sortie et le motif — quand un seuil est touché · **1 valeur, `None`**,
      quand la position reste ouverte.
      **Selon la branche, elle rend 1 ou 2 valeur(s).**
      [rend: 1 ou 2]
⑥ TRAITEMENT — **Quatre tests DANS CET ORDRE, et l ordre fait le résultat** :
      ① ouverture sous le stop, sortie à l ouverture · ② ouverture au-dessus de
      l objectif, sortie à l ouverture · ③ plus bas sous le stop, sortie au stop ·
      ④ plus haut au-dessus de l objectif, sortie à l objectif. (Ordre du
      30-09-2026 ; avant, ② et ③ étaient inversés.)
    ⑦ UNITÉ — Tous les prix en euros.
    ⑧ POURQUOI — **Les deux sauts d ouverture sont testés AVANT les extrêmes de
      la séance**, parce qu un saut d ouverture s exécute au prix réel et non au
      seuil, et que l ouverture est le premier prix de la séance : une séance qui
      ouvre au-dessus de l objectif puis descend sous le stop a vendu à
      l ouverture, en gain (R-607 ③, décision de Jean-Luc du 27-09-2026 à 16h14,
      exception à R-602). **Sans saut, le stop est testé avant l objectif : dans
      une séance qui touche les deux, on suppose le pire (R-602).**
    ⑨ CE QUI CLOCHE — **L ordre des quatre tests porte tout le sens.** Depuis le
      30-09-2026, `tests/EPREUVES_DE_L_ORDRE_DES_SORTIES_Mer_30-09-2026.py` joue
      sept cas et rougit si l ordre change ; le calibrage du module, lui, ne
      teste qu un saut à la hausse. **Le prix de convention n est pas rendu ici** :
      le programme du soir le déduit du motif (TP… donne l objectif), si bien que
      dans le cas « ouverture au-dessus de l objectif puis plus bas sous le stop »
      il écrit l objectif, quand le backtest (`_c5e10_sortie`, qui teste le plus
      bas d abord) retient le stop — le contrôle n°10 du radar verrait un écart
      sur un tel trade. Aucun trade du passé n est dans ce cas. Consigné au
      BACKLOG le 30-09-2026 (A-506), non réparé : le prix de convention et le contrôle
      n°10 relèvent de A-501, mis en attente par Jean-Luc.
    ⑩ EFFET — Aucun : elle ne modifie pas la séance reçue.
    ⑪ TERMINAISON — Rend la main. **Lève si une clé de prix manque.**
      [sort: non]
    """
    # LES DEUX SAUTS D'OUVERTURE D'ABORD (R-607 ③, décision de Jean-Luc du
    # 27-09-2026 à 16h14) : l'ouverture est le premier prix de la séance ; une
    # séance qui ouvre au-dessus de l'objectif puis descend sous la vente forcée
    # a vendu à l'ouverture, avant la baisse — c'est un gain. Avant le 30-09-2026,
    # le plus bas sous la vente forcée était testé avant le saut favorable, et ce
    # cas comptait une perte.
    if bar["open"] <= sl:
        return bar["open"], "SL_GAP"
    if bar["open"] >= tp:
        return bar["open"], "TP_GAP"
    # SANS SAUT, LE PIRE D'ABORD (R-602, inchangée) : dans une séance qui touche
    # les deux seuils, on ne sait pas lequel est venu en premier.
    if bar["low"] <= sl:
        return sl, "SL"
    if bar["high"] >= tp:
        return tp, "TP"
    return None


def sortie_position(seances, prix_entree):
    """Déroule les séances POSTÉRIEURES à l'entrée, dans l'ordre.
    seances = liste de dict open/high/low/close (J+1 de détention et suivants,
    c'est-à-dire à partir de la séance qui SUIT celle de l'entrée).
    Retourne None si la position reste ouverte, sinon un dict :
      indice_seance (0-based dans `seances`), prix_sortie, motif,
      pnl_net_eur (RÉEL), prix_sortie_convention, pnl_net_convention_eur.
    La CONVENTION remplace un _GAP par le prix théorique (TP ou SL, même
    famille) ; hors gap, les deux couples sont identiques.

    ① RÔLE — **Dérouler une position jusqu à sa sortie, et chiffrer les deux
      résultats.** C est la fonction qui clôt un trade.
    ② CONTEXTE D APPEL — Le calibrage de ce module. **Le circuit du soir ne
      l appelle pas : `programmes/TENIR_LES_POSITIONS.py` déroule lui-même les
      séances, avec les seuils du registre.**
    ③ ENTRÉE — `seances` : les séances POSTÉRIEURES à l entrée, dans l ordre ·
      `prix_entree` : le prix d ouverture de la séance d entrée.
    ④ CONDITIONS D ENTRÉE — **`seances` commence à la séance qui SUIT celle de
      l entrée**, jamais à celle de l entrée. Un décalage d une séance change la
      sortie sans qu aucune erreur ne se produise.
    ⑤ SORTIE — **UNE valeur : un dictionnaire de SEPT clés** — `indice_seance`,
      `prix_sortie`, `motif`, `pnl_net_eur`, `prix_sortie_convention`,
      `motif_convention`, `pnl_net_convention_eur` — **ou `None` si la position
      reste ouverte.**
      [rend: 1]
    ⑥ TRAITEMENT — ① poser les seuils · ② pour chaque séance, appliquer les
      quatre tests · ③ si l une déclenche, chiffrer le réel ET la convention ·
      ④ **sinon, sortir au dernier cours après `HORIZON` séances.**
    ⑦ UNITÉ — Prix et résultats en euros · `indice_seance` est un rang dans la
      liste reçue, **compté depuis zéro** · `HORIZON` en séances de bourse.
    ⑧ POURQUOI — **DEUX montants, toujours.** Le réel tient compte des sauts
      d ouverture, la convention suppose une exécution au seuil exact. **Sans
      cette double écriture, on ne peut pas comparer une opération vécue à un
      backtest.**
    ⑨ CE QUI CLOCHE — **`None` veut dire DEUX choses : la position reste
      ouverte, ou la liste de séances était vide.** L appelant ne peut pas les
      distinguer. **Et `HORIZON` est lu ici alors que l appelant réel passe la
      valeur du registre : le même chiffre vit à deux endroits.**
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main, `None` compris. **`tester_seance`,
      [sort: non]
    ⑫ DÉFINITIONS —
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      la convention : le prix de sortie théorique, celui de l'objectif ou du stop, par opposition au prix réellement observé. C'est ce qui permet de comparer une opération vécue à un test sur le passé
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      un trade : une opération simulée, de l'achat à la revente
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    p = parametres_entree(prix_entree)
    tp, sl = p["tp"], p["sl"]
    for i, bar in enumerate(seances):
        res = tester_seance(bar, tp, sl)
        if res is not None:
            px, motif = res
            px_conv = sl if motif.startswith("SL") else tp
            motif_conv = "SL" if motif.startswith("SL") else "TP"
            return {"indice_seance": i, "prix_sortie": px, "motif": motif,
                    "pnl_net_eur": pnl_net(prix_entree, px),
                    "prix_sortie_convention": px_conv,
                    "motif_convention": motif_conv,
                    "pnl_net_convention_eur": pnl_net(prix_entree, px_conv)}
        # Les frais employés ici sont ceux en vigueur aujourd'hui : 0,15 % par ordre.
# Les trades déjà écrits au journal gardent les frais de leur époque — on ne
# recalcule jamais le passé, sinon les chiffres publiés changeraient. (A-50)
        if i + 1 >= HORIZON:
            px = bar["close"]
            return {"indice_seance": i, "prix_sortie": px, "motif": "HORIZON",
                    "pnl_net_eur": pnl_net(prix_entree, px),
                    "prix_sortie_convention": px,
                    "motif_convention": "HORIZON",
                    "pnl_net_convention_eur": pnl_net(prix_entree, px)}
    return None


# ══════════════════════════════════════════════════════════════
# CALIBRAGE — reproduire le trade de référence AVANT tout usage.
# Référence : BUREAU_VERITAS, journal_trades.csv (ligne du 27→29/07/2026).
#   entrée 27,28 · séances : 28/07 (pas de sortie) puis 29/07 Open 29,2400
#   attendu RÉEL       : TP_GAP · 29,2400 · +6 873,97 € (frais réels 0,15 %,
#     tarif Fortuneo Progress, décision de Jean-Luc du 11-08-2026 (A-50)). ⚠ La ligne du journal
#     porte +6 884,75 € : sa colonne réel avait utilisé un forfait de 300 € —
#     anomalie de 10,78 € FIGÉE (l'historique ne se réécrit jamais), documentée.
#   attendu CONVENTION : 28,3712 · +3 694,00 € (reproduit au centime)
# Lancer :  python3 MODULE_POSITIONS.py
# ══════════════════════════════════════════════════════════════
def _calibrage():
    """Reproduit un trade connu au centime, ou refuse de laisser utiliser ce module.

    ① RÔLE — **Prouver que le moteur mesure juste, avant tout usage.**
    ② CONTEXTE D APPEL — Le lancement direct de ce fichier. **Personne d autre ne
      l appelle.**
    ③ ENTRÉE — Aucune : les séances et les valeurs attendues sont écrites dans
      la fonction.
    ④ CONDITIONS D ENTRÉE — Aucune : elle ne dépend d aucun fichier.
    ⑤ SORTIE — UNE valeur : vrai si tout est reproduit.
      [rend: 1]
    ⑥ TRAITEMENT — ① rejouer deux séances de BUREAU_VERITAS, entrée à 27,28 ·
      ② comparer le motif, le prix réel et le prix de convention · ③ comparer le
      résultat de convention aux frais de l époque.
    ⑦ UNITÉ — Prix et résultats en euros · la tolérance est un demi-centime.
    ⑧ POURQUOI — **Le trade de référence porte une anomalie assumée** : la
      colonne réelle du journal dit +6 884,75 € parce qu un forfait de 300 € y
      avait été employé. **L écart de 10,78 € est FIGÉ — l historique ne se
      réécrit jamais — et le calibrage ne le reproduit pas.** Il vérifie la
      MÉCANIQUE, pas le montant réel d époque.
    ⑨ CE QUI CLOCHE — **Un seul cas, un saut à la hausse.** Les trois autres
      tests de `tester_seance` — stop touché, saut à la baisse, horizon — **ne
      sont jamais joués. Une inversion de l ordre des tests passerait.**
    ⑩ EFFET — **AFFICHE** le détail de chaque comparaison.
    ⑪ TERMINAISON — Rend la main, vrai ou faux. **C est l appel du bas du fichier
      qui en fait un code de sortie.**
      [sort: non]
    """
    seances = [
        # 28/07/2026 — séance sans déclenchement (source : cours du projet)
        {"open": 27.30, "high": 27.86, "low": 27.16, "close": 27.82},
        # 29/07/2026 — ouverture au-dessus du TP (28,3712) : TP_GAP
        {"open": 29.24, "high": 30.18, "low": 29.00, "close": 29.60},
    ]
    r = sortie_position(seances, 27.28)
    # Mécanique de sortie : doit reproduire la référence exactement.
    attendu = {"motif": "TP_GAP", "prix_sortie": 29.2400,
               "prix_sortie_convention": 28.3712}
    print("── CALIBRAGE BUREAU_VERITAS (mécanique) ──")
    ok = True
    for k, v in attendu.items():
        got = r[k]
        m = (abs(got - v) < 0.005) if isinstance(v, float) else (got == v)
        ok = ok and m
        print(f"  {'✅' if m else '❌'} {k}: obtenu {got!r} · attendu {v!r}")
    # P&L convention aux frais d'ÉPOQUE (0,15 % réels) : 3 694,00 € attendu.
    pnl_epoque = pnl_net(27.28, 28.3712, taux=0.0015)
    m = abs(pnl_epoque - 3694.00) < 0.005
    ok = ok and m
    print(f"  {'✅' if m else '❌'} pnl convention (frais d'époque 0,15 %) : "
          f"{pnl_epoque:.2f} · attendu 3694.00")
    # Note historique : la colonne RÉELLE du journal (+6 884,75 €) a utilisé un
    # forfait de 300 € au lieu de 0,15 % de la valeur échangée. Constaté le
# 11-08-2026, et figé
    # dans l'historique, non reproduite ici : c'est la convention Fortuneo qui
    # s'applique aux trades futurs.
    print(f"  ℹ régime A-50 acté (0,15 % Progress) sur ce trade : "
          f"réel {pnl_net(27.28, 29.24):.2f} € · conv {pnl_net(27.28, 28.3712):.2f} €")
    print("CALIBRAGE :", "OK" if ok else "ÉCHEC — NE PAS UTILISER (règle 9bis)")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _calibrage() else 1)
