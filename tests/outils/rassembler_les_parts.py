#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rassembler_les_parts — Mer 04-11-2026 (Paris), tour 3 après l'avis du superviseur R-759 du 04-11-2026 à 19h59 ;
réparé le Jeu 05-11-2026 pour la version B (étude github_series/RAPPORT.md). Simulation uniquement.

① RÔLE — Réunir les parts d'une série de sabotages jouées sur plusieurs machines (jouer_une_part.py) en UN dossier
  de travail, comme si une seule machine avait tout joué, puis faire écrire le RELEVÉ par le joueur du dépôt
  lui-même (tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py, en reprise : tous les lots sont faits, il ne rejoue rien).
  Le relevé obtenu a donc la forme exacte de celui de la machine, et la certification de nuit le lit sans changement.
② CONTEXTE D'APPEL — Le job final du circuit public .github/workflows/series_longues.yml, une fois par série, quand
  TOUS les jobs des parts sont verts, sur les dossiers que les parts ont poussés au dépôt privé, chacune sur SA
  branche (le circuit les extrait de ces branches dans un dossier de la machine, jamais dans le dépôt) :
  python3 -B rassembler_les_parts.py <racine> <épreuve> <relevé> --depuis=<dossier des parts> --travail=<dossier neuf>
  [--raisons-acceptees=S1,S2,…]   (passé tel quel au joueur : les raisons nouvelles que Jean-Luc a acceptées)
  Aussi à la main, pour l'essai local, et pour refaire le relevé d'un passage de GitHub après une décision de
  Jean-Luc sur des raisons « à examiner » (les parts restent sur leurs branches jusqu'au rangement).
③ ENTRÉE — La racine : une copie du MÊME commit que celle où les parts ont joué (l'empreinte du départ est
  comparée) ; l'épreuve et le relevé, relatifs à la racine ; `--depuis` : un dossier où chaque part a laissé son
  dossier de travail (lots, un dossier par flux de l'écoute, etat_du_depart.json, debut.txt, part.json ; le module d'écoute n'est pas
  nécessaire : il est réécrit ici depuis le joueur), à n'importe quelle profondeur ;
  `--travail` : le dossier où réunir les parts.
④ CONDITIONS D'ENTRÉE — `--travail` n'existe pas ou est vide (on ne mélange jamais deux rassemblements). Chaque part
  porte part.json, que jouer_une_part.py n'écrit qu'après une part complète.
⑤ SORTIE — UNE valeur : le code de sortie. 0 : relevé écrit, série conforme. 1 : relevé écrit, série NON conforme
  (un sabotage manque, est doublé, ne mord pas, ou un lot a rendu autre chose que 0 — jugé par le joueur). 2 : rien
  d'écrit par ce programme, ou le joueur a dû rejouer un lot (part manquante ou en double, manifestes en désaccord,
  lot absent, code d'un lot illisible ou différent de celui du manifeste, programme interdit lu par une part, flux
  d'écoute d'une part qui avait des lots absent ou qui ne nomme pas l'épreuve, fichier d'une part illisible, empreintes du
  départ différentes, part sans sa place libre minimale (témoin du milieu), découpage différent de celui du joueur, dossier de travail non vide, toute erreur imprévue,
  code 2 du joueur, ou joueur qui ne rend ni 0 ni 1, ou qui rend 0 ou 1 sans avoir dit « FINI … relevé » ni écrit le
  relevé). Aucune trace Python ne sort en code 1, ni du rassembleur ni du joueur qu'il lance : 1 veut toujours dire
  « relevé écrit, NON conforme ».
