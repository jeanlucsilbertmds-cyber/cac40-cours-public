#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py — Sam 10-10-2026 (Paris) — PROPOSÉ, non validé (A-539, A-555).
Simulation uniquement.

① RÔLE — Confronter chaque ligne de donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv aux documents GARDÉS au
  dépôt, et REFUSER : ① une phrase que la colonne `phrases_des_documents_gardes` attribue à un document et qui n'y
  est pas, mot pour mot · ② une phrase attribuée à un document que la ligne n'invoque pas · ③ un document gardé
  dont l'empreinte ou la taille a changé · ④ un chiffre déclaré (prix de souscription, parité, dividende non
  attaché, valeur distribuée) que ses phrases CONTREDISENT : une phrase de la ligne écrit cette grandeur, à sa place
  (le premier montant qui suit « prix de souscription », « dividende », « cours d'ouverture »), et ce n'est pas le
  chiffre déclaré — il suffit d'UNE telle écriture, même si une autre écrit le bon chiffre ·
  ⑤ un droit dont le prix ou la parité n'est pas déclaré, un dividende écrit et non déclaré, une ligne qui déclare
  à la fois un droit et une distribution · ⑥ un chiffre NON
  PROUVÉ — aucune phrase ne l'écrit — sans raison écrite dans la colonne `chiffres_sans_document` de sa ligne, ou
  dont la raison ne commence pas par ce chiffre ; et une raison écrite pour un chiffre prouvé.
  Le jour est dit « écrit » ou « non écrit » dans les phrases, sans plus : c'est K21 qui le juge, sur les cours.
② CONTEXTE D'APPEL — À la main, depuis la racine du dépôt, après toute modification de la table ou du registre :
  python3 programmes/CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py [racine]. Importé par
  etudes/outils/RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES.py (qui remplit la colonne des phrases) et par
  etudes/outils/GARDER_LES_DOCUMENTS_DES_DROITS.py (qui garde les documents). Ses épreuves :
  tests/EPREUVES_DE_LA_CONFRONTATION_AUX_DOCUMENTS_Sam_10-10-2026.py.
③ ENTRÉE — Facultatif : la racine du dépôt (par défaut, le dossier courant).
④ CONDITIONS D'ENTRÉE — La table porte les colonnes de son contrat (`DETACHEMENTS_OFFICIELS`) ; le registre
  `REGISTRE` (fichier, adresse, octets, sha256 ; `fichier` relatif au dossier du registre) ; `pdftotext` (poppler)
  pour les PDF, `soffice` (LibreOffice) pour les .doc.
⑤ SORTIE — UNE valeur : le code de sortie. 0 = aucun refus · 1 = au moins un refus, chacun nommé · 2 = la
  confrontation n'a pas pu tourner (table ou registre illisible, document gardé absent, outil d'extraction absent,
  toute erreur imprévue) — jamais 0 dans ce cas (R-734).
⑥ TRAITEMENT — ① lire le registre, vérifier l'empreinte et la taille de chaque document gardé · ② pour chaque ligne,
  lire ses phrases (`phrases_de_la_ligne`), vérifier que leur document est invoqué par la ligne
  (`documents_invoques`) et chercher chacune dans son document (`texte_du_document`, `phrase_dans_le_texte`) ·
  ③ juger chaque chiffre sur les phrases TROUVÉES (`juger_la_ligne`) · ④ confronter les non-prouvés aux raisons
  écrites (`raisons_de_la_ligne`) · ⑤ afficher une ligne par ligne de la table, les refus, les non-prouvés avec
  leur raison, ce qui est à lire, le compte · ⑥ sortir.
⑦ UNITÉ — Des euros par action (prix, dividende, valeur distribuée) ; un nombre d'actions anciennes pour une
  nouvelle (parité) ; des jours AAAA-MM-JJ ; des nombres de phrases.
⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026 à 13h18 : « 1 » à « Écrire le programme qui confronte chaque
  citation et chaque chiffre déclaré à son document gardé, et refuse ce qui n'y est pas ». Relecture de Cowork du
  même jour (22cc10b) : un prix de souscription déclaré faux de 0,15 % (Société Générale 2008, 47,00 € au lieu de
  47,50 €) passe TOUS les contrôles des cours, parce que la règle officielle se calcule sur le chiffre déclaré ; et
  deux phrases de BNP Paribas 2006, attribuées au BALO, n'y étaient pas. Seul le document peut refuser ces fautes.
  La relecture indépendante du 10-10-2026 a cassé la première version : un montant QUELCONQUE de la phrase
  prouvait le prix (le cours de clôture de 77,72 € « prouvait » un prix de 77,72 €), une date quelconque prouvait
  le jour, une phrase d'une autre ligne était acceptée, « 7,50 euros » était trouvé dans « 47,50 euros », et un
  chiffre devenu non prouvé passait sans refus. D'où : le montant LIÉ à son mot (`montants_lies`), le jour écrit
  sans valeur de preuve, le document invoqué, la frontière de mot, et la raison écrite exigée.
⑨ CE QUI CLOCHE — Un chiffre CALCULÉ (Kering, LVMH, TotalEnergies, le dividende de Vinci) n'est écrit dans aucun
  document : il porte sa raison, et le calcul est dans la citation. · LA TABLE EST ÉCRITE À LA MAIN : qui change à
  la fois un chiffre et sa raison, ou un chiffre et ses phrases (en ajoutant une phrase vraie d'un document invoqué
  qui écrit le faux chiffre et en retirant celles qui écrivent le vrai), ou une adresse dans la citation, passe —
  seconde relecture indépendante du 10-10-2026, cas V7 à V12. Ce programme refuse les ERREURS sur un chiffre ; il
  ne remplace pas la relecture du changement de la table (git diff), qui seule voit une raison ou une phrase
  changée. · Le cours de la veille vient des cours
  (bnains, Yahoo) : il n'est pas confronté ici. · La grandeur d'une phrase se reconnaît à des mots
  (`MOTS_PRIX`, `MOTS_DIVIDENDE`, `MOTS_OUVERTURE`, `POUR`) : une phrase tournée autrement ne prouve ni ne contredit
  rien, et le chiffre reste non prouvé — il faut alors une raison écrite, ce qui le montre. · Une parité se lit
  comme le rapport de deux nombres de part et d'autre de « pour » : une phrase qui en écrit deux prouve l'une ou
  l'autre. · Une valeur distribuée n'est prouvée que si une phrase écrit une parité de 1 pour 1 et l'ouverture :
  sinon elle est calculée. · Un dividende ÉCRIT par une phrase et non déclaré est refusé sauf raison écrite : la
  phrase peut parler du dividende que les actions nouvelles touchent, et c'est à l'homme de le dire. · Un document qui change chez sa source n'est pas
  suivi : on confronte à la copie gardée. → BACKLOG.
