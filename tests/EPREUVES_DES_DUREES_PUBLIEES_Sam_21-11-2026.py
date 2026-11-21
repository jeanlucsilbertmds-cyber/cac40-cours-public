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
  certification FABRIQUÉ par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, la tâche finale (job « reunir ») : a) joue,
  dans cet ordre, la réunion, le dépôt du certificat, la publication (« --publier-les-durees », qui reprend d'abord les
  journaux de la nuit, sous la condition décidée), puis le dépôt des durées ; b) le dépôt des durées n'ajoute que le
  fichier, au chemin même du certificateur, sous une autre identité que « certification-publique », et seulement si
  la publication a réussi ; le dépôt du certificat ne porte pas ce fichier (I-1 de la relecture de Cowork du
  21-11-2026) ; c) chaque commande de la publication dit son échec et rend 1, sans « continue-on-error », « || true »
  ni « exit 0 » (I-2), et le pas, JOUÉ par « bash -e » avec un faux git et un faux certificateur, rend 0 et publie
  quand tout réussit, rend non nul avec son « ::error:: » quand l'un échoue (I-4). Le dépôt des durées tourne dès que
  la publication a tourné (réussie ou non), vide l'index, ajoute le fichier ET le journal de la tâche (I-3) ; les deux
  dépôts gardent leur commit et n'abandonnent pas un rebasage en plan (m-9). Ses sabotages (F1 à F5, G1 à G12, H1 à
  H5) portent sur une copie du FABRICANT.
⑦ UNITÉ — Des secondes.
⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 15h34, réponse « 1 » à la question du Chat de 15h33 : « Publier au
  dépôt public les seules durées des épreuves (des chiffres de temps, aucun cours) pour que GitHub juge pour de vrai ».
  La copie jouée sur GitHub exclut les journaux (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, SERIES_COPIE) : sans eux,
  chaque lancement comptait pour son délai, et N5 voyait 20 400 s par tranche. Les journaux, qui portent aussi les
  sorties des épreuves, ne doivent jamais être publiés : d'où la garde, éprouvée ici des deux côtés.
