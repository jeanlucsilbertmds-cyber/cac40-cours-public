#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INVENTORIER_LES_VINGT_ANS.py — Mer 11-11-2026 23h20 (Paris). Simulation uniquement. LECTURE SEULE.

① RÔLE — Mesurer, part par part, ce qui existe au dépôt pour le fichier des 20 ans (2000-2026, à part du fichier
  maître, plan V7 bloc 7 révisé le 11-11-2026 à 18h04) : pour chaque part, sa source, sa convention de prix
  (cours BRUT de Paris, ou courbe AJUSTÉE à ramener au brut — décision de Jean-Luc du 11-11-2026 à 20h52, R-108
  telle quelle), sa clé (la société est-elle nommée par un mnémonique du référentiel, ou par un numéro de
  IDENTITES_DES_SOCIETES.csv ?), et ce qui bloque le juge sur 2000-2026 côté frais (la taxe sur les transactions
  financières, A-550).
② CONTEXTE D'APPEL — À la main, par l'agent E2 du plan V7 ou par son épreuve
  (tests/EPREUVES_DE_L_INVENTAIRE_DES_VINGT_ANS_Mer_11-11-2026.py) :
  python3 -I INVENTORIER_LES_VINGT_ANS.py <racine> [--saboter S1|…|S6]
③ ENTRÉE — La racine d'un dépôt (ses fichiers sont lus, jamais écrits) ; facultatif, un sabotage nommé.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/RECONSTRUIRE_L_HISTORIQUE_LONG.py et ses entrées (④ de ce
  programme), programmes/MODULE_POSITIONS.py et ses deux tables de frais, le référentiel des valeurs,
  donnees/sources_indice/{INDICE_CAC40,PASSAGES_DANS_LE_CAC40,IDENTITES_DES_SOCIETES}.csv, les barres des sociétés
  sorties (N3) et etudes/VINGT_ANS_PAR_YAHOO_Dim_08-11-2026/sorties/A_VERSER.csv.
⑤ SORTIE — UNE valeur : le code de sortie — 0 si tous les calibrages passent, 1 si l'un échoue, 2 si le programme
  n'a pas pu tourner (R-734). À l'écran : une ligne par mesure, puis une ligne par calibrage. [rend: 1]
⑥ TRAITEMENT — ① historique long : chaque ligne reçoit le facteur des opérations sur titre postérieures
  (`RECONSTRUIRE_L_HISTORIQUE_LONG.facteur_apres`) ; facteur 1 = déjà au brut, autre = à ramener au brut
  (cours ÷ facteur), inconnu = impossible à ramener ; compté par période · ② bnains, maître, N3, A_VERSER :
  lignes, sources, dates · ③ clés : sociétés de PASSAGES absentes de IDENTITES ; noms de A_VERSER absents du
  référentiel · ④ frais : pour la première séance de chaque année, le coût d'un achat est demandé à
  `MODULE_POSITIONS.cout_d_un_ordre` ; une année qui lève est une année où le juge s'arrête · ⑤ calibrages.
⑦ UNITÉ — Des lignes (une valeur × une séance) ; des RAPPORTS sans unité pour les facteurs ; des euros.
⑧ POURQUOI — Le cadre de la mission E2 exige un inventaire mesuré AVANT tout code d'assemblage (R-708 : étendre ce
  qui existe ; R-728 : ce qui se mesure ne s'écrit pas à la main). La couverture (jours-membres couverts ou non) est
  déjà mesurée par etudes/RECOMPTE_DES_20_ANS_Dim_08-11-2026/recompter.py : ce programme ne la refait pas ; il
  mesure ce que le recompte ne dit pas (convention des prix, clé, frais).
