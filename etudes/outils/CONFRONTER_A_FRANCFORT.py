"""CONFRONTER_A_FRANCFORT.py — Mer 07-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit.

À quoi il sert : confronter l'historique long réparé à une TROISIÈME source, la cotation des mêmes actions à la
Bourse de Francfort (méthode F du chapitre « Comment l'historique long a été construit » de
donnees/LISEZ_MOI_LES_COURS.md). Paris et Francfort cotent la même action : hors frais et décalage d'horaire, les
deux cours restent proches, et un écart durable de plusieurs pour cent est impossible sur un marché réel.

Comment s'en servir :
1. python3 -I etudes/outils/CONFRONTER_A_FRANCFORT.py <racine du dépôt> <dossier de travail>
2. Le dossier de travail reçoit les cours de Francfort téléchargés (un CSV par valeur) ; s'ils y sont déjà, ils ne
   sont pas retéléchargés. Deux sorties : donnees/sources_francfort/COURS_DE_FRANCFORT.csv, les clôtures de
   Francfort du 03-01-2000 au 28-02-2017 (la période de bnains), que la réparation et le contrôle lisent ; et
   donnees/sources_francfort/CONFRONTATION_DES_SEANCES_COMBLEES.csv.
Simulation uniquement.
"""
import csv, datetime, glob, json, os, statistics, sys, time, urllib.request

# Les cotations de Francfort chez Yahoo (symbole « .F »), cherchées le 07-10-2026 ; Pernod Ricard n'a que Xetra
# (« .DE ») et seulement depuis décembre 2007.
SYMBOLES = {
    "ACCOR": "ACR.F", "AIR LIQUIDE": "AIL.F", "AIRBUS": "AIR.F", "AXA": "AXA.F", "BNP PARIBAS": "BNP.F",
    "BOUYGUES": "BYG.F", "BUREAU VERITAS": "4BV.F", "CAPGEMINI": "CGM.F", "CARREFOUR": "CAR.F",
    "CREDIT AGRICOLE SA": "XCA.F", "DANONE": "BSN.F", "DASSAULT SYSTEMES": "DSY.F", "EIFFAGE": "EF3.F",
    "ENGIE": "GZF.F", "ESSILORLUXOTTICA": "ESL.F", "EUROFINS SCIENTIFIC": "ESF0.DE", "EURONEXT": "ENXB.F",
    "HERMES INTL": "HMI.F", "KERING": "PPX.F", "L'OREAL": "LOR.F", "LEGRAND": "LRC.F", "LVMH": "MOH.F",
    "MICHELIN": "MCHA.F", "ORANGE": "FTE.F", "PERNOD RICARD": "PER.DE", "PUBLICIS GROUPE": "PUB.F",
    "RENAULT": "RNL.F", "SAFRAN": "SEJ1.F", "SAINT-GOBAIN": "GOB.F", "SANOFI": "SNW.F",
    "SCHNEIDER ELECTRIC": "SND.F", "SOCIETE GENERALE": "SGE.F", "STMICROELECTRONICS": "SGM.F", "THALES": "CSF.F",
    "TOTALENERGIES": "TOTB.F", "UNIBAIL-RODAMCO-WESTFIELD": "1BR1.F", "VEOLIA": "VVD.F", "VINCI": "SQU.F",
}


