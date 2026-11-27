#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le SHARPE DÉGONFLÉ, calcul du contrôle 1 du juge. Simulation uniquement : on mesure des rendements passés, aucun
ordre réel n'est jamais passé.

LE SENS EN TÊTE — R-505 version 2, étape 5 (texte accepté par Jean-Luc le 27-11-2026 à 18h38) : le contrôle 1 du juge
(« la stratégie gagne ») se CALCULE PAR LE SHARPE DÉGONFLÉ, un seul calcul, avec N = k (décision de Jean-Luc du
27-11-2026 à 19h00, « OK pour le 1 », BACKLOG A-1095), au seuil 0,05 SANS division par k : le Sharpe dégonflé compte
déjà les k essais (A-1095, correction du 27-11-2026 à 21h19 ; le contrôle 2, jour au hasard, garde 0,05 ÷ k).
Ce module porte la formule, lue dans les articles et calibrée au chiffre près sur leurs résultats publiés ; il ne
décide rien : la grille de `MODULE_JUGEMENT` compare.
Sa sœur, la probabilité de surapprentissage (contrôle 5), vit dans `MODULE_SURAPPRENTISSAGE.py`, à part parce qu'elle
exige numpy et que ce module-ci est atteint par le circuit du soir, qui n'installe pas numpy (épreuve
`tests/EPREUVES_DE_LA_VERSION_DE_PYTHON_Mar_17-11-2026.py`, constat M2 du 27-11-2026).

