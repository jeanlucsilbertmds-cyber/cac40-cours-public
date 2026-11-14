#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BALAYER_LES_MUTANTS_DES_JOURNEES — Ven 13-11-2026 (Paris), E2c tours 4 et 5. Simulation uniquement.

① RÔLE — Soumettre à une mutation systématique les trois fonctions qui remettent au bon jour les journées que bnains a
  rangées sous un autre jour, et RANGER chaque mutant dans l'une de quatre classes, en confrontant deux mesures : ce que
  disent les ÉPREUVES (une épreuve tombe-t-elle ?) et ce que fait la FONCTION (sa sortie diffère-t-elle EN CONTENU de
  celle de l'original, sur un domaine énuméré ?). Les fonctions : `journees_d_un_autre_jour` et `redater_les_journees`
  (programmes/CONTROLER_L_HISTORIQUE_LONG.py, dit K), jouées contre la couche A (H69 à H75, `epreuves_des_journees`
  des épreuves de l'historique long) ; `journees_hors_de_leur_fichier` (le juge de P17,
  tests/EPREUVES_DU_FICHIER_DES_VINGT_ANS_Jeu_12-11-2026.py), jouée en mémoire contre le témoin tel quel et ses
  sabotages (`sabotages_de_p17`).
② CONTEXTE D'APPEL — python3 -I tests/outils/BALAYER_LES_MUTANTS_DES_JOURNEES.py <racine> [--complet]
  <racine> : un dépôt (un clone neuf) qui porte un témoin des 20 ans avec son manifeste au contrat (sinon la partie
  P17 ne peut pas tourner : code 2). --complet : chaque mutant de K que la couche A laisse vert est rejoué contre
  TOUTES les épreuves de l'historique long (`epreuves`, environ deux minutes par mutant).
③ ENTRÉE — Le dépôt : les deux programmes éprouvés, les deux fichiers d'épreuves, leurs données.
④ CONDITIONS D'ENTRÉE — Les trois fonctions existent sous leur nom ; le mutant zéro (la fonction réécrite par
  `ast.unparse` SANS mutation) rend toutes les épreuves vertes ET la même sortie que l'original sur tout le domaine —
  sinon le balayage mesurerait la réécriture et non la mutation : arrêt, code 2.
⑤ SORTIE — UNE valeur : le code — 0 quand aucun mutant n'est SURVIVANT ni ÉPREUVE QUI SUR-SPÉCIFIE, que chaque
  déclaration écrite d'EQUIVALENTS vise un ÉQUIVALENT MESURÉ et que sa preuve se rejoue, et que chaque contre-épreuve
  de dents (m-i, m-j, m-l) manque ce qu'elle doit manquer ; 1 sinon ; 2 si le balayage n'a pas pu tourner (R-734). Une
  ligne par mutant : « M<n> <fonction> l.<ligne> <mutation> → <CLASSE> · épreuves [...] · contenu … ».
  [rend: 1]
