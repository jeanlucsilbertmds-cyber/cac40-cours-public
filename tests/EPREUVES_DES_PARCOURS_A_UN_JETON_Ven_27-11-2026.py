#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DES PARCOURS À UN JETON (lot W2d du plan R505) — Ven 27-11-2026.
Simulation uniquement : des opérations fictives (année 2030) et les 100 opérations simulées de C5-ETENDU-10 sur
2024-2026 (le jeu du golden, ses années de réglage, déjà vues) ; aucune stratégie n'est jouée sur 2000-2023, aucun
ordre réel n'est jamais passé.

LE SENS EN TÊTE — R-505 version 2, étape 6, décision de Jean-Luc du 27-11-2026 à 18h27 (A-1092) : la mise en direct
en un jeton se décide sur des milliers de parcours à un jeton ; le creux « 1 fois sur 20 sur 5 ans » (A-796) et le
gain net par an au pire (A-793) s'y mesurent, à 95 % ; les signaux pris et ignorés se comparent. Ces épreuves
prouvent : la règle du jeton est celle du circuit du soir (E1) et retrouve le golden un jeton opération par
opération depuis les jetons illimités (E2, vraie ligne) ; la couture ne fait jamais tenir deux positions (E3) ; le
creux est la mécanique de l'alarme, et égale au centime celle de `mesurer_les_indicateurs` quand il n'y a qu'un
parcours possible (E4, golden : 21 500 €) ; le gain au pire est le rang 5 % des parcours (E5) ; une règle qui prend
les plus mauvais est dénoncée, une règle qui prend les meilleurs ne l'est pas (E6) ; les NON TERMINÉES sont à part
(E7) ; les refus lèvent (E8) ; le hasard est reproductible (E9) ; R-207bis et le creux ne sont pas recopiés (E10).
`--saboter` casse le code de chaque façon de la table SABOTAGES ; chacune doit faire rougir au moins un cas (R-731).

USAGE : python3 -B tests/EPREUVES_DES_PARCOURS_A_UN_JETON_Ven_27-11-2026.py <racine> [--saboter | --mesurer | <sabotage>…]
CODE : 0 si Z0 est vert et si chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de sabotage
est introuvable, si le nom est inconnu, ou si une donnée manque (R-734).

