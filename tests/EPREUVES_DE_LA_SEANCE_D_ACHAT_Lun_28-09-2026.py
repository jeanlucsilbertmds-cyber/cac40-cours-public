#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_SEANCE_D_ACHAT — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : garder au dépôt la réparation du défaut 4 de A-491 (R-608 : la séance d'achat compte), et prouver que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche le juge des stratégies, la clôture des positions, ou la lecture de l'horizon (R-755 ②).

À QUOI ÇA SERT. Jean-Luc a décidé le 27-09-2026 à 19h40 (R-608) que l'objectif et la vente forcée
se surveillent dès la séance où la position est achetée. Le programme du soir (`cloturer`) et le juge des stratégies
(`jouer`) ne les testaient qu'à partir du lendemain. Le tableau de référence des 100 trades,
lui, les teste dès l'achat : 9 sorties sur 100 tombent ce jour-là (Vinci le 07-06-2024 à la vente
forcée, Airbus le 11-10-2024 à l'objectif). Avant la réparation, le juge des stratégies retrouvait 97 familles de
sortie sur 100 et 91 dates sur 100 ; après, 100 et 100.

CE QUI TOURNE CHAQUE SOIR, SANS CE FICHIER : le calibrage du programme du soir rejoue Vinci, Airbus et
le cas des deux seuils touchés le jour de l'achat (R-602) ; le juge des stratégies, à chaque lancement, compare
chacune de ses 100 sorties de calibrage au tableau de référence, famille et date, et s'arrête sinon.
Ce fichier éprouve en plus le circuit de bout en bout, la lecture unique de l'horizon, et PROUVE QUE
CHAQUE ÉPREUVE A DES DENTS : chaque sabotage retire une protection, et au moins une épreuve rougit (R-731).

