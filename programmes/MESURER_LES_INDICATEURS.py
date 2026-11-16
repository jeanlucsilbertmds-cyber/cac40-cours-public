#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MESURER_LES_INDICATEURS.py — les indicateurs de performance d'une stratégie, calculés UNE fois, au même endroit.

Simulation uniquement : aucun ordre réel n'est jamais passé.
Écrit le samedi 14-11-2026 (Paris), étape INDIC du planning du plan V7.

LE SENS EN TÊTE. Jean-Luc a décidé le 14-11-2026 (A-788, 17h36-17h39) que la fiche d'une stratégie porte deux blocs
figés, 70 % et 30 %, et que le carnet porte la vraie vie, « mêmes indicateurs ». Pour que « mêmes indicateurs » soit
vrai, chaque indicateur doit être calculé par UNE seule fonction, que le juge (les blocs) et la mesure du soir (le
carnet) appelleront tous les deux. Aujourd'hui, le taux et sa borne de Wilson sont calculés deux fois, le creux trois
fois, la série de pertes deux fois, et sept indicateurs ne sont calculés nulle part (analyse d'impact du 14-11-2026,
`etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/IMPACT_FICHE_ET_CARNET_Sam_14-11-2026.md`, §1b). Ce
programme les réunit, en APPELANT les fonctions qui existent déjà (deux implémentations d'une même chose divergent
toujours, R-708) et en écrivant seulement celles qui manquent. Il ne branche RIEN dans le juge ni dans la mesure du
soir : ce branchement viendra après l'installation des lots en attente, pour éviter les conflits (consigne du Chat).

Il porte aussi LE REJEU « UN JETON » : l'historique des signaux repassé, soir après soir, dans les fonctions mêmes du
circuit (`TENIR_LES_POSITIONS.tenir`), avec la règle de départage R-207bis. Aucun programme du dépôt ne le faisait ;
il retrouve le golden un jeton au centime (44 opérations, 63,6 %, +58 800,00 €) avant de servir.

① RÔLE — Rendre, pour une liste d'opérations et une comptabilité, la liste exacte des indicateurs décidés en A-788,
  chacun avec son unité dans son nom ; et rejouer « un jeton » par le circuit.
② CONTEXTE D'APPEL — Lancé à la main : `python3 programmes/MESURER_LES_INDICATEURS.py .` calibre sur le golden et
  affiche les indicateurs des deux comptabilités. Importé par son épreuve,
  `tests/EPREUVES_DES_INDICATEURS_Sam_14-11-2026.py`. Aucun autre programme ne l'appelle encore.
③ ENTRÉE — En ligne de commande, un argument facultatif : la racine du dépôt (« . » par défaut).
④ CONDITIONS D'ENTRÉE — À la racine : `gouvernance/golden_tests_*.json`, le témoin
  `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`, et dans `programmes/` les briques qu'il appelle : le juge
  des stratégies, le module de jugement, le module de statistiques, la mesure de la performance, le module des
  positions, la tenue des positions, le contrat des fichiers.
⑤ SORTIE — Lancé : un code de sortie, 0 si le golden est retrouvé, 1 s'il ne l'est pas, 2 si le calibrage n'a pas pu
  tourner (fichier absent, témoin non conforme). Importé : ce que rendent ses fonctions.
⑥ TRAITEMENT — Voir chaque fonction. Rien ne s'exécute au chargement, sinon la définition des constantes.
⑦ UNITÉ — Euros (`_eur`), pourcents (`_pct`), jours calendaires (`jours_`), nombres d'opérations, et ratios sans
  unité (Kelly, Sortino, Calmar). L'unité voyage dans le nom de chaque case (R-708).
⑧ POURQUOI — A-787 : Jean-Luc, 14-11-2026 à 17h19 : « j'ai peur qu'on ait perdu énormément de travail sur la fiche de
  la stratégie […] le très vieux tableau validé […] win rate, pertes successives, pires creux ». A-788 : sa décision
  du même jour, 17h36-17h39 : « je voudrais les 70-30 dans la fiche parce que […] ça fait partie de l'identité de la
  stratégie. Et puis c'est figé […] je peux voir dans le carnet la réalité », et « Oui » à la liste : opérations et
  opérations par mois, fréquence (un gain tous les X jours), probabilité de gain et sa marge d'incertitude, gain moyen
  par opération et son cas défavorable, gagnante moyenne, perdante moyenne, gain net par an, pire creux en euros et
  temps pour en sortir, plus longue série de pertes, Kelly, Sortino et Calmar (affichés). A-793 : sa décision du
  14-11-2026 à 19h16, « 1 » à « des limites (réussite, creux), puis le meilleur gain par an » : ces limites lisent la
  borne basse de Wilson, le creux « 1 fois sur 20 sur 5 ans » en euros et en un jeton, et le gain net par an au pire,
  qui sont donc calculés ici.
⑨ CE QUI CLOCHE — Consigné, non corrigé (R-752) : voir le ⑨ de chaque fonction, et la note de livraison
  `echanges/A_RELIRE.md`. Le plus lourd : le circuit du soir ne range PAS les signaux par CCI avant `tenir` (il les
  passe dans l'ordre de l'univers) ; rejoué dans cet ordre-là, l'historique donne 44 opérations à 65,9 % et
  +67 688,60 €, pas le golden. R-207bis n'est donc appliquée qu'ici.
⑩ EFFET — Lit des fichiers ; n'écrit aucun fichier ; ne sort pas sur le réseau ; affiche quand il est lancé.
⑪ TERMINAISON — Rend la main ; lancé seul, termine le programme par son code de sortie.

⑫ DÉFINITIONS —
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est passé.
  un jeton : la comptabilité où une seule position est ouverte à la fois par stratégie ; un signal reçu pendant une
    position est ignoré.
  jetons illimités : la comptabilité où tous les signaux sont joués, sans contrainte de capital.
  le golden : `gouvernance/golden_tests_*.json`, chiffres de référence figés le 01-08-2026.
  le creux : la plus grande baisse du cumul des gains nets, d'un sommet au plus bas qui suit, quelle que soit sa durée.
  la borne de Wilson : la borne basse à 95 % de la probabilité de réussite (Brown, Cai & DasGupta, 2001).
