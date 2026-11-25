#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_MUTANTS_DU_CONTROLE_DES_TRADES_Jeu_26-11-2026.py — Jeu 26-11-2026 (Paris). EN ESSAI · épreuve COURTE.
Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. `defauts_d_un_trade` (tests/EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py) est le contrôle
qui dit, dans l'épreuve par propriétés, si un trade du soir est juste. Trois relectures de suite (D1, N-42, N-46 du
25-11-2026) y ont trouvé une branche sans témoin faux, et chaque réparation ajoutait une LISTE de cas écrits à la main.
Le superviseur R-759 du 26-11-2026 à 00h02 a jugé : « Réparation par énumération » ; poursuivre avec (a) un MUTATEUR
AUTOMATIQUE sur l'arbre syntaxique de la fonction et (b) des TÉMOINS FABRIQUÉS à partir de l'oracle
`MODULE_POSITIONS.vendre` (la vente du circuit), « pas de nouvelle liste de cas à la main ». Ce fichier fait les deux.

(b) LES TÉMOINS. Des séries FACTICES (achat à 100,00 le 2024-01-09, objectif +4 % = 104,00, stop −2,5 % = 97,50, et
d'autres prix d'achat pour l'arrondi) où UNE ou DEUX séances touchent un seuil pile, à 1e-4 € près, en ouverture, au
plus haut ou au plus bas, à la séance d'achat ou après, l'échéance h étant 1, 2, 3 ou « aucune ». Pour chaque série,
`vendre` rend LA sortie ; on fabrique alors tous les trades voisins : chaque motif sur chaque séance de la fenêtre
(donc la date ±1), au prix que ce motif donnerait, et le prix de la séance de sortie remplacé par l'objectif, le stop,
l'ouverture, la clôture, le plus haut, le plus bas. PROPRIÉTÉ : `defauts_d_un_trade` accepte un trade ⇔ ce trade est
celui que rend `vendre` (même motif, même date, même prix écrit en « %.5f »), et le drapeau « trou » qu'elle rend vaut
« la fenêtre enjambe une date du calendrier absente de la série ». Une seule exception écrite, R-112 non appliquée
(cas K07) : dans une fenêtre à trou, l'échéance n'est pas jugée, donc un HORIZON juste à une autre ligne est accepté.

(a) LE MUTATEUR. Chaque nœud MUTABLE de l'arbre de `defauts_d_un_trade` (fonctions intérieures comprises, textes des
messages exclus) donne ses mutants : opérande d'un and/or forcé à vrai puis à faux · not retiré · comparaison
inversée (sa négation) et sa borne changée (« < » ↔ « <= », « > » ↔ « >= ») · ±1 sur l'opérande de droite d'une
comparaison numérique et sur les bornes d'une tranche ou d'un indice · constante numérique changée de signe et mise à
zéro (EPS_SEUIL, EPS_PRIX…) · + ↔ − · appel rendu muet (`rendu.append` retiré) · ZONE MORTE de 1e-3 € rétablie sur UN
appel de `haut` ou `bas` à la fois, dans le sens qui laisse passer (sous un `not`, le seuil s'éloigne ; ailleurs, il
se rapproche). Chaque mutant est joué sur les témoins (b) puis sur les 26 cas I1-C* écrits à la main
(`cas_limites_des_defauts`, gardés : R-732, cas réels) ; il est TUÉ dès qu'un témoin le contredit, et le témoin est
nommé. CONTRÔLE DE COMPLÉTUDE (propriété, jamais un compte figé) : l'ensemble des nœuds réellement mutés doit être
égal à l'ensemble des nœuds mutables relevé par un SECOND parcours, indépendant (`ast.walk`). Un survivant non déclaré
dans EQUIVALENTS, ou une déclaration qui ne survit plus, rend le code 1.

