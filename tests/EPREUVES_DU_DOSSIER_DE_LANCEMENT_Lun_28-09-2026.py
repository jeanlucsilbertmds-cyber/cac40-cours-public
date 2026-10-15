#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_DOSSIER_DE_LANCEMENT — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que le verdict de programmes/EPREUVES_DU_GARDE_FOU.py ne dépend pas du dossier d'où on le lance.
Quand l'appeler : avant toute livraison qui touche programmes/EPREUVES_DU_GARDE_FOU.py ou la façon dont
programmes/CONTROLER_MA_LIVRAISON.py choisit le dossier où il rejoue les commandes citées (R-755 ②).

À QUOI ÇA SERT. Mesure du 28-09-2026, 00h50 : sur le même code, les épreuves du garde-fou rendaient
le code 0 lancées depuis la racine du dépôt, et le code 1 lancées depuis programmes/, avec
« ❌ refus ligne 1110 AUCUNE ÉPREUVE NE LE VOIT ». Même résultat sur la version a568952 : le défaut
existait avant la nuit. Cause : le cas « aucun programme à confronter » n'a pas de dossier programmes,
et pour lui le garde-fou rejoue les commandes citées depuis le DOSSIER COURANT. Depuis programmes/,
la commande « python3 programmes/EPREUVES_DU_SOCLE.py . » ne trouve rien, un second refus s'ajoute,
et neutraliser le premier ne fait plus passer le cas. Réparation : les épreuves lancent le garde-fou
depuis un dossier neutre fixe (fonction dossier_neutre).

CE FICHIER lance les épreuves du garde-fou depuis deux dossiers qui ne sont pas la racine, sur une
COPIE du dépôt, et exige le code 0. Chaque sabotage retire la réparation ; au moins une épreuve doit
rougir (R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve).

USAGE : python3 tests/EPREUVES_DU_DOSSIER_DE_LANCEMENT_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Durée : mesurée par le relecteur le 28-09-2026, 16 s pour Z0 et 46 s avec --saboter.
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
EGF = "programmes/EPREUVES_DU_GARDE_FOU.py"
_SAB = ('                               capture_output=True, text=True, errors="replace",\n'
        '                               cwd=dossier_neutre())')
SABOTAGES = {
    "Z0": [],
    # le sabotage retire le dossier neutre là où il compte : la relance contre la copie sabotée
    "S1_sabotage_relance_depuis_le_dossier_courant": [(EGF, _SAB,
        '                               capture_output=True, text=True, errors="replace")')],
    # le dossier neutre existe, mais vide : aucun des deux scripts cités n'y est posé
    "S2_dossier_neutre_sans_ses_scripts": [(EGF, "        for nom, source in SCRIPTS_CITES.items():",
                                            "        for nom, source in {}.items():")],
}


def copie(sab):
    d = tempfile.mkdtemp(prefix="lanc_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, (sab, f, a[:50])
        with open(p, "w", encoding="utf-8") as h:
            h.write(t.replace(a, b))
    return d


def epreuves(sab):
    d = copie(sab)
    res = []
    # E2 : un dossier vide, jamais la racine du disque — sans dossier neutre, le garde-fou
    # recopierait le dossier courant entier pour y rejouer les commandes citées.
    for nom, ou in (("E1 lancées depuis programmes/", os.path.join(d, "programmes")),
                    ("E2 lancées depuis un dossier vide", tempfile.mkdtemp(prefix="vide_"))):
        r = subprocess.run([sys.executable, os.path.join(d, EGF)], cwd=ou,
                           capture_output=True, text=True, errors="replace", timeout=1800)
        sortie = r.stdout + r.stderr
        ok = r.returncode == 0 and "AUCUNE ÉPREUVE NE LE VOIT" not in sortie
        res.append((nom, ok, "code %d · %s" % (r.returncode, sortie.strip().splitlines()[-1][:70]
                                              if sortie.strip() else "(rien)")))
    shutil.rmtree(d, ignore_errors=True)
    return res


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    r = epreuves(sab)
    rouges = [x for x in r if not x[1]]
    vert = sab == "Z0"
    print(f"== {sab} : {len(r) - len(rouges)} vertes, {len(rouges)} rouges" + (
        "  <-- ATTENDU : 0 rouge" if vert and rouges else "  <-- SABOTAGE NON VU" if not vert and not rouges else ""))
    for nom, ok, det in r:
        if not ok:
            print(f"     ROUGE {nom} · {det}")
    _faute = _faute or (vert and bool(rouges)) or (not vert and not rouges)
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
