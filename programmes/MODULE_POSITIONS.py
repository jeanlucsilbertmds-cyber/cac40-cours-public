# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════
# MODULE POSITIONS — CAC 40 · gestion des positions simulées
# Transpose en Python la logique de la procédure de tenue des positions
# qui vivait dans un texte de consigne, remplacée par ce module le 11-08-2026.
# Le prompt devient minimal : il APPELLE ce module, il ne décrit plus.
# VERSION 1.0 — Mar 11-08-2026 23h05 (Paris).
# NOM FIXE : ce fichier ne sera jamais renommé ni horodaté, parce que d'autres
# programmes le chargent par son nom ; un nom qui change casse tous ses lecteurs
# en silence. (R-713)
# Simulations uniquement — aucun ordre réel.
#
# RÈGLES TRANSPOSÉES ICI. Elles venaient de trois endroits : une consigne en
# français appliquée à la main, la décision du 29-07-2026 sur les quatre tests de
# sortie (D-290726-01), et le module de la stratégie C5-étendu-10.
#  · Entrée à l'Open J+1 ; TP = entrée ×1,040 ; SL = entrée ×0,975 ;
#    horizon 20 séances de bourse après l'entrée.
#  · Clôture : 4 tests DANS CET ORDRE par séance (l'ouverture d'abord ;
#    ordre du 30-09-2026, R-607 ③ — avant, 2 et 3 étaient inversés) :
#      1. Open <= SL  → sortie à l'OUVERTURE, motif SL_GAP
#      2. Open >= TP  → sortie à l'OUVERTURE,  motif TP_GAP
#      3. Low  <= SL  → sortie au prix SL,     motif SL
#      4. High >= TP  → sortie au prix TP,     motif TP
#    Aucun déclenchement en 20 séances → sortie au Close, motif HORIZON.
#  · DEUX montants, toujours : le RÉEL (prix de sortie effectif) et la
#    CONVENTION du backtest (prix TP/SL théorique) — colonnes séparées.
#  · Frais : lus dans le barème daté `donnees/BAREME_FRAIS.csv` (A-550,
#    29-10-2026) — courtage Fortuneo Progress, 0,15 % de la VALEUR ÉCHANGÉE
#    (quantité × prix) à l'entrée ET à la sortie (décision de Jean-Luc du
#    11-08-2026, A-50), plus la taxe sur les transactions financières à l'achat
#    des valeurs taxées (0,3 % jusqu'au 31-03-2025, 0,4 % depuis), selon la liste
#    annuelle `donnees/VALEURS_TTF.csv`. Jamais de forfait pour un trade nouveau.
#  · Capital : 100 000 € par stratégie ; quantité fractionnaire.
# ══════════════════════════════════════════════════════════════

