"""emp — L'EMPREINTE DU CODE d'un fichier Python : la seule définition du dépôt (R-708). Format « emp-v2 ».

① RÔLE — Rendre seize caractères qui changent si, et seulement si, le CODE d'un fichier change : ni un commentaire, ni
  un texte explicatif (la chaîne en tête d'un module, d'une classe ou d'une fonction), ni la mise en page ne la
  changent ; et la même valeur pour un même code sous toutes les versions de Python.
② CONTEXTE D'APPEL — Importé : `programmes/LIRE_LE_CODE.empreinte_du_code` (donc le marqueur, le garde-fou et
  `JUGE_DES_STRATEGIES.empreinte_d_un_module`, d'où l'empreinte des réglages, `jeton_d_essai`, le tri, le registre des
  essais, JUGER_UNE_FICHE) ; `programmes/DECLARER_UNE_STRATEGIE.empreintes_du_code` (chargé par chemin). À la main :
  `python3 emp.py FICHIER…` imprime l'empreinte de chaque fichier.
③ ENTRÉE — `empreinte(src)` : le texte entier d'un fichier Python (str), avec ou sans la marque d'ordre des octets
  (BOM, le caractère U+FEFF) qu'un éditeur Windows peut poser en tête : elle est retirée ici, à un seul endroit,
  jamais chez chaque lecteur (MIN-1 du relecteur du 17-11-2026 : un fichier avec BOM s'exécute, mais `ast.parse` de
  la chaîne levait SyntaxError).
④ CONDITIONS D'ENTRÉE — Le texte s'analyse sous le Python qui tourne ; sinon SyntaxError, levée telle quelle.
⑤ SORTIE — `empreinte` rend UNE valeur : seize caractères hexadécimaux, les seize premiers du sha256 de l'étiquette
  FORMAT, d'un saut de ligne et de la forme stable de l'arbre. En ligne de commande : une ligne par fichier,
  « empreinte  chemin ». Exemple mesuré le 17-11-2026 : programmes/JUGE_DES_STRATEGIES.py rend la même valeur sous
  Python 3.11, 3.12 et 3.13 (épreuve tests/EPREUVES_DE_L_EMPREINTE_STABLE_Mar_17-11-2026.py).
⑥ TRAITEMENT — ⓪ retirer un BOM en tête du texte · ① analyser (`ast.parse`) · ② retirer la chaîne en tête du corps de chaque module, classe et fonction
  (le texte explicatif) · ③ écrire l'arbre sous une forme stable (`_forme`) : le nom du nœud, puis chaque champ
  (`ast.iter_fields`) nommé, en SAUTANT les champs qui valent None ou [] et le champ `kind` des constantes ; la valeur
  d'une constante s'écrit avec son type et son repr (1 et 1.0, True et 1, 0.0 et -0.0 diffèrent) · ④ hacher
  « emp-v2 », un saut de ligne, puis cette forme.
⑦ UNITÉ — Aucune.
⑧ POURQUOI — Décision de Jean-Luc du 17-11-2026 à 07h46 (A-872, « 1 », option « Oui, on change la définition une fois
  pour toutes ») : une forme stable entre versions de Python, à un seul endroit, avec une étiquette de format.
  L'ancienne forme (v1, sans étiquette) hachait le texte de `ast.dump`, qui change d'une version à l'autre : le
  superviseur R-759 a mesuré le 17-11-2026 à 00h18 (A-871) que C5E10-QA-V1 rendait 6f4658b2… en 3.11, 571fac04… en
  3.12, d622c74a… en 3.13 — GitHub (3.11) et la machine du Chat (3.13) ne reconnaissaient pas le même code. Les
  champs vides que `ast.dump` écrit ou omet selon la version (par exemple `type_params=[]`, apparu en 3.12) sont
  sautés : la forme devient commune. `kind` vaut « u » pour u"…" et None sinon : c'est une graphie, pas du code.
  L'étiquette « emp-v2 » est DANS le texte haché : une empreinte v1 ne peut pas être prise pour la v2 du même code.
⑨ CE QUI CLOCHE — ① Une version FUTURE de Python peut renommer un nœud ou ajouter un champ non vide ; l'épreuve
  multi-versions le verra sous chaque Python installé, pas avant. ② Un fichier qu'une version ancienne n'analyse pas
  (syntaxe plus récente) lève sous elle. ③ Une chaîne seule en tête d'un corps est toujours prise pour un texte
  explicatif et retirée de l'empreinte. Elle n'est PAS sans effet à l'exécution : Python la range dans `__doc__`, et
  un programme peut la lire — 21 lectures de `__doc__` dans programmes/ (compté le 17-11-2026 par
  `grep -rn __doc__ programmes/*.py`), par exemple CALIBRER_LE_HASARD_DES_GAINS.py:325, qui découpe `__doc__` sur
  « USAGE ». Conséquence, LIMITE CONSIGNÉE et non corrigée (code inchangé, relecteur neuf du 17-11-2026, m1) : un
  changement de ce texte qui change ce qu'un programme affiche, ou le fait lever, laisse l'empreinte INCHANGÉE.
  La même limite est notée par CONTROLER_MA_LIVRAISON.py (⑨ de la comparaison à `origin/main`). ④ Le code qu'un module charge par chemin n'est pas dans son empreinte (N7,
  BACKLOG). ⑤ `_forme` est récursive : un arbre plus profond que la limite de récursion de Python lèverait
  RecursionError (aucun fichier du dépôt ne l'atteint, mesuré le 17-11-2026 sur programmes/ et tests/). ⑥ CE FICHIER
  EST VERROUILLÉ À L'OCTET : le sha256 de ses octets et l'étiquette FORMAT sont rangés avec la valeur figée de
  C5E10-QA-V1 (programmes/CONTRATS_DES_FICHIERS.py, EMPREINTE_FIGEE_CALCULEE_AVEC) ; TOUTE modification, même d'un
  commentaire, fait rougir l'épreuve E-ancre (tests/EPREUVES_DE_L_ESSAI_SANS_REGARD_Lun_16-11-2026.py). Voulu (E1,
  point 4, du superviseur R-759 du 17-11-2026) : la marche à suivre est écrite à côté de la valeur figée.
⑩ EFFET — Aucun à l'import. En ligne de commande : lit les fichiers nommés et imprime.
⑪ TERMINAISON — Rend la main. Un de mes appels peut-il ne pas revenir ? Non : l'analyse et le parcours d'un arbre fini
  finissent.
  [sort: non]
"""
import ast
import hashlib
import sys

