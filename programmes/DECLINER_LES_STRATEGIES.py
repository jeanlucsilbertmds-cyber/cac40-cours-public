#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DECLINER_LES_STRATEGIES.py — Mer 07-10-2026 (Paris)
DÉCIDÉ · outil · Rôle : fabriquer toutes les versions figées d'une stratégie à partir des réglages validés.
Quand l'appeler : à la main, après que Jean-Luc a validé le tableau VARIABLES_DE_DECLINAISON_<STRATÉGIE>_<ESSAI>.

USAGE
    python3 DECLINER_LES_STRATEGIES.py <registre> <tableau_des_variables> <dossier_sortie>
    exemple :
    python3 programmes/DECLINER_LES_STRATEGIES.py donnees/cac40_strategies.csv \
        donnees/combinatoires/VARIABLES_DE_DECLINAISON_C5E10-OBS-V1_E01.csv donnees/combinatoires

CE QUE CE PROGRAMME EST DANS LA CHAÎNE (action A-541 du BACKLOG)
    ⓪ PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES propose les réglages ; Jean-Luc valide ;
    ① CE PROGRAMME croise ces réglages en versions figées ; ② jouer les rejoue ;
    ③ TRIER_LES_VARIANTES écarte les plus faibles ; ④ juger examine le reste ; Jean-Luc décide.

① RÔLE — Transformer un ensemble de possibilités (pour chaque réglage, plusieurs
  valeurs à essayer) en une liste de versions entièrement figées, une par ligne,
  chaque réglage n'ayant plus qu'une valeur. Chaque version reçoit un identifiant
  unique : stratégie, essai, numéro — par exemple `C5E10-OBS-V1-E01-0003`
  (décision de Jean-Luc du 07-10-2026 à 17h59). Ce programme ne calcule aucun gain.
  COMMENT UNE VERSION SE JOUE ENSUITE : une version ne porte que les réglages qui
  varient. Pour la jouer, on prend la fiche d'origine au registre des stratégies
  (colonne `strategie` = son identifiant) et on y remplace les cases `tp`, `sl`,
  `horizon` et `univers` par celles de la version ; le reste de la fiche
  (indicateurs, période) est inchangé. La fiche ne nomme pas son programme de
  signal : tant qu'A-542 n'est pas faite, il faut y poser
  `_fonction_signal = signaux_c5etendu10`, comme le fait `main` du juge des
  stratégies, sans quoi `jouer` s'arrête sur « le module de signal n'expose pas
  'signaux' » (relevé à la relecture du 07-10-2026). C'est le travail de l'étape ②,
  faite depuis le 08-10-2026 par `programmes/JOUER_LES_VERSIONS.py`.
  Mesuré le 07-10-2026, deux fois et par deux chemins (le relecteur en appelant
  `jouer`, le Chat en lançant `python3 programmes/JUGE_DES_STRATEGIES.py .` sur
  une copie du dépôt dont le registre ne portait que la version fusionnée) : la
  version C5E10-OBS-V1-E01-0562, identique à la fiche, rend 100 opérations,
  61,0 % de réussite et +125 842,31 €, exactement comme la fiche d'origine.
  Le 08-10-2026, la grille élargie par Jean-Luc porte le numéro de cette
  version à C5E10-OBS-V1-E01-0914, avec le même résultat.
② CONTEXTE D'APPEL — À la main, par le Chat, après la validation de Jean-Luc.
  Aucune tâche automatique ne l'appelle. `programmes/EPREUVES_DE_LA_DECLINAISON.py`
  l'appelle pour l'éprouver.
③ ENTRÉE — La ligne de commande, trois arguments obligatoires :
  `<registre>` : le registre des stratégies, pour confronter le tableau à la
  fiche d'origine et au référentiel des valeurs rangé à côté ;
  `<tableau_des_variables>` : un fichier écrit par
  PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES, puis validé ;
  `<dossier_sortie>` : le dossier où écrire la combinatoire.
