"""DETECTER_PAR_L_INDICE.py — Jeu 08-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit.

À quoi il sert : contrôler l'historique long là où il n'a plus de seconde source — de mars 2017 à octobre 2026, Yahoo
est seul (bnains s'arrête au 28-02-2017). Deux mesures :
1. LE DÉTECTEUR À UNE SEULE SOURCE. L'indice CAC 40 est calculé par Euronext sur les clôtures officielles. Le poids de
   chaque valeur dans son mouvement se mesure sur les séances voisines ; une séance où les clôtures du fichier sont
   fausses laisse une trace : l'écart à l'indice sur le pas qui y entre, et l'écart opposé sur le pas qui en sort.
2. LA COMPARAISON AU FICHIER MAÎTRE, ligne à ligne, de janvier 2024 à octobre 2026 : donnees/cours_maitre.csv (Google,
   validé contre FactSet, puis ABC Bourse) y est une vraie seconde source.

Comment s'en servir : python3 -I etudes/outils/DETECTER_PAR_L_INDICE.py <racine du dépôt>
Il se CALIBRE d'abord (code 1 s'il échoue) : sur le fichier Yahoo d'origine, il doit trouver le 07-05-2010 (les
clôtures de Yahoo y sont fausses, l'arbitre à deux sources l'a prouvé) ; sur le fichier réparé, il ne doit plus le
trouver ; et la comparaison au maître doit retrouver une erreur de 10 % fabriquée en mémoire sur une ligne réelle (le
cas réel qui l'avait calibrée, Air Liquide 08-06-2026, a été corrigé au maître le 08-10-2026 par décision de Jean-Luc,
R-107 : un calibrage ne peut pas reposer sur une erreur qu'on corrige).
Simulation uniquement. N'écrit rien.
"""
import csv, datetime, os, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
import CONTROLER_L_HISTORIQUE_LONG as K                 # lire_cours, resoudre, chemins (R-708)
from CONTRATS_DES_FICHIERS import INDICE_CAC40

MAITRE = os.path.join("donnees", "cours_maitre.csv")
BLOC = 20          # séances dont les poids sont mesurés ensemble
DEMI = 125         # séances prises de chaque côté du bloc pour mesurer les poids
SEUIL = 4.0        # une séance est suspecte quand son score dépasse 4 bruits
ECART_MAITRE = 0.005   # une ligne s'écarte du maître quand son rapport bouge de plus de 0,5 % de sa médiane locale


