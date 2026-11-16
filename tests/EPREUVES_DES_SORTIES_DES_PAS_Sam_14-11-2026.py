#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DES SORTIES DES PAS — Sam 14-11-2026 (Paris) — chaque sortie de pas lue par le circuit du soir est écrite.

Simulation uniquement — aucun ordre réel.

① RÔLE — Prouver, par une PROPRIÉTÉ du fichier du circuit `.github/workflows/collecte_abc.yml`, que chaque
  `steps.<X>.outputs.<Y>` qu'il lit désigne un pas d'`id` <X> qui ÉCRIT <Y> dans `$GITHUB_OUTPUT`, et réciproquement
  que chaque sortie écrite est lue quelque part. Une sortie lue sous un nom que personne n'écrit vaut toujours la
  chaîne vide : le pas de fin qui en dépend ne rougit jamais, et le soir reste VERT en silence. Prouver aussi, par
  `tests/GARDE_DU_PAS_ROUGE.garde_du_pas_rouge`, que le pas de fin « Rougir si une anomalie d identite a ete dite »
  est bien formé pour la sortie `anomalies_d_identite` (aucune autre épreuve automatique ne le faisait : relecteur
  QE2 du 16-11-2026, D-4).
② CONTEXTE D APPEL — À la main avant toute livraison qui touche le fichier du circuit ou un programme qui écrit une
  sortie de pas ; `--saboter` joue chaque sabotage, qui doit faire rougir l'épreuve POUR SA RAISON.
③ ENTRÉE — `sys.argv[1]` : la racine du dépôt ; `--saboter` facultatif.
④ CONDITIONS D ENTRÉE — Le fichier du circuit sous la racine ; les programmes qu'il appelle sous `programmes/` ;
  `tests/GARDE_DU_PAS_ROUGE.py` sous la racine ; le module `yaml` de Python.
⑤ SORTIE — UNE valeur : le code de sortie — 0 si Z0 est vert et, avec `--saboter`, si chaque sabotage produit
  EXACTEMENT les rouges qu'il déclare ; 1 si une attente tombe, dont Z0 rouge (les sabotages sortent alors
  « NON JUGÉ ») ; 2 si un sabotage ne s'applique pas ou si un fichier ne se lit pas (R-734).
  [rend: 1] Une ligne « == » par jeu, puis le détail des rouges.
⑥ TRAITEMENT — ① lire le texte du circuit et des programmes (saboté, en mémoire seulement) · ② relever TOUTES les
  lectures `steps.<X>.outputs.<Y>` du texte entier · ③ pour chaque pas, relever ce qu'il écrit : une ligne de son
  `run` qui contient `<Y>=` et `$GITHUB_OUTPUT` (`echo "a_part=1" >> "$GITHUB_OUTPUT"`), ou, dans un programme
  `programmes/<P>.py` que son `run` nomme et qui contient `GITHUB_OUTPUT`, une CONSTANTE CHAÎNE lue par l'arbre
  syntaxique (`ast`, docstrings exclues) qui, découpée sur ses retours à la ligne, a un morceau commençant par `<Y>=`
  (« positions_signalees=%d » et « \nsignaux_mis_a_part=%d » dans TENIR_LES_POSITIONS) · ④ rouge pour toute lecture
  sans pas <X>, toute lecture que <X> n'écrit pas, toute sortie écrite que rien ne lit, et chaque manque de la garde
  du pas rouge sur `anomalies_d_identite` · ⑤ avec `--saboter` : Z0 d'abord ; s'il n'est pas vert, aucun sabotage
  n'est jugé (« NON JUGÉ ») ; sinon chaque sabotage est joué et comparé à SA liste de rouges déclarée ; enfin S9
  rejoue le tout avec un Z0 rouge exprès et exige que chaque sabotage sorte « NON JUGÉ ».
