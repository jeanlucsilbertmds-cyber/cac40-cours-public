#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_PUBLICATION_AUTOMATIQUE — Mer 25-11-2026 (Paris), ESSAI DE BOUT EN BOUT. Simulation uniquement :
aucun ordre réel, jamais.

LE SENS EN TÊTE. « Ces épreuves lancent programmes/PUBLIER_LES_VERSIONS_EN_ATTENTE.py EN ENTIER contre une COPIE NUE
LOCALE d'un dépôt public et un faux dépôt privé, sans réseau, et vérifient ce qu'il POUSSE (rien à blanc, sans force,
une seule demande, au format du relais de main), ce qu'il MONTRE (rien de privé, vocabulaire fixe), ce qu'il RETIENT
(échecs comptés par pointe, arrêt au deuxième) et le pas « Ranger le journal » du circuit ; avec --saboter, chaque
sabotage doit faire rougir au moins un cas, sinon l'épreuve est une décoration. »
Elle remplace les épreuves de la première version (archivées), dont les 15 sabotages ne visaient que les fonctions
pures : la relecture à mandat inversé du 25-11-2026 (21h45) a laissé VERTS 12 sabotages de la partie qui agit.

① RÔLE — Construire les dépôts d'essai une fois, jouer les scénarios, puis (option --saboter) les rejouer sur des
  copies sabotées du programme et du circuit.
