#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_DUREES_PUBLIEES — Sam 21-11-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que le fichier des durées publiées (rapports/durees_des_epreuves_en_secondes.csv, A-968) ne porte que
  la clé d'un lancement et ses secondes, qu'il est refusé dès qu'il porte autre chose, et qu'il donne à la répartition
  des tranches de la nuit la même tranche la plus lourde que les journaux dont il est tiré.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py joue toute épreuve de
  tests/) ; à la main avant toute livraison qui touche `durees_relevees`, `garder_les_durees`,
  `lire_les_durees_publiees` ou `publier_les_durees` (R-731) :
  python3 tests/EPREUVES_DES_DUREES_PUBLIEES_Sam_21-11-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt : son programmes/CERTIFIER_LA_VERSION.py, ses épreuves (pour la liste des lancements et
  leurs délais), son programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (le nombre de tranches), ses journaux s'il en a, son
  fichier des durées publiées s'il en a un.
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le code de sortie : 0 si P1 à P7 donnent la réponse attendue et, avec --saboter, si chaque sabotage fait
  tomber le cas qu'il vise (ATTENDU) ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT — Sur des dossiers jetables, avec le certificateur copié (saboté ou non) :
  P1 SANS LE FICHIER — ni journal ni fichier : `durees_relevees` rend {} ; la répartition compte alors chaque
  lancement pour son délai (ce que N5 de la nuit découpée voyait sur GitHub, passage 44906050466).
  P2 REFUS — `garder_les_durees`, puis `lire_les_durees_publiees` sur le même tableau écrit en fichier, lèvent
  ValueError pour : une troisième colonne à l'en-tête · une ligne à trois champs · une clé qui n'a pas la forme d'un
  lancement (« Société Générale ») · des secondes qui ne sont pas faites de chiffres mais que int() accepterait
  (« +12 », « 1_2 », « 12 » précédé d'une espace) · une clé en double. ÉTALONNAGE : un tableau correct passe.
  P3 L'ÉCRIVAIN EST GARDÉ — un journal dont une ligne porte une clé hors forme : `publier_les_durees` lève ValueError
  et n'écrit aucun fichier.
  P4 ÉGALITÉ — des journaux témoins (deux passages, une durée par vrai lancement, tirée de sa clé) : publiés, puis
  relus dans un dossier qui n'a QUE le fichier, ils rendent les mêmes durées et la même tranche la plus lourde ; et
  cette tranche diffère de celle de P1 (sinon le cas ne discriminerait rien). Si la racine a ses vrais journaux, la
  même égalité sur eux, journaux copiés dans un dossier jetable (la racine n'est jamais écrite).
  P5 LES JOURNAUX PRIMENT — un dossier qui a des journaux ET un fichier aux durées différentes : les journaux sont lus.
  P6 LE FICHIER DU DÉPÔT EST SAIN — s'il existe à la racine, `lire_les_durees_publiees` l'accepte.
  P7 LE CIRCUIT DE NUIT LE REFAIT (A-969, décision de Jean-Luc du 21-11-2026 à 16h09) — dans le circuit de
  certification FABRIQUÉ par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, la tâche finale (job « reunir ») : a) lance
  CERTIFIER_LA_VERSION.py « --publier-les-durees » APRÈS « --reunir » et AVANT le dépôt au privé ; b) son dépôt ajoute
  le fichier, au chemin même du certificateur ; c) ce pas ne masque pas son échec (aucun « continue-on-error », un
  « ::error:: » et un « exit 1 »). Ses sabotages (F1 à F5) portent sur une copie du FABRICANT.
⑦ UNITÉ — Des secondes.
⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 15h34, réponse « 1 » à la question du Chat de 15h33 : « Publier au
  dépôt public les seules durées des épreuves (des chiffres de temps, aucun cours) pour que GitHub juge pour de vrai ».
  La copie jouée sur GitHub exclut les journaux (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, SERIES_COPIE) : sans eux,
  chaque lancement comptait pour son délai, et N5 voyait 20 400 s par tranche. Les journaux, qui portent aussi les
  sorties des épreuves, ne doivent jamais être publiés : d'où la garde, éprouvée ici des deux côtés.
