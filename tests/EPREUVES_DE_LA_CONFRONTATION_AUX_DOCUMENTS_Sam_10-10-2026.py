#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_CONFRONTATION_AUX_DOCUMENTS — Sam 10-10-2026 (Paris)
Rôle : prouver que programmes/CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py refuse une phrase absente de son document
et un chiffre que ses phrases contredisent, et n'accepte rien en silence ; que
etudes/outils/RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES.py remplit la colonne des phrases sans rien d'autre ; que
etudes/outils/GARDER_LES_DOCUMENTS_DES_DROITS.py garde sans copier deux fois ; et que chaque épreuve a des dents (R-731).
Quand l'appeler : avant toute livraison qui touche l'un de ces trois programmes, la table
donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv ou le registre des documents gardés.

À QUOI ÇA SERT. Décision de Jean-Luc du 10-10-2026 à 13h18 : « 1 » à « Écrire le programme qui confronte chaque
citation et chaque chiffre déclaré à son document gardé, et refuse ce qui n'y est pas ». Le cas qui doit ÉCHOUER est
celui de Cowork (relecture du 10-10-2026, 22cc10b) : Société Générale 2008 déclarée à 47,00 € au lieu de 47,50 €,
qui passe tous les contrôles des cours. Les épreuves C1 à C5 jouent des phrases RÉELLES des documents gardés ; C6 les
VRAIS documents ; C7 la VRAIE table sur une copie, puis la même copie faussée ; C8 et C9 les deux outils, sur copie.

LES ÉPREUVES :
C1  forme : ligature « ﬁ », espace insécable, apostrophe courbe, accents, tiret demi-cadratin, trait d'union
    conditionnel ramenés.
C2  phrase_dans_le_texte : mot pour mot ; « […] » saute un passage, dans l'ordre seulement ; une phrase vide → faux ;
    « 7,50 euros », « 50 euros » et « est de 47 euros » ne sont pas trouvés dans « est de 47,50 euros », ni « prix »
    dans « prixes » (frontière de mot).
C3  montants : « 47,50 euros », « €59.65 », « (euro)26.50 », « 0,90 EUR », « 1287.000 € », « 45 euros »,
    « 4 005 337 152,50 euros », « 476.842.699 euros » ; « 50.000 euros » est ambigu et ne compte pas ; un nombre
    sans monnaie, ou suivi de « Euronext », n'en est pas un.
C4  parites : « 1action … pour 10 » (BNP Paribas 2006), « (1) action nouvelle pour 20 » (Société Générale 2006),
    « une (1) … pour cinq (5) » (Pernod Ricard 2007), « deux (2) … pour quarante et une (41) » (LVMH 2014),
    « 12 droits … donneront le droit de souscrire à 1 action » (AXA 2009), « Six Rights will entitle the holder to
    purchase one Share » (Veolia 2002), « au prix de 16,07 euros pour onze » (Crédit Agricole 2003 : 11, pas 16,07) ;
    une date (« le 21 février 2008 pour 3 », « 1er janvier 2006 pour 3 ») ne fait pas de parité.
C5  juger_la_ligne, sur des phrases réelles : prix de Société Générale 2008 — 47,50 prouvé ; 47,00 CONTREDIT (le cas de
    Cowork) ; 47,504 prouvé, 47,51 contredit ; 77,72 (le cours de clôture) et 5,86 (la valeur du droit), écrits dans
    une autre phrase de la ligne, contredits ; « au prix de 19,80 euros avec un cours de bourse de 24,47 euros » :
    24,47 contredit · parité 4 prouvée, 5 et 4,02 contredites · dividende 0,90 non prouvé sans phrase de dividende,
    prouvé par « un dividende de 0,90 euros », contredit à 0,95 ; un « prix de souscription de 0,90 euros » ne le
    prouve pas ; vide alors qu'une phrase en écrit un : « à lire » · prix 0 prouvé par « actions gratuites »,
    contredit par une phrase de prix ou par un « prix d'exercice » (Saint-Gobain 2009) ; des BSA attribués
    « gratuitement » ne le prouvent pas · prix ou parité vide pour un droit : « non déclaré » · valeur distribuée
    (Accor 2010) : 13 prouvé avec la parité de 1 pour 1, 14,80 contredit ; sans parité de 1 pour 1, non prouvée
    (TotalEnergies 2006) · « closing price of €84.65 » ne contredit pas un prix de 59,65 · une seconde phrase qui
    écrit un autre prix (46,00) ou une autre parité (« 3 actifs pour les 15 mois ») contredit, même à côté de la bonne · un
    montant au-delà de 80 signes, ou de l'autre côté d'un « […] », n'est pas lié · « at a price of € 12.75 » (AXA
    2003) lie le prix · prix ET valeur distribuée :
    « deux natures » · jour « écrit » par la phrase qui l'écrit, « non écrit » sinon.
C6  texte_du_document sur les vrais documents gardés : un PDF (le BALO de Société Générale 2008) ; une phrase de BNP
    Paribas 2006 que la mise en page en colonnes coupe dans `-layout` et que l'ordre de lecture garde ; un .doc
    (Pernod Ricard 2007) ; une page web dont le texte d'un <script> ne compte pas.
