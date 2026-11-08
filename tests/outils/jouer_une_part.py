#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jouer_une_part — Mer 04-11-2026 (Paris), tour 3 après l'avis du superviseur R-759 du 04-11-2026 à 19h59 ; réparé
le Jeu 05-11-2026 pour la version B (étude github_series/RAPPORT.md). Simulation uniquement.

① RÔLE — Jouer UNE PART d'une série de sabotages : les lots qui reviennent à cette part quand la série est
  partagée entre plusieurs machines, chacun joué exactement comme le ferait tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py
  (même découpage en lots, même écoute des fichiers lus, même environnement git). La part n'écrit PAS de relevé :
  elle laisse un dossier de travail que rassembler_les_parts.py réunit aux autres parts.
② CONTEXTE D'APPEL — Un job de la matrice du circuit public .github/workflows/series_longues.yml (fabriqué par
  programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py), une fois par part :
  python3 -B -u jouer_une_part.py <racine> <épreuve> <relevé> --part=I --nb-parts=N --lot=L [--parallele=2]
  --travail=<dossier neuf>   (`épreuve` et `relevé` relatifs à la racine). Aussi à la main, pour l'essai local.
  Et `python3 -B jouer_une_part.py --interdits` : écrit les noms des programmes interdits, un par ligne (le circuit
  les retire de la copie et refuse de les choisir comme épreuve, sans les épeler lui-même).
③ ENTRÉE — La racine d'un dépôt (une copie jetable, jamais le dépôt où l'on travaille : l'épreuve y écrit) ;
  l'épreuve, qui doit porter un dictionnaire SABOTAGES et accepter « --saboter=S1,S2,… » ; le nom du relevé final
  (il n'est pas écrit ici, il est seulement écarté de l'empreinte du départ, comme le fait le joueur) ; le numéro
  de la part I (0 à N-1), le nombre de parts N, la taille d'un lot, le nombre de lots joués en même temps.
④ CONDITIONS D'ENTRÉE — La racine porte tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py et programmes/ (le joueur les
  importe) ; elle ne porte AUCUN fichier nommé comme un programme d'INTERDITS (le circuit les retire de sa copie).
  0 <= I < N. Le dossier de travail n'existe pas, ou ne contient que ce qu'une part précédente de MÊME
  numéro y a laissé (les lots finis sont gardés, comme la reprise du joueur).
⑤ SORTIE — UNE valeur : le code de sortie. 0 : la part est COMPLÈTE — tous ses lots ont été joués, aucun programme
  interdit n'a été lu, la racine n'a pas changé, le manifeste part.json est écrit ; un lot qui a rendu autre chose
  que 0 est écrit dans son .code et dans le manifeste, et c'est le relevé qui le dira (« lots rouges », NON
  CONFORME). 2 : rien de sûr (arguments faux, épreuve illisible ou interdite, programme interdit présent dans la
  racine ou lu pendant la part, écoute absente ou SOURDE — un lot dont un flux d'écoute ne nomme pas l'épreuve, ou
  une part qui a joué sans qu'un flux ne la nomme —, la racine a changé pendant la part, toute erreur imprévue) —
  pas de manifeste, le job rougit, et le rassemblement refuse toute la série. Le code 1 n'est jamais rendu (garde
  générale de `__main__`, tour 3). Un lot dont la sortie porte une trace d'erreur système (disque plein…) ne fait
  pas rougir la part : le joueur, au rassemblement, rend la série NON CONFORME ; la part le dit à l'écran et note
  la place libre du disque au début, à la fin et AU PLUS BAS PENDANT LES LOTS dans part.json (« place_libre_mo ») ;
  chaque lot compté laisse sa place dans « lot_NN.place », écrite avant « lot_NN.code » (`jouer_un_lot` du joueur,
  tour 3, B-2), que le rassemblement exige et que le joueur juge contre son plancher (superviseur R-759 du
  05-11-2026, M1 (2)). Une part dont le dossier temporaire n'est pas sur le disque du dossier de travail est
  refusée (2) avant tout lot (`refus_du_disque_temporaire` du joueur, tour 3, M-1).
