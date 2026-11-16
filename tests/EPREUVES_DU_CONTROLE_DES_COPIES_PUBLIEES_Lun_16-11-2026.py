#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CONTROLE_DES_COPIES_PUBLIEES — Lun 16-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. A-857 : l'étage A de la publication (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py,
`refus_selon_l_historique`) refuse toute publication dont un fichier écrit au public a le contenu entier d'un fichier du
dépôt privé à un chemin qui ne se publie pas, dans l'historique entier ou sur le disque. Le contrôle avant dépôt
`copies_de_fichiers_publies` de programmes/CONTROLER_MA_LIVRAISON.py en empêche la cause. Le 16-11-2026, le superviseur
R-759 (etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/SUPERVISEUR_COPIE_CTL_Lun_16-11-2026.md) a rendu
« RUSTINE, À REPRENDRE » : le contrôle réécrivait à la main le critère de l'étage A, et une copie commitée puis retirée
le passait (B1, la panne d'A-848) ; deux implémentations d'une même chose divergent toujours (R-708). Depuis, le
contrôle APPELLE l'étage A sur ce que la publication écrirait (`ce_que_la_publication_ecrit` du fabricant). Cette
épreuve joue les cas (a) à (j) du superviseur, chacun rougissant sur l'ancien calcul (sabotage SC03), et garde les
cas C1 à C8 de la première livraison (sabotages n° 7 à 11 du superviseur SUPERVISEUR_ETAGE_A_D1).

① RÔLE — Éprouver `copies_de_fichiers_publies` et son appel par `main` de programmes/CONTROLER_MA_LIVRAISON.py.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine, puis avec --saboter) ;
  à la main avant toute livraison qui touche ce contrôle (R-731) :
  python3 tests/EPREUVES_DU_CONTROLE_DES_COPIES_PUBLIEES_Lun_16-11-2026.py <racine> [--saboter]
③ ENTRÉE — La racine d'un dépôt : programmes/ (CONTROLER_MA_LIVRAISON.py, FABRIQUER_LE_CIRCUIT_PUBLIC.py,
  TENIR_UN_PLANNING.py et ce que le contrôle importe), emp.py, tests/LANCEMENT_DES_EPREUVES.json (la table des séries
  du fabricant), .github/workflows/collecte_abc.yml (le circuit privé, recopié dans chaque dépôt de cas).
④ CONDITIONS D'ENTRÉE — git installé ; aucun réseau (dépôts locaux jetables sous le dossier temporaire).
⑤ SORTIE — Le code de sortie : 0 si chaque cas donne la réponse attendue et, avec --saboter, si chaque sabotage en fait
  échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus ou si une copie sabotée ne charge pas sa table.
  [rend: 1]
