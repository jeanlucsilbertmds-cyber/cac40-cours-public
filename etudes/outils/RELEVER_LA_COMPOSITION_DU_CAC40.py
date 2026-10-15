#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RELEVER_LA_COMPOSITION_DU_CAC40.py — Lun 12-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit. Simulation uniquement.

① RÔLE — Dire, pour chaque ligne de cotation, de quelle séance à quelle séance elle a fait partie du CAC 40 depuis le
  03-01-2000 (les « passages »), à partir de l'historique des admissions et retraits archivé par bnains et de la date
  d'effet lue dans chaque avis officiel d'Euronext ; et vérifier que la composition rejouée compte 40 valeurs à chaque
  séance.
② CONTEXTE D'APPEL — À la main, depuis la racine du dépôt :
  python3 -I etudes/outils/RELEVER_LA_COMPOSITION_DU_CAC40.py <racine> [--telecharger]
  « --telecharger » relève de nouveau les pages et les avis sur bnains.org et réécrit les témoins ; sans lui, le
  programme ne lit que les témoins gardés au dépôt. Aucune tâche ne l'appelle.
③ ENTRÉE — Sous la racine : le dossier des témoins TEMOINS (la page de l'historique, la composition du 03-01-2000, les
  avis officiels en PDF et leur texte, et leur REGISTRE.csv avec l'empreinte de chacun) ; le calendrier des séances
  (programmes/CALENDRIER_DE_LA_BOURSE.py, `lire_les_seances`).
④ CONDITIONS D'ENTRÉE — Chaque témoin inscrit au registre existe et porte l'empreinte inscrite, et le dossier ne porte
  aucun fichier hors registre (sinon : arrêt, code 2) ; la composition du 03-01-2000 porte 40 lignes.
⑤ SORTIE — Le fichier SORTIE (contrat PASSAGES_DANS_LE_CAC40) et un compte rendu affiché ; le code de sortie : 0 quand
  les séances où la composition ne compte pas 40 valeurs sont exactement les écarts connus (ECARTS_CONNUS) et les dates
  de bnains corrigées par un avis exactement celles connues (ECARTS_A_LA_COLONNE), 1 sinon, 2 quand la lecture n'a pas
  pu se faire ou que le registre des témoins a changé (R-734).
⑥ TRAITEMENT — ① vérifier les témoins · ② lire la composition du 03-01-2000 · ③ lire chaque événement de l'historique
  (date, admission ou retrait, code, libellé, note, avis) · ④ dater chaque événement par l'avis officiel quand il se
  lit, sinon par la note de bnains, sinon par la colonne de bnains, en appariant un retrait sans date à l'admission de
  la séance suivante · ⑤ rejouer la composition séance par séance · ⑥ en tirer les passages · ⑦ écrire, afficher.
⑦ UNITÉ — Des séances du calendrier (R-110) ; « première séance » et « dernière séance » d'un passage sont toutes deux
  des séances où la ligne était dans l'indice.
⑧ POURQUOI — Décision de Jean-Luc du 11-10-2026 (« Oui », à 22h57) de construire les deux tables de la règle I-3 —
  les sociétés avec leurs entrées et sorties de l'indice, et leurs identités datées —, puis « Oui dépose les » le
  12-10-2026 à 07h47. La table que Cowork avait relevée par nom le 04-10-2026
  (donnees/sources_yahoo/composition_cac40_passages.csv) portait 7 dates de sortie fausses, un passage manquant
  (Edenred, 02-07-2010) et 7 lignes mêlant deux sociétés ; ce qu'un programme peut faire, un programme le fait (R-754).
  Elle est rangée depuis le 12-10-2026, sur décision de Jean-Luc, sous archives/composition_cac40_passages_REMPLACEE_
  LE_12-10-2026_PAR_PASSAGES_DANS_LE_CAC40_RETRAITS_PROVISOIRES_PROLONGES_A_TORT.csv.
⑨ CE QUI CLOCHE — La composition compte 39 valeurs pendant 8 périodes et 41 pendant 2 (ECARTS_CONNUS, chacun avec sa
  preuve) : c'est réel quand un avis le dit (Aventis « provisoirement retirée … à l'issue de la séance du 18 juin
  2004 », avis 2004-1786, sans remplaçant avant le 01-10-2004 ; Edenred ajoutée le 02-07-2010, avis 2010-097) ;
  Worldline du 03-05 au 21-06-2019 n'a pas d'avis trouvé. · Les codes ISIN sont ceux de bnains, qui garde parfois un
  code périmé (Lafarge pour LafargeHolcim, Technip pour TechnipFMC, Dassault Systèmes avant sa division de 2021) : un
  passage n'est PAS une société ; la table des identités dit quelle société portait la ligne à chaque date. · Un avis
  dont la date ne se lit pas (2000-2735) laisse la date de bnains. · Les libellés sont ceux de bnains, tronqués chez
  lui (« Aventis (Ex Rh »). · Quatre codes ISIN calculés depuis le Sicovam (ancien Legrand, CCF, Aérospatiale Matra,
  Vivendi) ne figurent dans aucun avis gardé : calculés, non lus.
⑩ EFFET — Lit les témoins ; écrit SORTIE ; avec « --telecharger », lit bnains.org et réécrit les témoins.
⑪ TERMINAISON — Rend la main ; les téléchargements ont chacun un délai de 60 secondes.
  [sort: oui]
"""
import csv
import hashlib
import html
import importlib.util
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
TEMOINS = os.path.join("temoins", "COMPOSITION_DU_CAC40_Lun_12-10-2026")
SORTIE = os.path.join("donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv")
HISTORIQUE = "histocac.html"
COMPOSITION_INITIALE = "composition_2000-01-03.html"
DEBUT = date(2000, 1, 3)
ADRESSE = "https://www.bnains.org/archives/histocac/"
UA = "Mozilla/5.0"
MOIS = {"janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
        "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12}
# La phrase d'un avis qui porte sa date d'effet. Les phrases « à l'issue de la séance du », « after markets close
# on » et « as from the market close of » désignent la DERNIÈRE séance de l'ancienne composition : la date d'effet est
# la séance suivante. Le blanc avant l'année est facultatif : l'avis 2002-2789 écrit « A compter du 6 août2002 »
# (relecture du 12-10-2026). Un avis qui écrit « Annule et remplace l'avis N°… » rend l'avis désigné nul : ses dates ne
# sont jamais lues (l'avis 2000-5131 annule le 2000-5128, qui faisait entrer Dassault Systèmes le 21-12-2000).
ANNULE = re.compile(r"annule et remplace l.\s?avis\s*(?:n°\s*|du\s*)?(\d{4})\s*[-–]\s*(\d+)", re.I)
# Le numéro d'un avis se lit dans son TEXTE (« N° 2002 - 2789 », « Announcement No: 2010 - 097 ») et jamais dans le
# nom du fichier (relecture du 12-10-2026 : « 0_4245_1626_… » donnait le faux numéro 4245-1626).
NUMERO_D_AVIS = re.compile(r"(?:N°|No\s*:)\s*(\d{4})\s*[-–]\s*(\d{2,4})")
# La date de publication d'un avis, quand son en-tête la donne : après « Issue Date: » ou « Date de publication : »
# (« Issue Date: Friday 2 September 2011 »), sinon juste avant son numéro (« 29 août 2002 N° 2002 - 2789 », « 15 juin/
# June 16th, 2006 N° 2006-1694 », « 18 août 2005 / august 18 , 2005 N° 2005-3339 »). Relecture du 12-10-2026 : la première forme, sensible à la casse et liée aux mots
# « NOTICES » ou « FRANCAISES », ne lisait que 18 avis sur 52.
PUBLICATION = (re.compile(r"(?:issue date|date de publication)\s*:\s*(?:\w+\s+)?(\d{1,2})\s+([A-Za-zéû]+)\s*(\d{4})", re.I),
               re.compile(r"(\d{1,2})\s+([A-Za-zéû]+)\s*(?:\d{4}\s*)?(?:/[^/N]{0,25}?)?,?\s*(\d{4})\s*N°"))
A_VENIR = "à venir : au-delà de la dernière séance du calendrier"
# L'empreinte SHA-256 du registre des témoins. Changer de témoins (un nouveau relevé avec « --telecharger ») change
# cette empreinte : le relevé s'arrête alors (code 2) jusqu'à ce que la nouvelle empreinte soit recopiée ici, après
# relecture des témoins nouveaux. Relecture du 12-10-2026 : un faux avis inscrit au registre avec sa propre empreinte
# passait sans bruit.
EMPREINTE_DU_REGISTRE = "2641aabf7597637c8ce9c6ff55290901a1668c452101c54d3edcabe858e4cdc8"
PHRASE_D_EFFET = re.compile(
    r"(effective date\s*:|date d.effet\s*:|prendront effet (?:à compter du |le )|effective (?:from|as of)|"
    r"effective(?= (?:monday|tuesday|wednesday|thursday|friday))|after (?:the )?markets? close on|"
    r"as from the markets? close of|à compter du|a compter du|à l.\s?issue de la séance (?:de bourse )?du|à partir du)"
    r"\s*(?:\w+day |lundi |mardi |mercredi |jeudi |vendredi )?(\d{1,2})(?:er)?\s+([A-Za-zéû]+)\s*(\d{4})?", re.I)
# LES ÉCARTS CONNUS AU COMPTE DE 40, chacun avec son explication et la source de celle-ci — un avis, ou bnains seul
# quand aucun avis n'est gardé (AGF, Worldline, Thomson Multimédia, Dassault Systèmes 2000 : à vérifier). Écrit À LA
# MAIN : la mesure se calcule, l'explication non.
# Le programme rend 0 quand les écarts mesurés sont exactement ceux-là, 1 sinon — un écart nouveau, disparu ou
# déplacé se voit au code de sortie (relecture du 12-10-2026 : avec 1 permanent, rien ne pouvait rougir).
ECARTS_CONNUS = {
    ("2000-06-26", "2000-08-22", 39): "CCF sort (avis 2000-2735 : « le 26 juin 2000 »), Thomson Multimédia n'entre que le "
                                      "23-08-2000 (colonne de bnains, avis absent)",
    ("2000-12-11", "2000-12-20", 39): "Canal+ sort le 11-12-2000 (avis 2000-5131), Dassault Systèmes entre le 21-12-2000 "
                                      "(colonne de bnains ; l'avis 2000-5128 qui le disait est annulé)",
    ("2003-05-22", "2003-07-10", 39): "Crédit Lyonnais suspendu (avis 2003-1483), Pernod Ricard entre le 11-07-2003 "
                                      "(avis 2003-2057)",
    ("2003-10-01", "2003-11-20", 39): "Orange SA suspendue (avis 2003-3086), Arcelor entre le 21-11-2003 (avis 2003-3549)",
    ("2004-06-21", "2004-09-30", 39): "Aventis « provisoirement retirée » (avis 2004-1786), Publicis entre le 01-10-2004",
    ("2006-06-19", "2006-09-15", 39): "Arcelor : « l'indice CAC40 sera donc provisoirement constitué de 39 valeurs à "
                                      "compter du 19 juin 2006 » (avis 2006-1694)",
    ("2007-04-11", "2007-06-15", 39): "AGF suspendue le 11-04-2007 (colonne de bnains, avis absent)",
    ("2008-07-22", "2008-09-19", 39): "Suez retirée « as from the market close of 21 July » (avis 363871), Suez "
                                      "Environnement entre le 22-09-2008 (avis 381663)",
    ("2010-07-02", "2010-07-02", 41): "« Both Accor and Edenred will be included in the CAC40 » (avis 2010-097)",
    ("2019-05-03", "2019-06-21", 41): "Worldline entre le 03-05-2019 selon la colonne de bnains, AUCUN AVIS TROUVÉ : "
                                      "à vérifier",
}
# LES DATES DE BNAINS QUE L'AVIS CORRIGE DE PLUS DE TROIS JOURS — (date de bnains, événement, séance d'effet de l'avis),
# chacune confirmée dans l'avis par la relecture du 12-10-2026 (« Effective Date: Monday 23 June 2014 » pour Vallourec,
# « prendront effet le 18 septembre 2017 » pour Nokia et STMicroelectronics…). Écrit À LA MAIN. Une date d'effet qui
# glisse (un an de trop, une phrase d'un autre indice) s'écarte de bnains et change cette liste : le code devient 1,
# même quand le compte reste à 40.
ECARTS_A_LA_COLONNE = {
    ("2014-06-18", "Retrait", "2014-06-23"), ("2015-03-18", "Retrait", "2015-03-23"),
    ("2017-03-18", "Retrait", "2017-09-18"), ("2017-03-20", "Admission", "2017-09-18"),
    ("2018-06-24", "Admission", "2019-06-24"), ("2020-06-22", "Admission", "2020-09-21"),
}
NOTE_D_EFFET = re.compile(r"(\d\d)/(\d\d)/(\d{4}) (avant l'ouverture|à l'ouverture|après la clôture)")


def _charger(nom):
    """Importe un programme du dossier programmes/ par son chemin.

    ① RÔLE — Lire le calendrier des séances et les contrats sans recopier leur code (R-708).
    ② CONTEXTE D'APPEL — À l'import de ce module, deux fois.
    ③ ENTRÉE — `nom` : le nom du programme, sans « .py ».
    ④ CONDITIONS D'ENTRÉE — Le programme est dans ../../programmes/ par rapport à ce fichier.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, par le chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves copient ce fichier avec le dossier programmes/ ; l'import par le chemin y trouve la copie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le programme chargé (des déclarations seulement).
    ⑪ TERMINAISON — Rend la main ou lève l'erreur d'import.
      [sort: non]
    """
    chemin = os.path.join(ICI, "..", "..", "programmes", nom + ".py")
    spec = importlib.util.spec_from_file_location(f"{nom}_compo", chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CAL = _charger("CALENDRIER_DE_LA_BOURSE")
CONTRATS = _charger("CONTRATS_DES_FICHIERS")


def isin_du_sicovam(code):
    """Rend le code ISIN français qui correspond à un ancien code Sicovam.

    ① RÔLE — Donner un code ISIN aux lignes que bnains ne connaît que par leur code Sicovam (avant 2003).
    ② CONTEXTE D'APPEL — `lire_l_historique`, `lire_la_composition_initiale`.
    ③ ENTRÉE — `code` : le code Sicovam, de 3 à 6 chiffres.
    ④ CONDITIONS D'ENTRÉE — Une société française : pour une société étrangère, le code obtenu est faux (Equant, 12701,
      est NL0000200889) ; les appelants préfèrent alors le code ISIN que bnains écrit à côté.
    ⑤ SORTIE — UNE valeur : le code ISIN, « FR » puis le Sicovam sur 9 chiffres puis la clé de contrôle.
      [rend: 1]
    ⑥ TRAITEMENT — la règle de la clé de contrôle des codes ISIN (lettres changées en nombres, doublement d'un chiffre
      sur deux en partant de la droite, somme des chiffres, complément à dix).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Vérifié le 11-10-2026 sur cinq paires dont les deux codes sont connus (Vinci 12548 → FR0000125486,
      Crédit Agricole 4507 → FR0000045072, Vivendi Environnement 12414, Pernod Ricard 12069, Accor 12040).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    base = "FR" + code.zfill(9)
    chiffres = "".join(str(int(c, 36)) for c in base)
    total = 0
    for i, c in enumerate(reversed(chiffres)):
        n = int(c) * (2 if i % 2 == 0 else 1)
        total += n // 10 + n % 10
    return base + str((10 - total % 10) % 10)


