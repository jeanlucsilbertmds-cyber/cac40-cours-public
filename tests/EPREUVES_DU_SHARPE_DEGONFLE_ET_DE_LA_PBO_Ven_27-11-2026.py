#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU SHARPE DÉGONFLÉ ET DE LA PROBABILITÉ DE SURAPPRENTISSAGE (lot L3 du plan R505) — Ven 27-11-2026.
Simulation uniquement : des séries synthétiques et des cours réels 2024-2026 ; aucune stratégie n'est jouée sur
2000-2023, aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — R-505 version 2, étape 5 : le contrôle 1 du juge se calcule par le Sharpe dégonflé, N = k (décision
de Jean-Luc du 27-11-2026 à 19h00, A-1095), au seuil 0,05 SANS division par k (A-1095, correction du 27-11-2026 à
21h19 : « le Sharpe dégonflé compte déjà les k essais ») ; la PBO est exigée, seuil de départ 0,05 lu à un seul endroit (décision du
27-11-2026 à 18h53, A-1093). Ces épreuves prouvent que les formules sont celles des articles, AU CHIFFRE PRÈS sur les
résultats publiés (E1, E5), que leurs refus ne rendent jamais un chiffre (E2, E7, E8c, E8l, E8m), que la grille du
juge décide le contrôle 1 par le Sharpe dégonflé en cas 2, au seuil 0,05 lu dans le fichier déclaré (E8e, E8j), et la
PBO au seuil lu au même fichier, une PBO égale au seuil passant (E8h, E9) ; E10 recalcule la barre qui en résulte. Une épreuve qui
reste verte quand on retire ce qu'elle teste est une décoration (R-731) : `--saboter` casse le code de chaque façon de
la table SABOTAGES et chacune doit faire rougir au moins un cas.