④ CONDITIONS D'ENTRÉE — Toutes les lignes portent la même stratégie (lettres,
  chiffres, point, tiret, tiret bas) et le même essai (E01 à E99). Chaque
  paramètre apparaît une fois et appartient à la liste connue. `tp`, `sl`,
  `horizon` et `univers` sont présents et JOUABLES ; les réglages du signal sont
  NON jouables tant qu'A-542 n'est pas faite ; le moment d'achat (`entree`) et
  les filtres (`filtres`), s'ils figurent au tableau, sont NON jouables tant
  qu'A-546 ⑤ ⑥ n'est pas faite, et portent exactement la valeur du registre. Une
  ligne NON ne porte aucune valeur à essayer. La colonne `jouable` vaut
  exactement « OUI » ou « NON ». Chaque ligne jouable porte un nom dans
  `valide_par` écrit exactement « Jean-Luc le JJ-MM-AAAA » (exemple : « Jean-Luc
  le 07-10-2026 ») : c'est lui seul qui valide, et toute autre mention — « à
  valider », « Jean-Luc : NON » — est refusée. Chaque
  valeur est lisible, sans doublon une fois normalisée ; objectif et stop entre 0
  et 50 % ; durée entière. La fiche existe une seule fois au registre, et la
  colonne `valeur_fiche` dit la même chose qu'elle. Chaque ensemble de valeurs
  ne contient que des codes de l'univers de la fiche, connus du référentiel et
  non marqués hors univers. La valeur de la fiche figure parmi les valeurs à
  essayer. Le fichier de sortie n'existe pas déjà.
⑤ SORTIE — Un code de sortie et un fichier. 0 : la combinatoire
  `COMBINATOIRE_<STRATÉGIE>_<ESSAI>.csv` est écrite puis relue conforme ·
  1 : une condition manque, rien n'est écrit (un fichier dont la relecture
  échoue est effacé) · 2 : arguments absents.
⑥ TRAITEMENT — ① lire le tableau · ② vérifier tout ce que dit ④ · ③ normaliser
  les valeurs · ④ croiser · ⑤ numéroter · ⑥ marquer la version identique à la
  fiche · ⑦ écrire en mode exclusif · ⑧ relire : mêmes lignes, identifiants uniques.
⑦ UNITÉ — DANS LA COMBINAISON ÉCRITE, objectif et stop sont des FRACTIONS du
  prix d'entrée (4 % s'écrit 0.04, un stop de 2,5 % s'écrit 0.025) : c'est la
  seule écriture que `pourcent` du juge des stratégies lit sans erreur pour
  toutes les valeurs, y compris sous 1 % · durée en SÉANCES · univers en
  MNÉMONIQUES séparés par des virgules, comme au registre · le nombre de
  versions est un compte.
⑧ POURQUOI — Jean-Luc, 04-10-2026 à 17h45 : générer et vérifier « c'est deux
  choses différentes ». Ce programme ne fait que générer. Le nombre total de
  versions voyage avec chaque ligne, parce que le juge doit savoir combien de
  versions ont été essayées : plus on en essaie, plus l'une gagne par chance.
⑨ CE QUI CLOCHE — ① Le nombre de versions croît vite : mesuré le 07-10-2026 sur
  C5E10-OBS-V1, 5 objectifs × 5 stops × 4 durées × 11 ensembles de valeurs font
  1 100 versions ; le 08-10-2026, grille élargie par Jean-Luc, 7 × 7 × 5 × 11
  font 2 695 versions ; aucune limite n'est posée. ② Le compte total d'une stratégie,
  tous essais réunis, n'est pas tenu ici : c'est l'action A-226, non faite.
  ③ Le programme exige la forme « Jean-Luc le JJ-MM-AAAA », mais ne peut pas
  savoir qui l'a réellement écrite.
