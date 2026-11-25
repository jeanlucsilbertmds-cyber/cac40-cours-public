#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INSTALLER.py — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Demande de Jean-Luc du 20-11-2026 à 19h38 (voir programmes/LIVRER.py) : installer une branche relue
sur main par un PROGRAMME, jamais de mémoire. Règle A-818 (Jean-Luc, 15-11-2026 à 15h42 et 15h48) : « juste avant
d'installer, on regarde si un traitement tourne ou attend son tour […] : s'il n'y en a aucun, on installe tout de
suite ; s'il y en a un, on attend qu'il finisse, puis on revérifie ».
Réparation du 20-11-2026 au soir (relecteur neuf : « NON DÉPLOYABLE », parce qu'une exception levée APRÈS la poussée
de main sortait en « refusé, rien installé » alors que main avait bougé ; superviseur R-759 : « RUSTINE, À REPRENDRE,
AVEC SIMPLIFICATION ») : INSTALLER S'ARRÊTE À LA FUSION POUSSÉE. Il ne publie plus rien : programmes/REPUBLIER.py
amène le public à main (lancé à la main, et vérifié en tête du circuit du soir). Avant de fusionner, il exige la
PREUVE des épreuves longues lue dans les RESULTAT.json de GitHub, jamais dans la note du Chat.
Décision de Jean-Luc du 21-11-2026 à 13h27 (réponse « 1 » à la question N-2 du Chat de 13h25, critère : « le circuit
du soir ne doit jamais tomber à cause d'une installation » ; choix « 1. INSTALLER enchaîne lui-même la republication
(recommandé) ») : APRÈS la fusion poussée, INSTALLER lance lui-même programmes/REPUBLIER.py (le programme existant,
par sous-processus : R-708, aucune ligne recopiée), puis « REPUBLIER.py --verifier » sur main et un clone public neuf.
Il ne rend 0 que si ce contrôle passe ; sinon il rend 4 et dit « main installé, public EN RETARD : lancer REPUBLIER »
avec la commande exacte. Le pas « Le public porte-t-il le code de main ? » du circuit du soir reste la seconde ligne
de défense.

① RÔLE — Installer sur main une branche travail-… jugée DÉPLOYABLE par Cowork, dont les épreuves longues ont été
  jouées par GitHub sur le code relu et rendent toutes 0.
② CONTEXTE D'APPEL — À la main par le Chat, depuis la racine de son clone privé :
  python3 -B programmes/INSTALLER.py <branche travail-…>
  (la republication est enchaînée par INSTALLER ; sur le code 4 seulement : python3 -B programmes/REPUBLIER.py)
③ ENTRÉE — La branche. Les variables LIVRER_* de programmes/LIVRER.py valent ici aussi.
④ CONDITIONS D'ENTRÉE — Celles de LIVRER.py ; main n'est extraite dans aucun worktree, ou dans un worktree propre à
  la pointe d'origin/main.