⑩ EFFET — Lit la table, le registre et les documents ; écrit puis efface un dossier temporaire pour la conversion
  d'un .doc. N'écrit rien au dépôt. Affiche le compte rendu.
⑪ TERMINAISON — Toujours : un nombre fini de documents et de lignes ; chaque extraction est bornée à `ATTENTE`
  secondes (un outil qui ne rend pas la main lève une erreur : sortie 2).
"""
import csv, hashlib, html, os, re, shutil, subprocess, sys, tempfile, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import DETACHEMENTS_OFFICIELS
import CONTROLER_L_HISTORIQUE_LONG as K

TABLE = os.path.join("donnees", "sources_bnains", "DETACHEMENTS_OFFICIELS.csv")
REGISTRE = os.path.join("temoins", "DOCUMENTS_DES_DROITS_REGLE_OFFICIELLE_Sam_10-10-2026", "DOCUMENTS.csv")
COLONNES_DU_REGISTRE = ["fichier", "adresse", "octets", "sha256"]
COLONNE = "phrases_des_documents_gardes"
COLONNE_RAISONS = "chiffres_sans_document"
GRANDEURS = ("prix_souscription", "anciennes_pour_une_nouvelle", "dividende_non_attache", "valeur_distribuee")
ENTRE_LES_PHRASES = " ¦ "        # sépare deux entrées dans les deux colonnes
ENTRE_FICHIER_ET_PHRASE = " :: "  # sépare le fichier gardé de la phrase
ENTRE_GRANDEUR_ET_RAISON = " : "  # sépare la grandeur (nom de colonne) de sa raison
COUPURE = re.compile(r"\s*\[(?:…|\.\.\.)\]\s*")   # « […] » : la citation saute un passage du document
ATTENTE = 120          # secondes par extraction
AU_CENTIME = 0.005     # euros : un montant écrit est le chiffre déclaré à moins d'un demi-centime près
PARITE_RELATIVE = 1e-6 # la parité déclarée à 7 chiffres (Pernod Ricard 2009 : 5,6666667 pour 17 ÷ 3)
AVANT, APRES = 60, 40  # signes : où chercher les deux nombres d'une parité, avant et après « pour »
LIEN = 80              # signes : le montant d'une grandeur est le PREMIER montant écrit moins de LIEN signes après
                       # son mot (Carrefour 2011 : « cours d'ouverture de l'action dia sur les bourses espagnoles
                       # s'est eleve a 3,40 euros », 58 signes)

NOMBRES_EN_LETTRES = {
    "un": 1, "une": 1, "one": 1, "deux": 2, "two": 2, "trois": 3, "three": 3, "quatre": 4, "four": 4,
    "cinq": 5, "five": 5, "six": 6, "sept": 7, "seven": 7, "huit": 8, "eight": 8, "neuf": 9, "nine": 9,
    "dix": 10, "ten": 10, "onze": 11, "eleven": 11, "douze": 12, "twelve": 12,
}
MOIS = ("janvier fevrier mars avril mai juin juillet aout septembre octobre novembre decembre "
        "january february march april may june july august september october november december").split()
# Un nombre : groupes de trois chiffres séparés par une espace ou un point (« 4 005 337 152,50 », « 476.842.699 »),
# ou des chiffres avec une décimale (« 47,50 », « 59.65 », « 1287.000 »). Jamais pris au milieu d'un autre nombre.
NOMBRE = r"(?<![\d.,])(?:\d{1,3}(?:[ .]\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(?![\d])"
# « at a price of » ajouté le 10-10-2026 : AXA 2003, « subscribe one ORAN bond at a price of € 12.75 for every 16
# warrants held » (document de la SEC gardé par Cowork) — l'anglais de « au prix de ».
MOTS_PRIX = re.compile(r"prix (?:unitaire )?(?:de souscription|d'emission|d'exercice)|prix unitaire|au prix de"
                       r"|subscription price|issue price|exercise price|offer price|at a price of")
MOTS_DIVIDENDE = re.compile(r"\bdividendes?\b|\bdividends?\b")
MOTS_OUVERTURE = re.compile(r"cours d'ouverture|opening price")
GRATUIT = re.compile(r"actions? (?:nouvelles? )?gratuites?|attribution gratuite d'(?:une )?actions?|free shares?"
                     r"|bonus shares?")
# ce qui sépare les deux nombres d'une parité : « 1 action nouvelle pour 4 », « 2 Offer Shares for every 5 »,
# « 12 droits préférentiels de souscription donneront le droit de souscrire à 1 action » (AXA 2009), « 10 droits
# préférentiels de souscription permettront de souscrire une action » (BNP Paribas 2009), « Six Rights will entitle »
POUR = re.compile(r"\b(?:pour|for every|for|permettront|permettent|donneront le droit|donnent le droit|entitle)\b")


def adresses_de_la_ligne(r):
    """Rend les adresses web écrites dans les colonnes `source` et `citation` d'une ligne de la table.

    ① RÔLE — Savoir quels documents une ligne invoque.
    ② CONTEXTE D'APPEL — `documents_invoques` ;
      etudes/outils/GARDER_LES_DOCUMENTS_DES_DROITS.py.
    ③ ENTRÉE — `r` : une ligne de la table (dictionnaire).
    ④ CONDITIONS D'ENTRÉE — Les clés `source` et `citation`.
    ⑤ SORTIE — UNE valeur : la liste des adresses, dans l'ordre d'apparition, sans doublon.
      [rend: 1]
    ⑥ TRAITEMENT — Chercher « http(s)://… » jusqu'au premier blanc ; ôter la ponctuation finale ) , ; . » ].
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La colonne `source` porte parfois une remarque après l'adresse (Edenred :
      « … .pdf (page 274 du PDF) ») et la citation porte les adresses de la presse et des communiqués.
    ⑨ CE QUI CLOCHE — Une adresse qui finit par une parenthèse fermante légitime la perd.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    vues = []
    for u in re.findall(r"https?://[^\s«»\"]+", r["source"] + " " + r["citation"]):
        u = u.rstrip("),;.»]")
        if u not in vues:
            vues.append(u)
    return vues


