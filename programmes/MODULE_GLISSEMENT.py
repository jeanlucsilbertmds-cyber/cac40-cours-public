#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MODULE_GLISSEMENT — Ven 27-11-2026 (Paris), lot W2e du plan R505. SIMULATION UNIQUEMENT : aucun ordre réel.

À QUOI SERT CE MODULE, EN FRANÇAIS SIMPLE. Le GLISSEMENT est l'écart entre le prix qu'un calcul suppose et le prix
qu'un ordre obtiendrait vraiment. Jusqu'au 27-11-2026, la grille de verdict l'approchait par des « frais doublés »
(0,30 % par ordre au lieu de 0,15 %). Jean-Luc a demandé d'où venait ce « double » (27-11-2026 à 13h31 : « Mais ça
vient d'où d'estimer que ces écarts seraient le double des frais? ») ; aucune publication ne le justifie. Décision de
Jean-Luc du 27-11-2026 à 13h33 (« Très bien, oui, fait comme ça », BACKLOG A-1068) : plus de frais doublés ; le
glissement est MESURÉ sur nos données et AJOUTÉ au calcul des gains. Ce module est le SEUL endroit où il se calcule
(R-708 : deux écritures d'une même chose divergent toujours) ; le juge des stratégies l'appelle dans
`jouer_une_entree`, la seule mécanique d'achat-vente du juge et de la moulinette.

LES DEUX PARTS DU GLISSEMENT ET CE QUI EST DÉJÀ COMPTÉ (confrontation à R-602 et R-607, REGISTRE) :
  ① LE SAUT À L'OUVERTURE SOUS LE STOP (vente « SL_GAP ») : R-607 ② (décision de Jean-Luc du 27-09-2026 à 15h17)
     compte DÉJÀ le prix réel d'ouverture, pire que le stop. Ce glissement est donc DÉJÀ DANS LE GAIN : ce module le
     MESURE (`glissement_des_ventes_sur_stop`) et l'affiche, il ne le RETIRE PAS une seconde fois (pas de double compte).
     R-602 (objectif et stop touchés la même séance, sans saut : on compte la perte) traite un DOUTE sur l'ordre des
     seuils, pas un écart de prix : elle ne compte aucune part du glissement.
  ② L'ÉCART ACHAT-VENTE (la « fourchette ») : aucun calcul du projet ne le comptait. Il est ESTIMÉ à partir des
     prix quotidiens, par DEUX estimateurs publiés, calculés sur les MÊMES séances (celles d'avant l'ordre) :
     • L'ESTIMATEUR PRINCIPAL, « EDGE » : Ardia, Guidotti et Kroencke, « Efficient estimation of bid-ask spreads
       from open, high, low, and close prices », Journal of Financial Economics 161, 2024, article 103916,
       doi 10.1016/j.jfineco.2024.103916 (référence vérifiée le 27-11-2026, lot W2e-FIX, sur la page des auteurs et
       la notice du paquet R « bidask » au CRAN, version 2.1.5). Il lit l'ouverture, le plus haut, le plus bas et la
       clôture. La formule est celle du programme Python publié par les auteurs (paquet « bidask », fichier
       python/bidask/edge.py du dépôt github.com/eguidotti/bidask, licence MIT), transcrite sans numpy dans `edge`.
       CALIBRÉ : `edge` rend les trois valeurs que les auteurs ont publiées dans leurs épreuves (python/tests/
       test_edge.py et tests/testthat/test-edge.R) sur leurs données d'essai (pseudocode/ohlc.csv et ohlc-miss.csv,
       recopiées dans temoins/) : 0.0101849034905478, −0.016889917516422 (dix premières lignes, signé) et
       0.01013284969780197 (données à trous) — épreuve E1 du lot W2e-FIX.
       Pourquoi lui : il est « asymptotiquement sans biais » et de variance minimale, et les auteurs montrent qu'il
       domine les autres estimateurs tirés des prix de transaction (résumé de l'article) ; dans leurs simulations,
       « CS estimates a spread of 0.04% where the actual spread used in the simulation is 1.00% » (§ simulations,
       séances à peu de transactions). LIMITE PUBLIÉE PAR LES AUTEURS, qui vaut pour NOUS : avec des prix QUOTIDIENS,
       l'estimation est biaisée VERS LE HAUT « especially when the spread is small compared to volatility », et
       « more evident in more recent periods and for larger stocks » — EDGE y donne 0.42 % aux grandes valeurs
       américaines en décembre 2021 pour 0.06 % mesurés sur les cotations (référence « HJ ») ; la cause : ramener à
       zéro (ou à sa valeur absolue) une estimation négative sur un petit échantillon (Jahan-Parvar et Zikes, 2023,
       cités par les auteurs) ; le remède publié : une fenêtre plus longue, ou des prix intrajournaliers. Nos grandes
       valeurs du CAC 40 sont exactement ce cas : le coût calculé ici est donc probablement un PLAFOND, pas une mesure
       exacte (⑨ de `edge`).
     • À CÔTÉ, CORWIN ET SCHULTZ, « A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices »,
       Journal of Finance 67(2), 2012, p. 719-760 (référence vérifiée le 27-11-2026 par le lot W2e : notice RePEc
       bla:jfinan:v:67:y:2012:i:2:p:719-760 ; formule relue dans le document de travail NBER des auteurs, 2009, et
       dans le paquet R « bidask » et un programme Python publié : `ecart_de_deux_seances`). Il est CALCULÉ ET
       AFFICHÉ, il ne retire rien au gain par défaut.
     Un ordre paie la MOITIÉ de l'écart ; ce coût est AJOUTÉ (retranché du gain) par `cout_du_glissement`.

QUELS ORDRES PAIENT (ORDRES_QUI_PAIENT) : l'ACHAT se fait à l'ouverture du lendemain du signal (R-601, REGISTRE :
« Entrée Open J+1, JAMAIS au close ») ; à Euronext Paris, l'ouverture est une ENCHÈRE (pré-ouverture à 7h15, fixage
à 9h00) qui fixe un PRIX UNIQUE, le prix d'ouverture de nos données (BACKLOG A-1068 ①, source newtrading.io ;
horaires relus le 27-11-2026 sur la page « Transaction rules Paris » de Keytrade : fixage 9h00, fixage de clôture
17h35) : à ce prix, acheteurs et vendeurs paient le même prix, AUCUNE demi-fourchette. Seules les ventes faites
PENDANT la séance continue la paient : l'objectif (motif « TP ») et le stop (motif « SL ») touchés en séance. Une
vente au prix d'OUVERTURE (sauts « SL_GAP », « TP_GAP » ; échéance sans cours, R-112 ②) ou de CLÔTURE (échéance
« HORIZON », fin des données) se fait à une enchère et ne la paie pas. THÉORIQUE pour la clôture : que notre clôture
soit le prix de l'enchère de clôture n'est pas mesuré. La lecture prudente, « les_deux » (les deux ordres paient),
est calculée et affichée à côté (`sensibilite_du_glissement`).

