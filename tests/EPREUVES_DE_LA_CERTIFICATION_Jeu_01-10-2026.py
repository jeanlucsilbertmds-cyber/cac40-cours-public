#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_CERTIFICATION — Jeu 01-10-2026 (Paris), réécrites le Ven 02-10-2026
Rôle : prouver que programmes/CERTIFIER_LA_VERSION.py refuse une version qui recule, et qu'il ne refuse pas les autres.
Quand l'appeler : avant toute livraison qui touche le certificateur ou tests/LANCEMENT_DES_EPREUVES.json (R-731) ; le certificateur
lui-même la rejoue à chaque certification, puisqu'elle vit dans tests/.

À QUOI ÇA SERT. Le certificateur dit si une version du dépôt est certifiée : toutes les épreuves vertes, et rien de moins
examiné qu'à la référence. S'il se trompe en disant « certifiée », plus rien ne protège le système et personne ne le voit.
Ces épreuves fabriquent un dépôt minuscule dont on connaît la bonne réponse — un programme CALCUL.py de trois fonctions,
une épreuve qui l'appelle — et font juger au VRAI certificateur des versions qui reculent de chacune des façons connues,
dont les cinq que la relecture indépendante du 01-10-2026 a fait passer dans la première version (S10 à S14).

LES ÉPREUVES (code de sortie attendu du certificateur) :
Z0 témoin : la référence s'écrit (0), puis la même version est certifiée (0) · S1 une épreuve devient rouge → 1 ·
S2 `triple` n'est plus appelée → 1 · S3 la référence manque → 2 · S4 un fichier programmes/EPREUVES_X.py que la table de
lancement ne déclare pas → 2 · S5 le certificateur saboté ne transmet plus la variable qui arme la mesure : la mesure est aveugle,
le calibrage doit le dire → 2 · S6 une épreuve qui ne revient pas est arrêtée (code 124) et comptée rouge → 1 · S7 un
programme nouveau qu'aucune épreuve n'examine → 1 · S8 deux lignes ajoutées en tête de CALCUL.py décalent tous les
numéros, rien d'autre ne change → 0 · S9 écrire une référence qui recule sans l'accord de Jean-Luc est refusé (1) et la
référence ne change pas ; avec --accord, elle s'écrit (0) et porte l'accord · S10 LEURRE : l'épreuve n'appelle plus
`triple` dans le vrai programme mais dans une copie de même nom au contenu différent → 1 · S11 SOUS-DOSSIER : `signe` est
déplacée dans programmes/lib/SIGNE.py, qu'aucune épreuve n'appelle → 1 · S12 ÉCHANGE : la référence examine `return 1` de
`signe` et pas `return -1` ; ensuite l'inverse, à nombres égaux → 1 · S13 une épreuve disparaît → 1 · S14 une épreuve
nommée dans un texte d'une autre reste jouée, et un outil importé par une épreuve n'est pas joué → 0 (c'est le cas qui
ne doit PAS rougir) · S15 DÉRIVE : seule une donnée lue par l'épreuve change, le code est identique → 0, et le rapport
dit « DÉRIVE DE MESURE » · S16 le certificateur saboté crédite toute copie de même nom, sans regarder l'empreinte : le
calibrage doit voir le leurre → 2 · S17 un programme qui porte son propre jeu d'épreuves (mode « epreuves » lu sur sa
ligne de commande, R-731 ①) sans être déclaré à la table de lancement → 2 · S18 ce mode, déclaré à la table, rend 1 : il est joué et
compté rouge → 1 · S19 la table de lancement ne se lit pas → 2, sans plantage · S20 un programme qu'aucune épreuve
n'exécute est cassé (erreur de syntaxe) → 2, et le rapport ne le dit pas « disparu » (cassure K1 de Cowork, 02-10-2026) ·
S21 une épreuve de tests/ est cassée (erreur de syntaxe) → 2, avec un rapport, et non une trace. Puis, sur un programme
AUTRE.py qu'aucune épreuve n'exécute (relecture de Cowork du 02-10-2026, second tour) : S22 il est vidé → 1 · S23 il perd
sa ligne « import os » → 1 · S24 il porte un octet qui n'est pas de l'UTF-8 → 2, « que Python ne sait pas lire » · S25 une
épreuve se met à l'exécuter → 0 : un progrès n'est pas un recul (le cas qui ne doit PAS rougir) · S26 une épreuve est jouée sans la configuration Git
de la machine → 0 (le 02-10-2026, la signature des commits de la machine du Chat faisait rougir une épreuve ici seulement) ·
S27 AUTRE.py, qu'aucune épreuve n'exécute, est supprimé → 1 (cas K19 de Cowork, troisième tour).

