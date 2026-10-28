#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_PREUVES_DU_REFERENTIEL — Sam 24-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py rend 0 sur le référentiel du dépôt, rend 1 avec
  le bon motif sur chaque défaut plausible (ligne décalée, nom en double, clé à espace, citation raccourcie ou
  recousue, nom Yahoo pris ailleurs, fichier en trop, adresse fausse, preuve retirée, avis échangé, colonnes
  absentes…), rend 2 avec le bon motif quand il ne peut pas tourner ; et, avec --saboter, que chacune de ses gardes,
  retirée, fait tomber au moins un cas.
② CONTEXTE D'APPEL — Par la certification (programmes/CERTIFIER_LA_VERSION.py), chaque nuit, depuis la racine, la racine
  en argument, puis une seconde fois avec --saboter. À la main :
  python3 tests/EPREUVES_DES_PREUVES_DU_REFERENTIEL_Sam_24-10-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt (lue, jamais écrite) ; l'option --saboter.
④ CONDITIONS D'ENTRÉE — pdftotext installé (sinon code 2, sans jouer aucun cas).
⑤ SORTIE — Le code : 0 si chaque cas rend le code et le motif attendus (et, avec --saboter, si chaque garde retirée
  fait tomber au moins un cas) ; 1 si un cas est faux ou si une garde ne mord pas ; 2 si l'épreuve n'a pas pu juger
  (pdftotext absent, un cas ou une garde ne s'applique plus, erreur imprévue). Une ligne « OK »/« FAUX » par cas,
  « BILAN », puis avec --saboter une ligne « <garde> mord … » / « NE MORD PAS » / « NE S'APPLIQUE PLUS » par garde,
  et « VERDICT ».
  [rend: 1]
⑥ TRAITEMENT — Un banc dans un dossier temporaire : une copie du vérificateur (à l'octet, pour que la mesure de
  couverture le crédite), du référentiel, du carnet et de chaque fichier que le référentiel cite, plus l'archive
  2016.ZIP pour le cas d'une archive imbriquée. Chaque cas : une copie du banc en liens durs, un fichier remplacé
  (jamais écrit à travers un lien), le vérificateur lancé par sous-processus, son code ET un fragment de son écran
  comparés à l'attendu. Avec --saboter, chaque garde du vérificateur est retirée une à une, et les cas sont rejoués
  jusqu'au premier qui tombe.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve. R-755 ② : les
  épreuves d'un programme de programmes/ vivent dans tests/ (relecteur du 24-10-2026, tour 2). Le fragment de motif
  distingue une détection d'un plantage, qui rendait le même code (même relecteur, C-e). Les cas des pannes servent à ce
  que chaque instruction du vérificateur soit exécutée : la certification exige qu'un programme absent de la
  référence ait tout examiné (superviseur R-759 du 24-10-2026, tour 2). Mesuré le 24-10-2026 par coverage --branch sur
  les cas non sabotés : 182 instructions sur 182, 79 embranchements sur 80 (manque la sortie du « if __name__ ») ;
  après les corrections du tour 4 (même jour, 20h27) : 188 instructions sur 188, 81 embranchements sur 82.
⑨ CE QUI CLOCHE — Les cas sont écrits pour les valeurs actuelles (AC, AI, BVI, DSY, ML, ERF) et pour les lignes de leurs
  preuves ; les chemins des réponses de Yahoo sont tirés des fichiers que le référentiel cite. Si l'un change, son cas
  « ne s'applique plus » et l'épreuve rend 2 ; une préparation qui ne change rien le dit aussi (relecteur du
  24-10-2026, tour 3, N2 : un dossier de Yahoo daté autrement faisait rendre 1 sur un dépôt sain). · Une garde qui
  « mord » peut mordre par le message ou par un plantage du vérificateur saboté, sans qu'il rende CONFORME : elle
  prouve que l'épreuve voit la différence, pas que la garde est la seule défense (tour 3, N9 ; BACKLOG A-622 ⑩). · Le cas « ISIN unique hors du CAC 40 »
  n'est pas joué : c'est la limite déclarée au ⑨ du vérificateur, comme l'échange de deux paires. · Un arrêt brutal
  laisse son dossier temporaire. · La durée s'affiche (« DURÉE ») ; elle n'est pas encore mesurée sous la mesure de couverture de la nuit, qui ralentit
  jusqu'à quatre fois (tests/LANCEMENT_DES_EPREUVES.json).
⑩ EFFET — Écrit et efface un dossier temporaire ; lance le vérificateur.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 s ; sort par sys.exit.
  [sort: oui]
"""
import csv
import glob
import io
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

VERIF = "programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py"
CARNET = "donnees/PROVENANCE_DES_FICHIERS.csv"
BNAINS = "donnees/sources_bnains/archives_bnains"
SEP = " · "


class NeSAppliquePlus(Exception):
    pass


def lancer(programme, racine, env=None, args=None, sans_b=False):
    """① Lancer le vérificateur. ⑤ DEUX valeurs : code, écran. ⑪ borné à 300 s.
      [rend: 2]
      [sort: non]"""
    p = subprocess.run([sys.executable] + ([] if sans_b else ["-B"]) + ["-I", programme] + ([racine] if args is None else args),
                       capture_output=True, text=True, timeout=300, env=env)
    return p.returncode, p.stdout + p.stderr


def construire_le_banc(depot, banc):
    """① Copier dans `banc` ce que lit le vérificateur. ⑤ UNE valeur : le chemin relatif du référentiel.
      [rend: 1]
      [sort: non]"""
    refs = [os.path.relpath(p, depot) for p in glob.glob(os.path.join(depot, "donnees", "REFERENTIEL_VALEURS_*.csv"))]
    if len(refs) != 1:
        raise NeSAppliquePlus(f"{len(refs)} référentiel(s) au dépôt")
    lus = list(csv.DictReader(open(os.path.join(depot, refs[0]), encoding="utf-8-sig", newline="")))
    # tout programmes/*.py, sans liste : le vérificateur charge le lecteur des cours, qui charge ses voisins
    # (relecteur du 24-10-2026, tour 4, D3 : une liste de quatre modules tombait dès qu'un voisin s'ajoutait)
    progs = {os.path.relpath(p, depot) for p in glob.glob(os.path.join(depot, "programmes", "*.py"))}
    a_copier = {VERIF, CARNET, refs[0], f"{BNAINS}/2016.ZIP"} | progs
    for r in lus:
        a_copier |= {f for f in (r.get("fichiers_cites") or "").split(";") if f}
    for f in sorted(a_copier):
        os.makedirs(os.path.dirname(os.path.join(banc, f)), exist_ok=True)
        shutil.copyfile(os.path.join(depot, f), os.path.join(banc, f))
    return refs[0]


def copie_du_banc(banc, dossier):
    """① Une copie du banc en liens durs. ⑤ —. [sort: non]"""
    for base, _, fichiers in os.walk(banc):
        cible = os.path.join(dossier, os.path.relpath(base, banc))
        os.makedirs(cible, exist_ok=True)
        for f in fichiers:
            os.link(os.path.join(base, f), os.path.join(cible, f))


def remplacer(dossier, chemin, octets):
    """① Remplacer un fichier d'une copie sans écrire à travers son lien. ⑤ —. [sort: non]"""
    p = os.path.join(dossier, chemin)
    if os.path.lexists(p):
        os.remove(p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(octets)


def fabriquer_les_cas(banc, ref):
    """① La table des cas. ⑤ UNE valeur : nom → (préparation, code attendu, fragment attendu).
      [rend: 1]
      [sort: non]"""
    orig = open(os.path.join(banc, ref), "rb").read()
    texte = orig.decode("utf-8-sig")
    lus = list(csv.DictReader(io.StringIO(texte, newline="")))
    champs = list(lus[0].keys())
    par_code = {r["mnemonique"]: r for r in lus}
    for c in ("AC", "AI", "BVI", "DSY", "ML", "ERF"):
        if c not in par_code:
            raise NeSAppliquePlus(f"la valeur {c} n'est plus au référentiel")
    carnet_txt = open(os.path.join(banc, CARNET), "rb").read()

    def ecrire(lignes, colonnes=champs):
        t = io.StringIO()
        w = csv.DictWriter(t, fieldnames=colonnes, extrasaction="ignore", lineterminator="\r\n")
        w.writeheader()
        w.writerows(lignes)
        return ("﻿" + t.getvalue()).encode("utf-8")

    def ligne(code, changer):
        def prep(d):
            copie = [dict(r) for r in lus]
            for r in copie:
                if r["mnemonique"] == code:
                    avant = dict(r)
                    changer(r)
                    if r == avant:
                        raise NeSAppliquePlus(f"le changement de la ligne {code} ne change rien")
            remplacer(d, ref, ecrire(copie))
        return prep

    def brut(a, b):
        def prep(d):
            if a not in orig:
                raise NeSAppliquePlus(f"« {a[:30]!r} » n'est plus au référentiel")
            remplacer(d, ref, orig.replace(a, b, 1))
        return prep

    def fichier(chemin, octets):
        def prep(d):
            p = os.path.join(d, chemin)
            if not os.path.isfile(p) or open(p, "rb").read() == octets:
                raise NeSAppliquePlus(f"{chemin} est absent du banc, ou le remplacer ne change rien")
            remplacer(d, chemin, octets)
        return prep

    def cite(code, fin):
        x = [f for f in par_code[code]["fichiers_cites"].split(";") if f.endswith(fin)]
        if len(x) != 1:
            raise NeSAppliquePlus(f"la ligne {code} ne cite pas un seul fichier finissant par {fin}")
        return x[0]

    def morceaux_sans(r, motif):
        return SEP.join(p for p in r["citation"].split(SEP) if motif not in p)

    def ajouter(texte, a):
        return texte + ";" + a

    adresses = {}
    for x in csv.DictReader(io.StringIO(carnet_txt.decode("utf-8-sig"))):
        adresses.setdefault(x["fichier"], []).append(x["adresse"])

    def retirer_le_morceau(r, motif):
        # retire le morceau qui porte `motif`, puis le fichier qu'il désignait s'il ne sert plus, puis les adresses
        # que le carnet donne à ce fichier : rien n'est écrit en dur (relecteur du 24-10-2026, tour 4, D4)
        garde = [p for p in r["citation"].split(SEP) if motif not in p]
        otes = [p for p in r["citation"].split(SEP) if motif in p]
        if len(otes) != 1:
            raise NeSAppliquePlus(f"la ligne {r['mnemonique']} n'a pas un seul morceau qui porte « {motif[:30]} »")
        nom = otes[0].split(" : « ", 1)[0].split(" › ")[0]
        cites = r["fichiers_cites"].split(";")
        if not any(p.split(" : « ", 1)[0].split(" › ")[0] == nom for p in garde):
            f = [c for c in cites if os.path.basename(c) == nom]
            cites = [c for c in cites if c not in f]
            sources = [a for a in r["source"].split(";") if not any(a in adresses.get(x, []) for x in f)]
            r["source"] = ";".join(sources)
        r["citation"], r["fichiers_cites"] = SEP.join(garde), ";".join(cites)

    yahoo_ai = cite("AI", "/AI.PA.json")
    yahoo_ac = cite("AC", "/AC.PA.json")
    adresse_ai = [r for r in csv.DictReader(io.StringIO(carnet_txt.decode("utf-8-sig"))) if r["fichier"] == yahoo_ai]
    if not adresse_ai:
        raise NeSAppliquePlus("la réponse de Yahoo d'AI n'est plus au carnet")
    adresse_ai = adresse_ai[0]["adresse"]
    # le cas d'une archive imbriquée : la ligne d'Accor du dernier jour de 2016
    z = zipfile.ZipFile(os.path.join(banc, BNAINS, "2016.ZIP"))
    m = sorted(n for n in z.namelist() if n.upper().endswith(".ZIP"))[-1]
    z2 = zipfile.ZipFile(io.BytesIO(z.read(m)))
    jour = sorted(n for n in z2.namelist() if n.lower().endswith(".txt"))[-1]
    acc = [l for l in z2.read(jour).decode("latin-1").splitlines() if l.split("\t")[0] == par_code["AC"]["isin"]]
    if not acc:
        raise NeSAppliquePlus("Accor n'est pas dans le dernier jour de 2016.ZIP")
    adresse_2016 = [r["adresse"] for r in csv.DictReader(io.StringIO(carnet_txt.decode("utf-8-sig")))
                    if r["fichier"] == f"{BNAINS}/2016.ZIP"]

    def imbriquee(r):
        r["citation"] = f"2016.ZIP › {m} › {jour} : « {acc[0]} »" + SEP + r["citation"]
        r["fichiers_cites"] = f"{BNAINS}/2016.ZIP;" + r["fichiers_cites"]
        r["source"] = ";".join(adresse_2016 + [r["source"]])

    def sans_case(d):
        t = orig.split(b"\r\n")
        t[2] = t[2].rsplit(b",", 1)[0]           # la dernière case de la ligne d'AI retirée
        remplacer(d, ref, b"\r\n".join(t))

    def deux_ref(d):
        remplacer(d, ref.replace("REFERENTIEL_VALEURS_", "REFERENTIEL_VALEURS_COPIE_"), orig)

    def ref_dossier(d):
        os.remove(os.path.join(d, ref))
        os.makedirs(os.path.join(d, ref))

    l_ml = "FR0000121261\tMICHELIN"
    return {
        "V00_temoin": (lambda d: None, 0, "VERDICT CONFORME"),
        "V01_isin_d_air_liquide_sur_accor": (brut(b"ACCOR,FR0000120404", b"ACCOR,FR0000120073"), 1, "est porté par deux lignes"),
        "V02_code_ai_sur_accor": (brut(b"ACCOR,FR0000120404,AC,", b"ACCOR,FR0000120404,AI,"), 1, "AI est porté par deux lignes"),
        "V03_code_ai_sur_accor_avec_sa_preuve_yahoo": (ligne("AC", lambda r: r.update(
            mnemonique="AI", citation=r["citation"].replace("AC.PA", "AI.PA").replace('"longName":"Accor SA"', '"longName":"L\'Air Liquide S.A."'),
            fichiers_cites=r["fichiers_cites"].replace("AC.PA.json", "AI.PA.json"), source=r["source"].replace("chart/AC.PA", "chart/AI.PA"))),
            1, "AI est porté par deux lignes"),
        "V04_nom_en_double": (ligne("AI", lambda r: r.update(nom_usuel="ACCOR")), 1, "le lecteur des cours refuse le référentiel"),
        "V04b_nom_en_double_a_la_casse_pres": (ligne("AI", lambda r: r.update(nom_usuel="Accor")), 1, "désigne AC et AI"),
        "V04c_nom_d_onglet_d_une_autre_valeur": (ligne("AI", lambda r: r.update(onglet_google="ACCOR")), 1, "désigne AC et AI"),
        "V04d_case_en_trop": (brut(b"ACCOR,FR0000120404,AC,", b"ACCOR,,FR0000120404,AC,"), 1, "cases au lieu de"),
        "V05_espace_en_bord_du_code": (ligne("AC", lambda r: r.update(mnemonique="AC ")), 1, "porte une espace en bord"),
        "V05b_espace_en_bord_du_nom": (ligne("AC", lambda r: r.update(nom_usuel="ACCOR ")), 1, "la colonne nom_usuel porte une espace en bord"),
        "V06_citation_raccourcie": (ligne("AC", lambda r: r.update(citation=SEP.join(
            (p.split("\t")[0] + "\t" + p.split("\t")[1] + " »") if p.startswith("201702.ZIP") else p for p in r["citation"].split(SEP)))),
            1, "n'est pas une ligne entière"),
        "V07_citation_recousue": (ligne("BVI", lambda r: r.update(citation=r["citation"].replace("\tBUREAU VERITAS\t", "\tLEGRAND\t"))), 1, "n'est pas une ligne entière"),
        "V08_nom_yahoo_pris_dans_un_autre_fichier": (ligne("AC", lambda r: r.update(
            citation=morceaux_sans(r, '"longName"') + SEP + 'AI.PA.json : « "longName":"L\'Air Liquide S.A." »',
            fichiers_cites=ajouter(r["fichiers_cites"], yahoo_ai), source=ajouter(r["source"], adresse_ai))),
            1, "n'est pas cité dans la réponse de Yahoo dont"),
        "V09_nom_yahoo_d_une_autre_valeur": (ligne("AC", lambda r: r.update(citation=r["citation"].replace('"longName":"Accor SA"', '"longName":"L\'Air Liquide S.A."'))), 1, "n'est pas un membre"),
        "V10_nom_yahoo_retire": (ligne("AC", lambda r: r.update(citation=morceaux_sans(r, '"longName"'))), 1, "le \"longName\" n'est pas cité"),
        "V11_symbole_yahoo_retire": (ligne("AC", lambda r: r.update(citation=morceaux_sans(r, '"symbol"'))), 1, "aucune réponse de Yahoo citée"),
        "V12_fichier_cite_en_trop": (ligne("AC", lambda r: r.update(fichiers_cites=ajouter(r["fichiers_cites"], yahoo_ai), source=ajouter(r["source"], adresse_ai))), 1, "ne sert à aucun morceau"),
        "V13_adresse_fausse": (ligne("AC", lambda r: r.update(source=r["source"].replace("https://www.bnains.org", "https://exemple.org"))), 1, "la colonne source n'est pas"),
        "V14_ancien_isin_de_michelin_sans_preuve": (ligne("ML", lambda r: retirer_le_morceau(r, l_ml)),
            1, "n'a pour clé FR0000121261"),
        "V15_ancien_isin_de_dassault_prouve_par_l_avis": (ligne("DSY", lambda r: retirer_le_morceau(r, "FR0000130650\tDASSAULT")),
            0, "VERDICT CONFORME"),
        "V16_archive_imbriquee": (ligne("AC", imbriquee), 0, "VERDICT CONFORME"),
        "V17_avis_echange": (fichier("donnees/sources_du_referentiel/ERF_EUREX_Info_002_ERF.pdf",
                                     open(os.path.join(banc, "donnees/sources_du_referentiel/DSY_EUREX_Info_002_DYS1.pdf"), "rb").read()),
                             1, "n'est pas une ligne entière de ERF_"),
        "V18_colonnes_de_preuve_absentes": (lambda d: remplacer(d, ref, ecrire(lus, [c for c in champs if c not in ("source", "citation", "fichiers_cites")])), 1, "référentiel sans les colonnes"),
        "V19_referentiel_vide": (lambda d: remplacer(d, ref, ecrire([])), 1, "référentiel vide"),
        "V20_fichier_absent_du_carnet": (fichier(CARNET, b"\n".join(l for l in carnet_txt.split(b"\n") if not l.startswith(yahoo_ac.encode() + b","))), 1, "n'est pas au carnet"),
        "V21_morceau_mal_forme": (ligne("AC", lambda r: r.update(citation=r["citation"] + SEP + "sans guillemets")), 1, "mal formé"),
        "V22_designation_sans_fichier": (ligne("AC", lambda r: r.update(citation=r["citation"] + SEP + "INCONNU.ZIP › x.txt : « y »")), 1, "ne désigne aucun fichier cité"),
        "V23_type_de_fichier_inconnu": (ligne("AC", lambda r: r.update(citation=r["citation"] + SEP + "PROVENANCE_DES_FICHIERS.csv : « x »", fichiers_cites=ajouter(r["fichiers_cites"], CARNET))), 1, "n'est ni une archive"),
        "V24_archive_sans_fichier_du_jour": (ligne("AC", lambda r: r.update(citation=r["citation"].replace("201702.ZIP › ", "201702.ZIP", 1).replace("201702.ZIP20170228.txt", "201702.ZIP"))), 1, "ne dit pas quel fichier du jour"),
        "V25_reponse_yahoo_sans_resultat": (fichier(yahoo_ac, b'{"chart":{"result":[]}}'), 1, "n'est pas un membre"),
        "V26_referentiel_absent": (lambda d: os.remove(os.path.join(d, ref)), 2, "0 référentiel(s)"),
        "V27_deux_referentiels": (deux_ref, 2, "2 référentiel(s)"),
        "V28_referentiel_illisible": (ref_dossier, 2, "référentiel illisible"),
        "V29_carnet_absent": (lambda d: os.remove(os.path.join(d, CARNET)), 2, "carnet illisible"),
        "V30_archive_corrompue": (fichier(f"{BNAINS}/201702.ZIP", b"pas une archive"), 2, "illisible"),
        "V31_reponse_yahoo_illisible": (fichier(yahoo_ac, b"{pas du json"), 2, "illisible"),
        "V32_avis_corrompu": (fichier("donnees/sources_du_referentiel/DSY_EUREX_Info_002_DYS1.pdf", b"pas un pdf"), 2, "pdftotext a échoué"),
        "V33_case_manquante": (sans_case, 1, "cases au lieu de"),
        "V36_lance_sans_option_B_n_ecrit_rien": ("SANS_B", 0, "VERDICT CONFORME"),
        "V37_referentiel_en_latin1": (lambda d: remplacer(d, ref, orig.decode("utf-8-sig").encode("latin-1", "replace")), 2, "erreur imprévue"),
        "V34_pdftotext_absent": ("SANS_PDFTOTEXT", 2, "pdftotext n'a pas pu lire"),
        "V35_appel_sans_racine": ("SANS_RACINE", 2, "appel mal formé"),
    }


def jouer(banc, travail, cas, programme_relatif, bavard=True, jusqu_a_la_premiere_chute=False):
    """① Jouer les cas avec un vérificateur donné. ⑤ DEUX valeurs : justes, faux (listes de noms).
      [rend: 2]
      [sort: non]"""
    justes, faux = [], []
    for nom, (prep, attendu, fragment) in cas.items():
        d = tempfile.mkdtemp(prefix="cas_", dir=travail)
        try:
            copie_du_banc(banc, d)
            env, args = None, None
            if prep == "SANS_PDFTOTEXT":
                env = dict(os.environ, PATH="/nonexistent")
            elif prep == "SANS_RACINE":
                args = []
            elif prep != "SANS_B":
                prep(d)
            code, ecran = lancer(os.path.join(d, programme_relatif), d, env, args, sans_b=(prep == "SANS_B"))
            ok = code == attendu and fragment in ecran
            if prep == "SANS_B" and os.path.exists(os.path.join(d, "programmes", "__pycache__")):
                ok, ecran = False, ecran + "\nDÉFAUT DE L'ÉPREUVE : programmes/__pycache__ a été écrit"
            (justes if ok else faux).append(nom)
            if bavard or not ok:
                derniere = [l for l in ecran.splitlines() if l.startswith(("DÉFAUT", "VERDICT", "Traceback"))][:2]
                print(("OK   " if ok else "FAUX ") + f"{nom} : code {code} (attendu {attendu}, motif « {fragment} ») — "
                      + " | ".join(x[:100] for x in derniere))
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if jusqu_a_la_premiere_chute and faux:
            break
    return justes, faux


GARDES = {
    "G01_unicite": ("            if k in vus:\n", "            if False:\n"),
    "G02_espace_en_bord": ("            if r[c] != r[c].strip():", "            if False:"),
    "G03_ligne_entiere_de_paris": ("            if texte not in cache[cle]:", "            if False:"),
    "G04_ligne_entiere_du_pdf": ("            if texte not in cache[f]:", "            if False:"),
    "G05_membre_de_yahoo": ("            if not y or cache[f].get(y.group(1)) != y.group(2):", "            if not y:"),
    "G06_couverture_des_isin": ("        if k not in cles:", "        if False:"),
    "G07_symbole_de_yahoo": ("    if not fichiers_du_code:", "    if False:"),
    "G08_nom_yahoo_du_meme_fichier": ("    elif not any(\"longName\" in yahoo.get(f, ()) for f in fichiers_du_code):",
                                      "    elif not any(\"longName\" in v for v in yahoo.values()):"),
    "G09_fichier_inutile": ("        if f not in utilises:", "        if False:"),
    "G10_adresses_du_carnet": ("    if r[\"source\"] != \";\".join(attendu):", "    if False:"),
    "G11_fichier_absent_du_carnet": ("        if f not in carnet:\n", "        if f not in carnet and False:\n"),
    "G12_morceau_mal_forme": ("    d += [f\"{code} : morceau de citation mal formé", "    d += [][:0] and [f\"{code} : morceau de citation mal formé"),
    "G13_designation_sans_fichier": ("        if f is None:\n", "        if f is None and False:\n"),
    "G14_type_inconnu": ("            d.append(f\"{code} : {f} n'est ni une archive", "            pass  # d.append(f\"{code} : {f} n'est ni une archive"),
    "G15_archive_sans_fichier_du_jour": ("            if len(parties) < 2:", "            if False:"),
    "G16_referentiel_vide": ("    if not lus:\n        return [\"référentiel vide\"]", "    if False:\n        return [\"référentiel vide\"]"),
    "G17_colonnes_absentes": ("    if manque:", "    if False:"),
    "G19_identite_des_noms": ("    refus = identite_des_noms(racine)\n", "    refus = []\n"),
    "G20_arret_si_le_lecteur_refuse": ("    if refus:                                           # le lecteur refuse", "    if False:  # le lecteur refuse"),
    "G21_pas_de_cache_de_compilation": ("    sys.dont_write_bytecode = True                      # le chargement", "    pass  # le chargement"),
    "G18_dernier_filet": ("    except Exception as e:                                # dernier filet",
                          "    except ZeroDivisionError as e:                        # dernier filet"),
}


def main(argv):
    """① Le point d'entrée. ⑤ UNE valeur : le code de sortie (voir le ⑤ du programme).
      [rend: 1]
      [sort: non]"""
    args = [a for a in argv[1:] if a != "--saboter"]
    saboter = "--saboter" in argv[1:]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__.split("③")[0])
        print("VERDICT IMPOSSIBLE — appel mal formé")
        return 2
    if shutil.which("pdftotext") is None:
        print("VERDICT IMPOSSIBLE — pdftotext n'est pas installé : aucun cas n'est joué")
        return 2
    depot = os.path.abspath(args[0])
    debut = time.monotonic()
    travail = tempfile.mkdtemp(prefix="epreuves_preuves_referentiel.")
    try:
        banc = os.path.join(travail, "banc")
        ref = construire_le_banc(depot, banc)
        cas = fabriquer_les_cas(banc, ref)
        justes, faux = jouer(banc, travail, cas, VERIF)
        print(f"BILAN {len(justes)} / {len(cas)} cas justes")
        ok = not faux
        impossible = False
        if saboter:
            source = open(os.path.join(banc, VERIF), encoding="utf-8").read()
            for nom, (a, b) in GARDES.items():
                if source.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS")
                    impossible = True
                    continue
                sab = os.path.join(travail, "sabotage")
                shutil.rmtree(sab, ignore_errors=True)
                copie_du_banc(banc, sab)
                remplacer(sab, VERIF, source.replace(a, b).encode("utf-8"))
                _, tombes = jouer(sab, travail, cas, VERIF, bavard=False, jusqu_a_la_premiere_chute=True)
                shutil.rmtree(sab, ignore_errors=True)
                print(f"{nom} mord : {tombes}" if tombes else f"{nom} NE MORD PAS []")
                ok = ok and bool(tombes)
    except NeSAppliquePlus as e:
        print(f"VERDICT IMPOSSIBLE — un cas ne s'applique plus : {e}")
        return 2
    except Exception as e:                                # dernier filet : une panne de l'épreuve n'est pas un verdict
        print(f"VERDICT IMPOSSIBLE — erreur imprévue de l'épreuve : {type(e).__name__} : {e}")
        return 2
    finally:
        shutil.rmtree(travail, ignore_errors=True)
    if impossible:
        print("VERDICT IMPOSSIBLE — une garde ne s'applique plus")
        return 2
    print(f"DURÉE {time.monotonic() - debut:.0f} s")
    print("VERDICT", "CONFORME" if ok else "NON CONFORME")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
