#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py — Mer 11-11-2026 (Paris), tour 2 le 11-11-2026 vers 23h50. Simulation
uniquement.
EN ESSAI · épreuve · Rôle : éprouver `programmes/TRIER_LES_VARIANTES.py` (plan V7, bloc 5l ① ; A-541 fonction ③),
l'option `--cours=` de `programmes/JOUER_LES_VERSIONS.py` (bloc 5l ⑤), sa fin de période calculée (bloc 5g) et sa
partie de réglage coupée par le module de jugement (relecteur neuf du 11-11-2026, D1).

USAGE
    python3 tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py <racine>                 les épreuves
    python3 tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py <racine> --sabotages     + chaque sabotage
    python3 tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py <racine> --un-sabotage=S3

① RÔLE — Prouver, sur de vraies lignes, que le tri ne lit que la partie de réglage (aucune séance des 30 % gardés
  pour le jugement ne change son choix), garde exactement les versions qui passent le critère, n'en garde jamais une
  sans opération, compte chaque version une fois par son empreinte, refuse des essais joués dans des conditions
  différentes, lit son critère au REGISTRE puis au fichier provisoire et refuse ce qui est illisible ; que JOUER lit
  `--cours=` comme le juge et le lui passe ; que la fin calculée est la plus tardive qui laisse « horizon + 1 »
  séances à chaque valeur, sans reculer au-delà du réglage lu ; puis que chaque sabotage fait rougir.
② CONTEXTE D'APPEL — À la main, par l'auteur, son relecteur et Cowork (boucle R-731). Aucune tâche du soir.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ; `--sabotages` ou `--un-sabotage=Sn` en option.
④ CONDITIONS D'ENTRÉE — Sous la racine : les deux programmes, le juge, le module de jugement, le contrat,
  `donnees/cours_maitre.csv`, la combinatoire de C5E10-OBS-V1 E01, le fichier réel d'avant le 11-11-2026
  `etudes/IND-001-RETEST/moulinette_a_blanc_2024-2026/RESULTATS_IND-001-RETEST_E01.csv`, et les deux réglages
  provisoires `donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv` et `RECUL_MAXIMUM_DE_LA_FIN.csv`.
⑤ SORTIE — Un code de sortie : 0 si tout passe (et, avec `--sabotages`, si chaque sabotage rougit) ; 1 sinon ; 2 si
  la racine est inutilisable (R-734). Une ligne par cas.
  [rend: 1]
⑥ TRAITEMENT — ① famille TRI (le vrai JOUER produit deux fichiers de résultats réels, sur les cours du maître coupés
  au 20-07-2026, l'un avec UNE séance des 30 % altérée ; faux REGISTRE dans des dossiers temporaires) · ② famille FIN
  (`fin_utilisable` contre une force brute, sur les vraies séries du maître, dont le cas réel d'Accor ; recul) ·
  ③ famille JOUER (sous-processus : options, `--cours=`, colonnes, garde-fous) · ④ avec sabotage : copier le
  programme visé dans un dossier temporaire, y remplacer UN texte (qui doit figurer une fois) pour neutraliser UNE
  condition, rejouer les seuls cas visés sur la copie, exiger l'échec.
⑦ UNITÉ — Des versions, des séances, des dates AAAA-MM-JJ, des euros.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction (instructions du projet, §7) ; un cas au moins
  vient d'une vraie ligne de fichier (R-732). Relecteur neuf du 11-11-2026 : D1 à D9 ont chacun un cas et un sabotage.
⑨ CE QUI CLOCHE — ① Le cas réel d'Accor tronque le maître au 10-11-2026 (l'état du 11-11-2026 à 19h53) : une
  révision d'une séance passée le fait rougir — voulu. ② Aucun jeu sur les 20 ans (`donnees/VALEURS_TTF.csv` sans
  liste pour 2001, mesuré le 11-11-2026). ③ Les volumes (9 800 versions) viennent du fichier réel d'avant le
  11-11-2026, complété ICI de colonnes recopiées (« _70 » = période entière) : c'est un fichier FABRIQUÉ pour éprouver
  le compte, dit dans chaque cas qui l'emploie. ④ Les sabotages de JOUER tournent sur une copie du programme, le juge
  restant celui de la racine.
⑩ EFFET — Crée et efface des dossiers temporaires ; lance `python3`. N'écrit rien sous la racine.
⑪ TERMINAISON — Sort lui-même. Un de ses appels peut-il ne pas revenir ? Non : 300 s au plus par sous-processus.
  [sort: oui]
"""
import bisect
import csv
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import types

sys.dont_write_bytecode = True
DELAI = 300
RACINE = None
P_TRI = "programmes/TRIER_LES_VARIANTES.py"
P_JOUER = "programmes/JOUER_LES_VERSIONS.py"
REEL_ANCIEN = "etudes/IND-001-RETEST/moulinette_a_blanc_2024-2026/RESULTATS_IND-001-RETEST_E01.csv"
COMB_C5 = "donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv"
P_JUGE = "programmes/JUGE_DES_STRATEGIES.py"
P_MJ = "programmes/MODULE_JUGEMENT.py"
CHEMINS = {}            # programme -> chemin joué (la racine, ou la copie sabotée)
DOSSIERS, CAS = [], []
SELECTION = None        # None : tous les cas ; sinon les seuls cas nommés (mode sabotage)
FIXTURE = {}

# Chaque sabotage : (programme, texte à remplacer, remplacement, cas qui doivent rougir, la condition neutralisée).
SABOTAGES = {
    "S1": (P_JOUER, "        commande.append(OPTION_COURS + cours)\n", "        pass\n", ["J5"],
           "le juge n'est plus lancé avec --cours="),
    "S2": (P_JOUER, "    if borne > fin_de_la_fiche:\n        return fin_de_la_fiche, None",
           "    if True:\n        return fin_de_la_fiche, None", ["F1"], "la fin n'est plus jamais ramenée"),
    "S3": (P_JOUER, "dates[-besoin] < borne:\n            borne, limite = dates[-besoin], m",
           "dates[-besoin + 1] < borne:\n            borne, limite = dates[-besoin + 1], m", ["F1"],
           "une séance de moins après la fin"),
    "S4": (P_JOUER, "if autre_cours is not None and not os.path.isfile(",
           "if autre_cours is not None and False and not os.path.isfile(", ["J1"],
           "l'existence du fichier de --cours= n'est plus contrôlée"),
    "S5": (P_JOUER, '"periode_debut": periode_jouee[0], "periode_fin": periode_jouee[1],',
           '"periode_debut": periode_jouee[0], "periode_fin": bornes[1],', ["J4"],
           "la fin écrite n'est plus la fin calculée"),
    "S6": (P_TRI, "            passe, non_mesurable = False, True", "            non_mesurable = True", ["T13"],
           "une case vide passe le critère"),
    "S7": (P_TRI, "variantes_essayees=essayees,", "variantes_essayees=len(gardees),", ["T1", "T2"],
           "le compte devient celui des retenues"),
    "S8": (P_TRI, "        if mauvais or len(statuts) > 1:", "        if False:", ["T7"],
           "le fichier du seuil peut se dire décidé sans date ni renvoi"),
    "S9": (P_TRI, "    if table is not None:\n", "    if table is not None and not os.path.exists(f_prov):\n", ["T4"],
           "le provisoire passe devant le REGISTRE"),
    "S10": (P_TRI, "    if annonces != {str(len(lignes))}:", "    if False:", ["T12"], "un fichier tronqué passe"),
    "S11": (P_JOUER, '    return c.get("embargo_seances"), c.get("res_70", {"n": 0})',
            '    return c.get("embargo_seances"), mod_jug._resume(ops)', ["J9", "T30"],
            "la partie de réglage n'est plus coupée : les 30 % entrent dans les colonnes « _70 »"),
    "S12": (P_TRI, "        if col not in contrat.COLONNES_DU_TRI:", "        if col not in contrat.RESULTATS_DES_VERSIONS:",
            ["T9"], "le critère peut lire une colonne de la période entière"),
    "S13": (P_TRI, "    if ops70.isdigit() and int(ops70) == 0:", "    if False:", ["T13"],
            "une version sans opération peut être retenue"),
    "S14": (P_TRI, "    return x if math.isfinite(x) else None", "    return x", ["T11", "T12"],
            "« nan » et « inf » sont des nombres"),
    "S15": (P_TRI, "        if len(valeurs) != 1:", "        if False:", ["T2"],
            "des essais joués dans des conditions différentes sont réunis"),
    "S16": (P_TRI, "                if e in vues:", "                if False:", ["T2", "T15"],
            "une même version est comptée deux fois"),
    "S17": (P_JOUER, "    if recul > recul_max:", "    if False:", ["J7"], "le recul de la fin n'est plus borné"),
    "S18": (P_JOUER, "    if marge[plus_court] < h_max + 1:", "    if False:", ["J6"],
            "le recompte de la marge ne garde plus rien"),
    "S19": (P_TRI, "        if courtes:", "        if False:", ["T11"], "une rangée courte du REGISTRE passe"),
    "S21": (P_JOUER, "    frontiere = mod_jug.frontiere_de_la_fiche(fiche, seances_lues, bornes)",
            "    frontiere = mod_jug.frontiere_de_la_fiche(fiche, seances_lues, None)", ["J10"],
            "JOUER prend sa frontière hors des bornes de la fiche (relecteur, tour 2, S21)"),
    "S22": (P_JOUER, "horizon=horizon, frontiere=frontiere)", "horizon=horizon, frontiere=frontiere, embargo_seances=0)",
            ["J10", "J9"], "JOUER retire l'embargo (relecteur, tour 2, S22)"),
    "S23": (P_JUGE, "frontiere=J.frontiere_de_la_fiche(fiche, seances, _bornes))",
            "frontiere=J.frontiere_de_la_fiche(fiche, seances, None))", ["J10"],
            "le juge prend sa frontière hors des bornes de la fiche"),
    "S24": (P_TRI, '    if attendue != par_fichier[0][0]["frontiere_70_30"]:', "    if False:", ["T16"],
            "le tri ne compare plus la frontière à celle du registre (N1)"),
    "S25": (P_TRI, '    if (ligne["periode_debut"], ligne["fin_ecrite_dans_la_fiche"]) != tuple(bornes):', "    if False:",
            ["T16"], "le tri ne voit plus qu'une fiche a changé de période"),
    "S26": (P_TRI, '    if emp != ligne["empreinte_des_cours"]:', "    if False:", ["T16"],
            "le tri ne voit plus que les cours ont changé"),
    "S27": (P_TRI, "                    if any(l0[c] != l[c] for c in CHIFFRES_D_UNE_VERSION):", "                    if False:",
            ["T17"], "deux résultats différents pour les mêmes réglages : le premier gagne en silence (N3)"),
    "S28": (P_TRI, "    if ops70.isdigit() and int(ops70) == 0:", '    if ops70 == "0":', ["T13"],
            "le texte « 0 » au lieu du nombre zéro (N4)"),
    "S29": (P_MJ,
            "    return cal[min(int(len(cal) * part), len(cal) - 1)]",
            "    return cal[min(int(len(cal) * part) + 1, len(cal) - 1)]", ["F11"],
            "la frontière calculée glisse d'une séance"),
    "S30": (P_MJ,
            "        if bornes and not (bornes[0] <= declaree <= bornes[1]):", "        if False:", ["F10"],
            "une frontière déclarée hors des bornes est acceptée"),
    "S31": (P_JOUER, "horizon=horizon, frontiere=frontiere)\n", "horizon=horizon, frontiere=None)\n", ["J11"],
            "X4 du relecteur : JOUER appelle la coupure sans la frontière reçue"),
    "S32": (P_JOUER, "    if ops and c.get(\"frontiere\") != frontiere:", "    if False:", ["J12"],
            "JOUER ne compare plus la coupe réelle à la frontière écrite (M1)"),
    "S33": (P_MJ, "        if declaree not in set(seances):", "        if False:", ["F10"],
            "une frontière déclarée qui n'est pas une séance est acceptée"),
    "S34": (P_MJ, "    if frontiere is None:\n        raise", "    if False:\n        raise", ["F12"],
            "la coupure accepte de ne pas recevoir de frontière"),
    "S35": (P_JOUER, "            if len(ligne) > i and ligne[i] <= fin:", "            if len(ligne) > i:", ["T16"],
            "l'empreinte porte sur tout le fichier de cours : le maître qui grandit rend le tri impossible (M2)"),
    "S36": (P_JOUER, "            if len(ligne) > i and ligne[i] <= fin:",
            "            if len(ligne) > i and ligne[i] <= fin[:8] + \"%02d\" % (int(fin[8:]) + 3):", ["T16"],
            "Y2 du relecteur, tour 4 : l'empreinte déborde de trois jours après la fin de la fiche (m3)"),
    "S37": (P_MJ, "    frontiere = cal[i_frontiere] if i_frontiere < len(cal) else frontiere\n", "    pass\n", ["F13"],
            "Y7 du relecteur, tour 4 : la coupure rend la frontière reçue au lieu de la séance coupée (m4)"),
    "S38": (P_JOUER, "        a_jouer = periode if periode is not None else bornes", "        a_jouer = bornes",
            ["J13", "J8"], "la fin calculée est ignorée, toute la fiche est jouée (relecteur de la fusion, défaut 2, "
            "13-11-2026)"),
    "S20": (P_JOUER, '("aucune opération" if not ref_jouee["n"] else', '("aucune opération" if False else', ["J8"],
            "« aucune opération » redevient un arrêt"),
}


def voulu(cas):
    """Dit si un cas doit être joué.
    ① RÔLE — Ne jouer, sous sabotage, que les cas visés. ② CONTEXTE D'APPEL — Chaque cas.
    ③ ENTRÉE — `cas` : son code (« T1 », « J4 »…). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai s'il faut le jouer. [rend: 1] ⑥ TRAITEMENT — Tout sans sélection, sinon la sélection.
    ⑦ UNITÉ — — ⑧ POURQUOI — Vingt sabotages ne doivent pas rejouer vingt fois tous les lancements de JOUER (cadre V7 :
    pas de série de plus de dix minutes). ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return SELECTION is None or cas in SELECTION


