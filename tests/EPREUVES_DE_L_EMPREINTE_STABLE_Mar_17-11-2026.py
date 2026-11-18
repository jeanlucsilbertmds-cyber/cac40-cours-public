#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_EMPREINTE_STABLE — Mar 17-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. L'empreinte du code (`emp.empreinte`, à la racine du dépôt) doit reconnaître le MÊME code sous toutes
les versions de Python. Décision de Jean-Luc du 17-11-2026 à 07h46 (A-872, « 1 », option « Oui, on change la
définition une fois pour toutes ») : la définition change une fois, avec une forme stable entre versions, à un seul
endroit (emp.py), et une étiquette de format. Fait mesuré par le superviseur R-759 le 17-11-2026 à 00h18 (A-871) :
l'ancienne forme (le hachage de `ast.dump`) donnait pour C5E10-QA-V1 6f4658b2… en 3.11, 571fac04… en 3.12, d622c74a…
en 3.13. Cette épreuve lance UN sous-processus par Python installé ; chacun calcule l'empreinte de emp.py et de tous
les programmes et épreuves (programmes/*.py, tests/**/*.py) et joue les propriétés ; puis elle compare. Elle vérifie
aussi qu'AUCUN AUTRE ENDROIT du code vivant (racine, programmes/, tests/) ne calcule une empreinte de code (superviseur
R-759 du 17-11-2026) : une seconde définition divergerait (R-708). DEPUIS LE 17-11-2026 AU SOIR (E1 du superviseur
R-759, sur MAJ-1 du relecteur : trois affaiblissements d'emp.py — format des f-strings, `a.b`/`a.c`, valeurs par défaut
— laissaient l'épreuve VERTE) : la sensibilité est une PROPRIÉTÉ PAR MUTATION sur les 202 fichiers, sans échantillon
et sans aucun nom de champ écrit, plus un CONTRÔLE DE COMPOSITION au niveau d'`empreinte` (une mutation par fichier).
Avec « --saboter », elle écrit chaque sabotage dans une copie légère (emp.py, programmes/, tests/) et exige que chacun
la fasse rougir, sous un seul Python, la mutation arrêtée au premier champ aveugle.

① RÔLE — Rougir si deux versions de Python rendent une empreinte différente pour un même fichier, ou si une propriété
  de la définition tombe sous l'une d'elles.
② CONTEXTE D'APPEL — À la main, par le Chat ou un agent ; `python3 tests/EPREUVES_DE_L_EMPREINTE_STABLE_Mar_17-11-2026.py
  [racine]`.
③ ENTRÉE — La ligne de commande : la racine du dépôt (facultative ; par défaut, le dossier parent de tests/) ;
  « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte emp.py, programmes/ (dont le fabricant, qui porte VERSION_DE_PYTHON et
  VERSIONS_COMPAREES) et tests/. python3.11 et python3.13 dans le PATH : EXIGÉS (A-891), cherchés sous leur nom en
  clair ; d'autres versions, facultatives, sont comparées en plus (`pythons_installes`).
⑤ SORTIE — Le code de sortie : 0 si tout concorde, toutes les propriétés tiennent sous chaque Python, aucun autre
  endroit ne calcule d'empreinte de code et, avec --saboter, chaque sabotage mord ; 1 sinon ; 2 si l'épreuve n'a pas
  pu tourner — un Python exigé absent ou des noms exigés qui divergent des constantes du fabricant, un sous-processus sans réponse lisible, le motif de recherche qui
  échoue à son calibrage, ou un sabotage dont le texte n'est pas trouvé (R-734 : un contrôle qui n'a pas pu tourner
  ne rend jamais 0).
  [rend: 1]
⑥ TRAITEMENT — ① chercher les Python installés, un par version mineure · ② pour chacun, un sous-processus isolé (-I -B)
  qui importe emp.py de la racine et rend en JSON : la version, l'étiquette, l'empreinte de chaque fichier, le résultat
  de chaque propriété — dont la MUTATION LOCALE (chaque nœud de chaque fichier, chaque champ non vide d'`ast.iter_fields`
  hors `Constant.kind` : valeur changée, `emp._forme(nœud)` doit changer ; une liste : longueur changée ET deux
  éléments distincts permutés) et la COMPOSITION (par fichier, la première instruction d'un corps qui n'est pas un
  texte explicatif remplacée : `emp.empreinte` du texte doit changer), avec comptes et durées · ③ comparer fichier par
  fichier ; imprimer les écarts et les propriétés fausses · ④ chercher les autres définitions (`autres_definitions`),
  motif calibré d'abord · ⑤ sous --saboter, rejouer ② à ④ sur une copie sabotée, sous le premier Python seul, pour
  chaque sabotage de SABOTAGES.
⑦ UNITÉ — Des empreintes (seize caractères hexadécimaux) ; des secondes (DELAI, par sous-processus ; durées
  imprimées). Mesuré le 17-11-2026 sur la machine du Chat : environ 19 s de mutation (998 195 mutations, 119 couples
  nœud.champ) et 6 s de composition par version ; environ 90 s l'épreuve simple sous trois versions.
⑧ POURQUOI — A-871 : GitHub (3.11) et la machine du Chat (3.13) ne reconnaissaient pas le même code ; jeton_d_essai,
  le tri, le registre des essais et les déclarations comparent des empreintes calculées sur des machines différentes.
  Une seule mesure le prouve : calculer partout et comparer.
⑨ CE QUI CLOCHE — ① Seules les versions INSTALLÉES sont éprouvées : Python 3.14 N'A JAMAIS ÉTÉ ÉPROUVÉ sur la machine
  du Chat (absent au 17-11-2026) et peut changer l'arbre ; sur GitHub, où elle est le Python du système (A-893), elle
  est prise EN PLUS et comparée : voir `pythons_installes`, ⑨. ② Les propriétés sont jouées sur de petits textes écrits ici, pas
  sur tous les programmes. Les propriétés de SENSIBILITÉ (is/==, ordre des arguments, 4/4.0, ajoutées après M1 du
  relecteur neuf du 17-11-2026) ne couvrent pas tout changement de code : « return » contre « return None », « x[a:] »
  contre « x[:a] » ne sont pas des propriétés (le relecteur les a mesurés DIFFÉRENTS à la main, 3.11/3.12/3.13).
  DEPUIS E1 (superviseur R-759 du 17-11-2026), la sensibilité générale est portée par la MUTATION, sur les vrais
  fichiers. Ce qu'elle NE couvre PAS : ⓐ la mutation « vide → non vide » (un champ None ou [] qui prendrait une
  valeur) n'est pas jouée localement, car emp.py SAUTE les champs vides ; elle est couverte en pratique (une valeur
  ajoutée apparaît dans la forme comme un champ de plus, ce que la composition et les propriétés voient sur leurs
  cas), pas prouvée champ par champ · ⓑ la mutation est LOCALE (`_forme` du nœud) : ce qui se perd entre `_forme` et
  le hachage est vu par la COMPOSITION, qui n'est qu'un ÉCHANTILLON d'une mutation par fichier · ⓒ seule
  `Constant.kind` est exclue, exprès (graphie u"…", voir emp.py ⑧) · ⓓ une valeur d'un type non prévu par `_autre`
  est comptée « non prévue » et fait rougir, elle n'est pas sautée · ⓔ sous --saboter, un seul Python (le plus
  ancien trouvé) : voir `main`, ⑨. ③ Le témoin de l'ancienne forme (`ANCIENNE_FORME_V1`) est une RECOPIE de l'ancienne
  définition, gardée comme pièce historique pour prouver qu'une empreinte v1 ne se confond pas avec une v2 ; elle ne
  sert à rien d'autre. ④ Un fichier qui ne s'analyse pas sous une version est rendu « NON ANALYSABLE » et compte comme
  un écart. ⑤ Le motif des autres définitions lit l'ARBRE du code : une définition écrite dans une chaîne exécutée
  plus tard (comme ENFANT ici, ou ANCIENNE_FORME_V1) ne se voit pas ; une définition qui passerait l'arbre par une
  autre fonction avant de le hacher non plus.
⑩ EFFET — Lance des processus ; sous --saboter, écrit puis efface une copie légère dans un dossier temporaire.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Chaque sous-processus est borné à DELAI.
  [sort: oui]
"""
import ast
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

DELAI = 300

# CE QUE CHAQUE SOUS-PROCESSUS EXÉCUTE : il importe emp.py de la racine, calcule, joue les propriétés, rend du JSON.
ENFANT = r'''
import ast, glob, hashlib, json, math, os, sys, time
racine = sys.argv[1]
premier = "--premier" in sys.argv[2:]
sys.path.insert(0, racine)
import emp

# L'ANCIENNE FORME (v1), recopiée comme pièce historique : sert seulement à prouver qu'une v1 ne passe pas pour une v2.
def ANCIENNE_FORME_V1(src):
    a = ast.parse(src)
    for n in ast.walk(a):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if (n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)
                    and isinstance(n.body[0].value.value, str)):
                n.body = n.body[1:]
    return hashlib.sha256(ast.dump(a).encode()).hexdigest()[:16]

fichiers = sorted(set([os.path.join(racine, "emp.py")]
                      + glob.glob(os.path.join(racine, "programmes", "*.py"))
                      + glob.glob(os.path.join(racine, "tests", "**", "*.py"), recursive=True)))
empreintes, v1_egales = {}, []
for f in fichiers:
    rel = os.path.relpath(f, racine)
    try:
        src = open(f, encoding="utf-8").read()
        e = emp.empreinte(src)
        empreintes[rel] = e
        if e == ANCIENNE_FORME_V1(src):
            v1_egales.append(rel)
    except (SyntaxError, ValueError, UnicodeDecodeError) as x:
        empreintes[rel] = "NON ANALYSABLE : %s" % type(x).__name__

BASE = 'def f(x):\n    """Texte explicatif."""\n    y = x + 1\n    return y\n'
def E(s):
    return emp.empreinte(s)
proprietes = {}
proprietes["commentaire_sans_effet"] = E(BASE) == E(BASE.replace("    y = x + 1\n", "    # un commentaire\n    y = x + 1  # et un autre\n\n"))
proprietes["texte_explicatif_modifie_sans_effet"] = E(BASE) == E(BASE.replace("Texte explicatif.", "Un tout autre texte, plus long."))
proprietes["texte_explicatif_retire_sans_effet"] = E(BASE) == E(BASE.replace('    """Texte explicatif."""\n', ""))
proprietes["ligne_de_code_ajoutee_change"] = E(BASE) != E(BASE.replace("    return y\n", "    y = y * 2\n    return y\n"))
proprietes["1.0_contre_1_change"] = E("x = 1\n") != E("x = 1.0\n")
proprietes["-0.0_contre_0.0_change"] = E("x = 0.0\n") != E("x = -0.0\n")
proprietes["True_contre_1_change"] = E("x = True\n") != E("x = 1\n")
proprietes["prefixe_u_sans_effet"] = E('x = u"a"\n') == E('x = "a"\n')
# LA SENSIBILITÉ (M1 du relecteur neuf du 17-11-2026) : emp.py promet en ① « change si, et seulement si, le CODE
# change » ; ces trois propriétés gardent le « si ». Cas réels du relecteur sur MODULE_C5_ETENDU_10 : « if px_out is
# None » contre « == None », « min(i_in + C5E10_HORIZON, n - 1) » contre « min(n - 1, …) », « round(px_in, 4) » contre
# « round(px_in, 4.0) ».
proprietes["is_contre_egal_change"] = E("a = x is None\n") != E("a = x == None\n")
proprietes["ordre_des_arguments_change"] = E("m = min(a + b, n - 1)\n") != E("m = min(n - 1, a + b)\n")
proprietes["4_contre_4.0_change"] = E("p = round(x, 4)\n") != E("p = round(x, 4.0)\n")
proprietes["chaine_en_fonction_non_premiere_compte"] = E(BASE) != E(BASE.replace("    return y\n", "    'pas un texte explicatif'\n    return y\n"))
# L'ÉTIQUETTE EST DANS LE TEXTE HACHÉ : changer emp.FORMAT doit changer l'empreinte.
fmt = getattr(emp, "FORMAT", None)
proprietes["etiquette_emp-v2_declaree"] = fmt == "emp-v2"
if isinstance(fmt, str):
    avant = E(BASE)
    emp.FORMAT = "emp-v1"
    try:
        proprietes["etiquette_dans_le_texte_hache"] = E(BASE) != avant
    finally:
        emp.FORMAT = fmt
else:
    proprietes["etiquette_dans_le_texte_hache"] = False
proprietes["aucune_v1_prise_pour_une_v2"] = not v1_egales and E(BASE) != ANCIENNE_FORME_V1(BASE)
# LE BOM (E2 du superviseur R-759 du 17-11-2026, MIN-1 du relecteur) : avec ou sans BOM en tête, même empreinte.
try:
    proprietes["bom_sans_effet"] = E("x = 1\n") == E("\ufeffx = 1\n") and E(BASE) == E("\ufeff" + BASE)
except SyntaxError:
    proprietes["bom_sans_effet"] = False

# LA SENSIBILITÉ PAR MUTATION (E1 du superviseur R-759 du 17-11-2026, sur MAJ-1 du relecteur) : sur CHAQUE fichier,
# CHAQUE nœud, CHAQUE champ non vide pris par `ast.iter_fields` (aucun nom de champ écrit ici), on change la valeur du
# champ et on exige que `emp._forme(nœud)` change. Mutation LOCALE : la forme du nœud, pas l'empreinte du fichier
# (coût quadratique sinon). Les positions (lineno…) sont dans `_attributes`, hors des champs : elles ne sont pas
# mutées. SEULE EXCLUSION : `Constant.kind` — il vaut « u » pour u"…" et None sinon, c'est une graphie et emp.py le
# saute exprès (⑧ d'emp.py ; propriété prefixe_u_sans_effet). Une liste reçoit DEUX mutations : sa longueur changée
# (dernier élément retiré) ET deux éléments de formes différentes permutés (sans la permutation, des listes TRIÉES
# passeraient : sabotage S6).
_RIEN = object()


def _autre(v):
    if isinstance(v, ast.AST):
        return ast.Pass() if type(v) is not ast.Pass else ast.Break()
    if isinstance(v, bool):
        return not v
    if isinstance(v, (int, float, complex)):
        w = v + 1
        return w if w != v and not (isinstance(v, float) and math.isnan(v)) else 0
    if isinstance(v, str):
        return v + "_m"
    if isinstance(v, bytes):
        return v + b"_m"
    if v is Ellipsis:
        return 0
    return _RIEN


def _mutations(v):
    if isinstance(v, list):
        yield v[:-1]
        formes = [emp._forme(e) for e in v]
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                if formes[i] != formes[j]:
                    w = list(v)
                    w[i], w[j] = w[j], w[i]
                    yield w
                    return
        return
    yield _autre(v)


debut = time.time()
mutations, aveugles, inconnus, par_champ = 0, [], [], set()
for f in fichiers:
    rel = os.path.relpath(f, racine)
    try:
        arbre = ast.parse(open(f, encoding="utf-8").read())
    except (SyntaxError, ValueError, UnicodeDecodeError):
        continue
    for n in ast.walk(arbre):
        avant = None
        for nom, val in list(ast.iter_fields(n)):
            if val is None or (isinstance(val, list) and not val):
                continue
            if isinstance(n, ast.Constant) and nom == "kind":
                continue
            if avant is None:
                avant = emp._forme(n)
            for m in _mutations(val):
                if m is _RIEN:
                    inconnus.append("%s.%s : type %s" % (type(n).__name__, nom, type(val).__name__))
                    continue
                setattr(n, nom, m)
                try:
                    apres = emp._forme(n)
                finally:
                    setattr(n, nom, val)
                mutations += 1
                par_champ.add("%s.%s" % (type(n).__name__, nom))
                if apres == avant:
                    aveugles.append("%s.%s (%s:%s)" % (type(n).__name__, nom, rel, getattr(n, "lineno", "?")))
            if premier and aveugles:
                break
        if premier and aveugles:
            break
    if premier and aveugles:
        break
duree_mutation = time.time() - debut
proprietes["mutation_locale_aucun_champ_aveugle"] = mutations > 0 and not aveugles and not inconnus

# LE CONTRÔLE DE COMPOSITION (E1, point 2) : la mutation locale prouve `_forme` ; ceci prouve qu'`empreinte` la
# transmet. Pour chaque fichier : le premier corps (champ qui est une liste d'instructions, ordre de `ast.walk`) dont la
# première instruction n'est pas une chaîne seule (un texte explicatif, retiré par emp.py) ; cette instruction est
# remplacée par `pass` (par `0` si c'est déjà `pass`) ; l'empreinte du texte réécrit (`ast.unparse`) doit différer de
# celle du texte d'origine réécrit de même. Un fichier dont CHAQUE corps commence par un texte explicatif (cas réel :
# tests/HORLOGE_D_EPREUVE.py) : la DEUXIÈME instruction du premier corps qui en a deux. UN ÉCHANTILLON : une mutation
# par fichier.
debut = time.time()
compo_vues, compo_aveugles, compo_sans_instruction = 0, [], []
for f in fichiers:
    rel = os.path.relpath(f, racine)
    try:
        arbre = ast.parse(open(f, encoding="utf-8").read())
    except (SyntaxError, ValueError, UnicodeDecodeError):
        continue
    corps, rang, repli = None, 0, None
    for n in ast.walk(arbre):
        for _nom, val in ast.iter_fields(n):
            if isinstance(val, list) and val and all(isinstance(e, ast.stmt) for e in val):
                s0 = val[0]
                if not (isinstance(s0, ast.Expr) and isinstance(s0.value, ast.Constant)
                        and isinstance(s0.value.value, str)):
                    corps = val
                    break
                if repli is None and len(val) > 1:
                    repli = val
        if corps is not None:
            break
    if corps is None and repli is not None:
        corps, rang = repli, 1
    if corps is None:
        compo_sans_instruction.append(rel)
        continue
    origine = ast.unparse(arbre)
    corps[rang] = ast.Pass() if type(corps[rang]) is not ast.Pass else ast.Expr(ast.Constant(0))
    compo_vues += 1
    if emp.empreinte(ast.unparse(arbre)) == emp.empreinte(origine):
        compo_aveugles.append(rel)
duree_composition = time.time() - debut
# Un fichier sans AUCUNE instruction hors textes explicatifs n'a rien à muter : il est nommé dans la sortie, pas compté
# comme une faute (aucun au 17-11-2026).
proprietes["composition_chaque_fichier_change"] = compo_vues > 0 and not compo_aveugles
print(json.dumps({"version": "%d.%d.%d" % sys.version_info[:3], "format": fmt, "empreintes": empreintes,
                  "proprietes": proprietes, "v1_egales": v1_egales,
                  "mutation": {"mutations": mutations, "aveugles": aveugles[:5], "nb_aveugles": len(aveugles),
                               "inconnus": inconnus[:5], "champs": len(par_champ), "secondes": round(duree_mutation, 1),
                               "arret_au_premier": premier},
                  "composition": {"vues": compo_vues, "aveugles": compo_aveugles[:5], "nb_aveugles": len(compo_aveugles),
                                  "sans_instruction": compo_sans_instruction, "secondes": round(duree_composition, 1)}}))
'''


# LES PYTHON EXIGÉS, ÉCRITS EN CLAIR (A-891, décision de Jean-Luc du 17-11-2026 à 23h09) : l'épreuve E6 du circuit public
# (tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py) exige que tout logiciel cherché par shutil.which soit nommé en
# clair, pour vérifier que la certification le pose (« command -v »). 3.11 : la version qui exécute le code dans chaque
# circuit (VERSION_DE_PYTHON du fabricant) ; 3.13 : la version de la machine du Chat (VERSIONS_COMPAREES du fabricant).
# `pythons_installes` confronte ces deux noms aux constantes du fabricant (R-708 : deux écritures divergent toujours).
FABRICANT = os.path.join("programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py")


def constantes_du_fabricant(racine):
    """Rend les versions que le fabricant pose. ① RÔLE — Lire VERSION_DE_PYTHON et VERSIONS_COMPAREES sans importer le
    fabricant. ② CONTEXTE D'APPEL — `pythons_installes`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE —
    DEUX valeurs : la version exécutante (texte « 3.N ») et les versions comparées (tuple), ou None et None si le
    fabricant est absent, illisible, ou si une constante n'est pas un littéral de la forme attendue. [rend: 2]
    ⑥ TRAITEMENT — Analyse l'arbre du fabricant ; prend la première affectation de niveau module de chaque nom, par
    `ast.literal_eval`. ⑦ UNITÉ — —. ⑧ POURQUOI — Importer le fabricant exécuterait son code de tête (lecture de la
    table des épreuves) dans une épreuve qui ne le demande pas ; la constante est un littéral, l'arbre suffit.
    ⑨ CE QUI CLOCHE — Une constante calculée (non littérale) rend None : l'épreuve rend alors 2, elle ne devine pas.
    ⑩ EFFET — Lit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    try:
        arbre = ast.parse(open(os.path.join(racine, FABRICANT), encoding="utf-8").read())
    except (OSError, SyntaxError, ValueError):
        return None, None
    lues = {}
    for n in arbre.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            nom = n.targets[0].id
            if nom in ("VERSION_DE_PYTHON", "VERSIONS_COMPAREES") and nom not in lues:
                try:
                    lues[nom] = ast.literal_eval(n.value)
                except ValueError:
                    lues[nom] = None
    v, c = lues.get("VERSION_DE_PYTHON"), lues.get("VERSIONS_COMPAREES")
    if not (isinstance(v, str) and re.fullmatch(r"3\.\d+", v)):
        return None, None
    if not (isinstance(c, tuple) and c and all(isinstance(x, str) and re.fullmatch(r"3\.\d+", x) for x in c)):
        return None, None
    return v, c


def pythons_installes(racine):
    """Rend les Python à comparer, un par version mineure, ou un motif d'arrêt. ① RÔLE — Trouver de quoi comparer.
    ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine (pour lire les constantes du fabricant). ④ CONDITIONS D'ENTRÉE —
    —. ⑤ SORTIE — DEUX valeurs : la liste triée de triplets (version « 3.N », chemin, « exigée » ou « en plus »), et le
    motif d'arrêt (texte) ou None. [rend: 2] ⑥ TRAITEMENT — ① EXIGÉS : python3.11 et python3.13, cherchés par
    shutil.which sous leur nom EN CLAIR ; chacun doit être trouvé et répondre la version de son nom ; l'ensemble
    {3.11, 3.13} doit être celui des constantes du fabricant (VERSION_DE_PYTHON plus VERSIONS_COMPAREES) ; sinon motif
    d'arrêt (l'épreuve rend 2, R-734). ② EN PLUS, FACULTATIFS : l'interpréteur courant, puis python3.N trouvés dans
    /usr/bin et /usr/local/bin ; une version non encore vue est ajoutée et comparée COMME les exigées (un écart rougit).
    Chaque chemin demande lui-même sa version (`-c`). ⑦ UNITÉ — —. ⑧ POURQUOI — E6 (épreuve du circuit public) : un nom
    composé (« python3.%d » % n) ne dit pas quoi installer, la certification ne pouvait donc pas le garantir ; le
    17-11-2026 elle ne posait que 3.11 et l'épreuve, sur GitHub, comparait 3.11 au Python du système (3.14) au lieu de
    3.13 (m2). Les versions EN PLUS restent comparées : A-872 veut la même empreinte sous TOUTES les versions, un écart
    sous l'une est une instabilité réelle d'emp.py. ⑨ CE QUI CLOCHE — ① Sur GitHub (image ubuntu-26.04, mesuré le
    17-11-2026, A-893), le glob trouve /usr/bin/python3.14, le Python du système : 3.14 est alors comparée sans avoir
    jamais été éprouvée (la machine du Chat n'a que 3.11, 3.12, 3.13) ; un écart ou une propriété fausse sous 3.14
    rougira la certification — un rouge VRAI (emp.py instable sous une version que GitHub fournit), à trancher par
    Jean-Luc (emp.py est gelé, A-890) ; un ENFANT qui ne tourne pas sous 3.14 rendrait 2. Un passage d'essai sur GitHub
    est proposé avant la nuit. ② Les versions EN PLUS ne sont cherchées que là (glob), sans « command -v » : E6 ne
    les voit pas (faille annexe d'E6, BACKLOG). ③ Si la machine du Chat passe à une autre version, les exigés ne la
    suivent pas tant que VERSIONS_COMPAREES et ces deux noms ne changent pas ensemble. ⑩ EFFET — Lance de courts
    processus. ⑪ TERMINAISON — Rend la main ; chaque appel est borné à 30 s. [sort: non]"""
    def version_de(c):
        if not re.search(r"python3(\.\d+)?$", c) or not os.access(c, os.X_OK):
            return None
        try:
            r = subprocess.run([c, "-I", "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
                               capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return None
        v = r.stdout.strip()
        return v if r.returncode == 0 and re.fullmatch(r"3\.\d+", v) else None
    exiges = {"3.11": shutil.which("python3.11"), "3.13": shutil.which("python3.13")}
    executante, comparees = constantes_du_fabricant(racine)
    if executante is None:
        return [], "constantes VERSION_DE_PYTHON / VERSIONS_COMPAREES illisibles dans %s" % FABRICANT
    if set(exiges) != {executante} | set(comparees):
        return [], ("Python exigés ici %s, le fabricant pose %s : les noms écrits en clair et les constantes du "
                    "fabricant divergent" % (sorted(exiges), sorted({executante} | set(comparees))))
    trouves = {}
    for v, c in sorted(exiges.items()):
        if not c:
            return [], "python%s absent du PATH (exigé)" % v
        if version_de(c) != v:
            return [], "python%s (%s) ne répond pas la version %s" % (v, c, v)
        trouves[v] = (c, "exigée")
    candidats = [sys.executable]
    for d in ("/usr/bin", "/usr/local/bin"):
        candidats += sorted(glob.glob(os.path.join(d, "python3.[0-9]*")))
    for c in candidats:
        v = version_de(c)
        if v and v not in trouves:
            trouves[v] = (c, "en plus")
    return sorted(((v, c, s) for v, (c, s) in trouves.items()), key=lambda x: int(x[0].split(".")[1])), None


def mesurer(python, racine, premier=False):
    """Rend la mesure d'un Python, ou None. ① RÔLE — Faire calculer un Python. ② CONTEXTE D'APPEL — `juger`, une fois
    par version. ③ ENTRÉE — le chemin de l'interpréteur ; la racine ; `premier` : vrai sous --saboter, la mutation
    s'arrête au premier champ aveugle. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs : le dictionnaire rendu
    par ENFANT, ou None ; le motif d'échec, ou None. [rend: 2] ⑥ TRAITEMENT — lance ENFANT en -I -B (avec « --premier »
    si `premier`), lit la dernière ligne en JSON. ⑦ UNITÉ — —. ⑧ POURQUOI — Un processus par version : seule façon de
    calculer sous chacune. Le premier aveugle suffit à faire mordre un sabotage (E1 du superviseur R-759 du
    17-11-2026, point 3). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main ; DELAI au
    plus. [sort: non]"""
    try:
        r = subprocess.run([python, "-I", "-B", "-c", ENFANT, racine] + (["--premier"] if premier else []),
                           capture_output=True, text=True, timeout=DELAI)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, "%s : %s" % (type(e).__name__, e)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1]), None
    except (ValueError, IndexError):
        return None, "code %d, %r" % (r.returncode, (r.stdout + r.stderr)[-400:])


# Le texte d'emp.py après lequel S5 et S8 à S12 insèrent un champ sauté, et la forme de l'insertion.
_CHAMPS = '            if val is None or (isinstance(val, list) and not val):\n                continue\n'
_SAUTER = '            if %s:\n                continue\n'

# LES SABOTAGES (superviseur R-759 du 17-11-2026) : chacun écrit dans la copie légère ce qu'il nomme ; chacun doit
# faire rougir l'épreuve. (fichier, ancien texte, nouveau texte) — l'ancien doit figurer UNE fois, sinon code 2.
SABOTAGES = {
    "S1_ast_dump_remis": ("emp.py", 'return hashlib.sha256((FORMAT + "\\n" + _forme(a)).encode("utf-8"))',
                          'return hashlib.sha256((FORMAT + "\\n" + ast.dump(a)).encode("utf-8"))'),
    "S2_etiquette_retiree": ("emp.py", 'return hashlib.sha256((FORMAT + "\\n" + _forme(a)).encode("utf-8"))',
                             'return hashlib.sha256((_forme(a)).encode("utf-8"))'),
    "S3_kind_plus_saute": ("emp.py", '            if isinstance(x, ast.Constant) and nom == "kind":\n                continue\n',
                           ""),
    "S4_seconde_definition": (os.path.join("programmes", "LIRE_LE_CODE.py"), "\nimport ast, os, sys\n",
                              "\ndef _seconde_empreinte(src):\n    import ast as _a, hashlib as _hl\n"
                              "    t = _a.parse(src)\n    return _hl.sha256(_a.dump(t).encode()).hexdigest()[:16]\n\n\nimport ast, os, sys\n"),
    # S5 et S6 : les deux sabotages du relecteur neuf du 17-11-2026 (M1, rapport
    # etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/RELECTEUR_EMPREINTE_STABLE_Mar_17-11-2026.md). Avant
    # les propriétés de SENSIBILITÉ (is/==, ordre des arguments, 4/4.0), l'épreuve restait VERTE sous chacun.
    "S5_ops_et_op_sautes": ("emp.py", _CHAMPS, _CHAMPS + _SAUTER % 'nom in ("ops", "op")'),
    "S6_listes_triees": ("emp.py", 'return "[%s]" % ",".join(_forme(e) for e in x)',
                         'return "[%s]" % ",".join(sorted(_forme(e) for e in x))'),
    # S7 à S14 (E1 du superviseur R-759 du 17-11-2026, sur MAJ-1 du relecteur ; numéros du relecteur gardés pour S7,
    # S8, S10, S11) : S8, S10 et S11 restaient VERTS avant la mutation. S7 (nombres ramenés à float) tombe par les
    # propriétés 1.0/1 et 4/4.0 ; S8 à S13 sautent un champ ou tronquent une liste et doivent tomber par la MUTATION,
    # sans qu'aucun nom de champ ne soit écrit dans la propriété elle-même.
    "S7_nombres_normalises": ("emp.py", 'parties.append("value=%s:%r" % (type(val).__name__, val))',
                              'parties.append("value=%s:%r" % (("float", float(val)) if type(val) in (int, float) '
                              'else (type(val).__name__, val)))'),
    "S8_fstring_format_et_conversion_sautes": ("emp.py", _CHAMPS, _CHAMPS + _SAUTER % (
        '(isinstance(x, ast.FormattedValue) and nom in ("conversion", "format_spec"))')),
    "S9_ctx_saute": ("emp.py", _CHAMPS, _CHAMPS + _SAUTER % 'nom == "ctx"'),
    "S10_attr_saute": ("emp.py", _CHAMPS, _CHAMPS + _SAUTER % '(isinstance(x, ast.Attribute) and nom == "attr")'),
    "S11_valeurs_par_defaut_sautees": ("emp.py", _CHAMPS, _CHAMPS + _SAUTER % 'nom in ("defaults", "kw_defaults")'),
    "S12_level_saute": ("emp.py", _CHAMPS, _CHAMPS + _SAUTER % 'nom == "level"'),
    "S13_listes_tronquees": ("emp.py", 'return "[%s]" % ",".join(_forme(e) for e in x)',
                             'return "[%s]" % ",".join(_forme(e) for e in x[:2])'),
    # S14 : la forme de l'ARBRE ENTIER tronquée avant le hachage — `_forme` reste juste, la mutation locale reste
    # verte ; seul le contrôle de COMPOSITION (au niveau d'`empreinte`) doit la voir.
    "S14_forme_hachee_tronquee": ("emp.py", 'return hashlib.sha256((FORMAT + "\\n" + _forme(a)).encode("utf-8"))',
                                  'return hashlib.sha256((FORMAT + "\\n" + _forme(a)[:3000]).encode("utf-8"))'),
    # S15 : le BOM plus retiré (E2 du superviseur R-759 du 17-11-2026) — la propriété bom_sans_effet doit tomber.
    "S15_bom_plus_retire": ("emp.py", '    if src.startswith("\\ufeff"):\n        src = src[1:]\n', ""),
}


def _nom_d_appel(c):
    """Rend le nom d'un appel. ① RÔLE — Lire « module.fonction » dans l'arbre. ② CONTEXTE D'APPEL —
    `definitions_d_empreinte`. ③ ENTRÉE — un nœud ast.Call. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : le
    texte (« hashlib.sha256 », « parse », « ?.dump » si l'objet n'est pas un nom, « » sinon). [rend: 1] ⑥ TRAITEMENT —
    selon la forme de c.func. ⑦ UNITÉ — —. ⑧ POURQUOI — Un appel se reconnaît à son nom. ⑨ CE QUI CLOCHE — Un module
    importé sous un autre nom (`import ast as a`) donne « a.parse ». ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    f = c.func
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        return f.value.id + "." + f.attr
    if isinstance(f, ast.Attribute):
        return "?." + f.attr
    return f.id if isinstance(f, ast.Name) else ""


def definitions_d_empreinte(src):
    """Rend les endroits d'un texte Python qui calculent une empreinte de CODE. ① RÔLE — Le motif de la recherche
    d'une seconde définition (R-708). ② CONTEXTE D'APPEL — `autres_definitions`. ③ ENTRÉE — le texte d'un fichier.
    ④ CONDITIONS D'ENTRÉE — Il s'analyse. ⑤ SORTIE — UNE valeur : la liste triée de (ligne, fonction). [rend: 1]
    ⑥ TRAITEMENT — Dans chaque fonction : les noms affectés depuis un appel `….parse` ou `parse` (l'arbre) ; puis
    chaque appel `hashlib.…` (ou un module `_hashlib`, `_hl`, `h`) dont un argument contient un de ces noms ou un appel
    `….dump`. ⑦ UNITÉ — —. ⑧ POURQUOI — Une empreinte de code = un hachage de l'arbre ; un hachage d'octets
    (CERTIFIER_LA_VERSION.empreinte_du_code, ligne 288 : sha256 des fichiers) n'en est pas une. Calibré le
    17-11-2026 : retrouve emp.py (v1 et v2) et deux outils d'etudes/ qui hachent `ast.dump` ; ne retrouve pas
    CERTIFIER:288 ni deux épreuves qui analysent un arbre et hachent un fichier de données dans la même fonction.
    ⑨ CE QUI CLOCHE — Voir ⑨ ⑤ du fichier. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    trouves = set()
    for n in ast.walk(ast.parse(src)):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        arbres = set()
        for a in ast.walk(n):
            if isinstance(a, ast.Assign) and any(
                    isinstance(c, ast.Call) and (_nom_d_appel(c).endswith(".parse") or _nom_d_appel(c) == "parse")
                    for c in ast.walk(a.value)):
                arbres |= {x.id for x in a.targets if isinstance(x, ast.Name)}
        for c in ast.walk(n):
            if not (isinstance(c, ast.Call) and _nom_d_appel(c).split(".")[0] in ("hashlib", "_hashlib", "_hl", "h")):
                continue
            for arg in c.args:
                if any((isinstance(x, ast.Name) and x.id in arbres)
                       or (isinstance(x, ast.Call) and _nom_d_appel(x).endswith(".dump")) for x in ast.walk(arg)):
                    trouves.add((c.lineno, n.name))
    return sorted(trouves)


def autres_definitions(racine):
    """Rend les définitions trouvées hors d'emp.py, ou un motif d'échec du calibrage. ① RÔLE — Prouver qu'emp.py est le
    seul endroit (A-872). ② CONTEXTE D'APPEL — `juger`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE —
    DEUX valeurs : la liste des « fichier:ligne fonction » hors emp.py ; le motif d'échec du calibrage, ou None.
    [rend: 2] ⑥ TRAITEMENT — Calibrage : le motif DOIT retrouver emp.py:empreinte et NE DOIT PAS retrouver
    CERTIFIER_LA_VERSION.empreinte_du_code (un cas qui doit échouer : sinon il sur-détecte) ; puis tous les .py de la
    racine, de programmes/ et de tests/. ⑦ UNITÉ — —. ⑧ POURQUOI — « Un motif se calibre sur un cas connu, et sur un
    cas qui doit échouer » (instructions, §4). ⑨ CE QUI CLOCHE — etudes/ et archives/ ne sont pas cherchés : ce sont
    des brouillons, pas du code vivant. ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    def dans(rel):
        return definitions_d_empreinte(open(os.path.join(racine, rel), encoding="utf-8").read())
    if not any(nom == "empreinte" for _l, nom in dans("emp.py")):
        return [], "le motif ne retrouve pas emp.py:empreinte"
    certifier = os.path.join("programmes", "CERTIFIER_LA_VERSION.py")
    if not os.path.isfile(os.path.join(racine, certifier)):
        return [], "témoin négatif absent : %s" % certifier
    if dans(certifier):
        return [], "le motif retrouve %s (%s) : il sur-détecte" % (certifier, dans(certifier))
    fichiers = sorted(set(glob.glob(os.path.join(racine, "*.py")) + glob.glob(os.path.join(racine, "programmes", "*.py"))
                          + glob.glob(os.path.join(racine, "tests", "**", "*.py"), recursive=True)))
    autres = []
    for f in fichiers:
        rel = os.path.relpath(f, racine)
        if rel == "emp.py":
            continue
        try:
            autres += ["%s:%d %s" % (rel, l, nom) for l, nom in dans(rel)]
        except SyntaxError:
            autres.append("%s NON ANALYSABLE" % rel)
    return autres, None


def juger(racine, pythons, premier=False):
    """Joue l'épreuve sur une racine ; rend (code, défauts). ① RÔLE — Comparer et juger. ② CONTEXTE D'APPEL — `main`,
    sur la racine (tous les Python) puis sur chaque copie sabotée (un seul Python, `premier` vrai). ③ ENTRÉE — la
    racine ; les Python ; `premier` (voir `mesurer`). ④ CONDITIONS D'ENTRÉE — Celles du fichier. ⑤ SORTIE — DEUX
    valeurs : 0, 1 ou 2 ; la liste des défauts (ou le motif d'arrêt). [rend: 2]
    ⑥ TRAITEMENT — `mesurer` pour chaque Python, comparaison fichier par fichier, propriétés (dont la mutation locale
    et la composition, avec leurs comptes et leurs durées imprimés), `autres_definitions`.
    ⑦ UNITÉ — Des secondes pour les durées imprimées. ⑧ POURQUOI — Voir le fichier. ⑨ CE QUI CLOCHE — —. ⑩ EFFET —
    Imprime. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    mesures = {}
    for v, chemin in pythons:
        m, motif = mesurer(chemin, racine, premier)
        if m is None:
            return 2, ["Python %s sans réponse lisible — %s" % (v, motif)]
        mesures[v] = m
    defauts = []
    versions = list(mesures)
    fichiers = sorted(set().union(*(m["empreintes"] for m in mesures.values())))
    ecarts = 0
    for f in fichiers:
        valeurs = {v: mesures[v]["empreintes"].get(f, "ABSENT") for v in versions}
        if len(set(valeurs.values())) != 1 or any(not re.fullmatch(r"[0-9a-f]{16}", x) for x in valeurs.values()):
            ecarts += 1
            if ecarts <= 3:
                print("  ÉCART %s : %s" % (f, " · ".join("%s=%s" % kv for kv in valeurs.items())))
    print("Fichiers comparés : %d ; en écart : %d" % (len(fichiers), ecarts))
    if ecarts:
        defauts.append("%d fichier(s) dont l'empreinte diffère selon la version de Python" % ecarts)
    for v in versions:
        m = mesures[v]
        print("  Python %s · étiquette %r · emp.py %s · JUGE %s" % (
            m["version"], m["format"], m["empreintes"].get("emp.py"),
            m["empreintes"].get(os.path.join("programmes", "JUGE_DES_STRATEGIES.py"))))
        mu, co = m["mutation"], m["composition"]
        print("    mutation locale : %d mutations, %d champs (nœud.champ) distincts, %d aveugle(s)%s, %d type(s) non "
              "prévu(s)%s, %.1f s%s" % (mu["mutations"], mu["champs"], mu["nb_aveugles"],
                                       (" — " + " ; ".join(mu["aveugles"])) if mu["aveugles"] else "",
                                       len(mu["inconnus"]), (" — " + " ; ".join(mu["inconnus"])) if mu["inconnus"] else "",
                                       mu["secondes"], " (arrêt au premier aveugle)" if mu["arret_au_premier"] else ""))
        print("    composition : %d fichiers mutés, %d aveugle(s)%s, sans instruction : %s, %.1f s" % (
            co["vues"], co["nb_aveugles"], (" — " + " ; ".join(co["aveugles"])) if co["aveugles"] else "",
            ", ".join(co["sans_instruction"]) or "aucun", co["secondes"]))
        for p, ok in sorted(m["proprietes"].items()):
            if not ok:
                defauts.append("Python %s : propriété fausse « %s »" % (v, p))
        if m["v1_egales"]:
            defauts.append("Python %s : %d empreinte(s) v2 égales à la v1 (%s…)" % (v, len(m["v1_egales"]),
                                                                                   m["v1_egales"][0]))
    total = {v: hashlib.sha256("".join("%s %s\n" % kv for kv in sorted(mesures[v]["empreintes"].items()))
                                              .encode()).hexdigest()[:16] for v in versions}
    print("Empreinte totale par version : %s" % " · ".join("%s=%s" % kv for kv in total.items()))
    autres, motif = autres_definitions(racine)
    if motif:
        return 2, ["motif des autres définitions hors calibrage : %s" % motif]
    print("Autres endroits qui calculent une empreinte de code : %s" % (", ".join(autres) or "aucun"))
    if autres:
        defauts.append("seconde définition de l'empreinte du code : %s" % ", ".join(autres))
    if defauts:
        print("ROUGE — %d défaut(s) :" % len(defauts))
        for d in defauts:
            print("  - %s" % d)
        return 1, defauts
    print("VERT — %d fichiers, %d versions de Python, %d propriétés tenues partout, emp.py seul" % (
        len(fichiers), len(versions), len(mesures[versions[0]]["proprietes"])))
    return 0, []


def main():
    """Joue l'épreuve, puis les sabotages. ① RÔLE — Point d'entrée. ② CONTEXTE D'APPEL — Le lancement du fichier.
    ③ ENTRÉE — sys.argv. ④ CONDITIONS D'ENTRÉE — Celles du fichier. ⑤ SORTIE — Le code de sortie, 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — `pythons_installes`, `juger` sur la racine (tous les Python) ; sous --saboter, pour chaque
    sabotage : copie légère (emp.py, programmes/, tests/), texte remplacé (trouvé une fois, sinon 2), `juger` sous le
    SEUL premier Python trouvé (le plus ancien : 3.11, celui du circuit), mutation arrêtée au premier champ aveugle,
    qui doit rendre 1 ; copie effacée.
    ⑦ UNITÉ — —. ⑧ POURQUOI — « Un jeu d'épreuves se sabote contre sa propre correction » (instructions, §7). Un seul
    Python et l'arrêt au premier aveugle sous --saboter : E1 du superviseur R-759 du 17-11-2026, point 3 (durée).
    ⑨ CE QUI CLOCHE — Sous --saboter, l'écart ENTRE versions n'est pas rejoué : un sabotage qui ne romprait que la
    concordance entre versions ne mordrait pas (aucun des sabotages présents : chacun fait tomber une propriété sous
    un seul Python, voir la sortie). ⑩ EFFET — Imprime ; écrit et efface les copies. ⑪ TERMINAISON — Sort par sys.exit.
    [sort: oui]"""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) > 1 or any(o != "--saboter" for o in options):
        print("USAGE : %s [racine] [--saboter]" % os.path.basename(__file__))
        sys.exit(2)
    racine = os.path.abspath(args[0] if args else os.path.join(os.path.dirname(__file__), ".."))
    if not os.path.isfile(os.path.join(racine, "emp.py")):
        print("NE PEUT PAS TOURNER : pas d'emp.py dans %s" % racine)
        sys.exit(2)
    trouves, motif = pythons_installes(racine)
    if motif:
        print("NE PEUT PAS TOURNER : %s (R-734)" % motif)
        sys.exit(2)
    print("Python trouvés : %s" % ", ".join("%s (%s, %s)" % p for p in trouves))
    pythons = [(v, c) for v, c, _s in trouves]
    code, defauts = juger(racine, pythons)
    if code == 2:
        print("NE PEUT PAS TOURNER : %s" % defauts[0])
        sys.exit(2)
    if code != 0 or "--saboter" not in options:
        sys.exit(code)
    ne_mord_pas = []
    for nom, (rel, ancien, nouveau) in SABOTAGES.items():
        print("— %s" % nom)
        d = tempfile.mkdtemp(prefix="emp_sabotage_")
        try:
            shutil.copy2(os.path.join(racine, "emp.py"), d)
            for sous in ("programmes", "tests"):
                shutil.copytree(os.path.join(racine, sous), os.path.join(d, sous),
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            chemin = os.path.join(d, rel)
            texte = open(chemin, encoding="utf-8").read()
            if texte.count(ancien) != 1:
                print("NE PEUT PAS TOURNER : sabotage %s : texte trouvé %d fois" % (nom, texte.count(ancien)))
                sys.exit(2)
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(texte.replace(ancien, nouveau, 1))
            code_s, defauts_s = juger(d, pythons[:1], premier=True)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        print("%s %s" % (nom, "mord" if code_s == 1 else "NE MORD PAS (code %d)" % code_s))
        if code_s != 1:
            ne_mord_pas.append(nom)
    if ne_mord_pas:
        print("VERDICT : NON CONFORME — sabotages sans effet : %s" % ne_mord_pas)
        sys.exit(1)
    print("VERDICT : tout est conforme — %d sabotages mordent" % len(SABOTAGES))
    sys.exit(0)


if __name__ == "__main__":
    main()
