#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXPLIQUER_L_ECART_DE_GAIN_C5 — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. rapports/CALIBRAGE_C5.md (fabriqué par programmes/COMPARER_LE_CALIBRAGE_C5.py) dit que les 100
opérations de C5-ETENDU-10 du golden se retrouvent aujourd'hui, mêmes dates et mêmes motifs, et que SEUL LE GAIN
diffère : +111 334,24 € au golden, +82 022,24 € au rejeu. Ce programme teste l'hypothèse du Chat : l'écart vient du
seul régime de frais — forfait de 300 € par opération au golden, barème réel d'aujourd'hui au module (A-550, avec la
taxe sur les transactions financières). Il remplace le script de mesure rapports/PREUVE_ECART_DE_GAIN_C5.py, qui ne
tournait que sur le poste de son auteur (relecture Cowork du 21-11-2026, défaut I-1), et fabrique la section qui
était écrite à la main dans rapports/CALIBRAGE_C5.md (défaut I-2, R-728 : ce qui se calcule ne s'écrit jamais à la
main).

① RÔLE — Recalculer chaque opération du tableau des 100 trades du golden avec `MODULE_POSITIONS.pnl_net` sous trois
  barèmes (forfait « HIST_FORFAIT_300 », courtage sans taxe « HIST_COURTAGE_SANS_TTF », réel = sans argument), dire si
  le forfait retrouve chaque gain du golden à l'arrondi des prix près, et écrire rapports/CAUSE_DE_L_ECART_DE_GAIN_C5.md :
  totaux, part du courtage, part de la taxe, valeurs taxées et non taxées par année, verdict.
② CONTEXTE D'APPEL — À la main, par le Chat ou Cowork, depuis n'importe quel dossier ; l'épreuve
  tests/EPREUVE_DE_L_ECART_DE_GAIN_C5_Sam_21-11-2026.py appelle `lire_le_tableau`, `mesurer` et `ecrire_le_rapport`.
  Aucune tâche du soir.
③ ENTRÉE — La ligne de commande : « --racine=<dossier> » (défaut : le dépôt qui porte ce fichier) ;
  « --sortie=<fichier> » (défaut : <racine>/rapports/CAUSE_DE_L_ECART_DE_GAIN_C5.md).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/MODULE_POSITIONS.py, programmes/JUGE_DES_STRATEGIES.py,
  programmes/CONTRATS_DES_FICHIERS.py, programmes/COMPARER_LE_CALIBRAGE_C5.py et donnees/TABLEAU_100_TRADES_C5E10_*.csv.
  TOUTE DATE DU TABLEAU doit être postérieure à la fin de la fenêtre du regard unique
  (CONTRATS.fenetre_du_regard_unique) : sinon rien n'est calculé. Aucun fichier de cours n'est lu.
⑤ SORTIE — Le code de sortie : 0 hypothèse confirmée (chaque opération retrouvée au forfait) · 1 hypothèse réfutée
  (au moins une opération hors tolérance) · 2 le calcul n'a pas pu tourner (R-734). Le rapport écrit, deux lignes
  affichées.
⑥ TRAITEMENT — ① charger les quatre programmes de la racine · ② lire le tableau par `gain` du comparateur · ③ refuser
  une date dans la fenêtre du regard unique · ④ `mesurer` · ⑤ `ecrire_le_rapport` · ⑥ afficher et sortir.
