#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Épreuves de `programmes/MESURER_LES_INDICATEURS.py` — sur les vraies opérations du golden, avec sabotages.

Simulation uniquement : aucun ordre réel n'est jamais passé. Écrit le samedi 14-11-2026 (Paris).

① RÔLE — Prouver que chaque indicateur d'A-788 est juste sur de vraies opérations (le golden du 01-08-2026, rejoué
  par le circuit), et que chaque épreuve ROUGIT quand on casse le calcul qu'elle surveille.
② CONTEXTE D'APPEL — À la main, par le Chat, le relecteur ou Cowork :
  `python3 -B tests/EPREUVES_DES_INDICATEURS_Sam_14-11-2026.py .` (les cas) ;
  `… . --saboter` (les cas, puis chaque sabotage, qui doit faire rougir au moins un cas) ;
  `… . --comparer` (la mesure des trois creux et des deux durées, sans verdict) ;
  `… . --mesurer-l-arrondi` (l'effet de l'arrondi au centime du seuil exact sur de vraies opérations, sans verdict).
③ ENTRÉE — La ligne de commande : la racine du dépôt, puis une option facultative.
④ CONDITIONS D'ENTRÉE — Celles de `calibrer_sur_le_golden` ; et, pour les témoins indépendants,
  `etudes/JOURNEE_01-11-2026/alarme_seuils/sorties/trades_c5_un_jeton.csv` et le module de signal de C5.
⑤ SORTIE — Un code de sortie : 0 si tout tient (et, avec `--saboter`, si chaque sabotage mord) ; 1 si un cas tombe
  ou si un sabotage ne mord pas ; 2 si un contrôle n'a pas pu tourner (R-734).
⑥ TRAITEMENT — Voir `cas`, `sabotages`, `comparer`.
⑦ UNITÉ — Euros au centime, pourcents, jours calendaires, comptes.
⑧ POURQUOI — R-731 : tout code passe des épreuves avec sabotages ; R-732 : un cas au moins vient d'une VRAIE
  ligne (ici : les 44 et 100 opérations du golden) ; « une épreuve qui reste verte quand on retire ce qu'elle teste
  n'est pas une preuve, c'est une décoration ».
⑨ CE QUI CLOCHE — Une valeur reste FIGÉE comme témoin de régression : la borne basse du gain (597,73 €), que le
  relecteur INDIC a retrouvée exactement (loi binomiale), mais qui dépend de la graine de `borne_basse_gain` (une
  graine sur dix donne 450 €). Les seuils 1 sur 20 ont des témoins indépendants (relecteur, superviseur) et les
  durées sous l'eau des cas faits à la main (lot INDIC-1, 14-11-2026). Le creux du radar est recopié en trois lignes
  dans `comparer` : sa fonction est imbriquée dans le corps du radar et ne s'importe pas sans lancer tout l'audit.
