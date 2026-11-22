#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU VERSEMENT QUI DIT L'IDENTITÉ — Sam 14-11-2026 (Paris) — le vrai versement, sur les vraies données.

Simulation uniquement — aucun ordre réel.

① RÔLE — Prouver que `programmes/TENIR_L_HISTORIQUE.py`, lancé tel que le circuit du soir le lance, DIT une anomalie
  d'identité que le lecteur commun tolère (I-1) : à l'écran, et par la ligne `anomalies_d_identite=<n>` du fichier
  nommé par `GITHUB_OUTPUT`, sans changer son code ; et qu'il refuse d'écrire quand cette sortie ne s'écrit pas.
② CONTEXTE D APPEL — À la main avant toute livraison qui touche le versement ou la tolérance du lecteur ;
  `--saboter` joue chaque sabotage, qui doit faire rougir au moins un cas.
③ ENTRÉE — `sys.argv[1]` : la racine du dépôt ; `--saboter` facultatif.
④ CONDITIONS D ENTRÉE — Sous la racine : `programmes/`, `donnees/` (maître, incrément, tables d'identité),
  `gouvernance/` ; `git` installé ; environ 250 Mo libres sous le dossier temporaire.
⑤ SORTIE — UNE valeur : le code de sortie — 0 si Z0 est vert et, avec `--saboter`, si chaque sabotage rougit ; 1 si
  une attente tombe ; 2 si un sabotage ne s'applique pas, si une prémisse de données est fausse ou si la copie ne se
  fait pas (R-734). [rend: 1]
⑥ TRAITEMENT — ① une copie jetable de `programmes/`, `donnees/`, `gouvernance/`, dont la DERNIÈRE séance du maître est
  retirée (l'incrément la porte encore : une vraie séance à verser ; N-3 de Cowork, 15-11-2026), enregistrée dans un
  dépôt git neuf (le versement relit `HEAD:donnees/cours_maitre.csv`) · ② pour chaque jeu, remettre la copie à son
  enregistrement, saboter le versement copié, puis jouer : P1 la vraie ligne de Peugeot S.A. (48) avec sa fin écrite
  « 2021-1-15 » → code 0, sortie `anomalies_d_identite=1`, l'anomalie et « le passage rougira » à l'écran, la séance
  VERSÉE (toutes ses lignes au maître) · P2 la table telle quelle → code 0, `anomalies_d_identite=0`, rien à l'écran,
  la séance versée · P5 la faute, `GITHUB_OUTPUT` absente → code 0, l'anomalie dite, « RIEN ne rougira », jamais « le
  passage rougira », la ligne `anomalies_d_identite=1` affichée, la séance VERSÉE (N-10 de Cowork) · P6 la faute,
  `GITHUB_OUTPUT` posée mais vide → code 1, l'anomalie dite, maître inchangé · P7 la faute, `GITHUB_OUTPUT` faite
  d'espaces → code 1, l'anomalie dite, maître inchangé (N-6 de Cowork) · P8 la table telle quelle, `GITHUB_OUTPUT`
  vide → code 1, « aucune anomalie d'identité ce soir », maître inchangé (remarque de Cowork) · P3 la faute,
  `--verifier` → code 0, `anomalies_d_identite=1`, maître inchangé · P4 la faute, `GITHUB_OUTPUT` désignant un dossier
  → code 1, « SORTIE DU PAS IMPOSSIBLE », l'anomalie dite, maître inchangé (N-10). Les sabotages T8, V1, V2, V3
  (RELU 38b7e4a3 de Cowork, 15-11-2026) survivaient au jeu d'avant ; V4, V5 tiennent les deux remarques : chacun mord désormais pour sa propre raison.
⑦ UNITÉ — Des codes de sortie, des nombres d'anomalies.
⑧ POURQUOI — K-1 de Cowork (14-11-2026) : sur fabd8224, le versement avec cette faute sortait à l'identique d'un soir
  sans faute (« SORTIES_IDENTIQUES »). R-731 et R-732 : épreuve sur une vraie ligne, sabotages qui mordent. Le chemin
  dans le circuit (le pas de fin qui rougit) est éprouvé par `EPREUVES_DU_PAS_DE_VERSEMENT` (W8 à W11), et la
  concordance des noms par `EPREUVES_DES_SORTIES_DES_PAS`.
⑨ CE QUI CLOCHE — La copie ne porte pas `temoins/` ni `etudes/` : le versement n'en lit rien aujourd'hui (mesuré le
  14-11-2026 : le versement tourne sur cette copie) ; s'il en lisait demain, P2 rougirait, du côté sûr. · La séance à
  verser est la dernière du maître du dépôt, à condition que l'incrément porte EXACTEMENT les mêmes couples (valeur,
  date) pour cette séance, ni plus ni moins (N-5 de Cowork : une ligne de plus dans l'incrément faisait rougir Z0 et
  accusait le programme) ; sinon PRÉMISSE FAUSSE, code 2.
⑩ EFFET — Une copie temporaire, effacée à la fin. N'écrit rien sous la racine.
⑪ TERMINAISON — Chaque versement est borné à 300 secondes.
  [sort: oui]
"""
import collections, inspect, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
VERSER = "programmes/TENIR_L_HISTORIQUE.py"
IDENT = "donnees/sources_indice/IDENTITES_DES_SOCIETES.csv"
VRAIE = "48,Peugeot S.A.,2000-01-03,2021-01-15,"
FAUTE = "48,Peugeot S.A.,2000-01-03,2021-1-15,"
TEXTE = "date de fin illisible « 2021-1-15 » pour la société 48 (Peugeot S.A.)"
SABOTAGES = {
    "Z0": [],
    "T1_jamais_dite": [("    if not dire_les_anomalies_d_identite(anomalies_d_identite):", "    if not True:")],
    "T2_anomalies_jetees": [('list(c.get("anomalies_d_identite") or [])', "[]")],
    "T3_compte_a_zero": [('"anomalies_d_identite=%d" % len(anomalies)', '"anomalies_d_identite=%d" % 0')],
    "T4_sortie_impossible_toleree": [('mais une anomalie ne serait pas vue par le circuit."))\n        return False\n',
                                      'mais une anomalie ne serait pas vue par le circuit."))\n        return True\n')],
    # N-1 de Cowork (15-11-2026) : hors du circuit, l'écran ne promet plus un rouge ; une variable vide est une panne
    "T5_rouge_promis_hors_du_circuit": [('"le passage rougira" if quoi == "" else', '"le passage rougira" if True else')],
    "T6_variable_vide_prise_pour_absente": [('    if sortie is not None and not sortie.strip():\n        quoi = "GITHUB_OUTPUT est posée mais vide"\n    elif sortie is not None:',
                                             '    if False:\n        quoi = ""\n    elif sortie:')],
    # N-3 de Cowork (15-11-2026) : la séance est VERSÉE malgré la faute — un arrêt juste après l'avoir dite rougit P1
    "T7_arret_apres_l_avoir_dite": [("    if not dire_les_anomalies_d_identite(anomalies_d_identite):\n        sys.exit(1)\n",
                                     "    if not dire_les_anomalies_d_identite(anomalies_d_identite):\n        sys.exit(1)\n    sys.exit(0)\n")],
    # RELU 38b7e4a3 de Cowork (15-11-2026) : quatre sabotages qui survivaient au jeu d'avant (N-6, N-10)
    "T8_espaces_pris_pour_un_chemin": [("    if sortie is not None and not sortie.strip():", "    if sortie is not None and not sortie:")],
    "V1_panne_tait_l_anomalie": [('        for a in anomalies:\n            print(f"  ❌ ANOMALIE D\'IDENTITÉ : {a}")\n', "")],
    "V2_hors_circuit_ne_verse_pas": [('        print("  " + ligne + "  (GITHUB_OUTPUT absente : sortie du pas affichée seulement)")\n',
                                      '        print("  " + ligne + "  (GITHUB_OUTPUT absente : sortie du pas affichée seulement)")\n        sys.exit(0)\n')],
    # remarques de Cowork (RELU 38b7e4a3) : en panne, le geste qui lève l'anomalie, et un texte juste un soir sans anomalie
    "V4_panne_sans_ce_qui_la_leve": [('            print(f"     Ce qui la lève : corriger', '            print(f"     corriger')],
    "V5_panne_parle_d_une_anomalie_absente": [('if anomalies else\n                 "aucune anomalie', 'if True else\n                 "aucune anomalie')],
    # RELU Cowork du 15-11-2026 (N-12, N-15) : textes de la panne et du soir normal, chacun tenu par son cas
    "X1_panne_dit_la_seance_versee": [("ce soir la séance N'EST PAS versée : réparer d'abord la sortie du pas.", "la séance du soir est versée.")],
    "X2_hors_panne_sans_ce_qui_la_leve": [('    if anomalies:\n        print(f"     Ce qui la lève : corriger la ligne de la société nommée dans {IDENTITES_A_CORRIGER} "\n              f"(décision de Jean-Luc) ; la séance du soir est versée.")\n',
                                           '    if False:\n        pass\n')],
    "X4_panne_sans_anomalie_dite_comme_sans": [('if anomalies else\n                 "aucune anomalie', 'if False else\n                 "aucune anomalie')],
    "X5_panne_ce_qui_la_leve_sans_anomalie": [('        if anomalies:\n            print(f"     Ce qui la lève', '        if True:\n            print(f"     Ce qui la lève')],
    "V3_hors_circuit_ligne_tue": [('        print("  " + ligne + "  (GITHUB_OUTPUT absente : sortie du pas affichée seulement)")\n', "        pass\n")],
}
MAITRE = "donnees/cours_maitre.csv"
INCREMENT = "donnees/claude_cours_nouveaux.csv"
DERNIERE = ["", 0]   # (date de la séance retirée du maître de la copie, nombre de lignes), posé par `principal`
GIT = dict(os.environ, GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false")


def sh(c, cwd):
    """Lance une commande git dans la copie et rend son résultat. ① RÔLE — Un appel. ② CONTEXTE D APPEL — `copier`,
    `remettre`. ③ ENTRÉE — `c` : la liste d'arguments ; `cwd` : le dossier. ④ CONDITIONS D ENTRÉE — git installé.
    ⑤ SORTIE — UNE valeur : le CompletedProcess. [rend: 1] ⑥ TRAITEMENT — subprocess.run, sortie capturée. ⑦ UNITÉ — —.
    ⑧ POURQUOI — Un seul endroit pour l'environnement git. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Celui de la commande.
    ⑪ TERMINAISON — Bornée à 600 secondes. [sort: non]"""
    return subprocess.run(c, cwd=cwd, env=GIT, capture_output=True, text=True, timeout=600)


def comparer_les_couples(portes, retires, derniere):
    """Compare les couples (valeur, date) portés par l'incrément à ceux retirés du maître, et nomme l'écart.

    ① RÔLE — La comparaison de la prémisse (N-5), isolée pour être éprouvée seule (N-40). ② CONTEXTE D APPEL —
    `copier`, et `cas_n17`. ③ ENTRÉE — deux listes de couples et la date de la séance. ④ CONDITIONS D ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : un TEXTE nommant les couples en plus et en moins (un doublon compte), ou "" si égaux.
    [rend: 1] ⑥ TRAITEMENT — `collections.Counter` des deux listes, différences, trois premiers. ⑦ UNITÉ — —.
    ⑧ POURQUOI — N-17 (RELU Cowork du 15-11-2026) : un set() masquait un doublon. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — —.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if sorted(portes) == sorted(retires):
        return ""
    cp, cr = collections.Counter(portes), collections.Counter(retires)
    plus = sorted((cp - cr).elements())[:3]
    moins = sorted((cr - cp).elements())[:3]
    return (f"l'incrément ne porte pas exactement les {len(retires)} couple(s) (valeur, date) de la séance {derniere} "
            f"retirés du maître : {len(portes)} porté(s) ; en plus {plus} ; en moins {moins}")


def cas_n17(sabote):
    """Éprouve N-17 : un doublon dans l'incrément doit être nommé. [rend: 1] Rend "" si tenu, sinon le défaut.

    ① RÔLE — Le cas qui tient la correction N-17 (N-40). ② CONTEXTE D APPEL — `principal`. ③ ENTRÉE — `sabote` :
    vrai pour rejouer la fonction avec l'ancien set(). ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : texte.
    ⑥ TRAITEMENT — couples fictifs (A, B ; A en double), appel, recherche du doublon dans le texte. ⑦ UNITÉ — —.
    ⑧ POURQUOI — Sans lui, défaire N-17 laissait tout vert. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — —. ⑪ TERMINAISON — Rend la main.
    """
    f = comparer_les_couples
    if sabote:
        src = inspect.getsource(comparer_les_couples).replace(
            "collections.Counter(portes), collections.Counter(retires)",
            "collections.Counter(set(portes)), collections.Counter(set(retires))")
        ns = {"collections": collections}
        exec(src, ns)
        f = ns["comparer_les_couples"]
    t = f([("A", "d"), ("A", "d"), ("B", "d")], [("A", "d"), ("B", "d")], "d")
    return "" if "en plus [('A', 'd')]" in t else f"doublon non nommé : {t!r}"


def copier(d):
    """Copie ce que lit le versement dans `d`, et l'enregistre dans un dépôt git neuf.

    ① RÔLE — La copie de travail. ② CONTEXTE D APPEL — Le programme principal, une fois. ③ ENTRÉE — `d` : un dossier
    vide. ④ CONDITIONS D ENTRÉE — Les trois dossiers sous la racine. ⑤ SORTIE — UNE valeur : un TEXTE (la prémisse
    fausse) si le maître n'a pas de dernière séance, ou si l'incrément ne porte pas EXACTEMENT ses couples (valeur,
    date) ; sinon le triplet (lignes retirées, date de la séance, vrai si la copie est enregistrée). [rend: 1]
    ⑥ TRAITEMENT — copytree des trois dossiers, retrait de la dernière séance du maître (N-3), comparaison des couples
    (valeur, date) retirés à ceux de l'incrément pour cette date (N-5), git init, add, commit. ⑦ UNITÉ — —.
    ⑧ POURQUOI — Le versement relit la version enregistrée du maître. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Écrit `d`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    for x in ("programmes", "donnees", "gouvernance"):
        shutil.copytree(os.path.join(DEPOT, x), os.path.join(d, x), symlinks=True)
    # N-3 de Cowork (15-11-2026) : la DERNIÈRE séance du maître est retirée avant l'enregistrement ; l'incrément la porte
    # encore, il y a donc une vraie séance à verser (sinon « 0 ligne ajoutée » et « maître inchangé » ne prouvent rien).
    m = os.path.join(d, MAITRE)
    lignes = open(m, encoding="utf-8").read().splitlines(True)
    derniere = max(l.split(",")[1] for l in lignes[1:] if l.count(",") >= 2)
    garde = [lignes[0]] + [l for l in lignes[1:] if l.split(",")[1:2] != [derniere]]
    open(m, "w", encoding="utf-8").write("".join(garde))
    a_verser = len(lignes) - len(garde)
    if not a_verser:
        return "le maître n'a pas de dernière séance"
    # N-5 de Cowork (15-11-2026) : l'incrément doit porter EXACTEMENT les couples (valeur, date) retirés — une ligne en
    # plus (une valeur que le maître n'a pas ce jour-là) ou en moins changerait ce que verse le programme sain, et Z0
    # rougirait en accusant le programme. C'est une prémisse de données : code 2, pas 1.
    retires = sorted(tuple(l.split(",")[:2]) for l in lignes[1:] if l.split(",")[1:2] == [derniere])
    inc = open(os.path.join(d, INCREMENT), encoding="utf-8").read().splitlines()
    portes = sorted(tuple(l.split(",")[:2]) for l in inc[1:] if l.split(",")[1:2] == [derniere])
    texte = comparer_les_couples(portes, retires, derniere)
    if texte:
        return texte
    return a_verser, derniere, all(sh(c, d).returncode == 0 for c in (["git", "init", "-q"], ["git", "add", "-A"],
               ["git", "-c", "user.name=e", "-c", "user.email=e@e", "commit", "-qm", "copie"]))


def remettre(d, sab, faute):
    """Remet la copie à son enregistrement, puis sabote le versement et pose la faute si le cas le demande.

    ① RÔLE — L'état de départ d'un cas. ② CONTEXTE D APPEL — `jouer`. ③ ENTRÉE — `d` : la copie ; `sab` : les
    remplacements ; `faute` : vrai pour poser la fin de Peugeot « 2021-1-15 ». ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE —
    UNE valeur : None si tout s'applique, sinon le texte de ce qui ne s'applique pas. [rend: 1] ⑥ TRAITEMENT —
    git checkout et clean, remplacements à ancre unique. ⑦ UNITÉ — —. ⑧ POURQUOI — Chaque cas part du même état.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Réécrit des fichiers de la copie. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sh(["git", "checkout", "-q", "--", "."], d)
    sh(["git", "clean", "-qfd"], d)
    for chemin, a, b in [(VERSER, a_, b_) for a_, b_ in sab] + ([(IDENT, VRAIE, FAUTE)] if faute else []):
        p = os.path.join(d, chemin)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            return f"ancre absente ou multiple dans {chemin} : {a[:60]!r}"
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return None


def jouer(d, sab, faute, verifier=False, sortie="fichier"):
    """Lance le vrai versement dans la copie et rend son code, sa sortie de pas, son écran et l'état du maître.

    ① RÔLE — Un cas P1 à P8. ② CONTEXTE D APPEL — `jeu`. ③ ENTRÉE — la copie, les remplacements, la faute, les
    options. ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : un dictionnaire (code, sortie, ecran, maitre_touche),
    ou un texte si l'état de départ ne se pose pas. [rend: 1] ⑥ TRAITEMENT — remettre, lancer
    `python3 -I programmes/TENIR_L_HISTORIQUE.py <copie> [--verifier]` avec `GITHUB_OUTPUT` posé. ⑦ UNITÉ — —.
    ⑧ POURQUOI — Le programme tel que le circuit le lance. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Le versement écrit dans la
    copie. ⑪ TERMINAISON — Borné à 300 secondes. [sort: non]
    """
    pb = remettre(d, sab, faute)
    if pb:
        return pb
    s = os.path.join(d, "..", "sortie_du_pas")
    env = {k: v for k, v in GIT.items() if k != "GITHUB_OUTPUT"}
    if sortie == "dossier":
        os.makedirs(s + "_dossier", exist_ok=True)
        s = s + "_dossier"
    elif sortie == "fichier":
        open(s, "w").close()
    if sortie in ("fichier", "dossier"):
        env["GITHUB_OUTPUT"] = s
    elif sortie == "vide":
        env["GITHUB_OUTPUT"] = ""
    elif sortie == "espaces":                     # N-6 de Cowork : une variable faite d'espaces est vide, pas un chemin
        env["GITHUB_OUTPUT"] = "   "
    p = subprocess.run([sys.executable, "-I", VERSER, d] + (["--verifier"] if verifier else []), cwd=d,
                       env=env, capture_output=True, text=True, timeout=300)
    touche = sh(["git", "diff", "--quiet", "--", MAITRE], d).returncode != 0
    seance = sum(1 for l in open(os.path.join(d, MAITRE), encoding="utf-8") if l.split(",")[1:2] == [DERNIERE[0]])
    return dict(code=p.returncode, sortie=open(s).read().split() if sortie == "fichier" else None,
                ecran=p.stdout + p.stderr, maitre_touche=touche, seance=seance)


def jeu(d, sab):
    """Joue P1 à P8 et rend la liste des rouges, ou un texte si le jeu ne s'applique pas.

    ① RÔLE — Un jeu. ② CONTEXTE D APPEL — Le programme principal. ③ ENTRÉE — la copie, les remplacements.
    ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : la liste des rouges, ou un texte. [rend: 1] ⑥ TRAITEMENT —
    voir ⑥ du module. ⑦ UNITÉ — —. ⑧ POURQUOI — Voir ⑧ du module. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Ceux de `jouer`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    rouges = []
    n = DERNIERE[1]
    cas = [("P1 la fin de Peugeot « 2021-1-15 » : code 0, anomalies_d_identite=1, dite, « rougira », séance VERSÉE",
            dict(faute=True), lambda r: r["code"] == 0 and r["sortie"] == ["anomalies_d_identite=1"]
            and TEXTE in r["ecran"] and "le passage rougira" in r["ecran"] and "Ce qui la lève" in r["ecran"] and r["maitre_touche"] and r["seance"] == n),
           ("P2 la table telle quelle : code 0, anomalies_d_identite=0, rien à l'écran, séance versée",
            dict(faute=False), lambda r: r["code"] == 0 and r["sortie"] == ["anomalies_d_identite=0"]
            and "ANOMALIE D'IDENTITÉ" not in r["ecran"] and r["seance"] == n),
           ("P5 la faute, GITHUB_OUTPUT absente (hors du circuit) : code 0, dite, AUCUN rouge promis",
            dict(faute=True, sortie="absente"), lambda r: r["code"] == 0 and TEXTE in r["ecran"]
            and "le passage rougira" not in r["ecran"] and "RIEN ne rougira" in r["ecran"]
            and "anomalies_d_identite=1" in r["ecran"] and "Ce qui la lève" in r["ecran"] and r["maitre_touche"] and r["seance"] == n),   # N-10
           ("P6 la faute, GITHUB_OUTPUT posée mais vide : code 1, dite, rien n'est écrit",
            dict(faute=True, sortie="vide"), lambda r: r["code"] == 1 and "posée mais vide" in r["ecran"]
            and TEXTE in r["ecran"] and "Ce qui la lève" in r["ecran"] and "N'EST PAS versée" in r["ecran"]
            and "ces anomalies d'identité ne seraient pas vues" in r["ecran"] and "aucune anomalie" not in r["ecran"]
            and not r["maitre_touche"]),
           ("P8 la table telle quelle, GITHUB_OUTPUT posée mais vide : code 1, « aucune anomalie », rien n'est écrit",
            dict(faute=False, sortie="vide"), lambda r: r["code"] == 1 and "aucune anomalie d'identité ce soir" in r["ecran"]
            and "ANOMALIE D'IDENTITÉ :" not in r["ecran"] and "Ce qui la lève" not in r["ecran"] and not r["maitre_touche"]),
           ("P7 la faute, GITHUB_OUTPUT faite d'espaces : code 1, dite, rien n'est écrit",                 # N-6
            dict(faute=True, sortie="espaces"), lambda r: r["code"] == 1 and "posée mais vide" in r["ecran"]
            and TEXTE in r["ecran"] and "ces anomalies d'identité ne seraient pas vues" in r["ecran"]
            and "aucune anomalie" not in r["ecran"] and not r["maitre_touche"]),
           ("P3 la faute en --verifier : code 0, anomalies_d_identite=1",
            dict(faute=True, verifier=True), lambda r: r["code"] == 0 and r["sortie"] == ["anomalies_d_identite=1"]
            and not r["maitre_touche"]),
           ("P4 la faute, sortie du pas impossible à écrire : code 1, rien n'est écrit",
            dict(faute=True, sortie="dossier"), lambda r: r["code"] == 1
            and "SORTIE DU PAS IMPOSSIBLE" in r["ecran"] and TEXTE in r["ecran"]
            and "ces anomalies d'identité ne seraient pas vues" in r["ecran"] and "aucune anomalie" not in r["ecran"]
            and not r["maitre_touche"])]
    for nom, opt, attendu in cas:
        r = jouer(d, sab, **opt)
        if isinstance(r, str):
            return r
        if not attendu(r):
            rouges.append(f"{nom} · code {r['code']}, sortie {r['sortie']}, maître touché {r['maitre_touche']}, "
                          f"lignes de la séance {DERNIERE[0]} au maître {r['seance']} (attendu {n} si versée)")
    return rouges


def principal():
    """Le chef d'orchestre. ① RÔLE — Copier, jouer Z0 puis les sabotages, dire le verdict. ② CONTEXTE D APPEL — La
    ligne de commande. ③ ENTRÉE — `sys.argv`. ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : le code de sortie.
    [rend: 1] ⑥ TRAITEMENT — prémisse (la vraie ligne de Peugeot, une fois), copie, jeux. ⑦ UNITÉ — —. ⑧ POURQUOI —
    R-734 : ce qui n'a pas pu tourner rend un code non nul. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Une copie temporaire,
    effacée. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if open(os.path.join(DEPOT, IDENT), encoding="utf-8").read().count(VRAIE) != 1:
        print(f"PRÉMISSE FAUSSE : la ligne « {VRAIE}… » n'est plus une fois dans {IDENT} — rien n'est éprouvé")
        print("VERDICT : NON CONFORME (code 2)")
        return 2
    tmp = tempfile.mkdtemp(prefix="versement_identite_")
    d = os.path.join(tmp, "copie")
    try:
        c = copier(d)
        if isinstance(c, str):
            print(f"PRÉMISSE FAUSSE : {c} — rien n'est éprouvé")
            print("VERDICT : NON CONFORME (code 2)")
            return 2
        if not c[2]:
            print("COPIE IMPOSSIBLE — rien n'est éprouvé\nVERDICT : NON CONFORME (code 2)")
            return 2
        DERNIERE[:] = [c[1], c[0]]
        print(f"  séance à verser : {c[1]}, {c[0]} ligne(s) retirées du maître enregistré de la copie")
        code = 0
        # N-40 (RELU Cowork du 22-11-2026) : le cas qui tient N-17, et son sabotage (retour à set())
        r17 = cas_n17(False)
        print("== N17_doublon_nomme : " + ("vert (attendu)" if not r17 else f"rouge <-- ATTENDU VERT : {r17}"))
        code = 1 if r17 else code
        if "--saboter" in sys.argv:
            r17s = cas_n17(True)
            print("== X6_doublon_masque_par_set : " + ("1 rouge(s) (attendu)" if r17s else "vert <-- SABOTAGE NON VU"))
            code = 1 if not r17s else code
        for nom in (SABOTAGES if "--saboter" in sys.argv else ["Z0"]):
            rg = jeu(d, SABOTAGES[nom])
            if isinstance(rg, str):
                print(f"== {nom} : INAPPLICABLE ({rg})")
                code = 2
                continue
            bon = (rg == []) if nom == "Z0" else bool(rg)
            print(f"== {nom} : " + ("vert" if not rg else f"{len(rg)} rouge(s)")
                  + (" (attendu)" if bon else (" <-- ATTENDU VERT" if nom == "Z0" else " <-- SABOTAGE NON VU")))
            for r in rg:
                print("     " + r)
            if not bon:
                code = max(code, 1)
        print("VERDICT : " + ("tout est conforme" if code == 0 else f"NON CONFORME (code {code})"))
        return code
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(principal())