"""

import os
import sys
import json
import math
import random
import bisect

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)

# DEUX NOMBRES DE TIRAGES, SÉPARÉS ET NOMMÉS (superviseur R-759 du 14-11-2026, D1) :
# · TIRAGES_DU_GAIN est passé à `MODULE_JUGEMENT.borne_basse_gain`, à la valeur que le juge emploie (2 000) : la borne
#   basse du gain doit rester le même nombre ici et chez le juge ; elle n'est PAS touchée par ce lot ;
# · TIRAGES_DU_SEUIL ne sert qu'au seuil de creux « 1 fois sur 20 » quand son calcul exact n'est pas faisable :
#   à 2 000 tirages, le seuil du golden variait de 19 800 € à 21 600 € selon la graine (relecteur INDIC, D1),
#   autour de la tolérance de 20 000 € décidée en A-796 ; à 200 000, trois graines rendent 21 500 € (superviseur).
TIRAGES_DU_GAIN = 2000
TIRAGES_DU_SEUIL = 200_000
# Le calcul exact du seuil de creux suit la profondeur sous le sommet, au centime ; au-delà de ce nombre d'états
# possibles, il est jugé infaisable et le tirage prend le relais (le barème réel donne des montants presque tous
# distincts, et les états explosent).
ETATS_MAX_DU_CALCUL_EXACT = 20_000
# « 1 fois sur 20 » : la valeur que seuls 5 % des cas dépassent (n°59, n°103, REGISTRE R-505 en direct ② et ③).
UNE_FOIS_SUR_VINGT = 0.95
# « sur 5 ans » : l'horizon commun à toutes les stratégies (n°102).
ANNEES_DU_SEUIL = 5
# Jours calendaires d'une année moyenne, bissextiles comprises ; un mois en est le douzième.
JOURS_PAR_AN = 365.25

_BRIQUES = {}


def charger_les_briques(racine):
    """Charge une fois les programmes du dépôt dont les fonctions sont réutilisées ici, et les rend par leur sigle.

    ① RÔLE — Trouver et charger les briques existantes (juge, module de jugement, statistiques, mesure du soir,
      positions, tenue des positions, contrat) au lieu de recopier leurs calculs (R-708).
    ② CONTEXTE D'APPEL — Toutes les fonctions de ce programme qui appellent une brique, et l'épreuve.
    ③ ENTRÉE — `racine` : la racine du dépôt, celle qui contient `programmes/`.
    ④ CONDITIONS D'ENTRÉE — Chaque brique existe en UN seul exemplaire dans `programmes/`.
    ⑤ SORTIE — UNE valeur : un dictionnaire sigle → module chargé (JS, MJ, MS, MES, MP, TP, C).
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher chaque brique par le début de son nom dans `programmes/` seulement · ② refuser si une
      brique a zéro ou plusieurs exemplaires · ③ la charger par `JUGE_DES_STRATEGIES.charger_module` · ④ garder le
      tout en mémoire, par racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les noms datés (`MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`) changent : on les trouve par le
      début du nom, pas par le nom entier (si je renomme un fichier, ce contrôle ne change pas d'avis). On ne
      cherche que dans `programmes/`, parce que des copies anciennes dorment dans `etudes/` et `archives/`.
    ⑨ CE QUI CLOCHE — Un fichier neuf dont le nom commence comme une brique (par exemple un
      `MODULE_JUGEMENT_V2.py`) ferait refuser le chargement : c'est voulu, mais le message ne le distingue pas d'un
      vrai doublon.
    ⑩ EFFET — LIT et EXÉCUTE le code de chargement des sept programmes ; aucune écriture.
    ⑪ TERMINAISON — Rend la main ; lève `FileNotFoundError` si une brique manque ou est en double.
      [sort: non]
    """
    racine = os.path.realpath(racine)
    if racine in _BRIQUES:
        return _BRIQUES[racine]
    prog = os.path.join(racine, "programmes")
    if prog not in sys.path:
        sys.path.insert(0, prog)
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("JUGE_DES_STRATEGIES", os.path.join(prog, "JUGE_DES_STRATEGIES.py"))
    if _sp is None or not os.path.isfile(os.path.join(prog, "JUGE_DES_STRATEGIES.py")):
        raise FileNotFoundError("programmes/JUGE_DES_STRATEGIES.py introuvable sous %s" % racine)
    JS = sys.modules.get("JUGE_DES_STRATEGIES")
    if JS is None or os.path.realpath(getattr(JS, "__file__", "")) != os.path.join(prog, "JUGE_DES_STRATEGIES.py"):
        JS = _iu.module_from_spec(_sp)
        sys.modules["JUGE_DES_STRATEGIES"] = JS
        _sp.loader.exec_module(JS)
    b = {"JS": JS}
    for sigle, debut in (("MJ", "MODULE_JUGEMENT.py"), ("MS", "MODULE_STATISTIQUES_"),
                         ("MES", "MESURER_LA_PERFORMANCE_"), ("MP", "MODULE_POSITIONS.py"),
                         ("TP", "TENIR_LES_POSITIONS.py"), ("C", "CONTRATS_DES_FICHIERS.py")):
        chemins = [p for p in JS.trouver_tous(prog, debut) if os.path.dirname(p) == prog and p.endswith(".py")]
        if len(chemins) != 1:
            raise FileNotFoundError("brique %s : %d exemplaire(s) dans programmes/ (%s) — un seul est attendu"
                                    % (debut, len(chemins), ", ".join(os.path.basename(c) for c in chemins)))
        nom = os.path.splitext(os.path.basename(chemins[0]))[0]
        if sigle in ("MP", "C"):
            # le module des positions et le contrat sont importés par leur nom fixe dans tout le circuit : on prend
            # le même objet, pour que `tenir` et ce programme voient le même barème en mémoire
            b[sigle] = sys.modules.get(nom) or JS.charger_module(chemins[0], nom)
            sys.modules.setdefault(nom, b[sigle])
        else:
            b[sigle] = JS.charger_module(chemins[0], "indic_" + sigle)
    _BRIQUES[racine] = b
    return b


def rejouer_les_signaux(racine, cours, signaux, reglages, bareme, fin, recu=None):
    """Repasse l'historique des signaux, soir après soir, dans la tenue des positions du circuit.

    ① RÔLE — Produire les opérations « un jeton » ET « jetons illimités » d'une stratégie sur le passé, par les
      fonctions mêmes qui tiennent les positions chaque soir — sans réécrire la comptabilité.
    ② CONTEXTE D'APPEL — `calibrer_sur_le_golden`, et l'épreuve. Demain : le juge, pour les blocs 70 % et 30 %.
    ③ ENTRÉE — `racine` : la racine du dépôt · `cours` : les séries par valeur, comme les rend
      `JUGE_DES_STRATEGIES.charger_cours` · `signaux` : la liste des signaux, chacun avec `strategie`, `valeur`,
      `date_signal` et `cci` · `reglages` : identifiant de stratégie → objectif, stop et horizon, au format de
      `TENIR_LES_POSITIONS.reglages_du_registre` · `bareme` : le nom d'un barème de `donnees/BAREME_FRAIS.csv` ·
      `fin` : la dernière séance jouée, AAAA-MM-JJ · `recu` : le reçu d'inscription au registre des essais, exigé
      si la période touche la fenêtre du regard unique (R-505 ③), `None` sinon.
    ④ CONDITIONS D'ENTRÉE — Les noms de valeurs des signaux se rapprochent de ceux des cours par
      `JUGE_DES_STRATEGIES.cle_valeur`. Chaque signal porte un CCI fini : sans lui, `tenir` refuse (A-839).
    ⑤ SORTIE — DEUX valeurs : les lignes de journal écrites par `cloturer` (les deux comptabilités, chacune avec son
      prix réel et son prix de convention), et la liste des incidents, positions restées ouvertes en fin comprises.
      [rend: 2]
    ⑥ TRAITEMENT — ① refuser une période qui touche la fenêtre du regard unique sans reçu, par la garde du juge ·
      ② fabriquer le calendrier des séances jusqu'à `fin` · ③ pour chaque séance S : couper les cours à S (rien du
      lendemain n'est visible), passer les signaux de S TELS QUELS à `TENIR_LES_POSITIONS.tenir` avec la séance
      suivante — c'est `tenir` qui les départage par `departager_r207bis` (R-207bis vit à UN seul endroit, A-839) ·
      ④ recueillir trades et incidents · ⑤ dire les positions encore ouvertes à la fin.
    ⑦ UNITÉ — Les montants du journal sont en euros ; les dates en AAAA-MM-JJ ; une séance est un jour de bourse.
    ⑧ POURQUOI — L'analyse d'impact du 14-11-2026 (A5, « le trou le plus grave ») : le juge ne joue que les jetons
      illimités, et le collège qui a reconstruit un jeton à la main a trouvé 46 opérations à 69,6 % au lieu de 44 à
      63,6 %. La comptabilité un jeton existe déjà, chaque soir, dans `TENIR_LES_POSITIONS` ; la rejouer, c'est la
      seule façon que le passé et le direct comptent pareil (R-708). Le calibrage exige d'abord le golden au centime.
    ⑨ CE QUI CLOCHE — ① Le rejeu ne passe pas la lecture unique ni `achat_admis` (la valeur dans le CAC 40 le jour
      de l'achat) : `tenir` est appelé sans `lecture`, comme le golden a été produit. ② Chaque soir recoupe toutes
      les séries : le temps croît comme séances × valeurs (2,6 s pour le golden, non mesuré sur 20 ans). ③ Les
      positions en attente d'entrée à la fin sont dites, pas comptées. ④ `cloturer` écrit les prix à cinq décimales :
      le net de convention peut différer de quelques centimes de « mise × 4 % − frais » (aucun écart sur le golden).
    ⑩ EFFET — Appelle `tenir`, qui n'écrit aucun fichier. Aucune écriture ici.
    ⑪ TERMINAISON — Rend la main ; lève `RegardNonInscrit` (garde du juge) et laisse remonter
      `TENIR_LES_POSITIONS.DepartageImpossible` quand un signal du jour arrive sans CCI : refus bruyant, jamais
      de rangement alphabétique en silence (décision de Jean-Luc A-839, 16-11-2026 à 07h56, « 1 »).
      [sort: non]
    """
    b = charger_les_briques(racine)
    JS, TP, MP = b["JS"], b["TP"], b["MP"]
    toutes = sorted({x["date"] for s in cours.values() for x in s if x["date"] <= fin})
    if not toutes:
        return [], ["aucune séance avant le %s : rien n'est rejoué" % fin]
    JS._garde_du_regard_unique(None, toutes[0], toutes[-1], (toutes[0], toutes[-1]), recu,
                               nom_du_module=None)
    dates_par_valeur = {k: [x["date"] for x in s] for k, s in cours.items()}
    par_jour = {}
    for s in signaux:
        par_jour.setdefault(s["date_signal"], []).append(s)
    positions, trades, incidents = [], [], []
    for i, d in enumerate(toutes):
        coupes = {k: s[:bisect.bisect_right(dates_par_valeur[k], d)] for k, s in cours.items()}
        du_jour = list(par_jour.get(d, []))  # départage R-207bis : dans `tenir` seul (A-839)
        suivante = toutes[i + 1] if i + 1 < len(toutes) else ""
        r = TP.tenir(positions, coupes, du_jour, suivante, MP, cle=JS.cle_valeur, reglages=reglages,
                     base=racine, bareme=bareme)
        positions = r["positions"]
        trades += r["trades"]
        incidents += ["%s : %s" % (d, x) for x in r["incidents"]]
    for p in positions:
        incidents.append("fin du rejeu (%s) : position %s %s %s encore %s" % (
            fin, p.get("comptabilite"), p.get("valeur"), p.get("date_signal"), p.get("statut")))
    return trades, incidents


def operations_du_journal(trades, comptabilite, prix):
    """Traduit les lignes de journal d'une comptabilité en opérations, la forme que lisent les indicateurs.

    ① RÔLE — Passer du format du journal des trades (contrat TRADE) au format des opérations du juge.
    ② CONTEXTE D'APPEL — `calibrer_sur_le_golden`, et l'épreuve.
    ③ ENTRÉE — `trades` : les lignes rendues par `rejouer_les_signaux` · `comptabilite` : « un_jeton » ou
      « jetons_illimites » · `prix` : « convention » (le prix théorique de l'objectif ou du stop, celui du golden)
      ou « reel » (le prix de sortie effectif, sauts d'ouverture compris).
    ④ CONDITIONS D'ENTRÉE — Les lignes portent les colonnes du contrat TRADE.
    ⑤ SORTIE — UNE valeur : la liste des opérations, chacune avec `valeur`, `date_signal`, `date_entree`,
      `date_sortie`, `motif` et `net` (euros), rangée par date de sortie puis d'entrée puis valeur.
      [rend: 1]
    ⑥ TRAITEMENT — ① garder la comptabilité demandée · ② lire le gain net du prix demandé · ③ ranger.
    ⑦ UNITÉ — `net` en euros, frais compris.
    ⑧ POURQUOI — Les fonctions du juge (`plus_longue_serie_de_pertes`, `borne_basse_gain`) lisent `net` et
      `date_signal` ; le journal écrit `pnl_net_eur`. La traduction se fait ici, une fois.
    ⑨ CE QUI CLOCHE — Le journal n'a pas de colonne `date_signal` : elle est reprise de l'explication si elle y est,
      sinon elle vaut la date d'entrée — l'ordre des opérations reste juste, la date n'est pas celle du signal.
      Les champs des opérations ne sont pas déclarés au contrat des fichiers (étape L9 du planning).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` si `prix` ou `comptabilite` est inconnu.
      [sort: non]
    """
    if prix not in ("convention", "reel"):
        raise ValueError("prix %r : « convention » ou « reel » attendu" % (prix,))
    if comptabilite not in ("un_jeton", "jetons_illimites"):
        raise ValueError("comptabilité %r inconnue" % (comptabilite,))
    col = "pnl_net_convention_eur" if prix == "convention" else "pnl_net_eur"
    ops = []
    for t in trades:
        if t.get("comptabilite") != comptabilite:
            continue
        ops.append({"valeur": t["valeur"], "date_signal": t.get("date_signal") or t["date_entree"],
                    "date_entree": t["date_entree"], "date_sortie": t["date_sortie"],
                    "motif": t.get("motif_sortie", ""), "net": float(t[col])})
    return sorted(ops, key=lambda o: (o["date_sortie"], o["date_entree"], o["valeur"]))


def annees_de_la_periode(periode):
    """Rend la durée d'une période déclarée, en années de 365,25 jours calendaires.

    ① RÔLE — Donner le dénominateur commun des indicateurs « par an » et « par mois ».
    ② CONTEXTE D'APPEL — `operations_par_mois`, `jours_entre_deux_gains`, `mesurer_les_indicateurs`.
    ③ ENTRÉE — `periode` : un couple (début, fin) de dates AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — La fin n'est pas antérieure au début.
    ⑤ SORTIE — UNE valeur : un nombre d'années, à virgule ; 0 quand début = fin.
      [rend: 1]
    ⑥ TRAITEMENT — (fin − début) en jours calendaires, divisé par 365,25.
    ⑦ UNITÉ — Années.
    ⑧ POURQUOI — La période est celle qui a été DÉCLARÉE (R-505 ①), jamais celle des opérations : une stratégie qui
      ne trade pas pendant un an doit le payer dans sa fréquence. Golden : 2024-01-02 → 2026-07-10, 920 jours,
      2,519 ans. UNE PÉRIODE DE 0 JOUR REND 0 au lieu de lever (relecteur INDIC, D4 : le premier soir du carnet
      plantait) ; c'est `mesurer_les_indicateurs` qui le dit en clair. Le compte des jours ne change pas
      (superviseur R-759, D4 réduit : passer aux bornes comprises changerait tous les chiffres annualisés, c'est une
      décision de Jean-Luc).
    ⑨ CE QUI CLOCHE — Le jour de fin n'est pas compté (920 jours et non 921) : convention choisie, non décidée. Une
      période de 0 jour rend 0 : tout appelant qui divise par ce nombre doit le tester (`operations_par_mois` et
      `jours_entre_deux_gains` rendent alors `None`).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` si la période est à l'envers.
      [sort: non]
    """
    from datetime import date
    d0, d1 = (date.fromisoformat(str(x)) for x in periode)
    if d1 < d0:
        raise ValueError("période %r à l'envers" % (periode,))
    return (d1 - d0).days / JOURS_PAR_AN


def operations_par_mois(n, periode):
    """Rend le nombre moyen d'opérations par mois sur la période déclarée.

    ① RÔLE — L'indicateur « opérations par mois » d'A-788 (le « Trades/mois » du tableau du 14-04-2026).
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `n` : le nombre d'opérations · `periode` : le couple (début, fin) déclaré.
    ④ CONDITIONS D'ENTRÉE — Celles de `annees_de_la_periode`.
    ⑤ SORTIE — UNE valeur : un nombre à virgule, ou `None` sur une période de 0 jour.
      [rend: 1]
    ⑥ TRAITEMENT — n ÷ (années × 12).
    ⑦ UNITÉ — Opérations par mois (un mois = un douzième de 365,25 jours).
    ⑧ POURQUOI — A-788 le nomme ; il manquait partout (analyse d'impact, §1b n°2).
    ⑨ CE QUI CLOCHE — Sur une période courte, le chiffre extrapolé n'a pas de sens ; aucun minimum n'est posé
      (décision de Jean-Luc, question de la note).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    annees = annees_de_la_periode(periode)
    return n / (annees * 12.0) if annees else None


def jours_entre_deux_gains(gagnantes, periode):
    """Rend la fréquence des gains : « un gain tous les X jours calendaires ».

    ① RÔLE — L'indicateur « fréquence » d'A-788.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `gagnantes` : le nombre d'opérations gagnantes · `periode` : le couple (début, fin) déclaré.
    ④ CONDITIONS D'ENTRÉE — Celles de `annees_de_la_periode`.
    ⑤ SORTIE — UNE valeur : un nombre de jours, ou `None` s'il n'y a aucun gain ou si la période dure 0 jour.
      [rend: 1]
    ⑥ TRAITEMENT — jours calendaires de la période ÷ nombre de gains.
    ⑦ UNITÉ — Jours calendaires.
    ⑧ POURQUOI — Jean-Luc, 14-11-2026 à 19h04 : « le temps le plus court entre les gains ». Définition du rapport
      CHOIX_MULTICRITERE §5 : « jours calendaires ÷ nombre de gains » ; c'est le chiffre « l'une gagne tous les
      3 jours, l'autre tous les 200 jours » qu'aucun programme ne calculait (rapport PERFORMANCE, n°6).
    ⑨ CE QUI CLOCHE — C'est une MOYENNE : deux gains le même jour puis six mois sans gain donnent le même chiffre
      que des gains réguliers. La durée sous l'eau (`episodes_sous_l_eau`) dit l'autre face.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    annees = annees_de_la_periode(periode)
    if not gagnantes or not annees:
        return None
    return annees * JOURS_PAR_AN / gagnantes


def taux_et_wilson(nets, racine):
    """Rend la probabilité de réussite et sa borne basse de Wilson à 95 %, par `MODULE_JUGEMENT.wilson_bas`.

    ① RÔLE — L'indicateur « probabilité de gain et sa marge d'incertitude » d'A-788, et la limite ① d'A-793.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `nets` : les gains nets des opérations, en euros · `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le taux de réussite et sa borne basse, en pourcents ; `None` et `None` sans opération.
      [rend: 2]
    ⑥ TRAITEMENT — ① compter les gagnantes (gain net strictement positif) · ② taux EXACT = 100 × gagnantes ÷ n ·
      ③ borne = `wilson_bas(n, taux exact)`.
    ⑦ UNITÉ — Pourcents.
    ⑧ POURQUOI — Deux formules existent : `MODULE_JUGEMENT.wilson_bas` (le juge) et
      `MESURER_LA_PERFORMANCE.wilson_borne_basse` (le carnet). Gardée : celle du juge, qui rend une borne dès une
      opération ; celle du carnet rend `None` sous 10 opérations (sa case est vide sur les 4 dernières lignes du
      carnet). Sur le golden, avec le taux exact, les deux donnent le même nombre au millionième (épreuve). Le taux
      est passé EXACT, jamais arrondi : un taux arrondi à 0,1 déplace la borne.
    ⑨ CE QUI CLOCHE — Une opération à 0,00 € compte perdante, comme dans `stats` et `plus_longue_serie_de_pertes`.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not nets:
        return None, None
    MJ = charger_les_briques(racine)["MJ"]
    taux = 100.0 * sum(1 for x in nets if x > 0) / len(nets)
    return taux, MJ.wilson_bas(len(nets), taux)


def moyennes_gagnante_perdante(nets):
    """Rend le gain moyen d'une opération gagnante et la perte moyenne d'une opération perdante.

    ① RÔLE — Les indicateurs « gagnante moyenne » et « perdante moyenne » d'A-788 (« Gain victoire / Perte défaite »
      du tableau du 14-04-2026).
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs` et `kelly`.
    ③ ENTRÉE — `nets` : les gains nets des opérations, en euros.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la gagnante moyenne (positive) et la perdante moyenne (négative ou nulle), en euros ;
      `None` à la place de celle qui n'a aucune opération.
      [rend: 2]
    ⑥ TRAITEMENT — moyenne des nets > 0 ; moyenne des nets ≤ 0.
    ⑦ UNITÉ — Euros par opération.
    ⑧ POURQUOI — Ces deux moyennes étaient calculées DANS `JUGER_UNE_FICHE._kelly`, puis jetées (analyse
      d'impact, §1b n°6). Elles sortent ici en fonction ; `_kelly` devra l'appeler au branchement (R-708).
    ⑨ CE QUI CLOCHE — `_kelly` garde aujourd'hui son propre calcul : deux exemplaires tant que le branchement n'est
      pas fait. La perdante moyenne est rendue avec son signe, alors que `_kelly` la manipule en valeur absolue.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    g = [x for x in nets if x > 0]
    p = [x for x in nets if x <= 0]
    return (sum(g) / len(g) if g else None), (sum(p) / len(p) if p else None)


def creux_du_compte(ops, racine):
    """Rend le pire creux du compte en euros, par `MESURER_LA_PERFORMANCE.pire_chute`, dans l'ordre des sorties.

    ① RÔLE — L'indicateur « pire creux en euros » d'A-788.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `ops` : les opérations, avec `date_sortie`, `date_entree`, `valeur` et `net` · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le pire creux en euros, positif, 0 sans baisse.
      [rend: 1]
    ⑥ TRAITEMENT — ① ranger par (date de sortie, date d'entrée, valeur) : le cumul ne bouge qu'à la clôture ·
      ② rendre la baisse la plus forte que mesure `pire_chute`.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — TROIS calculs du creux existent : `pire_chute` (mesure du soir), `calculer_time_underwater`
      (appelé par le juge sur les dates de SIGNAL), `_series_du_journal` (radar, dates de sortie). Gardé :
      `pire_chute`, qui garde les centimes, est déjà celui du carnet, et porte la définition décidée (A-793, rapport
      CHOIX §1 : « cumul relevé à la sortie de chaque opération (comme `pire_chute`) »). Sur le golden, les trois
      rendent le même montant quand ils lisent les opérations dans l'ordre des sorties.
    ⑨ CE QUI CLOCHE — Plusieurs sorties le même jour sont rangées par (entrée, valeur) : l'ordre peut creuser un
      creux de quelques euros à l'intérieur d'une journée ; `episodes_sous_l_eau`, qui agrège par jour, ne le voit
      pas (aucun écart sur le golden).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not ops:
        return 0.0
    rangees = sorted(ops, key=lambda o: (o["date_sortie"], o["date_entree"], o["valeur"]))
    return 0.0 - charger_les_briques(racine)["MES"].pire_chute([o["net"] for o in rangees])[1] + 0.0


def episodes_sous_l_eau(ops, periode):
    """Rend les épisodes passés sous le meilleur niveau du compte, et les DEUX durées décidées par Jean-Luc (A-798).

    ① RÔLE — L'indicateur « temps pour sortir du creux » d'A-788, écrit UNE fois : la plus longue durée d'un creux
      RATTRAPÉ, et le creux EN COURS avec « non sorti » et ses jours à ce jour ; les deux, aucun par défaut.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs` ; l'épreuve. Demain (BACKLOG, au branchement) : le juge
      (`JUGE_DES_STRATEGIES.py` l.3865, critère C4b) et `JUGER_SUR_8_CRITERES.py` (l.981), qui appellent aujourd'hui
      `MODULE_STATISTIQUES.calculer_time_underwater`.
    ③ ENTRÉE — `ops` : les opérations, avec `date_sortie` et `net` · `periode` : le couple (début, fin) déclaré.
    ④ CONDITIONS D'ENTRÉE — Toute sortie tombe dans la période.
    ⑤ SORTIE — UNE valeur : un dictionnaire — `episodes` (liste : date du sommet, sommet en euros, profondeur en euros,
      date de sortie ou `None`, jours, sorti oui/non) ; `jours_plus_long_creux_rattrape` (`None` si aucun creux n'a
      été rattrapé) ; `creux_en_cours_sorti` (faux si le compte est sous son meilleur niveau à la fin de la période,
      vrai sinon), `jours_du_creux_en_cours` et `creux_en_cours_eur` (`None` s'il n'y a pas de creux en cours).
      [rend: 1]
    ⑥ TRAITEMENT — ① le cumul part de 0 au DÉBUT de la période, qui est le premier sommet · ② on additionne les gains
      nets PAR JOUR DE SORTIE, en NOMBRES EXACTS : chaque gain est lu par l'écriture décimale de son nombre, sans
      arrondi au centime, et le cumul n'arrondit rien (l'ordre des sorties d'un même jour ne compte plus ; un retour
      exact au sommet reste exact ; un compte à 0,0047 € sous son sommet reste sous l'eau) · ③ un épisode commence quand le
      cumul passe sous le sommet ; sa profondeur est la plus grande baisse sous ce sommet · ④ il finit le premier
      jour où le cumul DÉPASSE strictement le sommet (un retour exact au sommet n'est pas une sortie) ; sa durée va
      du jour du sommet à ce jour-là · ⑤ un épisode encore ouvert à la fin est le creux EN COURS : ses jours vont du
      sommet au dernier jour de la période, marqué « non sorti » · ⑥ plus longue durée = le maximum des épisodes
      rattrapés seulement.
    ⑦ UNITÉ — Jours calendaires ; euros.
    ⑧ POURQUOI — DÉCISION de Jean-Luc, A-798, 14-11-2026 à 20h22, réponse « 3 » : afficher les deux chiffres, d'abord
      « la plus longue durée passée sous le meilleur niveau, en ne comptant que les creux rattrapés » (golden un
      jeton : 93 j), ensuite « le creux en cours, avec "non sorti" et le nombre de jours à ce jour » (65 j au
      10-07-2026) ; aucun n'est choisi par défaut. Le chiffre d'avant (62 j, `calculer_time_underwater`) s'arrêtait à
      la dernière opération encore sous l'eau et faisait partir une baisse de la première perte : 0 j avec une seule
      perte (relecteur INDIC, D2). Le superviseur R-759 (14-11-2026, D2) : l'écrire UNE fois ; A-793 range cette
      durée parmi les « affichés seulement ».
    ⑨ CE QUI CLOCHE — Tant que le juge et `JUGER_SUR_8_CRITERES` appellent `calculer_time_underwater`, deux mesures
      de la durée coexistent (R-708) : la migration est au BACKLOG, avec son effet sur le critère C4b à mesurer ;
      l'épreuve confronte les deux sur la profondeur, où elles doivent concorder. La profondeur est lue par jour :
      une baisse à l'intérieur d'une journée n'est pas vue (voir `creux_du_compte`).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` si la période est à l'envers, ou si un gain n'est pas un
      nombre fini (`NaN`, infini : refusés par `Fraction`, ce qui est voulu — Cowork, D3, 15-11-2026).
      [sort: non]
    """
    from datetime import date
    d0, d1 = str(periode[0]), str(periode[1])
    if d1 < d0:
        raise ValueError("période %r à l'envers" % (periode,))
    jours = lambda a, b: (date.fromisoformat(b) - date.fromisoformat(a)).days
    # EN NOMBRES EXACTS (relecteur INDIC tour 2, N1 ; Cowork, C1, 14-11-2026 à 21h56). En flottants, un retour EXACT au
    # sommet tombait une fois sur deux au-dessus par erreur d'arrondi (148,63 − 4 683,56 + 4 683,56). Arrondir chaque
    # gain au centime avant de l'additionner ne suffisait pas : les demi-centimes s'additionnent, et le juge, appelant
    # prévu au branchement, passe des gains NON arrondis (`JUGE_DES_STRATEGIES.py` l.3263, `"net": q * (px - pe) - f_tot`) ;
    # le journal, lui, les écrit au centime (`TENIR_LES_POSITIONS.py` l.1204, `"%.2f"`), et le rejeu de ce programme
    # ne voit donc que des centimes (Cowork, E2, 15-11-2026). Chaque gain est lu par l'écriture DÉCIMALE de son nombre
    # (`Fraction(repr(net))`, 148,63 vaut exactement 14 863/100 ; et non `Fraction(net)`, la valeur binaire, où
    # 0,1 + 0,2 dépasse 0,3) et le cumul est exact. Avec les gains bruités du juge (3 294,0000000000036), « exact »
    # veut dire exact sur le nombre reçu, bruit compris.
    from fractions import Fraction
    par_jour = {}
    for o in ops:
        par_jour[o["date_sortie"]] = par_jour.get(o["date_sortie"], Fraction(0)) + Fraction(repr(float(o["net"])))
    cumul, sommet, jour_sommet, ouvert, episodes = Fraction(0), Fraction(0), d0, None, []
    for d in sorted(par_jour):
        cumul += par_jour[d]
        if cumul > sommet:
            if ouvert is not None:
                ouvert.update(sortie=d, jours=jours(ouvert["date_sommet"], d), sorti=True)
                episodes.append(ouvert)
                ouvert = None
            sommet, jour_sommet = cumul, d
        elif cumul < sommet:
            if ouvert is None:
                ouvert = {"date_sommet": jour_sommet, "sommet_eur": sommet, "profondeur_eur": Fraction(0)}
            ouvert["profondeur_eur"] = max(ouvert["profondeur_eur"], sommet - cumul)
    if ouvert is not None:
        ouvert.update(sortie=None, jours=jours(ouvert["date_sommet"], d1), sorti=False)
        episodes.append(ouvert)
    for e in episodes:
        e["sommet_eur"], e["profondeur_eur"] = float(e["sommet_eur"]), float(e["profondeur_eur"])
    rattrapes = [e["jours"] for e in episodes if e["sorti"]]
    en_cours = episodes[-1] if episodes and not episodes[-1]["sorti"] else None
    return {"episodes": episodes,
            "jours_plus_long_creux_rattrape": max(rattrapes) if rattrapes else None,
            "creux_en_cours_sorti": en_cours is None,
            "jours_du_creux_en_cours": en_cours["jours"] if en_cours else None,
            "creux_en_cours_eur": en_cours["profondeur_eur"] if en_cours else None}


def loi_de_la_plus_longue_serie(part_des_pertes, n):
    """Rend, exactement, la plus longue série de pertes que n opérations ne dépassent qu'une fois sur vingt.

    ① RÔLE — Le seuil de série « 1 fois sur 20 » (alarme n°103), calculé sans aucun tirage.
    ② CONTEXTE D'APPEL — `seuils_1_sur_20_sur_5_ans`.
    ③ ENTRÉE — `part_des_pertes` : la part des opérations perdantes (gain net ≤ 0), entre 0 et 1 · `n` : le nombre
      d'opérations de la période visée (cinq ans).
    ④ CONDITIONS D'ENTRÉE — n ≥ 1.
    ⑤ SORTIE — DEUX valeurs : la plus petite longueur k telle que P(plus longue série ≤ k) ≥ 95 %, et cette
      probabilité.
      [rend: 2]
    ⑥ TRAITEMENT — Pour k = 0, 1, … : suivre opération par opération la loi de la série EN COURS (0 à k pertes
      d'affilée) ; une perte l'allonge, un gain la remet à 0, une série qui dépasse k sort du compte ; la masse qui
      reste après n opérations est P(plus longue série ≤ k) ; s'arrêter au premier k qui atteint 95 %.
    ⑦ UNITÉ — Nombre d'opérations perdantes d'affilée ; probabilité entre 0 et 1.
    ⑧ POURQUOI — La plus longue série ne dépend que de la part des pertes, quel que soit le barème : sa loi se
      calcule exactement (superviseur R-759 du 14-11-2026, D1 ① : « le tirage est inutile »). Golden un jeton,
      q = 16/44, n = 87 : 6, P(≤ 6) = 0,9571 — la valeur trouvée par le relecteur et par le superviseur, chacun de
      son côté. Les opérations sont supposées indépendantes, comme dans le tirage simple.
    ⑨ CE QUI CLOCHE — L'hypothèse d'indépendance (n°107 : tirages par groupes si dépendance) n'est pas levée ; ce
      choix revient à Jean-Luc (question de la note).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; au plus n + 1 valeurs de k, chacune en n × (k + 1) pas.
      [sort: non]
    """
    q = float(part_des_pertes)
    for k in range(0, n + 1):
        loi = [1.0] + [0.0] * k
        for _ in range(n):
            neuve = [0.0] * (k + 1)
            neuve[0] = sum(loi) * (1.0 - q)
            for r in range(k):
                neuve[r + 1] += loi[r] * q
            loi = neuve
        if sum(loi) >= UNE_FOIS_SUR_VINGT:
            return k, sum(loi)
    return n, 1.0


def creux_exact_1_sur_20(nets, n, etats_max=ETATS_MAX_DU_CALCUL_EXACT):
    """Rend, exactement, le creux que n opérations tirées des gains observés ne dépassent qu'une fois sur vingt.

    ① RÔLE — L'oracle exact (chaîne de Markov sur la profondeur sous le sommet) du seuil de creux, quand il est
      faisable.
    ② CONTEXTE D'APPEL — `seuils_1_sur_20_sur_5_ans`.
    ③ ENTRÉE — `nets` : les gains nets observés, en euros (chacun a la même chance d'être tiré) · `n` : le nombre
      d'opérations de cinq ans · `etats_max` : le nombre d'états au-delà duquel le calcul est abandonné.
    ④ CONDITIONS D'ENTRÉE — Au moins un gain net ; n ≥ 1.
    ⑤ SORTIE — UNE valeur : le seuil en euros, ou `None` si le nombre d'états dépasse `etats_max`.
      [rend: 1]
    ⑥ TRAITEMENT — ① passer en centimes entiers · ② profondeur sous le sommet après une opération = max(0,
      profondeur − gain) ; relever toutes les profondeurs atteignables en n opérations, abandonner au-delà de
      `etats_max` · ③ pour une valeur v, P(pire creux ≤ v) = la masse qui ne dépasse jamais v en n opérations ·
      ④ chercher par dichotomie, parmi les profondeurs atteignables, la plus petite v telle que P ≥ 95 %.
    ⑦ UNITÉ — Euros (calcul en centimes).
    ⑧ POURQUOI — À 2 000 tirages, le seuil du golden dépendait de la graine, de 19 800 € à 21 600 €, autour de la
      tolérance de 20 000 € décidée par Jean-Luc en A-796 (14-11-2026, 19h21, « 1 20 000 euros ») ; la valeur exacte
      est 21 500 € (relecteur INDIC, D1, chaîne de Markov ; confirmée par le superviseur à 200 000 tirages). Le
      superviseur R-759 : calcul exact quand c'est faisable, tirage sinon. Faisable quand les gains prennent peu de
      valeurs (le forfait : +3 700 € / −2 800 €) ; au barème réel, les montants sont presque tous distincts et les
      états explosent.
    ⑨ CE QUI CLOCHE — Même convention que le tirage simple : opérations indépendantes ; profondeur relevée à chaque
      opération, sans la baisse latente pendant une position. CHAQUE GAIN EST ARRONDI AU CENTIME avant le calcul
      (même famille que C1 de Cowork, 14-11-2026, réparé dans `episodes_sous_l_eau`) : sans effet sur le golden, dont
      les gains tombent au centime ; avec des gains à fractions de centime, l'écart peut aller jusqu'à un
      demi-centime par opération tirée (environ 1 € sur 200 opérations, Cowork) ; mesuré sur de vrais gains
      (`--mesurer-l-arrondi` de l'épreuve, 15-11-2026) : sous 2 centimes à n = 5. Non réparé : le calcul n'est faisable qu'à peu de montants distincts, et un passage en fractions
      exactes ferait exploser les états plus tôt.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; le coût croît comme n × états × valeurs distinctes × log(états).
      [sort: non]
    """
    poids = {}
    for x in nets:
        c = int(round(x * 100))
        poids[c] = poids.get(c, 0) + 1
    total = float(len(nets))
    lois = [(c, k / total) for c, k in poids.items()]
    atteintes, courantes = {0}, {0}
    for _ in range(n):
        courantes = {max(0, d - c) for d in courantes for c, _p in lois}
        atteintes |= courantes
        if len(atteintes) > etats_max:
            return None
    candidats = sorted(atteintes)

    def p_sous(v):
        """Rend la probabilité que la profondeur ne dépasse jamais v en n opérations.

        ① RÔLE — Le pas de la dichotomie.
        ② CONTEXTE D'APPEL — `creux_exact_1_sur_20`, une fois par valeur essayée.
        ③ ENTRÉE — `v` : la profondeur limite, en centimes.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la probabilité.
          [rend: 1]
        ⑥ TRAITEMENT — faire avancer la loi de la profondeur n fois ; la masse qui dépasse v sort du compte.
        ⑦ UNITÉ — Probabilité entre 0 et 1.
        ⑧ POURQUOI — Voir la fonction englobante.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        loi = {0: 1.0}
        for _ in range(n):
            neuve = {}
            for d, pd in loi.items():
                for c, pc in lois:
                    e = max(0, d - c)
                    if e <= v:
                        neuve[e] = neuve.get(e, 0.0) + pd * pc
            loi = neuve
        return sum(loi.values())
    bas, haut = 0, len(candidats) - 1
    while bas < haut:
        milieu = (bas + haut) // 2
        if p_sous(candidats[milieu]) >= UNE_FOIS_SUR_VINGT:
            haut = milieu
        else:
            bas = milieu + 1
    return candidats[bas] / 100.0


def seuils_1_sur_20_sur_5_ans(nets, operations_par_an, racine, tirages=TIRAGES_DU_SEUIL, graine=None,
                              etats_max=ETATS_MAX_DU_CALCUL_EXACT):
    """Rend le creux et la série de pertes qu'on ne dépasse qu'une fois sur vingt en cinq ans.

    ① RÔLE — Les seuils « 1 fois sur 20 sur 5 ans » : celui du creux est la limite ② d'A-793 (tolérance de
      20 000 € décidée en A-796) et l'alarme n°59 ; celui de la série de pertes est l'alarme n°103.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `nets` : les gains nets des opérations, en euros · `operations_par_an` : le rythme mesuré sur la
      période déclarée · `racine` : la racine · `tirages` : le nombre de tirages si le calcul exact du creux n'est pas
      faisable, `TIRAGES_DU_SEUIL` par défaut · `graine` : la graine du hasard, celle de `MODULE_JUGEMENT` si `None` ·
      `etats_max` : la limite du calcul exact.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire — `creux_eur`, `creux_marge_basse_eur`, `creux_marge_haute_eur`,
      `creux_methode` (« exacte » ou « tirages »), `tirages` (0 si exacte), `serie`, `serie_probabilite` ; toutes
      les valeurs à `None` sans opération ou si cinq ans ne font pas une opération.
      [rend: 1]
    ⑥ TRAITEMENT — ① N = arrondi(opérations par an × 5) · ② série : `loi_de_la_plus_longue_serie`, exacte · ③ creux :
      `creux_exact_1_sur_20` ; s'il n'est pas faisable, tirer N opérations avec remise, `tirages` fois, pire creux
      de chaque tirage par `pire_chute`, valeur de rang 95 % par `MODULE_JUGEMENT.valeur_au_rang`, et marge à 95 %
      sur ce rang : les rangs T × 0,95 ∓ 1,96 × √(T × 0,95 × 0,05) (loi binomiale approchée par la loi normale).
    ⑦ UNITÉ — Euros ; nombre d'opérations perdantes d'affilée ; probabilité.
    ⑧ POURQUOI — REGISTRE R-505 en direct ② et ③ : seuils calculés par stratégie, « 1 fois sur 20 sur 5 ans », en un
      jeton (n°101), sur 5 ans (n°102). Méthode du rapport CHOIX §1 (tirage avec remise, valeur dépassée par 5 %).
      Superviseur R-759 du 14-11-2026 (D1) : la série se calcule exactement ; le creux exactement quand c'est
      faisable, sinon par un tirage nombreux dont la marge est rendue. Le tirage ne partage PAS son nombre avec
      `borne_basse_gain` (deux constantes nommées).
    ⑨ CE QUI CLOCHE — ① Opérations supposées indépendantes : n°107 (tirage par groupes) attend la décision de
      Jean-Luc ; le relecteur a mesuré 22 400 € par blocs de 3 et 25 200 € par blocs de 5 et de 8. ② Que faire quand
      la tolérance de 20 000 € tombe DANS la marge : question à Jean-Luc, rien n'est décidé ici. ③ 200 000 tirages
      coûtent environ 11 s pour 87 opérations (mesuré par le superviseur) : trop pour un tri sur des milliers de
      versions ; `tirages` est un paramètre. ④ Le rang du tirage (`int(0,95 × T)`) et la définition exacte
      (P ≥ 95 %) peuvent différer d'un cran de 1/T.
    ⑩ EFFET — Aucun (le hasard a sa propre graine, le hasard global n'est pas touché).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    vide = {"creux_eur": None, "creux_marge_basse_eur": None, "creux_marge_haute_eur": None,
            "creux_methode": None, "tirages": 0, "serie": None, "serie_probabilite": None}
    b = charger_les_briques(racine)
    n_cinq_ans = int(round(operations_par_an * ANNEES_DU_SEUIL)) if operations_par_an else 0
    if not nets or n_cinq_ans < 1:
        return vide
    serie, p_serie = loi_de_la_plus_longue_serie(sum(1 for x in nets if x <= 0) / len(nets), n_cinq_ans)
    creux = creux_exact_1_sur_20(nets, n_cinq_ans, etats_max)
    if creux is not None:
        return {"creux_eur": creux, "creux_marge_basse_eur": creux, "creux_marge_haute_eur": creux,
                "creux_methode": "exacte", "tirages": 0, "serie": serie, "serie_probabilite": p_serie}
    r = random.Random(b["MJ"].GRAINE if graine is None else graine)
    tires = []
    for _ in range(tirages):
        ech = [nets[r.randrange(len(nets))] for _ in range(n_cinq_ans)]
        tires.append(round(0.0 - b["MES"].pire_chute(ech)[1] + 0.0, 2))
    tires.sort()
    ecart = 1.96 * math.sqrt(tirages * UNE_FOIS_SUR_VINGT * (1 - UNE_FOIS_SUR_VINGT))
    bas = max(0, int(math.floor(tirages * UNE_FOIS_SUR_VINGT - ecart)))
    haut = min(tirages - 1, int(math.ceil(tirages * UNE_FOIS_SUR_VINGT + ecart)))
    return {"creux_eur": b["MJ"].valeur_au_rang(tires, UNE_FOIS_SUR_VINGT),
            "creux_marge_basse_eur": tires[bas], "creux_marge_haute_eur": tires[haut],
            "creux_methode": "tirages", "tirages": tirages, "serie": serie, "serie_probabilite": p_serie}


def kelly(nets, racine):
    """Rend la fraction de Kelly, par `MODULE_STATISTIQUES.calculer_kelly_fractionnel`, nourrie des vraies moyennes.

    ① RÔLE — L'indicateur « Kelly (affiché) » d'A-788.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `nets` : les gains nets des opérations, en euros · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la fraction de Kelly entière (pas un quart), ou `None` sans gagnante ou sans perdante.
      [rend: 1]
    ⑥ TRAITEMENT — ① gagnante et perdante moyennes par `moyennes_gagnante_perdante` · ② taux exact · ③ appeler
      `calculer_kelly_fractionnel(taux, gagnante, |perdante|, 0, fraction=1)` exactement comme
      `JUGER_UNE_FICHE._kelly` · ④ rendre son `kelly_brut`.
    ⑦ UNITÉ — Fraction du capital, sans unité (0,31 = 31 %).
    ⑧ POURQUOI — Même calcul que la porte (`_kelly`), qui fait le filet de R-505 ⑨ (Kelly ≥ 0,05) : l'épreuve
      exige le même nombre que `_kelly` sur le golden. Affiché seulement : Kelly ne voit pas la fréquence (rapport
      PERFORMANCE §4 point 2).
    ⑨ CE QUI CLOCHE — `calculer_kelly_fractionnel` arrondit à quatre décimales. Les frais sont déjà dans les nets
      (on passe 0) : c'est le choix de `_kelly`, repris.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    gm, pm = moyennes_gagnante_perdante(nets)
    if gm is None or pm is None or pm == 0:
        return None
    MS = charger_les_briques(racine)["MS"]
    taux = 100.0 * sum(1 for x in nets if x > 0) / len(nets)
    r = MS.calculer_kelly_fractionnel(taux, gm, -pm, 0.0, fraction=1.0)
    return None if r.get("erreur") else r["kelly_brut"]


def sortino(nets):
    """Rend le ratio de Sortino par opération, cible zéro.

    ① RÔLE — L'indicateur « Sortino (affiché) » d'A-788.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `nets` : les gains nets des opérations, en euros.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le ratio, ou `None` sans opération ou sans perte.
      [rend: 1]
    ⑥ TRAITEMENT — gain moyen ÷ racine de la moyenne, sur TOUTES les opérations, de min(0, gain)².
    ⑦ UNITÉ — Sans unité, par opération (non annualisé).
    ⑧ POURQUOI — Décidé à afficher le 01-08-2026 (R-502ter), jamais programmé (`grep -i sortino programmes/*.py` ne
      trouvait rien). Définition de Sortino & Price (1994), cible zéro : seules les pertes font le risque. Par
      opération, comme le Sharpe par opération du rapport PERFORMANCE (illustration : 0,64 pour C5 en jetons
      illimités).
    ⑨ CE QUI CLOCHE — Le choix « par opération » plutôt que « quotidien » n'est pas décidé par Jean-Luc (question de
      la note). Non annualisé : il ne se compare pas à un Sortino publié.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not nets:
        return None
    bas = math.sqrt(sum(min(0.0, x) ** 2 for x in nets) / len(nets))
    if bas == 0:
        return None
    return (sum(nets) / len(nets)) / bas


def calmar(gain_net_par_an_eur, pire_creux_eur):
    """Rend le ratio de Calmar : gain net par an divisé par le pire creux.

    ① RÔLE — L'indicateur « Calmar (affiché) » d'A-788.
    ② CONTEXTE D'APPEL — `mesurer_les_indicateurs`.
    ③ ENTRÉE — `gain_net_par_an_eur` : le gain net par an, en euros · `pire_creux_eur` : le pire creux, en euros,
      positif.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le ratio, ou `None` si le creux est nul ou inconnu.
      [rend: 1]
    ⑥ TRAITEMENT — division.
    ⑦ UNITÉ — Par an (euros par an ÷ euros).
    ⑧ POURQUOI — Décidé à afficher le 01-08-2026 (R-502ter), jamais programmé. Terry Young, 1991 : rendement
      annuel ÷ pire creux.
    ⑨ CE QUI CLOCHE — Le creux grandit avec la durée observée (Magdon-Ismail & Atiya) : un Calmar 70 % et un Calmar
      30 % ne se comparent pas sans le dire. Le Calmar d'origine se mesure sur 36 mois ; ici sur la période déclarée.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not pire_creux_eur or gain_net_par_an_eur is None:
        return None
    return gain_net_par_an_eur / pire_creux_eur


def mesurer_les_indicateurs(operations, comptabilite, periode, racine, tirages_du_gain=TIRAGES_DU_GAIN,
                            tirages_du_seuil=TIRAGES_DU_SEUIL, graine=None):
    """Rend TOUS les indicateurs d'A-788 pour une liste d'opérations, une comptabilité et une période déclarée.

    ① RÔLE — Le point d'entrée unique : le juge (blocs 70 % et 30 %) et la mesure du soir (carnet) l'appelleront,
      pour que « mêmes indicateurs » soit vrai par construction.
    ② CONTEXTE D'APPEL — `main` (golden), l'épreuve ; demain le juge, le tri et la mesure du soir.
    ③ ENTRÉE — `operations` : la liste des opérations (`valeur`, `date_signal`, `date_entree`, `date_sortie`, `net`
      en euros) · `comptabilite` : « un_jeton » ou « jetons_illimites » · `periode` : le couple (début, fin)
      DÉCLARÉ · `racine` : la racine · `tirages_du_gain` : tirages de la borne basse du gain, ceux du juge par défaut
      · `tirages_du_seuil` : tirages du seuil de creux quand son calcul exact n'est pas faisable · `graine` : graine
      du hasard, celle de `MODULE_JUGEMENT` si `None`.
    ④ CONDITIONS D'ENTRÉE — Toute opération est sortie dans la période ; en un jeton, aucune opération n'entre
      avant la sortie de la précédente.
    ⑤ SORTIE — UNE valeur : un dictionnaire dont chaque clé porte son unité (`_eur`, `_pct`, `jours_`), listé au ⑥.
      La borne basse du gain vaut `None` sous 5 opérations (règle de `borne_basse_gain`). Sur une période de 0 jour,
      les cases rapportées au temps valent `None` et `motif_periode` le dit.
      [rend: 1]
    ⑥ TRAITEMENT — ① contrôler comptabilité, période et chevauchements · ② `operations` (compte) et
      `operations_par_mois` · ③ `jours_entre_deux_gains` · ④ `taux_reussite_pct` et
      `taux_reussite_borne_basse_pct` · ⑤ `gain_moyen_eur` et `gain_moyen_borne_basse_eur` par
      `MODULE_JUGEMENT.borne_basse_gain` · ⑥ `gagnante_moyenne_eur`, `perdante_moyenne_eur` · ⑦ `gain_net_par_an_eur`
      et `gain_net_par_an_borne_basse_eur` (gain moyen et sa borne × opérations par an) · ⑧ `pire_creux_eur` ·
      ⑨ les deux durées décidées en A-798 (`jours_plus_long_creux_rattrape` ; `creux_en_cours_sorti`,
      `jours_du_creux_en_cours`, `creux_en_cours_eur`), aucune par défaut · ⑩ `plus_longue_serie_de_pertes` par
      `MODULE_JUGEMENT` · ⑪ `creux_1_sur_20_sur_5_ans_eur` avec ses marges et sa méthode,
      `serie_1_sur_20_sur_5_ans` et sa probabilité · ⑫ `kelly`, `sortino`, `calmar` · ⑬ rappels : `comptabilite`,
      `periode`, `annees`, `motif_periode`, `gain_net_total_eur`, `tirages_du_gain`, `graine`.
    ⑦ UNITÉ — Dans le nom de chaque clé ; sans suffixe : un compte, un oui/non ou un ratio sans unité.
    ⑧ POURQUOI — A-788 (Jean-Luc, 14-11-2026, 17h36-17h39) fixe la liste ; A-793 (19h16) en fait lire trois au
      choix entre stratégies : la borne de Wilson (plancher 55 %, A-794), le creux 1 sur 20 sur 5 ans (tolérance
      20 000 €, A-796), le gain net par an au pire. Les deux comptabilités ne s'additionnent jamais (R-604) : on en
      mesure une par appel, et elle est contrôlée. Une période de 0 jour (le premier soir du carnet) ne fait plus
      planter le calcul (relecteur INDIC, D4) ; aucun minimum n'est posé ici, c'est une décision de Jean-Luc.
    ⑨ CE QUI CLOCHE — ① La plus longue série suit l'ordre des SIGNAUX (`plus_longue_serie_de_pertes` range par
      `date_signal`) alors que le creux suit l'ordre des SORTIES : en jetons illimités, 5 contre 4 sur le golden
      (relecteur, D9, question à Jean-Luc). ② Le « cas défavorable » du gain moyen vient de `borne_basse_gain`, dont
      la valeur dépend de la graine (une graine sur dix donne 450 € au lieu de 597,73 €, relecteur) : des trois
      chiffres du choix A-793, celui-ci reste instable ; sa réparation appartient à la branche `v7-bootstrap`
      (A-782/A-783). ③ Une opération appartient à la période par sa seule date de sortie ; la coupure des blocs
      70/30 se règle au branchement (superviseur, D6). ④ Facteur de profit, Sharpe, probabilité d'une année
      perdante ne sont pas repris (hors liste d'A-788).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur une entrée contraire au ④ ; le seuil de creux par tirage
      peut prendre une dizaine de secondes.
      [sort: non]
    """
    b = charger_les_briques(racine)
    if comptabilite not in b["C"].COMPTABILITES:
        raise ValueError("comptabilité %r inconnue (%s)" % (comptabilite, ", ".join(b["C"].COMPTABILITES)))
    d0, d1 = str(periode[0]), str(periode[1])
    annees = annees_de_la_periode((d0, d1))
    hors = [o for o in operations if not (d0 <= o["date_sortie"] <= d1)]
    if hors:
        raise ValueError("%d opération(s) sortie(s) hors de la période %s..%s, dont %s %s"
                         % (len(hors), d0, d1, hors[0]["valeur"], hors[0]["date_sortie"]))
    ops = sorted(operations, key=lambda o: (o["date_sortie"], o["date_entree"], o["valeur"]))
    if comptabilite == b["C"].UN_JETON:
        for a, c in zip(ops, ops[1:]):
            if c["date_entree"] <= a["date_sortie"]:
                raise ValueError("un jeton : %s entre le %s avant la sortie de %s le %s — deux positions à la fois"
                                 % (c["valeur"], c["date_entree"], a["valeur"], a["date_sortie"]))
    nets = [o["net"] for o in ops]
    n = len(nets)
    gagnantes = sum(1 for x in nets if x > 0)
    taux, wilson = taux_et_wilson(nets, racine)
    gm, pm = moyennes_gagnante_perdante(nets)
    _g = b["MJ"].GRAINE if graine is None else graine
    bb = b["MJ"].borne_basse_gain(ops, n_tirages=tirages_du_gain, graine=_g)
    gain_moyen = sum(nets) / n if n else None
    borne_gain = bb.get("borne_basse_5pct")
    par_an = n / annees if annees else None
    motif = "" if annees else ("période de 0 jour (%s..%s) : les cases rapportées au temps (par mois, par an, jours "
                               "entre deux gains, Calmar, seuils sur 5 ans) sont laissées vides" % (d0, d1))
    creux = creux_du_compte(ops, racine)
    eau = episodes_sous_l_eau(ops, (d0, d1))
    seuils = seuils_1_sur_20_sur_5_ans(nets, par_an, racine, tirages_du_seuil, graine)
    gain_an = gain_moyen * par_an if (gain_moyen is not None and par_an is not None) else None
    return {
        "comptabilite": comptabilite, "periode": (d0, d1), "annees": annees, "motif_periode": motif,
        "operations": n,
        "operations_par_mois": operations_par_mois(n, (d0, d1)),
        "jours_entre_deux_gains": jours_entre_deux_gains(gagnantes, (d0, d1)),
        "taux_reussite_pct": taux,
        "taux_reussite_borne_basse_pct": wilson,
        "gain_moyen_eur": gain_moyen,
        "gain_moyen_borne_basse_eur": borne_gain,
        "gagnante_moyenne_eur": gm,
        "perdante_moyenne_eur": pm,
        "gain_net_total_eur": sum(nets),
        "gain_net_par_an_eur": gain_an,
        "gain_net_par_an_borne_basse_eur": borne_gain * par_an if (borne_gain is not None and par_an) else None,
        "pire_creux_eur": creux,
        "jours_plus_long_creux_rattrape": eau["jours_plus_long_creux_rattrape"],
        "creux_en_cours_sorti": eau["creux_en_cours_sorti"],
        "jours_du_creux_en_cours": eau["jours_du_creux_en_cours"],
        "creux_en_cours_eur": eau["creux_en_cours_eur"],
        "plus_longue_serie_de_pertes": b["MJ"].plus_longue_serie_de_pertes(ops),
        "creux_1_sur_20_sur_5_ans_eur": seuils["creux_eur"],
        "creux_1_sur_20_sur_5_ans_marge_basse_eur": seuils["creux_marge_basse_eur"],
        "creux_1_sur_20_sur_5_ans_marge_haute_eur": seuils["creux_marge_haute_eur"],
        "creux_1_sur_20_sur_5_ans_methode": seuils["creux_methode"],
        "serie_1_sur_20_sur_5_ans": seuils["serie"],
        "serie_1_sur_20_sur_5_ans_probabilite": seuils["serie_probabilite"],
        "kelly": kelly(nets, racine),
        "sortino": sortino(nets),
        "calmar": calmar(gain_an, creux),
        "tirages_du_gain": tirages_du_gain, "tirages_du_seuil": seuils["tirages"], "graine": _g,
    }


def comparer_au_producteur_du_golden(racine, cours, fin, rendu):
    """Compare, opération par opération, le rejeu du circuit à `backtest_c5etendu10`, qui a produit le golden.

    ① RÔLE — Le calibrage opération par opération (relecteur INDIC, D3) : les totaux seuls ne distinguent pas
      R-207bis d'un départage alphabétique.
    ② CONTEXTE D'APPEL — `calibrer_sur_le_golden`, une fois.
    ③ ENTRÉE — `racine` : la racine · `cours` : les cours du témoin · `fin` : la dernière séance jouée · `rendu` :
      comptabilité → opérations rejouées.
    ④ CONDITIONS D'ENTRÉE — Le module de calibrage du juge expose `backtest_c5etendu10`.
    ⑤ SORTIE — UNE valeur : un dictionnaire comptabilité → (nombre de différences, première différence ou `None`).
      [rend: 1]
    ⑥ TRAITEMENT — ① lancer `backtest_c5etendu10` sur les cours coupés à `fin`, barème `HIST_FORFAIT_300` ·
      ② « vraie_vie » ↔ un jeton, « qualite_signal » ↔ jetons illimités · ③ comparer, AVEC LEURS EFFECTIFS
      (`Counter`, une opération en double compte deux fois), les opérations (valeur rapprochée par `cle_valeur`,
      date d'entrée, date de sortie, gain net au centime).
    ⑦ UNITÉ — Euros au centime.
    ⑧ POURQUOI — Le backtest du module de C5 est le chemin qui a produit le golden du 01-08-2026, indépendant de
      `tenir` ; il départage déjà par (CCI, valeur). Avec un départage alphabétique, deux opérations changent (VINCI
      → TOTALENERGIES le 2024-06-07, VEOLIA → EIFFAGE le 2024-12-23) sans changer les totaux : seule cette
      comparaison le voit. Écarté : figer la liste dans un fichier témoin (un second exemplaire, R-708).
    ⑨ CE QUI CLOCHE — Le motif de sortie n'est pas comparé (le backtest et `cloturer` ne l'écrivent pas pareil, le
      motif est comparé en total par le golden). Jusqu'au tour 2 du relecteur (N4), la comparaison portait sur des
      ENSEMBLES (une opération en double ne comptait qu'une fois) et sans la date de sortie : réparé.
    ⑩ EFFET — Lance le backtest du module de signal (lecture seule).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    b = charger_les_briques(racine)
    JS = b["JS"]
    sig = JS.signal_de_la_fiche(racine, dict(JS.SIGNAL_DU_CALIBRAGE, id="calibrage"))
    d = {v: [x for x in (cours.get(JS.cle_valeur(v)) or cours.get(v) or []) if x["date"] <= fin]
         for v in getattr(sig.module, "C5E10_UNIVERS", [])}
    r = sig.module.backtest_c5etendu10(d, bareme="HIST_FORFAIT_300")
    from collections import Counter
    ecarts = {}
    for compta, cle in (("un_jeton", "vraie_vie"), ("jetons_illimites", "qualite_signal")):
        attendu = Counter((JS.cle_valeur(t["valeur"]), d[t["valeur"]][t["i_in"]]["date"],
                           d[t["valeur"]][t["i_out"]]["date"], round(t["pnl"], 2)) for t in r[cle]["trades"])
        obtenu = Counter((JS.cle_valeur(o["valeur"]), o["date_entree"], o["date_sortie"], round(o["net"], 2))
                         for o in rendu.get(compta, []))
        diff = sorted(((attendu - obtenu) + (obtenu - attendu)).elements())
        ecarts[compta] = (len(diff), diff[0] if diff else None)
    return ecarts


def calibrer_sur_le_golden(racine):
    """Rejoue l'historique du golden par le circuit et exige ses chiffres au centime, dans les deux comptabilités.

    ① RÔLE — Prouver que le rejeu un jeton compte comme le golden avant qu'un seul indicateur ne soit écrit.
    ② CONTEXTE D'APPEL — `main`, et l'épreuve.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le golden, son témoin conforme (empreinte déclarée), le module de signal qu'il déclare.
    ⑤ SORTIE — TROIS valeurs : vrai si les deux comptabilités sont retrouvées · les lignes à afficher · un
      dictionnaire comptabilité → opérations rejouées (convention, forfait historique), avec la période sous
      « periode ». Le oui-ou-non exige les totaux du golden ET les opérations une à une de
      `comparer_au_producteur_du_golden`.
      [rend: 3]
    ⑥ TRAITEMENT — ① lire le golden et vérifier l'empreinte du témoin · ② charger les cours du témoin par
      `JUGE_DES_STRATEGIES.charger_cours` · ③ détecter les signaux par le module du calibrage du juge
      (`SIGNAL_DU_CALIBRAGE`), sur son univers, jusqu'à la fin déclarée · ④ seuils = `TP_PCT`, `SL_PCT`, `HORIZON` du
      module des positions · ⑤ rejouer au barème `HIST_FORFAIT_300` · ⑥ comparer n, taux arrondi au dixième, net
      au centime et motifs au golden, dans les deux comptabilités · ⑦ comparer les opérations une à une à
      `backtest_c5etendu10` (`comparer_au_producteur_du_golden`).
    ⑦ UNITÉ — Euros au centime ; pourcents au dixième ; comptes exacts.
    ⑧ POURQUOI — R-701 : « reproduire avant de produire ». Le golden du 01-08-2026 a été produit au prix de
      CONVENTION (seuil exact) et au forfait de 300 € par aller-retour (une gagnante +3 700 €, une perdante
      −2 800 €) ; ce barème vit au fichier daté sous le nom `HIST_FORFAIT_300` et `MODULE_POSITIONS` le calibre
      déjà au centime sur Bureau Veritas. La consigne du Chat (14-11-2026) : « Si tu ne le retrouves pas à l'euro
      près, ARRÊT ».
    ⑨ CE QUI CLOCHE — ① Les seuils viennent des constantes du module des positions, que son ⑨ dit écrites en dur ;
      `C5-ETENDU-10` n'a pas de ligne au registre des stratégies (mesuré par le juge le 20-09-2026). ② L'empreinte
      des opérations du golden (`a0e38dd02eaf4ca0`) n'est PAS recalculée : sa recette n'a pas été retrouvée ;
      le calibrage compare à la place, opération par opération, à `backtest_c5etendu10` (et l'épreuve aux 44
      opérations reconstruites par l'étude du 01-11-2026). ③ La fin vaut 2026-07-10 si le golden ne déclare pas `periode_fin`,
      comme dans `JUGE_DES_STRATEGIES.calibrer`.
    ⑩ EFFET — LIT le golden et le témoin ; aucune écriture.
    ⑪ TERMINAISON — Rend la main ; le rejeu dure quelques secondes.
      [sort: non]
    """
    import hashlib
    b = charger_les_briques(racine)
    JS, MP = b["JS"], b["MP"]
    lignes = []
    f_gold = JS.trouver(os.path.join(racine, "gouvernance"), "golden_tests_")
    f_tem = os.path.join(racine, "temoins", "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv")
    if not f_gold or not os.path.isfile(f_tem):
        return False, ["golden ou témoin introuvable : RIEN N'EST CALIBRÉ"], {}
    golden = json.load(open(f_gold, encoding="utf-8"))
    meta = golden.get("meta", {}) or {}
    emp = hashlib.sha256(open(f_tem, "rb").read()).hexdigest()[:16]
    if emp != meta.get("hash_donnees_sha256_16"):
        return False, ["témoin non conforme : empreinte %s, le golden déclare %s" % (
            emp, meta.get("hash_donnees_sha256_16"))], {}
    lignes.append("témoin conforme : %s (%s)" % (os.path.basename(f_tem), emp))
    cours = JS.charger_cours(f_tem)
    fin = meta.get("periode_fin") or "2026-07-10"
    sig = JS.signal_de_la_fiche(racine, dict(JS.SIGNAL_DU_CALIBRAGE, id="calibrage"))
    signaux = []
    for v in getattr(sig.module, "C5E10_UNIVERS", []):
        serie = cours.get(JS.cle_valeur(v)) or cours.get(v) or []
        for s in sig(serie):
            d = serie[s["i"]]["date"]
            if d <= fin:
                signaux.append({"strategie": "CALIBRAGE", "valeur": v, "date_signal": d, "cci": s["cci"]})
    reglages = {"CALIBRAGE": {"tp": MP.TP_PCT, "sl": MP.SL_PCT, "horizon": MP.HORIZON}}
    trades, incidents = rejouer_les_signaux(racine, cours, signaux, reglages, "HIST_FORFAIT_300", fin)
    debut = min(x["date"] for s in cours.values() for x in s)
    lignes.append("%d signaux de %s à %s ; %d incident(s)" % (len(signaux), debut, fin, len(incidents)))
    ok = True
    rendu = {"periode": (debut, fin)}
    for compta in ("un_jeton", "jetons_illimites"):
        ref = (golden.get("C5-ETENDU-10", {}) or {}).get(compta) or {}
        ops = operations_du_journal(trades, compta, "convention")
        rendu[compta] = ops
        n = len(ops)
        net = round(sum(o["net"] for o in ops), 2)
        wr = round(100.0 * sum(1 for o in ops if o["net"] > 0) / n, 1) if n else None
        motifs = {}
        for o in ops:
            m = o["motif"].replace("_GAP", "")
            motifs[m] = motifs.get(m, 0) + 1
        bon = (bool(ref) and n == ref.get("n") and wr == ref.get("wr") and abs(net - float(ref.get("net", 0))) < 0.005
               and motifs == (ref.get("motifs") or {}))
        ok = ok and bon
        lignes.append("%s %s : %d opérations . %.1f %% . %+.2f EUR . motifs %s (golden : %s . %s %% . %s . %s)" % (
            "OK" if bon else "ÉCART", compta, n, wr or 0.0, net, json.dumps(motifs, sort_keys=True),
            ref.get("n"), ref.get("wr"), ref.get("net"), json.dumps(ref.get("motifs"), sort_keys=True)))
    # OPÉRATION PAR OPÉRATION (relecteur INDIC, D3) : les totaux ne distinguent pas R-207bis d'un ordre alphabétique
    for compta, (k, premiere) in sorted(comparer_au_producteur_du_golden(racine, cours, fin, rendu).items()):
        ok = ok and k == 0
        lignes.append("%s %s : opérations une à une contre backtest_c5etendu10 : %d différence(s)%s" % (
            "OK" if k == 0 else "ÉCART", compta, k, "" if premiere is None else ", dont %s" % (premiere,)))
    return ok, lignes, rendu


def main():
    """Calibre sur le golden, puis affiche les indicateurs des deux comptabilités ; rend le code de sortie.

    ① RÔLE — Le lancement à la main : prouver le rejeu, puis montrer la fiche d'indicateurs du golden.
    ② CONTEXTE D'APPEL — Le bas de ce fichier, lancé seul.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Celles de `calibrer_sur_le_golden`.
    ⑤ SORTIE — UNE valeur : le code de sortie, 0 calibré, 1 écart au golden, 2 calibrage impossible.
      [rend: 1]
    ⑥ TRAITEMENT — ① racine = premier argument ou « . » · ② calibrer · ③ si calibré, mesurer et afficher chaque
      comptabilité, une case par ligne.
    ⑦ UNITÉ — Celles des cases.
    ⑧ POURQUOI — Un contrôle qui n'a pas pu tourner rend un code NON NUL (R-734) : 2, distinct de l'écart (1).
    ⑨ CE QUI CLOCHE — Les indicateurs affichés sont ceux des années de RÉGLAGE de C5 : ils ne prouvent rien sur la
      stratégie, ils montrent la forme de la fiche.
    ⑩ EFFET — AFFICHE ; aucune écriture.
    ⑪ TERMINAISON — Rend la main ; c'est le bas du fichier qui en fait un code de sortie.
      [sort: non]
    """
    racine = sys.argv[1] if len(sys.argv) > 1 else "."
    print("MESURER LES INDICATEURS — simulation uniquement, aucun ordre réel")
    try:
        ok, lignes, rendu = calibrer_sur_le_golden(racine)
    except (FileNotFoundError, OSError, ValueError) as e:
        print("  CALIBRAGE IMPOSSIBLE : %s: %s" % (type(e).__name__, e))
        return 2
    for l in lignes:
        print("  " + l)
    if not rendu:
        print("  CALIBRAGE IMPOSSIBLE")
        return 2
    if not ok:
        print("  ARRÊT : le rejeu ne retrouve pas le golden — aucun indicateur n'est rendu.")
        return 1
    print("  -> rejeu calibré sur le golden.")
    for compta in ("un_jeton", "jetons_illimites"):
        ind = mesurer_les_indicateurs(rendu[compta], compta, rendu["periode"], racine)
        print("INDICATEURS %s (période %s..%s, %.3f ans) :" % (compta, ind["periode"][0], ind["periode"][1],
                                                                ind["annees"]))
        for k, v in ind.items():
            if k in ("comptabilite", "periode", "annees"):
                continue
            print("  %-34s %s" % (k, ("%.4f" % v) if isinstance(v, float) else v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
