#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relève le périmètre de travail (machine du Chat, Cowork, circuits GitHub, forfait) et rend un tableau court en français.

Simulation boursière uniquement : ce programme ne touche ni aux cours ni aux positions, et ne passe aucun ordre.

① RÔLE — Mesurer, à chaque regard d'optimisation du plan, TOUT le périmètre dans lequel le Chat peut lancer des agents,
  et le rendre en un tableau d'une ligne par ressource : ce qui EXISTE, ce qui est UTILISÉ, un VERDICT
  (SOUS-EMPLOYÉ · JUSTE · SATURÉ · INCONNU) et le CRITÈRE qui a donné ce verdict. Neuf ressources : cœurs et charge,
  mémoire disponible, disque libre, épreuves en cours (voir ⑫), copies de travail (git worktree), copies
  dans /tmp, Cowork (dernière relecture et branches en attente), circuits GitHub, forfait. Une ressource qui ne se
  mesure pas rend INCONNU, jamais un chiffre inventé. Les seuils viennent d'UN seul fichier de réglage,
  `donnees/REGLAGES_DU_PERIMETRE.csv` (R-708 : un chiffre qui existe ailleurs ne se recopie pas).
② CONTEXTE D'APPEL — Lancé à la main par le Chat, à chaque regard d'optimisation et à chaque réveil de l'heure
  (MODE_EMPLOI_DEPOT.md §13.2, geste 8) ; le Chat montre le tableau à Jean-Luc. Éprouvé par
  tests/EPREUVES_DU_RELEVE_DU_PERIMETRE_Dim_15-11-2026.py. Aucune tâche du soir ne l'appelle.
③ ENTRÉE — La ligne de commande, toutes options facultatives : `--racine` (dépôt privé, par défaut celui qui contient ce
  programme) · `--pub` (clone du dépôt public, par défaut /home/claude/pub) · `--reglages` (par défaut
  `donnees/REGLAGES_DU_PERIMETRE.csv` de la racine) · `--proc` (par défaut /proc) · `--tmp` (par défaut /tmp) ·
  `--disque` (dossier dont on mesure le disque, par défaut la racine) · `--forfait` (par défaut
  `programmes/TENIR_LE_FORFAIT.py` de la racine). Les options autres que `--racine` servent surtout aux épreuves, qui
  fabriquent de fausses ressources. La commande `nproc` est cherchée dans le PATH.
④ CONDITIONS D'ENTRÉE — Le fichier de réglage existe et porte chacun des réglages de REGLAGES_ATTENDUS une seule fois,
  avec un nombre fini qui respecte ses bornes (voir `lire_reglages`) ; sinon le programme sort en 2 sans tableau.
  `--racine` est un dépôt Git ; sinon le programme sort en 2 sans tableau. Tout le reste peut manquer : la ressource
  rend INCONNU.
⑤ SORTIE — Un tableau affiché (en-tête, une ligne par ressource, une ligne de compte des verdicts) et un code de
  sortie : 0 quand le tableau est rendu, y compris avec des lignes INCONNU (chacune dit pourquoi) · 2 quand le fichier
  de réglage est illisible ou absurde, ou quand la racine n'est pas un dépôt Git, et alors aucun tableau (R-734 : un
  relevé qui n'a pas pu tourner ne rend jamais 0).
⑥ TRAITEMENT — Voir `main` : lire les réglages, mesurer chaque ressource, juger chaque mesure, afficher.
⑦ UNITÉ — Cœurs (nombre) et charge moyenne (tâches prêtes, sur 1, 5 et 15 minutes) · gigaoctets (10^9 octets) ·
  nombres de processus, de copies, de branches · heures · points de jauge du forfait · dates et heures de Paris.
⑧ POURQUOI — A-805, décision de Jean-Luc du 15-11-2026 à 12h50 (dictée) : « confirme-moi que tu fais bien une
  optimisation, une analyse aussi exhaustive dans le plan. Si ce n'est pas le cas, il faut y remédier et sans doute me
  montrer la même chose que tu viens de me montrer là quand tu lances ces phases d'optimisation ». Mesuré le 15-11 à
  12h50 : les quatre regards du 14-11 ne mentionnaient jamais les circuits GitHub, presque jamais Cowork, une seule fois
  les cœurs, alors que le relevé de 12h45 montrait 2 cœurs saturés (charge 2,85), Cowork sous-employé et les circuits
  de séries longues inutilisés. Préférence de Jean-Luc du 05-11-2026 : « utiliser autant d'agents que la machine le
  permet réellement, après avoir mesuré son périmètre ».
⑨ CE QUI CLOCHE — ① L'usage réel des circuits GitHub (exécutions, minutes) n'est pas visible d'ici : seuls les fichiers
  de circuit et les branches `series-longues/*` déjà rapatriées sont comptés ; le verdict est toujours INCONNU.
  ② Cowork se lit dans les références Git du DERNIER rapatriement (`git fetch`), que ce programme ne fait pas (lecture
  seule) : la date de ce rapatriement est affichée ; plus elle est vieille, moins la ligne vaut. Des références qui ne
  couvrent pas toutes les branches du dépôt partagé, une copie qui n'a jamais rapatrié depuis son clone, ou un
  dernier rapatriement venu d'un autre dépôt rendent INCONNU (voir `etat_des_references`) ; un clone
  superficiel est signalé dans le critère, sans être refusé. Une branche créée au dépôt partagé APRÈS le dernier
  rapatriement ne se voit pas, et rien ici ne peut le savoir sans réseau. ③ Le verdict du forfait
  lit la SORTIE en texte de TENIR_LE_FORFAIT.py (lignes « seuil … % », « PROJECTION À LA REMISE », « VERDICT ») : si ce
  programme change ses phrases, la ligne devient INCONNU, jamais fausse. ④ La taille des copies de /tmp compte aussi
  les copies de travail rangées sous /tmp (comptées deux fois). ⑤ Sans la commande `nproc`, les cœurs rendent INCONNU,
  sans repli sur une autre mesure. ⑥ La machine de Cowork elle-même (cœurs, charge) n'est pas visible d'ici : seule
  sa production (relectures poussées) l'est.
