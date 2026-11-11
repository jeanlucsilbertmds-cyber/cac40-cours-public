#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_C_LE_SOIR_LIT_LA_FICHE_Mar_10-11-2026.py — Mar 10-11-2026, repris le Mer 11-11-2026 (Paris) — épreuves de
l'agent C, plan V7, bloc 9a, et de la reprise A-706.

Simulation uniquement — aucun ordre réel.

① RÔLE — Prouver que `programmes/DETECTER_LES_SIGNAUX_GITHUB.py` (le détecteur du soir) lit le SIGNAL et l'UNIVERS
  dans les fiches du registre des stratégies, que la GARDE DU SOIR écarte une fiche que le juge refuse, et — depuis
  le 11-11-2026 (A-706, superviseur R-759 du 10-11-2026 sur le défaut C9-1) — que la garde N'ARRÊTE PLUS LE SOIR :
  le détecteur publie la séance avec `signaux: []` et le champ `garde_du_soir`, sort en 0 et dit `garde=<verdict>` ;
  dans le circuit (`.github/workflows/collecte_abc.yml`), la tenue des positions tourne, et le pas de fin « Rougir si
  la garde du soir a mordu » fait rougir le passage (refus_total, signaux_multiples, ou teneur en échec — il lit
  l'issue du teneur, C11-1 du 11-11-2026) ou seulement avertir (aucune_vivante, positions tenues) ; le lecteur `programmes/MESSAGE_DU_SOIR.py` lit le fichier sans le déclarer illisible et dit la
  garde. Avec `--saboter`, prouver que chaque épreuve MORD : chaque sabotage retire une partie de la correction et
  doit faire rougir au moins une épreuve.
② CONTEXTE D'APPEL — À la main : `python3 -I tests/EPREUVES_C_LE_SOIR_LIT_LA_FICHE_Mar_10-11-2026.py <racine> [--saboter]`.
③ ENTRÉE — `<racine>` : un clone du dépôt (jamais modifié : tout se joue sur une copie sous /dev/shm ou /tmp).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/, donnees/ (registre, référentiel, cours maître) et
  `.github/workflows/collecte_abc.yml` ; `bash` et le module `yaml` de Python ; environ 300 Mo libres dans le dossier
  temporaire.
⑤ SORTIE — UNE valeur, le code de sortie (C10 n'est verte qu'avec un teneur qui tient les positions sans fiche
  VIVANTE : celui de l'agent A, pas celui de main au 11-11-2026) : 0 si toutes les épreuves passent (et, avec --saboter, si tous les
  sabotages sont pris) ; 1 sinon ; 2 si la copie de travail n'a pas pu être faite. [rend: 1]
⑥ TRAITEMENT — ① copier la racine sans .git, etudes/, archives/ · ② pour chaque cas : remettre registre, contrat,
  détecteur, lecteur et circuit (sabotés ou non), modifier ce que le cas modifie, lancer le détecteur — seul, ou dans
  le circuit simulé (`jouer_le_circuit`) — et juger son code, son affichage, son fichier, la sortie du pas, le
  passage · ③ avec --saboter : refaire les cas avec chaque fichier saboté.
  LE CONTRAT : le changement A-706 (champ `garde_du_soir` dans SIGNAUX_DU_JOUR, déclaré facultatif dans
  `CHAMPS_FACULTATIFS_DE_SIGNAUX_DU_JOUR`) a été POSÉ par le Chat le 11-11-2026 dans
  `programmes/CONTRATS_DES_FICHIERS.py` : les cas jouent le contrat RÉEL. C11 et C12b jouent une copie du contrat
  dont `retirer_le_changement` a RETIRÉ ce changement (le contrat d'avant le 11-11-2026).
⑦ UNITÉ — —
⑧ POURQUOI — Boucle R-731 (épreuves avec sabotages, vraie ligne R-732) ; une épreuve qui reste verte quand on retire
  ce qu'elle teste est une décoration. C7 réécrite à la demande du superviseur R-759 du 10-11-2026 : « le fichier
  porte la garde, le teneur a tourné, et le passage rougit » ; et « retirer le pas de fin doit faire échouer
  l'épreuve » (sabotage Y1).
⑨ CE QUI CLOCHE — ① C1 lit la dernière séance du cours maître et la compare à la clôture de la vraie ligne : si la
  séance n'a pas de signal, C1 ne vérifie que l'univers et l'ordre (au 11-11-2026, séance du 10-11 : aucun signal ;
  le signal TOTALENERGIES du 09-11 est éprouvé par le rejeu d'identité, hors de ce fichier). ② Les cas C2 à C10
  dépendent des deux fiches vivantes au 10-11-2026 (C5E10-QA-V1, C5E10-OBS-V1). ③ LE CIRCUIT EST SIMULÉ, PAS LANCÉ :
  `jouer_le_circuit` joue trois pas pour de vrai (détecteur, teneur, pas de fin de la garde) et répute réussis les
  autres ; il évalue les conditions `if:` par un petit lecteur (`always()`, `success()`, `failure()`, comparaisons
  `steps.X.outputs.Y == / != '…'`, joints par `&&`) et lève sur toute autre forme. Le vrai GitHub Actions n'est pas
  lancé (interdit par le cadre des agents).
⑩ EFFET — Écrit seulement dans son dossier temporaire, qu'il efface à la fin.
⑪ TERMINAISON — Rend la main ; chaque programme lancé est borné à 300 s, chaque pas joué à 300 s.
  [sort: non]
"""
import csv, io, json, os, re, shutil, subprocess, sys, tempfile
import yaml

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SABOTER = "--saboter" in sys.argv
DET = "programmes/DETECTER_LES_SIGNAUX_GITHUB.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"   # le critère de la garde y vit (`fiche_suivie`, LC-1, 11-11-2026)
MSG = "programmes/MESSAGE_DU_SOIR.py"
CTR = "programmes/CONTRATS_DES_FICHIERS.py"
YML = ".github/workflows/collecte_abc.yml"
REG = "donnees/cac40_strategies.csv"
SIG = "donnees/signaux_du_jour.json"
POS = "donnees/claude_positions_ouvertes.csv"
OBS_DIX = ["TOTALENERGIES", "ENGIE", "VEOLIA", "BOUYGUES", "EIFFAGE", "AIRBUS", "RENAULT",
           "UNIBAIL_RODAMCO", "BUREAU_VERITAS", "VINCI"]
PAS_DET = "detecter_les_signaux_du_jour_le_calcul"
PAS_TENIR = "tenir_les_positions"
PAS_GARDE = "rougir_si_la_garde_du_soir_a_mordu"
# Les sorties d'un soir ordinaire pour les pas que la simulation ne joue pas (la collecte a rendu 0).
SORTIES_ORDINAIRES = {"collecte": {"code": "0"}}

# LE CHANGEMENT A-706 POSÉ PAR LE CHAT dans programmes/CONTRATS_DES_FICHIERS.py le 11-11-2026 — au mot près.
ANCRE_DU_CONTRAT = '"univers", "valeurs_sans_cette_seance"]\n'
CONTRAT_ETENDU = ('"univers", "valeurs_sans_cette_seance",\n'
                  '                   # écrit par programmes/DETECTER_LES_SIGNAUX_GITHUB.py les seuls soirs où la garde du\n'
                  '                   # soir mord (A-706, 11-11-2026), lu par programmes/MESSAGE_DU_SOIR.py.\n'
                  '                   "garde_du_soir"]\n'
                  '# Les champs de l\'enveloppe que l\'écrivain peut omettre : garde_du_soir n\'est écrit que si la garde mord.\n'
                  'CHAMPS_FACULTATIFS_DE_SIGNAUX_DU_JOUR = ("garde_du_soir",)\n')


def retirer_le_changement(texte):
    """Rend le texte du contrat RÉEL privé du changement A-706. ① RÔLE — Fabriquer, dans la copie, le contrat d'avant
    le 11-11-2026 (sans `garde_du_soir`), pour C11 et C12b. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — le texte réel de
    CONTRATS_DES_FICHIERS.py. ④ CONDITIONS D'ENTRÉE — le changement posé une seule fois, au mot près. ⑤ SORTIE — UNE
    valeur, le texte sans le changement. [rend: 1] ⑥ TRAITEMENT — remplacer le texte posé par l'ancre d'avant.
    ⑦ UNITÉ — —. ⑧ POURQUOI — Le Chat a posé le changement le 11-11-2026 (commit « contrat posé par le Chat ») :
    les épreuves jouent le contrat réel, et prouvent par ce retrait que sans lui la garde serait refusée (code 3).
    ⑨ CE QUI CLOCHE — si le texte posé change d'un caractère, ce programme lève et l'épreuve rougit (voulu : le
    texte demandé et le texte posé doivent rester les mêmes). ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Lève ValueError si le changement n'est pas trouvé une seule fois. [sort: non]"""
    if texte.count(CONTRAT_ETENDU) != 1:
        raise ValueError("changement du contrat (A-706) trouvé %d fois dans le contrat réel" % texte.count(CONTRAT_ETENDU))
    return texte.replace(CONTRAT_ETENDU, ANCRE_DU_CONTRAT)


def copier():
    """Copie la racine dans un dossier jetable. ① RÔLE — Ne jamais jouer sur le dépôt. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — la racine (RACINE). ④ CONDITIONS D'ENTRÉE — de la place sous /dev/shm ou le dossier temporaire.
    ⑤ SORTIE — UNE valeur, le chemin de la copie. [rend: 1] ⑥ TRAITEMENT — copier sans .git, etudes/, archives/.
    ⑦ UNITÉ — —. ⑧ POURQUOI — les programmes du circuit écrivent tous (instructions du projet, §7). ⑨ CE QUI CLOCHE —
    le nom porte le numéro du processus : deux lancements simultanés ne se gênent pas, mais une copie laissée par un
    arrêt brutal reste. ⑩ EFFET — écrit la copie. ⑪ TERMINAISON — rend la main ; lève OSError. [sort: non]"""
    base = os.path.join("/dev/shm" if os.path.isdir("/dev/shm") else tempfile.gettempdir(), "epreuves_C_%d" % os.getpid())
    shutil.copytree(RACINE, base, ignore=lambda d, n: [x for x in n if d == RACINE and x in (".git", "etudes", "archives")])
    return base


def changer(t, ident, colonne, valeur):
    """Rend le texte du registre où la DERNIÈRE ligne de `ident` a `colonne` = `valeur` (la dernière ligne fait foi).
    ① RÔLE — Fabriquer un registre de cas. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `t` : texte du registre ·
    `ident`, `colonne`, `valeur`. ④ CONDITIONS D'ENTRÉE — `ident` présent, `colonne` dans l'en-tête. ⑤ SORTIE — UNE
    valeur, le texte. [rend: 1] ⑥ TRAITEMENT — lire en CSV, changer la case, réécrire. ⑦ UNITÉ — —. ⑧ POURQUOI — décision
    n°83 du 01-11-2026 : la dernière ligne d'un identifiant fait foi. ⑨ CE QUI CLOCHE — les guillemets sont réécrits à
    la manière du module csv : le texte peut différer hors de la case changée. ⑩ EFFET — Aucun. ⑪ TERMINAISON — lève
    ValueError si l'identifiant ou la colonne manque. [sort: non]"""
    lignes = list(csv.reader(io.StringIO(t)))
    k = lignes[0].index(colonne)
    rang = max(i for i, l in enumerate(lignes) if l and l[0] == ident)
    lignes[rang][k] = valeur
    s = io.StringIO()
    csv.writer(s, lineterminator="\n").writerows(lignes)
    return s.getvalue()


def lancer(base, env=None):
    """Lance le détecteur de la copie. ① RÔLE — Emprunter le chemin réel, en ligne de commande. ② CONTEXTE D'APPEL —
    `les_cas`, `lancer_avec_sortie`. ③ ENTRÉE — `base` : la copie · `env` : l'environnement (None : celui du
    processus). ④ CONDITIONS D'ENTRÉE — le détecteur sous `base`. ⑤ SORTIE — TROIS valeurs : code, affichage, fichier
    des signaux lu (None s'il n'existe pas). [rend: 3] ⑥ TRAITEMENT — lancer, lire. ⑦ UNITÉ — —. ⑧ POURQUOI — le
    code de sortie fait partie de ce qui est éprouvé. ⑨ CE QUI CLOCHE — un fichier des signaux illisible lève.
    ⑩ EFFET — le détecteur écrit dans la copie. ⑪ TERMINAISON — borné à 300 s, lève au-delà. [sort: non]"""
    p = subprocess.run([sys.executable, "-B", DET, "."], cwd=base, capture_output=True, text=True, timeout=300,
                       env=env)
    j = None
    if os.path.isfile(os.path.join(base, SIG)):
        j = json.load(open(os.path.join(base, SIG), encoding="utf-8"))
    return p.returncode, p.stdout + p.stderr, j


def lancer_avec_sortie(base):
    """Lance le détecteur avec un fichier GITHUB_OUTPUT ; rend (code, affichage, fichier publié, sortie du pas).
    ① RÔLE — Voir la sortie de pas `garde=…`. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `base`. ④ CONDITIONS D'ENTRÉE —
    celles de `lancer`. ⑤ SORTIE — QUATRE valeurs. [rend: 4] ⑥ TRAITEMENT — créer le fichier vide, lancer, le relire.
    ⑦ UNITÉ — —. ⑧ POURQUOI — sur GitHub, c'est par ce fichier que le pas de fin apprend la garde. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — écrit `_sortie_du_pas` dans la copie. ⑪ TERMINAISON — celle de `lancer`. [sort: non]"""
    so = os.path.join(base, "_sortie_du_pas")
    open(so, "w").close()
    c, o, j = lancer(base, dict(os.environ, GITHUB_OUTPUT=so))
    return c, o, j, open(so, encoding="utf-8").read()


def condition_vraie(cond, echec, sorties):
    """Évalue une condition `if:` de GitHub Actions, sous la forme restreinte décrite au ⑨ du fichier ; lève sinon.
    ① RÔLE — Décider si un pas tourne. ② CONTEXTE D'APPEL — `jouer_le_circuit`, une fois par pas. ③ ENTRÉE — `cond` :
    la condition (None : aucune) · `echec` : un pas précédent est-il tombé · `sorties` : {id : {clé : valeur}}.
    ④ CONDITIONS D'ENTRÉE — termes joints par `&&` seulement. ⑤ SORTIE — UNE valeur, vrai ou faux. [rend: 1]
    ⑥ TRAITEMENT — retirer `${{ }}` · lire chaque terme · sans `always()`, `success()` ni `failure()`, ajouter le
    `success()` implicite de GitHub. ⑦ UNITÉ — —. ⑧ POURQUOI — le défaut C9-1 vivait dans ces conditions. ⑨ CE QUI
    CLOCHE — ni `||`, ni `!`, ni parenthèses, ni `outcome` : lève ValueError, et l'épreuve rougit (R-734). ⑩ EFFET —
    Aucun. ⑪ TERMINAISON — rend la main ou lève. [sort: non]"""
    if cond is None:
        return not echec
    c = str(cond).strip()
    if c.startswith("${{") and c.endswith("}}"):
        c = c[3:-2].strip()
    termes = [x.strip() for x in c.split("&&")]
    etat_dit, ok = False, True
    for x in termes:
        if x == "always()":
            etat_dit = True
        elif x == "success()":
            etat_dit, ok = True, ok and not echec
        elif x == "failure()":
            etat_dit, ok = True, ok and echec
        else:
            m = re.fullmatch(r"steps\.([A-Za-z0-9_\-]+)\.outputs\.([A-Za-z0-9_\-]+)\s*(==|!=)\s*'([^']*)'", x)
            if not m:
                raise ValueError("condition non lue par la simulation : " + x)
            v = sorties.get(m.group(1), {}).get(m.group(2), "")
            ok = ok and ((v == m.group(4)) if m.group(3) == "==" else (v != m.group(4)))
    if not etat_dit:
        ok = ok and not echec
    return ok


def jouer_le_circuit(base, texte_yml, teneur_force=None):
    """Simule le circuit du soir : joue pour de vrai le détecteur, le teneur et le pas de fin de la garde.

    ① RÔLE — Dire, pour un registre donné, quels pas tournent, ce qu'ils rendent, et si le passage rougit.
    ② CONTEXTE D'APPEL — `les_cas`, cas C4b, C7, C10 et C10b.
    ③ ENTRÉE — `base` : la copie · `texte_yml` : le fichier du circuit (saboté ou non) · `teneur_force` : None, ou un
      script bash joué À LA PLACE de celui du pas « Tenir les positions » (C10b : `exit 1`, un teneur qui échoue).
    ④ CONDITIONS D'ENTRÉE — Les pas joués ont un `run` ; `bash` installé.
    ⑤ SORTIE — DEUX valeurs : {id du pas : (code, affichage)} pour les pas JOUÉS qui ont tourné ; vrai si le passage
      rougit (un pas joué tombé sans `continue-on-error`). [rend: 2]
    ⑥ TRAITEMENT — Dans l'ordre des pas : évaluer la condition (`condition_vraie`) ; un pas joué tourne sous
      `bash --noprofile --norc -eo pipefail` comme sur GitHub, avec GITHUB_WORKSPACE, GITHUB_OUTPUT et son `env` (les
      `${{ steps.X.outputs.Y }}` et `${{ steps.X.outcome }}` remplacés — l'issue vaut success, failure ou skipped,
      comme sur GitHub) ; un pas non joué est réputé réussi, avec les sorties d'un soir ordinaire.
    ⑦ UNITÉ — Des codes de sortie.
    ⑧ POURQUOI — Superviseur R-759 du 10-11-2026 : l'épreuve C7 doit voir que le teneur a tourné et que le passage
      rougit ; seul le jeu des conditions le montre, et le défaut C9-1 vivait précisément là (le teneur sauté).
    ⑨ CE QUI CLOCHE — Voir ⑨ ③ du fichier : simulation, pas GitHub.
    ⑩ EFFET — Les pas joués écrivent dans la copie. ⑪ TERMINAISON — Chaque pas joué est borné à 300 s. [sort: non]
    """
    pas_ = [p for job in yaml.safe_load(texte_yml)["jobs"].values() for p in job.get("steps", [])]
    joues = {PAS_DET, PAS_TENIR, PAS_GARDE}
    echec, sorties, vus, issues = False, {}, {}, {}
    for p in pas_:
        ident = p.get("id", "")
        if not condition_vraie(p.get("if"), echec, sorties):
            issues[ident] = "skipped"
            continue
        if ident not in joues:
            sorties[ident] = dict(SORTIES_ORDINAIRES.get(ident, {}))
            issues[ident] = "success"
            continue
        so = os.path.join(base, "_sortie_" + ident)
        open(so, "w").close()
        env = dict(os.environ, GITHUB_WORKSPACE=base, GITHUB_OUTPUT=so)
        for k, v in (p.get("env") or {}).items():
            v = re.sub(r"\$\{\{\s*steps\.([A-Za-z0-9_\-]+)\.outputs\.([A-Za-z0-9_\-]+)\s*\}\}",
                       lambda m: sorties.get(m.group(1), {}).get(m.group(2), ""), str(v))
            env[k] = re.sub(r"\$\{\{\s*steps\.([A-Za-z0-9_\-]+)\.outcome\s*\}\}",
                            lambda m: issues.get(m.group(1), ""), v)
        script = teneur_force if (ident == PAS_TENIR and teneur_force is not None) else p["run"]
        r = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script], cwd=base, env=env,
                           capture_output=True, text=True, timeout=300)
        sorties[ident] = dict(l.split("=", 1) for l in open(so, encoding="utf-8").read().splitlines() if "=" in l)
        vus[ident] = (r.returncode, r.stdout + r.stderr)
        issues[ident] = "success" if r.returncode == 0 else "failure"
        if r.returncode != 0 and not p.get("continue-on-error"):
            echec = True
    return vus, echec


