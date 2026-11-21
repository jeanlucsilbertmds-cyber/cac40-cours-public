#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LIVRER_ET_INSTALLER — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Éprouve programmes/LIVRER.py, programmes/INSTALLER.py et programmes/QUI_FAIT_QUOI.py SANS RÉSEAU :
dépôts git jetables (un « privé » et un « public » nus, sous un dossier temporaire), un FAUX gh qui joue le relais,
la file du groupe long, le circuit des épreuves et les branches de résultats, un faux fabricant qui publie comme le
vrai (même garde de branche que `refus_de_branche`) et un faux garde-fou. Le rapatrieur
(tests/outils/rapatrier_les_epreuves_longues.py) et le fabricant (pour ses constantes) sont les VRAIS, copiés.

① RÔLE — Dire, cas par cas, si les trois programmes font ce que la consigne du 20-11-2026 (19h38, ajout de 19h40)
  demande, et, avec « --saboter », que chaque sabotage fait tomber au moins une épreuve.
② CONTEXTE D'APPEL — À la main : python3 -B tests/EPREUVES_DE_LIVRER_ET_INSTALLER_Ven_20-11-2026.py <racine>
  [--saboter | --saboter=S18,M1,…]. Durée mesurée : voir la note de livraison.
③ ENTRÉE — La racine du dépôt à éprouver (ses programmes/ et tests/ sont copiés) ; « --saboter ».
④ CONDITIONS D'ENTRÉE — git et python3 installés ; aucun réseau nécessaire.
⑤ SORTIE — Code 0 si toutes les épreuves passent (et, avec --saboter, si chaque sabotage mord) ; 1 sinon.
⑥ TRAITEMENT — Pour chaque cas : un monde neuf (`Monde`), un scénario du faux gh, un lancement, des vérifications
  sur l'ÉTAT des dépôts (pas sur les messages). Avec --saboter : chaque sabotage réécrit une copie des programmes,
  rejoue tous les cas, et doit en faire tomber au moins un.
⑦ UNITÉ — Secondes (durées affichées).
⑧ POURQUOI — R-731 : épreuves à la main avec sabotages ; « un jeu d'épreuves se sabote contre sa propre correction ».
⑨ CE QUI CLOCHE — Le faux fabricant ne fait pas les contrôles du vrai (provenance, étage A) : ils ont leurs propres
  épreuves. Le faux gh avance d'un pas par appel : le temps réel n'est pas éprouvé.
⑩ EFFET — Crée et efface des dossiers temporaires ; aucun réseau, aucun dépôt réel touché.
⑪ TERMINAISON — Sort du programme par sys.exit ; chaque lancement est borné à 300 s.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

# Les cas choisis par « --cas=I13,L15 » (vide : tous) ; essais courts d'un défaut sans rejouer les 43 cas (21-11-2026).
CHOISIS = set()


def choisi(nom):
    """Dit si le cas `nom` est à jouer.

    ① RÔLE — Restreindre un essai aux cas nommés par --cas=. ② CONTEXTE D'APPEL — Chaque famille de cas.
    ③ ENTRÉE — `nom` : « L15 », ou un préfixe de famille (« R », « Q »). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si aucun choix n'est fait, si un cas choisi est `nom`, si un choix de famille
      (lettres seules, « R ») est le début de `nom`, ou si `nom` est une famille dont un cas est choisi.
      [rend: 1]
    ⑥ TRAITEMENT — —. ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage rejoue les 43 cas (plus de 2 minutes).
    ⑨ CE QUI CLOCHE — Un essai restreint ne dit rien des autres cas. ⑩ EFFET — —. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return not CHOISIS or any(c == nom or (c.isalpha() and nom.startswith(c)) or (nom.isalpha() and c.startswith(nom))
                              for c in CHOISIS)


PROGRAMMES = ("LIVRER.py", "INSTALLER.py", "QUI_FAIT_QUOI.py", "REPUBLIER.py", "CONTRATS_DES_FICHIERS.py",
              # 21-11-2026 (N-7, N-11) : le fabricant et le module qu'il charge à côté de lui, pour que R5 et R8 lisent
              # la copie, sabotable, et non le dépôt
              "FABRIQUER_LE_CIRCUIT_PUBLIC.py", "FORME_D_UN_JETON.py")

FAUX_GH = r'''#!/usr/bin/env python3
import json, os, subprocess, sys, tempfile
E = os.environ["FAUX_GH_ETAT"]; PUB = os.environ["FAUX_PUBLIC"]; PRIV = os.environ["FAUX_PRIVE"]
s = json.load(open(E))
def heure():
    s["t"] += 7
    t = s["t"]; return "2026-11-20T%02d:%02d:%02dZ" % (10 + t // 3600, (t // 60) % 60, t % 60)
def g(*a, d=None):
    return subprocess.run(["git"] + list(a), cwd=d, capture_output=True, text=True)
def resultats(r):
    for code in r["codes"]:
        w = tempfile.mkdtemp()
        g("init", "-q", d=w)
        base = os.path.join(w, "rapports", "epreuves_longues", str(r["databaseId"]), code)
        os.makedirs(base)
        json.dump([{"code": c} for c in r["codes"]], open(os.path.join(base, "DEMANDE.json"), "w"))
        cs = s.get("codes_de_sortie", {}).get(code, 0)
        jouee = "f" * 40 if s.get("pointe_fausse") else r.get("pointe", "")
        if code not in s.get("sans_resultat", []):
            json.dump({"code_epreuve": code, "chemin": "tests/X.py", "arguments": [], "duree_secondes": 123,
                       "code_de_sortie": cs, "pointe_jouee": jouee}, open(os.path.join(base, "RESULTAT.json"), "w"))
        open(os.path.join(base, "SORTIE.txt"), "w").write("sortie\n")
        g("add", "-A", d=w); g("commit", "-q", "-m", "resultat", d=w)
        g("push", "-q", PRIV, "HEAD:refs/heads/epreuves-longues/%d/%s" % (r["databaseId"], code), d=w)
        subprocess.run(["rm", "-rf", w])
def avancer():
    for r in s["runs"]:
        if r["status"] != "completed" and r.get("ticks", 0) >= 0:
            r["ticks"] -= 1
            if r["ticks"] == 0:
                r["status"], r["conclusion"] = "completed", "success"
                if r["workflowName"] == "epreuves_longues.yml" and r["repo"] == "faux/public" and "codes" in r:
                    resultats(r)
                    if s.get("tiers"):
                        w = tempfile.mkdtemp()
                        g("clone", "-q", "-b", r["headBranch"], PRIV, w)
                        open(os.path.join(w, "tiers.txt"), "w").write("poussé par un tiers pendant le passage\n")
                        g("add", "tiers.txt", d=w); g("commit", "-q", "-m", "tiers", d=w); g("push", "-q", "origin", r["headBranch"], d=w)
                        subprocess.run(["rm", "-rf", w])
    for b in g("for-each-ref", "--format=%(refname:short)", "refs/heads", d=PUB).stdout.split():
        for sha in g("log", "--format=%H", "--diff-filter=A", b, "--", "demandes/", d=PUB).stdout.split():
            if sha in s["vus"]:
                continue
            s["vus"].append(sha)
            occupe = any(r["status"] != "completed" and r["repo"] == "faux/public"
                         and r["workflowName"] in ("series_longues.yml", "epreuves_longues.yml") for r in s["runs"])
            issue = s["relais"].pop(0) if s["relais"] else "ok"
            if occupe:
                issue = "occupe"
            s["n"] += 1
            relais = {"databaseId": s["n"], "repo": "faux/public", "workflowName": "demande_de_serie.yml",
                      "headBranch": b, "headSha": sha, "event": "push", "status": "completed",
                      "conclusion": "success" if issue == "ok" else "failure", "createdAt": heure(), "issue": issue}
            s["runs"].append(relais)
            if issue == "ok":
                f = g("diff-tree", "--no-commit-id", "--name-only", "-r", sha, d=PUB).stdout.split()[0]
                txt = g("show", "%s:%s" % (sha, f), d=PUB).stdout
                codes = [l.split("=", 1)[1] for l in txt.splitlines() if l.startswith("epreuves=")][0].split(",")
                pointe = [l.split("=", 1)[1] for l in txt.splitlines() if l.startswith("pointe=")][0]
                s["n"] += 1
                s["runs"].append({"databaseId": s["n"], "repo": "faux/public", "workflowName": "epreuves_longues.yml",
                                  "headBranch": b, "headSha": sha, "event": "workflow_dispatch",
                                  "status": "in_progress", "conclusion": "", "createdAt": heure(),
                                  "ticks": s.get("duree", 3), "codes": codes, "pointe": pointe})
                for etat in s.pop("jumeau", []):
                    s["n"] += 1
                    s["runs"].append({"databaseId": s["n"], "repo": "faux/public", "workflowName": "epreuves_longues.yml",
                                      "headBranch": b, "headSha": sha, "event": "workflow_dispatch", "status": etat,
                                      "conclusion": "success" if etat == "completed" else "", "createdAt": heure(),
                                      "ticks": -10 ** 9})
a = sys.argv[1:]
open(E + ".appels", "a").write(" ".join(a) + "\n")
avancer()
def opt(n):
    return a[a.index(n) + 1] if n in a else None
repo = opt("--repo")
if a[:2] == ["run", "list"]:
    out = [r for r in s["runs"] if r["repo"] == repo
           and (opt("--workflow") is None or r["workflowName"] == opt("--workflow"))
           and (opt("--branch") is None or r["headBranch"] == opt("--branch"))
           and (opt("--event") is None or r["event"] == opt("--event"))]
    out = sorted(out, key=lambda r: r["createdAt"], reverse=True)
    print(json.dumps(out))
elif a[:2] == ["run", "view"]:
    r = [r for r in s["runs"] if str(r["databaseId"]) == a[2] and r["repo"] == repo]
    if not r:
        print("run not found", file=sys.stderr); json.dump(s, open(E, "w")); sys.exit(1)
    if "--log-failed" in a:
        if r[0].get("issue") == "occupe":
            print("::error::DEMANDE REFUSEE : 1 passage(s) de epreuves_longues.yml en cours ou en attente ; redeposer")
        else:
            print("::error::DEMANDE REFUSEE : cle inconnue : x")
    else:
        print(json.dumps(r[0]))
else:
    print("commande inconnue", file=sys.stderr); json.dump(s, open(E, "w")); sys.exit(1)
json.dump(s, open(E, "w"))
'''

FAUX_FABRICANT = r'''#!/usr/bin/env python3
import os, subprocess, sys
prive, public = sys.argv[1], sys.argv[2]
open(os.environ["FAUX_FAB_LOG"], "a").write(" ".join(sys.argv[3:]) + "\n")
def g(d, *a):
    return subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
bp = g(prive, "symbolic-ref", "-q", "--short", "HEAD").stdout.strip()
bq = g(public, "symbolic-ref", "-q", "--short", "HEAD").stdout.strip()
if not bp or bp != bq:
    print("ARRET — le clone public est sur %r, le prive sur %r" % (bq, bp)); sys.exit(1)
sha = g(prive, "rev-parse", "HEAD").stdout.strip()
if os.environ.get("FAUX_FAB_MUET") and "--publier" not in sys.argv:   # muet à blanc seulement (N-4)
    sys.exit(0)
if os.environ.get("FAUX_FAB_IGNORE"):
    open(os.path.join(public, "ignore.txt"), "w").write(sha + "\n")
open(os.path.join(public, "version.txt"), "w").write(sha + "\n")
open(os.path.join(public, "code.txt"), "w").write(open(os.path.join(prive, "programmes", "CODE.py")).read())
if "--publier" in sys.argv:
    if os.environ.get("FAUX_FAB_REFUSE"):
        print("ARRET — publication refusee (scenario)"); sys.exit(1)
    g(public, "add", "version.txt", "code.txt")
    if g(public, "diff", "--cached", "--quiet").returncode:
        g(public, "commit", "-q", "-m", "code publie de la version %s, commit %s" % (bp, sha[:12]))
    p = g(public, "push", "-q", "origin", "HEAD:refs/heads/" + bp)
    if p.returncode:
        print("ARRET poussee", p.stderr); sys.exit(1)
    print("publie : %s = %s" % (bp, g(public, "rev-parse", "HEAD").stdout.strip()[:12]))
'''

FAUX_GARDE_FOU = r'''#!/usr/bin/env python3
import hashlib, re, sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
corps = re.sub(r"\n<!-- CONTROLE [0-9a-f]{16} [^\n]*-->\s*$", "", t).rstrip("\n")
e = hashlib.sha256(corps.encode()).hexdigest()[:16]
if "REFUSE_MOI" in t:
    print("REFUSE"); sys.exit(1)
if "--verifier" in sys.argv:
    m = re.search(r"<!-- CONTROLE ([0-9a-f]{16}) [^\n]*-->\s*$", t)
    if not m or m.group(1) != e:
        print("AUCUNE LIGNE DE CONTROLE ou EMPREINTE DIFFERENTE"); sys.exit(1)
    print("validee et intacte"); sys.exit(0)
open(p, "w", encoding="utf-8").write(corps + "\n\n<!-- CONTROLE %s · 2026-11-20 20:00 Paris -->\n" % e)
print("acceptee")
'''

NOTE = """DÉCIDÉ · Rôle : porter le travail soumis à relecture.

