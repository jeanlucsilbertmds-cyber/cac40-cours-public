#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_COURS_PROPRE_DE_YAHOO — Jeu 22-10-2026 (Paris), restructurée les 23-10-2026. Simulation uniquement.

① RÔLE — Prouver, chaque fois qu'on touche au programme, que programmes/FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py refait,
  depuis les 40 réponses de Yahoo du 21-10-2026 rangées au dépôt, exactement le fichier propre et le relevé des
  événements attendus ; qu'il refuse toute réponse que le carnet de provenance n'inscrit pas telle qu'elle est ; qu'il
  distingue un refus d'une panne ; qu'il n'écrit ni dans un dépôt, ni dans sa racine, ni à côté de lui-même, ni hors
  de sa sortie, ni à moitié ; et que chacune de ses gardes a des dents.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py), SANS sabotages : l'essai
  court, environ 30 s. La série de sabotages ne tourne que quand le programme, cette épreuve ou un fichier qu'elle lit
  change : elle est déclarée « hors de la nuit » (tests/LANCEMENT_DES_EPREUVES.json), jouée par
  tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py, qui la lance par lots avec --saboter=S1,S2,… (décisions de Jean-Luc
  du 23-10-2026 à 16h29 et 16h33, BACKLOG A-599 ⑭). À la main : python3 tests/EPREUVES_DU_COURS_PROPRE_DE_YAHOO_Jeu_
  22-10-2026.py <racine> [--saboter | --saboter=S1,S2,…]
③ ENTRÉE — La racine du dépôt : le programme, les modules de programmes/ qu'il importe, et ses trois sources y sont
  pris ; l'option --saboter (tous les sabotages) ou --saboter=<noms séparés par des virgules> (ceux-là seulement).
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le code de sortie : 0 si Z0 (le programme du dépôt) donne la réponse attendue à E1–E24 et, avec --saboter,
  si les trois témoins négatifs sont reconnus et si chaque sabotage joué fait tomber au moins un cas ; 1 si Z0 a un
  cas faux ou ne se charge pas (les sabotages ne sont alors pas joués), ou si un sabotage ne mord pas ; 2 si
  l'épreuve n'a pas pu juger : un sabotage ne s'applique plus ou n'existe pas, un témoin négatif n'est pas reconnu, un
  sabotage ne se charge pas, le juge a levé une exception, les sources du dépôt ont changé pendant l'épreuve, ou une
  erreur imprévue est sortie (dernier filet de `main`, qui écrit toujours son VERDICT). [rend: 1]
⑥ TRAITEMENT — Chaque tour (Z0, chaque témoin, chaque sabotage) se joue dans un dossier jetable : `banc/programmes`
  (le texte éprouvé et les modules de programmes/ qu'il importe, relevés par son arbre syntaxique), `sources` (vraie
  copie des trois sources), et un DOSSIER PAR CAS, `cas/<nom>`, qui porte la racine du cas sous `entree/` (liens vers
  `sources`), sa sortie et ses voisins préparés sous `sorties/` — deux parents différents —, et `tmp/`, le dossier
  temporaire donné au programme ; ce dossier du cas est AUSSI le dossier courant du programme. Le texte est d'abord chargé par un
  sous-processus (`charge`) ; s'il ne se charge pas, le tour n'est pas joué. Puis chaque cas est jugé par `juger`, en
  sous-processus borné à 120 s :
  E1 les vraies sources : code 0, empreintes PROPRE_ATTENDU et EVENEMENTS_ATTENDU · E2 un chiffre d'une clôture changé
  dans AC.PA (JSON toujours valide) → 1 « REFUSÉ » · E3 AI.PA retirée → 1 · E4 l'empreinte d'AC.PA changée au carnet →
  1 · E5 la ligne d'AC.PA retirée du carnet → 1 · E6 la ligne d'AC.PA en double → 1 · E7 AC.PA inscrite autrement que
  comme téléchargement → 1 · E8 un chiffre changé dans MT.PA, la réponse qui ne donne que des événements → 1 · E9
  sortie sous la racine → 2 · E10 sortie qui existe déjà, avec un fichier → 2 · E10b sortie qui existe déjà, vide → 2
  · E11 une source absente → 2 · E12 sans argument → 2 · E13 une réponse mal formée (chart.result vide) mais inscrite
  au carnet avec sa vraie empreinte → 2 « IMPOSSIBLE » · E14 le référentiel en ordre inverse → les mêmes deux
  empreintes · E15 la fonction date_de_paris, lancée par un sous-processus : 23h30 en temps universel le 15-01-2025 →
  16-01-2025, 12h00 → 15-01-2025 (sortie exacte) · E16 l'écriture du second fichier rendue impossible → 2, avec un
  voisin « sortie.en_cours.ancien » qui ne doit pas bouger · E17 (E17k1, E17k2…) le processus arrêté net (comme une
  coupure) au k-ième geste qui modifie le disque, pour k = 1, 2, 3… jusqu'à ce qu'il finisse : à chaque coupure,
  code 3, pas de sortie, seuls des provisoires « sortie.en_cours.* » à côté d'elle ; au dernier k, code 0 et les
  deux empreintes ; finir dès k = 1 est faux (la coupure n'a rien vu) · E18 un dossier
  « sortie.en_cours » et un provisoire d'un autre lancement « sortie.en_cours.ancien » existent déjà → 0, les deux
  empreintes, ces dossiers ne bougent pas · E19 sortie sous le dépôt qui
  porte le programme (le banc) → 2 · E20 sortie voisine de la racine, au nom qui commence pareil (« e20 » et
  « e20_voisin ») → 0, les deux empreintes · E21 dossier parent de la sortie absent → 2 (comportement seulement :
  aucune règle propre ne le porte, mkdtemp échoue) · E22 sortie donnée par un lien vers la racine → 2 · E23 racine
  donnée par un lien, sortie dans la vraie racine → 2 · E24 programme lancé par un lien vers le banc, sortie dans le
  vrai banc → 2 (E22 à E24 : la garde « chemins résolus », pour la sortie, la racine et le dépôt du programme).
  Avant tout cas, ce que le chargement du programme écrirait dans le banc est un cas faux « chargement ».
  UNE SEULE RÈGLE pour tous les cas, en plus du code et de l'écran : l'état du dossier du cas après le lancement est
  celui d'avant, plus la sortie si le code est 0 et seulement avec les deux empreintes attendues (E17, après une
  coupure : plus des provisoires à côté de la sortie) ; et l'état du banc ne change pas. Elle couvre la racine, la
  sortie, les voisins, le dossier courant, le dossier temporaire et le dossier du programme. (Le contrôle du banc,
  retiré au tour 4 faute de dent, est revenu au tour 5 : un programme qui écrit à côté de lui-même par __file__
  restait vert — S25 et S26 lui donnent ses dents.)
  Avec --saboter : trois témoins négatifs (un programme qui ne peut pas s'importer, un qui sort par sys.exit(0), un qui
  sort par os._exit(0), chacun au chargement) doivent être reconnus « ne se charge pas » ; puis chaque règle du
  programme retirée, une à la fois (SABOTAGES). Une ligne par sabotage, à la forme que lit
  programmes/SERIES_DE_SABOTAGES.py : « <nom> mord […] », « <nom> NE MORD PAS [] », « <nom> NE S'APPLIQUE PLUS ».