⑦ UNITÉ — —
⑧ POURQUOI — Superviseurs R-759 du 14-11-2026 (R-207bis, D3 ; QE2 K, K-1) : un pas de fin clé sur une sortie de pas
  ne rougit que si le nom lu est celui que le programme écrit ; une faute de frappe d'un côté rend le soir vert, et
  les épreuves qui ne jouent que le programme restent vertes. Superviseur R-759 du 16-11-2026 sur N-18
  (etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/rapports_du_11-11-2026/SUPERVISEUR_N18_Lun_16-11-2026.md), verdict
  « rustine, à reprendre » pour l'élargissement du motif : l'ancien motif sur le TEXTE (un guillemet juste avant le
  nom) ne voyait pas `"\nsignaux_mis_a_part=%d"` (Z0 rouge en permanence) et prenait un COMMENTAIRE pour une
  écriture (vert en silence, mesuré) ; l'arbre décode `\n`, ignore les commentaires et lit les morceaux fixes des
  f-chaînes — une propriété, pas une liste de préfixes. Et `bon = bool(rg)` comptait le rouge d'un Z0 rouge comme
  la morsure de chaque sabotage : l'épreuve ne prouvait plus rien. Calibrage de l'arbre (superviseur, 16-11-2026) :
  TENIR_LES_POSITIONS → positions_signalees, signaux_mis_a_part ; TENIR_L_HISTORIQUE → anomalies_d_identite ;
  DETECTER_LES_SIGNAUX_GITHUB → garde ; rien en trop.
⑨ CE QUI CLOCHE — Un programme qui écrit une sortie par un module qu'il importe n'est pas vu : sa lecture rougit
  (fausse alarme, du côté sûr). · Une constante chaîne « nom=… » sans rapport avec la sortie, dans un programme qui
  écrit une sortie, serait prise pour une sortie et rougirait comme « écrite, jamais lue » (aucune aujourd'hui,
  calibrage ci-dessus). · Un nom fabriqué à l'exécution (`"%s=%d" % (nom, n)`) n'est pas vu : sa lecture rougit (du
  côté sûr). · L'exclusion des docstrings n'a pas de sabotage qui mord : aucune docstring d'un programme écrivain
  n'a aujourd'hui de ligne `nom=`. · Les rouges attendus de la garde (S2, S5, S11) recopient ses messages : si la
  garde change de mots, ces sabotages sortent « NE MORD PAS POUR SA RAISON » (rouge, du côté sûr) et leur
  déclaration est à refaire. · La garde n'est jouée que pour `anomalies_d_identite` ; les deux sorties du teneur
  sont gardées par V10f et T10. · GitHub Actions n'est pas lancé : la propriété est lue dans les fichiers.
⑩ EFFET — Lit des fichiers ; n'écrit rien.
⑪ TERMINAISON — Rend la main.
  [sort: oui]
