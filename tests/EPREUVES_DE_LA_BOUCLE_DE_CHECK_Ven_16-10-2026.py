#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_BOUCLE_DE_CHECK — Ven 16-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/BOUCLE_DE_CHECK.py dit le bon événement dans chaque situation de la boucle de check —
  tour à faire, note refusée, chacun des arrêts, erreur —, qu'il ne touche pas au clone qu'il guette, et que chacune de
  ses gardes a des dents.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py) ; à la main avant toute
  livraison qui touche ce programme (R-731) :
  python3 tests/EPREUVES_DE_LA_BOUCLE_DE_CHECK_Ven_16-10-2026.py <racine> [--saboter | --saboter=S1,S2,…]
  Ses sabotages, trop longs pour la nuit (plus d'une heure), se jouent hors de la nuit par
  tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py, qui en écrit le relevé ; la nuit vérifie ce relevé et refait quelques
  essais (tests/LANCEMENT_DES_EPREUVES.json, « series_hors_de_la_nuit »).
③ ENTRÉE — La racine du dépôt (le programme est pris dans son programmes/).
④ CONDITIONS D'ENTRÉE — git sur la machine. Rien d'autre de la racine que le programme de la boucle : les cas sur la
  vraie relecture de Cowork du 16-10-2026 (B19, B19bis, B19ter) vivent depuis le 17-10-2026 dans
  tests/EPREUVES_DE_LA_VERIFICATION_DES_NOTES_Sam_17-10-2026.py.
⑤ SORTIE — Le code de sortie : 0 si tous les cas donnent la réponse attendue et, avec --saboter, si chaque sabotage en
  fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus, ou si un cas
  n'a pas pu être monté (une commande git qui écrit le dépôt d'essai a échoué : MontageImpossible).
  [rend: 1]
⑥ TRAITEMENT — Un faux dépôt distant (git init --bare), un clone qui écrit les notes comme le feraient le Chat et
  Cowork, un clone guetté, la copie propre au programme, et un faux garde-fou qui accepte une note portant « ACCEPTE »
  et refuse les autres avec le motif « MOTIF FAUX » ; il nomme le registre et programmes/LIRE_LE_CODE.py, comme le vrai.
  Les cas : B1 aucune version → ARRÊT · B2 deux versions → ARRÊT · B3 ma note est la plus récente → rien · B4 tour,
  journal sans « BOUCLE LANCÉE » → ARRÊT · B5 tour lancé, note acceptée → TOUR À FAIRE, « 0 allers-retours sur 10 » ·
  B6 note refusée → NOTE REFUSÉE et son motif · B7 dix réponses de Cowork après le lancement → ARRÊT BUDGET · B8 dix
  réponses, « BOUCLE CONTINUÉE », deux réponses → TOUR, « 2 allers-retours » · B9 « RIEN DE NEUF » en tête → ARRÊT ·
  B10 « **ARRÊT — DÉCISION DE JEAN-LUC** » → ARRÊT · B11 ma note a plus de 3 heures, rien de l'autre → ARRÊT SILENCE ;
  2 heures → rien · B12 la note de l'autre est plus récente, 5 heures après → TOUR, jamais SILENCE · B13 le garde-fou
  de la version diffère → « ATTENTION » ; B13bis un programme qu'il ne nomme pas diffère → pas d'« ATTENTION » ·
  B14 garde-fou absent → ERREUR, code 2 · B15 la ligne du journal a la forme fixe ; le journal est créé avec son
  en-tête · B16 lancé seul, le clone guetté n'est pas touché (mêmes références, même HEAD, même liste de copies, un
  fichier non commité intact) alors que le distant a avancé · B17 côté Cowork : la note attendue est celle du Chat ·
  B18 distant injoignable → ERREUR, code 2 · B19, B19bis, B19ter : voir l'épreuve de la vérification des notes · B20 lancé seul sur un tour prêt : « GUETTE » puis « TOUR À FAIRE », code 0 ·
  B21 « --noter » sans « --texte » → code 2 · B22 trois erreurs de suite → code 2 · B23 une réponse arrivée pendant que
  la surveillance était arrêtée est vue à la relance · B24 erreur, regard sain, deux erreurs, événement → code 0 (le
  compte d'erreurs repart de zéro) · B25 la version supprimée au distant → ARRÊT aucune version · B26 un journal hérité
  de la version officielle ne lance pas la boucle · B27 « RIEN DE NOUVEAU », « ARRÊT - … », « Arrêt — … »,
  « ARRET – … » → ARRÊT · B28 après un rebase poussé de force, celui qui a déjà répondu ne relit pas · B29 dix réponses
  dont une seule sans sa ligne au journal → ARRÊT BUDGET · B30 la note de l'autre supprimée → ARRÊT NOTE SUPPRIMÉE ·
  B31 un fichier que le garde-fou nomme a changé → « ATTENTION » · B32 une copie jetable laissée par un arrêt brutal est
  retirée au regard suivant · B49 la copie jetable d'un autre programme encore en marche est gardée, celle d'un
  programme arrêté est retirée · B50 la copie que le programme crée porte son propre numéro (16-10-2026 vers 23h20 :
  deux paquets de la série, joués en même temps sur un même clone, effaçaient la copie l'un de l'autre) · B51 quatre
  programmes vérifient 25 fois chacun, en même temps, sur un même dépôt : aucun échec, aucune copie restante (git
  ne supporte pas deux créations ou retraits de copies simultanés : le verrou des copies les sépare) · B52 la copie
  de ce programme-ci et les numéros 0 et 1 comptent pour arrêtés ; un refus du système compte pour vivant · B53 chaque
  commande « git worktree » du programme trouve le verrou des copies déjà tenu (sans hasard, contrairement à B51) ·
  B54 un arrêt reçu juste après la prise du verrou fait sortir le programme en moins de 30 secondes, sans copie
  restante (il gelait sur son propre verrou) · B55 un arrêt reçu entre la prise du verrou et le bloc qui le libère
  fait sortir le programme en moins de 30 secondes · B57 une copie verrouillée « initializing » d'un programme arrêté
  est retirée et comptée · B58 dans le dossier temporaire, le dossier vide d'un programme arrêté est effacé, celui d'un
  programme vivant et celui de ce programme-ci sont gardés (relecture indépendante, tour 10) · B56 un cas dont le
  montage échoue est déclaré « MONTAGE IMPOSSIBLE » (cassure N de Cowork, 17-10-2026). Avec --saboter : chaque garde du programme retirée, une à la fois, dans une copie.
⑦ UNITÉ — Des codes de sortie et des secondes (heures des commits fixées par GIT_COMMITTER_DATE).
⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 19h28 : la boucle de check devient un programme ; s'il se trompe, la
  boucle relit de trop ou s'arrête sans rien dire. Les cas B23 à B32 viennent de la relecture indépendante du même
  soir, qui a cassé la première version. Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une
  preuve (R-731).
⑨ CE QUI CLOCHE — L'attente de `guetter` entre deux regards n'est éprouvée qu'à intervalle zéro. · Le signal d'arrêt de
  l'outil de surveillance n'est pas joué : B32 éprouve le nettoyage, pas le signal.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement du programme seul est borné à 60 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import multiprocessing
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0]) if _args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(RACINE, "programmes", "BOUCLE_DE_CHECK.py")
T0 = 1_800_000_000              # heure de départ des commits d'essai, en secondes depuis 1970
REGISTRE_D_ESSAI = "# REGISTRE\n\n# LE PROTOCOLE DE LIVRAISON\n\ngestes\n\n---\n\n### R-755\n\npièges\n\n### R-756\n\nautre\n"
PROCESSUS_EN_MEME_TEMPS = 4     # B51 : programmes qui vérifient en même temps sur un même dépôt
VERIFICATIONS_PAR_PROCESSUS = 25  # B51 : sans le verrou, 18 échecs sur 4 × 50 (relecture du 16-10-2026, 23h40)
FAUX_GARDE_FOU = ('import sys\nVOISIN = "LIRE_LE_CODE.py"   # comme le vrai ; AUTRE.py n est cité qu en commentaire\n'
                  't = open(sys.argv[1], encoding="utf-8").read()\n'
                  'if "--verifier" not in sys.argv:\n    print("pas de vérification"); sys.exit(3)\n'
                  'tete = "\\n".join(t.split("\\n")[:3]).lower()\n'
                  'if any(a.startswith("--attendu=") for a in sys.argv):\n    print("  rôle attendu : essai — lu : essai")\n'
                  'if "--attendu=relecture" in sys.argv and "porter la relecture" not in tete:\n'
                  '    print("  ❌ LIVRAISON REFUSÉE — 1 motif(s) :"); print("     · RÔLE ATTENDU : RELECTURE"); sys.exit(1)\n'
                  'if "--attendu=livraison" in sys.argv and "soumis à relecture" not in tete:\n'
                  '    print("  ❌ LIVRAISON REFUSÉE — 1 motif(s) :"); print("     · RÔLE ATTENDU : LIVRAISON"); sys.exit(1)\n'
                  'if "ACCEPTE" in t:\n    print("  ✅ validée et intacte"); sys.exit(0)\n'
                  'print("  ❌ LIVRAISON REFUSÉE — 1 motif(s) :"); print("     · MOTIF FAUX"); sys.exit(1)\n')
