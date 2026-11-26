#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PILOTER_UN_PLANNING.py — le programme de pilotage, CŒUR GÉNÉRIQUE. Mer 25-11-2026 (Paris), corrigé le même soir.
Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. « Ce programme lit un planning (étapes, dépendances, ressources : des DONNÉES, jamais du code) et
l'état réel de chaque étape, et écrit la liste exacte des actions à faire maintenant et le verdict RESTER ÉVEILLÉ /
PEUT S'ARRÊTER ; il sert à ce que celui qui pilote exécute une liste au lieu de décider de mémoire. »
Il ne connaît aucun projet : ce qui est propre à un projet vit dans un ADAPTATEUR (un fichier Python nommé dans
planning.csv) et dans des CONTRÔLES (des commandes nommées dans controles.csv).

① RÔLE — Un passage complet : lire le planning ; demander l'état réel à l'adaptateur ; retenir l'état de chaque
  étape (l'OBSERVÉ l'emporte toujours sur le DÉCLARÉ) ; se souvenir des étapes annoncées LANCER et pas encore
  confirmées ; calculer les places prises, le chemin critique, le palier de chaque ressource (AIMD : monter d'un pas
  quand la ressource est pleine sans nouveau refus, diviser par deux dès un nouveau refus observé) ; remplir les
  places libres (chemin critique d'abord) ; lancer les contrôles ; comparer avec le passage précédent ; écrire les
  actions, le verdict et l'état.
② CONTEXTE D'APPEL — En PREMIER à chaque passage de celui qui pilote. À la main :
  python3 -I programmes/PILOTER_UN_PLANNING.py <dossier>. Les épreuves appellent `passage` directement.
③ ENTRÉE — <dossier du planning> ; options : --etat=DOSSIER (OBLIGATOIRE, hors de tout dépôt git : où lire et
  écrire l'état) · --maintenant=AAAA-MM-JJTHH:MM (heure de Paris imposée) · --param=CLE=VALEUR (répétable, transmis
  à l'adaptateur et aux contrôles : remplace la valeur de planning.csv) · --liberer=ETAPE (répétable : efface le
  lancement non confirmé de cette étape, geste humain unique après une ligne À VÉRIFIER ; refusé si l'étape n'a pas
  été signalée À VÉRIFIER) · --json · --sans-ecrire.
  Fichiers lus dans le dossier (séparateur « ; », UTF-8, en-tête exact) :
  planning.csv  « cle;valeur » — clés connues : nom, objectif, adaptateur (chemin du fichier Python ; vide =
                adaptateur intégré « fichiers »), racine (base des preuves et des commandes ; défaut : le dossier),
                delai_de_confirmation_min (OBLIGATOIRE, nombre > 0 : au-delà, une étape annoncée LANCER dont
                l'observation n'a pas changé est signalée À VÉRIFIER, une seule fois ; elle n'est JAMAIS relancée
                d'elle-même) ; duree_attendue_<ressource>_min et duree_attendue_<ressource>_source (facultatives,
                par paire : la durée attendue d'un LANCEMENT sur cette ressource, > 0, et sa source, qui commence par
                « mesurée » ou « estimée » — A-1021) ; toute autre clé est un PARAMÈTRE transmis.
  etapes.csv    « etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat » — depend_de : identifiants
                séparés par « | » ; duree_h : nombre décimal ≥ 0 ; preuve : « <préfixe>:<texte> », le préfixe étant
                lu par l'adaptateur intégré (« fichier: ») ou DÉCLARÉ par l'adaptateur du projet (PREUVES_LUES) ;
                etat (déclaré) : vide ou a_faire · pause · attend:<qui et quoi> · bloque:<raison>. « en_cours » et
                « fait » ne se DÉCLARENT pas : ils s'observent.
  ressources.csv « ressource;capacite;palier_initial;pas;source;mesure » — capacite, palier_initial, pas : entiers
                ≥ 1, palier_initial ≤ capacite ; source : d'où vient la capacité ; mesure : texte libre que SEUL l'adaptateur lit (vide permis).
  controles.csv (facultatif) « controle;commande » — commande découpée comme un shell (shlex), avec {racine},
                {dossier} et {param:CLE} remplacés en un seul passage.
④ CONDITIONS D'ENTRÉE — Identifiants uniques sans espace ; dépendances et ressources citées existantes ; pas de
  cycle ; chaque préfixe de preuve lu par un adaptateur ; état précédent lisible, sans heure future ; dossier
  d'état hors de tout dépôt git ; aucun autre passage en train d'écrire le même dossier d'état (verrou exclusif
  sur VERROU.lock). Sinon ARRET, code 2, rien écrit. L'adaptateur rend, s'il le peut, une `phase` STABLE par étape
  qui ne change QUE sur un geste de l'exécutant lancé (par exemple l'étape du travail et l'empreinte du CONTENU
  de ce qu'il doit produire — jamais la pointe d'une branche, qu'un commit sans rapport fait bouger) ; sinon son `detail` en tient lieu.
⑤ SORTIE — Des lignes affichées (et ACTIONS.txt) : ENQUÊTER (EN TÊTE, à chaque passage tant qu'une échéance est
  dépassée ; son apparition et sa disparition sont des changements, notifiés une fois — A-1021) · CHANGEMENT · CONTRADICTION · LANCER · À VÉRIFIER (une seule
  fois par lancement) · LANCÉE NON CONFIRMÉE · EN COURS · EN FILE · ATTEND · BLOQUÉE · EN PAUSE · RESSOURCE BLOQUÉE · MESURE IMPOSSIBLE · PALIER · CONTRÔLE ·
  puis UNE ligne VERDICT et UNE ligne NOTIFIER. Code de sortie, UNE valeur : 0 verdict rendu, contrôles muets ·
  3 verdict rendu, un contrôle ALERTE (l'emporte sur 4, les deux sont alors annoncés) · 4 verdict rendu, mais un
  contrôle ou une mesure n'a pas pu se faire (R-734) · 2 rien n'a pu être conclu.
⑥ TRAITEMENT — `lire_planning` → `observer` → `etats_finals` → `observation_de` → `lancements_a_suivre` →
  `suivre` → `echeances` → `chemin_critique` →
  `ressources_du_passage` (places prises + paliers) → `remplir` → `lancer_les_controles` → `verdict` →
  `changements` → `rediger` → écriture de l'état.
⑦ UNITÉ — Heures (durées) ; minutes (délai de confirmation) ; places (une place = une unité de ressource).
⑧ POURQUOI — Décisions du propriétaire du planning du 25-11-2026 : un programme de pilotage d'abord ; utilisable
  pour toute planification ; optimiser selon les ressources disponibles ; un point d'avancement à chaque
  changement (leurs numéros et leurs mots vivent dans la note de livraison et le registre du projet, pas ici : ce
  cœur ne connaît aucun projet). Corrigé après deux relectures à mandat inversé et deux jugements d'un superviseur :
  mémoire des lancements confirmés par l'OBSERVATION et jamais relancés d'eux-mêmes, observé contre déclaré, AIMD
  qui ne monte que sur l'observé, préfixes de preuve déclarés.
⑨ CE QUI CLOCHE — (a) Le chemin critique existe aussi dans un autre programme du projet d'origine (en pause) :
  deux implémentations d'une même chose divergent toujours ; à fondre à l'installation (voir la note de livraison). (b) Les durées sont
  déclarées, jamais mesurées. (c) Le programme ne lance rien : il ÉCRIT les actions ; les exécuter repose sur la
  parole de celui qui pilote. (d) Un adaptateur est du code exécuté avec les droits du programme. (e) Le palier
  monte d'un pas à CHAQUE passage où la ressource est pleine d'étapes OBSERVÉES : plus les passages sont rapprochés,
  plus il monte vite ; il n'est freiné que par la capacité et par les refus observés. (f) Sans signal de refus
  (l'adaptateur n'en rend pas pour la ressource), le palier peut monter jusqu'à la capacité déclarée. (g) Un
  lancement dont l'exécutant est mort garde sa place jusqu'au geste --liberer : c'est voulu, et dit une fois.
  (h) Deux passages SIMULTANÉS sur le même dossier d'état s'excluent par un verrou (fcntl.flock) : le second
  s'arrête (code 2) au lieu d'attendre. Le verrou ne vaut que sur une même machine et un disque local ; avec
  --sans-ecrire, aucun verrou n'est pris (rien n'est écrit). (i) Une étape redite LANCER après avoir été
  confirmée est un changement notifié (l'état gardé porte l'heure du lancement) : une confirmation à tort ne
  passe plus en silence, mais elle n'est pas empêchée — c'est à la `phase` de l'adaptateur d'être juste.
  (j) Un lancement dont l'étape est observée EN COURS reste en mémoire avec son heure de départ (N-79) ; si l'étape
  revient ensuite à l'observation du lancement sans rien produire (marque retirée), le lancement redevient non
  confirmé avec son heure d'origine : il n'est pas relancé, il est signalé (À VÉRIFIER, ENQUÊTER). (k) Deux règles
  d'alerte coexistent sur un lancement : le délai À VÉRIFIER (delai_de_confirmation_min) et l'échéance ENQUÊTER
  (A-1021) ; retirer la première demande l'accord du propriétaire du planning.
⑩ EFFET — Écrit dans le dossier d'état : ETAT_DU_PILOTAGE.json et ACTIONS.txt (remplacés d'un coup),
  JOURNAL_DES_CHANGEMENTS.csv (une ligne ajoutée par changement). Rien avec --sans-ecrire.
⑪ TERMINAISON — Pas de boucle ouverte ; chaque contrôle est borné à DELAI_CONTROLE_S secondes ; un adaptateur qui
  ne rend pas la main bloquerait le passage (son propre ⑪ doit le dire).
