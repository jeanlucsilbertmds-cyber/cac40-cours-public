#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MESURER_L_ARRIVEE_DES_COURS_ABC — relève, minute par minute, ce qu'ABC Bourse montre autour de la clôture.

① RÔLE — Mesurer à quelle minute la séance du jour apparaît chez ABC Bourse, et à partir de quand ses chiffres
  (ouverture, plus haut, plus bas, clôture, volume) ne bougent plus. Lecture seule d'ABC ; écrit un relevé.
② CONTEXTE D'APPEL — L'essai du mercredi 14-10-2026 (A-579), lancé par le Chat réveillé à 17h28 par une tâche
  programmée. À la main : python3 programmes/MESURER_L_ARRIVEE_DES_COURS_ABC.py <racine> <minutes> <nombre de valeurs>
③ ENTRÉE — TROIS arguments : la racine du dépôt (pour le référentiel des valeurs) · la durée du relevé en minutes ·
  le nombre de valeurs relevées, prises dans l'ordre du référentiel.
④ CONDITIONS D'ENTRÉE — Le référentiel se lit par `lire_referentiel` de programmes/COLLECTER_ABC_GITHUB.py ; le
  réseau atteint www.abcbourse.com (vérifié depuis le Chat le 13-10-2026 à 23h38 : page de LVMH lue, 30 séances).
⑤ SORTIE — Le code de sortie : 0 si au moins une lecture a réussi, 1 sinon, 2 si les arguments sont faux. À l'écran,
  une ligne par tour. ÉCRIT `etudes/ESSAI_ARRIVEE_DES_COURS_ABC_<AAAA-MM-JJ>.csv` (une ligne par valeur et par
  tour, en AJOUT : relancé le même jour, il continue le même relevé).
⑥ TRAITEMENT — à chaque tour : ① lire l'heure de Paris · ② pour chaque valeur, télécharger sa page et en extraire
  les séances avec les fonctions MÊMES de la collecte (`telecharger`, `extraire`) · ③ écrire la séance la plus
  récente (date et chiffres), ou l'erreur · ④ attendre la minute suivante.
⑦ UNITÉ — Heures de Paris (HH:MM:SS) ; prix en euros ; volume en titres.
⑧ POURQUOI — Décision de Jean-Luc du 13-10-2026 à 23h39 (« 1 mais en autoportant ») : avant de décider si un
  calcul des signaux peut se faire entre 17h35 et 17h40 — la phase « trading at last » où un ordre s'exécute au
  cours de clôture —, mesurer quand ABC Bourse donne ce cours. Une seule observation existe : le 09-09-2026,
  la clôture du jour y était « horodatée 17h55 » (A-391), et la collecte refuse la ligne du jour avant 18h.
  Les fonctions de lecture sont celles de la collecte, et non une copie (R-708 : deux implémentations d'une
  même chose divergent toujours) : le relevé voit ce que la collecte verrait.
⑨ CE QUI CLOCHE — ① La page ne dit pas l'heure de la donnée : on mesure l'heure de LECTURE, pas celle de
  publication. ② Peu de valeurs (une page par seconde et demie, comme la collecte), pour ne pas marteler le site :
  un tour de 3 valeurs prend environ 5 secondes. ③ La clôture « définitive » se juge après coup, en comparant
  au relevé du soir (circuit de 18h07 ou plus tard).
⑩ EFFET — Lit ABC Bourse ; écrit (en ajout) un fichier CSV dans etudes/.
⑪ TERMINAISON — S'arrête après le nombre de minutes demandé ; chaque lecture a un délai de 30 secondes
  (`telecharger`). [sort: oui]
"""
import csv
import importlib.util
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
CHAMPS = ["lu_a", "valeur", "code", "seance", "open", "high", "low", "close", "volume", "erreur"]


def _collecte():
    """Charge programmes/COLLECTER_ABC_GITHUB.py comme module et le rend.

    ① RÔLE — Emprunter `telecharger`, `extraire`, `lire_referentiel` et la pause entre pages.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Le fichier est à côté de ce programme.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importer le fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : lire comme la collecte lit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe un module (la collecte n'agit qu'en `__main__`).
    ⑪ TERMINAISON — Rend la main, ou lève si l'import échoue.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("collecte_abc", os.path.join(ici, "COLLECTER_ABC_GITHUB.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    """Fait le relevé.

    ① RÔLE — Voir la fiche du fichier.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv[1:4]`.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du fichier.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir la fiche du fichier.
    ⑪ TERMINAISON — Rend la main après la durée demandée.
      [sort: non]
    """
    try:
        racine, minutes, combien = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    except (IndexError, ValueError):
        print(__doc__.split("\n")[0])
        print("usage : python3 programmes/MESURER_L_ARRIVEE_DES_COURS_ABC.py <racine> <minutes> <nombre de valeurs>")
        return 2
    C = _collecte()
    _, valeurs = C.lire_referentiel(racine)
    valeurs = [v for v in valeurs if v[2] == "PARIS"][:combien]
    debut = datetime.now(PARIS)
    sortie = os.path.join(racine, "etudes", f"ESSAI_ARRIVEE_DES_COURS_ABC_{debut:%Y-%m-%d}.csv")
    neuf = not os.path.isfile(sortie)
    reussies = 0
    with open(sortie, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CHAMPS)
        if neuf:
            w.writeheader()
        for tour in range(minutes):
            depart = time.monotonic()
            resume = []
            for nom, code, _place in valeurs:
                lu = datetime.now(PARIS).strftime("%H:%M:%S")
                ligne = {"lu_a": lu, "valeur": nom, "code": code}
                try:
                    seances, note = C.extraire(C.telecharger(f"https://www.abcbourse.com/cotation/{code}"))
                    if seances:
                        s = seances[0]
                        ligne.update(seance=s["date"], open=s["open"], high=s["high"], low=s["low"],
                                     close=s["close"], volume=s["volume"])
                        reussies += 1
                        resume.append(f"{code} {s['date']} {s['close']}")
                    else:
                        ligne["erreur"] = note or "aucune séance"
                        resume.append(f"{code} ERREUR")
                except Exception as e:
                    ligne["erreur"] = f"{type(e).__name__}: {str(e)[:80]}"
                    resume.append(f"{code} ERREUR")
                w.writerow(ligne)
                f.flush()
                time.sleep(C.PAUSE_ENTRE_PAGES)
            print(f"{datetime.now(PARIS):%H:%M:%S} tour {tour + 1}/{minutes} · " + " · ".join(resume), flush=True)
            if tour + 1 < minutes:
                time.sleep(max(0.0, 60 - (time.monotonic() - depart)))
    print(f"relevé : {os.path.relpath(sortie, racine)} · {reussies} lecture(s) réussie(s)")
    return 0 if reussies else 1


if __name__ == "__main__":
    sys.exit(main())
