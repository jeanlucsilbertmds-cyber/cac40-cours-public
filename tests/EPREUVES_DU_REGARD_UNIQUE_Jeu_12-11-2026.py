#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU REGARD UNIQUE — une seule inscription pour tout le système (mission REGARD du plan V7). Simulation
uniquement : on rejoue des cours FABRIQUÉS, aucun ordre réel n'est jamais passé. Jeudi 12-11-2026.

LE SENS EN TÊTE — R-505 ③ (registre des règles, gouvernance/REGISTRE_REGLES.md) : les années d'examen se regardent UNE
seule fois. Le superviseur R-759 de la porte J (rapport du 12-11-2026, 00h09, « LA MARCHE ») fait tenir ce regard par
UNE inscription : le registre des essais, sur la branche des regards du dépôt distant (`CONTRATS_DES_FICHIERS.
BRANCHE_DES_REGARDS`). L'écriture pousse avant de rendre la main ; la lecture lit l'union des entrées jamais ajoutées,
après `fetch`, et signale tout effacement ; `jouer` exige le reçu de l'inscription pour toute séance de la fenêtre du
regard unique ; la porte exige HEAD = la branche principale et un arbre propre ; git est lancé par UN lanceur, purgé des
variables de LIEU du dépôt et jamais de sa configuration. Ces épreuves rejouent le pas 8 de la marche sur ce qui a été
construit : A1 et A1b (regard effacé, clone neuf), deux jugements simultanés, une avance rapide qui efface, A3 (commit
antidaté), A4 (GIT_DIR, environnement d'un crochet), le témoin du transport configuré — plus la garde de `jouer`, le cas
M2 fermé, k sur la branche, l'arbre sali, D7 (`cas=None`), D8 (loi absente), les mesureurs au contrat. TOUR 2 (relecteur
REGARD R-D1, R-D3 à R-D6 ; superviseur REGARD, pas ③ et ④) : une fusion ordinaire qui perd une déclaration, une fusion
sur la branche des regards, une copie locale, la garde de `jouer_une_entree` et de `backtest_c5etendu10`, le reçu clos,
le registre abîmé (XS1), le commit vide (XS5).

Chaque cas tourne sur SON dépôt fabriqué par `fabriquer` de l'épreuve J (cours fabriqués 2024-2025, aucune année de la
fenêtre jouée sauf par la garde, sur une série plate qui ne donne aucun signal) ; le dépôt distant est un dépôt NU LOCAL
dans /tmp/REGARD_* — RIEN N'EST POUSSÉ À GITHUB.

① RÔLE — Prouver que l'inscription unique tient, et que chaque garde a des dents (R-731 : chaque sabotage doit mordre).
② CONTEXTE D'APPEL — À la main, ou par la certification qui lance chaque fichier de tests/ avec la racine :
  `python3 -B tests/EPREUVES_DU_REGARD_UNIQUE_Jeu_12-11-2026.py <racine>` (Z0) ; `… <racine> --saboter` (Z0 puis
  chaque sabotage, sur SON seul cas) ; `… <racine> --sabotage=NOM` (répétable). Ce programme se relance en
  « --cas <dépôt> <cas> » dans un processus à part.
③ ENTRÉE — La ligne de commande.
④ CONDITIONS D'ENTRÉE — git ; sous la racine : programmes/, tests/EPREUVES_J_PORTE_D_ENTREE_Mer_11-11-2026.py,
  tests/EPREUVES_DU_JUGE_PAR_LE_LECTEUR_Mar_27-10-2026.py et les fichiers que copie l'épreuve J.
⑤ SORTIE — Code 0 si Z0 est vert et que chaque sabotage joué mord ; 1 sinon ; 2 si l'usage est faux ou une cible de
  sabotage introuvable (R-734).
⑥ TRAITEMENT — Pour chaque cas (et chaque sabotage) : fabriquer un dépôt neuf (épreuve J), appliquer le sabotage à SA
  copie, le commiter et le pousser au dépôt nu local (la porte exige un arbre propre), relancer « --cas », effacer.
⑦ UNITÉ — Des cas.
⑧ POURQUOI — R-731, R-732 (le registre des stratégies fabriqué prend pour modèle la vraie ligne C5E10-QA-V1, par
  `fabriquer`), R-734. Un cas par dépôt : une entrée inscrite ne s'efface pas de la branche, les cas ne se partagent
  donc rien.
⑨ CE QUI CLOCHE — ① Rien ne tourne sur GitHub : la règle « pas de forçage, pas de suppression » sur la branche des regards
  (J2 GITHUB, décision de Jean-Luc en attente) n'est pas éprouvée ; seul un clone qui connaissait la branche voit une
  suppression. ② Les deux jugements « simultanés » sont rejoués dans l'ordre qui les fait se bloquer (deux inscriptions,
  puis deux lectures) : un ordre où le premier lit avant que le second écrive laisse passer le premier, à juste titre.
  ③ Le coût réseau d'un `fetch` par lecture n'est pas mesuré sur GitHub. ④ Un appelant du même processus passe outre
  (limite J1, écrite) : aucun cas ne prétend le contraire.
⑩ EFFET — Crée puis efface des dossiers /tmp/REGARD_ep_* ; lance git et python ; aucun accès à GitHub.
⑪ TERMINAISON — Chaque relance est bornée à 300 s.
  [sort: oui — code de sortie]
