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
  echanges/RELU.md (date, ligne « ## VERDICT : … ») ; les branches origin/epreuves-longues/<passage>/<CODE> et leur
  RESULTAT.json ; dans origin/main, le fabricant programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (largeur, groupe, noms des
  circuits longs, préfixe des branches de résultats — LUS, jamais recopiés, R-708) ; les passages GitHub du dépôt
  public par « gh run list » et « gh run view ».
④ CONDITIONS D'ENTRÉE — git et gh lancés sans invite ; gh authentifié pour le dépôt public.
⑤ SORTIE — Un tableau lisible, ou du JSON avec --json. Code de sortie : 0 l'état est rendu · 2 IMPOSSIBLE, une source
  n'a pas pu être lue (git ou gh) et RIEN n'est rangé (R-734) · 5 PLANTAGE (exception imprévue, jamais un verdict).
⑥ TRAITEMENT — fetch (sauf --sans-fetch) · lire le fabricant · relever les résultats d'épreuves longues et la pointe
  jouée de chacun · relever les passages GitHub vivants · pour chaque branche : relever les faits, puis `ranger`.
⑦ UNITÉ — Heures de Paris à l'affichage ; secondes depuis l'époque Unix dans le JSON ; des fils (machines GitHub).
⑧ POURQUOI — Le 20-11-2026, trois faits : Cowork a rejoué des épreuves que GitHub jouait au même moment ; des étapes
  étaient « en cours » sans travail réel ; le Chat ne voit l'état qu'à ses réveils. Un état tiré des preuves, recalculé
  à chaque appel, ne dépend d'aucune mémoire.
⑨ CE QUI CLOCHE — (a) Un verdict autre que « DÉPLOYABLE » tout court (par exemple « DÉPLOYABLE APRÈS CORRECTIONS »)
  renvoie la branche en ÉCRITURE : règle la plus stricte, choisie ici, non décidée par Jean-Luc. (b) Une branche née de
  main sans aucun commit a sa pointe dans main : elle est rangée INSTALLÉE. (c) Un passage vivant est rattaché à une
  branche par son nom (headBranch), pas par sa pointe. (d) Les épreuves jouées valent pour la « pointe d'auteur » :
  la pointe, moins les commits qui ne touchent que echanges/RELU.md ou archives/ ; un commit de la note seule après
  la demande d'épreuves invalide les résultats. (e) Le registre etudes/REGISTRE_DES_TRAVAUX/ de travail-livrer-2 est
  un JOURNAL DE LANCEMENTS (étape, branche, exécutant, identifiant, lancé, fini, résultat) : il ne range pas une
  branche, il n'est donc pas lu ici. (f) Le dépôt public est nommé par défaut ici : le fabricant ne l'écrit pas en
  constante.
⑩ EFFET — Lit git et GitHub ; « git fetch » met à jour les références distantes du clone. N'écrit aucun fichier.
⑪ TERMINAISON — Sort du programme par sys.exit ; chaque appel à git ou gh est borné (DELAI_S secondes).
"""
import argparse
import ast
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
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
NOTE, RELU = "echanges/A_RELIRE.md", "echanges/RELU.md"
ETATS = ("ÉCRITURE", "À ÉPROUVER", "EN ÉPREUVE", "ÉPREUVE ROUGE", "À RELIRE", "DÉPLOYABLE", "INSTALLÉE")
RENDU, IMPOSSIBLE, PLANTAGE = 0, 2, 5
MOTIF_POINTE_DU_JOURNAL = re.compile(r"source de la publication : le commit ([0-9a-f]{7,40}) du dépôt privé")
MOTIF_VERDICT = re.compile(r"^\s*(#{1,6}\s*)?(\d+\s*·\s*)?\**VERDICT( EN UNE LIGNE)?\**\s*(:|$)")
MOTIF_CODE = re.compile(r"^-\s+`?([A-Za-z][A-Za-z0-9_]*)`?\s*$")


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


def lire_le_fabricant(depot):
    """Lit dans le fabricant de origin/main la largeur et les circuits longs.

    ① RÔLE — Donner la largeur des circuits longs, leur groupe, le nom de leurs circuits et le préfixe des branches
      de résultats, tels que le fabricant les écrit.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois.
    ③ ENTRÉE — `depot` : le clone.
    ④ CONDITIONS D'ENTRÉE — origin/main porte programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py.
    ⑤ SORTIE — UNE valeur : un dict {largeur, groupe, circuits_longs, prefixe}.
      [rend: 1]
    ⑥ TRAITEMENT — Lire le fichier par « git show » ; l'analyser par ast SANS l'exécuter ; relever les constantes
      PARTS_EN_MEME_TEMPS, GROUPE_DES_MACHINES_LONGUES, EPREUVES_BRANCHES ; puis, parmi les affectations de premier
      niveau dont un dictionnaire porte la clé « groupe » liée à GROUPE_DES_MACHINES_LONGUES, le « name: » de premier
      niveau du gabarit — ce sont les circuits qui partagent les fils.
    ⑦ UNITÉ — Des fils (jobs GitHub simultanés).
    ⑧ POURQUOI — R-708 : un chiffre qui existe ailleurs ne se recopie pas. Le fabricant n'est pas importé : il écrit.
    ⑨ CE QUI CLOCHE — Si le fabricant renomme ces constantes, la lecture lève Impossible : voulu.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    source = git(depot, "show", "origin/main:" + FABRICANT)
    arbre = ast.parse(source)
    constantes, circuits = {}, []
    for n in arbre.body:
        if not (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)):
            continue
        if isinstance(n.value, ast.Constant):
            constantes[n.targets[0].id] = n.value.value
        lie = any(isinstance(k, ast.Constant) and k.value == "groupe" and isinstance(v, ast.Name)
                  and v.id == "GROUPE_DES_MACHINES_LONGUES"
                  for d in ast.walk(n.value) if isinstance(d, ast.Dict) for k, v in zip(d.keys, d.values))
        if lie:
            texte = "".join(c.value for c in ast.walk(n.value)
                            if isinstance(c, ast.Constant) and isinstance(c.value, str))
            circuits += re.findall(r"(?m)^name: (.+)$", texte)[:1]
    manque = [c for c in ("PARTS_EN_MEME_TEMPS", "GROUPE_DES_MACHINES_LONGUES", "EPREUVES_BRANCHES")
              if c not in constantes]
    if manque or not circuits or not isinstance(constantes.get("PARTS_EN_MEME_TEMPS"), int):
        raise Impossible(f"fabricant illisible : constantes absentes {manque}, circuits longs {circuits}")
    return {"largeur": constantes["PARTS_EN_MEME_TEMPS"], "groupe": constantes["GROUPE_DES_MACHINES_LONGUES"],
            "circuits_longs": sorted(set(circuits)), "prefixe": constantes["EPREUVES_BRANCHES"]}