# NOTE D'ÉPREUVE

## À JOUER SUR GITHUB
{liste}

## DEMANDE DE RELECTURE PAR COWORK
Épreuves longues à lire sur GitHub, ne pas les rejouer.
"""


class Monde:
    """Un monde jetable : dépôt privé et public nus, un clone privé, le faux gh, ses scénarios.

    ① RÔLE — Donner à chaque cas des dépôts neufs, sans réseau.
    ② CONTEXTE D'APPEL — Chaque cas.
    ③ ENTRÉE — `source` : la racine éprouvée · `progs` : le dossier des programmes (copiés, sabotés ou non) ·
      `codes` : la section « à jouer » de la note.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — Voir __init__.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un état partagé entre cas masquerait un défaut.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée un dossier temporaire.
    ⑪ TERMINAISON — —
    """

    def __init__(self, source, progs, liste="- `CircuitPublic`\n- `GardeFou`", code_change=True):
        """Bâtit le monde.

        ① RÔLE — Dépôts, outils faux, état du faux gh.
        ② CONTEXTE D'APPEL — Chaque cas.
        ③ ENTRÉE — `self` · `source` · `progs` · `liste` : les éléments de la section « à jouer » · `code_change` :
          faux pour un travail qui ne change que echanges/ (N-3 : « aucune » n'est cru que pour lui).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — Dépôt de départ (code, fabricant et table copiés, rapatrieur copié, note contrôlée) poussé
          sur main et travail-x d'un privé nu ; public nu avec un main ; clone privé ; outils faux écrits.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit sous un dossier temporaire.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        self.t = tempfile.mkdtemp(prefix="epreuve_livrer_")
        self.progs = progs
        self.prive, self.public = os.path.join(self.t, "prive.git"), os.path.join(self.t, "public.git")
        self.clone = os.path.join(self.t, "clone")
        self.etat = os.path.join(self.t, "gh.json")
        self.env = dict(os.environ, GIT_AUTHOR_NAME="Claude", GIT_AUTHOR_EMAIL="c@x", GIT_COMMITTER_NAME="Claude",
                        GIT_COMMITTER_EMAIL="c@x", LIVRER_GH=os.path.join(self.t, "gh"),
                        LIVRER_DEPOT_PUBLIC=self.public, LIVRER_REPO_PUBLIC="faux/public",
                        LIVRER_REPO_PRIVE="faux/prive", LIVRER_FABRICANT=os.path.join(self.t, "fab.py"),
                        LIVRER_GARDE_FOU=os.path.join(self.t, "garde.py"), LIVRER_PAS="0", LIVRER_SANS_ATTENTE_DE_MINUTE="1", FAUX_GH_ETAT=self.etat,
                        FAUX_PUBLIC=self.public, FAUX_PRIVE=self.prive, PYTHONDONTWRITEBYTECODE="1",
                        FAUX_FAB_LOG=os.path.join(self.t, "fab.log"))
        for nom, texte in (("gh", FAUX_GH), ("fab.py", FAUX_FABRICANT), ("garde.py", FAUX_GARDE_FOU)):
            with open(os.path.join(self.t, nom), "w") as f:
                f.write(texte)
            os.chmod(os.path.join(self.t, nom), 0o755)
        self.scenario()
        dep = os.path.join(self.t, "depart")
        for d in ("programmes", "tests/outils", "echanges"):
            os.makedirs(os.path.join(dep, d))
        for rel in ("programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py", "programmes/CONTRATS_DES_FICHIERS.py",
                    "tests/LANCEMENT_DES_EPREUVES.json", "tests/outils/rapatrier_les_epreuves_longues.py",
                    ".gitattributes"):
            shutil.copyfile(os.path.join(source, rel), os.path.join(dep, rel))
        with open(os.path.join(dep, "programmes", "CODE.py"), "w") as f:
            f.write("V = 1\n")
        with open(os.path.join(dep, "echanges", "A_RELIRE.md"), "w") as f:
            f.write(NOTE.format(liste=liste))
        self.git(None, "init", "-q", "--bare", "-b", "main", self.prive)
        self.git(None, "init", "-q", "--bare", "-b", "main", self.public)
        self.git(dep, "init", "-q", "-b", "main")
        self.git(dep, "add", "-A")
        self.git(dep, "commit", "-q", "-m", "départ")
        self.git(dep, "push", "-q", self.prive, "main")
        self.git(dep, "push", "-q", self.public, "main")
        self.git(dep, "checkout", "-q", "-b", "travail-x")
        self.lancer([sys.executable, os.path.join(self.t, "garde.py"), "echanges/A_RELIRE.md"], dep)
        with open(os.path.join(dep, "programmes", "CODE.py") if code_change
                  else os.path.join(dep, "echanges", "TRAVAIL.md"), "w") as f:
            f.write("V = 2\n")
        self.git(dep, "add", "-A")
        self.git(dep, "commit", "-q", "-m", "travail")
        self.git(dep, "push", "-q", self.prive, "travail-x")
        self.git(None, "clone", "-q", self.prive, self.clone)

    def scenario(self, **k):
        """Écrit l'état de départ du faux gh.

        ① RÔLE — Régler le scénario d'un cas.
        ② CONTEXTE D'APPEL — Les cas.
        ③ ENTRÉE — `self` · `k` : relais (issues forcées), codes_de_sortie, runs (passages déjà là), duree,
          sans_resultat.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — JSON écrit.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit un fichier.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        s = {"t": 0, "n": 9000, "runs": [], "vus": [], "relais": []}
        s.update(k)
        with open(self.etat, "w") as f:
            json.dump(s, f)

    def gh_etat(self):
        """Rend l'état du faux gh.

        ① RÔLE — Lire ce que GitHub (faux) a vu. ② CONTEXTE D'APPEL — Les vérifications.
        ③ ENTRÉE — `self`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le dict.
          [rend: 1]
        ⑥ TRAITEMENT — json.load. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        with open(self.etat) as f:
            return json.load(f)

    def lancer(self, commande, dossier):
        """Lance une commande dans l'environnement du monde ; rend le résultat.

        ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — Partout.
        ③ ENTRÉE — `self` · `commande` · `dossier`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : CompletedProcess.
          [rend: 1]
        ⑥ TRAITEMENT — subprocess.run, 300 s. ⑦ UNITÉ — Secondes. ⑧ POURQUOI — Aucune attente sans borne.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Celui de la commande.
        ⑪ TERMINAISON — Rend la main, ou lève TimeoutExpired.
          [sort: non]
        """
        return subprocess.run(commande, cwd=dossier, capture_output=True, text=True, timeout=300, env=self.env)

    def git(self, dossier, *a):
        """git dans le monde ; rend la sortie.

        ① RÔLE — Raccourci. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — `self` · `dossier` · `a`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le texte de sortie.
          [rend: 1]
        ⑥ TRAITEMENT — `lancer`. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Celui de git.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return self.lancer(["git"] + list(a), dossier).stdout

    def programme(self, nom, *args):
        """Lance un programme éprouvé depuis le clone ; rend le résultat.

        ① RÔLE — Le lancement sous épreuve. ② CONTEXTE D'APPEL — Les cas.
        ③ ENTRÉE — `self` · `nom` · `args`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : CompletedProcess.
          [rend: 1]
        ⑥ TRAITEMENT — python3 -B <progs>/<nom> args, dossier = le clone. ⑦ UNITÉ — —
        ⑧ POURQUOI — Les programmes vivent hors du clone : le clone reste propre (INSTALLER l'exige).
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Celui du programme.
        ⑪ TERMINAISON — Rend la main ; un programme qui dépasse 300 s rend le code 124.
          [sort: non]
        """
        try:
            return self.lancer([sys.executable, "-B", os.path.join(self.progs, nom)] + list(args), self.clone)
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(nom, 124, "arrêté après 300 s", "")

    def montrer(self, ref, chemin, depot=None):
        """Rend le contenu d'un fichier à une référence d'un dépôt nu, ou « ».

        ① RÔLE — Lire l'état poussé. ② CONTEXTE D'APPEL — Les vérifications.
        ③ ENTRÉE — `self` · `ref` · `chemin` · `depot`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le texte.
          [rend: 1]
        ⑥ TRAITEMENT — git show. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return self.git(depot or self.prive, "show", f"{ref}:{chemin}")

    def entrees(self, ref):
        """Rend les entrées du registre des travaux poussées à une référence du privé nu.

        ① RÔLE — Lire le registre comme QUI_FAIT_QUOI le lit, sans le programme éprouvé. ② CONTEXTE D'APPEL — Les
        vérifications. ③ ENTRÉE — `self` · `ref`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la liste des dicts.
          [rend: 1]
        ⑥ TRAITEMENT — « git ls-tree » du dossier etudes/REGISTRE_DES_TRAVAUX/, puis « git show » de chaque *.json.
        ⑦ UNITÉ — — ⑧ POURQUOI — Un fichier par entrée (consigne du 20-11-2026 au soir, point C).
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        noms = [n for n in self.git(self.prive, "ls-tree", "--name-only", ref, "--",
                                    "etudes/REGISTRE_DES_TRAVAUX/").splitlines() if n.endswith(".json")]
        return [json.loads(self.git(self.prive, "show", f"{ref}:{n}")) for n in noms]

    def fermer(self):
        """Efface le monde et les worktrees jetables qu'il aurait laissés.

        ① RÔLE — Ne rien laisser. ② CONTEXTE D'APPEL — Fin de chaque cas. ③ ENTRÉE — `self`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — Les worktrees du clone sous /tmp/livrer_ retirés ; le dossier du monde effacé.
        ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Efface. ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        for l in self.git(self.clone, "worktree", "list", "--porcelain").splitlines():
            if l.startswith("worktree /tmp/livrer_"):
                self.git(self.clone, "worktree", "remove", "--force", l.split(" ", 1)[1])
        shutil.rmtree(self.t, ignore_errors=True)


PLANTEUR = r"""import builtins, os
_marque = os.environ.get("PLANTER_SUR")
if _marque:
    _vrai = builtins.print
    def print(*a, **k):
        if a and isinstance(a[0], str) and a[0].startswith(_marque):
            raise RuntimeError("plantage simule par l epreuve")
        return _vrai(*a, **k)
    builtins.print = print
"""


def planter(m, marque):
    """Fait lever une exception au premier affichage qui commence par `marque` (épreuve du code 5).

    ① RÔLE — Simuler un plantage à un point précis, SANS crochet dans le code éprouvé. ② CONTEXTE D'APPEL — L11, I10.
    ③ ENTRÉE — `m` : le monde · `marque` : le début de la ligne affichée. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Un sitecustomize.py dans un dossier du monde, mis en tête de PYTHONPATH, remplace print.
    ⑦ UNITÉ — — ⑧ POURQUOI — « un plantage après la fusion donne 5, jamais 1 » (consigne du 20-11-2026 au soir).
    ⑨ CE QUI CLOCHE — Les autres programmes du monde (faux gh, faux fabricant) héritent du remplacement : leurs
      affichages ne commencent jamais par la marque. ⑩ EFFET — Écrit un fichier. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    d = os.path.join(m.t, "planteur")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "sitecustomize.py"), "w") as f:
        f.write(PLANTEUR)
    m.env.update(PYTHONPATH=d, PLANTER_SUR=marque)


def pointe_de(m, ref="travail-x"):
    """Rend la pointe d'une branche du privé nu. ① RÔLE — Raccourci. ② CONTEXTE D'APPEL — Les cas.
    ③ ENTRÉE — `m` · `ref`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le commit. [rend: 1]
    ⑥ TRAITEMENT — rev-parse. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    return m.git(m.prive, "rev-parse", ref).strip()


def preuve(m, code, pointe, sortie=0, passage=9500):
    """Pousse au privé nu une branche de résultat epreuves-longues/<passage>/<code>, comme le circuit.

    ① RÔLE — Donner à INSTALLER une preuve GitHub sans GitHub. ② CONTEXTE D'APPEL — Les cas I.
    ③ ENTRÉE — `m` · `code` · `pointe` : la pointe jouée écrite · `sortie` : le code de sortie · `passage`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Dépôt neuf, commit SANS PARENT de rapports/epreuves_longues/<passage>/<code>/RESULTAT.json (forme
      du circuit : `pas_de_depot` du fabricant), poussé.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au privé nu. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    w = tempfile.mkdtemp(dir=m.t)
    m.git(w, "init", "-q")
    base = os.path.join(w, "rapports", "epreuves_longues", str(passage), code)
    os.makedirs(base)
    with open(os.path.join(base, "RESULTAT.json"), "w") as f:
        json.dump({"code_epreuve": code, "code_de_sortie": sortie, "duree_secondes": 1, "pointe_jouee": pointe}, f)
    m.git(w, "add", "-A")
    m.git(w, "commit", "-q", "-m", "resultat")
    m.git(w, "push", "-q", m.prive, f"HEAD:refs/heads/epreuves-longues/{passage}/{code}")


def relu(m, verdict="DÉPLOYABLE", auteur="cowork", pointe=None, apres=None, avant_relu=None, ranger=None):
    """Pousse un RELU sur travail-x, comme Cowork (ou un autre), et au besoin un changement avant ou après lui.

    ① RÔLE — Préparer une installation. ② CONTEXTE D'APPEL — Les cas I.
    ③ ENTRÉE — `m` : le monde · `verdict` · `auteur` · `pointe` : la pointe relue écrite (défaut : la pointe au
      moment du RELU) · `apres` : un chemin modifié après le RELU, ou None · `avant_relu` : un chemin modifié et
      commité avant le RELU (comme la note réécrite par LIVRER), ou None · `ranger` : un programme rangé en archives/
      APRÈS le RELU (« git mv », relecture de Cowork D-2), ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la pointe relue écrite.
      [rend: 1]
    ⑥ TRAITEMENT — clone travail-x dans un dossier du monde ; RELU commité sous l'auteur donné ; poussé.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au privé nu.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    w = os.path.join(m.t, "relecteur")
    m.git(None, "clone", "-q", "-b", "travail-x", m.prive, w)
    if avant_relu:
        with open(os.path.join(w, avant_relu), "a") as f:
            f.write("ajout de LIVRER\n")
        subprocess.run(["git", "commit", "-q", "-am", "note de LIVRER"], cwd=w, env=m.env)
    tete = m.git(w, "rev-parse", "HEAD").strip()
    with open(os.path.join(w, "echanges", "RELU.md"), "w") as f:
        f.write(f"DÉCIDÉ · Rôle : porter la relecture du travail soumis.\n\nRELU PAR : Cowork · branche travail-x · "
                f"pointe relue {pointe or tete}\n\n## VERDICT : {verdict}\n")
    env = dict(m.env, GIT_AUTHOR_NAME=auteur, GIT_COMMITTER_NAME=auteur)
    subprocess.run(["git", "add", "-A"], cwd=w, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "RELU"], cwd=w, env=env)
    if apres:
        with open(os.path.join(w, apres), "a") as f:
            f.write("# changé après la relecture\n")
        subprocess.run(["git", "commit", "-q", "-am", "après"], cwd=w, env=m.env)
    if ranger:
        os.makedirs(os.path.join(w, "archives"), exist_ok=True)
        subprocess.run(["git", "mv", ranger, "archives/" + os.path.basename(ranger)], cwd=w, env=m.env)
        subprocess.run(["git", "commit", "-q", "-m", "rangé en archives"], cwd=w, env=m.env)
    subprocess.run(["git", "push", "-q", "origin", "travail-x"], cwd=w, env=m.env)
    m.git(m.clone, "fetch", "-q", "origin")
    return pointe or tete


def cas_livrer(progs, source):
    """Les cas de LIVRER ; rend la liste des (nom, vrai si passé, détail).

    ① RÔLE — Éprouver LIVRER.py. ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `progs` : le dossier des programmes · `source` : la racine éprouvée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — L1 chemin nominal ; L2 file occupée (attente) ; L2b relais qui refuse une fois (redépôt) ;
      L3 épreuve rouge ; L4 nom sans code ; L5 note refusée ; L6 branche locale en avance ; L7 plafond, file
      « queued » (M2) ; L8 épreuve absente → 3, jamais verte (M1) ; L9a deux passages vivants → 3 (M3) ; L9b un fini et
      un vivant de la même branche → 3 (M3) ; L10 un ancien passage fini de la branche n'est pas pris (M4) ;
      L11 plantage → 5, registre poussé ; L12 un tiers pousse pendant le passage : rien n'est perdu ; L13 résultat
      d'une autre pointe → 3 ; L14 publication refusée → 3 (son clone public effacé : R0, sabotage S18) ; L15 note
      « aucune » sur un travail qui change du code → 2 (N-3) ; L16 « aucune autre que `X` » → 2 (N-3) ; L17 la même
      note sur un travail sans code changé → 2 (N-3 : X n'est pas perdu) ; L18 fabricant muet → 3, aucune demande
      (N-4 : le clone de contrôle n'est pas réécrit).
    ⑦ UNITÉ — — ⑧ POURQUOI — Consigne du 20-11-2026 (19h38) et réparation du soir (points C et D).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Mondes jetables.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = []
    LISTES = {"L4": {"liste": "- `CircuitPublic`\n- `UneEpreuveSansCode`"},
              "L15": {"liste": "- aucune"},
              "L16": {"liste": "- aucune autre que `CircuitPublic`"},
              "L17": {"liste": "- aucune autre que `CircuitPublic`", "code_change": False}}

    def nominal(m, p, nom, demandes=1):
        """Vérifie l'état après un lancement qui doit rendre 0 ; rend (vrai, détail).

        ① RÔLE — Les propriétés du chemin nominal. ② CONTEXTE D'APPEL — L1, L2, L2b, L10, L12.
        ③ ENTRÉE — `m` · `p` : le résultat · `nom` · `demandes` : le nombre de demandes attendu.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : vrai si tout tient, le détail.
          [rend: 2]
        ⑥ TRAITEMENT — code 0 ; public travail-x porte la pointe jouée (publication faite, sur branche nommée) ;
          UN passage des épreuves lancé par le relais, FINI chez le faux gh ; note poussée avec « RÉSULTATS GITHUB »,
          ce numéro et « 123 s » (lu dans RESULTAT.json) ; registre poussé avec une entrée finie « code 0 » par
          épreuve ; nombre de demandes.
        ⑦ UNITÉ — — ⑧ POURQUOI — « Cowork avant GitHub », « publication sautée », « branche détachée ».
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        s = m.gh_etat()
        ep = [x for x in s["runs"] if x["workflowName"] == "epreuves_longues.yml" and x["headBranch"] == "travail-x"
              and x["databaseId"] > 9000]
        note = m.montrer("travail-x", "echanges/A_RELIRE.md")
        entrees = m.entrees("travail-x")
        version = m.montrer("travail-x", "version.txt", m.public).strip()
        relais = [x for x in s["runs"] if x["workflowName"] == "demande_de_serie.yml"]
        verifs = {
            "code 0": p.returncode == 0,
            "publié (version publique = pointe jouée)": bool(version) and f"pointe jouée {version}" in note,
            "un seul passage d'épreuves, fini": len(ep) == 1 and ep[0]["status"] == "completed",
            "note : résultats lus": "## RÉSULTATS GITHUB" in note and ep and f"Passage {ep[0]['databaseId']}" in note
                                    and note.count("· 123 s") == 2,
            "note recontrôlée": re.search(r"<!-- CONTROLE [0-9a-f]{16}", (note.strip().splitlines() or [""])[-1])
                                is not None,
            "registre : épreuves finies": len([e for e in entrees if e["executant"] == "github"
                                               and e["etape"].startswith("epreuve:") and e["resultat"] == "code 0"]) == 2,
            f"{demandes} demande(s)": len(relais) == demandes,
        }
        rates = [k for k, v in verifs.items() if not v]
        return not rates, f"{nom} : " + ("ok" if not rates else "RATÉ " + ", ".join(rates) + " · " + p.stdout[-300:])

    def un(nom, regler, verifier, *args):
        """Joue un cas dans un monde neuf ; ajoute son résultat.

        ① RÔLE — Factoriser monde, lancement, vérification, effacement. ② CONTEXTE D'APPEL — Chaque cas L.
        ③ ENTRÉE — `nom` · `regler(m)` : prépare le monde · `verifier(m, p)` : rend (vrai, détail) · `args` : ceux de
          LIVRER après la branche. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — Monde, réglage, LIVRER, vérification, fermeture. ⑦ UNITÉ — — ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Monde jetable. ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if not choisi(nom):
            return
        m = Monde(source, progs, **LISTES.get(nom, {}))
        try:
            regler(m)
            p = m.programme("LIVRER.py", "travail-x", *args)
            ok, d = verifier(m, p)
            r.append((nom, ok, d))
        finally:
            m.fermer()

    def rien(m):
        """Aucun réglage. ① RÔLE — Cas nominal. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — — ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main. [sort: non]"""

    occupant = {"databaseId": 1, "repo": "faux/public", "workflowName": "series_longues.yml", "headBranch": "main",
                "headSha": "0", "event": "workflow_dispatch", "status": "in_progress", "conclusion": "",
                "createdAt": "2026-11-20T09:00:00Z", "ticks": 4}
    un("L1", rien, lambda m, p: nominal(m, p, "L1 nominal"))
    un("L2", lambda m: m.scenario(runs=[occupant]), lambda m, p: nominal(m, p, "L2 file occupée : attendre puis déposer"))
    un("L2b", lambda m: m.scenario(relais=["occupe", "ok"]),
       lambda m, p: nominal(m, p, "L2b relais qui refuse une fois : redéposer", demandes=2))
    un("L3", lambda m: m.scenario(codes_de_sortie={"GardeFou": 1}),
       lambda m, p: (p.returncode == 1 and "- GardeFou : code 1" in m.montrer("travail-x", "echanges/A_RELIRE.md"),
                     f"L3 épreuve rouge → 1 : code {p.returncode}"))
    un("L4", rien, lambda m, p: (p.returncode == 2 and not m.gh_etat()["vus"],
                                 f"L4 nom sans code → 2, aucune demande : code {p.returncode}"))

    def note_modifiee(m):
        """Pousse une note modifiée après son contrôle. ① RÔLE — Régler L5. ② CONTEXTE D'APPEL — L5.
        ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — clone, ajout, poussée.
        ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        w = os.path.join(m.t, "w5")
        m.git(None, "clone", "-q", "-b", "travail-x", m.prive, w)
        with open(os.path.join(w, "echanges", "A_RELIRE.md"), "a") as f:
            f.write("ajout après contrôle\n")
        m.git(w, "commit", "-q", "-am", "note modifiée")
        m.git(w, "push", "-q", "origin", "travail-x")
    un("L5", note_modifiee, lambda m, p: (p.returncode == 3 and not m.montrer("travail-x", "version.txt", m.public),
                                          f"L5 note non recontrôlée → 3, rien publié : code {p.returncode}"))

    def commit_local(m):
        """Laisse un commit local non poussé sur travail-x. ① RÔLE — Régler L6. ② CONTEXTE D'APPEL — L6.
        ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — worktree, commit,
        retrait. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit. ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        m.git(m.clone, "branch", "-q", "travail-x", "origin/travail-x")
        w = os.path.join(m.t, "w6")
        m.git(m.clone, "worktree", "add", "-q", w, "travail-x")
        with open(os.path.join(w, "local.txt"), "w") as f:
            f.write("non poussé\n")
        m.git(w, "add", "local.txt")
        m.git(w, "commit", "-q", "-m", "commit local")
        m.local = m.git(w, "rev-parse", "HEAD").strip()
        m.git(m.clone, "worktree", "remove", "--force", w)
    un("L6", commit_local, lambda m, p: (p.returncode == 3 and m.git(m.clone, "rev-parse", "refs/heads/travail-x").strip()
                                         == m.local, f"L6 commit local non poussé → 3 et gardé : code {p.returncode}"))
    un("L7", lambda m: m.scenario(runs=[{"databaseId": 1, "repo": "faux/public", "workflowName": "epreuves_longues.yml",
                                         "headBranch": "main", "headSha": "0", "event": "workflow_dispatch",
                                         "status": "queued", "conclusion": "", "createdAt": "2026-11-20T09:00:00Z",
                                         "ticks": -10 ** 9, "codes": []}]),
       lambda m, p: (p.returncode == 3 and not m.gh_etat()["vus"],
                     f"L7 file « queued » jamais libre → 3 au plafond, aucune demande : code {p.returncode}"), "--plafond=0")
    un("L8", lambda m: m.scenario(sans_resultat=["GardeFou"]),
       lambda m, p: (p.returncode == 3 and "- GardeFou : code ABSENTE" in m.montrer("travail-x", "echanges/A_RELIRE.md"),
                     f"L8 épreuve sans RESULTAT.json → 3, jamais verte (M1) : code {p.returncode}"))
    un("L9a", lambda m: m.scenario(jumeau=["in_progress"]),
       lambda m, p: (p.returncode == 3 and "2 passages des épreuves" in p.stdout,
                     f"L9a deux passages vivants pour une demande → 3 (M3) : code {p.returncode}"))
    un("L9b", lambda m: m.scenario(jumeau=["completed"]),
       lambda m, p: (p.returncode == 3 and "2 passages des épreuves" in p.stdout,
                     f"L9b un passage fini et un vivant de la même branche → 3 (M3) : code {p.returncode}"))
    un("L10", lambda m: m.scenario(runs=[{"databaseId": 1, "repo": "faux/public", "workflowName": "epreuves_longues.yml",
                                          "headBranch": "travail-x", "headSha": "0", "event": "workflow_dispatch",
                                          "status": "completed", "conclusion": "failure",
                                          "createdAt": "2026-11-20T09:00:00Z", "ticks": 0}]),
       lambda m, p: nominal(m, p, "L10 un ancien passage fini de la branche n'est pas pris (filtre createdAt, M4)"))

    def apres_plantage(m, p):
        """Vérifie L11. ① RÔLE — Code 5 et rien perdu. ② CONTEXTE D'APPEL — L11. ③ ENTRÉE — `m`, `p`.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : vrai, détail. [rend: 2] ⑥ TRAITEMENT — code 5 ; le
        registre poussé porte l'entrée « publication ». ⑦ UNITÉ — — ⑧ POURQUOI — Point C. ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        pub = [e for e in m.entrees("travail-x") if e["etape"] == "publication"]
        return (p.returncode == 5 and len(pub) == 1 and "PLANTAGE" in p.stdout,
                f"L11 plantage après la publication → 5 (jamais 1 ni 3), registre poussé : code {p.returncode}, "
                f"entrées publication {len(pub)}")
    un("L11", lambda m: planter(m, "ÉTAPE 2 — publié"), apres_plantage)

    def apres_tiers(m, p):
        """Vérifie L12. ① RÔLE — Rien perdu. ② CONTEXTE D'APPEL — L12. ③ ENTRÉE — `m`, `p`.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — nominal, et le fichier du tiers
        est sur la branche. ⑦ UNITÉ — — ⑧ POURQUOI — Point D. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        ok, d = nominal(m, p, "L12 un tiers pousse pendant le passage : ni la note ni le registre ne sont perdus")
        tiers = bool(m.montrer("travail-x", "tiers.txt"))
        return ok and tiers, d + ("" if tiers else " · fichier du tiers perdu")
    un("L12", lambda m: m.scenario(tiers=True), apres_tiers)
    un("L13", lambda m: m.scenario(pointe_fausse=True),
       lambda m, p: (p.returncode == 3 and "AUTRE POINTE" in m.montrer("travail-x", "echanges/A_RELIRE.md"),
                     f"L13 RESULTAT.json d'une autre pointe → 3 : code {p.returncode}"))
    un("L15", rien, lambda m, p: (p.returncode == 2 and not m.gh_etat()["vus"] and "(N-3)" in p.stdout,
                                  f"L15 « aucune » alors que le code change → 2, aucune demande (N-3) : code {p.returncode}"))
    un("L16", rien, lambda m, p: (p.returncode == 2 and not m.gh_etat()["vus"],
                                  f"L16 « aucune autre que `X` » → 2, aucune demande (N-3) : code {p.returncode}"))
    un("L17", rien, lambda m, p: (p.returncode == 2 and not m.gh_etat()["vus"],
                                  f"L17 « aucune autre que `X` » sans code changé → 2, X n'est pas perdu (N-3) : "
                                  f"code {p.returncode}"))
    un("L18", lambda m: m.env.update(FAUX_FAB_MUET="1"),
       lambda m, p: (p.returncode == 3 and not m.gh_etat()["vus"] and "(N-4)" in p.stdout,
                     f"L18 fabricant muet : publication non prouvée → 3, aucune demande (N-4) : code {p.returncode}"
                     + ("" if "(N-4)" in p.stdout else " · " + p.stdout[-400:])))
    un("L14", lambda m: m.env.update(FAUX_FAB_REFUSE="1"),
       lambda m, p: (p.returncode == 3 and not m.gh_etat()["vus"],
                     f"L14 publication refusée → 3, aucune demande (et R0 : clone public effacé) : code {p.returncode}"))
    return r


def cas_installer(progs, source):
    """Les cas d'INSTALLER ; rend la liste des (nom, vrai si passé, détail).

    ① RÔLE — Éprouver INSTALLER.py. ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `progs` · `source`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — I1 nominal (main fusionnée, public NON touché, message « public en retard ») ; I2 passage en
      cours → 3 ; I2b passage « queued » → 3 (M2) ; I3 « DÉPLOYABLE APRÈS CORRECTIONS » → 1 ; I4 RELU commité par un
      autre que Cowork → 1 ; I5 code changé après la pointe relue → 1 ; I6 aucune preuve GitHub → 1 (M1) ; I7 preuve
      rouge → 1 (M6) ; I8 pointe relue hors de l'histoire → 1 (M5) ; I9 preuve d'une pointe au code différent → 1 ;
      I9b preuve de la pointe jouée par LIVRER, relue une note plus loin → 0 ; I10 plantage après la fusion → 5 ;
      I11 un programme rangé en archives/ après le RELU → 1 (D-2) ; I12 auteur « Claude (pas cowork) » → 1 (D-5) ;
      I13 branche déjà dans main → 1, rien poussé ; I14 note « aucune » et code changé → 1 (N-3) ; I15 note « aucune »
      sur un travail sans code changé → 0 ; I16 plantage de l'écriture du registre entre la fusion et le commit → 5,
      main intacte, worktree de main propre et sans MERGE_HEAD (N-5).
    ⑦ UNITÉ — — ⑧ POURQUOI — Consigne du 20-11-2026, A-818 et réparation du soir (points A et D).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Mondes jetables.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = []
    vivant = {"databaseId": 7, "repo": "faux/prive", "workflowName": "Collecte ABC Bourse", "headBranch": "main",
              "headSha": "0", "event": "schedule", "status": "in_progress", "conclusion": "",
              "createdAt": "2026-11-20T09:00:00Z", "ticks": -10 ** 9}

    def preuves(m, sortie_gf=0, pointe=None):
        """Les deux preuves de la note du monde. ① RÔLE — Raccourci. ② CONTEXTE D'APPEL — Les cas I.
        ③ ENTRÉE — `m` · `sortie_gf` : le code de GardeFou · `pointe` : la pointe jouée (défaut : travail-x).
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — `preuve` deux fois. ⑦ UNITÉ — —
        ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        jouee = pointe or pointe_de(m)
        preuve(m, "CircuitPublic", jouee)
        preuve(m, "GardeFou", jouee, sortie=sortie_gf)

    def hors_histoire(m):
        """Un commit de même arbre que travail-x, hors de son histoire, joué et relu. ① RÔLE — Régler I8.
        ② CONTEXTE D'APPEL — I8. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien]
        ⑥ TRAITEMENT — « git commit-tree » de l'arbre de travail-x sur le parent main, poussé sous
        refs/heads/ailleurs ; preuves sur lui ; m.relue le retient. ⑦ UNITÉ — — ⑧ POURQUOI — Sabotage M5 : sans la
        garde d'ascendance, le même code passerait. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        x = m.git(m.prive, "commit-tree", "travail-x^{tree}", "-p", "main", "-m", "ailleurs").strip()
        m.git(m.prive, "update-ref", "refs/heads/ailleurs", x)
        preuves(m, pointe=x)
        m.relue = x

    def changer_le_code(m):
        """Preuves sur la pointe d'avant, puis un changement de code poussé sur travail-x. ① RÔLE — Régler I9.
        ② CONTEXTE D'APPEL — I9. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien]
        ⑥ TRAITEMENT — preuves, clone, CODE.py changé, poussée. ⑦ UNITÉ — — ⑧ POURQUOI — Une preuve d'un AUTRE code
        ne vaut pas. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        preuves(m)
        w = os.path.join(m.t, "w9")
        m.git(None, "clone", "-q", "-b", "travail-x", m.prive, w)
        with open(os.path.join(w, "programmes", "CODE.py"), "w") as f:
            f.write("V = 3\n")
        m.git(w, "commit", "-q", "-am", "code changé")
        m.git(w, "push", "-q", "origin", "travail-x")

    def passage_vivant(etat):
        """Rend le réglage « preuves et un passage vivant ». ① RÔLE — Régler I2, I2b. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — `etat`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la fonction. [rend: 1]
        ⑥ TRAITEMENT — —. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        def regler(m):
            """Preuves, puis scénario. ① RÔLE — Réglage. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — `m`.
            ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — —. ⑦ UNITÉ — — ⑧ POURQUOI — —
            ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse, écrit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            preuves(m)
            m.scenario(runs=[dict(vivant, status=etat)])
        return regler

    def preuves_et_plantage(m):
        """Preuves, et plantage au premier affichage après la fusion. ① RÔLE — Régler I10. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — —. ⑦ UNITÉ — —
        ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse, écrit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        preuves(m)
        planter(m, "ÉTAPE 4 — main")

    def preuves_et_registre_bloque(m):
        """Preuves, et le dossier du registre rendu impossible à créer dans le clone du Chat. ① RÔLE — Régler I16 :
        `noter` lève entre la fusion et le commit (N-5). ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — `m`.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — un FICHIER au chemin du dossier du
        registre, exclu par .git/info/exclude (le clone reste propre aux yeux de « git status »). ⑦ UNITÉ — —
        ⑧ POURQUOI — Un plantage réel du système de fichiers, sans crochet dans le code éprouvé. ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit dans le clone. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        preuves(m)
        os.makedirs(os.path.join(m.clone, "etudes"), exist_ok=True)
        with open(os.path.join(m.clone, "etudes", "REGISTRE_DES_TRAVAUX"), "w") as f:
            f.write("un fichier, pas un dossier\n")
        with open(os.path.join(m.clone, ".git", "info", "exclude"), "a") as f:
            f.write("etudes/REGISTRE_DES_TRAVAUX\n")

    cas = (
        # nom, code attendu, réglage (avant le RELU), arguments du RELU
        ("I1", 0, preuves, {}),
        ("I2", 3, passage_vivant("in_progress"), {}),
        ("I2b", 3, passage_vivant("queued"), {}),
        ("I3", 1, preuves, {"verdict": "DÉPLOYABLE APRÈS CORRECTIONS"}),
        ("I4", 1, preuves, {"auteur": "Claude"}),
        ("I5", 1, preuves, {"apres": "programmes/CODE.py"}),
        ("I6", 1, lambda m: None, {}),
        ("I7", 1, lambda m: preuves(m, sortie_gf=1), {}),
        ("I8", 1, hors_histoire, {}),
        ("I9", 1, changer_le_code, {}),
        ("I9b", 0, preuves, {"avant_relu": "echanges/A_RELIRE.md"}),
        ("I10", 5, preuves_et_plantage, {}),
        ("I11", 1, preuves, {"ranger": "programmes/CODE.py"}),
        ("I12", 1, preuves, {"auteur": "Claude (pas cowork)"}),
        ("I13", 1, preuves, {}),
        ("I14", 1, lambda m: None, {}),
        ("I15", 0, lambda m: None, {}),
        ("I16", 5, preuves_et_registre_bloque, {}),
    )
    mondes = {"I14": {"liste": "- aucune"}, "I15": {"liste": "- aucune", "code_change": False}}
    for nom, attendu, regler, kw in cas:
        if not choisi(nom):
            continue
        m = Monde(source, progs, **mondes.get(nom, {}))
        try:
            m.relue = None
            regler(m)
            avant = m.git(m.prive, "rev-parse", "main").strip()
            public_avant = m.git(m.public, "rev-parse", "main").strip()
            relu(m, **dict(kw, pointe=m.relue) if m.relue else kw)
            if nom == "I13":    # la branche est déjà dans main : relancer INSTALLER ne doit rien pousser
                w = os.path.join(m.t, "w13")
                m.git(None, "clone", "-q", "-b", "main", m.prive, w)
                m.git(w, "merge", "-q", "--no-ff", "-m", "déjà installée", "origin/travail-x")
                m.git(w, "push", "-q", "origin", "main")
                m.git(m.clone, "pull", "-q", "--ff-only")   # le clone du Chat suit main : seul le garde « déjà dans main » refuse
                avant = m.git(m.prive, "rev-parse", "main").strip()
            p = m.programme("INSTALLER.py", "travail-x")
            apres = m.git(m.prive, "rev-parse", "main").strip()
            public_apres = m.git(m.public, "rev-parse", "main").strip()
            fusion = m.git(m.prive, "log", "--format=%H", "--grep=^Installation de", "main").split()
            installe = [e for e in m.entrees("main") if e["etape"] == "installation"]
            if attendu == 0:
                ok = (p.returncode == 0 and apres != avant and len(fusion) == 1 and len(installe) == 1
                      and public_apres == public_avant and "public en retard, REPUBLIER s'en charge" in p.stdout)
            elif attendu == 5 and nom == "I16":   # N-5 : rien poussé, et le worktree de main n'est pas en fusion
                ok = (p.returncode == 5 and apres == avant and not m.git(m.clone, "status", "--porcelain").strip()
                      and m.lancer(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"], m.clone).returncode != 0)
            elif attendu == 5:
                ok = p.returncode == 5 and apres != avant and len(fusion) == 1
            else:
                ok = p.returncode == attendu and apres == avant
            r.append((nom, ok, f"{nom} attendu {attendu} : code {p.returncode} · main {'bougée' if apres != avant else 'intacte'}"
                               f" · public {'touché' if public_apres != public_avant else 'intact'}"
                               + ("" if ok else " · " + p.stdout[-300:])))
        finally:
            m.fermer()
    return r


def cas_republier(progs, source):
    """Les cas de REPUBLIER ; rend la liste des (nom, vrai si passé, détail).

    ① RÔLE — Éprouver REPUBLIER.py. ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `progs` · `source`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — R1 public différent de main → publié (le public porte main) ; R2 relancé sur un public égal → rien
      (aucun --publier, pointe publique inchangée) ; R3 --verifier : égal → 0, clone intact ; R4 --verifier après un
      commit de code sur main → 1, la commande nommée ; R6 --verifier avec un fabricant muet → 2 (N-4) ; R7 --verifier,
      fichier écrit par la fabrication mais ignoré par le .gitignore du public → 1 (N-4) ; R8 dans le circuit du soir
      fabriqué, `public_a_jour` garde « continue-on-error », un pas après le journal du premier job rougit sur son
      échec, et la collecte garde « !cancelled() » (N-7, N-11).
    ⑦ UNITÉ — — ⑧ POURQUOI — Consigne du 20-11-2026 au soir, point B.
    ⑨ CE QUI CLOCHE — Le faux fabricant ne fabrique que version.txt et code.txt. ⑩ EFFET — Monde jetable.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = []
    if not choisi("R"):
        return r
    m = Monde(source, progs)
    try:
        log = os.path.join(m.t, "fab.log")
        p1 = m.programme("REPUBLIER.py")
        version = m.montrer("main", "version.txt", m.public).strip()
        r.append(("R1", p1.returncode == 0 and version == pointe_de(m, "main"),
                  f"R1 public en retard → republié : code {p1.returncode}, le public porte main : "
                  f"{version == pointe_de(m, 'main')}"
                  + ("" if p1.returncode == 0 else " · " + p1.stdout[-300:])))
        avant = m.git(m.public, "rev-parse", "main").strip()
        with open(log) as f:
            n = len(f.read().splitlines())
        p2 = m.programme("REPUBLIER.py")
        with open(log) as f:
            publies = [l for l in f.read().splitlines()[n:] if "--publier" in l]
        apres = m.git(m.public, "rev-parse", "main").strip()
        r.append(("R2", p2.returncode == 0 and not publies and apres == avant and "ÉGAL" in p2.stdout,
                  f"R2 public déjà égal → rien : code {p2.returncode}, --publier lancés {len(publies)}, pointe "
                  f"{'inchangée' if apres == avant else 'BOUGÉE'}"))
        pub, priv = os.path.join(m.t, "pubv"), os.path.join(m.t, "privv")
        m.git(None, "clone", "-q", "-b", "main", m.public, pub)
        m.git(None, "clone", "-q", "-b", "main", m.prive, priv)
        p3 = m.lancer([sys.executable, "-B", os.path.join(progs, "REPUBLIER.py"), "--verifier", priv, pub], m.t)
        r.append(("R3", p3.returncode == 0 and not m.git(pub, "status", "--porcelain").strip(),
                  f"R3 --verifier sur un public égal → 0, clone intact : code {p3.returncode}"
                  + ("" if p3.returncode == 0 else " · " + p3.stdout[-300:])))
        with open(os.path.join(priv, "programmes", "CODE.py"), "w") as f:
            f.write("V = 9\n")
        m.git(priv, "commit", "-q", "-am", "code de main changé")
        p4 = m.lancer([sys.executable, "-B", os.path.join(progs, "REPUBLIER.py"), "--verifier", priv, pub], m.t)
        r.append(("R4", p4.returncode == 1 and "programmes/REPUBLIER.py" in p4.stdout,
                  f"R4 --verifier sur un public en retard → 1, commande nommée : code {p4.returncode}"))
        if choisi("R6"):
            env_muet = dict(m.env, FAUX_FAB_MUET="1")
            p6 = subprocess.run([sys.executable, "-B", os.path.join(progs, "REPUBLIER.py"), "--verifier", priv, pub],
                                cwd=m.t, capture_output=True, text=True, timeout=300, env=env_muet)
            r.append(("R6", p6.returncode == 2,
                      f"R6 --verifier avec un fabricant muet → 2, jamais « égal » (N-4) : code {p6.returncode}"))
        if choisi("R7"):
            m.git(priv, "reset", "-q", "--hard", "HEAD~1")    # le privé redevient égal au public
            with open(os.path.join(pub, ".gitignore"), "w") as f:
                f.write("ignore.txt\n")
            m.git(pub, "add", ".gitignore")
            m.git(pub, "commit", "-q", "-m", "ignore")
            env_ign = dict(m.env, FAUX_FAB_IGNORE="1")
            p7 = subprocess.run([sys.executable, "-B", os.path.join(progs, "REPUBLIER.py"), "--verifier", priv, pub],
                                cwd=m.t, capture_output=True, text=True, timeout=300, env=env_ign)
            r.append(("R7", p7.returncode == 1 and "ignore.txt" in p7.stdout,
                      f"R7 --verifier, fichier écrit mais ignoré par le public → 1 (N-4) : code {p7.returncode}"))
        spec = importlib.util.spec_from_file_location("FAB_R5", os.path.join(progs, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"))
        F = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(F)
        poser = F.CLONAGES[F.CLONAGES.index("Poser les programmes publics"):F.CLONAGES.index("Le garde du code")]
        r.append(("R5", F.COMMANDE_DE_REPUBLICATION in poser and "REPUBLIER.py --verifier" in F.PUBLIC_A_JOUR,
                  "R5 le circuit du soir nomme la commande au pas « Poser » et vérifie le public (D-3)"))
        if choisi("R8"):
            with open(os.path.join(source, F.CIRCUIT_PRIVE), encoding="utf-8") as f:
                soir = F.fabriquer_le_circuit(f.read())
            premier = soir[soir.index("  faut_il_tourner:\n"):soir.index("\n  collecte:\n")]
            collecte = soir[soir.index("\n  collecte:\n"):]
            pas = premier.split("      - ")
            rougir = [x for x in pas if re.search(r"if: \$\{\{ always\(\) && .*steps\.public_a_jour\.outcome == 'failure'", x)]
            verifs = {
                "N-11 public_a_jour en continue-on-error": "id: public_a_jour\n        continue-on-error: true\n" in premier,
                "N-7 un pas rougit sur l'échec de public_a_jour": len(rougir) == 1 and "exit 1" in rougir[0],
                "N-7 ce pas vient après le journal": bool(rougir) and premier.index(rougir[0]) > premier.index("id: journal"),
                "N-7 la collecte tourne malgré un premier job rouge":
                    "!cancelled()" in collecte[:collecte.index("runs-on:")],
            }
            rates = [k for k, v in verifs.items() if not v]
            r.append(("R8", not rates, "R8 le retard du public rougit le passage sans arrêter la collecte (N-7, N-11) : "
                                       + ("ok" if not rates else "RATÉ " + " ; ".join(rates))))
    finally:
        m.fermer()
    return r


def cas_qui_fait_quoi(progs, source):
    """Les cas de QUI_FAIT_QUOI ; rend la liste des (nom, vrai si passé, détail).

    ① RÔLE — Éprouver QUI_FAIT_QUOI.py. ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `progs` · `source`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — Q1 la même épreuve chez GitHub et chez Cowork → DOUBLON, code 1 ; Q2 registre cohérent → 0 ;
      Q3 registre « en cours » pour un passage fini → INCOHÉRENT ; Q4 Cowork lancé avant la fin de GitHub ;
      Q5 « noter » écrit et pousse une entrée lue ensuite ; Q6 une entrée d'exécutant hors contrat (« Cowork ») →
      ILLISIBLE, code 2 (D-6). Le registre est écrit en fichiers JSON, un par entrée.
    ⑦ UNITÉ — — ⑧ POURQUOI — Ajout du 20-11-2026 à 19h40, point 3 : le cas « doublon non vu ».
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Mondes jetables.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = []
    passage = {"databaseId": 9100, "repo": "faux/public", "workflowName": "epreuves_longues.yml",
               "headBranch": "travail-x", "headSha": "0", "event": "workflow_dispatch", "status": "completed",
               "conclusion": "success", "createdAt": "2026-11-20T09:00:00Z", "ticks": 0, "codes": []}
    cles = ("etape", "branche", "executant", "identifiant", "lance_le", "fini_le", "resultat")
    gh_fini = ("epreuve:CircuitPublic", "travail-x", "github", "9100", "2026-11-20 10:00:00", "2026-11-20 10:30:00",
               "code 0")
    for nom, lignes, attendu, mot in (
            ("Q1", [gh_fini, ("epreuve:CircuitPublic", "travail-x", "cowork", "abc123", "2026-11-20 10:05:00", "",
                              "EN COURS")], 1, "DOUBLON"),
            ("Q2", [gh_fini], 0, "== DOUBLON (0)"),
            ("Q3", [("epreuve:CircuitPublic", "travail-x", "github", "9100", "2026-11-20 10:00:00", "", "EN COURS")],
             1, "INCOHÉRENT"),
            ("Q4", [gh_fini, ("relecture", "travail-x", "cowork", "abc123", "2026-11-20 10:10:00", "", "EN COURS")],
             1, "COWORK AVANT GITHUB"),
            ("Q6", [gh_fini, ("relecture", "travail-x", "Cowork", "abc123", "2026-11-20 10:10:00", "", "EN COURS")],
             2, "exécutant 'Cowork'")):
        if not choisi(nom):
            continue
        m = Monde(source, progs)
        try:
            m.scenario(runs=[passage])
            w = os.path.join(m.t, "w")
            m.git(None, "clone", "-q", "-b", "travail-x", m.prive, w)
            os.makedirs(os.path.join(w, "etudes", "REGISTRE_DES_TRAVAUX"))
            for i, l in enumerate(lignes):
                nom_f = f"2026-11-20_10h00m0{i}_{i:012x}.json"
                with open(os.path.join(w, "etudes", "REGISTRE_DES_TRAVAUX", nom_f), "w") as f:
                    json.dump(dict(zip(cles, l)), f)
            m.git(w, "add", "-A")
            m.git(w, "commit", "-q", "-m", "registre")
            m.git(w, "push", "-q", "origin", "travail-x")
            p = m.programme("QUI_FAIT_QUOI.py")
            ok = p.returncode == attendu and mot in p.stdout
            r.append((nom, ok, f"{nom} attendu {attendu} « {mot} » : code {p.returncode}"
                               + ("" if ok else " · " + p.stdout[-300:])))
        finally:
            m.fermer()
    if not choisi("Q5"):
        return r
    m = Monde(source, progs)
    try:
        p = m.programme("QUI_FAIT_QUOI.py", "noter", "epreuve:GardeFou", "travail-x", "cowork", "abc123")
        ok = p.returncode == 0 and any(e["etape"] == "epreuve:GardeFou" and e["identifiant"] == "abc123"
                                       for e in m.entrees("travail-x"))
        r.append(("Q5", ok, f"Q5 noter écrit et pousse : code {p.returncode}"))
    finally:
        m.fermer()
    return r


def cas_des_fiches(progs, source):
    """Les cas qui confrontent une fiche au code ; rend la liste des (nom, vrai si passé, détail).

    ① RÔLE — Q7 (N-6 du RELU de Cowork sur 0f18a8d2a) : la fiche de `LIVRER.pousser` nomme, avant « PAS », exactement
      les programmes qui l'appellent. ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `progs` : le dossier des programmes · `source`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — L'élément ② de la fiche de `pousser`, coupé au premier « PAS » ; pour chaque programme de
      PROGRAMMES : appelant si son texte porte « pousser( » hors de « def pousser( » ; nommé si son nom sans « .py »
      (pour LIVRER : « `main` ») est dans le texte coupé. Appelant et nommé doivent coïncider.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une fiche qui promet plus que le code trompe le relecteur (N-6).
    ⑨ CE QUI CLOCHE — Lecture de texte : une fiche reformulée sans « PAS » nomme tout le reste de l'élément.
    ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not choisi("Q7"):
        return []
    livrer = open(os.path.join(progs, "LIVRER.py"), encoding="utf-8").read()
    fiche = livrer[livrer.index("def pousser("):]
    deux = fiche[fiche.index("② CONTEXTE D'APPEL"):fiche.index("③ ENTRÉE")]
    nommes_texte = deux.split("PAS")[0]
    ecarts = []
    for prog in PROGRAMMES:
        texte = open(os.path.join(progs, prog), encoding="utf-8").read().replace("def pousser(", "")
        appelle = "pousser(" in texte
        nom = "`main`" if prog == "LIVRER.py" else prog[:-3]
        if appelle != (nom in nommes_texte):
            ecarts.append(f"{prog} {'appelle' if appelle else 'n appelle pas'} mais la fiche "
                          f"{'ne le nomme pas' if appelle else 'le nomme'}")
    return [("Q7", not ecarts, "Q7 la fiche de pousser nomme ses vrais appelants (N-6) : "
             + ("ok" if not ecarts else " ; ".join(ecarts)))]


SABOTAGES = (
    ("S1 publication sautée", "LIVRER.py",
     "public, pub = publier_au_public(wt, branche)",
     "public, pub = cloner_le_public(branche), {'avant': '', 'apres': '', 'message': 'sauté'}"),
    ("S2 branche détachée pour publier", "LIVRER.py",
     "wt, jetable = worktree_nomme(racine, branche)",
     "wt, jetable = worktree_jetable(racine, f'origin/{branche}'), True"),
    ("S3 Cowork avant GitHub (verdict sans attendre le passage)", "LIVRER.py",
     "conclusion = suivre_le_passage(passage, plafond * 60, pas)\n"
     "            verdict, lignes = lire_les_resultats(racine, branche, passage, codes, pointe)",
     "conclusion, verdict, lignes = '?', 0, [(c, 0, '?', pointe) for c in codes]"),
    ("S4 pas d'attente de la file", "LIVRER.py",
     "        occ = passages_occupes(circuits)\n        if not occ:",
     "        occ = []\n        if not occ:"),
    ("S5 pas de redépôt après un refus « en cours »", "LIVRER.py",
     '        if "en cours ou en attente" in journal.stdout:', '        if False:'),
    ("S6 nom sans code ignoré", "LIVRER.py", "        if sans:\n            raise Arret(NOMS",
     "        if False:\n            raise Arret(NOMS"),
    ("S7 note non vérifiée", "LIVRER.py",
     'dire(f"ÉTAPE 1 — note de {branche} : " + verifier_la_note(racine, branche))', 'dire("ÉTAPE 1 sautée")'),
    ("S8 -B écrase un commit local", "LIVRER.py", "        if en_avance:\n", "        if False:\n"),
    ("S9 plafond ignoré", "LIVRER.py",
     "        if time.monotonic() >= fin:\n            raise Arret(TOMBE, f\"plafond atteint : {len(occ)}",
     "        if False:\n            raise Arret(TOMBE, f\"plafond atteint : {len(occ)}"),
    ("S10 installation pendant un passage (A-818)", "INSTALLER.py", "            if occupes:\n", "            if False:\n"),
    ("S12 verdict lu au début seulement", "INSTALLER.py", 'if valeur != "DÉPLOYABLE":',
     'if not valeur.startswith("DÉPLOYABLE"):'),
    ("S13 auteur du RELU non vérifié", "INSTALLER.py", 'if auteur.lower() != "cowork":', 'if False:'),
    ("D2 renommage suivi : programme rangé en archives/ accepté", "INSTALLER.py", '"diff", "--no-renames", "--name-only"',
     '"diff", "--name-only"'),
    ("D5 auteur lu comme sous-chaîne", "INSTALLER.py", 'if auteur.lower() != "cowork":',
     'if "cowork" not in auteur.lower():'),
    ("D13 branche déjà dans main réinstallée", "INSTALLER.py", '"--is-ancestor", ref, "origin/main").returncode == 0:',
     '"--is-ancestor", ref, "origin/main").returncode == 99:'),
    ("D6 lecteur du registre sans contrôle de l exécutant", "LIVRER.py",
     '        if d["executant"] not in c.EXECUTANTS_DES_TRAVAUX:\n', '        if False:\n'),
    ("S14 code changé après la relecture accepté", "INSTALLER.py", "    if hors:\n", "    if False:\n"),
    ("S15 doublon non vu", "QUI_FAIT_QUOI.py", "        if len(executants) > 1:", "        if False:"),
    ("S16 Cowork avant GitHub non vu", "QUI_FAIT_QUOI.py", "    incoherents += cowork_avant_github(retenus)", "    pass"),
    ("S17 registre cru sans GitHub", "QUI_FAIT_QUOI.py",
     '        if not fini and not vivant:\n', '        if False:\n'),
    ("S18 clone public laissé après un refus", "LIVRER.py",
     "    except BaseException:\n        shutil.rmtree(public, ignore_errors=True)\n        raise",
     "    except BaseException:\n        raise"),
    # Les six sabotages du relecteur neuf du 20-11-2026 (M1 à M6), puis ceux de la réparation du soir (P1 à P7).
    ("M1 épreuve absente comptée verte (LIVRER)", "LIVRER.py",
     '                lignes.append((c, "ABSENTE", "?", ""))\n                code = 2',
     '                lignes.append((c, 0, "?", ""))'),
    ("M1i épreuve sans preuve acceptée (INSTALLER)", "INSTALLER.py",
     "        if not retenus:\n            raise L.Arret(REFUS",
     "        if not retenus:\n            continue\n            raise L.Arret(REFUS"),
    ("M2 passage « queued » ignoré (LIVRER)", "LIVRER.py",
     '            if p.get("status") != "completed":\n                occupes.append',
     '            if p.get("status") == "in_progress":\n                occupes.append'),
    ("M2i passage « queued » ignoré (INSTALLER)", "INSTALLER.py",
     '            if p.get("status") != "completed":', '            if p.get("status") == "in_progress":'),
    ("M3 deux passages départagés en silence", "LIVRER.py",
     "                if len(vus) > 1:\n", "                if False:\n"),
    ("M4 filtre createdAt retiré", "LIVRER.py",
     '                       if q.get("createdAt", "") >= p.get("createdAt", "")]', '                       ]'),
    ("M5 pointe relue hors de l'histoire acceptée", "INSTALLER.py",
     '    if not relue or L.git(racine, "merge-base", "--is-ancestor", relue, ref).returncode != 0:',
     '    if not relue:'),
    ("M6 code non nul de RESULTAT.json ignoré", "INSTALLER.py",
     '        if res.get("code_de_sortie") != 0:', '        if False:'),
    ("P1 plantage lu comme refus (INSTALLER)", "INSTALLER.py",
     "un plantage n'est jamais lu comme un refus\n            code = PLANTAGE",
     "un plantage n'est jamais lu comme un refus\n            code = REFUS"),
    ("P2 plantage lu comme étape tombée (LIVRER)", "LIVRER.py",
     "jamais lu comme un verdict ni comme un refus\n        code = PLANTAGE",
     "jamais lu comme un verdict ni comme un refus\n        code = TOMBE"),
    ("P3 poussée sans rebase sur un tiers", "LIVRER.py",
     '        if git(wt, "pull", "-q", "--rebase", "origin", branche).returncode != 0:', '        if True:'),
    ("P4 pointe jouée non vérifiée (LIVRER)", "LIVRER.py", "                if jouee != pointe:\n",
     "                if False:\n"),
    ("P5 même code sans regarder le code (INSTALLER)", "INSTALLER.py",
     "    return not changes_hors_permis(racine, jouee, relue)", "    return True"),
    ("P6 REPUBLIER publie un public déjà égal", "REPUBLIER.py", "        if not reste:\n", "        if False:\n"),
    ("P7 REPUBLIER --verifier toujours égal", "REPUBLIER.py", "    if reste:\n        n = len",
     "    if False:\n        n = len"),
    # Les réparations des défauts N-3 à N-6 du RELU de Cowork sur 0f18a8d2a (21-11-2026) ; N-1 : D13 ci-dessus.
    ("N3a « aucune » cru sans regarder le code (LIVRER)", "LIVRER.py",
     "        change = code_change_par(wt, pointe) if not codes else []", "        change = []"),
    ("N3b « aucune » cru sans regarder le code (INSTALLER)", "INSTALLER.py",
     '    change = L.code_change_par(racine, relue) if etat == "aucune" else []', "    change = []"),
    ("N3c « aucune autre que `X` » lu comme « aucune »", "LIVRER.py",
     "            if nomme:   # « aucune", "            if False:   # « aucune"),
    ("N4a fabricant muet cru égal (REPUBLIER)", "REPUBLIER.py",
     "        if r.returncode == 0 and not reecrits:", "        if False:"),
    ("N4b fichier ignoré écrit non vu", "LIVRER.py",
     '    reste = "\\n".join([x for x in [reste] if x] + ["!! " + x for x in ecrits_ignores])', "    reste = reste"),
    ("N4c clone de contrôle muet accepté (LIVRER)", "LIVRER.py",
     "        if refait.returncode == 0 and not reecrits:", "        if False:"),
    ("N5 fusion inachevée laissée au worktree de main", "INSTALLER.py",
     'en fusion inachevée\n        L.git(wt, "merge", "--abort")\n        raise', "en fusion inachevée\n        raise"),
    ("N6 fiche de pousser qui promet INSTALLER", "LIVRER.py",
     "② CONTEXTE D'APPEL — `main` (bloc finally) et QUI_FAIT_QUOI « noter ». PAS INSTALLER",
     "② CONTEXTE D'APPEL — `main` (bloc finally), INSTALLER (commit de fusion), QUI_FAIT_QUOI « noter ». PAS INSTALLER"),
    # N-7 et N-11 du RELU de Cowork sur 2b62e3f2e (21-11-2026)
    ("N7 retard du public lu par personne", "FABRIQUER_LE_CIRCUIT_PUBLIC.py",
     "             + ROUGIR_SI_LE_PUBLIC_EST_EN_RETARD\n", ""),
    ("N11 continue-on-error retiré de public_a_jour", "FABRIQUER_LE_CIRCUIT_PUBLIC.py",
     "        id: public_a_jour\n        continue-on-error: true\n", "        id: public_a_jour\n"),
)


def jouer(progs, source):
    """Joue tous les cas ; rend la liste des (nom, vrai, détail).

    ① RÔLE — Un passage complet. ② CONTEXTE D'APPEL — `main`, et une fois par sabotage.
    ③ ENTRÉE — `progs` · `source`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — Les trois familles de cas, puis R0 : aucun dossier /tmp/livrer_* nouveau (ceux trouvés sont
      effacés après le compte). ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Mondes jetables. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    avant = laisses()
    r = (cas_livrer(progs, source) + cas_installer(progs, source) + cas_republier(progs, source)
         + cas_qui_fait_quoi(progs, source) + cas_des_fiches(progs, source))
    restes = sorted(laisses() - avant)
    r.append(("R0", not restes, f"R0 aucun dossier laissé sous /tmp/livrer_ : {len(restes)} laissé(s) {' '.join(restes[:3])}"))
    for d in restes:
        if d.startswith("/tmp/livrer_"):
            shutil.rmtree(d, ignore_errors=True)
    return r


def laisses():
    """Rend l'ensemble des dossiers /tmp/livrer_* présents.

    ① RÔLE — Voir ce que les programmes laissent derrière eux. ② CONTEXTE D'APPEL — `jouer`, avant et après.
    ③ ENTRÉE — —  ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins.
      [rend: 1]
    ⑥ TRAITEMENT — os.listdir de /tmp. ⑦ UNITÉ — — ⑧ POURQUOI — 18 clones publics laissés, mesurés le 20-11-2026.
    ⑨ CE QUI CLOCHE — Un autre LIVRER lancé en même temps sur la machine fausserait le compte. ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return {os.path.join("/tmp", d) for d in os.listdir("/tmp") if d.startswith("livrer_")}


def copier_les_programmes(source, dossier, sabotage=None):
    """Copie les programmes éprouvés dans un dossier, avec au plus un sabotage ; lève ValueError si le motif manque.

    ① RÔLE — Éprouver une copie, jamais le dépôt. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `source` · `dossier` · `sabotage` : (nom, fichier, avant, après) ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Copie de PROGRAMMES ; le motif « avant » doit exister UNE fois, remplacé par « après ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage dont le motif manque ne mordrait sur rien : il est refusé.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit des fichiers. ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    os.makedirs(dossier, exist_ok=True)
    for p in PROGRAMMES:
        shutil.copyfile(os.path.join(source, "programmes", p), os.path.join(dossier, p))
    if sabotage:
        _, fichier, avant, apres = sabotage
        chemin = os.path.join(dossier, fichier)
        texte = open(chemin, encoding="utf-8").read()
        if texte.count(avant) != 1:
            raise ValueError(f"motif du sabotage {sabotage[0]} trouvé {texte.count(avant)} fois")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte.replace(avant, apres))


def main():
    """Lance les épreuves, et les sabotages avec --saboter ; sort avec le code.

    ① RÔLE — Voir l'en-tête. ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv : la racine, « --saboter[=noms] », « --cas=noms » (essai restreint à ces cas).
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — Rien : sort (0 ou 1).
      [rend: rien]
    ⑥ TRAITEMENT — `jouer` sur une copie propre ; avec --saboter, `jouer` sur chaque copie sabotée : au moins un
      cas doit tomber. ⑦ UNITÉ — Secondes. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Dossiers temporaires. ⑪ TERMINAISON — Sort du programme par sys.exit.
      [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    source = os.path.abspath(args[0] if args else ".")
    for a in sys.argv[1:]:
        if a.startswith("--cas="):
            CHOISIS.update(x for x in a.split("=", 1)[1].split(",") if x)
    t0, ok = time.time(), True
    base = tempfile.mkdtemp(prefix="epreuve_livrer_progs_")
    try:
        copier_les_programmes(source, os.path.join(base, "propre"))
        for nom, passe, detail in jouer(os.path.join(base, "propre"), source):
            print(("✅ " if passe else "❌ ") + detail, flush=True)
            ok = ok and passe
        if any(a == "--saboter" or a.startswith("--saboter=") for a in sys.argv):
            choisis = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")), None)
            for s in SABOTAGES:
                if choisis and s[0].split()[0] not in choisis:
                    continue
                d = os.path.join(base, re.sub(r"\W", "_", s[0])[:20])
                try:
                    copier_les_programmes(source, d, s)
                except ValueError as e:
                    print(f"❌ {s[0]} : {e}", flush=True)
                    ok = False
                    continue
                tombes = [n for n, passe, _ in jouer(d, source) if not passe]
                print((f"✅ {s[0]} → {' '.join(tombes)} tombe(nt)" if tombes else f"❌ {s[0]} NE MORD PAS"), flush=True)
                ok = ok and bool(tombes)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(f"{'TOUT PASSE' if ok else 'ÉCHEC'} en {time.time() - t0:.0f} s")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
