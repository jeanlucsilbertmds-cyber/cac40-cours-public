#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MODULE_PARCOURS_A_UN_JETON.py — les milliers de parcours à un jeton de l'étape 6 de R-505 v2, et le contrôle des
signaux pris et ignorés (décision A-1092). Écrit le vendredi 27-11-2026 (Paris), lot W2d du plan R505.

Simulation uniquement : aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE. La qualité d'une stratégie se prouve avec TOUS ses signaux (jetons illimités, décision de Jean-Luc
du 27-09-2026 à 13h11 : « le comptage doit se faire sur le nombre illimité, puisqu'on veut voir si la stratégie
fonctionne »). La mise en direct, elle, ne tient qu'UNE position à la fois par stratégie : un signal reçu pendant une
position est ignoré. Le résultat en un jeton dépend donc en partie du hasard de l'arrivée des signaux. Jean-Luc, le
27-11-2026 à 18h24 : « il est possible que le hasard, puisqu'on aurait joué une autre action avant, fasse qu'on tombe
sur les deux qui ont échoué, et auquel cas on exclurait cette stratégie qui est ultra bonne » ; à 18h27 : « Bon, là
c'est une véritable proposition, donc je valide le principe » (A-1092). Ce module fabrique, à partir des opérations
en jetons illimités, des milliers de parcours à un jeton tirés au hasard, et mesure SUR CES PARCOURS les deux mesures
que A-1092 nomme : le « creux 1 fois sur 20 sur 5 ans » (A-796, mesure ② de l'étape 6) et le « gain net par an au
pire » (A-793, mesure ③), au niveau de confiance de 95 % (point ⑤ des « À PRÉCISER » de la loi, choix technique).
Il fait aussi le CONTRÔLE AJOUTÉ par A-1092 : comparer les signaux pris et les signaux ignorés, pour voir si la règle
de prise (premier signal ; même jour → le plus survendu, A-800, R-207bis) prend par construction les plus mauvais.

CE QU'IL NE FAIT PAS, EXPRÈS. ① La borne de Wilson (mesure ① de l'étape 6) et ④ le départage NE SONT PAS calculés sur
les parcours : le texte de la loi dit « LES MESURES ① À ④ », mais la décision A-1092 ne nomme que ② et ③ (relecteur
Cowork, défaut R5-8) ; c'est une décision de Jean-Luc, et ce module ne l'invente pas. La « part des parcours
gagnants » (Niveau 1 ⑥ de la loi) est AFFICHÉE, son seuil est « À MESURER » (table des seuils de la loi) : elle ne
décide rien. Il ne compare à aucun seuil (20 000 €, 55 %) : les seuils vivent dans la loi, la grille les applique.

① RÔLE — Tirer les parcours à un jeton d'une stratégie et rendre les mesures ② et ③ de l'étape 6 et le contrôle des
  signaux pris et ignorés, en APPELANT les fonctions qui font déjà le travail (R-708 : deux implémentations d'une
  même chose divergent toujours) : le départage du même jour est `TENIR_LES_POSITIONS.departager_r207bis` ; le
  creux « 1 fois sur 20 sur 5 ans » est `MESURER_LES_INDICATEURS.seuils_1_sur_20_sur_5_ans`, la mécanique même de
  l'alarme de creux en direct (trades tirés au hasard) ; le rang des quantiles est `MODULE_JUGEMENT.valeur_au_rang` ;
  la durée de la période est `MESURER_LES_INDICATEURS.annees_de_la_periode`.
② CONTEXTE D'APPEL — Aucun programme du circuit ne l'appelle encore (branchement : lignes E6-2, E6-3, E6-PARCOURS et
  E6-PRIS-IGNORES de donnees/GRILLE_R505_V2.csv, à faire par le Chat). Éprouvé par
  tests/EPREUVES_DES_PARCOURS_A_UN_JETON_Ven_27-11-2026.py.
③ ENTRÉE — Voir chaque fonction. Aucune ligne de commande.
④ CONDITIONS D'ENTRÉE — Python 3, bibliothèque standard ; à côté de ce fichier : MESURER_LES_INDICATEURS.py et les
  briques qu'il charge (TENIR_LES_POSITIONS, MODULE_JUGEMENT, MESURER_LA_PERFORMANCE…), COMMUN.py.
⑤ SORTIE — Le module rend des fonctions et cinq constantes (les deux façons de tirer, les deux ordres du jour, le
  nom du tirage historique).
⑥ TRAITEMENT — Rien ne s'exécute au chargement, sinon la définition des constantes.
⑦ UNITÉ — Euros (`_eur`), euros par an (`_par_an_eur`), parts entre 0 et 1, pourcents (`_pct`), dates AAAA-MM-JJ.
⑧ POURQUOI — A-1092 (voir le sens en tête) ; la loi, étape 6 : « le programme rejoue la stratégie des milliers de
  fois avec un seul jeton, en tirant au hasard quels signaux le jeton aurait pris, et l'on décide sur la liste des
  résultats possibles, pas sur le seul parcours historique ; même mécanique que l'alarme de creux en direct (trades
  tirés au hasard), écrite une seule fois (R-708) ».
