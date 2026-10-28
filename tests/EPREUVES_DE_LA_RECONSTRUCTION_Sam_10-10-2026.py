#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_RECONSTRUCTION — Sam 10-10-2026 (Paris)
Rôle : prouver que programmes/RECONSTRUIRE_L_HISTORIQUE_LONG.py dit juste, ligne par ligne, d'où vient chaque cours
de l'historique long, et que etudes/outils/RELEVER_LES_DIVISIONS_BNAINS.py relève juste la table des divisions de
bnains ; et que chaque épreuve a des dents (R-731).
Quand l'appeler : avant toute livraison qui touche l'un de ces deux programmes.

À QUOI ÇA SERT. Demande de Jean-Luc du 09-10-2026 à 20h55 : « on doit pouvoir comprendre chaque valeur de l'historique
et pouvoir absolument tout retrouver et reconstituer ». La reconstruction est l'instrument qui le dit ; un instrument
faux dirait « reconstruite » d'une ligne fausse. Les épreuves R1 à R5 jouent des cas FABRIQUÉS, chacun pris d'un cas
réel ; R6 joue les VRAIS fichiers du dépôt, copiés ; R7 et R8 jouent les VRAIES pages de bnains gardées au dépôt
(temoins/PAGES_BNAINS_DES_ACTIONS/), sans réseau.

LES ÉPREUVES :
R1  operations : une division de Yahoo vaut dénominateur ÷ numérateur ; une opération déclarée 1 ÷ (1 + marche) ;
    à prix nul elle se nomme « actions gratuites » ; un verdict « aucune déclaration » sans facteur à défaire donne un
    facteur inconnu (Carrefour 2000, dont le verdict dit « légitime » et non « ajustée par Yahoo ») ; un verdict OMISE,
    ou avec facteur à défaire, n'en donne pas, ni un verdict sur un jour déjà connu (Société Générale 2000) ; deux
    valeurs rendues ; une opération sans avis de bnains est « absente ».
R2  confronter : une division de bnains seule est AJOUTÉE (Société Générale 2000) ; même jour même facteur ; à moins
    de 40 jours ET au même facteur, « date différente » (Hermès 2006) ; facteur différent → complément (1 ÷ diviseur)
    ÷ retenu (Air Liquide 2012 : la parité « pour 10 » donne 1,1 exact contre 1,10254 ; Accor 2010 : 1,5328 sans
    parité contre 1,53886) ; la parité écrite remplace l'arrondi (Sagem 2003, 1,17 → 7 ÷ 6) ; le produit du jour
    compte la division ET les actions gratuites (Sagem 2000) ; un jour division + distribution ne compare que la
    division (Total 2006) ; une division d'avant 2000 est ignorée ; deux lignes de bnains du même jour se multiplient
    (D1) ; une action gratuite omise trente jours après une division s'ajoute à son jour sans défaire la division
    (D9) ; une division mal datée près d'un droit se rapproche de la division, pas du droit (D2) — trois cas de la
    relecture indépendante du 10-10-2026 ; diviseur_exact lit « pour 6 » et « pour quatre », refuse une parité en
    désaccord avec le diviseur écrit.
R3  deduire : un ajustement caché de facteur 0,9 (Eiffage 2001) se mesure 0,9 par les MÉDIANES, malgré une ligne
    aberrante de chaque côté.
R4  reconstruire : ligne exacte → reconstruite ; facteur appliqué à 0,5 % du documenté (Michelin 2010) → les lignes
    d'avant « reconstruite au facteur appliqué », écart du facteur mesuré ; une ligne seule à +3 % → ligne isolée ;
    Google à moins de 0,2 % → confirmée, à 10 % → écart à Google (Air Liquide 08-06-2026) ; ni brut ni Google → sans
    cours brut ; une opération au facteur inconnu → facteur inconnu ; le jour même de l'opération, la ligne est déjà
    ex-opération.
R5  expliquer : le texte nomme chaque opération postérieure, son facteur et sa source, le produit et l'écart ; une
    ligne absente le dit.
R6  main sur une COPIE des vrais fichiers : code 0, le résumé exact mesuré le 10-10-2026, et les deux tables
    identiques à l'octet à celles du dépôt ; --ligne SOCIETE GENERALE 2000-05-10 explique la division par 4 relevée
    chez bnains et un écart sous 0,2 % ; sans l'extrait bnains → 2 ; sans racine → 2.
