#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_SERIES_LONGUES_AU_RELAIS — Mer 11-11-2026 (Paris), agent E du plan V7. Simulation uniquement.

LE SENS EN TÊTE. Une seule propriété : TOUTE SÉRIE LONGUE DE SABOTAGES DU DÉPÔT A UNE LIGNE AU CIRCUIT DES SÉRIES, donc
peut partir sur GitHub par le relais (plan V7, bloc 2bis « Toutes les séries longues sur GitHub » : une ligne par série
dans la table du relais, pour ôter ces calculs de la machine du Chat, 2 processeurs). Avant le 11-11-2026, seules les
séries Yahoo et HL avaient une ligne ; celles de la boucle de check et de l'arrivée des signaux, qui ont un relevé, n'en
avaient pas, et rien ne le signalait.

① RÔLE — Rougir si une série longue de sabotages existe sans ligne au circuit des séries (« serie_du_circuit » d'une
  entrée de « series_hors_de_la_nuit » de tests/LANCEMENT_DES_EPREUVES.json, lue par la fonction même qui fabrique le
  circuit, `series_du_circuit` de programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py). Avec `--recenser`, imprimer le
  recensement des séries longues et des longs lancements « --saboter » de la nuit.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine, puis avec
  « --saboter ») ; à la main avant toute livraison qui touche la table, un relevé de série ou le fabricant du circuit
  (R-731) : python3 tests/EPREUVES_DES_SERIES_LONGUES_AU_RELAIS_Mer_11-11-2026.py <racine> [--saboter | --recenser]
③ ENTRÉE — La racine d'un dépôt : on y lit tests/LANCEMENT_DES_EPREUVES.json, les relevés de séries (dossier
  tests/resultats/ et dossier de chaque motif « releve » de la table), programmes/SERIES_DE_SABOTAGES.py (ENTETE, la
  première ligne de tout relevé) et programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (`series_du_circuit`).
④ CONDITIONS D'ENTRÉE — Aucune ; une table ou un module illisible est un cas faux (code 1), jamais un succès.
⑤ SORTIE — Le code de sortie : 0 si chaque cas (C0 à C8) donne la réponse attendue et, avec --saboter, si chaque
  sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus. Avec --recenser : 0, ou 1 si
  une série longue est sans ligne. [rend: 1]
⑥ TRAITEMENT — UNE SÉRIE LONGUE est (a) une épreuve nommée par un RELEVÉ DE SÉRIE — un fichier dont la première ligne
  est SERIES_DE_SABOTAGES.ENTETE, l'épreuve étant lue sur sa deuxième ligne « # épreuve : <chemin> » (le contenu, jamais
  le nom du fichier : si je renomme un relevé, le contrôle ne change pas d'avis) — ou (b) une épreuve déclarée dans
  « series_hors_de_la_nuit » (jouée hors de la nuit : sa série est longue par décision). Chacune doit exister et être
  rendue par `series_du_circuit` ; si le fabricant refuse la table (plus de séries que le bouton n'en porte, code mal
  formé), c'est faux aussi : aucune série ne peut alors partir. Pour chaque série du circuit qui a un relevé, le lot
  de la table doit être celui écrit dans l'en-tête du relevé (sinon ses lignes « lot k » ne sont plus comparables).
  Cas, sur des copies réduites (la table, les relevés, un fichier vide par épreuve existante) : C0 (R-732, les VRAIES
  lignes) le dépôt tel quel : aucune série sans ligne, et le recensement retrouve Yahoo et HL, qu'on sait exister
  (calibrage qui doit réussir) · C1 la ligne de la boucle de check retirée → rouge, l'épreuve nommée · C2 le relevé de
  l'arrivée des signaux RENOMMÉ → toujours vert · C3 l'épreuve de la boucle renommée partout (fichier, clé de la table,
  ligne du relevé) → toujours vert · C4 un relevé à un nom quelconque, de contenu vrai, pour une épreuve sans entrée
  → rouge · C5 un fichier NOMMÉ « SERIE_DE_SABOTAGES_… » sans l'en-tête d'un relevé → ne compte pas (calibrage qui
  doit échouer : le motif ne sur-détecte pas) · C6 une entrée « series_hors_de_la_nuit » sans relevé ni ligne → rouge ·
  C7 cinq séries au circuit (plus que SERIES_AU_PLUS) → rouge · C8 une ligne au circuit pour une épreuve absente du
  dépôt → rouge · C9 un relevé dont la deuxième ligne n'est pas « # épreuve : » → rouge (relevé illisible) ·
  (relecture du 11-11-2026) C10 le relevé des signaux rangé dans archives/ : son absence est dite, sans trace Python
  (D1) · C11 le lot de la boucle changé dans la table → rouge, il n'est plus celui de l'en-tête du relevé (L2) · C12
  un en-tête de relevé sans « N lots de L au plus » → rouge (taille de lot illisible, jamais un vert).
  Sabotages : chacun retire ce qu'un cas éprouve, sur une copie de CE fichier, et la copie doit rougir.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Plan V7, bloc 2bis ; R-731 (une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une
  preuve) ; « réparer par une propriété, jamais par une énumération » (instructions du projet, §7) : aucune série
  n'est nommée dans le contrôle ; R-708 : la table est lue par le lecteur du fabricant, pas relue ici à sa façon.
