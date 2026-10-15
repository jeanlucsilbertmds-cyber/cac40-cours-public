#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPLIQUER_UNE_SEANCE.py — Sam 10-10-2026 (Paris) — OUTIL D'ÉTUDE, non validé. Simulation uniquement.

① RÔLE — Mettre côte à côte, pour UNE valeur et UNE séance de l'historique long, ce que disent toutes les sources du
  dépôt : le pas du fichier réparé, les clôtures brutes de Paris (bnains) et de Francfort, l'indice CAC 40, l'écart
  à l'indice, et le pas brut de chaque valeur ce jour-là, rangées — pour dire si un écart à l'indice vient du
  fichier ou du marché.
② CONTEXTE D'APPEL — À la main, depuis la racine du dépôt :
  python3 etudes/outils/EXPLIQUER_UNE_SEANCE.py <racine> "<VALEUR>" <AAAA-MM-JJ>. Aucune tâche ne l'appelle.
③ ENTRÉE — La racine du dépôt, le nom de la valeur (tel que dans les fichiers), la date de la séance.
④ CONDITIONS D'ENTRÉE — donnees/sources_yahoo/historique_long_repare.csv, donnees/sources_bnains/bnains_cac40.csv,
  donnees/sources_francfort/COURS_DE_FRANCFORT.csv et donnees/sources_indice/INDICE_CAC40.csv existent ; la séance
  et celle qui la précède sont dans le fichier réparé.
⑤ SORTIE — UNE valeur : le code de sortie, 0 quand le compte rendu est affiché, 2 quand la séance ou une source
  manque (R-734).
⑥ TRAITEMENT — ① la séance précédente de la valeur dans le fichier réparé, et son pas · ② les clôtures brutes de
  bnains et de Francfort, la veille et le jour · ③ le pas de l'indice (colonne bnains, à défaut yahoo) et l'écart
  du pas réparé à l'indice · ④ le pas brut de bnains de chaque valeur ce jour-là, du plus bas au plus haut.
⑦ UNITÉ — Des euros (clôtures) ; des pour cent (pas) ; des points de pour cent (écart).
⑧ POURQUOI — Décision de Jean-Luc du 10-10-2026, réponse à la question posée après 15h29 (« Oui, les deux » : chercher l'écart de Société Générale du
  21-02-2008 à l'indice, −3,24 points mesurés par Cowork dans sa relecture 22cc10b). La mesure a d'abord été faite
  par un programme hors dépôt ; ce qu'un programme peut faire, un programme le fait, et se rejoue (R-754).
⑨ CE QUI CLOCHE — L'écart ne tient pas compte du poids de la valeur dans l'indice ni de sa sensibilité au marché :
  c'est l'écart brut. · Le pas brut de bnains, un jour d'opération, porte l'opération (Société Générale le
  21-02-2008 : −8,53 %, droit compris). · Francfort clôt plus tard que Paris : sa clôture peut différer d'un pour
  cent un jour agité.
⑩ EFFET — Lit quatre fichiers. N'écrit rien. Affiche.
⑪ TERMINAISON — Rend la main : un passage sur chaque fichier.
"""
import csv, os, sys

RANG = 5   # valeurs affichées en tête et en queue du classement du jour


def lire(racine, chemin):
    """Lit un CSV du dépôt en liste de dictionnaires.

    ① RÔLE — Une lecture, une seule fois écrite.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : la racine du dépôt · `chemin` : le chemin relatif du fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe, en UTF-8.
    ⑤ SORTIE — UNE valeur : la liste des lignes.
      [rend: 1]
    ⑥ TRAITEMENT — `csv.DictReader`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Quatre fichiers à lire de la même façon.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(os.path.join(racine, chemin), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv):
    """Affiche le compte rendu de la séance demandée.

    ① RÔLE — Voir l'en-tête du module.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la racine, la valeur, la date.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie (0 ou 2).
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(argv) != 3:
        print("usage : EXPLIQUER_UNE_SEANCE.py <racine> <VALEUR> <AAAA-MM-JJ>")
        return 2
    racine, valeur, jour = argv
    try:
        repare = [r for r in lire(racine, "donnees/sources_yahoo/historique_long_repare.csv") if r["valeur"] == valeur]
        jours = sorted(r["date"] for r in repare)
        veille = jours[jours.index(jour) - 1]
        c = {r["date"]: float(r["close"]) for r in repare}
        bn = {(r["valeur"], r["date"]): float(r["close"]) for r in lire(racine, "donnees/sources_bnains/bnains_cac40.csv")
              if r["date"] in (veille, jour)}
        fr = {r["date"]: float(r["close"]) for r in lire(racine, "donnees/sources_francfort/COURS_DE_FRANCFORT.csv")
              if r["valeur"] == valeur and r["date"] in (veille, jour)}
        ix = {r["date"]: float(r["bnains"] or r["yahoo"]) for r in lire(racine, "donnees/sources_indice/INDICE_CAC40.csv")
              if r["date"] in (veille, jour)}
        pas = c[jour] / c[veille] - 1
        pas_indice = ix[jour] / ix[veille] - 1
    except (OSError, KeyError, ValueError, IndexError) as e:
        print(f"SÉANCE OU SOURCE MANQUANTE : {type(e).__name__} : {e}")
        return 2
    print(f"{valeur}, {veille} → {jour}")
    print(f"  fichier réparé : {c[veille]:.4f} → {c[jour]:.4f} = {pas * 100:+.2f} %")
    for nom, s in (("bnains (Paris, brut)", {d: bn.get((valeur, d)) for d in (veille, jour)}), ("Francfort (brut)", fr)):
        a, b = s.get(veille), s.get(jour)
        print(f"  {nom} : " + (f"{a:.2f} → {b:.2f} = {(b / a - 1) * 100:+.2f} %" if a and b else "absent"))
    print(f"  indice CAC 40 : {ix[veille]:.2f} → {ix[jour]:.2f} = {pas_indice * 100:+.2f} %")
    print(f"  écart du fichier réparé à l'indice : {(pas - pas_indice) * 100:+.2f} points")
    rangs = sorted(((bn[(v, jour)] / bn[(v, veille)] - 1) * 100, v) for (v, d) in bn
                   if d == jour and (v, veille) in bn)
    print(f"  pas brut de chaque valeur ce jour-là (bnains), {len(rangs)} valeurs :")
    for x, v in rangs[:RANG] + rangs[-RANG:]:
        print(f"    {v:28} {x:+.2f} %")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