"""

import ast
import csv
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.abspath(__file__)
PORTE = "programmes/JUGER_UNE_FICHE.py"
ESSAIS = "programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
CONTRAT = "programmes/CONTRATS_DES_FICHIERS.py"
EPREUVE_J = "tests/EPREUVES_J_PORTE_D_ENTREE_Mer_11-11-2026.py"
EPREUVE_M2 = "tests/EPREUVES_DU_JUGE_PAR_LE_LECTEUR_Mar_27-10-2026.py"

# LES SABOTAGES : nom → (fichier de la copie, texte visé présent UNE fois, remplacement, cas qui DOIT rougir).
# Chacun retire la CONDITION que son cas éprouve.
SABOTAGES = {
    "RS01_lecture_sans_la_branche": (ESSAIS, "    sommet, raison = _sommet_distant(racine)\n    if sommet is None:\n"
                                             "        return {}, [\"registre des essais illisible : \" + raison]",
                                     "    return {}, []\n    sommet, raison = _sommet_distant(racine)\n    if sommet is None:\n"
                                     "        return {}, [\"registre des essais illisible : \" + raison]", "A1b"),
    "RS02_reference_locale_crue": (ESSAIS, '    code, _s, err = lancer_git(racine, ["fetch", "--quiet", "--no-tags", distant, '
                                           '"%s:%s" % (ref, suivi)])',
                                   '    code, _s, err = 0, b"", ""', "SIMUL"),
    "RS03_union_reduite_au_sommet": (ESSAIS, "    fichiers = {}\n    if objets:",
                                     "    au_sommet = git(\"ls-tree\", \"--name-only\", sommet, dossier + \"/\")[1].decode()\n"
                                     "    objets = {f: b for f, b in objets.items() if f in au_sommet}\n"
                                     "    fichiers = {}\n    if objets:", "FF"),
    "RS04_ajout_seul_muet": (ESSAIS, "    defauts += historique_en_ajout_seul(racine, sommet)\n", "", "FF"),
    "RS05_commit_au_dessus_de_la_branche_admis": (PORTE, "    if shas[0] != shas[1]:", "    if False:", "A3"),
    "RS06_arbre_sale_admis": (PORTE, "    if sortie.strip():\n        return False, \"arbre de travail non propre",
                              "    if False:\n        return False, \"arbre de travail non propre", "SALE"),
    # RS07 suit le texte du juge depuis la correction E-3 (12-11-2026) : la branche lue est la variable `branche`
    "RS07_k_lu_sur_head": (JUGE, 'git("rev-list", "-1", "--before=" + date_declaration, branche, "--",',
                           'git("rev-list", "-1", "--before=" + date_declaration, "HEAD", "--",', "K"),
    "RS08_environnement_herite": (ESSAIS, "    return {k: v for k, v in os.environ.items() if k not in lieux}",
                                  "    return dict(os.environ)", "A4"),
    "RS09_configuration_purgee": (ESSAIS, 'lieux = {v for v in r.stdout.split() if not v.startswith("GIT_CONFIG")}',
                                  'lieux = {v for v in r.stdout.split()} | {k for k in os.environ if k.startswith("GIT_CONFIG")}',
                                  "TRANSPORT"),
    "RS10_garde_de_jouer_ouverte": (JUGE, "    if not premiere or str(premiere) > fin or str(derniere) < debut:\n        return\n",
                                    "    if True:\n        return\n", "GARDE"),
    "RS11_m2_lit_la_fenetre": (EPREUVE_M2, '            if l.split(",", 2)[1] > fin:', "            if True:", "M2"),
    "RS12_cas_de_l_appelant_aux_sorties": (PORTE, 'return rendre(cas=None, k="INCONNU", declaration_manquants=lecture["champs_en_defaut"])',
                                           'return rendre(cas=cas, k="INCONNU", declaration_manquants=lecture["champs_en_defaut"])',
                                           "D7"),
    "RS13_loi_absente_non_gardee": (PORTE, "    if not os.path.isfile(chemin_loi):", "    if False:", "D8"),
    # TOUR 2 (relecteur REGARD R-D1, R-D3, R-D4, R-D5, R-D6 ; superviseur REGARD, pas ③ et ④)
    # TOUR 3 (décision « Reparer » du 12-11-2026 à 09h04 ; superviseur ANCRAGE, pas 5 ; relecteur REGARD tour 2)
    "RS15_ancre_au_sommet_meme_apres_un_regard": ("programmes/DECLARER_UNE_STRATEGIE.py",
                                                  "    ancre = sommet\n    if regard:", "    ancre = sommet\n    if False:",
                                                  "ANCRE"),
    "RS24_ancre_non_ancetre_admise": ("programmes/DECLARER_UNE_STRATEGIE.py",
                                      "        if code != 0:\n            raise ValueError(\"ancre",
                                      "        if False:\n            raise ValueError(\"ancre", "NON_ANCETRE"),
    "RS25_ancre_inconnue_admise": ("programmes/DECLARER_UNE_STRATEGIE.py", "        if len(ancre) != 40:",
                                   "        if False:", "SANS_SOMMET"),
    "RS26_adresse_scp_non_ramenee": (ESSAIS, 'else u if u.startswith("/") else u.replace(":", "/", 1))', "else u)",
                                     "COPIE"),
    "RS27_fiche_sans_identifiant_admise": (JUGE, '_garde_du_regard_unique(fiche.get("id") or "", _premiere,',
                                           '_garde_du_regard_unique(fiche.get("id"), _premiere,', "GARDE"),
    # TOUR 4 (relecteur REGARD tour 3, T3-D1 ; superviseur POSTE EN RETARD, marche ③)
    "RS28_derniere_ligne_non_comparee": ("programmes/DECLARER_UNE_STRATEGIE.py",
                                         "            if ligne_csv_de_la_declaration(engagee) != ligne_csv_de_la_declaration(ligne):",
                                         "            if False:", "ANCRE"),
    "RS29_sans_fetch_de_la_branche_principale": (PORTE, 'code, _s, err = TR.lancer_git(racine, ["fetch", "--quiet",',
                                                 'code, _s, err = (lambda *a: (0, b"", ""))(racine, ["fetch", "--quiet",',
                                                 "RETARD"),
    "RS30_amont_injoignable_ignore": (PORTE, "    if code != 0:\n        return False, \"branche principale non récupérée",
                                      "    if False:\n        return False, \"branche principale non récupérée",
                                      "AMONT"),
    "RS16_regards_sans_histoire_entiere": (ESSAIS, 'git("log", "--full-history", "--diff-filter=A",',
                                           'git("log", "--diff-filter=A",', "FUSION_REGARDS"),
    "RS17_fusion_admise_sur_les_regards": (ESSAIS, "    if code_f != 0 or fusions.strip():", "    if False:",
                                           "FUSION_REGARDS"),
    "RS18_copie_prise_pour_le_depot_commun": (ESSAIS, "    if code != 0 or norme(lu) != norme(ligne[\"valeur\"]):",
                                              "    if False:", "COPIE"),
    "RS19_XS1_garde_ignore_les_defauts": (JUGE, '        if defauts:\n            raise RegardNonInscrit(cause + " : registre',
                                          '        if False:\n            raise RegardNonInscrit(cause + " : registre',
                                          "GARDE"),
    "RS20_recu_clos_admis": (JUGE, '        if any(x.get("nature") == "RESULTAT" and x.get("preenregistrement") == nom',
                             '        if False and any(x.get("nature") == "RESULTAT" and x.get("preenregistrement") == nom',
                             "GARDE"),
    "RS21_jouer_une_entree_sans_garde": (JUGE, '    _garde_du_regard_unique(None, str(serie[j]["date"]),',
                                         '    (lambda *a: None)(None, str(serie[j]["date"]),', "GARDE"),
    "RS22_backtest_sans_garde": ("programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py",
                                 "    if _d and min(_d) <= _fin and max(_d) >= _deb:", "    if False:", "GARDE"),
    "RS23_XS5_commit_vide_pousse": (ESSAIS, "        if code != 0 or len(commit) != 40:", "        if code != 0:", "VIDE"),
    "RS14_mesureur_retire_du_contrat": (CONTRAT, '    "kelly": "JUGER_UNE_FICHE._kelly",', '    "kelly": None,',
                                        "MESUREURS"),
}
ORDRE_DES_CAS = ("A1", "A1b", "SIMUL", "FF", "A3", "SALE", "K", "A4", "TRANSPORT", "GARDE", "M2", "D7", "D8",
                 "MESUREURS", "ANCRE", "NON_ANCETRE", "SANS_SOMMET", "RETARD", "AMONT", "FUSION_REGARDS", "COPIE",
                 "VIDE")


def charger(chemin, nom):
    """Charge un programme par son chemin, sous un nom donné.
    ① RÔLE — Prendre le module de la copie. ② CONTEXTE D'APPEL — `preparer`, `cas`. ③ ENTRÉE — chemin, nom.
    ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT —
    spec_from_file_location, rangé dans sys.modules. ⑦ UNITÉ — —. ⑧ POURQUOI — la copie, pas le dépôt. ⑨ CE QUI
    CLOCHE — —. ⑩ EFFET — exécute le module. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