⑨ CE QUI CLOCHE — Une série longue qui n'a NI relevé NI entrée « series_hors_de_la_nuit » n'est pas vue : les longs
  lancements « --saboter » de la nuit (délais de la table au-delà de 15 minutes, par exemple la lecture des cours,
  10 800 s) restent dans la certification et ne sont pas des séries du circuit ; les en faire sortir est une décision
  de Jean-Luc (ce contrôle retiré de la nuit) et bute sur SERIES_AU_PLUS (4 séries, limite de 10 entrées du bouton).
  `--recenser` les imprime, sans les juger. Les relevés rangés dans archives/ (remplacés) ne comptent pas. Le
  circuit n'est pas joué ici : qu'une ligne parte vraiment sur GitHub reste prouvé par un passage (THÉORIQUE pour
  Boucle et Signaux au 11-11-2026).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque copie sabotée est bornée à 120 secondes ; sort par sys.exit.
  [sort: oui]
"""
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
MODULE_SERIES = "programmes/SERIES_DE_SABOTAGES.py"
RESULTATS = "tests/resultats"
LIGNE_EPREUVE = "# épreuve : "          # deuxième ligne d'un relevé (SERIES_DE_SABOTAGES.ecrire_le_releve)
# la taille de lot d'un relevé, telle que tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py l'écrit dans son en-tête
# (« 11 lots de 6 au plus ») ; calibré le 11-11-2026 sur les quatre relevés réels (cas C0), et sur un en-tête qui ne la
# porte pas (cas C12, qui doit rougir)
TAILLE_DE_LOT = re.compile(r"\b([0-9]+) lots? de ([0-9]+) au plus\b")
LIGNES_D_ENTETE = 8                     # la taille de lot est cherchée dans les premières lignes du relevé
SEUIL_LONG = 900                        # secondes : « longues séries (plus de 15 min) », cadre des agents du 11-11-2026, §5
CONNUES = ("tests/EPREUVES_DU_COURS_PROPRE_DE_YAHOO_Jeu_22-10-2026.py",     # calibrage C0 : séries qu'on sait exister
           "tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py")
BOUCLE = "tests/EPREUVES_DE_LA_BOUCLE_DE_CHECK_Ven_16-10-2026.py"           # cas réels de C1, C3
SIGNAUX = "tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py"       # cas réel de C2


def charger(chemin, nom):
    """Charge un programme comme un module, sous un nom à lui.

    ① RÔLE — Lire ENTETE et `series_du_circuit` là où ils vivent (R-708).
    ② CONTEXTE D'APPEL — `modules`.
    ③ ENTRÉE — `chemin` : le fichier ; `nom` : le nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module. Lève toute erreur du chargement. [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Éprouver les modules de la racine donnée, pas ceux du dossier de cette épreuve.
    ⑨ CE QUI CLOCHE — Le fabricant lit SA table au chargement (sa racine) ; seule `series_du_circuit(racine)` est
      appelée ici, avec la racine éprouvée.
    ⑩ EFFET — Exécute le haut du module.
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(chemin))
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path.pop(0)
    return m