① RÔLE — Porter, à UN seul endroit (R-708 : deux implémentations d'une même chose divergent toujours), la formule de
  Bailey et López de Prado, « The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and
  Non-Normality », Journal of Portfolio Management 40(5), 2014, p. 94-107.
② CONTEXTE D'APPEL — Au 27-11-2026 : les épreuves `tests/EPREUVES_DU_SHARPE_DEGONFLE_ET_DE_LA_PBO_Ven_27-11-2026.py`
  et le mesureur `MODULE_JUGEMENT.mesurer_le_sharpe_degonfle`. Destiné au juge (étape 5) et au banc des stratégies
  simulées (A-1094), qui compare le Sharpe dégonflé au calcul « gain > 0 à 0,05 ÷ k »
  (`MODULE_JUGEMENT.probabilite_que_le_gain_soit_du_hasard`, gardé appelable). Aucune ligne de commande.
③ ENTRÉE — Voir chaque fonction.
④ CONDITIONS D'ENTRÉE — Python 3.9 et plus, la bibliothèque livrée d'origine seule (`math`, `statistics`).
⑤ SORTIE — Ne rend rien : pose quatre fonctions et une constante.
⑥ TRAITEMENT — Définir `moments_des_rendements`, `sharpe_attendu_du_meilleur_hasard`, `sharpe_degonfle`,
  `sharpe_degonfle_d_une_serie`.
⑦ UNITÉ — UN RENDEMENT est une FRACTION par séance (0,004 pour +0,4 % du compte sur une séance), la série demandée par
  A-1071 (« la courbe du compte au jour le jour », lot W2b, pas encore fabriquée au 27-11-2026). LE SHARPE de ce module
  est NON ANNUALISÉ : moyenne ÷ écart-type des rendements PAR SÉANCE ; c'est l'unité de la formule (les chiffres
  annualisés de l'article se ramènent à la séance en divisant le Sharpe par √q et sa variance par q, q séances par an).
  Les probabilités sont des fractions entre 0 et 1.
⑧ POURQUOI — L'ancienne fonction `calculer_deflated_sharpe` de `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`
  n'est PAS réutilisée comme instrument de décision, et voici pourquoi (lu dans son code le 27-11-2026) : ① elle ARRONDIT
  sa probabilité au millième (`round(dsr, 3)`), or un arrondi au millième déplace la frontière du seuil 0,05, et les
  seuils 0,05 ÷ k du contrôle 2 descendent sous le millième (0,0005 pour k = 100) ; ② elle rend 0 quand elle refuse
  (moins de deux essais), la même valeur qu'une très mauvaise stratégie (son ⑨ ③) ; ③ elle refuse N = 1, alors que k
  peut valoir 1 (A-1082 : premier vrai passage) ; ④ elle annonce un Sharpe « annualisé » et le
  multiplie par √(nombre d'opérations − 1), deux unités qui ne vont pas ensemble. Elle reste en
  place, inchangée (R-751 ⑩ : rien ne se supprime sans accord) ; l'épreuve E3 confronte l'ancienne à la nouvelle pour
  que leur divergence se voie.
⑨ CE QUI CLOCHE — ① La série d'entrée (A-1071) n'existe pas encore : le mesureur du juge n'a pas d'appelant réel et la
  grille rend le contrôle INCONNU ; c'est voulu (R-505 : un contrôle non calculable empêche la validation). ② LE SHARPE
  DÉGONFLÉ EST CONÇU POUR « LA MEILLEURE PARMI N » ; le juge l'applique à CHAQUE version envoyée (réserve écrite dans la
  loi, étape 5) ; lequel des deux calculs (Sharpe dégonflé ou « gain > 0 ») rejette le moins de bonnes stratégies se
  mesure au banc (A-1094). La barre ne monte qu'UNE fois avec k, par le Sharpe du meilleur hasard SR0 : le seuil est
  0,05, comme l'article compare la probabilité à 0,95 (A-1095, correction du 27-11-2026 à 21h19 ; jusqu'au lot L3-FIX,
  le juge divisait encore 0,05 par k et comptait les essais deux fois).
  ③ La variance des Sharpe des essais est celle de la liste reçue : ce que la liste contient (versions envoyées au
  juge, regroupées par ressemblance, A-772 ; stratégies déjà jugées, A-1082) est choisi par l'appelant.
⑩ EFFET — Aucun : ne lit ni n'écrit de fichier.
⑪ TERMINAISON — Le chargement rend la main ; aucune fonction ne lit le réseau ni n'attend.
⑫ DÉFINITIONS
  le Sharpe : la moyenne des rendements divisée par leur écart-type, ici par séance
  le Sharpe dégonflé : la probabilité que le vrai Sharpe dépasse le meilleur Sharpe que N essais SANS talent auraient
    produit par chance, compte tenu de la longueur de la série, de son asymétrie et de son aplatissement
  k : les versions réellement envoyées au juge, regroupées par ressemblance, plus les stratégies déjà réellement
    jugées (A-774, A-772, A-1082)
"""

import math
from statistics import NormalDist

# LA CONSTANTE D'EULER-MASCHERONI, γ ≈ 0,5772 : elle vient de la formule du maximum attendu de N tirages normaux (Bailey
# et López de Prado 2014, équation du seuil SR0 ; Bailey et al. 2015, « Online Tools… », équation 3). Une constante
# mathématique, pas un réglage : elle s'écrit ici, comme π.
EULER_MASCHERONI = 0.5772156649015329

_NORMALE = NormalDist()


def moments_des_rendements(rendements):
    """Rend le Sharpe par séance d'une série de rendements, sa longueur, son asymétrie et son aplatissement.

    ① RÔLE — Donner au Sharpe dégonflé les quatre grandeurs qu'il prend de la série jugée : SR, T, γ3, γ4.
    ② CONTEXTE D'APPEL — `sharpe_degonfle_d_une_serie` ; les épreuves.
    ③ ENTRÉE — `rendements` : une suite de nombres, un par séance, dans l'ordre du temps (l'ordre n'entre pas dans le
      calcul).
    ④ CONDITIONS D'ENTRÉE — Au moins deux nombres finis, pas tous égaux.
    ⑤ SORTIE — UNE valeur : un dictionnaire de six clés : `n_observations` (T), `moyenne`, `ecart_type`, `sharpe`,
      `asymetrie` (γ3), `aplatissement` (γ4, BRUT : 3 pour la loi normale).
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser moins de deux nombres, un nombre non fini, un booléen · ② moyenne · ③ moments centrés
      d'ordre 2, 3, 4 (division par T) · ④ écart-type = racine du moment d'ordre 2 ; nul → refuser · ⑤ SR = moyenne ÷
      écart-type ; γ3 = m3 ÷ m2^1,5 ; γ4 = m4 ÷ m2².
    ⑦ UNITÉ — Moyenne et écart-type : FRACTION par séance ; Sharpe, γ3, γ4 : sans unité ; T : nombre de séances.
    ⑧ POURQUOI — L'aplatissement est BRUT parce que la formule de l'article porte (γ4 − 1) ÷ 4 : sous la loi normale
      (γ4 = 3, γ3 = 0) le dénominateur vaut 1 + SR² ÷ 2, la variance connue du Sharpe estimé (Lo, 2002) ; un aplatissement
      « en excès » (0 pour la loi normale) fausserait la correction. Tous les moments divisent par T (et non T − 1),
      pour que les quatre grandeurs soient du même estimateur ; l'écart sur des séries de milliers de séances est
      négligeable (un facteur √(T ÷ (T − 1))).
    ⑨ CE QUI CLOCHE — Le choix « division par T » est un CHOIX TECHNIQUE, non tranché par l'article lu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    x = []
    for v in rendements:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError("rendement non numérique ou non fini : %r" % (v,))
        x.append(float(v))
    t = len(x)
    if t < 2:
        raise ValueError("moins de deux rendements (%d) : pas de Sharpe" % t)
    moy = math.fsum(x) / t
    m2 = math.fsum((v - moy) ** 2 for v in x) / t
    if not m2 > 0.0:
        raise ValueError("rendements tous égaux : écart-type nul, Sharpe indéfini")
    m3 = math.fsum((v - moy) ** 3 for v in x) / t
    m4 = math.fsum((v - moy) ** 4 for v in x) / t
    et = math.sqrt(m2)
    return {"n_observations": t, "moyenne": moy, "ecart_type": et, "sharpe": moy / et,
            "asymetrie": m3 / m2 ** 1.5, "aplatissement": m4 / (m2 * m2)}