⑥ TRAITEMENT — ① lire chaque fonction dans son fichier par `ast` ; ② bâtir le DOMAINE : pour `redater_les_journees`,
  toutes les tables partielles sur quatre jours (et un cinquième hors table), chacune avec chaque ensemble de jours
  présents seul puis tous ensemble dans un appel à plusieurs valeurs (`domaine_des_journees`, LU dans les épreuves de
  l'historique long depuis le tour 6, la même énumération que H73 et que la preuve `_tables_reciproques_egales`,
  R-708) — et l'original doit y rendre exactement l'oracle `attendu_de_redater` des mêmes épreuves, sinon arrêt,
  code 2 —, plus les entrées que la couche A passe vraiment à la fonction
  (espionnées au mutant zéro) ; pour `journees_d_un_autre_jour`, les racines que la couche A lui passe (fichiers
  d'entrée de H69 à H75) et le vrai indice ; pour le juge de P17, le témoin et chaque sabotage ; ③ énumérer les sites et
  leurs mutations (`mutations`) ; ④ pour chaque mutant : les épreuves (K par `charger` des épreuves de l'historique long,
  la copie sabotée ; P17 en mémoire) et le CONTENU de ses sorties sur tout le domaine, comparé à celui de l'original
  (`==` sur les dictionnaires, qui ignore l'ordre ; la liste `bouge` ; l'exception et l'état des barres quand il y en
  a une ; pour P17 les fautives en multiensemble, le verdict et le nombre de lignes jugées, que juge aussi l'épreuve
  J17 — m-l du relecteur E2c tour 5) ; ⑤ ranger (`classer`) ; ⑥ les contre-épreuves : S28,
  m-i (comparer quatre champs, ou la seule clôture), m-j (« la dernière gagne »), D-6 (la réécriture en vraie
  permutation), m-l (l'issue d'avant m-l, sans le nombre de lignes jugées : ses mutants retombent en ÉQUIVALENT) ;
  ⑦ les déclarations écrites d'EQUIVALENTS, preuve rejouée.
⑦ UNITÉ — Des mutants ; des épreuves ; des cas comparés.
⑧ POURQUOI — Superviseur R-759 E2c tour 4 (13-11-2026), (4) : les tours 2 et 3 trouvaient à la main un mutant survivant
  chacun ; ce qu'un programme peut faire, un programme le fait (R-754). Superviseur R-759 E2c tour 5 (13-11-2026), (2) :
  le balayage du tour 4 comptait un mutant « tué » dès qu'une épreuve tombait, et ne voyait donc pas une épreuve qui
  tombe À TORT — trois mutants de contenu identique (le saut `continue` forcé, `in` → `not in` du `any`) étaient
  « tués » par une vérification de H73 qui exigeait l'objet et l'ordre (D-6 du relecteur E2c tour 4), et la réparation
  du tour 4 avait fabriqué ce défaut. Une épreuve doit tomber exactement quand le contrat est violé : les deux sens se
  mesurent. Les QUATRE CLASSES : TUÉ (une épreuve tombe, le contenu diffère) · SURVIVANT (aucune ne tombe, le contenu
  diffère : il faut une épreuve) · ÉQUIVALENT MESURÉ (aucune ne tombe, le contenu est identique sur tout le domaine) ·
  ÉPREUVE QUI SUR-SPÉCIFIE (une épreuve tombe ALORS QUE le contenu est identique : elle exige plus que le contrat).
⑨ CE QUI CLOCHE — UN DOMAINE ÉNUMÉRÉ N'EST PAS UNE PREUVE UNIVERSELLE : un mutant identique sur le domaine mais
  différent au-delà serait rangé ÉQUIVALENT MESURÉ à tort. Pourquoi ce domaine suffit ici pour `redater_les_journees` :
  la fonction ne lit des dates que leur appartenance à la table, et quatre jours couvrent toute forme d'une table
  réciproque à une ou deux paires, plus un jour fixe (le même argument que le ⑧ de `_tables_reciproques_egales`) ; NON
  couvert : une table à trois paires ou plus. · DEPUIS LE TOUR 6 (superviseur R-759, (1) (a)), pour
  `redater_les_journees`, la classe SURVIVANT est IMPOSSIBLE sur le domaine : H73 juge la sortie par l'oracle sur ce
  même domaine, et l'original y rend l'oracle — tout mutant de contenu différent y rougit H73. Le balayage garde sa
  valeur, pour cette fonction, sur la classe ÉPREUVE QUI SUR-SPÉCIFIE, et pour `journees_d_un_autre_jour` et le juge
  de P17. Les réécritures sémantiques d'un prédicat (`journees.get(vrai) != j` → `vrai not in journees`) ne sont pas
  des mutations d'opérateur : elles ne s'énumèrent pas, et ne sont pas ajoutées (n-1 de Cowork). Pour `journees_d_un_autre_jour`, le domaine est celui des fichiers que les
  épreuves fabriquent et du vrai indice : une constante mutée à l'intérieur de sa marge (ACCORD_INDICE × 2, ÷ 2) y est
  identique ; c'est une équivalence SUR LES DONNÉES, que déclare EQUIVALENTS avec la marge mesurée
  (`_marge_d_accord_indice`). Pour P17, le domaine est le témoin et ses sabotages. · Les mutations jouées : `and` ↔
  `or`, retrait d'une clause d'un `and`/`or` ou d'une comparaison enchaînée, `in` ↔ `not in`, `is` ↔ `is not`, `==` ↔
  `!=`, `<=` ↔ `<`, `>=` ↔ `>`, `not` retiré, test d'un `if` (ou d'un filtre de compréhension) forcé à vrai puis à
  faux, un élément retiré d'un n-uplet parcouru par `for`, `+ 1` ↔ `- 1`, RETRAIT de chaque instruction de chaque bloc
  (remplacée par `pass`), chaque CONSTANTE numérique × 2 et ÷ 2 (entière : division entière), y compris une constante
  numérique du module nommée en capitales (ACCORD_INDICE). NE SONT PAS mutés : les appels, les chaînes, les
  remplacements d'une instruction par une autre (`avant = s`, `setdefault` : R4 et R8 du relecteur E2c tour 4, joués
  à la main), l'intérieur d'une f-chaîne (le texte d'un message : au premier passage du tour 5, les indices de
  `f"{l[0]} {l[1]} …"` mutés changeaient le texte des fautives, et rien d'autre). Un mutant dont le texte est celui de
  l'original n'est pas compté. · K est muté sur la couche A seulement
  (sauf --complet). · `ast.unparse` perd les commentaires de la fonction : sans effet sur le code (mutant zéro).
⑩ EFFET — Lit ; affiche. Des copies jetables des programmes et des dossiers d'essai, chacun sous un dossier temporaire
  effacé après chaque mutant ; le dossier du domaine est effacé à la fin.
⑪ TERMINAISON — Rend la main : un nombre fini de mutants, aucune boucle ouverte (aucune mutation ne crée de `while`) ;
  l'appel de `principal` des épreuves des 20 ans ne lance aucun processus sans --saboter.
"""
import ast
import contextlib
import copy
import importlib.util
import io
import os
import shutil
import sys
import tempfile

FONCTIONS_K = ("journees_d_un_autre_jour", "redater_les_journees")
FONCTION_P17 = "journees_hors_de_leur_fichier"
EPREUVES_HL = os.path.join("tests", "EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py")
EPREUVES_VA = os.path.join("tests", "EPREUVES_DU_FICHIER_DES_VINGT_ANS_Jeu_12-11-2026.py")
CONTROLE = os.path.join("programmes", "CONTROLER_L_HISTORIQUE_LONG.py")
CONTRAIRES = {ast.In: ast.NotIn, ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.Eq: ast.NotEq,
              ast.NotEq: ast.Eq, ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt}
TUE, SURVIVANT, EQUIVALENT, SUR_SPECIFIE = "TUÉ", "SURVIVANT", "ÉQUIVALENT MESURÉ", "ÉPREUVE QUI SUR-SPÉCIFIE"
# LE MODULE DES ÉPREUVES DE L'HISTORIQUE LONG, chargé par `balayer` : il porte le domaine (`domaine_des_journees`) et
# l'oracle (`attendu_de_redater`) de `redater_les_journees`, en UN exemplaire, que ce balayage LIT (superviseur R-759
# E2c tour 6, 13-11-2026, (2) 1 ; R-708). Il ne peut pas être chargé à l'import : il lit sa racine dans `sys.argv`.
HL = None
# Le module des épreuves des 20 ans, chargé par `balayer` : il porte l'épreuve J17 (`ecarts_de_j17`), en UN exemplaire,
# que `juger_p17` appelle (n-2 de Cowork, superviseur R-759 E2c tour 6, (3) ; R-708).
VA = None


def _accord_jamais_atteint(K):
    """Preuve rejouée : aucun flottant q ne donne abs(q - 1) == K.ACCORD_INDICE, donc `<=` et `<` décident pareil.

    ① RÔLE — Rejouer la preuve d'équivalence des deux mutants `<=` → `<` sur ACCORD_INDICE.
    ② CONTEXTE D'APPEL — `balayer`, par EQUIVALENTS.
    ③ ENTRÉE — `K` : le contrôle chargé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai quand ni 1 + A ni 1 − A n'est un flottant (A = ACCORD_INDICE).
      [rend: 1]
    ⑥ TRAITEMENT — Pour q dans [0,5 ; 2], q − 1 est exact (lemme de Sterbenz) : abs(q − 1) == A exige q = 1 + A ou
      1 − A EXACTEMENT ; hors de [0,5 ; 2], abs(q − 1) ≥ 0,5 > A. Or si 1 + A n'est pas un flottant, (1 + A) − 1,
      calculé, diffère de A (l'arrondi de la somme, puis une soustraction exacte) ; de même pour 1 − A.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une égalité au bord est impossible : aucun domaine fini ne peut l'atteindre, la preuve est écrite.
    ⑨ CE QUI CLOCHE — La preuve vaut pour la valeur actuelle d'ACCORD_INDICE, rejouée à chaque balayage.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a = K.ACCORD_INDICE
    return 0 < a < 0.5 and (1 + a) - 1 != a and 1 - (1 - a) != a


def _tables_reciproques_egales(K):
    """Preuve rejouée : pour toute table que `redater_les_journees` accepte, l'ensemble de ses jours de rangement est
    celui de ses jours vrais ; `any(j in avant …)`, `any(vrai in avant …)` et leur `or` sont donc égaux.

    ① RÔLE — Rejouer la preuve d'équivalence des deux mutants « clause retirée » du `any`, au-delà du domaine.
    ② CONTEXTE D'APPEL — `balayer`, par EQUIVALENTS.
    ③ ENTRÉE — `K` : le contrôle chargé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai quand, pour CHAQUE table de `domaine_des_journees` que la fonction accepte, et CHAQUE
      ensemble de jours présents, les trois `any` sont égaux.
      [rend: 1]
    ⑥ TRAITEMENT — Le domaine de `domaine_des_journees` des épreuves de l'historique long (625 tables, 32
      présences) ; l'acceptation est demandée à la fonction elle-même (une table refusée lève).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — En toutes lettres : si journees[journees[j]] = j pour tout j, chaque jour de rangement j est le jour
      vrai de journees[j], et chaque jour vrai v = journees[j] est un jour de rangement (journees[v] = j existe) — les
      deux ensembles sont égaux. Le refus s'applique AVANT le `any` : aucune table non réciproque n'y arrive. Cet
      argument vaut pour toute taille de table : c'est ce que le domaine énuméré ne peut pas atteindre.
    ⑨ CE QUI CLOCHE — L'énumération borne la vérification à quatre jours ; l'argument du ⑧ vaut pour toute taille.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : 625 × 32 cas au plus.
      [sort: non]
    """
    tables, presences = HL.domaine_des_journees()
    for table in tables:
        try:
            K.redater_les_journees({}, table)
        except ValueError:
            continue
        for avant in presences:
            a = any(j in avant for j in table)
            b = any(v in avant for v in table.values())
            c = any(j in avant or v in avant for j, v in table.items())
            if not a == b == c:
                return False
    return True


def _marge_d_accord_indice(K):
    """Preuve rejouée : sur le vrai indice, A ÷ 2, A et A × 2 rendent la même table, et A × 10 une autre (A = ACCORD_INDICE).

    ① RÔLE — Rejouer la preuve d'équivalence SUR LES DONNÉES des mutants de la constante ACCORD_INDICE × 2 et ÷ 2 (R6
      et R7 du relecteur E2c tour 4) : ils sont à l'intérieur de la marge du calibrage, et la constante est gardée à
      l'extérieur de cette marge.
    ② CONTEXTE D'APPEL — `balayer`, par EQUIVALENTS.
    ③ ENTRÉE — `K` : le contrôle chargé (sa racine de travail est le dépôt : le vrai indice).
    ④ CONDITIONS D'ENTRÉE — Le dépôt porte l'indice (OSError sinon, rattrapée par `balayer` : code 2).
    ⑤ SORTIE — UNE valeur : vrai quand les tables à A ÷ 2, A et A × 2 sont égales et non vides, et celle à A × 10 en
      diffère.
      [rend: 1]
    ⑥ TRAITEMENT — Change ACCORD_INDICE dans le module, appelle la fonction sur la racine courante, remet la valeur.
    ⑦ UNITÉ — Des facteurs sans unité.
    ⑧ POURQUOI — Superviseur R-759 E2c tour 5, (3) : une constante n'est gardée qu'à l'extérieur de sa marge ; mesuré le
      13-11-2026 : la table ne change pas de A × 0 à A × 5, et A × 10 y ajoute le 2013-12-19 (non réciproque) ; affiné
      par Cowork (O-b, E2c tour 5) et rejoué au tour 6 : identique jusqu'à A × 6, NON réciproque dès A × 8 (H73 exige
      le refus de cette table réelle).
    ⑨ CE QUI CLOCHE — La marge est celle du vrai indice d'aujourd'hui ; un indice neuf la changerait (l'archive bnains
      s'arrête au 28-02-2017 : aucun cas nouveau ne peut y entrer).
    ⑩ EFFET — Change puis remet une constante du module.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a = K.ACCORD_INDICE
    try:
        tables = {}
        for f in (0.5, 1, 2, 10):
            K.ACCORD_INDICE = a * f
            tables[f] = K.journees_d_un_autre_jour(".")
    finally:
        K.ACCORD_INDICE = a
    print(f"      marge d'ACCORD_INDICE sur le vrai indice : { {f: sorted(x) for f, x in tables.items()} }")
    return bool(tables[1]) and tables[0.5] == tables[1] == tables[2] != tables[10]


# LES PREUVES ÉCRITES — {(fonction, description) : (preuve écrite, preuve rejouée)}. Elles ne valent que pour ce que le
# domaine ne peut pas atteindre (superviseur E2c tour 5, (2) 2) : le bord flottant d'ACCORD_INDICE, une table de plus de
# quatre jours, un indice autre que ceux des épreuves. Une déclaration doit viser un mutant rangé ÉQUIVALENT MESURÉ, et
# sa preuve doit se rejouer ; sinon arrêt, code 2 (une déclaration qui ne vise plus rien est une décoration).
EQUIVALENTS = {
    ("journees_d_un_autre_jour", "`<=` → `<` : abs(float(b) / float(y) - 1) <= ACCORD_INDICE"): (
        "aucun flottant q ne donne abs(q - 1) == ACCORD_INDICE (1 ± 0,0005 ne sont pas des flottants) : `<=` et `<` "
        "décident pareil pour toute entrée", _accord_jamais_atteint),
    ("journees_d_un_autre_jour", "`<=` → `<` : abs(float(b) / float(lignes[j][2]) - 1) <= ACCORD_INDICE"): (
        "même preuve : le bord n'est jamais atteint", _accord_jamais_atteint),
    ("journees_d_un_autre_jour", "constante ACCORD_INDICE → ACCORD_INDICE * 2 : abs(float(b) / float(y) - 1) <= ACCORD_INDICE"): (
        "équivalent SUR LES DONNÉES : à l'intérieur de la marge du calibrage, mesurée sur le vrai indice (R6 du "
        "relecteur E2c tour 4)", _marge_d_accord_indice),
    ("journees_d_un_autre_jour", "constante ACCORD_INDICE → ACCORD_INDICE / 2 : abs(float(b) / float(y) - 1) <= ACCORD_INDICE"): (
        "même preuve (R7)", _marge_d_accord_indice),
    ("journees_d_un_autre_jour",
     "constante ACCORD_INDICE → ACCORD_INDICE * 2 : abs(float(b) / float(lignes[j][2]) - 1) <= ACCORD_INDICE"): (
        "même preuve", _marge_d_accord_indice),
    ("journees_d_un_autre_jour",
     "constante ACCORD_INDICE → ACCORD_INDICE / 2 : abs(float(b) / float(lignes[j][2]) - 1) <= ACCORD_INDICE"): (
        "même preuve", _marge_d_accord_indice),
    ("redater_les_journees", "clause retirée « j in avant »"): (
        "une table acceptée est réciproque : ses jours de rangement et ses jours vrais sont le même ensemble, pour toute "
        "taille de table", _tables_reciproques_egales),
    ("redater_les_journees", "clause retirée « vrai in avant »"): (
        "même preuve", _tables_reciproques_egales),
}


def mutations(fonction, constantes):
    """Énumère les mutations d'une fonction ; rend la liste des (ligne, description, fonction mutée).

    ① RÔLE — Le générateur de mutants.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `fonction` : le nœud `ast.FunctionDef`, lu dans son fichier (les numéros de ligne sont ceux du fichier) ·
      `constantes` : les noms des constantes numériques du module de la fonction (nommées en capitales).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des (ligne du site, description, nœud muté), dans l'ordre de parcours ; le nœud
      muté est une COPIE, l'original n'est pas touché. Un mutant dont le texte est celui de l'original est omis.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourt la copie du corps (docstring exclue) ; à chaque site, la mutation se fait sur une copie
      neuve de la fonction, retrouvée par la position du site dans le parcours (le même `ast.walk` sur la copie).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑧ du fichier. Le retrait d'instruction et les constantes × 2, ÷ 2 : superviseur E2c tour 5, (3)
      — sinon le relecteur les retrouve à la main (R1 à R7 du relecteur E2c tour 4), et un tour de plus naît de ce que le
      programme aurait pu voir (R-754).
    ⑨ CE QUI CLOCHE — Voir ⑨ du fichier (les mutations non faites).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sites = []
    noeuds = list(ast.walk(fonction))
    docstring = fonction.body[0]
    # ni la docstring, ni l'intérieur d'une f-chaîne : le texte d'un message n'est pas du calcul (⑨ du fichier)
    hors_calcul = set(map(id, ast.walk(docstring)))
    for n in ast.walk(fonction):
        if isinstance(n, ast.JoinedStr):
            hors_calcul |= set(map(id, ast.walk(n)))
    for k, n in enumerate(noeuds):
        if id(n) in hors_calcul:
            continue
        if isinstance(n, ast.BoolOp):
            sites.append((k, "op", f"`{'and' if isinstance(n.op, ast.And) else 'or'}` → "
                                   f"`{'or' if isinstance(n.op, ast.And) else 'and'}` : {ast.unparse(n)[:70]}"))
            for i in range(len(n.values)):
                sites.append((k, ("retrait", i), f"clause retirée « {ast.unparse(n.values[i])[:60]} »"))
        if isinstance(n, ast.Compare):
            for i, op in enumerate(n.ops):
                if type(op) in CONTRAIRES:
                    sites.append((k, ("cmp", i), f"`{ast.unparse(ast.Compare(ast.Name('a'), [op], [ast.Name('b')]))[2:-2]}` → "
                                               f"`{ast.unparse(ast.Compare(ast.Name('a'), [CONTRAIRES[type(op)]()], [ast.Name('b')]))[2:-2]}`"
                                               f" : {ast.unparse(n)[:60]}"))
            if len(n.ops) == 2:
                for i in range(2):
                    sites.append((k, ("chaine", i), f"comparaison enchaînée, clause {i + 1} retirée : {ast.unparse(n)[:60]}"))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            sites.append((k, "not", f"`not` retiré : {ast.unparse(n)[:60]}"))
        if isinstance(n, (ast.If, ast.IfExp, ast.While)):
            for v in (True, False):
                sites.append((k, ("force", v), f"test forcé à {v} : {ast.unparse(n.test)[:60]}"))
        if isinstance(n, ast.comprehension):
            for i in range(len(n.ifs)):
                for v in (True, False):
                    sites.append((k, ("filtre", i, v), f"filtre forcé à {v} : {ast.unparse(n.ifs[i])[:60]}"))
        if isinstance(n, ast.For) and isinstance(n.iter, ast.Tuple) and len(n.iter.elts) >= 2:
            for i in range(len(n.iter.elts)):
                sites.append((k, ("nuplet", i), f"`{ast.unparse(n.iter.elts[i])}` retiré de {ast.unparse(n.iter)}"))
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub)) and isinstance(n.right, ast.Constant) \
                and n.right.value == 1:
            sites.append((k, "pm1", f"`{'+' if isinstance(n.op, ast.Add) else '-'} 1` → "
                                    f"`{'-' if isinstance(n.op, ast.Add) else '+'} 1` : {ast.unparse(n)[:60]}"))
        # E2c tour 5 — le retrait de chaque instruction de chaque bloc (remplacée par `pass`)
        for champ in ("body", "orelse", "finalbody"):
            bloc = getattr(n, champ, None)
            if isinstance(bloc, list) and bloc and isinstance(bloc[0], ast.stmt):
                for i, s in enumerate(bloc):
                    if s is docstring:
                        continue
                    sites.append((k, ("instruction", champ, i),
                                  f"instruction retirée : {ast.unparse(s).splitlines()[0][:70]}"))
        # E2c tour 5 — chaque constante numérique × 2 et ÷ 2, littérale ou nommée en capitales dans le module
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            for fois in (2, 0.5):
                nouveau = n.value * 2 if fois == 2 else (n.value // 2 if type(n.value) is int else n.value / 2)
                if nouveau != n.value:
                    sites.append((k, ("constante", fois), None))
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in constantes:
            for fois in (2, 0.5):
                sites.append((k, ("nommee", fois), None))
    sortie = []
    reference = ast.unparse(fonction)
    parents = {}
    for p in ast.walk(fonction):
        for c in ast.iter_child_nodes(p):
            parents[id(c)] = p
    for k, quoi, texte in sites:
        f = copy.deepcopy(fonction)
        n = list(ast.walk(f))[k]
        ligne = getattr(n, "lineno", None) or n.iter.lineno     # un `comprehension` n'a pas de ligne : celle de son itérable
        if quoi == "op":
            n.op = ast.Or() if isinstance(n.op, ast.And) else ast.And()
        elif quoi == "not":
            remplacer(f, n, n.operand)
        elif quoi == "pm1":
            n.op = ast.Sub() if isinstance(n.op, ast.Add) else ast.Add()
        elif quoi[0] == "retrait":
            reste = n.values[:quoi[1]] + n.values[quoi[1] + 1:]
            if len(reste) == 1:
                remplacer(f, n, reste[0])
            else:
                n.values = reste
        elif quoi[0] == "cmp":
            n.ops[quoi[1]] = CONTRAIRES[type(n.ops[quoi[1]])]()
        elif quoi[0] == "chaine":
            if quoi[1] == 0:
                n.left, n.ops, n.comparators = n.comparators[0], n.ops[1:], n.comparators[1:]
            else:
                n.ops, n.comparators = n.ops[:1], n.comparators[:1]
        elif quoi[0] == "force":
            n.test = ast.Constant(quoi[1])
        elif quoi[0] == "filtre":
            n.ifs[quoi[1]] = ast.Constant(quoi[2])
        elif quoi[0] == "nuplet":
            n.iter.elts = n.iter.elts[:quoi[1]] + n.iter.elts[quoi[1] + 1:]
        elif quoi[0] == "instruction":
            bloc = getattr(n, quoi[1])
            ligne = bloc[quoi[2]].lineno
            bloc[quoi[2]] = ast.Pass()
        elif quoi[0] == "constante":
            ancienne = n.value
            n.value = n.value * 2 if quoi[1] == 2 else (n.value // 2 if type(n.value) is int else n.value / 2)
            texte = f"constante {ancienne!r} → {n.value!r} : {ast.unparse(parents[id(noeuds[k])])[:60]}"
        elif quoi[0] == "nommee":
            # le site de la constante nommée : sa ligne, et la comparaison où elle sert (l'ancêtre `Compare` le plus
            # proche, sinon son parent)
            op = ast.Mult() if quoi[1] == 2 else ast.Div()
            remplacer(f, n, ast.BinOp(ast.Name(n.id, ast.Load()), op, ast.Constant(2)))
            haut = parents[id(noeuds[k])]
            while not isinstance(haut, ast.Compare) and isinstance(parents.get(id(haut)), ast.expr):
                haut = parents[id(haut)]
            texte = f"constante {n.id} → {n.id} {'*' if quoi[1] == 2 else '/'} 2 : {ast.unparse(haut)[:60]}"
        ast.fix_missing_locations(f)
        if ast.unparse(f) == reference:
            continue
        sortie.append((ligne, texte, f))
    return sortie


def remplacer(arbre, ancien, nouveau):
    """Remplace dans `arbre` le nœud `ancien` par `nouveau` (champ simple ou élément de liste) ; lève s'il est absent.

    ① RÔLE — L'outil des mutations qui remplacent un nœud entier (`not` retiré, clause retirée d'un `and`/`or` à deux,
      constante nommée multipliée ou divisée).
    ② CONTEXTE D'APPEL — `mutations`.
    ③ ENTRÉE — `arbre` : la fonction copiée · `ancien` : un nœud de cette copie · `nouveau` : son remplaçant.
    ④ CONDITIONS D'ENTRÉE — `ancien` est un enfant d'un nœud de `arbre` (ValueError sinon).
    ⑤ SORTIE — — (modifie `arbre`).
      [rend: 0]
    ⑥ TRAITEMENT — Cherche le parent par `ast.iter_fields`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `ast` n'a pas de lien vers le parent.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Modifie `arbre`.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    for p in ast.walk(arbre):
        for champ, valeur in ast.iter_fields(p):
            if valeur is ancien:
                setattr(p, champ, nouveau)
                return
            if isinstance(valeur, list):
                for i, x in enumerate(valeur):
                    if x is ancien:
                        valeur[i] = nouveau
                        return
    raise ValueError("nœud absent")


def lire_fonction(chemin, nom):
    """Rend (texte original de la fonction, nœud `ast`) de la fonction `nom` du fichier `chemin`.

    ① RÔLE — Trouver la fonction à muter et le texte exact à remplacer.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `chemin` : un fichier Python · `nom` : le nom d'une fonction de premier niveau.
    ④ CONDITIONS D'ENTRÉE — La fonction existe une fois (ValueError sinon).
    ⑤ SORTIE — DEUX valeurs : le texte de la fonction dans le fichier (de `def` à sa dernière ligne) ; son nœud.
      [rend: 2]
    ⑥ TRAITEMENT — `ast.parse`, puis les lignes `lineno` à `end_lineno`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le texte sert de cible au remplacement, comme les sabotages T des épreuves (une cible exacte).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    texte = open(chemin, encoding="utf-8").read()
    arbre = ast.parse(texte)
    trouves = [n for n in arbre.body if isinstance(n, ast.FunctionDef) and n.name == nom]
    if len(trouves) != 1:
        raise ValueError(f"{nom} trouvée {len(trouves)} fois dans {chemin}")
    f = trouves[0]
    lignes = texte.split("\n")
    return "\n".join(lignes[f.lineno - 1:f.end_lineno]), f


def charger_module(chemin, nom):
    """Charge un fichier Python comme module, sous `nom` ; rend le module.

    ① RÔLE — Charger les deux fichiers d'épreuves sans les lancer.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (OSError sinon).
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — `importlib`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves de l'historique long lisent la racine dans `sys.argv` à leur chargement.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut du module (lectures du calendrier pour l'historique long).
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


@contextlib.contextmanager
def dossier_jetable():
    """Fait du dossier temporaire un sous-dossier neuf le temps d'un bloc, puis l'efface.

    ① RÔLE — Borner la place prise par chaque mutant : les copies de `charger` et les racines d'essai des épreuves.
    ② CONTEXTE D'APPEL — `juger_k`, `juger_k_complet`, la contre-épreuve D-6.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur, cédée au bloc `with` : le chemin du dossier neuf.
      [rend: 1]
    ⑥ TRAITEMENT — `tempfile.mkdtemp` sous le dossier courant, `tempfile.tempdir` changé puis remis, `shutil.rmtree`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le tour 5 joue environ trois fois plus de mutants que le tour 4 ; chaque passage de la couche A copie
      une racine d'essai. Sans effacement, le disque (environ 5 Go libres) ne suffirait pas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée puis efface un dossier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    garde = tempfile.tempdir
    d = tempfile.mkdtemp(prefix="mutant_")
    tempfile.tempdir = d
    try:
        yield d
    finally:
        tempfile.tempdir = garde
        shutil.rmtree(d, ignore_errors=True)


def juger_k(hl, cible, remplace):
    """Joue la couche A contre K où `cible` est remplacé par `remplace` ; rend la liste triée des épreuves rouges.

    ① RÔLE — Le juge « épreuves » d'un mutant de K.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `hl` : le module des épreuves de l'historique long · `cible` : le texte original de la fonction ·
      `remplace` : la fonction mutée (texte).
    ④ CONDITIONS D'ENTRÉE — `cible` se trouve une fois dans K.
    ⑤ SORTIE — UNE valeur : la liste des épreuves rouges ; [« chargement : … »] si K muté ne se charge pas.
      [rend: 1]
    ⑥ TRAITEMENT — `hl.charger` (copie sabotée, comme les sabotages T), puis `hl.epreuves_des_journees`, dans un
      dossier jetable.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule mécanique de sabotage pour K (R-708).
    ⑨ CE QUI CLOCHE — Les sorties écran des épreuves sont avalées.
    ⑩ EFFET — Une copie jetable des programmes, effacée.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with dossier_jetable(), contextlib.redirect_stdout(io.StringIO()):
        try:
            K, _ = hl.charger((hl.CONTROLE, cible, remplace))
        except Exception as x:   # noqa: BLE001
            return [f"chargement : {type(x).__name__}"]
        res = hl.epreuves_des_journees(K)
    return sorted(k for k, v in res.items() if not v)


def juger_k_complet(hl, cible, remplace):
    """Joue TOUTES les épreuves de l'historique long contre K muté ; rend la liste triée des épreuves rouges.

    ① RÔLE — Le second juge, pour les mutants que la couche A laisse verts (option --complet).
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — Comme `juger_k`.
    ④ CONDITIONS D'ENTRÉE — Comme `juger_k`.
    ⑤ SORTIE — UNE valeur : la liste des épreuves rouges.
      [rend: 1]
    ⑥ TRAITEMENT — `hl.charger`, puis `hl.epreuves`, dans un dossier jetable.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un mutant que seule une épreuve hors de la couche A rougit n'est pas un survivant.
    ⑨ CE QUI CLOCHE — Environ deux minutes par mutant.
    ⑩ EFFET — Des copies et des dossiers jetables, effacés.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with dossier_jetable(), contextlib.redirect_stdout(io.StringIO()):
        K, R = hl.charger((hl.CONTROLE, cible, remplace))
        res = hl.epreuves(K, R)
    return sorted(k for k, v in res.items() if not v)


def fonction_de(texte, nom, espace):
    """Rend la fonction `nom` écrite `texte`, compilée dans une copie de l'espace de noms `espace` ; None si elle ne se
    compile pas.

    ① RÔLE — Avoir en main la fonction mutée elle-même, pour la comparaison différentielle.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `texte` : la fonction (texte) · `nom` : son nom · `espace` : le `__dict__` du module d'origine (ses
      constantes, ses imports).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la fonction, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — `exec` dans une COPIE de l'espace : le module d'origine n'est pas touché.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La fonction est jouée seule, sur le domaine ; ses appels internes restent ceux du module.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    ns = dict(espace)
    try:
        exec(compile(texte, f"<mutant {nom}>", "exec"), ns)
    except Exception:   # noqa: BLE001
        return None
    return ns[nom]


def issue(f, *args):
    """Rend ce que fait `f(*args)` : (« rend », sortie, arguments après l'appel) ou (« lève », type, arguments après).

    ① RÔLE — Le CONTENU d'un appel, comparable par `==`.
    ② CONTEXTE D'APPEL — `issues_redater`, `issues_journees`, `issues_p17`.
    ③ ENTRÉE — `f` : une fonction (ou None : elle ne s'est pas compilée) · `args` : ses arguments, déjà copiés par
      l'appelant (la fonction peut les modifier en place, et ce qu'elle en fait fait partie de l'issue).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un n-uplet comparable par `==` — les dictionnaires s'y comparent EN CONTENU (l'ordre et
      l'identité n'y comptent pas, comme le contrat de `redater_les_journees`).
      [rend: 1]
    ⑥ TRAITEMENT — Un appel dans un `try`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur E2c tour 5, (2) 1 : on compare le contenu du dictionnaire extérieur passé, la sortie et
      l'exception levée (avec les arguments, intacts ou non, quand il y en a une).
    ⑨ CE QUI CLOCHE — Le message de l'exception n'est pas comparé, seulement son type.
    ⑩ EFFET — Celui de `f` sur ses arguments.
    ⑪ TERMINAISON — Rend la main ; `f` est une des trois fonctions, ou un mutant sans boucle ouverte.
      [sort: non]
    """
    if f is None:
        return ("ne se compile pas",)
    try:
        return ("rend", f(*args), args)
    except Exception as x:   # noqa: BLE001
        return ("lève", type(x).__name__, args)


def cas_de_redater(entrees_des_epreuves):
    """Rend les cas de la comparaison différentielle de `redater_les_journees` : une liste de (barres, table).

    ① RÔLE — Le domaine de `redater_les_journees`, mis en barres.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `entrees_des_epreuves` : les (barres, table) que la couche A a passés à la fonction (espionnés).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des cas — pour chaque table de `domaine_des_journees`, chaque présence SEULE (une
      valeur), puis TOUTES ensemble (une valeur par présence, dans un même appel) ; puis les entrées des épreuves.
      [rend: 1]
    ⑥ TRAITEMENT — La barre de la valeur v au jour d est le texte « v@d » : unique, un déplacement se voit.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur E2c tour 5, (2) 1 : « toutes les tables partielles sur trois jours, plus un quatrième jour
      hors table, et toutes les présences … On ajoute des appels à plusieurs valeurs » ; étendu à quatre jours ((2) 4).
      Les entrées des épreuves y sont jointes : sans elles, un mutant qui ne diffère que sur un vrai extrait (H72) serait
      rangé ÉPREUVE QUI SUR-SPÉCIFIE à tort. Depuis le tour 6, le domaine est lu dans les épreuves de l'historique long
      (`HL.domaine_des_journees`), qui le parcourent aussi dans H73 : ces appels-là, espionnés, s'ajoutent en double
      des cas du domaine (sans effet sur les classes, seulement sur le nombre de cas).
    ⑨ CE QUI CLOCHE — ⑨ du fichier.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : 625 × 33 cas, plus les entrées des épreuves.
      [sort: non]
    """
    tables, presences = HL.domaine_des_journees()
    cas = []
    for table in tables:
        for k, avant in enumerate(presences):
            cas.append(({f"V{k}": {d: f"V{k}@{d}" for d in sorted(avant)}}, table))
        cas.append(({f"V{k}": {d: f"V{k}@{d}" for d in sorted(avant)} for k, avant in enumerate(presences)}, table))
    return cas + list(entrees_des_epreuves)


def issues_redater(f, cas):
    """Rend la liste des issues de `f` sur chaque cas (barres copiées sur deux niveaux, table copiée).

    ① RÔLE — Le contenu de `redater_les_journees` (ou d'un mutant) sur le domaine.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `f` : la fonction · `cas` : rendu de `cas_de_redater`.
    ④ CONDITIONS D'ENTRÉE — Les barres sont des textes ou des n-uplets (immuables) : deux niveaux de copie suffisent.
    ⑤ SORTIE — UNE valeur : la liste des issues (`issue`), dans l'ordre des cas.
      [rend: 1]
    ⑥ TRAITEMENT — Un appel par cas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'issue porte le dictionnaire EXTÉRIEUR passé après l'appel : c'est lui que relit `lire_paris`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [issue(f, {v: dict(s) for v, s in barres.items()}, dict(table)) for barres, table in cas]


def issues_journees(f, racines):
    """Rend la liste des issues de `f` (la détection) sur chaque racine.

    ① RÔLE — Le contenu de `journees_d_un_autre_jour` (ou d'un mutant) sur le domaine.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `f` : la fonction · `racines` : les racines que la couche A lui passe, et la vraie.
    ④ CONDITIONS D'ENTRÉE — Les fichiers d'indice de ces racines existent encore (le dossier du domaine n'est effacé
      qu'à la fin).
    ⑤ SORTIE — UNE valeur : la liste des issues.
      [rend: 1]
    ⑥ TRAITEMENT — Un appel par racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur E2c tour 5, (2) 1 : « on compare le dictionnaire rendu, sur les fichiers d'entrée de H69
      à H74 et sur le vrai fichier de l'indice » (H75 compris).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [issue(f, r) for r in racines]


def issues_p17(f, entrees, avec_jugees=True):
    """Rend la liste des issues du juge de P17 `f` sur chaque jeu d'entrées : (fautives en multiensemble, verdict, jugées).

    ① RÔLE — Le contenu du juge de P17 (ou d'un mutant) sur le témoin et ses sabotages.
    ② CONTEXTE D'APPEL — `balayer`, `juger_p17` ; la contre-épreuve m-l (`avec_jugees` à False).
    ③ ENTRÉE — `f` : la fonction · `entrees` : la liste des jeux d'entrées de `verifier` (le témoin, puis chaque
      sabotage) · `avec_jugees` : comparer aussi le nombre de lignes jugées (False : l'issue d'avant m-l, pour la
      contre-épreuve seulement).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des issues — (« rend », (fautives triées, verdict, nombre de lignes jugées)) ou
      (« lève », type). Les DEUX sorties du juge y sont : chacune entre dans le verdict de P17 — les fautives
      directement, le nombre de lignes jugées par la règle m-k (table non vide sans ligne jugée) et par l'épreuve J17.
      [rend: 1]
    ⑥ TRAITEMENT — L'appel même de `verifier`, mêmes arguments.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur E2c tour 5, (2) 1 : « on compare `fautives` (en contenu) et le verdict ». m-l du
      relecteur E2c tour 5 (13-11-2026) : le balayage compare toute sortie qui entre dans le verdict ; l'issue qui
      laissait de côté le nombre de lignes jugées (« il n'est qu'affiché ») était périmée depuis m-k, et rangeait
      ÉQUIVALENT MESURÉ quatre mutants de ce nombre (« jugees += 2 » : 178 lignes jugées sur le vrai témoin).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sortie = []
    for x in entrees:
        if f is None:
            sortie.append(("ne se compile pas",))
            continue
        try:
            fautives, jugees = f(x["lignes"], x["journees"], x["brut_paris"], x["brut_n3_rangees"], x["source_paris"],
                                 x["prefixe_sortie"])
            sortie.append(("rend", (sorted(fautives), not fautives) + ((jugees,) if avec_jugees else ())))
        except Exception as ex:   # noqa: BLE001
            sortie.append(("lève", type(ex).__name__))
    return sortie


def juger_p17(issues, noms, cibles, comptes=None):
    """Rend la liste des épreuves que les issues d'un juge de P17 rougissent.

    ① RÔLE — Le juge « épreuves » d'un mutant de P17, tiré de ses issues.
    ② CONTEXTE D'APPEL — `balayer` ; les contre-épreuves.
    ③ ENTRÉE — `issues` : rendu de `issues_p17` sur [témoin] + sabotages · `noms`, `cibles` : les noms et les cibles des
      sabotages, dans le même ordre (cible « P17 » : P17 doit tomber ; None : elle doit tenir) · `comptes` : pour chaque
      jeu, dans le même ordre, le compte de `lignes_que_p17_doit_juger` des épreuves des 20 ans (None : l'épreuve J17
      n'est pas jouée — la contre-épreuve m-l seulement).
    ④ CONDITIONS D'ENTRÉE — Avec `comptes`, les issues portent le nombre de lignes jugées (`issues_p17` avec
      `avec_jugees`).
    ⑤ SORTIE — UNE valeur : la liste des épreuves rougies — « P17 tombe sur le témoin tel quel », « <sabotage>
      manqué », « <contre-cas> tombé à tort », « J17 <jeu> : jugées n, compte m » — ou [« exception : … »] (l'épreuve
      s'arrêterait, code 2).
      [rend: 1]
    ⑥ TRAITEMENT — Le verdict de chaque issue confronté à ce que l'épreuve attend ; puis l'épreuve J17 elle-même
      (`ecarts_de_j17` des épreuves des 20 ans, celle qu'appelle `principal`) sur le nombre de lignes jugées de chaque
      issue et le compte du même jeu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule lecture des issues pour les deux mesures (épreuves et contenu). J17 : m-l du relecteur E2c
      tour 5 (13-11-2026).
    ⑨ CE QUI CLOCHE — `principal` n'est pas appelé avec --saboter (environ quinze minutes) : le lien de J17 au code de
      sortie de `principal` est gardé par la contre-épreuve du tour 6 (juge muté `jugees += 2` → code 1), pas ici. La
      comparaison, elle, est la même fonction (E2c tour 6 ; avant, écrite deux fois — n-2 de Cowork).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    leve = [x for x in issues if x[0] != "rend"]
    if leve:
        return [f"exception : {leve[0][1] if len(leve[0]) > 1 else leve[0][0]}"]
    rouges = ["P17 tombe sur le témoin tel quel"] if not issues[0][1][1] else []
    for nom, cible, x in zip(noms, cibles, issues[1:]):
        tient = x[1][1]
        if cible and tient:
            rouges.append(f"{nom.split()[0]} manqué")
        if not cible and not tient:
            rouges.append(f"{nom.split()[0]} tombé à tort (contre-cas)")
    if comptes is not None:
        rouges += [f"J17 {x}" for x in VA.ecarts_de_j17([(nom, x[1][2], compte) for nom, x, compte
                                                         in zip(["témoin"] + list(noms), issues, comptes)])]
    return rouges


def comparer(issues_original, issues_mutant):
    """Rend (identique, nombre de cas, rang du premier écart ou None).

    ① RÔLE — La comparaison différentielle EN CONTENU.
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — Deux listes d'issues, sur les mêmes cas.
    ④ CONDITIONS D'ENTRÉE — Même longueur.
    ⑤ SORTIE — TROIS valeurs.
      [rend: 3]
    ⑥ TRAITEMENT — `==` cas par cas.
    ⑦ UNITÉ — Des cas.
    ⑧ POURQUOI — ⑧ du fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for i, (a, b) in enumerate(zip(issues_original, issues_mutant)):
        if a != b:
            return False, len(issues_original), i
    return True, len(issues_original), None


def classer(rouges, identique):
    """Range un mutant dans l'une des quatre classes.

    ① RÔLE — La règle des quatre classes (superviseur R-759 E2c tour 5, (2) 2).
    ② CONTEXTE D'APPEL — `balayer`.
    ③ ENTRÉE — `rouges` : les épreuves que le mutant rougit · `identique` : son contenu est-il celui de l'original sur
      tout le domaine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : TUE, SURVIVANT, EQUIVALENT ou SUR_SPECIFIE.
      [rend: 1]
    ⑥ TRAITEMENT — Le tableau à double entrée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve doit tomber exactement quand le contrat est violé : le balayage du tour 4 ne mesurait que
      le sens « trop faible ».
    ⑨ CE QUI CLOCHE — « Contenu identique » ne vaut que sur le domaine (⑨ du fichier).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if rouges:
        return SUR_SPECIFIE if identique else TUE
    return EQUIVALENT if identique else SURVIVANT


def balayer(racine, complet):
    """Le balayage entier ; rend le code de sortie.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `racine` : le dépôt · `complet` : rejouer contre toutes les épreuves les mutants de K que la couche A
      laisse verts.
    ④ CONDITIONS D'ENTRÉE — ④ du fichier.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ du fichier).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — ⑧ du fichier.
    ⑨ CE QUI CLOCHE — ⑨ du fichier.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.chdir(racine)
    sys.argv = [sys.argv[0], racine]          # les épreuves de l'historique long lisent leur racine ici
    global HL
    hl = HL = charger_module(os.path.join(racine, EPREUVES_HL), "epreuves_hl")
    global VA
    va = VA = charger_module(os.path.join(racine, EPREUVES_VA), "epreuves_va")
    total = 0
    classes = {TUE: [], SURVIVANT: [], EQUIVALENT: [], SUR_SPECIFIE: []}
    # ① le domaine de K : les entrées que la couche A passe vraiment aux deux fonctions, espionnées sur K tel quel
    k_tel_quel, _ = hl.charger()
    vraies = {nom: getattr(k_tel_quel, nom) for nom in FONCTIONS_K}
    vues = {nom: [] for nom in FONCTIONS_K}

    def espion_journees(r):
        vues["journees_d_un_autre_jour"].append(r)
        return vraies["journees_d_un_autre_jour"](r)

    def espion_redater(barres, journees):
        vues["redater_les_journees"].append(({v: dict(s) for v, s in barres.items()}, dict(journees)))
        return vraies["redater_les_journees"](barres, journees)
    k_tel_quel.journees_d_un_autre_jour, k_tel_quel.redater_les_journees = espion_journees, espion_redater
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            r_tel_quel = hl.epreuves_des_journees(k_tel_quel)
    finally:
        for nom, f in vraies.items():
            setattr(k_tel_quel, nom, f)
    if not all(r_tel_quel.values()):
        print(f"ARRÊT — la couche A n'est pas verte sur K tel quel : {sorted(k for k, v in r_tel_quel.items() if not v)}")
        return 2
    # O-a de Cowork (E2c tour 5) : les racines dans l'ordre de leur PREMIER APPEL par la couche A (déterministe), et non
    # triées par leur chemin, tiré au hasard à chaque passage — le rang du premier cas différent se compare alors
    racines = list(dict.fromkeys(vues["journees_d_un_autre_jour"] + [racine]))
    domaines = {"journees_d_un_autre_jour": (lambda f: issues_journees(f, racines)),
                "redater_les_journees": (lambda f, c=cas_de_redater(vues["redater_les_journees"]): issues_redater(f, c))}
    print(f"DOMAINE journees_d_un_autre_jour : {len(racines)} racines (le vrai indice et les fichiers de H69 à H75)")
    print(f"DOMAINE redater_les_journees : {len(cas_de_redater(vues['redater_les_journees']))} appels "
          f"(625 tables × 33, plus {len(vues['redater_les_journees'])} entrées des épreuves)")
    # L'ORACLE (superviseur R-759 E2c tour 6, (2) 1) : la sortie de l'original doit être celle de `attendu_de_redater`
    # sur tout le domaine — la référence de la comparaison différentielle est alors aussi celle de H73
    cas_r = cas_de_redater(vues["redater_les_journees"])
    oracle = [(o[0], o[1], (o[2], dict(t))) for o, t in ((hl.attendu_de_redater(b, t), t) for b, t in cas_r)]
    id_o, n_o, e_o = comparer(oracle, domaines["redater_les_journees"](vraies["redater_les_journees"]))
    print(f"ORACLE attendu_de_redater contre redater_les_journees telle quelle : identique {id_o} sur {n_o} cas")
    if not id_o:
        print(f"ARRÊT — l'original s'écarte de l'oracle (cas {e_o}) : H73 ne peut pas être verte, le balayage s'arrête")
        return 2
    constantes_k = {n for n, v in vars(k_tel_quel).items() if n.isupper() and type(v) in (int, float)}
    lignes_du_bilan = []
    # ② K, couche A et contenu
    for nom in FONCTIONS_K:
        texte, f = lire_fonction(os.path.join(racine, CONTROLE), nom)
        reference = domaines[nom](vraies[nom])
        zero = ast.unparse(f)
        r0 = juger_k(hl, texte, zero)
        id0, n0, _ = comparer(reference, domaines[nom](fonction_de(zero, nom, vars(k_tel_quel))))
        print(f"MUTANT ZÉRO {nom} (réécrit sans mutation) : rouges {r0} · contenu identique {id0} sur {n0} cas")
        if r0 or not id0:
            print("ARRÊT — le mutant zéro n'est pas vert, ou pas identique : le balayage mesurerait la réécriture")
            return 2
        for ligne, quoi, fm in mutations(f, constantes_k):
            total += 1
            texte_m = ast.unparse(fm)
            rouges = juger_k(hl, texte, texte_m)
            if not rouges and complet:
                rouges = [f"(hors couche A) {x}" for x in juger_k_complet(hl, texte, texte_m)]
            identique, n, ecart = comparer(reference, domaines[nom](fonction_de(texte_m, nom, vars(k_tel_quel))))
            classe = classer(rouges, identique)
            classes[classe].append((nom, ligne, quoi, rouges, n))
            print(f"M{total} {nom} l.{ligne} {quoi} → {classe} · épreuves {rouges} · contenu "
                  + (f"identique sur {n} cas" if identique else f"différent (cas {ecart} sur {n})"))
    # ③ P17, en mémoire : le témoin et ses sabotages
    pris = {}
    garde = va.verifier

    def espion(e):
        pris.setdefault("e", e)
        return garde(e)
    va.verifier = espion
    try:
        with contextlib.redirect_stdout(io.StringIO()) as sortie:
            code = va.principal([racine])
    finally:
        va.verifier = garde
    if "e" not in pris or code != 0:
        print(f"ARRÊT — l'épreuve des 20 ans n'a pas tourné sur le témoin tel quel (code {code}) : "
              + " · ".join(sortie.getvalue().splitlines()[-3:]))
        return 2
    e = pris["e"]
    sabotages, arret = va.sabotages_de_p17(e)
    if arret:
        print(arret)
        return 2
    noms = list(sabotages)
    cibles = [sabotages[n][0] for n in noms]
    entrees = [e] + [sabotages[n][1] for n in noms]
    comptes = [va.lignes_que_p17_doit_juger(x) for x in entrees]     # J17 (m-l) : le compte calculé par l'épreuve
    print(f"P17 : sabotages joués contre chaque mutant : {[n.split()[0] for n in noms]}")
    texte, f = lire_fonction(os.path.join(racine, EPREUVES_VA), FONCTION_P17)
    reference = issues_p17(va.journees_hors_de_leur_fichier, entrees)
    zero = issues_p17(fonction_de(ast.unparse(f), FONCTION_P17, vars(va)), entrees)
    r0 = juger_p17(zero, noms, cibles, comptes)
    id0, n0, _ = comparer(reference, zero)
    print(f"MUTANT ZÉRO {FONCTION_P17} (réécrit sans mutation) : rouges {r0} · contenu identique {id0} sur {n0} cas")
    if r0 or not id0:
        print("ARRÊT — le mutant zéro n'est pas vert, ou pas identique : le balayage mesurerait la réécriture")
        return 2
    constantes_va = {n for n, v in vars(va).items() if n.isupper() and type(v) in (int, float)}
    reference_sans = issues_p17(va.journees_hors_de_leur_fichier, entrees, avec_jugees=False)
    sans_jugees = []      # contre-épreuve m-l : chaque mutant de P17 rangé aussi par l'issue et les épreuves d'avant m-l
    for ligne, quoi, fm in mutations(f, constantes_va):
        total += 1
        issues_m = issues_p17(fonction_de(ast.unparse(fm), FONCTION_P17, vars(va)), entrees)
        rouges = juger_p17(issues_m, noms, cibles, comptes)
        identique, n, ecart = comparer(reference, issues_m)
        classe = classer(rouges, identique)
        classes[classe].append((FONCTION_P17, ligne, quoi, rouges, n))
        issues_s = issues_p17(fonction_de(ast.unparse(fm), FONCTION_P17, vars(va)), entrees, avec_jugees=False)
        sans_jugees.append((f"M{total}", ligne, quoi, classe, classer(juger_p17(issues_s, noms, cibles),
                                                                       comparer(reference_sans, issues_s)[0])))
        print(f"M{total} {FONCTION_P17} l.{ligne} {quoi} → {classe} · épreuves {rouges} · contenu "
              + (f"identique sur {n} cas" if identique else f"différent (cas {ecart} sur {n})"))
    # ④ les contre-épreuves
    dents = True

    def p17_texte(t):
        return juger_p17(issues_p17(fonction_de(t, FONCTION_P17, vars(va)), entrees), noms, cibles, comptes)
    # S28 (superviseur E2c tour 4, (1) 2), sous ses deux lectures
    for titre, avant, apres in (("`brut is None or` retiré tel quel", "if brut is None or [float(x)", "if [float(x)"),
                                ("branche retirée en gardant la lecture (`brut is not None and`)",
                                 "if brut is None or [float(x)", "if brut is not None and [float(x)")):
        if texte.count(avant) != 1:
            print(f"ARRÊT — contre-épreuve de S28 ({titre}) : texte cible absent de P17")
            return 2
        print(f"CONTRE-ÉPREUVE S28 — P17, {titre} : rougi par {p17_texte(texte.replace(avant, apres))}")
    # m-i : le juge comparant quatre champs (Q1), ou la seule clôture (Q2) — les sabotages S32 à S36 doivent manquer
    # exactement les champs oubliés
    champs = {"S32": "ouverture", "S33": "plus haut", "S34": "plus bas", "S35": "clôture", "S36": "volume"}
    cible_q = "[float(x) for x in l[2:7]] != [float(x) for x in brut]"
    for titre, apres, oublies in (("Q1 quatre champs (`l[2:6]`)", "[float(x) for x in l[2:6]] != [float(x) for x in brut[:4]]",
                                   ["S36"]),
                                  ("Q2 la seule clôture", "float(l[5]) != float(brut[3])", ["S32", "S33", "S34", "S36"])):
        if texte.count(cible_q) != 1:
            print(f"ARRÊT — contre-épreuve m-i ({titre}) : texte cible absent de P17")
            return 2
        r = p17_texte(texte.replace(cible_q, apres))
        manques = sorted(x.split()[0] for x in r if x.endswith("manqué") and x.split()[0] in champs)
        bon = manques == oublies and len(r) == len(manques)
        dents &= bon
        print(f"CONTRE-ÉPREUVE m-i — P17, {titre} : rougi par {r} · attendu les seuls champs oubliés {oublies} : "
              f"{'OUI' if bon else 'NON — S32 à S36 sans dents'}")
    # m-j : la lecture des lignes brutes revenue à « la dernière gagne » — S37 et S38 doivent être manqués, et eux seuls
    garde_r = va.ranger_les_lignes_brutes
    va.ranger_les_lignes_brutes = lambda paires: dict(paires)
    try:
        sab_j, arret_j = va.sabotages_de_p17(e)
    finally:
        va.ranger_les_lignes_brutes = garde_r
    if arret_j:
        print(arret_j)
        return 2
    noms_j = list(sab_j)
    entrees_j = [e] + [sab_j[n][1] for n in noms_j]
    r = juger_p17(issues_p17(va.journees_hors_de_leur_fichier, entrees_j), noms_j,
                  [sab_j[n][0] for n in noms_j], [va.lignes_que_p17_doit_juger(x) for x in entrees_j])
    bon = sorted(x.split()[0] for x in r) == ["S37", "S38"] and all(x.endswith("manqué") for x in r)
    dents &= bon
    print(f"CONTRE-ÉPREUVE m-j — lignes brutes rangées « la dernière gagne » : rougi par {r} · attendu S37 et S38 "
          f"manqués, eux seuls : {'OUI' if bon else 'NON — S37 et S38 sans dents'}")
    # D-6 : la réécriture de `redater_les_journees` en vraie permutation (preuve 1 du relecteur E2c tour 4) — un
    # sabotage CONTRE LA CORRECTION, affiché, pas une garde (superviseur E2c tour 5, (2), rustines refusées)
    texte_r, _ = lire_fonction(os.path.join(racine, CONTROLE), "redater_les_journees")
    debut_corps = texte_r.index("    bouge = []\n")
    permutation = (texte_r[:debut_corps] + "    bouge = sorted((v, j, journees[j]) for v, s in barres.items() for j in s "
                   "if j in journees)\n    for v, s in barres.items():\n        barres[v] = dict(sorted((journees.get(x, x), y) "
                   "for x, y in s.items()))\n    return bouge\n")
    id_p, n_p, _ = comparer(domaines["redater_les_journees"](vraies["redater_les_journees"]),
                            domaines["redater_les_journees"](fonction_de(permutation, "redater_les_journees",
                                                                         vars(k_tel_quel))))
    print(f"CONTRE-ÉPREUVE D-6 — redater_les_journees réécrite en vraie permutation : contenu identique {id_p} sur "
          f"{n_p} cas · épreuves rouges {juger_k(hl, texte_r, permutation)} (attendu [] sous la H73 des tours 5 et 6, "
          f"['H73'] sous celle du tour 4)")
    # m-l (relecteur E2c tour 5) : rangés par l'issue d'avant m-l (sans le nombre de lignes jugées) et sans l'épreuve
    # J17, les mutants qui ne touchent que ce nombre doivent retomber en ÉQUIVALENT MESURÉ — sinon la réparation ne
    # mesure rien de plus que l'ancienne issue. PROPRIÉTÉ : au moins un mutant bascule, chaque basculé est TUÉ avec la
    # réparation, et aucun autre mutant de P17 ne change de classe
    bascules = [(m, l, q, c) for m, l, q, c, avant in sans_jugees if avant == EQUIVALENT and c != EQUIVALENT]
    autres = [(m, c, avant) for m, l, q, c, avant in sans_jugees
              if not (avant == EQUIVALENT and c != EQUIVALENT) and c != avant]
    bon = bool(bascules) and all(c == TUE for _, _, _, c in bascules) and not autres
    dents &= bon
    for m, l, q, c in bascules:
        print(f"CONTRE-ÉPREUVE m-l — {m} {FONCTION_P17} l.{l} {q} : sans le nombre de lignes jugées ni J17 → "
              f"{EQUIVALENT} · avec → {c}")
    print(f"CONTRE-ÉPREUVE m-l — issue d'avant m-l : {len(bascules)} mutant(s) retombent en {EQUIVALENT}, "
          f"autres changements de classe {autres} : {'OUI' if bon else 'NON — la comparaison des lignes jugées ne mesure rien'}")
    # ⑤ les preuves écrites
    vus, arret_eq = set(), None
    for nom, ligne, quoi, rouges, n in classes[EQUIVALENT]:
        if (nom, quoi) in EQUIVALENTS:
            preuve, rejouer = EQUIVALENTS[(nom, quoi)]
            if not rejouer(k_tel_quel):
                print(f"ARRÊT — la preuve écrite de {(nom, quoi)} ne se rejoue pas")
                return 2
            print(f"PREUVE ÉCRITE {nom} l.{ligne} {quoi} — rejouée ({rejouer.__name__}) : {preuve}")
            vus.add((nom, quoi))
    perimes = [k for k in EQUIVALENTS if k not in vus]
    if perimes:
        print(f"ARRÊT — preuves écrites qui ne visent aucun ÉQUIVALENT MESURÉ : {perimes}")
        return 2
    for classe in (TUE, EQUIVALENT, SURVIVANT, SUR_SPECIFIE):
        print(f"CLASSE {classe} : {len(classes[classe])}")
        if classe in (SURVIVANT, SUR_SPECIFIE):
            for nom, ligne, quoi, rouges, n in classes[classe]:
                print(f"   {classe} {nom} l.{ligne} {quoi} · épreuves {rouges}")
    print(f"ÉQUIVALENTS MESURÉS dont la preuve écrite va au-delà du domaine : {len(vus)} · mesurés sur le domaine seul : "
          f"{len(classes[EQUIVALENT]) - len(vus)}")
    sur = sorted({x for c in classes[SUR_SPECIFIE] for x in c[3]})
    print(f"BILAN : {total} mutants · tués {len(classes[TUE])} · équivalents mesurés {len(classes[EQUIVALENT])} · "
          f"survivants {len(classes[SURVIVANT])} · épreuves qui sur-spécifient {len(classes[SUR_SPECIFIE])} {sur} · "
          f"contre-épreuves de dents (m-i, m-j, m-l) {'tenues' if dents else 'NON TENUES'}")
    return 1 if classes[SURVIVANT] or classes[SUR_SPECIFIE] or not dents else 0


if __name__ == "__main__":
    _args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(_args) != 1 or not os.path.isdir(_args[0]):
        print("USAGE : BALAYER_LES_MUTANTS_DES_JOURNEES.py <racine> [--complet]")
        sys.exit(2)
    _d = tempfile.mkdtemp(prefix="balayage_")
    tempfile.tempdir = os.environ["TMPDIR"] = _d
    try:
        sys.exit(balayer(os.path.abspath(_args[0]), "--complet" in sys.argv))
    except Exception as _x:   # noqa: BLE001 — R-734 : un balayage qui n'a pas pu tourner rend le code 2
        print(f"ARRÊT — le balayage n'a pas pu tourner : {type(_x).__name__} : {_x}")
        sys.exit(2)
    finally:
        shutil.rmtree(_d, ignore_errors=True)