⑨ CE QUI CLOCHE — La FRAÎCHEUR du fichier n'est pas jugée : des durées périmées font une prévision périmée. P7 lit le
  TEXTE du circuit fabriqué, sauf la publication, JOUÉE avec des faux : il ne prouve pas que GitHub exécute le pas ni
  que la poussée réussit (seul un passage réel de la nuit le prouve) ; les deux dépôts ne sont pas joués. La publication elle-même au dépôt public n'est pas jouée ici.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; lance « bash -e » trois fois par fabricant jugé, chaque fois borné à 30 s ; sort par
  sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import re
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
    "F3_fichier_non_pousse": [('DUREES_PUBLIEES_DU_DEPOT + " " + JOURNAL_DE_LA_TACHE, VIDER_L_INDEX,',
                               '"rapports/autre.csv " + JOURNAL_DE_LA_TACHE, VIDER_L_INDEX,')],
    "F4_echec_masque": [("        id: publier_les_durees\n", "        id: publier_les_durees\n        continue-on-error: true\n")],
    "F5_chemin_divergent": [('DUREES_PUBLIEES_DU_DEPOT = "rapports/durees_des_epreuves_en_secondes.csv"',
                             'DUREES_PUBLIEES_DU_DEPOT = "rapports/durees.csv"')],
    # relecture de Cowork du 21-11-2026 (pointe 33915014d) : G1 à G4 sont SES sabotages (I-2), G5 à G8 gardent I-1
    "G1_condition_jamais_vraie": [("steps.poser_le_code.outcome == 'success' && steps.certifier.outcome != 'skipped' }}\n",
                                   "steps.poser_le_code.outcome == 'success' && steps.certifier.outcome == 'skipped' }}\n")],
    "G2_journaux_de_la_nuit_non_repris": [("          git checkout FETCH_HEAD -- rapports/journal_du_circuit \\\\\n"
                                           "            || { echo \"::error::JOURNAUX DE LA NUIT ILLISIBLES — durees non publiees\"; exit 1; }\n", "")],
    "G3_echec_de_publication_rendu_vert": [('NON PUBLIEES — le certificat est depose quand meme\"; exit 1; }',
                                            'NON PUBLIEES — le certificat est depose quand meme\"; exit 0; }')],
    "G4_ou_vrai_silencieux": [('--publier-les-durees \\\\\n', '--publier-les-durees || true \\\\\n')],
    "G5_durees_avec_le_certificat": [('"rapports/CERTIFICAT_DE_LA_VERSION.md rapports/journal_du_circuit/", ""),',
                                      '"rapports/CERTIFICAT_DE_LA_VERSION.md rapports/journal_du_circuit/ " + DUREES_PUBLIEES_DU_DEPOT, ""),')],
    "G6_durees_deposees_avant": [("%(deposer_final)s%(publier_les_durees)s%(deposer_les_durees)s%(verdict)s",
                                  "%(publier_les_durees)s%(deposer_les_durees)s%(deposer_final)s%(verdict)s")],
    "G7_durees_signees_certification": [('IDENTITE_DES_DUREES = "durees-publiees"', 'IDENTITE_DES_DUREES = "certification-publique"')],
    "G8_depot_des_durees_sans_condition": [('condition="${{ !cancelled() && steps.publier_les_durees.outcome != \'skipped\' }}")',
                                           'condition="always()")')],
    # relecture de Cowork du 21-11-2026 (pointe 5602b2271) : G9 et G10 gardent I-3 et le point 2 (b) du superviseur,
    # G11 et G12 gardent m-9 ; H1 à H5 sont SES façons de taire l'échec de la publication (I-4), jugées en JOUANT le pas
    "G9_journal_de_la_tache_non_depose": [('DUREES_PUBLIEES_DU_DEPOT + " " + JOURNAL_DE_LA_TACHE, VIDER_L_INDEX,',
                                          'DUREES_PUBLIEES_DU_DEPOT, VIDER_L_INDEX,')],
    "G10_index_non_vide": [('DUREES_PUBLIEES_DU_DEPOT + " " + JOURNAL_DE_LA_TACHE, VIDER_L_INDEX,',
                           'DUREES_PUBLIEES_DU_DEPOT + " " + JOURNAL_DE_LA_TACHE, "",')],
    "G11_commit_sans_garde": [('[skip ci]" \\\\\n            || { echo \\"::error::COMMIT IMPOSSIBLE — """ + reste + """ reste sur la machine jetable\\"; exit 1; }\n',
                              '[skip ci]"\n')],
    "G12_rebasage_laisse_en_plan": [('          done\n          git rebase --abort 2>/dev/null || true\n          echo "::error::POUSSEE REFUSEE """ + str(ESSAIS_DE_POUSSEE)',
                                    '          done\n          echo "::error::POUSSEE REFUSEE """ + str(ESSAIS_DE_POUSSEE)')],
    "H1_point_virgule_true": [('--publier-les-durees \\\\\n', '--publier-les-durees ; true \\\\\n')],
    "H2_ou_deux_points": [('--publier-les-durees \\\\\n', '--publier-les-durees || : \\\\\n')],
    "H3_echo_devant": [('          python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees',
                        '          echo python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees')],
    "H4_true_ou_devant": [('          python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees',
                           '          true || python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees')],
    "H5_commentaire": [('          python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees',
                        '          : # python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE" --publier-les-durees')],
}
# les deux conditions décidées, écrites ici une seconde fois à dessein (voir le ⑧ de `p7`)
CONDITION_DE_LA_PUBLICATION = ("${{ !cancelled() && steps.poser_le_code.outcome == 'success' && "
                               "steps.certifier.outcome != 'skipped' }}")
