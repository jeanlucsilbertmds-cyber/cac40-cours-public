#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CONTROLE_DE_LIVRAISON_SUR_GITHUB — Mer 25-11-2026 (Paris). Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. Décision de Jean-Luc du 25-11-2026 à 15h21 (BACKLOG A-995) : le contrôle final des livraisons
(programmes/CONTROLER_MA_LIVRAISON.py) se joue sur GitHub, au circuit des épreuves longues, sous le code « Livraison »
de tests/LANCEMENT_DES_EPREUVES.json. Cette épreuve prouve, sans GitHub et sans aucune donnée de cours, que :
le code est dans la table et le joueur le refuse s'il en est absent ; programmes/CONTROLER_LA_LIVRAISON_SUR_GITHUB.py
rend à la copie jouée un dépôt git (HEAD sur la pointe, origin/main) puis lance le contrôle avec « --attendu=livraison »,
et dit VERT, ROUGE ou IMPOSSIBLE ; le joueur (tests/outils/jouer_une_epreuve_longue.py) range dans RESULTAT.json le
verdict, la pointe et l'empreinte ; « --juger » refuse un résultat d'une autre pointe.
DEPUIS LE RELU DE COWORK DU 25-11-2026 (N-43, « 9 sabotages sur 10 vivent ») et le superviseur R-759 (« 10 mordent sur
10 est un compte, pas une propriété ») : en plus des sabotages écrits à la main, les sabotages des FONCTIONS-GARDES sont
FABRIQUÉS par programme à partir du code (`sabotages_fabriques`) : chaque `if` dont le corps refuse, et chaque terme
d'un « or » dans un tel `if`, devient `False` ; chacun doit faire tomber un cas, sauf ceux de REDONDANTS, dont chaque
raison est écrite pour le relecteur. Une garde ajoutée dans ces fonctions est donc éprouvée sans rien écrire ici.
DEPUIS LE RELU DE COWORK DU 25-11-2026 À 17h17 (N-50 : la garde qui ACCEPTE, « code == 0 », pouvait sauter sans
qu'un cas tombe ; N-51 : fullmatch → match et programmes/ retiré du diff, muets) et le superviseur R-759 de 18h08 :
les fonctions-gardes sont une PROPRIÉTÉ (`gardes` : toutes celles de l'enveloppe sauf `main`, et `lire_le_detail`) ;
la fabrication voit aussi l'ACCEPTATION par sa forme (chaque terme d'un « and » d'un `if` qui accepte, et d'un
`return` prédicat, devient `True` ; un court-circuit recopie le `return` d'acceptation avant la première garde) et
chaque `re.fullmatch` devient `re.match` ; un sabotage nommé dans ATTENDUS ne mord que par le cas qui le vise.
Le contrôle réel n'est PAS joué ici (il lirait tout donnees/) : un contrôle de remplacement, posé dans chaque copie
fabriquée, vérifie ce que le vrai exige (git, HEAD, origin/main, options) et écrit sa ligne de contrôle au format que
lit la fonction du vrai contrôle (`_marqueur_de_queue`, chargée depuis la racine éprouvée).

① RÔLE — Jouer les cas C1 à C28 ; avec « --saboter », jouer aussi les sabotages écrits (S1 à S13, A6) et les
  sabotages fabriqués des fonctions-gardes : chacun doit faire rougir au moins un cas (le cas nommé dans ATTENDUS,
  s'il y est), sinon l'épreuve est une décoration (R-731) — sauf un sabotage fabriqué inscrit dans REDONDANTS avec sa
  raison.
② CONTEXTE D'APPEL — À la main ; la certification de nuit (toute épreuve de tests/, avec la racine, puis
  « --saboter »).
③ ENTRÉE — `<racine>` (le dépôt éprouvé), `--saboter` facultatif.
④ CONDITIONS D'ENTRÉE — git est installé ; la racine porte les programmes nommés dans PIECES.
⑤ SORTIE — Le code de sortie : 0 tout est juste ; 1 un cas faux, un sabotage qui ne mord pas, ou un sabotage déclaré
  redondant qui mord (la liste ment) ; 2 l'épreuve n'a pas pu tourner (pièce absente, motif de sabotage introuvable,
  fonction-garde absente, entrée de REDONDANTS ou d'ATTENDUS qui ne désigne plus aucun sabotage : R-734).
  [rend: 1]
⑥ TRAITEMENT — `fabriquer` : une origine git à deux commits, son clone (refs/remotes/origin/main, HEAD détachée sur le
  second commit : « le clone du circuit »), une copie sans .git avec les pièces et le contrôle de remplacement ;
  `cas` : chaque cas sur une copie neuve ; `saboter` : chaque sabotage écrit remplace un texte UNIQUE d'une pièce de
  la copie, puis rejoue les cas ; `sabotages_fabriques` lit l'arbre syntaxique des fonctions-gardes (`gardes`).
⑦ UNITÉ — —
⑧ POURQUOI — R-731 (tout code passe des épreuves avec sabotages) ; consigne du 25-11-2026 : « code absent du JSON →
  refusé ; résultat sur une autre pointe → refusé ».
⑨ CE QUI CLOCHE — Le clone est fait par « git clone » et non par actions/checkout : que le clone de GitHub porte
  refs/remotes/origin/main n'est pas prouvé ici (THÉORIQUE — premier essai réel sur GitHub). Le vrai contrôle n'est
  pas joué.
⑩ EFFET — Écrit dans un dossier temporaire, effacé à la fin.
⑪ TERMINAISON — Rend la main ; chaque processus est borné à DELAI secondes.
  [sort: oui]
"""
import ast
import builtins
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ENVELOPPE = os.path.join("programmes", "CONTROLER_LA_LIVRAISON_SUR_GITHUB.py")
JOUEUR = os.path.join("tests", "outils", "jouer_une_epreuve_longue.py")
PIECES = (ENVELOPPE, JOUEUR, os.path.join("programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py"),
          os.path.join("programmes", "CERTIFIER_LA_VERSION.py"), os.path.join("tests", "outils", "jouer_une_part.py"),
          os.path.join("tests", "LANCEMENT_DES_EPREUVES.json"))
VRAI_CONTROLE = os.path.join("programmes", "CONTROLER_MA_LIVRAISON.py")
DELAI = 60
EMPREINTE = "0123456789abcdef"
# Le contrôle de remplacement : exige ce que le vrai exige (dépôt git à la racine de la note, HEAD, origin/main,
# historique lisible, options de l'usage local, et un INDEX égal à HEAD — le vrai lit l'état du dépôt par git, qui passe
# par l'index : sans « read-tree », tout fichier paraîtrait effacé ; M2 du RELU de Cowork du 25-11-2026) ; refuse une
# note qui porte REFUSER ; rend 0 SANS ligne pour SANSLIGNE.
REMPLACANT = '''import importlib.util, os, subprocess, sys
_s = importlib.util.spec_from_file_location("VRAI", os.environ["VRAI_CONTROLE_POUR_L_EPREUVE"])
_v = importlib.util.module_from_spec(_s); _s.loader.exec_module(_v)
_marqueur_de_queue = _v._marqueur_de_queue
if __name__ == "__main__":
    note = sys.argv[1]
    racine = os.path.dirname(os.path.dirname(os.path.abspath(note)))
    if sys.argv[2:] != ["--attendu=livraison"]:
        print("REMPLACANT options", sys.argv[2:]); sys.exit(1)
    for a in (["rev-parse", "--verify", "HEAD^{commit}"], ["rev-parse", "--verify", "refs/remotes/origin/main"],
              ["log", "--all", "--oneline"], ["cat-file", "-e", "HEAD:LISEZ_MOI.txt"],
              ["diff", "--cached", "--quiet", "HEAD"]):
        if subprocess.run(["git", "-C", racine] + a, capture_output=True).returncode != 0:
            print("REMPLACANT git refuse", a); sys.exit(1)
    t = open(note, encoding="utf-8").read()
    if "REFUSER" in t:
        print("REMPLACANT livraison refusee"); sys.exit(1)
    if "SANSLIGNE" not in t:
        open(note, "w", encoding="utf-8").write(t.rstrip("\\n") + "\\n\\n<!-- CONTROLE %s · 2026-11-25 15:00 Paris -->\\n")
    sys.exit(0)
''' % EMPREINTE
# Chaque sabotage : (nom, pièce, texte exact et unique, remplacement, ce qu'il retire).
SABOTAGES = (
    ("S1", ENVELOPPE, "    if tete != pointe:\n", "    if False:\n", "la porte de la pointe du clone"),
    ("S2", ENVELOPPE, '    if r.get("pointe_jouee") != pointe:\n', "    if False:\n",
     "le refus d'un résultat d'une autre pointe"),
    ("S3", ENVELOPPE, '    elif os.path.lexists(os.path.join(copie, ".git")):\n', "    elif False:\n",
     "le refus d'une copie qui porte déjà un .git"),
    ("S4", JOUEUR, "    env[RESULTAT_DE_L_EPREUVE] = detail\n", "    pass\n", "le nom du détail donné à l'épreuve"),
    ("S5", JOUEUR, "    lire_le_detail(detail, resultat)\n", "    pass\n", "le détail rangé dans RESULTAT.json"),
    ("S6", ENVELOPPE, "    if code == 0 and ligne:\n", "    if code == 0:\n", "l'exigence de la ligne de contrôle"),
    ("S7", ENVELOPPE, "detail.update(verdict=ROUGE,", "detail.update(verdict=VERT,", "le verdict ROUGE d'un refus"),
    ("S8", ENVELOPPE, 'OPTIONS = ("--attendu=livraison",)', "OPTIONS = ()", "les options de l'usage local"),
    ("S9", ENVELOPPE, 'if r.get("code_epreuve") != "Livraison":', 'if r.get("code_epreuve") != "Autre":',
     "le code de l'épreuve jugée"),
    ("S10", ENVELOPPE, '    git(env, copie, "rev-parse", "--verify", "refs/remotes/origin/main^{commit}")\n', "",
     "la relecture d'origin/main dans la copie"),
    ("S11", ENVELOPPE, "    if ecart.returncode != 0:\n", "    if False:\n",
     "le refus d'une copie dont le disque diffère de la pointe (superviseur R-759, point 3)"),
    # RELU de Cowork du 25-11-2026 : M2 (l'index lu de HEAD) n'est pas une garde « if » ; N-44 : la définition unique
    ("S12", ENVELOPPE, '    git(env, copie, "read-tree", "HEAD")\n', "", "l'index lu de HEAD (M2 de Cowork)"),
    ("S13", ENVELOPPE, "    return type(valeur) is int and valeur == 0\n", "    return valeur == 0\n",
     "le refus d'un code de sortie booléen (N-44)"),
    # N-51 (X3 de Cowork), A6 du superviseur R-759 de 18h08 : le diff ne regarde plus programmes/ — cas C27
    ("A6", ENVELOPPE, '"diff", "--quiet", "HEAD", "--", "programmes/", "echanges/"',
     '"diff", "--quiet", "HEAD", "--", "echanges/"', "programmes/ dans la comparaison du disque à la pointe (N-51)"),
)
# LES FONCTIONS-GARDES sont une PROPRIÉTÉ, plus une liste (superviseur R-759 du 25-11-2026 à 18h08, sur N-50, forme
# recommandée, point 1) : toutes les fonctions de l'enveloppe sauf `main`, plus `lire_le_detail` du joueur — `gardes`.
# Leurs sabotages sont fabriqués par `sabotages_fabriques`, jamais écrits à la main.
GARDE_DU_JOUEUR = (JOUEUR, "lire_le_detail")
# LES SABOTAGES FABRIQUÉS QUI NE PEUVENT PAS MORDRE, chacun avec sa raison (à relire par le relecteur). La clé est
# « fonction · condition retirée », telle que `sabotages_fabriques` la nomme. Mesurés le 25-11-2026 : chacun survit aux
# cas C1-C23, et chacun de ces cas montre que le refus a lieu quand même (C5, C20, C21, C22, C23) ; les deux entrées
# « match au lieu de fullmatch » de jouer_le_controle s'y ajoutent le 25-11-2026 au soir (A5 du superviseur de 18h08).
REDONDANTS = {
    "rendre_le_depot_git · git(env, copie, 'rev-parse', '--verify', 'HEAD^{commit}') != pointe":
        "deux lignes plus haut, « update-ref --no-deref HEAD <pointe> » vient de poser HEAD sur la pointe, et un échec "
        "de git lève déjà : cette relecture ne peut différer que si git ment (garde de défense, sans cas possible)",
    "jouer_le_controle · not re.fullmatch(POINTE, pointe)":
        "M10 de Cowork : une pointe vide ou mal formée ne peut pas égaler HEAD du clone ; `rendre_le_depot_git` refuse "
        "(« le clone n'est pas à la pointe jouée ») et le code reste 2 — cas C22",
    "jouer_le_controle · not source":
        "M1 de Cowork : sans GITHUB_WORKSPACE, le second terme cherche « .git » dans le dossier courant ; l'épreuve "
        "lance l'enveloppe dans un dossier sans .git, il refuse donc à sa place — cas C5",
    "jouer_le_controle · not os.path.isdir(os.path.join(source, '.git'))":
        "M1 de Cowork : un GITHUB_WORKSPACE qui n'est pas un dépôt git fait tomber « git rev-parse » dans "
        "`rendre_le_depot_git` (OSError), rendu 2 — cas C23",
    "jouer_le_controle · not os.path.isfile(note)":
        "une note absente fait tomber la lecture de son empreinte (open : OSError), rendue 2 — cas C20",
    "jouer_le_controle · not os.path.isfile(os.path.join(copie, CONTROLE))":
        "M6 de Cowork : un contrôle absent fait tomber `charger` (FileNotFoundError, une OSError), rendu 2 — cas C21",
    # A5 du superviseur R-759 de 18h08 (fullmatch → match dans jouer_le_controle) : « probablement REDONDANTS ».
    "jouer_le_controle · match au lieu de fullmatch n°1 · re.fullmatch(POINTE, pointe)":
        "ne change que le champ « pointe » du détail quand POINTE_JOUEE a 40 hexadécimaux puis un suffixe ; le "
        "résultat reste IMPOSSIBLE (code 2), car `rendre_le_depot_git` refuse une pointe qui n'est pas HEAD du clone ; "
        "« --juger » ne lit pas ce champ (point 4 du superviseur R-759) — cas C3, C22",
    "jouer_le_controle · match au lieu de fullmatch n°2 · re.fullmatch(POINTE, pointe)":
        "une POINTE_JOUEE de 40 hexadécimaux suivis d'un suffixe passe ce test mais ne peut pas égaler HEAD du clone : "
        "`rendre_le_depot_git` refuse (« le clone n'est pas à la pointe jouée »), code 2 — même raison que M10, cas C3",
}
# LE CAS QUI DOIT TOMBER, par sabotage (superviseur R-759 de 18h08, « SABOTAGES EXIGÉS (le cas qui doit tomber) ») :
# un sabotage nommé ici ne « mord » que si l'un de ces cas tombe. Clé : le nom du sabotage écrit, ou la clé du
# sabotage fabriqué telle que `sabotages_fabriques` l'écrit.
ATTENDUS = {
    "A6": ("C27",),
    "jouer_le_controle · accepte · code == 0": ("C24",),                    # A1
    "jouer_le_controle · accepte · ligne": ("C7",),                         # A2
    "jouer_le_controle · court-circuit": ("C2",),                           # A3
    "contenu_vert · court-circuit": ("C13", "C14", "C15", "C25"),           # A3
    "juger_un_resultat · court-circuit": ("C10",),                          # A3
    "code_de_sortie_nul · court-circuit": ("C15",),                         # A3
    "code_de_sortie_nul · accepte · valeur == 0": ("C25",),                 # A4
    "code_de_sortie_nul · accepte · type(valeur) is int": ("C15",),         # A4
    "contenu_vert · match au lieu de fullmatch n°1 · re.fullmatch('[0-9a-f]{16}', str(d.get('empreinte', '')))":
        ("C26",),                                                           # A5
    "juger_un_resultat · match au lieu de fullmatch n°1 · re.fullmatch(POINTE, pointe or '')": ("C28",),   # A5
}


def remplacer_le_texte_du_noeud(texte, noeud, par):
    """Rend `texte` où le code source du nœud `noeud` est remplacé par `par`.

    ① RÔLE — Poser un sabotage fabriqué exactement à l'endroit d'une condition, sans toucher le reste du fichier
      (commentaires et mise en page compris).
    ② CONTEXTE D'APPEL — `sabotages_fabriques`.
    ③ ENTRÉE — `texte` : le texte entier d'une pièce ; `noeud` : un nœud de l'arbre syntaxique de ce texte (porte
      lineno, col_offset, end_lineno, end_col_offset) ; `par` : le texte qui prend sa place.
    ④ CONDITIONS D'ENTRÉE — `noeud` vient de `ast.parse(texte)`.
    ⑤ SORTIE — UNE valeur : le texte modifié.
      [rend: 1]
    ⑥ TRAITEMENT — les débuts de ligne en OCTETS UTF-8 ; le début et la fin du nœud ; remplacement ; décodage.
    ⑦ UNITÉ — Des octets UTF-8 : les colonnes de `ast` comptent des octets, et les pièces portent des accents.
    ⑧ POURQUOI — Un sabotage fabriqué doit retirer UNE condition et rien d'autre ; `ast.unparse` du fichier entier
      réécrirait tout le fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    octets = texte.encode("utf-8")
    debuts = [0]
    for ligne in octets.split(b"\n"):
        debuts.append(debuts[-1] + len(ligne) + 1)
    i = debuts[noeud.lineno - 1] + noeud.col_offset
    j = debuts[noeud.end_lineno - 1] + noeud.end_col_offset
    return (octets[:i] + par.encode("utf-8") + octets[j:]).decode("utf-8")


def corps_qui_refuse(corps):
    """Dit si le corps d'un `if` REFUSE : il lève, rend 1 ou 2 (seul ou en tête d'un couple), ou écrit une raison.

    ① RÔLE — Reconnaître une garde dans le code, par sa forme, sans liste de lignes.
    ② CONTEXTE D'APPEL — `sabotages_fabriques`.
    ③ ENTRÉE — `corps` : la liste des instructions du corps d'un `if` (nœuds `ast`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si le corps contient un `raise`, un `return` de la constante 1 ou 2 (ou d'un couple
      qui commence par elle), ou une écriture dans un indice « raison » ou « detail_illisible ».
      [rend: 1]
    ⑥ TRAITEMENT — `ast.walk` de chaque instruction.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Définition du superviseur R-759 du 25-11-2026 : « chaque `if <condition>:` dont le corps refuse
      (return 1/2, raise, detail_illisible) ». Les gardes de `jouer_le_controle` écrivent detail["raison"] puis rendent
      2 plus bas : la raison écrite compte comme un refus.
    ⑨ CE QUI CLOCHE — Un refus écrit sous une autre forme (une fonction qui refuse pour lui) n'est pas reconnu : le
      `if` n'est alors pas saboté, et rien ne le dit. Une fonction imbriquée dans le corps serait parcourue aussi.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for instruction in corps:
        for n in ast.walk(instruction):
            if isinstance(n, ast.Raise):
                return True
            if isinstance(n, ast.Return) and n.value is not None:
                v = n.value.elts[0] if isinstance(n.value, ast.Tuple) and n.value.elts else n.value
                if isinstance(v, ast.Constant) and type(v.value) is int and v.value in (1, 2):
                    return True
            if isinstance(n, ast.Assign):
                for c in n.targets:
                    if (isinstance(c, ast.Subscript) and isinstance(c.slice, ast.Constant)
                            and c.slice.value in ("raison", "detail_illisible")):
                        return True
    return False


def acceptation(valeur):
    """Dit si la valeur d'un `return` est une ACCEPTATION, et de quelle forme.

    ① RÔLE — Reconnaître, par sa FORME, un `return` qui accepte (superviseur R-759 du 25-11-2026 à 18h08, N-50, forme
      recommandée, points 2 et 3 : « un corps qui rend la constante 0, ou un couple qui commence par 0 » ; « 0,
      (0, …), True »).
    ② CONTEXTE D'APPEL — `corps_qui_accepte`, `court_circuit`, `sabotages_fabriques`.
    ③ ENTRÉE — `valeur` : le nœud `ast` de la valeur d'un `return`, ou None (un `return` nu).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « constante » (0 ou True), « couple » (un tuple dont le premier élément est la constante
      0), « prédicat » (une expression « and », comme `code_de_sortie_nul`), ou None.
      [rend: 1]
    ⑥ TRAITEMENT — examen de la forme du nœud ; un booléen n'est jamais pris pour 0 (`type(...) is int`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-50 (RELU de Cowork du 25-11-2026 à 17h17) : la garde qui ACCEPTE (« if code == 0 and ligne: »,
      return 0) n'était ni fabriquée ni couverte.
    ⑨ CE QUI CLOCHE — Une acceptation rendue par une variable (« return code, raison » quand code vaut 0) n'est pas
      reconnue ; un prédicat écrit autrement qu'en « and » non plus.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    premier = valeur.elts[0] if isinstance(valeur, ast.Tuple) and valeur.elts else None
    if isinstance(valeur, ast.Constant) and (valeur.value is True or (type(valeur.value) is int and valeur.value == 0)):
        return "constante"
    if isinstance(premier, ast.Constant) and type(premier.value) is int and premier.value == 0:
        return "couple"
    if isinstance(valeur, ast.BoolOp) and isinstance(valeur.op, ast.And):
        return "prédicat"
    return None


def corps_qui_accepte(corps):
    """Dit si le corps d'un `if` ACCEPTE : il contient un `return` de la constante 0 ou True, ou d'un couple (0, …).

    ① RÔLE — Le miroir de `corps_qui_refuse` (superviseur R-759 de 18h08, forme recommandée, point 2).
    ② CONTEXTE D'APPEL — `sabotages_fabriques`.
    ③ ENTRÉE — `corps` : la liste des instructions du corps d'un `if` (nœuds `ast`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — `ast.walk` de chaque instruction ; `acceptation` « constante » ou « couple » sur chaque `return`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-50 : « if code == 0 and ligne: … return 0, detail » est la garde la plus importante du contrôle.
    ⑨ CE QUI CLOCHE — Comme `corps_qui_refuse` : une fonction imbriquée dans le corps serait parcourue aussi.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return any(isinstance(n, ast.Return) and acceptation(n.value) in ("constante", "couple")
               for instruction in corps for n in ast.walk(instruction))


def gardes(pieces):
    """Rend les fonctions-gardes, par PROPRIÉTÉ : toutes les fonctions de l'enveloppe sauf `main`, plus `lire_le_detail`.

    ① RÔLE — Superviseur R-759 de 18h08, forme recommandée, point 1 : « GARDES devient une propriété ; si l'on renomme
      ou ajoute une fonction, l'épreuve change d'avis ».
    ② CONTEXTE D'APPEL — `sabotages_fabriques`.
    ③ ENTRÉE — `pieces` : {chemin relatif : texte}.
    ④ CONDITIONS D'ENTRÉE — L'enveloppe s'analyse.
    ⑤ SORTIE — UNE valeur : la liste des (pièce, nom de fonction).
      [rend: 1]
    ⑥ TRAITEMENT — les `def` du premier niveau de l'enveloppe, `main` exclue (elle aiguille et affiche) ; puis
      GARDE_DU_JOUEUR.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Avec une liste écrite, `contenu_vert` et `code_de_sortie_nul` échappaient à la fabrication.
    ⑨ CE QUI CLOCHE — Le joueur n'est pris que par sa fonction `lire_le_detail` (les autres sont éprouvées par
      ailleurs) : une garde ajoutée ailleurs dans le joueur n'est pas fabriquée.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    arbre = ast.parse(pieces[ENVELOPPE])
    return [(ENVELOPPE, n.name) for n in arbre.body if isinstance(n, ast.FunctionDef) and n.name != "main"] \
        + [GARDE_DU_JOUEUR]