⑥ TRAITEMENT — Un dépôt jetable par cas : main porte programmes/TENIR_UN_PLANNING.py (le VRAI contenu de la racine,
  R-732), programmes/DONNEES_EN_CODE.py (un texte de forme CSV), tests/outils/OUTIL.py, programmes/VIDE.py (vide) et
  le vrai .github/workflows/collecte_abc.yml ; `origin/main` est posé sur ce commit ; la livraison est la branche
  travail-cas. « Refusé » veut dire : un refus de l'étage A nomme le blob attendu. Puis :
  C1 (n° 7, A-848 rejoué) la copie à l'octet de TENIR_UN_PLANNING.py au chemin d'A-848, indexée → refusée ; le
     programme entier → code non nul, motif « COPIE D UN FICHIER PUBLIÉ » ;
  C2 (n° 8) la même copie avec UN octet changé → rien (pas de sur-détection) ;
  C3 (n° 9) la copie sous un autre nom et dans un autre dossier, non suivie, puis commitée → refusée chaque fois ;
  C4 (n° 10) donnees/copie.csv identique à programmes/DONNEES_EN_CODE.py → refusée ;
  C5 (n° 11) HEAD sans commit (branche orpheline) → erreur ; le programme entier → motif « NON MESURÉES (R-734) » ;
  C6 un fichier vide à un chemin privé → rien (le blob vide n'est pas un contenu) ;
  C7 TENIR_UN_PLANNING.py modifié sur le disque, sa nouvelle version copiée sous etudes/ → refusée ;
  C8 la copie de tests/outils/OUTIL.py (publié : le critère est celui du fabricant) → refusée ;
  C9 un programme NEUF non suivi (programmes/NEUF.py), et sa copie commitée sous etudes/ → refusée (ce qui sera
     publié comprend les fichiers non suivis) ;
  CA (a, B1) une copie commitée puis retirée par un commit → refusée ;
  CB (b) une copie sur une autre branche locale seulement → refusée ;
  CC (c) une copie introduite par la résolution d'un commit de fusion, puis retirée → refusée ;
  CD (d) une copie présente sur origin/main → refusée ;
  CE (e) un fichier publié ramené au blob d'une ancienne version déjà rangée dans archives/ → refusé ;
  CF (f) la copie d'un circuit fabriqué (le gabarit CERTIFICATION du fabricant) rangée sous etudes/ → refusée ;
  CF2 (f bis, m1 du relecteur A-857 tour 2) la copie d'une FICHE de circuit publiée (le vrai collecte_abc.yml, publié
     à l'octet sous circuits_du_prive/) rangée sous etudes/ → refusée (sabotage SC12 : la fiche n'est plus confrontée) ;
  CG (g, M2, calibrage) l'ancienne version archivée avant le commit, le programme modifié sur le disque → RIEN ;
  CH (h) une copie jamais indexée → refusée ;
  CI (i) aucun refus ne propose « retirer » ; la ligne du motif du programme entier ne propose pas de retirer la
     COPIE (« la retirer », « retirer la copie ») et, depuis m2 (relecteur A-857 tour 2), nomme le retrait d'un objet
     LOCAL et ses trois commandes (git branch -D, git stash drop, git fetch --prune ; sabotage SC13) ; chaque refus
     porte « changer une ligne du fichier publié » ;
  CJ (j) git cassé (HEAD illisible) → erreur ; dépôt superficiel → erreur ; le programme entier → motif R-734.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — R-731 : tout code écrit a ses épreuves au dépôt, et chaque garde un sabotage qui mord pour sa raison.
  Le sabotage SC03 remet l'ANCIEN calcul (texte ANCIEN_CALCUL, le corps d'a6ad6018 sans ses fiches) à la place de
  l'appel : les cas (a) à (g) doivent rougir dessus — c'est la preuve qu'ils mesurent la divergence.
⑨ CE QUI CLOCHE — Le pas de commit du circuit, que nomme aussi A-857, n'est pas éprouvé (il n'est pas écrit). Le
  programme entier est lancé sur un dépôt minuscule : il y refuse aussi pour d'autres motifs (pas de REGISTRE, pas de
  passes) ; l'épreuve ne juge que la présence ou l'absence de SON motif. Les dépôts de cas n'ont pas de registre de
  provenance : le témoin de l'étage A y est sans objet (il est éprouvé par
  tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py). La sur-détection locale (branches périmées,
  remise) n'est pas éprouvée : elle est voulue (fiche ⑨ du contrôle) ; seul le TEXTE qui la nomme l'est (CI, m2).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

DEPOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
CONTROLE = os.path.join("programmes", "CONTROLER_MA_LIVRAISON.py")
FABRICANT = os.path.join("programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py")
TABLE = os.path.join("tests", "LANCEMENT_DES_EPREUVES.json")
CIRCUIT = ".github/workflows/collecte_abc.yml"
PLANNING = "programmes/TENIR_UN_PLANNING.py"
CHEMIN_A848 = "etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/planning_reel_Lun_16-11-2026/programmes/TENIR_UN_PLANNING.py"
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="e", GIT_AUTHOR_EMAIL="e@e", GIT_COMMITTER_NAME="e",
               GIT_COMMITTER_EMAIL="e@e", GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
MOTIF = "COPIE D UN FICHIER PUBLIÉ"
MOTIF_ERREUR = "COPIES DE FICHIERS PUBLIÉS NON MESURÉES (R-734)"
REMEDE = "changer une ligne du fichier publié"
DOCUMENT = "Rôle : porter le travail soumis à relecture\n\n# R-740\n\n**① mandat inversé**\n"