def noter(nom, ok, detail=""):
    """Note un cas.
    ① RÔLE — Garder le verdict d'un cas. ② CONTEXTE D'APPEL — Chaque cas. ③ ENTRÉE — `nom`, `ok`, `detail`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur. [rend: 0] ⑥ TRAITEMENT — ① ajouter à `CAS` · ② afficher.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un bilan unique en fin. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Une ligne affichée.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    CAS.append((nom, bool(ok)))
    print("  %s  %s%s" % ("OK    " if ok else "ÉCHEC ", nom, "" if ok else "  — " + str(detail)[:400]), flush=True)


def dossier():
    """Crée un dossier temporaire effacé à la fin.
    ① RÔLE — Isoler chaque cas. ② CONTEXTE D'APPEL — Les cas. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin. [rend: 1] ⑥ TRAITEMENT — `mkdtemp` sous /tmp, préfixe « tri_epreuve_ ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Rien sous la racine (cadre V7, point 3). ⑨ CE QUI CLOCHE — — ⑩ EFFET — Crée un dossier.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="tri_epreuve_", dir="/tmp")
    DOSSIERS.append(d)
    return d


def lancer(programme, *arguments):
    """Lance un programme depuis la racine, avec un délai.
    ① RÔLE — Un seul chemin de lancement. ② CONTEXTE D'APPEL — Les familles TRI et JOUER.
    ③ ENTRÉE — `programme` : P_TRI ou P_JOUER (remplacé par sa copie sabotée s'il y a lieu) · `arguments`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, la sortie (stdout et stderr). [rend: 2]
    ⑥ TRAITEMENT — `python3 -B`, cwd = la racine, délai `DELAI`. ⑦ UNITÉ — Secondes pour le délai.
    ⑧ POURQUOI — Les programmes s'éprouvent comme ils se lancent. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main ; délai dépassé = code 124. [sort: non]
    """
    try:
        r = subprocess.run([sys.executable, "-B", CHEMINS[programme]] + list(arguments), cwd=RACINE,
                           capture_output=True, text=True, timeout=DELAI)
    except subprocess.TimeoutExpired:
        return 124, "délai dépassé"
    return r.returncode, r.stdout + "\n" + r.stderr


def module(programme, nom):
    """Importe un programme par son chemin joué.
    ① RÔLE — Atteindre les fonctions pures. ② CONTEXTE D'APPEL — Les familles TRI et FIN.
    ③ ENTRÉE — `programme`, `nom` du module. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — `spec_from_file_location`. ⑦ UNITÉ — — ⑧ POURQUOI — Une copie sabotée doit être celle importée.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le haut du module. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sp = importlib.util.spec_from_file_location(nom, CHEMINS[programme])
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def ecrire(chemin, champs, lignes):
    """Écrit un CSV.
    ① RÔLE — Fabriquer les fichiers des cas. ② CONTEXTE D'APPEL — Les cas. ③ ENTRÉE — `chemin`, `champs`, `lignes`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le chemin. [rend: 1] ⑥ TRAITEMENT — DictWriter.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    with open(chemin, "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=champs)
        w.writeheader()
        w.writerows(lignes)
    return chemin


