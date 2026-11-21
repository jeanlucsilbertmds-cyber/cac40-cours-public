#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETAT_DES_TRAVAUX.py — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. « Ce programme dit, pour chaque version en attente (branche travail-*), où elle en est et ce qu'il
faut faire ensuite, en ne lisant que des PREUVES (git et GitHub) ; il sert à ce que le pilotage ne se fasse plus de
mémoire. » Demande de Jean-Luc du 20-11-2026 entre 19h42 et 22h00 : « tout doit être sous forme de programme et
tourner, optimisé » ; « il y a des machines entières qui ne travaillent pas alors qu'il y a un énorme boulot à faire ».
Conception : etudes/ORDONNANCEUR_CONCEPTION_Ven_20-11-2026.md (branche travail-ordonnanceur), § 4 « chaque statut est
tiré d'une preuve extérieure » et livraison L1 « l'observateur, qui ne lance rien ». Ce programme est cet observateur,
réduit aux branches : il ne lance rien et n'écrit rien au dépôt.

① RÔLE — Ranger chaque branche travail-* du dépôt privé dans UN état, et dire sa PROCHAINE ACTION :
  ÉCRITURE · À ÉPROUVER · EN ÉPREUVE · ÉPREUVE ROUGE · À RELIRE · DÉPLOYABLE · INSTALLÉE.
② CONTEXTE D'APPEL — À la main par le Chat, ou par programmes/ALARME_DES_MACHINES_OISIVES.py qui l'importe :
  python3 -B programmes/ETAT_DES_TRAVAUX.py [--depot=CHEMIN] [--gh=PROGRAMME] [--public=PROPRIETAIRE/NOM]
                                           [--sans-fetch] [--json] [--tout]
