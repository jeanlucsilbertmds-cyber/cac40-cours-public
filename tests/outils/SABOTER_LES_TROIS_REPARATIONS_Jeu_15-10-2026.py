#!/usr/bin/env python3
"""Sabote chacune des trois réparations du 15-10-2026 contre sa propre épreuve, sur des copies : chaque sabotage doit faire rougir."""
import os, shutil, subprocess, sys, tempfile
from datetime import datetime
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
import CERTIFIER_LA_VERSION as CERTIF  # noqa: E402  (l'environnement de la nuit, défini une fois)
DEPOT = sys.argv[1]
CAS = [
 ("SA retirer les deux programmes ajoutés à COPIE_DES_BOUCLES", "tests/EPREUVES_DE_LA_COPIE_DES_BOUCLES_Jeu_01-10-2026.py",
  "programmes/CONTRATS_DES_FICHIERS.py",
  '    "programmes/REPARER_L_HISTORIQUE_LONG.py",\n    "programmes/CONTROLER_L_HISTORIQUE_LONG.py",\n', ""),
 ("SB remettre le résumé du 10-10 dans l'épreuve de la reconstruction", "tests/EPREUVES_DE_LA_RECONSTRUCTION_Sam_10-10-2026.py",
  "tests/EPREUVES_DE_LA_RECONSTRUCTION_Sam_10-10-2026.py",
  'reconstruite : 144876 · "\n          "reconstruite au facteur appliqué : 5761 · sans cours brut : 67621")',
  'reconstruite : 144874 · "\n          "reconstruite au facteur appliqué : 5761 · sans cours brut : 67621 · écart à Google : 1")'),
 ("SB2 remettre les deux tables de la reconstruction du 10-10", "tests/EPREUVES_DE_LA_RECONSTRUCTION_Sam_10-10-2026.py", None, "git:1133f6e", ""),
 ("SC lire le dépôt au lieu de la copie figée", "tests/EPREUVES_DE_LA_LECTURE_DES_COURS_Sam_10-10-2026.py",
  "tests/EPREUVES_DE_LA_LECTURE_DES_COURS_Sam_10-10-2026.py", "DEPOT = depot_fige(DEPOT_DONNE)\n", "DEPOT = DEPOT_DONNE\n"),
 ("SC2 un témoin figé manque", "tests/EPREUVES_DE_LA_LECTURE_DES_COURS_Sam_10-10-2026.py", "RETIRER",
  "temoins/TEMOIN_cours_maitre_JEU_DE_LA_LECTURE_DES_COURS_13-10-2026.csv", ""),
]
lignes = [f"SABOTAGES DES TROIS RÉPARATIONS — {datetime.now(ZoneInfo('Europe/Paris')):%a %d-%m-%Y %Hh%M} (Paris), dépôt {DEPOT}",
          "Chaque sabotage retire une réparation dans une copie ; l'épreuve qu'elle répare DOIT alors rendre un code non nul.", ""]
code_final = 0
for nom, epreuve, fichier, ancien, nouveau in CAS:
    c = tempfile.mkdtemp(prefix="sab3_")
    subprocess.run(f"tar -C {DEPOT} --exclude=.git -cf - . | tar -C {c} -xf -", shell=True, check=True)
    if fichier == "RETIRER":
        os.remove(os.path.join(c, ancien))
    elif fichier is None:
        for t in ("RECONSTRUCTION_PAR_OPERATION.csv", "RECONSTRUCTION_ECARTS.csv"):
            v = subprocess.run(["git", "-C", DEPOT, "show", "1133f6e:donnees/sources_yahoo/" + t], capture_output=True, check=True).stdout
            open(os.path.join(c, "donnees/sources_yahoo", t), "wb").write(v)
    else:
        p = os.path.join(c, fichier); s = open(p, encoding="utf-8").read()
        if s.count(ancien) != 1:
            lignes.append(f"{nom} : INAPPLICABLE"); code_final = 2; shutil.rmtree(c, True); continue
        open(p, "w", encoding="utf-8").write(s.replace(ancien, nouveau))
    env = dict(os.environ)
    env.update(CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)   # défini une fois, R-708 (cassure N, 17-10-2026)
    r = subprocess.run([sys.executable, "-B", os.path.join(c, epreuve), c], cwd=c, env=env, capture_output=True, text=True, timeout=1800)
    sortie = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    utiles = [l for l in sortie if any(m in l for m in ("ROUGE", "Z0", "VERDICT", "ARRÊT"))][:6] or sortie[-3:]
    mord = r.returncode != 0
    if not mord: code_final = max(code_final, 1)
    lignes.append(f"{nom} : code {r.returncode} — {'MORD' if mord else 'SANS EFFET'}")
    lignes += ["    " + l for l in utiles]
    shutil.rmtree(c, True)
lignes.append(""); lignes.append("VERDICT : " + ("chaque sabotage mord" if code_final == 0 else f"NON CONFORME (code {code_final})"))
print("\n".join(lignes)); sys.exit(code_final)
