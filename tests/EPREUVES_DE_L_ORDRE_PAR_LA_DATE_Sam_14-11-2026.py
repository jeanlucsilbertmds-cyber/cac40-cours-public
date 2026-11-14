#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_ORDRE_PAR_LA_DATE — Sam 14-11-2026 (Paris)

À QUOI ÇA SERT. Le cockpit lisait la PLACE d'une ligne de donnees/cac40_strategies.csv comme une date : une ligne
ajoutée à une fiche la rangeait « en dernier ». Mesuré par le relecteur de la branche v7-E4 (D2) : la carte QA
passait de C5E10-OBS-V1 à C5E10-QA-V1 sans qu'aucun réglage ait changé, et C1-002, archivée en mars 2026, entrait
dans « les 6 dernières archivées ». Décision de Jean-Luc du 14-11-2026 à 11h35 : « le cockpit est complètement
débile, il ne lit pas la date, mais il lit le positionnement, c'est ça? […] C'est donc ça qu'il faut corriger,
non? ». L'ordre d'affichage vient désormais de la case `date_entree_etat`, lue par `date_d_entree_dans_l_etat` et
`ranger_par_date_d_entree` de programmes/CONTRATS_DES_FICHIERS.py ; la VALEUR d'une fiche reste sa dernière ligne
(n°83). Ces épreuves le prouvent, et leur sabotage prouve qu'elles rougissent quand on remet l'ancien défaut.

LANCEMENT : python3 -B tests/EPREUVES_DE_L_ORDRE_PAR_LA_DATE_Sam_14-11-2026.py <racine> [--saboter]
  Sans option : les épreuves sur le code de <racine>. Code 0 si toutes vertes, 1 sinon.
  --montrer-l-ordre : affiche, sur le vrai registre, l'ordre AVANT (par la place) et APRÈS (par la date), puis sort.
  --saboter : les épreuves, puis chaque sabotage sur une COPIE de <racine>/programmes dans un dossier temporaire ;
  chaque sabotage doit rendre au moins une épreuve rouge. Un sabotage dont le texte n'est pas trouvé, ou qui laisse
  tout vert, rend le code 1 (R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0).

LES ÉPREUVES (registre = une copie en mémoire du VRAI donnees/cac40_strategies.csv de <racine>) :
  E1 D2, carte QA : une ligne ajoutée à C5E10-QA-V1 (copie de sa dernière ligne, objectif passé à +6.0 %) ; la
     carte QA reste C5E10-OBS-V1 (entrée le 2026-08-11 contre 2026-07-27).
  E2 n°83 intact : dans le même registre, la fiche C5E10-QA-V1 porte l'objectif +6.0 % de sa dernière ligne.
  E3 D2, cas réel C1-002 : sept archivées reçoivent une date (C1-002 le 2026-03-28, six autres en avril 2026),
     puis une ligne ajoutée à C1-002 ; C1-002 n'est pas parmi les plus récentes montrées.
  E4 vraies données : la carte QA est C5E10-OBS-V1 sans signalement ; Production ne rend rien ; les 30 archivées,
     toutes sans date, sont NOMMÉES dans un signalement et aucun tableau n'est composé.
  E5 lecture des dates : formes réelles acceptées (« 2026-08-11 », « Dim_12-07-2026_18h22 ») ; refusées et
     signalées : vide, « 12/07/2026 », « 2026-13-01 », « Lun_12-07-2026_18h22 » (jour faux),
     « Dim_12-07-2026_25h00 », « 2026-08-11 » précédée d'une espace.
  E6 ex aequo en tête : deux fiches QA entrées le même jour → aucune carte, un signalement qui les nomme toutes deux.
  E7 ex aequo à la sixième place : sept archivées dont la 6e et la 7e entrées le même jour → les sept sont montrées.
  E8 sans date en QA : une fiche QA sans date à côté d'une fiche datée → la datée est retenue, la sans date nommée.
  E9 (tour 2, relecteur D1) la PAGE montre les signalements, par `bloc_strategie`, dans ses trois formes : ① ex aequo
     en tête (aucune carte) · ② seule fiche QA sans date (aucune carte) · ④ une fiche datée sans aucune mesure ET une
     fiche QA sans date (« Aucun indicateur ») · ③ une fiche datée avec ses mesures réelles ET une fiche QA sans date
     (section complète) — le nom de chaque fiche signalée est sur la page.
  E10 (tour 2, relecteur D2) la PHRASE d'en-tête des archives dit vrai : sur les vraies données, « aucune ne porte
     de date d entree lisible » ; sur le cas E7, « 7 datee(s), les 7 plus recentes ».
  E11 (tour 2, relecteur D4) une archivée s'écrit « id · nom » dans le tableau ET dans la liste des sans date.

