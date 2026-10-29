"""EPREUVES_DU_JUGE_PAR_LE_LECTEUR_Mar_27-10-2026.py — Mar 27-10-2026 (Paris) — épreuves de l'étape 1 de A-577.

① RÔLE — Prouver que le juge des stratégies (`programmes/JUGE_DES_STRATEGIES.py`), depuis qu'il lit les cours par le
  lecteur unique (A-577, étape 1, commit 39e4909 du 26-10-2026), fait les trois choses promises, et que chacune a des
  dents : ① il n'achète une valeur que si elle est dans le CAC 40 LE JOUR DE L'ACHAT ; ② il calcule les signaux
  morceau par morceau, coupés aux trous, mais garde la position à travers un trou (décision de Jean-Luc du 27-10-2026 à
  13h30 : « 1 la garder ») et achète, après un signal donné la veille d'un trou, à la séance suivante qui a un cours ; ③ son programme principal lit le fichier donné par l'option « --cours= », compte juste les coupures, et
  s'arrête quand le lecteur a mis des lignes à part, quand une valeur n'a aucun passage dans l'indice, sur une option
  mal écrite et sur une fiche visée absente (ces arrêts depuis le 27-10-2026, relecture et superviseur R-759).
② CONTEXTE D'APPEL — À la main : python3 -I tests/EPREUVES_DU_JUGE_PAR_LE_LECTEUR_Mar_27-10-2026.py <racine>
  [<fichier de résultats>] ; et chaque soir par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui ne
  donne que la racine. Ce programme se relance lui-même avec « --un <copie du juge> <racine> » pour jouer les cas
  sur une copie sabotée : ce mode n'est pas fait pour la main.
③ ENTRÉE — Un ou deux arguments : la racine du dépôt ; le chemin du relevé à écrire, facultatif (sans lui, le relevé
  va dans un dossier temporaire).
④ CONDITIONS D'ENTRÉE — Sous la racine : le juge, le lecteur unique, le module de positions, le module de signal
  C5-ETENDU-10, le registre des stratégies avec la fiche C5E10-QA-V1, le référentiel des valeurs, le fichier maître
  `donnees/cours_maitre.csv` et l'historique des 20 ans `donnees/sources_yahoo/historique_long_repare.csv`.
⑤ SORTIE — AUCUNE valeur rendue : le relevé est écrit et affiché ; une cible de sabotage introuvable lève
  AssertionError. Code de sortie : 0 si le juge tel quel passe tous les cas ET que chaque sabotage en fait échouer au
  moins un ; 1 sinon (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).
⑥ TRAITEMENT — ① pour le juge tel quel, puis pour chaque sabotage de `SAB` : écrire une copie du juge, modifiée,
  qui importe les programmes du dépôt ; ② relancer ce programme en mode « --un » sur cette copie ; ③ noter son code
  de sortie ; ④ écrire le relevé.
⑦ UNITÉ — Des CODES DE SORTIE ; dans les cas, des dates AAAA-MM-JJ et des nombres d'opérations.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction : une épreuve qui reste verte quand on retire
  ce qu'elle teste n'est pas une preuve (R-731). Les cas réels (R-732) : Eiffage, entrée dans le CAC 40 le
  22-12-2025 (référentiel des valeurs) ; Accor, sortie le 18-09-2020 et retour le 18-03-2024 ; le trou de Bouygues
  du 03 au 10-11-2011 dans l'historique des 20 ans (celui d'Accor du 24-12-2010, pris d'abord, est comblé depuis le
  27-10-2026) ; la fiche C5E10-QA-V1 sur le maître, dont la mesure du 26-10-2026 a
  retiré 11 opérations, toutes achetées hors de l'indice. Le relevé est écrit par le programme, jamais à la main
  (R-728).
⑨ CE QUI CLOCHE — La lecture passée à `_rejouer` dans `juger` (stabilité paramétrique) n'a pas de cas : la retirer
  ne fait échouer aucun cas d'ici. · Le refus d'un fichier figé modifié ou allongé n'a pas de
  cas. · L'argument `jusqu_au` de `lire_par_le_lecteur` n'est pas éprouvé : aucun
  appelant ne le donne. · Le cas M2 dépend de l'historique des 20 ans : s'il disparaît, le cas échoue (et le dit).
⑩ EFFET — Écrit le relevé ; écrit des copies du juge et un fichier de cours dans des dossiers temporaires, effacés.
  N'écrit rien sous la racine.
⑪ TERMINAISON — Un lancement de ce programme en mode « --un » pour le juge tel quel et un par sabotage de `SAB`,
  chacun borné à 900 secondes ; chacun lance le juge sept fois (M1 à M7), chaque fois borné à 300 secondes. Sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import datetime, importlib.util, os, re, shutil, subprocess, sys, tempfile, zoneinfo

LIGNE_DU_CHEMIN = "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"
FICHE = "C5E10-QA-V1"
HISTORIQUE = "donnees/sources_yahoo/historique_long_repare.csv"
SAB = {
    "S1 entrée dans l'indice exclue": ("return any(a <= jour and (b is None", "return any(a < jour and (b is None"),
    "S2 sortie de l'indice exclue": ("(b is None or jour <= b) for a, b in passages)", "(b is None or jour < b) for a, b in passages)"),
    # S3, S4, S6 et S22 recalés le 28-10-2026 : l'achat et la sortie vivent dans `jouer_une_entree` et `achat_admis`,
    # que l'étalon de hasard appelle aussi (R-708) ; chaque sabotage vise la même règle qu'avant, à sa nouvelle place.
    "S3 l'indice lu au jour du signal": ('return dans_l_indice(lecture["passages"].get(v, []), serie[j]["date"])',
                                         'return dans_l_indice(lecture["passages"].get(v, []), serie[j - 1]["date"])'),
    "S4 la composition ignorée": ('    if lecture is None or not lecture.get("composition"):\n        return True',
                                  '    if True:\n        return True'),
    "S5 les séries jamais coupées": ('if k < len(trous) and trous[k] < b["date"]:', "if False:"),
    "S6 les sorties testées dans le seul morceau": ("                op = jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture)",
                                                    "                op = jouer_une_entree(v, s, i + 1, tp, sl, h, mod_positions, lecture) if i + 1 < len(s) else None"),
    "S7 le signal de fin de morceau perdu": ("                j = rang[d_sig] + 1           #",
                                             "                j = rang[d_sig] + 1 if i + 1 < len(s) else len(serie)           #"),
    "S8 les lignes mises à part ignorées": ("    if a_part:\n", "    if False:\n"),
    "S9 l'option --cours ignorée": ("f_cours = os.path.join(base, _autre) if _autre else fichiers_de_cours(base)[0]",
                                    "f_cours = fichiers_de_cours(base)[0]"),
    "S10 un volume mal converti": ('"low": float(r["low"]), "close": float(r["close"]), "volume": float(r["volume"])}',
                                   '"low": float(r["low"]), "close": float(r["close"]), "volume": float(r["volume"]) + 1}'),
    "S11 la composition éteinte par le lecteur": ('"composition": True}', '"composition": False}'),
    "S12 la lecture non passée par main": (
        "ops, inconnus = jouer(f, cours, mnemo, mod_sig, mod_pos, periode=_bornes, lecture=lecture)",
        "ops, inconnus = jouer(f, cours, mnemo, mod_sig, mod_pos, periode=_bornes)"),
    "S13 les passages d'une autre valeur": ('passages[v] = [(iso(a), iso(b) if b else None) for a, b in c["dans_l_indice"].get(m, [])]',
                                            'passages[v] = [(iso(a), iso(b) if b else None) for a, b in c["dans_l_indice"].get("VIE", [])]'),
    "S15 une valeur sans passage acceptée": ("    if sans:   #", "    if False:   #"),
    "S16 une option mal écrite ignorée": ("    if _mal:\n", "    if False:\n"),
    "S17 une fiche visée absente ignorée": ('    if cible and not any(f["id"] == cible for f in passees):', "    if False:"),
    "S18 les coupures comptées par morceau": ("    _coupures = sum(len(m) - 1 for m in _morceaux.values())",
                                             "    _coupures = sum(len(m) for m in _morceaux.values())"),
    "S19 toutes les séances sans cours comptées": ('if m[i - 1][-1]["date"] < d < m[i][0]["date"])', "if True)"),
    "S20 les séances d'une valeur non triées": ("                    for d, r in sorted(barres.items())]",
                                                "                    for d, r in barres.items()]"),
    "S21 le dernier achat possible écarté": ("                if j >= len(serie):", "                if j >= len(serie) - 1:"),
    "S22 l'indice lu au surlendemain du signal": ('return dans_l_indice(lecture["passages"].get(v, []), serie[j]["date"])',
                                                  'return dans_l_indice(lecture["passages"].get(v, []), serie[min(j + 1, len(serie) - 1)]["date"])'),
    "S14 les trous d'une autre valeur": ("trous[v] = sorted(iso(d) for d, _ in lecteur.trous(c, m))",
                                         'trous[v] = sorted(iso(d) for d, _ in lecteur.trous(c, "VIE"))'),
}


def charger(chemin, racine):
    """Charge une copie du juge comme module.

    ① RÔLE — Rendre le juge (tel quel ou saboté) importable sans toucher au dépôt.
    ② CONTEXTE D'APPEL — `cas`, une fois par lancement en mode « --un ».
    ③ ENTRÉE — `chemin` : la copie du juge · `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — La copie importe ses voisins depuis `programmes/` de la racine (ligne remplacée par
      `copier`).
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — Ajouter `programmes/` au chemin d'import, charger le fichier sous le nom « juge_eprouve ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge importe COMMUN depuis son propre dossier ; la copie vit ailleurs.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut du module : des définitions, aucune écriture.
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur d'import.
      [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    spec = importlib.util.spec_from_file_location("juge_eprouve", chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def seances(*dates):
    """Fabrique des séances au prix fixe de 100, sauf la clôture, qui porte le rang de la séance.

    ① RÔLE — Donner aux cas fabriqués des séances où ni l'objectif ni la perte acceptée ne sont jamais touchés.
    ② CONTEXTE D'APPEL — `cas`, pour les cas T1 à T4.
    ③ ENTRÉE — Des dates AAAA-MM-JJ, dans l'ordre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des séances.
      [rend: 1]
    ⑥ TRAITEMENT — Une séance par date ; ouverture, plus haut et plus bas à 100 ; clôture à 100 plus le rang divisé
      par mille.
    ⑦ UNITÉ — Des euros par titre.
    ⑧ POURQUOI — Avec un objectif de +50 % et une perte acceptée de −50 %, seule l'échéance ou un trou ferment la
      position : le motif et la date de sortie disent alors seuls ce que le juge a fait.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [{"date": d, "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0 + k / 1000, "volume": 1.0}
            for k, d in enumerate(dates)]


class Signal:
    """Un module de signal fabriqué : il signale les séances dont la date est dans une liste donnée.

    ① RÔLE — Décider à la place d'une vraie stratégie, pour que chaque cas fabriqué sache où sont ses signaux.
    ② CONTEXTE D'APPEL — `cas`, passé à `jouer` comme module de signal.
    ③ ENTRÉE — Les dates à signaler.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Un objet dont la méthode `signaux` rend la liste des {"i": rang} des séances signalées.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir la série reçue — un morceau, quand le juge coupe aux trous.
    ⑦ UNITÉ — Des rangs dans la série reçue.
    ⑧ POURQUOI — `jouer` appelle la fonction de signal sur chaque morceau : le rang est relatif au morceau.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def __init__(self, *dates):
        self.dates = set(dates)

    def signaux(self, s):
        return [{"i": k} for k, b in enumerate(s) if b["date"] in self.dates]


def lancer_le_juge(copie, racine, *options):
    """Lance le programme principal d'une copie du juge et rend son code et sa sortie.

    ① RÔLE — Éprouver `main` tel qu'il tourne, ligne de commande comprise.
    ② CONTEXTE D'APPEL — `cas`, pour M1 à M3.
    ③ ENTRÉE — `copie` : la copie du juge · `racine` · `options` : les arguments qui suivent la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé) et la sortie, erreurs comprises.
      [rend: 2]
    ⑥ TRAITEMENT — Un sous-processus, sans le dossier du programme dans le chemin d'import.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `main` lit sa ligne de commande et rend un code ; seul un vrai lancement les éprouve.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Le juge lit des fichiers ; il n'écrit rien (relevé le 27-10-2026 dans `main`).
    ⑪ TERMINAISON — Borné à 300 secondes.
      [sort: non]
    """
    try:
        p = subprocess.run([sys.executable, "-I", "-B", copie, racine, *options], capture_output=True, text=True,
                           timeout=300)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, ""


def cas(copie, racine):
    """Joue tous les cas sur une copie du juge et rend leurs résultats.

    ① RÔLE — Le cœur des épreuves : chaque cas dit ce que le juge doit faire, et le vérifie.
    ② CONTEXTE D'APPEL — Le mode « --un » de ce programme.
    ③ ENTRÉE — `copie` : la copie du juge à éprouver · `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Celles du programme (④ de l'en-tête).
    ⑤ SORTIE — UNE valeur : la liste des (nom du cas, réussi ou non, détail).
      [rend: 1]
    ⑥ TRAITEMENT — Cas fabriqués T1 à T4 ; cas réels R1 à R5 ; lancements M1 à M3. Un cas qui lève une erreur
      compte comme échoué, avec l'erreur en détail.
    ⑦ UNITÉ — Des dates, des motifs, des nombres d'opérations.
    ⑧ POURQUOI — Voir ⑧ de l'en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier de cours dans un dossier temporaire, effacé.
    ⑪ TERMINAISON — Rend la main ; trois lancements du juge, bornés.
      [sort: non]
    """
    B = charger(copie, racine)
    pos = B.charger_module(B.trouver(racine, "MODULE_POSITIONS.py"), "pos")
    fiche = {"tp": "+50%", "sl": "-50%", "horizon": "3", "univers": "XXX"}
    mn = {"XXX": "XXX"}
    res = []

    def un(nom, f):
        try:
            ok, detail = f()
        except Exception as e:
            ok, detail = False, "%s : %s" % (type(e).__name__, str(e)[:160])
        res.append((nom, ok, detail))

    suite = seances("2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10", "2025-01-13",
                    "2025-01-14", "2025-01-15", "2025-01-16")
    trouee = seances("2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10",
                     "2025-01-14", "2025-01-15", "2025-01-16", "2025-01-17", "2025-01-20", "2025-01-21")

    def t1():
        lec = {"passages": {"XXX": [("2025-01-14", None)]}, "trous": {}, "composition": True}
        o, _ = B.jouer(fiche, {"XXX": suite}, mn, Signal("2025-01-09", "2025-01-13"), pos, lecture=lec)
        got = [x["date_signal"] for x in o]
        return got == ["2025-01-13"], "signaux joués %s (attendu : le seul 2025-01-13, acheté le 14, jour d'entrée)" % got

    def t2():
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = B.jouer(fiche, {"XXX": trouee}, mn, Signal("2025-01-08"), pos, lecture=lec)
        got = [(x["motif"], x["date_sortie"]) for x in o]
        # Décision de Jean-Luc du 27-10-2026 à 13h30 (« 1 la garder ») : la position traverse le trou du 13-01 ;
        # l'échéance, trois séances qui ont un cours après l'achat du 09, tombe le 15.
        return got == [("HORIZON", "2025-01-15")], "sorties %s (attendu : HORIZON le 2025-01-15, après le trou)" % got

    def t3():
        lec = {"passages": {}, "trous": {}, "composition": False}
        sig = Signal("2025-01-06", "2025-01-08", "2025-01-10")
        o1, _ = B.jouer(fiche, {"XXX": suite}, mn, sig, pos)
        o2, _ = B.jouer(fiche, {"XXX": suite}, mn, sig, pos, lecture=lec)
        return o1 == o2 and len(o1) == 3, "%d opérations sans lecture, %d avec une lecture neutre" % (len(o1), len(o2))

    def t4():
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = B.jouer(fiche, {"XXX": trouee}, mn, Signal("2025-01-17"), pos, lecture=lec)
        got = [(x["motif"], x["date_sortie"]) for x in o]
        return got == [("HORIZON", "2025-01-21")], "sorties %s (attendu : HORIZON le 2025-01-21, fin des données)" % got

    def t5():
        # La valeur sort de l'indice : sa dernière séance DANS l'indice est le 13-01 (les deux bornes d'un passage sont
        # des séances dans l'indice). Acheté le 13 : gardé ; acheté le 14 (signal du 13) : refusé.
        lec = {"passages": {"XXX": [("2025-01-06", "2025-01-13")]}, "trous": {}, "composition": True}
        o, _ = B.jouer(fiche, {"XXX": suite}, mn, Signal("2025-01-10", "2025-01-13"), pos, lecture=lec)
        got = [x["date_signal"] for x in o]
        return got == ["2025-01-10"], "signaux joués %s (attendu : le seul 2025-01-10, acheté le 13, dernier jour dans l'indice)" % got

    def t6():
        # L'échéance atteinte pile à la dernière séance d'un morceau : c'est une sortie à l'échéance, pas un trou.
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = B.jouer(fiche, {"XXX": trouee}, mn, Signal("2025-01-06"), pos, lecture=lec)
        got = [(x["motif"], x["date_sortie"]) for x in o]
        return got == [("HORIZON", "2025-01-10")], "sorties %s (attendu : HORIZON le 2025-01-10, troisième séance après l'achat)" % got

    un("T1 l'achat dans l'indice, pas le signal", t1)
    def t7():
        # Le signal à la dernière séance d'un morceau (le 10-01, veille du trou) achète à la séance suivante qui a un
        # cours, le 14-01, et sort à l'échéance le 17 (relecture du 27-10-2026 : il disparaissait sans un mot).
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = B.jouer(fiche, {"XXX": trouee}, mn, Signal("2025-01-10"), pos, lecture=lec)
        got = [(x["date_signal"], x["pe"], x["date_sortie"]) for x in o]
        return got == [("2025-01-10", 100.0, "2025-01-17")], "opérations %s (attendu : signal du 10, achat le 14, sortie le 17)" % got

    def t8():
        # L'achat à la dernière séance des données, dont le plus haut touche l'objectif : l'opération existe, sortie TP
        # le jour même (R-608 : la séance d'achat compte). Sabotage S21.
        fin = [dict(b) for b in trouee]
        fin[-1]["high"] = 200.0
        o, _ = B.jouer(fiche, {"XXX": fin}, mn, Signal("2025-01-20"), pos,
                       lecture={"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False})
        got = [(x["motif"], x["date_sortie"]) for x in o]
        return len(got) == 1 and got[0][0].startswith("TP") and got[0][1] == "2025-01-21", \
            "sorties %s (attendu : TP le 2025-01-21, jour de l'achat, dernière séance)" % got

    un("T2 la position traverse le trou", t2)
    un("T7 le signal la veille d'un trou achète après le trou", t7)
    un("T8 l'achat à la dernière séance des données", t8)
    un("T3 une lecture neutre ne change rien", t3)
    un("T4 le dernier morceau finit avec les données", t4)
    un("T5 la sortie de l'indice le lendemain de l'achat", t5)
    un("T6 l'échéance pile la veille d'un trou", t6)

    mnemo = B.table_mnemoniques(B.trouver(racine, "REFERENTIEL_VALEURS"))
    f_maitre = B.fichiers_de_cours(racine)[0]
    neuf, lec = B.lire_par_le_lecteur(racine, os.path.relpath(f_maitre, racine), mnemo)

    def r1():
        p = lec["passages"]["EIFFAGE"]
        got = (B.dans_l_indice(p, "2025-12-19"), B.dans_l_indice(p, "2025-12-22"))
        return got == (False, True), "Eiffage le 19-12-2025, le 22-12-2025 : %s (attendu : non, oui)" % (got,)

    def r2():
        p = lec["passages"]["ACCOR"]
        got = tuple(B.dans_l_indice(p, d) for d in ("2020-09-18", "2020-09-21", "2024-03-15", "2024-03-18"))
        return got == (True, False, False, True), \
            "Accor les 18-09-2020, 21-09-2020, 15-03-2024, 18-03-2024 : %s (attendu : oui, non, non, oui)" % (got,)

    def r3():
        # Bouygues, du 03 au 10-11-2011 : six séances que ni Yahoo ni bnains ne portent (la plus longue lacune réelle,
        # relevé de Cowork ; « non comblé » au journal des réparations). Le trou d'Accor du 24-12-2010, pris d'abord,
        # a été comblé le 27-10-2026 avec les cinq demi-séances (A-555 (b)) : si une décision comble aussi ces six
        # séances, ce cas tombe, et un autre trou réel est à prendre.
        c, l = B.lire_par_le_lecteur(racine, HISTORIQUE, mnemo)
        m = B.couper_aux_trous(c["BOUYGUES"], l["trous"]["BOUYGUES"])
        got = (m[0][-1]["date"], m[1][0]["date"])
        # Les trous sont ceux de LA valeur : le 03-11-2011 manque à Bouygues, pas à Accor (sabotage S14).
        propre = ("2011-11-03" in l["trous"]["BOUYGUES"], "2011-11-03" in l["trous"]["ACCOR"])
        return got == ("2011-11-02", "2011-11-11") and propre == (True, False), \
            "Bouygues, historique des 20 ans : premier morceau fini le %s, second commencé le %s (attendu : 2011-11-02, " \
            "2011-11-11) ; le 03-11-2011 manque à Bouygues, à Accor : %s (attendu : oui, non)" % (got + (propre,))

    def r4():
        vieux = B.charger_cours(f_maitre)
        return vieux == neuf and len(neuf) > 0, "%d valeurs ; mêmes séries que l'ancienne lecture : %s" % (len(neuf), vieux == neuf)

    fiches = __import__("csv").DictReader(open(B.trouver(racine, "cac40_strategies.csv"), encoding="utf-8-sig"))
    f = next(x for x in fiches if x["id"] == FICHE)
    _, _, bornes = B.porte_0(f)
    f.setdefault("_fonction_signal", "signaux_c5etendu10")
    sig = B.charger_module(B.trouver(racine, "MODULE_C5_ETENDU_10"), "sig")
    avec = []

    def r5():
        o1, _ = B.jouer(f, neuf, mnemo, sig, pos, periode=bornes)
        o2, _ = B.jouer(f, neuf, mnemo, sig, pos, periode=bornes, lecture=lec)
        avec.append(len(o2))
        k = lambda x: (x["valeur"], x["date_signal"])
        retirees = [x for x in o1 if k(x) not in {k(y) for y in o2}]
        ajoutees = [y for y in o2 if k(y) not in {k(x) for x in o1}]

        def achat(x):
            s = neuf[x["valeur"]]
            return s[[b["date"] for b in s].index(x["date_signal"]) + 1]["date"]
        hors = [x for x in retirees if not B.dans_l_indice(lec["passages"][x["valeur"]], achat(x))]
        ok = len(retirees) > 0 and len(hors) == len(retirees) and not ajoutees
        return ok, "%s : %d → %d opérations ; %d retirées, dont %d achetées hors de l'indice ; %d ajoutées" % (
            FICHE, len(o1), len(o2), len(retirees), len(hors), len(ajoutees))

    def r6():
        # Le fichier du soir est déclaré incrément : le lecteur n'y donne aucun passage dans l'indice. Le juge refuse
        # (relecture du 27-10-2026 : sans ce refus, chaque achat était écarté sans un mot, 0 opération).
        try:
            B.lire_par_le_lecteur(racine, "donnees/claude_cours_nouveaux.csv", mnemo)
            return False, "le fichier incrément a été lu sans refus"
        except ValueError as e:
            return str(e).startswith("le lecteur unique ne connaît aucun passage"), "refus : %s" % str(e)[:80]

    def r7():
        # Les lignes du maître dans l'ordre inverse : les séries rendues sont les mêmes, triées.
        d_ = tempfile.mkdtemp()
        try:
            lignes = open(f_maitre, encoding="utf-8").read().splitlines()
            f_ = os.path.join(d_, "melange.csv")
            open(f_, "w", encoding="utf-8").write("\n".join([lignes[0]] + lignes[1:][::-1]) + "\n")
            m_, _ = B.lire_par_le_lecteur(racine, os.path.relpath(f_, racine), mnemo)
            return m_ == neuf, "lignes inversées : mêmes séries que le maître : %s" % (m_ == neuf)
        finally:
            shutil.rmtree(d_, ignore_errors=True)

    un("R1 Eiffage entre le 22-12-2025", r1)
    un("R2 Accor sort et revient", r2)
    un("R3 le trou de Bouygues de novembre 2011", r3)
    un("R4 le lecteur rend les séries d'avant", r4)
    un("R5 chaque achat retiré est hors de l'indice", r5)
    un("R6 un fichier incrément est refusé", r6)
    un("R7 des lignes dans le désordre", r7)

    d = tempfile.mkdtemp()
    try:
        faux = os.path.join(d, "cours.csv")
        shutil.copyfile(f_maitre, faux)
        with open(faux, "a", encoding="utf-8") as h:
            h.write("SOCIETE INVENTEE,2026-10-26,1,1,1,1,1,abc\n")

        def m1():
            code, out = lancer_le_juge(copie, racine, FICHE, "--cours=" + faux)
            ok = code == 1 and "ARRET : le lecteur unique" in out and "LECTURE :" not in out
            return ok, "nom inconnu dans --cours : code %d, arrêt dit : %s" % (code, "ARRET : le lecteur unique" in out)

        def m2():
            code, out = lancer_le_juge(copie, racine, FICHE, "--cours=" + HISTORIQUE)
            n = re.search(r"LECTURE :.* (\d+) seances sans cours", out)
            ok = code == 0 and n is not None and int(n.group(1)) > 0
            return ok, "historique des 20 ans par --cours : code %d, séances sans cours %s (attendu : plus de 0)" % (
                code, n.group(1) if n else "non dites")

        def m3():
            code, out = lancer_le_juge(copie, racine, FICHE)
            n = re.search(r"=== %s .*?\n(?:.*\n){0,3}?\s+(\d+) operations" % re.escape(FICHE), out)
            ok = code == 0 and n is not None and avec and int(n.group(1)) == avec[0]
            return ok, "main sur le maître : %s opérations, jouer avec la lecture : %s" % (
                n.group(1) if n else "non dites", avec[0] if avec else "non mesuré")

        illisible = os.path.join(d, "illisible.csv")
        shutil.copyfile(f_maitre, illisible)
        with open(illisible, "a", encoding="utf-8") as h:
            h.write("VINCI,26/10/2026,1,1,1,1,1,abc\n")
        troue = os.path.join(d, "troue.csv")
        with open(troue, "w", encoding="utf-8") as h:   # le maître sans Vinci les 12-03-2025 et 18-06-2025
            for l in open(f_maitre, encoding="utf-8"):
                if not (l.startswith("VINCI,2025-03-12,") or l.startswith("VINCI,2025-06-18,")):
                    h.write(l)

        def m4():
            code, out = lancer_le_juge(copie, racine, FICHE, "--cours=" + illisible)
            ok = code == 1 and "ARRET : le lecteur unique a mis 1 ligne(s)" in out
            return ok, "date illisible dans --cours : code %d" % code

        def m5():
            code, out = lancer_le_juge(copie, racine, FICHE, "--cours", HISTORIQUE)
            return code == 1 and "ARRET : option inconnue" in out, "« --cours » sans « = » : code %d" % code

        def m6():
            code, out = lancer_le_juge(copie, racine, FICHE + "-FAUTE")
            return code == 1 and "ARRET : la fiche visee" in out, "fiche visée absente : code %d" % code

        def m7():
            code, out = lancer_le_juge(copie, racine, FICHE, "--cours=" + troue)
            # Les deux nombres se lisent entiers : « 42 coupures » contient « 2 coupures » (sabotage S18, 27-10-2026).
            n = re.search(r"LECTURE :.* ; (\d+) coupures des series, sur (\d+) seances sans cours", out)
            got = (int(n.group(1)), int(n.group(2))) if n else None
            return code == 0 and got == (2, 2), "Vinci privé de deux séances : coupures et séances %s (attendu : (2, 2))" % (got,)

        un("M1 un nom inconnu arrête le juge", m1)
        un("M2 l'option --cours lit le fichier donné", m2)
        un("M3 main juge avec la lecture", m3)
        un("M4 une date illisible arrête le juge", m4)
        un("M5 une option mal écrite arrête le juge", m5)
        un("M6 une fiche visée absente arrête le juge", m6)
        un("M7 le compte exact des coupures", m7)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return res


def copier(src, racine, a, b):
    """Écrit une copie du juge, sabotée ou non, dans un dossier temporaire.

    ① RÔLE — Préparer ce que le mode « --un » éprouvera.
    ② CONTEXTE D'APPEL — Le lancement principal, une fois par sabotage et une fois tel quel.
    ③ ENTRÉE — `src` : le texte du juge · `racine` · `a`, `b` : le texte à remplacer et son remplaçant (vides : tel
      quel).
    ④ CONDITIONS D'ENTRÉE — `a`, s'il n'est pas vide, figure UNE fois dans le juge.
    ⑤ SORTIE — DEUX valeurs : le dossier temporaire et le chemin de la copie.
      [rend: 2]
    ⑥ TRAITEMENT — Remplacer la ligne du chemin d'import par `programmes/` de la racine ; appliquer le sabotage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une cible introuvable ne sabote rien : elle lève AssertionError au lieu de passer pour un sabotage
      qui mord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier dans un dossier temporaire.
    ⑪ TERMINAISON — Rend la main, ou lève AssertionError.
      [sort: non]
    """
    assert src.count(LIGNE_DU_CHEMIN) == 1, "ligne du chemin d'import"
    s = src.replace(LIGNE_DU_CHEMIN, "sys.path.insert(0, %r)" % os.path.abspath(os.path.join(racine, "programmes")))
    if a:
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    d = tempfile.mkdtemp()
    p = os.path.join(d, "JUGE_DES_STRATEGIES.py")
    open(p, "w", encoding="utf-8").write(s)
    return d, p


if len(sys.argv) > 1 and sys.argv[1] == "--un":
    resultats = cas(sys.argv[2], sys.argv[3])
    for nom, ok, detail in resultats:
        print(("  ok   " if ok else "  ÉCHEC ") + nom + " — " + detail)
    sys.exit(0 if all(ok for _, ok, _ in resultats) else 1)

racine = os.path.abspath(sys.argv[1])
sortie = sys.argv[2] if len(sys.argv) > 2 else os.path.join(tempfile.mkdtemp(), "RELEVE_DU_JUGE_PAR_LE_LECTEUR.txt")
src = open(os.path.join(racine, "programmes", "JUGE_DES_STRATEGIES.py"), encoding="utf-8").read()
lignes = ["# Épreuves du juge par le lecteur unique (A-577, étape 1), jouées le "
          f"{datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Paris')):%d-%m-%Y à %Hh%M} (Paris) par un programme.",
          "# Le juge tel quel doit passer tous les cas ; un sabotage mord quand au moins un cas échoue (code 1)."]
fautes = 0
for nom, (a, b) in [("Z0 juge tel quel", ("", ""))] + list(SAB.items()):
    d, p = copier(src, racine, a, b)
    try:
        r = subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), "--un", p, racine],
                           capture_output=True, text=True, timeout=900)
        code, out = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        code, out = 124, "délai de 900 s dépassé\n"
    finally:
        shutil.rmtree(d, ignore_errors=True)
    if not a:
        lignes.append(f"{nom} : code {code}" + ("" if code == 0 else " — NON CONFORME"))
        lignes += [l for l in out.splitlines() if l.strip()]
        fautes += code != 0
    else:
        echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
        mord = code == 1 and bool(echecs)
        lignes.append(f"{nom} : code {code} — " + (("mord (" + " · ".join(echecs) + ")") if mord else
                                                   "NE MORD PAS" + ("" if code in (0, 1) else " : " + out.strip()[-200:])))
        fautes += not mord
open(sortie, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print("\n".join(lignes))
print(f"relevé : {sortie}")
print("VERDICT : " + ("tout est conforme" if not fautes else f"NON CONFORME — {fautes} faute(s)"))
sys.exit(1 if fautes else 0)
