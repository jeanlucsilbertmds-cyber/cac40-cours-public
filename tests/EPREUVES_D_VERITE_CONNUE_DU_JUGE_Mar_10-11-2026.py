"""ÉPREUVE À VÉRITÉ CONNUE DU JUGE — plan V7, bloc 5b, partie « écrite » (agent D), mardi 10-11-2026. Simulation uniquement.

LE SENS EN TÊTE — On fabrique des stratégies dont on connaît D'AVANCE la bonne réponse, et on vérifie que le juge
(`juger`, dans `programmes/JUGE_DES_STRATEGIES.py`, avec `programmes/MODULE_JUGEMENT.py`) la rend. Les signaux sont
calculés en REGARDANT L'AVENIR des vrais cours du fichier maître (`donnees/cours_maitre.csv`, quatre valeurs : Accor,
Air Liquide, Airbus, Axa) : une stratégie qui n'achète que les jours où l'objectif sera touché avant la perte acceptée
gagne à coup sûr ; celle qui n'achète que les jours où la perte sera touchée d'abord perd à coup sûr ; une stratégie
qui tire ses jours au sort ne sait rien. Le juge, lui, ne voit que les opérations : il doit dire « gagne » pour la
première, « perd » pour la deuxième, « rien de prouvé » pour la troisième. Une épreuve qui reste verte quand le juge se
trompe est une décoration (R-731) : `--saboter` casse le juge de onze façons et chacune doit faire rougir un cas.
LA VÉRITÉ NE VIENT PAS DU JUGE : l'issue d'un achat est relue ici, sur les cours, par `issue_sure`, et seuls les
achats dont l'issue est NETTE (pas de touche le jour d'achat, une seule borne touchée, avant l'avant-dernière séance de
l'horizon) sont retenus, pour que la vérité ne dépende d'aucune convention de la vente (ouverture, horizon, ordre des
bornes dans une même séance).

LE VERDICT LU ICI EST PROVISOIRE. Au 10-11-2026 le juge n'écrit pas de verdict « validée » : la grille de validation
(seuil du hasard 0,00135, critères C7 et C8) est le travail de l'agent B, et son appel dans `juger` celui de l'agent A
(PROPRIETAIRES_DES_FICHIERS.md, « non tranché » ①). L'épreuve lit donc les lignes que `juger` affiche déjà et
compose : VALIDÉE si et seulement si la marge sur le point mort est positive, la partie jamais vue est au-dessus du
point mort, sa borne basse de la partie jamais vue
est au-dessus du point mort, les trois fenêtres tiennent, et la stratégie bat le 95e centile du hasard dans les DEUX
modes (action au hasard, dates au hasard). Quand la grille de B sera branchée, son verdict s'ajoute ici (à faire, voir
echanges/A_RELIRE.md) ; le verdict provisoire reste comme second regard.

LES CAS « AUCUNE » (A1, A2) ATTENDENT L'AGENT A. Une stratégie sans durée maximale (horizon « aucune », contrat du lot 0
dans `programmes/COMMUN.py`) n'est pas jouable par le juge du 10-11-2026 : `lire_horizon` rend None et la vente lève
TypeError. Tant que `AUCUNE_ACTIVE` vaut False, un REFUS du juge sur ces cas s'écrit « ATTENTE A », ni vert ni rouge,
et n'entre pas dans le code de sortie ; mais si le juge les ACCEPTE déjà, ils sont jugés pour de vrai (vert ou rouge).
Seul le refus ATTENDU est mis en attente : une TypeError sur None ou portant le message du lot 0 ; toute autre erreur
est ROUGE (RELU Cowork D-4). Et le réglage se fait seul : dès que la copie du juge appelle `lire_horizon_ou_aucune`, ou
que `AUCUNE_ACTIVE` vaut True, un refus devient ROUGE.

USAGE : python3 -B tests/EPREUVES_D_VERITE_CONNUE_DU_JUGE_Mar_10-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 (le dépôt tel quel) est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si
une cible de sabotage est introuvable, si le nom demandé est inconnu ou si les données manquent (R-734).

① RÔLE — Prouver que le juge rend le verdict connu d'avance pour une stratégie gagnante, une perdante et trois
  stratégies de pur hasard, sur de vrais cours, et que chaque garde-fou du juge a des dents.
② CONTEXTE D'APPEL — À la main ; et par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque
  fichier de tests/ avec la racine seule, puis avec « --saboter » parce que ce texte contient ce mot. Ce programme se
  relance lui-même en mode « --cas <copie> <racine> » sur chaque copie du juge.
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/JUGE_DES_STRATEGIES.py`, `programmes/MODULE_JUGEMENT.py`,
  `programmes/MODULE_POSITIONS.py`, `programmes/MODULE_STATISTIQUES_*.py`, `programmes/COMMUN.py`, le référentiel des
  valeurs, `donnees/VALEURS_TTF.csv`, `donnees/cours_maitre.csv` avec les quatre valeurs jusqu'au 30-10-2026 au moins.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas, par sabotage, et le décompte des cas en attente.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage demandé : copier le juge et le module de jugement dans un dossier
  temporaire, appliquer le sabotage (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie :
  lire les cours, fabriquer les signaux à vérité connue, faire jouer et juger chaque stratégie par la copie, lire ce
  qu'elle affiche, comparer à la vérité · ③ Z0 doit être vert ; un sabotage doit faire rougir au moins un cas.
⑦ UNITÉ — Les seuils sont des FRACTIONS du prix d'entrée (0,04 = +4 %) ; l'horizon en SÉANCES ; les taux affichés
  par le juge en POURCENTS ; les gains en EUROS.
⑧ POURQUOI — Le plan V7 (bloc 5) : « une stratégie fausse doit être rejetée, une vraie acceptée ». Sans vérité
  connue, un juge qui dit « validée » à tout ou à rien ne se voit pas. Les vrais cours (R-732) plutôt que des cours
  tirés au sort : le juge est éprouvé sur la forme réelle des séances (écarts d'ouverture, frais réels avec la taxe sur
  les transactions de Accor, Air Liquide et Axa, Airbus non taxée — donnees/VALEURS_TTF.csv, année 2024). Le cas R1
  confronte une opération du juge à une ligne du fichier maître lue ici, sans passer par le lecteur du juge.
⑨ CE QUI CLOCHE — ① Le verdict lu est PROVISOIRE (voir plus haut) : le seuil 0,00135, C7 et C8 ne sont pas éprouvés.
  ② Les cas du hasard reposent sur trois graines fixes : leur vérité « rien de prouvé » est STATISTIQUE (un tirage
  peut, rarement, battre le 95e centile) ; les graines rendent le résultat reproductible, pas certain ; constaté vert
  au 10-11-2026 sur les trois. ③ Le voisinage (colline ou aiguille), la pire série et le creux ne sont pas jugés : leur
  vérité n'est pas connue d'avance. ④ La partie « jouée » de 5b (A1, A2 sur la vente de A) n'a pas tourné. ⑤ Le
  module de positions et le module de statistiques sont pris dans la racine, jamais sabotés ici : les sabotages ne
  portent que sur le juge et le module de jugement. ⑥ La lecture se fait sur le TEXTE affiché par `juger` : un
  changement de libellé fait rougir l'épreuve (c'est voulu : une ligne absente n'est pas un verdict), il faudra alors
  recaler les motifs de `lire_le_jugement`.
⑩ EFFET — Écrit et efface des dossiers temporaires ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 900 secondes ; un dépassement compte comme rouge. Un appel du
  juge peut ne pas revenir (code non borné), d'où cette borne. [sort: oui — code de sortie]
"""
import contextlib, csv, glob, importlib.util, io, os, random, re, shutil, subprocess, sys, tempfile