USAGE : python3 -B tests/EPREUVES_DU_SHARPE_DEGONFLE_ET_DE_LA_PBO_Ven_27-11-2026.py <racine> [--saboter | <sabotage>]
CODE : 0 si Z0 est vert et si chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable (texte absent ou présent plus d'une fois), si le nom est inconnu, ou si une donnée manque
(R-734).

① RÔLE — Prouver que le lot L3 fait ce que dit sa note, et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque
  fichier de tests/ avec la racine, puis avec « --saboter ». Ce programme se relance lui-même en « --cas <copie>
  <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/MODULE_SHARPE_DEGONFLE.py, MODULE_SURAPPRENTISSAGE.py, MODULE_JUGEMENT.py,
  CONTRATS_DES_FICHIERS.py, COMMUN.py, JUGER_UNE_FICHE.py, MODULE_STATISTIQUES_*.py ; gouvernance/REGISTRE_REGLES.md ;
  donnees/cours_maitre.csv ; donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv ; numpy installé.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier les sept programmes dans un dossier temporaire, appliquer le
  sabotage (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie · ③ Z0 doit être vert ;
  un sabotage doit faire rougir au moins un cas.
⑦ UNITÉ — Rendements : fraction par séance ; Sharpe par séance (les chiffres annualisés des articles sont ramenés à la
  séance : Sharpe ÷ √q, variance ÷ q, q séances par an) ; probabilités : fractions.
⑧ POURQUOI — R-731 (épreuves et sabotages), R-732 (un cas tiré d'une vraie ligne : E4 sur les cours réels d'ACCOR,
  E8 et E9 sur la vraie table du REGISTRE et le vrai fichier des seuils), R-734 (un contrôle qui n'a pas pu tourner
  rend un code non nul).
⑨ CE QUI CLOCHE — ① E6 compare aux FOURCHETTES publiées des cas d'essai de l'article de 2017 (tirages au hasard,
  graine fixe). Deux cas ne sont pas exigés dans la fourchette publiée elle-même : E6c (fort surapprentissage,
  T = 2 000 ; sortie du 27-11-2026 : 0,3994 pour « 0,4 à 0,5 », admise par une tolérance de 0,35 à 0,55) et E6e
  (faible surapprentissage, T = 1 000 ; sortie : 0,109 pour « 0,1 à 0,2 », affichée seulement). Chacun imprime
  « ÉCART CONNU » quand sa valeur sort de la fourchette publiée, « dans la fourchette » sinon : l'article ne publie
  pas son code de tirage entier, l'écart n'est pas expliqué. ② Le branchement de la porte du juge sur le
  fichier des seuils est vérifié par la STRUCTURE du code (E8d), pas par un jugement de bout en bout.
⑩ EFFET — Écrit et efface des dossiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 600 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""

import glob
import math
import os
import shutil
import subprocess
import sys
import tempfile

PROGRAMMES = ("MODULE_SHARPE_DEGONFLE.py", "MODULE_SURAPPRENTISSAGE.py", "MODULE_JUGEMENT.py", "CONTRATS_DES_FICHIERS.py", "COMMUN.py",
              "JUGER_UNE_FICHE.py")
MD = "MODULE_SHARPE_DEGONFLE.py"
MS = "MODULE_SURAPPRENTISSAGE.py"
MJ = "MODULE_JUGEMENT.py"
JF = "JUGER_UNE_FICHE.py"
STAT = "MODULE_STATISTIQUES_*"

# LES SABOTAGES : {nom : [(fichier, texte présent une fois, remplaçant)]}. Chacun retire ou fausse UNE propriété.
SABOTAGES = {
    "S01_aplatissement_en_exces": [(MD, "(aplatissement - 1.0) / 4.0", "(aplatissement - 3.0) / 4.0")],
    "S02_racine_de_T": [(MD, "math.sqrt(n_observations - 1)", "math.sqrt(n_observations)")],
    "S03_asymetrie_ignoree": [(MD, "d = 1.0 - asymetrie * sharpe +", "d = 1.0 - 0.0 * sharpe +")],
    "S04_N1_non_traite": [(MD, "    if n_essais == 1:\n        return 0.0\n", "")],
    "S05_variance_nulle_admise": [(MD, "or not v > 0.0:\n        raise", "or v < 0.0:\n        raise")],
    "S06_probabilite_arrondie": [(MD, '{"probabilite": _NORMALE.cdf(z),', '{"probabilite": round(_NORMALE.cdf(z), 3),')],
    "S07_rang_egalites_genereuses": [(MS, "rang = 1 + (r_out < choisi[:, None])", "rang = 1 + (r_out <= choisi[:, None])")],
    "S08_omega_sur_N": [(MS, "w = rang / (n + 1.0)", "w = rang / (n + 0.0)")],
    "S09_logit_strict": [(MS, '"pbo": float((lam <= 0.0).mean())', '"pbo": float((lam < 0.0).mean())')],
    "S10_lignes_recentes_ecartees": [(MS, "    m = m[ecartees:]\n", "    m = m[:m.shape[0] - ecartees]\n")],
    "S11_blocs_impairs_admis": [(MS, "n_blocs < 2 or n_blocs % 2:", "n_blocs < 2:")],
    "S12_gain_reste_condition_en_cas_2": [(MJ, 'if cas == "2" and cle in AFFICHAGE_EN_CAS_2:',
                                           'if False and cle in AFFICHAGE_EN_CAS_2:')],
    "S13_seuils_absents_rendent_vide": [(MJ, 'return illisible("seuils en attente illisibles (%s) : %s" % (type(e).__name__, chemin))',
                                         'return {}')],
    "S14_cle_en_double_admise": [(MJ, '        if cle in table:\n            return illisible("clé %r écrite deux fois" % cle)\n', "")],
    "S15_porte_sans_les_seuils": [(JF, "    table.update(J.table_des_seuils_en_attente(racine))\n", "")],
    "S16_mesure_arrondie": [(MJ, 'm["sharpe_degonfle"] = r["probabilite"]', 'm["sharpe_degonfle"] = round(r["probabilite"], 3)')],
    "S17_pbo_nombre_d_essais_k": [(MS, 'm["nombre_d_essais"] = r["n_versions"]', 'm["nombre_d_essais"] = 1')],
    # Lot L3-FIX (relecture V1 du lot L3 : D1, D2, D4 à D7 ; ses sabotages muets N07, N08, N09, N11)
    "S18_controle_1_remis_a_0_05_sur_k": [(MJ, 's_dsr, r_dsr = seuil_de_la_loi(table, "sharpe_degonfle_risque_maximum")',
                                           's_dsr, r_dsr = seuil_de_la_loi(table, "seuil_de_preuve", kk)')],
    "S19_pbo_echec_rend_zero": [(MS, '        return None, "probabilité de surapprentissage non calculable : %s: %s" % (type(e).__name__, e)',
                                 '        return {"pbo": 0.0, "nombre_d_essais": 10 ** 6, "n_versions": 10 ** 6}, ""')],
    "S20_pbo_egale_au_seuil_bloque": [(MJ, '"PASSE" if m["pbo"] <= s_pbo else "BLOQUE"', '"PASSE" if m["pbo"] < s_pbo else "BLOQUE"')],
    "S21_N1_deux_sharpe_exiges": [(MD, "if not (isinstance(n_essais, int) and not isinstance(n_essais, bool) and n_essais == 1):",
                                   "if True:")],
    "S22_debordement_non_attrape": [(MJ, "    except (ValueError, ArithmeticError) as e:\n        return None, \"Sharpe dégonflé",
                                     "    except ValueError as e:\n        return None, \"Sharpe dégonflé")],
    "S23_dsr_non_fini_admis": [(MJ, "or not math.isfinite(p) or not 0.0 <= p <= 1.0:\n        return None, \"Sharpe dégonflé",
                                ":\n        return None, \"Sharpe dégonflé")],
}


def lancer(racine, sabotage):
    """Copie les programmes, applique un sabotage, relance ce fichier en « --cas » et rend (code, sortie).

    ① RÔLE — Un passage d'épreuves sur une copie, intacte (Z0) ou sabotée. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` ; `sabotage` : un nom de SABOTAGES ou None. ④ CONDITIONS D'ENTRÉE — les programmes existent.
    ⑤ SORTIE — DEUX valeurs : le code de la relance (2 si une cible est introuvable) et sa sortie. [rend: 2]
    ⑥ TRAITEMENT — copier, remplacer (texte présent une fois exactement), relancer avec un délai de 600 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731 : le sabotage porte sur une COPIE, jamais sur le dépôt.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — un dossier temporaire, effacé. ⑪ TERMINAISON — bornée à 600 s. [sort: non]"""
    tmp = tempfile.mkdtemp(prefix="L3_epreuve_")
    try:
        prog = os.path.join(tmp, "programmes")
        os.makedirs(prog)
        for n in PROGRAMMES:
            shutil.copy(os.path.join(racine, "programmes", n), prog)
        for f in glob.glob(os.path.join(racine, "programmes", STAT + ".py")):
            shutil.copy(f, prog)
        for fichier, avant, apres in (SABOTAGES[sabotage] if sabotage else []):
            p = os.path.join(prog, fichier)
            s = open(p, encoding="utf-8").read()
            if s.count(avant) != 1:
                return 2, "CIBLE INTROUVABLE (%d fois) dans %s : %r" % (s.count(avant), fichier, avant[:70])
            open(p, "w", encoding="utf-8").write(s.replace(avant, apres))
        try:
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--cas", prog, racine],
                               capture_output=True, text=True, timeout=600)
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return 1, "DÉLAI DÉPASSÉ"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cas(prog, racine):
    """Joue les cas E1 à E10 sur les programmes du dossier `prog` et rend le nombre de rouges.

    ① RÔLE — Les épreuves elles-mêmes. ② CONTEXTE D'APPEL — `main`, en « --cas ». ③ ENTRÉE — `prog` : le dossier
    des programmes (copie) ; `racine` : les données. ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur :
    le nombre de cas rouges (une exception compte comme un rouge). [rend: 1] ⑥ TRAITEMENT — voir chaque cas.
    ⑦ UNITÉ — voir l'en-tête. ⑧ POURQUOI — une épreuve par propriété. ⑨ CE QUI CLOCHE — voir l'en-tête.
    ⑩ EFFET — écrit des fichiers temporaires (E9). ⑪ TERMINAISON — rend la main. [sort: non]"""
    sys.path.insert(0, prog)
    import importlib.util
    import numpy as np
    import MODULE_SHARPE_DEGONFLE as M
    import MODULE_SURAPPRENTISSAGE as P
    import MODULE_JUGEMENT as J
    f_stat = glob.glob(os.path.join(prog, STAT + ".py"))[0]
    spec = importlib.util.spec_from_file_location("stat_l3", f_stat)
    S = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S)
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

    # E1 — CALIBRAGE DU SHARPE DÉGONFLÉ SUR LES CHIFFRES PUBLIÉS (Bailey et López de Prado 2014, exemple de l'article :
    # SR annualisé 2,5, N = 100, V annualisée 0,5, T = 1 250, γ3 = −3, γ4 = 10 ; 250 séances par an)
    def e1():
        q = 250.0
        dsr = lambda n, s3, s4: M.sharpe_degonfle(2.5 / math.sqrt(q), n, 0.5 / q, 1250, s3, s4)["probabilite"]
        p100 = dsr(100, -3, 10)
        ok("E1a exemple de l'article, N = 100 : « 90 % »", round(p100, 2) == 0.90, p100)
        p46 = dsr(46, -3, 10)
        ok("E1b N = 46 : « 0.9505 » (article)", round(p46, 4) == 0.9505, p46)
        ok("E1c loi normale : passe 0,95 à N = 88, pas à N = 89 (article : « N = 88 »)",
           dsr(88, 0, 3) > 0.95 and dsr(89, 0, 3) < 0.95, (dsr(88, 0, 3), dsr(89, 0, 3)))
        q = 252.0
        p = M.sharpe_degonfle(2.5 / math.sqrt(q), 100, 0.5 / q, 1250, -3, 10)["probabilite"]
        ok("E1d 252 séances par an : 0.89967234849777633 (reproduction publiée de G. Marti, 2018)",
           abs(p - 0.89967234849777633) < 1e-12, repr(p))
    essai("E1", e1)

    # E2 — PROPRIÉTÉS ET REFUS DU SHARPE DÉGONFLÉ
    def e2():
        r1 = M.sharpe_degonfle(0.05, 1, None, 500, 0.0, 3.0)
        psr = 0.5 * (1 + math.erf(0.05 * math.sqrt(499) / math.sqrt(1 + 0.05 ** 2 / 2) / math.sqrt(2)))
        ok("E2a N = 1 : seuil nul, la probabilité est le Sharpe probabiliste de seuil 0",
           r1["sharpe_du_meilleur_hasard"] == 0.0 and abs(r1["probabilite"] - psr) < 1e-12, r1)
        ps = [M.sharpe_degonfle(0.08, n, 0.001, 800, -0.5, 6.0)["probabilite"] for n in (2, 10, 100, 1000)]
        ok("E2b plus d'essais, probabilité plus basse", all(a > b for a, b in zip(ps, ps[1:])), ps)
        a = M.sharpe_degonfle(0.08, 10, 0.001, 800, 0.0, 3.0)["probabilite"]
        b = M.sharpe_degonfle(0.08, 10, 0.001, 800, -2.0, 3.0)["probabilite"]
        ok("E2c une asymétrie négative abaisse la probabilité (gain positif)", b < a, (a, b))
        ok("E2d variance nulle avec N ≥ 2 : refus, jamais un chiffre", leve(M.sharpe_degonfle, 0.08, 10, 0.0, 800, 0, 3))
        ok("E2e N = 0, N booléen, T = 1 : refus", leve(M.sharpe_degonfle, 0.08, 0, 0.001, 800, 0, 3)
           and leve(M.sharpe_degonfle, 0.08, True, 0.001, 800, 0, 3) and leve(M.sharpe_degonfle, 0.08, 5, 0.001, 1, 0, 3))
        ok("E2f dénominateur négatif : refus", leve(M.sharpe_degonfle, 1.0, 5, 0.001, 800, 5.0, 3.0))
        p = M.sharpe_degonfle(0.12, 3, 0.0004, 1500, -0.3, 5.0)["probabilite"]
        ok("E2g probabilité NON arrondie (un arrondi au millième déplacerait la frontière du seuil 0,05)", round(p, 3) != p, repr(p))
        # D4 (relecture V1) : k = 1 PAR LA SÉRIE, sans Sharpe d'essais — le premier vrai passage (A-1082)
        serie = (np.random.default_rng(11).normal(0.0008, 0.01, 600)).tolist()
        mo = M.moments_des_rendements(serie)
        attendu = M.sharpe_degonfle(mo["sharpe"], 1, None, mo["n_observations"], mo["asymetrie"], mo["aplatissement"])
        r_s = M.sharpe_degonfle_d_une_serie(serie, 1, [])
        m_j, r_j = J.mesurer_le_sharpe_degonfle(serie, 1, None)
        ok("E2h k = 1 par la série, AUCUN Sharpe d'essai : mesuré (seuil nul), par le module et par le mesureur du juge",
           r_s["probabilite"] == attendu["probabilite"] and r_s["variance_des_sharpe"] is None and m_j is not None
           and m_j["sharpe_degonfle"] == attendu["probabilite"] and m_j["nombre_d_essais"] == 1, (r_s["probabilite"], r_j))
    essai("E2", e2)

    # E3 — CONFRONTATION À L'ANCIENNE FONCTION (MODULE_STATISTIQUES.calculer_deflated_sharpe, arrondie au millième)
    def e3():
        ecarts = []
        for sr, n, v, t, s3, s4 in ((0.1, 10, 0.002, 600, -1.0, 6.0), (0.05, 100, 0.001, 2000, 0.5, 4.0),
                                    (0.2, 3888, 0.003, 300, -0.2, 3.5), (2.5 / math.sqrt(250), 100, 0.5 / 250, 1250, -3, 10)):
            vieux = S.calculer_deflated_sharpe(sr, n, v, t, s3, s4)["dsr"]
            neuf = M.sharpe_degonfle(sr, n, v, t, s3, s4)["probabilite"]
            ecarts.append(abs(vieux - neuf))
        ok("E3 ancienne et nouvelle fonction d'accord au millième (arrondi de l'ancienne)", max(ecarts) <= 5e-4 + 1e-9, ecarts)
    essai("E3", e3)

    # E4 — UNE VRAIE SÉRIE (R-732) : les rendements de clôture à clôture d'ACCOR, donnees/cours_maitre.csv, 2024-2026
    def e4():
        import csv
        closes = [float(r["close"]) for r in csv.DictReader(open(os.path.join(racine, "donnees", "cours_maitre.csv"),
                                                                  encoding="utf-8")) if r["valeur"] == "ACCOR"]
        x = np.array([b / a - 1.0 for a, b in zip(closes, closes[1:])])
        m = M.moments_des_rendements(x.tolist())
        c = x - x.mean()
        m2 = (c ** 2).mean()
        attendu = (x.mean() / math.sqrt(m2), (c ** 3).mean() / m2 ** 1.5, (c ** 4).mean() / m2 ** 2)
        obtenu = (m["sharpe"], m["asymetrie"], m["aplatissement"])
        ok("E4a ACCOR (%d rendements) : Sharpe, asymétrie, aplatissement BRUT = calcul indépendant numpy" % len(x),
           len(x) > 500 and all(abs(a - b) < 1e-9 * max(1, abs(a)) for a, b in zip(attendu, obtenu)), obtenu)
        r = M.sharpe_degonfle_d_une_serie(x.tolist(), 5, [0.01, 0.02, -0.01, 0.03, 0.0])
        v = float(np.var([0.01, 0.02, -0.01, 0.03, 0.0], ddof=1))
        direct = M.sharpe_degonfle(m["sharpe"], 5, v, m["n_observations"], m["asymetrie"], m["aplatissement"])
        ok("E4b la série passe par la même formule, variance des essais en n − 1",
           abs(r["probabilite"] - direct["probabilite"]) < 1e-12 and abs(r["variance_des_sharpe"] - v) < 1e-15, r["probabilite"])
        ok("E4c moins de deux Sharpe d'essais pour k ≥ 2 : refus", leve(M.sharpe_degonfle_d_une_serie, x.tolist(), 5, [0.1]))
        ok("E4d série constante : refus", leve(M.moments_des_rendements, [0.0] * 50))
    essai("E4", e4)

    # E5 — LA PBO = LA TRANSCRIPTION PAS À PAS DE L'ALGORITHME 2.3 DE L'ARTICLE (lignes réelles, Sharpe recalculé sur
    # les lignes de chaque moitié, sans sommes par bloc), égalités comprises
    def e5():
        from itertools import combinations

        def reference(mat, s):
            t, n = len(mat), len(mat[0])
            mat = mat[t % s:]
            h = len(mat) // s
            blocs = [mat[i * h:(i + 1) * h] for i in range(s)]

            def sr(lignes, j):
                x = [l[j] for l in lignes]
                mu = sum(x) / len(x)
                var = sum((v - mu) ** 2 for v in x) / len(x)
                return mu / math.sqrt(var) if var > 1e-300 else 0.0
            lams = []
            for c in combinations(range(s), s // 2):
                jin = [l for i in c for l in blocs[i]]
                jout = [l for i in range(s) if i not in c for l in blocs[i]]
                rin = [sr(jin, j) for j in range(n)]
                rout = [sr(jout, j) for j in range(n)]
                best = max(range(n), key=lambda j: (rin[j], -j))
                rang = 1 + sum(1 for v in rout if v < rout[best])
                w = rang / (n + 1)
                lams.append(math.log(w / (1 - w)))
            return sum(1 for v in lams if v <= 0) / len(lams), sorted(lams)
        rng = np.random.default_rng(271120)
        ecarts = []
        for t, n, s, entier in ((50, 7, 4, False), (61, 9, 6, False), (48, 7, 8, True), (40, 5, 4, True)):
            mat = rng.normal(0, 1, (t, n))
            if entier:
                mat = np.round(mat)          # des égalités, sur J comme sur J̄
                mat[:, 2] = 0.0               # une version qui ne joue jamais : Sharpe nul partout
            pbo_ref, _l = reference(mat.tolist(), s)
            r = P.probabilite_de_surapprentissage(mat, n_blocs=s)
            ecarts.append((pbo_ref, r["pbo"]))
        ok("E5a PBO identique à la transcription pas à pas (4 matrices, dont 2 à égalités)",
           all(abs(a - b) < 1e-12 for a, b in ecarts), ecarts)
        ok("E5b S = 4 : 6 coupures ; S = 16 : 12 870 (article : C(S, S/2))",
           P.probabilite_de_surapprentissage(rng.normal(0, 1, (40, 3)), n_blocs=4)["n_combinaisons"] == 6
           and P.probabilite_de_surapprentissage(rng.normal(0, 1, (64, 3)))["n_combinaisons"] == 12870)
    essai("E5", e5)

    # E6 — LES CAS D'ESSAI DE L'ARTICLE (section 6) : T × N tirages normaux recentrés à un Sharpe exact de 0 ; la dernière
    # version recentrée à un Sharpe annualisé de 1 (fort surapprentissage) ou 2 (faible) ; q = 365,25 × 5 ÷ 7 (code de
    # l'article, section 7.1)
    def e6():
        q = 365.25 * 5 / 7.0
        rng = np.random.default_rng(20261127)

        def mat(t, n, sr):
            x = rng.standard_normal((t, n))
            x = (x - x.mean(0)) / x.std(0)
            if sr:
                x[:, -1] += sr / math.sqrt(q)
            return x

        def moyenne(t, n, sr, k=10):
            return float(np.mean([P.probabilite_de_surapprentissage(mat(t, n, sr))["pbo"] for _ in range(k)]))
        full = [P.probabilite_de_surapprentissage(mat(1000, 100, 0))["pbo"] for _ in range(3)]
        ok("E6a surapprentissage total (tous à Sharpe 0) : « φ → 1 »", min(full) >= 0.99, full)
        h = moyenne(1000, 100, 1)
        ok("E6b fort surapprentissage T = 1 000, N = 100 : « entre 0.7 et 0.8 »", 0.65 <= h <= 0.85, h)
        h2 = moyenne(2000, 100, 1)
        ok("E6c fort surapprentissage T = 2 000 : « entre 0.4 et 0.5 » (tolérance 0,35 à 0,55) — %s"
           % ("dans la fourchette" if 0.4 <= h2 <= 0.5 else "ÉCART CONNU, hors de la fourchette publiée"),
           0.35 <= h2 <= 0.55, h2)
        b2 = moyenne(2000, 100, 2)
        ok("E6d faible surapprentissage T = 2 000 : « entre 0 et 0.04 »", b2 <= 0.04, b2)
        b = moyenne(1000, 100, 2)
        print("  INFO  E6e non exigé, %s : faible surapprentissage T = 1 000, N = 100 : %.3f (article : « 0.1 à 0.2 »)"
              % ("dans la fourchette" if 0.1 <= b <= 0.2 else "ÉCART CONNU, hors de la fourchette publiée", b))
    essai("E6", e6)

    # E7 — REFUS ET DÉCOUPAGE DE LA PBO
    def e7():
        rng = np.random.default_rng(5)
        x = rng.normal(0, 1, (37, 4))
        ok("E7a S impair, une version, T < S, nombre non fini : refus",
           leve(P.probabilite_de_surapprentissage, x, 5) and leve(P.probabilite_de_surapprentissage, x[:, :1])
           and leve(P.probabilite_de_surapprentissage, x[:10], 16)
           and leve(P.probabilite_de_surapprentissage, np.where(x > 2, np.nan, x)))
        r = P.probabilite_de_surapprentissage(x, n_blocs=4)
        y = x.copy()
        y[0] = 99.0                                   # la PLUS ANCIENNE ligne, écartée (37 mod 4 = 1)
        z = x.copy()
        z[-1] = 99.0                                  # la plus récente, gardée
        ok("E7b les T mod S lignes écartées sont les PLUS ANCIENNES",
           r["lignes_ecartees"] == 1 and r["lignes_utilisees"] == 36
           and P.probabilite_de_surapprentissage(y, n_blocs=4)["pbo"] == r["pbo"]
           and P.probabilite_de_surapprentissage(z, n_blocs=4)["logit_median"] != r["logit_median"], r)
    essai("E7", e7)

    # E8 — LA GRILLE DU JUGE, SUR LA VRAIE TABLE DU REGISTRE RECOUVERTE PAR LE VRAI FICHIER DES SEUILS (R-732)
    def e8():
        table = J.table_de_la_loi(open(os.path.join(racine, "gouvernance", "REGISTRE_REGLES.md"), encoding="utf-8").read())
        avant = table.get("surapprentissage_maximum", {}).get("valeur")
        table.update(J.table_des_seuils_en_attente(racine))
        s, r = J.seuil_de_la_loi(table, "surapprentissage_maximum")
        ok("E8a le seuil de PBO lu est 0,05 (fichier), la table du REGISTRE disait %r" % avant, s == 0.05, (s, r))
        s1, r1 = J.seuil_de_la_loi(table, "sharpe_degonfle_risque_maximum")
        ok("E8a2 le seuil du contrôle 1 lu est 0,05, SANS ÷ k (fichier ; A-1095 corrigée le 27-11 à 21h19)",
           s1 == 0.05 and J.seuil_de_la_loi(table, "sharpe_degonfle_risque_maximum", 20)[0] == 0.05, (s1, r1))
        k = 4
        serie = (np.random.default_rng(9).normal(0.0012, 0.01, 700)).tolist()
        m, r = J.mesurer_le_sharpe_degonfle(serie, k, [0.01, 0.05, -0.02, 0.03])
        direct = M.sharpe_degonfle_d_une_serie(serie, k, [0.01, 0.05, -0.02, 0.03])["probabilite"]
        ok("E8b la mesure porte la probabilité NON arrondie et nombre_d_essais = k",
           m is not None and m["sharpe_degonfle"] == direct and m["nombre_d_essais"] == k, (m and m["sharpe_degonfle"], r))
        mauvais, r_m = J.mesurer_le_sharpe_degonfle([0.0] * 30, k, [0.1, 0.2])
        ok("E8c une série impossible rend (None, raison), jamais un chiffre", mauvais is None and r_m, r_m)
        # D7 (relecture V1) : un débordement numérique (rendements de 1e200) rend (None, raison), jamais une exception
        try:
            deb = J.mesurer_le_sharpe_degonfle([1e200, -1e200, 2e200, 0.5e200] * 5, k, [0.1, 0.2])
        except Exception as e:  # noqa: BLE001 — l'exception EST le défaut que ce cas guette
            deb = ("EXCEPTION", "%s: %s" % (type(e).__name__, e))
        ok("E8m un débordement (rendements 1e200) rend (None, raison), ni plantage ni chiffre",
           deb[0] is None and "Overflow" in deb[1], deb)
        # une probabilité non finie rendue par le module (module remplacé le temps du cas) : (None, raison)
        vrai_module = J._module_du_sharpe_degonfle

        class _Nan:
            """Faux module qui rend une probabilité NaN. ① RÔLE — éprouver la garde de finitude. ② `cas`. ③ — ④ —
            ⑤ — ⑥ — ⑦ — ⑧ un NaN comparé à 0,05 passerait en silence (1 − NaN < 0,05 est faux : BLOQUE, mais la
            raison serait perdue). ⑨ — ⑩ — ⑪ —"""
            @staticmethod
            def sharpe_degonfle_d_une_serie(*_a):
                """Rend une probabilité NaN. ①-⑪ : voir la classe. [rend: 1] [sort: non]"""
                return {"probabilite": float("nan")}
        J._module_du_sharpe_degonfle = lambda: _Nan
        try:
            nan_m, nan_r = J.mesurer_le_sharpe_degonfle(serie, k, [0.1, 0.2])
        finally:
            J._module_du_sharpe_degonfle = vrai_module
        ok("E8n une probabilité non finie rend (None, raison)", nan_m is None and "non finie" in nan_r, (nan_m, nan_r))

        def grille(cas, externes):
            return J.grille_de_validation(table, cas, k, mesures_externes=externes)
        g2, g1 = grille("2", {"sharpe_degonfle": m}), grille("1", {})
        ok("E8d cas 2 : le gain > 0 (calcul A) est un AFFICHAGE ; cas 1 : une CONDITION (inchangé)",
           g2["controles"]["gain_bat_zero"]["role"] == "AFFICHAGE" and g1["controles"]["gain_bat_zero"]["role"] == "CONDITION",
           (g2["controles"]["gain_bat_zero"]["role"], g1["controles"]["gain_bat_zero"]["role"]))
        c1 = g2["controles"]["sharpe_degonfle"]
        ok("E8e cas 2 : le contrôle 1 est le Sharpe dégonflé, 1 − p < 0,05 SANS ÷ k (k = %d, seuil rendu %r)" % (k, c1["seuil"]),
           c1["etat"] == "PASSE" and c1["seuil"] == 0.05 and 1.0 - m["sharpe_degonfle"] < 0.05, c1)
        # D2 (relecture V1) : 0,05 ÷ k ≤ 1 − p < 0,05 — la frontière qui sépare la loi corrigée de l'erreur
        g20 = J.grille_de_validation(table, "2", 20, mesures_externes={"sharpe_degonfle": {"sharpe_degonfle": 0.97,
                                                                                            "nombre_d_essais": 20}})
        c20 = g20["controles"]["sharpe_degonfle"]
        ok("E8j k = 20, 1 − p = 0,03 : entre 0,05 ÷ 20 = 0,0025 et 0,05 → PASSE (A-1095 corrigée)",
           0.05 / 20 <= 1.0 - 0.97 < 0.05 and c20["etat"] == "PASSE" and c20["seuil"] == 0.05, c20)
        faible = J.mesurer_le_sharpe_degonfle((np.random.default_rng(9).normal(0.0003, 0.01, 700)).tolist(), k,
                                              [0.01, 0.05, -0.02, 0.03])[0]
        ok("E8f un Sharpe faible BLOQUE le contrôle 1", grille("2", {"sharpe_degonfle": faible})["controles"]
           ["sharpe_degonfle"]["etat"] == "BLOQUE", faible["sharpe_degonfle"])
        x = np.random.default_rng(3).normal(0, 0.01, (320, 8))
        mp, _r = P.mesurer_le_surapprentissage(x)
        etat = grille("2", {"surapprentissage": mp})["controles"]["surapprentissage"]
        attendu = "PASSE" if mp["pbo"] < 0.05 else "BLOQUE"
        ok("E8g la PBO est comparée à 0,05, nombre_d_essais = nombre de versions (8)",
           etat["etat"] == attendu and etat["seuil"] == 0.05 and mp["nombre_d_essais"] == 8, (mp["pbo"], etat["etat"]))
        bonne = dict(mp, pbo=0.04)
        moyenne = dict(mp, pbo=0.06)
        ok("E8h PBO 0,04 PASSE, 0,06 BLOQUE (l'ancien 0,30 l'aurait laissé passer)",
           grille("2", {"surapprentissage": bonne})["controles"]["surapprentissage"]["etat"] == "PASSE"
           and grille("2", {"surapprentissage": moyenne})["controles"]["surapprentissage"]["etat"] == "BLOQUE")
        # D6 (relecture V1) : « au-dessus du seuil, la stratégie n'est pas validée » (loi) ; « greater than 0.05 »
        # (article) — une PBO ÉGALE au seuil passe ; atteignable avec S = 6 blocs (20 coupures, 1 sur 20 = 0,05)
        pile = grille("2", {"surapprentissage": dict(mp, pbo=0.05)})["controles"]["surapprentissage"]
        ok("E8h2 PBO = 0,05 pile (le seuil) : PASSE", pile["etat"] == "PASSE", pile["etat"])
        # D5 (relecture V1) : un calcul de PBO en échec rend (None, raison), jamais 0,0, la meilleure valeur
        rate, r_rate = P.mesurer_le_surapprentissage([[0.01, 0.02], [0.01]] * 40)
        ok("E8l une matrice irrégulière rend (None, raison), jamais une PBO", rate is None and r_rate, (rate, r_rate))
        import ast
        src = open(os.path.join(prog, JF), encoding="utf-8").read()
        f = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "juger_une_fiche"][0]
        appels = [n.func.attr for n in sorted((n for n in ast.walk(f) if isinstance(n, ast.Call)
                                               and isinstance(n.func, ast.Attribute)), key=lambda n: (n.lineno, n.col_offset))]
        ok("E8i la porte du juge pose les seuils en attente APRÈS la table du REGISTRE (structure du code)",
           "table_de_la_loi" in appels and "table_des_seuils_en_attente" in appels
           and appels.index("table_des_seuils_en_attente") > appels.index("table_de_la_loi"))
    essai("E8", e8)

    # E9 — LE LECTEUR DU FICHIER DES SEUILS : tout défaut rend ILLISIBLE (donc INCONNU), jamais l'ancien 0,30
    def e9():
        import CONTRATS_DES_FICHIERS as CT
        vrai = open(os.path.join(racine, CT.SEUILS_EN_ATTENTE_DU_REGISTRE), encoding="utf-8").read()
        ok("E9a le vrai fichier rend « 0,05 »",
           J.table_des_seuils_en_attente(racine)["surapprentissage_maximum"]["valeur"] == "0,05")
        ligne = [l for l in vrai.splitlines() if l.startswith("surapprentissage_maximum")][0]
        variantes = {"absent": None, "en-tête faux": vrai.replace("cle,valeur,sens,source", "cle,valeur,sens"),
                     "clé en double": vrai + "\n" + ligne + "\n", "clé inconnue": vrai + '\nautre_seuil,"1",x,y\n',
                     "clé absente": vrai.replace(ligne, "")}
        for nom, texte in variantes.items():
            tmp = tempfile.mkdtemp(prefix="L3_seuils_")
            try:
                os.makedirs(os.path.join(tmp, "donnees"))
                if texte is not None:
                    open(os.path.join(tmp, CT.SEUILS_EN_ATTENTE_DU_REGISTRE), "w", encoding="utf-8").write(texte)
                t = {"surapprentissage_maximum": {"valeur": "0,30", "sens": "", "source": ""}}
                t.update(J.table_des_seuils_en_attente(tmp))
                s, r = J.seuil_de_la_loi(t, "surapprentissage_maximum")
                ok("E9 %s : seuil INCONNU, jamais 0,30" % nom, s is None and t["surapprentissage_maximum"]["valeur"]
                   == "ILLISIBLE", (s, r))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    essai("E9", e9)

    # E10 — LA BARRE QUI RÉSULTE DU CONTRÔLE 1 CORRIGÉ (A-1095, 27-11-2026 à 21h19), RECALCULÉE, jamais écrite à la main.
    # Cadre de la note du lot L3 (séries normales γ3 = 0, γ4 = 3 ; T = 1 500 séances ; variance des Sharpe des essais
    # 0,0004 par séance ; 250 séances par an) : le Sharpe annualisé minimal pour que la GRILLE rende PASSE doit être
    # celui de l'article (probabilité > 0,95) et rester sous celui de l'ancienne barre 0,05 ÷ k (essais comptés deux fois).
    def e10():
        q, t, v = 250.0, 1500, 0.0004

        def minimum(passe):
            """Plus petit Sharpe annualisé qui passe, par dichotomie. ① RÔLE — mesurer une barre. ② `e10`.
            ③ `passe` : Sharpe par séance → booléen. ④ croissante. ⑤ UNE valeur, Sharpe annualisé. [rend: 1]
            ⑥ 60 coupes de [0, 10] (précision 10 ÷ 2⁶⁰). ⑦ Sharpe annualisé. ⑧ — ⑨ — ⑩ — ⑪ 60 tours. [sort: non]"""
            bas, haut = 0.0, 10.0
            for _ in range(60):
                mil = (bas + haut) / 2
                bas, haut = (bas, mil) if passe(mil / math.sqrt(q)) else (mil, haut)
            return haut

        lignes = []
        for kk in (1, 5, 20, 100):
            dsr = lambda sr, kk=kk: M.sharpe_degonfle(sr, kk, v if kk > 1 else None, t, 0.0, 3.0)["probabilite"]
            par_la_grille = minimum(lambda sr, kk=kk: J.grille_de_validation(table, "2", kk, mesures_externes={
                "sharpe_degonfle": {"sharpe_degonfle": dsr(sr), "nombre_d_essais": kk}})["controles"]["sharpe_degonfle"]["etat"] == "PASSE")
            article = minimum(lambda sr: dsr(sr) > 0.95)
            ancienne = minimum(lambda sr, kk=kk: 1.0 - dsr(sr) < 0.05 / kk)
            lignes.append((kk, par_la_grille, article, ancienne))
            print("  INFO  E10 k = %d : Sharpe annualisé minimal %.2f (grille) · %.2f (article, p > 0,95) · %.2f (ancienne"
                  " barre 0,05 ÷ k)" % (kk, par_la_grille, article, ancienne))
        ok("E10 la grille exige le Sharpe de l'article (à 1e-9 près) et, dès k ≥ 2, MOINS que l'ancienne barre 0,05 ÷ k",
           all(abs(g - a) < 1e-9 for _k, g, a, _o in lignes) and all(g < o for kk, g, _a, o in lignes if kk >= 2),
           [(kk, round(g, 4), round(o, 4)) for kk, g, _a, o in lignes])
    table = J.table_de_la_loi(open(os.path.join(racine, "gouvernance", "REGISTRE_REGLES.md"), encoding="utf-8").read())
    table.update(J.table_des_seuils_en_attente(racine))
    essai("E10", e10)

    print("== %d rouge(s)%s" % (len(rouges), (" : " + ", ".join(rouges)) if rouges else ""))
    return len(rouges)


