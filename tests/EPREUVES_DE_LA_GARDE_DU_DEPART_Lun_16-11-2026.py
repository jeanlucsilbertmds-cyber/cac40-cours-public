#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_GARDE_DU_DEPART — Lun 16-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Une seule propriété : LE RASSEMBLEUR DES PARTS (tests/outils/rassembler_les_parts.py) ACCEPTE DES
PARTS DONT LES etat_du_depart.json DISENT LA MÊME CHOSE, ET REFUSE, EN CODE 2 ET SANS TRACE PYTHON, DES PARTS DONT LES
DÉPARTS DIFFÈRENT OU NE SE LISENT PAS COMME UN ÉTAT DU DÉPÔT. Faits : la série de sabotages HL jouée sur GitHub (passage
43913791964, 16-11-2026) a échoué au rassemblement alors que ses 18 parts étaient parties du même dépôt — leurs 18
etat_du_depart.json portent les mêmes 6 856 empreintes, mais pas dans le même ordre (le dictionnaire est rempli dans
l'ordre de os.walk, qui n'est pas garanti), et la garde ④ du rassembleur comparait les OCTETS des fichiers. Le
superviseur R-759 du 16-11-2026 (« DE FOND ») demande de comparer les CONTENUS (une propriété, pas une forme
d'écriture), en restant strict (égalité complète, clés en plus comprises), et d'éprouver la garde, qu'aucune épreuve
ne jouait (cherché dans tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py et
tests/EPREUVES_DU_CIRCUIT_DES_SERIES_Jeu_05-11-2026.py). Son rapport brut : etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/
rapports_du_11-11-2026/SUPERVISEUR_ETAT_DU_DEPART_Lun_16-11-2026.md.

① RÔLE — Éprouver, au dépôt, la garde ④ du rassembleur (« même départ partout ») de bout en bout : le VRAI programme,
  lancé en ligne de commande sur des parts posées sur le disque.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine, puis avec --saboter) ;
  à la main avant toute livraison qui touche le rassembleur, jouer_une_part.py ou le départ écrit par le joueur
  (R-731 : tout code écrit ou modifié est relu et éprouvé) :
  python3 tests/EPREUVES_DE_LA_GARDE_DU_DEPART_Lun_16-11-2026.py <racine> [--saboter | --saboter=S1,S2,…]
