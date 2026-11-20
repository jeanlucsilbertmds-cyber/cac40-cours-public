#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py — Mer 07-10-2026 (Paris)
DÉCIDÉ · outil · Rôle : proposer, pour UNE stratégie, les réglages à essayer.
Quand l'appeler : à la main, quand une stratégie entre dans la recherche de sa meilleure version.

USAGE
    python3 PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py <registre> <ID_FICHE> <voisinage> <essai> <dossier_sortie>
    exemple :
    python3 programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py \
        donnees/cac40_strategies.csv C5E10-OBS-V1 donnees/combinatoires/VOISINAGE.csv E01 donnees/combinatoires

CE QUE CE PROGRAMME EST DANS LA CHAÎNE (action A-541 du BACKLOG)
    La chaîne TROUVER_LA_VERSION_OPTIMALE_DES_STRATEGIES compte cinq fonctions :
    ⓪ CE PROGRAMME — propose les réglages à essayer, que Jean-Luc valide ;
    ① DECLINER_LES_STRATEGIES — croise ces réglages en versions figées ;
    ② jouer — rejoue chaque version sur les cours (juge des stratégies) ;
    ③ TRIER_LES_VARIANTES — écarte celles qui restent sous un seuil ;
    ④ juger — examine à fond les versions retenues. Jean-Luc décide.

① RÔLE — Transformer la fiche d'une stratégie en une liste de réglages à
  essayer, réglage par réglage, pour que Jean-Luc la valide AVANT tout calcul.
  Une stratégie est une idée rendue assez précise pour qu'un programme la joue
  (A-541, complément du 07-10-2026) ; essayer seulement le réglage où elle a été
  trouvée ne dit rien de ses voisins. Ce programme ne calcule aucun gain.
② CONTEXTE D'APPEL — À la main, par le Chat, à la demande de Jean-Luc. Aucune
  tâche automatique ne l'appelle : le déclenchement automatique reste à décider
  par Jean-Luc (A-541). `programmes/EPREUVES_DE_LA_DECLINAISON.py` l'appelle
  pour l'éprouver.
③ ENTRÉE — La ligne de commande, cinq arguments obligatoires :
  `<registre>` : le registre des stratégies, `donnees/cac40_strategies.csv` ;
  `<ID_FICHE>` : l'identifiant d'une ligne de ce registre, par exemple
  `C5E10-OBS-V1` ; `<voisinage>` : le fichier qui dit jusqu'où aller autour de
  chaque réglage (colonnes parametre, pas, de_part_et_d_autre, minimum, maximum,
  unite, raison, et depuis le 11-11-2026 `liste` : quand elle est remplie, ses
  valeurs sont essayées telles quelles, « sans stop » et « aucune » compris) ; `<essai>` : le numéro d'essai, E01 à E99 ;
  `<dossier_sortie>` : le dossier où écrire le tableau.
④ CONDITIONS D'ENTRÉE — Le registre contient la fiche demandée ; si elle y est écrite plusieurs fois, sa DERNIÈRE
  ligne fait foi (décision n°83, depuis le 05-11-2026 ; avant, une fiche double était refusée).
  La fiche porte un objectif (`tp`), un stop (`sl`), une durée (`horizon`) et un
  univers lisibles : chaque code de l'univers doit exister au référentiel des
  valeurs (`REFERENTIEL_VALEURS*.csv`, un seul, dans le dossier du registre) et
  n'y être pas marqué hors univers (exemple réel : ArcelorMittal, MT, coté à
  Amsterdam, écarté par Jean-Luc le 13-09-2026). Objectif et stop sont compris
  entre 0,01 et 50 %. Le pas de voisinage de la durée est un nombre entier. Le
  voisinage porte une ligne pour tp, sl et horizon. L'identifiant ne contient
  que lettres, chiffres, point, tiret ou tiret bas. Le tableau à écrire n'existe
  pas déjà : un numéro d'essai ne sert qu'une fois (A-541, décision de Jean-Luc
  du 07-10-2026 à 17h59).
⑤ SORTIE — Un code de sortie et un fichier. 0 : le tableau
  `VARIABLES_DE_DECLINAISON_<ID_FICHE>_<essai>.csv` est écrit puis relu
  conforme · 1 : une condition d'entrée manque, rien n'est écrit · 2 : arguments
  absents, ce texte est affiché.