⑨ CE QUI CLOCHE — K3, K4 et K5 sont des CONSTATS D'ÉTAT (relecteur E2a, D2) : ils confrontent ce que le programme
  rapporte à une seconde lecture brute des fichiers, et restent verts quand le défaut est réparé (lot d'octobre,
  numéros 41+). Depuis le 12-11-2026 (tour 3, lot installé et numéros 41 à 78 attribués), K3 et K4 portent chacun
  un CONTRE-CAS qui doit échouer (l'année qui suit la dernière liste de taxe doit arrêter le juge ; un code absent
  des identités doit être vu sans numéro), sans quoi S2 et S3 ne mordaient plus. K6 admet une différence avec
  RECONSTRUCTION_ECARTS.csv (non refait par le lot) seulement si le journal des réparations ou les barres de Paris
  rectifiées portent ce (valeur, date) : 8 différences le 12-11-2026, toutes expliquées. · K3 RELIT LE MÊME BARÈME
  QUE LE CALCUL (MODULE_POSITIONS.cout_d_un_ordre lit donnees/BAREME_FRAIS.csv, K3 aussi) : il est tautologique et ne
  peut pas voir une DONNÉE fausse — une date de début avancée ou effacée change les deux côtés pareil (relecteur E2a du
  tour 3, D1 : début du 0,2 % avancé au 2012-01-01, K3 resté vert). Le filet sur les dates du barème est
  tests/EPREUVES_DES_DATES_DU_BAREME_Jeu_12-11-2026.py (superviseur R-759 du 12-11-2026 : K3 laissé tel quel). · Le facteur d'une ligne est celui de la liste des opérations que RECONSTRUIRE sait écrire : une
  opération absente de toutes ses sources laisse la ligne comptée « déjà au brut » à tort (son ⑨, exemple Sagem
  2003). · Le maître (Google) n'est pas confronté au brut ici : RECONSTRUIRE le dit déjà corrigé des divisions
  par Google. · Le coût de la taxe n'est demandé que pour ACCOR, à la première séance de l'année : il suffit à dire
  si l'année bloque (la liste annuelle manque pour toutes les valeurs à la fois), pas si une valeur précise y est.
⑩ EFFET — Lit des fichiers ; n'écrit rien (RECONSTRUIRE est appelé fonction par fonction, jamais par son `main`,
  qui écrit deux tables).
⑪ TERMINAISON — Rend la main : chaque étape parcourt un nombre fini de lignes ; aucun appel réseau. Aucun de mes
  appels ne peut ne pas revenir.