"""MODULE_POSITIONS.py — le moteur de calcul des positions simulées.

════════════════════════════════════════════════════════════════════════
LES ONZE ÉLÉMENTS — ce programme est une fonction comme les autres
════════════════════════════════════════════════════════════════════════
① RÔLE — **LE SEUL ENDROIT OÙ SE CALCULE CE QUE RAPPORTE UN TRADE.** Il ne
  décide rien : il applique les règles de sortie et chiffre le résultat.
  **C est l unique endroit où se calcule le coût d un ordre** (`cout_d_un_ordre`) :
  il le LIT dans le barème daté `donnees/BAREME_FRAIS.csv` et la liste des valeurs
  taxées `donnees/VALEURS_TTF.csv` ; tout autre programme l APPELLE, jamais ne
  recopie un taux (A-550).
② CONTEXTE D APPEL — Chargé par `programmes/TENIR_LES_POSITIONS.py`, qui lui
  demande deux choses : les frais d un ordre, et le verdict d une séance ; par le
  juge des stratégies (`jouer_une_entree`), qui lui demande la vente (`vendre`,
  depuis le 07-11-2026, lot ①a de J1) et les frais ; et, pour les frais, par le module de
  jugement (point mort), la mesure de la performance, le juge à huit critères et
  le module C5-ETENDU-10 (recalcul du radar).
  **Lancé seul, il ne fait que son calibrage.**
③ ENTRÉE — Aucune ligne de commande, sauf pour le calibrage. **Ce sont ses
  fonctions qui reçoivent : des prix, des séances, une valeur, des dates, et le
  nom d un barème quand on rejoue un montant ancien.**
④ CONDITIONS D ENTRÉE — Pour chiffrer des frais : `donnees/BAREME_FRAIS.csv` et
  `donnees/VALEURS_TTF.csv` existent et suivent leur contrat
  (`programmes/CONTRATS_DES_FICHIERS.py`), et `programmes/JUGE_DES_STRATEGIES.py`
  est à côté (sa clé des valeurs). Les fonctions de sortie (`tester_seance`,
  `seuils_de_vente`, `prix_de_convention`, `vendre`) ne lisent rien ; `vendre` importe
  `programmes/COMMUN.py` (la valeur « aucune durée »).
⑤ SORTIE — **Lancé seul : un code de sortie, 0 si le calibrage passe.**
  Utilisé comme module : ce que rendent ses fonctions publiques (neuf, listées au ⑥).
⑥ TRAITEMENT — Il expose cinq constantes (`CAPITAL`, `TP_PCT`, `SL_PCT`, `HORIZON`,
  `BAREME_PAR_DEFAUT`) et neuf fonctions publiques
  (`cout_d_un_ordre`, `valeur_taxee`, `frais_ordre`, `frais_aller_retour`, `pnl_net`,
  `seuils_de_vente`, `tester_seance`, `prix_de_convention`, `vendre`) ; `parametres_entree` et `sortie_position`
  sont retirées le 11-11-2026 (plan V7, bloc 4, accord de Jean-Luc du 08-11-2026 à 17h06, n°351 ; récupérables dans
  l'historique git). **Rien ne s exécute au chargement**, sinon la
  définition des constantes ; le barème est lu au premier calcul de frais.
⑦ UNITÉ — **`CAPITAL` en euros · `TP_PCT`, `SL_PCT` et les taux du barème en
  FRACTIONS, jamais en pourcents — 0,0015 vaut 0,15 %** · `HORIZON` en SÉANCES
  DE BOURSE, jamais en jours calendaires · les prix en euros · les dates en
  texte AAAA-MM-JJ.
⑧ POURQUOI — **Un seul endroit pour le coût d un ordre, et un barème DATÉ**,
  parce qu un chiffre recopié diverge et qu un taux unique ne dit pas la taxe, qui
  dépend de la valeur et de l année (ÉTUDE 18). **Et DEUX montants pour chaque trade** : le RÉEL, au prix de
  sortie effectif, et la CONVENTION, au prix théorique — **c est ce qui permet
  de comparer une opération vécue à un backtest sans confondre les deux.**
⑨ CE QUI CLOCHE — **Trois silences, aucun corrigé** — le ⑨ se consigne et ne se corrige pas (R-752) :
  · **`TP_PCT` et `SL_PCT` sont écrits ici en dur**, alors que les seuils
    viennent du registre `donnees/cac40_strategies.csv` par stratégie. **Deux
    sources pour la même grandeur** — `parametres_entree`, qui les employait, est
    retirée le 11-11-2026 : plus aucune fonction de ce fichier ne les lit, elles
    restent pour les programmes qui pourraient les lire (aucun au 11-11-2026, grep) ;
  · **`HORIZON = 20` est écrit ici ET passé par l appelant.** Le même chiffre
    vit à deux endroits ;
  · **aucun trade n a encore été clos sous le barème réel** : la taxe n est
    calibrée que sur des calculs à la main (400,00 € par achat taxé de 100 000 €),
    pas sur un montant vécu.
⑩ EFFET — **Il n écrit aucun fichier, ne sort pas sur le réseau, ne modifie
  rien.** Il LIT le barème et la liste des valeurs taxées au premier calcul de
  frais, et les garde en mémoire ; il CHARGE alors aussi
  `programmes/CONTRATS_DES_FICHIERS.py` (les colonnes attendues) et
  `programmes/JUGE_DES_STRATEGIES.py` (sa clé des valeurs).
⑪ TERMINAISON — **Chargé comme module : rien ne s exécute.** Lancé seul : il
  termine le programme, code 0 si le calibrage passe, 1 sinon.

⑫ DÉFINITIONS —
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub
    Actions — collecte, versement, signaux, positions, mesure, surveillance.
  la convention : le prix de sortie théorique, celui de l'objectif ou du stop, par opposition au prix réellement observé. C'est ce qui permet de comparer une opération vécue à un test sur le passé
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  un trade : une opération simulée, de l'achat à la revente
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""

CAPITAL = 100_000.0
TP_PCT  = 0.040
SL_PCT  = 0.025
HORIZON = 20          # séances de bourse après l'entrée

# LES FRAIS NE SONT PLUS UN TAUX ÉCRIT ICI (A-550, 29-10-2026). Ils se lisent dans
# un barème daté, `donnees/BAREME_FRAIS.csv` (courtage, taxe sur les transactions
# financières, régimes historiques nommés), et dans la liste annuelle des valeurs
# taxées, `donnees/VALEURS_TTF.csv`. Jusqu'au 29-10-2026, `FRAIS_TAUX = 0.0015` vivait
# ici : un taux unique, sans la taxe de 0,4 % à l'achat des valeurs françaises de plus
# d'un milliard d'euros (ÉTUDE 18, S1). Il a disparu : un taux recopié diverge (R-708).
# Le nom du barème appliqué quand l'appelant n'en donne aucun : celui des trades
# vécus aujourd'hui. Ce n'est pas un tarif, c'est un nom de ligne du fichier.
BAREME_PAR_DEFAUT = "REEL"
# LE BARÈME DES VERDICTS (superviseur R-759, tour 2, D2, 29-10-2026) : celui sous lequel se chiffrent les chiffres qui
# JUGENT une stratégie — le juge des stratégies (`jouer`, `jouer_une_entree`, `juger` : point mort et étalon de hasard),
# donc le juge à huit critères et la moulinette, et le point mort publié chaque soir par la mesure de la performance.
# DÉCISION DE JEAN-LUC DU 29-10-2026 À 19H16, recueillie par Cowork (`echanges/RELU.md`, commit ace1421) : à la
# question « Faire corriger l'étiquette, puis passer aux vrais frais ? », réponse « 1 ». L'étiquette d'abord (le verdict
# publié nomme le barème de son point mort, épreuve E17), PUIS les verdicts aux vrais frais : « REEL ». Raison donnée :
# les trades vécus paient déjà la taxe ; juger sans elle place la barre à 43,1 % au lieu de 49,2 % (objectif +4 %,
# perte acceptée −2,5 %, valeur taxée : 3 196,25 / (3 294 + 3 196,25)). Jusque-là, c'était « HIST_COURTAGE_SANS_TTF »,
# le régime d'avant la taxe. Le chiffre de la question, 49,2 %, était le « pire cas » de l'univers
# (`MODULE_JUGEMENT.point_mort_pire_cas` : la valeur la plus chère). DEPUIS LA DÉCISION DE JEAN-LUC DU 29-10-2026 (message
# reçu à 21h28, « A ») le point mort est la moyenne des opérations jouées, chacune à sa valeur et à sa date d'achat
# (`MODULE_JUGEMENT.point_mort_des_operations` : 48,70 % pour C5E10-QA-V1 rejouée). Revenir au courtage seul pour
# les verdicts : CETTE SEULE VALEUR ci-dessous.
# Les trades vécus se chiffrent toujours au barème réel (`BAREME_PAR_DEFAUT`) : ce sont de vrais frais, pas un jugement.
BAREME_DES_VERDICTS = "REEL"

_CACHE = {}


class FraisNonChiffrables(LookupError):
    """Les frais d'un ordre ne peuvent pas être chiffrés : la liste des valeurs taxées manque pour cette année ou cette valeur.

    ① RÔLE — Nommer UN cas, et un seul : la donnée de référence de la taxe manque
      (`donnees/VALEURS_TTF.csv` sans liste pour l'année, ou sans la valeur). C'est le
      seul cas qu'un appelant a le droit d'attraper pour continuer (une position laissée
      ouverte et dite, une stratégie non mesurée et dite) ; tout le reste continue de lever.
    ② CONTEXTE D'APPEL — Levée par `valeur_taxee` seulement. Attrapée par
      `programmes/TENIR_LES_POSITIONS.py` (`tenir`) et par
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py`.
    ③ ENTRÉE — Le message, qui nomme l'année et la valeur.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le superviseur R-759 du 29-10-2026 (C3, C7) : attraper `LookupError`
      avalerait aussi `KeyError` et `IndexError`, qui en sont des cas particuliers en
      Python, et une vraie faute de programmation passerait pour un « incident ». Le cas
      prévisible est janvier 2027 : la liste de l'année paraît au BOFiP vers le 20
      décembre (20-12-2023 pour 2024, 23-12-2024 pour 2025).
    ⑨ CE QUI CLOCHE — Hérite de `LookupError`, pour que les appelants qui attrapaient
      déjà `LookupError` restent justes ; un appelant qui attrape `LookupError` continue
      donc d'avaler les autres cas — à ne plus écrire.
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
      [sort: non]
    """


def _date_du_calendrier(date, quoi="date"):
    """Lit une date « AAAA-MM-JJ » et vérifie qu'elle existe au calendrier.

    ① RÔLE — Refuser une date mal écrite AVANT qu'elle ne soit comparée comme du texte.
    ② CONTEXTE D'APPEL — `cout_d_un_ordre` (la date de l'ordre, et les bornes `debut`
      et `fin` de chaque ligne du barème) ; `valeur_taxee`.
    ③ ENTRÉE — `date` : le texte · `quoi` : ce que c'est, pour le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la même date, en texte, inchangée.
      [rend: 1]
    ⑥ TRAITEMENT — ① forme exacte à dix caractères · ② lecture par le calendrier.
    ⑦ UNITÉ — Une date au format AAAA-MM-JJ.
    ⑧ POURQUOI — Le superviseur R-759 du 29-10-2026 (C11) : la forme seule acceptait
      « 2025-13-45 », qui, comparée comme du texte, tombe après « 2025-04-01 » et prend la
      taxe à 0,4 % sans rien dire ; une série datée « D030 » tombait hors de toutes les
      périodes et levait « aucune ligne de courtage », sans dire que la date était en cause.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` en nommant la date et ce qu'elle est.
      [sort: non]
    """
    import datetime, re
    if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise ValueError(f"{quoi} illisible : {date!r} (attendu AAAA-MM-JJ)")
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise ValueError(f"{quoi} absente du calendrier : {date!r}") from None
    return date


def _chemin_des_donnees(nom_du_fichier):
    """Rend le chemin d'un fichier du barème, dans le dépôt ou dans une copie à plat.

    ① RÔLE — Dire où lire le barème et la liste des valeurs taxées, sans que l'appelant
      ait à le savoir.
    ② CONTEXTE D'APPEL — `_lire_un_tableau`, à la première lecture de chaque fichier.
    ③ ENTRÉE — `nom_du_fichier` : son nom seul (« BAREME_FRAIS.csv »).
    ④ CONDITIONS D'ENTRÉE — Le fichier est dans `donnees/` à côté du dossier de ce
      programme (le dépôt, ses copies), ou dans le même dossier que ce programme (la
      copie à plat de `programmes/COPIER_POUR_LES_BOUCLES.py`, où chaque fichier de
      `COPIE_DES_BOUCLES` est posé sous son seul nom).
    ⑤ SORTIE — UNE valeur : le chemin absolu trouvé.
      [rend: 1]
    ⑥ TRAITEMENT — essayer `../donnees/<nom>` depuis le dossier de ce fichier, puis
      `<nom>` dans ce dossier ; rendre le premier qui existe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les copies du dépôt (épreuves, certification, dépôt public) gardent
      l'arborescence ; la copie à plat des boucles Cowork ne la garde pas.
    ⑨ CE QUI CLOCHE — Deux emplacements possibles : si les deux existent avec des
      contenus différents, le premier gagne sans rien dire.
    ⑩ EFFET — Regarde le disque ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `FileNotFoundError` en nommant les deux
      chemins essayés.
      [sort: non]
    """
    import os
    ici = os.path.dirname(os.path.abspath(__file__))
    essais = [os.path.join(os.path.dirname(ici), "donnees", nom_du_fichier), os.path.join(ici, nom_du_fichier)]
    for c in essais:
        if os.path.isfile(c):
            return c
    raise FileNotFoundError(f"{nom_du_fichier} introuvable : essayé " + " puis ".join(essais))


def _lire_un_tableau(nom_du_fichier, nom_du_contrat):
    """Lit un fichier de `donnees/` dont la première ligne est un commentaire, et le confronte à son contrat.

    ① RÔLE — Lire le barème des frais ou la liste des valeurs taxées, une fois, et
      refuser un fichier dont les colonnes ne sont pas celles que le contrat déclare.
    ② CONTEXTE D'APPEL — `_bareme` et `_valeurs_ttf`, à leur premier appel ; le
      résultat est gardé en mémoire (`_CACHE`) pour la durée du programme.
    ③ ENTRÉE — `nom_du_fichier` : le nom dans `donnees/` · `nom_du_contrat` : le nom
      de la liste de champs dans `programmes/CONTRATS_DES_FICHIERS.py`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe, en UTF-8 ; sa première ligne commence
      par « # » (le rôle du fichier), la deuxième est l'en-tête.
    ⑤ SORTIE — UNE valeur : la liste des lignes, chacune un dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le fichier · ② sauter la ligne de commentaire · ③ confronter
      l'en-tête au contrat, dans les deux sens (une colonne en trop ou en moins lève) ·
      ④ rendre les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ce qui se partage se déclare : le barème est écrit à la main et lu
      par ce module ; une colonne renommée ferait lire un taux vide comme un zéro.
    ⑨ CE QUI CLOCHE — Le contenu n'est pas contrôlé ici, seulement les colonnes : un
      taux faux mais lisible passe. Le calibrage (`_calibrage`) est ce qui le verrait.
    ⑩ EFFET — Lit un fichier ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `FileNotFoundError` si le fichier manque,
      `ValueError` si ses colonnes ne sont pas celles du contrat.
      [sort: non]
    """
    import csv, importlib.util, io, os
    cle = ("tableau", nom_du_fichier)
    if cle in _CACHE:
        return _CACHE[cle]
    chemin = _chemin_des_donnees(nom_du_fichier)
    with open(chemin, encoding="utf-8-sig") as f:
        texte = f.read()
    lignes_texte = texte.splitlines()
    if not lignes_texte or not lignes_texte[0].startswith("#"):
        raise ValueError(f"{chemin} : la première ligne doit être le commentaire « # … » qui dit le rôle du fichier")
    lecteur = csv.DictReader(io.StringIO("\n".join(lignes_texte[1:])))
    champs = list(lecteur.fieldnames or [])
    sp = importlib.util.spec_from_file_location(
        "_contrats_frais", os.path.join(os.path.dirname(os.path.abspath(__file__)), "CONTRATS_DES_FICHIERS.py"))
    contrats = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(contrats)
    ecarts = contrats.verifier(nom_du_contrat, champs, "ECRIT")
    if ecarts:
        raise ValueError(f"{chemin} ne suit pas son contrat : " + " · ".join(ecarts))
    lignes = list(lecteur)
    _CACHE[cle] = lignes
    return lignes


def _cle_des_valeurs():
    """Rend la fonction `cle_valeur` DU JUGE DES STRATÉGIES, jamais une copie.

    ① RÔLE — Rapprocher les graphies d'une valeur (« UNIBAIL-RODAMCO-WESTFIELD »,
      « UNIBAIL_RODAMCO ») pour la retrouver dans la liste des valeurs taxées.
    ② CONTEXTE D'APPEL — `valeur_taxee`, au premier besoin ; gardée en mémoire.
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D'ENTRÉE — `programmes/JUGE_DES_STRATEGIES.py` est à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : la fonction `cle_valeur` du juge.
      [rend: 1]
    ⑥ TRAITEMENT — charger le juge depuis le dossier de ce fichier et y prendre la fonction.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux implémentations d'une même chose divergent toujours (R-708) : le
      teneur de positions importe déjà cette fonction de la même façon
      (`cle_valeur_du_banc`) ; une copie ici serait une troisième graphie possible.
    ⑨ CE QUI CLOCHE — D'autres programmes portent encore leur propre `cle_valeur`
      (`programmes/TENIR_L_HISTORIQUE.py`), relevé le 29-10-2026 : défaut ancien, hors
      de ce travail.
    ⑩ EFFET — Charge un programme ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `FileNotFoundError` si le juge est absent.
      [sort: non]
    """
    import importlib.util, os
    if "cle" in _CACHE:
        return _CACHE["cle"]
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "JUGE_DES_STRATEGIES.py")
    if not os.path.isfile(chemin):
        raise FileNotFoundError(f"{chemin} introuvable : la clé des valeurs ne se recopie pas (R-708)")
    sp = importlib.util.spec_from_file_location("_juge_pour_les_frais", chemin)
    juge = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(juge)
    _CACHE["cle"] = juge.cle_valeur
    return juge.cle_valeur


def valeur_taxee(valeur, date):
    """Dit si l'achat d'une valeur, à une date, paie la taxe sur les transactions financières.

    ① RÔLE — Lire la liste annuelle des valeurs taxées (`donnees/VALEURS_TTF.csv`) pour
      une valeur et l'année d'une date.
    ② CONTEXTE D'APPEL — `cout_d_un_ordre`, à chaque achat d'action quand le barème
      porte une ligne de taxe applicable à la date.
    ③ ENTRÉE — `valeur` : son mnémonique (« URW ») ou son nom, sous n'importe quelle
      graphie que la clé du juge rapproche (« UNIBAIL-RODAMCO-WESTFIELD »,
      « UNIBAIL_RODAMCO ») · `date` : « AAAA-MM-JJ ».
    ④ CONDITIONS D'ENTRÉE — L'année de la date a sa liste dans le fichier (2024, 2025 et
      2026 au 29-10-2026), et la valeur y figure. La date existe au calendrier.
    ⑤ SORTIE — UNE valeur : vrai si la valeur est taxée cette année-là, faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre l'année de la date · ② chercher la valeur dans les lignes
      de cette année, par mnémonique puis par nom rapproché · ③ lire la colonne
      `assujettie` (OUI ou NON).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La liste change chaque année (publiée au BOFiP en décembre pour l'année
      suivante) : un drapeau écrit une fois pour toutes serait faux un an plus tard.
      Exemple : Bureau Veritas (BVI) est taxée en 2026, Airbus (AIR) ne l'est pas.
    ⑨ CE QUI CLOCHE — Une année sans liste lève au lieu de supposer : un juge qui
      rejoue 2000-2023 avec le barème réel s'arrête donc (la taxe existe depuis 2012, et
      les listes d'avant 2024 ne sont pas relevées). C'est voulu : supposer zéro ferait
      un chiffre faux et plausible.
    ⑩ EFFET — Lit un fichier au premier appel ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur une date illisible ou absente
      du calendrier, `FraisNonChiffrables` (un cas de `LookupError`) si l'année n'a pas de
      liste ou si la valeur n'y est pas, `ValueError` si la colonne `assujettie` ne vaut
      ni OUI ni NON.
      [sort: non]
    """
    _date_du_calendrier(date, "date de l'ordre, pour la taxe")
    annee = date[:4]
    lignes = [l for l in _lire_un_tableau("VALEURS_TTF.csv", "VALEURS_TTF") if l["annee"] == annee]
    if not lignes:
        raise FraisNonChiffrables(f"donnees/VALEURS_TTF.csv ne porte aucune liste pour {annee} : "
                          f"on ne sait pas quelles valeurs sont taxées cette année-là")
    cle = _cle_des_valeurs()
    v = str(valeur).strip()
    trouvees = [l for l in lignes if l["mnemonique"].strip().upper() == v.upper()]
    if not trouvees:
        trouvees = [l for l in lignes if cle(l["nom_usuel"]) == cle(v)]
    if len(trouvees) != 1:
        raise FraisNonChiffrables(f"donnees/VALEURS_TTF.csv : {len(trouvees)} ligne(s) pour {valeur!r} en {annee} "
                          f"(une exactement est attendue)")
    drapeau = trouvees[0]["assujettie"].strip().upper()
    if drapeau not in ("OUI", "NON"):
        raise ValueError(f"donnees/VALEURS_TTF.csv : assujettie = {drapeau!r} pour {valeur!r} en {annee}")
    return drapeau == "OUI"


def _nombre(texte):
    """Lit un nombre du barème ; une case vide rend `None`.

    ① RÔLE — Convertir une case du barème en nombre, sans confondre « vide » et « zéro ».
    ② CONTEXTE D'APPEL — `cout_d_un_ordre`, pour les taux, montants et seuils.
    ③ ENTRÉE — `texte` : le contenu de la case.
    ④ CONDITIONS D'ENTRÉE — Un nombre écrit avec un point décimal, ou rien.
    ⑤ SORTIE — UNE valeur : le nombre, ou `None` si la case est vide.
      [rend: 1]
    ⑥ TRAITEMENT — enlever les espaces ; vide → `None` ; sinon convertir.
    ⑦ UNITÉ — Celle de la colonne : fraction pour un taux, euros pour un montant.
    ⑧ POURQUOI — Une case vide veut dire « sans objet » (pas de seuil, pas de date) ;
      la lire comme zéro ferait un seuil à 0 € ou une taxe nulle.
    ⑨ CE QUI CLOCHE — Une virgule décimale lève : le barème est écrit avec des points.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur un texte qui n'est pas un nombre.
      [sort: non]
    """
    t = (texte or "").strip()
    return None if t == "" else float(t)


def _instrument_couvert(colonne, instrument):
    """Dit si une ligne du barème vaut pour un instrument.

    ① RÔLE — Appliquer la colonne `instrument` du barème.
    ② CONTEXTE D'APPEL — `cout_d_un_ordre`, pour chaque ligne.
    ③ ENTRÉE — `colonne` : la case (« action », « etf », « action_et_etf »,
      « etf:<ISIN> ») · `instrument` : « action », « etf » ou « etf:<ISIN> ».
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — « action_et_etf » couvre tout ; « etf » couvre tout fonds coté ;
      « etf:<ISIN> » ne couvre que ce fonds ; « action » ne couvre que les actions.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La taxe vise les actions, pas les fonds cotés (BOFiP, § 25, relevé au
      barème) ; le courtage vaut pour les deux.
    ⑨ CE QUI CLOCHE — Une case inconnue ne couvre rien, et le coût lève alors faute de
      courtage : c'est l'alerte voulue.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    c = (colonne or "").strip()
    i = (instrument or "").strip()
    if c == "action_et_etf":
        return i == "action" or i == "etf" or i.startswith("etf:")
    if c == "etf":
        return i == "etf" or i.startswith("etf:")
    return c == i