⑦ UNITÉ — Des codes de sortie et des empreintes sha256.
⑧ POURQUOI — Les deux empreintes attendues sont MESURÉES : PROPRE_ATTENDU est celle du fichier propre refait depuis le
  témoin du 08-10-2026 et depuis les bruts du 21-10 coupés au 02-10 (nuit du 21 au 22-10-2026, fiche N4, fait ①) ;
  EVENEMENTS_ATTENDU est celle de `donnees/sources_yahoo/evenements.json` au dépôt le 22-10-2026. Une épreuve qui reste
  verte quand on retire ce qu'elle teste n'est pas une preuve (R-731). La forme — un dossier par cas jugé par une seule
  règle, rien du programme dans le processus de l'épreuve, un banc qui ne copie que ce que le programme importe — vient
  des superviseurs R-759 des tours 3 et 4 (23-10-2026) : de tour en tour, les relecteurs ne trouvaient plus de défaut
  dans le programme, mais dans l'étanchéité du juge (sortie au chargement, liens durs vers le dépôt, dossier courant,
  contenu des voisins, tube), et chaque trou bouché à part en ouvrait un autre. Copier tout programmes/ faisait lire à
  l'épreuve ses 62 programmes : sous « hors de la nuit », toute modification d'un programme quelconque aurait rejoué
  la série.
⑨ CE QUI CLOCHE — LE MODÈLE DE MENACE : cette épreuve juge les RÉGRESSIONS PLAUSIBLES d'un programme non hostile — une
  règle retirée, un chemin relatif, un nettoyage par motif, une écriture en deux gestes, un fichier écrit au mauvais
  endroit. Elle ne juge pas un programme écrit pour la tromper (chemin absolu écrit en dur, variable PWD héritée, lecture
  des arguments du chargeur, absence de bac à sable) : ce risque est couvert par le contrôle nocturne des empreintes de
  toute la chaîne des 20 ans et la restauration par l'historique git (décision du 23-10-2026 à 16h33). Un défaut
  trouvé hors de ce modèle se consigne ici ou au BACKLOG, il ne se répare pas (superviseur du tour 4). · PROPRE_ATTENDU
  vient du même traitement que le programme : l'épreuve prouve qu'on le refait, pas qu'il est juste ; le relecteur du
  22-10-2026 l'a confronté ligne à ligne à l'ancien fichier (13 lignes changées et 1 ajoutée, toutes du 02-10-2026). ·
  Les règles « borne de la coupure incluse » et « accents gardés » n'ont pas de cas qui les distingue sur ces données.
  · « Mord » veut dire « au moins un cas tombe », pas « le cas visé tombe » (A-T3-1 ; la liste des cas que chaque
  sabotage doit faire tomber est une décision de Jean-Luc, BACKLOG A-599 ⑫). · Le juge vérifie le code et le premier
  mot de l'écran, pas la cause d'un refus (A-N3). · Un arrêt brutal de l'épreuve (SIGKILL) laisse son dossier jetable.
  · Le code de retour du chargement n'a pas de témoin propre (seul le marqueur retiré est éprouvé). · FABRIQUER n'est
  pas au certificat de référence (gouvernance/CERTIFICAT_REFERENCE.json) : aucun recul de couverture ne le signalerait.
⑩ EFFET — Écrit dans un dossier jetable par tour, effacé à la fin du tour ; lance le programme par sous-processus ; ne
  lit le dépôt que pour le copier.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 secondes (un dépassement est un cas faux) ; le juge
  n'ouvre que des fichiers ordinaires (un tube ou un lien ne le bloque pas) ; un programme qui tue son processus ne tue
  que le sous-processus ; sort par sys.exit. [sort: oui]
