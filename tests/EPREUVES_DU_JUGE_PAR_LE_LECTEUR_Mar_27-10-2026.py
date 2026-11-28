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
  appelant ne le donne. · Le cas M2 dépend de l'historique des 20 ans, dont il ne garde que les séances APRÈS la fenêtre du regard
  unique (mission REGARD, 12-11-2026) : s'il disparaît, le cas échoue (et le dit).
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
    # (29-10-2026, A-550 : l'appel porte le barème, le sabotage le garde)
    # (27-11-2026, lot L2 : l'appel porte aussi le calendrier de la vente, R-112 ; le sabotage le garde)
    "S6 les sorties testées dans le seul morceau": ("                op = jouer_une_entree(v, serie, j, tp, sl, h, mod_positions, lecture, bareme, recu, seances=_cal)",
                                                    "                op = jouer_une_entree(v, s, i + 1, tp, sl, h, mod_positions, lecture, bareme, recu, seances=_cal) if i + 1 < len(s) else None"),
    "S7 le signal de fin de morceau perdu": ("                j = rang[d_sig] + 1           #",
                                             "                j = rang[d_sig] + 1 if i + 1 < len(s) else len(serie)           #"),
    "S8 les lignes mises à part ignorées": ("    if a_part:\n", "    if False:\n"),
    "S9 l'option --cours ignorée": ("f_cours = os.path.join(base, _autre) if _autre else fichiers_de_cours(base)[0]",
                                    "f_cours = fichiers_de_cours(base)[0]"),
    "S10 un volume mal converti": ('"low": float(r["low"]), "close": float(r["close"]), "volume": float(r["volume"])}',
                                   '"low": float(r["low"]), "close": float(r["close"]), "volume": float(r["volume"]) + 1}'),
    # S11 recalé le 29-10-2026 (A-577, étape 7) : la lecture porte aussi « seances », la cible est le même texte allongé.
    # S11 recalé le 14-11-2026 (QE2 : la lecture porte aussi « trous_non_decides ») ; même visée
    "S11 la composition éteinte par le lecteur": ('"composition": True, "seances": seances,', '"composition": False, "seances": seances,'),
    # S12 recalé le 28-11-2026 (lot I1FIX) : l'appel de `main` lit les cours coupés à la partie de réglage
    # (`_cours_joues`, `_periode_jouee`, lot L1-CORR, A-1078) et porte le découpage du jour même (`types_de_marche=_tm`,
    # lot W2e-FIX, A-1105) ; même visée : retirer `lecture=lecture` du premier appel (celui sans reçu).
    "S12 la lecture non passée par main": (
        "ops, inconnus = jouer(f, _cours_joues, mnemo, mod_sig, mod_pos, periode=_periode_jouee, lecture=lecture,\n",
        "ops, inconnus = jouer(f, _cours_joues, mnemo, mod_sig, mod_pos, periode=_periode_jouee,\n"),
    "S13 les passages d'une autre valeur": ('passages[v] = [(iso(a), iso(b) if b else None) for a, b in c["dans_l_indice"].get(m, [])]',
                                            'passages[v] = [(iso(a), iso(b) if b else None) for a, b in c["dans_l_indice"].get("VIE", [])]'),
    "S15 une valeur sans passage acceptée": ("    if sans:   #", "    if False:   #"),
    "S16 une option mal écrite ignorée": ("    if _mal:\n", "    if False:\n"),
    # S17 recalé le 21-11-2026 : la garde a été réécrite au juge le 19-11-2026 (c01e42d43 : comparaison par
    # `_VC.norme`, puis 7066258c9 : « f is _visee ») ; même visée — la fiche visée absente doit arrêter le juge (M6).
    "S17 une fiche visée absente ignorée": ('    if cible and not any(f is _visee for f in passees):', "    if False:"),
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
    # QE (A-713 ①, 14-11-2026) : la traduction d'un mnémonique de société sortie (R8) et le refus d'une clé prise
    # deux fois (R9).
    "S23 le mnémonique d'une société sortie exigé au référentiel": ("        v = mnemo.get(m.upper(), cle_valeur(m))\n",
                                                                    "        v = mnemo[m.upper()]\n"),
    # QE2 (14-11-2026) : les trous non expliqués de l'univers d'une fiche, signalés sur sa période (R10)
    # S25 recalé le 28-11-2026 (lot I1FIX) : le même texte vit aussi dans `lecture_permise_pour_regler` (lot L1-CORR,
    # A-1078) ; la visée est allongée pour ne désigner que la ligne des trous non décidés, même sabotage.
    "S25 les trous non expliqués comptés hors de la période": (
        '.get("trous_non_decides", {}).get(v, []) if bornes[0] <= d <= bornes[1]]',
        '.get("trous_non_decides", {}).get(v, [])]'),
    "S26 les trous non expliqués jamais rendus par la lecture": (
        "        non_decides[v] = sorted(iso(d) for d, n in lecteur.trous(c, m) if n == lecteur.NON_DECIDEE)",
        "        non_decides[v] = []"),
    # QE2 tour 2 (superviseur R-759 ②) : la garde M (R11, M8, M9)
    "S27 la garde M ne refuse pas sur le regard unique": (
        "    if m_regard and (fiche.get(\"id\") or \"\") not in getattr(_CM, \"UNIVERS_BORNES_ACCEPTES_SUR_LE_REGARD_UNIQUE\", {}):",
        "    if False:"),
    # Q-1 et Q-2 de Cowork (14-11-2026) : la garde M dans `jouer` avec un reçu (R12) ; la fenêtre de M épinglée (R11)
    "S30 la garde M absente de la porte à reçu": ("        if _refus_m:\n            raise UniversBorneSurLeRegard",
                                                 "        if False:\n            raise UniversBorneSurLeRegard"),
    "S31 la fenêtre de M coupée au 2015-12-31": ("m_regard += sum(1 for d in jours if r_debut <= d <= r_fin)",
                                                "m_regard += sum(1 for d in jours if r_debut <= d <= \"2015-12-31\")"),
    # K-9 de Cowork (14-11-2026) : une seule écriture de « les séances touchent la fenêtre » (R12)
    "S32 la fenêtre du regard jamais touchée": ("    return bool(premiere) and not (str(premiere) > fin or str(derniere) < debut)",
                                                "    return False"),
    "S28 la garde M compte les sociétés écrites dans l'univers": ("        if mnemos[numero] & univers:\n            continue\n", ""),
    "S29 la ligne de la garde M non affichée": ("            _ligne_signal += \"\\n\" + _ligne_m\n", "            pass\n"),
    "S24 une clé prise deux fois admise": ("        if v in cours:\n            raise ValueError(\"le lecteur unique rend deux",
                                           "        if False:\n            raise ValueError(\"le lecteur unique rend deux"),
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


