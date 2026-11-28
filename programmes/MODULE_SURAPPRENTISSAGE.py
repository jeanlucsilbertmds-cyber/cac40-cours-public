#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La PROBABILITÉ DE SURAPPRENTISSAGE (PBO), contrôle 5 du juge, et son mesureur. Simulation uniquement : on mesure des
rendements passés, aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — R-505 version 2, étape 5 (texte accepté par Jean-Luc le 27-11-2026 à 18h38) : « LA PROBABILITÉ DE
SURAPPRENTISSAGE, calculée sur les 70 % sur toutes les versions, est reportée dans le verdict — EXIGÉE : au-dessus du
seuil, la stratégie n'est pas validée » ; seuil de départ 0,05, la valeur de l'article (décision de Jean-Luc du
27-11-2026 à 18h53, « 1 », BACKLOG A-1093 ; A-654, A-1066). Ce module porte l'algorithme de l'article, transcrit pas à
pas et éprouvé contre lui ; il ne décide rien : la grille de `MODULE_JUGEMENT` compare la PBO au seuil
`surapprentissage_maximum`, que la porte du juge lit dans `donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv`.

① RÔLE — Porter, à UN seul endroit (R-708), l'algorithme 2.3 (CSCV) de Bailey, Borwein, López de Prado et Zhu, « The
  Probability of Backtest Overfitting », Journal of Computational Finance 20(4), 2017, et la mesure que la grille attend.
② CONTEXTE D'APPEL — Au 27-11-2026 : les épreuves `tests/EPREUVES_DU_SHARPE_DEGONFLE_ET_DE_LA_PBO_Ven_27-11-2026.py`.
  Destiné à la moulinette sur les 70 % (étape 3 de R-505 v2) quand elle rendra le rendement quotidien de chaque version
  (A-1071, lot W2b), au juge, et au banc des stratégies simulées (A-1094 : comparer les seuils 0,05 et 0,30). Aucun
  programme du circuit du soir ne l'importe : il exige numpy, que le soir n'installe pas. Aucune ligne de commande.
③ ENTRÉE — Voir chaque fonction.
④ CONDITIONS D'ENTRÉE — Python 3.9 et plus ; numpy (12 870 coupures × des milliers de versions ne se calculent pas en
  Python pur ; la certification l'installe, `numpy==2.2.6`, .github/workflows/certifier.yml).
⑤ SORTIE — Ne rend rien : pose deux fonctions et une constante.
⑥ TRAITEMENT — Définir `probabilite_de_surapprentissage` et `mesurer_le_surapprentissage`.
⑦ UNITÉ — UN RENDEMENT est une FRACTION par séance ; la performance de chaque moitié est le Sharpe par séance ; la PBO
  est une fraction entre 0 et 1.
⑧ POURQUOI — L'ancienne fonction `calculer_pbo` de `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` n'est PAS
  réutilisée comme instrument de décision (lu dans son code le 27-11-2026) : elle range des OPÉRATIONS dans des blocs de
  JOURS DE CALENDRIER et additionne des euros, alors que l'article découpe une matrice de RENDEMENTS synchrones en blocs
  de lignes égales ; elle tire 1 000 coupures au hasard au lieu des 12 870 ; elle rend 0,0, la meilleure valeur, quand
  rien n'est mesuré (son ⑨ ①) ; son seuil 0,30 (GRILLE-26-04) est sans source (A-1093). Elle reste en place, inchangée
  (R-751 ⑩ : rien ne se supprime sans accord).
⑨ CE QUI CLOCHE — ① La matrice des 70 % n'existe pas encore (A-1071, W2b) : aucun appelant réel ; la porte du juge n'a
  pas de mesureur de surapprentissage (`CONTRATS_DES_FICHIERS.MESUREURS_DU_JUGE`), la grille rend le contrôle INCONNU.
  ② Les égalités ne sont pas traitées par l'article ; ce module prend le choix le plus sévère (voir la fonction).
  ③ Les cas d'essai publiés de l'article sont reproduits dans leurs fourchettes, sauf deux cas « faible
  surapprentissage » qui sortent un peu SOUS la fourchette publiée (épreuve E6, écart affiché, non expliqué).