⑥ TRAITEMENT — ① vérifier les arguments · ② lire la fiche et le référentiel ·
  ③ lire le voisinage · ④ pour l'objectif, le stop et la durée, entourer la
  valeur de la fiche de ses voisins · ⑤ proposer les ensembles de valeurs :
  l'univers de la fiche, puis chacune de ses valeurs seule s'il en a plusieurs ·
  ⑥ ajouter, marqués NON jouables, les réglages du signal, que `jouer` ne sait
  pas encore faire varier (A-542), puis le moment d'achat et les filtres, avec la
  valeur de la fiche, que le juge ne lit pas encore (A-546 ⑤ ⑥) · ⑦ écrire sans jamais écraser · ⑧ relire et
  vérifier que le fichier dit ce qui a été calculé · ⑨ afficher le nombre de
  versions que DECLINER_LES_STRATEGIES fabriquera.
⑦ UNITÉ — Dans ce tableau, objectif et stop sont en POURCENTS du prix d'entrée,
  toujours positifs (le stop « −2,5 % » s'écrit 2.5) · durée en SÉANCES de
  bourse · univers en MNÉMONIQUES (codes courts : TTE, ENGI…), les codes d'un
  même ensemble séparés par des virgules, les ensembles séparés par des
  points-virgules.
⑧ POURQUOI — Jean-Luc, 07-10-2026 à 18h18 : la fonction qui fabrique la liste
  des réglages à essayer « n'était pas décrite jusqu'à maintenant ». Choisir les
  valeurs à essayer est une DÉCISION : le programme propose, Jean-Luc tranche
  (R-754 : ce qu'un programme peut faire, un programme le fait ; le dialogue sert
  à décider). La règle du voisinage vit dans un fichier, jamais dans le code.
  La durée est lue par `COMMUN.lire_horizon_ou_aucune` (depuis le 11-11-2026 :
  « aucune » est lisible), la lecture commune d'un horizon du dépôt : deux
  implémentations d'une même chose divergent toujours (R-708).
⑨ CE QUI CLOCHE — ① La règle de voisinage n'est pas décidée par Jean-Luc : le
  fichier fourni pour l'essai E01 est une PROPOSITION ; la liste du stop
  (11-11-2026) est la grille choisie par le Chat sur délégation de Jean-Luc du
  19-10-2026 à 20h22 (A-541). ② Les ensembles de
  valeurs se limitent à l'univers de la fiche et à ses valeurs prises une à
  une : les secteurs et les groupes d'A-540 n'existent pas encore en fichier.
  ③ Les réglages du signal (durée du CMF, durée et seuil du CCI) sont listés
  mais ne peuvent pas être joués tant qu'A-542 n'est pas faite. ④ La période de
  la fiche n'est pas déclinée. ⑤ L'objectif et le stop sont lus par une
  lecture propre à ce programme, et non par `pourcent` du juge des stratégies,
  parce que `pourcent` lit « −0,6 % » comme 60 % (mesuré le 07-10-2026 :
  `pourcent('-0.6%')` rend 0.6) — défaut du juge, à consigner au BACKLOG.
⑩ EFFET — Écrit UN fichier nouveau dans `<dossier_sortie>`, créé en mode
  exclusif : s'il apparaît entre le contrôle et l'écriture, rien n'est écrasé.
  Si la relecture montre un fichier abîmé, il est effacé et le programme sort en 1.
  Ne modifie ni le registre, ni le voisinage, ni aucun autre fichier.
⑪ TERMINAISON — SORT DU PROGRAMME avec 0, 1 ou 2. Aucun appel réseau, aucun
  appel qui puisse ne pas revenir.
⑫ DÉFINITIONS —
  le registre des stratégies : `donnees/cac40_strategies.csv`, une ligne par stratégie, avec son état de vie.
  une fiche : une ligne de ce registre.
  un essai : une recherche de meilleure version sur une stratégie, numérotée E01, E02… ; un nouvel essai sur la même stratégie prend le numéro suivant.
  le voisinage : le fichier qui dit, pour chaque réglage, de combien on s'écarte de la valeur de la fiche et combien de fois.
  le référentiel des valeurs : `donnees/REFERENTIEL_VALEURS*.csv`, qui donne pour chaque valeur du CAC 40 son code court (mnémonique).
  jouer : la fonction du juge des stratégies (`programmes/JUGE_DES_STRATEGIES.py`) qui rejoue une stratégie sur les cours.
  le CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une valeur.
  le CCI : l'indice qui mesure de combien le prix s'écarte de sa moyenne récente.
"""
import csv
import glob
import math
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import COMMUN  # noqa: E402  la lecture d'horizon et de tableau vit là (R-708)
import CONTRATS_DES_FICHIERS as CONTRAT  # noqa: E402  la règle « la dernière ligne d'un identifiant fait foi » (n°83)

COLONNES = ["strategie", "essai", "parametre", "valeur_fiche", "valeurs_a_essayer",
            "unite", "jouable", "raison", "valide_par", "prepare_le"]
REGLAGES_DE_SORTIE = (("tp", "pourcents"), ("sl", "pourcents"), ("horizon", "seances"))
REGLAGES_DU_SIGNAL = (
    ("duree_cmf", "durée de calcul du CMF"),
    ("duree_cci", "durée de calcul du CCI"),
    ("seuil_cci", "seuil du CCI sous lequel on achète"),
)
# LE MOMENT D'ACHAT ET LES FILTRES FONT PARTIE DE L'IDENTITÉ D'UNE STRATÉGIE, mais le
# juge ne lit pas ces deux colonnes de la fiche : il achète toujours à l'ouverture du
# lendemain et n'applique aucun filtre (constat écrit dans A-546 ⑤ ⑥ le 10-10-2026).
# Ils figurent au tableau, NON jouables, avec la valeur de la fiche, pour ne pas être
# oubliés (décision de Jean-Luc du 10-10-2026 à 18h29, « Oui »).
REGLAGES_D_ACHAT = (
    ("entree", "moment et prix d'achat après le signal"),
    ("filtres", "conditions à remplir en plus du signal pour acheter"),
)
FORME_ID = re.compile(r"^[A-Za-z0-9_.\-]+$")
FORME_ESSAI = re.compile(r"^E[0-9]{2}$")
FORME_POURCENT = re.compile(r"^[+\-]?[0-9]+([.,][0-9]+)?$")
# LA GRILLE DU VOISINAGE VIT DANS COMMUN.py DEPUIS LE 11-11-2026 (plan V7, bloc 5l ⑥) : `voisins`, `pas_entier` et
# les deux bornes des pourcents y ont été DÉPLACÉS tels quels, pour que le juge des stratégies fabrique ses voisins par
# la même fonction que ce programme (R-708) sans dépendre de lui. Ils restent appelables ici sous leur nom.
from COMMUN import voisins, pas_entier, POURCENT_MINIMUM, POURCENT_MAXIMUM  # noqa: E402,F401


def lire_tableau(chemin):
    """Lit un fichier de tableau par la lecture commune du dépôt, ou lève une erreur claire.

    ① RÔLE — Lire registre, voisinage et référentiel par `COMMUN.lire_csv`, la
      lecture commune (R-708), en transformant une lecture ratée en erreur.
    ② CONTEXTE D'APPEL — `main`, trois fois, puis une fois pour relire le tableau écrit.
    ③ ENTRÉE — `chemin` : un fichier CSV.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la liste des lignes, chacune un dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① appeler `COMMUN.lire_csv` · ② si ce n'est pas une liste,
      lever OSError avec la raison.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `COMMUN.lire_csv` distingue « illisible » de « vide » : un
      fichier illisible ne doit jamais passer pour un tableau sans ligne.
    ⑨ CE QUI CLOCHE — Un fichier qui n'a qu'une ligne d'en-tête rend une liste
      vide : le refus vient alors de l'appelant.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève OSError.
      [sort: non]
    """
    lignes = COMMUN.lire_csv(chemin)
    if not isinstance(lignes, list):
        raise OSError("lecture ratée de %s : %s" % (chemin, getattr(lignes, "raison", lignes)))
    return lignes


def pourcents_de(texte):
    """Lit un pourcentage écrit au registre : « +4.0% », « -2.5% », « 4 » → 4.0, 2.5, 4.0.

    ① RÔLE — Rendre la grandeur d'un objectif ou d'un stop, en pourcents, sans signe.
    ② CONTEXTE D'APPEL — `preparer`, deux fois : objectif et stop.
    ③ ENTRÉE — `texte` : le contenu d'une case, par exemple « -2.5% ».
    ④ CONDITIONS D'ENTRÉE — Aucune : toute chaîne est acceptée.
    ⑤ SORTIE — UNE valeur : le nombre positif lu, en pourcents, ou `None` si la
      case n'est pas un nombre simple (« à renseigner », « 4-5 », « nan », vide).
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les espaces et le « % » final · ② exiger la forme
      « signe facultatif, chiffres, décimales facultatives » · ③ rendre la
      valeur sans signe, ou None.
    ⑦ UNITÉ — Des POURCENTS : 2.5 veut dire 2,5 %.
    ⑧ POURQUOI — Le registre écrit le stop « -2.5% » ; la proposition travaille sur
      sa grandeur. La forme est exigée parce qu'une lecture permissive lisait
      « 4-5 » comme 45 (relevé à la relecture du 07-10-2026).
    ⑨ CE QUI CLOCHE — Le signe est jeté : « -4 » et « +4 » donnent 4.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = (texte or "").replace(" ", "").rstrip("%")
    if not FORME_POURCENT.match(t):
        return None
    return abs(float(t.replace(",", ".")))


def ecrire_nombre(v):
    """Écrit un nombre sans zéros inutiles : 4.0 → « 4 », 2.5 → « 2.5 ».

    ① RÔLE — Rendre le tableau lisible par Jean-Luc et par DECLINER_LES_STRATEGIES.
    ② CONTEXTE D'APPEL — `preparer`, pour chaque valeur écrite.
    ③ ENTRÉE — `v` : un nombre positif, déjà arrondi à quatre décimales.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le texte du nombre.
      [rend: 1]
    ⑥ TRAITEMENT — ① écrire avec quatre décimales · ② retirer les zéros et le
      point final inutiles.
    ⑦ UNITÉ — Celle du nombre.
    ⑧ POURQUOI — « 4.0000 » se lit mal sur un téléphone.
    ⑨ CE QUI CLOCHE — Un nombre plus petit que 0,00005 s'écrit « 0 » : aucun
      réglage du projet n'est aussi petit.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return ("%.4f" % v).rstrip("0").rstrip(".")


def nouvelle_ligne(ident, essai, horodatage, parametre, valeur_fiche, valeurs, unite, jouable, raison):
    """Fabrique une ligne du tableau, case de validation vide.

    ① RÔLE — Donner à chaque ligne la même forme et les mêmes colonnes.
    ② CONTEXTE D'APPEL — `preparer`, une fois par réglage.
    ③ ENTRÉE — `ident` : l'identifiant de la fiche · `essai` : « E01 »… ·
      `horodatage` : l'heure de préparation · `parametre` : le nom du réglage ·
      `valeur_fiche` : sa valeur à la fiche · `valeurs` : ses valeurs à essayer,
      séparées par des points-virgules · `unite` : son unité · `jouable` : « OUI »
      ou « NON » · `raison` : pourquoi ces valeurs.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un dictionnaire portant les colonnes de `COLONNES`.
      [rend: 1]
    ⑥ TRAITEMENT — assembler le dictionnaire, `valide_par` vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La validation appartient à Jean-Luc : le programme laisse la case vide.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return {"strategie": ident, "essai": essai, "parametre": parametre,
            "valeur_fiche": valeur_fiche, "valeurs_a_essayer": valeurs, "unite": unite,
            "jouable": jouable, "raison": raison, "valide_par": "", "prepare_le": horodatage}


def valeur_de_sortie(parametre, texte):
    """Lit une valeur de sortie écrite (fiche ou liste) : un nombre, le MOT de « aucune » / « sans stop », ou None.

    ① RÔLE — LA lecture d'une valeur de l'objectif, du stop ou de la durée dans ce programme, mots compris : la case de
      la fiche et chaque élément de la colonne `liste` du voisinage passent par elle.
    ② CONTEXTE D'APPEL — `preparer`, pour la valeur de la fiche ; `valeurs_de_la_liste`, pour chaque élément.
    ③ ENTRÉE — `parametre` : « tp », « sl » ou « horizon » · `texte` : la case, par exemple « -2.5% », « 12 »,
      « sans stop », « 20j », « aucune ».
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : pour « sl », `COMMUN.MOT_DU_STOP_AUCUN` si le texte est « sans stop » (lu par
      `COMMUN.est_le_mot_du_stop_aucun`) ; pour « horizon », `COMMUN.MOT_DE_L_HORIZON_AUCUNE` si le texte est
      « aucune » (lu par `COMMUN.lire_horizon_ou_aucune`) ; sinon le nombre lu (pourcents par `pourcents_de`, entre
      POURCENT_MINIMUM et POURCENT_MAXIMUM ; séances entières > 0 par `COMMUN.lire_horizon_ou_aucune`, en nombre à
      virgule) ; None si illisible ou hors des bornes.
      [rend: 1]
    ⑥ TRAITEMENT — ① reconnaître le mot du paramètre · ② sinon lire le nombre par la lecture de son unité · ③ borner.
    ⑦ UNITÉ — Pourcents pour tp et sl (2.5 vaut 2,5 %) ; séances pour l'horizon.
    ⑧ POURQUOI — DÉCISION DE JEAN-LUC du 19-10-2026 à 20h22 (A-541) : le stop s'essaie aussi « sans stop » ; la durée
      « aucune » (plan V7, bloc 4 ; A-645) s'écrit par le mot du contrat du lot 0. Les mots se reconnaissent dans
      COMMUN, une fois (R-708) ; un mot n'est jamais un très grand nombre (A-541 ⑤).
    ⑨ CE QUI CLOCHE — « sans stop » n'existe pas pour l'objectif : un tp « sans stop » rend None (refusé).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; ses appels aussi.
      [sort: non]
    """
    if parametre == "sl" and COMMUN.est_le_mot_du_stop_aucun(texte):
        return COMMUN.MOT_DU_STOP_AUCUN
    if parametre == "horizon":
        h = COMMUN.lire_horizon_ou_aucune(texte)
        if h is COMMUN.HORIZON_AUCUNE:
            return COMMUN.MOT_DE_L_HORIZON_AUCUNE
        return None if h is None else float(h)
    v = pourcents_de(texte)
    if v is None or not POURCENT_MINIMUM <= v <= POURCENT_MAXIMUM:
        return None
    return v


def valeurs_de_la_liste(parametre, liste, valeur_fiche):
    """Rend les valeurs à essayer écrites telles quelles dans la colonne `liste` du voisinage, valeur de la fiche comprise.

    ① RÔLE — Permettre une grille IRRÉGULIÈRE (A-541, complément du 19-10-2026 à 21h46, « modification 1 ») : la
      grille du stop 1,5 · 2 · 2,5 · 3 · 3,5 · 4 · 4,5 · 5 · 6 · 7 · 8 · 10 · 12 · 15 % et « sans stop » change de pas,
      ce que `voisins` (un pas régulier) ne sait pas faire.
    ② CONTEXTE D'APPEL — `preparer`, pour chaque réglage de sortie dont la ligne du voisinage porte une `liste`.
    ③ ENTRÉE — `parametre` : « tp », « sl » ou « horizon » · `liste` : le texte de la colonne, valeurs séparées par
      des points-virgules, par exemple « 1.5;2;2.5;3;3.5;4;4.5;5;6;7;8;10;12;15;sans stop » · `valeur_fiche` : ce que
      `valeur_de_sortie` a lu dans la fiche (un nombre ou un mot).
    ④ CONDITIONS D'ENTRÉE — `valeur_fiche` n'est pas None.
    ⑤ SORTIE — UNE valeur : la liste des valeurs ÉCRITES (textes), sans doublon, nombres croissants d'abord, le mot
      (« sans stop », « aucune ») en dernier ; la valeur de la fiche toujours comprise.
      [rend: 1]
    ⑥ TRAITEMENT — ① couper aux points-virgules, ignorer les vides · ② lire chaque élément par `valeur_de_sortie`,
      refuser le premier illisible · ③ ajouter la valeur de la fiche si elle manque (comme `voisins` le fait) ·
      ④ trier : nombres croissants, puis le mot · ⑤ écrire les nombres par `ecrire_nombre`.
    ⑦ UNITÉ — Celle du réglage (pourcents ou séances).
    ⑧ POURQUOI — Proposition du Chat du 19-10-2026 à 21h46, feu vert de Jean-Luc (« 1 Ok, mais tu le fais en
      autoportant ») : « quand elle est remplie, PREPARER prend ces valeurs telles quelles, pour toute stratégie, au
      lieu de compter des pas autour de la fiche […] la valeur de la fiche est ajoutée si elle manque […] quand la
      colonne est vide, rien ne change ». L'ordre est fixé par le programme et non par l'écriture, pour que deux
      écritures d'une même liste donnent les mêmes numéros de version (DECLINER numérote dans l'ordre du tableau).
    ⑨ CE QUI CLOCHE — Les colonnes `pas`, `de_part_et_d_autre`, `minimum`, `maximum` de la ligne ne servent plus quand
      `liste` est remplie : rien ne le signale à qui les lirait. Une valeur de la fiche absente de la liste s'ajoute
      en silence (affichée dans le tableau, que Jean-Luc valide).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError (élément illisible, liste vide).
      [sort: non]
    """
    lues = []
    for brut in liste.split(";"):
        if not brut.strip():
            continue
        x = valeur_de_sortie(parametre, brut)
        if x is None:
            raise ValueError("liste du voisinage de « %s » : élément illisible ou hors des bornes %r" % (parametre, brut.strip()))
        lues.append(x)
    if not lues:
        raise ValueError("liste du voisinage de « %s » vide" % parametre)
    lues.append(valeur_fiche)
    nombres = sorted({round(x, 4) for x in lues if not isinstance(x, str)})
    mots = sorted({x for x in lues if isinstance(x, str)})
    return [ecrire_nombre(x) for x in nombres] + mots


def preparer(fiche, voisinage, essai, horodatage, codes_connus):
    """Fabrique les lignes du tableau des réglages à essayer.

    ① RÔLE — Le cœur du programme : une ligne par réglage, avec ses valeurs à
      essayer, la raison, et une case de validation vide.
    ② CONTEXTE D'APPEL — `main`, une fois. Les épreuves l'appellent aussi.
    ③ ENTRÉE — `fiche` : la ligne du registre · `voisinage` : dictionnaire
      parametre → règle · `essai` : « E01 »… · `horodatage` : texte de l'heure ·
      `codes_connus` : l'ensemble des mnémoniques du référentiel.
    ④ CONDITIONS D'ENTRÉE — Celles du programme (④ de l'en-tête).
    ⑤ SORTIE — DEUX valeurs : la liste des lignes, et la liste des manques. Si les
      manques ne sont pas vides, les lignes ne doivent pas être écrites.
      [rend: 2]
    ⑥ TRAITEMENT — ⓪ si la ligne du voisinage porte une `liste` : prendre ses valeurs telles quelles
      (`valeurs_de_la_liste`, mots « sans stop » et « aucune » compris, depuis le 11-11-2026) ; sinon :
      ① objectif et stop : lire en pourcents, entourer de voisins ·
      ② durée : lire par `COMMUN.lire_horizon_ou_aucune`, entourer de voisins entiers ; une fiche « sans stop » ou
      « aucune » sans liste est refusée (aucun voisin ne se compte autour d'un mot) ·
      ③ univers : refuser un code inconnu ou répété ; proposer l'univers entier,
      puis chaque valeur seule s'il y en a plusieurs · ④ réglages du signal : une
      ligne NON jouable chacun · ⑤ moment d'achat et filtres : une ligne NON
      jouable chacun, avec la valeur écrite dans la fiche.
    ⑦ UNITÉ — Voir l'en-tête.
    ⑧ POURQUOI — Séparer le calcul de l'écriture permet de l'éprouver sans fichier.
    ⑨ CE QUI CLOCHE — Les réglages du signal sont listés sans leur valeur de fiche :
      le registre ne les porte qu'en texte libre dans `indicateurs`. Le moment
      d'achat et les filtres sont recopiés tels quels, en texte libre, tant que
      le contrat des fichiers ne leur donne pas de forme (A-546 ⑤ ⑥).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError sur une règle de voisinage invalide.
      [sort: non]
    """
    ident = fiche.get("id", "")
    lignes, manques = [], []
    for p, unite in REGLAGES_DE_SORTIE:
        # UNE SEULE LECTURE DE LA VALEUR DE LA FICHE, MOTS COMPRIS (« sans stop », « aucune » : A-541, A-645, mission
        # VENTE du 11-11-2026) : `valeur_de_sortie`. Avant, l'horizon passait par `lire_horizon`, qui refuse « aucune ».
        v = valeur_de_sortie(p, fiche.get(p))
        if v is None:
            manques.append("la fiche ne porte pas de valeur lisible pour « %s » : %r" % (p, fiche.get(p)))
            continue
        if p not in voisinage:
            manques.append("le fichier de voisinage n'a pas de ligne pour « %s »" % p)
            continue
        # LA LISTE ÉCRITE TELLE QUELLE (A-541, modification 1 du 19-10-2026) : quand elle est remplie, elle remplace
        # le pas régulier ; vide ou absente (fichiers d'avant le 11-11-2026), rien ne change.
        liste = (voisinage[p].get("liste") or "").strip()
        if liste:
            try:
                ecrites = valeurs_de_la_liste(p, liste, v)
            except ValueError as e:
                manques.append(str(e))
                continue
            lignes.append(nouvelle_ligne(ident, essai, horodatage, p, v if isinstance(v, str) else ecrire_nombre(v),
                                         ";".join(ecrites), unite, "OUI", voisinage[p].get("raison", "")))
            continue
        if isinstance(v, str):
            manques.append("la fiche porte « %s » pour « %s » et la ligne du voisinage n'a pas de liste : aucun voisin ne "
                           "se compte autour d'un mot" % (v, p))
            continue
        if p == "horizon" and not pas_entier(voisinage[p].get("pas")):
            manques.append("le pas de voisinage de l'horizon doit être un nombre entier de séances : %r" % voisinage[p].get("pas"))
            continue
        vals = voisins(v, voisinage[p])
        if p == "horizon":
            vals = [x for x in vals if x >= 1]
        else:
            vals = [x for x in vals if POURCENT_MINIMUM <= x <= POURCENT_MAXIMUM]
        lignes.append(nouvelle_ligne(ident, essai, horodatage, p, ecrire_nombre(v),
                                     ";".join(ecrire_nombre(x) for x in vals),
                                     unite, "OUI", voisinage[p].get("raison", "")))
    brut = fiche.get("univers") or ""
    codes = [m.strip().upper() for m in brut.split(",") if m.strip()]
    inconnus = [c for c in codes if c not in codes_connus]   # codes_connus exclut les valeurs hors univers
    if not codes or inconnus:
        manques.append("l'univers de la fiche n'est pas une liste de codes du référentiel : %r" % brut)
    elif len(codes) != len(set(codes)):
        manques.append("l'univers de la fiche répète un code : %r" % brut)
    else:
        ensembles = [",".join(codes)] + (codes if len(codes) > 1 else [])
        lignes.append(nouvelle_ligne(ident, essai, horodatage, "univers", ",".join(codes), ";".join(ensembles),
                                     "mnemoniques", "OUI",
                                     "l'univers entier de la fiche, puis chacune de ses valeurs seule ; "
                                     "secteurs et groupes d'A-540 à ajouter quand ils existeront en fichier"))
    for p, libelle in REGLAGES_DU_SIGNAL:
        lignes.append(nouvelle_ligne(ident, essai, horodatage, p, "", "", "", "NON",
                                     "NON JOUABLE aujourd'hui : %s — jouer ne sait pas faire varier le signal (A-542)" % libelle))
    for p, libelle in REGLAGES_D_ACHAT:
        lignes.append(nouvelle_ligne(ident, essai, horodatage, p, (fiche.get(p) or "").strip(), "", "", "NON",
                                     "NON JOUABLE aujourd'hui : %s — le juge ne lit pas cette colonne de la fiche ;"
                                     " toutes les versions gardent celle de la fiche (A-546 ⑤ ⑥)" % libelle))
    return lignes, manques


def nombre_de_versions(lignes):
    """Compte les versions que DECLINER_LES_STRATEGIES fabriquera à partir de ces lignes.

    ① RÔLE — Annoncer à Jean-Luc, avant validation, la taille de ce qu'il valide.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves l'appellent aussi.
    ③ ENTRÉE — `lignes` : les lignes du tableau.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le produit du nombre de valeurs des lignes jouables.
      [rend: 1]
    ⑥ TRAITEMENT — multiplier, ligne jouable par ligne jouable.
    ⑦ UNITÉ — Un compte de versions.
    ⑧ POURQUOI — Plus on essaie de versions, plus l'une gagne par chance : le
      nombre doit être vu avant de valider.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    total = 1
    for l in lignes:
        if l["jouable"] == "OUI":
            total *= len(l["valeurs_a_essayer"].split(";"))
    return total


def main(argv):
    """Enchaîne lecture, proposition, écriture et relecture.

    ① RÔLE — Le point d'entrée du programme.
    ② CONTEXTE D'APPEL — Le lancement en ligne de commande ; les épreuves l'appellent aussi.
    ③ ENTRÉE — `argv` : les cinq arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier les arguments et leur forme · ② lire la fiche,
      sa DERNIÈRE ligne par `fiches_des_lignes` du contrat (n°83, depuis le
      05-11-2026 ; avant, une fiche double était refusée), refuser si absente ·
      ③ lire le référentiel, refuser s'il n'y en a
      pas exactement un · ④ lire le voisinage · ⑤ préparer · ⑥ refuser au moindre
      manque · ⑦ écrire en mode exclusif · ⑧ relire et comparer · ⑨ afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La relecture prouve que le fichier écrit dit ce qui a été calculé.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit un fichier nouveau ; l'efface si sa relecture échoue.
    ⑪ TERMINAISON — Rend la main avec un code ; c'est le bloc final qui sort.
      [sort: non]
    """
    if len(argv) != 5:
        print(__doc__)
        return 2
    registre, ident, f_vois, essai, dossier = argv
    if not FORME_ESSAI.match(essai):
        print("REFUS : le numéro d'essai doit avoir la forme E01 à E99 — reçu %r" % essai)
        return 1
    if not FORME_ID.match(ident):
        print("REFUS : identifiant de fiche de forme inattendue : %r" % ident)
        return 1
    refs = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(registre)), "REFERENTIEL_VALEURS*.csv")))
    if len(refs) != 1:
        print("REFUS : il faut exactement un référentiel des valeurs à côté du registre — trouvé %d" % len(refs))
        return 1
    try:
        # LA DERNIÈRE LIGNE DE L'IDENTIFIANT FAIT FOI (décision de Jean-Luc n°83 du 01-11-2026 à 12h33, « Les
        # précédentes restent comme historique ») : la règle vit au contrat. Avant le 05-11-2026, une fiche écrite deux
        # fois était refusée ici.
        fiche = CONTRAT.fiches_des_lignes(lire_tableau(registre)).get(ident)
        regles = lire_tableau(f_vois)
        codes_connus = {(l.get("mnemonique") or "").strip().upper() for l in lire_tableau(refs[0])
                        if not (l.get("hors_univers") or "").strip()} - {""}
    except OSError as e:
        print("REFUS : %s" % e)
        return 1
    if fiche is None:
        print("REFUS : la fiche %s est absente du registre" % ident)
        return 1
    voisinage = {r["parametre"]: r for r in regles}
    heure = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %Hh%M Paris")
    try:
        lignes, manques = preparer(fiche, voisinage, essai, heure, codes_connus)
    except ValueError as e:
        print("REFUS : %s" % e)
        return 1
    if manques:
        print("REFUS — rien n'est écrit :")
        for m in manques:
            print("  · " + m)
        return 1
    sortie = os.path.join(dossier, "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (ident, essai))
    os.makedirs(dossier, exist_ok=True)
    try:
        with open(sortie, "x", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLONNES)
            w.writeheader()
            w.writerows(lignes)
    except FileExistsError:
        print("REFUS : %s existe déjà — un numéro d'essai ne sert qu'une fois" % sortie)
        return 1
    if lire_tableau(sortie) != lignes:
        os.remove(sortie)
        print("ÉCHEC : le fichier relu ne disait pas ce qui a été calculé — il est effacé : %s" % sortie)
        return 1
    print("ÉCRIT : %s" % sortie)
    for l in lignes:
        print("  %-9s fiche=%-28s essayer=%s" % (l["parametre"], " ".join(l["valeur_fiche"].split())[:28],
                                                  l["valeurs_a_essayer"] or "— NON JOUABLE (%s)" % ("A-546" if l["parametre"] in dict(REGLAGES_D_ACHAT) else "A-542")))
    print("VERSIONS QUE DECLINER_LES_STRATEGIES FABRIQUERA : %d" % nombre_de_versions(lignes))
    print("À VALIDER PAR JEAN-LUC : remplir la colonne valide_par de chaque ligne jouable.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