USAGE : python3 -B tests/EPREUVES_DES_MUTANTS_DU_CONTROLE_DES_TRADES_Jeu_26-11-2026.py <racine> [--saboter]
  [--sans-mutants : interne à --saboter, ne joue que l'intacte et la complétude]
  <racine> : le dépôt (sa copie) ; seuls y sont lus l'épreuve par propriétés et programmes/ (MODULE_POSITIONS, COMMUN).
  --saboter : joue chaque SABOTAGE (dictionnaire SABOTAGES) sur une COPIE faite sous un dossier temporaire, et exige
  que l'épreuve y rende 1 avec le mot attendu ; ne touche jamais au dépôt.
CODE DE SORTIE : 0 tout tient · 1 un défaut (intacte contredite par l'oracle, survivant, nœud non muté, sabotage qui ne
mord pas) · 2 l'épreuve n'a pas pu tourner (R-734). Aucun cours réel lu : les séries sont fabriquées ici.
"""
import ast
import copy
import os
import shutil
import subprocess
import sys
import tempfile
import time
import types

EPREUVE = os.path.join("tests", "EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py")
CIBLE = "defauts_d_un_trade"
MOTIFS = ("SL_GAP", "TP_GAP", "SL", "TP", "HORIZON", "VENTE")
ZONE_MORTE = 1e-3          # la zone morte de 1e-3 € qu'avait main 3cee571f5 (I1p, m1), rétablie un appel à la fois
DATES = ["2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-15", "2024-01-16",
         "2024-01-17"]
TROU = "2024-01-11"        # la date du calendrier retirée de la série dans la famille « trou » (N-45)

# LES MUTANTS ÉQUIVALENTS, chacun avec sa raison (superviseur R-759 du 26-11-2026 : « mutants équivalents […] dans une
# liste écrite avec leur raison »). Clé : la description EXACTE que rend `mutants` (son lieu, sans numéro de ligne).
# Une clé qui ne survit plus fait rougir : la liste ne garde que de vrais équivalents.
EQUIVALENTS = {
    '[dans haut] Compare borne/0 : p >= obj - EPS_SEUIL':
        "« >= » devenu « > » dans `haut` : ne diffère qu'au prix EXACT objectif − 5e-6 €, un flottant qu'aucun prix écrit (quatre décimales au plus dans les cours, cinq au journal) n'atteint en face d'un objectif à cinq décimales au plus ; même nature que le sabotage D de Cowork (côté stop) et K8 (N-43 : l'égalité à la coupure est le ⑨ ② de la fonction)",
    '[dans egal] Compare borne/0 : abs(p - q) <= EPS_PRIX':
        "« <= » devenu « < » dans `egal` : ne diffère qu'à un écart EXACT de 1e-5 € entre deux prix écrits en « %.5f », qui ne sont alors pas le même prix ; K8 de Cowork (d1177fde, « quasi équivalente »)",
    "[si bas(b['open']) or bas(b['low']) or haut(b['op] BoolOp operande/0/False : bas(b['open']) or bas(b['low']) or haut(b['open']) or haut(b['high'])":
        "boucle ② sans « bas(ouverture) » : une ouverture au stop ou dessous a un plus bas au stop ou dessous (plus bas <= ouverture, toute séance réelle ou fabriquée) : l'opérande « plus bas » qui reste dit déjà la même chose",
    "[si bas(b['open']) or bas(b['low']) or haut(b['op] BoolOp operande/2/False : bas(b['open']) or bas(b['low']) or haut(b['open']) or haut(b['high'])":
        "boucle ② sans « haut(ouverture) » : une ouverture à l'objectif ou dessus a un plus haut à l'objectif ou dessus (ouverture <= plus haut) : l'opérande « plus haut » qui reste dit déjà la même chose",
    "[si motif == 'SL'] BoolOp operande/0/False : 'saut' in SANS_CONTROLE or not haut(b['open'])":
        "« 'saut' in SANS_CONTROLE » forcé à faux : il vaut déjà faux hors du sabotage S-I1a, seul à poser ce drapeau (S-I1a, joué par ProprietesSuiteSabot, le garde)",
    "[si motif == 'TP'] BoolOp operande/0/True : not bas(b['open']) and (not haut(b['open'])) and (not bas(b['low'])) a":
        "TP sans « not bas(ouverture) » : la branche exige aussi « not bas(plus bas) », et une ouverture au stop ou dessous a un plus bas au stop ou dessous (plus bas <= ouverture, toute séance réelle ou fabriquée) : l'opérande « plus bas » qui reste dit déjà la même chose",
    "[si motif == 'TP'] Call zone_morte/True : bas(b['open'])":
        "zone morte sur « not bas(ouverture) » du TP : même raison que l'opérande retiré, « not bas(plus bas) » décide seul",
    "[si motif == 'HORIZON'] BoolOp operande/0/True : not bas(b['open']) and (not bas(b['low'])) and (not haut(b['open'])) a":
        "HORIZON sans « not bas(ouverture) » : « not bas(plus bas) » reste, et une ouverture au stop ou dessous a un plus bas au stop ou dessous (plus bas <= ouverture, toute séance réelle ou fabriquée) : l'opérande « plus bas » qui reste dit déjà la même chose",
    "[si motif == 'HORIZON'] BoolOp operande/2/True : not bas(b['open']) and (not bas(b['low'])) and (not haut(b['open'])) a":
        "HORIZON sans « not haut(ouverture) » : « not haut(plus haut) » reste, et une ouverture à l'objectif ou dessus a un plus haut à l'objectif ou dessus (ouverture <= plus haut) : l'opérande « plus haut » qui reste dit déjà la même chose",
    "[si motif == 'HORIZON'] Call zone_morte/True : bas(b['open'])":
        'zone morte sur « not bas(ouverture) » du HORIZON : « not bas(plus bas) » décide seul (plus bas <= ouverture)',
    "[si motif == 'HORIZON'] Call zone_morte/True : haut(b['open'])":
        'zone morte sur « not haut(ouverture) » du HORIZON : « not haut(plus haut) » décide seul (ouverture <= plus haut)',
    "[si motif in ('SL_GAP', 'TP_GAP', 'SL', 'TP') and] BoolOp operande/2/True : motif in ('SL_GAP', 'TP_GAP', 'SL', 'TP') and isinstance(h, int) and (":
        "« not isinstance(h, bool) » forcé à vrai : seul un horizon booléen le rend faux, et `vendre` refuse un horizon booléen (ValueError) : aucun trade du circuit n'en porte ; K14 de Cowork (« sans portée »)",
    "[si motif in ('SL_GAP', 'TP_GAP', 'SL', 'TP') and] BoolOp operande/4/True : motif in ('SL_GAP', 'TP_GAP', 'SL', 'TP') and isinstance(h, int) and (":
        "« 'echeance' not in SANS_CONTROLE » forcé à vrai : il vaut déjà vrai hors du sabotage S-I1b, seul à poser ce drapeau (S-I1b le garde)",
}


def lire_la_cible(racine):
    """Rend (texte de l'épreuve, arbre du module, nœud FunctionDef de la cible).
    ① RÔLE — trouver `defauts_d_un_trade` dans l'épreuve par propriétés. ② CONTEXTE D'APPEL — `principal`.
    ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — l'épreuve existe et se lit. ⑤ SORTIE — TROIS valeurs. [rend: 3]
    ⑥ TRAITEMENT — `ast.parse`, puis la définition de premier niveau nommée CIBLE. ⑦ UNITÉ — —. ⑧ POURQUOI — muter
    l'arbre, jamais le texte : un remplacement de texte dépend de l'écriture exacte (R-756). ⑨ CE QUI CLOCHE — une
    cible absente lève ValueError (code 2 par `principal`). ⑩ EFFET — lit un fichier. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    texte = open(os.path.join(racine, EPREUVE), encoding="utf-8").read()
    arbre = ast.parse(texte)
    for n in arbre.body:
        if isinstance(n, ast.FunctionDef) and n.name == CIBLE:
            return texte, arbre, n
    raise ValueError("%s absente de %s" % (CIBLE, EPREUVE))


def hors_calcul(fn):
    """Rend l'ensemble des id() des nœuds qui ne sont pas du calcul : docstrings et textes des messages.
    ① RÔLE — exclure le texte. ② CONTEXTE D'APPEL — `sites_par_recursion`, `noeuds_mutables`. ③ ENTRÉE — la fonction.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : un ensemble. [rend: 1] ⑥ TRAITEMENT — les docstrings (première
    instruction chaîne de chaque def) et toute opération « chaîne % … » avec ses enfants. ⑦ UNITÉ — —. ⑧ POURQUOI —
    muter un message ne change aucun verdict. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    exclus = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.FunctionDef) and n.body and isinstance(n.body[0], ast.Expr) and \
                isinstance(n.body[0].value, ast.Constant) and isinstance(n.body[0].value.value, str):
            exclus |= set(map(id, ast.walk(n.body[0])))
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod) and isinstance(n.left, ast.Constant) and \
                isinstance(n.left.value, str):
            exclus |= set(map(id, ast.walk(n)))
        if isinstance(n, ast.JoinedStr):
            exclus |= set(map(id, ast.walk(n)))
    return exclus


NEGATION = {ast.Lt: ast.GtE, ast.LtE: ast.Gt, ast.Gt: ast.LtE, ast.GtE: ast.Lt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
            ast.In: ast.NotIn, ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}
BORNE = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt}
NUMERIQUES = (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq)


def genres(n, parent, exclus):
    """Rend la liste des genres de mutation que porte le nœud n (vide s'il n'est pas mutable).
    ① RÔLE — LA définition d'un nœud mutable, écrite une fois (R-708) et lue par les deux parcours. ② CONTEXTE D'APPEL
    — `sites_par_recursion`, `noeuds_mutables`. ③ ENTRÉE — le nœud, son parent, les exclus. ④ CONDITIONS D'ENTRÉE —
    —. ⑤ SORTIE — UNE valeur : liste de tuples. [rend: 1] ⑥ TRAITEMENT — voir le sens en tête, (a). ⑦ UNITÉ — —.
    ⑧ POURQUOI — la liste des opérateurs vient du superviseur R-759 du 26-11-2026 ; « appel muet » vient de ce qu'un
    `rendu.append` retiré est exactement un défaut qu'on ne dit plus. ⑨ CE QUI CLOCHE — ne mute ni les noms de
    variables, ni l'ordre des instructions, ni les clés de dictionnaire (« open » pour « high ») : un mutant de cette
    sorte n'est pas produit (consigné, BACKLOG à ouvrir). ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    if id(n) in exclus:
        return []
    g = []
    if isinstance(n, ast.BoolOp):
        g += [("operande", i, v) for i in range(len(n.values)) for v in (True, False)]
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
        g.append(("not",))
    if isinstance(n, ast.Compare):
        for i, op in enumerate(n.ops):
            if type(op) in NEGATION:
                g.append(("negation", i))
            if type(op) in BORNE:
                g.append(("borne", i))
            droite = n.comparators[i]
            if type(op) in NUMERIQUES and not (isinstance(droite, ast.Constant) and not
                                               isinstance(droite.value, (int, float))) \
                    and not isinstance(droite, (ast.Tuple, ast.List)):
                g += [("plus_un", i, +1), ("plus_un", i, -1)]
    if isinstance(n, ast.Slice):
        for champ in ("lower", "upper"):
            if getattr(n, champ) is not None:
                g += [("tranche", champ, +1), ("tranche", champ, -1)]
    if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Name):
        g += [("indice", +1), ("indice", -1)]
    if isinstance(n, ast.Constant) and type(n.value) in (int, float):
        g += [("constante", "signe"), ("constante", "zero")]
    if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub)):
        g.append(("plus_moins",))
    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute) and \
            n.value.func.attr == "append":
        g.append(("muet",))
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("haut", "bas"):
        sous_not = isinstance(parent, ast.UnaryOp) and isinstance(parent.op, ast.Not)
        g.append(("zone_morte", sous_not))
    return g