"""
import csv
import datetime
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
DELAI_CONTROLE_S = 120
ETATS = ("a_faire", "en_cours", "fait", "pause", "attend", "bloque")
DECLARABLES = ("a_faire", "pause", "attend", "bloque")
OBSERVABLES = ("a_faire", "en_cours", "fait")
PREUVES_INTEGREES = ("fichier:",)
COL_ETAPES = ("etape", "libelle", "depend_de", "executant", "ressource", "duree_h", "preuve", "etat")
COL_RESSOURCES = ("ressource", "capacite", "palier_initial", "pas", "source", "mesure")
COL_CONTROLES = ("controle", "commande")
FICHIERS_DU_PLANNING = ("planning.csv", "etapes.csv", "ressources.csv", "controles.csv")
NOM_ETAT = "ETAT_DU_PILOTAGE.json"
NOM_ACTIONS = "ACTIONS.txt"
NOM_JOURNAL = "JOURNAL_DES_CHANGEMENTS.csv"
NOM_VERROU = "VERROU.lock"
MOTIF_SUBSTITUTION = re.compile(r"\{(racine|dossier|param:[^{}]*)\}")


class Arret(Exception):
    """① RÔLE — Dire « rien n'a pu être conclu » avec sa raison.
    ② CONTEXTE D'APPEL — levée par toute lecture ou contrôle d'entrée ; rattrapée par `main` (code 2).
    ③ ENTRÉE — le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """


def nombre(texte, quoi):
    """① RÔLE — Lire un nombre décimal écrit à la française ou à l'anglaise.
    ② CONTEXTE D'APPEL — `lire_planning`, pour duree_h, capacite, palier_initial, pas, delai_de_confirmation_min.
    ③ ENTRÉE — `texte` : la case ; `quoi` : ce qu'elle désigne, pour le message d'erreur.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un float ≥ 0.
      [rend: 1]
    ⑥ TRAITEMENT — virgule → point, float(), refus du négatif et du non fini.
    ⑦ UNITÉ — celle de la case (heures, minutes ou places).
    ⑧ POURQUOI — les tableurs de Jean-Luc écrivent « 0,5 ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours, ou lève Arret.
      [sort: non]
    """
    try:
        v = float((texte or "").strip().replace(",", "."))
    except ValueError:
        raise Arret(f"{quoi} n'est pas un nombre : « {texte} »")
    if v != v or v in (float("inf"), float("-inf")) or v < 0:
        raise Arret(f"{quoi} négatif ou non fini : « {texte} »")
    return v


def lire_table(chemin, colonnes, obligatoire=True):
    """① RÔLE — Lire un CSV « ; » à en-tête fermé.
    ② CONTEXTE D'APPEL — `lire_planning`, une fois par fichier.
    ③ ENTRÉE — `chemin` ; `colonnes` : l'en-tête exact attendu ; `obligatoire` : absent = Arret, sinon liste vide.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des lignes (dicts, cases sans espaces autour).
      [rend: 1]
    ⑥ TRAITEMENT — csv.DictReader ; en-tête comparé à `colonnes` ; colonne en trop (un « ; » de trop) refusée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un en-tête fermé empêche qu'une colonne mal nommée soit ignorée en silence.
    ⑨ CE QUI CLOCHE — les lignes vides sont sautées ; une ligne commençant par « # » aussi (commentaire).
    ⑩ EFFET — lit un fichier.
    ⑪ TERMINAISON — revient toujours, ou lève Arret.
      [sort: non]
    """
    if not os.path.isfile(chemin):
        if obligatoire:
            raise Arret(f"fichier absent : {chemin}")
        return []
    try:
        with open(chemin, newline="", encoding="utf-8-sig") as f:
            lecteur = csv.DictReader(f, delimiter=";")
            if tuple(c.strip() for c in (lecteur.fieldnames or ())) != tuple(colonnes):
                raise Arret(f"en-tête de {os.path.basename(chemin)} : {lecteur.fieldnames} au lieu de {list(colonnes)}")
            lignes = []
            for l in lecteur:
                if None in l:
                    raise Arret(f"colonne en trop dans {os.path.basename(chemin)} : {l}")
                l = {k.strip(): (v or "").strip() for k, v in l.items()}
                if not any(l.values()) or l[colonnes[0]].startswith("#"):
                    continue
                lignes.append(l)
            return lignes
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        raise Arret(f"lecture impossible de {chemin} : {e}")


def lire_planning(dossier, params_imposes=None):
    """① RÔLE — Lire et contrôler tout le planning, avant toute décision.
    ② CONTEXTE D'APPEL — `passage`, une fois.
    ③ ENTRÉE — `dossier` ; `params_imposes` : dict CLE→VALEUR (option --param), qui remplace planning.csv.
    ④ CONDITIONS D'ENTRÉE — voir ④ du module.
    ⑤ SORTIE — UNE valeur : dict {params, delai_min, etapes (dict id→ligne, ordre du fichier conservé), ressources
      (dict), controles (liste), empreinte (des fichiers du planning), attendues ({ressource: (minutes, source)})}.
      [rend: 1]
    ⑥ TRAITEMENT — lire les quatre tables ; convertir les nombres ; vérifier unicité, références, états déclarés
      (en_cours et fait refusés : ils s'observent), délai de confirmation, cycle ; empreinte sha256 des fichiers.
    ⑦ UNITÉ — heures, minutes, places.
    ⑧ POURQUOI — tout ce qui peut échouer échoue AVANT qu'une action soit écrite (R-734). L'empreinte sert au
      journal : un planning modifié est un changement à notifier (mineur 9 de la relecture du 25-11-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lit des fichiers.
    ⑪ TERMINAISON — revient toujours, ou lève Arret.
      [sort: non]
    """
    # N-70 (RELU du 25-11-2026, 22h54) : un palier initial au-dessus de la capacité est refusé plus bas, comme une
    # capacité 0 ou un pas 0, au lieu d'être ramené à la capacité sans un mot.
    params = {}
    for l in lire_table(os.path.join(dossier, "planning.csv"), ("cle", "valeur")):
        if l["cle"] in params:
            raise Arret(f"clé en double dans planning.csv : {l['cle']}")
        params[l["cle"]] = l["valeur"]
    params.update(params_imposes or {})
    if "delai_de_confirmation_min" not in params:
        raise Arret("planning.csv sans delai_de_confirmation_min (minutes au-delà desquelles un LANCER sans effet "
                    "observé est redit « non confirmé »)")
    delai = nombre(params["delai_de_confirmation_min"], "delai_de_confirmation_min")
    if delai <= 0:
        raise Arret("delai_de_confirmation_min doit être > 0")
    etapes = {}
    for l in lire_table(os.path.join(dossier, "etapes.csv"), COL_ETAPES):
        e = l["etape"]
        if not e or any(c.isspace() for c in e) or e in etapes:
            raise Arret(f"identifiant d'étape vide, avec espace, ou en double : « {e} »")
        l["deps"] = [d.strip() for d in l["depend_de"].split("|") if d.strip()]
        l["duree"] = nombre(l["duree_h"], f"duree_h de {e}")
        decl = l["etat"] or "a_faire"
        tete = decl.split(":", 1)[0]
        if tete not in DECLARABLES or (tete in ("attend", "bloque") and ":" not in decl):
            raise Arret(f"état déclaré refusé pour {e} : « {decl} » (permis : {', '.join(DECLARABLES)} ; attend: et "
                        "bloque: avec leur raison ; en_cours et fait ne se déclarent pas, ils s'observent)")
        l["etat"] = decl
        etapes[e] = l
    if not etapes:
        raise Arret("aucune étape dans etapes.csv")
    ressources = {}
    for l in lire_table(os.path.join(dossier, "ressources.csv"), COL_RESSOURCES):
        r = l["ressource"]
        if not r or any(c.isspace() for c in r) or r in ressources:
            raise Arret(f"identifiant de ressource vide, avec espace, ou en double : « {r} »")
        for c in ("capacite", "palier_initial", "pas"):
            v = nombre(l[c], f"{c} de {r}")
            if v < 1 or v != int(v):
                raise Arret(f"{c} de {r} doit être un entier ≥ 1 : « {l[c]} »")
            l[c] = int(v)
        if l["palier_initial"] > l["capacite"]:
            raise Arret(f"palier_initial de {r} ({l['palier_initial']}) supérieur à sa capacité ({l['capacite']}) : "
                        "le palier serait ramené à la capacité sans le dire")
        ressources[r] = l
    for e, l in etapes.items():
        for d in l["deps"]:
            if d not in etapes:
                raise Arret(f"{e} dépend de « {d} », absente du planning")
        if l["ressource"] and l["ressource"] not in ressources:
            raise Arret(f"{e} utilise la ressource « {l['ressource']} », absente de ressources.csv")
    if a_un_cycle({e: l["deps"] for e, l in etapes.items()}):
        raise Arret("le graphe des dépendances a un cycle")
    # A-1021 : la durée attendue d'un LANCEMENT sur une ressource se déclare au planning, avec sa source
    attendues = {}
    for cle, v in params.items():
        m = re.fullmatch(r"duree_attendue_(.+)_min", cle)
        if not m:
            continue
        r = m.group(1)
        if r not in ressources:
            raise Arret(f"{cle} : la ressource « {r} » est absente de ressources.csv")
        minutes = nombre(v, cle)
        source = params.get(f"duree_attendue_{r}_source", "").strip()
        if minutes <= 0 or not source.lower().startswith(("mesurée", "estimée")):
            raise Arret(f"{cle} doit être > 0 et porter sa source (clé duree_attendue_{r}_source, commençant par "
                        f"« mesurée » ou « estimée ») : « {v} », source « {source} »")
        attendues[r] = (minutes, source)
    controles = lire_table(os.path.join(dossier, "controles.csv"), COL_CONTROLES, obligatoire=False)
    h = hashlib.sha256()
    for nom in FICHIERS_DU_PLANNING:
        c = os.path.join(dossier, nom)
        h.update(nom.encode() + b"\0" + (open(c, "rb").read() if os.path.isfile(c) else b"") + b"\0")
    return {"params": params, "delai_min": delai, "etapes": etapes, "ressources": ressources,
            "controles": controles, "empreinte": h.hexdigest()[:16], "attendues": attendues}


def a_un_cycle(deps):
    """① RÔLE — Dire si le graphe des dépendances a un cycle, pour refuser un planning circulaire avant tout calcul.
    ② CONTEXTE D'APPEL — `lire_planning`, une fois.
    ③ ENTRÉE — `deps` : dict identifiant → liste des identifiants dont il dépend.
    ④ CONDITIONS D'ENTRÉE — toutes les dépendances citées existent (vérifié avant).
    ⑤ SORTIE — UNE valeur : vrai s'il y a un cycle.
      [rend: 1]
    ⑥ TRAITEMENT — parcours en profondeur itératif, trois couleurs (blanc, gris, noir).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un cycle rendrait le chemin critique infini.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — chaque nœud est fermé une fois : revient toujours.
      [sort: non]
    """
    couleur = {e: 0 for e in deps}
    for depart in deps:
        if couleur[depart]:
            continue
        pile = [(depart, iter(deps[depart]))]
        couleur[depart] = 1
        while pile:
            n, it = pile[-1]
            suivant = next(it, None)
            if suivant is None:
                couleur[n] = 2
                pile.pop()
            elif couleur[suivant] == 1:
                return True
            elif couleur[suivant] == 0:
                couleur[suivant] = 1
                pile.append((suivant, iter(deps[suivant])))
    return False


def adaptateur_integre(planning, racine):
    """① RÔLE — L'adaptateur par défaut, « fichiers » : une étape est FAITE quand sa preuve existe et n'est pas vide,
      EN COURS quand une marque « <preuve>.en_cours » existe.
    ② CONTEXTE D'APPEL — `observer`, toujours, pour les étapes dont la preuve commence par « fichier: ».
    ③ ENTRÉE — `planning` (valeur de `lire_planning`) ; `racine` : dossier de base des chemins relatifs.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : {id: {etat, detail}} pour les étapes à preuve « fichier: » · {} (aucune ressource
      mesurée).
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque étape dont la preuve commence par « fichier: ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Luigi (une tâche est faite quand sa cible existe) : l'état se tire d'une preuve, jamais d'une
      déclaration (conception de l'ordonnanceur, 20-11-2026, § 1.2).
    ⑨ CE QUI CLOCHE — un octet suffit : il voit qu'un fichier EXISTE, jamais qu'il est BON.
    ⑩ EFFET — lit l'existence de fichiers.
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    obs = {}
    for e, l in planning["etapes"].items():
        if not l["preuve"].startswith("fichier:"):
            continue
        c = l["preuve"][len("fichier:"):].strip()
        c = c if os.path.isabs(c) else os.path.join(racine, c)
        if os.path.isfile(c) and os.path.getsize(c) > 0:
            obs[e] = {"etat": "fait", "detail": f"preuve présente : {c}"}
        elif os.path.exists(c + ".en_cours"):
            obs[e] = {"etat": "en_cours", "detail": f"marque {c}.en_cours"}
        else:
            obs[e] = {"etat": "a_faire", "detail": f"preuve absente : {c}"}
    return obs, {}


def charger_adaptateur(chemin):
    """① RÔLE — Charger le fichier Python de l'adaptateur du projet, pour donner au cœur la lecture propre au projet.
    ② CONTEXTE D'APPEL — `observer`, une fois par passage.
    ③ ENTRÉE — `chemin` : chemin absolu du fichier de l'adaptateur.
    ④ CONDITIONS D'ENTRÉE — le fichier définit observer(planning, racine, params) et PREUVES_LUES (tuple de préfixes).
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, avec le dossier du fichier ajouté au chemin des imports le temps du chargement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le cœur ne connaît aucun projet (A-1017).
    ⑨ CE QUI CLOCHE — le code chargé s'exécute avec les droits du programme.
    ⑩ EFFET — exécute le module.
    ⑪ TERMINAISON — revient, sauf si le module lui-même boucle ; lève Arret s'il est illisible ou incomplet.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("adaptateur_du_planning", chemin)
    if spec is None or spec.loader is None:
        raise Arret(f"adaptateur illisible : {chemin}")
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(chemin))
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path.pop(0)
    if not hasattr(m, "observer"):
        raise Arret(f"l'adaptateur {chemin} n'a pas de fonction observer(planning, racine, params)")
    lues = getattr(m, "PREUVES_LUES", None)
    if not isinstance(lues, tuple) or not all(isinstance(p, str) and p.endswith(":") for p in lues):
        raise Arret(f"l'adaptateur {chemin} ne déclare pas PREUVES_LUES (tuple de préfixes finissant par « : »)")
    return m


def observer(planning, dossier):
    """① RÔLE — Obtenir l'état réel des étapes et la mesure des ressources.
    ② CONTEXTE D'APPEL — `passage`, une fois.
    ③ ENTRÉE — `planning` ; `dossier` du planning.
    ④ CONDITIONS D'ENTRÉE — l'adaptateur, s'il est nommé, rend DEUX valeurs : {id: {etat (a_faire|en_cours|fait),
      action?, ressource?, detail?}} et {ressource: {occupees: int ou None (None = mesure impossible), capacite?:
      int, refus?: liste d'heures ISO des refus observés ou None (None = mesure impossible), detail?: str}} ; il
      peut remplir, pendant `observer`, une liste de module CONTROLES_DU_PASSAGE de (nom, liste d'arguments) ou
      (nom, None, raison) pour un contrôle impossible.
    ⑤ SORTIE — TROIS valeurs : observations des étapes · mesures des ressources · racine.
      [rend: 3]
    ⑥ TRAITEMENT — refuser toute preuve dont le préfixe n'est lu par personne (adaptateur intégré « fichier: » +
      PREUVES_LUES de l'adaptateur du projet) ; adaptateur intégré, puis celui du projet par-dessus ; exiger une
      observation, d'un état observable, pour CHAQUE étape.
    ⑦ UNITÉ — places.
    ⑧ POURQUOI — D5 de la relecture du 25-11-2026 : la preuve « aucune » de l'étape D n'était lue par personne, D
      restait « à lancer » pour toujours ; une preuve que personne ne lit est refusée (propriété, pas cas spécial).
    ⑨ CE QUI CLOCHE — une exception de l'adaptateur devient Arret : rien n'est conclu, ce qui est voulu (R-734).
    ⑩ EFFET — ceux de l'adaptateur.
    ⑪ TERMINAISON — celle de l'adaptateur.
      [sort: non]
    """
    racine = planning["params"].get("racine") or dossier
    racine = racine if os.path.isabs(racine) else os.path.normpath(os.path.join(dossier, racine))
    nom = planning["params"].get("adaptateur", "")
    module = None
    lues = PREUVES_INTEGREES
    if nom:
        chemin = nom if os.path.isabs(nom) else os.path.normpath(os.path.join(dossier, nom))
        if not os.path.isfile(chemin):
            raise Arret(f"adaptateur absent : {chemin}")
        module = charger_adaptateur(chemin)
        lues = PREUVES_INTEGREES + module.PREUVES_LUES
    for e, l in planning["etapes"].items():
        if not any(l["preuve"].startswith(p) for p in lues):
            raise Arret(f"preuve de {e} lue par personne : « {l['preuve']} » (préfixes lus : {', '.join(lues)}) — "
                        "l'étape ne pourrait jamais être vue faite")
    obs, mes = adaptateur_integre(planning, racine)
    planning["controles_adaptateur"] = []
    if module is not None:
        try:
            o2, m2 = module.observer(planning, racine, planning["params"])
        except Arret:
            raise
        except Exception as e:
            raise Arret(f"l'adaptateur a échoué : {type(e).__name__} {e}")
        obs.update(o2 or {})
        mes.update(m2 or {})
        planning["controles_adaptateur"] = list(getattr(module, "CONTROLES_DU_PASSAGE", []))
    for e, o in obs.items():
        if e not in planning["etapes"]:
            raise Arret(f"l'adaptateur rend une étape inconnue du planning : {e}")
        if o.get("etat") not in OBSERVABLES:
            raise Arret(f"l'adaptateur rend un état non observable pour {e} : « {o.get('etat')} »")
        if o.get("ressource") and o["ressource"] not in planning["ressources"]:
            raise Arret(f"l'adaptateur place {e} sur une ressource inconnue : {o['ressource']}")
    for e in planning["etapes"]:
        if e not in obs:
            raise Arret(f"aucune observation pour {e} : son préfixe de preuve est déclaré lu, mais rien n'a été rendu")
    return obs, mes, racine


def etats_finals(planning, obs):
    """① RÔLE — L'état retenu de chaque étape, sa ressource, son action, et la contradiction éventuelle.
    ② CONTEXTE D'APPEL — `passage`.
    ③ ENTRÉE — `planning` ; `obs` (observations, une par étape).
    ④ CONDITIONS D'ENTRÉE — chaque étape a une observation (garanti par `observer`).
    ⑤ SORTIE — UNE valeur : {id: {etat, motif, ressource, action, detail, executant, contradiction}}.
      [rend: 1]
    ⑥ TRAITEMENT — observé en_cours ou fait → c'est l'état retenu, TOUJOURS ; si le déclaré dit autre chose
      (pause, attend, bloque), la contradiction est écrite. Observé a_faire → l'état déclaré (a_faire, pause,
      attend, bloque), qui sert alors à EMPÊCHER le lancement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — D2 et mineur 11 de la relecture du 25-11-2026 : une pause déclarée cachait une étape qui tournait
      (« PEUT S'ARRÊTER » avec une étape en cours, occupation 0). Jugement du superviseur R-759 : le déclaré ne sert
      qu'à empêcher un lancement ; l'observé l'emporte toujours.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    out = {}
    for e, l in planning["etapes"].items():
        o = obs[e]
        decl = l["etat"]
        contradiction = ""
        if o["etat"] in ("en_cours", "fait"):
            brut = o["etat"]
            if decl != "a_faire":
                contradiction = f"déclaré « {decl} », observé « {o['etat']} » : l'observé l'emporte"
        else:
            brut = decl
        etat, _, motif = brut.partition(":")
        out[e] = {"etat": etat, "motif": motif.strip(), "ressource": o.get("ressource") or l["ressource"],
                  "action": o.get("action") or l["libelle"], "detail": o.get("detail", ""),
                  "executant": l["executant"], "contradiction": contradiction}
    return out


def heure(texte, quoi):
    """① RÔLE — Lire une heure ISO avec fuseau écrite dans l'état précédent.
    ② CONTEXTE D'APPEL — `lire_l_etat_precedent`.
    ③ ENTRÉE — `texte` ; `quoi` : ce qu'elle désigne, pour le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un datetime avec fuseau.
      [rend: 1]
    ⑥ TRAITEMENT — datetime.fromisoformat ; refus d'une heure sans fuseau.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — comparer une heure sans fuseau à une heure avec fuseau lève TypeError au milieu du passage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours, ou lève ValueError.
      [sort: non]
    """
    if not isinstance(texte, str):
        raise ValueError(f"{quoi} n'est pas un texte : {texte!r}")
    h = datetime.datetime.fromisoformat(texte)
    if h.tzinfo is None:
        raise ValueError(f"{quoi} sans fuseau : {texte}")
    return h


def lire_l_etat_precedent(chemin, maintenant):
    """① RÔLE — Lire et CONTRÔLER l'état du passage précédent avant de s'en servir.
    ② CONTEXTE D'APPEL — `passage`, une fois.
    ③ ENTRÉE — `chemin` du fichier ETAT_DU_PILOTAGE.json ; `maintenant` (datetime avec fuseau).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : dict {etapes: {id: texte}, ressources: {r: {palier: int, dernier_refus: ISO|None}},
      lancements: {id: {heure: datetime, observation: texte, ressource: texte, signale: datetime|None}}, actions:
      liste, verdict: texte, empreinte: texte, suivi: {id: {observation, depuis, en_cours_depuis}}, enqueter: liste}
      ; {} si le fichier n'existe pas.
      [rend: 1]
    ⑥ TRAITEMENT — json.load, puis vérification de chaque type (dont « suivi » {id: {observation, depuis,
      en_cours_depuis}} et « enqueter », liste d'identifiants — A-1021) ; une clé absente vaut vide (premier passage) ; une
      clé présente au mauvais type, l'ancienne clé « lancees » (lancements sans leur observation), une heure dans le
      FUTUR (plus d'une minute après `maintenant`), ou tout ValueError, KeyError, TypeError, AttributeError → Arret
      avec le conseil « le renommer pour repartir de zéro ».
    ⑦ UNITÉ — minutes (tolérance d'horloge : une).
    ⑧ POURQUOI — mineur 14 de la relecture du 25-11-2026 : un état mal formé levait KeyError au milieu du calcul.
      N-68 du RELU du 25-11-2026 (22h54) : une heure future (horloge en avance, --maintenant mal tapé) gelait une
      étape jusqu'à cette heure, affichée sans sa date. L'ancien format sans observation ne peut pas dire si un
      lancement est confirmé : le convertir serait deviner.
    ⑨ CE QUI CLOCHE — renommer l'état fait oublier les lancements en cours : celui qui pilote doit alors vérifier à
      la main ce qui tourne avant le passage suivant (le message le dit).
    ⑩ EFFET — lit un fichier.
    ⑪ TERMINAISON — revient toujours, ou lève Arret.
      [sort: non]
    """
    if not os.path.isfile(chemin):
        return {}
    conseil = (f" — le renommer pour repartir de zéro ({chemin}), après avoir vérifié à la main ce qui tourne : "
               "les lancements qu'il gardait seront oubliés")
    try:
        with open(chemin, encoding="utf-8") as f:
            brut = json.load(f)
        if not isinstance(brut, dict):
            raise TypeError("l'état n'est pas un objet JSON")
        if "lancees" in brut:
            raise ValueError("ancien format « lancees » (heures sans observation)")
        out = {"etapes": dict(brut.get("etapes", {})), "ressources": {}, "lancements": {},
               "actions": list(brut.get("actions", [])), "verdict": str(brut.get("verdict", "—")),
               "empreinte": str(brut.get("empreinte", ""))}
        if "heure" in brut:
            pas_futur(heure(brut["heure"], "heure du passage précédent"), maintenant, "heure du passage précédent")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in out["etapes"].items()):
            raise TypeError("« etapes » doit associer un texte à chaque étape")
        for r, v in dict(brut.get("ressources", {})).items():
            if not isinstance(v, dict) or not isinstance(v["palier"], int) or isinstance(v["palier"], bool):
                raise TypeError(f"ressource {r} : « palier » entier attendu")
            d = v.get("dernier_refus")
            if d is not None:
                heure(d, f"dernier_refus de {r}")
            out["ressources"][r] = {"palier": v["palier"], "dernier_refus": d}
        for e, v in dict(brut.get("lancements", {})).items():
            if not isinstance(v, dict) or not isinstance(v["observation"], str) or not isinstance(v["ressource"], str):
                raise TypeError(f"lancement de {e} : heure, observation et ressource attendues")
            s = v.get("signale")
            out["lancements"][e] = {
                "heure": pas_futur(heure(v["heure"], f"heure de lancement de {e}"), maintenant, f"lancement de {e}"),
                "observation": v["observation"], "ressource": v["ressource"],
                "signale": None if s is None else pas_futur(heure(s, f"signalement de {e}"), maintenant, f"signalement de {e}")}
        out["suivi"] = {}
        for e, v in dict(brut.get("suivi", {})).items():
            if not isinstance(v, dict) or not isinstance(v["observation"], str):
                raise TypeError(f"suivi de {e} : observation, depuis et en_cours_depuis attendus")
            c = v.get("en_cours_depuis")
            out["suivi"][e] = {
                "observation": v["observation"],
                "depuis": pas_futur(heure(v["depuis"], f"suivi de {e}"), maintenant, f"suivi de {e}"),
                "en_cours_depuis": None if c is None else pas_futur(heure(c, f"en cours de {e}"), maintenant, f"en cours de {e}")}
        out["enqueter"] = list(brut.get("enqueter", []))
        if not all(isinstance(x, str) for x in out["enqueter"]):
            raise TypeError("« enqueter » doit être une liste d'identifiants")
        return out
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise Arret(f"état précédent illisible : {type(e).__name__} {e}{conseil}")


def pas_futur(h, maintenant, quoi):
    """① RÔLE — Refuser une heure lue dans l'état qui est dans le FUTUR.
    ② CONTEXTE D'APPEL — `lire_l_etat_precedent`, pour chaque heure lue.
    ③ ENTRÉE — `h` et `maintenant` (datetime avec fuseau) ; `quoi` : ce que l'heure désigne, pour le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : `h` elle-même.
      [rend: 1]
    ⑥ TRAITEMENT — `h` plus d'une minute après `maintenant` → ValueError.
    ⑦ UNITÉ — minutes (tolérance : une, pour deux horloges presque d'accord).
    ⑧ POURQUOI — N-68 du RELU du 25-11-2026 (22h54) : une heure de lancement future gelait l'étape jusqu'à elle.
    ⑨ CE QUI CLOCHE — une horloge qui RECULE de moins d'une minute passe ; qui recule davantage arrête le passage.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours, ou lève ValueError.
      [sort: non]
    """
    if h > maintenant + datetime.timedelta(minutes=1):
        raise ValueError(f"{quoi} dans le futur : {h.isoformat()} (maintenant {maintenant.isoformat()})")
    return h


def observation_de(o):
    """① RÔLE — Résumer en UN texte ce que l'adaptateur observe d'une étape, pour reconnaître qu'elle a bougé.
    ② CONTEXTE D'APPEL — `passage`, une fois par étape ; le texte est gardé avec chaque lancement.
    ③ ENTRÉE — `o` : l'observation rendue par l'adaptateur ({etat, ressource?, phase?, detail?}).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte « etat | ressource observée | phase » (phase = `phase` si l'adaptateur la rend,
      sinon `detail`).
      [rend: 1]
    ⑥ TRAITEMENT — assemblage ; la ressource DÉCLARÉE au planning n'y entre pas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — superviseur R-759, tour 2 (25-11-2026 ~23h00) : la confirmation comparait l'ÉTAT, et l'adaptateur
      du projet traduit deux phases différentes (« à relire », « à écrire ») par le même état a_faire : une relecture
      lancée n'était jamais confirmée. Comparer TOUTE l'observation voit le passage d'une phase à l'autre. La
      ressource déclarée en est exclue : modifier le planning n'est pas une preuve que l'exécutant a commencé.
    ⑨ CE QUI CLOCHE — un adaptateur qui mettrait dans `detail` (sans `phase`) un texte qui change à chaque passage
      (une heure, un compteur) confirmerait tout lancement au passage suivant : son ④ doit rendre une `phase`
      stable. Un changement observé SANS rapport avec l'exécutant (un autre commit sur la même branche) confirme
      aussi : c'est le prix d'une observation qu'on ne devine pas.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    phase = o.get("phase") if o.get("phase") is not None else o.get("detail", "")
    return f"{o.get('etat')} | {o.get('ressource') or ''} | {phase}"


def lancements_a_suivre(etats, observations, precedent, maintenant, delai_min, liberer=()):
    """① RÔLE — LA notion « lancement » (R-708 : un seul endroit) : dire, pour chaque étape annoncée LANCER à un
      passage précédent, si elle est CONFIRMÉE, si elle garde sa place, et si elle doit être signalée À VÉRIFIER.
    ② CONTEXTE D'APPEL — `passage`, après `etats_finals` ; tout le reste (places prises, remplissage, verdict,
      journal, lignes, état écrit) lit ce qu'elle rend.
    ③ ENTRÉE — `etats` ; `observations` ({id: texte de `observation_de`}) ; `precedent` (valeur de
      `lire_l_etat_precedent`) ; `maintenant` ; `delai_min` (minutes) ; `liberer` : identifiants libérés à la main
      (option --liberer=X).
    ④ CONDITIONS D'ENTRÉE — chaque identifiant de `liberer` a un lancement en mémoire DÉJÀ SIGNALÉ À VÉRIFIER
      (sinon Arret : un lancement de quelques minutes, jamais signalé, ne se libère pas).
    ⑤ SORTIE — TROIS valeurs : `vivants`, {id: lancement + `demarre` (booléen)} — TOUS les lancements gardés,
      démarrés (l'étape est observée en_cours) ou non confirmés ; chacun garde SA ressource, SON heure de départ et
      SON observation du lancement, quel que soit l'état observé, et prend UNE place, sur la ressource du lancement ;
      `signale` y est rempli au passage où le délai est atteint (non confirmés seulement) · l'ensemble des
      identifiants signalés À CE PASSAGE · {id: lancement} des lancements libérés à la main. Jusqu'au tour 5, une
      QUATRIÈME sortie rendait les démarrés à part : elle a disparu (N-83, superviseur R-759 avant le tour 6), parce
      que deux dictionnaires étaient lus par deux règles différentes et qu'un démarré perdait sa ressource et sa durée.
      [rend: 3]
    ⑥ TRAITEMENT — pour chaque lancement en mémoire : libéré → effacé ; étape disparue du planning → oubliée ;
      étape observée en_cours → DÉMARRÉ (gardé, jamais terminé par là) ; observation différente de celle du
      lancement → TERMINÉ (oublié) ; sinon NON CONFIRMÉ, et si son âge atteint le délai sans signalement → signalé
      maintenant, UNE fois. Un lancement démarré dont l'étape revient à l'observation du lancement (marque retirée,
      rien produit) redevient non confirmé, avec son heure d'origine : il n'est pas relancé. Les appelants qui ne
      parlent que des NON CONFIRMÉS (verdict, lignes, notes) en tirent la vue `demarre` faux ; ils ne recalculent
      rien.
    ⑦ UNITÉ — minutes.
    ⑧ POURQUOI — D1 (BLOQUANT) de la relecture du 25-11-2026 (21h45) : sans mémoire, chaque passage redisait LANCER.
      N-63 (BLOQUANT) du RELU du 25-11-2026 (22h54) : après le délai, LANCER était redit à chaque délai, sans fin,
      en silence dès la troisième fois, et la place était rendue. Jugement du superviseur R-759 tour 2 : confirmé
      dès que l'observation diffère ; la place est gardée jusqu'à confirmation ou libération par un geste humain
      unique ; le délai ne sert plus qu'à notifier, une fois. N-64 en découle : une relecture longue n'est plus
      relancée pendant qu'elle tourne. N-72 (RELU du 25-11-2026, 23h29) : une commande --liberer rejouée (historique,
      dictée répétée) relançait aussitôt une étape relancée quelques minutes plus tôt ; le geste est réservé à une
      étape signalée À VÉRIFIER, comme le dit la ligne qui le propose. N-79 (RELU Cowork du 26-11-2026, 00h14) et
      superviseur R-759 tour 5 : un lancement ne prend fin que quand ce que SON exécutant doit produire apparaît, ou
      quand l'état rangé change (c'est l'adaptateur qui met l'un et l'autre dans l'observation) ; « en cours » n'est
      pas une fin : le lancement garde son heure de départ, dont l'échéance a besoin (A-1021). N-83 (RELU Cowork du
      26-11-2026, 01h19) : une relecture marquée « en cours » perdait la ressource et la durée de son lancement (son
      ENQUÊTER se taisait, sa place passait sur une autre ressource) ; propriété retenue par le superviseur R-759 :
      un lancement vivant, démarré ou non, garde sa ressource et son échéance — une seule place, celle du lancement.
    ⑨ CE QUI CLOCHE — un exécutant mort garde sa place jusqu'au geste humain : c'est voulu (un lancement deviné mort
      peut tourner encore), et la ligne À VÉRIFIER le dit une fois.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours, ou lève Arret.
      [sort: non]
    """
    memoire = dict((precedent or {}).get("lancements", {}))
    liberes = {}
    for x in liberer:
        if x not in memoire:
            raise Arret(f"--liberer={x} : aucun lancement de {x} en mémoire (lancements gardés : "
                        f"{', '.join(sorted(memoire)) or 'aucun'})")
        if memoire[x]["signale"] is None:
            raise Arret(f"--liberer={x} : le lancement de {x} n'a pas été signalé À VÉRIFIER (annoncé le "
                        f"{memoire[x]['heure'].astimezone(PARIS):%d-%m-%Y à %Hh%M}) : il peut tourner encore ; "
                        "attendre la ligne À VÉRIFIER")
        liberes[x] = memoire.pop(x)
    vivants, signales = {}, set()
    for e, v in memoire.items():
        if e not in etats:
            continue
        if etats[e]["etat"] == "en_cours":
            vivants[e] = dict(v, demarre=True)   # N-79 : l'exécutant a commencé ; le lancement dure, tel quel
            continue
        if observations.get(e) != v["observation"]:
            continue
        v = dict(v, demarre=False)
        if v["signale"] is None and (maintenant - v["heure"]).total_seconds() / 60 >= delai_min:
            v["signale"] = maintenant
            signales.add(e)
        vivants[e] = v
    return vivants, signales, liberes


def chemin_critique(planning, etats):
    """① RÔLE — Pour chaque étape non faite, la durée restante la plus longue d'elle jusqu'à la fin du planning.
    ② CONTEXTE D'APPEL — `passage`, pour ordonner les étapes prêtes.
    ③ ENTRÉE — `planning` ; `etats`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {id: heures} (la durée propre d'une étape faite compte 0).
      [rend: 1]
    ⑥ TRAITEMENT — reste(e) = durée(e) + max(reste(s) pour s qui dépend de e), itératif ; une étape retrouvée sur
      sa propre pile avant d'être calculée est un cycle → Arret.
    ⑦ UNITÉ — heures.
    ⑧ POURQUOI — remplir d'abord avec ce qui allonge la fin (méthode du chemin critique, CPM). Protégé SEUL contre
      un cycle (mineur 12 de la relecture du 25-11-2026 : sans `a_un_cycle`, il bouclait sans fin).
    ⑨ CE QUI CLOCHE — deuxième implémentation du chemin critique (voir ⑨ a du module) ; les durées sont déclarées.
    ⑩ EFFET — —
    ⑪ TERMINAISON — chaque étape est développée au plus une fois, sinon Arret : revient toujours.
      [sort: non]
    """
    succ = {e: [] for e in planning["etapes"]}
    for e, l in planning["etapes"].items():
        for d in l["deps"]:
            succ[d].append(e)
    reste, developpees = {}, set()
    for depart in planning["etapes"]:
        pile = [depart]
        while pile:
            n = pile[-1]
            if n in reste:
                pile.pop()
                continue
            manquants = [s for s in succ[n] if s not in reste]
            if manquants:
                if n in developpees:
                    raise Arret(f"cycle rencontré au chemin critique autour de {n}")
                developpees.add(n)
                pile.extend(manquants)
                continue
            propre = 0.0 if etats[n]["etat"] == "fait" else planning["etapes"][n]["duree"]
            reste[n] = propre + max([reste[s] for s in succ[n]] or [0.0])
            pile.pop()
    return reste


def places_prises(r, etats, vivants, mesure):
    """① RÔLE — LA notion « place prise » d'une ressource, calculée à cet endroit seulement (R-708), et la part de
      ces places qui est OBSERVÉE (et non seulement annoncée).
    ② CONTEXTE D'APPEL — `ressources_du_passage`, une fois par ressource ; tout le reste lit son résultat.
    ③ ENTRÉE — `r` : la ressource ; `etats` ; `vivants` (tous les lancements gardés, démarrés ou non, première
      valeur de `lancements_a_suivre`) ; `mesure` : le dict rendu par l'adaptateur pour `r` ({} s'il ne mesure rien).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : les places prises (entier ≥ 0) · les places OBSERVÉES (entier ≥ 0).
      [rend: 2]
    ⑥ TRAITEMENT — une étape qui a un lancement vivant compte sur la RESSOURCE DU LANCEMENT, jamais sur sa ressource
      observée ; une étape en cours sans lancement compte sur sa ressource observée. Prises = max(mesurée, étapes
      DISTINCTES lancées vivantes sur r ou en cours sans lancement sur r) : une étape en cours ET lancée compte UNE
      place (N-79), celle du lancement (N-83). Observées = les mêmes, moins les lancements non démarrés (annoncés,
      pas vus), ou l'occupation mesurée si elle est plus grande.
    ⑦ UNITÉ — places.
    ⑧ POURQUOI — superviseur R-759 (21h48) : un lancement non confirmé prend une place. Tour 2 : sur la ressource du
      LANCEMENT (une relecture annoncée occupe le relecteur, même si le planning a changé depuis) ; et seules les
      places OBSERVÉES font monter le palier (N-65 du RELU de 22h54 : le palier montait sur des lancements que le
      pilote avait lui-même annoncés, comme si TCP élargissait sa fenêtre à l'envoi et non à l'accusé de réception).
    ⑨ CE QUI CLOCHE — une étape lancée et déjà visible dans la mesure est comptée deux fois dans la somme, d'où le
      max et non la somme : le max peut SOUS-compter si la mesure voit d'autres occupants que nos étapes.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    en_cours = {e for e, v in etats.items() if v["ressource"] == r and v["etat"] == "en_cours" and e not in vivants}
    annoncees = {e for e, v in vivants.items() if v["ressource"] == r}
    vues = en_cours | {e for e in annoncees if vivants[e]["demarre"]}
    m = mesure.get("occupees")
    mesuree = m if isinstance(m, int) and not isinstance(m, bool) else 0
    return max(mesuree, len(en_cours | annoncees)), max(mesuree, len(vues))


