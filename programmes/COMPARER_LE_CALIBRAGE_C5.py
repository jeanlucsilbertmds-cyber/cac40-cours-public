#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COMPARER_LE_CALIBRAGE_C5 — Sam 21-11-2026 15h15 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Ce programme met côte à côte, opération par opération, les 100 opérations de C5-ETENDU-10 écrites
à la prise du golden (donnees/TABLEAU_100_TRADES_C5E10_*.csv, 01-08-2026) et celles que rend aujourd'hui le module C5
rejoué sur le jeu de données du golden (temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv). Il sort la liste
des opérations DISPARUES, NOUVELLES, CHANGÉES (date d'entrée, date de sortie ou famille de motif) et celles dont seul
le gain diffère. Il ne cherche PAS la cause. Fait qui l'a fait naître (BACKLOG A-959 ⑥) : à la prise du golden, C5
donnait 100 opérations pour +111 334,24 € ; rejoué dans la nuit du 20 au 21-11-2026, il en donnait 74 pour
+66 270,99 €. Décision de Jean-Luc du 21-11-2026 à 15h11, « 1 » : lancer la première moitié du rail ① du Plan V8
(A-967, A-966).

① RÔLE — Produire rapports/CALIBRAGE_C5.md : la liste des écarts entre les opérations de référence et celles
  d'aujourd'hui, chacune avec valeur, date d'entrée, date de sortie, motif et gain.
② CONTEXTE D'APPEL — À la main, par le Chat ou Cowork ; l'épreuve tests/EPREUVE_DU_CALIBRAGE_C5_Sam_21-11-2026.py
  n'appelle que `comparer`, `operations_de_reference` et `ecrire_le_rapport`. Aucune tâche du soir.
③ ENTRÉE — La ligne de commande : « --racine=<dossier> » (défaut : le dépôt qui porte ce fichier) ;
  « --sortie=<fichier> » (défaut : <racine>/rapports/CALIBRAGE_C5.md) ; « --bareme=<nom> » (défaut : aucun, le
  barème des trades vécus que le module prend sans argument, comme au rejeu de la nuit).
④ CONDITIONS D'ENTRÉE — La racine porte le golden, le témoin du golden, le tableau des 100 trades, le module C5,
  programmes/JUGE_DES_STRATEGIES.py et programmes/CONTRATS_DES_FICHIERS.py. LE TÉMOIN DOIT AVOIR L'EMPREINTE QUE LE
  GOLDEN DÉCLARE, et toute date lue (témoin et tableau) doit être POSTÉRIEURE à la fin de la fenêtre du regard unique
  (CONTRATS.fenetre_du_regard_unique, 2000-01-01 → 2023-12-31 au 21-11-2026) : sinon rien n'est rejoué.
⑤ SORTIE — Le code de sortie : 0 comparaison faite, aucune opération disparue, nouvelle ou changée · 1 comparaison
  faite, au moins un écart de cette sorte · 2 la comparaison n'a pas pu tourner (R-734 : un contrôle qui n'a pas pu
  tourner rend un code non nul). Le rapport écrit, et un résumé affiché.
⑥ TRAITEMENT — ① trouver les cinq fichiers · ② refuser si l'empreinte du témoin n'est pas celle du golden ·
  ③ lire le tableau de référence · ④ refuser toute date tombant dans la fenêtre du regard unique · ⑤ charger le témoin
  par le lecteur du juge (`charger_cours`) et refuser de même · ⑥ rejouer `backtest_c5etendu10` du module, compte
  « jetons illimités » · ⑦ comparer · ⑧ écrire le rapport.
⑦ UNITÉ — Gains en EUROS au centime ; dates AAAA-MM-JJ ; comptes en OPÉRATIONS.
⑧ POURQUOI — Rien ne recopie : l'univers, le jeu et les sorties sont ceux du module (R-708, deux implémentations
  d'une même chose divergent toujours) ; le lecteur et le rapprochement des noms sont ceux du juge. LE RAPPORT
  N'AFFICHE AUCUN COURS : seulement dates, valeurs, motifs et gains.