② CONTEXTE D'APPEL — À la main :
    python3 -B tests/EPREUVES_DE_LA_PUBLICATION_AUTOMATIQUE_Mer_25-11-2026.py <racine> [--saboter [--tranche=k/n]
        [--tous-les-rouges]]
  « --tranche=k/n » ne joue que les sabotages de rang k modulo n (la machine borne une épreuve locale à 2 min :
  les sabotages se jouent en huit tranches, 1/8 à 8/8, deux à la fois, chacune sous 2 min). « --tous-les-rouges »
  joue TOUS les cas sous chaque sabotage et les nomme tous (plus lent : pour montrer qu'un sabotage mord SON cas).
③ ENTRÉE — La racine d'un dépôt qui porte programmes/PUBLIER_LES_VERSIONS_EN_ATTENTE.py et
  circuits_publics_a_installer/publication_automatique.yml.
④ CONDITIONS D'ENTRÉE — git et bash installés. Aucun réseau : tout dépôt est local ; gh est remplacé par /bin/false
  (le programme ne doit pas l'appeler ; l'état des travaux est un faux voisin).
⑤ SORTIE — Le code : 0 tous verts (et, avec --saboter, chaque sabotage mord) · 1 un cas rouge ou un sabotage qui ne
  mord pas · 2 l'épreuve n'a pas pu tourner (R-734).
⑥ TRAITEMENT — Voir `scenarios` et `SABOTAGES`. Un sabotage remplace UN texte exact (absent ou en double : code 2).
⑦ UNITÉ — Secondes.
⑧ POURQUOI — R-731 (épreuves avec sabotages), BLOQUANT n°1 de la relecture du 25-11-2026 (P1 du superviseur R-759).
  R-732 : le format de demande vérifié est celui que le relais de main admet (lignes ~2580-2730 du fabricant de main).
⑨ CE QUI CLOCHE — Le fabricant et l'état des travaux sont FAUX (le vrai fabricant lit tout le dépôt privé) : la
  publication par le VRAI fabricant de main est éprouvée à part (echanges/A_RELIRE.md, point ⑧). La minute du nom de
  demande est lue deux fois (faux fabricant, puis programme) : un passage de minute entre les deux fausserait S9.
⑩ EFFET — Crée et retire des dossiers temporaires.
⑪ TERMINAISON — Sort par sys.exit ; chaque sous-processus borné à 60 s.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

PROGRAMME = "programmes/PUBLIER_LES_VERSIONS_EN_ATTENTE.py"
CIRCUIT = "circuits_publics_a_installer/publication_automatique.yml"
FAUX_JETON = "MOTIF = 'jeton'\n"
def _table(codes, argument="--court"):
    return json.dumps({"epreuves_longues": {c: {"chemin": "tests/E.py", "arguments": ["{copie}", argument],
                                                "pourquoi": "essai"} for c in codes}}, indent=1) + "\n"
TABLE_MAIN = _table(["Relais", "File"])

FAUX_FABRICANT = r'''#!/usr/bin/env python3
"""Faux fabricant de main (épreuve) : comme le vrai, il lit À CÔTÉ DE LUI ../tests/LANCEMENT_DES_EPREUVES.json, en
refuse un code ou un argument hors forme (ERREUR_DE_LA_TABLE), écrit le relais avec les codes de cette table,
recopie programmes/, publie sur la branche du privé."""
import hashlib, json, os, re, subprocess, sys, shutil
from datetime import datetime
from zoneinfo import ZoneInfo
_T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests", "LANCEMENT_DES_EPREUVES.json")
ERREUR_DE_LA_TABLE, EPREUVES_DU_CIRCUIT = None, []
try:
    for _c, _e in json.load(open(_T)).get("epreuves_longues", {}).items():
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,19}", _c):
            raise ValueError("code refuse")
        if not all(re.fullmatch(r"\{copie\}|[A-Za-z0-9_.=,-]{1,40}", a) for a in _e["arguments"]):
            raise ValueError("argument refuse")
        EPREUVES_DU_CIRCUIT.append((_c, _e["chemin"], _e["arguments"]))
except (OSError, ValueError, KeyError) as _x:
    ERREUR_DE_LA_TABLE, EPREUVES_DU_CIRCUIT = str(_x), []
try:
    _S = json.load(open(_T)).get("series_hors_de_la_nuit", {})
except (OSError, ValueError):
    _S = {}
for _s in _S.items():   # comme le vrai (l. 1915) : une liste ou un texte leve AttributeError, NON attrapee
    pass
prive, public = (sys.argv + ["", ""])[1:3]
publier = sys.argv[3:] == ["--publier"]
if __name__ == "__main__":
  with open(os.environ["FAB_LOG"], "a") as f:
    f.write(os.path.abspath(__file__) + " " + hashlib.sha256(open(__file__, "rb").read()).hexdigest()[:12] + " "
            + (hashlib.sha256(open(_T, "rb").read()).hexdigest()[:12] if os.path.exists(_T) else "sans-table") + "\n")
def _principal():
  if os.environ.get("FAB_ECHEC") == "1" or ERREUR_DE_LA_TABLE:
    sys.exit(1)
  g = lambda d, *a: subprocess.run(["git", "-C", d, "-c", "user.name=f", "-c", "user.email=f@f"] + list(a),
                                   capture_output=True, text=True, timeout=60)
  b = g(prive, "symbolic-ref", "--short", "HEAD").stdout.strip()
  if g(public, "symbolic-ref", "--short", "HEAD").stdout.strip() != b:
      sys.exit(1)
  os.makedirs(os.path.join(public, ".github/workflows"), exist_ok=True)
  open(os.path.join(public, ".github/workflows/demande_de_serie.yml"), "w").write("RELAIS DE MAIN (FILE-2) codes=" + ",".join(e[0] for e in EPREUVES_DU_CIRCUIT) + "\n")
  os.makedirs(os.path.join(public, "programmes"), exist_ok=True)
  for n in os.listdir(os.path.join(prive, "programmes")):
      shutil.copy(os.path.join(prive, "programmes", n), os.path.join(public, "programmes", n))
  if os.environ.get("FAB_MINUTE") == "1":
      os.makedirs(os.path.join(public, "demandes"), exist_ok=True)
      nom = "DEMANDE_" + datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d_%Hh%M") + ".txt"
      open(os.path.join(public, "demandes", nom), "w").write("deja\n")
  if not publier:
      sys.exit(0)
  g(public, "add", "-A")
  g(public, "commit", "-q", "-m", "code publie")
  if g(public, "push", "-q", "origin", "HEAD:refs/heads/" + b).returncode != 0:
      sys.exit(1)
  if os.environ.get("FAB_COURSE") == "1":
      autre = public + "_autre"
      subprocess.run(["git", "clone", "-q", "-b", b, g(public, "remote", "get-url", "origin").stdout.strip(), autre],
                     capture_output=True, timeout=60)
      open(os.path.join(autre, "COURSE.txt"), "w").write("un autre a pousse\n")
      g(autre, "add", "COURSE.txt"); g(autre, "commit", "-q", "-m", "COURSE"); g(autre, "push", "-q", "origin", b)
  if os.environ.get("FAB_SALE") == "1":
      open(os.path.join(public, "README.md"), "a").write("modifie sans commit\n")
if __name__ == "__main__":
  _principal()
'''

FAUX_ETAT = r'''"""Faux ETAT_DES_TRAVAUX (épreuve) : rend l'état écrit dans le fichier ETAT_FAUX."""
import json, os
class Impossible(Exception):
    pass
def etat_des_travaux(depot, gh="gh", public="", fetch=True):
    e = json.load(open(os.environ["ETAT_FAUX"]))
    if e.get("planter"):
        raise RuntimeError("SECRET-PRIVE travail-privee")
    return e
'''


def sh(d, *a, check=True):
    """git borné dans `d`, identité fixée.

    ① RÔLE — Fabriquer et lire les dépôts d'essai.
    ② CONTEXTE D'APPEL — Partout dans l'épreuve.
    ③ ENTRÉE — `d` : dossier · `a` : arguments de git · `check` : exiger le code 0.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la sortie standard, sans blancs autour.
      [rend: 1]
    ⑥ TRAITEMENT — subprocess.
    ⑦ UNITÉ — Secondes (60).
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    return subprocess.run(["git", "-C", d, "-c", "user.name=e", "-c", "user.email=e@e", "-c", "init.defaultBranch=main"]
                          + list(a), capture_output=True, text=True, check=check, timeout=60).stdout.strip()


def ecrire(chemin, texte):
    """Écrit un fichier, dossiers compris.

    ① RÔLE — Raccourci.
    ② CONTEXTE D'APPEL — `modele`, `jouer_un`.
    ③ ENTRÉE — `chemin`, `texte`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur.
      [rend: rien]
    ⑥ TRAITEMENT — makedirs, write.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def modele(racine_modele):
    """Construit une fois les dépôts d'essai : privé nu + clone, public nu.

    ① RÔLE — Le décor commun, recopié pour chaque scénario.
    ② CONTEXTE D'APPEL — `jouer`, une fois par jeu (sain ou saboté).
    ③ ENTRÉE — `racine_modele` : dossier vide.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : dict {nom de branche: pointe, "F2": commit FILE-2 d'essai, "vieille": pointe ancienne}.
      [rend: 1]
    ⑥ TRAITEMENT — Privé : main = c0 (avant FILE-2, porte déjà le fabricant de main), F2, puis branches travail-pub,
      travail-privee (base F2), travail-vieille (base c0), travail-fab (fabricant modifié), travail-pub-vieille
      (autre pointe, pour la mémoire), travail-table (sa table ajoute le code Propre), travail-table-fausse (code
      hors forme), travail-argument-faux (argument hors forme), travail-jeton (module du jeton modifié),
      travail-en-cours (marque EN_COURS), travail-table-plante (« series_hors_de_la_nuit » en liste : le
      fabricant de main ne se CHARGE pas, N-46 du RELU de Cowork du 25-11-2026 à 23h33). Main porte le faux fabricant, le faux module du jeton et la table de main
      (Relais, File). Public nu : main (README) et travail-pub déjà publique.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une branche de chaque PROPRIÉTÉ que le programme doit juger.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée des dépôts.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    t = racine_modele
    w = os.path.join(t, "w")
    os.makedirs(w)
    sh(w, "init", "-q")
    ecrire(os.path.join(w, "README.md"), "prive\n")
    ecrire(os.path.join(w, "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"), FAUX_FABRICANT)
    ecrire(os.path.join(w, "programmes/FORME_D_UN_JETON.py"), FAUX_JETON)
    ecrire(os.path.join(w, "tests/LANCEMENT_DES_EPREUVES.json"), TABLE_MAIN)
    sh(w, "add", "-A"); sh(w, "commit", "-q", "-m", "c0")
    c0 = sh(w, "rev-parse", "HEAD")
    ecrire(os.path.join(w, "FILE2.txt"), "le relais met en file\n")
    sh(w, "add", "-A"); sh(w, "commit", "-q", "-m", "F2")
    f2 = sh(w, "rev-parse", "HEAD")
    p = {"F2": f2}
    for b, base, fichier, texte in (("travail-pub", f2, "programmes/A.py", "a=1\n"),
                                    ("travail-privee", f2, "programmes/B.py", "b=1\n"),
                                    ("travail-vieille", c0, "programmes/C.py", "c=1\n"),
                                    ("travail-fab", f2, "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py", "# modifie\n"),
                                    ("travail-pub-vieille", f2, "programmes/D.py", "d=1\n"),
                                    ("travail-table", f2, "tests/LANCEMENT_DES_EPREUVES.json",
                                     _table(["Relais", "File", "Propre"])),
                                    ("travail-table-fausse", f2, "tests/LANCEMENT_DES_EPREUVES.json",
                                     _table(["Relais", "Mauvais-Code"])),
                                    ("travail-argument-faux", f2, "tests/LANCEMENT_DES_EPREUVES.json",
                                     _table(["Relais", "Propre"], "$(id)")),
                                    ("travail-jeton", f2, "programmes/FORME_D_UN_JETON.py", "MOTIF = 'autre'\n"),
                                    ("travail-en-cours", f2, "echanges/EN_COURS.md", "# EN COURS\n"),
                                    ("travail-table-plante", f2, "tests/LANCEMENT_DES_EPREUVES.json",
                                     json.dumps(dict(json.loads(_table(["Relais", "File", "Plante"])),
                                                     series_hors_de_la_nuit=["x"])) + "\n")):
        sh(w, "checkout", "-q", "-B", b, base)
        ecrire(os.path.join(w, fichier), texte)
        sh(w, "add", "-A"); sh(w, "commit", "-q", "-m", b)
        p[b] = sh(w, "rev-parse", "HEAD")
    sh(w, "checkout", "-q", "main")
    sh(t, "clone", "-q", "--bare", w, "prive.git")
    pw = os.path.join(t, "pw")
    os.makedirs(pw)
    sh(pw, "init", "-q")
    ecrire(os.path.join(pw, "README.md"), "public\n")
    sh(pw, "add", "-A"); sh(pw, "commit", "-q", "-m", "public")
    sh(pw, "checkout", "-q", "-b", "travail-pub")
    ecrire(os.path.join(pw, "programmes/A.py"), "a=0\n")
    sh(pw, "add", "-A"); sh(pw, "commit", "-q", "-m", "ancienne publication")
    sh(pw, "checkout", "-q", "main")
    sh(t, "clone", "-q", "--bare", pw, "public.git")
    shutil.rmtree(pw)
    shutil.rmtree(w)
    return p


FAUX_GIT = r'''#!/bin/sh
# Faux git (épreuve N-89) : simule une panne du RÉSEAU vers le public. PANNE contient « fetch » : tout fetch qui
# nomme le distant « origin » tombe (un fetch depuis un CHEMIN local passe) ; « push » : toute poussée tombe ;
# « vieux » (N-92, git antérieur à 2.29) : tout fetch dont un argument commence par « ^ » (refspec négative) tombe.
sous=""; prec=""
for a in "$@"; do
  if [ "$prec" = "-C" ] || [ "$prec" = "-c" ]; then prec=""; continue; fi
  case "$a" in -C|-c) prec="$a"; continue;; -*) continue;; esac
  sous="$a"; break
done
case "$sous:$PANNE" in
  fetch:*fetch*) for a in "$@"; do [ "$a" = origin ] && { echo "faux reseau coupe" >&2; exit 128; }; done;;
  push:*push*) echo "faux reseau coupe" >&2; exit 128;;
  fetch:*vieux*) for a in "$@"; do case "$a" in ^*) echo "fatal: invalid refspec" >&2; exit 128;; esac; done;;
esac
exec "$VRAI_GIT" "$@"
'''


def jouer_un(code_dir, modele_dir, d, p, branches, memoire=None, env=None, options=(), etat_brut=None, cwd=None,
             base_prete=False, panne=""):
    """Joue un passage du programme sur une copie neuve du décor.

    ① RÔLE — Un scénario : décor copié, mémoire posée, programme lancé.
    ② CONTEXTE D'APPEL — `scenarios`.
    ③ ENTRÉE — `code_dir` (programme + faux voisins) · `modele_dir` · `d` (dossier du scénario) · `p` (pointes) ·
      `branches` : liste de (nom, état) ou (nom, état, champs qui remplacent ceux par défaut : codes, resultats,
      pointe_heure) ; une branche absente du décor prend la pointe de travail-pub · `memoire` : dict ou chaîne brute posée sur publication-auto/journal ·
      `env` : variables pour le faux fabricant · `options` : options en plus · `etat_brut` : état écrit tel quel ·
      `cwd` : dossier courant du programme (None : celui de l'épreuve) · `base_prete` : la base du public est
      déjà clonée sous --travail (un dossier de travail réutilisé) · `panne` : « fetch » et/ou « push », la panne
      du réseau vers le public simulée par FAUX_GIT, mis en tête du PATH du programme (N-89) ; « vieux » : un git
      qui refuse les refspecs négatives (N-92).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : dict {code, ecran, memoire (dict ou None), public (refs avant/après), log (chemins du
      fabricant lancé), prive, travail, public_git}.
      [rend: 1]
    ⑥ TRAITEMENT — Copier les dépôts nus ; poser la mémoire en commit sur publication-auto/journal du privé nu ;
      cloner le privé ; écrire le faux état ; lancer le programme (gh = /bin/false) ; relever.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée des dossiers sous `d`.
    ⑪ TERMINAISON — Rend la main ; le programme borné à 60 s.
      [sort: non]
    """
    os.makedirs(d)
    for n in ("prive.git", "public.git"):
        shutil.copytree(os.path.join(modele_dir, n), os.path.join(d, n))
    if memoire is not None:
        m = os.path.join(d, "m")
        sh(d, "clone", "-q", os.path.join(d, "prive.git"), m)
        sh(m, "checkout", "-q", "--orphan", "publication-auto/journal")
        sh(m, "rm", "-rq", "--cached", ".")
        ecrire(os.path.join(m, "memoire.json"), memoire if isinstance(memoire, str) else json.dumps(memoire))
        sh(m, "add", "memoire.json"); sh(m, "commit", "-q", "-m", "memoire")
        sh(m, "push", "-q", "origin", "publication-auto/journal")
    prive = os.path.join(d, "prive")
    sh(d, "clone", "-q", os.path.join(d, "prive.git"), prive)
    etat = etat_brut if etat_brut is not None else {"fils": {"epreuves_en_cours": 0}, "branches": [
        dict({"branche": b[0], "pointe": p.get(b[0], p["travail-pub"]), "pointe_heure": int(time.time()) - 60,
              "etat": b[1], "codes": ["Relais", "File"], "resultats": {}}, **(b[2] if len(b) > 2 else {}))
        for b in branches]}
    ecrire(os.path.join(d, "etat.json"), json.dumps(etat))
    travail = os.path.join(d, "travail")
    os.makedirs(travail)
    if base_prete:
        sh(d, "clone", "-q", "--no-checkout", os.path.join(d, "public.git"), os.path.join(travail, "public_base"))
    log = os.path.join(d, "fab.log")
    ecrire(log, "")
    public_git = os.path.join(d, "public.git")
    avant = sh(public_git, "for-each-ref")
    e = dict(os.environ, ETAT_FAUX=os.path.join(d, "etat.json"), FAB_LOG=log, GIT_CONFIG_NOSYSTEM="1",
             GIT_AUTHOR_NAME="e", GIT_AUTHOR_EMAIL="e@e", GIT_COMMITTER_NAME="e", GIT_COMMITTER_EMAIL="e@e")
    e.update(env or {})
    if panne:
        faux = os.path.join(d, "faux_git")
        ecrire(os.path.join(faux, "git"), FAUX_GIT)
        os.chmod(os.path.join(faux, "git"), 0o755)
        e.update(PANNE=panne, VRAI_GIT=shutil.which("git"), PATH=faux + os.pathsep + os.environ.get("PATH", ""))
    sortie = os.path.join(d, "memoire_sortie.json")
    r = subprocess.run([sys.executable, "-B", os.path.join(code_dir, PROGRAMME), "--prive=" + prive,
                        "--travail=" + travail, "--memoire-sortie=" + sortie, "--depot-public=" + public_git,
                        "--gh=/bin/false", "--journal=" + os.path.join(d, "journal.log"), "--commit-file-2=" + p["F2"]]
                       + list(options), capture_output=True, text=True, timeout=60, env=e, cwd=cwd)
    try:
        mem = json.load(open(sortie))
    except (OSError, ValueError):
        mem = None
    return {"code": r.returncode, "ecran": r.stdout + r.stderr, "memoire": mem, "avant": avant,
            "apres": sh(public_git, "for-each-ref"), "log": open(log).read().split(), "prive": prive,
            "travail": travail, "public_git": public_git}


LIGNE_PERMISE = re.compile(r"^(travail-[A-Za-z0-9._-]+ [0-9a-f]{9} : (RIEN|ATTENTE|ATTEND L'INSTALLATION|"
                           r"PUBLIÉE ET DEMANDÉE|À BLANC|ÉCHEC|ARRÊT APRÈS 2 ÉCHECS)"
                           r"|publication automatique : (aucune branche examinée|ROUGE|rien de rouge)( \(à blanc\))?"
                           r"|IMPOSSIBLE — une source n'a pas pu être lue ; rien n'est décidé pour la suite "
                           r"\(détail au journal privé\)|PLANTAGE — exception imprévue \(détail au journal privé\))$")


def ecran_propre(r):
    """Dit si l'écran ne porte que des lignes permises et rien de privé.

    ① RÔLE — La propriété « rien de privé à l'écran public ».
    ② CONTEXTE D'APPEL — Chaque scénario.
    ③ ENTRÉE — `r` : le résultat de `jouer_un`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si propre.
      [rend: 1]
    ⑥ TRAITEMENT — Chaque ligne doit suivre LIGNE_PERMISE ; aucune ne nomme une branche absente du public d'essai
      (travail-privee, travail-vieille, travail-fab, travail-pub-vieille, travail-table…, travail-jeton,
      travail-en-cours, « travail-a b ») ni « Traceback » ni « SECRET ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Défaut 6 et sabotages I, J de la relecture.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = [l for l in r["ecran"].splitlines() if l.strip()]
    privees = ("travail-privee", "travail-vieille", "travail-fab", "travail-pub-vieille", "travail-table",
               "travail-argument-faux", "travail-jeton", "travail-en-cours", "travail-a b", "Traceback", "SECRET")
    return all(LIGNE_PERMISE.match(l) for l in lignes) and not any(x in r["ecran"] for x in privees)


def demandes_poussees(r):
    """Rend les commits de demande poussés au public d'essai : [(branche, fichiers touchés, texte)].

    ① RÔLE — Compter et lire les demandes.
    ② CONTEXTE D'APPEL — Scénarios S2, S4, S6.
    ③ ENTRÉE — `r` : le résultat de `jouer_un`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque branche du public, commits dont le message commence par « demande : ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    g = r["public_git"]
    rendu = []
    for b in sh(g, "for-each-ref", "--format=%(refname:short)", "refs/heads/").split():
        for c in sh(g, "log", "--format=%H %s", b).splitlines():
            sha, sujet = c.split(" ", 1)
            if sujet.startswith("demande : "):
                fichiers = sh(g, "diff-tree", "--no-commit-id", "--name-only", "-r", sha).split()
                rendu.append((b, fichiers, sh(g, "show", f"{sha}:{fichiers[0]}") + "\n" if fichiers else ""))
    return rendu


def seul_main(r, table):
    """Dit si chaque fabricant lancé est l'octet de main, lancé depuis un dossier composé, et a lu `table`.

    ① RÔLE — La propriété Q2 du superviseur R-759 (tour 2) : ce qui s'exécute est main, ce qui se lit vient de la
      branche.
    ② CONTEXTE D'APPEL — Les cas S2, S16, S19.
    ③ ENTRÉE — `r` : le résultat de `jouer_un` · `table` : le texte de la table que le fabricant doit avoir lue.
    ④ CONDITIONS D'ENTRÉE — Le faux fabricant écrit au journal FAB_LOG « chemin empreinte-de-lui empreinte-table ».
    ⑤ SORTIE — UNE valeur : vrai si au moins un lancement et tous conformes.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne : le dossier grand-parent du fabricant commence par « fabricant_ » (dossier
      composé), l'empreinte du fichier est celle de FAUX_FABRICANT, celle de la table est celle de `table`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-42 du RELU de Cowork (25-11-2026, 22h34).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import hashlib
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
    lignes = [l.split() for l in "\n".join([" ".join(r["log"][i:i + 3]) for i in range(0, len(r["log"]), 3)]).splitlines()]
    return bool(lignes) and all(len(x) == 3 and os.path.basename(os.path.dirname(os.path.dirname(x[0]))).startswith(
        "fabricant_") and x[1] == h(FAUX_FABRICANT) and x[2] == h(table) for x in lignes)


def bloc_du_circuit(code_dir, debut):
    """Rend les lignes du circuit d'un bloc de premier niveau, ou d'un pas, à partir de sa première ligne.

    ① RÔLE — Lire le YAML du circuit pour les épreuves X8 (always) et X9 (concurrency).
    ② CONTEXTE D'APPEL — Les cas S27, S28.
    ③ ENTRÉE — `code_dir` · `debut` : le texte exact de la première ligne (sans les blancs de tête).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des lignes (blancs de fin retirés) jusqu'à la ligne suivante de même
      indentation ou moins ; vide si la première ligne est absente.
      [rend: 1]
    ⑥ TRAITEMENT — Lecture ligne à ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Pas de lecteur YAML garanti sur la machine ; la forme du circuit est simple.
    ⑨ CE QUI CLOCHE — Pas un vrai lecteur YAML (ancres, blocs en ligne non compris).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = [l.rstrip() for l in open(os.path.join(code_dir, CIRCUIT), encoding="utf-8").read().splitlines()]
    for i, l in enumerate(lignes):
        if l.strip() == debut:
            ind = len(l) - len(l.lstrip())
            bloc = [l]
            for m in lignes[i + 1:]:
                if m.strip() and len(m) - len(m.lstrip()) <= ind:
                    break
                bloc.append(m)
            return bloc
    return []


def etape_du_circuit(code_dir, nom):
    """Extrait le script bash d'un pas du circuit, par son nom.

    ① RÔLE — Éprouver le vrai texte du circuit, pas une copie.
    ② CONTEXTE D'APPEL — S14, S15.
    ③ ENTRÉE — `code_dir` · `nom` : le début du nom du pas.
    ④ CONDITIONS D'ENTRÉE — Le pas a un bloc « run: | ».
    ⑤ SORTIE — UNE valeur : le script (indentation retirée).
      [rend: 1]
    ⑥ TRAITEMENT — Lignes après « - name: <nom> » puis « run: | », jusqu'au pas suivant.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Lecture ligne à ligne, pas un vrai lecteur YAML.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève (pas introuvable).
      [sort: non]
    """
    lignes = open(os.path.join(code_dir, CIRCUIT), encoding="utf-8").read().splitlines()
    i = next(k for k, l in enumerate(lignes) if l.strip().startswith("- name: " + nom))
    j = next(k for k in range(i, len(lignes)) if lignes[k].strip() == "run: |")
    script = []
    for l in lignes[j + 1:]:
        if l.strip().startswith("- name:") or l.strip().startswith("- uses:"):
            break
        script.append(l[10:])
    return "\n".join(script) + "\n"


def scenarios(code_dir, modele_dir, p, tmp, premier_rouge=False):
    """Joue tous les scénarios ; rend la liste (nom, vert, détail).

    ① RÔLE — Toutes les vérifications de bout en bout.
    ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `code_dir`, `modele_dir`, `p` (pointes), `tmp`, `premier_rouge` : s'arrêter au premier cas rouge
      (sabotages : un seul suffit à mordre).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des cas joués.
      [rend: 1]
    ⑥ TRAITEMENT — S1 à blanc · S2 passage normal (frein, format, garde du fabricant, ménage, écran, mémoire, relais
      de main publié) · S4 course (sans force, ÉCHEC rouge) · S5 deuxième échec, puis silence · S6 mémoire par pointe ·
      S7 base sans FILE-2 · S8 fabricant modifié · S9 minute prise · S10 --seulement inconnue · S11 aucune branche ·
      S12 mémoire illisible · S13 plantage · S14 pas « Ranger le journal » · S15 masque du base64 · S16 table de la
      branche (Q2) · S17, S18 table hors forme : ATTEND L'INSTALLATION · S19 filet Q1 · S20 module du jeton modifié ·
      S21 à S26 endroits X1, X2, X3, X4, X5, X13 du programme · S27, S28 endroits X8, X9 du circuit · S29a, S29b
      table qui fait planter le fabricant (S99 de Cowork, N-46) · S30 source d'UNE branche illisible · S31 table de
      main refusée · S32 commit FILE-2 absent · S33 json.py piégé dans le dossier courant (N-48) · C1, C1bis,
      C1ter, C4 réseau du public en panne, lecture puis écriture, et frein sur tentative (N-89) · GV git qui
      refuse les refspecs négatives (N-92) · K7 passage à blanc sans sonde d'écriture (N-93).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir le module.
    ⑨ CE QUI CLOCHE — Une exception dans un cas le rend rouge (jamais vert par défaut).
    ⑩ EFFET — Crée des dossiers sous `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cas = []
    n = [0]

    def ok(nom, f):
        """Joue un cas, attrape tout.

        ① RÔLE — Un cas.
        ② CONTEXTE D'APPEL — `scenarios`.
        ③ ENTRÉE — `nom` · `f` (rend vrai/faux et le détail).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — Rien si `premier_rouge` et un cas est déjà rouge ; sinon appeler f ; une exception est un rouge.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un cas qui casse ne doit jamais passer pour vert.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Ajoute à `cas`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if premier_rouge and any(not v for _, v, _ in cas):
            return
        try:
            v, detail = f()
        except Exception as e:  # un cas qui casse est rouge
            v, detail = False, f"{type(e).__name__} : {e}"
        cas.append((nom, bool(v), detail))

    def run(**k):
        """Raccourci de `jouer_un` dans un dossier neuf.

        ① RÔLE — Raccourci.
        ② CONTEXTE D'APPEL — Les cas.
        ③ ENTRÉE — `k` : les options de `jouer_un`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le résultat.
          [rend: 1]
        ⑥ TRAITEMENT — Dossier numéroté, puis `jouer_un`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Voir `jouer_un`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        n[0] += 1
        return jouer_un(code_dir, modele_dir, os.path.join(tmp, f"s{n[0]}"), p, **k)

    deux = [("travail-pub", "À ÉPROUVER"), ("travail-privee", "À ÉPROUVER")]

    def s1():
        """Cas S1 : à blanc : rien poussé, mémoire inchangée.

        ① RÔLE — à blanc : rien poussé, mémoire inchangée.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, options=["--a-blanc"])
        v = (r["code"] == 0 and r["avant"] == r["apres"] and r["memoire"] == {} and ecran_propre(r)
             and "travail-pub " + p["travail-pub"][:9] + " : À BLANC" in r["ecran"])
        return v, f"code {r['code']}, refs inchangées {r['avant'] == r['apres']}, mémoire {r['memoire']}"
    ok("S1 à blanc : rien poussé, mémoire inchangée", s1)

    def s2():
        """Cas S2 : une seule demande, format de main, seul le fabricant de main, ménage, écran sans privé.

        ① RÔLE — une seule demande, format de main, seul le fabricant de main, ménage, écran sans privé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, env={"FAB_SALE": "1"})
        d = demandes_poussees(r)
        attendu = f"circuit=epreuve\nepreuves=Relais,File\npointe={p['travail-pub']}\n"
        wt = sh(r["prive"], "worktree", "list").splitlines()
        restes = [x for x in os.listdir(r["travail"]) if x != "public_base"]
        relais = sh(r["public_git"], "show", "travail-pub:.github/workflows/demande_de_serie.yml", check=False)
        m = r["memoire"] or {}
        v = (r["code"] == 0 and len(d) == 1 and d[0][0] == "travail-pub" and len(d[0][1]) == 1
             and d[0][1][0].startswith("demandes/DEMANDE_") and d[0][2] == attendu
             and seul_main(r, TABLE_MAIN)
             and len(wt) == 1 and not restes and relais == "RELAIS DE MAIN (FILE-2) codes=Relais,File" and ecran_propre(r)
             and m.get(p["travail-pub"], {}).get("demande") is not None
             and m.get(p["travail-privee"], {}).get("demande") is None
             and "travail-pub " + p["travail-pub"][:9] + " : PUBLIÉE ET DEMANDÉE" in r["ecran"])
        return v, (f"code {r['code']}, demandes {[(b, len(f), x == attendu) for b, f, x in d]}, fabricant de main "
                   f"seul {seul_main(r, TABLE_MAIN)}, worktrees {len(wt)}, restes {restes}, relais {relais!r}")
    ok("S2 une seule demande, format de main, seul le fabricant de main, ménage, écran sans privé", s2)

    def s4():
        """Cas S4 : poussée sans force : course perdue = ÉCHEC rouge, rien écrasé.

        ① RÔLE — poussée sans force : course perdue = ÉCHEC rouge, rien écrasé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER")], env={"FAB_COURSE": "1"})
        course = "COURSE" in sh(r["public_git"], "log", "--format=%s", "travail-pub")
        m = (r["memoire"] or {}).get(p["travail-pub"], {})
        v = (r["code"] == 1 and course and not demandes_poussees(r) and m.get("echecs") == 1
             and " : ÉCHEC" in r["ecran"] and ecran_propre(r))
        return v, f"code {r['code']}, commit concurrent gardé {course}, mémoire {m}"
    ok("S4 poussée sans force : course perdue = ÉCHEC rouge, rien écrasé", s4)

    def s5():
        """Cas S5 : deuxième échec : ARRÊT rouge une fois, puis plus rien.

        ① RÔLE — deuxième échec : ARRÊT rouge une fois, puis plus rien.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        mem = {p["travail-pub"]: {"echecs": 1, "demande": None, "signalee": False, "branche": "travail-pub"}}
        r = run(branches=[("travail-pub", "À ÉPROUVER")], memoire=mem, env={"FAB_ECHEC": "1"})
        m = (r["memoire"] or {}).get(p["travail-pub"], {})
        r2 = run(branches=[("travail-pub", "À ÉPROUVER")], memoire=r["memoire"])
        v = (r["code"] == 1 and " : ARRÊT APRÈS 2 ÉCHECS" in r["ecran"] and m.get("echecs") == 2 and m.get("signalee")
             and r2["code"] == 0 and not r2["log"] and r2["avant"] == r2["apres"] and " : RIEN" in r2["ecran"])
        return v, f"1er {r['code']} {m} ; 2e code {r2['code']}, fabricant {r2['log']}"
    ok("S5 deuxième échec : ARRÊT rouge une fois, puis plus rien", s5)

    def s6():
        """Cas S6 : mémoire par POINTE ; demande en vol = attente ; vieille = échec compté puis nouvel essai.

        ① RÔLE — mémoire par POINTE ; demande en vol = attente ; vieille = échec compté puis nouvel essai.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        arretee = {p["travail-pub-vieille"]: {"echecs": 2, "demande": None, "signalee": True, "branche": "travail-pub"}}
        r = run(branches=[("travail-pub", "À ÉPROUVER")], memoire=arretee)
        jeune = {p["travail-pub"]: {"echecs": 0, "demande": int(__import__("time").time()) - 60, "signalee": False}}
        r2 = run(branches=[("travail-pub", "À ÉPROUVER")], memoire=jeune)
        vieille = {p["travail-pub"]: {"echecs": 0, "demande": int(__import__("time").time()) - 3 * 3600, "signalee": False}}
        r3 = run(branches=[("travail-pub", "À ÉPROUVER")], memoire=vieille)
        m3 = (r3["memoire"] or {}).get(p["travail-pub"], {})
        v = (len(demandes_poussees(r)) == 1 and r2["avant"] == r2["apres"] and " : ATTENTE" in r2["ecran"]
             and len(demandes_poussees(r3)) == 1 and m3.get("echecs") == 1)
        return v, (f"autre pointe arrêtée → {len(demandes_poussees(r))} demande ; en vol → ATTENTE "
                   f"{' : ATTENTE' in r2['ecran']} ; vieille → échecs {m3.get('echecs')}, "
                   f"{len(demandes_poussees(r3))} demande")
    ok("S6 mémoire par POINTE ; demande en vol = attente ; vieille = échec compté puis nouvel essai", s6)

    def s7():
        """Cas S7 : base sans FILE-2 : rien.

        ① RÔLE — base sans FILE-2 : rien.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-vieille", "À ÉPROUVER")])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        v = r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and "base sans FILE-2" in j
        return v, f"code {r['code']}, fabricant {r['log']}"
    ok("S7 base sans FILE-2 : rien", s7)

    def s8():
        """Cas S8 : fabricant modifié par la branche : ATTEND L'INSTALLATION, rien lancé.

        ① RÔLE — fabricant modifié par la branche : ATTEND L'INSTALLATION, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-fab", "À ÉPROUVER")])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        v = r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and "ATTEND L'INSTALLATION" in j
        return v, f"code {r['code']}, fabricant {r['log']}"
    ok("S8 fabricant modifié par la branche : ATTEND L'INSTALLATION, rien lancé", s8)

    def s9():
        """Cas S9 : minute déjà prise : ATTENTE, pas ÉCHEC.

        ① RÔLE — minute déjà prise : ATTENTE, pas ÉCHEC.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER")], env={"FAB_MINUTE": "1"})
        m = (r["memoire"] or {}).get(p["travail-pub"], {})
        return (r["code"] == 0 and " : ATTENTE" in r["ecran"] and m.get("echecs") == 0
                and not demandes_poussees(r)), f"code {r['code']}, {m}"
    ok("S9 minute déjà prise : ATTENTE, pas ÉCHEC", s9)

    def s10():
        """Cas S10 : --seulement inconnue : code 2.

        ① RÔLE — --seulement inconnue : code 2.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, options=["--seulement=travail-inconnue"])
        return r["code"] == 2 and r["avant"] == r["apres"] and ecran_propre(r), f"code {r['code']}"
    ok("S10 --seulement inconnue : code 2", s10)

    def s11():
        """Cas S11 : aucune branche : dit.

        ① RÔLE — aucune branche : dit.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "DÉPLOYABLE")])
        return (r["code"] == 0 and "aucune branche examinée" in r["ecran"]), r["ecran"].strip().replace(chr(10), " | ")[:120]
    ok("S11 aucune branche : dit", s11)

    def s12():
        """Cas S12 : mémoire illisible : code 2, écran fixe.

        ① RÔLE — mémoire illisible : code 2, écran fixe.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, memoire="pas du json {travail-privee}")
        return r["code"] == 2 and ecran_propre(r) and r["avant"] == r["apres"], r["ecran"].strip()[:160]
    ok("S12 mémoire illisible : code 2, écran fixe", s12)

    def s13():
        """Cas S13 : plantage : code 5, ni trace ni message.

        ① RÔLE — plantage : code 5, ni trace ni message.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[], etat_brut={"planter": True})
        return r["code"] == 5 and ecran_propre(r), r["ecran"].strip()[:160]
    ok("S13 plantage : code 5, ni trace ni message", s13)

    def s14():
        """Cas S14 : journal : une branche fixe, un commit par passage, arrêt sur erreur (set -e).

        ① RÔLE — journal : une branche fixe, un commit par passage, arrêt sur erreur (set -e).
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        d = os.path.join(tmp, "r14")
        os.makedirs(d)
        shutil.copytree(os.path.join(modele_dir, "prive.git"), os.path.join(d, "prive.git"))
        script = etape_du_circuit(code_dir, "Ranger le journal")
        codes = []
        for k in (1, 2, 3):
            rt = os.path.join(d, f"rt{k}")
            os.makedirs(rt)
            sh(d, "clone", "-q", os.path.join(d, "prive.git"), os.path.join(rt, "prive"))
            if k == 3:
                os.makedirs(os.path.join(rt, "journal.log", "x"))   # illisible pour hash-object
                ecrire(os.path.join(rt, "journal.log", "x", "y"), "y")
            else:
                ecrire(os.path.join(rt, "journal.log"), f"passage {k}\n")
                ecrire(os.path.join(rt, "memoire.json"), json.dumps({"k": k}))
            e = dict(os.environ, RUNNER_TEMP=rt, GITHUB_RUN_ID=str(100 + k), GITHUB_RUN_ATTEMPT="1")
            r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=60, env=e)
            codes.append((r.returncode, "journal range" in r.stdout))
        g = os.path.join(d, "prive.git")
        log = sh(g, "log", "--format=%H", "publication-auto/journal").splitlines()
        lineaire = sh(g, "rev-list", "--merges", "publication-auto/journal") == ""
        autres = sh(g, "for-each-ref", "--format=%(refname)", "refs/heads/publication-auto/").split()
        arbre = sh(g, "ls-tree", "-r", "--name-only", "publication-auto/journal").split()
        v = (codes[0] == (0, True) and codes[1] == (0, True) and codes[2][0] != 0 and not codes[2][1]
             and len(log) == 2 and lineaire and autres == ["refs/heads/publication-auto/journal"]
             and sorted(arbre) == ["memoire.json", "passages/passage_101_1.log", "passages/passage_102_1.log"])
        return v, f"codes {codes}, commits {len(log)}, branches {autres}, arbre {arbre}"
    ok("S14 journal : une branche fixe, un commit par passage, arrêt sur erreur (set -e)", s14)

    def s15():
        """Cas S15 : le base64 seul du secret est masqué.

        ① RÔLE — le base64 seul du secret est masqué.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un ou plusieurs passages du programme (`run`), puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Voir ⑥ de `scenarios` et la relecture du 25-11-2026.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        script = etape_du_circuit(code_dir, "Donner a git le secret")
        d = os.path.join(tmp, "r15")
        os.makedirs(d)
        e = dict(os.environ, JETON="jeton-d-essai", GITHUB_ENV=os.path.join(d, "env"))
        r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=60, env=e)
        import base64
        b = base64.b64encode(b"x-access-token:jeton-d-essai").decode()
        masques = [l[len("::add-mask::"):] for l in r.stdout.splitlines() if l.startswith("::add-mask::")]
        return r.returncode == 0 and b in masques, f"masques : {len(masques)}"
    ok("S15 le base64 seul du secret est masqué", s15)

    def s16():
        """Cas S16 : Q2 : la table de la BRANCHE est lue par le fabricant de main, son code est demandé et connu du relais.

        ① RÔLE — Q2 : la table de la BRANCHE est lue par le fabricant de main, son code est demandé et connu du relais.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-42 (BLOQUANT) du RELU de Cowork ; Q2 du superviseur R-759, tour 2.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-table", "À ÉPROUVER", {"codes": ["Propre"]})])
        d = demandes_poussees(r)
        relais = sh(r["public_git"], "show", "travail-table:.github/workflows/demande_de_serie.yml", check=False)
        table = sh(r["prive"], "show", p["travail-table"] + ":tests/LANCEMENT_DES_EPREUVES.json") + "\n"
        v = (r["code"] == 0 and len(d) == 1 and d[0][2] == f"circuit=epreuve\nepreuves=Propre\npointe={p['travail-table']}\n"
             and relais == "RELAIS DE MAIN (FILE-2) codes=Relais,File,Propre" and seul_main(r, table) and ecran_propre(r))
        return v, f"code {r['code']}, demandes {len(d)}, relais {relais!r}, seul main {seul_main(r, table)}"
    ok("S16 Q2 : la table de la BRANCHE est lue par le fabricant de main, son code est demandé et connu du relais.", s16)

    def s17():
        """Cas S17 : code hors forme dans la table de la branche : ATTEND L'INSTALLATION avant toute poussée, rien compté.

        ① RÔLE — code hors forme dans la table de la branche : ATTEND L'INSTALLATION avant toute poussée, rien compté.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Q2 du superviseur R-759, tour 2 : une table refusée n'est jamais un échec compté ; ⑨ (a) de l'ancienne fiche.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-table-fausse", "À ÉPROUVER", {"codes": ['Mauvais-Code']})])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        m = (r["memoire"] or {}).get(p["travail-table-fausse"], {})
        v = (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and "ATTEND L'INSTALLATION" in j
             and m.get("echecs") == 0 and m.get("demande") is None and ecran_propre(r))
        return v, f"code {r['code']}, fabricant {r['log']}, mémoire {m}"
    ok("S17 code hors forme dans la table de la branche : ATTEND L'INSTALLATION avant toute poussée, rien compté.", s17)

    def s18():
        """Cas S18 : argument hors forme dans la table de la branche : ATTEND L'INSTALLATION avant toute poussée, rien compté.

        ① RÔLE — argument hors forme dans la table de la branche : ATTEND L'INSTALLATION avant toute poussée, rien compté.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Q2 du superviseur R-759, tour 2 : une table refusée n'est jamais un échec compté ; ⑨ (a) de l'ancienne fiche.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-argument-faux", "À ÉPROUVER", {"codes": ['Propre']})])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        m = (r["memoire"] or {}).get(p["travail-argument-faux"], {})
        v = (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and "ATTEND L'INSTALLATION" in j
             and m.get("echecs") == 0 and m.get("demande") is None and ecran_propre(r))
        return v, f"code {r['code']}, fabricant {r['log']}, mémoire {m}"
    ok("S18 argument hors forme dans la table de la branche : ATTEND L'INSTALLATION avant toute poussée, rien compté.", s18)

    def s20():
        """Cas S20 : module du jeton modifié par la branche : ATTEND L'INSTALLATION, rien lancé.

        ① RÔLE — module du jeton modifié par la branche : ATTEND L'INSTALLATION, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Q2 du superviseur R-759, tour 2 : une table refusée n'est jamais un échec compté ; ⑨ (a) de l'ancienne fiche.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-jeton", "À ÉPROUVER", {"codes": ['Relais']})])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        m = (r["memoire"] or {}).get(p["travail-jeton"], {})
        v = (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and "ATTEND L'INSTALLATION" in j
             and m.get("echecs") == 0 and m.get("demande") is None and ecran_propre(r))
        return v, f"code {r['code']}, fabricant {r['log']}, mémoire {m}"
    ok("S20 module du jeton modifié par la branche : ATTEND L'INSTALLATION, rien lancé.", s20)

    def s19():
        """Cas S19 : filet Q1 : table de la branche refusée, seuls les codes de main sont demandés, avec la table de main.

        ① RÔLE — filet Q1 : table de la branche refusée, seuls les codes de main sont demandés, avec la table de main.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Q1 du superviseur R-759, tour 2 (en filet seulement).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-table-fausse", "À ÉPROUVER", {"codes": ["Relais", "Mauvais-Code"]})])
        d = demandes_poussees(r)
        v = (r["code"] == 0 and len(d) == 1
             and d[0][2] == f"circuit=epreuve\nepreuves=Relais\npointe={p['travail-table-fausse']}\n"
             and seul_main(r, TABLE_MAIN))
        return v, f"code {r['code']}, demandes {[x[2] for x in d]}"
    ok("S19 filet Q1 : table de la branche refusée, seuls les codes de main sont demandés, avec la table de main.", s19)

    def s21():
        """Cas S21 : X1 : pointe de plus de 3 jours : RIEN, rien lancé.

        ① RÔLE — X1 : pointe de plus de 3 jours : RIEN, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X1) du RELU de Cowork.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER", {"pointe_heure": int(time.time()) - 4 * 86400})])
        return (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and " : RIEN" in r["ecran"]), f"code {r['code']}, {r['log']}"
    ok("S21 X1 : pointe de plus de 3 jours : RIEN, rien lancé.", s21)

    def s22():
        """Cas S22 : X2 : marque EN_COURS sur la branche : ATTENTE, rien lancé.

        ① RÔLE — X2 : marque EN_COURS sur la branche : ATTENTE, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X2) du RELU de Cowork.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-en-cours", "À ÉPROUVER")])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        return (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and ": ATTENTE — marque EN_COURS" in j), f"code {r['code']}, {r['log']}"
    ok("S22 X2 : marque EN_COURS sur la branche : ATTENTE, rien lancé.", s22)

    def s23():
        """Cas S23 : X3 : une épreuve déjà jouée n'est pas redemandée.

        ① RÔLE — X3 : une épreuve déjà jouée n'est pas redemandée.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X3) du RELU de Cowork.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER", {"resultats": {"Relais": "VERT"}})])
        d = demandes_poussees(r)
        return (len(d) == 1 and d[0][2] == f"circuit=epreuve\nepreuves=File\npointe={p['travail-pub']}\n"), f"{[x[2] for x in d]}"
    ok("S23 X3 : une épreuve déjà jouée n'est pas redemandée.", s23)

    def s24():
        """Cas S24 : X4 : aucune épreuve manquante : RIEN, rien lancé.

        ① RÔLE — X4 : aucune épreuve manquante : RIEN, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X4) du RELU de Cowork.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER", {"resultats": {"Relais": "VERT", "File": "VERT"}})])
        return (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and " : RIEN" in r["ecran"]), f"code {r['code']}, {r['log']}"
    ok("S24 X4 : aucune épreuve manquante : RIEN, rien lancé.", s24)

    def s25():
        """Cas S25 : X5 : nom hors de la forme travail-… : ÉCHEC rouge, rien lancé.

        ① RÔLE — X5 : nom hors de la forme travail-… : ÉCHEC rouge, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X5) du RELU de Cowork.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-a b", "À ÉPROUVER")])
        j = open(os.path.join(tmp, f"s{n[0]}", "journal.log")).read()
        # le MOTIF est vérifié : depuis N-46, un nom hors forme qui passerait la garde finirait AUSSI en ÉCHEC (git
        # refuse la branche, Impossible de cette branche) — sans lui, le sabotage X5 ne mordait plus ici.
        return (r["code"] == 1 and r["avant"] == r["apres"] and not r["log"] and ecran_propre(r)
                and "ÉCHEC — nom de branche hors de la forme travail-…" in j), f"code {r['code']}, {r['log']}"
    ok("S25 X5 : nom hors de la forme travail-… : ÉCHEC rouge, rien lancé.", s25)

    def s26():
        """Cas S26 : X13 : --seulement sur une branche d'un autre état : RIEN, rien lancé.

        ① RÔLE — X13 : --seulement sur une branche d'un autre état : RIEN, rien lancé.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X13) du RELU de Cowork.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "DÉPLOYABLE")], options=["--seulement=travail-pub"])
        return (r["code"] == 0 and r["avant"] == r["apres"] and not r["log"] and " : RIEN" in r["ecran"]), f"code {r['code']}, {r['log']}"
    ok("S26 X13 : --seulement sur une branche d'un autre état : RIEN, rien lancé.", s26)

    def s27():
        """Cas S27 : X8 : le pas « Ranger le journal » tourne même après un échec (always()).

        ① RÔLE — X8 : le pas « Ranger le journal » tourne même après un échec (always()).
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X8) du RELU de Cowork : sans always(), un passage ROUGE ne range pas la mémoire, l'échec n'est jamais compté.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        bloc = bloc_du_circuit(code_dir, "- name: Ranger le journal au depot prive")
        return any(l.strip() == "if: ${{ always() }}" for l in bloc[1:3]), f"{bloc[:2]}"
    ok("S27 X8 : le pas « Ranger le journal » tourne même après un échec (always()).", s27)

    def s28():
        """Cas S28 : X9 : un seul passage à la fois (concurrency, sans annulation).

        ① RÔLE — X9 : un seul passage à la fois (concurrency, sans annulation).
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage du programme (`run`) ou la lecture du circuit, puis les propriétés vérifiées ci-dessous.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-43 (X9) du RELU de Cowork : deux passages ensemble liraient la même mémoire et déposeraient deux demandes.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        bloc = bloc_du_circuit(code_dir, "concurrency:")
        v = (bool(bloc) and bloc[0] == "concurrency:" and "  group: publication-automatique" in bloc
             and "  cancel-in-progress: false" in bloc)
        return v, f"{bloc}"
    ok("S28 X9 : un seul passage à la fois (concurrency, sans annulation).", s28)

    def journal_de(k):
        """Rend le journal privé du passage numéro `k`.

        ① RÔLE — Raccourci.
        ② CONTEXTE D'APPEL — S29 à S33.
        ③ ENTRÉE — `k` : le numéro du dossier du passage.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le texte (vide si absent).
          [rend: 1]
        ⑥ TRAITEMENT — Lecture.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit un fichier.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        try:
            return open(os.path.join(tmp, f"s{k}", "journal.log"), encoding="utf-8").read()
        except OSError:
            return ""

    def s29a():
        """Cas S29a : S99 de Cowork — table qui fait planter le fabricant : ATTEND L'INSTALLATION ; la suivante servie.

        ① RÔLE — N-46 : une erreur née d'une branche ne touche que cette branche.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele` (travail-table-plante).
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — travail-table-plante (code Plante, inconnu de main : le filet n'a rien à demander) puis
          travail-pub ; attendu : table-plante ATTEND L'INSTALLATION, rien compté ; travail-pub publiée et demandée ;
          sortie ≠ 2.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-46 du RELU de Cowork (23h33), épreuve S99 ; superviseur R-759 du 25-11-2026 à 23h37.
        ⑨ CE QUI CLOCHE — Avec un code CONNU de main, le filet publie : voir S29b (N-47).
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-table-plante", "À ÉPROUVER", {"codes": ["Plante"]}), ("travail-pub", "À ÉPROUVER")])
        j = journal_de(n[0])
        d = demandes_poussees(r)
        m = (r["memoire"] or {}).get(p["travail-table-plante"], {})
        v = (r["code"] == 0 and f"BRANCHE travail-table-plante {p['travail-table-plante'][:9]} : ATTEND L'INSTALLATION" in j
             and m.get("echecs") == 0 and m.get("demande") is None
             and len(d) == 1 and d[0][0] == "travail-pub" and ecran_propre(r)
             and "travail-pub " + p["travail-pub"][:9] + " : PUBLIÉE ET DEMANDÉE" in r["ecran"])
        return v, f"code {r['code']}, demandes {[x[0] for x in d]}, mémoire table-plante {m}"
    ok("S29a S99 de Cowork : table qui fait planter le fabricant : ATTEND L'INSTALLATION ; travail-pub servie ; sortie ≠ 2", s29a)

    def s29b():
        """Cas S29b : la même table, codes connus de main : le passage continue ; le FILET publie (N-47, en attente).

        ① RÔLE — Montrer ce que fait le filet tant que Jean-Luc n'a pas tranché N-47.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — travail-table-plante (codes Relais, File : ceux de S99 de Cowork) puis travail-pub ; attendu :
          sortie 0 (jamais 2), une ligne au journal pour CHAQUE branche ; table-plante publiée par le filet (table de
          main, codes de main), travail-pub en ATTENTE (frein : une demande par passage).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-46 (le passage ne s'arrête pas) ; N-47 (le filet, gardé jusqu'à l'accord de Jean-Luc).
        ⑨ CE QUI CLOCHE — Si Jean-Luc retire le filet, ce cas devient : table-plante ATTEND L'INSTALLATION, travail-pub
          servie, et S19 et le sabotage W3 sont à réécrire.
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-table-plante", "À ÉPROUVER"), ("travail-pub", "À ÉPROUVER")])
        j = journal_de(n[0])
        d = demandes_poussees(r)
        v = (r["code"] == 0 and f"BRANCHE travail-table-plante {p['travail-table-plante'][:9]} : PUBLIÉE ET DEMANDÉE" in j
             and f"BRANCHE travail-pub {p['travail-pub'][:9]} : ATTENTE" in j
             and len(d) == 1 and d[0][2] == f"circuit=epreuve\nepreuves=Relais,File\npointe={p['travail-table-plante']}\n"
             and seul_main(r, TABLE_MAIN) and ecran_propre(r))
        return v, f"code {r['code']}, demandes {[x[0] for x in d]}"
    ok("S29b même table, codes de main : le passage continue ; le filet publie (N-47 en attente de Jean-Luc)", s29b)

    def s30():
        """Cas S30 : source d'UNE branche illisible : ÉCHEC compté pour elle seule ; la suivante servie.

        ① RÔLE — N-46 ① : tout le corps de la boucle d'une branche dans un seul périmètre d'erreur.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — travail-fantome (pointe absente du clone : merge-base illisible) puis travail-pub ; attendu :
          sortie 1 (rouge, jamais 2), échecs 1 pour la pointe fantôme, travail-pub publiée et demandée.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Superviseur R-759 du 25-11-2026 à 23h37, N-46 ①.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        fantome = "0123456789abcdef0123456789abcdef01234567"
        r = run(branches=[("travail-fantome", "À ÉPROUVER", {"pointe": fantome}), ("travail-pub", "À ÉPROUVER")])
        d = demandes_poussees(r)
        m = (r["memoire"] or {}).get(fantome, {})
        v = (r["code"] == 1 and m.get("echecs") == 1 and len(d) == 1 and d[0][0] == "travail-pub" and ecran_propre(r))
        return v, f"code {r['code']}, mémoire fantôme {m}, demandes {[x[0] for x in d]}"
    ok("S30 source d'UNE branche illisible : ÉCHEC compté pour elle seule ; la suivante servie", s30)

    def s31():
        """Cas S31 : table de MAIN refusée par le fabricant de main : IMPOSSIBLE (code 2), rien poussé.

        ① RÔLE — N-46 ③ : le contrôle initial est une source commune.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Copie du code éprouvé dont la table de main porte un code hors forme ; travail-pub (table saine).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Sans ce contrôle, un code de main qui ne se charge plus rendrait toute table « refusée » :
          ATTEND L'INSTALLATION partout, sans une ligne rouge.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        autre = os.path.join(tmp, f"code_s31_{n[0]}")
        for sous in ("programmes", "tests", os.path.dirname(CIRCUIT)):   # jamais code_dir entier : il porte « jeu/ »
            shutil.copytree(os.path.join(code_dir, sous), os.path.join(autre, sous))
        ecrire(os.path.join(autre, "tests/LANCEMENT_DES_EPREUVES.json"), _table(["Relais", "Mauvais-Code"]))
        n[0] += 1
        r = jouer_un(autre, modele_dir, os.path.join(tmp, f"s{n[0]}"), p, [("travail-pub", "À ÉPROUVER")])
        v = r["code"] == 2 and r["avant"] == r["apres"] and not r["log"] and ecran_propre(r)
        return v, f"code {r['code']}, fabricant {r['log']}"
    ok("S31 table de MAIN refusée : IMPOSSIBLE (code 2), rien poussé", s31)

    def s32():
        """Cas S32 : commit FILE-2 absent du clone : IMPOSSIBLE (code 2) pour tout le passage, rien compté.

        ① RÔLE — N-46 ③ : FILE-2 est une source commune, pas un fait d'une branche.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — --commit-file-2 = un commit absent ; deux branches.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Sinon chaque branche compterait un échec dû au clone, et s'arrêterait au deuxième passage.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, options=["--commit-file-2=fedcba9876543210fedcba9876543210fedcba98"])
        m = r["memoire"] or {}
        v = (r["code"] == 2 and r["avant"] == r["apres"] and not r["log"] and ecran_propre(r)
             and all(x.get("echecs", 0) == 0 for x in m.values()))
        return v, f"code {r['code']}, mémoire {m}"
    ok("S32 commit FILE-2 absent : IMPOSSIBLE (code 2), rien compté", s32)

    def s33():
        """Cas S33 : json.py piégé dans le dossier courant : le lecteur isolé (-I) l'ignore.

        ① RÔLE — N-48 du RELU de Cowork : l'isolement « -I » du lecteur gardé par une épreuve.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Le programme lancé depuis un dossier qui porte json.py (« sys.exit(7) ») ; travail-pub.
          Avec -I : publiée et demandée. Sans -I : le lecteur charge le piège (« python -c » met le dossier courant en
          tête de sys.path), sort 7, et le contrôle initial rend IMPOSSIBLE.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-48 du RELU de Cowork (sabotage Y8 resté vert) ; superviseur R-759, tour 3.
        ⑨ CE QUI CLOCHE — PYTHONPATH n'est pas éprouvé : le programme lui-même (lancé sans -I) importerait le piège
          avant le lecteur.
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        piege = os.path.join(tmp, f"piege_{n[0]}")
        ecrire(os.path.join(piege, "json.py"), "import sys\nsys.exit(7)\n")
        r = run(branches=[("travail-pub", "À ÉPROUVER")], cwd=piege)
        d = demandes_poussees(r)
        v = r["code"] == 0 and len(d) == 1 and ecran_propre(r)
        return v, f"code {r['code']}, demandes {len(d)}"
    ok("S33 json.py piégé dans le dossier courant : le lecteur isolé (-I) l'ignore", s33)

    def c1():
        """Cas C1 : N-89 — fetch du public en panne aux passages 1 et 2 : IMPOSSIBLE, rien compté ; passage 3 servi.

        ① RÔLE — La lecture réseau du public est une source COMMUNE : sa panne ne compte d'échec à aucune branche.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Trois passages, la mémoire de sortie de l'un posée pour le suivant ; base du public déjà
          clonée (dossier de travail réutilisé) ; passages 1 et 2 : tout fetch vers « origin » tombe ; passage 3 :
          réseau revenu. Attendu : code 2 et mémoire sans échec aux passages 1 et 2 ; au passage 3, travail-pub
          publiée et demandée, code 0.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-89 du RELU de Cowork (26-11-2026, 00h13), son cas C1 ; superviseur R-759 de 00h16, geste ①.
        ⑨ CE QUI CLOCHE — La base est déjà clonée : avec une base clonée à ce passage, le geste ① ne joue pas (C1bis).
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r1 = run(branches=deux, base_prete=True, panne="fetch")
        r2 = run(branches=deux, base_prete=True, panne="fetch", memoire=r1["memoire"] or {})
        r3 = run(branches=deux, base_prete=True, memoire=r2["memoire"] or {})
        sans_echec = lambda r: all(x.get("echecs", 0) == 0 for x in (r["memoire"] or {}).values())
        v = (r1["code"] == 2 and r2["code"] == 2 and sans_echec(r1) and sans_echec(r2) and r1["avant"] == r1["apres"]
             and r3["code"] == 0 and len(demandes_poussees(r3)) == 1 and ecran_propre(r1) and ecran_propre(r3)
             and "travail-pub " + p["travail-pub"][:9] + " : PUBLIÉE ET DEMANDÉE" in r3["ecran"])
        return v, (f"passages 1, 2 : codes {r1['code']}, {r2['code']}, sans échec {sans_echec(r1)}, {sans_echec(r2)} ;"
                   f" passage 3 : code {r3['code']}, demandes {len(demandes_poussees(r3))}")
    ok("C1 fetch du public en panne aux passages 1-2 : IMPOSSIBLE, rien compté ; passage 3 servi", c1)

    def c1bis():
        """Cas C1bis : branche DÉJÀ publique, base clonée à ce passage, fetch réseau en panne : repart de sa pointe publique.

        ① RÔLE — Garder le geste ② : le clone de branche lit les branches distantes de la BASE (fetch local).
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele` (travail-pub déjà publique, commit « ancienne publication »).
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Un passage ; la base est clonée par le programme ; ensuite tout fetch vers « origin » tombe.
          Attendu : code 0, travail-pub publiée et demandée, et l'ancienne pointe publique est un ancêtre de la
          nouvelle (la publication est partie d'elle, pas de main).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Superviseur R-759 du 26-11-2026 à 00h16 : un clone --shared ne porte pas les branches distantes
          de la base ; retirer le fetch sans refspec ferait partir chaque branche publique de main (poussée refusée).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER")], panne="fetch")
        ancienne = next(l.split()[0] for l in r["avant"].splitlines() if l.endswith("refs/heads/travail-pub"))
        descend = subprocess.run(["git", "-C", r["public_git"], "merge-base", "--is-ancestor", ancienne, "travail-pub"],
                                 capture_output=True, timeout=60).returncode == 0
        neuve = sh(r["public_git"], "rev-parse", "travail-pub") != ancienne
        v = (r["code"] == 0 and descend and neuve and len(demandes_poussees(r)) == 1 and ecran_propre(r)
             and "travail-pub " + p["travail-pub"][:9] + " : PUBLIÉE ET DEMANDÉE" in r["ecran"])
        return v, f"code {r['code']}, part de la pointe publique {descend}, pointe avancée {neuve}"
    ok("C1bis branche déjà publique : repart de sa pointe publique, pas de main", c1bis)

    def c1ter():
        """Cas C1ter : poussée refusée pour toutes les branches : IMPOSSIBLE (sonde à blanc), rien compté.

        ① RÔLE — Garder le geste ③ : le droit d'écrire au public est une source commune.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Deux branches ; toute poussée tombe (y compris celle du fabricant). Attendu : code 2, mémoire
          sans échec, rien poussé, fabricant jamais lancé.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-89, famille relevée par Cowork (poussées du fabricant et de la demande) ; superviseur, geste ③.
        ⑨ CE QUI CLOCHE — Le faux git refuse TOUTE poussée, à blanc comprise : que GitHub refuse aussi la poussée à
          blanc d'un jeton révoqué n'est PAS éprouvé ici (THÉORIQUE).
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, panne="push")
        m = r["memoire"] or {}
        v = (r["code"] == 2 and r["avant"] == r["apres"] and not r["log"] and ecran_propre(r)
             and all(x.get("echecs", 0) == 0 for x in m.values()))
        return v, f"code {r['code']}, mémoire {m}, fabricant lancé {len(r['log']) // 3} fois"
    ok("C1ter poussée refusée pour toutes les branches : IMPOSSIBLE, rien compté", c1ter)

    def c4():
        """Cas C4 : une poussée TENTÉE qui tombe arme le frein : la branche suivante attend, un seul échec compté.

        ① RÔLE — Garder le geste ④ : le frein compte une tentative de poussée, pas seulement une réussite.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — travail-pub puis travail-privee ; course perdue (FAB_COURSE : la poussée de la demande est
          refusée). Attendu : code 1, travail-pub un échec, travail-privee ATTENTE et aucun échec.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Superviseur R-759 du 26-11-2026 à 00h16, geste ④ : une panne en cours de passage ne coûte qu'un
          échec, à une seule branche.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, env={"FAB_COURSE": "1"})
        m = r["memoire"] or {}
        j = journal_de(n[0])
        v = (r["code"] == 1 and m.get(p["travail-pub"], {}).get("echecs") == 1
             and m.get(p["travail-privee"], {}).get("echecs") == 0
             and f"BRANCHE travail-privee {p['travail-privee'][:9]} : ATTENTE" in j and ecran_propre(r))
        return v, (f"code {r['code']}, échecs pub {m.get(p['travail-pub'], {}).get('echecs')}, "
                   f"privee {m.get(p['travail-privee'], {}).get('echecs')}")
    ok("C4 poussée tentée qui tombe : la suivante attend (frein), un seul échec compté", c4)

    def gv():
        """Cas GV : N-92 — un git qui refuse les refspecs négatives (antérieur à 2.29) ne coûte d'échec à aucune branche.

        ① RÔLE — Garder la propriété : la boucle n'emploie aucune forme de commande qu'un git plus ancien refuserait.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — Deux branches, un passage ; le faux git (« vieux ») fait tomber tout fetch dont un argument
          commence par « ^ ». Attendu : code 0, aucun échec compté, une demande faite.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-92 et N-93 (K1) du RELU de Cowork du 26-11-2026 à 01h07 ; superviseur R-759 de 01h1x, Q2 ① :
          avec la refspec négative, chaque branche recevait un échec, puis toutes étaient ARRÊTÉES et l'écran
          redevenait vert (la forme de N-89).
        ⑨ CE QUI CLOCHE — Un faux git, pas un vrai git 2.28 : aucun vieux git n'est disponible ici.
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=deux, panne="vieux")
        m = r["memoire"] or {}
        v = (r["code"] == 0 and bool(m) and all(x.get("echecs", 0) == 0 for x in m.values())
             and len(demandes_poussees(r)) == 1 and ecran_propre(r))
        return v, f"code {r['code']}, mémoire {m}, demandes {len(demandes_poussees(r))}"
    ok("GV git qui refuse les refspecs négatives : aucun échec compté, demande faite", gv)

    def k7():
        """Cas K7 : N-93 — le passage à blanc ne sonde pas le droit d'écrire : poussée en panne, rien d'IMPOSSIBLE.

        ① RÔLE — Garder le CHOIX 1 de l'auteur (tour 5) : Cowork rejoue à blanc sans droit d'écrire au public.
        ② CONTEXTE D'APPEL — `scenarios`, par `ok`.
        ③ ENTRÉE — — (le décor et les pointes `p` du contexte).
        ④ CONDITIONS D'ENTRÉE — Le décor de `modele`.
        ⑤ SORTIE — DEUX valeurs : vrai si le cas est vert · le détail lisible.
          [rend: 2]
        ⑥ TRAITEMENT — « --a-blanc », une branche à examiner, toute poussée tombe. Attendu : code 0, dernière ligne
          de l'écran qui finit par « (à blanc) », pas d'IMPOSSIBLE, rien poussé.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-93 (K7) du RELU de Cowork du 26-11-2026 à 01h07 ; superviseur R-759 de 01h1x, Q2 ②.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Crée des dossiers sous `tmp`.
        ⑪ TERMINAISON — Rend la main ou lève (le cas est alors rouge).
          [sort: non]
        """
        r = run(branches=[("travail-pub", "À ÉPROUVER")], options=["--a-blanc"], panne="push")
        lignes = r["ecran"].strip().splitlines()
        v = (r["code"] == 0 and bool(lignes) and lignes[-1].endswith("(à blanc)") and "IMPOSSIBLE" not in r["ecran"]
             and r["avant"] == r["apres"] and ecran_propre(r))
        return v, f"code {r['code']}, dernière ligne {lignes[-1] if lignes else ''!r}"
    ok("K7 passage à blanc, poussée en panne : pas de sonde, code 0, « (à blanc) »", k7)
    return cas


