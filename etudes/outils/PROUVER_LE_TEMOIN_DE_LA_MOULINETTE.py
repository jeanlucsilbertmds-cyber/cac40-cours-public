"""PROUVER_LE_TEMOIN_DE_LA_MOULINETTE.py — Mar 27-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit.

① RÔLE — Prouver, version par version, d'où vient chaque écart entre le témoin de la moulinette
  (`donnees/combinatoires/TEMOIN_RESULTATS_C5E10-OBS-V1_E01.csv`) et les résultats du juge depuis qu'il lit les cours
  par le lecteur unique (A-577, étape 1) ; et écrire le témoin candidat.
② CONTEXTE D'APPEL — À la main : python3 -I -B etudes/outils/PROUVER_LE_TEMOIN_DE_LA_MOULINETTE.py <racine>
  <témoin candidat à écrire> [<témoin de référence>]. Le témoin de référence est, par défaut, celui du dépôt.
  Lancé le 27-10-2026, avant le remplacement du témoin décidé par Jean-Luc le même jour (« 1 · Oui, remplace »).
③ ENTRÉE — La racine du dépôt ; le chemin du témoin candidat, hors du dépôt ; le témoin de référence, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : le juge, `programmes/JOUER_LES_VERSIONS.py`, la combinatoire
  `donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv`, la fiche C5E10-OBS-V1 au registre des stratégies.
⑤ SORTIE — AUCUNE valeur rendue. Affiche quatre comptes ; écrit le témoin candidat. Code de sortie 0 si l'ancienne
  lecture retrouve le témoin de référence pour TOUTES les versions, si toute opération retirée a son achat hors du
  CAC 40, et si aucune n'est ajoutée ; 1 sinon (le témoin candidat n'est alors pas écrit).
⑥ TRAITEMENT — Pour chaque version : ① la fusionner à la fiche comme la moulinette (`fusionner` de
  JOUER_LES_VERSIONS) · ② la jouer sans lecture (l'ancienne façon) et comparer son résumé au témoin, au centime : c'est
  le CALIBRAGE · ③ la jouer avec la lecture du lecteur unique · ④ relever les opérations retirées et ajoutées, et pour
  chaque retirée si sa date d'achat est hors de l'indice · ⑤ écrire la ligne du témoin candidat.
⑦ UNITÉ — Des versions, des opérations, des euros.
⑧ POURQUOI — Un témoin ne se remplace pas sans preuve que chaque écart a la cause annoncée. Reproduire d'abord le
  témoin connu avec l'ancienne lecture prouve que l'instrument est calibré.
⑨ CE QUI CLOCHE — Ne vaut que pour la combinatoire E01 de C5E10-OBS-V1 : le nom est écrit ici. Sur le maître, aucune
  série n'a de trou : seule la composition est éprouvée.
⑩ EFFET — Écrit le témoin candidat. N'écrit rien sous la racine si le chemin donné est ailleurs.
⑪ TERMINAISON — 2 695 versions jouées deux fois, chacune finie ; sort par sys.exit.
  [sort: oui]
"""
import csv, os, sys

base, sortie = os.path.abspath(sys.argv[1]), sys.argv[2]
f_tem = sys.argv[3] if len(sys.argv) > 3 else os.path.join(base, "donnees/combinatoires/TEMOIN_RESULTATS_C5E10-OBS-V1_E01.csv")
sys.path.insert(0, os.path.join(base, "programmes"))
sys.dont_write_bytecode = True
import JUGE_DES_STRATEGIES as J, JOUER_LES_VERSIONS as V

comb = os.path.join(base, "donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv")
tem = {r["id_version"]: r for r in csv.DictReader(open(f_tem, encoding="utf-8-sig"))}
versions = list(csv.DictReader(open(comb, encoding="utf-8-sig")))
mnemo = J.table_mnemoniques(J.trouver(base, "REFERENTIEL_VALEURS"))
f_m = J.fichiers_de_cours(base)[0]
vieux = J.charger_cours(f_m)
neuf, lec = J.lire_par_le_lecteur(base, os.path.relpath(f_m, base), mnemo)
sig = J.charger_module(J.trouver(base, "MODULE_C5_ETENDU_10"), "sig")
pos = J.charger_module(J.trouver(base, "MODULE_POSITIONS.py"), "pos")
fiche = [f for f in csv.DictReader(open(J.trouver(base, "cac40_strategies.csv"), encoding="utf-8-sig"))
         if f["id"] == "C5E10-OBS-V1"][0]


def ligne(r):
    """Écrit un résumé du juge comme la moulinette l'écrit (trois champs).

    ① RÔLE — Comparer au témoin dans son propre format. ② CONTEXTE D'APPEL — la boucle des versions. ③ ENTRÉE — un
    résumé rendu par `resumer`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : (opérations, réussite à six
    décimales ou vide, gain net à deux décimales). [rend: 1] ⑥ TRAITEMENT — Les formats de `main` de
    JOUER_LES_VERSIONS. ⑦ UNITÉ — opérations, pourcents, euros. ⑧ POURQUOI — Le témoin est du texte. ⑨ CE QUI
    CLOCHE — Le format est recopié de JOUER_LES_VERSIONS (R-708) : s'il change là-bas, le calibrage échoue et le dit.
    ⑩ EFFET — —. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return (str(r["n"]), "%.6f" % r["wr_exact"] if r["n"] else "", "%.2f" % r["net"] if r["n"] else "0.00")


cle = lambda x: (x["valeur"], x["date_signal"])
calibrees = changees = retirees = hors = ajoutees = 0
lignes = []
for v in versions:
    f = V.fusionner(fiche, v)
    f.setdefault("_fonction_signal", "signaux_c5etendu10")
    _, _, b = J.porte_0(f)
    o1, _ = J.jouer(f, vieux, mnemo, sig, pos, periode=b)
    o2, _ = J.jouer(f, neuf, mnemo, sig, pos, periode=b, lecture=lec)
    t = tem[v["id_version"]]
    connu = (t["operations"], t["reussite_pourcents_exacte"], t["gain_net_euros"])
    calibrees += ligne(J.resumer(o1)) == connu
    gardees = {cle(y) for y in o2}
    r_ = [x for x in o1 if cle(x) not in gardees]
    ajoutees += sum(1 for y in o2 if cle(y) not in {cle(x) for x in o1})
    retirees += len(r_)
    for x in r_:
        s = neuf[x["valeur"]]
        achat = s[[q["date"] for q in s].index(x["date_signal"]) + 1]["date"]
        hors += not J.dans_l_indice(lec["passages"][x["valeur"]], achat)
    n2 = ligne(J.resumer(o2))
    changees += n2 != connu
    lignes.append(dict(t, operations=n2[0], reussite_pourcents_exacte=n2[1], gain_net_euros=n2[2]))
print("versions : %d · ancienne lecture = témoin au centime : %d · changées par le lecteur : %d"
      % (len(versions), calibrees, changees))
print("opérations retirées : %d, dont achat hors de l'indice : %d · ajoutées : %d" % (retirees, hors, ajoutees))
ok = calibrees == len(versions) and hors == retirees and ajoutees == 0
if ok:
    w = csv.DictWriter(open(sortie, "w", encoding="utf-8", newline=""), fieldnames=list(lignes[0].keys()))
    w.writeheader()
    w.writerows(lignes)
    print("témoin candidat écrit : %s" % sortie)
print("VERDICT : " + ("chaque écart a sa cause" if ok else "NON PROUVÉ — rien n'est écrit"))
sys.exit(0 if ok else 1)