CONDITION_DU_DEPOT_DES_DUREES = "${{ !cancelled() && steps.publier_les_durees.outcome != 'skipped' }}"
ATTENDU = {"F1_pas_retire": "P7 a)", "F2_option_retiree": "P7 a)", "F3_fichier_non_pousse": "P7 b)",
           "F4_echec_masque": "P7 c)", "F5_chemin_divergent": "P7 b)",
           "G1_condition_jamais_vraie": "P7 a) la condition", "G2_journaux_de_la_nuit_non_repris": "P7 a) la publication",
           "G3_echec_de_publication_rendu_vert": "P7 c)", "G4_ou_vrai_silencieux": "P7 c)",
           "G5_durees_avec_le_certificat": "P7 b) le dépôt du certificat", "G6_durees_deposees_avant": "P7 a)",
           "G7_durees_signees_certification": "P7 b) le dépôt des durées signe",
           "G8_depot_des_durees_sans_condition": "P7 b) la condition",
           "G9_journal_de_la_tache_non_depose": "P7 b) le dépôt des durées n'ajoute pas",
           "G10_index_non_vide": "P7 b) l'index", "G11_commit_sans_garde": "P7 b) commit",
           "G12_rebasage_laisse_en_plan": "P7 b) rebasage",
           "H1_point_virgule_true": "P7 c) joué", "H2_ou_deux_points": "P7 c) joué", "H3_echo_devant": "P7 c) joué",
           "H4_true_ou_devant": "P7 c) joué", "H5_commentaire": "P7 c) joué",
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

    ① RÔLE — Prouver que la tâche finale de la nuit refait et pousse le fichier des durées (A-969), sans jamais
      empêcher le dépôt du certificat ni taire un échec.
    ② CONTEXTE D'APPEL — `main`, en Z0 avec le fabricant de la racine, puis une fois par sabotage du fabricant.
    ③ ENTRÉE — `F` : le fabricant chargé (son texte CERTIFICATION, DUREES_PUBLIEES_DU_DEPOT, IDENTITE_DES_DUREES) ·
      `C` : le certificateur sain (son DUREES_PUBLIEES).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes (textes commençant par « P7 a) », « P7 b) » ou « P7 c) »).
      [rend: 1]
    ⑥ TRAITEMENT — ① isoler le job « reunir » (de « \\n  reunir:\\n » à la fin) et le couper en pas (« - name: » à six
      espaces) · ② a) un pas de chaque, DANS CET ORDRE : la réunion (« --reunir »), le dépôt du certificat
      (« Deposer au depot prive »), la publication (« CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE"
      --publier-les-durees »), le dépôt des durées (« Deposer les durees au depot prive ») ; la publication porte
      la ligne « git checkout FETCH_HEAD -- rapports/journal_du_circuit » AVANT son appel, et sa ligne « if: » est
      EXACTEMENT celle de CONDITION_DE_LA_PUBLICATION · ③ b) le chemin du fabricant, « / » remplacé par le séparateur
      du système, égale DUREES_PUBLIEES du certificateur ; la ligne « git add » du dépôt des durées n'ajoute QUE ce
      chemin, celle du dépôt du certificat ne le porte PAS ; l'identité du dépôt des durées n'est pas
      « certification-publique » ; la ligne « if: » du dépôt des durées est EXACTEMENT CONDITION_DU_DEPOT_DES_DUREES ·
      ④ c) le pas de publication : ni « continue-on-error », ni « || true », ni « exit 0 » ; ses commandes (une ligne
      finie par « \\ » se lit avec la suivante) finissent CHACUNE par « || { echo "::error::…"; exit 1; } ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 21-11-2026 à 16h09 (« 1 ») : le circuit de nuit refait le fichier chaque nuit,
      pour des prévisions toujours fondées sur des durées récentes. Sans ce pas, rien ne le refaisait (A-968).
      Relecture de Cowork du 21-11-2026 (pointe 33915014d) : I-1 — dans un même commit, un conflit sur ce fichier
      empêchait le dépôt du certificat (d'où l'ordre et l'identité) ; I-2 — la forme précédente de c) ne cherchait
      que la PRÉSENCE de « ::error:: » et « exit 1 » quelque part dans le pas : un « exit 0 » ou un « || true » sur la
      seconde commande restait vert (G3, G4), comme une condition jamais vraie (G1) ou des journaux non repris (G2).
      Les deux lignes « if: » sont écrites ICI une seconde fois, à dessein : l'épreuve confronte le fabricant à ce
      qui a été décidé, une condition retournée ne se voit pas autrement.
    ⑨ CE QUI CLOCHE — Lecture du texte seulement : l'exécution par GitHub n'est pas prouvée ici. Une commande écrite
      sur plusieurs lignes SANS « \\ » (un « if … fi » de plusieurs lignes) serait lue ligne par ligne et refusée :
      refus à tort, mais à voix haute.
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
    rangs = {"réunion": [i for i, p in enumerate(pas) if "--reunir" in p],
             "dépôt du certificat": [i for i, p in enumerate(pas) if p.startswith("Deposer au depot prive\n")],
             "publication": [i for i, p in enumerate(pas) if appel in p],
             "dépôt des durées": [i for i, p in enumerate(pas) if p.startswith("Deposer les durees au depot prive\n")]}
    if any(len(r) != 1 for r in rangs.values()) or [r[0] for r in rangs.values()] != sorted(r[0] for r in rangs.values()):
        faux.append(f"P7 a) rangs des pas {rangs} : attendu un pas de chaque, dans cet ordre")
        return faux
    pub, dep, dur = (pas[rangs[n][0]] for n in ("publication", "dépôt du certificat", "dépôt des durées"))
    lignes_pub = [l.strip() for l in pub.split("\n")]
    reprise = [i for i, l in enumerate(lignes_pub) if l.startswith("git checkout FETCH_HEAD -- rapports/journal_du_circuit")]
    i_appel = [i for i, l in enumerate(lignes_pub) if appel in l]
    if len(reprise) != 1 or not reprise[0] < i_appel[0]:
        faux.append("P7 a) la publication ne reprend pas, avant son appel, les journaux de la nuit "
                    "(« git checkout FETCH_HEAD -- rapports/journal_du_circuit ») : durées en retard d'une nuit")
    if "if: " + CONDITION_DE_LA_PUBLICATION not in lignes_pub:
        faux.append(f"P7 a) la condition de la publication n'est pas « {CONDITION_DE_LA_PUBLICATION} » : "
                    f"{[l for l in lignes_pub if l.startswith('if:')]}")
    chemin = F.DUREES_PUBLIEES_DU_DEPOT
    if chemin.replace("/", os.sep) != C.DUREES_PUBLIEES:
        faux.append(f"P7 b) chemin du fabricant {chemin} ≠ celui du certificateur {C.DUREES_PUBLIEES}")
    ajout = lambda p: [l.strip() for l in p.split("\n") if l.strip().startswith("git add ")]
    if ajout(dur) != [f"git add {chemin} {F.JOURNAL_DE_LA_TACHE} \\"] or not F.JOURNAL_DE_LA_TACHE.startswith(
            "rapports/journal_du_circuit/circuit_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${GITHUB_JOB}"):
        faux.append(f"P7 b) le dépôt des durées n'ajoute pas {chemin} et le journal de la tâche, seuls : {ajout(dur)}")
    l_dur = [l.strip() for l in dur.split("\n")]
    i_add = [i for i, l in enumerate(l_dur) if l.startswith("git add ")]
    if "git reset -q \\" not in l_dur[:i_add[0] if i_add else 0]:
        faux.append("P7 b) l'index n'est pas vidé (« git reset -q ») avant l'ajout : les journaux repris de main par la "
                    "publication partiraient dans le commit des durées")
    for nom_du_pas, texte_du_pas in (("dépôt du certificat", dep), ("dépôt des durées", dur)):
        lignes = [l.strip() for l in texte_du_pas.split("\n")]
        i_c = [i for i, l in enumerate(lignes) if l.startswith("git commit ")]
        if len(i_c) != 1 or not lignes[i_c[0]].endswith("\\") or not re.match(
                r'\|\| \{ echo "::error::[^"]+"; exit 1; \}$', lignes[i_c[0] + 1]):
            faux.append(f"P7 b) commit sans garde dans le {nom_du_pas} : il tomberait sans dire pourquoi (m-9)")
        i_err = [i for i, l in enumerate(lignes) if l.startswith('echo "::error::POUSSEE REFUSEE')]
        if len(i_err) != 1 or lignes[i_err[0] - 1] != "git rebase --abort 2>/dev/null || true":
            faux.append(f"P7 b) rebasage laissé en plan par le {nom_du_pas} après ses essais (m-9)")
    if any(chemin in l or "$DUREES" in l for l in ajout(dep)):
        faux.append(f"P7 b) le dépôt du certificat ajoute aussi les durées : {ajout(dep)} — un conflit sur ce fichier "
                    "empêcherait le dépôt du certificat")
    if "certification-publique" in dur or F.IDENTITE_DES_DUREES == "certification-publique":
        faux.append("P7 b) le dépôt des durées signe « certification-publique » : il passerait pour un certificat")
    if "if: " + CONDITION_DU_DEPOT_DES_DUREES not in [l.strip() for l in dur.split("\n")]:
        faux.append(f"P7 b) la condition du dépôt des durées n'est pas « {CONDITION_DU_DEPOT_DES_DUREES} »")
    run = pub.split("run: |\n", 1)[1] if "run: |\n" in pub else ""
    commandes, en_cours = [], ""
    for l in run.split("\n"):
        en_cours += " " + l.strip()
        if not l.rstrip().endswith("\\"):
            if en_cours.strip():
                commandes.append(en_cours.replace("\\ ", "").strip())
            en_cours = ""
    sans_garde = [c for c in commandes if not re.search(r'\|\| \{ echo "::error::[^"]+"; exit 1; \}$', c)]
    interdits = [m for m in ("continue-on-error", "|| true", "exit 0") if m in pub]
    if not commandes or sans_garde or interdits:
        faux.append(f"P7 c) le pas de publication peut taire un échec : commandes sans « || {{ echo \"::error::…\"; "
                    f"exit 1; }} » {[c[:60] for c in sans_garde]}, interdits présents {interdits}")
    faux += jouer_la_publication(run)
    return faux


def jouer_la_publication(run):
    """Joue le bloc « run » du pas de publication par « bash -e », avec un faux git et un faux certificateur.

    ① RÔLE — Juger le pas de publication par ce qu'il FAIT, et non par la forme de son texte (I-4 de la relecture de
      Cowork du 21-11-2026, pointe 5602b2271).
    ② CONTEXTE D'APPEL — `p7`, une fois par fabricant jugé.
    ③ ENTRÉE — `run` : le texte du bloc « run: | » du pas, tel que le fabricant l'écrit (indenté).
    ④ CONDITIONS D'ENTRÉE — bash et python3 sur la machine (la nuit tourne sous Linux).
    ⑤ SORTIE — UNE valeur : la liste des fautes (textes commençant par « P7 c) joué »).
      [rend: 1]
    ⑥ TRAITEMENT — Dans un dossier jetable : un « git » qui note son appel et rend GIT_CODE, posé en tête du PATH ; un
      programmes/CERTIFIER_LA_VERSION.py qui note son appel et ses arguments et rend CERT_CODE. Trois jeux, chacun par
      « bash -e » (ce que fait programmes/ETAPE_MUETTE.py, le shell des pas du job) : ① git 0, certificateur 0 → code 0
      ET le certificateur appelé avec « --publier-les-durees » · ② git 0, certificateur 1 → code non nul ET la ligne
      « ::error::DUREES DES EPREUVES NON PUBLIEES » · ③ git 1 → code non nul ET « ::error::JOURNAUX DE LA NUIT
      ILLISIBLES », sans appel du certificateur.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La forme précédente de c) découpait le pas en lignes et vérifiait leur FIN : « ; true », « || : »,
      « echo » ou « true || » devant l'appel, « : # » le rendaient vert alors que la publication avait échoué ou
      n'avait pas eu lieu (mesuré par Cowork, H1 à H5). Jouer le pas juge une propriété — il dit son échec, il rend
      non nul — qui ferme ces formes et leurs cousines d'un coup.
    ⑨ CE QUI CLOCHE — Les faux ne reproduisent pas le vrai git ni le vrai certificateur : une commande qui ne
      dépendrait que de leur sortie réelle n'est pas jugée. Le pas est joué par bash, pas par ETAPE_MUETTE lui-même.
    ⑩ EFFET — Un dossier jetable, effacé.
    ⑪ TERMINAISON — Chaque jeu est borné à 30 s ; un dépassement est une faute.
      [sort: non]
    """
    import subprocess
    import textwrap
    faux = []
    d = tempfile.mkdtemp(prefix="durees_pas_joue_")
    try:
        os.makedirs(os.path.join(d, "bin"))
        os.makedirs(os.path.join(d, "programmes"))
        faux_git = os.path.join(d, "bin", "git")
        open(faux_git, "w", encoding="utf-8").write('#!/bin/sh\necho "FAUX GIT $*"\nexit "${GIT_CODE:-0}"\n')
        os.chmod(faux_git, 0o755)
        open(os.path.join(d, "programmes", "CERTIFIER_LA_VERSION.py"), "w", encoding="utf-8").write(
            "import os, sys\nprint('FAUX CERTIFICATEUR APPELE', ' '.join(sys.argv[1:]))\n"
            "sys.exit(int(os.environ.get('CERT_CODE', '0')))\n")
        script = os.path.join(d, "pas.sh")
        open(script, "w", encoding="utf-8").write(textwrap.dedent(run))
        jeux = (("① git 0, certificateur 0", "0", "0", lambda c, o: c == 0 and "--publier-les-durees" in "".join(
                    l for l in o.splitlines() if l.startswith("FAUX CERTIFICATEUR APPELE"))),
                ("② certificateur 1", "0", "1", lambda c, o: c != 0 and "::error::DUREES DES EPREUVES NON PUBLIEES" in o),
                ("③ git 1", "1", "0", lambda c, o: c != 0 and "::error::JOURNAUX DE LA NUIT ILLISIBLES" in o
                    and "FAUX CERTIFICATEUR APPELE" not in o))
        for nom, git_code, cert_code, juste in jeux:
            env = dict(os.environ, PATH=os.path.join(d, "bin") + os.pathsep + os.environ.get("PATH", ""),
                       GIT_CODE=git_code, CERT_CODE=cert_code, GITHUB_WORKSPACE=d)
            try:
                r = subprocess.run(["bash", "-e", script], cwd=d, env=env, capture_output=True, text=True, timeout=30)
                code, sortie = r.returncode, r.stdout + r.stderr
            except subprocess.TimeoutExpired:
                code, sortie = None, "plus de 30 s"
            if not juste(code, sortie):
                faux.append(f"P7 c) joué, jeu {nom} : code {code}, sortie {sortie.strip().splitlines()[-2:]} — le pas tait "
                            "un échec ou ne publie pas")
    finally:
        shutil.rmtree(d, ignore_errors=True)
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
