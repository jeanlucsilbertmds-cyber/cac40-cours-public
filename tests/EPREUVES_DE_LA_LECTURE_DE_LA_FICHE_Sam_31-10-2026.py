#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_LECTURE_DE_LA_FICHE — Sam 31-10-2026 18h44 (Paris)
EN ESSAI · Rôle : prouver que le juge des stratégies LIT la fiche avant de la jouer — ses seuils (une seule lecture),
son moment d'achat, les données qu'elle demande, ses filtres (affichés, jamais joués) — et qu'il refuse, avant de
jouer, un signal dont la sortie est mal formée. Et que l'épreuve a des dents. SIMULATION UNIQUEMENT.
(Le contrôle « le signal ne voit pas l'avenir » n'est plus dans le juge depuis la décision de Jean-Luc du 31-10-2026
à 21h15 : il vit dans tests/EPREUVES_DE_L_ARRIVEE_DES_SIGNAUX_Sam_31-10-2026.py.)
Quand l'appeler : avant toute livraison qui touche `pourcent`, `seuil_de_la_fiche`, `manques_du_jeu`, `porte_0`,
`jouer`, `SignalNomme`, `forme_du_signal` ou `main` de programmes/JUGE_DES_STRATEGIES.py,
`_seuils` de programmes/JUGER_SUR_8_CRITERES.py, `reglages_du_registre` de programmes/TENIR_LES_POSITIONS.py.

À QUOI ÇA SERT (version B du plan du circuit, § 8 « le plan du juge », points 2, 5, 7, 8, 9 ; 31-10-2026) :
  E1 (A-547) un stop sous 1 % écrit avec « % » est lu juste : la VRAIE fiche C1-004 (« -0.6% ») rend 0,006 et non
     0,6 ; C4-BOLL (« -0.8% ») 0,008 ; une fraction de la moulinette (« 0.005 ») reste 0,005 ;
  E2 (A-547 ④) un objectif écrit avec un signe moins, ou un stop avec un signe plus, est refusé par la porte 0 ;
     et (relecteur de la version B, D7) un seuil qui n'est pas un nombre fini et non nul (« nan% », « -inf% »,
     « 0% ») aussi ;
  E3 (A-548) les trois lectures n'en font qu'UNE : le juge à 8 critères et le programme du soir rendent pour
     C1-004 les mêmes seuils que le juge, et leurs fichiers ne portent plus de lecture du « % » à eux ;
  E3b (A-547) joué avec le signal C5, C1-004 sort enfin au stop (0 sortie au stop avant la correction) ;
  E4 (point 5) la case `entree` est lue : « CLOSE » (vraie fiche C1-004), « INTRADAY » (vraie fiche C2-001) et une
     case vide (vraie fiche C5-EI-PARAMS, sa PREMIÈRE ligne, gardée telle quelle comme historique depuis la ligne
     ajoutée de la décision n°53) sont refusées en le nommant, à la porte 0 ET par `jouer` ; « Open J+1 »,
     « OPEN_J+1 » et « DÉFAUT » passent ;
  E5 (point 9) la case `donnees_demandees` est lue : « consensus » (sur la vraie ligne C2-001), « cours + dates de
     résultats » et une case vide sont refusés en le nommant, à la porte 0 ET par `jouer` ; « cours » passe ;
  E6 (QJ-17, décisions de Jean-Luc du 31-10-2026 à 17h15 et 17h16) le juge écrit « filtres non joués : » suivi du
     texte de la colonne sous C5E10-QA-V1, sans « banques exclues (R-204) » ; dans le code du juge, la colonne
     `filtres` n'est lue que par `main` (affichée, jamais jouée) ;
  E7 (point 8, forme) une sortie de signal mal formée (pas une liste, sans « i », « i » booléen, négatif, hors de la
     série, en double, en recul, décimal) est refusée (`SignalRefuse`) ; le vrai signal C5 passe sur les 40 valeurs ;
     et (relecteur de la version B, D8) le même signal C5 rendu en rangs numpy (`np.int64`) passe, rendu en
     flottants (« 3.0 ») est refusé ;
  E8 (point 8, refus au jeu) dans le programme principal du juge, une fiche dont le module rend un rang négatif est
     « REFUSÉE AU JEU » (pas « EN ÉCHEC »), C5E10-QA-V1 est jugée ensuite, le code reste 0 ;
  E9 le calibrage du juge reste vert (100 opérations, 100/100 sorties identiques) et C5E10-QA-V1, C5E10-OBS-V1 et
     C5-EI-PARAMS rendent les opérations mesurées avant la version B. Pour C5-EI-PARAMS, c'est sa DERNIÈRE ligne,
     telle qu'elle est au registre : la ligne AJOUTÉE avec « DÉFAUT » dans sa case entree (décision de Jean-Luc du
     31-10-2026 à 22h26, n°53 : « sa case entree vide reçoit DÉFAUT, par une LIGNE AJOUTÉE au registre des
     stratégies, l'ancienne gardée telle quelle » ; « la dernière ligne ajoutée fait foi », n°83 du 01-11-2026) ; et
     le programme principal du juge la juge : 48 opérations (avant le 04-11-2026, l'épreuve écrivait elle-même
     « DÉFAUT » dans une copie de la fiche). Tant que le code de n°83 n'est pas fait (reporté après le premier
     jugement de C5), la porte 0 du juge liste encore l'ancienne ligne, refusée.

