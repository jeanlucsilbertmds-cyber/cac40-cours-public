#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_ETAT_DES_TRAVAUX_Ven_20-11-2026.py — Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. « Ces épreuves fabriquent un faux dépôt git et un faux gh sous un dossier temporaire, y rejouent les
situations réelles du 20-11-2026, et vérifient que programmes/ETAT_DES_TRAVAUX.py range chaque branche comme il faut
et que programmes/ALARME_DES_MACHINES_OISIVES.py sonne quand des machines sont oisives, et seulement alors. »

① RÔLE — Éprouver les deux programmes (R-731), avec sabotages (--saboter) qui doivent faire rougir au moins un cas.
② CONTEXTE D'APPEL — Sur GitHub, par le circuit des épreuves longues (codes EtatTravaux et EtatTravauxSabot de
  tests/LANCEMENT_DES_EPREUVES.json) ; à la main : python3 -B tests/EPREUVES_DE_L_ETAT_DES_TRAVAUX_Ven_20-11-2026.py
  <racine> [--saboter].
③ ENTRÉE — La racine d'une copie du dépôt (programmes/ y est lu) ; l'option --saboter.
④ CONDITIONS D'ENTRÉE — git et python3 ; aucun réseau ; un dossier temporaire inscriptible.
⑤ SORTIE — Code 0 : tous les cas tiennent (et, avec --saboter, chaque sabotage fait rougir au moins un cas) ·
  1 : un cas faux ou un sabotage muet · 2 : l'épreuve n'a pas pu tourner.
⑥ TRAITEMENT — Fabriquer le faux dépôt (origin/main porte le VRAI fabricant de la racine, pour que la largeur soit
  lue comme en vrai) ; jouer les cas ; avec --saboter, copier les deux programmes, poser un sabotage, rejouer.
⑦ UNITÉ — Secondes Unix pour les dates fabriquées (heure de Paris du 20-11-2026, UTC+1).
⑧ POURQUOI — Réparations du RELU de Cowork du 20-11-2026 à 22h25 (B1, I1, I2, I3, m1, m2), chacune avec son cas et
  son sabotage (S5 à S11). R-731 et R-732 : au moins un cas vient d'une vraie situation — travail-contrat-6 (vert au passage
  44804954374, RELU DÉPLOYABLE à 21h16, installée par 38bec5772) et travail-proprietes-7 (EN ÉPREUVE au passage
  44814017661, six épreuves).
⑨ CE QUI CLOCHE — Le faux gh imite seulement « run list » et « run view --json jobs ».
⑩ EFFET — Écrit seulement sous un dossier temporaire, effacé à la fin.
⑪ TERMINAISON — Sort par sys.exit ; chaque git est borné à 60 s.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

T0 = 1795194000  # 20-11-2026 18h00 Paris (17h00 UTC)


def heure(h, m, s=0):
    """Secondes Unix d'une heure de Paris du 20-11-2026.

    ① RÔLE — Dater les commits fabriqués. ② CONTEXTE D'APPEL — Les cas. ③ ENTRÉE — `h`, `m`, `s` : heure de Paris.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur. ⑥ TRAITEMENT — T0 + décalage depuis 18h00.
    ⑦ UNITÉ — Secondes. ⑧ POURQUOI — Rejouer l'horaire réel. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    """
    return T0 + (h - 18) * 3600 + m * 60 + s


