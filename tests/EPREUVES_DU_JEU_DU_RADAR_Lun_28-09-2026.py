#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_JEU_DU_RADAR — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que programmes/TESTS_AUDIT.py, le jeu d'épreuves du radar, est de nouveau vert, et que dix de ses onze cas rougissent quand on retire au radar ce qu'ils surveillent.
Quand l'appeler : avant toute livraison qui touche programmes/TESTS_AUDIT.py ou le maillon 18 de
programmes/audit_ecosysteme.py (R-755 ②).

À QUOI ÇA SERT. Depuis le 12-09-2026, programmes/TESTS_AUDIT.py rendait « 4 CAS SUR 11 TOMBENT.
NE RIEN DEPOSER. » sans qu'aucun défaut du radar soit en cause (A-435 ②, mesuré le 19-09-2026, et
encore le 28-09-2026 sur origin/main) : trois cas lançaient une copie modifiée du radar posée seule
dans le dossier temporaire, qui ne trouvait plus programmes/COMMUN.py ; le quatrième écrivait son
historique fabriqué au premier niveau de la copie, à côté du vrai rangé dans donnees/. Réparé le
28-09-2026 : la copie emporte ses programmes voisins, l'historique fabriqué remplace le vrai.
Un jeu d'épreuves rouge pour des raisons qui lui sont propres cesse d'être consulté.

CE FICHIER lance le vrai programmes/TESTS_AUDIT.py sur une COPIE du dépôt (Z0 : 11 cas passent, code 0),
puis sur des copies dont le radar est saboté à l'endroit que surveille chacun des quatre cas réparés
(SA1 à SA11), et sur des copies dont la réparation est retirée (SH1, SH2). La troisième réparation —
la date portée par le NOM des traces, que _dater laissait — ne se sabote pas seule : sans elle le cas
« dimanche » reste vert, radar juste ou faux. Sa preuve est SA2 : mesuré le 28-09-2026 avant elle,
« SA2_week_end_compte_comme_ouvre : ÉCHEC (son cas tombe) · code 0 » ; après elle, le cas tombe. Chaque sabotage doit faire
tomber le cas qui lui correspond (R-731).

USAGE : python3 tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et que chaque sabotage fait tomber son cas ; 1 sinon.
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
RAD, TA = "programmes/audit_ecosysteme.py", "programmes/TESTS_AUDIT.py"

# chaque sabotage : (fichier, avant, après, cas qui doit tomber)
SABOTAGES = {
    "Z0": [],
    # Z1 : sans aucune vraie trace de l'audit du soir — le soir où le circuit est cassé
    # (A-441) — les onze cas passent encore : ils fabriquent leurs traces (relecteur, tour 2)
    "Z1_sans_trace_reelle_de_l_audit": [("rapports/audit_du_jour.md", None, None, None),
                                        ("archives/claude_audit_du_jour_PERIME_12-09-2026.md", None, None, None)],
    "SA1_tableau_lu_comme_un_document": [(RAD, '            _tableau = chemin.lower().endswith((".csv", ".tsv"))',
                                          "            _tableau = False", "un tableau qui s'empile")],
    "SA2_week_end_compte_comme_ouvre": [(RAD, "                if _d.weekday() < 5:", "                if True:",
                                         "dimanche")],
    "SA3_mode_inconnu_accepte": [(RAD, '        if _mode not in ("ouvré", "calendaire"):', "        if False:",
                                  "un mode inconnu")],
    "SA4_declaration_incomplete_tue": [(RAD, "            _propres.append(_decl)\n        else:",
                                        "            _propres.append(_decl)\n        elif False:", "un mode oublie")],
    "SA5_date_future_retenue": [(RAD, "        _vues = [d for d in _vues if d <= _aujourdhui]", "        _vues = list(_vues)",
                                 "une date future")],
    # SA6 à SA10 : ancres relevées par le relecteur du Chat, 28-09-2026 (A-435 disait que deux
    # cas ne pouvaient pas rougir : « sous-dossiers » et « trace RECOPIEE » ; ils le peuvent)
    "SA6_age_lu_sur_la_date_du_disque": [(RAD, "        _dates = [d for d in (_date_declaree(p) for p in _f) if d]",
                                          "        _dates = [_dt.fromtimestamp(os.path.getmtime(os.path.join(PROJ, p))).date() for p in _f]",
                                          "une trace RECOPIEE")],
    "SA7_document_date_la_plus_recente": [(RAD, "        return max(_vues) if _tableau else _vues[0]", "        return max(_vues)",
                                           "un document redige")],
    "SA8_absence_muette": [(RAD, "        if not _f:\n            check(\"18-Tâches\", False, \"\",\n                  f\"{_lib} n'a laissé AUCUNE trace",
                            "        if not _f:\n            continue\n            check(\"18-Tâches\", False, \"\",\n                  f\"{_lib} n'a laissé AUCUNE trace",
                            "une trace absente")],
    "SA9_sans_date_vaut_aujourd_hui": [(RAD, "        if not _dates:\n            check(\"18-Tâches\", False, \"\",\n                  f\"{_lib} a laissé une trace SANS DATE",
                                        "        if not _dates:\n            _dates = [_aujourdhui]\n        if False:\n            check(\"18-Tâches\", False, \"\",\n                  f\"{_lib} a laissé une trace SANS DATE",
                                        "une trace sans date")],
    "SA10_premier_niveau_seul": [(RAD, "        _sd[:] = [x for x in _sd if x not in _NON_VIVANT]   # on n'y descend même pas",
                                  "        _sd[:] = []", "les sous-dossiers")],
    # SA11 : le radar ne descend qu'à UN niveau, et les vraies traces sont datées du jour
    # (le soir après le circuit) — cassure du relecteur, tour 3
    "SA11_un_seul_niveau_un_soir_de_circuit": [
        (RAD, "        _sd[:] = [x for x in _sd if x not in _NON_VIVANT]   # on n'y descend même pas",
         "        _sd[:] = [x for x in _sd if x not in _NON_VIVANT] if _d == PROJ else []", "les sous-dossiers"),
        ("__DATER_AU_JOUR__", None, None, None)],
    "SH1_copie_modifiee_sans_ses_voisins": [(TA, '        if voisin.endswith(".py") and voisin != SCRIPT:',
                                             '        if False:', "dimanche")],
    "SH2_historique_fabrique_au_premier_niveau": [(TA, '        p = os.path.join(d, "donnees", "historique_mesures.csv")',
                                                   '        p = os.path.join(d, "historique_mesures.csv")',
                                                   "un tableau qui s'empile")],
}


