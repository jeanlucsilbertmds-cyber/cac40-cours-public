"""LIRE_L_INDICE_CAC40.py — Mer 07-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit.

À quoi il sert : poser au dépôt l'indice CAC 40 de chaque séance du 03-01-2000 au 28-02-2017, relevé à DEUX
sources indépendantes — les archives quotidiennes de bnains.org (ligne « CAC 40 ») et Yahoo (^FCHI). L'indice est
calculé par Euronext à partir des clôtures officielles des valeurs : une séance où Yahoo et bnains se contredisent
sur plusieurs valeurs, il dit laquelle des deux porte les vraies clôtures (`arbitre_de_l_indice`, dans
programmes/CONTROLER_L_HISTORIQUE_LONG.py). Mesuré le 07-10-2026 : 07-05-2010, les clôtures de Paris reproduisent
l'indice, celles de Yahoo s'en écartent de 7,5 points.
Du 01-03-2017 au 02-10-2026, bnains n'a plus rien : seule la colonne yahoo est remplie. Ces séances-là ne
servent pas à l'arbitre (`lire_indice` exige les deux relevés) ; elles servent au détecteur à une seule source,
etudes/outils/DETECTER_PAR_L_INDICE.py (08-10-2026), qui cherche les séances où les clôtures de Yahoo, pondérées,
s'écartent du mouvement de l'indice. Mesuré le 08-10-2026 : l'indice de Yahoo est identique à celui d'Euronext
(live.euronext.com, qui ne remonte qu'à octobre 2024) le 08-08-2025, 7 743,00.

Comment s'en servir :
1. Télécharger les archives de bnains : python3 programmes/LIRE_LES_ARCHIVES_BNAINS.py <racine> <dossier> --telecharger
2. python3 -I etudes/outils/LIRE_L_INDICE_CAC40.py <racine du dépôt> <dossier des archives bnains> <dossier de travail>
3. Le dossier de travail reçoit l'indice de Yahoo téléchargé (FCHI_2000_2026.json) ; s'il y est déjà, il n'est pas
   retéléchargé. Sortie : donnees/sources_indice/INDICE_CAC40.csv (contrat INDICE_CAC40).
Simulation uniquement.
"""
import collections, csv, datetime, io, json, os, re, sys, urllib.request, zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
from CONTRATS_DES_FICHIERS import INDICE_CAC40   # les champs, déclarés une fois (R-708)

SORTIE = os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv")
LIBELLE = "CAC 40"      # le libellé exact de la ligne de l'indice dans les fichiers quotidiens de bnains
FIGEE = 5               # une clôture répétée à l'identique sur plus de 5 séances est une ligne figée
FIN = "2026-10-02"      # dernière séance du fichier Yahoo des 26 ans (bnains s'arrête au 28-02-2017 ; après, Yahoo seul)
ADRESSE = ("https://query2.finance.yahoo.com/v8/finance/chart/%5EFCHI?period1=946684800&period2=1790985600"
           "&interval=1d")
UA = "Mozilla/5.0"