def copie_sans_la_fenetre(source, cible, fenetre):
    """Écrit une copie d'un fichier de cours SANS AUCUNE SÉANCE jusqu'à la fin de la fenêtre du regard unique, et avec
    deux trous fabriqués ; rend ce qui a été gardé, écarté, troué, et les séances de la fenêtre RELUES dans la copie.

    ① RÔLE — Fermer le cas M2 par une PROPRIÉTÉ (mission REGARD du 12-11-2026, pas 1 ; superviseur GITHUB, marche 1) :
      M2 lançait le juge sur l'historique des 20 ans avec C5E10-QA-V1, une version de C5, à chaque certification de
      nuit — le seul calcul de C5 sur 2000-2023 qui tournait. Il ne calculait que 2024-2026 parce que la fiche borne sa
      période (`JUGE_DES_STRATEGIES`, `_bornes`) : la garde tenait à une case de la fiche.
    ② CONTEXTE D'APPEL — Le cas M2 de `cas` ; l'épreuve du regard unique (`tests/EPREUVES_DU_REGARD_UNIQUE_Jeu_12-11-2026.py`),
      qui la sabote.
    ③ ENTRÉE — `source` : un fichier de cours (en-tête, puis « valeur,date,… ») · `cible` : le chemin de la copie ·
      `fenetre` : (début, fin) en textes AAAA-MM-JJ, LUE au contrat (`CONTRATS_DES_FICHIERS.fenetre_du_regard_unique`).
    ④ CONDITIONS D'ENTRÉE — La date est la deuxième case de chaque ligne.
    ⑤ SORTIE — QUATRE valeurs : lignes gardées, lignes écartées, lignes retirées pour faire les trous, séances de la
      fenêtre relues dans la copie (0 attendu).
      [rend: 4]
    ⑥ TRAITEMENT — ① garder l'en-tête et les lignes datées APRÈS la fin de la fenêtre · ② retirer, de la première
      valeur gardée, sa 100e et sa 200e séance (deux trous au milieu de sa série) · ③ relire la copie et compter les
      lignes dont la date tombe dans la fenêtre.
    ⑦ UNITÉ — Des lignes de cours.
    ⑧ POURQUOI — Le cas éprouve que « --cours lit le fichier donné » : il n'a pas besoin des 20 ans (superviseur
      GITHUB, M2). Il le prouve par les SÉANCES SANS COURS, que le maître n'a pas ; la partie 2024 et suivantes de
      l'historique n'en a pas non plus (mesuré le 12-11-2026 : « 0 coupures des series, sur 0 seances sans cours ») —
      d'où les deux trous fabriqués. La fenêtre vient du contrat : si elle grandit, la copie suit.
    ⑨ CE QUI CLOCHE — La relecture ③ compte les lignes de la COPIE, pas ce que le juge lit : le juge lit le fichier
      qu'on lui passe, et ce fichier est la copie (M2 passe son chemin).
    ⑩ EFFET — Écrit `cible`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    debut, fin = fenetre
    garde, ecarte, par_valeur, lignes = 0, 0, {}, []
    with open(source, encoding="utf-8") as e:
        tete = e.readline()
        for l in e:
            if l.split(",", 2)[1] > fin:
                lignes.append(l)
            else:
                ecarte += 1
    premiere = lignes[0].split(",", 1)[0] if lignes else None
    a_trouer = {i for i, l in enumerate(lignes) if l.split(",", 1)[0] == premiere}
    rangs = sorted(a_trouer)
    retirees = {rangs[k] for k in (100, 200) if k < len(rangs)}
    with open(cible, "w", encoding="utf-8") as s:
        s.write(tete)
        for i, l in enumerate(lignes):
            if i not in retirees:
                s.write(l)
                garde += 1
    dans = 0
    with open(cible, encoding="utf-8") as e:
        e.readline()
        for l in e:
            if debut <= l.split(",", 2)[1] <= fin:
                dans += 1
    return garde, ecarte, len(retirees), dans


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
    ⑥ TRAITEMENT — Cas fabriqués T1 à T8 ; cas réels R1 à R9 (R8 et R9 depuis le 14-11-2026, QE : une vraie ligne
      de Peugeot S.A., sortie, sous UG ; R10 depuis QE2 : ses trous non expliqués, sur la période) ; lancements M1 à M7. Un cas qui lève une erreur
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
    # depuis le 31-10-2026 (version B, points 5 et 9), `jouer` refuse une fiche sans moment d'achat ni données déclarés
    fiche = {"tp": "+50%", "sl": "-50%", "horizon": "3", "univers": "XXX", "entree": "DÉFAUT", "donnees_demandees": "cours"}
    mn = {"XXX": "XXX"}
    res = []

    def jouer_au_courtage_seul(*a, **k):
        # La valeur « XXX » est fabriquée : aucune liste de valeurs taxées ne la porte, et le barème réel lèverait, à
        # juste titre. Ces cas éprouvent la LECTURE (trous, indice) : ils se jouent au courtage seul (A-550, 29-10-2026).
        k.setdefault("bareme", "HIST_COURTAGE_SANS_TTF")
        # `jouer` n'accepte plus que le signal d'une fiche, un `SignalNomme` (A-542, 30-10-2026) : le signal fabriqué
        # de ces cas y est enveloppé, sans réglages.
        if isinstance(a[3], Signal):
            a = a[:3] + (B.SignalNomme(a[3].signaux, {}, "épreuve : signal fabriqué"),) + a[4:]
        return B.jouer(*a, **k)

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
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": suite}, mn, Signal("2025-01-09", "2025-01-13"), pos, lecture=lec)
        got = [x["date_signal"] for x in o]
        return got == ["2025-01-13"], "signaux joués %s (attendu : le seul 2025-01-13, acheté le 14, jour d'entrée)" % got

    def t2():
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": trouee}, mn, Signal("2025-01-08"), pos, lecture=lec)
        got = [(x["motif"], x["date_sortie"]) for x in o]
        # Décision de Jean-Luc du 27-10-2026 à 13h30 (« 1 la garder ») : la position traverse le trou du 13-01 ;
        # l'échéance, trois séances qui ont un cours après l'achat du 09, tombe le 15.
        return got == [("HORIZON", "2025-01-15")], "sorties %s (attendu : HORIZON le 2025-01-15, après le trou)" % got

    def t3():
        lec = {"passages": {}, "trous": {}, "composition": False}
        sig = Signal("2025-01-06", "2025-01-08", "2025-01-10")
        o1, _ = jouer_au_courtage_seul(fiche, {"XXX": suite}, mn, sig, pos)
        o2, _ = jouer_au_courtage_seul(fiche, {"XXX": suite}, mn, sig, pos, lecture=lec)
        return o1 == o2 and len(o1) == 3, "%d opérations sans lecture, %d avec une lecture neutre" % (len(o1), len(o2))

    def t4():
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": trouee}, mn, Signal("2025-01-17"), pos, lecture=lec)
        got = [(x["motif"], x["date_sortie"]) for x in o]
        return got == [("HORIZON", "2025-01-21")], "sorties %s (attendu : HORIZON le 2025-01-21, fin des données)" % got

    def t5():
        # La valeur sort de l'indice : sa dernière séance DANS l'indice est le 13-01 (les deux bornes d'un passage sont
        # des séances dans l'indice). Acheté le 13 : gardé ; acheté le 14 (signal du 13) : refusé.
        lec = {"passages": {"XXX": [("2025-01-06", "2025-01-13")]}, "trous": {}, "composition": True}
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": suite}, mn, Signal("2025-01-10", "2025-01-13"), pos, lecture=lec)
        got = [x["date_signal"] for x in o]
        return got == ["2025-01-10"], "signaux joués %s (attendu : le seul 2025-01-10, acheté le 13, dernier jour dans l'indice)" % got

    def t6():
        # L'échéance atteinte pile à la dernière séance d'un morceau : c'est une sortie à l'échéance, pas un trou.
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": trouee}, mn, Signal("2025-01-06"), pos, lecture=lec)
        got = [(x["motif"], x["date_sortie"]) for x in o]
        return got == [("HORIZON", "2025-01-10")], "sorties %s (attendu : HORIZON le 2025-01-10, troisième séance après l'achat)" % got

    un("T1 l'achat dans l'indice, pas le signal", t1)
    def t7():
        # Le signal à la dernière séance d'un morceau (le 10-01, veille du trou) achète à la séance suivante qui a un
        # cours, le 14-01, et sort à l'échéance le 17 (relecture du 27-10-2026 : il disparaissait sans un mot).
        lec = {"passages": {}, "trous": {"XXX": ["2025-01-13"]}, "composition": False}
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": trouee}, mn, Signal("2025-01-10"), pos, lecture=lec)
        got = [(x["date_signal"], x["pe"], x["date_sortie"]) for x in o]
        return got == [("2025-01-10", 100.0, "2025-01-17")], "opérations %s (attendu : signal du 10, achat le 14, sortie le 17)" % got

    def t8():
        # L'achat à la dernière séance des données, dont le plus haut touche l'objectif : l'opération existe, sortie TP
        # le jour même (R-608 : la séance d'achat compte). Sabotage S21.
        fin = [dict(b) for b in trouee]
        fin[-1]["high"] = 200.0
        o, _ = jouer_au_courtage_seul(fiche, {"XXX": fin}, mn, Signal("2025-01-20"), pos,
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
        # 12-11-2026 (E2a, installation du lot d'octobre) : le comblement par bnains du lot (« 17 séances comblées sans
        # ABC », commit ec686c76) a rempli les 04, 07, 08 et 10-11-2011 ; le 03 et le 09 restent sans cours. Le trou
        # du 03 est toujours réel : le second morceau commence désormais le 04 (lu dans le fichier le 12-11-2026).
        c, l = B.lire_par_le_lecteur(racine, HISTORIQUE, mnemo)
        m = B.couper_aux_trous(c["BOUYGUES"], l["trous"]["BOUYGUES"])
        got = (m[0][-1]["date"], m[1][0]["date"])
        # Les trous sont ceux de LA valeur : le 03-11-2011 manque à Bouygues, pas à Accor (sabotage S14).
        propre = ("2011-11-03" in l["trous"]["BOUYGUES"], "2011-11-03" in l["trous"]["ACCOR"])
        return got == ("2011-11-02", "2011-11-04") and propre == (True, False), \
            "Bouygues, historique des 20 ans : premier morceau fini le %s, second commencé le %s (attendu : 2011-11-02, " \
            "2011-11-04) ; le 03-11-2011 manque à Bouygues, à Accor : %s (attendu : oui, non)" % (got + (propre,))

    def r4():
        vieux = B.charger_cours(f_maitre)
        return vieux == neuf and len(neuf) > 0, "%d valeurs ; mêmes séries que l'ancienne lecture : %s" % (len(neuf), vieux == neuf)

    # LE REGISTRE SE NOMME ET SE LIT AU CONTRAT (n°83, 05-11-2026) : la fiche est la dernière ligne de son identifiant
    import CONTRATS_DES_FICHIERS as contrat
    f = contrat.fiches_du_registre(B.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES))[FICHE]
    _, _, bornes = B.porte_0(f)
    sig = B.signal_de_la_fiche(racine, f)   # le signal que la fiche nomme (A-542, 30-10-2026)
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

    # QE (A-713 ①, superviseur R-759 du 14-11-2026) : une VRAIE ligne d'une société sortie (R-732), Peugeot S.A. sous
    # UG, recopiée du témoin des 20 ans du 13-11-2026 à 10h59 ; le juge levait KeyError sur `mnemo["UG"]`.
    ligne_ug = "UG,2017-02-28,18.015,18.085,17.9,17.96,2561602,bnains archives (société sortie 48)"
    d_qe = tempfile.mkdtemp()
    try:
        f_qe = os.path.join(d_qe, "maitre_et_ug.csv")
        with open(f_qe, "w", encoding="utf-8") as h:
            h.write(open(f_maitre, encoding="utf-8").read().rstrip("\n") + "\n" + ligne_ug + "\n")

        def r8():
            c8, l8 = B.lire_par_le_lecteur(racine, os.path.relpath(f_qe, racine), mnemo)
            v = B.cle_valeur("UG")
            got = ([b["date"] for b in c8.get(v, [])], B.dans_l_indice(l8["passages"].get(v, []), "2017-02-28"),
                   B.dans_l_indice(l8["passages"].get(v, []), "2021-01-18"), "UG" in mnemo,
                   {k: s for k, s in c8.items() if k != v} == neuf)
            return got == (["2017-02-28"], True, False, False, True), \
                "UG (au référentiel : %s) : séances %s, dans l'indice le 2017-02-28 %s, le 2021-01-18 %s ; " \
                "les autres séries égales au maître %s (attendu : non, [2017-02-28], oui, non, oui)" % (
                    got[3], got[0], got[1], got[2], got[4])

        def r9():
            # deux mnémoniques traduits vers la même clé : la seconde série écraserait la première sans un mot
            faux = dict(mnemo)
            faux["UG"] = mnemo["AC"]
            try:
                B.lire_par_le_lecteur(racine, os.path.relpath(f_qe, racine), faux)
                return False, "UG et AC sous la même clé %s : lu sans refus" % mnemo["AC"]
            except ValueError as e:
                return str(e).startswith("le lecteur unique rend deux mnémoniques sous la même clé %s" % mnemo["AC"]), \
                    "refus : %s" % str(e)[:100]

        un("R8 une société sortie (UG, vraie ligne) est lue sous sa clé, avec ses passages", r8)
        un("R9 deux mnémoniques sous la même clé sont refusés", r9)

        def r10():
            # QE2 : la lecture rend les trous de nature non décidée ; UG (vraie ligne, sortie le 2021-01-15) en a dans sa
            # présence dans l'indice ; la fiche qui le demande les voit sur sa période, et seulement là
            c10, l10 = B.lire_par_le_lecteur(racine, os.path.relpath(f_qe, racine), mnemo)
            nd = l10["trous_non_decides"].get("UG", [])
            fiche = {"univers": "UG"}
            dedans = B.trous_non_expliques(fiche, l10, mnemo, ("2018-01-01", "2018-12-31"))
            attendu = [x for x in nd if "2018-01-01" <= x <= "2018-12-31"]
            ok = (len(nd) > 0 and nd == l10["trous"]["UG"] and len(attendu) > 0
                  and dedans == [("UG", len(attendu), attendu[0], attendu[-1])]
                  and B.trous_non_expliques(fiche, l10, mnemo, ("2022-01-01", "2022-12-31")) == [])
            return ok, "UG : %d trous non décidés ; en 2018 : %s ; en 2022 : %s" % (
                len(nd), dedans, B.trous_non_expliques(fiche, l10, mnemo, ("2022-01-01", "2022-12-31")))

        un("R10 les trous non expliqués de l'univers sur la période de la fiche (UG)", r10)

        def composition_attendue(univers, debut, fin, fenetre=None):
            # calcul de l'épreuve, sans le juge : IDENTITES et PASSAGES lus en CSV, les dates de l'indice publié
            import csv as _csv
            lire = lambda rel: list(_csv.DictReader(open(os.path.join(racine, rel), encoding="utf-8-sig", newline="")))
            ident = lire("donnees/sources_indice/IDENTITES_DES_SOCIETES.csv")
            pas = lire("donnees/sources_indice/PASSAGES_DANS_LE_CAC40.csv")
            dates = [l.split(",", 1)[0] for l in open(os.path.join(racine, "donnees/sources_indice/INDICE_CAC40.csv"),
                                                    encoding="utf-8-sig").read().splitlines()[1:]]
            dates = [d for d in dates if debut <= d <= fin]
            ouvertes = {r["numero"] for r in ident if not r["fin"]}
            total, dedans = 0, 0
            for numero in {r["numero"] for r in ident} - ouvertes:
                ls = [r for r in ident if r["numero"] == numero]
                if {r["mnemonique"].strip().upper() for r in ls} & set(univers):
                    continue
                codes = {r["isin"] for r in ls if r["isin"]}
                per = [(p["premiere_seance"], p["derniere_seance"] or "9999") for p in pas if p["isin_bnains"] in codes]
                jours = [d for d in dates if any(a <= d <= b for a, b in per)]
                total += len(jours)
                dedans += sum(1 for d in jours if fenetre and fenetre[0] <= d <= fenetre[1])
            return (total, dedans) if fenetre else total

        def r11():
            # la garde M, fonction seule : l'univers écrit d'IND-001-RETEST, et le même avec UG (sortie) ajouté
            f11 = contrat.fiches_du_registre(B.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES))["IND-001-RETEST"]
            u = B.mnemoniques_de_l_univers(f11["univers"])
            m1 = B.composition_hors_univers(racine, f11, "2000-01-03", "2026-10-30")
            m2 = B.composition_hors_univers(racine, dict(f11, univers=f11["univers"] + ",UG"), "2000-01-03", "2026-10-30")
            a1, a2 = composition_attendue(u, "2000-01-03", "2026-10-30"), composition_attendue(u + ["UG"], "2000-01-03", "2026-10-30")
            # Q-2 de Cowork : la part dans la fenêtre du regard unique, LUE au contrat, épinglée elle aussi
            _, f1 = composition_attendue(u, "2000-01-03", "2026-10-30", contrat.fenetre_du_regard_unique())
            return (m1[0] == a1 and m2[0] == a2 and a2 < a1 and m1[1] == f1 and 0 < f1 < a1), \
                "IND-001-RETEST M %s (attendu %d, dont %d dans la fenêtre) ; avec UG %s (attendu %d)" % (m1, a1, f1, m2, a2)

        un("R11 la garde M, calculée sur la composition historique (IND-001-RETEST, avec et sans UG)", r11)

        def r12():
            # Q-1 de Cowork : la porte qui consomme le regard unique passe un reçu à `jouer` ; la garde M doit l'arrêter
            # AVANT la vérification du reçu (un reçu fictif : sans la garde, c'est le reçu qui serait refusé, autrement)
            f12 = contrat.fiches_du_registre(B.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES))["IND-001-RETEST"]
            c12, l12 = B.lire_par_le_lecteur(racine, HISTORIQUE, mnemo)
            try:
                B.jouer(f12, c12, mnemo, B.signal_de_la_fiche(racine, f12), pos, periode=("2000-01-03", "2023-12-29"),
                        lecture=l12, recu=(racine, "RECU_FICTIF_DE_L_EPREUVE"))
                return False, "jouer a rendu la main"
            except B.RegardNonInscrit as e:
                return (type(e).__name__ == "UniversBorneSurLeRegard" and "REFUSEE (garde M, regard unique)" in str(e)), \
                    "%s : %s" % (type(e).__name__, str(e)[:110])

        un("R12 la garde M arrête `jouer` quand un reçu est passé (porte JUGER_UNE_FICHE)", r12)
    finally:
        shutil.rmtree(d_qe, ignore_errors=True)

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
            # LE REGARD UNIQUE (R-505 ③ ; mission REGARD du 12-11-2026, pas 1) : M2 ne lit PLUS l'historique des 20 ans,
            # mais une copie SANS AUCUNE SÉANCE de la fenêtre du regard unique (lue au contrat), avec deux trous.
            import CONTRATS_DES_FICHIERS as CF
            sans = os.path.join(d, "historique_sans_la_fenetre.csv")
            garde, ecarte, trous, dans = copie_sans_la_fenetre(os.path.join(racine, HISTORIQUE), sans,
                                                              CF.fenetre_du_regard_unique())
            if dans:
                return False, "la copie passée au juge porte %d séance(s) de la fenêtre du regard unique" % dans
            code, out = lancer_le_juge(copie, racine, FICHE, "--cours=" + sans)
            n = re.search(r"LECTURE :.* (\d+) seances sans cours", out)
            ok = code == 0 and n is not None and int(n.group(1)) > 0
            return ok, ("historique sans la fenêtre du regard unique (%d lignes gardées, %d écartées, %d trous) par "
                        "--cours : code %d, séances sans cours %s (attendu : plus de 0)" % (
                            garde, ecarte, trous, code, n.group(1) if n else "non dites"))

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

        # QE2 tour 2 : la garde M, LUE DANS LA SORTIE du juge. M8 : le maître allongé d'une vraie ligne de 2000 fait
        # entrer la fiche IND-001-RETEST dans la fenêtre du regard unique : refus, code 1, AVANT la garde
        # RegardNonInscrit. M9 : la fiche C5E10-QA-V1 sur le maître, verdict BORNÉ, M lu dans la ligne.
        # N-14 (RELU Cowork du 15-11-2026, réparé le 16-11-2026) : la ligne était ACCOR du 2000-01-03 au cours brut ;
        # depuis la courbe des calculs (programmes/COURBE_DES_CALCULS.py, venue de main), un fichier de cours autre que
        # le maître, non déclaré au cours brut, qui laisse VOIR une grande opération au jour dit est refusé avant toute
        # garde du juge (garder_la_nature, règle 2) — et entre ACCOR 2000-01-03 et ACCOR 2024 du maître passe la
        # scission Edenred (AC 2010-07-02, ×0,6498), vue : le juge s'arrêtait sur la courbe, jamais sur la garde M.
        # La garde de la courbe a raison ; c'était la PRÉMISSE du cas qui était fausse. La ligne est donc choisie par
        # une PROPRIÉTÉ, sans écrire de cours dans ce fichier : la première ligne du 2000-01-03 de l'historique des
        # 20 ans (HISTORIQUE, une vraie ligne, R-732) d'une valeur de l'univers de la fiche à laquelle RECONSTRUIRE ne
        # connaît AUCUNE opération sur titre (lue par COURBE_DES_CALCULS.lire_les_operations, la liste unique, R-708) :
        # aucune grande opération ne peut alors tomber entre 2000 et le maître. M ne dépend que de l'univers et de la
        # date de début : le cas éprouve la même garde, avec le même M attendu.
        long_ = os.path.join(d, "avec_2000.csv")
        C8 = B.charger_module(os.path.join(racine, "programmes", "COURBE_DES_CALCULS.py"), "courbe_du_cas_m8")
        connus8, ops8 = C8.lire_les_operations(racine)
        u8 = B.mnemoniques_de_l_univers(contrat.fiches_du_registre(
            B.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES))["IND-001-RETEST"]["univers"])
        noms8 = {mnemo[m].replace("_", " ") for m in u8 if m in mnemo} & (connus8 - set(ops8))
        ligne8 = next((l.rstrip("\n") for l in open(os.path.join(racine, HISTORIQUE), encoding="utf-8")
                       if l.split(",")[1:2] == ["2000-01-03"] and l.split(",")[0] in noms8), None)
        with open(long_, "w", encoding="utf-8") as h:
            h.write(open(f_maitre, encoding="utf-8").read().rstrip("\n") + "\n" + (ligne8 or "") + "\n")
        dates_maitre = sorted(l.split(",")[1] for l in open(f_maitre, encoding="utf-8").read().splitlines()[1:] if l)

        def m8():
            if ligne8 is None:
                return False, ("PRÉMISSE FAUSSE : aucune ligne du 2000-01-03 dans %s pour une valeur de l'univers "
                               "d'IND-001-RETEST sans opération sur titre connue (%d candidate(s)) — rien n'est éprouvé"
                               % (HISTORIQUE, len(noms8)))
            code, out = lancer_le_juge(copie, racine, "IND-001-RETEST", "--cours=" + long_)
            n = re.search(r"UNIVERS BORNE \(garde M\) : M = (\d+) .*?dont (\d+) dans la fenetre", out)
            u = B.mnemoniques_de_l_univers(contrat.fiches_du_registre(
                B.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES))["IND-001-RETEST"]["univers"])
            att = composition_attendue(u, "2000-01-03", min("2026-10-30", dates_maitre[-1]))
            ok = (code == 1 and "REFUSEE (garde M, regard unique)" in out and "RegardNonInscrit" not in out
                  and n is not None and int(n.group(1)) == att)
            return ok, "IND-001-RETEST avec une ligne de 2000 (%s) : code %d, refus dit %s, M lu %s (attendu %d)" % (
                ligne8.split(",")[0], code, "REFUSEE (garde M" in out, n.group(1) if n else "absent", att)

        def m9():
            code, out = lancer_le_juge(copie, racine, FICHE)
            n = re.search(r"UNIVERS BORNE \(garde M\) : M = (\d+) ", out)
            f9 = contrat.fiches_du_registre(B.trouver(racine, contrat.NOM_DU_REGISTRE_DES_STRATEGIES))[FICHE]
            deb, fin = [x.strip() for x in f9["periode"].split("->")]
            att = composition_attendue(B.mnemoniques_de_l_univers(f9["univers"]), max(deb, dates_maitre[0]),
                                       min(fin, dates_maitre[-1]))
            ok = code == 0 and n is not None and int(n.group(1)) == att and att > 0 and "REFUSEE (garde M" not in out
            return ok, "%s sur le maître : code %d, M lu %s (attendu %d)" % (FICHE, code, n.group(1) if n else "absent", att)

        un("M8 la garde M refuse sur le regard unique, avant RegardNonInscrit", m8)
        un("M9 la garde M dit un verdict BORNÉ, M lu dans la sortie", m9)
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
# 0 SABOTAGE INAPPLICABLE (21-11-2026) : un texte visé qui n'est pas UNE fois dans le juge ne sabote rien. Il est
# relevé ici, nommé, compté comme faute, et les autres sabotages sont joués — au lieu du Traceback de `copier`, qui
# arrêtait toute l'épreuve sans dire lequel (passage GitHub 44836965428, S17, texte réécrit au juge le 19-11-2026).
inapplicables = [(nom, src.count(a)) for nom, (a, _b) in SAB.items() if src.count(a) != 1]
lignes.append("SABOTAGES INAPPLICABLES : %d (attendu 0)" % len(inapplicables))
for nom, k in inapplicables:
    lignes.append("%s : INAPPLICABLE — texte visé présent %d fois dans le juge (attendu 1) — NON CONFORME" % (nom, k))
fautes += len(inapplicables)
for nom, (a, b) in [("Z0 juge tel quel", ("", ""))] + [x for x in SAB.items() if x[0] not in dict(inapplicables)]:
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
