#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DE LA RESSEMBLANCE ET DU COMPTE DES ESSAIS (lot W2c du plan R505) — Ven 27-11-2026.
Simulation uniquement : des séries synthétiques et des versions réelles de C5 sur 2024-2026 (ses années de RÉGLAGE) ;
aucune stratégie n'est jouée sur 2000-2023 ni sur les 30 % d'une autre stratégie, aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — R-505 version 2 : k compte les versions réellement envoyées au juge, regroupées par la ressemblance
mesurée, valeur la plus prudente, plus les autres stratégies déjà réellement jugées (A-772, A-1082, « À PRÉCISER » ⑨) ;
deux stratégies se ressemblent pour la mise en service si leurs gains quotidiens sont corrélés à 0,5 ou plus OU si
elles tiennent la même action le même jour au moins une fois sur deux (A-791). Ces épreuves prouvent que
programmes/COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py redonne les chiffres publiés de l'expert et du collège du 14-11-2026
sur de VRAIES versions de C5 (E1, E5), et chaque propriété sur des cas construits (E2 à E4, E6 à E11). Une épreuve qui
reste verte quand on retire ce qu'elle teste est une décoration (R-731) : `--saboter` casse le programme de chaque
façon de la table SABOTAGES, et chacune doit faire rougir au moins un cas.

USAGE : python3 -B tests/EPREUVES_DE_LA_RESSEMBLANCE_Ven_27-11-2026.py <racine> [--saboter | <sabotage>]
CODE : 0 si Z0 est vert et si chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de sabotage
est introuvable, si le nom est inconnu, ou si une donnée manque (R-734).

① RÔLE — Prouver que le lot W2c fait ce que dit sa note, et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis avec
  « --saboter ». Ce programme se relance lui-même en « --cas <copie> <racine> <matériau> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py, MODULE_JUGEMENT.py,
  CONTRATS_DES_FICHIERS.py, COMMUN.py, JUGE_DES_STRATEGIES.py, JOUER_LES_VERSIONS.py ; gouvernance/REGISTRE_REGLES.md ;
  donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv et son témoin ; donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv ;
  numpy installé.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① UNE FOIS : rejouer par le juge les 245 versions « TTE seule » de C5 et cinq versions nommées, sur la
  période et au barème du témoin, et ranger leurs opérations et les cours utiles dans un fichier temporaire (le
  « matériau ») · ② pour Z0 puis chaque sabotage : copier les quatre programmes dans un dossier temporaire, appliquer le
  sabotage (un texte présent UNE fois), relancer ce fichier en « --cas » · ③ Z0 doit être vert ; un sabotage doit
  faire rougir au moins un cas.
⑦ UNITÉ — Gains en euros ; k en essais ; corrélations et parts sans unité.
⑧ POURQUOI — R-731 (épreuves et sabotages) ; R-732 (cas tirés de vraies lignes : E1 sur les 245 versions TTE de
  COMBINATOIRE_C5E10-OBS-V1_E01.csv, E5 sur les versions 0144, 0529, 2454, 0924 et 0915) ; R-734. Le matériau est
  fabriqué UNE fois par le parent parce que les sabotages ne touchent que COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py :
  rejouer le juge à chaque sabotage coûterait 20 fois 15 s pour rien.
⑨ CE QUI CLOCHE — ① E1 compare à « 14.5 », le k publié par l'expert pour les 245 versions TTE (complement_par_valeur.py,
  premier calcul après la graine), au dixième ; un autre LAPACK pourrait signer autrement les vecteurs propres et donner
  un autre tirage (voir `_racine_de_la_correlation`, ⑨) : la tolérance est donc ±5 % (bruit mesuré par la
  contre-expertise), et l'égalité au dixième est affichée sans être exigée. ② La ressemblance d'IND-001-RETEST n'est
  pas éprouvée : la rejouer sur 2024-2026 serait regarder ses années d'examen (préambule du plan, §4). ③ Le calibrage
  complet des 2 695 versions n'est pas ici (plus de 2 minutes) : épreuve longue « EssaisRessemblance ».
⑩ EFFET — Écrit et efface des dossiers et fichiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 300 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""

import os
import pickle
import shutil
import subprocess
import sys
import tempfile

P = "COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py"
PROGRAMMES = (P, "MODULE_JUGEMENT.py", "CONTRATS_DES_FICHIERS.py", "COMMUN.py")
VERSIONS_NOMMEES = ("C5E10-OBS-V1-E01-0144", "C5E10-OBS-V1-E01-0529", "C5E10-OBS-V1-E01-2454",
                    "C5E10-OBS-V1-E01-0924", "C5E10-OBS-V1-E01-0915")