⑨ CE QUI CLOCHE — La FRAÎCHEUR du fichier n'est pas jugée : des durées périmées font une prévision périmée. P7 lit le
  TEXTE du circuit fabriqué : il ne prouve pas que GitHub exécute le pas ni que la poussée réussit (seul un passage
  réel de la nuit le prouve). La publication elle-même au dépôt public n'est pas jouée ici.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; aucun processus lancé ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import shutil
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
CERTIF = "programmes/CERTIFIER_LA_VERSION.py"
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
EN_TETE = ["cle_du_lancement", "secondes"]   # écrit ici à dessein : l'épreuve confronte le certificateur à ce contrat

SABOTAGES = {
    "Z0": [],
    "S1_sans_repli": [("        return lire_les_durees_publiees(racine)\n", "        return {}\n")],
    "S2_ligne_a_trois_champs_acceptee": [("        if len(l) != 2:\n", "        if len(l) < 2:\n"),
                                         ("        cle, secondes = l\n", "        cle, secondes = l[0], l[1]\n")],
    "S3_en_tete_non_verifie": [("    if not lignes or list(lignes[0]) != COLONNES_DES_DUREES:\n",
                                "    if not lignes:\n")],
    "S4_cle_non_verifiee": [("        if not re.match(CLE_PUBLIABLE, cle):\n", "        if False:\n")],
    "S5_secondes_non_verifiees": [('        if not re.fullmatch(r"[0-9]+", secondes):\n', "        if False:\n")],
    "S6_ecrire_sans_garde": [("    garder_les_durees(lignes)\n    chemin = ", "    chemin = ")],
    "S7_repli_meme_avec_journaux": [("    if not any(re.match(JOURNAL_DE_CERTIFICATION, f) for f in noms):\n",
                                     "    if True:\n")],
    "S8_fichier_absent_non_vide": [("        return {}\n    with open(chemin",
                                    '        return {"tests/x.py": 1}\n    with open(chemin')],
    "S9_publier_recopie_autre_chose": [("[[c, str(durees[c])] for c in sorted(durees)]",
                                        "[[c, str(durees[c] // 2)] for c in sorted(durees)]")],
    "S10_cle_en_double_acceptee": [("        if cle in rendu:\n", "        if False:\n")],
}
# les sabotages du FABRICANT (P7, A-969) : chaque texte doit paraître une fois dans programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py
SABOTAGES_DU_FABRICANT = {
    "F1_pas_retire": [('    "publier_les_durees": PUBLIER_LES_DUREES,\n', '    "publier_les_durees": "",\n')],
    "F2_option_retiree": [('CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees \\\\',
                           'CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" \\\\')],
    "F3_fichier_non_pousse": [('"rapports/CERTIFICAT_DE_LA_VERSION.md rapports/journal_du_circuit/ $DUREES"',
                               '"rapports/CERTIFICAT_DE_LA_VERSION.md rapports/journal_du_circuit/"')],
    "F4_echec_masque": [("        id: publier_les_durees\n", "        id: publier_les_durees\n        continue-on-error: true\n")],
    "F5_chemin_divergent": [('DUREES_PUBLIEES_DU_DEPOT = "rapports/durees_des_epreuves_en_secondes.csv"',
                             'DUREES_PUBLIEES_DU_DEPOT = "rapports/durees.csv"')],
}
ATTENDU = {"F1_pas_retire": "P7 a)", "F2_option_retiree": "P7 a)", "F3_fichier_non_pousse": "P7 b)",
           "F4_echec_masque": "P7 c)", "F5_chemin_divergent": "P7 b)",
           "S1_sans_repli": "P4 ", "S2_ligne_a_trois_champs_acceptee": "P2 ligne à trois champs",
           "S3_en_tete_non_verifie": "P2 troisième colonne", "S4_cle_non_verifiee": "P2 clé",
           "S5_secondes_non_verifiees": "P2 secondes", "S6_ecrire_sans_garde": "P3 ",
           "S7_repli_meme_avec_journaux": "P5 ", "S8_fichier_absent_non_vide": "P1 ",
           "S9_publier_recopie_autre_chose": "P4 ", "S10_cle_en_double_acceptee": "P2 clé en double"}


def charger(chemin, nom):
    """Charge un module depuis son fichier et le rend.

    ① RÔLE — Appeler les fonctions du certificateur copié (saboté ou non) et lire le fabricant.
    ② CONTEXTE D'APPEL — `tour`, `main`.
    ③ ENTRÉE — `chemin` : le fichier · `nom` : le nom donné au module.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le certificateur n'est pas un paquet : il se charge par son chemin.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le module (le certificateur et le fabricant ne font que définir à leur chargement).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def ecrire_csv(chemin, lignes):
    """Écrit un tableau en CSV (module csv), en créant son dossier.

    ① RÔLE — Poser un fichier de durées choisi par l'épreuve.
    ② CONTEXTE D'APPEL — `tour`, P2, P5.
    ③ ENTRÉE — `chemin` · `lignes` : liste de listes de textes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — csv.writer, fins de ligne « \\n ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La même écriture que `publier_les_durees`, pour que P2 éprouve la lecture et non le format.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import csv
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(lignes)