USAGE : python3 -B tests/EPREUVES_DE_LA_LECTURE_DE_LA_FICHE_Sam_31-10-2026.py <racine du dépôt> [--saboter | nom]
  sans option : Z0, le dépôt tel quel ; --saboter : Z0 puis chaque sabotage ; un nom de sabotage : celui-là seul.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins une épreuve ; 1 sinon ; 2 si une cible
de sabotage est introuvable (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; et par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque
  épreuve de tests/ depuis la racine avec la racine en argument. Ce programme se relance lui-même avec
  « --cas <copie> » pour jouer les épreuves dans une copie : ce mode n'est pas fait pour la main.
③ ENTRÉE — La racine du dépôt ; `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : le juge, le juge à 8 critères, le programme du soir, le module C5, le
  registre des stratégies avec ses colonnes `entree`, `filtres` et `donnees_demandees`, le fichier maître des cours,
  le référentiel, le golden, son témoin et le tableau des 100 trades.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par épreuve et par sabotage. [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① copier la racine dans un dossier temporaire (sans .git, etudes,
  caches) · ② appliquer le sabotage, en exigeant que sa cible existe une fois · ③ relancer ce programme en mode
  « --cas » sur la copie · ④ Z0 doit être vert, un sabotage doit faire échouer au moins une épreuve.
⑦ UNITÉ — Des fractions (0,006 vaut 0,6 %), des nombres d'opérations, des empreintes SHA-256 tronquées à 16.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction (R-731) : une épreuve qui reste verte quand on
  retire ce qu'elle teste est une décoration. Les cas réels (R-732) : les vraies fiches C1-004, C4-BOLL, C2-001,
  C5-EI-PARAMS, C5E10-QA-V1 et C5E10-OBS-V1 du registre, le vrai maître des cours.
⑨ CE QUI CLOCHE — ① Les empreintes figées de E9 ont été mesurées le 31-10-2026 sur le maître d'empreinte
  8898afb2b9d90b91 ; sur un autre maître, E9 le DIT et ne compare plus que les nombres d'opérations au calibrage.
  ② La propriété de E3 et de E6 lit le code sans l'exécuter : une lecture par un nom calculé lui échappe. ③ Si
  numpy manque sur la machine, E7 le dit et échoue (code 1, R-734) : le cas des rangs numpy n'a pas pu tourner.
⑩ EFFET — Écrit seulement dans des dossiers temporaires, effacés ; `-B` partout, aucun fichier compilé.
⑪ TERMINAISON — Sort lui-même. Chaque sous-processus a un délai ; un délai dépassé compte comme un échec.
  [sort: oui]
"""
import ast
import csv
import glob
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

JUGE = "programmes/JUGE_DES_STRATEGIES.py"
J8 = "programmes/JUGER_SUR_8_CRITERES.py"
SOIR = "programmes/TENIR_LES_POSITIONS.py"
C5 = "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"
CON = "programmes/CONTRATS_DES_FICHIERS.py"
# LE CHEMIN DU REGISTRE DES STRATÉGIES ET SA LECTURE vivent au contrat (n°83, 05-11-2026), jamais ici : pris dans le
# dépôt de ce fichier pour le chemin ; dans la COPIE éprouvée pour la lecture (`cas`), pour qu'un sabotage du contrat
# de la copie soit vu.
# Chargé sous un autre nom de module : le nom « CONTRATS_DES_FICHIERS » reste libre pour celui de la copie.
_sp = importlib.util.spec_from_file_location(
    "contrat_du_depot_de_l_epreuve", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), CON))
_contrat_du_depot = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_contrat_du_depot)
REGISTRE_DES_STRATEGIES = _contrat_du_depot.REGISTRE_DES_STRATEGIES
# Mesurées le 31-10-2026 à 18h40 sur la version A + L3 (commit b32cb4c), AVANT la version B, maître des cours
# d'empreinte 8898afb2b9d90b91 : nombre d'opérations et empreinte de la liste des opérations (json trié).
MAITRE_DE_LA_MESURE = "8898afb2b9d90b91"
AVANT = {"C5E10-QA-V1": (51, "564ccafa9527e254"), "C5E10-OBS-V1": (89, "cabc7102d02c9b35"),
         "C5-EI-PARAMS": (48, "1eb3d8510391f590")}
NOMBRE_DE_CAS = 10

SABOTAGES = {
    "Z0": [],
    # A-547 : le « % » ne décide plus, la lecture devine de nouveau sous 1
    "P1_pourcent_devine_meme_avec_le_signe": [(JUGE, "    if avec_signe_pourcent:\n        return v / 100\n", "")],
    # A-547 ④ : un objectif négatif passe
    "P2_signe_de_l_objectif_non_controle": [(JUGE, '    if champ == "tp" and debut == "-":\n', "    if False:\n")],
    # A-548 : le juge à 8 critères relit les pourcentages à sa façon
    "P3_J8_relit_a_sa_facon": [(J8, "    return juge.seuil_de_la_fiche(fiche, \"tp\"), juge.seuil_de_la_fiche(fiche, \"sl\")\n",
                                "    _l = lambda v: abs(float(str(v).replace(\"%\", \"\").replace(\",\", \".\").strip())) / 100.0\n"
                                "    return _l(fiche[\"tp\"]), _l(fiche[\"sl\"])\n")],
    # A-548 : le soir relit les pourcentages à sa façon (l'ancienne lecture du juge, qui devine sous 1)
    # (la cible a perdu un niveau d'indentation le 05-11-2026 : n°83, le soir lit les fiches au contrat, sans « with »)
    "P4_soir_relit_a_sa_facon": [(SOIR, "                sl = juge.seuil_de_la_fiche(x, \"sl\")\n",
                                  "                sl = abs(float(str(x[\"sl\"]).replace(\"%\", \"\")))\n"
                                  "                sl = sl / 100.0 if sl >= 1 else sl\n")],
    # point 5 : la case entree n'est plus lue
    # (cible reprise le 09-11-2026, bloc 3 : le lot S_kk, 2c12a8db, a confié la mise en forme de la case à cle_d_entree)
    "P5_entree_non_lue": [(JUGE, "    elif cle_d_entree(entree) not in ENTREES_JOUABLES:\n",
                           "    elif False:\n")],
    # point 5 : une case entree vide est jouée à l'ouverture
    "P6_entree_vide_acceptee": [(JUGE, "    if entree.lower() in VIDE:\n        manq.append(\"entree (aucun",
                                 "    if False:\n        manq.append(\"entree (aucun")],
    # points 5 et 9 : `jouer` joue une fiche que la porte aurait refusée
    "P7_jouer_ne_regarde_pas_la_fiche": [(JUGE, "    if _non_jouable:\n        raise ValueError(", "    if False:\n        raise ValueError(")],
    # point 9 : les données demandées ne sont plus confrontées à la liste fermée
    "P8_donnees_non_lues": [(JUGE, "        if absentes:\n", "        if False:\n")],
    # QJ-17 : la ligne des filtres disparaît
    "P9_filtres_non_affiches": [(JUGE, "        if _filtres.lower() not in VIDE:\n", "        if False:\n")],
    # QJ-17 : les filtres deviennent un refus (joués)
    "P10_filtres_joues": [(JUGE, "    donnees = (fiche.get(\"donnees_demandees\") or \"\").strip()\n",
                           "    if \"banques\" in (fiche.get(\"filtres\") or \"\"):\n        manq.append(\"filtre joué\")\n"
                           "    donnees = (fiche.get(\"donnees_demandees\") or \"\").strip()\n")],
    # point 8 : la forme de la sortie n'est plus contrôlée
    "P11_forme_non_controlee": [(JUGE, "        motif = forme_du_signal(resultat, len(serie))\n", "        motif = None\n")],
    # D7 : un seuil indéfini, infini ou nul repasse la porte
    "P15_seuil_non_fini_accepte": [(JUGE, "    if not (math.isfinite(v) and v > 0):\n", "    if False:\n")],
    # D8 : les rangs numpy redeviennent « mal formés »
    "P16_rang_numpy_refuse": [(JUGE, "not isinstance(i, numbers.Integral)", "not isinstance(i, int)")],
    # point 8 : un refus au jeu est compté comme une panne (EN ÉCHEC, code 1)
    "P14_refus_au_jeu_compte_en_echec": [(JUGE, "        except SignalRefuse as _refus_au_jeu:\n", "        except ZeroDivisionError as _refus_au_jeu:\n")],
    # n°83 (superviseur R-759 du 05-11-2026, défaut 3) : la lecture du contrat rend la PREMIÈRE ligne d'un identifiant
    # écrit deux fois au lieu de la dernière — E9 doit rougir (le juge rejuge l'ancienne ligne de C5-EI-PARAMS, refusée,
    # au lieu de la ligne ajoutée, 48 opérations)
    # (cible recâblée le 05-11-2026, tour court du superviseur R-759 de 09h05 : la fiche est désormais retirée puis
    # rangée à la place de sa dernière ligne ; le sabotage remet « la première écriture reste »)
    "P17_premiere_ligne_fait_foi": [(CON, "        fiches.pop(cle, None)        # la place de la fiche est celle de sa "
                                          "DERNIÈRE ligne (⑧)\n        fiches[cle] = ligne\n",
                                     "        fiches.setdefault(cle, ligne)\n")],
}


def lancer(copie, *arguments, delai=900):
    """Lance un programme Python dans la copie et rend son code et sa sortie.

    ① RÔLE — Un seul geste pour tous les lancements de programmes de la copie.
    ② CONTEXTE D'APPEL — E6, E8, E9 (le programme principal du juge) ; le programme principal (mode « --cas »).
    ③ ENTRÉE — `copie` : la racine de la copie · `arguments` : le programme et ses arguments · `delai` : en secondes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé), la sortie, erreurs comprises. [rend: 2]
    ⑥ TRAITEMENT — `python3 -B` depuis la racine de la copie.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Les programmes s'éprouvent tels qu'ils tournent, ligne de commande comprise.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ce que fait le programme lancé ; dans la copie seulement.
    ⑪ TERMINAISON — Rend la main ; borné par le délai. [sort: non]
    """
    try:
        r = subprocess.run([sys.executable, "-B"] + list(arguments), cwd=copie, capture_output=True, text=True,
                           timeout=delai)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 124, "délai de %d s dépassé" % delai


def empreinte_ops(ops):
    """Rend l'empreinte d'une liste d'opérations.

    ① RÔLE — Comparer deux listes d'opérations à l'octet près, champ par champ.
    ② CONTEXTE D'APPEL — E9.
    ③ ENTRÉE — `ops` : la liste rendue par `jouer`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux. [rend: 1]
    ⑥ TRAITEMENT — json trié, SHA-256, tronqué.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La même écriture que la mesure du 31-10-2026 qui a produit les empreintes de `AVANT`, et que
      tests/EPREUVES_DU_SIGNAL_NOMME_Ven_30-10-2026.py.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return hashlib.sha256(json.dumps(ops, sort_keys=True).encode()).hexdigest()[:16]


def charger(copie, chemin, nom):
    """Charge un programme de la copie comme module, et le rend.

    ① RÔLE — Appeler les fonctions du juge à 8 critères et du programme du soir sans lancer leur programme principal.
    ② CONTEXTE D'APPEL — E3.
    ③ ENTRÉE — `copie` · `chemin` : relatif à la copie · `nom` : le nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — `importlib`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les deux programmes gardent leur programme principal sous `if __name__ == "__main__"`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le premier niveau du fichier (définitions, `sys.path`).
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    sp = importlib.util.spec_from_file_location(nom, os.path.join(copie, chemin))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def ajouter_des_fiches_en_tete(copie, fiches):
    """Ajoute des fiches juste après l'en-tête du registre des stratégies de la copie.

    ① RÔLE — Poser dans la copie les fiches d'épreuve que le programme principal du juge jouera EN PREMIER.
    ② CONTEXTE D'APPEL — `cas`, une fois.
    ③ ENTRÉE — `copie` · `fiches` : des dictionnaires, complétés par les colonnes de l'en-tête.
    ④ CONDITIONS D'ENTRÉE — Le registre de la copie existe.
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — Lire l'en-tête, écrire les fiches juste après lui, fins de ligne CRLF comme le registre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le juge joue dans l'ordre du registre : une fiche refusée AVANT C5E10-QA-V1 prouve que le refus
      n'arrête pas les suivantes.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans le registre de la COPIE, jamais dans celui du dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import io
    p = os.path.join(copie, REGISTRE_DES_STRATEGIES)
    entete = next(csv.reader(open(p, encoding="utf-8-sig")))
    tampon = io.StringIO()
    w = csv.writer(tampon, lineterminator="\r\n")
    for f in fiches:
        w.writerow([f.get(c, "") for c in entete])
    brut = open(p, "rb").read().decode("utf-8")
    k = brut.index("\n") + 1
    with open(p, "w", encoding="utf-8", newline="") as h:
        h.write(brut[:k] + tampon.getvalue() + brut[k:])


def cas(copie):
    """Joue les épreuves E1 à E9 dans une copie, et rend la liste de leurs verdicts.

    ① RÔLE — Le cœur de l'épreuve : chaque cas dit vert ou rouge, avec ce qu'il a vu.
    ② CONTEXTE D'APPEL — Le mode « --cas » de ce programme, une fois par copie (Z0 ou un sabotage).
    ③ ENTRÉE — `copie` : la racine d'une copie du dépôt, éventuellement sabotée.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des (nom, réussi, détail). [rend: 1]
    ⑥ TRAITEMENT — ① lire le registre réel de la copie · ② E1 à E9 (E6 et E8 partagent un lancement du juge, fait
      après avoir posé en tête du registre une fiche au module « mal formé ») ; un cas qui lève compte comme échoué.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Écrit dans la copie (registre, un module d'épreuve) ; lance le juge de la copie.
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné. [sort: non]
    """
    res = []

    def un(nom, f):
        try:
            ok, detail = f()
        except (Exception, SystemExit) as e:
            ok, detail = False, "%s : %s" % (type(e).__name__, str(e)[:220])
        res.append((nom, bool(ok), detail))

    sys.path.insert(0, os.path.join(copie, "programmes"))
    os.chdir(copie)
    import JUGE_DES_STRATEGIES as B
    # LA LECTURE DU CONTRAT DE LA COPIE (n°83) : `lignes`, l'historique, toutes les lignes ; `par_id`, la fiche de
    # chaque identifiant, sa DERNIÈRE ligne
    import CONTRATS_DES_FICHIERS as contrat
    lignes = contrat.lignes_du_registre(REGISTRE_DES_STRATEGIES)
    par_id = contrat.fiches_du_registre(REGISTRE_DES_STRATEGIES)
    qa, obs = dict(par_id["C5E10-QA-V1"]), dict(par_id["C5E10-OBS-V1"])
    c1004, c4boll, c2001 = (dict(par_id[k]) for k in ("C1-004", "C4-BOLL", "C2-001"))
    # LA CASE VIDE, sur une vraie ligne : la PREMIÈRE ligne de C5-EI-PARAMS, gardée telle quelle comme historique
    # depuis la ligne ajoutée de la décision n°53 (`par_id` garde la dernière, celle qui porte « DÉFAUT »)
    eip = dict(next(x for x in lignes if x["id"] == "C5-EI-PARAMS" and not (x.get("entree") or "").strip()))
    mnemo = B.table_mnemoniques(B.trouver(".", "REFERENTIEL_VALEURS"))
    cours, lec = B.lire_par_le_lecteur(".", "donnees/cours_maitre.csv", mnemo)
    pos = B.charger_module(B.trouver(".", "MODULE_POSITIONS.py"), "pos")
    # une fiche jouable bâtie sur C1-004 : son signal, son univers, sa période, son moment d'achat et ses données sont
    # ceux de C5E10-QA-V1 ; ses SEUILS sont les siens (+1.0 % / -0.6 %)
    c1004_jouable = dict(c1004, **{k: qa[k] for k in ("module_signal", "fonction_signal", "reglages_signal", "univers",
                                                      "horizon", "periode", "entree", "donnees_demandees")})

    # ── E1 A-547 : un stop sous 1 % écrit avec « % » ──────────────────────────────────────────────────────────────
    def e1():
        vu = {"C1-004 sl « %s » -> 0,006" % c1004["sl"]: abs(B.seuil_de_la_fiche(c1004, "sl") - 0.006) < 1e-12,
              "C1-004 tp « %s » -> 0,01" % c1004["tp"]: abs(B.seuil_de_la_fiche(c1004, "tp") - 0.01) < 1e-12,
              "C4-BOLL sl « %s » -> 0,008" % c4boll["sl"]: abs(B.seuil_de_la_fiche(c4boll, "sl") - 0.008) < 1e-12,
              "C5E10-QA-V1 -> 0,04 / 0,025": (B.seuil_de_la_fiche(qa, "tp"), B.seuil_de_la_fiche(qa, "sl")) == (0.04, 0.025),
              "fraction de la moulinette 0.005 -> 0,005": B.pourcent("0.005") == 0.005,
              "porte 0 laisse passer C1-004 jouable": B.porte_0(c1004_jouable)[0]}
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E1 A-547 : la vraie fiche C1-004 (-0.6%) rend 0,006", e1)

    # ── E2 A-547 ④ : le signe ──────────────────────────────────────────────────────────────────────────────────────
    def e2():
        tp_neg = B.porte_0(dict(c1004_jouable, tp="-1.0%"))
        sl_pos = B.porte_0(dict(c1004_jouable, sl="+0.6%"))
        vu = {"objectif « -1.0% » refusé": (not tp_neg[0]) and any("tp mal signé" in m for m in tp_neg[1]),
              "stop « +0.6% » refusé": (not sl_pos[0]) and any("sl mal signé" in m for m in sl_pos[1]),
              "stop sans signe « 0.6% » accepté (convention A-548 non décidée)": B.porte_0(dict(c1004_jouable, sl="0.6%"))[0]}
        # D7 (relecteur de la version B, R09 A2) : les trois textes qu'il a vus passer la porte
        for champ, texte in (("sl", "nan%"), ("sl", "-inf%"), ("sl", "0%"), ("tp", "nan%"), ("tp", "0%")):
            ok0, manq, _b = B.porte_0(dict(c1004_jouable, **{champ: texte}))
            vu["%s « %s » refusé" % (champ, texte)] = (not ok0) and any("hors des bornes" in m for m in manq)
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E2 A-547 ④ et D7 : un objectif négatif, un stop positif, un seuil non fini ou nul est refusé", e2)

    # ── E3 A-548 : une seule lecture, appelée par les trois ────────────────────────────────────────────────────────
    def e3():
        m8 = charger(copie, J8, "j8_epreuve")
        ms = charger(copie, SOIR, "soir_epreuve")
        r_soir = ms.reglages_du_registre(copie)
        vu = {"J8 C1-004 = juge": m8._seuils(c1004) == (B.seuil_de_la_fiche(c1004, "tp"), B.seuil_de_la_fiche(c1004, "sl")),
              "soir C1-004 = juge": (r_soir["C1-004"]["tp"], r_soir["C1-004"]["sl"]) == (0.01, 0.006),
              "soir C5E10-QA-V1 = 0,04 / 0,025": (r_soir["C5E10-QA-V1"]["tp"], r_soir["C5E10-QA-V1"]["sl"]) == (0.04, 0.025)}
        # propriété : hors de `pourcent` du juge, aucun de ces trois fichiers ne retire lui-même le signe « % »
        hors = []
        for p in (JUGE, J8, SOIR):
            arbre = ast.parse(open(p, encoding="utf-8").read())
            permis = set()
            for n in ast.walk(arbre):
                if isinstance(n, ast.FunctionDef) and n.name == "pourcent" and p == JUGE:
                    permis |= {id(x) for x in ast.walk(n)}
            for n in ast.walk(arbre):
                if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "replace"
                        and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == "%"
                        and id(n) not in permis):
                    hors.append("%s:%d" % (p, n.lineno))
        appel = {p: "seuil_de_la_fiche" in open(p, encoding="utf-8").read() for p in (J8, SOIR)}
        vu["aucune lecture du « % » hors de pourcent"] = not hors
        vu["J8 et le soir appellent seuil_de_la_fiche"] = all(appel.values())
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + " · hors %s" % hors[:4]
    un("E3 A-548 : le juge à 8 critères et le soir lisent les seuils par le juge", e3)

    def e3b():
        ok0, _m, bornes = B.porte_0(c1004_jouable)
        ops, _ = B.jouer(c1004_jouable, cours, mnemo, B.signal_de_la_fiche(".", c1004_jouable), pos, periode=bornes, lecture=lec)
        sl = sum(1 for o in ops if o["motif"].startswith("SL"))
        return ok0 and sl > 0, "C1-004 (+1.0%% / -0.6%%) jouée avec le signal C5 : %d opérations, %d sorties au stop (0 avant A-547)" % (len(ops), sl)
    un("E3b A-547 : C1-004 sort au stop", e3b)

    # ── E4 point 5 : la case entree ────────────────────────────────────────────────────────────────────────────────
    def e4():
        def refus(f):
            ok, manq, _b = B.porte_0(f)
            return (not ok), manq
        vu = {}
        for nom, f, attendu in (("C1-004 « %s »" % c1004["entree"], dict(c1004_jouable, entree=c1004["entree"]), "moment d'achat non jouable"),
                                ("C2-001 « %s »" % c2001["entree"], dict(c1004_jouable, entree=c2001["entree"]), "moment d'achat non jouable"),
                                ("C5-EI-PARAMS « %s »" % eip["entree"], dict(eip), "aucun moment d'achat"),
                                ("« au plus haut »", dict(c1004_jouable, entree="au plus haut"), "moment d'achat non jouable")):
            r, manq = refus(f)
            vu["%s refusé à la porte" % nom] = r and any(attendu in m for m in manq)
            try:
                B.jouer(f, cours, mnemo, B.signal_de_la_fiche(".", qa), pos)
                vu["%s refusé par jouer" % nom] = False
            except ValueError as e:
                vu["%s refusé par jouer" % nom] = attendu in str(e)
        for v in ("Open J+1", "OPEN_J+1", "DÉFAUT"):
            vu["« %s » passe" % v] = not B.manques_du_jeu(dict(c1004_jouable, entree=v))
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E4 point 5 : la case entree est lue, refus nommé", e4)

    # ── E5 point 9 : la case donnees_demandees ─────────────────────────────────────────────────────────────────────
    def e5():
        base = dict(c2001, **{k: qa[k] for k in ("module_signal", "fonction_signal", "reglages_signal", "univers",
                                                 "horizon", "periode", "entree", "tp", "sl")})
        vu = {}
        for nom, valeur, attendu in (("consensus (C2-001)", "consensus", "donnée absente : consensus"),
                                     ("cours + dates de résultats", "cours + dates de résultats", "donnée absente : dates de résultats"),
                                     ("vide", "", "aucune donnée déclarée")):
            f = dict(base, donnees_demandees=valeur)
            ok, manq, _b = B.porte_0(f)
            vu["%s refusé à la porte" % nom] = (not ok) and any(attendu in m for m in manq)
            try:
                B.jouer(f, cours, mnemo, B.signal_de_la_fiche(".", qa), pos)
                vu["%s refusé par jouer" % nom] = False
            except ValueError as e:
                vu["%s refusé par jouer" % nom] = attendu in str(e)
        vu["« cours » passe"] = B.porte_0(dict(base, donnees_demandees="cours"))[0]
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E5 point 9 : la case donnees_demandees est lue, refus nommé", e5)

    # ── le lancement du juge partagé par E6, E8 et E9 : une fiche « mal formée » en tête du registre ──────────────
    module_mal_forme = "programmes/EPREUVE_SIGNAL_MAL_FORME.py"
    open(module_mal_forme, "w", encoding="utf-8").write(
        '"""EN ESSAI · module de signal · Rôle : module d\'épreuve qui rend un rang NÉGATIF (sortie mal formée).\n"""\n'
        "def signaux(ohlcv):\n"
        "    return [{\"i\": -1}] if ohlcv else []\n")
    ajouter_des_fiches_en_tete(copie, [dict(qa, id="AAA-EPREUVE-MAL-FORME", nom="EPREUVE signal qui rend un rang negatif",
                                            etat_vie="LABO", module_signal=module_mal_forme, fonction_signal="signaux",
                                            reglages_signal="")])
    code_j, sortie_j = lancer(copie, JUGE, ".")
    os.remove(module_mal_forme)

    # ── E6 QJ-17 : les filtres affichés, jamais joués ──────────────────────────────────────────────────────────────
    def e6():
        """Le cas E6 : les filtres affichés, jamais joués (QJ-17).

        ① RÔLE — Voir l'en-tête, E6. ② CONTEXTE D'APPEL — `un`, dans `cas`, une fois. ③ ENTRÉE — Par fermeture :
        `sortie_j`, `qa`, le contrat de la copie. ④ CONDITIONS D'ENTRÉE — Le juge a tourné. ⑤ SORTIE — DEUX valeurs :
        réussi, détail. [rend: 2] ⑥ TRAITEMENT — ① la ligne « filtres non joués » sous C5E10-QA-V1 · ② les fiches
        C5E10-QA-V1 et C5E10-OBS-V1, lues par `fiches_du_registre` du contrat (n°83, 05-11-2026), sans « banques
        exclues (R-204) » · ③ dans le code du juge, la colonne `filtres` lue par `main` seul. ⑦ UNITÉ — —. ⑧ POURQUOI —
        Décisions de Jean-Luc du 31-10-2026 à 17h15 et 17h16. ⑨ CE QUI CLOCHE — La propriété ③ lit le code sans
        l'exécuter (⑨ ② de l'en-tête). ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
        """
        bloc = sortie_j.split("=== C5E10-QA-V1", 1)[1].split("===", 1)[0] if "=== C5E10-QA-V1" in sortie_j else ""
        lu = [x for x in contrat.fiches_du_registre(REGISTRE_DES_STRATEGIES).values() if x["id"] in ("C5E10-QA-V1", "C5E10-OBS-V1")]
        arbre = ast.parse(open(JUGE, encoding="utf-8").read())
        lecteurs = set()
        for fn in (n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)):
            for n in ast.walk(fn):
                if isinstance(n, ast.Constant) and n.value == "filtres":
                    lecteurs.add(fn.name)
        vu = {"ligne « filtres non joués : %s »" % qa["filtres"]: ("filtres non joués : %s" % qa["filtres"]) in bloc,
              "C5E10-QA-V1 et C5E10-OBS-V1 sans « banques exclues (R-204) »": len(lu) == 2 and all("banques exclues (R-204)" not in x["filtres"] for x in lu),
              "le reste de la case gardé": len(lu) == 2 and all(re.search(r"r[eè]gles pr[eé]-trade R-301", x["filtres"]) for x in lu),
              "filtres lus par main seule (%s)" % sorted(lecteurs): lecteurs == {"main"}}
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E6 QJ-17 : « filtres non joués » à chaque verdict, jamais joués", e6)

    # ── E7 point 8 : la forme de la sortie ─────────────────────────────────────────────────────────────────────────
    def e7():
        serie = cours[next(v for v in sorted(cours))]
        n = len(serie)
        fautifs = {"pas une liste": lambda s: ({"i": 3},),
                   "sans « i »": lambda s: [{"rang": 3}],
                   "i booléen": lambda s: [{"i": True}],
                   "i négatif": lambda s: [{"i": -1}],
                   "i hors de la série": lambda s: [{"i": len(s)}],
                   "i en double": lambda s: [{"i": 3}, {"i": 3}],
                   "i en recul": lambda s: [{"i": 5}, {"i": 3}],
                   "i décimal": lambda s: [{"i": 3.0}]}
        sig = B.signal_de_la_fiche(".", qa)
        # D8 (relecteur de la version B, R09 A5) : le VRAI signal C5, rendu en flottants entiers, reste refusé
        fautifs["C5 en flottants entiers"] = lambda s: [{"i": float(x["i"])} for x in sig.fonction(s)]
        vu = {}
        for nom, fn in fautifs.items():
            try:
                B.SignalNomme(fn, {}, "épreuve : " + nom)(serie)
                vu[nom + " refusé"] = False
            except B.SignalRefuse as e:
                vu[nom + " refusé"] = "mal formée" in str(e)
        total = 0
        for v in sorted(cours):
            total += len(sig(cours[v]))
        vu["C5 passe sur les %d valeurs (%d signaux)" % (len(cours), total)] = total > 0
        # D8 : le même signal C5, ses rangs rendus en entiers numpy, passe et rend les mêmes rangs
        try:
            import numpy as np
        except ImportError:
            vu["numpy présent (sinon ce cas n'a pas pu tourner, R-734)"] = False
        else:
            en_numpy = B.SignalNomme(lambda s: [{"i": np.int64(x["i"])} for x in sig.fonction(s)], {}, "épreuve : C5 en numpy")
            pareils = all([int(x["i"]) for x in en_numpy(cours[v])] == [x["i"] for x in sig(cours[v])] for v in sorted(cours))
            vu["C5 en rangs numpy (np.int64) passe, mêmes rangs"] = pareils
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + " · série de %d séances" % n
    un("E7 point 8 : une sortie mal formée est refusée, C5 passe", e7)

    # ── E8 point 8 : le refus au jeu ───────────────────────────────────────────────────────────────────────────────
    def e8():
        vu = {}
        bloc = sortie_j.split("=== AAA-EPREUVE-MAL-FORME", 1)[1].split("===", 1)[0] if "=== AAA-EPREUVE-MAL-FORME" in sortie_j else ""
        vu["juge : la fiche mal formée REFUSÉE AU JEU"] = "REFUSÉE AU JEU" in bloc and "mal formée" in bloc
        vu["juge : pas EN ÉCHEC"] = "EN ÉCHEC" not in sortie_j
        vu["juge : C5E10-QA-V1 jugée ensuite"] = re.search(r"=== C5E10-QA-V1 .*\n(?:.*\n){0,3}?\s+51 operations", sortie_j) is not None
        vu["juge : code 0"] = code_j == 0
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + " · code %d" % code_j
    un("E8 point 8 : un signal mal formé est REFUSÉ AU JEU, pas EN ÉCHEC", e8)

    # ── E9 le calibrage et les opérations de C5 ────────────────────────────────────────────────────────────────────
    def e9():
        """Le cas E9 : le calibrage du juge reste vert, et les trois fiches C5 rendent les opérations d'avant.

        ① RÔLE — Voir l'en-tête, E9. ② CONTEXTE D'APPEL — `un`, dans `cas`, une fois. ③ ENTRÉE — Par fermeture :
        `sortie_j` (la sortie du programme principal du juge sur la copie), `par_id` (la dernière ligne de chaque
        identifiant du registre de la copie), `cours`, `mnemo`, `lec`, `pos`. ④ CONDITIONS D'ENTRÉE — Le juge a tourné.
        ⑤ SORTIE — DEUX valeurs : réussi (booléen) et le détail. [rend: 2] ⑥ TRAITEMENT — ① les quatre lignes du
        calibrage dans `sortie_j` · ② l'ancienne ligne de C5-EI-PARAMS refusée, la ligne ajoutée (n°53) jugée à 48
        opérations · ③ chaque fiche de `AVANT`, prise telle qu'elle est au registre (dernière ligne), passe la porte 0
        et rend le même nombre d'opérations, et la même empreinte si le maître est celui de la mesure. ⑦ UNITÉ — Des
        opérations. ⑧ POURQUOI — Décision n°53 (31-10-2026, 22h26) : C5-EI-PARAMS reçoit « DÉFAUT » par une ligne
        ajoutée, et doit rendre ses 48 opérations d'avant ; la jouer telle qu'au registre (et non plus avec un
        « DÉFAUT » écrit par l'épreuve) fait rougir ce cas si la ligne est retirée (mesuré le 04-11-2026). ⑨ CE QUI
        CLOCHE — « 48 operations » est cherché à trois lignes au plus du titre « === C5-EI-PARAMS » : une mise en page
        du juge qui l'éloignerait ferait rougir à tort. ⑩ EFFET — Joue le juge en mémoire. ⑪ TERMINAISON — Rend la
        main. [sort: non]
        """
        maitre = hashlib.sha256(open("donnees/cours_maitre.csv", "rb").read()).hexdigest()[:16]
        vu = {"calibrage : 100 opérations": re.search(r"n   : obtenu 100 \. attendu 100 \. OK", sortie_j) is not None,
              "calibrage : 100/100 sorties": "sorties : 100/100 identiques" in sortie_j,
              "calibrage : OK": "-> OK, l'instrument est calibre." in sortie_j,
              # n°83 (05-11-2026) : l'ancienne ligne n'est plus jugée — une fiche par identifiant, sa dernière ligne
              "l'ancienne ligne de C5-EI-PARAMS n'est plus jugée (n°83)": re.search(r"C5-EI-PARAMS refusee", sortie_j) is None,
              # décision n°53 : la ligne ajoutée (« DÉFAUT ») est jugée par le programme principal du juge
              "C5-EI-PARAMS jugée par le juge, 48 opérations (ligne ajoutée, n°53)":
                  re.search(r"=== C5-EI-PARAMS .*\n(?:.*\n){0,3}?\s+48 operations", sortie_j) is not None}
        d = []
        for ident, (n_avant, e_avant) in AVANT.items():
            f = dict(par_id[ident])     # la DERNIÈRE ligne de chaque identifiant (n°83) ; C5-EI-PARAMS : la ligne de n°53
            ok0, _m, bornes = B.porte_0(f)
            ops, _ = B.jouer(f, cours, mnemo, B.signal_de_la_fiche(".", f), pos, periode=bornes, lecture=lec)
            bon = ok0 and len(ops) == n_avant
            if maitre == MAITRE_DE_LA_MESURE:
                bon = bon and empreinte_ops(ops) == e_avant
            vu["%s %d op %s" % (ident, len(ops), empreinte_ops(ops))] = bon
        if maitre != MAITRE_DE_LA_MESURE:
            d.append("maître %s, pas celui de la mesure (%s) : nombres d'opérations seulement" % (maitre, MAITRE_DE_LA_MESURE))
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()) + " ".join(d)
    un("E9 le calibrage reste vert, les fiches C5 rendent les mêmes opérations", e9)
    return res


def preparer(depot, sab):
    """Copie le dépôt et y applique un sabotage.

    ① RÔLE — Donner à chaque sabotage sa copie, pour que rien ne touche au dépôt.
    ② CONTEXTE D'APPEL — Le programme principal, une fois par sabotage joué.
    ③ ENTRÉE — `depot` : la racine · `sab` : le nom du sabotage.
    ④ CONDITIONS D'ENTRÉE — Chaque cible du sabotage existe UNE fois dans son fichier.
    ⑤ SORTIE — DEUX valeurs : le dossier temporaire et la racine de la copie. [rend: 2]
    ⑥ TRAITEMENT — ① copier sans .git, etudes, caches · ② remplacer chaque cible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une cible introuvable ne sabote rien : elle lève au lieu de passer pour un sabotage qui mord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un dossier temporaire (dans TMPDIR s'il est posé).
    ⑪ TERMINAISON — Rend la main, ou lève AssertionError. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="lecture_fiche_")
    r = os.path.join(d, "r")
    shutil.copytree(depot, r, ignore=shutil.ignore_patterns(".git", "etudes", "__pycache__", "_site_travail"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(r, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, "%s : cible trouvée %d fois dans %s : %r" % (sab, t.count(a), f, a[:60])
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d, r


if len(sys.argv) > 2 and sys.argv[1] == "--cas":
    resultats = cas(os.path.abspath(sys.argv[2]))
    for nom, ok, detail in resultats:
        print(("  ok    " if ok else "  ÉCHEC ") + nom + " — " + detail)
    # LE MARQUEUR DE FIN : sans lui, une épreuve interrompue (sortie silencieuse) ne passe ni pour verte ni pour mordue
    print("FIN DES CAS : %d" % len(resultats))
    sys.exit(0 if all(ok for _, ok, _ in resultats) else 1)

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not _args:
    print(__doc__.split("① RÔLE")[0])
    sys.exit(2)
DEPOT = os.path.abspath(_args[0])
_choix = list(SABOTAGES) if "--saboter" in sys.argv else [_args[1]] if len(_args) > 1 else ["Z0"]
_faute = False
for sab in _choix:
    try:
        d, r = preparer(DEPOT, sab)
    except AssertionError as e:
        print("== %s : CIBLE INTROUVABLE — %s" % (sab, e))
        sys.exit(2)
    try:
        code, out = lancer(r, os.path.abspath(__file__), "--cas", r, delai=1200)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
    if sab == "Z0":
        bon = code == 0 and not echecs and "FIN DES CAS : %d" % NOMBRE_DE_CAS in out
        print("== Z0 dépôt tel quel : %s" % ("tout vert" if bon else "ROUGE (code %d)" % code))
        print("\n".join(l for l in out.splitlines() if l.strip()))
    else:
        bon = code == 1 and bool(echecs) and "FIN DES CAS : %d" % NOMBRE_DE_CAS in out
        print("== %s : %s" % (sab, ("mord (" + " · ".join(echecs) + ")") if bon else
                                    "NE MORD PAS (code %d) %s" % (code, out.strip()[-300:])))
    _faute = _faute or not bon
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