def lire(chemin):
    """Lit un CSV.
    ① RÔLE — Relire. ② CONTEXTE D'APPEL — Les cas. ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — DEUX valeurs : les champs, les lignes. [rend: 2] ⑥ TRAITEMENT — DictReader. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    r = csv.DictReader(open(chemin, encoding="utf-8-sig"))
    return list(r.fieldnames), list(r)


def fausse_racine(registre_texte=None, provisoire=None, autres=None):
    """Fabrique une racine en MIROIR du dépôt, où seuls quelques fichiers sont remplacés.
    ① RÔLE — Faire varier le critère ou le registre des stratégies sans toucher la racine.
    ② CONTEXTE D'APPEL — La famille TRI.
    ③ ENTRÉE — `registre_texte` : le texte du REGISTRE des règles (un texte sans marque si None) · `provisoire` :
      (champs, lignes) du fichier du seuil, ou None pour l'ôter · `autres` : {chemin relatif : texte} à remplacer.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le chemin de la fausse racine. [rend: 1]
    ⑥ TRAITEMENT — ① chaque fichier remplacé est écrit ; ② chaque dossier de la racine (hors .git) est un vrai
      dossier ; les fichiers de `programmes/` sont COPIÉS (5,5 Mo) ; chaque autre fichier est un lien symbolique
      vers celui de la racine.
    ⑦ UNITÉ — — ⑧ POURQUOI — Depuis le 12-11-2026, le tri relit le registre des stratégies, le juge, le module de
      jugement et les cours (N1) : une racine minimale ne suffit plus, et le disque ne permet pas une copie.
    ⑨ CE QUI CLOCHE — `trouver` du juge ne descend pas dans un dossier qui est un lien : tous les dossiers sont
      donc de vrais dossiers ici (environ 700 dossiers et 6 800 liens, moins d'une seconde). Et le juge refuse un
      module de signal dont le chemin réel sort de la racine (« lien hors racine ») : `programmes/` est copié.
    ⑩ EFFET — Écrit des fichiers et des liens temporaires. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = dossier()
    remplaces = {"gouvernance/REGISTRE_REGLES.md":
                 registre_texte if registre_texte is not None else "# REGISTRE\nAucun seuil du tri ici.\n",
                 "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv": None}
    remplaces.update(autres or {})
    for rep_, dossiers, fichiers in os.walk(RACINE):
        dossiers[:] = [x for x in dossiers if x != ".git"]
        rel = os.path.relpath(rep_, RACINE)
        os.makedirs(os.path.join(d, rel), exist_ok=True)
        for nom in fichiers:
            r = os.path.normpath(os.path.join(rel, nom))
            if r in remplaces or r == ".git":
                continue
            if r.startswith("programmes" + os.sep):
                # COPIÉS, pas liés : la porte du signal refuse un module dont le chemin réel sort de la racine
                shutil.copy2(os.path.join(RACINE, r), os.path.join(d, r))
            else:
                os.symlink(os.path.join(RACINE, r), os.path.join(d, r))
    for k, texte in remplaces.items():
        os.makedirs(os.path.join(d, os.path.dirname(k)), exist_ok=True)
        if texte is not None:
            open(os.path.join(d, k), "w", encoding="utf-8").write(texte)
    if provisoire is not None:
        ecrire(os.path.join(d, "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv"), *provisoire)
    return d


def resultats_reels():
    """Fait produire par le vrai JOUER deux fichiers de résultats réels, l'un sur des cours où UNE séance des 30 % change.
    ① RÔLE — La matière réelle des familles TRI et JOUER (R-732). ② CONTEXTE D'APPEL — Les cas T1, T16, T30, J9, J10.
    ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — La combinatoire de C5E10-OBS-V1 E01 et le maître existent.
    ⑤ SORTIE — UNE valeur : le dictionnaire (dossier, combinatoire, cours, cours_altere, date_alteree, resultats,
      resultats_altere). [rend: 1]
    ⑥ TRAITEMENT — ① trois versions réelles (0001, 0500, 0914 celle de la fiche) · ② le maître coupé au 20-07-2026 ·
      ③ jouer · ④ lire la frontière écrite · ⑤ copier les cours en abaissant de 10 % le plus bas de chaque valeur à la
      PREMIÈRE séance après la frontière (la plus proche des 70 % : un embargo retiré ou une frontière décalée la
      ferait entrer dans les colonnes « _70 », relecteur, tour 2, N2) · ⑥ rejouer. Une seule fois par lancement ;
      sous sabotage du tri, les fichiers du lancement parent sont repris (`EPREUVE_TRI_RESULTATS`).
    ⑦ UNITÉ — — ⑧ POURQUOI — Un fichier de résultats réel, avec sa partie de réglage, n'existe pas au dépôt.
    ⑨ CE QUI CLOCHE — Les fichiers de cours vivent sous /tmp ; JOUER les lit par un chemin relatif à la racine.
    ⑩ EFFET — Lance JOUER deux fois. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if FIXTURE:
        return FIXTURE
    d = os.environ.get("EPREUVE_TRI_RESULTATS") if CHEMINS[P_JOUER] == os.path.join(RACINE, P_JOUER) else None
    if not d:
        d = dossier()
        champs, comb = lire(os.path.join(RACINE, COMB_C5))
        trois = [dict(l, versions_dans_l_essai="3") for l in comb
                 if l["id_version"].split("-")[-1] in ("0001", "0500", "0914")]
        ecrire(os.path.join(d, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"), champs, trois)
        ch_c, cours = lire(os.path.join(RACINE, "donnees/cours_maitre.csv"))
        court = [l for l in cours if l["date"] <= "2026-07-20"]
        ecrire(os.path.join(d, "cours_au_20-07.csv"), ch_c, court)

        def jouer_sur(f_c, out):
            c, s = lancer(P_JOUER, ".", os.path.join(d, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"), os.path.join(d, out),
                          "--cours=" + os.path.relpath(os.path.join(d, f_c), RACINE))
            open(os.path.join(d, out + ".sortie"), "w", encoding="utf-8").write("code %d\n%s" % (c, s))
        jouer_sur("cours_au_20-07.csv", "R.csv")
        if not os.path.exists(os.path.join(d, "R.csv")):
            # JOUER a refusé (sous un sabotage, par exemple) : les cas qui lisent R.csv rougiront ; ceux qui ne lisent
            # que la combinatoire et les cours (J11) tournent quand même
            open(os.path.join(d, "date_alteree"), "w").write("")
            FIXTURE.update(dossier=d, combinatoire=os.path.join(d, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"),
                           cours=os.path.join(d, "cours_au_20-07.csv"), resultats=os.path.join(d, "R.csv"),
                           resultats_altere=os.path.join(d, "R_altere.csv"), date_alteree="")
            return FIXTURE
        frontiere = lire(os.path.join(d, "R.csv"))[1][0]["frontiere_70_30"]
        date = min(l["date"] for l in court if l["date"] > frontiere)
        altere = [dict(l, low=repr(0.9 * min(float(l["open"]), float(l["close"])))) if l["date"] == date else l
                  for l in court]
        os.makedirs(os.path.join(d, "a"))
        ecrire(os.path.join(d, "a", "cours_au_20-07.csv"), ch_c, altere)
        open(os.path.join(d, "date_alteree"), "w").write(date)
        jouer_sur("a/cours_au_20-07.csv", "R_altere.csv")
    FIXTURE.update(dossier=d, combinatoire=os.path.join(d, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"),
                   cours=os.path.join(d, "cours_au_20-07.csv"), resultats=os.path.join(d, "R.csv"),
                   resultats_altere=os.path.join(d, "R_altere.csv"),
                   date_alteree=open(os.path.join(d, "date_alteree")).read())
    return FIXTURE


def conditions_reelles():
    """Rend, pour IND-001-RETEST sur le maître, l'empreinte des cours et la frontière que le juge appliquera.
    ① RÔLE — Donner aux fichiers FABRIQUÉS de `volume` des conditions de jeu vraies, que le tri accepte.
    ② CONTEXTE D'APPEL — `volume`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — Le maître et la fiche existent.
    ⑤ SORTIE — DEUX valeurs : l'empreinte du maître, la frontière. [rend: 2]
    ⑥ TRAITEMENT — Par le juge et `frontiere_de_la_fiche` du module de jugement (la fonction éprouvée en F10-F11).
    ⑦ UNITÉ — — ⑧ POURQUOI — Les cas du compte ne portent pas sur la frontière ; T16 la refuse sur de vrais fichiers.
    ⑨ CE QUI CLOCHE — Emploie le code éprouvé pour fabriquer une donnée d'épreuve ; F11 le confronte à un calcul
      indépendant. ⑩ EFFET — Lit le maître. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if "conditions" not in FIXTURE:
        sys.path.insert(0, os.path.join(RACINE, "programmes"))
        import CONTRATS_DES_FICHIERS as C_
        import JUGE_DES_STRATEGIES as J
        fiche = C_.fiches_du_registre(os.path.join(RACINE, C_.REGISTRE_DES_STRATEGIES))["IND-001-RETEST"]
        bornes = J.porte_0(fiche)[2]
        mn = J.table_mnemoniques(J.trouver(RACINE, "REFERENTIEL_VALEURS"))
        cours, _ = J.lire_par_le_lecteur(RACINE, "donnees/cours_maitre.csv", mn)
        MJ = J.charger_module(os.path.join(RACINE, "programmes", "MODULE_JUGEMENT.py"), "jug_epreuve")
        V = module(P_JOUER, "jouer_conditions")
        FIXTURE["conditions"] = (V.empreinte_des_cours_jusqu_a(os.path.join(RACINE, "donnees/cours_maitre.csv"),
                                                               bornes[1]),
                                 MJ.frontiere_de_la_fiche(fiche, {b["date"] for s in cours.values() for b in s}, bornes),
                                 bornes)
    return FIXTURE["conditions"]


def volume(champs_contrat, n=None, **changer):
    """Fabrique, à partir du fichier réel d'avant le 11-11-2026, un fichier au format du contrat.
    ① RÔLE — Éprouver le compte sur 9 800 vraies versions. ② CONTEXTE D'APPEL — Les cas T2 à T15.
    ③ ENTRÉE — `champs_contrat` : les champs du contrat · `n` : garder les n premières lignes · `changer` : colonnes
      à remplacer sur toutes les lignes. ④ CONDITIONS D'ENTRÉE — Le fichier réel existe.
    ⑤ SORTIE — UNE valeur : la liste des lignes. [rend: 1]
    ⑥ TRAITEMENT — Colonnes « _70 » recopiées de la période entière ; conditions communes VRAIES (fiche
      IND-001-RETEST au registre, maître, sa frontière), par `conditions_reelles`.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le compte et les refus ne dépendent pas de la coupure ; ce fichier est FABRIQUÉ et dit.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨ ③. ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    empreinte_maitre, frontiere, bornes = conditions_reelles()
    _, reel = lire(os.path.join(RACINE, REEL_ANCIEN))
    lignes = []
    for l in reel[:n] if n else reel:
        x = dict(l, periode_debut=bornes[0], fin_ecrite_dans_la_fiche=bornes[1], cours_joues="donnees/cours_maitre.csv",
                 empreinte_des_cours=empreinte_maitre, frontiere_70_30=frontiere, embargo_seances="21",
                 operations_70=l["operations"], reussite_pourcents_exacte_70=l["reussite_pourcents_exacte"],
                 gain_net_euros_70=l["gain_net_euros"])
        if n:
            x["versions_dans_l_essai"] = str(n)
        x.update(changer)
        lignes.append({c: x[c] for c in champs_contrat})
    return lignes


def famille_tri():
    """Éprouve le tri : la partie de réglage seule, le compte, le critère, les refus.
    ① RÔLE — Les cas T0 à T15. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête. ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — Chaque cas lance le tri (sous-processus) ou appelle ses fonctions, et compare à un calcul fait ICI.
    ⑦ UNITÉ — Des versions, des euros. ⑧ POURQUOI — Le compte, le partage et l'étanchéité aux 30 % sont les promesses.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance le tri ; écrit dans des dossiers temporaires.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sys.path.insert(0, os.path.join(RACINE, "programmes"))
    import CONTRATS_DES_FICHIERS as contrat
    C = list(contrat.RESULTATS_DES_VERSIONS)
    if voulu("T0"):
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, REEL_ANCIEN)
        noter("T0 vrai fichier d'avant le 11-11-2026 (9 800 versions, sans partie de réglage) : refusé",
              c == 1 and "champs absents" in s and "operations_70" in s and not os.path.exists(out), s)
    STATUT_DU_DEPOT = lire(os.path.join(RACINE, "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv"))[1][0]["statut"]
    if voulu("T1") or voulu("T30") or voulu("T16") or voulu("T17"):
        F = resultats_reels()
        _, reel = lire(F["resultats"])
        _, alt = lire(F["resultats_altere"])
    if voulu("T1"):
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, F["resultats"])
        att = {l["id_version"] for l in reel if int(l["operations_70"]) > 0 and float(l["gain_net_euros_70"]) > 0}
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T1 vrai fichier de JOUER (3 versions) : retenues = gain_70 > 0 calculé à part, 3 essayées, critère "
              "provisoire annoncé", c == 0 and len(reel) == 3 and {l["id_version"] for l in tri} == att and att
              and all(l["variantes_essayees"] == "3" and l["statut_du_critere"] == STATUT_DU_DEPOT for l in tri)
              and "gain_net_euros_70 > 0.0" in s and "CE SEUIL EST PROVISOIRE" not in s, s)
    if voulu("T30"):
        # D1 : une séance des 30 % altérée change la période ENTIÈRE (dents) mais ni la partie de réglage ni le tri.
        dents = [(a["operations"], a["gain_net_euros"]) for a in reel] != [(b["operations"], b["gain_net_euros"])
                                                                           for b in alt]
        o1, o2 = os.path.join(dossier(), "TRI.csv"), os.path.join(dossier(), "TRI.csv")
        c1, s1 = lancer(P_TRI, ".", o1, F["resultats"])
        c2, s2 = lancer(P_TRI, ".", o2, F["resultats_altere"])
        garde = lambda f: [{k: v for k, v in l.items() if k in contrat.COLONNES_DU_TRI or k == "id_version"}
                           for l in lire(f)[1]]
        noter("T30 la PREMIÈRE séance après la frontière altérée (%s) : la période entière change, le choix du tri ne "
              "change pas" % F["date_alteree"], dents and c1 == 0 and c2 == 0 and garde(o1) == garde(o2) and len(garde(o1)) > 0,
              "dents %s · %s · %s" % (dents, s1[-200:], s2[-200:]))
    if voulu("T2"):
        d = dossier()
        e01 = volume(C)
        f1 = ecrire(os.path.join(d, "R_E01.csv"), C, e01)
        # FABRIQUÉ : E02 = les mêmes réglages sous un autre essai et d'autres identifiants -> comptés une fois
        f2 = ecrire(os.path.join(d, "R_E02.csv"), C, [dict(l, essai="E02", id_version=l["id_version"].replace(
            "-E01-", "-E02-")) for l in e01])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, f1, f2)
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T2 la même combinatoire recopiée sous E02 : comptée UNE fois (9800), « 9800 version(s) en double »",
              c == 0 and "9800 version(s) en double" in s and tri and all(l["variantes_essayees"] == "9800" for l in tri)
              and all("-E01-" in l["id_version"] for l in tri), s)
        f3 = ecrire(os.path.join(d, "R_E03.csv"), C, [dict(l, essai="E03", tp=repr(float(l["tp"]) + 0.005), id_version=l["id_version"].replace(
            "-E01-", "-E03-")) for l in e01])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, f1, f3)
        _, tri = lire(out) if c == 0 else ([], [])
        # FABRIQUÉ : E03 = chaque objectif décalé d'un demi-point, toutes les versions diffèrent de celles de E01
        noter("T2b deux essais aux réglages différents : 19600 versions essayées, « E01+E03 »",
              c == 0 and tri and all(l["variantes_essayees"] == "19600" and l["essais_comptes"] == "E01+E03"
                                     for l in tri), s)
        # D4 : CHAQUE colonne commune du contrat, changée seule dans l'essai E03, fait refuser (propriété du contrat)
        for col in contrat.COLONNES_COMMUNES_A_UN_TRI:
            f4 = ecrire(os.path.join(d, "R_%s.csv" % col), C, volume(C, n=5, essai="E04", **{col: "AUTRE"}))
            out = os.path.join(dossier(), "TRI.csv")
            c, s = lancer(P_TRI, ".", out, ecrire(os.path.join(d, "R5.csv"), C, volume(C, n=5)), f4)
            noter("T2c « %s » différent entre deux essais : refus, rien d'écrit" % col,
                  c == 1 and "mêmes conditions" in s and col in s and not os.path.exists(out), s)
    if voulu("T3"):
        f = ecrire(os.path.join(dossier(), "R5.csv"), C, volume(C, n=5))
        c, s = lancer(P_TRI, ".", os.path.join(dossier(), "T.csv"), f, f)
        noter("T3 le même fichier deux fois : refus", c == 1 and "donné deux fois" in s, s)
        c, s = lancer(P_TRI, ".", os.path.join(dossier(), "T.csv"), f, os.path.join(dossier(), "x.csv"))
        noter("T3b un fichier de résultats absent : refus", c == 1 and "ARRÊT" in s, s)
    reg = ("# REGISTRE\n### LES SEUILS DU TRI DES VARIANTES\n\n| colonne | comparaison | valeur | source |\n"
           "|---|---|---|---|\n| operations_70 | >= | 100 | épreuve |\n| gain_net_euros_70 | > | 0 | épreuve |\n\nfin\n")
    prov = (["colonne", "comparaison", "valeur", "statut", "source"],
            [{"colonne": "gain_net_euros_70", "comparaison": "<", "valeur": "0", "statut": "À DÉCIDER PAR JEAN-LUC",
              "source": "épreuve"}])
    grand = None
    if voulu("T4") or voulu("T5") or voulu("T7") or voulu("T9") or voulu("T11"):
        grand = ecrire(os.path.join(dossier(), "R_E01.csv"), C, volume(C))
    if voulu("T4"):
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, fausse_racine(reg, prov), out, grand)
        _, vol = lire(grand)
        att4 = {l["id_version"] for l in vol if int(l["operations_70"]) >= 100 and float(l["gain_net_euros_70"]) > 0}
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T4 critère au REGISTRE (2 conditions) : il prime, le provisoire est IGNORÉ, statut DÉCIDÉ",
              c == 0 and {l["id_version"] for l in tri} == att4 and att4 and "IGNORÉ" in s
              and all(l["statut_du_critere"] == "DÉCIDÉ AU REGISTRE" for l in tri), s)
    refus = [
        ("T5", "T5 marque écrite deux fois au REGISTRE", reg + "\nLES SEUILS DU TRI DES VARIANTES\n", None,
         "plusieurs fois"),
        ("T5", "T6 tableau sans le bon en-tête", reg.replace("| colonne | comparaison |", "| col | comparaison |"),
         None, "n'a pas l'en-tête"),
        ("T7", "T7 provisoire qui se dit décidé", None, (prov[0], [dict(prov[1][0], statut="DÉCIDÉ")]),
         "une décision s'écrit au REGISTRE"),
        ("T5", "T8 aucun critère nulle part", None, None, "aucun critère du tri"),
        ("T9", "T9 critère sur une colonne de la période ENTIÈRE (30 % compris)",
         reg.replace("| operations_70 |", "| gain_net_euros |"), None, "pas une colonne de la partie de réglage"),
        ("T9", "T9b colonne hors contrat", reg.replace("| operations_70 |", "| gain_moyen |"), None,
         "pas une colonne de la partie de réglage"),
        ("T5", "T10 comparaison inconnue", reg.replace("| >= |", "| == |"), None, "comparaison « == » inconnue"),
        ("T11", "T11 valeur qui n'est pas un nombre", reg.replace("| 100 |", "| cent |"), None, "nombre fini"),
        ("T11", "T11b seuil « nan »", reg.replace("| 100 |", "| nan |"), None, "nombre fini"),
        ("T11", "T11c seuil « inf »", reg.replace("| 100 |", "| inf |"), None, "nombre fini"),
        ("T11", "T11d rangée courte au REGISTRE (D9)", reg.replace("| operations_70 | >= | 100 | épreuve |",
                                                                   "| operations_70 | >= |"), None, "rangée de 2 case"),
        ("T5", "T11e tableau sans condition", "LES SEUILS DU TRI DES VARIANTES\n| colonne | comparaison | valeur | "
         "source |\n|---|---|---|---|\n", None, "aucune condition"),
    ]
    for code_cas, nom, texte, pv, frag in refus:
        if not voulu(code_cas):
            continue
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, fausse_racine(texte, pv), out, grand)
        noter(nom + " : critère illisible, code 2, rien d'écrit", c == 2 and frag in s and not os.path.exists(out), s)
    if voulu("T12") or voulu("T11"):
        d = dossier()
        peu = volume(C, n=3)
        cas12 = [
            ("T12", "T12a fichier tronqué (annonce 9800, en porte 9799)", C, volume(C)[:-1], "annonce"),
            ("T12", "T12b colonne manquante", [c_ for c_ in C if c_ != "bareme"],
             [{k: v for k, v in l.items() if k != "bareme"} for l in peu], "champs absents ['bareme']"),
            ("T12", "T12c colonne hors contrat", C + ["autre"], [dict(l, autre="x") for l in peu],
             "hors contrat ['autre']"),
            ("T12", "T12d identifiant en double", C, peu[:2] + [dict(peu[2], id_version=peu[0]["id_version"])],
             "en double"),
            ("T12", "T12e deux stratégies", C, peu[:2] + [dict(peu[2], strategie="AUTRE")], "plusieurs stratégies"),
            ("T12", "T12f zéro opération mais un gain", C, peu[:2] + [dict(peu[2], operations_70="0")],
             "zéro opération_70"),
            ("T12", "T12g opérations illisibles", C, peu[:2] + [dict(peu[2], operations="dix")], "illisible"),
            ("T12", "T12h fichier vide", C, [], "aucune version"),
            ("T12", "T12i gain « inf » (D3)", C, peu[:2] + [dict(peu[2], gain_net_euros_70="inf")], "non fini"),
            ("T12", "T12j réussite « nan » (D3)", C, peu[:2] + [dict(peu[2], reussite_pourcents_exacte_70="nan")],
             "non finie"),
        ]
        for code_cas, nom, ch, lignes, frag in cas12:
            if not voulu(code_cas) and not (code_cas == "T12" and voulu("T11")):
                continue
            f = ecrire(os.path.join(d, "R_%d.csv" % len(CAS)), ch, lignes)
            out = os.path.join(dossier(), "TRI.csv")
            c, s = lancer(P_TRI, ".", out, f)
            noter(nom + " : refus", c == 1 and frag in s and not os.path.exists(out), s)
    if voulu("T13"):
        T = module(P_TRI, "tri_epreuve")
        peu = volume(C, n=3)
        zero = dict(peu[2], operations_70="0", gain_net_euros_70="0.00", reussite_pourcents_exacte_70="")
        r1 = T.passe_le_critere(zero, [("gain_net_euros_70", ">=", 0.0)])
        r2 = T.passe_le_critere(dict(peu[2], reussite_pourcents_exacte_70=""), [("reussite_pourcents_exacte_70", ">=",
                                                                                 0.0)])
        noter("T13 zéro opération et « gain_70 >= 0 » : jamais retenue, non mesurable (D2) ; case vide : non mesurable",
              r1 == (False, True) and r2 == (False, True), (r1, r2))
        reg13 = ("LES SEUILS DU TRI DES VARIANTES\n| colonne | comparaison | valeur | source |\n|---|---|---|---|\n"
                 "| gain_net_euros_70 | >= | -1000000000 | épreuve |\n")
        f = ecrire(os.path.join(dossier(), "R_zero.csv"), C, peu[:2] + [zero])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, fausse_racine(reg13), out, f)
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T13b programme entier, seuil qui laisse tout passer : 2 retenues sur 3, « dont 1 non mesurables »",
              c == 0 and len(tri) == 2 and "dont 1 non mesurables" in s, s)
    if voulu("T7"):
        # N5 : un statut de décision à la bonne forme (date, heure, renvoi au BACKLOG) est accepté et recopié
        dec = "DÉCIDÉ PAR JEAN-LUC LE 12-11-2026 À 09h10 (A-708)"
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, fausse_racine(None, (prov[0], [dict(prov[1][0], statut=dec, comparaison=">",
                                                                 valeur="0")])), out, grand or ecrire(os.path.join(
                                                                     dossier(), "R5.csv"), C, volume(C, n=5)))
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T7b décision datée renvoyant au BACKLOG : acceptée, recopiée dans chaque ligne, pas d'alerte « provisoire »",
              c == 0 and tri and all(l["statut_du_critere"] == dec for l in tri) and "CE SEUIL EST PROVISOIRE" not in s, s)
        for mauvais in ("DÉCIDÉ PAR JEAN-LUC LE 12-11-2026", "DÉCIDÉ PAR JEAN-LUC LE 12-11-2026 À 09h10"):
            out = os.path.join(dossier(), "TRI.csv")
            c, s = lancer(P_TRI, fausse_racine(None, (prov[0], [dict(prov[1][0], statut=mauvais)])), out,
                          ecrire(os.path.join(dossier(), "R5.csv"), C, volume(C, n=5)))
            noter("T7c décision sans heure ou sans renvoi au BACKLOG (« %s ») : code 2" % mauvais, c == 2, s)
    if voulu("T13"):
        peu = volume(C, n=3)
        f = ecrire(os.path.join(dossier(), "R00.csv"), C, peu[:2] + [dict(peu[2], operations_70="00",
                                                                          gain_net_euros_70="0.00",
                                                                          reussite_pourcents_exacte_70="")])
        reg13 = ("LES SEUILS DU TRI DES VARIANTES\n| colonne | comparaison | valeur | source |\n|---|---|---|---|\n"
                 "| gain_net_euros_70 | >= | 0 | épreuve |\n")
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, fausse_racine(reg13), out, f)
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T13c « 00 » opération et « gain_70 >= 0 » : écartée comme zéro (N4, le nombre et non le texte)",
              c == 0 and peu[2]["id_version"] not in {l["id_version"] for l in tri} and "dont 1 non mesurables" in s, s)
    if voulu("T16"):
        # N1 : la frontière d'un fichier se recalcule depuis le registre des stratégies et les cours joués.
        champs_r, r = lire(F["resultats"])
        d = dossier()
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, ecrire(os.path.join(d, "R_2099.csv"), champs_r,
                                              [dict(l, frontiere_70_30="2099-01-01") for l in r]))
        noter("T16a frontière réécrite (2099-01-01) : refus, la frontière de la fiche au registre est nommée",
              c == 1 and "frontière 70/30 des résultats 2099-01-01" in s and r[0]["frontiere_70_30"] in s
              and not os.path.exists(out), s)
        # la fiche change de période au registre APRÈS le jeu : une nouvelle dernière ligne (n°83)
        import CONTRATS_DES_FICHIERS as contrat_
        f_reg = os.path.join(RACINE, contrat_.REGISTRE_DES_STRATEGIES)
        texte_reg = open(f_reg, encoding="utf-8-sig").read()
        ch_reg, lignes_reg = lire(f_reg)
        derniere = [l for l in lignes_reg if l["id"] == r[0]["strategie"]][-1]
        nouvelle = dict(derniere, periode="2024-01-02 -> 2025-06-30")
        import io
        tampon = io.StringIO()
        w = csv.DictWriter(tampon, fieldnames=ch_reg, lineterminator="\n")
        w.writerow(nouvelle)
        fr = fausse_racine(None, None, {contrat_.REGISTRE_DES_STRATEGIES: texte_reg.rstrip("\n") + "\n" + tampon.getvalue(),
                                         "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv":
                                         open(os.path.join(RACINE, "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv"),
                                              encoding="utf-8").read()})
        f_rel = ecrire(os.path.join(d, "R_rel.csv"), champs_r,
                       [dict(l, cours_joues=os.path.relpath(F["cours"], fr)) for l in r])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, fr, out, f_rel)
        noter("T16b la fiche change de période au registre après le jeu : refus « a changé de période »",
              c == 1 and "a changé de période" in s and not os.path.exists(out), s)
        # les cours joués changent après le jeu DANS la période de la fiche (une clôture modifiée) : refus
        ch_c, cc = lire(F["cours"])
        k = max(i_ for i_, l in enumerate(cc) if l["date"] <= r[0]["fin_ecrite_dans_la_fiche"])
        cc2 = list(cc)
        cc2[k] = dict(cc[k], close=repr(float(cc[k]["close"]) * 1.01))
        f_c2 = ecrire(os.path.join(d, "cours_modifies.csv"), ch_c, cc2)
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, ecrire(os.path.join(d, "R_cours.csv"), champs_r,
                                              [dict(l, cours_joues=os.path.relpath(f_c2, RACINE)) for l in r]))
        noter("T16c une séance DANS la période de la fiche modifiée depuis le jeu (%s) : refus" % cc[k]["date"],
              c == 1 and "soit les cours de la période ont changé" in s and "à rejouer" in s
              and not os.path.exists(out), s)
        # M2 : une séance AJOUTÉE après la fin de la fiche (le maître grandit chaque soir) : accepté
        f_c3 = ecrire(os.path.join(d, "cours_allonges.csv"), ch_c, cc + [dict(cc[-1], date="2026-07-21")])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, ecrire(os.path.join(d, "R_allonge.csv"), champs_r,
                                              [dict(l, cours_joues=os.path.relpath(f_c3, RACINE)) for l in r]))
        noter("T16d une séance AJOUTÉE après la fin de la fiche (le maître grandit chaque soir) : accepté (M2)",
              c == 0 and os.path.exists(out), s)
        # m3 (relecteur, tour 4) : la BORNE HAUTE est la fin de la fiche — une séance modifiée ENTRE la fin de la fiche
        # et la dernière ligne du fichier (le 2026-07-13) ne compte pas : accepté
        fin_f = r[0]["fin_ecrite_dans_la_fiche"]
        k2 = min(i_ for i_, l in enumerate(cc) if l["date"] > fin_f)
        cc3 = list(cc)
        cc3[k2] = dict(cc[k2], close=repr(float(cc[k2]["close"]) * 1.01))
        f_c4 = ecrire(os.path.join(d, "cours_apres_fin.csv"), ch_c, cc3)
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, ecrire(os.path.join(d, "R_apres_fin.csv"), champs_r,
                                              [dict(l, cours_joues=os.path.relpath(f_c4, RACINE)) for l in r]))
        noter("T16e une séance modifiée APRÈS la fin de la fiche (%s, la fin est le %s) : accepté (m3)"
              % (cc[k2]["date"], fin_f), c == 0 and os.path.exists(out) and cc[k2]["date"] < cc[-1]["date"], s)
    if voulu("T17"):
        # N3 : mêmes réglages sous un autre essai, chiffres différents -> ARRÊT en nommant les deux fichiers
        champs_r, r = lire(F["resultats"])
        d = dossier()
        f2 = ecrire(os.path.join(d, "R_E02.csv"), champs_r, [dict(l, essai="E02", id_version=l["id_version"].replace(
            "-E01-", "-E02-"), gain_net_euros_70="-999.00") for l in r])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, F["resultats"], f2)
        noter("T17 mêmes réglages, chiffres différents dans deux essais : ARRÊT qui nomme les deux fichiers (N3)",
              c == 1 and "chiffres différents" in s and "R.csv" in s and "R_E02.csv" in s and not os.path.exists(out), s)
        f3 = ecrire(os.path.join(d, "R_E03.csv"), champs_r, [dict(l, essai="E03", id_version=l["id_version"].replace(
            "-E01-", "-E03-")) for l in r])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, F["resultats"], f3)
        noter("T17b mêmes réglages, mêmes chiffres : comptés une fois", c == 0 and "3 version(s) en double" in s, s)
    if voulu("T14"):
        out = os.path.join(dossier(), "TRI.csv")
        open(out, "w").close()
        c, s = lancer(P_TRI, ".", out, ecrire(os.path.join(dossier(), "R5.csv"), C, volume(C, n=5)))
        noter("T14 fichier trié déjà présent : refus", c == 1 and "existe déjà" in s, s)
    if voulu("T15"):
        peu = volume(C, n=3)
        # FABRIQUÉ : la version 3 reprend les réglages de la version 1 sous un autre identifiant, univers réordonné
        cop = dict(peu[0], id_version=peu[2]["id_version"],
                   univers=",".join(reversed(peu[0]["univers"].split(","))))
        f = ecrire(os.path.join(dossier(), "R3.csv"), C, peu[:2] + [cop])
        out = os.path.join(dossier(), "TRI.csv")
        c, s = lancer(P_TRI, ".", out, f)
        _, tri = lire(out) if c == 0 else ([], [])
        noter("T15 mêmes réglages sous un autre identifiant (univers dans un autre ordre) : 2 versions essayées",
              c == 0 and "1 version(s) en double" in s and all(l["variantes_essayees"] == "2" for l in tri), s)