def main(argv):
    """Joue Z0 puis les sabotages demandés et rend le code de sortie.
    ① RÔLE — Le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — « --cas » : jouer les cas ; sinon Z0, puis chaque sabotage demandé.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — — ⑩ EFFET — affiche ; dossiers temporaires.
    ⑪ TERMINAISON — bornée par les relances. [sort: oui — code de sortie]"""
    if len(argv) >= 4 and argv[1] == "--cas":
        try:
            return 1 if cas(argv[2], argv[3]) else 0
        except Exception as e:  # noqa: BLE001 — un cas qui n'a pas pu tourner n'est pas vert (R-734)
            print("CAS IMPOSSIBLE : %s: %s" % (type(e).__name__, e))
            return 2
    if len(argv) < 2:
        print(__doc__.split("\n\n")[2])
        return 2
    racine = os.path.abspath(argv[1])
    manque = [p for p in [os.path.join("programmes", n) for n in PROGRAMMES]
              + ["gouvernance/REGISTRE_REGLES.md", "donnees/cours_maitre.csv",
                 "donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv"] if not os.path.isfile(os.path.join(racine, p))]
    if manque or not glob.glob(os.path.join(racine, "programmes", STAT + ".py")):
        print("DONNÉE MANQUANTE : %s" % (", ".join(manque) or STAT))
        return 2
    demande = argv[2] if len(argv) > 2 else None
    if demande and demande != "--saboter" and demande not in SABOTAGES:
        print("SABOTAGE INCONNU : %s" % demande)
        return 2
    code, sortie = lancer(racine, None)
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
        c, s = lancer(racine, nom)
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