def git(d, *args, env=None):
    """Lance git dans `d` et rend sa sortie texte ; lève si le code est non nul.
    ① RÔLE — Fabriquer l'état d'un cas (commit, clone, poussée vers le dépôt nu LOCAL). ② CONTEXTE D'APPEL — `preparer`,
    `cas`. ③ ENTRÉE — le dossier, les arguments, un environnement ou None. ④ CONDITIONS D'ENTRÉE — git. ⑤ SORTIE — UNE
    valeur : la sortie. [rend: 1] ⑥ TRAITEMENT — lancer, capturer. ⑦ UNITÉ — —. ⑧ POURQUOI — l'épreuve fabrique ; elle
    n'emploie PAS le lanceur qu'elle éprouve. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — git écrit dans `d`. ⑪ TERMINAISON — Rend
    la main ; lève CalledProcessError. [sort: non]"""
    return subprocess.run(["git", "-C", d, "-c", "user.name=epreuve REGARD", "-c", "user.email=e@regard"] + list(args),
                          capture_output=True, text=True, check=True, env=env).stdout.strip()


def preparer(source, sab):
    """Fabrique un dépôt neuf (épreuve J), y applique un sabotage, le commite et le pousse au dépôt nu local.
    ① RÔLE — Un dépôt par cas. ② CONTEXTE D'APPEL — `relancer`. ③ ENTRÉE — la racine source, un nom de sabotage ou
    None. ④ CONDITIONS D'ENTRÉE — le texte visé présent une fois. ⑤ SORTIE — UNE valeur : le dossier. [rend: 1]
    ⑥ TRAITEMENT — `fabriquer` de l'épreuve J (dépôt nu `.depot_nu`, branche principale poussée) ; copier l'épreuve M2
    dans le dépôt (exclue de git) ; saboter ; commiter, pousser, rapporter. ⑦ UNITÉ — —. ⑧ POURQUOI — la porte exige
    HEAD = la branche principale et un arbre propre : un sabotage laissé sur le disque rendrait tout INCONNU et
    « mordrait » pour une autre raison. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit /tmp/REGARD_ep_*. ⑪ TERMINAISON — Rend
    la main ; lève LookupError (cible) ou ce que lève git. [sort: non]"""
    d = tempfile.mkdtemp(prefix="REGARD_ep_")
    sys.path.insert(0, os.path.join(source, "tests"))
    J = charger(os.path.join(source, EPREUVE_J), "epreuve_j_pour_regard")
    J.fabriquer(source, d)
    os.makedirs(os.path.join(d, "tests"), exist_ok=True)
    shutil.copy(os.path.join(source, EPREUVE_M2), os.path.join(d, EPREUVE_M2))
    with open(os.path.join(d, ".git", "info", "exclude"), "a", encoding="utf-8") as f:
        f.write("\ntests/\n.clones/\n")
    if sab:
        fichier, a, b, _cas = SABOTAGES[sab]
        p = os.path.join(d, fichier)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            raise LookupError("sabotage %s : texte visé présent %d fois dans %s" % (sab, t.count(a), fichier))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
        if not fichier.startswith("tests/"):
            git(d, "add", "-A")
            git(d, "commit", "-q", "-m", "sabotage " + sab)
            git(d, "push", "-q", "origin", "main")
            git(d, "fetch", "-q", "origin")
    return d