def sharpe_attendu_du_meilleur_hasard(n_essais, variance_des_sharpe):
    """Rend SR0, le meilleur Sharpe que N essais sans talent produiraient par chance, en moyenne.

    ① RÔLE — La barre du Sharpe dégonflé : plus on essaie de versions, plus le meilleur Sharpe dû à la seule chance
      est haut (A-1095 : « ses entrées : le nombre d'essais et la dispersion des Sharpe des essais »).
    ② CONTEXTE D'APPEL — `sharpe_degonfle` ; les épreuves.
    ③ ENTRÉE — `n_essais` : N, un entier ≥ 1 (k du juge) · `variance_des_sharpe` : V[SR_n], la variance des Sharpe
      NON ANNUALISÉS des essais.
    ④ CONDITIONS D'ENTRÉE — N entier ≥ 1, non booléen ; pour N ≥ 2, V finie et STRICTEMENT positive.
    ⑤ SORTIE — UNE valeur : SR0, un nombre ≥ 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① N = 1 → 0 · ② sinon SR0 = √V × ((1 − γ) × Z⁻¹(1 − 1/N) + γ × Z⁻¹(1 − 1/(N e))), Z⁻¹ la loi
      normale inverse, γ la constante d'Euler-Mascheroni, e le nombre d'Euler.
    ⑦ UNITÉ — SR0 est un Sharpe PAR SÉANCE si V est la variance de Sharpe par séance.
    ⑧ POURQUOI — FORMULE LUE le 27-11-2026 dans Bailey, Borwein, Salehipour, López de Prado et Zhu, « Online Tools for
      Demonstration of Backtest Overfitting » (2015, escholarship.org/content/qt2329p290/qt2329p290.pdf), équation 3,
      qui reprend celle de l'article de 2014 ; et dans le code de l'article de 2014 (« Snippet 1 » :
      `maxZ=(1-emc)*ss.norm.ppf(1-1./numTrials)+emc*ss.norm.ppf(1-1./(numTrials*np.e))`, puis `mu+sigma*maxZ`, mu = 0
      sous l'hypothèse nulle d'un Sharpe nul). N = 1 rend 0 parce qu'avec un seul essai il n'y a pas de sélection :
      le Sharpe dégonflé devient le Sharpe probabiliste de seuil zéro, ce que dit l'article (« a PSR where the rejection
      threshold is adjusted to reflect the multiplicity of trials ») ; la formule elle-même n'existe pas en N = 1
      (Z⁻¹(0) = −∞). Une variance NULLE est refusée : elle ferait disparaître le dégonflage sans un mot (défaut ⑨ ① de
      l'ancienne fonction, mesuré le 19-09-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    if isinstance(n_essais, bool) or not isinstance(n_essais, int) or n_essais < 1:
        raise ValueError("nombre d'essais N = %r : il faut un entier ≥ 1" % (n_essais,))
    if n_essais == 1:
        return 0.0
    v = variance_des_sharpe
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not v > 0.0:
        raise ValueError("variance des Sharpe des essais = %r : il faut un nombre fini strictement positif" % (v,))
    g = EULER_MASCHERONI
    return math.sqrt(v) * ((1.0 - g) * _NORMALE.inv_cdf(1.0 - 1.0 / n_essais)
                           + g * _NORMALE.inv_cdf(1.0 - 1.0 / (n_essais * math.e)))


def sharpe_degonfle(sharpe, n_essais, variance_des_sharpe, n_observations, asymetrie, aplatissement):
    """Rend le Sharpe dégonflé : la probabilité que le vrai Sharpe dépasse celui du meilleur de N essais sans talent.

    ① RÔLE — Le calcul du contrôle 1 de l'étape 5 de R-505 v2 (A-1095) : il tient compte du nombre d'essais, de la
      longueur des données et de la forme des gains (asymétrie, aplatissement) — les nôtres, coupés par l'objectif et
      le stop, ne suivent pas la loi normale.
    ② CONTEXTE D'APPEL — `sharpe_degonfle_d_une_serie` ; les épreuves (calibrage sur les chiffres publiés).
    ③ ENTRÉE — `sharpe` : SR observé de la version, PAR SÉANCE · `n_essais` : N (= k) · `variance_des_sharpe` : V
      des Sharpe par séance des essais · `n_observations` : T, le nombre de rendements de la série · `asymetrie` : γ3 ·
      `aplatissement` : γ4 BRUT (3 = loi normale).
    ④ CONDITIONS D'ENTRÉE — Nombres finis ; T entier ≥ 2 ; celles de `sharpe_attendu_du_meilleur_hasard`.
    ⑤ SORTIE — UNE valeur : un dictionnaire de quatre clés : `probabilite` (le Sharpe dégonflé, entre 0 et 1, NON
      ARRONDI), `sharpe_du_meilleur_hasard` (SR0), `z` et `nombre_d_essais` (N).
      [rend: 1]
    ⑥ TRAITEMENT — ① contrôler les entrées · ② SR0 · ③ D = 1 − γ3 × SR + (γ4 − 1) ÷ 4 × SR² ; D ≤ 0 → refuser ·
      ④ z = (SR − SR0) × √(T − 1) ÷ √D · ⑤ probabilité = Z(z), la loi normale.
    ⑦ UNITÉ — SR, SR0 : Sharpe par séance ; z sans unité ; probabilité : fraction.
    ⑧ POURQUOI — FORMULE LUE le 27-11-2026 (Bailey et al. 2015, équation 2, reprise de l'article de 2014) :
      DSR = Z[(SR − SR0) √(T − 1) ÷ √(1 − γ3 SR + (γ4 − 1)/4 SR²)]. CALIBRÉE au chiffre près sur deux résultats publiés
      (épreuve E1) : l'exemple de l'article (SR annualisé 2,5, N = 100, V annualisée 0,5, T = 1 250, γ3 = −3, γ4 = 10,
      250 séances par an) rend 0,9004 — l'article : « 90 % » ; avec N = 46, 0,9505 — l'article : « 0.9505 » ; et la même
      série supposée normale passe 0,95 jusqu'à N = 88 et non à 89 — l'article : « N = 88 » ; à 252 séances par an, le
      même exemple rend 0,8996723484977763, le chiffre publié par la reproduction de G. Marti (gmarti.gitlab.io,
      30-05-2018). Rien n'est arrondi : un arrondi déplacerait la frontière du seuil du contrôle 1 (0,05).
    ⑨ CE QUI CLOCHE — La probabilité vaut exactement 1,0 en virgule flottante quand z dépasse environ 8,3 : 1 − 1,0 = 0
      passe alors toute barre, ce qui est juste (la vraie valeur est sous 1e-16).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    for nom, v in (("sharpe", sharpe), ("asymetrie", asymetrie), ("aplatissement", aplatissement)):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError("%s = %r : il faut un nombre fini" % (nom, v))
    if isinstance(n_observations, bool) or not isinstance(n_observations, int) or n_observations < 2:
        raise ValueError("nombre d'observations T = %r : il faut un entier ≥ 2" % (n_observations,))
    sr0 = sharpe_attendu_du_meilleur_hasard(n_essais, variance_des_sharpe)
    d = 1.0 - asymetrie * sharpe + (aplatissement - 1.0) / 4.0 * sharpe * sharpe
    if not d > 0.0:
        raise ValueError("dénominateur 1 − γ3·SR + (γ4 − 1)/4·SR² = %r ≤ 0 : Sharpe dégonflé indéfini" % (d,))
    z = (sharpe - sr0) * math.sqrt(n_observations - 1) / math.sqrt(d)
    return {"probabilite": _NORMALE.cdf(z), "sharpe_du_meilleur_hasard": sr0, "z": z, "nombre_d_essais": n_essais}


def sharpe_degonfle_d_une_serie(rendements, n_essais, sharpes_des_essais):
    """Rend le Sharpe dégonflé d'une série de rendements quotidiens, avec ses moments et la variance des essais.

    ① RÔLE — L'interface du contrôle 1 : une série (A-1071 : le rendement quotidien du compte de la version, sur les
      30 %), le nombre d'essais k et les Sharpe des essais — et rien d'autre à fournir.
    ② CONTEXTE D'APPEL — `MODULE_JUGEMENT.mesurer_le_sharpe_degonfle` ; le banc (A-1094) ; les épreuves.
    ③ ENTRÉE — `rendements` : la série de la version jugée, une FRACTION par séance · `n_essais` : N = k ·
      `sharpes_des_essais` : les Sharpe PAR SÉANCE des essais comptés dans k, dans la même unité, mesurés sur la même
      période que la série (au moins deux si N ≥ 2 ; ignorés si N = 1).
    ④ CONDITIONS D'ENTRÉE — Celles de `moments_des_rendements` et de `sharpe_degonfle`.
    ⑤ SORTIE — UNE valeur : le dictionnaire de `sharpe_degonfle`, plus les six clés de `moments_des_rendements` et
      `variance_des_sharpe` (None si N = 1).
      [rend: 1]
    ⑥ TRAITEMENT — ① moments · ② V = variance (division par n − 1) des Sharpe des essais si N ≥ 2 · ③ `sharpe_degonfle`.
    ⑦ UNITÉ — Celles de `sharpe_degonfle`.
    ⑧ POURQUOI — La variance des essais se prend AVEC n − 1 : c'est un échantillon de la dispersion des Sharpe, et
      l'estimateur sans biais est le plus prudent des deux (une variance plus grande relève SR0).
    ⑨ CE QUI CLOCHE — Le module ne vérifie pas que les Sharpe des essais ont été mesurés sur la même période ni à la
      même fréquence : c'est la responsabilité de l'appelant, écrite ici.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    m = moments_des_rendements(rendements)
    v = None
    if not (isinstance(n_essais, int) and not isinstance(n_essais, bool) and n_essais == 1):
        s = []
        for x in sharpes_des_essais or ():
            if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
                raise ValueError("Sharpe d'un essai non numérique ou non fini : %r" % (x,))
            s.append(float(x))
        if len(s) < 2:
            raise ValueError("%d Sharpe d'essais reçus : il en faut au moins deux pour leur variance" % len(s))
        moy = math.fsum(s) / len(s)
        v = math.fsum((x - moy) ** 2 for x in s) / (len(s) - 1)
    r = sharpe_degonfle(m["sharpe"], n_essais, v, m["n_observations"], m["asymetrie"], m["aplatissement"])
    r.update(m)
    r["variance_des_sharpe"] = v
    return r
