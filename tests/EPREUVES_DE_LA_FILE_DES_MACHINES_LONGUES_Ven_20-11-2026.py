#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_FILE_DES_MACHINES_LONGUES — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Décisions de Jean-Luc : A-884 ② (17-11-2026 à 22h00 : le garde « un circuit à la fois » est d'abord
MESURÉ, puis remplacé par une protection plus fine, jamais supprimé sans remplacement) ; A-888 (17-11-2026 à 22h30 :
« 18 calculs en parallèle au plus, et 2 places toujours libres pour le circuit du soir et le relais ») ; le 20-11-2026 à
20h52 : « Pourquoi on ne fait pas tous les 20… tout ce qui est parallélisable ». Ce soir-là, le relais des demandes
(.github/workflows/demande_de_serie.yml du dépôt public, fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py)
refusait toute demande dès qu'un passage long était en cours : contrat-6 n'occupait que 2 places sur 18, et
proprietes-6 était refusé. L'étape FILE-2 remplace ce refus global par UN réservoir de 18 places (un groupe de
concurrence par JOB, « place-longue-<k> ») et par trois protections fines. Cette épreuve garde les QUATRE propriétés
qui le traduisent, chacune avec un sabotage qui doit la faire rougir.

① RÔLE — Éprouver, sur les circuits que le fabricant écrit vraiment : F1 le relais ne refuse plus une demande pour un
  passage en cours ; F2 la protection fine (un groupe de passage par branche, en file, et chaque job sur une place
  bornée) ; F3 les poussées des résultats au dépôt privé se répètent (« git pull --rebase » puis nouvel essai) ;
  F4 la somme des circuits qui n'attendent pas reste au plus 20, dont 2 places hors du réservoir.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, avec la racine, puis avec --saboter) ; sur
  GitHub par le circuit des épreuves longues (code « File » de tests/LANCEMENT_DES_EPREUVES.json) ; à la main :
  python3 tests/EPREUVES_DE_LA_FILE_DES_MACHINES_LONGUES_Ven_20-11-2026.py <racine> [--saboter | --saboter=SF1,…]
③ ENTRÉE — La racine d'un dépôt : programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, programmes/FORME_D_UN_JETON.py,
  tests/LANCEMENT_DES_EPREUVES.json, .github/workflows/collecte_abc.yml.
④ CONDITIONS D'ENTRÉE — bash, git et jq installés (le relais et le placement les emploient, comme sur GitHub) ; sans
  eux, le cas est FAUX (un contrôle qui n'a pas pu tourner ne passe pas, R-734).
⑤ SORTIE — Le code de sortie : 0 si chaque cas donne la réponse attendue et, avec --saboter, si chaque sabotage en fait
  échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT —
  F1 (le relais, joué) : le pas « relayer » du relais fabriqué, joué par bash sur une poussée imitée (un dépôt git
  jetable : un commit qui AJOUTE demandes/DEMANDE_2026-11-20_21h00.txt, « circuit=epreuve », deux codes de la table),
  avec un faux gh qui répond trois passages EN COURS, un par circuit long, chacun « places 1+18 » (le réservoir
  plein) : le pas rend 0 et appuie UNE fois sur le bouton des épreuves, avec « premiere_place » et
  « nombre_de_places=2 ».
  F2 (la protection fine, lue sur les fiches) : les circuits des épreuves longues et des séries portent un groupe de
  PASSAGE nommé par la branche (« ${{ github.ref_name }} », seule expression), avec « queue: max » et sans
  « cancel-in-progress: true » ; les trois circuits longs sont des fiches du réservoir (`largeur_d_une_fiche` rend
  RESERVOIR_DES_PLACES : chaque job sur une place bornée, en file) ; `refus_de_la_file` ne rend aucun refus.
  F3 (les poussées, jouées) : dans le pas « deposer » du circuit des épreuves longues et du job « jouer » des séries,
  les lignes de la boucle d'essais (de « for essai in » à l'erreur finale) sont jouées par bash dans un dépôt git
  jetable dont l'origine est un dépôt nu qui REFUSE la première poussée (crochet « pre-receive ») : la boucle rend 0,
  au DEUXIÈME essai, et la branche du passage existe à l'origine. La boucle compte ESSAIS_DE_POUSSEE_SUR_SA_BRANCHE
  essais, au moins 2.
  F4 (la largeur) : `refus_de_la_largeur` sur les fiches fabriquées ne rend aucun refus, et le total qu'il affiche vaut
  2 + PLACES_LONGUES, au plus TACHES_EN_MEME_TEMPS_DU_COMPTE.
  Sabotages (--saboter), chacun sur une copie des fichiers lus, chacun doit faire rougir au moins un cas :
  SF1 remettre le refus global au relais ; SF2 retirer le groupe de passage par branche des épreuves longues ;
  SF3 retirer les nouveaux essais de poussée (une seule poussée, sans reprise) ; SF4 dépasser 20 (19 places) ;
  SF5 une boucle d'essais qui sort au premier refus (seule la partie jouée de F3 peut le voir).