"""
import ast, importlib.util, os, re, sys
import yaml

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
CIRCUIT = ".github/workflows/collecte_abc.yml"
TENEUR = "programmes/TENIR_LES_POSITIONS.py"
VERSEUR = "programmes/TENIR_L_HISTORIQUE.py"
DETECTEUR = "programmes/DETECTER_LES_SIGNAUX_GITHUB.py"
LECTURE = re.compile(r"steps\.([A-Za-z0-9_-]+)\.outputs\.([A-Za-z0-9_-]+)")
DEBUT_DE_LIGNE = re.compile(r"([a-z][a-z0-9_]*)=")
# L'ANCIEN motif, gardé SEULEMENT pour le sabotage S8 de l'épreuve elle-même : il doit faire rougir Z0.
LITTERAL_ANCIEN = re.compile(r"[\"']([a-z][a-z0-9_]*)=(?:%d|%s|[\"'])")


def noms_ecrits_par_l_arbre(source):
    """Rend l'ensemble des noms `<Y>` qu'un programme écrit comme ligne `<Y>=…`, lus dans ses constantes chaînes.

    ① RÔLE — Le lecteur des écritures d'un programme (réparation N-18 retenue par le superviseur R-759 du 16-11-2026).
    ② CONTEXTE D APPEL — `jeu`. ③ ENTRÉE — `source` : le texte d'un programme Python. ④ CONDITIONS D ENTRÉE — Le texte
    est du Python valide. ⑤ SORTIE — UNE valeur : un ensemble de noms. [rend: 1] ⑥ TRAITEMENT — ① lire l'arbre
    syntaxique · ② écarter les docstrings (constante chaîne seule en tête de module, classe ou fonction) · ③ pour
    chaque autre constante chaîne (y compris les morceaux fixes d'une f-chaîne), la découper sur ses retours à la
    ligne et garder le nom de chaque morceau qui commence par `nom=`. ⑦ UNITÉ — —. ⑧ POURQUOI — Voir ⑧ du module :
    l'arbre décode `\n` et ignore les commentaires ; les docstrings sont écartées pour qu'un texte explicatif ne
    passe pas pour une écriture. ⑨ CE QUI CLOCHE — Voir ⑨ du module. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ;
    lève SyntaxError si le texte n'est pas du Python. [sort: non]
    """
    arbre = ast.parse(source)
    docstrings = set()
    for n in ast.walk(arbre):
        if (isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.body
                and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)
                and isinstance(n.body[0].value.value, str)):
            docstrings.add(id(n.body[0].value))
    noms = set()
    for n in ast.walk(arbre):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docstrings:
            for morceau in n.value.split("\n"):
                m = DEBUT_DE_LIGNE.match(morceau)
                if m:
                    noms.add(m.group(1))
    return noms


def noms_ecrits_par_l_ancien_motif(source):
    """Rend les noms que voyait l'ANCIEN motif sur le texte (guillemet juste avant le nom) — pour S8 seulement.

    ① RÔLE — Rejouer l'épreuve d'avant N-18 pour prouver que la réparation est tenue. ② CONTEXTE D APPEL — `juger`,
    sabotage S8. ③ ENTRÉE — `source` : un texte. ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : un ensemble.
    [rend: 1] ⑥ TRAITEMENT — le motif `LITTERAL_ANCIEN`. ⑦ UNITÉ — —. ⑧ POURQUOI — S8 du superviseur R-759 du
    16-11-2026. ⑨ CE QUI CLOCHE — C'est le défaut N-18 lui-même. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    return set(LITTERAL_ANCIEN.findall(source))


def charger_la_garde():
    """Rend le module `tests/GARDE_DU_PAS_ROUGE.py` de la racine, chargé par chemin.

    ① RÔLE — Une seule garde des pas rouges (R-708 : deux implémentations d'une même chose divergent toujours).
    ② CONTEXTE D APPEL — `jeu`. ③ ENTRÉE — —. ④ CONDITIONS D ENTRÉE — Le fichier existe sous la racine.
    ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — `importlib` par chemin. ⑦ UNITÉ — —.
    ⑧ POURQUOI — Éprouver la garde de la racine donnée, pas une copie prise ailleurs. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Exécute le module (aucun effet au chargement). ⑪ TERMINAISON — Rend la main ou lève OSError.
    [sort: non]
    """
    chemin = os.path.join(DEPOT, "tests", "GARDE_DU_PAS_ROUGE.py")
    if not os.path.isfile(chemin):
        raise OSError(f"{chemin} est absent")
    spec = importlib.util.spec_from_file_location("garde_du_pas_rouge_des_sorties", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lire(chemin, sab):
    """Rend le texte d'un fichier de la racine, saboté en mémoire si le jeu le demande.

    ① RÔLE — La seule lecture de fichier de l'épreuve. ② CONTEXTE D APPEL — `jeu`. ③ ENTRÉE — `chemin` : relatif à la
    racine ; `sab` : la liste des remplacements du jeu. ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : le texte,
    ou None si le fichier manque ; lève ValueError si l'ancre d'un remplacement du jeu sur ce fichier est absente (le
    sabotage ne s'applique pas). [rend: 1] ⑥ TRAITEMENT — lire, remplacer (toutes les occurrences : un nom se change
    partout d'un côté). ⑦ UNITÉ — —. ⑧ POURQUOI — Ne jamais écrire sous la racine. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Lit un fichier. ⑪ TERMINAISON — Rend la main ou lève. [sort: non]
    """
    p = os.path.join(DEPOT, chemin)
    if not os.path.isfile(p):
        return None
    t = open(p, encoding="utf-8").read()
    for f, a, b in sab:
        if f == chemin:
            if a not in t:
                raise ValueError(f"ancre absente dans {chemin} : {a[:60]!r}")
            t = t.replace(a, b)
    return t


def jeu(sab, lecteur):
    """Rend la liste des rouges de la propriété « lu ⇔ écrit » et de la garde du pas rouge, saboté ou non.

    ① RÔLE — Un jeu. ② CONTEXTE D APPEL — `juger`. ③ ENTRÉE — `sab` : une liste de remplacements ; `lecteur` : la
    fonction qui lit les écritures d'un programme (l'arbre ; l'ancien motif pour S8 seulement).
    ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : la liste des rouges (textes). [rend: 1]
    ⑥ TRAITEMENT — voir ⑥ du module. ⑦ UNITÉ — —. ⑧ POURQUOI — Voir ⑧ du module. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main, ou lève ValueError (sabotage inapplicable, circuit
    absent), SyntaxError (programme saboté illisible), OSError ou yaml.YAMLError. [sort: non]
    """
    t = lire(CIRCUIT, sab)
    if t is None:
        raise ValueError(f"{CIRCUIT} est absent")
    pas = [p for job in yaml.safe_load(t)["jobs"].values() for p in job.get("steps", [])]
    lues = set(LECTURE.findall(t))
    ecrites = set()
    for p in pas:
        x, run = p.get("id"), str(p.get("run") or "")
        if not x:
            continue
        for ligne in run.splitlines():
            if "GITHUB_OUTPUT" in ligne:
                ecrites |= {(x, y) for y in re.findall(r"([A-Za-z0-9_-]+)=", ligne)}
        for prog in sorted(set(re.findall(r"programmes/([A-Za-z0-9_]+\.py)", run))):
            s = lire("programmes/" + prog, sab)
            if s and "GITHUB_OUTPUT" in s:
                ecrites |= {(x, y) for y in lecteur(s)}
    ids = {p.get("id") for p in pas}
    rouges = [f"lu, aucun pas d'id « {x} » : steps.{x}.outputs.{y}" for x, y in sorted(lues) if x not in ids]
    rouges += [f"lu, jamais écrit par le pas « {x} » : steps.{x}.outputs.{y}" for x, y in sorted(lues - ecrites)
               if x in ids]
    rouges += [f"écrit par le pas « {x} », jamais lu : {y}" for x, y in sorted(ecrites - lues)]
    rouges += [f"garde du pas rouge, anomalies_d_identite : {m}"
               for m in charger_la_garde().garde_du_pas_rouge(t, "anomalies_d_identite", VERSEUR)]
    return rouges


_MIS_A_PART_JAMAIS_ECRIT = ("lu, jamais écrit par le pas « tenir_les_positions » : "
                            "steps.tenir_les_positions.outputs.signaux_mis_a_part")
_GARDE_SANS_PAS_ROUGE = ("garde du pas rouge, anomalies_d_identite : 0 pas rouge(s) pour « anomalies_d_identite » "
                         "(if qui lit la sortie et run qui finit par « exit 1 ») : un seul attendu")
_FIN_DU_PAS_ROUGE_ANOMALIE = "corriger la ligne de la societe nommee)\"\n          exit 1\n"

# Chaque sabotage : (remplacements, rouges attendus EXACTEMENT, lecteur des programmes). Un sabotage « mord » si et
# seulement si l'épreuve rend exactement ses rouges déclarés — ni le rouge d'un Z0 rouge, ni un autre en plus.
SABOTAGES = {
    # le nom change d'un seul côté : le soir serait vert en silence
    "S1_nom_change_dans_le_versement_seul": (
        [(VERSEUR, '"anomalies_d_identite=%d"', '"anomalie_d_identite=%d"')],
        ["lu, jamais écrit par le pas « versement » : steps.versement.outputs.anomalies_d_identite",
         "écrit par le pas « versement », jamais lu : anomalie_d_identite"], noms_ecrits_par_l_arbre),
    "S2_nom_change_dans_le_circuit_seul": (
        [(CIRCUIT, "outputs.anomalies_d_identite", "outputs.anomalie_d_identite")],
        ["lu, jamais écrit par le pas « versement » : steps.versement.outputs.anomalie_d_identite",
         "écrit par le pas « versement », jamais lu : anomalies_d_identite", _GARDE_SANS_PAS_ROUGE],
        noms_ecrits_par_l_arbre),
    "S3_nom_change_dans_le_teneur_seul": (
        [(TENEUR, '"positions_signalees=%d"', '"positions_signalee=%d"')],
        ["lu, jamais écrit par le pas « tenir_les_positions » : steps.tenir_les_positions.outputs.positions_signalees",
         "écrit par le pas « tenir_les_positions », jamais lu : positions_signalee"], noms_ecrits_par_l_arbre),
    "S4_sortie_du_shell_tue": (
        [(CIRCUIT, '            echo "a_part=1" >> "$GITHUB_OUTPUT"\n', "")],
        ["lu, jamais écrit par le pas « versement » : steps.versement.outputs.a_part"], noms_ecrits_par_l_arbre),
    "S5_pas_renomme": (
        [(CIRCUIT, "        id: versement\n", "        id: versement_du_soir\n")],
        ["lu, aucun pas d'id « versement » : steps.versement.outputs.a_part",
         "lu, aucun pas d'id « versement » : steps.versement.outputs.anomalies_d_identite",
         "écrit par le pas « versement_du_soir », jamais lu : a_part",
         "écrit par le pas « versement_du_soir », jamais lu : anomalies_d_identite",
         "garde du pas rouge, anomalies_d_identite : 0 pas portent l'id « versement » lu par le pas rouge : un seul "
         "attendu"], noms_ecrits_par_l_arbre),
    # N-18 (superviseur R-759 du 16-11-2026) : le retour à la ligne perdu — pour GitHub, la valeur de
    # positions_signalees deviendrait « 0 signaux_mis_a_part=0 », et signaux_mis_a_part ne serait jamais écrite.
    "S6_retour_a_la_ligne_perdu_dans_le_teneur": (
        [(TENEUR, '"\\nsignaux_mis_a_part=%d"', '" signaux_mis_a_part=%d"')],
        [_MIS_A_PART_JAMAIS_ECRIT], noms_ecrits_par_l_arbre),
    # N-18 § 2 : l'écriture retirée, le nom laissé dans un COMMENTAIRE — l'ancien motif restait VERT ici.
    "S7_ecriture_retiree_nom_en_commentaire": (
        [(TENEUR, '    _ligne_du_pas += "\\nsignaux_mis_a_part=%d" % _n_mis_a_part\n',
          '    # ancien : "signaux_mis_a_part=%d"\n')],
        [_MIS_A_PART_JAMAIS_ECRIT], noms_ecrits_par_l_arbre),
    # Sabotage de l'épreuve elle-même : l'ancien motif « guillemet avant le nom » remis — la pointe doit rougir.
    "S8_ancien_motif_remis_dans_l_epreuve": ([], [_MIS_A_PART_JAMAIS_ECRIT], noms_ecrits_par_l_ancien_motif),
    # Le troisième écrivain, qu'aucune épreuve ne sabotait.
    "S10_nom_change_dans_le_detecteur_seul": (
        [(DETECTEUR, '"garde="', '"gard="')],
        ["lu, jamais écrit par le pas « detecter_les_signaux_du_jour_le_calcul » : "
         "steps.detecter_les_signaux_du_jour_le_calcul.outputs.garde",
         "écrit par le pas « detecter_les_signaux_du_jour_le_calcul », jamais lu : gard"], noms_ecrits_par_l_arbre),
    # D-4 du relecteur QE2 : le pas rouge de l'anomalie d'identité finit en « exit 0 » — seule la garde le voit.
    "S11_pas_rouge_de_l_anomalie_en_exit_0": (
        [(CIRCUIT, _FIN_DU_PAS_ROUGE_ANOMALIE, _FIN_DU_PAS_ROUGE_ANOMALIE.replace("exit 1", "exit 0"))],
        [_GARDE_SANS_PAS_ROUGE], noms_ecrits_par_l_arbre),
}
_ERREURS = (ValueError, OSError, SyntaxError, yaml.YAMLError)


def juger(fond, noms):
    """Joue Z0 sur `fond`, puis, SEULEMENT si Z0 est vert, chaque sabotage nommé ; rend les verdicts.

    ① RÔLE — Faire de Z0 vert une CONDITION (superviseur R-759 du 16-11-2026). ② CONTEXTE D APPEL — Le programme
    principal ; S9 (avec un fond qui rend Z0 rouge exprès). ③ ENTRÉE — `fond` : remplacements joués sous chaque jeu
    (vide en temps normal) ; `noms` : les sabotages à juger. ④ CONDITIONS D ENTRÉE — —. ⑤ SORTIE — UNE valeur : la
    liste des (nom, statut, rouges) ; statut parmi « vert », « ROUGE » (Z0), « mord », « NE MORD PAS POUR SA RAISON »,
    « NON JUGÉ », « INAPPLICABLE ». [rend: 1] ⑥ TRAITEMENT — Z0 ; si Z0 n'est pas vert, chaque sabotage sort
    « NON JUGÉ » sans être joué ; sinon chaque sabotage mord si ses rouges sont EXACTEMENT ceux qu'il déclare.
    ⑦ UNITÉ — —. ⑧ POURQUOI — `bon = bool(rg)` comptait le rouge d'un Z0 rouge pour la morsure de chaque sabotage.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        rz = jeu(fond, noms_ecrits_par_l_arbre)
    except _ERREURS as e:
        return [("Z0", "INAPPLICABLE", [f"{type(e).__name__} : {e}"])] + [(n, "NON JUGÉ", []) for n in noms]
    verdicts = [("Z0", "vert" if rz == [] else "ROUGE", rz)]
    for nom in noms:
        sab, attendus, lecteur = SABOTAGES[nom]
        if rz != []:
            verdicts.append((nom, "NON JUGÉ", []))
            continue
        try:
            rg = jeu(fond + sab, lecteur)
        except _ERREURS as e:
            verdicts.append((nom, "INAPPLICABLE", [f"{type(e).__name__} : {e}"]))
            continue
        verdicts.append((nom, "mord" if sorted(rg) == sorted(attendus) else "NE MORD PAS POUR SA RAISON", rg))
    return verdicts


_faute = ""
_saboter = "--saboter" in sys.argv
_verdicts = juger([], list(SABOTAGES) if _saboter else [])
for nom, statut, rg in _verdicts:
    bon = statut in ("vert", "mord")
    print(f"== {nom} : {statut}" + ("" if bon or statut == "NON JUGÉ" else "  <-- ATTENDU "
                                     + ("VERT" if nom == "Z0" else "SES ROUGES DÉCLARÉS")))
    for r in rg:
        print("     " + r)
    if statut == "INAPPLICABLE":
        _faute = "2"
    elif not bon and not _faute:
        _faute = "1"
if _verdicts[0][1] != "vert" and _saboter:
    print("   Z0 n'est pas vert : sabotages NON JUGÉS.")
if _saboter and _verdicts[0][1] == "vert":
    # S9 : Z0 rendu rouge exprès (S2 joué en fond) — chaque sabotage doit sortir « NON JUGÉ », aucun « mord ».
    _s2 = SABOTAGES["S2_nom_change_dans_le_circuit_seul"]
    _v9 = juger(_s2[0], list(SABOTAGES))
    _z0_rouge_pour_s2 = _v9[0][1] == "ROUGE" and sorted(_v9[0][2]) == sorted(_s2[1])
    _non_juges = sum(s == "NON JUGÉ" for _n, s, _r in _v9[1:])
    _bon9 = _z0_rouge_pour_s2 and _non_juges == len(SABOTAGES) == len(_v9) - 1
    print("== S9_z0_rouge_expres_les_autres_non_juges : " + ("mord" if _bon9 else "NE MORD PAS POUR SA RAISON")
          + f" (Z0 rouge pour la raison de S2 : {_z0_rouge_pour_s2} ; {_non_juges}/{len(SABOTAGES)} NON JUGÉ)")
    if not _bon9 and not _faute:
        _faute = "1"
print("VERDICT :", "tout est conforme" if not _faute else f"NON CONFORME (code {_faute})")
sys.exit(int(_faute) if _faute else 0)
