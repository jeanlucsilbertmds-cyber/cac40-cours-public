#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_JOUEUR_DE_SERIES — Sam 17-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py joue une série dans l'environnement où la nuit en
  refait les essais : sans la configuration git de la machine. Et que cette garde a des dents.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py) ; à la main avant toute
  livraison qui touche le joueur (R-731) : python3 tests/EPREUVES_DU_JOUEUR_DE_SERIES_Sam_17-10-2026.py <racine>
  [--saboter]
③ ENTRÉE — La racine du dépôt (le joueur est pris dans son tests/outils/, ses modules dans son programmes/).
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le code de sortie : 0 si J1 à J6 donnent la réponse attendue et, avec --saboter, si chaque sabotage en
  fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT — Un dépôt d'essai dont l'unique épreuve écrit « A1 mord » seulement si elle tourne sans la configuration
  git de la machine (GIT_CONFIG_GLOBAL vaut os.devnull, GIT_CONFIG_NOSYSTEM vaut 1, GIT_CONFIG_COUNT vaut 0 et
  GIT_CONFIG_PARAMETERS est vide). Le joueur est lancé avec une configuration git de la machine posée exprès
  (GIT_CONFIG_GLOBAL vers un fichier, un réglage par GIT_CONFIG_COUNT, un par GIT_CONFIG_PARAMETERS) : il doit l'ôter. J1 le joueur → code 0, relevé conforme qui porte « A1 mord » · J2 calibrage sur un cas qui doit
  échouer : l'épreuve d'essai lancée directement dans le même environnement écrit « A1 NE MORD PAS » · J3 une
  épreuve qui lit un fichier du dépôt puis l'efface : le joueur s'arrête sur « ARRET », code 2, sans trace · J4 (ajouté
  le 04-11-2026, décision de Jean-Luc n°71 du 01-11-2026 à 11h41 : la série de l'épreuve d'arrivée des signaux ne se
  rejoue que quand le code de l'épreuve change) : la table de lancement du dépôt d'essai déclare la portée « epreuve »
  pour une épreuve qui lit donnees/d.csv : code 0, le relevé porte UNE empreinte, celle de l'épreuve, et dit sa portée ·
  J5 une portée inconnue (« partout ») : « ARRET », code 2, aucun relevé · J6 (ajouté le 05-11-2026, CHOIX D43 DU
  CHAT, À CONFIRMER PAR JEAN-LUC : la portée « code_execute », le code que la série exécute, sans les données) : une
  épreuve faite à la manière de l'épreuve d'arrivée des signaux — elle copie le dépôt dans un dossier temporaire et y
  relance sa copie, qui EXÉCUTE programmes/M.py de la copie et lit donnees/d.csv ; programmes/N_inutilise.py est
  copié mais jamais exécuté. Code 0, le relevé porte exactement programmes/M.py et l'épreuve, NI le module inutilisé
  NI la donnée, et dit sa portée. Avec --saboter : chaque garde du joueur retirée, une à la fois, dans une copie ; un
  sabotage peut viser aussi programmes/SERIES_DE_SABOTAGES.py (le ramenage au dépôt d'un code exécuté dans une copie).
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Cassure N de Cowork, 17-10-2026 : le joueur ne neutralisait pas la configuration git, la nuit si ; le
  relevé de la boucle de check avait été écrit dans un autre environnement que celui où la nuit le rejoue, et 14
  sabotages avaient « mordu » parce qu'un `git commit` du montage était refusé. L'environnement est posé EXPRÈS par
  l'épreuve, et pas hérité : la certification lance déjà ses épreuves sans la configuration git, et un joueur qui ne
  la poserait pas resterait vert sous elle (même piège que S26 de l'épreuve de la certification, 02-10-2026).
⑨ CE QUI CLOCHE — Seules la garde de l'environnement, la portée et la mesure du code exécuté sont éprouvées ici ; le
  reste du joueur l'est par ses séries réelles. La mesure « exec » n'est prouvée que sous le Python qui lance cette
  épreuve (3.13 sur la machine du Chat le 05-11-2026) : chaque nuit où J6 tourne, elle l'est sous celui de la nuit.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 secondes ; sort par sys.exit.
  [sort: oui]
"""
import os
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
JOUEUR = os.path.join(DEPOT, "tests", "outils", "JOUER_UNE_SERIE_DE_SABOTAGES.py")
EPREUVE = ('import os, sys\nSABOTAGES = {"A1": 1}\n'
           'ok = (os.environ.get("GIT_CONFIG_GLOBAL") == os.devnull and os.environ.get("GIT_CONFIG_NOSYSTEM") == "1"\n'
           '      and os.environ.get("GIT_CONFIG_COUNT") == "0" and not os.environ.get("GIT_CONFIG_PARAMETERS"))\n'
           'print("Z0 programme tel quel : tous les cas conformes")\n'
           'print("A1 mord : [\'H1\']" if ok else "A1 NE MORD PAS : []")\n'
           'sys.exit(0 if ok else 1)\n')
# J3 : une épreuve qui lit un fichier du dépôt, puis l'efface (relecture indépendante, 17-10-2026, tour 15 : le joueur
# sortait sur une trace, code 1, au lieu d'un ARRET, code 2).
EPREUVE_QUI_EFFACE = ('import os, sys\nSABOTAGES = {"A1": 1}\n'
                      'f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "donnees", "d.csv")\n'
                      'if os.path.isfile(f):\n    open(f).read()\n    os.remove(f)\n'
                      'print("Z0 programme tel quel : tous les cas conformes")\nprint("A1 mord : [\'H1\']")\n')
# J4 et J5 : une épreuve qui lit une donnée du dépôt, et une table de lancement qui déclare la portée de son relevé
EPREUVE_QUI_LIT = ('import os, sys\nSABOTAGES = {"A1": 1}\n'
                   'open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "donnees", "d.csv")).read()\n'
                   'print("Z0 programme tel quel : tous les cas conformes")\nprint("A1 mord : [\'H1\']")\n')
# J6 : une épreuve à la manière de l'épreuve d'arrivée — copie du dépôt, puis un sous-processus qui EXÉCUTE un module
# de la copie et lit une donnée ; un module jamais exécuté reste à côté
EPREUVE_QUI_EXECUTE = ('import os, sys, shutil, subprocess, tempfile, importlib.util\nSABOTAGES = {"A1": 1}\n'
                       'if len(sys.argv) > 2 and sys.argv[1] == "--cas":\n'
                       '    c = sys.argv[2]\n'
                       '    sp = importlib.util.spec_from_file_location("M", os.path.join(c, "programmes", "M.py"))\n'
                       '    m = importlib.util.module_from_spec(sp)\n    sp.loader.exec_module(m)\n'
                       '    open(os.path.join(c, "donnees", "d.csv")).read()\n'
                       '    sys.exit(0 if m.VAL == 1 else 1)\n'
                       'racine = os.path.abspath(sys.argv[1])\n'
                       'd = tempfile.mkdtemp(prefix="joueur_j6_")\nr = os.path.join(d, "r")\n'
                       'shutil.copytree(racine, r)\n'
                       'code = subprocess.run([sys.executable, "-B", os.path.join(r, "tests", "EPR.py"), "--cas", r]).returncode\n'
                       'shutil.rmtree(d)\n'
                       'print("Z0 programme tel quel : tous les cas conformes")\n'
                       'print("A1 mord : [\'H1\']" if code == 0 else "A1 NE MORD PAS : []")\n')
TABLE_A_PORTEE = ('{"epreuves": {}, "series_hors_de_la_nuit": {"tests/EPR.py": {"releve": "tests/resultats/SERIE_*.txt", '
                  '"essais_refaits_chaque_nuit": 0, "portee_du_releve": "%s"}}}\n')
# Un remplacement est (cible, texte) dans le joueur, ou (fichier relatif, cible, texte) dans un autre fichier du dépôt.
SERIE_PY = "programmes/SERIES_DE_SABOTAGES.py"
SABOTAGES = {
    "S1_configuration_git_gardee": [("    env.update(CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)", "    pass")],
    "S2_fichier_disparu_plante": [("if not os.path.isfile(os.path.join(racine, c))\n              or SERIE.empreinte",
                                   "if SERIE.empreinte")],
    "S3_portee_ignoree": [("    couverts = lus if portee == SERIE.PORTEE_LECTURES else executes\n", "    couverts = lus\n")],
    "S4_portee_inconnue_admise": [("    if portee not in SERIE.PORTEES:\n", "    if False:\n")],
    # choix D43 du 05-11-2026 : le code exécuté, mesuré par « exec » et ramené au dépôt (J6 doit rougir)
    "S5_mesure_par_ouverture": [('    executes = SERIE.fichiers_executes(os.path.join(travail, "execution"), etat)\n',
                                 '    executes = SERIE.fichiers_executes(os.path.join(travail, "ecoute"), etat)\n')],
    "S6_ramenage_des_copies_retire": [(SERIE_PY, "    for i in range(len(morceaux)):\n", "    for i in range(0):\n")],
}


def tour(joueur):
    """Joue J1 à J6 avec le joueur à `joueur` ; rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `joueur` : le chemin du joueur à éprouver. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms des cas faux. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête, ⑥.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Un dépôt d'essai jetable.
    ⑪ TERMINAISON — Rend la main ; six lancements bornés à 120 secondes. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="joueur_")
    try:
        r = os.path.join(d, "depot")
        os.makedirs(os.path.join(r, "tests"))
        open(os.path.join(r, "tests", "EPR.py"), "w", encoding="utf-8").write(EPREUVE)
        machine = os.path.join(d, "configuration_git_de_la_machine")
        open(machine, "w").write("[commit]\n\tgpgsign = true\n")
        env = dict(os.environ, GIT_CONFIG_GLOBAL=machine, GIT_CONFIG_NOSYSTEM="", GIT_CONFIG_COUNT="1",
                   GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="true", GIT_CONFIG_PARAMETERS="'user.name'='x'")
        rel = "tests/resultats/SERIE_DE_SABOTAGES_DE_L_ESSAI_Sam_17-10-2026_10h00.txt"
        j = subprocess.run([sys.executable, joueur, r, "tests/EPR.py", rel, "--parts=1", "--lot=1",
                            "--travail=" + os.path.join(d, "travail")], capture_output=True, text=True, env=env,
                           timeout=120)
        releve = open(os.path.join(r, rel), encoding="utf-8").read() if os.path.isfile(os.path.join(r, rel)) else ""
        if j.returncode != 0 or "A1 mord : ['H1']" not in releve:
            faux.append(f"J1 (code {j.returncode})")
        e = subprocess.run([sys.executable, os.path.join(r, "tests", "EPR.py")], capture_output=True, text=True,
                           env=env, timeout=120)
        if "A1 NE MORD PAS" not in e.stdout:
            faux.append("J2")
        r3 = os.path.join(d, "depot3")
        os.makedirs(os.path.join(r3, "tests"))
        os.makedirs(os.path.join(r3, "donnees"))
        open(os.path.join(r3, "tests", "EPR.py"), "w", encoding="utf-8").write(EPREUVE_QUI_EFFACE)
        open(os.path.join(r3, "donnees", "d.csv"), "w", encoding="utf-8").write("1,2,3\n")
        j3 = subprocess.run([sys.executable, joueur, r3, "tests/EPR.py", rel, "--parts=1", "--lot=1",
                             "--travail=" + os.path.join(d, "travail3")], capture_output=True, text=True, env=env,
                            timeout=120)
        if j3.returncode != 2 or "ARRET" not in j3.stdout:
            faux.append(f"J3 (code {j3.returncode})")
        for cas, portee in (("J4", "epreuve"), ("J5", "partout")):
            r4 = os.path.join(d, "depot_" + cas)
            for c, texte in (("tests/EPR.py", EPREUVE_QUI_LIT), ("donnees/d.csv", "1,2,3\n"),
                             ("tests/LANCEMENT_DES_EPREUVES.json", TABLE_A_PORTEE % portee)):
                os.makedirs(os.path.dirname(os.path.join(r4, c)), exist_ok=True)
                open(os.path.join(r4, c), "w", encoding="utf-8").write(texte)
            j4 = subprocess.run([sys.executable, joueur, r4, "tests/EPR.py", rel, "--parts=1", "--lot=1",
                                 "--travail=" + os.path.join(d, "travail_" + cas)], capture_output=True, text=True,
                                env=env, timeout=120)
            p4 = os.path.join(r4, rel)
            releve4 = open(p4, encoding="utf-8").read() if os.path.isfile(p4) else ""
            empreintes = [l.split(" ", 2)[2] for l in releve4.splitlines() if l.startswith("EMPREINTE ")]
            if cas == "J4" and (j4.returncode != 0 or empreintes != ["tests/EPR.py"]
                                or "# portée du relevé : epreuve" not in releve4):
                faux.append(f"J4 (code {j4.returncode}, empreintes {empreintes})")
            if cas == "J5" and (j4.returncode != 2 or "ARRET" not in j4.stdout or releve4):
                faux.append(f"J5 (code {j4.returncode})")
        # J6 : la portée « code_execute » — le relevé porte le code exécuté dans la copie, ni le module inutilisé ni la donnée
        r6 = os.path.join(d, "depot_J6")
        for c, texte in (("tests/EPR.py", EPREUVE_QUI_EXECUTE), ("programmes/M.py", "VAL = 1\n"),
                         ("programmes/N_inutilise.py", "VAL = 2\n"), ("donnees/d.csv", "1,2,3\n"),
                         ("tests/LANCEMENT_DES_EPREUVES.json", TABLE_A_PORTEE % "code_execute")):
            os.makedirs(os.path.dirname(os.path.join(r6, c)), exist_ok=True)
            open(os.path.join(r6, c), "w", encoding="utf-8").write(texte)
        j6 = subprocess.run([sys.executable, joueur, r6, "tests/EPR.py", rel, "--parts=1", "--lot=1",
                             "--travail=" + os.path.join(d, "travail_J6")], capture_output=True, text=True,
                            env=env, timeout=120)
        p6 = os.path.join(r6, rel)
        releve6 = open(p6, encoding="utf-8").read() if os.path.isfile(p6) else ""
        empreintes6 = [l.split(" ", 2)[2] for l in releve6.splitlines() if l.startswith("EMPREINTE ")]
        if (j6.returncode != 0 or empreintes6 != ["programmes/M.py", "tests/EPR.py"]
                or "# portée du relevé : code_execute" not in releve6):
            faux.append(f"J6 (code {j6.returncode}, empreintes {empreintes6})")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête ; le
    joueur saboté est écrit dans un dépôt jetable dont programmes/ renvoie à celui de la racine, parce que le joueur
    importe ses modules depuis ../../programmes ; quand un sabotage vise un fichier de programmes/, ce dossier est fait
    de liens vers chaque fichier de la racine, sauf ce fichier, écrit saboté. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(JOUEUR)
    print("Z0 joueur tel quel : " + ("J1 à J6 conformes" if not faux else "FAUX " + ", ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv:
        for nom, remplacements in SABOTAGES.items():
            textes = {}       # fichier relatif → texte saboté ; le joueur est « tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py »
            for r in remplacements:
                fichier, a, b = r if len(r) == 3 else ("tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py",) + tuple(r)
                t = textes.get(fichier) or open(os.path.join(DEPOT, fichier), encoding="utf-8").read()
                if t.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                    return 2
                textes[fichier] = t.replace(a, b)
            textes.setdefault("tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py",
                              open(JOUEUR, encoding="utf-8").read())
            d = tempfile.mkdtemp(prefix="joueur_sab_")
            try:
                os.makedirs(os.path.join(d, "tests", "outils"))
                if any(f.startswith("programmes/") for f in textes):
                    os.makedirs(os.path.join(d, "programmes"))
                    for f in os.listdir(os.path.join(DEPOT, "programmes")):
                        if "programmes/" + f not in textes:
                            os.symlink(os.path.join(DEPOT, "programmes", f), os.path.join(d, "programmes", f))
                else:
                    os.symlink(os.path.join(DEPOT, "programmes"), os.path.join(d, "programmes"))
                for f, t in textes.items():
                    open(os.path.join(d, f), "w", encoding="utf-8").write(t)
                p = os.path.join(d, "tests", "outils", "JOUER_UNE_SERIE_DE_SABOTAGES.py")
                f = tour(p)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