⑦ UNITÉ — Gains, frais et écarts en EUROS ; prix en euros ; dates AAAA-MM-JJ ; comptes en OPÉRATIONS.
⑧ POURQUOI — Aucune formule recopiée (deux implémentations d'une même chose divergent toujours, R-708) : chaque gain
  vient de `pnl_net`, le barème de `cout_d_un_ordre`, la liste des valeurs taxées de `valeur_taxee`, la lecture des
  gains de `gain` du comparateur, la fenêtre du contrat. Tout chemin part de la racine : rien ne dépend du poste.
⑨ CE QUI CLOCHE — ① Le tableau garde les prix à 4 décimales : le forfait ne retrouve le golden qu'à une tolérance
  près, calculée par `tolerance` ; un tableau aux prix plus grossiers ferait rougir à tort. ② Le rejeu d'aujourd'hui
  (82 022,24 €) n'est pas relu ici (il lit les cours) : c'est `COMPARER_LE_CALIBRAGE_C5.py --bareme=HIST_FORFAIT_300`
  qui le relie au golden (« gain seul 0 »).
⑩ EFFET — Lit le tableau, le barème et la liste des valeurs taxées ; écrit le seul fichier de sortie ; aucun réseau.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Non : une boucle par ligne du tableau.
  [sort: oui]
"""
import csv
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

ICI = os.path.dirname(os.path.abspath(__file__))
FORFAIT = "HIST_FORFAIT_300"
SANS_TAXE = "HIST_COURTAGE_SANS_TTF"
DEMI_PAS_DE_PRIX = 0.00005  # le tableau écrit ses prix à 4 décimales : l'arrondi déplace chaque prix d'au plus 0,00005 €
DEMI_CENTIME = 0.005  # le tableau écrit ses gains au centime


def charger(chemin, nom):
    """Charge un programme de la racine comme un module.

    ① RÔLE — Atteindre le module des positions, le juge, le contrat et le comparateur sans rien en recopier.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `chemin` du fichier, `nom` du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe ; son dossier est mis en tête du chemin d'import.
    ⑤ SORTIE — UNE valeur : le module.
    [rend: 1]
    ⑥ TRAITEMENT — importlib depuis le chemin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 ; et le défaut I-1 : le chemin vient de la racine, jamais d'un dossier écrit en dur.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut du fichier chargé.
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


def lire_le_tableau(chemin, gain):
    """Lit le tableau des 100 trades du golden.

    ① RÔLE — Rendre chaque opération avec ses prix, ses dates et son gain du golden.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `chemin` du tableau (séparateur « ; »), `gain` la lecture des nombres du comparateur.
    ④ CONDITIONS D'ENTRÉE — Colonnes valeur, date_signal, date_entree, date_sortie, prix_entree, prix_sortie, net_eur.
    ⑤ SORTIE — UNE valeur : une liste de dictionnaires {valeur, date_signal, date_entree, date_sortie, prix_entree,
    prix_sortie, ref}.
    [rend: 1]
    ⑥ TRAITEMENT — lecture ligne à ligne.
    ⑦ UNITÉ — prix et `ref` en EUROS.
    ⑧ POURQUOI — La lecture des nombres « 3700,00 » est celle du comparateur (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Lève sur colonne absente ou nombre illisible.
    [sort: non]
    """
    with open(chemin, encoding="utf-8") as f:
        lignes = list(csv.DictReader(f, delimiter=";"))
    return [{"valeur": r["valeur"], "date_signal": r["date_signal"], "date_entree": r["date_entree"], "date_sortie": r["date_sortie"],
             "prix_entree": gain(r["prix_entree"]), "prix_sortie": gain(r["prix_sortie"]),
             "ref": gain(r["net_eur"])} for r in lignes]


def tolerance(capital, prix_entree, prix_sortie):
    """Écart admis entre le gain recalculé au forfait et le gain écrit au golden, pour UNE opération.

    ① RÔLE — Borner ce que l'arrondi du tableau peut expliquer.
    ② CONTEXTE D'APPEL — `mesurer`.
    ③ ENTRÉE — `capital` engagé, `prix_entree`, `prix_sortie` tels que le tableau les écrit.
    ④ CONDITIONS D'ENTRÉE — `prix_entree` non nul.
    ⑤ SORTIE — UNE valeur : la tolérance.
    [rend: 1]
    ⑥ TRAITEMENT — Le gain brut vaut capital × (sortie / entrée − 1) ; déplacer chaque prix d'au plus
    DEMI_PAS_DE_PRIX le déplace d'au plus capital × DEMI_PAS_DE_PRIX × (1 / entrée + sortie / entrée²) ; s'y ajoute
    DEMI_CENTIME, l'arrondi du gain écrit. Le forfait ne dépend pas du prix.
    ⑦ UNITÉ — EUROS.
    ⑧ POURQUOI — Une tolérance fixe serait trop large sur une valeur chère et trop étroite sur une valeur bon marché.
    ⑨ CE QUI CLOCHE — Suppose que le golden a calculé sur des prix dont le tableau est l'arrondi à 4 décimales.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Lève si `prix_entree` vaut zéro.
    [sort: non]
    """
    return capital * DEMI_PAS_DE_PRIX * (1.0 / prix_entree + prix_sortie / prix_entree ** 2) + DEMI_CENTIME


def mesurer(operations, M):
    """Recalcule chaque opération sous les trois barèmes et rend les totaux et le verdict.

    ① RÔLE — Chiffrer l'hypothèse et dire si elle tient.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `operations` de `lire_le_tableau`, `M` le module des positions chargé.
    ④ CONDITIONS D'ENTRÉE — Au moins une opération ; valeurs et dates connues du barème.
    ⑤ SORTIE — UNE valeur : un dictionnaire {n, ref, forfait, sans_taxe, reel, ecart_golden_reel, ecart_forfait_reel,
    part_courtage, part_taxe, par_groupe {(année d'entrée, taxée) : [n, écart]}, hors_tolerance [opérations],
    ecart_max, confirmee}.
    [rend: 1]
    ⑥ TRAITEMENT — pour chaque opération : `pnl_net` au forfait, sans taxe, au réel ; écart au golden comparé à
    `tolerance` ; groupe par année d'entrée et par `valeur_taxee` à la date d'entrée.
    ⑦ UNITÉ — EUROS, arrondis au centime dans le dictionnaire rendu.
    ⑧ POURQUOI — part_courtage = forfait − sans_taxe et part_taxe = sans_taxe − réel : leur somme est l'écart
    forfait − réel par construction ; la relecture Cowork (m-4) demandait la part de la taxe.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le barème et la liste des valeurs taxées (par le module).
    ⑪ TERMINAISON — Rend la main ; lève ce que lève `pnl_net`.
    [sort: non]
    """
    t = {"n": 0, "ref": 0.0, "forfait": 0.0, "sans_taxe": 0.0, "reel": 0.0}
    groupes, hors, ecart_max = {}, [], 0.0
    for o in operations:
        a = (o["prix_entree"], o["prix_sortie"], o["valeur"], o["date_entree"], o["date_sortie"])
        f = M.pnl_net(*a, bareme=FORFAIT)
        s = M.pnl_net(*a, bareme=SANS_TAXE)
        r = M.pnl_net(*a)
        t["n"] += 1
        t["ref"] += o["ref"]
        t["forfait"] += f
        t["sans_taxe"] += s
        t["reel"] += r
        ecart = abs(f - o["ref"])
        ecart_max = max(ecart_max, ecart)
        if ecart > tolerance(M.CAPITAL, o["prix_entree"], o["prix_sortie"]):
            hors.append(dict(o, forfait=round(f, 2)))
        g = groupes.setdefault((o["date_entree"][:4], bool(M.valeur_taxee(o["valeur"], o["date_entree"]))), [0, 0.0])
        g[0] += 1
        g[1] += f - r
    res = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in t.items()}
    res.update(ecart_golden_reel=round(t["ref"] - t["reel"], 2), ecart_forfait_reel=round(t["forfait"] - t["reel"], 2),
               part_courtage=round(t["forfait"] - t["sans_taxe"], 2), part_taxe=round(t["sans_taxe"] - t["reel"], 2),
               par_groupe={k: [v[0], round(v[1], 2)] for k, v in sorted(groupes.items())},
               hors_tolerance=hors, ecart_max=round(ecart_max, 2), confirmee=bool(t["n"]) and not hors)
    return res