def court_circuit(arbre, fn):
    """Rend (ligne, texte) du court-circuit d'acceptation de `fn`, ou None si `fn` n'accepte par aucun `return`.

    ① RÔLE — Le seul sabotage qui voit une acceptation SANS `if` (superviseur R-759 de 18h08, forme recommandée,
      point 3 : « recopier ce return en première instruction »).
    ② CONTEXTE D'APPEL — `sabotages_fabriques`.
    ③ ENTRÉE — `arbre` : l'arbre du module ; `fn` : le nœud de la fonction.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None, ou le couple (numéro de ligne où insérer, texte de l'instruction avec son
      retrait et sa fin de ligne).
      [rend: 1]
    ⑥ TRAITEMENT — le premier `return` d'acceptation dans l'ordre du texte ; le point d'insertion est la première
      instruction `if` du premier niveau du corps (avant toute garde), à défaut la première instruction après la
      docstring ; un prédicat devient « return True » ; un couple est recopié, chaque élément qui lit un nom NON
      encore lié à ce point (ni paramètre, ni nom du module, ni nom natif, ni nom affecté plus haut) devenant le texte
      "court-circuit" (sinon le sabotage planterait au lieu d'accepter).
    ⑦ UNITÉ — Des lignes du texte.
    ⑧ POURQUOI — `juger_un_resultat`, `contenu_vert` et `code_de_sortie_nul` acceptent en arrivant au bout, sans
      `if` : sans court-circuit, leur acceptation était invisible à la fabrication (N-50).
    ⑨ CE QUI CLOCHE — Insérer AVANT la première garde et non en toute première instruction est un choix de l'agent
      (écart à la lettre du superviseur, dit dans la note) : sans lui, `return 0, detail` de `jouer_le_controle`
      planterait (detail non encore défini) et le sabotage mordrait par un plantage, pas par une acceptation.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    retours = sorted((n for n in ast.walk(fn) if isinstance(n, ast.Return) and acceptation(n.value)),
                     key=lambda n: (n.lineno, n.col_offset))
    if not retours:
        return None
    corps = fn.body[1:] if (fn.body and isinstance(fn.body[0], ast.Expr)
                            and isinstance(fn.body[0].value, ast.Constant)) else fn.body
    i = next((k for k, s in enumerate(corps) if isinstance(s, ast.If)), 0)
    lies = {a.arg for a in fn.args.args + fn.args.kwonlyargs + fn.args.posonlyargs
            + [x for x in (fn.args.vararg, fn.args.kwarg) if x]} | set(dir(builtins))
    for s in arbre.body:
        if isinstance(s, (ast.FunctionDef, ast.ClassDef)):
            lies.add(s.name)
        elif isinstance(s, (ast.Import, ast.ImportFrom)):
            lies |= {(a.asname or a.name).split(".")[0] for a in s.names}
        elif isinstance(s, ast.Assign):
            lies |= {n.id for c in s.targets for n in ast.walk(c) if isinstance(n, ast.Name)}
    for s in corps[:i]:
        lies |= {n.id for n in ast.walk(s) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    v = retours[0].value
    if acceptation(v) == "prédicat":
        texte = "return True"
    elif acceptation(v) == "constante":
        texte = "return " + ast.unparse(v)
    else:
        elements = [ast.unparse(e) if {n.id for n in ast.walk(e) if isinstance(n, ast.Name)} <= lies
                    else '"court-circuit"' for e in v.elts]
        texte = "return " + ", ".join(elements)
    s = corps[i]
    return s.lineno, " " * s.col_offset + texte + "\n"


def sabotages_fabriques(pieces):
    """Fabrique, depuis le code, les sabotages des fonctions-gardes ; rend la liste, ou lève ValueError.

    ① RÔLE — La réparation de fond de N-43, puis de N-50 et N-51 (superviseurs R-759 du 25-11-2026 ; celui de 18h08 :
      « la fabrication doit reconnaître l'acceptation par sa FORME, pas par une liste ») : que chaque garde de ces
      fonctions, qui refuse OU qui accepte, soit sabotée sans que personne ait à l'écrire.
    ② CONTEXTE D'APPEL — `main`, avec « --saboter ».
    ③ ENTRÉE — `pieces` : {chemin relatif : texte} des pièces lues à la racine éprouvée.
    ④ CONDITIONS D'ENTRÉE — Chaque pièce de `gardes` est dans `pieces` et s'analyse.
    ⑤ SORTIE — UNE valeur : la liste des (clé, pièce, texte saboté de la pièce).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque (pièce, fonction) de `gardes(pieces)` (sinon ValueError si elle est absente) :
      (a) REFUS — chaque nœud `if` (« elif » compris) dont le corps refuse (`corps_qui_refuse`) : si sa condition est
      un « or », chaque terme devient `False` (un sabotage par terme) ; sinon la condition entière ; clé
      « fonction · terme ».
      (b) ACCEPTATION PAR UN `if` — chaque `if` dont le corps accepte (`corps_qui_accepte`) : si sa condition est un
      « and », chaque terme devient `True` ; sinon la condition entière ; clé « fonction · accepte · terme ».
      (c) PRÉDICAT — chaque `return` d'un « and » : chaque terme devient `True` ; clé « fonction · accepte · terme ».
      (d) COURT-CIRCUIT — `court_circuit` : le `return` d'acceptation recopié avant la première garde ; clé
      « fonction · court-circuit ».
      (e) `re.fullmatch` — chaque appel devient `re.match`, numérotés dans l'ordre du texte ; clé « fonction · match
      au lieu de fullmatch n°k · appel ».
      Deux sabotages de même clé → ValueError. Une fonction qui ne donne aucun sabotage (`charger`,
      `environnement_git` : ni garde ni acceptation) n'en donne aucun, et c'est dit par `main`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-43 : neuf sabotages à la main sur dix vivaient. N-50 : la garde qui ACCEPTE (« code == 0 ») pouvait
      sauter sans qu'un cas tombe. N-51 : fullmatch → match ne faisait tomber aucun cas. Un terme de « or » d'un refus
      (ou de « and » d'une acceptation) retiré seul est la forme exacte de M3 et M4 de Cowork.
    ⑨ CE QUI CLOCHE — Retirer un terme d'un « and » qui REFUSE élargit le refus : ce n'est pas un sabotage, il n'est pas
      fait ; de même un terme d'un « or » qui accepte. Une garde écrite autrement qu'en `if` (expression
      conditionnelle, compréhension) n'est pas sabotée, sauf par le court-circuit de sa fonction ; un refus délégué à
      une autre fonction (« if code != 0: return code, raison » de `juger_un_resultat`) n'est pas vu ici : il est
      sabotée dans la fonction déléguée (`contenu_vert`), si elle est parmi les gardes.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    fabriques = []

    def ajouter(cle, piece, texte):
        """Ajoute un sabotage. ① RÔLE — Refuser deux clés égales. ② CONTEXTE D'APPEL — `sabotages_fabriques`.
        ③ ENTRÉE — `cle`, `piece`, `texte` : la clé, la pièce, le texte saboté. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur. [rend: 0]
        ⑥ TRAITEMENT — liste. ⑦ UNITÉ — — ⑧ POURQUOI — Une clé double rendrait REDONDANTS et ATTENDUS ambigus.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main, ou lève ValueError. [sort: non]"""
        if any(cle == f[0] for f in fabriques):
            raise ValueError(f"deux sabotages fabriqués de même clé : {cle}")
        fabriques.append((cle, piece, texte))

    for piece, nom in gardes(pieces):
        texte = pieces[piece]
        arbre = ast.parse(texte)
        fn = next((n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef) and n.name == nom), None)
        if fn is None:
            raise ValueError(f"fonction-garde absente : {nom} dans {piece}")
        for n in ast.walk(fn):
            if isinstance(n, ast.If) and corps_qui_refuse(n.body):
                termes = n.test.values if isinstance(n.test, ast.BoolOp) and isinstance(n.test.op, ast.Or) else [n.test]
                for terme in termes:
                    ajouter(f"{nom} · {ast.unparse(terme)}", piece, remplacer_le_texte_du_noeud(texte, terme, "False"))
            if isinstance(n, ast.If) and corps_qui_accepte(n.body):
                termes = n.test.values if isinstance(n.test, ast.BoolOp) and isinstance(n.test.op, ast.And) else [n.test]
                for terme in termes:
                    ajouter(f"{nom} · accepte · {ast.unparse(terme)}", piece,
                            remplacer_le_texte_du_noeud(texte, terme, "True"))
            if isinstance(n, ast.Return) and acceptation(n.value) == "prédicat":
                for terme in n.value.values:
                    ajouter(f"{nom} · accepte · {ast.unparse(terme)}", piece,
                            remplacer_le_texte_du_noeud(texte, terme, "True"))
        cc = court_circuit(arbre, fn)
        if cc:
            lignes = texte.split("\n")
            ajouter(f"{nom} · court-circuit", piece, "\n".join(lignes[:cc[0] - 1]) + "\n" + cc[1]
                    + "\n".join(lignes[cc[0] - 1:]))
        appels = sorted((n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                         and n.func.attr == "fullmatch" and isinstance(n.func.value, ast.Name)
                         and n.func.value.id == "re"), key=lambda n: (n.lineno, n.col_offset))
        for k, appel in enumerate(appels, 1):
            ajouter(f"{nom} · match au lieu de fullmatch n°{k} · {ast.unparse(appel)}", piece,
                    remplacer_le_texte_du_noeud(texte, appel.func, "re.match"))
    return fabriques


def lancer(commande, env=None, cwd=None):
    """Lance une commande ; rend son code et sa sortie.

    ① RÔLE — Un seul lancement. ② CONTEXTE D'APPEL — partout. ③ ENTRÉE — la commande, l'environnement, le dossier.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, la sortie (erreurs comprises).
    [rend: 2]
    ⑥ TRAITEMENT — subprocess, DELAI secondes. ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main, ou lève au délai.
    [sort: non]
    """
    r = subprocess.run(commande, env=env, cwd=cwd, capture_output=True, text=True, timeout=DELAI,
                       stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout + r.stderr


def git(dossier, *a):
    """Lance git dans un dossier, exige le succès, rend la sortie.

    ① RÔLE — Fabriquer les dépôts de l'épreuve. ② CONTEXTE D'APPEL — `fabriquer`, `cas`. ③ ENTRÉE — le dossier, les
    arguments. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la sortie, sans espaces de fin.
    [rend: 1]
    ⑥ TRAITEMENT — `lancer`. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance git. ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    code, sortie = lancer(["git", "-C", dossier, "-c", "user.name=e", "-c", "user.email=e@e", *a], env=ENV_GIT)
    if code != 0:
        raise OSError(f"git {a[0]} : {sortie.strip()[:200]}")
    return sortie.strip()


ENV_GIT = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")


def fabriquer(racine, base, pieces, note="note de livraison\n"):
    """Fabrique une origine, son clone (le « clone du circuit ») et une copie sans .git ; rend leurs chemins.

    ① RÔLE — Le décor d'un cas. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — `racine` éprouvée ; `base` : dossier neuf ;
    `pieces` : {chemin relatif : texte} des pièces (éventuellement sabotées) ; `note` : le texte de la note.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le dictionnaire clone, copie, pointe, premier (le commit
    d'avant).
    [rend: 1]
    ⑥ TRAITEMENT — origine : deux commits sur main ; clone par « git clone », HEAD détachée ; copie : les pièces, le
    remplaçant du contrôle, la note, LISEZ_MOI.txt. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, ⑥.
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨. ⑩ EFFET — Écrit sous `base`. ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    origine, clone, copie = (os.path.join(base, n) for n in ("origine", "clone", "copie"))
    os.makedirs(origine)
    git(origine, "init", "-q", "-b", "main")
    with open(os.path.join(origine, "LISEZ_MOI.txt"), "w", encoding="utf-8") as f:
        f.write("un\n")
    git(origine, "add", "-A")
    git(origine, "commit", "-q", "-m", "un")
    premier = git(origine, "rev-parse", "HEAD")
    with open(os.path.join(origine, "LISEZ_MOI.txt"), "a", encoding="utf-8") as f:
        f.write("deux\n")
    git(origine, "commit", "-q", "-am", "deux")
    git(base, "clone", "-q", origine, clone)
    git(clone, "checkout", "-q", "--detach")
    pointe = git(clone, "rev-parse", "HEAD")
    for rel, texte in pieces.items():
        os.makedirs(os.path.dirname(os.path.join(copie, rel)), exist_ok=True)
        with open(os.path.join(copie, rel), "w", encoding="utf-8") as f:
            f.write(texte)
    os.makedirs(os.path.join(copie, "echanges"), exist_ok=True)
    with open(os.path.join(copie, VRAI_CONTROLE), "w", encoding="utf-8") as f:
        f.write(REMPLACANT)
    with open(os.path.join(copie, "echanges", "A_RELIRE.md"), "w", encoding="utf-8") as f:
        f.write(note)
    shutil.copy(os.path.join(clone, "LISEZ_MOI.txt"), os.path.join(copie, "LISEZ_MOI.txt"))
    return {"clone": clone, "copie": copie, "pointe": pointe, "premier": premier}


def env_de(racine, d, **plus):
    """Rend l'environnement d'un lancement de l'enveloppe ou du joueur, comme le circuit le donne.

    ① RÔLE — GITHUB_WORKSPACE, POINTE_JOUEE, et le chemin du vrai contrôle (pour son lecteur de ligne). ② CONTEXTE
    D'APPEL — `cas`. ③ ENTRÉE — la racine, le décor, des variables en plus (valeur None : retirée). ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le dictionnaire.
    [rend: 1]
    ⑥ TRAITEMENT — à partir d'ENV_GIT, sans RESULTAT_DE_L_EPREUVE hérité. ⑦ UNITÉ — — ⑧ POURQUOI — Un lancement
    reproductible, quoi que porte l'environnement de la nuit. ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    e = dict(ENV_GIT, GITHUB_WORKSPACE=d["clone"], POINTE_JOUEE=d["pointe"],
             VRAI_CONTROLE_POUR_L_EPREUVE=os.path.join(racine, VRAI_CONTROLE))
    e.pop("RESULTAT_DE_L_EPREUVE", None)
    for k, v in plus.items():
        if v is None:
            e.pop(k, None)
        else:
            e[k] = v
    return e


def envelopper(racine, d, detail, **plus):
    """Lance l'enveloppe de la copie ; rend son code et le détail écrit (ou {}).

    ① RÔLE — Un lancement direct de l'usage (a). ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — la racine, le décor, le
    chemin du détail, des variables en plus. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : code, détail.
    [rend: 2]
    ⑥ TRAITEMENT — `lancer` dans le dossier du décor (sans .git : le dossier courant de l'épreuve ne doit rien
    décider, voir REDONDANTS), puis lecture du détail. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    code, _ = lancer([sys.executable, "-B", os.path.join(d["copie"], ENVELOPPE), d["copie"]],
                     env=env_de(racine, d, RESULTAT_DE_L_EPREUVE=detail, **plus), cwd=os.path.dirname(d["copie"]))
    try:
        with open(detail, encoding="utf-8") as f:
            return code, json.load(f)
    except (OSError, ValueError):
        return code, {}


class PremierFaux(Exception):
    """Arrête les cas au premier faux (`cas` avec `au_premier`), ou au premier faux d'un cas ATTENDU : un sabotage n'a
    besoin que d'un cas qui tombe (du cas nommé, s'il en a un)."""


def cas(racine, pieces, base, au_premier=False, attendus=None):
    """Joue les cas C1 à C28 sur des décors neufs ; rend la liste des cas faux.

    ① RÔLE — Les preuves de la fiche en tête. ② CONTEXTE D'APPEL — `main`, une fois, puis une fois par sabotage.
    ③ ENTRÉE — `racine`, `pieces` (textes), `base` : un dossier neuf ; `au_premier` : s'arrêter au premier cas faux
    (les sabotages) ; `attendus` : les noms des cas nommés (ATTENDUS) — avec `au_premier`, s'arrêter au premier faux
    PARMI eux, ou None. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des textes des cas faux (vide : tout est juste).
    [rend: 1]
    ⑥ TRAITEMENT — C1 vert · C2 refus du contrôle → ROUGE · C3 POINTE_JOUEE sur un autre commit → 2 · C4 copie avec
      un .git → 2 · C5 sans GITHUB_WORKSPACE → 2 · C6 clone sans origin/main → 2 · C7 contrôle à 0 sans ligne → 2 ·
      C8 « --matrice … Livraison » accepté, et refusé quand le code est retiré de la table · C9 le joueur de bout en
      bout : RESULTAT.json porte code 0, pointe jouée, verdict VERT, empreinte · C10 « --juger » : oui sur la bonne
      pointe, non sur une autre pointe, non sur une autre épreuve, non sur un verdict ROUGE · C11 un détail illisible
      → « detail_illisible » · C12 (superviseur R-759, point 3) le disque de la copie diffère de la pointe (la note
      du commit n'est pas celle de la copie) → 2. RELU de Cowork du 25-11-2026 (N-43, N-44), superviseur R-759 :
      « --juger » : C13 code 0 et verdict ROUGE → 1 · C14 vert sans empreinte → 1 · C15 « code_de_sortie »: false →
      1 · C16 pointe relue abrégée → 2 · C17 résultat qui n'est pas un objet JSON → 2 ; le joueur : C18 détail-lien,
      détail de plus de 64 Kio, détail qui n'est pas un objet → « detail_illisible » ; l'enveloppe : C19 note-lien → 2 ·
      C20 note absente → 2 · C21 contrôle absent → 2 · C22 POINTE_JOUEE absente → 2 · C23 GITHUB_WORKSPACE sans .git
      → 2 ; et, par le contrôle de remplacement, un index égal à HEAD dans chaque cas vert (M2). RELU de Cowork du
      25-11-2026 à 17h17 (N-50, N-51), superviseur R-759 de 18h08 : C24 note qui porte déjà une ligne de contrôle,
      et le contrôle refuse → 1, ROUGE, empreinte vide · C25 « --juger » : code_de_sortie 1, verdict VERT,
      empreinte valide → 1 · C26 « --juger » : empreinte de 16 hexadécimaux suivie de « zz » → 1 · C27 la pointe suit
      programmes/TEMOIN.txt « a », la copie porte « b » → 2, « diffère de la pointe » · C28 « --juger » : pointe
      relue de 41 hexadécimaux → 2, « mal formée ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, ⑧. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit sous `base`.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    faux = []
    n = [0]

    def decor(note="note de livraison\n"):
        """Un décor neuf. ① RÔLE — `fabriquer` dans un sous-dossier neuf. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — la
        note. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le décor.
        [rend: 1]
        ⑥ TRAITEMENT — compteur. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]
        """
        n[0] += 1
        return fabriquer(racine, os.path.join(base, f"d{n[0]}"), pieces, note)

    def detail():
        """Un chemin de détail neuf. ① RÔLE — —. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le chemin.
        [rend: 1]
        ⑥ TRAITEMENT — compteur. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
        [sort: non]
        """
        n[0] += 1
        return os.path.join(base, f"detail{n[0]}.json")

    def juger(nom, condition, vu):
        """Note un cas. ① RÔLE — Afficher et retenir. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, condition, ce
        qui a été vu. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur.
        [rend: 0]
        ⑥ TRAITEMENT — liste. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Affiche.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]
        """
        if not condition:
            faux.append(f"{nom} : {vu}")
            if au_premier and (attendus is None or nom.split()[0] in attendus):
                raise PremierFaux()

    try:
        d = decor()
        sha = hashlib.sha256(b"note de livraison\n").hexdigest()
        code, det = envelopper(racine, d, detail())
        juger("C1 vert", code == 0 and det.get("verdict") == "VERT" and det.get("empreinte") == EMPREINTE
              and det.get("pointe") == d["pointe"] and det.get("sha256_de_la_note") == sha
              and git(d["clone"], "status", "--porcelain") == "" and git(d["clone"], "rev-parse", "HEAD") == d["pointe"],
              f"code {code}, {det}")
        code, det = envelopper(racine, decor("REFUSER\n"), detail())
        juger("C2 refus du contrôle → ROUGE", code == 1 and det.get("verdict") == "ROUGE", f"code {code}, {det}")
        d = decor()
        code, det = envelopper(racine, d, detail(), POINTE_JOUEE=d["premier"])
        juger("C3 autre pointe → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        d = decor()
        git(d["copie"], "init", "-q")
        code, det = envelopper(racine, d, detail())
        juger("C4 copie avec .git → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        code, det = envelopper(racine, decor(), detail(), GITHUB_WORKSPACE=None)
        juger("C5 sans GITHUB_WORKSPACE → 2", code == 2, f"code {code}, {det}")
        d = decor()
        git(d["clone"], "update-ref", "-d", "refs/remotes/origin/main")
        code, det = envelopper(racine, d, detail())
        juger("C6 clone sans origin/main → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        code, det = envelopper(racine, decor("SANSLIGNE\n"), detail())
        juger("C7 contrôle à 0 sans ligne → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        d = decor()
        code, sortie = lancer([sys.executable, "-B", os.path.join(d["copie"], JOUEUR), "--matrice", d["copie"],
                               "Livraison"], env=env_de(racine, d))
        lancement = os.path.join(d["copie"], "tests", "LANCEMENT_DES_EPREUVES.json")
        table = json.load(open(lancement, encoding="utf-8"))
        table["epreuves_longues"].pop("Livraison", None)
        json.dump(table, open(lancement, "w", encoding="utf-8"), ensure_ascii=False)
        code2, sortie2 = lancer([sys.executable, "-B", os.path.join(d["copie"], JOUEUR), "--matrice", d["copie"],
                                 "Livraison"], env=env_de(racine, d))
        juger("C8 code dans la table, refusé s'il en est absent",
              code == 0 and '"Livraison"' in sortie and code2 == 2 and "inconnue" in sortie2,
              f"avec : {code} {sortie.strip()[:120]} · sans : {code2} {sortie2.strip()[:120]}")
        d = decor()
        s = os.path.join(base, "sortie_c9")
        code, sortie = lancer([sys.executable, "-B", os.path.join(d["copie"], JOUEUR), d["copie"], "Livraison",
                               "--sortie=" + s], env=env_de(racine, d))
        try:
            r = json.load(open(os.path.join(s, "RESULTAT.json"), encoding="utf-8"))
        except (OSError, ValueError):
            r = {}
        dd = r.get("detail_de_l_epreuve") or {}
        juger("C9 joueur : RESULTAT.json porte verdict, pointe, empreinte",
              code == 0 and r.get("code_de_sortie") == 0 and r.get("pointe_jouee") == d["pointe"]
              and dd.get("verdict") == "VERT" and dd.get("pointe") == d["pointe"] and dd.get("empreinte") == EMPREINTE,
              f"code {code}, {json.dumps(r, ensure_ascii=False)[:300]} {sortie.strip()[-200:]}")
        env = env_de(racine, d)
        env_juge = [sys.executable, "-B", os.path.join(d["copie"], ENVELOPPE), "--juger"]
        # la pointe du décor de C9, gardée pour C13-C17 : `d` change à C12, et deux décors ne portent la même pointe
        # que s'ils tombent dans la même seconde (premier essai du 25-11-2026 : C13 « autre pointe » sous sabotage)
        pointe9 = d["pointe"]
        bon, _ = lancer(env_juge + [os.path.join(s, "RESULTAT.json"), d["pointe"]], env=env)
        autre, sortie_autre = lancer(env_juge + [os.path.join(s, "RESULTAT.json"), d["premier"]], env=env)
        faux_code = dict(r, code_epreuve="Carte")
        p = os.path.join(base, "faux_code.json")
        json.dump(faux_code, open(p, "w", encoding="utf-8"))
        mauvaise, _ = lancer(env_juge + [p, d["pointe"]], env=env)
        rouge = dict(r, code_de_sortie=1, detail_de_l_epreuve=dict(dd, verdict="ROUGE"))
        q = os.path.join(base, "rouge.json")
        json.dump(rouge, open(q, "w", encoding="utf-8"))
        r_rouge, _ = lancer(env_juge + [q, d["pointe"]], env=env)
        juger("C10 juger : oui sur la pointe relue, non sinon",
              (bon, autre, mauvaise, r_rouge) == (0, 1, 1, 1) and "autre pointe" in sortie_autre,
              f"bonne {bon}, autre pointe {autre}, autre épreuve {mauvaise}, rouge {r_rouge}")
        import importlib.util
        spec = importlib.util.spec_from_file_location("JOUEUR_EPROUVE", os.path.join(d["copie"], JOUEUR))
        j = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(j)
        mauvais = os.path.join(base, "illisible.json")
        open(mauvais, "w", encoding="utf-8").write("[1, 2")
        res = {}
        j.lire_le_detail(mauvais, res)
        rien = {}
        j.lire_le_detail(os.path.join(base, "absent.json"), rien)
        juger("C11 détail illisible dit, absent muet", "detail_illisible" in res and rien == {}, f"{res} {rien}")
        d = decor()
        os.makedirs(os.path.join(d["clone"], "echanges"), exist_ok=True)
        with open(os.path.join(d["clone"], "echanges", "A_RELIRE.md"), "w", encoding="utf-8") as f:
            f.write("une autre note, celle de la pointe\n")
        git(d["clone"], "add", "-A")
        git(d["clone"], "commit", "-q", "-m", "note de la pointe")
        code, det = envelopper(racine, d, detail(), POINTE_JOUEE=git(d["clone"], "rev-parse", "HEAD"))
        juger("C12 disque de la copie différent de la pointe → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE"
              and "diffère de la pointe" in det.get("raison", ""), f"code {code}, {det}")
        # « --juger », une garde par cas (N-43 : M3, M4 ; N-44 : J2 ; J4 de Cowork ; résultat qui n'est pas un objet)
        vert = dict(r, code_de_sortie=0, detail_de_l_epreuve=dict(dd, verdict="VERT", empreinte=EMPREINTE))

        def juge(nom, contenu, pointe, attendu, mot):
            """Écrit un résultat et le fait juger. ① RÔLE — Un cas de « --juger ». ② CONTEXTE D'APPEL — `cas`.
            ③ ENTRÉE — nom, contenu (objet ou texte brut), pointe relue, code attendu, mot attendu dans la sortie.
            ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur.
            [rend: 0]
            ⑥ TRAITEMENT — fichier, `lancer`, `juger`. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Écrit un fichier. ⑪ TERMINAISON — Rend la main, ou lève PremierFaux.
            [sort: non]
            """
            f = os.path.join(base, nom.split()[0] + ".json")
            with open(f, "w", encoding="utf-8") as h:
                h.write(contenu if isinstance(contenu, str) else json.dumps(contenu))
            c, s = lancer(env_juge + [f, pointe], env=env)
            juger(nom, c == attendu and mot in s, f"code {c} : {s.strip()[-160:]}")

        juge("C13 juger : code 0 et verdict ROUGE → 1", dict(vert, detail_de_l_epreuve=dict(
            vert["detail_de_l_epreuve"], verdict="ROUGE")), pointe9, 1, "non vert")
        juge("C14 juger : vert sans empreinte → 1", dict(vert, detail_de_l_epreuve=dict(
            vert["detail_de_l_epreuve"], empreinte="")), pointe9, 1, "sans empreinte")
        juge("C15 juger : code_de_sortie false → 1", dict(vert, code_de_sortie=False), pointe9, 1, "non vert")
        juge("C16 juger : pointe relue abrégée → 2", vert, pointe9[:9], 2, "mal formée")
        juge("C17 juger : résultat qui n'est pas un objet → 2", "[1, 2]", pointe9, 2, "pas un objet")
        # le joueur : détail-lien, trop gros, pas un objet (M8, M9 de Cowork)
        bon_detail = os.path.join(base, "bon_detail.json")
        with open(bon_detail, "w", encoding="utf-8") as h:
            json.dump({"verdict": "VERT"}, h)
        lien = os.path.join(base, "detail_lien.json")
        os.symlink(bon_detail, lien)
        gros = os.path.join(base, "detail_gros.json")
        with open(gros, "w", encoding="utf-8") as h:
            json.dump({"x": "a" * (64 * 1024 + 1)}, h)
        liste = os.path.join(base, "detail_liste.json")
        with open(liste, "w", encoding="utf-8") as h:
            json.dump([1, 2], h)
        vus = []
        for chemin in (lien, gros, liste, bon_detail):
            res = {}
            j.lire_le_detail(chemin, res)
            vus.append("detail_illisible" in res and "detail_de_l_epreuve" not in res)
        juger("C18 joueur : détail-lien, trop gros, pas un objet → illisible ; un bon détail est rangé",
              vus == [True, True, True, False], f"{vus}")
        # l'enveloppe : note-lien, note absente, contrôle absent, POINTE_JOUEE absente, GITHUB_WORKSPACE sans .git
        d = decor()
        ailleurs = os.path.join(base, "note_ailleurs.md")
        with open(ailleurs, "w", encoding="utf-8") as h:
            h.write("note de livraison\n")
        os.remove(os.path.join(d["copie"], "echanges", "A_RELIRE.md"))
        os.symlink(ailleurs, os.path.join(d["copie"], "echanges", "A_RELIRE.md"))
        code, det = envelopper(racine, d, detail())
        juger("C19 note-lien → 2", code == 2 and "lien" in det.get("raison", ""), f"code {code}, {det}")
        d = decor()
        os.remove(os.path.join(d["copie"], "echanges", "A_RELIRE.md"))
        code, det = envelopper(racine, d, detail())
        juger("C20 note absente → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        d = decor()
        os.remove(os.path.join(d["copie"], VRAI_CONTROLE))
        code, det = envelopper(racine, d, detail())
        juger("C21 contrôle absent → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        code, det = envelopper(racine, decor(), detail(), POINTE_JOUEE=None)
        juger("C22 POINTE_JOUEE absente → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        d = decor()
        sans_git = os.path.join(base, f"sans_git_{n[0]}")
        os.makedirs(sans_git)
        code, det = envelopper(racine, d, detail(), GITHUB_WORKSPACE=sans_git)
        juger("C23 GITHUB_WORKSPACE sans .git → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE", f"code {code}, {det}")
        # N-50 (A1) : une ligne de contrôle d'un passage précédent en queue de la note, et le contrôle d'aujourd'hui refuse
        code, det = envelopper(racine, decor("note de livraison\nREFUSER\n\n<!-- CONTROLE %s · 2026-11-25 15:00 Paris -->\n"
                                             % EMPREINTE), detail())
        juger("C24 ligne de contrôle ancienne et refus → ROUGE, 1", code == 1 and det.get("verdict") == "ROUGE"
              and det.get("empreinte") == "", f"code {code}, {det}")
        juge("C25 juger : code_de_sortie 1 et verdict VERT → 1", dict(vert, code_de_sortie=1), pointe9, 1, "non vert")
        juge("C26 juger : empreinte suivie de « zz » → 1", dict(vert, detail_de_l_epreuve=dict(
            vert["detail_de_l_epreuve"], empreinte=EMPREINTE + "zz")), pointe9, 1, "sans empreinte")
        # N-51 (X3 de Cowork, A6) : un programme du disque de la copie différent de la pointe
        d = decor()
        os.makedirs(os.path.join(d["clone"], "programmes"), exist_ok=True)
        with open(os.path.join(d["clone"], "programmes", "TEMOIN.txt"), "w", encoding="utf-8") as f:
            f.write("a\n")
        git(d["clone"], "add", "-A")
        git(d["clone"], "commit", "-q", "-m", "témoin de la pointe")
        with open(os.path.join(d["copie"], "programmes", "TEMOIN.txt"), "w", encoding="utf-8") as f:
            f.write("b\n")
        code, det = envelopper(racine, d, detail(), POINTE_JOUEE=git(d["clone"], "rev-parse", "HEAD"))
        juger("C27 programme du disque différent de la pointe → 2", code == 2 and det.get("verdict") == "IMPOSSIBLE"
              and "diffère de la pointe" in det.get("raison", ""), f"code {code}, {det}")
        juge("C28 juger : pointe relue de 41 hexadécimaux → 2", vert, pointe9 + "a", 2, "mal formée")
    except PremierFaux:
        pass
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        faux.append(f"DÉCOR IMPOSSIBLE : {type(e).__name__} : {e}")
    return faux


def mordus(faux, attendus):
    """Rend les cas faux qui comptent pour un sabotage : tous, ou ceux qui sont nommés dans ATTENDUS.

    ① RÔLE — Qu'un sabotage nommé ne « morde » que par le cas qui le vise (superviseur R-759 de 18h08 : « SABOTAGES
      EXIGÉS (le cas qui doit tomber) »). ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `faux` : les textes rendus par
      `cas` ; `attendus` : des noms de cas, ou None. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des textes retenus.
      [rend: 1]
    ⑥ TRAITEMENT — filtre sur le premier mot. ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage qui fait tomber un autre cas que
      celui qui le vise prouve moins que ce qu'on annonce. ⑨ CE QUI CLOCHE — « DÉCOR IMPOSSIBLE » n'est jamais un cas
      nommé : un décor qui tombe ne fait pas mordre un sabotage nommé. ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return faux if attendus is None else [f for f in faux if f.split()[0] in attendus]


