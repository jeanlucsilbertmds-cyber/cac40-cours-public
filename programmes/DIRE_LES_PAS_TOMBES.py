#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dit, à la fin du circuit du soir, quels pas sont tombés sans bloquer.

① RÔLE — En fin de passage : ① dire si le rapport du radar et le PILOTE portent
  bien la date du jour ; ② compter les pas du circuit par issue (réussi, tombé,
  jamais lancé, annulé) et annoncer en rouge ceux qui n'ont rien produit.
② CONTEXTE D'APPEL — Le dernier pas du circuit du soir, « Dire quels pas non
  bloquants sont tombes », lancé même si un pas précédent a échoué.
③ ENTRÉE — La ligne de commande : la racine du dépôt, ou `GITHUB_WORKSPACE`, ou
  le dossier courant. L'environnement : `PAS`, la table des pas que GitHub
  fournit (texte JSON) ; `GITHUB_STEP_SUMMARY`, le fichier du résumé du passage,
  facultatif.
④ CONDITIONS D'ENTRÉE — `PAS` est posé : sinon le programme s'arrête sur une
  erreur, code non nul. La première partie (les dates) ne bloque jamais : une
  erreur y est affichée et le programme continue.
⑤ SORTIE — UNE valeur : le code de sortie, 0 quand le compte a pu être fait
  (même si des pas sont tombés : ce pas annonce, il ne juge pas) ; non nul si
  `PAS` manque ou est illisible. [rend: 1]
⑥ TRAITEMENT — ① charger les contrats et appeler `fabrique_du_jour` sur
  `rapports/audit_du_jour.md` et `gouvernance/PILOTE.md` · ② lire `PAS`, ranger
  les pas par issue · ③ annoncer : aucun pas suivi, tous réussis, ou les pas
  tombés, jamais lancés, annulés · ④ écrire les mêmes annonces au résumé.
⑦ UNITÉ — Des nombres de pas.
⑧ POURQUOI — Ces lignes vivaient écrites dans le fichier du circuit, en deux
  blocs. Ce fichier devient public (A-543, décision de Jean-Luc du 08-10-2026 :
  « aucun code dans le fichier du circuit, le code vivant dans les programmes
  publiés »). Le texte est repris tel quel ; le premier bloc était suivi de
  « || true » : il ne bloquait jamais, et c'est gardé.
⑨ CE QUI CLOCHE — —
⑩ EFFET — ÉCRIT au résumé du passage quand `GITHUB_STEP_SUMMARY` est posé.
⑪ TERMINAISON — Rend la main. [sort: oui]
⑫ DÉFINITIONS
  un pas : une étape du circuit du soir, avec son identifiant.
  le PILOTE : `gouvernance/PILOTE.md`, le tableau de bord fabriqué chaque soir.
"""
import importlib.util
import json
import os
import sys


def dates_du_jour(base):
    """Annonce un rapport du radar ou un PILOTE qui ne porte pas la date du jour.

    ① RÔLE — Premier bloc de l'ancien pas : vérifier deux dates.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `base` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Aucune : toute erreur est rattrapée et affichée.
    ⑤ SORTIE — Ne rend rien ; affiche. [rend: 0]
      [rend: rien]
    ⑥ TRAITEMENT — Charger les contrats, appeler `fabrique_du_jour` sur les deux
      fichiers, afficher en rouge chaque date manquante.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'ancien bloc finissait par « || true » : il ne bloquait jamais.
    ⑨ CE QUI CLOCHE — Une erreur ici n'est qu'affichée, comme avant.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
      [sort: non]
    """
    try:
        _sp = importlib.util.spec_from_file_location("c", os.path.join(base, "programmes", "CONTRATS_DES_FICHIERS.py"))
        _m = importlib.util.module_from_spec(_sp)
        _sp.loader.exec_module(_m)
        for _ch, _mo, _q in (
                ("rapports/audit_du_jour.md", r"CAC 40 . \w+ (\d{2}-\d{2}-\d{4})", "ecrit"),
                ("gouvernance/PILOTE.md", r"Fabriqué le \w+ (\d{2}-\d{2}-\d{4})", "fabrique")):
            _d = _m.fabrique_du_jour(base, _ch, _mo, _q)
            if _d:
                print(f"::error::{_d}")
    except Exception as e:  # l'ancien bloc était suivi de « || true »
        print(f"dates du jour non vérifiées : {type(e).__name__}: {e}")


def compter_les_pas(pas):
    """Range les pas par issue et annonce ceux qui n'ont rien produit.

    ① RÔLE — Second bloc de l'ancien pas.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `pas` : la table des pas, dictionnaire lu dans `PAS`.
    ④ CONDITIONS D'ENTRÉE — Un dictionnaire.
    ⑤ SORTIE — Ne rend rien ; affiche et écrit au résumé. [rend: 0]
      [rend: rien]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥ ② à ④.
    ⑦ UNITÉ — Des nombres de pas.
    ⑧ POURQUOI — Un pas tombé sans bloquer ne doit jamais passer en silence.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — ÉCRIT au résumé du passage.
    ⑪ TERMINAISON — Rend la main. [sort: non]
      [sort: non]
    """
    issues = {}
    for n, v in pas.items():
        if isinstance(v, dict) and v.get("outcome"):
            issues.setdefault(v["outcome"], []).append(n)
    for k in issues:
        issues[k].sort()
    total = sum(len(v) for v in issues.values())
    reussis = issues.pop("success", [])
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if total == 0:
        print("::error::AUCUN PAS SUIVI — la table des pas est vide. "
              "Soit aucun pas ne porte d identifiant, soit le passage n a "
              "rien execute. Dans les deux cas, RIEN n est prouve.")
        if s:
            open(s, "a", encoding="utf-8").write(
                "## ⚠️ AUCUN PAS SUIVI — rien n est prouve\n")
    elif not issues:
        print(f"les {len(reussis)} pas suivis ont tous abouti")
    else:
        if "skipped" in issues and "failure" not in issues:
            normaux = issues.pop("skipped")
            print(f"  {len(normaux)} pas non applique(s) ce soir "
                  f"(condition non remplie, aucun echec) : {' '.join(normaux)}")
        for issue, noms in sorted(issues.items()):
            quoi = {"failure": "TOMBES SANS BLOQUER",
                    "skipped": "JAMAIS LANCES",
                    "cancelled": "ANNULES"}.get(issue, issue.upper())
            print(f"::error::{len(noms)} PAS {quoi} : {' '.join(noms)} — "
                  f"ces pas n ont RIEN PRODUIT")
            if s:
                open(s, "a", encoding="utf-8").write(
                    f"## ⚠️ {len(noms)} pas {quoi} : {' '.join(noms)}\n")
        print(f"  ({len(reussis)} pas abouti(s) sur {total} suivis)")


def main():
    """Les deux blocs, dans l'ordre de l'ancien pas.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv[1]`, facultatif : la racine ; `PAS`.
    ④ CONDITIONS D'ENTRÉE — `PAS` posé.
    ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — `dates_du_jour`, puis `compter_les_pas`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Rend la main. [sort: oui]
      [sort: non]
    """
    base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_WORKSPACE", ".")
    dates_du_jour(base)
    compter_les_pas(json.loads(os.environ["PAS"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