def cout_d_un_ordre(valeur, date, sens, montant, bareme=None, instrument="action"):
    """Ce que coûte UN ordre : le courtage et la taxe, séparément, lus dans le barème daté.

    ① RÔLE — **LE SEUL ENDROIT OÙ SE CALCULE LE COÛT D'UN ORDRE** (A-550, ÉTUDE 18, A2).
      Tout programme qui chiffre des frais passe par ici, directement ou par
      `frais_ordre`.
    ② CONTEXTE D'APPEL — `frais_ordre` (le teneur de positions, le juge des stratégies,
      le point mort) ; le calibrage de ce module.
    ③ ENTRÉE — `valeur` : mnémonique ou nom · `date` : « AAAA-MM-JJ », le jour de
      l'ordre · `sens` : « achat » ou « vente » · `montant` : la valeur échangée,
      quantité × prix · `bareme` : le nom d'une ligne de `donnees/BAREME_FRAIS.csv`,
      `None` pour le barème des trades vécus (« REEL ») ; un autre nom sert à rejouer un
      montant ancien sous le régime qui l'a produit (« HIST_COURTAGE_SANS_TTF »,
      « HIST_FORFAIT_300 ») · `instrument` : « action » par défaut, « etf » ou
      « etf:<ISIN> » pour un fonds coté.
    ④ CONDITIONS D'ENTRÉE — Le barème nommé existe ; pour la date, l'instrument, le
      sens et le montant, EXACTEMENT une ligne de courtage (ou de forfait) s'applique,
      et au plus une ligne de taxe.
    ⑤ SORTIE — UNE valeur : un dictionnaire de TROIS clés — `courtage`, `taxe` (en
      euros) et `bareme` (le nom appliqué).
      [rend: 1]
    ⑥ TRAITEMENT — ① garder les lignes du barème nommé qui couvrent l'instrument, le
      sens et la date, et dont les seuils encadrent le montant arrondi au centime ·
      ② courtage : la ligne de courtage (taux × montant, ou montant fixe) ; un forfait
      « aller_retour » se partage par moitié entre l'achat et la vente · ③ taxe : la
      ligne de taxe, appliquée à une action seulement si `valeur_taxee` le dit pour
      l'année de la date ; un fonds coté prend le taux de sa ligne (zéro) sans liste ·
      ④ les frais de gestion annuels d'un fonds ne sont pas un coût d'ordre : ignorés.
    ⑦ UNITÉ — **`montant` et le résultat en EUROS ; les taux du barème en FRACTIONS**
      (0,0015 vaut 0,15 %) ; les dates en texte AAAA-MM-JJ, vérifiées au calendrier
      (`_date_du_calendrier`) puis comparées comme du texte, ce qui est exact pour des
      dates valides de cette forme.
    ⑧ POURQUOI — Le coût dépend de la valeur et de la date, un taux unique ne peut pas
      le dire (ÉTUDE 18, § 5). Exemple : achat de 100 000 € de Bureau Veritas le
      27-07-2026 — 150,00 € de courtage et 400,00 € de taxe ; même achat d'Airbus —
      150,00 € et 0,00 €.
    ⑨ CE QUI CLOCHE — ① (RÉGLÉ LE 29-10-2026, C11 : la date de l'ordre et les bornes
      du barème sont vérifiées au calendrier avant d'être comparées.) ② Le courtage minimal de 4,90 € et le taux de 0,15 %
      se départagent au centime (3 000,00 € contre 3 000,01 €) : un montant non arrondi
      entre les deux est arrondi d'abord. ③ La promotion sur les fonds Amundi
      (PROMO_ETF_AMUNDI) n'a qu'une ligne d'achat : la nommer pour une vente lève.
      ④ `instrument` n'est transmis par AUCUN appelant du circuit : tous chiffrent une
      action. Une stratégie sur un fonds coté serait taxée comme une action, ou lèverait
      faute de la valeur dans la liste — défaut latent et bruyant (C13 du relecteur T1,
      29-10-2026), au BACKLOG.
    ⑩ EFFET — Lit deux fichiers au premier appel ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` (date illisible ou absente du
      calendrier, barème inconnu, sens inconnu, montant négatif, nature inconnue, zéro ou
      plusieurs courtages, plusieurs taxes) et `FraisNonChiffrables` (valeur ou année
      absente de la liste des valeurs taxées).
      [sort: non]
    """
    nom = BAREME_PAR_DEFAUT if bareme is None else bareme
    _date_du_calendrier(date, "date de l'ordre")
    if sens not in ("achat", "vente"):
        raise ValueError(f"sens d'un ordre : « achat » ou « vente », pas {sens!r}")
    m = round(float(montant), 2)
    if m < 0:
        raise ValueError(f"valeur échangée négative : {montant!r}")
    toutes = _lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS")
    lignes = [l for l in toutes if l["nom_bareme"] == nom]
    if not lignes:
        raise ValueError(f"barème inconnu : {nom!r} (donnees/BAREME_FRAIS.csv)")
    courtages, taxes = [], []
    for l in lignes:
        if not _instrument_couvert(l["instrument"], instrument):
            continue
        cote = l["sens"].strip()
        if cote not in ("achat_et_vente", "aller_retour", "detention", sens):
            continue
        debut, fin = l["debut"].strip(), l["fin"].strip()
        if debut:
            _date_du_calendrier(debut, f"début d'une ligne du barème {nom!r}")
        if fin:
            _date_du_calendrier(fin, f"fin d'une ligne du barème {nom!r}")
        if (debut and date < debut) or (fin and date > fin):
            continue
        bas, haut = _nombre(l["valeur_ordre_min_eur"]), _nombre(l["valeur_ordre_max_eur"])
        if (bas is not None and m < bas) or (haut is not None and m > haut):
            continue
        nature = l["nature"].strip()
        taux, fixe = _nombre(l["taux_fraction"]), _nombre(l["montant_eur"])
        if nature == "frais_gestion_annuels":
            continue
        if cote == "detention":
            raise ValueError(f"ligne « {nature} » au sens « detention » : ce n'est pas un coût d'ordre")
        if nature in ("courtage", "forfait"):
            part = (taux * m) if taux is not None else fixe
            if part is None:
                raise ValueError(f"ligne de {nature} sans taux ni montant dans le barème {nom!r}")
            courtages.append(part / 2.0 if cote == "aller_retour" else part)
        elif nature == "ttf":
            taxes.append(taux if taux is not None else 0.0)
        else:
            raise ValueError(f"nature inconnue dans le barème {nom!r} : {nature!r}")
    if len(courtages) != 1:
        raise ValueError(f"barème {nom!r}, {instrument} {sens} de {m:.2f} € le {date} : "
                         f"{len(courtages)} ligne(s) de courtage s'appliquent, une exactement est attendue")
    if len(taxes) > 1:
        raise ValueError(f"barème {nom!r}, {sens} le {date} : {len(taxes)} lignes de taxe s'appliquent")
    taxe = 0.0
    if taxes:
        if instrument == "action":
            if valeur_taxee(valeur, date):
                taxe = taxes[0] * m
        else:
            taxe = taxes[0] * m
    return {"courtage": courtages[0], "taxe": taxe, "bareme": nom}


