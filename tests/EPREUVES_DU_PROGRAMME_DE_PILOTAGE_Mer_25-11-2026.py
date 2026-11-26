#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Épreuves du programme de pilotage (cœur générique, comptage des défauts, adaptateur CAC 40). Mer 25-11-2026,
corrigées le même soir après la relecture à mandat inversé (21h45) et le superviseur R-759 (21h48).
Simulation uniquement : aucun ordre réel, jamais.

① RÔLE — Prouver que programmes/PILOTER_UN_PLANNING.py rend la BONNE liste d'actions sur un planning factice sans
  rapport avec le CAC 40 (un déménagement) ; que chaque correction du 25-11-2026 au soir (mémoire des lancements,
  observé contre déclaré, AIMD, préfixes de preuve, code 3 sur 4, ressource bloquée, état précédent mal formé,
  substitution en un passage, chemin critique protégé, planning modifié notifié) a une épreuve ; que des copies
  abîmées exprès du cœur, du comptage et de l'adaptateur font rougir au moins une épreuve (--mutations), chacune
  dans un processus à part, borné par un délai ; que COMPTER_LES_DEFAUTS.py lit son FORMAT sur de vraies lignes de
  RELU (R-732) ; que l'adaptateur CAC 40 traduit juste un petit dépôt git fabriqué et lit les refus du relais.
② CONTEXTE D'APPEL — À la main : python3 -I tests/EPREUVES_DU_PROGRAMME_DE_PILOTAGE_Mer_25-11-2026.py [--mutations]
  Le mode --une-mutation=K est réservé au lanceur de mutations (un processus par mutation).