# LES SABOTAGES : {nom : [(fichier, texte présent une fois, remplaçant)]}. Chacun retire ou fausse UNE propriété.
SABOTAGES = {
    "S01_prudent_le_plus_bas": [(P, '"k_prudent": max([k_plein] + k_blocs)', '"k_prudent": min([k_plein] + k_blocs)')],
    "S02_quantile_a_alpha": [(P, "np.concatenate(maxima), 1.0 - alpha", "np.concatenate(maxima), alpha")],
    "S03_moyenne_au_lieu_du_maximum": [(P, "TIRAGES_PAR_LOT))).max(axis=0)", "TIRAGES_PAR_LOT))).mean(axis=0)")],
    "S04_arrondi_vers_le_bas": [(P, 'int(math.ceil(mesure["k_prudent"] - 1e-9))', 'int(mesure["k_prudent"])')],
    "S05_k_non_borne_a_n": [(P, 'k_versions = min(int(math.ceil(mesure["k_prudent"] - 1e-9)), mesure["n_versions"])',
                             'k_versions = int(math.ceil(mesure["k_prudent"] - 1e-9))')],
    "S06_non_jugeable_compte": [(P, 'if d < limite and v["verdict"] != "NON JUGEABLE":', 'if d < limite:')],
    "S07_verdicts_futurs_comptes": [(P, 'if d < limite and v["verdict"] != "NON JUGEABLE":',
                                     'if v["verdict"] != "NON JUGEABLE":')],
    "S08_chevauchement_sur_la_plus_grande": [(P, "return len(a & b) / min(len(a), len(b))",
                                              "return len(a & b) / max(len(a), len(b))")],
    "S09_strictement_plus_d_une_fois_sur_deux": [(P, '("chevauchement", chev >= s_chev)', '("chevauchement", chev > s_chev)')],
    "S10_et_au_lieu_de_ou": [(P, '"semblables": bool(par)', '"semblables": len(par) == 2')],
    "S11_dates_hors_calendrier_ignorees": [(P, "    if hors:\n        raise ValueError", "    if False:\n        raise ValueError")],
    "S12_jour_de_sortie_exclu": [(P, 'if o["date_entree"] <= d <= o["date_sortie"])', 'if o["date_entree"] <= d < o["date_sortie"])')],
    "S13_seuils_en_dur": [(P, "    return rendu[0], rendu[1]\n", "    return 0.7, 0.7\n")],
    "S14_risque_en_dur": [(P, "        raise ValueError(\"risque global illisible à la table de la loi : %s\" % (raison or alpha))\n    return alpha\n",
                           "        raise ValueError(\"risque global illisible à la table de la loi : %s\" % (raison or alpha))\n    return 0.05\n")],
    "S15_service_compare_au_dernier_seul": [(P, "        for s in en_service:\n", "        for s in en_service[-1:]:\n")],
    "S16_versions_muettes_admises": [(P, "    if muettes:\n        raise ValueError", "    if False:\n        raise ValueError")],
    "S17_frais_oublies": [(P, '        s[rang[o["date_sortie"]]] -= o["frais"]\n', "")],
    "S18_reechantillonnage_absent": [(P, "    for _ in range(reechantillonnages):\n", "    for _ in range(0):\n")],
    "S19_graine_non_fixee": [(P, "    rng = np.random.default_rng(graine)\n", "    rng = np.random.default_rng()\n")],
}


