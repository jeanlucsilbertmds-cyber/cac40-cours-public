#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TENIR LE REGISTRE DES ESSAIS — inscrire chaque essai de stratégie AVANT son calcul, et compter les essais faits.
Simulation uniquement : un essai est un rejeu sur des cours passés ; aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — Plus on essaie de stratégies sur le même passé, plus le hasard fabrique de faux gagnants. La loi
(R-505 ⑤, ⑧) corrige le seuil de preuve par le nombre d'essais ; encore faut-il que chaque essai laisse une trace qu'on
ne puisse ni effacer ni antidater. Ce programme écrit cette trace et la compte. Il repose sur le contrat du registre
des essais (`programmes/CONTRATS_DES_FICHIERS.py`, NATURES_DES_ENTREES_D_ESSAI, fragment du lot L4 du 31-10-2026
« posé tel quel ») : une entrée = un fichier JSON immuable `registre_essais/<16 hex>.json`, nommé par l'empreinte de
ses octets, de nature PREENREGISTREMENT (écrite avant le calcul) ou RESULTAT (écrite après).

① RÔLE — Porter à UN seul endroit l'écriture et la lecture du registre des essais (FICHIERS_A_VENIR du contrat le
  désigne comme son seul écrivain) : `preenregistrer` avant un calcul, `inscrire_le_resultat` après, `lire_le_registre`
  pour contrôler qu'aucune entrée n'a été modifiée, `nombre_d_essais` pour compter les hypothèses distinctes, à un
  commit, par fiche, par famille ou par LIGNÉE ; `lignee_de_la_fiche` pour la lignée (mère, versions, sœurs) ;
  `regards_sur_les_annees` et `premier_regard` pour le regard unique de R-505 ③, compté sur la PORTÉE lue au fichier
  `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv` (`portee_du_regard`) ; `bilan_de_la_fiche` rend tout cela, et k, en
  un seul dictionnaire pour la porte d'entrée du juge.
  CHAQUE LECTURE rend des fiches sous FORME CANONIQUE (l'identifiant tel qu'écrit au registre des stratégies,
  `CONTRATS_DES_FICHIERS.identite_de_la_fiche`) ; un identifiant inconnu est un défaut, jamais une fiche vide. Un
  calibrage est un GENRE d'essai (case `genre_d_essai`), rattaché à sa fiche ; s'il compte comme regard est un réglage
  (`calibrage_compte_comme_regard`, question J3 pour Jean-Luc).