def documents_invoques(r, documents):
    """Rend les fichiers du registre qu'une ligne invoque : par leur adresse, ou par leur nom écrit dans la citation.

    ① RÔLE — Une phrase ne prouve un chiffre que si elle vient d'un document de SA ligne.
    ② CONTEXTE D'APPEL —
      `confronter` ; etudes/outils/RELEVER_LES_PHRASES_DES_DOCUMENTS_GARDES.py.
    ③ ENTRÉE — `r` : une ligne de la table · `documents` : le dictionnaire fichier → (chemin, adresse) du registre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fichiers, dans l'ordre du registre.
      [rend: 1]
    ⑥ TRAITEMENT — Un fichier est invoqué si son adresse est l'une de `adresses_de_la_ligne(r)` (BNP Paribas 2006 écrit
      dans sa citation l'adresse de sa note d'opération gardée). Le nom de fichier écrit dans la citation ne suffit
      plus : seconde relecture indépendante du 10-10-2026, « (voir aussi SOCIETE_GENERALE_2008_BALO…) » ajouté à la
      citation de Michelin faisait invoquer le BALO de Société Générale.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : la phrase du prix de Société Générale 2008,
      recopiée dans la ligne de Michelin 2010 déclarée à 47,50 €, « prouvait » le prix de Michelin.
    ⑨ CE QUI CLOCHE — Deux lignes qui invoquent le même document (la page de bnains de Safran, pour 2000 et 2003)
      peuvent s'échanger leurs phrases ; chaque phrase porte alors sa date, que le jour écrit montre. · Une adresse
      AJOUTÉE à la citation fait invoquer son document : la table est écrite à la main, et seul le relecteur de son
      changement le voit.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    adresses = adresses_de_la_ligne(r)
    return [f for f, (_, a) in documents.items() if a in adresses]


def forme(x):
    """Ramène un texte à la forme où une citation et le texte extrait d'un document se comparent.

    ① RÔLE — Comparer sans dépendre de la typographie.
    ② CONTEXTE D'APPEL — `texte_du_document`,
      `phrase_dans_le_texte`, `juger_la_ligne` ; l'outil qui remplit la colonne.
    ③ ENTRÉE — `x` : un texte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte ramené.
      [rend: 1]
    ⑥ TRAITEMENT — ① décomposition de compatibilité (NFKD : ligatures « ﬁ » → « fi », espaces insécables →
      espaces, accents séparés) puis accents ôtés · ② apostrophes ’ ‘ ʼ → ' ; tirets ‐ ‑ ‒ – — → - ; trait d'union
      conditionnel ôté · ③ minuscules · ④ blancs regroupés en une espace.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — pdftotext, les pages web et les citations n'écrivent pas pareil l'apostrophe,
      le tiret, l'espace insécable ni les ligatures (mesuré le 10-10-2026 sur les documents gardés).
    ⑨ CE QUI CLOCHE — Les accents ôtés confondent « prix d'émission » et « prix d'emission » : voulu.
      Une majuscule fautive dans la citation passe.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c) and c != chr(0xAD))
    x = re.sub(r"[’‘ʼ`´]", "'", x)
    x = re.sub(r"[‐‑‒–—−]", "-", x)
    return re.sub(r"\s+", " ", x.lower()).strip()


def texte_du_document(chemin):
    """Extrait le texte d'un document gardé (PDF, .doc ou page web) et le rend sous ses formes comparables.

    ① RÔLE — Avoir le texte où chercher les phrases.
    ② CONTEXTE D'APPEL — `confronter` ; l'outil qui remplit la
      colonne.
    ③ ENTRÉE — `chemin` : le chemin du document.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe ; `pdftotext` pour un PDF, `soffice` pour un .doc.
    ⑤ SORTIE — UNE valeur : la liste des textes extraits, chacun passé par `forme` — plusieurs lectures du
      même document, une phrase est trouvée si elle est dans l'une d'elles.
      [rend: 1]
    ⑥ TRAITEMENT — PDF (reconnu à ses premiers octets « %PDF ») : `pdftotext -layout` et `pdftotext` (ordre de
      lecture), et, pour chacune, une lecture où une coupure de mot en fin de ligne (« souscrip-␤tion ») est
      recollée · .doc (premiers octets D0 CF 11 E0) : `soffice --convert-to txt`, avec un profil LibreOffice
      à part, et son code de sortie lu · sinon page web : sans <script> ni <style>, balises → espaces, entités
      décodées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une mise en page en colonnes coupe une phrase dans `-layout` et la garde dans
      l'ordre de lecture (BNP Paribas 2006, « Cotation du droit préférentiel de souscription »). Le profil à part :
      relecture indépendante du 10-10-2026, une épreuve tombée une fois sur quatre quand plusieurs épreuves
      tournaient en même temps ; la cause SUPPOSÉE — deux conversions qui se disputent le profil commun — n'est pas
      mesurée.
    ⑨ CE QUI CLOCHE — Recoller les coupures ôte aussi le trait d'union d'un mot composé coupé en fin de ligne
      (« Saint-␤Gobain » devient « SaintGobain ») : c'est pourquoi la lecture brute est gardée à côté. · Un PDF
      scanné (image) ne rend aucun texte : ses phrases sont alors refusées, jamais acceptées.
    ⑩ EFFET — Écrit et efface un dossier temporaire pour un .doc.
    ⑪ TERMINAISON — Rend la main ; chaque outil est borné à `ATTENTE` secondes (sinon, erreur levée).
      [sort: non]
    """
    with open(chemin, "rb") as f:
        debut = f.read(4)
    bruts = []
    if debut == b"%PDF":
        if not shutil.which("pdftotext"):
            raise RuntimeError("pdftotext absent : les PDF ne peuvent pas être lus")
        for options in (["-layout"], []):
            r = subprocess.run(["pdftotext", *options, chemin, "-"], capture_output=True, timeout=ATTENTE)
            if r.returncode != 0:
                raise RuntimeError(f"pdftotext a échoué sur {chemin} : {r.stderr[:200]!r}")
            bruts.append(r.stdout.decode("utf-8", "replace"))
    elif debut == b"\xd0\xcf\x11\xe0":
        logiciel = shutil.which("soffice") or shutil.which("libreoffice")
        if not logiciel:
            raise RuntimeError("soffice absent : les .doc ne peuvent pas être lus")
        with tempfile.TemporaryDirectory() as dossier:
            r = subprocess.run([logiciel, f"-env:UserInstallation=file://{dossier}/profil", "--headless",
                                "--convert-to", "txt:Text", "--outdir", dossier, os.path.abspath(chemin)],
                               capture_output=True, timeout=ATTENTE)
            sorties = [n for n in os.listdir(dossier) if n.endswith(".txt")]
            if r.returncode != 0 or not sorties:
                raise RuntimeError(f"soffice n'a rien rendu pour {chemin} (code {r.returncode}) : {r.stderr[:200]!r}")
            bruts.append(open(os.path.join(dossier, sorties[0]), encoding="utf-8", errors="replace").read())
    else:
        t = open(chemin, encoding="utf-8", errors="replace").read()
        t = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", " ", t)
        bruts.append(html.unescape(re.sub(r"(?s)<[^>]*>", " ", t)))
    textes = []
    for b in bruts:
        textes.append(forme(b))
        textes.append(forme(re.sub(r"(\w)-[ \t]*\n\s*(\w)", r"\1\2", b)))
    return textes