⑥ TRAITEMENT — ⓪ refuser une épreuve interdite, et une racine qui porte un programme interdit (`interdits_presents`)
  · ① charger le joueur depuis la racine · ② lire les noms des sabotages (SERIES_DE_SABOTAGES,
  par le joueur) et découper en lots de `lot` (`decouper` du joueur) · ③ garder les lots k tels que
  (k-1) mod N == I (tour de rôle : les lots voisins, souvent de durée voisine, vont à des machines différentes) ·
  ④ préparer le dossier de travail par `preparer_le_travail` du joueur (module d'écoute et un dossier par flux),
  écrire l'empreinte du départ (`etat_du_depot` du joueur, sans le relevé), l'heure du début, la place libre ·
  ⑤ jouer chaque lot par `jouer_un_lot` du joueur, `parallele` à la fois, sous `surveiller_la_place` du joueur · ⑥ reprendre
  l'empreinte de la racine : un fichier présent au départ qui a changé ou disparu → 2 · ⑤bis un lot SOURD (le
  joueur rend None pour son code : un flux de son processus ne nomme pas l'épreuve) → 2 · ⑥bis relire chaque flux
  de l'écoute (FLUX_D_ECOUTE du joueur) : un programme interdit nommé, un flux absent, ou une part qui a joué des
  lots sans qu'un flux ne nomme l'épreuve (`ecoute_nomme`) → 2 · ⑦ écrire part.json, avec la place libre ; dire à
  l'écran les lots dont la sortie porte une trace d'erreur système (`trace_d_erreur_systeme` du joueur).
⑦ UNITÉ — Heures de Paris (« JJ-MM-AAAA HHhMM ») dans debut.txt, comme le joueur.
⑧ POURQUOI — Décision à prendre par Jean-Luc (circuit préparé le 04-11-2026, non poussé) : les séries HL et Yahoo
  durent 3,9 à 5,1 h sur la machine du Chat (2 processeurs) ; GitHub peut jouer plusieurs machines en même temps.
  Le joueur ne sait partager une série qu'entre les processeurs d'UNE machine (`--parts`) : cette part réutilise ses
  fonctions au lieu de les réécrire (deux rédactions d'une même chose divergent toujours, R-708).
  Tour 2 (relecture du 04-11-2026, défaut IMPORTANT D1) : une part qui avait lu un programme interdit donnait quand
  même un relevé « conforme ». Le rassemblement exige désormais que TOUTES les parts soient vertes ; une part ne
  rougit donc plus pour un lot rouge (sinon aucune série NON CONFORME n'aurait jamais de relevé), elle rougit
  seulement quand elle n'est pas sûre. Le contrôle des programmes interdits vit ICI (et dans le rassemblement),
  plus dans le .yml : la relecture a montré que le pas du .yml passait en silence sans écoute (D4).
  Tour 3 (relecture du 04-11-2026 à 19h53, I2 ; superviseur R-759 du 04-11-2026, R2) : une écoute VIDE passait pour
  une écoute valable (part en code 0, relevé « conforme » à 1 empreinte au lieu de 9). Réparé à la source, dans
  `jouer_un_lot` du joueur (patch joint), ET ici par `ecoute_nomme`, qui tient même si le joueur de la racine est
  encore l'ancien. L'épreuve est le seul fichier que tout lot lit : Python ouvre le programme qu'il lance.
  05-11-2026 (étude github_series/RAPPORT.md, §1.3, mesuré) : la version B du joueur fait écrire à l'écoute un
  second flux, dans un dossier « execution » ; cette part recopiait la préparation du dossier de travail et ne le
  créait pas : le module d'écoute plantait au démarrage, 0 ligne lue, code 0. La préparation, le découpage et les
  flux sont désormais ceux du joueur, appelés et non recopiés (R-708). Disque : un disque plein a donné un faux
  « mord » (series_A, essai 1) ; le disque d'une machine GitHub est de 14 Go (documentation lue le 05-11-2026), et
  un lot de l'historique long laisse environ 2,4 Go : la place libre est notée pour le mesurer.
⑨ CE QUI CLOCHE — L'empreinte du départ et l'heure du début sont encore écrites ici comme dans `main` du joueur
  (elles n'y vivent pas dans une fonction) ; un écart se voit au rassemblement (le joueur compare le départ). ·
  La vérification ⑥ porte sur TOUT fichier présent au départ (le joueur, lui, ne revérifie à la fin
  que les fichiers lus) : plus stricte, elle pourrait refuser une part dont l'épreuve réécrit un fichier qu'elle ne
  lit pas — jamais vu sur l'essai local (série BNAINS). · Un programme lancé avec « -I » ou « -E » par l'épreuve
  n'est pas écouté (même défaut que le joueur, fiche ⑨ du joueur) : pour les programmes INTERDITS, ce trou est
  fermé par leur ABSENCE de la racine (⓪), pas par l'écoute ; pour les autres fichiers lus, il reste. · Un fichier
  interdit présent HORS de la racine (ailleurs sur la machine) n'est pas vu par ⓪ : seule l'écoute le verrait. ·
  `ecoute_nomme` porte sur la PART : si un lot est sourd et un autre non, c'est le joueur qui le voit (⑤bis).
⑩ EFFET — Écrit dans le dossier de travail ; l'épreuve écrit ses dossiers jetables ; ne touche pas au relevé.
⑪ TERMINAISON — Rend la main quand tous les lots de la part ont fini ; aucun délai par lot (celui du job GitHub
  borne la durée) ; sort par sys.exit avec le code dit en ⑤. Un de mes appels peut ne pas revenir : `jouer_un_lot`
  attend l'épreuve sans délai.
"""
import concurrent.futures
import datetime
import importlib.util
import json
import os
import sys
import zoneinfo

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
JOUEUR = os.path.join("tests", "outils", "JOUER_UNE_SERIE_DE_SABOTAGES.py")
MANIFESTE = "part.json"
# LES PROGRAMMES INTERDITS DANS CE CIRCUIT (consigne du Chat, 04-11-2026 : « ne lance jamais
# MESURER_LES_AJUSTEMENTS_DE_YAHOO.py ni tests/EPREUVES_DES_AJUSTEMENTS_DE_YAHOO_Jeu_08-10-2026.py »). Par leur NOM de
# fichier, où qu'ils soient : le premier vit dans etudes/outils/, le second dans tests/. Écrits ICI et nulle part
# ailleurs (R-708) : le rassemblement les importe, le circuit les lit par `--interdits`.
INTERDITS = ("MESURER_LES_AJUSTEMENTS_DE_YAHOO.py", "EPREUVES_DES_AJUSTEMENTS_DE_YAHOO_Jeu_08-10-2026.py")


def charger_le_joueur(racine):
    """Charge tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py de la racine comme un module.

    ① RÔLE — Réutiliser le joueur de la version éprouvée, pas une copie. ② CONTEXTE D'APPEL — `main` ; aussi
    rassembler_les_parts.py. ③ ENTRÉE — `racine` : le dépôt éprouvé. ④ CONDITIONS D'ENTRÉE — Le joueur et
    programmes/SERIES_DE_SABOTAGES.py, programmes/CERTIFIER_LA_VERSION.py, programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py
    (tour 6 : la liste des fichiers de commandes de GitHub) existent dans la racine.
    ⑤ SORTIE — UNE valeur : le module. ⑥ TRAITEMENT — importlib ; le joueur ajoute lui-même racine/programmes au
    chemin d'import. ⑦ UNITÉ — — ⑧ POURQUOI — Une seule rédaction du jeu d'un lot (R-708).
    ⑨ CE QUI CLOCHE — Le code de tête du joueur s'exécute (imports seulement, `main` est gardé par __name__).
    ⑩ EFFET — Lit des fichiers de la racine. ⑪ TERMINAISON — Rend la main ; une erreur d'import remonte.
    """
    spec = importlib.util.spec_from_file_location("JOUER_UNE_SERIE_DE_SABOTAGES", os.path.join(racine, JOUEUR))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lots_de_la_part(nb_lots, nb_parts, part):
    """Rend les numéros de lots (à partir de 1) qui reviennent à une part.

    ① RÔLE — Partager les lots entre les parts sans trou ni doublon. ② CONTEXTE D'APPEL — `main` ;
    rassembler_les_parts.py, qui vérifie le partage. ③ ENTRÉE — le nombre de lots, le nombre de parts, le numéro de
    la part (0 à nb_parts-1). ④ CONDITIONS D'ENTRÉE — 0 <= part < nb_parts. ⑤ SORTIE — UNE valeur : la liste des
    numéros, croissante (vide si la part n'a aucun lot). ⑥ TRAITEMENT — tour de rôle : k tel que (k-1) mod N == part.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, ⑥ ③. ⑨ CE QUI CLOCHE — Les lots n'ont pas tous la même durée : la part
    la plus lente fixe la durée totale. ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
    """
    return [k for k in range(1, nb_lots + 1) if (k - 1) % nb_parts == part]


def interdits_presents(racine):
    """Rend les chemins (relatifs) des fichiers de la racine qui portent le nom d'un programme interdit.

    ① RÔLE — Vérifier que ce qui ne doit pas tourner n'est même pas là. ② CONTEXTE D'APPEL — `main`, avant tout lot.
    ③ ENTRÉE — `racine` : le dépôt joué. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste triée (vide si
    aucun). ⑥ TRAITEMENT — os.walk sans .git, nom de fichier comparé à INTERDITS. ⑦ UNITÉ — — ⑧ POURQUOI — Relecture
    du 04-11-2026, D4 : un programme lancé en « -I » n'est pas écouté ; absent, il ne peut pas être lancé depuis la
    racine. Une propriété (le nom), pas un chemin : un déplacement ne la contourne pas. ⑨ CE QUI CLOCHE — Un lien
    symbolique de nom interdit compte (os.walk le liste) ; un fichier interdit HORS de la racine n'est pas vu.
    ⑩ EFFET — Lit des dossiers. ⑪ TERMINAISON — Rend la main.
    """
    trouves = []
    for r, ds, fs in os.walk(racine):
        ds[:] = [d for d in ds if d != ".git"]
        trouves += [os.path.relpath(os.path.join(r, f), racine) for f in fs if f in INTERDITS]
    return sorted(trouves)


def interdits_lus(ecoute):
    """Rend les lignes d'une écoute qui nomment un programme interdit ; None si l'écoute n'existe pas.

    ① RÔLE — Dire si une part a ouvert un programme interdit. ② CONTEXTE D'APPEL — `main` (fin de part) ;
    rassembler_les_parts.py (chaque part, avant d'écrire quoi que ce soit). ③ ENTRÉE — `ecoute` : le dossier
    « ecoute » d'une part (un fichier « lus.<pid> » par processus écouté, un chemin par ligne). ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des lignes fautives (vide si aucune), ou None si le dossier manque.
    ⑥ TRAITEMENT — chaque ligne de chaque fichier ; fautive si son dernier élément (après le dernier « / ») est dans
    INTERDITS, ou est le code compilé d'un nom d'INTERDITS (« X.cpython-311.pyc » pour « X.py »). ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture du 04-11-2026, D1 et D4 : le pas du .yml passait en silence quand l'écoute manquait ; ici,
    l'absence se distingue (None) et l'appelant décide. ⑨ CE QUI CLOCHE — Ne voit que les processus écoutés (fiche
    en tête, ⑨). ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main.
    """
    if not os.path.isdir(ecoute):
        return None
    compiles = tuple(n[:-3] + "." for n in INTERDITS)
    fautives = []
    for f in sorted(os.listdir(ecoute)):
        for l in open(os.path.join(ecoute, f), encoding="utf-8", errors="replace").read().splitlines():
            nom = l.rsplit("/", 1)[-1]
            if nom in INTERDITS or (nom.endswith(".pyc") and nom.startswith(compiles)):
                fautives.append(l)
    return fautives


def ecoute_nomme(ecoute, chemin):
    """Dit si une ligne d'un flux de l'écoute est exactement `chemin`.

    ① RÔLE — Dire si un flux de l'écoute d'une part a entendu l'épreuve. ② CONTEXTE D'APPEL — `main` (fin de part,
    chaque flux) ; rassembler_les_parts.py (chaque flux d'une part qui a joué un lot). ③ ENTRÉE — `ecoute` : le dossier
    d'un flux (« ecoute », « execution » : FLUX_D_ECOUTE du joueur) ;
    `chemin` : le chemin absolu de l'épreuve sur la machine de la part. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE
    valeur : True ou False (False si le dossier manque). ⑥ TRAITEMENT — chaque ligne de chaque fichier, comparée à
    l'égalité. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête, ⑧ tour 3 : une écoute vide ou parasite ne prouve rien ; celle
    qui nomme l'épreuve prouve que le module d'écoute s'est chargé dans au moins un lot. ⑨ CE QUI CLOCHE — Fiche en
    tête, ⑨ (porte sur la part, pas sur chaque lot). ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main.
    """
    if not os.path.isdir(ecoute):
        return False
    for f in sorted(os.listdir(ecoute)):
        if chemin in open(os.path.join(ecoute, f), encoding="utf-8", errors="replace").read().splitlines():
            return True
    return False


def lire_les_arguments(arguments):
    """Rend ce que le joueur lit de sa ligne de commande : {racine, epreuve, releve, part, nb_parts, lot, parallele,
    travail} ; lève ValueError si elle ne convient pas.

    ① RÔLE — Lire la ligne de commande en UN endroit, que l'épreuve du relais des séries appelle elle-même (choix
      délégué par Jean-Luc, relevé du Chat n°347, Q3 = 1 : « l'épreuve lit avec la fonction du joueur ») : ce qu'elle
      compare à la demande est ce que le joueur lit vraiment, pas une seconde lecture qui pourrait différer.
    ② CONTEXTE D'APPEL — `main` ; tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py.
    ③ ENTRÉE — `arguments` : la liste des arguments, sans le nom du programme (sys.argv[1:]).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire (racine et travail en chemins réels ; part, nb_parts, lot, parallele en
      entiers). [rend: 1]
    ⑥ TRAITEMENT — trois arguments sans « -- » (racine, épreuve, relevé) ; les options « --nom=valeur », chacune AU
      PLUS UNE FOIS, parmi part, nb-parts, lot, parallele, travail ; part, nb-parts, lot et travail obligatoires,
      parallele 2 par défaut ; 0 <= part < nb_parts ; lot >= 1 ; parallele >= 1 ; une option inconnue ou sans « = »
      est refusée.
    ⑦ UNITÉ — lot : des sabotages par lot ; parallele : des lots joués en même temps.
    ⑧ POURQUOI — Défaut NV-2 du lot 262 (relevé n°298) : « --lot » donné deux fois, le dictionnaire gardait la
      dernière valeur (11 au lieu de 13) et tout restait vert. « --lot » n'a plus de valeur par défaut ici (6 avant le
      08-11-2026) : les valeurs par défaut vivent dans la table des séries (tests/LANCEMENT_DES_EPREUVES.json,
      « serie_du_circuit »), et le circuit passe toujours « --lot ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    pos = [a for a in arguments if not a.startswith("--")]
    opt = {}
    for a in arguments:
        if not a.startswith("--"):
            continue
        if "=" not in a:
            raise ValueError(f"option sans valeur : {a}")
        nom, valeur = a[2:].split("=", 1)
        if nom not in ("part", "nb-parts", "lot", "parallele", "travail"):
            raise ValueError(f"option inconnue : --{nom}")
        if nom in opt:
            raise ValueError(f"option donnée deux fois : --{nom}")
        opt[nom] = valeur
    if len(pos) != 3:
        raise ValueError(f"{len(pos)} argument(s) sans « -- », 3 attendus")
    for nom in ("part", "nb-parts", "lot", "travail"):
        if nom not in opt:
            raise ValueError(f"option --{nom} absente")
    lu = {"racine": os.path.realpath(pos[0]), "epreuve": pos[1], "releve": pos[2], "part": int(opt["part"]),
          "nb_parts": int(opt["nb-parts"]), "lot": int(opt["lot"]), "parallele": int(opt.get("parallele", 2)),
          "travail": os.path.realpath(opt["travail"])}
    if not (0 <= lu["part"] < lu["nb_parts"] and lu["lot"] >= 1 and lu["parallele"] >= 1):
        raise ValueError("part hors de 0..nb_parts-1, ou lot, ou parallele, inférieur à 1")
    return lu


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête. ⑤ SORTIE — UNE valeur : 0 ou 2. ⑥ TRAITEMENT — Fiche en tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête. ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main.
    """
    if sys.argv[1:] == ["--interdits"]:
        print("\n".join(INTERDITS))
        return 0
    try:
        lu = lire_les_arguments(sys.argv[1:])
    except ValueError as e:
        print(f"ARRET usage ({e}) : jouer_une_part.py <racine> <épreuve> <relevé> --part=I --nb-parts=N --lot=L "
              "[--parallele=2] --travail=<dossier>")
        return 2
    racine, epreuve, releve, travail = lu["racine"], lu["epreuve"], lu["releve"], lu["travail"]
    part, nb_parts, taille, parallele = lu["part"], lu["nb_parts"], lu["lot"], lu["parallele"]
    if os.path.basename(epreuve) in INTERDITS:
        print(f"ARRET épreuve interdite dans ce circuit : {epreuve}")
        return 2
    presents = interdits_presents(racine)
    if presents:
        print(f"ARRET la racine porte un programme interdit dans ce circuit : {', '.join(presents)} — le retirer de la copie")
        return 2
    try:
        joueur = charger_le_joueur(racine)
        noms = joueur.SERIE.noms_des_sabotages(os.path.join(racine, epreuve))
    except (OSError, SyntaxError, ValueError, ImportError) as e:
        print(f"ARRET joueur ou épreuve illisible : {type(e).__name__} : {e}")
        return 2
    if not noms:
        print(f"ARRET aucun dictionnaire SABOTAGES lisible dans {epreuve}")
        return 2
    lots = joueur.decouper(noms, taille)
    mes_lots = lots_de_la_part(len(lots), nb_parts, part)
    if os.path.exists(os.path.join(travail, MANIFESTE)):
        os.remove(os.path.join(travail, MANIFESTE))   # le manifeste ne vaut qu'après une part complète
    joueur.preparer_le_travail(travail)              # la préparation du joueur, pas une copie (fiche en tête, ⑧)
    refus = joueur.refus_du_disque_temporaire(travail)   # M-1 : la garde du joueur, pas une copie (R-708)
    if refus:
        print("ARRET " + refus)
        return 2
    place = {"debut": joueur.place_libre_mo(travail)}
    depart = os.path.join(travail, "etat_du_depart.json")
    etat = joueur.etat_du_depart(racine, releve)     # celui du joueur (R-708)
    if os.path.exists(depart):
        avant = json.load(open(depart, encoding="utf-8"))
        if any(etat.get(c) != e for c, e in avant.items()):
            print(f"ARRET la racine a changé depuis le départ de cette part ({travail}) — prendre un dossier neuf")
            return 2
        etat = avant
    else:
        json.dump(etat, open(depart, "w", encoding="utf-8"))
        open(os.path.join(travail, "debut.txt"), "w").write(datetime.datetime.now(PARIS).strftime("%d-%m-%Y %Hh%M"))
    print(f"ETAPE {joueur.heure()} part {part + 1}/{nb_parts} : {len(noms)} sabotages en {len(lots)} lots ; "
          f"cette part joue les lots {mes_lots or 'aucun'}, {parallele} à la fois ; place libre {place['debut']} Mo",
          flush=True)
    # le témoin du milieu : la place libre mesurée PENDANT les lots, par le joueur (une seule implémentation, R-708) ;
    # chaque lot y écrit sa place avant sa marque de fin ; le rassemblement les reprend et le joueur les juge
    with joueur.surveiller_la_place(travail):
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallele) as g:
            codes = dict(g.map(lambda k: joueur.jouer_un_lot(racine, epreuve, travail, k, lots[k - 1]), mes_lots))
    # ⑤bis un lot sourd (joueur patché : code None, rien écrit) : la part n'est pas sûre.
    sourds = sorted(k for k, c in codes.items() if c is None)
    if sourds:
        print(f"ARRET écoute sourde pour le(s) lot(s) {sourds} : impossible de dire ce qu'ils ont lu")
        return 2
    # ⑥ la racine ne doit pas avoir changé pendant la part : le rassemblement se fera sur une autre copie.
    apres = joueur.etat_du_depart(racine, releve)
    change = [c for c, e in etat.items() if apres.get(c) != e]
    if change:
        print(f"ARRET {len(change)} fichier(s) de la racine ont changé pendant la part : {', '.join(change[:5])}")
        return 2
    # ⑥bis chaque flux : aucun programme interdit nommé ; le flux doit exister (il est créé plus haut : son absence est
    # une anomalie) et, si la part a joué, nommer l'épreuve.
    for nom_du_flux in joueur.FLUX_D_ECOUTE.values():
        dossier = os.path.join(travail, nom_du_flux)
        fautives = interdits_lus(dossier)
        if fautives is None or fautives:
            print("ARRET " + (f"flux « {nom_du_flux} » de l'écoute absent : impossible de dire ce que la part a lu"
                              if fautives is None else
                              f"programme interdit lu pendant la part : {', '.join(fautives[:3])}"))
            return 2
        if mes_lots and not ecoute_nomme(dossier, os.path.realpath(os.path.join(racine, epreuve))):
            print(f"ARRET écoute sourde : aucune ligne du flux « {nom_du_flux} » ne nomme l'épreuve {epreuve} — "
                  "impossible de dire ce que la part a lu")
            return 2
    place["fin"] = joueur.place_libre_mo(travail)
    place["minimum"] = joueur.lire_la_place(travail)
    json.dump({"epreuve": epreuve, "releve": releve, "lot": taille, "nb_parts": nb_parts, "part": part,
               "parallele": parallele, "racine": racine, "noms": noms, "lots": mes_lots,
               "codes": {str(k): c for k, c in sorted(codes.items())}, "place_libre_mo": place},
              open(os.path.join(travail, MANIFESTE), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rouges = [k for k, c in codes.items() if c != 0]
    en_erreur = [k for k in mes_lots if joueur.trace_d_erreur_systeme(open(
        os.path.join(travail, f"lot_{k:02d}.out"), encoding="utf-8", errors="replace").read()) is not None]
    print(f"FINI {joueur.heure()} part {part + 1}/{nb_parts} : {len(mes_lots)} lot(s) joué(s), "
          f"lots rouges : {sorted(rouges) or 'aucun'} ; lots en erreur système (série NON CONFORME au rassemblement) : "
          f"{en_erreur or 'aucun'} ; place libre {place['debut']} Mo au début, {place['fin']} Mo à la fin, "
          f"{place['minimum']} Mo au plus bas (plancher {joueur.plancher_mo()} Mo, jugé au rassemblement)", flush=True)
    return 0


if __name__ == "__main__":
    # GARDE GÉNÉRALE (relecture du 04-11-2026 à 19h53, remarque sur la fiche ⑤) : une erreur imprévue sort en ARRET,
    # code 2, avec sa trace — jamais en 1.
    try:
        code = main()
    except Exception as e:   # noqa: BLE001 — toute erreur, par construction
        import traceback
        traceback.print_exc()
        print(f"ARRET erreur imprévue, rien de sûr : {type(e).__name__} : {e}", flush=True)
        code = 2
    sys.exit(code)
