#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DE LA COURBE DU COMPTE ET DE L'ANALYSE DE PUISSANCE (lot W2b du plan R505) — Ven 27-11-2026.
Simulation uniquement : des opérations fictives et les 100 opérations simulées de C5-ETENDU-10 sur 2024-2026 (ses
années de réglage, déjà vues) ; aucune stratégie n'est jouée sur 2000-2023, aucun ordre réel n'est jamais passé.

LE SENS EN TÊTE — R-505 version 2, étape 5, contrôle 4 (décision de Jean-Luc du 27-11-2026 à 13h46, A-1071) : la
stratégie est jugée sur la COURBE DU COMPTE AU JOUR LE JOUR (Fama 1998), et le minimum de données est CALCULÉ pour
chaque stratégie par une ANALYSE DE PUISSANCE (80 %, seuil 0,05 ÷ k) ; le plancher fixe de 30 ne décide plus. Ces
épreuves prouvent : la formule au chiffre près sur les exemples publiés (E1) ; la puissance réelle par simulation (E2) ;
« vingt achats nés de la même chute ne comptent qu'une fois », montré sur la courbe (E3) ; aucun euro créé ni perdu,
sur une vraie ligne de nos fichiers (E4) ; les séances sans position comptent (E5) ; tout refus rend INCONNU ou lève,
jamais un faux vert (E6) ; le 30 ne décide nulle part (E7) ; la courbe est branchée sur le Sharpe dégonflé du lot L3
sans recopie (E8) ; la puissance est lue au fichier déclaré (E9) ; le minimum bouge dans le bon sens (E10).
`--saboter` casse le code de chaque façon de la table SABOTAGES ; chacune doit faire rougir au moins un cas (R-731).

USAGE : python3 -B tests/EPREUVES_DE_LA_COURBE_DU_COMPTE_Ven_27-11-2026.py <racine> [--saboter | <sabotage>]
CODE : 0 si Z0 est vert et si chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de sabotage
est introuvable, si le nom est inconnu, ou si une donnée manque (R-734).

