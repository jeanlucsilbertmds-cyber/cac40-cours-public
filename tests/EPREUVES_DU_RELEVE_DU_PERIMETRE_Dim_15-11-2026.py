#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_RELEVE_DU_PERIMETRE — Dim 15-11-2026 (Paris)

Simulation boursière uniquement : rien ici ne touche aux cours ni aux positions.

À QUOI ÇA SERT. Prouver que programmes/RELEVER_LE_PERIMETRE.py rend, pour chaque ressource, un verdict tiré des seuils
de donnees/REGLAGES_DU_PERIMETRE.csv et de nulle part ailleurs (R-708), rend INCONNU pour une ressource absente
(jamais un chiffre inventé), rend SATURÉ sous une charge simulée, et n'écrit rien dans le dépôt réel. Décision de
Jean-Luc du 15-11-2026 à 12h50 (A-805) : à chaque regard d'optimisation, le périmètre est relevé par un programme et
montré à Jean-Luc.

LANCEMENT : python3 -B tests/EPREUVES_DU_RELEVE_DU_PERIMETRE_Dim_15-11-2026.py <racine> [--saboter]
  Sans option : les épreuves sur programmes/RELEVER_LE_PERIMETRE.py de <racine>. Code 0 si toutes vertes, 1 sinon.
  --saboter : les épreuves, puis chaque sabotage sur une COPIE du programme dans un dossier temporaire ; chacun doit
  faire rougir l'épreuve nommée (seule cette épreuve est rejouée, pour le temps). Un sabotage dont le texte n'est pas
  trouvé, ou qui laisse son épreuve verte, rend le code 1 (R-734).

LES RESSOURCES SONT FABRIQUÉES dans un dossier temporaire : un faux /proc (loadavg, meminfo, processus), une fausse
commande `nproc` en tête du PATH, un faux /tmp, un faux dépôt, un faux programme du forfait, et pour P3 une place
libre de disque fabriquée (LANCEUR_DISQUE remplace `shutil.disk_usage` : la série est la même sur toute machine).
Seul P12 lit le vrai.