⑩ EFFET — Écrit UN fichier nouveau dans `<dossier_sortie>`, créé en mode
  exclusif, effacé si sa relecture échoue. Ne modifie rien d'autre.
⑪ TERMINAISON — SORT DU PROGRAMME avec 0, 1 ou 2. Aucun appel qui puisse ne pas revenir.
⑫ DÉFINITIONS —
  une version : une stratégie dont chaque réglage a une seule valeur, prête à être jouée.
  la combinatoire : la liste de toutes les versions d'une stratégie pour un essai.
  un essai : une recherche de meilleure version sur une stratégie, numérotée E01, E02….
  jouer : la fonction du juge des stratégies (`programmes/JUGE_DES_STRATEGIES.py`) qui rejoue une stratégie sur les cours.
  le registre des stratégies : `donnees/cac40_strategies.csv`, une ligne par stratégie.
"""
import csv
import glob
import itertools
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import COMMUN  # noqa: E402  la lecture de tableau et d'horizon vit là (R-708)
import PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES as PREPARER  # noqa: E402  lecture des pourcents et bornes (R-708)

OBLIGATOIRES = ("tp", "sl", "horizon", "univers")
# Les réglages non jouables viennent de PREPARER, qui les écrit : une seule liste (R-708).
DU_SIGNAL = tuple(p for p, _ in PREPARER.REGLAGES_DU_SIGNAL)
D_ACHAT = tuple(p for p, _ in PREPARER.REGLAGES_D_ACHAT)
VALIDATION = re.compile(r"^Jean-Luc le [0-9]{2}-[0-9]{2}-[0-9]{4}$")
FORME_ID = re.compile(r"^[A-Za-z0-9_.\-]+$")
FORME_ESSAI = re.compile(r"^E[0-9]{2}$")
FORME_NOMBRE = re.compile(r"^[0-9]+(\.[0-9]+)?$")
FORME_CODE = re.compile(r"^[A-Z0-9]+$")


def lire_tableau(chemin):
    """Lit un fichier de tableau par la lecture commune du dépôt, ou lève une erreur claire.

    ① RÔLE — Lire le tableau d'entrée et relire la sortie par `COMMUN.lire_csv` (R-708).
    ② CONTEXTE D'APPEL — `main`, deux fois.
    ③ ENTRÉE — `chemin` : un fichier CSV.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la liste des lignes.
      [rend: 1]
    ⑥ TRAITEMENT — ① appeler `COMMUN.lire_csv` · ② si ce n'est pas une liste, lever OSError.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un fichier illisible ne doit jamais passer pour un tableau vide.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève OSError.
      [sort: non]
    """
    lignes = COMMUN.lire_csv(chemin)
    if not isinstance(lignes, list):
        raise OSError("lecture ratée de %s : %s" % (chemin, getattr(lignes, "raison", lignes)))
    return lignes


def normaliser(parametre, texte):
    """Rend la forme unique d'une valeur à essayer, ou None si elle est illisible.

    ① RÔLE — Faire que « 2 », « 2.0 » et « 2 » avec espace soient reconnus comme
      la même valeur, et écrire chaque valeur sous la forme que `jouer` lit.
    ② CONTEXTE D'APPEL — `verifier` et `decliner`, pour chaque valeur.
    ③ ENTRÉE — `parametre` : tp, sl, horizon ou univers · `texte` : une valeur du tableau.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — DEUX valeurs quand la valeur est lisible : la clé de comparaison et
      le texte à écrire ; UNE seule, None, quand elle est illisible.
      [rend: 1 ou 2]
    ⑥ TRAITEMENT — tp et sl : nombre de 0,01 à 50 en pourcents → fraction écrite
      à six décimales au plus · horizon : entier ≥ 1 · univers : codes en majuscules,
      séparés par des virgules, sans doublon dans l'ensemble ; la clé de comparaison
      est la liste TRIÉE des codes, pour que « ENGI,TTE » et « TTE,ENGI » soient le
      même ensemble.
    ⑦ UNITÉ — Entrée en pourcents ; sortie en fraction pour tp et sl.
    ⑧ POURQUOI — Un doublon masqué par un espace ou un « .0 » fabriquait des
      versions identiques sous deux numéros (relevé à la relecture du 07-10-2026).
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = (texte or "").strip()
    if parametre in ("tp", "sl"):
        if not FORME_NOMBRE.match(t) or not PREPARER.POURCENT_MINIMUM <= float(t) <= PREPARER.POURCENT_MAXIMUM:
            return None
        cle = round(float(t), 6)
        return cle, ("%.6f" % (cle / 100)).rstrip("0").rstrip(".")
    if parametre == "horizon":
        if not FORME_NOMBRE.match(t) or float(t) != int(float(t)) or int(float(t)) < 1:
            return None
        return int(float(t)), str(int(float(t)))
    if parametre == "univers":
        codes = [c.strip().upper() for c in t.split(",") if c.strip()]
        if not codes or len(codes) != len(set(codes)) or not all(FORME_CODE.match(c) for c in codes):
            return None
        return tuple(sorted(codes)), ",".join(codes)
    return None


