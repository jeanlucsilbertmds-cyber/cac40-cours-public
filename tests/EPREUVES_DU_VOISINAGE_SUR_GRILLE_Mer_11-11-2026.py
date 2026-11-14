#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES DU VOISINAGE SUR GRILLE — plan V7, bloc 5l geste ⑥, Mer 11-11-2026, tour 3 du Jeu 12-11-2026 (Paris).
Simulation uniquement.

USAGE
    python3 -B tests/EPREUVES_DU_VOISINAGE_SUR_GRILLE_Mer_11-11-2026.py <racine>               # les épreuves
    python3 -B tests/EPREUVES_DU_VOISINAGE_SUR_GRILLE_Mer_11-11-2026.py <racine> --sabotages   # et chaque sabotage
    python3 -B tests/EPREUVES_DU_VOISINAGE_SUR_GRILLE_Mer_11-11-2026.py <racine> --un-sabotage=S11_reglages_croises

① RÔLE — Prouver que le drapeau « voisinage » du juge suit R-505 ⑩ (« les 26 voisins à ±10 % de chaque réglage
  doivent tous gagner ») sans aucun hasard : les voisins viennent de `voisins` (`programmes/COMMUN.py`, la même
  fonction que la moulinette, R-708), par pas réguliers de ±10 % de chaque réglage, croisés ; les réglages se lisent
  dans `donnees/combinatoires/VOISINAGE_DU_JUGE.csv` ; un seul voisin perdant lève le DRAPEAU ; chaque voisin joué
  est compté ; la durée s'arrondit par une règle écrite et les voisins confondus sont dits.
