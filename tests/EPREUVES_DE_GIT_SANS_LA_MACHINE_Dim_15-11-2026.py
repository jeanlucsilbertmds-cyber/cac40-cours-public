#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DE GIT_SANS_LA_MACHINE — l'outil qui isole les épreuves du réglage git de la machine (étape MIN, tour 2,
Dim 15-11-2026). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE — `tests/outils/GIT_SANS_LA_MACHINE.py` doit faire qu'un `git commit` lancé par une épreuve réussisse
QUELLE QUE SOIT la machine : un réglage git qui exige une signature impossible peut venir de QUATRE endroits — le
fichier global (`~/.gitconfig` ou `GIT_CONFIG_GLOBAL`), le fichier système (`/etc/gitconfig` ou `GIT_CONFIG_SYSTEM`),
les variables `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n`, et `GIT_CONFIG_PARAMETERS` (ce que pose
`git -c`). Les relectures de Cowork du 15-11-2026 (13h54 et 13h56, RELU 5/N-1 et 6/N-2) ont mesuré que l'outil ne
neutralisait que les deux premiers, et qu'AUCUNE épreuve ne le gardait sur une machine qui ne signe pas (le circuit
GitHub) : une régression de l'outil y passait sans bruit. Ces épreuves posent ELLES-MÊMES chaque réglage hostile —
un faux signataire qui note son appel dans un journal puis échoue — et ne dépendent donc pas de la machine.