UNITÉS (elles voyagent avec les noms, R-708) : `_fraction` = fraction du prix (0,001 = 0,1 %) ; `_eur` = euros.
"""
import math

# LA FENÊTRE DE L'ESTIMATION : Corwin et Schultz (2012) moyennent les écarts de deux séances sur un MOIS (« we set all
# negative two-day spreads to zero before calculating monthly averages », document NBER 2009, §2) ; un mois de bourse
# compte environ 21 séances. CHOIX TECHNIQUE du lot W2e, à verser dans la table « LES SEUILS DE CETTE LOI » (défaut
# R5-12 du relecteur Cowork : les seuils absents de la table s'écrivent dans le code).
FENETRE_DE_L_ECART_SEANCES = 21

# QUELS ORDRES PAIENT LA DEMI-FOURCHETTE (voir l'en-tête). « enchere_gratuite » : seules les ventes en séance
# continue paient (consigne du Chat au lot W2e-FIX du 27-11-2026, tirée de R-601 et d'A-1068 ① ; la question 3 de la
# note du lot W2e reste à confirmer par Jean-Luc) ; « les_deux » : l'achat et la vente paient (la lecture prudente,
# affichée à côté).
ORDRES_QUI_PAIENT = ("enchere_gratuite", "les_deux")
ORDRES_QUI_PAIENT_PAR_DEFAUT = "enchere_gratuite"
# Les motifs de `MODULE_POSITIONS.vendre` dont le prix est atteint PENDANT la séance continue (le seuil lui-même) :
# l'objectif et le stop touchés en séance. Tout autre motif (SL_GAP, TP_GAP : l'ouverture ; HORIZON : la clôture ou
# l'ouverture ; FIN_DES_DONNEES : la dernière clôture) est un prix d'enchère.
MOTIFS_VENDUS_EN_SEANCE = ("TP", "SL")

# LES DEUX ESTIMATEURS DE L'ÉCART (voir l'en-tête) ; le principal retire le coût du gain, l'autre s'affiche.
ESTIMATEURS = ("EDGE", "CS")
ESTIMATEUR_PRINCIPAL = "EDGE"

def ecart_de_deux_seances(veille, jour):
    """Rend l'écart achat-vente estimé sur deux séances consécutives (Corwin et Schultz, 2012), ou None.

    ① RÔLE — Estimer la fourchette achat-vente d'une valeur à partir des plus hauts et plus bas de deux séances.
    ② CONTEXTE D'APPEL — `ecart_cs_avant`, pour chaque paire de séances de la fenêtre ; les épreuves du lot W2e.
    ③ ENTRÉE — `veille`, `jour` : deux séances consécutives d'une valeur, dictionnaires portant `high`, `low`, `close`.
    ④ CONDITIONS D'ENTRÉE — Prix strictement positifs ; sinon, ou si un prix manque, la fonction rend None.
    ⑤ SORTIE — UNE valeur : l'écart S en fraction du prix (≥ 0), ou None si les prix ne le permettent pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① AJUSTEMENT DE LA NUIT (document NBER, §2.1) : si le plus bas du jour est au-dessus de la clôture
      de la veille, le prix a monté pendant la nuit : on retire cette montée au plus haut et au plus bas du jour ; si
      le plus haut du jour est sous la clôture de la veille, on ajoute la baisse · ② β = [ln(H₁/L₁)]² + [ln(H₂/L₂)]²
      (les deux séances) · ③ γ = [ln(H/L)]², H et L le plus haut et le plus bas des DEUX séances · ④ α = (√(2β) − √β)
      ÷ (3 − 2√2) − √(γ ÷ (3 − 2√2)) · ⑤ S = 2(e^α − 1) ÷ (1 + e^α) · ⑥ un S négatif vaut 0 (les auteurs mettent à zéro
      les écarts négatifs de deux séances avant de moyenner).
    ⑦ UNITÉ — Fraction du prix (0,001 = 0,1 %).
    ⑧ POURQUOI — Décision A-1068 : mesurer l'écart à partir des plus hauts et plus bas que nous avons ; l'idée de la
      méthode : le plus haut d'une séance est presque toujours un achat (payé au prix vendeur) et le plus bas une vente
      (au prix acheteur), donc l'étendue d'une séance mêle volatilité et fourchette ; la volatilité croît avec la durée,
      la fourchette non : comparer une séance et deux séances les sépare.
    ⑨ CE QUI CLOCHE — ① La méthode suppose une fourchette constante sur les deux séances et des prix continus ; sur une
      séance très calme (plus haut = plus bas) elle rend souvent 0. ② Elle mesure la fourchette des transactions de la
      séance, pas celle de l'enchère d'ouverture où nous achetons (voir ORDRES_QUI_PAIENT).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; ne lève pas sur un prix manquant ou nul.
      [sort: non]
    """
    try:
        h1, l1 = float(veille["high"]), float(veille["low"])
        h2, l2, c1 = float(jour["high"]), float(jour["low"]), float(veille["close"])
    except (KeyError, TypeError, ValueError):
        return None
    if min(h1, l1, h2, l2, c1) <= 0 or h1 < l1 or h2 < l2:
        return None
    if l2 > c1:                       # montée pendant la nuit
        h2, l2 = h2 - (l2 - c1), c1
    elif h2 < c1:                     # baisse pendant la nuit
        h2, l2 = c1, l2 + (c1 - h2)
    beta = math.log(h1 / l1) ** 2 + math.log(h2 / l2) ** 2
    gamma = math.log(max(h1, h2) / min(l1, l2)) ** 2
    k = 3.0 - 2.0 * math.sqrt(2.0)
    alpha = (math.sqrt(2.0 * beta) - math.sqrt(beta)) / k - math.sqrt(gamma / k)
    s = 2.0 * (math.exp(alpha) - 1.0) / (1.0 + math.exp(alpha))
    return max(0.0, s)


def _nanmoyenne(xs):
    """Rend la moyenne des valeurs qui ne sont pas NaN, ou NaN s'il n'y en a aucune (le `nanmean` de numpy).

    ① RÔLE — La moyenne « en ignorant les manques » de l'estimateur EDGE, sans numpy.
    ② CONTEXTE D'APPEL — `edge`, onze fois.
    ③ ENTRÉE — `xs` : une liste de nombres (float, NaN compris).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un float, NaN si toutes les valeurs manquent ou la liste est vide.
      [rend: 1]
    ⑥ TRAITEMENT — garder les valeurs non NaN, moyenne.
    ⑦ UNITÉ — Celle des valeurs.
    ⑧ POURQUOI — Le programme des auteurs utilise `np.nanmean` ; le même sens, sans dépendance.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    v = [x for x in xs if not math.isnan(x)]
    return sum(v) / len(v) if v else float("nan")