def frais_ordre(quantite, prix, valeur, date, sens, bareme=None, instrument="action"):
    """Frais d'UN ordre, en euros : courtage + taxe, lus dans le barème daté.

    ① RÔLE — **Chiffrer ce que coûte UN passage d'ordre.** Appelée deux fois par
      trade : à l'achat et à la vente.
    ② CONTEXTE D'APPEL — `pnl_net` ; `programmes/TENIR_LES_POSITIONS.py`, à la clôture
      d'une position ; `programmes/JUGE_DES_STRATEGIES.py` (`jouer_une_entree`) ;
      `programmes/MODULE_JUGEMENT.py` (point mort). **Le teneur de positions l'exige à
      l'import** : sans elle, il refuse de charger ce module.
    ③ ENTRÉE — `quantite` : le nombre de titres · `prix` : le prix unitaire ·
      `valeur`, `date`, `sens`, `bareme`, `instrument` : ceux de `cout_d_un_ordre`.
    ④ CONDITIONS D'ENTRÉE — Celles de `cout_d_un_ordre`.
    ⑤ SORTIE — UNE valeur : le montant des frais.
      [rend: 1]
    ⑥ TRAITEMENT — ① la valeur échangée est quantité × prix · ② `cout_d_un_ordre` en
      donne le courtage et la taxe · ③ rendre leur somme.
    ⑦ UNITÉ — **`quantite` en titres, `prix` et le résultat en EUROS.**
    ⑧ POURQUOI — **Les frais portent sur la VALEUR ÉCHANGÉE et dépendent de la valeur
      et de la date** (la taxe). Jusqu'au 29-10-2026 elle prenait un taux, 0,0015 ; ce
      paramètre a disparu : choisir un régime se fait par le NOM d'un barème, jamais
      par un chiffre (A-550, garde-fou A4).
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Lit deux fichiers au premier appel ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève ce que `cout_d_un_ordre` lève.
      [sort: non]
    """
    c = cout_d_un_ordre(valeur, date, sens, quantite * prix, bareme, instrument)
    return c["courtage"] + c["taxe"]


def frais_aller_retour(quantite, prix_achat, prix_vente, valeur, date_achat, date_vente, bareme=None,
                       instrument="action"):
    """Frais d'UN aller-retour, en euros : l'achat et la vente, l'exonération du jour même comprise.

    ① RÔLE — **LE SEUL ENDROIT OÙ S'ASSEMBLE LE COÛT D'UN ALLER-RETOUR** (superviseur
      R-759, C10, 29-10-2026). Tout programme qui chiffre un trade passe par ici.
    ② CONTEXTE D'APPEL — `pnl_net` ; `programmes/TENIR_LES_POSITIONS.py` (`cloturer`,
      prix réel et prix de convention) ; `programmes/JUGE_DES_STRATEGIES.py`
      (`jouer_une_entree`) ; `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py`
      (`_c5e10_sortie`) ; le calibrage du pont de `programmes/JUGER_SUR_8_CRITERES.py`.
    ③ ENTRÉE — `quantite` : le nombre de titres, le même à l'achat et à la vente ·
      `prix_achat`, `prix_vente` · `valeur` · `date_achat`, `date_vente` : le jour de
      chaque ordre · `bareme`, `instrument` : ceux de `cout_d_un_ordre`.
    ④ CONDITIONS D'ENTRÉE — Celles de `cout_d_un_ordre`, pour chacun des deux ordres.
    ⑤ SORTIE — UNE valeur : un dictionnaire de QUATRE clés, en euros — `achat` (frais
      de l'ordre d'achat), `vente`, `total`, et `taxe_exoneree` (la taxe que l'achat
      aurait payée s'il n'avait pas été revendu le jour même, 0 sinon).
      [rend: 1]
    ⑥ TRAITEMENT — ① chiffrer l'achat et la vente par `cout_d_un_ordre`, chacun à son
      jour · ② si l'achat et la vente tombent le même jour, retirer la taxe de l'achat ·
      ③ additionner.
    ⑦ UNITÉ — **EUROS.** `quantite` en titres.
    ⑧ POURQUOI — La taxe frappe le SOLDE NET des acquisitions en fin de journée : « Seul
      le solde net des acquisitions en fin de journée est dans ce cas soumis à la taxe »
      (BOFiP, BOI-TCA-FIN-10-10-20151221, § 60, lu le 29-10-2026). Un titre acheté puis
      revendu le même jour laisse un solde nul : pas de taxe. Le cas existe ici : les
      seuils sont testés dès la séance d'achat, et un objectif atteint le jour même
      revend le jour même. Exemple : 100 000 € de Bureau Veritas achetés à l'ouverture
      du 27-07-2026 et revendus le même jour — 150,00 € + 156,00 € de courtage, 0 € de
      taxe ; revendus le lendemain — 400,00 € de taxe en plus. L'exonération porte sur
      l'aller-retour, pas sur un ordre : la mettre dans un seul appelant aurait laissé
      les autres taxer (deux implémentations divergent toujours, R-708).
    ⑨ CE QUI CLOCHE — L'exonération suppose que TOUT ce qui a été acheté est revendu le
      jour même, ce qui est le cas ici (capital entier, revente entière). Une revente
      partielle n'existe pas dans ce système ; elle demanderait de taxer le solde.
    ⑩ EFFET — Lit deux fichiers au premier appel ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève ce que `cout_d_un_ordre` lève.
      [sort: non]
    """
    a = cout_d_un_ordre(valeur, date_achat, "achat", quantite * prix_achat, bareme, instrument)
    v = cout_d_un_ordre(valeur, date_vente, "vente", quantite * prix_vente, bareme, instrument)
    exoneree = a["taxe"] if date_achat == date_vente else 0.0
    f_achat = a["courtage"] + a["taxe"] - exoneree
    f_vente = v["courtage"] + v["taxe"]
    return {"achat": f_achat, "vente": f_vente, "total": f_achat + f_vente, "taxe_exoneree": exoneree}