C7  main sur une COPIE de la vraie table et des vrais documents : code 0 et le résumé mesuré le 10-10-2026 ; puis la
    copie faussée — chaque fois code 1 et le refus nommé : prix de Société Générale 2008 à 47,00 ; Michelin 2010 à
    46 €, sa phrase du prix remplacée par une phrase ABSENTE du document qui écrit 46 € (elle ne prouve rien : le prix
    reste NON PROUVÉ) ; une phrase de la note de BNP
    Paribas 2006 attribuée au BALO ; une phrase attribuée à un fichier hors registre ; la phrase du prix de Société
    Générale 2008 recopiée chez Michelin 2010 déclaré à 47,50, le nom du BALO ajouté à sa citation (document NON
    INVOQUÉ) ; la phrase du prix de Michelin
    retirée (non prouvé SANS RAISON) ; TotalEnergies déclaré 27 (la raison ne commence pas par ce chiffre) ; une
    raison écrite pour le prix prouvé de Danone ; un document gardé dont un octet change, sa taille gardée, ou dont
    la taille au registre est fausse (MODIFIÉ) — puis code 2 : un document gardé effacé, l'en-tête de la table faux, l'en-tête du
    registre faux, pdftotext introuvable.
C8  le relevé des phrases, sur copie : la table SANS les deux colonnes nouvelles → la colonne des phrases remplie,
    82 phrases, chacune dans la colonne du dépôt, la colonne des raisons vide, et rien d'autre de la table changé ;
    relancé, il ne change plus rien (octet pour octet) ; un document gardé modifié → code 2 et la table intacte.