def edge(ouv, haut, bas, clo, signe=False):
    """Rend l'écart achat-vente estimé par EDGE (Ardia, Guidotti et Kroencke, 2024) sur une suite de séances, ou NaN.

    ① RÔLE — L'estimateur PRINCIPAL de la fourchette, transcription du programme publié par les auteurs.
    ② CONTEXTE D'APPEL — `ecart_edge_avant` ; l'épreuve de calibrage E1 du lot W2e-FIX.
    ③ ENTRÉE — Quatre listes de même longueur, dans l'ordre du temps : `ouv`, `haut`, `bas`, `clo` (prix ; None ou NaN
      pour un prix manquant) · `signe` : rendre l'estimation signée (vrai) ou sa valeur absolue (faux, le défaut des
      auteurs).
    ④ CONDITIONS D'ENTRÉE — Longueurs égales (sinon ValueError, comme les auteurs) ; prix > 0 quand ils sont donnés.
    ⑤ SORTIE — UNE valeur : l'écart en fraction du prix (0,01 = 1 %, la convention des auteurs), NaN si moins de trois
      séances, moins de deux séances « actives » (τ = 1), ou une probabilité po ou pc nulle.
      [rend: 1]
    ⑥ TRAITEMENT — Ligne pour ligne le fichier python/bidask/edge.py des auteurs : ① logarithmes o, h, l, c et
      m = (h + l) ÷ 2 · ② décaler d'une séance (h1, l1, c1, m1 = la veille) · ③ rendements r1 = m − o, r2 = o − m1,
      r3 = m − c1, r4 = c1 − m1, r5 = o − c1 · ④ indicatrices τ = (h ≠ l ou l ≠ c1), po1 = τ·(o ≠ h), po2 = τ·(o ≠ l),
      pc1 = τ·(c1 ≠ h1), pc2 = τ·(c1 ≠ l1), NaN si un prix manque · ⑤ pt = moy(τ), po = moy(po1) + moy(po2),
      pc = moy(pc1) + moy(pc2) ; NaN si Στ < 2 ou po = 0 ou pc = 0 · ⑥ d1 = r1 − moy(r1)÷pt·τ (de même d3, d5) ·
      ⑦ x1 = −4÷po·d1·r2 − 4÷pc·d3·r4 ; x2 = −4÷po·d1·r5 − 4÷pc·d5·r4 · ⑧ e1, e2 leurs moyennes, v1, v2 leurs
      variances · ⑨ s² = (v2·e1 + v1·e2) ÷ (v1 + v2) si v1 + v2 > 0, sinon (e1 + e2) ÷ 2 · ⑩ s = √|s²|, du signe de s²
      si `signe`. Toutes les moyennes ignorent les NaN (`_nanmoyenne`).
    ⑦ UNITÉ — Fraction du prix.
    ⑧ POURQUOI — A-1068 (b) 2 : mesurer l'écart avec les prix que nous avons ; consigne du lot W2e-FIX : l'estimateur
      vérifié des auteurs comme estimateur principal, Corwin-Schultz à côté. CALIBRÉ sur les trois chiffres publiés
      par les auteurs (voir l'en-tête du module).
    ⑨ CE QUI CLOCHE — ① BIAIS VERS LE HAUT PUBLIÉ par les auteurs pour les grandes valeurs, les périodes récentes et
      les petites fenêtres de prix quotidiens, dû à la valeur absolue (ou au zéro) imposée à une estimation négative :
      sur 22 séances, le coût est probablement surévalué (voir l'en-tête) ; la version signée moyennée sur une longue
      période l'éviterait, mais un coût d'ordre ne peut pas être négatif — question à Jean-Luc (note du lot).
      ② `signe` à faux comme les auteurs par défaut. ③ Sommes en flottants Python, ordre de numpy non garanti :
      écart au chiffre publié de l'ordre de 1e-15 (mesuré par E1).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si les longueurs diffèrent.
      [sort: non]
    """
    n = len(ouv)
    if len(haut) != n or len(bas) != n or len(clo) != n:
        raise ValueError("ouverture, plus haut, plus bas et clôture doivent avoir la même longueur")
    if n < 3:
        return float("nan")
    nan = float("nan")

    def lg(x):
        """Rend le logarithme d'un prix, NaN pour un prix manquant.

        ① RÔLE — Les logarithmes de `edge`.
        ② CONTEXTE D'APPEL — `edge`, une fois par prix.
        ③ ENTRÉE — `x` : un prix, None ou NaN.
        ④ CONDITIONS D'ENTRÉE — Un prix donné est > 0.
        ⑤ SORTIE — UNE valeur, un float.
          [rend: 1]
        ⑥ TRAITEMENT — None ou NaN → NaN ; sinon ln.
        ⑦ UNITÉ — Logarithme d'un prix.
        ⑧ POURQUOI — Le `np.log` des auteurs rend NaN sur NaN.
        ⑨ CE QUI CLOCHE — Un prix ≤ 0 lève (ValueError de math.log).
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main ou lève.
          [sort: non]
        """
        if x is None:
            return nan
        x = float(x)
        return nan if math.isnan(x) else math.log(x)
    o_, h_, l_, c_ = [lg(x) for x in ouv], [lg(x) for x in haut], [lg(x) for x in bas], [lg(x) for x in clo]
    m_ = [(a + b) / 2.0 for a, b in zip(h_, l_)]
    h1, l1, c1, m1 = h_[:-1], l_[:-1], c_[:-1], m_[:-1]
    o, h, l, m = o_[1:], h_[1:], l_[1:], m_[1:]
    k = range(n - 1)
    r1 = [m[i] - o[i] for i in k]
    r2 = [o[i] - m1[i] for i in k]
    r3 = [m[i] - c1[i] for i in k]
    r4 = [c1[i] - m1[i] for i in k]
    r5 = [o[i] - c1[i] for i in k]

    def ind(a, b, c=None, d=None):
        """Rend l'indicatrice « différents » des auteurs (1.0 ou 0.0), NaN si un prix manque.

        ① RÔLE — Les indicatrices τ, po, pc de `edge`.
        ② CONTEXTE D'APPEL — `edge`.
        ③ ENTRÉE — `a`, `b` : deux logarithmes (a ≠ b) ; `c`, `d` : deux de plus, facultatifs (a ≠ b ou c ≠ d).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur, un float.
          [rend: 1]
        ⑥ TRAITEMENT — NaN si une entrée est NaN, sinon la comparaison en 1.0 ou 0.0.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Le `np.where(np.isnan(...), np.nan, ...)` des auteurs.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        vals = (a, b) if c is None else (a, b, c, d)
        if any(math.isnan(x) for x in vals):
            return nan
        return float(a != b) if c is None else float((a != b) or (c != d))
    tau = [ind(h[i], l[i], l[i], c1[i]) if not math.isnan(c1[i]) else nan for i in k]
    po1 = [tau[i] * ind(o[i], h[i]) for i in k]
    po2 = [tau[i] * ind(o[i], l[i]) for i in k]
    pc1 = [tau[i] * ind(c1[i], h1[i]) for i in k]
    pc2 = [tau[i] * ind(c1[i], l1[i]) for i in k]
    pt = _nanmoyenne(tau)
    po = _nanmoyenne(po1) + _nanmoyenne(po2)
    pc = _nanmoyenne(pc1) + _nanmoyenne(pc2)
    if sum(x for x in tau if not math.isnan(x)) < 2 or po == 0 or pc == 0:
        return nan
    mr1, mr3, mr5 = _nanmoyenne(r1), _nanmoyenne(r3), _nanmoyenne(r5)
    d1 = [r1[i] - mr1 / pt * tau[i] for i in k]
    d3 = [r3[i] - mr3 / pt * tau[i] for i in k]
    d5 = [r5[i] - mr5 / pt * tau[i] for i in k]
    x1 = [-4.0 / po * d1[i] * r2[i] + -4.0 / pc * d3[i] * r4[i] for i in k]
    x2 = [-4.0 / po * d1[i] * r5[i] + -4.0 / pc * d5[i] * r4[i] for i in k]
    e1, e2 = _nanmoyenne(x1), _nanmoyenne(x2)
    v1 = _nanmoyenne([x * x for x in x1]) - e1 ** 2
    v2 = _nanmoyenne([x * x for x in x2]) - e2 ** 2
    vt = v1 + v2
    s2 = (v2 * e1 + v1 * e2) / vt if vt > 0 else (e1 + e2) / 2.0
    s = math.sqrt(abs(s2))
    if signe:
        s = math.copysign(s, s2) if s2 != 0 else 0.0
    return float(s)


def ecart_cs_avant(serie, j, fenetre=FENETRE_DE_L_ECART_SEANCES):
    """Rend l'écart Corwin-Schultz moyen des `fenetre` paires de séances qui PRÉCÈDENT la séance `j`, ou None.

    ① RÔLE — Donner, pour un ordre passé à la séance `j`, l'écart Corwin-Schultz estimé avec ce qui était connu AVANT
      cette séance.
    ② CONTEXTE D'APPEL — `ecart_estime_avant` ; l'épreuve anti-avenir du lot W2e.
    ③ ENTRÉE — `serie` : la série d'une valeur (séances dans l'ordre) · `j` : le rang de la séance de l'ordre ·
      `fenetre` : le nombre de paires, en séances.
    ④ CONDITIONS D'ENTRÉE — `0 <= j < len(serie)` ; `fenetre >= 1`.
    ⑤ SORTIE — UNE valeur : la moyenne des écarts des paires (k − 1, k) pour k de j − fenetre à j − 1, en fraction,
      ou None si aucune paire n'est calculable (début de série).
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les paires dont la seconde séance est STRICTEMENT AVANT `j` · ② garder les écarts
      calculables · ③ moyenne.
    ⑦ UNITÉ — Fraction du prix.
    ⑧ POURQUOI — Aucune donnée postérieure à l'ordre n'est lue, pas même la séance de l'ordre : l'épreuve anti-avenir
      (A-674, A-692) le vérifie. Le coût d'un ordre ne doit pas dépendre de ce qui arrive après lui.
    ⑨ CE QUI CLOCHE — ① Une série coupée par un trou mêle deux séances séparées par la suspension en une « paire » ;
      l'ajustement de la nuit en absorbe une partie, pas tout (non mesuré). ② Les écarts négatifs ramenés à 0 avant la
      moyenne (règle des auteurs) poussent l'estimation vers le haut (voir l'en-tête, Jahan-Parvar et Zikes).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    vals = []
    for k in range(max(1, j - fenetre), j):
        s = ecart_de_deux_seances(serie[k - 1], serie[k])
        if s is not None:
            vals.append(s)
    return sum(vals) / len(vals) if vals else None


