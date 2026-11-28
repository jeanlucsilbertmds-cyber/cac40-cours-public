#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA COURBE DU COMPTE AU JOUR LE JOUR et L'ANALYSE DE PUISSANCE du contrôle 4 du juge (« ASSEZ DE DONNÉES »),
CALCULÉE ET AFFICHÉE, QUI NE DÉCIDE PAS.
Simulation uniquement : on mesure des opérations simulées, aucun ordre réel n'est jamais passé.

CE QUI A CHANGÉ LE 27-11-2026 AU SOIR (lot W2bFIX) — DEUX DÉCISIONS DE JEAN-LUC :
① A-1103, 22h04, « 1 » à « le retirer comme critère qui bloque, afficher seulement le nombre de séances qu'il
  faudrait » : le contrôle 4 « ASSEZ DE DONNÉES » est calculé et AFFICHÉ, il NE BLOQUE PLUS ; il se mesure sur le gain
  des 70 % (Jean-Luc, 21h38 : « on le fait sur les 70 % »). Raison : quand le contrôle du gain (Sharpe dégonflé) passe,
  il y avait assez de données par définition ; quand il échoue, la fourchette du gain dit déjà RÉFUTÉE ou NON TRANCHÉE
  (A-1074) ; un contrôle de plus pour la même question est une chance de plus de rejeter une bonne stratégie (A-1094).
  `assez_de_donnees` rend donc toujours le nombre de séances nécessaire et disponible, avec une ÉTIQUETTE
  (`constat`) et le rôle AFFICHAGE : aucun programme ne doit s'en servir pour décider (épreuve E11).