SABOTAGES = [
    ("A_fabricant_de_la_branche", PROGRAMME,
     '[sys.executable, "-B", fabricant, prive_wt, public_wt]',
     '[sys.executable, "-B", os.path.join(prive_wt, FABRICANT), prive_wt, public_wt]'),
    ("A2_comparaison_du_code_retiree", PROGRAMME,
     'faits["code_de_main"] = faits["code_de_main"] and code == 0 and a_branche.strip() == a_main.strip()',
     'faits["code_de_main"] = True'),
    ("W1_table_de_main_toujours", PROGRAMME, "fabricant_main, compose, False, journal)", "fabricant_main, compose, True, journal)"),
    ("W2_table_non_jugee", PROGRAMME, "connus = codes_du_relais(fabricant, journal) if posee else None\n        filet",
     "connus = list(codes)\n        filet"),
    ("W3_filet_demande_tout", PROGRAMME, "a_demander = [c for c in codes if c in (connus or [])]", "a_demander = list(codes)"),
    ("W4_module_du_jeton_non_compare", PROGRAMME, "for chemin in (FABRICANT, MODULE_DU_JETON):\n        _, a_main",
     "for chemin in (FABRICANT,):\n        _, a_main"),
    ("X1_fraicheur_retiree", PROGRAMME, 'if maintenant - faits["pointe_heure"] > FRAICHEUR_S:', "if False:"),
    ("X2_marque_en_cours_ignoree", PROGRAMME, 'if faits["en_cours"]:', "if False:"),
    ("X3_codes_deja_joues_redemandes", PROGRAMME, 'codes = [c for c in faits["codes"] if c not in faits["resultats"]]',
     'codes = list(faits["codes"])'),
    ("X4_aucune_manquante_ignoree", PROGRAMME, 'if not [c for c in faits["codes"] if c not in faits["resultats"]]:',
     "if False:"),
    ("X5_forme_de_branche_retiree", PROGRAMME, "if not MOTIF_BRANCHE.match(branche):", "if False:"),
    ("X13_etat_autre_publie", PROGRAMME, 'if faits["etat"] != "À ÉPROUVER":', "if False:"),
    ("X8_ranger_sans_always", CIRCUIT, "        if: ${{ always() }}\n", ""),
    ("X9_concurrence_retiree", CIRCUIT, "concurrency:\n  group: publication-automatique\n  cancel-in-progress: false\n", ""),
    ("B_echec_pas_rouge", PROGRAMME, "ROUGES = (ECHEC, ARRET)", "ROUGES = (ARRET,)"),
    ("C_poussee_forcee", PROGRAMME, '"push", "-q", "origin", f"HEAD:refs/heads/{branche}"',
     '"push", "-q", "-f", "origin", f"HEAD:refs/heads/{branche}"'),
    ("E_memoire_par_branche", PROGRAMME, "souvenir = constater(memoire.get(pointe, {}), maintenant)",
     'souvenir = constater(next((v for v in memoire.values() if v.get("branche") == branche), {}), maintenant)'),
    ("F_sans_frein", PROGRAMME, "    if demande_deja_ce_passage:\n", "    if False:\n"),
    ("G_cle_version", PROGRAMME, 'return f"circuit=epreuve\\nepreuves={\',\'.join(codes)}\\npointe={pointe}\\n"',
     'return f"circuit=epreuve\\nepreuves={\',\'.join(codes)}\\npointe={pointe}\\nversion=x\\n"'),
    ("H_worktree_garde", PROGRAMME,
     'lancer(["git", "-C", prive, "worktree", "remove", "--force", prive_wt], journal, tolere=True)', "pass"),
    ("I_message_a_l_ecran", PROGRAMME,
     """print("IMPOSSIBLE — une source n'a pas pu être lue ; rien n'est décidé pour la suite (détail au journal privé)")""",
     'print("IMPOSSIBLE — " + str(e))'),
    ("J_trace_a_l_ecran", PROGRAMME, 'print("PLANTAGE — exception imprévue (détail au journal privé)")',
     'print("PLANTAGE — " + traceback.format_exc())'),
    ("K_commit_a", PROGRAMME, '"--", nom], journal)\n    code, _ = lancer(', '"-a"], journal)\n    code, _ = lancer('),
    ("L_a_blanc_qui_pousse", PROGRAMME, 'option = [] if a_blanc else ["--publier"]', 'option = ["--publier"]'),
    ("M_sans_arret", PROGRAMME, 'if souvenir["echecs"] >= ECHECS_MAX:', "if False:"),
    ("N_demande_jamais_jugee", PROGRAMME, 'if s["demande"] is not None and maintenant - s["demande"] >= GARDE_S:',
     "if False:"),
    ("O_file_2_ignore", PROGRAMME, 'faits["base_file_2"] = code == 0', 'faits["base_file_2"] = True'),
    ("P_ecran_toutes_branches", PROGRAMME, "if branche in publiques:", "if True:"),
    ("Q_minute_prise_echec", PROGRAMME, 'return ATTENTE, "une demande porte déjà le nom de cette minute"',
     'return ECHEC, "une demande porte déjà le nom de cette minute"'),
    ("R_seulement_inconnue_avalee", PROGRAMME, 'raise Impossible("--seulement nomme une branche inconnue")', "pass"),
    ("S_ranger_sans_set_e", CIRCUIT, '          set -euo pipefail\n          [ -s "$RUNNER_TEMP/journal.log" ]',
     '          set -u\n          [ -s "$RUNNER_TEMP/journal.log" ]'),
    ("T_base64_non_masque", CIRCUIT, '          echo "::add-mask::$B"\n', '          true\n'),
    ("U_a_blanc_ecrit_la_memoire", PROGRAMME, "            if not a.a_blanc:\n", "            if True:\n"),
    ("V_aucune_branche_tue", PROGRAMME, '            print("publication automatique : aucune branche examinée")\n',
     "            pass\n"),
    ("Z1_perimetre_de_branche_retire", PROGRAMME, "            except Impossible as e:\n                action, motif = ECHEC",
     "            except KeyboardInterrupt as e:\n                action, motif = ECHEC"),
    ("Z2_plantage_de_table_impossible", PROGRAMME,
     '        journal.ecrire(f"table refusée par le fabricant composé (code du lecteur {code})")\n        return None',
     '        if code != 3:\n            raise Impossible("table")\n        return None'),
    ("Z3_controle_initial_retire", PROGRAMME, "            controler_le_fabricant_de_main(fabricant_main, a.travail, journal)\n",
     "            pass\n"),
    ("Z4_file_2_commun_retire", PROGRAMME,
     'lancer(["git", "-C", a.prive, "cat-file", "-e", a.commit_file_2 + "^{commit}"], journal)', "pass"),
    ("Z5_lecteur_sans_isolement", PROGRAMME, '[sys.executable, "-I", "-B", "-c", LECTEUR_DE_LA_TABLE',
     '[sys.executable, "-B", "-c", LECTEUR_DE_LA_TABLE'),
    ("Z6_fetch_commun_retire", PROGRAMME,
     '            lancer(["git", "-C", base, "fetch", "-q", "--prune", "origin"], journal)\n', "            pass\n"),
    ("Z7_fetch_local_retire", PROGRAMME,
     '        lancer(["git", "-C", public_wt, "fetch", "-q", base_publique, "+refs/remotes/origin/*:refs/remotes/origin/*"],\n'
     '               journal)\n', "        pass\n"),
    ("Z8_sonde_d_ecriture_retiree", PROGRAMME,
     '                lancer(["git", "-C", base, "push", "--dry-run", "-q", "origin",\n'
     '                        "refs/remotes/origin/main:refs/heads/" + SONDE_D_ECRITURE], journal)\n',
     "                pass\n"),
    ("Z9_frein_sur_reussite_seulement", PROGRAMME,
     '            demande_deja = demande_deja or tentative["poussee"]   # N-89 ④', "            pass   # N-89 ④"),
    ("Z10_refspec_negative_remise", PROGRAMME, '"+refs/remotes/origin/*:refs/remotes/origin/*"],',
     '"+refs/remotes/origin/*:refs/remotes/origin/*", "^refs/remotes/origin/HEAD"],'),
    ("Z11_sonde_aussi_a_blanc", PROGRAMME, "            if not a.a_blanc:   # N-89 ③", "            if True:   # N-89 ③"),
]


