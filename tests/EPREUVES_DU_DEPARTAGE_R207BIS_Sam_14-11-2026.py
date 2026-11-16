#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_DEPARTAGE_R207BIS — le jeton du soir va au CCI le plus bas, égalité → alphabétique (R-207bis).

Simulation uniquement : aucun ordre réel n'est jamais passé.
Écrit le samedi 14-11-2026 (Paris).

LE SENS EN TÊTE. R-207bis (gouvernance/REGISTRE_REGLES.md) : « stratégies TECHNIQUES → le CCI le plus bas (la plus
survendue), égalité → alphabétique ». Jusqu'au 14-11-2026, programmes/TENIR_LES_POSITIONS.py donnait le jeton à la
première valeur de l'univers, et son adaptateur perdait le CCI. Ces épreuves prouvent la réparation : le CCI voyage
(`attribuer_aux_strategies`), et la sélection l'applique à un seul endroit (`departager_r207bis`, appelé par
`ouvrir_sur_signaux`, donc par `tenir`, donc par le circuit ET par tout rejeu). Depuis le tour 2 (relecteur et
superviseur R-759 du 14-11-2026) : tout signal doit porter un CCI fini ; le soir, une stratégie dont un signal est
fautif est MISE À PART seule (`mettre_a_part_les_cci_fautifs`), le teneur sort en 0 et dit `signaux_mis_a_part=<n>`,
et `.github/workflows/collecte_abc.yml` rougit sur ce nom.

① RÔLE — Éprouver `_cci_du_signal`, `departager_r207bis`, `mettre_a_part_les_cci_fautifs`,
  `attribuer_aux_strategies`, `ouvrir_sur_signaux` et `tenir_pour_de_vrai` de programmes/TENIR_LES_POSITIONS.py, et
  les noms de sortie lus par `.github/workflows/collecte_abc.yml`, sur des cas construits, sur deux vraies journées
  du fichier maître, sur une vraie soirée rejouée de bout en bout (2026-10-20) et sur le golden.
② CONTEXTE D'APPEL — À la main : `python3 -B tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py <racine>
  [--indic=<chemin de MESURER_LES_INDICATEURS.py> | --indic-git=<révision>] [--saboter]`. Sans option, le rejeu
  est lu sous `<racine>/programmes/` (installé sur main). Une révision antérieure à A-839 (16-11-2026), qui porte
  encore `ordre_de_departage`, fait tomber T07 : c'est voulu.
③ ENTRÉE — La racine du dépôt ; `--indic=` : un autre rejeu, s'il n'est pas sous
  `<racine>/programmes/` ; `--indic-git=` : le même, lu dans une révision Git du dépôt (copie temporaire effacée
  après chargement) ; `--saboter` : rejouer les cas sur des copies sabotées du code.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/TENIR_LES_POSITIONS.py, programmes/DETECTER_LES_SIGNAUX_GITHUB.py,
  donnees/cours_maitre.csv, le registre des stratégies, le référentiel, le golden et son témoin,
  .github/workflows/collecte_abc.yml.
⑤ SORTIE — Code 0 si tous les cas tiennent (et, avec --saboter, si chaque sabotage fait tomber au moins un cas, et,
  quand il porte une raison attendue, la fait apparaître dans le message d'un cas tombé) ; 1 sinon ; 2 si un cas n'a
  pas pu tourner ou si le texte visé par un sabotage n'est pas trouvé une fois (R-734 : un contrôle qui n'a pas tourné
  ne rend pas 0).
⑥ TRAITEMENT — Voir `main`.
⑦ UNITÉ — CCI sans unité ; euros ; pourcents.
⑧ POURQUOI — R-731 : tout code modifié passe des épreuves avec sabotages, dont une sur une vraie ligne (R-732).
⑨ CE QUI CLOCHE — T06 construit la liste des stratégies comme `tenir_pour_de_vrai` (VIVANTE et univers non vide) sans repasser
  `fiche_suivie` du juge.
⑩ EFFET — Lit des fichiers ; écrit dans des dossiers temporaires une copie du dépôt (sans .git, etudes, archives et
  les sources brutes de donnees/) pour rejouer la soirée du 2026-10-20, et les copies sabotées ; les efface à la fin.
  N'écrit rien dans le dépôt.
⑪ TERMINAISON — Termine le programme par son code de sortie.
"""

import os
import sys
import csv
import io
import json
import shutil
import tempfile
import subprocess
import contextlib
import importlib.util

# LA GARDE DES PAS ROUGES, partagée avec V10f de la vente unique (superviseur R-759 du tour 2, N-2). Le dossier de
# ce fichier est mis en tête de sys.path explicitement : l'import ne dépend pas de la façon dont Python est lancé.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import GARDE_DU_PAS_ROUGE  # noqa: E402

CAS = []


def cas(fonction):
    """Inscrit une fonction comme cas d'épreuve.

    ① RÔLE — Tenir la liste ordonnée des cas. ② CONTEXTE D'APPEL — Décorateur, au chargement.
    ③ ENTRÉE — `fonction` : un cas, qui reçoit le contexte et lève AssertionError s'il tombe.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la fonction reçue. ⑥ TRAITEMENT — L'ajoute à `CAS`.
    ⑦ UNITÉ — — ⑧ POURQUOI — Rejouer les mêmes cas sur chaque sabotage. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Modifie `CAS`. ⑪ TERMINAISON — Rend la main.
    """
    CAS.append(fonction)
    return fonction


def charger(nom, chemin):
    """Charge un fichier Python sous un nom de module.

    ① RÔLE — Charger le code éprouvé, original ou saboté. ② CONTEXTE D'APPEL — `main`, `sabotage`.
    ③ ENTRÉE — `nom` : nom de module · `chemin` : le fichier. ④ CONDITIONS D'ENTRÉE — Le dossier `programmes/` de la
    racine est dans `sys.path` (le module y importe ses voisins). ⑤ SORTIE — UNE valeur : le module.
    ⑥ TRAITEMENT — spec, module, exécution. ⑦ UNITÉ — — ⑧ POURQUOI — Un module neuf par sabotage.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le code chargé. ⑪ TERMINAISON — Lève si le code ne se charge pas.
    """
    sp = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def sig(strat, valeur, cci, date="2026-01-05"):
    """Fabrique un signal attribué.

    ① RÔLE — Écrire un cas court. ② CONTEXTE D'APPEL — Les cas construits. ③ ENTRÉE — stratégie, valeur, CCI, date.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : un dictionnaire {strategie, valeur, date_signal, cci}.
    ⑥ TRAITEMENT — — ⑦ UNITÉ — CCI sans unité. ⑧ POURQUOI — La forme rendue par `attribuer_aux_strategies`.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    d = {"strategie": strat, "valeur": valeur, "date_signal": date}
    if cci is not None:
        d["cci"] = cci
    return d


def jeton(TP, positions, strat):
    """Rend la valeur qui a pris le jeton d'une stratégie en « un jeton ».

    ① RÔLE — Lire le choix fait par `ouvrir_sur_signaux`. ② CONTEXTE D'APPEL — Les cas. ③ ENTRÉE — le module, les
    positions rendues, la stratégie. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des valeurs en un
    jeton pour cette stratégie. ⑥ TRAITEMENT — Filtre. ⑦ UNITÉ — — ⑧ POURQUOI — Le jeton est ce que R-207bis décide.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    return [p["valeur"] for p in positions if p["strategie"] == strat and p["comptabilite"] == TP.UN_JETON]


# ── LES CAS ─────────────────────────────────────────────────────────────────────────────────────────────────────────
# Le cas construit des quatre ordres : reçu dans l'ordre « de l'univers » MU, ZETA, KAPPA, ALPHA.
#   R-207bis (CCI bas, puis nom)   → KAPPA  (−120, à égalité avec MU, KAPPA < MU)
#   ordre de l'univers             → MU
#   CCI le plus haut               → ZETA   (−30)
#   alphabétique seul              → ALPHA
QUATRE = [("MU", -120.0), ("ZETA", -30.0), ("KAPPA", -120.0), ("ALPHA", -80.0)]


@cas
def T01_quatre_ordres_distingues(ctx):
    """R-207bis choisit KAPPA, que ni l'univers (MU), ni le CCI haut (ZETA), ni l'alphabet seul (ALPHA) ne choisissent.

    ① RÔLE — Distinguer les quatre ordres possibles. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune ; lève AssertionError. ⑥ TRAITEMENT — Range, puis ouvre.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le golden seul ne distingue pas l'alphabétique (consigne du Chat, 14-11-2026).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    recus = [sig("S", v, c) for v, c in QUATRE]
    ordre = [s["valeur"] for s in TP.departager_r207bis(recus)]
    assert ordre == ["KAPPA", "MU", "ALPHA", "ZETA"], ordre
    nouvelles, ignores = TP.ouvrir_sur_signaux([], recus, None)
    assert jeton(TP, nouvelles, "S") == ["KAPPA"], jeton(TP, nouvelles, "S")
    illim = sorted(p["valeur"] for p in nouvelles if p["comptabilite"] == TP.JETONS_ILLIMITES)
    assert illim == ["ALPHA", "KAPPA", "MU", "ZETA"], illim
    assert len(ignores) == 3, ignores


@cas
def T02_strategies_separees_places_gardees(ctx):
    """Chaque stratégie est départagée chez elle, et les places de chaque stratégie dans la liste sont gardées.

    ① RÔLE — Prouver que le départage ne mélange pas les stratégies. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune. ⑥ TRAITEMENT — Liste entrelacée de deux stratégies.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le jeton est par stratégie ; un tri global changerait l'entrelacement sans raison.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    recus = [sig("A", "VINCI", -50), sig("B", "ENGIE", -10), sig("A", "ENGIE", -90), sig("B", "AIRBUS", -200)]
    rendu = TP.departager_r207bis(recus)
    assert [(s["strategie"], s["valeur"]) for s in rendu] == [
        ("A", "ENGIE"), ("B", "AIRBUS"), ("A", "VINCI"), ("B", "ENGIE")], rendu
    nouvelles, _ = TP.ouvrir_sur_signaux([], recus, None)
    assert jeton(TP, nouvelles, "A") == ["ENGIE"] and jeton(TP, nouvelles, "B") == ["AIRBUS"]


@cas
def T03_tout_cci_fautif_refuse(ctx):
    """Absent, null, texte blanc, illisible, à virgule, NaN, infini : refusés par DepartageImpossible, même SEUL ;
    un CCI en texte à point décimal est lu.

    ① RÔLE — Les conditions d'entrée de `departager_r207bis` (superviseur R-759 du 14-11-2026, D1 : il n'existe plus
    de « cas sans CCI »). ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune. ⑥ TRAITEMENT — Sept listes d'un seul signal, une de deux. ⑦ UNITÉ — —
    ⑧ POURQUOI — Avant, un CCI absent laissait l'ordre de l'univers, sans un mot (relecteur du tour 1, D1).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    sans_cle = {"strategie": "S", "valeur": "A", "date_signal": "2026-01-05"}
    for mauvais in ([sans_cle], [dict(sans_cle, cci=None)], [dict(sans_cle, cci="  ")], [dict(sans_cle, cci="abc")],
                    [dict(sans_cle, cci="-57,03")], [dict(sans_cle, cci=float("nan"))],
                    [dict(sans_cle, cci=float("-inf"))], [sig("S", "B", -10), dict(sans_cle, cci=None)]):
        try:
            TP.departager_r207bis(mauvais)
        except TP.DepartageImpossible:
            continue
        raise AssertionError("accepté à tort : %r" % mauvais)
    rendu = TP.departager_r207bis([sig("S", "A", "-10.5"), sig("S", "B", "-99")])
    assert [s["valeur"] for s in rendu] == ["B", "A"], rendu


@cas
def T04_liste_recue_intacte(ctx):
    """La liste reçue n'est pas modifiée, et les objets rendus sont les objets reçus.

    ① RÔLE — Le ⑩ « Aucun » de `departager_r207bis`. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune. ⑥ TRAITEMENT — Compare avant et après. ⑦ UNITÉ — —
    ⑧ POURQUOI — `tenir_pour_de_vrai` relit `signaux` après `tenir`. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    recus = [sig("S", v, c) for v, c in QUATRE]
    avant = [dict(s) for s in recus]
    rendu = TP.departager_r207bis(recus)
    assert recus == avant and [id(s) for s in recus] != [id(s) for s in rendu]
    assert sorted(id(s) for s in recus) == sorted(id(s) for s in rendu)


@cas
def T05_le_cci_voyage(ctx):
    """`attribuer_aux_strategies` recopie le CCI du détecteur dans chaque signal attribué, pour chaque stratégie.

    ① RÔLE — Le maillon perdu le 12-09-2026. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx` (référentiel réel).
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune. ⑥ TRAITEMENT — Deux signaux, deux stratégies. ⑦ UNITÉ — —
    ⑧ POURQUOI — Sans CCI, le départage laisse l'ordre de l'univers. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    du_detecteur = [{"valeur": "BOUYGUES", "date_signal": "2025-10-07", "cmf": 0.021878, "cci": -81.77, "close": 37.15},
                    {"valeur": "VINCI", "date_signal": "2025-10-07", "cmf": 0.105847, "cci": -120.54, "close": 115.6}]
    t, sans, hors = TP.attribuer_aux_strategies(du_detecteur, [("X", {"EN", "DG"}), ("Y", {"EN"})], ctx["mnemo"])
    assert not sans and not hors, (sans, hors)
    assert [(s["strategie"], s["valeur"], s["cci"]) for s in t] == [
        ("X", "BOUYGUES", -81.77), ("Y", "BOUYGUES", -81.77), ("X", "VINCI", -120.54)], t


