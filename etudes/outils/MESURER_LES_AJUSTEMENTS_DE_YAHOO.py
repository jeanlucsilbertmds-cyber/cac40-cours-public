"""MESURER_LES_AJUSTEMENTS_DE_YAHOO.py — Jeu 08-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit.

À quoi il sert : trouver chaque fois que Yahoo a corrigé le passé de ses cours (colonne close) pour un événement qui ne le
justifie pas. La convention du système (donnees/LISEZ_MOI_LES_COURS.md) : les cours sont ajustés des divisions, des
attributions d'actions gratuites et des augmentations de capital, PAS des dividendes. Mesuré le 08-10-2026, Yahoo s'en
écarte au moins deux fois : EssilorLuxottica, 06-05-2024 (dividende payable en actions, ajusté comme une distribution,
sans le déclarer) et Crédit Agricole, 22-05-2018 (dividende en espèces, déclaré comme une division « 27 pour 26 »).

Quatre mesures, et la confrontation au fichier des verdicts :
1. LA MARCHE AU DÉTACHEMENT : pour chaque dividende déclaré par Yahoo, là où une source de cours bruts existe (bnains
   jusqu'au 28-02-2017, le fichier maître depuis le 02-01-2024), le rapport fichier ÷ brut doit être le même avant et
   après ; une marche dit que Yahoo a corrigé le passé ce jour-là.
2. LA BAISSE AU DÉTACHEMENT, là où il n'y a pas de source brute (mars 2017 → décembre 2023) : un dividende fait baisser
   le cours ; une baisse absente, une fois le marché retiré, dit que Yahoo a corrigé le passé pour l'effacer.
3. LE PONT : le rapport Yahoo ÷ brut en février 2017 (bnains) et en janvier 2024 (maître) ne doit différer que des
   divisions que Yahoo déclare entre les deux ; un reste est un ajustement non déclaré.
4. LE TÉMOIN OFFICIEL : les cours extrêmes de l'année publiés par Crédit Agricole (document de référence 2018).
Toute anomalie mesurée doit avoir son verdict dans donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv (écrit à la main,
chaque ligne avec sa preuve) ; une anomalie sans verdict fait rendre 1.

Comment s'en servir : python3 -I etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py <racine> <dossier de travail>
Le dossier de travail garde les réponses de Yahoo (une par valeur) ; s'il les a, rien n'est retéléchargé. L'outil écrit
donnees/sources_yahoo/EVENEMENTS_YAHOO.csv (les dividendes et les divisions déclarés par Yahoo).
Simulation uniquement.
"""
import csv, datetime, glob, json, os, statistics, sys, time, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
import CONTROLER_L_HISTORIQUE_LONG as K
from CONTRATS_DES_FICHIERS import AJUSTEMENTS_DE_YAHOO, COURS_BNAINS, EVENEMENTS_YAHOO

MAITRE = os.path.join("donnees", "cours_maitre.csv")
VERDICTS = os.path.join("donnees", "sources_yahoo", "AJUSTEMENTS_DE_YAHOO.csv")
EVENEMENTS = os.path.join("donnees", "sources_yahoo", "EVENEMENTS_YAHOO.csv")
FIN_BNAINS, DEBUT_MAITRE = "2017-02-28", "2024-01-02"
MARCHE = 0.005        # une marche de plus de 0,5 % du rapport fichier ÷ brut au détachement est une correction
ECARTS = 3            # une baisse au détachement inférieure à la baisse ordinaire de plus de 3 incertitudes est absente
INCERTITUDE = 0.5     # … mesurée seulement quand le bruit propre de la valeur est inférieur à la moitié du dividende
PONT = 0.003          # un reste du pont de plus de 0,3 % est un ajustement non déclaré
FACTEUR = 0.001       # un facteur à défaire doit être, à 0,1 % près, celui que Yahoo a appliqué
# Le témoin officiel : cours extrêmes de l'action Crédit Agricole S.A. par année, document de référence 2018, page
# « Données boursières » (https://www.bnains.org/archives/communiques/Credit_Agricole/
# 20190326_Document_de_reference_2018_Credit_Agricole.pdf) : plus haut en séance, plus bas en séance, dernier cours.
TEMOIN = ("CREDIT AGRICOLE SA", {"2018": (15.54, 9.10, 9.43), "2017": (15.68, 11.06, 13.80), "2016": (12.07, 6.79, 11.78),
                                 "2015": (14.49, 9.82, 10.88), "2014": (12.22, 9.14, 10.76)})