ICI = os.path.abspath(__file__)
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
MODULE = "programmes/MODULE_JUGEMENT.py"
MAITRE = "donnees/cours_maitre.csv"
# Les quatre valeurs : nom dans le fichier maître, mnémonique (clé d'identité, jamais le nom).
VALEURS = (("ACCOR", "AC"), ("AIR LIQUIDE", "AI"), ("AIRBUS", "AIR"), ("AXA", "CS"))
DEBUT, FIN = "2024-01-02", "2026-10-30"     # fenêtre figée : la vérité ne bouge pas quand le maître grandit
TP, SL, HORIZON = 0.04, 0.03, 20             # objectif et perte DIFFÉRENTS, pour qu'un échange des deux se voie
GRAINES_DU_HASARD = (1, 2, 3)
# V7 (RELU Cowork D-1) : sait l'avenir jusqu'à cette date, tire au sort ensuite. Choisie AVANT la frontière 70/30 lue
# le 10-11-2026 (2025-12-23), pour que la partie jamais vue soit tout entière du hasard.
SAIT_JUSQU_AU = "2025-10-31"
AUCUNE_ACTIVE = False   # à passer à True par le Chat quand la vente de l'agent A accepte l'horizon « aucune »

# LES SABOTAGES : (fichier, texte présent UNE fois, remplacement). Chacun retire ce qu'un cas teste.
SABOTAGES = {
    "S1_partie_jamais_vue_lue_a_l_envers": [(JUGE, '"au-dessus du" if b["wr"] > pm else "sous le"',
                                             '"au-dessus du" if b["wr"] < pm else "sous le"')],
    "S2_borne_basse_lue_a_l_envers": [(JUGE, '"encore au-dessus du point mort" if _bb > pm',
                                       '"encore au-dessus du point mort" if _bb < pm')],
    "S3_hasard_lu_a_l_envers": [(JUGE, '"au-dessus du" if _net > hz["gain_95pct"] else "sous le",',
                                 '"au-dessus du" if _net < hz["gain_95pct"] else "sous le",')],
    "S4_point_mort_a_zero": [(JUGE, "pm = J.point_mort_des_operations(tp, sl, ops, mod_pos, bareme)",
                              "pm = 0.0 * J.point_mort_des_operations(tp, sl, ops, mod_pos, bareme)")],
    "S5_les_fenetres_tiennent_toujours": [(MODULE, 'f["tient"] = f["au_pire"] > point_mort_pct',
                                           'f["tient"] = True')],
    "S6_borne_basse_egale_au_taux": [(MODULE, "    return 100.0 * (c - e)", "    return wr_pct")],
    "S7_jamais_vue_remplacee_par_l_apprentissage": [(JUGE, 'a, b = c["res_70"], c["res_30"]',
                                                     'a, b = c["res_70"], c["res_70"]')],
    "S8_gain_de_la_strategie_oublie": [(JUGE, '_net = sum(o["net"] for o in ops)', "_net = 0.0")],
    "S9_achat_le_jour_du_signal": [(JUGE, "j = rang[d_sig] + 1           #", "j = rang[d_sig]           #")],
    "S10_objectif_et_perte_echanges": [(JUGE, '_vente = _vendre(serie, j, {"tp": tp, "sl": sl, "horizon": h}, "vendre")',
                                        '_vente = _vendre(serie, j, {"tp": sl, "sl": tp, "horizon": h}, "vendre")')],
    # S11 (RELU Cowork D-1) : le sabotage COMBINÉ qui laissait V4-V6 verts ; il doit faire valider V7, la fausse.
    "S11_jamais_vue_borne_et_fenetres_toujours_bonnes": [
        (JUGE, '"au-dessus du" if b["wr"] > pm else "sous le"', '"au-dessus du" if True else "sous le"'),
        (JUGE, '"encore au-dessus du point mort" if _bb > pm', '"encore au-dessus du point mort" if True'),
        (MODULE, 'f["tient"] = f["au_pire"] > point_mort_pct', 'f["tient"] = True')],
}


