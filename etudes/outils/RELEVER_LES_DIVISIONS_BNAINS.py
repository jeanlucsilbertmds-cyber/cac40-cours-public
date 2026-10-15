#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RELEVER_LES_DIVISIONS_BNAINS.py — Sam 10-10-2026 (Paris) — PROPOSÉ, non validé. Simulation uniquement.

① RÔLE — Relever, pour chaque valeur du référentiel, la table « Historique des divisions » que bnains publie sur la
  page de l'action (https://www.bnains.org/archives/action.php?codeISIN=<ISIN>) : date de la division, diviseur,
  dernier cours avant, commentaire (« Division du nominal par 4 », « Attribution d'une action gratuite pour
  quatre »…). Garder chaque page telle que reçue, comme témoin, et écrire la table en clair.
② CONTEXTE D'APPEL — À la main, quand une opération sur le capital doit être prouvée :
  python3 etudes/outils/RELEVER_LES_DIVISIONS_BNAINS.py <racine>. Sa table est lue par
  programmes/RECONSTRUIRE_L_HISTORIQUE_LONG.py.
③ ENTRÉE — La racine du dépôt.
④ CONDITIONS D'ENTRÉE — Le référentiel donnees/REFERENTIEL_VALEURS_*.csv (le plus récent par sa date, lu par
  `COMMUN.le_plus_recent`, jamais par l'alphabet) avec ses colonnes nom_usuel et isin ; l'accès à bnains.org.
⑤ SORTIE — UNE valeur : le code de sortie — 0 quand chaque page a été lue, 2 quand une page n'a pas pu l'être ou
  ne porte pas la table (R-734 : un relevé incomplet ne rend jamais 0). Écrit la table, les pages et leur liste.
⑥ TRAITEMENT — ① lire le référentiel · ② pour chaque ISIN, télécharger la page, l'écrire telle quelle dans
  temoins/PAGES_BNAINS_DES_ACTIONS/<ISIN>.html avec son empreinte · ③ `extraire` la table des divisions · ④ écrire
  donnees/sources_bnains/DIVISIONS_BNAINS.csv (une ligne par division) et
  temoins/PAGES_BNAINS_DES_ACTIONS/PAGES.csv (une ligne par page : empreinte, nombre de divisions lues).
⑦ UNITÉ — Des dates ISO ; le diviseur est un RAPPORT (2 = une action devient deux) ; le dernier cours est en euros,
  ou en francs quand bnains l'écrit « F » (la colonne devise le dit).
⑧ POURQUOI — Le 10-10-2026, la reconstruction a trouvé trois opérations que Yahoo a ajustées sans les déclarer et
  qu'aucun fichier du dépôt ne documentait : Société Générale (division par 4, 11-05-2000), Pernod Ricard (une
  action gratuite pour quatre, 14-02-2003), Eiffage (02-07-2001). La page de bnains donne les deux premières, avec
  le dernier cours avant l'opération, qui se confronte à l'extrait bnains au centime.
⑨ CE QUI CLOCHE — Une table VIDE ne prouve pas l'absence d'opération : celle d'Eiffage est vide, alors que Yahoo
  déclare trois divisions d'Eiffage (2004, 2005, 2006). · La page est du HTML : un changement de présentation chez
  bnains ferait lire zéro division ; c'est pourquoi une page sans l'en-tête de la table rend 2. · Le dernier cours
  de la page peut différer de l'extrait bnains (Carrefour, 10-04-2000 : 138,50 € sur la page, 136,50 € dans
  l'extrait) : ce relevé ne tranche pas, il écrit. · bnains a ses propres fautes : la date du dernier cours de la
  division de Danone du 15-06-2004 est « 30/11/-0001 », celle de Dassault Systèmes du 17-07-2014 est « 16/07/2007 » ;
  une date illisible est écrite telle quelle, précédée de « illisible chez bnains ». · Un changement d'ISIN coupe
  l'histoire : Michelin et Dassault Systèmes sont relus sous leur ancien ISIN (`ANCIENS_ISIN`) ; l'ancien ISIN
  d'Eurofins (FR0000038259) donne une page sans nom ni division, il n'est pas relu.