def leve(fonction, *args):
    """Dit si un appel lève ValueError.

    ① RÔLE — Juger un refus. ② CONTEXTE D'APPEL — `tour`, P2 et P3.
    ③ ENTRÉE — `fonction` et ses arguments. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : True si ValueError est levée, False si l'appel rend la main.
      [rend: 1]
    ⑥ TRAITEMENT — appeler, attraper ValueError seulement. ⑦ UNITÉ — —
    ⑧ POURQUOI — Toute autre exception est une panne : elle remonte, et l'épreuve tombe en trace (code 1, rouge).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Celui de l'appel. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        fonction(*args)
    except ValueError:
        return True
    return False


def tour(C, k, lancements, delais):
    """Joue P1 à P6 avec le certificateur `C` et rend la liste des fautes.

    ① RÔLE — Un tour d'épreuves.
    ② CONTEXTE D'APPEL — `main`, une fois tel quel (Z0) puis une fois par sabotage.
    ③ ENTRÉE — `C` : le certificateur chargé · `k` : le nombre de tranches de la nuit · `lancements`, `delais` : ceux
      de la racine (lus par `main`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes (textes commençant par le nom du cas).
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥.
    ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Les durées témoins de P4 sont tirées de la longueur de chaque clé : elles ne ressemblent pas aux
      vraies, elles servent à discriminer (P4 vérifie qu'elles changent la tranche la plus lourde).
    ⑩ EFFET — Écrit des dossiers jetables, effacés à la fin.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    faux = []
    jet = tempfile.mkdtemp(prefix="durees_publiees_")
    try:
        def lourde(durees):
            """Rend la charge de la tranche la plus lourde, en secondes. ① RÔLE — Résumer une répartition.
            ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `durees`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur.
            [rend: 1] ⑥ TRAITEMENT — `repartir` du certificateur, k tranches. ⑦ UNITÉ — Des secondes.
            ⑧ POURQUOI — N5 de la nuit découpée juge chaque tranche : la plus lourde décide. ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            return max(C.repartir(lancements, durees, delais, k)[1])

        # P1 — ni journal ni fichier
        vide = os.path.join(jet, "vide")
        os.makedirs(vide)
        d1 = C.durees_relevees(vide)
        if d1 != {}:
            faux.append(f"P1 sans journal ni fichier : {len(d1)} durée(s) rendue(s), attendu aucune")
        sans = lourde({})

        # P2 — refus, et étalonnage
        bon = [EN_TETE, ["tests/x.py", "12"], ["tests/x.py --saboter", "30"]]
        cas = [("troisième colonne", [EN_TETE + ["cours"], ["tests/x.py", "12"]]),
               ("ligne à trois champs", [EN_TETE, ["tests/x.py", "12", "101.5"]]),
               ("clé", [EN_TETE, ["Société Générale", "12"]]),
               ("secondes « +12 »", [EN_TETE, ["tests/x.py", "+12"]]),
               ("secondes « 1_2 »", [EN_TETE, ["tests/x.py", "1_2"]]),
               ("secondes « 12» précédé d'une espace", [EN_TETE, ["tests/x.py", " 12"]]),
               ("clé en double", [EN_TETE, ["tests/x.py", "12"], ["tests/x.py", "13"]])]
        if leve(C.garder_les_durees, bon) or C.garder_les_durees(bon) != {"tests/x.py": 12, "tests/x.py --saboter": 30}:
            faux.append("P2 étalonnage : un tableau correct est refusé ou mal rendu")
        for i, (nom, lignes) in enumerate(cas):
            if not leve(C.garder_les_durees, lignes):
                faux.append(f"P2 {nom} : accepté par la garde")
            r = os.path.join(jet, f"p2_{i}")
            ecrire_csv(os.path.join(r, C.DUREES_PUBLIEES), lignes)
            if not leve(C.lire_les_durees_publiees, r):
                faux.append(f"P2 {nom} : accepté à la lecture du fichier")
        r = os.path.join(jet, "p2_bon")
        ecrire_csv(os.path.join(r, C.DUREES_PUBLIEES), bon)
        if leve(C.lire_les_durees_publiees, r):
            faux.append("P2 étalonnage : un fichier correct est refusé à la lecture")

        # P3 — l'écrivain est gardé : une clé hors forme dans un journal
        r = os.path.join(jet, "p3")
        os.makedirs(os.path.join(r, C.JOURNAUX))
        open(os.path.join(r, C.JOURNAUX, "circuit_100_1_certifier.log"), "w", encoding="utf-8").write(
            C.ligne_du_journal("tests/x.py", [], 0, 5) + "\n  vert  Société Générale 45,30 · code 0 · 7 s\n")
        if not leve(C.publier_les_durees, r):
            faux.append("P3 un journal à clé hors forme est publié sans refus")
        if os.path.exists(os.path.join(r, C.DUREES_PUBLIEES)):
            faux.append("P3 le fichier des durées est écrit malgré une clé hors forme")

        # P4 — égalité : journaux témoins, puis vrais journaux s'il y en a
        temoin = os.path.join(jet, "p4_journaux")
        os.makedirs(os.path.join(temoin, C.JOURNAUX))
        cles = sorted({C.cle_de(l[0], l[2]) for l in lancements})
        for passage, facteur in (("200", 7), ("201", 11)):
            open(os.path.join(temoin, C.JOURNAUX, f"circuit_{passage}_1_certifier_tranche_1.log"), "w",
                 encoding="utf-8").write("".join(C.ligne_du_journal(c, [], 0, (len(c) * facteur) % 997 + 1) + "\n"
                                                 for c in cles))
        sources = [("témoins", temoin)]
        vrais = os.path.join(DEPOT, C.JOURNAUX)
        if os.path.isdir(vrais):
            copie = os.path.join(jet, "p4_vrais")
            shutil.copytree(vrais, os.path.join(copie, C.JOURNAUX))
            sources.append(("vrais", copie))
        for nom, source in sources:
            d_j = C.durees_relevees(source)
            if nom == "vrais" and not d_j:
                continue                     # la racine n'a pas de journal de certification : rien à comparer
            try:
                C.publier_les_durees(source)
            except ValueError as e:
                faux.append(f"P4 {nom} : publication refusée ({e})")
                continue
            seul = os.path.join(jet, f"p4_{nom}_fichier_seul")
            os.makedirs(os.path.dirname(os.path.join(seul, C.DUREES_PUBLIEES)))
            shutil.copyfile(os.path.join(source, C.DUREES_PUBLIEES), os.path.join(seul, C.DUREES_PUBLIEES))
            d_f = C.durees_relevees(seul)
            if d_f != d_j:
                faux.append(f"P4 {nom} : le fichier seul rend {len(d_f)} durée(s), dont "
                            f"{sum(1 for c in d_f if d_j.get(c) != d_f[c])} différente(s) des journaux ({len(d_j)})")
            if lourde(d_f) != lourde(d_j):
                faux.append(f"P4 {nom} : tranche la plus lourde {lourde(d_f)} s avec le fichier, "
                            f"{lourde(d_j)} s avec les journaux")
            if nom == "témoins" and lourde(d_j) == sans:
                faux.append(f"P4 témoins : la tranche la plus lourde vaut {sans} s avec ou sans durées — le cas ne "
                            "discrimine rien")

        # P5 — les journaux priment sur le fichier
        r = os.path.join(jet, "p5")
        os.makedirs(os.path.join(r, C.JOURNAUX))
        open(os.path.join(r, C.JOURNAUX, "circuit_300_1_certifier.log"), "w", encoding="utf-8").write(
            C.ligne_du_journal("tests/x.py", [], 0, 40) + "\n")
        ecrire_csv(os.path.join(r, C.DUREES_PUBLIEES), [EN_TETE, ["tests/x.py", "9999"]])
        if C.durees_relevees(r) != {"tests/x.py": 40}:
            faux.append(f"P5 journaux et fichier présents : {C.durees_relevees(r)}, attendu les journaux, "
                        "{'tests/x.py': 40}")

        # P6 — le fichier du dépôt, s'il existe, est sain
        if os.path.isfile(os.path.join(DEPOT, C.DUREES_PUBLIEES)) and leve(C.lire_les_durees_publiees, DEPOT):
            faux.append(f"P6 le fichier {C.DUREES_PUBLIEES} du dépôt est refusé par la garde")
    finally:
        shutil.rmtree(jet, ignore_errors=True)
    return faux


def p7(F, C):
    """Juge le circuit de certification fabriqué par `F` (P7) et rend la liste des fautes.

    ① RÔLE — Prouver que la tâche finale de la nuit refait et pousse le fichier des durées (A-969).
    ② CONTEXTE D'APPEL — `main`, en Z0 avec le fabricant de la racine, puis une fois par sabotage du fabricant.
    ③ ENTRÉE — `F` : le fabricant chargé (son texte CERTIFICATION et DUREES_PUBLIEES_DU_DEPOT) · `C` : le certificateur
      sain (son DUREES_PUBLIEES).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes (textes commençant par « P7 a) », « P7 b) » ou « P7 c) »).
      [rend: 1]
    ⑥ TRAITEMENT — ① isoler le job « reunir » (de « \\n  reunir:\\n » à la fin) et le couper en pas (« - name: » à six
      espaces) · ② a) un pas porte « CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees », placé après le
      pas qui porte « --reunir » et avant « Deposer au depot prive » · ③ b) le chemin du fabricant, « / » remplacé par
      le séparateur du système, égale DUREES_PUBLIEES du certificateur, et le pas de dépôt l'affecte à DUREES et porte
      « $DUREES » sur sa ligne « git add » · ④ c) le pas de publication ne porte pas « continue-on-error » et porte
      « ::error:: » et « exit 1 ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 16h09 (« 1 ») : le circuit de nuit refait le fichier chaque nuit,
      pour des prévisions toujours fondées sur des durées récentes. Sans ce pas, rien ne le refaisait (A-968).
    ⑨ CE QUI CLOCHE — Lecture du texte seulement : l'exécution par GitHub n'est pas prouvée ici.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    faux = []
    texte = F.CERTIFICATION
    if "\n  reunir:\n" not in texte:
        return ["P7 a) job « reunir » introuvable dans le circuit fabriqué"]
    pas = texte.split("\n  reunir:\n", 1)[1].split("\n      - name: ")
    appel = 'CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees'
    i_pub = [i for i, p in enumerate(pas) if appel in p]
    i_reu = [i for i, p in enumerate(pas) if "--reunir" in p]
    i_dep = [i for i, p in enumerate(pas) if p.startswith("Deposer au depot prive")]
    if len(i_pub) != 1 or len(i_reu) != 1 or len(i_dep) != 1 or not i_reu[0] < i_pub[0] < i_dep[0]:
        faux.append(f"P7 a) publication {i_pub}, réunion {i_reu}, dépôt {i_dep} : attendu un pas de chaque, dans cet ordre")
    chemin = F.DUREES_PUBLIEES_DU_DEPOT
    if chemin.replace("/", os.sep) != C.DUREES_PUBLIEES:
        faux.append(f"P7 b) chemin du fabricant {chemin} ≠ celui du certificateur {C.DUREES_PUBLIEES}")
    if len(i_dep) == 1:
        dep = pas[i_dep[0]]
        ajout = [l for l in dep.split("\n") if l.strip().startswith("git add ")]
        if f"DUREES={chemin}" not in dep or len(ajout) != 1 or "$DUREES" not in ajout[0].split():
            faux.append(f"P7 b) le dépôt n'ajoute pas {chemin} : {ajout}")
    if len(i_pub) == 1:
        pub = pas[i_pub[0]]
        if "continue-on-error" in pub or "::error::" not in pub or "exit 1" not in pub:
            faux.append("P7 c) le pas de publication masque son échec (continue-on-error, ou sans ::error:: / exit 1)")
    return faux


