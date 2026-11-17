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
R-759 du 17-11-2026) : une seconde définition divergerait (R-708). Avec « --saboter », elle écrit chaque sabotage dans
une copie légère (emp.py, programmes/, tests/) et exige que chacun la fasse rougir.

① RÔLE — Rougir si deux versions de Python rendent une empreinte différente pour un même fichier, ou si une propriété
  de la définition tombe sous l'une d'elles.
② CONTEXTE D'APPEL — À la main, par le Chat ou un agent ; `python3 tests/EPREUVES_DE_L_EMPREINTE_STABLE_Mar_17-11-2026.py
  [racine]`.
③ ENTRÉE — La ligne de commande : la racine du dépôt (facultative ; par défaut, le dossier parent de tests/) ;
  « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte emp.py, programmes/ et tests/. Au moins DEUX versions de Python installées parmi
  celles que `pythons_installes` cherche.
⑤ SORTIE — Le code de sortie : 0 si tout concorde, toutes les propriétés tiennent sous chaque Python, aucun autre
  endroit ne calcule d'empreinte de code et, avec --saboter, chaque sabotage mord ; 1 sinon ; 2 si l'épreuve n'a pas
  pu tourner — moins de deux versions de Python, un sous-processus sans réponse lisible, le motif de recherche qui
  échoue à son calibrage, ou un sabotage dont le texte n'est pas trouvé (R-734 : un contrôle qui n'a pas pu tourner
  ne rend jamais 0).
  [rend: 1]
⑥ TRAITEMENT — ① chercher les Python installés, un par version mineure · ② pour chacun, un sous-processus isolé (-I -B)
  qui importe emp.py de la racine et rend en JSON : la version, l'étiquette, l'empreinte de chaque fichier, le résultat
  de chaque propriété · ③ comparer fichier par fichier ; imprimer les écarts et les propriétés fausses · ④ chercher
  les autres définitions (`autres_definitions`), motif calibré d'abord · ⑤ sous --saboter, rejouer ① à ④ sur une
  copie sabotée, pour chaque sabotage de SABOTAGES.
⑦ UNITÉ — Des empreintes (seize caractères hexadécimaux) ; des secondes (DELAI, par sous-processus).
⑧ POURQUOI — A-871 : GitHub (3.11) et la machine du Chat (3.13) ne reconnaissaient pas le même code ; jeton_d_essai,
  le tri, le registre des essais et les déclarations comparent des empreintes calculées sur des machines différentes.
  Une seule mesure le prouve : calculer partout et comparer.
⑨ CE QUI CLOCHE — ① Seules les versions INSTALLÉES sont éprouvées : une version future (3.14) peut changer l'arbre ;
  l'épreuve la prendra dès qu'elle sera installée. ② Les propriétés sont jouées sur de petits textes écrits ici, pas
  sur tous les programmes. ③ Le témoin de l'ancienne forme (`ANCIENNE_FORME_V1`) est une RECOPIE de l'ancienne
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
import ast, glob, hashlib, json, os, sys
racine = sys.argv[1]
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
print(json.dumps({"version": "%d.%d.%d" % sys.version_info[:3], "format": fmt, "empreintes": empreintes,
                  "proprietes": proprietes, "v1_egales": v1_egales}))
'''


def pythons_installes():
    """Rend les Python installés, un par version mineure. ① RÔLE — Trouver de quoi comparer. ② CONTEXTE D'APPEL —
    `main`. ③ ENTRÉE — Aucune. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la liste triée de couples
    (version « 3.N », chemin). [rend: 1] ⑥ TRAITEMENT — Cherche python3.N dans le PATH (N de 8 à 20), dans /usr/bin et
    /usr/local/bin, plus l'interpréteur courant ; garde le premier chemin trouvé par version, qu'il demande lui-même
    (`-c`). ⑦ UNITÉ — —. ⑧ POURQUOI — Éprouver toutes les versions présentes, sans liste écrite à la main.
    ⑨ CE QUI CLOCHE — Un Python installé ailleurs (pyenv, /opt) n'est vu que s'il est dans le PATH. ⑩ EFFET — Lance
    de courts processus. ⑪ TERMINAISON — Rend la main ; chaque appel est borné à 30 s. [sort: non]"""
    candidats = [sys.executable]
    for n in range(8, 21):
        w = shutil.which("python3.%d" % n)
        if w:
            candidats.append(w)
    for d in ("/usr/bin", "/usr/local/bin"):
        candidats += sorted(glob.glob(os.path.join(d, "python3.[0-9]*")))
    trouves = {}
    for c in candidats:
        if not re.search(r"python3(\.\d+)?$", c) or not os.access(c, os.X_OK):
            continue
        try:
            r = subprocess.run([c, "-I", "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
                               capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            continue
        v = r.stdout.strip()
        if r.returncode == 0 and re.fullmatch(r"3\.\d+", v) and v not in trouves:
            trouves[v] = c
    return sorted(trouves.items(), key=lambda kv: int(kv[0].split(".")[1]))


def mesurer(python, racine):
    """Rend la mesure d'un Python, ou None. ① RÔLE — Faire calculer un Python. ② CONTEXTE D'APPEL — `main`, une fois
    par version. ③ ENTRÉE — le chemin de l'interpréteur ; la racine. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX
    valeurs : le dictionnaire rendu par ENFANT, ou None ; le motif d'échec, ou None. [rend: 2] ⑥ TRAITEMENT — lance
    ENFANT en -I -B, lit la dernière ligne en JSON. ⑦ UNITÉ — —. ⑧ POURQUOI — Un processus par version : seule façon
    de calculer sous chacune. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main ; DELAI
    au plus. [sort: non]"""
    try:
        r = subprocess.run([python, "-I", "-B", "-c", ENFANT, racine], capture_output=True, text=True, timeout=DELAI)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, "%s : %s" % (type(e).__name__, e)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1]), None
    except (ValueError, IndexError):
        return None, "code %d, %r" % (r.returncode, (r.stdout + r.stderr)[-400:])


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


def juger(racine, pythons):
    """Joue l'épreuve sur une racine ; rend (code, défauts). ① RÔLE — Comparer et juger. ② CONTEXTE D'APPEL — `main`,
    sur la racine puis sur chaque copie sabotée. ③ ENTRÉE — la racine ; les Python. ④ CONDITIONS D'ENTRÉE — Celles du
    fichier. ⑤ SORTIE — DEUX valeurs : 0, 1 ou 2 ; la liste des défauts (ou le motif d'arrêt). [rend: 2]
    ⑥ TRAITEMENT — `mesurer` pour chaque Python, comparaison fichier par fichier, propriétés, `autres_definitions`.
    ⑦ UNITÉ — —. ⑧ POURQUOI — Voir le fichier. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Imprime. ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    mesures = {}
    for v, chemin in pythons:
        m, motif = mesurer(chemin, racine)
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
    ⑥ TRAITEMENT — `pythons_installes`, `juger` sur la racine ; sous --saboter, pour chaque sabotage : copie légère
    (emp.py, programmes/, tests/), texte remplacé (trouvé une fois, sinon 2), `juger`, qui doit rendre 1 ; copie effacée.
    ⑦ UNITÉ — —. ⑧ POURQUOI — « Un jeu d'épreuves se sabote contre sa propre correction » (instructions, §7).
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Imprime ; écrit et efface les copies. ⑪ TERMINAISON — Sort par sys.exit.
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
    pythons = pythons_installes()
    print("Python trouvés : %s" % ", ".join("%s (%s)" % p for p in pythons))
    if len(pythons) < 2:
        print("NE PEUT PAS TOURNER : moins de deux versions de Python — rien à comparer (R-734)")
        sys.exit(2)
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
            code_s, defauts_s = juger(d, pythons)
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