def charger_yahoo(racine, travail):
    """Lit, pour chaque valeur, les dividendes et les divisions que Yahoo déclare ; rend valeur → (dividendes, divisions).

    ① RÔLE — Relever ce que Yahoo DIT avoir fait, pour le confronter à ce qu'il a FAIT.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le dépôt · `travail` : le dossier où garder les réponses de Yahoo.
    ④ CONDITIONS D'ENTRÉE — Le référentiel des valeurs donne le mnémonique ; le symbole Yahoo est « mnémonique.PA ».
    ⑤ SORTIE — UNE valeur : le dictionnaire valeur → (liste (date, montant) des dividendes, liste (date, rapport) des
      divisions), dates ISO, pour les valeurs de l'historique long.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque valeur, la réponse de Yahoo gardée, ou téléchargée et gardée · ② les événements
      « dividends » et « splits », datés en temps universel (le jour de la séance de Paris).
    ⑦ UNITÉ — Des EUROS par action pour un dividende ; un RAPPORT nouvelles ÷ anciennes pour une division.
    ⑧ POURQUOI — Mesuré le 08-10-2026 : les 39 séries de Yahoo téléchargées ce jour-là ont, au 15-09-2026, la même
      clôture que le fichier ; ce sont donc les mêmes séries que celles de l'historique long.
    ⑨ CE QUI CLOCHE — Yahoo peut changer ses déclarations d'un jour à l'autre : les réponses gardées font foi pour une
      mesure, et EVENEMENTS_YAHOO.csv en garde la trace au dépôt.
    ⑩ EFFET — Écrit les réponses de Yahoo dans `travail` quand elles y manquent. Réseau.
    ⑪ TERMINAISON — Une demande par valeur, bornée à 60 secondes.
      [sort: non]
    """
    ref = sorted(glob.glob(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS_*.csv")))[-1]
    mnemo = {r["nom_usuel"]: r["mnemonique"] for r in csv.DictReader(open(ref, encoding="utf-8-sig"))}
    valeurs = sorted({l.split(",")[0] for l in open(os.path.join(racine, K.FICHIER), encoding="utf-8")} - {"valeur"})
    sortie = {}
    for v in valeurs:
        sym = f"{mnemo[v]}.PA"
        cache = os.path.join(travail, f"{v}__{sym}.json")
        if not os.path.exists(cache):
            url = (f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?period1=946684800&period2=1790985600"
                   f"&interval=1d&events=div,split")
            open(cache, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                                           timeout=60).read())
            time.sleep(0.3)
        ev = json.load(open(cache, encoding="utf-8"))["chart"]["result"][0].get("events", {})
        jour = lambda t: datetime.datetime.fromtimestamp(int(t), datetime.timezone.utc).date().isoformat()
        sortie[v] = (sorted((jour(t), x["amount"]) for t, x in ev.get("dividends", {}).items()),
                     sorted((jour(t), x["numerator"] / x["denominator"]) for t, x in ev.get("splits", {}).items()), sym)
    return sortie


def marches_au_detachement(series, brut, dividendes):
    """Mesure, à chaque détachement de dividende où une source brute existe, la marche du rapport fichier ÷ brut.

    ① RÔLE — Mesure 1 : voir directement si Yahoo a corrigé le passé le jour d'un dividende.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `series` : le fichier réparé · `brut` : valeur → {date: barre} de cours bruts (bnains avant le
      28-02-2017, le maître après le 02-01-2024) · `dividendes` : `charger_yahoo`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste (valeur, date du dividende, dividende ÷ cours de la veille, marche, jour du saut,
      divisions déclarées), marche = médiane du rapport sur les 5 séances qui commencent au détachement ÷ médiane sur
      les 5 qui le précèdent − 1 ; seulement là où les deux côtés ont 3 séances au moins ; jour du saut = la séance de
      la fenêtre où le rapport change le plus d'une séance à la suivante ; divisions déclarées = produit des divisions
      que Yahoo déclare entre la première et la dernière séance de la fenêtre (1 s'il n'y en a pas).
      [rend: 1]
    ⑥ TRAITEMENT — Par valeur et par dividende : les séances du fichier autour du jour, leur rapport au brut, le jour
      du saut, les divisions déclarées dans la fenêtre.
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — Un dividende non corrigé laisse le rapport inchangé : le fichier et le brut baissent ensemble.
      Le nombre de dividendes mesurés et de marches est affiché par `main` à chaque passage.
    ⑨ CE QUI CLOCHE — Le maître n'est pas brut pour les divisions et les actions gratuites (il les ajuste comme Yahoo) :
      la mesure ne dit rien d'elles. · Une division qui tombe dans la fenêtre d'un dividende fait une marche : mesuré le
      08-10-2026, huit marches de 2000 à 2006 sont des divisions (Yahoo en déclare sept, datées de 0 à 6 jours de la
      chute du brut ; Carrefour, 11-04-2000, n'est pas déclarée) — d'où le jour du saut et les divisions déclarées.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cas = []
    for v, (divs, divisions, _) in sorted(dividendes.items()):
        s, b = series.get(v, {}), brut.get(v, {})
        ds = sorted(s)
        for d, montant in divs:
            if d not in s or d not in b:
                continue
            i = ds.index(d)
            fen = [x for x in ds[max(0, i - 5):i + 5] if x in b and b[x][3] > 0]
            av = [s[x][3] / b[x][3] for x in fen if x < d]
            ap = [s[x][3] / b[x][3] for x in fen if x >= d]
            if len(av) >= 3 and len(ap) >= 3 and i > 0:
                saut = max(zip(fen, fen[1:]), key=lambda p: abs(s[p[1]][3] / b[p[1]][3] / (s[p[0]][3] / b[p[0]][3]) - 1))[1]
                declare = 1.0
                for x, k in divisions:
                    if fen[0] <= x <= fen[-1]:
                        declare *= k
                cas.append((v, d, montant / s[ds[i - 1]][3], statistics.median(ap) / statistics.median(av) - 1, saut, declare))
    return cas


def baisses_au_detachement(series, indice, dividendes, du, au):
    """Mesure, à chaque détachement entre `du` et `au`, quelle part du dividende le cours a perdue, marché retiré.

    ① RÔLE — Mesure 2 : voir une correction du passé là où il n'y a pas de source brute.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `series` · `indice` : date → clôture de l'indice · `dividendes` · `du`, `au` : dates.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste (valeur, date, dividende ÷ cours, k, incertitude) ; k = −(rendement du jour − bêta ×
      rendement de l'indice) ÷ (dividende ÷ cours) ; incertitude = écart-type des résidus des 120 séances
      précédentes ÷ (dividende ÷ cours).
      [rend: 1]
    ⑥ TRAITEMENT — Bêta et résidus par moindres carrés sur les 120 séances qui précèdent ; puis le jour du détachement.
    ⑦ UNITÉ — k sans unité : ≈ 1, le cours a baissé du dividende ; ≈ 0, la baisse a été effacée.
    ⑧ POURQUOI — Un dividende fait baisser le cours d'un peu moins que son montant (effet connu de la fiscalité) ; la
      baisse ORDINAIRE est la médiane des k mesurables, calculée par `main`. Crédit Agricole, 22-05-2018 : k −0,35 ±
      0,19, loin de toute autre mesure.
    ⑨ CE QUI CLOCHE — Un jour de grand mouvement du marché brouille la mesure (Sanofi, 04-05-2020). · Un dividende
      petit devant le bruit de la valeur ne se mesure pas (TotalEnergies, acomptes trimestriels de 1,2 à 1,5 %).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cas = []
    for v, (divs, _, _) in sorted(dividendes.items()):
        s = series.get(v, {})
        ds = sorted(s)
        for d, montant in divs:
            if not du <= d <= au or d not in s:
                continue
            i = ds.index(d)
            if i < 121:
                continue
            p = ds[i - 1]
            X, Y = [], []
            for a, z in zip(ds[i - 121:i - 1], ds[i - 120:i]):
                if a in indice and z in indice:
                    X.append(indice[z] / indice[a] - 1)
                    Y.append(s[z][3] / s[a][3] - 1)
            if len(X) < 60 or p not in indice or d not in indice:
                continue
            mx, my = statistics.mean(X), statistics.mean(Y)
            beta = sum((x - mx) * (y - my) for x, y in zip(X, Y)) / sum((x - mx) ** 2 for x in X)
            bruit = statistics.pstdev([y - beta * x for x, y in zip(X, Y)])
            dp = montant / s[p][3]
            e = (s[d][3] / s[p][3] - 1) - beta * (indice[d] / indice[p] - 1)
            cas.append((v, d, dp, -e / dp, bruit / dp))
    return cas


def ponts(origine, bnains, maitre, dividendes):
    """Compare le rapport Yahoo ÷ brut de février 2017 à celui de janvier 2024, divisions déclarées retirées.

    ① RÔLE — Mesure 3 : trouver tout ajustement que Yahoo n'a pas déclaré entre mars 2017 et décembre 2023.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `origine` : le fichier Yahoo d'origine · `bnains` · `maitre` · `dividendes` : `charger_yahoo`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste (valeur, rapport mesuré, rapport déclaré, reste), rapport mesuré = médiane de
      Yahoo ÷ maître du 02-01 au 15-02-2024 ÷ médiane de Yahoo ÷ bnains du 16-01 au 28-02-2017, cours bruts sans
      aucune division ; rapport déclaré = produit des divisions que Yahoo déclare après le 28-02-2017 ; reste =
      mesuré ÷ déclaré − 1 ; les valeurs sans dix séances aux deux bouts sont omises.
      [rend: 1]
    ⑥ TRAITEMENT — Par valeur : les deux médianes, puis le reste.
    ⑦ UNITÉ — Des RAPPORTS.
    ⑧ POURQUOI — Le maître ajuste les divisions et les actions gratuites comme Yahoo, et pas les dividendes : le pont
      compte donc toutes les divisions déclarées après 2017, y compris celles d'après 2024 (Air Liquide 2024, 2026).
    ⑨ CE QUI CLOCHE — Une division déclarée FAUSSE (Crédit Agricole, 2018) ne laisse aucun reste : le pont ne la voit
      pas ; ce sont la mesure 2 et le témoin officiel qui la voient. · Un ajustement suivi d'un ajustement inverse ne
      laisse pas de reste.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def rapport(v, brut, du, au):
        r = [origine[v][d][3] / brut[d][3] for d in sorted(origine.get(v, {})) if du <= d <= au and d in brut and brut[d][3] > 0]
        return statistics.median(r) if len(r) >= 10 else None
    cas = []
    for v, (_, divisions, _) in sorted(dividendes.items()):
        a = rapport(v, bnains.get(v, {}), "2017-01-16", FIN_BNAINS)
        z = rapport(v, maitre.get(v, {}), DEBUT_MAITRE, "2024-02-15")
        if a is None or z is None:
            continue
        declare = 1.0
        for d, k in divisions:
            if d > FIN_BNAINS:
                declare *= k
        cas.append((v, z / a, declare, z / a / declare - 1))
    return cas


def classer_les_marches(cas):
    """Sépare les marches au détachement qu'une division déclarée explique de celles qu'elle n'explique pas.

    ① RÔLE — Une seule règle de tri, pour le fichier de Yahoo et le fichier réparé.
    ② CONTEXTE D'APPEL — `main`, deux fois.
    ③ ENTRÉE — `cas` : `marches_au_detachement`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : ① tous les cas · ② les marches de plus de `MARCHE` non expliquées · ③ celles
      qu'explique, à `MARCHE` près, le produit des divisions déclarées dans la fenêtre.
      [rend: 3]
    ⑥ TRAITEMENT — Filtrer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑨ de `marches_au_detachement`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    marches = [c for c in cas if abs(c[3]) > MARCHE]
    non = [c for c in marches if abs((1 + c[3]) / c[5] - 1) > MARCHE]
    return cas, non, [c for c in marches if c not in non]


def baisses_absentes(cas):
    """Rend, parmi les baisses au détachement mesurables, celles qui sont absentes.

    ① RÔLE — Une seule règle, pour le fichier de Yahoo et le fichier réparé.
    ② CONTEXTE D'APPEL — `main`, deux fois.
    ③ ENTRÉE — `cas` : `baisses_au_detachement`.
    ④ CONDITIONS D'ENTRÉE — Au moins deux cas mesurables.
    ⑤ SORTIE — QUATRE valeurs : ① les cas mesurables (incertitude inférieure à `INCERTITUDE`) · ② k ordinaire, leur
      médiane · ③ les baisses absentes, à plus de `ECARTS` incertitudes sous k ordinaire · ④ le suivant : (écart en
      incertitudes, valeur, date) du cas mesurable le plus éloigné qui n'est pas absent.
      [rend: 4]
    ⑥ TRAITEMENT — Filtrer, médiane, filtrer.
    ⑦ UNITÉ — k et les écarts, sans unité.
    ⑧ POURQUOI — Un seuil fixe sur k (k < 0,3, essayé le 08-10-2026) retenait six cas de bruit ; l'écart en
      incertitudes sépare Crédit Agricole 2018 (6,2) du suivant (2,6).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    mesurables = [c for c in cas if c[4] < INCERTITUDE]
    k = statistics.median(c[3] for c in mesurables)
    absentes = [c for c in mesurables if (k - c[3]) / c[4] > ECARTS]
    return mesurables, k, absentes, max(((k - c[3]) / c[4], c[0], c[1]) for c in mesurables if c not in absentes)


def temoin_officiel(series):
    """Rapporte les cours de Crédit Agricole d'une série aux cours extrêmes officiels de chaque année de `TEMOIN`.

    ① RÔLE — Le témoin officiel, pour le fichier de Yahoo (calibrage) et le fichier réparé (preuve de la correction).
    ② CONTEXTE D'APPEL — `main`, deux fois.
    ③ ENTRÉE — `series` : un fichier de cours lu par `K.lire_cours`.
    ④ CONDITIONS D'ENTRÉE — La série de Crédit Agricole a des séances chaque année de `TEMOIN`.
    ⑤ SORTIE — UNE valeur : année → (plus haut de la série ÷ plus haut officiel, plus bas ÷ plus bas officiel, clôture
      du dernier jour ouvré de décembre ÷ dernier cours officiel, ou None si la série n'a pas ce jour).
      [rend: 1]
    ⑥ TRAITEMENT — Par année.
    ⑦ UNITÉ — Des RAPPORTS.
    ⑧ POURQUOI — Le « dernier cours » officiel est celui du dernier jour ouvré de décembre. Mesuré le 08-10-2026 :
      Yahoo n'a pas la séance du 31-12-2015 (sa dernière clôture est celle du 30-12, bnains 10,895 ; l'officiel
      10,88 est celle du 31) : la clôture ne se compare que si la série a ce jour-là.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    s, sortie = series.get(TEMOIN[0], {}), {}
    for an, (h, l, c) in TEMOIN[1].items():
        x = {d: b for d, b in s.items() if d.startswith(an)}
        fin = max(f"{an}-12-{j:02d}" for j in range(25, 32) if datetime.date(int(an), 12, j).weekday() < 5)
        sortie[an] = (max(b[1] for b in x.values()) / h, min(b[2] for b in x.values()) / l,
                      x[fin][3] / c if fin in x else None)
    return sortie


def main(argv):
    """Mesure, calibre, confronte aux verdicts, écrit les événements de Yahoo ; rend le code de sortie.

    ① RÔLE — Dire quels ajustements de Yahoo ne suivent pas la convention, et vérifier que chacun est jugé.
    ② CONTEXTE D'APPEL — À la main. Aucun circuit ne le lance.
    ③ ENTRÉE — `argv` : la racine du dépôt, le dossier de travail.
    ④ CONDITIONS D'ENTRÉE — Le fichier réparé, le fichier Yahoo d'origine, bnains, le maître, l'indice, les verdicts,
      les droits de bnains et les opérations déclarées (`K.lire_detachements`).
    ⑤ SORTIE — UNE valeur : 0 quand le calibrage passe, que les corrections sont prouvées et que toute anomalie a son
      verdict ; 1 sinon ; 2 si un fichier manque ou que Yahoo ne répond pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① charger · ② écrire EVENEMENTS_YAHOO.csv · ③ les quatre mesures, sur le fichier de Yahoo et sur le
      fichier réparé · ④ CALIBRAGE, sur le fichier de Yahoo : la mesure 1 doit trouver EssilorLuxottica, saut le
      06-05-2024 ; la mesure 2, Crédit Agricole, 22-05-2018 ; le témoin officiel doit montrer Yahoo à 0,963 des cours
      officiels de 2014 à 2017, et à 1 sur la clôture du 31-12-2018 · ⑤ CORRECTIONS : pour chaque ajustement à défaire
      (`K.lire_a_defaire`), le facteur écrit doit être, à `FACTEUR` près, celui que Yahoo a appliqué (la marche de la
      mesure 1 sur le fichier de Yahoo, ou, pour Crédit Agricole, l'inverse du témoin officiel 2014-2017), et le
      fichier réparé ne doit plus le montrer (ni marche, ni baisse absente ; témoin officiel à 1 de 2014 à 2018) — sauf
      la marche d'une opération déclarée le jour même dans DETACHEMENTS_OFFICIELS.csv, qui la remplace, et seulement si
      la marche vue vaut, à `FACTEUR` près, sa marche permise (Accor, 02-07-2010 : Edenred à 13,00 €, décision de
      Jean-Luc du 09-10-2026 à 21h00) ; la mesure 2 (baisse absente) ne se mesure sur aucune opération remplacée
      aujourd'hui (Accor 2010 tombe hors de 2017-2023) : cette branche n'est éprouvée par aucun cas réel ·
      ⑥ sur le fichier réparé, chaque anomalie —
      marche non expliquée (datée du jour du saut), baisse absente, reste du pont, division déclarée entre mars 2017 et décembre 2023 (que rien de brut ne
      vérifie) — doit avoir une ligne de verdict (même valeur ; même date, sauf pour un reste du pont : daté entre les
      deux bouts, et dont la colonne ce_que_yahoo_declare commence par « aucune déclaration »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Demande de Jean-Luc du 08-10-2026 à 10h40 : « mesure la famille », et stocker « proprement,
      clairement, en autoportant » ce qui est découvert, « sinon on va refaire les calculs infiniment ».
    ⑨ CE QUI CLOCHE — La mesure 1 voit aussi les zones que le fichier Yahoo avait fausses et que la réparation a
      refaites (les anomalies se jugent sur le fichier réparé pour cela) ; ce qui reste, comme Accor 2010 (Edenred),
      doit avoir son verdict. · Décision de Jean-Luc du 08-10-2026 à 11h14, « S'il y a des erreurs, il faut les
      corriger » : depuis, le fichier réparé n'a plus les deux erreurs (ni, depuis le 09-10-2026, le facteur d'Accor
      2010), et le calibrage, qui doit les retrouver, se
      fait sur le fichier de Yahoo tel que déposé.
    ⑩ EFFET — Écrit donnees/sources_yahoo/EVENEMENTS_YAHOO.csv. Affiche.
    ⑪ TERMINAISON — Voir `charger_yahoo`.
      [sort: non]
    """
    if len(argv) != 2 or not os.path.isdir(argv[0]) or not os.path.isdir(argv[1]):
        print("USAGE : MESURER_LES_AJUSTEMENTS_DE_YAHOO.py <racine> <dossier de travail>")
        return 2
    r, travail = argv
    try:
        div = charger_yahoo(r, travail)
        repare, _, _ = K.lire_cours(os.path.join(r, K.FICHIER))
        origine, _, _ = K.lire_cours(os.path.join(r, K.ORIGINE))
        bnains, _, _ = K.lire_cours(os.path.join(r, K.BNAINS), COURS_BNAINS)
        K.oter_les_barres_fausses(os.path.join(r, K.FAUSSES), bnains)
        brut_m, _, _ = K.lire_cours(os.path.join(r, MAITRE))
        lecteur = csv.DictReader(open(os.path.join(r, VERDICTS), encoding="utf-8"))
        if lecteur.fieldnames != AJUSTEMENTS_DE_YAHOO:
            raise ValueError(f"{VERDICTS} : en-tête {lecteur.fieldnames}")
        verdicts = list(lecteur)
        a_defaire = K.lire_a_defaire(os.path.join(r, K.VERDICTS_YAHOO))
        # une opération déclarée le jour même d'une correction défaite la remplace (Accor, 02-07-2010 : décision de
        # Jean-Luc du 09-10-2026 à 21h00) : sa marche, seule, doit rester dans le fichier réparé
        detachements, _ = K.lire_detachements(os.path.join(r, K.DROITS), os.path.join(r, K.OFFICIELS))
        indice = {}
        for x in csv.DictReader(open(os.path.join(r, K.INDICE), encoding="utf-8")):
            if x["yahoo"]:
                indice[x["date"]] = float(x["yahoo"])
    except (OSError, ValueError, KeyError) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    maitre = {}
    for v, s in brut_m.items():
        maitre.setdefault(v.replace("_", " "), {}).update(s)
    with open(os.path.join(r, EVENEMENTS), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(EVENEMENTS_YAHOO)
        for v, (divs, spl, sym) in sorted(div.items()):
            w.writerows([v, sym, "dividende", d, m] for d, m in divs)
            w.writerows([v, sym, "division", d, round(k, 6)] for d, k in spl)
    brut = {v: {d: x for d, x in bnains.get(v, {}).items() if d <= FIN_BNAINS} for v in div}
    for v in div:
        brut[v].update({d: x for d, x in maitre.get(v, {}).items() if d >= DEBUT_MAITRE})
    # Le CALIBRAGE et la mesure des facteurs se font sur le fichier de Yahoo tel que déposé ; les anomalies et la
    # preuve de la correction, sur le fichier réparé (qui défait les deux erreurs depuis le 08-10-2026, et le facteur
    # d'Accor 2010 depuis le 09-10-2026).
    tous_o, m1_o, _ = classer_les_marches(marches_au_detachement(origine, brut, div))
    tous, m1, m1_division = classer_les_marches(marches_au_detachement(repare, brut, div))
    _, _, m2_o, _ = baisses_absentes(baisses_au_detachement(origine, indice, div, "2017-03-01", "2023-12-31"))
    mesurables, k_ordinaire, m2, m2_suivant = baisses_absentes(
        baisses_au_detachement(repare, indice, div, "2017-03-01", "2023-12-31"))
    pont = ponts(origine, bnains, maitre, div)
    m3 = [c for c in pont if abs(c[3]) > PONT]
    m4 = [(v, d, k) for v, (_, spl, _) in sorted(div.items()) for d, k in spl if FIN_BNAINS < d < DEBUT_MAITRE]
    print(f"événements de Yahoo écrits : {EVENEMENTS} — {sum(len(x[0]) for x in div.values())} dividendes, "
          f"{sum(len(x[1]) for x in div.values())} divisions, {len(div)} valeurs")
    print(f"1. dividendes mesurés (une source brute des deux côtés) : {len(tous)} ; marches de plus de {MARCHE:.1%} : "
          f"{len(m1) + len(m1_division)}")
    print(f"1. marches au détachement (> {MARCHE:.1%}) expliquées par une division que Yahoo déclare dans la fenêtre : "
          f"{[(v, f'saut {j}', f'déclarée ×{k:g}') for v, _, _, _, j, k in m1_division]}")
    print(f"1. marches au détachement (> {MARCHE:.1%}) NON expliquées : "
          f"{[(v, j, f'{100 * s:+.2f} %', f'dividende {100 * dp:.2f} %') for v, _, dp, s, j, _ in m1]}")
    print(f"2. baisse ordinaire au détachement, 2017-2023 : k médian {k_ordinaire:.2f} sur {len(mesurables)} dividendes "
          f"mesurables (incertitude < {INCERTITUDE})")
    print(f"2. baisses absentes (k inférieur de plus de {ECARTS} incertitudes) : "
          f"{[(v, d, f'k {k:.2f} ± {u:.2f}') for v, d, _, k, u in m2]} · le suivant : {m2_suivant[1]} {m2_suivant[2]} "
          f"à {m2_suivant[0]:.1f} incertitudes")
    print(f"3. valeurs mesurées par le pont : {len(pont)}")
    print(f"3. restes du pont 2017 → 2024 (> {PONT:.1%}) : {[(v, f'{100 * c:+.2f} %') for v, _, _, c in m3]}")
    print(f"4. divisions déclarées 2017-2023, invérifiables par un cours brut : {[(v, d, round(k, 4)) for v, d, k in m4]}")
    temoin_o, temoin_r = temoin_officiel(origine), temoin_officiel(repare)
    for nom, tem in (("fichier de Yahoo", temoin_o), ("fichier réparé", temoin_r)):
        print(f"témoin officiel, Crédit Agricole, {nom} (÷ officiel : plus haut, plus bas, clôture du dernier jour ouvré) : "
              + " · ".join(f"{an} {a:.4f} {b:.4f} " + (f"{c:.4f}" if c else "séance absente du fichier")
                           for an, (a, b, c) in sorted(tem.items())))
    avant_2018 = [x for an in ("2014", "2015", "2016", "2017") for x in temoin_o[an] if x is not None]
    ok = (any(v == "ESSILORLUXOTTICA" and j == "2024-05-06" for v, _, _, _, j, _ in m1_o)
          and any(v == "CREDIT AGRICOLE SA" and d == "2018-05-22" for v, d, *_ in m2_o)
          and all(0.962 < x < 0.964 for x in avant_2018) and len(avant_2018) >= 10
          and temoin_o["2018"][2] is not None and 0.999 < temoin_o["2018"][2] < 1.001)
    print(f"CALIBRAGE (fichier de Yahoo) : {'passé' if ok else 'ÉCHOUÉ'}")
    if not ok:
        return 1
    # Chaque ajustement à défaire : le facteur écrit est-il celui que Yahoo a appliqué, et le fichier réparé en est-il
    # débarrassé ?
    faux = []
    for v, d, f in a_defaire:
        mesure = next((1 + s for x, _, _, s, j, _ in m1_o if x == v and j == d), None)
        if mesure is None and v == TEMOIN[0]:
            mesure = 1 / statistics.median(avant_2018)
        reste = ([j for x, _, _, _, j, _ in m1 if x == v and j == d] + [x for x, y, *_ in m2 if x == v and y == d])
        droit = detachements.get(v, {}).get(d)
        remplace = ""
        if droit and droit[0] in ("document", "distribution"):
            permise = K.marche_permise({}, droit)
            vue = [s for x, _, _, s, j, _ in m1 if x == v and j == d]
            if len(vue) == 1 and abs((1 + vue[0]) / (1 + permise) - 1) <= FACTEUR:
                reste = [x for x, y, *_ in m2 if x == v and y == d]
                remplace = f" (remplacé par l'opération déclarée : marche {100 * vue[0]:+.2f} %, permise {100 * permise:+.2f} %)"
        k_apres = next((f"k {k:.2f} ± {u:.2f}" for x, y, _, k, u in mesurables if x == v and y == d), "non mesurable")
        print(f"défait · {v} {d} : facteur écrit {f:.6f}, appliqué par Yahoo "
              f"{'non mesurable' if mesure is None else f'{mesure:.6f}'} ; dans le fichier réparé : "
              f"{'ENCORE VU' if reste else 'plus vu'}{remplace} ; baisse au détachement, fichier réparé : {k_apres}")
        if mesure is None or abs(mesure / f - 1) > FACTEUR or reste:
            faux.append((v, d))
    apres_2014 = [x for an in ("2014", "2015", "2016", "2017", "2018") for x in temoin_r[an] if x is not None]
    if not all(0.999 < x < 1.001 for x in apres_2014):
        faux.append((TEMOIN[0], "témoin officiel du fichier réparé"))
    print(f"CORRECTIONS (fichier réparé) : {'prouvées' if not faux else f'ÉCHOUÉES {faux}'}")
    if faux:
        return 1
    juge = lambda v, d: any(x["valeur"] == v and x["date"] == d for x in verdicts)
    # Un reste du pont est un ajustement que Yahoo n'a PAS déclaré : seule une ligne « aucune déclaration » le juge
    # (sinon la ligne d'une vraie division de la même valeur le couvrirait par erreur).
    juge_pont = lambda v: any(x["valeur"] == v and FIN_BNAINS < x["date"] < DEBUT_MAITRE
                              and x["ce_que_yahoo_declare"].startswith("aucune déclaration") for x in verdicts)
    sans = ([("marche", v, j) for v, _, _, _, j, _ in m1 if not juge(v, j)] + [("baisse absente", v, d) for v, d, *_ in m2 if not juge(v, d)]
            + [("pont", v, "") for v, *_ in m3 if not juge_pont(v)] + [("division", v, d) for v, d, _ in m4 if not juge(v, d)])
    print(f"anomalies sans verdict dans {VERDICTS} : {len(sans)} {sans}")
    for x in verdicts:
        print(f"  verdict · {x['valeur']} {x['date']} — {x['verdict']}")
    return 1 if sans else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