⑤ SORTIE — Le code de sortie : 0 INSTALLÉ ET PUBLIC À JOUR (main poussée, REPUBLIER puis REPUBLIER --verifier
  rendent 0) · 4 INSTALLÉ, PUBLIC EN RETARD (main poussée, mais la republication ou son contrôle a échoué : la
  commande à lancer est affichée) · 1 REFUSÉ, rien installé (RELU absent, pas de Cowork, verdict autre que DÉPLOYABLE, pointe
  relue hors de l'histoire ou dépassée par du code, preuve des épreuves absente, d'une autre pointe ou rouge, fusion
  en conflit, poussée de main refusée) · 3 RÉESSAYER (un passage tourne ou attend, A-818 ; rien n'est écrit) ·
  5 PLANTAGE (exception imprévue : l'état de main est à relire, le programme ne sait pas s'il a poussé).
⑥ TRAITEMENT — ① RELU de la branche lu et jugé · ② preuve des épreuves longues (`prouver_les_epreuves`) · ③ aucun
  passage en cours ni en attente au public ni au privé · ④ fusion --no-ff dans le worktree de main, entrée
  « installation » au registre dans le commit de fusion, poussée sans force · ⑤ republication enchaînée
  (`republier_apres_installation`) : REPUBLIER, puis REPUBLIER --verifier → code 0, ou 4.
⑦ UNITÉ — Heures de Paris (registre).
⑧ POURQUOI — Voir le sens en tête. Installer et publier restent deux PROGRAMMES (chacun simple, chaque code juste),
  mais INSTALLER enchaîne le second (décision du 21-11-2026 à 13h27) : sans cela, le circuit du soir tombait au pas
  « Poser les programmes publics » jusqu'à ce que quelqu'un pense à lancer REPUBLIER (N-2 du RELU de Cowork).
⑨ CE QUI CLOCHE — Entre le regard ③ et la poussée, un passage peut démarrer (quelques secondes). Sur le code 4, le
  public reste en retard tant que REPUBLIER n'a pas tourné : le circuit du soir le signale en tête (pas « Le public
  porte-t-il le code de main ? ») et nomme la commande. Le REPUBLIER lancé est celui posé à côté de ce programme (le
  clone du Chat), pas celui de main : un REPUBLIER changé par la branche installée ne sert qu'au passage suivant ; mais
  publication ET vérification prennent le FABRICANT de main (`LIVRER.fabricant_de`, N-21 du RELU de Cowork sur
  4e4dc386f). Une branche dont la note déclare « aucune » épreuve longue ne s'installe que si elle ne
  change rien hors de echanges/, archives/ et du registre, ET, depuis le 25-11-2026 (A-995), avec la preuve verte de
  « Livraison », exigée de toute branche (`LIVRER.changes_hors_permis` ; N-3, puis N-14 du RELU de
  Cowork sur e7b230083). Le regard ③ précède la fusion ; l'étape ⑤ peut ensuite publier jusqu'à 7 200 s : une
  installation lancée peu avant 20h peut pousser au public pendant le circuit du soir, qui garde son pas de défense
  (N-23 du RELU de Cowork sur 4e4dc386f ; éviter l'heure qui précède 20h est une question posée à Jean-Luc, pas une
  décision).
⑩ EFFET — Pousse sur main au privé, jamais en force. Au public, seulement par REPUBLIER (son fabricant, sans force).
⑪ TERMINAISON — Sort du programme par sys.exit.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import LIVRER as L

RELU = "echanges/RELU.md"
INSTALLE, REFUS, REESSAYER, PLANTAGE = 0, 1, 3, L.PLANTAGE
PUBLIC_EN_RETARD = 4   # main installée, public non prouvé à jour (décision de Jean-Luc du 21-11-2026 à 13h27)
REPUBLIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "REPUBLIER.py")
BRANCHES_DES_RESULTATS = "refs/remotes/origin/epreuves-longues/"   # le préfixe EPREUVES_BRANCHES du fabricant, au privé
DOSSIER_DES_RESULTATS = "rapports/epreuves_longues"                 # où le circuit dépose RESULTAT.json sur ces branches


# « Même code » : une seule écriture, LIVRER.changes_hors_permis (R-708, N-14 du RELU de Cowork sur e7b230083) ;
# ce nom la désigne ici pour `juger_le_relu` et `meme_code`.
changes_hors_permis = L.changes_hors_permis