def main():
    """La ligne de commande (fiche en tête).

    ① RÔLE — Jouer les cas, puis les sabotages. ② CONTEXTE D'APPEL — Fiche en tête, ②. ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④. ⑤ SORTIE — UNE valeur : le code de sortie (fiche en tête, ⑤).
    [rend: 1]
    ⑥ TRAITEMENT — lire les pièces de la racine ; les cas ; avec « --saboter » : pour chaque sabotage écrit, le texte
      doit se trouver une fois dans sa pièce (sinon 2), et les cas doivent rougir (sinon 1) ; puis les sabotages
      fabriqués (`sabotages_fabriques` ; ValueError → 2) : chaque clé de REDONDANTS et d'ATTENDUS doit désigner un
      sabotage (sinon 2, la liste a vieilli) ; un sabotage nommé dans ATTENDUS ne mord que par un de ses cas (`mordus`) ; un sabotage hors REDONDANTS doit faire rougir un cas (sinon 1) ; un sabotage de
      REDONDANTS qui fait rougir un cas rend 1 aussi (sa raison est fausse). Les cas d'un sabotage s'arrêtent au
      premier faux.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, ⑧. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Fiche en tête, ⑩.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    a = sys.argv[1:]
    if not a or a[0].startswith("--") or any(x != "--saboter" for x in a[1:]):
        print("usage : EPREUVES_DU_CONTROLE_DE_LIVRAISON_SUR_GITHUB_Mer_25-11-2026.py <racine> [--saboter]")
        return 2
    racine = os.path.abspath(a[0])
    try:
        pieces = {rel: open(os.path.join(racine, rel), encoding="utf-8").read() for rel in PIECES + (VRAI_CONTROLE,)}
    except OSError as e:
        print(f"IMPOSSIBLE — pièce illisible : {e}")
        return 2
    pieces.pop(VRAI_CONTROLE)
    base = tempfile.mkdtemp(prefix="epreuve_controle_github_")
    try:
        faux = cas(racine, pieces, os.path.join(base, "juste"))
        for f in faux:
            print("  FAUX " + f)
        print(f"cas C1-C28 : {'tous justes' if not faux else str(len(faux)) + ' faux'}")
        if faux:
            return 1
        if "--saboter" not in a[1:]:
            return 0
        muets = []
        for nom, piece, ancien, nouveau, quoi in SABOTAGES:
            if pieces[piece].count(ancien) != 1:
                print(f"IMPOSSIBLE — {nom} : texte trouvé {pieces[piece].count(ancien)} fois dans {piece}")
                return 2
            sabote = dict(pieces)
            sabote[piece] = pieces[piece].replace(ancien, nouveau)
            rouges = mordus(cas(racine, sabote, os.path.join(base, nom), au_premier=True, attendus=ATTENDUS.get(nom)),
                            ATTENDUS.get(nom))
            print(f"  {nom} ({quoi}) : " + (f"MORD — {rouges[0][:110]}" if rouges else "NE MORD PAS"
                                           + (f" sur le cas nommé {' '.join(ATTENDUS[nom])}" if nom in ATTENDUS else "")))
            if not rouges:
                muets.append(nom)
        print(f"sabotages écrits : {len(SABOTAGES) - len(muets)} mordent sur {len(SABOTAGES)}"
              + (f" ; muets : {' '.join(muets)}" if muets else ""))
        try:
            fabriques = sabotages_fabriques(pieces)
        except ValueError as e:
            print(f"IMPOSSIBLE — sabotages fabriqués : {e}")
            return 2
        connus = {f[0] for f in fabriques} | {s[0] for s in SABOTAGES}
        vieillis = sorted((set(REDONDANTS) | set(ATTENDUS)) - connus)
        if vieillis:
            print("IMPOSSIBLE — REDONDANTS ou ATTENDUS désigne un sabotage qui n'existe plus : " + " | ".join(vieillis))
            return 2
        sans = [f"{nom} ({piece})" for piece, nom in gardes(pieces) if not any(f[0].startswith(nom + " · ")
                                                                            for f in fabriques)]
        print("fonctions-gardes sans aucun sabotage fabriqué (ni garde, ni acceptation) : " + (", ".join(sans) or "—"))
        muets_f, menteurs, i = [], [], 0
        for cle, piece, texte in fabriques:
            i += 1
            sabote = dict(pieces)
            sabote[piece] = texte
            rouges = mordus(cas(racine, sabote, os.path.join(base, f"F{i}"), au_premier=True,
                                attendus=ATTENDUS.get(cle)), ATTENDUS.get(cle))
            if cle in REDONDANTS:
                print(f"  F{i} {cle} : " + (f"MORD alors qu'il est déclaré redondant — {rouges[0][:90]}" if rouges
                                            else "redondant — " + REDONDANTS[cle]))
                if rouges:
                    menteurs.append(cle)
                continue
            print(f"  F{i} {cle} : " + (f"MORD — {rouges[0][:100]}" if rouges else "NE MORD PAS"
                                         + (f" sur le cas nommé {' '.join(ATTENDUS[cle])}" if cle in ATTENDUS else "")))
            if not rouges:
                muets_f.append(cle)
        print(f"sabotages fabriqués : {len(fabriques)} ({len(REDONDANTS)} déclarés redondants) ; "
              f"{len(fabriques) - len(REDONDANTS) - len(muets_f)} mordent sur {len(fabriques) - len(REDONDANTS)}"
              + (f" ; muets : {' | '.join(muets_f)}" if muets_f else "")
              + (f" ; redondants qui mordent : {' | '.join(menteurs)}" if menteurs else ""))
        return 1 if muets or muets_f or menteurs else 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