⑥ TRAITEMENT — ① trouver les part.json sous `--depuis` et garder ceux de l'épreuve · ② exiger qu'ils s'accordent
  (épreuve, relevé, taille de lot, nombre de parts, noms des sabotages) et que les noms soient ceux de l'épreuve du
  jour · ③ exiger chaque numéro de part de 0 à N-1 une fois et une seule, chaque part avec exactement ses lots
  (`lots_de_la_part`), chaque lot avec sa sortie et son code, ce code lisible et égal à celui du manifeste ·
  ③bis pour CHAQUE flux de l'écoute (FLUX_D_ECOUTE du joueur : « ecoute », et « execution » depuis la version B),
  exiger qu'aucune part n'y ait nommé un programme interdit (`interdits_lus` de jouer_une_part.py), et que le flux
  existe ET nomme l'épreuve (`ecoute_nomme`, chemin de l'épreuve sur la machine de la part) pour toute part qui a
  joué un lot (une part sans lot peut arriver sans ses dossiers vides : une
  archive ne garde pas forcément un dossier vide) · ④ exiger le même etat_du_depart.json dans toutes les
  parts · ④bis exiger de chaque part sa place libre minimale (`lire_la_place` du joueur : chaque lot compté de la
  part porte « lot_NN.place », tour 3, B-2), et copier ces fichiers avec les lots : le joueur prend le minimum sur
  tous les lots et le juge contre son plancher · ⑤ écrire le dossier réuni : `preparer_le_travail` du joueur (module d'écoute et un dossier par flux),
  départ, début = le plus tôt des parts, lots, fichiers de chaque flux renommés
  « p<I>_… » (deux machines peuvent avoir le même numéro de processus), chemins de la racine des parts ramenés à la
  racine d'ici · ⑥ lancer le joueur avec ce dossier, `--lot` de la série et `--parts` = somme des lots joués en même
  temps par les parts · ⑦ si le joueur a joué un lot (ligne « ETAPE … lot k fini »), refuser : 2 · ⑧ ne rendre 0
  ou 1 que si le joueur a rendu 0 ou 1, a dit « FINI … relevé <relevé> » et que le relevé existe ; sinon 2.
⑦ UNITÉ — Heures de Paris dans debut.txt (« JJ-MM-AAAA HHhMM »), comme le joueur.
⑧ POURQUOI — Le relevé doit être celui que la machine aurait écrit : c'est le joueur qui l'écrit, pas une seconde
  rédaction (R-708). Une part perdue ou un sabotage perdu ne doit jamais donner un relevé conforme : ③ refuse la
  première, le joueur compte le second (« manquent »). Tour 2, relecture du 04-11-2026 : D1 (une part qui avait lu
  un programme interdit donnait un relevé « conforme ») → ③bis ; D2 (une part sans lot privée de son dossier vide
  « ecoute » faisait une trace en code 1, lu « NON conforme » à tort) → ③bis et la garde générale de `__main__` ;
  D3 (les codes du manifeste n'étaient jamais relus) → ③. Tour 3, relecture du 04-11-2026 à 19h53 et superviseur
  R-759 : I2 (une écoute vide passait) → ③bis `ecoute_nomme`, et le joueur patché refuse lui-même (« aucune écoute
  ne nomme l'épreuve ») ; M-b (le joueur qui plantait sortait en 1 sans relevé) → ⑧. 05-11-2026 (étude
  github_series/RAPPORT.md, §1.3) : la version B ajoute le flux « execution » ; ne réunir que « ecoute » aurait
  privé la portée « code_execute » de tout code exécuté (le joueur s'arrête alors : l'épreuve n'est pas couverte).
  La préparation, le découpage et la liste des flux sont ceux du joueur (R-708). Une trace d'erreur système dans la
  sortie d'un lot est jugée par le joueur, ici même : série NON CONFORME (1), jamais « mord ».
⑨ CE QUI CLOCHE — La ligne d'en-tête « série jouée du … au … , L lots de T au plus, P à la fois » diffère forcément
  d'un relevé de la machine : autres heures, et P compte les lots joués en même temps sur toutes les machines. Les
  empreintes, les lignes des sabotages et le verdict, eux, sont identiques (essai local du 04-11-2026). · Le
  partage `lots_de_la_part` vit dans jouer_une_part.py, le découpage `decouper` dans le joueur : un désaccord
  n'est vu qu'en ⑦, après coup. · La vérification que la racine n'a pas changé PENDANT chaque part est faite par la
  part elle-même ; ici, le joueur vérifie la racine d'ici contre le départ.
⑩ EFFET — Écrit le dossier réuni ; le joueur écrit le relevé dans la racine et y range l'ancien relevé de la même
  série dans archives/.
⑪ TERMINAISON — Rend la main ; sort par sys.exit avec le code dit en ⑤. Un de mes appels peut ne pas revenir : le
  joueur, s'il se mettait à rejouer un lot (découpage divergent), attendrait l'épreuve sans délai.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import traceback

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import jouer_une_part as PART   # noqa: E402  (découpage et partage : une rédaction pour les deux programmes)

ACCORD = ("epreuve", "releve", "lot", "nb_parts", "noms")   # ce que toutes les parts d'une série partagent


def arret(message):
    """Écrit le refus et rend le code 2.

    ① RÔLE — Un seul geste pour tout refus. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `message`. ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 2. ⑥ TRAITEMENT — print. ⑦ UNITÉ — — ⑧ POURQUOI — Repère « ARRET » en tête
    de ligne, comme le joueur. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit à l'écran. ⑪ TERMINAISON — Rend la main.
    """
    print(f"ARRET {message}", flush=True)
    return 2


def trouver_les_parts(depuis, epreuve):
    """Rend les parts de l'épreuve trouvées sous `depuis` : liste de (dossier, manifeste).

    ① RÔLE — Retrouver les parts quel que soit leur rangement. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `depuis` : le dossier ; `epreuve` : chemin relatif. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur :
    la liste, triée par dossier. ⑥ TRAITEMENT — os.walk, part.json lu en JSON, gardé si son épreuve est la nôtre.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le circuit extrait la branche de chaque part dans un sous-dossier à son nom (tour 3).
    ⑨ CE QUI CLOCHE — Un part.json illisible est ignoré ici, donc compté comme une part manquante (refus en ③).
    ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main.
    """
    trouvees = []
    for r, ds, fs in os.walk(depuis):
        ds.sort()
        if PART.MANIFESTE in fs:
            try:
                m = json.load(open(os.path.join(r, PART.MANIFESTE), encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if m.get("epreuve") == epreuve:
                trouvees.append((r, m))
    return sorted(trouvees, key=lambda dm: dm[0])


def lire_les_arguments(arguments):
    """Rend ce que le rassembleur lit de sa ligne de commande : {racine, epreuve, releve, depuis, travail} ; lève
    ValueError si elle ne convient pas.

    ① RÔLE — Lire la ligne de commande en UN endroit, que l'épreuve du relais des séries appelle elle-même (relevé
      du Chat n°347, Q3 = 1).
    ② CONTEXTE D'APPEL — `main` ; tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py.
    ③ ENTRÉE — `arguments` : sys.argv[1:].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire (racine, depuis, travail en chemins réels ; raisons_acceptees : le texte
      de l'option, ou None). [rend: 1]
    ⑥ TRAITEMENT — trois arguments sans « -- » ; les options « --depuis=… » et « --travail=… », chacune exactement une
      fois, « --raisons-acceptees=… » au plus une fois ; toute autre option est refusée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Défaut NV-2 du lot 262 (relevé n°298) : une option donnée deux fois gardait la dernière valeur.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    pos = [a for a in arguments if not a.startswith("--")]
    opt = {}
    for a in arguments:
        if not a.startswith("--"):
            continue
        nom, egal, valeur = a[2:].partition("=")
        if not egal or nom not in ("depuis", "travail", "raisons-acceptees") or nom in opt:
            raise ValueError(f"option refusée (inconnue, sans valeur ou donnée deux fois) : {a[:60]}")
        opt[nom] = valeur
    if len(pos) != 3 or not {"depuis", "travail"} <= set(opt):
        raise ValueError("trois arguments sans « -- », --depuis et --travail attendus")
    return {"racine": os.path.realpath(pos[0]), "epreuve": pos[1], "releve": pos[2],
            "depuis": os.path.realpath(opt["depuis"]), "travail": os.path.realpath(opt["travail"]),
            "raisons_acceptees": opt.get("raisons-acceptees")}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. ⑥ TRAITEMENT — Fiche en tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête. ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Fiche en tête.
    """
    try:
        arguments_lus = lire_les_arguments(sys.argv[1:])
    except ValueError as e:
        return arret(f"usage ({e}) : rassembler_les_parts.py <racine> <épreuve> <relevé> --depuis=<parts> --travail=<dossier>")
    racine, epreuve, releve, depuis, travail = arguments_lus["racine"], arguments_lus["epreuve"], arguments_lus["releve"], arguments_lus["depuis"], arguments_lus["travail"]
    if os.path.exists(travail) and os.listdir(travail):
        return arret(f"le dossier de travail {travail} n'est pas vide : un rassemblement ne se mélange pas à un autre")
    # ① ② les parts et leur accord
    parts = trouver_les_parts(depuis, epreuve)
    if not parts:
        return arret(f"aucune part de {epreuve} sous {depuis}")
    for cle in ACCORD:
        valeurs = {json.dumps(m.get(cle), ensure_ascii=False) for _, m in parts}
        if len(valeurs) != 1:
            return arret(f"les parts ne s'accordent pas sur « {cle} »")
    m0 = parts[0][1]
    if m0["releve"] != releve:
        return arret(f"les parts ont été jouées pour le relevé {m0['releve']}, pas pour {releve}")
    try:
        joueur = PART.charger_le_joueur(racine)
        noms = joueur.SERIE.noms_des_sabotages(os.path.join(racine, epreuve))
    except (OSError, SyntaxError, ValueError, ImportError) as e:
        return arret(f"joueur ou épreuve illisible dans la racine : {type(e).__name__} : {e}")
    if noms != m0["noms"]:
        return arret("les sabotages de l'épreuve d'ici ne sont pas ceux des parts : autre version")
    # ③ chaque part une fois, chaque lot une fois, avec sa sortie et son code
    nb, taille = m0["nb_parts"], m0["lot"]
    lots = joueur.decouper(noms, taille)
    vus = sorted(m["part"] for _, m in parts)
    if vus != list(range(nb)):
        manquent = sorted(set(range(nb)) - set(vus))
        doubles = sorted({p for p in vus if vus.count(p) > 1})
        return arret(f"parts attendues 0 à {nb - 1} : manquent {manquent or 'aucune'}, en double {doubles or 'aucune'}")
    for d, m in parts:
        attendus = PART.lots_de_la_part(len(lots), nb, m["part"])
        if m["lots"] != attendus:
            return arret(f"la part {m['part']} a joué les lots {m['lots']}, elle devait jouer {attendus}")
        for k in attendus:
            for suffixe in ("out", "code"):
                if not os.path.isfile(os.path.join(d, f"lot_{k:02d}.{suffixe}")):
                    return arret(f"la part {m['part']} n'a pas lot_{k:02d}.{suffixe}")
        # ③ le code de chaque lot : lisible, et celui que le manifeste a noté à la fin de la part (D3)
        codes = m.get("codes")
        if not isinstance(codes, dict) or sorted(codes) != sorted(str(k) for k in attendus):
            return arret(f"la part {m['part']} : le manifeste ne porte pas un code par lot joué")
        for k in attendus:
            try:
                lu = int(open(os.path.join(d, f"lot_{k:02d}.code")).read().strip())
            except ValueError:
                return arret(f"la part {m['part']} : lot_{k:02d}.code illisible")
            if lu != codes[str(k)]:
                return arret(f"la part {m['part']} : lot_{k:02d}.code dit {lu}, le manifeste dit {codes[str(k)]}")
        # ③bis chaque flux : aucun programme interdit nommé (D1) ; le flux n'est exigé que d'une part qui a joué (D2)
        for nom_du_flux in joueur.FLUX_D_ECOUTE.values():
            fautives = PART.interdits_lus(os.path.join(d, nom_du_flux))
            if fautives is None and attendus:
                return arret(f"la part {m['part']} a joué {len(attendus)} lot(s) mais son flux d'écoute « {nom_du_flux} » "
                             "manque")
            if fautives:
                return arret(f"la part {m['part']} a lu un programme interdit dans ce circuit : {', '.join(fautives[:3])}")
            if attendus and not PART.ecoute_nomme(os.path.join(d, nom_du_flux),
                                                  os.path.normpath(os.path.join(m["racine"], epreuve))):
                return arret(f"la part {m['part']} a joué {len(attendus)} lot(s) mais son flux d'écoute « {nom_du_flux} » "
                             "ne nomme pas l'épreuve : écoute sourde")
    # ④ même départ partout
    departs = {open(os.path.join(d, "etat_du_depart.json"), "rb").read() for d, _ in parts}
    if len(departs) != 1:
        return arret("les parts ne sont pas parties du même état du dépôt (etat_du_depart.json différents)")
    # ④bis le témoin du milieu de chaque part (superviseur R-759 du 05-11-2026, M1 (2)) : sans lui, rien de sûr
    places = {m["part"]: joueur.lire_la_place(d) for d, m in parts}
    sans = sorted(p for p, v in places.items() if v is None)
    if sans:
        return arret(f"la part {sans[0]} n'a pas noté sa place libre minimale : le milieu de ses lots est inconnu")
    # ⑤ le dossier réuni
    # le module d'écoute et un dossier par flux : la préparation du joueur de la racine (R-708), rien venu d'une part
    joueur.preparer_le_travail(travail)
    shutil.copyfile(os.path.join(parts[0][0], "etat_du_depart.json"), os.path.join(travail, "etat_du_depart.json"))
    debuts = [datetime.datetime.strptime(open(os.path.join(d, "debut.txt")).read().strip(), "%d-%m-%Y %Hh%M")
              for d, _ in parts]
    open(os.path.join(travail, "debut.txt"), "w").write(min(debuts).strftime("%d-%m-%Y %Hh%M"))
    for d, m in parts:
        for k in m["lots"]:
            for suffixe in ("out", joueur.SUFFIXE_DE_LA_PLACE, "code"):
                # une place absente n'est pas jugée ici : la garde ④bis l'a déjà refusée (une garde, une place ;
                # sinon la copie plantait et rendait 2 pour une autre raison — sabotage SP3 du tour 3, « NE MORD PAS »)
                if suffixe == joueur.SUFFIXE_DE_LA_PLACE and not os.path.isfile(os.path.join(d, f"lot_{k:02d}.{suffixe}")):
                    continue
                shutil.copyfile(os.path.join(d, f"lot_{k:02d}.{suffixe}"), os.path.join(travail, f"lot_{k:02d}.{suffixe}"))
        ailleurs = m["racine"].rstrip(os.sep) + os.sep
        for nom_du_flux in joueur.FLUX_D_ECOUTE.values():
            ecoute = os.path.join(d, nom_du_flux)
            for f in sorted(os.listdir(ecoute)) if os.path.isdir(ecoute) else []:
                lignes = open(os.path.join(ecoute, f), encoding="utf-8", errors="replace").read().splitlines()
                lignes = [racine + os.sep + l[len(ailleurs):] if l.startswith(ailleurs) else l for l in lignes]
                with open(os.path.join(travail, nom_du_flux, f"p{m['part']}_{f}"), "w", encoding="utf-8") as s:
                    s.write("".join(l + "\n" for l in lignes))
    ensemble = sum(m["parallele"] for _, m in parts)
    print(f"ETAPE {len(parts)} parts réunies : {len(lots)} lots de {taille} au plus, {ensemble} à la fois en tout",
          flush=True)
    # ⑥ le joueur du dépôt écrit le relevé
    joueur = os.path.join(racine, PART.JOUEUR)
    r = subprocess.run([sys.executable, "-B", "-u", joueur, racine, epreuve, releve, f"--lot={taille}",
                        f"--parts={ensemble}", f"--travail={travail}"]
                       + ([f"--raisons-acceptees={arguments_lus['raisons_acceptees']}"] if arguments_lus["raisons_acceptees"] else []),
                       capture_output=True, text=True)
    print(r.stdout + r.stderr, end="", flush=True)
    # ⑦ le joueur ne devait rien rejouer
    if re.search(r"^ETAPE \S+ lot \d+ fini", r.stdout, re.M):
        return arret("le joueur a rejoué au moins un lot : son découpage n'est pas celui des parts — relevé non fiable")
    # ⑧ (M-b) : 0 ou 1 seulement si le joueur l'a rendu, a dit FINI pour CE relevé, et que le relevé existe.
    if r.returncode == 2:
        return 2
    if r.returncode not in (0, 1):
        return arret(f"le joueur s'est arrêté sur le code {r.returncode} : rien de sûr")
    dit_fini = re.search(r"^FINI \S+ relevé " + re.escape(releve) + " : ", r.stdout, re.M)
    if not dit_fini or not os.path.isfile(os.path.join(racine, releve)):
        return arret(f"le joueur a rendu {r.returncode} sans avoir fini le relevé {releve} (trace ci-dessus ?) : "
                     "rien de sûr")
    return r.returncode


if __name__ == "__main__":
    # GARDE GÉNÉRALE (D2) : une erreur imprévue (fichier d'une part illisible, debut.txt absent, JSON tronqué…) ne doit
    # jamais sortir en code 1, qui veut dire « relevé écrit, NON conforme » : elle sort en ARRET, code 2, avec sa trace.
    try:
        code = main()
    except Exception as e:   # noqa: BLE001 — toute erreur, par construction
        traceback.print_exc()
        code = arret(f"erreur imprévue, rien de sûr : {type(e).__name__} : {e}")
    sys.exit(code)