def ecrire_le_rapport(chemin, res, entete):
    """Écrit rapports/CAUSE_DE_L_ECART_DE_GAIN_C5.md.

    ① RÔLE — Mettre la mesure et le verdict par écrit ; aucun chiffre tapé à la main.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve (dossier jetable).
    ③ ENTRÉE — `chemin`, `res` de `mesurer`, `entete` (lignes de provenance).
    ④ CONDITIONS D'ENTRÉE — Le dossier de `chemin` peut être créé.
    ⑤ SORTIE — UNE valeur : le texte écrit.
    [rend: 1]
    ⑥ TRAITEMENT — hypothèse, totaux, décomposition, groupes, opérations hors tolérance, verdict.
    ⑦ UNITÉ — EUROS au centime.
    ⑧ POURQUOI — Défaut I-2 de la relecture Cowork du 21-11-2026 : la section était écrite à la main dans un rapport
    qu'un autre programme réécrit en entier ; elle vit maintenant dans son propre fichier, fabriqué ici.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le fichier.
    ⑪ TERMINAISON — Lève sur une écriture impossible.
    [sort: non]
    """
    pc = lambda x: "%.1f %%" % (100.0 * x / res["ecart_forfait_reel"]) if res["ecart_forfait_reel"] else "—"
    t = ["# CAUSE DE L'ÉCART DE GAIN DE C5 — forfait du golden contre barème réel", "",
         "Simulation uniquement. Programme : programmes/EXPLIQUER_L_ECART_DE_GAIN_C5.py. Fichier fabriqué : ne pas "
         "l'éditer à la main. Aucun cours n'est lu ni affiché.", ""]
    t += ["- " + e for e in entete]
    t += ["", "## HYPOTHÈSE", "",
          "Le golden comptait un forfait de 300 € par opération (barème %s) ; le module applique le barème réel "
          "(sans argument, A-550, avec la taxe sur les transactions financières). Si c'est la seule cause, chaque gain "
          "du golden se retrouve au forfait, à l'arrondi des prix du tableau près." % FORFAIT, "",
          "## TOTAUX SUR LES %d OPÉRATIONS DU TABLEAU" % res["n"], "",
          "- golden (tableau) : %+.2f €" % res["ref"],
          "- recalculé au forfait : %+.2f €" % res["forfait"],
          "- recalculé au courtage réel sans taxe (%s) : %+.2f €" % (SANS_TAXE, res["sans_taxe"]),
          "- recalculé au barème réel : %+.2f €" % res["reel"],
          "- écart golden − réel : %.2f € ; écart forfait − réel : %.2f €" % (res["ecart_golden_reel"],
                                                                         res["ecart_forfait_reel"]),
          "- dont courtage (forfait − sans taxe) : %.2f € (%s) ; dont taxe (sans taxe − réel) : %.2f € (%s)"
          % (res["part_courtage"], pc(res["part_courtage"]), res["part_taxe"], pc(res["part_taxe"])),
          "- écart maximal d'une opération, forfait contre golden : %.2f €" % res["ecart_max"], "",
          "## ÉCART FORFAIT − RÉEL PAR ANNÉE D'ENTRÉE ET PAR TAXE", "",
          "année | valeur taxée | opérations | écart €", "--- | --- | --- | ---"]
    t += ["%s | %s | %d | %.2f" % (a, "oui" if tx else "non", n, e) for (a, tx), (n, e) in res["par_groupe"].items()]
    t += ["", "## OPÉRATIONS HORS TOLÉRANCE (forfait contre golden)", "",
          "valeur | entrée | sortie | golden € | forfait €", "--- | --- | --- | --- | ---"]
    t += ["%s | %s | %s | %+.2f | %+.2f" % (o["valeur"], o["date_entree"], o["date_sortie"], o["ref"], o["forfait"])
          for o in res["hors_tolerance"]]
    t += ["", "## VERDICT", "",
          ("hypothèse CONFIRMÉE : les %d opérations se retrouvent au forfait ; l'écart de gain vient du seul régime de "
           "frais." % res["n"]) if res["confirmee"] else
          ("hypothèse RÉFUTÉE : %d opération(s) hors tolérance au forfait." % len(res["hors_tolerance"])), ""]
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
    ⑥ TRAITEMENT — fiche en tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — fiche en tête, ⑩.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    inconnus = [a for a in sys.argv[1:] if not (a.startswith("--") and "=" in a)
                or a[2:].split("=", 1)[0] not in ("racine", "sortie")]
    if inconnus:
        print("usage : EXPLIQUER_L_ECART_DE_GAIN_C5.py [--racine=…] [--sortie=…] ; inconnu : %s" % inconnus)
        return 2
    racine = os.path.abspath(opts.get("racine", os.path.dirname(ICI)))
    sortie = opts.get("sortie", os.path.join(racine, "rapports", "CAUSE_DE_L_ECART_DE_GAIN_C5.md"))
    p = os.path.join(racine, "programmes")
    try:
        J = charger(os.path.join(p, "JUGE_DES_STRATEGIES.py"), "JUGE_DES_STRATEGIES")
        C = charger(os.path.join(p, "CONTRATS_DES_FICHIERS.py"), "CONTRATS_DES_FICHIERS")
        K = charger(os.path.join(p, "COMPARER_LE_CALIBRAGE_C5.py"), "COMPARER_LE_CALIBRAGE_C5")
        M = charger(os.path.join(p, "MODULE_POSITIONS.py"), "MODULE_POSITIONS")
        f_tab = J.trouver(racine, "TABLEAU_100_TRADES_C5E10")
        if not f_tab:
            print("ARRÊT : tableau des 100 trades introuvable sous %s" % racine)
            return 2
        operations = lire_le_tableau(f_tab, K.gain)
        _deb, fin_regard = C.fenetre_du_regard_unique()
        dates = [o[k] for o in operations for k in ("date_signal", "date_entree", "date_sortie")]
        if not dates or min(dates) <= fin_regard:
            print("ARRÊT : le tableau porte une date dans la fenêtre du regard unique (ou est vide) — rien n'est calculé.")
            return 2
        res = mesurer(operations, M)
    except Exception as e:  # le calcul n'a pas pu tourner (R-734)
        print("ARRÊT : %s: %s" % (type(e).__name__, e))
        return 2
    rel = lambda x: os.path.relpath(x, racine)
    entete = ["date du rapport : %s" % J.horodatage(), "tableau : %s" % rel(f_tab),
              "calcul : `MODULE_POSITIONS.pnl_net`, barèmes %s, %s et réel (sans argument)" % (FORFAIT, SANS_TAXE),
              "lien au rejeu d'aujourd'hui : `programmes/COMPARER_LE_CALIBRAGE_C5.py --bareme=%s` (voir "
              "rapports/CALIBRAGE_C5.md pour le rejeu au barème réel)" % FORFAIT]
    ecrire_le_rapport(sortie, res, entete)
    print("%d opérations · golden %.2f · forfait %.2f · sans taxe %.2f · réel %.2f · écart forfait-réel %.2f "
          "(courtage %.2f, taxe %.2f) · écart max %.2f · hors tolérance %d"
          % (res["n"], res["ref"], res["forfait"], res["sans_taxe"], res["reel"], res["ecart_forfait_reel"],
             res["part_courtage"], res["part_taxe"], res["ecart_max"], len(res["hors_tolerance"])))
    print("verdict : %s · rapport : %s" % ("CONFIRMÉE" if res["confirmee"] else "RÉFUTÉE", rel(sortie)))
    return 0 if res["confirmee"] else 1


if __name__ == "__main__":
    sys.exit(main())
