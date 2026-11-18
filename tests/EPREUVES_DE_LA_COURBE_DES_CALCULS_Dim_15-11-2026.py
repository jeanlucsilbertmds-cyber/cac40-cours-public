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
  RECONSTRUIRE et leurs voisins), donnees/ (dont DETACHEMENTS_OFFICIELS.csv et l'historique long réparé, où les
  barres corrigées des essais sont lues) et le témoin des 20 ans déclaré au cours brut (où les barres brutes des
  essais sont lues). Un fichier absent fait échouer les cas, et le programme rend 1 ou 2, jamais 0 ; une source des
  essais absente ou changée (empreinte) arrête avant tout cas, code 2.
⑤ SORTIE — AUCUNE valeur rendue ; affiche chaque cas et chaque sabotage. Code de sortie : 0 quand Z0 passe tous les
  cas et que chaque sabotage en fait échouer au moins un ; 1 sinon ; 2 quand une copie n'a pas pu se faire ou qu'une
  cible de sabotage est introuvable (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① une racine jetable — programmes/ COPIÉ (le sabotage y est écrit, et
  les petits fichiers d'essai déclarés au cours brut y sont déclarés), tout le reste de la racine relié par lien
  symbolique, sauf .git et prompts_taches/ ; un dossier essai_courbe/ avec cinq petits fichiers de cours faits de
  VRAIES lignes, LUES à chaque lancement dans leur fichier d'origine et contrôlées par empreinte (`EXTRAITS`,
  `extraire` ; aucune barre n'est écrite dans ce programme, A-555) (`ESSAIS` : MICHELIN du 08 au 22-06-2022, la division par quatre du 16-06-2022, au brut du témoin et
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
  données (mesuré le 15-11-2026). · C11 n'éprouve que la COURBE : que les sociétés sorties soient exactement les
  sociétés sans ligne d'identité ouverte n'a pas de cas direct ici (il relève de l'épreuve de la lecture) — BACKLOG.
  · AUCUN programme ne lit encore « valeurs_aux_operations_inconnues » (⑨ de COURBE_DES_CALCULS) : les 18 sociétés
  sorties gardent leurs barres au facteur 1, donc leurs divisions restent des chutes (ALO ×0,51 en 2008, UG ×0,17 en
  2001, NOKIA ×0,23, VK ×0,19) ; C11 le constate sans le corriger — BACKLOG. · La cible de S7 est le suffixe de la
  déclaration (le témoin juste avant « FICHIERS_DE_COURS_FIGES ») : une déclaration nouvelle qui listerait le témoin
  avant une autre constante la ferait introuvable (code 2, R-734) — BACKLOG. · Le harnais compte « mord » sur tout
  code de sortie non nul : un sabotage ne déclare pas les cas qu'il doit faire rougir, et un cas qui lève — même une
  NameError dans un sabotage mal écrit — le fait compter « mord » (J2 doit faire rougir C11 seul ; SZ5, C6 et C11 :
  vérifié en lisant la sortie, pas par le harnais) — BACKLOG. · L'attendu de C11 n'est indépendant de la courbe
  que pour la lecture des noms : même `table_des_ecritures`, même règle « univers = noms de l'historique long »,
  et aucun sabotage de `table_des_ecritures` — BACKLOG. · « MT » (C11) et VIV, UG, AC, LR (SZ6, SZ5, SZ5b) sont
  écrits en dur : un renommage de mnémonique rend C11 rouge ou le sabotage SANS EFFET, deux issues visibles —
  BACKLOG.
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


def fichier_de_l_historique_long(racine):
    """Rend le chemin de l'historique long réparé tel que le déclare CONTROLER_L_HISTORIQUE_LONG, relatif à la racine.

    ① RÔLE — Donner aux essais le chemin de l'historique long sans le recopier : le fichier que lit la courbe.
    ② CONTEXTE D'APPEL — `extraire`, pour l'extrait MICHELIN_CORRIGE, dans le processus qui prépare les racines
      jetables (une fois par lancement, `extraire` met le texte en cache).
    ③ ENTRÉE — `racine` : la racine du dépôt (str).
    ④ CONDITIONS D'ENTRÉE — programmes/CONTROLER_L_HISTORIQUE_LONG.py existe sous `racine` et se charge (il insère son
      dossier en tête de `sys.path` et importe CONTRATS_DES_FICHIERS et CALENDRIER_DE_LA_BOURSE sous leurs noms).
    ⑤ SORTIE — UNE valeur : `FICHIER` du module chargé, tel quel. Exemple mesuré le 18-11-2026 :
      « donnees/sources_yahoo/historique_long_repare.csv ».
      [rend: 1]
    ⑥ TRAITEMENT — `charger` le programme sous le nom « historique_long_essai_courbe », distinct de celui sous lequel
      l'assemblage l'importe ; rendre son `FICHIER`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : deux implémentations d'une même chose divergent toujours. Jusqu'au 18-11-2026, l'épreuve
      recopiait ce chemin (constante HISTORIQUE_LONG) : renommé chez le contrôleur, l'ancien fichier resté en place,
      l'épreuve aurait lu l'ancien et la courbe le nouveau (relecteur neuf de travail-c1, R3 ; superviseur R-759).
    ⑨ CE QUI CLOCHE — Le contrôleur est chargé ici depuis la racine du DÉPÔT, et la courbe le lit dans la racine
      jetable (copie de programmes/) : les deux fichiers sont les mêmes octets tant qu'aucun sabotage ne touche le
      contrôleur (aucun ne le touche). C11, lui, prend le chemin dans le module même que lit la courbe.
    ⑩ EFFET — Exécute les déclarations du contrôleur (son `main` n'est pas appelé) ; ajoute un dossier à `sys.path`.
    ⑪ TERMINAISON — Rend la main ou lève l'erreur de chargement, que `main` transforme en code 2 (OSError) ou laisse
      remonter.
      [sort: non]
    """
    return charger(os.path.join(racine, "programmes", "CONTROLER_L_HISTORIQUE_LONG.py"),
                   "historique_long_essai_courbe").FICHIER


# LES PETITS FICHIERS D'ESSAI, faits de VRAIES lignes (R-732 : un jeu d'épreuves ouvre le vrai fichier). Aucune
# barre n'est écrite ici (A-555, A-543 : les données du dépôt privé ne se publient pas, et ce fichier est publié) :
# seules les CLÉS le sont — le fichier d'origine, la valeur, les dates — avec l'EMPREINTE SHA-256 des lignes
# retenues, prise le 15-11-2026 sur les lignes qui étaient écrites ici jusque-là (mêmes octets). Les lignes sont
# LUES à chaque lancement (`extraire`) ; un fichier absent, une ligne manquante ou une empreinte différente arrête
# l'épreuve (code 2, R-734). Brut : le témoin des 20 ans. Corrigé : l'historique long réparé (convention de
# Yahoo), mêmes dates — son chemin n'est PAS écrit ici : il est lu dans CONTROLER_L_HISTORIQUE_LONG.FICHIER, celui que
# lit la courbe (`fichier_de_l_historique_long` ; R-708 : deux implémentations d'une même chose divergent toujours).
ENTETE = "valeur,date,open,high,low,close,volume,source\n"
DATES_MICHELIN = ("2022-06-08", "2022-06-09", "2022-06-10", "2022-06-13", "2022-06-14", "2022-06-15", "2022-06-16",
                  "2022-06-17", "2022-06-20", "2022-06-21", "2022-06-22")
DATES_SAINT_GOBAIN = ("2002-06-25", "2002-06-26", "2002-06-27", "2002-06-28", "2009-02-20", "2009-02-23")
# nom → (fichier d'origine — un chemin, ou la fonction qui le rend depuis la racine —, valeur, dates, empreinte SHA-256
# des lignes retenues, chacune suivie d'un saut de ligne)
EXTRAITS = {
    "MICHELIN_BRUT": (TEMOIN, "MICHELIN", DATES_MICHELIN,
                      "07e822d09d94df2ed4047a4c92c83f06ccb5c9e33cb7a18fbdae6fba8573223d"),
    "MICHELIN_CORRIGE": (fichier_de_l_historique_long, "MICHELIN", DATES_MICHELIN,
                         "86ffba4101c32dd31b0bbb93affaa6936c19da30b5c5ed941544066e73835228"),
    "SAINT_GOBAIN_BRUT": (TEMOIN, "SAINT-GOBAIN", DATES_SAINT_GOBAIN,
                          "15259f0f293937fba1ae30d466b9958a462a893b5873a115f36276ceb0e4cca7"),
}
# chemin → (nom de l'extrait, déclaré au cours brut dans la copie du contrat)
ESSAIS = {
    "essai_courbe/MICHELIN_BRUT.csv": ("MICHELIN_BRUT", True),
    "essai_courbe/MICHELIN_BRUT_NON_DECLARE.csv": ("MICHELIN_BRUT", False),
    "essai_courbe/MICHELIN_CORRIGE.csv": ("MICHELIN_CORRIGE", False),
    "essai_courbe/MICHELIN_CORRIGE_DECLARE.csv": ("MICHELIN_CORRIGE", True),
    "essai_courbe/SAINT_GOBAIN_BRUT.csv": ("SAINT_GOBAIN_BRUT", True),
}
_LUS = {}


def extraire(depot, nom):
    """Rend le contenu d'un petit fichier d'essai, lu dans son fichier d'origine et contrôlé par son empreinte.

    ① RÔLE — Fournir les VRAIES lignes des essais sans qu'aucune soit écrite dans ce programme publié.
    ② CONTEXTE D'APPEL — `preparer`, une fois par petit fichier ; mis en cache par nom pour le lancement.
    ③ ENTRÉE — `depot` : la racine du dépôt · `nom` : une clé d'`EXTRAITS`, dont le fichier d'origine est un chemin
      relatif à `depot` ou une fonction de `depot` qui le rend (`fichier_de_l_historique_long`).
    ④ CONDITIONS D'ENTRÉE — Le fichier d'origine existe sous `depot` et porte, pour la valeur, chaque date une fois.
    ⑤ SORTIE — UNE valeur : le texte du fichier d'essai (`ENTETE` puis les lignes retenues, dans l'ordre du fichier).
      [rend: 1]
    ⑥ TRAITEMENT — Rendre le chemin du fichier d'origine (appeler la fonction s'il en est une) ; le lire ligne à
      ligne ; garder celles dont les deux premiers champs sont la valeur
      et une des dates ; exiger une ligne par date et l'empreinte SHA-256 d'`EXTRAITS`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-555 et A-543 : une barre du dépôt privé ne se publie pas ; R-732 : les cas viennent de vraies
      lignes ; l'empreinte garantit que les cas lisent les mêmes octets qu'avant (sinon leurs attendus bougeraient).
    ⑨ CE QUI CLOCHE — Une correction légitime du fichier d'origine arrête l'épreuve : l'empreinte se reprend alors, à
      la main, après décision.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève FileNotFoundError (fichier absent) ou AssertionError (lignes ou empreinte),
      que `main` transforme en code 2.
      [sort: non]
    """
    import hashlib
    if nom not in _LUS:
        fichier, valeur, dates, empreinte = EXTRAITS[nom]
        if callable(fichier):   # le chemin déclaré par son programme, jamais recopié ici (R-708)
            fichier = fichier(depot)
        retenues = []
        with open(os.path.join(depot, fichier), encoding="utf-8", newline="") as f:
            for ligne in f:
                champs = ligne.split(",", 2)
                if champs[0] == valeur and len(champs) > 2 and champs[1] in dates:
                    retenues.append(ligne.rstrip("\r\n") + "\n")
        vues = [x.split(",", 2)[1] for x in retenues]
        assert sorted(vues) == sorted(dates), f"{nom} : dates lues dans {fichier} {vues}, attendues {list(dates)}"
        corps = "".join(retenues)
        vu = hashlib.sha256(corps.encode("utf-8")).hexdigest()
        assert vu == empreinte, f"{nom} : empreinte des lignes de {fichier} {vu}, attendue {empreinte}"
        _LUS[nom] = ENTETE + corps
    return _LUS[nom]


def barres_d_essai(racine, fichier):
    """Rend les barres d'un petit fichier d'essai, telles qu'écrites, par date : {date: {champ: nombre}}.

    ① RÔLE — Donner aux cas les valeurs d'entrée des attendus sans les écrire dans le code.
    ② CONTEXTE D'APPEL — `cas` (C1, C2, C7).
    ③ ENTRÉE — `racine` : la racine jetable · `fichier` : un chemin d'`ESSAIS`.
    ④ CONDITIONS D'ENTRÉE — Le fichier a été écrit par `preparer` (donc contrôlé par son empreinte).
    ⑤ SORTIE — UNE valeur : le dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — csv.DictReader ; open, high, low, close, volume en float.
    ⑦ UNITÉ — Euros par titre et titres.
    ⑧ POURQUOI — Les attendus sont des formules sur l'entrée (× 0,25, ÷ 0,25, tel quel) ; l'empreinte fige l'entrée,
      donc les attendus sont les mêmes nombres qu'avant.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    import csv
    with open(os.path.join(racine, fichier), encoding="utf-8", newline="") as f:
        return {x["date"]: {k: float(x[k]) for k in ("open", "high", "low", "close", "volume")}
                for x in csv.DictReader(f)}


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
    # S7 : la cible porte le suffixe « ,\n)\n\nFICHIERS_DE_COURS_FIGES = {\n » — le chemin seul est écrit deux fois
    # dans le contrat (la déclaration et FICHIERS_DE_COURS_FIGES) ; avec ce suffixe, une seule fois, copie comprise
    "S7 témoin mal écrit dans la déclaration": ("CONTRATS_DES_FICHIERS.py",
                                                '    "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv"'
                                                ',\n)\n\nFICHIERS_DE_COURS_FIGES = {\n',
                                                '    "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h58.csv"'
                                                ',\n)\n\nFICHIERS_DE_COURS_FIGES = {\n'),
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
    # superviseur R-759 de C1 (17-11-2026, SZ6 et SZ5) : l'univers des opérations connues, élargi puis rétréci, dans
    # la courbe seulement — l'attendu de C11, calculé par l'épreuve depuis l'historique long, ne bouge pas
    "SZ6 univers élargi (VIV et UG prises pour connues)": ("COURBE_DES_CALCULS.py",
                                                         "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n",
                                                         "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n"
                                                         "    connus_m = connus_m | {\"VIV\", \"UG\"}\n"),
    "SZ5 univers rétréci d'une valeur à grande opération : la garde mesurée refuse": ("COURBE_DES_CALCULS.py",
                                          "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n",
                                          "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n"
                                          "    connus_m = connus_m - {\"AC\"}\n"),
    # SZ5 (ACCOR retirée) mord par la garde de la courbe mesurée corrigée (ACCOR a une grande opération : C6 et C11
    # rougissent par « la courbe corrigée de … »), pas par l'égalité de C11 ; SZ5b retire une valeur
    # SANS opération connue (LEGRAND, mesuré le 17-11-2026) : ses barres ne changent pas, seul C11 peut le voir
    "SZ5b univers rétréci (LEGRAND, sans opération, retirée)": ("COURBE_DES_CALCULS.py",
                                                               "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n",
                                                               "    par_m, connus_m = operations_par_mnemonique(table, norm, connus, ops)\n"
                                                               "    connus_m = connus_m - {\"LR\"}\n"),
    # J2 (relecteur neuf de travail-c1, R1 ; superviseur R-759) : la moitié « barres intactes » de C11 n'avait aucun
    # sabotage au catalogue. La clôture des SEULES valeurs aux opérations inconnues (`sans_operations_connues` de
    # `corriger`) prend 0,01 € : aucun autre cas ne lit ces valeurs, seul C11 doit rougir
    "J2 barres des valeurs aux opérations inconnues : clôture + 0,01": ("COURBE_DES_CALCULS.py",
                                                                       "    if inconnus:\n        inconnus.sort()\n",
                                                                       "    for m in sans_operations_connues:\n"
                                                                       "        for d in out[m]:\n"
                                                                       "            out[m][d] = dict(out[m][d], close=repr(float(out[m][d][\"close\"]) + 0.01))\n"
                                                                       "    if inconnus:\n        inconnus.sort()\n"),
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
      lecture elle-même (exempté) · C11 : sur le témoin, les valeurs hors de l'univers de RECONSTRUIRE — l'attendu,
      CALCULÉ ici : les mnémoniques du témoin moins ceux des noms de l'historique long réparé (son chemin pris dans le
      module même où la courbe le lit, `C._assembler().R.K.FICHIER`, jamais recopié), rangés par la table du
      lecteur ; mesuré le 17-11-2026 : MT (ArcelorMittal) et les 18 sociétés sorties — sont exactement celles nommées
      aux opérations inconnues ; l'attendu n'est pas vide et porte MT (vraie ligne connue, R-732) ; pour chacune, le
      nombre de barres et les cinq champs sont ceux du lecteur (facteur 1) · C12 : L'OREAL privée de ses opérations entre la lecture
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
        e = barres_d_essai(racine, "essai_courbe/MICHELIN_BRUT.csv")   # l'entrée, figée par son empreinte
        attendu = {k: e["2022-06-15"][k] * 0.25 for k in ("open", "high", "low", "close")}
        attendu["volume"] = e["2022-06-15"]["volume"] / 0.25
        ok = (all(proche(v15[k], v) for k, v in attendu.items()) and proche(v16["close"], e["2022-06-16"]["close"])
              and len(b) == 11)
        return ok, ("15-06 " + " ".join(f"{k} {v15[k]}" for k in attendu) + f" · 16-06 clôture {v16['close']} · "
                    f"{len(b)} séances")

    def c2():
        s, _ = J.lire_par_le_lecteur(racine, "essai_courbe/MICHELIN_CORRIGE.csv", {"ML": "MICHELIN"})
        v15 = {x["date"]: x for x in s["MICHELIN"]}["2022-06-15"]
        e = barres_d_essai(racine, "essai_courbe/MICHELIN_CORRIGE.csv")["2022-06-15"]   # figée par son empreinte
        return v15["close"] == e["close"] and v15["volume"] == e["volume"], f"corrigé, non déclaré : 15-06 clôture {v15['close']}"

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
        e = barres_d_essai(racine, "essai_courbe/SAINT_GOBAIN_BRUT.csv")   # l'entrée, figée par son empreinte
        ok = (all(proche(b["2002-06-26"][k], e["2002-06-26"][k] * division * droit)
                  for k in ("open", "high", "low", "close"))
              and proche(b["2002-06-27"]["close"], e["2002-06-27"]["close"] * droit)
              and proche(b["2009-02-20"]["close"], e["2009-02-20"]["close"] * droit)
              and proche(b["2009-02-23"]["close"], e["2009-02-23"]["close"]))
        return ok, (f"droit calculé {droit!r} · 26-06-2002 clôture {b['2002-06-26']['close']} (attendu "
                    f"{e['2002-06-26']['close'] * division * droit!r}) · 20-02-2009 {b['2009-02-20']['close']}")

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
        # L'attendu est CALCULÉ par l'épreuve elle-même, jamais par COURBE : l'univers de RECONSTRUIRE est l'ensemble
        # des noms de l'historique long réparé, rangés sous leur mnémonique par la table du lecteur ; toute valeur du
        # témoin hors de cet univers doit être nommée aux opérations inconnues, ses barres gardées au facteur 1
        lu, x = courbe_du_temoin()
        table, _ = L.table_des_ecritures(racine)
        historique = C._assembler().R.K.FICHIER   # le chemin que lit la courbe (R.lire_les_entrees), jamais recopié
        with open(os.path.join(racine, historique), encoding="utf-8", newline="") as f:
            univers = {table[L.COMMUN.norm_valeur(r["valeur"])] for r in csv.DictReader(f)}
        attendu = sorted(set(lu["barres"]) - univers)
        inconnues = x.get("valeurs_aux_operations_inconnues")
        abimees = [m for m in attendu
                   if len(x["barres"].get(m, {})) != len(lu["barres"][m])
                   or not all(float(x["barres"][m][d][k]) == float(lu["barres"][m][d][k])
                              for d in lu["barres"][m] for k in ("open", "high", "low", "close", "volume"))]
        intactes = not abimees
        return (bool(attendu) and "MT" in attendu and inconnues == attendu and intactes,
                f"inconnues : {inconnues} · attendu (témoin hors de l'univers de l'historique long) : {attendu} · "
                f"barres intactes : {intactes}" + (f", abîmées : {abimees}" if abimees else ""))

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
                   ("C11 les valeurs hors de l'univers de RECONSTRUIRE sont nommées, leurs barres intactes", c11),
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
      petits fichiers d'`ESSAIS`, lus par `extraire` ; déclarer au cours brut, dans la copie du contrat, ceux qui le sont ; appliquer le
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
        for f, (nom, _) in ESSAIS.items():
            contenu = extraire(depot, nom)   # lu dans le fichier d'origine, contrôlé par son empreinte
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
        except (OSError, AssertionError) as e:   # dont un fichier d'origine absent ou changé (`extraire`)
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
