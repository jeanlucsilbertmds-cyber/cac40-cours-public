#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCIDÉ · outil · v1.0 · 02-09-2026 · Rôle : tenir les positions du soir.

CE QUE CE PROGRAMME REMPLACE, ET POURQUOI IL EXISTE
====================================================
Une consigne en français, appliquée à la main avant ce module, décrivait une suite de
calculs : clôturer les positions dont le stop ou l'objectif est touché, entrer
celles qui attendaient, ouvrir les nouvelles. Chaque soir, un agent relit ce
texte et le refait à sa façon.

UN AGENT NE REPRODUIT PAS. IL REFORMULE. C'est structurel, et cela ne se
corrige par aucune vigilance. Le 01-09-2026 la tâche d'audit a réécrit son
propre script « de mémoire » : 33 623 octets au lieu de 62 922, la moitié
perdue, et le rapport annonçait « seuls les commentaires d'en-tête ». C'était
faux. Six incidents de transport en trois jours l'avaient déjà montré.

Un programme, lui, fait deux fois la même chose. C'est la seule différence qui
compte, et c'est Jean-Luc qui l'a nommée le 02-09-2026 : « on a des programmes
déterministes, ils sont déterministes, et tout le reste n'est pas fiable ».

CE QUE CE PROGRAMME NE FAIT PAS — ne jamais réécrire ce qui existe déjà (R-708)
========================================
Il NE RÉIMPLÉMENTE AUCUN CALCUL. Pas un seul. Les frais, le gain net, les
paramètres d'entrée, le test d'une séance : tout vient de MODULE POSITIONS, par
import. Si ce module change, ce programme suit sans être touché.
Deux implémentations d'une même chose divergent toujours — c'est mathématique,
pas une question d'attention.

Il n'écrit AUCUN fichier. Il rend des structures ; l'appelant écrit. Ainsi il
se teste sans rien casser, et le transport reste un geste séparé et visible.

CE QU'IL FAIT, DANS L'ORDRE EXACT DU PROMPT
============================================
  A) les ÉCHÉANCES d'abord — recalculées depuis la séance d'achat (27-09-2026)
  B) les CLÔTURES ensuite   — une position ouverte peut sortir aujourd'hui
  C) les ENTRÉES ensuite    — une position en attente devient ouverte
  D) les SIGNAUX en dernier — les nouveaux signaux créent des attentes

Cet ordre n'est pas indifférent : une position clôturée ce matin LIBÈRE le
jeton unique, et un signal du soir peut alors entrer. L'inverse le bloquerait
à tort.

CE QUE CE PROGRAMME EMPRUNTE AU MODULE, ET CE QU'IL NE LUI EMPRUNTE PAS
=======================================================================
Il emprunte `tester_seance` et `frais_ordre` : ces deux-la ne dependent
d'AUCUN reglage de strategie. Un taux de frais ne se recopie jamais.

Il n'emprunte NI `sortie_position` NI `parametres_entree`, aux DEUX bouts du
trade — a l'entree comme a la sortie. Ce n'a pas toujours ete vrai : le 03/09,
`entrer()` appelait encore `parametres_entree`, et une position MA200-S1
s'ouvrait donc avec les seuils de la strategie C5-ETENDU-10. L'erreur etait ecrite a l'ouverture,
puis exactement executee a la cloture. Corrige : les seuils viennent du
parametre `reglages`, que l'appelant tire du registre.
Ces deux fonctions RECALCULENT les seuils depuis deux constantes fixes du
module — TP_PCT 4,0 % et SL_PCT 2,5 %. Or le registre porte des seuils PAR
STRATEGIE : MA200-S1, en PRODUCTION, est a +5,0 % / -2,0 %. Une position de
cette strategie aurait ete cloturee aux seuils d'une AUTRE, EN SILENCE.
Releve le 02-09-2026 : aucun autre programme du projet ne les appelle. Le
juge des stratégies, lui, lit les seuils de la fiche depuis toujours. Ce programme fait
pareil. C'est la seule facon de servir plusieurs strategies sans toucher au
module — donc sans toucher au juge des stratégies ni au radar qui en dependent.

LE CHARGEMENT DES COURS APPARTIENT AU JUGE DES STRATÉGIES. `charger_cours(*chemins)` fusionne
plusieurs fichiers, rapproche les graphies par `cle_valeur`, dedoublonne par
date et TRIE. Deux pieges y sont resolus depuis toujours : les cours vivent
dans DEUX fichiers — `cac40 ohlcv.csv` s'arrete au 10-07-2026 — et les deux
fichiers n'ecrivent pas le meme nom, « UNIBAIL-RODAMCO-WESTFIELD » contre
« UNIBAIL_RODAMCO ».

════════════════════════════════════════════════════════════════════════
LES ONZE ELEMENTS — ce programme est une fonction comme les autres
════════════════════════════════════════════════════════════════════════
① ROLE — **LE PAS N°6 DU CIRCUIT DU SOIR**, apres la detection. Il cloture ce
  qui doit l etre, ouvre ce que les signaux commandent, et enregistre. **C est
  le seul programme qui touche a l argent simule.**
② CONTEXTE D APPEL — Le circuit du soir, apres le detecteur. **Entree a l Open
  de J+1 : ce programme decide la veille pour le lendemain.**
③ ENTREE — La ligne de commande : la racine du depot, ou `.` a defaut, et
  `--calibrage` pour ne faire que le calibrage. **Et quatre fichiers** : les
  signaux du jour, les positions ouvertes, le journal des trades, les cours.
④ CONDITIONS D ENTREE — Le module de positions doit etre trouvable, et le
  registre des regles lisible. **`programmes/CONTRATS_DES_FICHIERS.py` doit etre
  a cote de ce programme** : depuis le 27-09-2026, les colonnes du journal et des
  positions et les deux comptabilites y sont lues au chargement ; sans lui, le
  programme s arrete sur « ModuleNotFoundError ». **Les fichiers de travail peuvent tous manquer :
  c est le premier soir.**
⑤ SORTIE — **Un code de sortie, et deux fichiers reecrits.**
⑥ TRAITEMENT — ① charger le module et lire les reglages AU REGISTRE ·
  ② **CALIBRER sur un trade connu, et s arreter s il ne tombe pas au centime** ·
  ③ cloturer les positions qui touchent leur cible, leur stop ou leur echeance ·
  ④ ouvrir sur les signaux du jour, **une position au plus par strategie** ·
  ⑤ reecrire les positions et le journal.
⑦ UNITE — **Les montants sont en euros, les seuils en POURCENTS, l horizon en
  JOURS DE BOURSE et non en jours calendaires.** Les frais sont un taux, ecrit
  a un seul endroit — `MODULE_POSITIONS.FRAIS_TAUX` — et tout autre programme
  le LIT.
⑧ POURQUOI — **Les seuils d objectif et de stop, et le nombre de seances avant
  echeance, sont lus dans `donnees/cac40_strategies.csv`, jamais ecrits dans le
  code.** C est la seule facon de servir plusieurs strategies sans toucher au
  module, donc sans toucher au juge des stratégies ni au radar qui en dependent.
  **Et le calibrage precede tout** : un moteur qui ne rejoue pas un trade connu
  au centime ne peut rien affirmer des trades a venir.
⑨ CE QUI CLOCHE — **Quatre silences** — le ⑨ se consigne et ne se corrige pas (R-752) :
  · **`_ecrire_csv` jette silencieusement toute colonne absente de sa liste**, et
    cela touchait le journal des trades : la comptabilite de chaque cloture etait
    jetee. CORRIGE LE 27-09-2026 EN AMONT (defaut 3 de A-491) : les colonnes
    viennent du contrat et `fautes_d_ecriture` refuse avant d ecrire ;
  · **l ecriture n est pas atomique** : une interruption laisse un journal
    tronque, et rien ne le detecterait au passage suivant ;
  · **`_ancien_main` est du code mort** qui ressemble a `main` a s y meprendre,
    et porte une explication que personne ne lira la ou elle sert ;
  · **`_lire_csv` rend une liste vide pour un fichier absent ET pour un fichier
    sans lignes** : l appelant ne peut pas distinguer le premier soir d un
    fichier vide.
⑩ EFFET — **REECRIT `donnees/claude_positions_ouvertes.csv` et
  `donnees/claude_journal_trades.csv` EN ENTIER** · **cree les dossiers
  manquants** · **EXECUTE le code du juge des stratégies et du module qu il charge.**
⑪ TERMINAISON — **`main` REND la main avec un code** — 0 si tout va ; en
  calibrage seul, 1 s il echoue ; sur le chemin reel, les codes de
  `tenir_pour_de_vrai` : 2 si le calibrage echoue ou si une entree manque,
  1 sur une faute (signal hors contrat, valeur sans mnemonique, aucune
  strategie vivante, horizon illisible, faute d ecriture depuis le 27-09-2026)
  ou sur l alerte que rend `tenir` — et c est l appel du bas du fichier qui en fait un code de
  processus. **Mais `charger_module_positions` et `trouver_module`, appeles en
  premier, TERMINENT le programme si le module est introuvable.**

PREUVE QU'IL MESURE JUSTE, sur les vraies donnees du projet : rejoue sur la
position UNIBAIL du 21-08, il rend « 2026-08-27 · SL · 100,57125 ·
-2 796,25 EUR ». Le journal des trades porte exactement ces valeurs, produites
a la main par un agent le 30-08. Identique au centime.

⑫ DÉFINITIONS —
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont
    lus dans `donnees/cac40_strategies.csv`.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub
    Actions — collecte, versement, signaux, positions, mesure, surveillance.
  PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
  l horizon : le nombre de seances au bout duquel une position se ferme si ni l objectif ni le seuil de perte n ont ete touches.
  la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  le module de positions : `programmes/MODULE_POSITIONS.py`, propriétaire du taux de frais et des règles de sortie d'une position.
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
  un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
  un trade : une opération simulée, de l'achat à la revente
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""

import csv
import datetime
import importlib.util
import os
import sys

VERSION = "tenir-positions-1.0"

# les deux comptabilités — LUES dans le contrat, jamais recopiées (R-708). Depuis le
# 27-09-2026 : la mesure les lit au même endroit, un seul nom fait donc foi aux deux bouts.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import COMPTABILITES, TRADE, POSITION, UN_JETON, JETONS_ILLIMITES, noms_d_une_strategie
from COMMUN import lire_horizon                 # la seule lecture d'un horizon (R-708)

# les statuts d'une ligne de positions_ouvertes.csv
EN_ATTENTE = "EN_ATTENTE_ENTREE"
OUVERTE = "OUVERTE"

# valeur écrite dans les colonnes non encore connues, telle que le prompt l'exige
INCONNU = "EN_ATTENTE"


