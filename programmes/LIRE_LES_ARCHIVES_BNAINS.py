#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIRE_LES_ARCHIVES_BNAINS.py — Dim 04-10-2026 (Paris) — PROPOSÉ, non validé (A-539, action ①).
Rôle : lire les archives de cours de la Bourse de Paris publiées par bnains.org, de 2000 à
février 2017, et n'en garder que les valeurs du référentiel, dans un seul fichier.
Simulation uniquement : ce programme lit des fichiers publics, il ne passe rien.

① RÔLE — Fabriquer donnees/sources_bnains/bnains_cac40.csv : pour chaque valeur du
  référentiel, et pour Suez (témoin du retrait d'Engie avant juillet 2005), chaque séance
  de 2000 au 28-02-2017 telle que bnains.org l'a archivée — ouverture, plus haut, plus bas,
  clôture, volume, COURS BRUTS non ajustés. C'est la seconde source qui sert à réparer et à
  contrôler le fichier Yahoo des 26 ans (A-539).
② CONTEXTE D'APPEL — À la main, une fois, puis chaque fois que la liste des valeurs change :
  python3 programmes/LIRE_LES_ARCHIVES_BNAINS.py <racine> <dossier des archives> [--telecharger].
  Aucun circuit ne le lance. Ses épreuves :
  tests/EPREUVES_DES_ARCHIVES_BNAINS_Dim_04-10-2026.py.
③ ENTRÉE — Deux arguments : la racine du dépôt, et le dossier où sont (ou seront) rangées
  les archives telles que bnains.org les publie (`ARCHIVES`). Option --telecharger :
  télécharger d'abord celles qui manquent dans ce dossier.
④ CONDITIONS D'ENTRÉE — Un seul fichier donnees/REFERENTIEL_VALEURS_*.csv sous la racine,
  avec les colonnes nom_usuel, isin et source_isin. Les vingt archives de `ARCHIVES` dans le
  dossier, ou l'accès réseau à www.bnains.org avec --telecharger.
⑤ SORTIE — UNE valeur : le code de sortie. 0 = les quatre fichiers écrits · 1 = au moins une
  archive manque (nommée à l'écran), ou une archive est incomplète (`LACUNE`), et RIEN n'est
  écrit : un extrait partiel aurait l'air complet · 2 = rien n'a pu être fait (arguments, référentiel, archive illisible, code
  attribué à deux valeurs, ou toute erreur imprévue). Plus un résumé à l'écran.
⑥ TRAITEMENT — ① avec --telecharger, télécharger les archives absentes (`telecharger`) ·
  ② vérifier qu'aucune ne manque · ③ lire la table de conversion SICOVAM → ISIN
  (`lire_conversion`) · ④ fixer les codes de chaque valeur (`codes_des_valeurs`) · ⑤ lire
  toutes les séances et les droits de souscription (`lire_archives`) · ⑤bis refuser une lacune
  (`lacunes`) · ⑥ écrire l'extrait, l'inventaire des archives, les conflits et les droits
  (`ecrire`) · ⑦ afficher le résumé et sortir.
⑦ UNITÉ — Des COURS en EUROS tels que cotés ce jour-là (non ajustés des divisions ni des
  dividendes), des VOLUMES en NOMBRE DE TITRES, des DATES de séance (calendrier de Paris).
⑧ POURQUOI — Le 04-10-2026, Cowork a montré que le fichier Yahoo des 26 ans est faux par
  endroits : AXA 2001-2007 en marches d'escalier (735 barres plates), EssilorLuxottica
  2000-2001 décalé, Engie avant juillet 2005 portant les cours de Suez, 222 séances
  manquantes. Une seconde source est le seul moyen de réparer ET de contrôler ; bnains.org
  est la seule trouvée qui remonte à 2000 gratuitement (Euronext : 2 ans, Boursorama : 3).
  Ce programme réécrit le brouillon de Cowork (etudes/brouillons_cowork/lire_bnains.py),
  qui écrivait toutes les actions de Paris (près de 4,8 millions de lignes) sans choisir de
  code : ici, chaque valeur reçoit ses codes une fois, et rien d'autre n'est gardé.
⑨ CE QUI CLOCHE — Le droit d'usage des archives bnains.org n'est pas établi (A-516) : la
  page des archives ne dit rien des conditions de réutilisation, lue le 04-10-2026. · Le
  site refuse (403) un téléchargement sans en-tête de navigateur : `UA` en imite un. · La
  table de conversion date du 23-06-2003 : une valeur entrée à Paris après cette date n'y
  est pas, et n'a donc pas de code SICOVAM — sans effet, puisque bnains n'emploie les codes
  SICOVAM que jusqu'au 27-06-2003, puis une dernière fois sur 33 lignes du 16-11-2004
  (relecture indépendante du 04-10-2026, recompté dans l'extrait le même jour). · L'ancien ISIN d'Eurofins Scientific (`ANCIENS_ISIN`) n'est écrit
  nulle part dans le référentiel : il est porté ici en attendant qu'il y entre. → BACKLOG.
⑩ EFFET — Écrit donnees/sources_bnains/bnains_cac40.csv, ARCHIVES_BNAINS.csv,
  CONFLITS_BNAINS.csv et DROITS_BNAINS.csv, en les remplaçant entièrement. Avec --telecharger, écrit les archives
  absentes dans le dossier donné. Ne touche à aucun autre fichier — jamais au fichier
  maître des cours.
⑪ TERMINAISON — Toujours : chaque téléchargement est borné à 300 secondes et ne se répète
  pas ; la lecture parcourt un nombre fini d'archives. Aucun de mes appels ne peut boucler.
"""
import csv, datetime, glob, hashlib, io, os, re, sys, urllib.request, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import COURS_BNAINS, DROITS_BNAINS   # les champs, déclarés une fois (R-708)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
ADRESSE = "https://www.bnains.org/archives/"
# Les archives lues, telles que la page https://www.bnains.org/archives/archives.php les liste le
# 04-10-2026 : une par année de 2000 à 2016, une par mois pour janvier et février 2017 (dernier mois
# publié), et la table de conversion des codes d'Euronext du 23-06-2003.
ARCHIVES = [f"cours/france/{a}.ZIP" for a in range(2000, 2017)] + \
           ["cours/france/201701.ZIP", "cours/france/201702.ZIP", "conv_isin.zip"]
CONVERSION = "conv_isin.zip"
DOSSIER = os.path.join("donnees", "sources_bnains")
SORTIE = os.path.join(DOSSIER, "bnains_cac40.csv")
INVENTAIRE = os.path.join(DOSSIER, "ARCHIVES_BNAINS.csv")
CONFLITS = os.path.join(DOSSIER, "CONFLITS_BNAINS.csv")
DROITS = os.path.join(DOSSIER, "DROITS_BNAINS.csv")
# Un ISIN ancien absent du référentiel : Eurofins Scientific a changé d'ISIN en 2020 (division par
# dix) ; bnains, qui s'arrête en 2017, ne connaît que l'ancien. Relevé par Cowork le 04-10-2026
# (etudes/brouillons_cowork/recouper.py) ; la table de conversion le nomme « EUROFINS SCIENT. ».
ANCIENS_ISIN = {"EUROFINS SCIENTIFIC": ["FR0000038259"]}
# Une société qui n'est pas au référentiel, gardée comme TÉMOIN : Suez, dont Yahoo a mis les cours
# sous le nom d'Engie avant le 08-07-2005 (relevé de Cowork du 04-10-2026, mesure 5). Le retrait
# d'Engie se contrôle sur elle.
TEMOINS = {"SUEZ": ["FR0000120529"]}
# Plus de 3 jours ouvrés sans séance entre deux séances lues : une archive est incomplète. Mesuré le
# 04-10-2026 sur les vraies archives : 2 jours ouvrés au plus (Noël, Pâques).
LACUNE = 3


def telecharger(dossier, ouvrir=urllib.request.urlopen):
    """Télécharge, dans `dossier`, les archives de `ARCHIVES` qui n'y sont pas encore.

    ① RÔLE — Aller chercher chez bnains.org les archives absentes, sans retoucher celles déjà là.
    ② CONTEXTE D'APPEL — `main`, avec l'option --telecharger, avant toute lecture.
    ③ ENTRÉE — `dossier` : où ranger les archives · `ouvrir` : la fonction qui ouvre une adresse
      (urllib.request.urlopen ; les épreuves en passent une fausse).
    ④ CONDITIONS D'ENTRÉE — `dossier` existe ou peut être créé ; l'accès réseau à bnains.org.
    ⑤ SORTIE — UNE valeur : la liste des archives qui n'ont PAS pu être téléchargées, chacune
      avec sa raison ; vide si tout est là.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque archive absente : ① la demander avec l'en-tête de navigateur `UA`
      · ② l'écrire sous un nom provisoire, puis la renommer : une archive coupée en route ne
      prend jamais le vrai nom · ③ noter l'échec sans s'arrêter.
    ⑦ UNITÉ — Des NOMS d'archives.
    ⑧ POURQUOI — Le site rend 403 sans en-tête de navigateur (mesuré le 04-10-2026, 15h55).
    ⑨ CE QUI CLOCHE — Une archive déjà présente n'est pas comparée à celle du site : si le site
      la republie corrigée, elle n'est pas reprise. Son empreinte est gardée dans l'inventaire.
    ⑩ EFFET — Écrit les archives absentes dans `dossier`. Réseau.
    ⑪ TERMINAISON — Chaque demande est bornée à 300 secondes, sans nouvel essai.
      [sort: non]
    """
    os.makedirs(dossier, exist_ok=True)
    echecs = []
    for nom in ARCHIVES:
        cible = os.path.join(dossier, os.path.basename(nom))
        if os.path.exists(cible):
            continue
        try:
            req = urllib.request.Request(ADRESSE + nom, headers={"User-Agent": UA})
            with ouvrir(req, timeout=300) as r:
                octets = r.read()
            open(cible + ".partiel", "wb").write(octets)
            os.replace(cible + ".partiel", cible)
            print(f"  téléchargée : {nom} ({len(octets)} octets)")
        except Exception as e:
            echecs.append(f"{nom} : {type(e).__name__} {e}")
    return echecs


def lire_conversion(chemin):
    """Lit la table de conversion d'Euronext et rend, pour chaque ISIN, ses codes SICOVAM.

    ① RÔLE — Donner les codes SICOVAM sous lesquels bnains range une valeur avant 2003.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `chemin` : l'archive conv_isin.zip, qui contient conv_isin.csv.
    ④ CONDITIONS D'ENTRÉE — Une archive lisible dont le premier fichier .csv a les colonnes
      SICOVAM et ISIN, séparées par des points-virgules, en latin-1.
    ⑤ SORTIE — UNE valeur : un dictionnaire ISIN → ensemble de codes SICOVAM, écrits SANS les
      zéros de tête (bnains écrit « 12062 », la table « 012062 »). Lève ValueError sur une ligne
      à qui manque une colonne ou dont le code SICOVAM n'est pas un nombre : aucune n'existe dans la table du
      23-06-2003 (9 701 lignes, mesuré le 04-10-2026), une telle ligne dirait une autre table.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir le .csv de l'archive · ② pour chaque ligne, ajouter le code SICOVAM,
      lu comme un nombre, à son ISIN.
    ⑦ UNITÉ — Des CODES.
    ⑧ POURQUOI — Un même ISIN porte parfois plusieurs codes SICOVAM dans la table (AXA : 012062
      et 405772) ; mesuré le 04-10-2026, les codes 405xxx n'apparaissent dans aucune archive de
      2000 à 2003 : les garder tous ne coûte rien et ne suppose rien.
    ⑨ CE QUI CLOCHE — La table date du 23-06-2003 (⑨ du programme).
    ⑩ EFFET — Lit l'archive. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève si l'archive est illisible.
      [sort: non]
    """
    with zipfile.ZipFile(chemin) as z:
        nom = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        texte = z.read(nom).decode("latin-1")
    table = {}
    for n, r in enumerate(csv.DictReader(io.StringIO(texte), delimiter=";"), 2):
        try:
            table.setdefault(r["ISIN"].strip(), set()).add(str(int(r["SICOVAM"])))
        except (KeyError, AttributeError, TypeError, ValueError):
            raise ValueError(f"table de conversion, ligne {n} illisible : {r}")
    return table


def codes_des_valeurs(racine, conversion):
    """Fixe, pour chaque valeur du référentiel et chaque témoin, les codes qui la désignent chez bnains.

    ① RÔLE — Dire une fois pour toutes quel code est quelle valeur, avant de lire une seule séance.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : la racine du dépôt · `conversion` : la table de `lire_conversion`.
    ④ CONDITIONS D'ENTRÉE — Un seul référentiel donnees/REFERENTIEL_VALEURS_*.csv, avec les
      colonnes nom_usuel, isin, source_isin.
    ⑤ SORTIE — UNE valeur : un dictionnaire code → valeur. Lève ValueError si le référentiel
      manque ou manque de colonnes, ou si un code désignerait deux valeurs.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque valeur : ① son ISIN du référentiel · ② les ISIN que sa colonne
      source_isin dit remplacés (« remplace FR… ») · ③ ceux de `ANCIENS_ISIN` · ④ les codes
      SICOVAM de chacun · puis les témoins (`TEMOINS`) de la même façon · ⑤ refuser un code
      déjà pris par une autre valeur.
    ⑦ UNITÉ — Des CODES (ISIN ou SICOVAM).
    ⑧ POURQUOI — Le brouillon de Cowork dérivait aussi un code SICOVAM des chiffres de l'ISIN ;
      ce n'est pas une règle écrite, et la table d'Euronext donne les mêmes codes (vérifié le
      04-10-2026 sur les 30 ISIN en FR0000 : identiques). Les anciens ISIN de Dassault
      Systèmes, Michelin et Unibail sont LUS dans le référentiel, où A-531 les a écrits le
      03-10-2026 : ils ne sont pas recopiés ici (R-708).
    ⑨ CE QUI CLOCHE — Un ISIN remplacé n'est trouvé que s'il est écrit « remplace » suivi d'un
      espace et de l'ISIN, comme dans les trois lignes de A-531.
    ⑩ EFFET — Lit le référentiel. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    refs = glob.glob(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS_*.csv"))
    if len(refs) != 1:
        raise ValueError(f"{len(refs)} référentiel(s) trouvé(s) au lieu d'un")
    lignes = list(csv.DictReader(open(refs[0], encoding="utf-8-sig")))
    if not lignes or not {"nom_usuel", "isin", "source_isin"} <= set(lignes[0]):
        raise ValueError("référentiel vide ou sans les colonnes nom_usuel, isin, source_isin")
    isins = {}
    for r in lignes:
        v = r["nom_usuel"].strip()
        isins[v] = [r["isin"].strip()] + re.findall(r"remplace ([A-Z]{2}[0-9A-Z]{10})", r["source_isin"]) \
            + ANCIENS_ISIN.get(v, [])
    isins.update(TEMOINS)
    codes = {}
    for v, liste in isins.items():
        for c in [i for i in liste if i] + sorted({s for i in liste for s in conversion.get(i, ())}):
            if codes.get(c, v) != v:
                raise ValueError(f"le code {c} désignerait deux valeurs : {codes[c]} et {v}")
            codes[c] = v
    return codes


def fichiers_du_jour(z):
    """Parcourt une archive et ses archives imbriquées ; rend chaque fichier de séance.

    ① RÔLE — Trouver les fichiers « AAAAMMJJ.txt », à toute profondeur.
    ② CONTEXTE D'APPEL — `lire_archives`, une fois par archive ; elle-même, par archive imbriquée.
    ③ ENTRÉE — `z` : une archive ouverte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Une suite de paires (date « AAAA-MM-JJ », octets du fichier), rendues une à une ;
      le compte des autres fichiers, ignorés, est rangé dans l'attribut `ignores` de la fonction.
      [rend: générateur]
    ⑥ TRAITEMENT — ① pour chaque nom : une archive imbriquée est ouverte et parcourue · ② un nom
      en AAAAMMJJ.txt est lu et rendu · ③ tout autre nom est compté, JAMAIS lu.
    ⑦ UNITÉ — Des DATES de séance.
    ⑧ POURQUOI — Ne jamais lire un fichier ignoré : le fichier « infos et mises à jour.htm » des
      archives de 2009 à 2013 porte un nom écrit de deux façons dans l'archive, et sa lecture lève
      (mesuré le 04-10-2026 : BadZipFile). Les années 2000 à 2003 et les deux mois de 2017 sont
      plates ; 2004 à 2016 contiennent une archive par mois (relevé le 04-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit l'archive. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; l'imbrication est finie.
      [sort: non]
    """
    for n in z.namelist():
        if n.upper().endswith(".ZIP"):
            with zipfile.ZipFile(io.BytesIO(z.read(n))) as z2:
                yield from fichiers_du_jour(z2)
        elif re.fullmatch(r"(?:.*/)?\d{8}\.txt", n, re.I):
            d = re.search(r"(\d{8})\.txt$", n, re.I).group(1)
            yield f"{d[:4]}-{d[4:6]}-{d[6:]}", z.read(n)
        else:
            fichiers_du_jour.ignores += 1


fichiers_du_jour.ignores = 0


def nombre(texte):
    """Lit un nombre de bnains : point ou virgule décimale ; rend son écriture avec un point.

    ① RÔLE — Rendre un nombre écrit « 19,00 » (2000-2001) ou « 19.00 » sous une forme unique.
    ② CONTEXTE D'APPEL — `lire_archives`, cinq fois par ligne gardée.
    ③ ENTRÉE — `texte` : le champ tel qu'il est écrit.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte avec un point décimal. Lève ValueError si ce n'est pas un
      nombre, s'il porte à la fois point et virgule (séparateur de milliers), ou s'il est négatif.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser point et virgule ensemble · ② remplacer la virgule · ③ vérifier que
      c'est un nombre positif ou nul.
    ⑦ UNITÉ — Des EUROS ou un NOMBRE DE TITRES, selon le champ.
    ⑧ POURQUOI — Mesuré le 04-10-2026 : virgule décimale sur 111 830 lignes en 2000 et 87 663 en
      2001, point ailleurs. Garder le texte, et non un nombre à virgule flottante, évite d'écrire
      « 17.079999 » pour 17.08. Le négatif est refusé parce que bnains écrit « -1.00 » au plus haut
      et au plus bas d'une séance SANS ÉCHANGE (Eurofins Scientific, 13 et 14-03-2000, volume 0,
      lu dans l'archive le 04-10-2026) : ce n'est pas une barre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    t = texte.strip()
    if "," in t and "." in t:
        raise ValueError(f"« {texte} » : point et virgule ensemble")
    t = t.replace(",", ".")
    if float(t) < 0:
        raise ValueError(f"« {texte} » : négatif")
    return t


def lire_archives(dossier, codes):
    """Lit toutes les séances des archives et garde celles des codes voulus.

    ① RÔLE — Construire l'extrait, et dire ce qui a été écarté et pourquoi.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `dossier` : où sont les archives · `codes` : le dictionnaire code → valeur.
    ④ CONDITIONS D'ENTRÉE — Toutes les archives de cours de `ARCHIVES` présentes et lisibles.
    ⑤ SORTIE — CINQ valeurs : ① les lignes gardées, une liste de listes dans l'ordre de
      `COURS_BNAINS` · ② l'inventaire, une ligne par archive (nom, octets, empreinte, lignes lues,
      lignes gardées) · ③ les conflits, une ligne par (valeur, date) écartée · ④ les droits de
      souscription, une ligne par droit dans l'ordre de `DROITS_BNAINS` · ⑤ un dictionnaire de
      comptes (lignes lues par année, lignes mal formées, doublons identiques, fichiers ignorés).
      [rend: 5]
    ⑥ TRAITEMENT — Pour chaque archive, chaque fichier de séance, chaque ligne : ① compter la
      ligne · ② une ligne à moins de sept champs est mal formée · ③ un code non voulu est passé ·
      ④ lire les cinq nombres (`nombre`) ; une ligne illisible est mal formée · ⑤ ranger la ligne
      sous (valeur, date). Puis : ⑥ une (valeur, date) vue plusieurs fois avec les MÊMES cinq
      nombres garde une ligne (doublon identique) ; avec des nombres DIFFÉRENTS, aucune n'est
      gardée et toutes vont aux conflits. ⑦ Une ligne d'un code non voulu dont le libellé finit
      par « DS » ou « DPS », et dont le reste du libellé est le DÉBUT du libellé d'UNE SEULE ligne
      gardée le même jour, est un droit de souscription de cette valeur (« AXA DS » pour « AXA »,
      « VEOLIA DS » pour « VEOLIA ENVIRONNEMENT », « SOCIETE GENER DS » pour « SOCIETE GENERALE ») :
      ses jours de cotation sont notés, et sa clôture du premier jour, qui borne la marche permise
      le jour du détachement (contrôle K15 de programmes/CONTROLER_L_HISTORIQUE_LONG.py). Un début
      de libellé commun à deux valeurs gardées ne rattache le droit à aucune.
    ⑦ UNITÉ — Des LIGNES, des euros, des titres.
    ⑧ POURQUOI — Mesuré le 04-10-2026 : 28 907 doublons en 2000 (tous identiques), des doublons
      DIFFÉRENTS en 2001 et de 2004 à 2013 (2 557), et la séance du 30-08-2006 publiée dans deux
      fichiers. Choisir l'une de deux versions différentes serait deviner : le conflit est écarté
      et dit. Le compte des lignes lues par année reproduit, au chiffre près, celui du brouillon
      de Cowork (calibrage, ⑨bis des préférences de Jean-Luc).
    ⑨ CE QUI CLOCHE — Une ligne mal formée d'un code voulu est perdue sans être nommée : seul son
      nombre est rendu. Un droit dont le libellé ne commence pas comme celui de l'action n'est pas
      vu ; la règle du début de libellé trouve neuf droits sur 2000-2017 (mesuré le 07-10-2026 sur
      toutes les lignes « DS » et « DPS » des archives) et n'en rattache aucun autre : « CARREFOUR
      PROP DS », « GROUPE ARES DS », « EURODISNEY DPS » restent seuls. Aucun droit pour BNP Paribas
      (2006). · Le premier jour de cotation chez bnains n'est PAS toujours le jour du détachement :
      bnains montre les droits un jour de bourse après l'ouverture officielle de la souscription
      pour AXA, Danone, Michelin, Pernod Ricard, Veolia, Crédit Agricole et Société Générale 2009,
      mais le jour même pour Suez 2005 (communiqués lus le 07-10-2026). Le jour du détachement
      vient donc d'un fichier de dates officielles (`lire_detachements` du contrôle), pas d'ici. Les lignes sont coupées au seul saut de ligne : des lignes de 2001 portent,
      dans leur libellé, des octets de contrôle (0x1C) que `splitlines` prend pour des fins de ligne
      (NATEXIS PWF EURO S, 15-03-2001) ; coupées ainsi, elles donnaient 610 morceaux de moins de sept
      champs, mesuré le 04-10-2026. Coupées au saut de ligne, elles sont lues entières, et le compte
      des lignes lues par année ne change pas.
    ⑩ EFFET — Lit les archives. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève si une archive est illisible.
      [sort: non]
    """
    vues, inventaire, droits = {}, [], {}
    comptes = {"par_annee": {}, "mal_formees": 0, "doublons_identiques": 0}
    fichiers_du_jour.ignores = 0
    for nom in ARCHIVES:
        if nom == CONVERSION:
            continue
        chemin = os.path.join(dossier, os.path.basename(nom))
        octets = open(chemin, "rb").read()
        lues = gardees = 0
        with zipfile.ZipFile(io.BytesIO(octets)) as z:
            for date, contenu in fichiers_du_jour(z):
                libelles_du_jour, candidats = {}, []
                for ligne in contenu.decode("latin-1").split("\n"):
                    if not ligne.strip():
                        continue
                    p = ligne.rstrip("\r").split("\t")
                    if len(p) < 7:
                        comptes["mal_formees"] += 1
                        continue
                    lues += 1
                    comptes["par_annee"][date[:4]] = comptes["par_annee"].get(date[:4], 0) + 1
                    code = p[0].strip()
                    if code not in codes:
                        droit = re.fullmatch(r"(.+?)\s+(DS|DPS)", p[1].strip())
                        if droit:
                            try:
                                candidats.append((code, p[1].strip(), droit.group(1), nombre(p[5])))
                            except ValueError:
                                comptes["mal_formees"] += 1
                        continue
                    try:
                        chiffres = tuple(nombre(x) for x in p[2:7])
                    except ValueError:
                        comptes["mal_formees"] += 1
                        continue
                    gardees += 1
                    libelles_du_jour[p[1].strip()] = codes[code]
                    vues.setdefault((codes[code], date), []).append((code, p[1].strip(), chiffres))
                for code, libelle, prefixe, cloture in candidats:
                    valeurs = {v for lib, v in libelles_du_jour.items() if lib.startswith(prefixe)}
                    if len(valeurs) == 1:
                        droits.setdefault((valeurs.pop(), code, libelle), []).append((date, cloture))
        inventaire.append([os.path.basename(nom), len(octets), hashlib.sha256(octets).hexdigest(), lues, gardees])
    lignes, conflits = [], []
    for (valeur, date), versions in sorted(vues.items()):
        if len({v[2] for v in versions}) > 1:
            for code, libelle, ch in versions:
                conflits.append([valeur, date, code, libelle, *ch])
            continue
        comptes["doublons_identiques"] += len(versions) - 1
        code, libelle, ch = versions[0]
        lignes.append([valeur, date, code, libelle, *ch])
    comptes["fichiers_ignores"] = fichiers_du_jour.ignores
    lignes_droits = [[v, c, l, min(d)[0], max(d)[0], len({x[0] for x in d}), min(d)[1]]
                     for (v, c, l), d in sorted(droits.items())]
    return lignes, inventaire, conflits, lignes_droits, comptes


def lacunes(lignes):
    """Rend les trous de plus de `LACUNE` jours ouvrés entre deux séances lues.

    ① RÔLE — Voir une archive présente mais incomplète.
    ② CONTEXTE D'APPEL — `main`, une fois, après la lecture.
    ③ ENTRÉE — `lignes` : les lignes gardées, la date en deuxième position.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des trous, « du AAAA-MM-JJ au AAAA-MM-JJ : N jours ouvrés ».
      [rend: 1]
    ⑥ TRAITEMENT — ① les dates lues, triées · ② entre deux dates qui se suivent, compter les jours
      du lundi au vendredi · ③ garder les écarts de plus de `LACUNE`.
    ⑦ UNITÉ — Des JOURS OUVRÉS (lundi à vendredi, fériés compris).
    ⑧ POURQUOI — Relecture indépendante du 04-10-2026 : une archive de 2005 privée de mai et de
      juin passait la lecture en 0, puis la réparation retirait toutes les lignes d'AXA de ces deux
      mois, et le contrôle passait aussi.
    ⑨ CE QUI CLOCHE — Un seul jour manquant ne se voit pas : bnains n'a pas le fichier de 21
      séances isolées (relevé le 04-10-2026), c'est normal.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    dates = sorted({datetime.date.fromisoformat(l[1]) for l in lignes})
    trous = []
    for a, b in zip(dates, dates[1:]):
        n = sum(1 for k in range(1, (b - a).days) if (a + datetime.timedelta(days=k)).weekday() < 5)
        if n > LACUNE:
            trous.append(f"du {a} au {b} : {n} jours ouvrés")
    return trous


def ecrire(racine, lignes, inventaire, conflits, droits):
    """Écrit l'extrait, l'inventaire, les conflits et les droits sous donnees/sources_bnains/.

    ① RÔLE — Poser les quatre fichiers, en entier, d'un seul geste par fichier.
    ② CONTEXTE D'APPEL — `main`, une fois, quand rien ne manque.
    ③ ENTRÉE — `racine` : la racine du dépôt · `lignes`, `inventaire`, `conflits`, `droits` : les
      quatre listes rendues par `lire_archives`.
    ④ CONDITIONS D'ENTRÉE — La racine est accessible en écriture.
    ⑤ SORTIE — Aucune valeur.
      [rend: rien]
    ⑥ TRAITEMENT — Pour chaque fichier : ① écrire sous un nom provisoire · ② renommer.
    ⑦ UNITÉ — Des LIGNES.
    ⑧ POURQUOI — Un fichier à moitié écrit ne doit jamais porter le vrai nom.
    ⑨ CE QUI CLOCHE — Les quatre renommages ne sont pas un seul geste : une coupure entre eux
      laisse un inventaire d'une lecture et un extrait d'une autre.
    ⑩ EFFET — Écrit les quatre fichiers, en remplaçant les anciens.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    os.makedirs(os.path.join(racine, DOSSIER), exist_ok=True)
    for chemin, entete, contenu in (
            (SORTIE, COURS_BNAINS, lignes),
            (INVENTAIRE, ["archive", "octets", "sha256", "lignes_lues", "lignes_gardees"], inventaire),
            (CONFLITS, COURS_BNAINS, conflits),
            (DROITS, DROITS_BNAINS, droits)):
        cible = os.path.join(racine, chemin)
        with open(cible + ".partiel", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(entete)
            w.writerows(contenu)
        os.replace(cible + ".partiel", cible)


def main(argv):
    """Enchaîne le téléchargement, la lecture et l'écriture ; rend le code de sortie.

    ① RÔLE — Porter la ligne de commande.
    ② CONTEXTE D'APPEL — Le bloc final, en ligne de commande ; les épreuves l'appellent aussi.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — Voir ④ du programme.
    ⑤ SORTIE — UNE valeur : le code 0, 1 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — ⑩ du programme ; affiche le résumé.
    ⑪ TERMINAISON — Rend la main ; une erreur prévue rend 2, une erreur imprévue lève et le bloc
      final la change en 2.
      [sort: non]
    """
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2 or not os.path.isdir(args[0]):
        print("USAGE : LIRE_LES_ARCHIVES_BNAINS.py <racine> <dossier des archives> [--telecharger]")
        return 2
    racine, dossier = args
    if "--telecharger" in argv:
        for e in telecharger(dossier):
            print(f"  ÉCHEC du téléchargement — {e}")
    manquantes = [n for n in ARCHIVES if not os.path.isfile(os.path.join(dossier, os.path.basename(n)))]
    if manquantes:
        print(f"ARRÊT — {len(manquantes)} archive(s) absente(s) de {dossier}, rien n'est écrit : "
              + ", ".join(manquantes))
        return 1
    try:
        codes = codes_des_valeurs(racine, lire_conversion(os.path.join(dossier, CONVERSION)))
        lignes, inventaire, conflits, droits, comptes = lire_archives(dossier, codes)
    except (ValueError, zipfile.BadZipFile, OSError) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    trous = lacunes(lignes)
    if trous:
        print(f"ARRÊT — {len(trous)} lacune(s) dans les séances lues, une archive est incomplète, rien n'est écrit : "
              + " ; ".join(trous))
        return 1
    ecrire(racine, lignes, inventaire, conflits, droits)
    par_valeur = {}
    for l in lignes:
        par_valeur[l[0]] = par_valeur.get(l[0], 0) + 1
    print("lignes lues par année", dict(sorted(comptes["par_annee"].items())))
    print(f"lignes mal formées {comptes['mal_formees']} · doublons identiques {comptes['doublons_identiques']}"
          f" · fichiers non lus {comptes['fichiers_ignores']} · conflits {len(conflits)} ligne(s)")
    print(f"{len(lignes)} lignes gardées, {len(par_valeur)} valeur(s) sur {len(set(codes.values()))} attendue(s) ; "
          "sans aucune ligne : " + (", ".join(sorted(set(codes.values()) - set(par_valeur))) or "aucune"))
    print(f"droits de souscription : {len(droits)} — " + ", ".join(f"{d[0]} {d[3]}" for d in droits))
    print(f"écrit : {SORTIE} · {INVENTAIRE} · {CONFLITS} · {DROITS}")
    return 0


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as e:
        print(f"ARRÊT — erreur imprévue {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
