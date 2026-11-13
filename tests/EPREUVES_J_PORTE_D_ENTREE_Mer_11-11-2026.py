#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DE J — LA PORTE D'ENTRÉE `juger_une_fiche`, de bout en bout, sur un dépôt à vérité connue.
Simulation uniquement. Mercredi 11-11-2026.

LE SENS EN TÊTE — Le superviseur R-759 du 11-11-2026 (lot B, point 3 ③) demande « UNE épreuve à vérité connue, de bout
en bout, sur un faux dépôt construit par l'épreuve », et « Sabotage obligatoire : la porte qui renvoie [] au lieu de
lire doit rougir ». Cette épreuve FABRIQUE un dépôt git dans /tmp, où l'on sait d'avance la réponse :
  · trois valeurs réelles (AIRBUS, TOTALENERGIES, VINCI), aux séances réelles du calendrier 2024-2025, avec des cours
    FABRIQUÉS : un bruit faible qui ne baisse jamais de 3 % en un jour, et, environ toutes les cinq séances, sur une
    des trois valeurs, une baisse de 3,5 % suivie, 17 fois sur 20, de trois hausses de 2 % (sinon trois baisses de
    1,5 %) ;
  · une stratégie VRAIMENT BONNE : acheter le lendemain d'une baisse de 3 % ou plus — elle voit exactement l'événement
    fabriqué ;
  · une stratégie TIRÉE AU HASARD : des jours choisis par l'empreinte de la date, sans rapport avec les cours ;
  · des déclarations datées, commitées, et des fiches qui en manquent, en ont une incomplète, non commitée, dont les
    années d'examen recouvrent les années de réglage, ou dont une vente tombe après la fin des années d'examen.
Puis elle appelle `juger_une_fiche(racine, fiche, cas)` — rien d'autre — et confronte chaque verdict à la vérité.

① RÔLE — Éprouver la porte et ses lectures (déclaration, k, calendrier, registre des essais, jeu), pas la grille
  (gelée, éprouvée par le lot B).
② CONTEXTE D'APPEL — À la main : `python3 -B tests/EPREUVES_J_PORTE_D_ENTREE_Mer_11-11-2026.py <racine>` (Z0 seul),
  ou `… <racine> --saboter` (Z0 puis chaque sabotage), ou `… <racine> --sabotage=S01_…` (Z0 puis ce sabotage). La racine est celle d'un clone du dépôt (les programmes et les
  fichiers de l'indice et du calendrier sont copiés depuis elle).
③ ENTRÉE — La ligne de commande.
④ CONDITIONS D'ENTRÉE — git ; environ 10 Mo libres dans /tmp.
⑤ SORTIE — Code 0 si tout est vert (et, avec --saboter, si chaque sabotage mord), 1 sinon, 2 si l'usage est faux.
⑥ TRAITEMENT — Pour Z0 et chaque sabotage : fabriquer un dépôt neuf, appliquer le sabotage à SA copie de la porte,
  relancer ce programme en « --cas » dans un processus à part, lire les cas, effacer le dépôt.
⑦ UNITÉ — Des cas.
⑧ POURQUOI — R-731, R-732 (un cas vient d'une vraie ligne : la ligne C5E10-QA-V1 du registre sert de modèle aux
  fiches), R-734.
⑨ CE QUI CLOCHE — ① « Validée » n'est atteinte qu'avec les MESURES SANS AUTEUR simulées par l'épreuve (voisins, frais
  doublés, gain et creux en un jeton, et en cas 2 surapprentissage et Sharpe dégonflé) : sans elles, la porte rend
  NON TRANCHÉE (MESURE MANQUANTE voisins), ce que V1 vérifie. ② La table de la loi du dépôt fabriqué est la table
  synthétique du lot B (rôles de Q-G2 et Q-G3 posés), pas celle du REGISTRE, où ils manquent.
⑩ EFFET — Crée puis efface des dossiers /tmp/J_porte_* ; lance git et python. Depuis la mission REGARD (12-11-2026),
  chaque dépôt fabriqué a son dépôt distant NU LOCAL (`.depot_nu`, jamais GitHub), où la porte pousse ses regards ; un
  sabotage est commité et poussé (la porte exige HEAD = la branche principale et un arbre propre).