def codes_a_jouer(note):
    """Relève les codes de la section « ## À JOUER SUR GITHUB » d'une note.

    ① RÔLE — Dire quelles épreuves longues la note demande.
    ② CONTEXTE D'APPEL — `faits_d_une_branche`.
    ③ ENTRÉE — `note` : le texte de echanges/A_RELIRE.md.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des codes, dans l'ordre, sans doublon.
      [rend: 1]
    ⑥ TRAITEMENT — Après la ligne « ## À JOUER SUR GITHUB », jusqu'à la prochaine ligne qui commence par « # » :
      garder les lignes « - CODE » ou « - `CODE` » où CODE est un identifiant seul sur sa ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les notes du 20-11-2026 écrivent les deux formes (travail-contrat-6 : « - VenteReglable » ;
      travail-livrer-2 : « - `Certification` »). Une ligne de prose (« - (aucune …) ») n'est pas un code.
    ⑨ CE QUI CLOCHE — Un code suivi d'un commentaire sur la même ligne n'est pas relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    codes, dedans = [], False
    for ligne in note.splitlines():
        if ligne.strip().startswith("## À JOUER SUR GITHUB"):
            dedans = True
            continue
        if dedans and ligne.startswith("#"):
            break
        m = MOTIF_CODE.match(ligne.strip()) if dedans else None
        if m and m.group(1) not in codes:
            codes.append(m.group(1))
    return codes


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
      « — CLORE … ».
      [rend: 1]
    ⑥ TRAITEMENT — Expression rationnelle.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « DÉPLOYABLE APRÈS CORRECTIONS » demande des corrections : la règle la plus stricte prime.
    ⑨ CE QUI CLOCHE — « CONFORME — RIEN DE NEUF QUI BLOQUE » n'est pas reconnu déployable.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return re.match(r"^\**DÉPLOYABLE\**\s*($|[·—-]\s*CLORE)", verdict) is not None


def resultats_github(depot, prefixe):
    """Relève tous les résultats d'épreuves longues rendus au dépôt privé.

    ① RÔLE — Dire, pour chaque pointe jouée, le code de sortie de chaque épreuve.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois.
    ③ ENTRÉE — `depot` : le clone · `prefixe` : le préfixe des branches de résultats, lu au fabricant.
    ④ CONDITIONS D'ENTRÉE — Les branches origin/<prefixe><passage>/<CODE> portent
      rapports/epreuves_longues/<passage>/<CODE>/RESULTAT.json.
    ⑤ SORTIE — DEUX valeurs : un dict {pointe complète : {code : {sortie, passage, heure}}} où, pour un même code et
      une même pointe, le résultat le plus récent l'emporte · la liste des branches de résultats sans pointe lisible.
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
    refs = git(depot, "for-each-ref", "--format=%(refname:short) %(committerdate:unix)",
               "refs/remotes/origin/" + prefixe)
    par_pointe, sans_pointe = {}, []
    for ligne in refs.splitlines():
        ref, heure = ligne.rsplit(" ", 1)
        morceaux = ref[len("origin/" + prefixe):].split("/")
        if len(morceaux) != 2:
            continue
        passage, code = morceaux
        fichiers = git(depot, "ls-tree", "-r", "--name-only", ref).splitlines()
        chemin = f"rapports/epreuves_longues/{passage}/{code}/RESULTAT.json"
        if chemin not in fichiers:
            sans_pointe.append(ref)
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


