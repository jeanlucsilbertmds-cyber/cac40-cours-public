#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CARNET_DE_LA_VRAIE_VIE — Lun 16-11-2026 (Paris). Étape CARNET, partie 2. SIMULATION UNIQUEMENT.

À QUOI ÇA SERT, EN FRANÇAIS SIMPLE. Jean-Luc a décidé le 14-11-2026 (A-788, 17h36-17h39) que le carnet porte « la
vraie vie » d'une stratégie — une ligne par soir, les mêmes indicateurs que les blocs figés de sa fiche, sur les
trades vécus, rien d'écrasé — puis le 16-11-2026 à 10h16 (A-845, « 1 ») que ce carnet VIT dans
donnees/historique_mesures.csv, par des colonnes ajoutées. Et le 14-11-2026 à 11h48 (A-768 ②) : « même identifiant ⇒
même empreinte, sinon rouge ». Cette épreuve vérifie, sur les VRAIES données du dépôt (R-732), que la mesure du soir
(programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py) écrit ces colonnes sans réécrire une ligne passée, que le
contrôle d'empreinte rougit sur le cas E5 de la branche v7-E4 RETOURNÉ, et que le cockpit qui lit le fichier ne casse
pas.

LES CAS, JOUÉS DANS DES COPIES (programmes/, gouvernance/, emp.py, fichiers de premier niveau de donnees/) :
  C1 le contrat : `MESURE` = les 27 colonnes d'avant puis `CARNET_DE_LA_VRAIE_VIE` ; chaque colonne du carnet a sa
     définition et rien d'autre n'en a ; les deux colonnes anciennes de sens différent (`pertes_consecutives`,
     `pire_chute_eur`) ont le leur au contrat et y nomment leur voisine du carnet ; la mesure lit ses colonnes au contrat ; chaque colonne `carnet_X` (sauf
     l'état et le début de période) est une clé que rend `mesurer_les_indicateurs` ; l'en-tête du fichier du dépôt
     est le contrat.
  C2 l'historique du dépôt, ramené à son en-tête d'avant (27 colonnes) et privé de ses 4 lignes de la dernière séance
     (de vraies lignes) : la mesure rend 0, allonge l'en-tête, garde À L'OCTET les lignes écrites, réécrit les 4
     lignes avec un carnet CALCULÉ, une empreinte de 16 hexadécimaux commune aux deux comptabilités d'une stratégie,
     et des chiffres qui recoupent les colonnes anciennes calculées par un autre chemin (`stats`) : opérations,
     gain moyen, taux ; `pire_chute_eur` ≤ 0 et `carnet_pire_creux_eur` ≥ 0 ; le début de période est le même pour les deux comptabilités d'une stratégie, et vaut celui
     que l'épreuve recalcule (plus ancienne de `date_entree_etat` et des entrées d'opérations comptées).
  C3 relancée, la mesure n'ajoute rien et le fichier ne change pas d'un octet.
  C4 L'ÉPREUVE E5 DE v7-E4, RETOURNÉE : la dernière ligne de C5E10-QA-V1 (tp +4,0 %) recopiée sous le même
     identifiant avec un tp de +9,0 % → la mesure rend 1 et nomme C5E10-QA-V1, et lui seul ; la dernière ligne de
     C5E10-OBS-V1 recopiée avec une note changée ne rougit pas (cas qui doit échouer à rougir). Dans v7-E4, cette
     ligne passait pour une « version neuve » que seul l'écrivain refusait ; depuis A-768, elle est la faute.
  C5 un en-tête qui n'est pas le début du contrat (une colonne renommée) → ARRÊT, code 1, fichier intact.
  C6 sans le module des indicateurs, les colonnes anciennes sont écrites, le carnet dit INCONNU et la mesure rend 1
     (R-734).
  C7 le cockpit (GENERATEUR_COCKPIT, nourri comme PUBLIER_LE_SITE le nourrit) rend la même page, à l'heure près,
     sur l'historique à 27 colonnes et sur le même historique à en-tête allongé ; puis il tourne sur l'historique où
     la mesure a écrit des lignes de carnet.

USAGE : python3 -B tests/EPREUVES_DU_CARNET_DE_LA_VRAIE_VIE_Lun_16-11-2026.py <racine> [--saboter | nom]
CODE : 0 si Z0 est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si la racine est
inutilisable, si une cible de sabotage est introuvable ou si le nom demandé n'existe pas (R-734).

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; et par programmes/CERTIFIER_LA_VERSION.py, qui lance chaque épreuve de tests/ avec la
  racine, puis avec `--saboter`. Le mode « --cas <copie> » est interne.
③ ENTRÉE — La racine d'un dépôt ; `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : la mesure du soir, le contrat, le module des indicateurs, le juge, le
  générateur du cockpit, donnees/historique_mesures.csv (au moins 4 lignes de la dernière séance), le journal des
  trades, le registre des stratégies avec C5E10-QA-V1 et C5E10-OBS-V1, donnees/cours_maitre.csv.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : copier la racine (partiellement, voir plus haut), appliquer le
  sabotage, relancer la copie en mode « --cas », juger.