⑨ CE QUI CLOCHE — Consigné, non corrigé (R-752) : ① la façon de tirer les parcours n'est PAS fixée par la loi (« date
  de départ au hasard, ou choix au hasard parmi les signaux disponibles, à éprouver ») : les deux sont programmées,
  l'appelant DOIT choisir, rien n'est choisi par défaut ; ② le creux se mesure sur le MÉLANGE des opérations de tous
  les parcours (voir `mesurer_les_parcours`) : il garde l'hypothèse d'indépendance des opérations de
  `seuils_1_sur_20_sur_5_ans` (son ⑨ ①, n°107) ; ③ les opérations d'entrée n'ont pas de CCI chez le juge (il ne le
  garde pas) : l'appelant doit l'ajouter, ou passer par `rattacher_les_signaux`.
⑩ EFFET — Aucun : lit ce qu'on lui passe, n'écrit aucun fichier, ne sort pas sur le réseau.
⑪ TERMINAISON — Rend la main.

⑫ DÉFINITIONS —
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est passé.
  un jeton : une seule position à la fois par stratégie ; un signal reçu pendant une position est ignoré.
  jetons illimités : tous les signaux joués, chacun avec sa position ; cette comptabilité juge la qualité.
  un parcours à un jeton : la suite des opérations qu'un jeton unique aurait prises, tirée au hasard selon une des
    deux façons de tirer ; le parcours HISTORIQUE est celui de la règle du direct, depuis la première séance.
  le creux : la plus grande baisse du cumul des gains nets depuis un sommet, quelle que soit sa durée, en euros.