def _texte(fragment):
    """Rend le texte d'un morceau de page, sans balises ni blancs répétés.

    ① RÔLE — Une seule façon de lire une case de tableau.
    ② CONTEXTE D'APPEL — `lire_l_historique`, `lire_la_composition_initiale`.
    ③ ENTRÉE — `fragment` : du texte HTML.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — retirer les balises, décoder les entités, réduire les blancs.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()


def lire_la_composition_initiale(page):
    """Lit la composition du CAC 40 au 03-01-2000, telle que la rend l'outil de bnains.

    ① RÔLE — Le point de départ du rejeu.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `page` : le texte de la page COMPOSITION_INITIALE.
    ④ CONDITIONS D'ENTRÉE — La page porte « Liste des 40 valeurs du CAC40 au 3/1/2000 » et 40 lignes (ValueError
      sinon).
    ⑤ SORTIE — DEUX valeurs : {code ISIN : libellé}, et {code Sicovam : code ISIN} pour les lignes dont bnains donne
      les deux codes.
      [rend: 2]
    ⑥ TRAITEMENT — lire chaque ligne (ISIN, Sicovam, libellé) ; un ISIN « na » est tiré du Sicovam.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les événements d'avant 2003 ne portent que le Sicovam : la table Sicovam → ISIN donne le bon code aux
      sociétés étrangères (Equant, Dexia, STMicroelectronics).
    ⑨ CE QUI CLOCHE — Quatre lignes portent « na » chez bnains (Aerospatiale Matra, CCF, Legrand, Vivendi) : leur
      ISIN est tiré du Sicovam, donc calculé et non lu.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    if not re.search(r"Liste des 40 valeurs du CAC40 au 3/1/2000", page):
        raise ValueError("composition initiale : en-tête « 40 valeurs au 3/1/2000 » absent")
    init, sico = {}, {}
    for r in re.split(r"<tr[\s>]", page.split("<tbody>", 1)[1])[1:]:
        c = [_texte(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
        if len(c) < 3:
            continue
        isin = c[0] if c[0] != "na" else isin_du_sicovam(c[1])
        init[isin] = c[2]
        if c[0] != "na":
            sico[c[1]] = c[0]
    if len(init) != 40:
        raise ValueError(f"composition initiale : {len(init)} lignes au lieu de 40")
    return init, sico


def lire_l_historique(page, sico):
    """Lit chaque admission, retrait ou suspension de l'historique de bnains.

    ① RÔLE — Transformer la page de l'historique en une liste d'événements.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `page` : le texte de la page HISTORIQUE · `sico` : {Sicovam : ISIN} de la composition initiale.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des événements, dans l'ordre de la page ; chacun {date, evenement, code, isin,
      origine_isin, libelle, note, avis} ; `avis` réunit les liens d'avis de la ligne, séparés par « | ».
      [rend: 1]
    ⑥ TRAITEMENT — découper la page à chaque case de date (et non à chaque balise de ligne : des lignes de bnains n'ont
      pas de balise de fin) ; dans chaque morceau, le code, le libellé, la note, les liens ; l'ISIN est le code
      lui-même, sinon le lien du nom pour un code étranger, sinon la table Sicovam, sinon le calcul.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Mesuré le 11-10-2026 : découper aux balises de ligne perdait les événements de 2006 à 2009, et une
      case « 20/03/2017 style=… » (une faute de la page) perdait l'entrée d'Atos.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    pos = [m.start() for m in re.finditer(r"<td[^>]*>\s*\d\d/\d\d/\d{4}[^<]*</td>", page)]
    out = []
    for i, p in enumerate(pos):
        bloc = page[p: pos[i + 1] if i + 1 < len(pos) else len(page)]
        cellules = re.findall(r"<td[^>]*>(.*?)</td>", bloc, re.S)
        c = [_texte(x) for x in cellules]
        jour, typ = c[0][:10], c[1]
        reste = c[2:]
        code = next((x for x in reste if re.fullmatch(r"[A-Z]{2}[0-9A-Z]{9}[0-9]|\d{3,6}|\?", x)), "")
        k = reste.index(code) if code in reste else -1
        apres = [x for x in reste[k + 1:] if x] if k >= 0 else [x for x in reste if x]
        libelle = apres[0] if apres else ""
        note = re.sub(r"\s(19|20)\d\d$", "", " ".join(apres[1:]))
        lien_nom = []
        j = [n for n, x in enumerate(cellules) if _texte(x) == code]
        if j and j[0] + 1 < len(cellules):
            lien_nom = re.findall(r"codeISIN=([A-Z0-9]{12})", cellules[j[0] + 1])
        if re.fullmatch(r"[A-Z]{2}[0-9A-Z]{9}[0-9]", code):
            isin, origine = code, "code de bnains"
        elif lien_nom and re.fullmatch(r"\d{3,6}", code) and not lien_nom[0].startswith("FR"):
            isin, origine = lien_nom[0], "lien du nom (code étranger)"
        elif code in sico:
            isin, origine = sico[code], "Sicovam de la composition du 03-01-2000"
        elif re.fullmatch(r"\d{3,6}", code):
            isin, origine = isin_du_sicovam(code), "CALCULÉ depuis le Sicovam"
        else:
            isin, origine = "", ""
        jj, mm, aa = jour.split("/")
        liens = sorted(set(x for x in re.findall(r'href="([^"]+)"', bloc) if "avis/" in x))
        out.append({"date": f"{aa}-{mm}-{jj}", "evenement": typ, "code": code, "isin": isin, "origine_isin": origine,
                    "libelle": libelle, "note": note[:300], "avis": "|".join(liens)})
    return out


def nom_du_temoin(lien):
    """Rend le nom de fichier sous lequel un avis est gardé.

    ① RÔLE — Une seule façon de nommer un avis gardé.
    ② CONTEXTE D'APPEL — `telecharger`, `dates_d_effet`.
    ③ ENTRÉE — `lien` : le lien relatif de bnains, par exemple « avis/2010-097.pdf ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom, caractères hors lettres, chiffres, point, tiret et souligné remplacés par « _ ».
      [rend: 1]
    ⑥ TRAITEMENT — dernier élément du lien, caractères remplacés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Des noms d'avis de bnains portent des espaces et des crochets.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return re.sub(r"[^A-Za-z0-9_.-]", "_", lien.split("/")[-1])


def dates_d_effet(texte, annee, seances):
    """Rend les dates d'effet qu'un avis officiel écrit, chacune ramenée à la première séance de la composition neuve.

    ① RÔLE — Lire, dans un avis d'Euronext, à partir de quand une admission ou un retrait s'applique.
    ② CONTEXTE D'APPEL — `dater`, une fois par avis d'un événement.
    ③ ENTRÉE — `texte` : le texte de l'avis · `annee` : l'année à prendre quand la phrase n'en donne pas · `seances` :
      la liste triée des séances.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la liste triée des séances trouvées (vide si aucune phrase ne se lit), et la liste triée
      des jours écrits au-delà de la dernière séance du calendrier.
      [rend: 2]
    ⑥ TRAITEMENT — chercher chaque PHRASE_D_EFFET ; un jour « à l'issue de la séance du » ou « after markets close on »
      donne la séance suivante ; les autres donnent la première séance à partir du jour écrit.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Mesuré le 12-10-2026 sur les 52 avis gardés : une date d'effet au moins se lit dans 51 ; la colonne
      de bnains se trompe de plus de trois jours 6 fois (Thales revient le 24-06-2019, bnains écrivait 2018 ; Nokia et
      STMicroelectronics le 18-09-2017, bnains écrivait mars 2017).
    ⑨ CE QUI CLOCHE — Une date au-delà de la dernière séance du calendrier n'a pas de séance : elle est rendue à part
      (relecture du 12-10-2026 : l'annonce de la révision de décembre bloquait tout le relevé, puis, jetée sans bruit,
      laissait l'événement daté par bnains) ; `dater` marque alors l'événement « à venir ». Une date impossible
      (« 31 juin ») est sautée. · L'avis 2000-2735 (CCF) écrit « sortie de l'indice CAC 40 … le 26 juin 2000 » : cette phrase ne se lit
      pas (« le » seul attraperait toutes les dates d'un avis) ; la date vient alors de bnains, et la relecture du
      12-10-2026 l'a trouvée juste. · L'avis 2002-2789 est daté du 29 août 2002 et écrit « A compter du 6 août2002 » :
      un effet antérieur à la publication, lu tel quel, à vérifier.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    texte = re.sub(r"\s+", " ", texte)
    out, au_dela = set(), set()
    for x in PHRASE_D_EFFET.finditer(texte):
        mois = MOIS.get(x.group(3).lower())
        if not mois:
            continue
        try:
            d = date(int(x.group(4)) if x.group(4) else annee, mois, int(x.group(2)))
        except ValueError:
            continue
        fin_de_seance = "issue" in x.group(1).lower() or "close" in x.group(1).lower()
        seance = next((s for s in seances if (s > d if fin_de_seance else s >= d)), None)
        if seance is not None:
            out.add(seance)
        else:
            au_dela.add(d)
    return sorted(out), sorted(au_dela)


def date_de_publication(texte):
    """Rend la date de publication qu'écrit l'en-tête d'un avis, ou None.

    ① RÔLE — Voir qu'une date d'effet précède la publication de l'avis qui la donne.
    ② CONTEXTE D'APPEL — `dater`, une fois par avis lu.
    ③ ENTRÉE — `texte` : le texte de l'avis.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la date, ou None quand l'en-tête ne la donne pas sous une forme connue (PUBLICATION).
      [rend: 1]
    ⑥ TRAITEMENT — la première date de la première forme de PUBLICATION, sinon de la seconde.
    ⑦ UNITÉ — Un jour du calendrier, pas une séance.
    ⑧ POURQUOI — Relecture du 12-10-2026 : l'avis 2002-2789, publié le 29 août 2002, écrit « A compter du 6 août2002 » ;
      la table donnait cette date comme « avis officiel », sans réserve.
    ⑨ CE QUI CLOCHE — Les communiqués de 2015 à 2025 n'ont ni « Issue Date » ni numéro « N° » : leur date n'est pas
      lue.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    texte = re.sub(r"\s+", " ", texte)
    m = PUBLICATION[0].search(texte) or PUBLICATION[1].search(texte)
    if not m or not MOIS.get(m[2].lower()):
        return None
    try:
        return date(int(m[3]), MOIS[m[2].lower()], int(m[1]))
    except ValueError:
        return None


def avis_annules(dossier, inscrits):
    """Rend les noms des avis gardés qu'un autre avis gardé annule.

    ① RÔLE — Ne jamais dater un événement par un avis annulé.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `dossier` : le dossier des témoins · `inscrits` : les noms inscrits au registre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des noms de fichiers PDF annulés.
      [rend: 1]
    ⑥ TRAITEMENT — chercher ANNULE dans chaque texte inscrit ; un avis gardé est annulé quand son numéro, lu dans son
      texte (NUMERO_D_AVIS, le premier trouvé), est celui que désigne la phrase.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture à mandat inversé du 12-10-2026 : l'avis 2000-5128 (Canal+ remplacée par Dassault Systèmes
      le 21-12-2000) est annulé par le 2000-5131, qui ne cite plus Dassault ; la table donnait pourtant le 5128 comme
      preuve de l'entrée de Dassault.
    ⑨ CE QUI CLOCHE — Un avis annulé par un avis que bnains n'a pas gardé n'est pas vu. · Un avis sans numéro lisible
      dans son texte (les communiqués de 2015 à 2025, « 220869.pdf ») ne peut pas être reconnu comme annulé. · Deux
      annulations visent des avis non gardés (2006-1694 annule le 2006-1691, 2003-1483 le 2003-1468) : sans effet.
    ⑩ EFFET — Lit les textes.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    vises, numero = set(), {}
    for nom in inscrits:
        if nom.endswith(".pdf.txt"):
            with open(os.path.join(dossier, nom), encoding="utf-8", errors="replace") as f:
                texte = re.sub(r"\s+", " ", f.read())
            vises |= {(a, int(n)) for a, n in ANNULE.findall(texte)}
            m = NUMERO_D_AVIS.search(texte)
            if m:
                numero[nom[:-4]] = (m[1], int(m[2]))
    return {nom for nom, n in numero.items() if n in vises}


def dater(evenements, dossier, seances, inscrits, annules):
    """Donne à chaque événement depuis le 03-01-2000 sa séance d'effet, et dit d'où elle vient.

    ① RÔLE — Dater chaque entrée et chaque sortie à la séance où la composition change.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `evenements` : le rendu de `lire_l_historique` · `dossier` : le dossier des témoins · `seances` : la liste
      triée des séances · `inscrits` : les noms inscrits au registre (seuls lus) · `annules` : les avis annulés (jamais
      lus).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des événements depuis DEBUT, chacun complété de `effet` (AAAA-MM-JJ, vide pour un
      événement au-delà de la dernière séance du calendrier — par la colonne de bnains ou par une date de son avis —,
      dont `origine_date` commence par A_VENIR), `origine_date`,
      `dates_de_l_avis` et `avis_de_la_date` (le nom de l'avis qui a donné la date, vide sinon) ; quand la date choisie
      précède la date de publication de son avis, `origine_date` le dit (avis 2002-2789 : publié le 29-08-2002, effet
      « A compter du 6 août2002 »).
      [rend: 1]
    ⑥ TRAITEMENT — ① la date de l'avis la plus proche de la colonne de bnains · ② à défaut, la date d'une note « le
      JJ/MM/AAAA avant l'ouverture » (ou « à l'ouverture » ; « après la clôture » donne la séance suivante) · ③ à défaut,
      la colonne de bnains ; un retrait encore sans source prend la séance
      de l'unique admission de la séance suivante.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Ni la colonne de bnains ni ses notes ne sont sûres seules : la colonne écrit 2018 pour Thales (avis :
      24-06-2019), la note écrit 19/09/2011 pour Legrand (avis : 19 décembre 2011). L'avis officiel tranche.
    ⑨ CE QUI CLOCHE — L'appariement d'un retrait à l'admission suivante est une convention : il donne le 18-01-2021 à la
      sortie de Peugeot (dernière séance le 15-01-2021) et le 23-12-2024 à celle de Vivendi, dont les avis manquent chez
      bnains. · « La date de l'avis la plus proche de la colonne de bnains » est une règle, pas une lecture : un avis qui
      cite plusieurs dates (une autre valeur, un autre indice) donnerait la mauvaise si la colonne de bnains était
      elle-même fausse — relecture du 12-10-2026 : l'avis 2003-1483 cite aussi le 02-06-2003, un changement de code
      pour le SBF 250.
    ⑩ EFFET — Lit les textes des avis gardés et inscrits.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    garde = lambda d: next((s for s in seances if s >= d), None)
    rang = {s: i for i, s in enumerate(seances)}
    ev = [dict(e) for e in evenements if e["date"] >= DEBUT.isoformat()]
    for e in ev:
        colonne = garde(date.fromisoformat(e["date"]))
        if colonne is None:
            e.update(effet="", origine_date=A_VENIR, dates_de_l_avis="", avis_de_la_date="")
            continue
        trouvees, etat, publie, futures = [], "absent", {}, []
        for lien in filter(None, e["avis"].split("|")):
            nom = nom_du_temoin(lien)
            if nom in annules:
                etat = "annulé" if etat == "absent" else etat
                continue
            if nom + ".txt" in inscrits:
                etat = "illisible"
                with open(os.path.join(dossier, nom + ".txt"), encoding="utf-8", errors="replace") as f:
                    texte = f.read()
                lues, plus_tard = dates_d_effet(texte, colonne.year, seances)
                trouvees += [(d, nom) for d in lues]
                futures += plus_tard
                publie[nom] = date_de_publication(texte)
        trouvees = sorted(set(trouvees))
        e["dates_de_l_avis"] = " ".join(sorted({d.isoformat() for d, _ in trouvees} | {d.isoformat() for d in futures}))
        e["avis_de_la_date"] = ""
        if futures:
            e.update(effet="", origine_date=A_VENIR + f" (l'avis annonce le {max(futures).isoformat()})")
            continue
        if trouvees:
            meilleure, nom = min(trouvees, key=lambda x: (abs((x[0] - colonne).days), x[0], x[1]))
            e["effet"], e["avis_de_la_date"] = meilleure.isoformat(), nom
            e["origine_date"] = "avis officiel" + ("" if abs((meilleure - colonne).days) <= 3
                                                   else f" (bnains écrivait {e['date']})")
            if publie.get(nom) and meilleure < publie[nom]:
                e["origine_date"] += f" (effet antérieur à la publication du {publie[nom].isoformat()} : à vérifier)"
            continue
        m = NOTE_D_EFFET.search(e["note"])
        if m:
            jour = date(int(m[3]), int(m[2]), int(m[1]))
            effet = next((s for s in seances if s > jour), None) if "clôture" in m[4] else garde(jour)
            e["effet"] = effet.isoformat() if effet else ""
            e["origine_date"] = "note de bnains, avis " + etat if effet else A_VENIR
        else:
            e["effet"] = colonne.isoformat()
            e["origine_date"] = "colonne de bnains, avis " + etat
    for e in ev:
        if e["evenement"] == "Retrait" and e["origine_date"].startswith("colonne"):
            suivantes = [a for a in ev if a["evenement"] == "Admission" and a["effet"]
                         and 0 < rang[date.fromisoformat(a["effet"])] - rang[date.fromisoformat(e["effet"])] <= 1]
            if len(suivantes) == 1:
                e["effet"] = suivantes[0]["effet"]
                e["origine_date"] += f", apparié à l'admission de {suivantes[0]['libelle']}"
    return ev


def rejouer(initiale, evenements, seances):
    """Rejoue la composition de l'indice séance par séance.

    ① RÔLE — Reconstituer qui était dans l'indice à chaque séance.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `initiale` : {ISIN : libellé} au 03-01-2000 · `evenements` : le rendu de `dater` · `seances` : la liste
      triée des séances, depuis DEBUT.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : {séance : ensemble des ISIN}, et la liste des événements sans effet (un retrait d'une
      ligne déjà absente).
      [rend: 2]
    ⑥ TRAITEMENT — à chaque séance, appliquer les retraits puis les admissions qui y prennent effet ; une suspension
      retire ; une fin de suspension réadmet.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Le compte de 40 à chaque séance est la propriété qui prouve le relevé, sans liste à tenir.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    par_seance = defaultdict(list)
    for e in evenements:
        par_seance[e["effet"]].append(e)
    etat, membres, sans_effet = set(initiale), {}, []
    for s in seances:
        for e in sorted(par_seance.get(s.isoformat(), []), key=lambda x: x["evenement"] != "Retrait"):
            if e["evenement"] in ("Admission", "Fin de suspension"):
                etat.add(e["isin"])
            elif e["isin"] in etat:
                etat.discard(e["isin"])
            else:
                sans_effet.append(e)
        membres[s] = frozenset(etat)
    return membres, sans_effet


def passages(membres, libelles):
    """Rend les passages : chaque suite continue de séances où une ligne était dans l'indice.

    ① RÔLE — Tirer les entrées et sorties de la composition rejouée.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `membres` : le premier rendu de `rejouer` · `libelles` : {ISIN : libellé de bnains}.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des passages {isin_bnains, libelle_bnains, premiere_seance, derniere_seance},
      triée par libellé puis date ; `derniere_seance` vide pour une ligne encore dans l'indice.
      [rend: 1]
    ⑥ TRAITEMENT — parcourir les séances, ouvrir un passage à l'apparition, le fermer à la disparition.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    seances = sorted(membres)
    ouverts, out, avant = {}, [], frozenset()
    for i, s in enumerate(seances):
        for x in membres[s] - avant:
            ouverts[x] = s
        for x in avant - membres[s]:
            out.append((x, ouverts.pop(x), seances[i - 1]))
        avant = membres[s]
    out += [(x, a, None) for x, a in ouverts.items()]
    lignes = [{"isin_bnains": x, "libelle_bnains": libelles.get(x, ""), "premiere_seance": a.isoformat(),
               "derniere_seance": b.isoformat() if b else ""} for x, a, b in out]
    return sorted(lignes, key=lambda r: (r["libelle_bnains"].lower(), r["premiere_seance"]))


def preuves(lignes, evenements, initiale, seances):
    """Ajoute à chaque passage la preuve de sa première et de sa dernière séance.

    ① RÔLE — Dire, pour chaque date d'un passage, d'où elle vient.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `lignes` : le rendu de `passages` · `evenements` : le rendu de `dater` · `initiale` : {ISIN : libellé}
      au 03-01-2000 · `seances` : la liste triée des séances.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les mêmes passages, chacun complété de `preuve_entree` et `preuve_sortie`.
      [rend: 1]
    ⑥ TRAITEMENT — l'entrée : la composition du 03-01-2000 pour une ligne présente ce jour-là, sinon l'admission (ou
      la fin de suspension) qui prend effet à la première séance ; la sortie : le retrait (ou la suspension) qui prend
      effet à la séance qui suit la dernière ; chaque preuve nomme l'avis qui a donné la date, sinon l'avis que cite
      bnains (« cité par bnains » : non gardé, annulé ou sans date lisible), et l'origine de la date.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une date sans sa preuve ne se contrôle pas : la table des passages doit se relire seule (R-751 ④).
    ⑨ CE QUI CLOCHE — Un passage dont aucun événement ne prend effet à la bonne séance porte « aucun événement trouvé »
      — c'est le cas d'une sortie dont la date vient d'un appariement mal tombé.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rang = {s.isoformat(): i for i, s in enumerate(seances)}

    def dire(liste):
        """Rend la preuve écrite d'un événement trouvé, ou « aucun événement trouvé ».

        ① RÔLE — Une seule façon d'écrire une preuve.
        ② CONTEXTE D'APPEL — `preuves`.
        ③ ENTRÉE — `liste` : les événements qui conviennent.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le texte.
          [rend: 1]
        ⑥ TRAITEMENT — le nom de l'avis qui a donné la date ; à défaut, le premier avis que cite bnains, suivi de
          « (cité par bnains) » ; à défaut, « aucun avis » ; puis l'origine de la date, qui dit si l'avis est absent,
          annulé ou illisible.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if not liste:
            return "aucun événement trouvé"
        e = liste[0]
        if e["avis_de_la_date"]:
            return f"{e['avis_de_la_date']} — {e['origine_date']}"
        avis = [nom_du_temoin(x) for x in e["avis"].split("|") if x]
        return f"{avis[0] + ' (cité par bnains)' if avis else 'aucun avis'} — {e['origine_date']}"

    for p in lignes:
        if p["premiere_seance"] == seances[0].isoformat() and p["isin_bnains"] in initiale:
            p["preuve_entree"] = "déjà dans l'indice le 03-01-2000 (composition de bnains du 03-01-2000)"
        else:
            p["preuve_entree"] = dire([e for e in evenements if e["isin"] == p["isin_bnains"]
                                       and e["effet"] == p["premiere_seance"]
                                       and e["evenement"] in ("Admission", "Fin de suspension")])
        if not p["derniere_seance"]:
            p["preuve_sortie"] = ""
            continue
        suivante = seances[rang[p["derniere_seance"]] + 1].isoformat()
        p["preuve_sortie"] = dire([e for e in evenements if e["isin"] == p["isin_bnains"] and e["effet"] == suivante
                                   and e["evenement"] not in ("Admission", "Fin de suspension")])
    return lignes


def verifier_les_temoins(dossier):
    """Confronte chaque témoin à son empreinte inscrite au registre.

    ① RÔLE — Ne jamais calculer sur un témoin changé.
    ② CONTEXTE D'APPEL — `relever`.
    ③ ENTRÉE — `dossier` : le dossier des témoins.
    ④ CONDITIONS D'ENTRÉE — REGISTRE.csv existe (colonnes fichier, adresse, sha256, octets, releve_le).
    ⑤ SORTIE — UNE valeur : l'ensemble des noms inscrits ; lève ValueError si le registre a changé, au premier écart,
      au premier absent, ou pour un fichier du dossier que le registre ne porte pas.
      [rend: 1]
    ⑥ TRAITEMENT — l'empreinte du registre, comparée à EMPREINTE_DU_REGISTRE ; l'empreinte SHA-256 de chaque fichier
      inscrit, comparée ; puis chaque fichier du dossier, cherché au registre.
    ⑦ UNITÉ — Des fichiers.
    ⑧ POURQUOI — Une preuve qui peut changer sans bruit n'en est pas une (même geste que le registre des documents des
      droits, temoins/DOCUMENTS_DES_DROITS_REGLE_OFFICIELLE_Sam_10-10-2026/DOCUMENTS.csv). Relecture du 12-10-2026 : un
      texte d'avis ajouté hors registre était lu et déplaçait la sortie de Sodexo au 22-09-2020, sans code 2.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les fichiers.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    with open(os.path.join(dossier, "REGISTRE.csv"), "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()
    if empreinte != EMPREINTE_DU_REGISTRE:
        raise ValueError(f"le registre des témoins a changé (empreinte {empreinte}) : relire les témoins nouveaux, puis "
                         "recopier cette empreinte dans EMPREINTE_DU_REGISTRE")
    inscrits = set()
    with open(os.path.join(dossier, "REGISTRE.csv"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            chemin = os.path.join(dossier, r["fichier"])
            if not os.path.exists(chemin):
                raise ValueError(f"témoin absent : {r['fichier']}")
            with open(chemin, "rb") as g:
                if hashlib.sha256(g.read()).hexdigest() != r["sha256"]:
                    raise ValueError(f"témoin changé : {r['fichier']}")
            inscrits.add(r["fichier"])
    for nom in os.listdir(dossier):
        if nom != "REGISTRE.csv" and nom not in inscrits:
            raise ValueError(f"fichier hors registre dans les témoins : {nom}")
    return inscrits


def telecharger(dossier):
    """Relève sur bnains.org la page de l'historique, la composition du 03-01-2000 et les avis, et les garde.

    ① RÔLE — Fabriquer les témoins, avec leur registre.
    ② CONTEXTE D'APPEL — `main`, avec « --telecharger » seulement.
    ③ ENTRÉE — `dossier` : le dossier des témoins.
    ④ CONDITIONS D'ENTRÉE — Le réseau atteint bnains.org ; pdftotext est installé.
    ⑤ SORTIE — Ne rend rien : écrit les fichiers et REGISTRE.csv.
      [rend: rien]
    ⑥ TRAITEMENT — ① la page de l'historique · ② la composition au 03/01/2000 (formulaire de compocac.php) · ③ chaque
      avis lié depuis 2000, gardé s'il commence par « %PDF », et son texte par pdftotext · ④ le registre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Rejouer sans réseau : le calcul ne lit que les témoins.
    ⑨ CE QUI CLOCHE — Deux avis manquent chez bnains (relevé le 11-10-2026 : 20200611 et 20241217, réponse 404) : ils
      ne sont pas gardés, et les événements qui les citent sont datés par la colonne de bnains.
    ⑩ EFFET — Lit le réseau ; écrit dans `dossier`.
    ⑪ TERMINAISON — Rend la main ; chaque requête est bornée à 60 secondes.
      [sort: non]
    """
    os.makedirs(dossier, exist_ok=True)

    def prendre(adresse, nom, donnees=None):
        """Télécharge une adresse dans le dossier des témoins.

        ① RÔLE — Une seule façon de télécharger.
        ② CONTEXTE D'APPEL — `telecharger`.
        ③ ENTRÉE — `adresse` · `nom` : le fichier à écrire · `donnees` : le corps d'un formulaire, ou None.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : les octets reçus, ou None en cas d'échec.
          [rend: 1]
        ⑥ TRAITEMENT — requête, écriture.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit le réseau ; écrit un fichier.
        ⑪ TERMINAISON — Rend la main ; requête bornée à 60 secondes.
          [sort: non]
        """
        try:
            req = urllib.request.Request(adresse, data=donnees, headers={"User-Agent": UA})
            octets = urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            print(f"  échec : {adresse} ({type(e).__name__})")
            return None
        with open(os.path.join(dossier, nom), "wb") as f:
            f.write(octets)
        return octets

    if prendre(ADRESSE + "histocac.php", HISTORIQUE) is None or \
            prendre(ADRESSE + "compocac.php", COMPOSITION_INITIALE, b"date_input=03/01/2000") is None:
        raise OSError("la page de l'historique ou la composition du 03-01-2000 n'a pas pu être relevée")
    with open(os.path.join(dossier, HISTORIQUE), encoding="utf-8", errors="replace") as f:
        page = f.read()
    _, sico = lire_la_composition_initiale(open(os.path.join(dossier, COMPOSITION_INITIALE), encoding="utf-8",
                                                errors="replace").read())
    liens = sorted({x for e in lire_l_historique(page, sico) if e["date"] >= DEBUT.isoformat()
                    for x in e["avis"].split("|") if x})
    lien_de = {}
    for lien in liens:
        nom = nom_du_temoin(lien)
        octets = prendre(ADRESSE + urllib.parse.quote(lien), nom)
        if not octets or not octets.startswith(b"%PDF"):
            if os.path.exists(os.path.join(dossier, nom)):
                os.remove(os.path.join(dossier, nom))
            continue
        lien_de[nom] = lien
        subprocess.run(["pdftotext", "-layout", os.path.join(dossier, nom), os.path.join(dossier, nom + ".txt")],
                       check=True, timeout=60)
        time.sleep(0.5)
    maintenant = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(dossier, "REGISTRE.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fichier", "adresse", "sha256", "octets", "releve_le"])
        for nom in sorted(os.listdir(dossier)):
            if nom == "REGISTRE.csv":
                continue
            with open(os.path.join(dossier, nom), "rb") as g:
                b = g.read()
            source = {HISTORIQUE: ADRESSE + "histocac.php",
                      COMPOSITION_INITIALE: ADRESSE + "compocac.php (date_input=03/01/2000)"}.get(
                nom, f"texte tiré de {nom[:-4]} par pdftotext -layout" if nom.endswith(".txt")
                else ADRESSE + lien_de.get(nom, "avis/" + nom))
            w.writerow([nom, source, hashlib.sha256(b).hexdigest(), len(b), maintenant])


def relever(racine):
    """Fait tout le relevé depuis les témoins, et rend ce qu'il faut écrire et dire.

    ① RÔLE — Le calcul entier, sans écrire.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : un dictionnaire {passages, evenements, membres, sans_effet, ecarts} ; `ecarts` est la liste
      des plages de séances où la composition ne compte pas 40 valeurs, chacune (première, dernière, compte).
      [rend: 1]
    ⑥ TRAITEMENT — témoins, composition initiale, historique, datation, rejeu, passages et leurs preuves, écarts.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Séparer le calcul de l'écriture permet aux épreuves de juger le calcul sans toucher au dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit les témoins et le calendrier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    dossier = os.path.join(racine, TEMOINS)
    inscrits = verifier_les_temoins(dossier)
    with open(os.path.join(dossier, COMPOSITION_INITIALE), encoding="utf-8", errors="replace") as f:
        initiale, sico = lire_la_composition_initiale(f.read())
    with open(os.path.join(dossier, HISTORIQUE), encoding="utf-8", errors="replace") as f:
        historique = lire_l_historique(f.read(), sico)
    seances = sorted(d for d in CAL.lire_les_seances(racine)["indice"] if d >= DEBUT)
    ev = dater(historique, dossier, seances, inscrits, avis_annules(dossier, inscrits))
    membres, sans_effet = rejouer(initiale, ev, seances)
    libelles = dict(initiale)
    for e in ev:
        libelles.setdefault(e["isin"], e["libelle"])
    ecarts = []
    for i, s in enumerate(seances):
        n = len(membres[s])
        if n == 40:
            continue
        if ecarts and ecarts[-1][2] == n and seances.index(ecarts[-1][1]) == i - 1:
            ecarts[-1][1] = s
        else:
            ecarts.append([s, s, n])
    lignes = preuves(passages(membres, libelles), ev, initiale, seances)
    return {"passages": lignes, "evenements": ev, "membres": membres,
            "sans_effet": sans_effet, "ecarts": ecarts}


def corrections_de_l_avis(evenements):
    """Rend les dates de bnains que l'avis a corrigées de plus de trois jours.

    ① RÔLE — Mesurer ce que compare ECARTS_A_LA_COLONNE.
    ② CONTEXTE D'APPEL — `code_de_sortie`, `main`.
    ③ ENTRÉE — `evenements` : le rendu de `dater`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des (date de bnains, événement, séance d'effet).
      [rend: 1]
    ⑥ TRAITEMENT — les événements dont `origine_date` porte « bnains écrivait ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return {(e["date"], e["evenement"], e["effet"]) for e in evenements if "bnains écrivait" in e["origine_date"]}


def code_de_sortie(ecarts, evenements):
    """Rend 0 si les écarts au compte de 40 et les corrections de bnains sont exactement ceux connus, 1 sinon.

    ① RÔLE — Faire voir au code de sortie un écart nouveau, disparu ou déplacé, et une date d'effet qui glisse.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `ecarts` : la liste des plages (première, dernière, compte) rendue par `relever` · `evenements` : le
      rendu de `dater`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0 ou 1.
      [rend: 1]
    ⑥ TRAITEMENT — comparer l'ensemble des plages, écrites AAAA-MM-JJ, aux clés d'ECARTS_CONNUS, et les corrections de
      l'avis à ECARTS_A_LA_COLONNE.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ECARTS_CONNUS et ECARTS_A_LA_COLONNE. Relecture du 12-10-2026 : un an de décalage sur une paire
      retrait-admission gardait le compte à 40 et le code à 0.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    plages = {(a.isoformat(), b.isoformat(), n) for a, b, n in ecarts}
    return 0 if plages == set(ECARTS_CONNUS) and corrections_de_l_avis(evenements) == ECARTS_A_LA_COLONNE else 1


def main(argv):
    """Relève, écrit SORTIE, affiche le compte rendu.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la racine, puis « --telecharger » éventuellement.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie (0, 1 ou 2, voir l'en-tête).
      [rend: 1]
    ⑥ TRAITEMENT — télécharger si demandé, relever, écrire, afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit SORTIE ; affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    args = [a for a in argv if not a.startswith("--")]
    racine = args[0] if args else "."
    try:
        if "--telecharger" in argv:
            telecharger(os.path.join(racine, TEMOINS))
        r = relever(racine)
    except (OSError, ValueError, StopIteration, IndexError, KeyError, subprocess.SubprocessError) as e:
        print(f"RELEVÉ IMPOSSIBLE : {type(e).__name__} : {e}")
        return 2
    os.makedirs(os.path.dirname(os.path.join(racine, SORTIE)), exist_ok=True)
    with open(os.path.join(racine, SORTIE), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CONTRATS.PASSAGES_DANS_LE_CAC40)
        w.writeheader()
        w.writerows(r["passages"])
    print(f"{len(r['passages'])} passages, {len({p['isin_bnains'] for p in r['passages']})} lignes de cotation → {SORTIE}")
    for e in r["evenements"]:
        if not e["origine_date"].startswith("avis officiel") or "écrivait" in e["origine_date"]:
            print(f"  DATE : {e['date']} {e['evenement']} {e['libelle']} → {e['effet']} ({e['origine_date']})")
    for e in r["sans_effet"]:
        print(f"  SANS EFFET : {e['date']} {e['evenement']} {e['libelle']} (déjà absente)")
    for a, b, n in r["ecarts"]:
        cle = (a.isoformat(), b.isoformat(), n)
        print(f"  COMPTE {n} du {a} au {b} — " + ECARTS_CONNUS.get(cle, "ÉCART INCONNU"))
    for cle in sorted(set(ECARTS_CONNUS) - {(a.isoformat(), b.isoformat(), n) for a, b, n in r["ecarts"]}):
        print(f"  ÉCART CONNU DISPARU : {cle}")
    for cle in sorted(corrections_de_l_avis(r["evenements"]) ^ ECARTS_A_LA_COLONNE):
        print(f"  CORRECTION DE BNAINS INATTENDUE OU DISPARUE : {cle}")
    for e in r["evenements"]:
        if not e["effet"]:
            print(f"  À VENIR : {e['date']} {e['evenement']} {e['libelle']} (hors du rejeu)")
    code = code_de_sortie(r["ecarts"], r["evenements"])
    sur_bnains = sum(1 for v in ECARTS_CONNUS.values() if "colonne de bnains" in v or "AUCUN AVIS" in v)
    print(f"ÉCARTS AU COMPTE DE 40 : {len(r['ecarts'])} — " + (
        f"tous connus, dont {sur_bnains} expliqués en partie par bnains seul (à vérifier)" if code == 0
        else "DIFFÉRENTS DES ÉCARTS CONNUS"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