def ecart_edge_avant(serie, j, fenetre=FENETRE_DE_L_ECART_SEANCES):
    """Rend l'écart EDGE estimé sur les séances qui PRÉCÈDENT la séance `j` — les mêmes que `ecart_cs_avant` —, ou None.

    ① RÔLE — Donner, pour un ordre passé à la séance `j`, l'écart EDGE estimé avec ce qui était connu AVANT elle.
    ② CONTEXTE D'APPEL — `ecart_estime_avant` ; les épreuves du lot W2e-FIX.
    ③ ENTRÉE — `serie`, `j`, `fenetre` : ceux de `ecart_cs_avant`.
    ④ CONDITIONS D'ENTRÉE — Celles de `ecart_cs_avant` ; chaque séance porte `open`, `high`, `low`, `close`.
    ⑤ SORTIE — UNE valeur : l'écart en fraction, ou None si EDGE rend NaN (moins de trois séances, séances figées).
      [rend: 1]
    ⑥ TRAITEMENT — `edge` sur les séances de rang max(0, j − fenetre − 1) à j − 1 : `fenetre` + 1 séances, soit
      `fenetre` paires, les mêmes paires que Corwin-Schultz (la seconde séance de chaque paire est avant `j`).
    ⑦ UNITÉ — Fraction du prix.
    ⑧ POURQUOI — Comparer les deux estimateurs sur les MÊMES séances ; ne rien lire de l'ordre ni d'après (A-674).
    ⑨ CE QUI CLOCHE — Le biais vers le haut des petites fenêtres (⑨ ① de `edge`).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    b = serie[max(0, j - fenetre - 1):j]
    s = edge([x.get("open") for x in b], [x.get("high") for x in b], [x.get("low") for x in b],
             [x.get("close") for x in b])
    return None if math.isnan(s) else s


def ecart_estime_avant(serie, j, fenetre=FENETRE_DE_L_ECART_SEANCES, estimateur=ESTIMATEUR_PRINCIPAL):
    """Rend l'écart estimé avant la séance `j` par l'estimateur nommé, ou None.

    ① RÔLE — Le choix de l'estimateur, à UN SEUL endroit.
    ② CONTEXTE D'APPEL — `cout_du_glissement`, `sensibilite_du_glissement` ; les épreuves des lots W2e et W2e-FIX.
    ③ ENTRÉE — `serie`, `j`, `fenetre` : ceux de `ecart_cs_avant` · `estimateur` : une valeur d'ESTIMATEURS.
    ④ CONDITIONS D'ENTRÉE — `estimateur` connu, sinon ValueError (aucune valeur par défaut silencieuse).
    ⑤ SORTIE — UNE valeur : l'écart en fraction, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — « EDGE » → `ecart_edge_avant` ; « CS » → `ecart_cs_avant`.
    ⑦ UNITÉ — Fraction du prix.
    ⑧ POURQUOI — Afficher la sensibilité aux deux estimateurs sans écrire deux chemins de coût.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    if estimateur == "EDGE":
        return ecart_edge_avant(serie, j, fenetre)
    if estimateur == "CS":
        return ecart_cs_avant(serie, j, fenetre)
    raise ValueError("estimateur inconnu : %r (attendu : %s)" % (estimateur, ESTIMATEURS))