② CONTEXTE D'APPEL — Au 11-11-2026 : les épreuves `tests/EPREUVES_B_DU_BLOC_5A_Mer_11-11-2026.py` et
  `tests/EPREUVES_B2_DU_REGISTRE_DES_ESSAIS_Mer_11-11-2026.py` ; `DECLARER_UNE_STRATEGIE.declaration_engagee`.
  Destiné au juge des stratégies (`jouer`, propriété de l'agent A ; la porte `juger_une_fiche`, agent J) et au
  laboratoire : l'interface est décrite dans `echanges/A_RELIRE_B2.md`. Lancé en ligne de commande : `python3 programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py <racine>
  [--branche origin/main]` contrôle le registre (et son histoire) et affiche le nombre d'essais.
③ ENTRÉE — En ligne de commande : la racine du dépôt, et facultativement la date du compte.
④ CONDITIONS D'ENTRÉE — Python 3.9 au moins (zoneinfo) ; `programmes/CONTRATS_DES_FICHIERS.py` voisin ; git pour un
  compte daté ; `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv` et `donnees/DECLARATIONS_DATEES.csv` pour les regards.
⑤ SORTIE — En ligne de commande : le code 0 si le registre est sain et compté, 1 s'il porte un défaut, 2 si le compte
  n'a pas pu se faire (R-734 : un contrôle qui n'a pas pu tourner rend un code non nul).
⑥ TRAITEMENT — Définir les fonctions ; en ligne de commande, `main`.
⑦ UNITÉ — Des ESSAIS, comptés en hypothèses distinctes (empreinte de l'hypothèse) ; des dates en heure de Paris.
⑧ POURQUOI — A-226 (16-08-2026) : « même une expérience sans résultat est enregistrée ». Le lot L4 (31-10-2026) avait
  écrit un moteur complet sur une copie, jamais fusionné ; le contrat, lui, a été posé au dépôt. Ce programme en est
  l'écrivain minimal, qui tient les trois propriétés dont le compte dépend : une entrée ne se réécrit pas (création
  exclusive), une entrée modifiée se voit (son nom est l'empreinte de ses octets), une entrée ne s'antidate pas (le
  compte à un point lit l'ORDRE de l'histoire de la branche principale, jamais une date — ni celle écrite dans
  l'entrée, que le contrat dit « n'ordonne rien », ni celle d'un commit, qu'un rebase change), et un effacement commis
  se voit (`historique_en_ajout_seul`). Périmètre : l'erreur d'un agent, pas un faussaire (hypothèse du superviseur
  R-759 du 11-11-2026, à confirmer par Jean-Luc). LA PORTÉE DU REGARD est un RÉGLAGE lu dans un fichier : la lecture
  « par lignée déclarée » est celle du superviseur R-759 du 11-11-2026 à 22h19 (n°46, n°61), À CONFIRMER PAR
  JEAN-LUC ; elle se change sans toucher au code.
⑨ CE QUI CLOCHE — ① Depuis la mission REGARD (12-11-2026), le registre vit sur la branche des regards : une entrée
  effacée par un commit en avance rapide reste COMPTÉE (union des ajouts) et `historique_en_ajout_seul` le signale ;
  la réécriture forcée et la suppression de branche ne sont signalées qu'AU MIEUX, SANS GARANTIE (forçage, suppression : voies de faussaire, hors J1 ; la règle GitHub J2 est impossible sur le dépôt privé avec l'abonnement actuel, 403 mesuré par le superviseur REGARD, M2). LIMITE J1 :
  le registre protège de l'ERREUR d'agent, pas d'un agent qui tricherait (décidée par Jean-Luc le 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708). `premier_regard` lit la branche des
  regards ; l'ancre de la déclaration est le `sommet_principal` qu'inscrit chaque préenregistrement (décision de
  Jean-Luc du 12-11-2026 à 09h04, « Reparer »). `nombre_d_essais(commit=…)` lit encore le registre sur la branche
  PRINCIPALE, où plus rien ne s'inscrit. ② Aucun verrou entre deux écrivains : deux entrées identiques à la
  même seconde diffèrent par leur `alea`, et la création exclusive empêche qu'une écrase l'autre. ③ Ni le juge ni le
  laboratoire n'appellent encore ce programme : tant qu'ils ne le font pas, le registre est vide et le nombre d'essais
  ne compte rien de ce qu'ils font.
⑩ EFFET — `preenregistrer` et `inscrire_le_resultat` INSCRIVENT une entrée `registre_essais/<nom>.json` sur la BRANCHE
  DES REGARDS (`CONTRATS_DES_FICHIERS.BRANCHE_DES_REGARDS`) et la POUSSENT au dépôt distant ; aucun fichier du disque de
  travail n'est écrit (mission REGARD du 12-11-2026). La lecture fait un `fetch` de cette branche ; le reste lit.
  Les fonctions d'histoire et `bilan_de_la_fiche` (pour k) lancent git en lecture.
⑪ TERMINAISON — En ligne de commande, sort avec 0, 1 ou 2. Un appel à git peut ne pas revenir (aucun délai posé).
⑫ DÉFINITIONS
  un essai : un calcul d'une stratégie sur des cours passés, qu'il ait donné un résultat ou non
  l'hypothèse : ce que le calcul calcule vraiment — objectif, perte acceptée, durée, univers, signal, période, barème ;
    deux essais de même hypothèse sont le même essai refait
  l'empreinte : les 16 premiers caractères hexadécimaux du SHA-256 d'un texte ou d'octets
  la racine : le dossier du dépôt, ou d'une copie qui en garde l'arborescence
  la lignée : une fiche, sa mère, ses versions et leurs sœurs — tout ce que relient les liens déclarés (champ `lignee`
    des déclarations datées) et les liens du registre des essais (case `mere` d'un préenregistrement)
  la portée du regard : les fiches dont un essai compte comme regard d'une autre (« fiche », « lignee », « toutes »)
"""

import csv
import hashlib
import json
import os
import secrets
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import CONTRATS_DES_FICHIERS as C  # noqa: E402

PARIS = ZoneInfo("Europe/Paris")
DOSSIER = next(ch for ch, (contrat, _e, _l) in C.FICHIERS_A_VENIR.items() if contrat == "NATURES_DES_ENTREES_D_ESSAI")
# LES CASES QUE L'HYPOTHÈSE PORTE, telles que le contrat les énumère dans le commentaire de `hypothese`
# (ENTREE_PREENREGISTREMENT) : sans l'une d'elles, deux calculs différents auraient la même empreinte.
CASES_DE_L_HYPOTHESE = ("tp_pct", "sl_pct", "horizon", "univers", "signal", "periode", "bareme")
# LES RÉGLAGES DU REGISTRE DES ESSAIS — ce qui se change sans réécrire le code. Un seul programme les lit (celui-ci).
REGLAGES = "donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv"
EN_TETE_DES_REGLAGES = ["cle", "valeur", "statut", "source"]
# LES SENS QUE LE CODE SAIT APPLIQUER à `portee_du_regard` ; le CHOIX entre eux vit dans REGLAGES, jamais ici.
#   fiche  : un regard ne compte que pour la fiche qui l'a fait
#   lignee : un regard compte pour toute la lignée déclarée de la fiche (`lignee_de_la_fiche`)
#   toutes : un regard compte pour toutes les fiches
PORTEES_DU_REGARD = ("fiche", "lignee", "toutes")
# Ce que le registre ne sait pas : les essais faits avant lui (A-226, « HISTORIQUE NON COMPTABILISÉ », jamais zéro).
AVANT_LE_REGISTRE = "HISTORIQUE NON COMPTABILISÉ"
# LES SENS QUE LE CODE SAIT APPLIQUER à `calibrage_compte_comme_regard` (question J3 pour Jean-Luc) ; le choix vit dans
# REGLAGES : « oui » (un calibrage sur des années d'examen est un regard, lecture la plus stricte) ou « non ».
CALIBRAGE_REGARD = ("oui", "non")
# LE DOMAINE D'UN RÉGLAGE ENTIER (`_reglage`) : un entier ≥ 1, écrit en chiffres. `poussees_des_regards` (combien de fois
# une inscription tente sa poussée avant de lever) en est un ; sa valeur vit dans REGLAGES, jamais ici.
ENTIER_POSITIF = "entier ≥ 1"
# LE DOMAINE D'UN RÉGLAGE ADRESSE : un texte non vide. `depot_des_regards` (l'adresse du dépôt commun, où seul s'inscrit
# le regard) en est un ; sa valeur vit dans REGLAGES.
ADRESSE = "adresse non vide"
# Ce qui sépare, dans le bilan, plusieurs `part_regardee` distinctes d'une même fiche (toutes ses déclarations).
SEPARATEUR_DES_PARTS = " || "
# Les clés du dictionnaire rendu par `bilan_de_la_fiche`, dans leur ordre : l'interface que lit la porte du juge.
CLES_DU_BILAN = ("fiche_id", "portee_du_regard", "calibrage_compte_comme_regard", "lignee", "liens", "regards", "annees_deja_regardees",
                 "parts_regardees_declarees", "essais_de_la_fiche", "essais_de_la_lignee", "essais_du_registre", "k",
                 "avant_le_registre", "raisons")


def _horizon_en_json(objet):
    """Écrit l'horizon « aucune » par son mot dans le JSON (contrat du lot 0 ①), et refuse tout autre objet.
    ① RÔLE — Le crochet `default` de `json.dumps`.
    ② CONTEXTE D'APPEL — `empreinte_de_l_hypothese`, `_ecrire`.
    ③ ENTRÉE — `objet` : un objet que JSON ne sait pas écrire.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : le mot « aucune » pour COMMUN.HORIZON_AUCUNE.
      [rend: 1]
    ⑥ TRAITEMENT — reconnaître HORIZON_AUCUNE par identité, sinon lever.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — « dans un fichier JSON, il s'écrit par la chaîne de ce même mot, jamais par null : null y veut déjà
    dire absent » (contrat du lot 0 ①).
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève TypeError.
      [sort: non]"""
    import COMMUN
    if objet is COMMUN.HORIZON_AUCUNE:
        return COMMUN.MOT_DE_L_HORIZON_AUCUNE
    raise TypeError("registre des essais : objet non écrivable en JSON : %r" % (objet,))


def empreinte_de_l_hypothese(hypothese):
    """Rend l'empreinte de l'hypothèse d'un essai, en écriture canonique : CE QUI COMPTE dans le nombre d'essais.

    ① RÔLE — Dire si deux essais sont le même : même empreinte = même calcul refait, qui ne compte qu'une fois.
    ② CONTEXTE D'APPEL — `preenregistrer` ; `lire_le_registre`, qui la recalcule pour chaque entrée.
    ③ ENTRÉE — `hypothese` : un dictionnaire portant au moins CASES_DE_L_HYPOTHESE.
    ④ CONDITIONS D'ENTRÉE — Les valeurs s'écrivent en JSON (l'horizon « aucune » comme objet de COMMUN ou comme mot).
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser une case manquante · ② écrire en JSON trié, sans espaces, caractères non ASCII gardés ·
      ③ SHA-256, 16 premiers caractères.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'ordre des clés et les espaces ne changent pas un calcul : l'écriture canonique les efface. « 20 » et
      « aucune » sont deux essais différents (contrat du lot 0 ①) : le mot est écrit, jamais None.
    ⑨ CE QUI CLOCHE — 4.0 et 4 s'écrivent différemment en JSON : deux hypothèses égales en nombre mais pas en type
      compteraient deux fois. Le contrat demande des pourcents à 6 décimales : c'est à l'appelant de les arrondir.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (case manquante) ou TypeError (valeur non écrivable).
      [sort: non]
    """
    manque = [c for c in CASES_DE_L_HYPOTHESE if c not in hypothese]
    if manque:
        raise ValueError("hypothèse incomplète, case(s) manquante(s) : %s" % ", ".join(manque))
    texte = json.dumps(hypothese, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                       default=_horizon_en_json)
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:16]


def _maintenant():
    """Rend l'heure de Paris avec son décalage, à la seconde.
    ① RÔLE — Horodater une entrée.
    ② CONTEXTE D'APPEL — `preenregistrer`, `inscrire_le_resultat`.
    ③ ENTRÉE — —.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : « AAAA-MM-JJTHH:MM:SS+01:00 ».
      [rend: 1]
    ⑥ TRAITEMENT — horloge, fuseau Europe/Paris.
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — horodatage Europe/Paris du projet.
    ⑨ CE QUI CLOCHE — n'ordonne rien (contrat).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    return datetime.now(PARIS).isoformat(timespec="seconds")


def _ecrire(racine, entree, contrat):
    """Inscrit une entrée sur la BRANCHE DES REGARDS, sous le nom de l'empreinte de ses octets, après l'avoir
    confrontée ; rend son nom seulement quand la poussée a réussi.

    ① RÔLE — La seule écriture du registre — LA seule inscription du regard pour tout le système (superviseur J du
      12-11-2026, réponse 1).
    ② CONTEXTE D'APPEL — `preenregistrer`, `inscrire_le_resultat`.
    ③ ENTRÉE — `racine` : un dépôt git dont le dépôt distant de `CONTRATS_DES_FICHIERS.BRANCHE_PRINCIPALE` est
      joignable · `entree` : le dictionnaire · `contrat` : « NATURES_DES_ENTREES_D_ESSAI ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom de l'entrée, sans « .json » — LE REÇU que `JUGE_DES_STRATEGIES.jouer` exige pour
      toute séance de la fenêtre du regard unique.
      [rend: 1]
    ⑥ TRAITEMENT — ① confronter au contrat (`ecarts_d_une_entree`), lever s'il y a un écart · ② écrire les octets
      (JSON trié, indenté, fin de ligne) · ③ nom = empreinte des octets · ④ `_pousser_l_entree` : commit sur la
      branche des regards, poussée sans forçage, jusqu'à `poussees_des_regards` tentatives (réglage lu).
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Une entrée n'est jamais réécrite (R-505 ③) : son nom est l'empreinte de ses octets, et une entrée de
      même nom déjà sur la branche fait lever. POUSSER AVANT DE RENDRE : un regard écrit sur un disque seulement se
      contournait en effaçant le disque ou en prenant un clone neuf (relecteur J, D1, attaques A1 et A1b) ; sur la
      branche, tout clone le voit. RIEN N'EST ÉCRIT SUR LE DISQUE DE TRAVAIL : la porte exige un arbre propre (pas 6).
    ⑨ CE QUI CLOCHE — ① Le serveur accepte un commit en avance rapide qui EFFACE une entrée : l'ajout seul est une
      propriété de la LECTURE (`lire_le_registre`), pas de l'écriture (superviseur J, M3). ② Une réécriture forcée ou
      une suppression de la branche n'est pas bloquée (forçage, suppression : voies de faussaire, hors J1 ; la règle GitHub J2 est impossible sur le dépôt privé avec l'abonnement actuel, 403 mesuré par le superviseur REGARD, M2). ③ Le coût réseau d'une poussée par entrée n'est pas mesuré sur GitHub.
    ⑩ EFFET — Écrit des objets git dans le dépôt de `racine`, met à jour sa référence de suivi de la branche des
      regards, POUSSE vers le dépôt distant. Aucun fichier du disque de travail n'est touché.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (écart au contrat), FileExistsError (entrée déjà sur la branche)
      ou RuntimeError (poussée refusée autant de fois que le réglage le permet, ou réglage illisible) ; git peut ne pas revenir.
      [sort: non]
    """
    ecarts = C.ecarts_d_une_entree("entrée à écrire", entree, contrat)
    if ecarts:
        raise ValueError("registre des essais : " + " ; ".join(ecarts))
    octets = (json.dumps(entree, sort_keys=True, indent=1, ensure_ascii=False, default=_horizon_en_json)
              + "\n").encode("utf-8")
    nom = hashlib.sha256(octets).hexdigest()[:16]
    _pousser_l_entree(racine, nom, octets)
    return nom


def _depot_des_regards():
    """Rend le dépôt distant, la référence distante et la référence de suivi de la branche des regards.
    ① RÔLE — Nommer une fois, depuis le contrat, où vit l'inscription.
    ② CONTEXTE D'APPEL — `_pousser_l_entree`, `_octets_de_la_branche`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — BRANCHE_PRINCIPALE s'écrit « <dépôt distant>/<branche> ».
    ⑤ SORTIE — TROIS valeurs : « origin », « refs/heads/regards/… », « refs/remotes/origin/regards/… ».
      [rend: 3]
    ⑥ TRAITEMENT — couper BRANCHE_PRINCIPALE au premier « / » ; composer avec BRANCHE_DES_REGARDS.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le dépôt distant est celui de la branche principale : il n'est pas écrit une seconde fois (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    distant = C.BRANCHE_PRINCIPALE.split("/", 1)[0]
    return (distant, "refs/heads/" + C.BRANCHE_DES_REGARDS,
            "refs/remotes/%s/%s" % (distant, C.BRANCHE_DES_REGARDS))


def _depot_commun(racine):
    """Dit si le dépôt distant de cette racine EST le dépôt commun nommé au fichier des réglages.

    ① RÔLE — Qu'une copie locale (le geste ordinaire des épreuves et de la certification) n'inscrive jamais son
      regard dans son clone parent, et que la garde n'accepte jamais le reçu d'un dépôt jetable (relecteur REGARD,
      R-D3 ; superviseur REGARD, « À ajouter »).
    ② CONTEXTE D'APPEL — `_sommet_distant`, donc toute lecture et toute écriture de la branche des regards.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : vrai ou faux, et la raison (vide si vrai).
      [rend: 2]
    ⑥ TRAITEMENT — ① l'adresse attendue : `depot_des_regards` au fichier des réglages (`_reglage`, domaine ADRESSE) ·
      ② l'adresse CONFIGURÉE du dépôt distant (`git config --get remote.<distant>.url`, avant toute réécriture
      `insteadOf`, qui est le transport et non le nom) · ③ comparer après avoir retiré le protocole, l'identifiant
      (« …@ »), la barre et le « .git » finaux, sans casse ; « hôte:chemin » (SSH à la scp) vaut « hôte/chemin ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le dépôt distant était « celui de qui lance » : un `git clone d copie` inscrivait dans `d`, et le
      regard n'arrivait jamais au dépôt commun (mesuré par le relecteur, AT5b).
    ⑨ CE QUI CLOCHE — Une copie dont on récrit À LA FOIS le fichier des réglages et l'adresse du dépôt distant passe :
      geste délibéré, hors J1 (À SAVOIR). L'arbre propre exigé par la porte refuse un fichier des réglages modifié sans
      commit.
    ⑩ EFFET — Lance git en lecture ; lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    distant = C.BRANCHE_PRINCIPALE.split("/", 1)[0]
    ligne, raison = _reglage(racine, "depot_des_regards", ADRESSE)
    if ligne is None:
        return False, raison
    code, sortie, _err = lancer_git(racine, ["config", "--get", "remote.%s.url" % distant])
    lu = sortie.decode().strip()
    # « git@hôte:chemin » (adresse SSH à la scp) s'écrit « hôte/chemin » comme les autres (relecteur REGARD tour 2,
    # T2-D6) ; un chemin local (« /… ») garde ses deux-points.
    norme = lambda u: ((u.split("://", 1)[1] if "://" in u else u if u.startswith("/") else u.replace(":", "/", 1))
                       .split("@", 1)[-1].rstrip("/").removesuffix(".git").casefold())
    if code != 0 or norme(lu) != norme(ligne["valeur"]):
        return False, ("le dépôt distant « %s » de cette racine n'est pas le dépôt commun « %s » (%s) : une copie "
                       "n'inscrit ni ne lit les regards" % (lu, ligne["valeur"], REGLAGES))
    return True, ""


def _sommet_distant(racine):
    """Lit le sommet de la branche des regards AU DÉPÔT DISTANT et le rapporte dans la référence de suivi.

    ① RÔLE — Voir l'état réel de l'inscription, jamais celui d'un disque ou d'une référence locale.
    ② CONTEXTE D'APPEL — `_pousser_l_entree` (avant chaque tentative), `_octets_de_la_branche`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le commit au sommet (40 caractères), "" si la branche n'existe pas au dépôt distant, ou
      None si l'on ne sait pas ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ le dépôt distant doit être le dépôt commun (`_depot_commun`), sinon None · ① `git ls-remote
      --exit-code` : code 2 → la branche n'existe pas → "" ; mais si la référence de suivi
      locale existe, la branche a été SUPPRIMÉE au dépôt distant → None (défaut) · ② sinon `git fetch` de la branche
      SANS « + » : AU MIEUX, SANS GARANTIE, une réécriture forcée fait échouer la mise à jour de la référence de
      suivi → None (un `git fetch` ordinaire, un `--prune` ou un clone neuf l'effacent : relecteur REGARD, R-D2).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur J, M3 : la réécriture forcée et la suppression échappent au serveur ; un clone qui les a
      déjà vues, et rien fait d'autre, les signale. Ce signal est DÉCLASSÉ (superviseur REGARD, pas ⑤, décidé avec J1) :
      ce n'est pas une garantie.
    ⑨ CE QUI CLOCHE — ① Un clone NEUF ne connaît pas l'histoire d'avant une réécriture forcée : il ne la voit pas
      (forçage, suppression : voies de faussaire, hors J1 ; la règle GitHub J2 est impossible sur le dépôt privé avec l'abonnement actuel, 403 mesuré par le superviseur REGARD, M2). ② MESURÉ LE 12-11-2026 : une SUPPRESSION poussée DEPUIS CE
      CLONE (`git push origin :<branche>`) efface aussi sa référence de suivi — ce clone l'oublie et lit un registre
      VIDE ; seuls les autres clones la signalent. Voie de faussaire, hors J1.
    ⑩ EFFET — Lance git en réseau ; met à jour la référence de suivi.
    ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir (réseau).
      [sort: non]
    """
    distant, ref, suivi = _depot_des_regards()
    commun, raison = _depot_commun(racine)
    if not commun:
        return None, raison
    git = git_de(racine)
    code, sortie, err = lancer_git(racine, ["ls-remote", "--exit-code", distant, ref])
    if code == 2:
        code_l, _s = git("rev-parse", "--verify", "--quiet", suivi)
        if code_l == 0:
            return None, "branche des regards %s SUPPRIMÉE au dépôt distant (la référence de suivi la connaissait)" % ref
        return "", ""
    if code != 0:
        return None, "branche des regards illisible au dépôt distant %s (ls-remote code %d : %s)" % (
            distant, code, err.strip()[:160])
    code, _s, err = lancer_git(racine, ["fetch", "--quiet", "--no-tags", distant, "%s:%s" % (ref, suivi)])
    if code != 0:
        return None, "branche des regards non rapportée (fetch code %d — réécriture forcée ?) : %s" % (
            code, err.strip()[:160])
    code, sortie = git("rev-parse", "--verify", "--quiet", suivi + "^{commit}")
    if code != 0:
        return None, "référence de suivi %s illisible après fetch" % suivi
    return sortie.decode().strip(), ""


def _pousser_l_entree(racine, nom, octets):
    """Ajoute `registre_essais/<nom>.json` à la branche des regards, par un commit poussé sans forçage.

    ① RÔLE — Rendre l'inscription visible de tout clone AVANT que l'appelant calcule.
    ② CONTEXTE D'APPEL — `_ecrire`, une fois par entrée.
    ③ ENTRÉE — `racine` · `nom` : 16 caractères hexadécimaux · `octets` : le contenu de l'entrée.
    ④ CONDITIONS D'ENTRÉE — Le dépôt distant joignable.
    ⑤ SORTIE — Aucune valeur : rend la main quand la poussée a réussi.
      [rend: rien]
    ⑥ TRAITEMENT — jusqu'à `poussees_des_regards` fois (lu au fichier des réglages, `_reglage`) : ① sommet distant (`_sommet_distant`), inconnu → tentative
      perdue · ② l'entrée y est déjà → FileExistsError · ③ objet de l'entrée (`hash-object -w`), sous-arbre du
      dossier = celui du sommet plus l'entrée (`mktree`), arbre racine = ce seul dossier · ④ `commit-tree`, parent =
      le sommet (aucun s'il n'y a pas de branche) · ⑤ `git push <distant> <commit>:<branche>` SANS forçage ; refusée
      (un autre a poussé entre-temps) → recommencer sur le nouveau sommet.
    ⑦ UNITÉ — Des tentatives.
    ⑧ POURQUOI — Deux réservations concurrentes : la seconde est refusée, puis passe après relecture, et chacune voit
      l'autre (superviseur J, M3, mesuré sur un dépôt nu local). Un commit propre à chaque tentative (son entrée porte
      `alea` et `horodatage_paris`) : le piège « même commit poussé deux fois réussit en silence » (M4 de GITHUB) ne
      s'applique pas. Le commit est fait par la plomberie de git, sans toucher l'index ni le disque de travail.
    ⑨ CE QUI CLOCHE — ① L'identité du commit est celle du registre (« registre des essais »), pas celle de l'agent :
      choix technique de la mission REGARD, sans incidence sur l'ordre (lu par l'histoire, jamais par les dates).
      ② La branche des regards ne porte QUE le dossier du registre ; un fichier d'un autre dossier poussé par un tiers
      serait perdu au commit suivant (non contrôlé).
    ⑩ EFFET — Écrit des objets git ; pousse ; met à jour la référence de suivi.
    ⑪ TERMINAISON — Rend la main ; lève FileExistsError ou RuntimeError ; git peut ne pas revenir.
      [sort: non]
    """
    distant, ref, _suivi = _depot_des_regards()
    dossier = DOSSIER.rstrip("/")
    git = git_de(racine)
    ligne, raison = _reglage(racine, "poussees_des_regards", ENTIER_POSITIF)
    if ligne is None:
        raise RuntimeError("registre des essais : entrée %s non inscrite : %s" % (nom, raison))
    tentatives = int(ligne["valeur"])
    raisons = []
    for _tentative in range(tentatives):
        sommet, raison = _sommet_distant(racine)
        if sommet is None:
            raisons.append(raison)
            continue
        lignes = []
        if sommet:
            code, sortie = git("ls-tree", sommet, dossier + "/")
            if code != 0:
                raisons.append("ls-tree impossible au sommet %s" % sommet[:12])
                continue
            for l in sortie.decode().splitlines():
                meta, _t, chemin = l.partition("\t")
                if os.path.basename(chemin) == nom + ".json":
                    raise FileExistsError("entrée %s déjà inscrite sur la branche des regards" % nom)
                lignes.append("%s\t%s" % (meta, os.path.basename(chemin)))
        code, blob = git("hash-object", "-w", "--stdin", entree=octets)
        if code != 0:
            raisons.append("hash-object impossible")
            continue
        lignes.append("100644 blob %s\t%s.json" % (blob.decode().strip(), nom))
        code, sous_arbre = git("mktree", entree="".join(l + "\n" for l in lignes).encode())
        code2, arbre = git("mktree", entree=("040000 tree %s\t%s\n" % (sous_arbre.decode().strip(), dossier)).encode())
        if code != 0 or code2 != 0:
            raisons.append("mktree impossible")
            continue
        parent = ["-p", sommet] if sommet else []
        code, commit = git("-c", "user.name=registre des essais", "-c", "user.email=registre-des-essais@simulation",
                           "commit-tree", arbre.decode().strip(), *parent, "-m", "registre des essais : " + nom)
        commit = commit.decode().strip()
        if code != 0 or len(commit) != 40:
            # JAMAIS « git push <distant> :<branche> » : un commit vide SUPPRIMERAIT la branche des regards (mesuré le
            # 12-11-2026 sur l'outil d'épreuve, dont le commit-tree avait échoué en silence)
            raisons.append("commit-tree impossible")
            continue
        code, _s, err = lancer_git(racine, ["push", "--quiet", distant, "%s:%s" % (commit, ref)])
        if code == 0:
            _sommet_distant(racine)
            return
        raisons.append("poussée refusée (code %d) : %s" % (code, err.strip()[:160]))
    raise RuntimeError("registre des essais : entrée %s non inscrite après %d tentatives : %s"
                       % (nom, tentatives, " | ".join(raisons)))


def preenregistrer(racine, fiche_id, hypothese, famille="NON_DECLARE", mere="", octets=None, declaration=None,
                   genre="ESSAI"):
    """Inscrit un essai AVANT son calcul et rend son nom : sans ce nom, le calcul n'a pas de trace.

    ① RÔLE — Écrire l'entrée PREENREGISTREMENT d'un essai (contrat ENTREE_PREENREGISTREMENT).
    ② CONTEXTE D'APPEL — Destiné à `jouer` du juge et au laboratoire, avant chaque calcul ; l'épreuve de B.
    ③ ENTRÉE — `racine` · `fiche_id` : l'identifiant de la fiche · `hypothese` : voir `empreinte_de_l_hypothese` ·
      `famille` : la famille déclarée, « NON_DECLARE » sinon · `mere` : l'empreinte d'hypothèse du calcul englobant,
      vide sinon · `octets` : {libellé : [chemin relatif, empreinte ou « ABSENT »]}, pour refaire l'essai ·
      `declaration` : {periode_conception, part_regardee, regle_univers, date_regle_univers} lus dans la déclaration
      datée de la fiche, ou None · `genre` : l'un de `CONTRATS_DES_FICHIERS.GENRES_D_ESSAI` (« ESSAI », « CALIBRAGE »).
    ④ CONDITIONS D'ENTRÉE — Celles de `empreinte_de_l_hypothese` ; le registre des stratégies sous la racine.
    ⑤ SORTIE — UNE valeur : le nom de l'entrée (16 caractères hexadécimaux).
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ le genre hors de GENRES_D_ESSAI → lever ; l'identité de la fiche
      (`CONTRATS_DES_FICHIERS.identite_de_la_fiche`) : inconnue du registre des stratégies → lever ;
      l'entrée porte l'identifiant TEL QU'ÉCRIT AU REGISTRE · ① calculer l'empreinte de l'hypothèse · ② composer l'entrée aux clés du contrat, les quatre champs
      de la déclaration valant « NON_DECLARE » quand ils ne sont pas donnés (contrat : « NON_DECLARE ») · ③ `_ecrire`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Même une expérience sans résultat est enregistrée » (A-226) : l'inscription précède le calcul, pour
      qu'un calcul qui tombe ou déçoit compte quand même.
    ⑨ CE QUI CLOCHE — Rien n'empêche un appelant de calculer sans préenregistrer : seul l'appel dans `jouer` le
      garantira (demande à l'agent A). Une version de la moulinette doit être inscrite au registre des stratégies
      AVANT son premier essai (R-505 : « toute version essayée compte comme un essai et comme une stratégie à part
      entière ») ; sinon son essai est refusé.
    ⑩ EFFET — Inscrit et pousse une entrée sur la branche des regards (`_ecrire`).
    ⑪ TERMINAISON — Rend la main ; lève ValueError (genre ou fiche inconnus) ou voir `_ecrire`.
      [sort: non]
    """
    if genre not in C.GENRES_D_ESSAI:
        raise ValueError("registre des essais : genre %r hors de %s" % (genre, ", ".join(C.GENRES_D_ESSAI)))
    connue, raison = C.identite_de_la_fiche(racine, fiche_id)
    if connue is None:
        raise ValueError("registre des essais : " + raison)
    d = declaration or {}
    entree = {
        "nature": "PREENREGISTREMENT", "horodatage_paris": _maintenant(), "alea": secrets.token_hex(4),
        "fiche_id": connue, "genre_d_essai": genre, "famille": famille or "NON_DECLARE", "mere": mere or "",
        "hypothese": hypothese, "empreinte_hypothese": empreinte_de_l_hypothese(hypothese),
        "octets": octets or {},
    }
    for cle in ("periode_conception", "part_regardee", "regle_univers", "date_regle_univers"):
        entree[cle] = d.get(cle) or "NON_DECLARE"
    # LE SOMMET DE LA BRANCHE PRINCIPALE QUE CE REGARD VOIT (superviseur ANCRAGE du 12-11-2026, §4.1 ; décision de
    # Jean-Luc du 12-11-2026 à 09h04, « Reparer ») : l'ancre de la déclaration datée. La référence locale, sans fetch :
    # c'est la version que la porte a jugée (elle exige HEAD = cette branche). Illisible → « INCONNU », l'ancre est
    # alors inconnue et la fiche NON JUGEABLE (échec fermé) ; le regard est inscrit quand même (A-226).
    code, sortie, _err = lancer_git(racine, ["rev-parse", "--verify", "--quiet", C.BRANCHE_PRINCIPALE + "^{commit}"])
    entree["sommet_principal"] = sortie.decode().strip() if code == 0 else "INCONNU"
    return _ecrire(racine, entree, "NATURES_DES_ENTREES_D_ESSAI")


def inscrire_le_resultat(racine, preenregistrement, resultat=None, echec=""):
    """Inscrit le résultat (ou l'échec) d'un essai préenregistré, et rend le nom de l'entrée RESULTAT.

    ① RÔLE — Fermer un essai : son résultat, ou la cause de sa chute, sans jamais réécrire le préenregistrement.
    ② CONTEXTE D'APPEL — Destiné à `jouer` après son calcul ; l'épreuve de B.
    ③ ENTRÉE — `racine` · `preenregistrement` : le nom rendu par `preenregistrer` · `resultat` : un dictionnaire, ou
      None si le calcul est tombé · `echec` : « TypeErreur: message », vide sinon.
    ④ CONDITIONS D'ENTRÉE — Le préenregistrement est sur la branche des regards (union lue par `lire_le_registre`).
    ⑤ SORTIE — UNE valeur : le nom de l'entrée RESULTAT.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser un préenregistrement absent · ② refuser un résultat ET un échec à la fois, ou aucun des
      deux · ③ composer l'entrée, `_ecrire`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un résultat sans préenregistrement serait un essai dont on ne sait pas s'il a été déclaré avant.
    ⑨ CE QUI CLOCHE — Deux résultats pour un même préenregistrement sont admis (deux fichiers) ; `lire_le_registre` les
      signale.
    ⑩ EFFET — Crée un fichier.
    ⑪ TERMINAISON — Rend la main ; lève FileNotFoundError, ValueError ou FileExistsError.
      [sort: non]
    """
    entrees, _defauts = lire_le_registre(racine)
    if (entrees.get(preenregistrement) or {}).get("nature") != "PREENREGISTREMENT":
        raise FileNotFoundError("préenregistrement « %s » absent de la branche des regards" % preenregistrement)
    if (resultat is None) == (not echec):
        raise ValueError("un résultat OU un échec, jamais les deux ni aucun")
    entree = {"nature": "RESULTAT", "horodatage_paris": _maintenant(), "alea": secrets.token_hex(4),
              "preenregistrement": preenregistrement, "resultat": resultat, "echec": echec or ""}
    return _ecrire(racine, entree, "NATURES_DES_ENTREES_D_ESSAI")


def entrees_des_octets(fichiers, racine):
    """Lit et contrôle des entrées données par leurs octets : rend les entrées saines et la liste des défauts.

    ① RÔLE — Le contrôle commun au registre du jour et au registre d'une date passée.
    ② CONTEXTE D'APPEL — `lire_le_registre`, `nombre_d_essais` (à un commit), `premier_regard`.
    ③ ENTRÉE — `fichiers` : {nom de fichier (« <16 hex>.json ») : octets} · `racine` : où lire le registre des
      stratégies (sur le disque) pour la forme canonique des fiches.
    ④ CONDITIONS D'ENTRÉE — Le registre des stratégies sous la racine, dès qu'il y a un préenregistrement.
    ⑤ SORTIE — DEUX valeurs : {nom sans .json : entrée} et la liste des défauts (phrases). Chaque PREENREGISTREMENT
      rendu porte son `fiche_id` sous FORME CANONIQUE (une copie de l'entrée ; le fichier n'est pas touché).
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque fichier : ① nom = empreinte des octets, sinon « altérée » · ② JSON lisible · ③ confronté
      au contrat · ④ PREENREGISTREMENT : empreinte d'hypothèse recalculée égale à celle écrite ; genre dans
      GENRES_D_ESSAI ; fiche ramenée à sa forme canonique (`CONTRATS_DES_FICHIERS.identite_de_la_fiche`), inconnue ou
      ambiguë → DÉFAUT · puis ⑤ chaque RESULTAT renvoie à un PREENREGISTREMENT présent · ⑥ au plus un RESULTAT par
      préenregistrement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un compte fait sur un registre abîmé serait faux sans le dire (relecture du lot L4, M1). La forme
      canonique à la LECTURE, une fois, et non comparaison par comparaison (superviseur R-759 du 11-11-2026, 23h32,
      point 4.2 : « chaque nouveau lecteur l'oubliera ») ; une entrée au nom inconnu était lue sans bruit et jamais
      comptée (relecteur de B2, D5).
    ⑨ CE QUI CLOCHE — Le registre des stratégies lu est celui du DISQUE, même pour un registre des essais lu à un commit.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    saines, defauts, fiches = {}, [], None
    for nom_f in sorted(fichiers):
        octets = fichiers[nom_f]
        nom = nom_f[:-5] if nom_f.endswith(".json") else nom_f
        if hashlib.sha256(octets).hexdigest()[:16] != nom:
            defauts.append("%s : altérée — son nom n'est plus l'empreinte de ses octets" % nom_f)
            continue
        try:
            e = json.loads(octets.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as ex:
            defauts.append("%s : JSON illisible (%s)" % (nom_f, ex))
            continue
        ecarts = C.ecarts_d_une_entree(nom_f, e, "NATURES_DES_ENTREES_D_ESSAI")
        if ecarts:
            defauts += ecarts
            continue
        if e["nature"] == "PREENREGISTREMENT":
            try:
                recalc = empreinte_de_l_hypothese(e["hypothese"])
            except (ValueError, TypeError) as ex:
                defauts.append("%s : hypothèse illisible (%s)" % (nom_f, ex))
                continue
            if recalc != e["empreinte_hypothese"]:
                defauts.append("%s : empreinte d'hypothèse écrite %s, recalculée %s"
                               % (nom_f, e["empreinte_hypothese"], recalc))
                continue
            if e["genre_d_essai"] not in C.GENRES_D_ESSAI:
                defauts.append("%s : genre d'essai %r hors de %s" % (nom_f, e["genre_d_essai"], ", ".join(C.GENRES_D_ESSAI)))
                continue
            if fiches is None:
                try:
                    fiches = C.lire_les_fiches(racine)
                except (OSError, ValueError) as ex:
                    return {}, defauts + ["registre des stratégies illisible : %s" % ex]
            canon, raison = C.identite_de_la_fiche(racine, e["fiche_id"], fiches)
            if canon is None:
                defauts.append("%s : %s" % (nom_f, raison))
                continue
            e = dict(e, fiche_id=canon)
        saines[nom] = e
    vus = {}
    for nom, e in saines.items():
        if e["nature"] == "RESULTAT":
            p = e["preenregistrement"]
            if saines.get(p, {}).get("nature") != "PREENREGISTREMENT":
                defauts.append("%s.json : résultat sans préenregistrement « %s »" % (nom, p))
            vus[p] = vus.get(p, 0) + 1
    defauts += ["préenregistrement %s : %d résultats" % (p, n) for p, n in sorted(vus.items()) if n > 1]
    return saines, defauts


def _octets_de_la_branche(racine, sommet):
    """Rend les octets de TOUTES les entrées jamais ajoutées le long de la branche des regards, jusqu'à `sommet`.

    ① RÔLE — L'UNION des entrées, y compris celles qu'un commit postérieur aurait effacées.
    ② CONTEXTE D'APPEL — `lire_le_registre`.
    ③ ENTRÉE — `racine` · `sommet` : un commit de la branche des regards.
    ④ CONDITIONS D'ENTRÉE — Les objets de la branche présents (rapportés par `_sommet_distant`).
    ⑤ SORTIE — DEUX valeurs : {nom de fichier (« <16 hex>.json ») : octets} et la liste des défauts (phrases).
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ un commit à plusieurs parents sur la branche → défaut · ① `git log --full-history
      --diff-filter=A --raw` du dossier : chaque fichier jamais AJOUTÉ, avec son objet, y compris du côté perdu d'une
      fusion ·
      ② un même nom ajouté deux fois avec deux contenus → défaut · ③ les octets par `git cat-file --batch` ·
      ④ `historique_en_ajout_seul` le long de la branche : un effacement ou une retouche commis → défaut, et
      l'entrée effacée RESTE comptée (elle est dans l'union).
    ⑦ UNITÉ — Des entrées.
    ⑧ POURQUOI — Le serveur accepte un commit en avance rapide qui efface une entrée (superviseur J, M3, mesuré :
      « commit ff qui EFFACE une entrée: 0 ») : l'ajout seul doit être une propriété de la LECTURE — l'union des
      entrées jamais ajoutées (déjà écrit pour `premier_regard`, `--diff-filter=A`), plus le signal de
      `historique_en_ajout_seul`.
    ⑨ CE QUI CLOCHE — ① Le coût grandit avec l'histoire de la branche (un `log` et un `cat-file` par lecture) : non
      mesuré au-delà de quelques dizaines d'entrées. ② Une fusion poussée par erreur sur la branche des regards est un
      défaut DÉFINITIF : toute garde refuse ensuite (échec fermé, voulu). Conduite à tenir : la décision revient à
      Jean-Luc ; un agent ne force jamais la branche pour la réparer (relecteur REGARD tour 2, T2-D7).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir.
      [sort: non]
    """
    git = git_de(racine)
    dossier = DOSSIER.rstrip("/")
    code, sortie = git("log", "--full-history", "--diff-filter=A", "--no-renames", "--raw", "--no-abbrev", "--format=",
                       sommet, "--", dossier + "/")
    if code != 0:
        return {}, ["histoire de la branche des regards illisible au sommet %s" % sommet[:12]]
    objets, defauts = {}, []
    # AUCUNE FUSION SUR LA BRANCHE DES REGARDS : seul `_pousser_l_entree` l'écrit, toujours à un parent ; un commit à
    # plusieurs parents n'y vient d'aucun geste légitime (superviseur REGARD, « À ajouter » ; relecteur, R-D1).
    code_f, fusions = git("rev-list", "--min-parents=2", sommet)
    if code_f != 0 or fusions.strip():
        defauts.append("commit(s) de fusion sur la branche des regards : %s" % (
            " ".join(c[:12] for c in fusions.decode().split()[:3]) or "liste illisible"))
    for l in sortie.decode().splitlines():
        if not l.startswith(":"):
            continue
        meta, _t, chemin = l.partition("\t")
        f = os.path.basename(chemin)
        if not f.endswith(".json"):
            continue
        blob = meta.split()[3]
        if f in objets and objets[f] != blob:
            defauts.append("%s : ajoutée deux fois avec deux contenus différents" % f)
        objets.setdefault(f, blob)
    fichiers = {}
    if objets:
        noms = sorted(objets)
        code, flux = git("cat-file", "--batch", entree=("\n".join(objets[f] for f in noms) + "\n").encode())
        if code != 0:
            return {}, defauts + ["objets de la branche des regards illisibles"]
        pos = 0
        for f in noms:
            fin = flux.index(b"\n", pos)
            tete = flux[pos:fin].split()
            if len(tete) != 3 or tete[1] != b"blob":
                return {}, defauts + ["objet de %s illisible" % f]
            taille = int(tete[2])
            fichiers[f] = flux[fin + 1:fin + 1 + taille]
            pos = fin + 1 + taille + 1
    defauts += historique_en_ajout_seul(racine, sommet)
    return fichiers, defauts


def lire_le_registre(racine):
    """Lit le registre des essais SUR LA BRANCHE DES REGARDS du dépôt distant — l'union de toutes ses entrées — et le
    contrôle. Le disque de travail n'est plus lu.

    ① RÔLE — Le registre tel que le dépôt distant le porte, le même pour tout clone.
    ② CONTEXTE D'APPEL — `nombre_d_essais` sans date ; `regards_sur_les_annees`, `lignee_de_la_fiche`,
      `inscrire_le_resultat` ; `JUGE_DES_STRATEGIES._garde_du_regard_unique` (le reçu) ; `main`.
    ③ ENTRÉE — `racine` : un dépôt git dont le dépôt distant de la branche principale est joignable.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : celles d'`entrees_des_octets` (fiches sous forme canonique), plus les défauts de la
      branche. Une branche qui n'existe pas au dépôt distant (et que ce clone n'a jamais vue) rend ({}, []) : un
      registre vide. Un dépôt distant illisible rend ({}, [raison]) : jamais un registre vide (R-734).
      [rend: 2]
    ⑥ TRAITEMENT — ① `_sommet_distant` (fetch) · ② `_octets_de_la_branche` (union + ajout seul) ·
      ③ `entrees_des_octets`.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — Superviseur J du 12-11-2026, réponse 1 : « dans `lire_le_registre` : lire, après `fetch`, l'union des
      entrées jamais ajoutées sur cette branche, avec le contrôle d'ajout seul. Le disque n'est plus lu. » Une lecture
      du disque laissait passer A1 (regard effacé du disque) et A1b (clone neuf) du relecteur J.
    ⑨ CE QUI CLOCHE — ① Un `fetch` à chaque lecture : coût réseau non mesuré. ② Les sous-dossiers et les fichiers qui
      ne finissent pas par .json sont ignorés.
    ⑩ EFFET — Lance git en réseau (fetch) ; met à jour la référence de suivi.
    ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir.
      [sort: non]
    """
    sommet, raison = _sommet_distant(racine)
    if sommet is None:
        return {}, ["registre des essais illisible : " + raison]
    if not sommet:
        return {}, []
    fichiers, defauts = _octets_de_la_branche(racine, sommet)
    saines, d2 = entrees_des_octets(fichiers, racine)
    return saines, defauts + d2


def environnement_sans_lieu():
    """Rend une copie de l'environnement d'où sont retirées les variables qui désignent un LIEU du dépôt pour git.

    ① RÔLE — Que git lise le dépôt de `racine`, et lui seul, quel que soit l'environnement hérité (relecteur J, D3 ;
      superviseur J du 12-11-2026, M5 : « GIT_DIR l'emporte sur -C »).
    ② CONTEXTE D'APPEL — `lancer_git`, à chaque appel.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — git installé.
    ⑤ SORTIE — UNE valeur : un dictionnaire {nom : valeur}, l'environnement à passer à git.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander à git LUI-MÊME la liste des variables locales au dépôt (`git rev-parse
      --local-env-vars` : « GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE… ») · ② en retirer celles de la CONFIGURATION (nom
      qui commence par « GIT_CONFIG ») · ③ copier `os.environ` sans les autres.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — PAR PROPRIÉTÉ, JAMAIS PAR ÉNUMÉRATION : la liste vient de git, qui sait quelles variables changent le
      dépôt lu ; une version de git qui en ajoute une est couverte sans toucher ce code. LA CONFIGURATION RESTE :
      l'environnement de cette machine porte GIT_CONFIG_COUNT et ses clés (`url.<…>.insteadOf`, l'identification), dont
      la poussée de la réservation dépend (superviseur J, M5 ; mission REGARD : « JAMAIS GIT_CONFIG_* ») — mesuré le
      12-11-2026 : `git rev-parse --local-env-vars` rend GIT_CONFIG, GIT_CONFIG_PARAMETERS et GIT_CONFIG_COUNT parmi les
      variables locales ; les retirer casserait le transport.
    ⑨ CE QUI CLOCHE — ① GIT_NAMESPACE (que le superviseur cite) n'est PAS dans la liste de git 2.43 : il reste. Il ne
      change que l'espace des références, pas le dépôt ; consigné, non corrigé (une énumération à la main serait le
      défaut que ce code évite). ② Un appelant du même processus peut remplacer cette fonction : limite J1, écrite
      (erreur d'agent, pas faussaire, décidée par Jean-Luc le 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708). ③ Les configurations par variable laissées
      (GIT_CONFIG_*) peuvent elles-mêmes désigner un autre lieu (`core.worktree`) : hors périmètre « accident ».
    ⑩ EFFET — Lance git une fois par appel (sans dépôt).
    ⑪ TERMINAISON — Rend la main ; lève RuntimeError si git ne rend pas sa liste (R-734 : un contrôle qui n'a pas pu
      tourner ne passe jamais pour vert) ; git peut ne pas revenir.
      [sort: non]
    """
    r = subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True, text=True)
    lieux = {v for v in r.stdout.split() if not v.startswith("GIT_CONFIG")}
    if r.returncode != 0 or "GIT_DIR" not in lieux:
        raise RuntimeError("git ne rend pas la liste de ses variables de lieu (code %d) : aucun appel git n'est sûr"
                           % r.returncode)
    return {k: v for k, v in os.environ.items() if k not in lieux}


def lancer_git(racine, args, entree=None):
    """LE lanceur git du système du regard : git dans `racine`, environnement purgé de ses variables de lieu.

    ① RÔLE — Une seule façon d'appeler git pour le registre des essais, la déclaration (B3), la porte du juge (J) et k
      (`JUGE_DES_STRATEGIES.k_a_la_date`) : il y en avait trois (superviseur J, M5 ; R-708).
    ② CONTEXTE D'APPEL — `git_de` ; `JUGER_UNE_FICHE._head_est_la_branche` ; `JUGE_DES_STRATEGIES.k_a_la_date`.
    ③ ENTRÉE — `racine` : le dossier du dépôt · `args` : la liste des arguments de git · `entree` : des octets pour
      l'entrée standard, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le code de sortie, les octets de la sortie, le texte de l'erreur.
      [rend: 3]
    ⑥ TRAITEMENT — `git -C racine <args>`, environnement de `environnement_sans_lieu`, sorties capturées.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Voir `environnement_sans_lieu`.
    ⑨ CE QUI CLOCHE — Aucun délai posé.
    ⑩ EFFET — Lance git, qui peut écrire (poussée, objets) selon les arguments.
    ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir (réseau, aucun délai).
      [sort: non]
    """
    r = subprocess.run(["git", "-C", racine] + list(args), capture_output=True, input=entree,
                       env=environnement_sans_lieu())
    return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace")


def git_de(racine):
    """Rend une fonction qui lance git dans `racine`, par le lanceur unique `lancer_git`.
    ① RÔLE — Une seule façon d'appeler git dans ce programme (et dans DECLARER_UNE_STRATEGIE, qui l'importe).
    ② CONTEXTE D'APPEL — `historique_en_ajout_seul`, `_registre_au_commit`, `premier_regard`, `nombre_d_essais`, la
      branche des regards (`_octets_de_la_branche`, `_pousser_l_entree`), et
      `DECLARER_UNE_STRATEGIE.declaration_engagee`.
    ③ ENTRÉE — `racine` : la racine du dépôt git.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la fonction git(*args, entree=None) → (code, octets).
      [rend: 1]
    ⑥ TRAITEMENT — fabriquer la fonction.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : une seule façon d'appeler git ; l'environnement purgé vient de `lancer_git`.
    ⑨ CE QUI CLOCHE — aucun délai posé.
    ⑩ EFFET — Aucun (la fonction rendue lance git).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def git(*args, entree=None):
        """Lance git dans la racine.
        ① RÔLE — lire l'histoire, ou écrire la branche des regards.
        ② CONTEXTE D'APPEL — les fonctions d'histoire et de la branche des regards.
        ③ ENTRÉE — `args` : les arguments de git · `entree` : octets pour l'entrée standard, ou None.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : le code et les octets de sortie.
          [rend: 2]
        ⑥ TRAITEMENT — `lancer_git`.
        ⑦ UNITÉ — octets.
        ⑧ POURQUOI — une seule façon d'appeler git.
        ⑨ CE QUI CLOCHE — l'erreur de git est perdue (voir `lancer_git` pour l'avoir).
        ⑩ EFFET — lance git.
        ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir.
          [sort: non]"""
        code, sortie, _err = lancer_git(racine, args, entree)
        return code, sortie
    return git


def histoire_lisible(racine, branche):
    """Dit si l'histoire de `branche` est entière (dépôt non superficiel) et si la branche existe.
    ① RÔLE — La condition préalable de tout compte ou de tout ancrage par l'ordre dans l'histoire.
    ② CONTEXTE D'APPEL — `nombre_d_essais`, `premier_regard`, `DECLARER_UNE_STRATEGIE.declaration_engagee`.
    ③ ENTRÉE — `racine` · `branche` : le nom de la branche principale (« origin/main » par défaut chez les appelants).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le commit au sommet de la branche (40 caractères) ou None, et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — ① refuser un dépôt superficiel · ② lire le sommet de la branche.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un clone superficiel n'a pas l'histoire : ce qui en dépend se dit INCONNU (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    git = git_de(racine)
    code, sortie = git("rev-parse", "--is-shallow-repository")
    if code != 0 or sortie.strip() != b"false":
        return None, "histoire absente : dépôt superficiel ou illisible"
    code, sortie = git("rev-parse", "--verify", "--quiet", branche + "^{commit}")
    if code != 0 or not sortie.strip():
        return None, "branche « %s » introuvable" % branche
    return sortie.decode().strip(), ""


def historique_en_ajout_seul(racine, branche):
    """Dit si, le long de `branche`, chaque version du registre des essais CONTIENT la précédente, octet pour octet.

    ① RÔLE — Faire rougir un effacement ou une retouche d'entrée commis puis commités (superviseur R-759, défaut 5 :
      « chaque version du registre doit être un préfixe exact de la suivante, un effacement rougit »).
    ② CONTEXTE D'APPEL — `nombre_d_essais` (compte à un commit), `premier_regard` ; `main`.
    ③ ENTRÉE — `racine` · `branche`.
    ④ CONDITIONS D'ENTRÉE — Histoire lisible (`histoire_lisible`).
    ⑤ SORTIE — UNE valeur : la liste des défauts (phrases), vide si l'ajout seul tient.
      [rend: 1]
    ⑥ TRAITEMENT — ① les commits de la branche qui touchent le dossier, du plus ancien au plus récent
      (`git rev-list --reverse --topo-order`) · ② à chacun, la liste {fichier : objet git} du dossier
      (`git ls-tree`) · ③ chaque entrée d'une version doit se retrouver, même objet, dans la suivante (les fusions sont
      refusées à part, par `_octets_de_la_branche`).
    ⑦ UNITÉ — Des commits et des fichiers.
    ⑧ POURQUOI — Pour un dossier d'entrées immuables, « préfixe exact » se lit « ensemble inclus, objets identiques ».
    ⑨ CE QUI CLOCHE — Une réécriture forcée de la branche efface l'histoire elle-même (forçage, suppression : voies de faussaire, hors J1 ; la règle GitHub J2 est impossible sur le dépôt privé avec l'abonnement actuel, 403 mesuré par le superviseur REGARD, M2). LIMITE J1 :
      l'erreur d'un agent, pas un faussaire (décidée par Jean-Luc le 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    git = git_de(racine)
    dossier = DOSSIER.rstrip("/")
    # Histoire LINÉAIRE : sur la branche des regards, toute fusion est déjà un défaut (`_octets_de_la_branche`) ;
    # l'histoire entière et la comparaison par parent y étaient redondantes, sans épreuve qui les distingue
    # (relecteur REGARD tour 2, T2-D3, sabotages XT1 et XT3 survivants) : retirées (R-751, simple sans perdre le fond).
    code, sortie = git("rev-list", "--reverse", "--topo-order", branche, "--", dossier)
    if code != 0:
        return ["histoire du registre illisible sur %s" % branche]
    defauts, avant = [], None
    for commit in sortie.decode().split():
        code, arbre = git("ls-tree", commit, dossier + "/")
        if code != 0:
            return ["ls-tree impossible au commit %s" % commit[:12]]
        version = {}
        for l in arbre.decode().splitlines():
            meta, _t, chemin = l.partition("\t")
            version[chemin] = meta.split()[2]
        for chemin, objet in (avant or {}).items():
            if chemin not in version:
                defauts.append("entrée %s effacée au commit %s" % (os.path.basename(chemin), commit[:12]))
            elif version[chemin] != objet:
                defauts.append("entrée %s modifiée au commit %s" % (os.path.basename(chemin), commit[:12]))
        avant = version
    return defauts


def _registre_au_commit(racine, commit):
    """Rend les octets des entrées du registre telles que le commit les porte.
    ① RÔLE — Lire le registre à un point de l'histoire.
    ② CONTEXTE D'APPEL — `nombre_d_essais`, `premier_regard`.
    ③ ENTRÉE — `racine` · `commit` : un commit.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs : {nom de fichier : octets} ou None, et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — `git ls-tree` du dossier, puis `git show` de chaque entrée.
    ⑦ UNITÉ — —.
    ⑧ POURQUOI — l'histoire, pas le disque ni l'horodatage écrit.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    git = git_de(racine)
    code, sortie = git("ls-tree", "--name-only", commit, DOSSIER.rstrip("/") + "/")
    if code != 0:
        return None, "ls-tree impossible au commit %s" % commit[:12]
    fichiers = {}
    for chemin in sortie.decode().splitlines():
        if chemin.endswith(".json"):
            c, o = git("show", "%s:%s" % (commit, chemin))
            if c != 0:
                return None, "entrée illisible au commit %s : %s" % (commit[:12], chemin)
            fichiers[os.path.basename(chemin)] = o
    return fichiers, ""


def nombre_d_essais(racine, commit=None, fiche_id=None, famille=None, branche=C.BRANCHE_PRINCIPALE, lignee_de=None):
    """Compte les essais faits : le nombre d'hypothèses DISTINCTES préenregistrées, au registre du jour ou à un commit.

    ① RÔLE — Donner le nombre d'essais que la loi demande (R-505 ⑧ : la probabilité de surapprentissage et le Sharpe
      dégonflé, « nombre_d_essais » au contrat DETAILS_DES_CONTROLES ; l'affichage « nombre_d_essais » du verdict).
    ② CONTEXTE D'APPEL — Destiné au juge, au moment du verdict ; `bilan_de_la_fiche` ; `main` ; les épreuves de B et B2.
    ③ ENTRÉE — `racine` · `commit` : le commit de la déclaration, ou None pour le registre du disque · `fiche_id`,
      `famille` : pour ne compter qu'une fiche ou une famille, None pour tout compter · `branche` : la branche
      principale · `lignee_de` : une fiche, pour ne compter que les essais de sa lignée (`lignee_de_la_fiche`, liens
      des déclarations lus SUR LE DISQUE même avec `commit`), None sinon.
    ④ CONDITIONS D'ENTRÉE — Avec `commit` : un dépôt git complet.
    ⑤ SORTIE — DEUX valeurs : le nombre (entier) ou « INCONNU », et la raison (vide si le nombre est rendu).
      [rend: 2]
    ⑥ TRAITEMENT — ① sans commit : lire le disque · ② avec commit : histoire lisible, commit ANCÊTRE de la branche
      (`git merge-base --is-ancestor`), histoire du registre en ajout seul, puis le registre à ce commit · ③ un défaut
      → INCONNU · ③bis `fiche_id` ramené à sa forme canonique, inconnu → INCONNU, jamais 0 (relecteur de B2, D2) ·
      ④ avec `lignee_de` : la lignée, inconnue (fiche inconnue comprise) → INCONNU · ⑤ compter les
      `empreinte_hypothese` distinctes des PREENREGISTREMENT filtrés (les fiches y sont déjà canoniques).
    ⑦ UNITÉ — Des essais.
    ⑧ POURQUOI — L'ORDRE DANS L'HISTOIRE, PAS LES DATES (superviseur R-759, défaut 5) : un rebase, un amend ou un
      cherry-pick changent les dates de commit, pas l'ordre des ancêtres. Un essai refait ne compte qu'une fois.
    ⑨ CE QUI CLOCHE — CE NOMBRE N'EST PAS k (R-505 ⑤, Q-G5 tranchée par Jean-Luc le 05-11-2026 à 13h40 : k compte les
      versions du registre des stratégies, `JUGE_DES_STRATEGIES.k_a_la_date`) ; la question d'y ajouter les essais
      est posée dans la note de B. Les filtres se cumulent (fiche ET famille ET lignée).
    ⑩ EFFET — Lit des fichiers, ou lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if commit is None:
        entrees, defauts = lire_le_registre(racine)
    else:
        sommet, raison = histoire_lisible(racine, branche)
        if sommet is None:
            return "INCONNU", raison
        code, _s = git_de(racine)("merge-base", "--is-ancestor", commit, branche)
        if code != 0:
            return "INCONNU", "le commit %s n'est pas un ancêtre de %s" % (str(commit)[:12], branche)
        histoire = historique_en_ajout_seul(racine, branche)
        if histoire:
            return "INCONNU", "registre des essais réécrit : " + histoire[0]
        fichiers, raison = _registre_au_commit(racine, commit)
        if fichiers is None:
            return "INCONNU", raison
        entrees, defauts = entrees_des_octets(fichiers, racine)
    if defauts:
        return "INCONNU", "registre des essais abîmé : " + defauts[0]
    if fiche_id is not None:
        fiche_id, raison = C.identite_de_la_fiche(racine, fiche_id)
        if fiche_id is None:
            return "INCONNU", raison
    famille_de = None
    if lignee_de is not None:
        lignee, _l, raison = lignee_de_la_fiche(racine, lignee_de, entrees)
        if lignee is None:
            return "INCONNU", "lignée inconnue : " + raison
        famille_de = set(lignee)
    hyp = {e["empreinte_hypothese"] for e in entrees.values()
           if e["nature"] == "PREENREGISTREMENT"
           and (fiche_id is None or e["fiche_id"] == fiche_id)
           and (famille is None or e["famille"] == famille)
           and (famille_de is None or e["fiche_id"] in famille_de)}
    return len(hyp), ""


def _bornes(texte_ou_liste):
    """Lit une période « début..fin » ou [début, fin] en deux dates AAAA-MM-JJ.
    ① RÔLE — Comparer une période essayée aux années d'examen.
    ② CONTEXTE D'APPEL — `regards_sur_les_annees`.
    ③ ENTRÉE — `texte_ou_liste` : « 2000-01-03..2023-12-29 » ou ["2000-01-03", "2023-12-29"].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le couple (début, fin), ou None si illisible.
      [rend: 1]
    ⑥ TRAITEMENT — découper, lire deux dates ISO, exiger début ≤ fin.
    ⑦ UNITÉ — jours.
    ⑧ POURQUOI — les deux formes circulent (contrat DECLARATION_DATEE ; hypothèse du juge).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    from datetime import date
    if isinstance(texte_ou_liste, str):
        morceaux = texte_ou_liste.split("..")
    elif isinstance(texte_ou_liste, (list, tuple)):
        morceaux = list(texte_ou_liste)
    else:
        return None
    if len(morceaux) != 2:
        return None
    try:
        a, b = date.fromisoformat(str(morceaux[0]).strip()), date.fromisoformat(str(morceaux[1]).strip())
    except ValueError:
        return None
    return (a, b) if a <= b else None


def _reglage(racine, cle, domaine):
    """Lit une ligne du fichier des réglages du registre des essais et rend sa valeur si elle est dans le domaine.

    ① RÔLE — La seule lecture de `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv` (R-708) : ce qui se change sans
      réécrire le code.
    ② CONTEXTE D'APPEL — `portee_du_regard`, `calibrage_compte_comme_regard`, `_pousser_l_entree`, `_depot_commun`.
    ③ ENTRÉE — `racine` · `cle` : la clé cherchée · `domaine` : les valeurs dont le code connaît le sens, ou
      ENTIER_POSITIF (un entier ≥ 1 écrit en chiffres), ou ADRESSE (un texte non vide).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la ligne lue, un dictionnaire aux clés EN_TETE_DES_REGLAGES, ou None ; et la raison
      (vide si la ligne est rendue).
      [rend: 2]
    ⑥ TRAITEMENT — ① fichier absent → None · ② en-tête différent de EN_TETE_DES_REGLAGES → None · ③ la clé absente ou
      écrite deux fois → None · ④ une valeur hors du domaine → None · ⑤ rendre la ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un réglage se lit dans un fichier, jamais écrit dans le code (cadre V7, point 4) ; un réglage illisible
      ne se remplace jamais par une valeur par défaut (R-734).
    ⑨ CE QUI CLOCHE — Le fichier n'est pas au contrat de `CONTRATS_DES_FICHIERS.py` (un seul programme le lit) ; une
      fois les choix confirmés par Jean-Luc, leur place est la table de R-505 (R-735).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin = os.path.join(racine, REGLAGES)
    if not os.path.isfile(chemin):
        return None, "réglages du registre des essais absents : %s" % REGLAGES
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f)
        lignes = list(lecteur)
        if lecteur.fieldnames != EN_TETE_DES_REGLAGES:
            return None, "%s : en-tête %r, attendu %r" % (REGLAGES, lecteur.fieldnames, EN_TETE_DES_REGLAGES)
    trouvees = [l for l in lignes if (l.get("cle") or "").strip() == cle]
    if len(trouvees) != 1:
        return None, "%s : la clé %s est écrite %d fois (il en faut une)" % (REGLAGES, cle, len(trouvees))
    ligne = {c: (trouvees[0].get(c) or "").strip() for c in EN_TETE_DES_REGLAGES}
    if domaine == ADRESSE:
        if not ligne["valeur"]:
            return None, "%s : %s vide" % (REGLAGES, cle)
    elif domaine == ENTIER_POSITIF:
        if not (ligne["valeur"].isdigit() and int(ligne["valeur"]) >= 1):
            return None, "%s : %s = %r, hors de %s" % (REGLAGES, cle, ligne["valeur"], ENTIER_POSITIF)
    elif ligne["valeur"] not in domaine:
        return None, "%s : %s = %r, hors de %s" % (REGLAGES, cle, ligne["valeur"], ", ".join(domaine))
    return ligne, ""


def portee_du_regard(racine):
    """Lit sur quelles fiches un regard se compte : « fiche », « lignee » ou « toutes ».

    ① RÔLE — Rendre MODIFIABLE SANS RÉÉCRIRE LE CODE la portée du regard de R-505 ③.
    ② CONTEXTE D'APPEL — `_perimetre_du_regard` ; `bilan_de_la_fiche` ; l'épreuve de B2.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : celles de `_reglage` pour la clé `portee_du_regard` et le domaine PORTEES_DU_REGARD.
      [rend: 2]
    ⑥ TRAITEMENT — `_reglage`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La portée « par lignée déclarée » est la LECTURE DES TEXTES du superviseur R-759 (11-11-2026, 22h19,
      `etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/SUPERVISEUR_LOT_B_TOUR4_Mer_11-11-2026.md`, point
      4), fondée sur n°46 (31-10-2026, 20h48) « la moulinette sur C5 […] dont les versions ne pourront plus compter
      2000-2023 comme jamais vues » et n°61 (01-11-2026, 00h12). CE N'EST PAS UNE DÉCISION EXPLICITE DE JEAN-LUC : à
      confirmer par lui ; d'où un réglage.
    ⑨ CE QUI CLOCHE — Voir `_reglage`.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return _reglage(racine, "portee_du_regard", PORTEES_DU_REGARD)


def calibrage_compte_comme_regard(racine):
    """Lit si un essai de genre CALIBRAGE sur des années d'examen compte comme regard : « oui » ou « non ».

    ① RÔLE — Rendre modifiable sans réécrire le code la réponse à la question J3 (superviseur R-759 du 11-11-2026,
      23h32, section 7).
    ② CONTEXTE D'APPEL — `_regards_dans` (par `regards_sur_les_annees` et `premier_regard`) ; `bilan_de_la_fiche`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : celles de `_reglage` pour la clé `calibrage_compte_comme_regard` et le domaine
      CALIBRAGE_REGARD.
      [rend: 2]
    ⑥ TRAITEMENT — `_reglage`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Lecture la plus stricte, « oui », posée au fichier comme À CONFIRMER : calibrer, c'est choisir des
      réglages « en regardant des années de cours » (R-505, LES MOTS, « Régler », n°62) ; le relecteur de B2 (D3) a
      montré qu'un préfixe « CALIBRAGE: » faisait échapper un essai au compte. Pas une décision de Jean-Luc.
    ⑨ CE QUI CLOCHE — Voir `_reglage`.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return _reglage(racine, "calibrage_compte_comme_regard", CALIBRAGE_REGARD)


def liens_de_la_lignee(texte):
    """Lit le champ `lignee` d'une déclaration datée en liens mère → fille.

    ① RÔLE — La seule lecture du champ `lignee` (contrat DECLARATION_DATEE : « mère → filles, par leurs identifiants au
      registre (C-9) ; « aucune » s'écrit »).
    ② CONTEXTE D'APPEL — `lignee_de_la_fiche` ; l'épreuve de B2.
    ③ ENTRÉE — `texte` : la case `lignee`, par exemple « C5-ETENDU-10 → C5-essai3, C5-essai4 » ou « aucune ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des couples (mère, fille), vide pour « aucune », ou None si le texte est illisible.
      [rend: 1]
    ⑥ TRAITEMENT — ① « aucune » (casse ignorée) → [] · ② couper sur « ; » ; chaque morceau s'écrit « MÈRE → FILLE,
      FILLE… » (flèche « → » ou « -> », une seule par morceau) · ③ un identifiant vide, ou qui porte un espace, une
      virgule ou une flèche, rend le texte illisible · ④ une fiche qui serait sa propre fille rend le texte illisible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contrat nomme le sens (« mère → filles ») sans fixer l'écriture : celle-ci est la plus proche de ses
      mots. Un texte qu'on ne sait pas lire n'est jamais pris pour « aucune » (R-734 : ce qui n'a pas pu se mesurer se
      dit INCONNU).
    ⑨ CE QUI CLOCHE — L'écriture « ; » entre deux morceaux est un choix de B2, pas une décision : à confirmer par le
      Chat, qui écrira la première déclaration (DÉL-D21).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not isinstance(texte, str) or not texte.strip():
        return None
    if texte.strip().lower() == "aucune":
        return []
    liens = []
    for morceau in texte.split(";"):
        m = morceau.replace("->", "→")
        if m.count("→") != 1:
            return None
        mere, filles = (x.strip() for x in m.split("→"))
        ids = [mere] + [f.strip() for f in filles.split(",")]
        if any((not i) or any(c.isspace() for c in i) for i in ids):
            return None
        for f in ids[1:]:
            if f == mere:
                return None
            liens.append((mere, f))
    return liens


def lignee_de_la_fiche(racine, fiche_id, entrees=None):
    """Rend la LIGNÉE d'une fiche : elle-même, sa mère, ses versions, et tout ce qui leur est relié, avec les liens.

    ① RÔLE — Donner la famille sur laquelle se comptent les regards (portée « lignee ») et les essais d'une lignée
      (`nombre_d_essais(lignee_de=…)`).
    ② CONTEXTE D'APPEL — `_perimetre_du_regard`, `nombre_d_essais`, `bilan_de_la_fiche` ; l'épreuve de B2.
    ③ ENTRÉE — `racine` · `fiche_id` : la fiche, sous n'importe quelle écriture que `identite_de_la_fiche` ramène ·
      `entrees` : les entrées saines du registre des essais (fiches canoniques), ou None pour lire le disque.
    ④ CONDITIONS D'ENTRÉE — `donnees/DECLARATIONS_DATEES.csv` et le registre des stratégies sous la racine.
    ⑤ SORTIE — TROIS valeurs : la liste triée des fiches canoniques de la lignée (la fiche comprise), ou None ; la liste
      triée des liens [mère, fille, source] ; la raison (vide si la lignée est rendue).
      [rend: 3]
    ⑥ TRAITEMENT — ① forme canonique de la fiche ; inconnue → None · ② les liens du REGISTRE DES ESSAIS : une entrée
      dont `mere` est l'empreinte d'hypothèse d'un préenregistrement est fille de la fiche de ce préenregistrement ;
      une `mere` qui ne renvoie à aucun préenregistrement → None · ③ les liens DÉCLARÉS : l'UNION des champs `lignee`
      de TOUTES les lignes du fichier des déclarations (`CONTRATS_DES_FICHIERS.declarations_du_fichier`, la seule
      lecture du fichier), chaque identifiant ramené à sa forme canonique ; un champ illisible ou vide, un identifiant
      inconnu, un fichier illisible → None · ④ la composante reliée de la fiche, liens pris dans les deux sens.
    ⑦ UNITÉ — Des identifiants de fiches, canoniques.
    ⑧ POURQUOI — L'UNION de toutes les déclarations, jamais la dernière seule : le fichier ne fait qu'ajouter, et une
      déclaration postérieure « aucune » effaçait le lien (relecteur de B2, D6b ; superviseur R-759 du 11-11-2026,
      23h32, point 4.5). LECTURE DES TEXTES, À CONFIRMER PAR JEAN-LUC (voir `portee_du_regard`) : n°46 et n°61 (mère →
      filles), R-505 ① (« la lignée (mère, filles) » est fixée par la déclaration) ; le sens filles → mère : les années
      où la moulinette essaie des versions sont des années de RÉGLAGE de la lignée (« Régler », n°62), lecture du
      superviseur du tour 4, point 7, Q1. Les sœurs comptent. Le préfixe d'identifiant (« C5-… ») n'est PAS un lien.
    ⑨ CE QUI CLOCHE — ① Une version sans mère déclarée ni `mere` au registre n'appartient à aucune lignée : la lignée
      dépend de ce qui est écrit (relecteur de B2, D6a ; cas réel : C5E10-QA-V1 et C5E10-OBS-V1, « origine » vide).
      ② Une seule déclaration au champ `lignee` illisible rend TOUTE lignée inconnue : côté strict, voulu.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        fiches = C.lire_les_fiches(racine)
    except (OSError, ValueError) as ex:
        return None, [], "registre des stratégies illisible : %s" % ex
    canon, raison = C.identite_de_la_fiche(racine, fiche_id, fiches)
    if canon is None:
        return None, [], raison
    if entrees is None:
        entrees, defauts = lire_le_registre(racine)
        if defauts:
            return None, [], "registre des essais abîmé : " + defauts[0]
    pre = {n: e for n, e in entrees.items() if e["nature"] == "PREENREGISTREMENT"}
    par_empreinte = {}
    for e in pre.values():
        par_empreinte.setdefault(e["empreinte_hypothese"], set()).add(e["fiche_id"])
    liens = set()
    for nom, e in pre.items():
        if e["mere"]:
            if e["mere"] not in par_empreinte:
                return None, [], "entrée %s : mère %s introuvable au registre des essais" % (nom, e["mere"])
            for m in par_empreinte[e["mere"]]:
                if m != e["fiche_id"]:
                    liens.add((m, e["fiche_id"], "registre des essais"))
    try:
        declarations = C.declarations_du_fichier(racine)
    except (OSError, ValueError) as ex:
        return None, [], "déclarations illisibles : %s" % ex
    for decl in declarations:
        lus = liens_de_la_lignee(decl.get("lignee"))
        if lus is None:
            return None, [], "déclaration de %s du %s : lignée illisible %r" % (
                decl["fiche_id"], decl.get("date_declaration"), decl.get("lignee"))
        for m, fi in lus:
            cm, rm = C.identite_de_la_fiche(racine, m, fiches)
            cf, rf = C.identite_de_la_fiche(racine, fi, fiches)
            if cm is None or cf is None:
                return None, [], "déclaration de %s : lignée %r : %s" % (decl["fiche_id"], decl.get("lignee"), rm or rf)
            if cm != cf:
                liens.add((cm, cf, "déclaration de %s du %s" % (decl["fiche_id"], decl.get("date_declaration"))))
    voisins = {}
    for m, fi, _s in liens:
        voisins.setdefault(m, set()).add(fi)
        voisins.setdefault(fi, set()).add(m)
    famille, pile = {canon}, [canon]
    while pile:
        for v in voisins.get(pile.pop(), ()):
            if v not in famille:
                famille.add(v)
                pile.append(v)
    return sorted(famille), sorted([m, fi, s] for m, fi, s in liens if m in famille), ""


def _perimetre_du_regard(racine, fiche_id, entrees):
    """Rend les fiches dont les essais comptent comme regards de `fiche_id` (canonique), selon la portée lue.

    ① RÔLE — Un seul endroit traduit la portée en fiches (R-708).
    ② CONTEXTE D'APPEL — `regards_sur_les_annees` (entrées du disque), `premier_regard` (entrées de la branche).
    ③ ENTRÉE — `racine` · `fiche_id` : canonique · `entrees` : les entrées saines du registre (fiches canoniques).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : un ensemble de fiches canoniques, le mot « toutes », ou None ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — `portee_du_regard` ; « fiche » → {fiche} ; « lignee » → `lignee_de_la_fiche` ; « toutes » → « toutes ».
    ⑦ UNITÉ — Des fiches.
    ⑧ POURQUOI — Voir `portee_du_regard`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    ligne, raison = portee_du_regard(racine)
    if ligne is None:
        return None, raison
    if ligne["valeur"] == "fiche":
        return {fiche_id}, ""
    if ligne["valeur"] == "toutes":
        return "toutes", ""
    famille, _liens, raison = lignee_de_la_fiche(racine, fiche_id, entrees)
    if famille is None:
        return None, "lignée inconnue : " + raison
    return set(famille), ""


def _regards_dans(racine, entrees, examen, perimetre, sauf):
    """Rend les préenregistrements du périmètre dont la période touche les années d'examen.
    ① RÔLE — Le compte des regards, commun au disque et à la branche.
    ② CONTEXTE D'APPEL — `regards_sur_les_annees`, `premier_regard`.
    ③ ENTRÉE — `racine` (pour le réglage du calibrage) · `entrees` (fiches canoniques) · `examen` : (début, fin) ·
      `perimetre` : ensemble de fiches canoniques ou « toutes » · `sauf`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste triée des noms, ou None ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — ① lire `calibrage_compte_comme_regard` (illisible → None) · ② garder les PREENREGISTREMENT du
      périmètre, hors `sauf`, et hors CALIBRAGE si le réglage dit « non » · ③ une période illisible → None · ④ garder
      ceux qui chevauchent, bornes comprises.
    ⑦ UNITÉ — Des entrées ; des jours.
    ⑧ POURQUOI — Une période illisible : on ne sait pas si l'essai a regardé (R-734). Les fiches sont comparées telles
      quelles : elles sont déjà canoniques des deux côtés (forme posée à la lecture).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    calib, raison = calibrage_compte_comme_regard(racine)
    if calib is None:
        return None, raison
    vus = []
    for nom, e in entrees.items():
        if e["nature"] != "PREENREGISTREMENT" or nom in sauf:
            continue
        if perimetre != "toutes" and e["fiche_id"] not in perimetre:
            continue
        if e["genre_d_essai"] == "CALIBRAGE" and calib["valeur"] == "non":
            continue
        p = _bornes(e["hypothese"].get("periode"))
        if p is None:
            return None, "entrée %s : période illisible %r" % (nom, e["hypothese"].get("periode"))
        if p[0] <= examen[1] and examen[0] <= p[1]:
            vus.append(nom)
    return sorted(vus), ""


def regards_sur_les_annees(racine, annees_d_examen, fiche_id, sauf=()):
    """Rend les entrées du registre des essais qui ont DÉJÀ joué une partie des années d'examen, comptées sur la
    PORTÉE lue au fichier des réglages (aujourd'hui : la lignée déclarée de la fiche).

    ① RÔLE — Donner au contrôle ③ de R-505 (« ne regarder qu'une seule fois les années d'examen ») sa SOURCE : le
      registre des essais (superviseur R-759, défaut 4 : « regard unique doit lire le registre des essais »).
    ② CONTEXTE D'APPEL — La porte d'entrée du juge (agent J), juste avant de préenregistrer le jugement (sinon passer
      son nom dans `sauf`) ; sa sortie va dans `grille_de_validation(regards_anterieurs=…)`. `bilan_de_la_fiche`.
      Les épreuves de B2 et du bloc 5a.
    ③ ENTRÉE — `racine` · `annees_d_examen` : « début..fin » · `fiche_id` : la fiche, sous n'importe quelle écriture
      que `identite_de_la_fiche` ramène · `sauf` : des noms d'entrées à ne pas compter.
    ④ CONDITIONS D'ENTRÉE — `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv`, le registre des stratégies et, pour la
      portée « lignee », `donnees/DECLARATIONS_DATEES.csv` sous la racine.
    ⑤ SORTIE — DEUX valeurs : la liste triée des noms d'entrées PREENREGISTREMENT du périmètre dont la période touche
      les années d'examen (bornes comprises ; VIDE = AUCUN REGARD INSCRIT AU REGISTRE, ce qui ne dit rien des regards
      faits avant lui, A-226), ou None si l'on ne sait pas ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — ① forme canonique de la fiche (`CONTRATS_DES_FICHIERS.identite_de_la_fiche`) ; inconnue → None ·
      ② années d'examen illisibles → None · ③ registre abîmé (une entrée au nom inconnu en est un) → None · ④ périmètre
      (`_perimetre_du_regard`) inconnu → None · ⑤ `_regards_dans`.
    ⑦ UNITÉ — Des entrées.
    ⑧ POURQUOI — LE REGARD SE COMPTE SUR LA PORTÉE LUE, PAS DANS LE CODE : la lecture « par lignée déclarée » est celle
      du superviseur R-759 du 11-11-2026 (point 4), fondée sur n°46 et n°61 ; ce n'est PAS une décision explicite de
      Jean-Luc, et le tour 4 du lot B l'avait à tort attribuée à Jean-Luc sous la forme « par fiche ». Les mots « pour
      cette période et cette fiche seulement » (R-505) portent sur l'EXCEPTION des années déjà regardées.
    ⑨ CE QUI CLOCHE — ① Un calcul fait hors du registre n'est pas vu. ② Les regards antérieurs au registre (rejeux de
      C5 sur 2000-2023 du 02-10 et du 28-10-2026, n°26) n'y sont pas : c'est le champ `part_regardee` des déclarations
      qui les porte (voir `bilan_de_la_fiche`).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    connue, raison = C.identite_de_la_fiche(racine, fiche_id)
    if connue is None:
        return None, raison
    examen = _bornes(annees_d_examen)
    if examen is None:
        return None, "années d'examen illisibles : %r" % (annees_d_examen,)
    entrees, defauts = lire_le_registre(racine)
    if defauts:
        return None, "registre des essais abîmé : " + defauts[0]
    perimetre, raison = _perimetre_du_regard(racine, connue, entrees)
    if perimetre is None:
        return None, raison
    return _regards_dans(racine, entrees, examen, perimetre, sauf)


def premier_regard(racine, annees_d_examen, fiche_id):
    """Rend le nom de l'entrée qui a inscrit le PREMIER regard compté pour une fiche sur des années d'examen, dans
    l'ordre de la BRANCHE DES REGARDS (regard compté sur la portée lue, voir `regards_sur_les_annees`).

    ① RÔLE — Donner le « moment du regard » (R-505 ③) et, par le `sommet_principal` de son entrée, l'ANCRE de la
      déclaration datée (`DECLARER_UNE_STRATEGIE.declaration_engagee`).
    ② CONTEXTE D'APPEL — `DECLARER_UNE_STRATEGIE.declaration_engagee` ; les épreuves de B2 et du bloc 5a.
    ③ ENTRÉE — `racine` · `annees_d_examen` : « début..fin » · `fiche_id` : la fiche.
    ④ CONDITIONS D'ENTRÉE — Le dépôt commun joignable ; les réglages et les déclarations sous la racine.
    ⑤ SORTIE — DEUX valeurs : le nom de l'entrée (16 caractères), "" si aucun regard n'est inscrit, ou None si l'on ne
      sait pas ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ fiche connue, années lisibles · ① le registre de la branche des regards (`lire_le_registre` :
      union, ajout seul, fusions refusées), sans défaut · ② le périmètre (`_perimetre_du_regard`) · ③ les regards
      (`_regards_dans`) · ④ pour chacun, le commit qui l'a ajouté sur la branche des regards (`git log --diff-filter=A`)
      · ⑤ le plus ancien dans l'ordre de cette branche (`git rev-list --reverse --topo-order`), jamais par sa date.
    ⑦ UNITÉ — Des entrées.
    ⑧ POURQUOI — Les regards vivent sur la branche des regards depuis la mission REGARD ; les chercher sur la branche
      principale rendait l'ancrage INERTE (superviseur ANCRAGE du 12-11-2026, §1, mesuré). L'ordre des ancêtres, pas
      les dates. La branche des regards n'a aucune fusion (refusée à la lecture) : son histoire est une ligne.
    ⑨ CE QUI CLOCHE — LIMITE J1 (décision de Jean-Luc du 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) »,
      BACKLOG A-708) : protège de l'ERREUR d'agent, pas d'un agent qui tricherait (il a tous les droits sur le dépôt).
    ⑩ EFFET — Lance git (fetch de la branche des regards) ; lit des fichiers.
    ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir.
      [sort: non]
    """
    connue, raison = C.identite_de_la_fiche(racine, fiche_id)
    if connue is None:
        return None, raison
    examen = _bornes(annees_d_examen)
    if examen is None:
        return None, "années d'examen illisibles : %r" % (annees_d_examen,)
    entrees, defauts = lire_le_registre(racine)
    if defauts:
        return None, "registre des essais abîmé : " + defauts[0]
    perimetre, raison = _perimetre_du_regard(racine, connue, entrees)
    if perimetre is None:
        return None, raison
    vus, raison = _regards_dans(racine, entrees, examen, perimetre, ())
    if vus is None:
        return None, raison
    if not vus:
        return "", ""
    suivi = _depot_des_regards()[2]
    git = git_de(racine)
    code, sortie = git("rev-list", "--reverse", "--topo-order", suivi)
    rang = {c: i for i, c in enumerate(sortie.decode().split())}
    ajout = {}
    for nom in vus:
        code, s = git("log", "--format=%H", "--diff-filter=A", suivi, "--", DOSSIER + nom + ".json")
        c = s.decode().split()
        if code != 0 or not c or c[-1] not in rang:
            return None, "commit d'ajout de %s introuvable sur la branche des regards" % nom
        ajout[nom] = rang[c[-1]]
    return min(vus, key=lambda n: (ajout[n], n)), ""


def bilan_de_la_fiche(racine, fiche_id, annees_d_examen, date_declaration=None, temoins=None, sauf=()):
    """Rend, en UN dictionnaire, tout ce que le registre des essais sait d'une fiche : sa lignée, ses regards, ses
    essais, k, et les regards antérieurs DÉCLARÉS par sa lignée.

    ① RÔLE — L'interface que lit la porte d'entrée du juge (agent J, `juger_une_fiche`) : un seul appel, aucune liste
      vide passée par l'appelant (superviseur R-759 du 11-11-2026, tour 4, point 3 ②).
    ② CONTEXTE D'APPEL — La porte d'entrée du juge ; l'épreuve de B2.
    ③ ENTRÉE — `racine` · `fiche_id` : sous n'importe quelle écriture que `identite_de_la_fiche` ramène ·
      `annees_d_examen` : « début..fin » · `date_declaration` : celle de la déclaration retenue
      (AAAA-MM-JJTHH:MM+01:00), ou None · `temoins` : son champ `temoins` (« aucun » ou un entier), ou None · `sauf` :
      des entrées à ne pas compter comme regards (le préenregistrement du jugement lui-même).
    ④ CONDITIONS D'ENTRÉE — Celles de `regards_sur_les_annees` ; pour k, un dépôt git entier (non superficiel).
    ⑤ SORTIE — UNE valeur : un dictionnaire aux clés CLES_DU_BILAN, dans cet ordre :
      `fiche_id` (FORME CANONIQUE, ou l'écriture reçue si elle est inconnue) ; `portee_du_regard` et
      `calibrage_compte_comme_regard` (les lignes des réglages, ou None) ; `lignee` (liste ou None) ; `liens` ([mère,
      fille, source]) ; `regards` (liste ou None) ; `annees_deja_regardees` : « OUI » (un regard inscrit), « AUCUN
      REGARD INSCRIT » (le registre n'en porte aucun ; ne dit rien d'avant le registre) ou « INCONNU » ;
      `parts_regardees_declarees` ({fiche de la lignée : les `part_regardee` DISTINCTS de toutes ses déclarations,
      dans l'ordre du fichier, joints par SEPARATEUR_DES_PARTS}) ; `essais_de_la_fiche`, `essais_de_la_lignee`,
      `essais_du_registre` (entier ou « INCONNU ») ; `k` (le dictionnaire de `JUGE_DES_STRATEGIES.k_a_la_date`, ou
      None) ; `avant_le_registre` (« HISTORIQUE NON COMPTABILISÉ ») ; `raisons` ({clé : raison} de chaque None ou
      INCONNU).
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ forme canonique de la fiche ; INCONNUE → tout le bilan est INCONNU (regards, essais de la fiche
      et de la lignée, lignée, k), avec la raison, et rien d'autre n'est lu · ① les deux réglages · ② `lignee_de_la_fiche`
      · ③ `regards_sur_les_annees` → OUI / AUCUN REGARD INSCRIT / INCONNU · ④ pour chaque fiche de la lignée, les
      `part_regardee` de TOUTES ses lignes (`declarations_du_fichier`) · ⑤ trois comptes par `nombre_d_essais` · ⑥ k
      par `JUGE_DES_STRATEGIES.k_a_la_date` (R-708 : k n'est pas recompté ici) si une date est donnée.
    ⑦ UNITÉ — Des fiches, des entrées, des essais (hypothèses distinctes) ; k en versions du registre des stratégies
      plus les témoins.
    ⑧ POURQUOI — Une fiche inconnue rendait 0 essai et une lignée « elle seule » (relecteur de B2, D2) ; une autre
      écriture perdait la `part_regardee` déclarée (D1). k compte tout le registre des stratégies (n°26, 31-10-2026
      16h05 ; R-505 ⑤, n°82) et n'est PAS le nombre d'essais (Q-G5, 05-11-2026 13h40) : les deux sont rendus côte à
      côte, jamais additionnés. « AUCUN REGARD INSCRIT » et non « NON » : A-226, « NE JAMAIS CONFONDRE « INCONNU » ET
      « ZÉRO » ». Toutes les `part_regardee`, pas la dernière : un regard déclaré une fois reste un regard.
    ⑨ CE QUI CLOCHE — ① `part_regardee` est un texte libre : rendu, pas interprété. ② k hérite des limites de
      `k_a_la_date` (agent A) : ancré par une DATE et lu à HEAD, quand les essais se lisent sur la branche (relecteur de
      B2, « Ce qui tient » ; le contrôle « HEAD contient la branche principale » est à J, superviseur point 1).
    ⑩ EFFET — Lit des fichiers ; lance git en lecture (k).
    ⑪ TERMINAISON — Rend la main ; un appel à git peut ne pas revenir (aucun délai posé).
      [sort: non]
    """
    b = {c: None for c in CLES_DU_BILAN}
    b.update(fiche_id=fiche_id, liens=[], parts_regardees_declarees={}, avant_le_registre=AVANT_LE_REGISTRE,
             raisons={})
    canon, r = C.identite_de_la_fiche(racine, fiche_id)
    if canon is None:
        b.update(annees_deja_regardees="INCONNU", essais_de_la_fiche="INCONNU", essais_de_la_lignee="INCONNU",
                 essais_du_registre="INCONNU")
        for cle in ("fiche_id", "lignee", "regards", "essais_de_la_fiche", "essais_de_la_lignee", "essais_du_registre",
                    "k"):
            b["raisons"][cle] = r
        return b
    b["fiche_id"] = canon
    b["portee_du_regard"], r = portee_du_regard(racine)
    if r:
        b["raisons"]["portee_du_regard"] = r
    b["calibrage_compte_comme_regard"], r = calibrage_compte_comme_regard(racine)
    if r:
        b["raisons"]["calibrage_compte_comme_regard"] = r
    b["lignee"], b["liens"], r = lignee_de_la_fiche(racine, canon)
    if r:
        b["raisons"]["lignee"] = r
    b["regards"], r = regards_sur_les_annees(racine, annees_d_examen, canon, sauf)
    if b["regards"] is None:
        b["annees_deja_regardees"] = "INCONNU"
        b["raisons"]["regards"] = r
    else:
        b["annees_deja_regardees"] = "OUI" if b["regards"] else "AUCUN REGARD INSCRIT"
    if b["lignee"]:
        try:
            for d in C.declarations_du_fichier(racine):
                if d["fiche_id"] in b["lignee"]:
                    parts = b["parts_regardees_declarees"].setdefault(d["fiche_id"], [])
                    if d.get("part_regardee", "") not in parts:
                        parts.append(d.get("part_regardee", ""))
        except (OSError, ValueError) as ex:
            b["raisons"]["parts_regardees_declarees"] = "déclarations illisibles : %s" % ex
        b["parts_regardees_declarees"] = {f: SEPARATEUR_DES_PARTS.join(p)
                                          for f, p in b["parts_regardees_declarees"].items()}
    for cle, kw in (("essais_de_la_fiche", {"fiche_id": canon}), ("essais_de_la_lignee", {"lignee_de": canon}),
                    ("essais_du_registre", {})):
        b[cle], r = nombre_d_essais(racine, **kw)
        if r:
            b["raisons"][cle] = r
    if date_declaration is None:
        b["raisons"]["k"] = "aucune date de déclaration donnée"
    else:
        import JUGE_DES_STRATEGIES as JU
        b["k"], r = JU.k_a_la_date(racine, date_declaration, temoins)
        if r:
            b["raisons"]["k"] = r
    return b


def main(argv):
    """Contrôle le registre des essais d'une racine et affiche le nombre d'essais.
    ① RÔLE — Le contrôle à la main.
    ② CONTEXTE D'APPEL — la ligne de commande.
    ③ ENTRÉE — `argv` : la racine, puis « --branche <nom> » facultatif.
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : 0 sain et compté, 1 défaut (entrée abîmée, histoire réécrite), 2 compte impossible ou
    usage faux.
      [rend: 1]
    ⑥ TRAITEMENT — lire, afficher les défauts, contrôler l'histoire si une branche est donnée, compter.
    ⑦ UNITÉ — essais.
    ⑧ POURQUOI — R-734.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    if not argv or (len(argv) not in (1, 3)) or (len(argv) == 3 and argv[1] != "--branche"):
        print("usage : TENIR_LE_REGISTRE_DES_ESSAIS.py <racine> [--branche origin/main]")
        return 2
    racine = argv[0]
    entrees, defauts = lire_le_registre(racine)
    if len(argv) == 3:
        sommet, raison = histoire_lisible(racine, argv[2])
        if sommet is None:
            print("HISTOIRE :", raison)
            return 2
        defauts += historique_en_ajout_seul(racine, argv[2])
    for d in defauts:
        print("DÉFAUT :", d)
    n, raison = nombre_d_essais(racine)
    print("entrées saines : %d · défauts : %d · essais distincts : %s%s"
          % (len(entrees), len(defauts), n, (" (" + raison + ")") if raison else ""))
    if defauts:
        return 1
    return 2 if n == "INCONNU" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