def passages_github(gh, public, circuits_longs):
    """Relève les passages GitHub vivants et les fils qu'ils occupent.

    ① RÔLE — Dire ce qui tourne sur GitHub, et combien de jobs des circuits longs ne sont pas finis.
    ② CONTEXTE D'APPEL — `etat_des_travaux`, une fois.
    ③ ENTRÉE — `gh` : le programme gh · `public` : « propriétaire/nom » du dépôt public · `circuits_longs` : les noms
      des circuits qui partagent les fils, lus au fabricant.
    ④ CONDITIONS D'ENTRÉE — gh authentifié.
    ⑤ SORTIE — DEUX valeurs : la liste des passages vivants (dicts : passage, circuit, branche, statut, jobs_vivants)
      · le nombre de jobs non finis des circuits longs (« épreuves en cours »).
      [rend: 2]
    ⑥ TRAITEMENT — « gh run list --limit 100 » ; vivant = statut autre que « completed » ; pour chaque passage
      vivant d'un circuit long, « gh run view --json jobs » et compter les jobs dont le statut n'est pas
      « completed ». Un passage long vivant dont aucun job n'est encore créé compte pour 0.
    ⑦ UNITÉ — Des jobs (un job occupe un fil).
    ⑧ POURQUOI — Les fils libres = largeur − épreuves en cours (demande du Chat du 20-11-2026).
    ⑨ CE QUI CLOCHE — Au-delà de 100 passages récents, un passage vivant plus ancien ne serait pas vu. Un job
      « preparer » d'un circuit long compte comme une épreuve.
    ⑩ EFFET — Lance gh.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    try:
        passages = json.loads(commande([gh, "run", "list", "-R", public, "--limit", "100", "--json",
                                        "databaseId,workflowName,status,headBranch,createdAt"]))
    except ValueError:
        raise Impossible("gh run list : réponse qui n'est pas du JSON")
    vivants, en_cours = [], 0
    for p in passages:
        if p.get("status") == "completed":
            continue
        jobs = 0
        if p.get("workflowName") in circuits_longs:
            try:
                vue = json.loads(commande([gh, "run", "view", str(p["databaseId"]), "-R", public, "--json", "jobs"]))
            except ValueError:
                raise Impossible(f"gh run view {p['databaseId']} : réponse qui n'est pas du JSON")
            jobs = sum(1 for j in vue.get("jobs", []) if j.get("status") != "completed")
            en_cours += jobs
        vivants.append({"passage": p["databaseId"], "circuit": p.get("workflowName"), "branche": p.get("headBranch"),
                        "statut": p.get("status"), "jobs_vivants": jobs})
    return vivants, en_cours


def pointe_d_auteur(depot, base, pointe):
    """Rend la pointe de la branche sans les commits de relecture.

    ① RÔLE — Donner le commit auquel les épreuves jouées doivent correspondre.
    ② CONTEXTE D'APPEL — `faits_d_une_branche`.
    ③ ENTRÉE — `depot` : le clone · `base` : le point de départ de la branche (merge-base avec origin/main) ·
      `pointe` : la pointe de la branche.
    ④ CONDITIONS D'ENTRÉE — `base` est un ancêtre de `pointe`.
    ⑤ SORTIE — UNE valeur : le premier commit, en remontant la première lignée depuis la pointe, qui touche autre
      chose que echanges/RELU.md et archives/ ; `base` si aucun commit de la branche ne le fait (la branche ne porte
      alors que de la relecture : son travail est celui de main).
      [rend: 1]
    ⑥ TRAITEMENT — « git log --first-parent --name-only base..pointe », du plus récent au plus ancien.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Cas réel du 20-11-2026 : travail-contrat-6 jouée sur 0787558b1, puis trois commits de Cowork (RELU,
      archive) jusqu'à 1bc903007 ; les épreuves restent valables pour la pointe 1bc903007.
    ⑨ CE QUI CLOCHE — Un commit de fusion (sans fichier listé) arrête la remontée.
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    sortie = git(depot, "log", "--first-parent", "--format=%x01%H", "--name-only", f"{base}..{pointe}")
    for bloc in sortie.split("\x01")[1:]:
        lignes = [x for x in bloc.splitlines() if x.strip()]
        sha, fichiers = lignes[0], lignes[1:]
        if not fichiers or any(f != RELU and not f.startswith("archives/") for f in fichiers):
            return sha
    return base


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
    ③ ENTRÉE — `faits` : un dict {installee, note_heure, codes, passages_vivants, resultats, relu_heure, verdict,
      pointe_auteur}.
    ④ CONDITIONS D'ENTRÉE — `resultats` ne porte que les résultats de la pointe d'auteur.
    ⑤ SORTIE — DEUX valeurs : l'état (un des ETATS) · la prochaine action, en français.
      [rend: 2]
    ⑥ TRAITEMENT — Dans cet ordre, le premier qui s'applique : pointe dans main → INSTALLÉE · pas de note écrite sur
      la branche → ÉCRITURE · un passage GitHub vivant sur la branche → EN ÉPREUVE · un code demandé rendu non nul →
      ÉPREUVE ROUGE · un code demandé sans résultat → À ÉPROUVER · RELU absent ou plus ancien que la note →
      À RELIRE · verdict DÉPLOYABLE → DÉPLOYABLE · sinon ÉCRITURE (reprendre selon le RELU).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Cet ordre suit la conception (§ 2.4 ②) : la relecture Cowork ne devient prête qu'une fois
      l'épreuve longue de la MÊME pointe verte ; c'est ce qui supprime le doublon du 20-11-2026.
    ⑨ CE QUI CLOCHE — Une note sans section « ## À JOUER SUR GITHUB » passe droit à la relecture.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if faits["installee"]:
        return "INSTALLÉE", "rien — pointe dans main (branche supprimable sur accord de Jean-Luc)"
    if faits["note_heure"] is None:
        return "ÉCRITURE", "écrire et pousser echanges/A_RELIRE.md sur la branche"
    if faits["passages_vivants"]:
        return "EN ÉPREUVE", "attendre la fin du passage " + ", ".join(str(p) for p in faits["passages_vivants"])
    resultats = faits["resultats"]
    rouges = [c for c in faits["codes"] if c in resultats and resultats[c]["sortie"] != 0]
    if rouges:
        return "ÉPREUVE ROUGE", ("lire SORTIE.txt et réparer : " + ", ".join(
            f"{c} (code {resultats[c]['sortie']}, passage {resultats[c]['passage']})" for c in rouges))
    manquants = [c for c in faits["codes"] if c not in resultats]
    if manquants:
        return "À ÉPROUVER", (f"déposer la demande d'épreuves longues sur {faits['pointe_auteur'][:9]} : "
                              + ", ".join(manquants))
    if faits["relu_heure"] is None or faits["relu_heure"] < faits["note_heure"]:
        return "À RELIRE", "lancer la relecture Cowork (épreuves longues à lire sur GitHub, ne pas les rejouer)"
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
    ⑤ SORTIE — UNE valeur : le dict des faits, plus « branche », « pointe », « pointe_heure », « resultats_tous ».
      [rend: 1]
    ⑥ TRAITEMENT — pointe ; INSTALLÉE si la pointe est un ancêtre de origin/main, ou si la pointe d'auteur est le
      départ de la branche (seule de la relecture a été ajoutée après main) — rien d'autre n'est lu alors ; sinon
      merge-base, dates de la note et du RELU sur la branche, codes, verdict, pointe d'auteur, résultats de
      cette pointe, passages vivants de même nom de branche.
    ⑦ UNITÉ — Secondes Unix.
    ⑧ POURQUOI — Séparer la lecture (ici) du rangement (`ranger`), pour éprouver le rangement sans git.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance git.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    ref = "origin/" + branche
    pointe = git(depot, "rev-parse", ref).strip()
    faits = {"branche": branche, "pointe": pointe, "pointe_heure": int(git(depot, "log", "-1", "--format=%ct", ref)),
             "installee": False, "note_heure": None, "codes": [], "passages_vivants": [], "resultats": {},
             "relu_heure": None, "verdict": "", "pointe_auteur": pointe}
    code = commande(["git", "-C", depot, "merge-base", "--is-ancestor", pointe, "origin/main"], tolere=True)
    if code == 0:
        faits["installee"] = True
        return faits
    if code != 1:
        raise Impossible(f"merge-base --is-ancestor {branche} : code {code}")
    base = git(depot, "merge-base", pointe, "origin/main").strip()
    faits["note_heure"] = date_du_dernier_commit(depot, base, pointe, NOTE)
    faits["relu_heure"] = date_du_dernier_commit(depot, base, pointe, RELU)
    if faits["note_heure"] is not None:
        faits["codes"] = codes_a_jouer(git(depot, "show", f"{ref}:{NOTE}"))
    if faits["relu_heure"] is not None:
        faits["verdict"] = verdict_du_relu(git(depot, "show", f"{ref}:{RELU}"))
    faits["pointe_auteur"] = pointe_d_auteur(depot, base, pointe)
    if faits["pointe_auteur"] == base:
        faits["installee"] = True
        return faits
    faits["resultats"] = resultats.get(faits["pointe_auteur"], {})
    faits["passages_vivants"] = [v["passage"] for v in vivants if v["branche"] == branche]
    return faits


