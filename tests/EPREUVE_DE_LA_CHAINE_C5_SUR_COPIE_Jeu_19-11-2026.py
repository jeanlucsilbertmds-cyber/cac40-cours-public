#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVE_DE_LA_CHAINE_C5_SUR_COPIE_Jeu_19-11-2026.py — Jeu 19-11-2026 (Paris). Simulation uniquement : aucun ordre
réel, jamais.

LE SENS EN TÊTE. Décisions de Jean-Luc : A-916 (19-11-2026 à 08h04, « 1 ») — C5 sert à ÉPROUVER TOUTE LA CHAÎNE, et son
verdict est marqué « déjà vu, ne prouve rien » (C5 a déjà été regardée sur ces années) ; A-917 (19-11-2026 à 08h33,
« 1 ») — cette chaîne s'éprouve SUR UNE COPIE du dépôt (juge en essai, fiche, circuit du soir), sans rien écrire au vrai
registre. Règles gardées intactes : A-767 ① (rien ne s'écrit dans une fiche RÉELLE sans regard) et A-861 (une fiche
d'essai n'entre jamais au vrai registre). Ce programme rejoue la chaîne de bout en bout, dans une copie jetable,
et dit maillon par maillon ce qui a tenu, avec ses chiffres.

① RÔLE — Dans UNE copie jetable du dépôt, hors du dépôt : ① préparer la fiche d'essai C5 par
  programmes/PREPARER_LA_MOULINETTE_D_ESSAI.py, tel quel · ② lancer le juge en essai sans regard sur 2000-2026 · ③ écrire
  dans la fiche de la COPIE le verdict d'essai, porteur de MARQUE_D_ESSAI · ④ passer cette fiche à l'état QA (suivie par
  le soir) et rejouer le circuit du soir — détecteur, teneur des positions, radar — séance par séance, de
  PREMIERE_SEANCE à DERNIERE_SEANCE · ⑤ affirmer par propriétés · ⑥ rendre un RAPPORT, un maillon par ligne.
  Avec « --saboter » : rejouer trois fois la chaîne, chaque fois avec un défaut posé exprès, et exiger que le maillon
  visé rougisse.