LES ÉPREUVES :
  P1 CHARGE SIMULÉE : loadavg 9,00 sur 2 cœurs → Cœurs SATURÉ, critère « 4,50 ».
  P2 BORDS (seuils 1,0 et 0,5, fenêtre 5 min, 2 cœurs) : charge 2,00 → SATURÉ (≥) · 1,98 → JUSTE · 1,00 → JUSTE
     (0,50 n'est pas < 0,50) · 0,98 → SOUS-EMPLOYÉ.
  P3 LES SEUILS VIENNENT DU FICHIER : cœurs 0,75 par cœur → JUSTE, puis SATURÉ (seuil 0,7), puis SOUS-EMPLOYÉ (seuil
     bas 0,8) · mémoire 0,30 disponible → JUSTE, SATURÉ (0,4), SOUS-EMPLOYÉ (0,2) · disque (place libre FABRIQUÉE :
     7 Go, jamais le vrai disque — D-1 du relecteur neuf du 16-11-2026) : « 7,0 Go libres » affiché, seuil 0 → JUSTE,
     10^12 Go → SATURÉ · /tmp : 1000 Go → JUSTE, 0 → SATURÉ · fenêtre 1 min avec charges 9 / 0,2 / 0,2 → SATURÉ, 5 min →
     SOUS-EMPLOYÉ.
  P4 RESSOURCES ABSENTES : pas de `nproc` dans le PATH, /proc inexistant, disque, /tmp, clone public et programme du
     forfait inexistants, dépôt Git SANS origine → sept lignes INCONNU sans aucun chiffre dans « Existe » et
     « Utilisé », la ligne des circuits sans chiffre inventé, code 0, 9 lignes. (Les copies de travail se mesurent :
     0 est une mesure.)
  P4b RACINE QUI N'EST PAS UN DÉPÔT (D-5 du RELU du 15-11-2026) → code 2, « ERREUR RACINE », aucun tableau.
  P5 ÉPREUVES EN COURS (S-1 du RELU ; N-3 et N-5 de la seconde relecture) : vingt-deux processus fabriqués, chacun
     avec son parent (`status`, ligne PPid). Une épreuve qui a une épreuve parmi ses descendants n'est pas comptée :
     seul le bout de chaque chaîne l'est. Comptés (12) :
     `/usr/bin/python3.11 -B /x/tests/B.py` · `python3 -I programmes/EPREUVES_P.py --mutations` (déclarée sans
     argument dans le faux tests/LANCEMENT_DES_EPREUVES.json) · `python3 EPREUVES_D.py` lancé depuis un dossier tests
     (lien cwd) · `python tests/E.py` (python sans 3) · `python3 --check-hash-based-pycs always tests/G.py` ·
     `python3 programmes/TENIR_P.py . --calibrage` (déclarée avec `{copie}` et `--calibrage`) ·
     `python3 /r/programmes/DECL.py /r/donnees/x.csv` (déclarée avec `donnees/x.csv`) ·
     `python3 tests/K.py --sortie /x/rapport.txt` · `python3 tests/EPREUVES_A.py --cas /tmp/y`, ENFANT de 101 (101,
     l'épreuve qui se relance, n'est pas comptée en plus) · `python3 tests/H.py`, petit-enfant de 101 par un
     programme qui n'est pas une épreuve · `tests/L1.py` et `tests/L2.py`, lancés en parallèle par
     `tests/outils/LANCEUR.py` (qui n'est pas compté en plus). Exclus : `python3 -B programmes/RELEVER_LE_PERIMETRE.py --tmp
     /x/tests/` · `bash tests/d.sh` · `python3 programmes/C.py` · `python3 -c tests/x` · `python3 -Bc tests/x.py`
     (lettres collées) · `python3 programmes/TENIR_P.py .` (production, sans `--calibrage`) · `python3
     programmes/DECL.py autre.csv` · `python3 tests/EPREUVES_A.py` (101) et `tests/outils/LANCEUR.py`, têtes de
     chaînes. D-3 du relecteur neuf du 16-11-2026 : `python3 programmes/CHK.py epreuves` (déclarée avec l'argument
     `epreuves`, qui n'est pas un chemin) est comptée ; `python3 programmes/CHK.py /x/epreuves` ne l'est pas (un mot
     sans barre oblique n'est jamais une fin de chemin). Total compté : 13. Sur 13 cœurs → « 13 épreuves », 1,00 →
     JUSTE ; sur 12 cœurs → SATURÉ.
  P6 MÉMOIRE SANS MemAvailable → INCONNU.
  P7 COPIES DE TRAVAIL (S-2 du RELU) : un dépôt et deux copies de travail, dont une effacée du disque → « 1 hors
     dépôt principal » ; seuil 1 → SATURÉ, seuil 2 → JUSTE.
  P8 COPIES DANS /tmp : a/.git dossier, b/.git fichier, c/ sans .git, un fichier → « 2 copies du dépôt sur 3
     dossiers ».
  P9 COWORK : une origine nue, son clone rapatrié EN ENTIER (`git fetch origin`), puis l'adresse de l'origine
     remplacée par une adresse de réseau, et `FETCH_HEAD` réécrit comme Git l'aurait écrit pour cette adresse
     (`rapatrier` : aucun réseau n'est contacté ; le relevé ne rapatrie rien). main porte une relecture cowork du 08-11 ;
     quatre branches. travail-a : relu par cowork puis note neuve → en attente. travail-b : note puis relu par cowork le
     10-11 → à jour. travail-c : note, puis RELU.md changé par « Chat » → en attente. travail-d : relu par cowork le
     12-11 à 08h00 UTC, puis note DÉPOSÉE à 09h00 avec une date d'AUTEUR de 07h00 (note re-déposée par amend) → en
     attente (date de dépôt, pas d'auteur). Attendu : « 4 branches travail-* », « dernière relecture 12-11 09h00 ;
     3 en attente : travail-a, travail-c, travail-d », date du rapatriement écrite ; seuil d'attente 4 → SOUS-EMPLOYÉ
     (silence > 6 h) ; seuil 3 → SATURÉ ; seuil 4 et silence 10^6 h → JUSTE.
  P9b CLONE À UNE SEULE BRANCHE (cas réel du 15-11-2026 à 13h06), puis `git fetch origin` (un FETCH_HEAD complet
     pour cette branche, pour que seul le motif de rapatriement puisse rougir) → Cowork INCONNU, raison « une seule
     branche », traces des circuits INCONNU.
  P9c ORIGINE QUI EST UNE COPIE LOCALE (D-1 a du RELU) : clone d'un clone de la machine, puis `git fetch origin` →
     Cowork et traces INCONNU, raison « copie sur cette machine ».
  P9d RAPATRIEMENT D'UNE SEULE BRANCHE (D-1 b du RELU) : clone complet, puis `git fetch origin travail-a` → Cowork et
     traces INCONNU, raison « rapatriement partiel ».
  P9e AUCUNE BRANCHE travail-* (S-3 du RELU) : références travail-* effacées du clone → « 0 branches travail-* »,
     « dernière relecture 08-11 10h00 » (celle de main).
  P9f CLONE SUPERFICIEL (S-2 du RELU) : clone `--depth 1 --no-single-branch` → le critère le signale.
  P9g RAPATRIEMENT VENU D'UN AUTRE DÉPÔT (N-1 de la seconde relecture) : clone complet, puis `git fetch miroir`, un
     second dépôt aux mêmes noms de branches → Cowork et traces INCONNU, raison « venu d'ailleurs ».
  P9h AUCUN RAPATRIEMENT DEPUIS LE CLONE (N-6 a) : clone complet sans `git fetch`, origine remise sur l'adresse de
     réseau → Cowork et traces INCONNU, raison « aucun rapatriement ».
  P9i ORIGINE RÉÉCRITE VERS UNE COPIE LOCALE (N-6 c) : `url.<copie locale>.insteadOf <adresse de réseau>` → Cowork
     INCONNU, raison « copie sur cette machine ».
  P9j BRANCHE SUPPRIMÉE AU DÉPÔT PARTAGÉ (N-2) : `travail-b` supprimée à l'origine ; `git fetch origin` sans
     `--prune` → INCONNU, et le conseil rendu dit `--prune` ; puis `git fetch --prune origin` → « 3 branches
     travail-* ».
  P9k ADRESSE AVEC IDENTIFIANTS (D-4 du relecteur neuf du 16-11-2026) : origine `faux://utilisateur:secret@…`,
     rapatriée par Git LUI-MÊME (`rapatrier_par_git` : une aide de transport locale, aucun réseau ; FETCH_HEAD n'est
     pas réécrit) → FETCH_HEAD dit « of faux://depot-partage.invalid/depot », sans identifiants, et Cowork n'est pas
     INCONNU (« 4 branches travail-* »). Retirer des identifiants est donc nécessaire pour reconnaître l'origine.
  P9l FORME `utilisateur@hôte:chemin` (même D-4) : même chose par une fausse commande ssh → « of
     depot-partage.invalid:depot ».
  P10 FORFAIT (faux programme, seuil 95 dans SA sortie, écart 10 dans le réglage) : code 4 → SATURÉ · code 3 → JUSTE ·
     code 0 projection 50,0 → SOUS-EMPLOYÉ, 84,9 → SOUS-EMPLOYÉ, 85,0 → JUSTE, 105,0 → JUSTE, 105,1 → SATURÉ ·
     84,9 avec un écart de 20 → JUSTE · projection INCONNUE → INCONNU · code 5 → INCONNU · programme qui dort 30 s
     avec un délai de 2 s → INCONNU, et le relevé finit en moins de 20 s.
  P10b FORFAIT, VRAI PROGRAMME (C-2 de Cowork, 25-11-2026) : TENIR_LE_FORFAIT.py de <racine>, copié, sur un journal
     fabriqué relatif à l'horloge (10 % il y a 2 h, un agent, 20 % il y a 1 h) → la colonne « utilisé » commence par
     « jauge 3 » (30,0 % : 20 + 10 points/h × 1 h), jamais « jauge INCONNU ». Sabotage S51 : l'ancien libellé
     « ESTIMÉE » remis au motif de lecture → « jauge INCONNU ».
  P11 CIRCUITS : 2 fichiers privés (.yml, .yaml ; un .txt ignoré), 2 publics dont series_longues.yml → verdict
     INCONNU, critère « non visible » ; sans clone public → « publics INCONNU ».
  P12 VRAIES DONNÉES ET LECTURE SEULE (R-732 ; D-2 du RELU, N-7 de la seconde relecture) : un clone du vrai dépôt
     <racine> par `file://` à une profondeur de 1 (vrais fichiers et vrais réglages de la pointe, sans l'histoire),
     sans `alternates` (vérifié), le vrai /proc, le vrai /tmp → code 0, 9 lignes, verdicts dans l'ensemble permis,
     « <nproc> cœurs », circuits INCONNU, compte des verdicts = 9 ; et RIEN n'a changé dans ce clone : ni
     `git status --porcelain`, ni la liste des références (`git for-each-ref` et HEAD), ni aucun fichier du dossier
     `.git`, `index` compris (chemin, taille, date de modification ET empreinte SHA-256 du contenu ; l'empreinte se
     prend après un `git status`, qui rafraîchit l'index). Le clone ne partage aucun objet avec le vrai dépôt : un
     sabotage qui écrit n'écrit que dans le clone. (La seconde relecture avait fait écrire un sabotage dans le VRAI
     dépôt par les `alternates` d'un clone `--shared`, P12 restant vert.)
  P13 RÉGLAGE illisible ou absurde (D-3 du RELU, N-4 de la seconde relecture) : un réglage absent, un en double, le
     fichier manquant, puis `nan`, `inf`, un négatif, un délai nul, un délai de 3601 s, un délai de 1e300, un nombre
     de copies de 2,5, un nombre de copies écrit `1_0`, une fenêtre de 7 minutes, des seuils de mémoire croisés, des
     seuils de cœurs croisés → code 2, « ERREUR RÉGLAGE », aucun tableau.
  P14 DÉLAI DÉPASSÉ (D-4 du RELU) : un faux `nproc` qui dort 5 s, délai 1 s → critère des cœurs « sans réponse en
     1 s », jamais « introuvable » ; un faux `git` qui dort 5 s → code 2, « ERREUR RACINE », « sans réponse ».
  P15 ARRONDI (S-4 du RELU) : charge 5 min 1,9998 sur 2 cœurs (0,9999 par cœur, seuil 1,00) → JUSTE, et la valeur
     affichée n'est pas « 1,00 ».

LES SABOTAGES : chacun change UN texte d'une COPIE du programme et doit faire rougir l'épreuve nommée POUR SA PROPRE
RAISON : le détail de l'épreuve rouge doit contenir la marque donnée (un sabotage qui rougit pour une autre raison ne
compte pas). La liste est dans SABOTAGES, ci-dessous.
"""
import json, os, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PROG = "RELEVER_LE_PERIMETRE.py"
PARIS = ZoneInfo("Europe/Paris")
VERDICTS = {"SOUS-EMPLOYÉ", "JUSTE", "SATURÉ", "INCONNU"}
RESEAU = "https://depot-partage.invalid/depot.git"  # adresse de réseau jamais contactée : le relevé ne rapatrie rien
# Place libre FABRIQUÉE pour P3 (D-1 du relecteur neuf du 16-11-2026) : la série rendait vert ou rouge selon la place
# libre du VRAI disque (S3 mordait pour une autre raison sous 5 Go libres). P3 ne lit plus le vrai disque : le
# programme est lancé par LANCEUR_DISQUE, qui remplace `shutil.disk_usage` par une mesure qui rend cette valeur.
LIBRE_FABRIQUE = 7 * 10 ** 9  # octets ; « 7,0 Go libres » attendu dans la ligne Disque
LANCEUR_DISQUE = """import os, runpy, shutil, sys
from collections import namedtuple
libre, prog = int(sys.argv[1]), sys.argv[2]
vrai = shutil.disk_usage
Mesure = namedtuple("Mesure", "total used free")


def fabriquee(dossier):
    vrai(dossier)  # un dossier absent lève OSError, comme sans le lanceur
    return Mesure(4 * libre, 3 * libre, libre)


shutil.disk_usage = fabriquee
sys.argv = [prog] + sys.argv[3:]
sys.path[0] = os.path.dirname(prog)
runpy.run_path(prog, run_name="__main__")
"""
# Adresses de réseau AVEC identifiants (D-4 du relecteur neuf du 16-11-2026) : P9k et P9l les font rapatrier par Git
# lui-même, par un faux transport local, pour MESURER ce que Git écrit dans FETCH_HEAD au lieu de le fabriquer.
RESEAU_IDENTIFIE = "faux://utilisateur:secret@depot-partage.invalid/depot.git"
RESEAU_SCP = "utilisateur@depot-partage.invalid:depot.git"
# Valeurs des ÉPREUVES (pas celles du dépôt) : chaque cas les fixe lui-même ; les NOMS doivent être ceux du vrai
# fichier de réglage (vérifié par `reglages_de_base`).
BASE = {"coeurs_fenetre_minutes": 5, "coeurs_charge_par_coeur_saturee": 1.0,
        "coeurs_charge_par_coeur_sous_employee": 0.5, "memoire_part_disponible_saturee": 0.10,
        "memoire_part_disponible_sous_employee": 0.50, "disque_libre_sature_go": 0, "epreuves_par_coeur_saturees": 1.0,
        "epreuves_par_coeur_sous_employees": 0.5, "worktrees_nombre_sature": 10, "copies_tmp_go_saturees": 1000,
        "cowork_attente_saturee": 3, "cowork_silence_heures_sous_employe": 6, "forfait_ecart_points": 10,
        "delai_de_mesure_secondes": 20}

# nom → (épreuve qui doit rougir, texte du programme, texte saboté, marque attendue dans le détail de l'épreuve rouge)
# Les comptes de P5 marqués ci-dessous incluent `programmes/CHK.py epreuves` (pid 123, ajouté pour D-3 le 16-11-2026),
# compté sous tout sabotage qui laisse lire les arguments déclarés : d'où +1 sur S27, S40, S41, S42, S47, et +2 sur S39
# (qui compte aussi le pid 124, `/x/epreuves`).
SABOTAGES = {
    "S1_seuil_coeurs_en_dur": ("P3", 'v = juger_par_seuils(par_coeur, r["coeurs_charge_par_coeur_saturee"],',
                               'v = juger_par_seuils(par_coeur, 1.0,', "coeurs 0,7"),
    "S2_seuils_memoire_en_dur": ("P3", 'r["memoire_part_disponible_saturee"], r["memoire_part_disponible_sous_employee"], False)',
                                 '0.10, 0.50, False)', "mémoire 0,4"),
    # Le seuil en dur vaut 1 Go, sous la place fabriquée (7 Go) : ce n'est pas une copie du réglage du dépôt (R-708).
    "S3_seuil_disque_en_dur": ("P3", 'r["disque_libre_sature_go"], None, False)', '1, None, False)', "disque 1e12"),
    "S4_coeurs_inventes": ("P4", 'm["pourquoi"] = echec("nproc", code, raison)', 'm["coeurs"] = 4', "Cœurs"),
    "S5_forfait_absent_juste": ("P4", 'return ["Forfait", INCONNU, INCONNU, INCONNU, m["pourquoi"]]',
                                'return ["Forfait", "seuil 95 %", "jauge 0 %", "JUSTE", m["pourquoi"]]', "Forfait"),
    "S6_bord_strict": ("P2", "if valeur >= sature:", "if valeur > sature:", "'2.00': ('JUSTE', 'SATURÉ')"),
    "S7_tout_processus_compte": ("P5", "        lance = fichier_lance(mots)\n", "        lance = (mots or ['x'])[-1]\n",
                                 "10 épreuves"),
    "S8_filtre_cowork_retire": ("P9",  ' and "cowork" in l.split("\\t", 1)[1].lower()', "",
                                "2 en attente : travail-a, travail-d"),
    "S9_tout_dossier_est_copie": ("P8", 'if os.path.exists(os.path.join(d, ".git")))', "if True)", "3 copies"),
    "S10_circuits_juges": ("P11", "traces, INCONNU,", 'traces, "JUSTE",', "JUSTE"),
    "S11_forfait_toujours_juste": ("P10", 'v = "SATURÉ" if p > m["seuil"] + e else "SOUS-EMPLOYÉ" if p < m["seuil"] - e else "JUSTE"',
                                   'v = "JUSTE"', "proj 50,0"),
    "S12_fenetre_ignoree": ("P3", 'm["charges"][fenetres[f]]', 'm["charges"][1]', "fenêtre 1"),
    "S13_sans_delai": ("P10", "timeout=delai)", "timeout=None)", "dort 30 s"),
    "S14_memavailable_absente": ("P6", 'if not m["total"] or m["disponible"] is None:', 'if not m["total"]:',
                                 "mémoire jugée sans MemAvailable"),
    "S15_clone_une_branche_accepte": ("P9b", 'if not any("refs/heads/*" in l for l in motifs.splitlines()):',
                                      "if False:", "en attente"),
    "S16_seuil_worktrees_en_dur": ("P7", 'r["worktrees_nombre_sature"], None, True)', "10**6, None, True)", "seuil 1"),
    "S17_depot_principal_compte": ("P7", 'if l.startswith("worktree ")][1:]', 'if l.startswith("worktree ")]',
                                   "2 hors dépôt principal"),
    "S18_copie_effacee_comptee": ("P7", "chemins = [c for c in chemins if os.path.isdir(c)]", "chemins = list(chemins)",
                                  "2 hors dépôt principal"),
    "S19_silence_en_dur": ("P9", 'silence > r["cowork_silence_heures_sous_employe"]', "silence > 6", "'silence 10^6': 'SOUS-EMPLOYÉ'"),
    "S20_ecart_forfait_en_dur": ("P10", 'e = r["forfait_ecart_points"]', "e = 10", "écart 20"),
    "S21_superficiel_muet": ("P9f", 'if m["superficiel"] else "")', 'if False else "")', "superficiel"),
    "S22_origine_locale_acceptee": ("P9c", "    if origine_sur_cette_machine(url.strip()):", "    if False:", "en attente"),
    "S23_rapatriement_partiel_accepte": ("P9d", "    if vieilles:", "    if False:", "en attente"),
    "S24_relecture_lue_sur_travail_seulement": ("P9e", '"--remotes=origin", "--format=%ct\\t%an"',
                                                '"--remotes=origin/travail-*", "--format=%ct\\t%an"', "dernière relecture aucune"),
    "S25_date_d_auteur": ("P9", '"--format=%ct", b, "--",', '"--format=%at", b, "--",',
                          "2 en attente : travail-a, travail-c"),
    "S26_epreuve_reconnue_par_un_mot": ("P5", '        if "tests" in dossiers or (attendus is not None and all(',
                                        '        if any("tests/" in x for x in mots[1:]) or (False and all(',
                                        "9 épreuves"),
    "S27_dossier_du_processus_ignore": ("P5", 'lance = os.path.join(os.readlink(os.path.join(proc, e, "cwd")), lance)',
                                        "pass", "12 épreuves"),
    "S28_epreuves_declarees_ignorees": ("P5", "attendus = declarees.get(os.path.join(*chemin.split(os.sep)[-2:]))",
                                        "attendus = None", "9 épreuves"),
    "S29_ecrit_une_reference": ("P12", "    taille = mesurer_taille(chemins, delai)\n",
                                '    taille = mesurer_taille(chemins, delai)\n    lancer(["git", "-C", racine, "update-ref", '
                                '"refs/heads/sabotage", "HEAD"], delai)\n', "références changées"),
    "S30_ecrit_dans_git": ("P12", "    taille = mesurer_taille(chemins, delai)\n",
                           '    taille = mesurer_taille(chemins, delai)\n    open(os.path.join(racine, ".git", '
                           '"SABOTAGE"), "w").write("x")\n', "fichiers de .git changés"),
    "S31_bornes_des_reglages_retirees": ("P13", "    if fautes:\n", "    if False:\n", "délai nul"),
    "S32_delai_dit_introuvable": ("P14", 'return None, None, f"sans réponse en {fr(delai, 0)} s"',
                                  'return None, None, "introuvable"', "introuvable"),
    "S33_racine_non_depot_acceptee": ("P4b", "    if code != 0:\n        print(f\"ERREUR RACINE", "    if False:\n        print(f\"ERREUR RACINE",
                                      "PÉRIMÈTRE"),
    "S34_arrondi_qui_contredit": ("P15", "    while d < 9 and valeur != seuil and fr(valeur, d) == fr(seuil, d):",
                                  "    while False:", "1,00"),
    # Seconde relecture de Cowork du 15-11-2026 (pointe 79905bcb) : N-1 à N-7.
    "S35_rapatriement_d_un_autre_depot_accepte": ("P9g", "rafraichies = {nom for nom, venue in lignes if adresse_rapatriee(venue) == origine}",
                                                  "rafraichies = {nom for nom, venue in lignes}", "en attente"),
    "S36_sans_fetch_head_accepte": ("P9h", "    except FileNotFoundError:\n        return (f\"aucun rapatriement",
                                    "    except FileNotFoundError:\n        return None, superficiel, None\n        return (f\"aucun rapatriement",
                                    "en attente"),
    "S37_adresse_ecrite_au_lieu_d_effective": ("P9i", '"ls-remote", "--get-url", "origin"', '"config", "--get", "remote.origin.url"',
                                               "en attente"),
    "S38_conseil_sans_prune": ("P9j", "`git fetch --prune origin`, sans nom", "`git fetch origin`, sans nom",
                               "conseil sans --prune"),
    "S39_arguments_declares_ignores": ("P5", "for a in attendus)):", "for a in [])):", "16 épreuves"),
    "S40_tete_de_chaine_comptee": ("P5", "            if p in epreuves:\n                porteuses.add(p)",
                                   "            if False:\n                porteuses.add(p)", "15 épreuves"),
    "S47_tete_comptee_au_lieu_du_bout": ("P5", "                porteuses.add(p)", "                porteuses.add(e)",
                                         "11 épreuves"),
    "S41_lettres_collees_ignorees": ("P5", '                if lettre in "cm":', "                if False:", "15 épreuves"),
    "S42_option_a_valeur_longue_ignoree": ("P5", 'sauter = m == "--check-hash-based-pycs"', "sauter = False",
                                           "12 épreuves"),
    "S43_index_reecrit": ("P12", "    taille = mesurer_taille(chemins, delai)\n",
                          '    taille = mesurer_taille(chemins, delai)\n    lancer(["git", "-C", racine, "update-index", '
                          '"--index-version", "4"], delai)\n', "fichiers de .git changés"),
    "S44_contenu_reecrit_meme_taille_meme_date": ("P12", "    taille = mesurer_taille(chemins, delai)\n",
                                                  '    taille = mesurer_taille(chemins, delai)\n    _c = os.path.join(racine, ".git", '
                                                  '"description"); _s = os.stat(_c); _t = open(_c).read(); open(_c, "w").write(_t[::-1]); '
                                                  'os.utime(_c, ns=(_s.st_atime_ns, _s.st_mtime_ns))\n', "fichiers de .git changés"),
    "S45_reglage_ecrit_n_importe_comment": ("P13", 'if not re.fullmatch(r"-?[0-9]+(?:[.,][0-9]+)?", brut):', "if False:",
                                            "souligné 1_0"),
    "S46_delai_sans_borne_haute": ("P13", '(vus["delai_de_mesure_secondes"] <= 3600,', "(True,", "délai 3601"),
    # Relecteur neuf du 16-11-2026 (pointe c4fd029d) : D-3 et D-4.
    "S48_fin_de_chemin_pour_un_mot": ("P5", "os.path.normpath(w) == os.path.normpath(a) or (os.sep in os.path.normpath(a) and ",
                                      "os.path.normpath(w) == os.path.normpath(a) or (True and ", "14 épreuves"),
    "S49_identifiants_du_schema_gardes": ("P9k", '    url = re.sub(r"^([A-Za-z][A-Za-z0-9+.-]*://)[^/@]*@", r"\\1", url)\n', "",
                                          "venu d'ailleurs"),
    # Relecture de Cowork du 25-11-2026 (travail-forf2, C-2) : l'ancien libellé du forfait remis
    "S51_jauge_ancien_libelle": ("P10b", 'JAUGE PROJETÉE MAINTENANT : (', 'JAUGE ESTIMÉE MAINTENANT : (', "jauge INCONNU"),
    "S50_identifiants_scp_gardes": ("P9l", '    url = re.sub(r"^[^/:@]+@([^/:]+:)", r"\\1", url)\n', "", "venu d'ailleurs"),
}


def reglages_de_base(racine):
    """Rend les noms du vrai fichier de réglage, et refuse si les épreuves n'ont pas les mêmes."""
    import csv
    with open(os.path.join(racine, "donnees", "REGLAGES_DU_PERIMETRE.csv"), encoding="utf-8", newline="") as f:
        noms = [l["reglage"] for l in csv.DictReader(f)]
    if sorted(noms) != sorted(BASE):
        raise SystemExit(f"ÉPREUVES DÉSACCORDÉES : réglages du dépôt {sorted(noms)} ≠ épreuves {sorted(BASE)}")


def ecrire(chemin, texte, mode=None):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    if mode:
        os.chmod(chemin, mode)


def ecrire_reglages(chemin, **changes):
    v = dict(BASE, **changes)
    ecrire(chemin, "reglage,valeur,etat,qui_decide,raison\n" + "".join(f"{k},{x},x,x,x\n" for k, x in v.items()))


class Banc:
    """Un dossier temporaire avec de fausses ressources ; `lancer` relève le périmètre sur elles."""

    def __init__(self, prog, d):
        self.prog, self.d = prog, d
        self.bin = os.path.join(d, "bin")
        self.coeurs(2)
        self.proc = os.path.join(d, "proc")
        self.charge("0.60 0.60 0.60")
        self.memoire(1000, 300)
        self.tmp = os.path.join(d, "tmp")
        os.makedirs(self.tmp, exist_ok=True)
        self.racine = os.path.join(d, "racine")
        os.makedirs(self.racine, exist_ok=True)
        git(self.racine, "init", "-q")
        self.reglages = os.path.join(d, "reglages.csv")
        ecrire_reglages(self.reglages)
        self.pub = os.path.join(d, "pub_absent")
        self.forfait = os.path.join(d, "forfait_absent.py")
        self.disque = d
        self.libre_fabrique = None  # octets : si donné, la mesure du disque rend cette place libre (LANCEUR_DISQUE)
        self.path = self.bin + os.pathsep + os.environ.get("PATH", "")

    def coeurs(self, n):
        ecrire(os.path.join(self.bin, "nproc"), f"#!/bin/sh\necho {n}\n", 0o755)

    def charge(self, texte):
        ecrire(os.path.join(self.proc, "loadavg"), texte + " 1/100 4242\n")

    def memoire(self, total_ko, dispo_ko):
        ecrire(os.path.join(self.proc, "meminfo"), f"MemTotal: {total_ko} kB\nMemFree: 1 kB\n"
               + (f"MemAvailable: {dispo_ko} kB\n" if dispo_ko is not None else ""))

    def processus(self, pid, mots, cwd=None, ppid=1):
        os.makedirs(os.path.join(self.proc, str(pid)), exist_ok=True)
        ecrire(os.path.join(self.proc, str(pid), "status"), f"Name:\tx\nPPid:\t{ppid}\n")
        with open(os.path.join(self.proc, str(pid), "cmdline"), "wb") as f:
            f.write(b"\0".join(m.encode() for m in mots) + b"\0")
        if cwd:
            os.symlink(cwd, os.path.join(self.proc, str(pid), "cwd"))

    def lancer(self, borne=60, garder=False, **changes):
        if not garder:  # chaque relevé part des réglages de BASE, plus ses changements
            ecrire_reglages(self.reglages, **changes)
        env = dict(os.environ, PATH=self.path)
        tete = [sys.executable, "-B", self.prog]
        if self.libre_fabrique is not None:
            lanceur = os.path.join(self.d, "lanceur_disque.py")
            ecrire(lanceur, LANCEUR_DISQUE)
            tete = [sys.executable, "-B", lanceur, str(self.libre_fabrique), self.prog]
        args = tete + ["--racine", self.racine, "--pub", self.pub, "--reglages",
                self.reglages, "--proc", self.proc, "--tmp", self.tmp, "--disque", self.disque, "--forfait", self.forfait]
        try:
            p = subprocess.run(args, capture_output=True, text=True, env=env, timeout=borne)
        except subprocess.TimeoutExpired:
            return None, "DÉPASSE LA BORNE", {}
        return p.returncode, p.stdout + p.stderr, tableau(p.stdout)


def tableau(sortie):
    t = {}
    for l in sortie.splitlines():
        if l.startswith("| ") and not l.startswith("| Ressource") and not l.startswith("|---"):
            c = [x.strip() for x in l.strip("|").split(" | ")]
            if len(c) == 5:
                t[c[0]] = c[1:]
    return t


def v(t, ressource):
    return t.get(ressource, [None, None, None, None])[2]


def git(cwd, *args, auteur=None, date=None, date_auteur=None, env_en_plus=None):
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, **(env_en_plus or {}))
    if auteur:
        env.update(GIT_AUTHOR_NAME=auteur, GIT_AUTHOR_EMAIL=f"{auteur}@x", GIT_COMMITTER_NAME=auteur,
                   GIT_COMMITTER_EMAIL=f"{auteur}@x")
    if date:
        env.update(GIT_AUTHOR_DATE=date_auteur or date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-c", "init.defaultBranch=main", "-c", "user.name=t", "-c", "user.email=t@x",
                           "-c", "protocol.file.allow=always"] + list(args),
                          cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout


def origine_nue(d):
    """Fabrique une origine nue : main (relecture cowork du 08-11) et quatre branches travail-* ; rend son chemin."""
    src, orig = os.path.join(d, "src"), os.path.join(d, "orig.git")
    os.makedirs(src)
    git(src, "init", "-q")
    ecrire(os.path.join(src, "echanges", "A_RELIRE.md"), "0\n")
    ecrire(os.path.join(src, "echanges", "RELU.md"), "0\n")
    git(src, "add", ".")
    git(src, "commit", "-qm", "base", auteur="Claude", date="2026-11-01T08:00:00+00:00")

    def changer(fichier, auteur, date, date_auteur=None):
        with open(os.path.join(src, "echanges", fichier), "a", encoding="utf-8") as f:
            f.write(date + "\n")
        git(src, "commit", "-qam", fichier, auteur=auteur, date=date, date_auteur=date_auteur)

    changer("RELU.md", "cowork", "2026-11-08T09:00:00+00:00")
    git(src, "checkout", "-qb", "travail-a", "main")
    changer("RELU.md", "cowork", "2026-11-09T08:00:00+00:00")
    changer("A_RELIRE.md", "Claude", "2026-11-09T09:00:00+00:00")
    git(src, "checkout", "-qb", "travail-b", "main")
    changer("A_RELIRE.md", "Claude", "2026-11-10T07:00:00+00:00")
    changer("RELU.md", "cowork", "2026-11-10T08:00:00+00:00")
    git(src, "checkout", "-qb", "travail-c", "main")
    changer("A_RELIRE.md", "Claude", "2026-11-11T07:00:00+00:00")
    changer("RELU.md", "Chat", "2026-11-11T08:00:00+00:00")
    git(src, "checkout", "-qb", "travail-d", "main")
    changer("RELU.md", "cowork", "2026-11-12T08:00:00+00:00")
    changer("A_RELIRE.md", "Claude", "2026-11-12T09:00:00+00:00", date_auteur="2026-11-12T07:00:00+00:00")
    git(d, "clone", "-q", "--bare", src, orig)
    return orig


def rapatrier(clone, *arguments):
    """Rapatrie depuis l'origine nue `orig.git` voisine, puis remet l'adresse de réseau et réécrit `FETCH_HEAD` comme
    Git l'aurait écrit pour cette adresse (sans `.git` final : mesuré le 16-11-2026, git 2.43). Aucun réseau."""
    orig = os.path.join(os.path.dirname(clone), "orig.git")
    git(clone, "remote", "set-url", "origin", "file://" + orig)
    git(clone, *arguments)
    git(clone, "remote", "set-url", "origin", RESEAU)
    chemin = os.path.join(clone, ".git", "FETCH_HEAD")
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte.replace(" of file://" + orig[:-len(".git")] + "\n", " of " + RESEAU[:-len(".git")] + "\n"))


def depot_cowork(d, nom="clone", *options, rapatrier_par=("fetch", "origin")):
    """Clone l'origine nue, rapatrie comme demandé (`rapatrier`), puis donne à l'origine une adresse de réseau ; rend
    le clone."""
    orig = origine_nue(d) if not os.path.isdir(os.path.join(d, "orig.git")) else os.path.join(d, "orig.git")
    clone = os.path.join(d, nom)
    git(d, "clone", "-q", *options, "file://" + orig, clone)
    git(clone, "remote", "set-url", "origin", RESEAU)
    if rapatrier_par:
        rapatrier(clone, *rapatrier_par)
    return clone


def rapatrier_par_git(clone, adresse):
    """Donne à l'origine l'adresse `adresse` (avec identifiants), puis la fait rapatrier par Git LUI-MÊME
    (`git fetch origin`) : `FETCH_HEAD` est celui que Git écrit, il n'est pas réécrit. Le réseau est remplacé par un
    faux transport local vers l'origine nue `orig.git` voisine : pour `faux://…`, une aide de transport
    `git-remote-faux` (capacité `connect`) ; pour la forme `utilisateur@hôte:chemin`, une fausse commande ssh
    (`GIT_SSH_COMMAND`, variante `simple`) qui lance la commande demandée dans le dossier de l'origine. Rend le texte
    de `FETCH_HEAD`."""
    d = os.path.dirname(clone)
    orig = os.path.join(d, "orig.git")
    outils = os.path.join(d, "outils_reseau")
    ecrire(os.path.join(outils, "git-remote-faux"),
           "#!/bin/sh\nwhile read cmd arg; do\n  case \"$cmd\" in\n    capabilities) printf 'connect\\n\\n' ;;\n"
           f"    connect) printf '\\n'; exec git upload-pack '{orig}' ;;\n    *) exit 1 ;;\n  esac\ndone\n", 0o755)
    ecrire(os.path.join(outils, "faux_ssh"), f"#!/bin/sh\nfor a; do last=$a; done\ncd '{d}' && eval \"exec $last\"\n", 0o755)
    if not os.path.exists(os.path.join(d, "depot.git")):
        os.symlink(orig, os.path.join(d, "depot.git"))
    git(clone, "remote", "set-url", "origin", adresse)
    git(clone, "-c", "protocol.faux.allow=always", "fetch", "origin",
        env_en_plus={"PATH": outils + os.pathsep + os.environ.get("PATH", ""),
                     "GIT_SSH_COMMAND": os.path.join(outils, "faux_ssh"), "GIT_SSH_VARIANT": "simple"})
    with open(os.path.join(clone, ".git", "FETCH_HEAD"), encoding="utf-8") as f:
        return f.read()


def empreinte_git(depot):
    """Chemin, taille, date de modification et empreinte SHA-256 du contenu de chaque fichier des dossiers Git du
    dépôt, `index` compris (N-7 de la seconde relecture : taille et date seules laissaient passer un contenu réécrit
    à même taille et date remise, et l'index exclu laissait passer sa réécriture)."""
    import hashlib
    dossiers = set()
    for option in ("--git-dir", "--git-common-dir"):
        x = subprocess.run(["git", "-C", depot, "rev-parse", option], capture_output=True, text=True).stdout.strip()
        dossiers.add(os.path.realpath(x if os.path.isabs(x) else os.path.join(depot, x)))
    vu = {}
    for dossier in sorted(dossiers):
        for base, _, fichiers in os.walk(dossier):
            for f in fichiers:
                c = os.path.join(base, f)
                st = os.lstat(c)
                h = hashlib.sha256()
                if not os.path.islink(c):
                    with open(c, "rb") as fl:
                        for bloc in iter(lambda: fl.read(1 << 20), b""):
                            h.update(bloc)
                vu[c] = (st.st_size, st.st_mtime_ns, h.hexdigest())
    return vu


def epreuves(prog, racine, seulement=None):
    """Joue les cas P1 à P15 sur un programme ; rend la liste (nom, vert ?, détail).

    ① RÔLE — Le corps de l'épreuve (fiche en tête, LES ÉPREUVES). ② CONTEXTE D'APPEL — `main` : une fois sur le
    programme de la racine, puis une fois par sabotage, sur la copie sabotée, avec le seul cas visé.
    ③ ENTRÉE — `prog` : le programme éprouvé · `racine` : le dépôt dont P12 fait un clone · `seulement` : un nom de cas,
    ou None pour tous. ④ CONDITIONS D'ENTRÉE — `du` et `git` installés (P4, P12).
    ⑤ SORTIE — UNE valeur : la liste des cas joués, chacun (nom, vert ?, détail). [rend: 1]
    ⑥ TRAITEMENT — Chaque cas dans son dossier temporaire (`cas`), sur un banc fabriqué (`Banc`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête. Depuis le 17-11-2026 (cause C2), P4 cherche `du` et `git` par des noms écrits en
      clair : voir la fiche de `p4`.
    ⑨ CE QUI CLOCHE — Une exception d'un cas le rend rouge, avec son type et son message.
    ⑩ EFFET — Écrit dans des dossiers temporaires, effacés à la fin de chaque cas.
    ⑪ TERMINAISON — Rend la main ; chaque relevé est borné par `Banc.lancer`.
      [sort: non]
    """
    res = []

    def cas(nom, f):
        if seulement and nom != seulement:
            return
        with tempfile.TemporaryDirectory(prefix="perim_" + nom + "_") as d:
            try:
                ok, detail = f(Banc(prog, d), d)
            except Exception as e:  # une épreuve qui plante est rouge
                ok, detail = False, f"exception {type(e).__name__} : {e}"
        res.append((nom, ok, detail))

    def p1(b, d):
        b.charge("9.00 9.00 9.00")
        code, s, t = b.lancer()
        return code == 0 and v(t, "Cœurs") == "SATURÉ" and "4,50" in t["Cœurs"][3], t.get("Cœurs")
    cas("P1", p1)

    def p2(b, d):
        vus = {}
        for charge, attendu in (("2.00", "SATURÉ"), ("1.98", "JUSTE"), ("1.00", "JUSTE"), ("0.98", "SOUS-EMPLOYÉ")):
            b.charge(f"0.00 {charge} 0.00")
            vus[charge] = (v(b.lancer()[2], "Cœurs"), attendu)
        return all(a == b_ for a, b_ in vus.values()), vus
    cas("P2", p2)

    def p3(b, d):
        b.charge("0.00 1.50 0.00")
        b.libre_fabrique = LIBRE_FABRIQUE
        vus = {}
        vus["coeurs défaut"] = (v(b.lancer()[2], "Cœurs"), "JUSTE")
        vus["coeurs 0,7"] = (v(b.lancer(coeurs_charge_par_coeur_saturee=0.7, coeurs_charge_par_coeur_sous_employee=0.5)[2],
                               "Cœurs"), "SATURÉ")
        vus["coeurs bas 0,8"] = (v(b.lancer(coeurs_charge_par_coeur_sous_employee=0.8)[2], "Cœurs"), "SOUS-EMPLOYÉ")
        vus["mémoire défaut"] = (v(b.lancer()[2], "Mémoire"), "JUSTE")
        vus["mémoire 0,4"] = (v(b.lancer(memoire_part_disponible_saturee=0.4)[2], "Mémoire"), "SATURÉ")
        vus["mémoire bas 0,2"] = (v(b.lancer(memoire_part_disponible_sous_employee=0.2)[2], "Mémoire"), "SOUS-EMPLOYÉ")
        disque = b.lancer()[2].get("Disque", ["", "", "", ""])
        vus["disque 0"] = (disque[2], "JUSTE")
        vus["disque fabriqué"] = (disque[1], f"{LIBRE_FABRIQUE / 1e9:.1f}".replace(".", ",") + " Go libres")
        vus["disque 1e12"] = (v(b.lancer(disque_libre_sature_go=1e12)[2], "Disque"), "SATURÉ")
        vus["tmp 1000"] = (v(b.lancer()[2], "Copies dans /tmp"), "JUSTE")
        vus["tmp 0"] = (v(b.lancer(copies_tmp_go_saturees=0)[2], "Copies dans /tmp"), "SATURÉ")
        b.charge("9.00 0.20 0.20")
        vus["fenêtre 1"] = (v(b.lancer(coeurs_fenetre_minutes=1)[2], "Cœurs"), "SATURÉ")
        vus["fenêtre 5"] = (v(b.lancer()[2], "Cœurs"), "SOUS-EMPLOYÉ")
        faux = {k: x for k, x in vus.items() if x[0] != x[1]}
        return not faux, faux or "13 cas tenus"
    cas("P3", p3)

    def p4(b, d):
        """Le cas P4, ressources absentes : rend (vert ?, détail).

        ① RÔLE — Prouver qu'une ressource absente rend INCONNU, jamais un chiffre inventé (fiche en tête, P4).
        ② CONTEXTE D'APPEL — `cas("P4", p4)`, dans `epreuves`, sur la racine puis sur chaque copie sabotée.
        ③ ENTRÉE — `b` : le banc (`Banc`) ; `d` : son dossier temporaire.
        ④ CONDITIONS D'ENTRÉE — `du` et `git` installés sur la machine (le relevé les lance).
        ⑤ SORTIE — DEUX valeurs : vert ou rouge, et le détail (code, nombre de lignes, lignes fausses). [rend: 2]
        ⑥ TRAITEMENT — Un PATH réduit à `du` et `git` (donc sans `nproc`), /proc, /tmp et disque inexistants ; un
          relevé ; sept lignes INCONNU sans chiffre, la ligne des circuits sans chiffre inventé, code 0, 9 lignes.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — `du` et `git` sont cherchés par `shutil.which("du")` et `shutil.which("git")`, chacun écrit EN
          CLAIR, et non par une boucle sur une variable : l'épreuve E6 du circuit public
          (tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py) lit dans le code chaque logiciel cherché par `which`
          pour vérifier qu'il est installé avant la certification, et refuse un nom qu'elle ne peut pas lire
          (certification de la nuit du 17-11-2026, cause C2, réparation jugée DE FOND par le superviseur R-759).
        ⑨ CE QUI CLOCHE — Un `which` qui rend None (logiciel absent) fait lever `os.symlink` : le cas est rouge par
          exception, sans dire lequel manque.
        ⑩ EFFET — Écrit dans `d` (liens, faux dossiers).
        ⑪ TERMINAISON — Rend la main ; le relevé est borné par `Banc.lancer`.
          [sort: non]
        """
        nu = os.path.join(d, "bin_sans_nproc")
        os.makedirs(nu)
        os.symlink(shutil.which("du"), os.path.join(nu, "du"))
        os.symlink(shutil.which("git"), os.path.join(nu, "git"))
        b.path = nu
        b.proc = os.path.join(d, "proc_inexistant")
        b.tmp = os.path.join(d, "tmp_inexistant")
        b.disque = os.path.join(d, "disque_inexistant")
        code, s, t = b.lancer()
        attendus = ["Cœurs", "Mémoire", "Disque", "Épreuves en cours", "Copies dans /tmp", "Cowork (relecture)", "Forfait"]
        faux = [r for r in attendus if v(t, r) != "INCONNU" or any(ch.isdigit() for ch in t[r][0] + t[r][1])]
        circ = t.get("Circuits GitHub", ["", "", "", ""])
        faux += ["Circuits GitHub"] if any(ch.isdigit() for ch in circ[0] + circ[1]) or circ[2] != "INCONNU" else []
        return code == 0 and len(t) == 9 and not faux, {"code": code, "lignes": len(t), "fausses": faux}
    cas("P4", p4)

    def p4b(b, d):
        b.racine = os.path.join(d, "pas_un_depot")
        os.makedirs(b.racine)
        code, s, t = b.lancer()
        return code == 2 and "ERREUR RACINE" in s and "| Ressource" not in s, (code, s.strip()[:150])
    cas("P4b", p4b)

    def p5(b, d):
        dossier_tests = os.path.join(d, "ailleurs", "tests")
        os.makedirs(dossier_tests)
        ecrire(os.path.join(b.racine, "tests", "LANCEMENT_DES_EPREUVES.json"),
               json.dumps({"epreuves": {"programmes/EPREUVES_P.py": {"dossier": ".", "arguments": []},
                                        "programmes/TENIR_P.py": {"dossier": ".", "arguments": ["{copie}", "--calibrage"]},
                                        "programmes/DECL.py": {"dossier": ".", "arguments": ["donnees/x.csv"]},
                                        "programmes/CHK.py": {"dossier": ".", "arguments": ["epreuves"]}}}))
        for pid, mots, cwd, ppid in (
                (101, ["python3", "tests/EPREUVES_A.py"], None, 1),
                (102, ["/usr/bin/python3.11", "-B", "/x/tests/B.py"], None, 1),
                (103, ["python3", "-I", "programmes/EPREUVES_P.py", "--mutations"], None, 1),
                (104, ["python3", "EPREUVES_D.py"], dossier_tests, 1),
                (105, ["python", "tests/E.py"], None, 1),
                (106, ["python3", "-B", "programmes/RELEVER_LE_PERIMETRE.py", "--tmp", "/x/tests/"], None, 1),
                (107, ["bash", "tests/d.sh"], None, 1),
                (108, ["python3", "programmes/C.py"], None, 1),
                (109, ["python3", "-c", "tests/x"], None, 1),
                (110, ["python3", "-Bc", "tests/x.py"], None, 1),
                (111, ["python3", "--check-hash-based-pycs", "always", "tests/G.py"], None, 1),
                (112, ["python3", "programmes/TENIR_P.py", "."], None, 1),
                (113, ["python3", "programmes/TENIR_P.py", ".", "--calibrage"], None, 1),
                (114, ["python3", "/r/programmes/DECL.py", "/r/donnees/x.csv"], None, 1),
                (115, ["python3", "programmes/DECL.py", "autre.csv"], None, 1),
                (116, ["python3", "tests/EPREUVES_A.py", "--cas", "/tmp/y"], None, 101),
                (117, ["python3", "programmes/C.py"], None, 101),
                (118, ["python3", "tests/H.py"], None, 117),
                (119, ["python3", "tests/K.py", "--sortie", "/x/rapport.txt"], None, 1),
                (120, ["python3", "tests/outils/LANCEUR.py"], None, 1),
                (121, ["python3", "tests/L1.py"], None, 120),
                (122, ["python3", "tests/L2.py"], None, 120),
                (123, ["python3", "programmes/CHK.py", "epreuves"], None, 1),
                (124, ["python3", "programmes/CHK.py", "/x/epreuves"], None, 1)):
            b.processus(pid, mots, cwd, ppid)
        b.coeurs(13)
        t1 = b.lancer()[2]
        b.coeurs(12)
        t2 = b.lancer()[2]
        e1, e2 = t1.get("Épreuves en cours", ["", "", ""]), t2.get("Épreuves en cours", ["", "", ""])
        ok = e1[1] == "13 épreuves" and e1[2] == "JUSTE" and e2[1] == "13 épreuves" and e2[2] == "SATURÉ"
        return ok, ("épreuves vues", e1, e2)
    cas("P5", p5)

    def p6(b, d):
        b.memoire(1000, None)
        code, s, t = b.lancer()
        ok = code == 0 and v(t, "Mémoire") == "INCONNU" and t["Mémoire"][0] == "INCONNU"
        return ok, ("mémoire jugée sans MemAvailable" if not ok else "", t.get("Mémoire") or s[-300:])
    cas("P6", p6)

    def p7(b, d):
        ecrire(os.path.join(b.racine, "f"), "x")
        git(b.racine, "add", ".")
        git(b.racine, "commit", "-qm", "x")
        for n in ("w1", "w2"):
            git(b.racine, "worktree", "add", "-q", "-b", n, os.path.join(d, n))
        shutil.rmtree(os.path.join(d, "w2"))
        vus = {}
        for seuil, attendu in ((1, "SATURÉ"), (2, "JUSTE")):
            c = b.lancer(worktrees_nombre_sature=seuil)[2].get("Copies de travail (worktree)", ["", "", ""])
            vus[f"seuil {seuil}"] = (c[0], c[2], ("1 hors dépôt principal", attendu))
        faux = {k: x for k, x in vus.items() if (x[0], x[1]) != x[2]}
        return not faux, faux or vus
    cas("P7", p7)

    def p8(b, d):
        os.makedirs(os.path.join(b.tmp, "a", ".git"))
        ecrire(os.path.join(b.tmp, "b", ".git"), "gitdir: ailleurs\n")
        os.makedirs(os.path.join(b.tmp, "c"))
        ecrire(os.path.join(b.tmp, "f"), "x")
        t = b.lancer()[2]
        return t["Copies dans /tmp"][0] == "2 copies du dépôt sur 3 dossiers", t.get("Copies dans /tmp")
    cas("P8", p8)

    def heure(iso):
        return datetime.fromisoformat(iso).astimezone(PARIS).strftime("%d-%m %Hh%M")

    def p9(b, d):
        b.racine = depot_cowork(d)
        attendu = heure("2026-11-12T08:00:00+00:00")
        t1 = b.lancer(cowork_attente_saturee=4)[2]
        t2 = b.lancer(cowork_attente_saturee=3)[2]
        t3 = b.lancer(cowork_attente_saturee=4, cowork_silence_heures_sous_employe=10 ** 6)[2]
        c = t1.get("Cowork (relecture)", ["", "", "", ""])
        vus = {"Cowork": c[:3], "seuil 3": v(t2, "Cowork (relecture)"), "silence 10^6": v(t3, "Cowork (relecture)")}
        ok = (c[0] == "4 branches travail-*"
              and c[1] == f"dernière relecture {attendu} ; 3 en attente : travail-a, travail-c, travail-d"
              and c[2] == "SOUS-EMPLOYÉ" and "rapatriement du INCONNU" not in c[3]
              and vus["seuil 3"] == "SATURÉ" and vus["silence 10^6"] == "JUSTE")
        return ok, (vus, f"attendu dernière relecture {attendu}, 3 en attente dont travail-d")
    cas("P9", p9)

    def p9b(b, d):
        b.racine = depot_cowork(d, "clone_une_branche", "--single-branch", "--branch", "travail-a")
        t = b.lancer()[2]
        c, g = t.get("Cowork (relecture)", ["", "", "", ""]), t.get("Circuits GitHub", ["", "", "", ""])
        ok = c[2] == "INCONNU" and "une seule branche" in c[3] and g[1].startswith("traces INCONNU")
        return ok, ("Cowork", c, g[1])
    cas("P9b", p9b)

    def p9c(b, d):
        premier = depot_cowork(d, "premier_clone")
        b.racine = os.path.join(d, "clone_d_un_clone")
        git(d, "clone", "-q", premier, b.racine)
        git(b.racine, "fetch", "origin")  # un FETCH_HEAD, pour que seul le refus de l'origine locale puisse rougir
        t = b.lancer()[2]
        c, g = t.get("Cowork (relecture)", ["", "", "", ""]), t.get("Circuits GitHub", ["", "", "", ""])
        ok = c[2] == "INCONNU" and "copie sur cette machine" in c[3] and g[1].startswith("traces INCONNU")
        return ok, ("Cowork", c, g[1])
    cas("P9c", p9c)

    def p9d(b, d):
        b.racine = depot_cowork(d, "clone", rapatrier_par=("fetch", "origin", "travail-a"))
        t = b.lancer()[2]
        c, g = t.get("Cowork (relecture)", ["", "", "", ""]), t.get("Circuits GitHub", ["", "", "", ""])
        ok = c[2] == "INCONNU" and "rapatriement partiel" in c[3] and g[1].startswith("traces INCONNU")
        return ok, ("Cowork", c, g[1])
    cas("P9d", p9d)

    def p9e(b, d):
        b.racine = depot_cowork(d)
        for n in ("a", "b", "c", "d"):
            git(b.racine, "update-ref", "-d", f"refs/remotes/origin/travail-{n}")
        c = b.lancer()[2].get("Cowork (relecture)", ["", "", "", ""])
        attendu = f"dernière relecture {heure('2026-11-08T09:00:00+00:00')} ; 0 en attente"
        return c[0] == "0 branches travail-*" and c[1] == attendu, (c[:2], f"attendu {attendu}")
    cas("P9e", p9e)

    def p9f(b, d):
        b.racine = depot_cowork(d, "clone_superficiel", "--depth", "1", "--no-single-branch")
        c = b.lancer()[2].get("Cowork (relecture)", ["", "", "", ""])
        return c[2] != "INCONNU" and "clone superficiel" in c[3], ("superficiel non signalé", c)
    cas("P9f", p9f)

    def inconnu(t, raison):
        c, g = t.get("Cowork (relecture)", ["", "", "", ""]), t.get("Circuits GitHub", ["", "", "", ""])
        return c[2] == "INCONNU" and raison in c[3] and g[1].startswith("traces INCONNU"), ("Cowork", c, g[1])

    def p9g(b, d):
        b.racine = depot_cowork(d)
        miroir = os.path.join(d, "miroir.git")
        git(d, "clone", "-q", "--bare", os.path.join(d, "orig.git"), miroir)
        git(b.racine, "remote", "add", "miroir", "file://" + miroir)
        git(b.racine, "fetch", "miroir")
        return inconnu(b.lancer()[2], "venu d'ailleurs")
    cas("P9g", p9g)

    def p9h(b, d):
        b.racine = depot_cowork(d, rapatrier_par=None)
        return inconnu(b.lancer()[2], "aucun rapatriement")
    cas("P9h", p9h)

    def p9i(b, d):
        b.racine = depot_cowork(d)
        git(b.racine, "config", f"url.file://{os.path.join(d, 'orig.git')}.insteadOf", RESEAU)
        return inconnu(b.lancer()[2], "copie sur cette machine")
    cas("P9i", p9i)

    def p9j(b, d):
        b.racine = depot_cowork(d)
        git(os.path.join(d, "orig.git"), "branch", "-D", "travail-b")
        rapatrier(b.racine, "fetch", "origin")
        ok1, detail1 = inconnu(b.lancer()[2], "")
        conseil = "--prune" in detail1[1][3]
        rapatrier(b.racine, "fetch", "--prune", "origin")
        c2 = b.lancer()[2].get("Cowork (relecture)", ["", "", "", ""])
        ok = ok1 and conseil and c2[0] == "3 branches travail-*"
        return ok, ("conseil sans --prune" if not conseil else "", detail1, c2[:3])
    cas("P9j", p9j)

    def identifiants(b, d, adresse, ecrite_par_git):
        b.racine = depot_cowork(d, rapatrier_par=None)
        fetch_head = rapatrier_par_git(b.racine, adresse)
        c = b.lancer()[2].get("Cowork (relecture)", ["", "", "", ""])
        ok = (f" of {ecrite_par_git}\n" in fetch_head and "utilisateur" not in fetch_head and c[2] != "INCONNU"
              and c[0] == "4 branches travail-*")
        return ok, ("Cowork", c, "FETCH_HEAD : " + fetch_head.splitlines()[0].split("\t")[-1])

    def p9k(b, d):
        return identifiants(b, d, RESEAU_IDENTIFIE, "faux://depot-partage.invalid/depot")
    cas("P9k", p9k)

    def p9l(b, d):
        return identifiants(b, d, RESEAU_SCP, "depot-partage.invalid:depot")
    cas("P9l", p9l)

    def p10(b, d):
        vus = {}
        b.forfait = os.path.join(d, "faux_forfait.py")
        for nom, sortie, code, attendu, ecart in (
                ("code 4", "seuil 95 %\nVERDICT : ARRÊTER LES NOUVEAUX AGENTS", 4, "SATURÉ", 10),
                ("code 3", "seuil 95 %\nVERDICT : ALERTER", 3, "JUSTE", 10),
                ("proj 50,0", "seuil 95 %\nPROJECTION À LA REMISE : 50.0 %\nVERDICT : CONTINUER", 0, "SOUS-EMPLOYÉ", 10),
                ("proj 84,9", "seuil 95 %\nPROJECTION À LA REMISE : 84.9 %\nVERDICT : CONTINUER", 0, "SOUS-EMPLOYÉ", 10),
                ("proj 85,0", "seuil 95 %\nPROJECTION À LA REMISE : 85.0 %\nVERDICT : CONTINUER", 0, "JUSTE", 10),
                ("proj 105,0", "seuil 95 %\nPROJECTION À LA REMISE : 105.0 %\nVERDICT : CONTINUER", 0, "JUSTE", 10),
                ("proj 105,1", "seuil 95 %\nPROJECTION À LA REMISE : 105.1 %\nVERDICT : CONTINUER", 0, "SATURÉ", 10),
                ("écart 20, proj 84,9", "seuil 95 %\nPROJECTION À LA REMISE : 84.9 %\nVERDICT : CONTINUER", 0, "JUSTE", 20),
                ("proj inconnue", "seuil 95 %\nPROJECTION À LA REMISE : INCONNUE — x\nVERDICT : CONTINUER", 0, "INCONNU", 10),
                ("code 5", "seuil 95 %\nVERDICT : INCONNU", 5, "INCONNU", 10)):
            ecrire(b.forfait, f"import sys\nprint({sortie!r})\nsys.exit({code})\n")
            vus[nom] = (v(b.lancer(forfait_ecart_points=ecart)[2], "Forfait"), attendu)
        ecrire(b.forfait, "import time\ntime.sleep(30)\n")
        debut = time.monotonic()
        code, s, t = b.lancer(borne=20, delai_de_mesure_secondes=2)
        duree = time.monotonic() - debut
        vus["dort 30 s, délai 2 s"] = (v(t, "Forfait") if code is not None else "BORNE DÉPASSÉE", "INCONNU")
        faux = {k: x for k, x in vus.items() if x[0] != x[1]}
        return not faux and duree < 20, faux or f"11 cas tenus, relevé du programme endormi en {duree:.1f} s"
    cas("P10", p10)

    def p10b(b, d):
        # C-2 de Cowork (25-11-2026) : la jauge se lit sur la sortie du VRAI programme du forfait (copié depuis
        # <racine>, journal fabriqué relatif à l'horloge), et non sur un faux qui recopie le libellé attendu
        f = os.path.join(d, "forf", "programmes", "TENIR_LE_FORFAIT.py")
        os.makedirs(os.path.dirname(f))
        os.makedirs(os.path.join(d, "forf", "donnees"))
        shutil.copy(os.path.join(racine, "programmes", "TENIR_LE_FORFAIT.py"), f)
        ecrire(os.path.join(d, "forf", "donnees", "REGLAGES_DU_FORFAIT.csv"),
               "reglage,valeur,etat,qui_decide,raison\nseuil_d_arret,95,x,x,x\nmarge_d_alerte,10,x,x,x\n"
               "age_max_de_la_capture,2,x,x,x\nduree_min_d_une_paire,0,x,x,x\n")
        h = datetime.now(PARIS).replace(second=0, microsecond=0)
        a = lambda delta: (h + delta).strftime("%Y-%m-%dT%H:%M")
        for args in (["--remise", a(timedelta(days=3)), "--a", a(timedelta(hours=-3))],
                     ["--capture", "10", "--a", a(timedelta(hours=-2))],
                     ["--agent", "x", "1000000", "--a", a(timedelta(hours=-1, minutes=-30))],
                     ["--capture", "20", "--a", a(timedelta(hours=-1))]):
            r = subprocess.run([sys.executable, "-I", f] + args, capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                return False, "ajout refusé : " + r.stdout + r.stderr
        b.forfait = f
        c = b.lancer()[2].get("Forfait", ["", "", "", ""])
        # 20 % + rythme de pointe 10 points/h × 1 h = 30,0 % (30,x si une minute passe pendant l'épreuve)
        return c[1].startswith("jauge 3") and "INCONNU" not in c[1].split(";")[0], ("Forfait", c)
    cas("P10b", p10b)

    def p11(b, d):
        for f in ("a.yml", "b.yaml", "c.txt"):
            ecrire(os.path.join(b.racine, ".github", "workflows", f), "x")
        t1 = b.lancer()[2]
        b.pub = os.path.join(d, "pub")
        for f in ("series_longues.yml", "x.yml"):
            ecrire(os.path.join(b.pub, ".github", "workflows", f), "x")
        t2 = b.lancer()[2]
        c1, c2 = t1["Circuits GitHub"], t2["Circuits GitHub"]
        ok = (c1[0] == "2 privés, publics INCONNU (clone absent)" and c2[0] == "2 privés, 2 publics dont series_longues.yml"
              and c1[2] == c2[2] == "INCONNU" and "non visible" in c2[3])
        return ok, (c1, c2)
    cas("P11", p11)

    def p12(b, d):
        copie = os.path.join(d, "copie_du_vrai_depot")
        subprocess.run(["git", "clone", "-q", "--no-checkout", "--depth", "1", "file://" + racine, copie], check=True,
                       capture_output=True)
        if os.path.exists(os.path.join(copie, ".git", "objects", "info", "alternates")):
            return False, "le clone partage les objets du vrai dépôt (alternates) : il ne le protège pas"
        a_lire = ["donnees/REGLAGES_DU_PERIMETRE.csv", "tests/LANCEMENT_DES_EPREUVES.json", ".github"]
        subprocess.run(["git", "-C", copie, "checkout", "HEAD", "--"] + a_lire, check=True, capture_output=True)

        def etat():  # `git status` d'abord : il rafraîchit l'index, dont l'empreinte est prise ensuite
            st = subprocess.run(["git", "-C", copie, "status", "--porcelain"], capture_output=True, text=True).stdout
            refs = subprocess.run(["git", "-C", copie, "for-each-ref", "--format=%(refname) %(objectname)"],
                                  capture_output=True, text=True).stdout
            tete = subprocess.run(["git", "-C", copie, "rev-parse", "HEAD"], capture_output=True, text=True).stdout
            return st, refs + tete, empreinte_git(copie)
        # Index « racy » : juste après le checkout, chaque `git status` réécrit l'index (date seule) tant que sa date
        # n'a pas dépassé d'une seconde celle des fichiers (mesuré le 16-11-2026). Un status, une attente, puis l'état.
        subprocess.run(["git", "-C", copie, "status", "--porcelain"], capture_output=True)
        time.sleep(1.5)
        avant = etat()
        p = subprocess.run([sys.executable, "-B", prog, "--racine", copie], capture_output=True, text=True, timeout=900)
        apres = etat()
        t = tableau(p.stdout)
        n = subprocess.run(["nproc"], capture_output=True, text=True).stdout.strip()
        compte = [l for l in p.stdout.splitlines() if l.startswith("VERDICTS : ")]
        somme = sum(int(x.rsplit(" ", 1)[1]) for x in compte[0][len("VERDICTS : "):].split(" · ")[:4]) if compte else -1
        changes = []
        if avant[0] != apres[0]:
            changes.append("git status changé")
        if avant[1] != apres[1]:
            changes.append("références changées")
        fichiers = sorted(set(avant[2]) ^ set(apres[2]) | {c for c in avant[2] if c in apres[2] and avant[2][c] != apres[2][c]})
        if fichiers:
            changes.append(f"fichiers de .git changés : {[os.path.relpath(c, copie) for c in fichiers][:3]}")
        ok = (p.returncode == 0 and len(t) == 9 and all(x[2] in VERDICTS for x in t.values())
              and t.get("Cœurs", [None])[0] == f"{n} cœurs" and v(t, "Circuits GitHub") == "INCONNU" and somme == 9
              and not changes)
        return ok, {"code": p.returncode, "lignes": len(t), "somme": somme, "lecture seule": changes or "rien n'a changé",
                    "cœurs": t.get("Cœurs", [None])[0]}
    cas("P12", p12)

    def p13(b, d):
        vus = []
        ecrire(b.reglages, "reglage,valeur,etat,qui_decide,raison\ncoeurs_fenetre_minutes,5,x,x,x\n")
        vus.append(("absent",) + tuple(b.lancer(garder=True)[:2]))
        ecrire_reglages(b.reglages)
        with open(b.reglages, "a", encoding="utf-8") as f:
            f.write("disque_libre_sature_go,3,x,x,x\n")
        vus.append(("double",) + tuple(b.lancer(garder=True)[:2]))
        os.remove(b.reglages)
        vus.append(("manquant",) + tuple(b.lancer(garder=True)[:2]))
        for nom, changes in (("nan fenêtre", {"coeurs_fenetre_minutes": "nan"}),
                             ("nan cœurs", {"coeurs_charge_par_coeur_saturee": "nan"}),
                             ("inf", {"coeurs_charge_par_coeur_saturee": "inf"}),
                             ("négatif", {"coeurs_charge_par_coeur_saturee": -1}),
                             ("délai nul", {"delai_de_mesure_secondes": 0}),
                             ("délai négatif", {"delai_de_mesure_secondes": -5}),
                             ("délai 3601", {"delai_de_mesure_secondes": 3601}),
                             ("délai 1e300", {"delai_de_mesure_secondes": "1e300"}),
                             ("souligné 1_0", {"worktrees_nombre_sature": "1_0"}),
                             ("fenêtre 7", {"coeurs_fenetre_minutes": 7}),
                             ("copies 2,5", {"worktrees_nombre_sature": 2.5}),
                             ("mémoire croisée", {"memoire_part_disponible_saturee": 0.95}),
                             ("cœurs croisés", {"coeurs_charge_par_coeur_sous_employee": 2.0})):
            vus.append((nom,) + tuple(b.lancer(**changes)[:2]))
        faux = [(n, c, s.strip()[:90]) for n, c, s in vus
                if not (c == 2 and "ERREUR RÉGLAGE" in s and "| Ressource" not in s)]
        return not faux, faux or f"{len(vus)} réglages refusés en code 2"
    cas("P13", p13)

    def p14(b, d):
        ecrire(os.path.join(b.bin, "nproc"), "#!/bin/sh\nexec sleep 5\n", 0o755)
        code, s, t = b.lancer(delai_de_mesure_secondes=1)
        coeurs = t.get("Cœurs", ["", "", "", ""])[3]
        lent = os.path.join(d, "bin_git_lent")
        ecrire(os.path.join(lent, "git"), "#!/bin/sh\nexec sleep 5\n", 0o755)
        b.path = lent + os.pathsep + b.path
        code2, s2, t2 = b.lancer(delai_de_mesure_secondes=1)
        ok = ("sans réponse en 1 s" in coeurs and "introuvable" not in coeurs
              and code2 == 2 and "ERREUR RACINE" in s2 and "sans réponse" in s2)
        return ok, (coeurs, code2, s2.strip()[:120])
    cas("P14", p14)

    def p15(b, d):
        b.charge("0.00 1.9998 0.00")
        c = b.lancer()[2].get("Cœurs", ["", "", "", ""])
        return c[2] == "JUSTE" and "= 1,00 ;" not in c[3], ("JUSTE lu face à 1,00", c[2:])
    cas("P15", p15)
    return res


def afficher(res):
    for nom, ok, detail in res:
        print(f"  {'ok   ' if ok else 'ROUGE'} {nom} — {detail}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    racine = os.path.abspath(sys.argv[1])
    reglages_de_base(racine)
    prog = os.path.join(racine, "programmes", PROG)
    res = epreuves(prog, racine)
    afficher(res)
    rouges = [n for n, ok, _ in res if not ok]
    print(f"FIN DES CAS : {len(res)} · rouges : {len(rouges)}")
    if "--saboter" not in sys.argv:
        print("VERDICT : TOUT PASSE" if not rouges else "VERDICT : ROUGE")
        return 0 if not rouges else 1
    if rouges:
        print("VERDICT : ROUGE (épreuves rouges avant sabotage)")
        return 1
    source = open(prog, encoding="utf-8").read()
    mordent = 0
    for nom, (cible, vieux, neuf, marque) in SABOTAGES.items():
        if source.count(vieux) != 1:
            print(f"{nom} : TEXTE INTROUVABLE OU AMBIGU ({source.count(vieux)} fois)")
            continue
        with tempfile.TemporaryDirectory(prefix="perim_sabotage_") as d:
            copie = os.path.join(d, "programmes", PROG)
            ecrire(copie, source.replace(vieux, neuf))
            r = epreuves(copie, racine, seulement=cible)
        rouge = [x for x in r if not x[1]]
        if rouge and marque in str(rouge[0][2]):
            mordent += 1
            print(f"{nom} mord : {cible} rouge — {str(rouge[0][2])[:150]}")
        elif rouge:
            print(f"{nom} MORD POUR UNE AUTRE RAISON (marque « {marque} » absente) : {cible} — {str(rouge[0][2])[:200]}")
        else:
            print(f"{nom} NE MORD PAS : {cible} reste vert — {r[0][2] if r else 'aucun cas'}")
    print(f"sabotages qui mordent : {mordent} sur {len(SABOTAGES)}")
    print("VERDICT : TOUT PASSE" if mordent == len(SABOTAGES) else "VERDICT : ROUGE")
    return 0 if mordent == len(SABOTAGES) else 1


if __name__ == "__main__":
    sys.exit(main())
