#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confronte chaque fichier partagé à son contrat, pour le circuit du soir.

① RÔLE — Dire si un fichier lu par deux programmes ne porte plus les champs que
  son contrat déclare, et rendre un code de sortie non nul si c'est le cas.
② CONTEXTE D'APPEL — Le pas « Confronter les fichiers a leurs contrats » du
  circuit du soir, sur le dépôt privé comme sur le dépôt public.
③ ENTRÉE — La ligne de commande : la racine du dépôt (dossier), ou
  `GITHUB_WORKSPACE`, ou le dossier courant à défaut.
④ CONDITIONS D'ENTRÉE — `programmes/CONTRATS_DES_FICHIERS.py` existe sous la
  racine : sinon le programme s'arrête sur une erreur, code non nul.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si tous les fichiers portent leurs
  champs, 1 sinon ; à l'écran, une ligne « !! » par écart. [rend: 1]
⑥ TRAITEMENT — ① charger le module des contrats depuis la racine · ② appeler
  `confronter_tous(racine)` · ③ afficher chaque écart · ④ rendre 1 s'il y en a.
⑦ UNITÉ — —
⑧ POURQUOI — Ces lignes vivaient écrites dans le fichier du circuit. Ce
  fichier devient public (A-543, décision de Jean-Luc du 08-10-2026 : « aucun
  code dans le fichier du circuit, le code vivant dans les programmes
  publiés »). Le texte est repris tel quel, sans changer ce qu'il fait.
⑨ CE QUI CLOCHE — —
⑩ EFFET — Aucun : lit seulement.
⑪ TERMINAISON — Rend la main. [sort: oui]
⑫ DÉFINITIONS
  un contrat : la liste des champs d'un fichier partagé, déclarée une fois dans
    `programmes/CONTRATS_DES_FICHIERS.py`.
"""
import importlib.util
import os
import sys


def main():
    """Charge les contrats et confronte tous les fichiers.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv[1]`, facultatif : la racine.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: oui]
    """
    base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_WORKSPACE", ".")
    sp = importlib.util.spec_from_file_location("c", os.path.join(base, "programmes", "CONTRATS_DES_FICHIERS.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    e = m.confronter_tous(base)
    for x in e:
        print("  !!", x)
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main())