def etat_des_travaux(depot, gh="gh", public=PUBLIC_PAR_DEFAUT, fetch=True):
    """Rend l'état de toutes les branches travail-*.

    ① RÔLE — Le point d'entrée commun au tableau, au JSON et à l'alarme.
    ② CONTEXTE D'APPEL — `main` ; programmes/ALARME_DES_MACHINES_OISIVES.py.
    ③ ENTRÉE — `depot` : le clone · `gh` : le programme gh · `public` : le dépôt public · `fetch` : faire
      « git fetch origin » d'abord.
    ④ CONDITIONS D'ENTRÉE — Voir le module.
    ⑤ SORTIE — UNE valeur : un dict {heure, fabricant, fils, passages, branches, resultats_sans_pointe}.
      [rend: 1]
    ⑥ TRAITEMENT — fetch · fabricant · résultats · passages · faits et rangement de chaque origin/travail-* ·
      fils libres = largeur − épreuves en cours, jamais sous 0.
    ⑦ UNITÉ — Fils ; secondes Unix.
    ⑧ POURQUOI — Voir le module.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — « git fetch » met à jour les références distantes ; lance gh.
    ⑪ TERMINAISON — Rend la main ou lève Impossible.
      [sort: non]
    """
    if fetch:
        git(depot, "fetch", "-q", "origin")
    fab = lire_le_fabricant(depot)
    resultats, sans_pointe = resultats_github(depot, fab["prefixe"])
    vivants, en_cours = passages_github(gh, public, fab["circuits_longs"])
    branches = []
    for ligne in git(depot, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/travail-*").splitlines():
        faits = faits_d_une_branche(depot, ligne[len("origin/"):], resultats, vivants)
        faits["etat"], faits["action"] = ranger(faits)
        branches.append(faits)
    return {"heure": int(time.time()), "fabricant": fab,
            "fils": {"largeur": fab["largeur"], "epreuves_en_cours": en_cours,
                     "libres": max(0, fab["largeur"] - en_cours)},
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
           f"fils GitHub des circuits longs : largeur {f['largeur']} (lue au fabricant) − épreuves en cours "
           f"{f['epreuves_en_cours']} = {f['libres']} libre(s)"]
    for p in etat["passages"]:
        out.append(f"  tourne : passage {p['passage']} · {p['circuit']} · {p['branche']} · {p['statut']}"
                   f" · {p['jobs_vivants']} job(s) non fini(s)")
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
