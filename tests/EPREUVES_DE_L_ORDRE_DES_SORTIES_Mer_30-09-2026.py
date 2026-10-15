#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_ORDRE_DES_SORTIES — Mer 30-09-2026 (Paris)
Rôle : prouver que `tester_seance` de programmes/MODULE_POSITIONS.py applique ses quatre tests de sortie dans
l'ordre décidé, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche `tester_seance` (R-755 ②).

À QUOI ÇA SERT. Une position simulée porte deux seuils fixés à l'achat : l'OBJECTIF (on vend en gain) et la
VENTE FORCÉE (on vend en perte). `tester_seance` dit, pour une séance (ouverture, plus haut, plus bas, clôture),
si la position sort et à quel prix. Le juge des stratégies et le programme du soir (TENIR_LES_POSITIONS.py)
l'empruntent tous deux. R-607 ③ (décision de Jean-Luc du 27-09-2026 à 16h14, option 1 : « On compte le gain à
l'ouverture, parce que la vente a eu lieu avant la baisse. ») : une séance qui OUVRE au-dessus de l'objectif puis
descend sous la vente forcée donne un gain au prix d'ouverture. Jusqu'au 30-09-2026, la fonction testait le plus
bas avant le saut favorable et comptait une perte.

LES ÉPREUVES, sur la vraie fonction, importée de la copie du dépôt (objectif 104, vente forcée 97,5 — les seuils
de +4 % et −2,5 % pour une entrée à 100) :
E1 le cas de R-607 ③ — ouverture 105, plus bas 97 : gain à l'ouverture, 105, TP_GAP ;
E2 saut défavorable — ouverture 97, plus haut 106 : perte à l'ouverture, 97, SL_GAP ;
E3 les deux seuils touchés sans saut — ouverture 100, plus haut 106, plus bas 97 : perte au seuil, 97,5, SL (R-602) ;
E4 objectif seul — ouverture 100, plus haut 105 : 104, TP ;
E5 vente forcée seule — ouverture 100, plus bas 97 : 97,5, SL ;
E6 rien — ouverture 100, entre les seuils : aucune sortie ;
E7 le cas réel du calibrage du module (Bureau Veritas, 29-07-2026, ouverture 29,24 au-dessus de l'objectif
   28,3712) : 29,24, TP_GAP.
LES SABOTAGES : S1 remet l'ordre d'avant (plus bas avant le saut favorable) → E1 · S2 teste le plus haut avant le
plus bas → E3 · S3 vend le saut favorable à l'objectif au lieu de l'ouverture → E1, E7 · S4 vend le saut
défavorable à la vente forcée → E2.

