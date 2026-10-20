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
⑤ SORTIE — Le code de sortie : 0 si J1, J2 et J3 donnent la réponse attendue et, avec --saboter, si chaque sabotage en
  fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT — Un dépôt d'essai dont l'unique épreuve écrit « A1 mord » seulement si elle tourne sans la configuration
  git de la machine (GIT_CONFIG_GLOBAL vaut os.devnull, GIT_CONFIG_NOSYSTEM vaut 1, GIT_CONFIG_COUNT vaut 0 et
  GIT_CONFIG_PARAMETERS est vide). Le joueur est lancé avec une configuration git de la machine posée exprès
  (GIT_CONFIG_GLOBAL vers un fichier, un réglage par GIT_CONFIG_COUNT, un par GIT_CONFIG_PARAMETERS) : il doit l'ôter. J1 le joueur → code 0, relevé conforme qui porte « A1 mord » · J2 calibrage sur un cas qui doit
  échouer : l'épreuve d'essai lancée directement dans le même environnement écrit « A1 NE MORD PAS » · J3 une
  épreuve qui lit un fichier du dépôt puis l'efface : le joueur s'arrête sur « ARRET », code 2, sans trace. Avec
  --saboter : chaque garde du joueur retirée, une à la fois, dans une copie.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Cassure N de Cowork, 17-10-2026 : le joueur ne neutralisait pas la configuration git, la nuit si ; le
  relevé de la boucle de check avait été écrit dans un autre environnement que celui où la nuit le rejoue, et 14
  sabotages avaient « mordu » parce qu'un `git commit` du montage était refusé. L'environnement est posé EXPRÈS par
  l'épreuve, et pas hérité : la certification lance déjà ses épreuves sans la configuration git, et un joueur qui ne
  la poserait pas resterait vert sous elle (même piège que S26 de l'épreuve de la certification, 02-10-2026).
⑨ CE QUI CLOCHE — Seule la garde de l'environnement est éprouvée ici ; le reste du joueur l'est par ses séries réelles.
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
SABOTAGES = {
    "S1_configuration_git_gardee": [("    env.update(CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)", "    pass")],
    "S2_fichier_disparu_plante": [("if not os.path.isfile(os.path.join(racine, c))\n              or SERIE.empreinte",
                                   "if SERIE.empreinte")],
}


def tour(joueur):
    """Joue J1, J2 et J3 avec le joueur à `joueur` ; rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `joueur` : le chemin du joueur à éprouver. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms des cas faux. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête, ⑥.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Un dépôt d'essai jetable.
    ⑪ TERMINAISON — Rend la main ; trois lancements bornés à 120 secondes. [sort: non]
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
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête ; le
    joueur saboté est écrit dans un dépôt jetable dont programmes/ renvoie à celui de la racine, parce que le joueur
    importe ses modules depuis ../../programmes. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(JOUEUR)
    print("Z0 joueur tel quel : " + ("J1, J2 et J3 conformes" if not faux else "FAUX " + ", ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv:
        texte = open(JOUEUR, encoding="utf-8").read()
        for nom, remplacements in SABOTAGES.items():
            t = texte
            for a, b in remplacements:
                if t.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois")
                    return 2
                t = t.replace(a, b)
            d = tempfile.mkdtemp(prefix="joueur_sab_")
            try:
                os.makedirs(os.path.join(d, "tests", "outils"))
                os.symlink(os.path.join(DEPOT, "programmes"), os.path.join(d, "programmes"))
                p = os.path.join(d, "tests", "outils", "JOUER_UNE_SERIE_DE_SABOTAGES.py")
                open(p, "w", encoding="utf-8").write(t)
                f = tour(p)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