def lire_bnains(dossier):
    """Lit, dans toutes les archives de bnains, les lignes de l'indice ; rend date → liste de clôtures.

    ① RÔLE — Relever l'indice tel que bnains l'a archivé, séance par séance, sans rien choisir.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `dossier` : les archives annuelles et mensuelles de bnains (2000.ZIP … 201702.ZIP).
    ④ CONDITIONS D'ENTRÉE — Les archives sont celles que programmes/LIRE_LES_ARCHIVES_BNAINS.py télécharge.
    ⑤ SORTIE — UNE valeur : le dictionnaire date ISO → liste triée des clôtures DIFFÉRENTES lues ce jour-là sous
      le libellé `LIBELLE` (plusieurs quand bnains en porte plusieurs ; une ligne répétée à l'identique compte une
      fois — mesuré le 07-10-2026 : 107 séances de 2000, 2005 et 2006 portent deux fois la même ligne).
      [rend: 1]
    ⑥ TRAITEMENT — Ouvrir chaque archive, puis les archives qu'elle contient ; dans chaque fichier AAAAMMJJ.txt,
      garder les lignes dont la deuxième colonne vaut `LIBELLE`, et leur sixième (la clôture), virgule décimale
      ramenée au point.
    ⑦ UNITÉ — Des POINTS d'indice ; des dates de séance.
    ⑧ POURQUOI — Mesuré le 07-10-2026 : les fichiers des années 2000 à 2003 écrivent parfois la clôture avec une
      virgule (« 5672,95 », 18-01-2000).
    ⑨ CE QUI CLOCHE — Les fichiers qui ne sont ni des archives ni des AAAAMMJJ.txt sont ignorés sans être nommés.
    ⑩ EFFET — Lit les archives. N'écrit rien.
    ⑪ TERMINAISON — Toujours : un nombre fini d'archives, chacune lue une fois.
      [sort: non]
    """
    lignes = collections.defaultdict(list)

    def lire(z):
        """Parcourt une archive et celles qu'elle contient ; ajoute à `lignes` chaque clôture de l'indice.

        ① RÔLE — Descendre dans les archives emboîtées de bnains (année → mois → séance).
        ② CONTEXTE D'APPEL — `lire_bnains`, sur chaque archive annuelle ou mensuelle, puis sur elle-même.
        ③ ENTRÉE — `z` : une archive ouverte (zipfile.ZipFile).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — AUCUNE valeur : elle remplit `lignes`, de l'appelant.
          [rend: 0]
        ⑥ TRAITEMENT — Pour chaque nom : une archive → s'y appeler ; un AAAAMMJJ.txt → garder les lignes du
          libellé `LIBELLE` ; le reste → l'ignorer, sans le lire.
        ⑦ UNITÉ — Des POINTS d'indice, en texte.
        ⑧ POURQUOI — Mesuré le 07-10-2026 : un fichier « infos et mises à jour.htm » de l'archive porte un nom
          dont l'en-tête diffère du répertoire ; le lire lève BadZipFile. On ne lit donc que ce qui sert.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie `lignes`.
        ⑪ TERMINAISON — Toujours : la profondeur des archives emboîtées est finie.
          [sort: non]
        """
        for n in z.namelist():
            jour = re.search(r"(\d{8})\.txt$", n, re.I)
            if n.upper().endswith(".ZIP"):
                lire(zipfile.ZipFile(io.BytesIO(z.read(n))))
            elif jour:
                d = jour.group(1)
                for l in z.read(n).decode("latin-1").splitlines():
                    c = l.split("\t")
                    if len(c) >= 6 and c[1].strip() == LIBELLE:
                        lignes[f"{d[:4]}-{d[4:6]}-{d[6:]}"].append(c[5].strip().replace(",", "."))

    for a in sorted(os.listdir(dossier)):
        if re.fullmatch(r"\d{4}(\d{2})?\.ZIP", a, re.I):
            lire(zipfile.ZipFile(os.path.join(dossier, a)))
    return {d: sorted(set(v)) for d, v in lignes.items()}