⑩ EFFET — Lit ; n'écrit aucun fichier ; affiche.
⑪ TERMINAISON — Rend la main au bas du fichier, qui sort avec le code.
"""

import os
import sys
import csv
import math
import importlib.util

RACINE = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
sys.path.insert(0, os.path.join(RACINE, "programmes"))


def charger():
    """Charge le programme éprouvé, neuf, et rend le module.

    ① RÔLE — Donner aux cas un module propre, sans les sabotages d'un tour précédent.
    ② CONTEXTE D'APPEL — `main`, une fois par tour (normal puis chaque sabotage).
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — `programmes/MESURER_LES_INDICATEURS.py` existe sous la racine.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — charger le fichier sous un nom neuf.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sabotage qui survit au tour suivant fausserait le tour suivant.
    ⑨ CE QUI CLOCHE — Les briques (juge, modules) sont gardées en mémoire entre les tours : un sabotage qui les
      touche doit les restaurer lui-même (fait par `sabotages`).
    ⑩ EFFET — Exécute le chargement du programme.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("MESURER_LES_INDICATEURS",
                                                os.path.join(RACINE, "programmes", "MESURER_LES_INDICATEURS.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def charger_mute(remplacements):
    """Charge le programme éprouvé depuis son texte MODIFIÉ en mémoire, pour un sabotage du code lui-même.

    ① RÔLE — Casser une ligne précise du programme sans toucher au fichier.
    ② CONTEXTE D'APPEL — Les sabotages qui portent sur une condition écrite dans une fonction.
    ③ ENTRÉE — `remplacements` : une liste de couples (texte d'origine, texte saboté).
    ④ CONDITIONS D'ENTRÉE — Chaque texte d'origine paraît EXACTEMENT une fois dans le programme.
    ⑤ SORTIE — UNE valeur : le module saboté.
      [rend: 1]
    ⑥ TRAITEMENT — lire le texte, remplacer, exécuter dans un module neuf.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un sabotage par enveloppe ne peut pas changer une comparaison écrite au milieu d'une fonction
      (par exemple « > » en « >= ») ; celui-ci le peut.
    ⑨ CE QUI CLOCHE — Un texte d'origine absent ou en double fait lever : `main` affiche alors « SABOTAGE NON
      POSÉ » et rend le code 1 ; c'est voulu (il faut le voir et le réécrire).
    ⑩ EFFET — Lit le programme ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` si un texte d'origine n'est pas unique.
      [sort: non]
    """
    f = os.path.join(RACINE, "programmes", "MESURER_LES_INDICATEURS.py")
    t = open(f, encoding="utf-8").read()
    for a, b in remplacements:
        if t.count(a) != 1:
            raise ValueError("sabotage : %r paraît %d fois" % (a[:60], t.count(a)))
        t = t.replace(a, b)
    import types
    m = types.ModuleType("MESURER_LES_INDICATEURS")
    m.__file__ = f
    exec(compile(t, f, "exec"), m.__dict__)
    return m


def proche(a, b, tol=0.005):
    """Dit si deux nombres sont égaux à la tolérance près.

    ① RÔLE — La comparaison de tous les cas chiffrés.
    ② CONTEXTE D'APPEL — `cas`.
    ③ ENTRÉE — `a` : l'obtenu · `b` : l'attendu · `tol` : l'écart permis, un demi-centime par défaut.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai ou faux ; faux si l'un est `None` et pas l'autre.
      [rend: 1]
    ⑥ TRAITEMENT — écart absolu ≤ tolérance.
    ⑦ UNITÉ — Celle des nombres comparés.
    ⑧ POURQUOI — Une seule façon de comparer.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= tol


def cas(M):
    """Joue tous les cas sur le module donné et rend la liste (nom, tenu, détail).

    ① RÔLE — Le jeu d'épreuves lui-même.
    ② CONTEXTE D'APPEL — `main`, au tour normal puis à chaque sabotage.
    ③ ENTRÉE — `M` : le module éprouvé, éventuellement saboté.
    ④ CONDITIONS D'ENTRÉE — Celles du ④ du fichier.
    ⑤ SORTIE — UNE valeur : la liste des cas.
      [rend: 1]
    ⑥ TRAITEMENT — T01 calibrage au centime · T02 les 44 opérations contre l'étude du 01-11 · T03 contre
      `backtest_c5etendu10` · T04 opérations par mois · T05 jours entre deux gains · T06 taux et Wilson (contre la
      formule de la mesure du soir) · T07 gain moyen et sa borne · T08 gagnante et perdante moyennes · T09 gain par
      an et sa borne · T10 pire creux (témoins 14 000 € et 22 500 €) · T11 jours sous l'eau (témoin 156 j) · T12
      plus longue série · T13 seuils 1 sur 20 (cas dégénérés exacts et témoin figé) · T14 Kelly (contre `_kelly`
      de la porte et la formule fermée) · T15 Sortino (formule fermée) · T16 Calmar · T17 refus d'entrée · T18
      départage · T19 garde du regard unique.
    ⑦ UNITÉ — Celles des indicateurs.
    ⑧ POURQUOI — Chaque indicateur a au moins un cas qui le pince ; chaque cas a un sabotage qui le fait rougir.
    ⑨ CE QUI CLOCHE — Voir le ⑨ du fichier : trois témoins figés de régression.
    ⑩ EFFET — Appelle le module ; aucune écriture.
    ⑪ TERMINAISON — Rend la main ; une exception dans un cas est attrapée et le cas tombe.
      [sort: non]
    """
    R = []

    def note(nom, f):
        """Joue un cas et l'inscrit, en attrapant toute exception comme un échec.

        ① RÔLE — Inscrire un cas.
        ② CONTEXTE D'APPEL — `cas`, une fois par cas.
        ③ ENTRÉE — `nom` : le nom du cas · `f` : une fonction sans argument qui rend (tenu, détail).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — appeler `f`, inscrire, ou inscrire l'exception.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un cas qui lève ne doit pas arrêter les autres.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Ajoute à la liste des cas.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        try:
            ok, det = f()
        except Exception as e:  # le cas tombe, il ne lève pas
            ok, det = False, "%s: %s" % (type(e).__name__, str(e)[:160])
        R.append((nom, bool(ok), det))

    garde_departage = M.ordre_de_departage
    ok_cal, lignes, rendu = M.calibrer_sur_le_golden(RACINE)
    import json
    golden = json.load(open(M.charger_les_briques(RACINE)["JS"].trouver(
        os.path.join(RACINE, "gouvernance"), "golden_tests_"), encoding="utf-8"))["C5-ETENDU-10"]
    uj, ji = rendu.get("un_jeton", []), rendu.get("jetons_illimites", [])
    per = rendu.get("periode")
    b = M.charger_les_briques(RACINE)

    note("T01 calibrage au centime, deux comptabilités", lambda: (
        ok_cal and len(uj) == golden["un_jeton"]["n"] and proche(sum(o["net"] for o in uj), golden["un_jeton"]["net"])
        and len(ji) == golden["jetons_illimites"]["n"]
        and proche(sum(o["net"] for o in ji), golden["jetons_illimites"]["net"]), " | ".join(lignes[-2:])))

    def t01c():
        """Éprouve que le programme lancé seul rend le code 1 sous un départage alphabétique.

        ① RÔLE — Le calibrage doit refuser la mauvaise règle, pas seulement l'épreuve (relecteur INDIC, D3).
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — module neuf, départage remplacé par l'ordre alphabétique, `main` lancé sur la racine, sortie
          avalée ; exiger le code 1.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Avec l'ordre alphabétique, les totaux du golden sont retrouvés et deux opérations changent.
        ⑨ CE QUI CLOCHE — Le module saboté est celui que `M` désigne : si `M` est déjà saboté ailleurs, le cas
          porte sur ce module-là.
        ⑩ EFFET — Lance `main` ; aucune écriture.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        import io
        import contextlib
        M.ordre_de_departage = lambda sj: sorted(sj, key=lambda x: x["valeur"])
        argv = sys.argv
        sys.argv = ["MESURER_LES_INDICATEURS.py", RACINE]
        try:
            with contextlib.redirect_stdout(io.StringIO()) as sortie:
                code = M.main()
        finally:
            sys.argv = argv
            M.ordre_de_departage = garde_departage
        return code == 1, "code %s ; %s" % (code, [l for l in sortie.getvalue().split("\n") if "une à une" in l][:2])

    def t02():
        """Compare les 44 opérations rejouées à celles reconstruites par l'étude du 01-11-2026.

        ① RÔLE — Témoin indépendant, opération par opération.
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — Le fichier de l'étude existe.
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — même valeur (rapprochée par `cle_valeur`), mêmes dates d'entrée et de sortie, même net au
          forfait, dans l'ordre.
        ⑦ UNITÉ — Euros.
        ⑧ POURQUOI — L'empreinte des opérations du golden ne se recalcule pas (recette introuvable) ; la liste
          reconstruite par l'étude, qui retrouve le golden, en tient lieu.
        ⑨ CE QUI CLOCHE — L'étude a été construite depuis le tableau des 100 trades, pas par le circuit : c'est
          justement ce qui la rend indépendante.
        ⑩ EFFET — Lit le fichier de l'étude.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        f = os.path.join(RACINE, "etudes", "JOURNEE_01-11-2026", "alarme_seuils", "sorties", "trades_c5_un_jeton.csv")
        ref = list(csv.DictReader(open(f, encoding="utf-8")))
        cle = b["JS"].cle_valeur      # deux graphies d'une même société (R-719) : UNIBAIL_RODAMCO(_WESTFIELD)
        a = [(cle(o["valeur"]), o["date_entree"], o["date_sortie"], round(o["net"], 2)) for o in uj]
        e = [(cle(r["valeur"]), r["date_entree"], r["date_sortie"], round(float(r["net_forfait"]), 2)) for r in ref]
        diff = [x for x, y in zip(a, e) if x != y]
        return a == e, "%d rejouées, %d témoins, %d différences %s" % (len(a), len(e), len(diff), diff[:1])
    note("T02 les 44 opérations un jeton = celles de l'étude du 01-11-2026", t02)

    note("T03 le calibrage compare les opérations une à une à backtest_c5etendu10 (il l'appelle, l'épreuve ne recopie rien)",
         lambda: (all(any(l.startswith("OK %s : opérations une à une" % c) for l in lignes)
                      for c in ("un_jeton", "jetons_illimites")), " | ".join(l for l in lignes if "une à une" in l)))
    note("T01c départage alphabétique : le programme lancé seul rend le code 1", t01c)

    def t03b():
        """Éprouve que la comparaison au producteur du golden compte les doublons et lit la date de sortie.

        ① RÔLE — Pincer N4 (relecteur INDIC, tour 2).
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — DANS LES DEUX COMPTABILITÉS (Cowork, C2) : ① les opérations rejouées, telles quelles :
          0 différence · ② une opération en double : au moins une différence · ③ une date de sortie décalée :
          au moins une différence.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une comparaison d'ensembles ne voit pas un doublon ; sans la date de sortie, une sortie fausse
          passe.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Relit les cours du témoin.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        cours = b["JS"].charger_cours(os.path.join(RACINE, "temoins", "TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv"))
        tel = M.comparer_au_producteur_du_golden(RACINE, cours, per[1], {"un_jeton": uj, "jetons_illimites": ji})
        double = M.comparer_au_producteur_du_golden(RACINE, cours, per[1], {"un_jeton": uj + uj[:1],
                                                                            "jetons_illimites": ji + ji[:1]})
        decale = M.comparer_au_producteur_du_golden(RACINE, cours, per[1], {
            "un_jeton": [dict(uj[0], date_sortie="2024-02-29")] + uj[1:],
            "jetons_illimites": [dict(ji[0], date_sortie="2024-02-29")] + ji[1:]})
        c = ("un_jeton", "jetons_illimites")
        return (all(tel[k][0] == 0 and double[k][0] > 0 and decale[k][0] > 0 for k in c),
                "%s / doublon %s / sortie %s" % ([tel[k][0] for k in c], [double[k][0] for k in c],
                                                [decale[k][0] for k in c]))
    note("T03b comparaison au producteur : un doublon et une date de sortie fausse sont vus", t03b)

    # jetons illimités : le seuil de creux se tire (calcul exact infaisable) ; 20 000 tirages suffisent ici, aucun cas
    # ne lit ce seuil-là, et 200 000 coûteraient une dizaine de secondes à chaque tour de sabotage
    I = {"un_jeton": M.mesurer_les_indicateurs(uj, "un_jeton", per, RACINE),
         "jetons_illimites": M.mesurer_les_indicateurs(ji, "jetons_illimites", per, RACINE, tirages_du_seuil=20000)}
    u, j = I["un_jeton"], I["jetons_illimites"]
    jours = 920.0  # 2024-01-02 → 2026-07-10, compté par le calendrier : vérifié dans T04
    from datetime import date
    jours_calendrier = (date.fromisoformat(per[1]) - date.fromisoformat(per[0])).days
    note("T04 opérations et opérations par mois", lambda: (
        jours_calendrier == jours and u["operations"] == 44 and proche(u["operations_par_mois"], 44 * 365.25 / 12 / jours, 1e-9)
        and proche(j["operations_par_mois"], 100 * 365.25 / 12 / jours, 1e-9),
        "%s / %s" % (u["operations_par_mois"], j["operations_par_mois"])))
    note("T05 un gain tous les X jours (920 j ÷ 28 gains ; ÷ 61)", lambda: (
        proche(u["jours_entre_deux_gains"], jours / 28, 1e-9) and proche(j["jours_entre_deux_gains"], jours / 61, 1e-9)
        and M.jours_entre_deux_gains(0, per) is None, "%s / %s" % (u["jours_entre_deux_gains"], j["jours_entre_deux_gains"])))
    note("T06 taux et borne de Wilson = formule de la mesure du soir", lambda: (
        proche(u["taux_reussite_pct"], 100 * 28 / 44, 1e-9)
        and proche(u["taux_reussite_borne_basse_pct"], b["MES"].wilson_borne_basse(28, 44), 1e-9)
        and proche(j["taux_reussite_borne_basse_pct"], b["MES"].wilson_borne_basse(61, 100), 1e-9),
        "%.6f / %.6f" % (u["taux_reussite_borne_basse_pct"], j["taux_reussite_borne_basse_pct"])))
    note("T07 gain moyen exact et borne basse (témoin figé 597,73 € ; égale au gain si tout est égal)", lambda: (
        proche(u["gain_moyen_eur"], 58800 / 44, 1e-9) and proche(u["gain_moyen_borne_basse_eur"], 597.73)
        and u["gain_moyen_borne_basse_eur"] < u["gain_moyen_eur"]
        and proche(M.mesurer_les_indicateurs([dict(o, net=1000.0) for o in uj], "un_jeton", per, RACINE)
                   ["gain_moyen_borne_basse_eur"], 1000.0),
        "%s / %s" % (u["gain_moyen_eur"], u["gain_moyen_borne_basse_eur"])))
    note("T08 gagnante +3 700 € et perdante −2 800 € (forfait), illimités", lambda: (
        proche(u["gagnante_moyenne_eur"], 3700.0) and proche(u["perdante_moyenne_eur"], -2800.0)
        and proche(j["gagnante_moyenne_eur"] * 61 + j["perdante_moyenne_eur"] * 39, 111334.24, 0.01)
        and M.moyennes_gagnante_perdante([5.0]) == (5.0, None),
        "%s %s / %s %s" % (u["gagnante_moyenne_eur"], u["perdante_moyenne_eur"], j["gagnante_moyenne_eur"], j["perdante_moyenne_eur"])))
    note("T09 gain net par an et sa borne basse", lambda: (
        proche(u["gain_net_par_an_eur"], 58800 * 365.25 / jours, 1e-6)
        and proche(u["gain_net_par_an_borne_basse_eur"], u["gain_moyen_borne_basse_eur"] * 44 * 365.25 / jours, 1e-6),
        "%s / %s" % (u["gain_net_par_an_eur"], u["gain_net_par_an_borne_basse_eur"])))
    note("T10 pire creux : 14 000 € (étude du 01-11) et 22 500 € (rapport PERFORMANCE)", lambda: (
        proche(u["pire_creux_eur"], 14000.0) and proche(j["pire_creux_eur"], 22500.0)
        and M.creux_du_compte([], RACINE) == 0.0, "%s / %s" % (u["pire_creux_eur"], j["pire_creux_eur"])))
    note("T11a A-798, les deux chiffres : creux rattrapé le plus long 93 j ; creux en cours non sorti, 65 j, 14 000 €",
         lambda: ((u["jours_plus_long_creux_rattrape"], u["creux_en_cours_sorti"], u["jours_du_creux_en_cours"],
                   u["creux_en_cours_eur"], j["jours_plus_long_creux_rattrape"])
                  == (93, False, 65, 14000.0, 156),
                  "%s %s %s %s / %s" % (u["jours_plus_long_creux_rattrape"], u["creux_en_cours_sorti"],
                                        u["jours_du_creux_en_cours"], u["creux_en_cours_eur"],
                                        j["jours_plus_long_creux_rattrape"])))

    def t11e():
        """Éprouve que les DEUX chiffres d'A-798 sont rendus ET affichés, aucun ne remplaçant l'autre.

        ① RÔLE — Rougir si l'un des deux chiffres disparaît (demande du Chat après A-798).
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — ① les cases des deux chiffres sont présentes et non vides sur le golden un jeton · ② `main`,
          lancé sur la racine, affiche les deux lignes.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — A-798 (Jean-Luc, 14-11-2026 à 20h22, « 3 ») : les deux s'affichent, aucun n'est choisi par défaut.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Lance `main` ; aucune écriture.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        import io
        import contextlib
        argv = sys.argv
        sys.argv = ["MESURER_LES_INDICATEURS.py", RACINE]
        try:
            with contextlib.redirect_stdout(io.StringIO()) as sortie:
                M.main()
        finally:
            sys.argv = argv
        texte = sortie.getvalue()
        cles = ("jours_plus_long_creux_rattrape", "jours_du_creux_en_cours", "creux_en_cours_sorti")
        rendus = all(u.get(k) is not None for k in cles)
        affiches = all(texte.count(k) >= 2 for k in cles)
        return rendus and affiches, "rendus %s · affichés %s" % (rendus, [texte.count(k) for k in cles])
    note("T11e les deux chiffres d'A-798 sont rendus et affichés (deux comptabilités)", t11e)
    perte = [{"valeur": "X", "date_signal": "2024-01-09", "date_entree": "2024-01-10", "date_sortie": "2024-01-11",
              "net": -2800.0}]
    note("T11b une seule perte sur 30 j : creux en cours, non sorti, 30 j, 2 800 € ; aucun rattrapé (l'ancien : 0 j)", lambda: (
        M.episodes_sous_l_eau(perte, ("2024-01-01", "2024-01-31"))["jours_du_creux_en_cours"] == 30
        and M.episodes_sous_l_eau(perte, ("2024-01-01", "2024-01-31"))["creux_en_cours_sorti"] is False
        and M.episodes_sous_l_eau(perte, ("2024-01-01", "2024-01-31"))["jours_plus_long_creux_rattrape"] is None
        and M.episodes_sous_l_eau(perte, ("2024-01-01", "2024-01-31"))["episodes"][0]["profondeur_eur"] == 2800.0,
        str(M.episodes_sous_l_eau(perte, ("2024-01-01", "2024-01-31")))))
    egal = [dict(perte[0], date_sortie="2024-01-11", net=1000.0), dict(perte[0], date_sortie="2024-01-15", net=-500.0),
            dict(perte[0], date_sortie="2024-01-20", net=500.0), dict(perte[0], date_sortie="2024-01-25", net=1.0)]
    note("T11c un retour EXACT au sommet n'est pas une sortie (sommet du 11, égalité le 20, dépassé le 25 : 14 j)",
         lambda: (M.episodes_sous_l_eau(egal, ("2024-01-01", "2024-01-31"))["episodes"] ==
                  [{"date_sommet": "2024-01-11", "sommet_eur": 1000.0, "profondeur_eur": 500.0,
                    "sortie": "2024-01-25", "jours": 14, "sorti": True}],
                  str(M.episodes_sous_l_eau(egal, ("2024-01-01", "2024-01-31"))["episodes"])))
    cent = [dict(perte[0], date_sortie="2024-01-03", net=148.63), dict(perte[0], date_sortie="2024-01-05", net=-4683.56),
            dict(perte[0], date_sortie="2024-01-08", net=4683.56)]
    cent += [dict(perte[0], date_sortie="2024-01-10", net=-0.29)]
    note("T11f retour EXACT au sommet en centimes (148,63 − 4 683,56 + 4 683,56 − 0,29) : creux en cours, non sorti, "
         "sommet 148,63 € et profondeur 4 683,56 € exacts ; une perte seule de 0,29 € vaut 0,29 €",
         lambda: (M.episodes_sous_l_eau(cent, ("2024-01-01", "2024-01-31"))["creux_en_cours_sorti"] is False
                  and M.episodes_sous_l_eau(cent, ("2024-01-01", "2024-01-31"))["jours_plus_long_creux_rattrape"] is None
                  and M.episodes_sous_l_eau(cent, ("2024-01-01", "2024-01-31"))["episodes"] ==
                  [{"date_sommet": "2024-01-03", "sommet_eur": 148.63, "profondeur_eur": 4683.56, "sortie": None,
                    "jours": 28, "sorti": False}]
                  and M.episodes_sous_l_eau([dict(perte[0], net=-0.29)], ("2024-01-01", "2024-01-31"))
                  ["creux_en_cours_eur"] == 0.29,
                  str(M.episodes_sous_l_eau(cent, ("2024-01-01", "2024-01-31"))["episodes"])))
    frac = [dict(perte[0], date_sortie="2024-01-0%d" % k, net=x)
            for k, x in ((3, 100.0049), (4, -25.0049), (5, -25.0049), (8, 50.0051))]
    frac_sort = frac[:3] + [dict(frac[3], net=50.0141)]
    note("T11g gains à fractions de centime (Cowork, C1) : 100,0049 − 25,0049 − 25,0049 + 50,0051 reste 0,0047 € sous le "
         "sommet (non sorti) ; avec + 50,0141 il le dépasse de 0,0043 € (sorti le 08)",
         lambda: (M.episodes_sous_l_eau(frac, ("2024-01-01", "2024-01-31"))["creux_en_cours_sorti"] is False
                  and M.episodes_sous_l_eau(frac_sort, ("2024-01-01", "2024-01-31"))["episodes"][0]["sortie"]
                  == "2024-01-08",
                  "%s / %s" % (M.episodes_sous_l_eau(frac, ("2024-01-01", "2024-01-31"))["episodes"],
                               M.episodes_sous_l_eau(frac_sort, ("2024-01-01", "2024-01-31"))["episodes"])))
    dec = [dict(perte[0], date_sortie="2024-01-03", net=0.3), dict(perte[0], date_sortie="2024-01-05", net=-0.3),
           dict(perte[0], date_sortie="2024-01-08", net=0.1), dict(perte[0], date_sortie="2024-01-08", net=0.2)]
    six = [dict(perte[0], date_sortie="2024-01-03", net=1.000001), dict(perte[0], date_sortie="2024-01-05", net=-1.0),
           dict(perte[0], date_sortie="2024-01-08", net=1.0000015)]
    note("T11h lecture DÉCIMALE et aucun arrondi (Cowork, E1) : +0,3 −0,3 puis +0,1 +0,2 le même jour revient PILE au "
         "sommet (non sorti) ; +1,000001 −1 +1,0000015 le dépasse de 0,0000005 € (sorti le 08)",
         lambda: (M.episodes_sous_l_eau(dec, ("2024-01-01", "2024-01-31"))["creux_en_cours_sorti"] is False
                  and M.episodes_sous_l_eau(six, ("2024-01-01", "2024-01-31"))["episodes"][0]["sortie"] == "2024-01-08",
                  "%s / %s" % (M.episodes_sous_l_eau(dec, ("2024-01-01", "2024-01-31"))["episodes"],
                               M.episodes_sous_l_eau(six, ("2024-01-01", "2024-01-31"))["episodes"])))
    note("T11d confrontation : profondeur des épisodes = pire_chute = calculer_time_underwater (golden, deux comptabilités)",
         lambda: (all(proche(max(e["profondeur_eur"] for e in M.episodes_sous_l_eau(o, per)["episodes"]),
                             M.creux_du_compte(o, RACINE))
                      and proche(b["MS"].calculer_time_underwater(
                          [{"date": x["date_sortie"], "gain": x["net"]} for x in o])["dd_max_eur"],
                          M.creux_du_compte(o, RACINE)) for o in (uj, ji)), "14000 / 22500"))
    note("T12 plus longue série de pertes = 5 (rapport PERFORMANCE ; 5 × 2 800 = le creux)", lambda: (
        u["plus_longue_serie_de_pertes"] == 5 and j["plus_longue_serie_de_pertes"] == 5,
        "%s / %s" % (u["plus_longue_serie_de_pertes"], j["plus_longue_serie_de_pertes"])))

    def t13():
        """Éprouve les seuils 1 sur 20 sur 5 ans : valeurs exactes du golden, cas dégénérés, tirage contre exact.

        ① RÔLE — Pincer le nombre d'opérations de cinq ans, la loi exacte de la série, le creux exact et le repli
          par tirage.
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — ① golden un jeton (87 opérations) : creux 21 500 € par la méthode exacte, série 6 avec
          P(≤ 6) = 0,9571 · ② toutes pertes −1 000 €, 10 par an → 50 sur 5 ans : 50 000 € et 50 · ③ tout gain : 0
          et 0 · ④ le repli par tirage (calcul exact interdit) à 200 000 tirages retrouve 21 500 € et sa marge le
          contient.
        ⑦ UNITÉ — Euros ; opérations ; probabilité.
        ⑧ POURQUOI — Les valeurs ① viennent de deux calculs indépendants du lot : la chaîne de Markov du relecteur
          INDIC (21 500 €, P(≤ 21 500) = 0,9563) et la programmation dynamique du superviseur (série 6,
          P(≤ 6) = 0,9571). Le ④ confronte les deux méthodes du lot.
        ⑨ CE QUI CLOCHE — Le ④ coûte une dizaine de secondes.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        a = M.seuils_1_sur_20_sur_5_ans([-1000.0], 10.0, RACINE)
        z = M.seuils_1_sur_20_sur_5_ans([1000.0], 10.0, RACINE)
        nets = [o["net"] for o in uj]
        t = M.seuils_1_sur_20_sur_5_ans(nets, 44 / (jours / 365.25), RACINE, etats_max=1)
        ok = (proche(u["creux_1_sur_20_sur_5_ans_eur"], 21500.0) and u["creux_1_sur_20_sur_5_ans_methode"] == "exacte"
              and u["serie_1_sur_20_sur_5_ans"] == 6 and proche(u["serie_1_sur_20_sur_5_ans_probabilite"], 0.9571, 5e-5)
              and (a["creux_eur"], a["serie"]) == (50000.0, 50) and (z["creux_eur"], z["serie"]) == (0.0, 0)
              and t["creux_methode"] == "tirages" and proche(t["creux_eur"], 21500.0)
              and t["creux_marge_basse_eur"] <= 21500.0 <= t["creux_marge_haute_eur"])
        return ok, "golden %s %s %s %.4f / %s %s / %s %s / tirage %s [%s ; %s]" % (
            u["creux_1_sur_20_sur_5_ans_eur"], u["creux_1_sur_20_sur_5_ans_methode"], u["serie_1_sur_20_sur_5_ans"],
            u["serie_1_sur_20_sur_5_ans_probabilite"], a["creux_eur"], a["serie"], z["creux_eur"], z["serie"],
            t["creux_eur"], t["creux_marge_basse_eur"], t["creux_marge_haute_eur"])
    note("T13 seuils 1 fois sur 20 sur 5 ans", t13)
    note("T13b ordre des marges du tirage (jetons illimités, 20 000 tirages) : basse ≤ seuil ≤ haute, basse < haute",
         lambda: (j["creux_1_sur_20_sur_5_ans_methode"] == "tirages"
                  and j["creux_1_sur_20_sur_5_ans_marge_basse_eur"] <= j["creux_1_sur_20_sur_5_ans_eur"]
                  <= j["creux_1_sur_20_sur_5_ans_marge_haute_eur"]
                  and j["creux_1_sur_20_sur_5_ans_marge_basse_eur"] < j["creux_1_sur_20_sur_5_ans_marge_haute_eur"],
                  "%s [%s ; %s]" % (j["creux_1_sur_20_sur_5_ans_eur"], j["creux_1_sur_20_sur_5_ans_marge_basse_eur"],
                                    j["creux_1_sur_20_sur_5_ans_marge_haute_eur"])))

    def t14():
        """Éprouve Kelly contre la porte (`JUGER_UNE_FICHE._kelly`) et contre la formule fermée du un jeton.

        ① RÔLE — Pincer Kelly.
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — `programmes/JUGER_UNE_FICHE.py` se charge.
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — ① `_kelly` sur les mêmes opérations, deux comptabilités · ② (p·b − q) ÷ b avec p = 28/44,
          b = 3 700 / 2 800, arrondi à quatre décimales.
        ⑦ UNITÉ — Fraction.
        ⑧ POURQUOI — La porte décide Kelly ≥ 0,05 (R-505 ⑨) : l'affiché doit être le même nombre.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Charge la porte.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        JF = b["JS"].charger_module(os.path.join(RACINE, "programmes", "JUGER_UNE_FICHE.py"), "porte_epreuve")
        ku, _ = JF._kelly(RACINE, {}, uj)
        kj, _ = JF._kelly(RACINE, {}, ji)
        p, q, bb = 28 / 44, 16 / 44, 3700 / 2800
        ferme = round((p * bb - q) / bb, 4)
        return (u["kelly"] == ku["kelly"] and j["kelly"] == kj["kelly"] and u["kelly"] == ferme,
                "%s %s %s / %s %s" % (u["kelly"], ku["kelly"], ferme, j["kelly"], kj["kelly"]))
    note("T14 Kelly = celui de la porte = formule fermée", t14)
    note("T15 Sortino = 1 336,36 ÷ (2 800 × √(16/44))", lambda: (
        proche(u["sortino"], (58800 / 44) / (2800 * math.sqrt(16 / 44)), 1e-9) and M.sortino([1.0, 2.0]) is None,
        "%s" % u["sortino"]))
    note("T16 Calmar = gain par an ÷ pire creux", lambda: (
        proche(u["calmar"], (58800 * 365.25 / jours) / 14000.0, 1e-9) and M.calmar(1.0, 0.0) is None, "%s" % u["calmar"]))

    def leve(f):
        """Rend vrai si l'appel lève `ValueError`.

        ① RÔLE — Éprouver un refus.
        ② CONTEXTE D'APPEL — T17, T18.
        ③ ENTRÉE — `f` : une fonction sans argument.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : vrai si `ValueError` est levée.
          [rend: 1]
        ⑥ TRAITEMENT — appeler, attraper.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un refus qui ne lève pas laisse passer une entrée fausse.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Celui de `f`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        try:
            f()
        except ValueError:
            return True
        return False
    chevauche = [dict(uj[0]), dict(uj[1], date_entree=uj[0]["date_sortie"])]
    note("T17 refus : un jeton qui chevauche, opération hors période, comptabilité inconnue", lambda: (
        leve(lambda: M.mesurer_les_indicateurs(chevauche, "un_jeton", per, RACINE))
        and not leve(lambda: M.mesurer_les_indicateurs(chevauche, "jetons_illimites", per, RACINE))
        and leve(lambda: M.mesurer_les_indicateurs(uj, "un_jeton", (per[0], "2025-01-01"), RACINE))
        and leve(lambda: M.mesurer_les_indicateurs(uj, "les_deux", per, RACINE)), "refus"))
    note("T18 départage R-207bis : CCI le plus bas, puis alphabétique ; CCI mêlés refusés", lambda: (
        [s["valeur"] for s in M.ordre_de_departage([{"valeur": "B", "cci": -60}, {"valeur": "A", "cci": -60},
                                                    {"valeur": "C", "cci": -90}])] == ["C", "A", "B"]
        and [s["valeur"] for s in M.ordre_de_departage([{"valeur": "B"}, {"valeur": "A"}])] == ["A", "B"]
        and leve(lambda: M.ordre_de_departage([{"valeur": "B", "cci": -60}, {"valeur": "A"}])), "ordre"))

    def t19():
        """Éprouve que le rejeu refuse une période dans la fenêtre du regard unique sans reçu.

        ① RÔLE — Le rejeu ne doit pas être une porte dérobée vers les années d'examen (R-505 ③).
        ② CONTEXTE D'APPEL — `cas`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : tenu, détail.
          [rend: 2]
        ⑥ TRAITEMENT — deux séances fabriquées en 2010, aucun signal, aucun reçu : le rejeu doit lever.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — La garde vit dans le juge ; le rejeu l'appelle.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        c = {"X": [{"date": "2010-03-01", "open": 1, "high": 1, "low": 1, "close": 1},
                   {"date": "2010-03-02", "open": 1, "high": 1, "low": 1, "close": 1}]}
        try:
            M.rejouer_les_signaux(RACINE, c, [], {}, "HIST_FORFAIT_300", "2010-12-31")
        except Exception as e:
            return type(e).__name__ == "RegardNonInscrit", type(e).__name__
        return False, "aucun refus"
    note("T19 rejeu dans la fenêtre du regard unique sans reçu : refusé", t19)
    nul = {}
    note("T20 période de 0 jour : pas de plantage, cases rapportées au temps vides, motif dit", lambda: (
        nul.update(M.mesurer_les_indicateurs(perte, "un_jeton", ("2024-01-11", "2024-01-11"), RACINE)) or
        nul["operations"] == 1 and all(nul[k] is None for k in (
            "operations_par_mois", "jours_entre_deux_gains", "gain_net_par_an_eur", "calmar",
            "creux_1_sur_20_sur_5_ans_eur", "serie_1_sur_20_sur_5_ans"))
        and "période de 0 jour" in nul["motif_periode"], nul["motif_periode"]))
    zero = [dict(perte[0], date_sortie="2024-01-1%d" % k, date_entree="2024-01-1%d" % k, net=x)
            for k, x in enumerate((1000.0, 0.0, -1000.0, 2000.0))]
    zi = {}
    note("T21 une opération à 0,00 € compte perdante : taux 50 %, perdante moyenne −500 €, série 2", lambda: (
        zi.update(M.mesurer_les_indicateurs(zero, "jetons_illimites", ("2024-01-01", "2024-03-01"), RACINE)) or
        proche(zi["taux_reussite_pct"], 50.0, 1e-9) and proche(zi["perdante_moyenne_eur"], -500.0)
        and zi["plus_longue_serie_de_pertes"] == 2,
        "%s %s %s" % (zi["taux_reussite_pct"], zi["perdante_moyenne_eur"], zi["plus_longue_serie_de_pertes"])))
    cent = list(range(1, 101))
    cent1 = list(range(1, 102))
    note("T22 rang partagé (MODULE_JUGEMENT.valeur_au_rang) : 1..100 → 96 et 6 ; 1..101 (rang 95,95 et 5,05 : la "
         "partie entière, ni l'arrondi ni le plafond) → 96 et 6", lambda: (
        b["MJ"].valeur_au_rang(cent, 0.95) == 96 and b["MJ"].valeur_au_rang(cent, 0.05) == 6
        and b["MJ"].valeur_au_rang(cent1, 0.95) == 96 and b["MJ"].valeur_au_rang(cent1, 0.05) == 6,
        "%s %s / %s %s" % (b["MJ"].valeur_au_rang(cent, 0.95), b["MJ"].valeur_au_rang(cent, 0.05),
                           b["MJ"].valeur_au_rang(cent1, 0.95), b["MJ"].valeur_au_rang(cent1, 0.05))))
    return R