③ ENTRÉE — l'option --mutations, facultative.
④ CONDITIONS D'ENTRÉE — programmes/PILOTER_UN_PLANNING.py, COMPTER_LES_DEFAUTS.py, ADAPTATEUR_PILOTAGE_CAC40.py et
  ETAT_DES_TRAVAUX.py présents ; git installé (épreuve de l'adaptateur).
⑤ SORTIE — une ligne par épreuve, et UNE valeur : le code 0 si tout passe (et, avec --mutations, si chaque mutation
  est tuée), 1 sinon, 2 si une mutation ne trouve plus son texte (l'épreuve ne peut pas tourner, R-734).
⑥ TRAITEMENT — fabrique des plannings dans des dossiers temporaires, appelle `passage` avec une heure imposée et
  compare ; avec --mutations, pour chaque mutation, relance CE fichier dans un sous-processus borné qui réécrit une
  copie du fichier visé, la charge et rejoue la suite concernée ; une suite qui dépasse le délai compte TUÉE.
⑦ UNITÉ — heures de Paris imposées ; places ; secondes (délais).
⑧ POURQUOI — R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration. La relecture
  du 25-11-2026 (21h45) a trouvé 14 sabotages restés verts et un qui faisait PENDRE la suite : chacun est ici une
  mutation, avec un délai.
⑨ CE QUI CLOCHE — la lecture réelle des passages GitHub n'est éprouvée que par un faux gh ; les contrôles réels
  (blocages, rattachement) ne sont pas rejoués ici. Les fonctions imbriquées `voir` portent une fiche courte.
⑩ EFFET — des dossiers temporaires, effacés à la fin.
⑪ TERMINAISON — aucun appel réseau ; git local borné ; chaque mutation bornée par DELAI_MUTATION_S.
"""
import contextlib
import fcntl
import datetime
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(os.path.dirname(ICI), "programmes")
COEUR = os.path.join(PROG, "PILOTER_UN_PLANNING.py")
DEFAUTS = os.path.join(PROG, "COMPTER_LES_DEFAUTS.py")
ADAPT = os.path.join(PROG, "ADAPTATEUR_PILOTAGE_CAC40.py")
P = ZoneInfo("Europe/Paris")
T0 = datetime.datetime(2026, 11, 25, 21, 0, tzinfo=P)
M = datetime.timedelta(minutes=1)
DELAI_MUTATION_S = 20
EN_TETE_R = "ressource;capacite;palier_initial;pas;source;mesure\n"

# Mutations : (fichier visé, nom, texte exact, remplacement). Chacune doit faire rougir au moins une épreuve.
MUTATIONS = [
    ("coeur", "les dépendances sont ignorées",
     'and all(etats[d]["etat"] == "fait" for d in planning["etapes"][e]["deps"])]', ']'),
    ("coeur", "la capacité est ignorée", 'elif attribuees[r] < ress[r]["libres"]:', 'elif True:'),
    ("coeur", "le chemin critique n'ordonne plus", 'pretes.sort(key=lambda e: (-reste[e], ordre.index(e)))', 'pass'),
    ("coeur", "ordre inversé pour départager", 'pretes.sort(key=lambda e: (-reste[e], ordre.index(e)))',
     'pretes.sort(key=lambda e: (-reste[e], -ordre.index(e)))'),
    ("coeur", "étape faite gardant sa durée au chemin critique",
     'propre = 0.0 if etats[n]["etat"] == "fait" else planning["etapes"][n]["duree"]',
     'propre = planning["etapes"][n]["duree"]'),
    ("coeur", "chemin critique sans protection propre contre un cycle",
     '                if n in developpees:\n                    raise Arret', '                if False:\n                    raise Arret'),
    ("coeur", "AIMD : le palier ne monte jamais", 'palier, raison = prev["palier"] + l["pas"], (f"pleine',
     'palier, raison = prev["palier"], (f"pleine'),
    ("coeur", "AIMD : le palier ne recule pas sur refus", 'palier, raison = prev["palier"] // 2, (',
     'palier, raison = prev["palier"], ('),
    ("coeur", "AIMD : le palier repart toujours du palier initial", 'elif observees >= prev["palier"]:\n            palier, raison = prev["palier"] + l["pas"]',
     'elif observees >= prev["palier"]:\n            palier, raison = l["palier_initial"] + l["pas"]'),
    ("coeur", "AIMD : refus déjà vus recomptés (cumul ignoré)", 'nouveaux = [t for t in refus if prev is not None and (avant is None or t > avant)]',
     'nouveaux = [t for t in refus if prev is not None]'),
    ("coeur", "refus illisibles pris pour zéro", 'refus_illisible, refus = True, []', 'refus_illisible, refus = False, []'),
    ("coeur", "le palier dépasse la capacité", 'palier = max(1, min(cap, palier))', 'palier = max(1, palier)'),
    ("coeur", "capacité mesurée ignorée", 'cap = min(cap, max(0, mc))', 'pass'),
    ("coeur", "occupation mesurée ignorée", 'mesuree = m if isinstance(m, int) and not isinstance(m, bool) else 0', 'mesuree = 0'),
    ("coeur", "lancées non confirmées sans place", 'annoncees = {e for e, v in vivants.items() if v["ressource"] == r}', 'annoncees = set()'),
    ("coeur", "place comptée sur la ressource actuelle, pas celle du lancement",
     'annoncees = {e for e, v in vivants.items() if v["ressource"] == r}',
     'annoncees = {e for e in vivants if etats[e]["ressource"] == r}'),
    ("coeur", "C1 : confirmation par l'ÉTAT au lieu de l'observation",
     'if observations.get(e) != v["observation"]:\n            continue', 'if etats[e]["etat"] != "a_faire":\n            continue'),
    ("coeur", "N-63 : relancée après le délai", '        vivants[e] = v\n    return vivants, signales, liberes',
     '        if v["signale"] is None or e in signales:\n            vivants[e] = v\n    return vivants, signales, liberes'),
    ("coeur", "N-63 : À VÉRIFIER redit à chaque passage", 'if v["signale"] is None and (maintenant - v["heure"])',
     'if (maintenant - v["heure"])'),
    ("coeur", "N-63 : jamais signalé", 'v["signale"] = maintenant\n            signales.add(e)', 'pass'),
    ("coeur", "--liberer sans effet", 'liberes[x] = memoire.pop(x)', 'liberes[x] = memoire[x]'),
    ("coeur", "--liberer inconnu accepté", 'if x not in memoire:\n            raise Arret', 'if False:\n            raise Arret'),
    ("coeur", "N-65 : AIMD monte sur l'annoncé", 'elif observees >= prev["palier"]:', 'elif prises >= prev["palier"]:'),
    ("coeur", "observées sans l'occupation mesurée", 'max(mesuree, len(en_cours | annoncees)), max(mesuree, len(vues))',
     'max(mesuree, len(en_cours | annoncees)), len(vues)'),
    ("coeur", "N-70 : palier initial au-dessus de la capacité accepté", 'if l["palier_initial"] > l["capacite"]:', 'if False:'),
    ("coeur", "N-70 : places libres malgré mesure impossible", '"libres": 0 if impossible else max(0, palier - prises),',
     '"libres": max(0, palier - prises),'),
    ("coeur", "N-68 : heure future acceptée", 'if h > maintenant + datetime.timedelta(minutes=1):', 'if False:'),
    ("coeur", "N-68 : heure future sans tolérance", 'if h > maintenant + datetime.timedelta(minutes=1):', 'if h > maintenant:'),
    ("coeur", "N-68 : date absente de la ligne", "quand = f\"{v['heure'].astimezone(PARIS):%d-%m-%Y à %Hh%M}\"",
     "quand = f\"{v['heure'].astimezone(PARIS):%Hh%M}\""),
    ("coeur", "N-69 : --etat facultatif", 'if not dossier_etat:\n        raise Arret', 'if not dossier_etat:\n        dossier_etat = dossier\n    if False:\n        raise Arret'),
    ("coeur", "N-69 : état accepté dans un dépôt git", 'if git:\n        raise Arret', 'if False:\n        raise Arret'),
    ("coeur", "N-67 : --json sans les non confirmées", 'sortie["non_confirmees"] = {', 'sortie["_"] = {'),
    ("coeur", "ancien format « lancees » accepté", 'if "lancees" in brut:', 'if False:'),
    ("coeur", "lancées non confirmées relancées", 'if etats[e]["etat"] == "a_faire" and e not in en_attente', 'if etats[e]["etat"] == "a_faire"'),
    ("coeur", "le déclaré l'emporte sur l'observé", 'if o["etat"] in ("en_cours", "fait"):', 'if decl == "a_faire" and o["etat"] in ("en_cours", "fait"):'),
    ("coeur", "contradiction tue", 'L.append(f"CONTRADICTION {e} — {v[\'contradiction\']}")', 'pass'),
    ("coeur", "en_cours déclarable", 'DECLARABLES = ("a_faire", "pause", "attend", "bloque")', 'DECLARABLES = ETATS'),
    ("coeur", "preuve non lue acceptée", 'if not any(l["preuve"].startswith(p) for p in lues):', 'if False:'),
    ("coeur", "verdict toujours PEUT S'ARRÊTER", 'if lancer:\n        return "RESTER ÉVEILLÉ"', 'if False:\n        return "RESTER ÉVEILLÉ"'),
    ("coeur", "verdict qui ignore les étapes en cours", 'if cours:\n        return "RESTER ÉVEILLÉ"', 'if False:\n        return "RESTER ÉVEILLÉ"'),
    ("coeur", "verdict qui ignore les lancées non confirmées", 'if en_attente:\n        return "RESTER ÉVEILLÉ"',
     'if False:\n        return "RESTER ÉVEILLÉ"'),
    ("coeur", "N-76 / M3 : le verdict ne nomme plus les À VÉRIFIER", 'if a_voir:\n        raison +=', 'if False:\n        raison +='),
    ("coeur", "N-71 : une redite de LANCER sans l'heure (silencieuse)",
     'return f"lancee@{maintenant.astimezone(PARIS):%Y-%m-%dT%H:%M}"', 'return "lancee"'),
    ("coeur", "N-71 : non confirmée sans l'heure du lancement",
     "return f\"{mot}@{en_attente[e]['heure'].astimezone(PARIS):%Y-%m-%dT%H:%M}\"", "return mot"),
    ("coeur", "N-73 : pas de verrou", 'fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)', 'pass'),
    ("coeur", "N-73 : verrou seulement sans écrire", 'verrou = prendre_le_verrou(dossier_etat) if ecrire else None',
     'verrou = prendre_le_verrou(dossier_etat) if not ecrire else None'),
    ("coeur", "N-72 : --liberer accepté sans signalement", 'if memoire[x]["signale"] is None:\n            raise Arret',
     'if False:\n            raise Arret'),
    ("coeur", "N-79 : « en cours » termine le lancement",
     '            vivants[e] = dict(v, demarre=True)   # N-79 : l\'exécutant a commencé ; le lancement dure, tel quel\n            continue',
     '            continue'),
    ("coeur", "N-79 / N-83 : une étape en cours ET lancée compte deux places (sa ressource observée en plus)",
     ' and v["etat"] == "en_cours" and e not in vivants}', ' and v["etat"] == "en_cours"}'),
    ("coeur", "N-79 : un lancement démarré n'est pas gardé dans l'état", '        lancements = {e: v for e, v in vivants.items()}\n',
     '        lancements = {e: v for e, v in vivants.items() if not v["demarre"]}\n'),
    ("coeur", "N-83 : échéance d'un lancement démarré sur la durée de l'étape (forme du tour 5)",
     '        if e in vivants:\n            v = vivants[e]', '        if e in vivants and not vivants[e]["demarre"]:\n            v = vivants[e]'),
    ("coeur", "N-83 : un lancement démarré n'est pas une place observée", 'vues = en_cours | {e for e in annoncees if vivants[e]["demarre"]}',
     'vues = en_cours'),
    ("coeur", "N-84 C1 : échéance atteinte PILE = dépassée", 'if age > prevue:', 'if age >= prevue:'),
    ("coeur", "N-84 C4 : en_cours_depuis remis à chaque passage",
     '(a["en_cours_depuis"] if a and a["en_cours_depuis"] else maintenant)', 'maintenant'),
    ("coeur", "N-85 : comparaison en minutes non entières (autre unité que l'affichage)",
     'age = int((maintenant - depart).total_seconds() // 60)', 'age = (maintenant - depart).total_seconds() / 60'),
    ("coeur", "N-85 : affichage arrondi sous une heure", '    return f"{m} min"', '    return f"{int(round(minutes))} min"'),
    ("coeur", "M7 / N-80 : verrou pris puis rendu aussitôt", 'verrou = prendre_le_verrou(dossier_etat) if ecrire else None',
     'verrou = prendre_le_verrou(dossier_etat) if ecrire else None\n    if verrou is not None:\n        verrou.close()\n        verrou = None'),
    ("coeur", "A-1021 : sans la règle de l'échéance", 'if age > prevue:', 'if False:'),
    ("coeur", "A-1021 : ENQUÊTER en queue et non en tête", 'L[1:1] = [t for _, t in enqueter]', 'L[-2:-2] = [t for _, t in enqueter]'),
    ("coeur", "A-1021 : ENQUÊTER notifié à chaque passage", 'for e, _ in enqueter if e not in avant_enq]', 'for e, _ in enqueter]'),
    ("coeur", "A-1021 : ENQUÊTER jamais notifié", 'chg += [(f"enquêter {e}", "—", "échéance dépassée") for e, _ in enqueter if e not in avant_enq]', 'pass'),
    ("coeur", "A-1021 : durée attendue déclarée ignorée", 'prevue, source = planning["attendues"].get(', 'prevue, source = {}.get('),
    ("coeur", "A-1021 : étape en cours partie de sa première vue, pas de son lancement",
     'depart = v["heure"]', 'depart = suivi[e]["en_cours_depuis"] or v["heure"]'),
    ("coeur", "A-1021 : durée attendue sans source acceptée", 'if minutes <= 0 or not source.lower().startswith(("mesurée", "estimée")):', 'if minutes <= 0:'),
    ("coeur", "M1 : seuil du délai >= devient >", '.total_seconds() / 60 >= delai_min', '.total_seconds() / 60 > delai_min'),
    ("coeur", "M5 : observation sans la ressource observée",
     'return f"{o.get(\'etat\')} | {o.get(\'ressource\') or \'\'} | {phase}"', 'return f"{o.get(\'etat\')} | {phase}"'),
    ("coeur", "verdict qui ignore la file", 'if vivantes:\n        return "RESTER ÉVEILLÉ"', 'if False:\n        return "RESTER ÉVEILLÉ"'),
    ("coeur", "ressource bloquée garde éveillé", 'vivantes = [e for e in en_file if e not in bloquees]', 'vivantes = list(en_file)'),
    ("coeur", "le journal se tait sur les étapes", '        if a != b:\n            out.append((e, a, b))', '        pass'),
    ("coeur", "le journal se tait sur le palier", 'out.append((f"palier {r}", a, b))', 'pass'),
    ("coeur", "le journal se tait sur le verdict", 'out.append(("verdict", p.get("verdict", "—"), verdict_txt))', 'pass'),
    ("coeur", "le journal se tait sur un planning modifié", 'out.append(("planning", p.get("empreinte", "") or "—", empreinte))', 'pass'),
    ("coeur", "une mesure impossible laisse lancer", 'elif ress[r]["mesure_impossible"]:', 'elif False:'),
    ("coeur", "un contrôle impossible rend 0", 'code = 3 if alerte else 4 if impossible else 0', 'code = 3 if alerte else 0'),
    ("coeur", "le code 4 masque l'ALERTE", 'code = 3 if alerte else 4 if impossible else 0', 'code = 4 if impossible else 3 if alerte else 0'),
    ("coeur", "ALERTE d'un contrôle devenue OK", 'statut = {0: "OK", 3: "ALERTE"}', 'statut = {0: "OK", 3: "OK"}'),
    ("coeur", "paramètre absent ignoré", 'if manque:\n            a_lancer.append', 'if False:\n            a_lancer.append'),
    ("coeur", "en-tête CSV non contrôlé", 'if tuple(c.strip() for c in (lecteur.fieldnames or ())) != tuple(colonnes):', 'if False:'),
    ("coeur", "durée négative acceptée", 'v < 0:\n        raise Arret', 'False:\n        raise Arret'),
    ("coeur", "état déclaré inconnu accepté", 'if tete not in DECLARABLES or', 'if False and tete not in DECLARABLES or'),
    ("coeur", "clé en double acceptée", 'if l["cle"] in params:\n            raise', 'if False:\n            raise'),
    ("coeur", "état précédent mal formé sans conseil", 'except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:',
     'except (OSError,) as e:'),
    ("defauts", "D7 : CORRIGÉ referme un défaut", 'statuts.setdefault(i, set()).add("ouvert")\n                elif jeton == JETON_FERME:',
     'statuts.setdefault(i, set()).add("fermé" if "CORRIG" in ligne.upper() else "ouvert")\n                elif jeton == JETON_FERME:'),
    ("defauts", "D7 : statut illisible ignoré", 'illisibles.append(f"{i} [{jeton}]")', 'pass'),
    ("defauts", "N-66 : statut lu n'importe où après la gravité", r'r"(?:[^)\n]*\))?\s*(?:\[([^\]\n]*)\])?"',
     r'r"(?:[^)\n]*\))?[^\[\n]*(?:\[([^\]\n]*)\])?"'),
    ("defauts", "N-66 : un seul [FERMÉ] ferme malgré une définition contraire", 'fermes = {i for i, s in statuts.items() if s == {"fermé"}}',
     'fermes = {i for i, s in statuts.items() if "fermé" in s}'),
    ("defauts", "N-66 : définitions contraires non signalées", 'if len(s) > 1:\n            illisibles', 'if False:\n            illisibles'),
    ("defauts", "D7 : défaut sans gravité muet", '("défaut sans gravité", sans)', '("défaut sans gravité", [])'),
    ("adaptateur", "D4 : refus illisibles rendus comme zéro", 'mesures[r_ep]["refus"] = None', 'mesures[r_ep]["refus"] = []'),
    ("adaptateur", "D4 : un refus « clé inconnue » compte", 'if "DEMANDE REFUSEE" in journal and "en cours ou en attente" in journal:',
     'if "DEMANDE REFUSEE" in journal:'),
    ("adaptateur", "D5 : l'adaptateur ne déclare plus ses preuves", 'PREUVES_LUES = ("branche:",)', 'PREUVES_LUES = ()'),
    ("adaptateur", "N-71 / M6 : la phase redevient la pointe", '"phase": phase_observee(', '"phase": faits["pointe"] or phase_observee('),
    ("adaptateur", "M6 de Cowork : l'adaptateur ne rend plus la phase", '"phase": phase_observee(', '"_": phase_observee('),
    ("adaptateur", "N-79 : la phase porte aussi la note (forme du tour 3)",
     'fichier = PRODUIT_DE_L_EXECUTANT.get(etat_txt)\n    if fichier is None:',
     'return f"[{etat_txt}] RELU {empreinte(\'echanges/RELU.md\') or \'—\'} A_RELIRE {empreinte(\'echanges/A_RELIRE.md\') or \'—\'}"\n    fichier = None\n    if fichier is None:'),
    ("adaptateur", "M10 / N-81 : la phase sans l'état rangé",
     'fichier = PRODUIT_DE_L_EXECUTANT.get(etat_txt)\n    if fichier is None:',
     'fichier = PRODUIT_DE_L_EXECUTANT.get(etat_txt)\n    etat_txt = ""\n    if fichier is None:'),
    ("adaptateur", "N-79 : table vide (l'état seul, jamais le produit)", 'PRODUIT_DE_L_EXECUTANT = {"À RELIRE": "echanges/RELU.md", "ÉCRITURE": "echanges/A_RELIRE.md"}',
     'PRODUIT_DE_L_EXECUTANT = {}'),
    ("adaptateur", "N-85 C8 : l'entrée ÉCRITURE de la table attend le RELU au lieu de la note",
     'PRODUIT_DE_L_EXECUTANT = {"À RELIRE": "echanges/RELU.md", "ÉCRITURE": "echanges/A_RELIRE.md"}',
     'PRODUIT_DE_L_EXECUTANT = {"À RELIRE": "echanges/RELU.md", "ÉCRITURE": "echanges/RELU.md"}'),
    ("adaptateur", "N-83 : la marque EN_COURS sans la ressource de l'état rangé (forme du tour 5)",
     '"etat": "en_cours", "ressource": ress,', '"etat": "en_cours",'),
    ("adaptateur", "N-86 R1 : la phase porte le dernier COMMIT du produit, pas son contenu (forme du tour 5)",
     'lambda f, b=b: (E.git(\n                          depot, "ls-tree", f"origin/{b}", "--", f).split() + ["", "", ""])[2]),',
     'lambda f, b=b, base=base: E.git(\n                          depot, "log", "-1", "--format=%H", f"{base}..origin/{b}", "--", f).strip()),'),
    ("adaptateur", "D2 : pause déclarée l'emporte sur la marque EN_COURS", 'if marques:\n            obs[e] = {"etat": "en_cours"',
     'if marques and not l["etat"].startswith("pause"):\n            obs[e] = {"etat": "en_cours"'),
]


def charger(chemin, nom="coeur"):
    """① RÔLE — Charger un fichier Python comme module.
    ② CONTEXTE D'APPEL — les suites et le mode --une-mutation.
    ③ ENTRÉE — `chemin` ; `nom` du module.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module.
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — éprouver une copie abîmée sans toucher l'original.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — exécute le module.
    ⑪ TERMINAISON — revient.
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ecrire(dossier, nom, texte):
    """① RÔLE — Écrire un fichier d'épreuve.
    ② CONTEXTE D'APPEL — les fabriques et les suites.
    ③ ENTRÉE — `dossier`, `nom`, `texte`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin écrit.
    ⑥ TRAITEMENT — crée le dossier, écrit en UTF-8.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit un fichier.
    ⑪ TERMINAISON — revient.
    """
    c = os.path.join(dossier, nom)
    os.makedirs(os.path.dirname(c), exist_ok=True)
    with open(c, "w", encoding="utf-8") as f:
        f.write(texte)
    return c


def demenagement(dossier, sans_dependance=False, capacite=2, palier=None, delai=30, adaptateur=""):
    """① RÔLE — Fabriquer le planning FACTICE du déménagement (aucun rapport avec le CAC 40).
    ② CONTEXTE D'APPEL — `epreuves_du_coeur`.
    ③ ENTRÉE — `dossier` ; `sans_dependance` (sabotage des données : CHARGER ne dépend plus de CUISINE) ;
      `capacite` et `palier` (initial, défaut = capacité) des déménageurs ; `delai` de confirmation (minutes) ;
      `adaptateur` (nom d'un fichier Python du dossier, vide = adaptateur intégré).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — trois étapes : CUISINE (2 h) et SALON (1 h), CHARGER (3 h) qui dépend de CUISINE ; preuve
      « fichier:<étape>.fait » ; une ressource « demenageurs ».
    ⑦ UNITÉ — heures, places, minutes.
    ⑧ POURQUOI — A-1017 et A-1018 (Jean-Luc, 25-11-2026) : l'épreuve du déménagement.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit trois CSV.
    ⑪ TERMINAISON — revient.
    """
    ecrire(dossier, "planning.csv", "cle;valeur\nnom;Déménagement factice\nobjectif;tout est dans le camion\n"
           f"delai_de_confirmation_min;{delai}\n" + (f"adaptateur;{adaptateur}\n" if adaptateur else ""))
    dep = "" if sans_dependance else "CUISINE"
    ecrire(dossier, "etapes.csv",
           "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
           "CUISINE;Emballer la cuisine;;Paul;demenageurs;2;fichier:CUISINE.fait;\n"
           "SALON;Emballer le salon;;Marie;demenageurs;1;fichier:SALON.fait;\n"
           f"CHARGER;Charger le camion;{dep};Paul;demenageurs;3;fichier:CHARGER.fait;\n")
    ecrire(dossier, "ressources.csv", EN_TETE_R + f"demenageurs;{capacite};{palier or capacite};1;deux amis disponibles samedi;\n")


FACTICE = ("import json, os\nPREUVES_LUES = ()\n"
           "def observer(planning, racine, params):\n"
           "    m = json.load(open(os.path.join(racine, 'mesure.json')))\n"
           "    return {}, {'demenageurs': m}\n")


FACTICE_PHASES = ("import json, os\nPREUVES_LUES = ('phase:',)\n"
                  "def observer(planning, racine, params):\n"
                  "    return json.load(open(os.path.join(racine, 'obs.json'))), {}\n")


FACTICE_VERROU = ("import fcntl, os\nPREUVES_LUES = ()\n"
                  "def observer(planning, racine, params):\n"
                  "    f = open(os.path.join(racine, 'VERROU.lock'), 'a')\n"
                  "    try:\n"
                  "        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
                  "        r = 'pris'\n"
                  "    except BlockingIOError:\n"
                  "        r = 'refuse'\n"
                  "    f.close()\n"
                  "    open(os.path.join(racine, 'essai_du_verrou.txt'), 'w').write(r)\n"
                  "    return {}, {}\n")


def cas_planning_attendu(minutes, source):
    """① RÔLE — Fabriquer un déménagement qui déclare une durée attendue de lancement sur « demenageurs ».
    ② CONTEXTE D'APPEL — `epreuves_du_coeur`, épreuves A-1021.
    ③ ENTRÉE — `minutes` et `source` (textes écrits dans planning.csv).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dossier.
    ⑥ TRAITEMENT — `demenagement`, puis deux clés ajoutées à planning.csv.
    ⑦ UNITÉ — minutes.
    ⑧ POURQUOI — A-1021 : une durée attendue porte sa source, « mesurée » ou « estimée ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit des fichiers.
    ⑪ TERMINAISON — revient.
    """
    d = tempfile.mkdtemp(prefix="attendue_")
    demenagement(d)
    with open(os.path.join(d, "planning.csv"), "a", encoding="utf-8") as f:
        f.write(f"duree_attendue_demenageurs_min;{minutes}\nduree_attendue_demenageurs_source;{source}\n")
    return d


def relecture(dossier, phase, ressource, delai=20):
    """① RÔLE — Fabriquer un planning d'UNE étape A1 dont l'adaptateur factice rend la phase (comme l'adaptateur CAC 40
      rend « [À RELIRE] » puis « [ÉCRITURE] » avec la pointe de la branche).
    ② CONTEXTE D'APPEL — `epreuves_du_coeur`, cas C (confirmation par observation).
    ③ ENTRÉE — `dossier` ; `phase` (texte rendu comme `phase`) ; `ressource` rendue ; `delai` (minutes).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — trois CSV, l'adaptateur factice, obs.json.
    ⑦ UNITÉ — minutes, places.
    ⑧ POURQUOI — superviseur R-759 tour 2 (25-11-2026 ~23h00) : la confirmation comparait un ÉTAT, et l'adaptateur
      traduit À RELIRE et ÉCRITURE tous deux en a_faire : une relecture lancée n'était jamais confirmée.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit des fichiers.
    ⑪ TERMINAISON — revient.
    """
    ecrire(dossier, "planning.csv", f"cle;valeur\nnom;relecture factice\ndelai_de_confirmation_min;{delai}\n"
           "adaptateur;phases.py\n")
    ecrire(dossier, "phases.py", FACTICE_PHASES)
    ecrire(dossier, "ressources.csv", EN_TETE_R + "agents;1;1;1;épreuve;\nrelecteur;1;1;1;épreuve;\n")
    ecrire(dossier, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
           "A1;programme;;agent;agents;1;phase:A1;\n")
    observer_phase(dossier, phase, ressource)


def observer_phase(dossier, phase, ressource, etat="a_faire"):
    """① RÔLE — Écrire ce que l'adaptateur factice observera pour A1.
    ② CONTEXTE D'APPEL — `relecture` et les cas C.
    ③ ENTRÉE — `dossier` ; `phase` ; `ressource` (None : la clé n'est pas écrite, comme la marque EN_COURS de
      l'adaptateur réel au tour 5 — N-83) ; `etat` observé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — obs.json.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — voir `relecture`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit obs.json.
    ⑪ TERMINAISON — revient.
    """
    o = {"etat": etat, "phase": phase, "detail": f"travail-x [{phase}]"}
    if ressource is not None:
        o["ressource"] = ressource
    ecrire(dossier, "obs.json", json.dumps({"A1": o}))


def epreuves_du_coeur(C, parler=True):
    """① RÔLE — Les épreuves du cœur, contre le module `C` (l'original ou une copie abîmée).
    ② CONTEXTE D'APPEL — `main` et le mode --une-mutation.
    ③ ENTRÉE — `C` (module) ; `parler` (afficher chaque ligne).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre d'échecs.
    ⑥ TRAITEMENT — chaque cas fabrique son dossier, appelle C.passage, compare.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — voir ⑧ du module.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — dossiers temporaires.
    ⑪ TERMINAISON — revient (une copie abîmée peut pendre : le lanceur de mutations la borne).
    """
    echecs = 0

    def voir(nom, ok, detail=""):
        """① RÔLE — Compter et afficher une épreuve.
        ② CONTEXTE D'APPEL — chaque cas.
        ③ ENTRÉE — nom, ok, détail.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — —
        ⑥ TRAITEMENT — incrémente `echecs` si faux.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — affiche.
        ⑪ TERMINAISON — revient.
        """
        nonlocal echecs
        if not ok:
            echecs += 1
        if parler:
            print(f"{'OK   ' if ok else 'ÉCHEC'} {nom}{' — ' + str(detail) if detail and not ok else ''}")

    def cas(preuves=(), mesure=None, **k):
        """① RÔLE — Fabriquer un déménagement dans un dossier neuf.
        ② CONTEXTE D'APPEL — chaque cas.
        ③ ENTRÉE — preuves à poser, mesure (dict → adaptateur factice), options de `demenagement`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le dossier.
        ⑥ TRAITEMENT — fabrique.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — écrit.
        ⑪ TERMINAISON — revient.
        """
        d = tempfile.mkdtemp(prefix="demenagement_")
        if mesure is not None:
            ecrire(d, "factice.py", FACTICE)
            ecrire(d, "mesure.json", json.dumps(mesure))
            k["adaptateur"] = "factice.py"
        demenagement(d, **k)
        for p in preuves:
            ecrire(d, p, "fait\n")
        return d

    def arret(d, quoi):
        """① RÔLE — Dire si un passage s'arrête (Arret) avec `quoi` dans le message.
        ② CONTEXTE D'APPEL — cas A.
        ③ ENTRÉE — dossier, texte attendu (vide = tout message).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si Arret.
        ⑥ TRAITEMENT — appel.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — revient.
        """
        try:
            passer(d, T0, ecrire=False)
            return False
        except C.Arret as e:
            return quoi in str(e)

    def arret_a(d, t, quoi):
        """① RÔLE — Dire si un passage à l'heure `t` s'arrête (Arret) avec `quoi` dans le message.
        ② CONTEXTE D'APPEL — cas H1.
        ③ ENTRÉE — dossier, heure, texte attendu (vide = tout message).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si Arret.
        ⑥ TRAITEMENT — un passage sans écrire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — N-68 : l'heure du passage décide.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — revient.
        """
        try:
            passer(d, t, ecrire=False)
            return False
        except C.Arret as e:
            return quoi in str(e)

    def remplacer_dans(d, nom, avant, apres):
        """① RÔLE — Saboter une donnée d'un fichier du dossier.
        ② CONTEXTE D'APPEL — cas.
        ③ ENTRÉE — dossier, nom, avant, après.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — —
        ⑥ TRAITEMENT — remplacement.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — écrit.
        ⑪ TERMINAISON — revient.
        """
        t = open(os.path.join(d, nom), encoding="utf-8").read()
        ecrire(d, nom, t.replace(avant, apres))

    def passer(d, t, params=None, **k):
        """① RÔLE — Appeler C.passage avec l'état DANS le dossier temporaire de l'épreuve (hors de tout dépôt git).
        ② CONTEXTE D'APPEL — chaque cas du cœur.
        ③ ENTRÉE — dossier, heure, paramètres, options de C.passage.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : celle de C.passage.
        ⑥ TRAITEMENT — `dossier_etat` vaut le dossier s'il n'est pas donné.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — l'état est obligatoire et refusé dans un dépôt git (N-69 du RELU du 25-11-2026, 22h54).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — ceux de C.passage.
        ⑪ TERMINAISON — revient, ou lève ce que lève C.passage.
        """
        k.setdefault("dossier_etat", d)
        return C.passage(d, t, params, **k)

    try:
        # D1 — la bonne liste : CUISINE (chemin critique 5 h) puis SALON ; CHARGER attend CUISINE
        r = passer(cas(), T0, ecrire=False)
        voir("D1 déménagement : LANCER CUISINE puis SALON, CHARGER attend", r["lancer"] == ["CUISINE", "SALON"], r["lancer"])
        voir("D1 verdict RESTER ÉVEILLÉ, code 0", r["verdict"] == "RESTER ÉVEILLÉ" and r["code"] == 0, (r["verdict"], r["code"]))
        # S1, S2 — sabotages des DONNÉES : la liste change
        r = passer(cas(sans_dependance=True), T0, ecrire=False)
        voir("S1 sans la dépendance : CHARGER puis CUISINE, SALON en file",
             r["lancer"] == ["CHARGER", "CUISINE"] and list(r["en_file"]) == ["SALON"], (r["lancer"], r["en_file"]))
        r = passer(cas(capacite=1), T0, ecrire=False)
        voir("S2 capacité 1 : CUISINE seule", r["lancer"] == ["CUISINE"], r["lancer"])
        r = passer(cas(preuves=["CUISINE.fait"]), T0, ecrire=False)
        voir("D2 CUISINE prouvée : LANCER CHARGER puis SALON", r["lancer"] == ["CHARGER", "SALON"], r["lancer"])
        d = cas()
        ecrire(d, "CUISINE.fait.en_cours", "x")
        r = passer(d, T0, ecrire=False)
        voir("D3 CUISINE en cours : SALON seule lancée (1 place libre)", r["lancer"] == ["SALON"], r["lancer"])
        r = passer(cas(preuves=["CUISINE.fait", "SALON.fait", "CHARGER.fait"]), T0, ecrire=False)
        voir("D4 tout prouvé : PEUT S'ARRÊTER, objectif atteint", r["verdict"] == "PEUT S'ARRÊTER" and "objectif" in r["raison"], r["raison"])
        d = cas()
        remplacer_dans(d, "etapes.csv", "fichier:CUISINE.fait;", "fichier:CUISINE.fait;attend:le propriétaire rend les clés")
        remplacer_dans(d, "etapes.csv", "fichier:SALON.fait;", "fichier:SALON.fait;pause")
        r = passer(d, T0, ecrire=False)
        voir("D5 attente et pause sans rien d'observé : PEUT S'ARRÊTER, CUISINE nommée",
             r["verdict"] == "PEUT S'ARRÊTER" and "CUISINE" in r["raison"], r["raison"])
        # V1 — verdict tenu par une étape EN COURS seule (sabotage resté vert le 25-11 : verdict qui ignore en cours)
        d = cas(preuves=["SALON.fait"])
        ecrire(d, "CUISINE.fait.en_cours", "x")
        r = passer(d, T0, ecrire=False)
        voir("V1 seule CUISINE en cours, rien à lancer : RESTER ÉVEILLÉ", r["lancer"] == [] and r["verdict"] == "RESTER ÉVEILLÉ", r["raison"])
        # V2 — verdict tenu par la FILE seule (occupation mesurée pleine)
        r = passer(cas(mesure={"occupees": 2}), T0, ecrire=False)
        voir("V2 occupation mesurée 2/2 : rien lancé, deux en file, RESTER ÉVEILLÉ",
             r["lancer"] == [] and len(r["en_file"]) == 2 and r["verdict"] == "RESTER ÉVEILLÉ", (r["lancer"], r["raison"]))
        voir("V2 message de file exact : places prises avant + attribuées pendant",
             "2 place(s) prise(s) avant ce passage + 0 attribuée(s)" in r["en_file"].get("CUISINE", ""), r["en_file"])
        # V3 — capacité mesurée plus petite que la déclarée
        r = passer(cas(mesure={"capacite": 1}), T0, ecrire=False)
        voir("V3 capacité mesurée 1 : CUISINE seule", r["lancer"] == ["CUISINE"], r["lancer"])
        # V4 — capacité mesurée 0 : ressource BLOQUÉE, ne garde pas éveillé (mineur 10)
        r = passer(cas(mesure={"capacite": 0}), T0, ecrire=False)
        voir("V4 capacité mesurée 0 : BLOQUÉE, PEUT S'ARRÊTER, nommée",
             r["lancer"] == [] and r["verdict"] == "PEUT S'ARRÊTER" and "BLOQUÉE" in r["raison"]
             and any(l.startswith("RESSOURCE BLOQUÉE demenageurs") for l in r["lignes"]), r["raison"])
        # O1 — D2 : pause déclarée + en_cours observé → l'observé l'emporte, contradiction affichée, place prise
        d = cas(capacite=1)
        remplacer_dans(d, "etapes.csv", "fichier:CUISINE.fait;", "fichier:CUISINE.fait;pause")
        ecrire(d, "CUISINE.fait.en_cours", "x")
        r = passer(d, T0, ecrire=False)
        voir("O1 pause déclarée, en cours observé : en_cours, place prise, rien lancé, RESTER ÉVEILLÉ",
             r["etats"]["CUISINE"]["etat"] == "en_cours" and r["lancer"] == [] and r["verdict"] == "RESTER ÉVEILLÉ"
             and r["ressources"]["demenageurs"]["prises"] == 1, (r["etats"]["CUISINE"]["etat"], r["lancer"], r["raison"]))
        voir("O1 ligne CONTRADICTION affichée", any(l.startswith("CONTRADICTION CUISINE") for l in r["lignes"]))
        # O2 — « en_cours » et « fait » ne se déclarent pas
        for decl in ("en_cours", "fait"):
            d = cas()
            remplacer_dans(d, "etapes.csv", "fichier:SALON.fait;", f"fichier:SALON.fait;{decl}")
            voir(f"O2 état « {decl} » déclaré : ARRET", arret(d, "ne se déclarent pas"))
        # L1 — D1 : mémoire des lancements non confirmés (délai 30 min)
        d = cas()
        r1 = passer(d, T0, ecrire=True)
        r2 = passer(d, T0 + 5 * M, ecrire=True)
        voir("L1 5 min après : rien relancé, deux lancées non confirmées", r2["lancer"] == [] and sorted(r2["en_attente"]) == ["CUISINE", "SALON"],
             (r2["lancer"], r2["en_attente"]))
        voir("L1 5 min après : rien n'a changé, NOTIFIER non, RESTER ÉVEILLÉ",
             r2["changements"] == [] and r2["lignes"][-1].startswith("NOTIFIER : non") and r2["verdict"] == "RESTER ÉVEILLÉ",
             (r2["changements"], r2["raison"]))
        voir("L1 ligne LANCÉE NON CONFIRMÉE", any(l.startswith("LANCÉE NON CONFIRMÉE CUISINE") for l in r2["lignes"]))
        voir("L1 les lancées prennent leurs places", r2["ressources"]["demenageurs"]["prises"] == 2, r2["ressources"]["demenageurs"])
        voir("L1 la ligne LANCÉE NON CONFIRMÉE porte la date (N-68)",
             any("annoncée le 25-11-2026 à 21h00" in l for l in r2["lignes"] if l.startswith("LANCÉE NON CONFIRMÉE CUISINE")),
             [l for l in r2["lignes"] if l.startswith("LANCÉE")])
        try:
            passer(d, T0 + 6 * M, ecrire=False, liberer=["CUISINE"])
            voir("N72 --liberer=CUISINE lancée 6 min plus tôt, jamais signalée : ARRET", False, "aucun arrêt")
        except C.Arret as ex:
            voir("N72 --liberer=CUISINE lancée 6 min plus tôt, jamais signalée : ARRET", "pas été signalé" in str(ex), ex)
        r3 = passer(d, T0 + 40 * M, ecrire=True)
        voir("L1 après le délai (N-63) : rien relancé, À VÉRIFIER dit, notifié une fois",
             r3["lancer"] == [] and r3["a_verifier"] == ["CUISINE", "SALON"]
             and any(l.startswith("À VÉRIFIER CUISINE") for l in r3["lignes"])
             and ("CUISINE", "lancee@2026-11-25T21:00", "lancee_a_verifier@2026-11-25T21:00") in r3["changements"], (r3["lancer"], r3["changements"]))
        voir("L1 après le délai : aucune ligne ne commence par LANCER, les places restent prises",
             not any(l.startswith("LANCER ") for l in r3["lignes"]) and r3["ressources"]["demenageurs"]["prises"] == 2,
             r3["ressources"]["demenageurs"])
        for minutes in (70, 200):
            rx = passer(d, T0 + minutes * M, ecrire=True)
            # A-1021 : SALON (1 h) dépasse son échéance avant 70 min, CUISINE (2 h) avant 200 min : un seul
            # changement, « enquêter », à son apparition ; rien d'autre ne bouge
            voir(f"L1 à {minutes} min (N-63) : ni LANCER ni À VÉRIFIER, seul changement l'échéance qui apparaît",
                 rx["lancer"] == [] and not any(l.startswith(("À VÉRIFIER", "LANCER ")) for l in rx["lignes"])
                 and rx["changements"] == [(f"enquêter {'SALON' if minutes == 70 else 'CUISINE'}", "—", "échéance dépassée")]
                 and sorted(rx["en_attente"]) == ["CUISINE", "SALON"],
                 (rx["lancer"], rx["changements"], [l for l in rx["lignes"] if l.startswith("À V")]))
        ecrire(d, "CUISINE.fait.en_cours", "x")
        r4 = passer(d, T0 + 205 * M, ecrire=True)
        voir("L1 marque posée : CUISINE confirmée en cours, SALON encore en attente",
             r4["etats"]["CUISINE"]["etat"] == "en_cours" and list(r4["en_attente"]) == ["SALON"], (r4["en_attente"],))
        voir("N76 / M3 une étape en cours ET SALON À VÉRIFIER : la raison nomme SALON À VÉRIFIER",
             "en cours" in r4["raison"] and "À VÉRIFIER par quelqu'un : SALON" in r4["raison"], r4["raison"])
        # C2 — --liberer : geste humain unique, l'étape est relancée au même passage ; inconnu → ARRET
        r5 = passer(d, T0 + 210 * M, ecrire=True, liberer=["SALON"])
        voir("C2 --liberer=SALON : SALON relancée, libération au journal",
             r5["lancer"] == ["SALON"] and any(o == "libération SALON" for o, _, _ in r5["changements"]),
             (r5["lancer"], r5["changements"]))
        try:
            passer(d, T0 + 216 * M, ecrire=True, liberer=["SALON"])
            voir("N72 --liberer=SALON rejoué 6 min après : ARRET, SALON pas relancée", False, "aucun arrêt")
        except C.Arret as ex:
            voir("N72 --liberer=SALON rejoué 6 min après : ARRET, SALON pas relancée", "pas été signalé" in str(ex), ex)
        try:
            passer(d, T0 + 215 * M, ecrire=False, liberer=["CHARGER"])
            voir("C2 --liberer=CHARGER sans lancement en mémoire : ARRET", False, "aucun arrêt")
        except C.Arret as ex:
            voir("C2 --liberer=CHARGER sans lancement en mémoire : ARRET", "aucun lancement" in str(ex), ex)
        # C3 — la place reste sur la ressource DU LANCEMENT si le planning change de ressource
        d = cas()
        ecrire(d, "ressources.csv", EN_TETE_R + "demenageurs;2;2;1;x;\ncamion;1;1;1;x;\n")
        passer(d, T0, ecrire=True)
        remplacer_dans(d, "etapes.csv", "CUISINE;Emballer la cuisine;;Paul;demenageurs", "CUISINE;Emballer la cuisine;;Paul;camion")
        r = passer(d, T0 + 5 * M, ecrire=False)
        voir("C3 ressource changée au planning : la place reste sur demenageurs (2), camion libre (0)",
             r["ressources"]["demenageurs"]["prises"] == 2 and r["ressources"]["camion"]["prises"] == 0 and r["lancer"] == [],
             (r["ressources"]["demenageurs"]["prises"], r["ressources"]["camion"]["prises"], r["lancer"]))
        # H1 — N-68 : une heure future dans l'état arrête le passage
        d = cas()
        passer(d, T0 + 60 * M, ecrire=True)
        voir("H1 état écrit à 22h00, passage à 21h00 : ARRET « futur »", arret_a(d, T0, "futur"))
        voir("H1 état écrit à 22h00, passage à 21h59 et 30 s : accepté (tolérance d'une minute)",
             not arret_a(d, T0 + 60 * M - datetime.timedelta(seconds=30), ""))
        # G1 — N-69 : --etat obligatoire, refusé dans un dépôt git
        d = cas()
        try:
            C.passage(d, T0, ecrire=False)
            voir("G1 sans --etat : ARRET", False, "aucun arrêt")
        except C.Arret as ex:
            voir("G1 sans --etat : ARRET", "obligatoire" in str(ex), ex)
        os.makedirs(os.path.join(d, "depot", ".git"))
        try:
            C.passage(d, T0, dossier_etat=os.path.join(d, "depot", "etat"), ecrire=False)
            voir("G1 état dans un dépôt git : ARRET", False, "aucun arrêt")
        except C.Arret as ex:
            voir("G1 état dans un dépôt git : ARRET", "dépôt git" in str(ex), ex)
        # N67 — le JSON rend les lancements non confirmés
        d = cas()
        passer(d, T0, ecrire=True)
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            code_json = C.main(["x", d, f"--etat={d}", "--json", "--maintenant=2026-11-25T21:05"])
        j = json.loads(tampon.getvalue())
        voir("N67 --json : non_confirmees CUISINE et SALON, lancer vide",
             code_json == 0 and sorted(j.get("non_confirmees", {})) == ["CUISINE", "SALON"] and j["lancer"] == [], j)
        # L2 — occupation mesurée 0 mais deux lancées en attente : place prise = max(mesurée, comptées)
        d = cas(mesure={"occupees": 0})
        passer(d, T0, ecrire=True)
        r = passer(d, T0 + 5 * M, ecrire=True)
        voir("L2 mesurée 0, deux lancées non confirmées : prises 2", r["ressources"]["demenageurs"]["prises"] == 2,
             r["ressources"]["demenageurs"])
        # C1 — superviseur R-759 tour 2 : une étape qui passe de « À RELIRE » à « ÉCRITURE » a CONFIRMÉ sa relecture
        d = tempfile.mkdtemp(prefix="relecture_")
        relecture(d, "À RELIRE pointe aaa", "relecteur")
        r1 = passer(d, T0, ecrire=True)
        observer_phase(d, "ÉCRITURE pointe bbb", "agents")
        r2 = passer(d, T0 + 5 * M, ecrire=True)
        voir("C1 À RELIRE puis ÉCRITURE : relecture confirmée, A1 relancée pour l'écriture",
             r1["lancer"] == ["A1"] and r2["lancer"] == ["A1"] and not r2["en_attente"], (r1["lancer"], r2["lancer"], r2["en_attente"]))
        voir("C1 la relecture ne garde plus de place sur relecteur", r2["ressources"]["relecteur"]["prises"] == 0,
             r2["ressources"]["relecteur"])
        # N71 — une redite de LANCER (confirmation à tort) est un changement NOTIFIÉ, jamais silencieux
        d = tempfile.mkdtemp(prefix="redite_")
        relecture(d, "[À RELIRE] RELU — A_RELIRE aaa", "relecteur")
        passer(d, T0, ecrire=True)
        r2 = passer(d, T0 + 5 * M, ecrire=True)
        observer_phase(d, "[À RELIRE] RELU — A_RELIRE bbb", "relecteur")
        r3 = passer(d, T0 + 10 * M, ecrire=True)
        voir("N71 5 min : rien relancé, NOTIFIER non", r2["lancer"] == [] and r2["changements"] == [], r2["changements"])
        voir("N71 phase changée, A1 redite LANCER : CHANGEMENT A1 lancee@21:00 → lancee@21:10, NOTIFIER oui",
             r3["lancer"] == ["A1"] and ("A1", "lancee@2026-11-25T21:00", "lancee@2026-11-25T21:10") in r3["changements"]
             and r3["lignes"][-1].startswith("NOTIFIER : oui"), (r3["lancer"], r3["changements"], r3["lignes"][-1]))
        # M5 — la ressource observée fait partie de l'observation : même phase, autre ressource → confirmée
        d = tempfile.mkdtemp(prefix="ressource_")
        relecture(d, "[ÉCRITURE] RELU — A_RELIRE —", "agents")
        passer(d, T0, ecrire=True)
        observer_phase(d, "[ÉCRITURE] RELU — A_RELIRE —", "relecteur")
        r = passer(d, T0 + 5 * M, ecrire=True)
        voir("M5 même phase, ressource observée changée : lancement confirmé, A1 relancée sur relecteur",
             r["lancer"] == ["A1"] and not r["en_attente"] and r["etats"]["A1"]["ressource"] == "relecteur",
             (r["lancer"], r["en_attente"]))
        # M1 — la borne du délai : à EXACTEMENT le délai (30 min), le lancement est signalé
        d = cas()
        passer(d, T0, ecrire=True)
        r = passer(d, T0 + 30 * M, ecrire=True)
        voir("M1 délai 30 min atteint pile : CUISINE et SALON À VÉRIFIER", r["a_verifier"] == ["CUISINE", "SALON"], r["a_verifier"])
        # N73 — verrou exclusif : un passage qui écrit pendant qu'un autre tient le verrou s'arrête
        d = cas()
        with open(os.path.join(d, C.NOM_VERROU), "a") as tenu:
            fcntl.flock(tenu, fcntl.LOCK_EX | fcntl.LOCK_NB)
            try:
                passer(d, T0, ecrire=True)
                voir("N73 verrou tenu par un autre passage : ARRET, rien écrit", False, "aucun arrêt")
            except C.Arret as ex:
                voir("N73 verrou tenu par un autre passage : ARRET, rien écrit",
                     "verrou" in str(ex) and not os.path.exists(os.path.join(d, C.NOM_ETAT)), ex)
            r = passer(d, T0, ecrire=False)
            voir("N73 --sans-ecrire ne prend pas le verrou : passage rendu", r["lancer"] == ["CUISINE", "SALON"], r["lancer"])
        r = passer(d, T0, ecrire=True)
        voir("N73 verrou rendu : le passage suivant écrit", r["lancer"] == ["CUISINE", "SALON"]
             and os.path.exists(os.path.join(d, C.NOM_ETAT)), r["lancer"])
        # N80 — le verrou est TENU pendant tout le passage : l'adaptateur tente de le prendre pendant `observer`
        d = cas()
        ecrire(d, "verrou.py", FACTICE_VERROU)
        remplacer_dans(d, "planning.csv", "delai_de_confirmation_min;30\n", "delai_de_confirmation_min;30\nadaptateur;verrou.py\n")
        passer(d, T0, ecrire=True)
        essai = open(os.path.join(d, "essai_du_verrou.txt"), encoding="utf-8").read()
        voir("N80 / M7 pendant `observer`, un second preneur du verrou est refusé", essai == "refuse", essai)
        # N79 — « en cours » ne termine pas un lancement ; il garde son heure de départ
        d = tempfile.mkdtemp(prefix="n79_")
        relecture(d, "[À RELIRE] echanges/RELU.md aaa", "relecteur")
        r1 = passer(d, T0, ecrire=True)
        observer_phase(d, "marque EN_COURS", "relecteur", etat="en_cours")
        r2 = passer(d, T0 + 5 * M, ecrire=True)
        garde = json.load(open(os.path.join(d, C.NOM_ETAT), encoding="utf-8"))["lancements"].get("A1", {})
        voir("N79 marque posée : A1 en cours, lancement gardé dans l'état avec son heure de 21h00, une place",
             r1["lancer"] == ["A1"] and (r2.get("vivants") or {}).get("A1", {}).get("demarre") is True and not r2["en_attente"]
             and garde.get("heure", "").startswith("2026-11-25T21:00") and r2["ressources"]["relecteur"]["prises"] == 1,
             (r2.get("vivants"), r2["en_attente"], garde, r2["ressources"]["relecteur"]))
        observer_phase(d, "[À RELIRE] echanges/RELU.md aaa", "relecteur")
        r3 = passer(d, T0 + 10 * M, ecrire=True)
        voir("N79 marque retirée, rien produit : pas de redite LANCER, A1 non confirmée depuis 21h00",
             r3["lancer"] == [] and "A1" in r3["en_attente"] and r3["en_attente"]["A1"]["heure"] == T0,
             (r3["lancer"], r3["en_attente"]))
        # N79 (b) — un RELU puis une note nouvelle entre deux passages : la relecture est relancée (produit apparu)
        d = tempfile.mkdtemp(prefix="n79b_")
        relecture(d, "[À RELIRE] echanges/RELU.md aaa", "relecteur")
        passer(d, T0, ecrire=True)
        observer_phase(d, "[À RELIRE] echanges/RELU.md bbb", "relecteur")
        r = passer(d, T0 + 30 * M, ecrire=True)
        voir("N79 (b) RELU bbb puis note nouvelle : relecture terminée, A1 relancée et notifiée",
             r["lancer"] == ["A1"] and ("A1", "lancee@2026-11-25T21:00", "lancee@2026-11-25T21:30") in r["changements"],
             (r["lancer"], r["changements"]))
        voir("N79 une étape en cours ET lancée non confirmée compte UNE place",
             C.places_prises("r", {"X": {"ressource": "r", "etat": "en_cours"}}, {"X": {"ressource": "r", "demarre": True}}, {}) == (1, 1),
             C.places_prises("r", {"X": {"ressource": "r", "etat": "en_cours"}}, {"X": {"ressource": "r", "demarre": True}}, {}))
        # A-1021 — l'échéance, dans le déménagement factice : SALON (1 h) en cours depuis son lancement
        d = cas()
        passer(d, T0, ecrire=True)
        ecrire(d, "SALON.fait.en_cours", "x")
        r = passer(d, T0 + 10 * M, ecrire=True)
        voir("E-1021 SALON en cours depuis 10 min, prévue 1 h : pas d'ENQUÊTER", r.get("enqueter") == [], r.get("enqueter"))
        r = passer(d, T0 + 61 * M, ecrire=True)
        voir("E-1021 échéance de SALON dépassée (61 min sur 1 h) : ENQUÊTER SALON en TÊTE de la liste, notifié",
             r.get("enqueter") == ["SALON"] and r["lignes"][1].startswith("ENQUÊTER SALON : prévue 1 h 00")
             and "en cours depuis 1 h 01" in r["lignes"][1] and ("enquêter SALON", "—", "échéance dépassée") in r["changements"],
             (r["lignes"][:3], r["changements"]))
        r = passer(d, T0 + 66 * M, ecrire=True)
        voir("E-1021 passage suivant : ENQUÊTER SALON redit en tête, PAS renotifié",
             r["lignes"][1].startswith("ENQUÊTER SALON") and not any(o.startswith("enquêter") for o, _, _ in r["changements"]),
             (r["lignes"][:2], r["changements"]))
        ecrire(d, "SALON.fait", "fait")
        r = passer(d, T0 + 70 * M, ecrire=True)
        voir("E-1021 SALON faite : ENQUÊTER disparaît, et c'est un changement",
             r.get("enqueter") == [] and ("enquêter SALON", "échéance dépassée", "—") in r["changements"], r["changements"])
        voir("E-1021 durée attendue sans source « mesurée » ou « estimée » : ARRET",
             arret(cas_planning_attendu("15", "dit par quelqu'un"), "source"))
        # A-1021 — R-732 : la VRAIE durée attendue du Plan V8 se lit (planning/PLAN_V8/planning.csv, relecteur 15 min)
        try:
            vrai = C.lire_planning(os.path.join(os.path.dirname(ICI), "planning", "PLAN_V8"))
            voir("E-1021 vrai planning PLAN_V8 : relecteur attendu 15 min, source « mesurée »",
                 vrai["attendues"].get("relecteur", (0, ""))[0] == 15 and vrai["attendues"]["relecteur"][1].startswith("mesurée"),
                 vrai.get("attendues"))
        except (C.Arret, KeyError) as ex:
            voir("E-1021 vrai planning PLAN_V8 : relecteur attendu 15 min, source « mesurée »", False, ex)
        # A-1021 — CAS RÉEL rejoué : travail-pilotage livrée (À RELIRE) à 21h35, relecture Cowork ≈ 15 min mesurées
        d = tempfile.mkdtemp(prefix="cas_reel_")
        relecture(d, "[À RELIRE] echanges/RELU.md —", "relecteur", delai=60)
        remplacer_dans(d, "planning.csv", "adaptateur;phases.py\n", "adaptateur;phases.py\nduree_attendue_relecteur_min;15\n"
                       "duree_attendue_relecteur_source;mesurée le 25-11-2026 (relecture Cowork)\n")
        t = datetime.datetime(2026, 11, 25, 21, 35, tzinfo=P)
        ra = passer(d, t, ecrire=True)
        rb = passer(d, t + 10 * M, ecrire=True)
        rc = passer(d, t + 16 * M, ecrire=True)
        voir("E-1021 cas réel : LANCER à 21h35, rien à 21h45, ENQUÊTER A1 à 21h51 (prévue 15 min), notifié",
             ra["lancer"] == ["A1"] and rb.get("enqueter") == [] and rb["changements"] == [] and rc.get("enqueter") == ["A1"]
             and rc["lignes"][1].startswith("ENQUÊTER A1 : prévue 15 min (mesurée le 25-11-2026") and "lancée depuis 16 min" in rc["lignes"][1]
             and "rien n'a bougé depuis le 25-11-2026 à 21h35" in rc["lignes"][1] and rc["lignes"][-1].startswith("NOTIFIER : oui"),
             (rb["changements"], rc["lignes"][:2], rc["lignes"][-1]))
        # A1 — AIMD, montée sur l'OBSERVÉ seulement (N-65) : capacité 4, palier initial 1
        d = cas(capacite=4, palier=1)
        a = passer(d, T0, ecrire=True)
        b = passer(d, T0 + 5 * M, ecrire=True)
        ecrire(d, "CUISINE.fait.en_cours", "x")
        c = passer(d, T0 + 10 * M, ecrire=True)
        ecrire(d, "SALON.fait.en_cours", "x")
        e4 = passer(d, T0 + 15 * M, ecrire=True)
        pa = [x["ressources"]["demenageurs"]["palier"] for x in (a, b, c, e4)]
        voir("A0 N-65 : un lancement NON CONFIRMÉ ne fait pas monter le palier (1 → 1)", pa[:2] == [1, 1], pa)
        voir("A1 AIMD pleine d'étapes observées : palier 1 → 1 → 2 → 3", pa == [1, 1, 2, 3], pa)
        voir("A1 SALON lancé quand CUISINE est observée (place gagnée)", c["lancer"] == ["SALON"], c["lancer"])
        voir("A1 journal : CHANGEMENT palier demenageurs 1 → 2", ("palier demenageurs", 1, 2) in c["changements"], c["changements"])
        # A5 — montée sur l'occupation MESURÉE
        d = cas(capacite=4, palier=1, mesure={"occupees": 1})
        a = passer(d, T0, ecrire=True)
        b = passer(d, T0 + 5 * M, ecrire=True)
        pa = [x["ressources"]["demenageurs"]["palier"] for x in (a, b)]
        voir("A5 occupation mesurée 1 au palier 1 : 1 → 2", pa == [1, 2], pa)
        # A2 — AIMD, recul : un refus NOUVEAU divise par deux ; un refus déjà vu ne recompte pas
        d = cas(capacite=3, mesure={"refus": []})
        a = passer(d, T0, ecrire=True)
        ecrire(d, "mesure.json", json.dumps({"refus": ["2026-11-25T21:03:00+01:00"]}))
        b = passer(d, T0 + 5 * M, ecrire=True)
        ecrire(d, "CUISINE.fait.en_cours", "x")
        c = passer(d, T0 + 10 * M, ecrire=True)
        pa = [x["ressources"]["demenageurs"]["palier"] for x in (a, b, c)]
        voir("A2 refus nouveau : 3 → 1 ; même refus au passage suivant, pleine : 1 → 2", pa == [3, 1, 2], pa)
        # A3 — refus illisibles : palier gelé, code 4, jamais 0
        ecrire(d, "mesure.json", json.dumps({"refus": None}))
        r = passer(d, T0 + 15 * M, ecrire=False)
        voir("A3 refus illisibles : code 4, palier gelé à 2", r["code"] == 4 and r["ressources"]["demenageurs"]["palier"] == 2,
             (r["code"], r["ressources"]["demenageurs"]))
        # A4 — borne : palier déjà à la capacité, pleine → reste à la capacité
        d = cas(capacite=2)
        passer(d, T0, ecrire=True)
        r = passer(d, T0 + 5 * M, ecrire=True)
        voir("A4 pleine au plafond : palier reste 2", r["ressources"]["demenageurs"]["palier"] == 2, r["ressources"]["demenageurs"])
        # M1 — mesure impossible : rien lancé, code 4
        r = passer(cas(mesure={"occupees": None, "detail": "compteur illisible"}), T0, ecrire=False)
        voir("M1 mesure impossible : rien lancé, code 4, libres 0 (N-70)", r["lancer"] == [] and r["code"] == 4
             and r["ressources"]["demenageurs"]["libres"] == 0 and "non mesurée" in r["en_file"].get("CUISINE", ""),
             (r["lancer"], r["code"], r["ressources"]["demenageurs"], r["en_file"]))
        voir("N70 palier_initial 9 pour une capacité 2 : ARRET", arret(cas(capacite=2, palier=9), "palier_initial"))
        # J1 — journal : identique → rien ; preuve posée → changement ; verdict au premier passage
        d = cas()
        r1 = passer(d, T0, ecrire=True)
        voir("J1 premier passage : CHANGEMENT verdict — → RESTER ÉVEILLÉ", ("verdict", "—", "RESTER ÉVEILLÉ") in r1["changements"])
        ecrire(d, "CUISINE.fait", "x")
        r3 = passer(d, T0 + 20 * M, ecrire=True)
        voir("J1 preuve posée : CHANGEMENT CUISINE lancee → fait", ("CUISINE", "lancee@2026-11-25T21:00", "fait") in r3["changements"], r3["changements"])
        voir("J1 journal écrit sur disque", "CUISINE;lancee@2026-11-25T21:00;fait" in open(os.path.join(d, C.NOM_JOURNAL), encoding="utf-8").read())
        voir("J1 ACTIONS.txt contient la ligne VERDICT", "VERDICT" in open(os.path.join(d, C.NOM_ACTIONS), encoding="utf-8").read())
        # J2 — mineur 9 : planning modifié → notifié
        remplacer_dans(d, "ressources.csv", "deux amis disponibles samedi", "trois amis disponibles samedi")
        r = passer(d, T0 + 25 * M, ecrire=True)
        voir("J2 planning modifié : CHANGEMENT planning, NOTIFIER oui", any(o == "planning" for o, _, _ in r["changements"]), r["changements"])
        # E1 — mineur 14 : état précédent mal formé → ARRET avec le conseil « renommer »
        for mauvais in ({"ressources": {"demenageurs": {"t": 1}}}, {"lancees": {"CUISINE": 5}}, [1, 2]):
            d = cas()
            ecrire(d, C.NOM_ETAT, json.dumps(mauvais))
            voir(f"E1 état précédent {str(mauvais)[:30]} : ARRET « renommer »", arret(d, "renommer"))
        # K1 — contrôles : 3 → ALERTE code 3 ; absent → IMPOSSIBLE code 4 ; les deux → code 3, ligne CODE 3
        d = cas()
        ecrire(d, "alerte.py", "import sys\nprint('un blocage')\nsys.exit(3)\n")
        ecrire(d, "controles.csv", f"controle;commande\nblocages;{sys.executable} -I {{dossier}}/alerte.py\n")
        r = passer(d, T0, ecrire=False)
        voir("K1 contrôle qui rend 3 : ALERTE, code 3", r["code"] == 3 and r["controles"][0][1] == "ALERTE", r["controles"])
        ecrire(d, "controles.csv", "controle;commande\nabsent;/nulle/part/programme_absent\n")
        r = passer(d, T0, ecrire=False)
        voir("K1 contrôle impossible à lancer : IMPOSSIBLE, code 4", r["code"] == 4, r["controles"])
        ecrire(d, "controles.csv", f"controle;commande\nblocages;{sys.executable} -I {{dossier}}/alerte.py\nabsent;/nulle/part/x\n")
        r = passer(d, T0, ecrire=False)
        voir("K1 ALERTE et IMPOSSIBLE : code 3, ligne CODE 3 annonçant les deux",
             r["code"] == 3 and any(l.startswith("CODE 3") for l in r["lignes"]), (r["code"], r["controles"]))
        # K2 — paramètre absent → IMPOSSIBLE ; --param=X={param:X} ne boucle pas (mineur 12)
        ecrire(d, "controles.csv", "controle;commande\np;echo {param:ABSENT}\n")
        r = passer(d, T0, ecrire=False)
        voir("K2 paramètre absent : IMPOSSIBLE, code 4", r["code"] == 4 and "ABSENT" in r["controles"][0][2], r["controles"])
        ecrire(d, "controles.csv", "controle;commande\np;echo {param:X}\n")
        r = passer(d, T0, {"X": "{param:X}"}, ecrire=False)
        voir("K2 --param=X={param:X} : un seul passage, OK", r["controles"][0][1] == "OK", r["controles"])
        # A — arrêts : planning illisible ou faux → rien n'est conclu
        for nom, fichier, rempl, quoi in (
                ("cycle", "etapes.csv", ("CUISINE;Emballer la cuisine;;", "CUISINE;Emballer la cuisine;CHARGER;"), "cycle"),
                ("dépendance inconnue", "etapes.csv", (";CUISINE;Paul", ";GARAGE;Paul"), "GARAGE"),
                ("colonne en trop", "etapes.csv", ("Emballer le salon", "Emballer le salon;et la cave"), "colonne en trop"),
                ("en-tête faux", "etapes.csv", ("duree_h", "duree"), "en-tête"),
                ("durée négative", "etapes.csv", (";demenageurs;1;", ";demenageurs;-1;"), "négatif"),
                ("état inconnu", "etapes.csv", ("fichier:SALON.fait;", "fichier:SALON.fait;peut-etre"), "refusé"),
                ("clé en double", "planning.csv", ("nom;Déménagement factice\n", "nom;Déménagement factice\nnom;bis\n"), "double"),
                ("délai absent", "planning.csv", ("delai_de_confirmation_min;30\n", ""), "delai_de_confirmation_min"),
                ("preuve lue par personne (D5)", "etapes.csv", ("fichier:SALON.fait", "aucune"), "lue par personne")):
            d = cas()
            remplacer_dans(d, fichier, *rempl)
            voir(f"A {nom} : ARRET", arret(d, quoi))
        # CC — le chemin critique, appelé SEUL sur un cycle, s'arrête (sans l'aide de a_un_cycle)
        faux = {"etapes": {"X": {"deps": ["Y"], "duree": 1.0}, "Y": {"deps": ["X"], "duree": 1.0}}}
        try:
            C.chemin_critique(faux, {"X": {"etat": "a_faire"}, "Y": {"etat": "a_faire"}})
            voir("CC chemin critique seul sur un cycle : ARRET", False, "aucun arrêt")
        except C.Arret:
            voir("CC chemin critique seul sur un cycle : ARRET", True)
        # R — départage à durée égale (ordre du fichier) ; étape faite à 0 h au chemin critique
        d = tempfile.mkdtemp(prefix="ordre_")
        ecrire(d, "planning.csv", "cle;valeur\nnom;ordre\ndelai_de_confirmation_min;30\n")
        ecrire(d, "ressources.csv", EN_TETE_R + "r;1;1;1;épreuve;\n")
        ecrire(d, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "A;a;;x;r;2;fichier:A;\nB;b;;x;r;2;fichier:B;\n")
        r = passer(d, T0, ecrire=False)
        voir("R1 durées égales : l'ordre du fichier départage (A)", r["lancer"] == ["A"], r["lancer"])
        ecrire(d, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "P;p;;x;r;1;fichier:P;\nS;s;P;x;r;10;fichier:S;\nQ;q;;x;r;3;fichier:Q;\n")
        ecrire(d, "S", "fait")
        r = passer(d, T0, ecrire=False)
        voir("R2 S faite compte 0 h : Q (3 h) avant P (1 h)", r["lancer"] == ["Q"], r["lancer"])
        # R3 — cas tiré d'une VRAIE ligne du planning du projet (planning/PLAN_V8/etapes.csv, ligne D, R-732)
        vraie = [l for l in open(os.path.join(os.path.dirname(ICI), "planning", "PLAN_V8", "etapes.csv"),
                                 encoding="utf-8").read().splitlines() if l.startswith("D;")][0]
        d = tempfile.mkdtemp(prefix="vraie_ligne_")
        lignes = ["etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat"]
        for e in ("B", "C_CONTROLE_GITHUB", "C_LANCEUR", "C_LANCEUR_2", "C_SELECTION", "C_FILE_DEMANDES"):
            lignes.append(f"{e};{e};;pilote;machines_github;1;fichier:{e};")
            if e != "B":
                ecrire(d, e, "fait")
        lignes.append(vraie.replace("branche:travail-toutes-strategies", "fichier:D"))
        ecrire(d, "etapes.csv", "\n".join(lignes) + "\n")
        ecrire(d, "planning.csv", "cle;valeur\nnom;vraie ligne\ndelai_de_confirmation_min;20\n")
        ecrire(d, "ressources.csv", EN_TETE_R + "machines_github;20;10;5;A-593;\n")
        r = passer(d, T0, ecrire=False)
        voir("R3 vraie ligne D : B prête, D non lancée", r["lancer"] == ["B"], r["lancer"])
        ecrire(d, "B", "fait")
        r = passer(d, T0, ecrire=False)
        voir("R3 vraie ligne D : B faite → D lancée", r["lancer"] == ["D"], r["lancer"])
    except Exception as e:   # une copie abîmée qui plante compte comme rougie
        echecs += 1
        if parler:
            print(f"ÉCHEC exception imprévue : {type(e).__name__} {e}")
    return echecs + epreuves_du_tour_6(C, parler)


def epreuves_du_tour_6(C, parler=True):
    """① RÔLE — Les épreuves de N-83, N-84 et N-85 (b) (RELU Cowork du 26-11-2026, 01h19), contre le module `C`.
    ② CONTEXTE D'APPEL — `epreuves_du_coeur` (donc aussi chaque mutation du cœur) ; à la main, contre une copie du
      cœur du tour 5, pour montrer qu'elles y rougissent.
    ③ ENTRÉE — `C` (module) ; `parler`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre d'échecs.
    ⑥ TRAITEMENT — trois plannings factices à l'adaptateur de phases (`FACTICE_PHASES`) : (1) N-83, deux étapes ; la
      marque EN_COURS est posée SANS clé ressource, comme l'adaptateur réel du tour 5 la rendait ; (2) N-84 et N-85,
      la borne pile et à 15 min 01 s ; (3) N-84, une étape en cours jamais lancée. Seules des clés présentes au
      tour 5 et au tour 6 sont lues (lancer, en_attente, enqueter, lignes, ressources), et `places_prises` est
      appelée avec une forme que les deux signatures acceptent.
    ⑦ UNITÉ — minutes, places.
    ⑧ POURQUOI — N-83 : l'épreuve N79 posait la marque avec la ressource « relecteur », ce que l'adaptateur réel ne
      faisait pas (un témoin qui n'emprunte pas le chemin du calcul réel). N-84 : les sabotages C1 (>=) et C4
      (en_cours_depuis remis à chaque passage) laissaient la suite verte. N-85 : « prévue 15 min, lancée depuis
      15 min » à 15 min 01 s.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — dossiers temporaires.
    ⑪ TERMINAISON — revient.
    """
    echecs = 0

    def voir(nom, ok, detail=""):
        """① RÔLE — Compter et afficher une épreuve. ② CONTEXTE D'APPEL — chaque cas. ③ ENTRÉE — nom, ok, détail.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — ⑥ TRAITEMENT — incrémente `echecs` si faux. ⑦ UNITÉ — —
        ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — affiche. ⑪ TERMINAISON — revient.
        """
        nonlocal echecs
        echecs += not ok
        if parler:
            print(f"{'OK   ' if ok else 'ÉCHEC'} {nom}{'' if ok else ' — ' + str(detail)}")

    def passer(d, t):
        """① RÔLE — Un passage qui écrit, état dans le dossier. ② CONTEXTE D'APPEL — chaque cas. ③ ENTRÉE — dossier,
        heure. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : celle de C.passage. ⑥ TRAITEMENT — appel.
        ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — ceux de C.passage. ⑪ TERMINAISON — revient.
        """
        return C.passage(d, t, None, dossier_etat=d, ecrire=True, controles=False)

    def obs(d, **etapes):
        """① RÔLE — Écrire obs.json pour plusieurs étapes. ② CONTEXTE D'APPEL — cas N-83. ③ ENTRÉE — dossier,
        {étape: observation}. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — ⑥ TRAITEMENT — JSON. ⑦ UNITÉ — —
        ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — écrit. ⑪ TERMINAISON — revient.
        """
        ecrire(d, "obs.json", json.dumps(etapes))

    S = datetime.timedelta(seconds=1)
    attendu = "duree_attendue_relecteur_min;15\nduree_attendue_relecteur_source;mesurée (épreuve)\n"
    try:
        # N-83 — la marque EN_COURS SANS clé ressource : le lancement garde sa ressource et son échéance
        d = tempfile.mkdtemp(prefix="n83_")
        ecrire(d, "planning.csv", "cle;valeur\nnom;N-83\ndelai_de_confirmation_min;60\nadaptateur;phases.py\n" + attendu)
        ecrire(d, "phases.py", FACTICE_PHASES)
        ecrire(d, "ressources.csv", EN_TETE_R + "agents;1;1;1;épreuve;\nrelecteur;1;1;1;épreuve;\n")
        ecrire(d, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "A1;un;;agent;agents;1;phase:A1;\nA2;deux;;agent;agents;1;phase:A2;\n")
        a_relire = {"etat": "a_faire", "ressource": "relecteur", "phase": "[À RELIRE] echanges/RELU.md —", "detail": "x"}
        marque = {"etat": "en_cours", "detail": "travail-x : marque echanges/EN_COURS.md"}   # forme exacte du tour 5
        obs(d, A1=a_relire, A2={"etat": "en_cours", "detail": "travail-y : marque echanges/EN_COURS.md"})
        r1 = passer(d, T0)
        obs(d, A1=marque, A2={"etat": "en_cours", "detail": "travail-y : marque echanges/EN_COURS.md"})
        r2 = passer(d, T0 + 5 * M)
        prises = {x: r2["ressources"][x]["prises"] for x in ("relecteur", "agents")}
        voir("N83 marque SANS ressource sur A1 lancée en relecture : relecteur prises 1, agents prises 1 (A2 seule)",
             r1["lancer"] == ["A1"] and prises == {"relecteur": 1, "agents": 1}, (r1["lancer"], prises))
        obs(d, A1=marque, A2=a_relire)
        r3 = passer(d, T0 + 6 * M)
        voir("N83 A2 devient À RELIRE pendant la relecture marquée de A1 : PAS de LANCER A2 (palier 1 du relecteur)",
             r3["lancer"] == [] and r3["ressources"]["relecteur"]["prises"] == 1, (r3["lancer"], r3["ressources"]["relecteur"]))
        r4 = passer(d, T0 + 15 * M)
        r5 = passer(d, T0 + 16 * M)
        l5 = [x for x in r5["lignes"] if x.startswith("ENQUÊTER A1")]
        voir("N83 relecture marquée : rien à 15 min pile, ENQUÊTER A1 à 16 min (prévue 15 min, mesurée), en cours",
             r4.get("enqueter") == [] and r5.get("enqueter") == ["A1"] and l5
             and l5[0].startswith("ENQUÊTER A1 : prévue 15 min (mesurée") and "en cours depuis 16 min" in l5[0],
             (r4.get("enqueter"), r5.get("enqueter"), l5))
        voir("N83 unitaire : en cours sur agents, lancement vivant démarré sur relecteur : une place, sur relecteur",
             C.places_prises("relecteur", {"X": {"ressource": "agents", "etat": "en_cours"}},
                             {"X": {"ressource": "relecteur", "demarre": True, "signale": None}}, {}) == (1, 1)
             and C.places_prises("agents", {"X": {"ressource": "agents", "etat": "en_cours"}},
                                 {"X": {"ressource": "relecteur", "demarre": True, "signale": None}}, {}) == (0, 0))
        # N-84 C1 et N-85 — la borne : rien à 15 min pile ni à 15 min 01 s ; ENQUÊTER à 16 min, sans contradiction
        d = tempfile.mkdtemp(prefix="n84_pile_")
        relecture(d, "[À RELIRE] echanges/RELU.md —", "relecteur", delai=60)
        remplacer = open(os.path.join(d, "planning.csv"), encoding="utf-8").read() + attendu
        ecrire(d, "planning.csv", remplacer)
        ra = passer(d, T0)
        rb = passer(d, T0 + 15 * M)
        rc = passer(d, T0 + 15 * M + S)
        rd = passer(d, T0 + 16 * M)
        voir("N84 C1 échéance atteinte PILE (15 min sur 15) : pas d'ENQUÊTER", ra["lancer"] == ["A1"] and rb.get("enqueter") == [],
             (ra["lancer"], rb.get("enqueter")))
        voir("N85 à 15 min 01 s : pas d'ENQUÊTER (minutes entières, l'unité de l'affichage)", rc.get("enqueter") == [],
             [x for x in rc["lignes"] if x.startswith("ENQUÊTER")])
        voir("N84 / N85 à 16 min : ENQUÊTER A1 « prévue 15 min … lancée depuis 16 min »", rd.get("enqueter") == ["A1"]
             and "prévue 15 min" in rd["lignes"][1] and "lancée depuis 16 min" in rd["lignes"][1], rd["lignes"][:2])
        voir("N85 duree_lisible : une règle (troncature) — 15,02 → 15 min · 59,6 → 59 min · 61,5 → 1 h 01",
             (C.duree_lisible(15.02), C.duree_lisible(59.6), C.duree_lisible(61.5)) == ("15 min", "59 min", "1 h 01"),
             (C.duree_lisible(15.02), C.duree_lisible(59.6), C.duree_lisible(61.5)))
        # N-84 C4 — une étape en cours JAMAIS lancée (cas réel A1 et P_MESURE_SEUIL du Plan V8) : départ = première vue
        d = tempfile.mkdtemp(prefix="n84_jamais_")
        relecture(d, "[ÉCRITURE] —", None, delai=60)
        observer_phase(d, "marque", None, etat="en_cours")
        r0 = passer(d, T0)
        r30 = passer(d, T0 + 30 * M)
        r61 = passer(d, T0 + 61 * M)
        l61 = [x for x in r61["lignes"] if x.startswith("ENQUÊTER A1")]
        voir("N84 C4 en cours jamais lancée (1 h) : rien à +30 min, ENQUÊTER A1 à +61 min « prévue 1 h 00 … depuis 1 h 01 »",
             r0["lancer"] == [] and r30.get("enqueter") == [] and r61.get("enqueter") == ["A1"] and l61
             and l61[0].startswith("ENQUÊTER A1 : prévue 1 h 00 (duree_h de etapes.csv)") and "en cours depuis 1 h 01" in l61[0],
             (r0["lancer"], r30.get("enqueter"), r61.get("enqueter"), l61))
    except Exception as e:   # une copie abîmée qui plante compte comme rougie
        echecs += 1
        if parler:
            print(f"ÉCHEC tour 6 : exception imprévue {type(e).__name__} {e}")
    return echecs


def epreuves_des_defauts(D, parler=True):
    """① RÔLE — COMPTER_LES_DEFAUTS (module `D`) : son FORMAT, sur de VRAIES lignes de RELU (R-732) et sur les
      formulations qui fermaient à tort un BLOQUANT (D7 de la relecture du 25-11-2026).
    ② CONTEXTE D'APPEL — `main` et le mode --une-mutation.
    ③ ENTRÉE — `D` (module) ; `parler`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre d'échecs.
    ⑥ TRAITEMENT — D.compter et D.main (code de sortie) sur des textes.
    ⑦ UNITÉ — défauts.
    ⑧ POURQUOI — un motif se calibre sur un cas connu ET sur un cas qui doit échouer (§ 4 des instructions).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — un fichier temporaire par appel de D.main.
    ⑪ TERMINAISON — revient.
    """
    echecs = 0

    def voir(nom, ok, detail=""):
        """① RÔLE — Compter et afficher une épreuve.
        ② CONTEXTE D'APPEL — chaque cas.
        ③ ENTRÉE — nom, ok, détail.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — —
        ⑥ TRAITEMENT — incrémente `echecs` si faux.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — affiche.
        ⑪ TERMINAISON — revient.
        """
        nonlocal echecs
        echecs += not ok
        if parler:
            print(f"{'OK   ' if ok else 'ÉCHEC'} {nom}{'' if ok else ' — ' + str(detail)}")

    def code(texte):
        """① RÔLE — Le code de sortie de D.main sur un texte.
        ② CONTEXTE D'APPEL — cas.
        ③ ENTRÉE — texte.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le code.
        ⑥ TRAITEMENT — fichier temporaire, D.main sans affichage.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — écrit.
        ⑪ TERMINAISON — revient.
        """
        c = ecrire(tempfile.mkdtemp(prefix="relu_"), "RELU.md", texte)
        sortie = sys.stdout
        sys.stdout = open(os.devnull, "w")
        try:
            return D.main(["x", c])
        finally:
            sys.stdout.close()
            sys.stdout = sortie

    try:
        vrai = ("### N-62 (MINEUR) — l'empreinte « sans textes » est aveugle aux chaînes qui décident des verdicts\n"
                "2. N-59, N-60, N-61 (MINEURS, relectures de 16h11 et 16h15) : confirmés ou concordants ici (§ 2.4).\n"
                "- N-57 (IMPORTANT) : CORRIGÉ sur le fond (§ 2.1). RESTE : aucune ligne de contrôle dans la note du dépôt ; elle doit\n"
                "- N-53 : PAS CORRIGÉ (renvoi au RELU de 16h15 : `grep` sur le BACKLOG → 0).\n"
                "### N-54 (BLOQUANT) — le contrôle final refuse la note de ce tour : `Livraison` sera ROUGE\n"
                "- **N-50 (IMPORTANT) — RÉPARÉ.** Mon témoin du RELU précédent rejoué sur une copie :\n")
        o, f, s, i = D.compter(vrai)
        voir("F1 vraies lignes : mineurs N-59 N-60 N-61 N-62, bloquant N-54 ouverts", o["MINEUR"] == ["N-59", "N-60", "N-61", "N-62"]
             and o["BLOQUANT"] == ["N-54"], o)
        voir("F1 vraies lignes : CORRIGÉ et RÉPARÉ sans jeton → N-50 et N-57 OUVERTS", o["IMPORTANT"] == ["N-50", "N-57"] and f == [], (o, f))
        voir("F1 N-53 sans gravité : listé, et le code est 3", s == ["N-53"] and code(vrai) == 3, s)
        for neg in ("pas encore corrigé", "**PAS** CORRIGÉ", "NON-CORRIGÉ", "à corriger, rien de corrigé", "CORRIGÉ en partie"):
            o, f, s, i = D.compter(f"- N-7 (BLOQUANT) : {neg}\n")
            voir(f"F2 « {neg} » : bloquant OUVERT, code 3", o["BLOQUANT"] == ["N-7"] and code(f"- N-7 (BLOQUANT) : {neg}\n") == 3, (o, f))
        o, f, s, i = D.compter("- N-12 (BLOQUANT) [FERMÉ] — le compte est juste\n- N-13 (MINEUR) [OUVERT] — reste\n")
        voir("F3 « [FERMÉ] » ferme N-12 ; « [OUVERT] » laisse N-13 ouvert ; rien d'illisible",
             f == ["N-12"] and o["MINEUR"] == ["N-13"] and not i and not s, (o, f, i))
        voir("F3 code 0 (aucun bloquant ouvert, rien d'illisible)", code("- N-12 (BLOQUANT) [FERMÉ] — ok\n") == 0)
        o, f, s, i = D.compter("- N-14 (IMPORTANT) [FERME] — sans accent\n")
        voir("F4 « [FERME] » : statut illisible, défaut ouvert, code 3", i == ["N-14 [FERME]"] and o["IMPORTANT"] == ["N-14"]
             and code("- N-14 (IMPORTANT) [FERME] — x\n") == 3, (o, i))
        # F6 — N-66 : les deux lignes du RELU du 25-11-2026 (22h54), réécrites avec « N-6 » et « N-7 » et le vrai jeton
        n66 = ("- N-6 (BLOQUANT) — ne pas le marquer [FERMÉ] tant que la mesure manque\n"
               "- N-7 (BLOQUANT) [OUVERT] — ancien statut [FERMÉ] retiré\n")
        o, f, s, i = D.compter(n66)
        voir("F6 N-66 : jeton hors de sa place → N-6 et N-7 OUVERTS, code 3", o["BLOQUANT"] == ["N-6", "N-7"] and f == []
             and code(n66) == 3, (o, f))
        # F7 — deux définitions contraires du même numéro → illisible, ouvert
        o, f, s, i = D.compter("- N-8 (IMPORTANT) [FERMÉ] — réparé\n### N-8 (IMPORTANT) — reste à faire\n")
        voir("F7 définitions contraires : N-8 ouvert et illisible", o["IMPORTANT"] == ["N-8"] and f == []
             and i == ["N-8 (définitions contraires)"], (o, f, i))
        # F8 — une simple mention hors définition ne ferme rien
        o, f, s, i = D.compter("### N-10 (MINEUR) — x\nN-10 [FERMÉ] dans une phrase\n")
        voir("F8 mention « N-10 [FERMÉ] » hors définition : ouvert", o["MINEUR"] == ["N-10"] and f == [], (o, f))
        # F9 — le VRAI RELU de Cowork (22h54) : 1 bloquant, 3 importants, 4 mineurs, aucun fermé
        o, f, s, i = D.compter(open(os.path.join(ICI, "TEMOIN_RELU_COWORK_DU_PILOTE_Mer_25-11-2026_22h54.md"),
                                    encoding="utf-8").read())
        if True:
            voir("F9 vrai RELU de 22h54 : N-63 bloquant ; N-64..66 importants ; N-67..70 mineurs ; 0 fermé",
                 o["BLOQUANT"] == ["N-63"] and o["IMPORTANT"] == ["N-64", "N-65", "N-66"]
                 and o["MINEUR"] == ["N-67", "N-68", "N-69", "N-70"] and f == [] and not i, (o, f, i))
        o, f, s, i = D.compter("### N-9 (MOYEN) — défaut d'une gravité non reconnue\n")
        voir("F5 gravité MOYEN : sans gravité, code 3", s == ["N-9"] and code("### N-9 (MOYEN) — x\n") == 3, s)
    except Exception as e:
        echecs += 1
        if parler:
            print(f"ÉCHEC exception imprévue : {type(e).__name__} {e}")
    return echecs


FAUX_GH = r'''#!/usr/bin/env python3
import json, sys
a = sys.argv[1:]
mode = open(__file__ + ".mode").read().strip()
if a[:2] == ["run", "list"] and "--status" in a:
    print(json.dumps([{"databaseId": 7, "createdAt": "2026-11-25T20:00:00Z"},
                      {"databaseId": 8, "createdAt": "2026-11-25T20:30:00Z"}]))
elif a[:2] == ["run", "list"]:
    print(json.dumps([{"status": "in_progress"}, {"status": "completed"}]))
elif a[:2] == ["run", "view"]:
    if mode == "panne":
        sys.exit(1)
    print("::error::DEMANDE REFUSEE : 3 passage(s) de epreuves_longues.yml en cours ou en attente ; redeposer"
          if a[2] == "7" else "::error::DEMANDE REFUSEE : cle inconnue : x")
else:
    sys.exit(1)
'''


def epreuve_de_l_adaptateur(chemin_adaptateur=ADAPT, parler=True):
    """① RÔLE — L'adaptateur CAC 40 sur un petit dépôt git fabriqué : branche absente, marque EN_COURS (même sous une
      pause déclarée), branche qui ne porte qu'une note, branche fusionnée, branche à relire ; lecture des refus du
      relais par un faux gh ; préfixes de preuve déclarés.
    ② CONTEXTE D'APPEL — `main` et le mode --une-mutation.
    ③ ENTRÉE — `chemin_adaptateur` (l'original ou une copie abîmée, posée à côté d'ETAT_DES_TRAVAUX.py) ; `parler`.
    ④ CONDITIONS D'ENTRÉE — git installé.
    ⑤ SORTIE — UNE valeur : le nombre d'échecs.
    ⑥ TRAITEMENT — fabrique « amont » (dépôt nu) et un clone ; pousse main et des branches travail-* ; lance le cœur
      avec l'adaptateur, avec gh=/bin/false (mesure impossible voulue), puis avec un faux gh.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 : exécution de l'adaptateur sans réseau ; D4 et D5 de la relecture du 25-11-2026.
    ⑨ CE QUI CLOCHE — le faux gh ne reproduit que les champs lus.
    ⑩ EFFET — dossier temporaire.
    ⑪ TERMINAISON — git local borné à 60 s par appel.
    """
    echecs = 0
    t = tempfile.mkdtemp(prefix="adaptateur_")
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null", GIT_AUTHOR_NAME="e",
               GIT_AUTHOR_EMAIL="e@e", GIT_COMMITTER_NAME="e", GIT_COMMITTER_EMAIL="e@e")

    def voir(nom, ok, detail=""):
        """① RÔLE — Compter et afficher une épreuve.
        ② CONTEXTE D'APPEL — chaque cas.
        ③ ENTRÉE — nom, ok, détail.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — —
        ⑥ TRAITEMENT — incrémente `echecs` si faux.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — affiche.
        ⑪ TERMINAISON — revient.
        """
        nonlocal echecs
        echecs += not ok
        if parler:
            print(f"{'OK   ' if ok else 'ÉCHEC'} {nom}{'' if ok else ' — ' + str(detail)}")

    def g(*a, cwd=None):
        """① RÔLE — Lancer git.
        ② CONTEXTE D'APPEL — fabrique du dépôt.
        ③ ENTRÉE — arguments, dossier.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la sortie.
        ⑥ TRAITEMENT — subprocess.
        ⑦ UNITÉ — secondes.
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — écrit dans le dépôt fabriqué.
        ⑪ TERMINAISON — borné à 60 s.
        """
        return subprocess.run(["git", *a], cwd=cwd, env=env, capture_output=True, text=True, check=True, timeout=60).stdout

    try:
        amont, w = os.path.join(t, "amont.git"), os.path.join(t, "w")
        g("init", "-q", "--bare", "-b", "main", amont)
        g("clone", "-q", amont, w)
        ecrire(w, "programmes/a.py", "x = 1\n")
        ecrire(w, "echanges/.garde", "")
        g("add", "-A", cwd=w); g("commit", "-qm", "base", cwd=w); g("push", "-q", "origin", "main", cwd=w)
        g("checkout", "-qb", "travail-marque", cwd=w); ecrire(w, "echanges/EN_COURS.md", "en cours\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "marque", cwd=w); g("push", "-q", "origin", "travail-marque", cwd=w)
        g("checkout", "-q", "main", cwd=w); g("checkout", "-qb", "travail-note", cwd=w)
        ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\nnote\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "note", cwd=w); g("push", "-q", "origin", "travail-note", cwd=w)
        g("checkout", "-q", "main", cwd=w); g("checkout", "-qb", "travail-code", cwd=w)
        ecrire(w, "programmes/a.py", "x = 2\n"); ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\nnote\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "code", cwd=w); g("push", "-q", "origin", "travail-code", cwd=w)
        g("checkout", "-q", "main", cwd=w); g("checkout", "-qb", "travail-fusionnee", cwd=w)
        ecrire(w, "programmes/b.py", "y = 1\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "b", cwd=w); g("push", "-q", "origin", "travail-fusionnee", cwd=w)
        g("checkout", "-q", "main", cwd=w); g("merge", "-q", "--ff-only", "travail-fusionnee", cwd=w)
        g("push", "-q", "origin", "main", cwd=w); g("fetch", "-q", "origin", cwd=w)
        pl = os.path.join(t, "planning")
        ecrire(pl, "planning.csv", "cle;valeur\nnom;adaptateur fabriqué\ndelai_de_confirmation_min;20\n"
               f"adaptateur;{chemin_adaptateur}\nracine;{w}\ngh;/bin/false\n")
        ecrire(pl, "ressources.csv", EN_TETE_R + "agents;4;4;1;épreuve;\nrelecteur;1;1;1;épreuve;relecture\n"
               "relais;3;3;1;épreuve;relais epreuves_longues.yml demande_de_serie.yml\n")
        ecrire(pl, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "ABS;absente;;agent;agents;1;branche:travail-absente;\n"
               "MAR;marque;;agent;agents;1;branche:travail-marque;pause\n"
               "NOT;note seule;;agent;agents;1;branche:travail-note;\n"
               "COD;code;;agent;agents;1;branche:travail-code;\n"
               "FUS;fusionnée;;agent;agents;1;branche:travail-fusionnee;\n")
        C = charger(COEUR)
        r = C.passage(pl, T0, dossier_etat=os.path.join(t, "etat0"), ecrire=False, controles=False)
        e = {k: (v["etat"], v["ressource"]) for k, v in r["etats"].items()}
        attendu = {"ABS": ("a_faire", "agents"), "MAR": ("en_cours", "agents"), "NOT": ("a_faire", "agents"),
                   "COD": ("a_faire", "relecteur"), "FUS": ("fait", "agents")}
        for k, v in attendu.items():
            voir(f"AD {k} → {v}" + (" (pause déclarée, marque observée)" if k == "MAR" else ""), e.get(k) == v, e.get(k))
        voir("AD gh absent : MESURE IMPOSSIBLE du relais (occupation et refus), code 4",
             r["code"] == 4 and r["ressources"]["relais"]["mesure_impossible"] and r["ressources"]["relais"]["refus_illisible"],
             r["ressources"]["relais"])
        # N71 / M6 — un commit SANS RAPPORT sur la branche à relire ne confirme pas la relecture lancée
        e71 = os.path.join(t, "etat71")
        r = C.passage(pl, T0, dossier_etat=e71, ecrire=True, controles=False)
        note_cod = g("log", "-1", "--format=%H", "origin/travail-code", "--", "echanges/A_RELIRE.md", cwd=w).strip()
        pointe_cod = g("rev-parse", "origin/travail-code", cwd=w).strip()
        obs_cod = json.load(open(os.path.join(e71, C.NOM_ETAT), encoding="utf-8"))["lancements"].get("COD", {}).get("observation", "")
        voir("AD-71 / N-79 COD lancée en relecture ; sa phase porte l'état et le RELU, ni la note ni la pointe",
             "COD" in r["lancer"] and "[À RELIRE] echanges/RELU.md —" in obs_cod and note_cod not in obs_cod
             and pointe_cod not in obs_cod, (r["lancer"], obs_cod))
        g("checkout", "-q", "travail-code", cwd=w); ecrire(w, "echanges/SUPERVISEUR.md", "avis\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "commit sans rapport", cwd=w)
        g("push", "-q", "origin", "travail-code", cwd=w); g("checkout", "-q", "main", cwd=w)
        r = C.passage(pl, T0 + 5 * M, dossier_etat=e71, ecrire=True, controles=False)
        voir("AD-71 commit étranger sur travail-code : ni LANCER COD, COD toujours non confirmée",
             "COD" not in r["lancer"] and "COD" in r["en_attente"]
             and g("rev-parse", "origin/travail-code", cwd=w).strip() != pointe_cod, (r["lancer"], sorted(r["en_attente"])))
        # N79 (a) — l'AUTEUR corrige sa note pendant la relecture : ce n'est pas le geste du relecteur
        g("checkout", "-q", "travail-code", cwd=w); ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\nnote, coquille corrigée\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "coquille de la note", cwd=w)
        g("push", "-q", "origin", "travail-code", cwd=w); g("checkout", "-q", "main", cwd=w)
        r = C.passage(pl, T0 + 10 * M, dossier_etat=e71, ecrire=True, controles=False)
        voir("AD-79 (a) note corrigée par l'auteur pendant la relecture : ni LANCER COD, COD toujours non confirmée",
             "COD" not in r["lancer"] and "COD" in r["en_attente"] and r["etats"]["COD"]["ressource"] == "relecteur",
             (r["lancer"], sorted(r["en_attente"]), r["etats"]["COD"]))
        # N79 (b) — le relecteur pousse son RELU, puis l'auteur une note nouvelle, entre deux passages
        g("checkout", "-q", "travail-code", cwd=w); ecrire(w, "echanges/RELU.md", "RELU PAR : x\nVERDICT : À CORRIGER\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "relu", cwd=w)
        ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\nnote du tour suivant\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "note nouvelle", cwd=w)
        g("push", "-q", "origin", "travail-code", cwd=w); g("checkout", "-q", "main", cwd=w)
        r = C.passage(pl, T0 + 15 * M, dossier_etat=e71, ecrire=True, controles=False)
        voir("AD-79 (b) RELU puis note nouvelle : la relecture d'avant est terminée, COD relancée en relecture",
             "COD" in r["lancer"] and r["etats"]["COD"]["ressource"] == "relecteur",
             (r["lancer"], sorted(r["en_attente"]), r["etats"]["COD"]))
        # N-83 — la marque EN_COURS du relecteur, posée sur la branche À RELIRE : l'observation porte « relecteur »
        g("checkout", "-q", "travail-code", cwd=w); ecrire(w, "echanges/EN_COURS.md", "relecture en cours\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "marque du relecteur", cwd=w)
        g("push", "-q", "origin", "travail-code", cwd=w); g("checkout", "-q", "main", cwd=w)
        r = C.passage(pl, T0 + 20 * M, dossier_etat=e71, ecrire=True, controles=False)
        voir("AD-83 marque EN_COURS sur la branche À RELIRE : COD en cours SUR relecteur, une place relecteur, lancement gardé",
             r["etats"]["COD"]["etat"] == "en_cours" and r["etats"]["COD"]["ressource"] == "relecteur"
             and r["ressources"]["relecteur"]["prises"] == 1 and (r.get("vivants") or {}).get("COD", {}).get("demarre") is True,
             (r["etats"]["COD"], r["ressources"]["relecteur"], sorted(r.get("vivants") or {})))
        # N-85 (a) — l'entrée ÉCRITURE de la table : la note réécrite (« ## À JOUER SUR GITHUB ») sur une branche qui
        # reste en ÉCRITURE termine le lancement d'écriture (NOT relancée), et rien d'autre ne le fait
        etat_not = r["etats"]["NOT"]["action"]
        g("checkout", "-q", "travail-note", cwd=w)
        ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\nnote\n\n## À JOUER SUR GITHUB\n- Livraison\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "note réécrite", cwd=w)
        g("push", "-q", "origin", "travail-note", cwd=w); g("checkout", "-q", "main", cwd=w)
        r = C.passage(pl, T0 + 25 * M, dossier_etat=e71, ecrire=True, controles=False)
        voir("AD-85 note réécrite sur une branche qui reste ÉCRITURE : lancement terminé, NOT relancée",
             "[ÉCRITURE]" in etat_not and "[ÉCRITURE]" in r["etats"]["NOT"]["action"] and "NOT" in r["lancer"],
             (etat_not, r["etats"]["NOT"]["action"], r["lancer"], sorted(r["en_attente"])))
        # N-86 R1 — l'auteur rebase sa branche sur main pendant la relecture : même contenu du RELU, pas de redite
        g("checkout", "-qb", "travail-rebase", "main", cwd=w)
        ecrire(w, "programmes/r.py", "z = 1\n"); ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\ntour 1\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "tour 1", cwd=w)
        ecrire(w, "echanges/RELU.md", "RELU PAR : x\nVERDICT : À CORRIGER\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "relu du tour 1", cwd=w)
        ecrire(w, "echanges/A_RELIRE.md", "SERT : A-1\ntour 2\n")
        g("add", "-A", cwd=w); g("commit", "-qm", "tour 2", cwd=w)
        g("push", "-q", "origin", "travail-rebase", cwd=w); g("checkout", "-q", "main", cwd=w)
        pl6 = os.path.join(t, "planning_rebase")
        os.makedirs(pl6)
        for f in ("planning.csv", "ressources.csv"):
            shutil.copy(os.path.join(pl, f), pl6)
        ecrire(pl6, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "REB;rebase;;agent;agents;1;branche:travail-rebase;\n")
        e86 = os.path.join(t, "etat86")
        ra = C.passage(pl6, T0, dossier_etat=e86, ecrire=True, controles=False)
        relu_avant = g("log", "-1", "--format=%H", "origin/travail-rebase", "--", "echanges/RELU.md", cwd=w).strip()
        ecrire(w, "programmes/m.py", "m = 1\n"); g("add", "-A", cwd=w); g("commit", "-qm", "main avance", cwd=w)
        g("push", "-q", "origin", "main", cwd=w)
        g("checkout", "-q", "travail-rebase", cwd=w); g("rebase", "-q", "main", cwd=w)
        g("push", "-qf", "origin", "travail-rebase", cwd=w); g("checkout", "-q", "main", cwd=w)
        relu_apres = g("log", "-1", "--format=%H", "origin/travail-rebase", "--", "echanges/RELU.md", cwd=w).strip()
        rb = C.passage(pl6, T0 + 5 * M, dossier_etat=e86, ecrire=True, controles=False)
        voir("AD-86 rebase pendant la relecture (commit du RELU réécrit, contenu identique) : pas de redite LANCER REB",
             ra["lancer"] == ["REB"] and ra["etats"]["REB"]["ressource"] == "relecteur" and relu_avant != relu_apres
             and rb["lancer"] == [] and "REB" in rb["en_attente"],
             (ra["lancer"], relu_avant[:9], relu_apres[:9], rb["lancer"], sorted(rb["en_attente"])))
        # M10 / N-81 — l'état rangé est TOUJOURS dans la phase (un état qui change sans produit change la phase)
        phase = getattr(charger(chemin_adaptateur, "ADAPTATEUR_EPREUVE"), "phase_observee", lambda etat, f: "")
        meme = lambda f: "c1"   # noqa: E731 — le même commit pour tout fichier
        voir("AD-81 À ÉPROUVER puis ÉPREUVE ROUGE sans nouveau commit : la phase change",
             phase("À ÉPROUVER", meme) != phase("ÉPREUVE ROUGE", meme), (phase("À ÉPROUVER", meme), phase("ÉPREUVE ROUGE", meme)))
        gh = ecrire(t, "faux_gh.py", FAUX_GH)
        os.chmod(gh, 0o755)
        ecrire(t, "faux_gh.py.mode", "normal")
        C.passage(pl, T0, {"gh": gh}, dossier_etat=os.path.join(t, "etat"), ecrire=True, controles=False)
        r = C.passage(pl, T0 + 5 * M, {"gh": gh}, dossier_etat=os.path.join(t, "etat"), ecrire=False, controles=False)
        rel = r["ressources"]["relais"]
        voir("AD-R faux gh : 1 passage vivant, refus « file pleine » seul retenu (20h00 UTC), « clé inconnue » ignoré",
             rel["prises"] >= 1 and rel["dernier_refus"] == "2026-11-25T20:00:00+00:00" and not rel["refus_illisible"], rel)
        ecrire(t, "faux_gh.py.mode", "panne")
        r = C.passage(pl, T0 + 10 * M, {"gh": gh}, dossier_etat=os.path.join(t, "etat"), ecrire=False, controles=False)
        voir("AD-R journal du relais illisible : refus illisibles (jamais 0), code 4",
             r["ressources"]["relais"]["refus_illisible"] and r["code"] == 4, r["ressources"]["relais"])
        ecrire(pl, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "ABS;absente;;agent;agents;1;aucune;\n")
        try:
            C.passage(pl, T0, dossier_etat=os.path.join(t, "etat0"), ecrire=False, controles=False)
            voir("AD-P preuve « aucune » avec l'adaptateur CAC 40 : ARRET", False, "aucun arrêt")
        except C.Arret as ex:
            voir("AD-P preuve « aucune » avec l'adaptateur CAC 40 : ARRET", "lue par personne" in str(ex), ex)
        ecrire(pl, "etapes.csv", "etape;libelle;depend_de;executant;ressource;duree_h;preuve;etat\n"
               "ABS;absente;;agent;agents;1;branche:travail-absente;\n")
        r = C.passage(pl, T0, dossier_etat=os.path.join(t, "etat0"), ecrire=False, controles=False)
        voir("AD-P preuve « branche: » acceptée", r["etats"]["ABS"]["etat"] == "a_faire", r["etats"]["ABS"])
    except Exception as ex:
        echecs += 1
        if parler:
            print(f"ÉCHEC adaptateur : exception {type(ex).__name__} {ex}")
    finally:
        shutil.rmtree(t, True)
    return echecs


def une_mutation(k):
    """① RÔLE — Jouer UNE mutation dans ce processus : copier le fichier visé, le muter, rejouer la suite concernée.
    ② CONTEXTE D'APPEL — `mutations`, par un sous-processus « --une-mutation=K » borné par DELAI_MUTATION_S.
    ③ ENTRÉE — `k` : l'indice dans MUTATIONS.
    ④ CONDITIONS D'ENTRÉE — le texte « avant » existe UNE fois dans le fichier visé.
    ⑤ SORTIE — UNE valeur : 0 la suite reste verte (mutation SURVIVANTE) · 1 la suite rougit (TUÉE) · 2 texte introuvable.
    ⑥ TRAITEMENT — copie dans un dossier temporaire (avec ETAT_DES_TRAVAUX.py pour l'adaptateur), remplacement,
      chargement, suite muette.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 ; un processus par mutation pour qu'une mutation qui pend soit bornée (relecture du
      25-11-2026 : la suppression de la détection de cycle faisait PENDRE la suite).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — dossier temporaire.
    ⑪ TERMINAISON — peut pendre si la copie abîmée boucle : c'est le lanceur qui la borne.
    """
    cible, nom, avant, apres = MUTATIONS[k]
    source = {"coeur": COEUR, "defauts": DEFAUTS, "adaptateur": ADAPT}[cible]
    src = open(source, encoding="utf-8").read()
    if src.count(avant) != 1:
        return 2
    t = tempfile.mkdtemp(prefix="mutation_")
    try:
        if cible == "adaptateur":
            shutil.copy(os.path.join(PROG, "ETAT_DES_TRAVAUX.py"), t)
            c = ecrire(t, "ADAPTATEUR_PILOTAGE_CAC40.py", src.replace(avant, apres))
            n = epreuve_de_l_adaptateur(c, parler=False)
        else:
            c = ecrire(t, f"m{k}.py", src.replace(avant, apres))
            m = charger(c, f"m{k}")
            n = epreuves_du_coeur(m, parler=False) if cible == "coeur" else epreuves_des_defauts(m, parler=False)
    except Exception:
        n = 1
    finally:
        shutil.rmtree(t, True)
    return 1 if n else 0


def mutations():
    """① RÔLE — Rejouer les suites contre chaque copie abîmée ; chacune doit rougir.
    ② CONTEXTE D'APPEL — `main --mutations`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0 toutes tuées, 1 une survivante, 2 un texte introuvable.
    ⑥ TRAITEMENT — un sous-processus par mutation (python3 -I ce fichier --une-mutation=K), délai DELAI_MUTATION_S ;
      code 1 ou délai dépassé → TUÉE ; 0 → SURVIVANTE ; 2 → INTROUVABLE.
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — R-731.
    ⑨ CE QUI CLOCHE — une mutation qui pend est dite tuée : le comportement change, mais l'épreuve n'a pas conclu.
    ⑩ EFFET — affichage.
    ⑪ TERMINAISON — chaque sous-processus est tué au bout de DELAI_MUTATION_S.
    """
    code = 0
    for k, (cible, nom, _, _) in enumerate(MUTATIONS):
        try:
            p = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), f"--une-mutation={k}"],
                               capture_output=True, text=True, timeout=DELAI_MUTATION_S)
            r = p.returncode
            etiquette = {1: "TUÉE    ", 0: "SURVIVANTE", 2: "INTROUVABLE"}.get(r, f"ERREUR {r}")
        except subprocess.TimeoutExpired:
            r, etiquette = 1, "TUÉE (délai)"
        print(f"{etiquette} [{cible}] {nom}")
        if r == 2 or r not in (0, 1):
            code = 2
        elif r == 0 and code == 0:
            code = 1
    return code


def main(argv):
    """① RÔLE — Lancer les épreuves.
    ② CONTEXTE D'APPEL — ligne de commande.
    ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code (voir ⑤ du module).
    ⑥ TRAITEMENT — --une-mutation=K → `une_mutation` seule ; sinon cœur, défauts, adaptateur, puis mutations sur
      demande.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — affichage.
    ⑪ TERMINAISON — revient.
    """
    for a in argv[1:]:
        if a.startswith("--une-mutation="):
            return une_mutation(int(a.split("=", 1)[1]))
    n = epreuves_du_coeur(charger(COEUR)) + epreuves_des_defauts(charger(DEFAUTS, "defauts")) + epreuve_de_l_adaptateur()
    print(f"BILAN : {n} échec(s)")
    code = 1 if n else 0
    if "--mutations" in argv:
        m = mutations()
        code = 2 if m == 2 else max(code, m)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
