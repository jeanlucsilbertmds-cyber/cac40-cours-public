#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_ENCHAINER_LA_MOULINETTE_Jeu_19-11-2026.py — Jeu 19-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Éprouve la porte de la chaîne (A-919) : programmes/VERIFIER_LA_CHAINE.py, appelé par le JUGE lui-même,
l'enchaîneur programmes/ENCHAINER_LA_MOULINETTE.py, et les tranches de JOUER_LES_VERSIONS.py. Un passage complet ⓪→④
sur une copie jetable (C5E10-OBS-V1 E01, période de sa fiche) ; puis des SABOTAGES qui doivent rougir pour LEUR raison
(code ET message) et redevenir verts une fois retirés ; puis une CONTRE-ÉPREUVE : la porte neutralisée, les sabotages
de la porte doivent cesser de rougir, sinon ces épreuves ne prouvent rien.

① RÔLE — Prouver que la chaîne tourne et que le juge refuse une version sans ① ② ③.
② CONTEXTE D'APPEL — À la main, une phase par appel (chacune sous 10 minutes) :
  `python3 -B tests/EPREUVES_ENCHAINER_LA_MOULINETTE_Jeu_19-11-2026.py <source> <vrai_depot> <travail> <phase>`,
  phases dans l'ordre : avant · passage · sabotages · sabotages2 · sabotages3 · contre · contre2 · contre3 · bilan
  (les sabotages S11 à S17, ajoutés après la relecture du 19-11-2026, forment le lot 2 ; S18 à S21, ajoutés au tour 3
  — superviseur R-759 du 19-11-2026 —, le lot 3 : un lot par appel, chacun sous 10 minutes).
③ ENTRÉE — `<source>` : le worktree copié ; `<vrai_depot>` : le dépôt principal, jamais modifié ; `<travail>` : un
  dossier sous /dev/shm.