SABOTAGES = {
    "S1_budget_ignore": [("    if n >= BUDGET:\n", "    if False:\n")],
    "S2_continuee_ignoree": [('LANCEMENT = re.compile(r"^BOUCLE (LANCÉE|CONTINUÉE)\\b")',
                              'LANCEMENT = re.compile(r"^BOUCLE (LANCÉE)\\b")')],
    "S3_arret_ecrit_ignore": [("    if ecrit:\n", "    if False:\n")],
    "S4_refus_ignore": [("    if code != 0:\n        r = annoncer(\"refusée \"", "    if False:\n        r = annoncer(\"refusée \"")],
    "S5_silence_ignore": [("        if maintenant - mon_heure > SILENCE:\n", "        if False:\n")],
    "S6_tour_jamais_vu": [("    mon_tour = sien is not None and (mien is None", "    mon_tour = False and (mien is None")],
    "S7_boucle_non_lancee_admise": [("    if ligne is None:\n", "    if False:\n")],
    "S8_plusieurs_versions_admises": [("    if len(versions) > 1:\n", "    if False:\n")],
    "S9_garde_fou_change_tu": [("if garde_fou_change(depot, sien) else", "if False else")],
    "S10_branches_supprimees_gardees": [('"fetch", "-q", "--prune", "origin"', '"fetch", "-q", "origin"')],
    "S11_note_lue_hors_de_la_copie": [("cwd=copie, capture_output=True", "cwd=depot, capture_output=True")],
    "S12_erreurs_sans_fin": [("            if erreurs >= 3:\n", "            if erreurs >= 10 ** 9:\n")],
    "S13_forme_du_journal": [("Paris · {nom} · {commit[:7]} · ", "Paris - {nom} - {commit[:7]} - ")],
    "S14_fetch_ignore": [("    if code != 0:\n        return 2, f\"ERREUR · le fetch", "    if False:\n        return 2, f\"ERREUR · le fetch")],
    "S15_garde_fou_muet": [("    if code == 2:\n        return 2, f\"ERREUR · {branche}", "    if False:\n        return 2, f\"ERREUR · {branche}")],
    "S16_ordre_des_notes_ignore": [("(mien is None or est_ancetre(depot, mien, sien)\n", "(True\n")],
    "S17_journal_herite_compte": [("if x not in avant and LIGNE_DU_JOURNAL.match(x)", "if LIGNE_DU_JOURNAL.match(x)")],
    "S18_graphies_non_normalisees": [('"", normaliser(nue).lstrip(', '"", nue.lstrip(')],
    "S19_rien_de_nouveau_ignore": [("RIEN DE (NEUF|NOUVEAU)", "RIEN DE (NEUF)")],
    "S20_budget_compte_au_journal": [('f"{commits[0]}..origin/{branche}", "--", NOTE_DE_COWORK)',
                                      'f"{commits[0]}..origin/{branche}", "--", JOURNAL)')],
    "S21_note_supprimee_ignoree": [("    if note is None:\n        return annoncer(\"supprimée",
                                    "    if False:\n        return annoncer(\"supprimée")],
    "S22_voisins_du_garde_fou_ignores": [("    return sorted(vus)\n", "    return [GARDE_FOU]\n")],
    "S23_copies_laissees": [("            nettoyer_les_copies(depot)\n", "")],
    "S24_erreurs_jamais_remises_a_zero": [("        else:\n            erreurs = 0\n", "        else:\n            pass\n")],
    "S25_travail_dans_le_clone_guette": [("    depot, motif = copie_du_programme(clone, dossier)\n",
                                          "    depot, motif = clone, \"\"\n")],
    # second tour de la relecture indépendante, 16-10-2026 vers 20h40
    "S26_fusion_sans_horloge": [("\n                                     or (not est_ancetre(depot, sien, mien) and son_heure > mon_heure))",
                                 ")")],
    "S27_notes_concurrentes_ignorees": [("    if sien and mien and (sien == mien or", "    if False and (sien == mien or")],
    "S28_ma_note_jamais_controlee": [("        if code != 0:\n            r = annoncer(\"ma note refusée \"",
                                      "        if False:\n            r = annoncer(\"ma note refusée \"")],
    "S29_memoire_ignoree": [('        if cle in mem["annonces"]:\n            return None\n', '        if False:\n            return None\n')],
    "S30_arret_au_milieu_de_la_ligne": [("        if ARRET_MARQUE.match(n) and not", "        if ARRET_MARQUE.search(n) and not")],
    "S31_marques_d_arret_etroites": [("|TOURNE EN ROND|SILENCE)", ")")],
    "S32_role_non_transmis": [('"--verifier", f"--attendu={ATTENDU[fichier]}"]', '"--verifier"]')],
    "S33_notes_heritees_comptees": [('    plage = f"{base}..origin/{branche}" if base else "origin/" + branche\n',
                                     '    plage = "origin/" + branche\n')],
    "S34_adresse_figee": [('    git(dossier, "remote", "set-url", "origin", adresse)\n    for cle in', '    for cle in')],
    "S35_identifiants_non_recopies": [('            git(dossier, "config", cle, valeur)\n', '            pass\n')],
    "S36_sigterm_brutal": [("    signal.signal(signal.SIGTERM, _arret_propre)\n", "")],
    "S37_sans_verrou": [("        fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)\n", "        pass\n")],
    "S38_imports_ignores": [('                noms |= {a.name.split(".")[0] for a in n.names}\n', '                pass\n')],
    "S39_registre_ignore": [('    return (sections_lues_du_registre(lire_au_commit(depot, "origin/main", REGISTRE))\n'
                             '            != sections_lues_du_registre(lire_au_commit(depot, commit, REGISTRE)))\n',
                             '    return False\n')],
    "S40_registre_entier_compare": [('    return protocole + "\\n" + r755\n', '    return t\n')],
    # troisième tour de la relecture indépendante, 16-10-2026 vers 21h40
    "S41_marques_ouvertes": [("    if ARRET_MARQUE.match(n)", "    if re.match(r\"(RIEN DE (NEUF|NOUVEAU)|ARRET)\", n)")],
    "S42_silence_apres_refus_tu": [("        if r is None and maintenant - son_heure > SILENCE:\n", "        if False:\n")],
    "S43_silence_apres_mon_refus_tu": [("            if r:\n                return r\n        if maintenant",
                                        "            return r\n        if maintenant")],
    "S44_fin_de_boucle_dite_une_fois_pour_toutes": [
        ('annoncer("aucune version après " + (git(depot, "rev-parse", "origin/main")[1] or "?"),',
         'annoncer("aucune version",')],
    "S45_jeton_de_l_environnement_ecrit": [('git(clone, "config", "--local", "--get", cle)', 'git(clone, "config", "--get", cle)')],
    "S46_erreur_gardee_en_memoire": [('            del mem["verifiees"][cle]\n', '')],
    # quatrième tour de la relecture indépendante, 16-10-2026 vers 22h
    "S47_verdict_de_l_autre_recalcule": [('    if cle not in mem["verifiees"]:\n        code, motif = controler(depot, sien, sa_note)\n',
                                          '    if True:\n        code, motif = controler(depot, sien, sa_note)\n')],
    "S48_recu_du_role_ignore": [("        if not any(x.startswith(RECU_DU_ROLE) for x in lignes):\n", "        if False:\n")],
    "S50_reserve_ignoree": [('        if ARRET_MARQUE.match(n) and not (n.startswith("RIEN DE") and RESERVE.search(n)):\n',
                             "        if ARRET_MARQUE.match(n):\n")],
    "S51_reserve_sur_tous_les_arrets": [('not (n.startswith("RIEN DE") and RESERVE.search(n))', "not RESERVE.search(n)")],
    "S49_guillemet_de_tete_garde": [('normaliser(nue).lstrip("«“\\" "))', 'normaliser(nue))')],
    # 16-10-2026 vers 23h20 : deux paquets de la série, en même temps sur un clone, effaçaient la copie l'un de l'autre
    "S52_copie_d_un_vivant_effacee": [("    if not m or int(m.group(1)) <= 1 or int(m.group(1)) == os.getpid():\n",
                                       "    if True:\n")],
    "S53_copie_sans_numero": [('d = tempfile.mkdtemp(prefix=f"{PREFIXE_DES_COPIES}{os.getpid()}_")',
                               "d = tempfile.mkdtemp(prefix=PREFIXE_DES_COPIES)")],
    # relecture indépendante du même soir, vers 23h40 : git lui-même ne supporte pas deux « worktree » simultanés
    "S54_copies_sans_verrou": [("                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)\n", "")],
    # tour 9 de la même relecture : un arrêt juste après la prise du verrou gelait le programme sur son propre verrou
    "S58_verrou_garde_sur_interruption": [("    except BaseException:\n        f.close()\n        raise\n",
                                           "    except BaseException:\n        raise\n")],
    # tour 10 de la relecture indépendante, 17-10-2026
    "S60_un_seul_force": [('                code, _ = git(depot, "worktree", "remove", "--force", "--force", chemin)',
                           '                code, _ = git(depot, "worktree", "remove", "--force", chemin)')],
    "S61_compte_sans_le_code": [("                n += code == 0\n", "                n += 1\n")],
    "S62_dossiers_vides_gardes": [("    for nom in os.listdir(dossier):\n", "    for nom in []:\n")],
    "S63_ma_copie_en_cours_effacee": [("        if (m and int(m.group(1)) != os.getpid() and", "        if (m and")],
    "S59_verrou_repris_par_son_detenteur": [("        if verrou is not None:          # interrompu", "        if False:          # interrompu")],
    "S55_propre_copie_gardee": [(" or int(m.group(1)) == os.getpid():", ":")],
    "S56_refus_du_systeme_vaut_mort": [("    except PermissionError:\n        return True\n",
                                        "    except PermissionError:\n        return False\n")],
    "S57_numeros_0_et_1_admis": [("int(m.group(1)) <= 1 or ", "")],
}