⑦ UNITÉ — Des tâches de GitHub ; des codes de sortie.
⑧ POURQUOI — R-731 : tout code écrit a ses épreuves au dépôt, avec des sabotages qui mordent chacun pour sa raison ;
  la consigne de l'étape FILE-2 (20-11-2026) nomme ces quatre sabotages.
⑨ CE QUI CLOCHE — Ce que fait GitHub n'est imité nulle part : un groupe de concurrence de JOB avec « queue: max »,
  un job en attente sur sa place qui ne prend aucune machine, les jobs au-delà de 18 mis en file : THÉORIQUE tant
  qu'un passage réel ne l'a pas montré (commentaire de PLACES_LONGUES du fabricant). F1 imite gh ; F3 imite un refus
  passager par un crochet, pas une panne réelle de GitHub.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
JETON = "programmes/FORME_D_UN_JETON.py"     # chargé par le fabricant, à côté de lui
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
CIRCUIT_PRIVE = ".github/workflows/collecte_abc.yml"
LUS = (FABRICANT, JETON, TABLE, CIRCUIT_PRIVE)
NOM_DE_DEMANDE = "demandes/DEMANDE_2026-11-20_21h00.txt"
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GIT_ENV.update(GIT_AUTHOR_NAME="essai", GIT_AUTHOR_EMAIL="essai@local", GIT_COMMITTER_NAME="essai",
               GIT_COMMITTER_EMAIL="essai@local", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
# Le faux gh : « run list » rend les passages imités passés par le filtre « --jq » reçu (appliqué par jq, comme gh) ;
# « workflow run » est seulement noté au journal.
FAUX_GH = '''#!/usr/bin/env python3
import json, os, subprocess, sys
a = sys.argv[1:]
with open(os.environ["FAUX_GH_JOURNAL"], "a", encoding="utf-8") as f:
    f.write(json.dumps(a) + "\\n")
if a[:2] == ["run", "list"]:
    passages = json.loads(os.environ.get("FAUX_GH_PASSAGES", "[]"))
    p = subprocess.run(["jq", "-r", a[a.index("--jq") + 1]], input=json.dumps(passages), capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.exit(p.returncode)
'''


def lancer(args, cwd=None, env=None):
    """Lance une commande ; rend (code, sortie et erreurs réunies).

    ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `args`, `cwd`, `env`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, le texte. [rend: 2] ⑥ TRAITEMENT — subprocess, 300 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : rangé parmi les cas faux.
    ⑩ EFFET — Ce que fait la commande. ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env, timeout=300, errors="replace")
    return p.returncode, p.stdout + p.stderr


def charger(chemin, nom):
    """Charge un programme comme un module, par son chemin.

    ① RÔLE — Appeler les fonctions de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Le code de tête du programme s'exécute. ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pas_du_gabarit(texte, ident):
    """Rend (environnement brut, script) du premier pas d'identifiant `ident` d'un circuit fabriqué.

    ① RÔLE — Extraire un pas pour le jouer. ② CONTEXTE D'APPEL — `tour` (F1, F3). ③ ENTRÉE — le texte, l'identifiant.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : {nom : valeur brute} du bloc « env: », le script (texte
      désindenté) ; (None, "") si le pas manque. [rend: 2]
    ⑥ TRAITEMENT — la ligne « id: <ident> », puis le bloc « env: » à sa marge, puis « run: | » et les lignes plus
      indentées que lui. ⑦ UNITÉ — — ⑧ POURQUOI — Jouer le texte FABRIQUÉ, pas une copie.
    ⑨ CE QUI CLOCHE — Lecture par l'indentation, pas par yaml (même limite que le fabricant). ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = texte.split("\n")
    debut = [i for i, l in enumerate(lignes) if l.strip() == "id: " + ident]
    if not debut:
        return None, ""
    i = debut[0]
    marge = len(lignes[i]) - len(lignes[i].lstrip())
    env = {}
    while i < len(lignes) and lignes[i].strip() != "run: |":
        if lignes[i].strip() == "env:" and len(lignes[i]) - len(lignes[i].lstrip()) == marge:
            k = i + 1
            while k < len(lignes) and len(lignes[k]) - len(lignes[k].lstrip()) > marge:
                nom, _, valeur = lignes[k].strip().partition(": ")
                env[nom] = valeur
                k += 1
            i = k
            continue
        i += 1
    if i >= len(lignes):
        return None, ""
    corps, k = [], i + 1
    while k < len(lignes) and (not lignes[k].strip() or len(lignes[k]) - len(lignes[k].lstrip()) > marge):
        corps.append(lignes[k][marge + 2:])
        k += 1
    return env, "\n".join(corps) + "\n"


def boucle_de_poussee(texte, ident):
    """Rend les lignes de la boucle d'essais de poussée du pas `ident` (de « for essai in » à l'erreur finale), ou "".

    ① RÔLE — Isoler la boucle pour la jouer seule (F3). ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — le texte, l'identifiant.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte, "" si la boucle manque. [rend: 1]
    ⑥ TRAITEMENT — dans le script du pas : de la ligne qui commence par « for essai in » à la ligne « ::error:: » qui
      suit son « done ». ⑦ UNITÉ — — ⑧ POURQUOI — Le reste du pas lit le jeton et le dépôt privé : il ne se joue pas ici.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    _, script = pas_du_gabarit(texte, ident)
    lignes = script.split("\n")
    debut = next((i for i, l in enumerate(lignes) if l.startswith("for essai in ")), None)
    if debut is None:
        return ""
    fin = next((i for i in range(debut, len(lignes)) if lignes[i] == "done"), None)
    if fin is None or fin + 1 >= len(lignes) or "::error::" not in lignes[fin + 1]:
        return ""
    return "\n".join(lignes[debut:fin + 2]) + "\n"