def phrase_dans_le_texte(phrase, textes):
    """Dit si une phrase citée est dans un document : mot pour mot, aux sauts « […] » près, dans l'ordre.

    ① RÔLE — Le cœur de la confrontation.
    ② CONTEXTE D'APPEL — `confronter` ; l'outil qui remplit la colonne.
    ③ ENTRÉE — `phrase` : la phrase citée · `textes` : ce que rend `texte_du_document`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si, dans l'un des textes, chaque morceau de la phrase (coupée aux « […] »)
      se trouve, chacun après le précédent, et sans être collé à une lettre ou un chiffre de part et d'autre ;
      faux sinon, et faux pour une phrase vide.
      [rend: 1]
    ⑥ TRAITEMENT — Couper aux « […] », ramener chaque morceau par `forme`, chercher chacun dans l'ordre ; une
      occurrence dont le signe d'avant (ou d'après) est une lettre ou un chiffre — ou un point ou une virgule
      suivi d'un chiffre — quand le morceau commence (ou finit) par une lettre ou un chiffre, ne compte pas, et la
      suivante est cherchée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les citations sautent des passages (Pernod Ricard 2007 : « détenues. Le
      Conseil d'Administration […] a fixé la date »). La frontière : relecture indépendante du 10-10-2026,
      « 7,50 euros » était trouvé dans « 47,50 euros ».
    ⑨ CE QUI CLOCHE — Deux morceaux très éloignés passent : la distance n'est pas bornée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main : chaque recherche avance d'au moins un signe.
      [sort: non]
    """
    morceaux = [forme(m) for m in COUPURE.split(phrase) if forme(m)]
    if not morceaux:
        return False

    def borne(t, i, m):
        """Dit si l'occurrence du morceau `m` à la position `i` du texte `t` n'est collée à rien.

        ① RÔLE — La frontière de mot de la recherche.
        ② CONTEXTE D'APPEL — `phrase_dans_le_texte`, pour chaque occurrence trouvée.
        ③ ENTRÉE — `t` : un texte ramené · `i` : une position où `m` commence · `m` : un morceau ramené, non vide.
        ④ CONDITIONS D'ENTRÉE — `t[i:i + len(m)] == m`.
        ⑤ SORTIE — UNE valeur : vrai si l'occurrence est bornée des deux côtés, faux sinon.
          [rend: 1]
        ⑥ TRAITEMENT — Si `m` commence par une lettre ou un chiffre, le signe d'avant ne doit être ni une lettre ni un
          chiffre, ni « chiffre puis point ou virgule » ; de même après, si `m` finit par une lettre ou un chiffre.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — « 7,50 euros » trouvé dans « 47,50 euros » (relecture indépendante du 10-10-2026).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        avant = t[max(0, i - 2):i]
        apres = t[i + len(m):i + len(m) + 2]
        if m[0].isalnum() and avant and (avant[-1].isalnum() or re.fullmatch(r"\d[.,]", avant)):
            return False
        if m[-1].isalnum() and apres and (apres[0].isalnum() or re.fullmatch(r"[.,]\d", apres)):
            return False
        return True

    for t in textes:
        position = 0
        for m in morceaux:
            i = t.find(m, position)
            while i >= 0 and not borne(t, i, m):
                i = t.find(m, i + 1)
            if i < 0:
                break
            position = i + len(m)
        else:
            return True
    return False


def en_nombre(s):
    """Lit un nombre écrit à la française ou à l'anglaise ; rend None quand l'écriture est ambiguë.

    ① RÔLE — Comparer un montant écrit au chiffre déclaré.
    ② CONTEXTE D'APPEL — `montants`, `parites`.
    ③ ENTRÉE — `s` : un texte qui répond à `NOMBRE`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre (float), ou None.
      [rend: 1]
    ⑥ TRAITEMENT — ① les espaces sont des séparateurs de milliers (« 4 005 337 152,50 ») · ② avec une virgule :
      les points sont des milliers, la virgule la décimale · ③ sans virgule, plusieurs points : des milliers
      (« 476.842.699 ») · ④ sans virgule, un seul point suivi d'exactement trois chiffres et précédé d'au plus
      trois (« 50.000 », « 97.050 ») : AMBIGU, None · ⑤ sinon le point est la décimale (« 59.65 », « 1287.000 »).
    ⑦ UNITÉ — Celle du texte.
    ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : la note d'opération de BNP
      Paribas 2006 écrit les milliers avec des points 37 fois, le document de référence d'AXA 35 fois ;
      « 476.842.699 » faisait tomber la lecture ; « 50.000 euros » (LVMH, cinquante mille) se lisait 50.
    ⑨ CE QUI CLOCHE — « 97.050 € » (bnains, Safran : 97,05 €) et « 50.000 euros » (LVMH : 50 000 €) s'écrivent
      pareil : les deux sont ambigus et ne prouvent rien.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s = s.replace(" ", "")
    if "," in s:
        return float(s.replace(".", "").replace(",", "."))
    if s.count(".") > 1:
        return float(s.replace(".", ""))
    if re.fullmatch(r"\d{1,3}\.\d{3}", s):
        return None
    return float(s)