def cle(n, debut):
    """La clé d'un nœud : (genre de nœud, ligne depuis le « def », colonne, colonne de fin). [rend: 1]
    ① RÔLE — identifier un nœud dans deux parcours et dans une copie. ② CONTEXTE D'APPEL — les deux parcours,
    `appliquer`. ③ ENTRÉE — nœud, ligne du def. ④ CONDITIONS D'ENTRÉE — le nœud porte ses positions. ⑤ SORTIE — UN
    tuple. ⑥ TRAITEMENT — positions de l'analyseur. ⑦ UNITÉ — lignes, colonnes. ⑧ POURQUOI — `deepcopy` garde les
    positions : la même clé retrouve le nœud dans la copie. ⑨ CE QUI CLOCHE — deux nœuds de même genre aux mêmes
    positions n'existent pas en Python. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    return (type(n).__name__, n.lineno - debut, n.col_offset, n.end_lineno - debut, n.end_col_offset)


def sites_par_recursion(fn):
    """Rend la liste (clé, genre) des sites de mutation, par un parcours RÉCURSIF à la main.
    ① RÔLE — le parcours du mutateur. ② CONTEXTE D'APPEL — `mutants`. ③ ENTRÉE — la fonction. ④ CONDITIONS
    D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : liste. [rend: 1] ⑥ TRAITEMENT — descend champ par champ (`ast.iter_fields`)
    en portant le parent. ⑦ UNITÉ — —. ⑧ POURQUOI — un parcours DIFFÉRENT de celui du contrôle (`ast.walk`) : s'il
    oublie une branche, le contrôle de complétude le voit (sabotage S-M3). ⑨ CE QUI CLOCHE — un nœud sans position
    (Slice d'avant Python 3.9) n'aurait pas de clé ; Python 3.9+ est exigé par le dépôt. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main ; la récursion suit la profondeur de l'arbre, finie. [sort: non]"""
    exclus = hors_calcul(fn)
    sortie = []

    def descendre(n, parent):
        for g in genres(n, parent, exclus):
            sortie.append((cle(n, fn.lineno), g))
        for _champ, valeur in ast.iter_fields(n):
            enfants = valeur if isinstance(valeur, list) else [valeur]
            for e in enfants:
                if isinstance(e, ast.AST):
                    descendre(e, n)
    descendre(fn, None)
    return sortie


def noeuds_mutables(fn):
    """Rend l'ensemble des clés des nœuds mutables, par `ast.walk` — le parcours du CONTRÔLE.
    ① RÔLE — l'étalon de la complétude. ② CONTEXTE D'APPEL — `principal`. ③ ENTRÉE — la fonction. ④ CONDITIONS
    D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : ensemble de clés. [rend: 1] ⑥ TRAITEMENT — table des parents, puis `genres`.
    ⑦ UNITÉ — —. ⑧ POURQUOI — « nœuds mutés = nœuds mutables de l'arbre » (superviseur R-759, 26-11-2026), une
    propriété : renommer ou ajouter une branche ne change pas l'avis du contrôle. ⑨ CE QUI CLOCHE — partage `genres`
    avec le mutateur : une erreur DANS `genres` n'est pas vue ici (elle l'est par les survivants). ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    exclus = hors_calcul(fn)
    parents = {}
    for p in ast.walk(fn):
        for c in ast.iter_child_nodes(p):
            parents[id(c)] = p
    return {cle(n, fn.lineno) for n in ast.walk(fn) if genres(n, parents.get(id(n)), exclus)}


def appliquer(fn, k, g):
    """Rend une COPIE de fn où le nœud de clé k a reçu la mutation g, et sa description.
    ① RÔLE — fabriquer un mutant. ② CONTEXTE D'APPEL — `mutants`. ③ ENTRÉE — la fonction, la clé, le genre.
    ④ CONDITIONS D'ENTRÉE — k est une clé de fn. ⑤ SORTIE — DEUX valeurs : la fonction mutée, le texte. [rend: 2]
    ⑥ TRAITEMENT — `deepcopy`, nœud retrouvé par sa clé, puis remplacement dans son parent. ⑦ UNITÉ — —.
    ⑧ POURQUOI — l'original n'est jamais touché. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main ; lève LookupError si la clé manque. [sort: non]"""
    f = copy.deepcopy(fn)
    parents = {}
    cible = None
    for p in ast.walk(f):
        for c in ast.iter_child_nodes(p):
            parents[id(c)] = p
        if cible is None and hasattr(p, "lineno") and cle(p, fn.lineno) == k:
            cible = p
    if cible is None:
        raise LookupError(k)
    avant = ast.unparse(cible)[:70]
    # LE NOM DU MUTANT NE PORTE AUCUN NUMÉRO DE LIGNE : le lieu se dit par la branche qui l'entoure — le test du « if »
    # ou de l'« elif » le plus proche, sinon l'itérable de la boucle, sinon la fonction intérieure — relevé AVANT la
    # mutation. Raison : une docstring allongée décale les lignes, et la liste EQUIVALENTS changerait d'avis (« si je
    # renomme, mon contrôle change-t-il d'avis ? », section 7 des instructions).
    lieu, x = "", cible
    while id(x) in parents and not lieu:
        x = parents[id(x)]
        if isinstance(x, ast.If):
            lieu = "si " + ast.unparse(x.test)[:45]
        elif isinstance(x, ast.For):
            lieu = "boucle sur " + ast.unparse(x.iter)
        elif isinstance(x, ast.FunctionDef):
            lieu = "dans " + x.name if x.name != CIBLE else ""
            break
    nouveau = None
    if g[0] == "operande":
        cible.values[g[1]] = ast.Constant(g[2])
    elif g[0] == "not":
        nouveau = cible.operand
    elif g[0] == "negation":
        cible.ops[g[1]] = NEGATION[type(cible.ops[g[1]])]()
    elif g[0] == "borne":
        cible.ops[g[1]] = BORNE[type(cible.ops[g[1]])]()
    elif g[0] == "plus_un":
        cible.comparators[g[1]] = ast.BinOp(cible.comparators[g[1]], ast.Add(), ast.Constant(g[2]))
    elif g[0] == "tranche":
        setattr(cible, g[1], ast.BinOp(getattr(cible, g[1]), ast.Add(), ast.Constant(g[2])))
    elif g[0] == "indice":
        cible.slice = ast.BinOp(cible.slice, ast.Add(), ast.Constant(g[1]))
    elif g[0] == "constante":
        cible.value = -cible.value if g[1] == "signe" else type(cible.value)(0)
    elif g[0] == "plus_moins":
        cible.op = ast.Sub() if isinstance(cible.op, ast.Add) else ast.Add()
    elif g[0] == "muet":
        nouveau = ast.Pass()
    elif g[0] == "zone_morte":
        # sous un `not` : le seuil s'éloigne (« pas touché » plus facile) ; ailleurs il se rapproche (« touché »)
        seuil = "obj" if cible.func.id == "haut" else "stp"
        vers = (+1 if seuil == "obj" else -1) * (1 if g[1] else -1)
        op = ast.GtE() if seuil == "obj" else ast.LtE()
        nouveau = ast.Compare(cible.args[0], [op], [ast.BinOp(ast.Name(seuil, ast.Load()), ast.Add(),
                                                              ast.Constant(vers * ZONE_MORTE))])
    if nouveau is not None:
        p = parents[id(cible)]
        for champ, valeur in ast.iter_fields(p):
            if valeur is cible:
                setattr(p, champ, nouveau)
            elif isinstance(valeur, list):
                for i, x in enumerate(valeur):
                    if x is cible:
                        valeur[i] = nouveau
    ast.fix_missing_locations(f)
    texte = "[%s] %s %s : %s" % (lieu or "corps", k[0], "/".join(str(x) for x in g), avant)
    return f, texte


def mutants(fn):
    """Rend la liste (clé, description, fonction mutée) de tous les mutants. [rend: 1]
    ① RÔLE — le mutateur. ② CONTEXTE D'APPEL — `principal`. ③ ENTRÉE — la fonction. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : liste. ⑥ TRAITEMENT — `sites_par_recursion` puis `appliquer` ; un mutant dont le texte est
    celui de l'original est omis. ⑦ UNITÉ — —. ⑧ POURQUOI — voir le sens en tête. ⑨ CE QUI CLOCHE — —. ⑩ EFFET —
    aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    ref = ast.unparse(fn)
    sortie = []
    vus = {}
    for k, g in sites_par_recursion(fn):
        f, texte = appliquer(fn, k, g)
        if ast.unparse(f) != ref:
            vus[texte] = vus.get(texte, 0) + 1
            if vus[texte] > 1:                      # deux sites au même lieu et au même texte : numérotés
                texte += " #%d" % vus[texte]
            sortie.append((k, texte, f))
    return sortie


def charger(racine, texte):
    """Rend le module de l'épreuve par propriétés exécuté depuis son texte, et MODULE_POSITIONS de la racine.
    ① RÔLE — préparer l'oracle et les cas. ② CONTEXTE D'APPEL — `principal`. ③ ENTRÉE — racine, texte.
    ④ CONDITIONS D'ENTRÉE — programmes/ porte MODULE_POSITIONS et COMMUN. ⑤ SORTIE — DEUX valeurs. [rend: 2]
    ⑥ TRAITEMENT — sys.argv vidé le temps de l'exécution (SANS_CONTROLE le lit) ; programmes/ de la racine mis en
    tête du chemin d'import. ⑦ UNITÉ — —. ⑧ POURQUOI — sous --saboter, la copie sabotée doit être celle chargée.
    ⑨ CE QUI CLOCHE — un MODULE_POSITIONS déjà importé dans ce processus serait réutilisé : `principal` tourne dans un
    processus neuf à chaque lancement. ⑩ EFFET — modifie sys.path. ⑪ TERMINAISON — rend la main. [sort: non]"""
    m = types.ModuleType("EPREUVE_PAR_PROPRIETES")
    m.__file__ = os.path.join(racine, EPREUVE)
    argv = sys.argv
    sys.argv = [m.__file__]
    try:
        exec(compile(texte, m.__file__, "exec"), m.__dict__)
    finally:
        sys.argv = argv
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import MODULE_POSITIONS
    import COMMUN
    return m, MODULE_POSITIONS, COMMUN


def seance(d, o, h, l, c=None):
    """Une séance factice (dict). ① RÔLE — fabriquer. ② CONTEXTE D'APPEL — `familles`. ③ ENTRÉE — date, prix.
    ④ CONDITIONS D'ENTRÉE — l <= o <= h. ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT — clôture au milieu si absente,
    à quatre décimales. ⑦ UNITÉ — euros. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend
    la main. [sort: non]"""
    return dict(date=d, open=o, high=h, low=l, close=round((h + l) / 2, 4) if c is None else c)


def formes(obj, stp, achat):
    """Les séances « spéciales » : ouverture, plus haut, plus bas autour des deux seuils. [rend: 1]
    ① RÔLE — la grille des témoins. ② CONTEXTE D'APPEL — `familles`. ③ ENTRÉE — seuils, vrai pour la séance d'achat
    (son ouverture est le prix d'achat). ④ CONDITIONS D'ENTRÉE — stp < 100 < obj. ⑤ SORTIE — UNE valeur : liste de
    (o, h, l). ⑥ TRAITEMENT — ouvertures {stop −1, −1e-4, pile, +1e-4, 100, objectif −1e-4, pile, +1e-4, +1} ; plus
    haut parmi {ouverture, objectif −1e-4, pile, +1e-4, +1} au-dessus de l'ouverture ; plus bas de même sous elle.
    ⑦ UNITÉ — euros. ⑧ POURQUOI — « seuils touchés pile, à 1e-4, en ouverture, plus haut, plus bas » (superviseur).
    ⑨ CE QUI CLOCHE — pas de prix à 8e-6 du seuil ici : I1-C24 le garde. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la
    main. [sort: non]"""
    ouv = [100.0] if achat else [stp - 1, stp - 1e-4, stp, stp + 1e-4, 100.0, obj - 1e-4, obj, obj + 1e-4, obj + 1]
    hauts = [obj - 1e-4, obj, obj + 1e-4, obj + 1]
    bas_ = [stp + 1e-4, stp, stp - 1e-4, stp - 1]
    sortie = []
    for o in ouv:
        for h in sorted({o, 101.0 if o < 101 else o} | {x for x in hauts if x >= o}):
            for l in sorted({o, 99.0 if o > 99 else o} | {x for x in bas_ if x <= o}):
                sortie.append((round(o, 6), round(h, 6), round(l, 6)))
    return sortie


def familles():
    """Rend la liste des témoins de séries : (nom, série, rang d'achat, calendrier, pe-tp-sl). [rend: 1]
    ① RÔLE — les séries FACTICES de (b). ② CONTEXTE D'APPEL — `temoins`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur. ⑥ TRAITEMENT — SIMPLE : une séance spéciale au rang k (0 = séance d'achat) dans une série
    calme ; DOUBLE : la même aux rangs k et k+1 (boucle ② : une séance AVANT la sortie touche déjà, N-42 K1, N-46 C-15) ;
    TROU : série calme ou à une séance spéciale, avec une date du calendrier absente (N-45) ; ARRONDI : prix d'achat à
    quatre décimales dont un seuil tombe sur une demi-unité de la cinquième, séance au seuil ARRONDI par le circuit
    (N-43). Une séance calme précède l'achat (pour la date −1). ⑦ UNITÉ — euros ; séances. ⑧ POURQUOI — voir le sens en
    tête. ⑨ CE QUI CLOCHE — séries de huit séances au plus : un défaut qui ne se voit qu'au-delà n'est pas fabriqué.
    ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    calme = lambda d: seance(d, 100.0, 101.0, 99.0, 100.5)  # noqa: E731
    sortie = []
    obj, stp = 104.0, 97.5
    for k in range(0, 5):
        for o, h, l in formes(obj, stp, k == 0):
            s = [calme(d) for d in DATES]
            s[1 + k] = seance(DATES[1 + k], o, h, l)
            sortie.append(("SIMPLE k=%d o=%s h=%s l=%s" % (k, o, h, l), s, 1, list(DATES), (100.0, 0.04, 0.025)))
            if k < 4:
                s2 = [dict(x) for x in s]
                s2[2 + k] = seance(DATES[2 + k], o, h, l)
                if k == 0:
                    s2[2] = seance(DATES[2], 100.0, h, l)
                sortie.append(("DOUBLE k=%d,%d o=%s h=%s l=%s" % (k, k + 1, o, h, l), s2, 1, list(DATES),
                               (100.0, 0.04, 0.025)))
    for k in (None, 1, 3):
        s = [calme(d) for d in DATES]
        if k is not None:
            s[1 + k] = seance(DATES[1 + k], 100.0, obj, 99.0)
        s = [x for x in s if x["date"] != TROU]
        sortie.append(("TROU %s k=%s" % (TROU, k), s, 1, list(DATES), (100.0, 0.04, 0.025)))
    # ARRONDI (N-43) : pe = k/1e4 avec k ≡ 2 (mod 4) met le stop −2,5 % sur une demi-unité de la cinquième décimale
    for pe in (100.0002, 100.0006, 25.6002, 145.0010, 33.3338):
        for tp, sl in ((0.04, 0.025), (0.03, 0.015), (0.05, 0.035)):
            o_, s_ = float("%.5f" % (pe * (1 + tp))), float("%.5f" % (pe * (1 - sl)))
            for quoi in ("haut", "bas"):
                s = [seance(d, pe, pe * 1.001, pe * 0.999, pe) for d in DATES]
                if quoi == "haut":
                    s[2] = seance(DATES[2], pe, o_, pe * 0.999)
                else:
                    s[2] = seance(DATES[2], pe, pe * 1.001, s_)
                sortie.append(("ARRONDI pe=%s tp=%s sl=%s %s au seuil arrondi" % (pe, tp, sl, quoi), s, 1,
                               list(DATES), (pe, tp, sl)))
    return sortie


def temoins(MP, COMMUN):
    """Rend la liste des témoins (nom, trade, série, tp, sl, h, calendrier, verdict attendu, trou attendu). [rend: 1]
    ① RÔLE — (b) : les trades fabriqués autour de la sortie de l'oracle. ② CONTEXTE D'APPEL — `principal`.
    ③ ENTRÉE — MODULE_POSITIONS (l'oracle `vendre`), COMMUN (HORIZON_AUCUNE). ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur. ⑥ TRAITEMENT — pour chaque série de `familles` et chaque échéance 1, 2, 3, aucune : la vente
    de `vendre` (mode « vendre ») ; une vente FIN_DES_DONNEES (aucun seuil sans échéance) n'est pas un trade, sautée ;
    puis chaque motif sur chaque séance de l'achat −1 à l'achat + h + 1 au prix naturel du motif ; le prix de la séance
    de sortie remplacé par six prix ; le prix d'entrée décalé d'un centime. Verdict attendu : accepté ⇔ (motif, date,
    « %.5f » du prix, prix d'entrée) == la vente — sauf R-112 (fenêtre à trou, HORIZON à la clôture d'une séance qui ne
    touche rien : accepté, cas K07). Trou attendu : les rangs du calendrier et de la série diffèrent. ⑦ UNITÉ — euros ;
    séances. ⑧ POURQUOI — l'oracle est le circuit lui-même : la propriété « accepte ⇔ identique à vendre » ne recopie
    aucune règle (R-708). ⑨ CE QUI CLOCHE — si `vendre` est faux, la propriété l'est aussi, mais elle le DIT : la
    fonction intacte, qui ne l'appelle pas, la contredit (sabotage S-M4). ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la
    main. [sort: non]"""
    sortie = []
    for nom, s, a, cal, (pe, tp, sl) in familles():
        dd = [b["date"] for b in s]
        for h in (1, 2, 3, COMMUN.HORIZON_AUCUNE):
            v = MP.vendre(s, a, {"tp": tp, "sl": sl, "horizon": h}, "vendre")
            if v is None or v["motif"] not in MOTIFS:
                continue
            ref = (v["motif"], v["date_sortie"], "%.5f" % v["px"], "%.5f" % pe)
            hn = h if isinstance(h, int) else "aucune"
            fin = len(s) - 1 if not isinstance(h, int) else min(len(s) - 1, a + h + 1)
            essais = []
            for z in range(a - 1, fin + 1):
                b = s[z]
                prix = {"SL_GAP": b["open"], "TP_GAP": b["open"], "SL": v["stop"], "TP": v["objectif"],
                        "HORIZON": b["close"], "VENTE": b["close"]}
                essais += [(m, z, prix[m], pe) for m in MOTIFS]
            zv = dd.index(v["date_sortie"])
            b = s[zv]
            essais += [(v["motif"], zv, p, pe) for p in (v["objectif"], v["stop"], b["open"], b["close"], b["high"],
                                                         b["low"])]
            essais.append((v["motif"], zv, v["px"], round(pe + 0.01, 4)))
            vus = set()
            for m, z, p, pe_t in essais:
                t = {"prix_entree": "%.5f" % pe_t, "prix_sortie": "%.5f" % p, "motif_sortie": m,
                     "date_entree": dd[a], "date_sortie": dd[z]}
                if tuple(sorted(t.items())) in vus:
                    continue
                vus.add(tuple(sorted(t.items())))
                attendu = (m, dd[z], t["prix_sortie"], t["prix_entree"]) == ref
                trou = cal.index(dd[z]) - cal.index(dd[a]) != z - a if z >= a else \
                    cal.index(dd[a]) - cal.index(dd[z]) != a - z
                if trou and m == "HORIZON" and v["motif"] == "HORIZON" and z > a and \
                        t["prix_sortie"] == "%.5f" % s[z]["close"] and t["prix_entree"] == ref[3] and \
                        all(x["low"] > v["stop"] and x["high"] < v["objectif"] and v["stop"] < x["open"] <
                            v["objectif"] for x in s[a:z + 1]):
                    attendu = True      # R-112 non appliquée (K07) : l'échéance d'une fenêtre à trou n'est pas jugée
                if not isinstance(h, int) and m == "HORIZON" and z >= a and \
                        t["prix_sortie"] == "%.5f" % s[z]["close"] and t["prix_entree"] == ref[3] and \
                        all(x["low"] > v["stop"] and x["high"] < v["objectif"] and v["stop"] < x["open"] <
                            v["objectif"] for x in s[a:z + 1]):
                    attendu = True      # N-48 consigné : sans échéance, un HORIZON n'est pas refusé (vendre n'en rend pas)
                sortie.append(("%s h=%s → vendre %s %s %s ; essai %s %s %s pe %s" % (
                    nom, hn, v["motif"], v["date_sortie"], ref[2], m, dd[z], t["prix_sortie"], t["prix_entree"]),
                    t, s, tp, sl, h, cal, attendu, trou if z >= a else None))
            # UNE DATE HORS DE LA SÉRIE (entrée, puis sortie) : refusée, jamais une exception
            for cle_d in ("date_entree", "date_sortie"):
                t = {"prix_entree": ref[3], "prix_sortie": ref[2], "motif_sortie": ref[0], "date_entree": dd[a],
                     "date_sortie": ref[1], cle_d: "2024-02-30"}
                sortie.append(("%s h=%s ; %s hors de la série" % (nom, hn, cle_d), t, s, tp, sl, h, cal, False, None))
    return sortie


def juger(fonction, tem, cas_i1):
    """Rend le nom du premier témoin qui contredit la fonction (None si aucun), et le nombre joué. [rend: 2]
    ① RÔLE — tuer un mutant, ou éprouver l'intacte. ② CONTEXTE D'APPEL — `principal`. ③ ENTRÉE — la fonction, les
    témoins, une fonction qui joue les cas I1-C* avec elle. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs.
    ⑥ TRAITEMENT — un témoin contredit si le verdict diffère, ou si le drapeau trou diffère (quand il est défini), ou si
    la fonction lève ; puis les cas I1-C*. ⑦ UNITÉ — —. ⑧ POURQUOI — s'arrêter au premier témoin qui tue : les tués
    coûtent peu, seuls les survivants parcourent tout. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la
    main ; un mutant qui bouclerait sans fin n'est pas possible ici (aucune boucle while, boucles sur des listes finies
    — les mutations ±1 ne font que décaler des bornes). [sort: non]"""
    for i, (nom, t, s, tp, sl, h, cal, attendu, trou) in enumerate(tem):
        try:
            rendu, tr = fonction(t, s, tp, sl, h, cal)
        except Exception as e:  # noqa: BLE001 — un mutant qui lève est tué par ce témoin
            return "%s (lève %s)" % (nom, type(e).__name__), i + 1
        if (not rendu) != attendu:
            return "%s : %s attendu, %s" % (nom, "ACCEPTÉ" if attendu else "REFUSÉ",
                                            "refusé (%s)" % rendu[0][:90] if rendu else "accepté"), i + 1
        if trou is not None and tr != trou:
            return "%s : trou %s attendu, %s rendu" % (nom, trou, tr), i + 1
    try:
        ecarts, n = cas_i1(fonction)
    except Exception as e:  # noqa: BLE001
        return "cas I1-C* (lève %s)" % type(e).__name__, len(tem)
    if ecarts:
        return ecarts[0][:160], len(tem) + n
    return None, len(tem) + n


def principal(racine):
    """L'épreuve. ① RÔLE — (a) et (b). ② CONTEXTE D'APPEL — `__main__`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE —
    celles de `charger`. ⑤ SORTIE — UNE valeur : le code 0 ou 1. [rend: 1] ⑥ TRAITEMENT — ① charger ; ② témoins ;
    ③ l'INTACTE doit concorder avec l'oracle sur tous les témoins et les cas I1-C* ; ④ complétude des nœuds ; ⑤ chaque
    mutant joué, survivants confrontés à EQUIVALENTS. ⑦ UNITÉ — secondes affichées. ⑧ POURQUOI — voir le sens en tête.
    ⑨ CE QUI CLOCHE — les mutants sont exécutés dans les globales du module chargé (mêmes SANS_CONTROLE). ⑩ EFFET —
    affiche. ⑪ TERMINAISON — rend la main. [sort: non]"""
    t0 = time.time()
    texte, arbre, fn = lire_la_cible(racine)
    M, MP, COMMUN = charger(racine, texte)
    tem = temoins(MP, COMMUN)
    print("(b) témoins fabriqués depuis MODULE_POSITIONS.vendre : %d trade(s) (%d accepté(s) attendu(s)), "
          "%d série(s) factice(s)" % (len(tem), sum(1 for x in tem if x[7]), len(familles())))
    cas_code = M.cas_limites_des_defauts.__code__

    def cas_i1(fonction):
        g = dict(M.__dict__)
        g[CIBLE] = fonction
        return types.FunctionType(cas_code, g)()

    def compiler(f):
        g = dict(M.__dict__)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[f], type_ignores=[])), M.__file__, "exec"), g)
        return g[CIBLE]
    rouge = False
    tue, n = juger(compiler(fn), tem, cas_i1)
    if tue:
        print("❌ INTACTE CONTREDITE : %s" % tue)
        rouge = True
    else:
        print("✅ intacte : concorde avec vendre sur les %d témoins et les cas I1-C*" % (n,))
    ms = mutants(fn)
    mutes = {k for k, _t, _f in ms}
    attendus = noeuds_mutables(fn)
    if mutes != attendus:
        print("❌ COMPLÉTUDE : nœuds mutables non mutés %s ; mutés hors liste %s" % (
            sorted(attendus - mutes)[:6], sorted(mutes - attendus)[:6]))
        rouge = True
    else:
        print("✅ complétude : %d nœud(s) muté(s) = %d nœud(s) mutable(s) de l'arbre (second parcours, ast.walk)" % (
            len(mutes), len(attendus)))
    tues, equiv, survivants = 0, [], []
    if "--sans-mutants" in sys.argv:        # sous --saboter seulement (S-M1, S-M3, S-M4) : l'intacte et la complétude
        print("mutants non joués (--sans-mutants)")
        print("VERDICT : %s" % ("NON CONFORME" if rouge else "TOUT TIENT"))
        return 1 if rouge else 0
    for _k, desc, f in ms:
        try:
            tue, _n = juger(compiler(f), tem, cas_i1)
        except Exception as e:  # noqa: BLE001 — un mutant qui ne compile pas est un défaut du mutateur
            tue = "ne compile pas : %s" % e
        if tue:
            tues += 1
            print("  TUÉ l.%d %s ← %s" % (_k[1] + fn.lineno, desc, tue[:200]))
        elif desc in EQUIVALENTS:
            equiv.append(desc)
            print("  ÉQUIVALENT %s — %s" % (desc, EQUIVALENTS[desc]))
        else:
            survivants.append(desc)
            print("❌ SURVIVANT %s (l.%d)" % (desc, _k[1] + fn.lineno))
    perimees = sorted(set(EQUIVALENTS) - set(equiv))
    for d in perimees:
        print("❌ DÉCLARÉ ÉQUIVALENT MAIS NON SURVIVANT (ou absent) : %s" % d)
    rouge |= bool(survivants) or bool(perimees)
    print("BILAN : %d mutant(s) — %d tué(s), %d équivalent(s) déclaré(s), %d survivant(s)" % (
        len(ms), tues, len(equiv), len(survivants)))
    print("DURÉE : %.0f s" % (time.time() - t0))
    print("VERDICT : %s" % ("NON CONFORME" if rouge else "TOUT TIENT"))
    return 1 if rouge else 0


# LES SABOTAGES DE VÉRIFICATION (consigne du pilote V8, 26-11-2026, d'après le superviseur R-759) : chacun est joué sur
# une COPIE ; (fichier relatif, texte avant, texte après, mot attendu dans la sortie). Le code attendu est 1.
SABOTAGES = {
    # S-M1 : chaque mutation de Cowork (N-42 K1 K2 K4 K12, N-46 C-11 à C-15) dans le VRAI fichier → l'intacte rougit
    "S-M1a K1 boucle ② sans la séance d'achat": (EPREUVE, "    for b in serie[a:z]:\n", "    for b in serie[a + 1:z]:\n",
                                                 "INTACTE CONTREDITE"),
    "S-M1b K2 HORIZON au-delà de l'échéance": (EPREUVE, "or z - a == h)", "or z - a >= h)", "INTACTE CONTREDITE"),
    "S-M1c K4 échéance sans SL_GAP/TP_GAP/SL": (EPREUVE, 'if motif in ("SL_GAP", "TP_GAP", "SL", "TP") and',
                                                'if motif in ("TP",) and', "INTACTE CONTREDITE"),
    "S-M1d K12 TP_GAP par le plus haut": (EPREUVE, 'ok = haut(b["open"]) and egal(px, b["open"])',
                                          'ok = haut(b["high"]) and egal(px, b["open"])', "INTACTE CONTREDITE"),
    "S-M1e C-11 zone morte dans TP_GAP seul": (EPREUVE, 'ok = haut(b["open"]) and egal(px, b["open"])',
                                               'ok = b["open"] >= obj - 1e-3 and egal(px, b["open"])',
                                               "INTACTE CONTREDITE"),
    "S-M1f C-15 zone morte dans la boucle ②": (
        EPREUVE, '        if bas(b["open"]) or bas(b["low"]) or haut(b["open"]) or haut(b["high"]):',
        '        if bas(b["open"]) or bas(b["low"]) or haut(b["open"]) or b["high"] >= obj + 1e-3:',
        "INTACTE CONTREDITE"),
    "S-M1g N-45 trou toujours faux": (EPREUVE, "    trou = calendrier.index(dd[z]) - calendrier.index(dd[a]) != z - a\n",
                                      "    trou = False\n", "INTACTE CONTREDITE"),
    # S-M2 : un témoin retiré (la famille ARRONDI, seule à tuer « EPS_SEUIL = 0 », N-43) → un survivant nommé
    "S-M2 famille ARRONDI retirée": (
        os.path.join("tests", "EPREUVES_DES_MUTANTS_DU_CONTROLE_DES_TRADES_Jeu_26-11-2026.py"),
        "    for pe in (100.0002, 100.0006, 25.6002, 145.0010, 33.3338):\n", "    for pe in ():\n", "SURVIVANT"),
    # S-M3 : le mutateur saute une branche → la complétude rougit
    "S-M3 mutateur qui saute la branche TP": (
        os.path.join("tests", "EPREUVES_DES_MUTANTS_DU_CONTROLE_DES_TRADES_Jeu_26-11-2026.py"),
        "                if isinstance(e, ast.AST):\n",
        "                if isinstance(e, ast.AST) and not (isinstance(n, ast.If) and"
        " ast.unparse(n.test) == \"motif == 'TP'\"):\n", "COMPLÉTUDE"),
    # S-M4 : l'oracle saboté (le TP vendu au plus haut) → (b) rougit
    "S-M4 oracle : TP vendu au plus haut": (os.path.join("programmes", "MODULE_POSITIONS.py"),
                                            '    if bar["high"] >= tp:\n        return tp, "TP"',
                                            '    if bar["high"] >= tp:\n        return bar["high"], "TP"',
                                            "INTACTE CONTREDITE"),
}


def saboter(racine):
    """Joue chaque sabotage sur une copie ; rend 0 si chacun mord, 1 sinon, 2 si un texte est introuvable.
    ① RÔLE — R-731 : l'épreuve rougit quand on sabote. ② CONTEXTE D'APPEL — `__main__` « --saboter ». ③ ENTRÉE — la
    racine. ④ CONDITIONS D'ENTRÉE — les textes « avant » existent une fois. ⑤ SORTIE — UNE valeur : le code.
    [rend: 1] ⑥ TRAITEMENT — copie de tests/ (ce fichier et l'épreuve) et de programmes/ sous un dossier temporaire,
    remplacement, lancement de ce fichier en processus neuf, code 1 et mot attendu exigés. ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — sabotages ① à ④ de la consigne. ⑨ CE QUI CLOCHE — S-M3 vise la branche TP par son texte : renommer
    le motif la fait chercher en vain (code 2, dit). ⑩ EFFET — écrit sous un dossier temporaire, l'efface.
    ⑪ TERMINAISON — chaque lancement a un délai de 600 s ; rend la main. [sort: non]"""
    code = 0
    moi = os.path.join("tests", os.path.basename(__file__))
    for nom, (fichier, avant, apres, mot) in SABOTAGES.items():
        d = tempfile.mkdtemp(prefix="mutants_sabot_")
        try:
            os.makedirs(os.path.join(d, "tests"))
            for f in (EPREUVE, moi):
                shutil.copy(os.path.join(racine, f), os.path.join(d, f))
            shutil.copytree(os.path.join(racine, "programmes"), os.path.join(d, "programmes"),
                            ignore=shutil.ignore_patterns("__pycache__"))
            chemin = os.path.join(d, fichier)
            t = open(chemin, encoding="utf-8").read()
            if t.count(avant) != 1:
                print("❌ %s : texte à saboter présent %d fois — NON JOUÉ" % (nom, t.count(avant)))
                code = max(code, 2)
                continue
            open(chemin, "w", encoding="utf-8").write(t.replace(avant, apres))
            complet = nom.startswith("S-M2")       # seul S-M2 a besoin des mutants ; les autres : l'intacte suffit
            r = subprocess.run([sys.executable, "-B", os.path.join(d, moi), d] + ([] if complet else
                                                                                ["--sans-mutants"]),
                               capture_output=True, text=True, timeout=600)
            ligne = next((x for x in r.stdout.splitlines() if mot in x), "")
            if r.returncode == 1 and ligne:
                print("✅ %s → MORD (code 1) : %s" % (nom, ligne.strip()[:220]))
            else:
                print("❌ %s → NE MORD PAS (code %d, « %s » %s)" % (nom, r.returncode, mot,
                                                                   "absent" if not ligne else "présent"))
                code = max(code, 1)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print("SABOTAGES : %s" % ("TOUS MORDENT" if code == 0 else "NON CONFORME"))
    return code


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.split("USAGE : ")[1].split("\n")[0])
        sys.exit(2)
    try:
        sys.exit(saboter(os.path.abspath(args[0])) if "--saboter" in sys.argv else principal(os.path.abspath(args[0])))
    except Exception as e:  # noqa: BLE001 — R-734 : une épreuve qui n'a pas pu tourner rend 2
        import traceback
        traceback.print_exc()
        print("ÉPREUVE NON JOUÉE : %s: %s" % (type(e).__name__, e))
        sys.exit(2)