class Depot:
    """Un faux dépôt privé, dont les branches « origin/… » sont des références posées à la main.

    ① RÔLE — Fabriquer commits et branches. ② CONTEXTE D'APPEL — `fabriquer`. ③ ENTRÉE — Le dossier.
    ④ CONDITIONS D'ENTRÉE — git. ⑤ SORTIE — — ⑥ TRAITEMENT — git init, commit-tree via l'index.
    ⑦ UNITÉ — — ⑧ POURQUOI — Aucun réseau, aucune configuration git (identité par variables d'environnement).
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans le dossier. ⑪ TERMINAISON — —
    """

    def __init__(self, dossier):
        """Crée le dépôt. ① à ⑪ : voir la classe."""
        self.d = dossier
        os.makedirs(dossier)
        self.git("init", "-q", "-b", "travail-local")

    def git(self, *a, date=None):
        """Lance git et rend sa sortie. ① à ⑪ : voir la classe ; lève si git échoue."""
        env = dict(os.environ, GIT_AUTHOR_NAME="Claude", GIT_AUTHOR_EMAIL="c@exemple.invalid",
                   GIT_COMMITTER_NAME="Claude", GIT_COMMITTER_EMAIL="c@exemple.invalid")
        if date is not None:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{date} +0100"
        r = subprocess.run(["git", "-C", self.d] + list(a), capture_output=True, text=True, env=env, timeout=60)
        if r.returncode != 0:
            raise RuntimeError(f"git {a[:2]} : {r.stderr[:200]}")
        return r.stdout.strip()

    def commit(self, parent, fichiers, date, message="m", second_parent=None):
        """Fabrique un commit sur `parent` qui écrit `fichiers` ; rend son sha. ① à ⑪ : voir la classe."""
        if parent:
            self.git("read-tree", parent)
        else:
            self.git("read-tree", "--empty")
        for chemin, contenu in fichiers.items():
            p = os.path.join(self.d, chemin)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(contenu)
            self.git("update-index", "--add", chemin)
        arbre = self.git("write-tree")
        args = ["commit-tree", arbre, "-m", message]
        for x in (parent, second_parent):
            if x:
                args += ["-p", x]
        return self.git(*args, date=date)

    def branche(self, nom, sha):
        """Pose la référence origin/<nom>. ① à ⑪ : voir la classe."""
        self.git("update-ref", "refs/remotes/origin/" + nom, sha)


def note(codes):
    """Le texte d'une note A_RELIRE portant ces codes. ① à ⑪ : voir `heure` ; rend UNE valeur."""
    return "# note\n\n## À JOUER SUR GITHUB\n" + "".join(f"- {c}\n" for c in codes) + \
        "\n## DEMANDE DE RELECTURE PAR COWORK — épreuves longues à lire sur GitHub, ne pas les rejouer\n"


def resultat(depot, passage, code, pointe, sortie, date, par_champ=False):
    """Fabrique la branche de résultat epreuves-longues/<passage>/<code>. ① à ⑪ : voir `Depot` ; rend rien.

    Par défaut la pointe jouée n'est que dans le journal (comme au passage réel 44804954374) ; `par_champ` la met
    dans RESULTAT.json (« pointe_jouee », forme annoncée sur travail-livrer-2).
    """
    r = {"code_epreuve": code, "code_de_sortie": sortie}
    if par_champ:
        r["pointe_jouee"] = pointe
    fichiers = {f"rapports/epreuves_longues/{passage}/{code}/RESULTAT.json": json.dumps(r),
                f"rapports/journal_du_circuit/circuit_{passage}_1_jouer_{code}.log":
                    f"source de la publication : le commit {pointe[:12]} du dépôt privé (ses blobs, jamais le disque)\n"}
    depot.branche(f"epreuves-longues/{passage}/{code}", depot.commit(None, fichiers, date))


def faux_gh(dossier, passages, jobs, echoue=False):
    """Écrit un faux gh ; rend son chemin. ① à ⑪ : voir `Depot`.

    `passages` : la liste rendue par « run list » · `jobs` : {passage : liste de statuts} · `echoue` : rend 1.
    """
    chemin = os.path.join(dossier, "faux_gh_%d" % len(os.listdir(dossier)))
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env python3\nimport json, sys\n"
                f"P = {json.dumps(passages)!r}\nJ = {json.dumps({str(k): v for k, v in jobs.items()})!r}\n"
                f"if {echoue!r}:\n    sys.stderr.write('gh : refus'); sys.exit(1)\n"
                "a = sys.argv[1:]\n"
                "if a[:2] == ['run', 'list']:\n    print(P)\n"
                "elif a[:2] == ['run', 'view']:\n"
                "    print(json.dumps({'jobs': [{'status': s} for s in json.loads(J).get(a[2], [])]}))\n"
                "else:\n    sys.exit(3)\n")
    os.chmod(chemin, 0o755)
    return chemin


