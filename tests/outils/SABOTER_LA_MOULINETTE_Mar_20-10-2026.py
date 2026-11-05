#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SABOTER_LA_MOULINETTE — Mar 20-10-2026 (Paris). Simulation uniquement.

USAGE
    python3 -B tests/outils/SABOTER_LA_MOULINETTE_Mar_20-10-2026.py <racine> <relevé>

① RÔLE — Prouver que les épreuves de la moulinette ont des dents : jouer chaque sabotage de la liste SABOTAGES sur
  une copie neuve du dépôt, lancer les DEUX épreuves que la nuit lance (`tests/EPREUVES_DE_LA_MOULINETTE_Mar_20-10-2026.py`
  et `programmes/EPREUVES_DE_LA_DECLINAISON.py`), et exiger qu'au moins l'une ROUGISSE, sauf pour le témoin de
  l'exigence du message, où les deux doivent rester VERTES (il prouve que cette exigence mord).
② CONTEXTE D'APPEL — À la main, à chaque livraison qui change la moulinette ou son épreuve (R-731).
③ ENTRÉE — Deux arguments : la racine d'un dépôt (non modifiée) et le chemin du relevé à écrire.
④ CONDITIONS D'ENTRÉE — Assez de place pour deux copies du dépôt sans .git (environ 200 Mo chacune le 20-10-2026).
⑤ SORTIE — Le relevé écrit, puis affiché : une ligne par sabotage (CONFORME ou NON CONFORME) et le bilan. Code de
  sortie 0 ; 2 sans les deux arguments.
