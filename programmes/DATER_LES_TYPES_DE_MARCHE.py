#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DATER LES TYPES DE MARCHÉ — chaque séance du CAC 40 reçoit son type : HAUSSE ou BAISSE croisé avec CALME ou
AGITÉ, et son époque (numéro de phase). Ven 27-11-2026 (Paris), lot L5 du plan R505, corrigé par le lot L5-CORR
d'après la relecture V1. Simulation uniquement.

① RÔLE — Découper l'historique de l'INDICE CAC 40 SEUL — jamais les résultats d'une stratégie — en quatre types de
  marché (HAUSSE_CALME, HAUSSE_AGITEE, BAISSE_CALME, BAISSE_AGITEE), à UN SEUL endroit, pour que le juge, la
  moulinette, la météo du marché et le calendrier lisent le même découpage (R-708 : deux implémentations d'une même
  chose divergent toujours). ① La hausse et la baisse se datent par les sommets et les creux selon le PROGRAMME
  PUBLIÉ PAR PAGAN ET SOSSOUNOV (bbstkjae.prg, archive de données du Journal of Applied Econometrics,
  2003-v18.1/pagan-sosunov), porté de Gauss en Python étape par étape — ou, en variante, par le filtre d'amplitude
  de Lunde et Timmermann (2004) ; ② le calme et l'agité se mesurent par la volatilité des rendements quotidiens sur
  une fenêtre glissante, comparée à un centile de toute la période.
② CONTEXTE D'APPEL — À la main, ou importé (`dater`, `types_aux_dates`, `figer`, `lire_le_fige`, `mesurer`,
  `lire_les_reglages`). Aucun appelant au 27-11-2026 : le juge, la moulinette et la météo ne le lisent pas encore
  (étapes suivantes du plan R505, W2a).
③ ENTRÉE — argv[1] : la racine du dépôt · argv[2] facultatif : `mesures` (affiche la sensibilité), `ecrire` suivi
  d'un chemin (une ligne par séance au contrat TYPES_DE_MARCHE), ou `figer` suivi d'une date de fin AAAA-MM-JJ et
  d'un chemin (découpage figé de la période, avec sa fiche d'empreintes).
④ CONDITIONS D'ENTRÉE — donnees/sources_indice/INDICE_CAC40.csv (contrat INDICE_CAC40), donnees/CALENDRIER_EURONEXT.csv
  et donnees/REGLAGES_DES_TYPES_DE_MARCHE.csv (contrat REGLAGES_DES_TYPES_DE_MARCHE) existent.
⑤ SORTIE — Lancé à la main : UN code de sortie, 0 si le découpage a été fait, 2 sinon (fichier absent ou faux,
  réglage inconnu, période impossible, fichier figé déjà présent) — R-734 : un calcul qui n'a pas pu se faire ne
  se tait pas.
⑥ TRAITEMENT — ① lire les réglages · ② lire les séances par le calendrier (CALENDRIER_DE_LA_BOURSE.lire_les_seances)
  et les clôtures par la météo (METEO_DU_MARCHE.lire_serie), sans les recopier · ③ convertir les durées, écrites en
  MOIS, dans le pas déclaré (`pas_de_temps` : séances au nombre MESURÉ de séances par mois, ou mois) · ④ sur le
  logarithme des cours : candidats dans une fenêtre entière, cycles minimaux, censure, bords, cycles, phases
  minimales avec levée — l'ordre et les règles du programme des auteurs · ⑤ numéroter les phases · ⑥ mesurer la
  volatilité et l'agitation · ⑦ croiser.
⑦ UNITÉ — Points d'indice ; rendements et levée en logarithme ; durées en SÉANCES ou en MOIS selon le pas (les
  réglages en mois sont convertis) ; seuils de Lunde et Timmermann en fraction (0,20 = 20 %).