② CONTEXTE D'APPEL — À la main, par l'auteur, son relecteur et Cowork ; par `programmes/CERTIFIER_LA_VERSION.py`,
  qui lance chaque épreuve de `tests/` depuis la racine d'une copie, la racine en argument.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ; option « --sabotages », ou « --un-sabotage=NOM » (répétable).
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/` (juge, module de statistiques, PREPARER, COMMUN), le registre des
  stratégies et son référentiel, `donnees/combinatoires/VOISINAGE.csv` et `VOISINAGE_DU_JUGE.csv`, les cours.
⑤ SORTIE — Un affichage (une ligne par épreuve, puis une par sabotage) et un code de sortie : 0 si tout passe et
  si chaque sabotage joué mord ; 1 sinon ; 2 si la racine est inutilisable (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① E1 à E5 : la grille sur de vraies fiches du registre · ② E6 : la lecture des réglages et ses
  refus · ③ E7 : le calcul du drapeau avec un faux rejeu · ④ E8 : le vrai juge sur C5E10-QA-V1 · ⑤ E9 : le vrai
  juge sur une racine jetable dont le fichier de réglages est changé · ⑥ E10 : le vrai juge sans ce fichier ·
  ⑦ E11 : l'arrondi de la durée et les voisins confondus · ⑧ avec « --sabotages » : fabriquer une racine jetable
  par sabotage (liens vers le dépôt, `programmes/` copié), y réécrire UN endroit, y rejouer ces épreuves, exiger le
  code 1 ET l'épreuve visée en échec.
⑦ UNITÉ — Objectif et perte acceptée en POURCENTS dans la grille, en FRACTIONS dans le juge ; durées en séances ;
  gains en euros.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction (instructions du projet, §7) ; R-731 exige
  des cas venant de vraies lignes de fichier (R-732). Chaque sabotage neutralise UNE condition du code.
⑨ CE QUI CLOCHE — ① E8 fige les gains du voisinage de C5E10-QA-V1 (voisins +43 335 à +55 793 €, centre +53 944 €,
  mesurés le 12-11-2026 sur 2024-01-02 → 2026-07-10) : une correction des cours de 2024-2026 le fera rougir, c'est
  voulu. ② Le registre des essais n'existe pas : E7 n'éprouve `inscrire` qu'avec une fonction de l'épreuve.
  ③ Aucune épreuve ne fait tourner le juge sur une fiche dont la période touche 2000-2023.
⑩ EFFET — Crée et efface des dossiers temporaires `/tmp/voisinage_*` ; lance `python3`. N'écrit rien sous la racine.
⑪ TERMINAISON — Sort du programme. Chaque sous-processus a un délai de 300 s : aucun appel qui ne revienne pas.
  [sort: oui]
"""
import importlib.util
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ICI = os.path.abspath(__file__)
PREP = os.path.join("programmes", "PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py")
COMM = os.path.join("programmes", "COMMUN.py")
STAT = os.path.join("programmes", "MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py")
JUGE = os.path.join("programmes", "JUGE_DES_STRATEGIES.py")
REGLAGES = os.path.join("donnees", "combinatoires", "VOISINAGE_DU_JUGE.csv")
GRILLE = os.path.join("donnees", "combinatoires", "VOISINAGE.csv")
DELAI = 300

# Chaque sabotage : (nom, fichier, texte exact à remplacer, remplacement, épreuve qui doit rougir). Chacun neutralise
# UNE condition du code. Tour 3 (12-11-2026) : S1, S4, S5, S8, S14 réécrits pour le critère de R-505 ⑩ ; S15 à S20
# ajoutés.
SABOTAGES = [
    ("S1_amplitude_ignoree", COMM, "        pas = v * amplitude_relative / 100\n",
     "        pas = amplitude_relative / 100\n", "E1"),
    ("S2_centre_garde", COMM, "            if jeu != base and jeu not in jeux:\n                jeux.append(jeu)\n    else:",
     "            if jeu not in jeux:\n                jeux.append(jeu)\n    else:", "E1"),
    ("S3_un_a_la_fois_croise", COMM, '    if croisement == "produit":\n        combinaisons',
     '    if croisement in CROISEMENTS_ADMIS:\n        combinaisons', "E3"),
    ("S4_seuil_non_strict", STAT, 'if not d["net"] > gain_net_de_chaque_voisin_doit_depasser]',
     'if not d["net"] >= gain_net_de_chaque_voisin_doit_depasser]', "E7"),
    ("S5_passe_sans_voisin", STAT, '    if not details:\n        motif = "aucun voisin donne"\n',
     '    if False:\n        motif = "aucun voisin donne"\n', "E7"),
    ("S6_erreur_avalee", STAT, "        net = _net(fonction_backtest(dict(jeu)))\n",
     "        try:\n            net = _net(fonction_backtest(dict(jeu)))\n        except Exception:\n            continue\n",
     "E7"),
    ("S7_inscription_oubliee", STAT, "            inscrire(dict(jeu))\n", "            pass\n", "E7"),
    # S8 : l'ancien tirage au hasard remis à la place ; l'appel nouveau reste écrit mais n'est plus fait (sa liste
    # d'arguments part dans une fonction muette), pour que le juge tourne et que seule la mesure change.
    ("S8_ancien_hasard", JUGE, "        st = S.calculer_voisinage_sur_grille(\n",
     "        _v = S.calculer_stabilite_parametrique(_rejouer, _en_fractions(_centre), 0.10, 5)\n"
     "        st = dict(verdict=\"PASSE\" if _v.get(\"stable\") else \"DRAPEAU\", perdants=[], motif_non_mesure=\"\",\n"
     "                  net_min_voisins=_v.get(\"net_min\", 0), net_max_voisins=_v.get(\"net_max\", 0), net_base=0,\n"
     "                  ecart_relatif=None, n_voisins=5, essais_non_inscrits=5)\n"
     "        (lambda *a, **k: None)(\n", "E8"),
    ("S9_bougent_ecrit_dans_le_code", COMM,
     '    bougent = tuple((vus["bougent"].get("valeur") or "").split())\n',
     '    bougent = ("tp", "sl", "horizon")\n', "E9"),
    ("S10_pas_nul_accepte", COMM, "    if n != int(n) or not 1 <= n <= 10:", "    if n != int(n) or not 0 <= n <= 10:", "E6"),
    # S11 : objectif et perte acceptée inversés à la conversion. (Une première forme, « / 1 » au lieu de « / 100 » sur
    # l'objectif, ne mordait pas, mesuré le 11-11-2026 : `pourcent` du juge lit « 4.0 » comme 4 % — il masque l'oubli.)
    ("S11_reglages_croises", JUGE, 'dict(j, tp=round(j["tp"] / 100, 6), sl=round(j["sl"] / 100, 6))',
     'dict(j, tp=round(j["sl"] / 100, 6), sl=round(j["tp"] / 100, 6))', "E8"),
    ("S12_moulinette_avec_sa_propre_grille", PREP,
     "from COMMUN import voisins, pas_entier, POURCENT_MINIMUM, POURCENT_MAXIMUM  # noqa: E402,F401\n",
     "from COMMUN import voisins, pas_entier, POURCENT_MINIMUM, POURCENT_MAXIMUM  # noqa: E402,F401\n"
     "voisins = lambda valeur, regle: [round(valeur, 4)]\n", "E2"),
    # Tour 2 (relecteur du 11-11-2026) : D1, un voisinage qui n'a pas pu tourner doit faire sortir le juge en 1 ;
    # D3, un gain moyen nul ne doit pas rendre un écart relatif de 0 (depuis le tour 3, il s'affiche « indéfini »).
    ("S13_echec_du_voisinage_avale", JUGE,
     '        raise RuntimeError("le voisinage n\'a pas pu tourner (R-734) : %s" % _echec_du_voisinage)\n',
     "        pass\n", "E10"),
    ("S14_gain_moyen_nul_ecart_zero", STAT, '    verdict, motif, ecart_relatif = None, "", None\n',
     '    verdict, motif, ecart_relatif = None, "", 0.0\n', "E7"),
    # Tour 3 (12-11-2026, R-505 ⑩).
    ("S15_un_gagnant_suffit", STAT, '        verdict = "PASSE" if not perdants else "DRAPEAU"\n',
     '        verdict = "PASSE" if len(perdants) < len(details) else "DRAPEAU"\n', "E7"),
    ("S16_centre_compte_parmi_les_voisins", STAT, "    perdants = [d for d in details if",
     '    perdants = [d for d in [{"params": dict(params_base), "net": net_base}] + details if', "E7"),
    ("S17_arrondi_de_python", COMM, "                pas_entiers = math.floor(ecart + 0.5)\n",
     "                pas_entiers = round(ecart)\n", "E11"),
    ("S18_confusion_tue", COMM, "            confondus.append(", "            (lambda *a: None)(", "E11"),
    ("S19_gain_du_fichier_ignore_par_le_juge", JUGE,
     '            _rv["gain_net_de_chaque_voisin_doit_depasser"], inscrire=None)',
     "            0, inscrire=None)", "E9"),
    ("S20_amplitude_du_fichier_ignoree_par_le_juge", JUGE,
     '        _g = GRILLE.grille_du_voisinage(_centre, _rv["bougent"], _rv["amplitude_relative"],',
     '        _g = GRILLE.grille_du_voisinage(_centre, _rv["bougent"], 10.0,', "E9"),
    ("S21_grille_sans_la_fonction_commune", COMM,
     '            bruts = voisins(v, {"pas": pas, "de_part_et_d_autre": pas_de_part_et_d_autre,\n'
     '                                "minimum": POURCENT_MINIMUM, "maximum": POURCENT_MAXIMUM})\n',
     "            bruts = sorted({round(v + k * pas, 4) for k in range(-pas_de_part_et_d_autre,"
     " pas_de_part_et_d_autre + 1)})\n", "E2"),
]

def charger(racine, chemin, nom):
    """Charge un programme du dépôt éprouvé comme module, sans l'exécuter comme programme.

    ① RÔLE — Donner aux épreuves les fonctions de PREPARER et du module de statistiques de LA racine éprouvée.
    ② CONTEXTE D'APPEL — `epreuves`, trois fois.
    ③ ENTRÉE — `racine` : le dépôt éprouvé · `chemin` : relatif à la racine · `nom` : nom donné au module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et s'importe ; `programmes/` de la racine fournit ses imports.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — ① mettre `programmes/` de la racine en tête du chemin d'import · ② charger le fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sabotage réécrit la copie : l'épreuve doit lire la copie, jamais le dépôt d'origine.
    ⑨ CE QUI CLOCHE — Les modules déjà importés (COMMUN, CONTRATS) restent ceux du premier chargement : aucun
      sabotage ne les touche.
    ⑩ EFFET — Modifie `sys.path` du processus ; exécute le haut du fichier chargé.
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur d'import.
      [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    spec = importlib.util.spec_from_file_location(nom, os.path.join(racine, chemin))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def racine_jetable(racine, prefixe):
    """Fabrique une racine jetable : des liens vers chaque fichier du dépôt, `programmes/` et la grille copiés.

    ① RÔLE — Donner aux sabotages, à E9 et à E10 un dépôt où réécrire un programme ou un réglage sans toucher l'original.
    ② CONTEXTE D'APPEL — `epreuves` (E9, E10) et `main` (chaque sabotage).
    ③ ENTRÉE — `racine` : le dépôt d'origine · `prefixe` : début du nom du dossier temporaire.
    ④ CONDITIONS D'ENTRÉE — `cp` accepte l'option `-rs` (liens symboliques) ; ≈ 35 Mo libres sous /tmp.
    ⑤ SORTIE — UNE valeur : le chemin du dossier créé, à effacer par l'appelant.
      [rend: 1]
    ⑥ TRAITEMENT — ① créer le dossier · ② pour chaque entrée de la racine sauf `.git`, `cp -rs` · ③ remplacer les
      liens de `programmes/` et de `donnees/combinatoires/` par de vraies copies.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le disque est presque plein (cadre du plan V7, point 3) : une copie complète du dépôt est exclue ;
      le juge trouve ses fichiers en parcourant des dossiers réels, pas des liens de dossier.
    ⑨ CE QUI CLOCHE — Les fichiers restés en lien pointent vers l'original : un programme qui écrirait dans la
      racine jetable écrirait dans le dépôt. Le juge n'écrit aucun fichier.
    ⑩ EFFET — Crée un dossier sous /tmp.
    ⑪ TERMINAISON — Rend la main, ou lève CalledProcessError. `cp` local : il revient.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix=prefixe)
    for e in sorted(os.listdir(racine)):
        if e != ".git":
            subprocess.run(["cp", "-rs", os.path.join(os.path.abspath(racine), e), os.path.join(d, e)], check=True)
    for sous in ("programmes", os.path.join("donnees", "combinatoires")):
        shutil.rmtree(os.path.join(d, sous))
        shutil.copytree(os.path.join(racine, sous), os.path.join(d, sous))
    return d


def juge_sur(racine):
    """Lance le vrai juge sur C5E10-QA-V1 dans `racine` et rend sa sortie.

    ① RÔLE — Faire tourner le juge tel qu'il tourne pour Jean-Luc, pour E8, E9 et E10.
    ② CONTEXTE D'APPEL — `epreuves`, trois fois.
    ③ ENTRÉE — `racine` : un dépôt complet.
    ④ CONDITIONS D'ENTRÉE — Le juge et ses fichiers sont sous la racine.
    ⑤ SORTIE — UNE valeur : le couple (code de sortie, texte affiché).
      [rend: 1]
    ⑥ TRAITEMENT — ① lancer `python3 -B programmes/JUGE_DES_STRATEGIES.py . C5E10-QA-V1` depuis la racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — C'est la commande du cadre de la mission : « l'instrument est calibre » doit y rester.
    ⑨ CE QUI CLOCHE — Un délai dépassé lève TimeoutExpired, rattrapé par `main` comme une racine inutilisable.
    ⑩ EFFET — Lance un sous-processus qui lit les fichiers de la racine.
    ⑪ TERMINAISON — Rend la main ; le sous-processus est arrêté à 300 s.
      [sort: non]
    """
    r = subprocess.run([sys.executable, "-B", JUGE, ".", "C5E10-QA-V1"], cwd=racine, capture_output=True,
                       text=True, timeout=DELAI)
    return r.returncode, r.stdout + r.stderr


def epreuves(racine):
    """Joue E1 à E11 sur la racine et rend la liste des résultats.

    ① RÔLE — Porter chaque propriété promise par la livraison du voisinage (R-505 ⑩).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : le dépôt éprouvé.
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête du programme.
    ⑤ SORTIE — UNE valeur : la liste des triplets (nom, vrai ou faux, détail).
      [rend: 1]
    ⑥ TRAITEMENT — ① charger PREPARER, COMMUN et le module de statistiques · ② E1 à E11, chacun enveloppé : une erreur
      inattendue rend le cas faux avec son message.
    ⑦ UNITÉ — Pourcents dans la grille ; euros pour les gains.
    ⑧ POURQUOI — Les cas E1, E2, E5 et E8 partent de vraies lignes du registre et des vrais cours (R-732).
    ⑨ CE QUI CLOCHE — Les valeurs attendues d'E1, E5 et E11 sont écrites ici, déduites à la main de ±10 % (4 % →
      3,6 et 4,4 ; 2,5 % → 2,25 et 2,75 ; 20 séances → 18 et 22 ; 30 → 27 et 33).
    ⑩ EFFET — Lance le juge trois fois ; crée et efface deux racines jetables.
    ⑪ TERMINAISON — Rend la main ; le juge est borné à 300 s par lancement.
      [sort: non]
    """
    P = charger(racine, PREP, "prep_eprouve")
    C = charger(racine, COMM, "commun_eprouve")
    S = charger(racine, STAT, "stat_eprouve")
    res = []
    ARR = "ecart_au_plus_proche_moitie_en_s_eloignant_du_centre"

    def note(nom, ok, detail=""):
        """Ajoute un résultat à la liste des épreuves.

        ① RÔLE — Écrire un cas dans la liste rendue. ② CONTEXTE D'APPEL — `epreuves`, une fois par cas.
        ③ ENTRÉE — nom, vrai ou faux, détail. ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — ajouter le triplet. ⑦ UNITÉ — —
        ⑧ POURQUOI — Une seule forme de résultat. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Modifie `res`.
        ⑪ TERMINAISON — Rend toujours la main. [sort: non]
        """
        res.append((nom, bool(ok), detail))

    def grille(centre, bougent=("tp", "sl", "horizon"), amplitude=10.0, n=1, croisement="produit"):
        """Appelle la grille du voisinage de la racine éprouvée avec les réglages de R-505 ⑩ par défaut.

        ① RÔLE — Raccourcir les appels d'E1 à E5 et E11. ② CONTEXTE D'APPEL — `epreuves`.
        ③ ENTRÉE — le centre, et les réglages qui s'écartent du défaut. ④ CONDITIONS D'ENTRÉE — Celles de
        `grille_du_voisinage`. ⑤ SORTIE — UNE valeur : son dictionnaire {"jeux", "confondus"}. [rend: 1]
        ⑥ TRAITEMENT — un appel. ⑦ UNITÉ — pourcents, séances. ⑧ POURQUOI — Un seul endroit pour la forme d'appel.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ou lève ValueError. [sort: non]
        """
        return C.grille_du_voisinage(centre, bougent, amplitude, n, croisement, ARR)

    voisinage_moulinette = {l["parametre"]: l for l in P.lire_tableau(os.path.join(racine, GRILLE))}
    import CONTRATS_DES_FICHIERS as CONTRAT
    fiches = CONTRAT.fiches_des_lignes(P.lire_tableau(os.path.join(racine, "donnees", "cac40_strategies.csv")))

    def centre_de(ident):
        """Rend les réglages d'une vraie fiche du registre, en pourcents et séances.

        ① RÔLE — Partir d'une VRAIE ligne du registre (R-732). ② CONTEXTE D'APPEL — `epreuves`, E1, E2, E5.
        ③ ENTRÉE — `ident` : identifiant de fiche. ④ CONDITIONS D'ENTRÉE — La fiche existe et se lit.
        ⑤ SORTIE — UNE valeur : {"tp", "sl", "horizon"}. [rend: 1]
        ⑥ TRAITEMENT — lire tp, sl par `pourcents_de` et l'horizon par `COMMUN.lire_horizon`, comme `preparer`.
        ⑦ UNITÉ — Pourcents, séances. ⑧ POURQUOI — Lire comme la moulinette lit.
        ⑨ CE QUI CLOCHE — Une durée « aucune » lèverait : aucune fiche éprouvée n'en porte.
        ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ou lève. [sort: non]
        """
        f = fiches[ident]
        return {"tp": P.pourcents_de(f["tp"]), "sl": P.pourcents_de(f["sl"]),
                "horizon": float(P.COMMUN.lire_horizon(f["horizon"]))}

    try:
        c = centre_de("C5E10-QA-V1")
        g = grille(c)
        attendu = {(t, s, h) for t in (3.6, 4.0, 4.4) for s in (2.25, 2.5, 2.75) for h in (18.0, 20.0, 22.0)} - {
            (4.0, 2.5, 20.0)}
        vus = {(x["tp"], x["sl"], x["horizon"]) for x in g["jeux"]}
        note("E1 C5E10-QA-V1 (4 % · 2,5 % · 20 séances) : 26 voisins à ±10 %, croisés, centre exclu, aucun confondu",
             len(g["jeux"]) == 26 and vus == attendu and g["confondus"] == [], "%d jeux" % len(g["jeux"]))
    except Exception as e:
        note("E1 grille de C5E10-QA-V1", False, repr(e))
    try:
        # R-708 : une seule fonction `voisins`, celle de COMMUN, pour la moulinette et pour le juge.
        meme = P.voisins.__module__ == "COMMUN"   # la moulinette tient `voisins` du module COMMUN, pas d'elle-même
        appels = []
        vraie = C.voisins

        def espion(valeur, regle):
            """Compte les appels de la grille du juge à `voisins`, puis appelle la vraie.

            ① RÔLE — Voir si la grille du juge passe par la fonction commune. ② CONTEXTE D'APPEL — E2.
            ③ ENTRÉE — celle de `voisins`. ④ CONDITIONS D'ENTRÉE — Aucune. ⑤ SORTIE — UNE valeur : celle de
            `voisins`. [rend: 1] ⑥ TRAITEMENT — noter, appeler. ⑦ UNITÉ — Celle du réglage.
            ⑧ POURQUOI — R-708. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Modifie `appels`.
            ⑪ TERMINAISON — Rend la main ou lève ValueError. [sort: non]
            """
            appels.append(valeur)
            return vraie(valeur, regle)

        C.voisins = espion
        try:
            grille(c)
        finally:
            C.voisins = vraie
        ref = sorted(__import__("glob").glob(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS*.csv")))[0]
        codes = {(l.get("mnemonique") or "").strip().upper() for l in P.lire_tableau(ref)
                 if not (l.get("hors_univers") or "").strip()} - {""}
        lignes, manques = P.preparer(fiches["C5E10-QA-V1"], voisinage_moulinette, "E99", "epreuve", codes)
        moul = {l["parametre"]: [float(v) for v in l["valeurs_a_essayer"].split(";")] for l in lignes
                if l["parametre"] == "tp"}
        ok = (meme and len(appels) == 3 and not manques
              and moul["tp"] == vraie(c["tp"], voisinage_moulinette["tp"]))
        note("E2 R-708 : la grille du juge appelle `voisins` de COMMUN (3 fois) et la moulinette l'importe de COMMUN",
             ok, "appels=%d moulinette=%s module=%s" % (len(appels), moul.get("tp"), P.voisins.__module__))
    except Exception as e:
        note("E2 une seule fonction voisins", False, repr(e))
    try:
        j = grille(c, croisement="un_a_la_fois")["jeux"]
        note("E3 un_a_la_fois : 6 voisins, un seul réglage bouge", len(j) == 6 and all(
            sum(x[p] != c[p] for p in c) == 1 for x in j), "%d jeux" % len(j))
    except Exception as e:
        note("E3 un_a_la_fois", False, repr(e))
    try:
        j = grille({"tp": 4.0, "sl": 2.5})["jeux"]
        note("E4 durée « aucune » : la durée ne bouge pas, 8 voisins", len(j) == 8 and all("horizon" not in x for x in j),
             "%d jeux" % len(j))
    except Exception as e:
        note("E4 durée aucune", False, repr(e))
    try:
        c3 = centre_de("C5-EI-PARAMS")
        g = grille(c3)
        note("E5 C5-EI-PARAMS (durée 30, hors des bornes 5-25 de la moulinette) : 26 voisins, durées 27, 30, 33",
             len(g["jeux"]) == 26 and {x["horizon"] for x in g["jeux"]} == {27.0, 30.0, 33.0},
             "%d jeux, centre %s" % (len(g["jeux"]), c3))
    except Exception as e:
        note("E5 C5-EI-PARAMS", False, repr(e))
    try:
        r = C.lire_reglages_du_voisinage_du_juge(os.path.join(racine, REGLAGES))
        lus = C.lire_csv(os.path.join(racine, REGLAGES))
        de_r505 = [l["reglage"] for l in lus if (l.get("statut") or "").strip() == "R-505 ⑩"
                   and "R-505 ⑩" in (l.get("source") or "")]
        ok = (set(r) == {"bougent", "amplitude_relative", "pas_de_part_et_d_autre", "croisement",
                         "gain_net_de_chaque_voisin_doit_depasser", "arrondi_de_la_duree", "provisoires"}
              and r["provisoires"] == ["arrondi_de_la_duree"] and len(de_r505) == 5
              and r["bougent"] == ("tp", "sl", "horizon") and r["amplitude_relative"] == 10
              and r["pas_de_part_et_d_autre"] == 1 and r["croisement"] == "produit"
              and r["gain_net_de_chaque_voisin_doit_depasser"] == 0)
        refus = 0
        tmp = tempfile.mkdtemp(prefix="voisinage_e6_")
        cas = [("amplitude_relative", "0"), ("amplitude_relative", "100"), ("amplitude_relative", "nan"),
               ("pas_de_part_et_d_autre", "0"), ("pas_de_part_et_d_autre", "1.5"), ("croisement", "tout"),
               ("bougent", "tp tp"), ("bougent", "objectif"), ("gain_net_de_chaque_voisin_doit_depasser", "nan"),
               ("arrondi_de_la_duree", "python")]
        with open(os.path.join(racine, REGLAGES), encoding="utf-8") as fh:
            texte = fh.read()
        for nom, val in cas:
            lignes = texte.splitlines(True)
            lignes = [(nom + "," + val + "," + l.split(",", 2)[2]) if l.startswith(nom + ",") else l for l in lignes]
            ch = os.path.join(tmp, "r.csv")
            with open(ch, "w", encoding="utf-8") as fh:
                fh.write("".join(lignes))
            try:
                C.lire_reglages_du_voisinage_du_juge(ch)
            except ValueError:
                refus += 1
        with open(os.path.join(tmp, "r.csv"), "w", encoding="utf-8") as fh:
            fh.write(texte + texte.splitlines(True)[1])
        try:
            C.lire_reglages_du_voisinage_du_juge(os.path.join(tmp, "r.csv"))
        except ValueError:
            refus += 1
        shutil.rmtree(tmp)
        note("E6 réglages lus : 5 de R-505 ⑩, 1 provisoire (l'arrondi) ; 11 fichiers fautifs refusés", ok and refus == 11,
             "%d refus sur 11 ; R-505 : %s" % (refus, de_r505))
    except Exception as e:
        note("E6 lecture des réglages", False, repr(e))
    try:
        appels = []

        def rejeu(p):
            """Faux rejeu : gain = 1000 × objectif, et lève si l'objectif vaut 99.

            ① RÔLE — Fabriquer des gains connus. ② CONTEXTE D'APPEL — E7. ③ ENTRÉE — un jeu de réglages.
            ④ CONDITIONS D'ENTRÉE — `tp` présent. ⑤ SORTIE — UNE valeur : {"net"}. [rend: 1]
            ⑥ TRAITEMENT — noter l'appel, lever sur 99, rendre le gain. ⑦ UNITÉ — euros.
            ⑧ POURQUOI — Des gains connus d'avance. ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Modifie `appels`. ⑪ TERMINAISON — Rend la main ou lève RuntimeError. [sort: non]
            """
            appels.append(("rejeu", p["tp"]))
            if p["tp"] == 99:
                raise RuntimeError("rejeu tombé")
            return {"net": 1000.0 * p["tp"]}

        def inscrire(p):
            """Fausse inscription au registre des essais : note l'appel.

            ① RÔLE — Voir l'ordre inscription / rejeu. ② CONTEXTE D'APPEL — E7. ③ ENTRÉE — un jeu.
            ④ CONDITIONS D'ENTRÉE — Aucune. ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — noter.
            ⑦ UNITÉ — — ⑧ POURQUOI — A-226 : inscrire AVANT le calcul. ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Modifie `appels`. ⑪ TERMINAISON — Rend toujours la main. [sort: non]
            """
            appels.append(("inscrire", p["tp"]))

        F = S.calculer_voisinage_sur_grille
        random.seed(7)
        attendu_alea = random.random()
        random.seed(7)
        st = F(rejeu, {"tp": 4}, [{"tp": 3}, {"tp": 5}], 0, inscrire=inscrire)
        sans_alea = random.random() == attendu_alea
        ordre = appels == [("rejeu", 4), ("inscrire", 3), ("rejeu", 3), ("inscrire", 5), ("rejeu", 5)]
        st2 = F(rejeu, {"tp": 4}, [{"tp": 3}, {"tp": 5}], 3000)        # 3 000 € n'est PAS au-dessus de 3 000 €
        st3 = F(rejeu, {"tp": 4}, [], 0)                                # aucun voisin
        st4 = F(rejeu, {"tp": 4}, [{"tp": -1}, {"tp": 5}], 0)           # un perdant, un gagnant
        st5 = F(rejeu, {"tp": -1}, [{"tp": 3}, {"tp": 5}], 0)           # centre perdant, voisins gagnants
        st6 = F(rejeu, {"tp": 0}, [{"tp": -1}, {"tp": 1}], 0)           # gain moyen nul
        try:
            F(rejeu, {"tp": 4}, [{"tp": 99}], 0)
            leve = False
        except RuntimeError:
            leve = True
        ok = (sans_alea and ordre and st["verdict"] == "PASSE" and st["perdants"] == [] and st["ecart_relatif"] == 0.5
              and st["n_voisins"] == 2 and st["essais_inscrits"] == 2 and st["essais_non_inscrits"] == 0
              and st["net_min_voisins"] == 3000 and st["net_max_voisins"] == 5000 and st["net_base"] == 4000
              and st2["verdict"] == "DRAPEAU" and [d["params"] for d in st2["perdants"]] == [{"tp": 3}]
              and st2["essais_non_inscrits"] == 2
              and st3["verdict"] is None and st3["n_voisins"] == 0 and st3["motif_non_mesure"] == "aucun voisin donne"
              and st4["verdict"] == "DRAPEAU" and [d["params"] for d in st4["perdants"]] == [{"tp": -1}]
              and st5["verdict"] == "PASSE" and st5["perdants"] == []
              and st6["ecart_relatif"] is None and st6["verdict"] == "DRAPEAU" and leve)
        note("E7 calcul : tous les voisins doivent dépasser le seuil (strict), centre hors du compte, aucun hasard, "
             "inscription avant rejeu, erreur non avalée, sans voisin → None, moyenne nulle → écart indéfini", ok,
             "st=%s st2=%s st3=%s st4=%s st5=%s st6=%s/%s leve=%s ordre=%s alea=%s" % (
                 st["verdict"], st2["verdict"], st3["verdict"], st4["verdict"], st5["verdict"], st6["verdict"],
                 st6["ecart_relatif"], leve, ordre, sans_alea))
    except Exception as e:
        note("E7 calcul du voisinage", False, repr(e))
    try:
        code, sortie = juge_sur(racine)
        ok = (code == 0 and "l'instrument est calibre" in sortie
              and "26 voisin(s) a +-10 % de chaque reglage (tp sl horizon ; 1 pas de part et d'autre ; produit ; R-505 ⑩)"
              in sortie
              and "de +43 335 a +55 793 EUR · centre +53 944 EUR" in sortie
              and "PASSE — les 26 voisins gagnent" in sortie and "26 joue(s), 26 NON INSCRIT(S)" in sortie
              and "reglages PROVISOIRES, A DECIDER PAR JEAN-LUC : arrondi_de_la_duree" in sortie)
        note("E8 vrai juge sur C5E10-QA-V1 : calibré, 26 voisins à ±10 %, voisins +43 335 à +55 793, PASSE, essais dits",
             ok, "code %s" % code)
    except Exception as e:
        note("E8 vrai juge", False, repr(e))
    d = None
    try:
        d = racine_jetable(racine, "voisinage_e9_")
        ch = os.path.join(d, REGLAGES)
        with open(ch, encoding="utf-8") as fh:
            texte = fh.read()
        for avant, apres in (("bougent,tp sl horizon,", "bougent,tp,"), ("amplitude_relative,10,", "amplitude_relative,20,"),
                             ("gain_net_de_chaque_voisin_doit_depasser,0,",
                              "gain_net_de_chaque_voisin_doit_depasser,1000000000,")):
            if texte.count(avant) != 1:
                raise ValueError("E9 : %r introuvable dans le fichier des réglages" % avant)
            texte = texte.replace(avant, apres)
        with open(ch, "w", encoding="utf-8") as fh:
            fh.write(texte)
        code, sortie = juge_sur(d)
        perdants = sorted(l.split(":")[0].split("TP ")[1].split(" ")[0] for l in sortie.splitlines()
                          if l.strip().startswith("perdant "))
        note("E9 le juge lit le fichier : tp seul, ±20 %, seuil 10⁹ € → DRAPEAU, 2 perdants (3,20 % et 4,80 %), code 0",
             code == 0 and "2 voisin(s) a +-20 % de chaque reglage (tp ;" in sortie
             and "DRAPEAU « voisinage » — 2 voisin(s) sur 2 ne depasse(nt) pas +1 000 000 000 EUR" in sortie
             and perdants == ["+3.20%", "+4.80%"], "code %s, perdants %s" % (code, perdants))
    except Exception as e:
        note("E9 lecture du fichier par le juge", False, repr(e))
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
    d = None
    try:
        d = racine_jetable(racine, "voisinage_e10_")
        os.remove(os.path.join(d, REGLAGES))
        code, sortie = juge_sur(d)
        note("E10 réglages absents : VOISINAGE EN ÉCHEC, rapport poursuivi, fiche EN ÉCHEC, code 1 (R-734)",
             code == 1 and "VOISINAGE            EN ÉCHEC — n'a pas pu tourner" in sortie and "PIRE CREUX" in sortie
             and "FICHES EN ÉCHEC (1) : C5E10-QA-V1" in sortie, "code %s" % code)
    except Exception as e:
        note("E10 voisinage qui n'a pas pu tourner", False, repr(e))
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
    try:
        dur = {}
        for h in (5.0, 20.0, 21.0, 25.0, 30.0):
            g = grille({"tp": 4.0, "sl": 2.5, "horizon": h}, bougent=("horizon",))
            dur[h] = ([x["horizon"] for x in g["jeux"]], g["confondus"])
        g4 = grille({"tp": 4.0, "sl": 2.5, "horizon": 4.0}, bougent=("horizon",))
        try:
            grille({"tp": 4.0, "sl": 2.5, "horizon": 20.5})
            refuse = False
        except ValueError:
            refuse = True
        ok = (dur[5.0] == ([4.0, 6.0], []) and dur[20.0] == ([18.0, 22.0], []) and dur[21.0] == ([19.0, 23.0], [])
              and dur[25.0] == ([22.0, 28.0], []) and dur[30.0] == ([27.0, 33.0], [])
              and g4["jeux"] == [] and len(g4["confondus"]) == 1 and g4["confondus"][0].startswith("horizon : 1 valeur")
              and refuse)
        note("E11 arrondi de la durée : 5→4/6, 21→19/23, 25→22/28 ; 4 séances → voisins confondus et dits ; "
             "durée non entière refusée", ok, "%s ; 4 → %s ; refus %s" % (dur, g4, refuse))
    except Exception as e:
        note("E11 arrondi de la durée", False, repr(e))
    return res


def main(argv):
    """Lance les épreuves, puis, sur demande, chaque sabotage, et rend le code de sortie.

    ① RÔLE — Point d'entrée. ② CONTEXTE D'APPEL — Le lancement du programme.
    ③ ENTRÉE — `argv` : la racine, puis « --sabotages » ou « --un-sabotage=NOM », facultatifs.
    ④ CONDITIONS D'ENTRÉE — La racine porte les fichiers de l'en-tête ; sinon code 2.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier la racine · ② jouer les épreuves et afficher · ③ avec « --sabotages » : pour chaque
      sabotage, racine jetable, réécriture d'UN endroit (refus si le texte n'y est pas exactement une fois), rejeu
      de ce programme sur la copie, exiger le code 1 ET l'épreuve visée en ÉCHEC · ④ rendre le code.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (§7).
    ⑨ CE QUI CLOCHE — Les sabotages tournent l'un après l'autre (21 lancements de 20 à 30 s chacun).
    ⑩ EFFET — Affiche ; crée et efface des racines jetables.
    ⑪ TERMINAISON — Rend la main avec le code ; chaque rejeu est borné à 300 s.
      [sort: non]
    """
    if not argv:
        print(__doc__)
        return 2
    racine = os.path.abspath(argv[0])
    for f in (PREP, COMM, STAT, JUGE, REGLAGES, GRILLE):
        if not os.path.isfile(os.path.join(racine, f)):
            print("RACINE INUTILISABLE : %s absent" % f)
            return 2
    try:
        res = epreuves(racine)
    except Exception as e:
        print("RACINE INUTILISABLE : %r" % (e,))
        return 2
    for nom, ok, detail in res:
        print("%s  %s  %s" % ("OK    " if ok else "ÉCHEC ", nom, detail))
    code = 0 if all(ok for _, ok, _ in res) else 1
    print("VERDICT : %s" % ("tout vert" if code == 0 else "ROUGE"))
    seul = [a.split("=", 1)[1] for a in argv[1:] if a.startswith("--un-sabotage=")]
    if "--sabotages" in argv[1:] or seul:
        mordent = 0
        choisis = [x for x in SABOTAGES if not seul or x[0] in seul]
        for nom, fichier, avant, apres, visee in choisis:
            d = racine_jetable(racine, "voisinage_sab_")
            try:
                ch = os.path.join(d, fichier)
                with open(ch, encoding="utf-8") as fh:
                    texte = fh.read()
                if texte.count(avant) != 1:
                    print("== %s : CIBLE INTROUVABLE (%d occurrences) — NE MORD PAS" % (nom, texte.count(avant)))
                    code = 1
                    continue
                with open(ch, "w", encoding="utf-8") as fh:
                    fh.write(texte.replace(avant, apres))
                r = subprocess.run([sys.executable, "-B", ICI, d], capture_output=True, text=True, timeout=DELAI * 3)
                rouges = [m.group(1) for m in (re.match(r"^ÉCHEC\s+(E[0-9]+)\s", l) for l in r.stdout.splitlines()) if m]
                mord = r.returncode == 1 and visee in rouges
                mordent += mord
                if not mord:
                    code = 1
                print("== %s : %s (%s)" % (nom, "mord" if mord else "NE MORD PAS",
                                          " · ".join(rouges) or "code %s" % r.returncode))
            finally:
                shutil.rmtree(d, ignore_errors=True)
        print("SABOTAGES : %d/%d mordent" % (mordent, len(choisis)))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