def lire_indice_yahoo(chemin):
    """Lit la colonne yahoo de l'indice CAC 40 ; rend date → clôture.

    ① RÔLE — Donner au détecteur l'indice de chaque séance, y compris après le 28-02-2017 où bnains n'a plus rien.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `chemin` : donnees/sources_indice/INDICE_CAC40.csv.
    ④ CONDITIONS D'ENTRÉE — L'en-tête est celui du contrat `INDICE_CAC40`.
    ⑤ SORTIE — UNE valeur : le dictionnaire date → clôture de Yahoo, pour les cases lisibles et positives. Lève
      ValueError si l'en-tête n'est pas celui du contrat.
      [rend: 1]
    ⑥ TRAITEMENT — Vérifier l'en-tête ; garder chaque clôture yahoo positive.
    ⑦ UNITÉ — Des POINTS d'indice.
    ⑧ POURQUOI — `K.lire_indice` exige les deux relevés et ne rend donc rien après 2017 : c'est voulu pour
      l'arbitre, qui doit croire l'indice ; le détecteur, lui, n'a que Yahoo après 2017.
    ⑨ CE QUI CLOCHE — Un indice faux chez Yahoo fait une séance suspecte comme une clôture fausse : mesuré le
      08-10-2026, le 19-12-2013 et le 27-06-2016, où l'indice de Yahoo diffère de celui de bnains, sont signalés.
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    indice = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != INDICE_CAC40:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {INDICE_CAC40}")
        for r in lecteur:
            try:
                x = float(r["yahoo"])
            except ValueError:
                continue
            if x > 0:
                indice[r["date"]] = x
    return indice


def residus(series, indice, du, au):
    """Mesure, pour chaque pas d'une séance à la suivante, l'écart du mouvement de l'indice au mouvement pondéré du fichier.

    ① RÔLE — Le cœur du détecteur : ce que les clôtures du fichier n'expliquent pas du mouvement de l'indice.
    ② CONTEXTE D'APPEL — `main`, sur le fichier d'origine et sur le fichier réparé.
    ③ ENTRÉE — `series` : valeur → {date: barre} (`K.lire_cours`) · `indice` : date → clôture · `du`, `au` : dates.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des pas (date d'arrivée, résidu, bruit), le résidu en rendement (0,01 = 1 point),
      le bruit étant l'écart absolu médian des résidus du bloc, ramené à un écart-type (× 1,4826).
      [rend: 1]
    ⑥ TRAITEMENT — Les séances de l'indice entre `du` et `au`, par blocs de `BLOC` pas : ① les valeurs qui ont une
      clôture à chaque séance de `DEMI` pas avant le bloc à `DEMI` pas après · ② leurs poids, par moindres carrés
      régularisés de `K.CRETE` (`K.resoudre`) du rendement de l'indice sur leurs rendements · ③ le résidu de chaque pas
      du bloc.
    ⑦ UNITÉ — Des RENDEMENTS.
    ⑧ POURQUOI — Mesuré le 08-10-2026 : depuis 2017, nos 39 valeurs expliquent l'indice à 0,025-0,037 point près par
      séance ; de 2000 à 2016, à 0,05-0,24 point près, la composition de l'indice ayant plus changé.
    ⑨ CE QUI CLOCHE — Une valeur de l'indice absente de nos 39 qui fait un grand mouvement fait un résidu que rien ne
      répare. · Une valeur à qui il manque une seule séance dans la fenêtre sort du calcul de tout le bloc.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Toujours : un nombre fini de blocs, chacun un système de la taille du nombre de valeurs.
      [sort: non]
    """
    jours = [d for d in sorted(indice) if du <= d <= au]
    vals = sorted(series)
    pas = []
    for a, z in zip(jours, jours[1:]):
        r = [series[v][z][3] / series[v][a][3] - 1 if a in series[v] and z in series[v] and series[v][a][3] > 0
             else None for v in vals]
        pas.append((z, indice[z] / indice[a] - 1, r))
    sortie = []
    for b0 in range(0, len(pas), BLOC):
        lo, hi = max(0, b0 - DEMI), min(len(pas), b0 + BLOC + DEMI)
        cols = [k for k in range(len(vals)) if all(pas[t][2][k] is not None for t in range(lo, hi))]
        X = [[pas[t][2][k] for k in cols] for t in range(lo, hi)]
        y = [pas[t][1] for t in range(lo, hi)]
        n = len(cols)
        a = [[sum(l[i] * l[j] for l in X) + (K.CRETE if i == j else 0) for j in range(n)] for i in range(n)]
        w = K.resoudre(a, [sum(l[i] * c for l, c in zip(X, y)) for i in range(n)])
        e = [c - sum(wi * xi for wi, xi in zip(w, l)) for l, c in zip(X, y)]
        bruit = statistics.median(abs(x) for x in e) * 1.4826
        for t in range(b0, min(b0 + BLOC, len(pas))):
            sortie.append((pas[t][0], e[t - lo], bruit))
    return sortie


def seances_suspectes(res):
    """Rend les séances dont l'entrée et la sortie s'écartent de l'indice en sens opposés, au-delà de `SEUIL`.

    ① RÔLE — Reconnaître la trace d'une séance fausse : un écart en y entrant, l'écart opposé en en sortant.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `res` : `residus`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste (date, résidu d'entrée, résidu de sortie, bruit, score), score =
      |entrée − sortie| ÷ (bruit × √2), en bruits ; seulement les signes opposés et les scores au-delà de `SEUIL`.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque séance, l'entrée est le résidu du pas qui y arrive, la sortie celui du pas suivant.
    ⑦ UNITÉ — Des RENDEMENTS ; le score en nombre de bruits.
    ⑧ POURQUOI — Une clôture fausse de e % le jour z fausse le rendement de z−1 à z de +e et celui de z à z+1 de −e ;
      exiger les deux, de signes opposés, écarte le simple bruit. Calibré le 08-10-2026 sur 2000-2017 : au seuil de 4,
      les quatre suites où l'arbitre à deux sources donne tort à Yahoo (05-07-2007, 26-07-2007, 07-05-2010, septembre
      2011) sont trouvées ; une seule jambe forte, sans l'autre, ne suffit pas toujours (05-07-2007 : −1,6 et +4,0).
    ⑨ CE QUI CLOCHE — Une suite de plusieurs séances fausses du même sens ne laisse de trace qu'à ses bords.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    cas = []
    for (d0, e0, b0), (d1, e1, b1) in zip(res, res[1:]):
        a, b = e0 / b0, e1 / b1
        score = abs(a - b) / 2 ** 0.5
        if a * b < 0 and score > SEUIL:
            cas.append((d0, e0, e1, b0, score))
    return cas


def comparer_au_maitre(series, maitre):
    """Compare chaque clôture du fichier à celle du fichier maître, rapportée à sa médiane sur les séances voisines.

    ① RÔLE — Vérifier 2024-2026, où le fichier maître est une vraie seconde source.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `series` : le fichier réparé · `maitre` : `K.lire_cours` sur donnees/cours_maitre.csv, avec les noms
      ramenés à une seule graphie (le maître écrit « AIR_LIQUIDE » depuis le 13-07-2026, « AIR LIQUIDE » avant).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le nombre de lignes comparées, et la liste des cas (valeur, date, écart, clôture du
      fichier, clôture du maître) dont le rapport fichier ÷ maître s'écarte de plus de `ECART_MAITRE` de sa médiane
      sur les 10 séances communes de chaque côté.
      [rend: 2]
    ⑥ TRAITEMENT — Par valeur, les séances communes ; le rapport ; sa médiane locale ; l'écart.
    ⑦ UNITÉ — Des RAPPORTS sans unité.
    ⑧ POURQUOI — Les deux fichiers n'ajustent pas forcément les mêmes événements : on compare au rapport local, pas à
      1. Mesuré le 08-10-2026 : 27 335 lignes, 3 cas, aucun où Yahoo a tort.
    ⑨ CE QUI CLOCHE — Un changement de convention entre les deux fichiers (EssilorLuxottica, 06-05-2024) ne fait un
      cas qu'à ses bords.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    n, cas = 0, []
    for v in sorted(series):
        if v not in maitre:
            continue
        ds = [d for d in sorted(series[v]) if d in maitre[v] and maitre[v][d][3] > 0 and series[v][d][3] > 0]
        q = {d: series[v][d][3] / maitre[v][d][3] for d in ds}
        for i, d in enumerate(ds):
            n += 1
            vois = [q[x] for x in ds[max(0, i - 10):i] + ds[i + 1:i + 11]]
            if not vois:
                continue
            e = q[d] / statistics.median(vois) - 1
            if abs(e) > ECART_MAITRE:
                cas.append((v, d, e, series[v][d][3], maitre[v][d][3]))
    return n, cas


def main(argv):
    """Calibre le détecteur, l'applique à 2017-2026, compare au maître ; rend le code de sortie.

    ① RÔLE — Dire si l'historique long réparé est juste là où il n'a plus de seconde source.
    ② CONTEXTE D'APPEL — À la main. Aucun circuit ne le lance.
    ③ ENTRÉE — `argv` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le fichier Yahoo d'origine, le fichier réparé, l'indice et le fichier maître existent.
    ⑤ SORTIE — UNE valeur : 0 quand le calibrage passe, 1 s'il échoue (rien d'autre n'est alors mesuré), 2 si un
      fichier manque ou est illisible.
      [rend: 1]
    ⑥ TRAITEMENT — ① CALIBRAGE, 2006-2012 : le fichier d'origine doit faire du 07-05-2010 une séance suspecte, le
      fichier réparé non · ② les séances suspectes du fichier réparé du 01-03-2017 au 02-10-2026 · ③ la comparaison
      au maître · ④ la même comparaison sur une copie du maître où la clôture d'Air Liquide du 10-06-2026 est
      multipliée par 1,1 : elle doit trouver cette ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un détecteur qui ne retrouve pas un cas connu ne prouve rien quand il ne trouve rien ; et un cas
      corrigé qu'il trouverait encore ferait de lui un générateur d'alarmes.
    ⑨ CE QUI CLOCHE — Le calibrage ne porte que sur une séance de chaque sorte. · Le cas du maître est fabriqué :
      le cas réel (Air Liquide, 08-06-2026) a été corrigé au maître le 08-10-2026 (R-107).
    ⑩ EFFET — Affiche. N'écrit rien.
    ⑪ TERMINAISON — Toujours.
      [sort: non]
    """
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        print("USAGE : DETECTER_PAR_L_INDICE.py <racine>")
        return 2
    r = argv[0]
    try:
        indice = lire_indice_yahoo(os.path.join(r, K.INDICE))
        origine, _, _ = K.lire_cours(os.path.join(r, K.ORIGINE))
        repare, _, _ = K.lire_cours(os.path.join(r, K.FICHIER))
        brut, _, _ = K.lire_cours(os.path.join(r, MAITRE))
    except (OSError, ValueError) as e:
        print(f"ARRÊT — {type(e).__name__} : {e}")
        return 2
    maitre = {}
    for v, s in brut.items():
        maitre.setdefault(v.replace("_", " "), {}).update(s)
    o = [c[0] for c in seances_suspectes(residus(origine, indice, "2006-01-01", "2012-12-31"))]
    p = [c[0] for c in seances_suspectes(residus(repare, indice, "2006-01-01", "2012-12-31"))]
    print(f"calibrage 2006-2012 — fichier d'origine : {len(o)} séances suspectes, 07-05-2010 trouvé : {'2010-05-07' in o}"
          f" · fichier réparé : {len(p)}, 07-05-2010 trouvé : {'2010-05-07' in p}")
    if "2010-05-07" not in o or "2010-05-07" in p:
        print("CALIBRAGE ÉCHOUÉ — rien d'autre n'est mesuré")
        return 1
    fin = max(indice)
    cas = seances_suspectes(residus(repare, indice, "2016-09-01", fin))
    cas = [c for c in cas if c[0] >= "2017-03-01"]
    print(f"séances suspectes du fichier réparé, 01-03-2017 → {fin} : {len(cas)}")
    for d, e0, e1, b, s in cas:
        print(f"  {d} entrée {100 * e0:+.2f} pt, sortie {100 * e1:+.2f} pt, bruit {100 * b:.3f} pt, score {s:.1f}")
    n, ecarts = comparer_au_maitre(repare, maitre)
    print(f"comparaison au fichier maître : {n} lignes, {len(ecarts)} à plus de {ECART_MAITRE:.1%} de leur rapport local")
    for v, d, e, cf, cm in ecarts:
        print(f"  {v} {d} écart {100 * e:+.2f} % — fichier réparé {cf}, maître {cm}")
    faux = {v: dict(s) for v, s in maitre.items()}
    jour = "2026-06-10"
    if jour not in faux.get("AIR LIQUIDE", {}):
        print(f"CALIBRAGE ÉCHOUÉ — le maître n'a pas la ligne AIR LIQUIDE du {jour} sur laquelle fabriquer l'erreur")
        return 1
    b = faux["AIR LIQUIDE"][jour]
    faux["AIR LIQUIDE"][jour] = b[:3] + (b[3] * 1.1,) + b[4:]
    _, trouves = comparer_au_maitre(repare, faux)
    print(f"calibrage de la comparaison : une erreur de 10 % fabriquée sur AIR LIQUIDE {jour} — trouvée : "
          f"{any(v == 'AIR LIQUIDE' and d == jour for v, d, *_ in trouves)}")
    if not any(v == "AIR LIQUIDE" and d == jour for v, d, *_ in trouves):
        print("CALIBRAGE ÉCHOUÉ — la comparaison au maître ne retrouve pas l'erreur fabriquée")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
