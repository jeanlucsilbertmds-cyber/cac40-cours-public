#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_QUI_TOUCHE_CE_FICHIER — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que programmes/QUI_TOUCHE_CE_FICHIER.py trouve tous ceux qui nomment un fichier, s'arrête sur un nom inconnu ou ambigu, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/QUI_TOUCHE_CE_FICHIER.py, ou les fonctions
lister, cles_de, lecteurs et ce_qu_il_appelle de programmes/FABRIQUER_LE_SOCLE.py (R-755 ②).

À QUOI ÇA SERT. R-755 ① demande, avant d'écrire du code, la liste de tout ce qui touche les fichiers
modifiés. Le 27-09-2026, le radar (programmes/audit_ecosysteme.py), lecteur du journal des trades, avait
été oublié. programmes/QUI_TOUCHE_CE_FICHIER.py fait cette liste. Ce fichier la confronte à une mesure
INDÉPENDANTE — une simple recherche du texte « journal_trades » dans le périmètre — et à un cas réel de
recherche par motif : le radar cherche « PROMPT_BOUCLE » pour etudes/PROMPT_BOUCLE_v4_Jeu_13-08-2026_14h39.md
(cassure relevée par Cowork le 13-09-2026).

USAGE : python3 tests/EPREUVES_DE_QUI_TOUCHE_CE_FICHIER_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est tout vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Chaque épreuve travaille sur une COPIE temporaire ; le dépôt n'est jamais touché.
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
QT = "programmes/QUI_TOUCHE_CE_FICHIER.py"
PERIMETRE = ("programmes/", "tests/", ".github/workflows/", "prompts_taches/")

SABOTAGES = {
    "Z0": [],
    "S1_sans_la_recherche_par_motif": [(QT, "        motifs = {m for m in fichiers if SOCLE.lecteurs({m.lower(): {p}}, cible)}",
                                        "        motifs = set()")],
    "S2_sans_la_partie_indirecte": [(QT, "        if via:\n", "        if False:\n")],
    "S3_nom_inconnu_rend_zero": [(QT, "        print(f\"ARRÊT — {msg}. Rien n'a été cherché.\")\n        sys.exit(2)",
                                  "        print(f\"ARRÊT — {msg}. Rien n'a été cherché.\")\n        sys.exit(0)")],
    "S4_nom_ambigu_prend_le_premier": [(QT, "    if len(tous) == 1:", "    if tous:")],
    "S5_fichier_illisible_saute": [(QT, "            raise Illisible(f\"{p} : {type(e).__name__} {e}\")", "            continue")],
    "S6_seul_le_nom_complet_cherche": [(QT, "        lignes = [i for i, m in enumerate(mots_de[p], 1) if designe(m, cles, module, noms)]",
                                        "        lignes = [i for i, m in enumerate(mots_de[p], 1) if os.path.basename(cible).lower() in m]")],
    "S7_partie_3_limitee_aux_programmes": [(QT, "    for p, lignes_de_mots in mots_de.items():",
                                            "    for p, lignes_de_mots in [x for x in mots_de.items() if x[0].endswith('.py')]:")],
    "S8_nom_suivi_d_un_attribut_rate": [(QT, "    if module:\n        tete = module", "    if False:\n        tete = module")],
    "S11_meme_radical_pris_pour_la_cible": [(QT, "        return any(m.startswith(tete) and m not in noms for m in mots_vus)",
                                             "        return any(m.startswith(tete) for m in mots_vus)")],
    "S12_attribut_suppose_pour_tout_fichier": [(QT, '    return nom[:-3].lower() if nom.endswith(".py") else None',
                                                "    return os.path.splitext(nom)[0].lower()")],
    "S13_lien_symbolique_resolu": [(QT, "    vrai = os.path.join(os.path.realpath(os.path.dirname(brut)), os.path.basename(brut))",
                                    "    vrai = os.path.realpath(brut)")],
    "S14_racine_par_lien_non_resolue": [(QT, "    rac = os.path.realpath(racine)", "    rac = os.path.normpath(os.path.abspath(racine))")],
    "S9_chemin_hors_du_depot_accepte": [(QT, "        if not vrai.startswith(rac + os.sep):", "        if False:")],
    "S10_chemin_absolu_garde_tel_quel": [(QT, '            return os.path.relpath(vrai, rac), ""', '            return vrai, ""')],
}