def juger_le_relu(racine, branche):
    """Étape ① : le dernier RELU de la branche permet-il l'installation ? Rend la pointe relue, ou lève Arret(1).

    ① RÔLE — N'installer que ce que Cowork a jugé DÉPLOYABLE, à la pointe qui sera installée.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le clone privé · `branche`.
    ④ CONDITIONS D'ENTRÉE — origin/<branche> lu.
    ⑤ SORTIE — UNE valeur : le commit relu (40 caractères).
      [rend: 1]
    ⑥ TRAITEMENT — echanges/RELU.md à origin/<branche> : une ligne « RELU PAR : Cowork » ; le dernier commit qui
      touche ce fichier a pour auteur exactement « cowork » (casse ignorée) ; UN seul titre « VERDICT : … », dont la valeur
      est exactement DÉPLOYABLE (« DÉPLOYABLE APRÈS CORRECTIONS » refusé) ; « pointe relue <sha> » se résout, est un
      ancêtre de la pointe (sabotage M5 du relecteur : une pointe hors de l'histoire), et seuls echanges/, archives/
      et le registre des travaux ont changé depuis.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026, étape ① ; l'auteur du commit est une PROPRIÉTÉ que le texte seul ne donne
      pas (un RELU écrit par un relecteur neuf du Chat porte aussi « RELU PAR »).
    ⑨ CE QUI CLOCHE — L'auteur git se déclare : n'importe qui peut écrire « cowork » ; c'est un filet contre l'oubli,
      pas une preuve (relecture de Cowork, D-5). Le nom est comparé EN ENTIER (« Claude (pas cowork) » refusé).
      Le format exigé est écrit au mode d'emploi des échanges, section « CE QUE LES PROGRAMMES LISENT » (D-4).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    ref = f"origin/{branche}"
    lu = L.git(racine, "show", f"{ref}:{RELU}")
    if lu.returncode != 0:
        raise L.Arret(REFUS, f"{RELU} absent de {ref}")
    texte = lu.stdout
    if not re.search(r"(?im)^\s*RELU PAR\s*:\s*\**\s*Cowork\b", texte):
        raise L.Arret(REFUS, "le RELU ne porte pas « RELU PAR : Cowork »")
    auteur = L.git(racine, "log", "-1", "--format=%an", ref, "--", RELU).stdout.strip()
    if not L.est_cowork(auteur):
        raise L.Arret(REFUS, f"le dernier commit du RELU n'est pas de Cowork (auteur : {auteur or 'aucun'})")
    verdicts = re.findall(r"(?m)^#+\s*VERDICT\s*:\s*(.+?)\s*$", texte)
    if len(verdicts) != 1:
        raise L.Arret(REFUS, f"le RELU porte {len(verdicts)} titre(s) « VERDICT : » (un seul attendu)")
    valeur = re.sub(r"[*`_]", "", verdicts[0]).strip()
    if valeur != "DÉPLOYABLE":
        raise L.Arret(REFUS, f"verdict « {valeur} » : seul « DÉPLOYABLE » s'installe")
    m = re.search(r"(?i)pointe relue\s*:?\s*`?([0-9a-f]{7,40})", texte)
    if not m:
        raise L.Arret(REFUS, "le RELU ne dit pas sa « pointe relue »")
    relue = L.git(racine, "rev-parse", "--verify", "-q", m.group(1) + "^{commit}").stdout.strip()
    if not relue or L.git(racine, "merge-base", "--is-ancestor", relue, ref).returncode != 0:
        raise L.Arret(REFUS, f"pointe relue {m.group(1)} inconnue ou hors de l'histoire de {ref}")
    if L.git(racine, "merge-base", "--is-ancestor", ref, "origin/main").returncode == 0:
        raise L.Arret(REFUS, f"{ref} est déjà dans origin/main : rien à installer")
    hors = changes_hors_permis(racine, relue, ref)
    if hors:
        raise L.Arret(REFUS, f"{len(hors)} fichier(s) changé(s) depuis la pointe relue {relue[:12]} : {', '.join(hors[:5])}")
    return relue


def meme_code(racine, jouee, relue):
    """Rend vrai si la pointe jouée par GitHub porte le même code que la pointe relue par Cowork.

    ① RÔLE — Relier la preuve des épreuves au code relu.
    ② CONTEXTE D'APPEL — `prouver_les_epreuves`.
    ③ ENTRÉE — `racine` · `jouee` : la pointe lue dans RESULTAT.json · `relue` : la pointe relue (40 caractères).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — Égalité exacte ; ou bien `jouee` est un ancêtre de `relue` et seuls echanges/, archives/ et le
      registre ont changé entre les deux (`changes_hors_permis`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026 au soir : « la POINTE JOUÉE est égale à la pointe relue par Cowork ». LIVRER
      joue la pointe T, puis pousse la note et le registre (pointe T+1) que Cowork relit : l'égalité stricte refuserait
      chaque installation où Cowork nomme la pointe qu'il a lue. L'égalité est donc prise AU CODE PRÈS, avec la même
      propriété que `juger_le_relu` applique entre la pointe relue et la pointe installée (choix du sous-agent, à
      valider par Jean-Luc ; le sabotage « égalité retirée » le fait mordre).
    ⑨ CE QUI CLOCHE — Une pointe jouée inconnue du clone (non récupérée) rend faux.
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not re.fullmatch(r"[0-9a-f]{40}", jouee or ""):
        return False
    if jouee == relue:
        return True
    if L.git(racine, "merge-base", "--is-ancestor", jouee, relue).returncode != 0:
        return False
    return not changes_hors_permis(racine, jouee, relue)


def livraison_de_la_note(racine, res, relue):
    """Rend vrai si un RESULTAT.json de « Livraison » a jugé la NOTE relue, et l'a jugée verte.

    ① RÔLE — Relier le contrôle final (A-995) à la note que Cowork a relue, et non seulement au code.
    ② CONTEXTE D'APPEL — `prouver_les_epreuves`, pour le seul code « Livraison » (L.LIVRAISON).
    ③ ENTRÉE — `racine` · `res` : le RESULTAT.json lu (dictionnaire) · `relue` : la pointe relue (40 caractères).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — le même code (`meme_code`) ; le détail du joueur dit VERT ; et la pointe jouée EST la pointe
      relue, OU le sha256 de la note dans le détail (« sha256_de_la_note ») est celui de echanges/A_RELIRE.md à la
      pointe relue (octets lus par « git cat-file blob »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 25-11-2026, (b) : `meme_code` accepte un résultat joué sur un ancêtre quand
      seuls echanges/ et le registre ont changé, or c'est echanges/A_RELIRE.md que « Livraison » juge ; LIVRER écrit
      désormais ses résultats à part (echanges/RESULTATS_GITHUB.md), la note reste celle qui a été jugée.
    ⑨ CE QUI CLOCHE — Le détail est écrit par le code de la version jouée (programmes/CONTROLER_LA_LIVRAISON_SUR_GITHUB.py
      de la branche) : une branche qui affaiblit ce programme se fait juger par lui (superviseur, point 13, BACKLOG).
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    jouee = res.get("pointe_jouee", "")
    detail = res.get("detail_de_l_epreuve") if isinstance(res.get("detail_de_l_epreuve"), dict) else {}
    if detail.get("verdict") != "VERT" or not meme_code(racine, jouee, relue):
        return False
    if jouee == relue:
        return True
    note = L.lancer(["git", "-C", racine, "rev-parse", "--verify", "-q", f"{relue}:{L.NOTE}"])
    if note.returncode != 0:
        return False
    octets = subprocess.run(["git", "-C", racine, "cat-file", "blob", note.stdout.strip()], capture_output=True,
                            timeout=600)
    return octets.returncode == 0 and hashlib.sha256(octets.stdout).hexdigest() == detail.get("sha256_de_la_note")


def prouver_les_epreuves(racine, relue):
    """Étape ② : les épreuves longues déclarées à la pointe relue ont-elles été jouées par GitHub sur ce code, et
    rendent-elles 0 ? Rend la liste des (code, passage) prouvés, ou lève Arret(1).

    ① RÔLE — N'installer que ce que GitHub a éprouvé, lu à la source (RESULTAT.json), jamais dans la note du Chat.
    ② CONTEXTE D'APPEL — `main`, après `juger_le_relu`.
    ③ ENTRÉE — `racine` : le clone privé (fetch fait : les branches origin/epreuves-longues/… sont lues) · `relue`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des (code, numéro de passage) ; elle porte TOUJOURS « Livraison » (depuis le
      25-11-2026, A-995 : même une note « aucune », sur un travail qui ne change aucun code qui s'exécute, exige le
      contrôle final vert) ; une note « aucune » sur un travail qui change du code est refusée (N-3).
      [rend: 1]
    ⑥ TRAITEMENT — La note et la table à la pointe relue donnent les codes (`LIVRER.codes_a_jouer`, R-708 ; section
      absente, vide ou nom sans code → refus), « Livraison » ajoutée en tête si elle n'y est pas. Pour chaque code :
      chaque branche
      origin/epreuves-longues/<passage>/<CODE> ; son RESULTAT.json ; on garde ceux dont « pointe_jouee » porte le même
      code que la pointe relue (`meme_code`) — pour « Livraison », ceux qui ont jugé la note relue et l'ont dite
      verte (`livraison_de_la_note`) ; le passage le plus récent (numéro le plus grand) fait foi ; son
      « code_de_sortie » doit valoir 0 (sabotage M6 du relecteur). Aucun résultat retenu → refus (M1 : une épreuve
      absente n'est jamais verte).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026 au soir, point A : « La note écrite par le Chat ne fait JAMAIS foi ».
    ⑨ CE QUI CLOCHE — La LISTE des épreuves vient de la note à la pointe relue (relue par Cowork) ; seuls les
      RÉSULTATS viennent de GitHub. Un passage plus ancien vert ne rattrape pas un plus récent rouge.
    ⑩ EFFET — Lance git en lecture.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    note = L.git(racine, "show", f"{relue}:{L.NOTE}")
    table = L.git(racine, "show", f"{relue}:{L.TABLE}")
    if note.returncode != 0 or table.returncode != 0:
        raise L.Arret(REFUS, f"note ou table des épreuves illisible à la pointe relue {relue[:12]}")
    codes, sans, etat = L.codes_a_jouer(note.stdout, json.loads(table.stdout).get("epreuves_longues", {}))
    if etat in ("absente", "vide") or sans:
        raise L.Arret(REFUS, f"la note relue ne dit pas quoi jouer (section {etat}, sans code : {', '.join(sans) or '—'})")
    change = L.code_change_par(racine, relue) if etat == "aucune" else []
    if change:
        raise L.Arret(REFUS, "la note relue déclare « aucune » épreuve longue, mais ce travail change du code qui "
                             "s'exécute : " + ", ".join(change[:5]) + " (N-3)")
    if L.LIVRAISON not in codes:   # toujours exigée, même absente de la note (A-995 ; superviseur R-759, point 12)
        codes = [L.LIVRAISON] + codes
    prouves = []
    for code in codes:
        retenus = []
        for ref in L.git(racine, "for-each-ref", "--format=%(refname)", BRANCHES_DES_RESULTATS).stdout.split():
            morceaux = ref[len(BRANCHES_DES_RESULTATS):].split("/")
            if len(morceaux) != 2 or morceaux[1] != code or not morceaux[0].isdigit():
                continue
            lu = L.git(racine, "show", f"{ref}:{DOSSIER_DES_RESULTATS}/{morceaux[0]}/{code}/RESULTAT.json")
            try:
                res = json.loads(lu.stdout) if lu.returncode == 0 else None
            except ValueError:
                res = None
            if not isinstance(res, dict):
                continue
            if (livraison_de_la_note(racine, res, relue) if code == L.LIVRAISON
                    else meme_code(racine, res.get("pointe_jouee", ""), relue)):
                retenus.append((int(morceaux[0]), res))
        if not retenus:
            raise L.Arret(REFUS, f"aucune preuve GitHub pour {code} sur le code relu {relue[:12]} "
                                 f"(RESULTAT.json absent, ou d'une autre pointe)")
        passage, res = max(retenus, key=lambda x: x[0])
        if res.get("code_de_sortie") != 0:
            raise L.Arret(REFUS, f"{code} : code {res.get('code_de_sortie')} au passage {passage} (RESULTAT.json)")
        prouves.append((code, passage))
    return prouves


def passages_en_cours(racine):
    """Étape ② (A-818) : rend la liste des passages en cours ou en attente, au public et au privé.

    ① RÔLE — Voir si un traitement tourne ou attend son tour, circuit du soir compris.
    ② CONTEXTE D'APPEL — `main`, juste avant la fusion.
    ③ ENTRÉE — `racine` : le clone privé (pour nommer le dépôt privé).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des « dépôt circuit numéro état ».
      [rend: 1]
    ⑥ TRAITEMENT — « gh run list --repo <d> --limit 100 --json … » pour les deux dépôts, tous circuits ; état
      différent de completed.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-818 : plus aucune heure interdite fixe, un regard juste avant chaque installation.
    ⑨ CE QUI CLOCHE — Les 100 derniers passages de chaque dépôt seulement.
    ⑩ EFFET — Lit GitHub.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    vus = []
    for depot in (L.repo_public(), L.repo_prive(racine)):
        for p in L.gh_json("run", "list", "--repo", depot, "--limit", "100",
                           "--json", "databaseId,status,workflowName") or []:
            if p.get("status") != "completed":
                vus.append(f"{depot} « {p.get('workflowName')} » {p.get('databaseId')} {p.get('status')}")
    return vus


def worktree_de_main(racine):
    """Rend le worktree de main (pris tel quel s'il existe, propre et à jour) et s'il a été créé ici.

    ① RÔLE — Un dépôt privé sur la branche NOMMÉE main, pour fusionner puis publier.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le clone privé.
    ④ CONDITIONS D'ENTRÉE — fetch fait.
    ⑤ SORTIE — DEUX valeurs : le chemin, vrai s'il est jetable.
      [rend: 2]
    ⑥ TRAITEMENT — `LIVRER.worktree_nomme(racine, "main")`, avec le code REFUS au lieu de 3.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 ; main est souvent extraite dans la racine du Chat.
    ⑨ CE QUI CLOCHE — Le worktree pris tel quel est celui du Chat : la fusion y est faite.
    ⑩ EFFET — Peut créer un worktree.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    try:
        chemin, jetable = L.worktree_nomme(racine, "main")
    except L.Arret as e:
        raise L.Arret(REFUS, e.args[1])
    return chemin, jetable


def fusionner(wt, branche, relue):
    """Étape ④ : fusion --no-ff de origin/<branche> dans main, registre noté dans le commit, poussée sans force.

    ① RÔLE — Installer, et rien d'autre.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `wt` : le worktree de main · `branche` · `relue` : la pointe relue.
    ④ CONDITIONS D'ENTRÉE — `wt` propre, à origin/main.
    ⑤ SORTIE — UNE valeur : le commit de fusion poussé.
      [rend: 1]
    ⑥ TRAITEMENT — « git merge --no-ff --no-commit origin/<branche> » ; conflit → « git merge --abort » et refus ;
      entrée « installation » au registre ; commit — si l'un des deux lève, « git merge --abort » puis l'exception
      remonte (N-5 : le worktree de main, souvent celui du Chat, ne reste pas en fusion inachevée) ;
      « git push origin HEAD:refs/heads/main » (une seule fois : main
      ne se rebase pas) ; refusée → main locale remise à son commit d'avant (« git reset --keep ») et refus. Un
      COMMIT refusé (crochet, signature) ne lève rien : « git merge --abort » d'abord, sinon « reset --keep » est
      refusé au milieu d'une fusion et le worktree de main reste en fusion inachevée (N-13 du RELU de Cowork sur
      e7b230083). Le code de l'abandon et du retour est lu : s'il échoue, le refus le DIT au lieu de « remise en
      l'état ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 20-11-2026, étape ③. Pas de « pull --rebase » sur main : une fusion rebasée perdrait sa
      forme, et un tiers qui a poussé sur main doit faire refaire le regard A-818.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Commit et poussée sur main.
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    avant = L.git(wt, "rev-parse", "HEAD").stdout.strip()
    debut = L.maintenant()
    m = L.git(wt, "merge", "--no-ff", "--no-commit", f"origin/{branche}")
    if m.returncode != 0:
        L.git(wt, "merge", "--abort")
        raise L.Arret(REFUS, f"fusion de {branche} en conflit : " + (m.stdout + m.stderr).strip()[-200:])
    try:
        L.noter(wt, "installation", branche, "chat", relue, debut, L.maintenant(), "fusionnée dans main")
        L.git(wt, "add", "--", L.REGISTRE)
        c = L.git(wt, "commit", "-q", "-m", f"Installation de {branche} (pointe relue {relue[:12]}, DÉPLOYABLE par Cowork)")
    except BaseException:   # N-5 : un plantage entre la fusion et le commit ne laisse pas main en fusion inachevée
        L.git(wt, "merge", "--abort")
        raise
    if c.returncode != 0:   # N-13 : un commit refusé laisse la fusion en cours ; seul « merge --abort » la défait
        a = L.git(wt, "merge", "--abort")
        etat = "fusion abandonnée, main locale intacte" if a.returncode == 0 else \
            "ABANDON DE LA FUSION REFUSÉ, worktree de main en fusion inachevée : " + (a.stderr or a.stdout).strip()[:120]
        raise L.Arret(REFUS, f"commit de fusion refusé ({etat}) : " + (c.stderr or c.stdout).strip()[:200])
    p = L.git(wt, "push", "-q", "origin", "HEAD:refs/heads/main")
    if p.returncode != 0:
        k = L.git(wt, "reset", "-q", "--keep", avant)
        etat = "main locale remise en l'état" if k.returncode == 0 else \
            "MAIN LOCALE NON REMISE EN L'ÉTAT : " + (k.stderr or k.stdout).strip()[:120]
        raise L.Arret(REFUS, f"poussée de main refusée, {etat} : " + (p.stderr or p.stdout).strip()[:200])
    return L.git(wt, "rev-parse", "HEAD").stdout.strip()


def republier_apres_installation(racine):
    """Étape ⑤ : lance REPUBLIER, puis REPUBLIER --verifier sur main et un clone public neuf ; rend (code, raison).

    ① RÔLE — Ne rendre 0 que si le public porte le code de main après l'installation (décision de Jean-Luc du
      21-11-2026 à 13h27, réponse « 1 » à N-2).
    ② CONTEXTE D'APPEL — `main`, seulement après une fusion poussée (code INSTALLE).
    ③ ENTRÉE — `racine` : le clone privé.
    ④ CONDITIONS D'ENTRÉE — main poussée ; le worktree jetable de main déjà retiré.
    ⑤ SORTIE — DEUX valeurs : INSTALLE (0) ou PUBLIC_EN_RETARD (4) ; la raison d'un 4 (vide sur 0).
      [rend: 2]
    ⑥ TRAITEMENT — « python3 -B REPUBLIER.py » dans `racine` (publie si et seulement si le public diffère) ; code
      non nul → 4. Puis fetch, worktree NOMMÉ de main (`LIVRER.worktree_nomme`), clone public neuf
      (`LIVRER.cloner_le_public`), « REPUBLIER.py --verifier --fabricant-du-prive <main> <public> » : le fabricant
      DU WORKTREE DE MAIN (`LIVRER.fabricant_de`), celui qui a publié (N-21) ; code non nul → 4. Toute exception
      → 4 : main est déjà poussée, un 1 ou un 5 dirait le faux.
    ⑦ UNITÉ — Secondes (bornes : 7 200 pour publier, 3 600 pour vérifier).
    ⑧ POURQUOI — R-708 : REPUBLIER est le seul code qui publie et qui compare ; INSTALLER le lance, il ne le recopie
      pas. Le --verifier séparé prouve le résultat par la même propriété que le circuit du soir.
    ⑨ CE QUI CLOCHE — Le circuit du soir vérifie avec le fabricant PUBLIÉ ; ici, celui de main : les deux sont le même
      code après une publication prouvée.
    ⑩ EFFET — Peut pousser au public (par REPUBLIER) ; crée puis retire un worktree et un clone sous /tmp.
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné (LIVRER.lancer).
      [sort: non]
    """
    wt, jetable, public = None, False, None
    try:
        r = L.lancer([sys.executable, "-B", REPUBLIER], dossier=racine, borne=7200)
        for ligne in (r.stdout + r.stderr).strip().splitlines()[-8:]:
            L.dire("  REPUBLIER │ " + ligne)
        if r.returncode != 0:
            return PUBLIC_EN_RETARD, f"REPUBLIER a rendu {r.returncode}"
        if L.git(racine, "fetch", "-q", "origin").returncode != 0:
            return PUBLIC_EN_RETARD, "fetch du dépôt privé refusé avant la vérification"
        wt, jetable = L.worktree_nomme(racine, "main")
        public = L.cloner_le_public("main")
        v = L.lancer([sys.executable, "-B", REPUBLIER, "--verifier", "--fabricant-du-prive", wt, public],
                     dossier=racine, borne=3600)
        for ligne in (v.stdout + v.stderr).strip().splitlines()[-4:]:
            L.dire("  REPUBLIER --verifier │ " + ligne)
        if v.returncode != 0:
            return PUBLIC_EN_RETARD, f"REPUBLIER --verifier a rendu {v.returncode}"
        return INSTALLE, ""
    except L.Arret as e:
        return PUBLIC_EN_RETARD, f"vérification impossible : {e.args[1]}"
    except Exception as e:   # noqa: BLE001 — main est poussée : jamais 1 ni 5 ici
        return PUBLIC_EN_RETARD, f"{type(e).__name__} : {e}"
    finally:
        if wt and jetable:
            L.retirer_worktree(racine, wt)
        if public:
            shutil.rmtree(public, ignore_errors=True)


def main():
    """Enchaîne les étapes de l'installation ; sort avec son code.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv : la branche.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — Rien : sort (0, 1, 3, 4 ou 5).
      [rend: rien]
    ⑥ TRAITEMENT — Voir l'en-tête. Toute exception autre qu'un arrêt prévu sort en 5 (PLANTAGE), jamais en 1 : après
      la poussée de main, un 1 dirait « rien installé » à tort (défaut bloquant du relecteur du 20-11-2026).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Sort du programme par sys.exit.
      [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not re.match(r"^travail-[A-Za-z0-9._-]+$", args[0]):
        L.dire("usage : INSTALLER.py <branche travail-…>")
        sys.exit(REFUS)
    branche, racine = args[0], os.getcwd()
    wt, jetable, code = None, False, REFUS
    try:
        try:
            if L.git(racine, "fetch", "-q", "origin").returncode != 0:
                raise L.Arret(REFUS, "fetch du dépôt privé refusé")
            relue = juger_le_relu(racine, branche)
            L.dire(f"ÉTAPE 1 — RELU de Cowork : DÉPLOYABLE, pointe relue {relue[:12]}")
            prouves = prouver_les_epreuves(racine, relue)
            L.dire("ÉTAPE 2 — preuve GitHub : " + (" · ".join(f"{c} passage {n} code 0" for c, n in prouves)
                                                   or "aucune épreuve longue déclarée à la pointe relue"))
            try:
                occupes = passages_en_cours(racine)
            except L.Arret as e:
                raise L.Arret(REESSAYER, "passages illisibles, rien n'est installé : " + e.args[1])
            if occupes:
                raise L.Arret(REESSAYER, f"{len(occupes)} passage(s) en cours ou en attente (A-818) : "
                                         + " ; ".join(occupes[:3]))
            L.dire("ÉTAPE 3 — aucun passage en cours ni en attente (A-818)")
            wt, jetable = worktree_de_main(racine)
            fusion = fusionner(wt, branche, relue)
            code = INSTALLE
            L.dire(f"ÉTAPE 4 — main = {fusion[:12]}, poussée")
        except L.Arret as e:
            code = e.args[0]
            L.dire(f"ARRÊT (code {code}) — {e.args[1]}")
        except Exception as e:   # noqa: BLE001 — un plantage n'est jamais lu comme un refus
            code = PLANTAGE
            L.dire(f"PLANTAGE (code {PLANTAGE}) — {type(e).__name__} : {e}")
            L.dire(traceback.format_exc().rstrip())
        finally:
            if wt and jetable:
                L.retirer_worktree(racine, wt)
    except Exception as e:   # noqa: BLE001 — même règle pendant le rangement
        code = PLANTAGE
        L.dire(f"PLANTAGE (code {PLANTAGE}) pendant le rangement — {type(e).__name__} : {e}")
    raison = ""
    if code == INSTALLE:
        L.dire("ÉTAPE 5 — republication enchaînée (décision de Jean-Luc du 21-11-2026 à 13h27)")
        code, raison = republier_apres_installation(racine)
    L.dire({INSTALLE: "INSTALLÉ (code 0) — main installé, public à jour (REPUBLIER --verifier : égal)",
            PUBLIC_EN_RETARD: f"main installé, public EN RETARD : lancer REPUBLIER (code {PUBLIC_EN_RETARD}, {raison}) "
                              f"— commande exacte : cd {racine} && {L.commande_de_republication(racine)}",
            REFUS: "REFUSÉ (code 1) : rien n'est installé",
            REESSAYER: "RÉESSAYER (code 3) : rien n'est installé",
            PLANTAGE: "PLANTAGE (code 5) : ni verdict ni refus — relire origin/main ET « git status » du worktree de "
                      "main avant tout autre geste"}[code])
    sys.exit(code)


if __name__ == "__main__":
    main()