③ ENTRÉE — Un clone git du dépôt privé (par défaut le dossier parent de programmes/) et le programme gh. Lus :
  les branches origin/travail-* ; sur chacune echanges/A_RELIRE.md (date, codes « ## À JOUER SUR GITHUB ») et
  echanges/RELU.md (date, ligne « ## VERDICT : … ») ; les branches de résultats origin/*/<passage>/<CODE> et leur
  RESULTAT.json ; dans origin/main, le dernier journal du circuit public où le fabricant a IMPRIMÉ la largeur qu'il a
  calculée (largeur et fiches des circuits longs — LUES, jamais recopiées, R-708) ; les passages GitHub du dépôt
  public par « gh run list » (titres « places p+n »), « gh workflow list » et « gh run view ».
④ CONDITIONS D'ENTRÉE — git et gh lancés sans invite ; gh authentifié pour le dépôt public.
⑤ SORTIE — Un tableau lisible, ou du JSON avec --json. Code de sortie : 0 l'état est rendu · 2 IMPOSSIBLE, une source
  n'a pas pu être lue (git ou gh) et RIEN n'est rangé (R-734) · 5 PLANTAGE (exception imprévue, jamais un verdict).
⑥ TRAITEMENT — fetch (sauf --sans-fetch) · lire la largeur publiée · relever les résultats d'épreuves longues et la pointe
  jouée de chacun · relever les passages GitHub vivants · pour chaque branche : relever les faits, puis `ranger`.
⑦ UNITÉ — Heures de Paris à l'affichage ; secondes depuis l'époque Unix dans le JSON ; des fils (machines GitHub).
⑧ POURQUOI — Le 20-11-2026, trois faits : Cowork a rejoué des épreuves que GitHub jouait au même moment ; des étapes
  étaient « en cours » sans travail réel ; le Chat ne voit l'état qu'à ses réveils. Un état tiré des preuves, recalculé
  à chaque appel, ne dépend d'aucune mémoire.
⑨ CE QUI CLOCHE — (a) Un verdict autre que « DÉPLOYABLE » tout court (par exemple « DÉPLOYABLE APRÈS CORRECTIONS »)
  renvoie la branche en ÉCRITURE : règle la plus stricte, choisie ici, non décidée par Jean-Luc. (b) Une branche née de
  main sans aucun commit, ou qui n'ajoute que la note, le RELU et archives/, est rangée INSTALLÉE. (c) Un passage vivant est rattaché à une
  branche par son nom (headBranch), pas par sa pointe. (d) Épreuves, relecture et installation valent tant que le
  CODE est le même (`meme_code` : la différence ne touche que echanges/ et archives/) ; la relecture est rattachée à
  la « pointe relue » écrite dans l'en-tête du RELU. (e) Le registre etudes/REGISTRE_DES_TRAVAUX/ de travail-livrer-2 est
  un JOURNAL DE LANCEMENTS (étape, branche, exécutant, identifiant, lancé, fini, résultat) : il ne range pas une
  branche, il n'est donc pas lu ici. (f) Le dépôt public est nommé par défaut ici : le fabricant ne l'écrit pas en
  constante.
⑩ EFFET — Lit git et GitHub ; « git fetch » met à jour les références distantes du clone. N'écrit aucun fichier.
⑪ TERMINAISON — Sort du programme par sys.exit ; chaque appel à git ou gh est borné (DELAI_S secondes).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
DELAI_S = 120
PUBLIC_PAR_DEFAUT = "jeanlucsilbertmds-cyber/cac40-cours-public"
JOURNAUX = "rapports/journal_du_circuit/"
# La ligne que le fabricant IMPRIME pour chaque fiche publiée (« largeur : <fiche> : famille … · groupe … · largeur N »),
# relevée au journal du 21-11-2026 (passage 44846586835).
MOTIF_LARGEUR = re.compile(r"(?m)^largeur : (\S+\.ya?ml) : famille (.+?) · groupe (.+?) · largeur (\d+)\s*$")
# Le titre qu'un passage des circuits longs porte depuis l'étape FILE-2 : « … places <première>+<nombre> ».
MOTIF_PLACES = re.compile(r"places (\d+)\+(\d+)")
JOURNAUX_LUS_AU_PLUS = 50
NOTE, RELU = "echanges/A_RELIRE.md", "echanges/RELU.md"
ETATS = ("ÉCRITURE", "À ÉPROUVER", "EN ÉPREUVE", "ÉPREUVE ROUGE", "À RELIRE", "DÉPLOYABLE", "INSTALLÉE")
RENDU, IMPOSSIBLE, PLANTAGE = 0, 2, 5
MOTIF_POINTE_DU_JOURNAL = re.compile(r"source de la publication : le commit ([0-9a-f]{7,40}) du dépôt privé")
MOTIF_VERDICT = re.compile(r"^\s*(#{1,6}\s*)?(\d+\s*·\s*)?\**VERDICT( EN UNE LIGNE)?\**\s*(:|$)")
MOTIF_POINTE_RELUE = re.compile(r"(?i)pointe relue\W{0,12}([0-9a-f]{7,40})")
# HORS DU CODE : ce que le relecteur et l'auteur écrivent sans changer le programme éprouvé (la note, le RELU, les
# archives). Une différence limitée à ces dossiers ne rend caduques ni les épreuves, ni la relecture, ni l'installation.
HORS_CODE = ("echanges/", "archives/")
TABLE_DES_EPREUVES = "tests/LANCEMENT_DES_EPREUVES.json"


class Impossible(Exception):
    """Une source n'a pas pu être lue.

    ① RÔLE — Porter jusqu'à `main` le fait qu'une source (git, gh, le fabricant) est illisible.
    ② CONTEXTE D'APPEL — Levée par `commande` et par les lecteurs ; attrapée par `main` et par l'alarme.
    ③ ENTRÉE — Le message, en français.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul, jamais un état partiel.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """


def commande(arguments, dossier=None, tolere=False):
    """Lance une commande et rend sa sortie.

    ① RÔLE — Le seul endroit où ce programme lance git ou gh.
    ② CONTEXTE D'APPEL — Tous les lecteurs de ce programme.
    ③ ENTRÉE — `arguments` : la liste des mots de la commande · `dossier` : le dossier courant, ou None ·
      `tolere` : vrai si un code non nul est une réponse attendue (par exemple « merge-base --is-ancestor »).
    ④ CONDITIONS D'ENTRÉE — Le premier mot est un programme trouvable.
    ⑤ SORTIE — UNE valeur : le couple n'est pas rendu ; avec `tolere`, le code de sortie (entier) ; sinon le texte
      de la sortie standard.
      [rend: 1]
    ⑥ TRAITEMENT — Lancer avec un délai de DELAI_S secondes ; lever Impossible si le programme manque, si le délai
      passe, ou si le code est non nul sans `tolere`.
    ⑦ UNITÉ — Secondes pour le délai.
    ⑧ POURQUOI — Un appel qui échoue en silence rendrait un état faux (R-734).
    ⑨ CE QUI CLOCHE — La sortie d'erreur n'est montrée que tronquée.
    ⑩ EFFET — Lance un processus.
    ⑪ TERMINAISON — Rend la main ou lève ; l'appel est borné par le délai.
      [sort: non]
    """
    try:
        r = subprocess.run(arguments, cwd=dossier, capture_output=True, text=True, errors="replace",
                           timeout=DELAI_S)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Impossible(f"{arguments[0]} {arguments[1] if len(arguments) > 1 else ''} : {type(e).__name__}")
    if tolere:
        return r.returncode
    if r.returncode != 0:
        raise Impossible(f"« {' '.join(arguments[:4])} … » rend {r.returncode} : {r.stderr.strip()[:200]}")
    return r.stdout


def git(depot, *arguments):
    """Lance git dans le dépôt.

    ① RÔLE — Raccourci de `commande` pour git.
    ② CONTEXTE D'APPEL — Les lecteurs de git de ce programme.
    ③ ENTRÉE — `depot` : le clone · `arguments` : les mots après « git ».
    ④ CONDITIONS D'ENTRÉE — `depot` est un clone git.
    ⑤ SORTIE — UNE valeur : le texte de la sortie.
      [rend: 1]
    ⑥ TRAITEMENT — Appeler `commande` avec « git -C depot ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un seul chemin vers git.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    return commande(["git", "-C", depot] + list(arguments))


def heure_paris(secondes):
    """Écrit une date en heure de Paris.

    ① RÔLE — Afficher une date lisible.
    ② CONTEXTE D'APPEL — L'affichage du tableau.
    ③ ENTRÉE — `secondes` : secondes depuis l'époque Unix, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « JJ-MM HHhMM », ou « — ».
      [rend: 1]
    ⑥ TRAITEMENT — Conversion par zoneinfo Europe/Paris.
    ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Les instructions du projet datent tout en heure de Paris.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if secondes is None:
        return "—"
    return datetime.fromtimestamp(secondes, PARIS).strftime("%d-%m %Hh%M")


def largeur_publiee(depot):
    """Lit la largeur des circuits longs que le fabricant a CALCULÉE et IMPRIMÉE à sa dernière publication.

    ① RÔLE — Donner la largeur des circuits longs, leur groupe et le nom de leurs fiches, sans recopier un chiffre ni
      dépendre d'un nom de constante du fabricant.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois.
    ③ ENTRÉE — `depot` : le clone.
    ④ CONDITIONS D'ENTRÉE — origin/main porte des journaux du circuit public (rapports/journal_du_circuit/) dont l'un
      au moins contient les lignes « largeur : … » imprimées par le fabricant.
    ⑤ SORTIE — UNE valeur : un dict {largeur, groupe, fiches_longues, journal}.
      [rend: 1]
    ⑥ TRAITEMENT — Remonter les commits de origin/main qui touchent les journaux (au plus JOURNAUX_LUS_AU_PLUS) ; dans
      le premier qui porte des lignes MOTIF_LARGEUR, regrouper les fiches par groupe ; les circuits longs sont LE
      groupe que PLUSIEURS fiches partagent (propriété : ils se partagent les places) ; sa largeur est celle que le
      fabricant a imprimée. Aucun groupe partagé, ou plusieurs, ou des largeurs différentes dans le groupe : Impossible.
    ⑦ UNITÉ — Des fils (jobs GitHub simultanés).
    ⑧ POURQUOI — R-708. Le 21-11-2026 à 01h41, l'installation de travail-file-2 a supprimé GROUPE_DES_MACHINES_LONGUES
      et fait de PARTS_EN_MEME_TEMPS une expression : la lecture par noms de constantes du tour 2 a rendu « fabricant
      illisible » (passage 44845541079). Ce que le fabricant imprime survit à un renommage interne.
    ⑨ CE QUI CLOCHE — La largeur est celle de la DERNIÈRE PUBLICATION journalisée, pas celle du code de main tant
      qu'aucun passage n'a publié. Un changement du texte de la ligne imprimée rend Impossible (voulu, R-734).
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    commits = git(depot, "log", f"-{JOURNAUX_LUS_AU_PLUS}", "--format=%H", "origin/main", "--", JOURNAUX).split()
    for c in commits:
        lignes = []
        for f in git(depot, "show", "--name-only", "--format=", c).splitlines():
            if f.startswith(JOURNAUX) and f.endswith(".log"):
                lignes += MOTIF_LARGEUR.findall(git(depot, "show", f"{c}:{f}"))
        if not lignes:
            continue
        par_groupe = {}
        for fiche, _famille, groupe, largeur in lignes:
            par_groupe.setdefault(groupe, {})[fiche] = int(largeur)
        partages = {g: f for g, f in par_groupe.items() if len(f) >= 2}
        if len(partages) != 1 or len(set(next(iter(partages.values())).values())) != 1:
            raise Impossible(f"journal {c[:9]} : groupes partagés illisibles {sorted(partages)}")
        groupe, fiches = next(iter(partages.items()))
        return {"largeur": next(iter(fiches.values())), "groupe": groupe, "fiches_longues": sorted(fiches),
                "journal": c}
    raise Impossible(f"aucune ligne « largeur : » dans les {len(commits)} derniers journaux de origin/main")


def table_des_codes(depot, ref):
    """Rend les codes d'épreuves longues que la table de la branche connaît.

    ① RÔLE — Donner la liste fermée des codes qu'une note peut demander.
    ② CONTEXTE D'APPEL — `faits_d_une_branche`.
    ③ ENTRÉE — `depot` : le clone · `ref` : la branche.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des clés de « epreuves_longues » de tests/LANCEMENT_DES_EPREUVES.json sur la
      branche ; vide si la table manque ou ne porte pas cette section.
      [rend: 1]
    ⑥ TRAITEMENT — « git cat-file -e » puis « git show », lecture JSON.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un code est ce que la table connaît : une propriété, pas une forme d'écriture (RELU Cowork I1 du
      20-11-2026, 22h25 : « - **File** — … » n'était pas lu).
    ⑨ CE QUI CLOCHE — Une table qui n'est pas du JSON est traitée comme vide : la note sera alors « illisible ».
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    if commande(["git", "-C", depot, "cat-file", "-e", f"{ref}:{TABLE_DES_EPREUVES}"], tolere=True) != 0:
        return set()
    try:
        table = json.loads(git(depot, "show", f"{ref}:{TABLE_DES_EPREUVES}"))
    except ValueError:
        return set()
    longues = table.get("epreuves_longues") if isinstance(table, dict) else None
    return set(longues) if isinstance(longues, dict) else set()


def codes_a_jouer(note, connus):
    """Relève les codes de la section « ## À JOUER SUR GITHUB » d'une note.

    ① RÔLE — Dire quelles épreuves longues la note demande, et quelles lignes de la section ne se lisent pas.
    ② CONTEXTE D'APPEL — `faits_d_une_branche` ; les épreuves.
    ③ ENTRÉE — `note` : le texte de echanges/A_RELIRE.md · `connus` : les codes de la table de la branche.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste des codes, dans l'ordre, sans doublon · la liste des lignes illisibles.
      [rend: 2]
    ⑥ TRAITEMENT — Après la ligne « ## À JOUER SUR GITHUB », jusqu'à la prochaine ligne qui commence par « # » :
      ① une puce (« - … ») : sa TÊTE est le texte avant le premier « — » ; chaque mot de la tête qui est un code
      connu est retenu (gras, accents graves, virgules tolérés) ; une puce sans code connu dans sa tête est illisible ·
      ② une ligne de texte hors puce est un commentaire, SAUF si la section n'a aucune puce : alors toute la section
      est illisible dès qu'elle porte du texte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relevé du 20-11-2026 sur les notes réelles : « - VenteReglable », « - `Certification` »,
      « - **File** — l'épreuve … », « - **ProprietesChaine, ProprietesSabot, …** — à rejouer », et des listes en
      prose séparées par « · » (travail-a952). Un silence ne doit jamais passer pour « rien à jouer ».
    ⑨ CE QUI CLOCHE — Une tête de puce qui cite un code pour dire qu'il ne faut PAS le jouer serait lue comme une
      demande. Une liste en prose n'est pas lue : elle rend la section illisible.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    codes, illisibles, texte, puces, dedans = [], [], [], 0, False
    for ligne in note.splitlines():
        if ligne.strip().startswith("## À JOUER SUR GITHUB"):
            dedans = True
            continue
        if not dedans:
            continue
        if ligne.startswith("#"):
            break
        if not ligne.strip():
            continue
        if ligne.lstrip().startswith("- "):
            puces += 1
            tete = ligne.lstrip()[2:].split(" — ")[0]
            trouves = [m for m in re.findall(r"[A-Za-z][A-Za-z0-9_]*", tete) if m in connus]
            if not trouves:
                illisibles.append(ligne.strip()[:80])
            for c in trouves:
                if c not in codes:
                    codes.append(c)
        else:
            texte.append(ligne.strip()[:80])
    if texte and not puces:
        illisibles += texte
    return codes, illisibles


def verdict_du_relu(relu):
    """Relève le verdict d'un RELU.

    ① RÔLE — Lire la ligne « ## VERDICT : … ».
    ② CONTEXTE D'APPEL — `faits_d_une_branche`.
    ③ ENTRÉE — `relu` : le texte de echanges/RELU.md.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte du verdict, ou "" s'il n'y en a pas.
      [rend: 1]
    ⑥ TRAITEMENT — Première ligne qui OUVRE par « VERDICT » (précédé ou non de « # » et de « ** ») suivi de « : »
      ou de la fin de ligne ; le texte après « : », ou, s'il n'y en a pas, la première ligne non vide qui suit.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relevé du 20-11-2026 sur les RELU des branches travail-* : 10 écrivent « ## VERDICT » seul, le
      verdict à la ligne suivante ; celui de travail-file-2 écrit « VERDICT : À REPRENDRE » sans « ## » ; travail-e3b
      « ## 0 · VERDICT : … » ; travail-e4 et travail-livrer « ## VERDICT EN UNE LIGNE », le verdict dessous.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = relu.splitlines()
    for i, ligne in enumerate(lignes):
        if MOTIF_VERDICT.match(ligne):
            reste = ligne.split(":", 1)[1].strip() if ":" in ligne else ""
            if reste:
                return reste
            suite = [x.strip() for x in lignes[i + 1:] if x.strip()]
            return suite[0] if suite else ""
    return ""


def est_deployable(verdict):
    """Dit si un verdict autorise l'installation.

    ① RÔLE — Trancher DÉPLOYABLE contre tout le reste.
    ② CONTEXTE D'APPEL — `ranger`.
    ③ ENTRÉE — `verdict` : le texte rendu par `verdict_du_relu`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si le verdict est « DÉPLOYABLE » seul, ou suivi seulement de « · CLORE … » ou
      « — CLORE … », ou fermé par un point (« **DÉPLOYABLE.** Le jeu entier… », RELU de travail-a924-f1f3).
      [rend: 1]
    ⑥ TRAITEMENT — Retirer les « * » de tête ; exiger le mot DÉPLOYABLE ; le reste, privé des « * », doit être
      vide, commencer par un point, ou être « · CLORE » / « — CLORE ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « DÉPLOYABLE APRÈS CORRECTIONS » demande des corrections : la règle la plus stricte prime.
    ⑨ CE QUI CLOCHE — « CONFORME — RIEN DE NEUF QUI BLOQUE » n'est pas reconnu déployable.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    v = verdict.lstrip("*").strip()
    if not v.startswith("DÉPLOYABLE"):
        return False
    reste = v[len("DÉPLOYABLE"):]
    if reste.startswith("."):
        return True
    reste = reste.strip("* ")
    return reste == "" or re.match(r"^[·—-]\s*CLORE", reste) is not None


def resultats_github(depot):
    """Relève tous les résultats d'épreuves longues rendus au dépôt privé.

    ① RÔLE — Dire, pour chaque pointe jouée, le code de sortie de chaque épreuve.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois.
    ③ ENTRÉE — `depot` : le clone.
    ④ CONDITIONS D'ENTRÉE — Une branche de résultat est une référence origin/<x>/<passage>/<CODE> (passage en
      chiffres) qui porte rapports/epreuves_longues/<passage>/<CODE>/RESULTAT.json : c'est ce fichier qui la désigne,
      pas le nom <x>.
    ⑤ SORTIE — DEUX valeurs : un dict {pointe complète : {code : {sortie, passage, heure}}} où, pour un même code et
      une même pointe, le résultat le plus récent l'emporte · la liste des branches de résultats (RESULTAT.json
      présent) sans pointe lisible.
      [rend: 2]
    ⑥ TRAITEMENT — Lister les branches ; lire RESULTAT.json ; la pointe jouée vient de son champ « pointe_jouee »
      ou « pointe » s'il existe, sinon de la ligne « source de la publication : le commit … du dépôt privé » du
      journal rapports/journal_du_circuit/circuit_<passage>_*_jouer_<CODE>.log ; l'abréviation se résout en pointe
      complète par git.
    ⑦ UNITÉ — Secondes Unix pour l'heure (celle du commit de la branche de résultat).
    ⑧ POURQUOI — RESULTAT.json du passage 44804954374 ne porte pas la pointe ; son journal la porte (0787558b1e26).
    ⑨ CE QUI CLOCHE — Une pointe abrégée que le clone ne connaît pas est rangée sans pointe.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    refs = git(depot, "for-each-ref", "--format=%(refname:short) %(committerdate:unix)", "refs/remotes/origin/*/*/*")
    par_pointe, sans_pointe = {}, []
    for ligne in refs.splitlines():
        ref, heure = ligne.rsplit(" ", 1)
        morceaux = ref.split("/")
        if len(morceaux) != 4 or not morceaux[2].isdigit():
            continue
        passage, code = morceaux[2], morceaux[3]
        fichiers = git(depot, "ls-tree", "-r", "--name-only", ref).splitlines()
        chemin = f"rapports/epreuves_longues/{passage}/{code}/RESULTAT.json"
        if chemin not in fichiers:
            continue
        try:
            resultat = json.loads(git(depot, "show", f"{ref}:{chemin}"))
        except ValueError:
            sans_pointe.append(ref)
            continue
        pointe = resultat.get("pointe_jouee") or resultat.get("pointe") or ""
        if not pointe:
            for f in fichiers:
                if f.startswith(f"rapports/journal_du_circuit/circuit_{passage}_") and f.endswith(f"_jouer_{code}.log"):
                    m = MOTIF_POINTE_DU_JOURNAL.search(git(depot, "show", f"{ref}:{f}"))
                    if m:
                        pointe = m.group(1)
                        break
        complete = ""
        if pointe and commande(["git", "-C", depot, "cat-file", "-e", pointe + "^{commit}"], tolere=True) == 0:
            complete = git(depot, "rev-parse", pointe + "^{commit}").strip()
        if not complete:
            sans_pointe.append(ref)
            continue
        deja = par_pointe.setdefault(complete, {}).get(code)
        if deja is None or int(heure) >= deja["heure"]:
            par_pointe[complete][code] = {"sortie": resultat.get("code_de_sortie"), "passage": passage,
                                          "heure": int(heure)}
    return par_pointe, sans_pointe


def passages_github(gh, public, fiches_longues):
    """Relève les passages GitHub vivants et les places qu'ils occupent.

    ① RÔLE — Dire ce qui tourne sur GitHub, et combien de places des circuits longs sont prises.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois.
    ③ ENTRÉE — `gh` : le programme gh · `public` : « propriétaire/nom » du dépôt public · `fiches_longues` : les noms
      de fichier des fiches longues, lus au journal du fabricant.
    ④ CONDITIONS D'ENTRÉE — gh authentifié.
    ⑤ SORTIE — DEUX valeurs : la liste des passages vivants (dicts : passage, circuit, branche, statut, places) · le
      nombre de places occupées (« épreuves en cours »).
      [rend: 2]
    ⑥ TRAITEMENT — « gh run list --limit 100 » ; vivant = statut autre que « completed » ; un passage vivant dont le
      titre porte « places p+n » occupe n places (le nouveau relais les a réservées) ; un passage vivant d'une fiche
      longue sans ce titre (circuit d'avant FILE-2, ou lancé à la main) occupe ses jobs non finis
      (« gh run view --json jobs ») ; la fiche d'un passage se lit par « gh workflow list » (nom → chemin).
    ⑦ UNITÉ — Des places (une place = une machine).
    ⑧ POURQUOI — Depuis l'étape FILE-2 (installée le 21-11-2026 à 01h36), le relais choisit les places de chaque
      demande et les écrit dans le titre ; trois passages tournaient ensemble à 01h41 (places 1+3, 4+3, 7+2).
    ⑨ CE QUI CLOCHE — Au-delà de 100 passages récents, un passage vivant plus ancien ne serait pas vu. Un passage en
      file compte ses places comme prises : prudent pour l'alarme (moins de fils libres annoncés).
    ⑩ EFFET — Lance gh.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    try:
        passages = json.loads(commande([gh, "run", "list", "-R", public, "--limit", "100", "--json",
                                        "databaseId,workflowName,status,headBranch,createdAt,displayTitle"]))
        fiches = json.loads(commande([gh, "workflow", "list", "-R", public, "--all", "--json", "name,path"]))
    except ValueError:
        raise Impossible("gh run list ou gh workflow list : réponse qui n'est pas du JSON")
    longs = {f.get("name") for f in fiches if os.path.basename(f.get("path", "")) in fiches_longues}
    vivants, occupees = [], 0
    for p in passages:
        if p.get("status") == "completed":
            continue
        m = MOTIF_PLACES.search(p.get("displayTitle") or "")
        if m:
            places = int(m.group(2))
        elif p.get("workflowName") in longs:
            try:
                vue = json.loads(commande([gh, "run", "view", str(p["databaseId"]), "-R", public, "--json", "jobs"]))
            except ValueError:
                raise Impossible(f"gh run view {p['databaseId']} : réponse qui n'est pas du JSON")
            places = sum(1 for j in vue.get("jobs", []) if j.get("status") != "completed")
        else:
            places = 0
        occupees += places
        vivants.append({"passage": p["databaseId"], "circuit": p.get("workflowName"), "branche": p.get("headBranch"),
                        "statut": p.get("status"), "places": places})
    return vivants, occupees


def meme_code(depot, a, b):
    """Dit si deux commits portent le même code.

    ① RÔLE — La propriété unique qui dit si une épreuve, une relecture ou une installation vaut encore.
    ② CONTEXTE D'APPEL — `faits_d_une_branche`.
    ③ ENTRÉE — `depot` : le clone · `a`, `b` : deux commits.
    ④ CONDITIONS D'ENTRÉE — Les deux commits existent dans le clone.
    ⑤ SORTIE — UNE valeur : vrai si « git diff --name-only a b » ne touche que des chemins sous HORS_CODE.
      [rend: 1]
    ⑥ TRAITEMENT — Un appel à git.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — RELU Cowork du 20-11-2026, 22h25 : B1 (un code changé après le RELU restait DÉPLOYABLE), I2
      (travail-enchainer, dont seuls la note, le RELU et archives/ diffèrent de main, était « à installer »), I3 (une
      note réécrite après l'épreuve la rendait caduque). Une seule propriété répond aux trois.
    ⑨ CE QUI CLOCHE — Un fichier de données ou d'étude hors HORS_CODE compte comme du code.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    if a == b:
        return True
    return all(f.startswith(HORS_CODE) for f in git(depot, "diff", "--name-only", a, b).splitlines() if f.strip())


def pointe_relue(depot, relu):
    """Rend la pointe que le RELU déclare avoir relue.

    ① RÔLE — Rattacher une relecture au code qu'elle a lu.
    ② CONTEXTE D'APPEL — `faits_d_une_branche`.
    ③ ENTRÉE — `depot` : le clone · `relu` : le texte de echanges/RELU.md.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la pointe complète, ou "" si l'en-tête ne la porte pas ou si le clone ne la connaît pas.
      [rend: 1]
    ⑥ TRAITEMENT — Dans les 20 premières lignes, « pointe relue » suivi d'au plus 12 signes puis d'un identifiant
      hexadécimal ; résolu par « git rev-parse --verify ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relevé du 20-11-2026 : 116 RELU de travail-* sur 125 l'écrivent (« pointe relue **d9b84bf6e** »,
      « pointe relue f14bc3e72d33… »). Un RELU qui ne le dit pas ne prouve pas ce qu'il a relu.
    ⑨ CE QUI CLOCHE — Les 9 RELU sans cette mention sont traités comme non rattachés (À RELIRE).
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    m = MOTIF_POINTE_RELUE.search("\n".join(relu.splitlines()[:20]))
    if not m:
        return ""
    if commande(["git", "-C", depot, "cat-file", "-e", m.group(1) + "^{commit}"], tolere=True) != 0:
        return ""
    return git(depot, "rev-parse", m.group(1) + "^{commit}").strip()


def date_du_dernier_commit(depot, base, pointe, chemin):
    """Rend la date du dernier commit de la branche qui touche un fichier.

    ① RÔLE — Dater la note ou le RELU de la branche, et seulement s'ils ont été écrits SUR la branche.
    ② CONTEXTE D'APPEL — `faits_d_une_branche`, deux fois.
    ③ ENTRÉE — `depot` : le clone · `base` : le départ de la branche · `pointe` : sa pointe · `chemin` : le fichier.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : secondes Unix, ou None si aucun commit de base..pointe ne touche le fichier.
      [rend: 1]
    ⑥ TRAITEMENT — « git log -1 --format=%ct base..pointe -- chemin ».
    ⑦ UNITÉ — Secondes Unix.
    ⑧ POURQUOI — Une note héritée de main n'est pas la note de la branche.
    ⑨ CE QUI CLOCHE — La date est celle du commit, pas celle de l'écriture.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    sortie = git(depot, "log", "-1", "--format=%ct", f"{base}..{pointe}", "--", chemin).strip()
    return int(sortie) if sortie else None


def ranger(faits):
    """Range une branche dans UN état et dit sa prochaine action.

    ① RÔLE — Le cœur du programme : des faits à l'état, sans rien lire.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois par branche ; les épreuves l'appellent directement.
    ③ ENTRÉE — `faits` : un dict {installee, note_heure, codes, illisibles, passages_vivants, resultats, relu_heure,
      relu_pointe, relu_meme_code, verdict, pointe}.
    ④ CONDITIONS D'ENTRÉE — `resultats` ne porte que les résultats joués sur un commit de MÊME CODE que la pointe.
    ⑤ SORTIE — DEUX valeurs : l'état (un des ETATS) · la prochaine action, en français.
      [rend: 2]
    ⑥ TRAITEMENT — Dans cet ordre, le premier qui s'applique : même code que main → INSTALLÉE · pas de note écrite
      sur la branche → ÉCRITURE · section « À JOUER » illisible → ÉCRITURE (réécrire la section) · un passage GitHub
      vivant sur la branche → EN ÉPREUVE · un code demandé rendu non nul → ÉPREUVE ROUGE · un code demandé sans
      résultat → À ÉPROUVER · pas de RELU, RELU sans pointe relue, code changé depuis la pointe relue, ou note plus
      récente que le RELU → À RELIRE · verdict DÉPLOYABLE → DÉPLOYABLE · sinon ÉCRITURE (reprendre selon le RELU).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Cet ordre suit la conception (§ 2.4 ②) : la relecture Cowork ne devient prête qu'une fois
      l'épreuve longue du MÊME code verte ; c'est ce qui supprime le doublon du 20-11-2026.
    ⑨ CE QUI CLOCHE — Une note sans section « ## À JOUER SUR GITHUB » passe droit à la relecture.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if faits["installee"]:
        return "INSTALLÉE", "rien — même code que main (branche supprimable sur accord de Jean-Luc)"
    if faits["note_heure"] is None:
        return "ÉCRITURE", "écrire et pousser echanges/A_RELIRE.md sur la branche"
    if faits["illisibles"]:
        return "ÉCRITURE", ("réécrire « ## À JOUER SUR GITHUB » en puces « - Code » : illisible « "
                            + faits["illisibles"][0] + " »")
    if faits["passages_vivants"]:
        return "EN ÉPREUVE", "attendre la fin du passage " + ", ".join(str(p) for p in faits["passages_vivants"])
    resultats = faits["resultats"]
    rouges = [c for c in faits["codes"] if c in resultats and resultats[c]["sortie"] != 0]
    if rouges:
        return "ÉPREUVE ROUGE", ("lire SORTIE.txt et réparer : " + ", ".join(
            f"{c} (code {resultats[c]['sortie']}, passage {resultats[c]['passage']})" for c in rouges))
    manquants = [c for c in faits["codes"] if c not in resultats]
    if manquants:
        return "À ÉPROUVER", (f"déposer la demande d'épreuves longues sur {faits['pointe'][:9]} : "
                              + ", ".join(manquants))
    relire = "lancer la relecture Cowork (épreuves longues à lire sur GitHub, ne pas les rejouer)"
    if faits["relu_heure"] is None:
        return "À RELIRE", relire
    if not faits["relu_pointe"]:
        return "À RELIRE", relire + " — le RELU présent ne nomme pas de pointe relue lisible"
    elif not faits["relu_meme_code"]:
        return "À RELIRE", relire + f" — le code a changé depuis la pointe relue {faits['relu_pointe'][:9]}"
    if faits["relu_heure"] < faits["note_heure"]:
        return "À RELIRE", relire + " — la note est plus récente que le RELU"
    if est_deployable(faits["verdict"]):
        return "DÉPLOYABLE", "installer sur main, quand rien ne tourne sur GitHub (A-818), puis republier"
    return "ÉCRITURE", f"reprendre selon le RELU (verdict : « {faits['verdict'][:70]} »)"


def faits_d_une_branche(depot, branche, resultats, vivants):
    """Relève les faits d'une branche.

    ① RÔLE — Rassembler ce que `ranger` attend, pour une branche.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois par branche.
    ③ ENTRÉE — `depot` : le clone · `branche` : le nom sans « origin/ » · `resultats` : la première valeur de
      `resultats_github` · `vivants` : la première valeur de `passages_github`.
    ④ CONDITIONS D'ENTRÉE — origin/<branche> existe.
    ⑤ SORTIE — UNE valeur : le dict des faits, plus « branche », « pointe », « pointe_heure ».
      [rend: 1]
    ⑥ TRAITEMENT — pointe ; départ = merge-base avec origin/main ; INSTALLÉE si `meme_code(départ, pointe)` (rien
      d'autre n'est lu alors) ; sinon dates de la note et du RELU écrits sur la branche, codes lus contre la table de
      la branche, verdict, pointe relue et `meme_code(pointe relue, pointe)` ; résultats : pour chaque code, le plus
      récent parmi les commits de départ..pointe de même code que la pointe ; passages vivants de même nom.
    ⑦ UNITÉ — Secondes Unix.
    ⑧ POURQUOI — Séparer la lecture (ici) du rangement (`ranger`), pour éprouver le rangement sans git.
    ⑨ CE QUI CLOCHE — Une épreuve jouée sur un commit qui n'est pas dans l'histoire de la branche n'est pas comptée.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    ref = "origin/" + branche
    pointe = git(depot, "rev-parse", ref).strip()
    faits = {"branche": branche, "pointe": pointe, "pointe_heure": int(git(depot, "log", "-1", "--format=%ct", ref)),
             "installee": False, "note_heure": None, "codes": [], "illisibles": [], "passages_vivants": [],
             "resultats": {}, "relu_heure": None, "relu_pointe": "", "relu_meme_code": False, "verdict": ""}
    base = git(depot, "merge-base", pointe, "origin/main").strip()
    faits["installee"] = meme_code(depot, base, pointe)
    if faits["installee"]:
        return faits
    faits["note_heure"] = date_du_dernier_commit(depot, base, pointe, NOTE)
    faits["relu_heure"] = date_du_dernier_commit(depot, base, pointe, RELU)
    if faits["note_heure"] is not None:
        faits["codes"], faits["illisibles"] = codes_a_jouer(git(depot, "show", f"{ref}:{NOTE}"),
                                                            table_des_codes(depot, ref))
    if faits["relu_heure"] is not None:
        relu = git(depot, "show", f"{ref}:{RELU}")
        faits["verdict"] = verdict_du_relu(relu)
        faits["relu_pointe"] = pointe_relue(depot, relu)
        if faits["relu_pointe"]:
            faits["relu_meme_code"] = meme_code(depot, faits["relu_pointe"], pointe)
    histoire = set(git(depot, "rev-list", f"{base}..{pointe}").split())
    for p in sorted(histoire & set(resultats)):
        if not meme_code(depot, p, pointe):
            continue
        for code, r in resultats[p].items():
            if code not in faits["resultats"] or r["heure"] >= faits["resultats"][code]["heure"]:
                faits["resultats"][code] = r
    faits["passages_vivants"] = [v["passage"] for v in vivants if v["branche"] == branche]
    return faits


def etat_des_travaux(depot, gh="gh", public=PUBLIC_PAR_DEFAUT, fetch=True):
    """Rend l'état de toutes les branches travail-*.

    ① RÔLE — Le point d'entrée commun au tableau, au JSON et à l'alarme.
    ② CONTEXTE D'APPEL — `main` ; programmes/ALARME_DES_MACHINES_OISIVES.py.
    ③ ENTRÉE — `depot` : le clone · `gh` : le programme gh · `public` : le dépôt public · `fetch` : faire
      « git fetch origin » d'abord.
    ④ CONDITIONS D'ENTRÉE — Voir le module.
    ⑤ SORTIE — UNE valeur : un dict {heure, largeur_publiee, fils, passages, branches, resultats_sans_pointe}.
      [rend: 1]
    ⑥ TRAITEMENT — fetch · largeur publiée · résultats · passages · faits et rangement de chaque origin/travail-* ·
      fils libres = largeur − places occupées, jamais sous 0.
    ⑦ UNITÉ — Fils ; secondes Unix.
    ⑧ POURQUOI — Voir le module.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — « git fetch » met à jour les références distantes ; lance gh.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    if fetch:
        git(depot, "fetch", "-q", "origin")
    lu = largeur_publiee(depot)
    resultats, sans_pointe = resultats_github(depot)
    vivants, en_cours = passages_github(gh, public, lu["fiches_longues"])
    branches = []
    for ligne in git(depot, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/travail-*").splitlines():
        faits = faits_d_une_branche(depot, ligne[len("origin/"):], resultats, vivants)
        faits["etat"], faits["action"] = ranger(faits)
        branches.append(faits)
    return {"heure": int(time.time()), "largeur_publiee": lu,
            "fils": {"largeur": lu["largeur"], "epreuves_en_cours": en_cours,
                     "libres": max(0, lu["largeur"] - en_cours)},
            "passages": vivants, "branches": branches, "resultats_sans_pointe": len(sans_pointe)}


def tableau(etat, tout=False):
    """Écrit l'état en texte lisible.

    ① RÔLE — L'affichage pour Jean-Luc et le Chat.
    ② CONTEXTE D'APPEL — `main` sans --json.
    ③ ENTRÉE — `etat` : la valeur de `etat_des_travaux` · `tout` : montrer aussi, une par ligne, les branches
      INSTALLÉE (sinon elles sont seulement comptées).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — En-tête (heure, fils, passages vivants) ; une ligne par branche, rangées dans l'ordre des ETATS
      puis par pointe la plus récente ; compte par état.
    ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Une lecture mobile : l'état et l'action d'abord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    f = etat["fils"]
    out = [f"ÉTAT DES TRAVAUX — {heure_paris(etat['heure'])} (Paris)",
           f"fils GitHub des circuits longs : largeur {f['largeur']} (imprimée par le fabricant, journal "
           f"{etat['largeur_publiee']['journal'][:9]}) − places occupées "
           f"{f['epreuves_en_cours']} = {f['libres']} libre(s)"]
    for p in etat["passages"]:
        out.append(f"  tourne : passage {p['passage']} · {p['circuit']} · {p['branche']} · {p['statut']}"
                   f" · {p['places']} place(s)")
    if not etat["passages"]:
        out.append("  rien ne tourne sur GitHub")
    rang = {e: i for i, e in enumerate(ETATS)}
    compte = {e: 0 for e in ETATS}
    for b in sorted(etat["branches"], key=lambda x: (rang[x["etat"]], -x["pointe_heure"])):
        compte[b["etat"]] += 1
        if b["etat"] == "INSTALLÉE" and not tout:
            continue
        out.append(f"- {b['branche']} [{b['pointe'][:9]}, {heure_paris(b['pointe_heure'])}] {b['etat']} → {b['action']}")
    out.append("compte : " + " · ".join(f"{e} {n}" for e, n in compte.items()))
    out.append(f"résultats d'épreuves longues sans pointe lisible : {etat['resultats_sans_pointe']}")
    return "\n".join(out)


def main():
    """Lit la ligne de commande, rend l'état, sort.

    ① RÔLE — Le programme en ligne de commande.
    ② CONTEXTE D'APPEL — `python3 -B programmes/ETAT_DES_TRAVAUX.py …`.
    ③ ENTRÉE — La ligne de commande (voir le module).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Le code de sortie : 0 rendu · 2 IMPOSSIBLE · 5 PLANTAGE.
      [rend: rien]
    ⑥ TRAITEMENT — Analyser les options ; appeler `etat_des_travaux` ; afficher le tableau ou le JSON.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sur la sortie standard.
    ⑪ TERMINAISON — Sort par sys.exit.
      [sort: oui]
    """
    p = argparse.ArgumentParser(description="État des versions en attente (branches travail-*).")
    p.add_argument("--depot", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p.add_argument("--gh", default="gh")
    p.add_argument("--public", default=PUBLIC_PAR_DEFAUT)
    p.add_argument("--sans-fetch", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--tout", action="store_true")
    a = p.parse_args()
    try:
        etat = etat_des_travaux(a.depot, a.gh, a.public, fetch=not a.sans_fetch)
    except Impossible as e:
        print(f"IMPOSSIBLE — {e} — rien n'est rangé (R-734)")
        sys.exit(IMPOSSIBLE)
    except Exception as e:  # PLANTAGE : jamais lu comme un verdict
        print(f"PLANTAGE — {type(e).__name__} : {e}")
        sys.exit(PLANTAGE)
    print(json.dumps(etat, ensure_ascii=False, indent=1) if a.json else tableau(etat, a.tout))
    sys.exit(RENDU)


if __name__ == "__main__":
    main()