def lancer(args, cwd=None):
    """Lance une commande ; rend (code, sortie et erreurs réunies).

    ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — `args`, `cwd`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, le texte. [rend: 2] ⑥ TRAITEMENT — subprocess, 300 s.
    ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : rangé parmi les
    cas faux. ⑩ EFFET — Ce que fait la commande. ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, env=GIT_ENV, cwd=cwd, timeout=300, errors="replace")
    return p.returncode, p.stdout + p.stderr


def git(p, *args):
    """Lance git dans un dépôt de cas et lève si git échoue.

    ① RÔLE — Construire un décor sans échec silencieux (R-734). ② CONTEXTE D'APPEL — `tour`, `depot_jetable`.
    ③ ENTRÉE — `p`, `args`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la sortie. [rend: 1]
    ⑥ TRAITEMENT — `lancer`. ⑦ UNITÉ — —. ⑧ POURQUOI — Un décor raté ferait passer un cas pour une bonne raison
    fausse. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — git. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    code, sortie = lancer(["git", "-C", p, *args])
    if code != 0:
        raise RuntimeError(f"décor : git {' '.join(args)} : {sortie.strip()[:200]}")
    return sortie


def charger(racine, fichier, prefixe):
    """Charge un programme de la racine comme un module.

    ① RÔLE — Appeler le contrôle (ou lire le fabricant) de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`, `main`.
    ③ ENTRÉE — `racine`, `fichier`, `prefixe`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — importlib, sous un nom propre à la racine. ⑦ UNITÉ — — ⑧ POURQUOI — Une copie sabotée ne doit pas
    réutiliser le module déjà chargé. ⑨ CE QUI CLOCHE — Le code de tête s'exécute. ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    nom = prefixe + str(abs(hash(racine)))
    spec = importlib.util.spec_from_file_location(nom, os.path.join(racine, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ecrire(p, rel, contenu):
    """Écrit un fichier d'un dépôt de cas.

    ① RÔLE — —. ② CONTEXTE D'APPEL — `depot_jetable`, `tour`. ③ ENTRÉE — `p`, `rel`, `contenu` (octets).
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune valeur. [rend: rien] ⑥ TRAITEMENT — —. ⑦ UNITÉ — —.
    ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Écrit. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    os.makedirs(os.path.dirname(os.path.join(p, rel)), exist_ok=True)
    with open(os.path.join(p, rel), "wb") as f:
        f.write(contenu)


def depot_jetable(d, nom, planning, avant_origine=None):
    """Fabrique un dépôt git de cas : main commité, `origin/main` posé dessus, branche travail-cas ; rend son chemin.

    ① RÔLE — Le décor commun des cas. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `d` : dossier jetable ; `nom` ;
    `planning` : les octets du vrai TENIR_UN_PLANNING.py ; `avant_origine` : fichiers (chemin → octets) commités sur
    main dans un second commit AVANT de poser origin/main, ou None. ④ CONDITIONS D'ENTRÉE — git installé.
    ⑤ SORTIE — UNE valeur : le chemin du dépôt. [rend: 1] ⑥ TRAITEMENT — init, cinq fichiers, commit, update-ref.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le circuit privé est le vrai : le contrôle fabrique le circuit public comme le fabricant.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans `d`. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    p = os.path.join(d, nom)
    code, sortie = lancer(["git", "init", "-q", "-b", "main", p])
    if code != 0:
        raise RuntimeError("décor : git init : " + sortie[:200])
    circuit = open(os.path.join(DEPOT, *CIRCUIT.split("/")), "rb").read()
    for rel, c in ((PLANNING, planning), ("programmes/DONNEES_EN_CODE.py", b"date,valeur\n2001-02-03,12.34\n"),
                   ("tests/outils/OUTIL.py", b"OUTIL = 7\n"), ("programmes/VIDE.py", b""), (CIRCUIT, circuit)):
        ecrire(p, rel, c)
    git(p, "add", "-A")
    git(p, "commit", "-qm", "main")
    if avant_origine:
        for rel, c in avant_origine.items():
            ecrire(p, rel, c)
        git(p, "add", "-A")
        git(p, "commit", "-qm", "main 2")
    git(p, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(p, "checkout", "-q", "-b", "travail-cas")
    return p


def tout_le_controle(racine, p):
    """Lance le programme entier de la racine sur une livraison du dépôt de cas ; rend (code, sortie).

    ① RÔLE — Prouver que `main` refuse pour le motif, pas seulement que la fonction le rend. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `racine` : la racine éprouvée ; `p` : le dépôt de cas. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code, la sortie. [rend: 2] ⑥ TRAITEMENT — echanges/A_RELIRE.md minimal, « --verifier ».
    ⑦ UNITÉ — — ⑧ POURQUOI — « --verifier » n'écrit rien. ⑨ CE QUI CLOCHE — D'autres motifs refusent aussi (fiche ⑨).
    ⑩ EFFET — Écrit le document dans `p`. ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    ecrire(p, "echanges/A_RELIRE.md", DOCUMENT.encode("utf-8"))
    return lancer([sys.executable, "-B", os.path.join(racine, CONTROLE), os.path.join(p, "echanges", "A_RELIRE.md"),
                   "--verifier"], cwd=p)


