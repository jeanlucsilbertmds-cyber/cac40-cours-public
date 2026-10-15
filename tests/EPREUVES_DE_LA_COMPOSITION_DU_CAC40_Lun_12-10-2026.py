#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_COMPOSITION_DU_CAC40 — Lun 12-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que etudes/outils/RELEVER_LA_COMPOSITION_DU_CAC40.py date juste les entrées et sorties du CAC 40
  depuis le 03-01-2000, SUR DES RÉPONSES ÉCRITES À LA MAIN tirées des avis officiels d'Euronext, et que chaque
  épreuve a des dents.
② CONTEXTE D'APPEL — À la main, avant toute livraison qui touche ce programme (R-731) :
  python3 tests/EPREUVES_DE_LA_COMPOSITION_DU_CAC40_Lun_12-10-2026.py <racine du dépôt> [--saboter]
  [--seulement=S1,S6]
③ ENTRÉE — La racine du dépôt, qui porte les témoins (temoins/COMPOSITION_DU_CAC40_Lun_12-10-2026/), l'indice
  (donnees/sources_indice/INDICE_CAC40.csv) et la liste d'Euronext (donnees/CALENDRIER_EURONEXT.csv).
④ CONDITIONS D'ENTRÉE — Les témoins tels qu'inscrits à leur registre le 12-10-2026.
⑤ SORTIE — UNE valeur : le code de sortie — 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au
  moins une épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus, ou si une épreuve est tombée sur une panne de
  l'environnement (PANNES : disque plein…), qui ne juge rien.
  [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis pour chaque sabotage : copier le programme et ses deux dépendances dans un dossier
  jetable (etudes/outils/ et programmes/, comme au dépôt), y appliquer le sabotage, importer la copie, jouer C1 à C24.
⑦ UNITÉ — Des séances.
⑧ POURQUOI — Décision de Jean-Luc du 11-10-2026 à 22h57 (« Oui » : construire les deux tables de la règle I-3) et
  du 12-10-2026 à 07h47 (« Oui dépose les »). R-731 : tout code passe des épreuves sabotées.
  LES ÉPREUVES (chaque date vient d'un avis officiel gardé, sauf mention) :
  C1 93 passages, sur 80 codes ISIN (mesuré par le prototype du 11-10-2026, avant ce programme) ;
  C2 Aventis (FR0000130460) : du 03-01-2000 au 18-06-2004 — avis 2004-1786, « provisoirement retirée … à l'issue de
     la séance du 18 juin 2004 » ; son entrée est prouvée par la composition du 03-01-2000, sa sortie par l'avis
     (gardé sous le nom 0_4245_1626_53424_195930125_00.pdf) ;
  C3 Thales (FR0000121329) revient le 24-06-2019 (avis du 13-06-2019 ; bnains écrivait 2018) ;
  C4 Peugeot (FR0000121501) : dernière séance le 15-01-2021 ; Stellantis (NL00150001Q9) entre le 18-01-2021 ;
  C5 Vivendi (FR0000127771) : dernière séance le 20-12-2024 ; Bureau Veritas (FR0006174348) entre le 23-12-2024 ;
  C6 EADS est rangée sous son code néerlandais NL0000235190, du 10-07-2000 à aujourd'hui ;
  C7 Edenred (FR0010908533) : un passage d'une seule séance, le 02-07-2010 (avis 2010-097 : « Both Accor and
     Edenred will be included in the CAC40 ») ;
  C8 au 02-10-2026 l'indice compte 40 lignes, et exactement 40 passages n'ont pas de dernière séance ;
  C9 les écarts au compte de 40 sont exactement les dix plages mesurées le 11-10-2026 (huit à 39, deux à 41) ;
  C10 exactement trois événements sans effet : Crédit Lyonnais (FR0000184202, 07-09-2003), Orange SA — l'opérateur
     mobile, pas France Télécom — (FR0000079196, 21-11-2003), Arcelor (LU0140205948, 18-09-2006) — chaque fois le
     retrait définitif d'une ligne déjà ôtée par sa suspension (avis 2003-1483, 2003-3086, 2006-1694) ;
  C11 un témoin changé d'un octet, un témoin effacé, un texte d'avis ajouté hors registre, le même inscrit au registre
     avec sa propre empreinte : `main` rend 2 ;
  C12 sur une copie du dépôt, `main` rend 0 (les dix écarts sont les écarts connus) et écrit un fichier dont l'en-tête
     est le contrat ; un écart déplacé d'une séance, un écart en moins, un écart en plus, une correction de bnains de
     plus : `code_de_sortie` rend 1 ;
  C13 la clé ISIN tirée du Sicovam : Vinci 12548 → FR0000125486, Crédit Agricole 4507 → FR0000045072, Vivendi
     Environnement 12414 → FR0000124141, Pernod Ricard 12069 → FR0000120693, Accor 12040 → FR0000120404 ;
  C14 DOIT ÉCHOUER : pour Equant (12701, société néerlandaise), le calcul ne donne pas NL0000200889 — et le passage
     d'Equant est bien rangé sous NL0000200889 ;
  C15 la lecture d'une phrase d'effet : « à l’ issue de la séance du 18 juin 2004 » (pdftotext met un blanc après
     l'apostrophe, avis 2004-1786) → 21-06-2004 ; « after markets close on Friday 17 September 2021 » → 20-09-2021 ;
     « Effective date: Monday 24 June 2019 » → 24-06-2019 ; un texte sans phrase → rien ; « A compter du 6 août2002 »
     (avis 2002-2789, sans blanc) → 06-08-2002 ; « à l'issue de la séance de bourse du 21 mai 2003 » (avis 2003-1483)
     → 22-05-2003 ; « as from the market close of 21 July 2008 » (avis 363871) → 22-07-2008 ;
  C16 Atos (FR0000051732) : du 20-03-2017 au 17-09-2021 (la case de date « 20/03/2017 style=… » de bnains est lue) ;
  C17 la preuve de chaque date est écrite : aucune « aucun événement trouvé » ; celle de Thales en 2019 nomme l'avis
     20190613_pr_quarterly_index_review_cac_q2_2019.pdf et dit que bnains écrivait 2018 (sans l'avis, la note de
     bnains donne aussi le 24-06-2019 : seule la preuve distingue les deux chemins) ;
  C18 la note de bnains, pour un événement sans avis : « le 07/01/2016 avant l'ouverture » → 07-01-2016 ; « … après
     la clôture » → 08-01-2016 ; une note sans date → la colonne de bnains. Sur les vraies données la note ne change
     rien (Alcatel retombe sur le 07-01-2016 par l'appariement à Nokia) : ce cas est fabriqué pour donner des dents ;
  C19 la colonne de bnains s'écarte de l'avis de plus de trois jours exactement six fois, chaque date confirmée par
     la relecture du 12-10-2026 dans l'avis : Vallourec sort le 23-06-2014, Gemalto le 23-03-2015, Nokia et
     STMicroelectronics s'échangent le 18-09-2017, Thales revient le 24-06-2019, Alstom entre le 21-09-2020 ;
  C20 l'appariement d'un retrait sans source ne joint que l'admission de la séance suivante (cas fabriqués) ;
  C21 l'avis 2000-5128 est annulé par le 2000-5131 (« Annule et remplace l'avis N°2000-5128 ») : il n'est jamais une
     preuve ; l'entrée de Dassault Systèmes le 21-12-2000 dit qu'elle vient de la colonne de bnains, avis annulé ; le
     numéro d'un avis se lit dans son texte (« N° 2000 - 5131 »), pas dans le nom du fichier ;
  C22 un avis qui annonce un effet au-delà du calendrier (« effective from Monday 21 December 2026 ») ne lève pas : la
     date n'est pas lue, l'événement est « à venir » ; une date impossible (« 31 juin 2004 ») est sautée ;
  C23 la date de publication de l'en-tête : 2002-2789 le 29-08-2002, 2010-097 le 11-06-2010, 2000-5128 le
     08-12-2000 ; l'entrée de Crédit Agricole (« A compter du 6 août2002 ») porte « effet antérieur à la publication » ;
  C24 chaque avis gardé dont le texte porte « Issue Date », « Date de publication » ou « N° » et une année a sa date de
     publication lue (la propriété, pas un compte ; le 12-10-2026, 37 avis la portent) ;
  et C22 contient aussi le cas du troisième tour de relecture : un avis lisible qui annonce un jour au-delà du
     calendrier rend l'événement « à venir », même quand la colonne de bnains tombe dans le calendrier.
⑨ CE QUI CLOCHE — C1, C9 et C10 sont des mesures du prototype du 11-10-2026, pas des lectures d'avis : elles prouvent
  que le programme refait le prototype, pas que le prototype avait raison. Les autres sont lues dans les avis. · Aucune
  épreuve ne fixe la date de CHAQUE événement : un décalage qui garde le compte à 40 et ne touche aucune des valeurs
  nommées ici passerait (la relecture du 12-10-2026 l'a montré avec un an de décalage ; C19 l'attrape désormais, car la
  date s'écarte alors de la colonne de bnains). · Les sabotages « admissions avant les retraits » et « un seul avis lu
  par événement » laissent tout vert : sans effet possible sur les données d'aujourd'hui, non éprouvés.
⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin.
⑪ TERMINAISON — Rend la main.
  [sort: oui]
"""
import contextlib
import csv
import errno
import hashlib
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile
from datetime import date

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
D = date.fromisoformat
OUTIL = os.path.join("etudes", "outils", "RELEVER_LA_COMPOSITION_DU_CAC40.py")
DEPENDANCES = ("CALENDRIER_DE_LA_BOURSE.py", "CONTRATS_DES_FICHIERS.py")
R = "RELEVER_LA_COMPOSITION_DU_CAC40.py"
# Les erreurs de l'ENVIRONNEMENT, qui ne disent rien du code éprouvé : disque plein, quota, trop de fichiers ouverts.
# Relecture indépendante du 12-10-2026 (sur le banc de la lecture des cours) : disque plein, 17 rouges « No space left
# on device » ont compté comme des détections, et le verdict a dit « tout est conforme ». Une épreuve tombée sur l'une
# d'elles n'est PAS JUGÉE (code 2).
PANNES = (errno.ENOSPC, errno.EDQUOT, errno.EMFILE, errno.ENFILE)
SABOTAGES = {
    "Z0": [],
    "S1_sans_les_dates_des_avis": [(R, "        if trouvees:\n            meilleure", "        if False:\n            meilleure")],
    "S2_sans_le_decalage_de_fin_de_seance": [(R, "(s > d if fin_de_seance else s >= d)", "(s >= d)")],
    "S3_sans_l_appariement": [(R, "            if len(suivantes) == 1:", "            if False:")],
    "S4_sans_la_table_sicovam": [(R, "        elif code in sico:", "        elif False:")],
    "S5_motif_sans_after_close": [(R, "after (?:the )?markets? close on|", "")],
    "S6_registre_non_verifie": [(R, "                if hashlib.sha256(g.read()).hexdigest() != r[\"sha256\"]:", "                if False:")],
    "S7_ecarts_non_comptes": [(R, "    return 0 if plages == set(ECARTS_CONNUS) and corrections_de_l_avis(evenements) == ECARTS_A_LA_COLONNE else 1", "    return 0")],
    "S8_suspension_ignoree": [(R, "            elif e[\"isin\"] in etat:", "            elif e[\"evenement\"] == \"Retrait\" and e[\"isin\"] in etat:")],
    "S9_note_de_bnains_ignoree": [(R, "        if m:\n            jour", "        if False:\n            jour")],
    "S10_lignes_encore_dans_l_indice_perdues": [(R, "    out += [(x, a, None) for x, a in ouverts.items()]", "")],
    "S11_isin_na_garde": [(R, "        isin = c[0] if c[0] != \"na\" else isin_du_sicovam(c[1])", "        isin = c[0]")],
    "S12_cle_isin_fausse": [(R, "(2 if i % 2 == 0 else 1)", "(1 if i % 2 == 0 else 2)")],
    "S13_lien_du_nom_ignore": [(R, "        elif lien_nom and re.fullmatch", "        elif False and re.fullmatch")],
    "S14_case_de_date_stricte": [(R, "\\s*\\d\\d/\\d\\d/\\d{4}[^<]*</td>", "\\s*\\d\\d/\\d\\d/\\d{4}</td>")],
    "S15_preuve_initiale_oubliee": [(R, "        if p[\"premiere_seance\"] == seances[0].isoformat() and p[\"isin_bnains\"] in initiale:", "        if False:")],
    "S17_cloture_comme_ouverture": [(R, "effet = next((s for s in seances if s > jour), None) if \"clôture\" in m[4] else garde(jour)", "effet = garde(jour)")],
    "S16_avis_le_plus_eloigne": [(R, "            meilleure, nom = min(trouvees,", "            meilleure, nom = max(trouvees,")],
    "S18_annee_par_defaut_fausse": [(R, "if x.group(4) else annee,", "if x.group(4) else annee + 1,")],
    "S19_fichier_hors_registre_lu": [(R, "        if nom != \"REGISTRE.csv\" and nom not in inscrits:", "        if False:")],
    "S20_avis_annules_lus": [(R, "    ev = dater(historique, dossier, seances, inscrits, avis_annules(dossier, inscrits))", "    ev = dater(historique, dossier, seances, inscrits, set())")],
    "S21_appariement_elargi": [(R, "rang[date.fromisoformat(e[\"effet\"])] <= 1]", "rang[date.fromisoformat(e[\"effet\"])] <= 60]")],
    "S22_preuve_par_le_premier_lien": [(R, "        if e[\"avis_de_la_date\"]:\n", "        if False:\n")],
    "S23_blanc_obligatoire_avant_l_annee": [(R, "([A-Za-zéû]+)\\s*(\\d{4})?", "([A-Za-zéû]+)\\s+(\\d{4})?")],
    "S24_seance_de_bourse_non_lue": [(R, "séance (?:de bourse )?du", "séance du")],
    "S25_registre_non_fige": [(R, "    if empreinte != EMPREINTE_DU_REGISTRE:", "    if False:")],
    "S26_date_future_leve": [(R, "        seance = next((s for s in seances if (s > d if fin_de_seance else s >= d)), None)", "        seance = next(s for s in seances if (s > d if fin_de_seance else s >= d))")],
    "S27_publication_ignoree": [(R, "            if publie.get(nom) and meilleure < publie[nom]:", "            if False:")],
    "S28_corrections_non_comparees": [(R, "plages == set(ECARTS_CONNUS) and corrections_de_l_avis(evenements) == ECARTS_A_LA_COLONNE", "plages == set(ECARTS_CONNUS)")],
    "S29_numero_d_avis_absent": [(R, "                numero[nom[:-4]] = (m[1], int(m[2]))", "                pass")],
    "S30_en_tete_bilingue_non_lu": [(R, "\\s*(?:\\d{4}\\s*)?(?:/[^/N]", "\\s*(?:/[^/N]")],
    "S31_date_future_de_l_avis_jetee": [(R, "        if futures:\n", "        if False:\n")],
}


def muet(f, *a):
    """Appelle f(*a) sans rien laisser s'afficher, et rend ce qu'elle rend.

    ① RÔLE — Garder l'affichage des épreuves lisible quand une épreuve appelle `main`.
    ② CONTEXTE D'APPEL — `epreuves`, C11 et C12.
    ③ ENTRÉE — `f` : une fonction · `a` : ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : ce que rend `f`.
      [rend: 1]
    ⑥ TRAITEMENT — détourner la sortie standard le temps de l'appel.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `f`, sans l'affichage.
    ⑪ TERMINAISON — Rend la main ou laisse passer l'erreur de `f`.
      [sort: non]
    """
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a)


def copie_du_depot(tmp, nom):
    """Fabrique une racine jetable avec les témoins, l'indice et la liste d'Euronext.

    ① RÔLE — Laisser `main` écrire, et laisser une épreuve changer un témoin, sans toucher au dépôt.
    ② CONTEXTE D'APPEL — `epreuves`, C11 et C12.
    ③ ENTRÉE — `tmp` : un dossier jetable · `nom` : le nom de la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de la racine.
      [rend: 1]
    ⑥ TRAITEMENT — copier les trois choses que lit le programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les programmes du circuit écrivent : on ne les lance jamais sur le dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = os.path.join(tmp, nom)
    shutil.copytree(os.path.join(DEPOT, "temoins", "COMPOSITION_DU_CAC40_Lun_12-10-2026"),
                    os.path.join(r, "temoins", "COMPOSITION_DU_CAC40_Lun_12-10-2026"))
    os.makedirs(os.path.join(r, "donnees", "sources_indice"))
    shutil.copy(os.path.join(DEPOT, "donnees", "sources_indice", "INDICE_CAC40.csv"),
                os.path.join(r, "donnees", "sources_indice"))
    shutil.copy(os.path.join(DEPOT, "donnees", "CALENDRIER_EURONEXT.csv"), os.path.join(r, "donnees"))
    return r


def epreuves(dossier, tmp):
    """Joue C1 à C24 avec le programme du dossier `dossier`, et rend la liste (nom, verdict).

    ① RÔLE — Les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `dossier` : la racine jetable qui porte etudes/outils/ et programmes/, sabotés ou non · `tmp` : un
      dossier jetable.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : la liste des couples (nom, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — importer la copie ; faire le relevé une fois sur le dépôt (s'il lève, toutes les épreuves qui en
      dépendent sont rouges) ; chaque épreuve dans son propre essai.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Chaque réponse attendue est écrite à la main : le programme ne se juge pas lui-même.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(tmp, exist_ok=True)
    sp = importlib.util.spec_from_file_location("compo_%d" % id(tmp), os.path.join(dossier, OUTIL))
    M = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(M)
    res = []
    try:
        r = M.relever(DEPOT)
    except Exception:
        r = None

    def essai(nom, f):
        """Joue une épreuve et range son verdict.

        ① RÔLE — Une épreuve qui lève est rouge, les suivantes jouent.
        ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — `nom` · `f` : l'épreuve, sans argument.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Ne rend rien : ajoute (nom, verdict) à `res` ; le verdict vaut None quand l'erreur vient de
          l'environnement (PANNES, ou mémoire épuisée) : l'épreuve n'est pas jugée.
          [rend: rien]
        ⑥ TRAITEMENT — appeler, attraper ; une erreur de l'environnement donne None, toute autre erreur False.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Celui de l'épreuve.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        try:
            res.append((nom, bool(f())))
        except Exception as e:
            panne = isinstance(e, MemoryError) or getattr(e, "errno", None) in PANNES
            res.append((nom + (f" — {type(e).__name__} : {e}"[:200] if panne else ""), None if panne else False))

    def de(isin):
        """Rend les passages d'un code ISIN, en couples (première, dernière).

        ① RÔLE — Lire le résultat par code.
        ② CONTEXTE D'APPEL — Les épreuves.
        ③ ENTRÉE — `isin`.
        ④ CONDITIONS D'ENTRÉE — Le relevé a réussi (sinon l'épreuve lève, donc rougit).
        ⑤ SORTIE — UNE valeur : la liste triée des couples.
          [rend: 1]
        ⑥ TRAITEMENT — filtrer.
        ⑦ UNITÉ — Des séances, écrites AAAA-MM-JJ.
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return sorted((p["premiere_seance"], p["derniere_seance"]) for p in r["passages"] if p["isin_bnains"] == isin)

    def ligne(isin, premiere):
        """Rend le passage d'un code ISIN qui commence à une séance donnée.

        ① RÔLE — Lire les preuves d'un passage.
        ② CONTEXTE D'APPEL — C2, C17.
        ③ ENTRÉE — `isin` · `premiere` : AAAA-MM-JJ.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le passage (StopIteration s'il n'existe pas, donc rouge).
          [rend: 1]
        ⑥ TRAITEMENT — chercher.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return next(p for p in r["passages"] if p["isin_bnains"] == isin and p["premiere_seance"] == premiere)

    seances = sorted(d for d in M.CAL.lire_les_seances(DEPOT)["indice"] if d >= M.DEBUT)
    essai("C1 93 passages sur 80 codes ISIN",
          lambda: len(r["passages"]) == 93 and len({p["isin_bnains"] for p in r["passages"]}) == 80)
    essai("C2 Aventis du 03-01-2000 au 18-06-2004, entrée prouvée par la composition du 03-01-2000",
          lambda: de("FR0000130460") == [("2000-01-03", "2004-06-18")]
          and ligne("FR0000130460", "2000-01-03")["preuve_entree"].startswith("déjà dans l'indice le 03-01-2000")
          and ligne("FR0000130460", "2000-01-03")["preuve_sortie"] == "0_4245_1626_53424_195930125_00.pdf — avis officiel")
    essai("C3 Thales revient le 24-06-2019", lambda: ("2019-06-24", "") in de("FR0000121329"))
    essai("C4 Peugeot sort après le 15-01-2021, Stellantis entre le 18-01-2021",
          lambda: de("FR0000121501")[-1][1] == "2021-01-15" and de("NL00150001Q9") == [("2021-01-18", "")])
    essai("C5 Vivendi sort après le 20-12-2024, Bureau Veritas entre le 23-12-2024",
          lambda: de("FR0000127771")[-1][1] == "2024-12-20" and de("FR0006174348") == [("2024-12-23", "")])
    essai("C6 EADS sous NL0000235190 depuis le 10-07-2000", lambda: de("NL0000235190") == [("2000-07-10", "")])
    essai("C7 Edenred : une seule séance, le 02-07-2010", lambda: de("FR0010908533")[0] == ("2010-07-02", "2010-07-02"))
    essai("C8 40 lignes au 02-10-2026, 40 passages ouverts",
          lambda: len(r["membres"][D("2026-10-02")]) == 40
          and sum(1 for p in r["passages"] if not p["derniere_seance"]) == 40)
    attendus = [("2000-06-26", "2000-08-22", 39), ("2000-12-11", "2000-12-20", 39), ("2003-05-22", "2003-07-10", 39),
                ("2003-10-01", "2003-11-20", 39), ("2004-06-21", "2004-09-30", 39), ("2006-06-19", "2006-09-15", 39),
                ("2007-04-11", "2007-06-15", 39), ("2008-07-22", "2008-09-19", 39), ("2010-07-02", "2010-07-02", 41),
                ("2019-05-03", "2019-06-21", 41)]
    essai("C9 exactement les dix plages d'écart",
          lambda: [(a.isoformat(), b.isoformat(), n) for a, b, n in r["ecarts"]] == attendus)
    essai("C10 exactement trois événements sans effet",
          lambda: sorted((e["date"], e["isin"]) for e in r["sans_effet"]) ==
          [("2003-09-07", "FR0000184202"), ("2003-11-21", "FR0000079196"), ("2006-09-18", "LU0140205948")]
          and {e["evenement"] for e in r["sans_effet"]} == {"Retrait"})

    def c11():
        """Un témoin changé, puis un témoin effacé : `main` rend 2.

        ① RÔLE — C11.
        ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si les quatre rendent 2.
          [rend: 1]
        ⑥ TRAITEMENT — trois copies du dépôt ; un octet ajouté à un avis ; un avis effacé ; un texte d'avis ajouté hors
          registre (le cas de la relecture du 12-10-2026, qui déplaçait la sortie de Sodexo au 22-09-2020) ; le même
          texte inscrit au registre avec sa propre empreinte (second tour de la relecture).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une preuve qui peut changer sans bruit n'en est pas une.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit dans `tmp`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        a = copie_du_depot(tmp, "c11a")
        with open(os.path.join(a, M.TEMOINS, "2010-097.pdf.txt"), "a", encoding="utf-8") as f:
            f.write(" ")
        b = copie_du_depot(tmp, "c11b")
        os.remove(os.path.join(b, M.TEMOINS, "2010-097.pdf.txt"))
        c = copie_du_depot(tmp, "c11c")
        with open(os.path.join(c, M.TEMOINS, "20200611_Communique_revision_trimestrielle_famille_cac.pdf.txt"), "w",
                  encoding="utf-8") as f:
            f.write("Ces changements prendront effet le 22 septembre 2020.")
        d = copie_du_depot(tmp, "c11d")
        faux = os.path.join(d, M.TEMOINS, "20200611_Communique_revision_trimestrielle_famille_cac.pdf.txt")
        with open(faux, "w", encoding="utf-8") as f:
            f.write("Ces changements prendront effet le 22 septembre 2020.")
        with open(faux, "rb") as f, open(os.path.join(d, M.TEMOINS, "REGISTRE.csv"), "a", encoding="utf-8") as g:
            g.write(f"{os.path.basename(faux)},faux,{hashlib.sha256(f.read()).hexdigest()},1,2026-10-12\n")
        return (muet(M.main, [a]) == 2 and muet(M.main, [b]) == 2 and muet(M.main, [c]) == 2
                and muet(M.main, [d]) == 2)
    essai("C11 un témoin changé, effacé, un fichier hors registre, un registre complété : code 2", c11)

    def c12():
        """Sur une copie du dépôt, `main` rend 0 et écrit l'en-tête du contrat ; un écart changé rend 1.

        ① RÔLE — C12.
        ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si le code est 0, l'en-tête celui du contrat, 93 lignes écrites, et si
          `code_de_sortie` rend 1 pour un écart déplacé d'une séance, un écart en moins, un écart en plus, et pour une
          correction de bnains de plus (Alcatel, comme si son avis avait glissé d'un an).
          [rend: 1]
        ⑥ TRAITEMENT — copie, lancement, lecture du fichier écrit.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — R-734. Relecture du 12-10-2026 : le code 1 permanent ne pouvait rien signaler.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit dans `tmp`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = copie_du_depot(tmp, "c12")
        code = muet(M.main, [c])
        with open(os.path.join(c, M.SORTIE), encoding="utf-8", newline="") as f:
            lu = list(csv.reader(f))
        e = r["ecarts"]
        deplace = [(e[0][0], seances[seances.index(e[0][1]) + 1], e[0][2])] + e[1:]
        plus = e + [(D("2026-10-02"), D("2026-10-02"), 39)]
        ev = r["evenements"]
        glisse = [dict(x, origine_date=x["origine_date"] + " (bnains écrivait 2013-12-23)") if x["libelle"] == "Alcatel"
                  else x for x in ev]
        return (code == 0 and lu[0] == M.CONTRATS.PASSAGES_DANS_LE_CAC40 and len(lu) == 94
                and M.code_de_sortie(e, ev) == 0 and M.code_de_sortie(deplace, ev) == 1
                and M.code_de_sortie(e[1:], ev) == 1 and M.code_de_sortie(plus, ev) == 1
                and M.code_de_sortie(e, glisse) == 1)
    essai("C12 main rend 0 sur les écarts connus et écrit le contrat ; un écart ou une correction de plus rend 1", c12)
    essai("C13 la clé ISIN tirée du Sicovam, cinq paires connues",
          lambda: [M.isin_du_sicovam(x) for x in ("12548", "4507", "12414", "12069", "12040")]
          == ["FR0000125486", "FR0000045072", "FR0000124141", "FR0000120693", "FR0000120404"])
    essai("C14 DOIT ÉCHOUER : le calcul ne donne pas le code d'Equant ; Equant est rangée sous NL0000200889",
          lambda: M.isin_du_sicovam("12701") != "NL0000200889" and de("NL0000200889") == [("2000-01-03", "2001-05-03")])
    essai("C15 la lecture des phrases d'effet",
          lambda: M.dates_d_effet("retirée à l’ issue de la séance du 18 juin 2004 .", 2004, seances)[0] == [D("2004-06-21")]
          and M.dates_d_effet("take place after markets close on Friday 17 September 2021.", 2021, seances)[0]
          == [D("2021-09-20")]
          and M.dates_d_effet("Effective date: Monday 24 June 2019", 2019, seances)[0] == [D("2019-06-24")]
          and M.dates_d_effet("Euronext Indices annonce la composition.", 2019, seances)[0] == []
          and M.dates_d_effet("A compter du 6 août2002 , Crédit Agricole", 2002, seances)[0] == [D("2002-08-06")]
          and M.dates_d_effet("à l’issue de la séance de bourse du 21 mai 2003", 2003, seances)[0] == [D("2003-05-22")]
          and M.dates_d_effet("as from the market close of 21 July 2008", 2008, seances)[0] == [D("2008-07-22")])
    essai("C16 Atos du 20-03-2017 au 17-09-2021", lambda: de("FR0000051732") == [("2017-03-20", "2021-09-17")])
    essai("C17 chaque date a sa preuve ; Thales 2019 nomme son avis",
          lambda: not any("aucun événement trouvé" in p["preuve_entree"] + p["preuve_sortie"] for p in r["passages"])
          and ligne("FR0000121329", "2019-06-24")["preuve_entree"]
          == "20190613_pr_quarterly_index_review_cac_q2_2019.pdf — avis officiel (bnains écrivait 2018-06-24)")


    def c18():
        """La note de bnains date un événement sans avis ; « après la clôture » donne la séance suivante.

        ① RÔLE — C18.
        ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si les trois événements sont datés comme attendu.
          [rend: 1]
        ⑥ TRAITEMENT — trois retraits fabriqués, sans avis et sans admission voisine (pas d'appariement possible).
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Sur les vraies données, la note ne change rien (Alcatel retombe sur le 07-01-2016 par
          l'appariement) : sans ce cas fabriqué, l'ôter ne rougirait rien.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        base = {"evenement": "Retrait", "code": "", "isin": "X", "origine_isin": "", "libelle": "x", "avis": ""}
        ev = [dict(base, date="2016-01-06", note="Remplacement le 07/01/2016 avant l'ouverture."),
              dict(base, date="2016-01-06", note="Remplacement le 07/01/2016 après la clôture."),
              dict(base, date="2016-01-06", note="sans date")]
        d = M.dater(ev, tmp, seances, set(), set())
        return ([e["effet"] for e in d] == ["2016-01-07", "2016-01-08", "2016-01-06"]
                and d[0]["origine_date"].startswith("note de bnains") and d[2]["origine_date"].startswith("colonne"))
    essai("C18 la note de bnains : avant l'ouverture, après la clôture, sans date", c18)
    essai("C19 bnains se trompe de plus de trois jours exactement six fois, chaque fois corrigé par l'avis",
          lambda: sorted((e["date"], e["evenement"], e["effet"]) for e in r["evenements"]
                         if "écrivait" in e["origine_date"]) ==
          [("2014-06-18", "Retrait", "2014-06-23"), ("2015-03-18", "Retrait", "2015-03-23"),
           ("2017-03-18", "Retrait", "2017-09-18"), ("2017-03-20", "Admission", "2017-09-18"),
           ("2018-06-24", "Admission", "2019-06-24"), ("2020-06-22", "Admission", "2020-09-21")])

    def c20():
        """L'appariement ne joint un retrait qu'à l'admission de la séance suivante.

        ① RÔLE — C20.
        ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si le premier retrait est apparié et le second non.
          [rend: 1]
        ⑥ TRAITEMENT — deux retraits sans source le vendredi 15-01-2021 ; une admission le lundi 18 (séance suivante),
          une autre le mardi 26-01-2021 (sept séances plus loin) ; les retraits portent des codes différents.
        ⑦ UNITÉ — Des séances.
        ⑧ POURQUOI — Relecture du 12-10-2026 : élargir l'appariement à 60 séances laissait tout vert.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        base = {"code": "", "origine_isin": "", "avis": "", "note": ""}
        ev = [dict(base, date="2021-01-15", evenement="Retrait", isin="A", libelle="a"),
              dict(base, date="2021-01-18", evenement="Admission", isin="B", libelle="b"),
              dict(base, date="2021-01-26", evenement="Admission", isin="C", libelle="c")]
        d = M.dater(ev, tmp, seances, set(), set())
        ev2 = [dict(ev[0]), dict(ev[2])]
        d2 = M.dater(ev2, tmp, seances, set(), set())
        return d[0]["effet"] == "2021-01-18" and d2[0]["effet"] == "2021-01-15"
    essai("C20 l'appariement : la séance suivante seulement", c20)
    tz = os.path.join(DEPOT, M.TEMOINS)

    def texte(nom):
        """Rend le texte d'un avis gardé.

        ① RÔLE — Lire un témoin.
        ② CONTEXTE D'APPEL — C23.
        ③ ENTRÉE — `nom` : le nom du PDF gardé.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le texte.
          [rend: 1]
        ⑥ TRAITEMENT — lire le .txt.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit un fichier.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        with open(os.path.join(tz, nom + ".txt"), encoding="utf-8") as f:
            return f.read()
    def c22b():
        """Un avis lisible qui annonce une date au-delà du calendrier rend l'événement « à venir », même quand la
        colonne de bnains tombe dans le calendrier.

        ① RÔLE — Le cas du troisième tour de la relecture du 12-10-2026.
        ② CONTEXTE D'APPEL — C22.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si l'effet est vide et l'origine dit « à venir ».
          [rend: 1]
        ⑥ TRAITEMENT — un avis fabriqué « effective from Monday 5 October 2026 » (après la dernière séance du
          calendrier, le 02-10-2026 au moment d'écrire), un retrait daté par bnains le 30-09-2026.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Jetée sans bruit, la date laissait l'événement à la date de bnains, avec « avis illisible ».
        ⑨ CE QUI CLOCHE — Le jour du 05-10-2026 deviendra une séance du calendrier dès que l'indice de ce jour sera
          versé ; l'épreuve prend donc le lendemain de la dernière séance, calculé.
        ⑩ EFFET — Écrit un fichier dans `tmp`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        apres = seances[-1].toordinal() + 3
        jour = date.fromordinal(apres)
        mois = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                "November", "December"][jour.month]
        with open(os.path.join(tmp, "futur.pdf.txt"), "w", encoding="utf-8") as f:
            f.write(f"Effective date: {jour.day} {mois} {jour.year}")
        e = {"date": seances[-2].isoformat(), "evenement": "Retrait", "code": "", "isin": "X", "origine_isin": "",
             "libelle": "x", "note": "", "avis": "avis/futur.pdf"}
        d = M.dater([e], tmp, seances, {"futur.pdf.txt"}, set())[0]
        return d["effet"] == "" and d["origine_date"].startswith(M.A_VENIR)
    essai("C22 une date au-delà du calendrier : rien de lu, événement « à venir », pas d'arrêt",
          lambda: M.dates_d_effet("effective from Monday 21 December 2026.", 2026, seances) == ([], [D("2026-12-21")])
          and M.dater([{"date": "2026-12-21", "evenement": "Admission", "code": "", "isin": "X", "origine_isin": "",
                        "libelle": "x", "note": "", "avis": ""}], tmp, seances, set(), set())[0]["effet"] == ""
          and M.dates_d_effet("à compter du 31 juin 2004", 2004, seances)[0] == []
          and c22b())
    essai("C23 la date de publication : 2002-2789 le 29-08-2002, 2010-097 le 11-06-2010, 2000-5128 le 08-12-2000 ; "
          "l'entrée de Crédit Agricole le dit antérieure",
          lambda: M.date_de_publication(texte("DA2002_2789FR.pdf")) == D("2002-08-29")
          and M.date_de_publication(texte("2010-097.pdf")) == D("2010-06-11")
          and M.date_de_publication(texte("DA2000_5128FR.pdf")) == D("2000-12-08")
          and ligne("FR0000045072", "2002-08-06")["preuve_entree"] == "DA2002_2789FR.pdf — avis officiel (effet "
          "antérieur à la publication du 2002-08-29 : à vérifier)")
    def c24():
        """Chaque avis gardé dont l'en-tête porte une date de publication la voit lue.

        ① RÔLE — C24.
        ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si aucun avis à en-tête n'est sans date, et si au moins un avis en a un (sinon
          l'épreuve ne prouverait rien).
          [rend: 1]
        ⑥ TRAITEMENT — un avis « porte un en-tête » quand son texte contient « Issue Date », « Date de publication » ou
          « N° » suivi d'une année ; la propriété ne dépend pas du nombre d'avis gardés.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecture du 12-10-2026 : la date n'était lue que dans 18 avis sur 52.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lit les témoins.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        portent = [n for n in os.listdir(tz) if n.endswith(".pdf.txt")
                   and re.search(r"issue date|date de publication|N°\s*\d{4}", texte(n[:-4]), re.I)]
        return portent and all(M.date_de_publication(texte(n[:-4])) for n in portent)
    essai("C24 chaque avis à en-tête a sa date de publication lue", c24)
    essai("C21 l'avis annulé 2000-5128 n'est jamais une preuve ; Canal+ sort par le 2000-5131",
          lambda: M.avis_annules(os.path.join(DEPOT, M.TEMOINS), M.verifier_les_temoins(os.path.join(DEPOT, M.TEMOINS)))
          == {"DA2000_5128FR.pdf"}
          and M.NUMERO_D_AVIS.search("N° 2000 - 5131 INDICES SBF Annule et remplace l’avis N°2000-5128").groups()
          == ("2000", "5131")
          and ligne("FR0000130650", "2000-12-21")["preuve_entree"]
          == "DA2000_5128FR.pdf (cité par bnains) — colonne de bnains, avis annulé"
          and ligne("FR0000125460", "2000-01-03")["preuve_sortie"] == "DA2000_5131FR.pdf — avis officiel")
    return res


def main():
    """Joue Z0, puis chaque sabotage avec --saboter, et rend le code de sortie.

    ① RÔLE — Le chef d'orchestre.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie (0, 1 ou 2).
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque sabotage : copier le programme et ses dépendances, appliquer, jouer, afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit et efface un dossier jetable ; affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    saboter = "--saboter" in sys.argv
    seulement = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--seulement=")]
    code = 0
    tmp = tempfile.mkdtemp(prefix="epreuves_composition_")
    try:
        for nom, subs in SABOTAGES.items():
            if nom != "Z0" and not saboter:
                continue
            if seulement and nom != "Z0" and not any(nom.startswith(x + "_") for x in seulement[0]):
                continue
            dossier = os.path.join(tmp, "prog_" + nom)
            os.makedirs(os.path.join(dossier, "etudes", "outils"))
            os.makedirs(os.path.join(dossier, "programmes"))
            shutil.copy(os.path.join(DEPOT, OUTIL), os.path.join(dossier, "etudes", "outils"))
            for p in DEPENDANCES:
                shutil.copy(os.path.join(DEPOT, "programmes", p), os.path.join(dossier, "programmes"))
            ok = True
            for fichier, ancien, nouveau in subs:
                chemin = os.path.join(dossier, "etudes", "outils", fichier)
                s = open(chemin, encoding="utf-8").read()
                if s.count(ancien) != 1:
                    print(f"SABOTAGE {nom} INAPPLICABLE : ancre absente ou multiple dans {fichier}")
                    ok = False
                    break
                open(chemin, "w", encoding="utf-8").write(s.replace(ancien, nouveau))
            if not ok:
                code = 2
                continue
            res = epreuves(dossier, os.path.join(tmp, "t_" + nom))
            shutil.rmtree(dossier, ignore_errors=True)
            shutil.rmtree(os.path.join(tmp, "t_" + nom), ignore_errors=True)
            pannes = [n for n, v in res if v is None]
            if pannes:
                print(f"== {nom} : NON JUGÉ — l'environnement a manqué (disque, mémoire) : " + pannes[0])
                code = 2
                continue
            rouges = [n for n, v in res if not v]
            print(f"== {nom} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
            for n in rouges:
                print("     ROUGE " + n)
            if nom == "Z0" and rouges:
                code = max(code, 1)
            if nom != "Z0" and not rouges:
                print(f"     SABOTAGE {nom} SANS EFFET : aucune épreuve ne rougit")
                code = max(code, 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("VERDICT : " + ("tout est conforme" if code == 0 else f"NON CONFORME (code {code})"))
    return code


if __name__ == "__main__":
    sys.exit(main())