① RÔLE — Prouver que le lot W2b fait ce que dit sa note, et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis avec
  « --saboter ». Ce programme se relance lui-même en « --cas <copie> <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/ (MODULE_COURBE_DU_COMPTE, MODULE_SHARPE_DEGONFLE, MODULE_JUGEMENT,
  MODULE_POSITIONS, CALENDRIER_DE_LA_BOURSE, JUGE_DES_STRATEGIES et leurs voisins) ; donnees/cours_maitre.csv ;
  donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv ; donnees/sources_indice/INDICE_CAC40.csv ;
  donnees/CALENDRIER_EURONEXT.csv ; donnees/SEUILS_DE_R505_V2_EN_ATTENTE_DU_REGISTRE.csv.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier programmes/ dans un dossier temporaire, appliquer le sabotage
  (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie · ③ Z0 doit être vert ; un sabotage
  doit faire rougir au moins un cas.
⑦ UNITÉ — Rendements : fraction par séance ; Sharpe par séance ; gains en euros ; durées en séances.
⑧ POURQUOI — R-731 (épreuves et sabotages), R-732 (un cas tiré d'une vraie ligne : E4, les 100 opérations de C5 et les
  cours réels lus par le lecteur du juge), R-734 (un contrôle qui n'a pas pu tourner rend un code non nul).
⑨ CE QUI CLOCHE — ① E2 est une simulation (1 000 séries, graine fixe) : la fourchette 0,75-0,85 autour de 0,80 vaut
  environ quatre écarts-types de l'estimation ; sous la puissance 50 % du sabotage S01, le taux tombe vers 0,5.
  ② E4 ne juge rien : C5 a été réglée sur 2024-2026, son Sharpe y est affiché à titre de mesure, pas de preuve.
⑩ EFFET — Écrit et efface des dossiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 600 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""

import math
import os
import shutil
import subprocess
import sys
import tempfile

MC = "MODULE_COURBE_DU_COMPTE.py"
TRADES_C5 = os.path.join("donnees", "TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv")

# LES SABOTAGES : {nom : [(fichier, texte présent une fois, remplaçant)]}. Chacun retire ou fausse UNE propriété.
SABOTAGES = {
    "S01_puissance_oubliee": [(MC, "z = _NORMALE.inv_cdf(1.0 - seuil) + _NORMALE.inv_cdf(puissance)",
                               "z = _NORMALE.inv_cdf(1.0 - seuil)")],
    "S02_capital_fixe_et_non_engage": [(MC, "rendements = [g / (mise * k) if k else 0.0",
                                        "rendements = [g / mise if k else 0.0")],
    "S03_plancher_de_30_remis": [(MC, "    if seances_disponibles >= necessaires:\n",
                                  "    if seances_disponibles >= max(necessaires, 30):\n")],
    "S04_courbe_lissee_admise": [(MC, 'or courbe_de_l_effet.get("mode") != AU_COURS:',
                                  'or courbe_de_l_effet.get("mode") not in (AU_COURS, LISSEE):')],
    "S05_barre_du_hasard_ignoree": [(MC, 'seuil, puissance,\n                                   m["sharpe_du_meilleur_hasard"])',
                                     'seuil, puissance,\n                                   0.0)')],
    "S06_gain_de_vente_faux": [(MC, "                valeur = mise + net\n", "                valeur = mise + 0.5 * net\n")],
    "S07_cloture_manquante_tue": [(MC, "valeur, manquantes = precedente, manquantes + 1", "valeur = precedente")],
    "S08_aplatissement_en_exces": [(MC, "d = 1.0 - asymetrie * sharpe + (aplatissement - 1.0) / 4.0",
                                    "d = 1.0 - asymetrie * sharpe + (aplatissement - 3.0) / 4.0")],
    "S09_jours_sans_position_retires": [(MC, "rendements = [g / (mise * k) if k else 0.0 for g, k in zip(gains, ouvertes)]",
                                         "rendements = [g / (mise * k) for g, k in zip(gains, ouvertes) if k]")],
    "S10_hors_periode_admis": [(MC, "        if de not in rang or ds not in rang:\n            raise",
                                "        if False:\n            raise")],
    "S11_arrondi_par_defaut": [(MC, "necessaires = int(math.ceil(brut - 1e-9))", "necessaires = int(brut)")],
    "S12_puissance_moins_stricte_admise": [(MC, "    if p < ref:\n", "    if False:\n")],
    "S13_sharpe_sur_courbe_lissee": [(MC, '    if courbe.get("mode") != AU_COURS:\n        return None,',
                                      '    if False:\n        return None,')],
    "S14_vente_avant_achat_admise": [(MC, "        if i1 < i0:\n", "        if False:\n")],
    # lot W2bFIX (28-11-2026)
    "S15_cloture_manquante_mise_a_la_mise": [(MC, "valeur, manquantes = precedente, manquantes + 1",
                                              "valeur, manquantes = float(mise), manquantes + 1")],
    "S16_non_terminees_dans_la_courbe": [(MC, "    ops, non_terminees = J.mettre_a_part_les_non_terminees(ops)   #",
                                          "    _x, non_terminees = J.mettre_a_part_les_non_terminees(ops)   #")],
    "S17_non_terminees_dans_la_grille": [("MODULE_JUGEMENT.py", "    ops, non_terminees = mettre_a_part_les_non_terminees(ops)\n",
                                          "    _x, non_terminees = mettre_a_part_les_non_terminees(ops)\n")],
    "S18_latent_faux": [("MODULE_JUGEMENT.py", "        latent += net\n", "        latent += 0.0\n")],
    "S19_minimum_decide_encore_en_cas_2": [("MODULE_JUGEMENT.py", '        elif cas == "2":\n            # A-1103',
                                            '        elif False:\n            # A-1103')],
    "S20_role_condition_en_cas_2": [("MODULE_JUGEMENT.py", 'AFFICHAGE_EN_CAS_2 = ("gain_bat_zero", "observations_independantes")',
                                     'AFFICHAGE_EN_CAS_2 = ("gain_bat_zero",)')],
    "S21_refutee_exige_le_minimum": [("MODULE_JUGEMENT.py", 'obs_ok = (n_obs is not None) if cas == "2" else',
                                      'obs_ok = (n_obs is None) if cas == "2" else')],
    "S22_affichage_devient_condition": [(MC, '{"constat": INCONNU, "role": AFFICHAGE,',
                                         '{"constat": INCONNU, "role": "CONDITION",')],
    "S23_porte_sans_mise_a_part": [("JUGER_UNE_FICHE.py", "            jeu, _non_terminees = _operations_jugees(jeu)\n",
                                    "            _non_terminees = None\n")],
    "S24_assez_au_verdict": [("CONTRATS_DES_FICHIERS.py", '    "observations_independantes",  # ④',
                              '    "assez_de_donnees",\n    "observations_independantes",  # ④')],
}


def lancer(racine, sabotage):
    """Copie programmes/, applique un sabotage, relance ce fichier en « --cas » et rend (code, sortie).
    ① RÔLE — Un passage d'épreuves sur une copie, intacte (Z0) ou sabotée. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` ; `sabotage` : un nom de SABOTAGES ou None. ④ CONDITIONS D'ENTRÉE — programmes/ existe.
    ⑤ SORTIE — DEUX valeurs : le code de la relance (2 si une cible est introuvable) et sa sortie. [rend: 2]
    ⑥ TRAITEMENT — copier, remplacer (texte présent une fois exactement), relancer avec un délai de 600 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-731 : le sabotage porte sur une COPIE, jamais sur le dépôt.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — un dossier temporaire, effacé. ⑪ TERMINAISON — bornée à 600 s. [sort: non]"""
    tmp = tempfile.mkdtemp(prefix="W2b_epreuve_")
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
                               capture_output=True, text=True, timeout=600)
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return 1, "DÉLAI DÉPASSÉ"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def jours(n, debut="2030-01-07"):
    """Rend n séances fictives consécutives (jours de calendrier), en textes AAAA-MM-JJ.
    ① RÔLE — un calendrier fictif, hors de toute année réelle jugée. ② `cas`. ③ n, début. ④ — ⑤ UNE liste. [rend: 1]
    ⑥ jours consécutifs. ⑦ séances. ⑧ 2030 : aucune donnée réelle ne peut s'y glisser. ⑨ — ⑩ — ⑪ rend. [sort: non]"""
    import datetime as dt
    d0 = dt.date.fromisoformat(debut)
    return [(d0 + dt.timedelta(days=i)).isoformat() for i in range(n)]


def cas(prog, racine):
    """Joue les cas E1 à E10 sur les programmes du dossier `prog` et rend le nombre de rouges.
    ① RÔLE — Les épreuves elles-mêmes. ② CONTEXTE D'APPEL — `main`, en « --cas ». ③ ENTRÉE — `prog` : le dossier
    des programmes (copie) ; `racine` : les données. ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — UNE valeur :
    le nombre de cas rouges (une exception compte comme un rouge). [rend: 1] ⑥ TRAITEMENT — voir chaque cas.
    ⑦ UNITÉ — voir l'en-tête. ⑧ POURQUOI — une épreuve par propriété. ⑨ CE QUI CLOCHE — voir l'en-tête.
    ⑩ EFFET — écrit des fichiers temporaires (E9). ⑪ TERMINAISON — rend la main. [sort: non]"""
    sys.path.insert(0, prog)
    import random
    import MODULE_COURBE_DU_COMPTE as K
    import MODULE_SHARPE_DEGONFLE as SD
    import MODULE_JUGEMENT as J
    rouges = []

    def ok(nom, vrai, detail=""):
        """Affiche un cas. ① RÔLE — une ligne VERT/ROUGE. ② `cas`. ③ nom, booléen, détail. ④ — ⑤ aucune. [rend: 0]
        ⑥ — ⑦ — ⑧ — ⑨ — ⑩ EFFET — affiche. ⑪ Rend la main. [sort: non]"""
        print("  %s %s%s" % ("VERT " if vrai else "ROUGE", nom, ("  — " + str(detail)) if detail else ""))
        if not vrai:
            rouges.append(nom)

    def leve(f, *a):
        """Rend True si f(*a) lève ValueError. ① RÔLE — tester un refus. ② `cas`. ③ f, arguments. ④ — ⑤ booléen.
        [rend: 1] ⑥ appeler. ⑦ — ⑧ un refus doit LEVER, jamais rendre une courbe. ⑨ — ⑩ — ⑪ rend. [sort: non]"""
        try:
            f(*a)
        except ValueError:
            return True
        except Exception:  # noqa: BLE001 — une autre erreur n'est pas le refus attendu
            return False
        return False

    def essai(nom, f):
        """Joue un groupe de cas ; une exception est un rouge. ① RÔLE — isoler les groupes. ② `cas`. ③ nom, fonction.
        ④ — ⑤ aucune. [rend: 0] ⑥ appeler. ⑦ — ⑧ R-734. ⑨ — ⑩ affiche. ⑪ rend. [sort: non]"""
        try:
            f()
        except Exception as e:  # noqa: BLE001 — toute chute d'un groupe est un rouge, nommé
            ok(nom + " (le groupe a levé)", False, "%s: %s" % (type(e).__name__, e))

    # E1 — CALIBRAGE SUR LES CHIFFRES PUBLIÉS : à puissance 50 % (Z⁻¹ = 0), la formule est la MinTRL de Bailey et López
    # de Prado (2012, équation 13 p. 11) ; exemples de la section 5 p. 11-12 et de l'annexe A.3 : SR annualisé 2,
    # SR* = 1, 95 % ; mensuel γ3 = −0,72, γ4 = 5,78 → « obs=59.895 », « approx. 4.99 years » ; loi normale : quotidien
    # 2,73 ans, hebdomadaire 2,83, mensuel 3,24.
    def e1():
        def ans(q, s3, s4):
            return K.seances_necessaires(2 / math.sqrt(q), s3, s4, 0.05, 0.5, 1 / math.sqrt(q)) / q
        n = K.seances_necessaires(2 / math.sqrt(12), -0.72, 5.78, 0.05, 0.5, 1 / math.sqrt(12))
        ok("E1a mensuel non normal : 59,895 mois (article, annexe A.3)", abs(n - 59.895) < 0.001, "%.4f" % n)
        ok("E1b le même en années : 4,99", round(n / 12, 2) == 4.99, "%.4f" % (n / 12))
        for nom, q, attendu in (("quotidien (252)", 252, 2.73), ("hebdomadaire (52)", 52, 2.83), ("mensuel", 12, 3.24)):
            a = ans(q, 0.0, 3.0)
            ok("E1c loi normale, %s : %.2f ans" % (nom, attendu), round(a, 2) == attendu, "%.4f" % a)
    essai("E1", e1)

    # E2 — LA PUISSANCE RÉELLE : des séries normales de Sharpe 0,2 par séance, de la longueur que la fonction dit
    # nécessaire à 80 % et au seuil 0,01 ; le test du contrôle 1 (Sharpe dégonflé du lot L3, k = 1) doit les reconnaître
    # environ 8 fois sur 10.
    def e2():
        sr, seuil, p = 0.2, 0.01, 0.80
        t = int(math.ceil(K.seances_necessaires(sr, 0.0, 3.0, seuil, p, 0.0)))
        g = random.Random(20261127)
        rejets = 0
        for _ in range(1000):
            x = [g.gauss(sr, 1.0) for _ in range(t)]
            if 1.0 - SD.sharpe_degonfle_d_une_serie(x, 1, None)["probabilite"] < seuil:
                rejets += 1
        ok("E2 puissance mesurée sur 1 000 séries de %d séances : entre 0,75 et 0,85" % t,
           0.75 <= rejets / 1000 <= 0.85, "%.3f" % (rejets / 1000))
    essai("E2", e2)

    # E3 — VINGT ACHATS NÉS DE LA MÊME CHUTE NE COMPTENT QU'UNE FOIS (A-1071), montré sur la courbe : 60 séances
    # fictives, des opérations indépendantes, puis la même chute jouée par UN achat, ou par VINGT achats de vingt
    # valeurs au même parcours, mêmes dates. La courbe, le Sharpe et le minimum de séances doivent être identiques ;
    # seul le nombre de positions ouvertes change. Compter par opération dirait 20 preuves au lieu d'une.
    def e3():
        s = jours(60)
        g = random.Random(7)
        prix = {s[i]: 100.0 * (1 + 0.01 * g.uniform(-1, 1)) for i in range(60)}
        clot = {"V%02d" % i: dict(prix) for i in range(20)}
        clot["A"] = {d: 100.0 for d in s}        # parcours plat : tout le gain de la base tombe le jour de la vente
        base = [{"date_entree": s[i], "date_sortie": s[i + 2], "net": g.uniform(-1000, 4000), "valeur": "A",
                 "pe": 100.0} for i in range(0, 50, 5)]
        chute = {"date_entree": s[51], "date_sortie": s[55], "net": 3700.0, "pe": 100.0}
        un = K.courbe_du_compte(base + [dict(chute, valeur="V00")], s, clot)
        vingt = K.courbe_du_compte(base + [dict(chute, valeur="V%02d" % i) for i in range(20)], s, clot)
        ok("E3a la courbe de vingt achats est celle d'un seul",
           all(abs(a - b) < 1e-12 for a, b in zip(un["rendements"], vingt["rendements"]))
           and len(un["rendements"]) == len(vingt["rendements"]) == 60)
        ok("E3b même nombre de séances (60), alors que les opérations passent de %d à %d"
           % (un["n_operations"], vingt["n_operations"]), un["n_seances"] == vingt["n_seances"] == 60
           and vingt["n_operations"] - un["n_operations"] == 19)
        ok("E3c vingt positions ouvertes ensemble, un seul rendement par séance",
           max(vingt["positions_ouvertes"]) == 20 and max(un["positions_ouvertes"]) == 1)
        ok("E3d le gain en euros, lui, est vingt fois celui d'un achat (aucun euro perdu)",
           abs(sum(vingt["gains_eur"]) - sum(un["gains_eur"]) - 19 * 3700.0) < 1e-6)
        a1 = K.assez_de_donnees(un, 60, 1, None, 0.05, 0.80)
        a20 = K.assez_de_donnees(vingt, 60, 1, None, 0.05, 0.80)
        ok("E3e même minimum de séances et même verdict", a1["seances_necessaires"] == a20["seances_necessaires"]
           and a1["constat"] == a20["constat"] and a1["seances_necessaires"] is not None,
           "%s / %s séances, %s" % (a1["seances_necessaires"], a20["seances_necessaires"], a1["constat"]))
    essai("E3", e3)

    # E4 — UNE VRAIE LIGNE DE NOS FICHIERS (R-732) : les 100 opérations simulées de C5-ETENDU-10 (2024-2026), avec les
    # cours lus par le lecteur du juge et les séances du calendrier de la bourse. La somme des gains de la courbe est la
    # somme des gains nets du tableau (aucun euro créé ni perdu) ; la courbe lissée gonfle le Sharpe et ne décide pas.
    def e4():
        import csv
        import JUGE_DES_STRATEGIES as JS
        lignes = list(csv.DictReader(open(os.path.join(racine, TRADES_C5), encoding="utf-8"), delimiter=";"))
        f = lambda x: float(x.replace(",", "."))
        # la clé de la valeur par la traduction du juge (COMMUN : « UNIBAIL_RODAMCO_WESTFIELD » du tableau → clé
        # « UNIBAIL_RODAMCO » des cours, mnémonique URW) ; jamais une table recopiée ici
        ops = [{"date_entree": l["date_entree"], "date_sortie": l["date_sortie"], "valeur": JS.cle_valeur(l["valeur"]),
                "pe": f(l["prix_entree"]), "net": f(l["net_eur"])} for l in lignes]
        ok("E4a la première ligne réelle est lue telle quelle (AIRBUS, 2024-02-21 → 2024-02-28, +3 700 €)",
           ops[0] == {"date_entree": "2024-02-21", "date_sortie": "2024-02-28", "valeur": "AIRBUS", "pe": 145.88,
                      "net": 3700.0} and len(ops) == 100)
        mnemo = JS.table_mnemoniques(JS.trouver(racine, "REFERENTIEL_VALEURS"))
        cours, _l = JS.lire_par_le_lecteur(racine, os.path.join("donnees", "cours_maitre.csv"), mnemo)
        clot = K.clotures_des_cours(cours)
        s = K.seances_de_la_periode(racine, min(o["date_entree"] for o in ops), max(o["date_sortie"] for o in ops))
        c = K.courbe_du_compte(ops, s, clot)
        total = sum(o["net"] for o in ops)
        ok("E4b somme des gains de la courbe = somme des gains nets (%.2f €)" % total,
           abs(sum(c["gains_eur"]) - total) < 0.01, "%.4f" % sum(c["gains_eur"]))
        ok("E4c une séance du calendrier par rendement (%d), clôtures manquantes comptées (%d)"
           % (c["n_seances"], c["clotures_manquantes"]),
           c["n_seances"] == len(s) == len(c["rendements"]) and c["mode"] == K.AU_COURS)
        # le 24-12-2024 : séance au calendrier si l'indice l'a publiée ; mesuré, pas supposé
        li = K.courbe_du_compte(ops, s, None)
        m_au = SD.moments_des_rendements(c["rendements"])
        m_li = SD.moments_des_rendements(li["rendements"])
        ok("E4d la courbe lissée sous-estime les secousses : écart-type %.6f lissé < %.6f au cours"
           % (m_li["ecart_type"], m_au["ecart_type"]), m_li["ecart_type"] < m_au["ecart_type"]
           and abs(sum(li["gains_eur"]) - total) < 0.01)
        a_li = K.assez_de_donnees(li, li["n_seances"], 1, None, 0.05, 0.80)
        ok("E4e la courbe lissée ne décide pas : INCONNU", a_li["constat"] == K.INCONNU, a_li["raison"][:80])
        a = K.assez_de_donnees(c, c["n_seances"], 1, None, 0.05, 0.80)
        ok("E4f la courbe au cours se calcule (mesure affichée, pas un jugement : C5 a été réglée sur ces années)",
           a["constat"] in (K.ASSEZ, K.PAS_ASSEZ) and a["seances_necessaires"] is not None,
           "Sharpe %.4f par séance, γ3 %.2f, γ4 %.2f ; %s séances nécessaires, %d disponibles : %s"
           % (a["sharpe_par_seance"], a["asymetrie"], a["aplatissement"], a["seances_necessaires"],
              a["seances_disponibles"], a["constat"]))
        # une clôture retirée : la séance garde la valeur de la veille et se compte
        o = ops[0]
        clot2 = {v: dict(t) for v, t in clot.items()}
        retiree = s[s.index(o["date_entree"]) + 1]
        del clot2[o["valeur"]][retiree]
        c2 = K.courbe_du_compte(ops, s, clot2)
        ok("E4g une clôture retirée (%s %s) se compte, et la somme reste juste" % (o["valeur"], retiree),
           c2["clotures_manquantes"] == c["clotures_manquantes"] + 1 and abs(sum(c2["gains_eur"]) - total) < 0.01)
        # W2b-2 (relecture Cowork du 28-11-2026) : la séance sans clôture garde la valeur de la veille, gain NUL ce jour
        seul = K.courbe_du_compte([o], s, clot2)
        ok("E4h la séance sans clôture rend un gain nul pour la position (valeur de la veille gardée)",
           seul["positions_ouvertes"][s.index(retiree)] == 1 and seul["gains_eur"][s.index(retiree)] == 0.0,
           seul["gains_eur"][s.index(retiree)])
        # A-1108 sur une VRAIE ligne (R-732) : le dernier trade réel de C5 marqué « non terminé » (motif FIN_DES_DONNEES)
        # sort de la courbe dès son achat ; la courbe est celle des 99 autres, et son gain s'affiche à part.
        motif = J._commun().MOTIF_FIN_DES_DONNEES
        marque = ops[:-1] + [dict(ops[-1], motif=motif)]
        c3, c99 = K.courbe_du_compte(marque, s, clot), K.courbe_du_compte(ops[:-1], s, clot)
        ok("E4i vraie ligne non terminée (%s %s, %+.2f €) : courbe = celle des 99 autres, affichée à part"
           % (ops[-1]["valeur"], ops[-1]["date_entree"], ops[-1]["net"]),
           c3["rendements"] == c99["rendements"] and c3["gains_eur"] == c99["gains_eur"] and c3["n_operations"] == 99
           and c3["non_terminees"]["n"] == 1 and c3["non_terminees"]["resultat_latent_eur"] == ops[-1]["net"]
           and c3["non_terminees"]["role"] == "AFFICHAGE" and c["non_terminees"]["n"] == 0,
           c3["non_terminees"])
    essai("E4", e4)

    # E5 — LES SÉANCES SANS POSITION COMPTENT : zéro, et dans la série.
    def e5():
        s = jours(10)
        clot = {"A": {d: 100.0 + i for i, d in enumerate(s)}}
        c = K.courbe_du_compte([{"date_entree": s[2], "date_sortie": s[4], "net": 1000.0, "valeur": "A",
                                 "pe": 102.0}], s, clot)
        ok("E5a dix séances, dix rendements ; les sept sans position valent zéro et restent dans la série",
           len(c["rendements"]) == 10 and c["n_seances_investies"] == 3
           and all(r == 0.0 for r, k in zip(c["rendements"], c["positions_ouvertes"]) if k == 0)
           and sum(1 for k in c["positions_ouvertes"] if k == 0) == 7 and c["rendements"][3] > 0)
        ok("E5b la valeur au cours : séance 2 = 0, séance 3 = 100 000 × 103 ÷ 102 − 100 000",
           abs(c["gains_eur"][2]) < 1e-9 and abs(c["gains_eur"][3] - (1e5 * 103 / 102 - 1e5)) < 1e-6
           and abs(sum(c["gains_eur"]) - 1000.0) < 1e-9)
    essai("E5", e5)

    # E6 — LES REFUS : jamais une courbe fausse, jamais un faux vert.
    def e6():
        s = jours(10)
        clot = {"A": {d: 100.0 for d in s}}
        op = {"date_entree": s[2], "date_sortie": s[4], "net": 10.0, "valeur": "A", "pe": 100.0}
        ok("E6a opération qui déborde de la période : refusée", leve(K.courbe_du_compte,
           [dict(op, date_sortie="2031-01-01")], s, clot))
        ok("E6b vente avant l'achat : refusée", leve(K.courbe_du_compte, [dict(op, date_entree=s[5])], s, clot))
        ok("E6c séances non croissantes : refusées", leve(K.courbe_du_compte, [op], [s[1], s[0]] + s[2:], clot))
        ok("E6d gain non fini : refusé", leve(K.courbe_du_compte, [dict(op, net=float("nan"))], s, clot))
        ok("E6e prix d'entrée nul : refusé", leve(K.courbe_du_compte, [dict(op, pe=0.0)], s, clot))
        plate = K.courbe_du_compte([], s, clot)
        ok("E6f courbe sans opération : INCONNU", K.assez_de_donnees(plate, 10, 1, None, 0.05, 0.8)["constat"]
           == K.INCONNU)
        g = random.Random(3)
        bonne = {"mode": K.AU_COURS, "rendements": [g.gauss(0.3, 1.0) for _ in range(400)]}
        for nom, args in (("seuil 0", (bonne, 400, 1, None, 0.0, 0.8)), ("puissance 1", (bonne, 400, 1, None, 0.05, 1.0)),
                          ("k = 3 sans Sharpe d'essais", (bonne, 400, 3, None, 0.05, 0.8)),
                          ("séances disponibles négatives", (bonne, -1, 1, None, 0.05, 0.8)),
                          ("courbe sans mode", ({"rendements": bonne["rendements"]}, 400, 1, None, 0.05, 0.8))):
            r = K.assez_de_donnees(*args)
            ok("E6g %s : INCONNU avec sa raison" % nom, r["constat"] == K.INCONNU and r["raison"], r["raison"][:70])
        perd = {"mode": K.AU_COURS, "rendements": [g.gauss(-0.2, 1.0) for _ in range(400)]}
        r = K.assez_de_donnees(perd, 400, 1, None, 0.05, 0.8)
        ok("E6h effet négatif : PAS ASSEZ, aucune longueur ne suffit", r["constat"] == K.PAS_ASSEZ
           and r["seances_necessaires"] is None and math.isinf(r["seances_necessaires_brut"]))
        m, raison = K.sharpe_degonfle_de_la_courbe(K.courbe_du_compte([op], s, None), 1, None)
        ok("E6i Sharpe dégonflé sur courbe lissée : refusé", m is None and "lissée" in raison)
    essai("E6", e6)

    # E7 — LE PLANCHER FIXE DE 30 NE DÉCIDE NULLE PART : ① la grille du juge ne lit plus sa ligne (clé hors des clés
    # lues) et rend le même contrôle ④ que la table dise 30, 1 ou un milliard ; ② ce module ne porte aucun 30 et dit
    # ASSEZ dès que le minimum calculé est atteint, même sous 30.
    def e7():
        import ast
        ok("E7a « plancher_observations » n'est pas une clé lue par la grille",
           "plancher_observations" not in J.CLES_DE_LA_TABLE_LUES_PAR_LA_GRILLE)
        modele = ("x\n  **LES SEUILS DE CETTE LOI** — épreuve\n\n  | clé | valeur | sens | source |\n  |---|---|---|---|\n"
                  "  | seuil_de_preuve | 0,05 ÷ k | g | e |\n  | plancher_observations | {p} | p | e |\n\nfin\n")
        s = jours(200)
        g = random.Random(11)
        ops = [{"date_signal": s[i], "date_entree": s[i], "date_sortie": s[i + 1], "net": g.uniform(-2800, 3700),
                "valeur": "X"} for i in range(0, 190, 4)]
        rendus = []
        for p in ("30", "1", "1000000000"):
            r = J.grille_de_validation(J.table_de_la_loi(modele.format(p=p)), "2", 1, ops=ops)
            rendus.append((r["controles"]["observations_independantes"], r["verdict"], r["premier_controle_bloquant"]))
        ok("E7b contrôle ④ et verdict identiques pour un plancher de 30, 1 ou 10⁹", rendus[0] == rendus[1] == rendus[2],
           "④ %s (seuil %s)" % (rendus[0][0]["etat"], rendus[0][0]["seuil"]))
        arbre = ast.parse(open(K.__file__, encoding="utf-8").read())
        trente = [n.lineno for n in ast.walk(arbre) if isinstance(n, ast.Constant) and n.value == 30]
        ok("E7c aucun nombre 30 dans le code du module", not trente, trente)
        g2 = random.Random(5)
        forte = {"mode": K.AU_COURS, "rendements": [g2.gauss(1.2, 1.0) for _ in range(25)]}
        r = K.assez_de_donnees(forte, 25, 1, None, 0.05, 0.80)
        ok("E7d une stratégie très forte : ASSEZ avec 25 séances, sous 30", r["constat"] == K.ASSEZ
           and r["seances_necessaires"] < 25, "%s nécessaires" % r["seances_necessaires"])
    essai("E7", e7)

    # E8 — BRANCHÉ SUR LE SHARPE DÉGONFLÉ DU LOT L3, SANS RECOPIE : même probabilité que le mesureur de L3 ; le minimum
    # utilise le SR0 de L3 (k essais, variance des Sharpe des essais), pas un SR0 refait.
    def e8():
        s = jours(300)
        g = random.Random(13)
        clot = {"A": {}}
        p = 100.0
        for d in s:
            p *= 1 + g.gauss(0.002, 0.01)
            clot["A"][d] = p
        ops = [{"date_entree": s[i], "date_sortie": s[i + 3], "valeur": "A", "pe": clot["A"][s[i]],
                "net": 1e5 * (clot["A"][s[i + 3]] / clot["A"][s[i]] - 1) - 300.0} for i in range(0, 290, 6)]
        c = K.courbe_du_compte(ops, s, clot)
        essais = [g.gauss(0.0, 0.05) for _ in range(20)]
        m, r = K.sharpe_degonfle_de_la_courbe(c, 20, essais)
        m_l3, _r = J.mesurer_le_sharpe_degonfle(c["rendements"], 20, essais)
        ok("E8a même Sharpe dégonflé que le mesureur de L3", m is not None and m["sharpe_degonfle"]
           == m_l3["sharpe_degonfle"] and m["nombre_d_essais"] == 20, r)
        v = sum((x - sum(essais) / 20) ** 2 for x in essais) / 19
        a = K.assez_de_donnees(c, 300, 20, essais, 0.05 / 20, 0.80)
        ok("E8b le minimum utilise la barre SR0 de L3 (k = 20)",
           a["sharpe_du_meilleur_hasard"] == SD.sharpe_attendu_du_meilleur_hasard(20, v) > 0
           and a["seances_necessaires_brut"] == K.seances_necessaires(
               a["sharpe_par_seance"], a["asymetrie"], a["aplatissement"], 0.05 / 20, 0.80, a["sharpe_du_meilleur_hasard"]),
           "SR0 %.5f, %s séances" % (a["sharpe_du_meilleur_hasard"] or 0, a["seances_necessaires"]))
        a1 = K.assez_de_donnees(c, 300, 1, None, 0.05, 0.80)
        ok("E8c plus d'essais, plus de séances nécessaires (k = 20 contre k = 1)",
           a["seances_necessaires_brut"] > a1["seances_necessaires_brut"])
    essai("E8", e8)

    # E9 — LA PUISSANCE EST LUE AU FICHIER DÉCLARÉ, 0,80, et une valeur moins stricte est refusée.
    def e9():
        import CONTRATS_DES_FICHIERS as CT
        p, r = K.puissance_visee(racine)
        ok("E9a vrai fichier : 0,80", p == 0.80, r)
        vrai = open(os.path.join(racine, CT.SEUILS_EN_ATTENTE_DU_REGISTRE), encoding="utf-8").read()
        for nom, texte in (("0,50 (moins strict)", vrai.replace('puissance_visee,"0,80"', 'puissance_visee,"0,50"')),
                           ("ligne absente", "\n".join(l for l in vrai.splitlines()
                                                       if not l.startswith("puissance_visee")) + "\n"),
                           ("1,5", vrai.replace('puissance_visee,"0,80"', 'puissance_visee,"1,5"'))):
            tmp = tempfile.mkdtemp(prefix="W2b_E9_")
            try:
                os.makedirs(os.path.join(tmp, "donnees"))
                open(os.path.join(tmp, CT.SEUILS_EN_ATTENTE_DU_REGISTRE), "w", encoding="utf-8").write(texte)
                p, r = K.puissance_visee(tmp)
                ok("E9b %s : refusée" % nom, p is None and r, r[:70])
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        p95 = vrai.replace('puissance_visee,"0,80"', 'puissance_visee,"0,90"')
        tmp = tempfile.mkdtemp(prefix="W2b_E9_")
        try:
            os.makedirs(os.path.join(tmp, "donnees"))
            open(os.path.join(tmp, CT.SEUILS_EN_ATTENTE_DU_REGISTRE), "w", encoding="utf-8").write(p95)
            p, r = K.puissance_visee(tmp)
            ok("E9c 0,90 (plus strict) : admise", p == 0.90, r)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    essai("E9", e9)

    # E10 — LE MINIMUM BOUGE DANS LE BON SENS, et l'arrondi est au-dessus.
    def e10():
        n = lambda sr=0.1, s3=0.0, s4=3.0, a=0.01, p=0.8, sr0=0.0: K.seances_necessaires(sr, s3, s4, a, p, sr0)
        ok("E10a puissance 90 % > 80 % > 50 %", n(p=0.9) > n(p=0.8) > n(p=0.5))
        ok("E10b barre plus basse (0,001) : plus de séances", n(a=0.001) > n(a=0.01))
        ok("E10c asymétrie négative et queues épaisses : plus de séances", n(s3=-1.0, s4=8.0) > n())
        ok("E10d effet double : environ quatre fois moins", 3.5 < (n(sr=0.1) - 1) / (n(sr=0.2) - 1) < 4.5)
        g = random.Random(17)
        c = {"mode": K.AU_COURS, "rendements": [g.gauss(0.15, 1.0) for _ in range(600)]}
        a = K.assez_de_donnees(c, 600, 1, None, 0.01, 0.8)
        brut = a["seances_necessaires_brut"]
        ok("E10e minimum = arrondi AU-DESSUS du calcul (%.3f → %s)" % (brut, a["seances_necessaires"]),
           a["seances_necessaires"] == math.ceil(brut))
        b = K.assez_de_donnees(c, math.ceil(brut) - 1, 1, None, 0.01, 0.8)
        h = K.assez_de_donnees(c, math.ceil(brut), 1, None, 0.01, 0.8)
        ok("E10f une séance de moins que le minimum : PAS ASSEZ ; le minimum : ASSEZ",
           b["constat"] == K.PAS_ASSEZ and h["constat"] == K.ASSEZ)
    essai("E10", e10)

    # E11 — A-1103 (Jean-Luc, 27-11-2026 à 22h04, « 1 ») : LE CONTRÔLE « ASSEZ DE DONNÉES » EST AFFICHÉ, IL NE DÉCIDE
    # PLUS. ① chaque rendu d'`assez_de_donnees` porte le rôle AFFICHAGE, quelle que soit son étiquette ; ② aucune clé
    # « assez_de_donnees » parmi les contrôles qui font le verdict ; ③ en cas 2, le contrôle ④ de la grille ne décide
    # plus par le minimum d'A-782 : sous le minimum, il PASSE en AFFICHAGE, le minimum montré ; en cas 1, rien ne change ;
    # ④ en cas 2, la voie RÉFUTÉE ne demande plus le minimum atteint.
    def e11():
        g = random.Random(3)
        forte = {"mode": K.AU_COURS, "rendements": [g.gauss(1.2, 1.0) for _ in range(25)]}
        faible = {"mode": K.AU_COURS, "rendements": [g.gauss(0.01, 1.0) for _ in range(25)]}
        rendus = [K.assez_de_donnees(forte, 25, 1, None, 0.05, 0.8), K.assez_de_donnees(faible, 25, 1, None, 0.05, 0.8),
                  K.assez_de_donnees({"mode": K.LISSEE, "rendements": []}, 25, 1, None, 0.05, 0.8)]
        ok("E11a ASSEZ, PAS ASSEZ, INCONNU : tous au rôle AFFICHAGE, nécessaires et disponibles rendus",
           [r["constat"] for r in rendus] == [K.ASSEZ, K.PAS_ASSEZ, K.INCONNU]
           and all(r["role"] == K.AFFICHAGE == "AFFICHAGE" and "verdict" not in r for r in rendus)
           and rendus[0]["seances_necessaires"] is not None and rendus[0]["seances_disponibles"] == 25,
           [(r["constat"], r["role"]) for r in rendus])
        ordre = J._contrat("CONTROLES_DU_VERDICT")
        ok("E11b aucune clé « assez_de_donnees » parmi les contrôles du verdict",
           "assez_de_donnees" not in ordre and "observations_independantes" in ordre)
        modele = ("x\n  **LES SEUILS DE CETTE LOI** — épreuve\n\n  | clé | valeur | sens | source |\n  |---|---|---|---|\n"
                  "  | seuil_de_preuve | 0,05 ÷ k | g | e |\n  | refutation_borne_haute | 0,05 | r | e |\n\nfin\n")
        t = J.table_de_la_loi(modele)
        s = jours(400)
        # 10 opérations espacées, 5 gagnantes de +100 €, 5 perdantes de −3 000 € : q = 1/2, k = 69 → minimum d'A-782
        # = ⌈ln(0,05 ÷ 69) ÷ ln(0,5)⌉ = 11 > 10 observations
        nets = [100.0, -3000.0] * 5
        ops = [{"date_signal": s[30 * i], "date_entree": s[30 * i], "date_sortie": s[30 * i + 3], "net": x,
                "valeur": "X"} for i, x in enumerate(nets)]
        mini = J.minimum_d_observations(nets, 0.05 / 69)
        commun = dict(ops=ops, declaration_manquants=[], seances_hors_examen=0, regards_anterieurs=[])
        r2, r1 = J.grille_de_validation(t, "2", 69, **commun), J.grille_de_validation(t, "1", 69, **commun)
        c2, c1 = r2["controles"]["observations_independantes"], r1["controles"]["observations_independantes"]
        mots = J._contrat("MOTS_DU_VERDICT")
        ok("E11c cas 2, %s observations sous le minimum de %s : ④ PASSE en AFFICHAGE, minimum montré" % (c2["valeur"], mini),
           c2["valeur"] is not None and c2["valeur"] < mini and c2["etat"] == "PASSE" and c2["role"] == "AFFICHAGE"
           and c2["detail"]["minimum_a_782"] == mini and c2["detail"]["au_dessus_du_minimum"] is False,
           (c2["etat"], c2["role"], c2.get("detail", {}).get("minimum_a_782")))
        ok("E11d cas 1 inchangé : ④ CONDITION, BLOQUE « TROP PETIT »",
           c1["etat"] == "BLOQUE" and c1["role"] == "CONDITION" and c1["raison"] == "TROP PETIT", (c1["etat"], c1["role"]))
        ok("E11e cas 2 : RÉFUTÉE sans le minimum (borne haute du gain sous zéro) ; cas 1 : jamais RÉFUTÉE sous le minimum",
           r2["verdict"] == mots[1] and r1["verdict"] != mots[1], (r2["verdict"], r1["verdict"]))
        # la grille rend le même verdict que la mesure d'assez de données dise ASSEZ ou PAS ASSEZ (elle ne la lit pas)
        va = J.grille_de_validation(t, "2", 69, mesures_externes={"assez_de_donnees": rendus[0]}, **commun)
        vp = J.grille_de_validation(t, "2", 69, mesures_externes={"assez_de_donnees": rendus[1]}, **commun)
        ok("E11f même verdict de la grille avec « assez » ASSEZ ou PAS ASSEZ",
           (va["verdict"], va["motif"], va["premier_controle_bloquant"]) == (vp["verdict"], vp["motif"],
                                                                              vp["premier_controle_bloquant"]))
    essai("E11", e11)

    # E12 — A-1108 (Jean-Luc, 27-11-2026 à 22h29, « 2 ») : LES POSITIONS NON TERMINÉES SONT EXCLUES du gain jugé, de la
    # courbe (dès leur achat), du Kelly et du taux de réussite, et AFFICHÉES (nombre, résultat latent frais compris).
    def e12():
        motif = J._commun().MOTIF_FIN_DES_DONNEES
        s = jours(60)
        clot = {"A": {d: 100.0 + (i % 7) for i, d in enumerate(s)}, "B": {d: 50.0 - (i % 5) for i, d in enumerate(s)}}
        termine = {"date_entree": s[2], "date_sortie": s[8], "net": 1200.0, "valeur": "A", "pe": 102.0, "motif": "TP"}
        ouverte = {"date_entree": s[5], "date_sortie": s[59], "net": -9000.0, "valeur": "B", "pe": 50.0, "motif": motif}
        avec, sans = K.courbe_du_compte([termine, ouverte], s, clot), K.courbe_du_compte([termine], s, clot)
        ok("E12a courbe : la position non terminée n'y entre à aucune séance, dès son achat",
           avec["rendements"] == sans["rendements"] and avec["positions_ouvertes"] == sans["positions_ouvertes"]
           and avec["n_operations"] == 1)
        ok("E12b affichée : 1 position, résultat latent −9 000 € (son net : dernier cours, frais de vente compris)",
           avec["non_terminees"] == {"n": 1, "resultat_latent_eur": -9000.0, "role": "AFFICHAGE"}, avec["non_terminees"])
        ok("E12c un résultat latent illisible est refusé, jamais tu",
           leve(J.mettre_a_part_les_non_terminees, [dict(ouverte, net=float("nan"))]))
        modele = ("x\n  **LES SEUILS DE CETTE LOI** — épreuve\n\n  | clé | valeur | sens | source |\n  |---|---|---|---|\n"
                  "  | seuil_de_preuve | 0,05 ÷ k | g | e |\n\nfin\n")
        t = J.table_de_la_loi(modele)
        j = jours(400)
        g = random.Random(23)
        ops = [{"date_signal": j[8 * i], "date_entree": j[8 * i], "date_sortie": j[8 * i + 3],
                "net": g.uniform(-2500, 3500), "valeur": "X", "motif": "TP"} for i in range(40)]
        perte = {"date_signal": j[390], "date_entree": j[390], "date_sortie": j[399], "net": -60000.0, "valeur": "X",
                 "motif": motif}
        ga = J.grille_de_validation(t, "2", 1, ops=ops + [perte], point_mort_pct=40.0)
        gs = J.grille_de_validation(t, "2", 1, ops=ops, point_mort_pct=40.0)
        vals = lambda r: [(cle, r["controles"][cle]["etat"], r["controles"][cle]["valeur"])
                          for cle in ("observations_independantes", "gain_bat_zero", "taux_face_au_point_mort")]
        ok("E12d grille : gain jugé, observations et taux de réussite identiques avec ou sans la perte non terminée",
           vals(ga) == vals(gs) and ga["verdict"] == gs["verdict"], vals(ga))
        ok("E12e grille : la position non terminée est affichée (1, −60 000 €)",
           ga["non_terminees"] == {"n": 1, "resultat_latent_eur": -60000.0, "role": "AFFICHAGE"}
           and gs["non_terminees"]["n"] == 0, ga["non_terminees"])
        # LE KELLY, LE HASARD ET LE POINT MORT de la porte du juge (JUGER_UNE_FICHE) : la mise à part se fait AVANT eux.
        # Épreuve de STRUCTURE (la porte exige un dépôt git et une déclaration : non jouée ici, dit dans la note).
        import ast
        src = open(os.path.join(prog, "JUGER_UNE_FICHE.py"), encoding="utf-8").read()
        f = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "juger_une_fiche"][0]
        lignes = {}
        for n in ast.walk(f):
            if isinstance(n, ast.Call):
                nom = ast.unparse(n.func)
                lignes.setdefault(nom, []).append(n.lineno)
        # (28-11-2026, réunion I1) la mise à part de la porte passe par `_operations_jugees` (éprouvée par ailleurs dans
        # EPREUVES_DE_LA_REUNION_I1, R6, avec le jeu qu'elle remplace)
        part = min(lignes.get("_operations_jugees", [10 ** 9]))
        apres = [min(lignes.get(x, [0])) for x in ("mesurer", "_hasard", "J.point_mort_des_operations")]
        ok("E12f porte du juge : mise à part (ligne %s) avant le Kelly et les mesureurs, le hasard, le point mort %s"
           % (part, apres), all(part < x for x in apres) and part < 10 ** 9)
    essai("E12", e12)

    print("== %d rouge(s)" % len(rouges))
    return len(rouges)


def main():
    """Point d'entrée : Z0, puis les sabotages demandés.
    ① RÔLE — Orchestrer. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — sys.argv. ④ — ⑤ SORTIE — par
    sys.exit. [rend: rien] ⑥ « --cas » : jouer ; sinon Z0 puis sabotages. ⑦ — ⑧ R-731, R-734. ⑨ — ⑩ affiche.
    ⑪ TERMINAISON — sort par sys.exit. [sort: oui — code de sortie]"""
    a = sys.argv[1:]
    if a[:1] == ["--cas"]:
        sys.exit(1 if cas(a[1], a[2]) else 0)
    if not a:
        print("usage : <racine> [--saboter | <sabotage>]")
        sys.exit(2)
    racine = os.path.abspath(a[0])
    for f in (os.path.join("programmes", MC), TRADES_C5, os.path.join("donnees", "cours_maitre.csv")):
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
