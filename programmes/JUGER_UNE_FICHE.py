#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JUGER UNE FICHE — LA porte d'entrée du jugement d'une stratégie par R-505. Simulation uniquement : on rejoue des cours
passés, aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — Le superviseur R-759 du 11-11-2026 (lot B, 3e saisine, rapport
`etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/SUPERVISEUR_LOT_B_TOUR4_Mer_11-11-2026.md`, point 3 ②) :
« écrire UNE seule porte d'entrée `juger_une_fiche(racine, fiche_id, cas)`. Cette porte lira elle-même la déclaration,
le calendrier, le registre des essais (avec la lignée) et k ». La grille de R-505 (`MODULE_JUGEMENT.grille_de_validation`,
GELÉE) ne lit aucun fichier : elle croit ce qu'on lui passe, et une liste vide ne distingue pas « j'ai lu et il n'y a
rien » de « je n'ai pas lu » (point 2 du même rapport). Cette porte est le seul appelant prévu de la grille : elle ne
reçoit AUCUN état de son appelant — ni époques, ni années, ni déclaration, ni regard, ni opérations — et lit tout
elle-même, sous la racine qu'on lui donne.

① RÔLE — `juger_une_fiche` : rendre le verdict de R-505 d'UNE fiche, en lisant elle-même tout ce que la grille croit.
② CONTEXTE D'APPEL — Au 11-11-2026 : l'épreuve `tests/EPREUVES_J_PORTE_D_ENTREE_Mer_11-11-2026.py` seule, sur un
  dépôt fabriqué à vérité connue. Destinée au juge des stratégies (agent A) et au laboratoire. Aucune ligne de
  commande : un jugement est un REGARD (R-505 ③), il ne se lance pas par mégarde.
③ ENTRÉE — Voir `juger_une_fiche`.
④ CONDITIONS D'ENTRÉE — Les programmes voisins (`CONTRATS_DES_FICHIERS`, `MODULE_JUGEMENT`, `JUGE_DES_STRATEGIES`,
  `TENIR_LE_REGISTRE_DES_ESSAIS`, `DECLARER_UNE_STRATEGIE`, `CALENDRIER_DE_LA_BOURSE`) sont dans le même dossier que
  ce fichier ; la racine est un dépôt git complet.
⑤ SORTIE — Voir `juger_une_fiche`.
⑥ TRAITEMENT — Définir les fonctions.
⑦ UNITÉ — Voir chaque fonction.
⑧ POURQUOI — Voir le sens en tête.
⑨ CE QUI CLOCHE — ① Le CODE vient du dossier de ce fichier, les DONNÉES de la racine : jugé sur un autre dépôt que
  celui qui porte ce fichier, le code n'est pas celui de la racine (comme `DECLARER_UNE_STRATEGIE`). ② Six mesures
  n'ont pas encore d'auteur (voir `CONTRATS_DES_FICHIERS.MESUREURS_DU_JUGE`) : tant qu'elles manquent, aucun « Validée » n'est possible, et c'est
  voulu (R-505, règle commune (a) : un contrôle INCONNU empêche la validation). ③ Le verdict n'est pas écrit dans un
  fichier (R-505 ⑫) : c'est le travail du juge.
⑩ EFFET — `juger_une_fiche` INSCRIT deux entrées au registre des essais, sur la BRANCHE DES REGARDS du dépôt distant
  (le préenregistrement de son regard, puis son résultat), quand la déclaration permet de jouer ; rien n'est écrit sur
  le disque de travail (la porte exige un arbre propre) ; le reste lit.
⑪ TERMINAISON — Voir `juger_une_fiche`.
⑫ DÉFINITIONS
  la racine : le dossier d'un dépôt git complet (ou d'un dépôt fabriqué par une épreuve) qui en garde l'arborescence
  la fiche : la dernière ligne d'un identifiant au registre des stratégies `donnees/cac40_strategies.csv`
  la déclaration datée : la ligne de `donnees/DECLARATIONS_DATEES.csv` qui fixe, avant le regard, tout ce qui sera jugé
  le regard : le jeu de la fiche sur ses années d'examen pour la juger (R-505 ③) ; il se préenregistre
  une opération : un achat simulé et sa revente, avec son gain net en euros
