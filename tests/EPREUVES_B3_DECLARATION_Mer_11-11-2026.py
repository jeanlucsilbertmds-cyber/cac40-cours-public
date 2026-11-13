#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES B3 — LA DÉCLARATION DATÉE (plan V7, mission B3, Mer 11-11-2026). Simulation uniquement.

LE SENS EN TÊTE — R-505 ① : « Exiger la déclaration datée, écrite avant le regard, sinon rendre NON JUGEABLE en nommant
le champ qui manque ». Le superviseur R-759 du 11-11-2026 (22h19, point 2) : la grille passait ce contrôle sur une liste
vide venue de l'appelant. Ces épreuves vérifient, sur un faux dépôt git construit ici avec de VRAIS fichiers du dépôt
(le registre des stratégies, l'en-tête du fichier des déclarations, le module de signal de IND-001-RETEST, le juge,
emp.py) et le texte réel de la déclaration en projet de IND-001-RETEST, que `lire_la_declaration` CALCULE la liste des
champs en défaut : déclaration absente, incomplète, mal formée, non engagée avant le regard, empreinte qui a changé →
NON_JUGEABLE et le champ nommé ; fichier ou instant illisible → ILLISIBLE et None, jamais []. Et que
`preparer_une_declaration` calcule la date et les empreintes et refuse qu'on les saisisse (R-728).

USAGE : python3 -B tests/EPREUVES_B3_DECLARATION_Mer_11-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de sabotage
est introuvable, un nom inconnu ou une donnée manquante (R-734).

① RÔLE — Prouver que la lecture et l'écriture de la déclaration font ce que dit la note echanges/A_RELIRE_B3.md, et
  que chaque garde a des dents (R-731).