def brute(dates, debut, fin_fiche, h):
    """Calcule la fin utilisable par force brute, sans le code de JOUER.
    ① RÔLE — Le calcul indépendant de la famille FIN. ② CONTEXTE D'APPEL — `famille_fin`.
    ③ ENTRÉE — `dates` : {valeur: dates triées} · `debut`, `fin_fiche` · `h` : l'horizon le plus long.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la fin, ou None. [rend: 1]
    ⑥ TRAITEMENT — Parmi la fin de la fiche et toutes les séances entre le début et elle, garder la plus tardive D
      telle que CHAQUE valeur ait au moins h + 1 séances strictement après D.
    ⑦ UNITÉ — Dates ; séances. ⑧ POURQUOI — Une autre écriture que celle du programme (aucun indice négatif).
    ⑨ CE QUI CLOCHE — Compte par recherche dichotomique (`bisect`) : les dates doivent être triées. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    tous = sorted({d for ds in dates.values() for d in ds if debut <= d <= fin_fiche} | {fin_fiche}, reverse=True)
    for D in tous:
        if all(len(ds) - bisect.bisect_right(ds, D) >= h + 1 for ds in dates.values()):
            return D
    return None




def famille_fin():
    """Éprouve `fin_utilisable`, `recul_en_seances` et `lire_le_recul_maximum`.
    ① RÔLE — Les cas F1 à F9. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — Le maître existe.
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — Charger les séries par le lecteur unique du juge (comme JOUER) ; comparer à `brute`.
    ⑦ UNITÉ — Dates ; séances.
    ⑧ POURQUOI — Le cas réel F1 est celui qui a coûté une correction à la main le 11-11-2026 (plan V7, bloc 5g).
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨ ①. ⑩ EFFET — Lit le maître. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    V = module(P_JOUER, "jouer_epreuve")
    sys.path.insert(0, os.path.join(RACINE, "programmes"))
    import JUGE_DES_STRATEGIES as J
    mn = J.table_mnemoniques(J.trouver(RACINE, "REFERENTIEL_VALEURS"))
    cours, _ = J.lire_par_le_lecteur(RACINE, "donnees/cours_maitre.csv", mn)
    univ = ("AC,AI,AIR,CS,BNP,EN,BVI,CAP,CA,ACA,BN,DSY,FGR,ENGI,EL,ERF,ENX,RMS,KER,OR,LR,MC,ML,ORA,RI,PUB,RNO,SAF,SGO,"
            "SAN,SU,GLE,STLAP,STMPA,HO,TTE,URW,VIE,DG").split(",")   # l'univers de la fiche IND-001-RETEST
    au_10_11 = {m: [b["date"] for b in cours[mn.get(m, J.cle_valeur(m))] if b["date"] <= "2026-11-10"] for m in univ}
    fin, lim = V.fin_utilisable(au_10_11, "2000-01-03", "2026-10-30", 25)
    noter("F1 cas réel du 11-11-2026 (maître au 10-11, IND-001-RETEST, horizon 25) : fin 2026-10-05 ramenée par AC",
          (fin, lim) == ("2026-10-05", "AC"), (fin, lim))
    r_f1 = V.recul_en_seances(au_10_11, "2026-10-05", "2026-10-30")
    noter("F1b recul du cas réel : 19 séances (6 au 30-10-2026)", r_f1 == 19, r_f1)
    tout = {m: [b["date"] for b in cours[mn.get(m, J.cle_valeur(m))]] for m in univ}
    for h, fin_f in ((20, "2026-07-10"), (25, "2026-10-30"), (100, "2026-10-30"), (300, "2026-10-30")):
        r = V.fin_utilisable(tout, "2024-01-02", fin_f, h)[0]
        b = brute(tout, "2024-01-02", fin_f, h)
        noter("F2 maître entier, horizon %d, fiche au %s : %s = force brute %s" % (h, fin_f, r, b), r == b, (r, b))
    d3 = {"A": ["2026-01-%02d" % k for k in range(1, 13)],
          "B": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-07", "2026-01-08"]}   # B en trou du 4 au 6
    r3, b3 = V.fin_utilisable(d3, "2026-01-01", "2026-01-12", 1), brute(d3, "2026-01-01", "2026-01-12", 1)
    noter("F3 valeur B en trou : fin %s = force brute %s, qui n'est pas une séance de B" % (r3[0], b3),
          r3 == (b3, "B") and b3 not in d3["B"], (r3, b3))
    r4 = V.fin_utilisable({"A": d3["A"], "Z": ["2026-01-01"]}, "2026-01-01", "2026-01-12", 2)
    noter("F4 une valeur sans assez de séances : aucune fin, elle est nommée", r4 == (None, "Z"), r4)
    r5 = V.fin_utilisable(d3, "2026-01-01", "2026-01-05", 1)
    noter("F5 la fiche laisse assez de séances : sa fin est gardée (même un jour sans séance de B)",
          r5 == ("2026-01-05", None) and brute(d3, "2026-01-01", "2026-01-05", 1) == "2026-01-05", r5)
    r6 = V.fin_utilisable(d3, "2026-01-07", "2026-01-12", 1)
    noter("F6 la borne tombe avant le début de la fiche : aucune fin", r6[0] is None, r6)
    p, c_, refus = V.lire_la_ligne_de_commande(["a", "b", "c", "--cours=x.csv"])
    noter("F7 lecture de la ligne de commande : « --cours=x.csv » rendu, trois positions",
          (p, c_, refus) == (["a", "b", "c"], "x.csv", None), (p, c_, refus))
    rm = V.lire_le_recul_maximum(RACINE)
    noter("F8 le recul maximum se lit dans %s, marqué provisoire" % V.RECUL_MAXIMUM,
          rm[0] >= 0 and rm[1] == "PROVISOIRE, À DÉCIDER PAR JEAN-LUC", rm)
    mauvais = 0
    for texte in ("reglage,valeur,unite,statut,source\nrecul_maximum,vingt,seances,P,x\n",
                  "reglage,valeur,unite,statut,source\nrecul_maximum,26,jours,P,x\n",
                  "reglage,valeur,unite,statut,source\nrecul_maximum,26,seances,,x\n", "a,b\n1,2\n", None):
        d = dossier()
        if texte is not None:
            os.makedirs(os.path.join(d, os.path.dirname(V.RECUL_MAXIMUM)))
            open(os.path.join(d, V.RECUL_MAXIMUM), "w", encoding="utf-8").write(texte)
        try:
            V.lire_le_recul_maximum(d)
        except ValueError:
            mauvais += 1
    noter("F9 recul maximum illisible, d'une autre unité, sans statut, mal formé ou absent : 5 refus sur 5",
          mauvais == 5, mauvais)
    MJ = module(P_MJ, "mj_epreuve")
    if voulu("F10"):
        b = ("2024-01-02", "2026-07-10")
        sea = {"2024-01-02", "2025-01-15", "2027-01-15"}
        ok_dec = MJ.frontiere_de_la_fiche({"frontiere_70_30": "2025-01-15"}, sea, b) == "2025-01-15"
        refus = 0
        for dec in ("2027-01-15", "15-01-2025", "2025-1-15", "2025-01-16"):
            try:
                MJ.frontiere_de_la_fiche({"frontiere_70_30": dec}, sea, b)
            except ValueError:
                refus += 1
        noter("F10 frontière DÉCLARÉE : lue telle quelle ; hors bornes, illisible ou pas une séance (M1) : 4 refus sur 4",
              ok_dec and refus == 4, (ok_dec, refus))
    if voulu("F13"):
        # m4 (relecteur, tour 4) : la coupure rend la séance où elle a RÉELLEMENT coupé — une frontière tombée entre
        # deux séances (un samedi) rend la séance suivante (le lundi) ; le refus M1 de JOUER repose sur cette sincérité
        c13 = MJ.coupure_70_30([{"date_signal": "2025-06-02", "net": 1.0}],
                               {"2025-05-29", "2025-05-30", "2025-06-02", "2025-06-03"}, horizon=5,
                               frontiere="2025-05-31")
        noter("F13 frontière reçue entre deux séances (2025-05-31) : la coupure rend la séance coupée, 2025-06-02 (m4)",
              c13.get("frontiere") == "2025-06-02", c13.get("frontiere"))
    if voulu("F12"):
        try:
            MJ.coupure_70_30([{"date_signal": "2024-01-02", "net": 1.0}], {"2024-01-02", "2024-01-03"}, horizon=5)
            r12 = "PASSE"
        except ValueError as e:
            r12 = "frontière est exigée" in str(e)
        except Exception as e:
            r12 = "%s : %s" % (type(e).__name__, e)
        noter("F12 la coupure sans frontière s'arrête, « la frontière est exigée » (plus de repli silencieux, M1)",
              r12 is True, r12)
    if voulu("F11"):
        # calcul indépendant : la séance de rang 70 % parmi celles des bornes, comptée à la main sur les vraies séances
        seances = {d for ds in tout.values() for d in ds}
        dans = sorted(d for d in seances if "2024-01-02" <= d <= "2026-07-10")
        attendu = dans[(len(dans) * 7) // 10]
        r = MJ.frontiere_de_la_fiche({}, seances, ("2024-01-02", "2026-07-10"))
        noter("F11 frontière calculée sur les vraies séances (2024-01-02 -> 2026-07-10) : %s = calcul à part %s"
              % (r, attendu), r == attendu and r == "2025-10-06", (r, attendu))


def famille_jouer():
    """Éprouve JOUER_LES_VERSIONS en sous-processus : l'option, le passage au juge, la fin, les garde-fous.
    ① RÔLE — Les cas J1 à J9. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — La combinatoire de C5E10-OBS-V1 E01 et le maître existent sous la racine.
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — Trois versions réelles (0001, 0500 et 0914, celle de la fiche) ; des fichiers de cours tronqués du
      maître dans un dossier temporaire ; deux copies du programme modifiées ICI pour atteindre un garde-fou (J6, J8).
    ⑦ UNITÉ — Dates ; opérations.
    ⑧ POURQUOI — `--cours=` doit valoir pour le juge ET pour ce programme (bloc 5l ⑤) ; chaque garde-fou doit pouvoir
      rougir (relecteur neuf, D5, D6, D8).
    ⑨ CE QUI CLOCHE — Environ quinze secondes par lancement (calibrage du juge compris).
    ⑩ EFFET — Lance JOUER ; écrit dans des dossiers temporaires. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = dossier()
    champs, comb = lire(os.path.join(RACINE, COMB_C5))
    trois = [dict(l, versions_dans_l_essai="3") for l in comb if l["id_version"].split("-")[-1] in ("0001", "0500", "0914")]
    f_comb = ecrire(os.path.join(d, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"), champs, trois)
    ch_c, cours = lire(os.path.join(RACINE, "donnees/cours_maitre.csv"))
    court = ecrire(os.path.join(d, "cours_au_20-07.csv"), ch_c, [l for l in cours if l["date"] <= "2026-07-20"])
    rel = lambda f: os.path.relpath(f, RACINE)
    if voulu("J1"):
        c, s = lancer(P_JOUER, ".", f_comb, os.path.join(d, "R1.csv"), "--cours=%s" % rel(os.path.join(d, "absent.csv")))
        noter("J1 --cours= vers un fichier absent : refus avant le calibrage",
              c == 1 and "n'existe pas" in s and "CALIBRAGE" not in s, s)
    if voulu("J2"):
        c, s = lancer(P_JOUER, ".", f_comb, os.path.join(d, "R2.csv"), "--cours", rel(court))
        noter("J2 « --cours fichier » sans « = » : refus (comme le juge)", c == 1 and "option inconnue ou mal écrite" in s, s)
        c, s = lancer(P_JOUER, ".", f_comb, os.path.join(d, "R3.csv"), "--cours=" + rel(court), "--cours=" + rel(court))
        noter("J3 --cours= écrit deux fois : refus", c == 1 and "écrite 2 fois" in s, s)
    if voulu("J4"):
        out = os.path.join(d, "R4.csv")
        c, s = lancer(P_JOUER, ".", f_comb, out, "--cours=" + rel(court))
        _, res = lire(out) if c == 0 else ([], [])
        sys.path.insert(0, os.path.join(RACINE, "programmes"))
        import JUGE_DES_STRATEGIES as J
        mn = J.table_mnemoniques(J.trouver(RACINE, "REFERENTIEL_VALEURS"))
        lus, _ = J.lire_par_le_lecteur(RACINE, rel(court), mn)
        codes = sorted({x.strip() for l in trois for x in l["univers"].split(",") if x.strip()})
        attendu = brute({m: [b["date"] for b in lus[mn.get(m, J.cle_valeur(m))]] for m in codes},
                        "2024-01-02", "2026-07-10", max(int(l["horizon"]) for l in trois))
        noter("J4 --cours= au 20-07 : code 0, periode_fin = %s (force brute), fin de la fiche 2026-07-10 recopiée, "
              "cours_joues et son empreinte nommés" % attendu,
              c == 0 and len(res) == 3 and attendu < "2026-07-10"
              and all(l["periode_fin"] == attendu and l["fin_ecrite_dans_la_fiche"] == "2026-07-10"
                      and l["cours_joues"] == rel(court)
                      and l["empreinte_des_cours"] == module(P_JOUER, "jouer_j4").empreinte_des_cours_jusqu_a(
                          court, "2026-07-10")
                      for l in res) and "FIN CALCULÉE : %s" % attendu in s, s)
    if voulu("J5"):
        tres_court = ecrire(os.path.join(d, "cours_au_30-06.csv"), ch_c, [l for l in cours if l["date"] <= "2026-06-30"])
        c, s = lancer(P_JOUER, ".", f_comb, os.path.join(d, "R5.csv"), "--cours=" + rel(tres_court))
        noter("J5 --cours= au 30-06 : le juge, lancé avec le même --cours=, retrouve la fiche (calibrage OK, pas de "
              "désaccord)", c == 0 and "CALIBRAGE PAR LE JUGE SEUL : OK" in s and "ne rendent pas la même chose" not in s,
              s)
    if voulu("J6"):
        # D8 : une copie où le calcul oublie la séance d'achat (une séance de moins) ; le recompte doit l'arrêter.
        texte = open(CHEMINS[P_JOUER], encoding="utf-8").read()
        avant = "    besoin = horizon_max + 1\n"
        copie = os.path.join(dossier(), "JOUER_LES_VERSIONS.py")
        open(copie, "w", encoding="utf-8").write(texte.replace(avant, "    besoin = horizon_max\n"))
        r = subprocess.run([sys.executable, "-B", copie, ".", f_comb, os.path.join(d, "R6.csv"), "--cours=" + rel(court)],
                           cwd=RACINE, capture_output=True, text=True, timeout=DELAI)
        s = r.stdout + r.stderr
        noter("J6 calcul faussé d'une séance : le recompte de la marge arrête (« pas assez de cours »), rien d'écrit",
              texte.count(avant) == 1 and r.returncode == 1 and "pas assez de cours après la période pour" in s
              and "FIN CALCULÉE" in s and not os.path.exists(os.path.join(d, "R6.csv")), s[-600:])
    if voulu("J7"):
        # D6 : une seule valeur (AIR, présente dans l'univers des trois versions) dont les cours s'arrêtent au 31-03-2026
        sys.path.insert(0, os.path.join(RACINE, "programmes"))
        import JUGE_DES_STRATEGIES as J
        nom_air = J.table_mnemoniques(J.trouver(RACINE, "REFERENTIEL_VALEURS"))["AIR"]
        coupe = ecrire(os.path.join(d, "cours_air_court.csv"), ch_c,
                       [l for l in cours if l["date"] <= "2026-07-20" and not (l["valeur"] == nom_air
                                                                              and l["date"] > "2026-03-31")])
        c, s = lancer(P_JOUER, ".", f_comb, os.path.join(d, "R7.csv"), "--cours=" + rel(coupe))
        noter("J7 une valeur dont les cours s'arrêtent tôt : la fin reculerait trop, refus qui NOMME la valeur",
              c == 1 and "la fin calculée recule de" in s and "par AIR" in s and not os.path.exists(os.path.join(d, "R7.csv")),
              s[-600:])
    if voulu("J8"):
        # D5 : une copie dont le réglage du recul est remplacé par un fichier temporaire permissif ; horizon 700 sur la
        # version 0500 : la fiche n'a AUCUNE opération sur la période ramenée ; c'est un résultat, pas un arrêt.
        reglage = os.path.join(dossier(), "RECUL.csv")
        open(reglage, "w", encoding="utf-8").write("reglage,valeur,unite,statut,source\n"
                                                    "recul_maximum,100000,seances,ÉPREUVE,épreuve J8\n")
        texte = open(CHEMINS[P_JOUER], encoding="utf-8").read()
        avant = 'RECUL_MAXIMUM = "donnees/combinatoires/RECUL_MAXIMUM_DE_LA_FIN.csv"'
        copie = os.path.join(dossier(), "JOUER_LES_VERSIONS.py")
        open(copie, "w", encoding="utf-8").write(texte.replace(avant, "RECUL_MAXIMUM = %r" % reglage))
        c700 = ecrire(os.path.join(d, "C700.csv"), champs, [dict(l, horizon="700") if l["id_version"].endswith("-0500")
                                                             else l for l in trois])
        r = subprocess.run([sys.executable, "-B", copie, ".", c700, os.path.join(d, "R8.csv")], cwd=RACINE,
                           capture_output=True, text=True, timeout=DELAI)
        s = r.stdout + r.stderr
        noter("J8 la fiche n'a aucune opération sur la période ramenée : « aucune opération », code 0, jamais KeyError",
              texte.count(avant) == 1 and r.returncode == 0 and "la fiche sur la période jouée : aucune opération" in s
              and "KeyError" not in s, s[-600:])
    if voulu("J9"):
        F = resultats_reels()
        _, a = lire(F["resultats"])
        _, b = lire(F["resultats_altere"])
        cles = ("id_version", "frontiere_70_30", "operations_70", "reussite_pourcents_exacte_70", "gain_net_euros_70")
        noter("J9 la PREMIÈRE séance après la frontière altérée (%s) : période entière différente, colonnes « _70 » "
              "égales" % F["date_alteree"],
              len(a) == 3 and [(x["operations"], x["gain_net_euros"]) for x in a]
              != [(x["operations"], x["gain_net_euros"]) for x in b]
              and [{k: x[k] for k in cles} for x in a] == [{k: x[k] for k in cles} for x in b]
              and all(x["frontiere_70_30"] < F["date_alteree"] for x in a),
              open(F["resultats"] + ".sortie", encoding="utf-8").read()[-400:] if os.path.exists(F["resultats"] + ".sortie")
              else "")
    if voulu("J11"):
        # M1 : une fiche à frontière DÉCLARÉE (2025-06-02), de bout en bout, dans une racine miroir dont le registre
        # porte une colonne `frontiere_70_30`. JOUER doit écrire ET couper à cette date ; le juge, lancé seul, est le
        # calcul à part : sa ligne « apprentissage N op » doit égaler `operations_70` de la version de la fiche.
        F = resultats_reels()
        sys.path.insert(0, os.path.join(RACINE, "programmes"))
        import CONTRATS_DES_FICHIERS as contrat_
        # en listes, pas en dictionnaires : le registre a des colonnes sans nom, qu'un DictReader confondrait
        with open(os.path.join(RACINE, contrat_.REGISTRE_DES_STRATEGIES), encoding="utf-8-sig", newline="") as h_:
            rangs = list(csv.reader(h_))
        import io
        tampon = io.StringIO()
        w = csv.writer(tampon, lineterminator="\n")
        i_id = rangs[0].index("id")
        w.writerow(rangs[0] + ["frontiere_70_30"])
        for l in rangs[1:]:
            w.writerow(l + ["2025-06-02" if l and l[i_id] == "C5E10-OBS-V1" else ""])
        fr = fausse_racine(None, None, {contrat_.REGISTRE_DES_STRATEGIES: tampon.getvalue(),
                                         "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv":
                                         open(os.path.join(RACINE, "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv"),
                                              encoding="utf-8").read()})
        out = os.path.join(dossier(), "R_declaree.csv")
        cours_rel = "--cours=" + os.path.relpath(F["cours"], fr)
        r1 = subprocess.run([sys.executable, "-B", CHEMINS[P_JOUER], fr, F["combinatoire"], out, cours_rel],
                            cwd=fr, capture_output=True, text=True, timeout=DELAI)
        r2 = subprocess.run([sys.executable, "-B", os.path.join(fr, P_JUGE), fr, "C5E10-OBS-V1", cours_rel], cwd=fr,
                            capture_output=True, text=True, timeout=DELAI)
        import re as re_
        m_f = re_.search(r"COUPURE 70/30\s+frontiere (\S+) \.", r2.stdout)
        m_a = re_.search(r"apprentissage\s+(\d+) op", r2.stdout)
        _, res = lire(out) if r1.returncode == 0 and os.path.exists(out) else ([], [])
        v = [x for x in res if x["id_version"].endswith("-0914")]
        noter("J11 frontière DÉCLARÉE (2025-06-02) : JOUER l'écrit et y coupe ; le juge seul dit la même date et le même "
              "nombre d'opérations de réglage (%s)" % (m_a.group(1) if m_a else None),
              r1.returncode == 0 and v and m_f and m_a and v[0]["frontiere_70_30"] == "2025-06-02" == m_f.group(1)
              and v[0]["operations_70"] == m_a.group(1),
              (r1.stdout[-500:] + r1.stderr[-500:] + " || " + r2.stdout[-300:]))
        out_t = os.path.join(dossier(), "TRI.csv")
        c, s_ = lancer(P_TRI, fr, out_t, out)
        noter("J11b le tri accepte ce fichier dans la même racine (frontière déclarée recalculée : la même)",
              c == 0, s_)
    if voulu("J12"):
        # M1 : `partie_de_reglage` refuse une coupure qui a coupé ailleurs que la frontière reçue
        V = module(P_JOUER, "jouer_j12")
        faux = types.SimpleNamespace(coupure_70_30=lambda ops, sea, horizon=None, frontiere=None: {
            "frontiere": "2025-10-06", "embargo_seances": 21, "res_70": {"n": 1}})
        try:
            V.partie_de_reglage(faux, [{"date_signal": "2025-01-02"}], {"2025-01-02"}, 20, "2025-06-02")
            r12 = "PASSE"
        except ValueError as e:
            r12 = "la coupure a coupé au 2025-10-06" in str(e)
        noter("J12 une coupure qui coupe au 2025-10-06 quand la frontière écrite est le 2025-06-02 : refus (M1)",
              r12 is True, r12)
    if voulu("J13"):
        # GARDE DIRECT DE LA PÉRIODE RAMENÉE (superviseur R-759 de la fusion du tri, 13-11-2026, défaut 2 du relecteur) :
        # la `periode_fin` écrite doit être la fin calculée (force brute, sans le code de JOUER) ET les opérations écrites
        # pour la version identique à la fiche doivent être celles que le juge, appelé ICI à part, rend sur
        # (début, periode_fin écrite). Le cas exige aussi que cette période et la fiche entière donnent des comptes
        # DIFFÉRENTS : sinon il ne pourrait pas voir une période ignorée, et il le dit. Indépendant de J8.
        F = resultats_reels()
        _, res = lire(F["resultats"]) if os.path.exists(F["resultats"]) else ([], [])
        sys.path.insert(0, os.path.join(RACINE, "programmes"))
        import JUGE_DES_STRATEGIES as J
        import CONTRATS_DES_FICHIERS as contrat_
        mn = J.table_mnemoniques(J.trouver(RACINE, "REFERENTIEL_VALEURS"))
        f_rel = os.path.relpath(F["cours"], RACINE)
        lus, lecture = J.lire_par_le_lecteur(RACINE, f_rel, mn)
        fiche = contrat_.fiches_du_registre(J.trouver(RACINE, contrat_.NOM_DU_REGISTRE_DES_STRATEGIES))["C5E10-OBS-V1"]
        _ok0, _manq, bornes = J.porte_0(dict(fiche))
        mod_sig = J.signal_de_la_fiche(RACINE, dict(fiche))
        mod_pos = J.charger_module(J.trouver(RACINE, "MODULE_POSITIONS.py"), "pos_j13")
        _, comb = lire(F["combinatoire"])
        codes = sorted({x.strip() for l in comb for x in l["univers"].split(",") if x.strip()})
        attendu = brute({m: [b["date"] for b in lus[mn.get(m, J.cle_valeur(m))]] for m in codes},
                        bornes[0], bornes[1], max(int(l["horizon"]) for l in comb))
        v = [x for x in res if x["id_version"].endswith("-0914")]
        ramenee = J.resumer(J.jouer(dict(fiche), lus, mn, mod_sig, mod_pos, periode=(bornes[0], attendu),
                                    lecture=lecture)[0])
        entiere = J.resumer(J.jouer(dict(fiche), lus, mn, mod_sig, mod_pos, periode=tuple(bornes),
                                    lecture=lecture)[0])
        ecrit = (v[0]["periode_fin"], v[0]["operations"], v[0]["gain_net_euros"]) if v else None
        noter("J13 période ramenée jouée : periode_fin écrite = fin calculée (%s) et opérations écrites = celles du juge sur "
              "cette période (%d), distinctes de la fiche entière (%d)" % (attendu, ramenee["n"], entiere["n"]),
              bool(v) and attendu is not None and attendu < bornes[1] and ramenee["n"] != entiere["n"]
              and ecrit == (attendu, str(ramenee["n"]), "%.2f" % ramenee["net"] if ramenee["n"] else "0.00"),
              "écrit %s · juge sur la période ramenée %s · juge sur la fiche entière %s · bornes %s"
              % (ecrit, (attendu, ramenee["n"], ramenee.get("net")), (bornes[1], entiere["n"], entiere.get("net")),
                 bornes))
    if voulu("J10"):
        # N2 : DEUX CHEMINS — la frontière et l'embargo écrits par JOUER contre ceux que le juge IMPRIME pour la fiche
        F = resultats_reels()
        _, a = lire(F["resultats"])
        fiche_v = [x for x in a if x["id_version"].endswith("-0914")][0]     # la version identique à la fiche
        r = subprocess.run([sys.executable, "-B", CHEMINS[P_JUGE], ".", "C5E10-OBS-V1",
                            "--cours=" + os.path.relpath(F["cours"], RACINE)], cwd=RACINE, capture_output=True,
                           text=True, timeout=DELAI,
                           env=dict(os.environ, PYTHONPATH=os.path.join(RACINE, "programmes")))
        import re as re_
        m = re_.search(r"COUPURE 70/30\s+frontiere (\S+) \. embargo (\d+) seances", r.stdout)
        noter("J10 frontière et embargo de JOUER (%s, %s) = ceux que le juge imprime (%s)"
              % (fiche_v["frontiere_70_30"], fiche_v["embargo_seances"], m.groups() if m else None),
              m is not None and (fiche_v["frontiere_70_30"], fiche_v["embargo_seances"]) == m.groups(),
              r.stdout[-400:] + r.stderr[-300:])


def saboter(code):
    """Prépare la copie sabotée d'un programme et la sélection des cas visés.
    ① RÔLE — Remplacer UN texte dans une copie. ② CONTEXTE D'APPEL — `main`, avec `--un-sabotage=`.
    ③ ENTRÉE — `code` : la clé de `SABOTAGES`. ④ CONDITIONS D'ENTRÉE — Le texte figure UNE fois.
    ⑤ SORTIE — UNE valeur : la liste des cas à jouer. [rend: 1]
    ⑥ TRAITEMENT — ① lire le programme · ② exiger une seule occurrence · ③ écrire la copie dans un dossier temporaire ·
      ④ pointer `CHEMINS` dessus.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage qui ne s'applique pas ne prouve rien : il s'arrête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit une copie. ⑪ TERMINAISON — Rend la main ; lève si le texte manque. [sort: non]
    """
    prog, avant, apres, cas, _ = SABOTAGES[code]
    texte = open(os.path.join(RACINE, prog), encoding="utf-8").read()
    if texte.count(avant) != 1:
        raise RuntimeError("sabotage %s : le texte visé figure %d fois" % (code, texte.count(avant)))
    copie = os.path.join(dossier(), os.path.basename(prog))
    open(copie, "w", encoding="utf-8").write(texte.replace(avant, apres))
    CHEMINS[prog] = copie
    return cas


def main(argv):
    """Joue les familles, puis les sabotages si demandé.
    ① RÔLE — Le verdict. ② CONTEXTE D'APPEL — Le bas du fichier. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — ① vérifier la racine · ② en `--un-sabotage=` : saboter, ne jouer que les cas visés · ③ sinon jouer
      les trois familles · ④ en `--sabotages` : relancer ce fichier une fois par sabotage (les résultats réels du
      lancement parent sont prêtés aux sabotages du tri), exiger le code 1 · ⑤ effacer les dossiers.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir l'en-tête. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance des programmes ; efface ses dossiers. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    global RACINE, SELECTION
    pos = [a for a in argv if not a.startswith("--")]
    if len(pos) != 1:
        print(__doc__.split("①")[0])
        return 2
    RACINE = os.path.abspath(pos[0])
    manque = [f for f in (P_TRI, P_JOUER, REEL_ANCIEN, COMB_C5, "donnees/cours_maitre.csv",
                          "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv",
                          "donnees/combinatoires/RECUL_MAXIMUM_DE_LA_FIN.csv")
              if not os.path.exists(os.path.join(RACINE, f))]
    if manque:
        print("ÉPREUVE IMPOSSIBLE : absents %s" % manque)
        return 2
    for p in (P_TRI, P_JOUER, P_JUGE, P_MJ):
        CHEMINS[p] = os.path.join(RACINE, p)
    un = next((a.split("=", 1)[1] for a in argv if a.startswith("--un-sabotage=")), None)
    familles = (("TRI", "T", famille_tri), ("FIN", "F", famille_fin), ("JOUER", "J", famille_jouer))
    code = 1
    try:
        try:
            if un:
                SELECTION = set(saboter(un))
                print("SABOTAGE %s (%s) — cas %s" % (un, SABOTAGES[un][4], sorted(SELECTION)))
            for nom, lettre, f in familles:
                if SELECTION is None or any(c.startswith(lettre) for c in SELECTION):
                    print("FAMILLE %s" % nom)
                    f()
        except Exception as e:   # une famille interrompue est un échec, jamais un silence
            noter("famille interrompue", False, "%s : %s" % (type(e).__name__, e))
        tenus = sum(ok for _, ok in CAS)
        print("CAS : %d / %d tenus" % (tenus, len(CAS)))
        code = 0 if CAS and tenus == len(CAS) else 1
        if "--sabotages" in argv and not un:
            print("SABOTAGES — chacun doit faire rougir les cas qu'il vise :")
            env = dict(os.environ, EPREUVE_TRI_RESULTATS=FIXTURE.get("dossier", ""))
            for k in SABOTAGES:
                r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), RACINE, "--un-sabotage=" + k],
                                   capture_output=True, text=True, timeout=DELAI * 6, env=env)
                echecs = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ÉCHEC")]
                mord = r.returncode == 1 and echecs and "famille interrompue" not in r.stdout
                print("  %s %s (%s) : %s" % ("MORD   " if mord else "NE MORD PAS", k, SABOTAGES[k][4],
                                             echecs[0][:170] if echecs else r.stdout[-300:]), flush=True)
                code = code if mord else 1
    finally:
        for d in DOSSIERS:
            shutil.rmtree(d, ignore_errors=True)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