⑩ EFFET — Aucun : ne lit ni n'écrit de fichier.
⑪ TERMINAISON — Le chargement rend la main.
⑫ DÉFINITIONS
  la PBO : la part des coupures des données en deux moitiés où la version qui gagne sur une moitié retombe sous la
    médiane des versions sur l'autre moitié
  une version : une stratégie déclinée par la moulinette ; « une version est équivalent à une nouvelle stratégie »
    (Jean-Luc, 31-10-2026 à 15h51, A-666)
  les 70 % : les 70 % les plus anciens des séances réellement lues, où l'on choisit
"""

# LE NOMBRE DE BLOCS DE LA PBO PAR DÉFAUT : 16, celui des exemples de l'article de 2017 (« S = 16 », 12 870 coupures).
# Un CHOIX TECHNIQUE (R-505 v2, « À PRÉCISER AVANT LA PROGRAMMATION » : fixé à la programmation, éprouvé sur le banc),
# pas un seuil de décision ; l'article demande S pair, et assez petit pour ne pas casser la structure des données.
BLOCS_DE_LA_PBO = 16


def probabilite_de_surapprentissage(matrice, n_blocs=BLOCS_DE_LA_PBO, taille_des_paquets=256):
    """Rend la PBO d'un lot de versions par la validation croisée symétrique combinatoire (CSCV) de l'article.

    ① RÔLE — Le contrôle 5 de l'étape 5 de R-505 v2 : la version choisie parmi toutes celles essayées sur les 70 %
      reste-t-elle bonne sur des morceaux de données qui n'ont pas servi à la choisir ? (A-654, A-1066, A-1093.)
    ② CONTEXTE D'APPEL — `mesurer_le_surapprentissage` ; la moulinette sur les 70 % quand elle rendra
      les séries par version (A-1071, lot W2b) ; le banc ; les épreuves.
    ③ ENTRÉE — `matrice` : T lignes × N colonnes de RENDEMENTS (fraction par séance), une colonne par version essayée,
      une ligne par séance, toutes les colonnes sur les MÊMES séances (liste de lignes, ou tableau numpy 2-D) ·
      `n_blocs` : S, pair, ≥ 2 · `taille_des_paquets` : nombre de coupures calculées à la fois (mémoire seulement).
    ④ CONDITIONS D'ENTRÉE — numpy installé ; N ≥ 2 ; T ≥ S ; nombres finis.
    ⑤ SORTIE — UNE valeur : un dictionnaire de neuf clés : `pbo` (fraction), `n_combinaisons` (C(S, S/2)), `n_blocs`,
      `n_versions` (N), `lignes_utilisees`, `lignes_ecartees`, `logit_median`, `part_hors_echantillon_negative` (part
      des coupures où la version choisie a un Sharpe négatif sur l'autre moitié), `performance` (« sharpe »).
      [rend: 1]
    ⑥ TRAITEMENT — Les étapes de l'algorithme 2.3 de l'article : ① écarter les T mod S PREMIÈRES lignes (les plus
      anciennes) pour que les S blocs aient la même taille T ÷ S · ② couper la matrice en S blocs de lignes successives ·
      ③ toutes les combinaisons de S/2 blocs (12 870 pour S = 16) · ④ pour chacune : J = ces blocs, J̄ = les autres ;
      performance = Sharpe de chaque version sur J et sur J̄ ; n* = la meilleure sur J (à égalité, la première colonne) ;
      rang hors échantillon r = 1 + le nombre de versions STRICTEMENT moins bonnes que n* sur J̄ ; ω = r ÷ (N + 1) ;
      λ = ln(ω ÷ (1 − ω)) · ⑤ PBO = part des λ ≤ 0.
    ⑦ UNITÉ — Rendements : fraction par séance ; Sharpe sans unité ; PBO : fraction entre 0 et 1.
    ⑧ POURQUOI — ALGORITHME LU le 27-11-2026 dans Bailey, Borwein, López de Prado et Zhu, « The Probability of Backtest
      Overfitting », Journal of Computational Finance 20(4), 2017 (carmamaths.org/jon/backtest2.pdf), algorithme 2.3 :
      matrice T × N, S blocs « of equal dimensions », toutes les combinaisons de S/2, ω̄ = r̄ ÷ (N + 1), logit, PBO =
      intégrale de f(λ) sur λ ≤ 0 ; la performance des exemples de l'article est le Sharpe. LES ÉGALITÉS, que
      l'article ne traite pas, prennent le choix le PLUS SÉVÈRE (R-505 : la règle la plus stricte) : un rang compte
      seulement les versions STRICTEMENT moins bonnes, si bien qu'une version choisie à égalité avec d'autres hors
      échantillon tombe au plus bas de leur groupe. UNE MOITIÉ SANS VARIATION (une version qui ne joue jamais sur J̄,
      rendements tous nuls) a un Sharpe de 0 : aucun gain, aucune perte. Les PREMIÈRES lignes sont écartées, et non
      les dernières, parce que les plus récentes sont les plus proches de la période d'examen.
    ⑨ CE QUI CLOCHE — ① Une version au rendement constant NON NUL (impossible pour un compte qui achète et vend) aurait
      un écart-type d'arrondi minuscule et un Sharpe énorme. ② Le calibrage « au chiffre près » se fait contre une
      transcription pas à pas de l'article (épreuve E5), et contre les fourchettes publiées des cas d'essai (épreuve E6),
      l'article ne publiant aucun exemple entièrement reproductible.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError / ImportError. Le temps croît comme C(S, S/2) × N : pour S = 16 et
      21 000 versions, environ 2,7 × 10⁸ comparaisons, quelques dizaines de secondes avec numpy.
      [sort: non]
    """
    import numpy as np
    from itertools import combinations
    if isinstance(n_blocs, bool) or not isinstance(n_blocs, int) or n_blocs < 2 or n_blocs % 2:
        raise ValueError("nombre de blocs S = %r : il faut un entier pair ≥ 2" % (n_blocs,))
    m = np.asarray(matrice, dtype=float)
    if m.ndim != 2:
        raise ValueError("la matrice doit avoir deux dimensions (séances × versions), elle en a %d" % m.ndim)
    t, n = m.shape
    if n < 2:
        raise ValueError("%d version(s) : il en faut au moins deux pour une PBO" % n)
    if t < n_blocs:
        raise ValueError("%d séance(s) pour %d blocs : il faut au moins une séance par bloc" % (t, n_blocs))
    if not np.all(np.isfinite(m)):
        raise ValueError("la matrice porte des nombres non finis")
    ecartees = t % n_blocs
    m = m[ecartees:]
    h = m.shape[0] // n_blocs
    blocs = m.reshape(n_blocs, h, n)
    somme, carres = blocs.sum(axis=1), (blocs * blocs).sum(axis=1)          # S × N
    tot_s, tot_c = somme.sum(axis=0), carres.sum(axis=0)
    moitie = n_blocs // 2
    nb_lignes = moitie * h

    def sharpe(s, c):
        """Rend le Sharpe de chaque version d'une moitié, à partir de ses sommes et de ses sommes de carrés.
        ① RÔLE — Mesurer la performance de l'article (le Sharpe) sur une moitié des blocs.
        ② CONTEXTE D'APPEL — La boucle des coupures de `probabilite_de_surapprentissage`, deux fois par paquet.
        ③ ENTRÉE — `s`, `c` : tableaux (coupures × versions) des sommes et des sommes de carrés des rendements sur
          `nb_lignes` séances.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le tableau (coupures × versions) des Sharpe.
          [rend: 1]
        ⑥ TRAITEMENT — moyenne, variance (division par le nombre de séances), Sharpe ; variance ≤ 0 → 0.
        ⑦ UNITÉ — Sharpe par séance.
        ⑧ POURQUOI — Les sommes par bloc évitent de rejouer les lignes 12 870 fois ; E5 prouve l'égalité avec le
          calcul direct sur les lignes.
        ⑨ CE QUI CLOCHE — Voir ⑨ ① de la fonction (rendement constant non nul).
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]"""
        moy = s / nb_lignes
        var = c / nb_lignes - moy * moy
        et = np.sqrt(np.where(var > 0.0, var, 1.0))
        return np.where(var > 0.0, moy / et, 0.0)

    coupures = list(combinations(range(n_blocs), moitie))
    logits, negatifs = [], 0
    for i in range(0, len(coupures), taille_des_paquets):
        paquet = coupures[i:i + taille_des_paquets]
        ind = np.zeros((len(paquet), n_blocs))
        for j, c in enumerate(paquet):
            ind[j, list(c)] = 1.0
        s_in, c_in = ind @ somme, ind @ carres
        r_in = sharpe(s_in, c_in)
        r_out = sharpe(tot_s - s_in, tot_c - c_in)
        meilleur = np.argmax(r_in, axis=1)                               # à égalité : la première colonne
        choisi = r_out[np.arange(len(paquet)), meilleur]
        rang = 1 + (r_out < choisi[:, None]).sum(axis=1)
        w = rang / (n + 1.0)
        logits.extend(np.log(w / (1.0 - w)).tolist())
        negatifs += int((choisi < 0.0).sum())
    lam = np.asarray(logits)
    return {"pbo": float((lam <= 0.0).mean()), "n_combinaisons": len(coupures), "n_blocs": n_blocs, "n_versions": n,
            "lignes_utilisees": int(m.shape[0]), "lignes_ecartees": int(ecartees),
            "logit_median": float(np.median(lam)), "part_hors_echantillon_negative": negatifs / len(coupures),
            "performance": "sharpe"}


def mesurer_le_surapprentissage(matrice_des_70):
    """Rend la mesure `surapprentissage` que la grille attend (contrôle 5 de l'étape 5 de R-505 v2), ou la raison.

    ① RÔLE — Le mesureur du contrôle 5 : « LA PROBABILITÉ DE SURAPPRENTISSAGE, calculée sur les 70 % sur toutes les
      versions, est reportée dans le verdict — EXIGÉE : au-dessus du seuil, la stratégie n'est pas validée » (R-505 v2,
      étape 5 ; décisions de Jean-Luc du 31-10-2026 à 17h35, n°30, du 01-11-2026 à 13h23, n°109, et du 27-11-2026 à
      18h47 et 18h53, A-1093). La grille compare la PBO au seuil `surapprentissage_maximum`, que la porte du juge lit
      dans le fichier des seuils en attente (`MODULE_JUGEMENT.table_des_seuils_en_attente`).
    ② CONTEXTE D'APPEL — Au 27-11-2026 : les épreuves et le banc. PAS ENCORE la porte ni la moulinette : la moulinette
      ne rend que des lignes de résultats par version, pas les séries quotidiennes que la PBO découpe (A-1071, W2b).
    ③ ENTRÉE — `matrice_des_70` : séances × versions, le rendement quotidien du compte de CHAQUE version essayée sur
      les 70 % (une FRACTION par séance), toutes les colonnes sur les mêmes séances.
    ④ CONDITIONS D'ENTRÉE — Celles de `probabilite_de_surapprentissage`.
    ⑤ SORTIE — DEUX valeurs : la mesure (champs du contrat DETAILS_DES_CONTROLES["surapprentissage"] — `pbo` et
      `nombre_d_essais`, le nombre de versions de la matrice — plus le détail du calcul), ou None ; et la raison.
      [rend: 2]
    ⑥ TRAITEMENT — appeler `probabilite_de_surapprentissage(matrice_des_70)` avec ses blocs par défaut ; une
      ValueError, une ImportError ou une erreur numérique (ArithmeticError), ou une PBO qui n'est pas un nombre fini
      entre 0 et 1, devient (None, sa raison) — jamais 0, la meilleure valeur (relecture V1 du lot L3, D5).
    ⑦ UNITÉ — PBO : fraction entre 0 et 1 ; nombre d'essais : nombre de versions.
    ⑧ POURQUOI — `nombre_d_essais` est le nombre de VERSIONS ESSAYÉES (toutes les colonnes), et non k : la loi calcule
      la PBO « sur TOUTES les versions essayées » ; la grille exige qu'il ne soit pas inférieur à k (lecture D2 de B).
    ⑨ CE QUI CLOCHE — La matrice des 70 % n'existe pas encore (W2b) : aucun appelant réel.
    ⑩ EFFET — Charge numpy au premier appel.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import math
    try:
        r = probabilite_de_surapprentissage(matrice_des_70)
    except (ValueError, ImportError, ArithmeticError) as e:
        return None, "probabilité de surapprentissage non calculable : %s: %s" % (type(e).__name__, e)
    p = r.get("pbo")
    if isinstance(p, bool) or not isinstance(p, float) or not math.isfinite(p) or not 0.0 <= p <= 1.0:
        return None, "probabilité de surapprentissage non calculable : PBO %r hors de [0, 1] ou non finie" % (p,)
    m = dict(r)
    m["nombre_d_essais"] = r["n_versions"]
    return m, ""