def sabotages():
    """Rend la liste des sabotages : (nom, fonction qui casse le module, fonction qui restaure les briques).

    ① RÔLE — Casser un à un ce que chaque cas surveille.
    ② CONTEXTE D'APPEL — `main`, option `--saboter`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — Chaque sabotage remplace une fonction ou une constante du module éprouvé, ou d'une brique
      (alors restaurée après le tour), ou rend un module chargé depuis un texte modifié (`charger_mute`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 ; « une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration ».
    ⑨ CE QUI CLOCHE — Les sabotages sont écrits par l'auteur : un relecteur doit en ajouter d'autres.
    ⑩ EFFET — Modifie les modules en mémoire, jamais les fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    S = []

    def ajouter(nom, casser, restaurer=None):
        """Inscrit un sabotage.

        ① RÔLE — Inscrire.
        ② CONTEXTE D'APPEL — `sabotages`.
        ③ ENTRÉE — `nom` : le nom · `casser` : fonction(M) qui casse · `restaurer` : fonction(M) qui restaure.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — ajouter le triplet.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Ajoute à la liste.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        S.append((nom, casser, restaurer))

    def remplacer(M, nom, f):
        """Remplace une fonction du module éprouvé par `f(ancienne, *a, **k)`.

        ① RÔLE — Poser un sabotage autour d'une fonction existante.
        ② CONTEXTE D'APPEL — Les sabotages.
        ③ ENTRÉE — `M` : le module · `nom` : le nom de la fonction · `f` : la fonction de remplacement, qui reçoit
          l'ancienne en premier argument.
        ④ CONDITIONS D'ENTRÉE — La fonction existe.
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — fermer l'ancienne dans une enveloppe, l'écrire à sa place.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie le module en mémoire.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        ancienne = getattr(M, nom)
        setattr(M, nom, lambda *a, **k: f(ancienne, *a, **k))

    ajouter("S01 opérations par mois doublées", lambda M: remplacer(
        M, "operations_par_mois", lambda o, *a: None if o(*a) is None else 2 * o(*a)))
    ajouter("S02 fréquence comptée sur un gain de plus", lambda M: remplacer(
        M, "jours_entre_deux_gains", lambda o, g, p: o(g + 1, p) if g else o(g, p)))
    ajouter("S03 Wilson nourri du taux arrondi au dixième", lambda M: remplacer(
        M, "taux_et_wilson", lambda o, nets, r: (o(nets, r)[0], M.charger_les_briques(r)["MJ"].wilson_bas(
            len(nets), round(o(nets, r)[0], 1)))))
    ajouter("S04 perdante moyenne en valeur absolue", lambda M: remplacer(
        M, "moyennes_gagnante_perdante", lambda o, nets: (o(nets)[0], abs(o(nets)[1]) if o(nets)[1] else o(nets)[1])))
    ajouter("S05 creux rangé par date d'ENTRÉE (l'ordre du juge aujourd'hui)", lambda M: remplacer(
        M, "creux_du_compte", lambda o, ops, r: o([dict(x, date_sortie=x["date_entree"]) for x in ops], r)))
    ajouter("S06 « 1 fois sur 20 » pris au rang 50 %", lambda M: setattr(M, "UNE_FOIS_SUR_VINGT", 0.5))
    ajouter("S07 cinq ans comptés quatre", lambda M: setattr(M, "ANNEES_DU_SEUIL", 4))
    ajouter("S08 Kelly au quart", lambda M: remplacer(M, "kelly", lambda o, n, r: None if o(n, r) is None else round(o(n, r) / 4, 4)))
    ajouter("S09 Sortino divisé par les seules pertes", lambda M: remplacer(
        M, "sortino", lambda o, nets: None if o(nets) is None else o(nets) * math.sqrt(
            sum(1 for x in nets if x < 0) / len(nets))))
    ajouter("S10 Calmar sur le gain total", lambda M: remplacer(
        M, "calmar", lambda o, g, c: o(None if g is None else g * 2.519, c)))
    ajouter("S11 départage dans l'ordre de l'univers (celui du circuit)", lambda M: setattr(
        M, "ordre_de_departage", lambda s: list(s)))
    ajouter("S12 barème réel au lieu du forfait du golden", lambda M: remplacer(
        M, "rejouer_les_signaux", lambda o, r, c, s, g, bar, f, recu=None: o(r, c, s, g, "REEL", f, recu)))

    def casser_chevauchement(M):
        """Retire le contrôle des chevauchements en un jeton en déclarant tout en jetons illimités.

        ① RÔLE — Sabotage S13.
        ② CONTEXTE D'APPEL — `main`.
        ③ ENTRÉE — `M` : le module.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Rien.
          [rend: rien]
        ⑥ TRAITEMENT — envelopper `mesurer_les_indicateurs` : la comptabilité un jeton est mesurée comme jetons
          illimités, puis relabellisée.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — T17 doit rougir.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie le module en mémoire.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        remplacer(M, "mesurer_les_indicateurs", lambda o, ops, c, p, r, *a, **k: dict(
            o(ops, "jetons_illimites" if c == "un_jeton" else c, p, r, *a, **k), comptabilite=c))
    ajouter("S13 contrôle des chevauchements retiré", casser_chevauchement)

    def brique(sigle, nom, f):
        """Fabrique un sabotage d'une brique, et sa restauration.

        ① RÔLE — Casser une fonction d'une brique (module du dépôt) le temps d'un tour.
        ② CONTEXTE D'APPEL — `sabotages`.
        ③ ENTRÉE — `sigle` : la brique · `nom` : la fonction · `f` : le remplacement, qui reçoit l'ancienne.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : la fonction qui casse et celle qui restaure.
          [rend: 2]
        ⑥ TRAITEMENT — garder l'ancienne, poser l'enveloppe, la remettre ensuite.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Les briques sont gardées en mémoire entre les tours.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie la brique en mémoire.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        garde = {}

        def casser(M):
            """Pose le sabotage sur la brique.

            ① RÔLE — Casser.
            ② CONTEXTE D'APPEL — `main`.
            ③ ENTRÉE — `M` : le module éprouvé.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Rien.
              [rend: rien]
            ⑥ TRAITEMENT — remplacer.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — —
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Modifie la brique.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            B = M.charger_les_briques(RACINE)[sigle]
            garde["f"] = getattr(B, nom)
            setattr(B, nom, lambda *a, **k: f(garde["f"], *a, **k))

        def restaurer(M):
            """Remet la fonction de la brique.

            ① RÔLE — Restaurer.
            ② CONTEXTE D'APPEL — `main`.
            ③ ENTRÉE — `M` : le module éprouvé.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Rien.
              [rend: rien]
            ⑥ TRAITEMENT — remettre.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — —
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Modifie la brique.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            """
            setattr(M.charger_les_briques(RACINE)[sigle], nom, garde["f"])
        return casser, restaurer

    ajouter("S21 départage alphabétique (le CCI ignoré)", lambda M: setattr(
        M, "ordre_de_departage", lambda s: sorted(s, key=lambda x: x["valeur"])))
    ajouter("S22 comparaison opération par opération retirée du calibrage", lambda M: charger_mute(
        [("        ok = ok and k == 0\n", "        ok = ok\n")]))
    ajouter("S23 une opération à 0 € comptée gagnante dans le taux", lambda M: charger_mute(
        [("    taux = 100.0 * sum(1 for x in nets if x > 0) / len(nets)\n    return taux, MJ.wilson_bas",
          "    taux = 100.0 * sum(1 for x in nets if x >= 0) / len(nets)\n    return taux, MJ.wilson_bas")]))
    ajouter("S24 une opération à 0 € comptée gagnante dans les moyennes", lambda M: charger_mute(
        [("    g = [x for x in nets if x > 0]\n    p = [x for x in nets if x <= 0]",
          "    g = [x for x in nets if x >= 0]\n    p = [x for x in nets if x < 0]")]))
    ajouter("S25 un retour exact au sommet compté comme une sortie", lambda M: charger_mute(
        [("        if cumul > sommet:\n", "        if cumul >= sommet:\n")]))
    ajouter("S26 durée sous l'eau prise à l'ancien calcul (calculer_time_underwater)", lambda M: remplacer(
        M, "episodes_sous_l_eau", lambda o, ops, p: dict(o(ops, p), jours_plus_long_creux_rattrape=M.charger_les_briques(RACINE)["MS"]
            .calculer_time_underwater([{"date": x["date_sortie"], "gain": x["net"]} for x in ops])
            ["time_underwater_max_jours"])))
    ajouter("S32 creux en cours retiré des cases (un seul chiffre gardé)", lambda M: remplacer(
        M, "mesurer_les_indicateurs", lambda o, *a, **k: {x: y for x, y in o(*a, **k).items()
                                                           if x != "jours_du_creux_en_cours"}))
    ajouter("S33 creux rattrapé le plus long retiré des cases", lambda M: remplacer(
        M, "mesurer_les_indicateurs", lambda o, *a, **k: {x: y for x, y in o(*a, **k).items()
                                                           if x != "jours_plus_long_creux_rattrape"}))
    ajouter("S34 le plus long compte aussi le creux en cours (lecture écartée)", lambda M: charger_mute(
        [('    rattrapes = [e["jours"] for e in episodes if e["sorti"]]', '    rattrapes = [e["jours"] for e in episodes]')]))
    ajouter("S37 marges du tirage inversées", lambda M: charger_mute(
        [("            \"creux_marge_basse_eur\": tires[bas], \"creux_marge_haute_eur\": tires[haut],",
          "            \"creux_marge_basse_eur\": tires[haut], \"creux_marge_haute_eur\": tires[bas],")]))
    ajouter("S38 comparaison au producteur par ENSEMBLES (doublons perdus)", lambda M: charger_mute(
        [("        diff = sorted(((attendu - obtenu) + (obtenu - attendu)).elements())",
          "        diff = sorted(set(attendu) ^ set(obtenu))")]))
    ajouter("S39 date de sortie retirée de la comparaison au producteur", lambda M: charger_mute(
        [('                           d[t["valeur"]][t["i_out"]]["date"], round(t["pnl"], 2))',
          '                           round(t["pnl"], 2))'),
         ('        obtenu = Counter((JS.cle_valeur(o["valeur"]), o["date_entree"], o["date_sortie"], round(o["net"], 2))',
          '        obtenu = Counter((JS.cle_valeur(o["valeur"]), o["date_entree"], round(o["net"], 2))')]))
    ajouter("S40 cumul des épisodes en euros flottants (N1 défait)", lambda M: charger_mute(
        [('Fraction(repr(float(o["net"])))', 'float(o["net"])'),
         ('Fraction(0), Fraction(0), d0, None, []', '0.0, 0.0, d0, None, []')]))
    ajouter("S41 gains arrondis au centime avant le cumul (C1 défait)", lambda M: charger_mute(
        [('Fraction(repr(float(o["net"])))', 'Fraction(int(round(o["net"] * 100)), 100)')]))
    ajouter("S42 gains tronqués au centime avant le cumul", lambda M: charger_mute(
        [('Fraction(repr(float(o["net"])))', 'Fraction(int(o["net"] * 100), 100)')]))
    ajouter("S43 comparaison par ENSEMBLES en jetons illimités seulement (Cowork, X2)", lambda M: charger_mute(
        [("        diff = sorted(((attendu - obtenu) + (obtenu - attendu)).elements())",
          "        diff = (sorted(((attendu - obtenu) + (obtenu - attendu)).elements()) if compta == \"un_jeton\"\n"
          "                else sorted(set(attendu) ^ set(obtenu)))")]))
    ajouter("S44 valeur BINAIRE du flottant (Fraction(net), sans repr ; Cowork, X5)", lambda M: charger_mute(
        [('Fraction(repr(float(o["net"])))', 'Fraction(float(o["net"]))')]))
    ajouter("S45 gains arrondis au millième d'euro (Cowork, X3)", lambda M: charger_mute(
        [('Fraction(repr(float(o["net"])))', 'Fraction(repr(round(float(o["net"]), 3)))')]))
    ajouter("S46 gains arrondis au dix-millième d'euro (Cowork, X4)", lambda M: charger_mute(
        [('Fraction(repr(float(o["net"])))', 'Fraction(repr(round(float(o["net"]), 4)))')]))
    ajouter("S27 épisode ouvert à la fin compté « sorti »", lambda M: charger_mute(
        [("        ouvert.update(sortie=None, jours=jours(ouvert[\"date_sommet\"], d1), sorti=False)",
          "        ouvert.update(sortie=None, jours=jours(ouvert[\"date_sommet\"], d1), sorti=True)")]))
    ajouter("S28 période de 0 jour refusée comme avant", lambda M: charger_mute(
        [("    if d1 < d0:\n        raise ValueError(\"période %r à l'envers\" % (periode,))\n    return (d1 - d0)",
          "    if d1 <= d0:\n        raise ValueError(\"période %r à l'envers\" % (periode,))\n    return (d1 - d0)")]))
    ajouter("S29 série exacte calculée avec la part des GAINS", lambda M: charger_mute(
        [("loi_de_la_plus_longue_serie(sum(1 for x in nets if x <= 0) / len(nets)",
          "loi_de_la_plus_longue_serie(sum(1 for x in nets if x > 0) / len(nets)")]))
    ajouter("S30 creux exact : seuil de probabilité à 90 %", lambda M: charger_mute(
        [("        if p_sous(candidats[milieu]) >= UNE_FOIS_SUR_VINGT:",
          "        if p_sous(candidats[milieu]) >= 0.90:")]))
    ajouter("S31 marge du tirage réduite au seul rang central", lambda M: charger_mute(
        [("            \"creux_marge_basse_eur\": tires[bas], \"creux_marge_haute_eur\": tires[haut],",
          "            \"creux_marge_basse_eur\": 21600.0, \"creux_marge_haute_eur\": 21600.0,")]))
    ajouter("S19 année comptée 365 jours", lambda M: setattr(M, "JOURS_PAR_AN", 365.0))
    ajouter("S20 départage par le CCI le plus HAUT", lambda M: setattr(
        M, "ordre_de_departage", lambda s: sorted(s, key=lambda x: (-float(x["cci"]), x["valeur"]))))
    c, r = brique("MJ", "borne_basse_gain", lambda o, ops, **k: dict(o(ops, **k), borne_basse_5pct=o(ops, **k).get("gain_moyen")))
    ajouter("S14 borne basse du gain = gain moyen", c, r)
    c, r = brique("MJ", "plus_longue_serie_de_pertes", lambda o, ops: max(0, o(ops) - 1))
    ajouter("S15 plus longue série amputée d'une perte", c, r)
    c, r = brique("JS", "_garde_du_regard_unique", lambda o, *a, **k: None)
    ajouter("S16 garde du regard unique retirée", c, r)
    c, r = brique("MJ", "valeur_au_rang", lambda o, t, part: t[min(len(t) - 1, int(part * len(t)) + 1)])
    ajouter("S17 rang partagé décalé d'un cran", c, r)
    c, r = brique("MJ", "valeur_au_rang", lambda o, t, part: t[min(len(t) - 1, math.ceil(part * len(t)))])
    ajouter("S35 rang partagé au plafond (ceil)", c, r)
    c, r = brique("MJ", "valeur_au_rang", lambda o, t, part: t[min(len(t) - 1, round(part * len(t)))])
    ajouter("S36 rang partagé à l'arrondi (round)", c, r)
    c, r = brique("MES", "pire_chute", lambda o, p, *a: (o(p, *a)[0], o(p, *a)[1] - 100.0))
    ajouter("S18 creux de la mesure du soir décalé de 100 €", c, r)
    return S


