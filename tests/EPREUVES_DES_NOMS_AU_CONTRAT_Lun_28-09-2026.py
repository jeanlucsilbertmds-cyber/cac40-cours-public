#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_NOMS_AU_CONTRAT — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que le radar, le programme du soir et le versement de l'historique lisent au contrat ce qu'ils recopiaient (R-708), et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche noms_d_une_strategie ou COURS_MAITRE dans
programmes/CONTRATS_DES_FICHIERS.py, le maillon 17 du radar, reglages_du_registre dans
programmes/TENIR_LES_POSITIONS.py, ou COLONNES dans programmes/TENIR_L_HISTORIQUE.py (R-755 ②).

À QUOI ÇA SERT. « Deux implémentations d'une même chose divergent toujours » (R-708). Le 28-09-2026,
trois programmes recopiaient ce que le contrat déclare : le radar (maillon 17, trois fois) et le
programme du soir recopiaient la règle « l'identifiant, et le nom avant la parenthèse » de
noms_d_une_strategie ; le versement de l'historique recopiait les huit colonnes de COURS_MAITRE.
Aujourd'hui les copies sont identiques à l'original — mesuré : radar, programme du soir et versement
rendent la même sortie avant et après. Ces épreuves prouvent donc autre chose : QU'UN CHANGEMENT DU
CONTRAT ARRIVE JUSQU'À EUX. Chacune modifie le contrat dans une copie et regarde si le programme suit.

USAGE : python3 tests/EPREUVES_DES_NOMS_AU_CONTRAT_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Chaque épreuve travaille sur une COPIE temporaire ; le dépôt n'est jamais touché.
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
RAD, TEN, HIS, CON = ("programmes/audit_ecosysteme.py", "programmes/TENIR_LES_POSITIONS.py",
                      "programmes/TENIR_L_HISTORIQUE.py", "programmes/CONTRATS_DES_FICHIERS.py")
ENTETE = "strategie,valeur,date_signal,date_entree,prix_entree,tp,sl,horizon_fin,statut,comptabilite,regles_pre_trade,explication\n"

SABOTAGES = {
    "Z0": [],
    "S1_colonnes_recopiees": [(HIS, "COLONNES = list(COURS_MAITRE)",
                               'COLONNES = ["valeur", "date", "open", "high", "low", "close", "volume", "source"]')],
    "S2_radar_recopie_les_noms": [(RAD, "    _noms = set().union(*(_noms_17(s) for s in _strats))",
                                   '    _noms = {(s.get("nom") or "").split(" (")[0].strip() for s in _strats} | '
                                   '{(s.get("id") or "").strip() for s in _strats}')],
    "S3_soir_recopie_les_noms": [(TEN, "                for k in sorted(noms_d_une_strategie(x)):",
                                  '                for k in ((x.get("id") or "").strip(), (x.get("nom") or "").split(" (")[0].strip()):')],
    "S4_radar_sans_repli": [(RAD, "        def _noms_17(s):\n", "        def _pas_de_repli(s):\n")],
    "S6_univers_recopie_la_regle": [(RAD, "            for _cle in (_noms_17(s) if _u else ()):",
                                     '            for _cle in (({(s.get("id") or "").strip(), (s.get("nom") or "").split(" (")[0].strip()} - {""}) if _u else ()):')],
    "S5_univers_lu_sous_le_nom_seul": [(RAD, "            for _cle in (_noms_17(s) if _u else ()):",
                                        '            for _cle in ([(s.get("nom") or "").split(" (")[0].strip()] if _u else ()):')],
}


