#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEPOSER_UNE_DEMANDE — Mer 18-11-2026 (Paris). Simulation uniquement — aucun ordre réel.

LE SENS EN TÊTE. Déposer au dépôt public une demande pour le relais (.github/workflows/demande_de_serie.yml) SANS
l'écrire à la main : le nom est fabriqué à l'horloge de Paris, la pointe est lue au dépôt privé juste avant, et la
demande est examinée par LE MÊME TEXTE que celui du relais avant d'être poussée. Une demande refusée ne part donc
jamais, et le refus se voit tout de suite, ici, au lieu d'un passage rouge sur GitHub que personne ne regarde.
Cas fondateur (carte des pannes du 18-11-2026, A-897, panne P3, et A-895 ⑳) : des demandes écrites à la main ont été
refusées pour leur forme (nom non strict, pointe absente ou mal écrite, plus d'un fichier dans le commit).

① RÔLE — Écrire, examiner et (avec --pousser) pousser UNE demande demandes/DEMANDE_<AAAA-MM-JJ_HHhMM>.txt sur une
  branche du dépôt public (main ou travail-…), seule dans un commit à elle dont le parent est la pointe de la branche.
② CONTEXTE D'APPEL — À la main par le Chat (R-754 : ce qu'un programme peut faire, un programme le fait), et par
  l'ordonnanceur prévu par A-898. Exemples :
    python3 programmes/DEPOSER_UNE_DEMANDE.py /home/claude/pub main circuit=series serie=Yahoo --pousser
    python3 programmes/DEPOSER_UNE_DEMANDE.py /home/claude/pub main circuit=examen --pousser
③ ENTRÉE — La ligne de commande : le chemin d'un clone du dépôt public (son « origin » est le dépôt public) ; la
  branche publique visée ; des réglages « cle=valeur » (circuit obligatoire ; serie, epreuves, parts_<code>,
  lot_<code>, a_blanc : ceux que le relais connaît ; « version » est écrite par le programme, égale à la
  branche, jamais donnée à la main) ; « --prive=<adresse> » (par défaut le dépôt privé de
  FABRIQUER_LE_CIRCUIT_PUBLIC.DEPOT_PRIVE) ; « --pousser » (sans lui, rien n'est poussé : la demande est seulement
  fabriquée et examinée).
④ CONDITIONS D'ENTRÉE — git et bash installés ; le clone public peut lire (et, avec --pousser, pousser) son
  « origin » ; le dépôt privé se lit par « git ls-remote » avec les accès de la machine. La clé « pointe » n'est pas
  admise en entrée : elle est TOUJOURS lue au dépôt privé, sur la branche de même nom, pour les circuits qui la
  prennent (séries, épreuves) ; l'examen n'en prend pas.