"""

import os
import random
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)

import COMMUN  # noqa: E402
import MESURER_LES_INDICATEURS as MLI  # noqa: E402

# LES DEUX FAÇONS DE TIRER UN PARCOURS, celles que nomme la loi (étape 6, « RESTE À FIXER ») ; aucune n'est un défaut.
DEPART_AU_HASARD = "depart_au_hasard"
CHOIX_AU_HASARD = "choix_au_hasard"
TIRAGES = (DEPART_AU_HASARD, CHOIX_AU_HASARD)
# LES DEUX ORDRES D'UN JOUR À PLUSIEURS SIGNAUX : la règle du direct (R-207bis, A-800), ou le hasard.
ORDRE_R207BIS = "R207BIS"
ORDRE_AU_HASARD = "HASARD"
# Le nom de stratégie posé sur les signaux passés à `departager_r207bis`, qui départage stratégie par stratégie :
# un parcours est celui d'UNE stratégie, tous ses signaux portent donc le même nom.
_UNE_STRATEGIE = "PARCOURS"


def rattacher_les_signaux(operations, signaux):
    """Rend les opérations, chacune avec la vraie date de son signal et son CCI, pris aux signaux.

    ① RÔLE — Adapter des opérations venues du journal des trades (qui n'a ni date de signal ni CCI) à l'entrée de ce
      module.
    ② CONTEXTE D'APPEL — L'épreuve, sur le rejeu du golden (`MESURER_LES_INDICATEURS.calibrer_sur_le_golden`) ; tout
      appelant dont les opérations n'ont pas de CCI.
    ③ ENTRÉE — `operations` : des opérations (`valeur`, `date_entree`, `date_sortie`, `net`) · `signaux` : les
      signaux qui les ont fait naître (`valeur`, `date_signal`, `cci`).
    ④ CONDITIONS D'ENTRÉE — L'entrée se fait à la séance qui suit le signal (R-601) : le signal d'une opération est,
      pour sa valeur, le plus tardif strictement avant la date d'entrée.
    ⑤ SORTIE — UNE valeur : une NOUVELLE liste d'opérations (copies), chacune avec `date_signal` et `cci`.
      [rend: 1]
    ⑥ TRAITEMENT — ① ranger les signaux par valeur et par date · ② pour chaque opération, prendre le dernier signal
      de sa valeur avant son entrée · ③ lever s'il n'y en a pas.
    ⑦ UNITÉ — Dates AAAA-MM-JJ ; CCI sans unité.
    ⑧ POURQUOI — `operations_du_journal` met la date d'ENTRÉE à la place de la date du signal (son ⑨) : la règle du
      jeton, qui compare le jour du signal au jour de la sortie précédente, serait fausse d'une séance.
    ⑨ CE QUI CLOCHE — Le rapprochement se fait par le nom de valeur tel qu'écrit, sans `cle_valeur` du juge : deux
      graphies d'une même valeur ne se rapprochent pas (le golden n'en a qu'une).
    ⑩ EFFET — Aucun : les opérations reçues ne sont pas modifiées.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` si une opération n'a aucun signal avant son entrée.
      [sort: non]
    """
    par_valeur = {}
    for s in signaux:
        par_valeur.setdefault(s["valeur"], []).append(s)
    for v in par_valeur:
        par_valeur[v].sort(key=lambda s: s["date_signal"])
    rendu = []
    for o in operations:
        avant = [s for s in par_valeur.get(o["valeur"], []) if s["date_signal"] < o["date_entree"]]
        if not avant:
            raise ValueError("opération %s entrée le %s : aucun signal avant son entrée" % (o["valeur"],
                                                                                          o["date_entree"]))
        n = dict(o)
        n["date_signal"] = avant[-1]["date_signal"]
        n["cci"] = avant[-1]["cci"]
        rendu.append(n)
    return rendu


def _non_terminee(o):
    """Dit si une opération est restée ouverte à la fin des données (NON TERMINÉE, A-1100).

    ① RÔLE — Le seul test « non terminée » du module : il APPELLE `MODULE_JUGEMENT.est_non_terminee`, la règle unique
      du dépôt (réunion I1 du 28-11-2026, contradiction C1 de la relecture V2 : ce module en avait une copie, R-708).
    ② CONTEXTE D'APPEL — `prendre_en_un_jeton`, `_resumer`, `comparer_pris_et_ignores`, `mesurer_les_parcours`.
    ③ ENTRÉE — `o` : une opération.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le rendu de `MODULE_JUGEMENT.est_non_terminee(o)` (motif FIN_DES_DONNEES ou sortie absente).
      [rend: 1]
    ⑥ TRAITEMENT — charger MODULE_JUGEMENT (voisin, par son nom) et lui poser la question.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 27-11-2026 à 19h29 (A-1100) : les positions encore ouvertes à la fin sont
      marquées « NON TERMINÉES » et comptées à part, jamais inventées ; le motif vit dans COMMUN (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import MODULE_JUGEMENT   # à la demande : la règle unique (R-708)
    return MODULE_JUGEMENT.est_non_terminee(o)


def prendre_en_un_jeton(operations, depart, ordre_du_jour, racine, hasard=None):
    """Rend ce qu'un jeton unique aurait pris parmi les opérations en jetons illimités, à partir d'une séance.

    ① RÔLE — La règle du jeton appliquée à une liste d'opérations : un signal est pris si le jeton est libre le jour
      du signal (la position précédente est sortie ce jour-là ou avant), sinon il est ignoré ; un jour à plusieurs
      signaux, le premier dans l'ordre du jour est pris, les autres ignorés. C'EST UNE SECONDE ÉCRITURE de la règle
      d'occupation de `TENIR_LES_POSITIONS.tenir` / `ouvrir_sur_signaux` (R-708 : deux implémentations divergent
      toujours) — voir le ⑨ ④ : elle est attachée à `tenir` par l'épreuve E2.
    ② CONTEXTE D'APPEL — `tirer_les_parcours` (chaque parcours) et `mesurer_les_parcours` (le parcours historique).
    ③ ENTRÉE — `operations` : les opérations en jetons illimités, chacune avec `valeur`, `date_signal`, `date_sortie`,
      `net` (euros), `cci`, et `motif` facultatif · `depart` : la séance (AAAA-MM-JJ) où le jeton commence ; les
      signaux antérieurs sont joués APRÈS la fin, en boucle (voir ⑥) · `ordre_du_jour` : `ORDRE_R207BIS` ou
      `ORDRE_AU_HASARD` · `racine` : la racine du dépôt · `hasard` : un `random.Random`, exigé avec `ORDRE_AU_HASARD`.
    ④ CONDITIONS D'ENTRÉE — Chaque opération porte un CCI fini (sinon `departager_r207bis` lève) ; les dates sont au
      format AAAA-MM-JJ (comparées comme des textes).
    ⑤ SORTIE — UNE valeur : un dictionnaire — `pris` (les opérations prises, dans l'ordre), `ignores` (des couples
      (opération, cause) : « jeton occupé » ou « couture »), `depart`, `ordre_du_jour`.
      [rend: 1]
    ⑥ TRAITEMENT — ① ranger les signaux par jour · ② jouer d'abord les jours à partir de `depart`, puis — la
      « couture » — les jours d'avant `depart`, jeton libéré, en n'y prenant qu'une opération qui sort AVANT `depart`
      (sinon elle chevaucherait le début du parcours : elle est ignorée, cause « couture ») · ③ chaque jour, ordonner
      ses signaux : par `TENIR_LES_POSITIONS.departager_r207bis` (CCI le plus bas, égalité → alphabétique), ou au
      hasard · ④ le premier signal est pris si le jour du signal est postérieur ou égal à la sortie de la position
      en cours ; une opération NON TERMINÉE prise garde le jeton jusqu'à la fin de son tour.
    ⑦ UNITÉ — Dates AAAA-MM-JJ.
    ⑧ POURQUOI — C'est la règle du circuit du soir (`TENIR_LES_POSITIONS.tenir`) : on clôture AVANT d'ouvrir, donc
      une position sortie le jour D libère le jeton pour un signal de D (son ⑧) ; une position en attente d'entrée ou
      ouverte l'occupe (`ouvrir_sur_signaux`) ; R-207bis ne vit qu'à UN endroit (A-839). En un jeton, l'opération
      d'un signal pris est celle des jetons illimités (mêmes entrée, sortie, frais) : le parcours se tire donc dans
      la liste des jetons illimités, sans rejouer les cours. La couture fait que chaque parcours couvre TOUTE la
      période, quel que soit son départ (idée de la méthode « circulaire » des rééchantillonnages par blocs : « we
      wrap the data around a circle », Varga et Zempléni, arXiv 1606.00263, 2016, résumé lu ; Politis et Romano,
      1992, NON LU) : les gains par an se comparent d'un parcours à l'autre. Avec `depart` = la première séance et
      l'ordre R-207bis, c'est le parcours historique.
    ⑨ CE QUI CLOCHE — ① La couture coupe la période en deux tours qui ne se suivent pas dans le temps : le creux d'un
      parcours peut enjamber la couture. ② Le jeton est libre au départ, même si, en vrai, une position aurait été
      ouverte avant `depart` : c'est le principe du départ au hasard. ③ Les achats refusés (hors CAC 40, A-577) ne
      sont pas dans les opérations du juge : un signal refusé n'occupe pas le jeton, comme dans `tenir`.
      ④ SECONDE ÉCRITURE (R-708), consignée pour le BACKLOG : `tenir` rejoue les COURS séance par séance (2,6 s pour
      le golden, son ⑨ ② dans `rejouer_les_signaux`) ; mille parcours prendraient près d'une heure. La règle est donc
      réécrite ici sur la liste des opérations, et l'épreuve E2 la confronte à `tenir` opération par opération sur le
      golden (44 opérations, +58 800,00 €) : si `tenir` change, E2 doit rougir. Elle ne couvre pas un achat retardé
      (entrée après la séance qui suit le signal) : la date du signal est comparée à la sortie, comme `tenir` le
      fait par le statut « en attente ».
    ⑩ EFFET — Aucun : les opérations reçues ne sont pas modifiées ; `hasard` avance.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` (ordre inconnu, hasard manquant) et laisse remonter
      `DepartageImpossible` (CCI absent ou non fini).
      [sort: non]
    """
    if ordre_du_jour not in (ORDRE_R207BIS, ORDRE_AU_HASARD):
        raise ValueError("ordre du jour %r inconnu (%s, %s)" % (ordre_du_jour, ORDRE_R207BIS, ORDRE_AU_HASARD))
    if ordre_du_jour == ORDRE_AU_HASARD and hasard is None:
        raise ValueError("l'ordre au hasard exige un tirage (`hasard`)")
    TP = MLI.charger_les_briques(racine)["TP"]
    par_jour = {}
    for o in operations:
        par_jour.setdefault(o["date_signal"], []).append(o)
    jours = sorted(par_jour)
    tours = [[j for j in jours if j >= depart], [j for j in jours if j < depart]]
    pris, ignores = [], []
    for tour, jours_du_tour in enumerate(tours):
        sortie = None  # le jeton est libre au début de chaque tour
        for j in jours_du_tour:
            enveloppes = [{"strategie": _UNE_STRATEGIE, "valeur": o["valeur"], "cci": o["cci"], "_op": o}
                          for o in sorted(par_jour[j], key=lambda o: str(o["valeur"]))]
            if ordre_du_jour == ORDRE_R207BIS:
                enveloppes = TP.departager_r207bis(enveloppes)
            else:
                hasard.shuffle(enveloppes)
            for e in enveloppes:
                o = e["_op"]
                if sortie is not None and j < sortie:
                    ignores.append((o, "jeton occupé"))
                    continue
                if tour == 1 and (_non_terminee(o) or not o["date_sortie"] < depart):
                    ignores.append((o, "couture"))
                    continue
                pris.append(o)
                sortie = "9999-12-31" if _non_terminee(o) else o["date_sortie"]
    return {"pris": pris, "ignores": ignores, "depart": depart, "ordre_du_jour": ordre_du_jour}


def tirer_les_parcours(operations, seances, tirage, nombre, racine, graine):
    """Rend `nombre` parcours à un jeton tirés au hasard selon la façon de tirer demandée.

    ① RÔLE — Fabriquer la « liste des résultats possibles » en un jeton (A-1092).
    ② CONTEXTE D'APPEL — `mesurer_les_parcours`.
    ③ ENTRÉE — `operations` : comme `prendre_en_un_jeton` · `seances` : les séances de la période jouée, AAAA-MM-JJ ·
      `tirage` : `DEPART_AU_HASARD` (séance de départ tirée parmi `seances`, puis la règle du direct) ou
      `CHOIX_AU_HASARD` (départ à la première séance, et un jour à plusieurs signaux, le signal pris est tiré au
      hasard au lieu de R-207bis) · `nombre` : le nombre de parcours · `racine` · `graine` : la graine du hasard.
    ④ CONDITIONS D'ENTRÉE — `seances` non vide ; `nombre` ≥ 1.
    ⑤ SORTIE — UNE valeur : la liste des `nombre` rendus de `prendre_en_un_jeton`.
      [rend: 1]
    ⑥ TRAITEMENT — un seul `random.Random(graine)` pour tous les parcours ; pour chacun, tirer selon `tirage`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La loi (étape 6, « RESTE À FIXER ») nomme ces deux façons et dit « à éprouver » : aucune n'est
      choisie ici, l'appelant doit nommer la sienne. Le choix au hasard parmi les signaux d'un même jour est la
      pratique décrite par AmiBroker (guide « Monte Carlo Simulation of your trading system », lu le 27-11-2026 :
      « If there are more signals to open positions than we could take, this process would lead to randomized trade
      picks »), qui prévient qu'avec un classement remplacé par le hasard on éprouve « white noise, not the system »
      quand le système dépend de ce classement — d'où le contrôle des signaux pris et ignorés.
    ⑨ CE QUI CLOCHE — Avec `CHOIX_AU_HASARD`, seuls les jours à plusieurs signaux changent : une stratégie qui
      signale rarement deux valeurs le même jour donne presque toujours le parcours historique (le nombre de
      parcours DISTINCTS le dit, `mesurer_les_parcours`). Les séances de `seances` hors période ne sont pas refusées.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur une façon de tirer inconnue, un nombre < 1 ou des séances
      vides.
      [sort: non]
    """
    if tirage not in TIRAGES:
        raise ValueError("façon de tirer %r inconnue (%s)" % (tirage, ", ".join(TIRAGES)))
    if not isinstance(nombre, int) or nombre < 1:
        raise ValueError("nombre de parcours %r : un entier ≥ 1 attendu" % (nombre,))
    if not seances:
        raise ValueError("aucune séance : pas de départ possible")
    seances = sorted(seances)
    hasard = random.Random(graine)
    rendu = []
    for _ in range(nombre):
        if tirage == DEPART_AU_HASARD:
            rendu.append(prendre_en_un_jeton(operations, seances[hasard.randrange(len(seances))], ORDRE_R207BIS,
                                             racine))
        else:
            rendu.append(prendre_en_un_jeton(operations, seances[0], ORDRE_AU_HASARD, racine, hasard))
    return rendu


def _resumer(parcours, annees):
    """Rend les chiffres d'un parcours : opérations, gain net, gain par an, gagnant, non terminées.

    ① RÔLE — Une ligne de la « liste des résultats possibles ».
    ② CONTEXTE D'APPEL — `mesurer_les_parcours`.
    ③ ENTRÉE — `parcours` : un rendu de `prendre_en_un_jeton` · `annees` : la durée de la période, en années.
    ④ CONDITIONS D'ENTRÉE — `annees` > 0.
    ⑤ SORTIE — UNE valeur : un dictionnaire (`nets`, `operations`, `gain_net_eur`, `gain_net_par_an_eur`,
      `gagnant`, `non_terminees` (leur nombre), `resultat_latent_non_terminees_eur` (A-1108 : la somme de leurs `net`,
      résultat latent au dernier cours réel, frais de vente compris ; rendu même à zéro), `cle`).
      [rend: 1]
    ⑥ TRAITEMENT — mettre à part les NON TERMINÉES (A-1100) ; sommer les gains nets des autres ; diviser par les
      années ; gagnant = gain net strictement positif ; clé = la suite des (valeur, date du signal) prises.
    ⑦ UNITÉ — Euros ; euros par an ; un compte.
    ⑧ POURQUOI — Le gain par an se rapporte à la période DÉCLARÉE, comme `mesurer_les_indicateurs` (son ⑦) ; la
      couture fait que chaque parcours la couvre entière.
    ⑨ CE QUI CLOCHE — Un gain nul n'est pas « gagnant ».
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import MODULE_JUGEMENT   # la mise à part d'A-1108, l'endroit unique (R-708, réunion I1)
    faites, a_part = MODULE_JUGEMENT.mettre_a_part_les_non_terminees(parcours["pris"])
    nets = [float(o["net"]) for o in faites]
    gain = sum(nets)
    return {"nets": nets, "operations": len(nets), "gain_net_eur": gain, "gain_net_par_an_eur": gain / annees,
            "gagnant": gain > 0, "non_terminees": a_part["n"],
            "resultat_latent_non_terminees_eur": a_part["resultat_latent_eur"],
            "cle": tuple((o["valeur"], o["date_signal"]) for o in parcours["pris"])}


def comparer_pris_et_ignores(historique, parcours):
    """Rend le contrôle ajouté par A-1092 : la règle de prise prend-elle par construction les plus mauvais signaux ?

    ① RÔLE — Le CONTRÔLE AJOUTÉ de l'étape 6 : comparer les signaux pris et ignorés en un jeton.
    ② CONTEXTE D'APPEL — `mesurer_les_parcours`.
    ③ ENTRÉE — `historique` : le rendu de `prendre_en_un_jeton` pour la règle du direct depuis la première séance ·
      `parcours` : les rendus des parcours tirés au hasard.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire — `pris` et `ignores` (chacun : `operations`, `taux_reussite_pct`,
      `gain_moyen_eur`) du parcours historique ; `grappes` (le premier signal d'une grappe, pris, contre les suivants,
      ignorés pendant sa position : `grappes`, `premiers`, `suivants`) ; `part_des_parcours_pas_mieux` (la part des
      parcours tirés dont le gain moyen par opération prise est inférieur ou égal à celui du parcours historique) ;
      `etat` : « ALERTE » si cette part est au plus 1 − 95 %, « RIEN NE LE MONTRE » sinon, « INCONNU » sans parcours
      tiré ou sans opération prise.
      [rend: 1]
    ⑥ TRAITEMENT — ① séparer, dans le parcours historique, les opérations prises (hors NON TERMINÉES) et les ignorées
      (hors couture et NON TERMINÉES) · ② pour chaque opération prise, sa grappe : les signaux ignorés parce qu'elle
      tenait le jeton (jour du signal entre le sien et sa sortie) · ③ situer le gain moyen historique dans la liste
      des gains moyens des parcours tirés · ④ alerter si le parcours historique est dans les 5 % les plus mauvais.
    ⑦ UNITÉ — Euros ; pourcents ; parts entre 0 et 1.
    ⑧ POURQUOI — A-1092 ③ : « comparer les signaux pris et les signaux ignorés en un jeton, pour vérifier que la règle
      de prise (premier signal ; même jour → le plus survendu, A-800) ne prend pas par construction les plus mauvais
      (exemple à mesurer : le premier signal d'une chute du marché est-il plus souvent perdant que les suivants ?) » :
      les grappes répondent à l'exemple, le rang dans les parcours tirés au test. Le niveau de 95 % est celui des
      bornes « au pire » de l'étape 6 (point ⑤ des « À PRÉCISER », choix technique), lu à
      `MESURER_LES_INDICATEURS.UNE_FOIS_SUR_VINGT` (R-708).
    ⑨ CE QUI CLOCHE — ① Le seuil d'alerte reprend le niveau des bornes « au pire » : la loi ne fixe pas de seuil à ce
      contrôle (décision pour Jean-Luc, dans la note). ② Pris et ignorés NE SONT PAS des échantillons indépendants
      (les ignorés tombent pendant une position, donc dans le même moment du marché) : leur écart est AFFICHÉ, il ne
      décide pas ; seul le rang dans les parcours tirés alerte. ③ Avec `DEPART_AU_HASARD`, les parcours tirés gardent
      R-207bis : l'alerte compare alors des moments de départ, pas des règles de prise ; avec `CHOIX_AU_HASARD`, elle
      compare la règle au hasard, mais seulement sur les jours à plusieurs signaux.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def chiffres(ops):
        """Rend le compte, le taux de réussite et le gain moyen d'une liste d'opérations.

        ① RÔLE — Un résumé d'une liste d'opérations.
        ② CONTEXTE D'APPEL — `comparer_pris_et_ignores`, quatre fois.
        ③ ENTRÉE — `ops` : des opérations portant `net`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : un dictionnaire (`operations`, `taux_reussite_pct`, `gain_moyen_eur`).
          [rend: 1]
        ⑥ TRAITEMENT — compter, compter les gains strictement positifs, faire la moyenne.
        ⑦ UNITÉ — Euros ; pourcents.
        ⑧ POURQUOI — Les quatre listes comparées se résument de la même façon.
        ⑨ CE QUI CLOCHE — Une liste vide rend un taux et une moyenne à None.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        nets = [float(o["net"]) for o in ops]
        if not nets:
            return {"operations": 0, "taux_reussite_pct": None, "gain_moyen_eur": None}
        return {"operations": len(nets), "taux_reussite_pct": 100.0 * sum(1 for x in nets if x > 0) / len(nets),
                "gain_moyen_eur": sum(nets) / len(nets)}

    pris = [o for o in historique["pris"] if not _non_terminee(o)]
    ignores = [o for o, cause in historique["ignores"] if cause != "couture" and not _non_terminee(o)]
    premiers, suivants, grappes = [], [], 0
    for p in pris:
        g = [o for o in ignores if p["date_signal"] <= o["date_signal"] < p["date_sortie"] and o is not p]
        if g:
            grappes += 1
            premiers.append(p)
            suivants += g

    def moyenne(ps):
        """Rend le gain moyen par opération prise d'un parcours, None sans opération.

        ① RÔLE — La mesure que l'on classe parmi les parcours.
        ② CONTEXTE D'APPEL — `comparer_pris_et_ignores`, une fois par parcours.
        ③ ENTRÉE — `ps` : un rendu de `prendre_en_un_jeton`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : un nombre, ou None sans opération terminée.
          [rend: 1]
        ⑥ TRAITEMENT — moyenne des gains nets des opérations prises, NON TERMINÉES exclues.
        ⑦ UNITÉ — Euros.
        ⑧ POURQUOI — Le gain moyen par opération ne dépend pas du nombre d'opérations prises.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        nets = [float(o["net"]) for o in ps["pris"] if not _non_terminee(o)]
        return sum(nets) / len(nets) if nets else None

    m_h = moyenne(historique)
    tires = [m for m in (moyenne(p) for p in parcours) if m is not None]
    if m_h is None or not tires:
        part, etat = None, "INCONNU"
    else:
        part = sum(1 for m in tires if m <= m_h) / len(tires)
        etat = "ALERTE" if part <= 1.0 - MLI.UNE_FOIS_SUR_VINGT else "RIEN NE LE MONTRE"
    return {"pris": chiffres(pris), "ignores": chiffres(ignores),
            "grappes": {"grappes": grappes, "premiers": chiffres(premiers), "suivants": chiffres(suivants)},
            "gain_moyen_historique_eur": m_h, "part_des_parcours_pas_mieux": part, "etat": etat}


def mesurer_les_parcours(operations, periode, seances, tirage, nombre, racine, graine,
                         tirages_du_seuil=MLI.TIRAGES_DU_SEUIL):
    """Rend les mesures ② et ③ de l'étape 6 sur des milliers de parcours à un jeton, et le contrôle pris/ignorés.

    ① RÔLE — Le point d'entrée du lot : ce que la grille lira pour E6-2, E6-3, E6-PARCOURS et E6-PRIS-IGNORES.
    ② CONTEXTE D'APPEL — L'épreuve ; demain la grille de l'étape 6 (branchement à faire).
    ③ ENTRÉE — `operations` : les opérations en JETONS ILLIMITÉS de la version (voir `prendre_en_un_jeton`) ·
      `periode` : le couple (début, fin) DÉCLARÉ · `seances` : les séances de la période · `tirage` : une des deux
      façons de tirer, SANS DÉFAUT · `nombre` : le nombre de parcours, SANS DÉFAUT (la loi dit « des milliers ») ·
      `racine` · `graine` : la graine du hasard · `tirages_du_seuil` : passé à `seuils_1_sur_20_sur_5_ans` quand son
      calcul exact n'est pas faisable, `MESURER_LES_INDICATEURS.TIRAGES_DU_SEUIL` par défaut.
    ④ CONDITIONS D'ENTRÉE — Celles de `tirer_les_parcours` ; la période dure plus de 0 jour.
    ⑤ SORTIE — UNE valeur : un dictionnaire —
      `creux_1_sur_20_sur_5_ans_eur` (mesure ②) avec `creux_marge_basse_eur`, `creux_marge_haute_eur`,
      `creux_methode` ; `gain_net_par_an_au_pire_eur` (mesure ③) ; `gain_net_par_an_median_eur` ;
      `part_des_parcours_gagnants` et `seuil_des_parcours_gagnants` (« À MESURER ») ; `parcours`, `parcours_distincts`,
      `parcours_avec_non_terminee` ; `operations_par_an_moyen` ; `historique` (les mêmes chiffres pour le seul
      parcours historique, `creux_1_sur_20_sur_5_ans_eur` compris) ; `pris_et_ignores` (rendu de
      `comparer_pris_et_ignores`) ; `mesure_1_wilson` et `mesure_4_departage` : « NON PROGRAMMÉE » et la raison ;
      rappels `tirage`, `nombre`, `graine`, `periode`, `annees`, `niveau_de_confiance`.
      [rend: 1]
    ⑥ TRAITEMENT — ① la durée de la période par `annees_de_la_periode` · ② le parcours historique (première séance,
      R-207bis) · ③ `nombre` parcours tirés · ④ MESURE ③ : la liste des gains nets par an des parcours tirés,
      rangée ; « au pire » = la valeur au rang 5 % (`MODULE_JUGEMENT.valeur_au_rang`), soit celle que 95 % des
      parcours atteignent ou dépassent · ⑤ MESURE ② : `seuils_1_sur_20_sur_5_ans` sur le MÉLANGE des opérations de
      tous les parcours tirés (chaque opération prise par un parcours y figure une fois par parcours qui la prend),
      au rythme moyen des parcours : la valeur de creux sur 5 ans que seuls 5 % des tirages dépassent · ⑥ le même
      calcul sur le seul parcours historique, affiché à côté · ⑦ le contrôle pris/ignorés.
    ⑦ UNITÉ — Euros ; euros par an ; parts entre 0 et 1 ; opérations par an.
    ⑧ POURQUOI — A-1092 : la mise en direct se décide « sur la liste des résultats possibles, pas sur le seul parcours
      historique » ; le niveau 95 % est le point ⑤ des « À PRÉCISER » (le même que le pire cas en argent, A-1085).
      Le creux reprend TELLE QUELLE la mécanique de l'alarme de creux (tirage d'opérations avec remise, calcul exact
      quand il est faisable) : « même mécanique que l'alarme de creux en direct (trades tirés au hasard), écrite une
      seule fois (R-708) ». PROPRIÉTÉ VOULUE : quand tous les parcours tirés sont le parcours historique, le creux
      rendu est EXACTEMENT celui de `mesurer_les_indicateurs` en un jeton (l'épreuve le montre sur le golden :
      21 500 €), parce que le mélange n'est alors que la liste historique répétée, et que ses proportions sont les
      mêmes. Le gain « au pire » se lit sur la liste des parcours eux-mêmes : la période déclarée se mesure en
      années, sans extrapolation, et la couture fait que chaque parcours la couvre entière.
    ⑨ CE QUI CLOCHE — ① Le « gain par an au pire » d'A-793, dans `mesurer_les_indicateurs`, est la borne basse par
      rééchantillonnage du gain moyen (l'incertitude sur l'AVANTAGE) ; ici, c'est le 5 % des parcours (le hasard de
      l'ARRIVÉE des signaux). Les deux ne mesurent pas la même chose : le parcours historique porte les deux, côte à
      côte (`historique`) ; lequel décide, ou leur combinaison, est une décision de Jean-Luc (note de livraison).
      ② Le mélange garde l'hypothèse d'indépendance des opérations (n°107, en attente) et perd l'ordre propre à
      chaque parcours. ③ La part des parcours gagnants ne décide rien (seuil « À MESURER »). ④ Les mesures ① et ④ ne
      sont pas faites (R5-8). ⑤ Coût : le parcours coûte environ le nombre d'opérations ; le creux par tirage
      jusqu'à une dizaine de secondes (son ⑨ ③).
    ⑩ EFFET — Aucun (le hasard a sa propre graine ; le hasard global n'est pas touché).
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur une entrée contraire au ④.
      [sort: non]
    """
    b = MLI.charger_les_briques(racine)
    annees = MLI.annees_de_la_periode(periode)
    if not annees:
        raise ValueError("période %r de 0 jour : aucun gain par an" % (periode,))
    seances = sorted(seances)
    historique = prendre_en_un_jeton(operations, seances[0], ORDRE_R207BIS, racine) if seances else None
    tires = tirer_les_parcours(operations, seances, tirage, nombre, racine, graine)
    resumes = [_resumer(p, annees) for p in tires]
    gains = sorted(r["gain_net_par_an_eur"] for r in resumes)
    melange = [x for r in resumes for x in r["nets"]]
    rythme = sum(r["operations"] for r in resumes) / len(resumes) / annees
    seuil = MLI.seuils_1_sur_20_sur_5_ans(melange, rythme, racine, tirages_du_seuil, graine)
    h = _resumer(historique, annees)
    seuil_h = MLI.seuils_1_sur_20_sur_5_ans(h["nets"], h["operations"] / annees, racine, tirages_du_seuil, graine)
    non_prog = ("NON PROGRAMMÉE : la loi écrit « LES MESURES ① À ④ » sur les parcours, la décision A-1092 ne nomme que "
                "② et ③ (relecteur Cowork, R5-8) — décision de Jean-Luc")
    return {
        "creux_1_sur_20_sur_5_ans_eur": seuil["creux_eur"],
        "creux_marge_basse_eur": seuil["creux_marge_basse_eur"],
        "creux_marge_haute_eur": seuil["creux_marge_haute_eur"],
        "creux_methode": seuil["creux_methode"],
        "gain_net_par_an_au_pire_eur": b["MJ"].valeur_au_rang(gains, 1.0 - MLI.UNE_FOIS_SUR_VINGT),
        "gain_net_par_an_median_eur": b["MJ"].valeur_au_rang(gains, 0.5),
        "part_des_parcours_gagnants": sum(1 for r in resumes if r["gagnant"]) / len(resumes),
        "seuil_des_parcours_gagnants": "À MESURER (table des seuils de la loi, parcours_un_jeton_gagnants, A-1092)",
        "parcours": len(resumes),
        "parcours_distincts": len({r["cle"] for r in resumes}),
        "parcours_avec_non_terminee": sum(1 for r in resumes if r["non_terminees"]),
        "operations_par_an_moyen": rythme,
        "historique": {"operations": h["operations"], "gain_net_eur": h["gain_net_eur"],
                       "gain_net_par_an_eur": h["gain_net_par_an_eur"], "non_terminees": h["non_terminees"],
                       "creux_1_sur_20_sur_5_ans_eur": seuil_h["creux_eur"],
                       "creux_methode": seuil_h["creux_methode"]},
        "pris_et_ignores": comparer_pris_et_ignores(historique, tires),
        "mesure_1_wilson": non_prog, "mesure_4_departage": non_prog,
        "tirage": tirage, "nombre": nombre, "graine": graine, "periode": tuple(periode), "annees": annees,
        "niveau_de_confiance": MLI.UNE_FOIS_SUR_VINGT,
    }