④ CONDITIONS D'ENTRÉE — `<travail>/depot` n'existe pas à la phase `avant`.
⑤ SORTIE — UNE valeur, le code : 0 tout tient · 1 une épreuve rougit · 2 une épreuve n'a pas pu tourner (R-734).
⑥ TRAITEMENT — voir chaque phase.
⑦ UNITÉ — secondes.
⑧ POURQUOI — R-731 : épreuves avec sabotages ; un jeu d'épreuves se sabote contre sa propre correction.
⑨ CE QUI CLOCHE — ① La version jugée au passage est la première ligne du fichier trié : choix d'ÉPREUVE, pas une
  règle (A-775 non décidée). ② Les sabotages ne rejouent pas ② (trop long) : ils agissent sur le dossier de la chaîne
  déjà fait, restauré ensuite depuis un instantané. ③ Le juge lancé sans fiche visée (toutes les fiches) n'est pas
  éprouvé. ④ L'empreinte du vrai dépôt exclut .git, etudes/, archives/, prompts_taches/ et PILOTE_SOCLE* (exclusion
  déclarée, `ignorer` de l'épreuve du 19-11). ⑤ S17 n'est pas un sabotage qui rougit : il MONTRE, vert, le trou assumé
  d'A-921 (une fiche sans la marque est jugée) ; il rougirait le jour où ce trou serait bouché, et devrait alors
  changer de sens. ⑥ La contre-épreuve neutralise `porte_du_juge` entière : les sabotages qui visent l'enchaîneur
  seul (S0b, S4m, S15) et S9, S17 n'y sont pas rejoués. ⑦ LOT 3 : chaque sabotage porte SA contre-épreuve, un geste
  qui défait SA correction dans la copie (« contre3 ») ; il doit alors cesser de rougir, PAR LE CODE AUSSI (le code
  rendu diffère du code attendu) — M2 du relecteur du 19-11-2026 : S12 rougissait par le message seul. S12 vise donc
  maintenant un signal qui passe la porte 0 (celui d'IND-001-RETEST), et « contre2 » exige aussi son code. ⑧ S20b
  (courtage 0.0015 → 0.015 sous le même nom) : sa contre-épreuve ne juge que le message — comparaison neutralisée, la
  fiche est jouée puis mise EN ÉCHEC au point mort, code 1, le même code pour une autre raison.
⑩ EFFET — Écrit sous <travail> seulement.
⑪ TERMINAISON — Chaque programme lancé est borné à 600 s. [sort: oui — code]
"""
import csv
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("EPREUVE_C5", os.path.join(ICI, "EPREUVE_DE_LA_CHAINE_C5_SUR_COPIE_Jeu_19-11-2026.py"))
E = importlib.util.module_from_spec(_spec)
_argv, sys.argv = sys.argv, sys.argv[:1]
_spec.loader.exec_module(E)          # ignorer, empreinte_du_depot, regards_du_depot, registres_d_essais (R-708)
sys.argv = _argv

SID, ESSAI, NB = "C5E10-OBS-V1", "E01", 5
ENCH, VERIF, JUGE = "programmes/ENCHAINER_LA_MOULINETTE.py", "programmes/VERIFIER_LA_CHAINE.py", \
    "programmes/JUGE_DES_STRATEGIES.py"
CH = "CHAINE_%s_%s" % (SID, ESSAI)
TRI = "e3/TRI_%s_%s.csv" % (SID, ESSAI)


def py(copie, *args):
    """Lance `python3 -B` dans la copie ; rend (code, sortie). Borné à 600 s. [rend: 2]"""
    p = subprocess.run([sys.executable, "-B"] + list(args), cwd=copie, capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout + p.stderr


def ench(copie, *args):
    return py(copie, ENCH, copie, SID, ESSAI, *args)


def empreintes(source, vrai):
    """HEAD + état + arbre (sans ce que `ignorer` écarte) + regards, des deux dépôts. [rend: 1]"""
    r = {}
    for nom, d in (("source", source), ("vrai", vrai)):
        E.RACINE = d
        git = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout
        st = subprocess.run(["git", "-C", d, "status", "--porcelain"], capture_output=True, text=True).stdout
        r[nom] = {"head_status": hashlib.sha256((git + st).encode()).hexdigest()[:16],
                  "arbre": E.empreinte_du_depot(d)[0], "regards": E.regards_du_depot(d)}
    return r


def journal(ch):
    with open(os.path.join(ch, "JOURNAL_DE_LA_CHAINE.csv"), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def reecrire_journal(ch, lignes):
    with open(os.path.join(ch, "JOURNAL_DE_LA_CHAINE.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["etape", "fichier", "sha256", "ecrit_le"], lineterminator="\n")
        w.writeheader()
        w.writerows(lignes)


def sans(prefixe):
    return lambda ch, c: reecrire_journal(ch, [l for l in journal(ch) if not l["etape"].startswith(prefixe)])


def vider(ch, c):
    shutil.rmtree(ch)
    os.makedirs(ch)


def retirer(rel):
    return lambda ch, c: os.remove(os.path.join(ch, rel))


def modifier(rel, avant, apres):
    def f(ch, c):
        p = os.path.join(ch, rel)
        s = open(p, encoding="utf-8").read()
        assert avant in s, (rel, avant)
        open(p, "w", encoding="utf-8").write(s.replace(avant, apres, 1))
    return f


def non_valides(ch, c):
    """tp perd sa mention de validation, et son témoin est remis à jour : seule la validation manque."""
    rel = "valide/VARIABLES_DE_DECLINAISON_%s_%s.csv" % (SID, ESSAI)
    modifier(rel, "Jean-Luc le 08-10-2026,2026-10-08", "à valider,2026-10-08")(ch, c)
    j = journal(ch)
    for l in j:
        if l["etape"] == "0-variables-validees":
            l["sha256"] = hashlib.sha256(open(os.path.join(ch, rel), "rb").read()).hexdigest()
    reecrire_journal(ch, j)


def tri_illisible(ch, c):
    os.remove(os.path.join(ch, TRI))
    os.makedirs(os.path.join(ch, TRI))


def tranche_perdue_avant_assemblage(ch, c):
    """La tranche 2 n'a jamais été jouée : son témoin et l'assemblage retirés (M1 : rougir par les manquantes)."""
    os.remove(os.path.join(ch, "e2", "RESULTATS_%s_%s.csv" % (SID, ESSAI)))
    reecrire_journal(ch, [l for l in journal(ch) if l["etape"] not in ("2-tranche-2", "2-assembler", "3-trier")])


GOLDEN = "gouvernance/golden_tests_Sam_01-08-2026_20h19.json"


def golden_casse(ch, c):
    """Le juge échoue : le golden de la copie rendu illisible (mesuré : JSONDecodeError, code 1). Retirer un module
    ne suffisait pas : le juge le retrouvait par motif (mesuré : code 0)."""
    shutil.copyfile(os.path.join(c, GOLDEN), os.path.join(c, GOLDEN + ".sauve"))
    open(os.path.join(c, GOLDEN), "w").write("{\n")


def module_remis(c):
    if os.path.exists(os.path.join(c, GOLDEN + ".sauve")):
        os.replace(os.path.join(c, GOLDEN + ".sauve"), os.path.join(c, GOLDEN))


sys.path.insert(0, os.path.join(os.path.dirname(ICI), "programmes"))
import CONTRATS_DES_FICHIERS as _C  # noqa: E402  le registre est nommé au contrat (R-708)
REG = _C.REGISTRE_DES_STRATEGIES
NOUVEAUX = ("S11", "S12", "S13", "S14", "S15", "S16", "S17")     # le lot 2 (relecture du 19-11-2026)
LOT3 = ("S18", "S19", "S20", "S20b", "S21")                        # le lot 3 (superviseur R-759, tour 3)
# contre-épreuve : le code rendu doit AUSSI différer du code attendu (M2) — sauf S20b : comparaison neutralisée, la
# fiche est jouée sous le taux changé puis mise EN ÉCHEC au point mort, code 1 pour une AUTRE raison (mesuré 19-11-2026)
CODE_AUSSI = ("S12", "S18", "S19", "S20", "S21")
SAUVES = []                       # fichiers de programme ou de données de la copie modifiés par un geste du lot 3


def lot_de(nom):
    """1, 2 ou 3. [rend: 1]"""
    return 3 if nom.split()[0] in LOT3 else 2 if nom.split()[0] in NOUVEAUX else 1


def fichier_change(rel, avant, apres):
    """Geste : remplace une fois `avant` par `apres` dans un fichier de la copie, après l'avoir sauvé ; `fichiers_remis`
    le remet. Un texte absent arrête l'épreuve (AssertionError). [rend: 1]"""
    def f(ch, c):
        p = os.path.join(c, rel)
        s = open(p, encoding="utf-8").read()
        assert s.count(avant) == 1, (rel, avant)
        shutil.copyfile(p, p + ".sauve_epreuve")
        SAUVES.append(p)
        open(p, "w", encoding="utf-8").write(s.replace(avant, apres, 1))
    return f


def volume_change(rel, debut):
    """Geste : ajoute 1 au volume de LA ligne qui commence par `debut`, lue dans la copie au moment de l'épreuve.
    Pourquoi : la ligne reste une vraie ligne du fichier (R-732) sans qu'aucun chiffre de donnees/ soit écrit dans
    l'épreuve, que FABRIQUER_LE_CIRCUIT_PUBLIC refuse de publier (A-555, A-662). Une ligne absente ou en double
    arrête l'épreuve (AssertionError). [rend: 1]"""
    def f(ch, c):
        p = os.path.join(c, rel)
        lignes = [l for l in open(p, encoding="utf-8").read().splitlines() if l.startswith(debut)]
        assert len(lignes) == 1, (rel, debut, len(lignes))
        champs = lignes[0].split(",")
        champs[6] = str(int(champs[6]) + 1)          # colonne 7 : le volume (CONTRATS_DES_FICHIERS, cours_maitre)
        fichier_change(rel, lignes[0], ",".join(champs))(ch, c)
    return f


def fichiers_remis():
    while SAUVES:
        p = SAUVES.pop()
        os.replace(p + ".sauve_epreuve", p)


def deux_gestes(a, b):
    return lambda ch, c: (a(ch, c), b(ch, c))


# LES CONTRE-ÉPREUVES DU LOT 3 : (fichier, texte de la correction, texte qui la défait) — un geste par sabotage.
CONTRE3 = {
    "S18": ("programmes/VERIFIER_LA_CHAINE.py", "    if len(trouvees) != 1:\n", "    if not trouvees:\n"),
    "S19": ("programmes/VERIFIER_LA_CHAINE.py",
            "    case, marque = norme(fiche.get(C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE)), norme(C.MARQUE_DE_MOULINETTE)",
            "    case, marque = (fiche.get(C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE) or \"\").strip(), C.MARQUE_DE_MOULINETTE"),
    # S20 : la porte ne reçoit plus le barème du juge (nom et contenu) — sinon le contenu, gardé derrière le nom, rougit
    "S20": ("programmes/VERIFIER_LA_CHAINE.py", "(nom, JOUER.empreinte_du_bareme(mod_pos, nom)))", "None)"),
    "S20b": ("programmes/VERIFIER_LA_CHAINE.py",
             "elif bareme is not None and j[\"empreinte_du_bareme\"] != bareme[1]:", "elif False:"),
    "S21": ("programmes/VERIFIER_LA_CHAINE.py", "if vu != j[\"empreinte_des_cours\"]:", "if False:"),
}


def fiche_ajoutee(source, **changes):
    """Geste : ajoute au registre de la copie la dernière ligne de `source` (la fiche jugée au passage, marquée par
    l'enchaîneur), avec `changes` — comme le ferait une main. Le registre est remis depuis l'instantané du passage
    avant et après chaque sabotage (`jouer_les_sabotages`). [rend: 1]"""
    def f(ch, c):
        reg = os.path.join(c, REG)
        octets = open(reg, "rb").read()
        lignes = list(csv.reader(octets.decode("utf-8-sig").splitlines()))
        ent = lignes[0]
        neuve = list([l for l in lignes[1:] if l and l[ent.index("id")] == source][-1])
        for col, val in changes.items():
            neuve[ent.index(col)] = val
        with open(reg, "a", encoding="utf-8", newline="") as fh:
            csv.writer(fh, lineterminator="\r\n" if octets.endswith(b"\r\n") else "\n").writerow(neuve)
    return f


def temoin_augmente(ch, c):
    """S15 : le témoin de résultats de la chaîne gagne une version absente de la combinatoire (son journal remis à
    jour : seul ce défaut reste), et l'assemblage est à refaire (tranches gardées). [rend: rien]"""
    rel = "e1/TEMOIN_RESULTATS_%s_%s.csv" % (SID, ESSAI)
    lignes = list(csv.DictReader(open(os.path.join(ch, rel), encoding="utf-8-sig")))
    champs = list(lignes[0])
    lignes.append(dict(lignes[0], id_version="%s-%s-9999" % (SID, ESSAI)))
    with open(os.path.join(ch, rel), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=champs, lineterminator="\n")
        w.writeheader()
        w.writerows(lignes)
    j = journal(ch)
    for l in j:
        if l["etape"] == "1-temoin-de-resultats":
            l["sha256"] = hashlib.sha256(open(os.path.join(ch, rel), "rb").read()).hexdigest()
    reecrire_journal(ch, j)
    assemblage_a_refaire(ch, c)


def assemblage_a_refaire(ch, c):
    os.remove(os.path.join(ch, "e2", "RESULTATS_%s_%s.csv" % (SID, ESSAI)))
    reecrire_journal(ch, [l for l in journal(ch) if l["etape"] not in ("2-assembler", "3-trier")])


def journal_mal_forme(ch, c):
    """S16 : l'en-tête du journal dit « etap » au lieu de « etape » (M1 du relecteur du 19-11-2026). [rend: rien]"""
    p = os.path.join(ch, "JOURNAL_DE_LA_CHAINE.csv")
    s = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(s.replace("etape,", "etap,", 1))


def sabotages(travail):
    """(nom, instantané, geste, commande, code attendu, mots attendus, commande verte, porte?) [rend: 1]"""
    v = json.load(open(os.path.join(travail, "passage.json")))
    J, H = v["jugee"], v["hors_retenues"]
    juge, verif = [JUGE, "{copie}", J], [VERIF, "{copie}", J]
    import CONTRATS_DES_FICHIERS as C
    marque = "%s %s %s" % (C.MARQUE_DE_MOULINETTE, SID, ESSAI)
    autre = J.lower().rsplit("-", 1)[0] + "-00001 "      # 5 chiffres, minuscules, espace final (I1)
    return [
        ("S0 juge direct, sans journal", "inst", vider, juge, 2, "aucune chaîne n'est trouvée", verif, True),
        ("S0b ② sans ①", "inst", lambda ch, c: (vider(ch, c), ench(c, "preparer")), ["ENCH", "jouer", "0", "5"], 1,
         "1-decliner absente", verif, False),
        ("S1 sauter ①", "inst", sans("1-"), juge, 1, "1-decliner absente", verif, True),
        ("S2 sauter ②", "inst", sans("2-"), juge, 1, "2-assembler absente", verif, True),
        ("S3 sauter ③", "inst", sans("3-"), juge, 1, "3-trier absente", verif, True),
        ("S4 tranche de ② retirée", "inst", retirer("e2/tranche_2.csv"), juge, 1, "tranche_2.csv a disparu", verif,
         True),
        ("S4m tranche jamais jouée (M1)", "inst", tranche_perdue_avant_assemblage, ["ENCH", "assembler"], 1,
         "sans résultat", verif, False),
        ("S5 fichier de ③ modifié", "inst", modifier(TRI, ",0.02,", ",0.03,"), juge, 1, "a changé depuis son témoin",
         verif, True),
        ("S6 version hors retenues", "inst", fiche_ajoutee(J, id=H), [JUGE, "{copie}", H], 1, "retenues par le tri",
         verif, True),
        ("S7 réglages non validés", "inst", non_valides, juge, 1, "NON VALIDÉ PAR JEAN-LUC", verif, True),
        ("S8 tri illisible (R-734)", "inst", tri_illisible, juge, 2, "n'a pas pu être vérifiée", verif, False),
        ("S9 juge en échec", "inst", golden_casse, ["ENCH", "juger", J], 1, "aucun témoin ④", ["ENCH", "juger", J],
         False),
        ("S10 chiffres du juge falsifiés", "inst4", modifier("e4/juge_%s.txt" % J, "operations", "0perations"),
         [VERIF, "{copie}", J, "--juge-fait"], 1, "a changé depuis son témoin", [VERIF, "{copie}", J, "--juge-fait"],
         True),
        # LOT 2 — relecture du 19-11-2026 (B1, I1, I2, M1) et décision A-921 (la marque, jamais le nom)
        ("S11 même id, tp 9.5 (B1)", "inst", fiche_ajoutee(J, tp="9.5"), juge, 1, "ne sont pas ceux que ② a joués",
         verif, True),
        # S12 (M2 du relecteur du 19-11-2026) : un signal qui PASSE la porte 0 — celui d'IND-001-RETEST, au registre —,
        # pour que, porte neutralisée, le juge juge (code 0) : le code rougit alors pour la porte, pas pour la porte 0.
        ("S12 même id, autre signal", "inst",
         fiche_ajoutee(J, module_signal="programmes/MODULE_SIGNAL_RSI_REBOND.py", fonction_signal="signaux_rsi_rebond",
                       reglages_signal='{"periode": 14, "seuil": 30, "chauffe": 100}'),
         juge, 1, "ne sont pas ceux que ② a joués", verif, True),
        ("S13 marquée, sans chaîne", "inst", fiche_ajoutee(J, **{C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE:
                                                                marque.replace(" " + ESSAI, " E09")}),
         juge, 2, "aucune chaîne n'est trouvée", verif, True),
        ("S14 -00001 minuscules espace (I1)", "inst", fiche_ajoutee(J, id=autre), [JUGE, "{copie}", autre], 1,
         "retenues par le tri", verif, True),
        ("S15 témoin augmenté, 5 tranches (I2)", "inst", temoin_augmente, ["ENCH", "assembler"], 1,
         "diffère du témoin de résultats entier", ["PREP", assemblage_a_refaire, "ENCH", "assembler"], False),
        ("S16 journal mal formé (M1)", "inst", journal_mal_forme, juge, 2, "mal formé", verif, True),
        ("S17 marque retirée : TROU A-921", "inst", fiche_ajoutee(J, **{C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE: ""}),
         juge, 0, "operations .", verif, False),
        # LOT 3 — tour 3 du 19-11-2026 (superviseur R-759) : B1, I1, I2 du relecteur
        ("S18 deux fiches pour la cible (B1)", "inst",
         fiche_ajoutee(J, id=J + " ", tp="9.5", **{C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE: ""}), juge, 2,
         "ne désigne pas UNE fiche", verif, True),
        ("S19 marque en minuscules, tp 9.5 (I1)", "inst",
         fiche_ajoutee(J, tp="9.5", **{C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE: marque.lower()}), juge, 1,
         "ne sont pas ceux que ② a joués", verif, True),
        ("S20 autre barème des verdicts (I2)", "inst",
         fichier_change("programmes/MODULE_POSITIONS.py", 'BAREME_DES_VERDICTS = "REEL"',
                        'BAREME_DES_VERDICTS = "HIST_COURTAGE_SANS_TTF"'), juge, 1,
         "le barème du juge n'est pas celui que ② a joué", verif, True),
        ("S20b courtage 0.0015→0.015 (I2)", "inst",
         fichier_change("donnees/BAREME_FRAIS.csv", "REEL,action_et_etf,courtage,achat_et_vente,0.0015,",
                        "REEL,action_et_etf,courtage,achat_et_vente,0.015,"), juge, 1,
         "le contenu du barème 'REEL' a changé depuis ②", verif, True),
        ("S21 cours joués changés (I2)", "inst",
         volume_change("donnees/cours_maitre.csv", "ACCOR,2024-01-02,"), juge, 1,
         "les cours que ② a joués ont changé", verif, True),
    ]


def commande(copie, cmd):
    if cmd[0] == "PREP":                 # un geste avant la commande verte (S15) : l'état sans le seul sabotage
        cmd[1](os.path.join(copie, CH), copie)
        cmd = cmd[2:]
    if cmd[0] == "ENCH":
        return ench(copie, *cmd[1:])
    return py(copie, *[copie if x == "{copie}" else x for x in cmd])


def remettre(travail, copie, ch, inst):
    """Le dossier de la chaîne depuis son instantané, et le registre de la copie depuis celui du passage. [rend: rien]"""
    shutil.rmtree(ch)
    shutil.copytree(os.path.join(travail, inst), ch)
    shutil.copyfile(os.path.join(travail, "registre_apres_passage.csv"), os.path.join(copie, REG))


def jouer_les_sabotages(travail, attendre_rouge, lot):
    """Chaque sabotage du lot : instantané, geste, commande ; puis instantané, commande verte. [rend: 1]"""
    copie, ch = os.path.join(travail, "depot"), os.path.join(travail, "depot", CH)
    ok = True
    sys.path.insert(0, os.path.join(copie, "programmes"))
    for nom, inst, geste, cmd, code_att, mots, vert, porte in sabotages(travail):
        if lot_de(nom) != lot:
            continue
        if not attendre_rouge and not porte:
            continue                     # la contre-épreuve ne vise que la porte
        remettre(travail, copie, ch, inst)
        geste(ch, copie)
        if not attendre_rouge and lot == 3:      # la contre-épreuve du lot 3 : SA correction défaite
            fichier_change(*CONTRE3[nom.split()[0]])(ch, copie)
        c, o = commande(copie, list(cmd))
        temoin4 = nom.startswith("S9") and any(l["etape"].startswith("4-") for l in journal(ch))   # S16 : en-tête faux
        rouge = c == code_att and mots in o and not (nom.startswith("S9") and temoin4) and "Traceback" not in o
        if nom.startswith("S17") and rouge:
            print("    TROU DÉCLARÉ (A-921) MONTRÉ : la fiche jugée au passage, ré-ajoutée SANS la marque de moulinette,"
                  " a été JUGÉE (code 0) — c'est le trou assumé, écrit au ⑨ du juge")
        module_remis(copie)
        fichiers_remis()
        remettre(travail, copie, ch, inst)
        c2, o2 = commande(copie, list(vert))
        tient = (rouge and c2 == 0) if attendre_rouge else \
            (not rouge and (c != code_att or nom.split()[0] not in CODE_AUSSI))
        ok &= tient
        ligne = ([l for l in o.splitlines() if mots in l] or o.strip().splitlines()[-1:] or [""])[0].strip()
        print("%s %-32s rouge=%s (code %d, attendu %d) · retiré → code %d · « %s »"
              % ("OK " if tient else "KO ", nom, rouge, c, code_att, c2, ligne[:120]))
        if not tient and attendre_rouge:
            print("   sortie verte : %s" % o2.strip().splitlines()[-3:])
    remettre(travail, copie, ch, "inst4")
    return ok


def main():
    if len(sys.argv) != 5:
        print(__doc__.split("① RÔLE")[0])
        return 2
    source, vrai, travail = [os.path.abspath(x) for x in sys.argv[1:4]]
    phase = sys.argv[4]
    copie, ch = os.path.join(travail, "depot"), os.path.join(travail, "depot", CH)
    if phase == "avant":
        os.makedirs(travail, exist_ok=True)
        av = empreintes(source, vrai)
        json.dump(av, open(os.path.join(travail, "avant.json"), "w"))
        E.RACINE = source
        shutil.copytree(source, copie, ignore=E.ignorer, symlinks=False)
        print("EMPREINTES AVANT : %s\nCOPIE : %s · .git %s · prompts_taches %s" % (
            av, copie, os.path.lexists(os.path.join(copie, ".git")),
            os.path.lexists(os.path.join(copie, "prompts_taches"))))
        return 0
    if phase == "passage":
        t0 = time.time()
        for e in [["preparer"], ["decliner"]] + [["jouer", str(k), str(NB)] for k in range(NB)] + \
                [["assembler"], ["trier"]]:
            t = time.time()
            c, o = ench(copie, *e)
            print("%-12s code %d en %5.1f s" % (" ".join(e), c, time.time() - t))
            if c:
                print(o)
                return 1
        tri = list(csv.DictReader(open(os.path.join(ch, TRI), encoding="utf-8")))
        tous = [r["id_version"] for r in csv.DictReader(open(os.path.join(ch, "e1", "COMBINATOIRE_%s_%s.csv"
                                                                          % (SID, ESSAI)), encoding="utf-8"))]
        debuts = {r["periode_debut"] for r in csv.DictReader(open(os.path.join(ch, "e2", "RESULTATS_%s_%s.csv"
                                                                               % (SID, ESSAI)), encoding="utf-8"))}
        jugee = tri[0]["id_version"]
        hors = [i for i in tous if i not in {r["id_version"] for r in tri}][0]
        json.dump({"jugee": jugee, "hors_retenues": hors}, open(os.path.join(travail, "passage.json"), "w"))
        shutil.copytree(ch, os.path.join(travail, "inst"))       # avant le juge
        t = time.time()
        c, o = ench(copie, "juger", jugee)
        print("juger %s code %d en %.1f s" % (jugee, c, time.time() - t))
        print("\n".join("  " + l for l in o.splitlines() if "operations ." in l)[:600])
        shutil.copytree(ch, os.path.join(travail, "inst4"))      # après le juge
        shutil.copyfile(os.path.join(copie, REG), os.path.join(travail, "registre_apres_passage.csv"))
        c2, o2 = py(copie, VERIF, copie, jugee, "--juge-fait")
        print("VERIFIER --juge-fait : code %d · %s" % (c2, o2.strip().splitlines()[-1]))
        print("PASSAGE COMPLET : %.0f s · %d versions déclinées · %d retenues · période(s) jouée(s) dès %s"
              % (time.time() - t0, len(tous), len(tri), sorted(debuts)))
        return 0 if c == 0 and c2 == 0 and min(debuts) >= "2024-01-01" else 1
    if phase in ("sabotages", "sabotages2", "sabotages3"):
        return 0 if jouer_les_sabotages(travail, True, int(phase[-1]) if phase[-1].isdigit() else 1) else 1
    if phase == "contre3":
        ok = jouer_les_sabotages(travail, False, 3)
        print("CONTRE-ÉPREUVE DU LOT 3 : chaque correction défaite, son sabotage ne rougit plus, code compris : %s" % ok)
        return 0 if ok else 1
    if phase in ("contre", "contre2"):
        # LA PORTE ENTIÈRE NEUTRALISÉE : une porte qui ne garde plus rien, définie juste avant `main`.
        p = os.path.join(copie, VERIF)
        s = open(p, encoding="utf-8").read()
        motif, neutre = "\n\ndef main(argv):", "\n\ndef porte_du_juge(*a, **k):\n    return None\n\n\ndef main(argv):"
        if s.count(motif) != 1:
            print("CONTRE-ÉPREUVE IMPOSSIBLE : motif introuvable")
            return 2
        shutil.copyfile(p, p + ".garde")
        try:
            open(p, "w", encoding="utf-8").write(s.replace(motif, neutre))
            ok = jouer_les_sabotages(travail, False, 2 if phase.endswith("2") else 1)
        finally:
            os.replace(p + ".garde", p)
        print("CONTRE-ÉPREUVE : porte neutralisée, aucun sabotage de la porte ne rougit pour sa raison : %s" % ok)
        return 0 if ok else 1
    if phase == "bilan":
        av, ap = json.load(open(os.path.join(travail, "avant.json"))), empreintes(source, vrai)
        print("AVANT : %s\nAPRÈS : %s\nIDENTIQUES : %s · registre_essais dans la copie : %d" % (
            av, ap, av == ap, len(E.registres_d_essais(copie))))
        return 0 if av == ap else 1
    print("phase inconnue")
    return 2


if __name__ == "__main__":
    sys.exit(main())
