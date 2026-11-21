#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_NUIT_DECOUPEE — Ven 30-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que la certification de nuit découpée en tranches parallèles joue chaque épreuve une fois et une
  seule, que chaque tranche tient sous sa limite, et que la tâche finale rougit quand une tranche manque, est rouge,
  vient d'un autre passage ou n'a pas joué ce qu'elle devait.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py, qui joue toute épreuve de
  tests/) ; à la main avant toute livraison qui touche programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py ou la répartition de
  programmes/CERTIFIER_LA_VERSION.py (R-731) :
  python3 tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt (le fabricant et le certificateur sont pris dans son programmes/, les journaux des
  nuits dans son rapports/journal_du_circuit/).
④ CONDITIONS D'ENTRÉE — PyYAML et coverage installés (le circuit les installe) ; sinon code 2.
⑤ SORTIE — Le code de sortie : 0 si les cas N1 à N15, D1 et F0 à F9 donnent la réponse attendue et, avec --saboter, si
  chaque sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus ou si un module manque.
  [rend: 1]
⑥ TRAITEMENT — Sur une copie restreinte du dépôt (programmes, tests, fiches de circuit, journaux de certification) :
  N1 le fabricant écrit le circuit dans un dossier vide, code 0 · N2 le job « certifier » est une matrice des tranches
  1 à K, sans arrêt au premier échec (fail-fast: false), qui lance « --tranche ${{ matrix.tranche }}/K » ; le job
  « reunir » dépend de lui, tourne « always() » et lance « --reunir K », le même K · N3 chaque job a une limite
  (« timeout-minutes », 360 si absente, la valeur de GitHub) d'au plus 360 minutes · N4 la répartition faite par le
  certificateur (`repartir`, durées de `durees_relevees`) place chaque lancement dans exactement une tranche, et
  chaque fichier tests/*.py qu'aucun autre fichier de tests/ n'importe y figure (relevé ici par une autre rédaction
  que celle du certificateur) · N5 la charge prévue de chaque tranche ne dépasse pas le TIERS de sa limite · N6 le
  lancement d'une épreuve déclarée « series_hors_de_la_nuit » et sa vérification sont dans la même tranche.
  Puis sur un petit dépôt d'essai (un programme, trois épreuves, sa référence écrite par le certificateur) : les K
  tranches jouées pour de bon (passage « 777 »), puis la commande de la tâche finale, prise TELLE QU'ELLE EST ÉCRITE
  dans le circuit fabriqué et jouée par bash : F0 tout est là → 0, « VERSION CERTIFIÉE » et aucune « DÉRIVE » · F1 le certificat partiel
  d'une tranche VIDE effacé → non nul (aucun lancement n'y manque : seule la règle « il en manque un » le voit) · F1b
  celui d'une tranche pleine → non nul · F2 un autre passage → non nul · F3 une épreuve rouge dans un partiel → non nul · F4 un partiel
  qui se dit impossible → non nul · F5 un lancement joué par deux tranches → non nul · F6 un lancement joué par
  aucune → non nul · F7 une répartition différente → non nul · F8 un partiel d'une autre empreinte du code → non nul ·
  F9 un journal de CE passage aux durées extrêmes : la tranche relancée seule répartit comme ses sœurs (étalonné : vu
  d'un autre passage, il change la répartition). Et (31-10-2026) : N7 le pas « deposer » d'une tranche fait au moins
  autant d'essais de poussée qu'il y a de tranches · D1 `reunir_les_mesures` sur des mesures écrites à la main
  (intersection des lignes, des embranchements, des fonctions ; empreintes différentes écartées). Et (01-11-2026,
  relecture neuve, M8) : N8 la copie restreinte porte chaque fichier .py de chaque emplacement de code que le
  fabricant de la source publie (DOSSIERS_DE_CODE) — la copie ne garde pas sa propre liste. Et (09-11-2026, relecture
  de Cowork, B3-2) : N9 la coupure d'un lancement est le plus grand de son délai déclaré et de 3 × sa durée relevée,
  ce triple plafonné à 3 × DUREE_MAX_EPREUVE (relecture 4dcffa32, point 1 ; le délai déclaré n'est jamais raccourci)
  (`coupure`), et la boucle de jeu (`jouer_les_lancements`) la passe à `jouer` comme à `refaire_des_essais`. Et
  (09-11-2026, relecture de Cowork 4dcffa32, B3-9) : N10 `main` passe les durées relevées à cette boucle, en mode
  entier ET en mode tranche (voir `n10`). Et (15-11-2026, superviseur R-759 du 15-11-2026,
  etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/SUPERVISEUR_CERTIFICATION_Dim_15-11-2026.md) : N11 la
  sortie d'une épreuve rouge est gardée entière, celle d'une verte coupée à 3 lignes (`n11`) · N12 aucune épreuve de
  la nuit ne nomme un programme du dépôt rangé hors des dossiers gardés par le circuit (`n12`) ; et les sabotages Sm
  (6 tranches : N5 doit rougir), Sn, So, Sq (N11), St et Su (le filet du fabricant refuse une certification sans
  « ref: » ou sans le pas « meme_depot »), Sp (N12) — chacun doit faire tomber SON cas (ATTENDU). Et (15-11-2026,
  superviseur R-759, SUPERVISEUR_CERT3_Dim_15-11-2026.md, même dossier) : N13 la charge prévue d'un lancement est sa
  durée relevée, sinon son délai déclaré, sinon DUREE_MAX_EPREUVE, sur le vrai `repartir` (`n13`) ; N11 éprouve aussi
  une épreuve COUPÉE (sa sortie gardée, « ARRÊTÉE » en dernier) et les codes 2 et 124 ; sabotages Sh et Sv (N13),
  Sw et Sx (N11). Et (21-11-2026, A-961, décision de Jean-Luc du 21-11-2026 à 13h34) : N14 aucun sabotage perdu ni
  joué deux fois quand une épreuve est jouée en morceaux (`n14`, compte par une autre rédaction) · N15 le nombre de
  tranches est la largeur du réservoir des places longues, qui laisse 2 places au soir (`n15`) ; sabotages Sy (15
  tranches), Sz, Sz2, Sz3, Sz4, Sz5 (la découpe, la référence, la charge d'un morceau jamais joué).
⑦ UNITÉ — Des minutes (limites des jobs) et des secondes (charges).
⑧ POURQUOI — Décision de Jean-Luc du 30-10-2026 à 19h02 (réponse « 1 ») : « Couper la nuit en plusieurs tâches qui
  tournent en même temps, chacune avec ses propres 6 heures, plus une tâche finale qui réunit les résultats et dit
  rouge s'il en manque un. » La nuit du 29 au 30-10-2026, la certification d'un seul tenant a été coupée par sa
  limite de 330 minutes. Le tiers : les durées relevées ont varié du simple au double d'une nuit à l'autre (la série
  de la lecture des cours : 2 730 s, 4 379 s, 5 028 s les nuits du 23, du 24 et du 30-10-2026).
⑨ CE QUI CLOCHE — Le vrai GitHub Actions n'est pas joué : la matrice, « needs », « always() » et la limite sont lus
  dans le YAML, pas observés. Le pas « deposer » (poussée au dépôt privé, renommage du journal de la tranche) n'est
  pas joué. N5 dépend des journaux présents ; sur un dépôt sans journal (la copie jouée sur GitHub), des durées
  publiées (rapports/durees_des_epreuves_en_secondes.csv, A-968, décision de Jean-Luc du 21-11-2026 à 15h34) : des
  durées périmées y font une prévision périmée ; sans l'un ni l'autre, chaque lancement compte pour son délai.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné (120 s pour le fabricant et la tâche finale, 300 s pour
  une tranche du dépôt d'essai) ; sort par sys.exit.
  [sort: oui]
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
    import coverage  # noqa: F401  (le certificateur le demande pour jouer une tranche)
except ImportError as e:
    print(f"ARRÊT : module manquant ({e.name})")
    sys.exit(2)

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
CERTIF = "programmes/CERTIFIER_LA_VERSION.py"
CIRCUIT = ".github/workflows/certifier_la_version.yml"
LIMITE_DE_GITHUB = 360          # minutes : GitHub coupe toute tâche à 6 heures, et c'est aussi sa limite par défaut
TIERS = 3                       # une tranche ne prévoit pas plus du tiers de sa limite (voir ⑧)
PASSAGE = "777"
SABOTAGES = {
    "Z0": [],
    "S1_epreuve_retiree_de_la_repartition": [(CERTIF, "    for c in unites:\n", "    for c in unites[1:]:\n")],
    "S2_finale_sans_always": [(FAB, "    if: ${{ always() }}\n", "")],
    "S3_partiel_manquant_accepte": [(CERTIF,
        '            fautes.append(f"tranche {i} : certificat partiel absent ou illisible ({type(e).__name__})")\n',
        "            pass\n")],
    # S4 et S5 s'ancrent sur le COMMENTAIRE propre au job « certifier » : depuis le circuit des séries (fusion
    # 6c46ea65, 06-11-2026), le fabricant porte deux autres jobs avec « timeout-minutes: 330 » et « fail-fast: false »,
    # et l'ancre seule était trouvée 2 et 3 fois → « NE S'APPLIQUE PLUS », code 2 (diagnostic de l'examen 42384101504,
    # 08-11-2026). L'ancre reste unique dans la version du bloc 2 (travail-relais-des-series, e50dd73c).
    "S4_tranche_a_400_minutes": [(FAB, "    # 330 minutes PAR TRANCHE : GitHub coupe toute tâche à 6 heures ; chaque tranche a les siennes.\n"
                                      "    timeout-minutes: 330\n",
                                      "    # 330 minutes PAR TRANCHE : GitHub coupe toute tâche à 6 heures ; chaque tranche a les siennes.\n"
                                      "    timeout-minutes: 400\n")],
    "S5_arret_au_premier_echec": [(FAB, "      # une tranche rouge n'arrête pas les autres : la tâche finale doit voir chacune\n"
                                       "      fail-fast: false\n",
                                       "      # une tranche rouge n'arrête pas les autres : la tâche finale doit voir chacune\n")],
    "S6_autre_passage_accepte": [(CERTIF, 'attendu = {"passage": passage, "nombre"', 'attendu = {"nombre"')],
    "S7_doublon_accepte": [(CERTIF, '("joué(s) par plusieurs tranches", doubles)', '("joué(s) par plusieurs tranches", [])')],
    "S8_partiel_impossible_accepte": [(CERTIF, '        elif p.get("impossible"):\n', '        elif False:\n')],
    # S9 s'ancre sur l'ÉLÉMENT « - certifier » de la liste des dépendances de « reunir » (unique au fabricant) : depuis
    # le 15-11-2026, « needs » s'écrit en liste à tirets, et l'ancre « needs: certifier » n'existait plus (B1 de Cowork).
    "S9_finale_sans_dependance": [(FAB, "      - certifier\n", "")],
    "S10_repartitions_differentes_acceptees": [(CERTIF, "if not fautes and len({p.get(\"repartition\") for p in lus}) != 1:",
                                                "if False:")],
    "S12_moins_d_essais_que_de_tranches": [(FAB, "ESSAIS_DE_POUSSEE = TRANCHES_DE_LA_NUIT + 3\n",
                                            "ESSAIS_DE_POUSSEE = TRANCHES_DE_LA_NUIT - 1\n")],
    "Sa_passage_en_cours_non_ecarte": [(CERTIF, "        if not m or (passage_exclu and m.group(1) == passage_exclu):\n",
                                        "        if not m:\n")],
    "Sb_union_des_lignes": [(CERTIF, 'set.intersection(*(set(x["lignes"]) for x in v))', 'set.union(*(set(x["lignes"]) for x in v))')],
    "Sc_empreinte_du_code_non_verifiee": [(CERTIF, ', "tranche": i, "empreinte_du_code": empreinte}', ', "tranche": i}')],
    "Sd_union_des_embranchements": [(CERTIF, 'set.intersection(*({tuple(p) for p in x["branches"]} for x in v))',
                                     'set.union(*({tuple(p) for p in x["branches"]} for x in v))')],
    # B3-2 et B3-4 (relecture de Cowork du 09-11-2026) : la coupure suit la durée relevée (N9), et la charge prévue d'un
    # lancement jamais joué est son DÉLAI DÉCLARÉ (N5 : sans lui, chaque lancement nouveau compterait 1 500 s).
    "Se_coupure_sans_le_max": [(CERTIF, "        return max(delai, min(FACTEUR_DE_COUPURE * durees[cle], FACTEUR_DE_COUPURE * DUREE_MAX_EPREUVE))\n",
                                "        return delai\n")],
    # Le plafond (relecture de Cowork 4dcffa32, point 1) : sans lui, la coupure triple à chaque nuit ; et appliqué au
    # délai déclaré, il couperait la série de la lecture des cours (10 800 s déclarées, 5 097 s relevées).
    "Sk_coupure_sans_plafond": [(CERTIF, "        return max(delai, min(FACTEUR_DE_COUPURE * durees[cle], FACTEUR_DE_COUPURE * DUREE_MAX_EPREUVE))\n",
                                 "        return max(delai, FACTEUR_DE_COUPURE * durees[cle])\n")],
    "Sl_plafond_sur_le_delai_declare": [(CERTIF, "        return max(delai, min(FACTEUR_DE_COUPURE * durees[cle], FACTEUR_DE_COUPURE * DUREE_MAX_EPREUVE))\n",
                                         "        return min(max(delai, FACTEUR_DE_COUPURE * durees[cle]), FACTEUR_DE_COUPURE * DUREE_MAX_EPREUVE)\n")],
    "Sf_jeu_coupe_au_seul_delai": [(CERTIF, "coupure(cle, delais, durees), lectures)",
                                    "delais.get(cle, DUREE_MAX_EPREUVE), lectures)")],
    "Sg_essais_coupes_au_seul_delai": [(CERTIF, "                                                         coupure(cle, delais, durees))\n",
                                        "                                                         delais.get(cle, DUREE_MAX_EPREUVE))\n")],
    "Sh_prevue_sans_le_delai_declare": [(CERTIF, "        return durees.get(cle, delais.get(cle, DUREE_MAX_EPREUVE))\n",
                                         "        return durees.get(cle, DUREE_MAX_EPREUVE)\n")],
    # B3-9 (relecture de Cowork du 09-11-2026, 4dcffa32) : `main` passe les durées relevées à la boucle de jeu, dans
    # les deux modes (N10) ; un « {} » à la place faisait revenir en silence la coupure au seul délai déclaré (B3-2).
    "Si_entier_sans_les_durees": [(CERTIF, "                                             series, durees_relevees(racine, passage))\n",
                                   "                                             series, {})\n")],
    "Sj_tranche_sans_les_durees": [(CERTIF, "a_jouer, delais, series,\n                                         durees)\n",
                                    "a_jouer, delais, series,\n                                         {})\n")],
    # 15-11-2026 (superviseur R-759 du 15-11-2026, etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/
    # SUPERVISEUR_CERTIFICATION_Dim_15-11-2026.md, §5) — chacun doit faire tomber le cas que dit ATTENDU, pas un autre :
    # le nombre de tranches revenu à 6, la valeur d'avant : au nombre écrit, N5 est vert ; il doit rougir (sinon N5 est une
    # décoration). L'ancre ne lit pas la valeur (A-896, 15 tranches : l'ancre « = 12 » ne s'appliquait plus)
    "Sm_six_tranches_comme_avant": [(FAB, "\nTRANCHES_DE_LA_NUIT = ", "\nTRANCHES_DE_LA_NUIT = 6  # ")],
    # réparation 8 : la sortie d'une épreuve rouge gardée entière (N11)
    "Sn_sortie_rouge_coupee_a_trois": [(CERTIF,
        "    return list(lignes) if code != 0 else list(lignes)[-LIGNES_D_UNE_EPREUVE_VERTE:]\n",
        "    return list(lignes)[-LIGNES_D_UNE_EPREUVE_VERTE:]\n")],
    "So_jouer_coupe_a_trois": [(CERTIF, "          garder=None):\n", "          garder=3):\n")],
    "Sq_boucle_sans_la_regle_de_coupe": [(CERTIF, "lignes_gardees(code, lignes)])", "lignes])")],
    # réparation 1b-β : la certification sans « ref: » (propriété ⑦ du filet), puis sans le pas qui vérifie HEAD (⑦ bis)
    # 18-11-2026 (A-896) : depuis A-891 (installé le 18-11-2026 à 02h44), les pas de départ du job « certifier » sont
    # « depart_certifier » : le texte de St s'y trouvait deux fois et celui de Su nulle part — les deux rendaient « NE
    # S'APPLIQUE PLUS » (code 2 au certificat du 18-11-2026 05h58). St retire « ref: » des DEUX appels, Su vise le job
    # « certifier » sous son nouveau nom.
    "St_certification_sans_ref": [(FAB, 'ref="${{ needs.preparer.outputs.sha }}", jeton_garde=True),\n', "jeton_garde=True),\n"),
                                  (FAB, 'ref="${{ needs.preparer.outputs.sha }}", jeton_garde=True)),\n', "jeton_garde=True)),\n")],
    "Su_certification_sans_meme_depot": [(FAB, "%(depart_certifier)s%(meme_depot)s%(logiciels)s",
                                          "%(depart_certifier)s%(logiciels)s")],
    # réparation 4 : un programme éprouvé remis hors des dossiers gardés (N12) ; « None » : un fichier créé dans la copie
    "Sp_programme_eprouve_hors_des_dossiers_gardes": [
        ("tests/EPREUVES_DE_L_INVENTAIRE_DES_VINGT_ANS_Mer_11-11-2026.py", 'PROGRAMME = os.path.join("etudes", "outils", "INVENTORIER_LES_VINGT_ANS.py")',
         'PROGRAMME = os.path.join("etudes", "HORS_DU_CODE", "INVENTORIER_LES_VINGT_ANS.py")'),
        ("etudes/HORS_DU_CODE/INVENTORIER_LES_VINGT_ANS.py", None, "# un programme éprouvé hors des dossiers gardés\n")],
    # 15-11-2026 (superviseur R-759, SUPERVISEUR_CERT3_Dim_15-11-2026.md, même dossier) : la charge prévue, priorités
    # inversées (le délai déclaré avant la durée relevée) — Sh et Sv doivent faire tomber N13 (§1)
    "Sv_prevue_priorites_inversees": [(CERTIF, "        return durees.get(cle, delais.get(cle, DUREE_MAX_EPREUVE))\n",
                                       "        return delais.get(cle, durees.get(cle, DUREE_MAX_EPREUVE))\n")],
    # A2 (§2) : une épreuve coupée perd toute sa sortie ; m1 (§3) : seul le code 1 garde toute la sortie
    "Sw_coupee_sans_sa_sortie": [(CERTIF, "        code, sortie = 124, lu + f\"\\nARRÊTÉE : plus de {delai} s\"\n",
                                  "        code, sortie = 124, f\"ARRÊTÉE : plus de {delai} s\"\n")],
    "Sx_seul_le_code_1_garde_tout": [(CERTIF,
        "    return list(lignes) if code != 0 else list(lignes)[-LIGNES_D_UNE_EPREUVE_VERTE:]\n",
        "    return list(lignes) if code == 1 else list(lignes)[-LIGNES_D_UNE_EPREUVE_VERTE:]\n")],
    "S11_epreuve_coupee_en_deux": [(CERTIF, "        groupes.setdefault(unite_de(l), []).append(l)\n",
                                    "        groupes.setdefault(cle_de(l[0], l[2]), []).append(l)\n"),
                                   (CERTIF, "    return [[l for l in lancements if unite_de(l) in choisies[i]] for i in range(nombre)], charges",
                                    "    return [[l for l in lancements if cle_de(l[0], l[2]) in choisies[i]] for i in range(nombre)], charges")],
    # 21-11-2026 (A-961, décision de Jean-Luc du 21-11-2026 à 13h34) : 15 tranches au lieu de la largeur du réservoir
    # (18) — N15 doit rougir ; un sabotage perdu à la découpe (le dernier de chaque morceau) — N14 doit rougir ; la
    # lecture des sabotages amputée du dernier — N14 doit rougir (son compte vient d'une autre rédaction) ; un morceau
    # retiré (le lancement entier rangé tel quel) — N14 doit rougir.
    "Sy_quinze_tranches": [(FAB, "\nTRANCHES_DE_LA_NUIT = LARGEUR_DES_CIRCUITS_LONGS\n",
                            "\nTRANCHES_DE_LA_NUIT = LARGEUR_DES_CIRCUITS_LONGS - 3\n")],
    "Sz_sabotage_perdu_a_la_decoupe": [(CERTIF, 'ARGUMENT_DES_SABOTAGES + ",".join(codes[i - 1::nombre])',
                                        'ARGUMENT_DES_SABOTAGES + ",".join(codes[i - 1::nombre][:-1])')],
    "Sz2_lecture_des_sabotages_amputee": [(CERTIF, '            return [k.value for k in n.value.keys if k.value != "Z0"]\n',
                                           '            return [k.value for k in n.value.keys if k.value != "Z0"][:-1]\n')],
    "Sz3_sans_la_decoupe": [(CERTIF, '        if "--saboter" in textes[f] and "tests/" + f in morceaux:\n',
                             '        if False:\n')],
    "Sz4_morceau_manquant_non_vu": [(CERTIF, "        if len(n) == 1 and vus == {f\"{i}/{next(iter(n))}\" for i in range(1, int(next(iter(n))) + 1)}:\n",
                                     "        if True:\n")],
    "Sz5_charge_sans_z0": [(CERTIF, "    return -(-duree_entiere * (k + 1) // (tous + 1))\n",
                            "    return -(-duree_entiere * k // tous)\n")],
}
# Le texte que doit porter au moins une faute de chacun de ces sabotages : un sabotage qui ne fait tomber qu'un AUTRE cas
# ne prouve pas que le sien regarde (15-11-2026 : à 6 tranches, seul N5 rougit ; à 1, F1 rougirait aussi).
ATTENDU = {"Sm_six_tranches_comme_avant": "N5 ", "Sn_sortie_rouge_coupee_a_trois": "N11 ",
           "So_jouer_coupe_a_trois": "N11 ", "Sq_boucle_sans_la_regle_de_coupe": "N11 ",
           "St_certification_sans_ref": "sans « ref: »", "Su_certification_sans_meme_depot": "SERIES_MEME_DEPOT",
           # la faute visée nomme l'épreuve sabotée : la table SABOTAGES de cette épreuve-ci écrit le même chemin, et
           # N12 la voit aussi dans la copie, où le fichier créé existe (mesuré le 15-11-2026)
           "Sp_programme_eprouve_hors_des_dossiers_gardes": "N12 tests/EPREUVES_DE_L_INVENTAIRE_DES_VINGT_ANS",
           # superviseur R-759 du 15-11-2026 (SUPERVISEUR_CERT3_Dim_15-11-2026.md) : Sh et Sv (§1), Sw (§2), Sx (§3)
           "Sh_prevue_sans_le_delai_declare": "N13 ", "Sv_prevue_priorites_inversees": "N13 ",
           "Sw_coupee_sans_sa_sortie": "N11 ", "Sx_seul_le_code_1_garde_tout": "N11 ",
           # A-961 (21-11-2026)
           "Sy_quinze_tranches": "N15 ", "Sz_sabotage_perdu_a_la_decoupe": "N14 ",
           "Sz2_lecture_des_sabotages_amputee": "N14 ", "Sz3_sans_la_decoupe": "N14 ",
           "Sz4_morceau_manquant_non_vu": "N14 ", "Sz5_charge_sans_z0": "N14 "}

# Le petit dépôt d'essai : un programme à trois fonctions, une épreuve par fonction (chacune exécute sa fonction par un
# sous-processus, comme les vraies épreuves exécutent leurs programmes).
PROGRAMME = "def a():\n    return 1\n\n\ndef b():\n    return 2\n\n\ndef c():\n    return 3\n"
EPREUVE = ("import os, subprocess, sys\nracine = sys.argv[1]\n"
           "r = subprocess.run([sys.executable, '-E', '-c', 'import sys; sys.path.insert(0, %r); import P; "
           "sys.exit(0 if P.{f}() else 1)' % os.path.join(racine, 'programmes')])\nsys.exit(r.returncode)\n")


def copier_le_necessaire(source, cible):
    """Copie ce que l'épreuve lit du dépôt dans un dossier jetable.

    ① RÔLE — Travailler sur une copie, que les sabotages peuvent modifier. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `source` : la racine · `cible` : un dossier vide. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien. [rend: rien]
    ⑥ TRAITEMENT — les *.py de chaque emplacement de code publié, lus dans DOSSIERS_DE_CODE du fabricant de la source
      (la racine, programmes/, tests/, etudes/outils/, tests/outils/ au 01-11-2026), tests/*.json, les fiches
      .github/workflows/*.yml, les journaux de certification de rapports/journal_du_circuit/, et le fichier des
      durées publiées (son chemin LU au certificateur de la source, DUREES_PUBLIEES : A-968, 21-11-2026), que
      `durees_relevees` lit quand les journaux manquent — sur GitHub, la copie jouée n'a pas de journaux.
    ⑦ UNITÉ — — ⑧ POURQUOI — Copier tout le dépôt (des milliers de fichiers) à chaque sabotage serait lent ; le
      fabricant et le certificateur n'en lisent pas davantage ici. Les emplacements sont LUS au fabricant, jamais
      épelés ici : relecture neuve du 01-11-2026 (M8), une seconde liste avait gardé les quatre anciens (R-708).
    ⑨ CE QUI CLOCHE — Un fichier lu ailleurs ne serait pas copié : le cas qui en a besoin rougirait. · Si la lecture
      de DOSSIERS_DE_CODE au fabricant échoue (fabricant absent, nom changé), l'épreuve sort en trace Python, code 1,
      et non 2 comme le ⑤ du programme le promet quand elle n'a pas pu juger : c'est rouge pour la certification
      (programmes/CERTIFIER_LA_VERSION.py compte rouge tout code non nul), seule l'étiquette est fausse. Mesuré par la
      relecture n° 2 du 04-11-2026 (m6, AttributeError, code 1). Aucun filet « code 2 » dans `main` : il rangerait
      sous « n'a pas pu juger » une vraie panne du fabricant (superviseur R-759 du même jour, tour 3).
    ⑩ EFFET — Charge le fabricant et le certificateur de la source (ils ne font que définir) ; écrit la copie. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    code = [(d, r".*\.(py|json)$" if d == "tests" else r".*\.py$")
            for d in charger(os.path.join(source, FAB)).DOSSIERS_DE_CODE]
    for dossier, motif in code + [(".github/workflows", r".*\.ya?ml$"),
                                  ("rapports/journal_du_circuit", r"^circuit_\d+_\d+_certifier.*\.log$")]:
        d = os.path.join(source, dossier)
        if not os.path.isdir(d):
            continue
        os.makedirs(os.path.join(cible, dossier), exist_ok=True)
        for f in os.listdir(d):
            if re.match(motif, f) and os.path.isfile(os.path.join(d, f)):
                shutil.copyfile(os.path.join(d, f), os.path.join(cible, dossier, f))
    publiees = charger(os.path.join(source, CERTIF)).DUREES_PUBLIEES
    if os.path.isfile(os.path.join(source, publiees)):
        os.makedirs(os.path.dirname(os.path.join(cible, publiees)), exist_ok=True)
        shutil.copyfile(os.path.join(source, publiees), os.path.join(cible, publiees))


def charger(chemin):
    """Charge un module depuis son fichier et le rend.

    ① RÔLE — Appeler les fonctions du certificateur de la copie (saboté ou non). ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le module.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sp = importlib.util.spec_from_file_location("CERTIF_%d" % abs(hash(chemin)), chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def certifier(certificateur, racine, *options, passage=PASSAGE, delai=300):
    """Lance le certificateur sur une racine et rend son code et sa sortie.

    ① RÔLE — Jouer une tranche ou écrire une référence sur le dépôt d'essai. ② CONTEXTE D'APPEL — `essai`.
    ③ ENTRÉE — `certificateur` : son chemin · `racine` · `options` · `passage` : GITHUB_RUN_ID · `delai` : secondes.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, la sortie. [rend: 2]
    ⑥ TRAITEMENT — subprocess, sans la configuration Git de la machine. ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Borné à `delai`. [sort: non]
    """
    env = dict(os.environ, GITHUB_RUN_ID=passage)
    r = subprocess.run([sys.executable, "-B", certificateur, racine] + list(options), capture_output=True, text=True,
                       timeout=delai, env=env)
    return r.returncode, r.stdout + r.stderr


def tests_lances(copie):
    """Rend les tests/*.py qu'aucun autre fichier de tests/ n'importe — la règle relue ici, par une autre rédaction.

    ① RÔLE — Dire quelles épreuves de tests/ doivent figurer dans une tranche, sans demander au certificateur.
    ② CONTEXTE D'APPEL — `tour`, N4. ③ ENTRÉE — `copie`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins « tests/X.py ». [rend: 1]
    ⑥ TRAITEMENT — chercher « import X » ou « from X import » dans le texte des autres fichiers.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une épreuve oubliée à la fois par la liste et par la répartition ne serait vue par
      aucune vérification qui demande la liste au certificateur lui-même.
    ⑨ CE QUI CLOCHE — Un import écrit autrement (importlib) n'est pas vu : le fichier serait compté comme épreuve.
    ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    noms = sorted(f for f in os.listdir(os.path.join(copie, "tests")) if f.endswith(".py"))
    textes = {f: open(os.path.join(copie, "tests", f), encoding="utf-8").read() for f in noms}
    importes = {f for f in noms for g, t in textes.items() if g != f
                and re.search(r"^\s*(import|from)\s+%s\b" % re.escape(f[:-3]), t, re.M)}
    return {"tests/" + f for f in noms if f not in importes}


def essai(copie, circuit, faux):
    """Joue F0 à F9 : les tranches sur un petit dépôt d'essai, puis la commande de la tâche finale.

    ① RÔLE — Prouver que la tâche finale rougit quand elle doit, en jouant SA commande telle qu'elle est écrite.
    ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `copie` : la copie (le certificateur y est pris) · `circuit` : le YAML
      fabriqué, lu · `faux` : la liste des fautes, complétée.
    ④ CONDITIONS D'ENTRÉE — N2 a trouvé les jobs. ⑤ SORTIE — Rien. [rend: rien]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥ (F0 à F9).
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Jusqu'à F8, le dépôt d'essai n'a pas de journal : la répartition y suit les délais (tous égaux) ;
      F9 en pose un, à la fin. F9 ne lit pas le code de sortie des deux tranches relancées (BACKLOG proposé).
    ⑩ EFFET — Écrit un dépôt d'essai jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    commande = next((p.get("run") for p in circuit["jobs"]["reunir"]["steps"] if p.get("id") == "certifier"), None)
    nombre = len(circuit["jobs"]["certifier"]["strategy"]["matrix"]["tranche"])
    if not commande:
        faux.append("F commande de la tâche finale introuvable")
        return
    d = tempfile.mkdtemp(prefix="nuit_decoupee_")
    try:
        m = os.path.join(d, "depot")
        # le fabricant aussi (15-11-2026) : le certificateur y lit la liste des fichiers de commandes de GitHub qu'il
        # retire de l'environnement de chaque épreuve (`fichiers_de_commandes_de_github`), à côté de lui-même
        for c, t in [("programmes/P.py", PROGRAMME), ("programmes/CERTIFIER_LA_VERSION.py",
                                                       open(os.path.join(copie, CERTIF), encoding="utf-8").read()),
                     (FAB, open(os.path.join(copie, FAB), encoding="utf-8").read()),
                     ("tests/LANCEMENT_DES_EPREUVES.json", json.dumps({"epreuves": {}}))] + [
                (f"tests/T{f}.py", EPREUVE.replace("{f}", f)) for f in "abc"]:
            os.makedirs(os.path.dirname(os.path.join(m, c)), exist_ok=True)
            open(os.path.join(m, c), "w", encoding="utf-8").write(t)
        os.makedirs(os.path.join(m, "gouvernance"))   # où le certificateur écrit sa référence
        cert = os.path.join(m, CERTIF)
        c, o = certifier(cert, m, "--ecrire-la-reference")
        if c != 0:
            faux.append(f"F référence du dépôt d'essai non écrite (code {c}) : {o.strip().splitlines()[-1:]}")
            return
        for i in range(1, nombre + 1):
            c, o = certifier(cert, m, "--tranche", f"{i}/{nombre}")
            if c != 0:
                faux.append(f"F tranche {i}/{nombre} du dépôt d'essai : code {c} : {o.strip().splitlines()[-1:]}")
                return
        partiels = os.path.join(m, "rapports", "certificats_partiels")
        garde = {f: open(os.path.join(partiels, f), encoding="utf-8").read() for f in os.listdir(partiels)}

        def finale(passage=PASSAGE):
            r = subprocess.run(["bash", "-e", "-c", commande], cwd=m, capture_output=True, text=True, timeout=120,
                               env=dict(os.environ, GITHUB_WORKSPACE=m, GITHUB_RUN_ID=passage))
            texte = open(os.path.join(m, "rapports", "CERTIFICAT_DE_LA_VERSION.md"), encoding="utf-8").read()
            for f, t in garde.items():   # remettre les partiels en état pour le cas suivant
                open(os.path.join(partiels, f), "w", encoding="utf-8").write(t)
            return r.returncode, texte

        def modifier(n, quoi):
            p = json.loads(garde[f"TRANCHE_{n}.json"])
            quoi(p)
            open(os.path.join(partiels, f"TRANCHE_{n}.json"), "w", encoding="utf-8").write(json.dumps(p))

        pleine = next(n for n in range(1, nombre + 1) if json.loads(garde[f"TRANCHE_{n}.json"])["joues"])
        autre = next(n for n in range(1, nombre + 1) if n != pleine)
        c, t = finale()
        # « DÉRIVE » : le code du dépôt d'essai est celui de sa référence, et `conclure` rangerait en « DÉRIVE DE MESURE »
        # un recul né d'une réunion fausse, sans rougir (relecteur du 31-10-2026, I2) ; D1 éprouve la réunion directement
        if c != 0 or "VERSION CERTIFIÉE" not in t or "DÉRIVE" in t:
            faux.append(f"F0 tout est là : code {c}, attendu 0, « VERSION CERTIFIÉE » et aucune « DÉRIVE »")
        # F1 : le partiel d'une tranche VIDE effacé — seule la règle « il en manque un » peut le voir, puisque aucun
        # lancement n'y manque ; F1b : celui d'une tranche pleine
        vide = next((n for n in range(nombre, 0, -1) if not json.loads(garde[f"TRANCHE_{n}.json"])["joues"]), None)
        for cas, n in (("F1", vide), ("F1b", autre)):
            if n is None:
                faux.append(f"{cas} aucune tranche vide dans le dépôt d'essai : le cas ne peut pas se jouer")
                continue
            os.remove(os.path.join(partiels, f"TRANCHE_{n}.json"))
            c, t = finale()
            if c == 0 or "IMPOSSIBLE" not in t:
                faux.append(f"{cas} le certificat partiel effacé de la tranche {n} accepté (code {c})")
        c, t = finale("778")
        if c == 0:
            faux.append("F2 des partiels d'un autre passage acceptés")

        def rouge(p):
            p["resultats"][0][3] = 1
        modifier(pleine, rouge)
        c, t = finale()
        if c == 0:
            faux.append("F3 une épreuve rouge dans un partiel acceptée")
        modifier(autre, lambda p: p.update(impossible="la mesure est aveugle (essai)"))
        c, t = finale()
        if c == 0:
            faux.append("F4 un partiel « impossible » accepté")

        def double(p):
            q = json.loads(garde[f"TRANCHE_{pleine}.json"])
            p["joues"] += q["joues"][:1]
            p["resultats"] += q["resultats"][:1]
        modifier(autre, double)
        c, t = finale()
        if c == 0:
            faux.append("F5 un lancement joué par deux tranches accepté")
        modifier(pleine, lambda p: (p["joues"].pop(0), p["resultats"].pop(0)))
        c, t = finale()
        if c == 0:
            faux.append("F6 un lancement joué par aucune tranche accepté")
        modifier(autre, lambda p: p.update(repartition="0" * 16))
        c, t = finale()
        if c == 0:
            faux.append("F7 une répartition différente acceptée")
        modifier(pleine, lambda p: p.update(empreinte_du_code="0" * 16))
        c, t = finale()
        if c == 0:
            faux.append("F8 un partiel d'un autre code (empreinte) accepté")
        # F9 — le passage en cours écarté des durées (relecteur du 31-10-2026, I2, Sa) : un journal de CE passage, aux
        # durées extrêmes, est posé ; la tranche relancée seule (« Re-run failed jobs ») doit répartir comme ses sœurs.
        # Étalonnage : le même journal, vu depuis un AUTRE passage, doit changer la répartition — sinon le cas ne prouve rien.
        C = charger(cert)
        os.makedirs(os.path.join(m, C.JOURNAUX))
        with open(os.path.join(m, C.JOURNAUX, f"circuit_{PASSAGE}_1_certifier_tranche_1.log"), "w", encoding="utf-8") as s:
            s.write("\n".join(C.ligne_du_journal(f"tests/T{f}.py", ["{copie}"], 0, d_) for f, d_ in
                              (("a", 1), ("b", 2), ("c", 10000))) + "\n")
        avant = json.loads(garde[f"TRANCHE_{pleine}.json"])["repartition"]
        apres = {}
        for passage in (PASSAGE, "999"):
            c, o = certifier(cert, m, "--tranche", f"{pleine}/{nombre}", passage=passage)
            apres[passage] = json.load(open(os.path.join(partiels, f"TRANCHE_{pleine}.json"), encoding="utf-8")).get("repartition")
        if apres["999"] == avant:
            faux.append("F9 étalonnage : le journal posé ne change pas la répartition, le cas ne prouve rien")
        elif apres[PASSAGE] != avant:
            faux.append("F9 la tranche relancée dans le même passage a lu le journal de ce passage : autre répartition")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def n10(C, faux):
    """N10 — `main` du certificateur passe les durées relevées à la boucle de jeu, en mode entier ET en mode tranche.

    ① RÔLE — Garder le câblage de la coupure dans `main` (relecture de Cowork du 09-11-2026, 4dcffa32, B3-9).
    ② CONTEXTE D'APPEL — `tour`, une fois. ③ ENTRÉE — `C` : le certificateur de la copie, chargé · `faux` : la liste
      des fautes, complétée. ④ CONDITIONS D'ENTRÉE — coverage installé (`main` l'importe).
    ⑤ SORTIE — Rien ; ajoute à `faux`. [rend: rien]
    ⑥ TRAITEMENT — ① une racine témoin : programmes/ vide, une référence « {} », un journal témoin d'un passage 111
      écrit par `ligne_du_journal` (« t.py » : 700 s) · ② ÉTALONNAGE : `durees_relevees` lit 700 s sur ce journal,
      sinon le cas serait vide · ③ les fonctions qui copient, mesurent, listent, écrivent et concluent sont remplacées
      par des témoins ; `jouer` par un témoin qui note la coupure reçue · ④ `main` est appelé deux fois, sans option
      (mode entier) puis avec « --tranche 1/1 », GITHUB_RUN_ID valant 999 (le passage 111 n'est pas écarté) ·
      ⑤ la coupure reçue doit valoir 3 × 700 = 2 100 s dans les deux modes (délai déclaré : 300 s).
    ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — B3-9 : remplacer les durées par « {} » dans l'un ou l'autre appel de `main`
      laissait N1 à N9 verts, et la coupure revenait au seul délai déclaré (le défaut B3-2). Sabotages Si et Sj.
    ⑨ CE QUI CLOCHE — La copie, la mesure, la conclusion et l'écriture du partiel ne sont pas jouées ici (témoins) :
      les autres cas les éprouvent. ⑩ EFFET — Écrit une racine jetable, effacée ; remet les fonctions et l'environnement.
    ⑪ TERMINAISON — Rend la main ; rien n'est lancé. [sort: non]
    """
    rac = tempfile.mkdtemp(prefix="nuit_main_")
    noms = ("copier", "armer_la_mesure", "calibrer_la_mesure", "lister_les_epreuves", "options_de_lancement", "jouer",
            "ecrire_le_partiel", "mesure_brute", "lire_la_mesure", "conclure", "empreinte_du_code")
    garde, recus = {n: getattr(C, n) for n in noms}, {}
    argv, env = sys.argv, os.environ.get("GITHUB_RUN_ID")
    try:
        os.makedirs(os.path.join(rac, "programmes"))
        os.makedirs(os.path.join(rac, C.JOURNAUX))
        os.makedirs(os.path.dirname(os.path.join(rac, C.REFERENCE)), exist_ok=True)
        open(os.path.join(rac, C.REFERENCE), "w", encoding="utf-8").write("{}")
        open(os.path.join(rac, C.JOURNAUX, "circuit_111_1_certifier.log"), "w", encoding="utf-8").write(
            C.ligne_du_journal("t.py", [], 0, 700) + "\n")
        if C.durees_relevees(rac, "999") != {"t.py": 700}:
            faux.append(f"N10 étalonnage : le journal témoin rend {C.durees_relevees(rac, '999')}, attendu {{'t.py': 700}}")
            return
        C.copier = lambda racine, dossier: dossier
        C.armer_la_mesure = lambda dossier: ("py", None, None)
        C.calibrer_la_mesure = lambda dossier, py: (True, "")
        C.lister_les_epreuves = lambda copie: ([["t.py", "", []]], [])
        C.options_de_lancement = lambda copie: ({"t.py": 300}, {})
        C.ecrire_le_partiel = lambda racine, contenu: None
        C.mesure_brute = C.lire_la_mesure = lambda *a: {}
        C.conclure = lambda *a, **k: 0
        C.empreinte_du_code = lambda racine: "E"
        os.environ["GITHUB_RUN_ID"] = "999"
        for mode, options in (("entier", []), ("tranche", ["--tranche", "1/1"])):
            C.jouer = lambda copie, py, reg, man, chemin, dossier, arguments, delai, lectures=None, m=mode: (
                recus.__setitem__(m, delai) or (0, 0, []))
            sys.argv = ["CERTIFIER_LA_VERSION.py", rac] + options
            with contextlib.redirect_stdout(io.StringIO()):
                C.main()
    finally:
        for n, f in garde.items():
            setattr(C, n, f)
        sys.argv = argv
        if env is None:
            os.environ.pop("GITHUB_RUN_ID", None)
        else:
            os.environ["GITHUB_RUN_ID"] = env
        shutil.rmtree(rac, ignore_errors=True)
    if recus != {"entier": 2100, "tranche": 2100}:
        faux.append(f"N10 coupures reçues de `main` : {recus}, attendu {{'entier': 2100, 'tranche': 2100}} (3 × 700 s)")


def n11(C, faux):
    """N11 — la sortie d'une épreuve rouge est gardée entière, celle d'une verte coupée à ses dernières lignes.

    ① RÔLE — Garder la réparation 8 du superviseur R-759 du 15-11-2026 (« garder à la nuit la sortie entière d'une
      épreuve rouge ») : sans ce cas, aucune épreuve ne disait si la sortie entière est gardée (même rapport, §5).
    ② CONTEXTE D'APPEL — `tour`, une fois. ③ ENTRÉE — `C` : le certificateur de la copie, chargé · `faux` : la liste
      des fautes, complétée. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; ajoute à `faux`. [rend: rien]
    ⑥ TRAITEMENT — ① `jouer`, LE VRAI, sur un script jetable qui écrit dix lignes et rend 1 : il doit rendre les dix
      lignes · ② `jouer`, LE VRAI, sur un script jetable qui écrit dix lignes sur stdout, « CAS FAUTIF : X » sur
      stderr, puis dort 60 s, joué avec un délai de 3 s : code 124, les dix lignes et « CAS FAUTIF : X » gardés, et
      « ARRÊTÉE : plus de 3 s » en DERNIÈRE ligne (A2) · ③ `jouer_les_lancements` avec un `jouer` témoin qui rend dix
      lignes, code 0 pour « v.py », 1 pour « r1.py », 2 pour « r2.py », 124 pour « r124.py » : chaque rouge doit
      porter les dix lignes, la verte les trois dernières (m1).
    ⑦ UNITÉ — Des lignes. ⑧ POURQUOI — Enquête du 15-11-2026, C6 : trois lignes gardées, le cas fautif de
      VENTE_UNIQUE_A est resté inconnu. Sabotages Sn, So et Sq. Superviseur R-759 du 15-11-2026 (etudes/PLAN_V7_SOUS_
      L_OUTIL_PLANNING/rapports_du_11-11-2026/SUPERVISEUR_CERT3_Dim_15-11-2026.md) : A2 (§2) — une épreuve COUPÉE
      perdait toute sa sortie, alors qu'une coupure est justement un rouge à diagnostiquer ; sabotage Sw · m1 (§3) — le
      seul code 1 éprouvé laissait passer « code == 1 » à la place de « code != 0 », qui ne garde plus qu'un arrêt
      (code 2, le cas de B1) ou une coupure (124) à 3 lignes ; la propriété est « tout code non nul », éprouvée sur
      ses trois classes réelles, pas une liste qu'on allongerait ; sabotage Sx.
    ⑨ CE QUI CLOCHE — Le certificat partiel et le certificat ne sont pas écrits ici : ils recopient les lignes du
      résultat telles quelles (`ecrire_le_partiel`, `ecrire_le_rapport`). ⑩ EFFET — Un dossier jetable, effacé ;
      remet `jouer`. ⑪ TERMINAISON — Rend la main ; le premier script jetable est borné à 60 s, le second coupé à
      3 s par `jouer` (qui le tue, puis l'attend). [sort: non]
    """
    dix = [f"ligne {i}" for i in range(1, 11)]
    d = tempfile.mkdtemp(prefix="nuit_sortie_")
    garde = C.jouer
    try:
        open(os.path.join(d, "r.py"), "w", encoding="utf-8").write(
            "import sys\nfor i in range(1, 11):\n    print('ligne %d' % i)\nsys.exit(1)\n")
        code, _, lignes = C.jouer(d, sys.executable, "", "", "r.py", ".", [], 60)
        if code != 1 or lignes != dix:
            faux.append(f"N11 `jouer` sur une épreuve rouge de 10 lignes rend code {code} et {len(lignes)} ligne(s), "
                        "attendu code 1 et les 10")
        # A2 : une épreuve coupée garde ce qu'elle a écrit, « ARRÊTÉE » en dernière ligne
        open(os.path.join(d, "c.py"), "w", encoding="utf-8").write(
            "import sys, time\nfor i in range(1, 11):\n    print('ligne %d' % i)\nsys.stdout.flush()\n"
            "print('CAS FAUTIF : X', file=sys.stderr)\nsys.stderr.flush()\ntime.sleep(60)\n")
        code, _, lignes = C.jouer(d, sys.executable, "", "", "c.py", ".", [], 3)
        if code != 124 or lignes[:10] != dix or "CAS FAUTIF : X" not in lignes or lignes[-1:] != ["ARRÊTÉE : plus de 3 s"]:
            faux.append(f"N11 `jouer` sur une épreuve coupée rend code {code} et {lignes[-4:]}, attendu code 124, les 10 "
                        "lignes, « CAS FAUTIF : X », puis « ARRÊTÉE : plus de 3 s » en dernier")
        # m1 : tout code non nul garde tout — 1 (rouge), 2 (arrêt), 124 (coupure) ; 0 garde 3 lignes
        codes = {"v.py": 0, "r1.py": 1, "r2.py": 2, "r124.py": 124}
        C.jouer = lambda copie, py, reg, man, chemin, dossier, arguments, delai, lectures=None: (
            codes[chemin], 0, list(dix))
        with contextlib.redirect_stdout(io.StringIO()):
            res = C.jouer_les_lancements(d, d, d, "py", None, None, [[c, "", []] for c in codes], {}, {}, {})
        gardees = {r[0]: len(r[5] or []) for r in res}
        voulu = {c: (3 if n == 0 else 10) for c, n in codes.items()}
        if gardees != voulu or {r[0]: r[5] for r in res}.get("v.py") != dix[-3:]:
            faux.append(f"N11 lignes gardées par la boucle de jeu : {gardees}, attendu {voulu}")
    finally:
        C.jouer = garde
        shutil.rmtree(d, ignore_errors=True)


def n13(C, faux):
    """N13 — la charge prévue d'un lancement est sa durée relevée, sinon son délai déclaré, sinon DUREE_MAX_EPREUVE.

    ① RÔLE — Regarder DIRECTEMENT la règle du ⑤ de `prevue` (dans `repartir`), qu'aucun cas ne regardait.
    ② CONTEXTE D'APPEL — `tour`, une fois. ③ ENTRÉE — `C` : le certificateur de la copie, chargé · `faux` : la liste
      des fautes, complétée. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien ; ajoute à `faux`. [rend: rien]
    ⑥ TRAITEMENT — Le VRAI `repartir`, sur trois lancements fabriqués : « a.py » a une durée relevée de 700 s et un
      délai déclaré de 9 999 s (la relevée doit l'emporter) ; « b.py » n'a que son délai déclaré, 300 s ; « c.py »
      n'a ni l'un ni l'autre (il compte DUREE_MAX_EPREUVE). Joué à 1 et à 3 tranches, la somme des charges doit valoir
      700 + 300 + DUREE_MAX_EPREUVE (2 500 s le 15-11-2026). La valeur est LUE sur le certificateur, jamais recopiée.
    ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — Superviseur R-759 du 15-11-2026 (etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/
      rapports_du_11-11-2026/SUPERVISEUR_CERT3_Dim_15-11-2026.md, §1, « DE FOND ») : le sabotage Sh (« durée relevée,
      sinon 1 500 s ») ne mordait que par accident, quand N5 était déjà rouge sur les vrais journaux ; à 12 tranches,
      N5 est vert dans les deux cas, et Sh NE MORDAIT PAS (mesuré par Cowork et par CERT-3). Ce cas ne dépend ni des
      journaux ni du nombre de tranches, comme N9 qui regarde `coupure`. Mesuré par le superviseur : Sh donne 3 700 s,
      l'inversion des priorités (délai déclaré avant durée relevée, sabotage Sv) 11 799 s, pour 2 500 attendues.
    ⑨ CE QUI CLOCHE — L'ORDRE des épreuves dans les tranches n'est pas regardé ici (N4 et N5 le font sur les vrais
      lancements). ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lanc = [["a.py", ".", []], ["b.py", ".", []], ["c.py", ".", []]]
    ka, kb, _ = (C.cle_de(l[0], l[2]) for l in lanc)
    voulu = 700 + 300 + C.DUREE_MAX_EPREUVE
    for nombre in (1, 3):
        _, charges = C.repartir(lanc, {ka: 700}, {kb: 300, ka: 9999}, nombre)
        if sum(charges) != voulu:
            faux.append(f"N13 charges prévues ({nombre} tranche(s)) : {charges}, somme {sum(charges)}, attendu {voulu}")


def litteraux_py(texte):
    """Rend les chemins de programme (« dossier/…/NOM.py ») qu'un texte de Python écrit en littéraux.

    ① RÔLE — Lire, sans l'exécuter, quels programmes une épreuve nomme, pour N12.
    ② CONTEXTE D'APPEL — `n12`, une fois par épreuve. ③ ENTRÉE — `texte` : le source d'une épreuve.
    ④ CONDITIONS D'ENTRÉE — Le texte se lit en Python (sinon SyntaxError, qui remonte : rouge).
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins, séparés par « / ». [rend: 1]
    ⑥ TRAITEMENT — l'arbre syntaxique : chaque chaîne littérale hors des textes explicatifs (docstrings), et, pour
      chaque appel « ….join(…) », la suite de ses derniers arguments littéraux (au moins deux), jointe par « / » ;
      on garde ce qui a la forme « dossier/…/NOM.py ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Le 14-11-2026, deux épreuves nommaient leur programme par
      os.path.join(RACINE, "etudes", "VINGT_ANS_A_PART_Mer_11-11-2026", "….py") : la racine n'est pas un littéral,
      la suite l'est (mesuré le 15-11-2026 : sans la suite, la numérotation n'était pas vue).
    ⑨ CE QUI CLOCHE — Un chemin construit autrement (format, concaténation, variable intermédiaire) n'est pas lu.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import ast
    arbre = ast.parse(texte)
    explicatifs = {id(n.body[0].value) for n in ast.walk(arbre)
                   if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body
                   and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
    vus = set()
    for n in ast.walk(arbre):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", None) == "join":
            suite = []
            for a in reversed(n.args):
                if not (isinstance(a, ast.Constant) and isinstance(a.value, str)):
                    break
                suite.insert(0, a.value)
            if len(suite) >= 2:
                vus.add("/".join(suite))
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in explicatifs:
            vus.add(n.value)
    return {c for c in vus if re.fullmatch(r"(?:[\w.-]+/)+[\w.-]+\.py", c)}


def n12(C, depot, faux):
    """N12 — une épreuve de la nuit ne nomme aucun programme du dépôt rangé hors des dossiers que le circuit garde.

    ① RÔLE — Voir AVANT la nuit une épreuve née incompatible avec le circuit (enquête du 15-11-2026, C9 et C10).
    ② CONTEXTE D'APPEL — `tour`, une fois. ③ ENTRÉE — `C` : le certificateur de la copie · `depot` : la copie ·
      `faux` : la liste des fautes, complétée. ④ CONDITIONS D'ENTRÉE — DEPOT est un dépôt git (sinon seule la copie
      dit ce qui existe).
    ⑤ SORTIE — Rien ; ajoute à `faux`. [rend: rien]
    ⑥ TRAITEMENT — les dossiers gardés : DOSSIERS_DE_CODE du fabricant de la copie ; ce qui existe : les fichiers
      suivis par git au DÉPÔT (« git ls-files », qui voit aussi ce que le pas « poser » a effacé de l'arbre sur
      GitHub) et les fichiers de la copie ; pour chaque épreuve tests/*.py que le certificateur lance
      (`lister_les_epreuves`), chaque chemin de `litteraux_py` qui existe et dont le dossier n'est pas gardé est une
      faute.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le pas « poser le code public » efface tout .py hors des dossiers gardés : le 14-11-2026,
      INVENTAIRE_DES_VINGT_ANS et NUMEROTATION_DES_SOCIETES_SORTIES ont rougi sur GitHub (FileNotFoundError), vertes
      sur la machine du Chat. Superviseur R-759 du 15-11-2026, réparation 4 : la propriété plutôt qu'une liste de
      dossiers de plus. « Existe » : un chemin fabriqué par une épreuve pour ses propres cas (« etudes/x/programmes/
      A.py ») n'est pas un programme du dépôt (mesuré le 15-11-2026 : 4 épreuves en écrivent). Placée ICI et non dans
      EPREUVES_DU_DOSSIER_DE_LANCEMENT que nomme le superviseur : celle-là éprouve le dossier d'où le garde-fou est
      lancé, pas la table des lancements ; celle-ci lit déjà les lancements et DOSSIERS_DE_CODE (N4, N8).
    ⑨ CE QUI CLOCHE — `litteraux_py` ne lit pas tout chemin (son ⑨). « --saboter seul accepté » n'est pas vérifié
      ici : une lecture du texte se trompe (mesuré le 15-11-2026 : 2 épreuves sur 3 qui l'acceptent par argparse ou
      par une liste seraient refusées) ; c'est consigné, pas réparé.
    ⑩ EFFET — Lance « git ls-files » (lecture). ⑪ TERMINAISON — Rend la main ; git est borné à 120 s. [sort: non]
    """
    gardes = set(charger(os.path.join(depot, FAB)).DOSSIERS_DE_CODE)
    r = subprocess.run(["git", "-C", DEPOT, "ls-files", "-z", "--", "*.py"], capture_output=True, text=True, timeout=120)
    suivis = set(r.stdout.split("\0")) if r.returncode == 0 else set()
    lancements, _ = C.lister_les_epreuves(depot)
    for e in sorted({l[0] for l in lancements if l[0].startswith("tests/") and l[0].endswith(".py")}):
        for c in sorted(litteraux_py(open(os.path.join(depot, e), encoding="utf-8").read())):
            if os.path.dirname(c) not in gardes and (c in suivis or os.path.isfile(os.path.join(depot, c))):
                faux.append(f"N12 {e} nomme {c}, hors des dossiers gardés par le circuit : il y sera effacé")


def sabotages_comptes(texte):
    """Rend les noms des sabotages d'une épreuve, Z0 exclu, lus par une AUTRE rédaction que celle du certificateur.

    ① RÔLE — Compter les sabotages d'une épreuve « avant la découpe », sans passer par `sabotages_declares`.
    ② CONTEXTE D'APPEL — `n14`, une fois par épreuve déclarée en morceaux.
    ③ ENTRÉE — `texte` : le code de l'épreuve.
    ④ CONDITIONS D'ENTRÉE — Le dictionnaire s'ouvre par une ligne « SABOTAGES = { » et se ferme par une ligne « } »
      seule ; chaque clé commence une ligne, indentée de quatre espaces. Sinon la liste est vide, et `n14` rougit.
    ⑤ SORTIE — UNE valeur : la liste des noms.
      [rend: 1]
    ⑥ TRAITEMENT — expression régulière sur le texte (et non l'arbre syntaxique, que lit le certificateur).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un compte fait par la même fonction que la découpe ne verrait pas une lecture amputée (sabotage
      Sz2). Calibré le 21-11-2026 sur l'épreuve de la lecture des cours : 122 sabotages, autant que par l'arbre ; une
      première forme exigeait une espace après « : » et en manquait un (S80, écrit « …sans_code":[ »).
    ⑨ CE QUI CLOCHE — Une clé écrite sur une ligne qui ne commence pas par quatre espaces n'est pas vue : le compte
      diffère alors de celui du certificateur, et `n14` rougit — à tort, mais jamais en silence.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    debut = texte.find("\nSABOTAGES = {\n")
    fin = texte.find("\n}\n", debut)
    if debut < 0 or fin < 0:
        return []
    return [n for n in re.findall(r'^    "([^"]+)":\s*\[', texte[debut:fin], re.M) if n != "Z0"]


def n14(C, depot, faux):
    """N14 — aucun sabotage perdu ni joué deux fois quand une épreuve est jouée en morceaux (A-961).

    ① RÔLE — Compter les sabotages avant et après la découpe, et rougir si les comptes diffèrent.
    ② CONTEXTE D'APPEL — `tour`, une fois.
    ③ ENTRÉE — `C` : le certificateur de la copie · `depot` : la copie · `faux` : la liste des fautes, complétée.
    ④ CONDITIONS D'ENTRÉE — tests/LANCEMENT_DES_EPREUVES.json se lit.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — pour chaque épreuve de la table « morceaux_de_la_nuit » : ① ses sabotages comptés par
      `sabotages_comptes` · ② ses lancements rendus par `lister_les_epreuves` : aucun lancement « --saboter » entier
      ne reste, les morceaux sont exactement 1/N … N/N, et chacun porte « --seulement=… » · ③ chaque code court des
      morceaux désigne exactement un sabotage compté, aucun code n'est joué deux fois, et le compte des codes égale le
      compte des sabotages · ④ sur des lancements écrits à la main : `comparer` voit le lancement entier de la
      référence joué quand tous ses morceaux le sont, disparu s'il en manque un ; `charge_estimee_du_morceau` compte Z0.
    ⑦ UNITÉ — Des nombres de sabotages ; des secondes (④).
    ⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 13h34 (A-961) : découper la grosse épreuve ; consigne du même
      jour : « aucun sabotage ne doit être perdu ». Un sabotage perdu à la découpe est une partie du code qu'on croit
      éprouvée chaque nuit et qui ne l'est plus — et rien d'autre ne le verrait : la morsure de chaque sabotage joué
      reste verte.
    ⑨ CE QUI CLOCHE — Le nombre de morceaux lui-même n'est pas jugé ici : c'est N5 qui dit si chaque morceau tient sous
      le tiers d'une tranche.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    table = json.load(open(os.path.join(depot, "tests", "LANCEMENT_DES_EPREUVES.json"), encoding="utf-8"))
    lancements, _ = C.lister_les_epreuves(depot)
    for chemin, e in (table.get("morceaux_de_la_nuit") or {}).items():
        avant = sabotages_comptes(open(os.path.join(depot, chemin), encoding="utf-8").read())
        if not avant:
            faux.append(f"N14 {chemin} : aucun sabotage compté avant la découpe")
            continue
        siens = [l for l in lancements if l[0] == chemin and "--saboter" in l[2]]
        n = e.get("morceaux") if isinstance(e, dict) else None
        etiquettes = sorted(a for l in siens for a in l[2] if a.startswith("--morceau="))
        if any(l[2] == ["{copie}", "--saboter"] for l in siens):
            faux.append(f"N14 {chemin} : le lancement « --saboter » entier est encore rangé (la découpe n'a pas eu lieu)")
        if etiquettes != sorted(f"--morceau={i}/{n}" for i in range(1, (n or 0) + 1)):
            faux.append(f"N14 {chemin} : morceaux {etiquettes}, attendu 1/{n} … {n}/{n}")
        codes = [c for l in siens for a in l[2] if a.startswith("--seulement=") for c in a.split("=", 1)[1].split(",")]
        courts = [x.split("_", 1)[0] for x in avant]
        mal = sorted({c for c in codes if courts.count(c) != 1})
        doubles = sorted({c for c in codes if codes.count(c) > 1})
        perdus = sorted(x for x in avant if x.split("_", 1)[0] not in codes)
        if len(codes) != len(avant) or mal or doubles or perdus:
            faux.append(f"N14 {chemin} : {len(avant)} sabotages avant la découpe, {len(codes)} après ; perdus "
                        f"{perdus[:3]} ; joués deux fois {doubles[:3]} ; codes qui ne désignent pas un sabotage {mal[:3]}")
    # N14 (suite) — sur des lancements écrits à la main : la référence qui porte le lancement entier le voit joué si
    # TOUS ses morceaux le sont, et « disparu » s'il en manque un (`comparer`) ; la charge d'un morceau jamais joué est
    # la durée entière × (k + 1) ÷ (K + 1), Z0 compté (`charge_estimee_du_morceau`) : 1 000 s, morceaux de 2 et 1
    # sabotages → 750 s et 500 s
    m1 = ["t.py", ".", ["{copie}", "--saboter", "--morceau=1/2", "--seulement=S1,S3"]]
    m2 = ["t.py", ".", ["{copie}", "--saboter", "--morceau=2/2", "--seulement=S2"]]
    ref = {"epreuves": [["t.py", ".", ["{copie}", "--saboter"]]]}
    for joues, voulu in (([m1, m2], 0), ([m1], 1)):
        disparues = C.comparer({}, joues, ref, {})[1]
        if len(disparues) != voulu:
            faux.append(f"N14 comparer : {len(joues)} morceau(x) sur 2 joués, {len(disparues)} épreuve(s) disparue(s), "
                        f"attendu {voulu}")
    estimees = [C.charge_estimee_du_morceau(m, [m1, m2], 1000) for m in (m1, m2)]
    if estimees != [750, 500]:
        faux.append(f"N14 charge estimée des morceaux : {estimees}, attendu [750, 500]")


def n15(depot, k, faux):
    """N15 — le nombre de tranches est la largeur du réservoir, qui laisse 2 places au circuit du soir (A-961, A-888).

    ① RÔLE — Garder la décision du 21-11-2026 : 18 tranches, jamais une place du soir.
    ② CONTEXTE D'APPEL — `tour`, une fois, après N2.
    ③ ENTRÉE — `depot` : la copie (le fabricant y est pris) · `k` : le nombre de tranches lu dans le circuit fabriqué
      (N2) · `faux` : la liste des fautes, complétée.
    ④ CONDITIONS D'ENTRÉE — Le fabricant de la copie se charge.
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — trois comparaisons : k = PLACES_LONGUES ; PLACES_LONGUES = TACHES_EN_MEME_TEMPS_DU_COMPTE − 2 ;
      TRANCHES_DE_LA_NUIT = k.
    ⑦ UNITÉ — Des tâches de GitHub.
    ⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 13h34 (« 18 morceaux ») et A-888 du 17-11-2026 à 22h30
      (« 2 places toujours libres pour le circuit du soir et le relais »). Lu sur le circuit FABRIQUÉ (k) et non sur la
      seule constante : c'est le circuit que GitHub exécute. N5 seul ne suffit pas à garder 18 : sur les journaux
      présents au 21-11-2026, 15 tranches et la découpe tiendraient sous le tiers (6 439 s mesurés) — N5 ne rougirait
      pas, et la décision serait défaite sans signal.
    ⑨ CE QUI CLOCHE — La valeur 2 est relue ici, écrite une seconde fois : elle répète A-888 (la règle « 2 places »
      n'est portée par aucune constante du fabricant, seulement par LARGEUR_DES_CIRCUITS_LONGS = 18 et un commentaire).
    ⑩ EFFET — Exécute le fabricant de la copie (chargement).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    F = charger(os.path.join(depot, FAB))
    if k != F.PLACES_LONGUES or F.TRANCHES_DE_LA_NUIT != k:
        faux.append(f"N15 {k} tranches au circuit (constante : {F.TRANCHES_DE_LA_NUIT}), attendu la largeur du "
                    f"réservoir, {F.PLACES_LONGUES} places (A-961)")
    if F.PLACES_LONGUES != F.TACHES_EN_MEME_TEMPS_DU_COMPTE - 2:
        faux.append(f"N15 réservoir de {F.PLACES_LONGUES} places pour {F.TACHES_EN_MEME_TEMPS_DU_COMPTE} tâches du "
                    "compte : les 2 places du soir ne sont plus libres (A-888)")


def tour(depot):
    """Joue N1 à N15, D1, puis F0 à F9 sur une copie de `depot`, et rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `depot` : la copie restreinte à éprouver. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes. [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥. ⑦ UNITÉ — Minutes, secondes. ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit un dossier jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    pub = tempfile.mkdtemp(prefix="nuit_publique_")
    try:
        r = subprocess.run([sys.executable, "-B", os.path.join(depot, FAB), depot, pub], capture_output=True,
                           text=True, timeout=120)
        if r.returncode != 0 or not os.path.isfile(os.path.join(pub, CIRCUIT)):
            return [f"N1 le fabricant rend {r.returncode} : {(r.stdout + r.stderr).strip()[-200:]}"]
        y = yaml.safe_load(open(os.path.join(pub, CIRCUIT), encoding="utf-8"))
    finally:
        shutil.rmtree(pub, ignore_errors=True)
    jobs = y.get("jobs") or {}
    t, f = jobs.get("certifier") or {}, jobs.get("reunir") or {}
    tranches = ((t.get("strategy") or {}).get("matrix") or {}).get("tranche")
    if not isinstance(tranches, list) or not tranches:
        return ["N2 le job « certifier » n'est pas une matrice de tranches"]
    k = len(tranches)
    if tranches != list(range(1, k + 1)):
        faux.append(f"N2 tranches {tranches}, attendu 1 à {k}")
    if (t.get("strategy") or {}).get("fail-fast") is not False:
        faux.append("N2 la matrice s'arrête au premier échec (fail-fast n'est pas false)")
    run_t = next((p.get("run", "") for p in t.get("steps", []) if p.get("id") == "certifier"), "")
    run_f = next((p.get("run", "") for p in f.get("steps", []) if p.get("id") == "certifier"), "")
    if f"--tranche ${{{{ matrix.tranche }}}}/{k}" not in run_t:
        faux.append(f"N2 la tranche ne lance pas « --tranche ${{{{ matrix.tranche }}}}/{k} » : {run_t!r}")
    if not re.search(r"--reunir %d\s*$" % k, run_f):
        faux.append(f"N2 la tâche finale ne lance pas « --reunir {k} » : {run_f!r}")
    besoins = f.get("needs")
    if "certifier" not in ([besoins] if isinstance(besoins, str) else (besoins or [])):
        faux.append("N2 la tâche finale ne dépend pas des tranches (needs)")
    if "always()" not in str(f.get("if", "")):
        faux.append("N2 la tâche finale ne tourne pas « always() » : elle se tairait quand une tranche échoue")
    for nom, j in jobs.items():
        lim = j.get("timeout-minutes", LIMITE_DE_GITHUB)
        if not isinstance(lim, int) or lim > LIMITE_DE_GITHUB:
            faux.append(f"N3 job {nom} : limite {lim!r} minutes, au-delà de {LIMITE_DE_GITHUB}")
    # N4 à N6 — la répartition du certificateur de la copie, sur les journaux de la copie
    C = charger(os.path.join(depot, CERTIF))
    lancements, _ = C.lister_les_epreuves(depot)
    delais, series = C.options_de_lancement(depot)
    parts, charges = C.repartir(lancements, C.durees_relevees(depot), delais, k)
    vus = [json.dumps(l) for p in parts for l in p]
    for l in lancements:
        n = vus.count(json.dumps(l))
        if n != 1:
            faux.append(f"N4 {C.cle_de(l[0], l[2])} : dans {n} tranche(s), attendu 1")
    places = {l[0] for p in parts for l in p}
    for e in sorted(tests_lances(depot) - places):
        faux.append(f"N4 épreuve de tests/ dans aucune tranche : {e}")
    limite = t.get("timeout-minutes", LIMITE_DE_GITHUB)
    for i, ch in enumerate(charges, 1):
        if not isinstance(limite, int) or ch * TIERS > limite * 60:
            faux.append(f"N5 tranche {i} : {ch} s prévues, au-delà du tiers de {limite} minutes")
    # N7 — assez d'essais de poussée : une tranche échoue au plus (tranches − 1) + (poussées étrangères) fois
    # (superviseur R-759 du 31-10-2026) ; moins d'essais que de tranches perd des partiels à coup sûr
    depot_t = next((p.get("run", "") for p in t.get("steps", []) if p.get("id") == "deposer"), "")
    essais = re.findall(r"for i in \$\(seq 1 (\d+)\)", depot_t)
    if len(essais) != 1 or int(essais[0]) < k:
        faux.append(f"N7 essais de poussée d'une tranche : {essais}, il en faut au moins {k} (le nombre de tranches)")
    # D1 — la réunion des mesures, éprouvée directement (prototype du superviseur R-759 du 31-10-2026) : ce qu'aucune
    # tranche n'examine est l'INTERSECTION de leurs non-examinés ; un programme d'empreintes différentes est écarté
    a_ = {"p.py": {"empreinte": "E", "lignes": [1, 2], "branches": [[1, 2], [2, 3]], "fonctions_non_examinees": ["f", "g"]}}
    b_ = {"p.py": {"empreinte": "E", "lignes": [2, 3], "branches": [[2, 3], [4, 5]], "fonctions_non_examinees": ["g", "h"]}}
    c_ = {"p.py": {"empreinte": "AUTRE", "lignes": [], "branches": [], "fonctions_non_examinees": []}}
    r_, _ = C.reunir_les_mesures([a_, b_])
    for cle, voulu in (("lignes", [2]), ("branches", [[2, 3]]), ("fonctions_non_examinees", ["g"])):
        if r_.get("p.py", {}).get(cle) != voulu:
            faux.append(f"D1 réunion des {cle} : {r_.get('p.py', {}).get(cle)}, attendu {voulu}")
    r_, e_ = C.reunir_les_mesures([a_, c_])
    if e_ != ["p.py"] or r_:
        faux.append("D1 un programme mesuré avec deux empreintes n'est pas écarté")
    # N8 — la copie porte le code de chaque emplacement que le fabricant de la SOURCE publie (relecture neuve du
    # 01-11-2026, M8) : une liste gardée par `copier_le_necessaire` oublierait un emplacement ajouté au fabricant, et
    # aucun autre cas ne le verrait (le relecteur l'a mesuré : la liste des quatre anciens restait verte)
    for dossier in charger(os.path.join(DEPOT, FAB)).DOSSIERS_DE_CODE:
        src = os.path.join(DEPOT, dossier)
        manque = sorted(f for f in (os.listdir(src) if os.path.isdir(src) else [])
                        if f.endswith(".py") and os.path.isfile(os.path.join(src, f))
                        and not os.path.isfile(os.path.join(depot, dossier, f)))
        if manque:
            faux.append(f"N8 la copie n'a pas le code de « {dossier or '.'} » : {len(manque)} fichier(s), dont {manque[:2]}")
    for e in series:
        ou = {i for i, p in enumerate(parts) for l in p if l[0] == e}
        if len(ou) != 1:
            faux.append(f"N6 série hors de la nuit {e} : son lancement et sa vérification dans {len(ou)} tranches")
    # N9 — la coupure d'un lancement (relecture de Cowork du 09-11-2026, B3-2) : le plus grand du délai déclaré et de
    # 3 × la durée relevée ; puis la boucle de jeu la passe bien à `jouer` ET à `refaire_des_essais` (fonctions
    # remplacées par des témoins qui notent le délai reçu, rien n'est lancé)
    for d_, r_, voulu in (({"a": 300}, {"a": 400}, 1200), ({"a": 300}, {"a": 50}, 300), ({"a": 300}, {}, 300),
                          ({}, {}, C.DUREE_MAX_EPREUVE), ({}, {"a": 1000}, 3000),
                          # le plafond : 3 × DUREE_MAX_EPREUVE pour la croissance, jamais sous le délai déclaré
                          ({}, {"a": 4500}, 3 * C.DUREE_MAX_EPREUVE), ({"a": 10800}, {"a": 5097}, 10800)):
        if C.coupure("a", d_, r_) != voulu:
            faux.append(f"N9 coupure(délai {d_}, durée {r_}) = {C.coupure('a', d_, r_)}, attendu {voulu}")
    recus, garde = {}, (C.jouer, C.verifier_une_serie, C.refaire_des_essais)
    try:
        C.jouer = lambda copie, py, reg, man, chemin, dossier, arguments, delai, lectures=None: (
            recus.__setitem__(chemin, delai) or (0, 0, []))
        C.verifier_une_serie = lambda *a, **k: (0, 0, [])
        C.refaire_des_essais = lambda copie, py, reg, man, chemin, motif, nombre, delai: (
            recus.__setitem__(chemin + " essais", delai) or (0, 0, []))
        jet = tempfile.mkdtemp(prefix="nuit_coupure_")
        try:
            with contextlib.redirect_stdout(io.StringIO()):   # ses lignes de journal ne regardent pas ce cas
                C.jouer_les_lancements(depot, jet, depot, "py", None, None,
                                       [["t.py", "", []], ["s.py", "", ["--saboter"]]],
                                       {"t.py": 300, "s.py --saboter": 300}, {"s.py": {"essais": 2, "releve": "m"}},
                                       {"t.py": 500, "s.py --saboter": 400})
        finally:
            shutil.rmtree(jet, ignore_errors=True)
    finally:
        C.jouer, C.verifier_une_serie, C.refaire_des_essais = garde
    if recus != {"t.py": 1500, "s.py essais": 1200}:
        faux.append(f"N9 coupures reçues par la boucle de jeu : {recus}, attendu {{'t.py': 1500, 's.py essais': 1200}}")
    n11(C, faux)
    n12(C, depot, faux)
    n13(C, faux)
    n10(C, faux)
    n14(C, depot, faux)
    n15(depot, k, faux)
    essai(depot, y, faux)
    return faux


def main():
    """Joue le tour tel quel (Z0), puis, avec --saboter, un tour par sabotage.

    ① RÔLE — Le programme entier. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête. ⑤ SORTIE — Le code de sortie (0, 1, 2). [rend: 1]
    ⑥ TRAITEMENT — Pour chaque cas : copie restreinte, sabotage appliqué (chaque texte doit y être une fois), tour.
      Z0 doit être vert ; chaque sabotage doit faire au moins une faute, et, s'il est dans ATTENDU, une faute qui
      porte le texte attendu (15-11-2026). Un sabotage dont le texte d'origine vaut None CRÉE le fichier dans la copie.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
    ⑨ CE QUI CLOCHE — Si la lecture de DOSSIERS_DE_CODE au fabricant échoue, trace Python, code 1 : rouge pour la
      certification, voir le ⑨ de `copier_le_necessaire`.
    ⑩ EFFET — Écrit des dossiers jetables. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    noms = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    code = 0
    for nom in noms:
        d = tempfile.mkdtemp(prefix="nuit_copie_")
        try:
            copier_le_necessaire(DEPOT, d)
            for fichier, avant, apres in SABOTAGES[nom]:
                p = os.path.join(d, fichier)
                if avant is None:          # un fichier créé dans la copie (15-11-2026, Sp)
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    open(p, "w", encoding="utf-8").write(apres)
                    continue
                texte = open(p, encoding="utf-8").read()
                if texte.count(avant) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte trouvé {texte.count(avant)} fois dans {fichier}")
                    code = 2
                    break
                open(p, "w", encoding="utf-8").write(texte.replace(avant, apres))
            else:
                faux = tour(d)
                if nom == "Z0":
                    print("Z0 " + ("vert" if not faux else "ROUGE : " + " | ".join(faux)))
                    code = max(code, 1 if faux else 0)
                else:
                    vise = [f for f in faux if ATTENDU.get(nom, "") in f]
                    print(f"{nom} " + ("mord : " + str((vise or faux)[:2])[:160] if vise else
                                       f"NE MORD PAS{' SUR « ' + ATTENDU[nom].strip() + ' »' if faux else ''} : "
                                       + str(faux[:2])[:160] if faux else "NE MORD PAS"))
                    code = max(code, 0 if vise else 1)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
