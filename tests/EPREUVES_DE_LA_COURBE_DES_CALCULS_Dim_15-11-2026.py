"""EPREUVES_DE_LA_COURBE_DES_CALCULS_Dim_15-11-2026.py — Dim 15-11-2026 (Paris) — épreuves du point ③ de l'étape LU.
Simulation uniquement.

① RÔLE — Prouver que le juge des stratégies calcule sur la courbe corrigée des opérations sur titre (R-108 ②) quand,
  et seulement quand, le fichier de cours est déclaré au cours brut (CONTRATS.FICHIERS_DE_COURS_AU_COURS_BRUT), et que
  chaque propriété a des dents : chaque sabotage de `SAB` doit faire échouer au moins un cas.
② CONTEXTE D'APPEL — À la main : python3 -I tests/EPREUVES_DE_LA_COURBE_DES_CALCULS_Dim_15-11-2026.py <racine>
  [--saboter | --saboter=S1,S2] ; et chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py), sans
  puis avec « --saboter ». « --un <racine de copie> » est le mode interne qui joue les cas sur une copie, pas fait
  pour la main.
③ ENTRÉE — La racine du dépôt ; facultatif, « --saboter » (tous les sabotages de `SAB`) ou « --saboter=<noms courts
  séparés par des virgules> » (C0, S1…). Z0, le programme tel quel, est toujours joué ; sans « --saboter », lui seul.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/ (le juge, le lecteur unique, COURBE_DES_CALCULS, l'assemblage,
  RECONSTRUIRE et leurs voisins), donnees/ (dont DETACHEMENTS_OFFICIELS.csv) et le témoin des 20 ans déclaré au cours
  brut. Un fichier absent fait échouer les cas, et le
  programme rend 1 ou 2, jamais 0.
⑤ SORTIE — AUCUNE valeur rendue ; affiche chaque cas et chaque sabotage. Code de sortie : 0 quand Z0 passe tous les
  cas et que chaque sabotage en fait échouer au moins un ; 1 sinon ; 2 quand une copie n'a pas pu se faire ou qu'une
  cible de sabotage est introuvable (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① une racine jetable — programmes/ COPIÉ (le sabotage y est écrit, et
  les petits fichiers d'essai déclarés au cours brut y sont déclarés), tout le reste de la racine relié par lien
  symbolique, sauf .git et prompts_taches/ ; un dossier essai_courbe/ avec cinq petits fichiers de cours faits de
  VRAIES lignes (`ESSAIS` : MICHELIN du 08 au 22-06-2022, la division par quatre du 16-06-2022, au brut du témoin et
  corrigé de l'historique long, chacun déclaré ou non ; SAINT-GOBAIN 2002 et 2009, deux opérations) · ② relancer ce
  programme en mode « --un » sur cette racine, borné à 900 secondes ; il joue les cas C1 à C13 et
  rend 0 si tous passent · ③ effacer la racine jetable · ④ juger : Z0 doit rendre 0, chaque sabotage autre chose
  que 0 (C0, le sabotage nul, doit rester SANS EFFET : il vérifie que le harnais sait voir un sabotage qui ne mord
  pas).
⑦ UNITÉ — Des codes de sortie ; dans les cas, des euros par titre, des titres et des rapports.
⑧ POURQUOI — R-731 : un jeu d'épreuves se sabote contre sa propre correction ; une épreuve qui reste verte quand on
  retire ce qu'elle teste n'est pas une preuve. R-732 : les cas viennent de vraies lignes (MICHELIN 2022-06-15 :
  clôture 111,45 €, division par quatre le lendemain, l'exemple même de R-108 ②). Superviseur R-759 du 14-11-2026
  (SUPERVISEUR_LU_TOUR7) : pas d'épreuve sur l'épreuve elle-même ; un cas par propriété du programme.
⑨ CE QUI CLOCHE — Les valeurs attendues de C1 et C7 supposent qu'aucune opération de MICHELIN n'est connue après le
  16-06-2022, ni de SAINT-GOBAIN après le 23-02-2009 ; une opération nouvelle ferait échouer le cas (et le dirait). ·
  La division 4 pour 1 de SAINT-GOBAIN (1/4) est écrite ici d'après sa source (evenements.json, « 4 pour 1 ») ; le
  droit de 2009 est CALCULÉ depuis DETACHEMENTS_OFFICIELS.csv. · Un fichier INDÉCIDABLE autre que le maître (aucune
  grande opération dans ses dates) n'a pas de cas : il passe, comme le maître. · Le refus
  d'une opération au facteur inconnu (C3) est joué sur une opération fabriquée : aucune n'existe dans les vraies
  données (mesuré le 15-11-2026). · Les sociétés sorties (facteur 1, nommées aux opérations inconnues, ⑨ de
  COURBE_DES_CALCULS) n'ont pas de cas sur main, où le lecteur ne les connaît pas : MT (C11) tient leur place.
⑩ EFFET — Écrit des racines jetables dans le dossier temporaire du système, chacune effacée après son tour ; n'écrit
  rien sous la racine. Affiche.
⑪ TERMINAISON — Un lancement « --un » pour Z0 et un par sabotage, chacun borné à 900 secondes ; sort par sys.exit avec
  le code dit en ⑤. Un de mes appels peut ne pas revenir avant sa borne : il est alors compté comme un échec.
  [sort: oui]
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

TEMOIN = "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv"
DETACHEMENTS = "donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv"
# LES PETITS FICHIERS D'ESSAI, faits de VRAIES lignes (R-732), recopiées ici pour que les cas ne bougent pas avec les
# fichiers. Brut : le témoin des 20 ans. Corrigé : l'historique long réparé (convention de Yahoo), mêmes dates.
ENTETE = "valeur,date,open,high,low,close,volume,source\n"
MICHELIN_BRUT = ENTETE + """MICHELIN,2022-06-08,122.0,122.1,119.0,120.95,432479,yahoo ramené au brut ÷ 0.250000
MICHELIN,2022-06-09,120.05,121.5,119.3,121.1,357690,yahoo ramené au brut ÷ 0.250000
MICHELIN,2022-06-10,120.4,120.95,117.1,117.5,404658,yahoo ramené au brut ÷ 0.250000
MICHELIN,2022-06-13,115.5,116.45,110.9,111.95,617182,yahoo ramené au brut ÷ 0.250000
MICHELIN,2022-06-14,110.4,111.95,108.4,108.6,566448,yahoo ramené au brut ÷ 0.250000
MICHELIN,2022-06-15,110.25,112.1,109.9,111.45,519803,yahoo ramené au brut ÷ 0.250000
MICHELIN,2022-06-16,28.06,28.18,27.06,27.22,1187164,yahoo ramené au brut ÷ 1.000000
MICHELIN,2022-06-17,27.44,27.975,27.405,27.815,3676440,yahoo ramené au brut ÷ 1.000000
MICHELIN,2022-06-20,27.84,27.99,27.265,27.77,1289251,yahoo ramené au brut ÷ 1.000000
MICHELIN,2022-06-21,27.7,28.2,27.65,27.81,1306124,yahoo ramené au brut ÷ 1.000000
MICHELIN,2022-06-22,27.335,27.34,26.755,27.0,1760261,yahoo ramené au brut ÷ 1.000000
"""
MICHELIN_CORRIGE = ENTETE + """MICHELIN,2022-06-08,30.5,30.525,29.75,30.2375,1729916,yahoo
MICHELIN,2022-06-09,30.0125,30.375,29.825,30.275,1430760,yahoo
MICHELIN,2022-06-10,30.1,30.2375,29.275,29.375,1618632,yahoo
MICHELIN,2022-06-13,28.875,29.1125,27.725,27.9875,2468728,yahoo
MICHELIN,2022-06-14,27.6,27.9875,27.1,27.15,2265792,yahoo
MICHELIN,2022-06-15,27.5625,28.025,27.475,27.8625,2079212,yahoo
MICHELIN,2022-06-16,28.06,28.18,27.06,27.22,1187164,yahoo
MICHELIN,2022-06-17,27.44,27.975,27.405,27.815,3676440,yahoo
MICHELIN,2022-06-20,27.84,27.99,27.265,27.77,1289251,yahoo
MICHELIN,2022-06-21,27.7,28.2,27.65,27.81,1306124,yahoo
MICHELIN,2022-06-22,27.335,27.34,26.755,27,1760261,yahoo
"""
SAINT_GOBAIN_BRUT = ENTETE + """SAINT-GOBAIN,2002-06-25,177.9,179.5,174.0,176.2,549646,bnains
SAINT-GOBAIN,2002-06-26,170.5,177.7,169.1,177.5,1103438,bnains
SAINT-GOBAIN,2002-06-27,44.31,44.8,43.75,44.1,1374587,bnains
SAINT-GOBAIN,2002-06-28,45.3,45.45,44.52,45.45,2588072,bnains
SAINT-GOBAIN,2009-02-20,24.26,25.3,22.83,23.8,14602274,bnains
SAINT-GOBAIN,2009-02-23,22.1,22.89,21.13,21.29,7093554,bnains
"""
# chemin → (contenu, déclaré au cours brut dans la copie du contrat)
ESSAIS = {
    "essai_courbe/MICHELIN_BRUT.csv": (MICHELIN_BRUT, True),
    "essai_courbe/MICHELIN_BRUT_NON_DECLARE.csv": (MICHELIN_BRUT, False),
    "essai_courbe/MICHELIN_CORRIGE.csv": (MICHELIN_CORRIGE, False),
    "essai_courbe/MICHELIN_CORRIGE_DECLARE.csv": (MICHELIN_CORRIGE, True),
    "essai_courbe/SAINT_GOBAIN_BRUT.csv": (SAINT_GOBAIN_BRUT, True),
}
DECLARATION = 'FICHIERS_DE_COURS_AU_COURS_BRUT = (\n'
CROCHET = ('    c = charger_module(os.path.join(base, "programmes", "COURBE_DES_CALCULS.py"),\n'
           '                       "courbe_des_calculs").courbe_si_le_fichier_est_brut(base, lecteur, c)\n')
LIGNE_PRIX = '            for k in ("open", "high", "low", "close"):\n'
LIGNE_LISTE = '        liste = ops.get(m, [])\n        c = out[m] = {}\n'
# (fichier sous programmes/, texte exact, remplacement) — chaque sabotage retire ou fausse UNE propriété
SAB = {
    "C0 sabotage nul": ("COURBE_DES_CALCULS.py", "import importlib.util\n", "import importlib.util\n"),
    "S1 le juge ne demande pas la courbe": ("JUGE_DES_STRATEGIES.py", CROCHET, ""),
    "S2 tout fichier pris pour brut": ("COURBE_DES_CALCULS.py",
                                       "    return chemin_declare(racine, fichier) in contrats.FICHIERS_DE_COURS_AU_COURS_BRUT",
                                       "    return chemin_declare(racine, fichier) is not None"),
    "S3 le jour même de l'opération compté": ("COURBE_DES_CALCULS.py",
                                              'p = facteur_apres(liste, d.isoformat() if hasattr(d, "isoformat") else str(d))',
                                              'p = facteur_apres(liste, (d - __import__("datetime").timedelta(days=1)).isoformat())'),
    "S4 facteur inconnu pris pour 1": ("COURBE_DES_CALCULS.py",
                                       "                inconnus.append((m, d))\n                continue\n",
                                       "                p = 1.0\n"),
    "S5 deux noms sous un même mnémonique admis": ("COURBE_DES_CALCULS.py", "        if m in de:\n", "        if False:\n"),
    "S6 volume multiplié au lieu de divisé": ("COURBE_DES_CALCULS.py", 'repr(float(ligne["volume"]) / p)',
                                              'repr(float(ligne["volume"]) * p)'),
    "S7 témoin mal écrit dans la déclaration": ("CONTRATS_DES_FICHIERS.py",
                                                '    "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv",\n)',
                                                '    "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h58.csv",\n)'),
    "S8 barres corrigées retirées": ("COURBE_DES_CALCULS.py", "            c[d] = x\n",
                                     "            if p == 1.0:\n                c[d] = x\n"),
    "S9 la règle 2 de la garde retirée (non déclaré, vue)": ("COURBE_DES_CALCULS.py",
                                                             "    if not declare_brut and vues:\n", "    if False:\n"),
    "S10 la règle 1 de la garde retirée (déclaré, non vue)": ("COURBE_DES_CALCULS.py",
                                                              "    if declare_brut and non_vues:\n", "    if False:\n"),
    "S11 tout fichier non déclaré refusé": ("COURBE_DES_CALCULS.py",
                                            "    if not declare_brut and vues:\n", "    if not declare_brut:\n"),
    "S12 opérations inconnues prises pour aucune opération": ("COURBE_DES_CALCULS.py",
                                                              "        if m not in connus:\n", "        if False:\n"),
    # X1 à X4 : sabotages du relecteur LU2 tour 1 (15-11-2026) ; X1 à X3 restaient verts au tour 1
    "X1 seule la clôture corrigée": ("COURBE_DES_CALCULS.py", LIGNE_PRIX, '            for k in ("close",):\n'),
    "X2 droits et actions gratuites oubliés": ("COURBE_DES_CALCULS.py", LIGNE_LISTE,
                                               "        liste = [o for o in ops.get(m, []) if o[1] is None or o[1] < 0.6]\n"
                                               "        c = out[m] = {}\n"),
    "X3 seule la dernière opération gardée": ("COURBE_DES_CALCULS.py", LIGNE_LISTE,
                                              "        liste = ops.get(m, [])[-1:]\n        c = out[m] = {}\n"),
    "X4 la courbe appliquée deux fois par le juge": ("JUGE_DES_STRATEGIES.py", CROCHET, CROCHET + CROCHET),
    # tour 3 (superviseur R-759 de LU2, § 2) : la totalité des noms et la courbe mesurée corrigée
    "S13 la courbe n'est plus mesurée corrigée": ("COURBE_DES_CALCULS.py",
                                                  "    garder_la_nature(False, *operations_jugees(x, ops, table, norm),",
                                                  "    (lambda *a: None)(False, *operations_jugees(x, ops, table, norm),"),
    "S14 la totalité des noms retirée": ("COURBE_DES_CALCULS.py", "    if sans:\n", "    if False:\n"),
    # SX1b de Cowork (RELU de 4be799c3) : seules MICHELIN et AIR LIQUIDE gardent leurs opérations, dans le code
    "SX1b seules ML et AI gardent leurs opérations": ("COURBE_DES_CALCULS.py",
                                                     "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n",
                                                     "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n"
                                                     "    par_m = {m: o for m, o in par_m.items() if m in (\"ML\", \"AI\")}\n"),
}


def charger(chemin, nom):
    """Charge un programme par son chemin.

    ① RÔLE — Charger les programmes de la racine jetable, jamais ceux du dépôt.
    ② CONTEXTE D'APPEL — `cas`.
    ③ ENTRÉE — `chemin` : le fichier · `nom` : le nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les sabotages vivent dans la copie : un import par le nom prendrait peut-être le dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le module chargé.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def cas(racine):
    """Joue les cas C1 à C13 sur une racine jetable ; rend le nombre de cas échoués.

    ① RÔLE — Les propriétés du point ③, une par cas.
    ② CONTEXTE D'APPEL — Le mode « --un ».
    ③ ENTRÉE — `racine` : la racine jetable préparée par `preparer`.
    ④ CONDITIONS D'ENTRÉE — Celles du ④ du programme.
    ⑤ SORTIE — UNE valeur : le nombre de cas échoués (une exception dans un cas le fait échouer, avec son texte).
      [rend: 1]
    ⑥ TRAITEMENT — C1 : le juge (`lire_par_le_lecteur`) lit le petit fichier Michelin BRUT déclaré sur la courbe : le
      2022-06-15, les QUATRE prix × 0,25 et le volume ÷ 0,25 ; le 2022-06-16 (déjà ex-division) 27,22 · C2 : le petit
      fichier Michelin CORRIGÉ (historique long), non déclaré, est lu tel quel (27,8625) · C3 : une opération au facteur
      inconnu arrête la courbe · C4 : deux noms d'opérations sous un même mnémonique l'arrêtent · C5 : chaque fichier
      déclaré au cours brut existe · C6 : sur le témoin entier, la courbe garde chaque barre et chaque date, et la
      paire MICHELIN 15→16-06-2022 passe de ×0,244 à moins que le seuil · C7 : SAINT-GOBAIN, DEUX opérations cumulées
      (division 4 pour 1 du 2002-06-27, droit du 2009-02-23) : le facteur du droit est CALCULÉ depuis la ligne de
      DETACHEMENTS_OFFICIELS.csv (prix théorique après détachement ÷ cours de la veille), jamais recopié du code,
      comparé à 1e-12 près · C8 : le petit fichier Michelin BRUT non déclaré est REFUSÉ (garde, règle 2) · C9 : le
      petit fichier Michelin CORRIGÉ déclaré est REFUSÉ (garde, règle 1) · C10 : sur le maître, la porte rend la
      lecture elle-même (exempté) · C11 : sur le témoin, MT (ArcelorMittal, hors de l'univers de RECONSTRUIRE) est
      nommé aux opérations inconnues, ses barres gardées, intactes · C12 : L'OREAL privée de ses opérations entre la lecture
      et la courbe (le rangement est filtré dans le processus du cas) : la courbe, mesurée corrigée, refuse (« la courbe corrigée de … ») · C13 :
      CARREFOUR privé de son mnémonique dans la table que lit la courbe : la totalité refuse (« sans mnémonique »).
    ⑦ UNITÉ — Euros par titre, titres, rapports.
    ⑧ POURQUOI — Voir le ⑧ du programme. C7 et les cinq champs de C1 : relecteur LU2 tour 1 (D1, trois sabotages verts)
      et superviseur R-759 de LU2 (l'attendu du droit se calcule depuis la source). C2, C8, C9 : superviseur de LU2,
      D3 (C2 réécrit : sans lui, « tout fichier non déclaré refusé » resterait vert).
    ⑨ CE QUI CLOCHE — Voir le ⑨ du programme.
    ⑩ EFFET — Lit des fichiers ; affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import csv
    P = os.path.join(racine, "programmes")
    J = charger(os.path.join(P, "JUGE_DES_STRATEGIES.py"), "juge_essai_courbe")
    L = charger(os.path.join(P, "LIRE_LES_COURS.py"), "lecteur_essai_courbe")
    C = charger(os.path.join(P, "COURBE_DES_CALCULS.py"), "courbe_essai_courbe")
    K = charger(os.path.join(P, "CONTROLER_LES_COURS.py"), "controle_essai_courbe")
    fautes = 0

    def juge(nom, f):
        nonlocal fautes
        try:
            ok, dit = f()
        except Exception as e:   # noqa: BLE001  un cas qui lève échoue, et dit pourquoi
            ok, dit = False, f"{type(e).__name__} : {str(e)[:200]}"
        fautes += not ok
        print(f"{'TIENT ' if ok else 'ROUGE '} {nom} — {dit}")

    def proche(a, b, tol=1e-12):
        return abs(a - b) <= tol * max(1.0, abs(b))

    def refus(fichier, motif):
        try:
            J.lire_par_le_lecteur(racine, fichier, {"ML": "MICHELIN"})
        except ValueError as e:
            return motif in str(e), f"refus : {str(e)[:150]}"
        return False, "aucun refus"

    def c1():
        s, _ = J.lire_par_le_lecteur(racine, "essai_courbe/MICHELIN_BRUT.csv", {"ML": "MICHELIN"})
        b = {x["date"]: x for x in s["MICHELIN"]}
        v15, v16 = b["2022-06-15"], b["2022-06-16"]
        attendu = {"open": 110.25 * 0.25, "high": 112.1 * 0.25, "low": 109.9 * 0.25, "close": 111.45 * 0.25,
                   "volume": 519803 / 0.25}
        ok = all(proche(v15[k], v) for k, v in attendu.items()) and proche(v16["close"], 27.22) and len(b) == 11
        return ok, ("15-06 " + " ".join(f"{k} {v15[k]}" for k in attendu) + f" · 16-06 clôture {v16['close']} · "
                    f"{len(b)} séances")

    def c2():
        s, _ = J.lire_par_le_lecteur(racine, "essai_courbe/MICHELIN_CORRIGE.csv", {"ML": "MICHELIN"})
        v15 = {x["date"]: x for x in s["MICHELIN"]}["2022-06-15"]
        return v15["close"] == 27.8625 and v15["volume"] == 2079212, f"corrigé, non déclaré : 15-06 clôture {v15['close']}"

    def c3():
        R = C._assembler().R
        lu = L.lire(racine, "essai_courbe/MICHELIN_BRUT.csv")
        ops = {"ML": [("2022-06-16", 0.25, "division", "essai"), ("2022-06-20", None, "fabriquée", "essai")]}
        try:
            C.corriger(lu["barres"], ops, {"ML"}, R.facteur_apres)
        except ValueError as e:
            return "facteur inconnu" in str(e), f"refus : {str(e)[:120]}"
        return False, "aucun refus : une barre au facteur inconnu est passée"

    def c4():
        table, _ = L.table_des_ecritures(racine)
        n = L.COMMUN.norm_valeur
        connus, ops = C.lire_les_operations(racine)
        double = dict(table)
        double[n("AIR LIQUIDE")] = double[n("MICHELIN")]
        try:
            C.operations_par_mnemonique(double, n, connus, ops)
        except ValueError as e:
            return "même mnémonique" in str(e), f"refus : {str(e)[:120]}"
        return False, "aucun refus : AIR LIQUIDE et MICHELIN rangés sous ML"

    def c5():
        manque = [f for f in L.CONTRATS.FICHIERS_DE_COURS_AU_COURS_BRUT if not os.path.isfile(os.path.join(racine, f))]
        return not manque and TEMOIN in L.CONTRATS.FICHIERS_DE_COURS_AU_COURS_BRUT, f"absents : {manque}"

    temoin = {}

    def courbe_du_temoin():
        if not temoin:
            lu = L.lire(racine, TEMOIN)
            temoin.update(lu=lu, x=C.courbe_si_le_fichier_est_brut(racine, L, lu))
        return temoin["lu"], temoin["x"]

    def c6():
        lu, x = courbe_du_temoin()
        memes = all(set(x["barres"][m]) == set(lu["barres"][m]) for m in lu["barres"]) and set(x["barres"]) == set(lu["barres"])
        d15, d16 = [d for d in lu["barres"]["ML"] if d.isoformat() in ("2022-06-15", "2022-06-16")]
        brut = float(lu["barres"]["ML"][d16]["close"]) / float(lu["barres"]["ML"][d15]["close"])
        courbe = float(x["barres"]["ML"][d16]["close"]) / float(x["barres"]["ML"][d15]["close"])
        seuil = float(K.SEUIL_VARIATION)
        ok = memes and abs(brut - 1) > seuil and abs(courbe - 1) <= seuil
        return ok, f"mêmes barres : {memes} · ML 15→16-06-2022 brut ×{brut:.4f}, courbe ×{courbe:.4f}, seuil {seuil}"

    def c7():
        with open(os.path.join(racine, DETACHEMENTS), encoding="utf-8", newline="") as f:
            r = [x for x in csv.DictReader(f) if x["valeur"] == "SAINT-GOBAIN" and x["jour_du_detachement"] == "2009-02-23"]
        if len(r) != 1:
            return False, f"{len(r)} ligne(s) SAINT-GOBAIN 2009-02-23 dans {DETACHEMENTS}"
        veille, prix, n = (float(r[0][k]) for k in ("cours_veille", "prix_souscription", "anciennes_pour_une_nouvelle"))
        droit = (n * veille + prix) / (n + 1) / veille     # prix théorique après détachement ÷ cours de la veille
        division = 1 / 4                                     # 4 pour 1 du 2002-06-27 (evenements.json, déclarée par Yahoo)
        s, _ = J.lire_par_le_lecteur(racine, "essai_courbe/SAINT_GOBAIN_BRUT.csv", {"SGO": "SAINT-GOBAIN"})
        b = {x["date"]: x for x in s["SAINT-GOBAIN"]}
        ok = (all(proche(b["2002-06-26"][k], v * division * droit)
                  for k, v in (("open", 170.5), ("high", 177.7), ("low", 169.1), ("close", 177.5)))
              and proche(b["2002-06-27"]["close"], 44.1 * droit) and proche(b["2009-02-20"]["close"], 23.8 * droit)
              and proche(b["2009-02-23"]["close"], 21.29))
        return ok, (f"droit calculé {droit!r} · 26-06-2002 clôture {b['2002-06-26']['close']} (attendu "
                    f"{177.5 * division * droit!r}) · 20-02-2009 {b['2009-02-20']['close']}")

    def c8():
        return refus("essai_courbe/MICHELIN_BRUT_NON_DECLARE.csv", "n'est pas déclaré au cours brut")

    def c9():
        return refus("essai_courbe/MICHELIN_CORRIGE_DECLARE.csv", "est déclaré au cours brut, mais")

    def c10():
        lu = L.lire(racine)
        return C.courbe_si_le_fichier_est_brut(racine, L, lu) is lu, f"maître : {lu['fichier']}"

    def c12():
        # L'OREAL perd ses opérations ENTRE la lecture et la courbe (comme SX1b de Cowork, pour une seule valeur) : sa
        # courbe garderait la division par dix du 03-07-2000 ; la courbe, mesurée corrigée, doit le voir et refuser
        vrai = C.operations_par_mnemonique
        def sans_loreal(*a):
            par_m, connus_m = vrai(*a)
            return {m: o for m, o in par_m.items() if m != "OR"}, connus_m
        C.operations_par_mnemonique = sans_loreal
        try:
            C.courbe_si_le_fichier_est_brut(racine, L, L.lire(racine, TEMOIN))
        except ValueError as e:
            return "la courbe corrigée de" in str(e), f"refus : {str(e)[:170]}"
        finally:
            C.operations_par_mnemonique = vrai
        return False, "aucun refus : la courbe de L'OREAL n'est pas corrigée et passe"

    def c13():
        # CARREFOUR perd son mnémonique dans la table que lit la courbe (N-1 de Cowork) : ses opérations seraient perdues
        vrai = L.table_des_ecritures
        def sans_carrefour(racine_):
            table, hors = vrai(racine_)
            return {k: m for k, m in table.items() if m != "CA"}, hors
        lu = L.lire(racine, TEMOIN)
        L.table_des_ecritures = sans_carrefour
        try:
            C.courbe_si_le_fichier_est_brut(racine, L, lu)
        except ValueError as e:
            return "sans mnémonique" in str(e), f"refus : {str(e)[:170]}"
        finally:
            L.table_des_ecritures = vrai
        return False, "aucun refus : CARREFOUR sans mnémonique est passé"

    def c11():
        lu, x = courbe_du_temoin()
        inconnues = x.get("valeurs_aux_operations_inconnues")
        intactes = all(float(x["barres"]["MT"][d][k]) == float(lu["barres"]["MT"][d][k])
                       for d in lu["barres"]["MT"] for k in ("open", "high", "low", "close", "volume"))
        return (inconnues == ["MT"] and intactes and len(x["barres"]["MT"]) == len(lu["barres"]["MT"]),
                f"inconnues : {inconnues} · barres de MT intactes : {intactes}")

    for nom, f in (("C1 le juge lit la courbe d'un fichier déclaré au cours brut, cinq champs", c1),
                   ("C2 un fichier corrigé non déclaré est lu tel quel", c2),
                   ("C3 un facteur inconnu arrête la courbe", c3),
                   ("C4 deux noms sous un même mnémonique arrêtent la courbe", c4),
                   ("C5 chaque fichier déclaré au cours brut existe", c5),
                   ("C6 le témoin entier : mêmes barres, la division de Michelin effacée", c6),
                   ("C7 deux opérations cumulées, le droit calculé depuis sa source", c7),
                   ("C8 un fichier brut non déclaré est refusé", c8),
                   ("C9 un fichier corrigé déclaré au cours brut est refusé", c9),
                   ("C10 le maître est rendu tel quel", c10),
                   ("C11 une valeur hors de l'univers de RECONSTRUIRE est nommée, ses barres intactes", c11),
                   ("C12 une valeur privée de ses opérations : la courbe mesurée corrigée refuse", c12),
                   ("C13 un nom de RECONSTRUIRE sans mnémonique : la totalité refuse", c13)):
        juge(nom, f)
    return fautes


def preparer(depot, sabotage):
    """Fabrique une racine jetable : programmes/ copié et saboté, le reste relié ; rend son chemin.

    ① RÔLE — Jouer un sabotage sans toucher le dépôt.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `depot` : la racine du dépôt · `sabotage` : (fichier, texte, remplacement), ou None pour Z0.
    ④ CONDITIONS D'ENTRÉE — Le texte visé est présent UNE fois ; la déclaration FICHIERS_DE_COURS_AU_COURS_BRUT existe.
    ⑤ SORTIE — UNE valeur : le chemin de la racine jetable.
      [rend: 1]
    ⑥ TRAITEMENT — Copier programmes/ ; relier tout le reste du dépôt sauf .git et prompts_taches/ ; écrire les cinq
      petits fichiers d'`ESSAIS` ; déclarer au cours brut, dans la copie du contrat, ceux qui le sont ; appliquer le
      sabotage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les données font plusieurs centaines de mégaoctets : les relier au lieu de les copier tient sur un
      disque presque plein (une seule épreuve lourde à la fois).
    ⑨ CE QUI CLOCHE — Un programme qui écrirait sous donnees/ écrirait dans le dépôt, à travers le lien : aucun des
      programmes joués ici n'écrit (leurs fiches, ⑩).
    ⑩ EFFET — Écrit dans le dossier temporaire du système.
    ⑪ TERMINAISON — Rend la main ou lève (AssertionError pour une cible introuvable).
      [sort: non]
    """
    r = tempfile.mkdtemp(prefix="courbe_des_calculs_")
    try:
        shutil.copytree(os.path.join(depot, "programmes"), os.path.join(r, "programmes"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        for n in os.listdir(depot):
            if n not in ("programmes", ".git", "prompts_taches"):
                os.symlink(os.path.join(os.path.abspath(depot), n), os.path.join(r, n))
        os.mkdir(os.path.join(r, "essai_courbe"))
        for f, (contenu, _) in ESSAIS.items():
            with open(os.path.join(r, f), "w", encoding="utf-8") as h:
                h.write(contenu)
        p = os.path.join(r, "programmes", "CONTRATS_DES_FICHIERS.py")
        t = open(p, encoding="utf-8").read()
        assert t.count(DECLARATION) == 1, "déclaration FICHIERS_DE_COURS_AU_COURS_BRUT introuvable"
        declares = "".join(f"    {f!r},\n" for f, (_, oui) in ESSAIS.items() if oui)
        open(p, "w", encoding="utf-8").write(t.replace(DECLARATION, DECLARATION + declares))
        if sabotage:
            f, a, b = sabotage
            p = os.path.join(r, "programmes", f)
            t = open(p, encoding="utf-8").read()
            assert t.count(a) == 1, f"cible introuvable ou multiple dans {f} : {a[:60]!r}"
            open(p, "w", encoding="utf-8").write(t.replace(a, b))
    except BaseException:
        shutil.rmtree(r, ignore_errors=True)
        raise
    return r


def main(argv):
    """Joue Z0 et les sabotages ; rend le code de sortie.

    ① RÔLE — Le harnais : chaque sabotage doit mordre, Z0 doit passer.
    ② CONTEXTE D'APPEL — Le bloc final.
    ③ ENTRÉE — `argv` : voir ② du programme.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code dit au ⑤ du programme.
      [rend: 1]
    ⑥ TRAITEMENT — Mode « --un » : `cas`, 0 si aucun échec, 1 sinon. Sinon : un nom de sabotage inconnu arrête
      (code 2) ; pour Z0 et chaque sabotage retenu, `preparer`, relancer en « --un », effacer, juger.
    ⑦ UNITÉ — Des codes de sortie.
    ⑧ POURQUOI — Voir le ⑧ du programme.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir le ⑩ du programme.
    ⑪ TERMINAISON — Voir le ⑪ du programme.
      [sort: non]
    """
    if argv[:1] == ["--un"]:
        return 1 if cas(argv[1]) else 0
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : EPREUVES_DE_LA_COURBE_DES_CALCULS_Dim_15-11-2026.py <racine> [--saboter | --saboter=S1,S2]")
        return 2
    depot = os.path.abspath(argv[0])
    sab = next((a for a in argv[1:] if a.startswith("--saboter")), None)
    seul = sab.split("=", 1)[1].split(",") if sab and "=" in sab else None
    inconnus = [n for n in (seul or []) if n not in {k.split()[0] for k in SAB}]
    if inconnus:   # un nom mal écrit ne joue rien : il ne doit pas passer pour « aucun sabotage sans effet »
        print(f"ARRÊT — sabotage(s) inconnu(s) : {inconnus}")
        return 2
    jeu = [("Z0 programme tel quel", None)] + [(n, s) for n, s in SAB.items()
                                               if sab and (seul is None or n.split()[0] in seul)]
    fautes, sans_effet = 0, []
    for nom, s in jeu:
        try:
            r = preparer(depot, s)
        except (OSError, AssertionError) as e:
            print(f"== {nom} : NON JUGÉ — {type(e).__name__} : {e}")
            return 2
        try:
            p = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--un", r], capture_output=True,
                               text=True, timeout=900)
            code, sortie = p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            code, sortie = "borne de 900 s", ""
        finally:
            shutil.rmtree(r, ignore_errors=True)
        rouges = [l for l in sortie.splitlines() if l.startswith("ROUGE")]
        print(f"== {nom} : code {code} · {len(rouges)} cas rouge(s)")
        for l in (sortie.splitlines() if s is None else rouges):
            print("   " + l)
        if s is None:
            fautes += code != 0
        elif nom.startswith("C0"):
            if code == 0:
                print("   SANS EFFET, comme attendu pour le sabotage nul")
            else:
                fautes += 1
        elif code == 0:
            sans_effet.append(nom)
            fautes += 1
            print("   SABOTAGE SANS EFFET")
    print(f"sabotages sans effet : {sans_effet}")
    print("VERDICT : " + ("tout est conforme" if not fautes else f"NON CONFORME — {fautes} faute(s)"))
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