def comparer():
    """Mesure, sans verdict, les trois calculs du creux et les deux chiffres de la durée sous l'eau, sur le golden.

    ① RÔLE — Montrer en quoi les trois creux existants diffèrent sur de vraies données (consigne du Chat).
    ② CONTEXTE D'APPEL — `main`, option `--comparer`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Celles de `calibrer_sur_le_golden`.
    ⑤ SORTIE — Rien : affiche.
      [rend: rien]
    ⑥ TRAITEMENT — ① une fois : le rejeu un jeton avec les signaux dans l'ordre où le circuit du soir les passe
      (l'ordre de l'univers) · pour chaque comptabilité : ② `pire_chute` (mesure du soir) dans l'ordre des sorties ·
      ③ `pire_chute` dans l'ordre des ENTRÉES (l'ordre du juge), avec DEUX clés de tri explicites pour les entrées
      d'un même jour, (entrée, valeur) et (entrée, valeur à l'envers), d'où une fourchette · ④
      `calculer_time_underwater` nourri des dates d'entrée (ce que fait le juge) et des dates de sortie · ⑤ le calcul
      du radar (`_series_du_journal`, recopié en trois lignes) dans l'ordre des sorties · ⑥ les deux chiffres de la
      durée (A-798) par `episodes_sous_l_eau`.
    ⑦ UNITÉ — Euros ; jours calendaires.
    ⑧ POURQUOI — Choisir une définition en montrant ce que les autres donnent. Le superviseur R-759 (D8) : un
      chiffre qui dépend de l'ordre de deux opérations du même jour se rend en fourchette, avec ses clés nommées.
    ⑨ CE QUI CLOCHE — La recopie du radar est un instrument de mesure, pas un indicateur : sa fonction est imbriquée
      dans le corps du radar et ne s'importe pas sans lancer tout l'audit.
    ⑩ EFFET — AFFICHE.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    M = charger()
    ok, _l, rendu = M.calibrer_sur_le_golden(RACINE)
    b = M.charger_les_briques(RACINE)
    for compta in ("un_jeton", "jetons_illimites"):
        if compta == "un_jeton":
            M2 = charger()
            M2.ordre_de_departage = lambda sj: list(sj)
            _ok2, l2, _r2 = M2.calibrer_sur_le_golden(RACINE)
            print("COMPARER départage dans l'ordre de l'univers (le circuit du soir) : "
                  + next(l for l in l2 if " un_jeton : " in l and "opérations ." in l))
        ops = rendu[compta]
        par_sortie = sorted(ops, key=lambda o: (o["date_sortie"], o["date_entree"], o["valeur"]))
        par_entree = sorted(ops, key=lambda o: (o["date_entree"], o["valeur"]))
        par_entree_inv = sorted(ops, key=lambda o: (o["date_entree"], [-ord(c) for c in o["valeur"]]))
        mes = -b["MES"].pire_chute([o["net"] for o in par_sortie])[1]
        f1 = -b["MES"].pire_chute([o["net"] for o in par_entree])[1]
        f2 = -b["MES"].pire_chute([o["net"] for o in par_entree_inv])[1]
        ms_ent = b["MS"].calculer_time_underwater([{"date": o["date_entree"], "gain": o["net"]} for o in par_entree])
        ms_sor = b["MS"].calculer_time_underwater([{"date": o["date_sortie"], "gain": o["net"]} for o in par_sortie])
        eq = pic = creux = 0.0
        for o in par_sortie:
            eq += o["net"]; pic = max(pic, eq); creux = max(creux, pic - eq)
        eau = M.episodes_sous_l_eau(ops, rendu["periode"])
        print("COMPARER %s : pire_chute (sorties) %.2f EUR · pire_chute (entrées, fourchette selon l'ordre des entrées "
              "d'un même jour, clés (entrée, valeur) et (entrée, valeur à l'envers)) %.2f à %.2f EUR · "
              "time_underwater (entrées) %s EUR %s j · time_underwater (sorties) %s EUR %s j · radar (sorties) %.2f EUR · "
              "creux rattrapé le plus long %s j · creux en cours %s j (sorti=%s)"
              % (compta, mes, min(f1, f2), max(f1, f2), ms_ent["dd_max_eur"], ms_ent["time_underwater_max_jours"],
                 ms_sor["dd_max_eur"], ms_sor["time_underwater_max_jours"], creux,
                 eau["jours_plus_long_creux_rattrape"], eau["jours_du_creux_en_cours"], eau["creux_en_cours_sorti"]))


def mesurer_l_arrondi():
    """Mesure, sans verdict, l'effet de l'arrondi au centime de `creux_exact_1_sur_20` sur de vraies opérations.

    ① RÔLE — La mesure demandée par Cowork (relecture du 15-11-2026, « mesure demandée ») et par le Chat.
    ② CONTEXTE D'APPEL — `main`, option `--mesurer-l-arrondi`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Celles de `calibrer_sur_le_golden` ; les fichiers d'étude `etudes/A521_CHECK_NEWSLETTER_*`.
    ⑤ SORTIE — Rien : affiche.
      [rend: rien]
    ⑥ TRAITEMENT — ① golden, deux comptabilités : nombre de gains qui ne tombent pas au centime ; en un jeton, le seuil
      exact au centime (le calcul livré) et au cent-millième (le même calcul, texte modifié par `charger_mute`) ·
      ② gains réels à fractions de centime des études A521 (colonne `gain_net_eur`, au plus 20 montants distincts),
      n = 5 : les deux seuils et leur écart, quand les deux sont faisables.
    ⑦ UNITÉ — Euros.
    ⑧ POURQUOI — Le ⑨ de `creux_exact_1_sur_20` affirme « quelques centimes » : cela se mesure.
    ⑨ CE QUI CLOCHE — Le calcul fin est le calcul livré dont le texte est modifié : il partage donc tout le reste.
    ⑩ EFFET — AFFICHE ; lit des fichiers d'étude.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import glob
    M = charger()
    fin = charger_mute([("        c = int(round(x * 100))", "        c = int(round(x * 100000))"),
                        ("    return candidats[bas] / 100.0", "    return candidats[bas] / 100000.0")])
    ok, _l, rendu = M.calibrer_sur_le_golden(RACINE)
    for compta in ("un_jeton", "jetons_illimites"):
        nets = [o["net"] for o in rendu[compta]]
        print("ARRONDI golden %s : %d gains, %d hors du centime" % (
            compta, len(nets), sum(1 for x in nets if abs(x * 100 - round(x * 100)) > 1e-6)))
    nets = [o["net"] for o in rendu["un_jeton"]]
    print("ARRONDI golden un_jeton, N = 87 : centime %s · cent-millième %s" % (
        M.creux_exact_1_sur_20(nets, 87), fin.creux_exact_1_sur_20(nets, 87, etats_max=200000)))
    for f in sorted(glob.glob(os.path.join(RACINE, "etudes", "A521_CHECK_NEWSLETTER_*", "**", "trades_*.csv"),
                              recursive=True)):
        try:
            nets = [float(r["gain_net_eur"]) for r in csv.DictReader(open(f, encoding="utf-8"))
                    if (r.get("gain_net_eur") or "").strip()]
        except (KeyError, ValueError):
            continue
        if not nets or len(set(nets)) > 20 or all(abs(x * 100 - round(x * 100)) < 1e-6 for x in nets):
            continue
        a, z = M.creux_exact_1_sur_20(nets, 5), fin.creux_exact_1_sur_20(nets, 5, etats_max=200000)
        if a is None or z is None:
            continue
        print("ARRONDI %s n=5 : centime %.2f · cent-millième %.5f · écart %+.5f EUR" % (
            os.path.relpath(f, RACINE), a, z, a - z))