def verifier(lignes, fiche, codes_connus):
    """Dit ce qui empêche de décliner un tableau de variables.

    ① RÔLE — Refuser AVANT tout croisement ce qui n'a pas été validé ou qui est mal formé.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves l'appellent aussi.
    ③ ENTRÉE — `lignes` : les lignes du tableau des variables · `fiche` : la
      ligne du registre que désigne la colonne `strategie`, ou None si elle est
      absente ou double · `codes_connus` : les mnémoniques du référentiel, hors
      valeurs marquées hors univers.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la liste des motifs de refus, vide si tout va bien.
      [rend: 1]
    ⑥ TRAITEMENT — Chaque condition de ④ de l'en-tête, dans l'ordre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une version fabriquée à partir d'un tableau non validé serait
      jouée sans que Jean-Luc ait choisi ce qu'on essaie.
    ⑨ CE QUI CLOCHE — Le nom écrit dans `valide_par` n'est pas authentifié.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if not lignes:
        return ["le tableau est vide"]
    motifs = []
    strategies = {l.get("strategie") for l in lignes}
    essais = {l.get("essai") for l in lignes}
    if len(strategies) != 1 or not FORME_ID.match(next(iter(strategies)) or ""):
        motifs.append("une seule stratégie, de forme simple, est attendue : %r" % sorted(map(str, strategies)))
    if len(essais) != 1 or not FORME_ESSAI.match(next(iter(essais)) or ""):
        motifs.append("un seul numéro d'essai, de forme E01 à E99, est attendu : %r" % sorted(map(str, essais)))
    params = [l.get("parametre") for l in lignes]
    if len(params) != len(set(params)):
        motifs.append("un paramètre apparaît deux fois")
    for p in params:
        if p not in OBLIGATOIRES + DU_SIGNAL + D_ACHAT:
            motifs.append("paramètre inconnu : %r" % p)
    for l in lignes:
        p, j = l.get("parametre"), l.get("jouable")
        if j not in ("OUI", "NON"):
            motifs.append("ligne « %s » : jouable doit valoir OUI ou NON, pas %r" % (p, j))
        elif p in OBLIGATOIRES and j != "OUI":
            motifs.append("ligne « %s » : ce réglage doit être jouable" % p)
        elif p in DU_SIGNAL and j != "NON":
            motifs.append("ligne « %s » : jouer ne sait pas encore faire varier le signal (A-542)" % p)
        elif p in D_ACHAT and j != "NON":
            motifs.append("ligne « %s » : le juge ne lit pas encore le moment d'achat ni les filtres (A-546 ⑤ ⑥)" % p)
    for l in lignes:
        # UNE LIGNE NON NE PORTE AUCUNE VALEUR À ESSAYER : sinon le tableau laisserait
        # croire qu'elles sont essayées, alors qu'aucune ne l'est (relecture du 10-10-2026, D2).
        if l.get("jouable") == "NON" and (l.get("valeurs_a_essayer") or "").strip():
            motifs.append("ligne « %s » : NON jouable, elle ne peut pas porter de valeurs à essayer : %r"
                          % (l.get("parametre"), l.get("valeurs_a_essayer")))
        # LE MOMENT D'ACHAT ET LES FILTRES AFFICHÉS DOIVENT ÊTRE CEUX DU REGISTRE : Jean-Luc
        # validerait sinon un tableau qui montre une autre entrée que celle qui sera jouée
        # (relecture du 10-10-2026, D1).
        if l.get("parametre") in D_ACHAT and fiche is not None and \
                (l.get("valeur_fiche") or "").strip() != (fiche.get(l.get("parametre")) or "").strip():
            motifs.append("ligne « %s » : valeur_fiche %r ne dit pas ce que dit le registre (%r)"
                          % (l.get("parametre"), l.get("valeur_fiche"), fiche.get(l.get("parametre"))))
    for p in OBLIGATOIRES:
        if p not in params:
            motifs.append("réglage obligatoire absent : %s" % p)
    for l in lignes:
        p = l.get("parametre")
        if l.get("jouable") != "OUI" or p not in OBLIGATOIRES:
            continue
        if not validation_valable(l):
            motifs.append("ligne « %s » non validée (colonne valide_par : « Jean-Luc le JJ-MM-AAAA », date réelle, pas avant la préparation)" % p)
        brutes = [v for v in (l.get("valeurs_a_essayer") or "").split(";") if v.strip()]
        lues = [normaliser(p, v) for v in brutes]
        if not brutes:
            motifs.append("ligne « %s » sans valeur à essayer" % p)
        if any(x is None for x in lues):
            motifs.append("ligne « %s » : valeur illisible dans %r" % (p, l.get("valeurs_a_essayer")))
            continue
        cles = [x[0] for x in lues]
        if len(cles) != len(set(cles)):
            motifs.append("ligne « %s » : une valeur apparaît deux fois" % p)
        f = normaliser(p, l.get("valeur_fiche"))
        if f is None or f[0] not in cles:
            motifs.append("ligne « %s » : la valeur de la fiche %r manque parmi les valeurs à essayer" % (p, l.get("valeur_fiche")))
        if fiche is not None and f is not None and f[0] != valeur_au_registre(p, fiche):
            motifs.append("ligne « %s » : valeur_fiche %r ne dit pas ce que dit le registre" % (p, l.get("valeur_fiche")))
        if p == "univers" and fiche is not None:
            permis = set(valeur_au_registre("univers", fiche) or ()) & codes_connus
            for x in lues:
                if x is not None and not set(x[0]) <= permis:
                    motifs.append("ligne « univers » : codes hors de l'univers de la fiche ou du référentiel : %s"
                                  % ",".join(sorted(set(x[0]) - permis)))
    if fiche is None:
        motifs.append("la stratégie du tableau est absente du registre, ou y figure plusieurs fois")
    return motifs


def validation_valable(ligne):
    """Dit si la case `valide_par` d'une ligne porte une validation de Jean-Luc recevable.

    ① RÔLE — N'accepter comme validation qu'une mention datée, réelle et postérieure à la préparation.
    ② CONTEXTE D'APPEL — `verifier`, une fois par ligne jouable.
    ③ ENTRÉE — `ligne` : une ligne du tableau, avec `valide_par` et `prepare_le`.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — ① exiger la forme « Jean-Luc le JJ-MM-AAAA », espaces de bord
      retirés · ② exiger une date qui existe au calendrier · ③ exiger qu'elle ne
      soit pas antérieure au jour de `prepare_le` (forme « AAAA-MM-JJ … »).
    ⑦ UNITÉ — Des jours.
    ⑧ POURQUOI — Relecture du 07-10-2026 : « Jean-Luc le 99-99-0000 » passait. On
      ne valide pas un tableau avant qu'il existe.
    ⑨ CE QUI CLOCHE — Une date future est acceptée.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    texte = (ligne.get("valide_par") or "").strip()
    if not VALIDATION.match(texte):
        return False
    try:
        jour = datetime.strptime(texte[-10:], "%d-%m-%Y").date()
        prepare = datetime.strptime((ligne.get("prepare_le") or "")[:10], "%Y-%m-%d").date()
    except ValueError:
        return False
    return jour >= prepare