def preparer(racine, dossier, sabotage=None):
    """Recopie le programme, le circuit et les faux voisins dans `dossier`, sabotés ou non.

    ① RÔLE — Un code neuf par jeu.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` (le dépôt éprouvé) · `dossier` · `sabotage` : (nom, fichier, ancien, nouveau) ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None, ou la raison pour laquelle le sabotage ne s'applique pas (texte absent ou double).
      [rend: 1]
    ⑥ TRAITEMENT — Copier ; le faux fabricant, le faux module du jeton et le faux ETAT_DES_TRAVAUX à côté du
      programme, la table de main sous tests/ ; remplacer UN texte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le faux fabricant est celui que le décor commet sur main (même empreinte : « fabricant de main »).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for f in (PROGRAMME, CIRCUIT):
        os.makedirs(os.path.dirname(os.path.join(dossier, f)), exist_ok=True)
        shutil.copy(os.path.join(racine, f), os.path.join(dossier, f))
    ecrire(os.path.join(dossier, "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"), FAUX_FABRICANT)
    ecrire(os.path.join(dossier, "programmes/ETAT_DES_TRAVAUX.py"), FAUX_ETAT)
    ecrire(os.path.join(dossier, "programmes/FORME_D_UN_JETON.py"), FAUX_JETON)
    ecrire(os.path.join(dossier, "tests/LANCEMENT_DES_EPREUVES.json"), TABLE_MAIN)
    if sabotage:
        _, f, ancien, nouveau = sabotage
        chemin = os.path.join(dossier, f)
        texte = open(chemin, encoding="utf-8").read()
        if texte.count(ancien) != 1:
            return f"texte trouvé {texte.count(ancien)} fois"
        open(chemin, "w", encoding="utf-8").write(texte.replace(ancien, nouveau))
    return None


def main():
    """Joue les scénarios, puis les sabotages ; sort.

    ① RÔLE — Le programme d'épreuve.
    ② CONTEXTE D'APPEL — Voir ② du module.
    ③ ENTRÉE — Voir ③ du module.
    ④ CONDITIONS D'ENTRÉE — Voir ④ du module.
    ⑤ SORTIE — Le code (⑤ du module).
      [rend: rien]
    ⑥ TRAITEMENT — Décor ; code sain : tous les cas ; avec --saboter : pour chaque sabotage, les cas jusqu'au premier
      rouge (« mord »), arrêt au premier (tous, avec --tous-les-rouges) ; un sabotage qui laisse tout vert est une
      décoration (code 1).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir le module.
    ⑨ CE QUI CLOCHE — Un sabotage s'arrête au PREMIER cas rouge (borne de 2 min) : la liste « cas rougis » n'en nomme
      qu'un, pas tous ceux qu'il ferait rougir.
    ⑩ EFFET — Dossiers temporaires, retirés.
    ⑪ TERMINAISON — Sort par sys.exit.
      [sort: oui]
    """
    if len(sys.argv) < 2 or not os.path.isfile(os.path.join(sys.argv[1], PROGRAMME)):
        print("usage : EPREUVES_DE_LA_PUBLICATION_AUTOMATIQUE_Mer_25-11-2026.py <racine> [--saboter]")
        sys.exit(2)
    racine = os.path.abspath(sys.argv[1])
    tmp = tempfile.mkdtemp(prefix="epreuve_pub_")
    rouge = False
    try:
        modele_dir = os.path.join(tmp, "modele")
        os.makedirs(modele_dir)
        p = modele(modele_dir)
        sain = os.path.join(tmp, "sain")
        preparer(racine, sain)
        for nom, v, detail in scenarios(sain, modele_dir, p, os.path.join(tmp, "jeu_sain")):
            print(f"{'VERT ' if v else 'ROUGE'} {nom} — {detail}")
            rouge = rouge or not v
        if "--saboter" in sys.argv:
            tranche = [x[len("--tranche="):] for x in sys.argv if x.startswith("--tranche=")]
            k, nb = (int(x) for x in tranche[0].split("/")) if tranche else (1, 1)
            for s in [s for i, s in enumerate(SABOTAGES) if i % nb == k - 1]:
                d = os.path.join(tmp, "sab_" + s[0])
                raison = preparer(racine, d, s)
                if raison:
                    print(f"IMPOSSIBLE sabotage {s[0]} : {raison}")
                    sys.exit(2)
                tous = "--tous-les-rouges" in sys.argv
                tues = [nom.split()[0] for nom, v, _ in scenarios(d, modele_dir, p, os.path.join(d, "jeu"), not tous)
                        if not v]
                print(f"{'MORD   ' if tues else 'NE MORD PAS'} {s[0]} — cas rougis : {' '.join(tues) or 'aucun'}")
                rouge = rouge or not tues
    except (OSError, subprocess.SubprocessError) as e:
        print(f"IMPOSSIBLE : {type(e).__name__} : {e}")
        sys.exit(2)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("BILAN :", "ROUGE" if rouge else "TOUT VERT")
    sys.exit(1 if rouge else 0)


if __name__ == "__main__":
    main()
