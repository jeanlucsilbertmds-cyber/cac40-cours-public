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
Le contrôle réel n'est PAS joué ici (il lirait tout donnees/) : un contrôle de remplacement, posé dans chaque copie
fabriquée, vérifie ce que le vrai exige (git, HEAD, origin/main, options) et écrit sa ligne de contrôle au format que
lit la fonction du vrai contrôle (`_marqueur_de_queue`, chargée depuis la racine éprouvée).

① RÔLE — Jouer les cas C1 à C12 ; avec « --saboter », jouer aussi les sabotages S1 à S11 : chacun doit faire rougir
  au moins un cas, sinon l'épreuve est une décoration (R-731).
② CONTEXTE D'APPEL — À la main ; la certification de nuit (toute épreuve de tests/, avec la racine, puis
  « --saboter »).
③ ENTRÉE — `<racine>` (le dépôt éprouvé), `--saboter` facultatif.
④ CONDITIONS D'ENTRÉE — git est installé ; la racine porte les programmes nommés dans PIECES.
⑤ SORTIE — Le code de sortie : 0 tout est juste ; 1 un cas faux ou un sabotage qui ne mord pas ; 2 l'épreuve n'a
  pas pu tourner (pièce absente, motif de sabotage introuvable : R-734).
  [rend: 1]
⑥ TRAITEMENT — `fabriquer` : une origine git à deux commits, son clone (refs/remotes/origin/main, HEAD détachée sur le
  second commit : « le clone du circuit »), une copie sans .git avec les pièces et le contrôle de remplacement ;
  `cas` : chaque cas sur une copie neuve ; `saboter` : chaque sabotage remplace un texte UNIQUE d'une pièce de la
  copie, puis rejoue les cas.
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
# historique lisible, options de l'usage local) ; refuse une note qui porte REFUSER ; rend 0 SANS ligne pour SANSLIGNE.
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
              ["log", "--all", "--oneline"], ["cat-file", "-e", "HEAD:LISEZ_MOI.txt"]):
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
)


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
    ⑥ TRAITEMENT — `lancer`, puis lecture du détail. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    code, _ = lancer([sys.executable, "-B", os.path.join(d["copie"], ENVELOPPE), d["copie"]],
                     env=env_de(racine, d, RESULTAT_DE_L_EPREUVE=detail, **plus))
    try:
        with open(detail, encoding="utf-8") as f:
            return code, json.load(f)
    except (OSError, ValueError):
        return code, {}


def cas(racine, pieces, base):
    """Joue les cas C1 à C12 sur des décors neufs ; rend la liste des cas faux.

    ① RÔLE — Les preuves de la fiche en tête. ② CONTEXTE D'APPEL — `main`, une fois, puis une fois par sabotage.
    ③ ENTRÉE — la racine, les pièces (textes), un dossier neuf. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des textes des cas faux (vide : tout est juste).
    [rend: 1]
    ⑥ TRAITEMENT — C1 vert · C2 refus du contrôle → ROUGE · C3 POINTE_JOUEE sur un autre commit → 2 · C4 copie avec
      un .git → 2 · C5 sans GITHUB_WORKSPACE → 2 · C6 clone sans origin/main → 2 · C7 contrôle à 0 sans ligne → 2 ·
      C8 « --matrice … Livraison » accepté, et refusé quand le code est retiré de la table · C9 le joueur de bout en
      bout : RESULTAT.json porte code 0, pointe jouée, verdict VERT, empreinte · C10 « --juger » : oui sur la bonne
      pointe, non sur une autre pointe, non sur une autre épreuve, non sur un verdict ROUGE · C11 un détail illisible
      → « detail_illisible » · C12 (superviseur R-759, point 3) le disque de la copie diffère de la pointe (la note
      du commit n'est pas celle de la copie) → 2.
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
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        faux.append(f"DÉCOR IMPOSSIBLE : {type(e).__name__} : {e}")
    return faux


def main():
    """La ligne de commande (fiche en tête).

    ① RÔLE — Jouer les cas, puis les sabotages. ② CONTEXTE D'APPEL — Fiche en tête, ②. ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④. ⑤ SORTIE — UNE valeur : le code de sortie (fiche en tête, ⑤).
    [rend: 1]
    ⑥ TRAITEMENT — lire les pièces de la racine ; les cas ; avec « --saboter », pour chaque sabotage, le texte doit
      se trouver une fois dans sa pièce (sinon 2), et les cas doivent rougir (sinon 1).
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
        print(f"cas C1-C12 : {'tous justes' if not faux else str(len(faux)) + ' faux'}")
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
            rouges = cas(racine, sabote, os.path.join(base, nom))
            print(f"  {nom} ({quoi}) : " + (f"MORD — {rouges[0][:110]}" if rouges else "NE MORD PAS"))
            if not rouges:
                muets.append(nom)
        print(f"sabotages : {len(SABOTAGES) - len(muets)} mordent sur {len(SABOTAGES)}"
              + (f" ; muets : {' '.join(muets)}" if muets else ""))
        return 1 if muets else 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