R7  extraire, sur les vraies pages gardées : Pernod Ricard, 5 divisions, la ligne du 14-02-2003 exacte ; Eiffage,
    table vide ; ArcelorMittal, « Aucune division référencée » → vide ; Danone, la date « 30/11/-0001 » gardée
    « illisible chez bnains » ; une page sans la table → None ; une ligne de 4 cellules → ValueError.
R8  main du relevé, réseau remplacé par les pages gardées : code 0 et la table du dépôt refaite à l'octet ; une page
    qui ne se lit pas → code 2.

LES SABOTAGES (avec --saboter) — S1 MEME_FACTEUR à 1 · S2 parité écrite prise même en désaccord avec le diviseur · S3 le produit du jour prend toutes
les opérations · S4 complément jamais ajouté · S5 rapprochement à 0 jour · S6 les divisions d'avant 2000 gardées ·
S7 tout verdict sans facteur pris pour un ajustement caché · S8 le facteur appliqué ignoré · S9 facteur_apres compte le
jour même · S10 deduire par la moyenne · S11 actions gratuites non nommées · S12 table vide de bnains illisible ·
S13 date illisible de bnains refusée · S14 un échec de page ne compte pas · S15 la tolérance de l'écart d'opération
ignorée · S16 un ajustement caché ajouté même quand l'opération est déjà connue · S17 « trois » lu 2 · S18 deux lignes
de bnains du même jour non multipliées · S19 une date différente acceptée sans le même facteur.