def charger(chemin, nom):
    """Charge un programme Python par son chemin.

    ① RÔLE — Donner le module éprouvé, pris dans la copie (sabotée ou non) ou dans la racine. ② CONTEXTE D'APPEL —
    `cas`. ③ ENTRÉE — `chemin` du fichier, `nom` du module. ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — le
    module chargé. [rend: 1] ⑥ TRAITEMENT — `spec_from_file_location`, puis exécution. ⑦ UNITÉ — — ⑧ POURQUOI —
    charger par chemin garantit que c'est la copie qui est éprouvée, jamais un module déjà importé. ⑨ CE QUI CLOCHE —
    — ⑩ EFFET — exécute le haut du fichier. ⑪ TERMINAISON — rend la main ou lève ce que le fichier lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lire_les_lignes_du_maitre(racine):
    """Lit les quatre valeurs dans le fichier maître, directement par csv, sans le lecteur du juge.

    ① RÔLE — Fournir la vérité de terrain (R-732) : les séances telles qu'écrites dans le fichier. ② CONTEXTE D'APPEL
    — `cas`, une fois. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — le fichier maître porte les colonnes valeur,
    date, open, high, low, close, volume. ⑤ SORTIE — UNE valeur : {nom de valeur: [séances triées par date]}, bornées
    à [DEBUT, FIN]. [rend: 1] ⑥ TRAITEMENT — filtrer les quatre noms et la fenêtre, convertir en nombres, trier, refuser
    une date en double. ⑦ UNITÉ — euros par titre ; volume en titres. ⑧ POURQUOI — la fenêtre figée rend la vérité
    stable quand le maître grandit chaque soir ; une lecture indépendante du lecteur du juge permet au cas R1 de
    confronter le juge au fichier. LE SOULIGNÉ VAUT UNE ESPACE : relevé le 10-11-2026 (corrigé par le RELU Cowork, D-5), le
    maître écrit Air Liquide « AIR LIQUIDE » sur 644 lignes (643 google, 1 euronext) et « AIR_LIQUIDE » sur 86 (14
    euronext, 28 google, 44 abc, du 13-07 au 09-11-2026) ; onze valeurs portent ainsi deux graphies ; une date présente
    sous les deux noms lève. ⑨ CE QUI CLOCHE — un autre renommage dans le
    maître rend une série plus courte que celle du lecteur du juge, et les cas L_ rougissent. ⑩ EFFET — lit un fichier. ⑪ TERMINAISON — rend la main ou lève
    ValueError. [sort: non]
    """
    noms = {n for n, _ in VALEURS}
    series = {n: {} for n in noms}
    with open(os.path.join(racine, MAITRE), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            nom = r["valeur"].replace("_", " ")      # « AIR_LIQUIDE » (euronext) = « AIR LIQUIDE » (google)
            if nom in noms and DEBUT <= r["date"] <= FIN:
                if r["date"] in series[nom]:
                    raise ValueError("date en double dans le maître : %s %s" % (nom, r["date"]))
                series[nom][r["date"]] = {"date": r["date"], **{k: float(r[k]) for k in
                                                  ("open", "high", "low", "close", "volume")}}
    return {n: [s[d] for d in sorted(s)] for n, s in series.items()}


def issue_sure(serie, i, tp, sl, horizon):
    """Dit, sur les cours seuls, si un achat au lendemain de la séance i gagne ou perd SANS AMBIGUÏTÉ.

    ① RÔLE — Être la vérité connue, indépendante du juge et de sa vente. ② CONTEXTE D'APPEL — les fabriques de
    signaux (`signal_qui_sait`) et le cas R1. ③ ENTRÉE — `serie` : séances triées · `i` : rang du signal · `tp`, `sl` :
    fractions · `horizon` : séances, ou None pour « aucune » (jusqu'à la fin des données). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : +1 (l'objectif est touché, la perte jamais avant), -1 (la perte est touchée, l'objectif
    jamais avant), None (ambigu ou sans issue). [rend: 1] ⑥ TRAITEMENT — ① achat à l'ouverture de i+1 · ② la séance
    d'achat ne doit toucher aucune borne · ③ parcourir les séances suivantes jusqu'à l'avant-dernière de l'horizon :
    la première qui touche une borne décide, si elle n'en touche qu'une ; si elle touche les deux, None. ⑦ UNITÉ —
    fractions, séances. ⑧ POURQUOI — exiger une issue nette rend la vérité vraie QUELLE QUE SOIT la convention de la
    vente : séance d'achat comptée ou non dans l'horizon, ordre des bornes dans une même séance, sortie à l'ouverture
    en cas d'écart. ⑨ CE QUI CLOCHE — un achat gagnant net peut sortir AU-DESSUS de l'objectif (ouverture en écart) :
    le cas R1 l'accepte. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend toujours la main. [sort: non]
    """
    j = i + 1
    if j >= len(serie):
        return None
    pe = serie[j]["open"]
    haut, bas = pe * (1 + tp), pe * (1 - sl)
    if serie[j]["high"] >= haut or serie[j]["low"] <= bas:
        return None
    fin = len(serie) if horizon is None else min(len(serie), j + horizon - 1)
    for k in range(j + 1, fin):
        h, b = serie[k]["high"] >= haut, serie[k]["low"] <= bas
        if h and b:
            return None
        if h:
            return 1
        if b:
            return -1
    return None


def signal_qui_sait(sens, part_au_hasard=0.0, graine=0, horizon=HORIZON, un_sur=3, jusqu_au=None):
    """Fabrique une fonction de signal qui regarde l'avenir, avec une part de jours tirés au sort.

    ① RÔLE — Donner les stratégies à vérité connue. ② CONTEXTE D'APPEL — `strategies`. ③ ENTRÉE — `sens` : +1 (ne
    retenir que les gains sûrs), -1 (que les pertes sûres), 0 (aucun, pur hasard) · `part_au_hasard` : probabilité
    d'ajouter un jour quelconque · `graine` · `horizon` · `un_sur` : n'en garder qu'un sur `un_sur` · `jusqu_au` :
    date AAAA-MM-JJ après laquelle la stratégie ne SAIT plus rien et ne tire plus qu'au sort (None : jamais). ④ CONDITIONS
    D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : une fonction (série) → [{"i": rang}]. [rend: 1] ⑥ TRAITEMENT — pour chaque
    rang : garder un jour sur `un_sur` parmi ceux dont `issue_sure` vaut `sens` ; ajouter les jours tirés au sort par
    un générateur dont la graine dépend de `graine` et de la première date de la série. ⑦ UNITÉ — rangs. ⑧ POURQUOI —
    « un sur trois » espace les achats (moins de positions superposées) et allège le juge ; la graine en texte rend le
    tirage identique d'un lancement à l'autre (random.Random sur une chaîne, sans `hash`, qui varie). ⑨ CE QUI
    CLOCHE — `jouer` appelle cette fonction sur une série entière (aucune lecture, donc aucun morceau) : rangs et
    séries coïncident. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    def fonction(serie):
        hasard = random.Random("%s|%s|%s" % (graine, serie[0]["date"] if serie else "", len(serie)))
        pris, n = [], 0
        for i in range(len(serie) - 1):
            sait = jusqu_au is None or serie[i]["date"] <= jusqu_au
            ajout = part_au_hasard and hasard.random() < part_au_hasard and (jusqu_au is None or not sait)
            if sens and sait and issue_sure(serie, i, TP, SL, horizon) == sens:
                n += 1
                if n % un_sur == 0:
                    pris.append({"i": i})
                    continue
            if ajout:
                pris.append({"i": i})
        return pris
    return fonction