@cas
def T06_vraie_journee_du_fichier_maitre(ctx):
    """Le 2025-10-07 et le 2026-05-18, relus par le VRAI détecteur sur donnees/cours_maitre.csv, puis attribués aux
    fiches VIVANTES du registre : le jeton va au CCI le plus bas.

    ① RÔLE — La chaîne réelle détecteur → adaptateur → sélection, sur de vraies lignes (R-732).
    ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx` (signaux relus une fois par `main`).
    ④ CONDITIONS D'ENTRÉE — Les fiches C5E10-OBS-V1 (univers avec EN, DG, ENGI, VIE) et C5E10-QA-V1 (EN, VIE, pas DG
    ni ENGI) sont VIVANTES au registre — mesuré le 14-11-2026. ⑤ SORTIE — Aucune.
    ⑥ TRAITEMENT — Pour chaque journée : signaux du détecteur, `attribuer_aux_strategies`, `ouvrir_sur_signaux`.
    ⑦ UNITÉ — — ⑧ POURQUOI — 2025-10-07 : BOUYGUES (−81,77) avant VINCI (−120,54) dans l'univers ; 2026-05-18 : ENGIE
    (−114,15) avant VEOLIA (−117,84). L'ancien circuit donnait BOUYGUES et ENGIE à C5E10-OBS-V1.
    ⑨ CE QUI CLOCHE — Les fiches peuvent changer : le cas le dit s'il ne trouve pas les univers attendus.
    ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    strategies = dict(ctx["strategies"])
    assert {"EN", "DG", "ENGI", "VIE"} <= strategies.get("C5E10-OBS-V1", set()), "univers OBS inattendu"
    assert "EN" in strategies.get("C5E10-QA-V1", set()) and "DG" not in strategies["C5E10-QA-V1"], "univers QA"
    attendu = {"2025-10-07": {"C5E10-OBS-V1": "VINCI", "C5E10-QA-V1": "BOUYGUES"},
               "2026-05-18": {"C5E10-OBS-V1": "VEOLIA", "C5E10-QA-V1": "VEOLIA"}}
    for jour, voulu in attendu.items():
        bruts = ctx["jours"][jour]
        assert len(bruts) == 2 and all(isinstance(s.get("cci"), float) for s in bruts), bruts
        t, sans, _hors = TP.attribuer_aux_strategies(bruts, ctx["strategies"], ctx["mnemo"])
        assert not sans, sans
        nouvelles, _ = TP.ouvrir_sur_signaux([], t, None)
        for strat, val in voulu.items():
            assert jeton(TP, nouvelles, strat) == [val], (jour, strat, jeton(TP, nouvelles, strat))


@cas
def T07_golden_par_le_circuit_seul(ctx):
    """Le rejeu, qui ne départage plus lui-même (A-839), retrouve le golden : 44 · 63,6 % · +58 800,00 € en un jeton,
    100 · 61,0 % · +111 334,24 € en jetons illimités — grâce au seul `tenir` du circuit.

    ① RÔLE — Prouver que R-207bis vit à UN seul endroit, `departager_r207bis` dans le circuit, et que le rejeu n'en
    garde aucune copie. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx` (module du rejeu).
    ④ CONDITIONS D'ENTRÉE — Le golden et son témoin. ⑤ SORTIE — Aucune.
    ⑥ TRAITEMENT — ① exiger que le rejeu n'ait plus de fonction `ordre_de_departage` (une copie revenue diviserait de
    nouveau la règle) · ② `calibrer_sur_le_golden`, la tenue des positions remplacée par le module éprouvé (saboté ou
    non) : le calibrage compare les opérations UNE À UNE au producteur du golden.
    ⑦ UNITÉ — Euros au centime, pourcents au dixième.
    ⑧ POURQUOI — Décision de Jean-Luc A-839 (16-11-2026 à 07h56, « 1 ») : R-207bis à un seul endroit, la tenue des
    positions du soir ; le rejeu passe les signaux tels quels. Ce cas remplace T01c, T18 et les sabotages S11, S20, S21
    de `tests/EPREUVES_DES_INDICATEURS_Sam_14-11-2026.py`, retirés par la même décision : S1 (ordre de l'univers), S2
    (CCI le plus haut) et S3 (alphabétique) le font rougir. Dans l'ordre de l'univers, l'ancien circuit donnait
    44 · 65,9 % · +67 688,60 € ; dans l'ordre alphabétique, les totaux restent mais deux opérations changent.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Remplace pour la durée du cas la brique TP du rejeu, puis la remet.
    ⑪ TERMINAISON — Rend la main.
    """
    M = ctx["M"]
    if M is None:
        raise RuntimeError("NON JOUÉ : MESURER_LES_INDICATEURS.py introuvable (--indic=)")
    assert not hasattr(M, "ordre_de_departage"), \
        "le rejeu porte encore sa copie de R-207bis (ordre_de_departage) : A-839 la retire"
    b = M.charger_les_briques(ctx["racine"])
    garde_tp = b["TP"]
    b["TP"] = ctx["TP"]
    try:
        ok, lignes, rendu = M.calibrer_sur_le_golden(ctx["racine"])
    finally:
        b["TP"] = garde_tp
    ctx["lignes_golden"] = lignes
    assert ok, "\n".join(lignes)
    un = rendu["un_jeton"]
    assert len(un) == 44 and abs(sum(o["net"] for o in un) - 58800.0) < 0.005, lignes


@cas
def T08_mise_a_part_par_strategie(ctx):
    """Cas A : une stratégie dont TOUS les signaux ont un CCI NaN, une autre dont le seul signal a un CCI null, sont
    mises à part en entier ; une stratégie saine garde ses signaux, dans l'ordre reçu.

    ① RÔLE — `mettre_a_part_les_cci_fautifs`. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune. ⑥ TRAITEMENT — Trois stratégies, un signal fautif sur une quatrième
    qui en a deux. ⑦ UNITÉ — — ⑧ POURQUOI — Superviseur R-759 du 14-11-2026, D2 : seule la stratégie fautive est mise
    à part, toute entière ; un NaN et un null sont traités pareil. Sabotage « NaN vaut absent » du relecteur : un NaN
    qui passerait pour un CCI absent serait ici aussi mis à part — le cas est écrit pour qu'un NaN RANGÉ rougisse.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    nan = float("nan")
    recus = [sig("NAN", "A", nan), sig("SAINE", "Z", -90), sig("NAN", "B", nan), sig("NUL", "C", None),
             sig("MIXTE", "D", -150), sig("SAINE", "Y", -95), sig("MIXTE", "E", nan)]
    gardes, a_part = TP.mettre_a_part_les_cci_fautifs(recus)
    assert [(s["strategie"], s["valeur"]) for s in gardes] == [("SAINE", "Z"), ("SAINE", "Y")], gardes
    vus = {m["strategie"]: [s["valeur"] for s in m["signaux"]] for m in a_part}
    assert vus == {"NAN": ["A", "B"], "NUL": ["C"], "MIXTE": ["D", "E"]}, vus
    assert all(m["raisons"] for m in a_part)


@cas
def T09_soiree_reelle_de_bout_en_bout(ctx):
    """Cas B : la soirée du 2026-10-20, rejouée par le VRAI détecteur puis le VRAI `tenir_pour_de_vrai` sur une copie
    du dépôt (cours tronqués à cette séance, positions vides) : sans faute, puis avec un NaN sur ENGIE, un CCI null
    sur un signal seul, le CCI retiré des deux signaux, et le dernier filet.

    ① RÔLE — Le chemin réel du soir (R-732 : une vraie ligne). ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx` (copie
    préparée par `preparer`). ④ CONDITIONS D'ENTRÉE — Ce soir-là, le détecteur rend ENGIE (CCI −57,03, première de
    l'univers) et EIFFAGE (CCI −166,47) ; ENGIE (ENGI) n'est que dans l'univers de C5E10-OBS-V1, EIFFAGE (FGR) dans
    les deux (relecteur du tour 1, mesuré). ⑤ SORTIE — Aucune ; range la sortie du pas sous ctx["sortie_du_pas"].
    ⑥ TRAITEMENT — Six soirées (la sixième : le second signal hors contrat, attendu neutre) ; chacune remet le
    fichier des signaux et les positions, appelle
    `tenir_pour_de_vrai`, lit le code, les positions écrites et `GITHUB_OUTPUT`. ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecteur du tour 1 (D2, D3 B) : le code 1 et la mise à part n'étaient éprouvés par aucun cas.
    Le dernier filet : `mettre_a_part_les_cci_fautifs` neutralisée, une DepartageImpossible arrive à
    `tenir_pour_de_vrai`, qui doit rendre 1 sans rien écrire (et non une trace d'erreur).
    ⑨ CE QUI CLOCHE — `GITHUB_OUTPUT` est simulé par un fichier ; GitHub Actions lui-même n'est pas lancé.
    ⑩ EFFET — Écrit dans la copie temporaire seulement ; remplace le temps d'une soirée un attribut du module éprouvé.
    ⑪ TERMINAISON — Rend la main.
    """
    TP, copie = ctx["TP"], ctx["copie"]
    if copie is None:
        raise RuntimeError("NON JOUÉ : la copie du 2026-10-20 n'a pas pu être préparée : %s" % ctx["copie_raison"])
    f_sig = os.path.join(copie, "donnees", "signaux_du_jour.json")
    f_pos = os.path.join(copie, "donnees", "claude_positions_ouvertes.csv")
    bruts = ctx["signaux_du_soir"]
    assert [(s["valeur"], s["cci"]) for s in bruts["signaux"]] == [("ENGIE", -57.03), ("EIFFAGE", -166.47)], bruts

    def soiree(modifier, neutraliser=False):
        d = json.loads(json.dumps(bruts))
        modifier(d["signaux"])
        with open(f_sig, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)
        with open(f_pos, "w", encoding="utf-8") as fh:
            fh.write(ctx["positions_vides"])
        f_out = os.path.join(ctx["dossier"], "github_output.txt")
        open(f_out, "w").close()
        os.environ["GITHUB_OUTPUT"] = f_out
        garde = TP.mettre_a_part_les_cci_fautifs
        if neutraliser:
            TP.mettre_a_part_les_cci_fautifs = lambda sg: (sg, [])
        tampon = io.StringIO()
        # Le compteur du calibrage n'est jamais remis à zéro (⑨ de `_dire`, défaut consigné) : un second calibrage
        # dans le même processus échoue. Chaque soirée est un soir neuf : on remet le compteur, rien d'autre.
        TP._dire.appels = 0
        try:
            with contextlib.redirect_stdout(tampon):
                code = TP.tenir_pour_de_vrai(copie)
        finally:
            TP.mettre_a_part_les_cci_fautifs = garde
            del os.environ["GITHUB_OUTPUT"]
        sortie = dict(l.split("=", 1) for l in open(f_out, encoding="utf-8").read().split("\n") if "=" in l)
        with open(f_pos, encoding="utf-8", newline="") as fh:
            pos = [(r["strategie"], r["valeur"], r["comptabilite"]) for r in csv.DictReader(fh)]
        return code, sortie, pos, tampon.getvalue()

    # ① sans faute : R-207bis donne EIFFAGE à OBS (main donnait ENGIE) ; rien n'est mis à part
    code, sortie, pos, txt = soiree(lambda l: None)
    ctx["sortie_du_pas"] = sortie
    assert code == 0, (code, [l for l in txt.splitlines() if "CODE" in l or "ECHEC" in l or "❌" in l][:5])
    assert sortie.get("signaux_mis_a_part") == "0" and sortie.get("positions_signalees") == "0", sortie
    assert ("C5E10-OBS-V1", "EIFFAGE", "un_jeton") in pos and ("C5E10-OBS-V1", "ENGIE", "un_jeton") not in pos, pos
    assert ("C5E10-QA-V1", "EIFFAGE", "un_jeton") in pos, pos
    # ② NaN sur ENGIE : OBS seule est mise à part (ses deux signaux), QA ouvre EIFFAGE, code 0
    code, sortie, pos, txt = soiree(lambda l: l[0].update(cci=float("nan")))
    assert code == 0, (code, txt[-600:])
    assert sortie.get("signaux_mis_a_part") == "2", sortie
    assert not [p for p in pos if p[0] == "C5E10-OBS-V1"], pos
    assert ("C5E10-QA-V1", "EIFFAGE", "un_jeton") in pos and "MIS A PART" in txt, (pos, txt[-600:])
    # ③ un seul signal, CCI null : les deux stratégies qui le reçoivent sont mises à part, rien ne s'ouvre
    code, sortie, pos, txt = soiree(lambda l: (l.pop(0), l[0].update(cci=None)))
    assert code == 0 and sortie.get("signaux_mis_a_part") == "2" and pos == [], (code, sortie, pos)
    # ④ CCI retiré des deux signaux (cas D1 du relecteur : avant, code 0 et ENGIE en un jeton, sans un mot)
    code, sortie, pos, txt = soiree(lambda l: [x.pop("cci") for x in l])
    assert code == 0 and sortie.get("signaux_mis_a_part") == "3" and pos == [], (code, sortie, pos)
    # ⑥ le SECOND signal porte un champ hors contrat (« date ») : il est LU — le message est affiché, et EIFFAGE n'est
    # ouvert pour aucune stratégie. ATTENDU NEUTRE (superviseur R-759 du tour 2, n-3) : ni « code 1 » ni « aucune
    # position écrite », car « faute du fichier » (tout s'arrête, comme depuis le 13-09-2026) ou « faute de la ligne »
    # (mise à part, comme le CCI) est une question posée à Jean-Luc.
    code, sortie, pos, txt = soiree(lambda l: l[1].update(date="2026-10-20"))
    assert "NE RESPECTE PAS SON CONTRAT" in txt, txt[-400:]
    assert not [p for p in pos if p[1] == "EIFFAGE"], pos
    # ⑤ le dernier filet : mise à part neutralisée, NaN sur ENGIE -> code 1, rien d'écrit, message nommé
    code, sortie, pos, txt = soiree(lambda l: l[0].update(cci=float("nan")), neutraliser=True)
    assert code == 1 and pos == [] and "PANNE DU DEPARTAGE" in txt, (code, pos, txt[-400:])


def noms_lus_et_ecrits(texte_yaml, sortie_du_pas):
    """Compare les noms `steps.tenir_les_positions.outputs.X` lus par le circuit aux noms que le teneur a écrits.

    ① RÔLE — La propriété du cas T10. ② CONTEXTE D'APPEL — T10, deux fois (le vrai fichier, et le calibrage).
    ③ ENTRÉE — le texte du YAML · le dictionnaire de la sortie du pas écrite par le teneur. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : les noms lus jamais écrits · les noms écrits jamais lus. ⑥ TRAITEMENT — Expression
    régulière sur le YAML ; différences d'ensembles. ⑦ UNITÉ — — ⑧ POURQUOI — Une faute de frappe dans un `if:` rend
    le soir VERT en silence (superviseur R-759 du 14-11-2026, D2 ②). ⑨ CE QUI CLOCHE — Ne lit que les noms écrits
    ce soir-là : un nom écrit sous condition seulement échapperait. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    import re
    lus = set(re.findall(r"steps\.tenir_les_positions\.outputs\.([A-Za-z0-9_]+)", texte_yaml))
    ecrits = set(sortie_du_pas)
    return sorted(lus - ecrits), sorted(ecrits - lus)


@cas
def T10_le_circuit_lit_les_noms_que_le_teneur_ecrit(ctx):
    """Chaque `steps.tenir_les_positions.outputs.X` lu par `collecte_abc.yml` est un nom réellement écrit par le teneur
    dans `GITHUB_OUTPUT` (sortie de la soirée T09), et réciproquement.

    ① RÔLE — Empêcher que la mise à part soit verte aux épreuves et muette sur GitHub. ② CONTEXTE D'APPEL — `main`,
    après T09. ③ ENTRÉE — `ctx`. ④ CONDITIONS D'ENTRÉE — T09 a tourné. ⑤ SORTIE — Aucune.
    ⑥ TRAITEMENT — ① calibrer SUR LE YAML D'ORIGINE (`ctx["yaml_original"]`, jamais saboté) : un YAML où
    `signaux_mis_a_part` est mal écrit doit mordre, le vrai nom `positions_signalees` ne doit pas ; la garde partagée
    doit voir la condition inversée de chaque nom écrit · ② appliquer au fichier joué (`ctx["yaml_texte"]`, saboté
    sous Y1 à Y13) les deux contrôles — noms lus contre noms écrits, et la garde
    `GARDE_DU_PAS_ROUGE.garde_du_pas_rouge` pour chaque nom écrit — et réunir TOUS les manques dans un seul message,
    une ligne chacun. ⑦ UNITÉ — — ⑧ POURQUOI — Superviseur R-759 du 14-11-2026, D3. Le calibrage se fait sur
    l'original depuis la relecture Cowork du 15-11-2026 (b-2) : fait sur le YAML déjà saboté, il tombait AVANT que la
    garde ne lise le fichier, et « Y1 MORD (T10) » ne prouvait pas que la garde voit une condition inversée. Les
    manques réunis permettent à `main` de vérifier que chaque sabotage mord pour SA raison. ⑨ CE QUI CLOCHE — Voir
    `noms_lus_et_ecrits`. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    sortie = ctx.get("sortie_du_pas")
    if not sortie:
        raise RuntimeError("NON JOUÉ : T09 n'a pas rendu la sortie du pas")
    origine, texte = ctx["yaml_original"], ctx["yaml_texte"]
    faux = origine.replace("outputs.signaux_mis_a_part", "outputs.signaux_mis_apart")
    assert faux != origine and noms_lus_et_ecrits(faux, sortie)[0] == ["signaux_mis_apart"], "calibrage : ne mord pas"
    assert "positions_signalees" not in noms_lus_et_ecrits(faux, sortie)[0]
    # LA FORME DE CHAQUE PAS ROUGE, par la garde partagée, pour CHAQUE nom écrit (lu, pas épelé : une troisième sortie
    # serait gardée sans retouche). Calibrage d'abord, sur l'original : la garde doit mordre sur une condition inversée.
    G = ctx["G"]
    for nom in sorted(sortie):
        inv = origine.replace("outputs.%s != '0'" % nom, "outputs.%s == '0'" % nom)
        assert inv != origine and G.garde_du_pas_rouge(inv, nom, "programmes/TENIR_LES_POSITIONS.py"), \
            "calibrage : la garde ne voit pas la condition inversée de %s" % nom
    manques = []
    lus_non_ecrits, ecrits_non_lus = noms_lus_et_ecrits(texte, sortie)
    if lus_non_ecrits or ecrits_non_lus:
        manques.append("noms lus jamais écrits %s · noms écrits jamais lus %s · sortie %s"
                       % (lus_non_ecrits, ecrits_non_lus, sortie))
    for nom in sorted(sortie):
        manques += ["%s : %s" % (nom, m) for m in G.garde_du_pas_rouge(texte, nom, "programmes/TENIR_LES_POSITIONS.py")]
    assert not manques, "\n".join(manques)


@cas
def T11_precision_du_tri(ctx):
    """Cas C : B à −120,4 et A à −120,1 → B. Un tri sur le CCI arrondi à l'entier les rendrait égaux et donnerait A.

    ① RÔLE — Fixer la précision du tri. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `ctx`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune. ⑥ TRAITEMENT — Un départage. ⑦ UNITÉ — CCI sans unité. ⑧ POURQUOI — Relecteur du tour 1, D3 C.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    TP = ctx["TP"]
    rendu = TP.departager_r207bis([sig("S", "A", -120.1), sig("S", "B", -120.4)])
    assert [s["valeur"] for s in rendu] == ["B", "A"], rendu


@cas
def T12_la_garde_voit_chaque_forme_fautive_pour_sa_raison(ctx):
    """Chaque sabotage du YAML de la liste `SABOTAGES` (Y1 à Y13), appliqué au YAML d'ORIGINE, fait dire à la garde
    partagée SA raison attendue, absente sur l'original.

    ① RÔLE — Donner des dents à CHAQUE condition de `GARDE_DU_PAS_ROUGE.garde_du_pas_rouge` : retirer une condition de
    la garde fait tomber ce cas en nommant la forme fautive qu'elle ne voit plus (sabotages S34 à S43).
    ② CONTEXTE D'APPEL — `main`, par `jouer`, sur l'original et sous chaque sabotage. ③ ENTRÉE — `ctx` : `G` (la garde,
    éventuellement sabotée), `yaml_original`. ④ CONDITIONS D'ENTRÉE — `SABOTAGES` est défini (fin du module).
    ⑤ SORTIE — Aucune ; lève AssertionError dont le message nomme, une ligne chacune, les formes fautives que la garde
    ne voit plus. ⑥ TRAITEMENT — Pour chaque entrée de `SABOTAGES` de cible « YAML » qui porte une raison : ① la
    raison est ABSENTE des manques de la garde sur l'original (sinon elle ne distingue rien) · ② le sabotage est
    appliqué à l'original par `appliquer` · ③ la raison est PRÉSENTE dans les manques de la garde sur le sabotage,
    pour la sortie `signaux_mis_a_part`. ⑦ UNITÉ — — ⑧ POURQUOI — Relecture Cowork du 15-11-2026 à 17h46 (N-1 de la
    partie A, B-1 de la partie B, mesuré par exécution) : quatre conditions de la garde (place après tout pas sans
    `always()`, « Tenir » qui précède, « Tenir » qui lance le teneur, `continue-on-error` sur « Tenir ») pouvaient être
    retirées sans qu'aucune des deux épreuves ne rougisse ; R-731 : une épreuve qui reste verte quand on retire ce
    qu'elle teste est une décoration. Sous un sabotage du YAML, T10 tombe ; T12, qui part de l'original, tient : les
    deux rôles ne se masquent pas. ⑨ CE QUI CLOCHE — Ne joue que `signaux_mis_a_part` (la sortie que les sabotages Y
    visent) ; `positions_signalees` passe par la même fonction, gardée par T10 et par V10f de la vente unique.
    ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ; lève RuntimeError (cas NON JOUÉ, code 2) si le texte visé par
    un sabotage n'est pas trouvé une fois dans l'original.
    """
    G, origine = ctx["G"], ctx["yaml_original"]
    prog = "programmes/TENIR_LES_POSITIONS.py"
    sur_l_origine = G.garde_du_pas_rouge(origine, "signaux_mis_a_part", prog)
    aveugles = []
    for nom, cible, avant, apres, raison in SABOTAGES:
        if cible != "YAML" or not raison:
            continue
        if origine.count(avant) != 1:
            raise RuntimeError("texte visé par %s trouvé %d fois dans le YAML" % (nom, origine.count(avant)))
        if any(raison in m for m in sur_l_origine):
            aveugles.append("%s : la raison « %s » est déjà dite sur le YAML d'origine" % (nom, raison))
            continue
        manques = G.garde_du_pas_rouge(appliquer(origine, avant, apres), "signaux_mis_a_part", prog)
        if not any(raison in m for m in manques):
            aveugles.append("%s : la garde ne dit plus « %s » (elle dit %s)" % (nom, raison, manques))
    assert not aveugles, "\n".join(aveugles)


def preparer_la_soiree(racine, dossier):
    """Copie le dépôt sans ce qui est lourd, tronque les cours au 2026-10-20, vide les positions, lance le VRAI
    détecteur ; rend (copie, signaux du soir, positions vides) ou lève.

    ① RÔLE — Le décor de T09. ② CONTEXTE D'APPEL — `preparer`. ③ ENTRÉE — la racine, un dossier temporaire.
    ④ CONDITIONS D'ENTRÉE — `donnees/cours_maitre.csv` couvre le 2026-10-20. ⑤ SORTIE — TROIS valeurs.
    ⑥ TRAITEMENT — ① copier sans .git, etudes, archives, sources brutes · ② garder les lignes de cours jusqu'au
    2026-10-20 · ③ positions : l'en-tête seul · ④ `DETECTER_LES_SIGNAUX_GITHUB.py <copie>` en sous-processus, code 0
    exigé · ⑤ lire le fichier des signaux. ⑦ UNITÉ — — ⑧ POURQUOI — Rejouer un soir réel hors soir de séance, sur une
    copie (A-643 ① : jamais un soir de séance, jamais sur le dépôt). ⑨ CE QUI CLOCHE — Le détecteur réécrit d'autres
    fichiers de la copie ; sans effet ici. ⑩ EFFET — Écrit dans le dossier temporaire ; lance un sous-processus.
    ⑪ TERMINAISON — Rend la main ; lève RuntimeError si le détecteur échoue.
    """
    copie = os.path.join(dossier, "depot")
    shutil.copytree(racine, copie, ignore=shutil.ignore_patterns(
        ".git", "etudes", "archives", "sources_bnains", "sources_yahoo", "sources_francfort", "__pycache__"))
    f_c = os.path.join(copie, "donnees", "cours_maitre.csv")
    with open(f_c, encoding="utf-8", newline="") as fh:
        lignes = fh.read().split("\n")
    garde = [lignes[0]] + [l for l in lignes[1:] if l and l.split(",")[1] <= "2026-10-20"]
    with open(f_c, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(garde) + "\n")
    f_pos = os.path.join(copie, "donnees", "claude_positions_ouvertes.csv")
    with open(f_pos, encoding="utf-8") as fh:
        vides = fh.readline()
    with open(f_pos, "w", encoding="utf-8") as fh:
        fh.write(vides)
    r = subprocess.run([sys.executable, "-B", os.path.join(copie, "programmes", "DETECTER_LES_SIGNAUX_GITHUB.py"),
                        copie], capture_output=True, text=True, cwd=copie, timeout=600)
    if r.returncode != 0:
        raise RuntimeError("détecteur en code %d : %s" % (r.returncode, (r.stdout + r.stderr)[-400:]))
    d = json.load(open(os.path.join(copie, "donnees", "signaux_du_jour.json"), encoding="utf-8"))
    if d.get("seance") != "2026-10-20":
        raise RuntimeError("le détecteur a lu la séance %s, pas le 2026-10-20" % d.get("seance"))
    return copie, d, vides


def preparer(racine, indic):
    """Lit une fois ce que les cas partagent : référentiel, stratégies vivantes, vraies journées, module du rejeu.

    ① RÔLE — Le contexte. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine, le chemin du rejeu (ou None).
    ④ CONDITIONS D'ENTRÉE — Celles du programme. ⑤ SORTIE — UNE valeur : un dictionnaire.
    ⑥ TRAITEMENT — ① référentiel : onglet_google → mnémonique, comme `tenir_pour_de_vrai` · ② stratégies : fiches
    VIVANTES à univers non vide, la dernière ligne faisant foi (`fiches_du_registre`) · ③ le détecteur réel relit
    deux journées sur le fichier maître · ④ le rejeu (`MESURER_LES_INDICATEURS.py`), s'il est trouvé. ⑦ UNITÉ — —
    ⑧ POURQUOI — Le détecteur coûte quelques secondes : une seule lecture. ⑨ CE QUI CLOCHE — Voir ⑨ du programme.
    ⑩ EFFET — Exécute le code du détecteur et du rejeu (lecture seule). ⑪ TERMINAISON — Rend la main ; lève si le
    matériel manque.
    """
    prog = os.path.join(racine, "programmes")
    from CONTRATS_DES_FICHIERS import fiches_du_registre, REGISTRE_DES_STRATEGIES
    mnemo = {}
    with open(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv"),
              encoding="utf-8-sig", newline="") as fh:
        for l in csv.DictReader(fh):
            nom, code = (l.get("onglet_google") or "").strip().upper(), (l.get("mnemonique") or "").strip().upper()
            if nom and code:
                mnemo[nom] = code
    strategies = []
    for l in fiches_du_registre(os.path.join(racine, REGISTRE_DES_STRATEGIES)).values():
        if "VIVANTE" in (l.get("statut") or "") and (l.get("univers") or "").strip():
            strategies.append((l["id"], {m.strip().upper() for m in l["univers"].split(",") if m.strip()}))
    D = charger("epreuve_detecteur", os.path.join(prog, "DETECTER_LES_SIGNAUX_GITHUB.py"))
    B, mod, cours, lecture = D.charger(racine)
    jours = {j: D.signaux_de_la_seance(cours, lecture, B, mod, j)[0] for j in ("2025-10-07", "2026-05-18")}
    M = None
    if indic is None:
        p = os.path.join(prog, "MESURER_LES_INDICATEURS.py")
        indic = p if os.path.isfile(p) else None
    if indic:
        M = charger("epreuve_indic", indic)
    with open(os.path.join(racine, ".github", "workflows", "collecte_abc.yml"), encoding="utf-8") as fh:
        yaml_texte = fh.read()
    dossier = tempfile.mkdtemp(prefix="r207_soiree_")
    copie, signaux_du_soir, vides, raison = None, None, "", ""
    try:
        copie, signaux_du_soir, vides = preparer_la_soiree(racine, dossier)
    except Exception as e:  # noqa: BLE001 — dit par T09 (NON JOUÉ), jamais tu
        raison = "%s : %s" % (type(e).__name__, e)
    return {"racine": racine, "mnemo": mnemo, "strategies": strategies, "jours": jours, "M": M,
            "dossier": dossier, "copie": copie, "signaux_du_soir": signaux_du_soir, "positions_vides": vides,
            "copie_raison": raison, "G": GARDE_DU_PAS_ROUGE, "yaml_texte": yaml_texte, "yaml_original": yaml_texte}


def jouer(ctx, TP):
    """Joue tous les cas sur un module de tenue des positions ; rend (tenus, tombés, non joués).

    ① RÔLE — Un passage. ② CONTEXTE D'APPEL — `main`, une fois sur l'original et une fois par sabotage.
    ③ ENTRÉE — le contexte, le module. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — TROIS valeurs : listes de noms.
    ⑥ TRAITEMENT — Chaque cas ; AssertionError → tombé, message ENTIER gardé (la raison d'un sabotage s'y cherche ;
    `main` le coupe à l'affichage) ; toute autre exception → non joué. ⑦ UNITÉ — —
    ⑧ POURQUOI — Un cas qui plante n'est pas un cas qui tient. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    """
    ctx = dict(ctx, TP=TP)
    tenus, tombes, non_joues = [], [], []
    for c in CAS:
        try:
            c(ctx)
            tenus.append(c.__name__)
        except AssertionError as e:
            tombes.append((c.__name__, str(e)))
        except Exception as e:  # noqa: BLE001 — dit, jamais tu
            non_joues.append((c.__name__, "%s : %s" % (type(e).__name__, str(e)[:300])))
    return tenus, tombes, non_joues, ctx.get("lignes_golden", [])


def decouper_le_pas(source, avant):
    """Sépare d'un YAML de workflow le pas qui commence au texte `avant`, jusqu'au pas suivant.

    ① RÔLE — Outil des sabotages qui retirent ou déplacent un pas entier. ② CONTEXTE D'APPEL — `retirer_le_pas`,
    `tenir_apres_le_pas_rouge`, `pas_rouge_dans_un_job_a_part`. ③ ENTRÉE — le texte du YAML · le début exact du pas
    (« - name: … »). ④ CONDITIONS D'ENTRÉE — `avant` est présent, et un autre pas le suit. ⑤ SORTIE — DEUX valeurs :
    le YAML sans le pas · le texte du pas, ligne vide finale comprise. ⑥ TRAITEMENT — Coupe de `avant` jusqu'au
    prochain « \n      - name: ». ⑦ UNITÉ — — ⑧ POURQUOI — Un `if: false` ajouté ne suffit pas à retirer un pas : le
    `if` du pas, écrit plus bas, le remplacerait (clé YAML en double, la dernière gagne). ⑨ CE QUI CLOCHE — Ne sait
    pas couper le DERNIER pas du fichier (lève). ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ; lève ValueError si
    un des deux textes manque.
    """
    debut = source.index(avant)
    fin = source.index("\n      - name:", debut + len(avant)) + 1
    return source[:debut] + source[fin:], source[debut:fin]


def retirer_le_pas(source, avant):
    """Sabotage Y8 : le pas rouge retiré en entier. ① RÔLE — Remplacement d'un sabotage. ② CONTEXTE D'APPEL —
    `appliquer`. ③ ENTRÉE — le YAML, le début du pas. ④ CONDITIONS D'ENTRÉE — Celles de `decouper_le_pas`.
    ⑤ SORTIE — UNE valeur : le YAML saboté. ⑥ TRAITEMENT — `decouper_le_pas`, sans le pas. ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir `decouper_le_pas`. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    return decouper_le_pas(source, avant)[0]


ANCRE_DU_DERNIER_PAS = "      - name: Dire quels pas non bloquants sont tombes\n"


def tenir_apres_le_pas_rouge(source, avant):
    """Sabotage Y10 : le pas « Tenir » déplacé APRÈS le pas rouge, sous `if: always()`.

    ① RÔLE — Isoler la condition « Tenir précède le pas rouge » de la garde. ② CONTEXTE D'APPEL — `appliquer`.
    ③ ENTRÉE — le YAML, le début du pas « Tenir ». ④ CONDITIONS D'ENTRÉE — `ANCRE_DU_DERNIER_PAS` présente une fois.
    ⑤ SORTIE — UNE valeur : le YAML saboté. ⑥ TRAITEMENT — Coupe le pas, lui ajoute `if: always()` sous son id, le
    remet juste avant le dernier pas du job (« Dire quels pas non bloquants sont tombes »), donc après les pas rouges.
    ⑦ UNITÉ — — ⑧ POURQUOI — Sans `always()`, « Tenir » déplacé deviendrait aussi un pas sans `always()` placé
    après le pas rouge, et la garde dirait DEUX raisons. Cela ne masquerait rien : T12 cherche la raison PRÉCISE
    (« ne précède pas »), et retirer la condition « Tenir précède » la ferait disparaître, donc T12 tomberait quand
    même (mesuré par Cowork le 15-11-2026, a-1, en rejouant Y10 sans `always()` sous S36). `always()` rend seulement
    la forme fautive plus pure : la garde n'y dit QUE sa raison (relecture Cowork du 15-11-2026, N-1, cas Y10). Sur GitHub, la
    sortie de « Tenir » serait encore vide au moment du `if` du pas rouge : il ne tournerait jamais.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ; lève si une ancre manque.
    """
    sans, bloc = decouper_le_pas(source, avant)
    bloc = bloc.replace("        id: tenir_les_positions\n", "        id: tenir_les_positions\n        if: always()\n", 1)
    if sans.count(ANCRE_DU_DERNIER_PAS) != 1:
        raise ValueError("ancre du dernier pas trouvée %d fois" % sans.count(ANCRE_DU_DERNIER_PAS))
    return sans.replace(ANCRE_DU_DERNIER_PAS, bloc + ANCRE_DU_DERNIER_PAS)


def pas_rouge_dans_un_job_a_part(source, avant):
    """Sabotage Y13 : le pas rouge rangé dans un job à part (`needs: collecte`, `if: always()`), en fin de fichier.

    ① RÔLE — Isoler la condition « même job » de la garde. ② CONTEXTE D'APPEL — `appliquer`. ③ ENTRÉE — le YAML, le
    début du pas rouge. ④ CONDITIONS D'ENTRÉE — `jobs` est la dernière clé du fichier (vrai le 15-11-2026 : `jobs:`
    l. 36, aucune clé de premier niveau après). ⑤ SORTIE — UNE valeur : le YAML saboté. ⑥ TRAITEMENT — Coupe le pas,
    ajoute en fin de fichier le job `rougir_a_part` qui le porte. ⑦ UNITÉ — — ⑧ POURQUOI — Relecture Cowork du
    15-11-2026, c-1 : sur GitHub, `steps.*` n'existe que dans le job courant ; la sortie lue y vaut '' et le pas ne
    tourne jamais (déduit de la règle documentée, non mesuré sur GitHub). ⑨ CE QUI CLOCHE — Si une clé de premier
    niveau suivait `jobs`, le job ajouté tomberait sous elle. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    """
    sans, bloc = decouper_le_pas(source, avant)
    return (sans.rstrip("\n") + "\n\n  rougir_a_part:\n    needs: collecte\n    if: always()\n"
            "    runs-on: ubuntu-latest\n    steps:\n" + bloc)


def appliquer(source, avant, apres):
    """Applique un sabotage à un texte. ① RÔLE — Un seul geste pour `main` et pour T12 (deux implémentations d'une même
    chose divergent toujours, R-708). ② CONTEXTE D'APPEL — `main` (--saboter), T12. ③ ENTRÉE — le texte, le texte
    visé, le remplacement : une chaîne, ou une fonction (texte, visé) → texte. ④ CONDITIONS D'ENTRÉE — `avant` est
    présent une fois (vérifié par l'appelant). ⑤ SORTIE — UNE valeur : le texte saboté. ⑥ TRAITEMENT — Appel de la
    fonction, ou remplacement. ⑦ UNITÉ — — ⑧ POURQUOI — Voir ① . ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    """
    return apres(source, avant) if callable(apres) else source.replace(avant, apres)


# Les sabotages : (nom, cible, texte exact visé, remplacement, raison attendue). Cible « TP » :
# programmes/TENIR_LES_POSITIONS.py ; « YAML » : .github/workflows/collecte_abc.yml ; « GARDE » :
# tests/GARDE_DU_PAS_ROUGE.py. Le remplacement est une chaîne ou une fonction (texte, visé) → texte. La RAISON
# ATTENDUE (ou None) est un morceau de texte qui doit figurer dans le message d'un cas tombé : un sabotage qui fait
# tomber un cas pour une autre raison ne prouve pas ce qu'il prétend (relecture Cowork du 15-11-2026, b-2 : Y1 et S34
# mordaient par le calibrage de T10, pas par la garde lisant le YAML saboté). Pour Y1 à Y13, c'est le manque que la
# garde doit dire ; pour S34 à S43 (une condition retirée ou faussée dans la garde), c'est le NOM du sabotage Y que T12 voit
# devenir invisible.
SABOTAGES = [
    ("S1 ordre de l'univers (départage retiré)", "TP",
     '    for sg in departager_r207bis(signaux):',
     '    for sg in list(signaux):', None),
    ('S2 CCI le plus HAUT', "TP",
     'key=lambda i: (ccis[i], str(signaux[i].get("valeur") or "")))',
     'key=lambda i: (-ccis[i], str(signaux[i].get("valeur") or "")))', None),
    ('S3 alphabétique seul', "TP",
     'key=lambda i: (ccis[i], str(signaux[i].get("valeur") or "")))',
     'key=lambda i: str(signaux[i].get("valeur") or ""))', None),
    ("S4 égalité laissée à l'ordre reçu", "TP",
     'key=lambda i: (ccis[i], str(signaux[i].get("valeur") or "")))',
     'key=lambda i: ccis[i])', None),
    ("S5 l'adaptateur perd le CCI", "TP",
     '"date_signal": sg["date_signal"], "cci": sg.get("cci")})',
     '"date_signal": sg["date_signal"]})', None),
    ("S6 CCI absent rangé en fin de liste au lieu d'être refusé", "TP",
     '    if x is None or (isinstance(x, str) and not x.strip()):\n        raise DepartageImpossible(',
     "    if x is None or (isinstance(x, str) and not x.strip()):\n        return float('inf')\n        raise DepartageImpossible(", None),
    ('S7 NaN accepté', "TP",
     '    if not math.isfinite(v):',
     '    if False:', None),
    ('S8 mise à part retirée du soir', "TP",
     '    traduits, _cci_a_part = mettre_a_part_les_cci_fautifs(traduits)',
     '    _cci_a_part = []', None),
    ('S9 places des stratégies non gardées (tri global)', "TP",
     '    ccis = [_cci_du_signal(sg) for sg in signaux]\n',
     "    signaux = sorted(signaux, key=lambda s: str(s.get('valeur')))\n    ccis = [_cci_du_signal(sg) for sg in signaux]\n", None),
    ('S10 seul le signal fautif mis à part (pas toute la stratégie)', "TP",
     '    gardes = [sg for sg in signaux if sg.get("strategie") not in raisons]',
     '    gardes = [sg for sg in signaux if not any(sg.get("valeur") in r for r in raisons.get(sg.get("strategie"), []))]', None),
    ('S11 sortie du pas renommée dans le code seul', "TP",
     'signaux_mis_a_part=%d',
     'signaux_mis_apart=%d', None),
    ("S12 tri sur le CCI arrondi à l'entier", "TP",
     'key=lambda i: (ccis[i], str(',
     'key=lambda i: (round(ccis[i]), str(', None),
    ('S13 dernier filet retiré (exception non attrapée)', "TP",
     '    except DepartageImpossible as e:\n        # DERNIER FILET',
     '    except ZeroDivisionError as e:\n        # DERNIER FILET', None),
    ("S14 la mise à part n'est pas comptée dans la sortie du pas", "TP",
     '    _n_mis_a_part = sum(len(_m["signaux"]) for _m in _cci_a_part)',
     '    _n_mis_a_part = 0', None),
    ('S15 contrat lu sur le seul premier signal', 'TP',
     '            for _sg in signaux:\n',
     '            for _sg in signaux[:1]:\n', None),
        ('Y1 pas rouge : condition inversée', 'YAML',
     "        if: always() && steps.tenir_les_positions.outputs.signaux_mis_a_part != '' && steps.tenir_les_positions.outputs.signaux_mis_a_part != '0'\n",
     "        if: always() && steps.tenir_les_positions.outputs.signaux_mis_a_part != '' && steps.tenir_les_positions.outputs.signaux_mis_a_part == '0'\n",
     "if du pas rouge de « signaux_mis_a_part »"),
    ('Y2 pas rouge : always() retiré', 'YAML',
     "        if: always() && steps.tenir_les_positions.outputs.signaux_mis_a_part != '' && steps.tenir_les_positions.outputs.signaux_mis_a_part != '0'\n",
     "        if: steps.tenir_les_positions.outputs.signaux_mis_a_part != '' && steps.tenir_les_positions.outputs.signaux_mis_a_part != '0'\n",
     "if du pas rouge de « signaux_mis_a_part »"),
    ('Y3 pas rouge : exit 0', 'YAML',
     'prise sans regarder la suite des cours)"\n          exit 1\n',
     'prise sans regarder la suite des cours)"\n          exit 0\n',
     "0 pas rouge(s) pour « signaux_mis_a_part »"),
    ('Y4 pas rouge en continue-on-error', 'YAML',
     '        id: rougir_si_des_signaux_ont_ete_mis_a_part\n',
     '        id: rougir_si_des_signaux_ont_ete_mis_a_part\n        continue-on-error: true\n',
     "le pas rouge de « signaux_mis_a_part » ou son job porte continue-on-error"),
    ('Y5 job du pas rouge en continue-on-error', 'YAML',
     '  collecte:\n    runs-on:',
     '  collecte:\n    continue-on-error: true\n    runs-on:',
     "le pas rouge de « signaux_mis_a_part » ou son job porte continue-on-error"),
    ('Y6 id renommé côté if', 'YAML',
     "        if: always() && steps.tenir_les_positions.outputs.signaux_mis_a_part != '' && steps.tenir_les_positions.outputs.signaux_mis_a_part != '0'\n",
     "        if: always() && steps.tenir_positions.outputs.signaux_mis_a_part != '' && steps.tenir_positions.outputs.signaux_mis_a_part != '0'\n",
     "0 pas portent l'id « tenir_positions »"),
    ('Y7 Tenir sauté par un if', 'YAML',
     '        id: tenir_les_positions\n',
     '        id: tenir_les_positions\n        if: false\n',
     "le pas « tenir_les_positions » porte un if autre que always()"),
    ('Y8 pas rouge retiré', 'YAML',
     '      - name: Rougir si des signaux ont ete mis a part\n',
     retirer_le_pas,
     "0 pas rouge(s) pour « signaux_mis_a_part »"),
    # Y9 à Y13 : une forme fautive par condition de la garde jusque-là sans sabotage (relecture Cowork du
    # 15-11-2026, N-1, B-1, c-1). Chacune ne fait dire à la garde QUE sa raison : retirer cette condition de la garde
    # (S35 à S39) la rend invisible, et T12 le dit.
    ('Y9 un pas sans always() ajouté après le pas rouge', 'YAML',
     ANCRE_DU_DERNIER_PAS,
     '      - name: Pas ajoute sans always\n        run: echo ajoute\n\n' + ANCRE_DU_DERNIER_PAS,
     "précède un pas sans always()"),
    ('Y10 Tenir déplacé après le pas rouge (sous always())', 'YAML',
     '      - name: Tenir les positions\n',
     tenir_apres_le_pas_rouge,
     "le pas « tenir_les_positions » ne précède pas le pas rouge"),
    ('Y11 Tenir ne lance plus le teneur', 'YAML',
     'run: python3 programmes/TENIR_LES_POSITIONS.py "$GITHUB_WORKSPACE"',
     'run: python3 programmes/TENIR_LES_POSITIONS_ANCIEN.py "$GITHUB_WORKSPACE"',
     "le pas « tenir_les_positions » ne lance pas programmes/TENIR_LES_POSITIONS.py"),
    ('Y12 Tenir seul en continue-on-error', 'YAML',
     '        id: tenir_les_positions\n',
     '        id: tenir_les_positions\n        continue-on-error: true\n',
     "le pas « tenir_les_positions » ou son job porte continue-on-error"),
    ('Y13 pas rouge dans un job à part', 'YAML',
     '      - name: Rougir si des signaux ont ete mis a part\n',
     pas_rouge_dans_un_job_a_part,
     "ne sont pas dans le même job"),
    ('S34 garde partagée faussée (même sabotage que dans la vente unique)', 'GARDE',
     'outputs.%s != \'0\'"',
     'outputs.%s == \'0\'"',
     'Y1 pas rouge : condition inversée'),
    # S35 à S39 : chaque condition de la garde jusque-là sans dents, RETIRÉE ; T12 doit nommer la forme Y devenue
    # invisible (relecture Cowork du 15-11-2026, B-1 : « exiger qu'au moins un sabotage NE MORDE PLUS »).
    ('S35 garde sans la condition « place après tout pas sans always() »', 'GARDE',
     '    if sans_always and r < max(sans_always):\n',
     '    if False and sans_always and r < max(sans_always):\n',
     'Y9 un pas sans always() ajouté après le pas rouge'),
    ('S36 garde sans la condition « Tenir précède le pas rouge »', 'GARDE',
     '    if t >= r:\n',
     '    if False and t >= r:\n',
     'Y10 Tenir déplacé après le pas rouge'),
    ('S37 garde sans la condition « Tenir lance le teneur »', 'GARDE',
     '    if programme not in str(pas[t].get("run", "")):\n',
     '    if False and programme not in str(pas[t].get("run", "")):\n',
     'Y11 Tenir ne lance plus le teneur'),
    ('S38 garde sans la condition « continue-on-error sur Tenir »', 'GARDE',
     '    if _neutralise(t):\n',
     '    if False and _neutralise(t):\n',
     'Y12 Tenir seul en continue-on-error'),
    ('S39 garde sans la condition « même job »', 'GARDE',
     '    if job_du_pas[t] is not job_du_pas[r]:\n',
     '    if False and job_du_pas[t] is not job_du_pas[r]:\n',
     'Y13 pas rouge dans un job à part'),
    # S40 à S43 : les conditions de la garde déjà gardées par un sabotage Y, retirées à leur tour : T12 doit nommer
    # la forme devenue invisible (même critère que S35 à S39 ; la famille de N-1, refaite sur toute la garde).
    ('S40 garde sans la forme exacte du if', 'GARDE',
     '    if _if(pas[r]) != canonique:\n',
     '    if False and _if(pas[r]) != canonique:\n',
     'Y1 pas rouge : condition inversée'),
    ('S41 garde sans la condition « continue-on-error sur le pas rouge »', 'GARDE',
     '    if _neutralise(r):\n',
     '    if False and _neutralise(r):\n',
     'Y4 pas rouge en continue-on-error'),
    ('S42 garde sans la condition « Tenir sans autre if que always() »', 'GARDE',
     '    if _if(pas[t]) not in ("", "always()"):\n',
     '    if False and _if(pas[t]) not in ("", "always()"):\n',
     'Y7 Tenir sauté par un if'),
    ('S43 garde sans la condition « exit 1 en dernière ligne »', 'GARDE',
     'if motif.search(_if(x)) and _derniere_ligne(x) == "exit 1"]',
     'if motif.search(_if(x))]',
     'Y3 pas rouge : exit 0'),
]


def main():
    """Joue les cas, puis, avec --saboter, chaque sabotage ; rend le code de sortie.

    ① RÔLE — Le verdict. ② CONTEXTE D'APPEL — Ligne de commande. ③ ENTRÉE — `sys.argv`.
    ④ CONDITIONS D'ENTRÉE — Celles du programme. ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
    ⑥ TRAITEMENT — ① lire le rejeu (chemin, ou révision Git copiée puis effacée) et préparer · ② jouer sur l'original · ③ avec --saboter, pour chaque sabotage : vérifier que le
    texte visé existe UNE fois (sinon le sabotage ne prouve rien : code 2), écrire la copie sabotée dans un dossier
    temporaire, la charger, jouer, exiger au moins un cas tombé et, si le sabotage porte une raison attendue, qu'elle
    figure dans le message d'un cas tombé (sinon code 1 : il mord pour une autre raison) ; effacer la copie, fichier
    par fichier.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit et efface des fichiers temporaires ; affiche. ⑪ TERMINAISON — Rend le code.
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    racine = os.path.realpath(args[0] if args else ".")
    indic = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--indic=")), None)
    rev = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--indic-git=")), None)
    copie_indic = None
    if rev and not indic:
        import subprocess
        r = subprocess.run(["git", "-C", racine, "show", rev + ":programmes/MESURER_LES_INDICATEURS.py"],
                           capture_output=True)
        if r.returncode != 0:
            print("CODE 2 — révision %s illisible : %s" % (rev, r.stderr.decode("utf-8", "replace").strip()[:200]))
            return 2
        fd, copie_indic = tempfile.mkstemp(prefix="r207_indic_", suffix=".py")
        with os.fdopen(fd, "wb") as fh:
            fh.write(r.stdout)
        indic = copie_indic
    saboter = "--saboter" in sys.argv[1:]
    prog = os.path.join(racine, "programmes")
    sys.path.insert(0, prog)
    f_tp = os.path.join(prog, "TENIR_LES_POSITIONS.py")
    try:
        ctx = preparer(racine, indic)
    finally:
        if copie_indic:
            os.remove(copie_indic)
    tenus, tombes, non_joues, lignes = jouer(ctx, charger("epreuve_tp", f_tp))
    for l in lignes:
        print("   golden · " + l)
    print("CAS : %d / %d tenus" % (len(tenus), len(CAS)))
    for n, e in tombes:
        print("   TOMBÉ %s : %s" % (n, e[:300]))
    for n, e in non_joues:
        print("   NON JOUÉ %s : %s" % (n, e))
    if non_joues:
        shutil.rmtree(ctx["dossier"], ignore_errors=True)
        print("CODE 2")
        return 2
    code = 0 if not tombes else 1
    if saboter:
        sources = {"TP": open(f_tp, encoding="utf-8").read(),
                   "YAML": ctx["yaml_texte"],
                   "GARDE": open(os.path.join(racine, "tests", "GARDE_DU_PAS_ROUGE.py"), encoding="utf-8").read()}
        tp_original = charger("epreuve_tp", f_tp)
        # La copie sabotée vit dans le `programmes/` de la copie du dépôt : le teneur cherche ses voisins (le juge
        # des stratégies) à côté de lui-même ; ailleurs, `tenir_pour_de_vrai` ne pourrait pas tourner, et T09 « planterait »
        # sous chaque sabotage sans rien prouver.
        a_effacer = ctx["copie"] is None
        dossier = tempfile.mkdtemp(prefix="r207_sabotage_") if a_effacer else os.path.join(ctx["copie"], "programmes")
        for nom, cible, avant, apres, raison in SABOTAGES:
            source = sources[cible]
            if source.count(avant) != 1:
                print("== %s : TEXTE VISÉ TROUVÉ %d FOIS — sabotage NON JOUÉ" % (nom, source.count(avant)))
                code = 2
                continue
            sabote = appliquer(source, avant, apres)
            if cible == "YAML":
                _t, tb, nj, _l = jouer(dict(ctx, yaml_texte=sabote), tp_original)
            else:
                f = os.path.join(dossier, "TP_sabote.py" if cible == "TP" else "GARDE_sabotee.py")
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(sabote)
                try:
                    if cible == "TP":
                        _t, tb, nj, _l = jouer(ctx, charger("epreuve_tp_sabote", f))
                    else:
                        _t, tb, nj, _l = jouer(dict(ctx, G=charger("epreuve_garde_sabotee", f)), tp_original)
                finally:
                    os.remove(f)
            mord = [n.split("_")[0] for n, _e in tb] + [n.split("_")[0] + "(plante)" for n, _e in nj]
            pour_sa_raison = raison is None or any(raison in e for _n, e in tb)
            if not mord:
                verdict = "NE MORD PAS"
            elif pour_sa_raison:
                verdict = "MORD (" + ", ".join(mord) + ")" + (" — raison vue : « %s »" % raison if raison else "")
            else:
                verdict = "MORD (%s) MAIS SANS LA RAISON ATTENDUE « %s »" % (", ".join(mord), raison)
            print("== %s : %s" % (nom, verdict))
            if (not mord or not pour_sa_raison) and code == 0:
                code = 1
        if a_effacer:
            os.rmdir(dossier)
    shutil.rmtree(ctx["dossier"], ignore_errors=True)
    print("CODE %d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())