⑤ SORTIE — Le code de sortie : 0 demande déposée (ou, sans --pousser, fabriquée et acceptée par l'examen) ; 1 demande
  refusée (par ce programme ou par l'examen du relais, dont « relais de la branche ancien »), rien n'est poussé ; 2 rien
  n'a pu être conclu (dépôt illisible, poussée refusée sans que la branche ait avancé, poussée refusée puis branche
  illisible, poussée sans réponse dans le délai — elle a PU aboutir —, poussée refusée trois fois) (R-734). La dernière ligne imprimée donne l'identifiant de la demande,
  DEMANDE_<AAAA-MM-JJ_HHhMM>@<branche>, que le passage lancé porte dans son titre (pour le retirer de la file de
  GitHub : « gh run cancel » sur ce passage).
  [rend: 1]
⑥ TRAITEMENT — `main` : lire la ligne de commande ; lire la pointe au privé ; jusqu'à trois fois : lire la pointe de
  la branche publique, fabriquer le nom (minute suivante si ce nom existe déjà sur la branche), fabriquer le commit
  sans toucher l'index ni la copie de travail du clone (`fabriquer_le_commit`), l'examiner (`examiner`), et pousser
  sans forcer ; une poussée refusée recommence avec la pointe nouvelle SI la branche publique a avancé (une course
  perdue) ; sinon le refus n'est pas une course (un crochet, un droit) : il est affiché EN ENTIER et rien n'est
  retenté (point T5 du RELU de travail-file-demandes, 18-11-2026 : le motif du crochet pre-push disparaissait, seuls
  les 200 derniers caractères étaient gardés, et le même refus était retenté trois fois). Si la branche ne se lit
  plus après le refus, rien ne dit si c'est une course : rien n'est retenté, code 2 (N3 du RELU du 25-11-2026). Une
  poussée sans réponse dans le délai rend code 2 et le dit : elle a PU aboutir, lire la branche avant de redéposer
  (C4 du même RELU).
  L'examen refuse aussi une branche dont le relais n'est pas une file du groupe GROUPE_DU_RELAIS (point T1 du même
  RELU, parade ② du relecteur, 25-11-2026) : un ancien relais, sans « queue: max », publié sur la branche, ferait
  annuler en silence une demande en attente ; la demande n'y est donc jamais poussée.
⑦ UNITÉ — —
⑧ POURQUOI — A-897 (P3) et A-898 ; R-708 : les motifs (NOM_DE_DEMANDE, MOTIF_DE_POINTE, MOTIF_DE_VERSION) et
  l'examen (EXAMEN_D_UNE_DEMANDE) sont IMPORTÉS du fabricant, jamais recopiés :
  deux écritures d'une même chose divergent toujours.
⑨ CE QUI CLOCHE — L'examen joué ici est celui du fabricant de CETTE version ; le relais en service au dépôt public
  peut être plus ancien et juger autrement (une clé « version » qu'il ne connaît pas encore). La file d'attente est
  celle de GitHub (« queue: max », A-896), pas d'ici. Le pre-push du clone public (posé par le fabricant) refuse une
  poussée vers une autre branche que la branche courante du clone, ou d'un commit qui n'est pas HEAD : avec --pousser,
  ce programme pousse un commit fabriqué hors de HEAD, donc refusé sur un clone qui porte ce garde (mesuré par le
  relecteur le 18-11-2026, T5) ; le refus s'affiche désormais en entier, code 2 ; le remède (crochet élargi par
  propriété, ou clone dédié sans crochet) est une décision de Jean-Luc, non prise. Le nom porte la minute :
  deux dépôts dans la même minute sur la même branche font attendre le second jusqu'à la minute suivante.
⑩ EFFET — Écrit des objets git dans le clone public (blob, arbre, commit), met à jour ses références
  refs/remotes/origin/<branche>, et, avec --pousser, pousse la branche publique. Ne touche ni l'index ni la copie de
  travail du clone.
⑪ TERMINAISON — Sort par sys.exit ; chaque commande git est bornée à DELAI_DE_GIT_EN_SECONDES (120 s par défaut) ; l'attente d'une minute libre est
  bornée à 61 secondes, deux fois au plus.
  [sort: oui]
"""
import datetime
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import time
import zoneinfo

ICI = os.path.dirname(os.path.abspath(__file__))
PARIS = zoneinfo.ZoneInfo("Europe/Paris")
CLES_A_POINTE = ("series", "epreuve")     # les circuits qui reçoivent la pointe de la version (A-811)
ESSAIS_DE_POUSSEE = 3
# LE DÉLAI D'UNE COMMANDE GIT, en secondes : 120 par défaut ; la variable d'environnement
# DEPOSER_DELAI_DE_GIT_EN_SECONDES le change (épreuve D13 : un crochet lent, délai réduit, pour éprouver le dépassement
# sans attendre deux minutes). Lue et vérifiée par `main` (un entier de 1 à 600, sinon rien de conclu, code 2).
DELAI_DE_GIT_EN_SECONDES = 120


def charger_le_fabricant():
    """Charge programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py de la même version que ce programme.

    ① RÔLE — Donner accès aux motifs et à l'examen du relais, sans les recopier (R-708).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Le fabricant est à côté de ce programme ; sa table des séries est lisible.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, depuis le dossier de ce programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — Le fabricant lit la table des séries à l'import ; une table illisible laisse
      EXAMEN_D_UNE_DEMANDE vide de séries : `main` refuse alors (ERREUR_DE_LA_TABLE).
    ⑩ EFFET — Exécute le code de tête du fabricant (lecture de la table).
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("FABRIQUER_LE_CIRCUIT_PUBLIC",
                                                  os.path.join(ICI, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(depot, *args, entree=None, env=None):
    """Lance git dans `depot` ; rend (code, sortie standard, sortie d'erreur).

    ① RÔLE — Un appel git borné.
    ② CONTEXTE D'APPEL — Partout.
    ③ ENTRÉE — `depot` : un dossier ; `args` : les arguments de git ; `entree` : octets envoyés sur l'entrée ;
      `env` : variables ajoutées à l'environnement.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le code, la sortie (texte, sans blancs autour), l'erreur (texte).
      [rend: 3]
    ⑥ TRAITEMENT — subprocess.run, DELAI_DE_GIT_EN_SECONDES au plus (120 s par défaut).
    ⑦ UNITÉ — secondes (le délai).
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : `main` le rend en code 2 à CHAQUE appel, poussée et fetch
      d'après un refus compris (C4 du RELU du 25-11-2026 : ces deux appels étaient hors du `try`, et un dépassement
      sortait en code 1, « refusée, rien n'est poussé », alors que la poussée a pu aboutir). Après un dépassement, git
      est tué, mais un crochet lancé par lui peut garder ses sorties ouvertes : l'attente dure alors jusqu'à la fin du
      crochet.
    ⑩ EFFET — Ce que fait la commande.
    ⑪ TERMINAISON — Rend la main ; DELAI_DE_GIT_EN_SECONDES au plus, sauf le cas du crochet ci-dessus.
      [sort: non]
    """
    p = subprocess.run(["git", "-C", depot] + list(args), input=entree, capture_output=True, timeout=DELAI_DE_GIT_EN_SECONDES,
                       env=dict(os.environ, **(env or {})))
    return p.returncode, p.stdout.decode("utf-8", "replace").strip(), p.stderr.decode("utf-8", "replace").strip()


def lire_la_ligne_de_commande(argv, F):
    """Lit la ligne de commande ; rend (clone, branche, réglages, adresse du privé, pousser) ou lève ValueError.

    ① RÔLE — Refuser tôt, avec une raison, ce que l'examen du relais refuserait de toute façon, et ce qu'il ne voit pas
      (une pointe donnée à la main).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `argv` : les arguments (sans le nom du programme) ; `F` : le fabricant.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — CINQ valeurs : le chemin du clone public ; la branche ; la liste ordonnée [(cle, valeur)] ; l'adresse
      du dépôt privé ; vrai si --pousser.
      [rend: 5]
    ⑥ TRAITEMENT — deux positionnels ; « --prive= » et « --pousser » ; chaque autre argument « cle=valeur », clé en
      minuscules et soulignés, chaque clé une fois ; « circuit » obligatoire et connu de CIRCUITS_DU_RELAIS ;
      « pointe » et « version » refusées (le programme les écrit) ; branche par MOTIF_DE_VERSION.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ③ et ④.
    ⑨ CE QUI CLOCHE — Les autres valeurs ne sont jugées que par l'examen du relais (`examiner`) : c'est voulu (R-708).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    positionnels, reglages, prive, pousser = [], [], "https://github.com/" + F.DEPOT_PRIVE + ".git", False
    for a in argv:
        if a == "--pousser":
            pousser = True
        elif a.startswith("--prive="):
            prive = a.split("=", 1)[1]
        elif a.startswith("--"):
            raise ValueError(f"option inconnue : {a}")
        elif "=" in a and len(positionnels) == 2:
            cle, valeur = a.split("=", 1)
            if not re.fullmatch(r"[a-z_]{1,20}", cle):
                raise ValueError(f"clé illisible : {cle!r}")
            if cle in (c for c, _ in reglages):
                raise ValueError(f"clé donnée deux fois : {cle}")
            reglages.append((cle, valeur))
        else:
            positionnels.append(a)
    if len(positionnels) != 2:
        raise ValueError("attendu : <clone public> <branche> cle=valeur… [--prive=<adresse>] [--pousser]")
    clone, branche = positionnels
    if not re.search(F.MOTIF_DE_VERSION, branche):
        raise ValueError("branche hors de la forme permise (main, ou une version en attente travail-...)")
    cles = dict(reglages)
    if "pointe" in cles:
        raise ValueError("la pointe n'est pas donnée à la main : elle est lue au dépôt privé, sur la branche visée")
    if "version" in cles:
        raise ValueError("la version n'est pas donnée à la main : c'est la branche visée")
    if cles.get("circuit") not in [c[0] for c in F.CIRCUITS_DU_RELAIS]:
        raise ValueError("circuit absent ou inconnu (" + ", ".join(c[0] for c in F.CIRCUITS_DU_RELAIS) + ")")
    return clone, branche, reglages, prive, pousser


def lire_la_pointe_privee(prive, branche, F):
    """Rend le commit complet de `branche` au dépôt privé, lu par git ls-remote, ou lève ValueError.

    ① RÔLE — Donner à la demande la pointe exacte de la version visée, juste avant le dépôt (A-811).
    ② CONTEXTE D'APPEL — `main`, pour les circuits de CLES_A_POINTE.
    ③ ENTRÉE — `prive` : l'adresse (ou le chemin) du dépôt privé ; `branche` ; `F` : le fabricant.
    ④ CONDITIONS D'ENTRÉE — La machine peut lire le dépôt privé.
    ⑤ SORTIE — UNE valeur : 40 caractères hexadécimaux, validés par MOTIF_DE_POINTE.
      [rend: 1]
    ⑥ TRAITEMENT — git ls-remote <prive> refs/heads/<branche> ; exactement une ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une pointe recopiée à la main peut être périmée ou abrégée (A-895 ⑳).
    ⑨ CE QUI CLOCHE — La version peut encore avancer entre ce moment et le départ de la série : « preparer » du
      circuit le dit alors (panne P4), et la demande est à redéposer.
    ⑩ EFFET — Lit le réseau.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    p = subprocess.run(["git", "ls-remote", prive, "refs/heads/" + branche], capture_output=True, timeout=120)
    lignes = [l for l in p.stdout.decode("utf-8", "replace").split("\n") if l.strip()]
    if p.returncode != 0 or len(lignes) != 1:
        raise ValueError(f"pointe de {branche} illisible au dépôt privé (code {p.returncode}, {len(lignes)} ligne(s))")
    pointe = lignes[0].split()[0]
    if not re.search(F.MOTIF_DE_POINTE, pointe):
        raise ValueError("pointe lue au dépôt privé hors de la forme d'un commit complet")
    return pointe


def fabriquer_le_commit(clone, tip, nom, contenu, message):
    """Fabrique, sans toucher l'index ni la copie de travail, le commit qui ajoute `nom` à `tip` ; rend son identifiant.

    ① RÔLE — Le commit de la demande, seul, dont le parent est la pointe publique (forme exigée par le relais).
    ② CONTEXTE D'APPEL — `main`, à chaque essai.
    ③ ENTRÉE — `clone` ; `tip` : le commit parent ; `nom` : demandes/DEMANDE_….txt ; `contenu` : octets ; `message`.
    ④ CONDITIONS D'ENTRÉE — `tip` est dans le clone ; l'identité git de la machine est réglée.
    ⑤ SORTIE — UNE valeur : le commit (40 caractères hexadécimaux). Lève RuntimeError si git échoue.
      [rend: 1]
    ⑥ TRAITEMENT — git hash-object -w ; un index temporaire lu depuis `tip`, l'entrée ajoutée, write-tree ;
      commit-tree -p tip.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le clone sert à d'autres travaux : son index et sa copie de travail ne sont pas les nôtres.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit des objets dans le clone ; l'index temporaire est effacé.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    with tempfile.TemporaryDirectory(prefix="demande_index_") as d:
        env = {"GIT_INDEX_FILE": os.path.join(d, "index")}
        code, blob, err = git(clone, "hash-object", "-w", "--stdin", entree=contenu)
        if code != 0:
            raise RuntimeError(f"hash-object : {err}")
        for args in (("read-tree", tip), ("update-index", "--add", "--cacheinfo", "100644," + blob + "," + nom)):
            code, _, err = git(clone, *args, env=env)
            if code != 0:
                raise RuntimeError(f"{args[0]} : {err}")
        code, arbre, err = git(clone, "write-tree", env=env)
        if code != 0:
            raise RuntimeError(f"write-tree : {err}")
        code, commit, err = git(clone, "commit-tree", arbre, "-p", tip, "-m", message)
        if code != 0:
            raise RuntimeError(f"commit-tree : {err}")
    return commit


def examiner(clone, tip, commit, branche, F):
    """Joue sur le commit l'examen même du relais (EXAMEN_D_UNE_DEMANDE) ; rend (accepté, compte rendu).

    ① RÔLE — Refuser ici ce que le relais refuserait sur GitHub, par le même texte.
    ② CONTEXTE D'APPEL — `main`, à chaque essai, avant toute poussée.
    ③ ENTRÉE — `clone` ; `tip` : la pointe d'avant ; `commit` : le commit de la demande ; `branche` ; `F` : le fabricant.
    ④ CONDITIONS D'ENTRÉE — bash installé ; les deux commits sont dans le clone.
    ⑤ SORTIE — DEUX valeurs : vrai si l'examen accepte ; sa sortie (le résumé ou le refus « DEMANDE REFUSEE : … »).
      [rend: 2]
    ⑥ TRAITEMENT — le texte de la fonction bash « examiner » du relais, sans son indentation, puis son appel en
      sous-shell sur (tip, commit, branche), dans un dossier jetable ; bash -e -o pipefail, comme « shell: bash ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 (une seule écriture de l'examen).
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨ (le relais en service peut être d'une autre version).
    ⑩ EFFET — Écrit dans un dossier jetable, effacé ensuite.
    ⑪ TERMINAISON — Rend la main ; DELAI_DE_GIT_EN_SECONDES au plus (120 s par défaut : l'examen n'est qu'une suite
      de commandes git) ; un dépassement lève TimeoutExpired, que `main` rend en code 2 (superviseur R-759 du
      25-11-2026, point 6 : l'appel était hors du `try`, et un dépassement sortait en code 1, « demande refusée »).
      [sort: non]
    """
    script = ("set -u -o pipefail\nexport LC_ALL=C\n" + textwrap.dedent(F.EXAMEN_D_UNE_DEMANDE)
              + '( examiner "$1" "$2" "$3" "$4" )\n')
    with tempfile.TemporaryDirectory(prefix="demande_examen_") as d:
        p = subprocess.run(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script, "examen",
                            tip, commit, branche, os.path.join(d, "s")], cwd=clone, capture_output=True,
                           timeout=DELAI_DE_GIT_EN_SECONDES,
                           env=dict(os.environ, LC_ALL="C"))
    sortie = (p.stdout + p.stderr).decode("utf-8", "replace").strip()
    return p.returncode == 0, sortie


def nom_libre(clone, tip, maintenant=None):
    """Rend (nom du fichier, heure) d'une demande à l'heure de Paris, à la minute, absent de `tip`.

    ① RÔLE — Fabriquer le nom strict (NOM_DE_DEMANDE) sans collision avec une demande de la même minute.
    ② CONTEXTE D'APPEL — `main`, à chaque essai.
    ③ ENTRÉE — `clone` ; `tip` : la pointe publique ; `maintenant` : une heure imposée (épreuves), sinon l'horloge.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : « demandes/DEMANDE_AAAA-MM-JJ_HHhMM.txt » et « AAAA-MM-JJ_HHhMM ». Lève RuntimeError si
      deux minutes de suite sont prises.
      [rend: 2]
    ⑥ TRAITEMENT — heure de Paris ; si le fichier existe dans `tip`, attente de la minute suivante (61 s au plus), deux
      fois au plus.
    ⑦ UNITÉ — minutes (le nom), secondes (l'attente).
    ⑧ POURQUOI — Le relais distingue les demandes par leur nom et leur branche.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Peut dormir jusqu'à 2 × 61 s.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    for _ in range(3):
        t = maintenant or datetime.datetime.now(PARIS)
        heure = t.strftime("%Y-%m-%d_%Hh%M")
        nom = f"demandes/DEMANDE_{heure}.txt"
        if git(clone, "cat-file", "-e", f"{tip}:{nom}")[0] != 0:
            return nom, heure
        if maintenant:
            break
        time.sleep(61 - t.second)
    raise RuntimeError(f"une demande de cette minute existe déjà sur la branche : {nom}")


def masque_ou_rien(F, texte):
    """Rend `texte` masqué par LA fonction du dépôt, ou une phrase qui dit qu'il ne peut pas l'être.

    ① RÔLE — Afficher un message d'erreur de git (un fetch) sans accès en clair.
    ② CONTEXTE D'APPEL — `main`, sur l'erreur d'un fetch (avant la poussée, et après un refus).
    ③ ENTRÉE — `F` : le fabricant (il charge programmes/FORME_D_UN_JETON.py) ; `texte` : le message (str).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte masqué, ou « (message non affiché : masque des accès illisible) ».
      [rend: 1]
    ⑥ TRAITEMENT — F.forme_d_un_jeton().masquer_les_acces(texte) ; toute exception → la phrase de remplacement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — E3 du RELU du 25-11-2026 : l'erreur du fetch s'affichait sans masque. git 2.43 anonymise lui-même
      l'adresse de « origin » (mesuré par le relecteur) ; un texte venu du serveur (« remote: … ») ne l'est pas. Le
      refus de la POUSSÉE garde son propre chemin dans `main` (code 2 si le masque est illisible, épreuve D11).
    ⑨ CE QUI CLOCHE — Les limites de masquer_les_acces (sa fiche).
    ⑩ EFFET — Charge le module du masque.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        return F.forme_d_un_jeton().masquer_les_acces(texte)
    except Exception:   # noqa: BLE001 — sans masque, rien n'est affiché
        return "(message non affiché : masque des accès illisible)"


def main(argv):
    """Le programme entier (fiche en tête).

    ① RÔLE — Fiche en tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (fiche en tête).
      [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Fiche en tête.
    ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    global DELAI_DE_GIT_EN_SECONDES
    delai = os.environ.get("DEPOSER_DELAI_DE_GIT_EN_SECONDES", str(DELAI_DE_GIT_EN_SECONDES))
    if not (delai.isdigit() and 1 <= int(delai) <= 600):
        print(f"RIEN DE CONCLU : DEPOSER_DELAI_DE_GIT_EN_SECONDES n'est pas un entier de 1 à 600 : {delai[:20]!r}")
        return 2
    DELAI_DE_GIT_EN_SECONDES = int(delai)
    try:
        F = charger_le_fabricant()
    except Exception as e:   # noqa: BLE001 — un fabricant illisible ne conclut rien
        print(f"RIEN DE CONCLU : fabricant illisible : {type(e).__name__} : {e}")
        return 2
    if F.ERREUR_DE_LA_TABLE:
        print(f"RIEN DE CONCLU : table des séries illisible : {F.ERREUR_DE_LA_TABLE}")
        return 2
    try:
        clone, branche, reglages, prive, pousser = lire_la_ligne_de_commande(argv, F)
    except ValueError as e:
        print(f"DEMANDE REFUSEE : {e}")
        return 1
    circuit = dict(reglages)["circuit"]
    try:
        pointe = lire_la_pointe_privee(prive, branche, F) if circuit in CLES_A_POINTE else ""
    except (ValueError, subprocess.TimeoutExpired) as e:
        print(f"RIEN DE CONCLU : {e}")
        return 2
    lignes = [f"circuit={circuit}", f"version={branche}"] + ([f"pointe={pointe}"] if pointe else []) + \
        [f"{c}={v}" for c, v in reglages if c != "circuit"]
    contenu = ("\n".join(lignes) + "\n").encode("ascii", "replace")
    for essai in range(1, ESSAIS_DE_POUSSEE + 1):
        try:
            code, _, err = git(clone, "fetch", "-q", "origin", f"+refs/heads/{branche}:refs/remotes/origin/{branche}")
            if code != 0:
                print(f"RIEN DE CONCLU : branche publique {branche} illisible : {masque_ou_rien(F, err)[-200:]}")
                return 2
            tip = git(clone, "rev-parse", f"refs/remotes/origin/{branche}")[1]
            nom, heure = nom_libre(clone, tip)
            ident = f"DEMANDE_{heure}@{branche}"
            commit = fabriquer_le_commit(clone, tip, nom, contenu, f"Demande du {heure} sur {branche} : " + " ".join(lignes))
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"RIEN DE CONCLU : {e}")
            return 2
        try:
            accepte, compte_rendu = examiner(clone, tip, commit, branche, F)
        except subprocess.TimeoutExpired:   # examen sans réponse : rien n'est jugé, rien n'est poussé
            print(f"RIEN DE CONCLU : examen sans réponse après {DELAI_DE_GIT_EN_SECONDES} s : rien n'est poussé ({ident})")
            return 2
        print(compte_rendu)
        if not accepte:
            print(f"REFUSEE PAR L'EXAMEN DU RELAIS : rien n'est poussé ({ident})")
            return 1
        if not pousser:
            print(f"EXAMINEE, NON POUSSEE (sans --pousser) : {ident}")
            return 0
        try:
            code, _, err = git(clone, "push", "-q", "origin", f"{commit}:refs/heads/{branche}")
        except subprocess.TimeoutExpired:   # poussée sans réponse (C4)
            print(f"RIEN DE CONCLU : poussée sans réponse après {DELAI_DE_GIT_EN_SECONDES} s : elle a PU aboutir ; lire "
                  f"la branche publique {branche} avant de redéposer ({ident})")
            return 2
        if code == 0:
            print(f"DEPOSEE : {ident}")
            return 0
        # le refus en entier, masqué par LA fonction du dépôt (programmes/FORME_D_UN_JETON.py, masquer_les_acces,
        # chargé par le fabricant ; R-708 : les motifs de jeton vivent là seulement) ; un module illisible ne laisse
        # rien passer en clair : rien de conclu, refus non affiché
        try:
            masque = F.forme_d_un_jeton().masquer_les_acces(err)
        except Exception as e:   # noqa: BLE001 — sans masque, afficher le refus pourrait montrer un accès
            print(f"RIEN DE CONCLU : poussée refusée, et masque des accès illisible ({type(e).__name__}) : refus non "
                  f"affiché ({ident})")
            return 2
        print(f"poussée refusée (essai {essai} sur {ESSAIS_DE_POUSSEE}), refus complet :\n{masque}")
        # T5 : retenter n'a de sens que si la branche a avancé (une course perdue) ; sinon le même refus reviendrait
        try:
            code_f, _, err_f = git(clone, "fetch", "-q", "origin", f"+refs/heads/{branche}:refs/remotes/origin/{branche}")
        except subprocess.TimeoutExpired:   # branche sans réponse après le refus (C4)
            code_f, err_f = None, f"sans réponse après {DELAI_DE_GIT_EN_SECONDES} s"
        if code_f != 0:   # N3 : sans la pointe d'après le refus, rien ne dit si c'est une course
            print(f"RIEN DE CONCLU : poussée refusée, puis branche publique {branche} illisible "
                  f"({masque_ou_rien(F, err_f)[-200:]}) : rien ne dit si c'est une course, rien n'est retenté ({ident})")
            return 2
        if code_f == 0 and git(clone, "rev-parse", f"refs/remotes/origin/{branche}")[1] == tip:
            print(f"RIEN DE CONCLU : poussée refusée alors que la branche {branche} n'a pas avancé : ce n'est pas une "
                  f"course, rien n'est retenté ({ident})")
            return 2
    print("RIEN DE CONCLU : poussée refusée trois fois")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