def lire_par_le_message(base):
    """Rend le message du soir composé par le lecteur de la copie (`composer`), sur la copie.
    ① RÔLE — Juger le lecteur sur le vrai fichier écrit par le détecteur. ② CONTEXTE D'APPEL — `les_cas`, C12 et C13.
    ③ ENTRÉE — `base`. ④ CONDITIONS D'ENTRÉE — MESSAGE_DU_SOIR.py et son contrat sous `base/programmes`. ⑤ SORTIE — UNE
    valeur, le message (et l'erreur éventuelle). [rend: 1] ⑥ TRAITEMENT — appeler `composer('.')` dans un processus
    neuf. ⑦ UNITÉ — —. ⑧ POURQUOI — l'écrivain et le lecteur se confrontent au même contrat. ⑨ CE QUI CLOCHE — la copie
    n'a pas d'historique git : le message dit la certification non jugée ; seules les lignes de la garde et des
    illisibles des signaux sont jugées. ⑩ EFFET — Aucun dans la copie. ⑪ TERMINAISON — borné à 300 s. [sort: non]"""
    p = subprocess.run([sys.executable, "-B", "-c", "import sys; sys.path.insert(0, 'programmes'); "
                        "import MESSAGE_DU_SOIR as M; print(M.composer('.')[0])"],
                       cwd=base, capture_output=True, text=True, timeout=300)
    return p.stdout + p.stderr