def fabriquer_le_materiau(racine, chemin):
    """Rejoue par le juge les versions des cas réels et range opérations et cours dans un fichier.

    ① RÔLE — Le matériau des cas tirés de vraies lignes (R-732), fabriqué une fois. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` ; `chemin` : le fichier à écrire. ④ CONDITIONS D'ENTRÉE — voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le nombre d'écarts au témoin. [rend: 1]
    ⑥ TRAITEMENT — `COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE._preparer_c5` et `_jouer_une` (le jeu du calibrage) sur les
      245 versions « TTE » et les versions nommées ; calendrier = séances des valeurs jouées sur la période du témoin. ⑦ UNITÉ — — ⑧ POURQUOI — les mêmes fonctions que le calibrage (R-708).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — écrit `chemin`. ⑪ TERMINAISON — rend la main. [sort: non]"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE as K
    K._initialiser(racine)
    p = K._ETAT["p"]
    versions = p["versions"]
    tte = [v for v in versions if v["univers"] == "TTE"]
    nommees = [v for v in versions if v["id_version"] in VERSIONS_NOMMEES]
    res = [K._jouer_une(v) for v in tte + nommees]
    # les valeurs jouées, sous le nom que le juge leur donne (les opérations portent le nom, l'univers le mnémonique) ;
    # les versions nommées 0144, 0529 et 2454 sont de l'univers entier : leurs opérations couvrent les 10 valeurs
    valeurs = sorted({o["valeur"] for _, ops, _ in res for o in ops})
    t0 = p["temoin"][versions[0]["id_version"]]
    cal = sorted({b["date"] for m in valeurs for b in p["cours"][m]
                  if t0["periode_debut"] <= b["date"] <= t0["periode_fin"]})
    jours = set(cal)
    close = {m: {b["date"]: b["close"] for b in p["cours"][m] if b["date"] in jours} for m in valeurs}
    with open(chemin, "wb") as f:
        pickle.dump({"ops": {vid: o for vid, o, _ in res}, "tte": [v["id_version"] for v in tte], "cal": cal,
                     "close": close}, f)
    return sum(not ok for _, _, ok in res)


def lancer(racine, sabotage, materiau):
    """Copie les programmes, applique un sabotage, relance ce fichier en « --cas » et rend (code, sortie).

    ① RÔLE — Un passage d'épreuves sur une copie, intacte (Z0) ou sabotée. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` ; `sabotage` : un nom de SABOTAGES ou None ; `materiau`. ④ CONDITIONS D'ENTRÉE — les programmes
    existent. ⑤ SORTIE — DEUX valeurs : le code de la relance (2 si une cible est introuvable) et sa sortie. [rend: 2]
    ⑥ TRAITEMENT — copier, remplacer (texte présent une fois exactement), relancer avec un délai de 300 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731 : le sabotage porte sur une COPIE, jamais sur le dépôt.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — un dossier temporaire, effacé. ⑪ TERMINAISON — bornée à 300 s. [sort: non]"""
    tmp = tempfile.mkdtemp(prefix="W2c_epreuve_")
    try:
        prog = os.path.join(tmp, "programmes")
        os.makedirs(prog)
        for n in PROGRAMMES:
            shutil.copy(os.path.join(racine, "programmes", n), prog)
        for fichier, avant, apres in (SABOTAGES[sabotage] if sabotage else []):
            chemin = os.path.join(prog, fichier)
            s = open(chemin, encoding="utf-8").read()
            if s.count(avant) != 1:
                return 2, "CIBLE INTROUVABLE (%d fois) dans %s : %r" % (s.count(avant), fichier, avant[:70])
            open(chemin, "w", encoding="utf-8").write(s.replace(avant, apres))
        try:
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--cas", prog, racine, materiau],
                               capture_output=True, text=True, timeout=300)
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return 1, "DÉLAI DÉPASSÉ"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cas(prog, racine, materiau):
    """Joue les cas E1 à E11 sur les programmes du dossier `prog` et rend le nombre de rouges.

    ① RÔLE — Les épreuves elles-mêmes. ② CONTEXTE D'APPEL — `main`, en « --cas ». ③ ENTRÉE — `prog` : le dossier des
    programmes (copie) ; `racine` : les données ; `materiau`. ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE
    valeur : le nombre de cas rouges (une exception compte comme un rouge). [rend: 1] ⑥ TRAITEMENT — voir chaque cas.
    ⑦ UNITÉ — voir l'en-tête. ⑧ POURQUOI — une épreuve par propriété. ⑨ CE QUI CLOCHE — voir l'en-tête.
    ⑩ EFFET — écrit des dossiers temporaires (E3). ⑪ TERMINAISON — rend la main. [sort: non]"""
    sys.path.insert(0, prog)
    import json
    import math
    import numpy as np
    import CONTRATS_DES_FICHIERS  # noqa: F401 — chargés depuis la COPIE avant que le programme n'ajoute la racine
    import MODULE_JUGEMENT  # noqa: F401
    import COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE as K
    assert os.path.dirname(os.path.abspath(K.__file__)) == os.path.abspath(prog), K.__file__
    with open(materiau, "rb") as f:
        mat = pickle.load(f)
    cal, close = mat["cal"], mat["close"]
    rang = {d: i for i, d in enumerate(cal)}
    dates_m = {m: [d for d in sorted(close[m]) if d in rang] for m in close}
    table = K.lire_les_seuils(racine)
    rouges = []

    def ok(nom, vrai, detail=""):
        """Affiche un cas. ① RÔLE — une ligne VERT/ROUGE. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, booléen,
        détail. ④ — ⑤ SORTIE — aucune. [rend: 0] ⑥ — ⑦ — ⑧ — ⑨ — ⑩ EFFET — affiche. ⑪ Rend la main. [sort: non]"""
        print("  %s %s%s" % ("VERT " if vrai else "ROUGE", nom, ("  — " + str(detail)) if detail else ""))
        if not vrai:
            rouges.append(nom)

    def leve(f, *a):
        """Rend True si f(*a) lève ValueError. ① RÔLE — tester un refus. ② `cas`. ③ f, arguments. ④ — ⑤ booléen.
        [rend: 1] ⑥ appeler. ⑦ — ⑧ un refus doit LEVER, jamais rendre un chiffre. ⑨ — ⑩ — ⑪ rend. [sort: non]"""
        try:
            f(*a)
        except ValueError:
            return True
        return False

    def essai(nom, f):
        """Joue un groupe de cas ; une exception est un rouge. ① RÔLE — isoler les groupes. ② `cas`. ③ nom, fonction.
        ④ — ⑤ aucune. [rend: 0] ⑥ appeler. ⑦ — ⑧ R-734. ⑨ — ⑩ affiche. ⑪ rend. [sort: non]"""
        try:
            f()
        except Exception as e:  # noqa: BLE001 — toute chute d'un groupe est un rouge, nommé
            ok(nom + " (le groupe a levé)", False, "%s: %s" % (type(e).__name__, e))

    def serie(vid, un_jeton=False):
        """Rend la série valorisée chaque soir d'une version du matériau. ① RÔLE — raccourci. ② `cas`. ③ vid.
        ④ — ⑤ UNE valeur : le tableau. [rend: 1] ⑥ `_serie_valorisee_chaque_soir`. ⑦ euros. ⑧ — ⑨ — ⑩ — ⑪ rend.
        [sort: non]"""
        o = K._un_jeton(mat["ops"][vid]) if un_jeton else mat["ops"][vid]
        return K._serie_valorisee_chaque_soir(o, close, dates_m, rang)

    # E1 — CALIBRAGE DU k SUR UNE VRAIE FAMILLE : les 245 versions « TTE seule » de C5 (expert, complement_par_valeur.py :
    # « univers TTE : 245 versions -> k équivalent 14.5 », premier calcul après la graine 20261114, 20 000 tirages).
    def e1():
        X = np.array([serie(v) for v in mat["tte"]])
        recon = max(abs(X[j].sum() - sum(o["net"] for o in mat["ops"][v])) for j, v in enumerate(mat["tte"]))
        ok("E1a 644 séances, série = gain net de chaque version au centime (expert : écart 0,000000 €)",
           len(cal) == 644 and recon < 0.01, (len(cal), recon))
        rng = np.random.default_rng(K.GRAINE)
        k = K.k_de_la_barre(K._barre_du_maximum(K._racine_de_la_correlation(X), rng, K.TIRAGES, 0.05), 0.05)
        ok("E1b k équivalent des 245 versions TTE à ±5 %% de 14,5 (publié) ; égal au dixième : %s" % (round(k, 1) == 14.5),
           abs(k - 14.5) <= 0.05 * 14.5, round(k, 3))
        m = K.mesurer_le_nombre_effectif(X, 0.05)
        ok("E1c la mesure complète : k plein = ce calcul, k prudent ≥ k plein, entre 1 et 245",
           abs(m["k_plein"] - k) < 1e-9 and m["k_prudent"] >= m["k_plein"] and 1 <= m["k_prudent"] <= 245,
           (round(m["k_plein"], 2), round(m["k_prudent"], 2)))
    essai("E1", e1)

    # E2 — PROPRIÉTÉS DE LA MESURE SUR DES SÉRIES CONSTRUITES
    def e2():
        g = np.random.default_rng(5)
        base = g.standard_normal(600)
        m = K.mesurer_le_nombre_effectif([base] * 30, 0.05, reechantillonnages=0)
        ok("E2a 30 copies d'une même série valent UN essai (k plein dans [0,9 ; 1,1])", 0.9 <= m["k_plein"] <= 1.1,
           m["k_plein"])
        indep = g.standard_normal((40, 600))
        m = K.mesurer_le_nombre_effectif(indep, 0.05, reechantillonnages=0)
        ok("E2b 40 séries indépendantes valent environ 40 essais (k plein dans [34 ; 46])", 34 <= m["k_plein"] <= 46,
           m["k_plein"])
        corr = indep[:5] + 0.0
        m1 = K.mesurer_le_nombre_effectif(corr, 0.05)
        m2 = K.mesurer_le_nombre_effectif(corr, 0.05)
        ok("E2c même entrée, même sortie (déterministe, graine fixe)", m1 == m2)
        echelle = corr.copy()
        echelle[2] *= 1000.0
        m3 = K.mesurer_le_nombre_effectif(echelle, 0.05)
        ok("E2d l'unité d'une série ne change pas k (×1 000 sur une ligne)", abs(m3["k_plein"] - m1["k_plein"]) < 1e-6,
           (m1["k_plein"], m3["k_plein"]))
        ok("E2e k prudent = le plus haut du calcul plein et des rééchantillonnages, 10 rééchantillonnages",
           len(m1["k_par_reechantillonnage"]) == 10
           and m1["k_prudent"] == max([m1["k_plein"]] + m1["k_par_reechantillonnage"])
           and max(m1["k_par_reechantillonnage"]) > m1["k_plein"], (m1["k_plein"], max(m1["k_par_reechantillonnage"])))
        muette = np.vstack([indep[:3], np.zeros((1, 600))])
        try:
            K.mesurer_le_nombre_effectif(muette, 0.05)
            motif = "aucun refus"
        except ValueError as e:
            motif = str(e)
        ok("E2f une version sans aucun gain non nul : refusée AVANT tout calcul, nommée par son rang (jamais un k, ni une "
           "erreur d'algèbre plus loin)", "sans aucun gain non nul (rangs [3])" in motif, motif[:90])
        trou = indep[:3].copy()
        trou[1, 7] = np.nan
        ok("E2g une valeur manquante : refus", leve(K.mesurer_le_nombre_effectif, trou, 0.05))
        ok("E2h une seule version : k = 1 sans tirage", K.mesurer_le_nombre_effectif(indep[:1], 0.05)["k_prudent"] == 1.0)
        ok("E2i k de la barre de Bonferroni de 69 essais = 69 (3,1847, expert)",
           abs(K.k_de_la_barre(3.18467, 0.05) - 69) < 0.05, K.k_de_la_barre(3.18467, 0.05))
    essai("E2", e2)

    # E3 — LE COMPTE k DU JUGE : arrondi prudent, borné à n, plus les verdicts déjà rendus (A-1082)
    def e3():
        tmp = tempfile.mkdtemp(prefix="W2c_verdicts_")
        try:
            g = np.random.default_rng(11)
            s = g.standard_normal((3, 300))
            s[1] = s[0] + 0.3 * s[1]
            r = K.compter_les_essais(s, tmp, "2026-11-27T21:00:00+01:00", table=table)
            kp = r["mesure"]["k_prudent"]
            ok("E3a k des versions = k prudent arrondi vers le HAUT (jamais vers le bas)",
               r["k_des_versions"] == min(math.ceil(kp - 1e-9), 3) and kp != int(kp), (kp, r["k_des_versions"]))
            ok("E3b sans dossier verdicts/ : aucune autre stratégie (« zéro à ce jour », A-1082)",
               r["autres_strategies_jugees"] == 0 and r["k"] == r["k_des_versions"])
            ok("E3c l'empreinte des séries est rendue", r["empreinte_des_series"].startswith("sha256:"))
            indep = g.standard_normal((3, 300))
            r2 = K.compter_les_essais(indep, tmp, "2026-11-27T21:00:00+01:00", table=table)
            ok("E3d k des versions borné à n quand le bruit le pousse au-delà",
               r2["mesure"]["k_prudent"] > 3 and r2["k_des_versions"] == 3, r2["mesure"]["k_prudent"])
            os.makedirs(os.path.join(tmp, "verdicts"))
            for nom, fiche, date, mot in (("a", "F1", "2026-11-20T10:00:00+01:00", "RÉFUTÉE"),
                                          ("b", "F2", "2026-11-21T10:00:00+01:00", "NON JUGEABLE"),
                                          ("c", "F1", "2026-11-22T10:00:00+01:00", "NON TRANCHÉE"),
                                          ("d", "F3", "2026-11-28T10:00:00+01:00", "RÉFUTÉE")):
                with open(os.path.join(tmp, "verdicts", nom + ".json"), "w", encoding="utf-8") as f:
                    json.dump({"fiche_id": fiche, "date_verdict": date, "verdict": mot}, f)
            n, liste = K.strategies_deja_jugees(tmp, "2026-11-27T21:00:00+01:00")
            ok("E3e verdicts comptés : avant l'instant, hors NON JUGEABLE, un rejugement compte (« À PRÉCISER » ⑩)",
               n == 2 and sorted(x[0] for x in liste) == ["F1", "F1"], liste)
            r3 = K.compter_les_essais(s, tmp, "2026-11-27T21:00:00+01:00", table=table)
            ok("E3f k = k des versions + verdicts déjà rendus", r3["k"] == r3["k_des_versions"] + 2, r3["k"])
            with open(os.path.join(tmp, "verdicts", "e.json"), "w", encoding="utf-8") as f:
                json.dump({"fiche_id": "F4", "date_verdict": "2026-11-23T10:00:00+01:00", "verdict": "VALIDÉE"}, f)
            ok("E3g un mot de verdict hors du contrat : refus", leve(K.strategies_deja_jugees, tmp, "2026-11-27T21:00:00+01:00"))
            ok("E3h un instant sans fuseau : refus", leve(K.strategies_deja_jugees, tmp, "2026-11-27T21:00:00"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    essai("E3", e3)

    # E4 — LE RISQUE GLOBAL SE LIT À LA LOI (« 0,05 » de « 0,05 ÷ k »), jamais dans le code
    def e4():
        ok("E4a vraie table : 0,05", K.risque_global(table) == 0.05, K.risque_global(table))
        t = dict(table)
        t["seuil_de_preuve"] = dict(table["seuil_de_preuve"], valeur="0,01 ÷ k")
        ok("E4b une table qui porte 0,01 ÷ k rend 0,01", K.risque_global(t) == 0.01, K.risque_global(t))
        t["seuil_de_preuve"] = dict(table["seuil_de_preuve"], valeur="calculé par programme")
        ok("E4c une case illisible : refus", leve(K.risque_global, t))
    essai("E4", e4)

    # E5 — CALIBRAGE DE LA RESSEMBLANCE SUR DE VRAIES VERSIONS DE C5, un jeton (collège, §3 : « tp 2 % contre tp 3 % […]
    # ρ = 0.67 · chevauchement = 0.85 ; tp 2 % contre tp 8 % : ρ = 0.35 · chevauchement = 0.65 » ; « DG seule contre TTE
    # seule : ρ = -0.08 · chevauchement = 0.00 »)
    def e5():
        for nom, a, b, rho_p, chev_p, semblables in (
                ("tp 2 % / tp 3 %", "C5E10-OBS-V1-E01-0144", "C5E10-OBS-V1-E01-0529", 0.67, 0.85, True),
                ("tp 2 % / tp 8 %", "C5E10-OBS-V1-E01-0144", "C5E10-OBS-V1-E01-2454", 0.35, 0.65, True),
                ("DG / TTE", "C5E10-OBS-V1-E01-0924", "C5E10-OBS-V1-E01-0915", -0.08, 0.00, False)):
            oa, ob = K._un_jeton(mat["ops"][a]), K._un_jeton(mat["ops"][b])
            m = K.se_ressemblent(list(serie(a, True)), list(serie(b, True)), K.jours_en_position(oa, dates_m),
                                 K.jours_en_position(ob, dates_m), table)
            ok("E5 %s : ρ %.2f et chevauchement %.2f (publiés), semblables %s" % (nom, rho_p, chev_p, semblables),
               abs(m["correlation"] - rho_p) <= 0.005 and abs(m["chevauchement"] - chev_p) <= 0.005
               and m["semblables"] is semblables, (round(m["correlation"], 4), round(m["chevauchement"], 4), m["par"]))
    essai("E5", e5)

    # E6 — LE CHEVAUCHEMENT : dénominateur = la plus petite des deux ; « au moins une fois sur deux » (≥)
    def e6():
        a = {("TTE", "2024-01-%02d" % j) for j in (2, 3)}
        b = a | {("TTE", "2024-02-%02d" % j) for j in range(1, 9)}
        ok("E6a une stratégie contenue dans l'autre : chevauchement 1", K.chevauchement(a, b) == 1.0, K.chevauchement(a, b))
        ok("E6b disjointes : 0", K.chevauchement(a, {("DG", "2024-01-02")}) == 0.0)
        ok("E6c vide : refus", leve(K.chevauchement, set(), b))
        g = np.random.default_rng(3)
        x, y = list(g.standard_normal(50)), list(g.standard_normal(50))
        pa = {("TTE", "d%02d" % j) for j in range(4)}
        pb = {("TTE", "d00"), ("TTE", "d01"), ("DG", "d02"), ("DG", "d03")}
        m = K.se_ressemblent(x, y, pa, pb, table)
        ok("E6d chevauchement EXACTEMENT 0,5, corrélation faible : semblables (≥, loi « au moins une fois sur deux »)",
           m["chevauchement"] == 0.5 and m["correlation"] < 0.5 and m["semblables"], m)
    essai("E6", e6)

    # E7 — L'ALIGNEMENT SUR LE CALENDRIER COMMUN
    def e7():
        calendrier = ["2024-01-02", "2024-01-03", "2024-01-04"]
        ok("E7a un jour sans gain vaut 0", K.aligner_sur_le_calendrier({"2024-01-03": 5.0}, calendrier) == [0.0, 5.0, 0.0])
        ok("E7b une date de gain hors du calendrier : refus",
           leve(K.aligner_sur_le_calendrier, {"2024-01-05": 1.0}, calendrier))
        ok("E7c un calendrier non trié : refus", leve(K.aligner_sur_le_calendrier, {}, calendrier[::-1]))
        ok("E7d corrélation de séries de longueurs différentes : refus", leve(K.correlation_des_gains, [1.0, 2.0], [1.0]))
        ok("E7e corrélation d'une série constante : refus", leve(K.correlation_des_gains, [1.0, 1.0, 1.0], [1.0, 2.0, 0.0]))
    essai("E7", e7)

    # E8 — LES JOURS DE POSITION : entrée et sortie COMPRISES
    def e8():
        cot = {"TTE": ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]}
        o = {"valeur": "TTE", "date_entree": "2024-01-02", "date_sortie": "2024-01-04"}
        ok("E8a entrée le 02, sortie le 04 : trois jours", K.jours_en_position([o], cot)
           == {("TTE", "2024-01-02"), ("TTE", "2024-01-03"), ("TTE", "2024-01-04")})
        ok("E8b une valeur sans cotations : refus", leve(K.jours_en_position, [dict(o, valeur="DG")], cot))
    essai("E8", e8)

    # E9 — LA MISE EN SERVICE GLOUTONNE : comparée à TOUTES celles déjà en service, sans enchaînement
    def e9():
        g = np.random.default_rng(8)
        z = g.standard_normal((4, 400))
        A, C = list(z[0]), list(z[1])
        B = list(z[0] + 0.2 * z[2])            # ressemble à A
        D = list(z[0] + 0.3 * z[3])            # ressemble à A, pas à C
        jours = lambda k: {("V%d" % k, "j%d" % j) for j in range(10)}
        cand = [{"id": "A", "gains": A, "jours": jours(0)}, {"id": "C", "gains": C, "jours": jours(1)},
                {"id": "B", "gains": B, "jours": jours(2)}, {"id": "D", "gains": D, "jours": jours(3)}]
        service, ecartes = K.mettre_en_service(cand, table)
        ok("E9a en service A et C ; B et D écartées par A (comparées à TOUTES celles en service)",
           service == ["A", "C"] and ecartes["B"][0] == "A" and ecartes["D"][0] == "A", (service, {k: v[0] for k, v in ecartes.items()}))
        ok("E9b identifiants en double : refus", leve(K.mettre_en_service, cand + cand[:1], table))
    essai("E9", e9)

    # E10 — LES SEUILS DE RESSEMBLANCE SE LISENT AU FICHIER DES SEUILS EN ATTENTE (0,5 et 0,5), jamais dans le code
    def e10():
        ok("E10a vrai fichier : 0,5 et 0,5", K.seuils_de_ressemblance(table) == (0.5, 0.5), K.seuils_de_ressemblance(table))
        t = dict(table)
        t["ressemblance_chevauchement_minimum"] = dict(table["ressemblance_chevauchement_minimum"], valeur="0,9")
        ok("E10b une table à 0,9 rend 0,9", K.seuils_de_ressemblance(t)[1] == 0.9)
        t["ressemblance_chevauchement_minimum"] = dict(table["ressemblance_chevauchement_minimum"], valeur="1,5")
        ok("E10c 1,5 hors du domaine d'une part : refus", leve(K.seuils_de_ressemblance, t))
        del t["ressemblance_chevauchement_minimum"]
        ok("E10d ligne absente : refus", leve(K.seuils_de_ressemblance, t))
    essai("E10", e10)

    # E11 — LA LIGNE DE COMMANDE ROUGIT QUAND LE CALIBRAGE NE PEUT PAS TOURNER (R-734)
    def e11():
        vide = tempfile.mkdtemp(prefix="W2c_vide_")
        try:
            r = subprocess.run([sys.executable, "-B", os.path.join(prog, P), vide, "--calibrer-c5", "--raccourci",
                                "--processus=1"], capture_output=True, text=True, timeout=120)
            ok("E11a racine vide : code 2, jamais 0", r.returncode == 2, r.stdout.strip().splitlines()[-1:])
            r = subprocess.run([sys.executable, "-B", os.path.join(prog, P), vide], capture_output=True, text=True,
                               timeout=60)
            ok("E11b sans « --calibrer-c5 » : code 2", r.returncode == 2)
        finally:
            shutil.rmtree(vide, ignore_errors=True)
    essai("E11", e11)

    print("ROUGES : %d" % len(rouges))
    return len(rouges)


def main(argv):
    """Fabrique le matériau, joue Z0 puis les sabotages demandés, et rend le code de sortie.
    ① RÔLE — Le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — « --cas » : jouer les cas ; sinon le matériau, Z0, puis chaque sabotage demandé.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — — ⑩ EFFET — affiche ; fichiers temporaires.
    ⑪ TERMINAISON — bornée par les relances. [sort: oui — code de sortie]"""
    if len(argv) >= 5 and argv[1] == "--cas":
        try:
            return 1 if cas(argv[2], argv[3], argv[4]) else 0
        except Exception as e:  # noqa: BLE001 — un cas qui n'a pas pu tourner n'est pas vert (R-734)
            print("CAS IMPOSSIBLE : %s: %s" % (type(e).__name__, e))
            return 2
    if len(argv) < 2:
        print(__doc__.split("\n\n")[2])
        return 2
    racine = os.path.abspath(argv[1])
    manque = [p for p in [os.path.join("programmes", n) for n in PROGRAMMES + ("JUGE_DES_STRATEGIES.py", "JOUER_LES_VERSIONS.py")]
              + ["gouvernance/REGISTRE_REGLES.md", "donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv",
                 "donnees/combinatoires/TEMOIN_RESULTATS_C5E10-OBS-V1_E01.csv",
                 "donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv"] if not os.path.isfile(os.path.join(racine, p))]
    if manque:
        print("DONNÉE MANQUANTE : %s" % ", ".join(manque))
        return 2
    demande = argv[2] if len(argv) > 2 else None
    if demande and demande != "--saboter" and demande not in SABOTAGES:
        print("SABOTAGE INCONNU : %s" % demande)
        return 2
    fd, materiau = tempfile.mkstemp(prefix="W2c_materiau_", suffix=".pkl")
    os.close(fd)
    try:
        try:
            ecarts = fabriquer_le_materiau(racine, materiau)
        except Exception as e:  # noqa: BLE001 — R-734
            print("MATÉRIAU IMPOSSIBLE : %s: %s" % (type(e).__name__, e))
            return 2
        print("== matériau : %d versions rejouées par le juge, écarts au témoin : %d" % (245 + len(VERSIONS_NOMMEES), ecarts))
        if ecarts:
            print("VERDICT : NON CONFORME (le juge ne redonne pas le témoin)")
            return 1
        code, sortie = lancer(racine, None, materiau)
        print("== Z0 (code %d)\n%s" % (code, sortie))
        if code != 0:
            print("VERDICT : NON CONFORME (Z0 n'est pas vert)")
            return 2 if code == 2 else 1
        if not demande:
            print("VERDICT : conforme")
            return 0
        noms = list(SABOTAGES) if demande == "--saboter" else [demande]
        muets, introuvables = [], []
        for nom in noms:
            c, s = lancer(racine, nom, materiau)
            rouges = [l.strip() for l in s.splitlines() if l.strip().startswith("ROUGE") or "a levé" in l]
            if c == 2 and "CIBLE INTROUVABLE" in s:
                introuvables.append(nom)
                print("  INTROUVABLE %s : %s" % (nom, s.strip()))
            elif c == 0:
                muets.append(nom)
                print("  MUET   %s : aucun cas ne rougit" % nom)
            else:
                print("  MORD   %s : %s" % (nom, rouges[0] if rouges else s.strip().splitlines()[-1]))
        print("== %d sabotage(s), %d muet(s), %d introuvable(s)" % (len(noms), len(muets), len(introuvables)))
        if introuvables:
            return 2
        if muets:
            print("VERDICT : NON CONFORME (sabotage(s) muet(s) : %s)" % ", ".join(muets))
            return 1
        print("VERDICT : conforme")
        return 0
    finally:
        os.remove(materiau)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