def _capital():
    """Rend le capital simulé d'un trade, lu dans MODULE_POSITIONS.

    ① RÔLE — Lire `MODULE_POSITIONS.CAPITAL`.
    ② CONTEXTE D'APPEL — `_cout`, à chaque opération.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — MODULE_POSITIONS importable.
    ⑤ SORTIE — UNE valeur : le capital simulé d'un trade.
      [rend: 1]
    ⑥ TRAITEMENT — Importer le module, lire la constante.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — R-708 : un chiffre qui existe ailleurs ne se recopie pas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ImportError.
      [sort: non]
    """
    import MODULE_POSITIONS
    return float(MODULE_POSITIONS.CAPITAL)


def _rang_de_vente(serie, j_achat, vente):
    """Rend le rang de la séance de vente dans la série.

    ① RÔLE — Trouver la séance de la vente rendue par `MODULE_POSITIONS.vendre`.
    ② CONTEXTE D'APPEL — `cout_du_glissement`, `sensibilite_du_glissement`.
    ③ ENTRÉE — `serie`, `j_achat`, `vente` (clé `date_sortie`).
    ④ CONDITIONS D'ENTRÉE — La date de vente est dans la série, au rang `j_achat` ou après.
    ⑤ SORTIE — UNE valeur : le rang.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir la série depuis `j_achat`.
    ⑦ UNITÉ — Rang de séance.
    ⑧ POURQUOI — Le coût de la vente se lit avec les séances d'avant SA séance.
    ⑨ CE QUI CLOCHE — Coût linéaire.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ValueError (date absente).
      [sort: non]
    """
    for k in range(j_achat, len(serie)):
        if serie[k]["date"] == vente["date_sortie"]:
            return k
    raise ValueError("date de vente %r absente de la série" % (vente["date_sortie"],))


