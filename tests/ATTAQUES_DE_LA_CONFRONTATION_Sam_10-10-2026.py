#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATTAQUES_DE_LA_CONFRONTATION — Sam 10-10-2026 (Paris). Simulation uniquement.
Rôle : rejouer contre programmes/CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS.py les tables FAUSSES fabriquées par les deux
relectures indépendantes du 10-10-2026 (et quelques autres), sur une copie de la table : chacune doit être REFUSÉE,
la vraie table ACCEPTÉE. Les quatre tables fausses que la confrontation ne peut pas refuser — elles changent à la
fois un chiffre et sa raison, ou ajoutent une phrase vraie qui écrit le faux chiffre — sont jouées à part, sous
« LIMITES CONNUES » : elles doivent être ACCEPTÉES, pour que la limite reste écrite et mesurée.
Usage : python3 tests/ATTAQUES_DE_LA_CONFRONTATION_Sam_10-10-2026.py <racine>
Code : 0 si la vraie table est acceptée, chaque attaque refusée et chaque limite connue acceptée ; 1 sinon.
Les textes des documents sont extraits une fois par contenu : la confrontation est lancée plus de 60 fois.
"""
import csv, os, sys, shutil, tempfile, copy
HL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
sys.path.insert(0, os.path.join(HL, "programmes"))
import CONFRONTER_LES_CHIFFRES_AUX_DOCUMENTS as C
from CONTRATS_DES_FICHIERS import DETACHEMENTS_OFFICIELS
cache = {}
orig = C.texte_du_document
def _t(p):
    k = os.path.abspath(p)
    if k not in cache:
        cache[k] = orig(p)
    return cache[k]
C.texte_du_document = _t
R = tempfile.mkdtemp(); os.makedirs(R + "/donnees/sources_bnains"); os.symlink(HL + "/temoins", R + "/temoins")
T = list(csv.DictReader(open(HL + "/" + C.TABLE, encoding="utf-8")))
def L(rows, v, j): return [r for r in rows if r["valeur"] == v and r["jour_du_detachement"] == j][0]
def jouer(titre, change):
    rows = copy.deepcopy(T); change(rows)
    with open(R + "/" + C.TABLE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=DETACHEMENTS_OFFICIELS, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    refus, np_, al, _ = C.confronter(R)
    print(f"{'REFUSÉ ' if refus else 'ACCEPTÉ'} · {titre}" + (f" · {refus[0][:110]}" if refus else ""))
    return bool(refus)
def poser(v, j, k, x): return lambda rows: L(rows, v, j).__setitem__(k, x)
def ajoute(r, f, p): r[C.COLONNE] += f" ¦ {f} :: {p}"
n = 0; acc = 0
vraie = not jouer("table telle quelle (doit être ACCEPTÉE)", lambda rows: None)
cas = [
 ("A1 SG 2008 prix 47.00 (cas de Cowork)", poser("SOCIETE GENERALE","2008-02-21","prix_souscription","47.00")),
 ("A1 SG 2008 prix 77.72 (cours de clôture)", poser("SOCIETE GENERALE","2008-02-21","prix_souscription","77.72")),
 ("A1 SG 2008 prix 5.86 (valeur du droit)", poser("SOCIETE GENERALE","2008-02-21","prix_souscription","5.86")),
 ("A1 BNP 2009 prix 2 (nominal)", poser("BNP PARIBAS","2009-09-30","prix_souscription","2")),
 ("A1 BNP 2009 prix 38 (prime)", poser("BNP PARIBAS","2009-09-30","prix_souscription","38")),
 ("A1 Schneider prix 0.72", poser("SCHNEIDER ELECTRIC","2007-03-12","prix_souscription","0.72")),
 ("A1 Schneider prix 85.22", poser("SCHNEIDER ELECTRIC","2007-03-12","prix_souscription","85.22")),
 ("A1 AXA 2006 prix 24.47", poser("AXA","2006-06-19","prix_souscription","24.47")),
 ("A1 Euronext prix 84.65 (closing price)", poser("EURONEXT","2021-04-30","prix_souscription","84.65")),
 ("A1 Euronext prix 81.60", poser("EURONEXT","2021-04-30","prix_souscription","81.60")),
 ("A1 Veolia 2021 prix 29.06", poser("VEOLIA","2021-09-17","prix_souscription","29.06")),
 ("A1 CA 2007 prix 152.50 (milliers en espaces)", poser("CREDIT AGRICOLE SA","2007-01-04","prix_souscription","152.50")),
 ("A2 Schneider dividende 0.72", poser("SCHNEIDER ELECTRIC","2007-03-12","dividende_non_attache","0.72")),
 ("A2 BNP 2006 dividende 2.00", poser("BNP PARIBAS","2006-03-07","dividende_non_attache","2.00")),
 ("A3 Accor valeur 14.80 (clôture)", poser("ACCOR","2010-07-02","valeur_distribuee","14.80")),
 ("A3 Total valeur 27 (raison gardée)", poser("TOTALENERGIES","2006-05-18","valeur_distribuee","27")),
 ("A5 Saint-Gobain prix 0 (BSA gratuits)", poser("SAINT-GOBAIN","2009-02-23","prix_souscription","0")),
 ("A6 SG 2006 prix 109.08 (+1 %)", poser("SOCIETE GENERALE","2006-10-02","prix_souscription","109.08")),
 ("A7 BNP 2006 dividende vidé", poser("BNP PARIBAS","2006-03-07","dividende_non_attache","")),
 ("A7 Schneider dividende vidé", poser("SCHNEIDER ELECTRIC","2007-03-12","dividende_non_attache","")),
 ("A7 SG 2008 prix vidé", poser("SOCIETE GENERALE","2008-02-21","prix_souscription","")),
 ("A7 Carrefour valeur vidée", poser("CARREFOUR","2011-07-05","valeur_distribuee","")),
 ("A8 Danone parité 4.2", poser("DANONE","2009-06-01","anciennes_pour_une_nouvelle","4.2")),
 ("A8 Michelin parité 5", poser("MICHELIN","2010-09-30","anciennes_pour_une_nouvelle","5")),
]
def michelin(rows):
    m = L(rows,"MICHELIN","2010-09-30"); m["prix_souscription"]="47.50"
    m[C.COLONNE] += " ¦ SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf :: Le prix de souscription est de 47,50 euros par action"
def sept(rows):
    s = L(rows,"SOCIETE GENERALE","2008-02-21"); s["prix_souscription"]="7.50"
    s[C.COLONNE] = "SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf :: 7,50 euros par action"
def retirer(rows):
    m = L(rows,"MICHELIN","2010-09-30")
    m[C.COLONNE] = " ¦ ".join(e for e in m[C.COLONNE].split(" ¦ ") if "45 euros" not in e)
cas += [("A4 phrase de SG 2008 recopiée chez Michelin, prix 47.50", michelin),
        ("A4 « 7,50 euros » pris dans « 47,50 euros »", sept),
        ("A9 phrase du prix de Michelin retirée", retirer)]
for i, r in enumerate(T):
    if r["prix_souscription"].strip() and float(r["prix_souscription"]) > 0:
        cas.append((f"A10 {r['valeur']} {r['jour_du_detachement']} prix ×1,01",
                    (lambda i, x: (lambda rows: rows[i].__setitem__("prix_souscription", x)))(i, f"{float(r['prix_souscription'])*1.01:.2f}")))
def v1(rows):
    r = L(rows, "EURONEXT", "2021-04-30"); r["prix_souscription"] = "84.65"
    ajoute(r, "EURONEXT_2021_FCMKW111494_20210429.pdf", "at the issue price. Based on the closing price of €84.65 per ordinary share")
def v2(rows):
    r = L(rows, "VEOLIA", "2021-09-17"); r["prix_souscription"] = "90.80"
    ajoute(r, "VEOLIA_2021_FCBWR136439_20210916.pdf", "Un actionnaire possédant 21 actions existantes Veolia pourra donc souscrire à 4 actions nouvelles pour un prix de souscription total de 90,80 €")
def v3(rows):
    r = L(rows, "VEOLIA", "2021-09-17"); r["anciennes_pour_une_nouvelle"] = "4"
    ajoute(r, "VEOLIA_2021_FCBWR136439_20210916.pdf", "3 Pro forma des actifs acquis de Suez, pour les 12 mois se terminant au 30 juin 2021")
def v5(rows):
    r = L(rows, "SOCIETE GENERALE", "2008-02-21"); r["prix_souscription"] = "1.25"
    ajoute(r, "SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf", "Le prix de souscription est de […] 1,25 euros")
def v6(rows):
    r = L(rows, "ACCOR", "2010-07-02"); r["valeur_distribuee"] = "14.80"
    ajoute(r, "../DOCUMENTS_OFFICIELS_ACCOR_EDENRED_2010/EDENRED_DOCUMENT_DE_REFERENCE_2010.pdf", "cours d’ouverture […] 14,80 euros")
def v9(rows):
    r = L(rows, "MICHELIN", "2010-09-30"); r["prix_souscription"] = "47.50"
    r[C.COLONNE] = " ¦ ".join(e for e in r[C.COLONNE].split(" ¦ ") if "45 euros" not in e)
    ajoute(r, "SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf", "Le prix de souscription est de 47,50 euros par action")
    r["citation"] += " (voir aussi SOCIETE_GENERALE_2008_BALO_2008-02-13.pdf)"
def v11(rows):
    r = L(rows, "BNP PARIBAS", "2006-03-07"); r["valeur_distribuee"] = "0.85"
    r[C.COLONNE_RAISONS] = (r[C.COLONNE_RAISONS] + " ¦ " if r[C.COLONNE_RAISONS] else "") + "valeur_distribuee : 0,85 — valeur théorique du droit"
def v12(rows):
    r = L(rows, "EURONEXT", "2021-04-30"); r["prix_souscription"] = ""; r["valeur_distribuee"] = "59.65"
    r[C.COLONNE_RAISONS] = (r[C.COLONNE_RAISONS] + " ¦ " if r[C.COLONNE_RAISONS] else "") + "valeur_distribuee : 59,65 — x"
cas += [("V1 Euronext prix 84.65 + phrase vraie « issue price. Based on the closing price of €84.65 »", v1),
        ("V2 Veolia 2021 prix 90.80 + phrase vraie « prix de souscription total de 90,80 € »", v2),
        ("V3 Veolia 2021 parité 4 + phrase vraie « 3 Pro forma … pour les 12 mois »", v3),
        ("V5 SG 2008 prix 1.25 + phrase raboutée « prix de souscription est de […] 1,25 euros »", v5),
        ("V6 Accor valeur 14.80 + phrase raboutée « cours d’ouverture […] 14,80 euros »", v6),
        ("V9 Michelin prix 47.50 + phrase de SG 2008 + nom du BALO dans la citation", v9),
        ("V11 BNP 2006 aussi distribution 0.85, avec raison", v11),
        ("V12 Euronext prix vidé, valeur 59.65, avec raison", v12)]
for titre, f in cas:
    n += 1; acc += not jouer(titre, f)
print(f"\nATTAQUES : {n} · acceptées : {acc}")

def v4(rows):
    r = L(rows, "VINCI", "2006-03-30"); r["dividende_non_attache"] = "1.05"
    r[C.COLONNE_RAISONS] = " ¦ ".join(e for e in r[C.COLONNE_RAISONS].split(" ¦ ") if not e.startswith("dividende_non_attache"))
    ajoute(r, "VINCI_2006_dividende.html", "Dernier détachement de dividende VINCI le 14/11/2023 : 1.05€")
def v7(rows):
    r = L(rows, "TOTALENERGIES", "2006-05-18"); r["valeur_distribuee"] = "0.70"
    r[C.COLONNE_RAISONS] = r[C.COLONNE_RAISONS].replace("valeur_distribuee : 0,675 —", "valeur_distribuee : 0,70 —")
def v8(rows):
    r = L(rows, "SOCIETE GENERALE", "2008-02-21"); r["prix_souscription"] = "47.00"
    r[C.COLONNE] = " ¦ ".join(e for e in r[C.COLONNE].split(" ¦ ") if "47,50" not in e)
    r[C.COLONNE_RAISONS] += " ¦ prix_souscription : 47,00 — communiqué non gardé"
def v10(rows):
    r = L(rows, "CARREFOUR", "2011-07-05"); r["valeur_distribuee"] = ""; r["prix_souscription"] = "0"; r["anciennes_pour_une_nouvelle"] = "1"
    r[C.COLONNE_RAISONS] = (r[C.COLONNE_RAISONS] + " ¦ " if r[C.COLONNE_RAISONS] else "") + "prix_souscription : 0 — dividende en nature"
print("\nLIMITES CONNUES (la table est écrite à la main : seule la relecture de son changement les voit)")
limites = [("V4 Vinci dividende 1.05 (celui de 2023) + phrase vraie de la page Tradingsat, raison retirée", v4),
           ("V7 TotalEnergies valeur 0.70 + raison réécrite « 0,70 — … »", v7),
           ("V8 SG 2008 prix 47.00 : phrase du prix retirée + raison « 47,00 — … »", v8),
           ("V10 Carrefour transformé en droit : prix 0, parité 1, raison", v10)]
refusees = sum(jouer(t, f) for t, f in limites)
print(f"LIMITES : {len(limites)} · acceptées : {len(limites) - refusees}")
sys.exit(0 if vraie and acc == 0 and refusees == 0 else 1)