def les_cas(base, reg0, textes):
    """Joue les cas sur `base` avec les fichiers `textes` ({chemin: texte}) ; rend la liste (nom, vrai/faux, preuve).
    ① RÔLE — Les cas C1 à C13. ② CONTEXTE D'APPEL — `main`, une fois puis une fois par sabotage. ③ ENTRÉE — `base`,
    `reg0` (le vrai registre), `textes`. ④ CONDITIONS D'ENTRÉE — les deux fiches vivantes du 10-11-2026.
    ⑤ SORTIE — UNE valeur, la liste. [rend: 1] ⑥ TRAITEMENT — chaque cas remet les fichiers, change le registre, lance,
    juge. ⑦ UNITÉ — —. ⑧ POURQUOI — voir ⑧ du fichier. ⑨ CE QUI CLOCHE — voir ⑨ du
    fichier. ⑩ EFFET — écrit dans la copie, remet le registre à la fin. ⑪ TERMINAISON — celle des programmes lancés.
    [sort: non]"""
    res = []
    pos0 = open(os.path.join(base, POS), encoding="utf-8").read()
    def preparer(reg, sig_temoin=None, contrat=None):
        open(os.path.join(base, REG), "w", encoding="utf-8").write(reg)
        open(os.path.join(base, POS), "w", encoding="utf-8").write(pos0)
        for chemin, t in textes.items():
            open(os.path.join(base, chemin), "w", encoding="utf-8").write(t)
        if contrat is not None:
            open(os.path.join(base, CTR), "w", encoding="utf-8").write(contrat)
        if os.path.exists(os.path.join(base, SIG)):
            os.remove(os.path.join(base, SIG))
        if sig_temoin is not None:
            open(os.path.join(base, SIG), "w", encoding="utf-8").write(sig_temoin)
    def dire(nom, ok, preuve):
        res.append((nom, bool(ok), str(preuve)[:400]))
    def derniere_seance():
        dates = set()
        for l in open(os.path.join(base, "donnees/cours_maitre.csv"), encoding="utf-8"):
            m = re.match(r"[^,]*,(\d{4}-\d{2}-\d{2}),", l)
            if m:
                dates.add(m.group(1))
        return max(dates)
    def deux_fermees():
        return changer(changer(reg0, "C5E10-OBS-V1", "entree", "CLOSE"), "C5E10-QA-V1", "entree", "CLOSE")
    # C1 — la vraie fiche, la vraie dernière séance (R-732) : univers des dix valeurs de C5E10-OBS-V1 dans son ordre,
    # chaque signal à la clôture de sa vraie ligne du cours maître, et AUCUN champ garde_du_soir.
    preparer(reg0)
    c, o, j, so = lancer_avec_sortie(base)
    seance = derniere_seance()
    vraies = {}
    entete = open(os.path.join(base, "donnees/cours_maitre.csv"), encoding="utf-8").readline().strip().split(",")
    for l in open(os.path.join(base, "donnees/cours_maitre.csv"), encoding="utf-8"):
        if (",%s," % seance) in l:
            d = dict(zip(entete, l.strip().split(",")))
            vraies[d.get("valeur") or l.split(",")[0]] = float(d["close"])
    sig = (j or {}).get("signaux", [])
    dire("C1 vraies fiches : code 0, univers 10 dans l'ordre de C5E10-OBS-V1, séance %s, clôtures des vraies lignes, "
         "pas de garde" % seance,
         c == 0 and j and j["univers"] == 10 and [d["valeur"] for d in j["detail_indicateurs"]] == OBS_DIX
         and j["seance"] == seance and j["strategie"] == "C5-ETENDU-10" and "garde_du_soir" not in j and so == ""
         and all(s["close"] == vraies.get(s["valeur"]) for s in sig),
         (c, j and j.get("univers"), j and j.get("seance"), seance, sig, so, o[-200:]))
    # C2 — LA GARDE (A-678) : C5E10-QA-V1 passée à « CLOSE » → refusée et dite ; OBS-V1 reste suivie ; pas de garde.
    preparer(changer(reg0, "C5E10-QA-V1", "entree", "CLOSE"))
    c, o, j, so = lancer_avec_sortie(base)
    dire("C2 garde partielle : QA-V1 « CLOSE » n'est pas suivie, c'est dit, pas de garde au fichier", c == 0
         and "⛔ GARDE DU SOIR — la fiche C5E10-QA-V1" in o and "fiches suivies : C5E10-OBS-V1 ·" in o
         and j and "garde_du_soir" not in j and so == "", (c, so, o[:400]))
    # C3 — L'UNIVERS VIENT DE LA FICHE : OBS-V1 refusée → seul l'univers de QA-V1 (6 valeurs), plus de TOTALENERGIES.
    preparer(changer(reg0, "C5E10-OBS-V1", "entree", "CLOSE"))
    c, o, j = lancer(base)
    dire("C3 univers lu dans la fiche : OBS-V1 refusée → 6 valeurs, sans TOTALENERGIES", c == 0 and j and j["univers"] == 6
         and "TOTALENERGIES" not in [d["valeur"] for d in j["detail_indicateurs"]], (c, j and j.get("univers"), o[:300]))
    # C4 — REFUS TOTAL (A-706) : deux fiches refusées → code 0, la séance du soir publiée sans signal, garde
    # « refus_total » nommant les deux fiches avec le motif du juge, sortie du pas garde=refus_total.
    preparer(deux_fermees(), '{"temoin": "hier"}')
    c, o, j, so = lancer_avec_sortie(base)
    g = (j or {}).get("garde_du_soir") or {}
    dire("C4 refus total : code 0, séance publiée, signaux vides, garde refus_total des deux fiches, garde=refus_total",
         c == 0 and j and j.get("seance") == seance and j.get("signaux") == [] and g.get("verdict") == "refus_total"
         and sorted(x["fiche"] for x in g.get("fiches", [])) == ["C5E10-OBS-V1", "C5E10-QA-V1"]
         and all("porte du juge" in x["motif"] for x in g.get("fiches", [])) and so == "garde=refus_total\n"
         and "seront tenues" not in o,
         (c, j, so, o[-300:]))
    # C4b — LE REFUS TOTAL DANS LE CIRCUIT : le teneur tourne (code 0, séance du soir) et le passage ROUGIT.
    preparer(deux_fermees(), '{"temoin": "hier"}')
    try:
        vus, rouge = jouer_le_circuit(base, open(os.path.join(base, YML), encoding="utf-8").read())
    except Exception as e:
        vus, rouge = {"exception": (type(e).__name__, str(e))}, None
    t = vus.get(PAS_TENIR, (None, ""))
    dire("C4b refus total dans le circuit : le teneur a tourné, le passage ROUGIT par le pas de fin",
         t[0] == 0 and ("seance %s" % seance) in t[1] and vus.get(PAS_GARDE, (None, ""))[0] == 1
         and "::error::GARDE DU SOIR « refus_total »" in vus[PAS_GARDE][1]
         and "les positions ont ete tenues" in vus[PAS_GARDE][1] and rouge is True,
         ({k: (v[0], v[1][-160:]) for k, v in vus.items()}, rouge))
    # C5 — une valeur ajoutée à l'univers de la fiche (LVMH, mnémonique MC) entre dans la détection.
    preparer(changer(reg0, "C5E10-OBS-V1", "univers", "TTE,ENGI,VIE,EN,FGR,AIR,RNO,URW,BVI,DG,MC"))
    c, o, j = lancer(base)
    dire("C5 univers élargi dans la fiche → 11 valeurs, LVMH regardée", c == 0 and j and j["univers"] == 11
         and "LVMH" in [d["valeur"] for d in j["detail_indicateurs"]], (c, j and j.get("univers"), o[-300:]))
    # C6 — une fonction de signal absente → la garde refuse la fiche, le motif est celui du juge.
    preparer(changer(reg0, "C5E10-QA-V1", "fonction_signal", "signaux_inexistants"))
    c, o, j = lancer(base)
    dire("C6 signal refusé par le juge → fiche non suivie", c == 0 and "⛔ GARDE DU SOIR — la fiche C5E10-QA-V1" in o
         and "signaux_inexistants" in o, (c, o[:400]))
    # C7 — DEUX SIGNAUX DIFFÉRENTS, DANS LE CIRCUIT (superviseur R-759 du 10-11-2026) : le fichier porte la garde
    # « signaux_multiples », le teneur de positions a tourné (code 0, il a lu la séance du soir), et le passage rougit
    # par le pas de fin.
    src = os.path.join(base, "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py")
    shutil.copyfile(src, os.path.join(base, "programmes/MODULE_C_COPIE.py"))
    preparer(changer(reg0, "C5E10-QA-V1", "module_signal", "programmes/MODULE_C_COPIE.py"), '{"temoin": "hier"}')
    try:
        vus, rouge = jouer_le_circuit(base, open(os.path.join(base, YML), encoding="utf-8").read())
    except Exception as e:
        vus, rouge = {"exception": (type(e).__name__, str(e))}, None
    j = json.load(open(os.path.join(base, SIG), encoding="utf-8")) if os.path.isfile(os.path.join(base, SIG)) else None
    g = (j or {}).get("garde_du_soir") or {}
    t = vus.get(PAS_TENIR, (None, ""))
    dire("C7 deux signaux : garde signaux_multiples au fichier, le teneur a tourné, le passage ROUGIT",
         g.get("verdict") == "signaux_multiples" and j.get("signaux") == [] and j.get("seance") == seance
         and len(g.get("fiches", [])) == 2 and all("signal déclaré" in x["motif"] for x in g["fiches"])
         and t[0] == 0 and ("seance %s" % seance) in t[1]
         and vus.get(PAS_GARDE, (None, ""))[0] == 1 and "::error::GARDE DU SOIR" in vus[PAS_GARDE][1]
         and "les positions ont ete tenues" in vus[PAS_GARDE][1] and rouge is True,
         ({k: (v[0], v[1][-160:]) for k, v in vus.items()}, rouge, g))
    # C8 — un seul signal, mais sans étalon → code 1 « CALIBRAGE IMPOSSIBLE » (vraie panne : bloquant, rien publié).
    preparer(changer(changer(reg0, "C5E10-QA-V1", "module_signal", "programmes/MODULE_C_COPIE.py"),
                     "C5E10-OBS-V1", "module_signal", "programmes/MODULE_C_COPIE.py"), '{"temoin": "hier"}')
    c, o, j = lancer(base)
    dire("C8 signal sans étalon → code 1, rien publié", c == 1 and j == {"temoin": "hier"}
         and "CALIBRAGE IMPOSSIBLE" in o, (c, o[-300:]))
    os.remove(os.path.join(base, "programmes/MODULE_C_COPIE.py"))
    # C9 — un mnémonique absent du référentiel → fiche refusée, nommée.
    preparer(changer(reg0, "C5E10-QA-V1", "univers", "EN,BVI,FGR,RNO,URW,VIE,ZZZ"))
    c, o, j = lancer(base)
    dire("C9 mnémonique inconnu → fiche refusée, ZZZ nommé", c == 0 and "⛔ GARDE DU SOIR — la fiche C5E10-QA-V1" in o
         and "ZZZ" in o, (c, o[:400]))
    # C10 — AUCUNE FICHE VIVANTE (fermeture voulue) : garde « aucune_vivante », le teneur TIENT LES POSITIONS (code 0 :
    # l'ISSUE est comptée, plus seulement le lancement — C11-1, RELU Cowork afcdb05c du 11-11-2026), le pas de fin
    # AVERTIT en disant « tenues », et le passage ne rougit pas. ROUGE ATTENDU avec le teneur de main (il rend 1 sans
    # fiche VIVANTE) ; VERT avec le teneur de l'agent A (épreuve V10 de A).
    preparer(changer(changer(reg0, "C5E10-OBS-V1", "statut", "CLOSE"), "C5E10-QA-V1", "statut", "CLOSE"))
    try:
        vus, rouge = jouer_le_circuit(base, open(os.path.join(base, YML), encoding="utf-8").read())
    except Exception as e:
        vus, rouge = {"exception": (type(e).__name__, str(e))}, None
    j = json.load(open(os.path.join(base, SIG), encoding="utf-8")) if os.path.isfile(os.path.join(base, SIG)) else None
    t = vus.get(PAS_TENIR, (None, ""))
    dire("C10 aucune fiche vivante : garde aucune_vivante, le teneur a TENU (code 0), le pas de fin avertit « tenues », "
         "passage non rouge",
         ((j or {}).get("garde_du_soir") or {}).get("verdict") == "aucune_vivante" and t[0] == 0
         and vus.get(PAS_GARDE, (None, ""))[0] == 0 and "::warning::GARDE DU SOIR" in vus[PAS_GARDE][1]
         and "les positions ont ete tenues" in vus[PAS_GARDE][1] and rouge is False,
         ({k: (v[0], v[1][-160:]) for k, v in vus.items()}, rouge))
    # C10b — AUCUNE VIVANTE, TENEUR EN ÉCHEC (forcé : `exit 1` à la place du teneur) : le pas de fin ne dit PAS
    # « tenues », il dit « NON TENUES » et ROUGIT, même pour aucune_vivante (scénario « FERMEE » de Cowork, C11-1).
    preparer(changer(changer(reg0, "C5E10-OBS-V1", "statut", "CLOSE"), "C5E10-QA-V1", "statut", "CLOSE"))
    try:
        vus, rouge = jouer_le_circuit(base, open(os.path.join(base, YML), encoding="utf-8").read(), "exit 1")
    except Exception as e:
        vus, rouge = {"exception": (type(e).__name__, str(e))}, None
    gp = vus.get(PAS_GARDE, (None, ""))
    dire("C10b teneur en échec : le pas de fin dit « NON TENUES » et rougit, sans dire « tenues »",
         vus.get(PAS_TENIR, (None, ""))[0] == 1 and gp[0] == 1 and "NON TENUES" in gp[1]
         and "ont ete tenues" not in gp[1] and "::warning::" not in gp[1] and rouge is True,
         ({k: (v[0], v[1][-200:]) for k, v in vus.items()}, rouge))
    # C11 — L'ÉCRIVAIN SE CONFRONTE AU CONTRAT : avec le contrat SANS le changement A-706, un refus total s'arrête
    # en code 3 et ne touche pas au fichier de la veille.
    preparer(deux_fermees(), '{"temoin": "hier"}', contrat=CONTRAT_SANS_LE_CHANGEMENT)
    c, o, j = lancer(base)
    dire("C11 contrat sans le changement : la garde est refusée par l'écrivain (code 3), fichier de la veille intact",
         c == 3 and j == {"temoin": "hier"} and "garde_du_soir" in o and "HORS CONTRAT SIGNAUX_DU_JOUR" in o,
         (c, j, o[-300:]))
    # C12 — LE LECTEUR S'ACCORDE AVEC L'ÉCRIVAIN : le fichier de garde (C4) lu par MESSAGE_DU_SOIR.composer — a) avec
    # le contrat étendu : pas illisible, et la garde est dite en 🚨 ; b) avec le contrat SANS le changement : le lecteur
    # le déclare hors contrat (la preuve que le changement demandé est nécessaire, et que la ligne 557 mord).
    preparer(deux_fermees())
    c, o, j = lancer(base)
    m = lire_par_le_message(base)
    dire("C12a lecteur, contrat étendu : fichier de garde lisible, garde « refus_total » dite en ALERTE, fiches nommées",
         c == 0 and (SIG + " (") not in m and "Garde du soir : refus_total (ALERTE)" in m
         and "C5E10-OBS-V1 : porte du juge" in m and "C5E10-QA-V1 : porte du juge" in m, (c, m[-700:]))
    open(os.path.join(base, CTR), "w", encoding="utf-8").write(CONTRAT_SANS_LE_CHANGEMENT)
    m = lire_par_le_message(base)
    dire("C12b lecteur, contrat sans le changement : le même fichier est hors contrat",
         "LU « garde_du_soir » : HORS CONTRAT SIGNAUX_DU_JOUR" in m, m[:500])
    # C13 — LE LECTEUR, AUCUNE VIVANTE : la garde est dite en ⚠️, pas en 🚨.
    preparer(changer(changer(reg0, "C5E10-OBS-V1", "statut", "CLOSE"), "C5E10-QA-V1", "statut", "CLOSE"))
    c, o, j = lancer(base)
    m = lire_par_le_message(base)
    dire("C13 lecteur : aucune_vivante dite en avertissement", c == 0
         and "Garde du soir : aucune_vivante (avertissement)" in m, (c, m[-500:]))
    preparer(reg0)
    return res