⑥ TRAITEMENT — Voir `jouer` ; deux sabotages à la fois.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Demande du superviseur du 20-10-2026 : que les sabotages soient reproductibles et relisables par Cowork.
⑨ CE QUI CLOCHE — Le code de sortie de ce programme ne dit pas le bilan : lire la dernière ligne du relevé.
⑩ EFFET — Crée et efface des copies ; écrit le relevé.
⑪ TERMINAISON — Sort après le dernier sabotage. Un de ses appels peut-il ne pas revenir ? Non : délai de l'épreuve.
"""
import os, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(2)
DEPOT, RELEVE = os.path.abspath(sys.argv[1]), sys.argv[2]
J = "programmes/JOUER_LES_VERSIONS.py"
P = "programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py"
D = "programmes/DECLINER_LES_STRATEGIES.py"
E = "programmes/EPREUVES_DE_LA_DECLINAISON.py"
T = "tests/EPREUVES_DE_LA_MOULINETTE_Mar_20-10-2026.py"
MSG = ('return arreter("les résultats ne retrouvent pas le témoin : rien n\'est écrit")',
       'return arreter("les résultats ne retrouvent pas le témoin.")')
# (nom, [(fichier, avant, apres)], code attendu : "rouge" ou "vert")
SABOTAGES = [
    ("K1 de Cowork : la comparaison au témoin retirée", [(J, "ecarts = comparer_au_temoin(f_comb, sid, essai, vue_du_temoin if rejouer else provisoire)", "ecarts = []")], "rouge"),
    ("C15 : l'écart entre les barèmes n'est plus confronté à la taxe", [(J, "or abs(ecart - taxes) > 0.01:", "or False:")], "rouge"),
    ("C15 : le témoin n'est plus rejoué sous son barème", [(J, "rejouer = b_tem is not None and b_tem != b_res", "rejouer = False")], "rouge"),
    ("C15 : un témoin sans barème accepté", [(J, '    if len(vals) != 1 or "" in vals:', '    if False:')], "rouge"),
    ("arreter rend 0", [(J, 'print("ARRÊT : %s" % message)\n    return 1', 'print("ARRÊT : %s" % message)\n    return 0')], "rouge"),
    ("fichier de résultats existant accepté", [(J, "if os.path.exists(f_out):", "if False:")], "rouge"),
    ("identifiants en double acceptés", [(J, "if len(set(ids)) != len(ids):", "if False:")], "rouge"),
    ("marge de cours non contrôlée", [(J, "if marge[plus_court] < h_max + 1:", "if False:")], "rouge"),
    ("désaccord avec le juge seul accepté", [(J, "if texte_ref != ligne_juge:", "if False:")], "rouge"),
    ("tableau vide accepté", [(D, 'return ["le tableau est vide"]', "return []")], "rouge"),
    ("voisinage invalide accepté", [(P, "if not finis or pas <= 0 or not 0 <= n <= 10 or mini > maxi:", "if False:")], "rouge"),
    ("sabotage inapplicable compté", [(E, "if texte.count(avant) != 1:", "if False:")], "rouge"),
    ("message d'arrêt du témoin changé, épreuve intacte", [(J,) + MSG], "rouge"),
    ("M1 de Cowork : refus « ce réglage doit être jouable » neutralisé",
     [(D, 'motifs.append("ligne « %s » : ce réglage doit être jouable" % p)', '(lambda *a: None)("ligne « %s » : ce réglage doit être jouable" % p)')], "rouge"),
    ("M2 de Cowork : détail de l'écart de fusion changé",
     [(J, 'ecarts.append("%s lu %r, version %r" % (k, fusion[k], version[k]))', 'ecarts.append("%s relu %r, version %r" % (k, fusion[k], version[k]))')], "rouge"),
    ("M2 de Cowork : détail de l'écart au témoin changé",
     [(J, 'ecarts.append("%s %s : %s au lieu de %s" % (k, c, res[k].get(c), tem[k].get(c)))', 'ecarts.append("%s %s : %s et non %s" % (k, c, res[k].get(c), tem[k].get(c)))')], "rouge"),
    ("TÉMOIN DE L'EXIGENCE DU MESSAGE : même message changé, épreuve privée de l'exigence",
     [(J,) + MSG, (T, "ok = code == code_attendu and vus", "ok = code == code_attendu")], "vert"),
]


def jouer(s):
    """Joue un sabotage sur une copie neuve et rend son verdict.

    ① RÔLE — Appliquer un sabotage, lancer les deux épreuves de la nuit (celle de tests/ et celle de la déclinaison),
      comparer à l'attendu.
    ② CONTEXTE D'APPEL — Le bas de ce fichier, une fois par sabotage, deux à la fois.
    ③ ENTRÉE — `s` : (nom, liste de (fichier, texte avant, texte après), « rouge » ou « vert »).
    ④ CONDITIONS D'ENTRÉE — Chaque texte « avant » figure exactement une fois dans son fichier, sinon INAPPLICABLE.
    ⑤ SORTIE — QUATRE valeurs : le nom, l'attendu, le détail vu (codes des deux épreuves), vrai si conforme.
      [rend: 4]
    ⑥ TRAITEMENT — ① copier le dépôt sans .git · ② remplacer les textes · ③ lancer les deux épreuves · ④ effacer
      la copie · ⑤ rouge si l'une rend autre chose que 0, comparé à l'attendu.
    ⑦ UNITÉ — Deux codes de sortie, un par épreuve.
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — Un sabotage par texte : si le code change, il devient INAPPLICABLE, et le relevé le dit.
    ⑩ EFFET — Crée puis efface une copie du dépôt.
    ⑪ TERMINAISON — Rend la main ; chaque épreuve a un délai de 1 800 secondes, soit 3 600 au plus pour les deux.
      [sort: non]
    """
    nom, changements, attendu = s
    d = tempfile.mkdtemp(prefix="sabotage_moul_")
    copie = os.path.join(d, "depot")
    shutil.copytree(DEPOT, copie, ignore=shutil.ignore_patterns(".git"))
    for f, avant, apres in changements:
        p = os.path.join(copie, f)
        t = open(p, encoding="utf-8").read()
        if t.count(avant) != 1:
            shutil.rmtree(d, ignore_errors=True)
            return nom, attendu, "INAPPLICABLE (texte trouvé %d fois dans %s)" % (t.count(avant), f), False
        open(p, "w", encoding="utf-8").write(t.replace(avant, apres))
    # LES DEUX ÉPREUVES DE LA NUIT : celle de tests/ et celle de la déclinaison, que le certificateur lance à part
    # (tests/LANCEMENT_DES_EPREUVES.json). Le 20-10-2026, l'outil ne lançait que la première, et le sabotage M1,
    # que seule la seconde voit, sortait « NON CONFORME » à tort.
    r = subprocess.run([sys.executable, "-B", T, "."], cwd=copie, capture_output=True, text=True, timeout=1800)
    r2 = subprocess.run([sys.executable, "-B", E, "donnees/cac40_strategies.csv"], cwd=copie, capture_output=True,
                        text=True, timeout=1800)
    shutil.rmtree(d, ignore_errors=True)
    fin = [l for l in r.stdout.splitlines() if l.startswith(("  ÉCHEC", "CAS :", "VERDICT"))]
    fin2 = [l.strip() for l in r2.stdout.splitlines() if l.startswith(("  ÉCHEC", "VERDICT"))]
    vu = "rouge" if (r.returncode != 0 or r2.returncode != 0) else "vert"
    return nom, attendu, "tests/ code %d · déclinaison code %d · %s · %s" % (
        r.returncode, r2.returncode, " | ".join(fin[:3]), " | ".join(fin2[:2])), vu == attendu


with ThreadPoolExecutor(max_workers=2) as ex:
    res = list(ex.map(jouer, SABOTAGES))
with open(RELEVE, "w", encoding="utf-8") as f:
    f.write("# Sabotages de l'épreuve de la moulinette, %d cas, joués chacun sur une copie neuve du dépôt (sans .git)\n" % len(res))
    for nom, attendu, detail, ok in res:
        f.write("%s · %s · attendu %s · %s\n" % ("CONFORME" if ok else "NON CONFORME", nom, attendu, detail))
    f.write("BILAN : %d conformes sur %d\n" % (sum(r[3] for r in res), len(res)))
print(open(RELEVE, encoding="utf-8").read())