def pnl_net(prix_entree, prix_sortie, valeur, date_entree, date_sortie, bareme=None, instrument="action"):
    """P&L net d'un aller-retour au capital fixe, frais des deux ordres déduits.

    ① RÔLE — **Chiffrer ce qu'un trade a rapporté ou coûté, frais déduits.**
    ② CONTEXTE D'APPEL — Le calibrage de ce module ; `sortie_position`, qui l'appelait
      deux fois par sortie, est retirée le 11-11-2026 (plan V7, bloc 4).
    ③ ENTRÉE — `prix_entree` · `prix_sortie` · `valeur` · `date_entree` : le jour de
      l'achat · `date_sortie` : le jour de la vente · `bareme` · `instrument` : ceux de
      `cout_d_un_ordre`.
    ④ CONDITIONS D'ENTRÉE — **`prix_entree` ne doit pas être nul** : il est au
      dénominateur.
    ⑤ SORTIE — UNE valeur : le résultat net.
      [rend: 1]
    ⑥ TRAITEMENT — ① la quantité est `CAPITAL` divisé par le prix d'entrée, **et elle
      est fractionnaire** · ② le brut est la variation relative appliquée au capital ·
      ③ retrancher les frais de l'aller-retour, par `frais_aller_retour` (chaque ordre à
      son jour ; pas de taxe sur un achat revendu le jour même).
    ⑦ UNITÉ — **Prix et résultat en EUROS, quantité en titres.**
    ⑧ POURQUOI — **Capital fixe de 100 000 € par trade, quantité fractionnaire.** Cela
      rend deux trades comparables quel que soit le prix de la valeur.
    ⑨ CE QUI CLOCHE — **Une division par `prix_entree` sans garde.** Un prix nul lève.
    ⑩ EFFET — Lit deux fichiers au premier appel ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main. **Lève si `prix_entree` vaut zéro**, et ce que
      `cout_d_un_ordre` lève.
      [sort: non]
    """
    q = CAPITAL / prix_entree
    brut = CAPITAL * (prix_sortie / prix_entree - 1.0)
    return brut - frais_aller_retour(q, prix_entree, prix_sortie, valeur, date_entree, date_sortie,
                                     bareme, instrument)["total"]


def tester_seance(bar, tp, sl):
    """Applique les quatre tests de sortie décidés le 29-07-2026 (D-290726-01), dans l ordre fixé le 30-09-2026 par R-607 ③, sur UNE séance.
    bar = dict open/high/low/close. Retourne (prix_sortie, motif) ou None.

    ① RÔLE — **Dire si une position sort ce jour-là, et à quel prix.** C est le
      grain le plus fin du moteur.
    ② CONTEXTE D APPEL — `vendre` (la vente du juge et du soir depuis le
      11-11-2026 ; le radar garde son recalcul indépendant, A-208 ⑤), une fois par séance de détention.
      **Et `programmes/TENIR_LES_POSITIONS.py` l exige à l import.**
    ③ ENTRÉE — `bar` : une séance, avec ses quatre prix · `tp` : l objectif ·
      `sl` : le stop.
    ④ CONDITIONS D ENTRÉE — **`bar` DOIT porter les quatre clés** `open`, `high`,
      `low`, `close`. Une clé absente lève.
    ⑤ SORTIE — **DEUX formes selon la branche** : **DEUX valeurs** — le prix de
      sortie et le motif — quand un seuil est touché · **1 valeur, `None`**,
      quand la position reste ouverte.
      **Selon la branche, elle rend 1 ou 2 valeur(s).**
      [rend: 1 ou 2]
⑥ TRAITEMENT — **Quatre tests DANS CET ORDRE, et l ordre fait le résultat** :
      ① ouverture sous le stop, sortie à l ouverture · ② ouverture au-dessus de
      l objectif, sortie à l ouverture · ③ plus bas sous le stop, sortie au stop ·
      ④ plus haut au-dessus de l objectif, sortie à l objectif. (Ordre du
      30-09-2026 ; avant, ② et ③ étaient inversés.)
    ⑦ UNITÉ — Tous les prix en euros.
    ⑧ POURQUOI — **Les deux sauts d ouverture sont testés AVANT les extrêmes de
      la séance**, parce qu un saut d ouverture s exécute au prix réel et non au
      seuil, et que l ouverture est le premier prix de la séance : une séance qui
      ouvre au-dessus de l objectif puis descend sous le stop a vendu à
      l ouverture, en gain (R-607 ③, décision de Jean-Luc du 27-09-2026 à 16h14,
      exception à R-602). **Sans saut, le stop est testé avant l objectif : dans
      une séance qui touche les deux, on suppose le pire (R-602).**
    ⑨ CE QUI CLOCHE — **L ordre des quatre tests porte tout le sens.** Depuis le
      30-09-2026, `tests/EPREUVES_DE_L_ORDRE_DES_SORTIES_Mer_30-09-2026.py` joue
      sept cas et rougit si l ordre change ; le calibrage du module, lui, ne
      teste qu un saut à la hausse. **Le prix de convention n est pas rendu ici** :
      le programme du soir le déduit du motif (TP… donne l objectif), si bien que
      dans le cas « ouverture au-dessus de l objectif puis plus bas sous le stop »
      il écrit l objectif, quand le backtest (`_c5e10_sortie`, qui teste le plus
      bas d abord) retient le stop — le contrôle n°10 du radar verrait un écart
      sur un tel trade. Aucun trade du passé n est dans ce cas. Consigné au
      BACKLOG le 30-09-2026 (A-506), non réparé : le prix de convention et le contrôle
      n°10 relèvent de A-501, mis en attente par Jean-Luc.
    ⑩ EFFET — Aucun : elle ne modifie pas la séance reçue.
    ⑪ TERMINAISON — Rend la main. **Lève si une clé de prix manque.**
      [sort: non]
    """
    # LES DEUX SAUTS D'OUVERTURE D'ABORD (R-607 ③, décision de Jean-Luc du
    # 27-09-2026 à 16h14) : l'ouverture est le premier prix de la séance ; une
    # séance qui ouvre au-dessus de l'objectif puis descend sous la vente forcée
    # a vendu à l'ouverture, avant la baisse — c'est un gain. Avant le 30-09-2026,
    # le plus bas sous la vente forcée était testé avant le saut favorable, et ce
    # cas comptait une perte.
    if bar["open"] <= sl:
        return bar["open"], "SL_GAP"
    if bar["open"] >= tp:
        return bar["open"], "TP_GAP"
    # SANS SAUT, LE PIRE D'ABORD (R-602, inchangée) : dans une séance qui touche
    # les deux seuils, on ne sait pas lequel est venu en premier.
    if bar["low"] <= sl:
        return sl, "SL"
    if bar["high"] >= tp:
        return tp, "TP"
    return None


def _horizon_aucune():
    """Rend la valeur HORIZON_AUCUNE de `programmes/COMMUN.py`, chargée une seule fois.

    ① RÔLE — Donner à `vendre` la valeur qui dit « aucune durée maximale », sans la recopier (R-708).
    ② CONTEXTE D'APPEL — `vendre`, à chaque appel.
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D'ENTRÉE — `programmes/COMMUN.py` est à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : l'objet `COMMUN.HORIZON_AUCUNE`.
      [rend: 1]
    ⑥ TRAITEMENT — ① mettre le dossier de ce fichier dans le chemin d'import s'il n'y est pas · ② importer
      COMMUN par son nom, pour que Python rende le module déjà chargé par l'appelant.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ce module est chargé par son chemin sous plusieurs noms (`_mp_frais` par le module C5, `positions`
      par l'épreuve à vérité connue) : l'import par le NOM « COMMUN » rend le même objet que celui du juge et du
      programme du soir, et c'est cet objet que `vendre` reconnaît par `is` (contrat du lot 0).
    ⑨ CE QUI CLOCHE — Un programme qui chargerait COMMUN par son chemin sous un autre nom aurait une seconde valeur,
      que `vendre` ne reconnaîtrait pas : elle tomberait sur le refus d'un horizon non entier (ValueError), jamais
      sur un calcul faux. Aucun programme ne le fait au 11-11-2026 (grep « spec_from_file_location » sur COMMUN :
      aucun).
    ⑩ EFFET — Peut ajouter un dossier au chemin d'import de Python.
    ⑪ TERMINAISON — Rend la main ; lève ImportError si COMMUN manque.
      [sort: non]
    """
    import os as _os, sys as _sys
    _ici = _os.path.dirname(_os.path.abspath(__file__))
    if _ici not in _sys.path:
        _sys.path.append(_ici)
    import COMMUN
    return COMMUN.HORIZON_AUCUNE


