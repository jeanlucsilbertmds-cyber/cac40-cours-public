#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ADAPTATEUR_PILOTAGE_CAC40.py — l'adaptateur du projet CAC 40 pour PILOTER_UN_PLANNING.py. Mer 25-11-2026.
Simulation uniquement : aucun ordre réel, jamais.

① RÔLE — Dire au cœur générique (programmes/PILOTER_UN_PLANNING.py) l'état RÉEL de chaque étape du planning dont la
  preuve est « branche:<nom> », et l'occupation des machines GitHub ; préparer les contrôles du passage
  (rattachement à une décision, comptage des défauts du RELU).
② CONTEXTE D'APPEL — Chargé par le cœur quand planning.csv porte « adaptateur;<chemin de ce fichier> » ; jamais
  lancé seul.
③ ENTRÉE — `observer(planning, racine, params)`. Paramètres lus (planning.csv ou --param) : depot (le clone du dépôt
  privé ; défaut : racine) · gh (programme gh ; défaut « gh ») · public (« propriétaire/nom » du dépôt public ;
  défaut celui de programmes/ETAT_DES_TRAVAUX.py) · backlog (chemin du BACKLOG pour le rattachement ; absent = pas
  de contrôle de rattachement). Les RÔLES des ressources se lisent dans la colonne « mesure » de ressources.csv,
  jamais dans ce code : « machines » (largeur publiée, places prises) · « relais <fiche des passages> <fiche du
  relais> » (passages vivants de la première fiche, refus du relais lus dans les journaux de la seconde ; reçoit
  aussi les étapes À ÉPROUVER et EN ÉPREUVE) · « relecture » (reçoit les étapes À RELIRE). Exemple réel
  (planning/PLAN_V8/ressources.csv) : « relais epreuves_longues.yml demande_de_serie.yml ».
④ CONDITIONS D'ENTRÉE — Le clone a ses références origin/* à jour (le cœur ne fait pas de fetch : celui qui pilote
  le fait avant, A-1016) ; programmes/ETAT_DES_TRAVAUX.py est dans le même dossier que ce fichier.