def modules(racine):
    """Rend (ENTETE, series_du_circuit) lus à la racine.

    ① RÔLE — Donner au contrôle l'en-tête des relevés et le lecteur de la table du fabricant.
    ② CONTEXTE D'APPEL — `eprouver`, `recenser`.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Les deux programmes existent à la racine.
    ⑤ SORTIE — DEUX valeurs : le texte de l'en-tête, la fonction. Lève si un module ne se charge pas. [rend: 2]
    ⑥ TRAITEMENT — `charger` deux fois.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Charge deux modules.
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    s = charger(os.path.join(racine, MODULE_SERIES), "SERIES_EPROUVE_E")
    f = charger(os.path.join(racine, FABRICANT), "FABRICANT_EPROUVE_E")
    return s.ENTETE, f.series_du_circuit


def series_longues(racine, entete):
    """Rend les séries longues de la racine : {épreuve : [sources]}, et les relevés illisibles.

    ① RÔLE — Recenser par leur CONTENU les relevés de séries, et les déclarations « series_hors_de_la_nuit ».
    ② CONTEXTE D'APPEL — `series_sans_ligne`, `recenser`.
    ③ ENTRÉE — `racine` ; `entete` : la première ligne de tout relevé (SERIES_DE_SABOTAGES.ENTETE).
    ④ CONDITIONS D'ENTRÉE — La table se lit en JSON (sinon lève).
    ⑤ SORTIE — DEUX valeurs : le dictionnaire épreuve → liste de sources (« relevé <chemin> » ou « table »), et la
      liste des relevés illisibles (en-tête de relevé, deuxième ligne sans l'épreuve). [rend: 2]
    ⑥ TRAITEMENT — les dossiers lus : tests/resultats/ et le dossier de chaque motif « releve » de la table ; chaque
      fichier ordinaire dont la première ligne vaut `entete` est un relevé ; sa deuxième ligne nomme l'épreuve ; puis
      chaque clé de « series_hors_de_la_nuit ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contenu et non le nom (« si je renomme un fichier, mon contrôle change-t-il d'avis ? »).
    ⑨ CE QUI CLOCHE — Un relevé hors de ces dossiers n'est pas vu (voir la fiche en tête, ⑨).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    table = json.load(open(os.path.join(racine, TABLE), encoding="utf-8"))
    hors = table.get("series_hors_de_la_nuit") or {}
    dossiers = {RESULTATS} | {os.path.dirname(e.get("releve", "")) for e in hors.values()
                              if isinstance(e, dict) and isinstance(e.get("releve"), str)}
    longues, illisibles = {}, []
    for d in sorted(x for x in dossiers if x):
        for chemin in sorted(glob.glob(os.path.join(racine, d, "*"))):
            if not os.path.isfile(chemin):
                continue
            with open(chemin, encoding="utf-8", errors="replace") as f:
                tete = [f.readline().rstrip("\n") for _ in range(2)]
            if tete[0] != entete:
                continue
            rel = os.path.relpath(chemin, racine)
            if not tete[1].startswith(LIGNE_EPREUVE):
                illisibles.append(rel)
                continue
            longues.setdefault(tete[1][len(LIGNE_EPREUVE):].strip(), []).append("relevé " + rel)
    for epreuve in hors:
        longues.setdefault(epreuve, []).append("table")
    return longues, illisibles


def lots_des_releves(racine, longues):
    """Rend [(épreuve, relevé, lot ou None)] : la taille de lot écrite dans l'en-tête de chaque relevé.

    ① RÔLE — Lire, dans le relevé lui-même, la taille de lot avec laquelle la série a été jouée.
    ② CONTEXTE D'APPEL — `series_sans_ligne`.
    ③ ENTRÉE — `racine` ; `longues` : le premier résultat de `series_longues`.
    ④ CONDITIONS D'ENTRÉE — Chaque relevé nommé existe.
    ⑤ SORTIE — UNE valeur : la liste des triplets ; lot = None si l'en-tête ne porte pas TAILLE_DE_LOT. [rend: 1]
    ⑥ TRAITEMENT — les LIGNES_D_ENTETE premières lignes de chaque relevé, première correspondance de TAILLE_DE_LOT.
    ⑦ UNITÉ — lot : des sabotages par lot.
    ⑧ POURQUOI — Relecture du 11-11-2026, L2 : la ligne du circuit reprend le lot du dernier relevé pour que ses
      lignes « lot k » restent comparables ; rien ne le vérifiait. Le lot se lit au relevé, jamais écrit ici.
    ⑨ CE QUI CLOCHE — Le motif dépend de la phrase écrite par le joueur : s'il la change, le lot devient illisible et
      le contrôle rougit (voulu : jamais un vert sur un en-tête non lu).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    res = []
    for epreuve, sources in sorted(longues.items()):
        for src in sources:
            if src.startswith("relevé "):
                rel = src[len("relevé "):]
                with open(os.path.join(racine, rel), encoding="utf-8", errors="replace") as f:
                    tete = " ".join(f.readline() for _ in range(LIGNES_D_ENTETE))
                m = TAILLE_DE_LOT.search(tete)
                res.append((epreuve, rel, int(m.group(2)) if m else None))
    return res


def series_sans_ligne(racine, entete, series_du_circuit):
    """Rend la liste des défauts : séries longues sans ligne au circuit, épreuves absentes, table refusée.

    ① RÔLE — Le contrôle lui-même.
    ② CONTEXTE D'APPEL — `eprouver` (chaque cas), `recenser`.
    ③ ENTRÉE — `racine` ; `entete` ; `series_du_circuit` : la fonction du fabricant.
    ④ CONDITIONS D'ENTRÉE — Voir `series_longues`.
    ⑤ SORTIE — UNE valeur : la liste des défauts, textes ; vide = conforme. [rend: 1]
    ⑥ TRAITEMENT — lire le circuit par le fabricant (refus = défaut) ; chaque série longue doit exister à la racine
      et être une épreuve du circuit ; chaque relevé illisible est un défaut ; pour chaque série du circuit qui a un
      relevé, le lot de la table doit être celui de l'en-tête du relevé (`lots_des_releves`), illisible = défaut.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Plan V7, bloc 2bis.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    longues, illisibles = series_longues(racine, entete)
    defauts = [f"relevé illisible (deuxième ligne sans « {LIGNE_EPREUVE.strip()} ») : {r}" for r in illisibles]
    try:
        lignes = series_du_circuit(racine)
    except (OSError, ValueError) as e:
        return defauts + [f"le fabricant refuse la table, aucune série ne peut partir : {e}"]
    circuit = {e for _, e, _, _ in lignes}
    lot_de = {e: l for _, e, _, l in lignes}
    for epreuve, sources in sorted(longues.items()):
        if not os.path.isfile(os.path.join(racine, epreuve)):
            defauts.append(f"{epreuve} : épreuve absente du dépôt ({', '.join(sources)})")
        elif epreuve not in circuit:
            defauts.append(f"{epreuve} : série longue sans ligne au circuit des séries ({', '.join(sources)})")
    for epreuve, rel, lot in lots_des_releves(racine, longues):
        if epreuve not in lot_de:
            continue
        if lot is None:
            defauts.append(f"{rel} : taille de lot illisible (aucun « N lots de L au plus » dans l'en-tête)")
        elif lot != lot_de[epreuve]:
            defauts.append(f"{epreuve} : lot de la table {lot_de[epreuve]}, lot du relevé {lot} ({rel}) — les lignes "
                           "« lot k » d'un nouveau relevé ne seraient plus comparables")
    return defauts


def copie_reduite(racine, d):
    """Rend une racine réduite : la table, les relevés, les deux modules lus, un fichier vide par épreuve existante.

    ① RÔLE — Donner à chaque cas un terrain à modifier sans toucher au dépôt.
    ② CONTEXTE D'APPEL — `eprouver`, une fois par cas.
    ③ ENTRÉE — `racine` ; `d` : un dossier jetable.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de la copie. [rend: 1]
    ⑥ TRAITEMENT — copier tests/resultats/, la table ; créer vide chaque épreuve de tests/ (sa seule existence compte).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les VRAIES lignes de la table et des relevés (R-732), sans recopier 500 Mo.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    c = tempfile.mkdtemp(dir=d)
    shutil.copytree(os.path.join(racine, RESULTATS), os.path.join(c, RESULTATS))
    shutil.copyfile(os.path.join(racine, TABLE), os.path.join(c, TABLE))
    for f in os.listdir(os.path.join(racine, "tests")):
        if f.endswith(".py"):
            open(os.path.join(c, "tests", f), "w").close()
    return c


def table_de(c):
    """Rend la table JSON de la copie `c`.

    ① RÔLE — Lire la table d'une copie réduite.
    ② CONTEXTE D'APPEL — `eprouver`, cas C1, C3, C6, C7.
    ③ ENTRÉE — `c` : la copie.
    ④ CONDITIONS D'ENTRÉE — La table existe.
    ⑤ SORTIE — UNE valeur : le dictionnaire. [rend: 1]
    ⑥ TRAITEMENT — json.load.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Chaque cas modifie la VRAIE table (R-732).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève si illisible. [sort: non]
    """
    return json.load(open(os.path.join(c, TABLE), encoding="utf-8"))


def ecrire_table(c, t):
    """Écrit la table `t` dans la copie `c`.

    ① RÔLE — Poser la table modifiée d'un cas.
    ② CONTEXTE D'APPEL — `eprouver`, cas C1, C3, C6, C7.
    ③ ENTRÉE — `c` : la copie ; `t` : le dictionnaire.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — json.dumps, même forme que la table du dépôt (indentation 1, UTF-8, fin de ligne).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fabricant relit la table de la copie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans la copie jetable.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    open(os.path.join(c, TABLE), "w", encoding="utf-8").write(json.dumps(t, indent=1, ensure_ascii=False) + "\n")


def releve_de(c, epreuve, entete):
    """Rend le chemin du relevé de `epreuve` dans la copie `c`, trouvé par son contenu.

    ① RÔLE — Trouver le vrai relevé d'une épreuve sans dépendre de son nom.
    ② CONTEXTE D'APPEL — `eprouver`, cas C2, C3, C9.
    ③ ENTRÉE — `c` : la copie ; `epreuve` : chemin relatif ; `entete` : la première ligne d'un relevé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin, ou None si aucun relevé ne la nomme (relevé rangé dans archives/, épreuve
      renommée : relecture du 11-11-2026, D1 — le cas est alors déclaré faux par son nom, sans trace Python). [rend: 1]
    ⑥ TRAITEMENT — les deux premières lignes de chaque fichier de tests/resultats/ de la copie.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les cas renomment des fichiers : les retrouver par leur nom serait circulaire.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return next((p for p in glob.glob(os.path.join(c, RESULTATS, "*"))
                 if open(p, encoding="utf-8", errors="replace").read().split("\n")[:2] == [entete, LIGNE_EPREUVE + epreuve]),
                None)


def eprouver(racine):
    """Joue les cas C0 à C12 ; rend la liste des cas faux.

    ① RÔLE — Les cas de la fiche en tête, ⑥.
    ② CONTEXTE D'APPEL — `main`, et chaque copie sabotée.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des cas faux (textes). [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731, R-732.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        entete, circuit = modules(racine)
    except Exception as e:   # noqa: BLE001 — tout échec de chargement est un cas faux
        return [f"chargement : {type(e).__name__} : {e}"]
    faux = []
    d = tempfile.mkdtemp(prefix="series_longues_E_")
    try:
        def cas(nom, c, rouge, doit_nommer=None):
            """Juge un cas : `rouge` = des défauts sont attendus ; `doit_nommer` : un texte qu'un défaut doit porter.

            ① RÔLE — Comparer le verdict du contrôle à l'attendu d'un cas.
            ② CONTEXTE D'APPEL — `eprouver`, une fois par cas.
            ③ ENTRÉE — `nom`, `c` (la copie), `rouge`, `doit_nommer` (facultatif).
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur ; ajoute un texte à `faux` si le cas est faux. [rend: 0]
            ⑥ TRAITEMENT — `series_sans_ligne` ; rouge attendu = au moins un défaut ; le défaut doit nommer ce qu'il faut.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un rouge pour une autre raison que celle du cas ne prouve rien.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Modifie `faux`.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            try:
                defauts = series_sans_ligne(c, entete, circuit)
            except Exception as e:   # noqa: BLE001
                faux.append(f"{nom} : le contrôle lève {type(e).__name__} : {e}")
                return
            if bool(defauts) != rouge:
                faux.append(f"{nom} : attendu {'rouge' if rouge else 'vert'}, obtenu {defauts or 'vert'}")
            elif doit_nommer and not any(doit_nommer in x for x in defauts):
                faux.append(f"{nom} : aucun défaut ne nomme {doit_nommer} : {defauts}")

        # C0 — le dépôt tel quel, et le calibrage du recensement sur des séries qu'on sait exister
        cas("C0 dépôt tel quel", racine, False)
        longues, _ = series_longues(racine, entete)
        for connue in CONNUES:
            if not any(s.startswith("relevé ") for s in longues.get(connue, [])):
                faux.append(f"C0 calibrage : le recensement ne retrouve pas le relevé de {connue}")
        # C1 — la ligne de la boucle retirée
        c = copie_reduite(racine, d)
        t = table_de(c)
        t["series_hors_de_la_nuit"][BOUCLE].pop("serie_du_circuit", None)
        ecrire_table(c, t)
        cas("C1 ligne de la boucle retirée", c, True, BOUCLE)
        # C2 — le relevé des signaux renommé
        c = copie_reduite(racine, d)
        p = releve_de(c, SIGNAUX, entete)
        if p is None:
            faux.append(f"C2 aucun relevé ne nomme {SIGNAUX} (rangé dans archives/ ou épreuve renommée ?)")
        else:
            os.rename(p, os.path.join(c, RESULTATS, "NOM_SANS_RAPPORT.txt"))
        cas("C2 relevé renommé", c, False)
        if p is not None and "relevé " + RESULTATS + "/NOM_SANS_RAPPORT.txt" not in series_longues(c, entete)[0].get(SIGNAUX, []):
            faux.append("C2 le relevé renommé ne compte plus : le vert ne viendrait que de la table")
        # C3 — l'épreuve de la boucle renommée partout
        c = copie_reduite(racine, d)
        neuf = "tests/EPREUVES_RENOMMEE_Mer_11-11-2026.py"
        p = releve_de(c, BOUCLE, entete)
        if p is None:
            faux.append(f"C3 aucun relevé ne nomme {BOUCLE} (rangé dans archives/ ou épreuve renommée ?)")
        else:
            texte = open(p, encoding="utf-8").read()        # lu AVANT d'ouvrir en écriture, qui vide le fichier
            open(p, "w", encoding="utf-8").write(texte.replace(BOUCLE, neuf))
        os.rename(os.path.join(c, BOUCLE), os.path.join(c, neuf))
        t = table_de(c)
        t["series_hors_de_la_nuit"] = {(neuf if k == BOUCLE else k): v for k, v in t["series_hors_de_la_nuit"].items()}
        ecrire_table(c, t)
        cas("C3 épreuve renommée partout", c, False)
        if p is not None and not any(x.startswith("relevé ") for x in series_longues(c, entete)[0].get(neuf, [])):
            faux.append("C3 le relevé de l'épreuve renommée ne compte plus : le vert ne viendrait que de la table")
        # C4 — un relevé de nom quelconque, de contenu vrai, pour une épreuve sans entrée
        c = copie_reduite(racine, d)
        orpheline = "tests/EPREUVES_SANS_LIGNE_Mer_11-11-2026.py"
        open(os.path.join(c, orpheline), "w").close()
        open(os.path.join(c, RESULTATS, "quelconque.log"), "w", encoding="utf-8").write(
            f"{entete}\n{LIGNE_EPREUVE}{orpheline}\nVERDICT : tout est conforme\n")
        cas("C4 relevé de nom quelconque sans ligne", c, True, orpheline)
        # C5 — un fichier nommé comme un relevé, sans son en-tête : ne compte pas
        c = copie_reduite(racine, d)
        open(os.path.join(c, RESULTATS, "SERIE_DE_SABOTAGES_DE_RIEN_Mer_11-11-2026_02h00.txt"), "w",
             encoding="utf-8").write(f"# un texte quelconque\n{LIGNE_EPREUVE}{orpheline}\n")
        cas("C5 nom de relevé sans en-tête", c, False)
        # C6 — une entrée hors de la nuit sans relevé ni ligne
        c = copie_reduite(racine, d)
        open(os.path.join(c, orpheline), "w").close()
        t = table_de(c)
        t["series_hors_de_la_nuit"][orpheline] = {"releve": RESULTATS + "/SERIE_ORPHELINE_*.txt",
                                                  "essais_refaits_chaque_nuit": 0, "pourquoi": "cas C6"}
        ecrire_table(c, t)
        cas("C6 entrée hors de la nuit sans ligne", c, True, orpheline)
        # C7 — une série de plus que le bouton n'en porte (SERIES_AU_PLUS lu chez le fabricant, R-708 : autant de
        # séries ajoutées qu'il en faut pour le dépasser d'une, quel que soit le nombre déjà à la table)
        c = copie_reduite(racine, d)
        t = table_de(c)
        deja = sum(1 for e in t["series_hors_de_la_nuit"].values() if isinstance(e, dict) and "serie_du_circuit" in e)
        for k in range(max(1, circuit.__globals__["SERIES_AU_PLUS"] + 1 - deja)):
            ajout = f"tests/EPREUVES_EN_TROP_{k}_Mer_11-11-2026.py"
            open(os.path.join(c, ajout), "w").close()
            t["series_hors_de_la_nuit"][ajout] = {"releve": RESULTATS + f"/SERIE_EN_TROP_{k}_*.txt",
                                                  "essais_refaits_chaque_nuit": 0, "pourquoi": "cas C7",
                                                  "serie_du_circuit": {"code": f"EnTrop{k}", "machines": 1, "lot": 1}}
        ecrire_table(c, t)
        cas("C7 plus de séries que le bouton", c, True, "refuse la table")
        # C8 — une ligne au circuit pour une épreuve absente
        c = copie_reduite(racine, d)
        os.remove(os.path.join(c, SIGNAUX))
        cas("C8 épreuve absente", c, True, SIGNAUX)
        # C9 — un relevé illisible
        c = copie_reduite(racine, d)
        p = releve_de(c, SIGNAUX, entete)
        if p is None:
            faux.append(f"C9 aucun relevé ne nomme {SIGNAUX} (rangé dans archives/ ou épreuve renommée ?)")
        else:
            lignes = open(p, encoding="utf-8").read().split("\n")
            open(p, "w", encoding="utf-8").write("\n".join([lignes[0], "# autre chose"] + lignes[2:]))
            cas("C9 relevé illisible", c, True, "illisible")
        # C10 — le relevé des signaux rangé dans archives/ : son absence se dit, sans trace Python (D1, 11-11-2026)
        c = copie_reduite(racine, d)
        p = releve_de(c, SIGNAUX, entete)
        if p is not None:
            os.makedirs(os.path.join(c, "archives"), exist_ok=True)
            os.rename(p, os.path.join(c, "archives", os.path.basename(p)))
        try:
            if releve_de(c, SIGNAUX, entete) is not None:
                faux.append("C10 un relevé rangé dans archives/ est encore trouvé")
        except Exception as e:   # noqa: BLE001 — l'absence doit être une réponse, pas une exception
            faux.append(f"C10 l'absence d'un relevé lève {type(e).__name__} au lieu d'être dite")
        cas("C10 relevé rangé dans archives/", c, False)
        # C11 — le lot de la boucle changé dans la table : il n'est plus celui du relevé (L2, 11-11-2026)
        c = copie_reduite(racine, d)
        t = table_de(c)
        t["series_hors_de_la_nuit"][BOUCLE]["serie_du_circuit"]["lot"] += 1
        ecrire_table(c, t)
        cas("C11 lot de la table différent du relevé", c, True, "lot du relevé")
        # C12 — l'en-tête d'un relevé sans sa taille de lot : illisible, jamais vert (cas qui doit échouer du motif)
        c = copie_reduite(racine, d)
        p = releve_de(c, BOUCLE, entete)
        if p is None:
            faux.append(f"C12 aucun relevé ne nomme {BOUCLE}")
        else:
            texte = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(TAILLE_DE_LOT.sub("des lots", texte))
            cas("C12 taille de lot absente de l'en-tête", c, True, "taille de lot illisible")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


# LES SABOTAGES — chacun retire ce qu'un cas éprouve, dans une copie de CE fichier (cible, remplacement).
SABOTAGES = {
    "S1_releves_ignores": [("            if tete[0] != entete:\n                continue",
                            "            if True:\n                continue")],
    "S2_releve_reconnu_par_son_nom": [("            if tete[0] != entete:\n",
                                       "            if not os.path.basename(chemin).startswith(\"SERIE_DE_SABOTAGES_\"):\n")],
    "S3_table_hors_de_la_nuit_ignoree": [("    for epreuve in hors:\n        longues.setdefault(epreuve, []).append(\"table\")",
                                          "    pass")],
    "S4_presence_dans_la_table_suffit": [("        elif epreuve not in circuit:",
                                          "        elif epreuve not in json.load(open(os.path.join(racine, TABLE), encoding=\"utf-8\"))[\"series_hors_de_la_nuit\"]:")],
    "S5_refus_du_fabricant_avale": [("        return defauts + [f\"le fabricant refuse la table, aucune série ne peut partir : {e}\"]",
                                     "        return defauts")],
    "S6_epreuve_absente_admise": [("        if not os.path.isfile(os.path.join(racine, epreuve)):",
                                   "        if False:")],
    "S8_releve_absent_leve": [("                 if open(p, encoding=\"utf-8\", errors=\"replace\").read().split(\"\\n\")[:2] == [entete, LIGNE_EPREUVE + epreuve]),\n                None)",
                               "                 if open(p, encoding=\"utf-8\", errors=\"replace\").read().split(\"\\n\")[:2] == [entete, LIGNE_EPREUVE + epreuve]))")],
    "S9_lot_non_compare": [("        elif lot != lot_de[epreuve]:", "        elif False:")],
    "S10_lot_illisible_admis": [("        if lot is None:\n", "        if False:\n")],
    "S7_releve_illisible_admis": [("            if not tete[1].startswith(LIGNE_EPREUVE):\n                illisibles.append(rel)\n",
                                   "            if not tete[1].startswith(LIGNE_EPREUVE):\n")],
}


def saboter(racine):
    """Joue chaque sabotage sur une copie de ce fichier ; rend le code de sortie.

    ① RÔLE — Prouver que chaque cas mord (R-731).
    ② CONTEXTE D'APPEL — `main`, avec --saboter.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Chaque cible existe une fois dans ce fichier, avant la table SABOTAGES.
    ⑤ SORTIE — UNE valeur : 0 si Z0 est vert et chaque sabotage rougit ; 1 sinon ; 2 si une cible manque. [rend: 1]
    ⑥ TRAITEMENT — Z0 d'abord (`eprouver`) ; puis, par sabotage : copie de ce fichier, remplacement, lancement sur la
      racine (120 s au plus) ; « <nom> mord : [cas faux] » si le code est 1.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve.
    ⑨ CE QUI CLOCHE — Les sabotages portent sur le contrôle de CE fichier, non sur la table : la table se sabote par
      les cas C1, C6, C7, C8.
    ⑩ EFFET — Écrit des copies jetables.
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 s. [sort: non]
    """
    faux = eprouver(racine)
    print("Z0 programme tel quel : " + ("; ".join(faux) if faux else "C0 à C12 conformes"))
    code = 1 if faux else 0
    source = open(os.path.abspath(__file__), encoding="utf-8").read()
    # les cibles se cherchent AVANT la table des sabotages : la table porte le texte de ses propres cibles
    coupe = source.index("\n# LES SABOTAGES")
    tete, queue = source[:coupe], source[coupe:]
    d = tempfile.mkdtemp(prefix="series_longues_E_sab_")
    try:
        for nom, remplacements in SABOTAGES.items():
            texte = tete
            for a, b in remplacements:
                if texte.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : cible trouvée {texte.count(a)} fois")
                    code = max(code, 2)
                    break
                texte = texte.replace(a, b)
            else:
                p = os.path.join(d, nom + ".py")
                open(p, "w", encoding="utf-8").write(texte + queue)
                r = subprocess.run([sys.executable, "-B", p, racine], capture_output=True, text=True, timeout=120)
                cases = [l for l in r.stdout.splitlines() if l.startswith("FAUX ")]
                if r.returncode == 1:
                    print(f"{nom} mord : {[l[5:].split(' : ')[0] for l in cases]}")
                else:
                    print(f"{nom} NE MORD PAS (code {r.returncode})")
                    code = max(code, 1)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return code


def recenser(racine):
    """Imprime le recensement des séries longues et des longs lancements « --saboter » de la nuit ; rend 0 ou 1.

    ① RÔLE — Recenser par programme (plan V7, bloc 2bis, action 1).
    ② CONTEXTE D'APPEL — `main`, avec --recenser.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 1 si une série longue est sans ligne (ou modules illisibles), 0 sinon. [rend: 1]
    ⑥ TRAITEMENT — séries longues (`series_longues`) avec leur ligne au circuit (code, machines, lot) et l'en-tête
      « série jouée … » de leur relevé ; puis les délais de la table au-delà de SEUIL_LONG.
    ⑦ UNITÉ — Des secondes pour les délais.
    ⑧ POURQUOI — Montrer le recensement, pas le dire.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Imprime.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    entete, circuit = modules(racine)
    lignes = {e: (c, n, l) for c, e, n, l in circuit(racine)}
    longues, _ = series_longues(racine, entete)
    for epreuve, sources in sorted(longues.items()):
        print(f"SÉRIE LONGUE {epreuve}")
        print(f"  ligne au circuit : {lignes.get(epreuve, 'AUCUNE')}")
        for s in sources:
            if s.startswith("relevé "):
                tete = open(os.path.join(racine, s[7:]), encoding="utf-8").read().split("\n")[:5]
                print(f"  {s} : {' '.join(x[2:] for x in tete[2:4])}")
            else:
                print(f"  {s}")
    table = json.load(open(os.path.join(racine, TABLE), encoding="utf-8"))
    for cle, e in sorted((table.get("delais") or {}).items()):
        if e.get("secondes", 0) > SEUIL_LONG:
            print(f"DÉLAI LONG DE LA NUIT {e['secondes']} s : {cle}")
    defauts = series_sans_ligne(racine, entete, circuit)
    for x in defauts:
        print("FAUX " + x)
    return 1 if defauts else 0


def main():
    """Lit la ligne de commande et sort avec le code dit en tête.

    ① RÔLE — Point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande (la certification passe la racine en premier argument, puis « --saboter »).
    ③ ENTRÉE — <racine> [--saboter | --recenser].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur : sys.exit avec le code de la fiche en tête. [rend: 0]
    ⑥ TRAITEMENT — `saboter`, `recenser` ou `eprouver`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Imprime.
    ⑪ TERMINAISON — Ne revient pas : sys.exit. [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    racine = os.path.abspath(args[0] if args else ".")
    if "--saboter" in sys.argv[1:]:
        sys.exit(saboter(racine))
    if "--recenser" in sys.argv[1:]:
        sys.exit(recenser(racine))
    faux = eprouver(racine)
    for x in faux:
        print("FAUX " + x)
    print("Z0 programme tel quel : " + ("NON CONFORME" if faux else "C0 à C12 conformes"))
    print("VERDICT : " + ("NON CONFORME" if faux else "tout est conforme"))
    sys.exit(1 if faux else 0)


if __name__ == "__main__":
    main()