CONTRAT_SANS_LE_CHANGEMENT = None

# (nom, fichier saboté, texte avant, texte après) — chaque texte « avant » doit exister une seule fois.
SABOTAGES = [
    # S1 et S5 visent, depuis le 11-11-2026 (LC-1), `fiche_suivie` du juge, où le critère vit une fois.
    ("S1 garde de la porte retirée", JUGE, "    if not porte[0]:\n        return None, None,", "    if False:\n        return None, None,"),
    ("S2 univers écrit en dur", DET, "    for v in mod.univers:\n",
     "    for v in ['TOTALENERGIES','ENGIE','VEOLIA','BOUYGUES','EIFFAGE','AIRBUS','RENAULT','UNIBAIL_RODAMCO','BUREAU_VERITAS','VINCI']:\n"),
    ("S3 plusieurs signaux acceptés", DET, "    if len(declarations) > 1:\n", "    if False:\n"),
    ("S4 signal sans étalon accepté", DET, "    if ETALON is None:\n", "    if False:\n"),
    ("S5 mnémonique inconnu accepté", JUGE, "    if inconnus:\n        return None, None,", "    if False:\n        return None, None,"),
    ("S6 refus total non gardé", DET, "    if not retenues:\n", "    if False:\n"),
    ("S7 refus tu", DET, "        print(f\"  ⛔ GARDE DU SOIR", "        pass  # print(f\"  ⛔ GARDE DU SOIR"),
    ("S8 sortie du pas tue", DET, "                fh.write(ligne + \"\\n\")\n", "                pass\n"),
    ("S9 garde absente du fichier", DET, "        \"garde_du_soir\": garde,\n", ""),
    ("S10 la garde arrête le soir (code 4)", DET,
     "octets\")\n    sys.exit(0)\n\n\ndef main", "octets\")\n    sys.exit(4)\n\n\ndef main"),
    ("S11 l'écrivain ne confronte plus l'enveloppe", DET,
     "    facultatifs = tuple(getattr(C, \"CHAMPS_FACULTATIFS_DE_SIGNAUX_DU_JOUR\", ()))\n",
     "    return\n"),
    ("S12 aucune vivante prise pour un refus total", DET, "    if not suivies:\n", "    if False:\n"),
    # Y1 : le pas entier, de son nom au pas suivant, est retiré (texte « avant » calculé par `pas_entier`).
    ("Y1 pas de fin de la garde retiré", YML, "PAS_ENTIER", ""),
    ("Y2 aucune_vivante rougit aussi", YML,
     '          if [ "$GARDE" = "aucune_vivante" ] && [ "$TENUE" = "success" ]; then\n',
     '          if [ "$GARDE" = "jamais" ] && [ "$TENUE" = "success" ]; then\n'),
    ("Y3 le teneur sauté sur une garde", YML,
     "      - name: Tenir les positions\n        id: tenir_les_positions\n",
     "      - name: Tenir les positions\n        id: tenir_les_positions\n"
     "        if: steps.detecter_les_signaux_du_jour_le_calcul.outputs.garde == ''\n"),
    ("Y4 la garde lue sur une autre sortie", YML,
     "        if: always() && steps.detecter_les_signaux_du_jour_le_calcul.outputs.garde != ''\n",
     "        if: always() && steps.detecter_les_signaux_du_jour_le_calcul.outputs.gardes != ''\n"),
    ("K1 contrat réel privé du changement A-706", CTR, CONTRAT_ETENDU, ANCRE_DU_CONTRAT),
    ("Y5 la tenue supposée", YML, '          if [ "$TENUE" = "success" ]; then\n', "          if true; then\n"),
    ("Y6 aucune_vivante avertit même sans tenue", YML,
     '          if [ "$GARDE" = "aucune_vivante" ] && [ "$TENUE" = "success" ]; then\n',
     '          if [ "$GARDE" = "aucune_vivante" ]; then\n'),
    ("D1 le détecteur promet la tenue", DET, 'dite(s) dans garde_du_soir.")\n',
     'dite(s) dans garde_du_soir. Les positions seront tenues.")\n'),
    ("M1 le lecteur tait la garde", MSG, "        detail.append(garde_dite)\n", "        pass\n"),
    ("M3 tout verdict en avertissement", MSG,
     "                niveau = \"avertissement\" if garde[\"verdict\"] == \"aucune_vivante\" else \"ALERTE\"\n",
     "                niveau = \"avertissement\"\n"),
    ("M2 le lecteur ne confronte plus l'enveloppe", MSG,
     "            ec += C.verifier(\"SIGNAUX_DU_JOUR\", list(s.keys()), \"LU\")\n", ""),
]