⑪ TERMINAISON — Chaque relance est bornée à 600 s.
"""

import csv
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.abspath(__file__)
PORTE = "programmes/JUGER_UNE_FICHE.py"
VALEURS = (("AIRBUS", "AIR"), ("TOTALENERGIES", "TTE"), ("VINCI", "DG"))
DEBUT, FIN = "2024-01-02", "2025-12-31"
FICHIERS_COPIES = ("emp.py", "donnees/CALENDRIER_EURONEXT.csv", "donnees/NATURE_DES_TROUS.csv",
                   "donnees/BAREME_FRAIS.csv", "donnees/VALEURS_TTF.csv", "donnees/sources_indice/INDICE_CAC40.csv",
                   "donnees/sources_indice/PASSAGES_DANS_LE_CAC40.csv",
                   "donnees/sources_indice/IDENTITES_DES_SOCIETES.csv", "donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv")
DATE_REGISTRE = "2026-11-01T12:00:00+01:00"
DATE_DECLARATIONS = "2026-11-02T12:00:00+01:00"
DECLAREE_LE = "2026-11-02T10:00+01:00"

SIGNAL_BON = '''"""Signal de l'épreuve J.
DÉCIDÉ · module de signal · Rôle : acheter le lendemain d'une baisse de 3 % ou plus (épreuve J, vérité connue).
"""


def baisse(serie):
    """Rend les rangs des séances en baisse de 3 % ou plus."""
    return [{"i": i} for i in range(1, len(serie)) if serie[i]["close"] / serie[i - 1]["close"] - 1 <= -0.03]
'''
SIGNAL_HASARD = '''"""Signal de l'épreuve J.
DÉCIDÉ · module de signal · Rôle : acheter des jours tirés par l'empreinte de leur date (épreuve J, vérité connue).
"""
import hashlib


def tirage(serie):
    """Rend les rangs des séances dont l'empreinte de la date tombe sur 0 modulo 5."""
    return [{"i": i} for i in range(len(serie))
            if int(hashlib.sha256(str(serie[i]["date"]).encode()).hexdigest(), 16) % 5 == 0]