def fabriquer(racine, tmp, installe):
    """Fabrique le faux dépôt des situations réelles du 20-11-2026 ; rend (dossier, faits utiles).

    ① RÔLE — Le monde des cas. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `racine` : la copie éprouvée · `tmp` : le
    dossier temporaire · `installe` : vrai pour l'état après 38bec5772 (travail-contrat-6 fusionnée dans main).
    ④ CONDITIONS D'ENTRÉE — Le fabricant existe dans la racine. ⑤ SORTIE — DEUX valeurs. ⑥ TRAITEMENT — Voir le code.
    ⑦ UNITÉ — — ⑧ POURQUOI — R-732. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit sous `tmp`. ⑪ TERMINAISON — Rend la main.
    """
    d = Depot(os.path.join(tmp, "depot_%s" % ("apres" if installe else "avant")))
    fab = open(os.path.join(racine, "programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), encoding="utf-8").read()
    connus = ["VenteReglable", "ContratSabot", "ProprietesBout", "ProprietesBoutSabot", "ProprietesChaine",
              "ProprietesSabot", "ProprietesSuite", "ProprietesSuiteSabot", "Tri", "Rouge", "Vert", "Vieux", "Code1",
              "Code2", "Vert4", "File", "Relais"]
    table = json.dumps({"epreuves_longues": {c: {"chemin": "tests/x.py", "arguments": ["{copie}"]} for c in connus}})
    m0 = d.commit(None, {"programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py": fab, "echanges/A_RELIRE.md": note([]),
                         "tests/LANCEMENT_DES_EPREUVES.json": table,
                         "echanges/RELU.md": "## VERDICT : DÉPLOYABLE\n"}, heure(18, 0))
    # travail-contrat-6 : 0787558b1 (20h20, code + note) ; vert au passage 44804954374 (fin 20h56) ;
    # Cowork : archive 21h16:12, RELU DÉPLOYABLE 21h16:20, heure de fin 21h16:28.
    p6 = d.commit(m0, {"programmes/X.py": "x=1\n", "echanges/A_RELIRE.md": note(["VenteReglable", "ContratSabot"])},
                  heure(20, 20, 5))
    for c in ("VenteReglable", "ContratSabot"):
        resultat(d, "44804954374", c, p6, 0, heure(20, 56, 44))
    a6 = d.commit(p6, {"archives/RELU_ANCIEN.md": "ancien\n"}, heure(21, 16, 12))
    entete = f"RELU PAR : Cowork · pointe relue **{p6[:9]}** (= pointe distante)\n"
    r6 = d.commit(a6, {"echanges/RELU.md": entete + "## VERDICT : DÉPLOYABLE\nfin 21h1\n"}, heure(21, 16, 20))
    t6 = d.commit(r6, {"echanges/RELU.md": entete + "## VERDICT : DÉPLOYABLE\nfin 21h16\n"}, heure(21, 16, 28))
    d.branche("travail-contrat-6", t6)
    main = m0
    if installe:  # 38bec5772 : fusion de la pointe 1bc903007 dans main, 21h27
        main = d.commit(m0, {"programmes/X.py": "x=1\n"}, heure(21, 27, 38), second_parent=t6)
    d.branche("main", main)
    # travail-proprietes-7 : 3261c1a68, six épreuves demandées, passage 44814017661 en cours
    six = ["ProprietesBout", "ProprietesBoutSabot", "ProprietesChaine", "ProprietesSabot", "ProprietesSuite",
           "ProprietesSuiteSabot"]
    d.branche("travail-proprietes-7", d.commit(m0, {"programmes/Y.py": "y=1\n", "echanges/A_RELIRE.md": note(six)},
                                               heure(21, 42)))
    # Branches fabriquées (pas des cas réels) pour les autres états
    d.branche("travail-a-eprouver", d.commit(m0, {"programmes/Z.py": "z\n", "echanges/A_RELIRE.md": note(["Tri"])},
                                             heure(21, 0)))
    pr = d.commit(m0, {"programmes/R.py": "r\n", "echanges/A_RELIRE.md": note(["Rouge", "Vert"])}, heure(19, 0))
    resultat(d, "100", "Rouge", pr, 1, heure(19, 30), par_champ=True)
    resultat(d, "100", "Vert", pr, 0, heure(19, 30), par_champ=True)
    d.branche("travail-rouge", pr)
    pv = d.commit(m0, {"programmes/V.py": "v\n", "echanges/A_RELIRE.md": "# note sans épreuve longue\n"},
                  heure(20, 0))
    d.branche("travail-a-relire", pv)
    d.branche("travail-ecriture", d.commit(m0, {"programmes/W.py": "w\n"}, heure(20, 0)))
    pc = d.commit(m0, {"programmes/C.py": "c\n", "echanges/A_RELIRE.md": note([])}, heure(19, 0))
    d.branche("travail-corrections", d.commit(pc, {"echanges/RELU.md": f"pointe relue {pc}\n"
                                                   "## VERDICT : DÉPLOYABLE APRÈS CORRECTIONS\n"}, heure(19, 30)))
    # Joué sur une ancienne pointe, puis un commit de code : les résultats ne valent plus
    pa = d.commit(m0, {"programmes/A.py": "a\n", "echanges/A_RELIRE.md": note(["Vieux"])}, heure(18, 30))
    resultat(d, "101", "Vieux", pa, 0, heure(18, 50))
    d.branche("travail-ancienne-pointe", d.commit(pa, {"programmes/A.py": "a2\n"}, heure(19, 10)))
    # B1 (RELU Cowork 22h25) : RELU DÉPLOYABLE sur b1, puis un commit de CODE, rejoué vert : jamais relu
    b1 = d.commit(m0, {"programmes/B.py": "b\n", "echanges/A_RELIRE.md": note(["Code1"])}, heure(18, 10))
    b1r = d.commit(b1, {"echanges/RELU.md": f"pointe relue {b1[:9]}\n## VERDICT : DÉPLOYABLE\n"}, heure(18, 40))
    b2 = d.commit(b1r, {"programmes/B.py": "b2\n"}, heure(19, 0))
    resultat(d, "102", "Code1", b2, 0, heure(19, 20))
    d.branche("travail-code-non-relu", b2)
    # RELU sans pointe relue : ne prouve pas ce qu'il a relu
    c1 = d.commit(m0, {"programmes/D.py": "d\n", "echanges/A_RELIRE.md": note(["Code2"])}, heure(18, 10))
    resultat(d, "103", "Code2", c1, 0, heure(18, 20))
    d.branche("travail-relu-sans-pointe", d.commit(c1, {"echanges/RELU.md": "## VERDICT : DÉPLOYABLE\n"},
                                                   heure(18, 50)))
    # I1 : codes en gras, liste en gras, puce inconnue, prose seule
    gras = ("# note\n\n## À JOUER SUR GITHUB\nCodes de la table :\n- **File** — l'épreuve nouvelle ;\n"
            "- **Relais, Tri** — à rejouer\n  (suite de la puce)\n\n## DEMANDE\n")
    d.branche("travail-gras", d.commit(m0, {"programmes/G.py": "g\n", "echanges/A_RELIRE.md": gras}, heure(20, 0)))
    inconnu = "## À JOUER SUR GITHUB\n- File\n- Lourd — 40 min\n"
    d.branche("travail-puce-inconnue", d.commit(m0, {"programmes/H.py": "h\n", "echanges/A_RELIRE.md": inconnu},
                                                heure(20, 0)))
    prose = "## À JOUER SUR GITHUB\nFile · Relais · Tri\n"
    d.branche("travail-prose", d.commit(m0, {"programmes/K.py": "k\n", "echanges/A_RELIRE.md": prose}, heure(20, 0)))
    # I2 : seuls la note, le RELU et archives/ diffèrent de main (cas réel travail-enchainer)
    d.branche("travail-deja-dans-main", d.commit(m0, {"echanges/A_RELIRE.md": note([]), "archives/r.md": "r\n",
                                                       "echanges/RELU.md": "## VERDICT : DÉPLOYABLE\n"}, heure(19, 0)))
    # I3 : la note réécrite APRÈS l'épreuve verte, code identique
    v4 = d.commit(m0, {"programmes/V4.py": "v\n", "echanges/A_RELIRE.md": note(["Vert4"])}, heure(18, 10))
    resultat(d, "104", "Vert4", v4, 0, heure(18, 30))
    d.branche("travail-note-apres-epreuve", d.commit(v4, {"echanges/A_RELIRE.md": note(["Vert4"]) + "vert\n"},
                                                     heure(18, 40)))
    return d.d, {"p6": p6, "t6": t6}


def charger(dossier):
    """Importe les deux programmes depuis `dossier` ; rend (E, A). ① à ⑪ : voir `fabriquer`."""
    sys.path.insert(0, dossier)
    for nom in ("ETAT_DES_TRAVAUX", "ALARME_DES_MACHINES_OISIVES"):
        sys.modules.pop(nom, None)
    try:
        sp = importlib.util.spec_from_file_location("ETAT_DES_TRAVAUX", os.path.join(dossier, "ETAT_DES_TRAVAUX.py"))
        E = importlib.util.module_from_spec(sp)
        sys.modules["ETAT_DES_TRAVAUX"] = E
        sp.loader.exec_module(E)
        sp = importlib.util.spec_from_file_location("ALARME", os.path.join(dossier, "ALARME_DES_MACHINES_OISIVES.py"))
        A = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(A)
    finally:
        sys.path.remove(dossier)
    return E, A


def jouer(racine, dossier_programmes, tmp):
    """Joue tous les cas ; rend la liste des échecs. ① à ⑪ : voir `fabriquer` ; rend UNE valeur."""
    E, A = charger(dossier_programmes)
    echecs = []

    def voir(nom, vrai, detail=""):
        """Note un cas. ① à ⑪ : voir `jouer`."""
        print(("  ✅ " if vrai else "  ❌ ") + nom + ("" if vrai else f" — {detail}"))
        if not vrai:
            echecs.append(nom)

    ghd = os.path.join(tmp, "gh_%d" % len(os.listdir(tmp)))
    os.makedirs(ghd)
    avant, f = fabriquer(racine, os.path.join(tmp, "monde_%d" % len(os.listdir(tmp))), False)
    apres, _ = fabriquer(racine, os.path.join(tmp, "monde_%d" % len(os.listdir(tmp))), True)
    proprietes = [{"databaseId": 44814017661, "workflowName": "Epreuves longues d'un tenant", "status": "in_progress",
                   "headBranch": "travail-proprietes-7", "createdAt": "2026-11-20T20:44:07Z"}]
    gh_six = faux_gh(ghd, proprietes, {44814017661: ["in_progress"] * 6})
    gh_rien = faux_gh(ghd, [], {})
    gh_plein = faux_gh(ghd, proprietes, {44814017661: ["in_progress"] * 18})

    etat = E.etat_des_travaux(avant, gh_six, "x/y", fetch=False)
    par = {b["branche"]: b for b in etat["branches"]}
    voir("R1 largeur lue au fabricant réel = 18", etat["fils"]["largeur"] == 18, etat["fils"])
    voir("R2 travail-proprietes-7 EN ÉPREUVE (passage 44814017661)",
         par["travail-proprietes-7"]["etat"] == "EN ÉPREUVE" and "44814017661" in par["travail-proprietes-7"]["action"],
         par["travail-proprietes-7"]["etat"])
    voir("R3 fils libres = 18 − 6 épreuves en cours = 12", etat["fils"]["libres"] == 12, etat["fils"])
    voir("R4 travail-contrat-6 DÉPLOYABLE (vert 44804954374 sur 0787558b1, RELU 21h16 qui la nomme)",
         par["travail-contrat-6"]["etat"] == "DÉPLOYABLE" and par["travail-contrat-6"]["relu_pointe"] == f["p6"]
         and par["travail-contrat-6"]["resultats"].get("ContratSabot", {}).get("passage") == "44804954374",
         (par["travail-contrat-6"]["etat"], par["travail-contrat-6"]["action"]))
    voir("B1 code changé après un RELU DÉPLOYABLE → À RELIRE", par["travail-code-non-relu"]["etat"] == "À RELIRE"
         and "code a changé" in par["travail-code-non-relu"]["action"], par["travail-code-non-relu"]["action"])
    voir("B1b RELU sans pointe relue → À RELIRE", par["travail-relu-sans-pointe"]["etat"] == "À RELIRE",
         par["travail-relu-sans-pointe"]["etat"])
    voir("I1 codes en gras lus : File, Relais, Tri", par["travail-gras"]["codes"] == ["File", "Relais", "Tri"]
         and par["travail-gras"]["etat"] == "À ÉPROUVER", (par["travail-gras"]["codes"], par["travail-gras"]["etat"]))
    voir("I1b puce sans code connu → ÉCRITURE, section illisible",
         par["travail-puce-inconnue"]["etat"] == "ÉCRITURE" and "illisible" in par["travail-puce-inconnue"]["action"],
         par["travail-puce-inconnue"]["action"])
    voir("I1c liste en prose seule → ÉCRITURE, section illisible",
         par["travail-prose"]["etat"] == "ÉCRITURE" and "illisible" in par["travail-prose"]["action"],
         par["travail-prose"]["action"])
    voir("I2 seuls note, RELU et archives/ diffèrent de main → INSTALLÉE",
         par["travail-deja-dans-main"]["etat"] == "INSTALLÉE", par["travail-deja-dans-main"]["etat"])
    voir("I3 note réécrite après l'épreuve verte, même code → À RELIRE (pas À ÉPROUVER)",
         par["travail-note-apres-epreuve"]["etat"] == "À RELIRE", par["travail-note-apres-epreuve"]["action"])
    voir("E1 travail-a-eprouver À ÉPROUVER", par["travail-a-eprouver"]["etat"] == "À ÉPROUVER",
         par["travail-a-eprouver"]["etat"])
    voir("E2 travail-rouge ÉPREUVE ROUGE (pointe lue dans RESULTAT.json)", par["travail-rouge"]["etat"] == "ÉPREUVE ROUGE",
         par["travail-rouge"]["etat"])
    voir("E3 travail-a-relire À RELIRE", par["travail-a-relire"]["etat"] == "À RELIRE", par["travail-a-relire"]["etat"])
    voir("E4 travail-ecriture ÉCRITURE (pas de note)", par["travail-ecriture"]["etat"] == "ÉCRITURE",
         par["travail-ecriture"]["etat"])
    voir("E5 « DÉPLOYABLE APRÈS CORRECTIONS » → ÉCRITURE", par["travail-corrections"]["etat"] == "ÉCRITURE",
         par["travail-corrections"]["etat"])
    voir("E6 résultats d'une ancienne pointe ne valent plus → À ÉPROUVER",
         par["travail-ancienne-pointe"]["etat"] == "À ÉPROUVER", par["travail-ancienne-pointe"]["etat"])
    code, phrases = A.alarmes(etat, 30, heure(22, 0))
    voir("A1 À ÉPROUVER et 12 fils libres → MACHINES OISIVES (code 1)",
         code == A.OISIVES and any("MACHINES OISIVES" in p and "travail-a-eprouver" in p for p in phrases), (code, phrases))
    voir("A2 relecture en attente rangée à part, marquée LIMITE",
         any(p.startswith("RELECTURE EN ATTENTE (LIMITE") and "travail-a-relire" in p for p in phrases), phrases)
    voir("A5 aucune alarme sur une branche déjà dans main (I2)",
         not any("travail-deja-dans-main" in p for p in phrases), phrases)
    voir("A6 pas d'INSTALLATION OUBLIÉE pour un code jamais relu (B1)",
         not any("travail-code-non-relu" in p and "INSTALLATION" in p for p in phrases), phrases)
    voir("A3 pas d'installation oubliée quand un passage tourne",
         not any("INSTALLATION OUBLIÉE" in p for p in phrases), phrases)

    etat = E.etat_des_travaux(avant, gh_plein, "x/y", fetch=False)
    code, phrases = A.alarmes(etat, 30, heure(22, 0))
    voir("F1 18 épreuves en cours → 0 fil libre", etat["fils"]["libres"] == 0, etat["fils"])
    voir("F2 0 fil libre → pas de MACHINES OISIVES", not any("MACHINES OISIVES" in p for p in phrases), phrases)

    etat = E.etat_des_travaux(avant, gh_rien, "x/y", fetch=False)
    code, phrases = A.alarmes(etat, 600, heure(22, 0))
    voir("I1 DÉPLOYABLE et rien ne tourne → INSTALLATION OUBLIÉE nomme travail-contrat-6",
         any("INSTALLATION OUBLIÉE" in p and "travail-contrat-6" in p for p in phrases), phrases)

    etat = E.etat_des_travaux(apres, gh_rien, "x/y", fetch=False)
    par = {b["branche"]: b for b in etat["branches"]}
    code, phrases = A.alarmes(etat, 600, heure(22, 0))
    voir("R5 après 38bec5772 : travail-contrat-6 INSTALLÉE", par["travail-contrat-6"]["etat"] == "INSTALLÉE",
         par["travail-contrat-6"]["etat"])
    voir("R6 aucune alarme sur une branche INSTALLÉE", not any("travail-contrat-6" in p for p in phrases), phrases)
    code, phrases = A.alarmes(etat, 600, heure(20, 10))
    voir("A4 seuil non atteint → pas de relecture en attente", not any("RELECTURE" in p for p in phrases), phrases)

    voir("C1 codes « - `Certification` » et « - Tri », pas « - (aucune …) »",
         E.codes_a_jouer("## À JOUER SUR GITHUB\n- `Certification`\n- Tri\n- (aucune : courte)\n# R-740\n- Pas\n",
                         {"Certification", "Tri", "Pas"}) == (["Certification", "Tri"], ["- (aucune : courte)"]))
    voir("C3 « **DÉPLOYABLE.** Le jeu… » et « DÉPLOYABLE · CLORE : oui » déployables ; « APRÈS CORRECTIONS » non",
         [E.est_deployable(v) for v in ("**DÉPLOYABLE.** Le jeu entier", "DÉPLOYABLE · CLORE : oui",
                                        "DÉPLOYABLE APRÈS CORRECTIONS", "DÉPLOYABLE")] == [True, True, False, True])
    voir("C2 verdicts lus sous leurs quatre formes",
         [E.verdict_du_relu(t) for t in ("## VERDICT : DÉPLOYABLE\n", "VERDICT : À REPRENDRE\n",
                                         "## VERDICT EN UNE LIGNE\nÀ REPRENDRE : x\n", "## 0 · VERDICT : OK\n")]
         == ["DÉPLOYABLE", "À REPRENDRE", "À REPRENDRE : x", "OK"])

    gh_ko = faux_gh(ghd, [], {}, echoue=True)
    r = subprocess.run([sys.executable, "-B", os.path.join(dossier_programmes, "ETAT_DES_TRAVAUX.py"), "--depot", avant,
                        "--gh", gh_ko, "--sans-fetch"], capture_output=True, text=True, timeout=120)
    voir("M1 gh en échec → IMPOSSIBLE, code 2 (R-734)", r.returncode == 2 and "IMPOSSIBLE" in r.stdout,
         (r.returncode, r.stdout[:120]))
    r = subprocess.run([sys.executable, "-B", os.path.join(dossier_programmes, "ALARME_DES_MACHINES_OISIVES.py"),
                        "--depot", avant, "--gh", gh_six, "--sans-fetch", "--maintenant", str(heure(22, 0))],
                       capture_output=True, text=True, timeout=120)
    voir("M2 l'alarme en ligne de commande rend 1 (machines oisives)", r.returncode == 1, (r.returncode, r.stdout[:200]))
    # m1 : une exception dans `alarmes` sort en 5 PLANTAGE, jamais en 1 (le code des machines oisives)
    vrai_etat, argv = A.E.etat_des_travaux, sys.argv
    A.E.etat_des_travaux = lambda *x, **y: {"fils": {"libres": 1, "largeur": 18}, "passages": [],
                                            "branches": [{"etat": "À RELIRE", "branche": "b"}]}
    sys.argv = ["alarme", "--sans-fetch"]
    try:
        A.main()
        code_m1 = "rendu sans sortir"
    except SystemExit as e:
        code_m1 = e.code
    except Exception as e:
        code_m1 = f"exception non attrapée : {type(e).__name__}"
    finally:
        A.E.etat_des_travaux, sys.argv = vrai_etat, argv
    voir("M3 un plantage dans alarmes() sort en 5, pas en 1", code_m1 == A.PLANTAGE, code_m1)
    return echecs


SABOTAGES = [
    ("S1 état mal rangé : un passage vivant ignoré", "ETAT_DES_TRAVAUX.py",
     'if faits["passages_vivants"]:', 'if False and faits["passages_vivants"]:'),
    ("S2 fils libres mal comptés : la largeur seule", "ETAT_DES_TRAVAUX.py",
     '"libres": max(0, fab["largeur"] - en_cours)', '"libres": fab["largeur"]'),
    ("S3 alarme muette alors que des machines sont oisives", "ALARME_DES_MACHINES_OISIVES.py",
     'if b["etat"] == "À ÉPROUVER" and libres > 0:', 'if b["etat"] == "À ÉPROUVER" and libres < 0:'),
    ("S4 alarme sur une branche installée", "ALARME_DES_MACHINES_OISIVES.py",
     'elif b["etat"] == "DÉPLOYABLE" and not etat["passages"]:',
     'elif b["etat"] in ("DÉPLOYABLE", "INSTALLÉE") and not etat["passages"]:'),
    ("S5 (I3) la note compte comme du code", "ETAT_DES_TRAVAUX.py",
     'HORS_CODE = ("echanges/", "archives/")', 'HORS_CODE = ("echanges/RELU.md", "archives/")'),
    ("S6 (B1) la pointe relue n'est pas confrontée au code", "ETAT_DES_TRAVAUX.py",
     'elif not faits["relu_meme_code"]:', "elif False:"),
    ("S7 (I1) seule la puce nue est lue", "ETAT_DES_TRAVAUX.py",
     'trouves = [m for m in re.findall(r"[A-Za-z][A-Za-z0-9_]*", tete) if m in connus]',
     "trouves = [tete.strip()] if tete.strip() in connus else []"),
    ("S8 (I1) une section illisible passe en silence", "ETAT_DES_TRAVAUX.py",
     '    if faits["illisibles"]:', "    if False:"),
    ("S9 (I2) INSTALLÉE seulement si la pointe est le départ", "ETAT_DES_TRAVAUX.py",
     'faits["installee"] = meme_code(depot, base, pointe)', 'faits["installee"] = (base == pointe)'),
    ("S10 (m1) plantage de alarmes() non attrapé", "ALARME_DES_MACHINES_OISIVES.py",
     "    except Exception as e:  # PLANTAGE : jamais lu comme un verdict", "    except KeyboardInterrupt as e:"),
    ("S11 (m2) « **DÉPLOYABLE.** » refusé", "ETAT_DES_TRAVAUX.py",
     '    if reste.startswith("."):\n        return True\n', "    if False:\n        return True\n"),
]


def main():
    """Joue les cas, puis les sabotages ; sort. ① à ⑪ : voir le module.

    [rend: rien]
    [sort: oui]
    """
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    racine = os.path.abspath(sys.argv[1])
    saboter = "--saboter" in sys.argv[2:]
    tmp = tempfile.mkdtemp(prefix="epreuve_etat_")
    try:
        print("== Z0 : programmes tels quels")
        echecs = jouer(racine, os.path.join(racine, "programmes"), tmp)
        if echecs:
            print(f"VERDICT : NON CONFORME — {len(echecs)} cas faux sur les programmes tels quels")
            sys.exit(1)
        muets = []
        if saboter:
            for nom, fichier, avant, apres in SABOTAGES:
                copie = os.path.join(tmp, "sabot_%d" % len(os.listdir(tmp)))
                os.makedirs(copie)
                for x in ("ETAT_DES_TRAVAUX.py", "ALARME_DES_MACHINES_OISIVES.py"):
                    shutil.copy(os.path.join(racine, "programmes", x), copie)
                texte = open(os.path.join(copie, fichier), encoding="utf-8").read()
                if texte.count(avant) != 1:
                    print(f"== {nom} : cible trouvée {texte.count(avant)} fois — sabotage impossible")
                    sys.exit(2)
                open(os.path.join(copie, fichier), "w", encoding="utf-8").write(texte.replace(avant, apres))
                print(f"== {nom}")
                rouges = jouer(racine, copie, tmp)
                print(f"   → {'MORD' if rouges else 'MUET'} : {rouges}")
                if not rouges:
                    muets.append(nom)
        if muets:
            print(f"VERDICT : NON CONFORME — sabotage(s) muet(s) : {muets}")
            sys.exit(1)
        print("VERDICT : tout est conforme" + (f" ({len(SABOTAGES)} sabotages mordent)" if saboter else ""))
        sys.exit(0)
    except Exception as e:
        print(f"ÉPREUVE IMPOSSIBLE — {type(e).__name__} : {e}")
        sys.exit(2)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