⑨ CE QUI CLOCHE — ① Le rejeu de la nuit qui a donné 74 n'est pas au dépôt (archives/RELU_COWORK_TRAVAIL_EMPREINTE_*,
  « le script de l'auteur n'est pas au dépôt ») : ce programme rejoue avec le lecteur du juge, et peut donc ne pas
  retrouver 74.
  ② La famille d'un motif (« TP_x » → « TP ») se calcule ici comme dans `calibrer` du juge, où elle est
  une expression anonyme non importable : deux écritures.
  ③ Le gain du tableau est au forfait de frais du golden,
  celui du module au barème vécu : un écart de gain seul est attendu (A-290, A-550) et n'entre pas dans le code 1.
⑩ EFFET — Lit les fichiers nommés ; écrit le seul fichier de sortie ; aucun réseau.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? `backtest_c5etendu10` n'a pas de borne
  de temps ; mesuré à moins d'une minute le 21-11-2026 sur le témoin.
  [sort: oui]
"""
import csv
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

ICI = os.path.dirname(os.path.abspath(__file__))


def charger(chemin, nom):
    """Charge un programme du dépôt comme un module.

    ① RÔLE — Atteindre le juge, le contrat et le module C5 sans rien en recopier.
    ② CONTEXTE D'APPEL — `main`.

    ③ ENTRÉE — `chemin` du fichier, `nom` du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe ; son dossier est mis
    en tête du chemin d'import pour ses propres imports.
    ⑤ SORTIE — UNE valeur : le module.
    [rend: 1]

    ⑥ TRAITEMENT — importlib depuis le chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET —
    Exécute le haut du fichier chargé.
    ⑪ TERMINAISON — Rend la main ; lève ce que lève l'import.
    [sort: non]
    """
    d = os.path.dirname(os.path.abspath(chemin))
    if d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


def famille(motif):
    """Rend la famille d'un motif de sortie.

    ① RÔLE — Ramener « TP », « TP_GAP » etc. à « TP ».
    ② CONTEXTE D'APPEL — `comparer`.
    ③ ENTRÉE — `motif`, un texte
    ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un texte.
    [rend: 1]
    ⑥ TRAITEMENT — premier morceau
    avant « _ ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La règle de `calibrer` du juge (comparaison par famille, A-491).

    ⑨ CE QUI CLOCHE — Deuxième écriture de cette règle (fiche en tête, ⑨ ②).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
    [sort: non]
    """
    return (motif or "").split("_")[0]


def gain(texte):
    """Lit un gain en euros écrit à la française.

    ① RÔLE — « 3700,00 » → 3700.0.
    ② CONTEXTE D'APPEL — `operations_de_reference`.
    ③ ENTRÉE — `texte`.

    ④ CONDITIONS D'ENTRÉE — Un nombre, virgule ou point décimal.
    ⑤ SORTIE — UNE valeur : un flottant.
    [rend: 1]

    ⑥ TRAITEMENT — virgule → point, espaces retirés.
    ⑦ UNITÉ — EUROS.
    ⑧ POURQUOI — Le tableau écrit « 3700,00 ».

    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Lève ValueError sur un texte illisible.
    [sort: non]
    """
    return float(str(texte).replace(" ", "").replace(" ", "").replace(",", "."))


def operations_de_reference(chemin, cle):
    """Lit les opérations de référence du golden.

    ① RÔLE — Rendre les opérations du tableau des 100 trades sous la forme commune.
    ② CONTEXTE D'APPEL — `main` ;
    l'épreuve.
    ③ ENTRÉE — `chemin` du tableau (séparateur « ; »), `cle` la fonction de rapprochement des noms
    (`cle_valeur` du juge).
    ④ CONDITIONS D'ENTRÉE — Colonnes date_signal, date_entree, valeur, date_sortie, motif,
    net_eur.
    ⑤ SORTIE — UNE valeur : une liste de dictionnaires {cle, valeur, date_signal, date_entree, date_sortie,
    motif, gain}.
    [rend: 1]
    ⑥ TRAITEMENT — lecture ligne à ligne.
    ⑦ UNITÉ — gain en EUROS.
    ⑧ POURQUOI — Le golden
    ne garde qu'une empreinte des trades ; ce tableau est la seule liste écrite (lu par `calibrer`, défaut 4 d'A-491).

    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Lève sur colonne absente.
    [sort: non]
    """
    with open(chemin, encoding="utf-8") as f:
        lignes = list(csv.DictReader(f, delimiter=";"))
    return [{"cle": cle(r["valeur"]), "valeur": r["valeur"], "date_signal": r["date_signal"],
             "date_entree": r["date_entree"], "date_sortie": r["date_sortie"], "motif": r["motif"],
             "gain": gain(r["net_eur"])} for r in lignes]


def operations_d_aujourd_hui(module, donnees, cle, bareme):
    """Rejoue C5 et rend ses opérations « jetons illimités ».

    ① RÔLE — Rendre les opérations du module d'aujourd'hui sous la forme commune.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `module` C5, `donnees` {nom de l'univers : séances}, `cle` le rapprochement, `bareme` ou None.

    ④ CONDITIONS D'ENTRÉE — Les clés de `donnees` écrites comme dans `C5E10_UNIVERS`.
    ⑤ SORTIE — UNE valeur : la
    liste.
    [rend: 1]
    ⑥ TRAITEMENT — `backtest_c5etendu10`, puis dates d'entrée et de sortie lues aux indices
    `i_in`, `i_out`.
    ⑦ UNITÉ — gain en EUROS (`pnl`).
    ⑧ POURQUOI — Le golden est la comptabilité « jetons illimités »
    (`qualite_signal`).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui du module.
    ⑪ TERMINAISON — Un appel non borné
    (`backtest_c5etendu10`).
    [sort: non]
    """
    r = module.backtest_c5etendu10(donnees, bareme)
    sortie = []
    for t in r["qualite_signal"]["trades"]:
        s = donnees[t["valeur"]]
        sortie.append({"cle": cle(t["valeur"]), "valeur": t["valeur"], "date_signal": t["date_signal"],
                       "date_entree": s[t["i_in"]]["date"], "date_sortie": s[t["i_out"]]["date"],
                       "motif": t["motif"], "gain": float(t["pnl"])})
    return sortie


def comparer(reference, aujourd_hui):
    """Compare deux listes d'opérations, opération par opération.

    ① RÔLE — Dire ce qui a disparu, ce qui est nouveau, ce qui a changé.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.

    ③ ENTRÉE — `reference` et `aujourd_hui`, deux listes sous la forme commune.
    ④ CONDITIONS D'ENTRÉE — Une opération s'identifie par (cle,
    date_signal) ; un doublon de clé est signalé dans « doublons ».
    ⑤ SORTIE — UNE valeur : un dictionnaire de
    listes « disparues », « nouvelles », « changees » (couples référence, aujourd'hui), « gain_seul » (couples),
    « doublons » (clés).
    [rend: 1]
    ⑥ TRAITEMENT — index par clé ; famille de motif et dates comparées ; gain comparé
    au centime.
    ⑦ UNITÉ — EUROS.
    ⑧ POURQUOI — La clé est celle de `calibrer` (valeur rapprochée, date du signal).

    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
    [sort: non]
    """
    doublons = []

    def index(liste):
        """Range une liste par clé.

        ① RÔLE — Indexer.
        ② CONTEXTE D'APPEL — `comparer`.
        ③ ENTRÉE — `liste`, une liste d'opérations.
        ④ CONDITIONS D'ENTRÉE — —

        ⑤ SORTIE — UNE valeur : un dictionnaire.
        [rend: 1]
        ⑥ TRAITEMENT — clé (cle, date_signal).
        ⑦ UNITÉ — —

        ⑧ POURQUOI — Un doublon écraserait une opération en silence : il est noté.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET —
        Ajoute à `doublons`.
        ⑪ TERMINAISON — Rend toujours la main.
        [sort: non]
        """
        d = {}
        for o in liste:
            k = (o["cle"], o["date_signal"])
            if k in d:
                doublons.append(k)
            d[k] = o
        return d

    ref, auj = index(reference), index(aujourd_hui)
    res = {"disparues": [], "nouvelles": [], "changees": [], "gain_seul": [], "doublons": doublons}
    for k in sorted(ref):
        if k not in auj:
            res["disparues"].append(ref[k])
            continue
        a, b = ref[k], auj[k]
        if (a["date_entree"], a["date_sortie"], famille(a["motif"])) != \
           (b["date_entree"], b["date_sortie"], famille(b["motif"])):
            res["changees"].append((a, b))
        elif round(a["gain"] - b["gain"], 2) != 0:
            res["gain_seul"].append((a, b))
    res["nouvelles"] = [auj[k] for k in sorted(auj) if k not in ref]
    return res


def ecrire_le_rapport(chemin, res, reference, aujourd_hui, entete):
    """Écrit rapports/CALIBRAGE_C5.md.

    ① RÔLE — Mettre la comparaison par écrit, sans aucun cours.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve (dossier
    jetable).
    ③ ENTRÉE — `chemin`, `res` de `comparer`, les deux listes `reference` et `aujourd_hui`, `entete` (lignes de provenance).

    ④ CONDITIONS D'ENTRÉE — Le dossier de `chemin` peut être créé.
    ⑤ SORTIE — UNE valeur : le texte écrit.
    [rend: 1]
    ⑥ TRAITEMENT — résumé, puis une table par catégorie.
    ⑦ UNITÉ — EUROS au centime.

    ⑧ POURQUOI — Le Chat cherchera la cause à partir de cette liste.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le fichier.
    ⑪ TERMINAISON — Lève sur une écriture impossible.
    [sort: non]
    """
    def ligne(o):
        """Une ligne de table.
            ① RÔLE — Formater une opération.
            ② CONTEXTE D'APPEL — `ecrire_le_rapport`.

        ③ ENTRÉE — `o`, une opération.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : un texte.
        [rend: 1]

        ⑥ TRAITEMENT — valeur, signal, entrée, sortie, motif, gain.
        ⑦ UNITÉ — EUROS.
        ⑧ POURQUOI — Les cinq champs
        demandés, plus la date du signal qui identifie.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main.
        [sort: non]
        """
        return "%s | %s | %s | %s | %s | %+.2f" % (o["valeur"], o["date_signal"], o["date_entree"],
                                                 o["date_sortie"], o["motif"], o["gain"])
    tete = "valeur | signal | entrée | sortie | motif | gain €\n--- | --- | --- | --- | --- | ---"
    t = ["# CALIBRAGE DE C5 — opérations du golden contre opérations d'aujourd'hui", "",
         "Simulation uniquement. Programme : programmes/COMPARER_LE_CALIBRAGE_C5.py. Aucun cours n'est affiché.", ""]
    t += ["- " + e for e in entete]
    t += ["", "## RÉSUMÉ", "",
          "- référence : %d opérations, %+.2f €" % (len(reference), sum(o["gain"] for o in reference)),
          "- aujourd'hui : %d opérations, %+.2f €" % (len(aujourd_hui), sum(o["gain"] for o in aujourd_hui)),
          "- disparues : %d · nouvelles : %d · changées : %d · gain seul différent : %d · doublons : %d"
          % (len(res["disparues"]), len(res["nouvelles"]), len(res["changees"]), len(res["gain_seul"]),
             len(res["doublons"])), ""]
    for titre, cle_ in (("DISPARUES (dans la référence, pas aujourd'hui)", "disparues"),
                        ("NOUVELLES (aujourd'hui, pas dans la référence)", "nouvelles")):
        t += ["## " + titre, "", tete] + [ligne(o) for o in res[cle_]] + [""]
    for titre, cle_ in (("CHANGÉES (entrée, sortie ou famille de motif)", "changees"),
                        ("GAIN SEUL DIFFÉRENT (attendu : forfait du golden contre barème vécu, A-290, A-550)",
                         "gain_seul")):
        t += ["## " + titre, "", "réf. / auj. | " + tete.split("\n")[0], "--- | " + tete.split("\n")[1]]
        for a, b in res[cle_]:
            t += ["réf. | " + ligne(a), "auj. | " + ligne(b)]
        t += [""]
    texte = "\n".join(t)
    os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    return texte


def main():
    """Point d'entrée.
        ① RÔLE — Voir fiche en tête.
        ② CONTEXTE D'APPEL — Le lancement.
        ③ ENTRÉE — fiche en tête, ③.

    ④ CONDITIONS D'ENTRÉE — fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
    [rend: 1]
    ⑥ TRAITEMENT — fiche en
    tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — fiche en tête, ⑩.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    inconnus = [a for a in sys.argv[1:] if not (a.startswith("--") and "=" in a)
                or a[2:].split("=", 1)[0] not in ("racine", "sortie", "bareme")]
    if inconnus:
        print("usage : COMPARER_LE_CALIBRAGE_C5.py [--racine=…] [--sortie=…] [--bareme=…] ; inconnu : %s" % inconnus)
        return 2
    racine = os.path.abspath(opts.get("racine", os.path.dirname(ICI)))
    sortie = opts.get("sortie", os.path.join(racine, "rapports", "CALIBRAGE_C5.md"))
    try:
        J = charger(os.path.join(racine, "programmes", "JUGE_DES_STRATEGIES.py"), "JUGE_DES_STRATEGIES")
        C = charger(os.path.join(racine, "programmes", "CONTRATS_DES_FICHIERS.py"), "CONTRATS_DES_FICHIERS")
        import json
        f_gold = J.trouver(racine, "golden_tests_")
        f_tem = J.trouver(racine, "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN")
        f_tab = J.trouver(racine, "TABLEAU_100_TRADES_C5E10")
        f_mod = J.trouver(racine, "MODULE_C5_ETENDU_10")
        manque = [n for n, f in (("golden", f_gold), ("témoin", f_tem), ("tableau", f_tab), ("module", f_mod)) if not f]
        if manque:
            print("ARRÊT : introuvable : %s" % manque)
            return 2
        golden = json.load(open(f_gold, encoding="utf-8"))
        attendu = str((golden.get("meta") or {}).get("hash_donnees_sha256_16", ""))
        emp = J.empreinte(f_tem)
        if not attendu or emp != attendu:
            print("ARRÊT : empreinte du témoin %s, le golden déclare %s — rien n'est rejoué." % (emp, attendu or "aucune"))
            return 2
        _deb, fin_regard = C.fenetre_du_regard_unique()
        reference = operations_de_reference(f_tab, J.cle_valeur)
        dates_ref = [o[k] for o in reference for k in ("date_signal", "date_entree", "date_sortie")]
        if not dates_ref or min(dates_ref) <= fin_regard:
            print("ARRÊT : le tableau de référence porte une date dans la fenêtre du regard unique — rien n'est rejoué.")
            return 2
        cours = J.charger_cours(f_tem)
        if not cours or min(s[0]["date"] for s in cours.values() if s) <= fin_regard:
            print("ARRÊT : le témoin porte une date dans la fenêtre du regard unique — rien n'est rejoué.")
            return 2
        module = charger(f_mod, "MODULE_C5_ETENDU_10")
        donnees = {v: cours[J.cle_valeur(v)] for v in module.C5E10_UNIVERS if J.cle_valeur(v) in cours}
        absentes = [v for v in module.C5E10_UNIVERS if v not in donnees]
        aujourd_hui = operations_d_aujourd_hui(module, donnees, J.cle_valeur, opts.get("bareme"))
    except Exception as e:  # la comparaison n'a pas pu tourner (R-734)
        print("ARRÊT : %s: %s" % (type(e).__name__, e))
        return 2
    res = comparer(reference, aujourd_hui)
    rel = lambda p: os.path.relpath(p, racine)
    entete = ["date du rapport : %s" % J.horodatage(),
              "référence : %s" % rel(f_tab), "golden : %s" % rel(f_gold),
              "jeu de données : %s (empreinte %s, celle du golden)" % (rel(f_tem), emp),
              "module rejoué : %s, `backtest_c5etendu10`, comptabilité jetons illimités" % rel(f_mod),
              "barème : %s" % (opts.get("bareme") or "défaut du module (aucun argument)"),
              "valeurs de l'univers sans cours : %s" % (", ".join(absentes) or "aucune")]
    ecrire_le_rapport(sortie, res, reference, aujourd_hui, entete)
    print("référence %d · aujourd'hui %d · disparues %d · nouvelles %d · changées %d · gain seul %d · doublons %d"
          % (len(reference), len(aujourd_hui), len(res["disparues"]), len(res["nouvelles"]), len(res["changees"]),
             len(res["gain_seul"]), len(res["doublons"])))
    print("rapport : %s" % sortie)
    return 1 if (res["disparues"] or res["nouvelles"] or res["changees"] or res["doublons"]) else 0


if __name__ == "__main__":
    sys.exit(main())
