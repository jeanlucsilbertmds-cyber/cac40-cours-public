#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_SOCLE_STABLE — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que programmes/FABRIQUER_LE_SOCLE.py rend le même classement à chaque lancement, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche le parcours de fabriquer dans programmes/FABRIQUER_LE_SOCLE.py (R-755 ②).

À QUOI ÇA SERT. Mesure du 28-09-2026 : sur le même dépôt, six lancements du socle avec six graines de
hachage différentes (PYTHONHASHSEED 0 à 5) rendaient SIX classements différents (de 2 à 6 lignes sur 306). Seule la colonne
« pourquoi » changeait (« appele par TENIR_LES_POSITIONS.py » ou « appele par
DETECTER_LES_SIGNAUX_GITHUB.py » pour le même programme) : le parcours suivait l'ordre d'un ensemble
Python, qui change d'un lancement à l'autre. Un fichier FABRIQUÉ qui change sans que rien n'ait changé
fait croire à un changement. Réparé : le parcours est trié. Ce fichier lance le socle sous douze graines,
sur le dépôt (Z0) et sur un dépôt où un programme est appelé par deux autres (Z1), et exige une seule
sortie ; chaque sabotage retire un tri.

USAGE : python3 tests/EPREUVES_DU_SOCLE_STABLE_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et que chaque sabotage fait rougir l'épreuve ; 1 sinon.
"""
import hashlib, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
SO = "programmes/FABRIQUER_LE_SOCLE.py"
# Z1 fabrique un losange : deux programmes appelés par un programme du soir appellent tous
# deux un troisième (relecteur du Chat, 28-09-2026). Sur le dépôt réel, aucun programme n'est
# dans ce cas, et un tri manquant dans les boucles ne se voyait pas.
LOSANGE = [("programmes/NOUV_BBB.py", "import NOUV_DDD\n"), ("programmes/NOUV_CCC.py", "import NOUV_DDD\n"),
           ("programmes/NOUV_DDD.py", "X = 1\n"),
           # un nom importé qui désigne DEUX fichiers par son début (NOUV_XX → NOUV_XX_1, NOUV_XX_2),
           # qui appellent tous deux NOUV_ZZ : l'ordre des candidats décide du « pourquoi »
           ("programmes/NOUV_XX_1.py", "import NOUV_ZZ\n"), ("programmes/NOUV_XX_2.py", "import NOUV_ZZ\n"),
           ("programmes/NOUV_ZZ.py", "Z = 1\n")]
SABOTAGES = {
    "Z0": [],
    "Z1_losange": [],
    "S1_pile_dans_l_ordre_d_un_ensemble": [(SO, "sorted(lances), {}, {}", "list(lances), {}, {}")],
    "S2_appeles_dans_l_ordre_d_un_ensemble": [(SO, "        for a in sorted(progs):", "        for a in progs:")],
    "S3_candidats_dans_l_ordre_d_un_ensemble": [(SO, "            for t in sorted(noms_py):\n                if t == cible",
                                                 "            for t in noms_py:\n                if t == cible")],
}
AVEC_LOSANGE = {"Z1_losange", "S2_appeles_dans_l_ordre_d_un_ensemble", "S3_candidats_dans_l_ordre_d_un_ensemble"}
GRAINES = 12


def empreintes(sab):
    d = tempfile.mkdtemp(prefix="socle_stable_")
    try:
        r = os.path.join(d, "r")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            assert t.count(a) == 1, (sab, a[:50])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))
        if sab in AVEC_LOSANGE:
            for f, texte in LOSANGE:
                with open(os.path.join(r, f), "w", encoding="utf-8") as h:
                    h.write(texte)
            p = os.path.join(r, "programmes", "TENIR_L_HISTORIQUE.py")    # lancé par la tâche du soir
            t = open(p, encoding="utf-8").read()
            with open(p, "w", encoding="utf-8") as h:
                h.write("import NOUV_BBB\nimport NOUV_CCC\nimport NOUV_XX\n" + t)
        vus = set()
        for k in range(GRAINES):
            sortie = os.path.join(d, "socle_%d.csv" % k)
            x = subprocess.run([sys.executable, SO, ".", sortie], cwd=r, capture_output=True, text=True,
                               env={**os.environ, "PYTHONHASHSEED": str(k)}, timeout=600)
            if x.returncode != 0:
                return None, "code %d à la graine %d" % (x.returncode, k)
            lignes = open(sortie, encoding="utf-8").read().split("\n")[1:]   # la 1re ligne porte l'heure
            vus.add(hashlib.sha256("\n".join(lignes).encode()).hexdigest()[:12])
        return vus, ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    vus, err = empreintes(sab)
    stable = vus is not None and len(vus) == 1
    ok = stable if sab.startswith("Z") else (vus is not None and len(vus) > 1)
    print(f"== {sab} : {'OK' if ok else 'ÉCHEC'} · {len(vus) if vus else 0} sortie(s) distincte(s) sur {GRAINES} graines {err}")
    _faute = _faute or not ok
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