def _cout(ea, ev, vente, ordres_qui_paient):
    """Rend le coût d'une opération à partir des deux écarts estimés.

    ① RÔLE — LA formule du coût, à UN SEUL endroit (R-708) : `cout_du_glissement` et `sensibilite_du_glissement`
      l'appellent.
    ② CONTEXTE D'APPEL — Ces deux fonctions.
    ③ ENTRÉE — `ea`, `ev` : les écarts (fraction ou None) estimés avant l'achat et avant la vente · `vente` : le
      dictionnaire de `MODULE_POSITIONS.vendre` (`pe`, `px`, `motif`) · `ordres_qui_paient` : une valeur de
      ORDRES_QUI_PAIENT.
    ④ CONDITIONS D'ENTRÉE — `ordres_qui_paient` connu, sinon ValueError.
    ⑤ SORTIE — UN dictionnaire de quatre clés : `demi_ecart_achat_fraction`, `demi_ecart_vente_fraction` (None si
      non estimable : compté 0, et `estime` le dit), `glissement_eur` (≥ 0), `estime` (vrai si chaque demi-écart PAYÉ
      a pu être estimé).
      [rend: 1]
    ⑥ TRAITEMENT — ① demi-écarts = moitiés des écarts · ② « les_deux » : l'achat et la vente paient ;
      « enchere_gratuite » : l'achat (enchère d'ouverture) ne paie pas, la vente paie si son motif est dans
      MOTIFS_VENDUS_EN_SEANCE · ③ coût = capital × demi-écart d'achat + quantité × prix de vente × demi-écart de vente.
    ⑦ UNITÉ — Fractions du prix ; coût en euros.
    ⑧ POURQUOI — A-1068 (c) : « le coût mesuré est AJOUTÉ au calcul des gains » ; R-601 et l'enchère d'ouverture.
    ⑨ CE QUI CLOCHE — ① Un objectif touché en séance est un ordre à cours limité, qui se place dans le carnet : il est
      compté comme payant la demi-fourchette (consigne du lot), alors qu'un ordre limité attendu n'en paie pas
      d'ordinaire — choix prudent, non mesuré. ② Un stop qui part en séance au-delà du stop (un glissement de prix)
      n'est pas vu : la vente « SL » est supposée au stop exact plus la demi-fourchette.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    if ordres_qui_paient not in ORDRES_QUI_PAIENT:
        raise ValueError("ordres_qui_paient inconnu : %r (attendu : %s)" % (ordres_qui_paient, ORDRES_QUI_PAIENT))
    da = None if ea is None else ea / 2.0
    dv = None if ev is None else ev / 2.0
    paie_achat = ordres_qui_paient == "les_deux"
    paie_vente = ordres_qui_paient == "les_deux" or vente["motif"] in MOTIFS_VENDUS_EN_SEANCE
    cap = _capital()
    q = cap / float(vente["pe"])
    cout = (cap * (da or 0.0) if paie_achat else 0.0) + (q * float(vente["px"]) * (dv or 0.0) if paie_vente else 0.0)
    estime = (not paie_achat or da is not None) and (not paie_vente or dv is not None)
    return {"demi_ecart_achat_fraction": da, "demi_ecart_vente_fraction": dv, "glissement_eur": cout,
            "estime": estime}


def cout_du_glissement(serie, j_achat, vente, ordres_qui_paient=ORDRES_QUI_PAIENT_PAR_DEFAUT,
                       fenetre=FENETRE_DE_L_ECART_SEANCES, estimateur=ESTIMATEUR_PRINCIPAL):
    """Rend le coût de la demi-fourchette d'une opération (achat à la séance `j_achat`, vente rendue par `vendre`).

    ① RÔLE — Chiffrer, en euros, ce que la fourchette achat-vente retire au gain d'une opération simulée.
    ② CONTEXTE D'APPEL — `JUGE_DES_STRATEGIES.jouer_une_entree`, à chaque opération (le juge, la moulinette,
      l'étalon de hasard) ; les épreuves des lots W2e et W2e-FIX.
    ③ ENTRÉE — `serie` : la série de la valeur · `j_achat` : le rang de la séance d'achat · `vente` : le dictionnaire
      de `MODULE_POSITIONS.vendre` (`pe`, `px`, `motif`, `date_sortie`) · `ordres_qui_paient` : une valeur de
      ORDRES_QUI_PAIENT · `fenetre` : celle de `ecart_cs_avant` · `estimateur` : une valeur d'ESTIMATEURS.
    ④ CONDITIONS D'ENTRÉE — `vente["date_sortie"]` est une date de la série ; réglages connus, sinon ValueError.
    ⑤ SORTIE — UN dictionnaire : les quatre clés de `_cout`, plus `estimateur` et `ordres_qui_paient` (ce qui a servi).
      Un demi-écart d'un ordre qui NE PAIE PAS n'est pas calculé : il vaut None (`estime` ne le compte pas).
      [rend: 1]
    ⑥ TRAITEMENT — ① rang de vente · ② écarts estimés avant l'achat et avant la vente (`ecart_estime_avant`), pour les
      seuls ordres qui paient · ③ `_cout`.
    ⑦ UNITÉ — Fractions du prix ; coût en euros.
    ⑧ POURQUOI — A-1068 (c). Par défaut l'estimateur PRINCIPAL (EDGE) et « enchere_gratuite » (R-601).
    ⑨ CE QUI CLOCHE — Ceux de `_cout` et de `edge`.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (réglage inconnu, date de vente absente).
      [sort: non]
    """
    if ordres_qui_paient not in ORDRES_QUI_PAIENT:
        raise ValueError("ordres_qui_paient inconnu : %r (attendu : %s)" % (ordres_qui_paient, ORDRES_QUI_PAIENT))
    j_vente = _rang_de_vente(serie, j_achat, vente)
    # un écart que personne ne paie n'est pas calculé (le juge appelle cette fonction à chaque tirage du hasard)
    paie_achat = ordres_qui_paient == "les_deux"
    paie_vente = paie_achat or vente["motif"] in MOTIFS_VENDUS_EN_SEANCE
    ea = ecart_estime_avant(serie, j_achat, fenetre, estimateur) if paie_achat else None
    ev = ecart_estime_avant(serie, j_vente, fenetre, estimateur) if paie_vente else None
    r = _cout(ea, ev, vente, ordres_qui_paient)
    r.update(estimateur=estimateur, ordres_qui_paient=ordres_qui_paient)
    return r


def cle_de_sensibilite(estimateur, ordres_qui_paient):
    """Rend la clé d'une combinaison de la sensibilité, « ESTIMATEUR|ordres ».

    ① RÔLE — Nommer une combinaison (estimateur, ordres qui paient) d'une seule façon.
    ② CONTEXTE D'APPEL — `sensibilite_du_glissement` ; l'affichage du juge ; les épreuves.
    ③ ENTRÉE — `estimateur`, `ordres_qui_paient`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un texte, par exemple « CS|les_deux ».
      [rend: 1]
    ⑥ TRAITEMENT — Joindre par « | ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une clé texte s'écrit dans un fichier et se somme dans `resumer`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return "%s|%s" % (estimateur, ordres_qui_paient)


