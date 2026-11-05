#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MESURER_LES_INSTRUCTIONS_DE_LA_MOULINETTE — Mar 20-10-2026 (Paris). Simulation uniquement.

USAGE
    python3 -B tests/outils/MESURER_LES_INSTRUCTIONS_DE_LA_MOULINETTE_Mar_20-10-2026.py <racine>

① RÔLE — Dire, programme par programme et ligne par ligne, quelles instructions des quatre programmes de la
  moulinette (A-541) aucune épreuve n'exécute, avec les fonctions MÊMES du certificateur de nuit
  (`programmes/CERTIFIER_LA_VERSION.py` : copier, armer_la_mesure, calibrer_la_mesure, lister_les_epreuves, jouer,
  lire_la_mesure), limitées aux lancements qui touchent ces programmes.
② CONTEXTE D'APPEL — À la main, avant de livrer une modification de la moulinette ou de ses épreuves.
③ ENTRÉE — Un argument : la racine d'un dépôt. Elle n'est pas modifiée : le certificateur travaille sur une copie.
④ CONDITIONS D'ENTRÉE — Le module coverage est installé (le circuit installe la version 7.16.2) ; les épreuves de la
  moulinette sont déclarées dans `tests/LANCEMENT_DES_EPREUVES.json` (sinon « non déclarées » le dit).
⑤ SORTIE — Un affichage : le calibrage de la mesure, les épreuves non déclarées, chaque épreuve jouée avec son code
  et sa durée, le compte par programme, le total, puis les lignes non exécutées. Code de sortie 0 ; 2 sans
  argument ; une erreur du certificateur le fait sortir en erreur.
⑥ TRAITEMENT — ① copier et armer la mesure · ② calibrer · ③ lister les lancements et garder ceux de la moulinette ·
  ④ les jouer · ⑤ lire la mesure · ⑥ afficher · ⑦ effacer le dossier jetable.
⑦ UNITÉ — Des instructions (lignes exécutables au sens de coverage) ; des secondes pour les durées.
⑧ POURQUOI — Le certificateur refuse un programme nouveau tant qu'une instruction n'est exécutée par aucune
  épreuve ; Jean-Luc a choisi le 20-10-2026 à 17h51 de les éprouver (voie A). Ce programme rend ce compte
  reproductible par Cowork, au lieu d'un chiffre écrit à la main (R-728).
⑨ CE QUI CLOCHE — Il ne joue que les lancements de la moulinette, pas la certification entière : il ne dit rien
  des autres programmes ni de la durée totale de la nuit.
⑩ EFFET — Crée puis efface un dossier jetable ; lance les épreuves de la moulinette.
⑪ TERMINAISON — Sort lui-même. Chaque épreuve a le délai du certificateur. Un de ses appels peut-il ne pas
  revenir ? Non : `jouer` du certificateur borne chaque épreuve.
"""
import importlib.util, json, os, sys, tempfile, shutil
if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)
racine = os.path.abspath(sys.argv[1])
s = importlib.util.spec_from_file_location("C", os.path.join(racine, "programmes", "CERTIFIER_LA_VERSION.py"))
C = importlib.util.module_from_spec(s); s.loader.exec_module(C)
MOUL = ("programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py", "programmes/DECLINER_LES_STRATEGIES.py",
        "programmes/JOUER_LES_VERSIONS.py", "programmes/EPREUVES_DE_LA_DECLINAISON.py")
jet = tempfile.mkdtemp(prefix="mesure_moul_")
try:
    copie = C.copier(racine, jet)
    py, reglages, manifestes = C.armer_la_mesure(jet)
    ok, raison = C.calibrer_la_mesure(jet, py)
    print("calibrage :", ok, raison or "")
    lancements, non_decl = C.lister_les_epreuves(copie)
    print("non déclarées :", non_decl)
    garder = [l for l in lancements if any(os.path.basename(m)[:-3] in l[0] for m in MOUL) or "MOULINETTE" in l[0]]
    for chemin, dossier, arguments in garder:
        code, duree, lignes = C.jouer(copie, py, reglages, manifestes, chemin, dossier, arguments)
        print("joué :", chemin, arguments, "· code", code, "·", duree, "s ·", lignes[-1:] if lignes else "")
    tab = C.lire_la_mesure(jet, reglages, manifestes, copie)
    total = 0
    for m in MOUL:
        e = tab.get(m, {})
        nx = e.get("instructions_non_examinees")
        n = len(nx) if isinstance(nx, (list, set, tuple)) else nx
        print("%s : instructions %s, non exécutées %s" % (m, e.get("instructions"), n))
        if isinstance(nx, (list, set, tuple)):
            total += len(nx)
            src = open(os.path.join(copie, m), encoding="utf-8").read().split("\n")
            for k in sorted(nx):
                print("    %5d : %s" % (k, src[k - 1].strip()[:110]))
        elif isinstance(n, int):
            total += n
    print("TOTAL NON EXÉCUTÉES :", total)
    rap = json.load(open(os.path.join(jet, "mesure.json"), encoding="utf-8"))["files"]
    for m in MOUL:
        cle = [k for k in rap if k.endswith(m)]
        if not cle: continue
        src = open(os.path.join(copie, m), encoding="utf-8").read().split("\n")
        print("== lignes non exécutées :", m)
        for k in rap[cle[0]]["missing_lines"]:
            print("    %5d : %s" % (k, src[k - 1].strip()[:110]))
    if not any(m in tab for m in MOUL):
        print("clés de la mesure (extrait) :", list(tab)[:5], "· une entrée :", json.dumps(next(iter(tab.values())), default=str)[:400])
finally:
    shutil.rmtree(jet, ignore_errors=True)