def copie(sab):
    d = tempfile.mkdtemp(prefix="qt_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, (sab, f, a[:50])
        with open(p, "w", encoding="utf-8") as h:
            h.write(t.replace(a, b))
    return d


def lancer(d, *args):
    r = subprocess.run([sys.executable, os.path.join(d, QT), d, *args],
                       capture_output=True, text=True, errors="replace", timeout=300)
    return r.returncode, r.stdout + r.stderr


def parties(sortie):
    """Rend {1: chemins, 2: chemins, 3: chemins} lus dans l'affichage."""
    res, cur = {1: set(), 2: set(), 3: set()}, None
    for l in sortie.split("\n"):
        if l.startswith("①"): cur = 1
        elif l.startswith("②"): cur = 2
        elif l.startswith("③"): cur = 3
        elif l.startswith("NE VOIT PAS"): cur = None
        elif cur and l.startswith("   ") and l.strip():
            res[cur].add(l.split()[0])
    return res


def epreuves(sab):
    d = copie(sab)
    res = []
    def dire(nom, ok, det=""):
        res.append((nom, ok, det))
    # E1 — mesure indépendante : tout fichier du périmètre dont le texte contient « journal_trades »
    attendu = set()
    for rac, sd, fs in os.walk(d):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail", "node_modules")]
        for f in fs:
            rel = os.path.relpath(os.path.join(rac, f), d)
            if rel.startswith(PERIMETRE):
                if "journal_trades" in open(os.path.join(rac, f), encoding="utf-8", errors="replace").read().lower():
                    attendu.add(rel)
    c, o = lancer(d, "donnees/claude_journal_trades.csv")
    vu = parties(o)
    dire("E1 journal des trades : partie ① = recherche du texte", c == 0 and vu[1] == attendu and len(attendu) >= 10,
         "code %d · manquent %s · en trop %s" % (c, sorted(attendu - vu[1])[:3], sorted(vu[1] - attendu)[:3]))
    # E2 — cas réel par motif
    c, o = lancer(d, "PROMPT_BOUCLE_v4_Jeu_13-08-2026_14h39.md")
    dire("E2 le radar cherche PROMPT_BOUCLE : trouvé en partie ②", c == 0 and "programmes/audit_ecosysteme.py" in parties(o)[2],
         "code %d" % c)
    # E3 — un niveau d'import
    dire("E3 JUGE_DES_STRATEGIES atteint le journal par MODULE_POSITIONS : partie ③",
         "programmes/JUGE_DES_STRATEGIES.py" in vu[3], "partie ③ : %d fichiers" % len(vu[3]))
    # E4 — nom inconnu
    c, o = lancer(d, "inexistant_28-09.csv")
    dire("E4 nom inconnu : code 2, rien cherché", c == 2 and "Rien n'a été cherché" in o, "code %d" % c)
    # E5 — nom ambigu
    os.makedirs(os.path.join(d, "donnees", "doublon"), exist_ok=True)
    shutil.copy(os.path.join(d, "donnees", "claude_journal_trades.csv"), os.path.join(d, "donnees", "doublon"))
    c, o = lancer(d, "claude_journal_trades.csv")
    dire("E5 nom porté par deux fichiers : code 2", c == 2 and "désigne 2 fichiers" in o, "code %d" % c)
    shutil.rmtree(os.path.join(d, "donnees", "doublon"))
    # E6 — fichier illisible dans le périmètre
    os.symlink(os.path.join(d, "n_existe_pas.py"), os.path.join(d, "programmes", "lien_mort.py"))
    c, o = lancer(d, "donnees/claude_journal_trades.csv")
    dire("E6 fichier du périmètre illisible : code 3", c == 3 and "lien_mort.py" in o, "code %d" % c)
    os.remove(os.path.join(d, "programmes", "lien_mort.py"))   # les épreuves suivantes veulent un périmètre lisible
    # E7 — une tâche du soir lance un programme qui nomme la cible (relecteur, 28-09-2026)
    c, o = lancer(d, "programmes/MODULE_POSITIONS.py")
    vp = parties(o)
    dire("E7 collecte_abc.yml lance TENIR_LES_POSITIONS : partie ③", c == 0 and ".github/workflows/collecte_abc.yml" in vp[3],
         "code %d" % c)
    # E8 — un nom suivi d'un attribut : MODULE_POSITIONS.FRAIS_TAUX (relecteur, 28-09-2026)
    dire("E8 MODULE_STATISTIQUES écrit MODULE_POSITIONS.FRAIS_TAUX : partie ①",
         "programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py" in vp[1], "partie ① : %d" % len(vp[1]))
    # E9 — un fichier existant hors du dépôt
    dehors = tempfile.mkdtemp(prefix="dehors_")
    open(os.path.join(dehors, "g.txt"), "w").write("x\n")
    c, o = lancer(d, os.path.join(dehors, "g.txt"))
    dire("E9 fichier hors du dépôt : code 2", c == 2 and "hors du dépôt" in o, "code %d" % c)
    shutil.rmtree(dehors, ignore_errors=True)
    # E10 — la cible donnée par son chemin absolu ne se liste pas elle-même
    c, o = lancer(d, os.path.join(d, "programmes", "MODULE_POSITIONS.py"))
    va = parties(o)
    dire("E10 chemin absolu : même partie ① que le chemin relatif, sans la cible",
         c == 0 and va[1] == vp[1] and "programmes/MODULE_POSITIONS.py" not in va[1], "code %d" % c)
    # E11 — même radical, autre fichier : le rapport du radar n'est pas le radar (relecteur, tour 2)
    attendu = set()
    for rac, sd, fs in os.walk(d):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail", "node_modules")]
        for f in fs:
            rel = os.path.relpath(os.path.join(rac, f), d)
            if rel.startswith(PERIMETRE) and "audit_ecosysteme.md" in open(os.path.join(rac, f), encoding="utf-8", errors="replace").read().lower():
                attendu.add(rel)
    c, o = lancer(d, "rapports/AUDIT_ECOSYSTEME.md")
    v11 = parties(o)[1]
    dire("E11 AUDIT_ECOSYSTEME.md : partie ① = recherche du texte", c == 0 and v11 == attendu and len(attendu) >= 2,
         "code %d · en trop %d · manquent %s" % (c, len(v11 - attendu), sorted(attendu - v11)[:2]))
    # E14 — sens inverse : nommer le rapport n'est pas nommer le programme (relecteur, tour 2)
    with open(os.path.join(d, "programmes", "LIT_RAPPORT.py"), "w", encoding="utf-8") as h:
        h.write('R = "rapports/AUDIT_ECOSYSTEME.md"\n')
    c, o = lancer(d, "programmes/audit_ecosysteme.py")
    dire("E14 « AUDIT_ECOSYSTEME.md » ne désigne pas audit_ecosysteme.py", c == 0 and "programmes/LIT_RAPPORT.py" not in parties(o)[1]
         and "programmes/TESTS_AUDIT.py" in parties(o)[1], "code %d" % c)
    os.remove(os.path.join(d, "programmes", "LIT_RAPPORT.py"))
    # E12 — une copie « .bak » d'une donnée ne désigne pas la donnée (cas fabriqué du relecteur, tour 2)
    with open(os.path.join(d, "programmes", "LIT_BAK.py"), "w", encoding="utf-8") as h:
        h.write('B = "claude_journal_trades.csv.bak"\n')
    c, o = lancer(d, "donnees/claude_journal_trades.csv")
    dire("E12 « claude_journal_trades.csv.bak » ne désigne pas le journal", c == 0 and "programmes/LIT_BAK.py" not in parties(o)[1],
         "code %d" % c)
    os.remove(os.path.join(d, "programmes", "LIT_BAK.py"))
    # E13 — un lien symbolique est un fichier de l'arbre sous son propre nom (relecteur, tour 2)
    os.symlink("claude_journal_trades.csv", os.path.join(d, "donnees", "alias_trades.csv"))
    with open(os.path.join(d, "programmes", "LIT_ALIAS.py"), "w", encoding="utf-8") as h:
        h.write('A = "alias_trades.csv"\n')
    c, o = lancer(d, "donnees/alias_trades.csv")
    dire("E13 lien symbolique : cherché sous son propre nom", c == 0 and "QUI TOUCHE donnees/alias_trades.csv" in o
         and "programmes/LIT_ALIAS.py" in parties(o)[1], "code %d" % c)
    # E15 — racine atteinte par un lien, cible par son vrai chemin (relecteur, tour 3)
    lien = d.rstrip("/") + "_lien"
    os.symlink(d, lien)
    r = subprocess.run([sys.executable, os.path.join(d, QT), lien, os.path.join(d, "donnees", "claude_journal_trades.csv")],
                       capture_output=True, text=True, errors="replace", timeout=300)
    dire("E15 racine par un lien, cible par son vrai chemin : trouvée", r.returncode == 0
         and "QUI TOUCHE donnees/claude_journal_trades.csv" in r.stdout, "code %d" % r.returncode)
    os.remove(lien)
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