def fabricant_sabote(nom, d):
    """Écrit dans `d` une copie du fabricant sabotée par `nom`, entourée du reste du dépôt, et la charge.

    ① RÔLE — Donner à P7 un fabricant saboté, sans jamais écrire dans la racine.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage du fabricant.
    ③ ENTRÉE — `nom` : une clé de SABOTAGES_DU_FABRICANT · `d` : un dossier jetable vide.
    ④ CONDITIONS D'ENTRÉE — Chaque texte du sabotage paraît une fois dans le fabricant.
    ⑤ SORTIE — UNE valeur : le module chargé, ou None si un texte ne paraît pas exactement une fois.
      [rend: 1]
    ⑥ TRAITEMENT — ① appliquer les remplacements au texte du fabricant · ② poser dans `d` un lien vers chaque entrée de
      la racine sauf programmes/, et dans `d`/programmes un lien vers chaque fichier sauf le fabricant, écrit saboté ·
      ③ le charger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fabricant lit des fichiers voisins par son propre chemin (__file__) : la copie doit avoir les mêmes
      voisins. Des liens, pour ne rien recopier ni rien écrire dans la racine.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d` (effacé par l'appelant).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    texte = open(os.path.join(DEPOT, FAB), encoding="utf-8").read()
    for avant, apres in SABOTAGES_DU_FABRICANT[nom]:
        if texte.count(avant) != 1:
            print(f"{nom} NE S'APPLIQUE PLUS : texte trouvé {texte.count(avant)} fois")
            return None
        texte = texte.replace(avant, apres)
    for e in os.listdir(DEPOT):
        if e not in ("programmes", ".git"):
            os.symlink(os.path.join(DEPOT, e), os.path.join(d, e))
    os.makedirs(os.path.join(d, "programmes"))
    for e in os.listdir(os.path.join(DEPOT, "programmes")):
        if e != os.path.basename(FAB):
            os.symlink(os.path.join(DEPOT, "programmes", e), os.path.join(d, "programmes", e))
    chemin = os.path.join(d, FAB)
    open(chemin, "w", encoding="utf-8").write(texte)
    return charger(chemin, "FAB_" + nom)


def main():
    """Joue Z0, puis, avec --saboter, un tour par sabotage du certificateur copié.

    ① RÔLE — Le programme entier.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête.
    ⑤ SORTIE — Le code de sortie (0, 1, 2).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire, avec le certificateur NON saboté de la racine, les lancements, leurs délais, et au fabricant
      le nombre de tranches · ② pour chaque cas : copier le certificateur dans un dossier jetable, y appliquer le
      sabotage (chaque texte doit y paraître une fois, sinon code 2), le charger, jouer `tour` (et `p7` en Z0) · avec
      --saboter, d'abord chaque sabotage du FABRICANT (`fabricant_sabote`, puis `p7`) · ③ Z0 doit être vert ;
      chaque sabotage doit produire une faute qui porte son texte ATTENDU.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit des dossiers jetables.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sain = charger(os.path.join(DEPOT, CERTIF), "CERTIF_SAIN")
    fab_sain = charger(os.path.join(DEPOT, FAB), "FAB_SAIN")
    k = fab_sain.TRANCHES_DE_LA_NUIT
    lancements, _ = sain.lister_les_epreuves(DEPOT)
    delais, _ = sain.options_de_lancement(DEPOT)
    if list(sain.COLONNES_DES_DUREES) != EN_TETE:
        print(f"Z0 ROUGE : en-tête du certificateur {sain.COLONNES_DES_DUREES}, attendu {EN_TETE}")
        return 1
    noms = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    code = 0
    for nom in (list(SABOTAGES_DU_FABRICANT) if "--saboter" in sys.argv else []):
        d = tempfile.mkdtemp(prefix="durees_fab_")
        try:
            F = fabricant_sabote(nom, d)
            if F is None:
                code = 2
                continue
            faux = p7(F, sain)
            vise = [f for f in faux if ATTENDU[nom] in f]
            print(f"{nom} " + (f"mord : {vise[0][:140]}" if vise else f"NE MORD PAS : {faux[:2]}"))
            code = max(code, 0 if vise else 1)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    for nom in noms:
        d = tempfile.mkdtemp(prefix="durees_certif_")
        try:
            texte = open(os.path.join(DEPOT, CERTIF), encoding="utf-8").read()
            for avant, apres in SABOTAGES[nom]:
                if texte.count(avant) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte trouvé {texte.count(avant)} fois")
                    code = 2
                    break
                texte = texte.replace(avant, apres)
            else:
                chemin = os.path.join(d, "CERTIFIER_LA_VERSION.py")
                open(chemin, "w", encoding="utf-8").write(texte)
                faux = tour(charger(chemin, "CERTIF_" + nom), k, lancements, delais)
                if nom == "Z0":
                    faux += p7(fab_sain, sain)
                if nom == "Z0":
                    print("Z0 " + ("vert" if not faux else "ROUGE : " + " | ".join(faux)))
                    code = max(code, 1 if faux else 0)
                else:
                    vise = [f for f in faux if ATTENDU[nom] in f]
                    print(f"{nom} " + (f"mord : {vise[0][:140]}" if vise else f"NE MORD PAS : {faux[:2]}"))
                    code = max(code, 0 if vise else 1)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