LES SABOTAGES (chacun doit faire rougir l'épreuve nommée entre parenthèses, sinon code 1 ; ils ne sont lancés que
si toutes les épreuves sont vertes sur le code non saboté) : S1 la carte reprend la dernière ligne de la liste (E1) · S2 les archives
reprennent les six dernières de la liste (E3) · S3 le rangement passe du plus ancien au plus récent (E1, E4) · S4
une date vide est rangée comme une date (E4) · S5 le jour de la semaine n'est plus vérifié (E5) · S6 un ex aequo en
tête choisit la première fiche (E6) · S7 les archives sont coupées à six exactement (E7) · S8 la valeur d'une fiche
redevient sa PREMIÈRE ligne (E2) · S9 les trois `alerte + ` retirés de `bloc_strategie`, puis S9a, S9b, S9c chacun
seul (E9) · S10 la phrase « aucune
datée » remplacée par « les 6 dernieres : » (E10) · S11 le compte des montrées remplacé par 6 (E10) · S12 la liste
des sans date reprend l'id seul (E11).
"""
import csv, importlib.util, io, os, shutil, subprocess, sys, tempfile

COCKPIT = "GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py"
CONTRAT = "CONTRATS_DES_FICHIERS.py"

SABOTAGES = {
    "S1_carte_par_la_place": ("E1", COCKPIT,
        "    return (groupes[0][1][0] if groupes else None), signalements\n",
        "    return (lignes[-1] if lignes else None), []\n"),
    "S2_archives_par_la_place": ("E3", COCKPIT,
        "    groupes, sans_date = _contrat_ordre.ranger_par_date_d_entree(archivees)\n",
        "    groupes, sans_date = [('?', archivees[-6:])], []\n"),
    "S3_ordre_croissant": ("E1", CONTRAT,
        "for jour in sorted(par_jour, reverse=True)], sans_date",
        "for jour in sorted(par_jour)], sans_date"),
    "S4_vide_range": ("E4", CONTRAT,
        "        if jour is None:\n            sans_date.append((fiche, raison))\n        else:\n"
        "            par_jour.setdefault(jour, []).append(fiche)\n",
        "        par_jour.setdefault(jour or '', []).append(fiche)\n"),
    "S5_jour_non_verifie": ("E5", CONTRAT,
        "    if jour_ecrit is not None and _JOURS_DE_LA_SEMAINE[d.weekday()] != jour_ecrit:\n",
        "    if False:\n"),
    "S6_ex_aequo_choisi": ("E6", COCKPIT,
        "    if groupes and len(groupes[0][1]) > 1:\n",
        "    if False:\n"),
    "S7_coupe_a_six": ("E7", COCKPIT,
        "        montrees += [(jour, f) for f in fiches]\n",
        "        montrees += [(jour, f) for f in fiches][:6 - len(montrees)]\n"),
    "S8_premiere_ligne": ("E2", CONTRAT,
        "        fiches.pop(cle, None)        # la place de la fiche est celle de sa DERNIÈRE ligne (⑧)\n"
        "        fiches[cle] = ligne\n",
        "        fiches.setdefault(cle, ligne)\n"),
    "S9_alerte_retiree_partout": ("E9", COCKPIT, "alerte + ", "", 3),
    "S9a_alerte_retiree_sans_carte": ("E9", COCKPIT, "return (alerte + f'<div style=\"font-size:15px", "return (f'<div style=\"font-size:15px"),
    "S9b_alerte_retiree_sans_mesure": ("E9", COCKPIT, "return (alerte + f'<div style=\"font-size:12px", "return (f'<div style=\"font-size:12px"),
    "S9c_alerte_retiree_section_complete": ("E9", COCKPIT, "return alerte + entete", "return entete"),
    "S10_entete_mensongere": ("E10", COCKPIT,
        "aucune ne porte de date d entree '\n                       f'lisible : les plus recentes ne peuvent pas etre montrees.",
        "les 6 dernieres : '\n                       f'"),
    "S11_compte_fixe": ("E10", COCKPIT, "f'les {len(montrees)} plus recentes", "f'les 6 plus recentes"),
    "S12_sans_date_par_l_id": ("E11", COCKPIT,
        "esc(', '.join(f\"{nom_de_fiche(f)} ({raison})\"", "esc(', '.join(f\"{f.get('id')} ({raison})\""),
}


def charger(dossier_programmes):
    """Charge le contrat et le cockpit d'un dossier `programmes`.

    ① RÔLE — Donner aux épreuves le code à éprouver : celui de la racine, ou celui d'une copie sabotée.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par lancement.
    ③ ENTRÉE — `dossier_programmes` : le chemin d'un dossier qui porte les deux programmes et programmes/COMMUN.py.
    ④ CONDITIONS D'ENTRÉE — Les deux fichiers existent ; aucun module du même nom n'est déjà chargé.
    ⑤ SORTIE — DEUX valeurs : le module du contrat, le module du cockpit.
      [rend: 2]
    ⑥ TRAITEMENT — ① mettre le dossier en tête du chemin de recherche · ② importer le contrat · ③ importer le
      cockpit par son chemin (son nom porte des tirets).
    ⑦ UNITÉ — Des modules Python.
    ⑧ POURQUOI — Le cockpit importe le contrat par son nom : le dossier doit être en tête pour qu'une copie
      sabotée soit celle qui est lue.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut des deux modules (aucune écriture : le cockpit n'écrit que dans `main`).
    ⑪ TERMINAISON — Rend la main ; lève si un import échoue, et `main` rend alors 1.
      [sort: non]
    """
    sys.path.insert(0, dossier_programmes)
    import CONTRATS_DES_FICHIERS as contrat
    spec = importlib.util.spec_from_file_location("cockpit_eprouve", os.path.join(dossier_programmes, COCKPIT))
    cockpit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cockpit)
    return contrat, cockpit


def epreuves(racine, dossier_programmes):
    """Lance les huit épreuves E1 à E8 et rend leurs verdicts.

    ① RÔLE — Prouver que l'ordre d'affichage vient de la date d'entrée et que la valeur d'une fiche reste sa
      dernière ligne (voir l'en-tête du fichier).
    ② CONTEXTE D'APPEL — `main`, une fois ; en sabotage, une fois par copie sabotée (sous-processus).
    ③ ENTRÉE — `racine` : le dépôt dont on lit le VRAI registre · `dossier_programmes` : le code éprouvé.
    ④ CONDITIONS D'ENTRÉE — `<racine>/donnees/cac40_strategies.csv` existe et porte C5E10-QA-V1, C5E10-OBS-V1, C1-002.
    ⑤ SORTIE — UNE valeur : une liste de triplets (nom, vert ?, détail).
      [rend: 1]
    ⑥ TRAITEMENT — ① charger le code · ② lire le vrai registre en lignes · ③ pour chaque épreuve, fabriquer en
      mémoire les lignes voulues, les ranger en fiches par le contrat, appeler le cockpit, comparer.
    ⑦ UNITÉ — Des fiches ; des dates AAAA-MM-JJ.
    ⑧ POURQUOI — Chaque cas part d'une VRAIE ligne du registre (R-732), et E4 tourne sur le registre tel quel.
    ⑨ CE QUI CLOCHE — E3 et E7 donnent des dates à des archivées qui n'en ont pas : ce sont des cas fabriqués à
      partir de vraies lignes, pas l'état du registre.
    ⑩ EFFET — Lit le registre ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; une exception d'une épreuve est rattrapée et rend cette épreuve rouge.
      [sort: non]
    """
    contrat, cockpit = charger(dossier_programmes)
    with open(contrat.chemin_du_registre(racine), encoding="utf-8", newline="") as f:
        reel = list(csv.DictReader(f))
    derniere = {l["id"]: l for l in reel}

    def fiches(lignes):
        return list(contrat.fiches_des_lignes(lignes).values())

    def en_etat(fs, mot):
        return [s for s in fs if (s.get("etat_vie") or s.get("statut") or "").strip().upper().startswith(mot)]

    class S:
        mesures = []

    def surveillance(fs):
        S.strategies = fs
        return cockpit.bloc_surveillance(S)

    def montrees(page):
        tableau = page.split("Archivee le", 1)[1].split("⚠", 1)[0] if "Archivee le" in page else ""
        return tableau

    res = []

    def ep(nom, fonction):
        try:
            ok, detail = fonction()
        except Exception as e:                      # une épreuve qui lève est rouge, jamais muette
            ok, detail = False, f"{type(e).__name__}: {e}"
        res.append((nom, ok, detail))

    def e1():
        ajout = dict(derniere["C5E10-QA-V1"], tp="+6.0%")
        carte, sig = cockpit.carte_strategie(fiches(reel + [ajout]), "QA")
        return (carte or {}).get("id") == "C5E10-OBS-V1", f"carte QA = {(carte or {}).get('id')}"
    ep("E1 ligne ajoutée à C5E10-QA-V1 : la carte QA reste C5E10-OBS-V1", e1)

    def e2():
        ajout = dict(derniere["C5E10-QA-V1"], tp="+6.0%")
        f = contrat.fiches_des_lignes(reel + [ajout])["C5E10-QA-V1"]
        return f.get("tp") == "+6.0%", f"tp de la fiche = {f.get('tp')}"
    ep("E2 n°83 : la fiche C5E10-QA-V1 porte la valeur de sa dernière ligne", e2)

    def e3():
        dates = {"C1-002": "2026-03-28", "C3-001": "2026-04-01", "C4-RAV": "2026-04-02", "C5-EI": "2026-04-03",
                 "C1-001": "2026-04-04", "C1-003": "2026-04-05", "C1-004": "2026-04-06"}
        lignes = [dict(l, date_entree_etat=dates.get(l["id"], l["date_entree_etat"])) for l in reel]
        lignes.append(dict(lignes[[l["id"] for l in lignes].index("C1-002")], note="ligne de jugement ajoutée"))
        t = montrees(surveillance(fiches(lignes)))
        vu = lambda i: cockpit.esc(cockpit.nom_de_fiche(derniere[i])) in t
        return (not vu("C1-002") and vu("C1-004"), f"C1-002 montrée : {vu('C1-002')} ; C1-004 montrée : {vu('C1-004')}")
    ep("E3 C1-002 (mars 2026) reçoit une ligne : elle n'entre pas parmi les plus récentes", e3)

    def e4():
        fs = fiches(reel)
        carte, sig = cockpit.carte_strategie(fs, "QA")
        prod, sigp = cockpit.carte_strategie(fs, "PRODUCTION")
        page = surveillance(fs)
        arch = [s for s in fs if "ARCHIV" in (s.get("statut", "") + s.get("etat_vie", "")).upper()]
        nommees = all(cockpit.esc(cockpit.nom_de_fiche(s)) + " (VIDE)" in page for s in arch)
        ok = ((carte or {}).get("id") == "C5E10-OBS-V1" and not sig and prod is None and not sigp
              and nommees and "Archivee le" not in page and f"⚠ {len(arch)} archivee(s)" in page)
        return ok, (f"carte QA {(carte or {}).get('id')}, signalements {len(sig)}, production {prod}, "
                    f"{len(arch)} archivées nommées : {nommees}, tableau : {'Archivee le' in page}")
    ep("E4 vraies données : carte QA, Production vide, 30 archivées sans date nommées, aucun tableau", e4)

    def e5():
        f = contrat.date_d_entree_dans_l_etat
        attendu = {"2026-08-11": "2026-08-11", "Dim_12-07-2026_18h22": "2026-07-12", "Mer_26-08-2026_15h05": "2026-08-26"}
        refuse = {"": "VIDE", "12/07/2026": "MAL FORMÉE", "2026-13-01": "IMPOSSIBLE",
                  "Lun_12-07-2026_18h22": "JOUR DE LA SEMAINE FAUX", "Dim_12-07-2026_25h00": "MAL FORMÉE",
                  " 2026-08-11": "MAL FORMÉE"}
        faux = [k for k, v in attendu.items() if f({"date_entree_etat": k}) != (v, None)]
        faux += [k for k, v in refuse.items() if f({"date_entree_etat": k})[0] is not None
                 or not (f({"date_entree_etat": k})[1] or "").startswith(v)]
        return not faux, f"lectures fausses : {faux}"
    ep("E5 formes acceptées et refusées de date_entree_etat", e5)

    def e6():
        a = dict(derniere["C5E10-QA-V1"], date_entree_etat="2026-08-11")
        b = dict(derniere["C5E10-OBS-V1"])
        carte, sig = cockpit.carte_strategie([a, b], "QA")
        return (carte is None and len(sig) == 1 and "C5E10-QA-V1" in sig[0] and "C5E10-OBS-V1" in sig[0],
                f"carte {(carte or {}).get('id')}, signalements {sig}")
    ep("E6 ex aequo en tête : aucune carte, les deux fiches nommées", e6)

    def e7():
        ids = ["C1-002", "C3-001", "C4-RAV", "C5-EI", "C1-001", "C1-003", "C1-004"]
        jours = ["2026-04-07", "2026-04-06", "2026-04-05", "2026-04-04", "2026-04-03", "2026-04-02", "2026-04-02"]
        fs = [dict(derniere[i], date_entree_etat=j) for i, j in zip(ids, jours)]
        t = montrees(surveillance(fs))
        vus = [i for i in ids if cockpit.esc(cockpit.nom_de_fiche(derniere[i])) in t]
        return len(vus) == 7, f"montrées : {len(vus)} sur 7"
    ep("E7 ex aequo à la sixième place : les sept sont montrées", e7)

    def e8():
        a = dict(derniere["C5E10-QA-V1"], date_entree_etat="")
        b = dict(derniere["C5E10-OBS-V1"])
        carte, sig = cockpit.carte_strategie([b, a], "QA")
        return ((carte or {}).get("id") == "C5E10-OBS-V1" and len(sig) == 1 and "C5E10-QA-V1" in sig[0]
                and "VIDE" in sig[0], f"carte {(carte or {}).get('id')}, signalements {sig}")
    ep("E8 fiche QA sans date : la datée retenue, la sans date nommée", e8)

    def e9():
        class T:
            mesures = []
        sans = dict(derniere["C5E10-QA-V1"], date_entree_etat="")
        T.strategies = [dict(derniere["C5E10-QA-V1"], date_entree_etat="2026-08-11"), dict(derniere["C5E10-OBS-V1"])]
        p1 = cockpit.bloc_strategie(T, "QA", "Aucune strategie en QA")
        T.strategies = [sans]
        p2 = cockpit.bloc_strategie(T, "QA", "Aucune strategie en QA")
        T.strategies = [dict(derniere["C5E10-OBS-V1"]), sans]       # carte, mais aucune mesure
        p4 = cockpit.bloc_strategie(T, "QA", "Aucune strategie en QA")
        # ③ la section COMPLÈTE : les vraies sources, rassemblées comme le fait PUBLIER_LE_SITE.py, dans une copie
        tmp = tempfile.mkdtemp(prefix="v7c_e9_")
        try:
            for src, dst in (("donnees/cours_maitre.csv", "cours_maitre.csv"),
                             ("donnees/historique_mesures.csv", "historique_mesures.csv"),
                             ("donnees/claude_journal_trades.csv", "journal_trades.csv"),
                             ("donnees/claude_positions_ouvertes.csv", "positions_ouvertes.csv")):
                if os.path.isfile(os.path.join(racine, src)):
                    shutil.copy(os.path.join(racine, src), os.path.join(tmp, dst))
            S3 = cockpit.Sources(tmp).charger()
        finally:
            shutil.rmtree(tmp)
        S3.strategies = [dict(derniere["C5E10-OBS-V1"]), sans]
        p3 = cockpit.bloc_strategie(S3, "QA", "Aucune strategie en QA")
        complete = "historique_mesures.csv (mesure du" in p3
        ok = ("C5E10-QA-V1" in p1 and "C5E10-OBS-V1" in p1 and "aucune n est choisie" in p1
              and "C5E10-QA-V1" in p2 and "VIDE" in p2 and "Aucun indicateur" in p4 and "C5E10-QA-V1" in p4 and complete and "C5E10-QA-V1" in p3 and "VIDE" in p3)
        return ok, (f"ex aequo nommés : {'C5E10-QA-V1' in p1 and 'C5E10-OBS-V1' in p1} · seule sans date nommée : "
                    f"{'C5E10-QA-V1' in p2} · sans mesure nommée : {'Aucun indicateur' in p4 and 'C5E10-QA-V1' in p4} · section complète : {complete}, sans date nommée : {'C5E10-QA-V1' in p3}")
    ep("E9 la page montre les signalements dans les trois formes de bloc_strategie", e9)

    def e10():
        a = surveillance(fiches(reel))
        ids = ["C1-002", "C3-001", "C4-RAV", "C5-EI", "C1-001", "C1-003", "C1-004"]
        jours = ["2026-04-07", "2026-04-06", "2026-04-05", "2026-04-04", "2026-04-03", "2026-04-02", "2026-04-02"]
        b = surveillance([dict(derniere[i], date_entree_etat=j) for i, j in zip(ids, jours)])
        p_a = "30 strategie(s) archivee(s) au registre — aucune ne porte de date d entree lisible" in a
        p_b = "7 strategie(s) archivee(s) au registre — 7 datee(s), les 7 plus recentes par leur date d entree" in b
        return p_a and p_b, f"phrase vraies données : {p_a} · phrase cas E7 : {p_b}"
    ep("E10 la phrase d en-tête des archives dit vrai", e10)

    def e11():
        ids = ["C1-002", "C3-001"]
        fs = [dict(derniere["C1-002"], date_entree_etat="2026-04-07"), dict(derniere["C3-001"], date_entree_etat="")]
        page = surveillance(fs)
        tab_ok = cockpit.esc("C1-002 · " + derniere["C1-002"]["nom"]) in montrees(page)
        sd_ok = cockpit.esc("C3-001 · " + derniere["C3-001"]["nom"]) + " (VIDE)" in page
        return tab_ok and sd_ok, f"tableau « id · nom » : {tab_ok} · sans date « id · nom » : {sd_ok}"
    ep("E11 une archivée s écrit « id · nom » dans les deux listes", e11)
    return res


def montrer_l_ordre(racine):
    """Affiche, sur le vrai registre, ce que le cockpit montrait par la PLACE et ce qu'il montre par la DATE.

    ① RÔLE — Rendre l'ordre avant/après mesurable par une commande que le garde-fou peut relancer.
    ② CONTEXTE D'APPEL — `main`, avec l'option `--montrer-l-ordre`.
    ③ ENTRÉE — `racine` : le dépôt dont on lit le registre et le code.
    ④ CONDITIONS D'ENTRÉE — Celles d'`epreuves`.
    ⑤ SORTIE — Aucune valeur : quatre lignes affichées (cinq depuis le tour 2 : les vivantes sans date).
      [rend: 0]
    ⑥ TRAITEMENT — ① ranger le registre en fiches (n°83) · ② AVANT : la dernière fiche QA de la liste, les six
      dernières archivées de la liste (le code de origin/main à 431b8c86, `lignes[-1]` et `archivees[-6:]`) ·
      ③ APRÈS : `carte_strategie` et `ranger_par_date_d_entree`.
    ⑦ UNITÉ — Des identifiants de fiches.
    ⑧ POURQUOI — L'ordre avant/après est demandé par la livraison ; une sortie écrite à la main serait invérifiable.
    ⑨ CE QUI CLOCHE — L'AVANT est une copie de deux lignes de l'ancien cockpit, pas l'ancien cockpit lui-même.
    ⑩ EFFET — Lit le registre ; affiche.
    ⑪ TERMINAISON — Rend la main ; lève si le registre manque.
      [sort: non]
    """
    contrat, cockpit = charger(os.path.join(racine, "programmes"))
    fs = list(contrat.fiches_du_registre(contrat.chemin_du_registre(racine)).values())
    qa = [s for s in fs if (s.get("etat_vie") or s.get("statut") or "").strip().upper().startswith("QA")]
    arch = [s for s in fs if "ARCHIV" in (s.get("statut", "") + s.get("etat_vie", "")).upper()]
    print(f"AVANT (place) carte QA : {qa[-1]['id']} · 6 dernières archivées : {', '.join(s['id'] for s in arch[-6:])}")
    carte, sig = cockpit.carte_strategie(fs, "QA")
    g_qa, _ = contrat.ranger_par_date_d_entree(qa)
    print(f"APRÈS (date) carte QA : {(carte or {}).get('id')} · ordre QA : "
          + ", ".join(f"{s['id']} {j}" for j, l in g_qa for s in l) + f" · signalements : {len(sig)}")
    viv = [s for s in fs if (s.get("etat_vie") or s.get("statut") or "").strip().upper().startswith(("QA", "PRODUCTION"))]
    _g, viv_sd = contrat.ranger_par_date_d_entree(viv)
    print(f"VIVANTES (QA ou PRODUCTION) : {len(viv)}, sans date lisible : {len(viv_sd)}")
    g_ar, sd = contrat.ranger_par_date_d_entree(arch)
    print(f"APRÈS (date) archivées : {len(arch)}, datées : {sum(len(l) for _, l in g_ar)}, "
          f"sans date : {len(sd)} ({', '.join(sorted(set(r for _, r in sd)))})")


def main():
    """Lance les épreuves, et en option les sabotages ; rend le code de sortie.

    ① RÔLE — Le point d'entrée (voir l'en-tête du fichier).
    ② CONTEXTE D'APPEL — La ligne de commande ; en sabotage, ce même fichier relancé par lui-même.
    ③ ENTRÉE — `sys.argv` : la racine, puis `--saboter`, `--montrer-l-ordre` ou `--programmes=<dossier>` (usage
      interne du sabotage).
    ④ CONDITIONS D'ENTRÉE — La racine est un dépôt qui porte `programmes/` et `donnees/cac40_strategies.csv`.
    ⑤ SORTIE — Aucune valeur rendue : le programme sort, 0 si tout est vert et que chaque sabotage a rougi, 1 sinon.
      [rend: 0]
    ⑥ TRAITEMENT — ① lancer les épreuves sur le code choisi et afficher une ligne par épreuve · ② en sabotage,
      refuser si une épreuve est déjà rouge, puis pour chaque sabotage : copier `programmes/` dans un dossier
      temporaire, remplacer le texte visé (exactement une fois), relancer ce fichier sur la copie, exiger un code
      non nul ET le rouge de l'épreuve visée, l'afficher · ③ sortir.
    ⑦ UNITÉ — Des épreuves ; des sabotages.
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
    ⑨ CE QUI CLOCHE — Chaque sabotage copie tout `programmes/` (quelques secondes chacun).
    ⑩ EFFET — Affiche ; en sabotage, écrit puis efface ses copies sous le dossier temporaire du système.
    ⑪ TERMINAISON — Sort toujours par `sys.exit` ; un sous-processus est borné à 300 secondes.
      [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    racine = os.path.abspath(args[0] if args else ".")
    prog = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--programmes=")),
                os.path.join(racine, "programmes"))
    if "--montrer-l-ordre" in sys.argv:
        montrer_l_ordre(racine)
        sys.exit(0)
    try:
        res = epreuves(racine, prog)
    except Exception as e:
        print(f"  ROUGE  les épreuves n'ont pas pu tourner : {type(e).__name__}: {e}")
        sys.exit(1)
    for nom, ok, detail in res:
        print(f"  {'VERT ' if ok else 'ROUGE'}  {nom} — {detail}")
    rouges = sum(1 for _, ok, _ in res if not ok)
    print(f"{len(res)} épreuves, {rouges} rouge(s)")
    code = 1 if rouges or not res else 0
    if "--saboter" in sys.argv:
        if code:
            print("  ROUGE  sabotages non lancés : une épreuve est rouge sur le code non saboté")
            sys.exit(1)
        for nom, (cible, fichier, avant, apres, *n) in SABOTAGES.items():
            n = n[0] if n else 1
            tmp = tempfile.mkdtemp(prefix="v7c_sabotage_")
            copie = os.path.join(tmp, "programmes")
            shutil.copytree(os.path.join(racine, "programmes"), copie,
                            ignore=shutil.ignore_patterns("__pycache__"))
            ch = os.path.join(copie, fichier)
            texte = open(ch, encoding="utf-8").read()
            if texte.count(avant) != n:
                print(f"  ROUGE  {nom} : texte visé trouvé {texte.count(avant)} fois au lieu de {n} — sabotage impossible")
                code = 1
                shutil.rmtree(tmp)
                continue
            open(ch, "w", encoding="utf-8").write(texte.replace(avant, apres))
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), racine, f"--programmes={copie}"],
                               capture_output=True, text=True, timeout=300)
            rougies = [l.split("  ", 2)[2].split(" — ")[0] for l in r.stdout.splitlines() if l.startswith("  ROUGE")]
            rougies = [x.split(" ")[0] for x in rougies]
            if r.returncode == 0 or cible not in rougies:
                print(f"  ROUGE  {nom} : {cible} n'a pas rougi (rouges : {rougies or 'aucune'}, code {r.returncode})")
                code = 1
            else:
                print(f"  VERT   {nom} : {cible} rougit (rouges : {', '.join(rougies)})")
            shutil.rmtree(tmp)
    sys.exit(code)


if __name__ == "__main__":
    main()