def copie(sab):
    d = tempfile.mkdtemp(prefix="noms_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        remplacer(d, f, a, b)
    return d


def remplacer(d, f, a, b):
    p = os.path.join(d, f)
    t = open(p, encoding="utf-8").read()
    assert t.count(a) == 1, (f, a[:60])
    with open(p, "w", encoding="utf-8") as h:
        h.write(t.replace(a, b))


def lancer(d, *args):
    r = subprocess.run([sys.executable, *args], cwd=d, capture_output=True, text=True,
                       errors="replace", timeout=900)
    return r.returncode, r.stdout + r.stderr


# le contrat, modifié dans la copie : un nom de plus pour chaque stratégie
_NOMS_AVANT = '    return {(ligne_du_registre.get("id") or "").strip(),'
_NOMS_APRES = '    return {"ALIAS_EPREUVE", (ligne_du_registre.get("id") or "").strip(),'


def epreuves(sab):
    res = []
    def dire(nom, ok, det=""):
        res.append((nom, ok, det))
    # E1 — une colonne ajoutée au contrat arrive aux colonnes du versement
    d = copie(sab)
    remplacer(d, CON, '    "low", "close", "volume", "source",\n]', '    "low", "close", "volume", "source", "colonne_epreuve",\n]')
    c, o = lancer(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import TENIR_L_HISTORIQUE as H; print(H.COLONNES)")
    dire("E1 une colonne ajoutée au contrat arrive au versement", c == 0 and "colonne_epreuve" in o, o.strip()[-80:])
    shutil.rmtree(d, ignore_errors=True)
    # E2, E3 — un nom ajouté par le contrat arrive au radar et au programme du soir
    d = copie(sab)
    remplacer(d, CON, _NOMS_AVANT, _NOMS_APRES)
    with open(os.path.join(d, "donnees", "claude_positions_ouvertes.csv"), "w", encoding="utf-8") as h:
        h.write(ENTETE + "ALIAS_EPREUVE,VINCI,2026-09-25,2026-09-26,100,104,97.5,2026-10-20,OUVERTE,un_jeton,,\n")
    c, o = lancer(d, RAD, ".")
    dire("E2 radar : une position sous un nom du contrat a sa fiche",
         "17-Registre" in o and "STRATÉGIE SANS FICHE" not in o, "code %d" % c)
    # E6 — le contrôle de l'univers suit lui aussi le contrat (relecteur, 28-09-2026 : sans E6,
    # une copie de la règle dans la clé de l'univers ne faisait rougir aucune épreuve)
    with open(os.path.join(d, "donnees", "claude_positions_ouvertes.csv"), "w", encoding="utf-8") as h:
        h.write(ENTETE + "ALIAS_EPREUVE,ZZZ_HORS_UNIVERS,2026-09-25,2026-09-26,100,104,97.5,2026-10-20,OUVERTE,un_jeton,,\n")
    c6, o6 = lancer(d, RAD, ".")
    dire("E6 radar : l'univers se lit sous un nom du contrat", "ALIAS_EPREUVE joue ZZZ_HORS_UNIVERS" in o6, "code %d" % c6)
    c, o = lancer(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import TENIR_LES_POSITIONS as T; "
                           "print('ALIAS_EPREUVE' in T.reglages_du_registre('.'))")
    dire("E3 soir : les réglages se trouvent sous un nom du contrat", c == 0 and o.strip().endswith("True"), o.strip()[-60:])
    shutil.rmtree(d, ignore_errors=True)
    # E4 — contrat illisible : le radar le dit et le maillon 17 tourne quand même (A-250)
    d = copie(sab)
    p = os.path.join(d, CON)
    t = open(p, encoding="utf-8").read()
    with open(p, "w", encoding="utf-8") as h:
        h.write('raise RuntimeError("contrat casse pour l epreuve")\n' + t)
    c, o = lancer(d, RAD, ".")
    dire("E4 contrat illisible : repli dit, maillon 17 présent",
         "lus par le repli du radar" in o and o.count("17-Registre") >= 3, "code %d · 17-Registre %d fois" % (c, o.count("17-Registre")))
    shutil.rmtree(d, ignore_errors=True)
    # E5 — une position écrite sous l'IDENTIFIANT est contrôlée contre l'univers
    d = copie(sab)
    with open(os.path.join(d, "donnees", "claude_positions_ouvertes.csv"), "w", encoding="utf-8") as h:
        h.write(ENTETE + "C5E10-QA-V1,LVMH,2026-09-25,2026-09-26,600,624,585,2026-10-20,OUVERTE,un_jeton,,\n")
    c, o = lancer(d, RAD, ".")
    dire("E5 position sous l'identifiant, valeur hors univers : dénoncée", "VALEUR HORS UNIVERS DÉCLARÉ : C5E10-QA-V1 joue LVMH" in o,
         "code %d" % c)
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