"""
import ast
import csv
import hashlib
import io
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
NOM = "FABRIQUER_LE_COURS_PROPRE_DE_YAHOO.py"
MODULE = os.path.join(DEPOT, "programmes", NOM)
REF = os.path.join("donnees", "REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv")
BRUTS = os.path.join("donnees", "sources_yahoo", "bruts_yahoo_21-10-2026")
CARNET = os.path.join("donnees", "PROVENANCE_DES_FICHIERS.csv")
PROPRE_ATTENDU = "ea18640899c7a90d50abe62f5a4de407b845859493abee9d6f66b288d5a43a27"
EVENEMENTS_ATTENDU = "e7e5f9a39fd53ec2289304eaee06199e227cbe651dd1ac359dd6d3c855f53997"
ATTENDUS = {"evenements.json": EVENEMENTS_ATTENDU, "yahoo_ohlcv_propre.csv": PROPRE_ATTENDU}
# Un lanceur qui rend impossible l'écriture du second fichier (E16), sans toucher au programme.
LANCEUR_E16 = (
    "import builtins, runpy, sys\n"
    "vrai = builtins.open\n"
    "def faux(p, *a, **k):\n"
    "    if str(p).endswith('evenements.json') and a and 'w' in a[0]:\n"
    "        raise OSError('écriture refusée par l épreuve')\n"
    "    return vrai(p, *a, **k)\n"
    "builtins.open = faux\n"
    "sys.argv = [sys.argv[1]] + sys.argv[2:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n")
# Un lanceur qui ARRÊTE NET le processus (os._exit(3), comme une coupure : rien ne nettoie) au k-ième geste qui
# modifie le disque — ouverture en écriture par open, io.open ou os.open, et os.mkdir, rename, replace, remove,
# unlink, rmdir, link, symlink. E17 le joue pour k = 1, 2, 3… jusqu'à ce que le programme finisse sans être coupé.
# Pourquoi toutes ces primitives et pas seulement open : une écriture « en deux gestes » faite par makedirs puis des
# rename (variante VH du superviseur du tour 5, 23-10-2026) n'ouvre aucun fichier et échappait à une coupure par open.
LANCEUR_COUPURE = (
    "import builtins, io, os, runpy, sys\n"
    "k = K_ICI; n = [0]\n"
    "def coupe():\n"
    "    n[0] += 1\n"
    "    if n[0] == k:\n"
    "        os._exit(3)\n"
    "vrai_open = builtins.open\n"
    "def faux_open(p, *a, **kw):\n"
    "    m = a[0] if a else kw.get('mode', 'r')\n"
    "    if any(c in m for c in 'wax+'):\n"
    "        coupe()\n"
    "    return vrai_open(p, *a, **kw)\n"
    "builtins.open = faux_open\n"
    "io.open = faux_open\n"
    "def garde(nom):\n"
    "    vrai = getattr(os, nom)\n"
    "    def f(*a, **kw):\n"
    "        coupe()\n"
    "        return vrai(*a, **kw)\n"
    "    setattr(os, nom, f)\n"
    "for nom in ('mkdir', 'rename', 'replace', 'remove', 'unlink', 'rmdir', 'link', 'symlink'):\n"
    "    garde(nom)\n"
    "vrai_osopen = os.open\n"
    "def faux_osopen(p, flags, *a, **kw):\n"
    "    if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT):\n"
    "        coupe()\n"
    "    return vrai_osopen(p, flags, *a, **kw)\n"
    "os.open = faux_osopen\n"
    "sys.argv = sys.argv[1:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n")
# Un lanceur qui charge le programme sans lancer `main` et écrit les deux dates de E15 : rien du programme ne
# tourne dans le processus de l'épreuve (relecteur du 23-10-2026, I-T3-1).
LANCEUR_E15 = ("import runpy, sys\n"
               "g = runpy.run_path(sys.argv[1], run_name='e15')\n"
               "print(g['date_de_paris'](1736983800), g['date_de_paris'](1736942400))\n")
# Les témoins négatifs : une tête posée avant le texte du programme ; chacun doit être reconnu « ne se charge pas ».
# Un par branche du jugement de `charge` (superviseur du 23-10-2026) : import impossible (code non nul), sortie par
# sys.exit(0) (attrapée, code 9), sortie par os._exit(0) (code 0 sans marqueur).
TEMOINS_NEGATIFS = {
    "import_impossible": "import module_qui_n_existe_pas\n",
    "sys_exit_0_au_chargement": "import sys; sys.exit(0)\n",
    "os_exit_0_au_chargement": "import os; os._exit(0)\n",
}
SABOTAGES = {
    "S1_empreinte_non_comparee": [("        if hashlib.sha256(octets).hexdigest() != lignes[0][\"sha256\"]:\n",
                                   "        if False:\n")],
    "S2_reponse_absente_toleree": [("            raise Refus(f\"{s} : réponse absente ({chemin})\")\n",
                                    "            continue\n")],
    "S3_doublon_au_carnet_tolere": [("        if len(lignes) != 1:\n", "        if len(lignes) < 1:\n")],
    "S4_sorte_non_verifiee": [("        if lignes[0][\"produit_par\"] != TELECHARGEMENT:\n", "        if False:\n")],
    "S5_cours_sans_coupure": [("        if d > COUPURE or (valeur", "        if False or (valeur")],
    "S6_stellantis_avec_peugeot": [("(valeur == \"STELLANTIS\" and d < DEBUT_STELLANTIS)", "False")],
    "S7_volume_nul_garde": [("if None in (o, h, b, c, vol) or vol == 0 or", "if None in (o, h, b, c, vol) or")],
    "S8_barre_incoherente_gardee": [(" or not (b <= o <= h and b <= c <= h):", ":")],
    "S9_evenements_sans_coupure": [("for t, x in ev.get(\"splits\", {}).items() if date_de_paris(t) <= COUPURE)",
                                    "for t, x in ev.get(\"splits\", {}).items())"),
                                   ("for t in ev.get(\"dividends\", {}) if date_de_paris(t) <= COUPURE)",
                                    "for t in ev.get(\"dividends\", {}))")],
    "S10_toute_reponse_donne_des_cours": [("    return m.get(\"instrumentType\") == TYPE_ACTION and m.get(\"currency\") == DEVISE\n",
                                           "    return True\n")],
    "S11_sortie_dans_un_depot": [("            return f\"la sortie est sous un dépôt ({d}) : verser est un geste à part\"\n",
                                  "            pass\n")],
    "S12_sortie_existante_acceptee": [("        return \"le dossier de sortie existe déjà\"\n", "        pass\n")],
    "S13_panne_prise_pour_refus": [("    except Exception as e:\n        print(f\"IMPOSSIBLE : {type(e).__name__} — {e}\")\n        return 2\n",
                                    "    except Exception as e:\n        print(f\"REFUSÉ : {e}\")\n        return 1\n")],
    "S14_date_en_temps_universel": [("datetime.datetime.fromtimestamp(int(horodatage), PARIS)",
                                     "datetime.datetime.fromtimestamp(int(horodatage), datetime.timezone.utc)")],
    "S15_ecriture_en_deux_gestes": [("        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + \".en_cours.\", dir=os.path.dirname(sortie))\n",
                                     "        provisoire = sortie\n        os.makedirs(provisoire)\n")],
    "S16_lignes_non_triees": [("    lignes.sort()\n", "")],
    "S18_provisoire_au_nom_fixe": [("        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + \".en_cours.\", dir=os.path.dirname(sortie))\n",
                                    "        provisoire = sortie + \".en_cours\"\n        os.makedirs(provisoire)\n")],
    "S19_depot_du_programme_non_garde": [("    for d in (os.path.realpath(racine), depot_du_programme):\n",
                                          "    for d in (os.path.realpath(racine),):\n")],
    "S20_prefixe_au_lieu_de_commonpath": [("        if os.path.commonpath([s, d]) == d:\n", "        if s.startswith(d):\n")],
    "S21_provisoire_laisse_apres_un_echec": [("            shutil.rmtree(provisoire, ignore_errors=True)\n",
                                              "            pass\n")],
    # S22 : la régression réaliste de I-N2, un nettoyage par motif qui efface aussi ce que le programme n'a pas créé.
    "S22_nettoyage_par_motif": [("            shutil.rmtree(provisoire, ignore_errors=True)\n",
                                 "            for x in os.listdir(os.path.dirname(sortie)):\n"
                                 "                if x.startswith(os.path.basename(sortie) + \".en_cours\"):\n"
                                 "                    shutil.rmtree(os.path.join(os.path.dirname(sortie), x), ignore_errors=True)\n")],
    # S23 : le programme écrit dans sa racine (le X5 du relecteur du 23-10-2026) : une ligne ajoutée au carnet.
    "S23_ecrit_dans_sa_racine": [("        carnet = list(csv.DictReader(f))\n",
                                  "        carnet = list(csv.DictReader(f))\n"
                                  "    open(os.path.join(racine, CARNET), \"a\", encoding=\"utf-8\").write(\"ecrit,en,place\\n\")\n")],
    # S24 : le programme verse son fichier dans le dépôt par un chemin relatif qu'il crée (superviseur du tour 4,
    # 23-10-2026 : seul un sabotage qui CRÉE son chemin donne une dent à la règle « le dossier du cas ne change pas »
    # du côté du dossier courant ; celui du relecteur plantait faute de dossier `donnees/`).
    "S24_verse_en_creant_le_chemin": [("        os.rename(provisoire, sortie)\n",
                                       "        os.rename(provisoire, sortie)\n"
                                       "        os.makedirs(os.path.join(\"donnees\", \"sources_yahoo\"), exist_ok=True)\n"
                                       "        open(os.path.join(\"donnees\", \"sources_yahoo\", \"yahoo_ohlcv_propre.csv\"), \"wb\").write(propre)\n")],
    # S25 à S31 : les régressions plausibles jouées par le relecteur et le superviseur du tour 5 (23-10-2026), qui
    # restaient vertes ; chacune doit désormais mordre.
    "S25_journal_a_cote_du_programme": [("        os.rename(provisoire, sortie)\n",
        "        os.rename(provisoire, sortie)\n"
        "        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), \"journal_du_cours_propre.txt\"), \"a\", encoding=\"utf-8\").write(\"écrit\\n\")\n")],
    "S26_verse_dans_le_depot_du_programme": [("        os.rename(provisoire, sortie)\n",
        "        os.rename(provisoire, sortie)\n"
        "        d = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), \"donnees\", \"sources_yahoo\")\n"
        "        os.makedirs(d, exist_ok=True)\n"
        "        open(os.path.join(d, \"yahoo_ohlcv_propre.csv\"), \"wb\").write(propre)\n")],
    "S27_copie_puis_effacement": [("        os.rename(provisoire, sortie)\n",
        "        shutil.copytree(provisoire, sortie)\n        shutil.rmtree(provisoire)\n")],
    "S28_provisoire_dans_le_dossier_temporaire": [
        ("        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + \".en_cours.\", dir=os.path.dirname(sortie))\n",
         "        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + \".en_cours.\")\n")],
    "S29_provisoire_a_cote_de_la_racine": [
        ("        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + \".en_cours.\", dir=os.path.dirname(sortie))\n",
         "        provisoire = tempfile.mkdtemp(prefix=os.path.basename(sortie) + \".en_cours.\", dir=os.path.dirname(racine))\n")],
    "S30_renomme_fichier_par_fichier": [("        os.rename(provisoire, sortie)\n",
        "        os.makedirs(sortie)\n        for x in sorted(os.listdir(provisoire)):\n"
        "            os.rename(os.path.join(provisoire, x), os.path.join(sortie, x))\n        os.rmdir(provisoire)\n")],
    "S31_chemins_non_resolus": [("    s = os.path.realpath(sortie)\n", "    s = os.path.abspath(sortie)\n"),
                                ("    for d in (os.path.realpath(racine), depot_du_programme):\n",
                                 "    for d in (os.path.abspath(racine), depot_du_programme):\n")],
    # S32 à S34 : les régressions plausibles du relecteur du tour 6 (23-10-2026), qui restaient vertes.
    "S32_nettoyage_des_provisoires_apres_succes": [("        os.rename(provisoire, sortie)\n",
        "        os.rename(provisoire, sortie)\n        [shutil.rmtree(os.path.join(os.path.dirname(sortie), x)) for x in os.listdir(os.path.dirname(sortie)) if x.startswith(os.path.basename(sortie) + \".en_cours.\")]\n")],
    "S33_depot_du_programme_non_resolu": [("    depot_du_programme = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))\n",
        "    depot_du_programme = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n")],
    "S34_journal_a_cote_du_programme_a_l_import": [("sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n",
        "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport logging; logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), \"fabriquer.log\"))\n")],
    "S17_ordre_des_evenements_du_referentiel": [
        ("    ordre = sorted(v for v, s in valeurs if s in actions) + sorted(v for v, s in valeurs if s not in actions)\n",
         "    ordre = [v for v, s in valeurs if s in actions] + [v for v, s in valeurs if s not in actions]\n")],
}




def chiffre_change(b):
    """Change un chiffre d'une clôture : la réponse reste un JSON valide, seule l'empreinte la trahit.

    ① RÔLE — Altérer sans casser. ② CONTEXTE D'APPEL — `tour` (E2, E8). ③ ENTRÉE — `b` : une réponse.
    ④ CONDITIONS D'ENTRÉE — Elle porte « "close":[ » suivi d'un chiffre. ⑤ SORTIE — UNE valeur : les octets abîmés.
    [rend: 1] ⑥ TRAITEMENT — Remplacer le premier chiffre après « "close":[ ». ⑦ UNITÉ — — ⑧ POURQUOI — Une
    altération qui casse le JSON serait refusée par accident, pas par le contrôle d'empreinte (sabotage S1, 22-10).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    i = b.index(b'"close":[') + len(b'"close":[')
    while not b[i:i + 1].isdigit():
        i += 1
    return b[:i] + (b"1" if b[i:i + 1] != b"1" else b"2") + b[i + 1:]


def carnet_change(f):
    """Rend une fonction qui réécrit le carnet ligne par ligne avec `f` (ligne → liste de lignes).

    ① RÔLE — Fabriquer un carnet faux. ② CONTEXTE D'APPEL — `tour` (E4 à E7, E13). ③ ENTRÉE — `f` : appliquée à
    chaque ligne lue (dictionnaire), rend les lignes à écrire. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : une
    fonction octets → octets. [rend: 1] ⑥ TRAITEMENT — Lire le CSV, appliquer, réécrire. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    def g(b):
        lus = list(csv.DictReader(io.StringIO(b.decode("utf-8"))))
        t = io.StringIO()
        w = csv.DictWriter(t, fieldnames=list(lus[0].keys()), lineterminator="\n")
        w.writeheader()
        for r in lus:
            w.writerows(f(r))
        return t.getvalue().encode("utf-8")
    return g


def acpa(r):
    """Dit si une ligne du carnet est celle d'AC.PA. ① RÔLE — Viser une ligne. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `r` : une ligne. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : vrai ou faux. [rend: 1]
    ⑥ TRAITEMENT — Comparer le nom de fichier. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return r["fichier"].endswith("/AC.PA.json")




def lancer(module, args, lanceur, courant):
    """Lance le programme seul, depuis le dossier du cas ; rend son code et ce qu'il a écrit à l'écran.

    ① RÔLE — Jouer un cas. ② CONTEXTE D'APPEL — `juger`. ③ ENTRÉE — `module` : le programme posé dans le banc ;
    `args` : ses arguments ; `lanceur` : un texte Python qui lance le programme à sa façon (E15, E16, E17), ou None ;
    `courant` : le dossier du cas, qui devient le dossier courant du programme.
    ④ CONDITIONS D'ENTRÉE — `courant` existe. ⑤ SORTIE — DEUX valeurs : le code de sortie et la sortie écrite. [rend: 2]
    ⑥ TRAITEMENT — Sous-processus `python3 -B -I`, dossier courant `courant`, TMPDIR `courant/tmp`, borné à 120 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le code et le premier mot (REFUSÉ, IMPOSSIBLE) font partie du contrat ; rien du programme
    ne tourne dans le processus de l'épreuve ; le dossier courant est celui du cas (relecteur du tour 4, 23-10-2026,
    I-T4-1 : lancé depuis le dépôt, un programme qui écrivait par un chemin relatif écrasait le fichier propre du dépôt,
    épreuve verte). ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main ; un dépassement
    lève TimeoutExpired, que `juger` écrit comme un cas faux. [sort: non]
    """
    tete = ["-c", lanceur, module] if lanceur else [module]
    # TMPDIR dans le dossier du cas : un provisoire posé dans le dossier temporaire du système et oublié (variante VA
    # du relecteur du tour 5) se voit alors par la règle du dossier du cas (superviseur du tour 5, P3).
    p = subprocess.run([sys.executable, "-B", "-I", *tete, *args], capture_output=True, text=True, timeout=120,
                       cwd=courant, env=dict(os.environ, TMPDIR=os.path.join(courant, "tmp")))
    return p.returncode, p.stdout


def empreinte(p):
    """Rend l'empreinte sha256 d'un fichier ordinaire, ou une marque — sans jamais lever ni bloquer.

    ① RÔLE — Mesurer un fichier. ② CONTEXTE D'APPEL — `etat`, `sources_du_depot`. ③ ENTRÉE — `p` : un chemin.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux pour un fichier ordinaire ; sinon
    « <absent> », « <dossier> », « <objet non ordinaire> » ou « <illisible> ». [rend: 1]
    ⑥ TRAITEMENT — os.lstat d'abord (sans suivre un lien) ; n'ouvre que ce que stat.S_ISREG dit ordinaire.
    ⑦ UNITÉ — — ⑧ POURQUOI — Relecteur du tour 4 (23-10-2026, P-T4-5) : ouvrir un tube nommé bloquait le juge sans fin,
    et un lien cassé le faisait lever ; superviseur du même jour : UNE fonction pour juger tout objet (R-708).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return "<absent>"
    except OSError:
        return "<illisible>"
    if stat.S_ISDIR(st.st_mode):
        return "<dossier>"
    if not stat.S_ISREG(st.st_mode):
        return "<objet non ordinaire>"
    try:
        with open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return "<illisible>"


def etat(dossier):
    """Rend l'état d'un dossier : chaque chemin relatif sous lui, avec l'empreinte ou la marque de ce qu'il porte.

    ① RÔLE — Voir qu'un lancement n'a rien changé, d'une seule mesure. ② CONTEXTE D'APPEL — `juger`, `tour`,
    `sources_du_depot`. ③ ENTRÉE — `dossier`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {chemin relatif : empreinte ou marque} ; {} si le dossier n'existe pas. [rend: 1]
    ⑥ TRAITEMENT — Parcours sans suivre les liens ; chaque dossier, même vide, est noté « <dossier> » ; chaque autre
      objet passe par `empreinte`.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une seule propriété pour tous les cas (superviseur du tour 4, 23-10-2026) : un fichier
      changé, ajouté, retiré, un dossier vidé ou effacé change l'état. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit les fichiers.
    ⑪ TERMINAISON — Rend la main ; ne lève pas, n'ouvre que des fichiers ordinaires. [sort: non]
    """
    out = {}
    if empreinte(dossier) != "<dossier>":
        return out
    pile = [""]
    while pile:
        rel = pile.pop()
        try:
            noms = sorted(os.listdir(os.path.join(dossier, rel)))
        except OSError:
            out[rel or "."] = "<illisible>"
            continue
        for n in noms:
            r = os.path.join(rel, n)
            out[r] = empreinte(os.path.join(dossier, r))
            if out[r] == "<dossier>":
                pile.append(r)
    return out


def modules_importes(texte):
    """Rend les fichiers de DEPOT/programmes/ que le texte importe, de proche en proche.

    ① RÔLE — Construire le banc avec ce que le programme lit, et rien de plus. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `texte` : le texte du programme. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des noms de fichiers (« CONTRATS_DES_FICHIERS.py », …). [rend: 1]
    ⑥ TRAITEMENT — Arbre syntaxique : chaque `import X` et `from X import …` de niveau 0 dont DEPOT/programmes/X.py
      existe ; puis les imports de ces fichiers, jusqu'à ce que rien ne s'ajoute. Un texte qui ne se lit pas comme du
      Python rend l'ensemble vide (il ne se chargera pas).
    ⑦ UNITÉ — — ⑧ POURQUOI — Une propriété, pas une liste (superviseur du tour 4, 23-10-2026) : copier tout programmes/
      faisait lire à l'épreuve ses 62 programmes, et sous « hors de la nuit » tout changement d'un seul aurait rejoué
      la série. ⑨ CE QUI CLOCHE — Un import dynamique (importlib, __import__) n'est pas vu : le programme ne se
      chargerait pas dans le banc, et Z0 tomberait. ⑩ EFFET — Lit les fichiers de programmes/.
    ⑪ TERMINAISON — Rend la main ; l'ensemble des fichiers est fini. [sort: non]
    """
    vus, a_lire = set(), [texte]
    while a_lire:
        try:
            arbre = ast.parse(a_lire.pop())
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            noms = [a.name for a in n.names] if isinstance(n, ast.Import) else \
                [n.module] if isinstance(n, ast.ImportFrom) and n.module and not n.level else []
            for x in noms:
                f = x.split(".")[0] + ".py"
                p = os.path.join(DEPOT, "programmes", f)
                if f not in vus and f != NOM and os.path.isfile(p):
                    vus.add(f)
                    a_lire.append(open(p, encoding="utf-8").read())
    return vus


def charge(module, courant):
    """Dit si un programme se charge : ses définitions s'exécutent sans sortir, et `main` et `date_de_paris` existent.

    ① RÔLE — Distinguer un programme qu'on peut éprouver d'un programme qui ne se charge pas.
    ② CONTEXTE D'APPEL — `tour`, avant tout cas. ③ ENTRÉE — `module` : le chemin du programme posé dans le banc ;
    `courant` : un dossier jetable vide, dossier courant du chargement. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux. [rend: 1]
    ⑥ TRAITEMENT — Un sous-processus exécute le programme sans lancer `main` (runpy, run_name « chargement »), attrape
      toute sortie (BaseException, code 9), vérifie les deux noms (code 8), puis écrit « CHARGÉ <jeton> », le jeton
      tiré au hasard par l'épreuve. Vrai si le code est 0 ET si la sortie est exactement ce marqueur.
    ⑦ UNITÉ — — ⑧ POURQUOI — Relecteur du 23-10-2026 (I-T3-1) : un programme qui sortait par sys.exit(0) ou os._exit(0)
      au chargement « se chargeait » et rendait l'épreuve verte. Le code 9 attrape sys.exit ; le marqueur attrape
      os._exit (code 0 sans marqueur) ; le jeton empêche un texte d'écrire lui-même le marqueur (superviseur du même
      jour). Chaque branche a son témoin négatif (TEMOINS_NEGATIFS).
    ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨. ⑩ EFFET — Lance un processus.
    ⑪ TERMINAISON — Rend la main ; borné à 120 secondes (un dépassement rend faux). [sort: non]
    """
    jeton = secrets.token_hex(8)
    chargeur = ("import runpy, sys\n"
                "try:\n"
                "    g = runpy.run_path(sys.argv[1], run_name='chargement')\n"
                "except BaseException:\n"
                "    sys.exit(9)\n"
                "if not (callable(g.get('main')) and callable(g.get('date_de_paris'))):\n"
                "    sys.exit(8)\n"
                "print('CHARGÉ', sys.argv[2], flush=True)\n")
    try:
        p = subprocess.run([sys.executable, "-B", "-I", "-c", chargeur, module, jeton],
                           capture_output=True, text=True, timeout=120, cwd=courant)
    except subprocess.TimeoutExpired:
        return False
    return p.returncode == 0 and p.stdout == f"CHARGÉ {jeton}\n"


def ecart(avant, apres):
    """Décrit la différence entre deux états, en trois listes courtes et reproductibles.

    ① RÔLE — Dire au relevé ce qui a bougé. ② CONTEXTE D'APPEL — `juger`. ③ ENTRÉE — Deux états (`etat`).
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : un texte. [rend: 1]
    ⑥ TRAITEMENT — Chemins ajoutés, retirés, changés (trois au plus chacun) ; le suffixe tiré au hasard d'un dossier
      provisoire (« .en_cours.<8 signes> », ceux de tempfile.mkdtemp) devient « .en_cours.<hasard> », et le nom de
      8 signes d'un fichier posé sous tmp/ devient « tmp/<hasard> ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Une série refaite la nuit doit rendre la même ligne, mot pour mot (relecteur du tour 4,
      P-T4-4). ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    # Le suffixe de tempfile.mkdtemp a 8 signes ; « sortie.en_cours.ancien », préparé par E16, n'est pas un hasard.
    # Et le fichier sonde de 8 signes que tempfile pose directement sous tmp/ (superviseur du tour 5, R3).
    hasard = lambda x: re.sub(r"(^|/)tmp/[a-z0-9_]{8}$", r"\1tmp/<hasard>",
                              re.sub(r"\.en_cours\.[a-z0-9_]{8}(?=/|$)", ".en_cours.<hasard>", x))
    fixe = lambda xs: sorted({hasard(x) for x in xs})[:3]
    morceaux = [("ajouté", fixe(set(apres) - set(avant))), ("retiré", fixe(set(avant) - set(apres))),
                ("changé", fixe(k for k in set(avant) & set(apres) if avant[k] != apres[k]))]
    return " ; ".join(f"{m} {v}" for m, v in morceaux if v)


def copie(dossier_du_cas, base, nom="racine", refaire=None):
    """Fabrique, dans le dossier du cas, une racine qui porte les trois sources en liens durs vers la copie du tour.

    ① RÔLE — Préparer un cas sans jamais toucher au dépôt. ② CONTEXTE D'APPEL — Les préparations des cas, dans `tour`.
    ③ ENTRÉE — `dossier_du_cas` ; `base` : le dossier jetable du tour (il porte `sources/`) ; `nom` : le nom de la
    racine ; `refaire` : None, ou (chemin relatif, fonction octets → octets, ou None pour retirer le fichier).
    ④ CONDITIONS D'ENTRÉE — `base/sources` existe. ⑤ SORTIE — UNE valeur : la racine fabriquée. [rend: 1]
    ⑥ TRAITEMENT — Lier chaque fichier de `base/sources` ; le fichier à abîmer est délié puis réécrit, jamais modifié en
    place. ⑦ UNITÉ — — ⑧ POURQUOI — Les liens durs évitent de recopier 27 Mo par cas ; ils ne visent que la copie du
    tour, jamais le dépôt (relecteur du 23-10-2026, I-T3-2), et restent sur un seul disque. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans le dossier du cas. ⑪ TERMINAISON — Rend la main ; une erreur remonte au juge. [sort: non]
    """
    r = os.path.join(dossier_du_cas, nom)
    shutil.copytree(os.path.join(base, "sources"), r, copy_function=os.link)
    if refaire:
        rel, f = refaire
        p = os.path.join(r, rel)
        b = f(open(p, "rb").read())
        os.remove(p)
        if b is not None:
            open(p, "wb").write(b)
    return r


def tour(texte):
    """Pose un texte de programme dans un banc neuf et joue E1 à E24 ; rend les cas faux et les pannes du juge.

    ① RÔLE — Un tour d'épreuves, le même pour Z0, les témoins et chaque sabotage.
    ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `texte` : le texte complet du programme à éprouver.
    ④ CONDITIONS D'ENTRÉE — DEPOT/programmes et les trois sources du dépôt existent.
    ⑤ SORTIE — DEUX valeurs : None si le texte ne se charge pas, sinon la liste des cas faux (vide si tout est
      conforme) ; et la liste des cas que le JUGE n'a pas pu juger (exception de l'épreuve, pas du programme).
      [rend: 2]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥. `base/banc/programmes` : le texte posé sous le nom du programme et les
      modules qu'il importe — c'est « le dépôt qui porte le programme » pour lui ; `base/sources` : vraie copie des
      trois sources ; `base/cas/<nom>` : un dossier par cas, dossier courant du programme ; `base/chargement` : le
      dossier courant du chargement.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête, ⑧. ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨.
    ⑩ EFFET — Crée puis efface `base` ; lance des sous-processus.
    ⑪ TERMINAISON — Rend la main ; une exception du juge est écrite, pas levée ; une panne de la préparation du banc
      (disque plein, par exemple) remonte au filet de `main` ; le `finally` efface le banc. [sort: non]
    """
    faux, pannes = [], []
    base = tempfile.mkdtemp(prefix="cours_propre_")
    try:
        banc = os.path.join(base, "banc")
        os.makedirs(os.path.join(banc, "programmes"))
        for f in modules_importes(texte):
            shutil.copyfile(os.path.join(DEPOT, "programmes", f), os.path.join(banc, "programmes", f))
        module = os.path.join(banc, "programmes", NOM)
        open(module, "w", encoding="utf-8").write(texte)
        os.makedirs(os.path.join(base, "chargement"))
        # Ce que le CHARGEMENT écrit dans le banc se voit aussi (relecteur du tour 6, V3 : un journal vide créé à
        # l'import à côté du programme passait, l'état du banc étant relevé après le chargement ; dent : S34).
        banc_avant_charge = etat(banc)
        if not charge(module, os.path.join(base, "chargement")):
            return None, []
        banc_apres_charge = etat(banc)
        if banc_apres_charge != banc_avant_charge:
            faux.append("chargement (banc changé : " + ecart(banc_avant_charge, banc_apres_charge) + ")")
        for rel in (REF, CARNET, BRUTS):
            src, dst = os.path.join(DEPOT, rel), os.path.join(base, "sources", rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            (shutil.copytree if os.path.isdir(src) else shutil.copyfile)(src, dst)

        def juger(nom, preparer, code_attendu, mot=None, exact=None, avec_sortie=False, lanceur=None,
                  sans_args=False, provisoires=False, module_=None):
            # Le juge unique : il ne lève jamais (superviseur du 23-10-2026) ; une erreur de l'épreuve est une PANNE.
            try:
                cas_ = os.path.join(base, "cas", nom)
                os.makedirs(os.path.join(cas_, "tmp"))
                racine, sortie = preparer(cas_)
                avant = etat(cas_)
                avant_banc = etat(banc)
                try:
                    lance = module_(cas_) if module_ else module   # E24 : le programme lancé par un lien
                    code, ecran = lancer(lance, [] if sans_args else [racine, sortie], lanceur, cas_)
                except subprocess.TimeoutExpired:
                    faux.append(f"{nom} (délai dépassé)")
                    return None
                raisons = []
                if code not in (code_attendu if isinstance(code_attendu, tuple) else (code_attendu,)):
                    raisons.append(f"code {code}")
                if mot is not None and not ecran.startswith(mot):
                    raisons.append(f"écran {ecran[:40]!r}")
                if exact is not None and ecran != exact:
                    raisons.append(f"écran {ecran[:40]!r}")
                # LA règle : le dossier du cas ne change pas, sauf la sortie permise (superviseur du tour 4).
                attendu = dict(avant)
                if code == 0 and avec_sortie:
                    s = os.path.relpath(sortie, cas_)
                    attendu[s] = "<dossier>"
                    attendu.update({os.path.join(s, f): h for f, h in ATTENDUS.items()})
                apres = etat(cas_)
                # Des provisoires ne sont admis qu'À CÔTÉ de la sortie, et seulement après une coupure (code 3) ; avec le
                # code 0, un provisoire qui reste est un défaut (superviseur du tour 5, R4).
                if provisoires and code == 3:
                    prefixe = os.path.relpath(sortie, cas_) + ".en_cours."
                    apres = {k: v for k, v in apres.items() if not k.startswith(prefixe)}
                if apres != attendu:
                    raisons.append("dossier du cas changé : " + ecart(attendu, apres))
                # Le banc (« le dépôt qui porte le programme ») ne change pas : un programme qui écrit à côté de lui-même,
                # par __file__, se voit ici (relecteur du tour 5, I-T5-1 ; dents : S25 et S26).
                apres_banc = etat(banc)
                if apres_banc != avant_banc:
                    raisons.append("banc changé : " + ecart(avant_banc, apres_banc))
                if raisons:
                    faux.append(f"{nom} ({', '.join(raisons)})")
                return code
            except Exception as e:
                pannes.append(f"{nom} (l'épreuve n'a pas pu juger : {type(e).__name__})")
                return None

        def simple(refaire=None, sortie=None):
            def preparer(c):
                # La racine et la sortie ont des parents DIFFÉRENTS : confondre « à côté de la sortie » et « à côté de la
                # racine » se voit (variante VC du relecteur du tour 5).
                r = copie(c, base, nom=os.path.join("entree", "racine"), refaire=refaire)
                os.makedirs(os.path.join(c, "sorties"))
                return r, sortie(c, r) if sortie else os.path.join(c, "sorties", "sortie")
            return preparer

        def avec_voisin(chemin, fichier, sortie="sortie"):
            def preparer(c):
                os.makedirs(os.path.join(c, "sorties", chemin))
                if fichier:
                    open(os.path.join(c, "sorties", chemin, fichier), "w").write("intact")
                return copie(c, base, nom=os.path.join("entree", "racine")), os.path.join(c, "sorties", sortie)
            return preparer

        reponse = lambda s: os.path.join(BRUTS, s + ".json")
        juger("E1", simple(), 0, "écrit", avec_sortie=True)
        juger("E2", simple((reponse("AC.PA"), chiffre_change)), 1, "REFUSÉ")
        juger("E3", simple((reponse("AI.PA"), lambda b: None)), 1, "REFUSÉ")
        juger("E4", simple((CARNET, carnet_change(lambda r: [dict(r, sha256="0" * 64) if acpa(r) else r]))),
              1, "REFUSÉ")
        juger("E5", simple((CARNET, carnet_change(lambda r: [] if acpa(r) else [r]))), 1, "REFUSÉ")
        juger("E6", simple((CARNET, carnet_change(lambda r: [r, r] if acpa(r) else [r]))), 1, "REFUSÉ")
        juger("E7", simple((CARNET, carnet_change(
            lambda r: [dict(r, produit_par="écrit à la main") if acpa(r) else r]))), 1, "REFUSÉ")
        juger("E8", simple((reponse("MT.PA"), chiffre_change)), 1, "REFUSÉ")
        juger("E9", simple(sortie=lambda c, r: os.path.join(r, "sortie_dans_la_racine")), 2, "IMPOSSIBLE")
        juger("E10", avec_voisin("existe", "temoin.txt", "existe"), 2, "IMPOSSIBLE")
        juger("E10b", avec_voisin("existe_vide", None, "existe_vide"), 2, "IMPOSSIBLE")
        juger("E11", simple((REF, lambda b: None)), 2, "IMPOSSIBLE")
        juger("E12", lambda c: (None, None), 2, "IMPOSSIBLE", sans_args=True)
        mal = b'{"chart":{"result":null,"error":null}}'
        def prep_e13(c):
            r = copie(c, base, nom=os.path.join("entree", "racine"), refaire=(CARNET, carnet_change(
                lambda x: [dict(x, sha256=hashlib.sha256(mal).hexdigest()) if acpa(x) else x])))
            os.remove(os.path.join(r, reponse("AC.PA")))
            open(os.path.join(r, reponse("AC.PA")), "wb").write(mal)
            os.makedirs(os.path.join(c, "sorties"))
            return r, os.path.join(c, "sorties", "sortie")
        juger("E13", prep_e13, 2, "IMPOSSIBLE")

        def inverse(b):
            t = b.decode("utf-8-sig").splitlines(keepends=True)
            return (t[0] + "".join(reversed(t[1:]))).encode("utf-8")
        juger("E14", simple((REF, inverse)), 0, "écrit", avec_sortie=True)
        # 15-01-2025 à 23h30 et à 12h00 en temps universel (heure d'hiver : Paris = temps universel + 1 h)
        juger("E15", lambda c: (None, None), 0, exact="2025-01-16 2025-01-15\n", lanceur=LANCEUR_E15, sans_args=True)
        juger("E16", avec_voisin("sortie.en_cours.ancien", "precieux.txt"), 2, "IMPOSSIBLE", lanceur=LANCEUR_E16)
        # E17 — la coupure à CHAQUE geste qui modifie le disque : pour k = 1, 2, 3…, le programme est arrêté net au
        # k-ième geste ; à chaque coupure (code 3), pas de sortie, seuls des provisoires à côté d'elle ; le dernier k le
        # laisse finir (code 0, les deux empreintes). Finir dès k = 1 veut dire que la coupure n'a rien vu : faux.
        for k in range(1, 51):
            code = juger(f"E17k{k}", simple(), (3, 0), lanceur=LANCEUR_COUPURE.replace("K_ICI", str(k)),
                         provisoires=True, avec_sortie=True)
            if code != 3:
                if k == 1 and code == 0:
                    faux.append("E17 (aucun geste d'écriture vu : la coupure n'a rien coupé)")
                break
        else:
            faux.append("E17 (plus de 50 gestes d'écriture)")
        # E18 porte aussi le provisoire d'un AUTRE lancement, au nom exact de ceux de mkdtemp : un nettoyage par motif
        # fait après un succès l'effaçait (relecteur du tour 6, V1 ; dent : S32).
        def prep_e18(c):
            r, s = avec_voisin("sortie.en_cours", "precieux.txt")(c)
            os.makedirs(os.path.join(c, "sorties", "sortie.en_cours.ancien"))
            open(os.path.join(c, "sorties", "sortie.en_cours.ancien", "precieux.txt"), "w").write("intact")
            return r, s
        juger("E18", prep_e18, 0, "écrit", avec_sortie=True)
        juger("E19", simple(sortie=lambda c, r: os.path.join(banc, "sortie_E19")), 2, "IMPOSSIBLE")
        def prep_e20(c):
            r = copie(c, base, nom=os.path.join("entree", "e20"))
            return r, r + "_voisin"
        juger("E20", prep_e20, 0, "écrit", avec_sortie=True)
        juger("E21", simple(sortie=lambda c, r: os.path.join(c, "sorties", "parent_absent", "sortie")), 2,
              "IMPOSSIBLE")
        # E22, E23 — la garde « chemins résolus » : un lien vers la racine ne fait pas sortir de la racine
        # (superviseur du tour 5, R6 : avec abspath au lieu de realpath, le programme écrivait dans la racine).
        def prep_e22(c):
            r = copie(c, base, nom=os.path.join("entree", "racine"))
            os.symlink(r, os.path.join(c, "lien"))
            return r, os.path.join(c, "lien", "sortie")
        juger("E22", prep_e22, 2, "IMPOSSIBLE")
        def prep_e23(c):
            r = copie(c, base, nom=os.path.join("entree", "racine"))
            os.symlink(r, os.path.join(c, "lien"))
            return os.path.join(c, "lien"), os.path.join(r, "sortie")
        juger("E23", prep_e23, 2, "IMPOSSIBLE")
        # E24 — le programme lancé par un lien vers le banc, sortie dans le vrai banc : la garde « chemins résolus » du
        # dépôt qui porte le programme (relecteur du tour 6, V2 ; dent : S33).
        def prep_e24(c):
            r = copie(c, base, nom=os.path.join("entree", "racine"))
            os.symlink(banc, os.path.join(c, "lien_banc"))
            return r, os.path.join(banc, "sortie_E24")
        juger("E24", prep_e24, 2, "IMPOSSIBLE", module_=lambda c: os.path.join(c, "lien_banc", "programmes", NOM))
        return faux, pannes
    finally:
        shutil.rmtree(base, ignore_errors=True)


def sources_du_depot():
    """Rend l'état des trois sources du dépôt éprouvé.

    ① RÔLE — Prouver que l'épreuve ne change rien au dépôt. ② CONTEXTE D'APPEL — `main`, au début et à la fin.
    ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : {chemin : empreinte, marque ou état}. [rend: 1]
    ⑥ TRAITEMENT — `empreinte` du référentiel et du carnet, `etat` du dossier des réponses. ⑦ UNITÉ — —
    ⑧ POURQUOI — Ceinture du banc (superviseurs des tours 3 et 4, 23-10-2026) : le reste du dépôt est couvert par le
    contrôle nocturne des empreintes de toute la chaîne, décidé à 16h33. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return {REF: empreinte(os.path.join(DEPOT, REF)), CARNET: empreinte(os.path.join(DEPOT, CARNET)),
            BRUTS: etat(os.path.join(DEPOT, BRUTS))}


def epreuve():
    """L'épreuve entière, sans le dernier filet (voir `main`) ; rend le code de sortie.

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — La ligne de commande (sys.argv).
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir la fiche en tête, ⑤). [rend: 1]
    ⑥ TRAITEMENT — Z0 ; puis, avec --saboter ou --saboter=<noms> et si Z0 est vert, les témoins négatifs et les
      sabotages demandés ; une ligne par sabotage ; la ceinture des sources du dépôt ; le VERDICT.
    ⑦ UNITÉ — — ⑧ POURQUOI — --saboter=<noms> : tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py joue la série par lots
      ainsi ; la ligne qui les lit reprend celle des cinq épreuves qui le font déjà (BACKLOG A-599 ⑬ b : un lecteur
      commun manque). ⑨ CE QUI CLOCHE — — ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    depot_avant = sources_du_depot()
    texte = open(MODULE, encoding="utf-8").read()
    deux, un = False, False
    faux, pannes = tour(texte)
    if faux is None:
        print("Z0 programme tel quel : NE SE CHARGE PAS")
        un = True
    else:
        print("Z0 programme tel quel : " + ("E1 à E24 conformes" if not faux else "FAUX " + ", ".join(faux)))
        un = un or bool(faux)
        if pannes:
            print("Z0 PANNE DU JUGE : " + ", ".join(pannes))
            deux = True
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        if un or deux:
            print("sabotages non joués : Z0 rouge")
        else:
            for nom in (choix[0] if choix else []):
                if nom not in SABOTAGES:
                    print(f"{nom} N'EXISTE PAS dans SABOTAGES")
                    deux = True
            for nom, tete in TEMOINS_NEGATIFS.items():
                f, _ = tour(tete + texte)
                print(f"TÉMOIN NÉGATIF {nom} : " + ("reconnu, ne se charge pas" if f is None else
                                                     "NON RECONNU — LE BANC NE TIENT PAS"))
                deux = deux or f is not None
            for nom, remplacements in SABOTAGES.items():
                if choix and nom not in choix[0]:
                    continue
                t = texte
                applicable = True
                for a, b in remplacements:
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS ({t.count(a)} fois) : {a[:60]!r}")
                        applicable = False
                        break
                    t = t.replace(a, b)
                if not applicable:
                    deux = True
                    continue
                f, p = tour(t)
                if f is None:
                    # Convention de l'écosystème (cassure N de Cowork, 17-10-2026) : un sabotage qu'on ne peut pas
                    # jouer ne mord pas, et la sortie vaut 2.
                    print(f"{nom} NE PEUT PAS ÊTRE JOUÉ : le programme saboté ne se charge pas")
                    deux = True
                    continue
                if p:
                    print(f"{nom} NE PEUT PAS ÊTRE JOUÉ : panne du juge {p}")
                    deux = True
                    continue
                print(f"{nom} {'mord' if f else 'NE MORD PAS'} {f}")
                un = un or not f
    if sources_du_depot() != depot_avant:
        print("LE DÉPÔT A CHANGÉ PENDANT L'ÉPREUVE (référentiel, carnet ou réponses)")
        deux = True
    code = 2 if deux else 1 if un else 0
    print("VERDICT : tout est conforme" if code == 0 else
          "VERDICT : NON CONFORME" if code == 1 else "VERDICT : L'ÉPREUVE N'A PAS PU JUGER")
    return code


def main():
    """Lance l'épreuve sous un dernier filet : toute erreur imprévue rend 2 et écrit son VERDICT.

    ① RÔLE — Garantir qu'une épreuve qui n'a pas pu juger ne rende jamais 0 ni 1. ② CONTEXTE D'APPEL — La ligne de
    commande. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — `epreuve()` dans un try ; BaseException (hors interruption au clavier) → « VERDICT : L'ÉPREUVE N'A
      PAS PU JUGER », 2. ⑦ UNITÉ — — ⑧ POURQUOI — Relecteur du tour 4 (23-10-2026, P-T4-3) : un dépôt sans référentiel
      faisait tomber l'épreuve sur une trace, code 1 (« non conforme »), sans VERDICT ; superviseur du même jour : le
      filet est dans `main`, pas dans `tour`. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        return epreuve()
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        print(f"VERDICT : L'ÉPREUVE N'A PAS PU JUGER — {type(e).__name__} : {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