def main(argv):
    """Télécharge Francfort au besoin, confronte chaque séance comblée, écrit le résultat ; rend le code de sortie.

    ① RÔLE — Dire, pour chaque séance que la réparation a comblée depuis bnains, si une troisième source la confirme.
    ② CONTEXTE D'APPEL — À la main, après programmes/REPARER_L_HISTORIQUE_LONG.py. Aucun circuit ne le lance.
    ③ ENTRÉE — `argv` : la racine du dépôt, puis le dossier de travail des cours de Francfort.
    ④ CONDITIONS D'ENTRÉE — donnees/sources_yahoo/historique_long_repare.csv et journal_des_reparations.csv existent ;
      le réseau joint query2.finance.yahoo.com, ou le dossier de travail contient déjà les cours.
    ⑤ SORTIE — UNE valeur : 0 quand le fichier est écrit, 2 sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque valeur sans fichier dans le dossier de travail, télécharger ses clôtures de
      Francfort de 2000 à 2026 · ①bis écrire celles du 03-01-2000 au 28-02-2017, arrondies à 4 décimales, dans
      donnees/sources_francfort/COURS_DE_FRANCFORT.csv · ② pour chaque séance comblée (geste « comblé » du journal) : « muet » si Francfort
      n'a pas de cours ce jour-là ou répète celui de la veille ; sinon, rapport Francfort ÷ fichier réparé ce
      jour-là, rapporté à sa médiane sur les dix séances communes de chaque côté ; « confirmée » si l'écart ne
      dépasse pas max(1 %, 3 × l'écart médian des voisins) ; sinon « confirmée, Francfort en retard d'une séance »
      si la clôture de Francfort du lendemain le respecte ; sinon « confirmée dans la fourchette du jour » si le
      cours de Francfort ramené tombe entre le plus bas et le plus haut du jour (élargis du même écart médian) ;
      sinon « en écart » · ③ écrire le CSV et afficher le compte par verdict.
    ⑦ UNITÉ — Des RAPPORTS sans unité, des DATES de séance.
    ⑧ POURQUOI — Les séances comblées n'avaient qu'une source, bnains, pour la Bourse de Paris (A-539, demande de
      Jean-Luc du 07-10-2026 : « tous les critères au niveau fort »). Mesuré le 07-10-2026 : Francfort n'a pas de
      cotation fraîche la plupart des jours où Yahoo manque — Yahoo y répète la veille, ou n'a rien —, ce que le
      verdict « muet » dit sans le cacher ; Francfort clôt plus tard que Paris (TotalEnergies, 16-11-2006 : 55,80 à
      Francfort, 56,50 à Paris, 54,45 le lendemain), d'où les deux verdicts de rattrapage.
    ⑨ CE QUI CLOCHE — Francfort est peu liquide les premières années : son bruit, mesuré sur les voisins, élargit la
      tolérance. · Les cours de Francfort chez Yahoo sont ajustés de certaines opérations et pas d'autres : ils ne
      servent qu'à comparer des séances voisines, jamais à dater un ajustement.
    ⑩ EFFET — Écrit dans le dossier de travail, donnees/sources_francfort/COURS_DE_FRANCFORT.csv et
      donnees/sources_francfort/CONFRONTATION_DES_SEANCES_COMBLEES.csv.
    ⑪ TERMINAISON — Rend la main. Un téléchargement peut attendre 30 secondes au plus par valeur.
      [sort: non]
    """
    if len(argv) != 2:
        print("USAGE : CONFRONTER_A_FRANCFORT.py <racine> <dossier de travail>")
        return 2
    racine, travail = argv
    os.makedirs(travail, exist_ok=True)
    fin = int(datetime.datetime(2026, 12, 31).timestamp())
    for valeur, symbole in sorted(SYMBOLES.items()):
        cible = os.path.join(travail, f"{valeur}__{symbole}.csv")
        if os.path.exists(cible):
            continue
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbole}?period1=946684800&period2={fin}&interval=1d"
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
            r = r["chart"]["result"][0]
        except Exception as e:
            print(f"{valeur} {symbole} : téléchargement impossible ({e})")
            continue
        q = r["indicators"]["quote"][0]
        with open(cible, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date", "open", "high", "low", "close", "volume"])
            for i, t in enumerate(r.get("timestamp") or []):
                if q["close"][i] is not None:
                    jour = (datetime.datetime.utcfromtimestamp(t) + datetime.timedelta(hours=2)).date().isoformat()
                    w.writerow([jour, q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i]])
        time.sleep(1)
    try:
        R, H, L = {}, {}, {}
        for r in csv.DictReader(open(os.path.join(racine, "donnees", "sources_yahoo", "historique_long_repare.csv"), encoding="utf-8")):
            R.setdefault(r["valeur"], {})[r["date"]] = float(r["close"])
            H[(r["valeur"], r["date"])], L[(r["valeur"], r["date"])] = float(r["high"]), float(r["low"])
        comblees = [r for r in csv.DictReader(open(os.path.join(racine, "donnees", "sources_yahoo", "journal_des_reparations.csv"),
                                                   encoding="utf-8")) if r["geste"] == "comblé"]
    except (OSError, ValueError, KeyError) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    F, cours = {}, []
    for fic in sorted(glob.glob(os.path.join(travail, "*__*.csv"))):
        valeur, symbole = os.path.basename(fic)[:-4].split("__")
        F[valeur] = {r["date"]: float(r["close"]) for r in csv.DictReader(open(fic, encoding="utf-8"))
                     if float(r["close"]) > 0}
        cours += [[valeur, symbole, d, repr(round(c, 4))] for d, c in sorted(F[valeur].items()) if d <= "2017-02-28"]
    chemin = os.path.join(racine, "donnees", "sources_francfort", "COURS_DE_FRANCFORT.csv")
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["valeur", "symbole", "date", "close"])
        w.writerows(cours)
    print(f"{len(cours)} clôtures de Francfort écrites : {os.path.relpath(chemin, racine)}")
    lignes = []
    for r in comblees:
        v, d = r["valeur"], r["date"]
        if v not in F or d not in F[v]:
            lignes.append([v, d, "muet", "", "", "Francfort n'a pas de cours ce jour-là"])
            continue
        commun = sorted(set(F[v]) & set(R[v]))
        j = commun.index(d)
        veille = commun[j - 1] if j else None
        if veille and F[v][d] == F[v][veille]:
            lignes.append([v, d, "muet", "", "", f"Francfort répète la clôture du {veille} : pas de cotation fraîche"])
            continue
        voisins = commun[max(0, j - 10):j] + commun[j + 1:j + 11]
        q = [F[v][x] / R[v][x] for x in voisins]
        m = statistics.median(q)
        bruit = statistics.median([abs(x / m - 1) for x in q])
        ecart, tol = F[v][d] / R[v][d] / m - 1, max(0.01, 3 * bruit)
        if abs(ecart) <= tol:
            lignes.append([v, d, "confirmée", f"{ecart:+.4f}", f"{bruit:.4f}", f"tolérance {tol:.2%}"])
            continue
        suivant = commun[j + 1] if j + 1 < len(commun) else None
        e2 = F[v][suivant] / R[v][d] / m - 1 if suivant else None
        if e2 is not None and abs(e2) <= tol:
            lignes.append([v, d, "confirmée, Francfort en retard d'une séance", f"{e2:+.4f}", f"{bruit:.4f}",
                           f"clôture de Francfort du {suivant} ; écart le jour même {ecart:+.2%} ; tolérance {tol:.2%}"])
            continue
        x = F[v][d] / m
        if L[(v, d)] * (1 - bruit) <= x <= H[(v, d)] * (1 + bruit):
            lignes.append([v, d, "confirmée dans la fourchette du jour", f"{ecart:+.4f}", f"{bruit:.4f}",
                           f"Francfort ramené {x:.4f} entre le plus bas {L[(v, d)]} et le plus haut {H[(v, d)]} (± bruit)"])
            continue
        lignes.append([v, d, "en écart", f"{ecart:+.4f}", f"{bruit:.4f}",
                       f"tolérance {tol:.2%} ; Francfort ramené {x:.4f}, fourchette {L[(v, d)]}–{H[(v, d)]}"])
    sortie = os.path.join(racine, "donnees", "sources_francfort", "CONFRONTATION_DES_SEANCES_COMBLEES.csv")
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    with open(sortie, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["valeur", "date", "verdict", "ecart", "bruit_median_des_voisins", "note"])
        w.writerows(lignes)
    compte = {}
    for l in lignes:
        compte[l[2]] = compte.get(l[2], 0) + 1
    print(f"{len(lignes)} séances comblées : {compte} · écrit : {os.path.relpath(sortie, racine)}")
    for l in lignes:
        if l[2] == "en écart":
            print("   en écart :", l[0], l[1], l[3], l[5])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