USAGE : python3 tests/EPREUVES_DE_LA_SEANCE_D_ACHAT_Lun_28-09-2026.py <racine du dépôt> [--saboter | nom]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Chaque épreuve travaille sur une COPIE temporaire ; le dépôt n'est jamais touché. Simulation uniquement.
"""
import csv, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
TEN, BAN, COM = "programmes/TENIR_LES_POSITIONS.py", "programmes/JUGE_DES_STRATEGIES.py", "programmes/COMMUN.py"

SABOTAGES = {
    "Z0": [],
    "S1_circuit_saute_la_seance_d_achat": [(TEN, 'apres = sorted((b for b in s if b["date"] >= d_ent),',
                                            'apres = sorted((b for b in s if b["date"] > d_ent),')],
    "S2_banc_saute_la_seance_d_achat": [(BAN, "            suite = s[i + 1:i + 2 + h]", "            suite = s[i + 2:i + 2 + h]")],
    "S3_banc_n_exige_plus_les_sorties": [(BAN, "        ok = ok and _ok_t\n", "        ok = ok\n")],
    "S4_banc_relit_l_horizon_a_sa_facon": [(BAN, '    if "horizon" not in manq and lire_horizon(fiche.get("horizon")) is None:',
                                            '    if "horizon" not in manq and not str(fiche.get("horizon")).strip().lstrip("-").isdigit():')],
    "S5_circuit_recopie_lire_horizon": [(TEN, "from COMMUN import lire_horizon                 # la seule lecture d'un horizon (R-708)",
                                         "lire_horizon = lambda x: (lambda h: int(h) if h.isdecimal() and int(h) > 0 else None)(str(x).strip().lower().rstrip('j'))")],
    "S6_echeance_comptee_des_l_achat": [(BAN, "                apres = suite[1:]          # l'echeance se compte APRES la seance d'achat",
                                         "                apres = suite[:-1]")],
    "S7_pas_de_second_passage_le_soir_de_l_achat": [(TEN, "    if _juste_entrees:\n", "    if False:\n")],
    "S8_banc_ne_compare_plus_les_dates": [(BAN, ' or _o.get("date_sortie") != _r["date_sortie"]:', ':')],
    "S9_banc_ne_compare_plus_les_familles": [(BAN, ' or _fam(_o["motif"]) != _fam(_r["motif"])', '')],
    "S10_banc_n_exige_plus_le_compte_du_tableau": [(BAN, "        _ok_t = not _ecarts and len(_ref) == len(ops)", "        _ok_t = not _ecarts")],
    "S12_echeance_passee_tue_au_second_passage": [(TEN, '            inc_e = inc_e + [x for x in _ip if "deja passee" in x or _k in _fermees]', '            pass')],
    "S13_repli_tu_au_second_passage": [(TEN, '            inc_e = inc_e + [x for x in _ip if "deja passee" in x or _k in _fermees]', '            inc_e = inc_e + [x for x in _ip if "deja passee" in x]')],
    "S11_hasard_saute_la_seance_d_achat": [("programmes/MODULE_JUGEMENT.py", "            for b in s[i + 1:i + 2 + horizon]:", "            for b in s[i + 2:i + 2 + horizon]:")],
}

def copie(sab):
    d = tempfile.mkdtemp(prefix="d4_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, (sab, f, a[:50]); open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d

def run(d, *args):
    r = subprocess.run([sys.executable, *args], cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def charge(d, f, n):
    sys.path.insert(0, os.path.join(d, "programmes"))
    s = importlib.util.spec_from_file_location(n + str(abs(hash(d))), os.path.join(d, f))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    sys.path.pop(0)
    return m

def epreuves(sab):
    res = []
    def dire(nom, ok, detail=""):
        res.append((nom, ok, detail))
    d = copie(sab)
    # E1 le juge des stratégies : ses 100 sorties de calibrage identiques au tableau de reference, et il juge
    c, o = run(d, BAN, d)
    dire("E1 juge des stratégies : 100/100 sorties identiques au tableau de reference", c == 0 and
         "sorties : 100/100 identiques au tableau de reference (famille et date) . OK" in o, f"code {c}")
    # E2 le calibrage du soir rejoue Vinci, Airbus et les deux seuils
    c, o = run(d, TEN, d, "--calibrage")
    dire("E2 calibrage du soir : Vinci, Airbus, deux seuils", c == 0 and all(
        re.search(re.escape(x) + r".*OK$", o, re.M) for x in (
            "Vinci 07-06-2024 : vendu le jour de l'achat", "Airbus 11-10-2024 : vendu a l'objectif le jour de l'achat",
            "deux seuils le jour de l'achat : la perte compte (R-602)",
            "achat et vente forcee le meme jour : vendu le soir meme",
            "et le jeton libere prend le signal du jour",
            "entree en retard : vendue a l'echeance le soir meme",
            "et l'echeance deja passee est dite",
            "entree en retard, horizon inconnu : le repli est dit")), f"code {c}")
    # E4 une seule lecture de l'horizon : la porte du juge des stratégies accepte « 20j » et refuse « 0 »
    #    (en sous-processus, sur la copie : un module deja charge ne doit pas repondre a sa place)
    c, o = run(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import JUGE_DES_STRATEGIES as b; "
               "f={'indicateurs':'x','univers':'DG','tp':'+4%','sl':'-2.5%','periode':'2024-01-02 -> 2026-07-10'}; "
               "print(b.porte_0(dict(f, horizon='20j'))[0], b.porte_0(dict(f, horizon='0'))[0])")
    dire("E4 porte du juge des stratégies : « 20j » lu, « 0 » refuse", o.strip().endswith("True False"), o.strip()[-40:])
    # E5 le programme du soir emploie LA fonction de COMMUN, pas une copie
    c, o = run(d, "-c", "import sys; sys.path.insert(0, 'programmes'); import TENIR_LES_POSITIONS as t, COMMUN as c; "
               "print(t.lire_horizon is c.lire_horizon)")
    dire("E5 le programme du soir importe lire_horizon de COMMUN", o.strip().endswith("True"), o.strip()[-40:])
    shutil.rmtree(d)
    # E3 de bout en bout : Vinci achete le 07-06-2024, vente forcee touchee le jour meme (vrais cours du maitre)
    d = copie(sab)
    col = ["strategie", "valeur", "date_signal", "date_entree", "prix_entree", "tp", "sl", "horizon_fin",
           "statut", "comptabilite", "regles_pre_trade", "explication"]
    with open(os.path.join(d, "donnees/claude_positions_ouvertes.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=col); w.writeheader()
        # PAR LE VRAI CHEMIN : la position attend son entree (signal Vinci du 06-06-2024), le soir
        # la fait entrer a l'ouverture du 07-06 et, la vente forcee etant touchee dans la seance,
        # la vend le soir meme (R-608).
        w.writerow(dict(strategie="C5E10-OBS-V1", valeur="VINCI", date_signal="2024-06-06", date_entree="",
                        prix_entree="EN_ATTENTE", tp="EN_ATTENTE", sl="EN_ATTENTE", horizon_fin="EN_ATTENTE",
                        statut="EN_ATTENTE_ENTREE", comptabilite="jetons_illimites", regles_pre_trade="", explication="epreuve"))
    c, o = run(d, TEN, d)
    j = list(csv.DictReader(open(os.path.join(d, "donnees/claude_journal_trades.csv"), encoding="utf-8-sig")))
    v = [x for x in j if x["valeur"] == "VINCI"]
    dire("E3 de bout en bout : Vinci vendu le 07-06-2024 a 110,76", c == 0 and len(v) == 1
         and (v[0]["date_sortie"], v[0]["motif_sortie"], round(float(v[0]["prix_sortie"]), 2)) == ("2024-06-07", "SL", 110.76),
         f"code {c} · {[(x['date_sortie'], x['motif_sortie'], x['prix_sortie']) for x in v]}")
    shutil.rmtree(d)
    # E6 le juge des stratégies S'ARRETE si ses sorties s'ecartent du tableau : on remet le defaut, il doit refuser
    d = copie(sab)
    p = os.path.join(d, BAN); t = open(p, encoding="utf-8").read()
    t = t.replace("            suite = s[i + 1:i + 2 + h]", "            suite = s[i + 2:i + 2 + h]")
    open(p, "w", encoding="utf-8").write(t)
    c, o = run(d, BAN, d)
    dire("E6 defaut remis dans le juge des stratégies : il s'arrete", c == 1 and "ARRET TOTAL" in o, f"code {c}")
    shutil.rmtree(d)
    # E7/E8/E9 chaque critere du juge des stratégies a ses dents : une seule ligne du tableau de reference
    # alteree (date, famille) ou retiree -> le juge des stratégies doit s'arreter
    import glob as _g
    for nom, alterer in (("E7 une date alteree au tableau : le juge des stratégies s'arrete", lambda r: dict(r, date_sortie="2099-01-01")),
                         ("E8 une famille alteree au tableau : le juge des stratégies s'arrete", lambda r: dict(r, motif={"TP": "SL"}.get(r["motif"], "TP"))),
                         ("E9 une ligne de trop au tableau : le juge des stratégies s'arrete", "ajout")):
        d = copie(sab)
        f = _g.glob(os.path.join(d, "donnees", "TABLEAU_100_TRADES_C5E10_*.csv"))[0]
        with open(f, encoding="utf-8-sig", newline="") as fh:
            lignes = list(csv.DictReader(fh, delimiter=";")); champs = list(lignes[0].keys())
        lignes = (lignes + [dict(lignes[0], date_signal="2099-01-01")]) if alterer == "ajout" \
            else [alterer(lignes[0])] + lignes[1:]
        with open(f, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=champs, delimiter=";"); w.writeheader(); w.writerows(lignes)
        c, o = run(d, BAN, d)
        dire(nom, c == 1 and "ARRET TOTAL" in o, f"code {c}")
        shutil.rmtree(d)
    # E10 le hasard de reference joue la meme mecanique : seance d'achat qui touche la vente
    # forcee, lendemain qui saute au-dessus de l'objectif -> avec R-608, 0 % de gagnants
    d = copie(sab)
    code = ("import sys; sys.path.insert(0, 'programmes'); import MODULE_JUGEMENT as j, MODULE_POSITIONS as p\n"
            "s = []\n"
            "for k in range(90):\n"
            "    d = '2025-%02d-%02d' % (1 + k // 28, 1 + k % 28)\n"
            "    s.append(dict(date=d, open=100.0, high=100.5, low=90.0, close=95.0) if k % 3 == 1 else "
            "dict(date=d, open=110.0, high=111.0, low=109.0, close=110.0) if k % 3 == 2 else "
            "dict(date=d, open=100.0, high=100.5, low=99.5, close=100.0))\n"
            "ops = [{'valeur': 'A', 'date_signal': s[k]['date']} for k in range(0, 60, 3)]\n"
            "print(j.etalon_hasard(ops, {'A': s}, ['A'], 0.04, 0.025, 20, p, mode='valeur', n_tirages=3).get('taux_median'))\n")
    c, o = run(d, "-c", code)
    dire("E10 le hasard de reference teste la seance d'achat", c == 0 and (o.strip().splitlines() or [""])[-1] == "0.0", o.strip()[-30:])
    shutil.rmtree(d)
    return res

_choix = (list(SABOTAGES) if "--saboter" in sys.argv else [_args[1]] if len(_args) > 1 else ["Z0"])
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
