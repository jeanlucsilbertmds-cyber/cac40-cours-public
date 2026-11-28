#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MODULE_QUAND_JOUER — Ven 27-11-2026 (Paris), lot W2e du plan R505. SIMULATION UNIQUEMENT : aucun ordre réel.

À QUOI SERT CE MODULE, EN FRANÇAIS SIMPLE. Le réglage « QUAND JOUER » dit dans quels types de marché une version
d'une stratégie joue : « toujours », ou seulement en marché agité, calme, en hausse, en baisse, ou leurs croisements.
Décision de Jean-Luc du 27-11-2026 à 16h30 (BACKLOG A-1079), après sa question de 16h27 : « ça suffit pas de dire si
elle est bonne ou pas bonne, mais dans quel environnement elle est bonne ». La loi R-505 v2 (étape 3) : le type de
marché est « MESURÉ LE JOUR MÊME par un indicateur connu à la clôture — par exemple la météo du marché (indice
au-dessus ou au-dessous de sa moyenne des 200 séances, programmes/METEO_DU_MARCHE.py, A-615) et l'agitation des 20
dernières séances —, JAMAIS par la datation après coup de l'étape 2 ».

LE DÉCOUPAGE DU JOUR MÊME EST CELUI QUI DÉCIDE (A-1105). Le relecteur Cowork (défaut R5-2, BLOQUANT, 27-11-2026 à
19h50) a montré que la loi porte DEUX découpages du marché : celui de l'étape 2, daté APRÈS COUP
(programmes/DATER_LES_TYPES_DE_MARCHE.py, lot L5), et celui « du jour même ». Décision de Jean-Luc du 27-11-2026 à
22h15 (A-1105, option 1 : « Alors le 1, mais là, pareillement, il faut tout mettre dans l'explication de comment on
sélectionne une stratégie en autoportant ») : le DÉCOUPAGE DU JOUR MÊME sert à dire quels jours une version joue et
à tirer le jour au hasard du contrôle 2 ; l'après coup ne sert qu'à l'affichage des époques et au contrôle « aucune
époque perdante à coup sûr ». Raison donnée à Jean-Luc : un expert ne compare une décision qu'à ce qui était possible
au moment de la prendre. `decoupage_par_defaut(racine)` rend donc le découpage du jour même, avec les réglages du
fichier du lot L5 (donnees/REGLAGES_DES_TYPES_DE_MARCHE.csv : fenêtre de volatilité, centile d'agitation). La
fonction `admis` garde son paramètre et refuse toujours de jouer un réglage autre que « toujours » SANS découpage
donné : le choix se fait chez l'appelant qui connaît la racine (le juge), jamais en silence ici.
LES DEUX CALCULS DU JOUR MÊME NE SONT PAS RECOPIÉS (R-708 : deux écritures d'une même chose divergent toujours) :
la moyenne des 200 séances et le côté de la clôture viennent de `METEO_DU_MARCHE.cotes_de_la_moyenne` (le calcul du
voyant), la volatilité de `DATER_LES_TYPES_DE_MARCHE.volatilites` (lot L5). Seul le SEUIL d'agitation est calculé
ici : celui de L5 (`seuil_d_agitation`) voit toute la période, l'avenir compris ; ici, il ne voit que le passé.

LES NOMS DES TYPES sont ceux du lot L5 (HAUSSE_CALME, HAUSSE_AGITEE, BAISSE_CALME, BAISSE_AGITEE ; INCONNU tant que
l'indicateur n'est pas calculable), pour qu'une version déclarée se lise dans les deux découpages.
"""
import math
import os

TYPES_DE_MARCHE = ("HAUSSE_CALME", "HAUSSE_AGITEE", "BAISSE_CALME", "BAISSE_AGITEE")
INCONNU = "INCONNU"
TOUJOURS = "toujours"
# Les mots du réglage (« agité, calme, hausse, baisse, et leurs croisements », loi R-505 v2 étape 3) : chacun désigne
# un ensemble de types ; un réglage en réunit plusieurs par « + ».
MOTS_DU_REGLAGE = {
    "HAUSSE": frozenset({"HAUSSE_CALME", "HAUSSE_AGITEE"}),
    "BAISSE": frozenset({"BAISSE_CALME", "BAISSE_AGITEE"}),
    "CALME": frozenset({"HAUSSE_CALME", "BAISSE_CALME"}),
    "AGITE": frozenset({"HAUSSE_AGITEE", "BAISSE_AGITEE"}),
    **{t: frozenset({t}) for t in TYPES_DE_MARCHE},
}


class Decoupage:
    """Un découpage du marché : un nom, le type de chaque date, et s'il est mesuré le jour même.

    ① RÔLE — Porter le découpage passé en paramètre au réglage « quand jouer ».
    ② CONTEXTE D'APPEL — Fabriqué par `decoupage_du_jour_meme` ou `decoupage_depuis_des_lignes` ; lu par `admis`.
    ③ ENTRÉE — `nom` : texte · `types` : {date AAAA-MM-JJ : type} · `jour_meme` : vrai si chaque type n'a lu que les
      séances connues à la clôture de sa date.
    ④ CONDITIONS D'ENTRÉE — Chaque type est dans TYPES_DE_MARCHE ou vaut INCONNU (sinon ValueError).
    ⑤ SORTIE — L'objet.
      [rend: 1]
    ⑥ TRAITEMENT — Contrôler les types, garder les trois champs.
    ⑦ UNITÉ — Dates et noms de types.
    ⑧ POURQUOI — Un découpage nommé et marqué empêche de prendre l'un pour l'autre (défaut R5-2).
    ⑨ CE QUI CLOCHE — `jour_meme` est DÉCLARÉ par la fabrique, pas prouvé ici : l'épreuve anti-avenir du lot W2e le
      prouve pour `decoupage_du_jour_meme`.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """

    def __init__(self, nom, types, jour_meme):
        """Range le découpage après avoir contrôlé ses types.

        ① RÔLE — Construire un `Decoupage`.
        ② CONTEXTE D'APPEL — Les deux fabriques du module ; les épreuves du lot W2e.
        ③ ENTRÉE — `self` · `nom` · `types` · `jour_meme` : voir ③ de la classe.
        ④ CONDITIONS D'ENTRÉE — Voir ④ de la classe.
        ⑤ SORTIE — Aucune valeur (constructeur).
          [rend: rien]
        ⑥ TRAITEMENT — ① relever les types hors de TYPES_DE_MARCHE et d'INCONNU · ② lever s'il y en a · ③ ranger les
          trois attributs, les types copiés.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un type mal écrit ne doit jamais devenir « jamais joué » en silence.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main ou lève ValueError.
          [sort: non]
        """
        mauvais = sorted({t for t in types.values() if t not in TYPES_DE_MARCHE and t != INCONNU})
        if mauvais:
            raise ValueError("types de marché inconnus dans le découpage %r : %s" % (nom, mauvais))
        self.nom, self.types, self.jour_meme = nom, dict(types), bool(jour_meme)


def lire_quand_jouer(texte):
    """Lit un réglage « quand jouer » : None pour « toujours », sinon l'ensemble des types où la version joue.

    ① RÔLE — Traduire le texte d'un réglage en ensemble de types.
    ② CONTEXTE D'APPEL — `admis` ; les épreuves du lot W2e ; à venir : la lecture des versions de la moulinette.
    ③ ENTRÉE — `texte` : « toujours », ou des mots de MOTS_DU_REGLAGE réunis par « + » (« AGITE », « HAUSSE+CALME »…).
    ④ CONDITIONS D'ENTRÉE — Un texte non vide ; casse et espaces indifférents.
    ⑤ SORTIE — UNE valeur : None (toujours) ou un frozenset non vide de TYPES_DE_MARCHE.
      [rend: 1]
    ⑥ TRAITEMENT — ① « toujours » → None · ② découper sur « + » · ③ réunir les ensembles des mots.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-1079 ① : « toujours, ou seulement dans certains types de marché ».
    ⑨ CE QUI CLOCHE — « HAUSSE+BAISSE » réunit les quatre types et vaut « toujours » sauf aux jours INCONNU : il est
      accepté tel quel, pas ramené à « toujours » (il compte comme un essai de plus, A-1079 limite ②).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur un mot inconnu ou un texte vide.
      [sort: non]
    """
    t = (texte or "").strip()
    if not t:
        raise ValueError("réglage « quand jouer » vide")
    if t.lower() == TOUJOURS:
        return None
    ens = set()
    for mot in t.upper().replace(" ", "").split("+"):
        if mot not in MOTS_DU_REGLAGE:
            raise ValueError("réglage « quand jouer » : mot inconnu %r (attendu : %s, ou « toujours »)"
                             % (mot, ", ".join(sorted(MOTS_DU_REGLAGE))))
        ens |= MOTS_DU_REGLAGE[mot]
    return frozenset(ens)


def admis(quand_jouer, decoupage, date_signal):
    """Dit si une version au réglage `quand_jouer` joue un signal du jour `date_signal`.

    ① RÔLE — Le filtre du réglage, à UN SEUL endroit (R-708).
    ② CONTEXTE D'APPEL — `JUGE_DES_STRATEGIES.jouer`, à chaque signal ; les épreuves du lot W2e.
    ③ ENTRÉE — `quand_jouer` : le texte du réglage · `decoupage` : un `Decoupage`, ou None · `date_signal` : la date
      du signal (la décision se prend à sa clôture ; l'achat suit à l'ouverture, R-601).
    ④ CONDITIONS D'ENTRÉE — Un réglage autre que « toujours » EXIGE un découpage (sinon ValueError : il se choisit chez
      l'appelant, `decoupage_par_defaut`, jamais en silence ici).
    ⑤ SORTIE — UNE valeur : vrai ou faux. Une date absente du découpage ou de type INCONNU n'est PAS jouée.
      [rend: 1]
    ⑥ TRAITEMENT — ① « toujours » : vrai · ② sinon le type de la date, et son appartenance au réglage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le type du JOUR DU SIGNAL : celui que la version connaît quand elle décide.
    ⑨ CE QUI CLOCHE — Un découpage « après coup » (L5) est accepté s'il est donné (pour l'affichage des époques) :
      ce n'est pas celui qui dit où la version joue (A-1105) ; l'épreuve anti-avenir montre qu'il lit l'avenir.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève ValueError.
      [sort: non]
    """
    ens = lire_quand_jouer(quand_jouer)
    if ens is None:
        return True
    if decoupage is None:
        raise ValueError("réglage « quand jouer » = %r sans découpage du marché : l'appelant passe "
                         "decoupage_par_defaut(racine), le découpage du jour même (A-1105) ; aucun n'est pris en "
                         "silence ici" % quand_jouer)
    return decoupage.types.get(date_signal, INCONNU) in ens


def decoupage_du_jour_meme(indice, fenetre_agitation, centile_agitation, nom="jour_meme"):
    """Rend le découpage « du jour même » : sens par la moyenne des 200 séances, agitation par la volatilité récente.

    ① RÔLE — Donner, pour chaque séance de l'indice, un type de marché calculé avec les SEULES séances connues à sa
      clôture.
    ② CONTEXTE D'APPEL — `decoupage_par_defaut` (le juge, pour une fiche dont le réglage « quand jouer » n'est pas
      « toujours ») ; l'épreuve anti-avenir des lots W2e et W2e-FIX.
    ③ ENTRÉE — `indice` : {date : clôture} du CAC 40 · `fenetre_agitation` : nombre de rendements de la volatilité, en
      séances (la loi : « l'agitation des 20 dernières séances ») · `centile_agitation` : fraction (A-1064 : agité
      au-dessus du 80e centile) · `nom`.
    ④ CONDITIONS D'ENTRÉE — Clôtures positives ; `fenetre_agitation` entier ≥ 2 ; 0 < `centile_agitation` < 1. Aucune
      valeur par défaut ici : les deux réglages vivent au fichier du lot L5 (donnees/REGLAGES_DES_TYPES_DE_MARCHE.csv),
      lu par `decoupage_par_defaut`.
    ⑤ SORTIE — UNE valeur : un `Decoupage` marqué `jour_meme`.
      [rend: 1]
    ⑥ TRAITEMENT — ① SENS de chaque séance : `METEO_DU_MARCHE.cotes_de_la_moyenne` (HAUSSE si la clôture est
      STRICTEMENT au-dessus de la moyenne des 200 dernières clôtures, séance comprise ; BAISSE sinon) · ② VOLATILITÉ de
      chaque séance : `DATER_LES_TYPES_DE_MARCHE.volatilites` (écart-type de population des `fenetre_agitation`
      derniers rendements logarithmiques) · ③ SEUIL, séance par séance : la volatilité de rang int(centile × N) parmi
      les N volatilités CONNUES JUSQU'À elle, triées (le rang de `seuil_d_agitation` de L5, sans l'avenir) ; AGITÉE si
      la volatilité est strictement au-dessus · ④ INCONNU tant que moins de METEO_DU_MARCHE.SEANCES_PLUS_HAUT séances
      sont connues (le voyant n'existe pas avant), ou sans volatilité.
    ⑦ UNITÉ — Points d'indice ; volatilité en écart-type de rendement logarithmique quotidien.
    ⑧ POURQUOI — A-1079 ② : « mesuré LE JOUR MÊME par des indicateurs connus à la clôture » ; A-1105 : c'est lui qui
      décide où la version joue. Les deux calculs sont importés (R-708), demande du Chat au lot W2e-FIX.
    ⑨ CE QUI CLOCHE — ① Le rang du centile (int(centile × N)) est réécrit ici, pas la fonction de L5 : l'appeler à
      chaque séance coûterait n² log n sur 6 844 séances ; seul le rang est commun, l'épreuve A2 compare les deux.
      ② Les séances de l'indice sont celles que l'appelant donne : `decoupage_par_defaut` donne celles du calendrier
      de L5 (clôture yahoo, sinon bnains, `lire_l_indice`).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur un réglage hors domaine.
      [sort: non]
    """
    import bisect
    import METEO_DU_MARCHE as M
    import DATER_LES_TYPES_DE_MARCHE as D
    if float(fenetre_agitation) != int(float(fenetre_agitation)) or int(float(fenetre_agitation)) < 2 or \
            not (0.0 < float(centile_agitation) < 1.0):
        raise ValueError("réglages d'agitation hors domaine : fenêtre %r, centile %r" % (fenetre_agitation,
                                                                                         centile_agitation))
    f = int(float(fenetre_agitation))
    dates, dessus, _moyennes = M.cotes_de_la_moyenne(indice)
    vols = D.volatilites([float(indice[d]) for d in dates], f)
    connues, types = [], {}
    for i, d in enumerate(dates):
        vol = vols[i]
        if vol is not None:
            bisect.insort(connues, vol)
        if i + 1 < M.SEANCES_PLUS_HAUT or vol is None or dessus[i] is None:
            types[d] = INCONNU
            continue
        sens = "HAUSSE" if dessus[i] else "BAISSE"
        seuil = connues[min(len(connues) - 1, int(float(centile_agitation) * len(connues)))]
        types[d] = sens + ("_AGITEE" if vol > seuil else "_CALME")
    return Decoupage(nom, types, jour_meme=True)


_PAR_DEFAUT = {}


def decoupage_par_defaut(racine):
    """Rend LE découpage qui dit où une version joue : celui du jour même, sur l'indice et les réglages de la racine.

    ① RÔLE — Le découpage par défaut décidé par Jean-Luc le 27-11-2026 à 22h15 (A-1105, option 1).
    ② CONTEXTE D'APPEL — `JUGE_DES_STRATEGIES.decoupage_pour_la_fiche` (le juge et son voisinage, une fiche dont le
      réglage « quand jouer » n'est pas « toujours ») ; les épreuves du lot W2e-FIX. À venir : le tirage du hasard du
      contrôle 2 (lot W2a).
    ③ ENTRÉE — `racine` : la racine d'un dépôt ou d'une copie.
    ④ CONDITIONS D'ENTRÉE — La racine porte donnees/REGLAGES_DES_TYPES_DE_MARCHE.csv et l'indice que lit
      `DATER_LES_TYPES_DE_MARCHE.lire_l_indice`.
    ⑤ SORTIE — UNE valeur : un `Decoupage` du jour même, nommé « jour_meme ».
      [rend: 1]
    ⑥ TRAITEMENT — ① réglages par `DATER_LES_TYPES_DE_MARCHE.lire_les_reglages` (fenetre_de_volatilite,
      centile_d_agitation : les mêmes que la datation de l'étape 2) · ② séances et clôtures par
      `DATER_LES_TYPES_DE_MARCHE.lire_l_indice` · ③ `decoupage_du_jour_meme` · ④ gardé en mémoire par racine (le
      voisinage du juge rejoue 26 fois la même fiche).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un réglage écrit au fichier, lu par programme (R-754), jamais recopié dans le code.
    ⑨ CE QUI CLOCHE — ① La mémoire par racine ne voit pas un fichier changé pendant le même lancement. ② Les deux
      réglages portent au fichier « EN ATTENTE DU CHOIX DE JEAN-LUC (RDV1) » pour la fenêtre : ils sont lus tels quels.
    ⑩ EFFET — Lit deux fichiers et l'horloge (le calendrier de L5).
    ⑪ TERMINAISON — Rend la main ou lève (fichier absent ou mal formé).
      [sort: non]
    """
    cle = os.path.abspath(racine)
    if cle not in _PAR_DEFAUT:
        import DATER_LES_TYPES_DE_MARCHE as D
        reg = D.lire_les_reglages(racine)
        dates, prix, _b = D.lire_l_indice(racine)
        _PAR_DEFAUT[cle] = decoupage_du_jour_meme(dict(zip(dates, prix)), reg["fenetre_de_volatilite"],
                                                  reg["centile_d_agitation"])
    return _PAR_DEFAUT[cle]


def decoupage_depuis_des_lignes(lignes, nom, jour_meme):
    """Rend un `Decoupage` à partir de lignes {date, type} — par exemple celles de `DATER_LES_TYPES_DE_MARCHE.dater`.

    ① RÔLE — Recevoir un découpage calculé ailleurs, sans le recalculer (R-708).
    ② CONTEXTE D'APPEL — L'appelant qui a les lignes du lot L5 ; l'épreuve anti-avenir du lot W2e.
    ③ ENTRÉE — `lignes` : itérable de dictionnaires portant `date` et `type` · `nom` · `jour_meme` : la déclaration
      de l'appelant (False pour le découpage d'après coup de l'étape 2).
    ④ CONDITIONS D'ENTRÉE — Types connus (sinon ValueError, par `Decoupage`).
    ⑤ SORTIE — UNE valeur : un `Decoupage`.
      [rend: 1]
    ⑥ TRAITEMENT — Copier date → type.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le découpage est un paramètre (R5-2) : celui de l'étape 2 doit pouvoir être passé, et se dire.
    ⑨ CE QUI CLOCHE — `jour_meme` est cru sur parole : passer True pour les lignes de L5 serait faux, et rien ici ne
      le voit (l'épreuve anti-avenir le voit).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    return Decoupage(nom, {l["date"]: l["type"] for l in lignes}, jour_meme)