def cas(d, nom):
    """Joue UN cas sur le dépôt fabriqué `d` et rend ses résultats.
    ① RÔLE — Le cœur de l'épreuve. ② CONTEXTE D'APPEL — `main` en « --cas ». ③ ENTRÉE — le dépôt, le nom du cas.
    ④ CONDITIONS D'ENTRÉE — fabriqué par `preparer`. ⑤ SORTIE — UNE liste de (nom, vert, détail). [rend: 1]
    ⑥ TRAITEMENT — voir chaque cas ci-dessous. ⑦ UNITÉ — —. ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE — voir
    l'en-tête. ⑩ EFFET — la porte inscrit au dépôt nu local ; des clones sous `d/.clones`. ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    sys.path.insert(0, os.path.join(d, "programmes"))
    P = charger(os.path.join(d, PORTE), "JUGER_UNE_FICHE")
    C = sys.modules["CONTRATS_DES_FICHIERS"]
    T = sys.modules["TENIR_LE_REGISTRE_DES_ESSAIS"]
    JS = sys.modules["JUGE_DES_STRATEGIES"]
    NT = C.MOTS_DU_VERDICT[2]
    res = []
    ok = lambda n, v, det="": res.append((n, bool(v), str(det)[:700]))
    juger = lambda racine, fiche, c="1": P.juger_une_fiche(racine, fiche, c)
    etat = lambda r, k: (r.get("controles", {}).get(k) or {}).get("etat")
    dit = lambda r: "%s · %s · %s · %s" % (r.get("verdict"), r.get("motif"), r.get("premier_controle_bloquant"),
                                          (r.get("lu") or {}).get("raisons"))
    bloque_par_le_regard = lambda r: (r["verdict"] == NT and r["motif"] == "DONNÉES DE CHOIX"
                                      and r["premier_controle_bloquant"] == "regard_unique")
    suivi = "refs/remotes/origin/" + C.BRANCHE_DES_REGARDS
    examen = "2024-01-02..2025-12-31"      # les années d'examen des déclarations fabriquées (épreuve J, DEBUT..FIN)
    hyp = {"tp_pct": "+4.0%", "sl_pct": "-2.5%", "horizon": "20", "univers": "AIR,TTE,DG", "signal": "épreuve",
           "periode": examen, "bareme": "épreuve"}

    def cloner(nom_du_clone):
        """Un clone NEUF du dépôt nu local, sous `d/.clones`. ① RÔLE — un second poste. ② CONTEXTE D'APPEL — A1b,
        SIMUL. ③ ENTRÉE — un nom. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : le dossier. [rend: 1]
        ⑥ TRAITEMENT — `git clone -b main`. ⑦ UNITÉ — —. ⑧ POURQUOI — A1b du relecteur J. ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — écrit sous `d`. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
        c = os.path.join(d, ".clones", nom_du_clone)
        os.makedirs(os.path.dirname(c), exist_ok=True)
        subprocess.run(["git", "clone", "-q", "-b", "main", os.path.join(d, ".depot_nu"), c], check=True,
                       capture_output=True)
        return c

    if nom == "A1":
        # A1 (relecteur J, D1) : le regard « effacé » de ce poste — ici sa référence de suivi — ne rend pas ③ PASSE
        r1 = juger(d, "BONNE-A")
        git(d, "update-ref", "-d", suivi)
        r2 = juger(d, "BONNE-A")
        ok("A1 BONNE-A rejugée après effacement de la référence locale des regards : BLOQUE par ③ (la branche fait foi)",
           etat(r1, "regard_unique") == "PASSE" and bloque_par_le_regard(r2), dit(r1) + " || " + dit(r2))
    elif nom == "A1b":
        # A1b (relecteur J) : un clone NEUF voit le regard du premier poste
        r1 = juger(d, "BONNE-A")
        c = cloner("neuf")
        r2 = juger(c, "BONNE-A")
        ok("A1b BONNE-A jugée sur un clone NEUF après un premier regard ailleurs : BLOQUE par ③",
           etat(r1, "regard_unique") == "PASSE" and bloque_par_le_regard(r2), dit(r1) + " || " + dit(r2))
    elif nom == "SIMUL":
        # deux jugements simultanés : deux inscriptions (la seconde refusée puis repassée sur le nouveau sommet), puis
        # deux lectures — l'ordre de la porte (préenregistrer, puis `bilan_de_la_fiche` en s'excluant par `sauf`)
        a, b = cloner("a"), cloner("b")
        na = T.preenregistrer(a, "BONNE-B", hyp)
        nb = T.preenregistrer(b, "BONNE-B", hyp)
        va, ra = T.regards_sur_les_annees(a, examen, "BONNE-B", sauf=(na,))
        vb, rb = T.regards_sur_les_annees(b, examen, "BONNE-B", sauf=(nb,))
        ok("SIMUL deux jugements simultanés de BONNE-B : chacun voit le regard de l'autre — les deux BLOQUE",
           va == [nb] and vb == [na], repr((va, ra, vb, rb)))
    elif nom == "FF":
        # une avance rapide qui EFFACE une entrée est acceptée par le serveur (superviseur J, M3) : la lecture la compte
        # toujours (union des ajouts) et l'ajout seul rougit
        T.preenregistrer(d, "BONNE-B", hyp)            # une autre entrée reste au sommet
        n = T.preenregistrer(d, "BONNE-C", hyp)
        retoucher = _retoucher(T)
        retoucher(d, n, None)
        entrees, defauts = T.lire_le_registre(d)
        sommet = git(d, "rev-parse", suivi)
        au_sommet = git(d, "ls-tree", "--name-only", sommet, "registre_essais/")
        r = juger(d, "BONNE-C")
        ok("FF entrée effacée par un commit en avance rapide : absente du sommet, TOUJOURS comptée, l'ajout seul rougit, "
           "③ n'est pas PASSE", n + ".json" not in au_sommet and n in entrees
           and any("effacée" in x for x in defauts) and etat(r, "regard_unique") != "PASSE",
           "%s · défauts %s · %s" % (n in entrees, defauts[:2], dit(r)))
    elif nom in ("A3", "K"):
        # A3 (relecteur J, D2) : un commit antidaté posé AU-DESSUS de la branche principale réduit le registre à BONNE-B
        chemin = os.path.join(d, C.REGISTRE_DES_STRATEGIES)
        lignes = open(chemin, encoding="utf-8").read().splitlines(True)
        open(chemin, "w", encoding="utf-8").write(lignes[0] + "".join(l for l in lignes[1:] if l.startswith("BONNE-B,")))
        env = dict(os.environ, GIT_AUTHOR_DATE="2026-11-01T18:00:00+01:00", GIT_COMMITTER_DATE="2026-11-01T18:00:00+01:00")
        git(d, "commit", "-q", "-am", "antidaté", env=env)
        if nom == "A3":
            r = juger(d, "BONNE-B")
            ok("A3 commit antidaté au-dessus de la branche principale : tout INCONNU (raison « branche »), aucun k lu",
               r["verdict"] == NT and r["motif"] == "MESURE MANQUANTE declaration"
               and "n'est pas" in str(((r.get("lu") or {}).get("raisons") or {}).get("branche"))
               and (r.get("lu") or {}).get("k") is None, dit(r))
        else:
            k, raison = JS.k_a_la_date(d, "2026-11-02T10:00+01:00", "aucun")
            ok("K k lu sur la branche principale, pas sur HEAD : 10 versions malgré le commit antidaté au-dessus",
               k.get("valeur") == 10, repr((k.get("valeur"), raison)))
    elif nom == "SALE":
        chemin = os.path.join(d, "gouvernance", "REGISTRE_REGLES.md")
        with open(chemin, "a", encoding="utf-8") as f:
            f.write("\nligne ajoutée sur le disque, jamais commitée\n")
        r = juger(d, "BONNE-A")
        ok("SALE la loi modifiée sur le disque (arbre sali) : tout INCONNU (raison « arbre de travail non propre »)",
           r["verdict"] == NT and "non propre" in str(((r.get("lu") or {}).get("raisons") or {}).get("branche")), dit(r))
    elif nom == "A4":
        # A4 (relecteur J, D3) et l'environnement d'un crochet (superviseur J, M5) : sans effet
        jumeau = cloner("jumeau")
        git(jumeau, "commit", "-q", "--allow-empty", "-m", "le jumeau avance")
        avant = dict(os.environ)
        try:
            os.environ.update(GIT_DIR=os.path.join(jumeau, ".git"), GIT_WORK_TREE=jumeau, GIT_INDEX_FILE=".git/index")
            code, haut, _e = T.lancer_git(d, ["rev-parse", "--show-toplevel"])
            est, raison = P._head_est_la_branche(d)
        finally:
            os.environ.clear()
            os.environ.update(avant)
        ok("A4 GIT_DIR, GIT_WORK_TREE et GIT_INDEX_FILE (crochet) hérités, désignant un jumeau en avance : git lit la "
           "racine, HEAD = branche", code == 0 and os.path.realpath(haut.decode().strip()) == os.path.realpath(d) and est,
           repr((code, haut[:80], est, raison)))
    elif nom == "TRANSPORT":
        # LE TÉMOIN : le dépôt distant n'est joignable QUE par une configuration d'environnement (GIT_CONFIG_*), comme
        # le proxy de cette machine ; l'inscription doit pousser par ce transport configuré
        n0 = int(os.environ.get("GIT_CONFIG_COUNT", "0") or 0)
        git(d, "remote", "set-url", "origin", "transport-de-l-epreuve:")
        J = charger(os.path.join(os.path.dirname(ICI), os.path.basename(EPREUVE_J)), "epreuve_j_transport")
        J.poser_le_depot_commun(d, "transport-de-l-epreuve:")     # le dépôt commun s'écrit sous son nom configuré
        os.environ.update({"GIT_CONFIG_COUNT": str(n0 + 1),
                           "GIT_CONFIG_KEY_%d" % n0: "url.%s.insteadOf" % os.path.join(d, ".depot_nu"),
                           "GIT_CONFIG_VALUE_%d" % n0: "transport-de-l-epreuve:"})
        sans = {k: v for k, v in os.environ.items() if not k.startswith("GIT_CONFIG")}
        sans_config = subprocess.run(["git", "-C", d, "ls-remote", "origin"], capture_output=True, env=sans).returncode
        try:
            n = T.preenregistrer(d, "BONNE-B", hyp)
            vu = n in T.lire_le_registre(d)[0]
            erreur = ""
        except Exception as e:
            vu, erreur = False, "%s: %s" % (type(e).__name__, e)
        ok("TRANSPORT témoin : sans la configuration d'environnement le dépôt distant est injoignable, avec elle "
           "l'inscription pousse et se relit", sans_config != 0 and vu, repr((sans_config, vu, erreur[:300])))
    elif nom == "GARDE":
        # LA GARDE DE `jouer` : une série PLATE datée dans la fenêtre — aucun signal, aucune opération, aucun gain calculé
        fiche = C.lire_les_fiches(d)["BONNE-B"]
        mnemo = JS.table_mnemoniques(JS.trouver(d, "REFERENTIEL_VALEURS"))
        mod_pos = JS.charger_module(JS.trouver(d, "MODULE_POSITIONS.py"), "pos_regard")
        signal = JS.signal_de_la_fiche(d, fiche)
        jours = ["2010-01-%02d" % j for j in range(4, 30) if j not in (9, 10, 16, 17, 23, 24)]
        barres = [{"date": x, "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0} for x in jours]
        cours = {mnemo.get(m, JS.cle_valeur(m)): list(barres) for m in JS.mnemoniques_de_l_univers(fiche["univers"])}
        periode = (jours[0], jours[-1])
        recu = T.preenregistrer(d, "BONNE-B", dict(hyp, periode="%s..%s" % periode))
        autre = T.preenregistrer(d, "BONNE-C", dict(hyp, periode="%s..%s" % periode))

        def essai(**k):
            """Joue et rend « ops » ou le nom de l'erreur. ① RÔLE — isoler. ② CONTEXTE D'APPEL — GARDE. ③ ENTRÉE —
            les arguments de `jouer`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT —
            appeler. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit la branche. ⑪ TERMINAISON —
            Rend la main. [sort: non]"""
            try:
                ops, _i = JS.jouer(fiche, cours, mnemo, signal, mod_pos, **k)
                return "ops=%d" % len(ops)
            except JS.RegardNonInscrit as e:
                return "REFUS " + str(e)[-90:]
        sans = essai(periode=periode)
        avec = essai(periode=periode, recu=(d, recu))
        faux = essai(periode=periode, recu=(d, "0000000000000000"))
        autre_fiche = essai(periode=periode, recu=(d, autre))
        plus_large = essai(periode=(jours[0], "2010-12-31"), recu=(d, recu))
        sans_periode = essai(recu=(d, recu))
        ok("GARDE jouer dans la fenêtre : sans reçu REFUS ; reçu valable joué (0 opération, série plate) ; reçu forgé, "
           "d'une autre fiche, période plus large, sans période (JUGER_SUR_8_CRITERES) : REFUS",
           sans.startswith("REFUS") and avec == "ops=0" and faux.startswith("REFUS") and autre_fiche.startswith("REFUS")
           and plus_large.startswith("REFUS") and sans_periode.startswith("REFUS"),
           " | ".join((sans, avec, faux, autre_fiche, plus_large, sans_periode)))
        # TOUR 2 (relecteur REGARD, R-D4, R-D5, R-D6/XS1) : les deux autres calculateurs gardés ; un reçu CLOS refusé ;
        # un registre abîmé refuse même un reçu neuf. Seuls des REFUS sont attendus : aucun gain n'est calculé.
        def refus(f):
            """Rend « REFUS … » ou ce que rend `f`. ① RÔLE — isoler. ② CONTEXTE D'APPEL — GARDE. ③ ENTRÉE — une
            fonction. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT — appeler. ⑦ UNITÉ — —.
            ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — celui de `f`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            try:
                return "CALCULÉ %r" % (f(),)
            except JS.RegardNonInscrit as e:
                return "REFUS " + str(e)[-80:]
        v0 = next(iter(cours))
        entree = refus(lambda: JS.jouer_une_entree(v0, cours[v0], 2, 0.04, 0.025, 20, mod_pos, None, "HIST_FORFAIT_300"))
        C5 = charger(os.path.join(d, "programmes", "MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"), "c5_regard")
        backtest = refus(lambda: C5.backtest_c5etendu10({C5.C5E10_UNIVERS[0]: list(barres)}, bareme="HIST_FORFAIT_300"))
        try:                                        # T2-D4 : une fiche SANS identifiant, avec le reçu d'une autre
            JS.jouer({k: v for k, v in fiche.items() if k != "id"}, cours, mnemo, signal, mod_pos, periode=periode,
                     recu=(d, autre))
            sans_id = "JOUÉ"
        except JS.RegardNonInscrit as e:
            sans_id = "REFUS " + str(e)[-80:]
        clos = T.preenregistrer(d, "BONNE-B", dict(hyp, periode="%s..%s" % periode))
        T.inscrire_le_resultat(d, clos, resultat={"essai": "clos"})
        recu_clos = essai(periode=periode, recu=(d, clos))
        neuf = T.preenregistrer(d, "BONNE-B", dict(hyp, periode="%s..%s" % periode, signal="neuf"))
        T._pousser_l_entree(d, "0123456789abcdef", b'{"abime": 1}\n')       # un défaut au registre
        abime = essai(periode=periode, recu=(d, neuf))
        ok("GARDE2 sans reçu : jouer_une_entree et backtest_c5etendu10 REFUS ; reçu clos par son résultat : REFUS ; "
           "registre abîmé, reçu neuf : REFUS ; fiche sans identifiant, reçu d'une autre : REFUS",
           entree.startswith("REFUS") and backtest.startswith("REFUS") and recu_clos.startswith("REFUS")
           and abime.startswith("REFUS") and sans_id.startswith("REFUS"),
           " | ".join((entree, backtest, recu_clos, abime, sans_id)))
    elif nom in ("ANCRE", "NON_ANCETRE", "SANS_SOMMET"):
        # L'ANCRAGE RÉPARÉ (décision de Jean-Luc du 12-11-2026 à 09h04, « Reparer » ; superviseur ANCRAGE, pas 5) : la
        # déclaration qui fait foi est celle que portait la branche principale au commit inscrit par le premier regard
        import csv as _csv
        D = sys.modules["DECLARER_UNE_STRATEGIE"]
        chemin = os.path.join(d, C.DECLARATIONS_DATEES)
        lire = lambda f: D.lire_la_declaration(d, f, P._maintenant())
        etat = lambda r: "%s %s" % (r["etat"], r["champs_en_defaut"])

        def ajouter(fiche_id, **champs):
            """Ajoute une ligne de déclaration copiée de celle de `fiche_id`, champs changés. ① RÔLE — fabriquer.
            ② CONTEXTE D'APPEL — ANCRE. ③ ENTRÉE — fiche, champs. ④ CONDITIONS D'ENTRÉE — la fiche est déclarée.
            ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — lire, copier, écrire. ⑦ UNITÉ — —. ⑧ POURQUOI — —.
            ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            lignes = list(_csv.DictReader(open(chemin, encoding="utf-8")))
            with open(chemin, "a", encoding="utf-8", newline="") as f:
                _csv.DictWriter(f, fieldnames=C.DECLARATION_DATEE).writerow(
                    dict([l for l in lignes if l["fiche_id"] == fiche_id][-1], **champs))

        def pousser():
            """Pousse main au dépôt nu local et rapporte. ① RÔLE — publier. ② CONTEXTE D'APPEL — ANCRE.
            ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — push, fetch.
            ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — pousse en local. ⑪ TERMINAISON — Rend la
            main ; lève. [sort: non]"""
            git(d, "push", "-q", "origin", "main")
            git(d, "fetch", "-q", "origin")
        if nom == "ANCRE":
            r0 = juger(d, "BONNE-A")                     # le regard : il inscrit le sommet de main qu'il voit
            # (b) fusions ordinaires APRÈS le regard : un essai annulé sur une branche de travail, puis une fusion
            # « -s ours » qui perd une déclaration (S5 et FUSION_DECL du relecteur)
            git(d, "checkout", "-q", "-b", "travail-x")
            ajouter("HASARD", reglages='{"essai": 1}')
            git(d, "commit", "-q", "-am", "essai")
            git(d, "revert", "--no-edit", "HEAD")
            git(d, "checkout", "-q", "main")
            git(d, "merge", "-q", "--no-ff", "-m", "fusion de l'essai annulé", "travail-x")
            git(d, "checkout", "-q", "-b", "travail-y")
            git(d, "commit", "-q", "--allow-empty", "-m", "travail")
            git(d, "checkout", "-q", "main")
            ajouter("HASARD", reglages='{"perdue": 1}')
            git(d, "commit", "-q", "-am", "une déclaration de plus")
            git(d, "checkout", "-q", "travail-y")
            git(d, "merge", "-q", "-s", "ours", "main", "-m", "fusion qui garde travail-y")
            git(d, "checkout", "-q", "main")
            git(d, "merge", "-q", "--ff-only", "travail-y")
            pousser()
            b = (etat(lire("BONNE-A")), etat(lire("BONNE-B")))
            # (a) une déclaration de BONNE-A écrite APRÈS son regard
            ajouter("BONNE-A", reglages='{"apres": 1}', date_declaration="2026-11-12T00:30+01:00")
            git(d, "commit", "-q", "-am", "déclaration postérieure au regard")
            pousser()
            a_ = lire("BONNE-A")
            # (c) son retour arrière sur main
            git(d, "revert", "--no-edit", "HEAD")
            pousser()
            c_ = etat(lire("BONNE-A"))
            ok("ANCRE fusions ordinaires après le regard : aucune fiche touchée ; déclaration postérieure au regard : "
               "date_declaration en défaut ; retour arrière : la déclaration d'avant fait foi",
               etat(r0["lu"]["declaration"]) == "COMPLETE []" and b == ("COMPLETE []", "COMPLETE []")
               and a_["etat"] == "NON_JUGEABLE" and "date_declaration" in a_["champs_en_defaut"]
               and c_ == "COMPLETE []", repr((b, etat(a_), c_)))
        elif nom == "NON_ANCETRE":
            juger(d, "BONNE-A")
            x = git(d, "commit-tree", "HEAD^{tree}", "-p", "HEAD~1", "-m", "main réécrite")
            git(d, "push", "-q", "-f", "origin", "%s:refs/heads/main" % x)
            git(d, "reset", "-q", "--hard", x)
            git(d, "fetch", "-q", "origin")
            r = lire("BONNE-A")
            ok("NON_ANCETRE l'ancre du regard n'est plus un ancêtre de la branche principale : ILLISIBLE (INCONNU)",
               r["etat"] == "ILLISIBLE" and "ancêtre" in str(r["raisons"]), repr((etat(r), r["raisons"][:1])))
        else:
            sommet = git(d, "rev-parse", "refs/remotes/origin/main")
            git(d, "update-ref", "-d", "refs/remotes/origin/main")
            n = T.preenregistrer(d, "BONNE-A", hyp)
            git(d, "update-ref", "refs/remotes/origin/main", sommet)
            r = lire("BONNE-A")
            ok("SANS_SOMMET un regard qui n'a pas pu inscrire le sommet de main : NON JUGEABLE (ancre inconnue)",
               T.lire_le_registre(d)[0][n]["sommet_principal"] == "INCONNU" and r["etat"] == "NON_JUGEABLE"
               and "ancre inconnue" in str(r["raisons"]), repr((etat(r), r["raisons"][:1])))
    elif nom in ("RETARD", "AMONT"):
        # T3-D1 (relecteur REGARD tour 3) et superviseur POSTE EN RETARD : la porte récupère la branche principale avant
        # de juger ; un poste en retard, ou un amont injoignable, rend INCONNU « branche » sans dépenser de regard
        nu = os.path.join(d, ".depot_nu")
        regards = lambda: git(nu, "ls-remote", ".", "refs/heads/" + C.BRANCHE_DES_REGARDS)
        if nom == "RETARD":
            a, b = cloner("a"), cloner("b")              # deux postes, un seul amont (dépôt nu local)
            import csv as _csv
            chemin = os.path.join(b, C.DECLARATIONS_DATEES)
            ligne_a = [l for l in _csv.DictReader(open(chemin, encoding="utf-8")) if l["fiche_id"] == "BONNE-A"][-1]
            with open(chemin, "a", encoding="utf-8", newline="") as f:
                _csv.DictWriter(f, fieldnames=C.DECLARATION_DATEE).writerow(dict(ligne_a, reglages='{"corrige": 1}'))
            git(b, "commit", "-q", "-am", "correction de la déclaration de BONNE-A, poussée AVANT tout regard")
            git(b, "push", "-q", "origin", "main")
            r = juger(a, "BONNE-A")                        # le poste a n'a pas récupéré la correction
        else:
            git(d, "remote", "set-url", "origin", os.path.join(d, ".amont_absent"))
            r = juger(d, "BONNE-A")
        ok("%s %s : INCONNU (raison « branche »), aucun regard dépensé" % (
            nom, "poste en retard sur la branche principale" if nom == "RETARD" else "amont injoignable"),
           r["verdict"] == NT and r["motif"] == "MESURE MANQUANTE declaration"
           and "branche" in ((r.get("lu") or {}).get("raisons") or {}) and not regards(), dit(r))
    elif nom == "FUSION_REGARDS":
        # R-D1, AT1 du relecteur : une fusion poussée en avance rapide qui ne garde qu'une entrée sur deux
        T.preenregistrer(d, "BONNE-B", hyp)
        perdue = T.preenregistrer(d, "BONNE-C", hyp)
        sommet = git(d, "rev-parse", suivi)
        garde_b = [l for l in git(d, "ls-tree", sommet, "registre_essais/").splitlines() if perdue not in l]
        sous = subprocess.run(["git", "-C", d, "mktree"], input="".join(l.split("\t")[0] + "\t" + l.split("/")[-1]
                                                                          + "\n" for l in garde_b),
                              capture_output=True, text=True, check=True).stdout.strip()
        haut = subprocess.run(["git", "-C", d, "mktree"], input="040000 tree %s\tregistre_essais\n" % sous,
                              capture_output=True, text=True, check=True).stdout.strip()
        orphelin = git(d, "commit-tree", haut, "-m", "orphelin")
        fusion = git(d, "commit-tree", haut, "-p", orphelin, "-p", sommet, "-m", "fusion")
        git(d, "push", "-q", "origin", "%s:refs/heads/%s" % (fusion, C.BRANCHE_DES_REGARDS))
        entrees, defauts = T.lire_le_registre(d)
        ok("FUSION_REGARDS une fusion en avance rapide qui perd une entrée : l'entrée reste COMPTÉE, et la fusion est "
           "signalée", perdue in entrees and any("fusion" in x for x in defauts), repr((perdue in entrees, defauts[:2])))
    elif nom == "COPIE":
        # R-D3 : une copie locale (geste ordinaire des épreuves et de la certification) n'inscrit ni ne lit ; un reçu
        # pris dans une copie est refusé
        nom_d = T.preenregistrer(d, "BONNE-B", hyp)
        copie = os.path.join(d, ".clones", "copie")
        os.makedirs(os.path.dirname(copie), exist_ok=True)
        subprocess.run(["git", "clone", "-q", d, copie], check=True, capture_output=True)
        _e, defauts = T.lire_le_registre(copie)
        try:
            T.preenregistrer(copie, "BONNE-B", hyp)
            inscrit = "INSCRIT"
        except RuntimeError as e:
            inscrit = "REFUS " + str(e)[-80:]
        try:
            JS._garde_du_regard_unique("BONNE-B", "2010-01-04", "2010-01-29", ("2010-01-04", "2010-01-29"),
                                       (copie, nom_d))
            garde = "PASSE"
        except JS.RegardNonInscrit as e:
            garde = "REFUS " + str(e)[-80:]
        # T2-D6 : l'adresse SSH « à la scp » du dépôt commun est le même dépôt ; un autre dépôt ne l'est pas
        J = charger(os.path.join(os.path.dirname(ICI), os.path.basename(EPREUVE_J)), "epreuve_j_copie")
        J.poser_le_depot_commun(copie, "https://github.com/proprietaire/depot")
        git(copie, "remote", "set-url", "origin", "git@github.com:proprietaire/depot.git")
        scp = T._depot_commun(copie)[0]
        git(copie, "remote", "set-url", "origin", "git@github.com:proprietaire/autre.git")
        autre = T._depot_commun(copie)[0]
        ok("COPIE une copie locale : lecture en défaut, inscription refusée, reçu pris dans la copie refusé ; "
           "adresse scp du dépôt commun admise, d'un autre dépôt refusée",
           any("dépôt commun" in x for x in defauts) and inscrit.startswith("REFUS") and garde.startswith("REFUS")
           and scp and not autre, " | ".join((str(defauts[:1]), inscrit, garde, str((scp, autre)))))
    elif nom == "VIDE":
        # XS5 du relecteur : un commit-tree qui rend un nom VIDE ne doit jamais devenir « git push origin :<branche> »
        n = T.preenregistrer(d, "BONNE-B", hyp)
        vrai_git_de = T.git_de

        def git_de_vide(racine):
            """Un lanceur dont `commit-tree` rend un nom vide. ① RÔLE — simuler l'échec silencieux. ② CONTEXTE D'APPEL
            — VIDE. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : la fonction. [rend: 1]
            ⑥ TRAITEMENT — envelopper. ⑦ UNITÉ — —. ⑧ POURQUOI — XS5. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main. [sort: non]"""
            g = vrai_git_de(racine)
            return lambda *a, **k: (0, b"") if "commit-tree" in a else g(*a, **k)
        T.git_de = git_de_vide
        try:
            T._pousser_l_entree(d, "fedcba9876543210", b"{}\n")
            leve = False
        except RuntimeError:
            leve = True
        finally:
            T.git_de = vrai_git_de
        existe = git(d, "ls-remote", "origin", "refs/heads/" + C.BRANCHE_DES_REGARDS)
        ok("VIDE un commit vide : l'inscription lève, la branche des regards existe toujours, l'entrée y reste",
           leve and existe and n in T.lire_le_registre(d)[0], repr((leve, bool(existe))))
    elif nom == "M2":
        # LE CAS M2 FERMÉ PAR UNE PROPRIÉTÉ : la copie passée au juge ne porte aucune séance de la fenêtre
        texte = open(os.path.join(d, EPREUVE_M2), encoding="utf-8").read()
        arbre = ast.parse(texte)
        fn = next(n for n in arbre.body if isinstance(n, ast.FunctionDef) and n.name == "copie_sans_la_fenetre")
        espace = {}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), "copie_sans_la_fenetre", "exec"), espace)
        source = os.path.join(d, ".clones", "cours_avec_la_fenetre.csv")
        os.makedirs(os.path.dirname(source), exist_ok=True)
        maitre = open(os.path.join(d, "donnees", "cours_maitre.csv"), encoding="utf-8").read().splitlines(True)
        with open(source, "w", encoding="utf-8") as f:
            f.write(maitre[0])
            for jour in ("1999-12-30", "2005-06-01", "2023-12-29"):
                f.write("AIRBUS,%s,1,1,1,1,1,google\n" % jour)
            f.writelines(maitre[1:])
        garde, ecarte, trous, dans = espace["copie_sans_la_fenetre"](source, os.path.join(d, ".clones", "copie.csv"),
                                                                    C.fenetre_du_regard_unique())
        ok("M2 la copie de l'historique passée au juge : aucune séance de la fenêtre, des lignes gardées, deux trous",
           dans == 0 and garde > 0 and trous == 2 and ecarte == 3, repr((garde, ecarte, trous, dans)))
    elif nom == "D7":
        r1, r2 = juger(d, "SANS-DECL", "1"), juger(d, "SANS-DECL", "2")
        e1 = {k: v["etat"] for k, v in r1["controles"].items()}
        e2 = {k: v["etat"] for k, v in r2["controles"].items()}
        ok("D7 sortie anticipée (sans déclaration) : le cas de l'appelant ne change aucun état rendu", e1 == e2,
           repr({k: (e1[k], e2[k]) for k in e1 if e1[k] != e2.get(k)}))
    elif nom == "D8":
        git(d, "rm", "-q", "gouvernance/REGISTRE_REGLES.md")
        git(d, "commit", "-q", "-m", "loi retirée")
        git(d, "push", "-q", "origin", "main")
        git(d, "fetch", "-q", "origin")
        try:
            r = juger(d, "BONNE-A")
            ok("D8 registre des règles absent : INCONNU (raison « table »), jamais FileNotFoundError",
               r["verdict"] == NT and "table" in ((r.get("lu") or {}).get("raisons") or {}), dit(r))
        except Exception as e:
            ok("D8 registre des règles absent : INCONNU (raison « table »), jamais FileNotFoundError", False,
               "%s: %s" % (type(e).__name__, e))
    elif nom == "MESUREURS":
        fonctions, raisons = P._mesureurs()
        ok("MESUREURS déclarés au contrat et résolus par la porte (kelly → JUGER_UNE_FICHE._kelly) ; la porte n'a plus de "
           "dictionnaire MESUREURS", fonctions.get("kelly") is P._kelly and not hasattr(P, "MESUREURS") and not raisons,
           repr((sorted(fonctions), raisons)))
    else:
        ok("cas inconnu " + nom, False)
    return res


