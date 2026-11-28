#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU CONTRÔLE 2 « MIEUX QUE LE HASARD » — Sam 28-11-2026 (Paris), lot W2a du plan R505. SIMULATION UNIQUEMENT.

LE SENS EN TÊTE — Ces épreuves vérifient que le contrôle 2 de la loi R-505 v2 tire le hasard dans le MÊME TYPE DE
MARCHÉ MESURÉ LE JOUR MÊME (A-1072, A-1105), avec deux barres (A-1081 : filtre large sur les 70 %, 0,05 ÷ k sur les
30 %, A-1070, A-1095 corrigée), et affiche les types sans opération. Chaque propriété a son épreuve ; chaque épreuve
est SABOTÉE (le programme fausse une copie du code et exige que l'épreuve rougisse) : une épreuve qui reste verte
quand on retire ce qu'elle teste est une décoration.

USAGE : python3 -B tests/EPREUVES_DU_CONTROLE_2_DU_HASARD_Sam_28-11-2026.py <racine> [--sans-sabotage] [--cas-reel]
  --cas-reel : rejoue en plus une stratégie FICTIVE sur les VRAIS cours de 2024-2026 et le VRAI découpage du jour
  même (aucun regard sur 2000-2023 : aucune opération avant 2024).
CODE : 0 si tout est vert et chaque sabotage rougit ; 1 sinon ; 2 si l'épreuve n'a pas pu tourner (R-734).

① RÔLE — Éprouver `MODULE_JUGEMENT.etalon_hasard` en mode « meme_type » et `MODULE_CONTROLE_2_DU_HASARD`.
② CONTEXTE D'APPEL — À la main, et sur GitHub (ENVOYER_LES_EPREUVES_SUR_GITHUB.py) pour le cas réel.
③ ENTRÉE — La racine d'un dépôt ou d'une copie ; les deux options.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/ ; pour --cas-reel, donnees/cours_maitre.csv et l'indice.
⑤ SORTIE — Le code ; à l'écran une ligne par épreuve et par sabotage, un verdict.
  [rend: 1]
⑥ TRAITEMENT — ① les épreuves sur un jeu fabriqué · ② chaque sabotage sur une copie temporaire de programmes/, dans un
  sous-processus, qui doit rougir · ③ le cas réel si demandé.
⑦ UNITÉ — Gains en EUROS ; p et barres des probabilités.
⑧ POURQUOI — R-731, R-732 (un cas d'une vraie ligne), R-734.
⑨ CE QUI CLOCHE — Le cas réel lit tout le fichier des cours (les prix de 2000-2023 sont lus, jamais une stratégie n'y
  est jouée) ; sa durée locale n'est pas garantie sous 2 minutes.
⑩ EFFET — Écrit et efface un dossier temporaire.
⑪ TERMINAISON — Rend la main ; chaque sous-processus est borné à 300 s.
  [sort: oui]
"""
import os
import shutil
import subprocess
import sys
import tempfile

ECHECS = []


def ok(nom, cond, detail=""):
    """Note une épreuve. ①affiche ②— ③nom, condition, détail ④— ⑤aucune ⑥ajoute aux échecs si faux ⑦— ⑧trace
    ⑨— ⑩écrit à l'écran ⑪rend la main. [rend: 0] [sort: non]"""
    print(("VERT  " if cond else "ROUGE ") + nom + ((" — " + detail) if detail else ""))
    if not cond:
        ECHECS.append(nom)


def jeu_fabrique(QJ):
    """Deux valeurs, 60 séances ; types alternés par blocs de 10 ; gain d'un achat = +1000 en HAUSSE_CALME, −1000
    ailleurs. ①fabriquer ②epreuves ③module QJ ④— ⑤cinq valeurs ⑥— ⑦euros ⑧vérité connue ⑨— ⑩— ⑪rend.
    [rend: 5] [sort: non]"""
    import datetime
    d0 = datetime.date(2024, 1, 1)
    dates = [(d0 + datetime.timedelta(days=i)).isoformat() for i in range(60)]
    ordre = ["HAUSSE_CALME", "BAISSE_AGITEE", "BAISSE_CALME", "HAUSSE_AGITEE", "HAUSSE_CALME", "BAISSE_CALME"]
    types = {d: ordre[i // 10] for i, d in enumerate(dates)}
    types[dates[25]] = "INCONNU"
    cours = {v: [{"date": d, "open": 10.0, "high": 10.0, "low": 10.0, "close": 10.0} for d in dates] for v in "AB"}
    tires = []

    def entree(v, j):
        d_sig = cours[v][j - 1]["date"]
        tires.append(types[d_sig])
        # (28-11-2026, lot I1FIX, W2bFIX-1) une opération TERMINÉE porte son motif et sa sortie : l'étalon « meme_type »
        # sort désormais des sommes tout achat tiré non terminé (`est_non_terminee` : motif FIN_DES_DONNEES ou sortie
        # absente) ; la fausse mécanique rendait une opération sans sortie, qui se lirait « non terminée »
        return {"net": 1000.0 if types[d_sig] == "HAUSSE_CALME" else -1000.0, "motif": "OBJECTIF",
                "date_sortie": cours[v][j]["date"]}

    dec = QJ.Decoupage("jour_meme_fabrique", types, jour_meme=True)
    return cours, dates, entree, dec, tires


def epreuves(racine):
    """Les épreuves sur le jeu fabriqué. ①éprouver ②main ③racine ④programmes/ ⑤aucune ⑥voir chaque `ok` ⑦—
    ⑧une épreuve par propriété ⑨— ⑩écrit ⑪rend. [rend: 0] [sort: non]"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import MODULE_JUGEMENT as J
    import MODULE_QUAND_JOUER as QJ
    import MODULE_CONTROLE_2_DU_HASARD as C
    cours, dates, entree, dec, tires = jeu_fabrique(QJ)
    admis = lambda v, j: True  # noqa: E731
    # ops : 4 en HAUSSE_CALME (dates 2..5), 2 en BAISSE_AGITEE (dates 12, 13)
    ops = [{"valeur": "A", "date_signal": dates[i], "net": 1000.0} for i in (2, 3, 4, 5)] + \
          [{"valeur": "B", "date_signal": dates[i], "net": -1000.0} for i in (12, 13)]
    # P1 — chaque tirage reproduit EXACTEMENT les types des vrais achats (le tirage reste dans le type)
    del tires[:]
    r = C.tirer_le_jour_au_hasard(ops, cours, ["A", "B"], entree, admis, None, dec, 50)
    attendu = sorted(dec.types[o["date_signal"]] for o in ops)
    par_tirage = [sorted(tires[i:i + len(ops)]) for i in range(0, len(tires), len(ops))]
    ok("P1 tirage dans le même type du jour même", len(par_tirage) == 50 and all(t == attendu for t in par_tirage),
       "types attendus %s" % attendu)
    # P1b — donc chaque tirage fait EXACTEMENT le gain de la version : p = 1 (le hasard du même type l'égale)
    p, n, _ = J.p_du_hasard(sum(o["net"] for o in ops), r)
    ok("P1b gain du hasard du même type = gain de la version", p == 1.0 and n == 50, "p=%r n=%r" % (p, n))
    # P2 — un découpage fait APRÈS COUP est refusé, et l'absence de découpage aussi
    apres = QJ.Decoupage("apres_coup", dec.types, jour_meme=False)
    for nom, d in (("après coup", apres), ("absent", None)):
        try:
            C.tirer_le_jour_au_hasard(ops, cours, ["A", "B"], entree, admis, None, d, 5)
            ok("P2 découpage %s refusé" % nom, False, "aucun refus")
        except ValueError:
            ok("P2 découpage %s refusé" % nom, True)
    # P3 — barre stricte des 30 % : 0,05 ÷ k lu à la table ; tirages insuffisants → INCONNU
    table = {"seuil_du_hasard": {"valeur": "0,05 ÷ k"}}
    gagnant = [dict(o, net=5000.0) for o in ops]
    r20 = C.tirer_le_jour_au_hasard(gagnant, cours, ["A", "B"], entree, admis, None, dec, 20)
    c = C.controle_2(gagnant, r20, "30", k=10, table=table)
    ok("P3a 20 tirages sous 0,05÷10 → INCONNU", c["etat"] == "INCONNU" and abs(c["seuil"] - 0.005) < 1e-12, str(c["etat"]))
    n_ok = C.nombre_de_tirages(0.05 / 10)
    rN = C.tirer_le_jour_au_hasard(gagnant, cours, ["A", "B"], entree, admis, None, dec, n_ok)
    c = C.controle_2(gagnant, rN, "30", k=10, table=table)
    ok("P3b version qui bat tous les tirages → PASSE", c["etat"] == "PASSE", "%s p=%r n=%d" % (c["etat"], c["valeur"], n_ok))
    c = C.controle_2(ops, C.tirer_le_jour_au_hasard(ops, cours, ["A", "B"], entree, admis, None, dec, n_ok), "30",
                     k=10, table=table)
    ok("P3c version égale au hasard du même type → BLOQUE", c["etat"] == "BLOQUE", "%s p=%r" % (c["etat"], c["valeur"]))
    c = C.controle_2(gagnant, rN, "30", k=None, table=table)
    ok("P3d k absent → INCONNU", c["etat"] == "INCONNU", c["raison"])
    # P4 — filtre large des 70 % : sans largeur → INCONNU ; avec une largeur passée → PASSE / BLOQUE
    larg, raison = C.largeur_du_filtre_large(racine)
    c = C.controle_2(gagnant, rN, "70", largeur=larg, raison_largeur=raison)
    ok("P4a filtre large non fixé → INCONNU", larg is None and c["etat"] == "INCONNU", c["raison"][:70])
    ok("P4b filtre large 0,5 : gagnante → PASSE", C.controle_2(gagnant, rN, "70", largeur=0.5)["etat"] == "PASSE")
    ok("P4c filtre large 0,5 : égale au hasard → BLOQUE",
       C.controle_2(ops, C.tirer_le_jour_au_hasard(ops, cours, ["A", "B"], entree, admis, None, dec, 30), "70",
                    largeur=0.5)["etat"] == "BLOQUE")
    # P5 — les types sans opération sont affichés
    ok("P5 types sans opération affichés", c is not None and
       C.types_sans_operation(r) == ["HAUSSE_AGITEE", "BAISSE_CALME"], str(C.types_sans_operation(r)))
    # P6 — RENVERSÉ LE 28-11-2026 (réunion I1, A-1117) : une opération dont le jour n'a pas de type mesuré le jour même
    # est EXCLUE du contrôle et comptée ; le contrôle rend le même p que sans elle (avant : INCONNU, DÉL-D26)
    ops_inc = ops + [{"valeur": "A", "date_signal": dates[25], "net": 1000.0}]
    r6 = C.tirer_le_jour_au_hasard(ops_inc, cours, ["A", "B"], entree, admis, None, dec, n_ok)
    c = C.controle_2(ops_inc, r6, "30", k=10, table=table)
    c_ref = C.controle_2(ops, C.tirer_le_jour_au_hasard(ops, cours, ["A", "B"], entree, admis, None, dec, n_ok), "30",
                         k=10, table=table)
    ok("P6 opération sans type → EXCLUE et comptée (A-1117), même p que sans elle",
       r6.get("operations_sans_type") == 1 and c["operations_exclues_sans_type"] == 1 and c["etat"] != "INCONNU"
       and c["valeur"] == c_ref["valeur"], str((c["etat"], c["valeur"], c_ref["valeur"], c["raison"][:60])))
    # P7 — un hasard tiré hors du type (mode « date ») n'est pas accepté par le contrôle
    rd = J.etalon_hasard(gagnant, cours, ["A", "B"], None, None, None, None, mode="date", n_tirages=n_ok,
                         entree=entree, admis=admis)
    # (28-11-2026, réunion I1) le rendu reçoit les cases d'A-1117 vides : seul le contrôle du MODE peut alors le refuser
    # (28-11-2026, lot I1FIX) et la case d'A-1118 (b), vide elle aussi
    rd_complet = dict(rd, signaux_sans_type=[], operations_sans_achat_tirable=0, signaux_absents_du_decoupage=[])
    ok("P7 hasard hors du type refusé par le contrôle", C.controle_2(gagnant, rd, "30", k=10, table=table)["etat"]
       == "INCONNU" and C.controle_2(gagnant, rd_complet, "30", k=10, table=table)["etat"] == "INCONNU")
    # P8 — les autres modes gardent leur forme (13 cases) : rien n'a changé pour le juge actuel
    rv = J.etalon_hasard(ops, cours, ["A", "B"], None, None, None, None, mode="valeur", n_tirages=5,
                         entree=entree, admis=admis)
    ok("P8 mode « valeur » inchangé (13 cases)", len(rv) == 13 and "operations_par_type" not in rv, str(len(rv)))


SABOTAGES = [
    ("S1 refus de l'après coup retiré", "programmes/MODULE_JUGEMENT.py",
     'getattr(decoupage, "jour_meme", None) is not True', 'False'),
    # (un sabotage « retirer « decoupage is None » » restait vert : la condition suivante refuse aussi None —
    #  redondance du code, pas un trou de l'épreuve ; constaté le 28-11-2026, sabotage retiré)
    ("S2 tirage hors du type", "programmes/MODULE_JUGEMENT.py",
     'cands = par_type.get(types_du_jour.get(o["date_signal"]), [])',
     'cands = [x for _c in par_type.values() for x in _c]'),
    ("S3 garde des tirages insuffisants retirée", "programmes/MODULE_CONTROLE_2_DU_HASARD.py",
     'if 1.0 / n_t >= seuil:', 'if False:'),
    ("S3b barre stricte sans ÷ k", "programmes/MODULE_CONTROLE_2_DU_HASARD.py",
     'J.seuil_de_la_loi(table, CLE_DU_SEUIL_STRICT, k)', '(0.05 if k else None, "")'),
    ("S4 types sans opération tus", "programmes/MODULE_CONTROLE_2_DU_HASARD.py",
     'return [t for t in QJ.TYPES_DE_MARCHE if not par.get(t)]', 'return []'),
    ("S5 opérations sans type acceptées", "programmes/MODULE_CONTROLE_2_DU_HASARD.py",
     'gardees = [o for o in (ops or []) if o.get("date_signal") not in dates_sans_type]', 'gardees = list(ops or [])'),
    ("S6 mode du hasard non vérifié", "programmes/MODULE_CONTROLE_2_DU_HASARD.py",
     '(rendu.get("mode") is not None and rendu.get("mode") != "meme_type")', 'False'),
    ("S7 filtre large inventé dans le code", "programmes/MODULE_CONTROLE_2_DU_HASARD.py",
     'if not isinstance(table, dict) or CLE_DU_FILTRE_LARGE not in table:', 'if False:\n        pass\n    return 0.5, ""\n    if True:'),
]


def saboter(racine):
    """Chaque sabotage sur une copie de programmes/, dans un sous-processus : il doit rougir. ①éprouver les épreuves
    ②main ③racine ④— ⑤aucune ⑥copie, remplacement unique, relance, code attendu 1 ⑦— ⑧une épreuve qui reste verte
    est une décoration ⑨— ⑩écrit/efface un dossier temporaire ⑪borné à 300 s. [rend: 0] [sort: non]"""
    for nom, fichier, avant, apres in SABOTAGES:
        tmp = tempfile.mkdtemp(prefix="w2a_sabo_")
        try:
            shutil.copytree(os.path.join(racine, "programmes"), os.path.join(tmp, "programmes"),
                            ignore=shutil.ignore_patterns("__pycache__"))
            for sous in ("donnees",):
                src = os.path.join(racine, sous)
                if os.path.isdir(src):
                    os.symlink(src, os.path.join(tmp, sous))
            p = os.path.join(tmp, fichier)
            t = open(p, encoding="utf-8").read()
            if t.count(avant) != 1:
                ok(nom + " (motif introuvable)", False, "%d occurrence(s)" % t.count(avant))
                continue
            open(p, "w", encoding="utf-8").write(t.replace(avant, apres))
            q = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), tmp, "--sans-sabotage"],
                               capture_output=True, text=True, timeout=300)
            rouges = [l for l in q.stdout.splitlines() if l.startswith("ROUGE")]
            ok(nom + " → l'épreuve rougit", q.returncode == 1 and bool(rouges),
               "code %d ; %s" % (q.returncode, rouges[0][6:60] if rouges else "aucun rouge"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def cas_reel(racine):
    """Stratégie FICTIVE sur les vrais cours 2024-2026 et le vrai découpage du jour même. ①cas réel R-732 ②main
    ③racine ④cours et indice ⑤aucune ⑥jouer une fiche fictive (achat toutes les 15 séances de trois valeurs) par la
    mécanique du juge, tirer le hasard du même type, afficher ⑦euros ⑧R-732 ⑨période bornée à l'indice ⑩lit
    ⑪rend. [rend: 0] [sort: non]"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import JUGE_DES_STRATEGIES as JS
    import MODULE_QUAND_JOUER as QJ
    import MODULE_CONTROLE_2_DU_HASARD as C
    mnemo = JS.table_mnemoniques(JS.trouver(racine, "REFERENTIEL_VALEURS"))
    f_cours = JS.fichiers_de_cours(racine)[0]
    cours, lecture = JS.lire_par_le_lecteur(racine, os.path.relpath(f_cours, racine), mnemo)
    mod_pos = JS.charger_module(JS.trouver(racine, "MODULE_POSITIONS.py"), "pos_w2a")
    cal = JS.calendrier_pour_la_vente(cours, lecture, mod_pos)
    dec = QJ.decoupage_par_defaut(racine)
    fin_indice = max(dec.types)
    periode = ("2024-01-02", fin_indice)
    tp, sl, h = 0.04, 0.025, 10
    univ = sorted(cours)[:3]
    entree = lambda v, j: JS.jouer_une_entree(v, cours[v], j, tp, sl, h, mod_pos, lecture, None, seances=cal)  # noqa
    admis = lambda v, j: JS.achat_admis(v, cours[v], j, lecture)  # noqa: E731
    ops = []
    for v in univ:
        s = cours[v]
        for j in range(1, len(s)):
            if periode[0] <= s[j - 1]["date"] <= periode[1] and j % 15 == 0 and admis(v, j):
                o = entree(v, j)
                if o is not None:
                    ops.append(dict(o, valeur=v, date_signal=s[j - 1]["date"]))
    ok("R0 cas réel : opérations jouées toutes après 2023", bool(ops) and min(o["date_signal"] for o in ops) >= "2024",
       "%d opérations, %s → %s, valeurs %s" % (len(ops), min(o["date_signal"] for o in ops) if ops else "-",
                                              max(o["date_signal"] for o in ops) if ops else "-", univ))
    k = 3
    n = C.nombre_de_tirages(0.05 / k)
    r = C.tirer_le_jour_au_hasard(ops, cours, univ, entree, admis, periode, dec, n)
    c30 = C.controle_2(ops, r, "30", k=k, table={"seuil_du_hasard": {"valeur": "0,05 ÷ k"}})
    larg, rl = C.largeur_du_filtre_large(racine)
    c70 = C.controle_2(ops, r, "70", largeur=larg, raison_largeur=rl)
    print("CAS RÉEL : %d tirages ; opérations par type %s ; achats tirables %s ; sans type %s ; types sans opération %s"
          % (r.get("n_tirages", 0), r.get("operations_par_type"), r.get("achats_permis_par_type"),
             r.get("operations_sans_type"), c30["types_sans_operation"]))
    print("CAS RÉEL : 30 %% → %s p=%r barre=%r ; 70 %% → %s (%s)" % (c30["etat"], c30["valeur"], c30["seuil"],
                                                                  c70["etat"], c70["raison"][:60]))
    ok("R1 cas réel : le contrôle rend un état", c30["etat"] in ("PASSE", "BLOQUE", "INCONNU") and r.get("n_tirages") == n)
    ok("R2 cas réel : chaque opération a son type du jour même", r.get("operations_sans_type") == 0,
       str(r.get("operations_sans_type")))


def main(argv):
    """①lancer ②main ③argv ④racine ⑤code ⑥épreuves, sabotages, cas réel ⑦— ⑧R-734 ⑨— ⑩écrit ⑪sort.
    [rend: 1] [sort: oui]"""
    if len(argv) < 2 or not os.path.isdir(os.path.join(argv[1], "programmes")):
        print("usage : <racine> [--sans-sabotage] [--cas-reel]")
        return 2
    racine = os.path.abspath(argv[1])
    try:
        epreuves(racine)
        if "--sans-sabotage" not in argv:
            saboter(racine)
        if "--cas-reel" in argv:
            cas_reel(racine)
    except Exception as ex:  # R-734 : une épreuve qui n'a pas pu tourner n'est pas verte
        print("ROUGE épreuve interrompue : %s: %s" % (type(ex).__name__, ex))
        return 1 if "--sans-sabotage" in argv else 2
    print("VERDICT : %s (%d rouge(s))" % ("VERT" if not ECHECS else "ROUGE", len(ECHECS)))
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