def blob(octets):
    """Rend l'identifiant git d'un contenu.

    ① RÔLE — Nommer le blob qu'un refus doit porter. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `octets`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : 40 caractères hexadécimaux. [rend: 1]
    ⑥ TRAITEMENT — sha1(« blob <taille>\\0 » + contenu), écrit ici en toutes lettres et non lu dans le fabricant.
    ⑦ UNITÉ — —. ⑧ POURQUOI — Une empreinte lue dans le programme éprouvé suivrait son sabotage.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import hashlib
    return hashlib.sha1(b"blob %d\0" % len(octets) + octets).hexdigest()


def refuse(r, e, octets):
    """Dit si la réponse du contrôle refuse le contenu `octets` (un refus qui porte son blob entier), sans erreur.

    ① RÔLE — Le jugement « refusé » de la fiche en tête. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `r`, `e` : la réponse ;
    `octets`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : vrai ou faux. [rend: 1] ⑥ TRAITEMENT — —.
    ⑦ UNITÉ — —. ⑧ POURQUOI — Juger par le blob vaut pour le nouveau calcul comme pour l'ancien (SC03). ⑨ CE QUI
    CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return not e and bool(r) and any(f"blob {blob(octets)}" in x for x in r)


def tour(racine):
    """Joue tous les cas sur une racine ; rend la liste des cas faux (vide : tout est conforme).

    ① RÔLE — Le corps de l'épreuve (fiche en tête, ⑥). ② CONTEXTE D'APPEL — `main`, sur la racine puis sur chaque
    copie sabotée. ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des cas faux. [rend: 1] ⑥ TRAITEMENT — Fiche en tête, ⑥. ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Une erreur imprévue d'un cas est rangée parmi les cas faux, et les
    cas suivants ne sont pas joués : elle ne fait jamais passer un tour.
    ⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="copies_publiees_")
    try:
        C = charger(racine, CONTROLE, "controle_")
        F = charger(racine, FABRICANT, "fabricant_")
        planning = open(os.path.join(racine, PLANNING), "rb").read()
        tous_les_refus = []

        def copies(p):
            """La fonction éprouvée. ① RÔLE — —. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `p`.
            ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — garde les refus pour CI.
            ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — git. ⑪ TERMINAISON — Rend la main.
            [sort: non]"""
            r, e = C.copies_de_fichiers_publies(p)
            tous_les_refus.extend(r or [])
            return r, e

        # C1 (n° 7) : A-848 rejoué
        p = depot_jetable(d, "c1", planning)
        ecrire(p, CHEMIN_A848, planning)
        git(p, "add", CHEMIN_A848)
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"C1 A-848 rejoué : {r} ; {e}")
        code, sortie = tout_le_controle(racine, p)
        lignes_du_motif = [l for l in sortie.splitlines() if MOTIF in l]
        if code == 0 or not lignes_du_motif or blob(planning) not in sortie:
            faux.append(f"C1 programme entier : code {code}, motif ou blob absent : {sortie[-300:]}")
        # CI (i) : la ligne du motif ne propose jamais de retirer la COPIE (l'étage A lit l'historique entier) ;
        # depuis m2 (relecteur A-857 tour 2), elle nomme le retrait d'un objet LOCAL et ses trois commandes
        for l in lignes_du_motif:
            bas = l.lower()
            if "la retirer" in bas or "retirer la copie" in bas:
                faux.append(f"CI (i) la ligne du motif propose de retirer la copie : {l[:300]}")
            manque = [c for c in ("git branch -D", "git stash drop", "git fetch --prune") if c not in l]
            if manque:
                faux.append(f"CI (i, m2) la ligne du motif ne nomme pas le retrait local {manque} : {l[:300]}")
        # C2 (n° 8) : un octet changé
        p = depot_jetable(d, "c2", planning)
        ecrire(p, CHEMIN_A848, planning[:-1] + (b"\r" if planning[-1:] != b"\r" else b"\n"))
        git(p, "add", CHEMIN_A848)
        r, e = copies(p)
        if e or r:
            faux.append(f"C2 un octet changé relevé : {r} ; {e}")
        code, sortie = tout_le_controle(racine, p)
        if MOTIF in sortie:
            faux.append("C2 programme entier : motif présent pour un octet changé")
        # C3 (n° 9) : autre nom, autre dossier, non suivi, puis commité
        p = depot_jetable(d, "c3", planning)
        ecrire(p, "etudes/sauvegarde.txt", planning)
        ecrire(p, "archives/vieux/x.py", planning)
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"C3 autre nom / autre dossier non suivis : {r} ; {e}")
        git(p, "add", "-A")
        git(p, "commit", "-qm", "copies")
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"C3 copies commitées sur la branche : {r} ; {e}")
        # C4 (n° 10) : un .csv identique à un fichier publié
        p = depot_jetable(d, "c4", planning)
        ecrire(p, "donnees/copie.csv", b"date,valeur\n2001-02-03,12.34\n")
        r, e = copies(p)
        if not refuse(r, e, b"date,valeur\n2001-02-03,12.34\n"):
            faux.append(f"C4 .csv identique : {r} ; {e}")
        # C5 (n° 11) : HEAD sans commit
        p = depot_jetable(d, "c5", planning)
        git(p, "checkout", "-q", "--orphan", "orpheline")
        git(p, "rm", "-rq", "--cached", ".")
        r, e = copies(p)
        if r is not None or not e:
            faux.append(f"C5 HEAD sans commit : rend {r} ; erreur {e}")
        code, sortie = tout_le_controle(racine, p)
        if code == 0 or MOTIF_ERREUR not in sortie:
            faux.append(f"C5 programme entier : code {code}, motif R-734 absent : {sortie[-300:]}")
        # C6 : un fichier vide n'est pas une copie
        p = depot_jetable(d, "c6", planning)
        ecrire(p, "etudes/vide.txt", b"")
        r, e = copies(p)
        if e or r:
            faux.append(f"C6 fichier vide relevé : {r} ; {e}")
        # C7 : la version du disque d'un fichier publié modifié
        p = depot_jetable(d, "c7", planning)
        neuf = planning + b"# ligne ajoutee\n"
        ecrire(p, PLANNING, neuf)
        ecrire(p, "etudes/neuf.py", neuf)
        r, e = copies(p)
        if not refuse(r, e, neuf):
            faux.append(f"C7 copie de la version du disque : {r} ; {e}")
        # C8 : le critère « publié » est celui du fabricant (tests/outils/ se publie)
        p = depot_jetable(d, "c8", planning)
        ecrire(p, "etudes/outil_copie.py", b"OUTIL = 7\n")
        r, e = copies(p)
        if not refuse(r, e, b"OUTIL = 7\n"):
            faux.append(f"C8 copie d'un fichier publié de tests/outils/ : {r} ; {e}")
        # C9 : un programme neuf non suivi sera publié ; sa copie commitée est refusée
        p = depot_jetable(d, "c9", planning)
        prog_neuf = b"NEUF = 'programme neuf du 16-11-2026'\n"
        ecrire(p, "etudes/copie_du_neuf.py", prog_neuf)
        git(p, "add", "-A")
        git(p, "commit", "-qm", "copie")
        ecrire(p, "programmes/NEUF.py", prog_neuf)
        r, e = copies(p)
        if not refuse(r, e, prog_neuf):
            faux.append(f"C9 programme neuf non suivi et sa copie : {r} ; {e}")
        # CA (a, B1) : une copie commitée puis retirée par un commit
        p = depot_jetable(d, "ca", planning)
        ecrire(p, CHEMIN_A848, planning)
        git(p, "add", "-A")
        git(p, "commit", "-qm", "copie")
        git(p, "rm", "-q", CHEMIN_A848)
        git(p, "commit", "-qm", "retrait")
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"CA (a) copie commitée puis retirée : {r} ; {e}")
        # CB (b) : une copie sur une autre branche locale seulement
        p = depot_jetable(d, "cb", planning)
        git(p, "checkout", "-q", "-b", "autre")
        ecrire(p, "etudes/sur_autre_branche.py", planning)
        git(p, "add", "-A")
        git(p, "commit", "-qm", "copie ailleurs")
        git(p, "checkout", "-q", "travail-cas")
        r, e = copies(p)
        if os.path.exists(os.path.join(p, "etudes", "sur_autre_branche.py")) or not refuse(r, e, planning):
            faux.append(f"CB (b) copie sur une autre branche : {r} ; {e}")
        # CC (c) : une copie introduite par la résolution d'un commit de fusion, puis retirée
        p = depot_jetable(d, "cc", planning)
        git(p, "checkout", "-q", "-b", "cote")
        ecrire(p, "etudes/cote.txt", b"cote\n")
        git(p, "add", "-A")
        git(p, "commit", "-qm", "cote")
        git(p, "checkout", "-q", "travail-cas")
        ecrire(p, "etudes/ici.txt", b"ici\n")
        git(p, "add", "-A")
        git(p, "commit", "-qm", "ici")
        git(p, "merge", "-q", "--no-ff", "--no-commit", "cote")
        ecrire(p, "etudes/dans_la_fusion.py", planning)
        git(p, "add", "-A")
        git(p, "commit", "-qm", "fusion")
        git(p, "rm", "-q", "etudes/dans_la_fusion.py")
        git(p, "commit", "-qm", "retrait")
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"CC (c) copie introduite par une fusion : {r} ; {e}")
        # CD (d) : une copie présente sur origin/main
        p = depot_jetable(d, "cd", planning, avant_origine={"etudes/sur_main.py": b"OUTIL = 7\n"})
        r, e = copies(p)
        if not refuse(r, e, b"OUTIL = 7\n"):
            faux.append(f"CD (d) copie sur origin/main : {r} ; {e}")
        # CE (e) : fichier publié ramené au blob d'une ancienne version déjà archivée (sur main et origin/main)
        v2 = planning + b"# version 2\n"
        p = depot_jetable(d, "ce", planning, avant_origine={"archives/TENIR_UN_PLANNING_v1.py": planning, PLANNING: v2})
        ecrire(p, PLANNING, planning)
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"CE (e) retour au blob d'une version archivée : {r} ; {e}")
        # CF (f) : la copie d'un circuit fabriqué rangée au privé
        p = depot_jetable(d, "cf", planning)
        certification = F.CERTIFICATION.encode("utf-8")
        ecrire(p, "etudes/certifier_la_version_copie.yml", certification)
        r, e = copies(p)
        if not refuse(r, e, certification):
            faux.append(f"CF (f) copie d'un circuit fabriqué : {str(r)[:300]} ; {e}")
        # CF2 (f bis, m1 du relecteur A-857 tour 2) : la copie d'une FICHE de circuit publiée (le vrai
        # .github/workflows/collecte_abc.yml, publié à l'octet sous circuits_du_prive/) rangée au privé → refusée
        p = depot_jetable(d, "cf2", planning)
        fiche = open(os.path.join(DEPOT, *CIRCUIT.split("/")), "rb").read()
        ecrire(p, "etudes/collecte_abc_copie.yml", fiche)
        r, e = copies(p)
        if not refuse(r, e, fiche):
            faux.append(f"CF2 (f bis) copie d'une fiche de circuit publiée : {str(r)[:300]} ; {e}")
        # CG (g, M2, calibrage) : l'ancienne version archivée avant le commit, le programme modifié → RIEN
        p = depot_jetable(d, "cg", planning)
        ecrire(p, "archives/TENIR_UN_PLANNING_avant_v2.py", planning)
        ecrire(p, PLANNING, planning + b"# version 2\n")
        r, e = copies(p)
        if e or r:
            faux.append(f"CG (g, M2) archiver l'ancienne version avant le commit est refusé : {str(r)[:300]} ; {e}")
        # CH (h) : une copie jamais indexée
        p = depot_jetable(d, "ch", planning)
        ecrire(p, "etudes/jamais_indexee.py", planning)
        r, e = copies(p)
        if not refuse(r, e, planning):
            faux.append(f"CH (h) copie non suivie : {r} ; {e}")
        # CI (i) : aucun refus ne propose « retirer » ; chacun porte le remède unique
        mauvais = [x for x in tous_les_refus if "retir" in x.lower() or REMEDE not in x]
        if not tous_les_refus or mauvais:
            faux.append(f"CI (i) remède : {len(tous_les_refus)} refus, dont {len(mauvais)} sans le remède unique "
                        f"ou qui proposent de retirer : {mauvais[:1]}")
        # CJ (j) : git cassé, puis dépôt superficiel
        p = depot_jetable(d, "cj", planning)
        with open(os.path.join(p, ".git", "HEAD"), "w", encoding="utf-8") as f:
            f.write("ceci n est pas une reference\n")
        r, e = copies(p)
        if r is not None or not e:
            faux.append(f"CJ (j) git cassé : rend {r} ; erreur {e}")
        p = depot_jetable(d, "cj_source", planning)
        git(p, "commit", "-q", "--allow-empty", "-m", "deux")
        superficiel = os.path.join(d, "cj_superficiel")
        code, sortie = lancer(["git", "clone", "-q", "--depth", "1", "file://" + p, superficiel])
        if code != 0:
            raise RuntimeError("décor : clone superficiel : " + sortie[:200])
        r, e = copies(superficiel)
        if r is not None or not e or "SUPERFICIEL" not in e:
            faux.append(f"CJ (j) dépôt superficiel : rend {r} ; erreur {e}")
        code, sortie = tout_le_controle(racine, superficiel)
        if code == 0 or MOTIF_ERREUR not in sortie:
            faux.append(f"CJ (j) programme entier, dépôt superficiel : code {code}, motif R-734 absent : {sortie[-300:]}")
    except Exception as e:   # noqa: BLE001 — une erreur imprévue est un cas faux, jamais un passage
        faux.append(f"erreur imprévue : {type(e).__name__} : {e}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux



# L'ANCIEN CALCUL (a6ad6018, `copies_de_fichiers_publies` sans ses fiches) : le sabotage SC03 le remet à la place de
# l'appel à l'étage A. Il est ici en toutes lettres, jamais relu dans l'historique : la certification joue une copie
# sans .git.
ANCIEN_CALCUL = r'''
def _ancien_calcul(racine):
    F = _fabricant()
    vide = F.empreinte_git(b'')
    base_ref = 'refs/remotes/origin/main'

    def disque(rel):
        p = os.path.join(racine, *rel.split('/'))
        if os.path.islink(p) or not os.path.isfile(p):
            return None
        with open(p, 'rb') as fh:
            return F.empreinte_git(fh.read())

    def lister(*arguments):
        r = _git(racine, *arguments)
        if r.returncode != 0:
            raise OSError(f"git {arguments[0]} : code {r.returncode} : {(r.stderr or '').strip()[:200]}")
        return [c for c in r.stdout.split('\x00') if c]
    try:
        avec_base = _git(racine, 'rev-parse', '--verify', '--quiet', base_ref).returncode == 0
        arbre = {}
        for e in lister('ls-tree', '-r', '-z', '--full-tree', 'HEAD'):
            meta, chemin = e.split('\t', 1)
            mode, _type, blob = meta.split()
            if mode in ('100644', '100755'):
                arbre[chemin] = blob
        index = {}
        for e in lister('ls-files', '-s', '-z'):
            meta, chemin = e.split('\t', 1)
            index[chemin] = meta.split()[1]
        if avec_base:
            livres = set(lister('diff', '--name-only', '-z', '--no-renames', base_ref))
            livres |= set(lister('diff', '--cached', '--name-only', '-z', '--no-renames', base_ref))
        else:
            livres = set(arbre) | set(index)
        livres |= set(lister('ls-files', '-z', '--others', '--exclude-standard'))
        publies = {}
        for chemin in set(arbre) | {c for c in livres if F.est_un_chemin_publie(c)}:
            if not F.est_un_chemin_publie(chemin):
                continue
            for b in (arbre.get(chemin), disque(chemin)):
                if b and b != vide:
                    publies.setdefault(b, set()).add(chemin)
        copies = []
        for chemin in sorted(livres):
            if F.est_un_chemin_publie(chemin):
                continue
            for b in dict.fromkeys((disque(chemin), index.get(chemin), arbre.get(chemin))):
                if b and b in publies:
                    copies.append(f'{chemin} = {sorted(publies[b])[0]} (blob {b})')
                    break
        return (copies, None)
    except (OSError, ValueError) as e:
        return (None, f'{type(e).__name__} : {e}')
'''

DEBUT_DU_CORPS = "    import posixpath\n    import shutil as _sh\n    import tempfile as _tf\n"
SABOTAGES = {
    "SC01_controle_desactive_dans_main": [(CONTROLE, "    elif _copies:\n", "    elif False:\n")],
    "SC02_fonction_ne_rend_rien": [(CONTROLE, "        return sorted(de_l_etage_a), None\n", "        return [], None\n")],
    "SC03_ancien_calcul_a_la_place_de_l_appel": [
        (CONTROLE, DEBUT_DU_CORPS, "    return _ancien_calcul(racine)\n" + DEBUT_DU_CORPS),
        (CONTROLE, "\ndef epreuves_de(racine, programme):\n", "\n" + ANCIEN_CALCUL + "\n\ndef epreuves_de(racine, programme):\n")],
    "SC04_erreur_de_git_tue": [(CONTROLE, '    except (OSError, ValueError) as e:\n        return None, f"{type(e).__name__} : {e}"\n    finally:\n',
                                '    except (OSError, ValueError) as e:\n        return [], None\n    finally:\n')],
    "SC05_critere_recopie": [(CONTROLE, "        F = _fabricant()\n",
                              "        F = _fabricant()\n        F.est_un_chemin_publie = lambda c: c.startswith('programmes/')\n")],
    "SC06_sans_les_circuits_fabriques": [
        (CONTROLE, "        ecritures = F.ce_que_la_publication_ecrit(racine, a_publier, fiches, texte)\n",
         "        ecritures = F.ce_que_la_publication_ecrit(racine, a_publier, fiches, texte)\n"
         "        ecritures = ecritures[:len(a_publier) + len(fiches)]\n")],
    "SC07_sans_les_fichiers_non_suivis": [(CONTROLE, '"ls-files", "-z", "--cached", "--others", "--exclude-standard")',
                                          '"ls-files", "-z", "--cached")')],
    "SC08_remede_qui_propose_de_retirer": [
        (FABRICANT, 'REMEDE_DE_L_ETAGE_A = "changer une ligne du fichier publié (comme 32aa88d0)"',
         'REMEDE_DE_L_ETAGE_A = "changer une ligne du fichier publié (comme 32aa88d0) ou retirer la copie"')],
    "SC09_message_de_main_qui_propose_de_retirer": [
        (CONTROLE, "chaque refus ci-après est le sien, avec son remède. ",
         "chaque refus ci-après est le sien ; sinon, la retirer (git garde chaque version). ")],
    "SC10_depot_superficiel_tolere": [
        (FABRICANT, '        if _git_prive(prive, "rev-parse", "--is-shallow-repository").strip() != b"false":\n',
         '        if False:\n')],
    "SC11_head_non_exige": [(CONTROLE, "        if tete.returncode != 0:\n", "        if False:\n")],
    # m1 du relecteur A-857 tour 2 : les fiches de .github/workflows/ ne sont plus confrontées → CF2 doit rougir
    "SC12_fiches_de_circuit_non_confrontees": [
        (CONTROLE, "                fiches.append(posixpath.basename(chemin))\n", "                pass\n")],
    # m2 du relecteur A-857 tour 2 : la phrase du retrait d'un objet local disparaît du message → CI doit rougir
    "SC13_message_sans_le_retrait_local": [
        (CONTROLE,
         '                     "Si la copie ne vit que dans un objet LOCAL — une branche locale jamais poussée, une remise "\n'
         '                     "(stash), une référence distante périmée —, retirer cet objet suffit (git branch -D <branche>, "\n'
         '                     "git stash drop, git fetch --prune) et aucun fichier publié n a à changer : "\n',
         '                     ": "\n')],
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter, une copie de programmes/, d'emp.py et de la table des séries par
      sabotage, le fichier visé écrit saboté, la table vérifiée chargée par le fabricant copié, un tour par copie.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. Une copie dont le fabricant ne lit pas sa table refuserait tout (R-734) :
      chaque sabotage « mordrait » pour une mauvaise raison ; elle arrête l'épreuve (code 2).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(DEPOT)
    print("Z0 programmes tels quels : " + ("C1 à C9 et CA à CJ conformes" if not faux else "FAUX " + " | ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv:
        for nom, gestes in SABOTAGES.items():
            d = tempfile.mkdtemp(prefix="copies_publiees_sab_")
            try:
                shutil.copytree(os.path.join(DEPOT, "programmes"), os.path.join(d, "programmes"),
                                ignore=shutil.ignore_patterns("__pycache__"))
                shutil.copyfile(os.path.join(DEPOT, "emp.py"), os.path.join(d, "emp.py"))
                os.makedirs(os.path.join(d, "tests"), exist_ok=True)
                shutil.copyfile(os.path.join(DEPOT, TABLE), os.path.join(d, TABLE))
                for fichier, a, b in gestes:
                    t = open(os.path.join(d, fichier), encoding="utf-8").read()
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                        return 2
                    open(os.path.join(d, fichier), "w", encoding="utf-8").write(t.replace(a, b))
                erreur = charger(d, FABRICANT, "table_").ERREUR_DE_LA_TABLE
                if erreur:
                    print(f"{nom} : la copie ne lit pas sa table des séries ({erreur}) — épreuve arrêtée")
                    return 2
                f = tour(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f[:12]}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