def charger(chemin):
    """Charge le programme depuis `chemin` et le rend.

    ① RÔLE — Avoir le programme vrai ou saboté. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`. ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le module (définitions seulement). ⑪ TERMINAISON — Rend la
    main. [sort: non]
    """
    sp = importlib.util.spec_from_file_location("BOUCLE_%d" % id(chemin), chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


class MontageImpossible(Exception):
    """Une commande git du montage a échoué hors d'un dossier du programme : le cas n'a pas été préparé, il ne juge rien.

    ① RÔLE — Séparer « le programme a mal répondu » de « le cas n'a pas pu être monté ». ② CONTEXTE D'APPEL — Levée
    par `g` et par `lancer_le_montage` ; reçue par `cas`. ③ ENTRÉE — Le message : la commande et son code. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — — [rend: rien] ⑥ TRAITEMENT — — ⑦ UNITÉ — — ⑧ POURQUOI — Cassure N de Cowork, 17-10-2026 : 14
    sabotages avaient « mordu » parce qu'un `git commit` du montage était refusé — l'épreuve s'était arrêtée, elle
    n'avait pas vu le sabotage. Classée par le DOSSIER et non par le nom de la commande : relecture indépendante du
    même jour, tour 11 — un rebase, une fusion ou un clone direct du montage échouaient comme le commit, par des voies
    non classées. ⑨ CE QUI CLOCHE — Une commande lancée dans la copie du programme (« copie_du_programme », ou une
    copie au préfixe du programme) reste une exception ordinaire même si elle prépare le cas : son échec peut être
    un vrai effet du sabotage (S25, B34). · Le clone guetté est un dossier du montage où un sabotage peut écrire
    (S25) : si une commande de l'épreuve y échoue à cause du sabotage, celui-ci sort « NE PEUT PAS ÊTRE JOUÉ » et la
    série rougit, au lieu de « mord » — l'erreur va dans le sens prudent (relecture indépendante, tour 12). ⑩ EFFET — —
    ⑪ TERMINAISON — — [sort: non]
    """


PROGRAMME = ("copie_du_programme", "boucle_de_check_copie_")   # les dossiers où travaille le programme éprouvé


def du_programme(chemin):
    """Dit si `chemin` est un dossier où travaille le programme éprouvé. [rend: 1] [sort: non]

    ① RÔLE — Séparer le montage de ce que fait le programme. ② CONTEXTE D'APPEL — `g`, `lancer_le_montage`.
    ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : vrai ou faux. ⑥ TRAITEMENT — un des
    morceaux du chemin commence par un nom de `PROGRAMME`. ⑦ UNITÉ — — ⑧ POURQUOI — Voir `MontageImpossible`.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
    """
    return any(morceau.startswith(PROGRAMME) for morceau in os.path.abspath(chemin).split(os.sep))


def lancer_le_montage(commande, **options):
    """Lance une commande git du montage hors de `g` ; son échec est un montage impossible. [rend: 1] [sort: non]

    ① RÔLE — Les quelques commandes du montage qui ne passent pas par `g` (un rebase qui garde ses dates d'auteur,
    un clone vers un dossier choisi). ② CONTEXTE D'APPEL — `Montage.copie`, B28, B35, B59. ③ ENTRÉE — `commande`
    et les options de subprocess.run. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le résultat de subprocess.run.
    ⑥ TRAITEMENT — subprocess.run, check=True ; CalledProcessError devient MontageImpossible, sauf dans un dossier du
    programme. ⑦ UNITÉ — — ⑧ POURQUOI — Relecture indépendante, tour 11 (17-10-2026). ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de la commande. ⑪ TERMINAISON — Rend la main ou lève.
    """
    try:
        return subprocess.run(commande, check=True, **options)
    except subprocess.CalledProcessError as e:
        if du_programme(commande[2] if commande[1:2] == ["-C"] else os.getcwd()):
            raise
        raise MontageImpossible(f"git {commande[3] if commande[1:2] == ['-C'] else commande[1]} : "
                                f"code {e.returncode}") from e


def g(dossier, *args, date=None):
    """Lance git dans `dossier` avec une identité et, si donnée, une heure de commit ; rend la sortie.

    ① RÔLE — Fabriquer les dépôts d'essai. ② CONTEXTE D'APPEL — Les fonctions de montage. ③ ENTRÉE — `dossier`,
    les mots de la commande, `date` en secondes. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la sortie standard.
    [rend: 1] ⑥ TRAITEMENT — subprocess.run, check=True. ⑦ UNITÉ — Secondes. ⑧ POURQUOI — L'heure fixée rend le
    silence éprouvable sans attendre. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Celui de la commande. ⑪ TERMINAISON — Lève si git
    échoue : CalledProcessError dans un dossier du programme (`du_programme`), MontageImpossible ailleurs. [sort: non]
    """
    env = dict(os.environ, GIT_AUTHOR_NAME="essai", GIT_AUTHOR_EMAIL="essai@exemple.invalid",
               GIT_COMMITTER_NAME="essai", GIT_COMMITTER_EMAIL="essai@exemple.invalid")
    if date is not None:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{date} +0000"
    try:
        return subprocess.run(["git", "-C", dossier, *args], capture_output=True, text=True, check=True,
                              env=env).stdout.strip()
    except subprocess.CalledProcessError as e:
        if du_programme(dossier):
            raise
        raise MontageImpossible(f"git {args[0] if args else ''} : code {e.returncode}") from e


class Montage:
    """Un faux distant, un clone qui écrit les notes, un clone guetté et la copie du programme.

    ① RÔLE — Mettre la boucle dans une situation voulue. ② CONTEXTE D'APPEL — `tour`, un montage par cas.
    ③ ENTRÉE — `d` : un dossier jetable. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — [rend: rien] ⑥ TRAITEMENT — main porte le
    faux garde-fou, le registre et LIRE_LE_CODE.py ; `ecrire` pousse des fichiers sur une branche à une heure donnée.
    ⑦ UNITÉ — Secondes. ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans `d`. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """

    def __init__(self, d):
        self.d = d
        self.origine = os.path.join(d, "origine.git")
        self.auteur = os.path.join(d, "auteur")
        self.guette = os.path.join(d, "guette")
        self.copie_du_programme = os.path.join(d, "copie_du_programme")
        g(d, "init", "-q", "--bare", "-b", "main", self.origine)      # par `g` : un échec est un montage impossible
        g(d, "clone", "-q", self.origine, self.auteur)
        g(self.auteur, "symbolic-ref", "HEAD", "refs/heads/main")
        self.ecrire("main", {"programmes/CONTROLER_MA_LIVRAISON.py": FAUX_GARDE_FOU,
                             "programmes/LIRE_LE_CODE.py": "import emp\nX = 1\n", "emp.py": "Z = 1\n",
                             "programmes/AUTRE.py": "Y = 1\n", "gouvernance/REGISTRE_REGLES.md": REGISTRE_D_ESSAI}, T0)

    def ecrire(self, branche, fichiers, date):
        """Pousse `fichiers` (None efface) sur `branche` à l'heure `date` ; rend le commit. [rend: 1] [sort: non]"""
        existe = bool(g(self.auteur, "branch", "--list", branche))
        if existe:
            g(self.auteur, "checkout", "-q", branche)
        elif branche != "main":                         # main naît au premier commit, sur la branche courante
            g(self.auteur, "checkout", "-q", "-b", branche, "main")
        for c, t in fichiers.items():
            p = os.path.join(self.auteur, c)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            if t is None:
                os.remove(p)
            else:
                open(p, "w", encoding="utf-8").write(t)
        g(self.auteur, "add", "-A")
        g(self.auteur, "commit", "-q", "--allow-empty", "-m", "note", date=date)
        g(self.auteur, "push", "-q", "-f", "origin", branche)
        return g(self.auteur, "rev-parse", "HEAD")

    def copie(self):
        """Clone le distant pour le côté guetté, si ce n'est fait, et rend le chemin du clone guetté. [rend: 1] [sort: non]"""
        if not os.path.isdir(self.guette):
            lancer_le_montage(["git", "clone", "-q", self.origine, self.guette], capture_output=True)
        return self.guette


def journal(*lignes):
    """Rend un journal de boucle avec ces lignes (qui, texte). [rend: 1] [sort: non]"""
    return "# JOURNAL\n\n" + "".join(f"- 2026-10-16 19h{i:02d} Paris · {qui} · abc{i:04d} · {t}\n"
                                     for i, (qui, t) in enumerate(lignes))


LANCE = ("Chat", "BOUCLE LANCÉE · essai")


def note_du_chat(texte):
    """Une note du Chat qui déclare son rôle. [rend: 1] [sort: non]"""
    return "DÉCIDÉ · Rôle : porter le travail soumis à relecture.\n" + texte


def note_de_cowork(texte):
    """Une note de Cowork qui déclare son rôle. [rend: 1] [sort: non]"""
    return "DÉCIDÉ · Rôle : porter la relecture de celui qui n'a pas produit.\n" + texte


ACCEPTE = note_de_cowork("RELU\nACCEPTE\n")


def tour(module):
    """Joue tous les cas avec le programme à `module` ; rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `module` : le chemin du programme à éprouver. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms des cas faux. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête, ⑥.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Dépôts jetables.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    B = charger(module)
    faux = []

    def cas(nom, fonction):
        d = tempfile.mkdtemp(prefix="boucle_epreuve_")
        try:
            ok = fonction(Montage(d))
        except MontageImpossible as e:                  # le cas n'a pas été monté : il ne juge rien (cassure N)
            ok = False
            nom = f"{nom} (MONTAGE IMPOSSIBLE : {e})"
        except Exception as e:                          # un cas qui lève est faux, et dit pourquoi
            ok = False
            # le type seul, jamais le message : il porte des chemins jetables, et un essai refait la nuit doit
            # rendre la même ligne, mot pour mot (cassure N de Cowork, 17-10-2026)
            nom = f"{nom} (levé : {type(e).__name__})"
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if not ok:
            faux.append(nom)

    def regard(m, cote="chat", maintenant=T0 + 600):
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        return B.un_regard(depot, cote, maintenant)

    def debut(r, code, mot):
        return r is not None and r[0] == code and r[1].startswith(mot)

    def lancee(m, quand=T0 + 5, note=note_du_chat("ACCEPTE · ma note\n")):
        """Le Chat lance la boucle : sa ligne au journal et sa note. [rend: 1] [sort: non]"""
        return m.ecrire("travail-x", {"echanges/A_RELIRE.md": note, B.JOURNAL: journal(LANCE)}, quand)

    cas("B1", lambda m: debut(regard(m), 0, "ARRÊT · aucune version"))

    def b2(m):
        m.ecrire("travail-a", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        m.ecrire("travail-b", {"echanges/RELU.md": ACCEPTE}, T0 + 20)
        r = regard(m)
        return debut(r, 0, "ARRÊT · plusieurs versions") and "travail-a" in r[1] and "travail-b" in r[1]
    cas("B2", b2)

    def b3(m):
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 5)
        lancee(m, T0 + 10)
        return regard(m) is None
    cas("B3", b3)

    def b4(m):
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": "ma note\n"}, T0 + 5)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        return debut(regard(m), 0, "ARRÊT · BOUCLE NON LANCÉE")
    cas("B4", b4)

    def b5(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        r = regard(m)
        return debut(r, 0, "TOUR À FAIRE") and "1 allers-retours sur 10" in r[1]
    cas("B5", b5)

    def b5bis(m):
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 3)
        lancee(m, T0 + 5, note_du_chat("ma note sans le mot\n"))
        return debut(regard(m, cote="cowork"), 0, "NOTE REFUSÉE")
    cas("B5bis", b5bis)

    def b6(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": note_de_cowork("RELU\nrien\n")}, T0 + 10)
        r = regard(m)
        return debut(r, 0, "NOTE REFUSÉE") and "MOTIF FAUX" in r[1]
    cas("B6", b6)

    def dix_reponses(m, depart=10, avec_journal=True):
        for i in range(10):
            f = {"echanges/RELU.md": ACCEPTE + f"tour {i}\n"}
            m.ecrire("travail-x", f, T0 + depart + 2 * i)
            if i < 9:
                m.ecrire("travail-x", {"echanges/A_RELIRE.md": f"ma note {i}\n"}, T0 + depart + 2 * i + 1)

    def b7(m):
        lancee(m)
        dix_reponses(m)
        r = regard(m)
        return debut(r, 0, "ARRÊT · BUDGET") and " 10 allers-retours" in r[1]
    cas("B7", b7)

    def b8(m):
        lancee(m)
        dix_reponses(m)
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": "ma note après accord\n",
                               B.JOURNAL: journal(LANCE, ("Chat", "BOUCLE CONTINUÉE · accord de Jean-Luc de 21h00"))},
                 T0 + 100)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE + "a\n"}, T0 + 101)
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": "encore\n"}, T0 + 102)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE + "b\n"}, T0 + 103)
        r = regard(m)
        return debut(r, 0, "TOUR À FAIRE") and "2 allers-retours sur 10" in r[1]
    cas("B8", b8)

    def arret(texte):
        def f(m):
            lancee(m)
            m.ecrire("travail-x", {"echanges/RELU.md": texte}, T0 + 10)
            r = regard(m)
            return debut(r, 0, "ARRÊT · ÉCRIT PAR L'AUTRE CÔTÉ")
        return f
    cas("B9", arret(note_de_cowork("\n# RELU — RIEN DE NEUF — je propose de clore\nACCEPTE\n")))

    def b10(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": note_de_cowork("\n**ARRÊT — DÉCISION DE JEAN-LUC** : le seuil\nACCEPTE\n")},
                 T0 + 10)
        r = regard(m)
        return debut(r, 0, "ARRÊT · ÉCRIT PAR L'AUTRE CÔTÉ") and r[1].endswith("ARRÊT — DÉCISION DE JEAN-LUC : le seuil")
    cas("B10", b10)

    def b11(m):
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        lancee(m, T0 + 100)
        tard = regard(m, maintenant=T0 + 100 + 3 * 3600 + 1)
        tot = regard(m, maintenant=T0 + 100 + 2 * 3600)
        return debut(tard, 0, "ARRÊT · SILENCE") and tot is None
    cas("B11", b11)

    def b12(m):
        lancee(m, T0 + 10)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 100)
        return debut(regard(m, maintenant=T0 + 100 + 5 * 3600), 0, "TOUR À FAIRE")
    cas("B12", b12)

    def b13(m, fichier=B.GARDE_FOU, texte=FAUX_GARDE_FOU + "# changé\n", attendu=True):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE, fichier: texte}, T0 + 10)
        r = regard(m)
        return debut(r, 0, "TOUR À FAIRE") and (("ATTENTION : le garde-fou a changé" in r[1]) == attendu)
    cas("B13", b13)
    cas("B13bis", lambda m: b13(m, "programmes/AUTRE.py", "Y = 2\n", False))
    cas("B31", lambda m: b13(m, "programmes/LIRE_LE_CODE.py", "X = 2\n", True))
    cas("B31bis", lambda m: b13(m, "gouvernance/REGISTRE_REGLES.md", REGISTRE_D_ESSAI.replace("gestes", "geste ajouté"), True))
    cas("B31ter", lambda m: b13(m, "gouvernance/REGISTRE_REGLES.md", REGISTRE_D_ESSAI.replace("autre", "autre changé"), False))
    cas("B31quater", lambda m: b13(m, "emp.py", "Z = 2\n", True))

    def b14(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE, B.GARDE_FOU: None}, T0 + 10)
        return debut(regard(m), 2, "ERREUR")
    cas("B14", b14)

    def b15(m):
        cl = m.auteur
        quand = datetime(2026, 10, 16, 19, 40, tzinfo=ZoneInfo("Europe/Paris"))
        l1 = B.noter(cl, "chat", "655103cdeadbeef", "BOUCLE LANCÉE ·  le filet\n de la nuit", quand)
        l2 = B.noter(cl, "cowork", "a714f09cafe", "cassure M", quand)
        t = open(os.path.join(cl, B.JOURNAL), encoding="utf-8").read()
        return (l1 == "- 2026-10-16 19h40 Paris · Chat · 655103c · BOUCLE LANCÉE · le filet de la nuit"
                and t.startswith("FABRIQUÉ · Rôle :") and t.rstrip("\n").endswith(l2)
                and B.derniere_ligne_de_lancement(t.split("\n")) == l1)
    cas("B15", b15)

    def b16(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        m.copie()
        cl = m.guette
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE + "plus récent que le clone guetté\n"}, T0 + 20)
        etat = lambda: (g(cl, "rev-parse", "HEAD"), g(cl, "for-each-ref"), g(cl, "worktree", "list", "--porcelain"))
        avant = etat()
        os.makedirs(os.path.join(cl, "echanges"), exist_ok=True)
        open(os.path.join(cl, "travail_non_commite.txt"), "w", encoding="utf-8").write("x")
        r = subprocess.run([sys.executable, module, cl, "--cote", "chat", "--intervalle", "0",
                            "--copie", m.copie_du_programme], capture_output=True, text=True, timeout=60)
        return (r.returncode == 0 and "TOUR À FAIRE" in r.stdout and etat() == avant
                and open(os.path.join(cl, "travail_non_commite.txt")).read() == "x")
    cas("B16", b16)

    def b17(m):
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE, B.JOURNAL: journal(LANCE)}, T0 + 10)
        avant = regard(m, cote="cowork")
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": note_du_chat("ACCEPTE\n")}, T0 + 20)
        apres = regard(m, cote="cowork")
        return avant is None and debut(apres, 0, "TOUR À FAIRE")
    cas("B17", b17)

    def b18(m):
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "remote", "set-url", "origin", os.path.join(m.d, "absent.git"))
        return debut(B.un_regard(depot, "chat", T0), 2, "ERREUR · le fetch")
    cas("B18", b18)

    def b20(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        m.copie()
        r = subprocess.run([sys.executable, module, m.guette, "--cote", "chat", "--intervalle", "0",
                            "--copie", m.copie_du_programme], capture_output=True, text=True, timeout=60)
        l = r.stdout.strip().split("\n")
        return r.returncode == 0 and len(l) == 2 and l[0].startswith("GUETTE · Chat") and l[1].startswith("TOUR À FAIRE")
    cas("B20", b20)

    def b21(m):
        r = subprocess.run([sys.executable, module, m.auteur, "--cote", "chat", "--noter", "--commit", "abc"],
                           capture_output=True, text=True, timeout=60)
        return r.returncode == 2 and r.stdout.startswith("ERREUR")
    cas("B21", b21)

    def b22(m):
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(m.guette, "remote", "set-url", "origin", os.path.join(m.d, "absent.git"))   # recopiée au démarrage
        try:
            r = subprocess.run([sys.executable, module, m.guette, "--cote", "chat", "--intervalle", "0",
                                "--copie", depot], capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return False
        return r.returncode == 2 and "trois erreurs de suite" in r.stdout
    cas("B22", b22)

    def b23(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        premier = regard(m)
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": note_du_chat("ACCEPTE · ma réponse\n")}, T0 + 20)
        attente = regard(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE + "réponse pendant l'arrêt\n"}, T0 + 30)
        relance = regard(m)
        return debut(premier, 0, "TOUR À FAIRE") and attente is None and debut(relance, 0, "TOUR À FAIRE")
    cas("B23", b23)

    def b24(m):
        suite = iter([(2, "ERREUR · a"), None, (2, "ERREUR · b"), (2, "ERREUR · c"), (0, "TOUR À FAIRE · fin")])
        import io, contextlib
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            m.copie()
            code = B.guetter(m.guette, "chat", 0, m.copie_du_programme, regard=lambda *a: next(suite))
        return code == 0 and sortie.getvalue().strip().endswith("TOUR À FAIRE · fin")
    cas("B24", b24)

    def b25(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        vu = regard(m)
        g(m.auteur, "push", "-q", "origin", "--delete", "travail-x")
        return debut(vu, 0, "TOUR À FAIRE") and debut(regard(m), 0, "ARRÊT · aucune version")
    cas("B25", b25)

    def b26(m):
        m.ecrire("main", {B.JOURNAL: journal(LANCE, ("Cowork", "tour"))}, T0 + 2)
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": "ma note\n"}, T0 + 5)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        return debut(regard(m), 0, "ARRÊT · BOUCLE NON LANCÉE")
    cas("B26", b26)

    for i, texte in enumerate(("# RELU — RIEN DE NOUVEAU\nACCEPTE\n", "**ARRÊT - TOURNE EN ROND**\nACCEPTE\n",
                               "**Arrêt — décision de Jean-Luc**\nACCEPTE\n", "**ARRET – SILENCE**\nACCEPTE\n",
                               "**ARRÊT : DÉCISION DE JEAN-LUC**\nACCEPTE\n", "**ARRÊT—TOURNE EN ROND**\nACCEPTE\n",
                               "ARRÊT. Décision de Jean-Luc\nACCEPTE\n", "RIEN DE NEUF : je propose de clore\n",
                               "RIEN DE NOUVEAU.\n", "« RIEN DE NOUVEAU »\n", "Rien de neuf, je propose de clore\n",
                               "ARRÊT — DÉCISION : quel seuil ?\n", "ARRÊT — DÉCISION DE JEAN LUC : le seuil\n",
                               "ARRÊT — DÉCISION DE JEAN-LUC : garder le seuil à 3 %, mais sur quelle base ?\n",
                               "ARRÊT — TOURNE EN ROND : M revient, mais réparée autrement\n")):
        cas(f"B27.{i + 1}", arret(note_de_cowork("\n" + texte)))

    def b28(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        cowork_avant = regard(m, cote="cowork")
        m.ecrire("main", {"programmes/AUTRE.py": "Y = 3\n"}, T0 + 15)
        g(m.auteur, "checkout", "-q", "travail-x")
        env_date = T0 + 16
        lancer_le_montage(["git", "-C", m.auteur, "rebase", "-q", "main"], capture_output=True,
                       env=dict(os.environ, GIT_COMMITTER_NAME="essai", GIT_COMMITTER_EMAIL="essai@exemple.invalid",
                                GIT_COMMITTER_DATE=f"@{env_date} +0000"))
        g(m.auteur, "push", "-q", "-f", "origin", "travail-x")
        return cowork_avant is None and regard(m, cote="cowork") is None and debut(regard(m), 0, "TOUR À FAIRE")
    cas("B28", b28)

    def b29(m):
        lancee(m)
        dix_reponses(m)                                   # dix commits de la note de Cowork…
        m.ecrire("travail-x", {B.JOURNAL: journal(LANCE, *[("Cowork", "tour")] * 9)}, T0 + 60)   # …neuf lignes
        return debut(regard(m), 0, "ARRÊT · BUDGET")
    cas("B29", b29)

    def b30(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        m.ecrire("travail-x", {"echanges/RELU.md": None}, T0 + 20)
        return debut(regard(m), 0, "ARRÊT · NOTE SUPPRIMÉE")
    cas("B30", b30)

    def b32(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        reste = tempfile.mkdtemp(prefix=B.PREFIXE_DES_COPIES)
        g(depot, "worktree", "add", "-q", "--detach", os.path.join(reste, "depot"), "origin/main")
        r = B.un_regard(depot, "chat", T0 + 600)
        copies = [x for x in g(depot, "worktree", "list", "--porcelain").split("\n") if x.startswith("worktree ")]
        reste_la = os.path.isdir(reste)
        shutil.rmtree(reste, ignore_errors=True)
        return debut(r, 0, "TOUR À FAIRE") and len(copies) == 1 and not reste_la
    cas("B32", b32)

    # ── second tour de la relecture indépendante, 16-10-2026 vers 20h40 ──
    def b33(m):
        cl = m.copie()
        g(cl, "config", "http.extraheader", "X-Essai: 1")
        depot = B.copie_du_programme(cl, m.copie_du_programme)[0]
        entete = g(depot, "config", "--get", "http.extraheader")
        nouvelle = os.path.join(m.d, "origine_deplacee.git")
        shutil.copytree(m.origine, nouvelle)
        g(cl, "remote", "set-url", "origin", nouvelle)
        B.copie_du_programme(cl, m.copie_du_programme)
        return entete == "X-Essai: 1" and g(depot, "remote", "get-url", "origin") == nouvelle
    cas("B33", b33)

    def b34(m):
        lent = FAUX_GARDE_FOU.replace("import sys\n", "import sys, time\ntime.sleep(8)\n", 1)
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE, B.GARDE_FOU: lent}, T0 + 10)
        m.copie()
        p = subprocess.Popen([sys.executable, module, m.guette, "--cote", "chat", "--intervalle", "0",
                              "--copie", m.copie_du_programme], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        import time as _t
        _t.sleep(4)
        p.send_signal(signal.SIGTERM)
        p.wait(timeout=30)
        copies = [x for x in g(m.copie_du_programme, "worktree", "list", "--porcelain").split("\n")
                  if x.startswith("worktree ")]
        return len(copies) == 1
    cas("B34", b34)

    def b35(m):
        lancee(m)
        cw = os.path.join(m.d, "cowork")
        lancer_le_montage(["git", "clone", "-q", "-b", "travail-x", m.origine, cw], capture_output=True)
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": note_du_chat("ACCEPTE · correction pendant la relecture\n")},
                 T0 + 10)
        os.makedirs(os.path.join(cw, "echanges"), exist_ok=True)
        open(os.path.join(cw, B.NOTE_DE_COWORK), "w", encoding="utf-8").write(ACCEPTE)
        g(cw, "add", "-A")
        g(cw, "commit", "-q", "-m", "relu", date=T0 + 20)
        g(cw, "pull", "-q", "--no-rebase", "--no-edit", "origin", "travail-x", date=T0 + 21)
        g(cw, "push", "-q", "origin", "travail-x")
        return debut(regard(m), 0, "TOUR À FAIRE") and regard(m, cote="cowork") is None
    cas("B35", b35)

    def b35bis(m):
        m.ecrire("travail-x", {"echanges/A_RELIRE.md": note_du_chat("ACCEPTE\n"), "echanges/RELU.md": ACCEPTE,
                               B.JOURNAL: journal(LANCE)}, T0 + 10)
        return debut(regard(m), 0, "ARRÊT · NOTES CONCURRENTES")
    cas("B35bis", b35bis)

    def b36(m):
        lancee(m, note=note_du_chat("ma note sans le mot\n"))
        premier = regard(m)
        return debut(premier, 0, "MA NOTE REFUSÉE") and "MOTIF FAUX" in premier[1] and regard(m) is None
    cas("B36", b36)

    def b37(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": note_de_cowork(
            "\n**PRODUIT PAR : le Chat · relecture indépendante : 3 tours, le dernier « RIEN DE NOUVEAU »**\nACCEPTE\n")},
            T0 + 10)
        return debut(regard(m), 0, "TOUR À FAIRE")
    cas("B37", b37)

    def b38(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": "RELU sans rôle\nACCEPTE\n"}, T0 + 10)
        r = regard(m)
        return debut(r, 0, "NOTE REFUSÉE") and "RÔLE ATTENDU" in r[1]
    cas("B38", b38)

    def b39(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": note_de_cowork("\nRIEN DE NEUF — je propose de clore\n")}, T0 + 10)
        return debut(regard(m), 0, "ARRÊT · ÉCRIT") and regard(m) is None
    cas("B39", b39)

    def b40(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        import fcntl as _f
        tenu = open(os.path.join(depot, ".git", "boucle_de_check.verrou"), "w")
        _f.flock(tenu, _f.LOCK_EX | _f.LOCK_NB)
        try:
            r = subprocess.run([sys.executable, module, m.guette, "--cote", "chat", "--intervalle", "0",
                                "--copie", depot], capture_output=True, text=True, timeout=60)
        finally:
            tenu.close()
        return r.returncode == 2 and "tourne déjà" in r.stdout
    cas("B40", b40)

    def b41(m):
        m.ecrire("main", {"echanges/A_RELIRE.md": note_du_chat("ACCEPTE ancienne\n")}, T0 + 2)
        m.ecrire("main", {"echanges/RELU.md": ACCEPTE}, T0 + 3)
        m.ecrire("travail-y", {"programmes/AUTRE.py": "Y = 9\n"}, T0 + 10)
        loin = T0 + 200 * 3600
        return regard(m, maintenant=loin) is None and regard(m, cote="cowork", maintenant=loin) is None
    cas("B41", b41)

    # ── troisième tour de la relecture indépendante, 16-10-2026 vers 21h40 ──
    def b42(m):
        ok = True
        for texte in ("**Arrêt du circuit du soir le 15-10 :** la tâche de 20h n'a pas tourné.\nACCEPTE\n",
                      "Arrêt sur image : la passe ② ne mord pas.\nACCEPTE\n",
                      "## Rien de nouveau dans la passe ②, mais M casse\nACCEPTE\n", "ARRÊTÉ le 15-10\nACCEPTE\n",
                      "RIEN DE NOUVEAU, sauf une cassure M (bloquante) ci-dessous\nACCEPTE\n",
                      "Rien de neuf : sauf le point 3, qui casse\nACCEPTE\n"):
            d = tempfile.mkdtemp(prefix="boucle_b42_")
            try:
                mm = Montage(d)
                lancee(mm)
                mm.ecrire("travail-x", {"echanges/RELU.md": note_de_cowork("\n" + texte)}, T0 + 10)
                ok = ok and debut(regard(mm), 0, "TOUR À FAIRE")
            finally:
                shutil.rmtree(d, ignore_errors=True)
        return ok
    cas("B42", b42)

    def b43(m):
        lancee(m)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        vrai = B.verifier_la_note
        reponses = iter([(2, "le garde-fou n'a pas pu tourner"), (0, "✅ validée")])
        B.verifier_la_note = lambda *a: next(reponses)
        try:
            premier = B.un_regard(depot, "chat", T0 + 600)
            second = B.un_regard(depot, "chat", T0 + 600)
        finally:
            B.verifier_la_note = vrai
        return debut(premier, 2, "ERREUR") and second is None
    cas("B43", b43)

    def b44(m):
        lancee(m, note=note_du_chat("ma note sans le mot\n"))
        tot_chat, tot_cowork = regard(m), regard(m, cote="cowork")
        tard = T0 + 5 + 3 * 3600 + 60
        tard_chat, tard_cowork = regard(m, maintenant=tard), regard(m, cote="cowork", maintenant=tard)
        return (debut(tot_chat, 0, "MA NOTE REFUSÉE") and debut(tot_cowork, 0, "NOTE REFUSÉE")
                and debut(tard_chat, 0, "ARRÊT · SILENCE") and debut(tard_cowork, 0, "ARRÊT · SILENCE"))
    cas("B44", b44)

    def b45(m):
        m.ecrire("travail-a", {"programmes/AUTRE.py": "Y = 4\n"}, T0 + 10)
        g(m.auteur, "push", "-q", "origin", "--delete", "travail-a")
        premiere = regard(m)
        m.ecrire("main", {"programmes/AUTRE.py": "Y = 5\n"}, T0 + 20)
        m.ecrire("travail-b", {"programmes/AUTRE.py": "Y = 6\n"}, T0 + 30)
        pendant = regard(m)
        g(m.auteur, "push", "-q", "origin", "--delete", "travail-b")
        seconde = regard(m)
        return (debut(premiere, 0, "ARRÊT · aucune version") and pendant is None
                and debut(seconde, 0, "ARRÊT · aucune version"))
    cas("B45", b45)

    def b46(m):
        env = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "http.extraheader", "GIT_CONFIG_VALUE_0": "X-Jeton: fictif"}
        avant = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        try:
            depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        finally:
            for k, v in avant.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        return "fictif" not in open(os.path.join(depot, ".git", "config"), encoding="utf-8").read()
    cas("B46", b46)

    # ── quatrième tour de la relecture indépendante, 16-10-2026 vers 22h ──
    def b47(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": note_de_cowork("RELU\nrien\n")}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        vrai, appels = B.verifier_la_note, []
        B.verifier_la_note = lambda *a: (appels.append(a), vrai(*a))[1]
        try:
            premier = B.un_regard(depot, "chat", T0 + 600)
            suite = [B.un_regard(depot, "chat", T0 + 600 + k) for k in (60, 120)]
        finally:
            B.verifier_la_note = vrai
        return debut(premier, 0, "NOTE REFUSÉE") and suite == [None, None] and len(appels) == 1   # une seule fois, la sienne
    cas("B47", b47)

    def b48(m):
        ancien = FAUX_GARDE_FOU.replace('if any(a.startswith("--attendu=") for a in sys.argv):\n    print("  rôle attendu : essai — lu : essai")\n', "")
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE, B.GARDE_FOU: ancien}, T0 + 10)
        r = regard(m)
        return ancien != FAUX_GARDE_FOU and debut(r, 2, "ERREUR") and "ne sait pas contrôler le rôle" in r[1]
    cas("B48", b48)

    # ── 16-10-2026 vers 23h20 : la série des sabotages jouait deux paquets en même temps sur un même clone ; le ménage
    # de l'un effaçait la copie de l'autre, et le programme intact échouait. ──
    def b49(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        vivant = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        mort = subprocess.Popen([sys.executable, "-c", "pass"])
        mort.wait()
        dossiers = {}
        try:
            for nom, pid in (("vivant", vivant.pid), ("mort", mort.pid)):
                dossiers[nom] = tempfile.mkdtemp(prefix=f"{B.PREFIXE_DES_COPIES}{pid}_")
                g(depot, "worktree", "add", "-q", "--detach", os.path.join(dossiers[nom], "depot"), "origin/main")
            r = B.un_regard(depot, "chat", T0 + 600)
            garde_vivant = os.path.isdir(os.path.join(dossiers["vivant"], "depot"))
            garde_mort = os.path.isdir(dossiers["mort"])
        finally:
            vivant.kill()
            vivant.wait()
            for d in dossiers.values():
                g(depot, "worktree", "remove", "--force", os.path.join(d, "depot")) if os.path.isdir(
                    os.path.join(d, "depot")) else None
                shutil.rmtree(d, ignore_errors=True)
            g(depot, "worktree", "prune")
        return debut(r, 0, "TOUR À FAIRE") and garde_vivant and not garde_mort
    cas("B49", b49)

    def b50(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        vus, vrai = [], B.tempfile.mkdtemp
        B.tempfile.mkdtemp = lambda *a, **k: (vus.append(k.get("prefix")), vrai(*a, **k))[1]
        try:
            r = B.un_regard(depot, "chat", T0 + 600)
        finally:
            B.tempfile.mkdtemp = vrai
        return (debut(r, 0, "TOUR À FAIRE") and bool(vus)
                and all(v == f"{B.PREFIXE_DES_COPIES}{os.getpid()}_" for v in vus))
    cas("B50", b50)

    # ── relecture indépendante du 16-10-2026 vers 23h40 : le numéro seul laissait git entrer en collision avec
    # lui-même (18 échecs sur 200) ; et deux branches de `proprietaire_vivant` n'étaient gardées par aucun cas. ──
    def b51(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        contexte = multiprocessing.get_context("fork")
        file = contexte.Queue()

        def un_processus():
            echecs = 0
            for _ in range(VERIFICATIONS_PAR_PROCESSUS):
                code, _motif = B.verifier_la_note(depot, "origin/travail-x", B.NOTE_DE_COWORK)
                echecs += code != 0
            file.put(echecs)

        enfants = [contexte.Process(target=un_processus) for _ in range(PROCESSUS_EN_MEME_TEMPS)]
        try:
            for e in enfants:
                e.start()
            echecs = [file.get(timeout=300) for _ in enfants]
        finally:
            for e in enfants:
                if e.is_alive():
                    e.kill()
                e.join()
        restes = [x for x in g(depot, "worktree", "list", "--porcelain").split("\n") if x.startswith("worktree ")]
        return sum(echecs) == 0 and len(restes) == 1
    cas("B51", b51)

    def b52(m):
        nom = lambda pid: f"{B.PREFIXE_DES_COPIES}{pid}_abc"
        moi = not B.proprietaire_vivant(nom(os.getpid()))
        zero_un = not B.proprietaire_vivant(nom(0)) and not B.proprietaire_vivant(nom(1))
        vrai_kill = B.os.kill

        def refuse(pid, sig):
            raise PermissionError(1, "Operation not permitted")
        B.os.kill = refuse
        try:
            autre_utilisateur = B.proprietaire_vivant(nom(os.getpid() + 1))
        finally:
            B.os.kill = vrai_kill
        return moi and zero_un and autre_utilisateur
    cas("B52", b52)

    # B53 — sans hasard : chaque commande « git worktree » du programme doit trouver le verrou des copies déjà tenu.
    # Tour 9 de la relecture : B51 seul ne mordait le verrou retiré que 3 fois sur 4.
    def b53(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        chemin = os.path.join(depot, ".git", "boucle_de_check_copies.verrou")
        vrai_git, sans_verrou, vues = B.git, [], []

        def espion(dossier, *args, **k):
            if args and args[0] == "worktree":
                vues.append(args[1])
                with open(chemin, "a") as f:
                    try:
                        B.fcntl.flock(f, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
                        sans_verrou.append(args[1])
                    except BlockingIOError:
                        pass
            return vrai_git(dossier, *args, **k)
        B.git = espion
        try:
            code, _ = B.verifier_la_note(depot, "origin/travail-x", B.NOTE_DE_COWORK)
        finally:
            B.git = vrai_git
        return code == 0 and {"add", "remove", "prune"} <= set(vues) and not sans_verrou
    cas("B53", b53)

    # B54 — un arrêt reçu juste après la prise du verrou : le programme sort, sans geler sur son propre verrou.
    def b54(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        script = os.path.join(m.d, "arret_apres_le_verrou.py")
        open(script, "w", encoding="utf-8").write(
            "import importlib.util, sys\n"
            "sp = importlib.util.spec_from_file_location('B', sys.argv[1]); B = importlib.util.module_from_spec(sp)\n"
            "sp.loader.exec_module(B)\n"
            "vrai, n = B.fcntl.flock, []\n"
            "def flock(f, op):\n"
            "    vrai(f, op); n.append(1)\n"
            "    if len(n) == 1:\n"
            "        B._arret_propre(15, None)\n"
            "B.fcntl.flock = flock\n"
            "try:\n"
            "    B.verifier_la_note(sys.argv[2], 'origin/travail-x', B.NOTE_DE_COWORK)\n"
            "except SystemExit as e:\n"
            "    print('SORTI', e.code)\n")
        try:
            r = subprocess.run([sys.executable, script, B.__file__, depot], capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return False
        restes = [x for x in g(depot, "worktree", "list", "--porcelain").split("\n") if x.startswith("worktree ")]
        return "SORTI 2" in r.stdout and len(restes) == 1
    cas("B54", b54)

    # B55 — un arrêt reçu entre la prise du verrou et le bloc qui le libère : le nettoyage libère d'abord ce verrou.
    def b55(m):
        lancee(m)
        m.ecrire("travail-x", {"echanges/RELU.md": ACCEPTE}, T0 + 10)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        script = os.path.join(m.d, "arret_entre_prise_et_bloc.py")
        open(script, "w", encoding="utf-8").write(
            "import importlib.util, linecache, sys\n"
            "sp = importlib.util.spec_from_file_location('B', sys.argv[1]); B = importlib.util.module_from_spec(sp)\n"
            "sp.loader.exec_module(B)\n"
            "vu = []\n"
            "def suivre(cadre, evenement, arg):\n"
            "    if cadre.f_code.co_name != 'verifier_la_note':\n"
            "        return None\n"
            "    def ligne(c, ev, a):\n"
            "        if ev == 'line' and not vu and linecache.getline(c.f_code.co_filename, c.f_lineno).strip()"
            ".startswith('if verrou is None'):\n"
            "            vu.append(1)\n"
            "            B._arret_propre(15, None)\n"
            "        return ligne\n"
            "    return ligne\n"
            "sys.settrace(suivre)\n"
            "try:\n"
            "    B.verifier_la_note(sys.argv[2], 'origin/travail-x', B.NOTE_DE_COWORK)\n"
            "except SystemExit as e:\n"
            "    print('SORTI', e.code, len(vu))\n")
        try:
            r = subprocess.run([sys.executable, script, B.__file__, depot], capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return False
        return "SORTI 2 1" in r.stdout
    cas("B55", b55)

    # B57 et B58 — relecture indépendante, tour 10 (17-10-2026) : une copie tuée pendant sa création restait inscrite
    # pour toujours (« locked initializing ») et était comptée comme retirée ; les dossiers vides restaient dans /tmp.
    def b57(m):
        lancee(m)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        g(depot, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
        mort = subprocess.Popen([sys.executable, "-c", "pass"])
        mort.wait()
        d = tempfile.mkdtemp(prefix=f"{B.PREFIXE_DES_COPIES}{mort.pid}_")
        try:
            g(depot, "worktree", "add", "-q", "--detach", os.path.join(d, "depot"), "origin/main")
            g(depot, "worktree", "lock", "--reason", "initializing", os.path.join(d, "depot"))
            n = B.nettoyer_les_copies(depot)
            restes = [x for x in g(depot, "worktree", "list", "--porcelain").split("\n") if x.startswith("worktree ")]
        finally:
            shutil.rmtree(d, ignore_errors=True)
            subprocess.run(["git", "-C", depot, "worktree", "prune"], capture_output=True)
        # et une copie que git refuse de retirer n'est pas comptée (le refus est simulé : sans lui, git retire tout)
        d2 = tempfile.mkdtemp(prefix=f"{B.PREFIXE_DES_COPIES}{mort.pid}_")
        vrai_git = B.git
        try:
            g(depot, "worktree", "add", "-q", "--detach", os.path.join(d2, "depot"), "origin/main")
            B.git = lambda dossier, *a, **k: (1, "") if a[:2] == ("worktree", "remove") else vrai_git(dossier, *a, **k)
            n_refus = B.nettoyer_les_copies(depot)
        finally:
            B.git = vrai_git
            shutil.rmtree(d2, ignore_errors=True)
            subprocess.run(["git", "-C", depot, "worktree", "prune"], capture_output=True)
        return n == 1 and len(restes) == 1 and n_refus == 0
    cas("B57", b57)

    def b58(m):
        lancee(m)
        depot = B.copie_du_programme(m.copie(), m.copie_du_programme)[0]
        vivant = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        mort = subprocess.Popen([sys.executable, "-c", "pass"])
        mort.wait()
        dossiers = {nom: tempfile.mkdtemp(prefix=f"{B.PREFIXE_DES_COPIES}{pid}_")
                    for nom, pid in (("vivant", vivant.pid), ("mort", mort.pid), ("moi", os.getpid()))}
        try:
            n = B.nettoyer_les_copies(depot)
            restent = {nom: os.path.isdir(d) for nom, d in dossiers.items()}
        finally:
            vivant.kill()
            vivant.wait()
            for d in dossiers.values():
                shutil.rmtree(d, ignore_errors=True)
        return n == 0 and restent == {"vivant": True, "mort": False, "moi": True}
    cas("B58", b58)

    # B56 — un cas dont le montage échoue est déclaré « MONTAGE IMPOSSIBLE », avec un message sans chemin jetable,
    # jamais compté comme un cas faux ordinaire (cassure N de Cowork, 17-10-2026). Ce cas éprouve l'épreuve elle-même.
    avant = len(faux)
    cas("B56_essai", lambda m: g(m.d, "commit", "-q", "-m", "x") is None)   # m.d n'est pas un dépôt git
    rendu = faux[avant:]
    del faux[avant:]
    if rendu != ["B56_essai (MONTAGE IMPOSSIBLE : git commit : code 128)"]:
        faux.append(f"B56 {rendu}")
    # B59 — classé par le dossier (relecture indépendante, tour 11) : un rebase du montage lancé hors de `g` est un
    # montage impossible ; une commande qui échoue dans un dossier du programme reste une exception ordinaire.
    avant = len(faux)
    cas("B59a", lambda m: lancer_le_montage(["git", "-C", m.d, "rebase", "-q", "main"], capture_output=True) is None)
    cas("B59b", lambda m: g(os.path.join(m.d, "copie_du_programme"), "status") is None)
    rendu = faux[avant:]
    del faux[avant:]
    if rendu != ["B59a (MONTAGE IMPOSSIBLE : git rebase : code 128)", "B59b (levé : CalledProcessError)"]:
        faux.append(f"B59 {rendu}")

    # B19, B19bis et B19ter (la vraie relecture de Cowork du 16-10-2026, a714f09) vivent depuis le 17-10-2026 dans
    # tests/EPREUVES_DE_LA_VERIFICATION_DES_NOTES_Sam_17-10-2026.py : ils copiaient tout programmes/ et gouvernance/,
    # et la série des sabotages de cette épreuve dépendait de 66 fichiers, dont gouvernance/PILOTE.md, réécrit chaque
    # soir (relecture indépendante du 17-10-2026, vers 13h20).
    return faux


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande ; tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py,
    par lots (« --saboter=S1,S2,… ») ; la certification de nuit, pour refaire quelques essais tirés au hasard.
    ③ ENTRÉE — Voir la fiche en tête ; « --saboter » joue tous les sabotages, « --saboter=S1,S2,… » ceux-là seulement.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête ; une
    ligne « Z0 … », puis une ligne par sabotage joué, « <nom> mord : [<cas faux>] » ou « <nom> NE MORD PAS : [] » ; un
    sabotage dont un cas n'a pas pu être monté écrit « <nom> NE PEUT PAS ÊTRE JOUÉ : […] », jamais « mord », et la
    sortie vaut 2 (cassure N de Cowork, 17-10-2026).
    ⑦ UNITÉ — — ⑧ POURQUOI — La forme des lignes est celle que lisent programmes/SERIES_DE_SABOTAGES.py et le joueur de
    séries (décision de Jean-Luc du 16-10-2026 à 22h52 : la série sort de la nuit comme celle des 20 ans) ; la liste
    des cas faux est donnée entière, dans l'ordre des cas, pour qu'un essai refait la nuit se compare mot pour mot.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(MODULE)
    impossible = any("MONTAGE IMPOSSIBLE" in f for f in faux)
    print("Z0 programme tel quel : " + ("tous les cas conformes" if not faux else "FAUX " + ", ".join(faux)))
    code = 1 if faux else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        texte = open(MODULE, encoding="utf-8").read()
        for nom, remplacements in SABOTAGES.items():
            if choix and nom not in choix[0]:
                continue
            t = texte
            for a, b in remplacements:
                if t.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois")
                    return 2
                t = t.replace(a, b)
            d = tempfile.mkdtemp(prefix="boucle_sab_")
            try:
                p = os.path.join(d, "BOUCLE_DE_CHECK.py")
                open(p, "w", encoding="utf-8").write(t)
                f = tour(p)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            if any("MONTAGE IMPOSSIBLE" in x for x in f):
                print(f"{nom} NE PEUT PAS ÊTRE JOUÉ : {[x for x in f if 'MONTAGE IMPOSSIBLE' in x]}", flush=True)
                impossible = True
                continue
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f}", flush=True)
            code |= 0 if f else 1
    if impossible:
        print("VERDICT : NON CONFORME — des cas n'ont pas pu être montés (R-734 : un contrôle qui n'a pas pu tourner)")
        return 2
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