USAGE : python3 tests/EPREUVES_DE_LA_RECONSTRUCTION_Sam_10-10-2026.py <racine du dépôt> [--saboter | --saboter=S1,S2…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import contextlib, csv, hashlib, importlib.util, io, json, os, shutil, sys, tempfile, urllib.request

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROGRAMMES = os.path.join(RACINE, "programmes")
RECONSTRUCTION = os.path.join(PROGRAMMES, "RECONSTRUIRE_L_HISTORIQUE_LONG.py")
RELEVE = os.path.join(RACINE, "etudes", "outils", "RELEVER_LES_DIVISIONS_BNAINS.py")
PAGES = os.path.join(RACINE, "temoins", "PAGES_BNAINS_DES_ACTIONS")
# Le résumé sur les vrais fichiers (mesuré par le programme, recopié ici comme valeur attendue).
# MIS À JOUR LE 15-10-2026. Celui du 10-10-2026 finissait par « reconstruite : 144874 · … · écart à Google : 1 ». Le seul
# écart était Air Liquide le 08-06-2026 : la reconstruction donnait 165,38, la barre Google du fichier maître 150,35. Cette
# barre Google était fausse : elle a été corrigée au fichier maître le 08-10-2026 sur la barre officielle d'Euronext, 165,38
# (commit 519cedd, R-107 et A-549), arrivée sur la version en attente par la fusion de la version officielle. La ligne n'a
# plus de barre Google à confronter : elle compte désormais parmi les reconstruites (144 875) et l'écart disparaît. Mesuré
# le 15-10-2026 : remettre le fichier maître du 10-10 (1133f6e) redonne exactement l'ancien résumé ; remettre le
# programme de contrôle ou les détachements officiels du 10-10 ne le change pas. R6 rougissait depuis la fusion
# (trouvé le 15-10-2026 avant le versement ; réparé sur décision de Jean-Luc, « 2 », 08h57) ; les deux tables de la
# reconstruction ont été refaites par le programme, sur une copie du dépôt, et seule la ligne d'Air Liquide y change.
# MIS À JOUR LE 24-10-2026. Le versement du 02-10 sur la version en attente (commit 30bc173, 23-10-2026) a ajouté une
# barre ESSILORLUXOTTICA du 02-10-2026 au fichier réparé : une ligne et une reconstruite de plus ; R6 rougissait depuis.
# Mesuré le 24-10-2026 : la table des écarts est identique, celle des opérations ne change que d'une cellule
# (ESSILORLUXOTTICA 2007-07-16, lignes après l'opération : 2486 → 2487) ; refaite par le programme sur une copie
# du dépôt (superviseur R-759 du même jour : de fond).
RESUME = ("lignes : 244994 · confirmée par Google : 25955 · ligne isolée : 781 · reconstruite : 144876 · "
          "reconstruite au facteur appliqué : 5761 · sans cours brut : 67621")

SABOTAGES = {
    "S1": (RECONSTRUCTION, "MEME_FACTEUR = 1e-3 ", "MEME_FACTEUR = 1.0 "),
    "S2": (RECONSTRUCTION, "        if abs((n + 1) / n - ecrit) <= ARRONDI_BNAINS:", "        if True:"),
    "S3": (RECONSTRUCTION, "                if nature.startswith(CHAMP_DE_BNAINS):\n",
           "                if True:\n"),
    "S4": (RECONSTRUCTION, "                ops[v].append((d, f / g, f\"complément", "                [].append((d, f / g, f\"complément"),
    "S5": (RECONSTRUCTION, "RAPPROCHEMENT = 40 ", "RAPPROCHEMENT = 0 "),
    "S16": (RECONSTRUCTION, "                and (r[\"valeur\"], r[\"date\"]) not in deja):", "                ):"),
    "S17": (RECONSTRUCTION, "\"trois\": 3,", "\"trois\": 2,"),
    "S18": (RECONSTRUCTION, "            x[0] *= diviseur_exact(r)", "            x[0] = diviseur_exact(r)"),
    "S19": (RECONSTRUCTION, "        voisins = sorted((abs((datetime.date.fromisoformat(x) - jd).days), x) for x, g in champ.items()\n                         if abs(f / g - 1) <= MEME_FACTEUR)",
            "        voisins = sorted((abs((datetime.date.fromisoformat(x) - jd).days), x) for x, g in champ.items())"),
    "S6": (RECONSTRUCTION, "        if r[\"date\"] >= DEBUT:", "        if True:"),
    "S7": (RECONSTRUCTION, "        if (r[\"ce_que_yahoo_declare\"].startswith(\"aucune déclaration\") and not r[\"facteur_a_defaire\"]",
           "        if (True and not r[\"facteur_a_defaire\"]"),
    "S8": (RECONSTRUCTION, "                    q *= g\n", "                    q *= 1\n"),
    "S9": (RECONSTRUCTION, "    for x, f, *_ in ops:\n        if x > d:", "    for x, f, *_ in ops:\n        if x >= d:"),
    "S10": (RECONSTRUCTION, "                liste[i] = (d, statistics.median(avant) / statistics.median(apres),",
            "                liste[i] = (d, statistics.mean(avant) / statistics.mean(apres),"),
    "S11": (RECONSTRUCTION, "genre = \"actions gratuites\" if", "genre = \"document\" if"),
    "S12": (RELEVE, "        if cellules == [AUCUNE]:\n            continue\n", ""),
    "S13": (RELEVE, "            veille = \"illisible chez bnains : \" + cellules[2]", "            raise"),
    "S14": (RELEVE, "            echecs.append(f\"{valeur} : {type(e).__name__} : {e}\")\n", ""),
    "S15": (RECONSTRUCTION, "if a is not None and z is not None and abs((1 + a) / (1 + z) - 1) > TOLERANCE:",
            "if a is not None and z is not None:"),
}


def charger(sabotage=None):
    """Charge la reconstruction et le relevé — les vrais fichiers, ou des copies dont l'un est saboté."""
    dossier = tempfile.mkdtemp()
    for f in ("CONTRATS_DES_FICHIERS.py", "CONTROLER_L_HISTORIQUE_LONG.py", "RECONSTRUIRE_L_HISTORIQUE_LONG.py",
              "COMMUN.py"):
        shutil.copy(os.path.join(PROGRAMMES, f), dossier)
    shutil.copy(RELEVE, dossier)
    if sabotage:
        chemin, cible, remplace = sabotage
        copie = os.path.join(dossier, os.path.basename(chemin))
        open(copie, "w", encoding="utf-8").write(open(chemin, encoding="utf-8").read().replace(cible, remplace))
    for nom in ("CONTRATS_DES_FICHIERS", "CONTROLER_L_HISTORIQUE_LONG", "RECONSTRUIRE_L_HISTORIQUE_LONG", "COMMUN",
                "RELEVER_LES_DIVISIONS_BNAINS"):
        sys.modules.pop(nom, None)
    sys.path.insert(0, dossier)
    try:
        modules = []
        for nom in ("RECONSTRUIRE_L_HISTORIQUE_LONG", "RELEVER_LES_DIVISIONS_BNAINS"):
            sp = importlib.util.spec_from_file_location(nom, os.path.join(dossier, nom + ".py"))
            m = importlib.util.module_from_spec(sp)
            sys.modules[nom] = m
            sp.loader.exec_module(m)
            modules.append(m)
    finally:
        sys.path.remove(dossier)
    return modules


def lancer(f, *argv):
    sortie = io.StringIO()
    ici = os.getcwd()
    try:
        with contextlib.redirect_stdout(sortie):
            code = f(*argv)
    finally:
        os.chdir(ici)
    return code, sortie.getvalue()


def verdicts(lignes):
    """Un faux fichier de verdicts de Yahoo, à l'en-tête vrai."""
    o = os.path.join(tempfile.mkdtemp(), "v.csv")
    with open(o, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(sys.modules["CONTRATS_DES_FICHIERS"].AJUSTEMENTS_DE_YAHOO)   # l'en-tête lu au contrat, jamais recopié (R-708)
        w.writerows(lignes)
    return o


def barres(d):
    """Une série {date: (o, h, b, c, vol)} depuis {date: clôture}."""
    return {x: (c, c, c, c, 1000) for x, c in d.items()}


def epreuves(R, B):
    res = {}
    K = R.K
    # R1
    try:
        garde = K.VERDICTS_YAHOO
        K.VERDICTS_YAHOO = verdicts([
            ["CARREFOUR", "2000-04-11", "aucune déclaration (ajustement caché de la colonne close)",
             "DIVISION RÉELLE (une action gratuite pour une), non déclarée par Yahoo — légitime", "", "", ""],
            ["KERING", "2013-06-20", "un dividende ce jour-là, l'opération non déclarée", "OMISE par Yahoo", "", "", ""],
            ["ESSILORLUXOTTICA", "2024-05-06", "aucune déclaration (ajustement caché)", "défait", "", "", "184.07/180.12"],
            ["SG", "2000-05-11", "aucune déclaration (ajustement caché de la colonne close)", "légitime", "", "", ""]])
        try:
            sortie = R.operations({"SG": {"divisions": [["2000-05-11", 4.0, 1.0]]}}, [],
                                  {"PR": {"2007-01-16": ("document", 171.8, 0, 5)},
                                   "VI": {"2006-03-30": ("document", 81.15, 70.25, 5.5)}}, {}, [])
        finally:
            K.VERDICTS_YAHOO = garde
        ops, avis = sortie
        res["R1"] = len(sortie) == 2 and ops["SG"] == [("2000-05-11", 0.25, "division déclarée par Yahoo, 4 pour 1",
                                                        "donnees/sources_yahoo/evenements.json")] \
            and abs(ops["PR"][0][1] - 5 / 6) < 1e-12 and ops["PR"][0][2].startswith("actions gratuites") \
            and ops["VI"][0][2].startswith("document") and abs(ops["VI"][0][1] - 1 / 1.0211009) < 1e-6 \
            and ops["CARREFOUR"] == [("2000-04-11", None, "ajustement caché de Yahoo, facteur non documenté",
                                      "donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv")] \
            and "KERING" not in ops and "ESSILORLUXOTTICA" not in ops \
            and avis[("SG", "2000-05-11")] == "absente de la table de bnains"
    except Exception as e:
        res["R1"] = False
    # R2
    try:
        def div(v, d, x, c="essai"):
            return {"valeur": v, "date": d, "diviseur": x, "commentaire": c}
        y = lambda d, n: (d, 1 / n, f"division déclarée par Yahoo, {n:g} pour 1", "y")
        ops = {"SG": [],
               "PR": [y("2008-01-15", 2)],
               "HE": [y("2006-06-12", 3)],
               "AL": [y("2012-05-31", 1.10254)],
               "SA": [y("2000-07-10", 3), ("2000-07-10", 1 / 1.2, "actions gratuites (marche permise +20 %)", "d"),
                      ("2003-12-19", 6 / 7, "actions gratuites (marche permise +16,67 %)", "d")],
               "AC": [("2010-07-02", 0.649832, "distribution (marche permise +53,886 %)", "d")],
               "TO": [y("2006-05-18", 4), ("2006-05-18", 0.987143, "distribution (marche permise +1,3 %)", "d")],
               "VI": [("2006-03-30", 0.979336, "document (marche permise +2,1 %)", "d")],
               "D1": [y("2000-07-10", 3.6)],
               "D9": [y("2010-06-01", 2)],
               "D2": [y("2011-09-02", 2), ("2011-08-05", 0.98, "document (marche permise +2 %)", "d")]}
        avis = R.confronter(ops, [div("SG", "2000-05-11", "4"), div("PR", "2008-01-15", "2"),
                                  div("HE", "2006-06-10", "3"),
                                  div("AL", "2012-05-31", "1.1", "1 action gratuite pour 10 le 31/05/2012"),
                                  div("SA", "2000-07-10", "3.6",
                                      "Distribution d'une action gratuite pour 5, puis division du nominal par 3"),
                                  div("SA", "2003-12-19", "1.17", "Attribution gratuite d'une action pour 6"),
                                  div("AC", "2010-07-02", "1.5328"), div("TO", "2006-05-18", "4"),
                                  div("PR", "1994-07-01", "1.2"),
                                  div("D1", "2000-07-10", "1.2", "une action gratuite pour cinq"),
                                  div("D1", "2000-07-10", "3"),
                                  div("D9", "2010-06-30", "1.1", "1 action gratuite pour 10"),
                                  div("D2", "2011-08-01", "2")])
        comp = lambda v: [x for x in ops[v] if x[2].startswith("complément")]
        res["R2"] = ops["SG"] == [("2000-05-11", 0.25, "division relevée chez bnains, ÷4 « essai »", R.DIVISIONS)] \
            and avis[("SG", "2000-05-11")].endswith("seule source") \
            and avis[("PR", "2008-01-15")].endswith("même date, même facteur") \
            and "date différente (2006-06-10), même facteur" in avis[("HE", "2006-06-12")] \
            and len(comp("AL")) == 1 and abs(comp("AL")[0][1] - 1.10254 / 1.1) < 1e-12 \
            and avis[("SA", "2000-07-10")].endswith("même date, même facteur") \
            and avis[("SA", "2003-12-19")].endswith("même date, même facteur") and len(ops["SA"]) == 3 \
            and len(comp("AC")) == 1 and "FACTEUR DIFFÉRENT" in avis[("AC", "2010-07-02")] \
            and avis[("TO", "2006-05-18")].endswith("même date, même facteur") and len(ops["TO"]) == 2 \
            and not any(x[0] == "1994-07-01" for x in ops["PR"]) \
            and ("VI", "2006-03-30") not in avis \
            and len(ops["D1"]) == 1 and avis[("D1", "2000-07-10")].endswith("même date, même facteur") \
            and ops["D9"][0] == y("2010-06-01", 2) and len(ops["D9"]) == 2 and ops["D9"][1][0] == "2010-06-30" \
            and abs(ops["D9"][1][1] - 1 / 1.1) < 1e-12 and avis[("D9", "2010-06-30")].endswith("seule source") \
            and len(ops["D2"]) == 2 and "date différente (2011-08-01), même facteur" in avis[("D2", "2011-09-02")] \
            and abs(R.diviseur_exact(div("X", "d", "1.17", "Attribution gratuite d'une action pour 6")) - 7 / 6) < 1e-12 \
            and R.diviseur_exact(div("X", "d", "1.5328", "une action gratuite Edenred")) == 1.5328 \
            and abs(R.diviseur_exact(div("X", "d", "1.25", "Attribution d'une action gratuite pour quatre.")) - 1.25) < 1e-12 \
            and R.diviseur_exact(div("X", "d", "1.3", "une action gratuite pour 4")) == 1.3 \
            and abs(R.diviseur_exact(div("X", "d", "1.33", "Attribution d'une action gratuite pour trois.")) - 4 / 3) < 1e-12
    except Exception:
        res["R2"] = False
    # R3
    try:
        jours = [f"2001-{m:02d}-{j:02d}" for m in (5, 6, 7, 8) for j in (2, 9, 16, 23)]
        brut = {"EI": {d: (100.0, "bnains") for d in jours}}
        fichier = {"EI": barres({d: (15.0 if d < "2001-07-02" else 16.6666667) for d in jours})}
        fichier["EI"]["2001-05-02"] = barres({"x": 30.0})["x"]            # une ligne aberrante avant
        fichier["EI"]["2001-08-23"] = barres({"x": 1.0})["x"]             # et une après
        ops = R.deduire(fichier, brut, {"EI": [("2001-07-02", None, "ajustement caché", "v")]})
        res["R3"] = abs(ops["EI"][0][1] - 0.9) < 1e-6 and "MESURÉ" in ops["EI"][0][2]
    except Exception:
        res["R3"] = False
    # R4
    try:
        jours = [f"2010-{m:02d}-{j:02d}" for m in (8, 9, 10, 11) for j in (2, 9, 16, 23)] + ["2010-09-30"]
        jours = sorted(set(jours))
        brut = {"MI": {d: (50.0, "bnains") for d in jours}}
        f_doc = 0.970760
        fichier = {"MI": barres({d: (50.0 * f_doc * 0.995 if d < "2010-09-30" else 50.0) for d in jours})}
        fichier["MI"]["2010-11-09"] = barres({"x": 51.5})["x"]
        brut["GO"] = {}
        fichier["GO"] = barres({"2026-06-05": 165.0, "2026-06-08": 165.38, "2026-06-09": 120.0})
        google = {"GO": {"2026-06-05": 165.1, "2026-06-08": 150.35}}
        brut["IN"] = {"2018-01-02": (10.0, "bnains"), "2018-06-01": (10.0, "bnains")}
        fichier["IN"] = barres({"2018-01-02": 9.0, "2018-06-01": 10.0})
        ops = {"MI": [("2010-09-30", f_doc, "bnains (marche permise +3,0 %)", "d")],
               "IN": [("2018-05-14", None, "ajustement caché", "v")]}
        lignes, par_op = R.reconstruire(fichier, brut, ops, google, {("MI", "2010-09-30"): "absente"})
        st = {(v, d): x for v, d, *_, x in lignes}
        avant = [st[("MI", d)] for d in jours if d < "2010-09-30"]
        mi = [x for x in par_op if x[0] == "MI"][0]
        res["R4"] = set(avant) == {"reconstruite au facteur appliqué"} and st[("MI", "2010-09-30")] == "reconstruite" \
            and st[("MI", "2010-11-09")] == "ligne isolée" and st[("MI", "2010-10-02")] == "reconstruite" \
            and abs(mi[9] - (-0.005)) < 1e-9 and mi[10] == "absente" and mi[7] == 8 and mi[8] == 9 \
            and st[("GO", "2026-06-05")] == "confirmée par Google" and st[("GO", "2026-06-08")] == "écart à Google" \
            and st[("GO", "2026-06-09")] == "sans cours brut" \
            and st[("IN", "2018-01-02")] == "facteur inconnu" and st[("IN", "2018-06-01")] == "reconstruite"
    except Exception:
        res["R4"] = False
    # R5
    try:
        t = R.expliquer("SG", "2000-05-10", {"SG": barres({"2000-05-10": 60.2})}, {"SG": {"2000-05-10": (240.8, "bnains")}},
                        {"SG": [("2000-05-11", 0.25, "division relevée chez bnains, ÷4", "D.csv"),
                                ("2006-10-02", 0.99336, "document", "O.csv")]})
        t2 = R.expliquer("SG", "1999-01-04", {"SG": {}}, {}, {})
        res["R5"] = "× 0.250000 — 2000-05-11, division relevée chez bnains, ÷4 (D.csv)" in t \
            and "× 0.993360 — 2006-10-02, document (O.csv)" in t and "facteur total : 0.248340" in t \
            and "écart du fichier : +0.6684 %" in t and "aucune ligne" in t2
    except Exception:
        res["R5"] = False
    # R6
    try:
        r = tempfile.mkdtemp()
        K = R.K
        for chemin in (K.FICHIER, K.BNAINS, K.FAUSSES, R.MAITRE, K.VERDICTS_YAHOO, K.EVENEMENTS, K.DROITS, K.OFFICIELS,
                       R.DIVISIONS):
            os.makedirs(os.path.dirname(os.path.join(r, chemin)), exist_ok=True)
            shutil.copy(os.path.join(RACINE, chemin), os.path.join(r, chemin))
        code, out = lancer(R.main, [r])
        emp = lambda c: hashlib.sha256(open(c, "rb").read()).hexdigest()
        memes = all(emp(os.path.join(r, c)) == emp(os.path.join(RACINE, c)) for c in (R.PAR_OPERATION, R.ECARTS))
        code_l, out_l = lancer(R.main, [r, "--ligne", "SOCIETE GENERALE", "2000-05-10"])
        ecart = float(out_l.split("écart du fichier : ")[1].split(" %")[0])
        os.remove(os.path.join(r, K.BNAINS))
        code_b, _ = lancer(R.main, [r])
        code_v, _ = lancer(R.main, [])
        res["R6"] = code == 0 and RESUME in out and memes and code_l == 0 \
            and "2000-05-11, division relevée chez bnains, ÷4" in out_l and abs(ecart) < 0.2 \
            and code_b == 2 and code_v == 2
    except Exception:
        res["R6"] = False
    # R7
    try:
        page = lambda isin: open(os.path.join(PAGES, isin + ".html"), encoding="utf-8").read()
        pr = B.extraire(page("FR0000120693"))
        dan = B.extraire(page("FR0000120644"))
        mauvaise = page("FR0000120693").replace("<tr style=\"background-color: #F0F0FF;\"><td class=\"text-center\">14/02/2003</td>",
                                                "<tr><td>14/02/2003</td>", 1)
        mauvaise = mauvaise.replace("<td>14/02/2003</td><td class=\"text-center\">1.25000</td>", "<td>14/02/2003</td>", 1)
        try:
            B.extraire(mauvaise)
            leve = False
        except ValueError:
            leve = True
        res["R7"] = len(pr) == 5 and ("2003-02-14", 1.25, "2003-02-13", 80.8, "EUR",
                                      "Attribution d'une action gratuite pour quatre.") in pr \
            and B.extraire(page("FR0000130452")) == [] and B.extraire(page("LU1598757687")) == [] \
            and ("2004-06-15", 2.0, "illisible chez bnains : 30/11/-0001", 142.3, "EUR", "Division du nominal par 2") in dan \
            and B.extraire("<html>rien</html>") is None and leve
    except Exception:
        res["R7"] = False
    # R8
    try:
        r = tempfile.mkdtemp()
        os.makedirs(os.path.join(r, "donnees", "sources_bnains"))
        for f in os.listdir(os.path.join(RACINE, "donnees")):
            if f.startswith("REFERENTIEL_VALEURS"):
                shutil.copy(os.path.join(RACINE, "donnees", f), os.path.join(r, "donnees", f))
        vraie = urllib.request.urlopen

        class Reponse:
            def __init__(self, octets):
                self.octets = octets

            def read(self):
                return self.octets

        def fausse(req, timeout=None):
            isin = req.full_url.split("codeISIN=")[1]
            return Reponse(open(os.path.join(PAGES, isin + ".html"), "rb").read())

        def cassee(req, timeout=None):
            if "FR0000120693" in req.full_url:
                raise OSError("coupure")
            return fausse(req, timeout)
        dormir = B.time.sleep
        B.time.sleep = lambda s: None
        try:
            urllib.request.urlopen = fausse
            code, out = lancer(B.main, [r])
            pareil = open(os.path.join(r, B.TABLE), "rb").read() == open(os.path.join(RACINE, B.TABLE), "rb").read()
            urllib.request.urlopen = cassee
            code2, out2 = lancer(B.main, [r])
        finally:
            urllib.request.urlopen = vraie
            B.time.sleep = dormir
        res["R8"] = code == 0 and pareil and code2 == 2 and "ÉCHEC PERNOD RICARD" in out2
    except Exception:
        res["R8"] = False
    return res


def main():
    R, B = charger()
    res = epreuves(R, B)
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programmes tels quels : {len(res) - len(rouges)}/{len(res)} épreuves vertes" + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        for k, (chemin, cible, remplace) in SABOTAGES.items():
            if choix and k not in choix[0]:
                continue
            source = open(chemin, encoding="utf-8").read()
            if source.count(cible) != 1:
                print(f"{k} NE S'APPLIQUE PLUS : texte cible trouvé {source.count(cible)} fois")
                return 2
            r = epreuves(*charger((chemin, cible, remplace)))
            tombees = [e for e, v in r.items() if not v]
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}")
            if not tombees:
                code = 1
    return code


if __name__ == "__main__":
    _DOSSIER_D_ESSAI = tempfile.mkdtemp(prefix="epreuves_")
    tempfile.tempdir = os.environ["TMPDIR"] = _DOSSIER_D_ESSAI
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(_DOSSIER_D_ESSAI, ignore_errors=True)