def sensibilite_du_glissement(serie, j_achat, vente, fenetre=FENETRE_DE_L_ECART_SEANCES):
    """Rend le coût d'une opération pour CHAQUE combinaison d'estimateur et de lecture des ordres qui paient.

    ① RÔLE — La sensibilité demandée au lot W2e-FIX : les deux estimateurs, et « les deux ordres paient ».
    ② CONTEXTE D'APPEL — `JUGE_DES_STRATEGIES.jouer_une_entree`, à chaque opération ; les épreuves.
    ③ ENTRÉE — `serie` : la série de la valeur · `j_achat` : le rang de la séance d'achat · `vente` : le dictionnaire
      de `MODULE_POSITIONS.vendre` · `fenetre` : celle de `ecart_cs_avant`.
    ④ CONDITIONS D'ENTRÉE — Celles de `cout_du_glissement`.
    ⑤ SORTIE — UN dictionnaire de len(ESTIMATEURS) × len(ORDRES_QUI_PAIENT) clés (`cle_de_sensibilite`), chacune le
      coût en euros (quatre aujourd'hui).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque estimateur : les deux écarts une fois ; pour chaque lecture : `_cout`.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — Montrer de combien le gain dépend de choix non mesurés, sans en retirer plus d'un du gain.
    ⑨ CE QUI CLOCHE — Recalcule les écarts du principal déjà calculés par `cout_du_glissement` (coût double, mesuré
      dans la note du lot).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ValueError (date de vente absente).
      [sort: non]
    """
    j_vente = _rang_de_vente(serie, j_achat, vente)
    out = {}
    for est in ESTIMATEURS:
        ea = ecart_estime_avant(serie, j_achat, fenetre, est)
        ev = ecart_estime_avant(serie, j_vente, fenetre, est)
        for oqp in ORDRES_QUI_PAIENT:
            out[cle_de_sensibilite(est, oqp)] = _cout(ea, ev, vente, oqp)["glissement_eur"]
    return out