⑦ UNITÉ — Lignes, octets, euros, pourcents, empreintes de 16 caractères hexadécimaux.
⑧ POURQUOI — Voir « À QUOI ÇA SERT ». Les recoupements de C2 passent par un AUTRE calcul (`stats` de la mesure) que
  celui du carnet (`mesurer_les_indicateurs`) : un même calcul ne se recoupe pas lui-même.
⑨ CE QUI CLOCHE — ① La séance réelle rejouée est la dernière du fichier ; elle change chaque soir, et ses chiffres ne
  sont pas figés ici (seuls les recoupements le sont). ② Le cockpit n'AFFICHE pas encore le carnet (étape L13 du
  planning) : C7 prouve seulement qu'il ne casse pas. ③ Les recoupements arrondissent au centième d'euro et au
  dixième de point.
⑩ EFFET — Crée et efface des dossiers temporaires ; lance python3. N'écrit rien sous la racine.
⑪ TERMINAISON — Sort du programme ; chaque relance a un délai de DELAI secondes.
  [sort: oui]
"""
import csv
import glob
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

SOI = os.path.join("tests", os.path.basename(__file__))
MESURER = os.path.join("programmes", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py")
CONTRAT = os.path.join("programmes", "CONTRATS_DES_FICHIERS.py")
COCKPIT = os.path.join("programmes", "GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py")
SITE = os.path.join("programmes", "PUBLIER_LE_SITE.py")
HISTO = os.path.join("donnees", "historique_mesures.csv")
DELAI = 900
NOMBRE_DE_CAS = 7
# Les 27 colonnes de l'historique avant le carnet (en-tête du fichier au 16-11-2026, relu ce jour-là).
COLONNES_D_AVANT = [
    "date_mesure", "strategie", "comptabilite", "etat", "n_operations", "gagnantes", "taux_reussite",
    "borne_basse_wilson", "point_mort", "verdict_c7", "cumul_net_eur", "esperance_eur", "facteur_profit",
    "serie_en_cours", "pertes_consecutives", "pire_chute_pct", "pire_chute_eur", "compteur", "seuil",
    "conformite_promis", "voyant_c7", "voyant_pertes", "voyant_chute", "temoin_permanent", "temoin_miroir",
    "rapport_gain_secousses", "source_calibrage",
]

SABOTAGES = {
    "K01_en_tete_reecrit_les_lignes": [(MESURER, "        neuf = ','.join(colonnes).encode('utf-8') + eol + reste\n",
                                        "        neuf = ','.join(colonnes).encode('utf-8') + eol + "
                                        "reste.replace(b'\\r\\n', b'\\n')\n")],
    "K02_confrontation_muette": [(MESURER, "    return sorted(e for e in ecrites if e != empreinte)\n",
                                  "    return []\n")],
    "K03_prix_inverses": [(MESURER, "PRIX_DE_LA_COLONNE = {'pnl_net_eur': 'reel', 'pnl_net_convention_eur': 'convention'}",
                           "PRIX_DE_LA_COLONNE = {'pnl_net_eur': 'convention', 'pnl_net_convention_eur': 'reel'}")],
    "K04_empreinte_non_ecrite": [(MESURER, "            _l['empreinte_des_reglages'] = _empreintes[sid][0]\n",
                                  "            _l['empreinte_des_reglages'] = ''\n")],
    "K05_colonnes_recopiees": [(MESURER, "COLONNES = list(_MESURE)\n", "COLONNES = list(_MESURE)[:27]\n")],
    "K06_en_tete_non_allonge": [(MESURER, "        _etat_tete, _phrase_tete = etendre_l_en_tete(dest, COLONNES)\n",
                                 "        _etat_tete, _phrase_tete = 'IDENTIQUE', ''\n")],
    "K07_periode_par_comptabilite": [(MESURER, "_colonne_de[gref], _periode))\n",
                                      "_colonne_de[gref], periode_du_carnet(carte, operations_de(operations, carte, "
                                      "gref), jour)))\n")],
    "K08_inconnu_deguise": [(MESURER, "        cases['carnet_etat'] = (ETAT_DU_CARNET_INCONNU + f\"{type(e).__name__}: {e}\")[:300]\n",
                             "        cases['carnet_etat'] = ETAT_DU_CARNET_CALCULE\n")],
    "K09_code_un_perdu": [(MESURER, "        print(\"        Le reste est ecrit ; CODE 1 (R-734).\")\n        _code = 1\n",
                           "        print(\"        Le reste est ecrit ; CODE 1 (R-734).\")\n        _code = 0\n")],
    "K10_refus_d_en_tete_ignore": [(MESURER, "    if len(champs) < len(colonnes) and champs == list(colonnes)[:len(champs)]:\n",
                                    "    if True:\n")],
    "K11_definition_manquante": [(CONTRAT, '    "carnet_calmar": "gain net par an ÷ pire creux (ratio sans unité, affiché, ne décide rien)",\n',
                                  "")],
    # F1 du 16-11-2026 : le sens des deux colonnes anciennes voisines du carnet est dit au contrat, et leurs signes
    # (chute négative, creux positif) sont vérifiés sur de vraies lignes en C2.
    "K13_sens_voisin_manquant": [(CONTRAT, '    "pertes_consecutives": "pertes d\'affilée EN COURS : celles qui terminent la liste des opérations, zéro si la "\n',
                                  '    "pertes_consecutives_x": "pertes d\'affilée EN COURS : celles qui terminent la liste des opérations, zéro si la "\n')],
    "K14_chute_ancienne_positive": [(MESURER, "        'pire_chute_eur': f\"{s['chute_eur']:.2f}\",\n",
                                     "        'pire_chute_eur': f\"{-s['chute_eur']:.2f}\",\n")],
    "K15_creux_du_carnet_negatif": [(os.path.join("programmes", "MESURER_LES_INDICATEURS.py"),
                                     '        "pire_creux_eur": creux,\n', '        "pire_creux_eur": -creux,\n')],
    "K12_empreinte_d_une_autre_fiche": [(MESURER, "        _empreintes[sid] = empreinte_de_la_carte(carte)\n",
                                         "        _empreintes[sid] = empreinte_de_la_carte(dict(carte, tp='+1.0%'))\n")],
}


def le_contrat(racine):
    """Charge le contrat des fichiers d'une racine, pour y lire le chemin du registre des stratégies et sa lecture.
    ① RÔLE — ne jamais écrire ici le nom du registre ni la règle n°83 (la dernière ligne fait foi) : ils vivent au
    contrat, une fois (`REGISTRE_DES_STRATEGIES`, `fiches_du_registre`). ② CONTEXTE D'APPEL — C2 et C4, avec la
    racine d'un scénario ; C7 passe par `les_entrees_du_site`. ③ ENTRÉE — `racine` : une copie du dépôt. ④ CONDITIONS D'ENTRÉE — la
    racine porte le fichier du contrat (`CONTRAT`). ⑤ SORTIE — UNE valeur : le module du contrat de cette racine.
    [rend: 1] ⑥ TRAITEMENT — import par chemin, sous un nom propre à l'épreuve. ⑦ UNITÉ — —. ⑧ POURQUOI — deux
    écritures d'une même chose divergent toujours (R-708) ; le contrat porte `REGISTRE_DES_STRATEGIES` et
    `NOM_DU_REGISTRE_DES_STRATEGIES` (décision n°83), et l'épreuve du registre des stratégies (G1) rougit dès qu'une
    constante du code les recopie : relecture du tour 3 (D1, 18-11-2026), superviseur R-759 « DE FOND ».
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — exécute le module du contrat. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]"""
    import importlib.util as iu
    sp = iu.spec_from_file_location("CONTRAT_DE_L_EPREUVE_DU_CARNET", os.path.join(racine, CONTRAT))
    module = iu.module_from_spec(sp)
    sp.loader.exec_module(module)
    return module


def les_entrees_du_site(racine):
    """Rend la table « fichier du dépôt → nom attendu par le générateur du cockpit » de la publication de la racine.
    ① RÔLE — nourrir le cockpit en C7 avec les MÊMES fichiers que la publication du soir, sans les recopier ici.
    ② CONTEXTE D'APPEL — `page` de C7, une fois par page. ③ ENTRÉE — `racine` : une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — la racine porte `SITE` et le contrat des fichiers sous `programmes/`.
    ⑤ SORTIE — UNE valeur : la liste `ENTREES` de PUBLIER_LE_SITE, couples (chemin sous la racine, nom à plat).
    [rend: 1] ⑥ TRAITEMENT — import par chemin, sous un nom propre à l'épreuve ; le haut du module ne fait qu'importer
    et poser des constantes (son travail est sous `if __name__ == "__main__"`). ⑦ UNITÉ — —. ⑧ POURQUOI — deux
    écritures d'une même chose divergent toujours (R-708) : `ENTREES` (PUBLIER_LE_SITE l.94-100) est la seule source de
    ces couples ; recopiés ici, un fichier ajouté ou renommé à la publication laissait C7 vert sur l'ancien jeu
    (relecture du tour 4, N2, 18-11-2026 ; superviseur R-759 « DE FOND »). ⑨ CE QUI CLOCHE — la table porte aussi
    l'historique des mesures, que C7 remplace ensuite par ses propres octets. ⑩ EFFET — exécute le haut du module
    (ajoute son dossier au chemin d'import). ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]"""
    import importlib.util as iu
    sp = iu.spec_from_file_location("SITE_DE_L_EPREUVE_DU_CARNET", os.path.join(racine, SITE))
    module = iu.module_from_spec(sp)
    sp.loader.exec_module(module)
    return list(module.ENTREES)


def copier_la_base(depot, cible):
    """Copie ce dont la mesure, le contrat, les indicateurs et le cockpit ont besoin.
    ① RÔLE — des copies légères (14 Mo au lieu de 337). ② CONTEXTE D'APPEL — `preparer`, `scenario`.
    ③ ENTRÉE — `depot` : la source · `cible` : le dossier à créer. ④ CONDITIONS D'ENTRÉE — `cible` n'existe pas.
    ⑤ SORTIE — Aucune. [rend: rien]
    ⑥ TRAITEMENT — programmes/, gouvernance/, tests/ de ce programme, emp.py, et les fichiers de premier niveau de
    donnees/ (sans ses sous-dossiers de sources). ⑦ UNITÉ — —. ⑧ POURQUOI — la mesure, le juge et le cockpit ne lisent
    que ceux-là (mesuré le 16-11-2026 : la mesure tourne à l'identique dans une telle copie).
    ⑨ CE QUI CLOCHE — un fichier de donnees/ rangé demain dans un sous-dossier manquerait. ⑩ EFFET — écrit.
    ⑪ TERMINAISON — Rend la main ; lève OSError. [sort: non]"""
    os.makedirs(os.path.join(cible, "donnees"))
    os.makedirs(os.path.join(cible, "tests"))
    for d in ("programmes", "gouvernance"):
        shutil.copytree(os.path.join(depot, d), os.path.join(cible, d),
                        ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(os.path.join(depot, "emp.py"), cible)
    shutil.copy2(os.path.join(depot, SOI), os.path.join(cible, "tests"))
    for f in os.listdir(os.path.join(depot, "donnees")):
        p = os.path.join(depot, "donnees", f)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(cible, "donnees", f))


def mesurer(racine):
    """Lance la mesure du soir sur une copie et rend (code, sortie).
    ① RÔLE — jouer le vrai programme, comme le circuit. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — `python3 MESURER racine`, depuis
    la racine (le fichier est écrit sous le dossier courant). ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — lance un processus qui écrit sous `racine`. ⑪ TERMINAISON — Rend la main ; lève sur délai dépassé.
    [sort: non]"""
    p = subprocess.run([sys.executable, "-B", os.path.join(racine, MESURER), racine], cwd=racine,
                       capture_output=True, text=True, timeout=DELAI)
    return p.returncode, p.stdout + p.stderr


def lire(racine):
    """Rend les octets et les lignes (dictionnaires) de l'historique d'une copie.
    ① RÔLE — lire le résultat. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — lecture brute puis `csv.DictReader`. ⑦ UNITÉ — —.
    ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    b = open(os.path.join(racine, HISTO), "rb").read()
    return b, list(csv.DictReader(io.StringIO(b.decode("utf-8"))))


def scenario(copie, nom):
    """Prépare un scénario : une copie de la copie, historique ramené à 27 colonnes et privé de sa dernière séance.
    ① RÔLE — partir chaque fois d'un état connu. ② CONTEXTE D'APPEL — les cas. ③ ENTRÉE — `copie`, `nom`.
    ④ CONDITIONS D'ENTRÉE — l'historique de la copie a au moins une séance. ⑤ SORTIE — TROIS valeurs : la racine du
    scénario, les octets des lignes gardées (après l'en-tête), la date de la séance retirée. [rend: 3]
    ⑥ TRAITEMENT — copier ; garder l'en-tête des 27 colonnes ; retirer les lignes dont la date est la plus récente
    (comparées par leur premier champ). ⑦ UNITÉ — —. ⑧ POURQUOI — rejouer l'état du dépôt AVANT le carnet, sur de
    vraies lignes. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit sous un dossier temporaire. ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    r = os.path.join(tempfile.mkdtemp(prefix="carnet_" + nom + "_"), "r")
    shutil.copytree(copie, r, ignore=shutil.ignore_patterns("__pycache__"))
    b = open(os.path.join(r, HISTO), "rb").read()
    lignes = b.split(b"\r\n")
    corps = [l for l in lignes[1:] if l]
    derniere = max(l.split(b",", 1)[0] for l in corps)
    gardees = [l for l in corps if l.split(b",", 1)[0] != derniere]
    reste = b"".join(l + b"\r\n" for l in gardees)
    open(os.path.join(r, HISTO), "wb").write(",".join(COLONNES_D_AVANT).encode() + b"\r\n" + reste)
    return r, reste, derniere.decode()


def charger(copie):
    """Charge le contrat, la mesure et le module des indicateurs de la copie.
    ① RÔLE — éprouver le code de la copie. ② CONTEXTE D'APPEL — C1. ③ ENTRÉE — `copie`. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — TROIS valeurs. [rend: 3] ⑥ TRAITEMENT — import par chemin. ⑦ UNITÉ — —. ⑧ POURQUOI — —.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — exécute les modules. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]"""
    import importlib.util as iu
    sys.path.insert(0, os.path.join(copie, "programmes"))
    import CONTRATS_DES_FICHIERS as C
    sp = iu.spec_from_file_location("MESURE_DU_SOIR", os.path.join(copie, MESURER))
    M = iu.module_from_spec(sp)
    sp.loader.exec_module(M)
    import MESURER_LES_INDICATEURS as MI
    return C, M, MI


def cas(copie):
    """Joue les sept cas et rend leurs résultats.
    ① RÔLE — C1 à C7 (voir l'en-tête). ② CONTEXTE D'APPEL — le mode « --cas ». ③ ENTRÉE — `copie`.
    ④ CONDITIONS D'ENTRÉE — celles du programme. ⑤ SORTIE — UNE valeur : liste de (nom, vrai/faux, détail).
    [rend: 1]
    ⑥ TRAITEMENT — chaque cas dans un `try`. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — crée des scénarios temporaires. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    res = []

    def un(nom, f):
        """Joue un cas. ① RÔLE — une erreur fait rougir. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, f.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune. [rend: rien] ⑥ TRAITEMENT — f() rend (ok, détail).
        ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — ajoute à res. ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        try:
            ok, detail = f()
        except Exception as e:
            ok, detail = False, "%s : %s" % (type(e).__name__, e)
        res.append((nom, bool(ok), detail))

    def c1():
        """C1. ① RÔLE — le contrat. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — voir l'en-tête. ⑦ UNITÉ — —. ⑧ POURQUOI — R-708.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — charge des modules. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        C, M, MI = charger(copie)
        fautes = []
        if list(C.MESURE) != COLONNES_D_AVANT + list(C.CARNET_DE_LA_VRAIE_VIE):
            fautes.append("MESURE n'est pas les 27 colonnes d'avant suivies du carnet")
        if set(C.DEFINITIONS_DU_CARNET) != set(C.CARNET_DE_LA_VRAIE_VIE):
            fautes.append("définitions ≠ colonnes : %s" % sorted(set(C.DEFINITIONS_DU_CARNET) ^ set(C.CARNET_DE_LA_VRAIE_VIE)))
        voisines = {"pertes_consecutives": "carnet_plus_longue_serie_de_pertes", "pire_chute_eur": "carnet_pire_creux_eur"}
        if set(C.SENS_DES_COLONNES_VOISINES) != set(voisines):
            fautes.append("sens des colonnes voisines : %s au lieu de %s" % (sorted(C.SENS_DES_COLONNES_VOISINES),
                                                                            sorted(voisines)))
        for a, b in voisines.items():
            if b not in C.SENS_DES_COLONNES_VOISINES.get(a, "") or a not in C.DEFINITIONS_DU_CARNET.get(b, ""):
                fautes.append("%s et %s ne se nomment pas l'une l'autre au contrat" % (a, b))
        if list(M.COLONNES) != list(C.MESURE):
            fautes.append("la mesure n'écrit pas les colonnes du contrat (%d au lieu de %d)" % (len(M.COLONNES), len(C.MESURE)))
        r = MI.mesurer_les_indicateurs([], C.UN_JETON, ("2026-01-01", "2026-02-01"), copie, tirages_du_seuil=10)
        absentes = [c for c in C.CARNET_DE_LA_VRAIE_VIE if c.startswith("carnet_")
                    and c not in ("carnet_etat", "carnet_periode_debut") and c[len("carnet_"):] not in r]
        if absentes:
            fautes.append("colonnes sans clé au module des indicateurs : %s" % absentes)
        tete = open(os.path.join(copie, HISTO), "rb").read().split(b"\r\n", 1)[0].decode().split(",")
        if tete != list(C.MESURE):
            fautes.append("l'en-tête du fichier du dépôt n'est pas le contrat (%d colonnes)" % len(tete))
        return not fautes, "; ".join(fautes) or "%d colonnes = 27 + %d du carnet, toutes définies" % (
            len(C.MESURE), len(C.CARNET_DE_LA_VRAIE_VIE))
    un("C1 contrat du carnet", c1)

    etat = {}

    def c2():
        """C2. ① RÔLE — la mesure écrit le carnet sur de vraies lignes. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — —.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — voir l'en-tête.
        ⑦ UNITÉ — euros, pourcents. ⑧ POURQUOI — recoupements par un autre calcul. ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — écrit sous un scénario. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        r, reste, seance = scenario(copie, "c2")
        etat["r"] = r
        code, out = mesurer(r)
        b, lignes = lire(r)
        sys.path.insert(0, os.path.join(copie, "programmes"))
        import CONTRATS_DES_FICHIERS as C
        fautes = []
        if code != 0:
            fautes.append("code %d : %s" % (code, out.strip()[-300:]))
        tete, corps = b.split(b"\r\n", 1)
        if tete.decode().split(",") != list(C.MESURE):
            fautes.append("en-tête non allongé au contrat")
        if not corps.startswith(reste):
            fautes.append("les lignes écrites n'ont pas gardé leurs octets")
        neuves = [l for l in lignes if l["date_mesure"] == seance]
        if len(neuves) != 4:
            fautes.append("%d lignes de la séance %s au lieu de 4" % (len(neuves), seance))
        ct = le_contrat(r)   # n°83 (la dernière ligne fait foi) lue au contrat, pas réécrite ici (N3, 18-11-2026)
        fiche = ct.fiches_du_registre(os.path.join(r, ct.REGISTRE_DES_STRATEGIES))
        journal = list(csv.DictReader(open(os.path.join(r, "donnees", "claude_journal_trades.csv"), encoding="utf-8")))
        par_strat = {}
        for l in neuves:
            if l.get("carnet_etat") != "CALCULÉ":
                fautes.append("%s %s : carnet %r" % (l["strategie"], l["comptabilite"], l.get("carnet_etat")))
                continue
            if not re.fullmatch(r"[0-9a-f]{16}", l.get("empreinte_des_reglages") or ""):
                fautes.append("%s : empreinte %r" % (l["strategie"], l.get("empreinte_des_reglages")))
            par_strat.setdefault(l["strategie"], []).append(l)
            if int(l["carnet_operations"]) != int(l["n_operations"]):
                fautes.append("%s %s : opérations %s ≠ %s" % (l["strategie"], l["comptabilite"],
                                                             l["carnet_operations"], l["n_operations"]))
            if l["esperance_eur"] and abs(float(l["carnet_gain_moyen_eur"]) - float(l["esperance_eur"])) > 0.006:
                fautes.append("%s %s : gain moyen %s ≠ espérance %s" % (l["strategie"], l["comptabilite"],
                                                                      l["carnet_gain_moyen_eur"], l["esperance_eur"]))
            # F1 : les signes dits au contrat (SENS_DES_COLONNES_VOISINES, DEFINITIONS_DU_CARNET)
            if float(l["pire_chute_eur"] or 0) > 0 or float(l["carnet_pire_creux_eur"] or 0) < 0:
                fautes.append("%s %s : chute %s (attendue ≤ 0), creux %s (attendu ≥ 0)" % (
                    l["strategie"], l["comptabilite"], l["pire_chute_eur"], l["carnet_pire_creux_eur"]))
            if l["taux_reussite"] and abs(float(l["carnet_taux_reussite_pct"]) - float(l["taux_reussite"])) > 0.051:
                fautes.append("%s %s : taux %s ≠ %s" % (l["strategie"], l["comptabilite"],
                                                       l["carnet_taux_reussite_pct"], l["taux_reussite"]))
        for sid, ls in par_strat.items():
            if len({l["empreinte_des_reglages"] for l in ls}) != 1:
                fautes.append("%s : deux empreintes le même soir" % sid)
            if len({l["carnet_periode_debut"] for l in ls}) != 1:
                fautes.append("%s : deux débuts de période (%s)" % (sid, sorted({l["carnet_periode_debut"] for l in ls})))
            # le début recalculé ici, sans la mesure : noms au journal = identifiant ou nom court (appariement exact)
            court = (fiche[sid].get("nom") or "").split("(")[0].strip()
            entrees = [t["date_entree"] for t in journal if t["strategie"] in (sid, court)]
            attendu = min([fiche[sid]["date_entree_etat"]] + entrees)
            if ls[0]["carnet_periode_debut"] != attendu:
                fautes.append("%s : début %s, attendu %s" % (sid, ls[0]["carnet_periode_debut"], attendu))
        if len(par_strat) == 2 and len({ls[0]["empreinte_des_reglages"] for ls in par_strat.values()}) != 2:
            fautes.append("les deux stratégies ont la même empreinte")
        return not fautes, "; ".join(fautes) or "séance %s : 4 lignes de carnet, %d octets anciens intacts, %s" % (
            seance, len(reste), ", ".join("%s %s" % (k, v[0]["empreinte_des_reglages"]) for k, v in sorted(par_strat.items())))
    un("C2 la mesure écrit le carnet sans toucher le passé", c2)

    def c3():
        """C3. ① RÔLE — idempotence. ② CONTEXTE D'APPEL — `cas`, après C2. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE —
        C2 a tourné. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — relancer, comparer les octets.
        ⑦ UNITÉ — octets. ⑧ POURQUOI — une ligne par soir. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit (rien attendu).
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        r = etat["r"]
        avant = open(os.path.join(r, HISTO), "rb").read()
        code, out = mesurer(r)
        apres = open(os.path.join(r, HISTO), "rb").read()
        return code == 0 and avant == apres and "0 ecrite(s)" in out, "code %d, octets %s" % (
            code, "identiques" if avant == apres else "CHANGÉS")
    un("C3 relance sans effet", c3)

    def c4():
        """C4. ① RÔLE — E5 de v7-E4 retournée. ② CONTEXTE D'APPEL — `cas`, après C2. ③ ENTRÉE — —.
        ④ CONDITIONS D'ENTRÉE — C2 a écrit des empreintes. ⑤ SORTIE — DEUX valeurs. [rend: 2]
        ⑥ TRAITEMENT — ajouter deux lignes à la fiche (tp +9,0 % sous C5E10-QA-V1 ; note changée sous C5E10-OBS-V1),
        relancer. ⑦ UNITÉ — —. ⑧ POURQUOI — A-768 ②. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit sous le scénario.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        r = os.path.join(tempfile.mkdtemp(prefix="carnet_c4_"), "r")
        shutil.copytree(etat["r"], r)
        ct = le_contrat(r)   # n°83 lue au contrat (N3, 18-11-2026)
        f = os.path.join(r, ct.REGISTRE_DES_STRATEGIES)
        fiches = ct.fiches_du_registre(f)
        entete = list(next(iter(fiches.values())).keys())
        qa = fiches["C5E10-QA-V1"]
        obs = fiches["C5E10-OBS-V1"]
        assert qa["tp"].strip() == "+4.0%", "tp de C5E10-QA-V1 : %r (attendu +4.0%%, le cas E5)" % qa["tp"]
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=entete, lineterminator="\r\n")
        w.writerow(dict(qa, tp="+9.0%"))
        w.writerow(dict(obs, note=(obs.get("note") or "") + " — note changée par l'épreuve"))
        brut = open(f, "rb").read()
        open(f, "wb").write(brut + ("" if brut.endswith(b"\n") else "\r\n").encode() + buf.getvalue().encode())
        code, out = mesurer(r)
        rouges = [l for l in out.splitlines() if "MEME IDENTIFIANT, AUTRE EMPREINTE" in l]
        ok = code == 1 and rouges and "C5E10-QA-V1 : MEME IDENTIFIANT" in out and "C5E10-OBS-V1 : MEME IDENTIFIANT" not in out
        return ok, "code %d ; %s" % (code, (rouges[0][:260] if rouges else "aucun rouge d'empreinte"))
    un("C4 E5 de v7-E4 retournée : tp +9,0 % sous le même identifiant rougit", c4)

    def c5():
        """C5. ① RÔLE — en-tête étranger refusé. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — renommer une colonne de l'en-tête, relancer.
        ⑦ UNITÉ — octets. ⑧ POURQUOI — un désaccord se tranche, il ne se répare pas. ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — écrit sous un scénario. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        r, _reste, _s = scenario(copie, "c5")
        p = os.path.join(r, HISTO)
        b = open(p, "rb").read().replace(b",taux_reussite,", b",taux_de_reussite,", 1)
        open(p, "wb").write(b)
        code, out = mesurer(r)
        return code == 1 and open(p, "rb").read() == b and "ARRET" in out, "code %d, fichier %s" % (
            code, "intact" if open(p, "rb").read() == b else "CHANGÉ")
    un("C5 en-tête étranger : arrêt, rien d'écrit", c5)

    def c6():
        """C6. ① RÔLE — INCONNU dit, R-734. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — retirer le module des indicateurs, relancer.
        ⑦ UNITÉ — —. ⑧ POURQUOI — un calcul qui n'a pas tourné ne rend pas 0. ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — écrit sous un scénario. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        r, _reste, seance = scenario(copie, "c6")
        os.remove(os.path.join(r, "programmes", "MESURER_LES_INDICATEURS.py"))
        code, out = mesurer(r)
        _b, lignes = lire(r)
        neuves = [l for l in lignes if l["date_mesure"] == seance]
        ok = (code == 1 and len(neuves) == 4 and all(l["carnet_etat"].startswith("INCONNU : ") for l in neuves)
              and all(l["n_operations"] for l in neuves))
        return ok, "code %d, %d lignes, états %s" % (code, len(neuves), sorted({l.get("carnet_etat", "")[:40] for l in neuves}))
    un("C6 module absent : colonnes anciennes écrites, carnet INCONNU, code 1", c6)

    def c7():
        """C7. ① RÔLE — le cockpit ne casse pas. ② CONTEXTE D'APPEL — `cas`, après C2. ③ ENTRÉE — —.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — nourrir le générateur comme
        PUBLIER_LE_SITE (fichiers à plat, noms sans `claude_`), trois fois. ⑦ UNITÉ — —. ⑧ POURQUOI — le cockpit lit
        ce fichier chaque soir. ⑨ CE QUI CLOCHE — l'heure de fabrication est retirée avant comparaison.
        ⑩ EFFET — écrit sous des dossiers temporaires. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        def page(racine, histo_octets):
            """Fabrique la page. ① RÔLE — une page. ② CONTEXTE D'APPEL — c7. ③ ENTRÉE — racine, octets de
            l'historique. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs : code, page sans l'heure. [rend: 2]
            ⑥ TRAITEMENT — à plat, générer, lire. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —.
            ⑩ EFFET — écrit. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            plat = tempfile.mkdtemp(prefix="carnet_plat_")
            sortie = tempfile.mkdtemp(prefix="carnet_page_")
            for src, nom in les_entrees_du_site(racine):   # R-708 : la table de la publication (N2, 18-11-2026)
                shutil.copy2(os.path.join(racine, src), os.path.join(plat, nom))
            # l'historique copié par la table est REMPLACÉ par les octets du cas (après la copie, jamais avant)
            open(os.path.join(plat, os.path.basename(HISTO)), "wb").write(histo_octets)
            p = subprocess.run([sys.executable, "-B", os.path.join(racine, COCKPIT), plat, sortie], cwd=plat,
                               capture_output=True, text=True, timeout=DELAI)
            pages = glob.glob(os.path.join(sortie, "*.html"))
            texte = open(pages[0], encoding="utf-8").read() if len(pages) == 1 else ""
            return p.returncode, re.sub(r"\w{3} \d{2}-\d{2}-\d{4} \d{2}h\d{2}|\d{2}h\d{2}", "H", texte)
        r2 = etat["r"]
        sys.path.insert(0, os.path.join(copie, "programmes"))
        import CONTRATS_DES_FICHIERS as C
        _r, reste, _s = scenario(copie, "c7")
        ancien = ",".join(COLONNES_D_AVANT).encode() + b"\r\n" + reste
        allonge = ",".join(C.MESURE).encode() + b"\r\n" + reste
        ca, pa = page(r2, ancien)
        cb, pb = page(r2, allonge)
        cc, pc = page(r2, open(os.path.join(r2, HISTO), "rb").read())
        ok = ca == cb == cc == 0 and pa and pa == pb and pc
        return ok, "codes %d/%d/%d ; pages 27 colonnes et allongée %s ; page avec carnet %d caractères" % (
            ca, cb, cc, "identiques" if pa == pb else "DIFFÉRENTES", len(pc))
    un("C7 cockpit inchangé sur l'en-tête allongé, et vivant avec le carnet", c7)
    return res


def preparer(depot, sab):
    """Copie le dépôt (partiellement) et y applique un sabotage.
    ① RÔLE — une copie par lancement. ② CONTEXTE D'APPEL — le programme principal. ③ ENTRÉE — `depot`, `sab`.
    ④ CONDITIONS D'ENTRÉE — chaque cible existe UNE fois. ⑤ SORTIE — DEUX valeurs : dossier temporaire, copie.
    [rend: 2]
    ⑥ TRAITEMENT — `copier_la_base`, puis remplacer. ⑦ UNITÉ — —. ⑧ POURQUOI — une cible absente ne sabote rien.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit un dossier temporaire. ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="carnet_vraie_vie_")
    r = os.path.join(d, "r")
    copier_la_base(depot, r)
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(r, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, "%s : cible trouvée %d fois dans %s : %r" % (sab, t.count(a), f, a[:60])
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d, r


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--cas":
        _tmp = tempfile.mkdtemp(prefix="carnet_cas_")
        tempfile.tempdir = _tmp
        try:
            resultats = cas(os.path.abspath(sys.argv[2]))
        finally:
            tempfile.tempdir = None
            shutil.rmtree(_tmp, ignore_errors=True)
        for nom_du_cas, ok, detail in resultats:
            print(("  ok    " if ok else "  ÉCHEC ") + nom_du_cas + " — " + detail)
        print("FIN DES CAS : %d" % len(resultats))
        sys.exit(0 if all(ok for _, ok, _ in resultats) else 1)
    _args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not _args or not os.path.isfile(os.path.join(_args[0], MESURER)) or not os.path.isfile(os.path.join(_args[0], HISTO)):
        print(__doc__.split("① RÔLE")[0])
        sys.exit(2)
    DEPOT = os.path.abspath(_args[0])
    if "--saboter" in sys.argv:
        _choix = ["Z0"] + list(SABOTAGES)
    else:
        _choix = [_args[1]] if len(_args) > 1 else ["Z0"]
        if _choix[0] != "Z0" and _choix[0] not in SABOTAGES:
            print("%s N'EXISTE PAS dans SABOTAGES" % _choix[0])
            sys.exit(2)
    _faute = False
    for sab in _choix:
        t0 = time.time()
        try:
            d, r = preparer(DEPOT, sab)
        except AssertionError as e:
            print("%s NE S'APPLIQUE PLUS : CIBLE INTROUVABLE — %s" % (sab, e))
            sys.exit(2)
        try:
            p = subprocess.run([sys.executable, "-B", os.path.join(r, SOI), "--cas", r], cwd=r,
                               capture_output=True, text=True, timeout=DELAI * 8)
            code, out = p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            code, out = 124, "délai de %d s dépassé" % (DELAI * 8)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
        fin = ("FIN DES CAS : %d" % NOMBRE_DE_CAS) in out
        if sab == "Z0":
            bon = code == 0 and not echecs and fin
            print("Z0 dépôt tel quel : %s" % ("tout vert" if bon else "ROUGE (code %d)" % code))
            print("\n".join(l for l in out.splitlines() if l.strip()))
            if not fin:
                print("Z0 N'A PAS PU TOURNER JUSQU'AU BOUT")
                sys.exit(2)
        else:
            bon = code == 1 and bool(echecs) and fin
            print(("%s mord : %r" % (sab, echecs)) if bon else "%s NE MORD PAS : code %d · %s" % (
                sab, code, out.strip()[-600:]))
        print("   durée : %d s" % (time.time() - t0))
        sys.stdout.flush()
        _faute = _faute or not bon
    print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
    sys.exit(1 if _faute else 0)