def echeances(planning, etats, vivants, suivi, maintenant):
    """① RÔLE — LA règle de l'échéance (A-1021), à cet endroit seulement : dire quelles étapes EN COURS et quelles
      actions LANCÉES ont dépassé leur échéance, pour écrire « ENQUÊTER » en tête de la liste.
    ② CONTEXTE D'APPEL — `passage_sous_verrou`, après `lancements_a_suivre` et la mise à jour du suivi.
    ③ ENTRÉE — `planning` (durées : `duree` de chaque étape en heures, `attendues` {ressource: (minutes, source)}) ;
      `etats` ; `vivants` (tous les lancements gardés, démarrés ou non, première valeur de `lancements_a_suivre`) ;
      `suivi` ({id: {observation, depuis, en_cours_depuis}} de ce passage) ; `maintenant`.
    ④ CONDITIONS D'ENTRÉE — chaque étape de `etats` a son suivi.
    ⑤ SORTIE — UNE valeur : liste ordonnée (ordre du planning) de (id, texte de la ligne ENQUÊTER) des échéances
      DÉPASSÉES ; vide sinon.
      [rend: 1]
    ⑥ TRAITEMENT — UNE règle pour tout lancement vivant, démarré ou non (N-83) : départ = heure du lancement ; durée
      = durée attendue déclarée pour la ressource DU LANCEMENT (duree_attendue_<r>_min), sinon duree_h de l'étape
      (dite « estimée, duree_h ») ; l'état observé n'y change rien, il ne choisit que le mot « en cours » ou
      « lancée ». Étape en cours SANS lancement : départ = premier passage qui l'a vue en cours ; durée = duree_h.
      Échéance = départ + durée ; l'âge se compte en MINUTES ENTIÈRES (tronquées), l'unité même de l'affichage
      (N-85) ; dépassée quand l'âge > la durée. Une étape de durée 0 n'a pas d'échéance.
    ⑦ UNITÉ — minutes entières (durées affichées en h et min, par `duree_lisible`, même troncature).
    ⑧ POURQUOI — A-1021 (Jean-Luc, 25-11-2026 22h45) : « Si une étape qui est estimée à 30 minutes, au bout de 35
      n'a toujours pas bougé et ne déclenche pas ce qu'elle devrait déclencher, tu es forcément obligé de te poser la
      question et d'aller vérifier […] suivie au millimètre ». La RÈGLE vient de TENIR_UN_PLANNING.py (« chaque
      jalon a une échéance et une preuve, et un retard ne se tait pas ») ; son code n'est pas appelé : ce cœur ne
      dépend d'aucun programme d'un projet (A-1017).
    ⑨ CE QUI CLOCHE — les durées sont déclarées : une durée fausse fait enquêter trop tôt ou trop tard (la source est
      affichée). Une étape vue en cours pour la première fois par ce programme part de ce passage, pas de son vrai
      début. Le délai À VÉRIFIER (delai_de_confirmation_min) existe encore à côté : deux règles d'alerte sur un même
      lancement (son retrait demande l'accord de Jean-Luc). N-85 : depuis le tour 6, la borne se lit en minutes
      entières — l'ENQUÊTER vient à départ + durée + 1 min (16 min pour 15), et non plus dès la première seconde
      au-delà ; c'est le prix d'une ligne qui ne se contredit pas (« prévue 15 min, depuis 15 min »).
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    duree = duree_lisible
    out = []
    for e, l in planning["etapes"].items():
        if e not in etats:
            continue
        if e in vivants:
            v = vivants[e]
            depart = v["heure"]
            prevue, source = planning["attendues"].get(v["ressource"], (l["duree"] * 60, "estimée, duree_h de etapes.csv"))
            quoi = "en cours" if v["demarre"] else "lancée"
        elif etats[e]["etat"] == "en_cours":
            depart = suivi[e]["en_cours_depuis"]
            prevue, source, quoi = l["duree"] * 60, "duree_h de etapes.csv", "en cours"
        else:
            continue
        if depart is None or prevue <= 0:
            continue
        age = int((maintenant - depart).total_seconds() // 60)
        if age > prevue:
            bouge = suivi[e]["depuis"].astimezone(PARIS)
            out.append((e, f"ENQUÊTER {e} : prévue {duree(prevue)} ({source}), {quoi} depuis {duree(age)} (départ le "
                           f"{depart.astimezone(PARIS):%d-%m-%Y à %Hh%M}), rien n'a bougé depuis le {bouge:%d-%m-%Y à %Hh%M}"
                           " — aller vérifier ce qui se passe"))
    return out


def duree_lisible(minutes):
    """① RÔLE — Écrire une durée en minutes comme on la dit : « 15 min », « 1 h 30 ».
    ② CONTEXTE D'APPEL — `echeances`, pour la ligne ENQUÊTER.
    ③ ENTRÉE — `minutes` (nombre ≥ 0).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — UNE règle : minutes entières TRONQUÉES ; moins d'une heure → « N min », sinon heures entières et
      minutes sur deux chiffres.
    ⑦ UNITÉ — minutes (entières, tronquées : l'unité de la comparaison de `echeances`).
    ⑧ POURQUOI — la ligne ENQUÊTER est lue par une personne (A-1021). N-85 (RELU Cowork du 26-11-2026, 01h19) : on
      arrondissait sous 1 h et tronquait au-delà, et à 15 min 01 s la ligne disait « prévue 15 min, lancée depuis
      15 min » ; comparer et afficher dans la même unité ôte la contradiction.
    ⑨ CE QUI CLOCHE — 59,6 min s'écrit « 59 min ».
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    m = int(minutes)
    if m >= 60:
        return f"{m // 60} h {m % 60:02d}"
    return f"{m} min"


def suivre(etats, observations, precedent, maintenant):
    """① RÔLE — Tenir, pour chaque étape, depuis quand son observation n'a pas bougé et depuis quand elle est en cours.
    ② CONTEXTE D'APPEL — `passage_sous_verrou`, une fois ; lu par `echeances`, écrit dans l'état.
    ③ ENTRÉE — `etats` ; `observations` ({id: texte de `observation_de`}) ; `precedent` ; `maintenant`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {id: {observation, depuis (datetime), en_cours_depuis (datetime ou None)}}.
      [rend: 1]
    ⑥ TRAITEMENT — observation identique à celle gardée → `depuis` gardé, sinon `maintenant` ; étape en cours →
      `en_cours_depuis` gardé s'il existe, sinon `maintenant` ; pas en cours → None.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-1021 : la ligne ENQUÊTER dit « rien n'a bougé depuis <heure> », et une étape en cours qu'aucun
      LANCER n'a annoncée a besoin d'une heure de départ.
    ⑨ CE QUI CLOCHE — un état écrit par l'ancien code n'a pas de suivi : le premier passage part de lui-même.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    avant = (precedent or {}).get("suivi", {})
    out = {}
    for e in etats:
        a = avant.get(e)
        depuis = a["depuis"] if a and a["observation"] == observations[e] else maintenant
        en_cours = (a["en_cours_depuis"] if a and a["en_cours_depuis"] else maintenant) if etats[e]["etat"] == "en_cours" else None
        out[e] = {"observation": observations[e], "depuis": depuis, "en_cours_depuis": en_cours}
    return out


def ressources_du_passage(planning, mes, etats, vivants, precedent):
    """① RÔLE — Pour chaque ressource : capacité, places prises, palier (AIMD), places libres, et ce qui n'a pas pu
      être mesuré.
    ② CONTEXTE D'APPEL — `passage`.
    ③ ENTRÉE — `planning` ; `mes` (mesures de l'adaptateur) ; `etats` ; `vivants` (tous les lancements gardés) ;
      `precedent`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {ressource: {capacite, palier, prises, observees, libres, bloquee, mesure_impossible,
      refus_illisible, dernier_refus, raison, detail, source}}.
      [rend: 1]
    ⑥ TRAITEMENT — capacité = min(déclarée, mesurée si l'adaptateur en rend une) ; mesurée 0 → ressource BLOQUÉE
      (palier 0). Palier : premier passage → palier initial ; sinon, partant du palier précédent : nouveau refus
      observé (une heure de refus postérieure au dernier refus déjà vu) → divisé par deux (au moins 1) ; sinon
      ressource pleine d'étapes OBSERVÉES (places observées ≥ palier précédent) → + pas ; sinon inchangé ; refus
      illisibles (None) → inchangé et mesure impossible ; borné à [1, capacité]. Libres = palier − prises (≥ 0),
      et 0 quand l'occupation n'a pas pu être mesurée.
    ⑦ UNITÉ — places.
    ⑧ POURQUOI — jugement du superviseur R-759 : la montée « au débit » n'avait pas de signal à cette échelle et
      oscillait selon la fréquence des passages (D3) ; AIMD (contrôle de congestion de TCP : montée additive, recul
      multiplicatif) ne lit que deux faits observables : la ressource est pleine, un refus est arrivé. D4 : le refus
      est un CUMUL horodaté, comparé à la dernière heure vue, jamais un compte qui pourrait redescendre.
      Mineur 10 : capacité mesurée 0 = BLOQUÉE, pas « éveillé pour toujours ». N-65 du RELU du 25-11-2026 (22h54) :
      ne monter que sur des places observées (voir `places_prises`). N-70 : « libres 3 » à côté de « MESURE
      IMPOSSIBLE » se contredisait ; une place qu'on n'a pas pu mesurer n'est pas libre.
    ⑨ CE QUI CLOCHE — voir ⑨ e et f du module.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    sortie = {}
    for r, l in planning["ressources"].items():
        m = mes.get(r, {})
        cap = l["capacite"]
        mc = m.get("capacite")
        if isinstance(mc, int) and not isinstance(mc, bool):
            cap = min(cap, max(0, mc))
        prises, observees = places_prises(r, etats, vivants, m)
        prev = (precedent or {}).get("ressources", {}).get(r)
        dernier_prec = prev["dernier_refus"] if prev else None
        signal = "refus" in m
        refus_illisible, refus = False, []
        if signal:
            try:
                refus = [datetime.datetime.fromisoformat(t) for t in m["refus"]]
                if any(t.tzinfo is None for t in refus):
                    raise ValueError("heure de refus sans fuseau")
            except (TypeError, ValueError):
                refus_illisible, refus = True, []
        avant = datetime.datetime.fromisoformat(dernier_prec) if dernier_prec else None
        nouveaux = [t for t in refus if prev is not None and (avant is None or t > avant)]
        dernier = max(refus + ([avant] if avant else [])).isoformat() if (refus or avant) else None
        if cap <= 0:
            palier, raison = 0, "capacité mesurée 0 : ressource BLOQUÉE"
        elif prev is None:
            palier, raison = l["palier_initial"], "premier passage : palier initial"
        elif refus_illisible:
            palier, raison = prev["palier"], "refus illisibles : palier gelé (mesure impossible)"
        elif nouveaux:
            palier, raison = prev["palier"] // 2, (f"{len(nouveaux)} nouveau(x) refus observé(s), le dernier à "
                                                   f"{max(nouveaux).isoformat()} : palier ÷ 2")
        elif observees >= prev["palier"]:
            palier, raison = prev["palier"] + l["pas"], (f"pleine d'étapes OBSERVÉES ({observees}/{prev['palier']}) "
                                                         f"sans nouveau refus : + {l['pas']}")
        else:
            palier, raison = prev["palier"], (f"pas pleine d'étapes observées ({observees}/{prev['palier']}, "
                                              f"{prises - observees} annoncée(s) non confirmée(s)) : inchangé")
        if cap > 0:
            palier = max(1, min(cap, palier))
        if not signal:
            raison += " (aucun signal de refus pour cette ressource)"
        elif not refus_illisible:
            raison += f" ({len(refus)} refus horodaté(s) lu(s), dernier vu : {dernier or 'aucun'})"
        impossible = "occupees" in m and m["occupees"] is None
        sortie[r] = {"capacite": cap, "palier": palier, "prises": prises, "observees": observees,
                     "libres": 0 if impossible else max(0, palier - prises),
                     "bloquee": cap <= 0, "mesure_impossible": impossible,
                     "refus_illisible": refus_illisible, "dernier_refus": dernier, "raison": raison,
                     "detail": m.get("detail", ""), "source": l["source"]}
    return sortie


def remplir(planning, etats, reste, ress, en_attente):
    """① RÔLE — Choisir les étapes à LANCER maintenant, et dire pour les autres pourquoi elles attendent.
    ② CONTEXTE D'APPEL — `passage`.
    ③ ENTRÉE — `planning` ; `etats` ; `reste` (chemin critique) ; `ress` (valeur de `ressources_du_passage`) ;
      `en_attente` (lancées non confirmées : jamais relancées).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la liste ordonnée des étapes à lancer · {id: raison} des étapes prêtes en file ·
      l'ensemble des étapes en file d'une ressource BLOQUÉE.
      [rend: 3]
    ⑥ TRAITEMENT — prête = a_faire, pas en attente de confirmation, dépendances faites ; tri par reste décroissant,
      puis ordre du fichier ; sans ressource → lancée ; ressource bloquée ou à la mesure impossible → en file ;
      sinon lancée tant qu'il reste des places libres.
    ⑦ UNITÉ — places.
    ⑧ POURQUOI — A-942 ② (Jean-Luc, 20-11-2026 12h55) : « les étapes prêtes […] dans l'ordre du chemin critique ;
      le Chat les lance jusqu'à la capacité ». Mineur 13 : le message « pleine » dit les places prises AVANT le
      passage et celles attribuées PENDANT.
    ⑨ CE QUI CLOCHE — une étape prend UNE place ; une étape qui en occupe plusieurs se déclare en plusieurs étapes.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    ordre = list(planning["etapes"])
    pretes = [e for e in ordre if etats[e]["etat"] == "a_faire" and e not in en_attente
              and all(etats[d]["etat"] == "fait" for d in planning["etapes"][e]["deps"])]
    pretes.sort(key=lambda e: (-reste[e], ordre.index(e)))
    attribuees = {r: 0 for r in ress}
    lancer, en_file, bloquees = [], {}, set()
    for e in pretes:
        r = etats[e]["ressource"]
        if not r:
            lancer.append(e)
        elif ress[r]["bloquee"]:
            en_file[e] = f"« {r} » BLOQUÉE : capacité mesurée 0"
            bloquees.add(e)
        elif ress[r]["mesure_impossible"]:
            en_file[e] = f"occupation de « {r} » non mesurée : rien n'y est lancé"
        elif attribuees[r] < ress[r]["libres"]:
            attribuees[r] += 1
            lancer.append(e)
        else:
            v = ress[r]
            en_file[e] = (f"« {r} » pleine au palier {v['palier']} : {v['prises']} place(s) prise(s) avant ce passage"
                          f" + {attribuees[r]} attribuée(s) à ce passage (capacité {v['capacite']})")
    return lancer, en_file, bloquees


def substituer(commande, racine, dossier, params):
    """① RÔLE — Remplacer {racine}, {dossier} et {param:CLE} dans une commande, en UN SEUL passage.
    ② CONTEXTE D'APPEL — `lancer_les_controles`, une fois par ligne de controles.csv.
    ③ ENTRÉE — `commande` (texte) ; `racine` ; `dossier` ; `params` (dict).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la commande remplacée · la liste des clés de paramètre absentes.
      [rend: 2]
    ⑥ TRAITEMENT — re.sub avec MOTIF_SUBSTITUTION : un texte inséré n'est jamais relu (une valeur qui contient
      « {param:X} » reste telle quelle).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — mineur 12 de la relecture du 25-11-2026 : la boucle « tant que {param: reste » ne s'arrêtait pas sur
      --param=X={param:X}.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — un passage : revient toujours.
      [sort: non]
    """
    manque = [m.group(1)[len("param:"):] for m in MOTIF_SUBSTITUTION.finditer(commande)
              if m.group(1).startswith("param:") and m.group(1)[len("param:"):] not in params]
    return MOTIF_SUBSTITUTION.sub(lambda m: valeur_de_la_marque(m, racine, dossier, params), commande), manque


def valeur_de_la_marque(m, racine, dossier, params):
    """① RÔLE — Le texte qui remplace UNE marque {racine}, {dossier} ou {param:CLE}.
    ② CONTEXTE D'APPEL — `substituer`, par re.sub, une fois par marque.
    ③ ENTRÉE — `m` : la marque trouvée par MOTIF_SUBSTITUTION ; `racine` ; `dossier` ; `params`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte de remplacement ; la marque elle-même si le paramètre manque.
      [rend: 1]
    ⑥ TRAITEMENT — racine, dossier, ou la valeur du paramètre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — voir ⑧ de `substituer`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    cle = m.group(1)
    if cle == "racine":
        return racine
    if cle == "dossier":
        return dossier
    return params.get(cle[len("param:"):], m.group(0))


def lancer_les_controles(planning, dossier, racine):
    """① RÔLE — Lancer chaque contrôle (de l'adaptateur puis de controles.csv) et lire son code.
    ② CONTEXTE D'APPEL — `passage` (sauf épreuves qui passent `controles=False`).
    ③ ENTRÉE — `planning` ; `dossier` ; `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de (nom, statut OK|ALERTE|IMPOSSIBLE, dernières lignes de sa sortie).
      [rend: 1]
    ⑥ TRAITEMENT — préparer la liste (nom, arguments ou None, raison) : contrôles de l'adaptateur, puis ceux de
      controles.csv (`substituer`, shlex.split) ; puis UNE seule boucle d'exécution : subprocess borné ; code 0 →
      OK, 3 → ALERTE, autre → IMPOSSIBLE ; un paramètre absent ou un contrôle déclaré impossible → IMPOSSIBLE.
    ⑦ UNITÉ — secondes (délai).
    ⑧ POURQUOI — R-708 : le cœur APPELLE les contrôles existants, il ne les recopie pas. Une seule boucle
      d'exécution (jugement du superviseur R-759).
    ⑨ CE QUI CLOCHE — la convention 0/3 est celle des contrôles de ce projet ; un contrôle qui rend 1 pour « alerte »
      sera dit IMPOSSIBLE, ce qui est le défaut prudent.
    ⑩ EFFET — ceux des commandes lancées.
    ⑪ TERMINAISON — chaque commande est tuée au bout de DELAI_CONTROLE_S.
      [sort: non]
    """
    a_lancer = []
    for item in planning.get("controles_adaptateur", []):
        if len(item) == 3:
            a_lancer.append((item[0], None, item[2]))
        else:
            a_lancer.append((item[0], list(item[1]), ""))
    for c in planning["controles"]:
        cmd, manque = substituer(c["commande"], racine, dossier, planning["params"])
        if manque:
            a_lancer.append((c["controle"], None, f"paramètre absent : {', '.join(manque)}"))
            continue
        try:
            a_lancer.append((c["controle"], shlex.split(cmd), ""))
        except ValueError as e:
            a_lancer.append((c["controle"], None, f"commande illisible : {e}"))
    out = []
    for nom, argv, raison in a_lancer:
        if argv is None:
            out.append((nom, "IMPOSSIBLE", raison))
            continue
        try:
            p = subprocess.run(argv, cwd=racine, capture_output=True, text=True, timeout=DELAI_CONTROLE_S)
            texte = (p.stdout + p.stderr).strip().splitlines()
            statut = {0: "OK", 3: "ALERTE"}.get(p.returncode, "IMPOSSIBLE")
            out.append((nom, statut, " / ".join(texte[-3:]) + (f" (code {p.returncode})" if statut == "IMPOSSIBLE" else "")))
        except (OSError, ValueError, subprocess.TimeoutExpired) as e:
            out.append((nom, "IMPOSSIBLE", f"{type(e).__name__} {e}"))
    return out


def verdict(etats, lancer, en_file, bloquees, en_attente):
    """① RÔLE — Dire RESTER ÉVEILLÉ ou PEUT S'ARRÊTER, avec la raison.
    ② CONTEXTE D'APPEL — `passage`.
    ③ ENTRÉE — `etats` ; `lancer` ; `en_file` ; `bloquees` (en file d'une ressource bloquée) ; `en_attente`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le mot (« RESTER ÉVEILLÉ » ou « PEUT S'ARRÊTER ») · la raison en une ligne.
      [rend: 2]
    ⑥ TRAITEMENT — tout fait → PEUT S'ARRÊTER (objectif atteint) ; une étape à lancer, en cours, lancée non
      confirmée, ou en file d'une ressource NON bloquée → RESTER ÉVEILLÉ ; sinon PEUT S'ARRÊTER, chaque étape
      restante nommée avec ce qu'elle attend. Dans TOUS les cas, les lancements déjà signalés À VÉRIFIER sont
      nommés à la fin de la raison.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-942 ② : ne s'arrêter que sur l'objectif atteint ou sur des étapes toutes bloquées, chacune nommée.
      Mineur 10 : une ressource à capacité mesurée 0 ne garde pas éveillé pour toujours. N-76 (RELU du 25-11-2026,
      23h29) : la raison taisait les À VÉRIFIER dès qu'une étape était à lancer ou en cours.
    ⑨ CE QUI CLOCHE — « en cours » chez un exécutant extérieur garde éveillé même s'il est mort : c'est à
      l'adaptateur de dire qu'une marque est périmée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    a_voir = [e for e, v in en_attente.items() if v["signale"] is not None]
    mot, raison = verdict_sans_les_a_verifier(etats, lancer, en_file, bloquees, en_attente)
    if a_voir:
        raison += f" — dont {len(a_voir)} À VÉRIFIER par quelqu'un : {', '.join(a_voir)}"
    return mot, raison


def verdict_sans_les_a_verifier(etats, lancer, en_file, bloquees, en_attente):
    """① RÔLE — Le mot et la raison du verdict, AVANT que `verdict` y ajoute les À VÉRIFIER.
    ② CONTEXTE D'APPEL — `verdict` seulement.
    ③ ENTRÉE — `etats`, `lancer`, `en_file`, `bloquees`, `en_attente` : les mêmes que `verdict`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le mot · la raison (sans les À VÉRIFIER).
      [rend: 2]
    ⑥ TRAITEMENT — voir ⑥ de `verdict`, dans cet ordre : tout fait · à lancer · en cours · lancées non confirmées ·
      file vivante · reste bloqué.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-76 : séparer le choix du mot de l'ajout des À VÉRIFIER, pour que cet ajout vale pour toutes les
      branches au lieu d'une seule.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    if all(v["etat"] == "fait" for v in etats.values()):
        return "PEUT S'ARRÊTER", "objectif atteint : toutes les étapes sont faites"
    if lancer:
        return "RESTER ÉVEILLÉ", f"{len(lancer)} étape(s) à lancer maintenant"
    cours = [e for e, v in etats.items() if v["etat"] == "en_cours"]
    if cours:
        return "RESTER ÉVEILLÉ", f"{len(cours)} étape(s) en cours : {', '.join(cours)}"
    if en_attente:
        return "RESTER ÉVEILLÉ", f"{len(en_attente)} étape(s) lancée(s), non encore confirmée(s) : {', '.join(en_attente)}"
    vivantes = [e for e in en_file if e not in bloquees]
    if vivantes:
        return "RESTER ÉVEILLÉ", f"{len(vivantes)} étape(s) prêtes en file d'une ressource : {', '.join(vivantes)}"
    restes = [f"{e} ({v['etat']}{' : ' + v['motif'] if v['motif'] else ''})" for e, v in etats.items()
              if v["etat"] in ("attend", "bloque", "pause")]
    restes += [f"{e} ({en_file[e]})" for e in bloquees]
    return "PEUT S'ARRÊTER", "plus rien ne peut avancer sans quelqu'un : " + ("; ".join(restes) or "étapes en attente de dépendances")


def etat_note(e, etats, lancer, en_attente, maintenant):
    """① RÔLE — Le texte d'état d'une étape tel qu'il est gardé et comparé d'un passage à l'autre.
    ② CONTEXTE D'APPEL — `passage`, pour le journal et l'état écrit.
    ③ ENTRÉE — `e` ; `etats` ; `lancer` ; `en_attente` (lancements non confirmés) ; `maintenant` (heure du passage,
      qui devient l'heure du lancement pour une étape de `lancer`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « lancee@AAAA-MM-JJTHH:MM » (annoncée, pas confirmée ; heure de Paris du lancement) ·
      « lancee_a_verifier@AAAA-MM-JJTHH:MM » (non confirmée, délai atteint, signalée) · sinon l'état avec son motif.
      [rend: 1]
    ⑥ TRAITEMENT — dans cet ordre : lancée à ce passage (heure = `maintenant`) · non confirmée signalée · non
      confirmée (heure = celle du lancement gardé) · état.
    ⑦ UNITÉ — minutes (l'heure est écrite à la minute).
    ⑧ POURQUOI — un LANCER est un changement (notifié une fois) ; le signalement À VÉRIFIER en est un, UNE fois
      (N-63 du RELU du 25-11-2026, 22h54) ; leur répétition à l'identique n'en est pas un. N-71 (RELU du 25-11-2026,
      23h29) : une étape confirmée à tort puis redite LANCER gardait le texte « lancee » et la redite passait SANS
      notification ; avec l'heure du lancement, toute redite de LANCER est un changement notifié.
    ⑨ CE QUI CLOCHE — deux lancements de la même étape dans la même minute (confirmé puis relancé à moins d'une
      minute d'écart) donneraient le même texte : ce n'est possible qu'avec des passages espacés de moins d'une
      minute.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    if e in lancer:
        return f"lancee@{maintenant.astimezone(PARIS):%Y-%m-%dT%H:%M}"
    if e in en_attente:
        mot = "lancee_a_verifier" if en_attente[e]["signale"] is not None else "lancee"
        return f"{mot}@{en_attente[e]['heure'].astimezone(PARIS):%Y-%m-%dT%H:%M}"
    return etats[e]["etat"] + (":" + etats[e]["motif"] if etats[e]["motif"] else "")


def changements(precedent, notes, ress, verdict_txt, actions, empreinte):
    """① RÔLE — Le journal des changements : ce qui a bougé depuis le passage précédent.
    ② CONTEXTE D'APPEL — `passage`.
    ③ ENTRÉE — `precedent` ({} au premier passage) ; `notes` ({id: texte de `etat_note`}) ; `ress` ; `verdict_txt` ;
      `actions` (liste triée des étapes à lancer, lancées non confirmées ou en file) ; `empreinte` du planning.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de (objet, avant, après) ; vide si rien n'a changé.
      [rend: 1]
    ⑥ TRAITEMENT — comparer l'état de chaque étape, le palier de chaque ressource, le verdict, la liste d'actions,
      l'empreinte des fichiers du planning ; une étape apparue ou disparue est un changement.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-1019 (Jean-Luc, 20h58) : « des points d'avancement à chaque fois qu'il y a un changement » ;
      jamais quand rien ne change. Mineur 9 : un planning modifié ou une liste d'actions changée se notifient.
    ⑨ CE QUI CLOCHE — au premier passage, tout est « changé » depuis « — ».
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    p = precedent or {}
    av_e = p.get("etapes", {})
    av_r = {r: v["palier"] for r, v in p.get("ressources", {}).items()}
    out = []
    for e in sorted(set(av_e) | set(notes)):
        a, b = av_e.get(e, "—"), notes.get(e, "—")
        if a != b:
            out.append((e, a, b))
    for r in sorted(set(av_r) | set(ress)):
        a, b = av_r.get(r, "—"), ress[r]["palier"] if r in ress else "—"
        if a != b:
            out.append((f"palier {r}", a, b))
    if p.get("verdict", "—") != verdict_txt:
        out.append(("verdict", p.get("verdict", "—"), verdict_txt))
    if p and p.get("actions", []) != actions:
        out.append(("actions", ",".join(p.get("actions", [])) or "—", ",".join(actions) or "—"))
    if p and p.get("empreinte", "") != empreinte:
        out.append(("planning", p.get("empreinte", "") or "—", empreinte))
    return out


def depot_git_englobant(chemin):
    """① RÔLE — Dire si un dossier est à l'intérieur d'un dépôt git (lui-même ou un de ses parents porte « .git »).
    ② CONTEXTE D'APPEL — `passage`, pour refuser un dossier d'état placé dans un dépôt.
    ③ ENTRÉE — `chemin` : un dossier (absolu), existant ou non.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dossier qui porte « .git », ou "" s'il n'y en a pas.
      [rend: 1]
    ⑥ TRAITEMENT — remonte de parent en parent jusqu'à la racine du disque.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-69 du RELU du 25-11-2026 (22h54) : un état écrit dans un clone que la tâche planifiée refait à
      chaque passage est perdu, et D1 (LANCER redit) revient en entier.
    ⑨ CE QUI CLOCHE — ne voit pas un dossier synchronisé par un autre moyen (un dossier partagé effacé) : seul git
      est reconnu.
    ⑩ EFFET — lit l'existence de fichiers.
    ⑪ TERMINAISON — chaque tour remonte d'un niveau : revient toujours.
      [sort: non]
    """
    c = os.path.abspath(chemin)
    while True:
        if os.path.exists(os.path.join(c, ".git")):
            return c
        parent = os.path.dirname(c)
        if parent == c:
            return ""
        c = parent


def passage(dossier, maintenant, params=None, dossier_etat=None, ecrire=True, controles=True, liberer=()):
    """① RÔLE — Un passage complet du pilotage (voir ⑥ du module).
    ② CONTEXTE D'APPEL — `main` ; les épreuves, avec une heure imposée et `ecrire` au choix.
    ③ ENTRÉE — `dossier` du planning ; `maintenant` (datetime avec fuseau) ; `params` (dict, --param) ;
      `dossier_etat` (OBLIGATOIRE, --etat) ; `ecrire` ; `controles` (False : ne lance aucun contrôle) ; `liberer`
      (identifiants, --liberer).
    ④ CONDITIONS D'ENTRÉE — voir ④ du module ; `dossier_etat` donné et hors de tout dépôt git.
    ⑤ SORTIE — UNE valeur : dict {lignes, code, lancer, en_file, vivants (tous les lancements gardés, avec
      `demarre`), en_attente (la vue des non confirmés), enqueter, a_verifier, liberes, verdict, raison, changements,
      etats, ressources, controles}. La clé « demarres » du tour 5 a disparu avec la 4e sortie de
      `lancements_a_suivre` (N-83).
      [rend: 1]
    ⑥ TRAITEMENT — voir ⑥ du module ; l'état n'est écrit qu'après que toutes les lignes sont calculées. Code : 3 si
      un contrôle ALERTE (même s'il y a aussi de l'impossible, alors annoncé sur la même ligne CODE) ; sinon 4 si
      un contrôle ou une mesure est impossible ; sinon 0.
    ⑦ UNITÉ — heures, minutes, places.
    ⑧ POURQUOI — séparer le passage de `main` permet de l'éprouver avec une heure fabriquée. D6 partie 2 de la
      relecture du 25-11-2026 : le code 4 masquait une vraie ALERTE. N-69 du RELU de 22h54 : l'état est obligatoire
      et refusé dans un dépôt git. N-73 du RELU de 23h29 : deux passages simultanés lançaient tous deux ; le passage
      qui écrit se fait sous un verrou exclusif du dossier d'état.
    ⑨ CE QUI CLOCHE — voir ⑨ du module.
    ⑩ EFFET — avec `ecrire` : crée le dossier d'état et VERROU.lock, puis les trois fichiers du dossier d'état (voir
      ⑩ du module).
    ⑪ TERMINAISON — voir ⑪ du module ; lève Arret si rien ne peut être conclu, ou si un autre passage tient le
      verrou (jamais d'attente).
      [sort: non]
    """
    if not dossier_etat:
        raise Arret("--etat=DOSSIER est obligatoire : la mémoire des lancements y vit, hors de tout dépôt")
    dossier = os.path.abspath(dossier)
    dossier_etat = os.path.abspath(dossier_etat)
    git = depot_git_englobant(dossier_etat)
    if git:
        raise Arret(f"le dossier d'état {dossier_etat} est dans le dépôt git {git} : un clone refait perdrait la "
                    "mémoire des lancements ; choisir un dossier hors de tout dépôt")
    verrou = prendre_le_verrou(dossier_etat) if ecrire else None
    try:
        return passage_sous_verrou(dossier, maintenant, params, dossier_etat, ecrire, controles, liberer)
    finally:
        if verrou is not None:
            verrou.close()   # fermer le fichier rend le verrou, même si le passage a levé Arret


def prendre_le_verrou(dossier_etat):
    """① RÔLE — Prendre un verrou EXCLUSIF sur le dossier d'état pour un passage qui écrit.
    ② CONTEXTE D'APPEL — `passage`, avant `passage_sous_verrou`, quand `ecrire` est vrai ; `passage` ferme le
      fichier rendu à la fin (normale ou par exception), ce qui rend le verrou.
    ③ ENTRÉE — `dossier_etat` : chemin absolu du dossier d'état.
    ④ CONDITIONS D'ENTRÉE — système qui connaît fcntl.flock (Linux, macOS).
    ⑤ SORTIE — UNE valeur : le fichier VERROU.lock ouvert, verrou tenu tant qu'il reste ouvert.
      [rend: 1]
    ⑥ TRAITEMENT — crée le dossier s'il manque, ouvre VERROU.lock, prend fcntl.flock(LOCK_EX | LOCK_NB) ; verrou
      déjà tenu → ferme le fichier et lève Arret.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — N-73 du RELU Cowork du 25-11-2026 (23h29) : la tâche planifiée et un passage à la main au même
      moment lisaient tous deux l'état d'avant, et disaient tous deux LANCER A1 (prouvé avec un adaptateur lent).
      Arrêter le second plutôt que le faire attendre : il relirait sinon un état que le premier vient de changer,
      sans que personne le voie.
    ⑨ CE QUI CLOCHE — flock ne vaut que pour les passages d'une même machine sur un disque local ; sur un dossier
      réseau partagé entre deux machines, il peut ne rien exclure. Le fichier VERROU.lock reste (vide) : c'est voulu,
      l'effacer ouvrirait une course.
    ⑩ EFFET — crée le dossier d'état et VERROU.lock (vide).
    ⑪ TERMINAISON — LOCK_NB : n'attend jamais ; revient toujours, ou lève Arret.
      [sort: non]
    """
    try:
        os.makedirs(dossier_etat, exist_ok=True)
        f = open(os.path.join(dossier_etat, NOM_VERROU), "a", encoding="utf-8")
    except OSError as e:
        raise Arret(f"dossier d'état {dossier_etat} inutilisable pour le verrou : {e}")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        f.close()
        raise Arret(f"un autre passage tient le verrou {os.path.join(dossier_etat, NOM_VERROU)} : deux passages "
                    "à la fois liraient le même état et lanceraient deux fois ; relancer après la fin de l'autre")
    return f


def passage_sous_verrou(dossier, maintenant, params, dossier_etat, ecrire, controles, liberer):
    """① RÔLE — Le corps d'un passage (voir ⑥ du module), une fois l'état vérifié et, s'il écrit, le verrou pris.
    ② CONTEXTE D'APPEL — `passage` seulement.
    ③ ENTRÉE — `dossier`, `maintenant`, `params`, `dossier_etat`, `ecrire`, `controles`, `liberer` : les mêmes que
      `passage`, chemins déjà absolus.
    ④ CONDITIONS D'ENTRÉE — `dossier_etat` hors de tout dépôt git ; avec `ecrire`, le verrou tenu par l'appelant.
    ⑤ SORTIE — UNE valeur : celle de `passage`.
      [rend: 1]
    ⑥ TRAITEMENT — voir ⑥ de `passage`.
    ⑦ UNITÉ — heures, minutes, places.
    ⑧ POURQUOI — N-73 : séparer le corps pour qu'il tourne en entier sous le verrou, lecture de l'état comprise.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — voir ⑩ de `passage`.
    ⑪ TERMINAISON — voir ⑪ du module ; lève Arret si rien ne peut être conclu.
      [sort: non]
    """
    planning = lire_planning(dossier, params)
    precedent = lire_l_etat_precedent(os.path.join(dossier_etat, NOM_ETAT), maintenant)
    obs, mes, racine = observer(planning, dossier)
    etats = etats_finals(planning, obs)
    observations = {e: observation_de(obs[e]) for e in etats}
    vivants, signales, liberes = lancements_a_suivre(etats, observations, precedent, maintenant,
                                                     planning["delai_min"], liberer)
    en_attente = {e: v for e, v in vivants.items() if not v["demarre"]}   # vue : les non confirmés, rien recalculé
    suivi = suivre(etats, observations, precedent, maintenant)
    enqueter = echeances(planning, etats, vivants, suivi, maintenant)
    reste = chemin_critique(planning, etats)
    ress = ressources_du_passage(planning, mes, etats, vivants, precedent)
    lancer, en_file, bloquees = remplir(planning, etats, reste, ress, en_attente)
    ctl = lancer_les_controles(planning, dossier, racine) if controles else []
    mot, raison = verdict(etats, lancer, en_file, bloquees, en_attente)
    notes = {e: etat_note(e, etats, lancer, en_attente, maintenant) for e in etats}
    actions = sorted(set(lancer) | set(en_attente) | set(en_file))
    chg = [(f"libération {e}", f"lancée le {v['heure'].astimezone(PARIS):%d-%m-%Y à %Hh%M}", "libérée à la main")
           for e, v in liberes.items()]
    chg += changements(precedent, notes, ress, mot, actions, planning["empreinte"])
    avant_enq = set((precedent or {}).get("enqueter", []))
    chg += [(f"enquêter {e}", "—", "échéance dépassée") for e, _ in enqueter if e not in avant_enq]
    chg += [(f"enquêter {e}", "échéance dépassée", "—") for e in sorted(avant_enq - {x for x, _ in enqueter})]
    L = rediger(planning, dossier, maintenant, etats, reste, ress, lancer, en_file, en_attente, signales, ctl, chg,
                mot, raison)
    L[1:1] = [t for _, t in enqueter]   # A-1021 : ENQUÊTER EN TÊTE, à chaque passage tant que l'échéance est dépassée
    alerte = any(s == "ALERTE" for _, s, _ in ctl)
    impossible = any(s == "IMPOSSIBLE" for _, s, _ in ctl) or \
        any(v["mesure_impossible"] or v["refus_illisible"] for v in ress.values())
    code = 3 if alerte else 4 if impossible else 0
    if alerte and impossible:
        L.insert(-2, "CODE 3 : un contrôle ALERTE ET un contrôle ou une mesure IMPOSSIBLE — les deux sont à lire")
    if ecrire:
        os.makedirs(dossier_etat, exist_ok=True)
        lancements = {e: v for e, v in vivants.items()}
        lancements.update({e: {"heure": maintenant, "observation": observations[e], "ressource": etats[e]["ressource"],
                               "signale": None} for e in lancer})
        nouvel = {"heure": maintenant.isoformat(), "verdict": mot, "etapes": notes, "actions": actions,
                  "empreinte": planning["empreinte"],
                  "lancements": {e: {"heure": v["heure"].isoformat(), "observation": v["observation"],
                                     "ressource": v["ressource"],
                                     "signale": v["signale"].isoformat() if v["signale"] else None}
                                 for e, v in lancements.items()},
                  "ressources": {r: {"palier": v["palier"], "dernier_refus": v["dernier_refus"]} for r, v in ress.items()},
                  "suivi": {e: {"observation": v["observation"], "depuis": v["depuis"].isoformat(),
                                "en_cours_depuis": v["en_cours_depuis"].isoformat() if v["en_cours_depuis"] else None}
                            for e, v in suivi.items()},
                  "enqueter": [e for e, _ in enqueter]}
        remplacer(os.path.join(dossier_etat, NOM_ETAT), json.dumps(nouvel, ensure_ascii=False, indent=1) + "\n")
        remplacer(os.path.join(dossier_etat, NOM_ACTIONS), "\n".join(L) + "\n")
        journal = os.path.join(dossier_etat, NOM_JOURNAL)
        neuf = not os.path.exists(journal)
        with open(journal, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter=";")
            if neuf:
                w.writerow(["heure", "objet", "avant", "apres"])
            for objet, a, b in chg:
                w.writerow([maintenant.isoformat(), objet, a, b])
    return {"lignes": L, "code": code, "lancer": lancer, "en_file": en_file, "en_attente": en_attente,
            "vivants": vivants, "enqueter": [e for e, _ in enqueter],
            "a_verifier": sorted(signales), "liberes": sorted(liberes), "verdict": mot, "raison": raison,
            "changements": chg, "etats": etats, "ressources": ress, "controles": ctl}


def rediger(planning, dossier, maintenant, etats, reste, ress, lancer, en_file, en_attente, signales, ctl, chg,
            mot, raison):
    """① RÔLE — Écrire les lignes du passage, dans l'ordre fixe du ⑤ du module.
    ② CONTEXTE D'APPEL — `passage`, une fois.
    ③ ENTRÉE — `planning` ; `dossier` ; `maintenant` ; `etats` ; `reste` (chemin critique) ; `ress` ; `lancer` ;
      `en_file` ; `en_attente` (lancements non confirmés) ; `signales` (signalés À VÉRIFIER à ce passage) ; `ctl`
      (contrôles) ; `chg` (changements) ; `mot` et `raison` du verdict.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des lignes, finissant par VERDICT puis NOTIFIER.
      [rend: 1]
    ⑥ TRAITEMENT — une ligne par fait ; un lancement non confirmé a sa ligne LANCÉE NON CONFIRMÉE (date et heure
      complètes) à chaque passage, et une ligne À VÉRIFIER au seul passage où le délai est atteint.
    ⑦ UNITÉ — heures, places.
    ⑧ POURQUOI — N-63 du RELU du 25-11-2026 (22h54) : une ligne qui commence par « LANCER » est exécutée par
      celui qui pilote ; un lancement non confirmé ne s'écrit donc JAMAIS « LANCER ». N-68 : l'heure affichée porte
      sa date. D2 : la contradiction est affichée.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    h = maintenant.strftime("%d-%m-%Y %Hh%M")
    L = [f"PILOTAGE {planning['params'].get('nom', os.path.basename(dossier))} — {h} (Paris)"]
    for objet, a, b in chg:
        L.append(f"CHANGEMENT {objet} : {a} → {b}")
    for e, v in etats.items():
        if v["contradiction"]:
            L.append(f"CONTRADICTION {e} — {v['contradiction']}")

    for e in lancer:
        v = etats[e]
        L.append(f"LANCER {e} — {v['action']} — par {v['executant'] or '?'} sur {v['ressource'] or 'aucune ressource'}"
                 f" (chemin critique : {reste[e]:g} h restantes)")
    for e, v in en_attente.items():
        quand = f"{v['heure'].astimezone(PARIS):%d-%m-%Y à %Hh%M}"
        if e in signales:
            L.append(f"À VÉRIFIER {e} — lancée le {quand}, rien observé de neuf après {planning['delai_min']:g} min : "
                     f"vérifier qu'elle tourne ; si elle est morte, la libérer par --liberer={e} (dit une seule fois)")
        L.append(f"LANCÉE NON CONFIRMÉE {e} — annoncée le {quand}, observation inchangée — ne pas relancer — occupe "
                 f"une place de {v['ressource'] or 'aucune ressource'}"
                 + (f" — signalée À VÉRIFIER le {v['signale'].astimezone(PARIS):%d-%m-%Y à %Hh%M}"
                    if v["signale"] is not None and e not in signales else ""))
    for e, v in etats.items():
        if v["etat"] == "en_cours":
            L.append(f"EN COURS {e} — {v['detail'] or v['action']}")
    for e, pourquoi in en_file.items():
        L.append(f"EN FILE {e} — {pourquoi}")
    for e, v in etats.items():
        if v["etat"] == "attend":
            L.append(f"ATTEND {e} — {v['motif']}")
        elif v["etat"] == "bloque":
            L.append(f"BLOQUÉE {e} — {v['motif']}")
        elif v["etat"] == "pause":
            L.append(f"EN PAUSE {e}{' — ' + v['motif'] if v['motif'] else ''}")
    for r, v in ress.items():
        if v["bloquee"]:
            L.append(f"RESSOURCE BLOQUÉE {r} — capacité mesurée 0 — {v['detail']}")
        if v["mesure_impossible"] or v["refus_illisible"]:
            quoi = " et ".join(q for q, oui in (("occupation", v["mesure_impossible"]), ("refus", v["refus_illisible"])) if oui)
            L.append(f"MESURE IMPOSSIBLE {r} ({quoi}) — {v['detail'] or 'non mesurée'}")
        L.append(f"PALIER {r} : {v['palier']} (capacité {v['capacite']}, prises {v['prises']}, libres {v['libres']})"
                 f" — {v['raison']} — source : {v['source']}")
    for nom, statut, texte in ctl:
        L.append(f"CONTRÔLE {nom} : {statut} — {texte}")
    L.append(f"VERDICT {mot} — {raison}")
    L.append("NOTIFIER : " + ("oui, " + str(len(chg)) + " changement(s)" if chg else "non, rien n'a changé"))
    return L


def remplacer(chemin, texte):
    """① RÔLE — Écrire un fichier entier d'un coup ; la seule écriture de fichier entier du programme.
    ② CONTEXTE D'APPEL — `passage`, deux fois (état, actions).
    ③ ENTRÉE — `chemin` : le fichier ; `texte` : son contenu.
    ④ CONDITIONS D'ENTRÉE — le dossier est inscriptible.
    ⑤ SORTIE — —
      [rend: rien]
    ⑥ TRAITEMENT — écrire à côté (« .tmp ») puis os.replace.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un lecteur ne voit jamais un fichier à moitié écrit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit le fichier.
    ⑪ TERMINAISON — revient toujours, ou lève OSError.
      [sort: non]
    """
    with open(chemin + ".tmp", "w", encoding="utf-8") as f:
        f.write(texte)
    os.replace(chemin + ".tmp", chemin)


def main(argv):
    """① RÔLE — Ligne de commande du programme de pilotage : lire les options, faire un passage, afficher.
    ② CONTEXTE D'APPEL — lancé par celui qui pilote (voir ② du module).
    ③ ENTRÉE — `argv` : la ligne de commande (voir ③ du module).
    ④ CONDITIONS D'ENTRÉE — un seul argument sans « -- » : le dossier du planning ; --etat obligatoire.
    ⑤ SORTIE — UNE valeur : le code de sortie (0, 2, 3 ou 4).
      [rend: 1]
    ⑥ TRAITEMENT — options, `passage`, affichage en lignes ou en JSON ; le JSON rend aussi les lancements non
      confirmés (`non_confirmees`), ceux signalés à ce passage (`a_verifier`) et les libérés (`liberes`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — séparer la ligne de commande du passage, que les épreuves appellent. N-67 du RELU du 25-11-2026
      (22h54) : le JSON ne distinguait pas un lancement déjà parti d'un premier lancement.
    ⑨ CE QUI CLOCHE — une erreur imprévue devient ARRET code 2, jamais un Traceback muet.
    ⑩ EFFET — affiche ; les écritures de `passage`.
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = [a for a in argv[1:] if a.startswith("--")]
    if len(args) != 1:
        print("USAGE : PILOTER_UN_PLANNING.py <dossier du planning> --etat=DOSSIER [--maintenant=AAAA-MM-JJTHH:MM]"
              " [--param=CLE=VALEUR ...] [--liberer=ETAPE ...] [--json] [--sans-ecrire]")
        return 2
    maintenant, etat, params, en_json, ecrire, liberer = datetime.datetime.now(PARIS), None, {}, False, True, []
    try:
        for o in opts:
            if o.startswith("--maintenant="):
                maintenant = datetime.datetime.strptime(o.split("=", 1)[1], "%Y-%m-%dT%H:%M").replace(tzinfo=PARIS)
            elif o.startswith("--etat="):
                etat = o.split("=", 1)[1]
            elif o.startswith("--param=") and "=" in o[len("--param="):]:
                k, v = o[len("--param="):].split("=", 1)
                params[k] = v
            elif o.startswith("--liberer=") and o[len("--liberer="):]:
                liberer.append(o[len("--liberer="):])
            elif o == "--json":
                en_json = True
            elif o == "--sans-ecrire":
                ecrire = False
            else:
                raise Arret(f"option inconnue : {o}")
        r = passage(args[0], maintenant, params, etat, ecrire, liberer=liberer)
    except Arret as e:
        print(f"ARRET {maintenant:%d-%m-%Y %Hh%M} — {e} — rien n'est conclu, rien n'est écrit")
        return 2
    except Exception as e:
        print(f"ARRET {maintenant:%d-%m-%Y %Hh%M} — erreur imprévue : {type(e).__name__} {e} — rien n'est conclu")
        return 2
    if en_json:
        sortie = {k: r[k] for k in ("code", "lancer", "en_file", "a_verifier", "liberes", "verdict", "raison",
                                    "changements", "controles", "enqueter")}
        sortie["non_confirmees"] = {e: {"heure": v["heure"].isoformat(), "ressource": v["ressource"],
                                        "signale": v["signale"].isoformat() if v["signale"] else None}
                                    for e, v in r["en_attente"].items()}
        print(json.dumps(sortie, ensure_ascii=False, indent=1))
    else:
        print("\n".join(r["lignes"]))
    return r["code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