# ─────────────────────────────────────────────────────────────────────
# CHARGEMENT DU MODULE DES POSITIONS — jamais de copie de ses formules
# ─────────────────────────────────────────────────────────────────────
def charger_module_positions(chemin):
    """Importe MODULE POSITIONS depuis son chemin réel.

    LE NOM SE RELÈVE, IL NE SE DEVINE PAS — un nom se relève sur le fichier vivant, il ne se devine pas (R-719). Le fichier vivant s'écrit
    « MODULE POSITIONS.py » AVEC UN ESPACE ; trois consignes l'ont cité avec un
    souligné et ont échoué. On accepte donc les deux graphies, et on dit
    laquelle a répondu.

    ① RÔLE — Charger `programmes/MODULE_POSITIONS.py`, le moteur de calcul des positions,
      et **refuser tout de suite s il n expose pas ce dont on se sert.**
    ② CONTEXTE D APPEL — `main` et `tenir_pour_de_vrai`, en tout premier.
    ③ ENTRÉE — `chemin` : le chemin réel du module, tel que `trouver_module` l a
      relevé sur le disque.
    ④ CONDITIONS D ENTRÉE — **Le chemin doit exister** — la fonction lève sinon.
      C est voulu : sans moteur, rien ne peut être calculé.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier que le fichier est là · ② le charger · ③ **exiger
      qu il expose les deux fonctions qu on appelle**, et lever sinon.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Le fichier du moteur s écrit tantôt `MODULE POSITIONS.py` avec
      un espace, tantôt `MODULE_POSITIONS.py` avec un tiret bas.** Trois consignes
      l ont cité avec la mauvaise graphie et ont échoué à le charger. Les deux
      sont donc acceptées. **Et on n exige QUE ce qu on
      appelle** : exiger plus ferait échouer sur des fonctions dont on ne se sert
      plus, ce qui est une fausse alerte.
    ⑨ CE QUI CLOCHE — **La liste des deux fonctions exigées est écrite ici, et
      les appels réels sont ailleurs.** Si un appel nouveau apparaissait, rien ne
      forcerait à l ajouter à la liste — et l erreur se verrait à l exécution, au
      milieu d une tenue de positions.
    ⑩ EFFET — **EXÉCUTE le code du module chargé.**
    ⑪ TERMINAISON — **LÈVE** si le fichier est absent, ou si le module n expose
      pas ce qu on attend. Rend la main sinon.
      [sort: non]
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError("module des positions introuvable : " + chemin)
    spec = importlib.util.spec_from_file_location("mod_positions", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # on n'exige QUE ce qu'on appelle : `pnl_net` ne l'est plus depuis que
    # le gain est calcule sur les seuils de la position.
    for f in ("frais_ordre", "tester_seance"):
        if not hasattr(mod, f):
            raise RuntimeError("le module des positions n'expose pas " + f)
    return mod


def cle_valeur_du_banc(base):
    """Rend la fonction `cle_valeur` DU JUGE DES STRATÉGIES, jamais une copie.

    LES DEUX FICHIERS N'ECRIVENT PAS LE MEME NOM. Mesure du 02-09-2026 :
    `cac40 ohlcv.csv` porte « UNIBAIL-RODAMCO-WESTFIELD » quand
    `positions_ouvertes.csv` porte « UNIBAIL_RODAMCO ». Sans rapprochement, la
    position est declaree introuvable et reste ouverte a tort — c'est
    exactement ce qui a coute 26 pour cent d'une mesure le 23/08 — trois orthographes pour la même valeur ont fait perdre 26 % d'une mesure, en silence (A-264).
    Le juge des stratégies sait deja le faire. On IMPORTE sa fonction : deux implementations
    d'une meme regle divergent toujours — deux implémentations d'une même chose divergent toujours (R-708).

    ① RÔLE — Rendre LA fonction qui rapproche deux graphies d un même nom de
      valeur. **Pas une copie : celle du juge des stratégies `programmes/JUGE_DES_STRATEGIES.py`.**
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, une fois, pour la passer ensuite
      à `cloturer` et `entrer`.
    ③ ENTRÉE — `base` : la racine où chercher le juge des stratégies.
    ④ CONDITIONS D ENTRÉE — **Le juge des stratégies doit exister et exposer `cle_valeur`** —
      la fonction lève sinon.
    ⑤ SORTIE — UNE valeur : la fonction elle-même, prête à être appelée.
      [rend: 1]
    ⑥ TRAITEMENT — ① essayer les deux graphies du juge des stratégies, À LA RACINE seulement ·
      ② le charger · ③ rendre sa fonction si elle est là.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Une même entreprise s écrit différemment selon le fichier :
      `UNIBAIL-RODAMCO-WESTFIELD` dans les cours, `UNIBAIL_RODAMCO` dans les
      positions.** Sans rapprochement, la position est déclarée introuvable et
      **reste ouverte à tort, indéfiniment**. Le 23-08-2026, ce défaut a fait
      disparaître 26 % des lignes d une mesure, sans aucune erreur affichée.
    ⑨ CE QUI CLOCHE — **Elle ne cherche qu À LA RACINE, là où `trouver_module` et
      `_banc` descendent dans l arborescence.** Au dépôt, les programmes vivent
      dans `programmes/` : lancée depuis la racine, elle lève. **C est le défaut
      corrigé le 12-09 sur `trouver_module`, et il vit encore ici.**
    ⑩ EFFET — **EXÉCUTE le code du juge des stratégies chargé.**
    ⑪ TERMINAISON — **LÈVE** si le juge des stratégies est introuvable ou muet. Rend la main
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for nom in ("JUGE_DES_STRATEGIES.py", "JUGE DES STRATEGIES.py"):
        p = os.path.join(base, nom)
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location("_banc", p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            if hasattr(m, "cle_valeur"):
                return m.cle_valeur
    raise FileNotFoundError(
        "le juge des stratégies est introuvable : impossible d'importer `cle_valeur`. "
        "On ne la reecrit PAS — sans elle, les noms ne se rapprochent pas.")


def reglages_du_registre(base):
    """Lit les seuils de CHAQUE strategie dans `cac40_strategies.csv`.

    POURQUOI CETTE FONCTION EXISTE, ET C'EST UN DEFAUT QU'ELLE REPARE.
    Le 03-09-2026, `entrer()` a cesse d'appeler `parametres_entree` du module —
    a juste titre, il imposait +4,0 / -2,5 a toutes les strategies. Mais le
    parametre `reglages` valait `None` par defaut : appele comme le
    circuit du soir l'appelle, le programme n'ouvrait PLUS AUCUNE POSITION. Jamais. Proprement,
    sans erreur, avec une ligne d'incident dans un rapport que personne ne lit
    ligne a ligne. Et le programme de surveillance quotidienne aurait rendu « 0 position ouverte »
    AU VERT.
    Un defaut silencieux etait devenu un ARRET silencieux.
    On ne laisse donc pas l'appelant deviner : le programme sait lire lui-meme
    la source qui fait autorite.

    LA CLE EST L'IDENTIFIANT, ET AUSSI LE NOM — parce que les deux circulent.
    Le registre designe une strategie par son identifiant court, par exemple
    `C5E10-QA-V1` ; le journal des trades et les
    positions designent par `nom` (COURS_BAS_ARGENT_REVIENT_6). Les deux sont
    donc acceptes, et le nom est pris avant sa parenthese explicative.

    ① RÔLE — **Lire les seuils et l horizon de CHAQUE stratégie à la source qui
      fait autorité** — le registre des stratégies `donnees/cac40_strategies.csv`, jamais le code.
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, avant toute ouverture de position.
    ③ ENTRÉE — `base` : la racine du dépôt.
    ④ CONDITIONS D ENTRÉE — Aucune : un registre absent rend un dictionnaire vide.
    ⑤ SORTIE — UNE valeur : un dictionnaire des réglages, indexé À LA FOIS par
      identifiant et par nom.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir le registre · ② pour chaque stratégie, relever ses
      seuils et son horizon · ③ l indexer sous ses deux désignations.
    ⑦ UNITÉ — **Les seuils sont en POURCENTS, l horizon en JOURS DE BOURSE et
      non en jours calendaires.**
    ⑧ POURQUOI — **Les seuils d objectif et de stop diffèrent d une stratégie à
      l autre, et ils vivent dans `donnees/cac40_strategies.csv`.** Les lire ici
      évite que l appelant ait à les deviner. **C est le défaut le plus grave que
      ce programme ait connu :** **le 03-09-2026, il n ouvrait PLUS AUCUNE POSITION.
      Jamais. Proprement, sans erreur — et le programme de surveillance quotidienne
      rendait « 0 position ouverte » AU VERT. Un défaut silencieux était devenu un ARRÊT silencieux.**
    ⑨ CE QUI CLOCHE — **Un registre absent rend un dictionnaire vide, et rien ne
      le dit.** C est exactement le retour à l arrêt silencieux de septembre :
      sans réglages, aucune position ne s ouvre, et la sortie reste verte.
    ⑩ EFFET — Aucun : elle lit.
    ⑪ TERMINAISON — Rend toujours la main, dictionnaire vide compris.
      [sort: non]
    """
    import csv as _csv
    # QUATRIEME occurrence du meme defaut dans ce seul fichier, 12-09-2026 :
    # chercher a plat une source qui vit dans `donnees/`. Une fonction ecrite
    # pour reparer un arret silencieux etait elle-meme arretee en silence.
    for nom in ("donnees/cac40_strategies.csv", "cac40_strategies.csv",
                "cac40 strategies.csv", "donnees/cac40 strategies.csv"):
        p = os.path.join(base, nom)
        if not os.path.exists(p):
            continue
        r = {}
        with open(p, encoding="utf-8-sig", newline="") as f:
            for x in _csv.DictReader(f):
                try:
                    tp = float(str(x["tp"]).replace("%", "").replace(",", ".")
                               .replace("+", "").strip()) / 100.0
                    sl = abs(float(str(x["sl"]).replace("%", "").replace(",", ".")
                                   .replace("-", "").strip())) / 100.0
                except (KeyError, ValueError):
                    continue
                # les noms d'une strategie se lisent au contrat (R-708), une fois
                for k in sorted(noms_d_une_strategie(x)):
                    if k:
                        # W2 de Cowork, 12-09 : l horizon est une colonne PAR
                        # STRATEGIE, et le fichier s en sert — C4-RAV 3j,
                        # MA200-S1 20j, C5-EI-PARAMS 30. Deux vivantes d horizons
                        # differents n est donc PAS une anomalie : c est une
                        # configuration que l etat civil prevoit. Mon garde-fou
                        # l interdisait, et « il ne protegeait pas d un defaut,
                        # il masquait une limite de conception ».
                        # W1 : la graphie MAJORITAIRE du fichier porte un « j ».
                        # `isdigit()` l excluait, l ensemble tombait vide, et le
                        # repli code en dur s appliquait EN ANNONCANT une lecture
                        # du registre qui n avait pas eu lieu.
                        # UNE SEULE LECTURE DE L'HORIZON (R-708) : `lire_horizon`,
                        # aussi employee par le garde-fou `horizons_illisibles`.
                        r[k] = {"tp": tp, "sl": sl,
                                "horizon": lire_horizon(x.get("horizon", ""))}
        return r
    raise FileNotFoundError(
        "le registre des strategies est introuvable dans %r : sans lui, aucune "
        "position ne peut s'ouvrir, et ce silence serait invisible." % base)


def _fichiers_de_cours(base):
    """Delegue au juge des stratégies — UN SEUL point de decision sur les fichiers de cours.

    ① RÔLE — Dire QUELS fichiers de cours lire, sans le décider soi-même :
      c est le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py` qui les choisit.
    ② CONTEXTE D APPEL — `charger_cours_du_banc`, juste avant de charger.
    ③ ENTRÉE — `base` : la racine.
    ④ CONDITIONS D ENTRÉE — Aucune. **Un juge des stratégies absent est un cas prévu.**
    ⑤ SORTIE — **UNE valeur : ce que rend `fichiers_de_cours` de
      `programmes/JUGE_DES_STRATEGIES.py`, un tuple d'UN chemin, `donnees/cours_maitre.csv`.**
      Si le maître manque, ou si le juge des stratégies manque, elle ne rend rien : une erreur
      est levée (voir ⑪).
      [rend: 1]
    ⑥ TRAITEMENT — ① demander au juge des stratégies · ② **s il est absent, lever une erreur qui
      le nomme** — plus aucun chemin écrit ici en dur depuis le 24-09-2026 (A-442).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un seul point de décision sur les fichiers de cours : le juge des stratégies.
      **Dix-sept programmes nommaient jadis ces fichiers en dur, et le fichier
      maître existait pendant que personne ne le lisait.**
    ⑨ CE QUI CLOCHE — **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** **DEUX replis, et ils ne se valent pas.**
      **Le premier est voulu** : `programmes/JUGE_DES_STRATEGIES.py` rend les deux anciens
      fichiers quand le maître n existe pas, ce qui a permis de brancher les
      programmes un par un.
      **Le second est le mien, et il contredit la raison d être de la fonction.**
      Si le juge des stratégies manque, elle rend deux chemins écrits ici — **dont le fichier
      maître ne fait PAS partie.** Le programme tournerait alors sur des cours
      incomplets, sans un mot. **Un repli silencieux sur une valeur périmée est
      pire qu une levée.**
    ⑩ EFFET — Aucun en propre, mais `_banc` exécute le code du juge des stratégies.
    ⑪ TERMINAISON — **Lève `FileNotFoundError` quand le fichier maître ou le juge des stratégies
      manque**, avec un message qui le nomme — voulu depuis le 24-09-2026 (A-442).
      Sinon rend la main. **`_banc`, qu elle appelle, peut lever
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout l'historique des cours et n'est jamais réécrit.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for m in (_banc(base),):
        if m and hasattr(m, "fichiers_de_cours"):
            return m.fichiers_de_cours(base)
    # PLUS DE REPLI — A-442 : sans le juge des stratégies, personne ne designe le fichier maitre.
    raise FileNotFoundError(
        "ARRET : programmes/JUGE_DES_STRATEGIES.py, qui designe le fichier maitre des cours, est "
        "introuvable. Aucun repli sur les anciens fichiers de cours (A-442).")


def _banc(base):
    """Trouve et charge le juge des stratégies, où qu il soit dans l arborescence.

    ① RÔLE — Rendre le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py` sans qu on ait à
      savoir où il est rangé.
    ② CONTEXTE D APPEL — `_fichiers_de_cours` et `charger_cours_du_banc`, qui ont
      besoin du juge des stratégies pour savoir QUELS fichiers de cours lire.
    ③ ENTRÉE — `base` : la racine à fouiller.
    ④ CONDITIONS D ENTRÉE — Aucune. **Un dossier sans juge des stratégies est un cas prévu.**
    ⑤ SORTIE — UNE valeur : le module chargé, **ou `None` si le juge des stratégies est
      introuvable.**
      [rend: 1]
    ⑥ TRAITEMENT — ① descendre l arborescence · ② **écarter les dossiers
      d archives, de git, de cache et de travail** · ③ au premier juge des stratégies trouvé,
      le charger et le rendre · ④ sinon rendre `None`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Les quatre dossiers écartés le sont pour éviter de charger une
      version ARCHIVÉE du juge des stratégies** : les archives portent d anciennes versions, et
      la première trouvée aurait pu être la périmée.
    ⑨ CE QUI CLOCHE — **La première trouvée gagne, et l ordre de descente n est
      pas garanti.** Si deux juges des stratégies vivants coexistaient, celui qui est chargé
      dépendrait du système de fichiers — et rien ne le dirait.
    ⑩ EFFET — **EXÉCUTE le code du juge des stratégies trouvé.** Charger un module, c est le
      faire tourner : tout ce qu il fait au chargement est fait ici.
    ⑪ TERMINAISON — Rend toujours la main, `None` compris. **Mais l exécution du
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      les archives : le dossier archives/ du dépôt, où sont rangées les versions abandonnées, sous un nom qui dit pourquoi elles sont tombées
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import importlib.util as _ilu
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail")]
        if "JUGE_DES_STRATEGIES.py" in fs:
            sp = _ilu.spec_from_file_location("banc", os.path.join(r, "JUGE_DES_STRATEGIES.py"))
            m = _ilu.module_from_spec(sp)
            sp.loader.exec_module(m)
            return m
    return None


def charger_cours_du_banc(base, *chemins):
    """Rend les cours PAR LA FONCTION DU JUGE DES STRATÉGIES, jamais par une lecture maison.

    `charger_cours(*chemins)` fait DEJA les quatre choses dont ce programme a
    besoin, et il les fait a un seul endroit : il FUSIONNE plusieurs fichiers,
    RAPPROCHE les graphies par `cle_valeur`, DEDOUBLONNE par date, et TRIE.
    Les deux « pieges » que ce programme signalait dans son en-tete — les cours
    en deux fichiers, les deux graphies d'UNIBAIL — y sont resolus depuis
    toujours. Les redecouvrir ici aurait ete une seconde implementation de la
    meme regle, et deux implementations divergent toujours — deux implémentations d'une même chose divergent toujours (R-708).

    ① RÔLE — Rendre les cours prêts à l emploi, en déléguant tout au juge des stratégies
      `programmes/JUGE_DES_STRATEGIES.py`.
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, une fois, avant toute clôture.
    ③ ENTRÉE — `base` : la racine · `chemins` : des fichiers de cours choisis,
      **et l appelant n en passe aucun** : la fonction demande alors au juge des stratégies.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : les cours, fusionnés, rapprochés, dédoublonnés, triés.
      [rend: 1]
    ⑥ TRAITEMENT — ① si aucun chemin n est donné, demander au juge des stratégies lesquels lire
      · ② lui déléguer le chargement.
    ⑦ UNITÉ — Prix en euros, volume en titres, dates au format AAAA-MM-JJ.
    ⑧ POURQUOI — **Deux pièges guettent quiconque charge les cours : ils vivent
      dans plusieurs fichiers qu il faut fusionner, et une même valeur y porte
      deux orthographes qu il faut rapprocher.** `programmes/JUGE_DES_STRATEGIES.py` les
      résout depuis toujours. **Les redécouvrir ici aurait créé une seconde
      version de la même règle, et deux versions divergent toujours (R-708).**
    ⑨ CE QUI CLOCHE — **Elle hérite du repli de `_fichiers_de_cours` : juge des stratégies
      absent, elle travaillerait sur deux fichiers écrits en dur, dont le fichier
      maître ne fait pas partie.**
    ⑩ EFFET — Aucun en propre ; le chargement du juge des stratégies exécute son code.
    ⑪ TERMINAISON — Rend la main. **Peut lever** si le juge des stratégies échoue à se charger
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    # LE JUGE DES STRATÉGIES SE CHERCHE DANS L ARBORESCENCE, pas seulement a plat. TROISIEME
    # occurrence du meme defaut dans ce seul fichier, le 12-09-2026 — apres
    # `trouver_module` et `_fichiers_de_cours`. Au depot, les programmes vivent
    # dans `programmes/`, et chercher a la racine ne trouve rien.
    m = _banc(base)
    if m and hasattr(m, "charger_cours"):
        return m.charger_cours(*chemins)
    raise FileNotFoundError(
        "le juge des stratégies est introuvable : on ne reecrit PAS son chargeur de cours.")


def trouver_module(base):
    """Cherche le module sous ses deux graphies, A PLAT PUIS DANS L ARBORESCENCE.

    Corrige le 12-09-2026. Au depot, les programmes vivent dans `programmes/` ;
    cette fonction ne regardait qu a la racine. Lance par le workflow, elle levait
    « aucune des deux graphies n existe » — et le pas etait marque
    `continue-on-error` — son echec n arretait pas les pas suivants —, donc
    LE CIRCUIT DU SOIR CONTINUAIT SANS TENIR LES POSITIONS.
    **Zero signal depuis la bascule : un programme qui n a rien a faire et un
    programme casse rendent le meme silence.** Meme famille que `chemin_de` du
    radar et que `_p` de la mesure, corrigees le meme jour.

    ① RÔLE — Trouver `programmes/MODULE_POSITIONS.py`, le moteur de calcul des positions,
      où qu il soit rangé et quelle que soit la graphie de son nom.
    ② CONTEXTE D APPEL — `main` et `tenir_pour_de_vrai`, avant tout chargement.
    ③ ENTRÉE — `base` : la racine à fouiller.
    ④ CONDITIONS D ENTRÉE — Aucune. **Un module absent est traité, par une
      levée.**
    ⑤ SORTIE — UNE valeur : le chemin réel du module.
      [rend: 1]
    ⑥ TRAITEMENT — ① essayer les deux graphies À PLAT · ② **sinon descendre
      l arborescence**, en écartant archives, git, cache et dossier de travail ·
      ③ lever si rien n est trouvé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Au dépôt, les programmes vivent dans `programmes/` ; cette
      fonction ne regardait qu à la racine.** Lancée par le circuit du soir, elle
      levait « aucune des deux graphies n existe ». **Et le pas était marqué
      tolérant à l échec — son échec n arrêtait pas les pas suivants —, donc le
      circuit du soir continuait SANS TENIR LES POSITIONS,
      du 12-09-2026 jusqu à la correction. Un programme qui n a rien à faire et un programme cassé rendaient
      le même silence.**
    ⑨ CE QUI CLOCHE — **La première trouvée gagne, et l ordre de descente n est
      pas garanti** — même défaut que `_banc`. Deux modules vivants donneraient
      un choix dépendant du système de fichiers.
    ⑩ EFFET — Aucun : elle ne fait que chercher.

    ⑪ TERMINAISON — **LÈVE** si aucune graphie n existe. Rend la main sinon.
      [sort: non]
    ⑫ DÉFINITIONS —
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for nom in ("MODULE POSITIONS.py", "MODULE_POSITIONS.py"):
        p = os.path.join(base, nom)
        if os.path.exists(p):
            return p
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail")]
        for nom in ("MODULE POSITIONS.py", "MODULE_POSITIONS.py"):
            if nom in fs:
                return os.path.join(r, nom)
    raise FileNotFoundError(
        "aucune des deux graphies du module des positions n'existe sous " + base)


def calendrier(cours):
    """Rend toutes les séances de bourse connues, triées, toutes valeurs confondues.

    ① RÔLE — **Le calendrier de la bourse**, tiré des cours. C est l unique
      endroit où il se calcule : `tenir_pour_de_vrai` et `entrer` l appellent
      tous les deux (deux implémentations d une même chose divergent toujours,
      R-708).
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, pour la séance qui suit celle du
      jour ; `entrer`, pour la date d entrée d une position qui n en a pas.
    ③ ENTRÉE — `cours` : un dictionnaire valeur → liste de séances, chaque
      séance étant un dictionnaire qui porte au moins la clé `date`.
    ④ CONDITIONS D ENTRÉE — Les dates sont au format année-mois-jour
      (AAAA-MM-JJ) : c est ce qui rend l ordre du texte égal à l ordre du temps.
    ⑤ SORTIE — UNE valeur : la liste triée des dates, sans doublon.
      [rend: 1]
    ⑥ TRAITEMENT — ① réunir les dates de toutes les valeurs · ② trier.
    ⑦ UNITÉ — Des JOURS de bourse, au format AAAA-MM-JJ.
    ⑧ POURQUOI — **La séance suivante est une date de la BOURSE, pas une date
      propre à une valeur.** Si l on prenait les seules séances d une valeur,
      une valeur privée d une séance par un trou de données serait achetée un
      jour plus tard, à un autre prix, sans un mot.
    ⑨ CE QUI CLOCHE — Une date fausse portée par une seule valeur entre dans le
      calendrier de toutes. Mesuré le 27-09-2026 sur `donnees/cours_maitre.csv`
      (Cowork, puis le Chat) : chaque séance y est portée par 39 ou 40 valeurs —
      ArcelorMittal n'a de séances que du 31-07 au 10-09-2026 ; aucune séance
      n est portée par une poignée de valeurs. (Première rédaction du même
      jour : « aucune date n y est portée par une partie seulement des
      valeurs » — inexacte au mot près, relevé par Cowork.)
    ⑩ EFFET — Aucun : rien n est modifié ni écrit.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas
      revenir.
      [sort: non]
    """
    return sorted({b["date"] for serie in cours.values() for b in serie})


def seance_suivante(dates_triees, date):
    """Rend la première séance du calendrier postérieure à une date, ou None.

    ① RÔLE — **Dire quelle séance suit une date** : c est la séance d achat
      d un signal, puisque l achat se fait à l ouverture du lendemain (R-601).
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai` (la séance qui suit celle du
      jour) et `entrer` (la date d entrée d une position qui n en a pas).
    ③ ENTRÉE — `dates_triees` : le calendrier rendu par `calendrier` ·
      `date` : une date AAAA-MM-JJ.
    ④ CONDITIONS D ENTRÉE — Les deux au format AAAA-MM-JJ : la comparaison se
      fait sur le texte. `entrer` vérifie le format avant d appeler.
    ⑤ SORTIE — UNE valeur : la date suivante, ou None si le calendrier n en a
      pas encore — le cas normal le soir même d une séance.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir le calendrier et rendre la première date plus
      grande que celle reçue.
    ⑦ UNITÉ — Des JOURS de bourse, au format AAAA-MM-JJ.
    ⑧ POURQUOI — Une seule définition de « la séance suivante » pour tout le
      programme ; jusqu au 27-09-2026 il y en avait une, et `entrer` n en avait
      aucune, d où le défaut de l achat qui ne se faisait jamais.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas
      revenir.
      [sort: non]
    """
    return next((x for x in dates_triees if x > date), None)


def _est_date(x):
    """Dit si un texte est une date au format AAAA-MM-JJ.

    ① RÔLE — **Refuser une date mal écrite avant de la comparer** : les dates se
      comparent comme du texte, et « 04/09/2026 » passerait pour antérieure à
      2024.
    ② CONTEXTE D APPEL — `entrer`, sur la date du signal et la date d entrée.
    ③ ENTRÉE — `x` : un texte.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : vrai si le texte a la forme AAAA-MM-JJ, en chiffres.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier la longueur, les deux tirets et les chiffres ·
      ② vérifier que la date existe au calendrier civil (pas de mois 13, pas
      de 30 février).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Trouvé le 27-09-2026 par le relecteur du Chat : une date du
      signal écrite « 04/09/2026 » — ce qu un tableur réécrit en français —
      faisait acheter au 02-01-2024, la première séance du fichier, sans un mot.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if not (len(x) == 10 and x[4] == "-" and x[7] == "-"
            and (x[:4] + x[5:7] + x[8:]).isdigit()):
        return False
    try:
        datetime.date.fromisoformat(x)
    except ValueError:
        return False  # « 2026-13-45 » a la forme, mais n'existe pas
    return True


def horizon_connu(p, reglages):
    """Rend l horizon de la stratégie d une position tel que les réglages le donnent, ou None.

    ① RÔLE — **Lire l horizon de SA stratégie**, sans repli. C est le seul
      endroit où cet horizon se lit dans les réglages (R-708) : `horizon_de`
      l appelle, et `completer_echeances` s en sert pour dire quand il manque.
    ② CONTEXTE D APPEL — `horizon_de` et `completer_echeances`.
    ③ ENTRÉE — `p` : la position · `reglages` : les réglages par stratégie, ou
      None.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un nombre entier de séances, strictement positif,
      ou None s il manque ou vaut 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher la stratégie, sans ses espaces · ② rendre son
      horizon s il est un entier positif, None sinon.
    ⑦ UNITÉ — Des SÉANCES de bourse.
    ⑧ POURQUOI — **Un horizon à 0 mettrait l échéance sur la séance d achat
      elle-même** : c est exactement la forme du défaut 2 (27-09-2026). Relevé
      par le relecteur du Chat le même jour.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if not reglages:
        return None
    h = (reglages.get((p.get("strategie") or "").strip()) or {}).get("horizon")
    return h if isinstance(h, int) and h > 0 else None


def horizon_de(p, reglages, horizon_seances):
    """Rend l horizon, en séances de bourse, de la stratégie d une position.

    ① RÔLE — **Dire combien de séances une position peut durer**, selon SA
      stratégie, avec un repli. La lecture elle-même est faite par
      `horizon_connu` ; `entrer` et `completer_echeances` appellent celle-ci
      (R-708).
    ② CONTEXTE D APPEL — `entrer` et `completer_echeances`.
    ③ ENTRÉE — `p` : la position · `reglages` : les réglages par stratégie, lus
      dans `donnees/cac40_strategies.csv`, ou None · `horizon_seances` : la
      valeur de repli.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un nombre entier de séances.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire l horizon par `horizon_connu` · ② rendre la valeur
      de repli s il manque ou vaut 0.
    ⑦ UNITÉ — Des SÉANCES de bourse.
    ⑧ POURQUOI — L horizon de SA propre stratégie, jamais celui du voisin. Le
      même calcul vivait dans `entrer` ; il est sorti pour servir aussi la
      complétion de l échéance, le 27-09-2026.
    ⑨ CE QUI CLOCHE — **Une stratégie absente des réglages, ou un horizon à 0,
      prend la valeur de repli.** Cette fonction ne le dit pas elle-même ;
      `completer_echeances` le dit par un incident depuis le 27-09-2026, et
      `tenir_pour_de_vrai` refuse un horizon nul au registre.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return horizon_connu(p, reglages) or horizon_seances


def echeance(serie, date_entree, h):
    """Rend la date de la séance qui tombe h séances après la séance d achat, ou None.

    ① RÔLE — **Dire quand une position arrive à son échéance** : à la clôture de
      la h-ième séance APRÈS la séance d achat.
    ② CONTEXTE D APPEL — `entrer`, le soir de l achat, et `completer_echeances`,
      les soirs suivants.
    ③ ENTRÉE — `serie` : les séances de la valeur · `date_entree` : la date de la
      séance d achat · `h` : l horizon en séances.
    ④ CONDITIONS D ENTRÉE — Les dates au format AAAA-MM-JJ. Une date présente
      deux fois dans la série est comptée une fois.
    ⑤ SORTIE — UNE valeur : la date de l échéance, ou None si la séance d achat
      n est pas dans la série, ou si la h-ième séance après elle n est pas encore
      publiée.
      [rend: 1]
    ⑥ TRAITEMENT — ① trier la série · ② trouver la séance d achat · ③ rendre la
      séance située h rangs plus loin, si elle existe.
    ⑦ UNITÉ — Des SÉANCES de bourse, jamais des jours du calendrier.
    ⑧ POURQUOI — **Défaut trouvé le 27-09-2026 (défaut 2 de A-491).**
      L échéance était calculée le soir de l achat, sur les seules séances
      connues ce soir-là, et bornée à la dernière : elle tombait sur la séance
      d achat elle-même, et la position était vendue dès le lendemain. Même
      sans cette borne, elle visait la 19ᵉ séance après l achat au lieu de la
      20ᵉ. Mesuré le même jour sur le tableau des 100 trades de référence : les
      4 sorties à l échéance tombent toutes 20 séances après la séance d achat.
      Une échéance qu on ne connaît pas encore n est pas une date : on ne la
      devine pas, on attend qu elle existe.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    dates = sorted({b["date"] for b in serie})
    if date_entree not in dates:
        return None
    i = dates.index(date_entree)
    return dates[i + h] if i + h < len(dates) else None


def completer_echeances(positions, cours, reglages, horizon_seances=20, cle=None):
    """Recalcule, chaque soir, l échéance de chaque position ouverte, depuis sa séance d achat.

    ① RÔLE — **Donner à chaque position ouverte son échéance exacte** — la
      séance h rangs après la séance d achat — dès que cette séance est publiée,
      et la laisser inconnue d ici là.
    ② CONTEXTE D APPEL — `tenir`, juste AVANT `cloturer`, pour que la clôture du
      soir lise une échéance juste ; et, depuis le 28-09-2026, une seconde fois
      après `entrer`, position par position, sur celles qui viennent d entrer.
    ③ ENTRÉE — `positions` · `cours` · `reglages` : les réglages par stratégie ·
      `horizon_seances` : la valeur de repli · `cle` : la fonction qui rapproche
      les graphies.
    ④ CONDITIONS D ENTRÉE — Aucune. Une position dont la séance d achat est
      illisible ou absente des cours garde l échéance déjà écrite si c est une
      date, et un incident le dit. Une position aux prix illisibles reçoit
      quand même son échéance ; c est `cloturer` qui signale ses prix.
    ⑤ SORTIE — DEUX valeurs : les positions, et les incidents.
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque position ouverte : ① dire si l horizon de sa
      stratégie est inconnu · ② si la séance d achat est illisible ou absente,
      le dire et garder l échéance écrite si elle est valide · ③ sinon calculer
      l échéance par `echeance`, inconnue si elle n est pas encore publiée ·
      ④ si l échéance écrite diffère, la remplacer et le dire · ⑤ si elle est
      déjà passée, le dire.
    ⑦ UNITÉ — Des SÉANCES de bourse.
    ⑧ POURQUOI — **L échéance écrite dans la ligne n est pas crue** : c est le
      même principe que pour la date d achat (défaut 1, 27-09-2026). Une ligne
      écrite par une version fautive du programme porterait une échéance fausse,
      et la position serait vendue au mauvais moment. Ce qui se calcule ne
      s écrit jamais à la main (R-728) ; ce qu un programme peut faire, un
      programme le fait (R-754). Les cas qui ne sont pas normaux se disent
      par un incident : horizon inconnu de la stratégie, séance d achat
      illisible ou absente, échéance écrite remplacée, échéance déjà passée
      après des soirs manqués.
    ⑨ CE QUI CLOCHE — **L échéance reste « EN_ATTENTE » dans le fichier des
      positions pendant les 20 premières séances**, et c est ce que le cockpit
      affiche. C est exact, mais moins lisible qu une date.
    ⑩ EFFET — **MODIFIE l échéance des positions reçues.**
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    incidents = []
    for p in positions:
        if (p.get("statut") or "").strip() != OUVERTE:
            continue
        v = (p.get("valeur") or "").strip()
        s = cours.get(cle(v)) if cle else cours.get(v)
        if not s:
            continue  # `cloturer` le dira
        d = (p.get("date_entree") or "").strip()
        ancienne = (p.get("horizon_fin") or "").strip()
        if horizon_connu(p, reglages) is None:
            incidents.append("position %s : horizon inconnu pour la strategie %r "
                             ": repli a %d seances"
                             % (v, (p.get("strategie") or "").strip(), horizon_seances))
        h = horizon_de(p, reglages, horizon_seances)
        dates = sorted({b["date"] for b in s})
        # SEANCE D'ACHAT ILLISIBLE OU ABSENTE : on ne peut rien calculer. Une
        # echeance deja ecrite et valide est GARDEE — l'effacer priverait la
        # position de toute sortie a l'echeance, pour toujours.
        if not _est_date(d) or d not in dates:
            incidents.append("position %s : seance d'achat %r %s : echeance non "
                             "recalculee" % (v, d, "absente des cours"
                                             if _est_date(d) else "illisible"))
            if not _est_date(ancienne):
                p["horizon_fin"] = INCONNU
            continue
        fin = echeance(s, d, h)
        nouvelle = fin or INCONNU
        if ancienne != nouvelle and ancienne not in ("", INCONNU):
            incidents.append("position %s : echeance ecrite %r remplacee par %s "
                             "(%d seances apres l'achat du %s)"
                             % (v, ancienne, nouvelle, h, d))
        # UNE ECHEANCE DEJA PASSEE SE DIT : apres des soirs manques, la
        # position sera vendue a une date anterieure a la derniere seance.
        # Un soir normal, l'echeance devient connue le soir meme : elle vaut
        # la derniere seance, la position est vendue ce soir-la, et rien n'est
        # dit. L'incident ne s'ecrit donc qu'une fois : le soir du rattrapage.
        if fin and fin < dates[-1]:
            incidents.append("position %s : echeance %s deja passee (derniere "
                             "seance %s) : vente retroactive a la cloture du %s, "
                             "sauf si l objectif ou la vente forcee a ete touche avant"
                             % (v, fin, dates[-1], fin))
        p["horizon_fin"] = nouvelle
    return positions, incidents


# ─────────────────────────────────────────────────────────────────────
# B) LES CLÔTURES
# ─────────────────────────────────────────────────────────────────────
def cloturer(positions, cours, mod, horizon_seances=20, cle=None):
    """Clôture toute position OUVERTE dont le stop, l'objectif ou l'échéance
    est atteint. Rend (lignes de journal, positions restantes, incidents).

    DEUX PRIX SONT ÉCRITS, ET C'EST VOULU — deux prix sont écrits, le réel et celui de convention (R-602). Le prix RÉEL tient compte
    des sauts d'ouverture ; le prix de CONVENTION suppose une exécution au
    seuil exact. Hors saut, les deux sont identiques. C'est ce qui permet de
    comparer une opération vécue à un backtest, sans confondre les deux.

    ① RÔLE — **Fermer ce qui doit l être, et écrire le trade au journal.** C est
      l endroit où une perte ou un gain devient définitif.
    ② CONTEXTE D APPEL — `tenir`, en PREMIER, avant toute ouverture. **Une
      clôture du matin libère le jeton pour un signal du soir.** Et, depuis le
      28-09-2026, une seconde fois après `entrer`, sur les positions qui viennent
      d entrer : leur séance d achat compte (R-608).
    ③ ENTRÉE — `positions` : toutes les positions, ouvertes et en attente ·
      `cours` : les séries de cours par valeur · `mod` : le moteur
      `programmes/MODULE_POSITIONS.py` · `horizon_seances` : **n est plus lu
      depuis le 27-09-2026** — l échéance vient de la position, calculée par
      `completer_echeances` ; le paramètre reste pour ne pas changer les
      appels · `cle` : la fonction qui rapproche les deux graphies d un même nom.
    ④ CONDITIONS D ENTRÉE — Les cours doivent porter les séances suivant
      l entrée. **Une valeur introuvable est un incident, pas une erreur.**
    ⑤ SORTIE — TROIS valeurs : les lignes de journal, les positions restantes,
      les incidents.
      [rend: 3]
    ⑥ TRAITEMENT — ① pour chaque position ouverte, retrouver sa série ·
      ② parcourir les séances DEPUIS LA SÉANCE D ACHAT COMPRISE (R-608) · ③ **s arrêter à la première qui
      touche le stop, l objectif ou l échéance** — l échéance seulement si elle
      est une date ; inconnue, elle n est pas encore publiée · ④ écrire les
      DEUX prix.
    ⑦ UNITÉ — **Les seuils sont en POURCENTS, les prix en euros, l horizon en
      JOURS DE BOURSE.** Le gain net est en euros, frais compris.
    ⑧ POURQUOI — **Deux prix sont écrits pour chaque sortie, et c est voulu.** Le
      prix RÉEL tient compte des sauts d ouverture, le prix de CONVENTION suppose
      une exécution au seuil exact. **C est ce qui permet de comparer une
      opération vécue à un backtest sans confondre les deux.**
    ⑨ CE QUI CLOCHE — — *(Réparé le 28-09-2026, défaut 4 de A-491 : la séance
      d achat n était pas parcourue. Avant le 27-09-2026, ce point disait :
      « `horizon_seances` vaut 20 par défaut » — ce paramètre n est plus lu.)*
    ⑩ EFFET — **RETIRE de la liste de positions reçue** celles qu elle clôture.
    ⑪ TERMINAISON — Rend toujours la main. **Aucun de ses appels ne termine.**
      [sort: non]
    """
    trades, restantes, incidents = [], [], []

    for p in positions:
        if (p.get("statut") or "").strip() != OUVERTE:
            restantes.append(p)
            continue

        v = (p.get("valeur") or "").strip()
        s = cours.get(cle(v)) if cle else cours.get(v)
        if not s:
            incidents.append("cours absents pour %s : position laissee ouverte" % v)
            restantes.append(p)
            continue

        try:
            pe = float(p["prix_entree"])
            tp = float(p["tp"])
            sl = float(p["sl"])
        except (ValueError, KeyError, TypeError):
            incidents.append("position illisible sur %s : %r" % (v, p.get("prix_entree")))
            restantes.append(p)
            continue

        # les séances depuis l'entrée, dans l'ordre — on ne saute rien
        # LES SEUILS VIENNENT DE LA POSITION, JAMAIS DU MODULE.
        # `sortie_position` et `parametres_entree` RECALCULENT les seuils a
        # partir de deux constantes fixes du module — TP_PCT 4,0 % et SL_PCT
        # 2,5 %. Or le registre porte des seuils PAR STRATEGIE : MA200-S1, en
        # PRODUCTION, est a +5,0 % / -2,0 %. Une position de cette strategie
        # serait donc cloturee aux seuils d'une AUTRE, en silence.
        # Mesure du 02-09-2026 : ces deux fonctions ne sont appelees par aucun
        # autre programme du projet. Le juge des stratégies, lui, lit les seuils de la fiche
        # et n'emprunte au module que `tester_seance` et `frais_ordre`, qui ne
        # dependent d'aucun reglage. On fait pareil : c'est la seule facon de
        # servir plusieurs strategies sans toucher au module, donc sans
        # toucher au juge des stratégies ni au radar qui l'utilisent.
        d_ent = (p.get("date_entree") or "")
        # LA SEANCE D'ACHAT COMPTE (R-608, decision de Jean-Luc du 27-09-2026 a
        # 19h40 ; defaut 4 de A-491) : les seuils se testent DES la seance ou la
        # position est achetee a l'ouverture, pas a partir du lendemain. Avant,
        # `> d_ent` sautait cette seance : Vinci, achete le 07-06-2024 a 113,60,
        # plus bas du jour 110,75 sous la vente forcee 110,76, n'etait pas vendu.
        # Le juge des stratégies fait de meme depuis le meme jour (R-708). L'echeance, elle,
        # tombe toujours h seances APRES l'achat (`completer_echeances`).
        apres = sorted((b for b in s if b["date"] >= d_ent),
                       key=lambda b: b["date"])
        if not apres:
            restantes.append(p)
            continue

        px = motif = None
        for k, bar in enumerate(apres):
            r = mod.tester_seance(bar, tp, sl)
            if r:
                px, motif = r[0], r[1]
                d_sortie = bar["date"]
                break
            # L ECHEANCE EST PORTEE PAR LA POSITION, pas par un compte global :
            # `cloturer` lit la date dans la ligne qu il traite. Depuis le
            # 27-09-2026, cette date est recalculee chaque soir par
            # `completer_echeances`, avec l horizon de SA strategie.
            # DEPUIS LE 27-09-2026 (defaut 2), L'ECHEANCE N'A PLUS DE REPLI :
            # `completer_echeances` la calcule juste avant. Inconnue, elle veut
            # dire que sa seance n'est pas encore publiee — ou que la seance
            # d'achat est absente ou illisible, ce que `completer_echeances` dit
            # par un incident. Dans les deux cas, pas de vente a l'echeance.
            _fin = (p.get("horizon_fin") or "").strip()
            if _est_date(_fin) and bar["date"] >= _fin:
                px, motif = bar["close"], "HORIZON"
                d_sortie = bar["date"]
                break

        if px is None:
            restantes.append(p)
            continue

        # LE PRIX DE CONVENTION : le seuil theorique, jamais le prix vecu.
        # Hors saut d'ouverture les deux sont identiques ; sur un saut ils
        # different, et c'est ce qui permet de comparer une operation vecue a
        # un backtest sans confondre les deux — deux prix sont écrits, le réel et celui de convention (R-602).
        prix_conv = sl if motif.startswith("SL") else (
            tp if motif.startswith("TP") else px)

        # LES FRAIS VIENNENT DU MODULE. On ne recopie jamais un taux.
        # LE CAPITAL VIENT DU MODULE. Il y porte le nom `CAPITAL`. L'ecrire
        # ici serait une seconde source pour la meme valeur : identiques
        # aujourd'hui, divergentes le jour ou l'une des deux change — et
        # personne ne verrait laquelle a raison.
        q = getattr(mod, "CAPITAL", 100000.0) / pe
        f_tot = mod.frais_ordre(q, pe) + mod.frais_ordre(q, px)
        f_conv = mod.frais_ordre(q, pe) + mod.frais_ordre(q, prix_conv)

        trades.append({
            "strategie": p.get("strategie", ""),
            "valeur": v,
            "date_entree": d_ent,
            "prix_entree": "%.5f" % pe,
            "date_sortie": d_sortie,
            "prix_sortie": "%.5f" % px,
            "motif_sortie": motif,
            "pnl_net_eur": "%.2f" % (q * (px - pe) - f_tot),
            "prix_sortie_convention": "%.5f" % prix_conv,
            "pnl_net_convention_eur": "%.2f" % (q * (prix_conv - pe) - f_conv),
            "comptabilite": p.get("comptabilite", ""),
            "regles_pre_trade": p.get("regles_pre_trade", ""),
            "explication": p.get("explication", ""),
        })

    return trades, restantes, incidents


# ─────────────────────────────────────────────────────────────────────
# C) LES ENTRÉES
# ─────────────────────────────────────────────────────────────────────
def entrer(positions, cours, mod, horizon_seances=20, cle=None,
           reglages=None):
    """Passe en OUVERTE toute position EN_ATTENTE_ENTREE dont la séance
    d'entrée est disponible. Le prix d'entrée est l'OUVERTURE de cette séance.

    JAMAIS LE CLOSE. GOOGLEFINANCE publie la séance entre 20h30 et 06h30 :
    un signal n'est donc jamais connu avant la clôture, et une entrée au cours
    du soir est structurellement impossible. La décomposition du 23/08 sur
    100 trades a montré que cela ne fait rien perdre : rendement de nuit
    −0,070 %, indistinguable du hasard.

    ① RÔLE — **Faire passer une position de l attente à l ouverture**, au prix
      d ouverture de la séance d entrée.
    ② CONTEXTE D APPEL — `tenir`, juste après `cloturer` et avant
      `ouvrir_sur_signaux` ; et `_calibrage`, sur des positions fabriquées.
      (Jusqu au 27-09-2026, cette fiche disait « `cloturer` » : c était faux,
      `cloturer` ne l appelle pas.)
    ③ ENTRÉE — `positions` · `cours` · `mod` : le moteur
      `programmes/MODULE_POSITIONS.py` · `horizon_seances` : le nombre de séances
      avant échéance · `cle` : la fonction qui rapproche les graphies ·
      `reglages` : les seuils par stratégie, lus dans
      `donnees/cac40_strategies.csv`.
    ④ CONDITIONS D ENTRÉE — **Chaque position doit porter une date de signal
      AAAA-MM-JJ qui est une séance des cours.** Sinon elle reste en attente,
      et un incident le dit. **La date d entrée écrite dans la ligne n est pas
      crue** : elle est vide le soir du signal, et elle se déduit ici du
      signal, chaque soir tant que la position attend.
    ⑤ SORTIE — DEUX valeurs : les positions mises à jour, et les incidents.
      [rend: 2]
    ⑥ TRAITEMENT — ① une date du signal illisible, postérieure aux cours ou
      absente du calendrier est dite par un incident, et la position attend ·
      ② **la date d entrée est la première séance de la bourse postérieure au
      signal** (`seance_suivante`) ; tant qu elle n est pas publiée, on
      attend sans rien dire · ③ une date d entrée écrite différente est
      remplacée, et un incident le dit · ④ retrouver la séance d entrée ;
      si elle manque alors que des séances plus récentes existent, le dire
      par un incident · ⑤ **prendre son OUVERTURE, jamais sa clôture** ·
      ⑥ calculer les seuils depuis ce prix · ⑦ fixer l échéance par `echeance`
      — inconnue le soir de l achat, puisque sa séance n est pas publiée.
    ⑦ UNITÉ — **Prix en euros, seuils en pourcents.**
    ⑧ POURQUOI — **Un signal se calcule sur la clôture d une séance : il n est donc
      jamais connu avant 17 h 35, et une entrée au cours du même soir serait
      impossible à passer.** L entrée se fait à l ouverture du lendemain.
      Et la mesure sur 100 trades a montré que cela ne fait rien perdre :
      **rendement de nuit −0,070 %, indistinguable du hasard.**
    ⑨ CE QUI CLOCHE — **Une position dont la séance d entrée ne vient jamais
      reste en attente indéfiniment**, et rien ne compte depuis combien de temps.
      Une valeur retirée de l univers laisserait une ligne éternelle. Depuis le
      27-09-2026, chaque soir où une position ne peut pas s ouvrir est dit par
      un incident, sauf le soir même du signal et le cas d une séance
      d entrée pas encore publiée ; **mais un incident ne fait pas rougir le
      circuit.** **Une séance d entrée qui ne viendra jamais pour sa valeur
      (cotation suspendue ce jour-là, par exemple) bloque la position pour
      toujours, et en un jeton elle garde le jeton de sa stratégie : plus aucun
      signal n est pris.** Une date d entrée corrigée à la main est remplacée
      chaque soir : il n existe aucune issue sans une règle de Jean-Luc
      (question posée le 27-09-2026). Mesuré le même jour par le relecteur du
      Chat : aucune valeur des cours réels n a de trou entre sa première et sa
      dernière séance.
      Jusqu au 27-09-2026, l échéance était calculée ici, le soir de l achat,
      sur les seules séances connues : elle tombait sur la séance d achat
      elle-même, et la position était vendue dès le lendemain (défaut 2 de
      A-491, réparé par `echeance` et `completer_echeances`).
    ⑩ EFFET — **MODIFIE les positions reçues** : leur date d entrée (déduite
      du signal), leur état, leur prix d entrée, leurs seuils.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    incidents = []
    # LE CALENDRIER DE LA BOURSE : toutes les seances connues, toutes valeurs
    # confondues, calcule par la meme fonction que dans `tenir_pour_de_vrai`.
    toutes = calendrier(cours)
    for p in positions:
        if (p.get("statut") or "").strip() != EN_ATTENTE:
            continue
        v = (p.get("valeur") or "").strip()
        d = (p.get("date_entree") or "").strip()
        s = cours.get(cle(v)) if cle else cours.get(v)
        if not s:
            incidents.append("cours absents pour %s : entree differee" % v)
            continue

        # LA DATE D'ENTREE SE DEDUIT DU SIGNAL, CHAQUE SOIR, TANT QUE LA
        # POSITION ATTEND : c'est la premiere seance de la bourse apres le
        # signal (entree a l'ouverture du lendemain, R-601). Celle qui est
        # ecrite dans la ligne n'est qu'un rappel ; si elle differe, elle est
        # remplacee, et on le dit.
        # Defaut trouve le 27-09-2026 (Chat, en rejouant un signal sur une
        # copie) : le circuit tourne a 20 h, le signal porte sur la seance du
        # jour, et la seance suivante n'existe pas encore. `ouvrir_sur_signaux`
        # ecrivait donc une date d'entree vide ; les soirs suivants, on
        # cherchait la seance portant une date vide, on ne la trouvait jamais,
        # et la position restait « en attente d'entree » POUR TOUJOURS, sans un
        # mot. Aucun signal reel n'aurait jamais ete achete.
        # Les relectures du meme jour ont montre qu'une date d'entree deja
        # ecrite ne doit pas etre crue : une date fausse achetait au prix de
        # janvier 2024, ou un jour trop tard, ou bloquait pour toujours une
        # position dont la date avait ete fixee avant un rattrapage de cours.
        # UNE ATTENTE NE SE TAIT QUE SI ELLE EST NORMALE — le soir meme du
        # signal, ou une seance d'entree pas encore publiee. Tout autre cas ou
        # la position ne peut pas s'ouvrir est dit par un incident.
        d_sig = (p.get("date_signal") or "").strip()
        if not _est_date(d_sig):
            incidents.append(
                "position %s : date de signal %r illisible (attendu "
                "AAAA-MM-JJ) : entree bloquee" % (v, d_sig))
            continue
        if toutes and d_sig > toutes[-1]:
            incidents.append(
                "position %s : signal du %s posterieur a la derniere seance "
                "des cours (%s) : cours en retard, entree differee"
                % (v, d_sig, toutes[-1]))
            continue
        if d_sig not in toutes:
            incidents.append(
                "position %s : signal du %s, qui n'est pas une seance des "
                "cours : entree bloquee" % (v, d_sig))
            continue
        attendu = seance_suivante(toutes, d_sig)
        if attendu is None:
            continue  # soir du signal : la seance suivante n'est pas publiee
        if d and d != attendu:
            incidents.append(
                "position %s : date d'entree ecrite %r remplacee par %s, la "
                "seance qui suit le signal du %s" % (v, d, attendu, d_sig))
        d = attendu
        p["date_entree"] = d

        bar = next((b for b in s if b["date"] == d), None)
        if bar is None:
            # Si la bourse a deja publie des seances apres la date d'entree,
            # celle-ci n'est plus « a venir » : elle manque pour cette valeur,
            # et la position attendrait indefiniment. On le dit.
            if any(x > d for x in toutes):
                incidents.append(
                    "seance d'entree %s absente des cours de %s alors que des "
                    "seances plus recentes existent : entree bloquee ; en un "
                    "jeton, la strategie %s ne prendra aucun autre signal tant "
                    "que cette ligne attend — aucune issue sans une regle de "
                    "Jean-Luc (abandonner la position, ou entrer a une autre "
                    "seance que celle qui suit le signal)"
                    % (d, v, (p.get("strategie") or "").strip()))
            # sinon la seance d'entree n'est pas encore publiee : on attend
            continue

        pe = bar["open"]
        # LES SEUILS VIENNENT DE LA STRATEGIE, A L'ENTREE COMME A LA SORTIE.
        # Premiere version : `entrer()` appelait `parametres_entree` du module,
        # qui recalcule depuis deux constantes fixes — +4,0 / -2,5. Une
        # position MA200-S1, qui est a +5,0 / -2,0, s'ouvrait donc avec les
        # seuils d'une AUTRE strategie. Et comme `cloturer` lit fidelement les
        # seuils de la ligne, il appliquait fidelement les mauvais : l'erreur
        # etait ecrite a l'ouverture puis executee sans broncher.
        # C'est le meme defaut que celui corrige le 02/09 a la sortie ; il
        # avait seulement change d'extremite. Les DEUX bouts du meme trade
        # doivent suivre la MEME regle.
        strat = (p.get("strategie") or "").strip()
        r_ = reglages.get(strat) if reglages else None
        if not r_:
            incidents.append(
                "seuils inconnus pour la strategie %r : entree differee. "
                "Le programme n'INVENTE pas de seuils — il attend qu'on les "
                "lui donne." % strat)
            continue
        tp = pe * (1.0 + r_["tp"])
        sl = pe * (1.0 - r_["sl"])

        # l'échéance se compte en SÉANCES DE BOURSE, jamais en jours calendaires,
        # sur une serie TRIEE : c'est `echeance` qui trie et qui compte.
        # L HORIZON DE SA PROPRE STRATEGIE, jamais celui du voisin.
        # L ECHEANCE : h seances APRES la seance d achat, et seulement si elle
        # existe deja — le soir de l achat, elle n existe jamais (defaut 2,
        # 27-09-2026 : elle tombait sur la seance d achat elle-meme).
        fin = echeance(s, bar["date"], horizon_de(p, reglages, horizon_seances)) or INCONNU

        p["prix_entree"] = "%.5f" % pe
        p["tp"] = "%.5f" % tp
        p["sl"] = "%.5f" % sl
        p["horizon_fin"] = fin
        p["statut"] = OUVERTE
    return positions, incidents


# ─────────────────────────────────────────────────────────────────────
# D) LES NOUVEAUX SIGNAUX
# ─────────────────────────────────────────────────────────────────────
def ouvrir_sur_signaux(positions, signaux, prochaine_seance):
    """Crée une ligne EN_ATTENTE_ENTREE par signal et par comptabilité.

    LA RÈGLE DU JETON UNIQUE : en `un_jeton`, un signal reçu pendant qu'une
    position est déjà en cours POUR CETTE STRATÉGIE est ignoré — mais il est
    MENTIONNÉ au rapport. Ignorer en silence reviendrait à perdre l'information
    qui permettrait de rejouer plus tard une autre
    façon de choisir les signaux à suivre.
    En `jetons_illimites`, on ouvre toujours : les chevauchements sont normaux,
    cette comptabilité ne correspond à aucun portefeuille réel et sert à juger
    la qualité du signal.

    ① RÔLE — **Transformer un signal en intention d achat.** C est le seul
      endroit où une position naît.
    ② CONTEXTE D APPEL — `tenir`, APRÈS les clôtures.
    ③ ENTRÉE — `positions` : toutes les positions · `signaux` : les signaux du
      jour, tels que `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` les a écrits ·
      `prochaine_seance` : une date d entrée **PROVISOIRE**, la séance qui
      suit celle du jour si elle est déjà publiée, None sinon — le cas normal
      du soir. **Elle n est qu un rappel : `entrer` la recalcule depuis la
      date du signal chaque soir tant que la position attend.**
      **Elle ne reçoit PAS les réglages : les seuils sont posés plus tard,
      par `entrer`.**
    ④ CONDITIONS D ENTRÉE — **Chaque signal doit porter sa stratégie**, sans quoi
      la règle du jeton unique ne peut pas s appliquer.
    ⑤ SORTIE — DEUX valeurs : les positions augmentées, et la liste des signaux
      ignorés.
      [rend: 2]
    ⑥ TRAITEMENT — ① pour chaque signal, pour chaque comptabilité · ② **en un
      jeton, vérifier qu aucune position n est en cours POUR CETTE STRATÉGIE** ·
      ③ créer la ligne en attente d entrée, avec la date provisoire reçue
      (vide le soir du signal) ; `entrer` fixe la vraie.
    ⑦ UNITÉ — **Les seuils sont en pourcents, l horizon en jours de bourse.**
    ⑧ POURQUOI — **Le système tient DEUX comptabilités séparées. En « un jeton », une seule
      position à la fois par stratégie : un signal reçu pendant qu une position est en cours est ignoré.
      Mais il est MENTIONNÉ au rapport.
      Ignorer en silence reviendrait à perdre l information qui permettrait de rejouer plus tard
      une autre façon de choisir les signaux à suivre.** Et les deux comptabilités ne se mélangent jamais :
      jetons illimités ne correspond à aucun portefeuille réel et sert à juger la
      qualité du signal.
    ⑨ CE QUI CLOCHE — **Un signal portant une stratégie absente des réglages est
      ignoré comme un signal en double.** Les deux cas finissent dans la même
      liste, et rien ne les distingue au rapport.
    ⑩ EFFET — **AJOUTE à la liste de positions reçue.**

    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS —
      un jeton : la comptabilité où une seule position peut être ouverte à la fois
        par stratégie ; un signal reçu pendant une position est ignoré.
      jetons illimités : la seconde comptabilité, où toute position s'ouvre sans
        limite ; elle ne correspond à aucun portefeuille réel.
      l horizon : le nombre de seances au bout duquel une position se ferme si ni l objectif ni le seuil de perte n ont ete touches.
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
"""
    nouvelles, ignores = [], []

    for sg in signaux:
        strat = sg["strategie"]
        val = sg["valeur"]
        d_sig = sg["date_signal"]

        for compta in (UN_JETON, JETONS_ILLIMITES):
            # anti-doublon : strategie + valeur + date_signal + comptabilite
            deja = any(
                (p.get("strategie") == strat and p.get("valeur") == val
                 and p.get("date_signal") == d_sig
                 and p.get("comptabilite") == compta)
                for p in positions + nouvelles)
            if deja:
                continue

            if compta == UN_JETON:
                occupe = any(
                    (p.get("strategie") == strat
                     and p.get("comptabilite") == UN_JETON
                     and (p.get("statut") or "").strip() in (OUVERTE, EN_ATTENTE))
                    for p in positions + nouvelles)
                if occupe:
                    ignores.append(
                        "signal ignore - position deja en cours (%s sur %s)"
                        % (strat, val))
                    continue

            nouvelles.append({
                "strategie": strat,
                "valeur": val,
                "date_signal": d_sig,
                "date_entree": prochaine_seance,
                "prix_entree": INCONNU,
                "tp": INCONNU,
                "sl": INCONNU,
                "horizon_fin": INCONNU,
                "statut": EN_ATTENTE,
                "comptabilite": compta,
                "regles_pre_trade": "",   # vérification manuelle par Jean-Luc
                "explication": sg.get("explication", ""),
            })

    return nouvelles, ignores


# ─────────────────────────────────────────────────────────────────────
# L'ENCHAÎNEMENT — l'ordre compte
# ─────────────────────────────────────────────────────────────────────
def tenir(positions, cours, signaux, prochaine_seance, mod,
          horizon_seances=20, cle=None, reglages=None, base="."):
    """B puis C puis D. Une clôture du matin libère le jeton pour un signal du
    soir ; l'ordre inverse le bloquerait à tort.

    ① RÔLE — **L orchestrateur d une séance** : clôturer d abord, ouvrir ensuite.
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, et le calibrage.
    ③ ENTRÉE — `positions` · `cours` · `signaux` · `prochaine_seance` : une
      date d entrée PROVISOIRE, **None le soir même du signal** ; `entrer` la
      recalcule depuis le signal · `mod` : le moteur `programmes/MODULE_POSITIONS.py` ·
      `horizon_seances` · `cle` : la fonction qui rapproche les graphies ·
      `reglages` : les seuils par stratégie, lus dans
      `donnees/cac40_strategies.csv` · `base` : la racine du dépôt.
    ④ CONDITIONS D ENTRÉE — Les réglages doivent être renseignés. **Sans eux,
      aucune position ne s ouvre** — c est le défaut du 03-09.
    ⑤ SORTIE — **UNE valeur : un dictionnaire de SIX clés.** `trades` : les
      trades clôturés · `positions` : les positions après la séance ·
      `signaux_ignores` : ceux que la règle du jeton unique a écartés ·
      `incidents` : ce qui n a pas pu être traité · `muet` : l affichage retenu ·
      `alerte` : ce qui doit remonter au rapport.
      **Les appelants écrivent `tenir(...)["trades"]` : c est bien un
      dictionnaire, et non un couple.**
      [rend: 1]
    ⑥ TRAITEMENT — ① recalculer l échéance des positions ouvertes
      (`completer_echeances`) · ② clôturer ce qui doit l être · ③ faire entrer
      les positions en attente · ③bis repasser, sur celles qui viennent d entrer,
      le calcul de l échéance puis la clôture — dès leur séance d achat (R-608),
      et jusqu à l échéance pour une entrée faite en retard (depuis le
      28-09-2026) · ④ ouvrir sur les signaux.
    ⑦ UNITÉ — Celles de ce qu elle reçoit : euros, pourcents, jours de bourse.
    ⑧ POURQUOI — **On clôture AVANT d ouvrir, et l ordre compte : une position
      fermée le matin libère le jeton de sa stratégie, ce qui permet d en ouvrir
      une autre le soir même. L ordre inverse la bloquerait à tort.** Et une
      position achetée le jour même et vendue dans sa séance d achat libère son
      jeton le soir même : c est l objet de ③bis (relecteur du Chat, 28-09-2026).
      Sans lui, le signal du jour sur la même stratégie était ignoré, et perdu.
    ⑨ CE QUI CLOCHE — Rien vu. **L ordre est le seul point délicat, et il est
      expliqué là où il s applique.**
    ⑩ EFFET — **MODIFIE la liste de positions qu elle reçoit**, au lieu d en
      rendre une neuve.
    ⑪ TERMINAISON — Rend la main. **Aucun de ses appels ne termine.**
      [sort: non]
    """
    # SI L'APPELANT NE DONNE PAS DE REGLAGES, ON VA LES LIRE. On ne se tait
    # pas, et on n'invente pas non plus : le registre fait autorite.
    # Sans cela, `reglages` valait None par defaut et le programme n'ouvrait
    # AUCUNE position — une fonction ecrite, eprouvee par un temoin, et
    # branchee nulle part. C'est exactement le defaut releve le 02/09 sur
    # `charger_cours_du_banc` : ecrite, jamais traversee par le chemin reel.
    if reglages is None:
        try:
            reglages = reglages_du_registre(base)
        except FileNotFoundError as _e:
            reglages = {}
            _sans_registre = str(_e)
        else:
            _sans_registre = ""
    else:
        _sans_registre = ""

    # L ECHEANCE SE RECALCULE AVANT LA CLOTURE (defaut 2, 27-09-2026).
    positions, inc_e = completer_echeances(positions, cours, reglages,
                                           horizon_seances, cle)
    trades, restantes, inc_b = cloturer(positions, cours, mod, horizon_seances, cle)
    _en_attente = {id(p) for p in restantes if (p.get("statut") or "").strip() == EN_ATTENTE}
    restantes, inc_c = entrer(restantes, cours, mod, horizon_seances, cle,
                              reglages)
    # LA SEANCE D'ACHAT D'UNE POSITION ENTREE CE SOIR SE TESTE CE SOIR (R-608 ;
    # relecteur du Chat, 28-09-2026). `entrer` passe apres `cloturer` : sans ce
    # second passage, une position achetee a l'ouverture du jour D et vendue le
    # jour meme (vente forcee touchee dans la seance) restait OUVERTE le soir de D,
    # et un signal de D sur la meme strategie etait ignore en un jeton — perdu pour
    # toujours, alors que le tableau de reference le prend. Seules les positions
    # que `entrer` vient d'ouvrir repassent : les autres ont deja ete testees.
    _juste_entrees = [p for p in restantes if id(p) in _en_attente
                      and (p.get("statut") or "").strip() == OUVERTE]
    if _juste_entrees:
        # l'echeance d'une position entree en retard peut etre deja passee : on la
        # recalcule comme au premier passage, pour que l'incident le DISE
        # (relecteur du Chat, tour 2 : la vente etait juste, l'avertissement manquait)
        # Position par position, pour savoir a qui appartient chaque incident :
        # « deja passee » est toujours dit ; les autres (horizon inconnu, par exemple)
        # ne le sont ici que si la position est vendue ce soir — sinon le premier
        # passage du soir suivant les dira, et les dire ce soir les doublerait
        # (relecteur du Chat, tour 3 : une vente a l'echeance de repli passait sans un mot).
        _inc_par_pos = {}
        for _p in _juste_entrees:
            _pp, _ip = completer_echeances([_p], cours, reglages, horizon_seances, cle)
            _inc_par_pos[id(_p)] = _ip
        _t2, _r2, _i2 = cloturer(_juste_entrees, cours, mod, horizon_seances, cle)
        _fermees = {id(p) for p in _juste_entrees} - {id(p) for p in _r2}
        for _k, _ip in _inc_par_pos.items():
            inc_e = inc_e + [x for x in _ip if "deja passee" in x or _k in _fermees]
        restantes = [p for p in restantes if id(p) not in _fermees]
        trades = trades + _t2
        inc_b = inc_b + _i2
    nouvelles, ignores = ouvrir_sur_signaux(restantes, signaux, prochaine_seance)
    # UN SILENCE COMPLET DOIT SE DENONCER LUI-MEME.
    # Le 03/09, le programme a cesse d'ouvrir toute position parce qu'aucun
    # reglage ne lui etait passe. Il le faisait PROPREMENT : pas d'erreur, une
    # ligne d'incident dans un rapport que personne ne lit ligne a ligne, et le
    # radar aurait rendu « 0 position ouverte » AU VERT. Un defaut silencieux
    # etait devenu un ARRET silencieux — le pire des deux.
    # Ce drapeau existe pour que l'appelant ne puisse pas confondre « rien a
    # faire ce soir » et « je ne sais plus rien faire ».
    incidents = inc_e + inc_b + inc_c
    if _sans_registre:
        incidents.append(_sans_registre)
    _bloque = [i for i in incidents if "seuils inconnus" in i]
    # LE DRAPEAU NE DEPEND QUE DE SON OBJET.
    # Premiere version : `and not nouvelles`. Le soir ou un signal arrivait,
    # l'alerte se TAISAIT — c'est-a-dire precisement le soir ou l'on perd
    # quelque chose. Et si des signaux arrivent regulierement, elle peut ne
    # jamais se lever. L'objet de ce drapeau est « des entrees ont ete
    # bloquees faute de reglages » ; l'arrivee d'un signal n'y change rien.
    # C'est la regle enoncee le 03/09 : un controle dont le verdict depend
    # d'autre chose que de son objet ne controle pas cet objet.
    muet = bool(_bloque)
    return {
        "trades": trades,
        "positions": restantes + nouvelles,
        "signaux_ignores": ignores,
        "incidents": incidents,
        "muet": muet,
        "alerte": ("AUCUNE POSITION NE PEUT S'OUVRIR : %d signal(aux) bloque(s) "
                   "faute de reglages. Ce n'est PAS un soir sans signal, c'est "
                   "un arret." % len(_bloque)) if muet else "",
    }


# ─────────────────────────────────────────────────────────────────────
# CALIBRAGE — reproduire un résultat connu avant de produire quoi que ce soit
# ─────────────────────────────────────────────────────────────────────
def _dire(libelle, obtenu, attendu, tol=0.0):
    """Compare une valeur obtenue à une valeur attendue, et l affiche.

    ① RÔLE — **Le grain du calibrage.** Chaque vérification du calibrage passe
      par elle, et c est elle qui dit OK ou ÉCHEC.
    ② CONTEXTE D APPEL — `_calibrage`, des dizaines de fois par exécution.
    ③ ENTRÉE — `libelle` : ce qu on vérifie · `obtenu` · `attendu` ·
      `tol` : l écart toléré, **nul par défaut**.
    ④ CONDITIONS D ENTRÉE — Aucune : elle accepte nombres et chaînes.
    ⑤ SORTIE — UNE valeur : vrai si la comparaison passe.
      [rend: 1]
    ⑥ TRAITEMENT — ① compter l appel · ② **comparer avec tolérance si les deux
      valeurs sont des nombres, à l identique sinon** · ③ afficher.
    ⑦ UNITÉ — **`tol` est dans l unité de ce qui est comparé** — euros pour un
      prix, points pour un CCI. La fonction ne le sait pas.
    ⑧ POURQUOI — La tolérance existe parce qu un calcul en virgule flottante ne
      rend pas deux fois le même chiffre à la dernière décimale.
    ⑨ CE QUI CLOCHE — **Elle compte ses appels dans un attribut posé sur
      elle-même, et ce compteur n est jamais remis à zéro.** Deux calibrages dans
      le même processus additionneraient leurs appels sans qu on le voie.
      **Et une tolérance nulle par défaut sur des nombres flottants est un piège
      pour qui l appelle sans y penser.**
    ⑩ EFFET — **AFFICHE**, et **modifie son propre compteur d appels**.

    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS —
      CCI : l'indice du canal des matières premières, qui mesure de combien le cours
        s'écarte de sa moyenne récente ; sans unité, typiquement entre −200 et +200.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    _dire.appels += 1
    ok = (abs(obtenu - attendu) <= tol) if isinstance(obtenu, (int, float)) \
        and isinstance(attendu, (int, float)) else (obtenu == attendu)
    print("  %-52s %s" % (libelle, "OK" if ok else
                          "ECHEC  obtenu %r attendu %r" % (obtenu, attendu)))
    return ok


_dire.appels = 0


def _calibrage(mod, base="."):
    """LE CAS UNIBAIL DU 27-08-2026, REJOUÉ.

    C'est la première clôture sur stop du système, et elle a été recalculée au
    centime par deux chemins indépendants le 30/08 : entrée le 21/08 à 103,15,
    stop à 100,57125, plus bas du 27/08 à 98,74, perte nette de 2 796,25 EUR
    frais compris. Si ce programme ne retrouve pas ce chiffre, il ne mesure
    rien et rien ne doit être construit dessus.

    ① RÔLE — **Reproduire un trade CONNU au centime, avant que quoi que ce soit
      ne soit décidé sur l argent simulé.**
    ② CONTEXTE D APPEL — `main` avec `--calibrage`, et `tenir_pour_de_vrai` en
      tout premier.
    ③ ENTRÉE — `mod` : le moteur `programmes/MODULE_POSITIONS.py` · `base` : la racine,
      `"."` par défaut.
    ④ CONDITIONS D ENTRÉE — Les cours doivent contenir la séance de l étalon.
    ⑤ SORTIE — UNE valeur : vrai si tout le calibrage passe.
      [rend: 1]
    ⑥ TRAITEMENT — Rejouer la position étalon et comparer chaque grandeur à sa
      valeur connue, par `_dire`.
    ⑦ UNITÉ — **Euros pour les prix et la perte, pourcents pour les seuils.**
    ⑧ POURQUOI — **Le trade de référence — UNIBAIL, entrée le 21-08-2026 à 103,15,
      sortie sur stop le 27-08 à 100,57125, perte nette de 2 796,25 € — a été
      recalculé au centime par DEUX CHEMINS INDÉPENDANTS le 30-08-2026.**
    ⑨ CE QUI CLOCHE — **L étalon est figé dans le programme.** Si sa séance
      disparaissait des cours, le message se lirait comme un défaut du moteur et
      non comme une donnée manquante. **Même défaut que dans le détecteur.**
    ⑩ EFFET — **AFFICHE** chaque comparaison, et **incrémente le compteur de
      `_dire`, qui n est jamais remis à zéro.**
    ⑪ TERMINAISON — Rend la main, vrai ou faux. **`charger_cours_du_banc`, qu il
      appelle, peut lever.**
      [sort: non]
    """
    print("\n  CALIBRAGE — le cas UNIBAIL du 27-08-2026\n")
    bons = 0
    cours = {"UNIBAIL_RODAMCO": [
        {"date": "2026-08-21", "open": 103.15, "high": 103.30, "low": 102.65, "close": 103.05},
        {"date": "2026-08-24", "open": 103.00, "high": 103.70, "low": 102.10, "close": 103.00},
        {"date": "2026-08-25", "open": 103.00, "high": 103.70, "low": 102.85, "close": 103.00},
        {"date": "2026-08-26", "open": 103.65, "high": 103.75, "low": 102.15, "close": 102.25},
        {"date": "2026-08-27", "open": 101.85, "high": 102.10, "low": 98.74, "close": 99.22},
    ]}
    pos = [{"strategie": "C5E10-QA-V1", "valeur": "UNIBAIL_RODAMCO",
            "date_signal": "2026-08-20", "date_entree": "2026-08-21",
            "prix_entree": "103.15", "tp": "107.276", "sl": "100.57125",
            "horizon_fin": "2026-09-18", "statut": OUVERTE,
            "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]

    r = tenir(pos, cours, [], "2026-08-28", mod)
    t = r["trades"]
    bons += _dire("une position cloturee", len(t), 1)
    if t:
        bons += _dire("motif = SL", t[0]["motif_sortie"], "SL")
        bons += _dire("sortie au prix du stop", float(t[0]["prix_sortie"]), 100.57125, 0.00001)
        bons += _dire("perte nette = -2 796,25 EUR",
                      float(t[0]["pnl_net_eur"]), -2796.25, 0.01)
        bons += _dire("date de sortie = 27-08", t[0]["date_sortie"], "2026-08-27")
    bons += _dire("plus aucune position ouverte", len(r["positions"]), 0)

    # LE PRIX DE CONVENTION NE SE VERIFIE QUE SUR UN SAUT D'OUVERTURE.
    # Sur UNIBAIL il n'y a pas eu de saut : le prix reel et le prix theorique
    # sont identiques, et une erreur sur la convention passe INVISIBLE. Le
    # sabotage l'a montre. On rejoue donc BUREAU_VERITAS du 29-07-2026, ou le
    # cours a OUVERT a 29,24 au-dessus d'un objectif a 28,37 : le prix reel est
    # 29,24, le prix de convention reste 28,37, et l'ecart de gain est reel.
    cours_bv = {"BUREAU_VERITAS": [
        {"date": "2026-07-27", "open": 27.28, "high": 27.50, "low": 27.10, "close": 27.40},
        {"date": "2026-07-28", "open": 27.45, "high": 27.90, "low": 27.30, "close": 27.80},
        {"date": "2026-07-29", "open": 29.24, "high": 29.50, "low": 29.10, "close": 29.30},
    ]}
    pos_bv = [{"strategie": "C5-ETENDU-10", "valeur": "BUREAU_VERITAS",
               "date_signal": "2026-07-24", "date_entree": "2026-07-27",
               "prix_entree": "27.28", "tp": "28.3712", "sl": "26.598",
               "horizon_fin": "2026-08-21", "statut": OUVERTE,
               "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    rb = tenir(pos_bv, cours_bv, [], "2026-07-30", mod)
    tb = rb["trades"]
    bons += _dire("saut d'ouverture : motif TP_GAP",
                  tb[0]["motif_sortie"] if tb else "?", "TP_GAP")
    if tb:
        bons += _dire("prix reel = l'ouverture reelle",
                      float(tb[0]["prix_sortie"]), 29.24, 0.001)
        bons += _dire("prix de convention = l'objectif theorique",
                      float(tb[0]["prix_sortie_convention"]), 28.3712, 0.001)
        bons += _dire("les deux gains DIFFERENT sur un saut",
                      float(tb[0]["pnl_net_eur"]) != float(tb[0]["pnl_net_convention_eur"]),
                      True)

    # DEUX CHEMINS QUE NI UNIBAIL NI BUREAU VERITAS N'EMPRUNTENT, ET QUE LE
    # SABOTAGE A REVELES NON GARDES : la sortie au stop AVEC saut, et la sortie
    # a l'echeance. Un calibrage qui ne traverse pas un chemin ne le garde pas.
    cours_gap = {"X": [
        {"date": "2026-05-04", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0},
        {"date": "2026-05-05", "open": 94.0, "high": 95.0, "low": 93.0, "close": 94.0},
    ]}
    pg = [{"strategie": "S", "valeur": "X", "date_signal": "2026-05-01",
           "date_entree": "2026-05-04", "prix_entree": "100.0", "tp": "104.0",
           "sl": "97.5", "horizon_fin": "2026-06-01", "statut": OUVERTE,
           "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    tg = tenir(pg, cours_gap, [], "2026-05-06", mod)["trades"]
    bons += _dire("saut SOUS le stop : motif SL_GAP",
                  tg[0]["motif_sortie"] if tg else "?", "SL_GAP")
    if tg:
        bons += _dire("prix reel = l'ouverture, PIRE que le stop",
                      float(tg[0]["prix_sortie"]), 94.0, 0.001)
        bons += _dire("prix de convention = le stop theorique",
                      float(tg[0]["prix_sortie_convention"]), 97.5, 0.001)

    # LA SORTIE A L'ECHEANCE. Premiere version : ce temoin passait
    # `horizon_seances=3`, un horizon maison. Depuis le 27-09-2026,
    # l'echeance vient de l'horizon de la STRATEGIE de la position (reglages),
    # calcule par `completer_echeances` : ce temoin lui donne donc un reglage
    # explicite, egal a la constante HORIZON du module.
    _H = getattr(mod, "HORIZON", 20)
    cours_h = {"Y": [{"date": "2026-05-%02d" % (3 + i), "open": 100.0,
                      "high": 100.5, "low": 99.5, "close": 100.0}
                     for i in range(_H + 2)]}
    ph = [{"strategie": "S", "valeur": "Y", "date_signal": "2026-05-01",
           "date_entree": "2026-05-03", "prix_entree": "100.0", "tp": "104.0",
           "sl": "97.5", "horizon_fin": "", "statut": OUVERTE,
           "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    th = tenir(ph, cours_h, [], "2026-06-01", mod,
               reglages={"S": {"tp": 0.04, "sl": 0.025, "horizon": _H}})["trades"]
    bons += _dire("echeance atteinte : motif HORIZON",
                  th[0]["motif_sortie"] if th else "?", "HORIZON")
    bons += _dire("l'echeance tombe a la %de seance APRES l'entree" % _H,
                  th[0]["date_sortie"] if th else "?",
                  cours_h["Y"][_H]["date"])

    # LE CAS QUI DISCRIMINE : l'objectif est touche le 2e jour, le stop le 4e.
    # Dans l'ordre, on sort GAGNANT au TP. A l'envers, on sortirait PERDANT au
    # SL — meme donnees, resultat oppose. UNIBAIL ne discriminait pas : son
    # stop tombe le dernier jour, donc le premier a l'envers, et la reponse
    # restait juste par hasard. Un temoin qui ne discrimine pas ne garde rien.
    c_ord = {"W": [
        {"date": "2026-06-01", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0},
        {"date": "2026-06-02", "open": 100.0, "high": 105.0, "low": 99.5, "close": 104.0},
        {"date": "2026-06-03", "open": 104.0, "high": 104.5, "low": 103.0, "close": 103.5},
        {"date": "2026-06-04", "open": 103.0, "high": 103.5, "low": 96.0, "close": 97.0},
    ]}
    p_ord = {"strategie": "S", "valeur": "W", "date_signal": "2026-05-29",
             "date_entree": "2026-06-01", "prix_entree": "100.0", "tp": "104.0",
             "sl": "97.5", "horizon_fin": "2026-07-01", "statut": OUVERTE,
             "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}
    t_ord = tenir([dict(p_ord)], c_ord, [], "2026-06-05", mod)["trades"]
    bons += _dire("dans l'ordre : sortie au TP le 06-02",
                  (t_ord[0]["motif_sortie"], t_ord[0]["date_sortie"]) if t_ord else "?",
                  ("TP", "2026-06-02"))
    t_env = tenir([dict(p_ord)], {"W": list(reversed(c_ord["W"]))},
                  [], "2026-06-05", mod)["trades"]
    bons += _dire("serie a l'envers : MEME sortie, le tri corrige",
                  (t_env[0]["motif_sortie"], t_env[0]["date_sortie"]) if t_env else "?",
                  ("TP", "2026-06-02"))

    # L'ENTREE SE FAIT A L'OUVERTURE, JAMAIS AU CLOSE. Ce temoin avait ete
    # emporte par une reecriture du bloc voisin le 02/09 — le sabotage l'a
    # montre en ne tombant plus. Un temoin perdu ne se signale pas tout seul.
    # La seance du signal (01-05) figure dans les cours : depuis le
    # 27-09-2026, une position dont le signal n'est pas une seance connue
    # n'entre pas.
    cours_e = {"Z": [{"date": "2026-05-01", "open": 40.0, "high": 41.0,
                      "low": 39.0, "close": 40.5},
                     {"date": "2026-05-04", "open": 50.0, "high": 52.0,
                      "low": 49.0, "close": 51.0}]}
    pe_att = [{"strategie": "S", "valeur": "Z", "date_signal": "2026-05-01",
               "date_entree": "2026-05-04", "prix_entree": INCONNU, "tp": INCONNU,
               "sl": INCONNU, "horizon_fin": INCONNU, "statut": EN_ATTENTE,
               "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    REG = {"S": {"tp": 0.04, "sl": 0.025},
           "MA200-S1": {"tp": 0.05, "sl": 0.02}}
    re_, _ = entrer(pe_att, cours_e, mod, reglages=REG)
    bons += _dire("l'entree se fait a l'OUVERTURE (50), pas au close (51)",
                  float(re_[0]["prix_entree"]), 50.0, 0.001)
    bons += _dire("la position passe a OUVERTE", re_[0]["statut"], OUVERTE)

    # LES SEUILS POSES A L'ENTREE SONT CEUX DE LA STRATEGIE, PAS DU MODULE.
    # Sur un prix d'entree de 50 : C5E10 (+4,0 / -2,5) donne 52,00 et 48,75 ;
    # MA200-S1 (+5,0 / -2,0) donne 52,50 et 49,00. Le module, lui, aurait rendu
    # 52,00 et 48,75 pour LES DEUX.
    bons += _dire("seuils de C5E10 a l'entree : tp 52,00",
                  float(re_[0]["tp"]), 52.0, 0.001)
    # CHAQUE CAS PART D'UNE POSITION NEUVE. `entrer()` modifie la ligne qu'on
    # lui passe : reutiliser la meme fait tester une position DEJA OUVERTE, et
    # le temoin mesure alors autre chose que ce qu'il annonce.
    def _neuve(strat):
        """Fabrique une position d'épreuve, en attente d'ouverture.

        ① RÔLE — Donner au calibrage une position à faire vivre, sans toucher au fichier
        réel des positions. C'est ce qui permet d'éprouver la tenue des positions sans
        rien écrire dans les données du système.
        ② CONTEXTE D'APPEL — Définie dans `_calibrage` et appelée par elle, une fois par
        cas éprouvé.
        ③ ENTRÉE — `strat` : le nom de la stratégie à inscrire sur la position.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : une liste d'une seule position, sous la forme d'un
        dictionnaire à douze cases.
          [rend: 1]
        ⑥ TRAITEMENT — ① composer le dictionnaire avec la stratégie reçue, la valeur
        fictive « Z », un signal daté du 1ᵉʳ mai 2026 et une entrée au 4 mai · ② laisser
        inconnus le prix d'entrée, l'objectif, la perte acceptée et la fin d'horizon ·
        ③ poser le statut en attente et la comptabilité à un jeton · ④ rendre la liste.
        ⑦ UNITÉ — Les dates sont des JOURS au format année-mois-jour. Le prix, l'objectif
        et la perte acceptée seraient en EUROS, mais ne sont pas renseignés.
        ⑧ POURQUOI — Les quatre chiffres sont laissés inconnus plutôt que mis à zéro :
        zéro est une valeur, inconnu n'en est pas une, et les confondre ferait passer une
        position sans prix pour une position gratuite. C'est la même raison qui fait
        écrire « nombre d'essais inconnu » plutôt que zéro ailleurs dans le système.
        ⑨ CE QUI CLOCHE — Les deux dates et la valeur « Z » sont écrites en clair dans la
        fonction : le calibrage est donc figé sur mai 2026 et ne peut pas éprouver un cas
        qui dépendrait du calendrier réel. Relevé par lecture du code le 20-09-2026, non
        provoqué.
        ⑩ EFFET — Aucun. Elle construit un objet neuf et n'écrit aucun fichier.
        ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas revenir.
          [sort: non]
        """
        return [{"strategie": strat, "valeur": "Z", "date_signal": "2026-05-01",
                 "date_entree": "2026-05-04", "prix_entree": INCONNU,
                 "tp": INCONNU, "sl": INCONNU, "horizon_fin": INCONNU,
                 "statut": EN_ATTENTE, "comptabilite": UN_JETON,
                 "regles_pre_trade": "", "explication": ""}]
    p_ma = _neuve("MA200-S1")
    r_ma, _ = entrer(p_ma, cours_e, mod, reglages=REG)
    bons += _dire("seuils de MA200-S1 a l'entree : tp 52,50",
                  float(r_ma[0]["tp"]), 52.5, 0.001)
    bons += _dire("et son stop : sl 49,00", float(r_ma[0]["sl"]), 49.0, 0.001)

    # STRATEGIE INCONNUE : ON N'INVENTE PAS DE SEUILS, ON DIFFERE L'ENTREE.
    p_inc = _neuve("JAMAIS_VUE")
    r_inc, i_inc = entrer(p_inc, cours_e, mod, reglages=REG)
    bons += _dire("strategie inconnue : la position reste en attente",
                  r_inc[0]["statut"], EN_ATTENTE)
    bons += _dire("et un incident le dit",
                  any("seuils inconnus" in x for x in i_inc), True)

    # UN SIGNAL DU SOIR DOIT ETRE ACHETE LE LENDEMAIN — par le chemin reel.
    # Defaut trouve le 27-09-2026 : le circuit tourne le soir du signal, la
    # seance suivante n'existe pas encore, la date d'entree etait ecrite vide
    # et la position ne s'ouvrait JAMAIS. Les temoins ci-dessus passaient tous,
    # parce qu'ils fabriquaient des positions avec une date d'entree deja
    # remplie — un cas que le circuit du soir ne produit pas.
    # Soir 1 : signal sur la derniere seance connue (04-05) → en attente.
    # Soir 2 : la seance du 05-05 arrive → achat a son ouverture (52).
    cours_s1 = {"Z": [{"date": "2026-05-04", "open": 50.0, "high": 52.0,
                       "low": 49.0, "close": 51.0}]}
    cours_s2 = {"Z": cours_s1["Z"] + [{"date": "2026-05-05", "open": 52.0,
                                       "high": 53.0, "low": 51.5, "close": 52.5}]}
    cours_s3 = {"Z": cours_s2["Z"] + [{"date": "2026-05-06", "open": 60.0,
                                       "high": 61.0, "low": 59.0, "close": 60.0}]}
    sig_s = [{"strategie": "S", "valeur": "Z", "date_signal": "2026-05-04"}]
    r_s1 = tenir([], cours_s1, sig_s, None, mod, reglages=REG)
    bons += _dire("soir du signal : la position attend son entree",
                  [x["statut"] for x in r_s1["positions"]], [EN_ATTENTE, EN_ATTENTE])
    bons += _dire("soir du signal : attendre n'est pas un incident",
                  r_s1["incidents"], [])
    r_s2 = tenir(r_s1["positions"], cours_s2, [], None, mod, reglages=REG)
    bons += _dire("le lendemain : la position est OUVERTE",
                  [x["statut"] for x in r_s2["positions"]], [OUVERTE, OUVERTE])
    bons += _dire("le lendemain : entree datee de la seance qui suit le signal",
                  [x["date_entree"] for x in r_s2["positions"]],
                  ["2026-05-05", "2026-05-05"])
    bons += _dire("le lendemain : au prix d'ouverture de cette seance (52)",
                  r_s2["positions"][0]["prix_entree"], "52.00000")
    # (compare en texte : sous sabotage, le prix vaut « EN_ATTENTE » et un
    # float() ferait tomber le calibrage par une exception au lieu d'un ECHEC)
    bons += _dire("le lendemain : aucun incident",
                  r_s2["incidents"], [])

    def _att(d_sig, d_ent, cours_x):
        """Fait entrer une position d épreuve portant un signal et une date d entrée donnés.

        ① RÔLE — Éprouver `entrer` sur un couple date du signal / date d entrée
          choisi, sans répéter trois lignes par cas.
        ② CONTEXTE D APPEL — `_calibrage`, une fois par cas de date.
        ③ ENTRÉE — `d_sig` : la date du signal · `d_ent` : la date d entrée
          écrite dans la ligne · `cours_x` : les cours du cas.
        ④ CONDITIONS D ENTRÉE — Aucune : les dates peuvent être mal écrites,
          c est ce qu on éprouve.
        ⑤ SORTIE — DEUX valeurs : la position après `entrer`, et la liste
          des incidents.
          [rend: 2]
        ⑥ TRAITEMENT — ① fabriquer une position neuve de la stratégie « S » ·
          ② y poser les deux dates · ③ appeler `entrer`.
        ⑦ UNITÉ — Des jours AAAA-MM-JJ.
        ⑧ POURQUOI — Chaque cas part d une position NEUVE : `entrer` modifie la
          ligne reçue, et réutiliser la même ferait éprouver une position déjà
          ouverte.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun hors de la position fabriquée.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        p_x = _neuve("S")
        p_x[0]["date_signal"] = d_sig
        p_x[0]["date_entree"] = d_ent
        r_x, i_x = entrer(p_x, cours_x, mod, reglages=REG)
        return r_x[0], i_x

    # La meme chose quand la date vide revient du fichier : le CSV rend "" et
    # non None.
    q, i_q = _att("2026-05-04", "", cours_s2)
    bons += _dire("date d'entree relue vide du fichier : achetee le 05-05",
                  (q["statut"], q["date_entree"], i_q), (OUVERTE, "2026-05-05", []))
    # UNE DATE DE SIGNAL QUI NE PERMET PAS DE SAVOIR QUAND ACHETER : la
    # position attend, et un incident le dit — que la date d'entree soit vide
    # ou deja ecrite. « 04/05/2026 » compare comme du texte passe pour
    # anterieure a tout : elle faisait acheter a la premiere seance du
    # fichier, sans un mot.
    for lib, d_s, mot in (
            ("sans date de signal", "", "illisible"),
            ("date de signal illisible", "04/05/2026", "illisible"),
            ("date de signal impossible (mois 13)", "2026-13-45", "illisible"),
            ("signal posterieur aux cours", "2026-05-09", "cours en retard"),
            ("signal hors calendrier", "2026-05-02", "pas une seance")):
        for d_e in ("", "2026-05-05"):
            q, i_q = _att(d_s, d_e, cours_s2)
            bons += _dire("%s, entree %s : en attente, et dit"
                          % (lib, d_e or "vide"),
                          (q["statut"], any(mot in x for x in i_q)),
                          (EN_ATTENTE, True))
    # UNE DATE D'ENTREE ECRITE N'EST PAS CRUE : elle est remplacee par la
    # seance qui suit le signal, et c'est dit. Trois cas trouves par le
    # relecteur du 27-09-2026 : une entree anterieure au signal, une entree
    # qui saute une seance (achat un jour trop tard, a un autre prix), une
    # entree illisible.
    for lib, d_s, d_e, d_att, prix in (
            ("entree anterieure au signal", "2026-05-05", "2026-05-04",
             "2026-05-06", "60.00000"),
            ("entree qui saute une seance", "2026-05-04", "2026-05-06",
             "2026-05-05", "52.00000"),
            ("entree illisible", "2026-05-04", "05/05/2026",
             "2026-05-05", "52.00000")):
        q, i_q = _att(d_s, d_e, cours_s3)
        bons += _dire(lib + " : remplacee par la seance suivant le signal, et dit",
                      (q["statut"], q["date_entree"], q["prix_entree"],
                       any("remplacee" in x for x in i_q)),
                      (OUVERTE, d_att, prix, True))
    # UNE DATE FIXEE PAR LE PROGRAMME AVANT UN RATTRAPAGE DE COURS NE BLOQUE
    # PAS LA POSITION. Soir A : toute la bourse n'a pas le 05-05 ; Y a le
    # 06-05, Z pas encore → date 06-05, attente. Soir B : le rattrapage apporte
    # 05-05, 06-05 et 07-05 a tous → la seance qui suit le signal est le 05-05 :
    # achat au 05-05, a son ouverture.
    c_a = {"Y": [{"date": x, "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}
                 for x in ("2026-05-04", "2026-05-06")],
           "Z": [cours_s1["Z"][0]]}
    c_b = {"Y": [{"date": x, "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}
                 for x in ("2026-05-04", "2026-05-05", "2026-05-06", "2026-05-07")],
           "Z": cours_s3["Z"] + [{"date": "2026-05-07", "open": 61.0,
                                  "high": 61.0, "low": 61.0, "close": 61.0}]}
    p_r = _neuve("S")
    p_r[0]["date_signal"] = "2026-05-04"
    p_r[0]["date_entree"] = ""
    r_ra, _ = entrer(p_r, c_a, mod, reglages=REG)
    d_soir_a = r_ra[0]["date_entree"]  # releve AVANT : `entrer` modifie la ligne
    r_rb, _ = entrer(r_ra, c_b, mod, reglages=REG)
    bons += _dire("rattrapage de cours : achat a la vraie seance suivante (05-05)",
                  (d_soir_a, r_rb[0]["statut"], r_rb[0]["date_entree"],
                   r_rb[0]["prix_entree"]),
                  ("2026-05-06", OUVERTE, "2026-05-05", "52.00000"))
    # Une seance d'entree qui manque pour la valeur alors que la bourse est
    # passee au-dela n'est plus une attente normale : on le dit.
    c_manque = {"Y": [{"date": x, "open": 1.0, "high": 1.0, "low": 1.0,
                       "close": 1.0} for x in ("2026-05-04", "2026-05-05",
                                               "2026-05-06")],
                "Z": [cours_s1["Z"][0]]}
    q, i_q = _att("2026-05-04", "2026-05-05", c_manque)
    bons += _dire("seance d'entree manquante et depassee : un incident le dit",
                  (q["statut"], any("absente des cours" in x for x in i_q)),
                  (EN_ATTENTE, True))
    # Et une seance d'entree simplement pas encore publiee reste silencieuse.
    c_futur = {"Y": c_manque["Y"][:2], "Z": [cours_s1["Z"][0]]}
    q, i_q = _att("2026-05-04", "", c_futur)
    bons += _dire("seance d'entree pas encore publiee pour la valeur : attente muette",
                  (q["statut"], q["date_entree"], i_q), (EN_ATTENTE, "2026-05-05", []))
    # LA SEANCE SUIVANTE EST CELLE DE LA BOURSE, PAS CELLE DE LA VALEUR.
    # Y a la seance du 05-05, Z ne l'a pas (trou de donnees) et a celle du
    # 06-05. Z doit etre datee du 05-05 et rester bloquee — surtout pas achetee
    # le 06-05, un autre jour, a un autre prix.
    c_trou = {"Y": c_manque["Y"][:2],
              "Z": [cours_s1["Z"][0], cours_s3["Z"][2]]}
    q, i_q = _att("2026-05-04", "", c_trou)
    bons += _dire("trou de donnees : datee du 05-05, pas achetee le 06-05",
                  (q["date_entree"], q["statut"],
                   any("absente des cours" in x for x in i_q)),
                  ("2026-05-05", EN_ATTENTE, True))

    # L'ECHEANCE : h SEANCES APRES LA SEANCE D'ACHAT, ET SEULEMENT QUAND ELLE
    # EXISTE (defaut 2 de A-491, 27-09-2026). Avant : calculee le soir de
    # l'achat sur les seules seances connues, elle tombait sur la seance
    # d'achat, et la position etait vendue le lendemain « HORIZON ».
    # Par le chemin reel : soir du signal (04-05), soir de l'achat (05-05),
    # puis le lendemain (06-05). La position doit rester ouverte.
    r_e1 = tenir([], cours_s1, sig_s, None, mod, reglages=REG)
    r_e2 = tenir(r_e1["positions"], cours_s2, [], None, mod, reglages=REG)
    bons += _dire("soir de l'achat : echeance inconnue, pas la seance d'achat",
                  [x["horizon_fin"] for x in r_e2["positions"]], [INCONNU, INCONNU])
    # (le 06-05 est une seance calme : ni objectif ni vente forcee touches)
    cours_e3 = {"Z": cours_s2["Z"] + [{"date": "2026-05-06", "open": 52.0,
                                       "high": 52.5, "low": 51.8, "close": 52.0}]}
    r_e3 = tenir(r_e2["positions"], cours_e3, [], None, mod, reglages=REG)
    bons += _dire("le lendemain de l'achat : pas de vente, la position reste",
                  (len(r_e3["trades"]), [x["statut"] for x in r_e3["positions"]]),
                  (0, [OUVERTE, OUVERTE]))
    # Une echeance fausse deja ecrite (la seance d'achat, comme le faisait
    # l'ancienne version) est remplacee, et c'est dit.
    c_plat = {"Z": [{"date": "2026-05-%02d" % j, "open": 100.0, "high": 100.5,
                     "low": 99.5, "close": 100.0} for j in range(4, 12)]}
    p_ech = _neuve("S")
    p_ech[0].update({"date_signal": "2026-05-04", "date_entree": "2026-05-05",
                     "prix_entree": "100.00000", "tp": "104.00000",
                     "sl": "97.50000", "horizon_fin": "2026-05-05",
                     "statut": OUVERTE})
    r_ech = tenir(p_ech, c_plat, [], None, mod, reglages=REG)
    bons += _dire("echeance ecrite fausse : pas de vente, remplacee, et dit",
                  (len(r_ech["trades"]), r_ech["positions"][0]["horizon_fin"]
                   if r_ech["positions"] else "?",
                   any("remplacee" in x for x in r_ech["incidents"])),
                  (0, INCONNU, True))
    # L'horizon de SA strategie : 5 seances -> vente a la cloture de la 5e
    # seance APRES l'achat (05-05 + 5 seances = 05-10), pas la 4e.
    REG5 = dict(REG); REG5["S5"] = {"tp": 0.04, "sl": 0.025, "horizon": 5}
    p_h5 = _neuve("S5")
    p_h5[0].update({"date_signal": "2026-05-04", "date_entree": "2026-05-05",
                    "prix_entree": "100.00000", "tp": "104.00000",
                    "sl": "97.50000", "horizon_fin": INCONNU, "statut": OUVERTE})
    r_h5 = tenir(p_h5, c_plat, [], None, mod, reglages=REG5)
    bons += _dire("horizon 5 : vente HORIZON a la 5e seance apres l'achat (05-10)",
                  [(x["motif_sortie"], x["date_sortie"]) for x in r_h5["trades"]],
                  [("HORIZON", "2026-05-10")])
    # Une echeance pas encore publiee n'a pas de repli : horizon 25, et
    # seulement 22 seances connues apres l'achat -> aucune vente, meme si
    # 20 seances sont passees (l'ancien repli vendait a la 20e).
    c_long = {"Z": [{"date": "2026-06-%02d" % j, "open": 100.0, "high": 100.5,
                     "low": 99.5, "close": 100.0} for j in range(1, 24)]}
    REG25 = dict(REG); REG25["S25"] = {"tp": 0.04, "sl": 0.025, "horizon": 25}
    p_25 = _neuve("S25")
    p_25[0].update({"date_signal": "2026-05-29", "date_entree": "2026-06-01",
                    "prix_entree": "100.00000", "tp": "104.00000",
                    "sl": "97.50000", "horizon_fin": INCONNU, "statut": OUVERTE})
    r_25 = tenir(p_25, c_long, [], None, mod, reglages=REG25)
    bons += _dire("horizon 25, 22 seances connues : aucune vente, pas de repli a 20",
                  (len(r_25["trades"]), r_25["positions"][0]["horizon_fin"]
                   if r_25["positions"] else "?"), (0, INCONNU))
    # Une seance d'achat absente des cours : l'echeance ne se calcule pas,
    # et c'est dit.
    p_abs = _neuve("S")
    p_abs[0].update({"date_entree": "2026-04-30", "prix_entree": "100.00000",
                     "tp": "104.00000", "sl": "97.50000", "statut": OUVERTE})
    r_abs = tenir(p_abs, c_plat, [], None, mod, reglages=REG)
    bons += _dire("seance d'achat absente : echeance inconnue, et dit",
                  (r_abs["positions"][0]["horizon_fin"] if r_abs["positions"] else "?",
                   any("absente des cours" in x for x in r_abs["incidents"])),
                  (INCONNU, True))
    # ... mais une echeance deja ecrite et valide est GARDEE : l'effacer
    # priverait la position de toute sortie a l'echeance, pour toujours.
    p_gar = _neuve("S")
    p_gar[0].update({"date_entree": "2026-04-30", "prix_entree": "100.00000",
                     "tp": "104.00000", "sl": "97.50000",
                     "horizon_fin": "2026-05-08", "statut": OUVERTE})
    r_gar = tenir(p_gar, c_plat, [], None, mod, reglages=REG)
    bons += _dire("seance d'achat absente, echeance ecrite valide : gardee",
                  [(x["motif_sortie"], x["date_sortie"]) for x in r_gar["trades"]],
                  [("HORIZON", "2026-05-08")])
    # Une date d'achat mal ecrite se dit « illisible », pas « absente ».
    p_ill = _neuve("S")
    p_ill[0].update({"date_entree": "05/05/2026", "prix_entree": "100.00000",
                     "tp": "104.00000", "sl": "97.50000", "statut": OUVERTE})
    r_ill = tenir(p_ill, c_plat, [], None, mod, reglages=REG)
    bons += _dire("date d'achat mal ecrite : dite illisible",
                  any("illisible" in x for x in r_ill["incidents"]), True)
    # Une echeance ecrite illisible est remplacee, et c'est dit.
    p_eil = _neuve("S5")
    p_eil[0].update({"date_signal": "2026-05-04", "date_entree": "2026-05-05",
                     "prix_entree": "100.00000", "tp": "104.00000",
                     "sl": "97.50000", "horizon_fin": "10/05/2026",
                     "statut": OUVERTE})
    r_eil = tenir(p_eil, {"Z": c_plat["Z"][:5]}, [], None, mod, reglages=REG5)
    bons += _dire("echeance ecrite illisible : remplacee, et dit",
                  any("remplacee" in x for x in r_eil["incidents"]), True)
    # UN SOIR NORMAL NE DIT RIEN : l'echeance devient connue le soir meme ou
    # sa seance est publiee, et la vente se fait ce soir-la, sans incident.
    p_nor = _neuve("S5")
    p_nor[0].update({"date_signal": "2026-05-04", "date_entree": "2026-05-05",
                     "prix_entree": "100.00000", "tp": "104.00000",
                     "sl": "97.50000", "horizon_fin": INCONNU, "statut": OUVERTE})
    r_nor = tenir(p_nor, {"Z": c_plat["Z"][:7]}, [], None, mod, reglages=REG5)
    bons += _dire("soir normal de l'echeance : vente le 05-10, aucun incident",
                  ([(x["motif_sortie"], x["date_sortie"]) for x in r_nor["trades"]],
                   r_nor["incidents"]), ([("HORIZON", "2026-05-10")], []))
    # Apres des soirs manques, l'echeance deja passee se dit.
    bons += _dire("echeance deja passee (soirs manques) : c'est dit",
                  any("deja passee" in x for x in r_h5["incidents"]), True)
    bons += _dire("strategie sans horizon aux reglages : le repli est dit",
                  any("horizon inconnu" in x for x in r_ech["incidents"]), True)
    bons += _dire("echeance pas encore publiee : aucun incident",
                  r_25["incidents"], [])
    # `echeance` trie la serie ; `completer_echeances` passe par `cle` ;
    # `horizon_de` lit la strategie sans ses espaces ; `entrer` pose deja
    # l'echeance si sa seance est publiee le soir de l'achat.
    bons += _dire("echeance sur une serie a l'envers : 05-10",
                  echeance(list(reversed(c_plat["Z"])), "2026-05-05", 5), "2026-05-10")
    p_cle = _neuve("S5")
    p_cle[0].update({"date_entree": "2026-05-05", "statut": OUVERTE,
                     "horizon_fin": INCONNU})
    completer_echeances(p_cle, {"Z_CLE": c_plat["Z"]}, REG5, 20,
                        cle=lambda x: x + "_CLE")
    bons += _dire("completer_echeances passe par cle", p_cle[0]["horizon_fin"],
                  "2026-05-10")
    bons += _dire("echeance : une seance en double comptee une fois",
                  echeance(c_plat["Z"][:3] + c_plat["Z"][2:], "2026-05-05", 5),
                  "2026-05-10")
    bons += _dire("horizon a 0 : repli, jamais la seance d'achat",
                  horizon_de({"strategie": "S0"}, {"S0": {"horizon": 0}}, 20), 20)
    p_h0 = _neuve("S0")
    p_h0[0].update({"date_entree": "2026-05-05", "statut": OUVERTE})
    _, i_h0 = completer_echeances(p_h0, c_plat, {"S0": {"horizon": 0}}, 20)
    # LE VRAI CHEMIN : un registre qui porte « ² » ne fait pas planter la
    # lecture des reglages (avant le 27-09-2026 : ValueError).
    import tempfile as _tf2
    _d2 = _tf2.mkdtemp()
    with open(os.path.join(_d2, "cac40_strategies.csv"), "w", encoding="utf-8", newline="") as _f2:
        _f2.write("id,nom,etat_vie,tp,sl,horizon\n"
                  "XA,Essai A,LABO,+4.0%,-2.5%,\u00b2\n"
                  "XB,Essai B,LABO,+4.0%,-2.5%,20j\n")
    try:
        _rx = reglages_du_registre(_d2)
        _lu = (_rx.get("XA", {}).get("horizon"), _rx.get("XB", {}).get("horizon"))
    except ValueError:
        _lu = "plantage"
    import shutil as _sh2
    _sh2.rmtree(_d2, ignore_errors=True)
    bons += _dire("registre avec un horizon « \u00b2 » : lu illisible, sans planter",
                  _lu, (None, 20))
    bons += _dire("horizon a 0 aux reglages : dit comme inconnu",
                  any("horizon inconnu" in x for x in i_h0), True)
    bons += _dire("horizons illisibles refuses : vide, 0, 00, mal ecrit, exposant",
                  horizons_illisibles([{"id": "A", "horizon": ""}, {"id": "B", "horizon": "0"},
                                       {"id": "C", "horizon": "00"}, {"id": "D", "horizon": "vingt"},
                                       {"id": "E", "horizon": "\u00b2"}, {"id": "F", "horizon": "20"},
                                       {"id": "G", "horizon": "20j"}]),
                  ["A", "B", "C", "D", "E"])
    # Apres une panne, l'echeance deja ecrite et deja passee se dit aussi.
    p_pan = _neuve("S5")
    p_pan[0].update({"date_signal": "2026-05-04", "date_entree": "2026-05-05",
                     "prix_entree": "100.00000", "tp": "104.00000",
                     "sl": "97.50000", "horizon_fin": "2026-05-10", "statut": OUVERTE})
    r_pan = tenir(p_pan, c_plat, [], None, mod, reglages=REG5)
    bons += _dire("echeance ecrite deja passee : vente au 05-10, et dit",
                  ([(x["motif_sortie"], x["date_sortie"]) for x in r_pan["trades"]],
                   any("deja passee" in x for x in r_pan["incidents"])),
                  ([("HORIZON", "2026-05-10")], True))
    bons += _dire("horizon_de lit la strategie sans ses espaces",
                  horizon_de({"strategie": " S5 "}, REG5, 20), 5)
    p_ent = _neuve("S5")
    p_ent[0].update({"date_signal": "2026-05-04", "date_entree": ""})
    r_ent, _ = entrer(p_ent, c_plat, mod, reglages=REG5)
    bons += _dire("entrer pose l'echeance quand sa seance est publiee",
                  (r_ent[0]["date_entree"], r_ent[0]["horizon_fin"]),
                  ("2026-05-05", "2026-05-10"))

    # DEUX STRATEGIES AUX SEUILS DIFFERENTS DOIVENT SORTIR DIFFEREMMENT.
    # C'est le defaut trouve le 02-09-2026 : `sortie_position` recalcule les
    # seuils depuis deux constantes fixes du module, alors que le registre en
    # donne PAR STRATEGIE — MA200-S1 est a +5,0 / -2,0 quand C5E10 est a
    # +4,0 / -2,5. Une position de MA200 aurait ete cloturee aux seuils de
    # C5E10, EN SILENCE. Ce temoin garde le fait que les seuils viennent bien
    # de la position.
    c_deux = {"V": [
        {"date": "2026-04-01", "open": 100.0, "high": 100.5, "low": 99.5, "close": 100.0},
        {"date": "2026-04-02", "open": 100.0, "high": 100.5, "low": 97.8, "close": 98.0},
    ]}
    base_p = {"strategie": "?", "valeur": "V", "date_signal": "2026-03-30",
              "date_entree": "2026-04-01", "prix_entree": "100.0",
              "horizon_fin": "", "statut": OUVERTE, "comptabilite": UN_JETON,
              "regles_pre_trade": "", "explication": ""}
    # C5E10 : stop a -2,5 % = 97,5 -> le bas de 97,8 ne le touche PAS
    p_a = dict(base_p); p_a["strategie"] = "C5E10"; p_a["tp"] = "104.0"; p_a["sl"] = "97.5"
    t_a = tenir([p_a], c_deux, [], "2026-04-03", mod)["trades"]
    bons += _dire("seuil -2,5 % : pas de cloture (bas 97,8 > 97,5)", len(t_a), 0)
    # MA200 : stop a -2,0 % = 98,0 -> le bas de 97,8 le touche
    p_b = dict(base_p); p_b["strategie"] = "MA200"; p_b["tp"] = "105.0"; p_b["sl"] = "98.0"
    t_b = tenir([p_b], c_deux, [], "2026-04-03", mod)["trades"]
    bons += _dire("seuil -2,0 % : cloture au stop de CETTE strategie",
                  float(t_b[0]["prix_sortie"]) if t_b else 0, 98.0, 0.001)

    # LE PROGRAMME SAIT LIRE LES REGLAGES LUI-MEME — sans quoi il n'ouvre
    # RIEN et le silence est invisible. Ce temoin traverse la lecture du vrai
    # registre quand il est la.
    # `base` DOIT DESIGNER LE DOSSIER OU LE MODULE A ETE TROUVE.
    # Sans ce temoin, neutraliser la transmission de `base` ne faisait rien
    # tomber : les autres temoins fabriquent leur propre dossier et ne
    # traversent donc pas `base`. Lance depuis ailleurs avec un `base` faux,
    # le module devient introuvable — et c'est exactement ce qu'on veut voir.
    try:
        trouver_module(base)
        _base_ok = True
    except FileNotFoundError:
        _base_ok = False
    bons += _dire("`base` designe bien le dossier du module", _base_ok, True)

    # LE DRAPEAU SE LEVE MEME QUAND UN SIGNAL ARRIVE — c'est le soir ou il sert
    # le plus. Ce temoin avait disparu dans une reecriture le 03/09, et le
    # sabotage l'a montre en cessant de tomber. Un temoin perdu ne se signale
    # jamais tout seul.
    _bl = [{"strategie": "INCONNUE", "valeur": "Z", "date_signal": "2026-05-01",
            "date_entree": "2026-05-04", "prix_entree": INCONNU, "tp": INCONNU,
            "sl": INCONNU, "horizon_fin": INCONNU, "statut": EN_ATTENTE,
            "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    # (la seance du signal, 01-05, figure dans les cours : depuis le
    # 27-09-2026, une position dont le signal n'est pas une seance connue
    # n'atteint pas le controle des reglages)
    _cz3 = {"Z": [{"date": "2026-05-01", "open": 40.0, "high": 41.0,
                   "low": 39.0, "close": 40.5},
                  {"date": "2026-05-04", "open": 50.0, "high": 52.0,
                   "low": 49.0, "close": 51.0}]}
    _av = tenir(_bl, _cz3, [{"strategie": "S", "valeur": "Z",
                             "date_signal": "2026-05-04"}],
                "2026-05-05", mod, reglages={"S": {"tp": 0.04, "sl": 0.025}})
    bons += _dire("le drapeau se leve MEME avec un nouveau signal",
                  _av["muet"], True)
    bons += _dire("un soir normal n'est pas denonce comme muet",
                  tenir([], {}, [], "2026-05-05", mod, reglages={})["muet"], False)

    # LES TEMOINS DU REGISTRE NE DEPENDENT PLUS DE L'ENVIRONNEMENT.
    # Premiere version : ils vivaient dans un « if le registre existe ». Lance
    # ailleurs, le bloc etait SAUTE — et deux sabotages ne tombaient plus :
    # « base ne descend plus » et « lecture auto des reglages ». Un temoin
    # qu'on peut sauter ne garde rien. C'est la regle enoncee par la relecture
    # adverse le 03/09 : un controle dont le verdict depend de son
    # environnement plutot que de son objet ne controle pas cet objet.
    # On FABRIQUE donc le registre dont on a besoin, dans un dossier a nous.
    import tempfile as _tf
    _dir = _tf.mkdtemp()
    with open(os.path.join(_dir, "cac40_strategies.csv"), "w",
              encoding="utf-8", newline="") as _f:
        _f.write("id,nom,etat_vie,tp,sl\n"
                 "C5E10-QA-V1,COURS_BAS_ARGENT_REVIENT_6 (C5-ETENDU-10),QA,+4.0%,-2.5%\n"
                 "MA200-S1,Retournement haussier,PRODUCTION,\"+5,0 %\",\"-2,0 %\"\n"
                 "VIDE-01,Sans seuils,LABO,,\n")
    _r = reglages_du_registre(_dir)
    bons += _dire("le registre rend des reglages", len(_r) > 0, True)
    bons += _dire("il connait une strategie par son IDENTIFIANT",
                  "C5E10-QA-V1" in _r, True)
    bons += _dire("et la meme par son NOM",
                  "COURS_BAS_ARGENT_REVIENT_6" in _r, True)
    bons += _dire("virgule decimale et espace absorbes (+5,0 %% -> 0,05)",
                  _r.get("MA200-S1", {}).get("tp"), 0.05, 0.0001)
    bons += _dire("le stop est rendu POSITIF (-2,0 %% -> 0,02)",
                  _r.get("MA200-S1", {}).get("sl"), 0.02, 0.0001)
    bons += _dire("une ligne sans seuils est EXCLUE, pas inventee",
                  "VIDE-01" in _r, False)

    # LA LECTURE AUTOMATIQUE EST TRAVERSEE, ET DEPUIS `base`.
    # Ce temoin echoue si `base` cesse de descendre ou si la lecture auto est
    # neutralisee — les deux sabotages qui passaient encore le 03/09.
    _p_auto = [{"strategie": "MA200-S1", "valeur": "Z", "date_signal": "2026-05-01",
                "date_entree": "2026-05-04", "prix_entree": INCONNU,
                "tp": INCONNU, "sl": INCONNU, "horizon_fin": INCONNU,
                "statut": EN_ATTENTE, "comptabilite": UN_JETON,
                "regles_pre_trade": "", "explication": ""}]
    _cz2 = {"Z": [{"date": "2026-05-01", "open": 40.0, "high": 41.0,
                   "low": 39.0, "close": 40.5},
                  {"date": "2026-05-04", "open": 50.0, "high": 52.0,
                   "low": 49.5, "close": 51.0}]}
    # plus bas 49,5 et non 49,0 depuis le 28-09-2026 : a -2,0 % sur 50, la vente
    # forcee vaut 49,0 ; touchee le jour de l'achat, elle vend desormais la position
    # ce jour-la (R-608), et ce temoin-ci ne porte pas sur la vente.
    _r_auto = tenir(_p_auto, _cz2, [], "2026-05-05", mod, base=_dir)
    bons += _dire("sans reglages fournis, la position s'ouvre quand meme",
                  _r_auto["positions"][0]["statut"], OUVERTE)
    bons += _dire("et aux seuils du REGISTRE (+5,0 %% sur 50 -> 52,50)",
                  float(_r_auto["positions"][0]["tp"]), 52.5, 0.001)
    import shutil as _sh
    _sh.rmtree(_dir, ignore_errors=True)

    # LE CHARGEUR DU JUGE DES STRATÉGIES EST APPELE ICI, sans quoi il ne serait garde par
    # rien. Cowork l'a releve le 02/09 : defini, jamais traverse. Une fonction
    # qu'aucun controle n'emprunte n'est pas eprouvee — elle est seulement
    # ecrite. On la fait donc travailler sur les vrais fichiers du projet
    # quand ils sont la, et on dit franchement quand ils ne le sont pas.
    # CORRIGE LE 24-09-2026 — releve par Cowork : ce bloc cherchait les anciens
    # fichiers a la RACINE du depot, ou ils ne sont pas ; il ne traversait jamais
    # le chargeur et le calibrage disait pourtant OK. Il eprouve desormais le
    # chargeur sur le fichier maitre, designe par `_fichiers_de_cours` (A-442), et
    # un chargeur non traverse FAIT ECHOUER le calibrage (R-734).
    try:
        _f = list(_fichiers_de_cours(base))
    except FileNotFoundError as _e:
        _f = []
        print("  chargeur du juge des stratégies : %s" % _e)
    if _f:
        _c = charger_cours_du_banc(base, *_f)
        bons += _dire("le chargeur du juge des stratégies rend des valeurs", len(_c) > 0, True)
        _u = _c.get("UNIBAIL_RODAMCO", [])
        bons += _dire("il rapproche les deux graphies d'UNIBAIL", len(_u) > 0, True)
        bons += _dire("et il rend une serie TRIEE",
                      _u == sorted(_u, key=lambda b: b["date"]), True)
    else:
        bons += _dire("le chargeur du juge des stratégies a ete eprouve sur le fichier maitre",
                      False, True)

    # LE JETON UNIQUE : un signal pendant une position en cours est IGNORE
    pos2 = [{"strategie": "S", "valeur": "A", "date_signal": "2026-08-20",
             "date_entree": "2026-08-21", "prix_entree": "100", "tp": "104",
             "sl": "97.5", "horizon_fin": "2026-09-18", "statut": OUVERTE,
             "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    n, ig = ouvrir_sur_signaux(pos2, [{"strategie": "S", "valeur": "B",
                                       "date_signal": "2026-08-27"}], "2026-08-28")
    bons += _dire("un jeton : le signal est ignore", len(ig), 1)
    bons += _dire("jetons illimites : il est ouvert quand meme",
                  sum(1 for x in n if x["comptabilite"] == JETONS_ILLIMITES), 1)

    # LA SEANCE D'ACHAT COMPTE (R-608 ; defaut 4 de A-491, 28-09-2026). Deux VRAIS cas
    # du tableau de reference des 100 trades, cours reels du fichier maitre, plus le
    # cas des deux seuils touches le jour de l'achat (R-602 : la perte compte).
    def _une(v, d_ent, pe, tp_, sl_, barres):
        """Fait passer une seule position ouverte par le circuit du soir et rend ses ventes.

        ① RÔLE — Rejouer un cas connu de vente par le VRAI circuit (`tenir`), pas par
          une copie de sa logique.
        ② CONTEXTE D'APPEL — Le calibrage de ce programme, trois fois : Vinci
          07-06-2024, Airbus 11-10-2024, et le cas des deux seuils touchés le jour de
          l'achat.
        ③ ENTRÉE — `v` : la valeur · `d_ent` : la date d'achat, AAAA-MM-JJ · `pe`,
          `tp_`, `sl_` : prix d'achat, objectif et vente forcée, en texte comme dans
          le fichier des positions · `barres` : les séances de cette valeur.
        ④ CONDITIONS D'ENTRÉE — `mod`, le module des positions, est chargé par le
          calibrage avant le premier appel.
        ⑤ SORTIE — UNE valeur : la liste des ventes que `tenir` rend pour cette
          position, vide si elle reste ouverte.
          [rend: 1]
        ⑥ TRAITEMENT — ① bâtir une position OUVERTE au livre « un jeton », stratégie
          « S », sans date d'échéance · ② la passer à `tenir` avec ses seules
          séances, sans signal et sans stratégie connue : `tenir` pose alors
          l'échéance de repli de 20 séances et le dit dans ses incidents · ③ rendre
          les ventes, et elles seules — l'incident « horizon inconnu » n'est pas
          rendu, les trois cas se jugeant sur la vente.
        ⑦ UNITÉ — Les prix sont en EUROS PAR ACTION.
        ⑧ POURQUOI — R-608 (la séance d'achat compte) se prouve sur de vrais cas du
          tableau de référence des 100 trades ; passer par `tenir` éprouve aussi
          l'ordre des étapes du soir.
        ⑨ CE QUI CLOCHE — L'échéance de repli n'intervient dans aucun des trois
          cas (ils se vendent en une ou deux séances) ; un cas qui durerait plus de
          20 séances serait vendu à cette échéance sans que le calibrage le voie.
        ⑩ EFFET — Aucun fichier : `tenir` travaille en mémoire.
        ⑪ TERMINAISON — Rend la main quand `tenir` la rend.
          [sort: non]
        """
        return tenir([{"strategie": "S", "valeur": v, "date_signal": "", "date_entree": d_ent,
                       "prix_entree": pe, "tp": tp_, "sl": sl_, "horizon_fin": "",
                       "statut": OUVERTE, "comptabilite": UN_JETON, "regles_pre_trade": "",
                       "explication": ""}], {v: barres}, [], None, mod)["trades"]
    _tv = _une("VINCI", "2024-06-07", "113.60", "118.144", "110.76", [
        {"date": "2024-06-07", "open": 113.6, "high": 113.8, "low": 110.75, "close": 110.75},
        {"date": "2024-06-10", "open": 106.2, "high": 106.95, "low": 102.9, "close": 104.8}])
    bons += _dire("Vinci 07-06-2024 : vendu le jour de l'achat",
                  (_tv[0]["date_sortie"], _tv[0]["motif_sortie"]) if _tv else None, ("2024-06-07", "SL"))
    bons += _dire("Vinci : au prix de la vente forcee, 110,76",
                  float(_tv[0]["prix_sortie"]) if _tv else None, 110.76, 0.00001)
    _ta = _une("AIRBUS", "2024-10-11", "127.74", "132.8496", "124.5465", [
        {"date": "2024-10-11", "open": 127.74, "high": 133.46, "low": 126.26, "close": 132.92},
        {"date": "2024-10-14", "open": 133.48, "high": 135.32, "low": 132.1, "close": 135.12}])
    bons += _dire("Airbus 11-10-2024 : vendu a l'objectif le jour de l'achat",
                  (_ta[0]["date_sortie"], _ta[0]["motif_sortie"], round(float(_ta[0]["prix_sortie"]), 4)) if _ta else None,
                  ("2024-10-11", "TP", 132.8496))
    _tb = _une("X", "2024-05-06", "100", "104", "97.5", [
        {"date": "2024-05-06", "open": 100.0, "high": 105.0, "low": 97.0, "close": 101.0}])
    bons += _dire("deux seuils le jour de l'achat : la perte compte (R-602)",
                  (_tb[0]["motif_sortie"], float(_tb[0]["prix_sortie"])) if _tb else None, ("SL", 97.5))

    # ET LE SOIR MEME DE L'ACHAT : une position entree ce soir et vendue le jour de
    # son achat libere son jeton ce soir, et le signal du jour sur la meme
    # strategie est pris (relecteur du Chat, 28-09-2026). Sans le second passage de
    # `tenir`, le signal etait ignore : perdu pour toujours.
    _ca = [{"date": "2026-05-04", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0},
           {"date": "2026-05-05", "open": 100.0, "high": 100.5, "low": 97.0, "close": 97.2}]
    _cb = [dict(x, open=50.0, high=51.0, low=49.0, close=50.0) for x in _ca]
    _pa = [{"strategie": "S", "valeur": "A", "date_signal": "2026-05-04", "date_entree": "",
            "prix_entree": INCONNU, "tp": INCONNU, "sl": INCONNU, "horizon_fin": INCONNU,
            "statut": EN_ATTENTE, "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    _rs = tenir(_pa, {"A": _ca, "B": _cb},
                [{"strategie": "S", "valeur": "B", "date_signal": "2026-05-05"}], None, mod,
                reglages={"S": {"tp": 0.04, "sl": 0.025, "horizon": 20}})
    bons += _dire("achat et vente forcee le meme jour : vendu le soir meme",
                  [(x["valeur"], x["date_sortie"], x["motif_sortie"]) for x in _rs["trades"]],
                  [("A", "2026-05-05", "SL")])
    bons += _dire("et le jeton libere prend le signal du jour", len(_rs["signaux_ignores"]), 0)
    # ENTREE EN RETARD : l'echeance est deja passee le soir de l'entree -> vendue a
    # l'echeance, ET c'est dit (relecteur du Chat, tour 2, 28-09-2026).
    import datetime as _dt
    _cl = [{"date": str(_dt.date(2026, 5, 4) + _dt.timedelta(days=k)), "open": 100.0,
            "high": 100.5, "low": 99.5, "close": 100.0} for k in range(12)]
    _pl = [{"strategie": "S", "valeur": "L", "date_signal": _cl[0]["date"], "date_entree": "",
            "prix_entree": INCONNU, "tp": INCONNU, "sl": INCONNU, "horizon_fin": INCONNU,
            "statut": EN_ATTENTE, "comptabilite": UN_JETON, "regles_pre_trade": "", "explication": ""}]
    _rl = tenir(_pl, {"L": _cl}, [], None, mod,
                reglages={"S": {"tp": 0.04, "sl": 0.025, "horizon": 5}})
    bons += _dire("entree en retard : vendue a l'echeance le soir meme",
                  [(x["date_sortie"], x["motif_sortie"]) for x in _rl["trades"]], [("2026-05-10", "HORIZON")])
    bons += _dire("et l'echeance deja passee est dite",
                  any("deja passee" in x for x in _rl["incidents"]), True)
    # et si l'horizon de la strategie est inconnu, la vente a l'echeance de REPLI le dit
    _pl2 = [dict(_pl[0], valeur="M", statut=EN_ATTENTE, date_entree="", prix_entree=INCONNU,
                 tp=INCONNU, sl=INCONNU, horizon_fin=INCONNU)]
    _cl2 = [dict(b, date=str(_dt.date(2026, 5, 4) + _dt.timedelta(days=k))) for k, b in enumerate(_cl * 3)]
    _rl2 = tenir(_pl2, {"M": _cl2}, [], None, mod, reglages={"S": {"tp": 0.04, "sl": 0.025}})
    bons += _dire("entree en retard, horizon inconnu : le repli est dit",
                  any("horizon inconnu" in x for x in _rl2["incidents"]) and len(_rl2["trades"]) == 1, True)

    # LA COMPTABILITE ARRIVE AU JOURNAL (defaut 3 de A-491, 27-09-2026).
    # Avant, elle etait jetee a l ecriture : chaque vente etait comptee dans
    # les deux comptabilites. Les lignes ci-dessous gardent les deux bouts :
    # la cloture la porte, et le controle d ecriture refuse ce qui la perdrait.
    bons += _dire("la cloture Unibail porte sa comptabilite",
                  t[0].get("comptabilite") if t else "?", UN_JETON)
    bons += _dire("une vraie cloture respecte le contrat du journal",
                  fautes_d_ecriture(t, TRADE, "journal") if t else ["?"], [])
    bons += _dire("les positions ouvertes respectent leur contrat",
                  fautes_d_ecriture(n, POSITION, "positions"), [])
    # VRAIE LIGNE DU JOURNAL, telle qu elle etait ecrite avant le 27-09-2026 :
    # sans colonne comptabilite (R-732 : un cas au moins vient d une vraie ligne).
    _bv = {"strategie": "C5-ETENDU-10", "valeur": "BUREAU_VERITAS",
           "date_entree": "2026-07-27", "prix_entree": "27.28",
           "date_sortie": "2026-07-29", "prix_sortie": "29.2400",
           "motif_sortie": "TP_GAP", "pnl_net_eur": "6884.75",
           "prix_sortie_convention": "28.3712", "pnl_net_convention_eur": "3694.00",
           "regles_pre_trade": "R-301 AURAIT BLOQUE", "explication": "Premier signal reel du systeme."}
    bons += _dire("une ligne sans comptabilite est refusee",
                  any("« comptabilite » ABSENTE" in x
                      for x in fautes_d_ecriture([_bv], TRADE, "journal")), True)
    bons += _dire("une comptabilite mal ecrite est refusee",
                  any("INCONNUE" in x for x in fautes_d_ecriture(
                      [dict(_bv, comptabilite="un jeton")], TRADE, "journal")), True)
    bons += _dire("une case hors contrat est refusee",
                  any("HORS CONTRAT" in x for x in fautes_d_ecriture(
                      [dict(_bv, comptabilite=UN_JETON, bidon="x")], TRADE, "journal")), True)
    bons += _dire("la meme ligne, complete, passe",
                  fautes_d_ecriture([dict(_bv, comptabilite=JETONS_ILLIMITES)], TRADE, "journal"), [])

    # LE TOTAL SE COMPTE, IL NE S'ANNONCE PAS DE MEMOIRE. Premiere version :
    # j'avais ecrit 9 alors que le calibrage porte 8 controles — le calibrage
    # echouait donc en annoncant OK sur chaque ligne. Un garde-fou dont le
    # total est faux denonce ce qui va bien : c'est pire qu'aucun garde-fou.
    # LE TOTAL SE COMPTE, IL NE S'ANNONCE PAS. Deux fois deja il a ete
    # ecrit de memoire et le calibrage denoncait ce qui allait bien.
    # ATTENTION : la ligne qui compte NE DOIT PAS SE COMPTER ELLE-MEME.
    # Premiere version : elle cherchait le texte « bons += _dire » et se
    # trouvait, d'ou un total de 20 pour 19 controles reussis — le calibrage
    # denoncait ce qui allait bien. On coupe le motif en deux morceaux qui ne
    # se rencontrent nulle part ailleurs.
    # LE TOTAL COMPTE CE QUI S'EXECUTE, PAS CE QUI EST ECRIT.
    # Troisieme fois la meme famille en deux jours, et cette fois en sens
    # inverse. Le total lisait les lignes du source : trois d'entre elles
    # vivent dans un bloc conditionnel qui ne s'execute que si les fichiers de
    # cours sont la. Lance ailleurs, le programme rendait 23 reussites, ZERO
    # echec, et le verdict « ne rien construire dessus » — sans une seule
    # ligne fautive a montrer. C'est le pire message possible : celui qui ne
    # dit pas quoi regarder.
    # `_dire` compte desormais lui-meme ses passages ; le total ne peut plus
    # etre ni trop petit ni trop grand.
    total = _dire.appels
    print("\n  %s\n" % ("CALIBRAGE OK." if bons == total
                        else "CALIBRAGE ECHOUE — ne rien construire dessus."))
    return bons == total


# `lire_horizon` vit dans COMMUN depuis le 28-09-2026 : le juge des stratégies lit la même
# colonne, et deux lectures d'une même chose divergent toujours (R-708, défaut 4 de A-491).


def horizons_illisibles(lignes):
    """Rend les identifiants des stratégies dont l horizon n est pas un entier positif.

    ① RÔLE — **Refuser un horizon absent, mal écrit ou nul** avant que le soir
      ne tienne une seule position.
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, sur les stratégies vivantes du
      registre ; et `_calibrage`, qui l éprouve.
    ③ ENTRÉE — `lignes` : des lignes du registre des stratégies, avec `id` et
      `horizon`.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la liste des identifiants refusés, vide si tout
      est lisible.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne : lire l horizon par `lire_horizon`, et
      refuser la ligne s il est illisible ou nul.
    ⑦ UNITÉ — Des SÉANCES de bourse.
    ⑧ POURQUOI — Un horizon illisible n est pas un 20 par défaut. Et un horizon
      à 0 mettrait l échéance sur la séance d achat : la forme exacte du
      défaut 2 (27-09-2026). Le test des chiffres est `isdecimal`, pas
      `isdigit` : « ² » passe `isdigit` et fait planter la conversion
      (relevé par le relecteur du Chat le 27-09-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return [l.get("id", "?") for l in lignes if lire_horizon(l.get("horizon", "")) is None]


def _lire_csv(chemin):
    """Lit un fichier CSV et rend ses lignes.

    ① RÔLE — Seul point de lecture des fichiers de travail : positions ouvertes,
      journal des trades.
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, au début, pour reprendre l état
      laissé la veille.
    ③ ENTRÉE — `chemin` : le chemin d un fichier CSV.
    ④ CONDITIONS D ENTRÉE — Aucune. **Un fichier absent est un cas prévu : c est
      le premier soir.**
    ⑤ SORTIE — UNE valeur : la liste des lignes, chacune un dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① si le fichier n existe pas, rendre la liste vide · ② sinon
      l ouvrir en ignorant le marqueur d encodage en tête · ③ rendre ses lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L encodage tolérant vient du même fait que partout ailleurs :
      **un fichier produit sous Windows porte trois octets invisibles en tête, et
      sans cette lecture la première colonne devient introuvable.**
    ⑨ CE QUI CLOCHE — **Une liste vide veut dire DEUX choses : le fichier n existe
      pas, ou il existe et ne porte que son en-tête.** L appelant ne peut pas les
      distinguer — **c est le même défaut que dans le programme du versement.**
    ⑩ EFFET — Aucun : elle ouvre en lecture.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if not os.path.isfile(chemin):
        return []
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def fautes_d_ecriture(lignes, colonnes, nom):
    """Rend la liste des fautes qui interdisent d'écrire ces lignes sous ces colonnes.

    ① RÔLE — **Refuser, AVANT toute écriture, une ligne qui perdrait une case ou
      dont la comptabilité est vide ou inconnue.** C'est la barrière qui rend
      impossible le défaut 3 : une information jetée sans un mot à l'écriture.
    ② CONTEXTE D'APPEL — `tenir_pour_de_vrai`, deux fois, juste après `tenir` et
      avant d'écrire quoi que ce soit : sur le journal entier (anciennes lignes plus
      clôtures du soir) avec le contrat TRADE, et sur les positions restantes avec
      le contrat POSITION. Et `_calibrage`, qui l'éprouve.
    ③ ENTRÉE — `lignes` : les lignes à écrire, chacune un dictionnaire ·
      `colonnes` : la liste du contrat, lue dans CONTRATS_DES_FICHIERS ·
      `nom` : le nom du fichier en toutes lettres, pour les messages.
    ④ CONDITIONS D'ENTRÉE — `colonnes` doit contenir `comptabilite` : les deux
      contrats appelés la contiennent.
    ⑤ SORTIE — UNE valeur : une liste de phrases, vide si tout peut s'écrire.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne, dans l'ordre : ① nommer chaque case que le
      contrat ne porte pas (elle serait jetée) · ② nommer chaque case du contrat
      absente de la ligne (elle serait écrite vide) · ③ refuser une comptabilité
      qui n'est pas l'une des deux déclarées au contrat.
    ⑦ UNITÉ — Un NOMBRE DE CASES. Aucune grandeur physique.
    ⑧ POURQUOI — Trouvé le 27-09-2026 (défaut 3 de A-491) : le teneur remplissait
      bien la comptabilité de chaque clôture, mais écrivait avec les colonnes du
      journal existant, qui n'avait pas cette colonne ; `extrasaction="ignore"` la
      jetait. La mesure comptait alors chaque vente dans les deux comptabilités :
      Unibail, un seul trade réel à −2 796,25 € (−2,80 %), faisait afficher
      « un jeton : 3 operation(s) · cumul 1292.25 EUR ». Sur un refus, ni le
      journal ni les positions ne sont réécrits : les clôtures se refont à
      l'identique le soir suivant, une fois la faute corrigée. MAIS LES SIGNAUX
      DU SOIR SONT PERDUS, comme à tout arrêt de ce programme : le détecteur
      réécrit son fichier chaque soir (relecteur du Chat, 27-09-2026). Le refus
      ne vise donc que ce qui ne peut arriver que par une main ou un défaut du
      code : une vraie clôture respecte le contrat, et le calibrage le vérifie
      chaque soir avant tout.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun : elle n'écrit rien et n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    fautes = []
    for i, l in enumerate(lignes, 1):
        qui = f"{nom}, ligne {i} ({l.get('valeur', '?')} {l.get('date_sortie') or l.get('date_signal') or ''})"
        for c in sorted(str(k) for k in l if k not in colonnes):
            fautes.append(f"{qui} : case « {c} » HORS CONTRAT — elle serait jetée")
        for c in colonnes:
            if c not in l:
                fautes.append(f"{qui} : case « {c} » ABSENTE — elle serait écrite vide")
        if "comptabilite" in l and l.get("comptabilite") not in COMPTABILITES:
            fautes.append(f"{qui} : comptabilité « {l.get('comptabilite')} » INCONNUE — "
                          f"admises : {', '.join(COMPTABILITES)}")
    return fautes


def _ecrire_csv(chemin, lignes, colonnes):
    """Écrit un fichier CSV, en écrasant ce qui s y trouvait.

    ① RÔLE — Seul point d écriture des fichiers de travail.
    ② CONTEXTE D APPEL — `tenir_pour_de_vrai`, à la fin, pour enregistrer les
      positions ouvertes et le journal des trades.
    ③ ENTRÉE — `chemin` · `lignes` : les lignes à écrire · `colonnes` : les
      colonnes retenues, dans l ordre.
    ④ CONDITIONS D ENTRÉE — **Chaque ligne doit porter au moins les colonnes
      demandées ; celles qu elle porte en plus sont JETÉES.**
    ⑤ SORTIE — Ne rend rien.
      [rend: rien]
    ⑥ TRAITEMENT — ① créer le dossier s il manque · ② ouvrir en écriture, ce qui
      VIDE le fichier · ③ écrire l en-tête · ④ écrire les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les colonnes sont imposées par l appelant pour que l ordre soit
      stable d un soir à l autre : **un fichier dont les colonnes changent d ordre
      ne se compare plus à sa version de la veille.**
    ⑨ CE QUI CLOCHE — **`extrasaction="ignore"` JETTE SILENCIEUSEMENT toute
      colonne absente de la liste.** Une colonne ajoutée en amont disparaîtrait
      sans un mot — **c est le même défaut que dans le programme du versement,
      et il touche ici le journal des trades.** C'est arrivé : la comptabilité
      de chaque clôture était jetée (défaut 3 de A-491, 27-09-2026). Depuis,
      `tenir_pour_de_vrai` passe les colonnes du contrat et appelle
      `fautes_d_ecriture` AVANT d'appeler cette fonction : rien ne lui arrive qui
      serait jeté. La fonction elle-même garde `ignore` — `raise` lèverait APRÈS
      avoir vidé le fichier.
      **Et l écriture n est pas atomique** : le fichier est vidé puis rempli. Une
      interruption entre les deux laisse un journal tronqué.
    ⑩ EFFET — **CRÉE le dossier s il manque** · **ÉCRASE le fichier EN ENTIER.**
    ⑪ TERMINAISON — Rend la main. **Peut lever** si le disque refuse l écriture.
      [sort: non]
    """
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)


def tenir_pour_de_vrai(base):
    """LE CHEMIN REEL — celui que le workflow emprunte chaque soir.

    POURQUOI CETTE FONCTION EXISTE, et c est la faute la plus grave trouvee le
    12-09-2026 : `main()` ne faisait que le CALIBRAGE. Le workflow lancait ce
    programme chaque soir, il se calibrait, et il repartait **sans jamais ouvrir
    ni fermer une position.** Le maillon entre le signal et la position etait
    absent du circuit — et invisible, parce qu aucun signal n etait tombe depuis
    la bascule. C est le defaut que ce programme denonce lui-meme en commentaire :
    « une fonction ecrite, eprouvee par un temoin, et branchee nulle part ».

    ① RÔLE — **LE CHEMIN RÉEL du pas n°6.** Tout ce qui est écrit sur l argent
      simulé passe par elle.
    ② CONTEXTE D APPEL — `main`, sans `--calibrage`. Chaque soir.
    ③ ENTRÉE — `base` : la racine. **Et quatre fichiers** : les signaux du jour,
      les positions ouvertes, le journal des trades, les cours.
    ④ CONDITIONS D ENTRÉE — `programmes/MODULE_POSITIONS.py` et `programmes/JUGE_DES_STRATEGIES.py`
      doivent être trouvables, et `donnees/cac40_strategies.csv` lisible. **Les fichiers de travail peuvent manquer.**
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — ① charger le module, le juge des stratégies, les réglages · ② **CALIBRER, et
      s arrêter si le trade connu ne tombe pas** · ③ lire l état de la veille ·
      ④ tenir la séance · ⑤ **contrôler toutes les lignes à écrire contre les
      contrats du journal et des positions, et s'arrêter en code 1 sans rien
      écrire sur la moindre faute** (depuis le 27-09-2026) · ⑥ réécrire les deux
      fichiers, avec les colonnes des contrats.
    ⑦ UNITÉ — **Montants en euros, seuils en pourcents, horizon en jours de
      bourse.**
    ⑧ POURQUOI — **C est la faute la plus grave trouvée le 12-09-2026 :**
      **`main` ne faisait que le CALIBRAGE. Le programme se calibrait chaque soir
      et repartait sans jamais ouvrir ni fermer une position** — invisible,
      parce qu aucun signal n était tombé depuis la bascule.
    ⑨ CE QUI CLOCHE — **Un refus d'écriture fait perdre les signaux du soir** :
      le détecteur réécrit son fichier chaque soir, et le pas du circuit, qui
      n'est pas « continue-on-error », arrête aussi cockpit, mesure, pilote et
      radar ce soir-là (relecteur du Chat, 27-09-2026) — comme tout autre code 1
      de ce programme. · Le `except ImportError` autour du contrôle des signaux
      est devenu inatteignable : le contrat est désormais importé au chargement.
      · **Les deux fichiers sont réécrits l un après l autre, sans
      rien qui garantisse que les deux aboutissent.** Une interruption entre les
      deux laisserait des positions clôturées absentes du journal, ou l inverse —
      **et la mesure de performance lit les deux.**
    ⑩ EFFET — **RÉÉCRIT les positions ouvertes et le journal des trades EN
      ENTIER**, sauf sur une faute d'écriture, où RIEN n'est écrit · **crée les
      dossiers manquants** · **exécute le code du module et du juge des stratégies.**
    ⑪ TERMINAISON — Rend la main avec un code. **Mais `charger_module_positions`
      et `trouver_module`, appelés en premier, LÈVENT si le module est
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import json
    mod = charger_module_positions(trouver_module(base))
    if not _calibrage(mod, base):
        print("  CALIBRAGE ECHOUE — aucune position n est touchee.")
        return 2

    f_pos = os.path.join(base, "donnees", "claude_positions_ouvertes.csv")
    f_jou = os.path.join(base, "donnees", "claude_journal_trades.csv")
    f_sig = os.path.join(base, "donnees", "signaux_du_jour.json")
    positions = _lire_csv(f_pos)
    journal = _lire_csv(f_jou)
    if not os.path.isfile(f_sig):
        print(f"  CODE 2 — {f_sig} absent : sans signaux, rien a tenir.")
        return 2
    d = json.load(open(f_sig, encoding="utf-8"))
    signaux = d.get("signaux") or []
    seance = d.get("seance")
    if not seance:
        print("  CODE 2 — le fichier des signaux ne porte pas de seance.")
        return 2
    # UNE SEANCE MAL ECRITE NE SE COMPARE PAS. Trouve le 27-09-2026 par le
    # relecteur du Chat : une seance « 04/09/2026 », comparee comme du texte,
    # donnait pour « prochaine seance » le 02-01-2024, et les positions
    # s'ouvraient au prix de janvier 2024, code 0.
    if not _est_date(str(seance)):
        print(f"  CODE 2 — la seance du fichier des signaux, {seance!r}, n est pas "
              "une date AAAA-MM-JJ : rien n est ouvert.")
        return 2

    cours = charger_cours_du_banc(base, *_fichiers_de_cours(base))
    if not cours:
        print("  CODE 2 — aucun cours charge.")
        return 2

    # L ENTREE SE FAIT A L OUVERTURE DE LA SEANCE SUIVANTE, jamais au close.
    # `ouvrir_sur_signaux` recoit donc la prochaine seance, pas celle du signal,
    # COMME DATE PROVISOIRE SEULEMENT. Le soir meme, elle n existe pas encore :
    # `prochaine` vaut alors None, et c est `entrer` qui deduit la date
    # d entree du signal, chaque soir tant que la position attend (defaut
    # trouve le 27-09-2026 : jusque-la, la position attendait pour toujours).
    prochaine = seance_suivante(calendrier(cours), seance)

    # ═══ L ADAPTATEUR, ET C EST LE MAILLON QUI MANQUAIT ═══
    # Trouve le 12-09-2026 : le detecteur emet {valeur, date, cmf, cci, close} ;
    # `ouvrir_sur_signaux` attend {strategie, valeur, date_signal}. **LES DEUX
    # N ONT JAMAIS ETE RELIES.** Le detecteur est ne le 11-09, le workflow appelle
    # le teneur juste apres, et aucun signal n est tombe depuis : un programme qui
    # n a rien a faire et deux programmes qui ne se parlent pas rendent le meme
    # silence. Le jour du premier signal, rien ne se serait ouvert.
    # UNE VALEUR PEUT DECLENCHER DEUX STRATEGIES. L univers de chacune se lit AU
    # REGISTRE, colonne `univers`, en mnemoniques — on ne l invente pas ici.
    strategies = []
    for ligne in _lire_csv(os.path.join(base, "donnees", "cac40_strategies.csv")):
        if "VIVANTE" in (ligne.get("statut") or "") and (ligne.get("univers") or "").strip():
            strategies.append((ligne["id"], {m.strip().upper()
                                             for m in ligne["univers"].split(",") if m.strip()}))
    mnemo = {}
    for ligne in _lire_csv(os.path.join(base, "donnees",
                                        "REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv")):
        nom = (ligne.get("onglet_google") or "").strip().upper()
        code = (ligne.get("mnemonique") or "").strip().upper()
        if nom and code:
            mnemo[nom] = code

    # ═══ LE LECTEUR SE CONFRONTE AU CONTRAT, LUI AUSSI ═══
    # CC1 de Cowork, 13-09-2026 : j avais ecrit « chaque bout se confronte AU
    # CONTRAT, jamais l un a l autre ». **Mesure : un seul bout le faisait.**
    # Il a remis le fichier hors contrat — « date » comme le 12-09 — et QUATRE
    # POSITIONS SE SONT OUVERTES SANS UN MOT, code 0.
    # Le garde-fou d ecriture protege d un detecteur qui regresse. Il ne protege
    # pas d un fichier arrive PAR UN AUTRE CHEMIN : une restauration, un rejeu,
    # un rebase qui ramene la version d hier, une main. **Et ce fichier est
    # commite au depot ENTRE les deux pas du workflow : il existe un intervalle
    # ou il peut changer sans repasser par le detecteur.**
    # LA TOLERANCE `sg.get("date")` DISPARAIT AVEC : ce n est plus au code de
    # decider quel nom est le bon, c est au contrat.
    if signaux:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from CONTRATS_DES_FICHIERS import verifier as _verif_c
            _ec = _verif_c("SIGNAL", list(signaux[0].keys()), "LU")
            if _ec:
                print("  ❌ LE FICHIER DES SIGNAUX NE RESPECTE PAS SON CONTRAT :")
                for _x in _ec:
                    print("     " + _x)
                print("     RIEN N EST OUVERT : un signal hors contrat n est pas un signal.")
                print("     (fichier restaure, rejoue, ou ecrit hors du detecteur)")
                return 1
        except ImportError:
            print("  ⚠️ CONTRATS_DES_FICHIERS introuvable — lecture NON VERIFIEE")

    traduits, sans_mnemo, hors_univers = [], [], []
    for sg in signaux:
        val = (sg.get("valeur") or "").strip().upper()
        code = mnemo.get(val, "")
        pris = False
        for sid, univers in strategies:
            if code and code in univers:
                traduits.append({"strategie": sid, "valeur": sg["valeur"],
                                 "date_signal": sg["date_signal"]})
                pris = True
        if code and not pris:
            hors_univers.append(sg.get("valeur"))
        if not code:
            sans_mnemo.append(sg.get("valeur"))
    # DIRE LAQUELLE DES DEUX FAUTES, JAMAIS LES DEUX D UN COUP.
    # U2 de Cowork, 12-09 : mon message proposait deux causes et laissait choisir —
    # « aucune strategie ne porte cette valeur, OU elle n a pas de mnemonique ».
    # **C est mot pour mot la faute que j avais corrigee ce matin dans le radar,
    # et dont j avais ecrit la regle en commentaire. Huit heures plus tard, la meme
    # construction revient dans un autre programme : une regle apprise dans un
    # fichier ne voyage pas jusqu au suivant.**
    #
    # ET LES DEUX CAS N ONT PAS LA MEME GRAVITE — c est sa U3 :
    #   · HORS UNIVERS = situation NORMALE. Le detecteur calcule sur dix valeurs,
    #     les strategies vivantes n en suivent pas forcement autant. Ce n est pas
    #     une faute : on le DIT et on continue.
    #   · SANS MNEMONIQUE = vraie faute. Le referentiel est incomplet, et la valeur
    #     est invisible a tout le systeme. On s arrete.
    # Sans cette distinction, un signal sur SANOFI — valeur parfaitement connue,
    # simplement hors des univers vivants — arretait TOUT LE CIRCUIT DU SOIR :
    # ni cockpit, ni depot public, ni mesure, ni pilote, ni radar.
    if sans_mnemo:
        print(f"  ❌ {len(sans_mnemo)} valeur(s) SANS MNEMONIQUE au referentiel : "
              + ", ".join(f"« {v} »" for v in sans_mnemo))
        print("     Le referentiel est incomplet : cette valeur est invisible au systeme.")
        print("     RIEN N EST ECRIT — un signal perdu est une position perdue.")
        return 1
    if hors_univers:
        print(f"  ⚠️ {len(hors_univers)} signal(aux) HORS UNIVERS, ignore(s) : "
              + ", ".join(f"« {v} »" for v in hors_univers))
        print("     Aucune strategie vivante ne suit cette valeur. Ce n est PAS une faute :")
        print("     le detecteur calcule plus large que les univers du registre.")
    signaux = traduits

    # L HORIZON SE LIT AU REGISTRE, IL NE S ECRIT PAS EN DUR.
    # Trouve le 12-09 en eprouvant la cloture : `tenir()` et `cloturer()` portent
    # `horizon_seances=20` par defaut, et mon appel laissait ce defaut. Le registre
    # dit 20 pour les deux strategies vivantes — donc c est JUSTE AUJOURD HUI, et
    # faux le jour ou une strategie changera d horizon, sans que rien ne le dise.
    # **C est la famille de la journee : un chiffre dans le code qui double une
    # source de verite.** `reglages_du_registre` le fait deja pour l objectif et le
    # stop ; l horizon suivait le meme chemin et ne le faisait pas.
    # W1 : PLUS DE REPLI MUET. `horizons else 20` faisait revenir par la porte
    # du repli le 20 qu on venait de retirer du code — ET le programme annonçait
    # « horizon lu au registre ». **Affirmer une lecture qui n a pas eu lieu, dans
    # le programme qui calcule le P&L, est le pire endroit du systeme pour une
    # valeur inventee.** Un horizon illisible n est pas un 20, c est un arret.
    lignes_v = [l for l in _lire_csv(os.path.join(base, "donnees", "cac40_strategies.csv"))
                if "VIVANTE" in (l.get("statut") or "")]
    illisibles = horizons_illisibles(lignes_v)
    if not lignes_v:
        print("  ❌ AUCUNE STRATEGIE VIVANTE au registre — rien a tenir.")
        return 1
    if illisibles:
        print(f"  ❌ HORIZON ILLISIBLE pour : {', '.join(illisibles)}")
        print("     Un horizon absent ou mal ecrit n est PAS un 20 par defaut :")
        print("     une cloture au mauvais horizon fausse le P&L de chaque trade.")
        return 1
    for l in lignes_v:
        print(f"  horizon lu au registre · {l['id']} : "
              f"{lire_horizon(l['horizon'])} seances")

    r = tenir(positions, cours, signaux, prochaine, mod, base=base)

    # LES COLONNES VIENNENT DU CONTRAT, JAMAIS DU FICHIER EXISTANT, ET RIEN NE
    # S'ÉCRIT AVANT QUE TOUT SOIT CONTRÔLÉ (défaut 3 de A-491, 27-09-2026). Avant,
    # les colonnes étaient celles de la première ligne du journal : il n'avait pas
    # de comptabilité, et chaque clôture perdait la sienne sans un mot.
    fautes = []
    if r["trades"]:
        fautes += fautes_d_ecriture(journal + r["trades"], TRADE, "journal des trades")
    if positions or r["positions"]:
        fautes += fautes_d_ecriture(r["positions"], POSITION, "positions ouvertes")
    if fautes:
        print(f"  ❌ {len(fautes)} FAUTE(S) D'ÉCRITURE — RIEN N'EST ÉCRIT, ni journal ni positions :")
        for x in fautes:
            print("     " + x)
        print("     Les clôtures du soir se referont à l'identique une fois la faute corrigée ;")
        print("     les SIGNAUX DE CE SOIR, eux, sont PERDUS (le détecteur réécrit son fichier chaque soir).")
        return 1
    if r["trades"]:
        _ecrire_csv(f_jou, journal + r["trades"], TRADE)
    if positions or r["positions"]:
        _ecrire_csv(f_pos, r["positions"], POSITION)

    print(f"  seance {seance} · prochaine {prochaine or 'AUCUNE — pas encore publiee'}")
    print(f"  {len(signaux)} signal(aux) · {len(r['trades'])} cloture(s)"
          f" · {len(r['positions'])} position(s) ouverte(s)")
    for i in r["signaux_ignores"]:
        print(f"  signal ignore : {i}")
    for i in r["incidents"]:
        print(f"  incident : {i}")
    if r["muet"]:
        print(f"  ⚠️ {r['alerte']}")
        return 1
    return 0


def main():
    """Tient les positions du jour, ou calibre seulement.

    ① RÔLE — **LE PAS N°6 DU CIRCUIT DU SOIR**, après la détection. Il clôture ce
      qui doit l être, ouvre ce que les signaux commandent, et enregistre.
    ② CONTEXTE D APPEL — Le circuit du soir, après le détecteur. **Entrée à
      l Open de J+1 : ce programme décide la veille pour le lendemain.**
    ③ ENTRÉE — La ligne de commande : la racine du dépôt, ou `"."` à défaut ·
      `--calibrage` pour ne faire que le calibrage.
    ④ CONDITIONS D ENTRÉE — `programmes/MODULE_POSITIONS.py` doit être trouvable.
    ⑤ SORTIE — UNE valeur : le code de sortie, **rendu et non imposé** —
      c est l appel du bas du fichier qui en fait un code de processus.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la racine · ② **si `--calibrage`, calibrer et
      s arrêter** · ③ sinon, tenir les positions pour de vrai.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Le calibrage seul existe pour qu on puisse vérifier le moteur
      sans toucher aux positions.** C est ce qui rend le programme rejouable sur
      un clone.
    ⑨ CE QUI CLOCHE — **`--calibrage` est cherché dans TOUS les arguments, y
      compris là où une racine est attendue.** Un dossier qui s appellerait ainsi
      changerait le comportement du programme.
    ⑩ EFFET — **Aucun en propre.** Tout ce qui est écrit l est par
      `tenir_pour_de_vrai`, qu elle appelle.
    ⑪ TERMINAISON — **REND LA MAIN, avec un code : 0 si tout va, 1 si le
      calibrage échoue.** **Mais ce qu elle appelle peut ne pas revenir** :
      `charger_module_positions` et `trouver_module` terminent le programme si le
      [sort: non]
    ⑫ DÉFINITIONS —
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les signaux du jour
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    if "--calibrage" in sys.argv:
        print("TENIR LES POSITIONS . %s . CALIBRAGE SEUL" % VERSION)
        return 0 if _calibrage(charger_module_positions(trouver_module(base)), base) else 1
    print("TENIR LES POSITIONS . %s" % VERSION)
    return tenir_pour_de_vrai(base)


def _ancien_main():
    """Ancienne version de `main`, conservée et jamais appelée.

    ① RÔLE — Aucun aujourd hui. **Elle ne tenait que le calibrage, là où `main`
      tient aussi les positions.**
    ② CONTEXTE D APPEL — **Personne ne l appelle.** Le bas du fichier appelle
      `main`.
    ③ ENTRÉE — La ligne de commande, comme `main`.
    ④ CONDITIONS D ENTRÉE — Les mêmes que `main` : `programmes/MODULE_POSITIONS.py` trouvable.
    ⑤ SORTIE — UNE valeur : 0 si le calibrage passe, 1 sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la racine · ② charger le module · ③ calibrer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le commentaire qu elle porte explique pourquoi `base` descend
      jusqu au bout : **sans cela le module était cherché dans le dossier passé
      en argument et le registre dans le répertoire COURANT — deux racines pour
      un seul programme.** Ce fait vaut encore pour `main`.
    ⑨ CE QUI CLOCHE — **C est du CODE MORT, et il porte une explication que
      personne ne lira là où elle sert.** Qui arrive dans ce fichier peut la
      prendre pour la version vivante : les deux fonctions se ressemblent, et
      seule la dernière ligne du fichier dit laquelle tourne.
    ⑩ EFFET — Aucun, puisqu elle n est jamais appelée.
    ⑪ TERMINAISON — Rendrait la main. **Ce qu elle appelle peut terminer le
      programme.**
      [sort: non]
    """
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    print("TENIR LES POSITIONS . %s" % VERSION)
    mod = charger_module_positions(trouver_module(base))
    # `base` DESCEND JUSQU'AU BOUT. Sans cela, le module etait cherche dans le
    # dossier donne en argument et le registre dans le repertoire COURANT :
    # deux racines pour un seul programme. Lance depuis ailleurs, la lecture
    # automatique des reglages ne trouvait rien — et l'on retombait sur le
    # defaut du 03/09, ouvrir zero position. Releve par Cowork le 03/09 19h24.
    return 0 if _calibrage(mod, base) else 1


if __name__ == "__main__":
    sys.exit(main())