"""

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import CALENDRIER_DE_LA_BOURSE as CAL  # noqa: E402
import CONTRATS_DES_FICHIERS as C  # noqa: E402
import DECLARER_UNE_STRATEGIE as D  # noqa: E402
import JUGE_DES_STRATEGIES as JS  # noqa: E402
import MODULE_JUGEMENT as J  # noqa: E402
import TENIR_LE_REGISTRE_DES_ESSAIS as TR  # noqa: E402

PARIS = ZoneInfo("Europe/Paris")
# LE REGISTRE DES RÈGLES, où vit la table « LES SEUILS DE CETTE LOI » de R-505 (instructions du projet, §11 : nom fixe,
# un seul exemplaire) ; la porte la lit SOUS LA RACINE, jamais dans le dossier de ce fichier.
REGISTRE_DES_REGLES = os.path.join("gouvernance", "REGISTRE_REGLES.md")
# LES DEUX MODES DE L'ÉTALON DE HASARD, ceux que `JUGE_DES_STRATEGIES.juger` joue déjà (« l'ACTION au hasard », « les
# DATES au hasard ») ; la liste y est écrite dans le code, pas dans une constante : elle est RÉPÉTÉE ici (⑨ de
# `_hasard`, au BACKLOG). Le plus grand p décide (grille, ⑨ ⑤).
MODES_DU_HASARD = ("valeur", "date")
# LA BRANCHE PRINCIPALE est UNE constante du contrat (`CONTRATS_DES_FICHIERS.BRANCHE_PRINCIPALE`), jamais un paramètre.


def _head_est_la_branche(racine):
    """Dit si le disque jugé EST la branche principale : HEAD au même commit qu'elle, et un arbre de travail propre.

    ① RÔLE — Exiger, une fois, en tête de la porte, que ce qui est jugé soit exactement la version officielle
      (superviseur J du 12-11-2026, réponse 3c : « en tête de la porte : HEAD = `C.BRANCHE_PRINCIPALE`, et `git status
      --porcelain` vide, sinon INCONNU »).
    ② CONTEXTE D'APPEL — `juger_une_fiche`, en tête, avant toute lecture.
    ③ ENTRÉE — `racine` : le dossier du dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : vrai ou faux, et la raison (vide si vrai).
      [rend: 2]
    ⑥ TRAITEMENT — par le lanceur git unique (`TENIR_LE_REGISTRE_DES_ESSAIS.lancer_git`, variables de lieu retirées,
      configuration gardée) : ⓪ `git fetch --quiet --no-tags <distant> refs/heads/<branche>:refs/remotes/<distant>/
      <branche>`, distant et branche lus dans `C.BRANCHE_PRINCIPALE`, refspec étroite SANS « + » ; échec → faux (on
      ferme, jamais on continue) · ① `git rev-parse HEAD` et `git rev-parse <branche principale>` : deux commits lisibles et ÉGAUX · ② `git status
      --porcelain` : vide (ni fichier modifié, ni fichier non suivi hors de `.gitignore`). Tout échec → faux.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le regard unique ne se dépense que si le disque jugé EST la branche principale DISTANTE au moment du
      regard : un poste en retard dépensait le regard sur une déclaration périmée (relecteur REGARD tour 3, T3-D1 ;
      superviseur POSTE EN RETARD, DE FOND : retour à la spécification « après fetch » du superviseur ANCRAGE). Un
      fetch en échec ferme : le regard exige le réseau de toute façon, et INCONNU ne dépense aucun regard. D'un même geste (superviseur J, réponse 3c) : un commit antidaté au-dessus de la branche ne choisit
      plus k ni la loi (relecteur J, D2, attaque A3) ; une table, un module ou un cours modifiés sur le disque ne sont
      plus jugés (D5) ; la fenêtre et la loi lues SONT celles de la branche (M3 de GITHUB). La porte n'écrit plus rien
      sur le disque (le regard est poussé sur la branche des regards) : la condition est tenable. « Contient la
      branche » (l'ancienne condition) laissait passer les commits posés au-dessus.
    ⑨ CE QUI CLOCHE — ① Fenêtre résiduelle, hors J1 : un autre poste qui pousse sur la branche principale ENTRE ce
      fetch et le préenregistrement du regard (quelques secondes) ; `sommet_principal` reste pris sans fetch, il égale
      alors le HEAD jugé (superviseur POSTE EN RETARD du 12-11-2026). ② Une branche `travail-*` ne peut plus être
      jugée : c'est voulu pour un vrai regard ; les épreuves fabriquent leur branche principale. ③ Un appelant du même
      processus peut réassigner `C.BRANCHE_PRINCIPALE` ou remplacer cette fonction : limite J1 (décidée par Jean-Luc le 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708),
      écrite, non défendue.
    ⑩ EFFET — Lance git en RÉSEAU (fetch de la seule branche principale ; met à jour sa référence de suivi), puis en
      lecture.
    ⑪ TERMINAISON — Rend la main ; git peut ne pas revenir (réseau, aucun délai posé).
      [sort: non]
    """
    distant, branche = C.BRANCHE_PRINCIPALE.split("/", 1)
    code, _s, err = TR.lancer_git(racine, ["fetch", "--quiet", "--no-tags", distant,
                                           "refs/heads/%s:refs/remotes/%s/%s" % (branche, distant, branche)])
    if code != 0:
        return False, "branche principale non récupérée (fetch code %d %s) : on ne juge pas une version peut-être en " \
                      "retard" % (code, err.strip()[:120])
    shas = []
    for ref in ("HEAD", C.BRANCHE_PRINCIPALE):
        code, sortie, err = TR.lancer_git(racine, ["rev-parse", "--verify", "--quiet", ref + "^{commit}"])
        if code != 0:
            return False, "%s illisible (git rev-parse : code %d %s)" % (ref, code, err.strip()[:120])
        shas.append(sortie.decode().strip())
    if shas[0] != shas[1]:
        return False, "HEAD (%s) n'est pas %s (%s) : seule la branche principale se juge" % (
            shas[0][:12], C.BRANCHE_PRINCIPALE, shas[1][:12])
    code, sortie, err = TR.lancer_git(racine, ["status", "--porcelain"])
    if code != 0:
        return False, "git status illisible (code %d %s)" % (code, err.strip()[:120])
    if sortie.strip():
        return False, "arbre de travail non propre : %s" % sortie.decode("utf-8", "replace").strip()[:160]
    return True, ""


def _kelly(racine, fiche, ops):
    """Mesure le Kelly entier de R-505 ⑨ sur les gains réels nets des opérations jouées.

    ① RÔLE — Donner à la grille la mesure `kelly` du contrat (DETAILS_DES_CONTROLES["kelly"] : « le Kelly entier, sur
      les gains réels nets », lot S_kk), que personne n'écrit encore.
    ② CONTEXTE D'APPEL — `juger_une_fiche`, par `CONTRATS_DES_FICHIERS.MESUREURS_DU_JUGE` (« JUGER_UNE_FICHE._kelly »),
      une fois.
    ③ ENTRÉE — `racine` : la racine · `fiche` : la fiche (non lue ici) · `ops` : les opérations jouées (`net` en euros).
    ④ CONDITIONS D'ENTRÉE — `ops` non vide.
    ⑤ SORTIE — DEUX valeurs : la mesure {kelly, gain_moyen_net_eur} ou None, et la raison (vide si mesurée).
      [rend: 2]
    ⑥ TRAITEMENT — ① charger le module de statistiques de la racine (`trouver`, comme `JUGE_DES_STRATEGIES.main`) ·
      ② taux de réussite, gain moyen des gagnantes, perte moyenne des perdantes · ③ `calculer_kelly_fractionnel`
      avec ces deux moyennes à la place de l'objectif et du stop, sans frais (ils sont déjà dans `net`) et sans
      fraction (1 : le Kelly ENTIER) · ④ rendre `kelly_brut`.
    ⑦ UNITÉ — Kelly : fraction du capital ; gain moyen : euros.
    ⑧ POURQUOI — R-708 : la formule existe (`MODULE_STATISTIQUES.calculer_kelly_fractionnel`, (p × b − q) ÷ b) ; elle
      prend un rapport gain ÷ perte, que les moyennes réelles donnent sans la réécrire.
    ⑨ CE QUI CLOCHE — ① Lecture de J : « gains réels » lus comme les moyennes des gagnantes et des perdantes ; à
      confirmer (le lot S_kk n'a rien écrit). ② Sans aucune perte, la formule refuse (perte nulle) : INCONNU, jamais
      1. ③ `kelly_brut` est arrondi à 4 décimales par la fonction réutilisée.
    ⑩ EFFET — Charge (exécute) le module de statistiques de la racine.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not ops:
        return None, "aucune opération"
    f_sta = JS.trouver(racine, "MODULE_STATISTIQUES")
    if not f_sta:
        return None, "module de statistiques introuvable sous la racine"
    S = JS.charger_module(f_sta, "sta_porte")
    gains = [o["net"] for o in ops]
    gagnes, perdus = [g for g in gains if g > 0], [-g for g in gains if g <= 0]
    if not gagnes or not perdus:
        return None, "Kelly incalculable : %d gagnante(s), %d perdante(s)" % (len(gagnes), len(perdus))
    r = S.calculer_kelly_fractionnel(100.0 * len(gagnes) / len(gains), sum(gagnes) / len(gagnes),
                                     sum(perdus) / len(perdus), 0.0, fraction=1.0)
    if r.get("erreur"):
        return None, "Kelly : " + r["erreur"]
    return {"kelly": r["kelly_brut"], "gain_moyen_net_eur": sum(gains) / len(gains)}, ""


def _mesureurs():
    """Rend les mesureurs DÉCLARÉS au contrat, résolus en fonctions : {clé : fonction ou None}, et leurs raisons.

    ① RÔLE — Lire `CONTRATS_DES_FICHIERS.MESUREURS_DU_JUGE` (qui prend quelle mesure de la grille), sans le muter.
    ② CONTEXTE D'APPEL — `juger_une_fiche`, une fois, après le jeu.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Les modules nommés sont dans le dossier de ce fichier (sys.path).
    ⑤ SORTIE — DEUX valeurs : {clé : fonction} pour les mesureurs résolus ; {clé : raison} pour ceux dont le nom ne
      se résout pas (les mesures sans auteur n'y sont pas : la grille les nomme).
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque clé du contrat : None → sautée ; « MODULE.fonction » → importer le module et
      prendre la fonction ; échec → la raison.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecteur J, D4 : le dictionnaire global de la porte était le canal par lequel un appelant faussait
      une mesure, et le SEUL chemin vers « Validée ». Déclarés au contrat, les mesureurs se branchent par un commit
      qui se relit (superviseur J, réponse 3d). Une copie neuve à chaque appel : la porte ne garde aucun état.
    ⑨ CE QUI CLOCHE — Ce n'est pas une défense : un appelant du même processus peut réassigner le dictionnaire du
      contrat (superviseur J, M4 ; limite J1, décidée par Jean-Luc le 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708).
    ⑩ EFFET — Importe les modules nommés (exécute leur code au premier import).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import importlib
    fonctions, raisons = {}, {}
    for cle, nom in dict(C.MESUREURS_DU_JUGE).items():
        if nom is None:
            continue                    # sans auteur : la grille rend le contrôle INCONNU et le nomme
        module, _p, fonction = str(nom).rpartition(".")
        try:
            fonctions[cle] = getattr(sys.modules.get(module) or importlib.import_module(module), fonction)
        except (ImportError, AttributeError, ValueError) as e:
            raisons[cle] = "mesureur %r introuvable : %s" % (nom, e)
    return fonctions, raisons


def _maintenant():
    """Rend l'instant présent, heure de Paris, en ISO avec son décalage.
    ① RÔLE — Dater le regard.
    ② CONTEXTE D'APPEL — `juger_une_fiche`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « AAAA-MM-JJTHH:MM:SS+01:00 ».
      [rend: 1]
    ⑥ TRAITEMENT — lire l'horloge.
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — `lire_la_declaration` exige un instant avec décalage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    return datetime.now(PARIS).isoformat(timespec="seconds")


def _periodes_regardees(texte):
    """Lit le champ `part_regardee` de la déclaration en une liste de périodes (début, fin).

    ① RÔLE — Dire quelles années ont déjà été vues, selon la déclaration elle-même (CHAMPS_P0, `part_regardee` :
      « chaque période dont un résultat a été vu, avec la date du regard ; « aucune » s'écrit »).
    ② CONTEXTE D'APPEL — `_seances_hors_examen`, une fois par fiche de la lignée.
    ③ ENTRÉE — `texte` : la case telle qu'écrite.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des couples de dates (vide pour « aucune »), ou None ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — ① « aucune » (casse et blancs ignorés) → [] · ② sinon relever chaque « AAAA-MM-JJ..AAAA-MM-JJ » et la
      lire par `TENIR_LE_REGISTRE_DES_ESSAIS._bornes` (la lecture des périodes du registre des essais, R-708) ·
      ③ aucune période lisible → None.
    ⑦ UNITÉ — Des jours.
    ⑧ POURQUOI — R-505, l'exception : « par défaut, une période dont un résultat a été vu ne prouve rien ».
    ⑨ CE QUI CLOCHE — ① Un texte libre sans période écrite « début..fin » (l'exemple du contrat, « 2000-2023, rejeu du
      28-10 ») rend None, donc INCONNU : plus strict, jamais plus large. ② `_bornes` est une fonction privée du
      registre des essais.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import re
    t = (texte or "").strip()
    if t.lower() == "aucune":
        return [], ""
    periodes = [TR._bornes(m) for m in re.findall(r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}", t)]
    if not periodes or any(p is None for p in periodes):
        return None, "part_regardee sans période lisible « début..fin » : %r" % (t[:80],)
    return periodes, ""


def _seances_hors_examen(ops, decl, seances_d_examen, parts):
    """Compte les séances des opérations jugées qui ne sont pas des séances d'années jamais vues (R-505 ②).

    ① RÔLE — Donner à la grille `seances_hors_examen`, CALCULÉ sur les opérations (superviseur, point 3 ②), au lieu
      d'un zéro reçu.
    ② CONTEXTE D'APPEL — `juger_une_fiche`, une fois, après le jeu.
    ③ ENTRÉE — `ops` : les opérations jouées (`date_entree`, `date_sortie`, AAAA-MM-JJ) · `decl` : la déclaration
      engagée · `seances_d_examen` : les séances du calendrier des années d'examen (textes AAAA-MM-JJ) · `parts` : les
      champs `part_regardee` de la fiche et de toute sa lignée (bilan de B2), ou None si la lignée est inconnue.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le nombre (entier ≥ 0) ou None, et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — Une séance d'achat ou de vente compte si ① elle n'est pas une séance d'examen du calendrier, ou
      ② elle tombe dans les années de réglage (`periode_conception`), ou ③ dans une période déjà regardée par la fiche
      OU sa lignée (`part_regardee` de chacune ; superviseur R-759, point 4 : le regard se compte sur la lignée). Une case illisible → None. L'exception « regard sans décision » n'est pas appliquée ici :
      une déclaration qui la porte rend None (voir ⑨).
    ⑦ UNITÉ — Des séances (une opération en apporte deux : son achat et sa vente).
    ⑧ POURQUOI — R-505 ② : « Refuser toute séance qui n'est pas une année d'examen » ; LE PRINCIPE : « une stratégie
      ne se prouve jamais sur les années qui ont servi à la trouver ou à la régler ». La VENTE compte : une opération
      revendue après la fin des années d'examen n'était vue ni par ② ni par ⑦ (note de B, tour 4, passe ①).
    ⑨ CE QUI CLOCHE — ① L'exception de R-505 (« une déclaration écrite et datée de Jean-Luc, pour une période et une
      fiche qu'elle nomme ») ne se lit pas par programme dans le champ `regard_sans_decision` d'aujourd'hui : la porte
      rend INCONNU plutôt que de l'appliquer ou de l'ignorer — question pour Jean-Luc (note J). Pour C5 (n°26), cela
      veut dire INCONNU tant que le champ n'a pas de forme lisible. ② La vente comptée hors examen est une lecture de
      J (la plus stricte) : à confirmer.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    from datetime import date
    if seances_d_examen is None:
        return None, "calendrier des années d'examen non lu"
    if (decl.get("regard_sans_decision") or "").strip():
        return None, ("exception « regard sans décision » déclarée : la porte ne sait pas la lire par programme "
                      "(question pour Jean-Luc)")
    reglage = TR._bornes((decl.get("periode_conception") or "").strip())
    if reglage is None:
        return None, "periode_conception illisible : %r" % (decl.get("periode_conception"),)
    if parts is None:
        return None, "lignée inconnue : les parts déjà regardées de la lignée ne sont pas lues"
    vues = []
    for texte in parts:
        v, raison = _periodes_regardees(texte)
        if v is None:
            return None, raison
        vues += v
    examen = set(seances_d_examen)
    interdites = [reglage] + vues
    n = 0
    for o in ops:
        for cle in ("date_entree", "date_sortie"):
            d = o.get(cle)
            if d not in examen or any(a <= date.fromisoformat(d) <= b for a, b in interdites):
                n += 1
    return n, ""


def _jouer_les_annees_d_examen(racine, fiche, bornes, recu):
    """Rejoue la fiche sur ses années d'examen, avec les lecteurs mêmes du juge des stratégies.

    ① RÔLE — Produire les opérations jugées, sans jamais les recevoir d'un appelant.
    ② CONTEXTE D'APPEL — `juger_une_fiche`, une fois, après le préenregistrement du regard.
    ③ ENTRÉE — `racine` · `fiche` : la fiche lue au registre · `bornes` : (début, fin) des années d'examen, en dates ·
      `recu` : (racine, nom du préenregistrement poussé) — le reçu que `jouer` exige dans la fenêtre du regard unique.
    ④ CONDITIONS D'ENTRÉE — Celles de `JUGE_DES_STRATEGIES.main` : cours maître, référentiel et module de positions
      sous la racine.
    ⑤ SORTIE — DEUX valeurs : un dictionnaire {ops, cours, lecture, mnemo, mod_pos, tp, sl, h, univ, periode, recu} ou
      None, et la raison (vide si joué).
      [rend: 2]
    ⑥ TRAITEMENT — ① `porte_0` (fiche incomplète → None) · ② cours par `lire_par_le_lecteur` sur `fichiers_de_cours`
      (le maître, A-442) · ③ module de positions par `trouver` · ④ signal par `signal_de_la_fiche` · ⑤ `jouer` avec
      la période des années d'examen · ⑥ une valeur demandée absente des cours → None (alerte d'identité) ·
      ⑦ univers du hasard comme `juger` (valeurs de la fiche présentes dans les cours).
    ⑦ UNITÉ — Seuils en fractions, horizon en séances, gains en euros.
    ⑧ POURQUOI — R-708 : jouer comme le juge, par ses fonctions, sinon la porte et le juge divergent.
    ⑨ CE QUI CLOCHE — ① La période passée à `jouer` filtre la date du SIGNAL ; l'achat (lendemain) et la vente peuvent
      sortir des années d'examen : `_seances_hors_examen` les compte. ② Le calibrage du juge (`calibrer`) n'est pas
      rejoué ici.
    ⑩ EFFET — Lit des fichiers ; exécute le module de positions et le module de signal nommé par la fiche.
    ⑪ TERMINAISON — Rend la main ; `jouer` et le signal exécutent du code tiers non borné.
      [sort: non]
    """
    ok, manq, _b = (JS.porte_0(fiche) + (None,))[:3]
    if not ok:
        return None, "fiche refusée à la porte 0 : " + ", ".join(manq)
    mnemo = JS.table_mnemoniques(JS.trouver(racine, "REFERENTIEL_VALEURS"))
    f_cours = JS.fichiers_de_cours(racine)[0]
    cours, lecture = JS.lire_par_le_lecteur(racine, os.path.relpath(f_cours, racine), mnemo)
    f_pos = JS.trouver(racine, "MODULE_POSITIONS.py")
    if not f_pos:
        return None, "module de positions introuvable sous la racine"
    mod_pos = JS.charger_module(f_pos, "pos_porte")
    signal = JS.signal_de_la_fiche(racine, fiche)
    periode = (bornes[0].isoformat(), bornes[1].isoformat())
    ops, inconnus = JS.jouer(fiche, cours, mnemo, signal, mod_pos, periode=periode, lecture=lecture, recu=recu)
    if inconnus:
        return None, "valeur(s) de la fiche absente(s) des cours : %s (identité des valeurs)" % ", ".join(inconnus)
    tp, sl = JS.seuil_de_la_fiche(fiche, "tp"), JS.seuil_de_la_fiche(fiche, "sl")
    h = JS.lire_horizon_ou_aucune(fiche["horizon"])
    univ = [mnemo.get(m, JS.cle_valeur(m)) for m in JS.mnemoniques_de_l_univers(fiche["univers"])]
    return {"ops": ops, "cours": cours, "lecture": lecture, "mnemo": mnemo, "mod_pos": mod_pos, "tp": tp, "sl": sl,
            "h": h, "univ": [v for v in univ if v in cours], "periode": periode, "recu": recu}, ""


def _hasard(jeu, s_hasard):
    """Joue l'étalon de hasard de R-505 ⑥ avec assez de tirages pour que 1 ÷ tirages passe sous le seuil.

    ① RÔLE — Donner à la grille sa liste `hasard` (un rendu d'`etalon_hasard` par mode).
    ② CONTEXTE D'APPEL — `juger_une_fiche`, une fois.
    ③ ENTRÉE — `jeu` : le rendu de `_jouer_les_annees_d_examen` · `s_hasard` : le seuil du hasard LU à la table
      (`seuil_de_la_loi`), sans unité.
    ④ CONDITIONS D'ENTRÉE — `s_hasard` dans ]0, 1].
    ⑤ SORTIE — UNE valeur : la liste des rendus, un par mode de MODES_DU_HASARD.
      [rend: 1]
    ⑥ TRAITEMENT — ① tirages = la partie entière de 1 ÷ seuil, plus un (le plus petit nombre dont l'inverse est sous
      le seuil) · ② pour chaque mode, `etalon_hasard` avec l'achat et l'admission du juge (`jouer_une_entree`,
      `achat_admis`) et la période des années d'examen, comme `JUGE_DES_STRATEGIES.juger`.
    ⑦ UNITÉ — Des tirages ; des euros.
    ⑧ POURQUOI — R-505 ⑥ : « Il faut assez de tirages pour que 1 ÷ (nombre de tirages) passe sous le seuil, sinon le
      contrôle est INCONNU » (DÉL-D38) : le nombre se CALCULE depuis le seuil, il ne s'écrit pas.
    ⑨ CE QUI CLOCHE — ① MODES_DU_HASARD répète la liste écrite dans `juger` (deux écritures : BACKLOG). ② Pour k = 69,
      0,05 ÷ 69 donne 1 381 tirages par mode : long sur les vraies données (non mesuré ici).
    ⑩ EFFET — Exécute le module de positions.
    ⑪ TERMINAISON — Rend la main ; le nombre de tirages est borné par le seuil.
      [sort: non]
    """
    n = int(1.0 / s_hasard) + 1
    cours, lecture, mod_pos = jeu["cours"], jeu["lecture"], jeu["mod_pos"]
    tp, sl, h = jeu["tp"], jeu["sl"], jeu["h"]
    rendus = []
    for mode in MODES_DU_HASARD:
        rendus.append(J.etalon_hasard(
            jeu["ops"], cours, jeu["univ"], tp, sl, h, mod_pos, mode=mode, n_tirages=n,
            entree=lambda v, j: JS.jouer_une_entree(v, cours[v], j, tp, sl, h, mod_pos, lecture, None, jeu["recu"]),
            admis=lambda v, j: JS.achat_admis(v, cours[v], j, lecture), periode=jeu["periode"]))
    return rendus


def juger_une_fiche(racine, fiche_id, cas):
    """Rend le verdict de R-505 d'une fiche, en lisant ELLE-MÊME tout ce que la grille croit.

    ① RÔLE — LA porte d'entrée du jugement (superviseur R-759 du 11-11-2026, lot B, point 3 ②). Elle lit la fiche, la
      déclaration engagée, k, la table de la loi, le calendrier, le registre des essais ; elle préenregistre son
      regard, joue la fiche sur ses années d'examen, mesure, appelle la grille gelée, et inscrit le résultat.
    ② CONTEXTE D'APPEL — L'épreuve de J (dépôt à vérité connue). Destinée au juge des stratégies et au laboratoire.
    ③ ENTRÉE — `racine` : un dépôt git complet · `fiche_id` : l'identifiant au registre des stratégies, tel qu'écrit ·
      `cas` : « 1 » ou « 2 », le cas de R-505 que l'appelant croit juger ; il n'est CRU que s'il est celui de la
      déclaration (la déclaration fixe le cas : contrat DECLARATION_DATEE, champ `cas`).
    ④ CONDITIONS D'ENTRÉE — La fiche existe au registre (sinon LookupError) ; la table de la loi est lisible au
      registre des règles de la racine (sinon ValueError de `table_de_la_loi` ; un registre ABSENT rend INCONNU) ;
      HEAD est la branche principale et l'arbre est propre (sinon INCONNU) ; le dépôt distant joignable (le regard se
      pousse avant le jeu ; sinon RuntimeError de l'inscription, et rien n'est joué).
    ⑤ SORTIE — UNE valeur : le rendu de `grille_de_validation` (six clés : verdict, motif, premier_controle_bloquant,
      seuil_de_preuve, seuil_du_hasard, controles), plus `lu` : ce que la porte a lu et pourquoi elle s'est arrêtée
      ({fiche_id, cas_declare, declaration : le rendu de `lire_la_declaration`, k, regard, bilan : celui de B2, raisons}).
      [rend: 1]
    ⑥ TRAITEMENT — ① HEAD = la branche principale du contrat et arbre propre (`_head_est_la_branche`), sinon tout
      INCONNU (table vide, `cas=None`), et rien n'est lu ni joué · ①bis le registre des règles absent → tout INCONNU
      (relecteur J, D8) · ①ter la table de la loi et la fiche · ② la déclaration, par `DECLARER_UNE_STRATEGIE.lire_la_declaration`
      (B3) : COMPLETE → on continue ; NON_JUGEABLE (absente, incomplète, non engagée avant le premier regard, empreinte
      du code changée) → NON JUGEABLE avec ses champs ; ILLISIBLE → contrôle ① INCONNU ; dans ces deux cas RIEN n'est
      joué (aucun regard sans déclaration) · ③ le cas : celui de la déclaration ; l'appelant en dit un autre → cas inconnu ·
      ⑤ les séances d'examen au calendrier (`seances_entre`) · ⑥ PRÉENREGISTRER le regard · ④ puis le BILAN de B2
      (`bilan_de_la_fiche`, en s'excluant par `sauf`) : k à la date de la déclaration, regards de la lignée, parts
      déjà regardées déclarées par la lignée · ⑦ jouer ·
      ⑧ séances hors examen, point mort, hasard, mesures externes des mesureurs du contrat (`_mesureurs`) · ⑨ la grille · ⑩ inscrire le
      résultat (ou l'échec, puis relever l'erreur).
    ⑦ UNITÉ — Celles de la grille : probabilités sans unité, point mort en POURCENTS, gains en EUROS.
    ⑧ POURQUOI — Point 2 du superviseur : une liste vide reçue ne distingue pas « lu et rien » de « pas lu ». Ici,
      chaque entrée de la grille est soit LUE par la porte, soit None avec sa raison (INCONNU) — jamais une valeur
      d'appelant. Le regard est préenregistré AVANT le jeu (A-226 : « même une expérience sans résultat est
      enregistrée ») : un second jugement des mêmes années voit le premier.
    ⑨ CE QUI CLOCHE — ① Le barème est celui des verdicts (`bareme=None`, comme `juger`) : le champ `bareme` de la
      déclaration n'est pas confronté (BACKLOG). ② La lignée se lit chez B2 (portée au fichier
      `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv`) : la porte ne lui passe que la fiche, les années, la date, les
      témoins et son propre regard. ③ Un appel qui
      lève APRÈS le préenregistrement laisse un regard inscrit avec son échec : c'est voulu (A-226). ④ LIMITE (e) DU
      SUPERVISEUR J, ÉCRITE ET NON DÉFENDUE : un appelant du même processus qui réassigne `C.BRANCHE_PRINCIPALE`,
      remplace une fonction, mute `C.MESUREURS_DU_JUGE` ou calcule à la main passe outre (M4) — périmètre « erreur
      d'agent, pas faussaire » (J1, décidée par Jean-Luc le 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708). ⑤ Deux jugements
      simultanés du même périmètre se BLOQUENT l'un l'autre (chacun voit le regard de l'autre) : le côté strict.
    ⑩ EFFET — Inscrit et POUSSE deux entrées sur la branche des regards quand la déclaration permet de jouer (aucun
      fichier du disque) ; lance git ; exécute les modules de positions, de statistiques et de signal.
    ⑪ TERMINAISON — Rend la main, ou lève (LookupError, ValueError, et ce que lèvent les lecteurs du juge) ; git et le
      module de signal peuvent ne pas revenir.
      [sort: non]
    """
    maintenant = _maintenant()
    raisons = {}
    lu = {"fiche_id": fiche_id, "cas_declare": None, "declaration": None, "k": None, "regard": None,
          "raisons": raisons}
    table = {}      # vide tant qu'elle n'est pas lue : la grille rend alors chaque contrôle INCONNU

    def rendre(**entrees):
        """Appelle la grille gelée et joint ce que la porte a lu.
        ① RÔLE — Un seul appel de la grille.
        ② CONTEXTE D'APPEL — `juger_une_fiche`, à chacune de ses sorties.
        ③ ENTRÉE — `**entrees` : les entrées nommées de `grille_de_validation`, sauf la table.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le rendu de la grille, avec la clé `lu`.
          [rend: 1]
        ⑥ TRAITEMENT — appeler, joindre.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un seul endroit appelle la grille.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]"""
        r = J.grille_de_validation(table, **entrees)
        r["lu"] = lu
        return r

    # ①bis LE DISQUE EST LA BRANCHE PRINCIPALE (HEAD au même commit, arbre propre), sinon tout le jugement est INCONNU,
    # rien n'est lu ni joué (superviseur J du 12-11-2026, réponse 3c). Aux sorties anticipées, `cas=None` : le cas de
    # l'appelant n'est cru que s'il égale la déclaration, jamais avant de l'avoir lue (relecteur J, D7).
    est, r_branche = _head_est_la_branche(racine)
    if not est:
        raisons["branche"] = r_branche
        return rendre(cas=None, k="INCONNU", declaration_manquants=None)
    # ①ter LA TABLE DE LA LOI : un registre des règles ABSENT rend tout INCONNU (relecteur J, D8 : il levait
    # FileNotFoundError) ; une table illisible lève toujours ValueError (④).
    chemin_loi = os.path.join(racine, REGISTRE_DES_REGLES)
    if not os.path.isfile(chemin_loi):
        raisons["table"] = "registre des règles absent : %s" % REGISTRE_DES_REGLES
        return rendre(cas=None, k="INCONNU", declaration_manquants=None)
    with open(chemin_loi, encoding="utf-8") as f:
        table.update(J.table_de_la_loi(f.read()))
    fiches = C.lire_les_fiches(racine)
    if fiche_id not in fiches:
        raise LookupError("fiche %r absente du registre des stratégies" % (fiche_id,))
    fiche = fiches[fiche_id]
    # ② LA DÉCLARATION : la lecture CONTRÔLÉE de B3 (`lire_la_declaration`) — champs en défaut calculés, empreintes du
    # code recalculées ; rien n'est joué sinon. L'ancrage par l'historique git est GARDÉ ET RÉPARÉ (décision de
    # Jean-Luc du 12-11-2026 à 09h04, « Reparer ») : la branche est lue dedans, l'instant est l'horloge de la porte.
    lecture = D.lire_la_declaration(racine, fiche_id, maintenant)
    decl = lecture["declaration"]
    lu["declaration"] = lecture
    if lecture["etat"] != C.ETATS_DE_LA_LECTURE_DE_LA_DECLARATION[0]:
        raisons["declaration"] = " ; ".join(lecture["raisons"])
        return rendre(cas=None, k="INCONNU", declaration_manquants=lecture["champs_en_defaut"])
    # ③ LE CAS : la déclaration le fixe
    lu["cas_declare"] = decl["cas"].strip()
    cas_retenu = lu["cas_declare"] if str(cas).strip() == lu["cas_declare"] else None
    if cas_retenu is None:
        raisons["cas"] = "l'appelant dit cas %r, la déclaration dit %r" % (cas, lu["cas_declare"])
    # ⑤ LES SÉANCES D'EXAMEN, AU CALENDRIER
    bornes = TR._bornes(decl["annees_d_examen"])
    seances_d_examen = None
    if bornes is None:
        raisons["annees_d_examen"] = "années d'examen illisibles : %r" % (decl["annees_d_examen"],)
    else:
        try:
            sc = CAL.lire_les_seances(racine)
            seances_d_examen = [d.isoformat() for d, _etat in CAL.seances_entre(bornes[0], bornes[1], sc)]
        except Exception as e:      # HorsCalendrier, fichier absent : le calendrier n'est pas lu, la grille le dira
            raisons["calendrier"] = "%s : %s" % (type(e).__name__, e)
    entrees = dict(cas=cas_retenu, k="INCONNU", declaration_manquants=[], epoques_declarees=decl["epoques"],
                   annees_d_examen=decl["annees_d_examen"], seances_d_examen=seances_d_examen)
    if bornes is None:
        return rendre(**entrees)
    # ⑥ LE REGARD : préenregistré AVANT le jeu, puis les regards antérieurs de cette fiche, lui excepté
    module, fonction, reglages = JS.declaration_du_signal(fiche)
    hypothese = {"tp_pct": fiche["tp"], "sl_pct": fiche["sl"], "horizon": fiche["horizon"],
                 "univers": fiche["univers"], "signal": " · ".join((module, fonction, reglages)),
                 "periode": decl["annees_d_examen"], "bareme": decl["bareme"]}
    nom = TR.preenregistrer(racine, fiche_id, hypothese, declaration=decl)
    lu["regard"] = nom
    try:
        # ④ LE BILAN DU REGISTRE DES ESSAIS (B2) : k à la date de la déclaration, regards de la LIGNÉE, parts déclarées
        bilan = TR.bilan_de_la_fiche(racine, fiche_id, decl["annees_d_examen"], decl["date_declaration"],
                                     decl["temoins"], sauf=(nom,))
        lu["bilan"], lu["k"] = bilan, bilan["k"]
        raisons.update({"bilan " + c: r for c, r in bilan["raisons"].items()})
        k = (bilan["k"] or {}).get("valeur", "INCONNU")
        entrees["k"] = k
        entrees["regards_anterieurs"] = bilan["regards"]
        parts = (None if bilan["lignee"] is None
                 else [decl["part_regardee"]] + list(bilan["parts_regardees_declarees"].values()))
        # ⑦ LE JEU. POINT DE BRANCHEMENT ② (règle figée, J2, en attente de Jean-Luc) : si la photographie est retenue,
        # c'est ICI que la trace de ce que le jeu lit (fichiers ouverts, colonnes de la fiche consultées) se prend,
        # puis se confronte à la photographie de la déclaration — NON JUGEABLE en nommant ce qui a changé.
        jeu, r_jeu = _jouer_les_annees_d_examen(racine, fiche, bornes, (racine, nom))
        if jeu is None:
            raisons["jeu"] = r_jeu
            rendu = rendre(**entrees)
        else:
            ops = jeu["ops"]
            entrees["ops"] = ops
            # ⑧ LES MESURES
            n_hors, r_hors = _seances_hors_examen(ops, decl, seances_d_examen, parts)
            if r_hors:
                raisons["seances_hors_examen"] = r_hors
            entrees["seances_hors_examen"] = n_hors
            if ops:
                entrees["point_mort_pct"] = J.point_mort_des_operations(jeu["tp"], jeu["sl"], ops, jeu["mod_pos"])
            s_hasard, r_s = J.seuil_de_la_loi(table, "seuil_du_hasard", k if isinstance(k, int) else None)
            if s_hasard is not None and ops:
                entrees["hasard"] = _hasard(jeu, s_hasard)
            else:
                raisons["hasard"] = r_s or "aucune opération"
            externes = {}
            fonctions, r_mes = _mesureurs()
            raisons.update(r_mes)
            for cle, mesurer in fonctions.items():
                m, r_m = mesurer(racine, fiche, ops)
                if m is None:
                    raisons[cle] = r_m
                else:
                    externes[cle] = m
            entrees["mesures_externes"] = externes
            # ⑨ LA GRILLE
            rendu = rendre(**entrees)
    except BaseException as e:
        TR.inscrire_le_resultat(racine, nom, echec="%s: %s" % (type(e).__name__, e))
        raise
    # ⑩ LE RÉSULTAT DU REGARD
    TR.inscrire_le_resultat(racine, nom, resultat={"verdict": rendu["verdict"], "motif": rendu["motif"],
                                                   "premier_controle_bloquant": rendu["premier_controle_bloquant"]})
    return rendu