def seuils_de_vente(prix_entree, tp, sl):
    """Rend l'objectif et le stop, en euros, d'un achat fait à `prix_entree` : LE seul calcul des deux seuils.

    ① RÔLE — Poser les deux prix de sortie d'une position à partir de son prix d'achat et des seuils de SA
      stratégie, arrondis à cinq décimales, pour tout le dépôt.
    ② CONTEXTE D'APPEL — `vendre` (le juge, l'étalon de hasard, la moulinette, qui passent des fractions) ;
      `programmes/TENIR_LES_POSITIONS.py`, `entrer`, qui écrit ces deux prix dans la position le soir de l'achat.
    ③ ENTRÉE — `prix_entree` : le prix d'achat en euros · `tp`, `sl` : l'objectif et la perte acceptée en
      FRACTIONS positives du prix d'achat (0.04 et 0.025 pour « +4 % » et « −2,5 % »).
    ④ CONDITIONS D'ENTRÉE — Trois nombres ; les seuils sont lus et validés par l'appelant (le juge par
      `seuil_de_la_fiche`, le soir par `reglages_du_registre`, qui l'emprunte au juge).
    ⑤ SORTIE — DEUX valeurs : l'objectif, puis le stop, en euros, chacun arrondi à cinq décimales.
      [rend: 2]
    ⑥ TRAITEMENT — ① objectif = prix × (1 + tp) · ② stop = prix × (1 − sl) · ③ chacun arrondi à cinq décimales
      par l'écriture « %.5f », celle que le programme du soir emploie pour écrire la position.
    ⑦ UNITÉ — Euros en entrée et en sortie ; seuils en FRACTIONS.
    ⑧ POURQUOI — DÉCISION DE JEAN-LUC DU 07-11-2026 À 15H49 (n°311, « 1 ») : « arrondi à 5 décimales partout pour
      comparer le prix à l'objectif et au stop, comme le circuit du soir le fait déjà. Le juge et le radar s'alignent
      sur le soir. » Exemple réel qui l'a motivée : ENGIE achetée le 17-06-2024 à 13,25, objectif brut
      13,780000000000001 ; le plus haut du 21-06 vaut 13,78 ; sans arrondi le juge ne vendait que le 24-06, le soir
      vendait le 21-06. Deux implémentations d'une même chose divergent toujours (R-708) : le calcul vivait dans
      `vendre` (brut), dans `entrer` du soir (arrondi à l'écriture) et dans le radar (brut ; le radar le garde, son
      recalcul restant INDÉPENDANT par décision de Jean-Luc, BACKLOG A-208 ⑤).
    ⑨ CE QUI CLOCHE — « %.5f » arrondit la valeur binaire exacte au plus proche ; une valeur tombant exactement sur
      la moitié du dernier chiffre est arrondie au pair. Le soir faisait de même : les deux restent identiques.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; aucun appel.
      [sort: non]
    """
    return float("%.5f" % (prix_entree * (1.0 + tp))), float("%.5f" % (prix_entree * (1.0 - sl)))


def prix_de_convention(motif, prix_sortie, objectif, stop):
    """Rend le prix de sortie « de convention » d'une vente : le seuil touché, jamais le prix d'un saut d'ouverture.

    ① RÔLE — Le seul calcul du prix de convention, celui qu'un test sur le passé suppose (R-602).
    ② CONTEXTE D'APPEL — `programmes/TENIR_LES_POSITIONS.py`, `cloturer` (le montant de convention du journal). Le
      radar ne l'appelle pas : son recalcul reste indépendant (BACKLOG A-208 ⑤, décision de Jean-Luc du 14-08-2026).
    ③ ENTRÉE — `motif` : celui que rend `vendre` (`SL_GAP`, `TP_GAP`, `SL`, `TP`, `HORIZON`) · `prix_sortie` : le
      prix réel que rend `vendre` · `objectif`, `stop` : les deux seuils en euros que rend `vendre`.
    ④ CONDITIONS D'ENTRÉE — Le motif est l'un des cinq.
    ⑤ SORTIE — UNE valeur : le stop pour un motif qui commence par « SL », l'objectif pour un motif qui commence par
      « TP », le prix réel sinon (l'échéance).
      [rend: 1]
    ⑥ TRAITEMENT — Lire la première lettre du motif.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — Deux prix sont écrits pour chaque sortie (R-602) : le réel tient compte du saut d'ouverture, la
      convention suppose une exécution au seuil exact. Le calcul vivait dans `cloturer` et dans
      `sortie_position` (retirée le 11-11-2026), et le radar en avait une troisième forme qui ne regardait jamais
      l'ouverture : une séance ouverte au-dessus de l'objectif puis passée sous le stop y comptait le stop (A-506).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; lève AttributeError si le motif n'est pas un texte.
      [sort: non]
    """
    if motif.startswith("SL"):
        return stop
    if motif.startswith("TP"):
        return objectif
    return prix_sortie


def vendre(serie, j, vente, fin_des_donnees):
    """Dit quand et à quel prix se revend un achat fait à l'ouverture de la séance `j` : LA décision de vente, pour tout le dépôt.

    ① RÔLE — Le seul endroit où se décide une vente : à partir d'un achat à l'ouverture de la séance `j`, rendre le
      jour, le prix et le motif de la revente — objectif, stop, ou échéance. Elle ne chiffre rien : ni frais, ni gain.
    ② CONTEXTE D'APPEL — `programmes/JUGE_DES_STRATEGIES.py`, `jouer_une_entree` (donc `jouer`, l'étalon de hasard,
      le juge à huit critères et la moulinette), fin des données `"vendre"` ; `programmes/TENIR_LES_POSITIONS.py`,
      `cloturer` (le circuit du soir), fin des données `"garder"`, seuils en euros lus dans la position. Depuis le
      11-11-2026 (plan V7, bloc 4) ; avant, le soir gardait sa propre boucle. Le radar (`_c5e10_sortie`) ne l'appelle
      PAS : son recalcul reste indépendant (BACKLOG A-208 ⑤, décision de Jean-Luc du 14-08-2026).
    ③ ENTRÉE — `serie` : la série ENTIÈRE des séances d'une valeur, triée par date, chaque séance avec `date`,
      `open`, `high`, `low`, `close` · `j` : le rang de la séance d'achat dans `serie` · `vente` : un dictionnaire
      qui porte `horizon` et, AU CHOIX, soit `tp` et `sl` (les seuils en FRACTIONS du prix d'achat, 0.04 et 0.025
      pour « +4 % » et « −2,5 % » ; les prix sont alors posés par `seuils_de_vente`), soit `objectif` et `stop` (les
      prix en euros, déjà posés : ceux qu'une position du soir porte depuis son achat). `horizon` : l'échéance en
      SÉANCES après l'achat, un entier > 0, ou `COMMUN.HORIZON_AUCUNE` (aucune durée maximale) · `fin_des_donnees` :
      `"vendre"` (le juge rejoue un passé fini : une série qui s'arrête avant l'échéance vend à la dernière clôture)
      ou `"garder"` (le soir vit un présent qui continue : la position reste ouverte).
    ④ CONDITIONS D'ENTRÉE — `0 <= j < len(serie)` ; `vente` porte `horizon` et exactement l'une des deux paires.
    ⑤ SORTIE — UNE valeur : None si la position reste ouverte (`"garder"` : l'échéance n'est pas encore dans la
      série, ou il n'y en a pas) ou si l'achat tombe sur la DERNIÈRE séance sans qu'un seuil y soit touché
      (`"vendre"` : aucune séance après lui) ; sinon un dictionnaire de six clés — `pe` (l'ouverture de `serie[j]`),
      `px` (le prix de vente), `motif` (`SL_GAP`, `TP_GAP`, `SL`, `TP` ou `HORIZON`), `date_sortie`, `objectif` et
      `stop` (les deux seuils en euros, pour le prix de convention). En `"vendre"`, un achat suivi de moins de
      `horizon` séances, ou sans horizon, est vendu à la dernière clôture connue, motif `HORIZON`.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser un `fin_des_donnees` inconnu, une paire de seuils ambiguë ou un horizon qui n'est ni un
      entier > 0 ni HORIZON_AUCUNE · ② prix d'achat = ouverture de `serie[j]` (R-601) ; seuils en euros reçus, ou
      posés par `seuils_de_vente` (arrondis à cinq décimales, n°311) · ③ tester, par `tester_seance`, les séances
      `serie[j]` à `serie[j + horizon]` (toutes les suivantes sans horizon), séance d'achat comprise (R-608), et
      vendre à la première qui touche un seuil · ④ sinon, si la `horizon`-ième séance APRÈS l'achat est dans la
      série, vendre à sa clôture, motif `HORIZON` · ⑤ sinon (fin des données) : `"garder"` rend None ; `"vendre"`
      vend à la dernière clôture connue, motif `HORIZON`, ou rend None s'il n'y a aucune séance après l'achat.
    ⑦ UNITÉ — Seuils en FRACTIONS du prix d'achat, ou en EUROS ; échéance en SÉANCES de la série (des lignes : voir
      ⑨) ; prix en EUROS ; dates en texte AAAA-MM-JJ ; `j` est un rang compté depuis zéro.
    ⑧ POURQUOI — Deux implémentations d'une même chose divergent toujours (R-708) : la décision « quand vendre » était
      écrite à quatre endroits, qui divergeaient (conception J1 du 07-11-2026, §1.4 : une séance qui ouvre au-dessus
      de l'objectif puis passe sous le stop donnait l'objectif au juge et le stop au radar ; la séance d'achat n'était
      pas surveillée par `sortie_position`). Le lot ①a (07-11-2026) a fait de cette fonction la vente du juge ; le
      bloc 4 du plan V7 (11-11-2026) y fait passer le soir (pas le radar, A-208 ⑤), et retire `sortie_position` (accord de
      Jean-Luc du 08-11-2026 à 17h06, n°351 : « retirer l'ancienne fonction de vente du module des positions […]
      APRÈS qu'un programme a prouvé qu'aucun programme ne l'appelle plus »). `fin_des_donnees` est la seule
      différence voulue entre le juge, qui rejoue un passé fini, et le soir, qui vit un présent qui continue. Les
      seuils en euros existent parce qu'une position du soir FIXE ses prix le soir de l'achat et les écrit : les
      recalculer chaque soir depuis le registre ferait changer de seuils une position ouverte si la fiche changeait.
      La durée « aucune » : plan V6 et V7, bloc 4 ; contrat du lot 0 (09-11-2026) dans `programmes/COMMUN.py`.
    ⑨ CE QUI CLOCHE — Consigné, non corrigé (R-752) : · l'échéance se compte en LIGNES de la série de la valeur, pas
      en séances du calendrier de la Bourse ; R-112 (décision de Jean-Luc du 10-10-2026) veut qu'une séance manquante
      fasse avancer l'horizon, et n°315 (07-11-2026) veut la mise en conformité « dans la refonte » — non faite ici :
      elle change la vente de toute position qui traverse un trou, à décider avec le calendrier passé en entrée ·
      une vente forcée par la FIN DES DONNÉES porte le motif `HORIZON`, comme une vraie échéance (décision 7 de la
      conception J1, non tranchée), y compris pour une stratégie sans horizon · un horizon passé comme booléen est
      refusé, un flottant aussi : seul un entier Python est un nombre de séances.
    ⑩ EFFET — Aucun : ne lit ni n'écrit aucun fichier, ne modifie pas `serie`.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (fin des données inconnue, seuils ambigus, horizon refusé),
      KeyError si `vente` ou une séance manque d'une clé, IndexError si `j >= len(serie)`. UN `j` NÉGATIF NE LÈVE
      PAS : Python le compte depuis la fin de `serie` ; le ④ l'interdit, rien ne le vérifie ici ; le juge ne passe
      que des rangs >= 1, le soir des rangs trouvés dans la série. Aucun de ses appels ne peut ne pas
      revenir : `tester_seance` ne fait que comparer.
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, qui rejoue une stratégie sur le passé et la juge.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
    """
    if fin_des_donnees not in ("vendre", "garder"):
        raise ValueError("vendre : fin_des_donnees %r inconnue ; \"vendre\" (le juge) ou \"garder\" (le soir, le "
                         "radar)" % (fin_des_donnees,))
    h = vente["horizon"]
    aucune = h is _horizon_aucune()
    if not aucune and (type(h) is not int or h <= 0):
        raise ValueError("vendre : horizon %r refusé ; un entier de séances > 0, ou HORIZON_AUCUNE" % (h,))
    pe = serie[j]["open"]
    en_euros, en_fractions = ("objectif" in vente or "stop" in vente), ("tp" in vente or "sl" in vente)
    if en_euros and en_fractions:
        raise ValueError("vendre : seuils ambigus, la vente porte à la fois tp/sl et objectif/stop")
    if en_euros:
        objectif, stop = vente["objectif"], vente["stop"]
    else:
        objectif, stop = seuils_de_vente(pe, vente["tp"], vente["sl"])
    # LA SEANCE D'ACHAT COMPTE (R-608, decision de Jean-Luc du 27-09-2026 a 19h40 ; defaut 4 de A-491) : les
    # seuils se testent des la seance ou l'on achete a l'ouverture. Exemple reel du tableau de reference : Vinci,
    # achete le 07-06-2024 a 113,60, plus bas du jour 110,75 sous la vente forcee 110,76 -> vendu le jour meme.
    # L'echeance, elle, est la h-ieme seance APRES l'achat, serie[j + h].
    if aucune:
        suite = serie[j:]
    else:
        suite = serie[j:j + 1 + h]
    for b in suite:
        r = tester_seance(b, objectif, stop)
        if r:
            return {"pe": pe, "px": r[0], "motif": r[1], "date_sortie": b["date"],
                    "objectif": objectif, "stop": stop}
    apres = suite[1:]          # l'echeance se compte APRES la seance d'achat
    if not aucune and len(apres) == h:
        return {"pe": pe, "px": apres[-1]["close"], "motif": "HORIZON", "date_sortie": apres[-1]["date"],
                "objectif": objectif, "stop": stop}
    # LA SERIE S'ARRETE AVANT L'ECHEANCE (ou il n'y en a pas) : le soir GARDE la position, le juge,
    # qui rejoue un passe fini, la VEND a la derniere cloture (RealTest : « when the data ends before the test does »).
    if fin_des_donnees == "garder" or not apres:
        return None
    return {"pe": pe, "px": apres[-1]["close"], "motif": "HORIZON", "date_sortie": apres[-1]["date"],
            "objectif": objectif, "stop": stop}


