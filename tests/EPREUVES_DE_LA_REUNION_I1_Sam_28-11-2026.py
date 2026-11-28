#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_REUNION_I1_Sam_28-11-2026.py — Sam 28-11-2026 (Paris), réunion I1 du plan R505. Simulation
uniquement : des opérations FICTIVES, aucun ordre réel, aucune stratégie réelle jouée.

LE SENS EN TÊTE — La réunion des lots du plan R505 (branche lot-r505-I1) devait résoudre les cinq contradictions de la
relecture neuve V2 (preuves/V2_RELU.md) et trois sabotages restés verts qui « peuvent fausser un verdict ». Ce fichier
éprouve CE QUE LA RÉUNION A CHANGÉ, une propriété par cas, et sabote chaque correction pour montrer que son cas rougit.

① RÔLE — Les épreuves de la réunion I1 : C1 (une seule règle « position non terminée »), C2 (AFFICHAGE_EN_CAS_2), C3 (k
  du juge par ressemblance), C5 (A-1117 : opérations sans type exclues du contrôle 2 et comptées), le jour absent du
  découpage jamais admis, la mise à part non jetée dans la porte du juge.
② CONTEXTE D'APPEL — À la main ou par GitHub : `python3 -B tests/EPREUVES_DE_LA_REUNION_I1_Sam_28-11-2026.py <racine>
  [--saboter]`.
③ ENTRÉE — La racine d'un dépôt (programmes/ dessous).
④ CONDITIONS D'ENTRÉE — numpy (pour `k_du_juge`).
⑤ SORTIE — Le code de sortie : 0 tout vert (et, avec --saboter, chaque sabotage mord) ; 1 sinon ; 2 si une cible de
  sabotage est introuvable ou si le contrôle n'a pas pu tourner (R-734).
⑥ TRAITEMENT — Z0 sur une copie intacte, puis chaque sabotage sur une copie.
⑦ UNITÉ — Euros ; probabilités.
⑧ POURQUOI — R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration.
⑨ CE QUI CLOCHE — ① La grille (contrôle ⑥ décidé par le seul « meme_type ») s'éprouve dans EPREUVES_B_DU_BLOC_5A
  (G2, G2c), pas ici. ② Aucun cas ne tire de VRAIE ligne de nos fichiers, sauf R8 (le découpage du jour même réel,
  première séance de l'indice) : les autres sont des opérations fictives (R-732 partiel, dit dans la note).
⑩ EFFET — Dossiers temporaires, effacés.
⑪ TERMINAISON — Chaque relance est bornée à 600 s.
"""
import ast
import os
import shutil
import subprocess
import sys
import tempfile

SABOTAGES = {
    "S1_predicat_motif_seul": [("MODULE_JUGEMENT.py",
                                '    return o.get("motif") == _commun().MOTIF_FIN_DES_DONNEES or not o.get("date_sortie")\n',
                                '    return o.get("motif") == _commun().MOTIF_FIN_DES_DONNEES\n')],
    "S2_mise_a_part_recopiee": [("MODULE_JUGEMENT.py", "        (a_part if est_non_terminee(o) else terminees).append(o)",
                                 '        (a_part if o.get("motif") == "FIN_DES_DONNEES" else terminees).append(o)')],
    "S3_w2d_copie_locale": [("MODULE_PARCOURS_A_UN_JETON.py", "    return MODULE_JUGEMENT.est_non_terminee(o)",
                             '    return o.get("motif") == COMMUN.MOTIF_FIN_DES_DONNEES')],
    "S4_w2d_sans_latent": [("MODULE_PARCOURS_A_UN_JETON.py",
                            '            "resultat_latent_non_terminees_eur": a_part["resultat_latent_eur"],',
                            '            "resultat_latent_non_terminees_eur": 0.0,')],
    "S5_purge_recopiee": [("MODULE_JUGEMENT.py",
                           "        purgees = [o for o in avant if est_non_terminee(o) or not o[\"date_sortie\"] < debut_bande]",
                           "        purgees = [o for o in avant if o.get(\"motif\") == _commun().MOTIF_FIN_DES_DONNEES "
                           "or not o.get(\"date_sortie\") or not o[\"date_sortie\"] < debut_bande]")],
    "S6_resumer_motif_seul": [("JUGE_DES_STRATEGIES.py", "    ouvertes = [o for o in ops if _non_terminee(o)]\n"
                               "    ops = [o for o in ops if not _non_terminee(o)]",
                               "    ouvertes = [o for o in ops if o[\"motif\"] == MOTIF_FIN_DES_DONNEES]\n"
                               "    ops = [o for o in ops if o[\"motif\"] != MOTIF_FIN_DES_DONNEES]")],
    "S7_porte_jette_la_mise_a_part": [("JUGER_UNE_FICHE.py", "            jeu, _non_terminees = _operations_jugees(jeu)\n",
                                       "            _jeu_t, _non_terminees = _operations_jugees(jeu)\n")],
    "S8_operations_jugees_rend_tout": [("JUGER_UNE_FICHE.py", "    return dict(jeu, ops=ops), a_part",
                                        "    return dict(jeu), a_part")],
    "S9_affichage_sans_A1103": [("MODULE_JUGEMENT.py",
                                 'AFFICHAGE_EN_CAS_2 = ("gain_bat_zero", "observations_independantes")',
                                 'AFFICHAGE_EN_CAS_2 = ("gain_bat_zero",)')],
    "S10_jour_absent_calme": [("MODULE_QUAND_JOUER.py", "    return decoupage.types.get(date_signal, INCONNU) in ens",
                               '    return decoupage.types.get(date_signal, "HAUSSE_CALME") in ens')],
    "S11_sans_type_non_exclu": [("MODULE_CONTROLE_2_DU_HASARD.py",
                                 "        gardees = [o for o in (ops or []) if o.get(\"date_signal\") not in dates_sans_type]",
                                 "        gardees = list(ops or [])")],
    "S12_sans_type_non_compte": [("MODULE_CONTROLE_2_DU_HASARD.py",
                                  '            "operations_exclues_sans_type": exclues,',
                                  '            "operations_exclues_sans_type": 0 if exclues is not None else None,')],
    "S13_sans_achat_admis": [("MODULE_CONTROLE_2_DU_HASARD.py", '    if rendu.get("operations_sans_achat_tirable"):',
                              "    if False:")],
    "S14_k_du_registre": [("JUGER_UNE_FICHE.py", "        k = k_r if k_r is not None else \"INCONNU\"",
                           "        k = k_r if k_r is not None else (bilan[\"k\"] or {}).get(\"valeur\", \"INCONNU\")")],
    "S15_series_entete_non_confrontee": [("COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.py",
                                          "            if list(r.fieldnames or []) != list(CT.SERIE_D_UNE_VERSION_ENVOYEE):",
                                          "            if False:")],
    "S16_etalon_sans_signaux": [("MODULE_JUGEMENT.py", '                   "signaux_sans_type": sorted(set(signaux_sans_type))}',
                                 "                   }")],
}


def lancer(racine, sabotage):
    """Copie programmes/, applique un sabotage, relance ce fichier en « --cas » et rend (code, sortie).
    ① RÔLE — Un passage sur une copie, intacte (Z0) ou sabotée. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `racine` ;
    `sabotage` : un nom de SABOTAGES ou None. ④ CONDITIONS D'ENTRÉE — programmes/ existe. ⑤ SORTIE — DEUX valeurs : le
    code (2 si une cible est introuvable) et la sortie. [rend: 2] ⑥ TRAITEMENT — copier, remplacer (texte présent une
    fois exactement), relancer. ⑦ UNITÉ — — ⑧ POURQUOI — R-731 : le sabotage porte sur une COPIE. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — un dossier temporaire, effacé. ⑪ TERMINAISON — bornée à 600 s. [sort: non]"""
    tmp = tempfile.mkdtemp(prefix="I1_epreuve_")
    try:
        prog = os.path.join(tmp, "programmes")
        shutil.copytree(os.path.join(racine, "programmes"), prog, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for fichier, avant, apres in (SABOTAGES[sabotage] if sabotage else []):
            p = os.path.join(prog, fichier)
            s = open(p, encoding="utf-8").read()
            if s.count(avant) != 1:
                return 2, "CIBLE INTROUVABLE (%d fois) dans %s : %r" % (s.count(avant), fichier, avant[:70])
            open(p, "w", encoding="utf-8").write(s.replace(avant, apres))
        try:
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--cas", tmp],
                               capture_output=True, text=True, timeout=600)
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return 1, "DÉLAI DÉPASSÉ"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cas(racine):
    """Joue les cas sur la copie `racine` et rend le nombre de rouges.
    ① RÔLE — Les propriétés de la réunion I1. ② CONTEXTE D'APPEL — `main --cas`. ③ ENTRÉE — la racine de la copie.
    ④ CONDITIONS D'ENTRÉE — programmes/ sous la racine. ⑤ SORTIE — UNE valeur : le nombre de rouges. [rend: 1]
    ⑥ TRAITEMENT — R1 à R12, chacun isolé (une exception est un rouge). ⑦ UNITÉ — euros. ⑧ POURQUOI — R-731.
    ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — affiche ; un dossier temporaire pour R12. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    prog = os.path.join(racine, "programmes")
    sys.path.insert(0, prog)
    import MODULE_JUGEMENT as J
    import MODULE_PARCOURS_A_UN_JETON as P
    import JUGE_DES_STRATEGIES as JS
    import JUGER_UNE_FICHE as JUF
    import MODULE_QUAND_JOUER as QJ
    import MODULE_CONTROLE_2_DU_HASARD as C2
    import COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE as KR
    rouges = []

    def ok(nom, cond, detail=""):
        print("%s %s %s" % ("VERT " if cond else "ROUGE", nom, detail))
        if not cond:
            rouges.append(nom)

    def essai(nom, f):
        try:
            f()
        except Exception as ex:   # une exception est un rouge, jamais un silence (R-734)
            ok(nom + " (exception)", False, "%s: %s" % (type(ex).__name__, ex))

    FIN = "FIN_DES_DONNEES"
    tp_ok = {"motif": "OBJECTIF", "date_signal": "2030-01-07", "date_sortie": "2030-01-10", "net": 300.0}
    fin = {"motif": FIN, "date_signal": "2030-01-08", "date_sortie": "2030-01-20", "net": -500.0}
    sans_sortie = {"motif": "OBJECTIF", "date_signal": "2030-01-09", "date_sortie": "", "net": -200.0}
    horizon = {"motif": "HORIZON", "date_signal": "2030-01-06", "date_sortie": "2030-01-15", "net": 50.0}
    quatre = [tp_ok, fin, sans_sortie, horizon]
    attendu = [False, True, True, False]

    def r1():
        ok("R1 est_non_terminee : FIN_DES_DONNEES ou sortie absente, pas OBJECTIF ni HORIZON datés",
           [J.est_non_terminee(o) for o in quatre] == attendu, [J.est_non_terminee(o) for o in quatre])
    essai("R1", r1)

    def r2():
        t, a = J.mettre_a_part_les_non_terminees([dict(o) for o in quatre])
        ok("R2 mise à part : 2 à part, latent −700 €, 2 gardées", a["n"] == 2 and abs(a["resultat_latent_eur"] + 700) < 1e-9
           and len(t) == 2, a)
    essai("R2", r2)

    def r3():
        ok("R3 W2d : _non_terminee rend ce que rend la règle unique",
           [P._non_terminee(o) for o in quatre] == [J.est_non_terminee(o) for o in quatre] == attendu)
        r = P._resumer({"pris": [dict(tp_ok, valeur="AI"), dict(fin, valeur="OR"), dict(sans_sortie, valeur="MC")]}, 1.0)
        ok("R3b W2d _resumer : 2 non terminées, latent −700 €, gain 300 €",
           r["non_terminees"] == 2 and abs(r.get("resultat_latent_non_terminees_eur", 1) + 700) < 1e-9
           and abs(r["gain_net_eur"] - 300) < 1e-9, {k: r.get(k) for k in ("non_terminees", "gain_net_eur",
                                                                             "resultat_latent_non_terminees_eur")})
    essai("R3", r3)

    def r4():
        # R-708 sur tout programmes/ : AUCUNE comparaison au motif FIN_DES_DONNEES hors de la règle unique, sauf la plus
        # longue opération du juge (autre question, ⑨ ② d'est_non_terminee) et l'écrivain du motif (MODULE_POSITIONS).
        # Motif calibré : il trouve la règle unique elle-même (cas qui doit être trouvé).
        trouves = []
        for nom in sorted(os.listdir(prog)):
            if not nom.endswith(".py"):
                continue
            arbre = ast.parse(open(os.path.join(prog, nom), encoding="utf-8").read())
            for f in [n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)]:
                for n in ast.walk(f):
                    if isinstance(n, ast.Compare):
                        txt = ast.unparse(n)
                        if "MOTIF_FIN_DES_DONNEES" in txt or "'FIN_DES_DONNEES'" in txt or '"FIN_DES_DONNEES"' in txt:
                            trouves.append("%s:%s" % (nom, f.name))
        trouves = sorted(set(trouves))
        permis = {"MODULE_JUGEMENT.py:est_non_terminee", "JUGE_DES_STRATEGIES.py:duree_d_embargo_sans_horizon"}
        autres = [t for t in trouves if t not in permis and not t.startswith("MODULE_POSITIONS.py:")
                  and not t.startswith("EPREUVES")]
        ok("R4 calibrage : la règle unique est trouvée par le motif", "MODULE_JUGEMENT.py:est_non_terminee" in trouves,
           trouves[:6])
        ok("R4b R-708 : aucune autre reconnaissance d'une position non terminée", not autres, autres[:8])
    essai("R4", r4)

    def r5():
        r = JS.resumer([dict(tp_ok, valeur="AI"), dict(sans_sortie, valeur="MC")])
        ok("R5 resumer du juge : la position sans sortie est à part (1, −200 €)",
           r.get("fin_des_donnees") == {"n": 1, "net": -200.0} and r["n"] == 1, r.get("fin_des_donnees"))
    essai("R5", r5)

    def r6():
        jeu = {"ops": [dict(o) for o in quatre], "autre": 1}
        j2, a = JUF._operations_jugees(jeu)
        ok("R6 porte : _operations_jugees ne garde que les terminées", len(j2["ops"]) == 2 and a["n"] == 2
           and len(jeu["ops"]) == 4 and j2["autre"] == 1, (len(j2["ops"]), a["n"]))
        src = open(os.path.join(prog, "JUGER_UNE_FICHE.py"), encoding="utf-8").read()
        f = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "juger_une_fiche"][0]
        affect = [n for n in ast.walk(f) if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)
                  and ast.unparse(n.value.func) == "_operations_jugees"]
        lien = (len(affect) == 1 and isinstance(affect[0].targets[0], ast.Tuple)
                and ast.unparse(affect[0].targets[0].elts[0]) == "jeu" and ast.unparse(affect[0].value.args[0]) == "jeu")
        ligne = affect[0].lineno if affect else 10 ** 9
        appels = {}
        for n in ast.walk(f):
            if isinstance(n, ast.Call):
                appels.setdefault(ast.unparse(n.func), []).append(n.lineno)
        apres = [min(appels.get(x, [0])) for x in ("mesurer", "_hasard", "J.point_mort_des_operations")]
        ok("R6b porte : le jeu MIS À PART remplace le jeu (jeu = …) avant le Kelly, le hasard et le point mort",
           lien and all(ligne < x for x in apres), (lien, ligne, apres))
    essai("R6", r6)

    def r7():
        ok("R7 AFFICHAGE_EN_CAS_2 porte A-1103 (observations) et le gain > 0",
           set(J.AFFICHAGE_EN_CAS_2) == {"gain_bat_zero", "observations_independantes"}, J.AFFICHAGE_EN_CAS_2)
    essai("R7", r7)

    def r8():
        d = QJ.Decoupage("essai", {"2030-01-07": "HAUSSE_CALME"}, jour_meme=True)
        admis = [QJ.admis(q, d, "2030-01-08") for q in ("HAUSSE_CALME", "CALME", "HAUSSE", "HAUSSE+BAISSE")]
        ok("R8 jour ABSENT du découpage : jamais admis", admis == [False] * 4, admis)
        vrai = QJ.decoupage_par_defaut(os.path.dirname(prog)) if os.path.isdir(os.path.join(os.path.dirname(prog),
                                                                                             "donnees")) else None
        if vrai is not None:
            premier = min(vrai.types)
            ok("R8b vraie première séance de l'indice (%s, %s) non admise en HAUSSE_CALME" % (premier, vrai.types[premier]),
               vrai.types[premier] != "INCONNU" or not QJ.admis("HAUSSE_CALME", vrai, premier))
    essai("R8", r8)

    def r9():
        tirages = {"mode": "meme_type", "n_tirages": 99, "gains_des_tirages": [150.0 + i for i in range(99)],
                   "signaux_sans_type": ["2030-01-08"], "operations_sans_type": 1, "operations_sans_achat_tirable": 0,
                   "operations_par_type": {"HAUSSE_CALME": 1}, "achats_permis_par_type": {"HAUSSE_CALME": 5}}
        ops = [dict(tp_ok, net=100.0), dict(tp_ok, date_signal="2030-01-08", net=1.0e6)]
        r = C2.controle_2(ops, tirages, "70", largeur=0.2)
        ok("R9 A-1117 : l'opération sans type est EXCLUE (gain comparé 100 € → BLOQUE) et comptée (1)",
           r["etat"] == "BLOQUE" and r["operations_exclues_sans_type"] == 1, (r["etat"], r["operations_exclues_sans_type"],
                                                                                r["raison"]))
        r2 = C2.controle_2(ops, dict(tirages, operations_sans_achat_tirable=1), "70", largeur=0.2)
        ok("R9b une opération TYPÉE sans achat tirable rend INCONNU", r2["etat"] == "INCONNU", r2["raison"])
        t3 = dict(tirages)
        del t3["signaux_sans_type"]
        r3 = C2.controle_2(ops, t3, "70", largeur=0.2)
        ok("R9c rendu sans `signaux_sans_type` : INCONNU", r3["etat"] == "INCONNU", r3["raison"])
    essai("R9", r9)

    def r10():
        # l'étalon « meme_type » rend les dates des signaux sans type (la donnée qu'exige R9)
        class D:
            jour_meme, nom = True, "essai"
            types = {"2030-01-07": "HAUSSE_CALME", "2030-01-08": "INCONNU"}
        cours = {"AI": [{"date": "2030-01-07"}, {"date": "2030-01-08"}, {"date": "2030-01-09"}]}
        ops = [dict(tp_ok, valeur="AI"), dict(fin, valeur="AI")]
        h = J.etalon_hasard(ops, cours, ["AI"], None, None, None, None, mode="meme_type", n_tirages=5, graine=1,
                            entree=lambda v, j: {"net": 10.0}, admis=lambda v, j: True, periode=None, decoupage=D())
        ok("R10 étalon meme_type : signaux_sans_type = [2030-01-08], 1 sans type, 0 sans achat",
           h.get("signaux_sans_type") == ["2030-01-08"] and h.get("operations_sans_type") == 1
           and h.get("operations_sans_achat_tirable") == 0, {k: h.get(k) for k in ("signaux_sans_type",
                                                                                     "operations_sans_type")})
    essai("R10", r10)

    def r11():
        src = open(os.path.join(prog, "JUGER_UNE_FICHE.py"), encoding="utf-8").read()
        f = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "juger_une_fiche"][0]
        k_affecte = [ast.unparse(n.value) for n in ast.walk(f) if isinstance(n, ast.Assign)
                     and any(ast.unparse(t) == "k" for t in n.targets)]
        appelle = any(isinstance(n, ast.Call) and ast.unparse(n.func) == "KR.k_du_juge" for n in ast.walk(f))
        ok("R11 porte : k vient de k_du_juge seul (le compte du registre n'entre pas dans k)",
           appelle and len(k_affecte) == 1 and "bilan" not in k_affecte[0] and "k_r" in k_affecte[0], k_affecte)
    essai("R11", r11)

    def r12():
        tmp = tempfile.mkdtemp(prefix="I1_k_")
        try:
            os.makedirs(os.path.join(tmp, "programmes"))
            for nom in os.listdir(prog):
                if nom.endswith(".py"):
                    shutil.copy(os.path.join(prog, nom), os.path.join(tmp, "programmes", nom))
            k, d, r = KR.k_du_juge(tmp, "FICTIVE-I1", None)
            ok("R12 sans séries : k None, raison dite", k is None and "absentes" in r, r[:90])
            dossier = os.path.join(tmp, "donnees", "SERIES_DES_VERSIONS_ENVOYEES_AU_JUGE")
            os.makedirs(dossier)
            with open(os.path.join(dossier, "FICTIVE-I1.csv"), "w", encoding="utf-8") as f:
                f.write("version,date,gain\nV1,2030-01-07,1\n")
            k, d, r = KR.k_du_juge(tmp, "FICTIVE-I1", None)
            ok("R12b en-tête hors contrat : k None", k is None and "en-tête" in r, r[:90])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    essai("R12", r12)

    print("== %d rouge(s)" % len(rouges))
    return len(rouges)


def main():
    """Point d'entrée : Z0, puis les sabotages demandés.
    ① RÔLE — Orchestrer. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — sys.argv. ④ — ⑤ SORTIE — par
    sys.exit. [rend: rien] ⑥ « --cas » : jouer ; sinon Z0 puis sabotages. ⑦ — ⑧ R-731, R-734. ⑨ — ⑩ affiche.
    ⑪ TERMINAISON — sort par sys.exit. [sort: oui — code de sortie]"""
    a = sys.argv[1:]
    if a[:1] == ["--cas"]:
        sys.exit(1 if cas(a[1]) else 0)
    if not a:
        print("usage : <racine> [--saboter | <sabotage>]")
        sys.exit(2)
    racine = os.path.abspath(a[0])
    if not os.path.isdir(os.path.join(racine, "programmes")):
        print("DONNÉE MANQUANTE : programmes/")
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