③ ENTRÉE — La racine d'un dépôt : on y prend tests/outils/ (le rassembleur, jouer_une_part.py, le joueur),
  programmes/*.py (le joueur les importe) et les deux témoins réels tests/temoins_etat_du_depart/ (R-732 : une copie
  RÉDUITE à 12 clés des etat_du_depart.json des parts 0 et 9 de la série HL du passage 43913791964, branches
  series-longues/43913791964/HL/part_0 et part_9 du dépôt privé ; mêmes 12 clés, chacune dans l'ordre d'origine de
  son fichier : contenus égaux, octets différents).
④ CONDITIONS D'ENTRÉE — Aucun réseau. python3.
⑤ SORTIE — Le code de sortie : 0 si chaque cas (E0 à E17) donne la réponse attendue et, avec --saboter, si chaque
  sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus ou si un sabotage demandé
  par « --saboter=… » n'existe pas.
  [rend: 1]
⑥ TRAITEMENT — Un dépôt d'essai minuscule (`depot_d_essai`) : les trois outils et programmes/*.py copiés de la
  racine, une épreuve tests/EPR.py à deux sabotages. Pour chaque cas, deux parts (trois pour E15) posées par
  `poser_les_parts` (manifeste part.json accordé, part 0 avec son lot 1 joué et ses flux d'écoute qui nomment
  l'épreuve, les autres parts sans lot), chacune avec le etat_du_depart.json du cas, AUCUNE avec sa place libre minimale ; puis le rassembleur lancé.
  Comme aucune part ne porte sa place, un rassemblement qui PASSE la garde ④ s'arrête à la garde suivante, ④bis
  (« place libre minimale ») : c'est ce qui se lit. « passe » = code 2, aucune trace Python, un ARRET de ④bis et
  aucun ARRET qui nomme etat_du_depart.json ; « refusé » = code 2, aucune trace Python, un ARRET qui nomme
  etat_du_depart.json et porte le fragment de SA raison.
  E0 (témoin) le même fichier réel dans les deux parts → passe (sans lui, un harnais cassé ferait tout « refuser »)
  · E1 (le cas du 16-11-2026, R-732) part 0 et part 9 réelles réduites : mêmes contenus, autre ordre → passe ;
  rouge sur le code d'avant la réparation · E2 une valeur différente → refusé · E3 une clé en plus dans la seule
  part 1 → refusé · E4 une clé en moins dans la seule part 1 → refusé · E5 une clé en double, dans les deux parts
  (json.load garderait la dernière, et les deux parts seraient égales) → refusé · E6 une valeur entière → refusé ·
  E7 une valeur de 64 caractères non hexadécimaux → refusé · E8 une valeur de 63 caractères hexadécimaux → refusé
  · E9 une liste non vide (des empreintes) au lieu d'un dictionnaire, dans les deux parts → refusé · E10 un dictionnaire vide dans les deux
  parts → refusé · E11 le fichier absent de la part 1 → refusé · E12 un JSON tronqué dans la part 1 → refusé ·
  E13 des octets qui ne sont pas de l'UTF-8 dans la part 1 → refusé · E14 une valeur en majuscules hexadécimales
  dans les deux parts → refusé (le joueur écrit hexdigest, en minuscules) · E15 TROIS parts, seule la troisième
  diffère (une valeur) → refusé (la série réelle a 18 parts : une garde qui ne comparerait que la deuxième part
  laisserait passer un désaccord en part 3 et au-delà — relecture du 16-11-2026, M1) · E16 une valeur de 65
  caractères hexadécimaux dans les deux parts → refusé (une empreinte trop longue dont les 64 premiers caractères
  conviennent : relecture du 16-11-2026, M2) · E17 un JSON imbriqué 100 000 fois (« [ » répété) dans la part 1 →
  refusé, sans trace (RecursionError au décodeur : relecture du 16-11-2026, M3).
  Avec --saboter, le rassembleur de la copie d'essai est réécrit par chaque sabotage de SABOTAGES et tous les cas
  sont rejoués : chacun doit faire tomber au moins un cas.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Superviseur R-759 du 16-11-2026, points 2, 3, 5 et 7 (rapport brut cité en tête).
⑨ CE QUI CLOCHE — Le passage de la garde ④ se lit à l'arrêt de la garde ④bis : si l'ordre des gardes changeait,
  E0 rougirait (c'est voulu, et cela se lit). Les témoins réels sont RÉDUITS (12 clés sur 6 856) : la mesure sur les
  fichiers entiers a été faite une fois, à la main, le 16-11-2026 (echanges/A_RELIRE.md de la branche
  travail-etat-depart). Le joueur et jouer_une_part.py, qui relisent aussi le départ, ne sont pas joués ici.
⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 secondes ; sort par sys.exit.
  [sort: oui]
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0]) if _args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RASSEMBLEUR = "tests/outils/rassembler_les_parts.py"
OUTILS = ("tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py", "tests/outils/jouer_une_part.py", RASSEMBLEUR)
TEMOINS = "tests/temoins_etat_du_depart"
REEL_0 = os.path.join(TEMOINS, "HL_43913791964_part_0_etat_du_depart_reduit.json")
REEL_9 = os.path.join(TEMOINS, "HL_43913791964_part_9_etat_du_depart_reduit.json")
EPR = 'SABOTAGES = {"A1": 1, "A2": 2}\nprint("Z0 programme tel quel : tous les cas conformes")\n'
REL = "tests/resultats/SERIE_DE_SABOTAGES_DE_L_ESSAI_Lun_16-11-2026_14h00.txt"
NOM = "etat_du_depart.json"

# Chaque sabotage : (fichier, texte présent une fois, texte qui le remplace). Les deux premiers sont ceux que le
# superviseur R-759 du 16-11-2026 exige (point 7) ; les suivants retirent, un par un, ce que la réparation ajoute.
SABOTAGES = {
    "S1_comparaison_des_octets_remise": [
        (RASSEMBLEUR, "        if etat != premier:\n",
         "        if open(os.path.join(d, NOM_DU_DEPART), \"rb\").read() != "
         "open(os.path.join(dossiers[0], NOM_DU_DEPART), \"rb\").read():\n")],
    "S2_cles_du_premier_seulement": [
        (RASSEMBLEUR, "        if etat != premier:\n",
         "        if any(etat.get(c) != v for c, v in premier.items()):\n")],
    "S3_doublons_admis": [(RASSEMBLEUR, "object_pairs_hook=sans_doublon", "object_pairs_hook=dict")],
    "S4_valeurs_non_controlees": [
        (RASSEMBLEUR, "        if not isinstance(v, str) or not EMPREINTE.fullmatch(v):\n", "        if False:\n")],
    "S5_dictionnaire_non_exige": [(RASSEMBLEUR, "    if not isinstance(etat, dict):\n", "    if False:\n")],
    "S6_depart_vide_admis": [(RASSEMBLEUR, "    if not etat:\n", "    if False:\n")],
    "S7_fichier_absent_non_rattrape": [(RASSEMBLEUR, "    except (OSError, ValueError, RecursionError) as e:\n",
                                        "    except (ValueError, RecursionError) as e:\n")],
    # Relecture du 16-11-2026, M1 à M3 : trois trous que les sabotages S1 à S7 ne voyaient pas.
    "S8_seule_la_deuxieme_part_comparee": [(RASSEMBLEUR, "zip(dossiers[1:], lus[1:])", "zip(dossiers[1:2], lus[1:2])")],
    "S9_fullmatch_en_match": [(RASSEMBLEUR, "EMPREINTE.fullmatch(v)", "EMPREINTE.match(v)")],
    "S10_recursion_non_rattrapee": [(RASSEMBLEUR, "    except (OSError, ValueError, RecursionError) as e:\n",
                                     "    except (OSError, ValueError) as e:\n")],
}


def lancer(args):
    """Lance une commande ; rend (code, sortie et erreur réunies).

    ① RÔLE — Un lancement borné.
    ② CONTEXTE D'APPEL — `jouer_un_cas`.
    ③ ENTRÉE — `args` : la commande.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (code, texte). [rend: 1]
    ⑥ TRAITEMENT — subprocess.run, borné à 300 s.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired, qui fait sortir l'épreuve sur une trace (code non nul).
    ⑩ EFFET — Ce que fait la commande.
    ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return p.returncode, p.stdout + p.stderr


def depot_d_essai(d, remplacements):
    """Fabrique le dépôt d'essai ; rend son chemin, ou None si un remplacement ne s'applique pas.

    ① RÔLE — Un dépôt minuscule où le rassembleur tourne en une seconde.
    ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `d` : le dossier jetable ; `remplacements` : la liste (fichier, a, b) d'un sabotage, ou [].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin, ou None. [rend: 1]
    ⑥ TRAITEMENT — programmes/*.py et les trois outils copiés de DEPOT ; tests/EPR.py ; chaque remplacement appliqué
      s'il trouve son texte exactement une fois.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le rassembleur charge le joueur, qui importe programmes/ ; et il compare les sabotages de l'épreuve
      de la racine à ceux des manifestes.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    r = os.path.join(d, "racine")
    os.makedirs(os.path.join(r, "programmes"))
    for f in os.listdir(os.path.join(DEPOT, "programmes")):
        if f.endswith(".py"):
            shutil.copyfile(os.path.join(DEPOT, "programmes", f), os.path.join(r, "programmes", f))
    for o in OUTILS:
        os.makedirs(os.path.dirname(os.path.join(r, o)), exist_ok=True)
        shutil.copyfile(os.path.join(DEPOT, o), os.path.join(r, o))
    with open(os.path.join(r, "tests", "EPR.py"), "w", encoding="utf-8") as f:
        f.write(EPR)
    for fichier, a, b in remplacements:
        t = open(os.path.join(r, fichier), encoding="utf-8").read()
        if t.count(a) != 1:
            print(f"le texte visé est trouvé {t.count(a)} fois dans {fichier} : {a.strip()[:80]}")
            return None
        open(os.path.join(r, fichier), "w", encoding="utf-8").write(t.replace(a, b))
    return r


def poser_les_parts(depuis, departs):
    """Pose une part par départ donné sous `depuis`, chacune avec le etat_du_depart.json donné.

    ① RÔLE — Des parts qui passent toutes les gardes du rassembleur avant ④, et n'ont pas leur place (④bis).
    ② CONTEXTE D'APPEL — `jouer_un_cas`.
    ③ ENTRÉE — `depuis` : le dossier des parts ; `departs` : une valeur par part (deux ou trois), les octets du départ
      de chaque part, ou None pour une part sans départ.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune. [rend: 0]
    ⑥ TRAITEMENT — part.json (épreuve tests/EPR.py, relevé REL, lot de 10, autant de parts que de départs, sabotages
      A1 et A2, lots de lots_de_la_part : [1] pour la part 0, [] pour les autres, codes, racine fictive « /ailleurs/racine », 1 à la fois) ; pour la part 0,
      lot_01.out, lot_01.code « 0 » et un fichier par flux d'écoute qui nomme /ailleurs/racine/tests/EPR.py ; debut.txt.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les gardes ① à ③bis du rassembleur doivent passer pour que ④ soit jouée.
    ⑨ CE QUI CLOCHE — Les noms des flux (« ecoute », « execution ») sont écrits ici : si le joueur en ajoute un, E0
      rougit (« flux d'écoute … manque »), ce qui se lit.
    ⑩ EFFET — Écrit sous `depuis`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    for i, depart in enumerate(departs):
        p = os.path.join(depuis, f"p{i}")
        os.makedirs(p)
        lots = [1] if i == 0 else []
        json.dump({"epreuve": "tests/EPR.py", "releve": REL, "lot": 10, "nb_parts": len(departs), "noms": ["A1", "A2"],
                   "part": i, "lots": lots, "codes": {str(k): 0 for k in lots}, "racine": "/ailleurs/racine",
                   "parallele": 1}, open(os.path.join(p, "part.json"), "w", encoding="utf-8"))
        for k in lots:
            open(os.path.join(p, f"lot_{k:02d}.out"), "w").write("Z0 programme tel quel : tous les cas conformes\n")
            open(os.path.join(p, f"lot_{k:02d}.code"), "w").write("0\n")
        for flux in ("ecoute", "execution"):
            os.makedirs(os.path.join(p, flux))
            if lots:
                open(os.path.join(p, flux, "lus.1"), "w").write("/ailleurs/racine/tests/EPR.py\n")
        open(os.path.join(p, "debut.txt"), "w").write("16-11-2026 14h00")
        if depart is not None:
            open(os.path.join(p, NOM), "wb").write(depart)


def les_cas(depot):
    """Rend les cas : liste de (nom, liste des octets du départ de chaque part, None si « passe » ou le fragment
    attendu dans le refus).

    ① RÔLE — Les cas E0 à E17 de la fiche en tête, en un endroit.
    ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `depot` : la racine éprouvée, où vivent les témoins réels.
    ④ CONDITIONS D'ENTRÉE — Les deux témoins se lisent.
    ⑤ SORTIE — UNE valeur : la liste. [rend: 1]
    ⑥ TRAITEMENT — les témoins lus en octets ; les cas fabriqués partent du contenu du témoin de la part 0.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ⑥.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit deux fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève si un témoin manque. [sort: non]
    """
    r0 = open(os.path.join(depot, REEL_0), "rb").read()
    r9 = open(os.path.join(depot, REEL_9), "rb").read()
    base = json.loads(r0)
    premiere = next(iter(base))

    def octets(valeur):
        """Rend `valeur` écrite en JSON, en octets UTF-8, comme json.dump du joueur (séparateurs par défaut).

        ① RÔLE — Fabriquer un départ. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `valeur`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : les octets. [rend: 1] ⑥ TRAITEMENT — json.dumps, encode. ⑦ UNITÉ — —
        ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
        """
        return json.dumps(valeur).encode("utf-8")

    double = r0.decode("utf-8").rstrip()[:-1] + f', "{premiere}": "{"0" * 64}"}}'
    return [
        ("E0 même fichier réel dans les deux parts", [r0, r0], None),
        ("E1 parts 0 et 9 réelles (HL 43913791964) : mêmes contenus, autre ordre", [r0, r9], None),
        ("E2 une valeur différente", [r0, octets(dict(base, **{premiere: "0" * 64}))], "pas parties du même état"),
        ("E3 une clé en plus dans la part 1 seule", [r0, octets(dict(base, **{"fichier_en_plus.txt": "f" * 64}))],
         "pas parties du même état"),
        ("E4 une clé en moins dans la part 1 seule", [r0, octets({c: v for c, v in base.items() if c != premiere})],
         "pas parties du même état"),
        ("E5 une clé en double dans les deux parts", [double.encode("utf-8"), double.encode("utf-8")], "deux fois"),
        ("E6 une valeur entière", [octets(dict(base, **{premiere: 12345})),
                                   octets(dict(base, **{premiere: 12345}))], "empreinte"),
        ("E7 une valeur de 64 caractères non hexadécimaux", [octets(dict(base, **{premiere: "z" * 64})),
                                                             octets(dict(base, **{premiere: "z" * 64}))], "empreinte"),
        ("E8 une valeur de 63 caractères hexadécimaux", [octets(dict(base, **{premiere: "a" * 63})),
                                                         octets(dict(base, **{premiere: "a" * 63}))], "empreinte"),
        ("E9 une liste non vide dans les deux parts", [octets(list(base.values())), octets(list(base.values()))],
         "pas un dictionnaire"),
        ("E10 un dictionnaire vide dans les deux parts", [b"{}", b"{}"], "vide"),
        ("E11 le fichier absent de la part 1", [r0, None], "illisible"),
        ("E12 un JSON tronqué dans la part 1", [r0, r0[:len(r0) // 2]], "illisible"),
        ("E13 des octets non UTF-8 dans la part 1", [r0, b"\xff\xfe{}"], "illisible"),
        ("E14 une valeur en majuscules hexadécimales", [octets(dict(base, **{premiere: "A" * 64})),
                                                        octets(dict(base, **{premiere: "A" * 64}))], "empreinte"),
        # Le refus doit nommer la TROISIÈME part (dossier « p2 ») : la phrase dit « le etat_du_depart.json de <dossier>
        # diffère de celui de … ».
        ("E15 trois parts, seule la troisième diffère", [r0, r9, octets(dict(base, **{premiere: "0" * 64}))],
         os.sep + "p2 diffère"),
        ("E16 une valeur de 65 caractères hexadécimaux", [octets(dict(base, **{premiere: "a" * 65})),
                                                          octets(dict(base, **{premiere: "a" * 65}))], "empreinte"),
        ("E17 un JSON imbriqué 100 000 fois dans la part 1", [r0, b"[" * 100000], "illisible : RecursionError"),
    ]


def jouer_un_cas(racine, d, nom, departs, attendu):
    """Joue un cas ; rend None s'il donne la réponse attendue, sinon la phrase qui dit l'écart.

    ① RÔLE — Un rassemblement, jugé.
    ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `racine` : le dépôt d'essai ; `d` : le dossier jetable ; `nom` ; `departs` : les octets du départ de
      chaque part (ou None) ; `attendu` : None (« passe ») ou le fragment de la raison du refus.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None ou une phrase. [rend: 1]
    ⑥ TRAITEMENT — `poser_les_parts` dans un dossier neuf ; le rassembleur lancé avec --depuis et un --travail neuf ;
      lecture du code, des lignes ARRET et de la présence d'une trace Python (« Traceback »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ⑥ : « passe » se lit à l'arrêt de la garde ④bis.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main ; le lancement est borné à 300 s. [sort: non]
    """
    cas = os.path.join(d, nom.split()[0])
    poser_les_parts(os.path.join(cas, "parts"), departs)
    code, sortie = lancer([sys.executable, "-B", os.path.join(racine, RASSEMBLEUR), racine, "tests/EPR.py", REL,
                           f"--depuis={os.path.join(cas, 'parts')}", f"--travail={os.path.join(cas, 'travail')}"])
    arrets = [l for l in sortie.splitlines() if l.startswith("ARRET ")]
    au_depart = [l for l in arrets if NOM in l]
    trace = "Traceback" in sortie
    if attendu is None:
        bon = (code == 2 and not trace and not au_depart and len(arrets) == 1
               and "place libre minimale" in arrets[0])
    else:
        bon = code == 2 and not trace and len(au_depart) == 1 and attendu in au_depart[0]
    if bon:
        return None
    return (f"{nom} : attendu {'passe' if attendu is None else 'refusé pour « ' + attendu + ' »'} ; code {code}, "
            f"trace {'oui' if trace else 'non'}, arrêts {[a[:160] for a in arrets]}")


def tour(remplacements):
    """Joue tous les cas sur un dépôt d'essai ; rend (la liste des écarts, ou None si un sabotage ne s'applique plus).

    ① RÔLE — Un tour complet.
    ② CONTEXTE D'APPEL — `main` : une fois tel quel, une fois par sabotage.
    ③ ENTRÉE — `remplacements` : ceux d'un sabotage, ou [].
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts (vide si tout est conforme), ou None. [rend: 1]
    ⑥ TRAITEMENT — `depot_d_essai`, puis `jouer_un_cas` pour chaque cas de `les_cas`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="garde_du_depart_")
    try:
        racine = depot_d_essai(d, remplacements)
        if racine is None:
            return None
        faux = []
        for nom, departs, attendu in les_cas(DEPOT):
            e = jouer_un_cas(racine, d, nom, departs, attendu)
            if e:
                faux.append(e)
        return faux
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter, un tour par sabotage (ou par sabotage nommé dans
      « --saboter=S1,S2,… »), chacun devant faire tomber au moins un cas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour([])
    print("Z0 programme tel quel : " + ("E0 à E17 conformes" if not faux else "FAUX\n  " + "\n  ".join(faux)),
          flush=True)
    code = 1 if faux else 0
    choix = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--saboter=")]
    if "--saboter" in sys.argv[1:] or choix:
        noms = choix[0].split(",") if choix else list(SABOTAGES)
        inconnus = [n for n in noms if n not in SABOTAGES]
        if inconnus:
            print(f"ARRET sabotage(s) inconnu(s) : {inconnus}")
            return 2
        for nom in noms:
            f = tour(SABOTAGES[nom])
            if f is None:
                print(f"{nom} NE S'APPLIQUE PLUS")
                return 2
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {[e.split(' : ')[0] for e in f]}", flush=True)
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