def strategies():
    """Rend les stratégies à vérité connue : (nom, fonction, horizon écrit, verdict attendu, contrôles en plus).

    ① RÔLE — La table des cas, en un seul endroit. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE —
    —. ⑤ SORTIE — UNE liste de quintuplets. [rend: 1] ⑥ TRAITEMENT — —. ⑦ UNITÉ — —. ⑧ POURQUOI — V1 gagne à coup sûr ;
    V2 a un vrai avantage dilué (deux tiers au moins de gains sûrs, le reste au hasard) ; V3 perd à coup sûr ; V4 à V6
    ne savent rien ; V7 sait l'avenir jusqu'au 31-10-2025 puis tire au sort — la stratégie FAUSSE À MARGE POSITIVE
    (surapprise), que seuls la jamais vue, sa borne basse et les fenêtres peuvent rejeter (RELU Cowork D-1) ; A1 et A2 rejouent V1 et V3 sans durée maximale. ⑨ CE QUI CLOCHE — voir ⑨ ② de l'en-tête pour
    V4-V6. ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    t = [("V1_gagne_a_coup_sur", signal_qui_sait(+1), str(HORIZON), True, "gagnante"),
         ("V2_avantage_dilue", signal_qui_sait(+1, part_au_hasard=0.30, graine=7, un_sur=2), str(HORIZON), True,
          "moderee"),
         ("V3_perd_a_coup_sur", signal_qui_sait(-1), str(HORIZON), False, "perdante")]
    t += [("V%d_pur_hasard_graine_%d" % (3 + g, g), signal_qui_sait(0, part_au_hasard=0.03, graine=g),
           str(HORIZON), False, "hasard") for g in GRAINES_DU_HASARD]
    t += [("V7_sait_avant_hasard_apres", signal_qui_sait(+1, part_au_hasard=0.10, graine=11, jusqu_au=SAIT_JUSQU_AU),
           str(HORIZON), False, "surapprise")]
    t += [("A1_gagne_sans_duree", signal_qui_sait(+1, horizon=None), "aucune", True, "gagnante"),
          ("A2_perd_sans_duree", signal_qui_sait(-1, horizon=None), "aucune", False, "perdante")]
    return t


MOTIFS = {
    "point_mort": re.compile(r"POINT MORT\s+([\d.]+) %\s+·\s+reussite ([\d.]+) %\s+·\s+marge ([+-][\d.]+) pts"),
    "frontiere": re.compile(r"COUPURE 70/30\s+frontiere (\d{4}-\d\d-\d\d) \. embargo (\d+) seances"),
    "jamais_vue": re.compile(r"JAMAIS VUE\s+(\d+) op \. ([\d.]+) %"),
    "verdict_jv": re.compile(r"verdict\s+(au-dessus du|sous le) point mort de"),
    "au_pire": re.compile(r"AU PIRE\s+([\d.]+) %\s+->\s+(encore au-dessus|SOUS)"),
    "fenetres": re.compile(r"(fenetres exploitables TIENNENT|fenetre\(s\) sur \d+ SOUS)"),
    "hasard": re.compile(r"la strategie rend ([+-]?[\d ]+) EUR -> (au-dessus du|sous le) 95e centile"),
}


def lire_le_jugement(texte):
    """Lit les verdicts affichés par `juger`.

    ① RÔLE — Transformer l'affichage du juge en mesures comparables à la vérité. ② CONTEXTE D'APPEL — `cas`.
    ③ ENTRÉE — le texte affiché. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : un dictionnaire ; une clé absente
    veut dire « ligne absente ». [rend: 1] ⑥ TRAITEMENT — chaque motif de `MOTIFS`, le premier trouvé (le hasard : tous,
    dans l'ordre action puis dates). ⑦ UNITÉ — pourcents, points, euros, dates. ⑧ POURQUOI — `juger` ne rend rien
    (son ⑨ ③) : l'affichage est sa seule sortie. ⑨ CE QUI CLOCHE — voir ⑨ ⑥ de l'en-tête. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    d = {}
    m = MOTIFS["point_mort"].search(texte)
    if m:
        d["point_mort"], d["reussite"], d["marge"] = float(m[1]), float(m[2]), float(m[3])
    m = MOTIFS["frontiere"].search(texte)
    if m:
        d["frontiere"] = m[1]
    m = MOTIFS["jamais_vue"].search(texte)
    if m:
        d["jv_n"], d["jv_taux"] = int(m[1]), float(m[2])
    m = MOTIFS["verdict_jv"].search(texte)
    if m:
        d["jv_au_dessus"] = m[1] == "au-dessus du"
    m = MOTIFS["au_pire"].search(texte)
    if m:
        d["au_pire"], d["au_pire_au_dessus"] = float(m[1]), m[2] == "encore au-dessus"
    m = MOTIFS["fenetres"].search(texte)
    if m:
        d["fenetres_tiennent"] = "TIENNENT" in m[1]
    h = MOTIFS["hasard"].findall(texte)
    if len(h) == 2:
        d["net_affiche"] = float(h[0][0].replace(" ", ""))
        d["bat_hasard_action"], d["bat_hasard_dates"] = (x[1] == "au-dessus du" for x in h)
    return d


def verdict_provisoire(d):
    """Compose le verdict provisoire « validée » à partir des lignes du juge (voir l'en-tête).

    ① RÔLE — Dire oui ou non, en attendant la grille de B. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — le dictionnaire de
    `lire_le_jugement`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : True, False, ou None si une ligne manque.
    [rend: 1] ⑥ TRAITEMENT — les cinq conditions de l'en-tête, toutes exigées. ⑦ UNITÉ — —. ⑧ POURQUOI — une
    stratégie fausse ne doit passer aucun filtre COMPLET ; une vraie doit les passer tous. ⑨ CE QUI CLOCHE — n'est pas
    la grille de B (seuil 0,00135, C7, C8). ⑩ EFFET — aucun. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    cles = ("marge", "jv_au_dessus", "au_pire_au_dessus", "fenetres_tiennent", "bat_hasard_action", "bat_hasard_dates")
    if any(k not in d for k in cles):
        return None
    return (d["marge"] > 0 and d["jv_au_dessus"] and d["au_pire_au_dessus"] and d["fenetres_tiennent"]
            and d["bat_hasard_action"] and d["bat_hasard_dates"])


def controles(nom, genre, attendu, d, ops, lendemain=None):
    """Rend la liste des contrôles d'un cas : (libellé, réussi, détail).

    ① RÔLE — Confronter chaque ligne du juge à la vérité connue. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — le nom, le
    genre (gagnante, moderee, perdante, hasard), le verdict attendu, les lignes lues, les opérations jouées.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE liste. [rend: 1] ⑥ TRAITEMENT — ① le verdict provisoire égale l'attendu ·
    ② la partie jamais vue ne compte que des opérations signalées après la frontière (contre S7) · ③ le gain total
    affiché égale la somme des opérations (contre S8) · ④ gagnante : marge, jamais vue, borne basse, fenêtres, hasard
    tous du bon côté ; perdante : tous du mauvais · ⑤ modérée : la borne basse est sous le taux (un taux entre 0 et
    100 % sur un nombre fini d'opérations a une borne basse strictement plus petite, contre S6). ⑦ UNITÉ — pourcents,
    euros. ⑧ POURQUOI — le verdict global seul laisse passer un juge qui se trompe sur une ligne sans changer le total.
    ⑨ CE QUI CLOCHE — la vérité des cas du hasard n'est exigée que sur le verdict global. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    r = []
    v = verdict_provisoire(d)
    r.append(("verdict provisoire %s" % ("VALIDÉE" if attendu else "NON validée"), v is attendu,
              "lu %r ; lignes lues : %s" % (v, sorted(d))))
    if "frontiere" in d and "jv_n" in d:
        apres = sum(1 for o in ops if o["date_signal"] > d["frontiere"])
        r.append(("jamais vue ⊂ après la frontière", d["jv_n"] <= apres, "%d op lues, %d après %s"
                  % (d["jv_n"], apres, d["frontiere"])))
    else:
        r.append(("jamais vue ⊂ après la frontière", False, "ligne absente"))
    total = sum(o["net"] for o in ops)
    r.append(("gain affiché = somme des opérations", abs(d.get("net_affiche", float("nan")) - total) <= 1.0,
              "affiché %s, somme %.0f" % (d.get("net_affiche"), total)))
    if genre in ("gagnante", "perdante"):
        bon = genre == "gagnante"
        for k in ("jv_au_dessus", "au_pire_au_dessus", "fenetres_tiennent", "bat_hasard_action", "bat_hasard_dates"):
            r.append(("%s %s" % (k, "oui" if bon else "non"), d.get(k) is bon, "lu %r" % d.get(k)))
        r.append(("marge %s" % ("> 0" if bon else "< 0"), "marge" in d and (d["marge"] > 0) is bon and d["marge"] != 0,
                  "lu %r" % d.get("marge")))
    if genre == "gagnante" and lendemain is not None:
        # D-3 (RELU Cowork) : S9 et S10 ne reposaient que sur R1 ; chaque opération de la gagnante est relue.
        mal = [o for o in ops if o["date_entree"] != lendemain.get((o["valeur"], o["date_signal"]))
               or o["px"] < o["pe"] * (1 + TP) - 1e-9]
        r.append(("achat au lendemain du signal, sortie au moins à l'objectif, toutes opérations", not mal,
                  "%d fautive(s) ; première %r" % (len(mal), mal[0] if mal else None)))
    if genre == "surapprise":
        r.append(("marge > 0 (la stratégie fausse paraît gagner)", d.get("marge", 0) > 0, "lu %r" % d.get("marge")))
        for k in ("au_pire_au_dessus", "fenetres_tiennent"):
            r.append(("%s non" % k, d.get(k) is False, "lu %r" % d.get(k)))
    if genre == "moderee":
        ok = "au_pire" in d and "jv_taux" in d and 0 < d["jv_taux"] < 100 and d["au_pire"] < d["jv_taux"]
        r.append(("borne basse < taux de la jamais vue", ok, "au pire %r, taux %r" % (d.get("au_pire"),
                                                                                       d.get("jv_taux"))))
    return r


def cas(copie, racine):
    """Joue tous les cas sur une copie du juge et rend leurs résultats.

    ① RÔLE — Le cœur de l'épreuve. ② CONTEXTE D'APPEL — le mode « --cas ». ③ ENTRÉE — le dossier de la copie, la
    racine. ④ CONDITIONS D'ENTRÉE — celles de l'en-tête. ⑤ SORTIE — UNE liste de (nom, état, détail), l'état valant
    « VERT », « ROUGE » ou « ATTENTE A ». [rend: 1] ⑥ TRAITEMENT — ① charger la copie du juge et du module de jugement,
    le module de positions et de statistiques de la racine · ② lire le maître deux fois : par csv (vérité) et par le
    lecteur du juge (`charger_cours`), et exiger qu'ils coïncident sur la fenêtre · ③ R1 · ④ pour chaque stratégie :
    `jouer` puis `juger`, affichage capturé, `controles`. ⑦ UNITÉ — —. ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE —
    voir l'en-tête. ⑩ EFFET — aucun fichier écrit. ⑪ TERMINAISON — rend la main ; une erreur dans un cas le rend
    ROUGE (ou ATTENTE A, voir l'en-tête). [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    sys.path.insert(0, os.path.join(copie, "programmes"))
    JU = charger(os.path.join(copie, JUGE), "juge_eprouve")
    J = charger(os.path.join(copie, MODULE), "jugement_eprouve")
    P = charger(os.path.join(racine, "programmes/MODULE_POSITIONS.py"), "positions")
    S = charger(sorted(glob.glob(os.path.join(racine, "programmes/MODULE_STATISTIQUES_*.py")))[-1], "statistiques")
    mnemo = JU.table_mnemoniques(JU.trouver(racine, "REFERENTIEL_VALEURS"))
    brutes = lire_les_lignes_du_maitre(racine)
    lu = JU.charger_cours(os.path.join(racine, MAITRE))
    res = []
    cours = {}
    for nom, m in VALEURS:
        cle = mnemo.get(m, JU.cle_valeur(m))
        serie = [b for b in lu.get(cle, []) if DEBUT <= b["date"] <= FIN]
        egal = len(serie) == len(brutes[nom]) > 400 and all(
            a["date"] == b["date"] and abs(a["open"] - b["open"]) < 1e-9 for a, b in zip(serie, brutes[nom]))
        res.append(("L_%s lecteur du juge = fichier maître" % m, "VERT" if egal else "ROUGE",
                    "%d séances lues, %d dans le fichier, clé %r" % (len(serie), len(brutes[nom]), cle)))
        cours[cle] = serie
    if any(e != "VERT" for _, e, _ in res):
        return res
    seances = {b["date"] for s in cours.values() for b in s}
    lendemain = {(v, s[k]["date"]): s[k + 1]["date"] for v, s in cours.items() for k in range(len(s) - 1)}
    aucune_active = AUCUNE_ACTIVE or "lire_horizon_ou_aucune" in open(os.path.join(copie, JUGE), encoding="utf-8").read()
    import COMMUN
    refus_attendu = lambda ex: isinstance(ex, TypeError) and ("NoneType" in str(ex)
                                                              or COMMUN.MESSAGE_DE_L_HORIZON_AUCUNE[:40] in str(ex))
    univers = ", ".join(m for _, m in VALEURS)
    base = {"id": "D-VERITE", "tp": "%g%%" % (100 * TP), "sl": "%g%%" % (100 * SL), "univers": univers,
            "entree": "DÉFAUT", "donnees_demandees": "cours", "periode": "%s..%s" % (DEBUT, FIN)}

    # R1 — UNE VRAIE LIGNE (R-732) : le premier gain sûr d'Accor, relu dans le fichier, doit être une opération gagnante
    # du juge, achetée à l'OUVERTURE DU LENDEMAIN telle qu'écrite dans le fichier, et sortie au moins à l'objectif.
    try:
        acc = brutes["ACCOR"]
        i = next(k for k in range(len(acc) - 1) if issue_sure(acc, k, TP, SL, HORIZON) == 1)
        sig = JU.SignalNomme(lambda s, _d=acc[i]["date"]: [{"i": k} for k, b in enumerate(s) if b["date"] == _d], {},
                             "épreuve D, R1")
        ops, _ = JU.jouer(dict(base, horizon=str(HORIZON), univers="AC"), cours, mnemo, sig, P)
        o = ops[0] if len(ops) == 1 else None
        ok = (o is not None and o["date_entree"] == acc[i + 1]["date"] and abs(o["pe"] - acc[i + 1]["open"]) < 1e-9
              and o["px"] >= o["pe"] * (1 + TP) - 1e-9 and o["net"] > 0)
        res.append(("R1 Accor, signal du %s, achat à l'ouverture du %s (%.2f dans le fichier) : gagnante" % (
            acc[i]["date"], acc[i + 1]["date"], acc[i + 1]["open"]), "VERT" if ok else "ROUGE", "opération %r" % o))
    except Exception as ex:
        res.append(("R1 une vraie ligne d'Accor", "ROUGE", "%s: %s" % (type(ex).__name__, ex)))

    for nom, fn, horizon, attendu, genre in strategies():
        fiche = dict(base, horizon=horizon)
        sig = JU.SignalNomme(fn, {}, "épreuve D, " + nom)
        try:
            ops, _ = JU.jouer(fiche, cours, mnemo, sig, P)
            tampon = io.StringIO()
            with contextlib.redirect_stdout(tampon):
                JU.juger(fiche, ops, cours, seances, J, S, P, mnemo, None, (sig,), None, None)
            d = lire_le_jugement(tampon.getvalue())
            for lib, ok, det in controles(nom, genre, attendu, d, ops, lendemain):
                res.append(("%s · %s" % (nom, lib), "VERT" if ok else "ROUGE", "%d op ; %s" % (len(ops), det)))
        except Exception as ex:
            etat = "ATTENTE A" if horizon == "aucune" and not aucune_active and refus_attendu(ex) else "ROUGE"
            res.append((nom, etat, "le juge refuse : %s: %s" % (type(ex).__name__, str(ex)[:160])))
    return res


def preparer(racine, sab):
    """Copie le juge et le module de jugement et y applique un sabotage.

    ① RÔLE — Donner à chaque sabotage sa copie. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine, le nom du sabotage
    ou « Z0 ». ④ CONDITIONS D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — le dossier de la copie.
    [rend: 1] ⑥ TRAITEMENT — copier, remplacer. ⑦ UNITÉ — —. ⑧ POURQUOI — une cible introuvable ne sabote rien : elle
    lève au lieu de passer pour un sabotage qui mord. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — crée un dossier temporaire.
    ⑪ TERMINAISON — rend la main ou lève LookupError. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="verite_%s_" % sab)
    os.makedirs(os.path.join(d, "programmes"))
    for f in (JUGE, MODULE):
        shutil.copy(os.path.join(racine, f), os.path.join(d, f))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            shutil.rmtree(d)
            raise LookupError("sabotage %s : le texte visé est présent %d fois dans %s" % (sab, t.count(a), f))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d


def main():
    """Programme principal : Z0, puis les sabotages demandés.

    ① RÔLE — Enchaîner l'épreuve. ② CONTEXTE D'APPEL — le lancement. ③ ENTRÉE — la ligne de commande (USAGE).
    ④ CONDITIONS D'ENTRÉE — voir l'en-tête. ⑤ SORTIE — le code de sortie. [rend: 1] ⑥ TRAITEMENT — voir l'en-tête.
    ⑦ UNITÉ — —. ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE — un sabotage « mord » dès qu'UN cas rougit, même si
    ce n'est pas celui qu'il vise ; le relevé nomme les cas rougis pour qu'on le voie. ⑩ EFFET — dossiers temporaires,
    effacés. ⑪ TERMINAISON — chaque relance est bornée à 900 s ; rend la main. [sort: non]
    """
    if len(sys.argv) > 3 and sys.argv[1] == "--cas":
        try:
            r = cas(sys.argv[2], sys.argv[3])
        except Exception as ex:
            print("ARRET : %s: %s" % (type(ex).__name__, ex))
            return 2
        for nom, e, det in r:
            print("  %-9s %s — %s" % (e, nom, det))
        print("  %d vert(s), %d rouge(s), %d en attente de l'agent A" % tuple(
            sum(1 for _, e, _ in r if e == x) for x in ("VERT", "ROUGE", "ATTENTE A")))
        return 0 if all(e != "ROUGE" for _, e, _ in r) else 1
    if len(sys.argv) < 2:
        print(__doc__.split("\n\n")[0])
        return 2
    racine = os.path.abspath(sys.argv[1])
    choix = sys.argv[2] if len(sys.argv) > 2 else None
    if choix not in (None, "--saboter") and choix not in SABOTAGES:
        print("ARRET : sabotage inconnu %r (connus : %s)" % (choix, ", ".join(SABOTAGES)))
        return 2
    code = 0
    for sab in ["Z0"] + (list(SABOTAGES) if choix == "--saboter" else ([choix] if choix else [])):
        try:
            d = preparer(racine, sab)
        except LookupError as ex:
            print("ARRET : %s" % ex)
            return 2
        try:
            p = subprocess.run([sys.executable, "-B", ICI, "--cas", d, racine], capture_output=True, text=True,
                               timeout=900)
            sortie, rc = p.stdout, p.returncode
        except subprocess.TimeoutExpired:
            sortie, rc = "  ROUGE     délai de 900 s dépassé", 1
        finally:
            shutil.rmtree(d, ignore_errors=True)
        rouges = [l.strip()[10:].split(" — ")[0] for l in sortie.splitlines() if l.strip().startswith("ROUGE")]
        if sab == "Z0":
            print("Z0 — le dépôt tel quel : %s" % ("VERT" if rc == 0 else "ROUGE"))
            print(sortie.rstrip())
            if rc == 2:
                return 2
            if rc != 0:
                code = 1
        else:
            mord = rc == 1 and bool(rouges)
            print("%s %s — %d cas rougis : %s" % ("MORD       " if mord else "NE MORD PAS", sab, len(rouges),
                                                 " | ".join(rouges[:3]) or sortie.strip()[-200:]))
            if not mord:
                code = 1
    print("CODE %d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())