def pas_entier(texte, debut):
    """Rend le texte d'un pas du circuit, de la ligne `debut` à la ligne « - name: » suivante (exclue) ; "" s'il manque.
    ① RÔLE — Le sabotage Y1 (pas entier retiré). ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `texte`, `debut`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur, le texte du pas. [rend: 1] ⑥ TRAITEMENT — chercher le début et
    le pas suivant. ⑦ UNITÉ — —. ⑧ POURQUOI — superviseur R-759 : retirer le pas de fin doit faire échouer C7.
    ⑨ CE QUI CLOCHE — "" si le pas manque : le motif est alors « trouvé 0 fois » et `main` rougit. ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    i = texte.find(debut)
    if i < 0:
        return ""
    k = texte.find("\n      - name: ", i + len(debut))
    return texte[i:k + 1] if k >= 0 else texte[i:]


def main():
    """Joue les cas, puis les sabotages. ① RÔLE — Le programme. ② CONTEXTE D'APPEL — la ligne de commande.
    ③ ENTRÉE — RACINE, SABOTER. ④ CONDITIONS D'ENTRÉE — celles du fichier. ⑤ SORTIE — UNE valeur, le code (voir ⑤ du
    fichier). [rend: 1] ⑥ TRAITEMENT — copier · lire registre, contrat réel (et sa copie sans le changement, par `retirer_le_changement`), détecteur,
    lecteur, circuit · jouer les cas · avec --saboter, chaque sabotage une fois,
    motif trouvé une seule fois exigé. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — `CONTRAT_SANS_LE_CHANGEMENT` est
    global. ⑩ EFFET — copie effacée à la fin.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    global CONTRAT_SANS_LE_CHANGEMENT
    try:
        base = copier()
    except OSError as e:
        print("CODE 2 — copie impossible : %s" % e)
        return 2
    try:
        reg0 = open(os.path.join(base, REG), encoding="utf-8").read()
        contrat_reel = open(os.path.join(base, CTR), encoding="utf-8").read()
        CONTRAT_SANS_LE_CHANGEMENT = retirer_le_changement(contrat_reel)   # le contrat SANS le changement (C11, C12b)
        textes0 = {DET: open(os.path.join(base, DET), encoding="utf-8").read(),
                   JUGE: open(os.path.join(base, JUGE), encoding="utf-8").read(),   # LC-1 : S1, S5 y visent `fiche_suivie`
                   MSG: open(os.path.join(base, MSG), encoding="utf-8").read(),
                   YML: open(os.path.join(base, YML), encoding="utf-8").read(),
                   CTR: contrat_reel}
        res = les_cas(base, reg0, textes0)
        for nom, ok, preuve in res:
            print(("  ✅ " if ok else "  ❌ ") + nom + ("" if ok else "\n       " + preuve))
        bon = all(ok for _n, ok, _p in res)
        if SABOTER:
            for nom, fichier, avant, apres in SABOTAGES:
                if avant == "PAS_ENTIER":
                    avant = pas_entier(textes0[fichier], "      - name: Rougir si la garde du soir a mordu\n")
                if textes0[fichier].count(avant) != 1:
                    print("  ❌ %s : motif trouvé %d fois (attendu 1)" % (nom, textes0[fichier].count(avant)))
                    bon = False
                    continue
                r = les_cas(base, reg0, dict(textes0, **{fichier: textes0[fichier].replace(avant, apres)}))
                rouges = [n.split(" ")[0] for n, ok, _p in r if not ok]
                print(("  ✅ " if rouges else "  ❌ ") + "%s → rougissent : %s" % (nom, ", ".join(rouges) or "AUCUNE"))
                bon = bon and bool(rouges)
        print("VERDICT :", "VERT" if bon else "ROUGE")
        return 0 if bon else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