⑩ EFFET — N'écrit rien, ne pousse rien, ne rapatrie rien. Lance en lecture `nproc`, `du`, `git` et, s'il existe,
  TENIR_LE_FORFAIT.py `--etat` (qui n'écrit rien). Aucun accès réseau.
⑪ TERMINAISON — Sort par `sys.exit` à la fin. Chaque commande lancée est bornée par `delai_de_mesure_secondes` ; au-delà
  elle est abandonnée et la ressource rend INCONNU. Aucun appel ne peut donc ne pas revenir.
⑫ DÉFINITIONS
  une copie de travail : un dossier rattaché au dépôt par `git worktree`, hors du dépôt principal
  une copie dans /tmp : un dossier de premier niveau de /tmp qui porte un `.git`
  une épreuve en cours : un processus dont l'interprète est un Python et dont le FICHIER LANCÉ (le premier argument
    qui n'est pas une option, chemin relatif résolu depuis le dossier du processus) est soit rangé dans un dossier
    `tests` à n'importe quelle profondeur, soit déclaré comme épreuve de `programmes/` dans
    `tests/LANCEMENT_DES_EPREUVES.json` de la racine ET lancé avec les arguments que cette table déclare (gabarits
    comme `{copie}` exceptés) — la même définition que celle du certificateur (programmes/CERTIFIER_LA_VERSION.py),
    lue au même endroit (R-708) ; une épreuve qui en lance d'autres (ses descendants) n'est pas comptée en plus
    d'elles : chaque chaîne d'épreuves compte une fois
  une branche en attente : une branche `origin/travail-*` dont le dernier DÉPÔT (date de commit, pas d'auteur) qui
    change `echanges/A_RELIRE.md` est plus récent que le dernier dépôt qui change `echanges/RELU.md` signé par un
    auteur dont le nom contient « cowork »
  la dernière relecture de Cowork : le plus récent dépôt de `echanges/RELU.md` signé « cowork » sur TOUTES les
    branches de l'origine (main comprise), pas seulement les branches travail-*
"""
import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAGES_ATTENDUS = (
    "coeurs_fenetre_minutes", "coeurs_charge_par_coeur_saturee", "coeurs_charge_par_coeur_sous_employee",
    "memoire_part_disponible_saturee", "memoire_part_disponible_sous_employee", "disque_libre_sature_go",
    "epreuves_par_coeur_saturees", "epreuves_par_coeur_sous_employees", "worktrees_nombre_sature",
    "copies_tmp_go_saturees", "cowork_attente_saturee", "cowork_silence_heures_sous_employe",
    "forfait_ecart_points", "delai_de_mesure_secondes",
)
INCONNU = "INCONNU"
GO = 1e9


def fr(x, d=2):
    """Écrit un nombre à la française, virgule décimale.

    ① RÔLE — Rendre un nombre lisible par Jean-Luc dans le tableau.
    ② CONTEXTE D'APPEL — Les fonctions `juger_*` et `ligne_*`, pour chaque nombre affiché.
    ③ ENTRÉE — `x` : le nombre · `d` : le nombre de décimales.
    ④ CONDITIONS D'ENTRÉE — `x` est un nombre.
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — Formater avec `d` décimales, remplacer le point par une virgule.
    ⑦ UNITÉ — Celle du nombre.
    ⑧ POURQUOI — Le tableau est lu en français.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return f"{x:.{d}f}".replace(".", ",")


def fr_face_au_seuil(valeur, seuil, d=2):
    """Écrit une valeur mesurée avec assez de décimales pour qu'elle ne se lise jamais égale à son seuil quand elle ne
    l'est pas.

    ① RÔLE — Empêcher que l'arrondi d'affichage contredise le verdict (« 5,0 Go » lu « JUSTE » face à « SATURÉ si
      ≥ 5,0 Go »).
    ② CONTEXTE D'APPEL — Les fonctions `ligne_*`, pour chaque valeur affichée à côté du seuil qui la juge.
    ③ ENTRÉE — `valeur` : le nombre mesuré · `seuil` : le seuil affiché à côté · `d` : les décimales voulues d'abord.
    ④ CONDITIONS D'ENTRÉE — `valeur` et `seuil` sont des nombres finis.
    ⑤ SORTIE — UNE valeur : le texte de `valeur`, à `d` décimales, ou davantage (neuf au plus) tant que ce texte et
      celui du seuil au même nombre de décimales sont identiques alors que les deux nombres diffèrent.
      [rend: 1]
    ⑥ TRAITEMENT — Ajouter une décimale tant que l'arrondi rend la valeur et le seuil identiques.
    ⑦ UNITÉ — Celle de la valeur et du seuil, qui doit être la même.
    ⑧ POURQUOI — Relecture de Cowork du 15-11-2026 (S-4) : « | Copies dans /tmp | … | 5,0 Go | JUSTE | SATURÉ si /tmp
      ≥ 5,0 Go | » — taille juste sous 5 Go ; Jean-Luc lit « 5,0 ≥ 5,0 » et « JUSTE ».
    ⑨ CE QUI CLOCHE — Le seuil reste écrit avec ses propres décimales dans le critère : seule la valeur s'allonge.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main : la boucle s'arrête à neuf décimales au plus.
      [sort: non]
    """
    while d < 9 and valeur != seuil and fr(valeur, d) == fr(seuil, d):
        d += 1
    return fr(valeur, d)


def plus_proche(valeur, seuil_a, seuil_b):
    """Rend celui des deux seuils d'une ligne qui est le plus proche de la valeur.

    ① RÔLE — Choisir le seuil contre lequel `fr_face_au_seuil` allonge l'affichage, quand une ligne en a deux.
    ② CONTEXTE D'APPEL — Les fonctions `ligne_*` à deux seuils (cœurs, mémoire, épreuves).
    ③ ENTRÉE — `valeur` : le nombre mesuré · `seuil_a`, `seuil_b` : les deux seuils.
    ④ CONDITIONS D'ENTRÉE — Trois nombres finis.
    ⑤ SORTIE — UNE valeur : le seuil le plus proche ; `seuil_a` à égalité.
      [rend: 1]
    ⑥ TRAITEMENT — Comparer les deux écarts absolus.
    ⑦ UNITÉ — Celle des trois nombres.
    ⑧ POURQUOI — Seul le seuil voisin de la valeur peut se lire égal à elle après arrondi.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return seuil_a if abs(valeur - seuil_a) <= abs(valeur - seuil_b) else seuil_b


def lire_reglages(chemin):
    """Lit tous les seuils du relevé dans leur seul fichier.

    ① RÔLE — Donner aux verdicts les seuils que Jean-Luc a fixés (ou doit confirmer), depuis LEUR seul endroit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `chemin` : le fichier de réglage, CSV à virgules, en-tête `reglage,valeur,etat,qui_decide,raison`.
    ④ CONDITIONS D'ENTRÉE — Chaque nom de REGLAGES_ATTENDUS y figure une seule fois, avec un nombre qui respecte les
      bornes ci-dessous ; sinon ValueError, ou OSError si le fichier manque.
    ⑤ SORTIE — UNE valeur : le dictionnaire nom → nombre.
      [rend: 1]
    ⑥ TRAITEMENT — Lire les lignes, refuser un doublon, refuser une valeur qui n'est pas écrite comme un nombre décimal
      simple (motif `-?chiffres`, suivi au plus d'une virgule ou d'un point et de chiffres : ni exposant, ni souligné,
      ni `nan`, ni `inf`), la convertir en nombre, refuser un manquant, puis refuser toute valeur absurde : ① non finie
      ou négative · ② délai de mesure nul ou au-delà de 3600 secondes · ③ fenêtre de
      charge autre que 1, 5 ou 15 minutes · ④ nombre de copies ou de branches qui n'est pas un entier d'au moins 1 ·
      ⑤ part de mémoire au-dessus de 1 · ⑥ seuils CROISÉS : le seuil de sous-emploi d'une ressource doit laisser la
      place à JUSTE, donc être du bon côté de son seuil de saturation (cœurs et épreuves : sous-emploi ≤ saturation ;
      mémoire : saturation ≤ sous-emploi).
    ⑦ UNITÉ — Celle que porte chaque réglage dans sa colonne `etat`.
    ⑧ POURQUOI — R-708 : un seuil écrit dans le code et dans un fichier finit par diverger ; il n'est écrit qu'ici.
      Les bornes : relecture de Cowork du 15-11-2026 (D-3) — `coeurs_fenetre_minutes=nan` faisait planter le relevé
      (code 1, pas 2), `coeurs_charge_par_coeur_saturee=nan` rendait les cœurs à jamais non SATURÉS (code 0),
      `delai_de_mesure_secondes=0` rendait 7 lignes INCONNU (code 0), et une mémoire à 91 % libre était jugée SATURÉ
      avec des seuils croisés (code 0). Un réglage absurde est un relevé qui ne peut pas tourner (R-734 : code 2).
      Seconde relecture du même jour (N-4) : `delai_de_mesure_secondes=1e300` était accepté puis faisait planter le
      relevé (OverflowError, code 1), et `1_0` était lu 10 sans un mot, parce que `float()` de Python accepte les
      exposants et les soulignés. La borne d'une heure : au-delà, une commande bloquée retiendrait le regard plus
      longtemps que le réveil de l'heure qui le relance (MODE_EMPLOI_DEPOT.md §13.2, geste 8).
    ⑨ CE QUI CLOCHE — Les bornes vérifient la cohérence, pas la justesse : un seuil cohérent mais mal choisi passe.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    vus = {}
    for l in lignes:
        cle = (l.get("reglage") or "").strip()
        if cle in REGLAGES_ATTENDUS:
            if cle in vus:
                raise ValueError(f"réglage {cle} écrit deux fois dans {chemin}")
            brut = (l.get("valeur") or "").strip()
            if not re.fullmatch(r"-?[0-9]+(?:[.,][0-9]+)?", brut):
                raise ValueError(f"réglage {cle}={brut!r} : pas un nombre décimal écrit simplement "
                                 f"(chiffres, puis au plus une virgule ou un point et des chiffres)")
            vus[cle] = float(brut.replace(",", "."))
    manquants = [c for c in REGLAGES_ATTENDUS if c not in vus]
    if manquants:
        raise ValueError(f"réglage absent de {chemin} : " + ", ".join(manquants))
    absurdes = [f"{c}={vus[c]}" for c in REGLAGES_ATTENDUS if not math.isfinite(vus[c]) or vus[c] < 0]
    if absurdes:
        raise ValueError("réglage non fini ou négatif : " + ", ".join(absurdes))
    regles = (
        (vus["delai_de_mesure_secondes"] > 0, "delai_de_mesure_secondes doit dépasser 0"),
        (vus["delai_de_mesure_secondes"] <= 3600, "delai_de_mesure_secondes ne dépasse pas 3600 (une heure)"),
        (vus["coeurs_fenetre_minutes"] in (1, 5, 15), "coeurs_fenetre_minutes doit valoir 1, 5 ou 15"),
        (vus["worktrees_nombre_sature"] >= 1 and vus["worktrees_nombre_sature"] == int(vus["worktrees_nombre_sature"]),
         "worktrees_nombre_sature doit être un entier d'au moins 1"),
        (vus["cowork_attente_saturee"] >= 1 and vus["cowork_attente_saturee"] == int(vus["cowork_attente_saturee"]),
         "cowork_attente_saturee doit être un entier d'au moins 1"),
        (vus["memoire_part_disponible_sous_employee"] <= 1 and vus["memoire_part_disponible_saturee"] <= 1,
         "une part de mémoire ne dépasse pas 1"),
        (vus["coeurs_charge_par_coeur_sous_employee"] <= vus["coeurs_charge_par_coeur_saturee"],
         "seuils des cœurs croisés : sous-emploi au-dessus de la saturation"),
        (vus["epreuves_par_coeur_sous_employees"] <= vus["epreuves_par_coeur_saturees"],
         "seuils des épreuves croisés : sous-emploi au-dessus de la saturation"),
        (vus["memoire_part_disponible_saturee"] <= vus["memoire_part_disponible_sous_employee"],
         "seuils de la mémoire croisés : saturation au-dessus du sous-emploi"),
    )
    fautes = [texte for tenu, texte in regles if not tenu]
    if fautes:
        raise ValueError("réglage absurde : " + " ; ".join(fautes))
    return vus


def lancer(commande, delai):
    """Lance une commande en lecture et rend sa sortie, ou None si elle n'a pas pu conclure.

    ① RÔLE — Un seul endroit pour lancer `nproc`, `du`, `git` et le programme du forfait, avec une borne de temps.
    ② CONTEXTE D'APPEL — Les fonctions `mesurer_*`.
    ③ ENTRÉE — `commande` : la liste des mots de la commande · `delai` : secondes laissées.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le code de sortie (None si la commande n'a pas conclu) · la sortie standard en texte
      (None dans le même cas) · la raison en mots quand la commande n'a pas conclu (« introuvable » ou « sans réponse
      en <n> s »), sinon None. Un code non nul n'est pas une raison : l'appelant le lit.
      [rend: 3]
    ⑥ TRAITEMENT — Lancer, attendre au plus `delai`, rendre code, sortie et None ; introuvable → (None, None,
      « introuvable ») ; trop long → (None, None, « sans réponse en <delai> s »).
    ⑦ UNITÉ — Secondes pour le délai.
    ⑧ POURQUOI — Une commande qui ne revient pas ne doit pas bloquer le regard : la ressource devient INCONNU. La
      raison est séparée depuis la relecture de Cowork du 15-11-2026 (D-4) : « introuvable » et « trop long » étaient
      confondus, et un `git` lent était rapporté « aucune origine configurée » sur un dépôt qui en a une.
    ⑨ CE QUI CLOCHE — La sortie d'erreur est jetée : la raison exacte d'un code non nul n'est pas affichée.
    ⑩ EFFET — Lance un processus.
    ⑪ TERMINAISON — Rend la main au plus tard après `delai` secondes, si le processus lancé ne laisse pas derrière lui
      un enfant qui garde sa sortie ouverte (cas non rencontré avec `nproc`, `du`, `git`).
      [sort: non]
    """
    try:
        p = subprocess.run(commande, capture_output=True, text=True, timeout=delai)
    except subprocess.TimeoutExpired:
        return None, None, f"sans réponse en {fr(delai, 0)} s"
    except OSError:
        return None, None, "introuvable"
    return p.returncode, p.stdout, None


def echec(nom, code, raison):
    """Dit en mots pourquoi une commande n'a pas rendu de mesure.

    ① RÔLE — Un seul endroit pour la phrase d'échec d'une commande, sans confondre délai, absence et refus.
    ② CONTEXTE D'APPEL — Les fonctions `mesurer_*` et `etat_des_references`, quand `lancer` n'a pas rendu le code 0.
    ③ ENTRÉE — `nom` : la commande en mots · `code` : le code rendu par `lancer` · `raison` : la raison rendue par
      `lancer`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la phrase.
      [rend: 1]
    ⑥ TRAITEMENT — Avec une raison : « commande <nom> <raison> » ; sinon « commande <nom> en échec (code <code>) ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑧ de `lancer`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return f"commande {nom} {raison}" if raison else f"commande {nom} en échec (code {code})"


def mesurer_coeurs(proc, delai):
    """Mesure le nombre de cœurs (`nproc`) et la charge moyenne sur 1, 5 et 15 minutes.

    ① RÔLE — Dire combien de cœurs la machine du Chat offre et combien de tâches les occupent.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `proc` : le dossier qui tient lieu de /proc (on y lit `loadavg`) · `delai` : secondes laissées à `nproc`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `coeurs` (entier ou None), `charges` (trois nombres ou None), `pourquoi`
      (texte quand quelque chose manque, sinon None).
      [rend: 1]
    ⑥ TRAITEMENT — Lancer `nproc` ; lire les trois premiers nombres de `loadavg`.
    ⑦ UNITÉ — Cœurs ; tâches prêtes en moyenne.
    ⑧ POURQUOI — Relevé du 15-11-2026 à 12h45 (A-805) : 2 cœurs, charge 2,85 ; les regards ne le disaient pas.
    ⑨ CE QUI CLOCHE — Sans `nproc`, aucun repli (voir ⑨ ⑤ du fichier).
    ⑩ EFFET — Lance `nproc`, lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = {"coeurs": None, "charges": None, "pourquoi": None}
    code, sortie, raison = lancer(["nproc"], delai)
    if code == 0 and sortie and sortie.strip().isdigit():
        m["coeurs"] = int(sortie.strip())
    else:
        m["pourquoi"] = echec("nproc", code, raison)
    try:
        with open(os.path.join(proc, "loadavg"), encoding="utf-8") as f:
            m["charges"] = [float(x) for x in f.read().split()[:3]]
        if len(m["charges"]) != 3:
            raise ValueError
    except (OSError, ValueError):
        m["charges"] = None
        m["pourquoi"] = ((m["pourquoi"] + " · ") if m["pourquoi"] else "") + "loadavg illisible"
    return m


def mesurer_memoire(proc):
    """Mesure la mémoire totale et la mémoire disponible.

    ① RÔLE — Dire combien de mémoire reste pour de nouveaux agents.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `proc` : le dossier qui tient lieu de /proc (on y lit `meminfo`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `total` et `disponible` en octets (ou None), `pourquoi`.
      [rend: 1]
    ⑥ TRAITEMENT — Lire les lignes `MemTotal` et `MemAvailable` (en kilooctets), convertir en octets.
    ⑦ UNITÉ — Octets.
    ⑧ POURQUOI — `MemAvailable` est l'estimation du noyau de ce qu'un nouveau processus peut prendre sans faire
      reprendre la mémoire des autres ; `MemFree` la sous-estime.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = {"total": None, "disponible": None, "pourquoi": None}
    try:
        with open(os.path.join(proc, "meminfo"), encoding="utf-8") as f:
            for l in f:
                morceaux = l.split()
                if len(morceaux) >= 2 and morceaux[0] == "MemTotal:":
                    m["total"] = int(morceaux[1]) * 1024
                elif len(morceaux) >= 2 and morceaux[0] == "MemAvailable:":
                    m["disponible"] = int(morceaux[1]) * 1024
    except (OSError, ValueError):
        pass
    if not m["total"] or m["disponible"] is None:
        m["total"], m["disponible"], m["pourquoi"] = None, None, "meminfo illisible ou sans MemTotal/MemAvailable"
    return m


def mesurer_disque(dossier):
    """Mesure la taille du disque qui porte `dossier` et ce qui reste libre pour l'utilisateur.

    ① RÔLE — Dire combien de clones et de copies le disque peut encore recevoir.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `dossier` : un dossier du disque à mesurer.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `total` et `libre` en octets (ou None), `pourquoi`.
      [rend: 1]
    ⑥ TRAITEMENT — `shutil.disk_usage` ; `libre` est la place utilisable sans droits d'administrateur.
    ⑦ UNITÉ — Octets.
    ⑧ POURQUOI — Un disque plein fait échouer les clones d'épreuve et les écritures du circuit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit l'état du système de fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        u = shutil.disk_usage(dossier)
    except OSError:
        return {"total": None, "libre": None, "pourquoi": f"dossier {dossier} introuvable"}
    return {"total": u.total, "libre": u.free, "pourquoi": None}


def fichier_lance(mots):
    """Rend le fichier qu'un interprète Python exécute, d'après sa ligne de commande.

    ① RÔLE — Désigner le programme réellement lancé, et non un mot quelconque des arguments.
    ② CONTEXTE D'APPEL — `compter_epreuves`, pour chaque processus.
    ③ ENTRÉE — `mots` : la ligne de commande, en liste de mots.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin tel qu'écrit, ou None si le processus n'est pas un Python qui lance un fichier.
      [rend: 1]
    ⑥ TRAITEMENT — Le premier mot doit être un interprète dont le nom est « python » suivi au plus de chiffres et de
      points (python, python3, python3.11). Parcourir ensuite les mots : « - » veut dire qu'aucun fichier n'est lancé ;
      `--check-hash-based-pycs` (sans « = ») saute le mot suivant, toute autre option longue est passée ; une option
      courte se lit LETTRE PAR LETTRE, parce que Python accepte les lettres collées (`-Bc`, `-IW…`) : une lettre `c` ou
      `m` veut dire qu'aucun fichier n'est lancé (le reste est du code ou un module), une lettre `W` ou `X` prend la
      suite du mot pour valeur, ou le mot suivant si elle est la dernière ; le premier mot qui ne commence pas par
      « - » est le fichier lancé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture de Cowork du 15-11-2026 (S-1) : compter « un mot contient tests/ » comptait
      `RELEVER_LE_PERIMETRE.py --tmp /x/tests/` et manquait `programmes/EPREUVES_TENIR_UN_PLANNING.py --mutations`.
      Seconde relecture du même jour (N-5, broutilles) : `python3 -Bc '…'` rendait le code comme nom de fichier, et
      `--check-hash-based-pycs always x.py` rendait « always ».
    ⑨ CE QUI CLOCHE — Une épreuve lancée par un autre programme que Python (bash, pytest installé comme commande)
      n'est pas vue. Les options sont celles de CPython 3 ; une option future qui prendrait une valeur serait lue comme
      une option sans valeur, et sa valeur comme le fichier lancé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not mots or not re.fullmatch(r"python[0-9.]*", os.path.basename(mots[0])):
        return None
    sauter = False
    for m in mots[1:]:
        if sauter:
            sauter = False
            continue
        if m == "-":
            return None
        if m.startswith("--"):
            sauter = m == "--check-hash-based-pycs"
            continue
        if m.startswith("-"):
            lettres = m[1:]
            for i, lettre in enumerate(lettres):
                if lettre in "cm":
                    return None
                if lettre in "WX":
                    sauter = i == len(lettres) - 1
                    break
            continue
        return m
    return None


def compter_epreuves(proc, racine):
    """Compte les épreuves en cours : les processus Python dont le fichier lancé est une épreuve (voir ⑫ du fichier).

    ① RÔLE — Dire combien d'épreuves tournent en ce moment sur la machine du Chat.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `proc` : le dossier qui tient lieu de /proc ; chaque sous-dossier numérique porte un `cmdline`, un
      lien `cwd` et un `status` (ligne `PPid:`) · `racine` : le dépôt, où se lit `tests/LANCEMENT_DES_EPREUVES.json`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `nombre` (entier, ou None si `proc` ne se lit pas) et `reserve` (texte
      quand les épreuves de `programmes/` ne peuvent pas être reconnues, sinon None).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les chemins déclarés sous la clé `epreuves` de `tests/LANCEMENT_DES_EPREUVES.json`, chacun
      avec ses `arguments` privés des gabarits (`{copie}` et tout mot entre accolades) · ② pour chaque sous-dossier
      numérique de `proc` (sauf ce processus), lire le parent (`PPid:` de `status`), puis `cmdline` (mots séparés par
      un octet nul) et en tirer le fichier lancé (`fichier_lance`) · ③ un chemin relatif se résout depuis le lien
      `cwd` du processus · ④ c'est une épreuve si un dossier de son chemin s'appelle `tests`, ou si ses deux derniers
      éléments (« programmes/<nom> ») sont un chemin déclaré ET que chacun de ses arguments déclarés figure parmi les
      mots qui suivent le fichier lancé (égal ; ou, si l'argument déclaré est un CHEMIN — il contient une barre
      oblique, comme `donnees/x.csv` —, fin de chemin égale : `/r/donnees/x.csv`. Un argument déclaré sans barre
      oblique, comme `epreuves`, n'est jamais une fin de chemin : `/x/epreuves` ne le vaut pas) · ⑤ n'est COMPTÉE qu'une
      épreuve dont aucun DESCENDANT (enfant, enfant d'enfant…) n'est lui-même une épreuve : chaque chaîne
      d'épreuves qui tourne compte une fois, par son bout.
    ⑦ UNITÉ — Processus.
    ⑧ POURQUOI — Les épreuves sont la charge principale de la machine pendant un plan. La définition est celle du
      certificateur (`programmes/CERTIFIER_LA_VERSION.py` lit le même fichier JSON) : une seule définition (R-708).
      Seconde relecture de Cowork du 15-11-2026 : (N-5) sur le vrai /proc, `EPREUVES_B_DU_BLOC_5A…py --saboter`
      relance LE MÊME FICHIER pour chaque cas (`--cas /tmp/b5a_…`) ; l'enfant était compté : deux épreuves réelles
      rendaient « 4 épreuves, SATURÉ » au lieu de « 2, JUSTE », et le Chat aurait retenu un agent que la machine
      pouvait prendre · (N-3) les arguments de la table étaient ignorés : `TENIR_LES_POSITIONS.py .` (production,
      sans `--calibrage`) et `CONTROLER_LES_COURS.py` (sans `epreuves`) étaient comptés comme épreuves. Le bout
      plutôt que la tête (la piste de la relecture était « aucun ancêtre n'est une épreuve ») : mesuré le 16-11-2026
      à 16h12 sur le vrai /proc, `tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py` lançait DEUX épreuves en parallèle,
      chacune relancée pour son cas ; compter la tête rendait 1 pour deux épreuves qui tournaient (sous-compte, sens
      dangereux), compter les bouts rend 2. Ce jour-là : 3 têtes, 4 bouts, 8 processus d'épreuve.
    ⑨ CE QUI CLOCHE — Un processus dont `cwd` ne se lit pas garde son chemin relatif tel quel : lancé depuis `tests/`
      par son seul nom, il n'est pas compté. Un processus qui finit pendant la lecture est ignoré. Un processus dont
      `status` ne se lit pas est pris sans parent : son épreuve parente serait comptée en plus de lui (sens
      prudent). Deux épreuves parentes l'une de l'autre (cycle, impossible dans un vrai /proc) ne comptent pas. Un programme déclaré dont tous les arguments sont des gabarits (`["{copie}"]`) ou vides est compté
      quel que soit son lancement : rien ne distingue alors l'épreuve de la production. Un fichier `.py` rangé dans un
      dossier `tests` d'un AUTRE projet de la machine est compté (la définition ne connaît pas le projet ; sens
      prudent). Le fichier lancé est retrouvé dans la ligne de commande par sa première occurrence : une option dont
      la valeur serait ce même mot fausserait la lecture des arguments. Un argument déclaré qui est un nom de fichier
      seul (`x.csv`, sans barre oblique) n'est reconnu que tel quel (`x.csv`, `./x.csv`), jamais au bout d'un chemin
      (`/r/x.csv`) : l'épreuve lancée ainsi n'est pas comptée (sens du sous-compte ; aucun argument déclaré n'a
      cette forme le 16-11-2026). (Relecteur neuf du 16-11-2026, D-3 : la règle « fin de chemin égale » valait pour
      tout argument ; une production lancée avec un chemin `…/epreuves` comptait comme l'épreuve de
      `CONTROLER_LES_COURS.py`, déclarée avec l'argument `epreuves`.)
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    reserve = None
    try:
        with open(os.path.join(racine, "tests", "LANCEMENT_DES_EPREUVES.json"), encoding="utf-8") as f:
            declarees = {os.path.normpath(c): [a for a in x.get("arguments", [])
                                               if not re.fullmatch(r"\{[^{}]*\}", a)]
                         for c, x in json.load(f)["epreuves"].items()}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        declarees = {}
        reserve = "épreuves de programmes/ non reconnues : tests/LANCEMENT_DES_EPREUVES.json illisible"
    try:
        entrees = os.listdir(proc)
    except OSError:
        return {"nombre": None, "reserve": reserve}
    parents, epreuves = {}, set()
    for e in entrees:
        if not e.isdigit() or int(e) == os.getpid():
            continue
        try:
            with open(os.path.join(proc, e, "status"), encoding="utf-8", errors="replace") as f:
                t = re.search(r"(?m)^PPid:\s*([0-9]+)", f.read())
            if t:
                parents[e] = t.group(1)
        except OSError:
            pass
        try:
            with open(os.path.join(proc, e, "cmdline"), "rb") as f:
                mots = [m.decode("utf-8", "replace") for m in f.read().split(b"\0") if m]
        except OSError:
            continue
        lance = fichier_lance(mots)
        if lance is None:
            continue
        suite = mots[mots.index(lance, 1) + 1:]
        if not os.path.isabs(lance):
            try:
                lance = os.path.join(os.readlink(os.path.join(proc, e, "cwd")), lance)
            except OSError:
                pass
        chemin = os.path.normpath(lance)
        dossiers = os.path.dirname(chemin).split(os.sep)
        attendus = declarees.get(os.path.join(*chemin.split(os.sep)[-2:]))
        if "tests" in dossiers or (attendus is not None and all(
                any(os.path.normpath(w) == os.path.normpath(a) or (os.sep in os.path.normpath(a) and os.path.normpath(
                    w).endswith(os.sep + os.path.normpath(a))) for w in suite)
                for a in attendus)):
            epreuves.add(e)
    porteuses = set()
    for e in epreuves:
        vus, p = {e}, parents.get(e)
        while p is not None and p not in vus:
            vus.add(p)
            if p in epreuves:
                porteuses.add(p)
            p = parents.get(p)
    return {"nombre": len(epreuves - porteuses), "reserve": reserve}


def mesurer_taille(chemins, delai):
    """Mesure la place occupée sur le disque par une liste de dossiers, avec `du`.

    ① RÔLE — Un seul endroit pour mesurer une taille de dossier.
    ② CONTEXTE D'APPEL — `mesurer_worktrees`, `mesurer_copies_tmp`.
    ③ ENTRÉE — `chemins` : la liste des dossiers · `delai` : secondes laissées à `du`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la somme en octets, 0 pour une liste vide, ou None si `du` n'a rien rendu dans le délai.
      [rend: 1]
    ⑥ TRAITEMENT — `du -s --block-size=1` sur tous les dossiers d'un coup ; additionner la première colonne.
    ⑦ UNITÉ — Octets.
    ⑧ POURQUOI — `du` compte les blocs réellement occupés ; un dossier illisible n'arrête pas les autres.
    ⑨ CE QUI CLOCHE — Un dossier illisible est compté pour ce que `du` en a pu lire (sortie d'erreur jetée).
    ⑩ EFFET — Lance `du`.
    ⑪ TERMINAISON — Rend la main au plus tard après `delai` secondes.
      [sort: non]
    """
    if not chemins:
        return 0
    code, sortie, _ = lancer(["du", "-s", "--block-size=1"] + list(chemins), delai)
    if sortie is None or not sortie.strip():
        return None
    try:
        return sum(int(l.split()[0]) for l in sortie.splitlines() if l.strip())
    except ValueError:
        return None


def mesurer_worktrees(racine, delai):
    """Compte les copies de travail rattachées au dépôt et mesure leur taille.

    ① RÔLE — Dire combien de copies de travail existent hors du dépôt principal, et ce qu'elles pèsent.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le dépôt · `delai` : secondes laissées à `git` puis à `du`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `nombre` (entier ou None), `taille` (octets ou None), `pourquoi`.
      [rend: 1]
    ⑥ TRAITEMENT — `git worktree list --porcelain` ; retenir les chemins « worktree » sauf le premier (le dépôt
      principal) et ceux qui n'existent plus sur le disque ; mesurer leur taille.
    ⑦ UNITÉ — Copies ; octets.
    ⑧ POURQUOI — Préférence de Jean-Luc du 13-11-2026 : les copies de travail temporaires s'effacent dès qu'elles ne
      servent plus.
    ⑨ CE QUI CLOCHE — Une copie de travail dont le dossier a disparu (« prunable ») n'est pas comptée.
    ⑩ EFFET — Lance `git` et `du` en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    code, sortie, raison = lancer(["git", "-C", racine, "worktree", "list", "--porcelain"], delai)
    if code != 0 or sortie is None:
        return {"nombre": None, "taille": None, "pourquoi": echec("git worktree list", code, raison)}
    chemins = [l[len("worktree "):] for l in sortie.splitlines() if l.startswith("worktree ")][1:]
    chemins = [c for c in chemins if os.path.isdir(c)]
    taille = mesurer_taille(chemins, delai)
    return {"nombre": len(chemins), "taille": taille,
            "pourquoi": None if taille is not None else "du sans réponse dans le délai"}


def mesurer_copies_tmp(tmp, delai):
    """Compte les copies du dépôt rangées dans /tmp et mesure la place occupée par /tmp.

    ① RÔLE — Dire ce que les copies temporaires laissées derrière les épreuves coûtent en disque.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `tmp` : le dossier qui tient lieu de /tmp · `delai` : secondes laissées à `du`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `copies` (entier ou None), `dossiers` (entier ou None), `taille` (octets ou
      None), `pourquoi`.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir le premier niveau de `tmp` ; compter les dossiers, et parmi eux ceux qui portent un `.git` ;
      mesurer la taille de `tmp` entier.
    ⑦ UNITÉ — Dossiers ; octets.
    ⑧ POURQUOI — Mesuré le 15-11-2026 : /tmp pesait 15,3 Go pour 2,4 Go libres sur le disque.
    ⑨ CE QUI CLOCHE — La taille compte aussi ce qui n'est pas une copie (fichiers, sorties d'épreuves).
    ⑩ EFFET — Lit le système de fichiers ; lance `du`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        entrees = list(os.scandir(tmp))
    except OSError:
        return {"copies": None, "dossiers": None, "taille": None, "pourquoi": f"dossier {tmp} illisible"}
    dossiers = [e.path for e in entrees if e.is_dir(follow_symlinks=False)]
    copies = sum(1 for d in dossiers if os.path.exists(os.path.join(d, ".git")))
    taille = mesurer_taille([tmp], delai)
    return {"copies": copies, "dossiers": len(dossiers), "taille": taille,
            "pourquoi": None if taille is not None else "du sans réponse dans le délai"}


def origine_sur_cette_machine(url):
    """Dit si l'adresse de l'origine désigne un dépôt de cette machine plutôt que le dépôt partagé.

    ① RÔLE — Reconnaître une origine qui est une COPIE locale : ses branches de suivi ne passent pas dans un clone.
    ② CONTEXTE D'APPEL — `etat_des_references`.
    ③ ENTRÉE — `url` : l'adresse EFFECTIVE de l'origine (`git ls-remote --get-url origin`, réécritures `insteadOf`
      appliquées : seconde relecture de Cowork du 15-11-2026, N-6 c).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si l'adresse est un chemin de fichier (absolu, relatif, ou `file://`), faux pour une
      adresse de réseau (`https://…`, `ssh://…`, `git@hôte:chemin`).
      [rend: 1]
    ⑥ TRAITEMENT — Règle de Git pour reconnaître un chemin local : `file://`, ou ni « :// » ni « hôte: » avant la
      première barre oblique.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture de Cowork du 15-11-2026 (D-1 a) : un clone fait depuis un autre clone de la machine
      (`git clone /home/claude/<dépôt>`) ne reçoit que les branches LOCALES de la source ; le relevé disait « 1 branche
      travail-* », « dernière relecture 14-11 20h09 » et SOUS-EMPLOYÉ, quand le dépôt partagé en avait 15 et une
      relecture du 15-11 13h18.
    ⑨ CE QUI CLOCHE — Un miroir local complet (`git clone --mirror`) tenu à jour serait refusé à tort (sens prudent :
      INCONNU).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if url.startswith("file://"):
        return True
    if "://" in url:
        return False
    return not re.match(r"^[^/]+:", url)


def adresse_rapatriee(url):
    """Écrit une adresse de dépôt sous la forme que Git donne dans `FETCH_HEAD`, pour comparer deux adresses.

    ① RÔLE — Reconnaître, dans `FETCH_HEAD`, les lignes qui viennent de l'origine et d'aucun autre dépôt.
    ② CONTEXTE D'APPEL — `etat_des_references`, pour l'adresse de l'origine et pour chaque ligne de `FETCH_HEAD`.
    ③ ENTRÉE — `url` : une adresse de dépôt (réseau, `git@hôte:chemin`, chemin, `file://`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'adresse sans identifiants (`utilisateur:secret@`), sans barres obliques finales, puis
      sans `.git` final.
      [rend: 1]
    ⑥ TRAITEMENT — Retirer les espaces des bords, les identifiants avant `@` (forme `schéma://` et forme
      `utilisateur@hôte:`), les `/` finaux, puis un `.git` final : c'est ce que fait Git en écrivant `FETCH_HEAD`
      (mesuré le 16-11-2026, git 2.43 : origine `file:///…/o.git/` → « of file:///…/o »). Appliquée aux deux côtés,
      la transformation est sans effet sur une adresse déjà écrite par Git.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Seconde relecture de Cowork du 15-11-2026 (N-1 et N-6 b) : le programme ne lisait que les NOMS de
      `FETCH_HEAD` ; un `git fetch` d'un autre dépôt aux mêmes noms de branches le réécrivait, et le relevé jugeait
      complètes et fraîches des références d'origine que ce rapatriement n'avait pas touchées.
    ⑨ CE QUI CLOCHE — Si une version de Git écrivait l'adresse autrement, aucune ligne ne serait reconnue et le relevé
      rendrait INCONNU (sens prudent).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    url = url.strip()
    url = re.sub(r"^([A-Za-z][A-Za-z0-9+.-]*://)[^/@]*@", r"\1", url)
    url = re.sub(r"^[^/:@]+@([^/:]+:)", r"\1", url)
    url = url.rstrip("/")
    return url[:-4] if len(url) > 4 and url.endswith(".git") else url


def etat_des_references(racine, delai):
    """Dit si les références de l'origine couvrent toutes les branches du dépôt partagé, depuis quand, et si le dépôt
    est superficiel.

    ① RÔLE — Empêcher qu'un clone ou un rapatriement partiel fasse croire que Cowork n'a rien relu ou que GitHub n'a
      rien produit.
    ② CONTEXTE D'APPEL — `mesurer_cowork`, `mesurer_circuits`.
    ③ ENTRÉE — `racine` : le dépôt · `delai` : secondes laissées à chaque commande `git`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la raison pour laquelle les références sont PARTIELLES ou illisibles (texte), ou None
      si elles couvrent toutes les branches · vrai si le dépôt est superficiel (`--depth`), faux sinon, None si
      inconnu · la date de Paris du dernier rapatriement (datetime), ou None s'il n'y en a pas eu depuis le clone.
      [rend: 3]
    ⑥ TRAITEMENT — La PROPRIÉTÉ vérifiée : « chaque référence `origin/*` lue ici a été rafraîchie par le dernier
      rapatriement, et ce rapatriement venait du dépôt partagé ». Dans l'ordre, la première condition qui manque
      donne la raison : ① une origine est configurée (`remote.origin.url` ; code 1 = absente, autre échec = la commande
      et sa raison) · ② son adresse EFFECTIVE (`git ls-remote --get-url origin`, qui applique les réécritures
      `url.<…>.insteadOf` sans toucher au réseau) n'est pas un dépôt de cette machine (`origine_sur_cette_machine`) ·
      ③ son motif de rapatriement couvre toutes les branches (`refs/heads/*` dans `remote.origin.fetch`) · ④ un
      `FETCH_HEAD` existe (chemin rendu par `git rev-parse --git-path`, propre à chaque copie de travail) : sinon
      aucun rapatriement n'a eu lieu depuis le clone, et rien ne dit d'où viennent les références · ⑤ au moins une
      ligne de `FETCH_HEAD` vient de l'origine (« branch '<nom>' of <adresse> », adresse comparée par
      `adresse_rapatriee`) · ⑥ chaque nom de `refs/remotes/origin/*` (sauf HEAD) figure parmi les lignes de
      `FETCH_HEAD` venues de l'origine : sinon le dernier rapatriement n'a pris qu'une partie des branches, ou une
      branche supprimée au dépôt partagé est restée faute de `--prune`. Puis lire `rev-parse --is-shallow-repository`.
    ⑦ UNITÉ — Dates et heures de Paris.
    ⑧ POURQUOI — Mesuré le 15-11-2026 à 13h06 : dans un clone neuf à une seule branche, le relevé disait « dernière
      relecture aucune » et « 0 séries longues rapatriées », deux chiffres faux présentés comme des mesures. Relecture
      de Cowork du même jour (D-1) : le premier correctif n'épelait qu'une FORME de clone partiel ; un clone fait
      depuis une copie locale, ou un `git fetch origin <une branche>` qui rafraîchit `FETCH_HEAD`, rendaient encore les
      deux chiffres faux, avec une date de rapatriement fraîche. Le dépôt principal est lui-même superficiel et voit
      pourtant 233 relectures de Cowork : être superficiel n'est donc pas un motif d'INCONNU, seulement une réserve.
      Seconde relecture du même jour : (N-1, N-6 b) un rapatriement d'un AUTRE dépôt aux mêmes noms passait pour
      complet ; (N-6 a) un clone fait depuis une copie locale puis remis sur l'adresse GitHub (`set-url`), sans
      `git fetch`, rendait les chiffres faux du D-1 d'origine, sans `FETCH_HEAD` ; (N-6 c) une réécriture `insteadOf`
      vers une copie locale passait le contrôle de l'adresse écrite ; (N-2) le conseil rendu après une branche
      supprimée (`git fetch origin` sans `--prune`) ne réparait pas.
    ⑨ CE QUI CLOCHE — ① Une branche créée au dépôt partagé après le dernier rapatriement n'est pas vue, faute de
      réseau. ② Un motif de rapatriement plus étroit que `refs/heads/*` mais qui couvre `travail-*` serait jugé
      partiel à tort (sens prudent : INCONNU). ③ `FETCH_HEAD` est propre à chaque copie de travail alors que les
      références sont communes : un rapatriement complet fait depuis une autre copie de travail ne se voit pas d'ici
      (INCONNU si cette copie-ci n'a jamais rapatrié), et un rapatriement partiel fait ici après lui rend INCONNU à
      tort (sens prudent). ④ Une branche supprimée au dépôt partagé, dont la référence reste ici faute de `--prune`,
      rend INCONNU (c'est juste : cette référence ne dit plus rien de vrai) ; le conseil rendu dit `--prune`. ⑤ Un
      nom de branche qui contient une apostrophe n'est pas lu dans `FETCH_HEAD` : INCONNU (sens prudent). ⑥ Un
      rapatriement fait depuis l'origine sous une AUTRE adresse (avant un `set-url`) n'est pas reconnu : INCONNU.
    ⑩ EFFET — Lance `git` en lecture ; lit `FETCH_HEAD`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    superficiel, rapatriement = None, None
    code, sortie, raison = lancer(["git", "-C", racine, "rev-parse", "--is-shallow-repository"], delai)
    if code == 0 and sortie is not None:
        superficiel = sortie.strip() == "true"
    code, url, raison = lancer(["git", "-C", racine, "config", "--get", "remote.origin.url"], delai)
    if code == 1:
        return "aucune origine configurée : références illisibles", superficiel, None
    if code != 0 or url is None:
        return echec("git config", code, raison) + " : références illisibles", superficiel, None
    code, url, raison = lancer(["git", "-C", racine, "ls-remote", "--get-url", "origin"], delai)
    if code != 0 or not url or not url.strip():
        return echec("git ls-remote --get-url", code, raison) + " : adresse effective illisible", superficiel, None
    if origine_sur_cette_machine(url.strip()):
        return ("l'origine est une copie sur cette machine : ses propres branches de suivi ne passent pas dans un "
                "clone, les branches des autres manquent"), superficiel, None
    code, motifs, raison = lancer(["git", "-C", racine, "config", "--get-all", "remote.origin.fetch"], delai)
    if code != 0 or motifs is None:
        return echec("git config", code, raison) + " : motif de rapatriement illisible", superficiel, None
    if not any("refs/heads/*" in l for l in motifs.splitlines()):
        return "clone à une seule branche : les branches des autres ne sont pas visibles", superficiel, None
    code, refs, raison = lancer(["git", "-C", racine, "for-each-ref", "--format=%(refname:lstrip=3)",
                                 "refs/remotes/origin"], delai)
    code2, chemin, raison2 = lancer(["git", "-C", racine, "rev-parse", "--git-path", "FETCH_HEAD"], delai)
    if code != 0 or refs is None:
        return echec("git for-each-ref", code, raison) + " : références illisibles", superficiel, None
    if code2 != 0 or chemin is None:
        return echec("git rev-parse", code2, raison2) + " : rapatriement illisible", superficiel, None
    chemin = chemin.strip()
    chemin = chemin if os.path.isabs(chemin) else os.path.join(racine, chemin)
    conseil = "lancer `git fetch --prune origin`, sans nom de branche, avant le relevé"
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            lignes = re.findall(r"(?m)\tbranch '([^']+)' of (.+)$", f.read())
        rapatriement = datetime.fromtimestamp(os.path.getmtime(chemin), PARIS)
    except FileNotFoundError:
        return (f"aucun rapatriement depuis le clone (pas de FETCH_HEAD) : rien ne dit que les références viennent du "
                f"dépôt partagé ; {conseil}"), superficiel, None
    except OSError:
        return "FETCH_HEAD illisible : date et étendue du dernier rapatriement inconnues", superficiel, None
    origine = adresse_rapatriee(url)
    rafraichies = {nom for nom, venue in lignes if adresse_rapatriee(venue) == origine}
    if not rafraichies:
        autres = sorted({adresse_rapatriee(venue) for _, venue in lignes})
        return (f"dernier rapatriement ({rapatriement.strftime('%d-%m %Hh%M')}) venu d'ailleurs que l'origine"
                + (f" ({len(autres)} autre{'s' if len(autres) > 1 else ''} adresse{'s' if len(autres) > 1 else ''})"
                   if autres else " (aucune branche lue)")
                + f" ; {conseil}"), superficiel, rapatriement
    suivies = [n for n in refs.split() if n and n != "HEAD"]
    vieilles = [n for n in suivies if n not in rafraichies]
    if vieilles:
        return (f"dernier rapatriement partiel ({rapatriement.strftime('%d-%m %Hh%M')}) : {len(vieilles)} références "
                f"de suivi sur {len(suivies)} non rafraîchies (dont {vieilles[0]}) ; {conseil}"), superficiel, rapatriement
    return None, superficiel, rapatriement


def dates_cowork(sortie):
    """Tire d'un `git log --format=%ct<tab>%an` les dates des dépôts signés par Cowork.

    ① RÔLE — Un seul endroit pour reconnaître une relecture de Cowork.
    ② CONTEXTE D'APPEL — `mesurer_cowork`, pour toutes les branches puis pour chacune.
    ③ ENTRÉE — `sortie` : le texte rendu par `git log`, une ligne « <secondes Unix><tab><auteur> » par dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des dates (secondes Unix) dont l'auteur contient « cowork », sans casse.
      [rend: 1]
    ⑥ TRAITEMENT — Garder les lignes à tabulation dont la seconde partie contient « cowork ».
    ⑦ UNITÉ — Secondes Unix.
    ⑧ POURQUOI — Le Chat écrit aussi `RELU.md` (copies, fusions) : seul l'auteur dit qui a relu.
    ⑨ CE QUI CLOCHE — Un autre auteur dont le nom contient « cowork » serait pris pour Cowork.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [int(l.split("\t", 1)[0]) for l in sortie.splitlines()
            if "\t" in l and "cowork" in l.split("\t", 1)[1].lower()]


def mesurer_cowork(racine, delai):
    """Relève la dernière relecture de Cowork et les branches qui attendent la sienne.

    ① RÔLE — Dire si la machine de Cowork travaille, et combien de livraisons l'attendent.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le dépôt · `delai` : secondes laissées à chaque commande `git`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `derniere` (datetime de Paris ou None), `en_attente` (liste de noms courts
      ou None), `branches` (nombre de branches travail-* ou None), `rapatriement` (datetime de Paris ou None),
      `superficiel` (vrai, faux ou None), `pourquoi`.
      [rend: 1]
    ⑥ TRAITEMENT — ⓪ si les références sont partielles (`etat_des_references`), s'arrêter : `pourquoi` le dit ·
      ① la dernière relecture est le plus récent dépôt signé « cowork » qui change `echanges/RELU.md` sur TOUTES les
      branches de l'origine (`--remotes=origin`, main comprise) · ② lister `refs/remotes/origin/travail-*` · ③ pour
      chacune, le dernier dépôt signé « cowork » qui change `echanges/RELU.md`, et le dernier dépôt qui change
      `echanges/A_RELIRE.md` · ④ une branche est en attente si sa note est plus récente que sa dernière relecture (ou
      s'il n'y en a aucune). Les dates sont celles du DÉPÔT (`%ct`), pas de l'auteur.
    ⑦ UNITÉ — Dates et heures de Paris ; branches.
    ⑧ POURQUOI — A-805 : Cowork était sous-employé (relecture seule) et aucun regard ne le disait. Relecture de Cowork
      du 15-11-2026 (S-3) : quand toutes les branches travail-* sont fusionnées et supprimées — l'état normal voulu
      par A-448 —, la ligne disait « dernière relecture aucune » alors que `origin/main` portait une relecture de
      Cowork du 14-11. Date de dépôt : une note modifiée par `commit --amend` ou `rebase` garde sa date d'auteur
      ancienne et aurait paru plus vieille que la relecture qui la précède.
    ⑨ CE QUI CLOCHE — Les références sont celles du dernier rapatriement (voir ⑨ ② du fichier). Une branche dont la
      note est relue sans changer RELU.md (relecture refusée sans écrit) reste comptée en attente.
    ⑩ EFFET — Lance `git` en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = {"derniere": None, "en_attente": None, "branches": None, "rapatriement": None, "pourquoi": None,
         "superficiel": None}
    partiel, m["superficiel"], m["rapatriement"] = etat_des_references(racine, delai)
    if partiel:
        m["pourquoi"] = partiel
        return m
    code, toutes, raison = lancer(["git", "-C", racine, "log", "--remotes=origin", "--format=%ct\t%an", "--",
                                   "echanges/RELU.md"], delai)
    if code != 0 or toutes is None:
        m["pourquoi"] = echec("git log", code, raison)
        return m
    code, sortie, raison = lancer(["git", "-C", racine, "for-each-ref", "--format=%(refname:short)",
                                   "refs/remotes/origin/travail-*"], delai)
    if code != 0 or sortie is None:
        m["pourquoi"] = echec("git for-each-ref", code, raison)
        return m
    branches = [b for b in sortie.split() if b]
    attente = []
    for b in branches:
        code1, relu, raison1 = lancer(["git", "-C", racine, "log", "--format=%ct\t%an", b, "--", "echanges/RELU.md"],
                                      delai)
        code2, note, raison2 = lancer(["git", "-C", racine, "log", "-1", "--format=%ct", b, "--",
                                       "echanges/A_RELIRE.md"], delai)
        if code1 != 0 or relu is None:
            m["pourquoi"] = echec(f"git log sur {b}", code1, raison1)
            return m
        if code2 != 0 or note is None:
            m["pourquoi"] = echec(f"git log sur {b}", code2, raison2)
            return m
        par_cowork = dates_cowork(relu)
        derniere = max(par_cowork) if par_cowork else None
        if note.strip() and (derniere is None or int(note.strip()) > derniere):
            attente.append(b.split("/", 1)[-1])
    m["branches"], m["en_attente"] = len(branches), attente
    globales = dates_cowork(toutes)
    if globales:
        m["derniere"] = datetime.fromtimestamp(max(globales), PARIS)
    return m


def mesurer_circuits(racine, pub, delai):
    """Compte les fichiers de circuit GitHub des deux dépôts et les traces de séries longues déjà rapatriées.

    ① RÔLE — Dire quels circuits GitHub existent pour les séries longues ; leur usage réel ne se voit pas d'ici.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le dépôt privé · `pub` : le clone du dépôt public · `delai` : secondes laissées à `git`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `prive` et `public` (listes de noms de fichiers, ou None si le dossier
      `.github/workflows` manque), `series` (nombre d'exécutions distinctes vues dans `series-longues/*`, ou None),
      `derniere_serie` (datetime de Paris ou None), `pourquoi_traces` (texte quand les références sont partielles).
      [rend: 1]
    ⑥ TRAITEMENT — Lister les `.yml` et `.yaml` des deux dossiers de circuits ; si les références sont complètes
      (`etat_des_references`), lister les références
      `refs/remotes/origin/series-longues/<numéro>/…`, compter les numéros distincts, garder la date de commit la plus
      récente.
    ⑦ UNITÉ — Fichiers ; exécutions ; dates de Paris.
    ⑧ POURQUOI — A-805 : les circuits de séries longues GitHub étaient inutilisés et aucun regard ne le disait.
    ⑨ CE QUI CLOCHE — Voir ⑨ ① du fichier : ni les exécutions en cours, ni les minutes consommées, ni les files
      d'attente de GitHub ne sont visibles sans son interface de programmation.
    ⑩ EFFET — Lit des dossiers ; lance `git` en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = {"prive": None, "public": None, "series": None, "derniere_serie": None, "pourquoi_traces": None}
    for cle, base in (("prive", racine), ("public", pub)):
        dossier = os.path.join(base, ".github", "workflows")
        if os.path.isdir(dossier):
            m[cle] = sorted(f for f in os.listdir(dossier) if f.endswith((".yml", ".yaml")))
    m["pourquoi_traces"], _, _ = etat_des_references(racine, delai)
    code, sortie, raison = lancer(["git", "-C", racine, "for-each-ref", "--format=%(committerdate:unix)\t%(refname)",
                                   "refs/remotes/origin/series-longues"], delai)
    if not m["pourquoi_traces"] and (code != 0 or sortie is None):
        m["pourquoi_traces"] = echec("git for-each-ref", code, raison)
    if code == 0 and sortie is not None and not m["pourquoi_traces"]:
        numeros, dates = set(), []
        for l in sortie.splitlines():
            if "\t" not in l:
                continue
            date, nom = l.split("\t", 1)
            morceaux = nom.split("/")
            if len(morceaux) > 4:
                numeros.add(morceaux[4])
                dates.append(int(date))
        m["series"] = len(numeros)
        m["derniere_serie"] = datetime.fromtimestamp(max(dates), PARIS) if dates else None
    return m


def mesurer_forfait(programme, delai):
    """Appelle `TENIR_LE_FORFAIT.py --etat`, s'il existe, et en lit le seuil, la projection et le verdict.

    ① RÔLE — Mettre le forfait dans le même tableau que les machines, sans refaire son calcul (R-708).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `programme` : le chemin de TENIR_LE_FORFAIT.py · `delai` : secondes laissées au programme.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire `code` (entier ou None), `seuil`, `jauge`, `projection` (nombres ou
      None), `verdict` (texte ou None), `pourquoi`.
      [rend: 1]
    ⑥ TRAITEMENT — Si le programme manque : `pourquoi` le dit. Sinon le lancer avec `--etat`, puis lire dans sa
      sortie « seuil <n> % », « JAUGE ESTIMÉE MAINTENANT : <n> % », « PROJECTION À LA REMISE : <n> % » et
      « VERDICT : <texte> ».
    ⑦ UNITÉ — Points de jauge (%).
    ⑧ POURQUOI — A-804 (15-11-2026) : le forfait est une étape obligatoire du plan tenue par un programme ; A-805 le
      met dans le tableau du regard.
    ⑨ CE QUI CLOCHE — Voir ⑨ ③ du fichier : couplage par le texte de la sortie.
    ⑩ EFFET — Lance un programme qui, avec `--etat`, n'écrit rien.
    ⑪ TERMINAISON — Rend la main au plus tard après `delai` secondes.
      [sort: non]
    """
    m = {"code": None, "seuil": None, "jauge": None, "projection": None, "verdict": None, "pourquoi": None}
    if not os.path.isfile(programme):
        m["pourquoi"] = f"{os.path.basename(programme)} absent de ce dépôt"
        return m
    code, sortie, raison = lancer([sys.executable, "-B", programme, "--etat"], delai)
    if code is None:
        m["pourquoi"] = f"le programme du forfait : {raison}"
        return m
    m["code"] = code
    motifs = {"seuil": r"seuil ([0-9]+(?:[.,][0-9]+)?) %",
              "jauge": r"JAUGE ESTIMÉE MAINTENANT : ([0-9]+(?:[.,][0-9]+)?) %",
              "projection": r"PROJECTION À LA REMISE : ([0-9]+(?:[.,][0-9]+)?) %"}
    for cle, motif in motifs.items():
        t = re.search(motif, sortie or "")
        m[cle] = float(t.group(1).replace(",", ".")) if t else None
    t = re.search(r"(?m)^VERDICT : (.+)$", sortie or "")
    m["verdict"] = t.group(1).strip() if t else None
    return m


def juger_par_seuils(valeur, sature, sous, plus_est_sature):
    """Rend le verdict d'une valeur entre deux seuils.

    ① RÔLE — Un seul endroit pour la comparaison aux seuils, avec des bords écrits une fois.
    ② CONTEXTE D'APPEL — Les fonctions `ligne_*`.
    ③ ENTRÉE — `valeur` : le nombre mesuré (ou None) · `sature` : le seuil de saturation · `sous` : le seuil de
      sous-emploi, ou None quand la ressource n'a pas d'état SOUS-EMPLOYÉ · `plus_est_sature` : vrai quand une valeur
      haute veut dire saturé (charge), faux quand une valeur basse le veut dire (place libre).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : SOUS-EMPLOYÉ, JUSTE, SATURÉ, ou INCONNU si `valeur` est None.
      [rend: 1]
    ⑥ TRAITEMENT — Valeur haute saturante : SATURÉ si valeur ≥ sature, SOUS-EMPLOYÉ si valeur < sous. Valeur basse
      saturante : SATURÉ si valeur < sature, SOUS-EMPLOYÉ si valeur > sous. Sinon JUSTE.
    ⑦ UNITÉ — Celle de la valeur et des seuils, qui doit être la même.
    ⑧ POURQUOI — Les bords (≥ ou >) décident au cas exact ; écrits une fois, ils ne divergent pas d'une ligne à
      l'autre.
    ⑨ CE QUI CLOCHE — Deux lignes ont un bord strict des deux côtés et ne passent pas par ici : les épreuves (SATURÉ
      au-dessus strict, une épreuve par cœur est juste) et le forfait (SATURÉ au-dessus strict de seuil + écart).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if valeur is None:
        return INCONNU
    if plus_est_sature:
        if valeur >= sature:
            return "SATURÉ"
        if sous is not None and valeur < sous:
            return "SOUS-EMPLOYÉ"
        return "JUSTE"
    if valeur < sature:
        return "SATURÉ"
    if sous is not None and valeur > sous:
        return "SOUS-EMPLOYÉ"
    return "JUSTE"


def ligne_coeurs(m, r):
    """Fait la ligne du tableau pour les cœurs et la charge.

    ① RÔLE — Mettre en mots la mesure des cœurs et son verdict.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_coeurs` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes (ressource, existe, utilisé, verdict, critère).
      [rend: 1]
    ⑥ TRAITEMENT — Charge par cœur = charge de la fenêtre réglée (1, 5 ou 15 minutes, borne vérifiée par
      `lire_reglages`) ÷ cœurs ; juger contre les deux seuils.
    ⑦ UNITÉ — Tâches prêtes par cœur.
    ⑧ POURQUOI — Voir `mesurer_coeurs`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fenetres = {1: 0, 5: 1, 15: 2}
    f = int(r["coeurs_fenetre_minutes"])
    existe = f"{m['coeurs']} cœurs" if m["coeurs"] else INCONNU
    utilise = ("charge " + " / ".join(fr(c) for c in m["charges"]) + " (1/5/15 min)") if m["charges"] else INCONNU
    par_coeur = m["charges"][fenetres[f]] / m["coeurs"] if m["coeurs"] and m["charges"] else None
    v = juger_par_seuils(par_coeur, r["coeurs_charge_par_coeur_saturee"],
                         r["coeurs_charge_par_coeur_sous_employee"], True)
    if v == INCONNU:
        critere = m["pourquoi"] or "mesure incomplète"
    else:
        s, b = r["coeurs_charge_par_coeur_saturee"], r["coeurs_charge_par_coeur_sous_employee"]
        valeur = fr_face_au_seuil(par_coeur, plus_proche(par_coeur, s, b))
        critere = f"charge {f} min par cœur = {valeur} ; SATURÉ si ≥ {fr(s)}, SOUS-EMPLOYÉ si < {fr(b)}"
    return ["Cœurs", existe, utilise, v, critere]


def ligne_memoire(m, r):
    """Fait la ligne du tableau pour la mémoire.

    ① RÔLE — Mettre en mots la mesure de la mémoire et son verdict.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_memoire` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Part disponible = disponible ÷ total ; juger, une part basse étant saturante.
    ⑦ UNITÉ — Gigaoctets ; part (0 à 1).
    ⑧ POURQUOI — Voir `mesurer_memoire`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    part = m["disponible"] / m["total"] if m["total"] else None
    v = juger_par_seuils(part, r["memoire_part_disponible_saturee"], r["memoire_part_disponible_sous_employee"], False)
    if v == INCONNU:
        return ["Mémoire", INCONNU, INCONNU, v, m["pourquoi"] or "mesure incomplète"]
    return ["Mémoire", f"{fr(m['total'] / GO, 1)} Go", f"{fr((m['total'] - m['disponible']) / GO, 1)} Go pris, "
            f"{fr(m['disponible'] / GO, 1)} Go disponibles", v,
            f"part disponible = {fr_face_au_seuil(part, plus_proche(part, r['memoire_part_disponible_saturee'], r['memoire_part_disponible_sous_employee']))} ; "
            f"SATURÉ si < {fr(r['memoire_part_disponible_saturee'])}, "
            f"SOUS-EMPLOYÉ si > {fr(r['memoire_part_disponible_sous_employee'])}"]


def ligne_disque(m, r):
    """Fait la ligne du tableau pour le disque.

    ① RÔLE — Mettre en mots la mesure du disque et son verdict.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_disque` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Juger la place libre en gigaoctets ; pas d'état SOUS-EMPLOYÉ.
    ⑦ UNITÉ — Gigaoctets (10^9 octets).
    ⑧ POURQUOI — Voir `mesurer_disque`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    libre = m["libre"] / GO if m["libre"] is not None else None
    v = juger_par_seuils(libre, r["disque_libre_sature_go"], None, False)
    if v == INCONNU:
        return ["Disque", INCONNU, INCONNU, v, m["pourquoi"] or "mesure incomplète"]
    return ["Disque", f"{fr(m['total'] / GO, 1)} Go", f"{fr_face_au_seuil(libre, r['disque_libre_sature_go'], 1)} Go libres", v,
            f"SATURÉ si < {fr(r['disque_libre_sature_go'], 1)} Go libres (pas de sous-emploi pour un disque)"]


def ligne_epreuves(e, m_coeurs, r):
    """Fait la ligne du tableau pour les épreuves en cours.

    ① RÔLE — Mettre en mots le nombre d'épreuves qui tournent, rapporté aux cœurs.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `e` : la mesure de `compter_epreuves` · `m_coeurs` : la mesure de `mesurer_coeurs` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Épreuves par cœur = n ÷ cœurs ; SATURÉ au-dessus STRICT du seuil (une par cœur est juste),
      SOUS-EMPLOYÉ en dessous strict de l'autre, sinon JUSTE ; comparaison écrite ici (voir ⑨ de `juger_par_seuils`).
    ⑦ UNITÉ — Processus par cœur.
    ⑧ POURQUOI — Voir `compter_epreuves`.
    ⑨ CE QUI CLOCHE — Sans cœurs connus, le compte s'affiche mais le verdict est INCONNU.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    n = e["nombre"]
    existe = f"{m_coeurs['coeurs']} cœurs" if m_coeurs["coeurs"] else INCONNU
    utilise = (f"{n} épreuve{'s' if n > 1 else ''}" + (f" ({e['reserve']})" if e["reserve"] else "")
               if n is not None else INCONNU)
    par_coeur = n / m_coeurs["coeurs"] if n is not None and m_coeurs["coeurs"] else None
    if par_coeur is None:
        v = INCONNU
    elif par_coeur > r["epreuves_par_coeur_saturees"]:
        v = "SATURÉ"
    elif par_coeur < r["epreuves_par_coeur_sous_employees"]:
        v = "SOUS-EMPLOYÉ"
    else:
        v = "JUSTE"
    critere = ("cœurs ou processus illisibles" if v == INCONNU else
               f"épreuves par cœur = {fr_face_au_seuil(par_coeur, plus_proche(par_coeur, r['epreuves_par_coeur_saturees'], r['epreuves_par_coeur_sous_employees']))} ; "
               f"SATURÉ si > {fr(r['epreuves_par_coeur_saturees'])}, "
               f"SOUS-EMPLOYÉ si < {fr(r['epreuves_par_coeur_sous_employees'])}")
    return ["Épreuves en cours", existe, utilise, v, critere]


def ligne_worktrees(m, r):
    """Fait la ligne du tableau pour les copies de travail.

    ① RÔLE — Mettre en mots le nombre et la taille des copies de travail.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_worktrees` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Juger le nombre ; pas d'état SOUS-EMPLOYÉ ; la taille est affichée, ou INCONNU.
    ⑦ UNITÉ — Copies ; gigaoctets.
    ⑧ POURQUOI — Voir `mesurer_worktrees`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    v = juger_par_seuils(m["nombre"], r["worktrees_nombre_sature"], None, True)
    if v == INCONNU:
        return ["Copies de travail (worktree)", INCONNU, INCONNU, v, m["pourquoi"] or "mesure incomplète"]
    taille = f"{fr(m['taille'] / GO, 1)} Go" if m["taille"] is not None else f"taille {INCONNU} ({m['pourquoi']})"
    return ["Copies de travail (worktree)", f"{m['nombre']} hors dépôt principal", taille, v,
            f"SATURÉ si ≥ {int(r['worktrees_nombre_sature'])} copies"]


def ligne_copies_tmp(m, r):
    """Fait la ligne du tableau pour /tmp.

    ① RÔLE — Mettre en mots le nombre de copies du dépôt dans /tmp et la place que /tmp occupe.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_copies_tmp` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Juger la taille en gigaoctets ; pas d'état SOUS-EMPLOYÉ.
    ⑦ UNITÉ — Dossiers ; gigaoctets.
    ⑧ POURQUOI — Voir `mesurer_copies_tmp`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if m["copies"] is None:
        return ["Copies dans /tmp", INCONNU, INCONNU, INCONNU, m["pourquoi"]]
    taille = m["taille"] / GO if m["taille"] is not None else None
    v = juger_par_seuils(taille, r["copies_tmp_go_saturees"], None, True)
    utilise = f"{fr_face_au_seuil(taille, r['copies_tmp_go_saturees'], 1)} Go" if taille is not None else INCONNU
    critere = (m["pourquoi"] if v == INCONNU else f"SATURÉ si /tmp ≥ {fr(r['copies_tmp_go_saturees'], 1)} Go")
    return ["Copies dans /tmp", f"{m['copies']} copies du dépôt sur {m['dossiers']} dossiers", utilise, v, critere]


def ligne_cowork(m, r, maintenant):
    """Fait la ligne du tableau pour Cowork.

    ① RÔLE — Mettre en mots la dernière relecture de Cowork et les branches qui l'attendent.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_cowork` · `r` : les réglages · `maintenant` : l'heure du relevé (Paris).
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — SATURÉ si les branches en attente atteignent le seuil ; SOUS-EMPLOYÉ si aucune n'attend, ou si la
      dernière relecture date de plus que le seuil d'heures ; sinon JUSTE.
    ⑦ UNITÉ — Branches ; heures.
    ⑧ POURQUOI — Voir `mesurer_cowork`.
    ⑨ CE QUI CLOCHE — Aucune relecture trouvée et des branches en attente : SOUS-EMPLOYÉ (Cowork n'a rien produit).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if m["en_attente"] is None:
        return ["Cowork (relecture)", INCONNU, INCONNU, INCONNU, m["pourquoi"] or "mesure incomplète"]
    rap = (m["rapatriement"].strftime("%d-%m %Hh%M") if m["rapatriement"]
           else f"{INCONNU} (aucun git fetch depuis le clone)")
    der = m["derniere"].strftime("%d-%m %Hh%M") if m["derniere"] else "aucune"
    silence = (maintenant - m["derniere"]).total_seconds() / 3600 if m["derniere"] else None
    n = len(m["en_attente"])
    if n >= r["cowork_attente_saturee"]:
        v = "SATURÉ"
    elif n == 0 or silence is None or silence > r["cowork_silence_heures_sous_employe"]:
        v = "SOUS-EMPLOYÉ"
    else:
        v = "JUSTE"
    attente = f"{n} en attente" + (" : " + ", ".join(m["en_attente"]) if n else "")
    return ["Cowork (relecture)", f"{m['branches']} branches travail-*",
            f"dernière relecture {der} ; {attente}", v,
            f"SATURÉ si ≥ {int(r['cowork_attente_saturee'])} en attente ; SOUS-EMPLOYÉ si 0 en attente ou "
            f"silence > {fr(r['cowork_silence_heures_sous_employe'], 0)} h"
            + (f" (silence {fr(silence, 1)} h)" if silence is not None else "")
            + f" ; références du rapatriement du {rap}"
            + (" ; clone superficiel : une relecture plus ancienne que la profondeur rapatriée n'est pas vue"
               if m["superficiel"] else "")]


def ligne_circuits(m):
    """Fait la ligne du tableau pour les circuits GitHub.

    ① RÔLE — Dire quels circuits existent, et que leur usage réel ne se voit pas d'ici.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_circuits`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes ; le verdict est toujours INCONNU.
      [rend: 1]
    ⑥ TRAITEMENT — Compter les fichiers de chaque dépôt (INCONNU pour un dépôt sans dossier de circuits), dire
      `series_longues.yml` s'il est présent, rendre les traces de séries comme ce qu'elles sont.
    ⑦ UNITÉ — Fichiers ; exécutions.
    ⑧ POURQUOI — Voir `mesurer_circuits`.
    ⑨ CE QUI CLOCHE — Voir ⑨ ① du fichier.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    prive = f"{len(m['prive'])} privés" if m["prive"] is not None else f"privés {INCONNU}"
    public = f"{len(m['public'])} publics" if m["public"] is not None else f"publics {INCONNU} (clone absent)"
    longues = " dont series_longues.yml" if m["public"] and "series_longues.yml" in m["public"] else ""
    if m["series"] is None:
        traces = f"traces {INCONNU}" + (f" ({m['pourquoi_traces']})" if m["pourquoi_traces"] else "")
    else:
        traces = f"traces au dépôt : {m['series']} séries longues rapatriées" + (
            f", dernière le {m['derniere_serie'].strftime('%d-%m %Hh%M')}" if m["derniere_serie"] else "")
    return ["Circuits GitHub", f"{prive}, {public}{longues}", traces, INCONNU,
            "usage réel (exécutions en cours, minutes) non visible d'ici, sans l'interface de GitHub"]


def ligne_forfait(m, r):
    """Fait la ligne du tableau pour le forfait.

    ① RÔLE — Traduire l'état rendu par TENIR_LE_FORFAIT.py en verdict du tableau.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `m` : la mesure de `mesurer_forfait` · `r` : les réglages.
    ④ CONDITIONS D'ENTRÉE — `r` vient de `lire_reglages`.
    ⑤ SORTIE — UNE valeur : la ligne, liste de cinq textes.
      [rend: 1]
    ⑥ TRAITEMENT — Code 4 (arrêter les nouveaux agents) : SATURÉ. Code 3 (alerter) : JUSTE. Code 0 (continuer) :
      projection à la remise < seuil − écart → SOUS-EMPLOYÉ, > seuil + écart → SATURÉ, sinon JUSTE ; projection ou
      seuil illisible → INCONNU. Programme absent, sans réponse, autre code → INCONNU.
    ⑦ UNITÉ — Points de jauge (%).
    ⑧ POURQUOI — Préférence de Jean-Luc du 09-11-2026 : le seuil est une cible à atteindre à la remise, pas un frein.
    ⑨ CE QUI CLOCHE — Le code 3 (alerte) est JUSTE même si la projection dépasse : l'alerte est déjà dite par le
      programme du forfait, dont le verdict est recopié dans la colonne « utilisé ».
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if m["code"] is None:
        return ["Forfait", INCONNU, INCONNU, INCONNU, m["pourquoi"]]
    jauge = f"jauge {fr(m['jauge'], 1)} %" if m["jauge"] is not None else f"jauge {INCONNU}"
    proj = f"projection {fr(m['projection'], 1)} %" if m["projection"] is not None else f"projection {INCONNU}"
    existe = f"seuil {fr(m['seuil'], 0)} %" if m["seuil"] is not None else f"seuil {INCONNU}"
    utilise = f"{jauge} ; {proj} ; verdict du forfait : {m['verdict'] or INCONNU}"
    e = r["forfait_ecart_points"]
    if m["code"] == 4:
        v, critere = "SATURÉ", "le programme du forfait dit d'arrêter les nouveaux agents (code 4)"
    elif m["code"] == 3:
        v, critere = "JUSTE", "le programme du forfait alerte (code 3) : près du seuil"
    elif m["code"] == 0 and m["projection"] is not None and m["seuil"] is not None:
        p = m["projection"]
        v = "SATURÉ" if p > m["seuil"] + e else "SOUS-EMPLOYÉ" if p < m["seuil"] - e else "JUSTE"
        critere = (f"projection à la remise ; SOUS-EMPLOYÉ si < seuil − {fr(e, 0)}, SATURÉ si > seuil + {fr(e, 0)}")
    else:
        v, critere = INCONNU, f"code {m['code']} du programme du forfait, ou projection illisible"
    return ["Forfait", existe, utilise, v, critere]


def afficher(lignes, maintenant, chemin_reglages):
    """Affiche le tableau et le compte des verdicts.

    ① RÔLE — Rendre le relevé lisible par le Chat, qui le montre à Jean-Luc tel quel.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `lignes` : les lignes des fonctions `ligne_*` · `maintenant` : l'heure du relevé · `chemin_reglages` :
      le fichier des seuils, nommé en tête.
    ④ CONDITIONS D'ENTRÉE — Chaque ligne a cinq textes.
    ⑤ SORTIE — Rien : affiche.
      [rend: rien]
    ⑥ TRAITEMENT — Une ligne d'en-tête, un tableau à barres verticales (lisible en texte et en Markdown), une ligne
      « VERDICTS : » qui compte chaque verdict.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-805 : Jean-Luc veut voir le même tableau que le Chat à chaque regard.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sur la sortie standard.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    print(f"PÉRIMÈTRE — {maintenant.strftime('%d-%m-%Y %Hh%M')} (Paris) · seuils : {chemin_reglages}")
    print("| Ressource | Existe | Utilisé | Verdict | Critère |")
    print("|---|---|---|---|---|")
    for l in lignes:
        print("| " + " | ".join(t.replace("|", "/") for t in l) + " |")
    compte = {v: sum(1 for l in lignes if l[3] == v) for v in ("SOUS-EMPLOYÉ", "JUSTE", "SATURÉ", INCONNU)}
    print("VERDICTS : " + " · ".join(f"{v} {n}" for v, n in compte.items()) + f" · LIGNES {len(lignes)}")


def main(arguments):
    """Lit les réglages, mesure les neuf ressources, juge, affiche, et sort.

    ① RÔLE — Enchaîner le relevé de bout en bout.
    ② CONTEXTE D'APPEL — Le bas de ce fichier, à son lancement.
    ③ ENTRÉE — `arguments` : la ligne de commande, sans le nom du programme (voir ③ du fichier).
    ④ CONDITIONS D'ENTRÉE — Voir ④ du fichier.
    ⑤ SORTIE — UNE valeur : le code de sortie, 0 (tableau rendu) ou 2 (réglage illisible ou absurde, racine qui n'est
      pas un dépôt Git).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les options · ② lire les réglages, sinon « ERREUR RÉGLAGE » et 2 · ②bis vérifier que la
      racine est un dépôt Git, sinon « ERREUR RACINE » et 2 (relecture de Cowork du 15-11-2026, D-5 : `--racine
      /inexistant` rendait un tableau et 0) · ③ noter l'heure de Paris ·
      ④ mesurer cœurs, mémoire, disque, épreuves, copies de travail, /tmp, Cowork, circuits, forfait · ⑤ faire les
      neuf lignes · ⑥ afficher · ⑦ rendre 0.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑧ du fichier.
    ⑨ CE QUI CLOCHE — Les mesures se font l'une après l'autre : le relevé dure le temps des deux `du` (16,6 s et 4,6 s
      mesurés le 15-11-2026 sur une machine chargée).
    ⑩ EFFET — Voir ⑩ du fichier.
    ⑪ TERMINAISON — Rend la main avec le code ; c'est le bas du fichier qui sort.
      [sort: non]
    """
    p = argparse.ArgumentParser(description="Relève le périmètre de travail et rend un tableau court.")
    p.add_argument("--racine", default=RACINE)
    p.add_argument("--pub", default="/home/claude/pub")
    p.add_argument("--reglages", default=None)
    p.add_argument("--proc", default="/proc")
    p.add_argument("--tmp", default="/tmp")
    p.add_argument("--disque", default=None)
    p.add_argument("--forfait", default=None)
    o = p.parse_args(arguments)
    reglages = o.reglages or os.path.join(o.racine, "donnees", "REGLAGES_DU_PERIMETRE.csv")
    try:
        r = lire_reglages(reglages)
    except (OSError, ValueError) as err:
        print(f"ERREUR RÉGLAGE : {err}")
        return 2
    delai = r["delai_de_mesure_secondes"]
    code, _, raison = lancer(["git", "-C", o.racine, "rev-parse", "--git-dir"], delai)
    if code != 0:
        print(f"ERREUR RACINE : {o.racine} — " + (echec("git rev-parse", code, raison) if raison
                                                  else "ce n'est pas un dépôt Git"))
        return 2
    maintenant = datetime.now(PARIS)
    coeurs = mesurer_coeurs(o.proc, delai)
    lignes = [
        ligne_coeurs(coeurs, r),
        ligne_memoire(mesurer_memoire(o.proc), r),
        ligne_disque(mesurer_disque(o.disque or o.racine), r),
        ligne_epreuves(compter_epreuves(o.proc, o.racine), coeurs, r),
        ligne_worktrees(mesurer_worktrees(o.racine, delai), r),
        ligne_copies_tmp(mesurer_copies_tmp(o.tmp, delai), r),
        ligne_cowork(mesurer_cowork(o.racine, delai), r, maintenant),
        ligne_circuits(mesurer_circuits(o.racine, o.pub, delai)),
        ligne_forfait(mesurer_forfait(o.forfait or os.path.join(o.racine, "programmes", "TENIR_LE_FORFAIT.py"),
                                      delai), r),
    ]
    afficher(lignes, maintenant, reglages)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