⑩ EFFET — Réseau : une requête par valeur. Écrit la table, les pages et leur liste. Affiche une ligne par page.
⑪ TERMINAISON — Rend la main : une requête par valeur, chacune bornée par `DELAI` secondes. Aucun de mes appels ne
  peut boucler.
"""
import csv, hashlib, html, os, re, sys, time, urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "programmes"))
from COMMUN import le_plus_recent

ADRESSE = "https://www.bnains.org/archives/action.php?codeISIN={}"
DELAI = 30                      # secondes accordées à une page
PAUSE = 1.0                     # secondes entre deux pages : ne pas presser le site
PAGES = os.path.join("temoins", "PAGES_BNAINS_DES_ACTIONS")
TABLE = os.path.join("donnees", "sources_bnains", "DIVISIONS_BNAINS.csv")
AUCUNE = "Aucune division référencée pour cette valeur."   # la seule ligne d'une table vide, lue le 10-10-2026
# Les ISIN d'avant un changement : la page de l'ISIN actuel ne porte pas l'histoire de l'ancien. Chaque ancien ISIN a
# été vérifié le 10-10-2026 par le titre de sa page chez bnains (« Michelin B », « Dassault Systèmes »).
ANCIENS_ISIN = {"MICHELIN": "FR0000121261", "DASSAULT SYSTEMES": "FR0000130650"}
CHAMPS = ["valeur", "isin", "date", "diviseur", "date_dernier_cours", "dernier_cours", "devise", "commentaire",
          "page", "sha256_page"]


def jour(s):
    """Rend la date ISO d'une date « JJ/MM/AAAA ».

    ① RÔLE — Écrire les dates comme partout au dépôt.
    ② CONTEXTE D'APPEL — `extraire`.
    ③ ENTRÉE — `s` : le texte d'une cellule.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « AAAA-MM-JJ ».
      [rend: 1]
    ⑥ TRAITEMENT — Retourner les trois nombres.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — bnains écrit les dates à la française.
    ⑨ CE QUI CLOCHE — Un texte qui n'est pas une date lève ValueError : la page ne se lit pas, et `main` rend 2.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir. [sort: non]
      [sort: non]
    """
    m = re.fullmatch(r"(\d\d)/(\d\d)/(\d{4})", s.strip())
    if not m:
        raise ValueError(f"date illisible : {s!r}")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"


def extraire(page):
    """Rend les lignes de la table des divisions d'une page, ou None si la table n'y est pas.

    ① RÔLE — Lire la table « Historique des divisions » d'une page d'action de bnains.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `page` : le texte HTML de la page.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None quand l'en-tête id="divisions" manque ; sinon la liste, éventuellement vide, des
      lignes (date, diviseur, date du dernier cours, dernier cours, devise, commentaire).
      [rend: 1]
    ⑥ TRAITEMENT — Prendre le texte entre l'en-tête id="divisions" et la fin de la première table qui suit ; dans
      chaque ligne <tr> du corps, les cinq cellules ; le cours « 240.800 &euro; » donne 240.8 et « EUR », « 4038.000 F »
      donne 4038.0 et « FRF ».
    ⑦ UNITÉ — Dates ISO ; diviseur sans unité ; cours dans la devise écrite.
    ⑧ POURQUOI — La table est la seule partie de la page qui sert ; la page entière est gardée à côté.
    ⑨ CE QUI CLOCHE — Une ligne qui n'a pas cinq cellules lève ValueError plutôt que d'être sautée en silence.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir. [sort: non]
      [sort: non]
    """
    i = page.find('id="divisions"')
    if i < 0:
        return None
    j = page.find("</table>", i)
    if j < 0:
        return None
    corps = page[i:j]
    k = corps.find("<tbody>")
    if k < 0:
        return []
    lignes = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", corps[k:], re.S):
        cellules = [html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
                    for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if cellules == [AUCUNE]:
            continue
        if len(cellules) != 5:
            raise ValueError(f"ligne de {len(cellules)} cellules : {cellules!r}")
        m = re.fullmatch(r"([\d.]+)\s*(€|F)", cellules[3])
        if not m:
            raise ValueError(f"cours illisible : {cellules[3]!r}")
        try:
            veille = jour(cellules[2])
        except ValueError:
            veille = "illisible chez bnains : " + cellules[2]
        lignes.append((jour(cellules[0]), float(cellules[1]), veille, float(m.group(1)),
                       "EUR" if m.group(2) == "€" else "FRF", cellules[4]))
    return lignes


def main(argv):
    """Relève toutes les pages, écrit la table ; rend le code de sortie.

    ① RÔLE — Porter la ligne de commande.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `argv` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — ④ du programme.
    ⑤ SORTIE — UNE valeur : 0 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — ⑧ du programme.
    ⑨ CE QUI CLOCHE — ⑨ du programme.
    ⑩ EFFET — ⑩ du programme.
    ⑪ TERMINAISON — Rend la main : une requête par valeur, bornée par `DELAI`. [sort: non]
      [sort: non]
    """
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : RELEVER_LES_DIVISIONS_BNAINS.py <racine>")
        return 2
    os.chdir(argv[0])
    d = "donnees"
    cands = [f for f in os.listdir(d) if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    if not cands:
        print("ARRÊT — référentiel introuvable")
        return 2
    valeurs = [(r["nom_usuel"], r["isin"]) for r in csv.DictReader(open(os.path.join(d, le_plus_recent(cands)),
                                                                        encoding="utf-8-sig"))]
    valeurs += sorted(ANCIENS_ISIN.items())
    os.makedirs(PAGES, exist_ok=True)
    sortie, liste, echecs = [], [], []
    for n, (valeur, isin) in enumerate(sorted(valeurs)):
        if n:
            time.sleep(PAUSE)
        url = ADRESSE.format(isin)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            octets = urllib.request.urlopen(req, timeout=DELAI).read()
            lignes = extraire(octets.decode("utf-8", errors="replace"))
        except (OSError, ValueError) as e:
            echecs.append(f"{valeur} : {type(e).__name__} : {e}")
            print(f"  ÉCHEC {valeur} ({isin}) : {type(e).__name__} : {e}")
            continue
        chemin = os.path.join(PAGES, f"{isin}.html")
        with open(chemin, "wb") as f:
            f.write(octets)
        sha = hashlib.sha256(octets).hexdigest()
        if lignes is None:
            echecs.append(f"{valeur} : la page ne porte pas la table des divisions")
            print(f"  ÉCHEC {valeur} ({isin}) : pas de table")
        liste.append([valeur, isin, url, chemin, len(octets), sha, "" if lignes is None else len(lignes)])
        for x in lignes or []:
            sortie.append([valeur, isin, x[0], f"{x[1]:g}", x[2], f"{x[3]:g}", x[4], x[5], url, sha])
        print(f"  {valeur} ({isin}) : {'—' if lignes is None else len(lignes)} division(s)")
    with open(TABLE, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(CHAMPS)
        w.writerows(sorted(sortie))
    with open(os.path.join(PAGES, "PAGES.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["valeur", "isin", "adresse", "page", "octets", "sha256", "divisions_lues"])
        w.writerows(liste)
    print(f"pages lues : {len(liste)} sur {len(valeurs)} · divisions : {len(sortie)} · échecs : {len(echecs)}")
    print(f"écrit : {TABLE} · {os.path.join(PAGES, 'PAGES.csv')}")
    return 2 if echecs else 0


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as e:
        print(f"ARRÊT — erreur imprévue {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