def jouer(sab):
    d = tempfile.mkdtemp(prefix="jeu_radar_")
    try:
        shutil.copytree(DEPOT, os.path.join(d, "r"), ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
        r = os.path.join(d, "r")
        attendu = None
        for f, a, b, cas in SABOTAGES[sab]:
            if f == "__DATER_AU_JOUR__":  # les vraies traces prennent la date du jour
                sys.path.insert(0, os.path.join(r, "programmes"))
                import importlib.util as _iu
                _sp = _iu.spec_from_file_location("TA_copie", os.path.join(r, TA))
                _T = _iu.module_from_spec(_sp); _sp.loader.exec_module(_T)
                from datetime import datetime as _dtm
                from zoneinfo import ZoneInfo as _Z
                _j = _dtm.now(_Z("Europe/Paris")).date().isoformat()   # le jour de Paris, comme le cas
                for _m in ("rapport_boucle", "cours_nouveaux", "audit_du_jour", "historique_mesures"):
                    _T._dater(r, _m, _j)
                sys.path.pop(0)
                continue
            p = os.path.join(r, f)
            if a is None:                 # une trace à retirer, pas un sabotage
                if os.path.exists(p):
                    os.remove(p)
                continue
            t = open(p, encoding="utf-8").read()
            assert t.count(a) >= 1, (sab, a[:50])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))   # toutes les occurrences ; SH2 ne fait tomber que « un tableau qui s'empile »
            attendu = cas
        x = subprocess.run([sys.executable, "TESTS_AUDIT.py", ".."], cwd=os.path.join(r, "programmes"),
                           capture_output=True, text=True, errors="replace", timeout=1200)
        sortie = x.stdout + x.stderr
        tombes = [l for l in sortie.split("\n") if l.strip().startswith("ECHEC")]
        if sab.startswith("Z"):
            ok = x.returncode == 0 and "LES 11 CAS PASSENT" in sortie
            return ok, "code %d · %d cas tombés" % (x.returncode, len(tombes))
        ok = x.returncode == 1 and any(attendu in l for l in tombes)
        return ok, "code %d · tombés : %s" % (x.returncode, [l.strip()[6:40].strip() for l in tombes])
    finally:
        shutil.rmtree(d, ignore_errors=True)


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    ok, det = jouer(sab)
    etiquette = "vert" if sab.startswith("Z") else "son cas tombe"
    print(f"== {sab} : {'OK' if ok else 'ÉCHEC'} ({etiquette}) · {det}")
    _faute = _faute or not ok
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
