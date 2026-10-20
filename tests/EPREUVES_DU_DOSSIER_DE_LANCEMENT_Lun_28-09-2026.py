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
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve PAR UN VERDICT du programme
éprouvé, sans plantage ; 1 sinon ; 2 si une ancre de sabotage ne se trouve pas exactement une fois.
Durée : mesurée par le relecteur le 28-09-2026, 16 s pour Z0 et 46 s avec --saboter, avec trois variantes ; elle a
crû depuis avec le jeu d'épreuves du garde-fou — la mesure du jour est au relevé
tests/resultats/DUREE_DE_L_EPREUVE_DU_DOSSIER_DE_LANCEMENT_Sam_17-10-2026.txt.
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
EGF = "programmes/EPREUVES_DU_GARDE_FOU.py"
# Le lanceur unique des cas, `lancer_un_cas` (17-10-2026) : c'est lui qui pose le dossier de lancement, pour
# `jouer` comme pour le sabotage du programme.
_SAB = ('                       capture_output=True, text=True, errors="replace",\n'
        '                       cwd=dossier_neutre())')
SABOTAGES = {
    "Z0": [],
    # le sabotage retire le dossier neutre du lanceur unique, donc pour `jouer` comme pour la relance contre la
    # copie sabotée
    "S1_sabotage_relance_depuis_le_dossier_courant": [(EGF, _SAB,
        '                       capture_output=True, text=True, errors="replace")')],
    # le dossier neutre existe, mais vide : aucun des deux scripts cités n'y est posé
    "S2_dossier_neutre_sans_ses_scripts": [(EGF, "        for nom, source in SCRIPTS_CITES.items():",
                                            "        for nom, source in {}.items():")],
    # le lanceur unique des cas oublie les arguments du montage — le défaut qui a rendu aveugle le sabotage du
    # programme du 16 au 17-10-2026 (superviseur, R-759) : les épreuves du garde-fou doivent rougir
    "S3_lanceur_sans_les_arguments_du_montage": [(EGF,
        '    r = subprocess.run([sys.executable, garde, p] + list((montage or {}).get("arguments", [])),',
        '    r = subprocess.run([sys.executable, garde, p],')],
    # le corps unique du sabotage du programme relance les cas sans leur montage : `jouer` ne passe pas par lui ;
    # c'est le témoin (la copie intacte) qui doit arrêter la mesure — « MESURE AVEUGLE », code 2 (superviseur,
    # R-759, 17-10-2026, 23h : prouve que le témoin a des dents)
    "S4_corps_du_sabotage_sans_le_montage": [(EGF,
        "        if lancer_un_cas(garde, cas[1], *cas[4:6]).returncode == 0:",
        "        if lancer_un_cas(garde, cas[1], *cas[4:5]).returncode == 0:")],
}

# Un sabotage ne mord que s'il fait rougir l'épreuve PAR UN VERDICT de son programme principal, sans trace
# d'exception (superviseur, R-759, 17-10-2026, 23h) : le 17-10-2026 à 22h49, S3 « mordait » par un NameError —
# un plantage, que l'ancienne règle comptait comme un sabotage vu.
VERDICTS_ROUGES = ("LE JEU D ÉPREUVES NE COUVRE PAS LE GARDE-FOU", "LE SABOTAGE DU PROGRAMME N A PAS PU MESURER")


def _ancres_introuvables(choix):
    """Rend, pour les sabotages choisis, les ancres qui ne se trouvent pas exactement une fois — avant tout lancement."""
    fautes = []
    for sab in choix:
        for f, a, _b in SABOTAGES[sab]:
            n = open(os.path.join(DEPOT, f), encoding="utf-8").read().count(a)
            if n != 1:
                fautes.append(f"{sab} · {f} · trouvée {n} fois · {a.strip()[:60]}")
    return fautes


def copie(sab):
    d = tempfile.mkdtemp(prefix="lanc_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            shutil.rmtree(d, ignore_errors=True)
            print(f"ARRÊT — ancre de {sab} trouvée {t.count(a)} fois dans {f} (code 2)")
            sys.exit(2)
        with open(p, "w", encoding="utf-8") as h:
            h.write(t.replace(a, b))
    return d


def epreuves(sab):
    d = copie(sab)
    res = []
    # E2 : un dossier vide, jamais la racine du disque — sans dossier neutre, le garde-fou
    # recopierait le dossier courant entier pour y rejouer les commandes citées.
    vide = tempfile.mkdtemp(prefix="vide_")
    for nom, ou in (("E1 lancées depuis programmes/", os.path.join(d, "programmes")),
                    ("E2 lancées depuis un dossier vide", vide)):
        r = subprocess.run([sys.executable, os.path.join(d, EGF)], cwd=ou,
                           capture_output=True, text=True, errors="replace", timeout=1800)
        sortie = r.stdout + r.stderr
        plante = "Traceback" in sortie
        if r.returncode == 0 and not plante and "AUCUNE ÉPREUVE NE LE VOIT" not in sortie:
            etat = "vert"
        elif r.returncode != 0 and not plante and any(v in sortie for v in VERDICTS_ROUGES):
            etat = "rouge"
        else:
            etat = "plantage"
        res.append((nom, etat, "code %d · %s" % (r.returncode, sortie.strip().splitlines()[-1][:70]
                                                if sortie.strip() else "(rien)")))
    shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(vide, ignore_errors=True)
    return res


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_introuvables = _ancres_introuvables(_choix)
if _introuvables:
    for x in _introuvables:
        print("ANCRE INTROUVABLE —", x)
    print("VERDICT : ARRÊT — rien n'a été éprouvé (code 2)")
    sys.exit(2)
_faute = False
for sab in _choix:
    r = epreuves(sab)
    vertes = [x for x in r if x[1] == "vert"]
    rouges = [x for x in r if x[1] == "rouge"]
    plantes = [x for x in r if x[1] == "plantage"]
    vert = sab == "Z0"
    print(f"== {sab} : {len(vertes)} vertes, {len(rouges)} rouges, {len(plantes)} plantages" + (
        "  <-- PLANTAGE : NE COMPTE PAS" if plantes else
        "  <-- ATTENDU : 0 rouge" if vert and rouges else "  <-- SABOTAGE NON VU" if not vert and not rouges else ""))
    for nom, etat, det in r:
        if etat != "vert":
            print(f"     {etat.upper()} {nom} · {det}")
    _faute = _faute or bool(plantes) or (vert and bool(rouges)) or (not vert and not rouges)
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