LES SABOTAGES (avec --saboter) : chaque correction du certificateur est retirée, une à la fois, dans une copie ; l'épreuve
qui la surveille DOIT changer de résultat. Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une
preuve, c'est une décoration (R-731). Liste : `SABOTAGES`.

USAGE : python3 tests/EPREUVES_DE_LA_CERTIFICATION_Jeu_01-10-2026.py <racine du dépôt> [--saboter]
CODE : 0 si toutes les épreuves rendent le résultat attendu et, avec --saboter, si chaque sabotage fait changer l'épreuve
qu'il vise ; 1 sinon ; 2 si le certificateur est introuvable ou si un sabotage ne s'applique plus (son texte n'est pas
présent exactement une fois).
"""
import concurrent.futures
import os
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
CERTIFICATEUR = os.path.join(DEPOT, "programmes", "CERTIFIER_LA_VERSION.py")
REFERENCE = os.path.join("gouvernance", "CERTIFICAT_REFERENCE.json")
RAPPORT = os.path.join("rapports", "CERTIFICAT_DE_LA_VERSION.md")

CALCUL = ("def double(x):\n    return 2 * x\n\n\ndef triple(x):\n    return 3 * x\n\n\n"
          "def signe(x):\n    if x >= 0:\n        return 1\n    return -1\n")
TOUS = "assert C.double(2) == 4; assert C.triple(2) == 6; assert C.signe(3) == 1; assert C.signe(-3) == -1"
EPREUVE = ("import os, subprocess, sys\n"
           "racine = sys.argv[1]\n"
           "code = \"import sys; sys.path.insert(0, 'programmes'); import CALCUL as C; \" + {appels!r}\n"
           "r = subprocess.run([sys.executable, '-E', '-c', code], cwd=racine, timeout=120)\n"
           "sys.exit(r.returncode)\n")
LEURRE = ("import os, subprocess, sys, tempfile\n"
          "racine = sys.argv[1]\n"
          "t = tempfile.mkdtemp()\n"
          "os.makedirs(os.path.join(t, 'programmes'))\n"
          "open(os.path.join(t, 'programmes', 'CALCUL.py'), 'w').write(\n"
          "    open(os.path.join(racine, 'programmes', 'CALCUL.py')).read() + '\\n# leurre\\n')\n"
          "entete = \"import sys; sys.path.insert(0, 'programmes'); import CALCUL as C; \"\n"
          "subprocess.run([sys.executable, '-E', '-c', entete + 'C.triple(2)'], cwd=t, check=True, timeout=120)\n"
          "subprocess.run([sys.executable, '-E', '-c', entete + 'C.double(2); C.signe(3); C.signe(-3)'], cwd=racine,\n"
          "               check=True, timeout=120)\n")


def epreuve(appels):
    """Rend le texte d'une épreuve du dépôt minuscule qui exécute `appels` sur CALCUL.py.

    ① RÔLE — Écrire en une ligne une épreuve qui ressemble aux vraies : elle lance le programme dans un sous-processus
      `python -E`, comme le font les épreuves du dépôt.
    ② CONTEXTE D'APPEL — `fabriquer` et les cas qui changent ce que l'épreuve appelle.
    ③ ENTRÉE — `appels` : du Python où `C` désigne le module CALCUL.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte du fichier.
      [rend: 1]
    ⑥ TRAITEMENT — remplir le modèle `EPREUVE`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui appellerait le programme dans son propre processus ne vérifierait pas que la mesure
      suit les sous-processus, ce qui a rendu la première mesure aveugle (1,9 % au lieu de 61,3 %, 01-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return EPREUVE.format(appels=appels)


def fabriquer(dossier, appels=TOUS):
    """Fabrique le dépôt minuscule dans `dossier` et rend sa racine.

    ① RÔLE — Un dépôt dont on connaît la bonne réponse.
    ② CONTEXTE D'APPEL — Chaque cas, une fois.
    ③ ENTRÉE — `dossier` : un dossier vide · `appels` : ce que son épreuve appelle.
    ④ CONDITIONS D'ENTRÉE — Le dossier existe.
    ⑤ SORTIE — UNE valeur : le chemin de la racine (`<dossier>/depot`).
      [rend: 1]
    ⑥ TRAITEMENT — tests/LANCEMENT_DES_EPREUVES.json (aucune épreuve déclarée), programmes/CALCUL.py,
      tests/EPREUVE_CALCUL.py, donnees/choix.txt.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le vrai dépôt demande une heure de certification ; ce dépôt, quelques secondes.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    racine = os.path.join(dossier, "depot")
    for d in ("programmes", "tests", "donnees", "gouvernance"):
        os.makedirs(os.path.join(racine, d))
    ecrire(racine, "tests/LANCEMENT_DES_EPREUVES.json", '{"epreuves": {}}\n')
    ecrire(racine, "programmes/CALCUL.py", CALCUL)
    ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve(appels))
    ecrire(racine, "donnees/choix.txt", "1\n")
    return racine


def ecrire(racine, chemin, contenu):
    """Écrit `contenu` dans `racine/chemin`, en créant le dossier.

    ① RÔLE — Une écriture en une ligne.
    ② CONTEXTE D'APPEL — `fabriquer` et les cas.
    ③ ENTRÉE — `racine` · `chemin` relatif · `contenu` : du texte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a = os.path.join(racine, chemin)
    os.makedirs(os.path.dirname(a), exist_ok=True)
    with open(a, "w", encoding="utf-8") as f:
        f.write(contenu)


def lire(racine, chemin):
    """Rend le texte de `racine/chemin`, ou une chaîne vide s'il n'existe pas.

    ① RÔLE — Lire le rapport ou la référence.
    ② CONTEXTE D'APPEL — Les cas.
    ③ ENTRÉE — `racine` · `chemin`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    a = os.path.join(racine, chemin)
    return open(a, encoding="utf-8").read() if os.path.exists(a) else ""


def certifier(certificateur, racine, *options):
    """Lance le certificateur sur `racine` et rend son code de sortie.

    ① RÔLE — Faire juger le dépôt minuscule par le certificateur (le vrai, ou une copie sabotée).
    ② CONTEXTE D'APPEL — Les cas, une à trois fois chacun.
    ③ ENTRÉE — `certificateur` : le chemin du programme · `racine` · `options` : par exemple `--ecrire-la-reference`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie (99 si le certificateur dépasse 900 secondes).
      [rend: 1]
    ⑥ TRAITEMENT — un sous-processus, par le même Python que ces épreuves.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le même Python : quand le certificateur rejoue ces épreuves, sa mesure suit le certificateur éprouvé.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus, qui écrit le rapport (et la référence) dans `racine`.
    ⑪ TERMINAISON — Rend la main ; le processus est borné à 900 secondes.
      [sort: non]
    """
    try:
        return subprocess.run([sys.executable, certificateur, racine] + list(options), capture_output=True, text=True,
                              timeout=900).returncode
    except subprocess.TimeoutExpired:
        return 99


def saboter_le_certificateur(tmp, certificateur, remplacements):
    """Écrit dans `tmp` une copie du certificateur où chaque texte ancien est remplacé, et rend son chemin.

    ① RÔLE — Fabriquer un certificateur fautif.
    ② CONTEXTE D'APPEL — S5, S6, S16 et chaque sabotage de `--saboter`.
    ③ ENTRÉE — `tmp` : un dossier · `certificateur` : le programme à copier · `remplacements` : (ancien, nouveau).
    ④ CONDITIONS D'ENTRÉE — Chaque texte ancien est présent exactement une fois.
    ⑤ SORTIE — UNE valeur : le chemin de la copie.
      [rend: 1]
    ⑥ TRAITEMENT — remplacer, après avoir compté.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sabotage qui ne s'applique plus laisserait passer le vrai certificateur pour le faux : il lève.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError`.
      [sort: non]
    """
    t = open(certificateur, encoding="utf-8").read()
    for ancien, nouveau in remplacements:
        if t.count(ancien) != 1:
            raise ValueError(f"le sabotage ne s'applique plus ({t.count(ancien)} fois) : {ancien[:60]}")
        t = t.replace(ancien, nouveau)
    chemin = os.path.join(tmp, "CERTIFIER_SABOTE.py")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(t)
    return chemin


AVEUGLE = [
    ('env = dict(os.environ, COVERAGE_PROCESS_START=reg, CERTIF_MANIFESTES=os.path.join(sonde, "manifestes"))',
     'env = {k: v for k, v in os.environ.items() if not k.startswith("COVERAGE")}; '
     'env["CERTIF_MANIFESTES"] = os.path.join(sonde, "manifestes")'),
    ('env = dict(os.environ, COVERAGE_PROCESS_START=reglages, CERTIF_MANIFESTES=manifestes,',
     'env = dict({k: v for k, v in os.environ.items() if not k.startswith("COVERAGE")}, CERTIF_MANIFESTES=manifestes,'),
]
CREDULE = [("if rel not in reels or vus.get(f) != empreintes[rel]:", "if rel not in reels:")]


def base(tmp, cert, appels=TOUS):
    """Fabrique le dépôt minuscule, y écrit la référence, et rend (racine, code de l'écriture).

    ① RÔLE — Le point de départ commun des cas.
    ② CONTEXTE D'APPEL — Les cas.
    ③ ENTRÉE — `tmp` · `cert` : le certificateur · `appels`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la racine, le code de l'écriture de la référence (0 attendu).
      [rend: 2]
    ⑥ TRAITEMENT — `fabriquer`, puis `certifier --ecrire-la-reference`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le dépôt minuscule et sa référence.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    racine = fabriquer(tmp, appels)
    return racine, certifier(cert, racine, "--ecrire-la-reference")


def cas(nom, cert, tmp):
    """Joue le cas `nom` avec le certificateur `cert` et rend (réussi, détail).

    ① RÔLE — Le corps des vingt-huit épreuves Z0, S1 à S27.
    ② CONTEXTE D'APPEL — `main`, une fois par cas, et une fois par sabotage.
    ③ ENTRÉE — `nom` : « Z0 », « S1 »… · `cert` : le certificateur · `tmp` : un dossier vide, propre au cas.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : vrai si le certificateur a rendu ce qui est attendu, et une phrase qui dit ce qu'il a rendu.
      [rend: 2]
    ⑥ TRAITEMENT — voir la liste en tête du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — Le cas S6 attend une épreuve qui dort 60 secondes ; le certificateur saboté l'arrête à 5.
    ⑩ EFFET — Écrit dans `tmp`, lance le certificateur.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if nom == "S5":
        cert = saboter_le_certificateur(tmp, cert, AVEUGLE)
        racine = fabriquer(tmp)
        c = certifier(cert, racine, "--ecrire-la-reference")
        return c == 2, f"écriture de la référence par un certificateur aveugle : {c} (attendu 2)"
    if nom == "S16":
        cert = saboter_le_certificateur(tmp, cert, CREDULE)
        racine = fabriquer(tmp)
        c = certifier(cert, racine, "--ecrire-la-reference")
        return c == 2, f"écriture de la référence par un certificateur crédule : {c} (attendu 2)"
    if nom == "S6":
        cert = saboter_le_certificateur(tmp, cert, [("DUREE_MAX_EPREUVE = 1500", "DUREE_MAX_EPREUVE = 5")])
    if nom == "S3":
        racine = fabriquer(tmp)
        c = certifier(cert, racine)
        return c == 2, f"sans référence : {c} (attendu 2)"
    if nom == "S12":
        racine, e = base(tmp, cert, "C.double(2); C.triple(2); C.signe(3)")
        ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve("C.double(2); C.triple(2); C.signe(-3)"))
        c = certifier(cert, racine)
        return e == 0 and c == 1, f"référence {e}, échange à nombres égaux : {c} (attendu 0 puis 1)"
    if nom == "S15":
        racine, e = base(tmp, cert, "C.double(2); C.signe(3); C.signe(-3); "
                                    "open('donnees/choix.txt').read().strip() == '1' and C.triple(2)")
        ecrire(racine, "donnees/choix.txt", "0\n")
        c = certifier(cert, racine)
        derive = "DÉRIVE DE MESURE" in lire(racine, RAPPORT)
        return e == 0 and c == 0 and derive, f"référence {e}, donnée changée : {c}, dérive dite : {derive} (attendu 0, 0, vrai)"
    if nom == "S14":
        racine = fabriquer(tmp)
        ecrire(racine, "tests/OUTIL_COMMUN.py", f"APPELS = {TOUS!r}\n")
        ecrire(racine, "tests/EPREUVE_A.py", "import OUTIL_COMMUN\n" + epreuve(TOUS).replace(repr(TOUS), "OUTIL_COMMUN.APPELS"))
        ecrire(racine, "tests/EPREUVE_B.py", epreuve(TOUS) + "print('voir aussi EPREUVE_A')\n")
        e = certifier(cert, racine, "--ecrire-la-reference")
        c = certifier(cert, racine)
        r = lire(racine, RAPPORT)
        joue, outil = "| tests/EPREUVE_A.py |" in r, "tests/OUTIL_COMMUN.py" in r
        return (e == 0 and c == 0 and joue and not outil,
                f"référence {e}, certification {c}, A jouée : {joue}, outil joué : {outil} (attendu 0, 0, vrai, faux)")
    if nom in ("S17", "S18"):
        racine, e = base(tmp, cert)
        ecrire(racine, "programmes/OUTIL.py", "import sys\n\nif len(sys.argv) > 1 and sys.argv[1] == 'epreuves':\n"
                                              "    sys.exit(1)\n")
        if nom == "S18":
            ecrire(racine, "tests/LANCEMENT_DES_EPREUVES.json",
                   '{"epreuves": {"programmes/OUTIL.py": {"dossier": ".", "arguments": ["epreuves"]}}}\n')
        c = certifier(cert, racine)
        attendu = 2 if nom == "S17" else 1
        return e == 0 and c == attendu, f"référence {e}, certification {c} (attendu 0 puis {attendu})"
    if nom == "S19":
        racine, e = base(tmp, cert)
        ecrire(racine, "tests/LANCEMENT_DES_EPREUVES.json", '{"epreuves": ')
        c = certifier(cert, racine)
        dit = "illisible" in lire(racine, RAPPORT)
        return e == 0 and c == 2 and dit, f"référence {e}, table illisible : {c}, dit au rapport : {dit} (attendu 0, 2, vrai)"
    if nom == "S20":
        racine = fabriquer(tmp)
        ecrire(racine, "programmes/AUTRE.py", "def autre():\n    return 1\n")
        e = certifier(cert, racine, "--ecrire-la-reference")
        ecrire(racine, "programmes/AUTRE.py", "def autre(:\n    return 1\n")
        c = certifier(cert, racine)
        r = lire(racine, RAPPORT)
        dit, disparu = "AUTRE.py" in r and "CERTIFICATION IMPOSSIBLE" in r, "disparu" in r
        return (e == 0 and c == 2 and dit and not disparu,
                f"référence {e}, programme jamais exécuté puis cassé : {c}, dit au rapport : {dit}, dit disparu : "
                f"{disparu} (attendu 0, 2, vrai, faux)")
    if nom == "S21":
        racine, e = base(tmp, cert)
        ecrire(racine, "tests/EPREUVE_CASSEE.py", "import sys\nsys.exit(0\n")
        c = certifier(cert, racine)
        dit = "EPREUVE_CASSEE.py" in lire(racine, RAPPORT)
        return e == 0 and c == 2 and dit, f"référence {e}, épreuve cassée : {c}, dite au rapport : {dit} (attendu 0, 2, vrai)"
    if nom in ("S22", "S23", "S24", "S25", "S27"):
        racine = fabriquer(tmp)
        ecrire(racine, "programmes/AUTRE.py", "import os\n\n\ndef jamais():\n    return os.sep\n")
        e = certifier(cert, racine, "--ecrire-la-reference")
        attendu = {"S22": 1, "S23": 1, "S24": 2, "S25": 0, "S27": 1}[nom]
        if nom == "S22":
            ecrire(racine, "programmes/AUTRE.py", "")
        elif nom == "S23":
            ecrire(racine, "programmes/AUTRE.py", "\n\ndef jamais():\n    return os.sep\n")
        elif nom == "S24":
            with open(os.path.join(racine, "programmes", "AUTRE.py"), "wb") as f:
                f.write(b"# \xe9t\xe9\nimport os\n\n\ndef jamais():\n    return os.sep\n")
        elif nom == "S27":
            os.remove(os.path.join(racine, "programmes", "AUTRE.py"))
        else:
            ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve(TOUS + "; import AUTRE; AUTRE.jamais()"))
        c = certifier(cert, racine)
        dit = nom != "S24" or "que Python ne sait pas lire" in lire(racine, RAPPORT)
        return (e == 0 and c == attendu and dit,
                f"référence {e}, certification {c}" + (f", « que Python ne sait pas lire » au rapport : {dit}" if nom == "S24" else "")
                + f" (attendu 0, {attendu}" + (", vrai)" if nom == "S24" else ")"))
    if nom == "S26":
        racine, e = base(tmp, cert)
        ecrire(racine, "tests/EPREUVE_GIT.py", "import os, sys\n"
               "sys.exit(0 if os.environ.get('GIT_CONFIG_GLOBAL') == os.devnull and os.environ.get('GIT_CONFIG_NOSYSTEM') == '1' else 1)\n")
        c = certifier(cert, racine)
        return e == 0 and c == 0, f"référence {e}, certification {c} (attendu 0, 0)"
    if nom == "S13":
        racine = fabriquer(tmp)
        ecrire(racine, "tests/EPREUVE_B.py", epreuve(TOUS))
        e = certifier(cert, racine, "--ecrire-la-reference")
        os.remove(os.path.join(racine, "tests", "EPREUVE_B.py"))
        c = certifier(cert, racine)
        return e == 0 and c == 1, f"référence {e}, épreuve disparue : {c} (attendu 0 puis 1)"
    racine, e = base(tmp, cert)
    if e != 0:
        return False, f"la référence du dépôt minuscule ne s'écrit pas : {e}"
    if nom == "Z0":
        c = certifier(cert, racine)
        dit = "VERSION CERTIFIÉE" in lire(racine, RAPPORT)
        return c == 0 and dit, f"certification : {c}, « VERSION CERTIFIÉE » au rapport : {dit} (attendu 0, vrai)"
    attendu, apres = {"S1": 1, "S2": 1, "S4": 2, "S6": 1, "S7": 1, "S8": 0, "S10": 1, "S11": 1}.get(nom), ""
    if nom == "S1":
        ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve("assert C.double(2) == 5"))
    elif nom == "S2":
        ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve("C.double(2); C.signe(3); C.signe(-3)"))
    elif nom == "S4":
        ecrire(racine, "programmes/EPREUVES_X.py", "import sys\nsys.exit(0)\n")
    elif nom == "S6":
        ecrire(racine, "tests/EPREUVE_LENTE.py", "import time\ntime.sleep(60)\n")
    elif nom == "S7":
        ecrire(racine, "programmes/NOUVEAU.py", "def oubliee():\n    return 0\n")
    elif nom == "S8":
        ecrire(racine, "programmes/CALCUL.py", "# deux lignes\n# ajoutées\n" + CALCUL)
    elif nom == "S10":
        ecrire(racine, "tests/EPREUVE_CALCUL.py", LEURRE)
    elif nom == "S11":
        ecrire(racine, "programmes/CALCUL.py", CALCUL.split("\n\n\ndef signe")[0] + "\n")
        ecrire(racine, "programmes/lib/SIGNE.py", "def signe(x):\n    if x >= 0:\n        return 1\n    return -1\n")
        ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve("C.double(2); C.triple(2)"))
    elif nom == "S9":
        avant = lire(racine, REFERENCE)
        ecrire(racine, "tests/EPREUVE_CALCUL.py", epreuve("C.double(2); C.signe(3); C.signe(-3)"))
        c1 = certifier(cert, racine, "--ecrire-la-reference")
        garde = lire(racine, REFERENCE) == avant
        c2 = certifier(cert, racine, "--ecrire-la-reference", "--accord", "essai du 02-10-2026")
        porte = lire(racine, REFERENCE) != avant and "essai du 02-10-2026" in lire(racine, REFERENCE)
        return (c1 == 1 and garde and c2 == 0 and porte,
                f"sans accord : {c1}, référence gardée : {garde} ; avec accord : {c2}, accord porté : {porte} "
                "(attendu 1, vrai, 0, vrai)")
    c = certifier(cert, racine)
    if nom == "S6":
        lente = [l for l in lire(racine, RAPPORT).splitlines() if l.startswith("| tests/EPREUVE_LENTE.py |")]
        apres = f", ligne du rapport : {lente[0] if lente else 'absente'}"
        return c == 1 and bool(lente) and "| 124 |" in lente[0], f"certification : {c} (attendu 1, code 124){apres}"
    return c == attendu, f"certification : {c} (attendu {attendu})"


NOMS = ["Z0"] + [f"S{i}" for i in range(1, 28)]

# Chaque correction du certificateur, retirée une à la fois : (nom, [(ancien, nouveau)], cas qui DOIT changer de résultat).
SABOTAGES = [
    ("crédit sans empreinte", CREDULE, "S10"),
    ("programmes/ sans sous-dossiers",
     [("                trouves[os.path.relpath(a, racine)] = a",
       "                trouves.update({os.path.relpath(a, racine): a} if d == os.path.join(racine, \"programmes\") else {})")],
     "S11"),
    ("comparaison par totaux et non par texte",
     [("pires = [t for t, n in m[cle].items() if n > r.get(cle, {}).get(t, 0)]",
       "pires = [\"total\"] if sum(m[cle].values()) > sum(r.get(cle, {}).values()) else []")], "S12"),
    ("outil reconnu à son nom dans un texte",
     [("if f[:-3] in importes:", "if any(f[:-3] in t for g, t in textes.items() if g != f):")], "S14"),
    ("épreuve disparue non vue", [("if json.dumps(l) not in joues:", "if False:")], "S13"),
    ("dérive de mesure non reconnue",
     [("if reculs_mesure and not rouges and not disparues and reference.get(\"empreinte_du_code\") == empreinte:",
       "if False:")], "S15"),
    ("épreuve non déclarée tolérée", [("if not calibree or non_declarees:", "if not calibree:")], "S4"),
    ("référence absente tolérée", [("if reference is None and not ecrire:", "if False:")], "S3"),
    ("table de lancement illisible non rattrapée",
     [('lancements, non_declarees = [], [f"épreuves illisibles ({type(e).__name__}: {e})"]', "raise")], "S19"),
    ("épreuve illisible non rattrapée", [("except (OSError, ValueError, KeyError, TypeError, SyntaxError) as e:",
                                         "except (OSError, ValueError, KeyError, TypeError) as e:")], "S21"),
    ("programme illisible pris pour disparu", [("        if illisibles or non_mesures:\n", "        if False:\n")], "S20"),
    ("programme illisible par Python non vu",
     [("        illisibles = programmes_illisibles(copie)\n", "        illisibles = []\n")], "S24"),
    ("épreuves jouées avec la configuration Git de la machine",
     # le sabotage ÔTE l'isolement, au lieu de seulement ne plus le poser : quand la certification rejoue ces
     # épreuves, l'isolement est déjà dans l'environnement hérité, et le sabotage restait vert (02-10-2026, 20h06)
     [('               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")',
       '               GIT_CONFIG_GLOBAL="", GIT_CONFIG_NOSYSTEM="")')], "S26"),
    ("ligne non éprouvée supprimée tolérée (programme vidé)", [("        if otees:\n", "        if False:\n")], "S22"),
    ("ligne non éprouvée supprimée tolérée (une ligne en moins)", [("        if otees:\n", "        if False:\n")], "S23"),
    ("programme non éprouvé supprimé toléré", [("        if nom not in sources and r.get(\"lignes_non_examinees\"):\n",
                                                "        if False:\n")], "S27"),
    ("épreuve reconnue à son seul nom", [("or modes_d_epreuve(a)))", "or False))")], "S17"),
    ("référence qui recule écrite sans accord",
     [("elif reference is not None and reculs and not accord:", "elif False:")], "S9"),
    ("une ligne non examinée de plus tolérée",
     [("if pires:", "if False:")], "S12"),
]


def jouer(travail):
    """Joue un travail (cas seul, ou cas avec un certificateur saboté) dans son dossier jetable et rend son résultat.

    ① RÔLE — Une unité de travail pour l'exécution en parallèle.
    ② CONTEXTE D'APPEL — `main`, par un groupe de quatre fils.
    ③ ENTRÉE — `travail` : (nom du cas, nom du sabotage ou None, remplacements).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — QUATRE valeurs : le nom du cas, le nom du sabotage (None sans sabotage), réussi, le détail ; un sabotage
      qui ne s'applique plus rend « réussi » à None.
      [rend: 4]
    ⑥ TRAITEMENT — un dossier jetable, le certificateur (saboté si demandé), `cas`, effacement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit puis efface un dossier jetable.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    nom, sabotage, remplacements = travail
    tmp = tempfile.mkdtemp(prefix="epreuve_certif_")
    try:
        cert = CERTIFICATEUR
        if sabotage:
            try:
                cert = saboter_le_certificateur(tmp, CERTIFICATEUR, remplacements)
            except ValueError as e:
                return nom, sabotage, None, str(e)
            os.makedirs(os.path.join(tmp, "cas"))
            ok, detail = cas(nom, cert, os.path.join(tmp, "cas"))
            return nom, sabotage, ok, detail
        try:
            ok, detail = cas(nom, cert, tmp)
        except ValueError as e:     # S5, S6, S16 sabotent le certificateur eux-mêmes : un sabotage périmé se dit
            return nom, "interne au cas " + nom, None, str(e)
        return nom, None, ok, detail
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    """Joue les vingt-huit cas, puis, avec --saboter, chaque sabotage ; rend 0, 1 ou 2.

    ① RÔLE — Le programme entier (voir la fiche en tête).
    ② CONTEXTE D'APPEL — La ligne de commande ; le certificateur, à chaque certification.
    ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Le module `coverage` est installé.
    ⑤ SORTIE — Le code de sortie, 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — les cas en parallèle, une ligne par cas ; les sabotages : le cas visé doit ÉCHOUER.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance le certificateur des dizaines de fois sur des dépôts minuscules.
    ⑪ TERMINAISON — Rend la main au bloc de lancement.
      [sort: non]
    """
    if not os.path.isfile(CERTIFICATEUR):
        print(f"ÉPREUVES IMPOSSIBLES — certificateur introuvable : {CERTIFICATEUR}")
        return 2
    travaux = [(n, None, None) for n in NOMS]
    if "--saboter" in sys.argv:
        travaux += [(c, s, r) for s, r, c in SABOTAGES]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as groupe:
        resultats = list(groupe.map(jouer, travaux))
    echecs, casses = 0, 0
    for nom, sabotage, ok, detail in resultats:
        if sabotage is None:
            print(f"{'✅' if ok else '❌'} {nom} — {detail}")
            echecs += not ok
        elif ok is None:
            print(f"⛔ sabotage « {sabotage} » — {detail}")
            casses += 1
        else:
            print(f"{'✅' if not ok else '❌'} sabotage « {sabotage} » : {nom} {'rougit' if not ok else 'RESTE VERT'} — {detail}")
            echecs += bool(ok)
    if casses:
        print(f"VERDICT : {casses} sabotage(s) ne s'appliquent plus — épreuves non concluantes")
        return 2
    print("VERDICT : tout est conforme" if not echecs else f"VERDICT : {echecs} échec(s)")
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
