#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_SERIES_DE_SABOTAGES — Ven 16-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/SERIES_DE_SABOTAGES.py refuse tout relevé qui ne vaut plus, et que chacune de ses
  gardes a des dents.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py) ; à la main avant toute
  livraison qui touche ce module (R-731) : python3 tests/EPREUVES_DES_SERIES_DE_SABOTAGES_Ven_16-10-2026.py <racine>
  [--saboter]
③ ENTRÉE — La racine du dépôt (le module est pris dans son programmes/).
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le code de sortie : 0 si les cas V0 à V19 donnent la réponse attendue et, avec --saboter, si chaque
  sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT — Un petit dépôt d'essai (une épreuve à trois sabotages qui nomme programmes/P.py, une donnée) et un vrai
  relevé écrit par `ecrire_le_releve` (qui couvre aussi un programme non nommé, programmes/Q.py), puis : V0 le relevé
  vaut → 0 · V1 un sabotage retiré du relevé → 1 · V2 un sabotage qui « NE MORD PAS » → 1 · V3 aucun programme
  couvert (P.py et Q.py retirés) → 1 · V3bis le programme nommé P.py sans empreinte, Q.py couvert → 0 (la règle
  « chaque programme nommé » est retirée le 17-10-2026) · V4 un sabotage ajouté à l'épreuve
  → 1 · V5 la donnée changée → 1 · V6 la donnée effacée → 1 · V7 relevé absent → 2 · V8 en-tête faux → 2 · V9 ligne
  d'empreinte illisible → 2 · V10 l'épreuve non couverte → 1 · V11 verdict « NON CONFORME » → 1 · V12 un chemin à
  retour à la ligne refusé à l'écriture (ValueError) · V13 lancé seul : 0 sur le vrai relevé, 2 sur un relevé absent,
  2 sans arguments · V14 les fichiers lus cette nuit tous au relevé → 0 · V15 un fichier lu absent du relevé → 1
  (relecture de Cowork du 16-10-2026, cassure M1) · V16 aucune lecture relevée → 2 · V17 une ligne « MONTAGE
  IMPOSSIBLE » → 1 · V18 une ligne qui porte un chemin jetable → 1 · V19 une exception notée par son type seul → 0
  (cassure N de Cowork, 17-10-2026 : un plantage n'est pas une morsure, et une ligne doit pouvoir se refaire). Avec --saboter : chaque garde du module retirée, une à la fois, dans une copie.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 14h30 : la série des 20 ans ne se rejoue plus la nuit, la nuit
  vérifie son relevé ; si cette vérification se trompe, l'alarme se tait. Une épreuve qui reste verte quand on retire
  ce qu'elle teste n'est pas une preuve (R-731).
⑨ CE QUI CLOCHE — Le cas d'un relevé dont l'épreuve est illisible n'est pas joué.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin ; lance le module seul trois fois par tour.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 60 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MODULE = os.path.join(DEPOT, "programmes", "SERIES_DE_SABOTAGES.py")
EPREUVE = ('import os, sys\nracine = sys.argv[1]\nSABOTAGES = {"A1": 1, "A2": 2, "A3": 3}\n'
           'open(os.path.join(racine, "donnees", "d.csv")).read()\nopen(os.path.join(racine, "programmes/P.py")).read()\n')
SABOTAGES = {
    "S1_noms_non_lus": [("    mal = [n for n in noms if vus.get(n) != [\"mord\"]]\n", "    mal = []\n")],
    "S2_ne_mord_pas_admis": [("vus.get(n) != [\"mord\"]", "n not in vus")],
    "S3_aucun_programme_admis": [("    if not any(c.startswith(\"programmes/\") for c in attendus):\n", "    if False:\n")],
    "S4_empreintes_non_comparees": [("        elif empreinte(p) != e:\n", "        elif False:\n")],
    "S5_disparu_admis": [("        if not os.path.isfile(p):\n            changes.append(c + \" (disparu)\")\n        elif",
                          "        if not os.path.isfile(p):\n            pass\n        elif")],
    "S6_entete_non_exige": [("    if not lignes or lignes[0] != ENTETE:\n", "    if not lignes:\n")],
    "S7_epreuve_non_exigee": [("    if epreuve not in attendus:\n", "    if False:\n")],
    "S8_verdict_ignore": [("    if lignes[-1] != VERDICT_CONFORME:\n", "    if False:\n")],
    "S9_absent_cru": [("        return 2, f\"relevé de la série illisible ou absent : {releve} ({type(e).__name__})\"",
                       "        return 0, f\"relevé de la série illisible ou absent : {releve} ({type(e).__name__})\"")],
    "S10_ligne_illisible_admise": [("            if len(morceaux) != 2 or len(morceaux[0]) != 64:\n", "            if False:\n")],
    "S11_retour_a_la_ligne_admis": [("    if any(\"\\n\" in c for c in chemins):\n", "    if False:\n")],
    "S12_lectures_ignorees": [("    if lus is not None:\n", "    if False:\n")],
    "S13_lectures_vides_admises": [("        if not lus:\n", "        if False:\n")],
    # cassure N de Cowork, 17-10-2026 : un plantage compté comme une morsure
    "S14_ligne_non_reproductible_admise": [("    if douteuses:\n", "    if False:\n")],
}


def charger(chemin):
    """Charge le module depuis `chemin` et le rend.

    ① RÔLE — Avoir le module vrai ou saboté. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`. ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le module. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sp = importlib.util.spec_from_file_location("SERIE_%d" % id(chemin), chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def tour(module):
    """Joue V0 à V19 avec le module à `module` ; rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `module` : le chemin du module à éprouver. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms des cas qui ne donnent pas la réponse attendue. [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit un dépôt d'essai jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    S = charger(module)
    faux = []
    d = tempfile.mkdtemp(prefix="series_")
    try:
        r = os.path.join(d, "depot")
        for c, t in (("tests/EPR.py", EPREUVE), ("programmes/P.py", "X = 1\n"), ("programmes/Q.py", "Y = 1\n"),
                     ("donnees/d.csv", "1,2,3\n")):
            os.makedirs(os.path.dirname(os.path.join(r, c)), exist_ok=True)
            open(os.path.join(r, c), "w", encoding="utf-8").write(t)
        rel = "tests/resultats/SERIE.txt"
        S.ecrire_le_releve(r, rel, "tests/EPR.py", ["programmes/P.py", "programmes/Q.py", "donnees/d.csv"],
                           ["A1 mord : ['H1']", "A2 mord : ['H1']", "A3 mord : ['H1']"], True, ["essai"])
        vrai = open(os.path.join(r, rel), encoding="utf-8").read()

        def avec(texte, cas, attendu, fichier=None, contenu=None):
            open(os.path.join(r, rel), "w", encoding="utf-8").write(texte)
            garde = None
            if fichier:
                p = os.path.join(r, fichier)
                garde = open(p, encoding="utf-8").read() if os.path.exists(p) else None
                if contenu is None:
                    os.remove(p)
                else:
                    open(p, "w", encoding="utf-8").write(contenu)
            code = S.verifier_la_serie(r, "tests/EPR.py", rel)[0]
            if fichier and garde is not None:
                open(os.path.join(r, fichier), "w", encoding="utf-8").write(garde)
            open(os.path.join(r, rel), "w", encoding="utf-8").write(vrai)
            if code != attendu:
                faux.append(f"{cas} (code {code}, attendu {attendu})")

        avec(vrai, "V0", 0)
        avec(vrai.replace("A2 mord : ['H1']\n", ""), "V1", 1)
        avec(vrai.replace("A2 mord", "A2 NE MORD PAS"), "V2", 1)
        # V3 : aucun programme couvert (P.py et Q.py retirés du relevé). La règle « chaque programme nommé » est retirée
        # le 17-10-2026 (superviseur, R-759) : un relevé qui garde Q.py sans P.py est désormais accepté (V3bis).
        avec("\n".join(l for l in vrai.splitlines() if not l.endswith((" programmes/P.py", " programmes/Q.py"))) + "\n",
             "V3", 1)
        avec("\n".join(l for l in vrai.splitlines() if not l.endswith(" programmes/P.py")) + "\n", "V3bis", 0)
        avec(vrai, "V4", 1, "tests/EPR.py", EPREUVE.replace('"A3": 3}', '"A3": 3, "A4": 4}'))
        avec(vrai, "V5", 1, "donnees/d.csv", "1,2,4\n")
        avec(vrai, "V6", 1, "donnees/d.csv", None)
        os.remove(os.path.join(r, rel))
        if S.verifier_la_serie(r, "tests/EPR.py", rel)[0] != 2:
            faux.append("V7")
        avec("# autre en-tête\n" + vrai, "V8", 2)
        avec(vrai.replace("EMPREINTE ", "EMPREINTE court ", 1), "V9", 2)
        avec("\n".join(l for l in vrai.splitlines() if not l.endswith(" tests/EPR.py")) + "\n", "V10", 1)
        avec(vrai.replace(S.VERDICT_CONFORME, "VERDICT : NON CONFORME"), "V11", 1)
        # V17 à V19 — une ligne qu'un essai refait ne rendrait pas mot pour mot (cassure N de Cowork, 17-10-2026)
        avec(vrai.replace("A2 mord : ['H1']", "A2 mord : ['H1 (MONTAGE IMPOSSIBLE : git commit : code 128)']"), "V17", 1)
        avec(vrai.replace("A2 mord : ['H1']", "A2 mord : [\"H1 (levé : CalledProcessError /tmp/boucle_epreuve_x/auteur)\"]"),
             "V18", 1)
        avec(vrai.replace("A2 mord : ['H1']", "A2 mord : ['H1 (levé : TypeError)']"), "V19", 0)
        try:
            S.ecrire_le_releve(r, "tests/resultats/X.txt", "tests/EPR.py", ["a\nb"], [], True, [])
            faux.append("V12")
        except ValueError:
            pass
        except Exception as e:      # une autre erreur : la garde n'a pas parlé
            faux.append(f"V12 ({type(e).__name__})")
        # V14 à V16 : la liste à surveiller vient de ce que l'épreuve a lu cette nuit (relecture de Cowork, cassure M1)
        open(os.path.join(r, "donnees", "autre.csv"), "w", encoding="utf-8").write("x\n")
        for cas, lus, attendu in (("V14", {"tests/EPR.py", "programmes/P.py", "donnees/d.csv"}, 0),
                                  ("V15", {"tests/EPR.py", "programmes/P.py", "donnees/d.csv", "donnees/autre.csv"}, 1),
                                  ("V16", set(), 2)):
            code = S.verifier_la_serie(r, "tests/EPR.py", rel, lus)[0]
            if code != attendu:
                faux.append(f"{cas} (code {code}, attendu {attendu})")
        codes = [subprocess.run([sys.executable, module, *a], capture_output=True, timeout=60).returncode
                 for a in ((r, rel), (r, "tests/resultats/ABSENT.txt"), ())]
        if codes != [0, 2, 2]:
            faux.append(f"V13 {codes}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Voir la fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(MODULE)
    print("== Z0 module tel quel : " + ("V0 à V19 conformes" if not faux else "FAUX " + ", ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv:
        texte = open(MODULE, encoding="utf-8").read()
        for nom, remplacements in SABOTAGES.items():
            t = texte
            for a, b in remplacements:
                if t.count(a) != 1:
                    print(f"== {nom} NE S'APPLIQUE PLUS ({t.count(a)} fois) : {a[:60]!r}")
                    return 2
                t = t.replace(a, b)
            d = tempfile.mkdtemp(prefix="series_sab_")
            try:
                p = os.path.join(d, "SERIES_DE_SABOTAGES.py")
                open(p, "w", encoding="utf-8").write(t)
                f = tour(p)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"== {nom} : {'mord' if f else 'NE MORD PAS'} {f[:3]}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