USAGE : python3 -B tests/EPREUVES_DE_GIT_SANS_LA_MACHINE_Dim_15-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 est vert et que chaque sabotage joué rougit EXACTEMENT les cas qu'il vise ; 1 sinon ; 2 si un
étalonnage ne rougit pas (l'épreuve ne prouverait rien), si une cible de sabotage n'est pas présente une fois, si un
nom est inconnu ou si une donnée manque (R-734).

① RÔLE — Prouver que l'outil neutralise les quatre sources de réglage git de la machine, garde une identité
  d'épreuve, et que chacune de ces gardes a des dents (R-731).
② CONTEXTE D'APPEL — À la main ; la certification (`programmes/CERTIFIER_LA_VERSION.py`) lance chaque fichier de
  tests/ avec la racine, puis « --saboter ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : tests/outils/GIT_SANS_LA_MACHINE.py et programmes/CERTIFIER_LA_VERSION.py
  (l'outil lit sa liste de variables dans ce dernier) ; git et /bin/sh.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① étalonner : chaque réglage hostile, SANS l'outil, doit faire échouer un commit et appeler le faux
  signataire · ② pour Z0 puis chaque sabotage : copier l'outil et CERTIFIER dans un dossier temporaire, appliquer le
  sabotage, jouer les cas · ③ Z0 doit être vert ; un sabotage doit rougir exactement ses cas visés.
⑦ UNITÉ — Des codes de sortie de git ; des nombres d'appels au faux signataire ou au faux crochet.
⑧ POURQUOI — R-731 (une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration), R-734.
  Exiger l'ensemble EXACT des cas rougis, et non « au moins un », répond à C-3 (relecture du CARNET : « mord » sur
  n'importe quel échec) : un sabotage doit mordre pour SA raison.
⑨ CE QUI CLOCHE — ① `safe.directory` (RELU 5/N-5) n'est pas éprouvé : l'outil retire aussi ce réglage de la
  machine ; une épreuve rejouée sur un clone appartenant à un autre utilisateur verrait « dubious ownership ».
  THÉORIQUE, non mesuré ici. ② Les épreuves qui APPELLENT l'outil ne sont pas rejouées ici : on éprouve l'outil, pas
  ses appelants. ③ Le cas « un appelant recopie `os.environ` AVANT l'appel » (④ de l'outil) n'est pas éprouvé.
⑩ EFFET — Écrit et efface des dossiers temporaires (préfixe gsm_) ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque commit est borné à 60 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""
import os
import shutil
import subprocess
import sys
import tempfile

OUTIL = "tests/outils/GIT_SANS_LA_MACHINE.py"
CERTIF = "programmes/CERTIFIER_LA_VERSION.py"
FORMES = ("global", "systeme", "count", "parametres")      # les quatre sources d'un réglage git de la machine
EMAIL = "epreuve@epreuve.invalid"                           # l'identité que l'outil doit poser

# LES SABOTAGES : nom → ([(fichier, texte présent UNE fois, remplacement)], cas qui doivent rougir, et eux seuls).
SABOTAGES = {
    # l'outil tel que livré le 15-11-2026 13h24 (pointe 5dec47d8) : seulement GLOBAL et NOSYSTEM — le défaut 5/N-1
    "S1_ancien_outil": ([(OUTIL, "    os.environ.update(_variables_de_certifier())\n",
                          "    os.environ[\"GIT_CONFIG_NOSYSTEM\"] = \"1\"\n")],
                        {"H_count", "H_parametres", "H_tout"}),
    # la constante de CERTIFIER perd NOSYSTEM : le fichier système hostile est relu
    "S2_systeme_relu": ([(CERTIF, "\"GIT_CONFIG_NOSYSTEM\": \"1\",", "\"GIT_CONFIG_NOSYSTEM\": \"0\",")],
                        {"H_systeme", "H_tout"}),
    # la constante de CERTIFIER perd COUNT : les variables GIT_CONFIG_KEY_n hostiles sont relues
    "S3_count_relu": ([(CERTIF, "\"GIT_CONFIG_COUNT\": \"0\", ", "")], {"H_count", "H_tout"}),
    # la constante de CERTIFIER perd PARAMETERS : le « git -c » hostile est relu
    "S4_parametres_relus": ([(CERTIF, ", \"GIT_CONFIG_PARAMETERS\": \"\"}", "}")], {"H_parametres", "H_tout"}),
    # l'outil ne pose plus son réglage d'épreuve : GLOBAL reste /dev/null, plus AUCUNE identité — chaque commit
    # tombe (« Please tell me who you are »), et c'est l'identité, pas la signature, que chaque cas exige
    "S5_sans_identite": ([(OUTIL, "    os.environ[\"GIT_CONFIG_GLOBAL\"] = f\n", "    pass\n")],
                         {"H_global", "H_systeme", "H_count", "H_parametres", "H_tout", "I_identite"}),
    # NEUTRE, doit rester VERT : la même mise à jour écrite autrement (l'épreuve ne sur-détecte pas)
    "S6_neutre": ([(OUTIL, "    os.environ.update(_variables_de_certifier())\n",
                    "    for _k, _v in _variables_de_certifier().items():\n        os.environ[_k] = _v\n")], set()),
}

ENFANT = r'''
import importlib.util, os, subprocess, sys
outil, depot, avec = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
if avec:
    sp = importlib.util.spec_from_file_location("GIT_SANS_LA_MACHINE", outil)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); m.isoler_git_de_la_machine()
subprocess.run(["git", "init", "-q", depot], check=True)
r = subprocess.run(["git", "-C", depot, "commit", "-q", "--allow-empty", "-m", "jetable"], capture_output=True, text=True)
if r.returncode:
    print("COMMIT %d %s" % (r.returncode, r.stderr.strip().replace("\n", " | ")[:160])); sys.exit(0)
print("AUTEUR " + subprocess.run(["git", "-C", depot, "log", "-1", "--format=%ae"], capture_output=True,
                                 text=True).stdout.strip())
'''


def preparer(d):
    """Écrit le faux signataire et les réglages hostiles.
    ① RÔLE — fabriquer le décor hostile, identique sur toute machine. ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `d`, un dossier temporaire vide. ④ CONDITIONS D'ENTRÉE — /bin/sh existe. ⑤ SORTIE — UNE valeur : un
    dictionnaire {forme : variables d'environnement hostiles}, plus la clé « journal » (chemin). [rend: 1]
    ⑥ TRAITEMENT — écrire `faux_gpg.sh` (note son appel, rend 1) et un fichier de réglage qui l'exige ; un crochet
    `pre-commit` qui note son appel et rend 1, exigé par le seul fichier SYSTÈME ; bâtir les variables des quatre
    formes. ⑦ UNITÉ — —. ⑧ POURQUOI — un réglage hostile posé ICI ne dépend pas de la machine
    (6/N-2 : sur GitHub, rien ne signe). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit quatre fichiers et un dossier sous `d`.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    journal = os.path.join(d, "journal_du_faux_signataire")
    gpg = os.path.join(d, "faux_gpg.sh")
    with open(gpg, "w", encoding="utf-8") as h:
        h.write("#!/bin/sh\necho appel >> '%s'\nexit 1\n" % journal)
    os.chmod(gpg, 0o755)
    hostile = os.path.join(d, "reglage_hostile")
    with open(hostile, "w", encoding="utf-8") as h:
        h.write("[user]\n\tname = machine\n\temail = machine@machine.invalid\n"
                "[commit]\n\tgpgsign = true\n[gpg]\n\tprogram = %s\n" % gpg)
    # LE FICHIER SYSTÈME porte EN PLUS un crochet qui échoue : le réglage global de l'outil, plus prioritaire, couvre
    # la signature (gpgsign = false) mais pas `core.hooksPath` — sans ce crochet, relire le système ne changerait
    # rien au commit et le sabotage S2 resterait vert (mesuré au premier lancement, 15-11-2026).
    crochets = os.path.join(d, "crochets")
    os.makedirs(crochets)
    with open(os.path.join(crochets, "pre-commit"), "w", encoding="utf-8") as h:
        h.write("#!/bin/sh\necho crochet >> '%s'\nexit 1\n" % journal)
    os.chmod(os.path.join(crochets, "pre-commit"), 0o755)
    hostile_systeme = os.path.join(d, "reglage_hostile_systeme")
    with open(hostile_systeme, "w", encoding="utf-8") as h:
        h.write(open(hostile, encoding="utf-8").read() + "[core]\n\thooksPath = %s\n" % crochets)
    cles = [("user.name", "machine"), ("user.email", "machine@machine.invalid"), ("commit.gpgsign", "true"),
            ("gpg.program", gpg)]
    count = {"GIT_CONFIG_COUNT": str(len(cles))}
    for i, (k, v) in enumerate(cles):
        count["GIT_CONFIG_KEY_%d" % i], count["GIT_CONFIG_VALUE_%d" % i] = k, v
    formes = {"global": {"GIT_CONFIG_GLOBAL": hostile, "GIT_CONFIG_NOSYSTEM": "1"},
              "systeme": {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": hostile_systeme},
              "count": dict(count, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1"),
              "parametres": {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                             "GIT_CONFIG_PARAMETERS": " ".join("'%s'='%s'" % kv for kv in cles)}}
    tout = dict(formes["global"])
    tout.update(formes["count"])
    tout.update(formes["parametres"])
    tout.update({"GIT_CONFIG_GLOBAL": hostile, "GIT_CONFIG_SYSTEM": hostile_systeme})
    tout.pop("GIT_CONFIG_NOSYSTEM")
    formes["tout"] = tout
    formes["journal"] = journal
    return formes


def un_commit(outil, variables, avec, journal):
    """Lance un processus enfant qui (avec l'outil ou sans) fait un commit dans un dépôt jetable.
    ① RÔLE — une mesure. ② CONTEXTE D'APPEL — `etalonner`, `jouer`. ③ ENTRÉE — le chemin de l'outil, les variables
    hostiles, `avec` (bool : appeler l'outil), le chemin du journal du faux signataire. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs : la ligne rendue par l'enfant (« COMMIT <code> … » ou « AUTEUR <courriel> »), le nombre
    d'appels au faux signataire. [rend: 2] ⑥ TRAITEMENT — bâtir un environnement NEUF (PATH, HOME vide, LANG) plus
    les variables ; vider le journal ; lancer l'enfant ; compter le journal. ⑦ UNITÉ — un nombre d'appels.
    ⑧ POURQUOI — l'environnement de celui qui lance l'épreuve n'entre pas dans le verdict. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — écrit et efface un dossier temporaire. ⑪ TERMINAISON — borné à 60 s ; un dépassement rend
    « DÉPASSEMENT ». [sort: non]"""
    d = tempfile.mkdtemp(prefix="gsm_commit_")
    try:
        os.makedirs(os.path.join(d, "maison"))
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.path.join(d, "maison"), "LANG": "C.UTF-8",
               "TMPDIR": d}
        env.update(variables)
        if os.path.exists(journal):
            os.remove(journal)
        try:
            r = subprocess.run([sys.executable, "-B", "-c", ENFANT, outil, os.path.join(d, "depot"),
                                "1" if avec else "0"], env=env, capture_output=True, text=True, timeout=60)
            ligne = (r.stdout.strip().splitlines() or ["ENFANT %d %s" % (r.returncode, r.stderr.strip()[-160:])])[-1]
        except subprocess.TimeoutExpired:
            ligne = "DÉPASSEMENT"
        appels = len(open(journal).read().splitlines()) if os.path.exists(journal) else 0
        return ligne, appels
    finally:
        shutil.rmtree(d, ignore_errors=True)


def etalonner(outil, formes):
    """Vérifie que chaque réglage hostile, SANS l'outil, fait échouer le commit et appelle le faux signataire.
    ① RÔLE — l'étalonnage (« un motif se calibre sur un cas qui doit échouer »). ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — l'outil, les formes. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la liste des formes qui NE
    rougissent PAS sans l'outil (vide si l'étalonnage tient). [rend: 1] ⑥ TRAITEMENT — un commit sans l'outil par
    forme. ⑦ UNITÉ — —. ⑧ POURQUOI — si un réglage hostile ne fait pas échouer git ici, le cas qui l'emploie serait
    vert quoi que fasse l'outil. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche une ligne par forme.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    muettes = []
    for f in FORMES + ("tout",):
        ligne, appels = un_commit(outil, formes[f], False, formes["journal"])
        ok = ligne.startswith("COMMIT ") and appels >= 1
        print("  ÉTALON %-10s sans l'outil : %s · faux signataire ou crochet appelé %d fois%s"
              % (f, ligne[:70], appels, "" if ok else "  ← NE ROUGIT PAS"))
        if not ok:
            muettes.append(f)
    return muettes


def jouer(racine, formes, sabotage):
    """Joue les cas sur une copie de l'outil et de CERTIFIER, sabotée ou non.
    ① RÔLE — un tour. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `racine`, les formes, `sabotage` (« Z0 » ou une clé
    de SABOTAGES). ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la liste des [nom, vert, détail]. [rend: 1]
    ⑥ TRAITEMENT — copier les deux fichiers sous /tmp/gsm_code_* EN GARDANT leur place relative (l'outil cherche
    CERTIFIER à ../../programmes), appliquer, jouer H_<forme>, H_tout et I_identite, effacer. ⑦ UNITÉ — —.
    ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit et efface un dossier. ⑪ TERMINAISON — Rend la main ;
    lève LookupError si une cible de sabotage n'est pas présente une fois. [sort: non]"""
    copie = tempfile.mkdtemp(prefix="gsm_code_")
    try:
        for f in (OUTIL, CERTIF):
            os.makedirs(os.path.dirname(os.path.join(copie, f)), exist_ok=True)
            shutil.copy(os.path.join(racine, f), os.path.join(copie, f))
        for f, avant, apres in SABOTAGES.get(sabotage, ([], set()))[0]:
            p = os.path.join(copie, f)
            s = open(p, encoding="utf-8").read()
            if s.count(avant) != 1:
                raise LookupError("cible du sabotage %s présente %d fois : %r" % (sabotage, s.count(avant), avant[:60]))
            open(p, "w", encoding="utf-8").write(s.replace(avant, apres))
        outil = os.path.join(copie, OUTIL)
        res = []
        for f in FORMES + ("tout",):
            ligne, appels = un_commit(outil, formes[f], True, formes["journal"])
            res.append(["H_" + f, ligne == "AUTEUR " + EMAIL and appels == 0,
                        "%s · faux signataire ou crochet appelé %d fois" % (ligne[:90], appels)])
        ligne, appels = un_commit(outil, {}, True, formes["journal"])
        res.append(["I_identite", ligne == "AUTEUR " + EMAIL, ligne[:90]])
        return res
    finally:
        shutil.rmtree(copie, ignore_errors=True)


def main(argv):
    """Étalonne, joue Z0 puis les sabotages demandés.
    ① RÔLE — le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — vérifier les données ;
    étalonner (2 si une forme ne rougit pas) ; Z0 ; chaque sabotage doit rougir exactement ses cas visés.
    ⑦ UNITÉ — —. ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche ; écrit et efface un dossier
    temporaire. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if not argv:
        print("usage : EPREUVES_DE_GIT_SANS_LA_MACHINE_Dim_15-11-2026.py <racine> [--saboter | nom]")
        return 2
    racine = os.path.abspath(argv[0])
    for f in (OUTIL, CERTIF):
        if not os.path.exists(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            return 2
    demandes = []
    if len(argv) > 1:
        demandes = list(SABOTAGES) if argv[1] == "--saboter" else [argv[1]]
        if any(s not in SABOTAGES for s in demandes):
            print("sabotage inconnu : %s" % argv[1])
            return 2
    d = tempfile.mkdtemp(prefix="gsm_decor_")
    try:
        formes = preparer(d)
        muettes = etalonner(os.path.join(racine, OUTIL), formes)
        if muettes:
            print("ÉTALONNAGE MUET : %s — l'épreuve ne prouverait rien ici (R-734)" % ", ".join(muettes))
            return 2
        z0 = jouer(racine, formes, "Z0")
        rouges = [x for x in z0 if not x[1]]
        for nom, vert, det in z0:
            print("  %s  %s  — %s" % ("VERT " if vert else "ROUGE", nom, det))
        print("== Z0 : %d cas, %d rouge(s)" % (len(z0), len(rouges)))
        code = 1 if rouges else 0
        for s in demandes:
            try:
                r = jouer(racine, formes, s)
            except LookupError as ex:
                print(ex)
                return 2
            mord = {n for n, v, _d in r if not v}
            vise = SABOTAGES[s][1]
            juste = mord == vise
            print("  %s  %s — rougis : %s · visés : %s" % (("MORD " if mord else "VERT ") if juste else "FAUX ", s,
                  ", ".join(sorted(mord)) or "aucun", ", ".join(sorted(vise)) or "aucun (neutre)"))
            if not juste:
                code = 1
        print("VERDICT : %s" % ("conforme" if code == 0 else "NON CONFORME"))
        return code
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