⑧ POURQUOI — Décisions de Jean-Luc du 27-11-2026 : à 13h17 (A-1064, les quatre types remplacent les trois tranches
  égales sans fondement), à 16h03 (A-1078 étape 2 : un seul découpage, par l'indice seul, des deux côtés de la
  coupure 70/30), à 18h20 (A-1091 : « à partir des durées minimales de Pagan… si ça s'applique à ce qu'on est en
  train de faire et que tout est cohérent, vérifié et analysé par un expert »), à 21h14 (A-1102 : partir des valeurs
  rapportées, l'article étant introuvable). La relecture V1 (27-11-2026, 21h26) a trouvé le programme des auteurs :
  la règle publiée fait foi, pas un réglage inventé (défauts D1 à D9).
⑨ CE QUI CLOCHE — ① Le texte de l'article n'a pas été lu (accès refusé le 27-11-2026) ; le programme des auteurs
  l'a été ; le portage n'est confronté qu'au portage indépendant du relecteur V1 (mêmes retournements sur l'indice,
  au jour et au mois, mesuré le 27-11-2026) et à la chronologie connue du S&P 500. ② Le pas quotidien est un choix du
  lot (les auteurs datent des mois) : déclaré dans les réglages, la sensibilité au pas mensuel est affichée par
  `mesures`, EN ATTENTE DE JEAN-LUC. ③ Le centile d'agitation et la datation voient TOUTE la période lue : ajouter
  des séances change le type de séances passées ; le découpage n'est figé que par l'option `figer` (période et
  empreinte d'entrée). ④ L'indice n'a que des clôtures : pas d'estimateur d'étendue (Garman-Klass, Yang-Zhang), que
  l'étude de littérature de la météo jugeait meilleur. ⑤ Six séances n'ont que la source bnains (dont 2010-12-24) :
  prise faute de yahoo ; les deux sources diffèrent parfois. ⑥ Datation APRÈS COUP : elle sert à juger le passé,
  jamais à décider en direct (A-1079). ⑦ Le fichier de l'indice s'arrête au 2026-10-02 alors que le témoin des 20 ans
  va au 2026-11-11 : `types_aux_dates` rend INCONNU ces dates (jamais rangées d'office) ; prolonger l'indice reste à
  faire avant le branchement au juge.
⑩ EFFET — Lit trois fichiers et l'horloge (par le calendrier) ; n'écrit que les chemins donnés après `ecrire` ou
  `figer`.
⑪ TERMINAISON — Rend la main : toutes les boucles sont bornées par le nombre de séances ou de points.
⑫ DÉFINITIONS
  un sommet (un creux) : une séance dont la clôture est la plus haute (basse) de la fenêtre entière qui l'entoure
  une phase : la période entre deux points de retournement successifs — hausse d'un creux à un sommet, baisse
    d'un sommet à un creux ; une époque est une phase, numérotée dans l'ordre
  un cycle : d'un sommet au sommet suivant (ou d'un creux au creux suivant)
  la levée : une phase plus courte que la durée minimale est gardée si le logarithme du cours a bougé de plus que
    ce seuil
  le pas : l'unité de temps des cours datés, la séance (quotidien) ou la fin de mois (mensuel)
"""
import csv, hashlib, importlib.util, math, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
REGLAGES = os.path.join("donnees", "REGLAGES_DES_TYPES_DE_MARCHE.csv")
INDICE = os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv")
HAUSSE, BAISSE = "HAUSSE", "BAISSE"
CALME, AGITE, INCONNUE = "CALME", "AGITE", "INCONNUE"
SOMMET, CREUX = "SOMMET", "CREUX"


def _module(nom):
    """Charge un programme voisin par son chemin, sous un nom propre à ce fichier.

    ① RÔLE — Importer CONTRATS_DES_FICHIERS, CALENDRIER_DE_LA_BOURSE et METEO_DU_MARCHE sans recopier leur code.
    ② CONTEXTE D'APPEL — `lire_les_reglages`, `lire_l_indice`.
    ③ ENTRÉE — `nom` : le nom du fichier sans « .py », dans le même dossier que ce programme.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe à côté de ce programme.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, par chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : on importe et on appelle, on ne recopie pas.
    ⑨ CE QUI CLOCHE — Chaque appel recharge le module (pas de cache) : sans effet mesurable ici.
    ⑩ EFFET — Exécute le haut du module chargé (déclarations seulement pour les trois modules visés).
    ⑪ TERMINAISON — Rend la main ou lève (fichier absent, erreur de syntaxe).
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("types_marche_" + nom, os.path.join(ICI, nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def lire_les_reglages(racine):
    """Lit le fichier des réglages et le confronte à son contrat.

    ① RÔLE — Donner au découpage ses paramètres depuis un FICHIER DE DONNÉES, jamais depuis le code (le registre
      dit : les seuils viennent des données, pas du code).
    ② CONTEXTE D'APPEL — `dater`, `main`, les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt, qui porte donnees/REGLAGES_DES_TYPES_DE_MARCHE.csv.
    ④ CONDITIONS D'ENTRÉE — En-tête exactement le contrat REGLAGES_DES_TYPES_DE_MARCHE ; chaque paramètre attendu
      (contrat PARAMETRES_DES_TYPES_DE_MARCHE) présent une fois, avec l'unité attendue ; aucun paramètre inconnu.
    ⑤ SORTIE — UNE valeur : un dictionnaire {paramètre: valeur}, nombres en float, textes tels quels.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire · ② refuser en-tête, paramètre manquant, doublon, inconnu, unité fausse, nombre illisible,
      fraction hors ]0 ; 1[, durée négative.
    ⑦ UNITÉ — Celle de chaque ligne : mois, séances, fraction, logarithme (écart de logarithme), ou « — ».
    ⑧ POURQUOI — Un réglage mal écrit qui passerait en silence changerait tout le découpage sans que rien ne le dise.
    ⑨ CE QUI CLOCHE — `methode`, `durees_minimales` et `pas_de_temps` sont contrôlés sur leur liste de valeurs ; les
      textes `source` et `raison` ne sont pas contrôlés.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    c = _module("CONTRATS_DES_FICHIERS")
    chemin = os.path.join(racine, REGLAGES)
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.reader(f))
    if not lignes or lignes[0] != list(c.REGLAGES_DES_TYPES_DE_MARCHE):
        raise ValueError(f"réglages : en-tête {lignes[0] if lignes else 'absent'} au lieu de {c.REGLAGES_DES_TYPES_DE_MARCHE}")
    attendus = dict(c.PARAMETRES_DES_TYPES_DE_MARCHE)
    lu = {}
    for n, l in enumerate(lignes[1:], start=2):
        if not l:
            continue
        nom, valeur, unite = l[0], l[1], l[2]
        if nom not in attendus:
            raise ValueError(f"réglages, ligne {n} : paramètre inconnu « {nom} »")
        if nom in lu:
            raise ValueError(f"réglages, ligne {n} : « {nom} » écrit deux fois")
        if unite != attendus[nom]:
            raise ValueError(f"réglages, ligne {n} : « {nom} » en « {unite} » au lieu de « {attendus[nom]} »")
        if nom == "methode":
            if valeur not in c.METHODES_DES_TYPES_DE_MARCHE:
                raise ValueError(f"réglages, ligne {n} : méthode « {valeur} » hors {c.METHODES_DES_TYPES_DE_MARCHE}")
            lu[nom] = valeur
        elif nom == "durees_minimales":
            if valeur not in ("oui", "non"):
                raise ValueError(f"réglages, ligne {n} : durees_minimales « {valeur} » au lieu de oui ou non")
            lu[nom] = valeur
        elif nom == "pas_de_temps":
            if valeur not in c.PAS_DE_TEMPS_DES_TYPES_DE_MARCHE:
                raise ValueError(f"réglages, ligne {n} : pas « {valeur} » hors {c.PAS_DE_TEMPS_DES_TYPES_DE_MARCHE}")
            lu[nom] = valeur
        else:
            try:
                x = float(valeur)
            except ValueError:
                raise ValueError(f"réglages, ligne {n} : « {valeur} » illisible pour « {nom} »")
            if not math.isfinite(x) or x < 0:
                raise ValueError(f"réglages, ligne {n} : « {nom} » = {valeur} négatif ou infini")
            if unite == "fraction" and not 0 < x < 1:
                raise ValueError(f"réglages, ligne {n} : « {nom} » = {valeur} hors de ]0 ; 1[")
            lu[nom] = x
    manquants = [k for k in attendus if k not in lu]
    if manquants:
        raise ValueError(f"réglages : paramètre(s) manquant(s) {manquants}")
    return lu


def lire_l_indice(racine, jusqu_au=None):
    """Rend les séances de l'indice et leurs clôtures, par les lecteurs existants.

    ① RÔLE — Lire l'indice CAC 40 sans écrire un troisième lecteur : les séances viennent du calendrier, les clôtures
      de la météo.
    ② CONTEXTE D'APPEL — `dater`, les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `jusqu_au` : date AAAA-MM-JJ incluse où s'arrêter, ou None pour tout.
    ④ CONDITIONS D'ENTRÉE — Celles de CALENDRIER_DE_LA_BOURSE.lire_les_seances et de METEO_DU_MARCHE.lire_serie.
    ⑤ SORTIE — TROIS valeurs : la liste des dates (texte, triées), la liste des clôtures, le nombre de séances prises
      à la source bnains faute de yahoo.
      [rend: 3]
    ⑥ TRAITEMENT — ① séances = les dates où l'indice est publié · ② clôture = yahoo (la colonne que lit la météo),
      sinon bnains · ③ une séance sans aucune clôture lève.
    ⑦ UNITÉ — Points d'indice.
    ⑧ POURQUOI — R-708. Mesuré le 27-11-2026 : 6 844 séances du 2000-01-03 au 2026-10-02, dont 6 sans yahoo.
    ⑨ CE QUI CLOCHE — Le calendrier lit aussi l'horloge et la liste d'Euronext, ce qui ne sert pas ici ; ses alertes
      sont ignorées (elles concernent 2026 et l'avenir, pas la datation).
    ⑩ EFFET — Lit deux fichiers et l'horloge.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    cal = _module("CALENDRIER_DE_LA_BOURSE")
    met = _module("METEO_DU_MARCHE")
    jours = sorted(d.isoformat() for d in cal.lire_les_seances(racine)["indice"])
    yahoo = met.lire_serie(os.path.join(racine, INDICE), "yahoo")
    bnains = met.lire_serie(os.path.join(racine, INDICE), "bnains")
    if jusqu_au:
        jours = [d for d in jours if d <= jusqu_au]
    prix, de_bnains = [], 0
    for d in jours:
        if d in yahoo:
            prix.append(yahoo[d])
        elif d in bnains:
            prix.append(bnains[d]); de_bnains += 1
        else:
            raise ValueError(f"indice : aucune clôture le {d}")
    return jours, prix, de_bnains


def seances_par_mois(dates):
    """Mesure le nombre moyen de séances par mois civil complet.

    ① RÔLE — Convertir les durées de l'article, écrites en mois, en séances, par une mesure et non par un chiffre
      écrit à la main (R-728).
    ② CONTEXTE D'APPEL — `durees_en_pas`.
    ③ ENTRÉE — `dates` : les dates des séances, AAAA-MM-JJ, triées.
    ④ CONDITIONS D'ENTRÉE — Au moins trois mois civils distincts.
    ⑤ SORTIE — UNE valeur : séances par mois, en nombre décimal.
      [rend: 1]
    ⑥ TRAITEMENT — compter les séances de chaque mois, sans le premier ni le dernier mois (souvent incomplets).
    ⑦ UNITÉ — Séances par mois.
    ⑧ POURQUOI — Kole et van Dijk ont adapté les valeurs de l'article à leurs données hebdomadaires ; on adapte aux
      nôtres, quotidiennes. Mesuré le 27-11-2026 : 21,32 séances par mois sur 2000-02 → 2026-09.
    ⑨ CE QUI CLOCHE — Une moyenne : un mois de 19 séances et un de 23 comptent pareil.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    par_mois = {}
    for d in dates:
        par_mois[d[:7]] = par_mois.get(d[:7], 0) + 1
    mois = sorted(par_mois)
    if len(mois) < 3:
        raise ValueError("moins de trois mois de séances")
    pleins = mois[1:-1]
    return sum(par_mois[m] for m in pleins) / len(pleins)


def durees_en_pas(reglages, dates):
    """Convertit les réglages écrits en mois dans le pas de la datation.

    ① RÔLE — Donner aux étapes de datation des durées dans l'unité des données datées.
    ② CONTEXTE D'APPEL — `dater_hausse_baisse`.
    ③ ENTRÉE — `reglages` : le rendu de `lire_les_reglages` (éventuellement modifié pour la sensibilité) · `dates` :
      les dates des séances.
    ④ CONDITIONS D'ENTRÉE — Les quatre durées `fenetre_des_sommets`, `censure`, `phase_minimale`, `cycle_minimal`
      sont présentes, en mois ; `pas_de_temps` vaut quotidien ou mensuel.
    ⑤ SORTIE — UNE valeur : {nom: nombre entier de pas, « seances_par_mois »: la mesure, « pas »: le pas}.
      [rend: 1]
    ⑥ TRAITEMENT — quotidien : mois × séances par mois mesurées, arrondi à l'entier le plus proche ; mensuel : les
      mois, arrondis à l'entier.
    ⑦ UNITÉ — Séances (quotidien) ou mois (mensuel) : la clé « pas » le dit.
    ⑧ POURQUOI — L'unité voyage avec le nom : le fichier dit « mois », le calcul travaille dans le pas des données.
      Kole et van Dijk ont converti les mois de l'article en semaines pour leurs données hebdomadaires ; le lot L5
      les convertit en séances (défaut D6 de la relecture V1 : ce choix est déclaré, `pas_de_temps`).
    ⑨ CE QUI CLOCHE — L'arrondi de Python (au pair pour ,5) : sans effet sur les valeurs de départ au 27-11-2026
      (8 × 21,32 = 170,5 → 171 ; 4 → 85 ; 16 → 341).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError (pas inconnu).
      [sort: non]
    """
    spm = seances_par_mois(dates)
    noms = ("fenetre_des_sommets", "censure", "phase_minimale", "cycle_minimal")
    if reglages["pas_de_temps"] == "quotidien":
        out = {k: int(round(reglages[k] * spm)) for k in noms}
    elif reglages["pas_de_temps"] == "mensuel":
        out = {k: int(round(reglages[k])) for k in noms}
    else:
        raise ValueError(f"pas « {reglages['pas_de_temps']} » inconnu")
    out["seances_par_mois"] = spm
    out["pas"] = reglages["pas_de_temps"]
    return out


def extremes_locaux(x, fenetre):
    """Relève les sommets et les creux candidats (étape 1 du programme des auteurs, `dates1`).

    ① RÔLE — Trouver chaque séance (ou chaque mois) dont le cours est le plus haut (le plus bas) de la fenêtre
      ENTIÈRE qui l'entoure, `fenetre` pas avant et `fenetre` pas après.
    ② CONTEXTE D'APPEL — `dater_pagan_sossounov`.
    ③ ENTRÉE — `x` : les logarithmes des cours (ou les cours : l'ordre est le même) · `fenetre` : demi-largeur, en pas.
    ④ CONDITIONS D'ENTRÉE — `fenetre` ≥ 1.
    ⑤ SORTIE — DEUX valeurs : la liste croissante des rangs des sommets candidats, celle des creux candidats.
      [rend: 2]
    ⑥ TRAITEMENT — pour i de `fenetre` à n − 1 − `fenetre` seulement (jamais aux bords, où la fenêtre serait
      coupée) : sommet si x[i] est le maximum de x[i − f .. i + f], creux s'il en est le minimum ; à égalité, TOUS
      les rangs égaux sont gardés ici, l'alternance tranche ensuite (`alterner`).
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — Programme des auteurs, bbstkjae.prg (archive de données du Journal of Applied Econometrics,
      2003-v18.1/pagan-sosunov), l.493-505 : « Determine dates that are higher than any values ±8 months »,
      boucle `i=9; do while i <= nd-8` : la fenêtre est toujours entière. Défaut D2 de la relecture V1 (27-11-2026) :
      l'ancienne fenêtre coupée aux bords datait un sommet au 2000-09-04 que les auteurs n'admettent pas.
    ⑨ CE QUI CLOCHE — Une séance à la fois maximum et minimum (fenêtre plate) serait dans les deux listes, comme
      chez les auteurs : jamais vu sur l'indice. Calcul en n × (2f + 1), moins d'une seconde mesurée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : une boucle bornée.
      [sort: non]
    """
    n = len(x)
    sommets, creux = [], []
    for i in range(fenetre, n - fenetre):
        fen = x[i - fenetre:i + fenetre + 1]
        if x[i] == max(fen):
            sommets.append(i)
        if x[i] == min(fen):
            creux.append(i)
    return sommets, creux


def filtre_d_amplitude(prix, hausse, baisse):
    """Date les retournements par le filtre d'amplitude de Lunde et Timmermann (variante).

    ① RÔLE — Variante sans fenêtre : la baisse commence au sommet dès que l'indice a perdu `baisse` depuis ce sommet ;
      la hausse commence au creux dès qu'il a regagné `hausse` depuis ce creux.
    ② CONTEXTE D'APPEL — `dater_hausse_baisse`, méthode LT ; c'est la « datation simplifiée » du Chat du 27-11-2026.
    ③ ENTRÉE — `prix` : les clôtures · `hausse`, `baisse` : fractions (0,20 = 20 %).
    ④ CONDITIONS D'ENTRÉE — Au moins deux clôtures.
    ⑤ SORTIE — UNE valeur : liste triée et alternée de couples (rang, SOMMET ou CREUX).
      [rend: 1]
    ⑥ TRAITEMENT — ① départ : suivre le plus haut et le plus bas depuis la première séance jusqu'au premier
      mouvement de l'ampleur voulue, qui fixe le premier point · ② puis la machine à deux états de Lunde et
      Timmermann (2000, p. 4-5, équations 1 à 3).
    ⑦ UNITÉ — Rangs de séances.
    ⑧ POURQUOI — Sert à reproduire les mesures du Chat du 27-11 et à comparer la règle à seuil à celle de l'article.
    ⑨ CE QUI CLOCHE — La règle de départ diffère de celle de Kole et van Dijk (compter trois ajustements) : sans
      effet mesuré au 27-11-2026 sur les points d'après 2000-09 aux trois seuils.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : boucles bornées par le nombre de séances.
      [sort: non]
    """
    n = len(prix)
    hi = lo = prix[0]; ih = il = 0; etat = None; i = 0
    for i in range(n):
        if prix[i] > hi: hi, ih = prix[i], i
        if prix[i] < lo: lo, il = prix[i], i
        if prix[i] >= lo * (1 + hausse): etat = HAUSSE; break
        if prix[i] <= hi * (1 - baisse): etat = BAISSE; break
    if etat is None:
        return []
    if etat == HAUSSE:
        pts = [(il, CREUX)]; m = max(prix[il:i + 1]); im = il + prix[il:i + 1].index(m)
    else:
        pts = [(ih, SOMMET)]; m = min(prix[ih:i + 1]); im = ih + prix[ih:i + 1].index(m)
    for j in range(i + 1, n):
        if etat == HAUSSE:
            if prix[j] > m: m, im = prix[j], j
            elif prix[j] <= m * (1 - baisse): pts.append((im, SOMMET)); etat = BAISSE; m, im = prix[j], j
        else:
            if prix[j] < m: m, im = prix[j], j
            elif prix[j] >= m * (1 + hausse): pts.append((im, CREUX)); etat = HAUSSE; m, im = prix[j], j
    return pts


def _ensemble(sommets, creux):
    """Range sommets et creux en une seule liste chronologique.

    ① RÔLE — Passer des deux listes des auteurs (bcp, bct) à la liste des couples (rang, sorte), et retour.
    ② CONTEXTE D'APPEL — `alterner`, `phases_minimales`, `dater_pagan_sossounov`.
    ③ ENTRÉE — `sommets`, `creux` : rangs.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de couples (rang, SOMMET ou CREUX), triée par rang ; à rang égal, le creux d'abord.
      [rend: 1]
    ⑥ TRAITEMENT — tri.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — Les auteurs trient par `sortc(…, 1)` sur le rang ; l'ordre à rang égal n'est pas dit par Gauss :
      on prend celui du portage du relecteur (creux = 0 avant sommet = 1).
    ⑨ CE QUI CLOCHE — Un rang à la fois sommet et creux n'est jamais arrivé sur l'indice.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [(i, SOMMET if s else CREUX) for i, s in sorted([(i, 1) for i in sommets] + [(i, 0) for i in creux])]


def _separer(pts):
    """Sépare une liste de couples (rang, sorte) en sommets et creux.

    ① RÔLE — L'inverse de `_ensemble`.
    ② CONTEXTE D'APPEL — `alterner`, `phases_minimales`, `dater_hausse_baisse`.
    ③ ENTRÉE — `pts` : couples (rang, sorte).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : les rangs des sommets, ceux des creux, dans l'ordre de `pts`.
      [rend: 2]
    ⑥ TRAITEMENT — filtre.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [i for i, s in pts if s == SOMMET], [i for i, s in pts if s == CREUX]


def alterner(x, sommets, creux):
    """Impose l'alternance sommet, creux, sommet… (procédure `alter2` des auteurs).

    ① RÔLE — Quand deux points de même sorte se suivent, n'en garder qu'un : le plus haut des deux sommets, le plus
      bas des deux creux.
    ② CONTEXTE D'APPEL — `cycles_minimaux`, `censurer`, `bords`, `phases_minimales`.
    ③ ENTRÉE — `x` : les logarithmes des cours · `sommets`, `creux` : rangs.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : les sommets et les creux gardés, alternés.
      [rend: 2]
    ⑥ TRAITEMENT — parcourir la liste chronologique ; deux sommets de suite : si le premier est ≥ au second, retirer
      le second, sinon le premier (À ÉGALITÉ, LE PREMIER SOMMET RESTE) ; deux creux de suite : si le premier est ≥
      au second, retirer le premier, sinon le second (À ÉGALITÉ, LE SECOND CREUX RESTE) ; après un retrait, recomparer
      au même rang.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.343-402 (`alter2` : « eliminate lesser of two peaks », « eliminate greater of two
      troughs », tests `x[d1,1] .>= x[d2,1]`). Les égalités suivent le code des auteurs, pas un choix maison
      (défaut D9-N1 de la relecture V1).
    ⑨ CE QUI CLOCHE — L'asymétrie des égalités (premier sommet, second creux) est celle du code des auteurs ; elle
      n'est expliquée nulle part.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : chaque tour avance ou retire un point.
      [sort: non]
    """
    an = _ensemble(sommets, creux)
    j = 0
    while j < len(an) - 1:
        (d1, s1), (d2, s2) = an[j], an[j + 1]
        if s1 == s2:
            if s1 == SOMMET:
                del an[j + 1 if x[d1] >= x[d2] else j]
            else:
                del an[j if x[d1] >= x[d2] else j + 1]
            continue
        j += 1
    return _separer(an)


def cycles_minimaux(x, sommets, creux, cycle_min):
    """Retire les cycles trop courts en gardant le plus haut sommet et le plus bas creux (procédure `enf1p`).

    ① RÔLE — Deux sommets (deux creux) plus proches que `cycle_min` : n'en garder qu'un, le plus haut (le plus bas).
    ② CONTEXTE D'APPEL — `dater_pagan_sossounov` (deux fois), `dater_hausse_baisse` pour la variante LT.
    ③ ENTRÉE — `x` : les logarithmes des cours · `sommets`, `creux` : rangs · `cycle_min` : en pas.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : sommets et creux gardés, alternés.
      [rend: 2]
    ⑥ TRAITEMENT — ① sommets : pour i = 1, 2…, si sommets[i] − sommets[i−1] < `cycle_min`, retirer le plus bas des
      deux (à égalité, le PREMIER part), puis passer à i + 1 sans recomparer · ② alterner · ③ même chose sur les
      creux, en retirant le plus haut (à égalité, le premier part) · ④ alterner.
    ⑦ UNITÉ — Rangs, pas.
    ⑧ POURQUOI — bbstkjae.prg l.274-303 : « Enforce 16 month P-P and T-T cycles. If Violated, choose highest peak
      and lowest trough ». Défaut D1 de la relecture V1 : le paramètre `retrait_dans_un_cycle` du lot L5
      (« aucune source ne dit quelle phase retirer ») était inventé ; la règle publiée le dit. Cas réel : le cycle
      creux 2018-12-27 → creux 2020-03-18 (312 séances < 341) garde le creux le plus bas, celui du krach de 2020.
    ⑨ CE QUI CLOCHE — Après un retrait, la paire suivante n'est pas recomparée (le code des auteurs incrémente i) :
      une suite de trois sommets proches peut en garder deux ; c'est la règle publiée, reproduite telle quelle.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : boucles bornées par la longueur des listes.
      [sort: non]
    """
    sommets = list(sommets); i = 1
    while i < len(sommets):
        if sommets[i] - sommets[i - 1] < cycle_min:
            del sommets[i if x[sommets[i - 1]] > x[sommets[i]] else i - 1]
        i += 1
    sommets, creux = alterner(x, sommets, creux)
    creux = list(creux); i = 1
    while i < len(creux):
        if creux[i] - creux[i - 1] < cycle_min:
            del creux[i if x[creux[i - 1]] < x[creux[i]] else i - 1]
        i += 1
    return alterner(x, sommets, creux)


def censurer(x, sommets, creux, censure):
    """Retire le premier et le dernier point trop près des bouts de la série (procédure `enfvbp`).

    ① RÔLE — Ne pas dater un retournement que la suite (ou le début) des données pourrait démentir.
    ② CONTEXTE D'APPEL — `dater_pagan_sossounov`.
    ③ ENTRÉE — `x` : les logarithmes des cours (sert à la longueur et à l'alternance) · `sommets`, `creux` : rangs ·
      `censure` : en pas.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : sommets et creux gardés, alternés.
      [rend: 2]
    ⑥ TRAITEMENT — dans chaque liste, retirer le PREMIER point si son rang est < `censure` (rang compté de 0) et le
      DERNIER si son rang est ≥ n − `censure` ; puis alterner. Les autres points ne sont pas regardés.
    ⑦ UNITÉ — Rangs, pas.
    ⑧ POURQUOI — bbstkjae.prg l.406-432 : « Eliminate Turns with 4 months of beginning and end of series »,
      `if bcp[1,1] .<= 4` (rang compté de 1) et `if bcp[rows(bcp),1] .> rows(x)-4`. Défaut D5 de la relecture V1 :
      les textes secondaires disent 6 mois, le code des auteurs 4.
    ⑨ CE QUI CLOCHE — Avec la fenêtre entière (`extremes_locaux`), aucun candidat n'est à moins de `fenetre` pas
      des bouts : la censure de 4 mois (< 8) n'agit pas sur les candidats de l'étape 1 ; elle reste pour la règle.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    n = len(x)
    return alterner(x, _bouts(sommets, n, censure), _bouts(creux, n, censure))


def _bouts(liste, n, censure):
    """Retire d'une liste de rangs son premier élément s'il est < `censure` et son dernier s'il est ≥ n − `censure`.

    ① RÔLE — Le geste de `enfvbp` sur une liste (sommets, ou creux).
    ② CONTEXTE D'APPEL — `censurer`, une fois pour les sommets, une fois pour les creux.
    ③ ENTRÉE — `liste` : rangs croissants · `n` : nombre de pas de la série · `censure` : en pas.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une nouvelle liste (l'entrée n'est pas modifiée).
      [rend: 1]
    ⑥ TRAITEMENT — deux tests, sur le dernier puis le premier ; un seul élément trop près des deux bouts part une fois.
    ⑦ UNITÉ — Rangs, pas.
    ⑧ POURQUOI — bbstkjae.prg l.414-425 (rang de 1 ≤ 4 ⇔ rang de 0 < 4 ; rang de 1 > n − 4 ⇔ rang de 0 ≥ n − 4).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    garde = list(liste)
    if garde and garde[-1] >= n - censure:
        garde.pop()
    if garde and garde[0] < censure:
        garde.pop(0)
    return garde


def bords(x, sommets, creux):
    """Retire un premier (dernier) sommet plus bas que le premier (dernier) cours, et de même pour les creux
    (procédure `enfvcp`).

    ① RÔLE — Un sommet n'en est pas un si la série commence (finit) plus haut que lui ; un creux n'en est pas un si
      elle commence (finit) plus bas.
    ② CONTEXTE D'APPEL — `dater_pagan_sossounov`.
    ③ ENTRÉE — `x` : les logarithmes des cours · `sommets`, `creux` : rangs.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : sommets et creux gardés, alternés.
      [rend: 2]
    ⑥ TRAITEMENT — tant qu'un retrait a lieu : ① le premier point est un sommet et x[0] > x[sommet] → le retirer ;
      c'est un creux et x[0] < x[creux] → le retirer · ② de même pour le dernier point avec x[n−1] · puis alterner.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.434-480 : « Elimination of Peaks (and Troughs) at both ends which are lower (or
      higher) than values closer to end » ; appelé l.587, entre la censure et le second passage des cycles.
      Défaut D3 de la relecture V1 (L5-1 de Cowork) : l'étape manquait.
    ⑨ CE QUI CLOCHE — Si l'une des deux listes se vide, l'étape s'arrête (le code des auteurs ne traite pas ce cas).
      Effet mesuré sur l'indice au 27-11-2026 : nul (première clôture 5 917 sous le premier sommet candidat,
      dernière 7 897 au-dessus du dernier creux).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : chaque tour retire un point ou s'arrête.
      [sort: non]
    """
    sommets, creux = list(sommets), list(creux)
    while sommets and creux:
        if min(sommets + creux) == sommets[0]:
            if x[0] > x[sommets[0]]:
                sommets.pop(0); continue
        elif x[0] < x[creux[0]]:
            creux.pop(0); continue
        if max(sommets + creux) == sommets[-1]:
            if x[-1] > x[sommets[-1]]:
                sommets.pop(); continue
        elif x[-1] < x[creux[-1]]:
            creux.pop(); continue
        break
    return alterner(x, sommets, creux)


def phases_minimales(x, sommets, creux, phase_min, levee):
    """Retire les phases trop courtes, sauf mouvement plus fort que la levée (procédure `enfve_2`).

    ① RÔLE — Une phase de moins de `phase_min` pas disparaît si le logarithme du cours a bougé de `levee` au plus.
    ② CONTEXTE D'APPEL — `dater_pagan_sossounov`, `dater_hausse_baisse` pour la variante LT.
    ③ ENTRÉE — `x` : les LOGARITHMES des cours · `sommets`, `creux` : rangs · `phase_min` : en pas · `levee` : écart de
      logarithme (0,20).
    ④ CONDITIONS D'ENTRÉE — `x` est en logarithme : l'appelant le garantit.
    ⑤ SORTIE — DEUX valeurs : sommets et creux gardés, alternés.
      [rend: 2]
    ⑥ TRAITEMENT — parcourir les points dans l'ordre ; si le suivant est à moins de `phase_min` pas et que
      |x[suivant] − x[courant]| n'est pas > `levee`, retirer le SUIVANT, alterner, et recomparer au même rang.
    ⑦ UNITÉ — Rangs, pas ; écart de logarithme (0,20 en logarithme = +22,1 % en hausse, −18,1 % en baisse).
    ⑧ POURQUOI — bbstkjae.prg l.220-271 : `if nind-cind .< 4` et `if abs(x[nind]-x[cind]) .> .2`, sur le
      logarithme des cours (readme de l'archive : « the log of monthly US stock prices »). Défaut D4 de la
      relecture V1 : le lot L5 mesurait la levée en variation simple.
    ⑨ CE QUI CLOCHE — Le point retiré est toujours le second de la phase, quelle que soit sa hauteur : c'est le code
      des auteurs ; l'alternance qui suit garde ensuite le plus extrême.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : chaque tour avance ou retire un point.
      [sort: non]
    """
    an = _ensemble(sommets, creux)
    j = 0
    while j < len(an) - 1:
        c, s = an[j][0], an[j + 1][0]
        if s - c < phase_min and not abs(x[s] - x[c]) > levee:
            del an[j + 1]
            an = _ensemble(*alterner(x, *_separer(an)))
            continue
        j += 1
    return _separer(an)


def dater_pagan_sossounov(prix, fenetre, cycle_min, phase_min, censure, levee, durees_minimales=True):
    """La règle de Pagan et Sossounov, dans l'ordre de leur programme (procédure `findates`).

    ① RÔLE — Rendre les retournements d'une série de cours selon le programme publié par les auteurs.
    ② CONTEXTE D'APPEL — `dater_hausse_baisse` (pas quotidien ou mensuel), les épreuves.
    ③ ENTRÉE — `prix` : les cours, positifs · `fenetre`, `cycle_min`, `phase_min`, `censure` : en pas entiers ·
      `levee` : écart de logarithme · `durees_minimales` : faux pour sauter les cycles et les phases.
    ④ CONDITIONS D'ENTRÉE — Cours tous > 0.
    ⑤ SORTIE — UNE valeur : liste alternée de couples (rang, SOMMET ou CREUX), triée.
      [rend: 1]
    ⑥ TRAITEMENT — x = ln(cours) · ① candidats (fenêtre entière) · ② cycles (`cycles_minimaux`) · ③ censure ·
      ④ bords · ⑤ cycles de nouveau · ⑥ phases avec levée. Sans durées minimales : ① → alternance → ③ → ④.
    ⑦ UNITÉ — Rangs.
    ⑧ POURQUOI — bbstkjae.prg l.535-592 : `dates1` → `enf1p` → `enfvbp` → `enfvcp` → `enf1p` → `enfve_2`.
      Étalonné le 27-11-2026 sur le portage indépendant du relecteur V1 (mêmes retournements sur l'indice, au jour
      et au mois) ; décisions de Jean-Luc A-1091 (« à partir des durées minimales de Pagan… si ça s'applique… »)
      et A-1102 (valeurs de départ).
    ⑨ CE QUI CLOCHE — Le portage Gauss → Python n'est confronté qu'au portage du relecteur et à la chronologie
      connue du S&P 500 (1987, 1990) : le tableau de dates de l'article n'a pas été lu (accès refusé).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    x = [math.log(p) for p in prix]
    sommets, creux = extremes_locaux(x, fenetre)
    if durees_minimales:
        sommets, creux = cycles_minimaux(x, sommets, creux, cycle_min)
    else:
        sommets, creux = alterner(x, sommets, creux)
    sommets, creux = censurer(x, sommets, creux, censure)
    sommets, creux = bords(x, sommets, creux)
    if durees_minimales:
        sommets, creux = cycles_minimaux(x, sommets, creux, cycle_min)
        sommets, creux = phases_minimales(x, sommets, creux, phase_min, levee)
    return _ensemble(sommets, creux)


def fins_de_mois(dates):
    """Rend le rang de la dernière séance de chaque mois civil.

    ① RÔLE — Fabriquer la série MENSUELLE des auteurs (cours de fin de mois) à partir des séances quotidiennes.
    ② CONTEXTE D'APPEL — `dater_hausse_baisse`, pas mensuel.
    ③ ENTRÉE — `dates` : dates AAAA-MM-JJ triées.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste croissante de rangs (un par mois, le premier et le dernier mois compris).
      [rend: 1]
    ⑥ TRAITEMENT — garder la séance dont le mois diffère de celui de la suivante.
    ⑦ UNITÉ — Rangs de séances.
    ⑧ POURQUOI — Pas mensuel : défaut D6 de la relecture V1, pour afficher la sensibilité « pas des auteurs contre
      pas quotidien » ; même construction que le portage du relecteur (dernier cours du mois).
    ⑨ CE QUI CLOCHE — Le dernier mois peut être incomplet (2026-10 : deux séances) : son « fin de mois » est la
      dernière séance lue.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [k for k in range(len(dates)) if k == len(dates) - 1 or dates[k][:7] != dates[k + 1][:7]]


def dater_hausse_baisse(prix, dates, reglages):
    """Rend les points de retournement selon les réglages.

    ① RÔLE — Enchaîner les étapes de la méthode et du pas choisis.
    ② CONTEXTE D'APPEL — `dater`, `mesurer`, les épreuves.
    ③ ENTRÉE — `prix` : les clôtures · `dates` : leurs dates · `reglages` : le rendu de `lire_les_reglages`.
    ④ CONDITIONS D'ENTRÉE — `methode` vaut PS ou LT ; `pas_de_temps` vaut quotidien ou mensuel.
    ⑤ SORTIE — DEUX valeurs : la liste alternée des points (rang de SÉANCE, sorte), et les durées en pas.
      [rend: 2]
    ⑥ TRAITEMENT — PS quotidien : `dater_pagan_sossounov` sur les séances, durées converties en séances. PS
      mensuel : sur les cours de fin de mois, durées en mois telles quelles, puis chaque point est reporté sur la
      dernière séance de son mois. LT : filtre d'amplitude sur les séances, puis, si « oui », les cycles et les
      phases minimales des auteurs (`cycles_minimaux`, `phases_minimales`) ; la fenêtre et la censure ne servent pas.
    ⑦ UNITÉ — Rangs ; séances (quotidien) ou mois (mensuel).
    ⑧ POURQUOI — A-1064 ① ; A-1091 ; A-1102 ; défaut D6 de la relecture V1 (le pas est un choix déclaré).
    ⑨ CE QUI CLOCHE — LT suivi des durées de Pagan et Sossounov est un assemblage du lot : aucune source ne
      l'emploie ; il ne sert qu'en sensibilité. Le pas mensuel n'est fait que pour PS.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError (méthode ou pas inconnu).
      [sort: non]
    """
    d = durees_en_pas(reglages, dates)
    oui = reglages["durees_minimales"] == "oui"
    if reglages["methode"] == "PS" and reglages["pas_de_temps"] == "quotidien":
        pts = dater_pagan_sossounov(prix, d["fenetre_des_sommets"], d["cycle_minimal"], d["phase_minimale"],
                                    d["censure"], reglages["seuil_de_levee"], oui)
    elif reglages["methode"] == "PS" and reglages["pas_de_temps"] == "mensuel":
        rangs = fins_de_mois(dates)
        pts = dater_pagan_sossounov([prix[k] for k in rangs], d["fenetre_des_sommets"], d["cycle_minimal"],
                                    d["phase_minimale"], d["censure"], reglages["seuil_de_levee"], oui)
        pts = [(rangs[i], s) for i, s in pts]
    elif reglages["methode"] == "LT":
        pts = filtre_d_amplitude(prix, reglages["seuil_de_hausse"], reglages["seuil_de_baisse"])
        if oui:
            x = [math.log(p) for p in prix]
            s, c = cycles_minimaux(x, *_separer(pts), d["cycle_minimal"])
            pts = _ensemble(*phases_minimales(x, s, c, d["phase_minimale"], reglages["seuil_de_levee"]))
    else:
        raise ValueError(f"méthode « {reglages['methode']} » ou pas « {reglages['pas_de_temps']} » inconnu")
    return pts, d


def volatilites(prix, fenetre):
    """Écart-type glissant des rendements quotidiens.

    ① RÔLE — Mesurer la turbulence de chaque séance avec ce qui est connu à sa clôture.
    ② CONTEXTE D'APPEL — `dater`, `mesurer`.
    ③ ENTRÉE — `prix` : les clôtures · `fenetre` : nombre de rendements, en séances.
    ④ CONDITIONS D'ENTRÉE — `fenetre` ≥ 2.
    ⑤ SORTIE — UNE valeur : liste de même longueur que `prix` ; None pour les `fenetre` premières séances.
      [rend: 1]
    ⑥ TRAITEMENT — rendement r[i] = ln(p[i] ÷ p[i−1]) ; à la séance i, écart-type (de population) de r[i−f+1..i].
    ⑦ UNITÉ — Écart-type d'un rendement quotidien en logarithme (0,01 ≈ 1 % par jour).
    ⑧ POURQUOI — C'est la mesure avec laquelle le Chat a obtenu le 27-11-2026 ses médianes d'épisodes (8 et 20 à 20
      séances, 18 et 58 à 60), reproduites par ce programme ; l'indice n'a que des clôtures.
    ⑨ CE QUI CLOCHE — Pas d'estimateur d'étendue (⑨ ④ du programme) ; somme glissante recalculée à chaque séance.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = [None] + [math.log(prix[i] / prix[i - 1]) for i in range(1, len(prix))]
    out = [None] * len(prix)
    for i in range(fenetre, len(prix)):
        x = r[i - fenetre + 1:i + 1]
        m = sum(x) / fenetre
        out[i] = math.sqrt(sum((a - m) ** 2 for a in x) / fenetre)
    return out


def seuil_d_agitation(vols, centile):
    """Rend la volatilité au-delà de laquelle une séance est agitée.

    ① RÔLE — Fixer le seuil calme/agité sur toute la période lue.
    ② CONTEXTE D'APPEL — `dater`, `mesurer`.
    ③ ENTRÉE — `vols` : le rendu de `volatilites` · `centile` : fraction (0,80 = 80e centile).
    ④ CONDITIONS D'ENTRÉE — Au moins une volatilité connue.
    ⑤ SORTIE — UNE valeur : la volatilité de rang int(centile × N) parmi les N connues, triées (rang de 0 à N−1).
      [rend: 1]
    ⑥ TRAITEMENT — tri, puis rang.
    ⑦ UNITÉ — Celle de `volatilites`.
    ⑧ POURQUOI — Études récentes : agité au-dessus du 80e centile (arXiv 2506.06356, rapporté par A-1064).
    ⑨ CE QUI CLOCHE — Le seuil voit toute la période, l'avenir compris (⑨ ③ et ⑥ du programme).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    connues = sorted(v for v in vols if v is not None)
    if not connues:
        raise ValueError("aucune volatilité connue")
    return connues[min(len(connues) - 1, int(centile * len(connues)))]


def dater(racine, surcharges=None, jusqu_au=None):
    """Rend, pour chaque séance, son sens, son époque, son agitation et son type.

    ① RÔLE — Le point d'entrée que liront le juge, la moulinette, la météo et le calendrier.
    ② CONTEXTE D'APPEL — `main` ; à venir : JUGE_DES_STRATEGIES, JOUER_LES_VERSIONS (W2a).
    ③ ENTRÉE — `racine` : la racine du dépôt · `surcharges` : dictionnaire qui remplace des réglages du fichier (pour
      la sensibilité), ou None · `jusqu_au` : date AAAA-MM-JJ incluse, ou None.
    ④ CONDITIONS D'ENTRÉE — Celles de `lire_les_reglages` et `lire_l_indice` ; au moins deux points de retournement.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes (dictionnaires au contrat TYPES_DE_MARCHE, une par séance lue) et
      un dictionnaire de contexte (réglages effectifs, durées en pas, seuil d'agitation, empreinte du fichier de
      l'indice, empreinte des séances lues, `jusqu_au`, points de retournement, cours extrême en attente à la fin).
      [rend: 2]
    ⑥ TRAITEMENT — ① points de retournement · ② avant le premier point : le sens opposé à celui qui commence au
      premier point (après un sommet vient la baisse, donc avant lui la hausse) ; après le dernier : le sens qui
      commence au dernier point ; ces deux phases sont « non terminées » · ③ la séance d'un sommet appartient à la
      hausse qu'il termine, celle d'un creux à la baisse qu'il termine · ④ agitation · ⑤ type = sens + agitation,
      INCONNU tant que la volatilité n'est pas connue.
    ⑦ UNITÉ — Points d'indice ; séances.
    ⑧ POURQUOI — A-1064, A-1078 étape 2.
    ⑨ CE QUI CLOCHE — Les phases ouvertes des deux bouts reçoivent un sens que la règle n'a pas confirmé
      (`phase_terminee` = 0 le dit). Une date demandée qui n'est pas une séance lue n'a pas de ligne : la demander
      par `types_aux_dates`, qui rend INCONNU. `jusqu_au` est INCLUS.
    ⑩ EFFET — Lit trois fichiers et l'horloge.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    reglages = dict(lire_les_reglages(racine))
    reglages.update(surcharges or {})
    dates, prix, de_bnains = lire_l_indice(racine, jusqu_au)
    pts, durees = dater_hausse_baisse(prix, dates, reglages)
    if len(pts) < 2:
        raise ValueError(f"{len(pts)} point(s) de retournement : découpage impossible")
    vols = volatilites(prix, int(reglages["fenetre_de_volatilite"]))
    seuil = seuil_d_agitation(vols, reglages["centile_d_agitation"])
    bornes = [-1] + [i for i, _ in pts] + [len(prix) - 1]
    sens_apres = {SOMMET: BAISSE, CREUX: HAUSSE}
    sens_phases = [HAUSSE if pts[0][1] == SOMMET else BAISSE] + [sens_apres[s] for _, s in pts]
    lignes = []
    for e in range(len(bornes) - 1):
        terminee = 0 if e in (0, len(bornes) - 2) else 1
        for i in range(bornes[e] + 1, bornes[e + 1] + 1):
            v = vols[i]
            ag = INCONNUE if v is None else (AGITE if v > seuil else CALME)
            sens = sens_phases[e]
            typ = "INCONNU" if ag == INCONNUE else f"{sens}_{'AGITEE' if ag == AGITE else 'CALME'}"
            lignes.append({"date": dates[i], "cloture": prix[i], "sens": sens, "epoque": e + 1,
                           "phase_terminee": terminee, "volatilite": "" if v is None else round(v, 6),
                           "agitation": ag, "type": typ})
    with open(os.path.join(racine, INDICE), "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()[:16]
    contexte = {"reglages": reglages, "durees": durees, "seuil_d_agitation": seuil, "empreinte_indice": empreinte,
                "empreinte_entree": empreinte_de_l_entree(dates, prix), "jusqu_au": jusqu_au,
                "points": [(dates[i], s) for i, s in pts], "seances_bnains": de_bnains,
                "en_attente": point_en_attente(prix, dates, pts, durees)}
    return lignes, contexte


def empreinte_de_l_entree(dates, prix):
    """Empreinte des séances datées, indépendante de ce que le fichier porte après la période.

    ① RÔLE — Dire, pour un découpage figé, sur QUELLES séances il a été fait ; l'empreinte du fichier entier change
      dès qu'une séance s'ajoute, celle-ci non.
    ② CONTEXTE D'APPEL — `dater`, `lire_le_fige`.
    ③ ENTRÉE — `dates`, `prix` : les séances lues et leurs clôtures, de même longueur.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux (sha256 des lignes « date;clôture » en repr de Python).
      [rend: 1]
    ⑥ TRAITEMENT — concaténer, hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Défaut D8 de la relecture V1 : le découpage du passé dépend de la fin des données ; il se fige sur
      une période déclarée (A-1063, A-1064 ⑤), et une révision d'une séance de cette période doit se voir.
    ⑨ CE QUI CLOCHE — `repr` d'un float : stable en Python 3 ; une autre langue devrait reproduire ce format.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    texte = "".join(f"{d};{p!r}\n" for d, p in zip(dates, prix))
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:16]


def point_en_attente(prix, dates, pts, durees):
    """Dit quel cours extrême, après le dernier retournement, pourrait encore devenir un retournement.

    ① RÔLE — Afficher que la fin des données peut changer le sens de séances passées (défaut D8 de la relecture V1).
    ② CONTEXTE D'APPEL — `dater` (le contexte), `main`.
    ③ ENTRÉE — `prix`, `dates` : les séances · `pts` : les retournements (rang de séance, sorte) · `durees` : le
      rendu de `durees_en_pas`.
    ④ CONDITIONS D'ENTRÉE — Au moins un point.
    ⑤ SORTIE — UNE valeur : None, ou un dictionnaire {date, sorte, cloture, seances_apres, fenetre_en_seances} : le
      plus haut cours (si le dernier point est un creux) ou le plus bas (si c'est un sommet) venu après le dernier
      point, le nombre de séances lues après lui, et la demi-fenêtre en séances.
      [rend: 1]
    ⑥ TRAITEMENT — chercher l'extrême après le dernier point ; demi-fenêtre en séances = `fenetre_des_sommets` ×
      séances par mois au pas mensuel, telle quelle au pas quotidien.
    ⑦ UNITÉ — Dates, points d'indice, séances.
    ⑧ POURQUOI — Mesuré par la relecture V1 : le plus haut du 2026-08-10 (8 726,03) n'a que 37 séances après lui ;
      s'il n'est pas battu pendant une fenêtre entière, il deviendra un sommet et la fin passera en BAISSE.
    ⑨ CE QUI CLOCHE — C'est un candidat, pas une prévision : les durées minimales peuvent encore le retirer.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not pts or pts[-1][0] >= len(prix) - 1:
        return None
    dernier, sorte = pts[-1]
    apres = range(dernier + 1, len(prix))
    k = (max if sorte == CREUX else min)(apres, key=lambda j: prix[j])
    f = durees["fenetre_des_sommets"]
    if durees["pas"] == "mensuel":
        f = int(round(f * durees["seances_par_mois"]))
    return {"date": dates[k], "sorte": SOMMET if sorte == CREUX else CREUX, "cloture": prix[k],
            "seances_apres": len(prix) - 1 - k, "fenetre_en_seances": f}


def types_aux_dates(lignes, dates_demandees):
    """Rend le type de marché de dates demandées, INCONNU pour une date sans séance de l'indice.

    ① RÔLE — La seule porte par laquelle un lecteur (juge, moulinette) demande le type d'un jour : une date que le
      découpage ne porte pas n'est JAMAIS rangée d'office dans un type (ni celui de la veille, ni le plus proche).
    ② CONTEXTE D'APPEL — À venir : le juge et la moulinette (W2a) ; les épreuves.
    ③ ENTRÉE — `lignes` : le premier rendu de `dater` (ou les lignes d'un découpage figé) · `dates_demandees` :
      dates AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : {date: type} (un de TYPES_DE_MARCHE_ADMIS) et {date: motif} pour chaque date INCONNUE
      — « après la dernière séance datée », « avant la première séance datée », « pas une séance de l'indice »,
      « volatilité pas encore connue ».
      [rend: 2]
    ⑥ TRAITEMENT — recherche exacte de la date ; sinon INCONNU avec son motif.
    ⑦ UNITÉ — Dates.
    ⑧ POURQUOI — Défaut D7 de la relecture V1 (bloquant pour le branchement au juge) : le fichier de l'indice
      s'arrête au 2026-10-02, le témoin des 20 ans au 2026-11-11 (28 dates sans type), et le 2016-03-28, lundi de
      Pâques, n'est pas une séance de l'indice. La loi (R-505 v2, étape 3) : « un jour sans type de marché n'est
      jamais rangé d'office dans un type, il rend INCONNUS les contrôles par type de marché ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    par_date = {l["date"]: l["type"] for l in lignes}
    premiere, derniere = (lignes[0]["date"], lignes[-1]["date"]) if lignes else ("", "")
    types, motifs = {}, {}
    for d in dates_demandees:
        t = par_date.get(d, "INCONNU")
        types[d] = t
        if d not in par_date:
            motifs[d] = ("après la dernière séance datée" if d > derniere else
                         "avant la première séance datée" if d < premiere else "pas une séance de l'indice")
        elif t == "INCONNU":
            motifs[d] = "volatilité pas encore connue"
    return types, motifs


def _sha(chemin):
    """sha256 d'un fichier, 16 premiers caractères.

    ① RÔLE — Empreinte d'un fichier pour la fiche de figeage.
    ② CONTEXTE D'APPEL — `figer`, `lire_le_fige`.
    ③ ENTRÉE — `chemin` : un fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — lecture en octets, hachage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def figer(racine, jusqu_au, chemin):
    """Date une période donnée et écrit le découpage FIGÉ, avec sa fiche d'empreintes.

    ① RÔLE — Fixer le découpage AVANT de regarder les résultats d'une stratégie (A-1063, A-1064 ⑤) : la période
      est déclarée, le résultat écrit une fois, jamais réécrit.
    ② CONTEXTE D'APPEL — `main` (option `figer`) ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `jusqu_au` : date AAAA-MM-JJ incluse, fin de la période datée ·
      `chemin` : le CSV à écrire (la fiche s'écrit à `chemin` + « .fige.json »).
    ④ CONDITIONS D'ENTRÉE — `jusqu_au` n'est pas après la dernière séance de l'indice ; ni le CSV ni la fiche
      n'existent déjà.
    ⑤ SORTIE — UNE valeur : la fiche (dictionnaire aux clés FIGEAGE_DES_TYPES_DE_MARCHE).
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser une fin au-delà de l'indice (sinon on daterait moins que demandé, en silence) et un
      fichier existant · ② `dater(racine, jusqu_au=…)` · ③ écrire le CSV au contrat TYPES_DE_MARCHE · ④ écrire la
      fiche : période, empreintes de l'entrée, de l'indice, des réglages, du programme, du CSV, réglages, points,
      heure de Paris.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Défaut D8 de la relecture V1 : dater les seuls 70 % change le type de 214 des 4 790 séances
      (4,5 %) ; la loi (R-505 v2, étape 2 ⑤) exige un découpage figé et déclaré.
    ⑨ CE QUI CLOCHE — Le refus d'écraser ne protège que le chemin donné : rien n'empêche de figer ailleurs une
      autre période ; c'est la déclaration de la stratégie qui doit nommer le fichier figé (à faire, W2a).
    ⑩ EFFET — Écrit deux fichiers.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    import datetime, json
    from zoneinfo import ZoneInfo
    c = _module("CONTRATS_DES_FICHIERS")
    fiche_chemin = chemin + ".fige.json"
    for x in (chemin, fiche_chemin):
        if os.path.exists(x):
            raise ValueError(f"{x} existe déjà : un découpage figé ne se réécrit pas")
    tous, _, _ = lire_l_indice(racine)
    if jusqu_au > tous[-1]:
        raise ValueError(f"jusqu_au {jusqu_au} après la dernière séance de l'indice ({tous[-1]}) : rien n'est daté")
    lignes, ctx = dater(racine, jusqu_au=jusqu_au)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(c.TYPES_DE_MARCHE))
        w.writeheader(); w.writerows(lignes)
    fiche = {"jusqu_au": jusqu_au, "premiere_seance": lignes[0]["date"], "derniere_seance": lignes[-1]["date"],
             "seances": len(lignes), "empreinte_entree": ctx["empreinte_entree"],
             "empreinte_indice": ctx["empreinte_indice"], "empreinte_reglages": _sha(os.path.join(racine, REGLAGES)),
             "empreinte_programme": _sha(os.path.abspath(__file__)), "empreinte_sortie": _sha(chemin),
             "reglages": ctx["reglages"], "points": ctx["points"],
             "fige_le": datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d_%Hh%M")}
    assert tuple(fiche) == tuple(c.FIGEAGE_DES_TYPES_DE_MARCHE)
    with open(fiche_chemin, "w", encoding="utf-8") as f:
        json.dump(fiche, f, ensure_ascii=False, indent=1)
    return fiche


def lire_le_fige(chemin, racine=None):
    """Relit un découpage figé et refuse s'il a changé.

    ① RÔLE — La lecture d'un découpage figé par le juge ou la moulinette : le CSV doit être celui que la fiche
      décrit, et, si `racine` est donnée, les séances de la période doivent être restées les mêmes dans l'indice.
    ② CONTEXTE D'APPEL — À venir : le juge, la moulinette (W2a) ; les épreuves.
    ③ ENTRÉE — `chemin` : le CSV figé (sa fiche à côté) · `racine` : la racine du dépôt, ou None.
    ④ CONDITIONS D'ENTRÉE — Les deux fichiers existent.
    ⑤ SORTIE — DEUX valeurs : les lignes (dictionnaires de textes, au contrat TYPES_DE_MARCHE) et la fiche.
      [rend: 2]
    ⑥ TRAITEMENT — ① empreinte du CSV contre `empreinte_sortie` · ② clés de la fiche contre le contrat · ③ si
      `racine` : relire l'indice jusqu'à `jusqu_au` et comparer `empreinte_entree` (une révision du passé ou une
      séance ajoutée dans la période se voit).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Défaut D8 de la relecture V1 ; « les révisions du passé se détectent, elles ne se devinent pas ».
    ⑨ CE QUI CLOCHE — Les nombres du CSV relu sont des textes : à convertir par le lecteur.
    ⑩ EFFET — Lit deux fichiers (trois avec `racine`).
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    import json
    c = _module("CONTRATS_DES_FICHIERS")
    with open(chemin + ".fige.json", encoding="utf-8") as f:
        fiche = json.load(f)
    if tuple(fiche) != tuple(c.FIGEAGE_DES_TYPES_DE_MARCHE):
        raise ValueError(f"fiche de figeage : clés {tuple(fiche)} au lieu de {c.FIGEAGE_DES_TYPES_DE_MARCHE}")
    if _sha(chemin) != fiche["empreinte_sortie"]:
        raise ValueError(f"{chemin} : empreinte {_sha(chemin)} au lieu de {fiche['empreinte_sortie']} : modifié")
    if racine is not None:
        dates, prix, _ = lire_l_indice(racine, fiche["jusqu_au"])
        if empreinte_de_l_entree(dates, prix) != fiche["empreinte_entree"]:
            raise ValueError("les séances de la période ont changé dans l'indice depuis le figeage")
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))
    return lignes, fiche


def _mediane(xs):
    """Médiane d'une liste, ou None si elle est vide.

    ① RÔLE — Résumer des durées.
    ② CONTEXTE D'APPEL — `mesurer`.
    ③ ENTRÉE — `xs` : des nombres.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la médiane (moyenne des deux du milieu pour un nombre pair), ou None.
      [rend: 1]
    ⑥ TRAITEMENT — tri.
    ⑦ UNITÉ — Celle de `xs`.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s = sorted(xs)
    if not s:
        return None
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def mesurer(lignes):
    """Compte et mesure les phases, les épisodes et les types d'un découpage.

    ① RÔLE — Donner les chiffres du rapport à Jean-Luc et du tableau de sensibilité, calculés et jamais écrits.
    ② CONTEXTE D'APPEL — `main` (option `mesures`), les épreuves, le rapport L5.
    ③ ENTRÉE — `lignes` : le premier rendu de `dater`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : dictionnaire — nombre de phases terminées et non terminées, durées médianes hausse et
      baisse (terminées seules, puis avec les non terminées), nombre de cycles sommet→sommet, épisodes agités et
      calmes (nombre, médiane), séances par type, et pour h = 3, 10, 20 séances la part des séances dont les h
      séances suivantes restent dans le même type (`meme_type_sur_h`) et dans la même époque (`meme_sens_sur_h`).
      [rend: 1]
    ⑥ TRAITEMENT — Durée d'une phase = rang de sa dernière séance − rang de la dernière séance de la phase
      précédente (de point à point), pour la première phase : son nombre de séances − 1. Un épisode = une suite de
      séances de même agitation connue.
    ⑦ UNITÉ — Séances ; nombres.
    ⑧ POURQUOI — Condition ③ d'A-1091 ; la part « même type sur h séances » dit si une opération de 3 à 20 séances
      reste dans le type de son jour d'achat (condition ②).
    ⑨ CE QUI CLOCHE — Les séances de type INCONNU ne sont pas prises comme départ, mais une fenêtre qui en
      contiendrait compterait comme changeante : sans effet, elles sont toutes au début.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    phases = {}
    for k, l in enumerate(lignes):
        p = phases.setdefault(l["epoque"], {"sens": l["sens"], "terminee": l["phase_terminee"], "debut": k, "fin": k})
        p["fin"] = k
    ordre = [phases[e] for e in sorted(phases)]
    for j, p in enumerate(ordre):
        p["duree"] = p["fin"] - (ordre[j - 1]["fin"] if j else p["debut"])
    fini = [p for p in ordre if p["terminee"]]
    out = {"phases_terminees": len(fini), "phases_non_terminees": len(ordre) - len(fini),
           "hausse_mediane": _mediane([p["duree"] for p in fini if p["sens"] == HAUSSE]),
           "baisse_mediane": _mediane([p["duree"] for p in fini if p["sens"] == BAISSE]),
           "hausse_mediane_avec_fin": _mediane([p["duree"] for p in ordre[1:] if p["sens"] == HAUSSE]),
           "baisse_mediane_avec_fin": _mediane([p["duree"] for p in ordre[1:] if p["sens"] == BAISSE]),
           "hausses_terminees": sum(1 for p in fini if p["sens"] == HAUSSE),
           "baisses_terminees": sum(1 for p in fini if p["sens"] == BAISSE)}
    sommets = [p for p in ordre[:-1] if p["sens"] == HAUSSE]
    out["cycles_sommet_a_sommet"] = max(0, len(sommets) - 1)
    episodes = {AGITE: [], CALME: []}
    prec, long_ = None, 0
    for l in lignes + [{"agitation": None}]:
        if l["agitation"] == prec:
            long_ += 1
            continue
        if prec in episodes:
            episodes[prec].append(long_)
        prec, long_ = l["agitation"], 1
    out["episodes_agites"] = len(episodes[AGITE]); out["agite_median"] = _mediane(episodes[AGITE])
    out["episodes_calmes"] = len(episodes[CALME]); out["calme_median"] = _mediane(episodes[CALME])
    out["seances_par_type"] = {}
    for l in lignes:
        out["seances_par_type"][l["type"]] = out["seances_par_type"].get(l["type"], 0) + 1
    types = [l["type"] for l in lignes]
    for h in (3, 10, 20):
        debuts = [i for i in range(len(types) - h) if types[i] != "INCONNU"]
        out[f"meme_type_sur_{h}"] = sum(1 for i in debuts if len(set(types[i:i + h + 1])) == 1) / len(debuts)
        out[f"meme_sens_sur_{h}"] = sum(1 for i in debuts if lignes[i]["sens"] == lignes[i + h]["sens"]
                                        and lignes[i]["epoque"] == lignes[i + h]["epoque"]) / len(debuts)
    return out


def sens_differents(a, b):
    """Compte les séances communes dont le sens (ou le type) diffère entre deux découpages.

    ① RÔLE — Mesurer, pour l'affichage de sensibilité, ce qu'un autre réglage ou une autre fin de données change.
    ② CONTEXTE D'APPEL — `main` (option `mesures`).
    ③ ENTRÉE — `a`, `b` : deux rendus de `dater` (premières valeurs).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le nombre de dates communes, combien changent de sens, combien changent de type.
      [rend: 3]
    ⑥ TRAITEMENT — jointure par date.
    ⑦ UNITÉ — Séances.
    ⑧ POURQUOI — Défauts D6 et D8 de la relecture V1 : afficher, pas décider.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    pb = {l["date"]: l for l in b}
    communes = [l for l in a if l["date"] in pb]
    return (len(communes), sum(1 for l in communes if l["sens"] != pb[l["date"]]["sens"]),
            sum(1 for l in communes if l["type"] != pb[l["date"]]["type"]))


def main(argv):
    """Lance le découpage à la main.

    ① RÔLE — Afficher le découpage au réglage du fichier, le tableau de sensibilité, écrire les lignes, ou figer
      une période.
    ② CONTEXTE D'APPEL — Ligne de commande.
    ③ ENTRÉE — `argv` : [programme, racine, (mesures | ecrire chemin | figer jusqu_au chemin)].
    ④ CONDITIONS D'ENTRÉE — Celles de `dater` (et de `figer` pour l'option `figer`).
    ⑤ SORTIE — UNE valeur : le code de sortie, 0 si le découpage est fait, 2 sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① découpage au réglage du fichier, avec le cours extrême encore en attente à la fin des
      données · ② `mesures` : méthodes PS et LT, seuils 15, 20, 25 %, avec et sans durées minimales, fenêtres de
      volatilité 20 et 60 ; puis le PAS MENSUEL DES AUTEURS CONTRE LE PAS QUOTIDIEN ; puis l'effet de la fin des
      données (dater en s'arrêtant 250, 500, 1 000 et 2 000 séances plus tôt) · ③ `ecrire` : CSV au contrat ·
      ④ `figer` : `figer(racine, jusqu_au, chemin)`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un code non nul quand rien n'a pu se faire. La sensibilité s'AFFICHE, elle ne sert jamais
      à rechoisir un réglage après coup (R-505 v2, étape 2 ③).
    ⑨ CE QUI CLOCHE — La sensibilité relit l'indice à chaque réglage (une quarantaine de lectures, quelques
      secondes). La part des séances changées n'est pas coupée en 70 % / 30 % : la coupure vit dans
      MODULE_JUGEMENT.frontiere_de_la_fiche et dépend du calendrier lu (R-708) ; non affichée ici.
    ⑩ EFFET — Affiche ; écrit le chemin donné après `ecrire` ou `figer`.
    ⑪ TERMINAISON — Rend la main ; toute erreur est rattrapée et rend 2.
      [sort: non]
    """
    if len(argv) < 2:
        print(__doc__.split("\n")[0]); return 2
    racine = argv[1]
    try:
        lignes, ctx = dater(racine)
        m = mesurer(lignes)
        print(f"réglage du fichier : {ctx['reglages']}")
        print(f"durées en pas : {ctx['durees']} · seuil d'agitation {ctx['seuil_d_agitation']:.6f} · "
              f"empreinte de l'indice {ctx['empreinte_indice']} · {len(lignes)} séances, {ctx['seances_bnains']} prises à bnains")
        print(f"points : {ctx['points']}")
        att = ctx["en_attente"]
        if att:
            print(f"FIN DES DONNÉES : {att['sorte']} candidat le {att['date']} ({att['cloture']}), {att['seances_apres']} "
                  f"séance(s) lue(s) après lui pour une demi-fenêtre de {att['fenetre_en_seances']} : s'il tient, le sens "
                  f"des séances depuis le dernier point peut changer — le découpage d'une période se FIGE (option figer)")
        print(f"mesures : {m}")
        if len(argv) > 2 and argv[2] == "mesures":
            print("méthode;seuil;durées;fenêtre;phases_terminées;hausse_méd;baisse_méd;hausse_méd_avec_fin;cycles;"
                  "épisodes_agités;agité_méd;épisodes_calmes;calme_méd;même_type_3;même_type_10;même_type_20;même_époque_20")
            for methode in ("PS", "LT"):
                for seuil in (0.15, 0.20, 0.25):
                    for durees in ("oui", "non"):
                        for fen in (20, 60):
                            s = {"methode": methode, "durees_minimales": durees, "fenetre_de_volatilite": fen}
                            s.update({"seuil_de_levee": seuil} if methode == "PS" else
                                     {"seuil_de_hausse": seuil, "seuil_de_baisse": seuil})
                            mm = mesurer(dater(racine, s)[0])
                            print(f"{methode};{seuil};{durees};{fen};{mm['phases_terminees']};{mm['hausse_mediane']};"
                                  f"{mm['baisse_mediane']};{mm['hausse_mediane_avec_fin']};{mm['cycles_sommet_a_sommet']};"
                                  f"{mm['episodes_agites']};{mm['agite_median']};{mm['episodes_calmes']};{mm['calme_median']};"
                                  f"{mm['meme_type_sur_3']:.3f};{mm['meme_type_sur_10']:.3f};{mm['meme_type_sur_20']:.3f};"
                                  f"{mm['meme_sens_sur_20']:.3f}")
            autre = "mensuel" if ctx["reglages"]["pas_de_temps"] == "quotidien" else "quotidien"
            l2, c2 = dater(racine, {"pas_de_temps": autre})
            n, ds, dt = sens_differents(lignes, l2)
            print(f"PAS {autre.upper()} CONTRE {ctx['reglages']['pas_de_temps'].upper()} (affiché, pas décidé) : {ds} séances "
                  f"sur {n} changent de sens ({100 * ds / n:.1f} %), {dt} de type ; points au pas {autre} : {c2['points']} ; "
                  f"dernière phase : {l2[-1]['sens']} au pas {autre}, {lignes[-1]['sens']} au réglage du fichier")
            for recul in (250, 500, 1000, 2000):
                if recul < len(lignes):
                    l3, _ = dater(racine, jusqu_au=lignes[-1 - recul]["date"])
                    n, ds, dt = sens_differents(l3, lignes)
                    print(f"FIN DES DONNÉES {recul} séances plus tôt (jusqu'au {l3[-1]['date']}) : {ds} séances sur {n} "
                          f"changent de sens ({100 * ds / n:.1f} %), {dt} de type ({100 * dt / n:.1f} %)")
        if len(argv) > 3 and argv[2] == "ecrire":
            c = _module("CONTRATS_DES_FICHIERS")
            with open(argv[3], "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(c.TYPES_DE_MARCHE))
                w.writeheader(); w.writerows(lignes)
            print(f"écrit : {argv[3]}")
        if len(argv) > 4 and argv[2] == "figer":
            fiche = figer(racine, argv[3], argv[4])
            print(f"figé : {argv[4]} · {fiche['seances']} séances du {fiche['premiere_seance']} au {fiche['derniere_seance']} · "
                  f"empreinte de l'entrée {fiche['empreinte_entree']} · du CSV {fiche['empreinte_sortie']}")
        return 0
    except Exception as e:
        print(f"ÉCHEC : {type(e).__name__} : {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