def montants(phrase):
    """Rend les montants en euros écrits dans une phrase : le nombre collé à « euros », « eur » ou « € ».

    ① RÔLE — Les montants qu'une phrase écrit.
    ② CONTEXTE D'APPEL — `montants_lies`, `parites`.
    ③ ENTRÉE — `phrase` : une phrase passée par `forme`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste de couples (début, nombre) — la position du nombre dans la phrase ; un nombre
      ambigu (`en_nombre` rend None) n'y figure pas.
      [rend: 1]
    ⑥ TRAITEMENT — Un `NOMBRE` suivi, à au plus une espace, du MOT « euro(s) » ou « eur », ou de « € » ; ou
      précédé de « € », « (euro) » ou du mot « eur ».
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — « 47,50 euros », « €59.65 », « (euro)26.50 », « 0,90 EUR », « 1287.000 € ».
      Le mot entier : « 2006 Euronext » n'est pas un montant (relecture indépendante du 10-10-2026).
    ⑨ CE QUI CLOCHE — « 2 euros de nominal » est un montant : il ne prouve un prix que s'il suit le mot du prix
      (`montants_lies`).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    trouves = []
    for m in re.finditer(r"(?:€|\(euro\)|\beur\b)\s?(" + NOMBRE + r")|(" + NOMBRE + r")\s?(?:euros?\b|eur\b|€)", phrase):
        texte, debut = (m.group(1), m.start(1)) if m.group(1) else (m.group(2), m.start(2))
        v = en_nombre(texte)
        if v is not None:
            trouves.append((debut, v))
    return trouves


def montants_lies(phrase, mots):
    """Rend les montants LIÉS à un mot : pour chaque occurrence du mot, le premier montant écrit après lui, à moins
    de `LIEN` signes.

    ① RÔLE — Savoir QUEL montant une phrase donne pour une grandeur : le prix, le dividende, l'ouverture.
    ② CONTEXTE D'APPEL — `sortes_de_la_phrase`, `juger_la_ligne`.
    ③ ENTRÉE — `phrase` : une phrase passée par `forme` · `mots` : une expression (`MOTS_PRIX`, `MOTS_DIVIDENDE`,
      `MOTS_OUVERTURE`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des montants liés (nombres), un au plus par occurrence du mot.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque occurrence du mot, parmi les `montants` qui commencent après sa fin et à moins de
      `LIEN` signes, le premier.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : quand tout montant de la phrase
      prouvait le prix, le cours de clôture (77,72 €) et la valeur du droit (5,86 €) de Société Générale 2008
      « prouvaient » un prix de souscription. « au prix de 19,80 euros avec un cours de bourse de 24,47 euros » :
      19,80 est lié au prix, 24,47 ne l'est pas.
    ⑨ CE QUI CLOCHE — Un document qui écrirait le montant AVANT le mot (« 47,50 euros, prix de souscription »)
      ne lie rien : le chiffre reste non prouvé, et sa raison est exigée. · Le lien dit « un prix », pas « le prix
      de cette opération » : seconde relecture indépendante du 10-10-2026, dans les documents invoqués, 21 prix
      liés sur 118 ne sont pas le prix déclaré (« issue price. Based on the closing price of €84.65 », un prix de
      souscription TOTAL, des options d'autres années) — d'où la règle « toutes les écritures » de
      `juger_la_ligne`, et la relecture humaine de chaque phrase ajoutée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sommes = montants(phrase)
    lies = []
    for m in mots.finditer(phrase):
        suivants = [v for d, v in sommes if m.end() <= d <= m.end() + LIEN]
        if suivants:
            lies.append(suivants[0])
    return lies


def parites(phrase):
    """Rend les parités qu'une phrase écrit : le rapport de deux nombres de part et d'autre de « pour » / « for ».

    ① RÔLE — Lire « 1 action nouvelle pour 4 actions anciennes », « 2 Offer Shares for every 5 existing »,
      « une (1) action nouvelle pour cinq (5) ».
    ② CONTEXTE D'APPEL — `sortes_de_la_phrase`, `juger_la_ligne`.
    ③ ENTRÉE — `phrase` : une phrase passée par `forme`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des rapports (le plus grand des deux nombres ÷ le plus petit), un par
      séparateur (`POUR` : « pour », « for », « permettront », « donneront le droit »…) qui a un nombre à moins de
      `AVANT` signes avant lui et à moins de `APRES` signes après.
      [rend: 1]
    ⑥ TRAITEMENT — ① les nombres de la phrase, en chiffres (`NOMBRE`), en lettres (`NOMBRES_EN_LETTRES`) ou entre
      parenthèses (« de (1) action », Société Générale 2006) ; un nombre en lettres suivi de son écriture entre
      parenthèses ne compte qu'une fois ; ni les montants (`montants`), ni les années (19xx, 20xx), ni un nombre
      suivi d'un nom de mois (« 1er juin ») ne comptent · ② pour chaque séparateur, le DERNIER nombre avant et le
      PREMIER après.
    ⑦ UNITÉ — Actions anciennes pour une nouvelle.
    ⑧ POURQUOI — La parité déclarée est toujours ≥ 1 ; le
      plus grand ÷ le plus petit rend le sens indifférent (« Six Rights will entitle the holder to purchase
      one Share » écrit l'ordre inverse).
    ⑨ CE QUI CLOCHE — Une phrase qui écrit deux « pour » (une action gratuite pour cinq, puis une division)
      rend deux parités, et prouve l'une ou l'autre. · « quarante et une (41) » se lit 41 grâce aux
      parenthèses ; sans elles, il ne se lit pas. · Le séparateur « pour » sert aussi hors des parités : « TSR à
      11 ans à taux variable émis en octobre 2001 pour un montant » se lit « 11 pour 1 » (Crédit Agricole,
      document de référence 2003, relevé le 10-10-2026) — une telle phrase, si on l'inscrivait, « prouverait »
      une parité de 11 : c'est le choix des phrases, relu, qui l'évite.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    pris = {d for d, _ in montants(phrase)}
    nombres = []
    # « 1action » (BNP Paribas 2006, BALO) : un chiffre se lit même collé au mot qui suit
    for m in re.finditer(r"\((\d+)\)|(" + NOMBRE + r")|\b([a-z]+)\b", phrase):
        if m.group(1):                       # « (1) », « (5) » : toujours un nombre
            if nombres and nombres[-1][2] and m.start() - nombres[-1][3] <= 2:
                nombres.pop()                # « cinq (5) » : le mot et ses chiffres ne comptent qu'une fois
            nombres.append((m.start(1), float(m.group(1)), False, m.end()))
        elif m.group(2):
            texte = m.group(2)
            if m.start(2) in pris or re.fullmatch(r"(19|20)\d\d", texte):
                continue
            suite = re.sub(r"^(?:er|st|nd|rd|th)\b", "", phrase[m.end(2):m.end(2) + 14]).split()  # « 1er juin »
            if suite and suite[0].strip(".,") in MOIS:
                continue
            v = en_nombre(texte)
            if v is not None:
                nombres.append((m.start(2), v, False, m.end()))
        elif m.group(3) in NOMBRES_EN_LETTRES:
            nombres.append((m.start(3), float(NOMBRES_EN_LETTRES[m.group(3)]), True, m.end()))
    nombres = [(d, v) for d, v, _, _ in nombres]
    rapports = []
    for p in POUR.finditer(phrase):
        avant = [v for d, v in nombres if p.start() - AVANT <= d < p.start()]
        apres = [v for d, v in nombres if p.end() < d <= p.end() + APRES]
        if avant and apres and min(avant[-1], apres[0]) > 0:
            rapports.append(max(avant[-1], apres[0]) / min(avant[-1], apres[0]))
    return rapports


def sortes_de_la_phrase(phrase):
    """Dit quelles grandeurs une phrase écrit À LEUR PLACE — sans regarder le chiffre déclaré.

    ① RÔLE — Savoir si une phrase écrit une grandeur de la même sorte qu'un chiffre déclaré, pour dire qu'elle le
      CONTREDIT quand elle ne l'écrit pas.
    ② CONTEXTE D'APPEL — `juger_la_ligne`.
    ③ ENTRÉE — `phrase` : une phrase passée par `forme`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des sortes, parmi "prix", "dividende", "ouverture", "parite".
      [rend: 1]
    ⑥ TRAITEMENT — "prix", "dividende", "ouverture" : un montant lié à `MOTS_PRIX`, `MOTS_DIVIDENDE`,
      `MOTS_OUVERTURE` (`montants_lies`) · "parite" : au moins une parité (`parites`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête, ⑧ : le jugement ne doit pas dépendre du chiffre jugé — sans quoi
      changer le chiffre changerait aussi ce qu'on lui oppose.
    ⑨ CE QUI CLOCHE — « Based on the closing price of €84.65 » n'est pas un prix de souscription : voulu.
      « 2 euros de nominal » dans une phrase de parité ne la rend pas « prix ».
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sortes = set()
    for nom, mots in (("prix", MOTS_PRIX), ("dividende", MOTS_DIVIDENDE), ("ouverture", MOTS_OUVERTURE)):
        if montants_lies(phrase, mots):
            sortes.add(nom)
    if parites(phrase):
        sortes.add("parite")
    return sortes


def phrases_de_la_ligne(r):
    """Lit la colonne `phrases_des_documents_gardes` d'une ligne : la liste des (fichier, phrase).

    ① RÔLE — Lire ce que la ligne affirme tenir de ses documents.
    ② CONTEXTE D'APPEL — `confronter` ; l'outil qui
      remplit la colonne.
    ③ ENTRÉE — `r` : une ligne de la table.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des couples (fichier, phrase) ; une entrée sans « :: » rend (None, entrée).
      [rend: 1]
    ⑥ TRAITEMENT — Couper à `ENTRE_LES_PHRASES`, puis chaque entrée au premier `ENTRE_FICHIER_ET_PHRASE`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une phrase est attribuée à UN document : BNP Paribas 2006 avait deux phrases
      attribuées au BALO qui étaient dans la note d'opération (Cowork, 10-10-2026).
    ⑨ CE QUI CLOCHE — Une phrase qui contiendrait « ¦ » serait coupée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sortie = []
    for e in (r.get(COLONNE) or "").split(ENTRE_LES_PHRASES):
        if not e.strip():
            continue
        if ENTRE_FICHIER_ET_PHRASE in e:
            fichier, phrase = e.split(ENTRE_FICHIER_ET_PHRASE, 1)
            sortie.append((fichier.strip(), phrase.strip()))
        else:
            sortie.append((None, e.strip()))
    return sortie


def raisons_de_la_ligne(r):
    """Lit la colonne `chiffres_sans_document` d'une ligne : la grandeur → la raison pour laquelle aucun document
    gardé ne l'écrit.

    ① RÔLE — Un chiffre non prouvé doit dire pourquoi.
    ② CONTEXTE D'APPEL — `confronter`.
    ③ ENTRÉE — `r` : une ligne de la table.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire grandeur (nom de colonne) → raison ; une entrée sans « : » ou d'une
      grandeur inconnue a la clé None.
      [rend: 1]
    ⑥ TRAITEMENT — Couper à `ENTRE_LES_PHRASES`, puis au premier `ENTRE_GRANDEUR_ET_RAISON`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : un chiffre devenu non prouvé (sa phrase
      retirée, ou une phrase trop pauvre) passait sans refus, la liste affichée ne gardant rien. La raison écrite
      dans la ligne fait de chaque non-prouvé une décision lisible.
    ⑨ CE QUI CLOCHE — La raison n'est pas jugée : elle est lue par l'homme.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    raisons = {}
    for e in (r.get(COLONNE_RAISONS) or "").split(ENTRE_LES_PHRASES):
        if not e.strip():
            continue
        grandeur, _, raison = e.partition(ENTRE_GRANDEUR_ET_RAISON)
        grandeur = grandeur.strip()
        raisons[grandeur if grandeur in GRANDEURS and raison.strip() else None] = raison.strip() or e.strip()
    return raisons


def juger_la_ligne(r, phrases):
    """Juge chaque chiffre déclaré d'une ligne contre les phrases trouvées dans ses documents.

    ① RÔLE — Dire, pour chaque grandeur de `GRANDEURS` : prouvé, contredit, non prouvé ou non déclaré ; et si le
      jour est écrit.
    ② CONTEXTE D'APPEL — `confronter` ; les épreuves.
    ③ ENTRÉE — `r` : une ligne de la table · `phrases` : les phrases de la ligne TROUVÉES dans leur document
      (une phrase absente ne prouve ni ne contredit rien : elle est refusée à part).
    ④ CONDITIONS D'ENTRÉE — Les colonnes du contrat.
    ⑤ SORTIE — UNE valeur : la liste des triplets (grandeur, chiffre déclaré, verdict). Verdicts : "prouvé",
      "contredit", "non prouvé", "non déclaré" (prix ou parité vide pour un droit), "à lire" (dividende écrit par
      une phrase, non déclaré), "deux natures" (prix ou parité ET valeur distribuée) ; pour le jour, "écrit" ou "non écrit". Une grandeur vide hors de ces cas n'y figure pas.
      [rend: 1]
    ⑥ TRAITEMENT — Toutes les phrases ramenées par `forme`. Une ligne est un DROIT si `valeur_distribuee` est vide.
      Les montants et les parités se lisent morceau par morceau, une phrase coupée à ses « […] ». PROUVÉ : la
      grandeur est écrite, et TOUTES ses écritures dans les phrases de la ligne valent le chiffre ; CONTREDIT : l'une
      au moins diffère ; NON PROUVÉ : aucune ne l'écrit.
      ① prix > 0 : écritures = les montants liés au prix (`montants_lies`, `MOTS_PRIX`), à `AU_CENTIME` près · prix = 0 (actions gratuites) : contredit si une
      phrase lie un prix ; prouvé si une phrase dit « actions gratuites » (`GRATUIT`) ; sinon non prouvé ·
      ② parité : écritures = les parités (`parites`), à `PARITE_RELATIVE` près · ③ dividende non attaché : comme
      le prix, avec `MOTS_DIVIDENDE` ; vide alors qu'une phrase en lie un : "à lire" · ④ valeur distribuée :
      écritures = les montants liés à `MOTS_OUVERTURE`, jugées seulement si une phrase écrit une parité de 1 pour
      1 ; sinon non prouvée · ⑤ prix ou parité vide pour un droit : non déclaré ; prix ou parité remplis pour une
      distribution : "deux natures" ·
      ⑥ jour : écrit si une phrase l'écrit (`K.jour_ecrit`), sans autre valeur.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête, ⑧. La valeur distribuée par action est le cours de ce qui est distribué × la
      parité : elle n'est le montant écrit que pour une parité de 1 pour 1 (Accor 2010, Carrefour 2011) ; ailleurs
      elle est calculée (TotalEnergies 2006 : 27 € ÷ 40). Le jour : une date écrite dans la phrase ne dit pas
      laquelle est le détachement (BNP Paribas 2006 écrit le 6 mars, veille du détachement, le 7 et le 20) —
      relecture indépendante du 10-10-2026, 14 jours faux sur 15 « prouvés ».
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    formes = [forme(p) for p in phrases]
    # les montants et les parités se lisent MORCEAU par morceau : jamais à travers un « […] »
    morceaux = [forme(m) for p in phrases for m in COUPURE.split(p) if forme(m)]
    lies = {nom: [v for p in morceaux for v in montants_lies(p, mots)]
            for nom, mots in (("prix", MOTS_PRIX), ("dividende", MOTS_DIVIDENDE), ("ouverture", MOTS_OUVERTURE))}
    toutes_parites = [q for p in morceaux for q in parites(p)]
    # prouvé : la grandeur est écrite, et TOUTES ses écritures valent le chiffre ; contredit : l'une diffère
    egal = lambda valeur, liste: bool(liste) and all(abs(v - valeur) <= AU_CENTIME for v in liste)
    differe = lambda valeur, liste: any(abs(v - valeur) > AU_CENTIME for v in liste)
    droit = not r["valeur_distribuee"].strip()
    verdicts = []

    def juger(grandeur, ok, contredit):
        """Ajoute aux verdicts celui d'une grandeur : prouvé, contredit ou non prouvé.

        ① RÔLE — Écrire un verdict d'une seule façon.
        ② CONTEXTE D'APPEL — `juger_la_ligne`, une fois par grandeur remplie.
        ③ ENTRÉE — `grandeur` : un nom de colonne de `GRANDEURS` · `ok` : la grandeur est prouvée · `contredit` :
          une écriture diffère du chiffre.
        ④ CONDITIONS D'ENTRÉE — `ok` et `contredit` ne sont pas vrais ensemble (une écriture qui diffère interdit
          « toutes égales »).
        ⑤ SORTIE — Rien n'est rendu : le verdict est ajouté à la liste.
          [rend: rien]
        ⑥ TRAITEMENT — Ajouter (grandeur, chiffre de la ligne, verdict) à la liste `verdicts` de `juger_la_ligne`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Trois verdicts, une seule règle pour les nommer.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie la liste `verdicts` de la fonction qui l'entoure.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        verdicts.append((grandeur, r[grandeur], "prouvé" if ok else "contredit" if contredit else "non prouvé"))

    if r["prix_souscription"].strip():
        prix = float(r["prix_souscription"])
        if prix == 0:
            juger("prix_souscription", not lies["prix"] and any(GRATUIT.search(p) for p in formes), bool(lies["prix"]))
        else:
            juger("prix_souscription", egal(prix, lies["prix"]), differe(prix, lies["prix"]))
    elif droit:
        verdicts.append(("prix_souscription", "", "non déclaré"))
    if r["anciennes_pour_une_nouvelle"].strip():
        n = float(r["anciennes_pour_une_nouvelle"])
        juger("anciennes_pour_une_nouvelle",
              bool(toutes_parites) and all(abs(q - n) <= PARITE_RELATIVE * n for q in toutes_parites),
              any(abs(q - n) > PARITE_RELATIVE * n for q in toutes_parites))
    elif droit:
        verdicts.append(("anciennes_pour_une_nouvelle", "", "non déclaré"))
    if r["dividende_non_attache"].strip():
        d = float(r["dividende_non_attache"])
        juger("dividende_non_attache", egal(d, lies["dividende"]), differe(d, lies["dividende"]))
    elif lies["dividende"]:
        verdicts.append(("dividende_non_attache", "", "à lire"))
    if not droit:
        un_pour_un = any(abs(q - 1) <= PARITE_RELATIVE for q in toutes_parites)
        v = float(r["valeur_distribuee"])
        juger("valeur_distribuee", un_pour_un and egal(v, lies["ouverture"]), un_pour_un and differe(v, lies["ouverture"]))
        if r["prix_souscription"].strip() or r["anciennes_pour_une_nouvelle"].strip():
            verdicts.append(("valeur_distribuee", r["valeur_distribuee"], "deux natures"))
    jour = r["jour_du_detachement"]
    verdicts.append(("jour_du_detachement", jour,
                     "écrit" if any(K.jour_ecrit(f"« {p} »", jour) for p in phrases) else "non écrit"))
    return verdicts


def lire_le_registre(racine):
    """Lit le registre des documents gardés et vérifie l'empreinte et la taille de chacun.

    ① RÔLE — Savoir quels documents sont gardés, et qu'ils n'ont pas changé.
    ② CONTEXTE D'APPEL — `confronter` ;
      l'outil qui remplit la colonne.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le registre existe.
    ⑤ SORTIE — DEUX valeurs, en un tuple : le dictionnaire fichier → (chemin complet, adresse) · la liste des
      fichiers dont l'empreinte ou la taille n'est pas celle du registre.
      [rend: 2]
    ⑥ TRAITEMENT — Lire le registre (en-tête `COLONNES_DU_REGISTRE`, sinon erreur) ; pour chaque fichier (absent :
      erreur levée), comparer son sha256 et son nombre d'octets au registre.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — Une phrase confrontée à un document modifié ne prouve plus rien.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin = os.path.join(racine, REGISTRE)
    dossier = os.path.dirname(chemin)
    documents, changes = {}, []
    with open(chemin, encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != COLONNES_DU_REGISTRE:
            raise ValueError(f"{REGISTRE} : en-tête {lecteur.fieldnames} au lieu de {COLONNES_DU_REGISTRE}")
        for r in lecteur:
            p = os.path.normpath(os.path.join(dossier, r["fichier"]))
            with open(p, "rb") as g:
                contenu = g.read()
            if hashlib.sha256(contenu).hexdigest() != r["sha256"] or str(len(contenu)) != r["octets"]:
                changes.append(r["fichier"])
            documents[r["fichier"]] = (p, r["adresse"])
    return documents, changes


def lire_la_table(racine):
    """Lit donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv et vérifie son en-tête contre le contrat.

    ① RÔLE — Les lignes à confronter.
    ② CONTEXTE D'APPEL — `confronter`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des lignes (dictionnaires).
      [rend: 1]
    ⑥ TRAITEMENT — Lire ; un en-tête autre que `DETACHEMENTS_OFFICIELS` lève une erreur.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ce qui se partage se déclare (CONTRATS_DES_FICHIERS).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(os.path.join(racine, TABLE), encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != DETACHEMENTS_OFFICIELS:
            raise ValueError(f"{TABLE} : en-tête {lecteur.fieldnames} au lieu de {DETACHEMENTS_OFFICIELS}")
        return list(lecteur)


def confronter(racine):
    """Fait la confrontation entière et rend son compte rendu.

    ① RÔLE — Voir l'en-tête du module.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — QUATRE valeurs, en un tuple : la liste des refus · la liste des non-prouvés avec leur raison · la
      liste de ce qui est à lire · la liste des lignes du compte rendu (une par ligne de la table) — des textes.
      [rend: 4]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥, pas ① à ④. Un non-prouvé sans raison est un refus ; une raison qui ne
      COMMENCE pas par le chiffre déclaré tel qu'il est dans la table, suivi d'une espace (« 0.675 » ou « 0,675 »),
      aussi — sans quoi la raison d'un chiffre calculé couvrirait un chiffre faux (relecture indépendante du
      10-10-2026 : TotalEnergies déclaré à 27 € au lieu de 0,675 € ; « contient » ne suffit pas, la raison écrit
      « 27 € » dans son calcul) ; une raison écrite pour une grandeur qui n'est pas non prouvée (prouvée, vide,
      inconnue) aussi. Un dividende écrit par une phrase et non déclaré est un refus, sauf raison écrite.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Séparé de `main` pour que les épreuves jugent les refus sans lire l'écran.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit ; voir `texte_du_document`.
    ⑪ TERMINAISON — Rend la main ; une erreur d'extraction ou de lecture est levée, pas avalée.
      [sort: non]
    """
    documents, changes = lire_le_registre(racine)
    refus = [f"document gardé MODIFIÉ (empreinte ou taille autre que celle du registre) : {f}" for f in changes]
    non_prouves, a_lire, lignes = [], [], []
    textes = {}
    for r in lire_la_table(racine):
        nom = f"{r['valeur']} {r['jour_du_detachement']}"
        invoques = documents_invoques(r, documents)
        trouvees = []
        entrees = phrases_de_la_ligne(r)
        for fichier, phrase in entrees:
            if fichier not in documents:
                refus.append(f"{nom} : phrase attribuée à un document NON GARDÉ ({fichier}) : « {phrase[:70]} »")
                continue
            if fichier not in invoques:
                refus.append(f"{nom} : phrase d'un document que la ligne N'INVOQUE PAS ({fichier}) : « {phrase[:70]} »")
                continue
            if fichier not in textes:
                textes[fichier] = texte_du_document(documents[fichier][0])
            if phrase_dans_le_texte(phrase, textes[fichier]):
                trouvees.append(phrase)
            else:
                refus.append(f"{nom} : phrase ABSENTE de {fichier} : « {phrase[:90]} »")
        verdicts = juger_la_ligne(r, trouvees)
        raisons = raisons_de_la_ligne(r)
        sans_preuve = set()
        for grandeur, chiffre, verdict in verdicts:
            if verdict == "contredit":
                refus.append(f"{nom} : {grandeur} déclaré {chiffre}, CONTREDIT par ses phrases (elles écrivent "
                             f"cette grandeur à sa place, mais pas ce chiffre)")
            elif verdict == "deux natures":
                refus.append(f"{nom} : la ligne déclare À LA FOIS un droit (prix ou parité) et une distribution "
                             f"(valeur distribuée {chiffre})")
            elif verdict == "non déclaré":
                refus.append(f"{nom} : {grandeur} NON DÉCLARÉ pour un droit")
            elif verdict == "à lire":
                sans_preuve.add(grandeur)
                if grandeur in raisons:
                    a_lire.append(f"{nom} : une phrase écrit un dividende, la ligne n'en déclare aucun — "
                                  f"{raisons[grandeur]}")
                else:
                    refus.append(f"{nom} : une phrase écrit un dividende, la ligne n'en déclare AUCUN, et sans raison "
                                 f"écrite dans `{COLONNE_RAISONS}`")
            elif verdict == "non prouvé":
                sans_preuve.add(grandeur)
                if grandeur not in raisons:
                    refus.append(f"{nom} : {grandeur} {chiffre} NON PROUVÉ, et sans raison écrite dans "
                                 f"`{COLONNE_RAISONS}`")
                elif not raisons[grandeur].startswith((chiffre + " ", chiffre.replace(".", ",") + " ")):
                    refus.append(f"{nom} : {grandeur} {chiffre} NON PROUVÉ, et sa raison ne commence pas par ce "
                                 f"chiffre (la raison vaut pour un autre chiffre)")
                else:
                    non_prouves.append(f"{nom} : {grandeur} {chiffre} — {raisons[grandeur]}")
        for grandeur in raisons:
            if grandeur not in sans_preuve:
                refus.append(f"{nom} : raison écrite pour « {grandeur} », qui n'est pas un chiffre non prouvé "
                             f"de la ligne : à retirer ou à corriger")
        lignes.append(f"{nom:32} phrases trouvées {len(trouvees)}/{len(entrees)} · " +
                      " · ".join(f"{g} {c} {v}" for g, c, v in verdicts))
    return refus, non_prouves, a_lire, lignes


def main(racine=None):
    """Lance la confrontation et sort avec son code.

    ① RÔLE — Voir l'en-tête du module.
    ② CONTEXTE D'APPEL — La ligne de commande ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt ; à défaut, `sys.argv[1]`, et à défaut le dossier courant.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — `confronter`, puis afficher : les lignes, les refus, les non-prouvés, ce qui est à lire, le compte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    racine = racine or (sys.argv[1] if len(sys.argv) > 1 else ".")
    try:
        refus, non_prouves, a_lire, lignes = confronter(racine)
    except Exception as e:  # R-734 : tout ce qui empêche de juger sort en 2, jamais en 0
        print(f"LA CONFRONTATION N'A PAS PU TOURNER : {type(e).__name__} : {e}")
        return 2
    for l in lignes:
        print(l)
    print(f"\nREFUS : {len(refus)}")
    for x in refus:
        print("  ✗", x)
    print(f"NON PROUVÉS, chacun avec sa raison écrite : {len(non_prouves)}")
    for x in non_prouves:
        print("  ·", x)
    print(f"À LIRE : {len(a_lire)}")
    for x in a_lire:
        print("  ?", x)
    print(f"\nRÉSUMÉ : lignes {len(lignes)} · refus {len(refus)} · non prouvés {len(non_prouves)} · à lire {len(a_lire)}")
    return 1 if refus else 0


if __name__ == "__main__":
    sys.exit(main())