USAGE : python3 tests/EPREUVES_DE_L_ORDRE_DES_SORTIES_Mer_30-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si les épreuves sont vertes sans sabotage et, avec --saboter, si chaque sabotage fait rougir au moins
une épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus (ancre absente).
"""
import importlib.util, os, shutil, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MP = "programmes/MODULE_POSITIONS.py"
T1 = '    if bar["open"] <= sl:\n        return bar["open"], "SL_GAP"\n'
T2 = '    if bar["open"] >= tp:\n        return bar["open"], "TP_GAP"\n'
T3 = '    if bar["low"] <= sl:\n        return sl, "SL"\n'
T4 = '    if bar["high"] >= tp:\n        return tp, "TP"\n'
SABOTAGES = {
    "Z0": [],
    "S1_ordre_d_avant": [(MP, T2 + "    # SANS SAUT", "    # SANS SAUT"), (MP, T3, T3 + T2)],
    "S2_plus_haut_d_abord": [(MP, T3 + T4, T4 + T3)],
    "S3_saut_favorable_a_l_objectif": [(MP, 'return bar["open"], "TP_GAP"', 'return tp, "TP_GAP"')],
    "S4_saut_defavorable_au_stop": [(MP, 'return bar["open"], "SL_GAP"', 'return sl, "SL_GAP"')],
}
CAS = [
    ("E1 R-607 ③ : ouvre au-dessus de l'objectif puis passe sous la vente forcée",
     {"open": 105.0, "high": 106.0, "low": 97.0, "close": 98.0}, 104.0, 97.5, (105.0, "TP_GAP")),
    ("E2 saut défavorable, même si le plus haut dépasse l'objectif",
     {"open": 97.0, "high": 106.0, "low": 96.0, "close": 100.0}, 104.0, 97.5, (97.0, "SL_GAP")),
    ("E3 les deux seuils sans saut : la perte (R-602)",
     {"open": 100.0, "high": 106.0, "low": 97.0, "close": 100.0}, 104.0, 97.5, (97.5, "SL")),
    ("E4 objectif seul", {"open": 100.0, "high": 105.0, "low": 99.0, "close": 104.5}, 104.0, 97.5, (104.0, "TP")),
    ("E5 vente forcée seule", {"open": 100.0, "high": 101.0, "low": 97.0, "close": 98.0}, 104.0, 97.5, (97.5, "SL")),
    ("E6 rien", {"open": 100.0, "high": 103.0, "low": 98.0, "close": 101.0}, 104.0, 97.5, None),
    ("E7 cas réel : Bureau Veritas, 29-07-2026", {"open": 29.24, "high": 29.5, "low": 28.9, "close": 29.3},
     28.3712, 26.598, (29.24, "TP_GAP")),
]


def epreuves(r):
    """Importe `tester_seance` de la copie `r` et joue les sept cas.

    ① RÔLE — rendre le verdict de chaque cas décrit en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `r` : la racine d'une copie du dépôt, éventuellement sabotée.
    ④ CONDITIONS D'ENTRÉE — le module doit s'importer ; sinon l'import lève.
    ⑤ SORTIE — UNE valeur : la liste des couples (nom du cas, vrai si vert).
      [rend: 1]
    ⑥ TRAITEMENT — importer le module de la copie, appeler la fonction sur chaque séance, comparer au résultat
      attendu, prix à un millionième près.
    ⑦ UNITÉ — des prix en euros.
    ⑧ POURQUOI — la fonction réelle est appelée, jamais une copie de son ordre (R-708).
    ⑨ CE QUI CLOCHE — E7 fabrique le plus haut, le plus bas et la clôture de la séance du 29-07-2026 : seule
      l'ouverture (29,24) et l'objectif (28,3712) sont les vrais, relevés dans R-607 ①.
    ⑩ EFFET — importe un module.
    ⑪ TERMINAISON — rend la main.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("MODULE_POSITIONS_copie", os.path.join(r, MP))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    res = []
    for nom, bar, tp, sl, attendu in CAS:
        obtenu = m.tester_seance(dict(bar), tp, sl)
        if attendu is None or obtenu is None:
            ok = obtenu is None and attendu is None
        else:
            ok = abs(obtenu[0] - attendu[0]) < 1e-6 and obtenu[1] == attendu[1]
        res.append((f"{nom} → {obtenu}", ok))
    return res


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — le lancement du fichier.
    ③ ENTRÉE — la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — la racine doit contenir programmes/MODULE_POSITIONS.py.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier le module dans un dossier jetable, appliquer le sabotage, jouer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — seul le module est copié, pas le dépôt : un sabotage ailleurs ne serait pas vu.
    ⑩ EFFET — crée puis efface des dossiers temporaires ; affiche un compte rendu.
    ⑪ TERMINAISON — rend la main par son code.
      [sort: non]
    """
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        d = tempfile.mkdtemp(prefix="ordre_sorties_")
        try:
            os.makedirs(os.path.join(d, "programmes"))
            shutil.copy(os.path.join(DEPOT, MP), os.path.join(d, MP))
            for f, a, b in SABOTAGES[sab]:
                p = os.path.join(d, f)
                x = open(p, encoding="utf-8").read()
                if x.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple — l'épreuve ne prouverait plus rien")
                    return 2
                open(p, "w", encoding="utf-8").write(x.replace(a, b))
            res = epreuves(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        rouges = [n for n, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for n in rouges:
            print("     ROUGE " + n)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