① RÔLE — Prouver que le lot W2d fait ce que dit sa note, et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis avec
  « --saboter ». Ce programme se relance lui-même en « --cas <copie> <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter », « --mesurer » (la mesure sur C5, sans épreuve) ou des noms de
  sabotages, facultatifs.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/ (MODULE_PARCOURS_A_UN_JETON, MESURER_LES_INDICATEURS et ses
  briques), gouvernance/golden_tests_*.json, temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier programmes/ dans un dossier temporaire, appliquer le sabotage
  (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie · ③ Z0 doit être vert ; un sabotage
  doit faire rougir au moins un cas.
⑦ UNITÉ — Euros ; euros par an ; parts entre 0 et 1 ; dates AAAA-MM-JJ.
⑧ POURQUOI — R-731 (épreuves et sabotages), R-732 (un cas tiré d'une vraie ligne : E2 et E4, le rejeu du golden de
  C5), R-734 (un contrôle qui n'a pas pu tourner rend un code non nul).
⑨ CE QUI CLOCHE — ① E2, E4 et E9 ne jugent rien : C5 a été réglée sur 2024-2026 ; ses chiffres sont des mesures de
  forme. ② E4b recompose le mélange dans l'épreuve à partir des parcours rendus : il prouve le branchement sur
  `seuils_1_sur_20_sur_5_ans`, pas la justesse statistique du mélange (décision pour Jean-Luc, note de livraison).
⑩ EFFET — Écrit et efface des dossiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 900 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""

import ast
import os
import shutil
import subprocess
import sys
import tempfile

MP = "MODULE_PARCOURS_A_UN_JETON.py"
TEMOIN = os.path.join("temoins", "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv")
GRAINE = 20261127

# LES SABOTAGES : {nom : [(fichier, texte présent une fois, remplaçant)]}. Chacun retire ou fausse UNE propriété.
SABOTAGES = {
    "S01_signal_du_jour_de_sortie_refuse": [(MP, "if sortie is not None and j < sortie:",
                                             "if sortie is not None and j <= sortie:")],
    "S02_departage_r207bis_retire": [(MP, "enveloppes = TP.departager_r207bis(enveloppes)",
                                      "enveloppes = list(enveloppes)")],
    "S03_couture_sans_garde": [(MP, 'if tour == 1 and (_non_terminee(o) or not o["date_sortie"] < depart):',
                                "if False:")],
    "S04_creux_sur_le_seul_historique": [(MP, "seuil = MLI.seuils_1_sur_20_sur_5_ans(melange, rythme,",
                                          'seuil = MLI.seuils_1_sur_20_sur_5_ans(resumes[0]["nets"], rythme,')],
    "S05_rythme_faux": [(MP, 'rythme = sum(r["operations"] for r in resumes) / len(resumes) / annees',
                         'rythme = max(r["operations"] for r in resumes) / annees')],
    "S06_gain_au_mieux": [(MP, "valeur_au_rang(gains, 1.0 - MLI.UNE_FOIS_SUR_VINGT)",
                           "valeur_au_rang(gains, MLI.UNE_FOIS_SUR_VINGT)")],
    "S07_rang_de_la_regle_inverse": [(MP, "part = sum(1 for m in tires if m <= m_h) / len(tires)",
                                      "part = sum(1 for m in tires if m >= m_h) / len(tires)")],
    "S08_grappe_sans_le_meme_jour": [(MP, 'if p["date_signal"] <= o["date_signal"] < p["date_sortie"] and o is not p]',
                                      'if p["date_signal"] < o["date_signal"] < p["date_sortie"] and o is not p]')],
    "S09_non_terminee_comptee": [(MP, 'return o.get("motif") == COMMUN.MOTIF_FIN_DES_DONNEES or not o.get("date_sortie")',
                                  'return not o.get("date_sortie")')],
    "S10_facon_de_tirer_non_controlee": [(MP, "    if tirage not in TIRAGES:\n        raise",
                                          "    if False:\n        raise")],
    "S11_r207bis_recopie": [(MP, "enveloppes = TP.departager_r207bis(enveloppes)",
                             'enveloppes = sorted(enveloppes, key=lambda e: (e["cci"], str(e["valeur"])))')],
    "S12_hasard_global": [(MP, "    hasard = random.Random(graine)\n    rendu = []",
                           "    hasard = random\n    rendu = []")],
}


def lancer(racine, sabotage):
    """Copie programmes/, applique un sabotage, relance ce fichier en « --cas » et rend (code, sortie).
    ① RÔLE — Un passage d'épreuves sur une copie, intacte (Z0) ou sabotée. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` ; `sabotage` : un nom de SABOTAGES ou None. ④ CONDITIONS D'ENTRÉE — programmes/ existe.
    ⑤ SORTIE — DEUX valeurs : le code de la relance (2 si une cible est introuvable) et sa sortie. [rend: 2]
    ⑥ TRAITEMENT — copier, remplacer (texte présent une fois exactement), relancer avec un délai de 900 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731 : le sabotage porte sur une COPIE, jamais sur le dépôt.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — un dossier temporaire, effacé. ⑪ TERMINAISON — bornée à 900 s. [sort: non]"""
    tmp = tempfile.mkdtemp(prefix="W2d_epreuve_")
    try:
        prog = os.path.join(tmp, "programmes")
        shutil.copytree(os.path.join(racine, "programmes"), prog,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for fichier, avant, apres in (SABOTAGES[sabotage] if sabotage else []):
            p = os.path.join(prog, fichier)
            s = open(p, encoding="utf-8").read()
            if s.count(avant) != 1:
                return 2, "CIBLE INTROUVABLE (%d fois) dans %s : %r" % (s.count(avant), fichier, avant[:70])
            open(p, "w", encoding="utf-8").write(s.replace(avant, apres))
        try:
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--cas", prog, racine],
                               capture_output=True, text=True, timeout=900)
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return 1, "DÉLAI DÉPASSÉ"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def op(valeur, signal, sortie, net, cci, motif="TP"):
    """Rend une opération fictive en jetons illimités.
    ① RÔLE — fabriquer les cas construits. ② `cas`. ③ valeur, jour du signal, jour de sortie, gain net, CCI, motif.
    ④ — ⑤ UNE valeur : un dictionnaire. [rend: 1] ⑥ — ⑦ euros ; dates 2030 (aucune donnée réelle ne peut s'y glisser).
    ⑧ — ⑨ la date d'entrée n'est pas lue par le module ; elle vaut le jour du signal. ⑩ — ⑪ rend. [sort: non]"""
    return {"valeur": valeur, "date_signal": signal, "date_entree": signal, "date_sortie": sortie, "net": net,
            "cci": cci, "motif": motif}


def jours(n, debut="2030-01-01"):
    """Rend n jours fictifs consécutifs, AAAA-MM-JJ.
    ① RÔLE — un calendrier fictif. ② `cas`. ③ n, début. ④ — ⑤ UNE liste. [rend: 1] ⑥ jours consécutifs.
    ⑦ dates. ⑧ 2030 : hors de toute année réelle. ⑨ — ⑩ — ⑪ rend. [sort: non]"""
    import datetime as dt
    d0 = dt.date.fromisoformat(debut)
    return [(d0 + dt.timedelta(days=i)).isoformat() for i in range(n)]


def golden(prog, racine):
    """Rend le rejeu du golden : opérations un jeton, opérations illimitées rattachées à leurs signaux, séances.
    ① RÔLE — la VRAIE ligne (R-732) : C5-ETENDU-10 sur le témoin du golden, 2024-2026. ② `cas`.
    ③ `prog` : les programmes ; `racine` : les données. ④ le golden et son témoin conformes.
    ⑤ QUATRE valeurs : un jeton, illimitées, séances, période. [rend: 4] ⑥ `calibrer_sur_le_golden`, puis les signaux
    du module du calibrage du juge (comme lui), puis `rattacher_les_signaux`. ⑦ euros ; dates. ⑧ le rejeu est calibré
    au centime par MESURER_LES_INDICATEURS avant de servir (sinon ROUGE). ⑨ — ⑩ lit. ⑪ rend ; lève si non calibré.
    [sort: non]"""
    import MESURER_LES_INDICATEURS as M
    import MODULE_PARCOURS_A_UN_JETON as P
    ok, lignes, rendu = M.calibrer_sur_le_golden(racine)
    if not ok:
        raise RuntimeError("golden non retrouvé : %s" % lignes)
    JS = M.charger_les_briques(racine)["JS"]
    cours = JS.charger_cours(os.path.join(racine, TEMOIN))
    fin = rendu["periode"][1]
    sig = JS.signal_de_la_fiche(racine, dict(JS.SIGNAL_DU_CALIBRAGE, id="calibrage"))
    signaux = []
    for v in getattr(sig.module, "C5E10_UNIVERS", []):
        serie = cours.get(JS.cle_valeur(v)) or cours.get(v) or []
        for s in sig(serie):
            d = serie[s["i"]]["date"]
            if d <= fin:
                signaux.append({"valeur": v, "date_signal": d, "cci": s["cci"]})
    seances = sorted({x["date"] for s in cours.values() for x in s if x["date"] <= fin})
    return (P.rattacher_les_signaux(rendu["un_jeton"], signaux), P.rattacher_les_signaux(rendu["jetons_illimites"],
            signaux), seances, rendu["periode"])


def cas(prog, racine):
    """Joue les cas E1 à E10 sur les programmes du dossier `prog` et rend le nombre de rouges.
    ① RÔLE — Les épreuves elles-mêmes. ② CONTEXTE D'APPEL — `main`, en « --cas ». ③ ENTRÉE — `prog` : le dossier
    des programmes (copie) ; `racine` : les données. ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur :
    le nombre de cas rouges (une exception compte comme un rouge). [rend: 1] ⑥ TRAITEMENT — voir chaque cas.
    ⑦ UNITÉ — voir l'en-tête. ⑧ POURQUOI — une épreuve par propriété. ⑨ CE QUI CLOCHE — voir l'en-tête.
    ⑩ EFFET — affiche. ⑪ TERMINAISON — rend la main. [sort: non]"""
    sys.path.insert(0, prog)
    import MESURER_LES_INDICATEURS as M
    import MODULE_PARCOURS_A_UN_JETON as P
    J = M.charger_les_briques(racine)["MJ"]
    rouges = []
    memo = {}

    def ok(nom, vrai, detail=""):
        """Affiche un cas. ① RÔLE — une ligne VERT/ROUGE. ② `cas`. ③ nom, booléen, détail. ④ — ⑤ aucune. [rend: 0]
        ⑥ — ⑦ — ⑧ — ⑨ — ⑩ EFFET — affiche. ⑪ Rend la main. [sort: non]"""
        print("  %s %s%s" % ("VERT " if vrai else "ROUGE", nom, ("  — " + str(detail)) if detail else ""))
        if not vrai:
            rouges.append(nom)

    def leve(f, *a, **k):
        """Rend le nom de l'exception levée par f, ou None. ① RÔLE — tester un refus. ② `cas`. ③ f, arguments.
        ④ — ⑤ UNE valeur. [rend: 1] ⑥ appeler. ⑦ — ⑧ un refus doit LEVER. ⑨ — ⑩ — ⑪ rend. [sort: non]"""
        try:
            f(*a, **k)
        except Exception as e:  # noqa: BLE001 — on rend son nom, le cas juge
            return type(e).__name__
        return None

    def essai(nom, f):
        """Joue un groupe de cas ; une exception est un rouge. ① RÔLE — isoler les groupes. ② `cas`. ③ nom, fonction.
        ④ — ⑤ aucune. [rend: 0] ⑥ appeler. ⑦ — ⑧ R-734. ⑨ — ⑩ affiche. ⑪ rend. [sort: non]"""
        try:
            f()
        except Exception as e:  # noqa: BLE001 — toute chute d'un groupe est un rouge, nommé
            ok(nom + " (le groupe a levé)", False, "%s: %s" % (type(e).__name__, e))

    def g():
        """Le rejeu du golden, une fois. ① RÔLE — mémoriser. ② les cas. ③ — ④ — ⑤ UNE valeur. [rend: 1] ⑥ — ⑦ —
        ⑧ coût (2 s). ⑨ — ⑩ — ⑪ rend. [sort: non]"""
        if "g" not in memo:
            memo["g"] = golden(prog, racine)
        return memo["g"]

    def cles(ops):
        """Les (valeur, date du signal) d'une liste. ① RÔLE — comparer des parcours. ② les cas. ③ ops. ④ — ⑤ UNE
        liste. [rend: 1] ⑥ — ⑦ — ⑧ — ⑨ — ⑩ — ⑪ rend. [sort: non]"""
        return [(o["valeur"], o["date_signal"]) for o in ops]

    # E1 — LA RÈGLE DU JETON (TENIR_LES_POSITIONS.tenir) sur un cas construit : A tient le jeton du 07 au 10 ; B (08)
    # est ignoré ; C, signalé le 10, jour de la sortie de A, est PRIS (on clôture avant d'ouvrir) ; le 20, E (CCI −150)
    # passe avant D (CCI −50), plus survendue ; le 25, égalité de CCI → ordre alphabétique (F avant G).
    def e1():
        ops = [op("A", "2030-01-07", "2030-01-10", 100.0, -100), op("B", "2030-01-08", "2030-01-09", 50.0, -120),
               op("C", "2030-01-10", "2030-01-15", -80.0, -110), op("D", "2030-01-20", "2030-01-22", 10.0, -50),
               op("E", "2030-01-20", "2030-01-23", 20.0, -150), op("G", "2030-01-25", "2030-01-26", 5.0, -90),
               op("F", "2030-01-25", "2030-01-27", 6.0, -90)]
        r = P.prendre_en_un_jeton(ops, "2030-01-01", P.ORDRE_R207BIS, racine)
        ok("E1a la règle du jeton : A, C (jour de sortie de A), E (plus survendue), F (alphabétique)",
           [o["valeur"] for o in r["pris"]] == ["A", "C", "E", "F"], [o["valeur"] for o in r["pris"]])
        ok("E1b les ignorés sont dits, avec leur cause", sorted((o["valeur"], c) for o, c in r["ignores"]) ==
           [("B", "jeton occupé"), ("D", "jeton occupé"), ("G", "jeton occupé")], r["ignores"])
        ok("E1c l'ordre au hasard exige un tirage", leve(P.prendre_en_un_jeton, ops, "2030-01-01", P.ORDRE_AU_HASARD,
                                                         racine) == "ValueError")
    essai("E1", e1)

    # E2 — VRAIE LIGNE (R-732) : depuis les 100 opérations en jetons illimités du golden, la règle du direct retrouve
    # opération par opération les 44 opérations du golden un jeton (+58 800,00 €), que le circuit du soir a produites.
    def e2():
        uj, ill, seances, periode = g()
        r = P.prendre_en_un_jeton(ill, seances[0], P.ORDRE_R207BIS, racine)
        net = round(sum(o["net"] for o in r["pris"]), 2)
        ok("E2a 100 opérations illimitées lues", len(ill) == 100, len(ill))
        ok("E2b le parcours historique = le golden un jeton, opération par opération (44, +58 800,00 €)",
           cles(r["pris"]) == cles(sorted(uj, key=lambda o: o["date_signal"])) and net == 58800.0,
           "%d opérations, %+.2f €" % (len(r["pris"]), net))
        ok("E2c pris + ignorés = toutes les opérations", len(r["pris"]) + len(r["ignores"]) == len(ill))
    essai("E2", e2)

    # E3 — LA COUTURE : un départ à la première séance rend le parcours historique ; tout parcours tiré, sur le golden,
    # ne tient jamais deux positions (contrôle de `mesurer_les_indicateurs` en un jeton, qui LÈVE sur un chevauchement),
    # et un départ tardif reprend des opérations d'avant le départ (le parcours couvre toute la période).
    def e3():
        uj, ill, seances, periode = g()
        h = P.prendre_en_un_jeton(ill, seances[0], P.ORDRE_R207BIS, racine)
        t = P.tirer_les_parcours(ill, seances, P.DEPART_AU_HASARD, 300, racine, GRAINE)
        def chevauche(pris):
            """Dit si deux opérations d'un parcours se chevauchent (l'entrée de l'une avant la sortie de l'autre).
            ① RÔLE — la propriété « une position à la fois », écrite comme le contrôle de `mesurer_les_indicateurs`
            (« date_entree <= date_sortie » de la précédente, dans l'ordre des sorties). ② `e3`. ③ les opérations.
            ④ — ⑤ UNE valeur. [rend: 1] ⑥ ranger par sortie, comparer voisines. ⑦ dates. ⑧ appeler
            `mesurer_les_indicateurs` 300 fois coûtait une minute (son creux exact). ⑨ — ⑩ — ⑪ rend. [sort: non]"""
            r = sorted(pris, key=lambda o: (o["date_sortie"], o["date_entree"], o["valeur"]))
            return any(c["date_entree"] <= a["date_sortie"] for a, c in zip(r, r[1:]))
        chev = [p["depart"] for p in t if chevauche(p["pris"])]
        ok("E3a 300 parcours tirés : aucun ne tient deux positions à la fois", not chev, chev[:3])
        tard = [p for p in t if p["depart"] > "2025-06-01"]
        avant = [p for p in tard if any(o["date_signal"] < p["depart"] for o in p["pris"])]
        ok("E3b un départ tardif reprend des opérations d'avant le départ", tard and len(avant) == len(tard),
           "%d/%d" % (len(avant), len(tard)))
        ok("E3c départ à la première séance = historique",
           cles(P.prendre_en_un_jeton(ill, seances[0], P.ORDRE_R207BIS, racine)["pris"]) == cles(h["pris"]))
    essai("E3", e3)

    # E4 — LE CREUX EST LA MÉCANIQUE DE L'ALARME. a) VRAIE LIGNE : sur les 44 opérations du golden un jeton (aucun
    # chevauchement, aucun jour double), tout parcours au choix au hasard est l'historique : le creux rendu est celui de
    # `mesurer_les_indicateurs` en un jeton, 21 500 € (exact). b) Sur le golden illimité, le creux est
    # `seuils_1_sur_20_sur_5_ans` du mélange des opérations des parcours, au rythme moyen.
    def e4():
        uj, ill, seances, periode = g()
        m = P.mesurer_les_parcours(uj, periode, seances, P.CHOIX_AU_HASARD, 200, racine, GRAINE,
                                   tirages_du_seuil=2000)
        ref = M.mesurer_les_indicateurs([dict(o) for o in uj], "un_jeton", periode, racine)
        ok("E4a un seul parcours possible → même creux que l'alarme, 21 500 €",
           m["parcours_distincts"] == 1 and m["creux_1_sur_20_sur_5_ans_eur"] == ref["creux_1_sur_20_sur_5_ans_eur"]
           == 21500.0, "%s distinct(s), %s € contre %s €" % (m["parcours_distincts"], m["creux_1_sur_20_sur_5_ans_eur"],
                                                          ref["creux_1_sur_20_sur_5_ans_eur"]))
        m2 = P.mesurer_les_parcours(ill, periode, seances, P.DEPART_AU_HASARD, 200, racine, GRAINE,
                                    tirages_du_seuil=2000)
        t = P.tirer_les_parcours(ill, seances, P.DEPART_AU_HASARD, 200, racine, GRAINE)
        annees = M.annees_de_la_periode(periode)
        nets = [[float(o["net"]) for o in p["pris"]] for p in t]
        attendu = M.seuils_1_sur_20_sur_5_ans([x for n in nets for x in n], sum(len(n) for n in nets) / len(nets)
                                              / annees, racine, 2000, GRAINE)
        ok("E4b creux = seuils_1_sur_20_sur_5_ans(mélange des parcours, rythme moyen)",
           m2["creux_1_sur_20_sur_5_ans_eur"] == attendu["creux_eur"] and m2["parcours_distincts"] > 1,
           "%s € contre %s € (%d parcours distincts)" % (m2["creux_1_sur_20_sur_5_ans_eur"], attendu["creux_eur"],
                                                         m2["parcours_distincts"]))
        # c) LE RYTHME EST LA MOYENNE DES PARCOURS : cas construit où les parcours n'ont pas le même nombre
        # d'opérations (A, longue, bloque dix opérations courtes ; un départ après sa sortie ne prend qu'elle).
        cal = jours(730)
        ops = [op("A", cal[0], cal[400], -1000.0, -100)] + [
            op("B%d" % i, cal[10 + 20 * i], cal[15 + 20 * i], -1000.0 if i % 2 else 500.0, -100) for i in range(10)]
        per = (cal[0], cal[-1])
        mc = P.mesurer_les_parcours(ops, per, cal, P.DEPART_AU_HASARD, 300, racine, GRAINE, tirages_du_seuil=500)
        t = P.tirer_les_parcours(ops, cal, P.DEPART_AU_HASARD, 300, racine, GRAINE)
        an = M.annees_de_la_periode(per)
        melange = [o["net"] for p in t for o in p["pris"]]
        moyen = M.seuils_1_sur_20_sur_5_ans(melange, len(melange) / len(t) / an, racine, 500, GRAINE)["creux_eur"]
        plus = M.seuils_1_sur_20_sur_5_ans(melange, max(len(p["pris"]) for p in t) / an, racine, 500,
                                           GRAINE)["creux_eur"]
        ok("E4c rythme = moyenne des parcours (le cas distingue moyenne et maximum)",
           mc["creux_1_sur_20_sur_5_ans_eur"] == moyen != plus,
           "%s € ; moyenne %s €, maximum %s €" % (mc["creux_1_sur_20_sur_5_ans_eur"], moyen, plus))
    essai("E4", e4)

    # E5 — LE GAIN PAR AN AU PIRE EST LE RANG 5 % DES PARCOURS : sur un cas construit, deux départs donnent deux
    # parcours, l'un à +1 000 €, l'autre à −1 000 € ; le rang 5 % des gains par an vaut le pire quand il pèse plus de
    # 5 %, et la médiane est au-dessus du pire.
    def e5():
        uj, ill, seances, periode = g()
        m = P.mesurer_les_parcours(ill, periode, seances, P.DEPART_AU_HASARD, 400, racine, GRAINE,
                                   tirages_du_seuil=2000)
        t = P.tirer_les_parcours(ill, seances, P.DEPART_AU_HASARD, 400, racine, GRAINE)
        annees = M.annees_de_la_periode(periode)
        gains = sorted(sum(o["net"] for o in p["pris"]) / annees for p in t)
        ok("E5a au pire = la valeur de rang 5 % des gains par an des parcours",
           abs(m["gain_net_par_an_au_pire_eur"] - J.valeur_au_rang(gains, 0.05)) < 1e-6,
           "%.2f contre %.2f" % (m["gain_net_par_an_au_pire_eur"], J.valeur_au_rang(gains, 0.05)))
        ok("E5b au pire < médiane sur le golden (des parcours différents)",
           m["gain_net_par_an_au_pire_eur"] < m["gain_net_par_an_median_eur"],
           "%.2f < %.2f" % (m["gain_net_par_an_au_pire_eur"], m["gain_net_par_an_median_eur"]))
        cal = jours(40)
        ops = [op("A", cal[0], cal[20], -1000.0, -100), op("B", cal[10], cal[12], 1000.0, -100)]
        mc = P.mesurer_les_parcours(ops, (cal[0], cal[-1]), cal, P.DEPART_AU_HASARD, 1000, racine, GRAINE,
                                    tirages_du_seuil=500)
        an = M.annees_de_la_periode((cal[0], cal[-1]))
        ok("E5c cas construit : au pire = le parcours perdant (−1 000 €), part des gagnants entre 0 et 1",
           abs(mc["gain_net_par_an_au_pire_eur"] - (-1000.0 / an)) < 1e-6 and 0 < mc["part_des_parcours_gagnants"] < 1,
           "%.2f €/an ; part %.3f" % (mc["gain_net_par_an_au_pire_eur"], mc["part_des_parcours_gagnants"]))
        ok("E5d la part des parcours gagnants ne décide rien : son seuil est « À MESURER »",
           mc["seuil_des_parcours_gagnants"].startswith("À MESURER"))
        ok("E5e les mesures ① et ④ ne sont pas inventées", m["mesure_1_wilson"].startswith("NON PROGRAMMÉE")
           and m["mesure_4_departage"].startswith("NON PROGRAMMÉE"))
    essai("E5", e5)

    # E6 — PRIS CONTRE IGNORÉS : 30 jours à deux signaux, sorties le lendemain ; a) le plus survendu PERD toujours :
    # la règle prend les plus mauvais → ALERTE ; b) il GAGNE toujours → RIEN NE LE MONTRE ; les grappes comptent les
    # 30 jours, premier contre suivant.
    def e6():
        cal = jours(1100)  # un jour double tous les 36 jours : 10 opérations par an, un creux sur 5 ans peu coûteux
        for nom, perd, attendu in (("a", -2800.0, "ALERTE"), ("b", 3700.0, "RIEN NE LE MONTRE")):
            ops = []
            for i in range(30):
                d = cal[36 * i]
                ops.append(op("BAS%02d" % i, d, cal[36 * i + 1], perd, -200))
                ops.append(op("HAUT%02d" % i, d, cal[36 * i + 1], 3700.0 if perd < 0 else -2800.0, -50))
            m = P.mesurer_les_parcours(ops, (cal[0], cal[-1]), cal, P.CHOIX_AU_HASARD, 500, racine, GRAINE,
                                       tirages_du_seuil=500)
            pi = m["pris_et_ignores"]
            ok("E6%s le plus survendu %s → %s" % (nom, "perd" if perd < 0 else "gagne", attendu), pi["etat"] == attendu,
               "%s, part des parcours pas mieux %.3f" % (pi["etat"], pi["part_des_parcours_pas_mieux"]))
            ok("E6%s grappes : 30 premiers contre 30 suivants" % nom,
               pi["grappes"]["grappes"] == 30 and pi["grappes"]["suivants"]["operations"] == 30
               and pi["grappes"]["premiers"]["taux_reussite_pct"] == (0.0 if perd < 0 else 100.0), pi["grappes"])
    essai("E6", e6)

    # E7 — LES NON TERMINÉES (A-1100) : une opération restée ouverte à la fin garde le jeton jusqu'au bout et n'entre
    # dans aucun gain ; elle est comptée à part.
    def e7():
        cal = jours(30)
        ops = [op("A", cal[0], cal[2], 500.0, -100), op("Z", cal[5], cal[29], 9999.0, -100, motif="FIN_DES_DONNEES"),
               op("B", cal[10], cal[12], 700.0, -100)]
        m = P.mesurer_les_parcours(ops, (cal[0], cal[-1]), cal, P.CHOIX_AU_HASARD, 20, racine, GRAINE,
                                   tirages_du_seuil=200)
        ok("E7a la NON TERMINÉE n'entre pas dans le gain, et bloque B", m["historique"]["gain_net_eur"] == 500.0
           and m["historique"]["non_terminees"] == 1, m["historique"])
        ok("E7b elle est comptée à part dans les parcours", m["parcours_avec_non_terminee"] == 20)
    essai("E7", e7)

    # E8 — LES REFUS : façon de tirer inconnue, aucune façon par défaut, nombre de parcours nul, période nulle.
    def e8():
        cal = jours(5)
        ops = [op("A", cal[0], cal[1], 1.0, -100)]
        ok("E8a façon de tirer inconnue → ValueError",
           leve(P.tirer_les_parcours, ops, cal, "au_flair", 3, racine, 1) == "ValueError")
        ok("E8b aucune façon de tirer par défaut", leve(P.mesurer_les_parcours, ops, (cal[0], cal[-1]), cal,
                                                        nombre=3, racine=racine, graine=1) == "TypeError")
        ok("E8c nombre de parcours nul → ValueError",
           leve(P.tirer_les_parcours, ops, cal, P.DEPART_AU_HASARD, 0, racine, 1) == "ValueError")
        ok("E8d période de 0 jour → ValueError", leve(P.mesurer_les_parcours, ops, (cal[0], cal[0]), cal,
                                                      P.DEPART_AU_HASARD, 3, racine, 1) == "ValueError")
    essai("E8", e8)

    # E9 — LE HASARD EST REPRODUCTIBLE : même graine → mêmes parcours ; autre graine → d'autres départs ; le hasard
    # global n'est pas touché.
    def e9():
        import random
        uj, ill, seances, periode = g()
        random.seed(7)
        avant = random.random()
        random.seed(7)
        a = P.tirer_les_parcours(ill, seances, P.DEPART_AU_HASARD, 50, racine, GRAINE)
        apres = random.random()
        b = P.tirer_les_parcours(ill, seances, P.DEPART_AU_HASARD, 50, racine, GRAINE)
        c = P.tirer_les_parcours(ill, seances, P.DEPART_AU_HASARD, 50, racine, GRAINE + 1)
        ok("E9a même graine → mêmes parcours", [p["depart"] for p in a] == [p["depart"] for p in b])
        ok("E9b autre graine → d'autres départs", [p["depart"] for p in a] != [p["depart"] for p in c])
        ok("E9c le hasard global n'est pas touché", avant == apres)
    essai("E9", e9)

    # E10 — R-708 : le module APPELLE departager_r207bis, seuils_1_sur_20_sur_5_ans, valeur_au_rang et
    # annees_de_la_periode, et ne range rien par le CCI lui-même.
    def e10():
        src = open(os.path.join(prog, MP), encoding="utf-8").read()
        arbre = ast.parse(src)
        appels = {n.func.attr for n in ast.walk(arbre) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        manque = {"departager_r207bis", "seuils_1_sur_20_sur_5_ans", "valeur_au_rang", "annees_de_la_periode"} - appels
        ok("E10a les briques existantes sont appelées", not manque, manque)
        tri_cci = [n.lineno for n in ast.walk(arbre) if isinstance(n, ast.Lambda) and "cci" in ast.unparse(n.body)]
        ok("E10b aucun tri par le CCI dans le module (R-207bis vit dans TENIR_LES_POSITIONS)", not tri_cci, tri_cci)
    essai("E10", e10)

    print("== %d rouge(s)" % len(rouges))
    return len(rouges)


def mesurer(racine):
    """Affiche les mesures de l'étape 6 sur C5-ETENDU-10 2024-2026 (golden), 2 000 parcours, les deux façons de tirer.
    ① RÔLE — Montrer la mesure sur une vraie ligne, SANS juger : C5 a été réglée sur ces années. ② `main`, option
    « --mesurer ». ③ `racine`. ④ celles de `golden`. ⑤ aucune : affiche. [rend: 0] ⑥ rejeu du golden, puis
    `mesurer_les_parcours` aux tirages par défaut du creux. ⑦ euros ; euros par an ; parts. ⑧ la note de livraison
    cite ces chiffres : ils se relancent. ⑨ environ 35 s. ⑩ affiche. ⑪ rend la main. [sort: non]"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import MODULE_PARCOURS_A_UN_JETON as P
    uj, ill, seances, periode = golden(os.path.join(racine, "programmes"), racine)
    for t in P.TIRAGES:
        m = P.mesurer_les_parcours(ill, periode, seances, t, 2000, racine, GRAINE)
        h, pi = m["historique"], m["pris_et_ignores"]
        print("%s : %d parcours, %d distincts ; creux 1/20 sur 5 ans %.2f € (%s, marge %.2f-%.2f) ; gain par an au "
              "pire %.2f €, médiane %.2f € ; part gagnante %.3f ; %.2f opérations par an" % (
                  t, m["parcours"], m["parcours_distincts"], m["creux_1_sur_20_sur_5_ans_eur"], m["creux_methode"],
                  m["creux_marge_basse_eur"], m["creux_marge_haute_eur"], m["gain_net_par_an_au_pire_eur"],
                  m["gain_net_par_an_median_eur"], m["part_des_parcours_gagnants"], m["operations_par_an_moyen"]))
        print("  historique : %d opérations, %.2f €, %.2f € par an, creux 1/20 sur 5 ans %.2f € (%s)" % (
            h["operations"], h["gain_net_eur"], h["gain_net_par_an_eur"], h["creux_1_sur_20_sur_5_ans_eur"],
            h["creux_methode"]))
        print("  pris %d (%.1f %%, %.2f €) ; ignorés %d (%.1f %%, %.2f €) ; grappes %d : premiers %.1f %%, suivants "
              "%.1f %% ; part des parcours pas mieux %.4f → %s" % (
                  pi["pris"]["operations"], pi["pris"]["taux_reussite_pct"], pi["pris"]["gain_moyen_eur"],
                  pi["ignores"]["operations"], pi["ignores"]["taux_reussite_pct"], pi["ignores"]["gain_moyen_eur"],
                  pi["grappes"]["grappes"], pi["grappes"]["premiers"]["taux_reussite_pct"],
                  pi["grappes"]["suivants"]["taux_reussite_pct"], pi["part_des_parcours_pas_mieux"], pi["etat"]))


def main():
    """Point d'entrée : Z0, puis les sabotages demandés.
    ① RÔLE — Orchestrer. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — sys.argv. ④ — ⑤ SORTIE — par
    sys.exit. [rend: rien] ⑥ « --cas » : jouer ; sinon Z0 puis sabotages. ⑦ — ⑧ R-731, R-734. ⑨ — ⑩ affiche.
    ⑪ TERMINAISON — sort par sys.exit. [sort: oui — code de sortie]"""
    a = sys.argv[1:]
    if a[:1] == ["--cas"]:
        sys.exit(1 if cas(a[1], a[2]) else 0)
    if not a:
        print("usage : <racine> [--saboter | <sabotage>…]")
        sys.exit(2)
    racine = os.path.abspath(a[0])
    if a[1:2] == ["--mesurer"]:
        mesurer(racine)
        sys.exit(0)
    for f in (os.path.join("programmes", MP), TEMOIN):
        if not os.path.isfile(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            sys.exit(2)
    code, sortie = lancer(racine, None)
    print("== Z0 (code intact)\n" + sortie)
    if code != 0:
        print("VERDICT : Z0 ROUGE")
        sys.exit(2 if code == 2 else 1)
    noms = list(SABOTAGES) if a[1:2] == ["--saboter"] else a[1:]
    muets, introuvables = [], []
    for nom in noms:
        if nom not in SABOTAGES:
            print("SABOTAGE INCONNU : %s" % nom)
            sys.exit(2)
        code, sortie = lancer(racine, nom)
        rougis = [l.strip() for l in sortie.splitlines() if l.strip().startswith("ROUGE")]
        if code == 2:
            introuvables.append(nom)
            print("  %s : %s" % (nom, sortie.strip()[:160]))
        elif code == 0 or not rougis:
            muets.append(nom)
            print("  %s : MUET — aucun cas n'a rougi" % nom)
        else:
            print("  %s : mord (%d rouge(s)) — %s" % (nom, len(rougis), rougis[0][:110]))
    if noms:
        print("== %d sabotage(s), %d muet(s), %d introuvable(s)" % (len(noms), len(muets), len(introuvables)))
    print("VERDICT : %s" % ("conforme" if not muets and not introuvables else "NON CONFORME"))
    sys.exit(2 if introuvables else (1 if muets else 0))


if __name__ == "__main__":
    main()