def glissement_des_ventes_sur_stop(ops, sl):
    """Mesure l'écart entre le stop prévu et le prix obtenu, ventes sur stop et ouvertures en trou comprises.

    ① RÔLE — A-1068 (b) 1 : « pour les ventes sur stop, l'écart entre le stop prévu et le prix obtenu, ouvertures en
      trou comprises ».
    ② CONTEXTE D'APPEL — L'épreuve et la mesure du lot W2e ; à venir : l'affichage du verdict.
    ③ ENTRÉE — `ops` : les opérations de `JUGE_DES_STRATEGIES.jouer` (`pe`, `px`, `motif`) · `sl` : le stop de la
      fiche, en fraction.
    ④ CONDITIONS D'ENTRÉE — Les motifs sont ceux de `MODULE_POSITIONS.vendre`.
    ⑤ SORTIE — UNE valeur : un dictionnaire : `ventes_sur_stop` (motifs SL et SL_GAP), `dont_en_trou` (SL_GAP),
      `ecart_moyen_fraction` (moyenne de (stop − prix obtenu) ÷ stop), `ecart_total_eur` (somme de quantité × (stop −
      prix obtenu)) et `deja_compte_dans_le_gain` (toujours vrai : R-607 ② compte le prix réel d'ouverture).
      [rend: 1]
    ⑥ TRAITEMENT — ① stop = `MODULE_POSITIONS.seuils_de_vente(pe, 0, sl)` (le seul calcul des seuils) · ② pour chaque
      vente SL ou SL_GAP, l'écart au stop · ③ sommes et moyenne.
    ⑦ UNITÉ — Fraction du stop ; euros.
    ⑧ POURQUOI — Montrer ce que le saut coûte, sans le recompter : il est déjà dans le gain (R-607 ②).
    ⑨ CE QUI CLOCHE — Une vente « SL » en séance est supposée faite au stop exact : son écart vaut 0 ici ; la
      demi-fourchette de `cout_du_glissement` est la seule part qui la frappe.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; lève KeyError si une opération n'a pas ses prix.
      [sort: non]
    """
    import MODULE_POSITIONS
    cap = float(MODULE_POSITIONS.CAPITAL)
    n, n_trou, fr, eur = 0, 0, 0.0, 0.0
    for o in ops:
        if o["motif"] not in ("SL", "SL_GAP"):
            continue
        stop = MODULE_POSITIONS.seuils_de_vente(float(o["pe"]), 0.0, sl)[1]
        n += 1
        n_trou += o["motif"] == "SL_GAP"
        fr += (stop - float(o["px"])) / stop
        eur += (cap / float(o["pe"])) * (stop - float(o["px"]))
    return {"ventes_sur_stop": n, "dont_en_trou": n_trou, "ecart_moyen_fraction": fr / n if n else None,
            "ecart_total_eur": eur, "deja_compte_dans_le_gain": True}