② A-1108, 22h29, « 2 » à « les exclure du gain jugé et les afficher seulement » : les positions encore ouvertes au
  dernier jour des données (motif FIN_DES_DONNEES, « NON TERMINÉES » dans la loi) sont EXCLUES de la courbe du compte
  dès leur achat ; leur nombre et leur résultat latent au dernier cours réel, frais de vente compris, sont AFFICHÉS
  (`courbe_du_compte` → `non_terminees`, par `MODULE_JUGEMENT.mettre_a_part_les_non_terminees`, l'endroit unique).

LE SENS EN TÊTE — R-505 version 2, étape 5, contrôle 4 (texte accepté par Jean-Luc le 27-11-2026 à 18h38) :
« ASSEZ DE DONNÉES, jugées sur la COURBE DU COMPTE AU JOUR LE JOUR, minimum calculé pour chaque stratégie par une
ANALYSE DE PUISSANCE » — décision de Jean-Luc du 27-11-2026 à 13h46 (« 1 », BACKLOG A-1071), qui abandonne le plancher
fixe de 30 observations (choix délégué DÉL-D35) et la mesure de ressemblance des opérations proches dans le temps.
Raison de la décision : « vingt achats nés de la même chute du marché ne sont qu'une seule preuve ; la courbe du compte
ne monte qu'une fois et compte d'elle-même la dépendance » (R-505 v2, étape 5, *Pourquoi*). La même courbe est l'unité
du contrôle 1 (Sharpe dégonflé ; R-505 v2, « À PRÉCISER » ① : « rendement quotidien du compte, A-1071 »).

① RÔLE — Trois choses, à UN seul endroit (R-708 : deux implémentations d'une même chose divergent toujours) :
  ① fabriquer, à partir des opérations d'une version, la série des rendements quotidiens du compte sur le calendrier
  des séances (`courbe_du_compte`) ; ② la donner au Sharpe dégonflé du lot L3 sans recopier sa formule
  (`sharpe_degonfle_de_la_courbe`) ; ③ calculer le nombre de séances nécessaire et l'AFFICHER pour le contrôle 4,
  sans rien décider (`seances_necessaires`, `assez_de_donnees` ; A-1103).
② CONTEXTE D'APPEL — Au 27-11-2026 : l'épreuve `tests/EPREUVES_DE_LA_COURBE_DU_COMPTE_Ven_27-11-2026.py`. Destiné à la
  porte du juge (`JUGER_UNE_FICHE`, par `CONTRATS_DES_FICHIERS.MESUREURS_DU_JUGE`), à la grille
  (`MODULE_JUGEMENT.grille_de_validation`), à la moulinette (étape 4, condition 4) et au banc (A-1094) — branchement
  laissé au Chat qui réunit les lots (plan R505), comme un champ d'AFFICHAGE, jamais dans CONTROLES_DU_VERDICT
  (A-1103 ; note du lot W2bFIX).
③ ENTRÉE — Voir chaque fonction.
④ CONDITIONS D'ENTRÉE — Python 3.9 et plus, la bibliothèque livrée d'origine seule (pas de numpy : le circuit du soir
  ne l'installe pas, constat M2 du lot L3).
⑤ SORTIE — Ne rend rien : pose sept fonctions et quelques constantes.
⑥ TRAITEMENT — Définir `seances_de_la_periode`, `clotures_des_cours`, `courbe_du_compte`, `sharpe_degonfle_de_la_courbe`,
  `seances_necessaires`, `assez_de_donnees`, `puissance_visee`.
⑦ UNITÉ — UN RENDEMENT est une FRACTION du capital engagé, par SÉANCE (0,004 = +0,4 %) ; un gain est en EUROS ; une
  durée est un nombre de SÉANCES du calendrier (R-112 : jamais des lignes de cours) ; le Sharpe est PAR SÉANCE, non
  annualisé (l'unité de MODULE_SHARPE_DEGONFLE) ; seuil et puissance sont des fractions.
⑧ POURQUOI — LA MÉTHODE DU PORTEFEUILLE EN TEMPS CALENDAIRE (Fama, « Market efficiency, long-term returns, and
  behavioral finance », Journal of Financial Economics 49(3), 1998, p. 283-306, lu le 27-11-2026, §4.2.2 p. 294 :
  « if average monthly returns are used, there has long been a full solution to the cross-correlation problem » ;
  « Re-form the portfolio every month » ; la variation du rendement de ce portefeuille « accurately captures the
  effects of the correlation of returns across event stocks ») : on ne compte pas les opérations, on suit chaque
  séance le rendement MOYEN des positions ouvertes ; vingt positions ouvertes ensemble font UN rendement de la séance,
  pas vingt observations. Fama l'écrit au mois ; nous suivons la séance, l'unité de nos trades de 3 à 20 séances.
  L'ANALYSE DE PUISSANCE retenue est la DURÉE MINIMALE D'HISTORIQUE de Bailey et López de Prado (« The Sharpe Ratio
  Efficient Frontier », Journal of Risk 15(2), 2012, p. 3-44, équation 13 p. 11, lue le 27-11-2026 :
  MinTRL = 1 + [1 − γ3·SR + (γ4 − 1)/4·SR²] × (Z_α ÷ (SR − SR*))²), ÉTENDUE À UNE PUISSANCE : voir `seances_necessaires`.
  Pourquoi elle et non Lo (2002) seul : Lo (« The Statistics of Sharpe Ratios », Financial Analysts Journal 58(4),
  p. 36-52, équation 8 p. 38) donne la variance du Sharpe estimé pour des rendements indépendants de loi quelconque
  mais la réduit, sous la loi normale, à 1 + SR²/2 ; la formule de Bailey et López de Prado garde l'asymétrie et
  l'aplatissement — nos gains, coupés net par l'objectif et le stop, ne suivent pas la loi normale — et c'est
  EXACTEMENT la statistique du Sharpe dégonflé du contrôle 1 (même dénominateur, même SR0) : la puissance calculée
  est celle du test qui décide, pas d'un autre.
⑨ CE QUI CLOCHE — ① SANS COURS, LA COURBE EST LISSÉE : le gain d'une opération est étalé à taux constant sur ses
  séances ; les secousses à l'intérieur du trade disparaissent, l'écart-type baisse, le Sharpe monte et le minimum
  baisse — un faux vert possible. Le mode lissé est donc REFUSÉ par `assez_de_donnees` (INCONNU) et par le Sharpe dégonflé ; seul
  le mode « au cours » (clôtures de chaque séance) est mesuré. ② Les frais et la taxe ne sont pas connus séance par séance : la valeur
  de la dernière séance est 100 000 € + gain net, donc tous les frais tombent le jour de la vente ; la somme des
  rendements en euros est exacte, leur répartition dans le temps ne l'est pas (un jour de vente un peu plus mauvais).
  ③ Une clôture manquante une séance où la position est ouverte (valeur non cotée ce jour-là) : la valeur de la veille
  est gardée, gain nul ce jour-là ; le nombre de ces séances est rendu (`clotures_manquantes`), jamais tu.
  ④ ANALYSE DE PUISSANCE SUR L'EFFET MESURÉ SUR LES MÊMES DONNÉES : si la taille d'effet est mesurée sur les 30 %
  eux-mêmes, « assez » équivaut à z observé ≥ z(1 − seuil) + z(puissance) — un contrôle 1 plus strict, pas une
  information nouvelle (Hoenig et Heisey, « The Abuse of Power », The American Statistician 55(1), 2001, p. 19-24 :
  « for any test the observed power is a 1:1 function of the p value », lu p. 2 du tiré à part). TRANCHÉ par A-1103
  (Jean-Luc, 27-11-2026, 21h38 et 22h04) : l'effet se mesure sur les 70 % (`courbe_de_l_effet`), et le résultat est
  affiché, il ne décide pas. ⑤ La formule est asymptotique (loi normale du Sharpe estimé, rendements indépendants
  d'une séance à l'autre) ; la courbe d'une stratégie à positions de plusieurs séances est autocorrélée (Lo 2002,
  p. 40-41 : la variance « includes all the covariances ») — non corrigé, non mesuré ici.
⑩ EFFET — Aucun au chargement. `seances_de_la_periode` et `puissance_visee` lisent des fichiers de la racine.
⑪ TERMINAISON — Le chargement rend la main ; aucune fonction ne lit le réseau ni n'attend.
⑫ DÉFINITIONS
  la courbe du compte : la suite, séance par séance, du rendement du capital engagé dans les positions ouvertes ;
    zéro une séance sans position (l'argent attend)
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
  jetons illimités : tous les signaux joués, 100 000 € chacun (MODULE_POSITIONS.CAPITAL)
  la puissance : la probabilité qu'une stratégie qui a vraiment l'effet mesuré soit reconnue par le test
  k : les versions réellement envoyées au juge, regroupées par ressemblance, plus les stratégies déjà réellement
    jugées (A-774, A-772, A-1082)
"""

import math
import os
import sys
from statistics import NormalDist

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import MODULE_POSITIONS as MP  # noqa: E402  (CAPITAL : 100 000 € par trade, écrit là une fois)
import MODULE_SHARPE_DEGONFLE as SD  # noqa: E402  (le Sharpe dégonflé du lot L3, jamais recopié)

_NORMALE = NormalDist()

# LES DEUX MODES DE LA COURBE (⑨ ①) : seul le premier est mesuré.
AU_COURS, LISSEE = "au_cours", "lissee"
# LES TROIS ÉTIQUETTES DU CONTRÔLE 4 (mandat du lot W2b : « ASSEZ / PAS ASSEZ / INCONNU si non calculable — jamais un
# faux vert »). Depuis A-1103 (Jean-Luc, 27-11-2026 à 22h04), ce sont des ÉTIQUETTES D'AFFICHAGE, pas des verdicts :
# rien ne décide sur elles. Le rôle est écrit à côté, une fois.
ASSEZ, PAS_ASSEZ, INCONNU = "ASSEZ", "PAS ASSEZ", "INCONNU"
AFFICHAGE = "AFFICHAGE"
# LA RÉFÉRENCE DE STRICTESSE DE LA PUISSANCE (même usage que MODULE_JUGEMENT.REFERENCES_DE_STRICTESSE : une référence
# qui se lirait dans le fichier qu'elle contrôle ne contrôlerait rien) : R-505 v2, « À PRÉCISER » ⑦ — « La puissance
# visée : CHOIX TECHNIQUE — 80 %, valeur standard employée par l'arbitrage du 14-11 ». Une puissance plus HAUTE est
# plus stricte (elle demande plus de séances) ; plus basse, elle est refusée.
REFERENCE_DE_LA_PUISSANCE = (0.80, "R-505 v2, À PRÉCISER ⑦")


def seances_de_la_periode(racine, debut, fin):
    """Rend les séances CONSTATÉES du calendrier de la bourse entre deux dates, bornes comprises, en textes AAAA-MM-JJ.

    ① RÔLE — Donner à la courbe le calendrier des séances, par le lecteur existant (R-708, R-110 : une séance est un jour
      où l'indice CAC 40 est publié, jamais une ligne de cours).
    ② CONTEXTE D'APPEL — Les épreuves ; destiné à la porte du juge (séances d'examen) et à la moulinette.
    ③ ENTRÉE — `racine` : la racine du dépôt · `debut`, `fin` : deux dates (`datetime.date`) ou deux textes AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — Celles de `CALENDRIER_DE_LA_BOURSE.lire_les_seances` et `seances_entre`.
    ⑤ SORTIE — UNE valeur : la liste triée des séances, en textes AAAA-MM-JJ.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le calendrier · ② les séances entre les deux dates · ③ refuser une séance PRÉVUE (à venir).
    ⑦ UNITÉ — Des SÉANCES.
    ⑧ POURQUOI — Une courbe ne se juge que sur des séances qui ont eu lieu : une séance à venir dans la série ferait un
      rendement nul inventé.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit deux fichiers de la racine (indice et liste d'Euronext).
    ⑪ TERMINAISON — Rend la main, ou lève (ValueError, HorsCalendrier, OSError).
      [sort: non]
    """
    import datetime as dt
    import CALENDRIER_DE_LA_BOURSE as CAL
    d0 = debut if isinstance(debut, dt.date) else dt.date.fromisoformat(debut)
    d1 = fin if isinstance(fin, dt.date) else dt.date.fromisoformat(fin)
    sc = CAL.lire_les_seances(racine)
    out = []
    for d, etat in CAL.seances_entre(d0, d1, sc):
        if etat != CAL.CONSTATEE:
            raise ValueError("séance %s %s : une courbe ne contient que des séances qui ont eu lieu" % (d, etat))
        out.append(d.isoformat())
    return out


def clotures_des_cours(cours):
    """Rend les clôtures {valeur : {AAAA-MM-JJ : clôture}} à partir des séries du lecteur unique des cours.

    ① RÔLE — Donner à `courbe_du_compte` les clôtures telles que le juge les lit, sans relire le fichier à sa façon.
    ② CONTEXTE D'APPEL — Les épreuves ; destiné à la porte du juge (son `jeu["cours"]`).
    ③ ENTRÉE — `cours` : le premier rendu de `JUGE_DES_STRATEGIES.lire_par_le_lecteur` (clé de la valeur → liste de
      séances {date, open, high, low, close, volume}).
    ④ CONDITIONS D'ENTRÉE — Chaque séance porte `date` et `close`.
    ⑤ SORTIE — UNE valeur : {valeur : {date : clôture}}.
      [rend: 1]
    ⑥ TRAITEMENT — une table par valeur.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — R-708 : le juge lit les cours par `lire_par_le_lecteur` (LIRE_LES_COURS) ; la courbe lit les mêmes.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève KeyError sur une séance sans `date` ou `close`.
      [sort: non]
    """
    return {v: {b["date"]: b["close"] for b in serie} for v, serie in cours.items()}


def courbe_du_compte(ops, seances, clotures=None, mise=None):
    """Fabrique la courbe du compte au jour le jour : un rendement par séance, positions ouvertes comprises.

    ① RÔLE — A-1071 (a) : « la stratégie est jugée sur la COURBE DU COMPTE AU JOUR LE JOUR (méthode du portefeuille en
      temps calendaire, Fama 1998) » ; jetons illimités, 100 000 € par trade.
    ② CONTEXTE D'APPEL — `sharpe_degonfle_de_la_courbe` et `assez_de_donnees` la reçoivent ; les épreuves.
    ③ ENTRÉE — `ops` : les opérations de la version, chacune un dictionnaire portant `date_entree` et `date_sortie`
      (AAAA-MM-JJ), `net` (gain net en euros, frais et taxe payés) et, en mode au cours, `valeur` et `pe` (prix
      d'entrée en euros) — les noms des opérations de JUGE_DES_STRATEGIES · `seances` : les séances de la période
      jugée, AAAA-MM-JJ (`seances_de_la_periode`) · `clotures` : {valeur : {AAAA-MM-JJ : clôture en euros}}, ou None
      (mode lissé : point « sans cours, la courbe est lissée » de l’en-tête) · `mise` : euros par trade ; None = MODULE_POSITIONS.CAPITAL.
    ④ CONDITIONS D'ENTRÉE — `seances` non vide, strictement croissante, sans doublon ; chaque opération entre et sort
      sur une séance de `seances` (sinon elle déborde de la période jugée : refusée, jamais coupée en silence) ;
      date_entree ≤ date_sortie ; `net` fini et > −mise ; en mode au cours, `pe` fini > 0 et la valeur présente dans
      `clotures`. Sinon ValueError, qui nomme l'opération.
    ⑤ SORTIE — UNE valeur : un dictionnaire de dix clés : `dates` (les séances), `rendements` (un par séance, fraction
      du capital engagé), `gains_eur` (gain du compte de chaque séance, euros), `positions_ouvertes` (nombre par
      séance), `mode` (AU_COURS ou LISSEE), `n_seances`, `n_seances_investies`, `n_operations` (opérations TERMINÉES
      portées par la courbe), `clotures_manquantes`, `non_terminees` (AFFICHAGE d'A-1108 : {n, resultat_latent_eur,
      role}, rendu de `MODULE_JUGEMENT.mettre_a_part_les_non_terminees`).
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ mettre à part les positions NON TERMINÉES (A-1108 : exclues de la courbe dès leur achat, affichées)
      · ① contrôler les séances et chaque opération terminée · ② pour chaque opération, la VALEUR de la position à la
      fin de chaque séance tenue : au cours, mise × clôture ÷ prix d'entrée (clôture manquante : valeur de la veille) ;
      lissée, mise × (1 + net ÷ mise)^(i ÷ n) à la i-ième des n séances ; la séance de vente, mise + net · ③ le gain de
      la séance = valeur − valeur de la veille (mise la veille de l'achat), ajouté au compte de la séance, et la
      position comptée ouverte ce jour-là · ④ rendement de la séance = somme des gains ÷ (mise × positions ouvertes) ;
      zéro sans position.
    ⑦ UNITÉ — Euros pour les gains et les valeurs ; fraction par séance pour les rendements ; séances.
    ⑧ POURQUOI — Diviser par le capital ENGAGÉ ce jour-là fait du rendement de la séance la MOYENNE des rendements des
      positions ouvertes — proche du portefeuille à poids égaux de Fama (1998, p. 294), à une nuance près : le gain du
      jour de chaque position est rapporté à sa MISE d'achat (100 000 €), pas à sa valeur de la veille (défaut W2b-3 de
      la relecture Cowork du 28-11-2026 ; écart mesuré sur C5 2024-2026 : Sharpe 0,10996 contre 0,11012 par séance). C'est lui qui fait que vingt achats
      nés de la même chute, mêmes dates et même parcours, donnent EXACTEMENT la courbe d'un seul achat (épreuve E3) :
      une seule preuve. Une séance sans position vaut ZÉRO et reste dans la série : c'est la courbe du compte, et le
      nombre de séances disponibles du contrôle 4 est le nombre de séances de la période. Choix technique : Fama et
      Mitchell et Stafford (2000) écartent les mois sans aucune position ; sur le Sharpe, inclure les zéros multiplie
      à peu près la moyenne et l'écart-type par la part p de séances investies et √p, le z = Sharpe × √T reste à peu
      près le même (non mesuré au-delà de l'épreuve E5). La somme des gains de la courbe égale la somme des `net` :
      aucun euro n'est créé ni perdu (épreuve E4, sur les 100 trades réels de C5).
    ⑨ CE QUI CLOCHE — Voir l’en-tête du module, points « courbe lissée », « frais au jour de la vente », « clôture manquante ».
    ⑩ EFFET — Importe MODULE_JUGEMENT au premier appel.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError. Une boucle par opération sur ses séances.
      [sort: non]
    """
    mise = MP.CAPITAL if mise is None else mise
    import MODULE_JUGEMENT as J
    ops, non_terminees = J.mettre_a_part_les_non_terminees(ops)   # A-1108 : hors de la courbe, affichées
    if isinstance(mise, bool) or not isinstance(mise, (int, float)) or not math.isfinite(mise) or not mise > 0:
        raise ValueError("mise = %r : il faut un nombre fini > 0" % (mise,))
    dates = list(seances)
    if not dates:
        raise ValueError("aucune séance : pas de courbe")
    for a, b in zip(dates, dates[1:]):
        if not a < b:
            raise ValueError("séances non strictement croissantes : %r puis %r" % (a, b))
    rang = {d: i for i, d in enumerate(dates)}
    mode = LISSEE if clotures is None else AU_COURS
    gains = [0.0] * len(dates)
    ouvertes = [0] * len(dates)
    manquantes = 0
    for n_op, o in enumerate(ops):
        de, ds, net = o.get("date_entree"), o.get("date_sortie"), o.get("net")
        if de not in rang or ds not in rang:
            raise ValueError("opération n°%d (%s → %s) : entrée ou sortie hors des séances de la période jugée"
                             % (n_op, de, ds))
        i0, i1 = rang[de], rang[ds]
        if i1 < i0:
            raise ValueError("opération n°%d : vente (%s) avant l'achat (%s)" % (n_op, ds, de))
        if isinstance(net, bool) or not isinstance(net, (int, float)) or not math.isfinite(net) or not net > -mise:
            raise ValueError("opération n°%d : gain net %r (il faut un nombre fini > −mise)" % (n_op, net))
        if mode == AU_COURS:
            pe, v = o.get("pe"), o.get("valeur")
            if isinstance(pe, bool) or not isinstance(pe, (int, float)) or not math.isfinite(pe) or not pe > 0:
                raise ValueError("opération n°%d : prix d'entrée %r" % (n_op, pe))
            if v not in clotures:
                raise ValueError("opération n°%d : valeur %r sans clôtures" % (n_op, v))
            serie = clotures[v]
        n = i1 - i0 + 1
        precedente = float(mise)
        for j in range(i0, i1 + 1):
            if j == i1:
                valeur = mise + net
            elif mode == AU_COURS:
                c = serie.get(dates[j])
                if c is None:
                    valeur, manquantes = precedente, manquantes + 1
                else:
                    valeur = mise * c / pe
            else:
                valeur = mise * (1.0 + net / mise) ** ((j - i0 + 1) / n)
            gains[j] += valeur - precedente
            ouvertes[j] += 1
            precedente = valeur
    rendements = [g / (mise * k) if k else 0.0 for g, k in zip(gains, ouvertes)]
    return {"dates": dates, "rendements": rendements, "gains_eur": gains, "positions_ouvertes": ouvertes,
            "mode": mode, "n_seances": len(dates), "n_seances_investies": sum(1 for k in ouvertes if k),
            "n_operations": len(ops), "clotures_manquantes": manquantes, "non_terminees": non_terminees}


def sharpe_degonfle_de_la_courbe(courbe, k, sharpes_des_essais):
    """Rend la mesure du contrôle 1 (Sharpe dégonflé) calculée sur la courbe du compte, par la fonction du lot L3.

    ① RÔLE — Brancher la courbe A-1071 sur le contrôle 1 (R-505 v2, « À PRÉCISER » ① : unité = « rendement quotidien
      du compte »), sans recopier le calcul (R-708).
    ② CONTEXTE D'APPEL — Les épreuves ; destiné à la porte du juge et au banc (A-1094).
    ③ ENTRÉE — `courbe` : le rendu de `courbe_du_compte` · `k` : le nombre d'essais (entier ≥ 1) · `sharpes_des_essais` :
      les Sharpe PAR SÉANCE des essais comptés dans k, sur la même période (ignorés si k = 1).
    ④ CONDITIONS D'ENTRÉE — Celles de `MODULE_JUGEMENT.mesurer_le_sharpe_degonfle`.
    ⑤ SORTIE — DEUX valeurs : la mesure de `mesurer_le_sharpe_degonfle` (champs du contrat `sharpe_degonfle`,
      `nombre_d_essais`, plus le détail) augmentée de `mode_de_la_courbe`, ou None ; et la raison (vide si mesurée).
      [rend: 2]
    ⑥ TRAITEMENT — ① mode lissé → (None, raison) · ② `MODULE_JUGEMENT.mesurer_le_sharpe_degonfle(rendements, k, ...)`.
    ⑦ UNITÉ — Probabilité : fraction ; Sharpe : par séance.
    ⑧ POURQUOI — Le mesureur de L3 attendait « le rendement QUOTIDIEN DU COMPTE de la version sur ses séances
      d'examen (A-1071) » : c'est `courbe["rendements"]`. Le mode lissé est refusé ici aussi : il gonfle le Sharpe
      (point « courbe lissée » de l’en-tête), donc la probabilité du contrôle 1 — un faux vert.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe MODULE_JUGEMENT au premier appel.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if courbe.get("mode") != AU_COURS:
        return None, "courbe %r : seule la courbe au cours décide (la courbe lissée gonfle le Sharpe)" % courbe.get("mode")
    import MODULE_JUGEMENT as J
    m, r = J.mesurer_le_sharpe_degonfle(courbe["rendements"], k, sharpes_des_essais)
    if m is not None:
        m["mode_de_la_courbe"] = courbe["mode"]
    return m, r


def seances_necessaires(sharpe, asymetrie, aplatissement, seuil, puissance, sharpe_du_meilleur_hasard=0.0):
    """Rend le nombre de séances (non arrondi) qu'il faut pour que le test du contrôle 1 reconnaisse cet effet.

    ① RÔLE — A-1071 (b) : « calculer pour chaque stratégie le nombre de jours nécessaire pour distinguer son gain du
      hasard à la barre 0,05 ÷ k : c'est l'analyse de puissance ».
    ② CONTEXTE D'APPEL — `assez_de_donnees` ; les épreuves (calibrage sur les chiffres publiés).
    ③ ENTRÉE — `sharpe` : la taille d'effet, Sharpe PAR SÉANCE de la courbe · `asymetrie` : γ3 · `aplatissement` : γ4
      BRUT (3 = loi normale) · `seuil` : la barre du test (0,05 ÷ k), dans ]0, 1[ · `puissance` : dans ]0, 1[ ·
      `sharpe_du_meilleur_hasard` : SR0, la barre du Sharpe dégonflé (0 si k = 1).
    ④ CONDITIONS D'ENTRÉE — Nombres finis ; sinon ValueError.
    ⑤ SORTIE — UNE valeur : le nombre de séances T nécessaire, un flottant ≥ 1, ou `math.inf` quand l'effet ne dépasse
      pas SR0 (aucune longueur ne suffit).
      [rend: 1]
    ⑥ TRAITEMENT — ① D = 1 − γ3·SR + (γ4 − 1)/4·SR² ; D ≤ 0 → ValueError · ② SR ≤ SR0 → infini ·
      ③ T = 1 + D × ((Z⁻¹(1 − seuil) + Z⁻¹(puissance)) ÷ (SR − SR0))².
    ⑦ UNITÉ — Des SÉANCES (l'unité de la série dont vient le Sharpe).
    ⑧ POURQUOI — Le contrôle 1 rejette « pas de talent » quand z = (SR^ − SR0)·√(T − 1) ÷ √D dépasse Z⁻¹(1 − seuil)
      (MODULE_SHARPE_DEGONFLE.sharpe_degonfle). Si la stratégie a vraiment le Sharpe SR, SR^ suit à peu près une loi
      normale de moyenne SR et de variance D ÷ (T − 1) (Bailey et López de Prado 2012 ; Lo 2002 sous la loi normale) ;
      le test réussit avec la probabilité Z((SR − SR0)·√(T − 1) ÷ √D − Z⁻¹(1 − seuil)) ; l'égaler à la puissance donne
      la formule ⑥ ③. Avec une puissance de 50 % (Z⁻¹ = 0), c'est mot pour mot la MinTRL de l'article (équation 13) :
      CALIBRÉE sur ses quatre exemples (épreuve E1 : 59,895 mois, « approx. 4.99 years » ; 2,73, 3,24 ans).
      Le « + Z⁻¹(puissance) » est la forme classique du calcul d'effectif d'un test unilatéral sur une moyenne ;
      vérifiée par simulation (épreuve E2 : 80 % de rejets attendus).
    ⑨ CE QUI CLOCHE — D est pris à l'effet SR, comme la MinTRL, et non à SR0 : approximation asymptotique (point « autocorrélation » de l’en-tête du
      module).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    for nom, x in (("sharpe", sharpe), ("asymetrie", asymetrie), ("aplatissement", aplatissement),
                   ("sharpe_du_meilleur_hasard", sharpe_du_meilleur_hasard)):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
            raise ValueError("%s = %r : il faut un nombre fini" % (nom, x))
    for nom, x in (("seuil", seuil), ("puissance", puissance)):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not (0.0 < x < 1.0):
            raise ValueError("%s = %r : il faut un nombre dans ]0, 1[" % (nom, x))
    d = 1.0 - asymetrie * sharpe + (aplatissement - 1.0) / 4.0 * sharpe * sharpe
    if not d > 0.0:
        raise ValueError("dénominateur 1 − γ3·SR + (γ4 − 1)/4·SR² = %r ≤ 0" % (d,))
    ecart = sharpe - sharpe_du_meilleur_hasard
    if not ecart > 0.0:
        return math.inf
    z = _NORMALE.inv_cdf(1.0 - seuil) + _NORMALE.inv_cdf(puissance)
    return 1.0 + d * (z / ecart) ** 2


def assez_de_donnees(courbe_de_l_effet, seances_disponibles, k, sharpes_des_essais, seuil, puissance):
    """Rend l'AFFICHAGE du contrôle 4 (« ASSEZ DE DONNÉES ») : séances nécessaires, séances disponibles, et une étiquette
    qui ne décide rien (A-1103).

    ① RÔLE — Le contrôle 4 de l'étape 5 de R-505 v2 et la condition 4 de l'étape 4, tous deux « AFFICHÉ, NE BLOQUE
      PLUS » (décision de Jean-Luc du 27-11-2026 à 22h04, « 1 », A-1103) : « le nombre de séances qu'il faudrait pour
      voir le gain mesuré sur les 70 % […] est calculé et AFFICHÉ, pour information ; il ne décide plus ».
    ② CONTEXTE D'APPEL — Les épreuves ; destiné à l'AFFICHAGE du juge et de la moulinette, jamais à leur décision
      (aucune clé `assez_de_donnees` dans CONTRATS_DES_FICHIERS.CONTROLES_DU_VERDICT : épreuve E11).
    ③ ENTRÉE — `courbe_de_l_effet` : le rendu de `courbe_du_compte` d'où se mesure la taille d'effet — la courbe des
      70 % (A-1103 ; point « effet mesuré sur les mêmes données » de l'en-tête du module) · `seances_disponibles` : le nombre de séances de la
      courbe jugée (entier ≥ 0) · `k` : nombre d'essais (N du Sharpe dégonflé) · `sharpes_des_essais` : Sharpe par
      séance des essais (ignorés si k = 1) · `seuil` : 0,05 ÷ k, lu à la table de la loi par l'appelant · `puissance` :
      lue par `puissance_visee`.
    ④ CONDITIONS D'ENTRÉE — —  (toute entrée fautive rend INCONNU avec sa raison, jamais une exception, jamais ASSEZ).
    ⑤ SORTIE — UNE valeur : un dictionnaire de treize clés : `constat` (étiquette d'affichage ASSEZ, PAS_ASSEZ ou
      INCONNU), `role` (toujours AFFICHAGE : rien ne décide sur ce rendu), `raison`,
      `seances_necessaires` (entier, arrondi au-dessus, ou None si infini ou inconnu), `seances_necessaires_brut`,
      `seances_disponibles`, `sharpe_par_seance`, `sharpe_du_meilleur_hasard`, `asymetrie`, `aplatissement`, `seuil`,
      `puissance`, `nombre_d_essais`.
      [rend: 1]
    ⑥ TRAITEMENT — ① courbe lissée → étiquette INCONNU · ② moments et SR0 par
      `MODULE_SHARPE_DEGONFLE.sharpe_degonfle_d_une_serie` (la fonction de L3 : mêmes SR, γ3, γ4 et SR0 que le
      contrôle 1) · ③ `seances_necessaires` · ④ étiquette : infini → PAS ASSEZ ; disponibles ≥ nécessaires → ASSEZ ;
      sinon PAS ASSEZ — affichée, elle ne décide rien.
    ⑦ UNITÉ — Séances ; Sharpe par séance ; fractions.
    ⑧ POURQUOI — « Le plancher fixe de 30 est abandonné » (A-1071 : règle de manuel, « trop prudente dans certains cas
      et insuffisante dans d'autres, surtout pour des gains dissymétriques comme les nôtres », arXiv 2409.06413) : le
      minimum dépend de la force de la stratégie, de la forme de ses gains et de la barre ; aucun nombre fixe n'apparaît
      ici. L'étiquette INCONNU quand le calcul est impossible dit qu'on ne sait pas (jamais un faux « ASSEZ »). Depuis
      A-1103, aucune de ces étiquettes ne décide : la question « assez de données ? » est déjà tranchée par le contrôle
      1 et par la fourchette du gain (A-1074) ; la reposer serait une chance de plus de rejeter une bonne stratégie.
    ⑨ CE QUI CLOCHE — Les points « effet mesuré sur les mêmes données » et « autocorrélation » de l'en-tête du module. Une courbe qui n'a
      jamais bougé (aucune opération) rend INCONNU (écart-type nul), pas PAS ASSEZ.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rendu = {"constat": INCONNU, "role": AFFICHAGE, "raison": "", "seances_necessaires": None, "seances_necessaires_brut": None,
             "seances_disponibles": seances_disponibles, "sharpe_par_seance": None, "sharpe_du_meilleur_hasard": None,
             "asymetrie": None, "aplatissement": None, "seuil": seuil, "puissance": puissance, "nombre_d_essais": k}
    if not isinstance(courbe_de_l_effet, dict) or courbe_de_l_effet.get("mode") != AU_COURS:
        rendu["raison"] = "courbe de l'effet %r : seule la courbe au cours décide (la courbe lissée gonfle le Sharpe)" % (
            courbe_de_l_effet.get("mode") if isinstance(courbe_de_l_effet, dict) else courbe_de_l_effet,)
        return rendu
    if isinstance(seances_disponibles, bool) or not isinstance(seances_disponibles, int) or seances_disponibles < 0:
        rendu["raison"] = "séances disponibles %r : il faut un entier ≥ 0" % (seances_disponibles,)
        return rendu
    try:
        m = SD.sharpe_degonfle_d_une_serie(courbe_de_l_effet["rendements"], k, sharpes_des_essais)
        rendu.update(sharpe_par_seance=m["sharpe"], sharpe_du_meilleur_hasard=m["sharpe_du_meilleur_hasard"],
                     asymetrie=m["asymetrie"], aplatissement=m["aplatissement"])
        brut = seances_necessaires(m["sharpe"], m["asymetrie"], m["aplatissement"], seuil, puissance,
                                   m["sharpe_du_meilleur_hasard"])
    except (ValueError, KeyError, TypeError) as e:
        rendu["raison"] = "analyse de puissance non calculable : %s" % e
        return rendu
    rendu["seances_necessaires_brut"] = brut
    if math.isinf(brut):
        rendu.update(constat=PAS_ASSEZ, raison="effet mesuré (Sharpe %.6g par séance) ≤ barre du hasard SR0 = %.6g : "
                     "aucune longueur ne suffit" % (m["sharpe"], m["sharpe_du_meilleur_hasard"]))
        return rendu
    necessaires = int(math.ceil(brut - 1e-9))
    rendu["seances_necessaires"] = necessaires
    if seances_disponibles >= necessaires:
        rendu["constat"] = ASSEZ
    else:
        rendu.update(constat=PAS_ASSEZ, raison="TROP PETIT : %d séances disponibles, %d nécessaires"
                     % (seances_disponibles, necessaires))
    return rendu


def puissance_visee(racine):
    """Rend la puissance visée lue au fichier des seuils de R-505 v2 en attente du REGISTRE, ou None et la raison.

    ① RÔLE — Lire la puissance à UN seul endroit, jamais en dur dans le code (A-1083 ② : « les seuils ne sont jamais
      écrits dans le code »), tant que R-505 v2 n'est pas au REGISTRE.
    ② CONTEXTE D'APPEL — Les épreuves ; destiné à la porte du juge.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la puissance (fraction) ou None, et la raison (vide si lue).
      [rend: 2]
    ⑥ TRAITEMENT — ① `MODULE_JUGEMENT.table_des_seuils_en_attente` (la lecture contrôlée du lot L3) · ② la case
      `puissance_visee` par `MODULE_JUGEMENT.seuil_de_la_loi` · ③ refuser hors de ]0, 1[ et sous la référence
      REFERENCE_DE_LA_PUISSANCE (moins strict).
    ⑦ UNITÉ — Fraction.
    ⑧ POURQUOI — R-505 v2, « À PRÉCISER » ⑦ : « 80 %, valeur standard employée par l'arbitrage du 14-11 » ; la table
      « LES SEUILS DE CETTE LOI » ne porte pas de ligne pour elle (écart signalé dans la note du lot W2b).
    ⑨ CE QUI CLOCHE — À l'installation de R-505 v2 (I1), la ligne doit passer au REGISTRE et ce fichier être archivé.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import MODULE_JUGEMENT as J
    p, r = J.seuil_de_la_loi(J.table_des_seuils_en_attente(racine), "puissance_visee")
    if p is None:
        return None, r
    ref, source = REFERENCE_DE_LA_PUISSANCE
    if not 0.0 < p < 1.0:
        return None, "puissance_visee = %r hors de ]0, 1[" % (p,)
    if p < ref:
        return None, "puissance_visee = %r moins stricte que %r (%s)" % (p, ref, source)
    return p, ""