def valeur_au_registre(parametre, fiche):
    """Rend la valeur d'un réglage telle que la fiche du registre la porte, sous la clé de comparaison de `normaliser`.

    ① RÔLE — Confronter la colonne `valeur_fiche` du tableau à la fiche elle-même.
    ② CONTEXTE D'APPEL — `verifier`, une ou deux fois par réglage.
    ③ ENTRÉE — `parametre` : tp, sl, horizon ou univers · `fiche` : la ligne du registre.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un nombre en pourcents (tp, sl), un entier (horizon), un
      tuple TRIÉ de codes (univers), ou None si la fiche est illisible.
      [rend: 1]
    ⑥ TRAITEMENT — tp et sl par `PREPARER.pourcents_de` ; horizon par
      `COMMUN.lire_horizon` ; univers en majuscules, découpé aux virgules.
    ⑦ UNITÉ — Pourcents, séances, mnémoniques.
    ⑧ POURQUOI — Un tableau retouché à la main ne doit pas pouvoir prétendre que la
      fiche dit autre chose que ce qu'elle dit (relecture du 07-10-2026 : une
      « version de la fiche » à 3 % alors que la fiche dit 4 %).
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if parametre in ("tp", "sl"):
        v = PREPARER.pourcents_de(fiche.get(parametre))
        return None if v is None else round(v, 6)
    if parametre == "horizon":
        return COMMUN.lire_horizon(fiche.get(parametre))
    if parametre == "univers":
        return tuple(sorted(c.strip().upper() for c in (fiche.get("univers") or "").split(",") if c.strip()))
    return None


def decliner(lignes):
    """Croise les valeurs des réglages en versions figées.

    ① RÔLE — Le cœur du programme : toutes les combinaisons, chacune numérotée.
    ② CONTEXTE D'APPEL — `main`, une fois, après `verifier` ; les épreuves aussi.
    ③ ENTRÉE — `lignes` : un tableau qui a passé `verifier`.
    ④ CONDITIONS D'ENTRÉE — `verifier(lignes)` est vide.
    ⑤ SORTIE — DEUX valeurs : la liste des colonnes, et la liste des versions
      (identifiant, stratégie, essai, tp, sl, horizon, univers, nombre de versions
      de l'essai, et « OUI » pour la version identique à la fiche).
      [rend: 2]
    ⑥ TRAITEMENT — ① prendre tp, sl, horizon, univers dans cet ordre fixe ·
      ② produit cartésien des valeurs normalisées · ③ numéroter sur quatre
      chiffres, davantage si besoin · ④ marquer la version de la fiche.
    ⑦ UNITÉ — Voir ⑦ de l'en-tête.
    ⑧ POURQUOI — L'ordre fixe des réglages et l'ordre des valeurs du tableau font
      que le même tableau donne toujours les mêmes identifiants.
    ⑨ CE QUI CLOCHE — Changer l'ordre des valeurs dans le tableau change les
      numéros : un tableau validé ne doit plus être modifié, un nouvel essai prend
      un nouveau numéro.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    par = {l["parametre"]: l for l in lignes}
    strat, essai = lignes[0]["strategie"], lignes[0]["essai"]
    listes, fiche = [], []
    for p in OBLIGATOIRES:
        vals = [normaliser(p, v) for v in par[p]["valeurs_a_essayer"].split(";") if v.strip()]
        listes.append(vals)
        fiche.append(normaliser(p, par[p]["valeur_fiche"])[0])
    total = 1
    for v in listes:
        total *= len(v)
    largeur = max(4, len(str(total)))
    colonnes = ["id_version", "strategie", "essai"] + list(OBLIGATOIRES) + ["versions_dans_l_essai", "version_de_la_fiche"]
    versions = []
    for i, combo in enumerate(itertools.product(*listes), start=1):
        v = {"id_version": "%s-%s-%0*d" % (strat, essai, largeur, i), "strategie": strat, "essai": essai}
        v.update({p: x[1] for p, x in zip(OBLIGATOIRES, combo)})
        v["versions_dans_l_essai"] = str(total)
        v["version_de_la_fiche"] = "OUI" if [x[0] for x in combo] == fiche else ""
        versions.append(v)
    return colonnes, versions


def main(argv):
    """Enchaîne lecture, vérification, croisement, écriture et relecture.

    ① RÔLE — Le point d'entrée du programme.
    ② CONTEXTE D'APPEL — Le lancement en ligne de commande ; les épreuves l'appellent aussi.
    ③ ENTRÉE — `argv` : les trois arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① arguments · ② lire le tableau, la fiche, le référentiel ·
      ③ vérifier, refuser au moindre motif ·
      ④ décliner · ⑤ écrire en mode exclusif · ⑥ relire : mêmes lignes,
      identifiants uniques, une seule version de la fiche · ⑦ afficher le bilan.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La relecture prouve que le fichier écrit porte toutes les versions.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit un fichier nouveau ; l'efface si sa relecture échoue.
    ⑪ TERMINAISON — Rend la main avec un code ; c'est le bloc final qui sort.
      [sort: non]
    """
    if len(argv) != 3:
        print(__doc__)
        return 2
    registre, entree, dossier = argv
    refs = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(registre)), "REFERENTIEL_VALEURS*.csv")))
    if len(refs) != 1:
        print("REFUS : il faut exactement un référentiel des valeurs à côté du registre — trouvé %d" % len(refs))
        return 1
    try:
        lignes = lire_tableau(entree)
        fiches = [l for l in lire_tableau(registre) if lignes and l.get("id") == lignes[0].get("strategie")]
        codes_connus = {(l.get("mnemonique") or "").strip().upper() for l in lire_tableau(refs[0])
                        if not (l.get("hors_univers") or "").strip()} - {""}
    except OSError as e:
        print("REFUS : %s" % e)
        return 1
    motifs = verifier(lignes, fiches[0] if len(fiches) == 1 else None, codes_connus)
    if motifs:
        print("REFUS — rien n'est décliné :")
        for m in motifs:
            print("  · " + m)
        return 1
    colonnes, versions = decliner(lignes)
    sortie = os.path.join(dossier, "COMBINATOIRE_%s_%s.csv" % (lignes[0]["strategie"], lignes[0]["essai"]))
    os.makedirs(dossier, exist_ok=True)
    try:
        with open(sortie, "x", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=colonnes)
            w.writeheader()
            w.writerows(versions)
    except FileExistsError:
        print("REFUS : %s existe déjà — un essai ne se décline qu'une fois" % sortie)
        return 1
    relu = lire_tableau(sortie)
    ids = [r["id_version"] for r in relu]
    fiche = [r["id_version"] for r in relu if r["version_de_la_fiche"] == "OUI"]
    if relu != versions or len(set(ids)) != len(ids) or len(fiche) != 1:
        os.remove(sortie)
        print("ÉCHEC : le fichier relu ne portait pas exactement les versions calculées — il est effacé : %s" % sortie)
        return 1
    print("ÉCRIT : %s" % sortie)
    print("VERSIONS : %d · réglages croisés : %s" % (len(relu), ", ".join(OBLIGATOIRES)))
    print("VERSION IDENTIQUE À LA FICHE : %s" % fiche[0])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