def une_cloture(lignes):
    """Garde, pour chaque séance, la seule clôture de bnains qui n'est pas figée ; rend (date → clôture, écartées).

    ① RÔLE — Dire quelle ligne de bnains est l'indice quand bnains en porte plusieurs.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `lignes` : `lire_bnains`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le dictionnaire date → clôture (nombre), pour les séances où il reste exactement une
      clôture lisible une fois les clôtures figées ôtées ; et la liste des séances écartées (aucune ou plusieurs).
      [rend: 2]
    ⑥ TRAITEMENT — ① compter chaque clôture sur toutes les séances · ② ôter celles qui se répètent sur plus de
      `FIGEE` séances · ③ garder la séance s'il reste une clôture.
    ⑦ UNITÉ — Des POINTS d'indice.
    ⑧ POURQUOI — Mesuré le 07-10-2026 : du 01-08-2011 au 22-07-2013, bnains porte une seconde ligne « CAC 40 »
      figée à 3 348,63 sur 277 séances, à côté de la vraie. Un indice réel ne reste jamais six séances au même
      centième.
    ⑨ CE QUI CLOCHE — Le 22-07-2013, bnains porte cinq clôtures différentes : la séance est écartée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    compte = collections.Counter(x for v in lignes.values() for x in v)
    gardees, ecartees = {}, []
    for d, v in sorted(lignes.items()):
        reste = []
        for x in v:
            try:
                if compte[x] <= FIGEE:
                    reste.append(float(x))
            except ValueError:
                pass
        if len(reste) == 1 and reste[0] > 0:
            gardees[d] = reste[0]
        else:
            ecartees.append(d)
    return gardees, ecartees


def main(argv):
    """Relève l'indice chez bnains et chez Yahoo, les confronte, écrit le fichier ; rend le code de sortie.

    ① RÔLE — Poser au dépôt l'indice CAC 40 à deux sources, et dire où elles s'accordent.
    ② CONTEXTE D'APPEL — À la main, une fois. Aucun circuit ne le lance.
    ③ ENTRÉE — `argv` : la racine du dépôt, le dossier des archives de bnains, le dossier de travail.
    ④ CONDITIONS D'ENTRÉE — Les archives sont dans leur dossier ; le réseau joint query2.finance.yahoo.com, ou le
      dossier de travail contient déjà FCHI_2000_2026.json.
    ⑤ SORTIE — UNE valeur : 0 quand le fichier est écrit, 2 sinon (arguments, téléchargement, lecture).
      [rend: 1]
    ⑥ TRAITEMENT — ① `lire_bnains`, puis `une_cloture` · ② télécharger ^FCHI si FCHI_2000_2026.json manque · ③ écrire une
      ligne par séance connue de l'une ou l'autre source jusqu'au `FIN`, case vide quand une source n'a rien ·
      ④ afficher le nombre de séances communes et celles où les deux sources s'écartent de plus de 0,05 %.
    ⑦ UNITÉ — Des POINTS d'indice.
    ⑧ POURQUOI — Une source seule peut se tromper ; deux sources qui s'accordent font un fait. Mesuré le
      07-10-2026 : 4 358 séances communes, 7 à plus de 0,05 % — dont le 19 et le 20-06-2001, où bnains porte
      les deux clôtures interverties.
    ⑨ CE QUI CLOCHE — Yahoo donne l'heure de chaque séance en secondes depuis 1970 : la date est prise en temps
      universel, qui tombe le même jour que la séance de Paris (ouverture à 9 h).
    ⑩ EFFET — Écrit donnees/sources_indice/INDICE_CAC40.csv en le remplaçant ; écrit FCHI_2000_2026.json dans le dossier de
      travail s'il manquait. Réseau.
    ⑪ TERMINAISON — Le téléchargement est borné à 60 secondes, sans nouvel essai.
      [sort: non]
    """
    if len(argv) != 3 or not all(os.path.isdir(x) for x in argv):
        print("USAGE : LIRE_L_INDICE_CAC40.py <racine> <dossier des archives bnains> <dossier de travail>")
        return 2
    racine, archives, travail = argv
    try:
        bnains, ecartees = une_cloture(lire_bnains(archives))
        cache = os.path.join(travail, "FCHI_2000_2026.json")
        if not os.path.exists(cache):
            with urllib.request.urlopen(urllib.request.Request(ADRESSE, headers={"User-Agent": UA}), timeout=60) as r:
                open(cache, "wb").write(r.read())
        r = json.load(open(cache, encoding="utf-8"))["chart"]["result"][0]
    except (OSError, ValueError, KeyError, IndexError, zipfile.BadZipFile) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    yahoo = {}
    for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        d = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).date().isoformat()
        if c is not None and c > 0 and d <= FIN:
            yahoo[d] = round(c, 2)
    communes = sorted(set(bnains) & set(yahoo))
    ecarts = [d for d in communes if abs(yahoo[d] / bnains[d] - 1) > 0.0005]
    cible = os.path.join(racine, SORTIE)
    os.makedirs(os.path.dirname(cible), exist_ok=True)
    with open(cible + ".partiel", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(INDICE_CAC40)
        for d in sorted(set(bnains) | set(yahoo)):
            w.writerow([d, bnains.get(d, ""), yahoo.get(d, "")])
    os.replace(cible + ".partiel", cible)
    print(f"bnains : {len(bnains)} séances ({len(ecartees)} écartées : {ecartees}) · Yahoo : {len(yahoo)} · "
          f"communes : {len(communes)} · à plus de 0,05 % l'une de l'autre : {len(ecarts)} {ecarts}")
    print(f"écrit : {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