def main():
    """Joue les cas, puis les sabotages si demandé ; rend le code de sortie.

    ① RÔLE — Le lancement.
    ② CONTEXTE D'APPEL — Le bas du fichier.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir le ⑤ du fichier).
      [rend: 1]
    ⑥ TRAITEMENT — ① `--comparer` : mesurer et rendre 0 · ② jouer les cas, afficher · ③ `--saboter` : pour chaque
      sabotage, module neuf, casser, jouer, restaurer ; exiger au moins un cas tombé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul (2).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — AFFICHE.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        if "--comparer" in sys.argv:
            comparer()
            return 0
        if "--mesurer-l-arrondi" in sys.argv:
            mesurer_l_arrondi()
            return 0
        M = charger()
        R = cas(M)
    except Exception as e:
        print("CONTRÔLE IMPOSSIBLE : %s: %s" % (type(e).__name__, e))
        return 2
    for nom, ok, det in R:
        print("  %s %s — %s" % ("OK   " if ok else "ÉCHEC", nom, det))
    tenus = sum(1 for _n, ok, _d in R if ok)
    print("CAS : %d / %d tenus" % (tenus, len(R)))
    code = 0 if tenus == len(R) else 1
    if "--saboter" in sys.argv:
        for nom, casser, restaurer in sabotages():
            M = charger()
            try:
                M = casser(M) or M
            except Exception as e:
                print("== %s : SABOTAGE NON POSÉ (%s: %s)" % (nom, type(e).__name__, e))
                code = 1
                continue
            try:
                Rs = cas(M)
            except Exception as e:
                Rs = [("lève", False, str(e))]
            finally:
                if restaurer:
                    restaurer(M)
            tombes = [n.split(" ")[0] for n, ok, _d in Rs if not ok]
            print("== %s : %s" % (nom, ("MORD (" + ", ".join(tombes) + ")") if tombes else "NE MORD PAS"))
            if not tombes:
                code = 1
    print("CODE %d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())