'''

# LES SABOTAGES : (fichier de la copie, texte visé, remplacement, cas qui DOIT rougir)
SABOTAGES = {
    "S01_regards_vides_au_lieu_de_lire": (
        PORTE, 'entrees["regards_anterieurs"] = bilan["regards"]', 'entrees["regards_anterieurs"] = []', "V3"),
    "S02_seances_hors_examen_a_zero": (PORTE, "    return n, \"\"\n", "    return 0, \"\"\n", "V6"),
    "S03_declaration_non_complete_jouee": (PORTE, 'if lecture["etat"] != C.ETATS_DE_LA_LECTURE_DE_LA_DECLARATION[0]:',
                                           "if False:", "V7"),
    "S04_le_regard_se_compte_lui_meme": (PORTE, 'decl["temoins"], sauf=(nom,))', 'decl["temoins"], sauf=())', "V2"),
    "S05_liste_vide_au_lieu_de_la_lecture": (PORTE, 'declaration_manquants=lecture["champs_en_defaut"])',
                                             "declaration_manquants=[])", "V5"),
    "S06_trop_peu_de_tirages": (PORTE, "n = int(1.0 / s_hasard) + 1", "n = int(1.0 / s_hasard) - 1", "V2"),
    "S07_cas_de_l_appelant_cru": (PORTE, 'cas_retenu = lu["cas_declare"] if str(cas).strip() == lu["cas_declare"] else None',
                                  "cas_retenu = str(cas).strip()", "V9"),
    "S08_vente_non_comptee": (PORTE, 'for cle in ("date_entree", "date_sortie"):', 'for cle in ("date_entree",):', "V10"),
    "S12_calendrier_aminci": (PORTE, "CAL.seances_entre(bornes[0], bornes[1], sc)]",
                              "CAL.seances_entre(bornes[0], bornes[1], sc)][::2]", "V2"),
    "S13_k_vaut_un": (PORTE, 'entrees["k"] = k', 'entrees["k"] = 1', "V12"),
    "S16_branche_choisie_par_l_appelant": (PORTE, "def juger_une_fiche(racine, fiche_id, cas):",
                                           "def juger_une_fiche(racine, fiche_id, cas, branche=None):",
                                           "V14"),
    "S17_disque_sans_la_branche_accepte": (PORTE, "    if not est:\n", "    if False:\n", "V15"),
    "S15_bilan_d_une_autre_fiche": (PORTE, "bilan = TR.bilan_de_la_fiche(racine, fiche_id,",
                                    'bilan = TR.bilan_de_la_fiche(racine, "PERSONNE",', "V13"),
    "S14_la_porte_fabrique_la_liste_des_manquants": (
        PORTE, 'declaration_manquants=lecture["champs_en_defaut"])',
        'declaration_manquants=C.champs_de_la_declaration_manquants(lecture["declaration"]))', "V7b"),
    "S10_regard_non_preenregistre": (PORTE, "nom = TR.preenregistrer(racine, fiche_id, hypothese, declaration=decl)",
                                     'nom = "0000000000000000"', "V3"),
    "S11_annees_de_reglage_ignorees": (PORTE, "interdites = [reglage] + vues", "interdites = vues", "V6"),
}


def seances(racine):
    """Rend les séances du calendrier réel entre DEBUT et FIN.
    ① RÔLE — Donner aux cours fabriqués les séances vraies. ② CONTEXTE D'APPEL — `fabriquer`. ③ ENTRÉE — la racine
    source. ④ CONDITIONS D'ENTRÉE — calendrier lisible. ⑤ SORTIE — UNE valeur : liste de textes AAAA-MM-JJ. [rend: 1]
    ⑥ TRAITEMENT — `CALENDRIER_DE_LA_BOURSE.seances_entre`. ⑦ UNITÉ — séances. ⑧ POURQUOI — le lecteur unique refuse
    une barre hors calendrier. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    from datetime import date
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import CALENDRIER_DE_LA_BOURSE as CAL
    sc = CAL.lire_les_seances(racine)
    return [d.isoformat() for d, _ in CAL.seances_entre(date.fromisoformat(DEBUT), date.fromisoformat(FIN), sc)]


def cours_fabriques(dates):
    """Fabrique les cours à vérité connue et rend les barres et les événements.
    ① RÔLE — Poser la vérité : une baisse de 3,5 % est suivie 17 fois sur 20 d'une hausse. ② CONTEXTE D'APPEL —
    `fabriquer`. ③ ENTRÉE — les séances. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs : les lignes du fichier
    de cours, la liste des événements (rang, valeur, réussi). [rend: 2] ⑥ TRAITEMENT — bruit borné à ±1 %, moins une
    dérive qui compense les événements ; un événement toutes les 5 séances, sur une valeur à tour de rôle.
    ⑦ UNITÉ — euros, séances. ⑧ POURQUOI — sans dérive, le hasard ne gagne rien ; avec l'événement, le signal gagne.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    alea = random.Random(20261111)
    evenements = {}
    for e, t in enumerate(range(10, len(dates) - 6, 5)):
        evenements[(t, e % 3)] = (e * 7) % 20 >= 3
    lignes = []
    for v, (nom, _m) in enumerate(VALEURS):
        c, suite = 100.0, {}
        for t, d in enumerate(dates):
            ouverture = c * (1 + alea.uniform(-0.001, 0.001))
            if (t, v) in evenements:
                r = -0.035
                for u in (1, 2, 3):
                    suite[t + u] = evenements[(t, v)]
            elif t in suite:
                r = 0.02 if suite[t] else -0.015
                ouverture = c * (1.002 if suite[t] else 0.998)
            else:
                r = alea.uniform(-0.01, 0.01) - 0.0007
            cloture = c * (1 + r)
            haut, bas = max(ouverture, cloture) * 1.004, min(ouverture, cloture) * 0.996
            lignes.append([nom, d, "%.4f" % ouverture, "%.4f" % haut, "%.4f" % bas, "%.4f" % cloture, "100000", "google"])
            c = cloture
    return lignes, sorted(evenements.items())


def fabriquer(source, dossier):
    """Fabrique le dépôt à vérité connue dans `dossier` et rend ce que l'épreuve doit en savoir.
    ① RÔLE — Construire la racine que la porte lira. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine source, un
    dossier vide. ④ CONDITIONS D'ENTRÉE — git. ⑤ SORTIE — UNE valeur : {fin_coupee}. [rend: 1]
    ⑥ TRAITEMENT — copier programmes et fichiers de l'indice ; écrire la table de la loi, les cours, les signaux, le
    registre des stratégies (modèle : la vraie ligne C5E10-QA-V1, R-732), les déclarations ; deux commits datés ; la
    branche principale ; puis une déclaration écrite sur le disque seulement (V8). ⑦ UNITÉ — —. ⑧ POURQUOI — vérité
    connue. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit sous `dossier`. ⑪ TERMINAISON — Rend la main ; git peut bloquer.
    [sort: non]"""
    shutil.copytree(os.path.join(source, "programmes"), os.path.join(dossier, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    for f in FICHIERS_COPIES:
        os.makedirs(os.path.dirname(os.path.join(dossier, f)) or dossier, exist_ok=True)
        shutil.copy(os.path.join(source, f), os.path.join(dossier, f))
    ref = [f for f in os.listdir(os.path.join(source, "donnees")) if f.startswith("REFERENTIEL_VALEURS")]
    for f in ref:
        shutil.copy(os.path.join(source, "donnees", f), os.path.join(dossier, "donnees", f))
    sys.path.insert(0, os.path.join(source, "tests"))
    b = charger(os.path.join(source, "tests", "EPREUVES_B_DU_BLOC_5A_Mer_11-11-2026.py"), "epreuve_b_table")
    os.makedirs(os.path.join(dossier, "gouvernance"))
    with open(os.path.join(dossier, "gouvernance", "REGISTRE_REGLES.md"), "w", encoding="utf-8") as f:
        f.write(b.TABLE_SYNTHETIQUE.format(c7="condition", emb="30"))
    dates = seances(source)
    lignes, evenements = cours_fabriques(dates)
    with open(os.path.join(dossier, "donnees", "cours_maitre.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["valeur", "date", "open", "high", "low", "close", "volume", "source"])
        w.writerows(lignes)
    for nom, texte in (("SIGNAL_J_BON.py", SIGNAL_BON), ("SIGNAL_J_HASARD.py", SIGNAL_HASARD)):
        open(os.path.join(dossier, "programmes", nom), "w", encoding="utf-8").write(texte)
    # LE REGISTRE DES STRATÉGIES : une VRAIE ligne (C5E10-QA-V1) comme modèle, R-732
    with open(os.path.join(source, "donnees", "cac40_strategies.csv"), encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f)
        entete = lecteur.fieldnames
        modele = [l for l in lecteur if l["id"] == "C5E10-QA-V1"][-1]
    univers = ",".join(m for _n, m in VALEURS)
    fiches = []
    for ident, module, fonction in (("BONNE-A", "SIGNAL_J_BON.py", "baisse"), ("BONNE-B", "SIGNAL_J_BON.py", "baisse"),
                                    ("BONNE-C", "SIGNAL_J_BON.py", "baisse"), ("HASARD", "SIGNAL_J_HASARD.py", "tirage"),
                                    ("SANS-DECL", "SIGNAL_J_BON.py", "baisse"), ("REGLAGE", "SIGNAL_J_BON.py", "baisse"),
                                    ("INCOMPLETE", "SIGNAL_J_BON.py", "baisse"),
                                    ("NON-ENGAGEE", "SIGNAL_J_BON.py", "baisse"),
                                    ("FIN-COUPEE", "SIGNAL_J_BON.py", "baisse"),
                                    ("FILLE-A", "SIGNAL_J_BON.py", "baisse")):
        l = dict(modele)
        l.update(id=ident, nom="épreuve J " + ident, note="épreuve J", univers=univers, etat_vie="LABO",
                 periode="%s -> %s" % (DEBUT, FIN), module_signal="programmes/" + module, fonction_signal=fonction,
                 reglages_signal="", tp="+4.0%", sl="-2.5%", horizon="20")
        fiches.append(l)
    with open(os.path.join(dossier, "donnees", "cac40_strategies.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=entete)
        w.writeheader()
        w.writerows(fiches)
    git = lambda *a, date=None: subprocess.run(["git", "-C", dossier] + list(a), check=True, capture_output=True,
                                               env=dict(os.environ, GIT_AUTHOR_DATE=date or "",
                                                        GIT_COMMITTER_DATE=date or ""))
    git("init", "-q", "-b", "main")
    git("config", "user.email", "epreuve@j")
    git("config", "user.name", "epreuve J")
    # MISSION REGARD (12-11-2026) : la porte exige HEAD = la branche principale ET un arbre propre ; le registre des
    # essais vit sur la branche des regards d'un DÉPÔT DISTANT — ici un dépôt nu local, jamais GitHub.
    open(os.path.join(dossier, ".gitignore"), "w", encoding="utf-8").write("__pycache__/\n.depot_nu/\n")
    nu = os.path.join(dossier, ".depot_nu")
    subprocess.run(["git", "init", "-q", "--bare", nu], check=True, capture_output=True)
    git("remote", "add", "origin", nu)
    poser_le_depot_commun(dossier, nu)
    git("add", "-A")
    git("commit", "-q", "-m", "dépôt à vérité connue", date=DATE_REGISTRE)
    # LES DÉCLARATIONS
    sys.path.insert(0, os.path.join(dossier, "programmes"))
    import CONTRATS_DES_FICHIERS as C
    import DECLARER_UNE_STRATEGIE as DS
    empreintes = {m: DS.empreintes_du_code(dossier, "programmes/" + m) for m in ("SIGNAL_J_BON.py", "SIGNAL_J_HASARD.py")}
    milieu = dates[len(dates) // 2]
    base = {c: "épreuve J" for c in C.DECLARATION_DATEE}
    base.update(date_declaration=DECLAREE_LE, cas="1", periode_conception="2022-01-03..2023-12-29",
                part_regardee="aucune", date_regle_univers="2026-11-01", lignee="aucune", parametres_libres="0",
                annees_d_examen="%s..%s" % (DEBUT, FIN), regard_sans_decision="", reglages="{}", temoins="aucun",
                epoques="%s..%s ; %s..%s" % (DEBUT, dates[len(dates) // 2 - 1], milieu, FIN))
    # FIN-COUPEE : les années d'examen finissent le lendemain d'un événement réussi — l'achat y est, la vente non
    t_coupe = max(t for (t, _v), ok in evenements if ok and t < len(dates) - 30)
    fin_coupee = dates[t_coupe + 1]
    declarations = []
    for ident in ("BONNE-A", "BONNE-B", "BONNE-C", "HASARD", "REGLAGE", "INCOMPLETE", "FIN-COUPEE", "FILLE-A"):
        d = dict(base, fiche_id=ident)
        juge, signal = empreintes["SIGNAL_J_HASARD.py" if ident == "HASARD" else "SIGNAL_J_BON.py"]
        d.update(empreinte_code_juge=juge, empreinte_code_signal=signal)
        if ident == "REGLAGE":
            d["periode_conception"] = "2025-01-02..2025-12-31"
        if ident == "INCOMPLETE":
            # l'hypothèse vide, et non la lignée : une lignée illisible dans UNE déclaration rend la lignée de TOUTES
            # les fiches inconnue chez B2 (mesuré à la fusion de B2, note J) — elle rendrait tout le dépôt NON JUGEABLE
            d["hypothese"] = ""
            # ET une forme fautive NON VIDE (12-11-2026) : « deux » n'est pas un champ manquant, seulement un champ en
            # défaut que SEULE la lecture contrôlée de B3 voit ; S14 (la porte refabrique la liste par
            # `champs_de_la_declaration_manquants`) survivait depuis que V8 ne lit plus la déclaration (arbre sali)
            d["parametres_libres"] = "deux"
        if ident == "FILLE-A":
            d["lignee"] = "BONNE-A → FILLE-A"
        if ident == "FIN-COUPEE":
            d.update(annees_d_examen="%s..%s" % (DEBUT, fin_coupee),
                     epoques="%s..%s ; %s..%s" % (DEBUT, dates[len(dates) // 2 - 1], milieu, fin_coupee))
        declarations.append(d)
    chemin = os.path.join(dossier, C.DECLARATIONS_DATEES)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=C.DECLARATION_DATEE)
        w.writeheader()
        w.writerows(declarations)
    git("add", "-A")
    git("commit", "-q", "-m", "déclarations datées", date=DATE_DECLARATIONS)
    git("push", "-q", "origin", "main")
    git("fetch", "-q", "origin")
    # V8 : la ligne NON-ENGAGEE n'est PLUS écrite ici (elle salirait l'arbre de tous les cas) : V8 l'écrit, juge, efface.
    with open(os.path.join(dossier, ".ligne_non_engagee.json"), "w", encoding="utf-8") as f:
        json.dump(dict(base, fiche_id="NON-ENGAGEE", empreinte_code_juge=empreintes["SIGNAL_J_BON.py"][0],
                       empreinte_code_signal=empreintes["SIGNAL_J_BON.py"][1]), f, ensure_ascii=False)
    with open(os.path.join(dossier, ".git", "info", "exclude"), "a", encoding="utf-8") as f:
        f.write("\n.ligne_non_engagee.json\n")
    return {"fin_coupee": fin_coupee}


def poser_le_depot_commun(dossier, adresse):
    """Écrit `adresse` comme dépôt commun au fichier des réglages du dépôt fabriqué (clé `depot_des_regards`).
    ① RÔLE — Depuis la mission REGARD (tour 2), seul le dépôt commun inscrit et lit les regards ; le dépôt fabriqué
    a pour dépôt commun son dépôt nu local. ② CONTEXTE D'APPEL — `fabriquer` ; l'épreuve du regard unique. ③ ENTRÉE —
    le dossier, l'adresse. ④ CONDITIONS D'ENTRÉE — le fichier des réglages est copié. ⑤ SORTIE — aucune valeur.
    [rend: 0] ⑥ TRAITEMENT — retirer la ligne `depot_des_regards`, en ajouter une. ⑦ UNITÉ — —. ⑧ POURQUOI — la
    vraie ligne nomme GitHub. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit le fichier. ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    chemin = os.path.join(dossier, "donnees", "REGLAGES_DU_REGISTRE_DES_ESSAIS.csv")
    lignes = [l for l in open(chemin, encoding="utf-8").read().splitlines(True) if not l.startswith("depot_des_regards,")]
    lignes[-1] = lignes[-1] if lignes[-1].endswith("\n") else lignes[-1] + "\n"
    open(chemin, "w", encoding="utf-8").write("".join(lignes) + "depot_des_regards,%s,épreuve,épreuve\n" % adresse)


def charger(chemin, nom):
    """Charge un programme par son chemin.
    ① RÔLE — prendre un module d'un dossier précis. ② CONTEXTE D'APPEL — `fabriquer`, `cas`. ③ ENTRÉE — chemin, nom.
    ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT —
    spec_from_file_location. ⑦ UNITÉ — —. ⑧ POURQUOI — la copie, pas le dépôt. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — exécute
    le module. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


def pieces_a_venir(P):
    """Simule les mesures qui n'ont pas encore d'auteur, avec des valeurs que la vérité fabriquée justifie.
    ① RÔLE — Atteindre « Validée » de bout en bout, en le disant. ② CONTEXTE D'APPEL — `cas`, V2 et V9. ③ ENTRÉE — le
    module de la porte. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : l'ancien MESUREURS. [rend: 1]
    ⑥ TRAITEMENT — un module de mesures simulées, rangé dans sys.modules ; les None de
    `CONTRATS_DES_FICHIERS.MESUREURS_DU_JUGE` remplacés par ses noms (depuis la mission REGARD, les mesureurs sont
    DÉCLARÉS au contrat, plus dans un dictionnaire de la porte). ⑦ UNITÉ — euros. ⑧ POURQUOI — la porte ne les écrit
    pas (R-708). ⑨ CE QUI CLOCHE — ce sont des SIMULATIONS : elles ne prouvent rien des futurs auteurs ; et c'est une
    mutation du contrat chargé en mémoire (limite J1 de la porte, écrite). ⑩ EFFET — modifie le contrat chargé.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    import types
    C = sys.modules["CONTRATS_DES_FICHIERS"]
    ancien = dict(C.MESUREURS_DU_JUGE)
    moy = lambda xs: sum(xs) / len(xs)
    simulees = types.ModuleType("MESURES_SIMULEES_DE_L_EPREUVE_J")
    sys.modules[simulees.__name__] = simulees
    fonctions = dict(
        voisins=lambda r, f, ops: ({"n_voisins": 26, "n_voisins_gagnants": 26, "ecart_pct": 10}, ""),
        frais_doubles=lambda r, f, ops: ({"gain_moyen_frais_doubles_eur": moy([o["net"] - o["frais"] for o in ops]),
                                          "multiplicateur_des_frais": 2}, ""),
        gain_un_jeton=lambda r, f, ops: ({"gain_un_jeton_eur": sum(o["net"] for o in ops)}, ""),
        creux_un_jeton=lambda r, f, ops: ({"creux_un_jeton_eur": 0.0}, ""),
        surapprentissage=lambda r, f, ops: ({"pbo": 0.1, "nombre_d_essais": 10 ** 6}, ""),
        sharpe_degonfle=lambda r, f, ops: ({"sharpe_degonfle": 0.9999, "nombre_d_essais": 10 ** 6}, ""))
    for cle, fn in fonctions.items():
        setattr(simulees, cle, fn)
        C.MESUREURS_DU_JUGE[cle] = "%s.%s" % (simulees.__name__, cle)
    return ancien


def cas(dossier):
    """Juge chaque fiche du dépôt fabriqué par la porte de SA copie, et confronte à la vérité.
    ① RÔLE — Les cas V1 à V15. ② CONTEXTE D'APPEL — `main` en « --cas ». ③ ENTRÉE — le dépôt fabriqué.
    ④ CONDITIONS D'ENTRÉE — fabriqué par `fabriquer`. ⑤ SORTIE — UNE valeur : liste de (nom, vert, détail). [rend: 1]
    ⑥ TRAITEMENT — appeler `juger_une_fiche`, lire verdict, motif, premier contrôle bloquant, états, k lu. ⑦ UNITÉ — —.
    ⑧ POURQUOI — la vérité est connue d'avance. ⑨ CE QUI CLOCHE — l'ordre compte : V3 rejuge BONNE-A après V1.
    ⑩ EFFET — la porte écrit au registre des essais du dépôt fabriqué. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    sys.path.insert(0, os.path.join(dossier, "programmes"))
    P = charger(os.path.join(dossier, PORTE), "porte_j")
    C = sys.modules["CONTRATS_DES_FICHIERS"]
    VAL, NJ, NT = C.MOTS_DU_VERDICT[0], C.MOTS_DU_VERDICT[3], C.MOTS_DU_VERDICT[2]
    T = sys.modules["TENIR_LE_REGISTRE_DES_ESSAIS"]
    nb_essais = lambda: len(T.lire_le_registre(dossier)[0])      # la branche des regards (mission REGARD)
    res = []

    def ok(nom, vert, detail):
        """Range un cas. ① RÔLE — noter. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, booléen, détail.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune. [rend: 0] ⑥ TRAITEMENT — ajouter. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        res.append((nom, bool(vert), detail))

    def juger(fiche, c="1"):
        """Juge une fiche ; une exception devient un rendu. ① RÔLE — isoler. ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — fiche, cas. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : le rendu ou {"erreur"}. [rend: 1]
        ⑥ TRAITEMENT — appeler. ⑦ UNITÉ — —. ⑧ POURQUOI — un cas qui lève est rouge, pas une épreuve qui tombe.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — celui de la porte. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        try:
            return P.juger_une_fiche(dossier, fiche, c)
        except Exception as e:
            return {"erreur": "%s: %s" % (type(e).__name__, e), "verdict": None, "motif": "", "controles": {},
                    "premier_controle_bloquant": ""}

    etats = lambda r: {k: v["etat"] for k, v in r.get("controles", {}).items()}
    dit = lambda r: "%s · %s · %s · %s" % (r.get("verdict"), r.get("motif"), r.get("premier_controle_bloquant"),
                                          r.get("erreur") or r.get("lu", {}).get("raisons"))
    mesures = ("declaration", "annees_d_examen", "regard_unique", "observations_independantes", "gain_bat_zero",
               "bat_le_hasard", "epoques", "kelly", "taux_face_au_point_mort", "borne_basse_du_gain")
    # V14 — la porte ne reçoit RIEN d'autre que la racine, la fiche et le cas : ni branche, ni instant du regard
    import inspect
    noms = list(inspect.signature(P.juger_une_fiche).parameters)
    ok("V14 signature de la porte = (racine, fiche_id, cas) : branche et instant fixés par la porte, jamais choisis",
       noms == ["racine", "fiche_id", "cas"], str(noms))
    # V1 — BONNE-A, mesures sans auteur ABSENTES : tout ce que la porte mesure passe ; le premier manque est nommé
    r = juger("BONNE-A")
    e = etats(r)
    ok("V1 bonne, mesures sans auteur absentes : NON TRANCHÉE (MESURE MANQUANTE voisins), ①-⑦, ⑨ et C7/C8 PASSE",
       r["verdict"] == NT and r["motif"] == "MESURE MANQUANTE voisins" and all(e.get(m) == "PASSE" for m in mesures)
       and e.get("surapprentissage") == "SANS_OBJET", dit(r) + " · " + str(e))
    # V2 — BONNE-B, mesures sans auteur SIMULÉES : Validée
    ancien = pieces_a_venir(P)
    r = juger("BONNE-B")
    ok("V2 bonne, pièces à venir simulées : Validée", r["verdict"] == VAL, dit(r) + " · " + str(etats(r)))
    # V12 — k est LU au registre des stratégies à la date de la déclaration : 9 fiches, 9 versions, aucun témoin
    kk = (r.get("lu") or {}).get("k") or {}
    ok("V12 k lu au registre (10 versions, 0 témoin), seuil de preuve = 0,05 ÷ 10", kk.get("valeur") == 10
       and kk.get("versions_comptees") == 10 and r.get("seuil_de_preuve") == 0.05 / 10,
       "k %r · seuil %r" % (kk, r.get("seuil_de_preuve")))
    # V9 — BONNE-C, l'appelant dit cas 2, la déclaration dit 1 : jamais Validée
    r = juger("BONNE-C", "2")
    ok("V9 cas 2 annoncé, cas 1 déclaré : pas Validée, ⑧ INCONNU", r["verdict"] != VAL
       and etats(r).get("surapprentissage") == "INCONNU", dit(r))
    # V10 — FIN-COUPEE : une vente après la fin des années d'examen
    r = juger("FIN-COUPEE")
    ok("V10 vente après la fin des années d'examen : NON TRANCHÉE (DONNÉES DE CHOIX) par ②", r["verdict"] == NT
       and r["motif"] == "DONNÉES DE CHOIX" and r["premier_controle_bloquant"] == "annees_d_examen", dit(r))
    C.MESUREURS_DU_JUGE.clear()
    C.MESUREURS_DU_JUGE.update(ancien)
    # V3 — BONNE-A rejugée : ses années ont déjà été regardées (V1)
    r = juger("BONNE-A")
    ok("V3 années déjà regardées (2e jugement de BONNE-A) : NON TRANCHÉE (DONNÉES DE CHOIX) par ③", r["verdict"] == NT
       and r["motif"] == "DONNÉES DE CHOIX" and r["premier_controle_bloquant"] == "regard_unique", dit(r))
    # V13 — FILLE-A, de la lignée de BONNE-A (déclarée « BONNE-A → FILLE-A ») : les années regardées par sa mère
    r = juger("FILLE-A")
    ok("V13 fille d'une fiche déjà regardée (lignée déclarée) : NON TRANCHÉE (DONNÉES DE CHOIX) par ③",
       r["verdict"] == NT and r["motif"] == "DONNÉES DE CHOIX" and r["premier_controle_bloquant"] == "regard_unique",
       dit(r))
    # V4 — HASARD : refusée
    r = juger("HASARD")
    ok("V4 stratégie tirée au hasard : refusée (gain ou hasard BLOQUE)", r["verdict"] in (NT, C.MOTS_DU_VERDICT[1])
       and (etats(r).get("gain_bat_zero") == "BLOQUE" or etats(r).get("bat_le_hasard") == "BLOQUE"), dit(r))
    # V5 — SANS-DECL : NON JUGEABLE, et AUCUN regard inscrit
    avant = nb_essais()
    r = juger("SANS-DECL")
    ok("V5 sans déclaration : NON JUGEABLE, aucun regard inscrit", r["verdict"] == NJ and nb_essais() == avant,
       dit(r) + " · essais %d → %d" % (avant, nb_essais()))
    # V6 — REGLAGE : années d'examen = années de réglage
    r = juger("REGLAGE")
    ok("V6 années de réglage dans les années d'examen : NON TRANCHÉE (DONNÉES DE CHOIX) par ②", r["verdict"] == NT
       and r["motif"] == "DONNÉES DE CHOIX" and r["premier_controle_bloquant"] == "annees_d_examen", dit(r))
    # V7 — INCOMPLETE : NON JUGEABLE, motif « hypothese »
    avant = nb_essais()
    r = juger("INCOMPLETE")
    ok("V7 déclaration sans hypothèse : NON JUGEABLE (hypothese), aucun regard", r["verdict"] == NJ
       and r["motif"] == "hypothese"
       and nb_essais() == avant, dit(r))
    raison_decl = str((r.get("controles", {}).get("declaration") or {}).get("raison"))
    ok("V7b la liste des champs en défaut est CELLE DE LA LECTURE (hypothese ET parametres_libres « deux »), "
       "jamais refabriquée par la porte", "hypothese" in raison_decl and "parametres_libres" in raison_decl, raison_decl)
    # V8 — NON-ENGAGEE : écrite sur le disque, absente de la branche. Depuis la mission REGARD, la porte exige un arbre
    # PROPRE : l'arbre sali rend tout INCONNU avant même de lire la déclaration (l'ancienne attente, NON JUGEABLE
    # « date_declaration », ne se voit plus par ce chemin : le disque n'est plus jugé).
    chemin_d = os.path.join(dossier, C.DECLARATIONS_DATEES)
    texte_d = open(chemin_d, encoding="utf-8").read()
    with open(chemin_d, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=C.DECLARATION_DATEE).writerow(
            json.load(open(os.path.join(dossier, ".ligne_non_engagee.json"), encoding="utf-8")))
    avant = nb_essais()
    r = juger("NON-ENGAGEE")
    open(chemin_d, "w", encoding="utf-8").write(texte_d)
    ok("V8 déclaration non commitée (arbre sali) : NON TRANCHÉE (MESURE MANQUANTE declaration), raison « branche », "
       "aucun regard", r["verdict"] == NT and r["motif"] == "MESURE MANQUANTE declaration" and nb_essais() == avant
       and "arbre de travail non propre" in str(((r.get("lu") or {}).get("raisons") or {}).get("branche")), dit(r))
    # V11 — chaque jugement joué a laissé un préenregistrement ET son résultat (A-226)
    entrees, defauts = T.lire_le_registre(dossier)
    natures = sorted(e["nature"] for e in entrees.values())
    ok("V11 registre des essais : 8 préenregistrements, 8 résultats, aucun défaut",
       not defauts and natures.count("PREENREGISTREMENT") == 8 and natures.count("RESULTAT") == 8,
       "%s · %s" % (natures, defauts[:2]))
    # V15 — cas (b) du superviseur de B2/B3 : le disque ne contient plus la branche principale → INCONNU, rien de joué
    sha = subprocess.run(["git", "-C", dossier, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "poussé ailleurs"],
                         capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "-C", dossier, "update-ref", "refs/remotes/origin/main", sha], check=True)
    avant = nb_essais()
    r = juger("BONNE-B")
    ok("V15 disque sans la branche principale : NON TRANCHÉE (MESURE MANQUANTE declaration), aucun regard",
       r["verdict"] == NT and r["motif"] == "MESURE MANQUANTE declaration" and nb_essais() == avant
       and "branche" in ((r.get("lu") or {}).get("raisons") or {}), dit(r))
    return res


def relancer(source, sab):
    """Fabrique un dépôt, y applique un sabotage, relance « --cas » et rend les cas.
    ① RÔLE — un processus et un dépôt par passage. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — source, sabotage ou
    « Z0 ». ④ CONDITIONS D'ENTRÉE — chaque texte visé présent une fois. ⑤ SORTIE — UNE valeur : liste de cas. [rend: 1]
    ⑥ TRAITEMENT — fabriquer, saboter, relancer (600 s), effacer. ⑦ UNITÉ — —. ⑧ POURQUOI — les modules ont les mêmes
    noms. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — dossiers /tmp/J_porte_*. ⑪ TERMINAISON — Rend la main ; lève LookupError.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="J_porte_%s_" % sab)
    try:
        fabriquer(source, d)
        if sab != "Z0":
            f, a, b, _v = SABOTAGES[sab]
            p = os.path.join(d, f)
            t = open(p, encoding="utf-8").read()
            if t.count(a) != 1:
                raise LookupError("sabotage %s : texte visé présent %d fois" % (sab, t.count(a)))
            open(p, "w", encoding="utf-8").write(t.replace(a, b))
            # LE SABOTAGE EST COMMITÉ ET POUSSÉ (mission REGARD) : la porte exige HEAD = la branche principale et un arbre
            # propre ; laissé sur le disque, il rendrait tout INCONNU et « mordrait » pour une autre raison.
            for args in (["add", "-A"], ["commit", "-q", "-m", "sabotage " + sab], ["push", "-q", "origin", "main"],
                         ["fetch", "-q", "origin"]):
                subprocess.run(["git", "-C", d] + args, check=True, capture_output=True)
        try:
            r = subprocess.run([sys.executable, "-B", ICI, "--cas", d], capture_output=True, text=True, timeout=600,
                               cwd=d)
        except subprocess.TimeoutExpired:
            return [("relance", False, "plus de 600 s")]
        try:
            return [tuple(x) for x in json.loads(r.stdout.strip().splitlines()[-1])]
        except (ValueError, IndexError):
            return [("relance", False, (r.stderr or r.stdout)[-600:])]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    """Joue Z0, puis chaque sabotage avec « --saboter ».
    ① RÔLE — Le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — « --cas » : jouer les cas
    et écrire leur JSON ; sinon Z0, puis les sabotages ; un sabotage MORD si le cas qu'il vise rougit. ⑦ UNITÉ — —.
    « --sabotage=NOM » (répétable) ne joue que ces sabotages : la série complète dure plus de 5 minutes.
    ⑧ POURQUOI — R-731, R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if argv[:1] == ["--cas"]:
        print(json.dumps(cas(argv[1]), ensure_ascii=False))
        return 0
    if not argv:
        print(__doc__)
        return 2
    source = os.path.abspath(argv[0])
    z0 = relancer(source, "Z0")
    rouges = [c for c in z0 if not c[1]]
    for nom, vert, detail in z0:
        print("  %s  %s%s" % ("VERT " if vert else "ROUGE", nom, "" if vert else "\n         " + str(detail)[:900]))
    print("== Z0 : %d cas, %d rouge(s)" % (len(z0), len(rouges)))
    code = 1 if rouges else 0
    choisis = [a.split("=", 1)[1] for a in argv if a.startswith("--sabotage=")]
    if "--saboter" in argv or choisis:
        for sab in (choisis or SABOTAGES):
            vise = SABOTAGES[sab][3]
            r = relancer(source, sab)
            mord = any(n.startswith(vise + " ") and not v for n, v, _d in r)
            print("  %s %s — %s" % ("MORD  " if mord else "SURVIT", sab, next((n for n, _v, _d in r if
                                                                              n.startswith(vise + " ")), r[0][0])))
            code = code or (0 if mord else 1)
    print("VERDICT : %s" % ("conforme" if code == 0 else "NON CONFORME"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