"""
import collections, csv, datetime, glob, gzip, hashlib, json, os, sys

SABOTAGES = ("S1", "S2", "S3", "S4", "S5", "S6")


# A-842 (16-11-2026) : empreinte sha256 de « valeur;date;close » de la vraie ligne ALSTOM 2006-08-01 de A_VERSER.csv,
# calculée sur cette ligne le 16-11-2026 ; aucun cours en clair dans ce fichier.
EMPREINTE_ALSTOM_2006_08_01 = "fc4a91aee13f76483aa6f46e21b1353fcd151371c056a4b613a8c3c8547546d0"


def lire(chemin):
    """Lit un tableau CSV (éventuellement compressé).

    ① RÔLE — Rendre les lignes d'un CSV en dictionnaires.
    ② CONTEXTE D'APPEL — `mesurer`, pour chaque fichier lu.
    ③ ENTRÉE — `chemin` : un fichier .csv ou .csv.gz.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (sinon `OSError`, que `principal` change en code 2).
    ⑤ SORTIE — UNE valeur : la liste des lignes. [rend: 1]
    ⑥ TRAITEMENT — Ouvrir (gzip si .gz), lire avec l'en-tête, ôter une marque d'ordre des octets.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un seul lecteur pour tous les fichiers de l'inventaire.
    ⑨ CE QUI CLOCHE — Une ligne de commentaire en tête (« # DÉCIDÉ… ») n'est pas sautée : aucun fichier lu ici n'en
      porte, sauf VALEURS_TTF et BAREME_FRAIS, qui ne sont lus que par MODULE_POSITIONS.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève `OSError`. [sort: non]
    """
    ouvrir = gzip.open if chemin.endswith(".gz") else open
    with ouvrir(chemin, "rt", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def lire_sans_commentaire(chemin):
    """Lit un CSV dont la première ligne peut être un commentaire « # ».

    ① RÔLE — Relire BRUT le barème des frais et la liste des valeurs taxées, sans passer par MODULE_POSITIONS.
    ② CONTEXTE D'APPEL — `mesurer`, pour le calibrage K3.
    ③ ENTRÉE — `chemin` : un fichier CSV.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : la liste des lignes. [rend: 1]
    ⑥ TRAITEMENT — Sauter les lignes qui commencent par « # », lire le reste avec l'en-tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — K3 confronte ce que le mécanisme de frais rend à ce que les fichiers disent : la seconde lecture
      doit venir d'un autre chemin que la première (relecteur E2a, D1 et D2).
    ⑨ CE QUI CLOCHE — Ne vérifie pas le contrat du fichier (MODULE_POSITIONS le fait).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève `OSError`. [sort: non]
    """
    with open(chemin, encoding="utf-8-sig") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def classe_du_facteur(p, s1):
    """Range le facteur d'une ligne de l'historique long.

    ① RÔLE — Dire si une ligne est déjà au cours brut, à ramener au brut, ou impossible à ramener.
    ② CONTEXTE D'APPEL — `mesurer`, pour chaque ligne de l'historique long.
    ③ ENTRÉE — `p` : le produit des facteurs des opérations postérieures (`facteur_apres`), ou None · `s1` : vrai
      sous le sabotage S1 (tout facteur lu comme 1).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « déjà au brut », « à ramener au brut » ou « facteur inconnu ». [rend: 1]
    ⑥ TRAITEMENT — None → inconnu ; |p − 1| < 1e-12 → déjà au brut ; sinon à ramener.
    ⑦ UNITÉ — Un RAPPORT sans unité.
    ⑧ POURQUOI — R-108 ① : le fichier des 20 ans garde le vrai cours ; une ligne de courbe ajustée n'y entre qu'une
      fois divisée par son facteur.
    ⑨ CE QUI CLOCHE — 1e-12 n'est pas un réglage : c'est l'égalité d'un produit de flottants qui vaut 1 par
      construction (aucune opération postérieure).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main. [sort: non]
    """
    if s1:
        p = 1.0
    if p is None:
        return "facteur inconnu"
    return "déjà au brut" if abs(p - 1.0) < 1e-12 else "à ramener au brut"


def mesurer(racine, sabotage):
    """Fait toutes les mesures et les calibrages ; rend le code de sortie.

    ① RÔLE — Le corps du programme (⑥ de l'en-tête).
    ② CONTEXTE D'APPEL — `principal`.
    ③ ENTRÉE — `racine` : la racine du dépôt · `sabotage` : None ou un nom de `SABOTAGES`.
    ④ CONDITIONS D'ENTRÉE — ④ de l'en-tête.
    ⑤ SORTIE — UNE valeur : 0 ou 1. [rend: 1]
    ⑥ TRAITEMENT — ⑥ de l'en-tête, dans l'ordre.
    ⑦ UNITÉ — ⑦ de l'en-tête.
    ⑧ POURQUOI — ⑧ de l'en-tête.
    ⑨ CE QUI CLOCHE — `os.chdir(racine)` : RECONSTRUIRE et CONTROLER lisent leurs fichiers par chemins relatifs.
    ⑩ EFFET — Change le dossier courant du processus ; affiche.
    ⑪ TERMINAISON — Rend la main ; lève `OSError`/`ValueError`/`ImportError` si une entrée manque. [sort: non]
    """
    racine = os.path.abspath(racine)
    os.chdir(racine)
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import RECONSTRUIRE_L_HISTORIQUE_LONG as R
    import CONTROLER_L_HISTORIQUE_LONG as K
    import MODULE_POSITIONS as M
    from CONTRATS_DES_FICHIERS import COURS_BNAINS

    # ── ① historique long : facteur de chaque ligne, par les fonctions de RECONSTRUIRE (R-708)
    fichier, _, _ = K.lire_cours(K.FICHIER)
    bnains, _, _ = K.lire_cours(K.BNAINS, COURS_BNAINS)
    K.oter_les_barres_fausses(K.FAUSSES, bnains)
    maitre, _, _ = K.lire_cours(R.MAITRE, K.CHAMPS)
    lignes_maitre = lire(R.MAITRE)
    sources_maitre = {(r["valeur"], r["date"]): r["source"] for r in lignes_maitre}
    a_defaire = K.lire_a_defaire(K.VERDICTS_YAHOO)
    evenements = json.load(open(K.EVENEMENTS, encoding="utf-8"))
    detachements, _ = K.lire_detachements(K.DROITS, K.OFFICIELS)
    brut, google = R.bruts(bnains, maitre, sources_maitre)
    ops, avis = R.operations(evenements, a_defaire, detachements, bnains, R.lire_divisions(R.DIVISIONS))
    ops = R.deduire(fichier, brut, ops)
    debut_maitre = min(r["date"] for r in lignes_maitre)
    sources_long = collections.Counter(r["source"] for r in lire(K.FICHIER))

    fin_bnains = "2012-01-01" if sabotage == "S6" else R.FIN_BNAINS   # S6 : borne de période fausse

    def periode(d):
        return ("1. ≤ " + R.FIN_BNAINS if d <= fin_bnains else
                "2. " + R.FIN_BNAINS + " < d < " + debut_maitre if d < debut_maitre else "3. ≥ " + debut_maitre)
    tableau = collections.Counter()
    exemple = {}
    for v, s in fichier.items():
        for d, x in s.items():
            p = R.facteur_apres(ops.get(v, []), d)
            c = classe_du_facteur(p, sabotage == "S1")
            tableau[(periode(d), c)] += 1
            exemple[(v, d)] = (x[3], p, c)
    n_long = sum(len(s) for s in fichier.values())
    dates_long = sorted({d for s in fichier.values() for d in s})
    print(f"I1 historique long donnees/sources_yahoo/historique_long_repare.csv : {n_long} lignes · {len(fichier)} valeurs · "
          f"{dates_long[0]} → {dates_long[-1]} · sources {dict(sources_long)}")
    print(f"   opérations sur titre connues de RECONSTRUIRE : {sum(len(o) for o in ops.values())} "
          f"(dont facteur inconnu : {sum(1 for o in ops.values() for x in o if x[1] is None)})")
    for (per, c), n in sorted(tableau.items()):
        print(f"   {per} · {c} : {n}")
    verif = collections.Counter()
    ecarts, ecarts_facteur_1 = set(), 0
    for (v, d), (c, p, cl) in exemple.items():
        b = brut.get(v, {}).get(d)
        if b is None or p is None:
            verif[(periode(d), "sans brut au dépôt" if b is None else "facteur inconnu")] += 1
        else:
            q = 1.0 if sabotage == "S5" else p          # S5 : la division par le facteur retirée
            if abs(c / q / b[0] - 1) <= R.TOLERANCE:
                verif[(periode(d), "cours ÷ facteur = brut à " + f"{R.TOLERANCE:.1%}" + " près")] += 1
            else:
                verif[(periode(d), "cours ÷ facteur ≠ brut (écart > " + f"{R.TOLERANCE:.1%}" + ")")] += 1
                ecarts.add((v, d))
                ecarts_facteur_1 += abs(p - 1.0) < 1e-12
    print(f"   confrontation au brut connu (bnains ≤ {R.FIN_BNAINS}, maître abc/euronext) :")
    for (per, c), n in sorted(verif.items()):
        print(f"     {per} · {c} : {n}")
    # la table écrite par RECONSTRUIRE (son main, lancé le 10-10-2026 et après) : une source déjà au dépôt, lue brute
    table_ecarts = lire(R.ECARTS)
    print(f"   dont écarts sur des lignes à facteur 1 (la division n'y est pour rien) : {ecarts_facteur_1} · "
          f"{R.ECARTS} : {len(table_ecarts)} lignes, statuts "
          f"{dict(collections.Counter(r['statut'] for r in table_ecarts))} · {R.PAR_OPERATION} : "
          f"{len(lire(R.PAR_OPERATION))} opérations écrites")
    # période ② recomptée par un autre chemin : lecture brute du fichier, bornes lues dans RECONSTRUIRE et le maître
    p2_brut = sum(1 for r in lire(K.FICHIER) if R.FIN_BNAINS < r["date"] < debut_maitre)
    p2_classe = sum(n for (per, c), n in tableau.items() if per.startswith("2."))
    p2_sans_brut = sum(n for (per, c), n in verif.items() if per.startswith("2.") and c == "sans brut au dépôt")

    # ── ② les autres parts
    bn = lire(K.BNAINS)
    print(f"I2 bnains donnees/sources_bnains/bnains_cac40.csv : {len(bn)} lignes · {len({r['valeur'] for r in bn})} valeurs · "
          f"{min(r['date'] for r in bn)} → {max(r['date'] for r in bn)} · après ôtage des barres fausses : "
          f"{sum(len(s) for s in bnains.values())} · cours BRUTS de Paris (LISEZ_MOI_LES_COURS § 0)")
    print(f"I3 maître {R.MAITRE} : {len(lignes_maitre)} lignes · {debut_maitre} → {max(r['date'] for r in lignes_maitre)} · "
          f"sources {dict(collections.Counter(r['source'] for r in lignes_maitre))} · google = corrigé des divisions par Google "
          f"(RECONSTRUIRE ①), abc et euronext = bruts")
    n3 = lire(os.path.join("etudes", "brouillons_chat", "NUIT_DES_20_ANS_Mer_21-10-2026", "N3_societes_sorties",
                           "BARRES_SOCIETES_SORTIES_PROPOSITION.csv.gz"))
    n3g = [r for r in n3 if r["statut"] == "GARDEE"]
    print(f"I4 sociétés sorties N3 (bnains, archives de Paris) : {len(n3)} barres · GARDEE {len(n3g)} · "
          f"ISIN {len({r['isin_passage'] for r in n3g})} · {min(r['date'] for r in n3g)} → {max(r['date'] for r in n3g)} · "
          f"statuts {dict(collections.Counter(r['statut'].split(' (')[0] for r in n3))}")
    av = lire(os.path.join("etudes", "VINGT_ANS_PAR_YAHOO_Dim_08-11-2026", "sorties", "A_VERSER.csv"))
    print(f"I5 Yahoo reconstruit A_VERSER.csv : {len(av)} lignes · {dict(collections.Counter(r['valeur'] for r in av))} · "
          f"{min(r['date'] for r in av)} → {max(r['date'] for r in av)} · cours ramenés au brut par paliers (8e colonne)")

    # ── ③ clés
    ref = lire(glob.glob(os.path.join("donnees", "REFERENTIEL_VALEURS_v3*.csv"))[0])
    noms_ref = {r["nom_usuel"].strip().upper() for r in ref}
    if sabotage == "S4":
        noms_ref |= {r["valeur"].strip().upper() for r in av}
    av_hors = sorted({r["valeur"] for r in av if r["valeur"].strip().upper() not in noms_ref})
    print(f"   I5 clé : noms absents du référentiel (ni mnémonique ni numéro) : {av_hors}")
    ident = lire(os.path.join("donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv"))
    isin_ident = {r["isin"] for r in ident}
    numeros = sorted({int(r["numero"]) for r in ident})
    passages = lire(os.path.join("donnees", "sources_indice", "PASSAGES_DANS_LE_CAC40.csv"))
    def numerote(code):                     # S3 : tout code passe pour numéroté
        return sabotage == "S3" or code in isin_ident
    sans_numero = collections.OrderedDict()
    for p in passages:
        if not numerote(p["isin_bnains"]):
            sans_numero.setdefault(p["isin_bnains"], p["libelle_bnains"])
    # contre-cas qui doit échouer (12-11-2026, tour 3 : toutes les sociétés de PASSAGES sont numérotées, le constat
    # d'état seul ne peut plus rougir) : un code absent de la table des identités doit être vu sans numéro
    sonde_vue = not numerote("XX0000000000")
    print(f"I6 identités : IDENTITES_DES_SOCIETES.csv numérote {len(numeros)} sociétés ({numeros[0]} à {numeros[-1]}) ; "
          f"PASSAGES porte {len({p['isin_bnains'] for p in passages})} ISIN, dont {len(sans_numero)} sans numéro "
          f"(sociétés sorties, I-2 à I-4, numéros 41 et suivants à attribuer)")
    print("   " + " · ".join(f"{i} {l}" for i, l in sans_numero.items()))
    n3_sans = {r["isin_passage"] for r in n3g} - isin_ident
    print(f"   I4 clé : ISIN de N3 GARDEE sans numéro : {len(n3_sans)} sur {len({r['isin_passage'] for r in n3g})}")

    # ── ④ frais : le juge s'arrête-t-il, année par année ? (MODULE_POSITIONS.cout_d_un_ordre, R-708)
    indice = [r["date"] for r in lire(os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv"))]
    premieres = {}
    for d in indice + sorted({r["date"] for r in lignes_maitre}):
        premieres.setdefault(d[:4], d)
    bloque = {}
    for an, d in sorted(premieres.items()):
        try:
            if sabotage != "S2":
                M.cout_d_un_ordre("AC", d, "achat", 100000.0)
            bloque[an] = ""
        except M.FraisNonChiffrables as e:
            bloque[an] = str(e)
    an_sans = str(max(int(r["annee"]) for r in lire_sans_commentaire(os.path.join("donnees", "VALEURS_TTF.csv"))) + 1)
    d_sans = next(f"{an_sans}-01-{j:02d}" for j in range(2, 9)
                  if datetime.date(int(an_sans), 1, j).weekday() < 5)
    try:
        if sabotage != "S2":
            M.cout_d_un_ordre("AC", d_sans, "achat", 100000.0)
        contre_arrete = False
    except M.FraisNonChiffrables:
        contre_arrete = True
    print(f"I7 frais (achat de 100 000 € d'ACCOR à la première séance de l'année) : années qui ARRÊTENT le juge : "
          f"{[a for a, e in bloque.items() if e]} · années chiffrées : {[a for a, e in bloque.items() if not e]}")
    ttf = [l for l in lire_bareme(M) if l["nature"] == "ttf" and l["instrument"] == "action"]
    for l in ttf:
        print(f"   barème {l['nom_bareme']} taxe {l['taux_fraction']} du « {l['debut']} » au « {l['fin']} »")
    # ce que le mécanisme DOIT rendre, déduit des deux fichiers lus bruts : une année arrête le juge si une ligne de
    # taxe du barème REEL s'applique à sa première séance ET si la liste annuelle de cette année manque
    bareme_brut = lire_sans_commentaire(os.path.join("donnees", "BAREME_FRAIS.csv"))
    annees_listees = {r["annee"] for r in lire_sans_commentaire(os.path.join("donnees", "VALEURS_TTF.csv"))}
    attendu_bloque = {an for an, d in premieres.items()
                      if an not in annees_listees and any(
                          l["nom_bareme"] == "REEL" and l["nature"] == "ttf" and l["instrument"] == "action"
                          and (not l["debut"] or l["debut"] <= d) and (not l["fin"] or d <= l["fin"])
                          for l in bareme_brut)}

    # ── ⑤ calibrages
    ok = True

    def calibrer(nom, condition, detail):
        nonlocal ok
        ok &= bool(condition)
        print(f"{nom} {'PASSE' if condition else 'ÉCHOUE'} — {detail}")
    c, p, cl = exemple.get(("ACCOR", "2000-01-03"), (None, None, None))
    b = brut.get("ACCOR", {}).get("2000-01-03", (None,))[0]
    calibrer("K1", cl == "à ramener au brut" and b is not None,
             f"vraie ligne ACCOR 2000-01-03 : cours {c}, facteur {p}, brut bnains {b} → à ramener, brut connu (R-732)")
    derniere = max(fichier.get("ACCOR", {"": 0}))
    calibrer("K2", exemple.get(("ACCOR", derniere), (0, 0, ""))[2] == "déjà au brut",
             f"contre-cas : ACCOR {derniere}, aucune opération après → déjà au brut")
    vu_bloque = {a for a, e in bloque.items() if e}
    calibrer("K3", vu_bloque == attendu_bloque and contre_arrete,
             f"constat d'état : années arrêtées {sorted(vu_bloque)[:1]}…{len(vu_bloque)} = années où une taxe "
             f"s'applique sans liste ({len(attendu_bloque)}), lues brutes dans le barème et VALEURS_TTF ; contre-cas "
             f"{d_sans} (l'année après la dernière liste) arrêté : {contre_arrete}")
    isin_ident_brut = {r["isin"] for r in lire(os.path.join("donnees", "sources_indice", "IDENTITES_DES_SOCIETES.csv"))}
    attendu_sans = {p["isin_bnains"] for p in passages} - isin_ident_brut
    calibrer("K4", set(sans_numero) == attendu_sans and sonde_vue,
             f"constat d'état : {len(sans_numero)} ISIN sans numéro = ISIN de PASSAGES absents du fichier "
             f"IDENTITES relu brut ({len(attendu_sans)}) ; Vivendi FR0000127771 "
             f"{'sans numéro' if 'FR0000127771' in sans_numero else 'numéroté'} ; contre-cas XX0000000000 vu sans numéro : "
             f"{sonde_vue}")
    alstom = [r for r in av if r["valeur"] == "ALSTOM" and r["date"] == "2006-08-01"]
    ref_brut = {r["nom_usuel"].strip().upper() for r in lire(glob.glob(os.path.join(
        "donnees", "REFERENTIEL_VALEURS_v3*.csv"))[0])}
    attendu_hors = sorted({r["valeur"] for r in av if r["valeur"].strip().upper() not in ref_brut})
    # 16-11-2026 (A-842, décision de Jean-Luc à 09h01) : la ligne se vérifie par son EMPREINTE, jamais par son prix
    # en clair — sha256 de « valeur;date;close », champs tels que lus dans A_VERSER.csv, calculée sur la vraie ligne.
    empreinte_k5 = (hashlib.sha256(f"{alstom[0]['valeur']};{alstom[0]['date']};{alstom[0]['close']}".encode("utf-8"))
                    .hexdigest() if alstom else None)
    calibrer("K5", empreinte_k5 == EMPREINTE_ALSTOM_2006_08_01 and av_hors == attendu_hors,
             "empreinte de la vraie ligne ALSTOM 2006-08-01 (R-732) dans A_VERSER ; constat d'état : noms hors "
             f"référentiel {len(av_hors)} = référentiel relu brut ({len(attendu_hors)})")
    reference = {(r["valeur"], r["date"]) for r in table_ecarts}
    journal = {(r["valeur"], r["date"]) for r in lire(os.path.join("donnees", "sources_yahoo", "journal_des_reparations.csv"))}
    journal |= {(r["valeur"], r["date"]) for r in lire(os.path.join("donnees", "sources_bnains", "BARRES_DE_PARIS_RECTIFIEES.csv"))}
    # 12-11-2026 (tour 3) : le lot d'octobre a réparé l'historique long (journal des réparations) et rectifié des
    # barres de Paris (BARRES_DE_PARIS_RECTIFIEES.csv, inversion des 19-20-06-2001) sans refaire
    # RECONSTRUCTION_ECARTS.csv ; une différence n'est admise que si l'un de ces deux fichiers porte ce (valeur, date)
    inexpliques = (ecarts ^ reference) - journal
    calibrer("K6", not inexpliques,
             f"les {len(ecarts)} écarts > {R.TOLERANCE:.1%} forment, au journal des réparations près ({len(inexpliques)} "
             f"différence(s) sans ligne au journal ni aux barres rectifiées), le MÊME ENSEMBLE (valeur, date) que les "
             f"{len(table_ecarts)} lignes de {R.ECARTS}"
             + (f" ; en plus : {len(ecarts - {(r['valeur'], r['date']) for r in table_ecarts})} dont {sorted(ecarts - {(r['valeur'], r['date']) for r in table_ecarts})[:5]}, en moins : "
                f"{len({(r['valeur'], r['date']) for r in table_ecarts} - ecarts)} dont {sorted({(r['valeur'], r['date']) for r in table_ecarts} - ecarts)[:5]}"
                if ecarts != {(r["valeur"], r["date"]) for r in table_ecarts} else ""))
    calibrer("K7", p2_classe == p2_brut and p2_sans_brut == p2_brut,
             f"période ② : {p2_classe} lignes classées = {p2_brut} lignes relues brutes entre {R.FIN_BNAINS} et "
             f"{debut_maitre} exclus, dont {p2_sans_brut} sans brut")
    print(f"RÉSULTAT DES CALIBRAGES : {'PASSE' if ok else 'ÉCHOUE'}" + (f" (sabotage {sabotage})" if sabotage else ""))
    return 0 if ok else 1


def lire_bareme(M):
    """Lit le barème des frais par le lecteur de MODULE_POSITIONS.

    ① RÔLE — Rendre les lignes de donnees/BAREME_FRAIS.csv telles que le juge les lit.
    ② CONTEXTE D'APPEL — `mesurer`, pour afficher les lignes de taxe.
    ③ ENTRÉE — `M` : le module MODULE_POSITIONS importé.
    ④ CONDITIONS D'ENTRÉE — Le barème suit son contrat (sinon le lecteur lève).
    ⑤ SORTIE — UNE valeur : la liste des lignes. [rend: 1]
    ⑥ TRAITEMENT — Appeler `M._lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS")`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : un second lecteur du barème divergerait du premier (ligne de commentaire, contrat).
    ⑨ CE QUI CLOCHE — Appelle une fonction privée (préfixe « _ ») d'un autre module.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève. [sort: non]
    """
    return M._lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS")


def principal(argv):
    """Lit la ligne de commande ; rend le code de sortie.

    ① RÔLE — Porter la ligne de commande.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `argv` : la racine, et facultativement « --saboter Sn ».
    ④ CONDITIONS D'ENTRÉE — La racine est un dossier.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ de l'en-tête). [rend: 1]
    ⑥ TRAITEMENT — Vérifier les arguments, appeler `mesurer`, changer toute erreur d'entrée en code 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un instrument qui n'a pas pu tourner ne rend jamais 0 (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sabotage = None
    if "--saboter" in argv:
        i = argv.index("--saboter")
        sabotage = argv[i + 1] if i + 1 < len(argv) else ""
        argv = argv[:i] + argv[i + 2:]
        if sabotage not in SABOTAGES:
            print(f"IMPOSSIBLE — sabotage inconnu {sabotage!r} (connus : {', '.join(SABOTAGES)})")
            return 2
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        print("USAGE : INVENTORIER_LES_VINGT_ANS.py <racine> [--saboter S1|…|S6]")
        return 2
    try:
        return mesurer(argv[0], sabotage)
    except (OSError, ValueError, ImportError, KeyError, IndexError) as e:
        print(f"IMPOSSIBLE — l'inventaire n'a pas pu tourner : {type(e).__name__} : {e}")
        return 2


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