C9  la garde des documents, réseau remplacé : adresses_de_la_ligne ôte « (page 274 du PDF) » et la ponctuation
    finale ; une réponse 403 et un contenu trop court ne sont pas gardés ; un contenu déjà gardé ailleurs (le
    communiqué d'Accor) est inscrit en renvoyant à ce fichier ; une adresse d'un autre registre (bnains) aussi ; un
    contenu neuf est écrit et inscrit ; les lignes déjà au registre ne changent pas.

LES SABOTAGES (avec --saboter) — S1 accents gardés · S2 apostrophes non ramenées · S3 seule la lecture -layout ·
S4 <script> gardé · S5 l'ordre des morceaux ignoré · S6 tolérance d'un montant à 5 centimes · S7 jamais
« contredit » · S8 tout « prix » pris pour un prix de souscription · S9 les montants comptés dans une parité · S10
les années comptées dans une parité · S11 un mot et ses chiffres comptés deux fois · S12 « donneront le droit »
oublié · S13 l'empreinte non vérifiée · S14 une phrase hors registre passée sous silence · S15 une erreur rend 0 ·
S16 le jour toujours écrit · S17 un dividende vide jamais « à lire » · S18 le relevé ajoute les doublons · S19 un
contenu trop court gardé · S20 un contenu déjà gardé recopié · S21 « […] » non coupé · S22 un prix nul toujours
prouvé · S23 la parité à 1 % près · S24 tout montant après le mot lié, pas le premier · S25 le document non invoqué
accepté · S26 sans frontière de mot · S27 la raison sans son chiffre · S28 la taille non vérifiée · S29 l'en-tête du
registre non vérifié · S30 les phrases absentes comptées comme preuves · S31 prix vide d'un droit accepté · S32 la
valeur distribuée sans parité de 1 pour 1 · S33 « 50.000 » lu 50 · S34 un dividende à lire non bloquant · S35 une
raison pour un chiffre prouvé acceptée · S36 « gratuitement » pris pour des actions gratuites · S37 un montant lié
à 100 000 signes · S38 « prouvé » dès qu'UNE écriture vaut le chiffre · S39 les montants lus à travers « […] » ·
S40 le nom de fichier dans la citation invoque le document · S41 une ligne à deux natures acceptée · S42 la parité
prouvée par UNE écriture · S43 « at a price of » oublié.

USAGE : python3 tests/EPREUVES_DE_LA_CONFRONTATION_AUX_DOCUMENTS_Sam_10-10-2026.py <racine du dépôt>
        [--saboter | --saboter=S1,S2…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import contextlib, csv, hashlib, importlib.util, io, os, shutil, sys, tempfile, urllib.error

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROGRAMMES = os.path.join(RACINE, "programmes")
CONFRONTATION = os.path.join(PROGRAMMES, "CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py")
RELEVE = os.path.join(RACINE, "etudes", "outils", "RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES.py")
GARDE = os.path.join(RACINE, "etudes", "outils", "GARDER_LES_DOCUMENTS_DES_DROITS.py")
DOSSIER = os.path.join("temoins", "DOCUMENTS_DES_DROITS_REGLE_OFFICIELLE_Sam_10-10-2026")
# Le résumé du 10-10-2026 sur la vraie table (mesuré par le programme, recopié ici comme valeur attendue).
RESUME = "RÉSUMÉ : lignes 32 · refus 0 · non prouvés 5 · à lire 0"   # 11 avant les documents de la SEC (10-10-2026, soir)
# Le relevé, passé sur la table sans la colonne, inscrit 82 phrases (mesuré le 10-10-2026 au soir, après l'inscription
# des trois documents de la SEC gardés par Cowork : 77 avant) ; la colonne du dépôt en porte 105 : les 23 autres ont été
# ajoutées à la main par le Chat le même jour, cherchées dans les documents.
RELEVEES = 82
# Phrases réelles, relevées dans les documents gardés le 10-10-2026.
SG_PRIX = "Le prix de souscription est de 47,50 euros par action"
SG_PARITE = "à raison de 1 action nouvelle pour 4 actions anciennes"
SG_JOUR = "La souscription des actions sera ouverte du 21 février 2008 au 29 février 2008 inclus."
SG_VALEUR = ("Sur la base du cours de clôture de l’action Société Générale le 8 février 2008, soit 77,72 euros, la "
             "valeur théorique du droit préférentiel de souscription s’élève à 5,86 euros")
ACCOR = ["Ainsi, chaque actionnaire de Accor recevra une action Edenred pour une action Accor détenue.",
         "Le premier jour de cotation, 2 juillet 2010, marquait une hausse avec un cours d’ouverture à 13 euros et un "
         "cours de clôture à 14,80 euros."]
BNP_COLONNES = ("Les droits préférentiels de souscription seront détachés des actions le 6 mars 2006 après la séance "
                "de bourse et négociables sur le marché Eurolist d’Euronext Paris du 7 mars 2006 au 20 mars 2006 inclus.")

SABOTAGES = {
    "S1": (CONFRONTATION, "if not unicodedata.combining(c) and c != chr(0xAD)", "if c != chr(0xAD)"),
    "S2": (CONFRONTATION, "    x = re.sub(r\"[’‘ʼ`´]\", \"'\", x)\n", ""),
    "S3": (CONFRONTATION, "for options in ([\"-layout\"], []):", "for options in ([\"-layout\"],):"),
    "S4": (CONFRONTATION, "        t = re.sub(r\"(?is)<(script|style)\\b.*?</\\1\\s*>\", \" \", t)\n", ""),
    "S5": (CONFRONTATION, "            position = i + len(m)\n", "            position = 0\n"),
    "S6": (CONFRONTATION, "AU_CENTIME = 0.005 ", "AU_CENTIME = 0.05 "),
    "S7": (CONFRONTATION, "\"prouvé\" if ok else \"contredit\" if contredit else \"non prouvé\"",
           "\"prouvé\" if ok else \"non prouvé\""),
    "S8": (CONFRONTATION, "MOTS_PRIX = re.compile(r\"prix (?:unitaire )?(?:de souscription|d'emission|d'exercice)|prix unitaire|au prix de\"",
           "MOTS_PRIX = re.compile(r\"prix|price\""),
    "S9": (CONFRONTATION, "if m.start(2) in pris or re.fullmatch", "if re.fullmatch"),
    "S10": (CONFRONTATION, "if m.start(2) in pris or re.fullmatch(r\"(19|20)\\d\\d\", texte):", "if m.start(2) in pris:"),
    "S11": (CONFRONTATION, "                nombres.pop()                # « cinq (5) »", "                pass                # « cinq (5) »"),
    "S12": (CONFRONTATION, "permettront|permettent|donneront le droit|donnent le droit|entitle", "permettront|permettent|entitle"),
    "S13": (CONFRONTATION, "if hashlib.sha256(contenu).hexdigest() != r[\"sha256\"] or str(len(contenu)) != r[\"octets\"]:",
            "if str(len(contenu)) != r[\"octets\"]:"),
    "S14": (CONFRONTATION, "                refus.append(f\"{nom} : phrase attribuée à un document NON GARDÉ", "                (f\"{nom} : phrase attribuée à un document NON GARDÉ"),
    "S15": (CONFRONTATION, "        print(f\"LA CONFRONTATION N'A PAS PU TOURNER : {type(e).__name__} : {e}\")\n        return 2",
            "        print(f\"LA CONFRONTATION N'A PAS PU TOURNER : {type(e).__name__} : {e}\")\n        return 0"),
    "S16": (CONFRONTATION, "\"écrit\" if any(K.jour_ecrit(f\"« {p} »\", jour) for p in phrases) else \"non écrit\"",
            "\"écrit\""),
    "S17": (CONFRONTATION, "    elif lies[\"dividende\"]:\n        verdicts.append((\"dividende_non_attache\", \"\", \"à lire\"))\n", ""),
    "S18": (RELEVE, "                if e not in entrees:\n", "                if True:\n"),
    "S19": (GARDE, "            if len(contenu) < PLUS_PETIT:", "            if len(contenu) < 0:"),
    "S20": (GARDE, "            if empreinte in par_empreinte:", "            if False:"),
    "S21": (CONFRONTATION, "COUPURE = re.compile(r\"\\s*\\[(?:…|\\.\\.\\.)\\]\\s*\")", "COUPURE = re.compile(r\"\\A\\Z\\Z\")"),
    "S22": (CONFRONTATION, "juger(\"prix_souscription\", not lies[\"prix\"] and any(GRATUIT.search(p) for p in formes), bool(lies[\"prix\"]))",
            "juger(\"prix_souscription\", True, False)"),
    "S23": (CONFRONTATION, "PARITE_RELATIVE = 1e-6 ", "PARITE_RELATIVE = 1e-2 "),
    "S24": (CONFRONTATION, "            lies.append(suivants[0])", "            lies.extend(suivants)"),
    "S25": (CONFRONTATION, "            if fichier not in invoques:", "            if False:"),
    "S26": (CONFRONTATION, "            while i >= 0 and not borne(t, i, m):", "            while False:"),
    "S27": (CONFRONTATION, "                elif not raisons[grandeur].startswith((chiffre + \" \", chiffre.replace(\".\", \",\") + \" \")):",
            "                elif False:"),
    "S28": (CONFRONTATION, "if hashlib.sha256(contenu).hexdigest() != r[\"sha256\"] or str(len(contenu)) != r[\"octets\"]:",
            "if hashlib.sha256(contenu).hexdigest() != r[\"sha256\"]:"),
    "S29": (CONFRONTATION, "        if lecteur.fieldnames != COLONNES_DU_REGISTRE:", "        if False:"),
    "S30": (CONFRONTATION, "        verdicts = juger_la_ligne(r, trouvees)", "        verdicts = juger_la_ligne(r, [p for _, p in entrees])"),
    "S31": (CONFRONTATION, "    elif droit:\n        verdicts.append((\"prix_souscription\", \"\", \"non déclaré\"))\n", ""),
    "S32": (CONFRONTATION, "juger(\"valeur_distribuee\", un_pour_un and egal(v, lies[\"ouverture\"]), un_pour_un and differe(v, lies[\"ouverture\"]))",
            "juger(\"valeur_distribuee\", egal(v, lies[\"ouverture\"]), differe(v, lies[\"ouverture\"]))"),
    "S33": (CONFRONTATION, "    if re.fullmatch(r\"\\d{1,3}\\.\\d{3}\", s):\n        return None\n", ""),
    "S34": (CONFRONTATION, "                    refus.append(f\"{nom} : une phrase écrit un dividende, la ligne n'en déclare AUCUN",
            "                    a_lire.append(f\"{nom} : une phrase écrit un dividende, la ligne n'en déclare AUCUN"),
    "S35": (CONFRONTATION, "                refus.append(f\"{nom} : raison écrite pour « {grandeur} »", "                (f\"{nom} : raison écrite pour « {grandeur} »"),
    "S37": (CONFRONTATION, "LIEN = 80 ", "LIEN = 100000 "),
    "S38": (CONFRONTATION, "egal = lambda valeur, liste: bool(liste) and all(abs(v - valeur) <= AU_CENTIME for v in liste)",
            "egal = lambda valeur, liste: any(abs(v - valeur) <= AU_CENTIME for v in liste)"),
    "S39": (CONFRONTATION, "    morceaux = [forme(m) for p in phrases for m in COUPURE.split(p) if forme(m)]",
            "    morceaux = formes"),
    "S40": (CONFRONTATION, "if a in adresses]", "if a in adresses or os.path.basename(f) in r[\"citation\"]]"),
    "S41": (CONFRONTATION, "            verdicts.append((\"valeur_distribuee\", r[\"valeur_distribuee\"], \"deux natures\"))", "            pass"),
    "S42": (CONFRONTATION, "              bool(toutes_parites) and all(abs(q - n) <= PARITE_RELATIVE * n for q in toutes_parites),",
            "              any(abs(q - n) <= PARITE_RELATIVE * n for q in toutes_parites),"),
    "S43": (CONFRONTATION, "|offer price|at a price of\")", "|offer price\")"),
    "S36": (CONFRONTATION, "GRATUIT = re.compile(r\"actions? (?:nouvelles? )?gratuites?|", "GRATUIT = re.compile(r\"gratuit|"),
}


def charger(sabotage=None):
    """Charge la confrontation, le relevé et la garde — les vrais fichiers, ou des copies dont l'un est saboté."""
    dossier = tempfile.mkdtemp()
    for f in ("CONTRATS_DES_FICHIERS.py", "CONTROLER_L_HISTORIQUE_LONG.py", "COMMUN.py",
              "CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py"):
        shutil.copy(os.path.join(PROGRAMMES, f), dossier)
    shutil.copy(RELEVE, dossier)
    shutil.copy(GARDE, dossier)
    if sabotage:
        chemin, cible, remplace = sabotage
        copie = os.path.join(dossier, os.path.basename(chemin))
        open(copie, "w", encoding="utf-8").write(open(chemin, encoding="utf-8").read().replace(cible, remplace))
    noms = ("CONTRATS_DES_FICHIERS", "COMMUN", "CONTROLER_L_HISTORIQUE_LONG", "CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS",
            "RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES", "GARDER_LES_DOCUMENTS_DES_DROITS")
    for nom in noms:
        sys.modules.pop(nom, None)
    sys.path.insert(0, dossier)
    try:
        modules = {}
        for nom in noms[3:]:
            sp = importlib.util.spec_from_file_location(nom, os.path.join(dossier, nom + ".py"))
            m = importlib.util.module_from_spec(sp)
            sys.modules[nom] = m
            sp.loader.exec_module(m)
            modules[nom] = m
    finally:
        sys.path.remove(dossier)
    return (modules["CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS"], modules["RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES"],
            modules["GARDER_LES_DOCUMENTS_DES_DROITS"])


def lancer(f, *argv, ici=None):
    """Lance f, la sortie capturée, depuis le dossier `ici` s'il est donné ; rend (code, sortie)."""
    sortie = io.StringIO()
    avant = os.getcwd()
    try:
        if ici:
            os.chdir(ici)
        with contextlib.redirect_stdout(sortie):
            code = f(*argv)
    finally:
        os.chdir(avant)
    return code, sortie.getvalue()


def copie_du_depot():
    """Une copie de ce que la confrontation lit : la table, le registre et les trois dossiers de documents gardés."""
    c = tempfile.mkdtemp()
    os.makedirs(os.path.join(c, "donnees", "sources_bnains"))
    shutil.copy(os.path.join(RACINE, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv"),
                os.path.join(c, "donnees", "sources_bnains"))
    for d in (DOSSIER, os.path.join("temoins", "PAGES_BNAINS_DES_ACTIONS"),
              os.path.join("temoins", "DOCUMENTS_OFFICIELS_ACCOR_EDENRED_2010")):
        shutil.copytree(os.path.join(RACINE, d), os.path.join(c, d))
    return c


def lire_table(c):
    with open(os.path.join(c, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv"), encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        return lecteur.fieldnames, list(lecteur)


def ecrire_table(c, noms, lignes):
    with open(os.path.join(c, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv"), "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=noms, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)


def ligne(prix="", n="", div="", dist="", jour="2008-02-21"):
    return {"valeur": "X", "jour_du_detachement": jour, "prix_souscription": prix, "anciennes_pour_une_nouvelle": n,
            "dividende_non_attache": div, "valeur_distribuee": dist}


def epreuves(C, P, G):
    res = {}
    # C1
    try:
        res["C1"] = (C.forme("Le prix d’émission  est ﬁxé –\u00a0souscrip\u00adtion") ==
                     "le prix d'emission est fixe - souscription")
    except Exception:
        res["C1"] = False
    # C2
    try:
        t = [C.forme("Le Conseil d'Administration, réuni le 9 janvier, a fixé la date d'attribution au 16 janvier 2007 ;"
                     " le prix de souscription est de 47,50 euros ; les prixes")]
        res["C2"] = (C.phrase_dans_le_texte("Le Conseil d’Administration […] a fixé la date", t)
                     and C.phrase_dans_le_texte("Le Conseil d’Administration [...] a fixé la date", t)
                     and not C.phrase_dans_le_texte("a fixé la date […] Le Conseil d’Administration", t)
                     and not C.phrase_dans_le_texte("Le Conseil d’Administration a fixé la date", t)
                     and not C.phrase_dans_le_texte("  ", t)
                     and C.phrase_dans_le_texte("LA DATE D’ATTRIBUTION", t)
                     and C.phrase_dans_le_texte("47,50 euros", t)
                     and not C.phrase_dans_le_texte("7,50 euros", t)
                     and not C.phrase_dans_le_texte("50 euros", t)
                     and not C.phrase_dans_le_texte("est de 47 euros", t)
                     and not C.phrase_dans_le_texte("les prix", t))
    except Exception:
        res["C2"] = False
    # C3
    try:
        m = lambda x: [v for _, v in C.montants(C.forme(x))]
        res["C3"] = (m("Le prix de souscription est de 47,50 euros par action") == [47.5]
                     and m("at the issue price of €59.65 per Offer Share") == [59.65]
                     and m("at a subscription price of (euro)26.50 per share") == [26.5]
                     and m("Dividende proposé : 0,90 EUR par action") == [0.9]
                     and m("10/07/2000 3.60000 07/07/2000 1287.000 € Distribution") == [1287.0]
                     and m("au prix de souscription de 45 euros") == [45.0]
                     and m("pour un montant de 4 005 337 152,50 euros") == [4005337152.5]
                     and m("d'un montant nominal de 476.842.699 euros") == [476842699.0]
                     and m("une somme de 50.000 euros") == []
                     and m("1 action nouvelle pour 4 actions anciennes, en 2008") == []
                     and m("le 30 avril 2021 Euronext Paris") == []
                     and m("euros 2006") == [])
    except Exception:
        res["C3"] = False
    # C4
    try:
        q = lambda x: C.parites(C.forme(x))
        res["C4"] = (q("à raison de 1action nouvelle de 2 euros de nominal chacune pour 10 actions anciennes") == [10.0]
                     and q("à raison de (1) action nouvelle pour 20 actions anciennes") == [20.0]
                     and q("une (1) action nouvelle pour cinq (5) actions anciennes détenues") == [5.0]
                     and q("deux (2) actions Hermès pour quarante et une (41) actions LVMH détenues") == [20.5]
                     and 12.0 in q("12 droits préférentiels de souscription donneront le droit de souscrire à 1 "
                                   "action nouvelle au prix de souscription de 11,90 euros")
                     and q("Six Rights will entitle the holder to purchase one Share") == [6.0]
                     and q("dans un nouveau titre au prix de 16,07 euros pour onze titres anciens détenus") == [11.0]
                     and q("ouverte le 21 février 2008 pour 3 semaines") == []
                     and q("Le 1er janvier 2006 pour 3 ans") == []
                     and q("2 Offer Shares for every 5 existing Ordinary Shares") == [2.5])
    except Exception:
        res["C4"] = False
    # C5
    try:
        J = lambda r, ph: {g: v for g, _, v in C.juger_la_ligne(r, ph)}
        sg = [SG_PRIX, SG_PARITE, SG_JOUR, SG_VALEUR]
        prix = lambda x, ph=sg: J(ligne(prix=x, n="4"), ph)["prix_souscription"]
        res["C5"] = (prix("47.50") == "prouvé" and prix("47.00") == "contredit"
                     and prix("47.504") == "prouvé" and prix("47.51") == "contredit"
                     and prix("77.72") == "contredit" and prix("5.86") == "contredit"
                     and prix("24.47", ["au prix de 19,80 euros avec un cours de bourse de 24,47 euros"]) == "contredit"
                     and prix("19.80", ["au prix de 19,80 euros avec un cours de bourse de 24,47 euros"]) == "prouvé"
                     and J(ligne(prix="47.50", n="4"), sg)["anciennes_pour_une_nouvelle"] == "prouvé"
                     and J(ligne(prix="47.50", n="5"), sg)["anciennes_pour_une_nouvelle"] == "contredit"
                     and J(ligne(prix="47.50", n="4.02"), sg)["anciennes_pour_une_nouvelle"] == "contredit"
                     and J(ligne(prix="47.50", n="4", div="0.90"), sg)["dividende_non_attache"] == "non prouvé"
                     and J(ligne(prix="47.50", n="4", div="0.90"), sg + ["un dividende de 0,90 euros par action"])["dividende_non_attache"] == "prouvé"
                     and J(ligne(prix="47.50", n="4", div="0.95"), sg + ["un dividende de 0,90 euros par action"])["dividende_non_attache"] == "contredit"
                     and J(ligne(prix="0.90", n="4", div="0.90"), ["au prix de souscription de 0,90 euros"])["dividende_non_attache"] == "non prouvé"
                     and J(ligne(prix="47.50", n="4"), sg + ["un dividende de 0,90 euros par action"])["dividende_non_attache"] == "à lire"
                     and "dividende_non_attache" not in J(ligne(prix="47.50", n="4"), sg)
                     and J(ligne(prix="0", n="5"), ["distribution d'actions gratuites à raison d'une (1) action nouvelle pour cinq (5)"])["prix_souscription"] == "prouvé"
                     and prix("0") == "contredit"
                     and J(ligne(prix="0", n="3.5"), ["Une parité simple de 2 actions nouvelles pour 7 actions existantes avec un prix d’exercice des BSA de 14 euros par action nouvelle"])["prix_souscription"] == "contredit"
                     and J(ligne(prix="0", n="4"), [SG_PARITE, "les BSA seront attribués gratuitement aux actionnaires"])["prix_souscription"] == "non prouvé"
                     and J(ligne(n="4"), sg)["prix_souscription"] == "non déclaré"
                     and J(ligne(prix="47.50"), sg)["anciennes_pour_une_nouvelle"] == "non déclaré"
                     and J(ligne(dist="13.00", jour="2010-07-02"), ACCOR)["valeur_distribuee"] == "prouvé"
                     and J(ligne(dist="14.80", jour="2010-07-02"), ACCOR)["valeur_distribuee"] == "contredit"
                     and J(ligne(dist="13.00", jour="2010-07-02"), ACCOR[1:])["valeur_distribuee"] == "non prouvé"
                     and J(ligne(dist="27", jour="2006-05-18"), ["1 action Arkema pour 10 actions Total", "un cours d'ouverture de 27 euros"])["valeur_distribuee"] == "non prouvé"
                     and "prix_souscription" not in J(ligne(dist="13.00", jour="2010-07-02"), ACCOR)
                     and J(ligne(prix="59.65", n="2.5"), ["Based on the closing price of €84.65 per ordinary share"])["prix_souscription"] == "non prouvé"
                     and prix("47.50", sg + ["au prix de souscription de 46,00 euros"]) == "contredit"
                     and prix("1.25", ["Le prix de souscription est de […] 1,25 euros"]) == "non prouvé"
                     and prix("12.75", ["the right to subscribe one ORAN bond at a price of € 12.75 for every 16 warrants held"]) == "prouvé"
                     and prix("47.50", ["au prix de " + "x" * 90 + " 47,50 euros"]) == "non prouvé"
                     and J(ligne(prix="47.50", n="4"), sg + ["3 actifs pour les 15 mois"])["anciennes_pour_une_nouvelle"] == "contredit"
                     and J(ligne(prix="1", dist="13.00", jour="2010-07-02"), ACCOR)["valeur_distribuee"] == "deux natures"
                     and J(ligne(prix="47.50", n="4"), sg)["jour_du_detachement"] == "écrit"
                     and J(ligne(prix="47.50", n="4", jour="2008-02-22"), sg)["jour_du_detachement"] == "non écrit"
                     and J(ligne(prix="47.50", n="4"), [])["jour_du_detachement"] == "non écrit")
    except Exception:
        res["C5"] = False
    # C6
    try:
        d = os.path.join(RACINE, DOSSIER)
        sg_t = C.texte_du_document(os.path.join(d, "SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf"))
        bnp = C.texte_du_document(os.path.join(d, "BNP_PARIBAS_2006_NOTE_D_OPERATION.pdf"))
        doc = C.texte_du_document(os.path.join(d, "PERNOD_RICARD_2007_FCMAN140150_20091021.doc"))
        web = os.path.join(tempfile.mkdtemp(), "page.html")
        open(web, "w", encoding="utf-8").write(
            "<html><script>var x='le cours est de 99 euros';</script><p>Le prix&nbsp;de souscription "
            "est de 10,60&nbsp;euros</p></html>")
        w = C.texte_du_document(web)
        res["C6"] = (C.phrase_dans_le_texte(SG_PRIX, sg_t)
                     and not C.phrase_dans_le_texte("Le prix de souscription est de 47,00 euros par action", sg_t)
                     and C.phrase_dans_le_texte(BNP_COLONNES, bnp)
                     and not C.phrase_dans_le_texte(BNP_COLONNES, bnp[:2])
                     and C.phrase_dans_le_texte("à raison d’une (1) action nouvelle pour cinq (5) actions anciennes", doc)
                     and C.phrase_dans_le_texte("Le prix de souscription est de 10,60 euros", w)
                     and not C.phrase_dans_le_texte("le cours est de 99 euros", w))
    except Exception:
        res["C6"] = False
    # C7 — C7 et C8 lancent la confrontation des dizaines de fois sur des copies : le texte de chaque document n'est
    # extrait qu'une fois par contenu (empreinte), par la fonction du programme — sabotée si elle l'est. C6 l'éprouve.
    extraire, memoire = C.texte_du_document, {}

    def memorise(chemin):
        cle = hashlib.sha256(open(chemin, "rb").read()).hexdigest()
        if cle not in memoire:
            memoire[cle] = extraire(chemin)
        return memoire[cle]
    C.texte_du_document = memorise
    try:
        c = copie_du_depot()
        code0, out0 = lancer(C.main, c)
        noms, lignes = lire_table(c)
        L = lambda v, j: [r for r in lignes if r["valeur"] == v and r["jour_du_detachement"] == j][0]
        essais = []

        def essai(change, attendu, code_attendu=1):
            garde = [dict(r) for r in lignes]
            change()
            ecrire_table(c, noms, lignes)
            code, out = lancer(C.main, c)
            lignes[:] = garde
            ecrire_table(c, noms, lignes)
            essais.append(code == code_attendu and attendu in out)
        sg, bnp, mic = L("SOCIETE GENERALE", "2008-02-21"), L("BNP PARIBAS", "2006-03-07"), L("MICHELIN", "2010-09-30")
        essai(lambda: L("SOCIETE GENERALE", "2008-02-21").__setitem__("prix_souscription", "47.00"),
              "SOCIETE GENERALE 2008-02-21 : prix_souscription déclaré 47.00, CONTREDIT")
        essai(lambda: L("MICHELIN", "2010-09-30").update({"prix_souscription": "46", C.COLONNE: " ¦ ".join(
              [e for e in mic[C.COLONNE].split(" ¦ ") if "45 euros" not in e] +
              ["MICHELIN_2010_RESUME_PROSPECTUS_2010-09-28.pdf :: au prix de souscription de 46 euros"])}),
              "MICHELIN 2010-09-30 : prix_souscription 46 NON PROUVÉ")
        essai(lambda: L("BNP PARIBAS", "2006-03-07").__setitem__(C.COLONNE, bnp[C.COLONNE] + C.ENTRE_LES_PHRASES +
              "BNP_PARIBAS_2006_BALO_2006-03-06.pdf :: " + BNP_COLONNES),
              "BNP PARIBAS 2006-03-07 : phrase ABSENTE de BNP_PARIBAS_2006_BALO")
        essai(lambda: L("BNP PARIBAS", "2006-03-07").__setitem__(C.COLONNE, bnp[C.COLONNE] + C.ENTRE_LES_PHRASES +
              "PAS_GARDE.pdf :: une phrase"), "NON GARDÉ (PAS_GARDE.pdf)")
        essai(lambda: L("MICHELIN", "2010-09-30").update({"prix_souscription": "47.50", C.COLONNE: mic[C.COLONNE] +
              " ¦ SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf :: " + SG_PRIX,
              "citation": mic["citation"] + " (voir aussi SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf)"}), "N'INVOQUE PAS")
        essai(lambda: L("MICHELIN", "2010-09-30").__setitem__(C.COLONNE, " ¦ ".join(
              e for e in mic[C.COLONNE].split(" ¦ ") if "45 euros" not in e)),
              "MICHELIN 2010-09-30 : prix_souscription 45 NON PROUVÉ, et sans raison")
        essai(lambda: L("TOTALENERGIES", "2006-05-18").__setitem__("valeur_distribuee", "27"),
              "TOTALENERGIES 2006-05-18 : valeur_distribuee 27 NON PROUVÉ, et sa raison ne commence pas")
        essai(lambda: L("DANONE", "2009-06-01").__setitem__(C.COLONNE_RAISONS, "prix_souscription : 24,73 — essai"),
              "DANONE 2009-06-01 : raison écrite pour « prix_souscription »")
        essai(lambda: L("SCHNEIDER ELECTRIC", "2007-03-12").__setitem__("dividende_non_attache", ""),
              "SCHNEIDER ELECTRIC 2007-03-12 : une phrase écrit un dividende, la ligne n'en déclare AUCUN")
        essai(lambda: L("SOCIETE GENERALE", "2008-02-21").__setitem__("prix_souscription", ""),
              "SOCIETE GENERALE 2008-02-21 : prix_souscription NON DÉCLARÉ")
        doc = os.path.join(c, DOSSIER, "DANONE_2009_COMMUNIQUE_2009-05-29.pdf")
        brut = open(doc, "rb").read()
        open(doc, "wb").write(brut[:-1] + bytes([brut[-1] ^ 1]))   # un octet changé, la taille gardée
        code4, out4 = lancer(C.main, c)
        open(doc, "wb").write(brut)
        registre = os.path.join(c, DOSSIER, "DOCUMENTS.csv")
        texte = open(registre, encoding="utf-8").read()
        open(registre, "w", encoding="utf-8").write(texte.replace(",24219,", ",24218,", 1))
        code4b, out4b = lancer(C.main, c)
        open(registre, "w", encoding="utf-8").write(texte.replace("fichier,adresse,octets,sha256", "fichier,adresse,sha256,octets", 1))
        code4c, _ = lancer(C.main, c)
        open(registre, "w", encoding="utf-8").write(texte)
        os.remove(doc)
        code5, out5 = lancer(C.main, c)
        c2 = copie_du_depot()
        ecrire_table(c2, noms[:-1], lignes)
        code6, _ = lancer(C.main, c2)
        chemin = os.environ.get("PATH", "")
        os.environ["PATH"] = ""
        C.texte_du_document = extraire            # ici l'extraction elle-même doit échouer
        try:
            code7, out7 = lancer(C.main, copie_du_depot())
        finally:
            os.environ["PATH"] = chemin
            C.texte_du_document = memorise
        res["C7"] = (code0 == 0 and RESUME in out0 and len(essais) == 10 and all(essais)
                     and code4 == 1 and "MODIFIÉ" in out4 and "DANONE_2009_COMMUNIQUE" in out4
                     and code4b == 1 and "MODIFIÉ" in out4b and code4c == 2
                     and code5 == 2 and code6 == 2 and code7 == 2 and "pdftotext absent" in out7)
    except Exception:
        res["C7"] = False
    # C8
    try:
        c = copie_du_depot()
        noms, lignes = lire_table(c)
        du_depot = {(r["valeur"], r["jour_du_detachement"]): C.phrases_de_la_ligne(r) for r in lignes}
        ecrire_table(c, noms[:-2], lignes)
        code1, out1 = lancer(P.main, ici=c)
        noms1, lignes1 = lire_table(c)
        inclus = all(set(C.phrases_de_la_ligne(r)) <= set(du_depot[(r["valeur"], r["jour_du_detachement"])])
                     for r in lignes1)
        nombre = sum(len(C.phrases_de_la_ligne(r)) for r in lignes1)
        nouvelles = (C.COLONNE, C.COLONNE_RAISONS)
        reste = all({k: v for k, v in r.items() if k not in nouvelles} == {k: v for k, v in s.items() if k not in nouvelles}
                    for r, s in zip(lignes1, lignes)) and all(r[C.COLONNE_RAISONS] == "" for r in lignes1)
        chemin = os.path.join(c, "donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv")
        avant = open(chemin, "rb").read()
        code2, _ = lancer(P.main, ici=c)
        pareil = open(chemin, "rb").read() == avant
        with open(os.path.join(c, DOSSIER, "VINCI_2006_BALO_2006-03-29.pdf"), "ab") as f:
            f.write(b" ")
        code3, out3 = lancer(P.main, ici=c)
        intacte = open(chemin, "rb").read() == avant
        res["C8"] = (code1 == 0 and noms1 == noms and inclus and reste and nombre == RELEVEES and code2 == 0 and pareil
                     and code3 == 2 and intacte and "RIEN N'EST ÉCRIT" in out3)
    except Exception:
        res["C8"] = False
    C.texte_du_document = extraire
    # C9
    try:
        a = G.adresses_de_la_ligne({"source": "https://www.edenred.com/x/doc_0.pdf (page 274 du PDF) ; copies au dépôt : "
                                              "temoins/X/", "citation": "(https://exemple.fr/a.html, relu) ; https://exemple.fr/b.pdf."})
        c = copie_du_depot()
        accor = open(os.path.join(c, "temoins", "DOCUMENTS_OFFICIELS_ACCOR_EDENRED_2010",
                                  "ACCOR_COMMUNIQUE_2010-06-29.pdf"), "rb").read()
        neuf = b"%PDF-1.4\n" + b"contenu neuf " * 400
        reponses = {"https://refus.fr/a.pdf": None, "https://court.fr/b.pdf": b"%PDF petit",
                    "https://double.fr/accor.pdf": accor, "https://neuf.fr/doc/communique": neuf}

        class Reponse:
            def __init__(self, contenu): self.contenu = contenu
            def __enter__(self): return self
            def __exit__(self, *x): return False
            def read(self): return self.contenu

        def ouvrir(demande, timeout=None):
            u = demande.full_url
            if reponses.get(u) is None:
                raise urllib.error.HTTPError(u, 403, "Forbidden", {}, None)
            return Reponse(reponses[u])
        registre = os.path.join(c, DOSSIER, "DOCUMENTS.csv")
        avant = open(registre, encoding="utf-8").read()
        deja = avant.splitlines()[1].split(",")[1]
        ecrire_table(c, C.DETACHEMENTS_OFFICIELS, [{
            "valeur": "VALEUR ESSAI", "jour_du_detachement": "2001-02-03", "citation": "",
            "source": " ; ".join(list(reponses) + [deja, "https://www.bnains.org/archives/action.php?codeISIN=FR0000120404"])}])
        garde_ouvrir = G.urllib.request.urlopen
        G.urllib.request.urlopen = ouvrir
        try:
            code, out = lancer(G.main, ici=c)
        finally:
            G.urllib.request.urlopen = garde_ouvrir
        apres = open(registre, encoding="utf-8").read()
        ajout = list(csv.reader(io.StringIO(apres[len(avant):])))
        res["C9"] = (a == ["https://www.edenred.com/x/doc_0.pdf", "https://exemple.fr/a.html", "https://exemple.fr/b.pdf"]
                     and code == 0 and apres.startswith(avant) and len(ajout) == 3
                     and ajout[0][0] == "../DOCUMENTS_OFFICIELS_ACCOR_EDENRED_2010/ACCOR_COMMUNIQUE_2010-06-29.pdf"
                     and ajout[1][0] == "VALEUR_ESSAI_2001_communique.pdf"
                     and open(os.path.join(c, DOSSIER, "VALEUR_ESSAI_2001_communique.pdf"), "rb").read() == neuf
                     and ajout[2][0] == "../PAGES_BNAINS_DES_ACTIONS/FR0000120404.html"
                     and "NON GARDÉ (HTTPError" in out and "NON GARDÉ (contenu de 10 octets)" in out)
    except Exception:
        res["C9"] = False
    return res


def main():
    res = epreuves(*charger())
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
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}", flush=True)
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