② CONTEXTE D'APPEL — À la main : `python3 -I -B tests/EPREUVE_DE_LA_CHAINE_C5_SUR_COPIE_Jeu_19-11-2026.py <racine>
  [--saboter]` ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis « --saboter ».
③ ENTRÉE — `<racine>` : un clone du dépôt (ou un worktree), jamais modifié.
④ CONDITIONS D'ENTRÉE — La racine est un dépôt git (pour compter les branches regards/*) et porte programmes/,
  donnees/ (registre, cours maître avec les séances de PREMIERE_SEANCE à DERNIERE_SEANCE, référentiel) et temoins/
  (le fichier des 20 ans de la moulinette d'essai) ; environ 400 Mo libres sous /dev/shm ou le dossier temporaire.
⑤ SORTIE — UNE valeur, le code de sortie : 0 si chaque maillon tient (et, avec --saboter, si chaque sabotage fait
  rougir son maillon) ; 1 sinon ; 2 si la copie n'a pas pu être faite ou si la racine n'est pas un dépôt (R-734 : un
  contrôle qui n'a pas pu tourner ne rend pas 0). [rend: 1]
⑥ TRAITEMENT — `jouer_la_chaine` une fois (Z0), puis une fois par sabotage ; chaque passage fait SA copie et l'efface
  avant le suivant : une seule copie à la fois sur le disque.
⑦ UNITÉ — Euros ; seuils de fiche en pourcents au registre, lus en fractions par `pourcent` du juge ; dates AAAA-MM-JJ.
⑧ POURQUOI — Boucle R-731 : épreuve sur les vraies données, avec sabotages ; R-732 : les cas viennent de vraies lignes
  (séances réelles du cours maître, du 2026-10-20 au 2026-11-04 : signaux réels EIFFAGE le 20-10 et BOUYGUES le 22-10,
  ENGIE le 20-10 hors de l'univers de la fiche ; sorties TP le 02-11 et le 04-11).
⑨ CE QUI CLOCHE — ① L'ÉCRITURE DU VERDICT EST PROPRE À CE PROGRAMME (`ecrire_dans_la_fiche`), une écriture minimale
  par ajout d'une ligne (n°83 : la dernière ligne d'un identifiant fait foi). L'écrivain des blocs
  (ECRIRE_LES_BLOCS_DE_LA_FICHE.py, branches travail-fiche et travail-e4) n'est PAS importé : il exige le contrat de
  ces branches (BLOCS_DE_LA_FICHE, CODES_DE_REFUS…, absents du contrat de main + travail-e8), une période déclarée
  datée (`declaration_de_la_fiche`), les indicateurs 70 %/30 % et des mots de verdict admis par partie, dont aucun ne
  porte la marque d'un essai. Le jour où l'écrivain des blocs sera sur main, ce verdict devra passer par lui (R-708).
  ② Les anciennes cases de résultat de la ligne recopiée de C5E10-QA-V1 (`n_trades`, `wr`, `net_2ans`, `note`) restent
  telles quelles dans la copie ; seule la case `statut` porte le verdict. ③ Le versement (TENIR_L_HISTORIQUE.py), la
  collecte, le cockpit, la mesure et le PILOTE ne sont pas rejoués : le cours maître de la copie est COUPÉ à chaque
  séance. ④ Les positions et le journal de la copie sont remis à leur seul en-tête avant le premier soir, pour que
  chaque position et chaque trade compté vienne de ce rejeu. ⑤ Les seuils de la fiche d'essai sont ceux de C5 : la
  propriété « seuils lus dans la fiche » ne distingue pas ici la fiche des constantes de C5 (l'épreuve E8, K6, le fait).
  ⑥ L'empreinte du dépôt ne lit ni .git, ni prompts_taches/, ni PILOTE_SOCLE* (jamais lus) : une écriture là n'est pas vue.
⑩ EFFET — Écrit une copie sous /dev/shm (ou le dossier temporaire), l'efface ; le sabotage S3 crée puis efface un
  fichier dans la racine (SABOTAGE_S3, nom donné plus bas).
⑪ TERMINAISON — Rend la main ; chaque programme lancé est borné (600 s le juge, 300 s les autres). [sort: oui — code]
"""
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo

sys.dont_write_bytecode = True

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
SABOTER = "--saboter" in sys.argv
# LA MARQUE DU VERDICT D'ESSAI — définie ICI, une fois (A-916 : « déjà vu, ne prouve rien »). Tout autre endroit qui la
# cherche la lit par ce nom.
MARQUE_D_ESSAI = "ESSAI — DÉJÀ VU, NE PROUVE RIEN"
# LES SÉANCES RÉELLES REJOUÉES (R-732) : du signal EIFFAGE du 2026-10-20 à la sortie TP de BOUYGUES du 2026-11-04.
PREMIERE_SEANCE, DERNIERE_SEANCE = "2026-10-20", "2026-11-04"
# LE TÉMOIN DU MATIN : mesuré le 19-11-2026 par le Chat sur une copie sans .git, juge en essai sans regard, C5 2000-2026
# (343 opérations · 48,4 % · +102 574,45 €). Un écart, à données figées identiques, est une régression.
TEMOIN_DU_MATIN = ("343", "48.4", "+102,574.45")
# les fichiers du teneur (écrits par TENIR_LES_POSITIONS.py, `tenir_pour_de_vrai`, l. 3172-3173 ; le contrat ne les nomme
# que par leur nom de fichier, CONTRATS_PAR_FICHIER)
POSITIONS = "donnees/claude_positions_ouvertes.csv"
JOURNAL = "donnees/claude_journal_trades.csv"
COURS_MAITRE = "donnees/cours_maitre.csv"
SIGNAUX = "donnees/signaux_du_jour.json"
# ce qui n'est jamais copié ni lu : au premier niveau .git, etudes/, archives/, prompts_taches/ ; partout PILOTE_SOCLE*
NON_COPIES_EN_TETE = (".git", "etudes", "archives", "prompts_taches")
SABOTAGE_S3 = os.path.join("donnees", "_SABOTAGE_S3_ECRITURE_DANS_LE_VRAI_DEPOT.tmp")
PARIS = ZoneInfo("Europe/Paris")


def ignorer(dossier, noms):
    """Rend les noms à ne pas copier. ① RÔLE — Le filtre de la copie. ② CONTEXTE D'APPEL — `copier`, par copytree.
    ③ ENTRÉE — `dossier`, `noms`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur, la liste. [rend: 1] ⑥ TRAITEMENT —
    NON_COPIES_EN_TETE au premier niveau, PILOTE_SOCLE* partout. ⑦ UNITÉ — —. ⑧ POURQUOI — consigne : ne jamais lire
    prompts_taches/ ni PILOTE_SOCLE* ; .git exclu pour que la copie soit refusée par aucun programme d'essai.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    tete = os.path.abspath(dossier) == RACINE
    return [n for n in noms if (tete and n in NON_COPIES_EN_TETE) or n.startswith("PILOTE_SOCLE")]


def empreinte_du_depot(racine):
    """Rend l'empreinte de l'arbre de la racine et le nombre de fichiers. ① RÔLE — Prouver qu'aucun octet du vrai dépôt
    n'a changé. ② CONTEXTE D'APPEL — `jouer_la_chaine`, avant et après. ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs : l'empreinte (16 hex), le compte de fichiers. [rend: 2] ⑥ TRAITEMENT — parcours trié, sans
    ce que `ignorer` écarte ; pour chaque fichier, son chemin relatif et le sha256 de ses octets (un lien : sa cible).
    ⑦ UNITÉ — —. ⑧ POURQUOI — une PROPRIÉTÉ (« aucun octet »), pas une liste de fichiers : renommer un fichier ne change
    pas l'avis du contrôle. ⑨ CE QUI CLOCHE — ⑨ ⑥ du fichier. ⑩ EFFET — Lit l'arbre (≈ 650 Mo). ⑪ TERMINAISON — rend
    la main. [sort: non]"""
    h, n = hashlib.sha256(), 0
    for d, dossiers, fichiers in os.walk(racine):
        ecartes = set(ignorer(d, dossiers + fichiers))
        dossiers[:] = sorted(x for x in dossiers if x not in ecartes)
        for f in sorted(x for x in fichiers if x not in ecartes):
            p = os.path.join(d, f)
            h.update(os.path.relpath(p, racine).encode("utf-8") + b"\0")
            if os.path.islink(p):
                h.update(b"->" + os.readlink(p).encode("utf-8"))
            else:
                with open(p, "rb") as fh:
                    for bloc in iter(lambda: fh.read(1 << 20), b""):
                        h.update(bloc)
            n += 1
    return h.hexdigest()[:16], n


def sha_court(chemin):
    """Rend les 16 premiers hex du sha256 d'un fichier, ou « absent ». ① RÔLE — Afficher l'empreinte d'un fichier nommé.
    ② CONTEXTE D'APPEL — `jouer_la_chaine`. ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur.
    [rend: 1] ⑥ TRAITEMENT — lire, hacher. ⑦ UNITÉ — —. ⑧ POURQUOI — le rapport nomme les fichiers que la consigne
    nomme. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Lit le fichier. ⑪ TERMINAISON — rend la main. [sort: non]"""
    if not os.path.isfile(chemin):
        return "absent"
    with open(chemin, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def regards_du_depot(racine):
    """Rend la liste des références git dont le nom contient « regards/ », ou None si git n'a pas répondu.
    ① RÔLE — Compter les inscriptions de regard (BRANCHE_DES_REGARDS du contrat). ② CONTEXTE D'APPEL — `jouer_la_chaine`.
    ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — un dépôt git. ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT —
    `git for-each-ref`, filtre. ⑦ UNITÉ — —. ⑧ POURQUOI — « JAMAIS de vrai regard » : un regard s'inscrit sur cette
    branche (CONTRATS.BRANCHE_DES_REGARDS). ⑨ CE QUI CLOCHE — seules les références locales et suivies sont vues, sans
    fetch. ⑩ EFFET — Aucun. ⑪ TERMINAISON — borné à 60 s. [sort: non]"""
    p = subprocess.run(["git", "-C", racine, "for-each-ref", "--format=%(refname)"], capture_output=True, text=True,
                       timeout=60)
    if p.returncode != 0:
        return None
    return [r for r in p.stdout.split() if "regards/" in r]


def registres_d_essais(racine):
    """Rend les chemins, sous `racine`, dont un élément commence par « registre_essais ». ① RÔLE — Voir qu'aucun
    registre des essais n'a été écrit. ② CONTEXTE D'APPEL — `jouer_la_chaine`. ③ ENTRÉE — `racine`. ④ CONDITIONS
    D'ENTRÉE — —. ⑤ SORTIE — UNE valeur, la liste. [rend: 1] ⑥ TRAITEMENT — parcours, sans ce que `ignorer` écarte.
    ⑦ UNITÉ — —. ⑧ POURQUOI — le registre des essais vit dans `registre_essais/<16 hex>.json` (contrat,
    NATURES_DES_ENTREES_D_ESSAI). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — rend la main. [sort: non]"""
    vus = []
    for d, dossiers, fichiers in os.walk(racine):
        ecartes = set(ignorer(d, dossiers + fichiers))
        dossiers[:] = [x for x in dossiers if x not in ecartes]
        vus += [os.path.join(d, x) for x in dossiers + fichiers if x.startswith("registre_essais")]
    return vus


def lancer(copie, sortie_du_pas, *arguments, delai=300):
    """Lance un programme de la copie ; rend (code, affichage, sortie du pas). ① RÔLE — Emprunter le chemin réel, en
    ligne de commande. ② CONTEXTE D'APPEL — `jouer_la_chaine`. ③ ENTRÉE — `copie`, `sortie_du_pas` (fichier hors de la
    copie), `arguments` (programme relatif puis ses arguments), `delai` en secondes. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — TROIS valeurs. [rend: 3] ⑥ TRAITEMENT — vider la sortie du pas, lancer `python3 -B`, relire.
    ⑦ UNITÉ — secondes. ⑧ POURQUOI — le code et la sortie du pas font partie de ce qui est éprouvé. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — le programme écrit dans la copie. ⑪ TERMINAISON — lève TimeoutExpired au-delà du délai. [sort: non]"""
    open(sortie_du_pas, "w").close()
    p = subprocess.run([sys.executable, "-B"] + list(arguments), cwd=copie, capture_output=True, text=True,
                       timeout=delai, env=dict(os.environ, GITHUB_OUTPUT=sortie_du_pas))
    with open(sortie_du_pas, encoding="utf-8") as fh:
        pas = dict(l.split("=", 1) for l in fh.read().splitlines() if "=" in l)
    return p.returncode, p.stdout + p.stderr, pas


def ecrire_dans_la_fiche(copie, chemin_rel, ident, cases):
    """Ajoute au registre de la COPIE une ligne de `ident` : sa dernière ligne, `cases` changées. ① RÔLE — L'écriture
    minimale du verdict d'essai et de l'état de vie (⑨ ① du fichier). ② CONTEXTE D'APPEL — `jouer_la_chaine`, deux fois.
    ③ ENTRÉE — `copie`, `chemin_rel` (le registre, nommé par le contrat), `ident`, `cases` {colonne: texte}.
    ④ CONDITIONS D'ENTRÉE — la copie n'a pas de .git ; le registre finit par une fin de ligne ; `ident` y est.
    ⑤ SORTIE — Aucune. [rend: rien] ⑥ TRAITEMENT — refuser un lieu porteur de .git ; lire les octets ; recopier la
    dernière ligne de `ident` (n°83) ; changer les cases ; ajouter la ligne avec la fin de ligne du fichier ; écrire à
    côté puis renommer. ⑦ UNITÉ — —. ⑧ POURQUOI — n°83 (« la dernière ligne ajoutée fait foi ») et R-727 (on ajoute, on
    n'écrase pas) ; A-861 : jamais dans un dépôt. ⑨ CE QUI CLOCHE — ⑨ ① et ② du fichier. ⑩ EFFET — Remplace le registre
    de la copie. ⑪ TERMINAISON — lève ValueError si le lieu, la fin de ligne, l'identifiant ou une colonne manque.
    [sort: non]"""
    if os.path.lexists(os.path.join(copie, ".git")):
        raise ValueError("%s porte .git : jamais d'écriture de fiche dans un dépôt (A-861)" % copie)
    chemin = os.path.join(copie, chemin_rel)
    with open(chemin, "rb") as fh:
        octets = fh.read()
    if not octets.endswith(b"\n"):
        raise ValueError("le registre ne finit pas par une fin de ligne")
    lignes = list(csv.reader(io.StringIO(octets.decode("utf-8-sig"), newline="")))
    entete, i_id = lignes[0], lignes[0].index("id")
    rangs = [i for i, l in enumerate(lignes) if len(l) > i_id and l[i_id] == ident]
    if not rangs:
        raise ValueError("%s absent du registre de la copie" % ident)
    neuve = list(lignes[rangs[-1]])
    for colonne, valeur in cases.items():
        neuve[entete.index(colonne)] = valeur
    texte = io.StringIO()
    csv.writer(texte, lineterminator="\r\n" if octets.endswith(b"\r\n") else "\n").writerow(neuve)
    with open(chemin + ".en_cours", "wb") as fh:
        fh.write(octets + texte.getvalue().encode("utf-8"))
    os.replace(chemin + ".en_cours", chemin)


def lire_csv(chemin):
    """Rend les lignes d'un CSV en dictionnaires. ① RÔLE — Lire positions et journal. ② CONTEXTE D'APPEL —
    `jouer_la_chaine`. ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT —
    csv.DictReader. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Lit. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    with open(chemin, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def jouer_la_chaine(sabotage=None):
    """Fait une copie, y joue la chaîne, juge les propriétés, efface la copie ; rend la liste des maillons.
    ① RÔLE — Un passage complet de la chaîne. ② CONTEXTE D'APPEL — `main`, une fois sans sabotage, puis une fois par
    sabotage. ③ ENTRÉE — `sabotage` : None, "S1", "S2" ou "S3" (voir SABOTAGES). ④ CONDITIONS D'ENTRÉE — celles du
    fichier. ⑤ SORTIE — UNE valeur : la liste (code du maillon, vrai/faux, chiffres et preuve). [rend: 1]
    ⑥ TRAITEMENT — M0 copie · M1 préparation · M2 juge en essai · M3 verdict marqué · M4 fiche suivie · M5 le soir lit
    la fiche (détecteur, teneur, radar, séance par séance) · M6 univers · M7 positions et trades de la fiche d'essai, à
    ses seuils · M8 vrai dépôt intact · M9 aucun regard. ⑦ UNITÉ — euros, dates. ⑧ POURQUOI — voir ⑧ du fichier.
    ⑨ CE QUI CLOCHE — voir ⑨ du fichier. ⑩ EFFET — copie écrite puis effacée ; S3 crée puis efface un fichier dans la
    racine. ⑪ TERMINAISON — celle des programmes lancés. [sort: non]"""
    res = []

    def dire(code, ok, preuve):
        res.append((code, bool(ok), str(preuve)))

    regards_avant = regards_du_depot(RACINE)
    empreinte_avant = empreinte_du_depot(RACINE)
    nommes_avant = {f: sha_court(os.path.join(RACINE, f)) for f in ("donnees/cac40_strategies.csv", JOURNAL, POSITIONS)}
    essais_avant = registres_d_essais(RACINE)
    lieu = tempfile.mkdtemp(prefix="chaine_c5_", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    copie = os.path.join(lieu, "depot")
    pas = os.path.join(lieu, "sortie_du_pas")
    try:
        # M0 — LA COPIE : hors du dépôt, sans .git, sans lien
        shutil.copytree(RACINE, copie, ignore=ignorer, symlinks=False)
        dedans = os.path.commonpath([os.path.realpath(copie), RACINE]) == RACINE
        liens = sum(1 for d, _ds, fs in os.walk(copie) for f in fs if os.path.islink(os.path.join(d, f)))
        dire("M0", not dedans and liens == 0 and not os.path.lexists(os.path.join(copie, ".git")),
             "copie %s · hors du dépôt : %s · liens : %d · .git : %s" % (copie, not dedans, liens,
                                                                        os.path.lexists(os.path.join(copie, ".git"))))
        if sabotage == "S3":
            with open(os.path.join(RACINE, SABOTAGE_S3), "w", encoding="utf-8") as fh:
                fh.write("sabotage S3 : une écriture dans le vrai dépôt\n")

        # les modules de la COPIE : contrat, préparation, juge (aucune valeur recopiée, R-708)
        sys.path.insert(0, os.path.join(copie, "programmes"))
        for m in ("CONTRATS_DES_FICHIERS", "PREPARER_LA_MOULINETTE_D_ESSAI", "JUGE_DES_STRATEGIES"):
            sys.modules.pop(m, None)
        import CONTRATS_DES_FICHIERS as C
        import PREPARER_LA_MOULINETTE_D_ESSAI as P
        import JUGE_DES_STRATEGIES as J
        ident, reg = P.IDENTIFIANT, C.REGISTRE_DES_STRATEGIES

        # M1 — LA PRÉPARATION, telle quelle
        c1, o1, _ = lancer(copie, pas, "programmes/PREPARER_LA_MOULINETTE_D_ESSAI.py", copie)
        fiche = C.fiches_du_registre(os.path.join(copie, reg)).get(ident) or {}
        dire("M1", c1 == 0 and fiche.get("etat_vie") == P.ETAT_DE_LA_FICHE_D_ESSAI,
             "préparation code %d · fiche %s · etat_vie %r · période %s" % (c1, ident, fiche.get("etat_vie"),
                                                                            fiche.get("periode")))

        # M2 — LE JUGE EN ESSAI SANS REGARD, 2000-2026
        c2, o2, _ = lancer(copie, pas, "programmes/JUGE_DES_STRATEGIES.py", copie, ident,
                           "--cours=" + P.COURS_DES_VINGT_ANS, C.OPTION_D_ESSAI_SANS_REGARD, delai=600)
        bloc = o2.split("=== %s" % ident, 1)[1] if ("=== %s" % ident) in o2 else ""
        m = re.search(r"(\d+) operations \. ([\d.]+) % de reussite \. ([+-][\d,]+\.\d\d) EUR", bloc)
        chiffres = m.groups() if m else None
        lignes2 = [l for l in o2.splitlines() if l.strip()]
        toutes_marquees = bool(lignes2) and all(l.startswith(C.STATUT_D_ESSAI) for l in lignes2)
        dire("M2", c2 == 0 and chiffres == TEMOIN_DU_MATIN and "ESSAI DÉCLARÉ" in o2 and toutes_marquees,
             "juge code %d · %s · témoin du matin %s · essai déclaré : %s · lignes marquées « %s » : %s"
             % (c2, "%s opérations · %s %% · %s EUR" % chiffres if chiffres else "chiffres introuvables",
                "égal" if chiffres == TEMOIN_DU_MATIN else "DIFFÉRENT", "ESSAI DÉCLARÉ" in o2, C.STATUT_D_ESSAI,
                toutes_marquees))

        # M3 — LE VERDICT D'ESSAI ÉCRIT DANS LA FICHE DE LA COPIE, marqué
        aujourd_hui = datetime.now(PARIS).strftime("%Y-%m-%d")
        verdict = "juge en essai sans regard, %s : %s" % (
            fiche.get("periode"), "%s opérations · %s %% · %s EUR" % chiffres if chiffres else "sans chiffres")
        texte = verdict if sabotage == "S1" else "%s · %s (A-916, A-917)" % (MARQUE_D_ESSAI, verdict)
        ecrire_dans_la_fiche(copie, reg, ident, {"statut": texte, "date_test": aujourd_hui})
        fiche = C.fiches_du_registre(os.path.join(copie, reg)).get(ident) or {}
        dire("M3", MARQUE_D_ESSAI in fiche.get("statut", "") and bool(chiffres) and verdict in fiche.get("statut", ""),
             "statut de la dernière ligne : %r" % fiche.get("statut"))

        # M4 — LA FICHE PASSE À L'ÉTAT SUIVI PAR LE SOIR (QA), dans la copie seulement
        if sabotage != "S2":
            ecrire_dans_la_fiche(copie, reg, ident, {"etat_vie": "QA"})
        fiche = C.fiches_du_registre(os.path.join(copie, reg)).get(ident) or {}
        dire("M4", C.suivie_par_le_soir(fiche), "etat_vie %r · suivie_par_le_soir : %s · marque gardée : %s"
             % (fiche.get("etat_vie"), C.suivie_par_le_soir(fiche), MARQUE_D_ESSAI in fiche.get("statut", "")))

        # M5 — LE CIRCUIT DU SOIR, séance par séance (cours maître coupé à chaque séance)
        with open(os.path.join(copie, COURS_MAITRE), encoding="utf-8") as fh:
            cours = fh.read().splitlines(True)
        seances = sorted({l.split(",")[1] for l in cours[1:] if PREMIERE_SEANCE <= l.split(",")[1] <= DERNIERE_SEANCE})
        for f in (POSITIONS, JOURNAL):          # ⑨ ④ du fichier : en-tête seul, lu dans le fichier lui-même
            with open(os.path.join(copie, f), encoding="utf-8") as fh:
                entete = fh.readline()
            with open(os.path.join(copie, f), "w", encoding="utf-8") as fh:
                fh.write(entete)
        mnemo = J.table_mnemoniques(J.trouver(copie, "REFERENTIEL_VALEURS"))
        univers = {mnemo.get(x.strip().upper(), x.strip().upper()) for x in fiche.get("univers", "").split(",") if x.strip()}
        tp_f, sl_f = J.pourcent(fiche.get("tp")), J.pourcent(fiche.get("sl"))
        horizon = J.lire_horizon(fiche.get("horizon"))
        soirs, positions_essai, hors_univers, radar_essai, ecarts_seuils = [], {}, [], 0, []
        for s in seances:
            with open(os.path.join(copie, COURS_MAITRE), "w", encoding="utf-8") as fh:
                fh.writelines([cours[0]] + [l for l in cours[1:] if l.split(",")[1] <= s])
            cd, od, _ = lancer(copie, pas, "programmes/DETECTER_LES_SIGNAUX_GITHUB.py", ".")
            ct, ot, st = lancer(copie, pas, "programmes/TENIR_LES_POSITIONS.py", ".")
            cr, orad, _ = lancer(copie, pas, "programmes/audit_ecosysteme.py", ".")
            suivies = od.split("fiches suivies : ", 1)[1].splitlines()[0] if "fiches suivies : " in od else ""
            lu = (ident in suivies.split(" · ")[0] and fiche.get("module_signal", "?") in suivies
                  and fiche.get("fonction_signal", "?") in suivies
                  and ("horizon lu au registre · %s : %s seances" % (ident, horizon)) in ot)
            with open(os.path.join(copie, SIGNAUX), encoding="utf-8") as fh:
                du_jour = [x["valeur"] for x in json.load(fh).get("signaux", [])]
            hors_univers += ["%s %s" % (v, s) for v in du_jour if v not in univers]
            for p in lire_csv(os.path.join(copie, POSITIONS)):
                if p["strategie"] == ident and p["statut"] == "OUVERTE":
                    positions_essai[(p["valeur"], p["date_entree"], p["comptabilite"])] = p
                    pe = float(p["prix_entree"])
                    if abs(float(p["tp"]) - pe * (1 + tp_f)) > 0.01 or abs(float(p["sl"]) - pe * (1 - sl_f)) > 0.01:
                        ecarts_seuils.append("%s %s" % (p["valeur"], s))
            l11 = [l for l in orad.splitlines() if "11-Positions" in l and "TP/SL" in l]
            radar_essai += sum(1 for l in l11 if l.startswith("✅") and ident in l)
            soirs.append((s, cd, ct, cr, lu, st.get("fiches_mises_a_part")))
        bons = [x for x in soirs if x[1] == 0 and x[2] == 0 and x[3] == 0 and x[4] and x[5] == "0"]
        dire("M5", len(seances) >= 2 and len(bons) == len(seances),
             "%d séance(s) %s → %s · %d où le détecteur suit la fiche (signal %s · %s), le teneur lit son horizon (%s), "
             "radar code 0, aucune fiche mise à part · échecs : %s"
             % (len(seances), seances[0] if seances else "-", seances[-1] if seances else "-", len(bons),
                fiche.get("module_signal"), fiche.get("fonction_signal"), horizon,
                [x for x in soirs if x not in bons][:3]))

        # M6 — L'UNIVERS DE LA FICHE : aucune position ni aucun trade de la fiche d'essai hors de son univers, et au
        # moins un signal réel hors univers dans le rejeu (sinon la propriété ne serait pas éprouvée)
        trades = [t for t in lire_csv(os.path.join(copie, JOURNAL)) if t["strategie"] == ident]
        hors = [v for v in [k[0] for k in positions_essai] + [t["valeur"] for t in trades] if v not in univers]
        dire("M6", not hors and bool(hors_univers),
             "univers de la fiche %s · valeurs de la fiche d'essai hors univers : %s · signaux du rejeu hors univers "
             "(non servis à la fiche) : %s" % (sorted(univers), hors or "aucune", hors_univers or "AUCUN"))

        # M7 — POSITIONS ET TRADES PORTENT L'IDENTIFIANT DE LA FICHE D'ESSAI, aux seuils de la fiche
        net = sum(float(t["pnl_net_eur"]) for t in trades)
        dire("M7", bool(positions_essai) and bool(trades) and not ecarts_seuils and radar_essai > 0,
             "%d position(s) %s ouvertes vues · %d trade(s) %s au journal, net %+.2f EUR (%s) · seuils de la fiche "
             "+%.1f %% / -%.1f %%, écarts : %s · radar maillon 11 ✅ nommant la fiche : %d soir(s)"
             % (len(positions_essai), ident, len(trades), ident, net,
                ", ".join("%s %s→%s %s %s" % (t["valeur"], t["date_entree"], t["date_sortie"], t["motif_sortie"],
                                              t["comptabilite"]) for t in trades),
                tp_f * 100, sl_f * 100, ecarts_seuils or "aucun", radar_essai))
    except Exception as e:  # un maillon qui lève est un KO nommé, jamais un vert (R-734)
        dire("EXC", False, "%s : %s" % (type(e).__name__, e))
    finally:
        for m in ("CONTRATS_DES_FICHIERS", "PREPARER_LA_MOULINETTE_D_ESSAI", "JUGE_DES_STRATEGIES"):
            sys.modules.pop(m, None)
        while os.path.join(copie, "programmes") in sys.path:
            sys.path.remove(os.path.join(copie, "programmes"))
        essais_copie = registres_d_essais(copie) if os.path.isdir(copie) else []
        shutil.rmtree(lieu, ignore_errors=True)
        # M8 — LE VRAI DÉPÔT N'A CHANGÉ D'AUCUN OCTET (mesuré AVANT d'effacer le fichier du sabotage S3)
        empreinte_apres = empreinte_du_depot(RACINE)
        nommes_apres = {f: sha_court(os.path.join(RACINE, f)) for f in nommes_avant}
        if sabotage == "S3" and os.path.exists(os.path.join(RACINE, SABOTAGE_S3)):
            os.remove(os.path.join(RACINE, SABOTAGE_S3))
        dire("M8", empreinte_avant == empreinte_apres and nommes_avant == nommes_apres and not os.path.exists(lieu),
             "arbre %s (%d fichiers) avant · %s (%d) après · %s · copie effacée : %s"
             % (empreinte_avant[0], empreinte_avant[1], empreinte_apres[0], empreinte_apres[1],
                " · ".join("%s %s→%s" % (os.path.basename(f), nommes_avant[f], nommes_apres[f]) for f in nommes_avant),
                not os.path.exists(lieu)))
        # M9 — AUCUN REGARD
        regards_apres = regards_du_depot(RACINE)
        essais_apres = registres_d_essais(RACINE)
        dire("M9", regards_avant == [] and regards_apres == [] and not essais_avant and not essais_apres
             and not essais_copie,
             "branches regards/* : %s avant, %s après · registre_essais : %d au dépôt avant, %d après, %d dans la copie"
             % (regards_avant, regards_apres, len(essais_avant), len(essais_apres), len(essais_copie)))
    return res


# (code, ce qui est saboté, maillon qui doit rougir)
SABOTAGES = [
    ("S1", "marque retirée du verdict écrit dans la fiche", "M3"),
    ("S2", "fiche non suivie par le soir (etat_vie laissé LABO)", "M4"),
    ("S3", "une écriture dans le vrai dépôt (un fichier créé dans la racine)", "M8"),
]


def main():
    """Joue la chaîne, puis les sabotages ; affiche le rapport et rend le code.
    ① RÔLE — Le programme. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — RACINE, SABOTER. ④ CONDITIONS
    D'ENTRÉE — voir ④ du fichier. ⑤ SORTIE — UNE valeur, le code. [rend: 1] ⑥ TRAITEMENT — refuser une racine qui n'est
    pas un dépôt (code 2) ; Z0 ; avec --saboter, S1 à S3, chacun doit rougir son maillon. ⑦ UNITÉ — —. ⑧ POURQUOI — une
    épreuve qui reste verte quand on retire ce qu'elle teste est une décoration. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — ceux de
    `jouer_la_chaine`. ⑪ TERMINAISON — rend la main avec le code. [sort: non]"""
    if regards_du_depot(RACINE) is None:
        print("CODE 2 — %s n'est pas un dépôt git : les regards ne peuvent pas être comptés" % RACINE)
        return 2
    rouge = False
    print("RAPPORT — CHAÎNE C5 SUR COPIE (Z0, sans sabotage) · %s" % datetime.now(PARIS).strftime("%Y-%m-%d %H:%M Paris"))
    for code, ok, preuve in jouer_la_chaine():
        print("  %s %s — %s" % ("OK" if ok else "KO", code, preuve))
        rouge = rouge or not ok
    if SABOTER:
        for code, quoi, visé in SABOTAGES:
            kos = [c for c, ok, _p in jouer_la_chaine(code) if not ok]
            mord = visé in kos
            print("  %s %s %s → rougissent : %s (visé %s)" % ("✅" if mord else "❌", code, quoi, ", ".join(kos) or "AUCUN",
                                                           visé))
            rouge = rouge or not mord
    print("VERDICT : %s" % ("ROUGE" if rouge else "VERT"))
    return 1 if rouge else 0


if __name__ == "__main__":
    sys.exit(main())