# ══════════════════════════════════════════════════════════════
# CALIBRAGE — reproduire des résultats connus AVANT tout usage (A-550 ④, ÉTUDE 18 A5).
# Témoins indépendants : les montants inscrits au journal des trades, à l'époque, par
# la boucle du soir — +3 694,00 € (convention de BUREAU_VERITAS) et −2 796,25 €
# (UNIBAIL_RODAMCO), courtage seul ; +6 884,75 € (réel de BUREAU_VERITAS), forfait de
# 300 €. Pour la taxe, le témoin est un calcul à la main : 0,4 % × 100 000 € = 400,00 €
# par achat d'une valeur taxée après le 01-04-2025, 0,3 % = 300,00 € avant, 0,00 € pour
# Airbus (non taxée). Si un chiffre ne tombe pas, le module ne doit pas servir.
# Lancer :  python3 MODULE_POSITIONS.py
# ══════════════════════════════════════════════════════════════
def _calibrage():
    """Reproduit des montants connus au centime, ou refuse de laisser utiliser ce module.

    ① RÔLE — **Prouver que le moteur mesure juste, avant tout usage** : la mécanique de
      sortie, chaque régime de frais nommé, et la taxe.
    ② CONTEXTE D APPEL — Le lancement direct de ce fichier. **Personne d autre ne
      l appelle.**
    ③ ENTRÉE — Aucune : les séances et les montants attendus sont écrits dans la
      fonction ; le barème et la liste des valeurs taxées sont lus dans `donnees/`.
    ④ CONDITIONS D ENTRÉE — `donnees/BAREME_FRAIS.csv`, `donnees/VALEURS_TTF.csv` et
      `programmes/JUGE_DES_STRATEGIES.py` existent.
    ⑤ SORTIE — UNE valeur : vrai si tout est reproduit.
      [rend: 1]
    ⑥ TRAITEMENT — ① rejouer deux séances de BUREAU_VERITAS, entrée à 27,28 le
      27-07-2026, et comparer le motif, le prix réel et le prix de convention ·
      ② retrouver les trois montants du journal sous le barème qui les a produits ·
      ③ retrouver la taxe d'un achat de 100 000 € sur quatre cas (valeur taxée avant et
      après le 01-04-2025, valeur non taxée, vente) et le courtage des deux tranches ·
      ④ dire ce que deviennent les deux trades sous le barème réel.
    ⑦ UNITÉ — Prix et résultats en euros · la tolérance est un demi-centime.
    ⑧ POURQUOI — Un instrument qui ne reproduit pas un résultat connu ne mesure rien
      (règle 9bis des préférences de Jean-Luc ; ÉTUDE 18, A5). Les trois montants du
      journal ont été écrits par la boucle du soir avant ce module : ce sont des
      témoins indépendants. Le montant réel de BUREAU_VERITAS (+6 884,75 €) n'est plus
      une « anomalie figée » : il se recalcule au centime sous le barème qui l'a
      produit, le forfait de 300 €.
    ⑨ CE QUI CLOCHE — **Un seul cas de mécanique, un saut à la hausse.** Les autres
      tests de `tester_seance` sont joués par `tests/EPREUVES_DE_L_ORDRE_DES_SORTIES_Mer_30-09-2026.py`,
      pas ici. Les montants de la taxe sont des calculs à la main, pas des témoins vécus :
      aucun trade n'a encore été clos sous le barème réel.
    ⑩ EFFET — **AFFICHE** le détail de chaque comparaison.
    ⑪ TERMINAISON — Rend la main, vrai ou faux ; une erreur de lecture du barème est
      rattrapée et rend faux. **C est l appel du bas du fichier qui en fait un code de
      sortie.**
      [sort: non]
    """
    ok = True

    def comparer(libelle, obtenu, attendu):
        """Compare un résultat du calibrage à son attendu, l affiche, et éteint `ok` s il ne tombe pas.

        ① RÔLE — Le geste élémentaire du calibrage : une comparaison, une ligne à l écran.
        ② CONTEXTE D APPEL — `_calibrage`, une fois par montant ou motif à reproduire, et `leve`,
          qui s en sert pour dire si une erreur attendue est survenue.
        ③ ENTRÉE — `libelle` : ce qui est comparé, en clair · `obtenu` : ce que le module a
          rendu · `attendu` : le témoin.
        ④ CONDITIONS D ENTRÉE — Si `attendu` est un nombre à virgule, `obtenu` doit être un nombre.
        ⑤ SORTIE — Rien : rend None. Son résultat est la variable `ok` de `_calibrage`,
          remise à faux au premier écart.
          [rend: rien]
        ⑥ TRAITEMENT — si `attendu` est un nombre à virgule, l écart doit être de moins d un
          demi-centime ; sinon les deux doivent être égaux · mettre `ok` à faux sinon ·
          afficher ✅ ou ❌, le libellé, l obtenu et l attendu.
        ⑦ UNITÉ — Celle du témoin : des euros pour les montants, la tolérance est 0,005.
        ⑧ POURQUOI — Un instrument qui ne reproduit pas un résultat connu ne mesure rien (voir
          `_calibrage`, ⑧) ; une seule façon de comparer pour tous les cas.
        ⑨ CE QUI CLOCHE — Un attendu écrit comme un ENTIER (0 et non 0.00) serait comparé à
          l égalité stricte, sans tolérance : tous les attendus numériques d aujourd hui sont
          écrits avec une virgule.
        ⑩ EFFET — AFFICHE une ligne ; ÉCRIT la variable `ok` de la fonction englobante.
        ⑪ TERMINAISON — Rend la main ; aucun appel qui puisse ne pas revenir.
          [sort: non]
        """
        nonlocal ok
        m = (abs(obtenu - attendu) < 0.005) if isinstance(attendu, float) else (obtenu == attendu)
        ok = ok and m
        print(f"  {'✅' if m else '❌'} {libelle} : obtenu {obtenu!r} · attendu {attendu!r}")

    seances = [
        # 28/07/2026 — séance sans déclenchement (source : cours du projet)
        {"date": "2026-07-28", "open": 27.30, "high": 27.86, "low": 27.16, "close": 27.82},
        # 29/07/2026 — ouverture au-dessus du TP (28,3712) : TP_GAP
        {"date": "2026-07-29", "open": 29.24, "high": 30.18, "low": 29.00, "close": 29.60},
    ]
    # LA SÉANCE D'ACHAT, qui compte (R-608) : la vraie ligne du fichier maître, `donnees/cours_maitre.csv` l. 5072,
    # « BUREAU_VERITAS,2026-07-27,27.28,27.36,27.07,27.07,977663,google » ; elle ne touche ni l'objectif (28,3712)
    # ni le stop (26,598). Ajoutée le 11-11-2026 : `sortie_position`, retirée, ne regardait pas la séance d'achat.
    seances = [{"date": "2026-07-27", "open": 27.28, "high": 27.36, "low": 27.07, "close": 27.07}] + seances
    try:
        print("── CALIBRAGE BUREAU_VERITAS (mécanique, par `vendre`, garder) ──")
        r = vendre(seances, 0, {"tp": TP_PCT, "sl": SL_PCT, "horizon": HORIZON}, "garder")
        comparer("motif", r["motif"], "TP_GAP")
        comparer("prix_sortie", r["px"], 29.2400)
        comparer("prix_sortie_convention", prix_de_convention(r["motif"], r["px"], r["objectif"], r["stop"]), 28.3712)
        print("── LES TROIS MONTANTS DU JOURNAL, SOUS LEUR BARÈME ──")
        comparer("BUREAU_VERITAS convention, HIST_COURTAGE_SANS_TTF",
                 round(pnl_net(27.28, 28.3712, "BUREAU_VERITAS", "2026-07-27", "2026-07-29",
                               bareme="HIST_COURTAGE_SANS_TTF"), 2), 3694.00)
        comparer("UNIBAIL_RODAMCO stop, HIST_COURTAGE_SANS_TTF",
                 round(pnl_net(103.15, 100.57125, "UNIBAIL_RODAMCO", "2026-08-21", "2026-08-27",
                               bareme="HIST_COURTAGE_SANS_TTF"), 2), -2796.25)
        comparer("BUREAU_VERITAS réel, HIST_FORFAIT_300",
                 round(pnl_net(27.28, 29.24, "BUREAU_VERITAS", "2026-07-27", "2026-07-29",
                               bareme="HIST_FORFAIT_300"), 2), 6884.75)
        print("── LA TAXE ET LE COURTAGE DU BARÈME RÉEL, ACHAT DE 100 000 € ──")
        comparer("taxe, BUREAU_VERITAS le 2026-07-27",
                 round(cout_d_un_ordre("BUREAU_VERITAS", "2026-07-27", "achat", 100000.0)["taxe"], 2), 400.00)
        comparer("taxe, RENAULT le 2025-03-10 (0,3 %)",
                 round(cout_d_un_ordre("RNO", "2025-03-10", "achat", 100000.0)["taxe"], 2), 300.00)
        comparer("taxe, RENAULT le 2025-04-01 (0,4 %)",
                 round(cout_d_un_ordre("RENAULT", "2025-04-01", "achat", 100000.0)["taxe"], 2), 400.00)
        comparer("taxe, AIRBUS le 2026-07-27 (non taxée)",
                 round(cout_d_un_ordre("AIRBUS", "2026-07-27", "achat", 100000.0)["taxe"], 2), 0.00)
        comparer("taxe, BUREAU_VERITAS à la vente",
                 round(cout_d_un_ordre("BUREAU_VERITAS", "2026-07-29", "vente", 100000.0)["taxe"], 2), 0.00)
        comparer("courtage, ordre de 100 000 €",
                 round(cout_d_un_ordre("AIRBUS", "2026-07-27", "achat", 100000.0)["courtage"], 2), 150.00)
        comparer("courtage, ordre de 3 000 €",
                 round(cout_d_un_ordre("AIRBUS", "2026-07-27", "achat", 3000.0)["courtage"], 2), 4.90)
        print("── L'ALLER-RETOUR DU MÊME JOUR NE PAIE PAS LA TAXE (BOFiP, BOI-TCA-FIN-10-10, § 60) ──")
        # Attendus faits à la main : vente de 100 000 × 29,24 / 27,28 = 107 184,75 € ;
        # courtage 0,15 % = 160,78 € ; achat 150,00 € ; taxe d'achat 400,00 €.
        _q = 100000.0 / 27.28
        comparer("BUREAU_VERITAS acheté et revendu le 2026-07-29 : frais",
                 round(frais_aller_retour(_q, 27.28, 29.24, "BUREAU_VERITAS", "2026-07-29", "2026-07-29")["total"], 2),
                 310.78)
        comparer("le même, taxe exonérée",
                 round(frais_aller_retour(_q, 27.28, 29.24, "BUREAU_VERITAS", "2026-07-29", "2026-07-29")["taxe_exoneree"], 2),
                 400.00)
        comparer("BUREAU_VERITAS acheté le 2026-07-27, revendu le 2026-07-29 : frais",
                 round(frais_aller_retour(_q, 27.28, 29.24, "BUREAU_VERITAS", "2026-07-27", "2026-07-29")["total"], 2),
                 710.78)
        print("── UNE DATE FAUSSE OU UNE LISTE ABSENTE LÈVE, ET DIT POURQUOI ──")
        def leve(libelle, appel, classe, mot):
            """Vérifie qu un appel lève l erreur attendue, en disant sa cause ; le compare par `comparer`.

            ① RÔLE — Éprouver les refus du module : une date fausse ou une liste absente doit
              lever, et le message doit dire pourquoi.
            ② CONTEXTE D APPEL — `_calibrage`, quatre fois : date « 2025-13-45 », date « D030 »,
              année 2023 sans liste, valeur absente de la liste.
            ③ ENTRÉE — `libelle` : le cas, en clair · `appel` : une fonction sans argument qui
              lance l appel à éprouver · `classe` : la classe d erreur attendue · `mot` : un
              mot que le message de l erreur doit contenir.
            ④ CONDITIONS D ENTRÉE — —
            ⑤ SORTIE — Rien : rend None. Son verdict passe par `comparer`, qui éteint `ok`.
              [rend: rien]
            ⑥ TRAITEMENT — lancer `appel` · s il ne lève rien : comparer « aucune erreur » au nom
              de la classe (échec) · s il lève la classe attendue : comparer « cause dite » ou
              « cause non dite » selon que `mot` est dans le message · s il lève une autre
              erreur : comparer son nom à celui de la classe attendue (échec).
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un refus qui ne dit pas sa cause laisse Jean-Luc sans geste ; un refus
              qui ne lève pas laisserait chiffrer des frais faux.
            ⑨ CE QUI CLOCHE — La cause est cherchée comme une sous-chaîne du message : un mot
              présent par hasard suffit. Une erreur qui n hérite pas d `Exception` (interruption)
              n est pas rattrapée et remonte.
            ⑩ EFFET — Lance `appel` ; affiche par `comparer`.
            ⑪ TERMINAISON — Rend la main ; `appel` peut ne pas revenir s il boucle — les quatre
              appels d aujourd hui sont des lectures de barème et de liste.
              [sort: non]
            """
            try:
                appel()
                comparer(libelle, "aucune erreur", classe.__name__)
            except classe as e:
                comparer(libelle, classe.__name__ + (" (cause dite)" if mot in str(e) else " (cause non dite)"),
                         classe.__name__ + " (cause dite)")
            except Exception as e:
                comparer(libelle, type(e).__name__, classe.__name__)
        leve("date « 2025-13-45 »", lambda: cout_d_un_ordre("AIRBUS", "2025-13-45", "achat", 1000.0),
             ValueError, "calendrier")
        leve("date « D030 »", lambda: cout_d_un_ordre("AIRBUS", "D030", "achat", 1000.0, "HIST_FORFAIT_300"),
             ValueError, "illisible")
        leve("année 2023 sans liste", lambda: cout_d_un_ordre("AIRBUS", "2023-06-01", "achat", 1000.0),
             FraisNonChiffrables, "2023")
        leve("valeur absente de la liste", lambda: cout_d_un_ordre("XXX", "2026-06-01", "achat", 1000.0),
             FraisNonChiffrables, "XXX")
        print(f"  ℹ sous le barème réel : BUREAU_VERITAS réel "
              f"{pnl_net(27.28, 29.24, 'BUREAU_VERITAS', '2026-07-27', '2026-07-29'):.2f} € · convention "
              f"{pnl_net(27.28, 28.3712, 'BUREAU_VERITAS', '2026-07-27', '2026-07-29'):.2f} € · UNIBAIL_RODAMCO "
              f"{pnl_net(103.15, 100.57125, 'UNIBAIL_RODAMCO', '2026-08-21', '2026-08-27'):.2f} €")
    except Exception as e:
        ok = False
        print(f"  ❌ le calibrage n'a pas pu tourner : {type(e).__name__} : {e}")
    print("CALIBRAGE :", "OK" if ok else "ÉCHEC — NE PAS UTILISER (règle 9bis)")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _calibrage() else 1)