# L'ÉTIQUETTE DU FORMAT, hachée avec la forme : la changer change toutes les empreintes (A-872).
FORMAT = "emp-v2"

_SANS_TEXTE = (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)


def _forme(x):
    """Écrit un nœud, une liste ou une valeur sous la forme stable.

    ① RÔLE — Donner un texte qui ne dépend que du code, pas de la version de Python.
    ② CONTEXTE D'APPEL — `empreinte`, sur l'arbre entier ; elle-même, sur chaque champ.
    ③ ENTRÉE — `x` : un nœud de `ast`, une liste, ou une valeur (nom, nombre, chaîne, octets, None, Ellipsis).
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — Nœud : « Nom(champ=forme,…) », champs pris par `ast.iter_fields` dans leur ordre, sauf ceux qui
      valent None ou [] et sauf `kind` d'une constante ; la valeur d'une constante s'écrit « type:repr ». Liste :
      « [forme,…] ». Autre valeur : son repr.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — Voir ⑧ du fichier : le texte de `ast.dump` diffère selon la version.
    ⑨ CE QUI CLOCHE — Un champ ajouté par une version future avec une valeur non vide changerait la forme sous elle.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main : la récursion descend un arbre fini.
      [sort: non]
    """
    if isinstance(x, ast.AST):
        parties = []
        for nom, val in ast.iter_fields(x):
            if val is None or (isinstance(val, list) and not val):
                continue
            if isinstance(x, ast.Constant) and nom == "kind":
                continue
            if isinstance(x, ast.Constant) and nom == "value":
                parties.append("value=%s:%r" % (type(val).__name__, val))
                continue
            parties.append("%s=%s" % (nom, _forme(val)))
        return "%s(%s)" % (type(x).__name__, ",".join(parties))
    if isinstance(x, list):
        return "[%s]" % ",".join(_forme(e) for e in x)
    return repr(x)


def empreinte(src):
    """Rend l'empreinte « emp-v2 » du code d'un texte Python.

    ① RÔLE — La seule définition de l'empreinte du code (R-708).
    ② CONTEXTE D'APPEL — Voir ② du fichier.
    ③ ENTRÉE — `src` : le texte d'un fichier Python (str), avec ou sans BOM en tête.
    ④ CONDITIONS D'ENTRÉE — Il s'analyse, une fois le BOM retiré ; sinon SyntaxError.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — Retirer UN BOM (U+FEFF) en tête ; analyser ; retirer le texte explicatif en tête de chaque module,
      classe, fonction ; hacher FORMAT, un saut de ligne et `_forme` de l'arbre ; garder seize caractères.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — Voir ⑧ du fichier. Le BOM : Python exécute un fichier qui en porte un, donc son empreinte doit être
      celle du même fichier sans BOM (correction E2 du superviseur R-759 du 17-11-2026, sur MIN-1 du relecteur).
    ⑨ CE QUI CLOCHE — Voir ⑨ du fichier. Un seul BOM est retiré : deux BOM de suite ne s'exécutent pas non plus.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if src.startswith("\ufeff"):
        src = src[1:]
    a = ast.parse(src)
    for n in ast.walk(a):
        if isinstance(n, _SANS_TEXTE):
            if (n.body and isinstance(n.body[0], ast.Expr)
                    and isinstance(n.body[0].value, ast.Constant)
                    and isinstance(n.body[0].value.value, str)):
                n.body = n.body[1:]
    return hashlib.sha256((FORMAT + "\n" + _forme(a)).encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"{empreinte(open(p,encoding='utf-8').read())}  {p}")