def _retoucher(T):
    """Rend la fonction de l'épreuve du bloc 5a qui pousse une retouche ou un effacement en avance rapide.
    ① RÔLE — Ne pas récrire ce que l'épreuve du bloc 5a fait déjà (R-708). ② CONTEXTE D'APPEL — le cas FF.
    ③ ENTRÉE — le module du registre. ④ CONDITIONS D'ENTRÉE — l'épreuve du bloc 5a à côté de ce fichier.
    ⑤ SORTIE — UNE valeur : f(dossier, nom, octets ou None). [rend: 1] ⑥ TRAITEMENT — extraire `retoucher_sur_la_branche`
    du texte de l'épreuve (sans l'exécuter tout entière). ⑦ UNITÉ — —. ⑧ POURQUOI — l'épreuve du bloc 5a joue des cas à
    son chargement. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    chemin = os.path.join(os.path.dirname(ICI), "EPREUVES_B_DU_BLOC_5A_Mer_11-11-2026.py")
    arbre = ast.parse(open(chemin, encoding="utf-8").read())
    fn = next(n for n in arbre.body if isinstance(n, ast.FunctionDef) and n.name == "retoucher_sur_la_branche")
    espace = {"os": os}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "retoucher_sur_la_branche", "exec"), espace)
    return lambda d, nom, octets: espace["retoucher_sur_la_branche"](d, T, nom, octets)


def relancer(source, sab, nom):
    """Prépare un dépôt, relance « --cas » sur un cas, rend ses résultats, efface le dépôt.
    ① RÔLE — un processus et un dépôt par cas. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — source, sabotage ou None, cas.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : liste de (nom, vert, détail). [rend: 1] ⑥ TRAITEMENT —
    `preparer`, relancer (300 s), effacer. ⑦ UNITÉ — —. ⑧ POURQUOI — les modules ont les mêmes noms d'un cas à l'autre.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — /tmp/REGARD_ep_*. ⑪ TERMINAISON — Rend la main ; lève LookupError. [sort: non]"""
    d = preparer(source, sab)
    try:
        try:
            r = subprocess.run([sys.executable, "-B", ICI, "--cas", d, nom], capture_output=True, text=True,
                               timeout=300, cwd=d)
        except subprocess.TimeoutExpired:
            return [(nom, False, "plus de 300 s")]
        try:
            return [tuple(x) for x in json.loads(r.stdout.strip().splitlines()[-1])]
        except (ValueError, IndexError):
            return [(nom, False, (r.stderr or r.stdout)[-700:])]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    """Joue Z0 (chaque cas), puis les sabotages demandés, chacun sur SON cas.
    ① RÔLE — Le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — « --cas » : un cas, sa
    sortie JSON ; sinon Z0, puis les sabotages ; un sabotage MORD si son cas rougit. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731,
    R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if argv[:1] == ["--cas"]:
        print(json.dumps(cas(argv[1], argv[2]), ensure_ascii=False))
        return 0
    if not argv:
        print(__doc__)
        return 2
    source = os.path.abspath(argv[0])
    choisis = [a.split("=", 1)[1] for a in argv if a.startswith("--sabotage=")]
    if "--saboter" in argv:
        choisis = list(SABOTAGES)
    if any(s not in SABOTAGES for s in choisis):
        print("sabotage inconnu : %s" % [s for s in choisis if s not in SABOTAGES])
        return 2
    code = 0
    for nom in ORDRE_DES_CAS:
        for n, vert, det in relancer(source, None, nom):
            print("  %s  %s%s" % ("VERT " if vert else "ROUGE", n, "" if vert else "\n         " + det))
            code = code or (0 if vert else 1)
    print("== Z0 : %d cas, %s" % (len(ORDRE_DES_CAS), "tous verts" if code == 0 else "ROUGE"))
    for sab in choisis:
        vise = SABOTAGES[sab][3]
        try:
            r = relancer(source, sab, vise)
        except LookupError as e:
            print(e)
            return 2
        mord = any(not v for _n, v, _d in r)
        print("  %s %s — %s" % ("MORD  " if mord else "SURVIT", sab, r[0][0] + ("" if mord else " (reste vert)")))
        code = code or (0 if mord else 1)
    print("VERDICT : %s" % ("conforme" if code == 0 else "NON CONFORME"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