⑤ SORTIE — DEUX valeurs (contrat du cœur) : {étape: {etat, action, ressource, phase, detail}} — `phase` : l'état
  rangé et, pour un état de la table PRODUIT_DE_L_EXECUTANT, le DERNIER COMMIT (depuis la base de la branche sur
  main ; « — » s'il n'y en a pas) du fichier que l'EXÉCUTANT de cet état doit produire : À RELIRE → echanges/RELU.md
  (le relecteur), ÉCRITURE → echanges/A_RELIRE.md (l'auteur) ; JAMAIS la pointe. Le cœur s'en sert pour terminer un
  lancement : seul ce que son exécutant produit, ou un changement d'état rangé, le termine ; un commit sans rapport
  ou la note corrigée par son auteur pendant une relecture, non (N-71 du RELU Cowork du 25-11-2026, 23h29 ; N-79 du
  RELU du 26-11-2026, 00h14 ; superviseur R-759 tours 3 et 5) · {ressource: {occupees,
  capacite?, detail}} ; et la liste de module CONTROLES_DU_PASSAGE remplie.
⑥ TRAITEMENT — Pour chaque étape « branche:<nom> » : branche absente → a_faire (« créer la branche ») ; marque
  echanges/EN_COURS* présente sur la pointe → en_cours ; sinon l'état et l'action viennent de ETAT_DES_TRAVAUX.ranger
  (APPELÉ, jamais recopié — R-708) et sont traduits : INSTALLÉE → fait · EN ÉPREUVE → en_cours sur la ressource
  des épreuves · À ÉPROUVER → a_faire sur la ressource des épreuves · À RELIRE → a_faire sur la ressource de
  relecture · ÉCRITURE, ÉPREUVE ROUGE, DÉPLOYABLE → a_faire sur la ressource déclarée de l'étape. Ressources : les
  passages vivants du circuit des épreuves longues (gh run list --workflow) occupent le relais ; les places prises
  par ETAT_DES_TRAVAUX.passages_github occupent les machines, dont la capacité mesurée est la largeur publiée.
  Refus : chaque passage ÉCHOUÉ du relais (gh run list --status failure) dont le journal des étapes échouées
  porte « DEMANDE REFUSEE » et « en cours ou en attente » donne son heure ; la liste de ces heures est le CUMUL
  horodaté rendu au cœur. gh illisible → occupation None et refus None (« mesure impossible », jamais 0) : le cœur
  ne lance alors rien sur ces ressources et rend le code 4.
⑦ UNITÉ — Places (une place = une machine GitHub ou un passage du relais).
⑧ POURQUOI — A-1017 (Jean-Luc, 25-11-2026 20h52) : un cœur générique et des adaptateurs par projet ; fait mesuré le
  25-11-2026 au soir (consigne du Chat) : le relais du dépôt public REFUSE une demande quand 3 passages
  epreuves_longues.yml sont en cours ou en attente.
⑨ CE QUI CLOCHE — (a) Une marque EN_COURS oubliée garde l'étape « en cours » pour toujours : aucune péremption
  ici. (b) Sans gh, une branche EN ÉPREUVE est vue « À ÉPROUVER » ; elle n'est pas relancée pour autant, car la
  ressource des épreuves est alors « mesure impossible ». (c) « DÉPLOYABLE » n'est pas « fait » : l'installation sur
  main est une action (A-818 : quand rien ne tourne sur GitHub), à la ressource déclarée. (d) ETAT_DES_TRAVAUX lit
  l'heure de la note et du RELU sur la branche, pas la ligne « SERT : » : le rattachement est le contrôle
  VERIFIER_LE_RATTACHEMENT. (f) ETAT_DES_TRAVAUX range INSTALLÉE une branche dont le code égale celui de sa base
  (son ⑨ b) : une branche neuve qui ne porte qu'une marque ou une note serait « faite ». Ici, INSTALLÉE n'est
  retenu que si la pointe est DANS main (aucun commit hors de main) ; sinon l'étape est à écrire. Conséquence
  connue : une branche fusionnée puis complétée d'une note est vue « à écrire » jusqu'à sa suppression.
  (g) Une marque EN_COURS l'emporte sur tout autre état. (h) Les contrôles (défauts, rattachement) ne lisent que
  la note et les RELU écrits SUR la branche (après sa base sur main) : une note héritée de main n'est pas la sienne ;
  le RELU « précédent » est l'avant-dernière version écrite sur la branche, absente au premier RELU. Les étapes en
  pause déclarée ne sont pas contrôlées. (e) Les fichiers temporaires des contrôles (notes et RELU extraits) sont effacés à la
  sortie du programme (atexit), pas avant.
  (i) Seuls les refus « en cours ou en attente » (file pleine) sont comptés : un refus pour une demande mal
  formée (« cle inconnue ») ne dit rien de la place, et ne fait pas reculer le palier. Seuls les 20 derniers passages
  échoués du relais sont lus. (j) VERIFIER_LE_RATTACHEMENT.py et RELEVER_LES_BLOCAGES.py vivent sur travail-carte,
  non installée : absents du dépôt, ils sont déclarés IMPOSSIBLES (étape I_CARTE du Plan V8), jamais exécutés depuis
  une autre branche (jugement du superviseur R-759 du 25-11-2026 : ce serait contourner la relecture).
  (k) La `phase` ignore les commits de code : une étape lancée en ÉCRITURE dont l'agent pousse du code sans marque
  EN_COURS ni note reste « lancée non confirmée » jusqu'à sa note (ou au changement d'état rangé), et devient une
  fois À VÉRIFIER après le délai — sens sûr (rien n'est relancé), au prix d'une alerte (N-71).
⑩ EFFET — Lance git et gh (lecture seule) ; écrit des copies de notes et de RELU dans un dossier temporaire.
⑪ TERMINAISON — Chaque appel git ou gh est borné par ETAT_DES_TRAVAUX.DELAI_S ; revient toujours.
"""
import atexit
import json
import os
import shutil
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import ETAT_DES_TRAVAUX as E  # noqa: E402  (programme du dépôt, appelé et jamais recopié — R-708)

CONTROLES_DU_PASSAGE = []
PREUVES_LUES = ("branche:",)
NOMBRE_DE_REFUS_LUS = 20
# N-79 (RELU Cowork du 26-11-2026, 00h14 ; superviseur R-759 tour 5) : LA table unique de ce que l'EXÉCUTANT d'un
# lancement doit produire, selon l'état rangé de la branche. Un lancement ne prend fin que quand ce fichier reçoit un
# commit, ou quand l'état rangé change ; jamais sur le geste d'un autre (la note corrigée par son auteur pendant que
# Cowork relit n'est pas le geste du relecteur). États absents de la table : l'état rangé seul.
PRODUIT_DE_L_EXECUTANT = {"À RELIRE": "echanges/RELU.md", "ÉCRITURE": "echanges/A_RELIRE.md"}
TRADUCTION = {"INSTALLÉE": "fait", "EN ÉPREUVE": "en_cours", "À ÉPROUVER": "a_faire", "À RELIRE": "a_faire",
              "ÉCRITURE": "a_faire", "ÉPREUVE ROUGE": "a_faire", "DÉPLOYABLE": "a_faire"}


def marques_en_cours(depot, branche):
    """Rend les marques echanges/EN_COURS* sur la pointe d'une branche.

    ① RÔLE — Voir qu'un agent travaille sur la branche.
    ② CONTEXTE D'APPEL — `observer`, une fois par branche.
    ③ ENTRÉE — `depot` : le clone ; `branche` : le nom sans « origin/ ».
    ④ CONDITIONS D'ENTRÉE — origin/<branche> existe.
    ⑤ SORTIE — UNE valeur : la liste des chemins des marques.
      [rend: 1]
    ⑥ TRAITEMENT — git ls-tree du dossier echanges/ ; garder les noms qui commencent par EN_COURS.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un agent pose sa marque avant d'écrire et la retire à la fin (consigne des agents).
    ⑨ CE QUI CLOCHE — aucune péremption : une marque oubliée dure.
    ⑩ EFFET — lance git.
    ⑪ TERMINAISON — bornée par ETAT_DES_TRAVAUX.DELAI_S ; lève E.Impossible si git échoue.
      [sort: non]
    """
    sortie = E.git(depot, "ls-tree", "--name-only", f"origin/{branche}", "echanges/")
    return [l for l in sortie.splitlines() if os.path.basename(l).startswith("EN_COURS")]


def existe(depot, branche):
    """Dit si origin/<branche> existe.

    ① RÔLE — Distinguer une étape pas commencée d'une étape en cours d'écriture.
    ② CONTEXTE D'APPEL — `observer`, une fois par étape « branche: ».
    ③ ENTRÉE — `depot` : le clone ; `branche` : le nom sans « origin/ ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si la référence existe.
      [rend: 1]
    ⑥ TRAITEMENT — git for-each-ref (rend vide si absente, sans erreur).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — git show sur une branche absente lèverait, et arrêterait tout le passage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lance git.
    ⑪ TERMINAISON — bornée par ETAT_DES_TRAVAUX.DELAI_S.
      [sort: non]
    """
    return bool(E.git(depot, "for-each-ref", "--format=%(refname)", f"refs/remotes/origin/{branche}").strip())


def relais_occupe(gh, public, fiche):
    """① RÔLE — Compter les passages du circuit des épreuves longues en cours ou en attente.
    ② CONTEXTE D'APPEL — `observer`, une fois.
    ③ ENTRÉE — `gh` ; `public` ; `fiche` (nom du fichier du circuit).
    ④ CONDITIONS D'ENTRÉE — gh authentifié pour le dépôt public.
    ⑤ SORTIE — UNE valeur : le nombre de passages dont le statut n'est pas « completed ».
      [rend: 1]
    ⑥ TRAITEMENT — gh run list --workflow <fiche> --limit 50 --json status.
    ⑦ UNITÉ — des passages.
    ⑧ POURQUOI — fait mesuré le 25-11-2026 au soir : le relais refuse une demande à 3 passages en cours ou en attente.
    ⑨ CE QUI CLOCHE — au-delà de 50 passages récents, un passage vivant plus ancien n'est pas vu.
    ⑩ EFFET — lance gh.
    ⑪ TERMINAISON — bornée ; lève E.Impossible si gh échoue ou ne rend pas du JSON.
      [sort: non]
    """
    try:
        passages = json.loads(E.commande([gh, "run", "list", "-R", public, "--workflow", fiche, "--limit", "50",
                                          "--json", "status"]))
    except ValueError:
        raise E.Impossible("gh run list --workflow : réponse qui n'est pas du JSON")
    return sum(1 for p in passages if p.get("status") != "completed")


def refus_du_relais(gh, public, fiche_relais):
    """① RÔLE — Rendre le CUMUL horodaté des refus « file pleine » du relais.
    ② CONTEXTE D'APPEL — `observer`, une fois, pour la ressource dont la mesure est « relais … ».
    ③ ENTRÉE — `gh` ; `public` ; `fiche_relais` (nom du fichier du circuit relais, par exemple demande_de_serie.yml).
    ④ CONDITIONS D'ENTRÉE — gh authentifié pour le dépôt public.
    ⑤ SORTIE — UNE valeur : la liste des heures ISO (createdAt de GitHub) des passages échoués dont le journal porte
      « DEMANDE REFUSEE » et « en cours ou en attente ».
      [rend: 1]
    ⑥ TRAITEMENT — gh run list --status failure --limit NOMBRE_DE_REFUS_LUS ; pour chacun, gh run view --log-failed.
    ⑦ UNITÉ — des heures.
    ⑧ POURQUOI — D4 de la relecture du 25-11-2026 et jugement du superviseur R-759 : le recul du palier ne doit lire
      que l'OBSERVABLE (les refus écrits par le relais dans ses journaux), en cumul horodaté ; illisible = mesure
      impossible, jamais 0. Même phrase que celle que programmes/LIVRER.py lit pour reconnaître ce refus.
    ⑨ CE QUI CLOCHE — voir ⑨ i du module ; un journal effacé par GitHub (rétention) fait disparaître le refus de la
      liste, ce qui ne fait pas remonter le palier (le cœur compare à la dernière heure vue).
    ⑩ EFFET — lance gh.
    ⑪ TERMINAISON — chaque appel borné par ETAT_DES_TRAVAUX.DELAI_S ; lève E.Impossible si gh échoue ou ne rend pas
      du JSON.
      [sort: non]
    """
    try:
        echecs = json.loads(E.commande([gh, "run", "list", "-R", public, "--workflow", fiche_relais, "--status",
                                        "failure", "--limit", str(NOMBRE_DE_REFUS_LUS), "--json", "databaseId,createdAt"]))
    except ValueError:
        raise E.Impossible("gh run list --status failure : réponse qui n'est pas du JSON")
    heures = []
    for p in echecs:
        journal = E.commande([gh, "run", "view", str(p["databaseId"]), "-R", public, "--log-failed"])
        if "DEMANDE REFUSEE" in journal and "en cours ou en attente" in journal:
            heures.append(p["createdAt"])
    return heures


def phase_observee(etat_txt, empreinte):
    """① RÔLE — Fabriquer la `phase` d'une étape : l'état rangé et, s'il en a un, l'EMPREINTE DU CONTENU de ce que
      l'exécutant de cet état doit produire (table PRODUIT_DE_L_EXECUTANT).
    ② CONTEXTE D'APPEL — `observer`, une fois par étape rangée hors marque EN_COURS.
    ③ ENTRÉE — `etat_txt` : l'état rangé par ETAT_DES_TRAVAUX.ranger ; `empreinte` : fonction qui rend, pour un
      chemin de fichier, le nom d'objet git de son CONTENU à la pointe de la branche — le même que
      `git rev-parse origin/<b>:<chemin>` (« » si le fichier n'y est pas).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « [<état>] » ou « [<état>] <fichier> <empreinte ou —> ».
      [rend: 1]
    ⑥ TRAITEMENT — l'état entre TOUJOURS ; le fichier produit seulement si l'état est dans la table.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-79 : la phase portait aussi le commit de la note ; l'auteur qui corrige sa note pendant la
      relecture « confirmait » la relecture, qui était redite LANCER. N-81 : rien ne gardait l'état dans la phase.
      N-86 (RELU Cowork du 26-11-2026, 01h21 ; superviseur R-759 avant le tour 6) : la phase portait le dernier
      COMMIT du produit ; un rebase de l'auteur pendant la relecture réécrit ce commit (même contenu, autre nom) et
      la relecture était redite LANCER. Le contenu ne change pas au rebase : son empreinte non plus.
    ⑨ CE QUI CLOCHE — un exécutant qui produit sans commit (un RELU non poussé) n'est pas vu : son lancement reste
      non confirmé jusqu'à À VÉRIFIER ou ENQUÊTER (sens sûr : rien n'est relancé). N-86 R2, consigné et NON réparé
      (jugement du superviseur : pas de rustine) : une fusion de main qui CHANGE le produit pendant la relecture
      (main porte un autre RELU, conflit résolu côté main) change vraiment le contenu, sans être le geste de
      l'exécutant : la relecture est redite LANCER, et c'est notifié (cas rare, sens sûr). Un produit identique à
      celui de main donne une empreinte non vide sans geste de l'exécutant : sans effet, seule la VARIATION compte.
      Un état écrit avant le tour 6 garde un nom de COMMIT dans l'observation de ses lancements : au premier
      passage, une étape dont le produit existe voit sa phase changer une fois (lancement terminé, une redite
      possible, notifiée).
    ⑩ EFFET — ceux de `empreinte` (git).
    ⑪ TERMINAISON — celle de `empreinte`.
      [sort: non]
    """
    fichier = PRODUIT_DE_L_EXECUTANT.get(etat_txt)
    if fichier is None:
        return f"[{etat_txt}]"
    return f"[{etat_txt}] {fichier} {empreinte(fichier) or '—'}"


def roles(planning):
    """① RÔLE — Lire le rôle de chaque ressource dans la colonne « mesure » de ressources.csv.
    ② CONTEXTE D'APPEL — `observer`, une fois.
    ③ ENTRÉE — `planning` (valeur de lire_planning du cœur).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {rôle: (ressource, arguments)} pour les rôles machines, relais, relecture.
      [rend: 1]
    ⑥ TRAITEMENT — premier mot de la case = rôle ; la suite = arguments ; un rôle inconnu ou en double, ou un relais
      sans ses deux fiches, lève ValueError (le cœur en fait un ARRET).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — mineur 15 de la relecture du 25-11-2026 : les noms de ressources et de fiches étaient écrits en dur
      ici, recopie de ressources.csv (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours, ou lève ValueError.
      [sort: non]
    """
    out = {}
    for r, l in planning["ressources"].items():
        mots = l.get("mesure", "").split()
        if not mots:
            continue
        if mots[0] not in ("machines", "relais", "relecture") or mots[0] in out:
            raise ValueError(f"mesure de {r} : rôle inconnu ou en double « {mots[0]} »")
        if mots[0] == "relais" and len(mots) != 3:
            raise ValueError(f"mesure de {r} : « relais <fiche des passages> <fiche du relais> » attendu")
        out[mots[0]] = (r, mots[1:])
    return out


def observer(planning, racine, params):
    """Rend l'état réel des étapes du planning et la mesure des ressources, pour le cœur.

    ① RÔLE — Voir ① du module.
    ② CONTEXTE D'APPEL — le cœur (PILOTER_UN_PLANNING.observer), une fois par passage.
    ③ ENTRÉE — `planning` : la valeur de lire_planning du cœur ; `racine` : dossier de base ; `params` : les
      paramètres du planning (voir ③ du module).
    ④ CONDITIONS D'ENTRÉE — voir ④ du module.
    ⑤ SORTIE — DEUX valeurs : observations des étapes, mesures des ressources (voir ⑤ du module).
      [rend: 2]
    ⑥ TRAITEMENT — voir ⑥ du module.
    ⑦ UNITÉ — places.
    ⑧ POURQUOI — voir ⑧ du module.
    ⑨ CE QUI CLOCHE — voir ⑨ du module.
    ⑩ EFFET — voir ⑩ du module.
    ⑪ TERMINAISON — voir ⑪ du module.
      [sort: non]
    """
    depot = params.get("depot") or racine
    gh = params.get("gh", "gh")
    public = params.get("public", E.PUBLIC_PAR_DEFAUT)
    rol = roles(planning)
    r_mach = rol.get("machines", (None,))[0]
    r_ep, fiches = rol.get("relais", (None, [None, None]))
    r_rel = rol.get("relecture", (None,))[0]
    del CONTROLES_DU_PASSAGE[:]
    resultats, _ = E.resultats_github(depot)
    mesures, vivants = {}, []
    if r_mach:
        try:
            lu = E.largeur_publiee(depot)
            vivants, occupees = E.passages_github(gh, public, lu["fiches_longues"])
            mesures[r_mach] = {"occupees": occupees, "capacite": lu["largeur"],
                               "detail": f"largeur publiée {lu['largeur']}, places prises {occupees}"}
        except E.Impossible as e:
            mesures[r_mach] = {"occupees": None, "detail": f"gh ou journal illisible : {e}"}
            vivants = []
    if r_ep:
        mesures[r_ep] = {}
        try:
            n = relais_occupe(gh, public, fiches[0])
            mesures[r_ep].update(occupees=n, detail=f"{n} passage(s) de {fiches[0]} en cours ou en attente")
        except E.Impossible as e:
            mesures[r_ep].update(occupees=None, detail=f"gh illisible : {e}")
        try:
            mesures[r_ep]["refus"] = refus_du_relais(gh, public, fiches[1])
        except E.Impossible as e:
            mesures[r_ep]["refus"] = None
            mesures[r_ep]["detail"] += f" · refus de {fiches[1]} illisibles : {e}"
    tmp = tempfile.mkdtemp(prefix="pilotage_cac40_")
    atexit.register(shutil.rmtree, tmp, True)
    notes, obs = [], {}
    for e, l in planning["etapes"].items():
        if not l["preuve"].startswith("branche:"):
            continue
        b = l["preuve"][len("branche:"):].strip()
        if not existe(depot, b):
            obs[e] = {"etat": "a_faire", "action": f"créer {b} et écrire : {l['libelle']}",
                      "detail": f"origin/{b} absente"}
            continue
        marques = marques_en_cours(depot, b)
        faits = E.faits_d_une_branche(depot, b, resultats, vivants)
        base = E.git(depot, "merge-base", f"origin/{b}", "origin/main").strip()
        ecrite = E.git(depot, "log", "-1", "--format=%H", f"{base}..origin/{b}", "--", "echanges/A_RELIRE.md").strip()
        etat_txt, action = E.ranger(faits)
        hors_main = int(E.git(depot, "rev-list", "--count", f"origin/main..origin/{b}").strip() or 0)
        if etat_txt == "INSTALLÉE" and hors_main:
            # même code que main, mais des commits hors de main : rien d'écrit au-delà des notes (⑨ f)
            etat_txt, action = "ÉCRITURE", ("la branche ne porte que des notes (echanges/, archives/) : écrire, ou "
                                            "reprendre selon le RELU" + (f" (verdict : « {faits['verdict'][:70]} »)"
                                                                         if faits.get("verdict") else ""))
        # N-83 : la ressource de l'état rangé se calcule AVANT la marque ; une marque posée sur une branche À RELIRE
        # porte donc « relecteur » : l'observation porte toujours la ressource de l'état rangé.
        ress = {"EN ÉPREUVE": r_ep, "À ÉPROUVER": r_ep, "À RELIRE": r_rel}.get(etat_txt) or l["ressource"]
        if marques:
            obs[e] = {"etat": "en_cours", "ressource": ress,
                      "detail": f"{b} : marque {', '.join(marques)} (pointe {faits['pointe'][:9]})"}
        else:
            obs[e] = {"etat": TRADUCTION[etat_txt], "action": f"{b} [{etat_txt}] : {action}",
                      "ressource": ress,
                      "phase": phase_observee(etat_txt, lambda f, b=b: (E.git(
                          depot, "ls-tree", f"origin/{b}", "--", f).split() + ["", "", ""])[2]),
                      "detail": f"{b} [{etat_txt}] pointe {faits['pointe'][:9]}"}
        if etat_txt == "INSTALLÉE" or (l["etat"].startswith("pause") and obs[e]["etat"] == "a_faire"):
            continue   # contrôles sur le travail vivant : une pause déclarée ET observée inactive ne fait pas de bruit
        note = E.git(depot, "show", f"origin/{b}:echanges/A_RELIRE.md") if ecrite else None
        if note is not None:
            c = os.path.join(tmp, f"{e}_A_RELIRE.md")
            open(c, "w", encoding="utf-8").write(note)
            notes.append(f"{e}={c}")
        versions = E.git(depot, "log", "-2", "--format=%H", f"{base}..origin/{b}", "--", "echanges/RELU.md").split()
        if versions:
            chemins = []
            for k, v in enumerate(versions):
                c = os.path.join(tmp, f"{e}_RELU_{k}.md")
                open(c, "w", encoding="utf-8").write(E.git(depot, "show", f"{v}:echanges/RELU.md"))
                chemins.append(c)
            CONTROLES_DU_PASSAGE.append((f"défauts {e}", [sys.executable, "-I", os.path.join(ICI, "COMPTER_LES_DEFAUTS.py")] + chemins))
    for nom, programme, args in (("rattachement", "VERIFIER_LE_RATTACHEMENT.py", notes),
                                 ("blocages", "RELEVER_LES_BLOCAGES.py", [])):
        if not params.get("backlog") or (nom == "rattachement" and not notes):
            continue
        chemin = os.path.join(ICI, programme)
        if not os.path.isfile(chemin):
            CONTROLES_DU_PASSAGE.append((nom, None, f"{programme} absent de ce dépôt : il vit sur travail-carte, non "
                                                    "installée (étape I_CARTE du planning)"))
        else:
            CONTROLES_DU_PASSAGE.append((nom, [sys.executable, "-I", chemin, params["backlog"]] + args))
    return obs, mesures