def tour(racine):
    """Joue F1 à F4 sur `racine` ; rend la liste des cas faux.

    ① RÔLE — Un tour complet. ② CONTEXTE D'APPEL — `main`, une fois tel quel et une fois par sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée (la vraie, ou une copie sabotée). ④ CONDITIONS D'ENTRÉE — Fiche en tête.
    ⑤ SORTIE — UNE valeur : la liste des cas faux (textes). [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, F1 à F4. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête.
    ⑩ EFFET — Dossiers jetables. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="file_longue_")
    try:
        F = charger(os.path.join(racine, FABRICANT), "fabricant_file")
        if F.RELAIS is None or F.EPREUVES is None or F.SERIES is None:
            return [f"gabarits non fabriqués : {F.ERREUR_DE_LA_TABLE}"]
        soir = F.fabriquer_le_circuit(open(os.path.join(racine, CIRCUIT_PRIVE), encoding="utf-8").read())
        fiches = {c.split("/")[-1]: o.decode("utf-8") for c, o in F.ce_que_la_publication_ecrit(racine, [], [], soir)
                  if c.startswith(".github/workflows/")}
        longs = [os.path.basename(F.CIRCUIT_SERIES), os.path.basename(F.CIRCUIT_EPREUVES),
                 os.path.basename(F.CIRCUIT_CERTIFICATION)]
        table = json.load(open(os.path.join(racine, TABLE), encoding="utf-8"))
        codes = list(table.get("epreuves_longues") or {})
        # ---- F1 : le relais, joué, avec le réservoir plein (trois passages en cours)
        outils = os.path.join(d, "outils")
        os.makedirs(outils)
        open(os.path.join(outils, "gh"), "w", encoding="utf-8").write(FAUX_GH)
        os.chmod(os.path.join(outils, "gh"), 0o755)
        env_r, script_r = pas_du_gabarit(F.RELAIS, "relayer")
        if env_r is None or len(codes) < 2:
            faux.append(f"F1 pas « relayer » introuvable, ou moins de deux épreuves longues dans la table ({len(codes)})")
        else:
            r = os.path.join(d, "public")
            os.makedirs(os.path.join(r, "demandes"))
            lancer(["git", "init", "-q", "-b", "main", r], env=GIT_ENV)
            open(os.path.join(r, "LISEZMOI"), "w").write("essai\n")
            lancer(["git", "-C", r, "add", "-A"], env=GIT_ENV)
            lancer(["git", "-C", r, "commit", "-q", "-m", "avant"], env=GIT_ENV)
            avant = lancer(["git", "-C", r, "rev-parse", "HEAD"], env=GIT_ENV)[1].strip()
            open(os.path.join(r, NOM_DE_DEMANDE), "w").write(f"circuit=epreuve\nepreuves={codes[0]},{codes[1]}\n")
            lancer(["git", "-C", r, "add", "-A"], env=GIT_ENV)
            lancer(["git", "-C", r, "commit", "-q", "-m", "demande"], env=GIT_ENV)
            apres = lancer(["git", "-C", r, "rev-parse", "HEAD"], env=GIT_ENV)[1].strip()
            contexte = {"github.event.before": avant, "github.sha": apres, "github.ref_name": "main",
                        "github.repository": "essai/public", "github.token": "jeton-fictif"}
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=d,
                       FAUX_GH_JOURNAL=os.path.join(d, "gh.jsonl"),
                       FAUX_GH_PASSAGES=json.dumps([{"status": "in_progress", "displayTitle": "en cours places 1+18"}]))
            for nom, valeur in env_r.items():
                m = re.fullmatch(r"\$\{\{ ([^}]+) \}\}", valeur)
                env[nom] = str(contexte[m.group(1)]) if m else valeur
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_r], cwd=r, env=env)
            journal = os.path.join(d, "gh.jsonl")
            appels = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
            listes = [a[3] for a in appels if a[:2] == ["run", "list"] and len(a) > 3]
            lances = [a for a in appels if a[:2] == ["workflow", "run"]]
            if c != 0 or len(lances) != 1 or "DEMANDE REFUSEE" in o:
                faux.append(f"F1 réservoir plein (trois passages en cours) : la demande n'est pas lancée une fois : code {c}, "
                            f"{len(lances)} lancement(s) : {o.strip()[-200:]}")
            elif not re.search(r"premiere_place=[0-9]+", " ".join(lances[0])) or "nombre_de_places=2" not in lances[0]:
                faux.append(f"F1 lancée sans ses places : {lances[0]}")
            if sorted(listes) != sorted(longs):
                faux.append(f"F1 le relais n'a pas lu les passages des trois circuits longs : {listes}")
        # ---- F2 : la protection fine, sur les fiches
        for nom in longs:
            texte = fiches.get(nom, "")
            try:
                groupe, _, file = F.structure_d_une_fiche(texte)
                reservoir = F.largeur_d_une_fiche(texte)[0]
            except ValueError as e:
                faux.append(f"F2 {nom} : illisible : {e}")
                continue
            if reservoir != F.RESERVOIR_DES_PLACES:
                faux.append(f"F2 {nom} : n'est pas une fiche du réservoir (chaque job sur une place) : {reservoir}")
            if nom != os.path.basename(F.CIRCUIT_CERTIFICATION):
                exprs = re.findall(r"\$\{\{[^}]*\}\}", groupe or "")
                if exprs != ["${{ github.ref_name }}"]:
                    faux.append(f"F2 {nom} : groupe de passage {groupe!r} : il doit être nommé par la branche, et par elle seule")
            if not groupe or file.get("queue") != "max" or file.get("cancel-in-progress") == "true":
                faux.append(f"F2 {nom} : groupe de passage {groupe!r} absent ou sans file ({file})")
        membres = {}
        for nom in longs:
            for p in F.NOMS_DES_PLACES:
                membres.setdefault(p, []).append(nom)
        refus_f = F.refus_de_la_file(fiches, membres)
        if refus_f:
            faux.append(f"F2 refus de la file : {refus_f}")
        # ---- F3 : les poussées, jouées contre une origine qui refuse la première
        for nom, texte, branche_env in (("épreuves longues", F.EPREUVES, {"GITHUB_RUN_ID": "77", "CODE": "Mini"}),
                                        ("séries", F.SERIES, {"GITHUB_RUN_ID": "78", "SERIE": "HL", "PART": "0"})):
            boucle = boucle_de_poussee(texte, "deposer")
            n = re.match(r"for essai in ((?:[0-9]+ ?)+); do", boucle)
            if not boucle or not n or len(n.group(1).split()) != F.ESSAIS_DE_POUSSEE_SUR_SA_BRANCHE \
                    or F.ESSAIS_DE_POUSSEE_SUR_SA_BRANCHE < 2 or "git pull -q --rebase origin" not in boucle:
                faux.append(f"F3 {nom} : pas de boucle de {F.ESSAIS_DE_POUSSEE_SUR_SA_BRANCHE} essais avec reprise "
                            f"(« git pull --rebase ») dans le pas « deposer » : {boucle[:160]!r}")
                continue
            nu = os.path.join(d, f"nu_{branche_env['GITHUB_RUN_ID']}.git")
            lancer(["git", "init", "-q", "--bare", nu], env=GIT_ENV)
            compteur = os.path.join(d, f"refus_{branche_env['GITHUB_RUN_ID']}")
            crochet = os.path.join(nu, "hooks", "pre-receive")
            open(crochet, "w").write(f"#!/bin/sh\nif [ ! -e '{compteur}' ]; then : > '{compteur}'; echo refus passager >&2; "
                                     "exit 1; fi\nexit 0\n")
            os.chmod(crochet, 0o755)
            t = os.path.join(d, f"t_{branche_env['GITHUB_RUN_ID']}")
            lancer(["git", "init", "-q", t], env=GIT_ENV)
            open(os.path.join(t, "SORTIE.txt"), "w").write("sortie\n")
            lancer(["git", "-C", t, "add", "-A"], env=GIT_ENV)
            lancer(["git", "-C", t, "commit", "-q", "-m", "resultat"], env=GIT_ENV)
            lancer(["git", "-C", t, "remote", "add", "origin", nu], env=GIT_ENV)
            # l'attente au hasard de la boucle (« sleep ») est remplacée par un faux sleep immédiat
            open(os.path.join(outils, "sleep"), "w").write("#!/bin/sh\nexit 0\n")
            os.chmod(os.path.join(outils, "sleep"), 0o755)
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], **branche_env)
            c, o = lancer(["bash", "--noprofile", "--norc", "-c", boucle], cwd=t, env=env)
            refs = lancer(["git", "-C", nu, "for-each-ref", "--format=%(refname)"], env=GIT_ENV)[1].split()
            if c != 0 or "essai 2" not in o or len(refs) != 1:
                faux.append(f"F3 {nom} : un refus passager n'est pas repris : code {c}, branches {refs} : {o.strip()[-200:]}")
        # ---- F4 : la largeur, au plus 20, dont 2 places hors du réservoir
        refus_l, lignes = F.refus_de_la_largeur(fiches)
        total = next((int(m.group(1)) for l in lignes for m in [re.search(r"sans attendre : .* = ([0-9]+) \(limite", l)] if m),
                     None)
        if refus_l or total != 2 + F.PLACES_LONGUES or total > F.TACHES_EN_MEME_TEMPS_DU_COMPTE:
            faux.append(f"F4 largeur : total {total} (attendu 2 + {F.PLACES_LONGUES}, au plus "
                        f"{F.TACHES_EN_MEME_TEMPS_DU_COMPTE}) ; refus {refus_l}")
    except Exception as e:   # noqa: BLE001 — une erreur imprévue est un cas faux, jamais un passage
        faux.append(f"erreur imprévue : {type(e).__name__} : {e}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


SABOTAGES = {
    # SF1 : le refus global remis au relais (l'état d'avant FILE-2 : refuser dès qu'un passage long est en cours)
    "SF1_refus_global_remis": [(FABRICANT, '''            done
            M=""" + str(PLACES_LONGUES) + """''', '''            done
            [ ! -s "$D/passages" ] || { echo "::error::DEMANDE REFUSEE : passage(s) en cours ou en attente"; exit 1; }
            M=""" + str(PLACES_LONGUES) + """''')],
    # SF2 : le groupe de passage par branche retiré du circuit des épreuves longues
    "SF2_groupe_par_branche_retire": [(FABRICANT, '''%(entrees)sconcurrency:
  group: %(groupe)s
  cancel-in-progress: false
  queue: max
permissions:
  contents: read
jobs:
  preparer:
    runs-on: ubuntu-latest
%(place_du_passage)s    timeout-minutes: 30
    outputs:
      sha: ${{ steps.matrice.outputs.sha }}
      matrice:''', '''%(entrees)spermissions:
  contents: read
jobs:
  preparer:
    runs-on: ubuntu-latest
%(place_du_passage)s    timeout-minutes: 30
    outputs:
      sha: ${{ steps.matrice.outputs.sha }}
      matrice:''')],
    # SF3 : les nouveaux essais de poussée retirés — une seule poussée, sans reprise (l'état d'avant FILE-2)
    "SF3_essais_de_poussee_retires": [(FABRICANT, '''          for essai in """ + " ".join(str(k) for k in range(1, ESSAIS_DE_POUSSEE_SUR_SA_BRANCHE + 1)) + """; do
            if git push -q origin "HEAD:refs/heads/""" + branche + """"; then echo "depose sur sa branche (essai $essai)"; exit 0; fi
            git pull -q --rebase origin "refs/heads/""" + branche + """" || git rebase --abort || true
            sleep $((RANDOM % 15 + 1))
          done
''', '''          git push -q origin "HEAD:refs/heads/""" + branche + """" || { echo "::error::une seule poussee"; exit 1; }
          echo "depose sur sa branche"; exit 0
''')],
    # SF5 : la boucle garde sa forme mais sort au premier refus (la partie JOUÉE de F3 doit le voir, pas la lecture)
    "SF5_boucle_qui_sort_au_premier_refus": [(FABRICANT, '''|| git rebase --abort || true
            sleep $((RANDOM % 15 + 1))''', '''|| git rebase --abort || true
            sleep $((RANDOM % 15 + 1)); exit 1''')],
    # SF4 : dépasser 20 — 19 places longues, le soir et le relais n'ont plus leurs deux places
    "SF4_vingt_et_un": [(FABRICANT, "\nLARGEUR_DES_CIRCUITS_LONGS = ", "\nLARGEUR_DES_CIRCUITS_LONGS = 1 + ")],
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter (ou --saboter=SF1,…), une copie des fichiers LUS par sabotage, le
      fichier visé écrit saboté (chaque remplacement doit trouver son texte EXACTEMENT une fois, sinon code 2), un tour
      par copie ; un sabotage qui ne fait rougir aucun cas « NE MORD PAS ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Copies jetables, effacées.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(DEPOT)
    print("Z0 programmes tels quels : " + ("F1 à F4 conformes" if not faux else "FAUX " + " | ".join(faux)))
    rouge = bool(faux)
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
    if "--saboter" in sys.argv[1:] or choix:
        noms = choix[0] if choix else list(SABOTAGES)
        for nom in noms:
            if nom not in SABOTAGES:
                print(f"ARRÊT sabotage inconnu : {nom}")
                return 2
            copie = tempfile.mkdtemp(prefix="file_sabot_")
            try:
                for f in LUS:
                    os.makedirs(os.path.dirname(os.path.join(copie, f)), exist_ok=True)
                    shutil.copyfile(os.path.join(DEPOT, f), os.path.join(copie, f))
                for f, avant, apres in SABOTAGES[nom]:
                    chemin = os.path.join(copie, f)
                    texte = open(chemin, encoding="utf-8").read()
                    if texte.count(avant) != 1:
                        print(f"ARRÊT {nom} ne s'applique plus ({texte.count(avant)} occurrence(s) dans {f})")
                        return 2
                    open(chemin, "w", encoding="utf-8").write(texte.replace(avant, apres))
                vus = tour(copie)
                print(f"{nom} " + (f"mord : {vus}" if vus else "NE MORD PAS : []"))
                rouge = rouge or not vus
            finally:
                shutil.rmtree(copie, ignore_errors=True)
    print("VERDICT : " + ("NON CONFORME" if rouge else "tout est conforme"))
    return 1 if rouge else 0


if __name__ == "__main__":
    sys.exit(main())