② CONTEXTE D'APPEL — À la main ; la certification (`programmes/CERTIFIER_LA_VERSION.py`) lance chaque fichier de
  tests/ avec la racine, puis « --saboter ». Ce programme se relance lui-même en « --cas <copie> <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/DECLARER_UNE_STRATEGIE.py, CONTRATS_DES_FICHIERS.py,
  TENIR_LE_REGISTRE_DES_ESSAIS.py, COMMUN.py, JUGE_DES_STRATEGIES.py, MODULE_SIGNAL_RSI_REBOND.py ; emp.py ;
  donnees/DECLARATIONS_DATEES.csv et donnees/cac40_strategies.csv ; git.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier les quatre programmes du code éprouvé dans un dossier
  temporaire, appliquer le sabotage (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie ·
  ③ Z0 doit être vert ; un sabotage doit faire rougir au moins un cas.
⑦ UNITÉ — Des instants en heure de Paris avec décalage ; des champs.
⑧ POURQUOI — R-731 (sabotages), R-732 (cas tirés de vraies lignes : L1, et le registre et le module réels du faux
  dépôt), R-734 (ce qui n'a pas pu tourner rend 2).
⑨ CE QUI CLOCHE — ① La jonction avec la grille et `juger` n'est pas éprouvée ici : c'est l'épreuve de bout en bout de
  l'agent J. ② Le faux dépôt n'a qu'une branche « main » ; la branche réelle « origin/main » n'est pas éprouvée.
  ③ Les sabotages ne portent que sur programmes/DECLARER_UNE_STRATEGIE.py. ④ Une lignée illisible contamine toute fiche
  (portée « lignee », côté strict voulu) : la ligne de L7 est jouée seule puis retirée ; aucun sabotage ne vise
  `lignee_de_la_fiche` (TENIR_LE_REGISTRE_DES_ESSAIS.py), seul L7c l'observe.
⑩ EFFET — Écrit et efface des dossiers temporaires sous /tmp (préfixe B3_) ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 300 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""
import csv, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, tempfile
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ICI = os.path.abspath(__file__)
DECL = "programmes/DECLARER_UNE_STRATEGIE.py"
CODE = (DECL, "programmes/CONTRATS_DES_FICHIERS.py", "programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py", "programmes/COMMUN.py",
        "programmes/JUGE_DES_STRATEGIES.py")   # le juge : LA lecture des colonnes du signal (REGARD tour 3, T2-D2)
FICHE = "IND-001-RETEST"                       # vraie fiche du registre, au vrai module de signal
EXAMEN = "2000-01-03..2023-12-29"

# LES SABOTAGES : (fichier, texte présent UNE fois, remplacement). Chacun retire ce qu'un cas teste.
SABOTAGES = {
    # S01, S12, S14 SUIVENT LE JUGE (12-11-2026) : REGARD tour 3 (13f55ff6) a retiré la branche des paramètres, le
    # contrôle des années et changé l'indentation de « ligne = engagee » ; leurs anciennes cibles étaient absentes
    # (« --saboter » rendait 2). Même propriété visée, cible actuelle.
    "S01_sans_branche_accepte": [(DECL, "    if sommet is None:\n        return None, raison\n",
                                  "    if sommet is None:\n        sommet = \"HEAD\"\n")],
    "S02_non_engagee_acceptee": [(DECL, 'defaut("date_declaration", "non engagée sur',
                                  '(lambda *a: None)("date_declaration", "non engagée sur')],
    "S03_empreinte_non_comparee": [(DECL, 'elif calculees[champ] != (ligne.get(champ) or "").strip():', "elif False:")],
    "S04_non_recalculable_accepte": [(DECL, 'defaut(champ, "non recalculable : " + raison)', "pass")],
    "S05_forme_ignoree_a_la_lecture": [(DECL, "    for champ, raison in defauts_par_champ(ligne).items():\n"
                                              "        defaut(champ, raison)\n", "")],
    "S06_parametres_libres_non_lus": [(DECL, 'not re.fullmatch(r"[0-9]+", ligne["parametres_libres"].strip())',
                                       "False")],
    "S07_univers_date_apres_accepte": [(DECL, "if jour is not None and du > jour:", "if False:")],
    "S08_illisible_devient_complete": [(DECL, "lecture.update(etat=illisible, champs_en_defaut=None,\n"
                                              "                       raisons=[\"fichier : lecture impossible (%s)",
                                        "lecture.update(etat=complete, champs_en_defaut=[],\n"
                                        "                       raisons=[\"fichier : lecture impossible (%s)")],
    "S09_champ_calcule_saisi_accepte": [(DECL, "    if saisis:\n        raise ValueError",
                                         "    if False:\n        raise ValueError")],
    "S10_empreinte_non_calculee": [(DECL, "empreinte_code_juge=juge, empreinte_code_signal=signal)",
                                    "empreinte_code_juge=saisie.get('empreinte_code_juge', ''), "
                                    "empreinte_code_signal=signal)")],
    "S11_date_apres_le_regard_acceptee": [(DECL, ") >= limite:", ") >= limite and False:")],
    "S12_annees_instables_acceptees": [(DECL, "if ligne_csv_de_la_declaration(engagee) != ligne_csv_de_la_declaration(ligne):",
                                        "if False:")],
    "S13_jamais_non_jugeable": [(DECL, "etat=non_jugeable if champs else complete", "etat=complete")],
    "S14_engagee_remplacee_par_le_disque": [(DECL, "            ligne = engagee\n", "")],
    "S15_ecrivain_sans_la_forme": [(DECL, '    defauts += ["%s : %s" % (c, r) for c, r in par_champ.items() if c not in vides]\n', "")],
}


def charger(chemin, nom):
    """Charge un programme par son chemin.
    ① RÔLE — charger le code éprouvé (copie sabotée ou non). ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — le dossier du programme contient ses voisins. ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — mettre son dossier en tête du chemin d'import, charger. ⑦ UNITÉ — —. ⑧ POURQUOI — chaque relance
    « --cas » est un processus neuf : aucun module d'une autre copie n'est en cache. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — modifie sys.path. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    sys.path.insert(0, os.path.dirname(chemin))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


def cas(copie, racine):
    """Joue tous les cas avec le code de `copie` sur des données tirées de `racine`.
    ① RÔLE — les cas de B3. ② CONTEXTE D'APPEL — `main` en « --cas ». ③ ENTRÉE — `copie` : un dossier qui porte
    programmes/ (le code éprouvé) · `racine` : le dépôt, source des vraies données. ④ CONDITIONS D'ENTRÉE — celles de
    l'en-tête. ⑤ SORTIE — UNE valeur : la liste des [nom, vert, détail]. [rend: 1] ⑥ TRAITEMENT — bâtir un faux dépôt
    git, jouer chaque cas, l'effacer. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — une exception dans un cas le
    rend rouge, avec son message. ⑩ EFFET — écrit et efface /tmp/B3_*. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    D = charger(os.path.join(copie, DECL), "DECLARER_UNE_STRATEGIE")
    C = sys.modules["CONTRATS_DES_FICHIERS"]
    T = sys.modules["TENIR_LE_REGISTRE_DES_ESSAIS"]
    res = []

    def ok(nom, vert, det=""):
        """Note un cas. ① RÔLE — un résultat. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `nom`, `vert`, `det`.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — ajouter. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie `res`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        res.append([nom, bool(vert), str(det)[:300]])

    def essai(nom, f):
        """Joue un groupe de cas ; une exception le rend rouge. ① RÔLE — isoler. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — `nom`, `f`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — appeler.
        ⑦ UNITÉ — —. ⑧ POURQUOI — un sabotage qui fait lever doit rougir. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie
        `res`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        try:
            f()
        except Exception as ex:                       # noqa: BLE001 — tout échec est un rouge
            ok(nom + " (exception)", False, "%s: %s" % (type(ex).__name__, ex))

    fiches = C.lire_les_fiches(racine)
    module = fiches[FICHE]["module_signal"]
    sans_module = next(k for k, v in fiches.items() if not (v.get("module_signal") or "").strip())
    d = tempfile.mkdtemp(prefix="B3_depot_")
    env = dict(os.environ, GIT_AUTHOR_NAME="b3", GIT_AUTHOR_EMAIL="b3@x", GIT_COMMITTER_NAME="b3",
               GIT_COMMITTER_EMAIL="b3@x")

    def g(*a):
        """Lance git dans le faux dépôt. ① RÔLE — bâtir l'histoire. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `a`.
        ④ CONDITIONS D'ENTRÉE — git. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — lancer. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit dans le faux dépôt. ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        subprocess.run(["git", "-C", d] + list(a), capture_output=True, check=True, env=env)

    def commit(m):
        """Commite tout. ① RÔLE — un pas d'histoire. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `m`.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — add, commit. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        g("add", "-A")
        g("commit", "-q", "--allow-empty", "-m", m)
        g("update-ref", "refs/remotes/origin/main", "HEAD")      # la branche principale du contrat (REGARD tour 3)

    chemin_decl = os.path.join(d, C.DECLARATIONS_DATEES)

    def ajouter_brut(ligne):
        """Ajoute une ligne SANS passer par l'écrivain (une ligne tapée à la main). ① RÔLE — fabriquer des lignes
        fautives. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `ligne`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune
        valeur. [rend: 0] ⑥ TRAITEMENT — DictWriter en ajout. ⑦ UNITÉ — —. ⑧ POURQUOI — l'écrivain refuserait.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        with open(chemin_decl, "a", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=C.DECLARATION_DATEE, lineterminator="\n").writerow(
                {c: ligne.get(c, "") for c in C.DECLARATION_DATEE})

    try:
        for f in ("emp.py", "programmes/JUGE_DES_STRATEGIES.py", module, fiches["C5E10-QA-V1"]["module_signal"],
                  C.REGISTRE_DES_STRATEGIES, C.DECLARATIONS_DATEES, T.REGLAGES):
            # T.REGLAGES (mission REGARD, 12-11-2026) : depuis B2, la portée du regard est un réglage LU ; sans lui,
            # `premier_regard` rendait « réglages absents » et huit cas rougissaient déjà sur la pointe 689e0149.
            os.makedirs(os.path.dirname(os.path.join(d, f)) or d, exist_ok=True)
            shutil.copy(os.path.join(racine, f), os.path.join(d, f))
        g("init", "-q", "-b", "main")
        # LE DÉPÔT DISTANT, LOCAL (mission REGARD) : le registre des essais vit sur sa branche des regards
        nu = os.path.join(d, ".depot_nu")
        subprocess.run(["git", "init", "-q", "--bare", nu], capture_output=True, check=True)
        with open(os.path.join(d, ".git", "info", "exclude"), "a", encoding="utf-8") as f:
            f.write("\n.depot_nu/\n")
        g("remote", "add", "origin", nu)
        reg = os.path.join(d, T.REGLAGES)          # le dépôt commun de cette racine : son dépôt nu (REGARD, tour 2)
        texte = "".join(l for l in open(reg, encoding="utf-8").read().splitlines(True)
                        if not l.startswith("depot_des_regards,"))
        open(reg, "w", encoding="utf-8").write(texte + "depot_des_regards,%s,épreuve,épreuve\n" % nu)
        commit("base")
        # LA SAISIE : le texte réel de etudes/IND-001-RETEST/DECLARATION_EN_PROJET_Mer_11-11-2026_17h36.md (champs
        # décidés) ; les champs que ce projet dit « à remplir par programme » et qui ne sont pas calculés aujourd'hui
        # portent ici des valeurs d'épreuve (reglages, bareme, reference_hasard, temoins, epoques, regle_de_departage).
        saisie = {
            "fiche_id": FICHE, "declaree_par": "Chat", "confirmee_par": "Jean-Luc, 11-11-2026 17h35, « Ok, ça marche »",
            "cas": "2", "periode_conception": "2024-01-02..2026-10-05",
            "part_regardee": "2024-01..2026-03 (IND-001, 28-03-2026) ; 2024-01-02..2026-10-05 (moulinette à blanc, 11-11-2026)",
            "regle_univers": "Les 39 valeurs du CAC 40 au référentiel des valeurs, banques comprises, sans ArcelorMittal",
            "date_regle_univers": "2026-11-11", "lignee": "IND-001 → IND-001-RETEST",
            "hypothese": "Quand le RSI 14 jours d'une valeur du CAC 40 repasse au-dessus de 30 après être passé dessous, "
                         "le cours remonte assez souvent dans les 20 séances pour gagner, frais compris.",
            "parametres_libres": "3", "moment_du_regard": "les 30 % les plus récents, une seule fois, au jugement",
            "biais_du_survivant": "univers du jour, déclaré", "annees_d_examen": EXAMEN, "regard_sans_decision": "",
            "reglages": '{"periode": 14, "seuil": 30, "chauffe": 100}', "bareme": "épreuve", "reference_hasard": "épreuve",
            "temoins": "aucun", "epoques": "2000-01-03..2023-12-29", "regle_de_departage": "alphabétique",
            "source": "épreuve B3",
        }

        def l1():
            with open(os.path.join(racine, C.DECLARATIONS_DATEES), encoding="utf-8-sig") as f:
                entete = next(csv.reader(f))
            ok("L1 vraie ligne : l'en-tête du fichier du dépôt est le contrat DECLARATION_DATEE",
               entete == C.DECLARATION_DATEE)
            r = D.lire_la_declaration(d, FICHE, "2031-01-01T00:00:00+01:00")
            ok("L1b le vrai fichier (en-tête seul) : NON_JUGEABLE, chaque champ exigé nommé, jamais []",
               r["etat"] == "NON_JUGEABLE" and r["champs_en_defaut"] == C.champs_de_la_declaration_manquants(None)
               and r["engagee"] is None and r["declaration"] is None, r)
            ok("L1c la lecture rend exactement les clés du contrat LECTURE_DE_LA_DECLARATION",
               list(r) == C.LECTURE_DE_LA_DECLARATION, list(r))
        essai("L1", l1)

        def p():
            for champ in C.CHAMPS_CALCULES_DE_LA_DECLARATION:
                try:
                    D.preparer_une_declaration(d, dict(saisie, **{champ: "0123456789abcdef"}))
                    ok("P1 %s saisi à la main : refusé" % champ, False)
                except ValueError as ex:
                    ok("P1 %s saisi à la main : refusé en le nommant" % champ, champ in str(ex), ex)
            avant = datetime.now(ZoneInfo("Europe/Paris"))
            ligne = D.preparer_une_declaration(d, saisie)
            juge, signal = D.empreintes_du_code(d, module)
            date = datetime.fromisoformat(ligne["date_declaration"])
            ok("P2 empreintes calculées par programme, égales à celles du code",
               ligne["empreinte_code_juge"] == juge and ligne["empreinte_code_signal"] == signal, ligne)
            ok("P3 date calculée à l'horloge, heure de Paris avec décalage",
               date.tzinfo is not None and abs(date - avant) < timedelta(minutes=2)
               and date.utcoffset() == avant.utcoffset(), ligne["date_declaration"])
            try:
                D.preparer_une_declaration(d, dict(saisie, parametres_libres="trois"))
                ok("P4 forme fautive : refusée", False)
            except ValueError as ex:
                ok("P4 forme fautive (parametres_libres « trois ») : refusée en le nommant", "parametres_libres" in str(ex), ex)
            try:
                D.ajouter_une_declaration(d, dict(ligne, date_regle_univers="2099-01-01"))
                ok("P5 l'écrivain refuse une règle d'univers datée après la déclaration", False)
            except ValueError as ex:
                ok("P5 l'écrivain refuse une règle d'univers datée après la déclaration", "date_regle_univers" in str(ex), ex)
            D.ajouter_une_declaration(d, ligne)
            commit("declaration")
        essai("P", p)

        instant = (datetime.now(ZoneInfo("Europe/Paris")) + timedelta(days=1)).isoformat(timespec="seconds")

        def l2():
            r = D.lire_la_declaration(d, FICHE, instant)
            ok("L2 déclarée, engagée, empreintes égales : COMPLETE, [] calculé",
               r["etat"] == "COMPLETE" and r["champs_en_defaut"] == [] and r["engagee"] is True and r["raisons"] == [], r["raisons"])
            ok("L2b empreinte de la déclaration = sha256 de sa ligne CSV, 16 caractères",
               r["empreinte_de_la_declaration"] == hashlib.sha256(D.ligne_csv_de_la_declaration(r["declaration"])).hexdigest()[:16]
               and re.fullmatch(r"[0-9a-f]{16}", r["empreinte_de_la_declaration"] or ""), r["empreinte_de_la_declaration"])
            import inspect                 # mission REGARD tour 3 : la branche n'est plus un paramètre (lue dedans)
            ok("L3 la branche n'est pas un paramètre : signature (racine, fiche_id, instant_du_regard)",
               list(inspect.signature(D.lire_la_declaration).parameters) == ["racine", "fiche_id", "instant_du_regard"])
            # SANS BRANCHE PRINCIPALE, L'ANTÉRIORITÉ N'EST PAS PROUVÉE (⑧ de `lire_la_declaration`) : jamais le HEAD local
            sommet = subprocess.run(["git", "-C", d, "rev-parse", "refs/remotes/origin/main"], capture_output=True,
                                    text=True, check=True).stdout.strip()
            g("update-ref", "-d", "refs/remotes/origin/main")
            try:
                r = D.lire_la_declaration(d, FICHE, instant)
            finally:
                g("update-ref", "refs/remotes/origin/main", sommet)
            ok("L3b branche principale introuvable : NON_JUGEABLE, date_declaration, non engagée",
               r["champs_en_defaut"] == ["date_declaration"] and r["engagee"] is False
               and "introuvable" in " ".join(r["raisons"]), r["raisons"])
            r = D.lire_la_declaration(d, FICHE, "2020-01-01T00:00:00+01:00")
            ok("L4 regard antérieur à la déclaration : aucune ligne, NON_JUGEABLE, tous les champs",
               r["etat"] == "NON_JUGEABLE" and r["declaration"] is None and len(r["champs_en_defaut"]) == len(
                   C.champs_de_la_declaration_manquants(None)), r["champs_en_defaut"])
        essai("L2", l2)

        def l5():
            juge = os.path.join(d, "programmes/JUGE_DES_STRATEGIES.py")
            src = open(juge, encoding="utf-8").read()
            try:
                open(juge, "w", encoding="utf-8").write(src.replace('"""', '"""Texte ajouté. ', 1))
                r = D.lire_la_declaration(d, FICHE, instant)
                ok("L5 un texte du juge changé : l'empreinte tient, COMPLETE", r["etat"] == "COMPLETE", r["raisons"])
                open(juge, "w", encoding="utf-8").write(src + "\nX_B3 = 1\n")
                r = D.lire_la_declaration(d, FICHE, instant)
                ok("L5b du code du juge changé : NON_JUGEABLE, empreinte_code_juge",
                   r["champs_en_defaut"] == ["empreinte_code_juge"], r["raisons"])
            finally:
                open(juge, "w", encoding="utf-8").write(src)
            sig = os.path.join(d, module)
            src = open(sig, encoding="utf-8").read()
            try:
                open(sig, "w", encoding="utf-8").write(src + "\nX_B3 = 1\n")
                r = D.lire_la_declaration(d, FICHE, instant)
                ok("L6 du code du signal changé : NON_JUGEABLE, empreinte_code_signal",
                   r["champs_en_defaut"] == ["empreinte_code_signal"], r["raisons"])
                os.remove(sig)
                r = D.lire_la_declaration(d, FICHE, instant)
                ok("L6b module de signal disparu : NON_JUGEABLE, empreintes non recalculables",
                   r["etat"] == "NON_JUGEABLE" and "empreinte_code_signal" in r["champs_en_defaut"]
                   and "non recalculable" in " ".join(r["raisons"]), r["raisons"])
            finally:
                open(sig, "w", encoding="utf-8").write(src)
        essai("L5", l5)

        def base_de(fid, date="2026-11-11T10:00+01:00"):
            """La saisie complétée pour une fiche, ses empreintes calculées sur SON module (vides sans module).
            ① RÔLE — fabriquer une ligne juste. ② CONTEXTE D'APPEL — L7, L12. ③ ENTRÉE — `fid`, `date`.
            ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : un dictionnaire. [rend: 1] ⑥ TRAITEMENT — compléter.
            ⑦ UNITÉ — —. ⑧ POURQUOI — chaque fiche a son module. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit deux
            fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            m = fiches[fid].get("module_signal") or ""
            j, sg = D.empreintes_du_code(d, m) if m else ("f" * 16, "f" * 16)
            return dict(saisie, fiche_id=fid, date_declaration=date, empreinte_code_juge=j, empreinte_code_signal=sg)

        def l7():
            base = base_de("C5E10-OBS-V1")
            # UNE LIGNÉE ILLISIBLE CONTAMINE TOUTE FICHE, ET C'EST VOULU : depuis B2 tour 2 (f0ac1f0c) et la mission
            # REGARD, la portée du regard est « lignee » (donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv) ; la lignée est
            # l'UNION des champs `lignee` de toutes les déclarations, et une seule illisible rend TOUTE lignée inconnue
            # (TENIR_LE_REGISTRE_DES_ESSAIS.lignee_de_la_fiche, ⑨ ②, « côté strict, voulu ») → premier regard inconnu
            # → date_declaration en défaut pour chaque fiche. La ligne à lignée vide est donc jouée SEULE, puis
            # retirée : sinon elle rougit L8, L9 et L13 pour une raison qui n'est pas la leur (12-11-2026, 4 rouges).
            avant = open(chemin_decl, encoding="utf-8").read()
            ajouter_brut(dict(base, lignee="", parametres_libres="deux"))
            commit("ligne fautive tapée à la main")
            r = D.lire_la_declaration(d, "C5E10-OBS-V1", instant)
            raisons = dict(x.split(" : ", 1) for x in (r["raisons"] or []))
            ok("L7 ligne tapée à la main, lignée vide et réglages libres « deux » : lignee et parametres_libres nommés, "
               "et date_declaration par la lignée illisible (ensemble exact, ordre du contrat)",
               r["champs_en_defaut"] == ["date_declaration", "lignee", "parametres_libres"]
               and "lignée illisible" in raisons.get("date_declaration", "") and raisons.get("lignee") == "vide",
               r["raisons"])
            r = D.lire_la_declaration(d, FICHE, instant)
            ok("L7c la même ligne rend la lignée inconnue pour une AUTRE fiche, juste par ailleurs : date_declaration seul",
               r["champs_en_defaut"] == ["date_declaration"] and "lignée illisible" in " ".join(r["raisons"]),
               r["raisons"])
            open(chemin_decl, "w", encoding="utf-8").write(avant)
            commit("retrait de la ligne à lignée illisible")
            r = D.lire_la_declaration(d, FICHE, instant)
            ok("L7d la ligne retirée : l'autre fiche redevient COMPLETE", r["etat"] == "COMPLETE", r["raisons"])
            # une empreinte recopiée à la main, fausse
            ajouter_brut(dict(base_de("C5-EI-PARAMS"), empreinte_code_juge="0" * 16))
            # une fiche sans module de signal au registre
            ajouter_brut(base_de(sans_module))
            commit("lignes fautives")
            ok("L7b l'écrivain refuse la même ligne (une seule définition du défaut)",
               any("lignee" in x for x in D.defauts_d_une_declaration(dict(base, lignee="", parametres_libres="deux")))
               and any("parametres_libres" in x for x in D.defauts_d_une_declaration(dict(base, parametres_libres="deux"))))
            r = D.lire_la_declaration(d, "C5-EI-PARAMS", instant)
            ok("L8 empreinte du juge recopiée fausse : NON_JUGEABLE, empreinte_code_juge",
               r["champs_en_defaut"] == ["empreinte_code_juge"], r["raisons"])
            r = D.lire_la_declaration(d, sans_module, instant)
            ok("L9 fiche sans module de signal : NON_JUGEABLE, les deux empreintes non recalculables",
               r["champs_en_defaut"] == ["empreinte_code_juge", "empreinte_code_signal"], r["raisons"])
            # écrite sur le disque, pas commitée (puis retirée du disque)
            texte = open(chemin_decl, encoding="utf-8").read()
            ajouter_brut(base_de("C5E10-QA-V1"))
            r = D.lire_la_declaration(d, "C5E10-QA-V1", instant)
            ok("L10 écrite sur le disque, pas sur la branche : NON_JUGEABLE, date_declaration, non engagée",
               r["champs_en_defaut"] == ["date_declaration"] and r["engagee"] is False, r["raisons"])
            open(chemin_decl, "w", encoding="utf-8").write(texte)
            ok("L11 règle d'univers datée après la déclaration : défaut nommé",
               list(D.defauts_par_champ(dict(base, date_regle_univers="2026-11-12"))) == ["date_regle_univers"])
        essai("L7", l7)

        def l12():
            # REGARDÉE PUIS DÉCLARÉE : le premier regard (registre des essais) est commité avant la déclaration
            hyp = {"tp_pct": 4.0, "sl_pct": 2.5, "horizon": 20, "univers": ["AC"], "signal": ["f", "0123"],
                   "periode": "2001-01-02..2005-12-30", "bareme": "Fortuneo"}
            T.preenregistrer(d, "C5E10-QA-V1", hyp)      # le regard inscrit le sommet de main qu'il voit (ancre)
            commit("regard avant la declaration")
            ajouter_brut(base_de("C5E10-QA-V1", "2026-11-11T09:00+01:00"))
            commit("declaration apres le regard, datee avant")
            r = D.lire_la_declaration(d, "C5E10-QA-V1", instant)
            ok("L12 regardée puis déclarée : NON_JUGEABLE, date_declaration, non engagée",
               r["champs_en_defaut"] == ["date_declaration"] and r["engagee"] is False, r["raisons"])
            # DEUX LIGNES : la ligne engagée (la dernière sur la branche) est datée après l'instant et porte d'autres
            # années d'examen que celle que l'instant retient au fichier
            ajouter_brut(dict(base_de("C5-EI-PARAMS", "2030-06-01T10:00+01:00"), annees_d_examen="2001-01-02..2010-12-31"))
            commit("seconde ligne")
            r = D.lire_la_declaration(d, "C5-EI-PARAMS", "2030-01-01T00:00:00+01:00")
            ok("L13 ligne engagée datée après l'instant du regard : date_declaration (le défaut « années » est remplacé "
               "par l'égalité de la ligne engagée et de la dernière ligne, REGARD tour 3)",
               "date_declaration" in (r["champs_en_defaut"] or []) and r["engagee"] is True, r["raisons"])
            # LES DEUX DÉFAUTS PORTENT LE MÊME CHAMP : le champ seul laisse chacun masquer l'autre (S11, S12, S14
            # muets le 12-11-2026). Chaque raison est donc exigée, et la ligne rendue doit être l'ENGAGÉE.
            raison = next((x for x in r["raisons"] or [] if x.startswith("date_declaration : ")), "")
            ok("L13b la ligne écrite diffère de la ligne engagée : raison nommée",
               "diffère de celle que portait" in raison, r["raisons"])
            ok("L13c la ligne engagée est datée après l'instant du regard : raison nommée",
               "datée à l'instant du regard ou après" in raison, r["raisons"])
            ok("L13d la ligne rendue est l'engagée (2030-06-01), pas celle du disque à l'instant",
               (r["declaration"] or {}).get("date_declaration", "").startswith("2030-06-01"),
               (r["declaration"] or {}).get("date_declaration"))
        essai("L12", l12)

        def l14():
            r = D.lire_la_declaration(d, FICHE, "2031-01-01T00:00:00")
            ok("L14 instant sans décalage : ILLISIBLE, None (jamais [])",
               r["etat"] == "ILLISIBLE" and r["champs_en_defaut"] is None, r)
            texte = open(chemin_decl, encoding="utf-8").read()
            try:
                open(chemin_decl, "w", encoding="utf-8").write(texte.replace("fiche_id,", "fiche,", 1))
                r = D.lire_la_declaration(d, FICHE, instant)
                ok("L15 en-tête hors contrat : ILLISIBLE, None", r["etat"] == "ILLISIBLE" and r["champs_en_defaut"] is None, r)
                os.remove(chemin_decl)
                r = D.lire_la_declaration(d, FICHE, instant)
                ok("L16 fichier absent : ILLISIBLE, None", r["etat"] == "ILLISIBLE" and r["champs_en_defaut"] is None, r)
            finally:
                open(chemin_decl, "w", encoding="utf-8").write(texte)
        essai("L14", l14)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return res


def jouer(racine, sabotage):
    """Joue les cas sur une copie du code, sabotée ou non.
    ① RÔLE — un tour. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `racine`, `sabotage` (« Z0 » ou une clé de SABOTAGES).
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la liste des [nom, vert, détail]. [rend: 1] ⑥ TRAITEMENT —
    copier CODE dans /tmp/B3_code_*, appliquer, relancer en « --cas », effacer. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit et efface un dossier. ⑪ TERMINAISON — Rend la main ; lève LookupError si
    une cible de sabotage n'est pas présente une fois. [sort: non]"""
    copie = tempfile.mkdtemp(prefix="B3_code_")
    try:
        for f in CODE:
            os.makedirs(os.path.dirname(os.path.join(copie, f)), exist_ok=True)
            shutil.copy(os.path.join(racine, f), os.path.join(copie, f))
        for f, avant, apres in SABOTAGES.get(sabotage, []):
            p = os.path.join(copie, f)
            s = open(p, encoding="utf-8").read()
            if s.count(avant) != 1:
                raise LookupError("cible du sabotage %s présente %d fois : %r" % (sabotage, s.count(avant), avant[:60]))
            open(p, "w", encoding="utf-8").write(s.replace(avant, apres))
        try:
            r = subprocess.run([sys.executable, "-B", ICI, "--cas", copie, racine], capture_output=True, text=True,
                               timeout=300)
        except subprocess.TimeoutExpired:
            return [["dépassement de 300 s", False, ""]]
        try:
            return json.loads(r.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            return [["relance illisible", False, (r.stderr or r.stdout)[-300:]]]
    finally:
        shutil.rmtree(copie, ignore_errors=True)


def main(argv):
    """Joue Z0 puis les sabotages demandés.
    ① RÔLE — le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — « --cas » : jouer les
    cas et écrire leur JSON ; sinon Z0, puis les sabotages ; afficher. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731, R-734.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if argv[:1] == ["--cas"]:
        print(json.dumps(cas(argv[1], argv[2]), ensure_ascii=False))
        return 0
    if not argv:
        print("usage : EPREUVES_B3_DECLARATION_Mer_11-11-2026.py <racine> [--saboter | nom]")
        return 2
    racine = os.path.abspath(argv[0])
    for f in CODE + ("emp.py", "programmes/JUGE_DES_STRATEGIES.py", "donnees/DECLARATIONS_DATEES.csv",
                     "donnees/cac40_strategies.csv"):
        if not os.path.exists(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            return 2
    demandes = []
    if len(argv) > 1:
        demandes = list(SABOTAGES) if argv[1] == "--saboter" else [argv[1]]
        if any(s not in SABOTAGES for s in demandes):
            print("sabotage inconnu : %s" % argv[1])
            return 2
    z0 = jouer(racine, "Z0")
    rouges = [x for x in z0 if not x[1]]
    for nom, vert, det in z0:
        print("  %s  %s%s" % ("VERT " if vert else "ROUGE", nom, ("  — " + det) if (det and not vert) else ""))
    print("== Z0 : %d cas, %d rouge(s)" % (len(z0), len(rouges)))
    code = 1 if rouges else 0
    for s in demandes:
        try:
            r = jouer(racine, s)
        except LookupError as ex:
            print(ex)
            return 2
        mord = [n for n, v, _d in r if not v]
        print("  %s  %s — %s" % ("MORD " if mord else "MUET ", s, ", ".join(mord[:4]) if mord else "aucun cas ne rougit"))
        if not mord:
            code = 1
    print("VERDICT : %s" % ("conforme" if code == 0 else "NON CONFORME"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
